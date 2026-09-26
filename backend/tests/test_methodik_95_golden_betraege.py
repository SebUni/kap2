"""Golden-Test der Beträge #95 (Hitzebelastung, Bericht Rev. 8) an gepinnten Zelldaten.

Bindet die Jahresbeträge des Zelllaufs aus Bericht ``docs/methodik/95_hitzebelastung.md``
(§3.0 und Tabelle „Gemessene Wirkung“ in §3.3, Spalte „Jahresbetrag mit Regel“, Preisstand 2024)
an den Produktcode:

- Berlin (AGS 11000000): 342,67 Mio. € je Jahr, 707.318 Einwohner ab 65,
- Warmsen (AGS 03256034): 173.099 € je Jahr.

Gerechnet wird mit dem Produkt: Altersbänder je Zelle aus ``zensus_loader.apply_zensus_to_cell_inputs``
(mit der Ersatzregel §3.3 für den geheimgehaltenen Anteil 65+), Todesfälle, YLL und Einweisungen aus
``impact.health.mortality`` und ``impact.health.morbidity``, Kostensätze aus dem Katalog. Die Zelldaten
(Zensus-Gitter [67], DWD-Raster [33], Gemeindegrenze VG250 [65]) liegen gepinnt unter
``backend/data/kalibrierung/golden95_zellen_<AGS>.csv.gz``; erzeugt mit
``backend/scripts/golden_95_zelldaten.py`` (Beschreibung: ``golden95_zellen.md``).

Wie im Zelllauf des Berichts (Wirkung (d) in §3.0) gilt je Zelle der Rasterwert des Sommermittels mit
einer Feinstruktur σ = 0,5 K darunter, Gauß-Hermite mit 21 Punkten; sie wirkt nur auf die Mortalität.
Die Wärmeinsel-Abweichung aus OSM, mit der das Produkt diese Feinstruktur im Betrieb rechnet, ist nicht
Teil der gepinnten Daten.

Gemessen (26.09.2026): Das Produkt lädt die Wochenquantile aus ``wochenquantile_region.csv``
(vier Nachkommastellen) und kommt auf 342,58 Mio. € und 172.957 €. Mit der Tabelle §3.2 des Berichts
(zwei Nachkommastellen), wie sie der Zelllauf des Berichts nutzt, sind es 342,67 Mio. € und 173.099 €.
Die Differenz liegt in der Toleranz und ist als Divergenz an den CMO gemeldet (T-1366-cto).

Toleranzen: Berlin ± 1 Mio. € (Bericht §3.0, Prüfblock ``rechenkette_95``: ``… / 0.9867 - 343) < 1``);
Warmsen ± 505 €, dieselbe Toleranz relativ übertragen (1 / 342,67 × 173.099 €; Vorgabe CEO in
T-1350-ceo, Nachtrag 26.09.2026, bis zur Bestätigung durch den CMO in T-1351-ceo).
"""

from __future__ import annotations

import csv
import gzip
import math
import os
import sys
from functools import lru_cache

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.data import catalog  # noqa: E402
from app.services import zensus_loader as zl  # noqa: E402
from app.services.engine import override_context  # noqa: E402
from app.services.engine.impact import health as H  # noqa: E402
from app.services.engine.impact.base import CellContext  # noqa: E402

KALIB = os.path.join(os.path.dirname(__file__), "..", "data", "kalibrierung")
MORT, MORB = "EXPECTED_ANNUAL_MORTALITY", "EXPECTED_ANNUAL_MORBIDITY"
BANDS = ("u65", "a65_74", "a75_84", "a85p")
SPALTEN65 = ("a65bis69", "a70bis74", "a75bis79", "a80bis84", "a85bis89", "a90undaelter")
SIGMA_K = 0.5            # Feinstruktur unter 1 km (Bericht §3.0 (d), §4)
GH_PUNKTE = 21           # Gauß-Hermite wie docs/methodik/anlagen/95_zellvergleich.py

BERLIN, WARMSEN = "11000000", "03256034"
LAND = {BERLIN: "Berlin", WARMSEN: "Niedersachsen"}

# Zielwerte des Berichts (Tabelle §3.3, Zelllauf mit Ersatzregel, Preisstand 2024)
BERLIN_EUR, BERLIN_TOL = 342_670_000.0, 1_000_000.0
WARMSEN_EUR = 173_099.0
WARMSEN_TOL = round(BERLIN_TOL / BERLIN_EUR * WARMSEN_EUR)      # 505 €
BERLIN_AB65 = 707_318


