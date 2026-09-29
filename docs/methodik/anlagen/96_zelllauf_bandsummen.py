#!/usr/bin/env python3
"""Zelllauf #96 für Berlin mit dem Produktcode: Bandsummen, Betroffene, Tage und Euro.

Anlage zu docs/methodik/96_aeroallergene.md, §3.0 („Kommune statt Zellen“) und Prüfblock
``rechenkette_96`` (Zeile ``zell = {…}``); Ledger reviews/BEFUNDE_96.md, Befunde 241 und 242.

Aufruf (über die Python-Umgebung des Produkts):

    bash scripts/testlauf.sh docs/methodik/anlagen/96_zelllauf_bandsummen.py -q -s

Was die Anlage rechnet, Schritt für Schritt:

  1. Zelldaten: die gepinnte Datei backend/data/kalibrierung/golden96_zellen_11000000.csv.gz
     (40.669 bewohnte 100-m-Zellen innerhalb der Gemeindegrenze Berlins, Zensus-Gitter 2022 und
     VG250; Beschreibung golden96_zellen.md). Es wird nichts geladen.
  2. Altersbänder je Zelle wie im Produkt: zensus_loader.apply_zensus_to_cell_inputs mit dem
     Gemeindeschlüssel 11000000, also mit der Ersatzregel aus Bericht #95 §3.3 für Zellen, deren
     Anteil 65+ im Gitter geheimgehalten ist (Stufe 1 aus den 5er-Jahresgruppen der Zelle, Stufe 2
     aus der Gemeindezeile der Regionaltabelle); u20 je Zelle aus den 5er-Jahresgruppen (§3.2).
  3. Bandsummen über alle Zellen. Berlin liegt in einer Region (δ in allen Zellen gleich), und der
     Vegetationsfaktor P̂ mittelt im Ausgangsstand auf 1 (§3.0 Ebene 7); Betroffene, Tage und Euro
     sind linear in der Bevölkerung je Band. Deshalb rechnet das Produkt die Summe über die
     Kommune genauso gut an den summierten Bändern (wie der Golden-Test
     backend/tests/test_methodik_96_golden_betraege.py).
  4. Betroffene, zusätzliche Symptomtage und Euro aus impact.compute_all_cell_impacts, Kostensatz je
     Symptomtag aus dem Katalog (6,20 €, Kap. 7 pollen.c_tag). Dasselbe für die Kette (Ebene 1 der
     Rechenkette) und die Zerlegung Zelllauf gegen Kette in Einwohnersumme und Altersbänder.

Die Testfunktion vergleicht die Ausgabe mit dem Bericht: Bänder in der Zeile ``zell = {…}`` des
Prüfblocks, Betroffene, Tage und Euro in §3.0. Weicht eine Zahl ab, endet der Aufruf mit Fehler.
Der Lauf ist deterministisch: dieselben Zelldaten und derselbe Code ergeben dieselben Zahlen.
"""
from __future__ import annotations

import ast
import csv
import gzip
import os
import re
import sys

HIER = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HIER, "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO, "backend"))

from app.data import catalog  # noqa: E402
from app.services import zensus_loader as zl  # noqa: E402
from app.services.engine import impact, override_context  # noqa: E402
from app.services.engine.impact.base import CellContext  # noqa: E402

AGS = "11000000"
DATEI = os.path.join(REPO, "backend", "data", "kalibrierung", f"golden96_zellen_{AGS}.csv.gz")
BERICHT = os.path.join(REPO, "docs", "methodik", "96_aeroallergene.md")
CODE = "EXPECTED_ANNUAL_ALLERGY_DAYS"
BANDS = ("u20", "a20_64", "a65_74", "a75_84", "a85p")
NAMEN = {"u20": "u20", "a20_64": "20-64", "a65_74": "65-74", "a75_84": "75-84", "a85p": "85+"}

# Ebene 1 der Rechenkette: Tab. 12411-09-01-4-B, 31.12.2023, Gemeinde Berlin (Bericht [68, 69])
U20 = 173_699 + 176_060 + 163_535 + 159_983
U65, A6574, A7584, A85P = 2_961_430, 339_490, 253_528, 107_933
KETTE = {"u20": U20, "a20_64": U65 - U20, "a65_74": A6574, "a75_84": A7584, "a85p": A85P}


def _zahl(s: str) -> float | None:
    return float(s) if s != "" else None


