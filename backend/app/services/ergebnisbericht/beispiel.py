"""Beispielkommunen des PDF-Ergebnisberichts (Formatpilot, T-1414).

Eine Beispielkommune rechnet ohne Datenbank: Ihre Zelldaten liegen gepinnt unter
``backend/data/kalibrierung/golden95_zellen_<AGS>.csv.gz`` (Zensus-Gitter, DWD-Raster,
Gemeindegrenze VG250; Beschreibung in ``golden95_zellen.md``). Der Jahresbetrag #95 entsteht
wie im Produkt über die Schicht-B-Funktionen ``impact.health.mortality`` und
``impact.health.morbidity``, mit derselben Aufbereitung der Altersbänder
(``zensus_loader.apply_zensus_to_cell_inputs`` samt Ersatzregel 65+) und derselben
Feinstruktur unter 1 km wie der Zelllauf des Berichts (σ = 0,5 K, Gauß-Hermite mit 21 Punkten,
nur auf die Mortalität) — also dieselbe Rechnung wie ``tests/test_methodik_95_golden_betraege.py``.
"""

from __future__ import annotations

import csv
import gzip
import math
import os
from dataclasses import dataclass, field
from functools import lru_cache

KALIB = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "kalibrierung")

MORT, MORB = "EXPECTED_ANNUAL_MORTALITY", "EXPECTED_ANNUAL_MORBIDITY"
BANDS = ("u65", "a65_74", "a75_84", "a85p")
SPALTEN65 = ("a65bis69", "a70bis74", "a75bis79", "a80bis84", "a85bis89", "a90undaelter")
SIGMA_K = 0.5
GH_PUNKTE = 21


@dataclass(frozen=True)
class Beispielkommune:
    kennung: str
    name: str
    ags: str
    kreis: str
    bundesland: str


BEISPIELE: dict[str, Beispielkommune] = {
    "warmsen": Beispielkommune(
        kennung="warmsen", name="Warmsen", ags="03256034",
        kreis="Landkreis Nienburg (Weser)", bundesland="Niedersachsen"),
}


@dataclass
class Ergebnis95:
    """Jahresergebnis #95 der Beispielkommune (Preisstand 2024)."""
    einwohner: float
    einwohner_ab65: float
    zellen: int
    todesfaelle: float
    yll: float
    einweisungen: float
    voly_eur: float
    c_fall_eur: float
    betrag_mortalitaet_eur: float
    betrag_morbiditaet_eur: float
    band_voly_eur: tuple[float, float] | None = None
    hitzetage_mittel: float = 0.0
    t_sommer_mittel: float = 0.0
    extra: dict = field(default_factory=dict)

    @property
    def jahresbetrag_eur(self) -> float:
        return self.betrag_mortalitaet_eur + self.betrag_morbiditaet_eur

    @property
    def band_eur(self) -> tuple[float, float] | None:
        """Band des Jahresbetrags aus dem Band des Kostensatzes je Lebensjahr."""
        if not self.band_voly_eur:
            return None
        lo, hi = self.band_voly_eur
        return (self.yll * lo + self.betrag_morbiditaet_eur,
                self.yll * hi + self.betrag_morbiditaet_eur)


def beispiel(kennung: str) -> Beispielkommune:
    try:
        return BEISPIELE[kennung.lower()]
    except KeyError:
        raise KeyError(
            f"Unbekannte Beispielkommune {kennung!r}; verfügbar: {', '.join(sorted(BEISPIELE))}"
        ) from None


def _zahl(s: str) -> float | None:
    return float(s) if s != "" else None


