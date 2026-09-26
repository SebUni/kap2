"""Kostentabelle je Klimawirkung: ``kwra_id`` in ``cost.by_risk`` (T-1432-ceo).

Die Tabelle „Erwartete Schäden je Risiko“ (frontend CostTablesSection) fasst Zeilen mit derselben
``kwra_id`` zu einer Summenzeile zusammen. Dieser Test prüft die Grundlage im Aggregat auf denselben
gepinnten Berliner Zelldaten wie ``test_methodik_95_endpunkt_berlin.py``:

(a) jede Zeile von ``by_risk`` trägt das Feld ``kwra_id`` (Zahl oder ``None``),
(b) genau die Zeilen „Hitzebelastung — Mortalität“ und „Hitzebelastung — Erkrankungen“ tragen 95,
(c) die Summe ihrer ``cost_eur`` liegt in derselben Toleranz um die Werte, die der Endpunkt-Test für
    die beiden Zeilen zusammen prüft (Golden-Jahresbetrag auf 1 € genau, Bericht §3.0 ± BERLIN_TOL).

Ohne Datenbank, ohne Server.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.services.engine import override_context  # noqa: E402
from app.services.engine import risk_engine  # noqa: E402
from test_methodik_95_endpunkt_berlin import _aggregat_zellen  # noqa: E402
from test_methodik_95_golden_betraege import (  # noqa: E402
    BERLIN, BERLIN_EUR, BERLIN_TOL, _jahresbetrag,
)

NAMEN_95 = {"Hitzebelastung — Mortalität", "Hitzebelastung — Erkrankungen"}


def _by_risk_berlin() -> list[dict]:
    override_context.set_overrides({})
    zellen, pop = _aggregat_zellen(BERLIN)
    return risk_engine.aggregate(zellen, pop, 891.0)["cost"]["by_risk"]


def test_jede_zeile_traegt_kwra_id():
    by_risk = _by_risk_berlin()
    assert by_risk
    for zeile in by_risk:
        assert "kwra_id" in zeile, zeile["code"]
        assert zeile["kwra_id"] is None or isinstance(zeile["kwra_id"], int), zeile


def test_genau_mortalitaet_und_erkrankungen_tragen_95():
    by_risk = _by_risk_berlin()
    namen = {z["name"] for z in by_risk if z["kwra_id"] == 95}
    assert namen == NAMEN_95
    assert sum(1 for z in by_risk if z["kwra_id"] == 95) == 2


def test_summe_95_wie_endpunkt_test():
    by_risk = _by_risk_berlin()
    summe = sum(z["cost_eur"] for z in by_risk if z["kwra_id"] == 95)
    print(f"Summenzeile #95 Berlin: {summe:,.2f} € ({summe / 1e6:.2f} Mio. €)")
    golden = _jahresbetrag(BERLIN)
    assert abs(summe - golden) <= 1.0, f"Summe {summe:.2f} € ≠ Golden {golden:.2f} €"
    assert abs(summe - BERLIN_EUR) <= BERLIN_TOL, f"{summe / 1e6:.2f} Mio. €"
