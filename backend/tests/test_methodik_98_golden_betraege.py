"""Golden-Test des Jahresbetrags #98 (UV-Schädigungen) an der Rechenkette Berlin.

Bindet die Beträge aus Bericht ``docs/methodik/98_uv_schaedigungen.md`` §3.0 (Beispielkommune
Berlin, Preisstand 2024) an die Produktfunktion ``health.uv_yll``, nicht an eine eigene Formel:

- Altersbänder nach Ebene 1 (Z. 301, Frauen und Männer zusammen, 3.662.381 Einwohner),
- ΔSSD +7,165 % (Ebene 4, Z. 304) als ``ssd_ref``/``ssd_neu`` der Zelle,
- Ziele Ebene 10 (Z. 368, 370): MM 5,14 Mio. €, C44 6,53 Mio. €, Summe 11,68 Mio. € je Jahr.

Toleranz aus dem Prüfblock ``rechenkette_98``: Euro ± 0,005 Mio. € (Fälle ± 0,05).
Die Bevölkerung am Gemeindepunkt (3.586.909, Bericht §3.0, Abweichungsliste) bindet dieser Test
nicht: Sie beschreibt die Populationsbasis des Modells (Anlage [72], §6 Modellgrenze 8), keinen
Produktwert (Befund 505 im Ledger 98).
"""

from __future__ import annotations

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.data import catalog  # noqa: E402
from app.services.engine import override_context  # noqa: E402
from app.services.engine.impact import health as H  # noqa: E402
from app.services.engine.impact.base import CellContext  # noqa: E402

CODE = "EXPECTED_ANNUAL_UV_YLL"

# Ebene 1 (Z. 301): Frauen + Männer je Band, Stichtag 31.12.2023 [75]
_F = (328_114, 1_137_634, 182_741, 146_451, 71_032)
_M = (345_163, 1_150_519, 156_749, 107_077, 36_901)
BANDS = ("u20", "a20_64", "a65_74", "a75_84", "a85p")
POP_BERLIN = {b: float(f + m) for b, f, m in zip(BANDS, _F, _M)}

# Ebene 4 (Z. 304): ΔSSD +7,165 %
SSD_REF, SSD_NEU = 1000.0, 1071.65

# Ziele (Z. 368, 370) und Toleranzen des Prüfblocks rechenkette_98
ZIEL_MM_MIO, ZIEL_C44_MIO, ZIEL_SUMME_MIO = 5.14, 6.53, 11.68
TOL_MIO = 0.005

# Kapitel-7-Werte für die Aufteilung nach Krebsart (Ebene 7–9)
LAM = {"mm": 0.11466, "c44": 0.005236}
L_REST = {"mm": 10.4569, "c44": 5.4787}
C_FALL = {"mm": 6724.0, "c44": 5883.0}
VOLY = 160_800.0


def _ctx_berlin() -> CellContext:
    b = dict(POP_BERLIN)
    b["u65"] = b["u20"] + b["a20_64"]
    return CellContext(
        ci={"pop": sum(POP_BERLIN.values()), "pop_age_bands": b,
            "ssd_ref": SSD_REF, "ssd_neu": SSD_NEU},
        hev={"hazards": {"UV_RADIATION": SSD_NEU}, "exposures": {}, "vulnerabilities": {}},
        hev_norm={"hazards": {}, "exposures": {}, "vulnerabilities": {}},
        indices={}, regional={"bundesland": "Berlin"})


def betrag_berlin() -> dict:
    """Jahresbetrag Berlin über ``health.uv_yll`` (für Paket 7/7 importierbar).

    Liefert ``mm_eur``, ``c44_eur``, ``summe_eur`` (Preisstand 2024) sowie ``cases_mm``,
    ``cases_c44`` und das Produktergebnis ``res``.
    """
    override_context.set_overrides({})
    risk = catalog.RISKS_BY_CODE[CODE]
    res = H.uv_yll(risk, _ctx_berlin())
    d = {"mm": res["cases_melanoma"], "c44": res["cases_c44"]}
    eur = {k: d[k] * C_FALL[k] + d[k] * LAM[k] * L_REST[k] * VOLY for k in d}
    return {"mm_eur": eur["mm"], "c44_eur": eur["c44"], "summe_eur": res["cost_eur"],
            "cases_mm": d["mm"], "cases_c44": d["c44"], "res": res}


def test_bevoelkerung_ebene_1():
    assert sum(POP_BERLIN.values()) == 3_662_381


def test_zusatzfaelle_ebene_6():
    r = betrag_berlin()
    assert abs(r["cases_mm"] - 25.8) < 0.05
    assert abs(r["cases_c44"] - 622.3) < 0.05


def test_betrag_mm_c44_ebene_10():
    r = betrag_berlin()
    assert abs(r["mm_eur"] / 1e6 - ZIEL_MM_MIO) < TOL_MIO, f"{r['mm_eur']:.0f}"
    assert abs(r["c44_eur"] / 1e6 - ZIEL_C44_MIO) < TOL_MIO, f"{r['c44_eur']:.0f}"


def test_summe_berlin_produktfunktion():
    r = betrag_berlin()
    assert abs(r["summe_eur"] / 1e6 - ZIEL_SUMME_MIO) < TOL_MIO, f"{r['summe_eur']:.0f}"
    # Aufteilung und Produkt-Gesamtbetrag stimmen überein
    assert r["summe_eur"] == pytest.approx(r["mm_eur"] + r["c44_eur"], rel=1e-9)
