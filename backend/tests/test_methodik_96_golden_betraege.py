"""Golden-Test der Beträge #96 (Aeroallergene) an Rechenkette und gepinnten Zelldaten.

Bindet die Jahresbeträge aus Bericht ``docs/methodik/96_aeroallergene.md`` §3.0 (Beispielkommune
Berlin, Preisstand 2024) an den Produktcode:

(i)  Rechenkette mit den Altersbändern aus Ebene 1 (Fortschreibung 31.12.2023): 402.103 Betroffene,
     755.753 zusätzliche Symptomtage, 4,69 Mio. € je Jahr (Prüfblock ``rechenkette_96``, Z. 379, 396, 406).
(ii) Zelllauf über die 40.669 bewohnten 100-m-Zellen innerhalb der Gemeindegrenze mit der Ersatzregel
     #95 §3.3 für den geheimgehaltenen Anteil 65+: 4,58 Mio. € je Jahr (``rechenkette_96``, Z. 432).

Gerechnet wird mit dem Produkt: Altersbänder je Zelle aus ``zensus_loader.apply_zensus_to_cell_inputs``
(u20 je Zelle aus den 5er-Jahresgruppen, §3.2), Symptomtage und Euro aus
``impact.compute_all_cell_impacts``, Kostensatz je Symptomtag aus dem Katalog. Die Zelldaten
(Zensus-Gitter [67], Gemeindegrenze VG250 [65]) liegen gepinnt unter
``backend/data/kalibrierung/golden96_zellen_11000000.csv.gz``; erzeugt mit
``backend/scripts/golden_96_zelldaten.py`` (Beschreibung: ``golden96_zellen.md``).

Ohne Vegetationsreferenz bleibt P̂ = 1. Das ist im Ausgangsstand für die Summe über die Kommune exakt:
P̂ ist auf das betroffenengewichtete Mittel der eigenen Zellen zentriert (§3.0 Ebene 7), die Summe
hängt nicht von der Vegetation ab. Symptomtage und Euro sind linear in der Bevölkerung je Band, und
Berlin liegt in einer Region (δ in allen Zellen gleich); die Zellbänder werden deshalb vor dem Aufruf
summiert.

Toleranzen aus dem Prüfblock ``rechenkette_96``: Betroffene und Tage ± 1, Euro ± 0,005 Mio. €.
"""

from __future__ import annotations

import csv
import gzip
import os
import sys
from functools import lru_cache

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.data import catalog  # noqa: E402
from app.services import zensus_loader as zl  # noqa: E402
from app.services.engine import impact, override_context  # noqa: E402
from app.services.engine.impact.base import CellContext  # noqa: E402

KALIB = os.path.join(os.path.dirname(__file__), "..", "data", "kalibrierung")
CODE = "EXPECTED_ANNUAL_ALLERGY_DAYS"
BANDS = ("u20", "a20_64", "a65_74", "a75_84", "a85p")
BERLIN = "11000000"

# Ebene 1 der Rechenkette: Tab. 12411-09-01-4-B, 31.12.2023, Gemeinde Berlin [68, 69]
U20 = 173_699 + 176_060 + 163_535 + 159_983
U65, A6574, A7584, A85P = 2_961_430, 339_490, 253_528, 107_933
POP_KETTE = {"u20": U20, "a20_64": U65 - U20, "a65_74": A6574, "a75_84": A7584, "a85p": A85P}

# Zielwerte des Berichts (§3.0, Prüfblock rechenkette_96)
KETTE_BETROFFENE = 402_103       # Z. 379
KETTE_TAGE = 755_753             # Z. 396
KETTE_EUR_MIO = 4.69             # Z. 406
ZELL_EUR_MIO = 4.58              # Z. 432, Zelllauf mit Ersatzregel
TOL_ANZAHL, TOL_MIO = 1, 0.005


def _ctx(bands: dict[str, float]) -> CellContext:
    b = {k: float(v) for k, v in bands.items()}
    b["u65"] = b["u20"] + b["a20_64"]
    return CellContext(
        ci={"pop": sum(bands.values()), "pop_age_bands": b},
        hev={"hazards": {}, "exposures": {}, "vulnerabilities": {}},
        hev_norm={"hazards": {}, "exposures": {}, "vulnerabilities": {}},
        indices={}, regional={"bundesland": "Berlin"})


