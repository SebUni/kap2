"""#98 S155 und #96 S158: Nutzen im Aggregat wie im Bericht bewertet (T-1861-ceo, Vorhaben T-1662-ceo).

Der Maßnahmen-Nutzen (``annual_benefit_damage_eur``) ist je Zelle ``Zellkosten · (1 − Faktor)`` mit dem
Faktor aus ``measure_service._measure_cell_factor``; der Aggregatweg mit Maßnahmen skaliert den
gespeicherten Zelleintrag mit demselben Faktor (``measure_service._scaled_cell_entry``). Der Bericht
rechnet den Nutzen anders: S155 mit ``W_e = BAF_e · h · €_e`` je Krebsart (Bericht #98 §5, Ebene 10:
verlorene Lebensjahre × VOLY plus Behandlungskosten je Fall), S158 mit vermiedenen Tagen × c_Tag.
Dieser Test misst für Berlin ohne Datenbank, dass beide Wege auf 1 % übereinstimmen:

(a) S155: Zellnutzen = ``s155_avoided_eur`` (Summe ``_s155_cell_effect``, wie ``_s155_summary_fields``);
(b) S155: Delta des Aggregats (``risk_engine.aggregate``) ohne/mit skaliertem Eintrag = dieselbe Zahl;
(c) S158: Zellnutzen = vermiedene Tage × c_Tag (wie ``cell_savings["s158_avoided_eur"]``).

Die Berliner Zelle für #98 ist die des Golden-Tests (``_ctx_berlin``, Runner-Eintrag); für #96 die Zelle
der Kette mit den Berliner Bändern (``POP_KETTE``), p̂ = 1 — S158 ist in den Tagen linear, die Quote
vermiedene/Zusatztage ist von der Zellgröße unabhängig. Ohne Datenbank, sichtbar mit ``-s``.
"""

from __future__ import annotations

import os
import sys
from importlib import import_module

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.data import catalog  # noqa: E402
from app.services import measure_service as ms  # noqa: E402
from app.services.engine import impact, override_context, risk_engine, runner  # noqa: E402

_b98 = import_module("test_methodik_98_golden_betraege")
_b96 = import_module("test_methodik_96_golden_betraege")
_ep98 = import_module("test_methodik_98_endpunkt_berlin")

CODE_96 = "EXPECTED_ANNUAL_ALLERGY_DAYS"
TOL = 0.01          # 1 % (Abnahmekriterium T-1861-ceo)


def _nutzen(mdef: dict, code: str, eintrag: dict, pop: float) -> float:
    """``annual_benefit_damage_eur`` einer Zelle (Zellschleife von ``measure_service``), ohne Datenbank."""
    risk = catalog.RISKS_BY_CODE[code]
    r = ms._with_cell_q_pfl(eintrag, {"pop": pop})
    faktor = ms._measure_cell_factor(mdef, None, code, 1.0, 1.0, r)
    return ms._cell_cost(risk, r, pop) * (1.0 - faktor)


def _abweichung(nutzen: float, bericht: float) -> float:
    return (nutzen - bericht) / bericht


def test_s155_berlin_zellnutzen_gleich_bericht():
    eintrag, pop = _ep98._gespeicherte_zelle()
    mdef = catalog.MEASURES_BY_CODE["UV_PROTECTION_PUBLIC_SPACE"]
    _, eur, fehlt = ms._s155_cell_effect(mdef, 1.0, eintrag)
    assert fehlt is False and eur is not None
    bericht = ms._s155_summary_fields(mdef, eur[0], eur[1], False)["s155_avoided_eur"]
    nutzen = _nutzen(mdef, _b98.CODE, eintrag, pop)
    ab = _abweichung(nutzen, bericht)
    print(f"S155 Berlin: annual_benefit_damage_eur {nutzen:,.2f} € | s155_avoided_eur {bericht:,.2f} € "
          f"| Abweichung {100 * ab:+.4f} %")
    assert abs(ab) <= TOL, f"{100 * ab:+.4f} %"


def test_s155_berlin_aggregat_delta_gleich_bericht():
    eintrag, pop = _ep98._gespeicherte_zelle()
    mdef = catalog.MEASURES_BY_CODE["UV_PROTECTION_PUBLIC_SPACE"]
    _, eur, _ = ms._s155_cell_effect(mdef, 1.0, eintrag)
    faktor = ms._measure_cell_factor(mdef, None, _b98.CODE, 1.0, 1.0, eintrag)
    ohne = _ep98._by_risk_98(eintrag, pop)["cost_eur"]
    mit = _ep98._by_risk_98(ms._scaled_cell_entry(eintrag, faktor), pop)["cost_eur"]
    delta = ohne - mit
    ab = _abweichung(delta, eur[0] + eur[1])
    print(f"S155 Berlin: Aggregat ohne {ohne:,.2f} € − mit {mit:,.2f} € = {delta:,.2f} € "
          f"| Bericht {eur[0] + eur[1]:,.2f} € | Abweichung {100 * ab:+.4f} %")
    assert abs(ab) <= TOL, f"{100 * ab:+.4f} %"


def test_s155_basiswert_unveraendert():
    """Der Basiswert #98 Berlin (Golden, T-1821-cto) hängt nicht am Maßnahmenfaktor."""
    eintrag, pop = _ep98._gespeicherte_zelle()
    zeile = _ep98._by_risk_98(eintrag, pop)
    assert abs(zeile["cost_eur"] - _b98.betrag_berlin()["summe_eur"]) <= 1.0
    assert abs(zeile["cost_eur"] / 1e6 - 11.68) < 0.005


def test_s158_berlin_zellnutzen_gleich_bericht():
    override_context.set_overrides({})
    ctx = _b96._ctx(_b96.POP_KETTE)
    roh = impact.compute_all_cell_impacts(ctx)[CODE_96]
    eintrag = runner.build_cell_risks({CODE_96: 0.0}, {CODE_96: roh})[CODE_96]
    mdef = catalog.MEASURES_BY_CODE["POLLEN_EARLY_WARNING"]
    _, tage, fehlt = ms._s158_cell_effect(mdef, 1.0, eintrag)
    assert fehlt is False and tage is not None and tage > 0.0
    bericht = risk_engine.cost_from_outcome(catalog.RISKS_BY_CODE[CODE_96], tage)
    nutzen = _nutzen(mdef, CODE_96, eintrag, ctx.pop)
    ab = _abweichung(nutzen, bericht)
    print(f"S158 Berlin (Kette): annual_benefit_damage_eur {nutzen:,.2f} € | s158_avoided_eur "
          f"{bericht:,.2f} € | Abweichung {100 * ab:+.4f} %")
    assert abs(ab) <= TOL, f"{100 * ab:+.4f} %"
