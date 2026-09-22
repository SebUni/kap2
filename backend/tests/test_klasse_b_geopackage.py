"""GeoPackage-Export: Klasse B trägt den Screening-Vermerk statt 0 (T-0515).

Verwechslungssperre Klasse A/B (T-0358): Eine Wirkung ohne Euro-Schicht
(Katalogeintrag ``"euro_layer": False``) darf in der Spalte ``<code>_cost_eur``
des Layers ``bewertung_100m`` keine 0 zeigen — ein GIS-Nutzer läse sie als
„kein Schaden". Dort steht je Zelle ``catalog.NO_EURO_LAYER_TEXT``.

Geprüft wird:
(1) die reine Funktion ``cost_column_values``: Klasse B → nur Vermerk,
    Euro-Schicht → unverändert float;
(2) ``build_geopackage`` gegen ein Session-Doppel mit abgefangenem
    ``_write_layer``: die an ``bewertung_100m`` übergebene Klasse-B-Spalte
    enthält ausschließlich den Vermerk, keinen Wert 0, 0.0, '-' oder None.

Ohne Datenbank und ohne pyogrio (fehlt in der Prüfumgebung).
"""

from __future__ import annotations

import sys
import types

import pytest

import _stub_heavy_deps

# Muss vor dem Import der App-Module laufen (nur wirksam, wo die echten Pakete
# fehlen — im Deploy-Venv passiert nichts).
_stub_heavy_deps.install()

# Der Export importiert ``from shapely import wkb``; das Ersatzmodul für shapely
# bildet ``wkb`` nicht ab. Nur ergänzen, wenn shapely selbst ersetzt ist.
if "shapely.wkb" not in sys.modules and not hasattr(sys.modules.get("shapely"), "wkb"):
    _wkb = types.ModuleType("shapely.wkb")
    _wkb.dumps = lambda g: b""
    sys.modules["shapely.wkb"] = _wkb
    sys.modules["shapely"].wkb = _wkb

from app.data import catalog  # noqa: E402
from app.models.models import CellAssessment, GridCell, Kommune  # noqa: E402
from app.services import geodata_export_service as gx  # noqa: E402

KLASSE_B_CODE = "TEST_KLASSE_B_GEOPACKAGE"
VERMERK = "Screening ohne Euro-Bezifferung"


def _klasse_b_eintrag() -> dict:
    return {
        "code": KLASSE_B_CODE,
        "name": "Testwirkung Klasse B (Screening)",
        "group": "health",
        "outcome_unit": "Fälle/Jahr",
        "ref_value": 10.0,
        "scale": "pop",
        "cost_per_outcome_eur": 1000.0,
        "cost_dimension": "health",
        "cost_source": "Testquelle",
        "euro_layer": False,
    }


# ── (1) reine Funktion ───────────────────────────────────────────────────────

def test_reine_funktion_klasse_b_liefert_nur_vermerk():
    werte = gx.cost_column_values(_klasse_b_eintrag(), [0.0, 0, 125.5])
    assert isinstance(werte, list)
    assert len(werte) == 3
    assert all(w == VERMERK for w in werte)
    assert catalog.NO_EURO_LAYER_TEXT == VERMERK


def test_reine_funktion_euro_schicht_bleibt_float():
    risk = next(r for r in catalog.RISKS if catalog.risk_has_euro_layer(r))
    werte = gx.cost_column_values(risk, [0.0, 3, 125.5])
    assert isinstance(werte, list)
    assert werte == [0.0, 3.0, 125.5]
    assert all(type(w) is float for w in werte)


# ── (2) build_geopackage gegen Session-Doppel ────────────────────────────────

class _FakeQuery:
    def __init__(self, rows):
        self._rows = list(rows)

    def filter(self, *a, **k):
        return self

    def join(self, *a, **k):
        return self

    def yield_per(self, *a, **k):
        return self

    def first(self):
        return self._rows[0] if self._rows else None

    def count(self):
        return len(self._rows)

    def __iter__(self):
        return iter(self._rows)


class _FakeDB:
    """Minimale Session: liefert je Modellklasse eine feste Zeilenliste."""

    def __init__(self, rows: dict):
        self._rows = rows

    def query(self, model, *a, **k):
        return _FakeQuery(self._rows.get(model, []))


@pytest.fixture
def geschriebene_layer(monkeypatch, tmp_path):
    """Lässt build_geopackage mit einem Klasse-B-Eintrag laufen und sammelt die
    Aufrufe von ``_write_layer`` je Layername."""
    klasse_b = _klasse_b_eintrag()
    monkeypatch.setattr(catalog, "RISKS", list(catalog.RISKS) + [klasse_b])

    daten = {"risks": {KLASSE_B_CODE: {"index": 40.0, "outcome": 1.0, "cost_eur": 0.0}}}
    zeilen = [
        (CellAssessment(data=daten), GridCell(gitter_id="G1", x_3035=1.0, y_3035=2.0, geometry=object())),
        (CellAssessment(data=daten), GridCell(gitter_id="G2", x_3035=3.0, y_3035=4.0, geometry=object())),
        # Zelle ganz ohne Wert für die Wirkung → Standard 0.0 im Rohwert
        (CellAssessment(data={}), GridCell(gitter_id="G3", x_3035=5.0, y_3035=6.0, geometry=object())),
    ]
    kommune = Kommune(id=1, name="Testkommune", bundesland="SN", area_km2=2.0,
                      population=500, boundary=object())
    # query(CellAssessment, GridCell) nimmt das erste Argument als Schlüssel.
    db = _FakeDB({Kommune: [kommune], CellAssessment: zeilen})

    monkeypatch.setattr(gx, "assessment_is_done", lambda db, kid: True)
    monkeypatch.setattr(gx, "_build_output_path", lambda kid, eid: str(tmp_path / "t.gpkg"))
    monkeypatch.setattr(gx, "to_shape", lambda g: types.SimpleNamespace(geom_type="Polygon"))

    aufrufe: dict = {}

    def _abgefangen(path, layer, geometries, field_data, fields, **kw):
        aufrufe[layer] = dict(zip(fields, field_data))

    monkeypatch.setattr(gx, "_write_layer", _abgefangen)
    gx.build_geopackage(db, 1, 1)
    return aufrufe


def test_bewertung_100m_klasse_b_spalte_traegt_nur_vermerk(geschriebene_layer):
    spalten = geschriebene_layer["bewertung_100m"]
    spalte = spalten[f"{KLASSE_B_CODE}_cost_eur"]
    assert len(spalte) == 3
    assert all(w == VERMERK for w in spalte), spalte
    for verboten in (0, 0.0, "-", None):
        assert verboten not in spalte, (verboten, spalte)


def test_bewertung_100m_euro_spalten_bleiben_float(geschriebene_layer):
    spalten = geschriebene_layer["bewertung_100m"]
    for r in catalog.RISKS:
        if r["code"] == KLASSE_B_CODE:
            continue
        spalte = spalten[f"{r['code']}_cost_eur"]
        assert all(type(w) is float for w in spalte), (r["code"], spalte)
