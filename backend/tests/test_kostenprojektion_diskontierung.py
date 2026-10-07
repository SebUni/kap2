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
  (e) ``diskontierung.diskontraten`` ist je Schlüssel RZPR + Komponente der
      relativen Preise.
  (f) Mit der Komponente 0,01 (monkeypatch) ist ``discounted["0.0"]``
      elementweise gleich ``discounted["0.01"]`` bei Komponente 0, und ihr
      Endwert liegt unter dem von ``cumulative``.
  (g) ``RELATIVE_PRICE_COMPONENT_SPEC`` ist als Abschätzung von KAP3
      gekennzeichnet, ``MODELLGRENZEN`` nennt die drei Grenzen mit Seite.
  (h) ``test_komponente_gilt_nur_fuer_m0_gesundheit``: Die Komponente trifft nur
      Risiken mit ``kwra_id`` 95, 96 oder 98; Übriges, OPEX und CAPEX werden mit
      der RZPR allein abgezinst, ``diskontraten_uebrige`` ist je RZPR die RZPR.

Diskontrate = Reine Zeitpräferenzrate (0 % und 1 %) + Komponente der relativen
Preise (``app.data.diskontierung``, vorläufig 0 Pp.).

Läuft ohne Datenbank: Aggregat, Klimaprojektion, Szenariofaktoren und
Maßnahmenabfrage werden ersetzt, ``db`` bleibt ungenutzt.
"""

from __future__ import annotations

import pytest

from app.data import diskontierung
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


def _fake_aggregate_m0(db, kommune_id, apply_measures=False, demo_session_id=None):
    """Wie ``_fake_aggregate``, aber das Risiko trägt einen Katalogeintrag mit
    ``kwra_id`` 95 (Gruppe ``heat``) und zählt damit zu den Gesundheitsschäden von M0."""
    total = 800_000.0 if apply_measures else 1_000_000.0
    return {
        "cost": {
            "total_eur": total,
            "by_risk": [{"code": "EXPECTED_ANNUAL_MORTALITY", "cost_eur": total}],
            "lower_bound": None,
        }
    }


M0_ANTEIL = {False: 600_000.0, True: 480_000.0}      # #95 ohne / mit Maßnahmen
UEBRIGER_ANTEIL = {False: 400_000.0, True: 320_000.0}  # TEST_RISK, ohne M0-Bezug


def _fake_aggregate_gemischt(db, kommune_id, apply_measures=False, demo_session_id=None):
    """Aggregat aus #95 (M0) und TEST_RISK (kein Katalogeintrag, kein M0-Bezug)."""
    m0 = M0_ANTEIL[bool(apply_measures)]
    rest = UEBRIGER_ANTEIL[bool(apply_measures)]
    return {
        "cost": {
            "total_eur": m0 + rest,
            "by_risk": [
                {"code": "EXPECTED_ANNUAL_MORTALITY", "cost_eur": m0},
                {"code": "TEST_RISK", "cost_eur": rest},
            ],
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


def test_diskontraten_sind_rzpr_plus_komponente(projection):
    """(e) Diskontrate je Schlüssel = RZPR + Komponente der relativen Preise."""
    block = projection["diskontierung"]
    komponente = diskontierung.RELATIVE_PRICE_COMPONENT
    assert block["rzpr"] == list(diskontierung.PURE_TIME_PREFERENCE_RATES)
    assert block["relative_preise"]["wert"] == komponente
    assert block["relative_preise"]["evidence_class"] == "abgeschaetzt"
    assert block["relative_preise"]["begruendung"]
    assert block["modellgrenzen"] == diskontierung.MODELLGRENZEN
    assert set(block["diskontraten"]) == {str(r) for r in block["rzpr"]}
    for r in block["rzpr"]:
        assert block["diskontraten"][str(r)] == pytest.approx(r + komponente)
    # Schlüssel wie im Feld ``discounted``
    for _, _, pfad in _pfade(projection):
        assert set(pfad["discounted"]) == set(block["diskontraten"])
    # Die Annahmen nennen die Zusammensetzung.
    assert any("Diskontrate = Reine Zeitpräferenzrate" in e
               and "Komponente der relativen Preise" in e
               for e in projection["assumptions"])


def test_komponente_verschiebt_die_diskontrate(projection, monkeypatch):
    """(f) Komponente 0,01: Reihe zur RZPR 0 % = Reihe zur RZPR 1 % bei Komponente 0."""
    # Die Komponente gilt nur für M0-Gesundheit: Das Aggregat trägt dafür ein
    # Katalogrisiko mit kwra_id 95; ``projection`` ist damit die Vergleichsreihe
    # bei Komponente 0.
    monkeypatch.setattr(cps, "get_risk_aggregate", _fake_aggregate_m0)
    projection = cps.project_costs(db=None, kommune_id=1, bundesland="SN")
    monkeypatch.setattr(diskontierung, "RELATIVE_PRICE_COMPONENT", 0.01)
    mit_komponente = cps.project_costs(db=None, kommune_id=1, bundesland="SN")
    assert mit_komponente["diskontierung"]["diskontraten"]["0.0"] == pytest.approx(0.01)
    for scenario, pfad, block in _pfade(mit_komponente):
        ohne = projection["scenarios"][scenario][pfad]
        assert block["discounted"]["0.0"] == ohne["discounted"]["0.01"], (scenario, pfad)
        assert block["discounted"]["0.0"][-1] < block["cumulative"][-1], (scenario, pfad)


def test_komponente_gilt_nur_fuer_m0_gesundheit(monkeypatch):
    """(h) Komponente 0,01 trifft nur den M0-Anteil (#95); der übrige Anteil, OPEX
    und CAPEX werden mit der RZPR allein abgezinst."""
    from types import SimpleNamespace

    massnahme = SimpleNamespace(
        id=1, name="Testmaßnahme",
        impact_summary={"capex_eur": 100_000.0, "opex_annual_eur": 5_000.0},
        implementation_year=2030, measure_type="TEST_MASSNAHME", config={},
    )

    class _QueryMitMassnahme:
        def all(self):
            return [massnahme]

    monkeypatch.setattr(cps, "get_risk_aggregate", _fake_aggregate_gemischt)
    monkeypatch.setattr(cps, "get_climate_projection", _fake_projection)
    monkeypatch.setattr(cps, "scenario_factors", _fake_scenario_factors)
    monkeypatch.setattr(cps, "kommune_measures_query",
                        lambda db, kommune_id, demo_session_id: _QueryMitMassnahme())
    monkeypatch.setattr(diskontierung, "RELATIVE_PRICE_COMPONENT", 0.01)
    ergebnis = cps.project_costs(db=None, kommune_id=1, bundesland="SN")

    faktoren = _fake_scenario_factors(None, "rcp45", "heat")
    for scenario, pfad, block in _pfade(ergebnis):
        mit = pfad == "with_measures"
        # Handrechnung: M0-Anteil mit 1 % abgezinst, Übriges (und Maßnahmenkosten) nicht.
        erwartet, laufend = [], 0.0
        for i, jahr in enumerate(YEARS):
            m0 = M0_ANTEIL[mit] * faktoren[i] / 1.01 ** i
            uebrig = UEBRIGER_ANTEIL[mit] * faktoren[i]
            if mit:
                uebrig += 5_000.0 if jahr >= 2030 else 0.0  # OPEX ab Umsetzungsjahr
                uebrig += 100_000.0 if jahr == 2030 else 0.0  # CAPEX einmalig
            laufend += m0 + uebrig
            erwartet.append(laufend)
        ist = block["discounted"]["0.0"]
        assert len(ist) == len(erwartet), (scenario, pfad)
        for jahr, a, b in zip(YEARS, ist, erwartet):
            assert a == pytest.approx(b, abs=0.01), (scenario, pfad, jahr)
        if mit:
            # Die Maßnahmenkosten der Handrechnung stimmen mit den Komponenten überein;
            # abgezinst werden sie in der Handrechnung oben nicht.
            assert block["components"]["capex"][YEARS.index(2030)] == 100_000.0
            assert block["components"]["opex"][-1] == 5_000.0

    diskontierung_block = ergebnis["diskontierung"]
    assert diskontierung_block["relative_preise"]["gilt_fuer_kwra"] == [95, 96, 98]
    assert set(diskontierung_block["diskontraten_uebrige"]) == set(diskontierung_block["diskontraten"])
    for r in diskontierung_block["rzpr"]:
        assert diskontierung_block["diskontraten_uebrige"][str(r)] == pytest.approx(r)
        assert diskontierung_block["diskontraten"][str(r)] == pytest.approx(r + 0.01)


def test_spec_und_modellgrenzen():
    """(g) Die Komponente ist als Abschätzung gekennzeichnet; Modellgrenzen mit Seite."""
    assert diskontierung.PURE_TIME_PREFERENCE_RATES == (0.0, 0.01)
    assert cps.PURE_TIME_PREFERENCE_RATES is diskontierung.PURE_TIME_PREFERENCE_RATES
    assert diskontierung.RELATIVE_PRICE_COMPONENT == 0.0
    spec = diskontierung.RELATIVE_PRICE_COMPONENT_SPEC
    for feld in ("label", "unit", "source", "source_detail"):
        assert isinstance(spec[feld], str) and spec[feld].strip(), feld
    assert spec["evidence_class"] == "abgeschaetzt"
    for feld in ("wert", "band", "sensitivitaet"):
        assert spec["evidence_derivation"][feld].strip(), feld

    grenzen = diskontierung.MODELLGRENZEN
    assert isinstance(grenzen, list) and grenzen
    for satz in grenzen:
        assert "Methodenkonvention 4.0" in satz and "S. " in satz, satz
    for stichworte in (("Richtung", "offen"), ("Risikoaversion",),
                       ("Finanzmärkten", "Grenznutzen der Betroffenen")):
        treffer = [s for s in grenzen if all(w in s for w in stichworte)]
        assert treffer, stichworte
        assert all("S. 15" in s for s in treffer), stichworte