def _zahl(s: str) -> float | None:
    return float(s) if s != "" else None


@lru_cache(maxsize=None)
def _zellen(ags: str):
    """Gepinnte Zelldaten → (Zellen mit Bändern nach Produktlogik, Summen)."""
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
    return gids, cell_inputs, klima


def _jahresbetrag(ags: str) -> float:
    """Σ YLL × VOLY + Σ Fälle × c_Fall über alle Zellen (€ je Jahr, Preisstand 2024).

    Mortalität und Morbidität sind linear in der Bevölkerung je Band; Zellen mit gleichem
    Rasterwert (Sommermittel, Hitzetage) werden daher vor dem Aufruf zusammengefasst."""
    gids, cis, klima = _zellen(ags)
    gruppen: dict[tuple[float, float], dict[str, float]] = {}
    for gid, ci in zip(gids, cis):
        acc = gruppen.setdefault(klima[gid], dict.fromkeys(BANDS, 0.0))
        for b in BANDS:
            acc[b] += float(ci["pop_age_bands"][b])

    import numpy as np
    xs, ws = np.polynomial.hermite.hermgauss(GH_PUNKTE)
    mort_risk, morb_risk = catalog.RISKS_BY_CODE[MORT], catalog.RISKS_BY_CODE[MORB]
    regional = {"bundesland": LAND[ags]}
    override_context.set_overrides({})
    yll = faelle = 0.0
    for (t, hd), bands in gruppen.items():
        def ctx(temp):
            return CellContext(
                ci={"pop": sum(bands.values()), "summer_temp_cell": temp, "pop_age_bands": bands},
                hev={"hazards": {"HEAT_WAVE": hd}, "exposures": {}, "vulnerabilities": {}},
                hev_norm={"hazards": {}, "exposures": {}, "vulnerabilities": {}},
                indices={}, regional=regional)
        yll += sum(w * H.mortality(mort_risk, ctx(t + math.sqrt(2) * SIGMA_K * x))["outcome"]
                   for x, w in zip(xs, ws)) / math.sqrt(math.pi)
        faelle += H.morbidity(morb_risk, ctx(t))["outcome"]
    return (yll * catalog.risk_default_cost_per_outcome(mort_risk)
            + faelle * catalog.risk_default_cost_per_outcome(morb_risk))


def test_zelldaten_gepinnt():
    """Die Anlage trägt die Zellen des Zelllaufs: Berlin 40.669 Zellen mit 3.593.357 Einwohnern
    (§3.0 (b)), Warmsen 3087 Einwohner mit 697 ab 65 nach der Ersatzregel (Tabelle §3.3)."""
    gids, cis, _ = _zellen(BERLIN)
    assert len(gids) == 40_669
    assert round(sum(ci["pop"] for ci in cis)) == 3_593_357
    gids, cis, _ = _zellen(WARMSEN)
    assert round(sum(ci["pop"] for ci in cis)) == 3087
    assert round(sum(ci["pop_over_65"] for ci in cis)) == 697


def test_berlin_einwohner_ab65():
    """Berlin: 707.318 Einwohner ab 65 in der Summe der Zellen (Tabelle §3.3, Ersatzregel)."""
    _, cis, _ = _zellen(BERLIN)
    assert round(sum(ci["pop_over_65"] for ci in cis)) == BERLIN_AB65
    assert round(sum(sum(ci["pop_age_bands"][b] for b in BANDS[1:]) for ci in cis)) == BERLIN_AB65


def test_berlin_jahresbetrag():
    """Berlin: 342,67 Mio. € je Jahr (Zelllauf mit Ersatzregel §3.3, Preisstand 2024), ± 1 Mio. €."""
    betrag = _jahresbetrag(BERLIN)
    assert abs(betrag - BERLIN_EUR) < BERLIN_TOL, f"{betrag / 1e6:.2f} Mio. €"


def test_warmsen_jahresbetrag():
    """Warmsen: 173.099 € je Jahr (Zelllauf mit Ersatzregel §3.3, Preisstand 2024), ± 505 €."""
    assert WARMSEN_TOL == 505
    betrag = _jahresbetrag(WARMSEN)
    assert abs(betrag - WARMSEN_EUR) < WARMSEN_TOL, f"{betrag:.0f} €"


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-q"]))
