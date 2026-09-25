"""Diskontierung der Kostenprojektion (UBA Methodenkonvention 4.0, Kap. 2.2.3).

Deckt ab:
  (a) Die Reihe zur Diskontrate 0,0 ist elementweise gleich der
      undiskontierten ``cumulative``-Reihe — Abzinsen mit 0 % ändert nichts.
  (b) Der Endwert der Reihe zur Diskontrate 0,01 liegt unter dem Endwert von
      ``cumulative`` — mit 1 % Diskontrate ist der Barwert kleiner.
  (c) Die Zeichenfolge „keine Diskontierung" kommt in ``assumptions`` nicht
      mehr vor; die frühere Einschränkung ist aufgehoben.
  (d) ``assumptions`` benennt die Diskontrate von 0 % und 1 % und behauptet
      nicht, die Reine Zeitpräferenzrate sei der ausgewiesene Zinssatz.

Die Diskontrate ist hier gleich der Reinen Zeitpräferenzrate gesetzt; die
Komponente der relativen Preise ist nicht angesetzt.

Läuft ohne Datenbank: Aggregat, Klimaprojektion, Szenariofaktoren und
Maßnahmenabfrage werden ersetzt, ``db`` bleibt ungenutzt.
"""

from __future__ import annotations

import pytest

from app.services import cost_projection_service as cps

YEARS = list(range(2025, 2066))


class _FakeQuery:
    """Ersatz für ``kommune_measures_query(...)`` — Kommune ohne Maßnahmen."""

    def all(self):
        return []


def _fake_aggregate(db, kommune_id, apply_measures=False, demo_session_id=None):
    total = 800_000.0 if apply_measures else 1_000_000.0
    return {
        "cost": {
            "total_eur": total,
            "by_risk": [{"code": "TEST_RISK", "cost_eur": total}],
            "lower_bound": None,
        }
    }


def _fake_projection(bundesland):
    return {
        "years": YEARS,
        "scenarios": {
            "rcp45": {"label": "RCP4.5"},
            "rcp85": {"label": "RCP8.5"},
        },
        "source": "Testdaten",
    }


def _fake_scenario_factors(proj, scenario, group):
    # Leicht steigendes Klimasignal, damit jedes Jahr einen positiven Beitrag hat.
    return [1.0 + 0.01 * i for i in range(len(YEARS))]


@pytest.fixture
def projection(monkeypatch):
    monkeypatch.setattr(cps, "get_risk_aggregate", _fake_aggregate)
    monkeypatch.setattr(cps, "get_climate_projection", _fake_projection)
    monkeypatch.setattr(cps, "scenario_factors", _fake_scenario_factors)
    monkeypatch.setattr(cps, "kommune_measures_query",
                        lambda db, kommune_id, demo_session_id: _FakeQuery())
    return cps.project_costs(db=None, kommune_id=1, bundesland="SN")


def _pfade(projection):
    for scenario in ("rcp45", "rcp85"):
        for pfad in ("no_measures", "with_measures"):
            yield scenario, pfad, projection["scenarios"][scenario][pfad]


def test_rate_null_ist_die_undiskontierte_reihe(projection):
    """(a) Diskontrate 0 % reproduziert die kumulierte Reihe elementweise."""
    for scenario, pfad, block in _pfade(projection):
        assert set(block["discounted"]) == {"0.0", "0.01"}, (scenario, pfad)
        assert block["discounted"]["0.0"] == block["cumulative"], (scenario, pfad)


def test_rate_ein_prozent_senkt_den_endwert(projection):
    """(b) Diskontrate 1 % ergibt einen kleineren Barwert am Ende des Horizonts."""
    for scenario, pfad, block in _pfade(projection):
        assert block["discounted"]["0.01"][-1] < block["cumulative"][-1], (scenario, pfad)


def test_assumptions_ohne_keine_diskontierung(projection):
    """(c) Der Vorbehalt „keine Diskontierung" steht nicht mehr in den Annahmen."""
    for eintrag in projection["assumptions"]:
        assert "keine Diskontierung" not in eintrag, eintrag


def test_assumptions_nennen_die_diskontrate(projection):
    """(d) Die Annahmen sprechen von der Diskontrate, nicht von ausgewiesener RZPR."""
    assert any("Diskontrate von 0 % und 1 %" in e for e in projection["assumptions"])
    # Zeichenfolge geteilt, damit die Testdatei die alte Formulierung nicht selbst trägt.
    alt = "Reiner Zeitpräferenzrate" + " ausgewiesen"
    for eintrag in projection["assumptions"]:
        assert alt not in eintrag, eintrag