def _de(x: float, nk: int = 0) -> str:
    """Zahl in deutscher Schreibweise (Tausenderpunkt, Dezimalkomma)."""
    s = f"{x:,.{nk}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def zellen(ersatzregel_stufe2: bool = True) -> list[dict]:
    """Zelleingaben mit Altersbändern nach Produktlogik aus den gepinnten Zelldaten."""
    population, share65, ages, gids = {}, {}, {}, []
    with gzip.open(DATEI, "rt", newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            gid = r["gitter_id"]
            ages[gid] = {c: _zahl(r[c]) for c in zl.ALL_AGE_COLUMNS}
            if gid == "__ausserhalb__":   # nur für die gebietsweiten Rückfälle des Loaders
                continue
            gids.append(gid)
            population[gid] = {"Einwohner": float(r["einwohner"])}
            share65[gid] = {"AnteilUeber65": _zahl(r["anteil_ueber65"])}
    override_context.set_overrides({})
    cis = [{} for _ in gids]
    zl.apply_zensus_to_cell_inputs(
        cis, [{"gitter_id": g} for g in gids],
        {"population": population, "share_over_65": share65, "age_groups": ages}, AGS,
        ersatzregel_stufe2=ersatzregel_stufe2)
    return cis


def rechnen(bands: dict[str, float]) -> tuple[float, float, float]:
    """(Betroffene, Symptomtage, Euro je Jahr) aus dem Produkt für summierte Bänder."""
    b = {k: float(v) for k, v in bands.items()}
    b["u65"] = b["u20"] + b["a20_64"]
    ctx = CellContext(
        ci={"pop": sum(bands.values()), "pop_age_bands": b},
        hev={"hazards": {}, "exposures": {}, "vulnerabilities": {}},
        hev_norm={"hazards": {}, "exposures": {}, "vulnerabilities": {}},
        indices={}, regional={"bundesland": "Berlin"})
    override_context.set_overrides({})
    res = impact.compute_all_cell_impacts(ctx)[CODE]
    c_tag = catalog.risk_default_cost_per_outcome(catalog.RISKS_BY_CODE[CODE])
    return res["betroffene"], res["outcome"], res["outcome"] * c_tag


def messen(ersatzregel_stufe2: bool = True) -> dict:
    cis = zellen(ersatzregel_stufe2)
    bands = {b: sum(float(ci["pop_age_bands"][b]) for ci in cis) for b in BANDS}
    herkunft: dict[str, int] = {}
    for ci in cis:
        h = ci.get("share_over_65_herkunft") or "ohne"
        herkunft[h] = herkunft.get(h, 0) + 1
    betroffene, tage, euro = rechnen(bands)
    k_betroffene, k_tage, k_euro = rechnen(KETTE)
    return {"zellen": len(cis), "einwohner": sum(ci["pop"] for ci in cis), "bands": bands,
            "herkunft": herkunft, "betroffene": betroffene, "tage": tage, "euro": euro,
            "kette_betroffene": k_betroffene, "kette_euro": k_euro,
            "einwohner_kette": sum(KETTE.values())}


def ausgabe(m: dict) -> list[str]:
    f_ew = m["einwohner"] / m["einwohner_kette"]
    f_ges = m["betroffene"] / m["kette_betroffene"]
    f_alter = f_ges / f_ew
    return [
        f"Zelllauf #96 Berlin {AGS}: {_de(m['zellen'])} Zellen, {_de(m['einwohner'])} Einwohner, "
        f"Ersatzregel 65+ (#95 §3.3)",
        "Herkunft Anteil 65+: " + " · ".join(f"{k} {_de(v)} Zellen" for k, v in sorted(m["herkunft"].items())),
        "Bandsummen: " + " · ".join(f"{NAMEN[b]} {_de(m['bands'][b])}" for b in BANDS),
        f"Betroffene {_de(m['betroffene'], 2)} · Tage {_de(m['tage'], 2)} · Euro {_de(m['euro'], 2)} "
        f"({_de(m['euro'] / 1e6, 2)} Mio. €)",
        f"Kette {_de(m['kette_euro'], 2)} € ({_de(m['kette_euro'] / 1e6, 2)} Mio. €) · Zelllauf/Kette "
        f"{_de(f_ges, 4)} = Einwohnersumme {_de(f_ew, 4)} × Altersbänder {_de(f_alter, 4)}",
    ]


def _bericht_zell() -> dict[str, int]:
    """Zeile ``zell = {…}`` im Prüfblock rechenkette_96 des Berichts."""
    text = open(BERICHT, encoding="utf-8").read()
    block = re.search(r"```python test: rechenkette_96\n(.*?)```", text, re.S).group(1)
    zeile = re.search(r"^zell = (\{.*\})$", block, re.M).group(1)
    return ast.literal_eval(zeile.replace("_", ""))


def _abschnitt_30() -> str:
    text = open(BERICHT, encoding="utf-8").read()
    return text[text.index("### 3.0 Rechenkette"):text.index("### 3.1 ")]


def test_zelllauf_bandsummen():
    m = messen()
    for zeile in ausgabe(m):
        print(zeile)
    assert m["zellen"] == 40_669 and round(m["einwohner"]) == 3_593_357
    # Bänder im Prüfblock = gemessene Bänder, auf ganze Einwohner gerundet
    zell = _bericht_zell()
    assert zell == {NAMEN[b]: round(m["bands"][b]) for b in BANDS}, zell
    # Betroffene, Tage und Euro in §3.0 = gemessene Werte in der Rundung des Berichts
    s = _abschnitt_30()
    for wert in (_de(m["betroffene"]), _de(m["tage"])):
        assert re.search(re.escape(wert) + r"\s", s), wert
    assert f"**{_de(m['euro'] / 1e6, 2)} Mio. € je Jahr" in s
    assert abs(m["euro"] / 1e6 - 4.58) < 0.005


if __name__ == "__main__":
    for zeile in ausgabe(messen("--ohne-stufe2" not in sys.argv)):
        print(zeile)
