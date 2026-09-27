"""``klimawirkungen(by_risk)``: eine Regel für jede Klimawirkung, im Backend (T-1470-cto).

Dieselbe Gruppierung wie ``bloecke()`` im Frontend (``CostTablesSection.tsx``, T-1432-ceo), aber im
Backend, damit auch Verbraucher außerhalb des Dashboards (Kartenebenen, Exporte) auf einen Blick
sehen, was zu welcher amtlichen Klimawirkung gehört: amtlicher Name, Nummer und Jahresbetrag als ein
Eintrag je Klimawirkung.

Rechnet mit Zeilen aus den beiden Katalogcodes mit ``kwra_id`` 95 (Hitzebelastung: Mortalität +
Morbidität) und ``EXPECTED_ANNUAL_ALLERGY_DAYS`` (kwra_id 96, Aeroallergene) — die Beträge sind frei
erfunden, nur die Codes und ``kwra_id``-Zuordnung stammen aus dem Katalog. Ohne Datenbank, ohne
Server.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.services import measure_service  # noqa: E402
from app.services.dashboard_cache import _SUMMARY_SCHEMA_VERSION  # noqa: E402
from app.services.klimawirkungen import klimawirkungen  # noqa: E402

ZEILE_MORTALITAET = {
    "code": "EXPECTED_ANNUAL_MORTALITY", "name": "Hitzebelastung — Mortalität",
    "kwra_id": 95, "cost_eur": 1000.0, "has_euro_layer": True,
}
ZEILE_MORBIDITAET = {
    "code": "EXPECTED_ANNUAL_MORBIDITY", "name": "Hitzebelastung — Erkrankungen",
    "kwra_id": 95, "cost_eur": 500.0, "has_euro_layer": True,
}
ZEILE_ALLERGIE = {
    "code": "EXPECTED_ANNUAL_ALLERGY_DAYS", "name": "Aeroallergene — zusätzliche Symptomtage",
    "kwra_id": 96, "cost_eur": 200.0, "has_euro_layer": True,
}


def _by_risk() -> list[dict]:
    return [dict(ZEILE_MORTALITAET), dict(ZEILE_MORBIDITAET), dict(ZEILE_ALLERGIE)]


def test_genau_ein_eintrag_fuer_95_mit_summe_und_zwei_teilen():
    eintraege = klimawirkungen(_by_risk())
    treffer_95 = [e for e in eintraege if e["kwra_id"] == 95]
    assert len(treffer_95) == 1, eintraege
    eintrag = treffer_95[0]
    assert eintrag["bezeichnung"] == "Hitzebelastung (#95)"
    assert eintrag["cost_eur"] == 1500.0
    assert len(eintrag["teile"]) == 2


def test_eintrag_96_traegt_amtlichen_namen_und_keine_teile():
    eintraege = klimawirkungen(_by_risk())
    treffer_96 = [e for e in eintraege if e["kwra_id"] == 96]
    assert len(treffer_96) == 1, eintraege
    eintrag = treffer_96[0]
    assert eintrag["bezeichnung"] == (
        "Allergische Reaktionen durch Aeroallergene pflanzlicher Herkunft (#96)"
    )
    assert eintrag["teile"] == []


def test_fehlende_kwra_id_wird_aus_dem_katalog_ergaenzt():
    zeile_ohne_kwra_id = {"code": "EXPECTED_ANNUAL_ALLERGY_DAYS",
                          "name": "Aeroallergene — zusätzliche Symptomtage",
                          "cost_eur": 200.0, "has_euro_layer": True}
    eintraege = klimawirkungen([zeile_ohne_kwra_id])
    assert len(eintraege) == 1
    assert eintraege[0]["kwra_id"] == 96
    assert eintraege[0]["bezeichnung"] == (
        "Allergische Reaktionen durch Aeroallergene pflanzlicher Herkunft (#96)"
    )


def test_build_cost_summary_und_get_risk_aggregate_tragen_cost_klimawirkungen(monkeypatch):
    by_risk = _by_risk()
    fake_aggregat = {
        "cost": {"total_eur": 1700.0, "by_risk": by_risk,
                  "klimawirkungen": klimawirkungen(by_risk),
                  "euro_coverage": {"covered": 3, "total": 3, "text": "3 von 3"}},
    }
    monkeypatch.setattr(measure_service, "get_risk_aggregate",
                        lambda *a, **k: fake_aggregat)
    monkeypatch.setattr(measure_service, "kommune_measures_query",
                        lambda *a, **k: type("Q", (), {"all": lambda self: []})())

    ergebnis = measure_service.build_cost_summary(db=None, kommune_id=1)
    assert ergebnis["klimawirkungen"] == klimawirkungen(by_risk)
    assert fake_aggregat["cost"]["klimawirkungen"] == klimawirkungen(by_risk)


def test_schema_version_ist_2():
    assert _SUMMARY_SCHEMA_VERSION == 2
