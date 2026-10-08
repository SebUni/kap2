"""#98 Berlin: Jahresbetrag im Weg des Endpunkts cost-summary (T-1865-cto, Muster T-1484-cto).

Der Endpunkt GET /api/kommune/{id}/cost-summary reicht ``cost.by_risk`` unverändert aus
``risk_engine.aggregate`` weiter. ``aggregate`` monetarisiert das gespeicherte Outcome live; für
UV-Schädigungen gehören die Behandlungskosten der Zusatzfälle (Bericht #98, Ebene 10) dazu, die
``health.uv_yll`` in ``cost_eur`` addiert. Dieser Test bildet die Berliner Zelle aus ``_ctx_berlin()``
des Golden-Tests über ``impact.compute_all_cell_impacts`` und ``runner.build_cell_risks`` (der
gespeicherte Eintrag, den die Datenbank hält), füttert ``aggregate`` damit und prüft:

(a) genau eine Zeile ``kwra_id`` 98 in ``by_risk``, ``cost_eur`` auf 1 € gleich ``betrag_berlin()["summe_eur"]``
    (11,68 Mio. €);
(b) der gespeicherte Eintrag trägt ``eur_mm``, ``eur_c44``, ``yll_mm``, ``yll_c44``, und
    ``measure_service._s155_cell_effect`` liefert für ihn einen Euro-Betrag (kein Vermerk);
(c) der mit ``measure_service._scaled_cell_entry`` auf Faktor 0,5 skalierte Eintrag ergibt im Aggregat
    auf 1 € die Hälfte des Betrags aus (a).

Ohne Datenbank, ohne Server. Sichtbar mit ``-s``.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.data import catalog  # noqa: E402
from app.services import measure_service  # noqa: E402
from app.services.engine import impact, override_context, risk_engine, runner  # noqa: E402
from test_methodik_98_golden_betraege import CODE, _ctx_berlin, betrag_berlin  # noqa: E402

AREA_KM2 = 891.0


def _gespeicherte_zelle() -> tuple[dict, float]:
    """Der gespeicherte ``risks``-Eintrag der Berliner Zelle (Runner-Weg) und ihre Bevölkerung."""
    override_context.set_overrides({})
    ctx = _ctx_berlin()
    impacts = impact.compute_all_cell_impacts(ctx)
    risks = runner.build_cell_risks({CODE: 0.0}, {CODE: impacts[CODE]})
    return risks[CODE], ctx.pop


def _by_risk_98(eintrag: dict, pop: float) -> dict:
    zelle = {"inputs": {"pop": pop}, "risks": {CODE: eintrag}}
    by_risk = risk_engine.aggregate([zelle], pop, AREA_KM2)["cost"]["by_risk"]
    zeilen = [e for e in by_risk if e.get("kwra_id") == 98]
    assert len(zeilen) == 1, f"{len(zeilen)} Zeilen mit kwra_id 98 statt genau einer"
    return zeilen[0]


def test_berlin_by_risk_98():
    eintrag, pop = _gespeicherte_zelle()
    zeile = _by_risk_98(eintrag, pop)
    golden = betrag_berlin()["summe_eur"]
    cost_eur = zeile["cost_eur"]
    print(f"by_risk Berlin #98 ({zeile['code']}): cost_eur = {cost_eur:,.2f} € "
          f"({cost_eur / 1e6:.2f} Mio. €); Golden = {golden:,.2f} €")
    assert abs(cost_eur - golden) <= 1.0, f"Endpunktweg {cost_eur:.2f} € ≠ Golden {golden:.2f} €"
    assert catalog.RISKS_BY_CODE[CODE]["kwra_id"] == 98


def test_berlin_klimawirkung_98_eine_zeile():
    """Derselbe ``aggregate``-Lauf: ``klimawirkungen`` trägt genau einen Block #98 ohne Teile."""
    eintrag, pop = _gespeicherte_zelle()
    zelle = {"inputs": {"pop": pop}, "risks": {CODE: eintrag}}
    cost = risk_engine.aggregate([zelle], pop, AREA_KM2)["cost"]
    bloecke = [k for k in cost["klimawirkungen"] if k.get("kwra_id") == 98]
    assert len(bloecke) == 1, f"{len(bloecke)} Blöcke mit kwra_id 98 statt genau einem"
    block = bloecke[0]
    assert block["teile"] == []
    assert block["bezeichnung"].endswith("(#98)")
    zeile = [e for e in cost["by_risk"] if e.get("kwra_id") == 98]
    assert len(zeile) == 1
    print(f"klimawirkungen Berlin #98: bezeichnung = {block['bezeichnung']!r}, teile = {block['teile']}, "
          f"cost_eur = {block['cost_eur']:,.2f} €; by_risk = {zeile[0]['cost_eur']:,.2f} €")
    assert abs(block["cost_eur"] - zeile[0]["cost_eur"]) <= 1.0


def test_zelle_traegt_entitaetsschluessel_und_s155_rechnet():
    eintrag, _ = _gespeicherte_zelle()
    for key in ("eur_mm", "eur_c44", "yll_mm", "yll_c44"):
        assert key in eintrag, f"Schlüssel {key} fehlt im gespeicherten Eintrag"
    faktor, eur, fehlt = measure_service._s155_cell_effect(
        {"default_reduction": 0.10}, 1.0, eintrag)
    print(f"S155 Berlin-Zelle: Faktor {faktor:.6f}, € (MM, C44) = {eur}, Vermerk = {fehlt}")
    assert fehlt is False
    assert eur is not None and eur[0] > 0.0 and eur[1] > 0.0


def test_skalierter_eintrag_gibt_die_haelfte():
    eintrag, pop = _gespeicherte_zelle()
    voll = _by_risk_98(eintrag, pop)["cost_eur"]
    halb = _by_risk_98(measure_service._scaled_cell_entry(eintrag, 0.5), pop)["cost_eur"]
    print(f"by_risk Berlin #98 mit Faktor 0,5: cost_eur = {halb:,.2f} € (voll {voll:,.2f} €)")
    assert abs(halb - voll / 2.0) <= 1.0, f"{halb:.2f} € ≠ Hälfte von {voll:.2f} €"
