"""Teil 6 des Ergebnisberichts: Maßnahme mit offenen Kosten (T-1720).

Setzt ``measure_service._stadtbaum_summary_fields`` ``kosten_nutzen_kennzahl_offen`` (Stadtbaumwahl
ohne gewählten Fall oder ohne Stückzahl), gibt es keine Kennzahl: ``nutzen_kosten`` ist None, der
Bericht führt „Kosten offen“ und nie ``math.inf`` („∞“, „inf“). Ohne das Flag bleibt es beim alten
Verhalten (CAPEX 0 → „ohne Kosten“).
"""

from __future__ import annotations

import datetime as dt
import math
import os
import sys
from types import SimpleNamespace

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HIER))

VERMERK = "Bitte Fall und Stückzahl wählen; ohne sie sind die Kosten offen."


def _summary(offen: bool) -> dict:
    s = {
        "measure_type": "HEAT_ACTION_PLANS", "affected_area_m2": 0.0,
        "capex_eur": 0.0, "opex_annual_eur": 0.0,
        "cost_breakdown": {"capex": {"components": []}, "opex": {"components": []}},
        "annual_benefit_damage_eur": 5_000.0, "annual_benefit_flat_eur": 0.0,
        "annual_benefit_direct_eur": 0.0, "annual_benefit_eur": 5_000.0,
    }
    if offen:
        s["kosten_nutzen_kennzahl_offen"] = True
        s["kosten_vermerk"] = VERMERK
    return s


def _zeile(offen: bool):
    from app.services.ergebnisbericht.massnahmen import massnahmenzeile
    return massnahmenzeile("HEAT_ACTION_PLANS", "Stadtbaumwahl", _summary(offen),
                           ort="Straßen", umsetzungsjahr=2027)


def _html(zeile) -> str:
    from app.services.ergebnisbericht.sammler import Stand
    from app.services.ergebnisbericht.teile import teil_6
    from app.services.ergebnisbericht.beispiel import beispiel
    d = SimpleNamespace(
        kommune=beispiel("warmsen"), massnahmen=[zeile],
        beziffert_text="1 von 3 Klimawirkungen in Euro beziffert",
        stand=Stand("Fassung 0.1", "#95", "M", "Zensus 2022", dt.date(2026, 9, 29)))
    return teil_6(d)


def test_kosten_offen_ohne_kennzahl():
    z = _zeile(True)
    assert z.capex_eur == 0.0
    assert z.nutzen_kosten is None
    html = _html(z)
    assert "Kosten offen" in html
    assert VERMERK in html
    assert "∞" not in html
    assert "inf" not in html.lower().replace("information", "").replace("infra", "")


def test_capex_null_ohne_flag_wie_bisher():
    z = _zeile(False)
    assert z.nutzen_kosten == math.inf
    html = _html(z)
    assert "ohne Kosten" in html
    assert "Kosten offen" not in html
