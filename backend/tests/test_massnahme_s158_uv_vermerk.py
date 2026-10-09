"""T-1937-cto: Förderung der Früherkennung von Hautkrebs (#98 S158) — Vermerk statt Betrag.

Bericht #98 §5, Integrationsauflage: „Für S158 braucht das Produkt keine Zahl, sondern den
Vermerk ‚Kostenwirkung im Basiswert voll angerechnet‘“; Abschnitt S158: „Vorgabe an das
Produkt ist deshalb keine Nullwirkung, sondern der Vermerk …“ (Log 34, Befund 502,
Vorgabe P2). Der Code S158 gehört im Katalog schon der Pollen-Frühwarnung (#96); die
Maßnahme zu #98 führt den Code ``SKIN_CANCER_EARLY_DETECTION``.

Geprüft wird:

(a) Katalog: aktive Maßnahme, eigener Code, qualitativ mit ``EXPECTED_ANNUAL_UV_YLL``
    verknüpft (kein Wirkungskanal), Quelle Bericht #98 §5 und Log 34, kein Kostenansatz.
(b) ``measure_service.compute_impact`` (volle Rechenkette, Session-Doppel wie in
    ``test_massnahme_s158_ausgabe.py``): ``benefit_display`` ist der Vermerk wörtlich, und
    es entsteht kein Euro-Zahlenfeld für den Nutzen — weder ``annual_benefit_*_eur`` noch
    ein anderes Nutzenfeld, auch keines mit dem Wert 0 (P2: nie 0 €).
(c) Je Zelle entsteht kein Euro-Betrag.

DB-frei (Session-Doppel); ``_coverage`` (PostGIS) wird mit festen Werten ersetzt.
"""

from __future__ import annotations

from app.data import catalog
from app.models.models import AdaptationMeasure, CellAssessment, ConfigParameter, Kommune
from app.services import measure_service, parameter_registry

CODE = "SKIN_CANCER_EARLY_DETECTION"
RISK = "EXPECTED_ANNUAL_UV_YLL"
VERMERK = "Kostenwirkung im Basiswert voll angerechnet"
KOMMUNE_ID = 1


class _Q:
    def __init__(self, rows):
        self._rows = list(rows)

    def filter(self, *a, **k):
        return self

    def all(self):
        return list(self._rows)

    def first(self):
        return self._rows[0] if self._rows else None

    def delete(self):
        return 0

    def scalar(self):
        return None


class _DB:
    def __init__(self, rows):
        self._rows = rows
        self.added: list = []

    def query(self, model, *a, **k):
        return _Q(self._rows.get(model, []))

    def add(self, obj):
        self.added.append(obj)

    def commit(self):
        pass


def _run(monkeypatch) -> tuple[dict, list]:
    measure = AdaptationMeasure(
        id=1, kommune_id=KOMMUNE_ID, name="Früherkennung Test", measure_type=CODE,
        geometry=None, config={}, implementation_year=2027, description="",
        impact_summary={})
    kommune = Kommune(id=KOMMUNE_ID, name="Testheim", osm_id="R-S158UV", population=10_000,
                      area_km2=5.0)
    assessments = [
        CellAssessment(id=cid, kommune_id=KOMMUNE_ID, grid_cell_id=cid,
                       data={"risks": {RISK: {"index": 0.4, "outcome": 3.0}},
                             "inputs": {"pop": 100.0}})
        for cid in (10, 11)
    ]
    db = _DB({AdaptationMeasure: [measure], CellAssessment: assessments,
             ConfigParameter: [], Kommune: [kommune]})
    monkeypatch.setattr(measure_service, "_coverage",
                        lambda _db, _m: ({10: 1.0, 11: 0.5}, 1000.0))
    monkeypatch.setattr(measure_service, "_params_fingerprint", lambda *a, **k: "fp-test-s158uv")
    monkeypatch.setattr(parameter_registry, "load_db_overrides", lambda *a, **k: [])
    monkeypatch.setattr(measure_service, "get_risk_aggregate",
                        lambda *a, **k: {"risks": {RISK: {"cost_eur": 1_000_000.0}}})
    summary = measure_service.compute_impact(db, measure.id)
    return summary, db.added


# ── (a) Katalog ──────────────────────────────────────────────────────────────────

def test_katalog_massnahme_zu_98_mit_eigenem_code():
    m = catalog.MEASURES_BY_CODE[CODE]
    assert m in catalog.MEASURES                      # aktiv, nicht geparkt
    assert m["name"] == "Förderung der Früherkennung von Hautkrebs (S158)"
    assert CODE != "POLLEN_EARLY_WARNING"             # der Code S158 der #96 bleibt dort


def test_katalog_qualitativ_verknuepft_ohne_wirkungskanal():
    m = catalog.MEASURES_BY_CODE[CODE]
    assert m["qualitative_risk_codes"] == [RISK]
    assert m["linked_risk_codes"] == []
    assert m["default_reduction"] is None             # keine Zahl, keine Nullwirkung


def test_katalog_quelle_bericht_und_log_ohne_kostenansatz():
    m = catalog.MEASURES_BY_CODE[CODE]
    assert "Bericht #98 §5" in m["source"]
    assert "Log 34" in m["source"]
    for feld in ("capex_fixed", "capex_per_unit", "capex_per_m2", "opex_fixed_year",
                 "opex_per_unit_year", "opex_per_m2_year", "benefit_per_m2_year"):
        assert m[feld] is None, feld                  # der Bericht nennt keine Kostenansätze


# ── (b) Ergebnis: Vermerk wörtlich, kein Euro-Nutzen ────────────────────────────

def test_vermerk_steht_wortlich_in_benefit_display(monkeypatch):
    assert measure_service.UV_FRUEHERKENNUNG_VERMERK == VERMERK
    summary, _ = _run(monkeypatch)
    assert summary["benefit_display"] == "Kostenwirkung im Basiswert voll angerechnet"
    assert summary["benefit_has_euro_layer"] is False
    assert summary["linked_risk_codes"] == []


def test_kein_euro_zahlenfeld_fuer_den_nutzen_mit_wert_null(monkeypatch):
    summary, _ = _run(monkeypatch)
    nutzenfelder = {k: v for k, v in summary.items()
                    if "benefit" in k and k.endswith("_eur")}
    assert nutzenfelder == {}, nutzenfelder           # kein 0 € (und kein anderer Betrag)
    for feld in measure_service.UV_FRUEHERKENNUNG_OHNE_NUTZEN_FELDER:
        assert feld not in summary
    # Auch sonst trägt die Zusammenfassung kein Euro-Zahlenfeld mit 0 zum Nutzen
    # (Kennzahlen wie s155_*/s158_* entstehen für diese Maßnahme nicht).
    assert not [k for k in summary if k.startswith(("s155_", "s158_", "stadtbaum_"))]
    assert not [k for k, v in summary.items()
                if isinstance(v, (int, float)) and not isinstance(v, bool)
                and v == 0 and "benefit" in k]


# ── (c) je Zelle kein Euro-Betrag ───────────────────────────────────────────────

def test_zellzeilen_ohne_euro_betrag(monkeypatch):
    _, added = _run(monkeypatch)
    assert added
    for zeile in added:
        assert not (zeile.savings or {})
        assert not (zeile.indicator_deltas or {})