def _rechnen(bands: dict[str, float]) -> tuple[float, float, float]:
    """(Betroffene, Symptomtage, € je Jahr) aus dem Produkt; € = Tage × Katalog-Kostensatz."""
    override_context.set_overrides({})
    res = impact.compute_all_cell_impacts(_ctx(bands))[CODE]
    c_tag = catalog.risk_default_cost_per_outcome(catalog.RISKS_BY_CODE[CODE])
    euro = res["outcome"] * c_tag
    assert abs(euro - res["cost_eur"]) < 1e-6 * max(1.0, euro)
    return res["betroffene"], res["outcome"], euro


def _zahl(s: str) -> float | None:
    return float(s) if s != "" else None


@lru_cache(maxsize=None)
def _zellen(ags: str):
    """Gepinnte Zelldaten → (Kennungen, Zelleingaben mit Bändern nach Produktlogik)."""
    pfad = os.path.join(KALIB, f"golden96_zellen_{ags}.csv.gz")
    population, share65, ages, gids = {}, {}, {}, []
    with gzip.open(pfad, "rt", newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            gid = r["gitter_id"]
            ages[gid] = {c: _zahl(r[c]) for c in zl.ALL_AGE_COLUMNS}
            if gid == "__ausserhalb__":   # nur für die gebietsweiten Rückfälle
                continue
            gids.append(gid)
            population[gid] = {"Einwohner": float(r["einwohner"])}
            share65[gid] = {"AnteilUeber65": _zahl(r["anteil_ueber65"])}
    override_context.set_overrides({})
    cell_inputs = [{} for _ in gids]
    zl.apply_zensus_to_cell_inputs(
        cell_inputs, [{"gitter_id": g} for g in gids],
        {"population": population, "share_over_65": share65, "age_groups": ages}, ags)
    return gids, cell_inputs


def _zellbaender(ags: str) -> dict[str, float]:
    _, cis = _zellen(ags)
    return {b: sum(float(ci["pop_age_bands"][b]) for ci in cis) for b in BANDS}


# ── (i) Rechenkette §3.0 ─────────────────────────────────────────────────────

def test_kette_kostensatz_katalog():
    """Ebene 9: Katalog-Kostensatz 6,20 € je Symptomtag (Kap. 7 pollen.c_tag)."""
    assert catalog.risk_default_cost_per_outcome(catalog.RISKS_BY_CODE[CODE]) == pytest.approx(6.20)


def test_kette_berlin():
    """Ebenen 1–10: 402.103 Betroffene, 755.753 Tage, 4,69 Mio. € je Jahr (Preisstand 2024)."""
    assert sum(POP_KETTE.values()) == 3_662_381
    betroffene, tage, euro = _rechnen(POP_KETTE)
    assert abs(betroffene - KETTE_BETROFFENE) < TOL_ANZAHL, f"{betroffene:.1f}"
    assert abs(tage - KETTE_TAGE) < TOL_ANZAHL, f"{tage:.1f}"
    assert abs(euro / 1e6 - KETTE_EUR_MIO) < TOL_MIO, f"{euro / 1e6:.4f} Mio. €"


# ── (ii) Zelllauf Berlin an den gepinnten Zelldaten ──────────────────────────

def test_zelldaten_gepinnt():
    """Dieselben Zellen wie #95: 40.669 Zellen mit 3.593.357 Einwohnern (§3.0)."""
    gids, cis = _zellen(BERLIN)
    assert len(gids) == 40_669
    assert round(sum(ci["pop"] for ci in cis)) == 3_593_357
    assert round(sum(_zellbaender(BERLIN).values())) == 3_593_357


def test_zelllauf_berlin():
    """Zelllauf mit Ersatzregel: 4,58 Mio. € je Jahr (Preisstand 2024), ± 0,005 Mio. €."""
    _, _, euro = _rechnen(_zellbaender(BERLIN))
    assert abs(euro / 1e6 - ZELL_EUR_MIO) < TOL_MIO, f"{euro / 1e6:.4f} Mio. €"


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-q"]))
