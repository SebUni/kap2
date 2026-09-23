"""GeoPackage-Export: fehlende Werte in ``<code>_outcome`` und ``<code>_index`` sind None (NULL), nie 0.0.

Ohne Datenbank; ``_write_layer`` wird abgefangen (Muster aus test_klasse_b_geopackage.py).
Ob pyogrio None als NULL schreibt, ist nicht Gegenstand dieser Datei.
"""

from __future__ import annotations

import types

import pytest

from app.data import catalog
from app.models.models import CellAssessment, GridCell, Kommune
from app.services import geodata_export_service as gx

from tests.test_klasse_b_geopackage import KLASSE_B_CODE, _FakeDB, _klasse_b_eintrag


@pytest.fixture
def layer(monkeypatch, tmp_path):
    monkeypatch.setattr(catalog, "RISKS", list(catalog.RISKS) + [_klasse_b_eintrag()])
    klasse_a = next(r["code"] for r in catalog.RISKS if catalog.risk_has_euro_layer(r))
    daten = {"risks": {
        klasse_a: {"index": 30.0, "outcome": 2, "cost_eur": 5.0},
        KLASSE_B_CODE: {"index": 40.0, "outcome": 1.0, "cost_eur": 0.0},
    }}
    zeilen = [
        (CellAssessment(data=daten), GridCell(gitter_id="G1", x_3035=1.0, y_3035=2.0, geometry=object())),
        (CellAssessment(data=daten), GridCell(gitter_id="G2", x_3035=3.0, y_3035=4.0, geometry=object())),
        (CellAssessment(data={}), GridCell(gitter_id="G3", x_3035=5.0, y_3035=6.0, geometry=object())),
    ]
    kommune = Kommune(id=1, name="K", bundesland="SN", area_km2=2.0, population=500, boundary=object())
    db = _FakeDB({Kommune: [kommune], CellAssessment: zeilen})
    monkeypatch.setattr(gx, "assessment_is_done", lambda db, kid: True)
    monkeypatch.setattr(gx, "_build_output_path", lambda kid, eid: str(tmp_path / "t.gpkg"))
    monkeypatch.setattr(gx, "to_shape", lambda g: types.SimpleNamespace(geom_type="Polygon"))
    aufrufe: dict = {}

    def _abgefangen(path, name, geoms, data, fields, **kw):
        aufrufe[name] = dict(zip(fields, data))

    monkeypatch.setattr(gx, "_write_layer", _abgefangen)
    gx.build_geopackage(db, 1, 1)
    return aufrufe["bewertung_100m"], klasse_a


@pytest.mark.parametrize("welche", ["a", "b"])
def test_fehlender_wert_ist_none(layer, welche):
    spalten, klasse_a = layer
    code = klasse_a if welche == "a" else KLASSE_B_CODE
    for suffix in ("_outcome", "_index"):
        spalte = spalten[f"{code}{suffix}"]
        assert len(spalte) == 3
        assert spalte[2] is None, (code, suffix, spalte)
        assert all(type(w) is float for w in spalte[:2]), (code, suffix, spalte)
    assert not any(isinstance(w, str) for w in spalten[f"{code}_outcome"])