@lru_cache(maxsize=None)
def zellen(ags: str):
    """Gepinnte Zelldaten → (Zellkennungen, Zell-Inputs mit Altersbändern, Klima je Zelle)."""
    from app.services import zensus_loader as zl
    from app.services.engine import override_context

    pfad = os.path.join(KALIB, f"golden95_zellen_{ags}.csv.gz")
    population, share65, ages, klima, gids = {}, {}, {}, {}, []
    with gzip.open(pfad, "rt", newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            gid = r["gitter_id"]
            ages[gid] = {c: _zahl(r[c]) for c in SPALTEN65}
            if gid == "__ausserhalb__":   # nur für die gebietsweite Aufteilung 65+
                continue
            gids.append(gid)
            population[gid] = {"Einwohner": float(r["einwohner"])}
            share65[gid] = {"AnteilUeber65": _zahl(r["anteil_ueber65"])}
            klima[gid] = (float(r["t_sommer"]), float(r["hitzetage"]))
    override_context.set_overrides({})
    cell_inputs = [{} for _ in gids]
    zl.apply_zensus_to_cell_inputs(
        cell_inputs, [{"gitter_id": g} for g in gids],
        {"population": population, "share_over_65": share65, "age_groups": ages}, ags)
    return tuple(gids), cell_inputs, klima


def _band_aus_text(text: str | None) -> tuple[float, float] | None:
    """Liest „136.400–165.600 …“ aus der Herleitung des Kostensatzes."""
    import re
    m = re.search(r"(\d{1,3}(?:\.\d{3})+)\s*[–-]\s*(\d{1,3}(?:\.\d{3})+)", text or "")
    if not m:
        return None
    return tuple(float(g.replace(".", "")) for g in m.groups())  # type: ignore[return-value]


def rechne_95(kommune: Beispielkommune) -> Ergebnis95:
    """Jahresbetrag #95 über die Schicht-B-Funktionen des Produkts."""
    import numpy as np

    from app.data import catalog
    from app.services.engine import override_context
    from app.services.engine.impact import health as H
    from app.services.engine.impact.base import CellContext

    gids, cis, klima = zellen(kommune.ags)
    gruppen: dict[tuple[float, float], dict[str, float]] = {}
    for gid, ci in zip(gids, cis):
        acc = gruppen.setdefault(klima[gid], dict.fromkeys(BANDS, 0.0))
        for b in BANDS:
            acc[b] += float(ci["pop_age_bands"][b])

    xs, ws = np.polynomial.hermite.hermgauss(GH_PUNKTE)
    mort_risk, morb_risk = catalog.RISKS_BY_CODE[MORT], catalog.RISKS_BY_CODE[MORB]
    regional = {"bundesland": kommune.bundesland}
    override_context.set_overrides({})
    yll = tote = faelle = 0.0
    for (t, hd), bands in gruppen.items():
        def ctx(temp, bands=bands, hd=hd):
            return CellContext(
                ci={"pop": sum(bands.values()), "summer_temp_cell": temp, "pop_age_bands": bands},
                hev={"hazards": {"HEAT_WAVE": hd}, "exposures": {}, "vulnerabilities": {}},
                hev_norm={"hazards": {}, "exposures": {}, "vulnerabilities": {}},
                indices={}, regional=regional)
        for x, w in zip(xs, ws):
            out = H.mortality(mort_risk, ctx(t + math.sqrt(2) * SIGMA_K * x))
            yll += w * out["outcome"] / math.sqrt(math.pi)
            tote += w * out["deaths"] / math.sqrt(math.pi)
        faelle += H.morbidity(morb_risk, ctx(t))["outcome"]

    voly = catalog.risk_default_cost_per_outcome(mort_risk)
    c_fall = catalog.risk_default_cost_per_outcome(morb_risk)
    pop = sum(float(ci["pop"]) for ci in cis)
    pop65 = sum(float(ci["pop_over_65"]) for ci in cis)
    gew = [(klima[g], float(ci["pop"])) for g, ci in zip(gids, cis)]
    return Ergebnis95(
        einwohner=pop, einwohner_ab65=pop65, zellen=len(gids),
        todesfaelle=tote, yll=yll, einweisungen=faelle,
        voly_eur=voly, c_fall_eur=c_fall,
        betrag_mortalitaet_eur=yll * voly, betrag_morbiditaet_eur=faelle * c_fall,
        band_voly_eur=_band_aus_text(
            (mort_risk.get("cost_evidence_derivation") or {}).get("band")),
        t_sommer_mittel=sum(k[0] * p for k, p in gew) / pop if pop else 0.0,
        hitzetage_mittel=sum(k[1] * p for k, p in gew) / pop if pop else 0.0,
    )
