"""T-0449: Zuordnung jeder Klimawirkung zu einem KWRA-Systembereich (Checkliste Zeile 10).

Prüft ``catalog.RISK_SYSTEMBEREICH`` und ``systembereiche.systembereich_auswertung``:
(a) jeder Code aus ``catalog.RISKS_BY_CODE`` hat eine Zuordnung,
(b) die vorkommenden Werte sind eine Teilmenge der fünf KWRA-Systembereiche,
(c) die Summe der fünf Bereichssummen ist gleich der Gesamtsumme ohne die
    nicht-additiven Codes (``catalog.NON_ADDITIVE_RISK_CODES``).
"""

from __future__ import annotations

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.data import catalog  # noqa: E402
from app.services import systembereiche  # noqa: E402

FUENF = {
    "Natürliche Systeme und Ressourcen",
    "Naturnutzende Wirtschaftssysteme",
    "Infrastrukturen und Gebäude",
    "Naturferne Wirtschaftssysteme",
    "Menschen und soziale Systeme",
}


def test_a_jeder_risikocode_hat_eine_zuordnung():
    assert catalog.RISKS_BY_CODE, "Katalog ohne Risiken"
    fehlend = sorted(c for c in catalog.RISKS_BY_CODE if c not in catalog.RISK_SYSTEMBEREICH)
    assert not fehlend, f"Ohne Systembereich: {fehlend}"


def test_b_werte_sind_teilmenge_der_fuenf_systembereiche():
    assert set(catalog.KWRA_SYSTEMBEREICHE) == FUENF
    werte = set(catalog.RISK_SYSTEMBEREICH.values())
    assert werte <= FUENF, f"Unzulässige Werte: {sorted(werte - FUENF)}"


def test_c_bereichssummen_ergeben_gesamtsumme_ohne_nicht_additive():
    by_risk = [
        {"code": code, "cost_eur": 1000.0 * (i + 1), "index": 0.1 * (i + 1),
         "has_euro_layer": catalog.risk_has_euro_layer(spec)}
        for i, (code, spec) in enumerate(catalog.RISKS_BY_CODE.items())
    ]
    # Nicht-additive Sammelrisiken stehen im Aggregat, gehen aber nicht in die Summe.
    by_risk += [{"code": code, "cost_eur": 99_999.0, "index": 0.9, "has_euro_layer": True}
                for code in sorted(catalog.NON_ADDITIVE_RISK_CODES)]
    agg = {"cost": {"by_risk": by_risk}}

    gesamt = round(sum(
        r["cost_eur"] for r in by_risk
        if r["has_euro_layer"] and r["code"] not in catalog.NON_ADDITIVE_RISK_CODES
    ), 2)
    auswertung = systembereiche.systembereich_auswertung(agg)

    assert set(auswertung) == FUENF
    bereichssumme = round(sum(b["schadenskosten_eur"] or 0.0 for b in auswertung.values()), 2)
    assert bereichssumme == pytest.approx(gesamt)
    anzahl = sum(b["anzahl_klimawirkungen"] for b in auswertung.values())
    assert anzahl == len(catalog.RISKS_BY_CODE)
