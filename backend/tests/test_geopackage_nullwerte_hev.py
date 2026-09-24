"""Fehlende Gefährdungs-/Expositions-/Vulnerabilitäts- und Kommunenwerte sind NULL, nie 0.0 (T-0850).

Echter pyogrio-Weg (Muster test_geopackage_pyogrio_rundweg.py), ohne Datenbank.
"""

from __future__ import annotations

import math

import pyogrio
import pyogrio.raw
import pytest
from shapely.geometry import Polygon, box

from app.data import catalog
from app.models.models import CellAssessment, GridCell, Kommune
from app.services import geodata_export_service as gx

from tests.test_klasse_b_geopackage import _FakeDB

HZ = catalog.HAZARDS[0]["code"]
EX = catalog.EXPOSURES[0]["code"]
VU = catalog.VULNERABILITIES[0]["code"]
AUX = catalog.AUXILIARY[0]["code"]


def _null(werte, i):
    w = werte[i]
    return w is None or (isinstance(w, float) and math.isnan(w))


@pytest.fixture
def gpkg(monkeypatch, tmp_path):
    # Zelle G0 (zuerst, col[0] ist None): alle Codes fehlen. Zelle G1: 0.0 gesetzt.
    voll = {"hazards": {HZ: 0.0}, "exposures": {EX: 0.0}, "vulnerabilities": {VU: 0.0},
            "auxiliary": {AUX: 0.0}}
    zeilen = [
        (CellAssessment(data={"hazards": {}, "exposures": {}, "vulnerabilities": {}, "auxiliary": {}}),
         GridCell(gitter_id="G0", x_3035=1.0, y_3035=1.0, geometry=box(13.0, 51.0, 13.001, 51.001))),
        (CellAssessment(data=voll),
         GridCell(gitter_id="G1", x_3035=2.0, y_3035=1.0, geometry=box(13.001, 51.0, 13.002, 51.001))),
    ]
    grenze = Polygon([(12.99, 50.99), (13.01, 50.99), (13.01, 51.01), (12.99, 51.01)])
    kommune = Kommune(id=1, name="K", bundesland="SN", area_km2=None, population=None, boundary=grenze)
    db = _FakeDB({Kommune: [kommune], CellAssessment: zeilen})
    pfad = tmp_path / "hev.gpkg"
    monkeypatch.setattr(gx, "assessment_is_done", lambda db, kid: True)
    monkeypatch.setattr(gx, "_build_output_path", lambda kid, eid: str(pfad))
    monkeypatch.setattr(gx, "to_shape", lambda g: g)
    gx.build_geopackage(db, 1, 1)
    return str(pfad)


def _spalten(pfad, layer):
    meta, _f, _g, werte = pyogrio.raw.read(pfad, layer=layer, return_fids=True)
    return dict(zip(meta["fields"], werte))


@pytest.mark.parametrize("code", [HZ, EX, VU])
def test_fehlender_hev_wert_ist_null_gesetzter_null_wert_bleibt(gpkg, code):
    sp = _spalten(gpkg, "bewertung_100m")[code]
    assert _null(sp, 0), sp
    assert not _null(sp, 1) and float(sp[1]) == 0.0, sp


def test_kommune_ohne_flaeche_und_einwohner_ist_null(gpkg):
    sp = _spalten(gpkg, "kommune")
    assert _null(sp["area_km2"], 0), sp["area_km2"]
    assert _null(sp["population"], 0), sp["population"]


def test_sonstige_spalte_fehlender_wert_ist_null(gpkg):
    sp = _spalten(gpkg, "sonstige_100m")[AUX]
    assert _null(sp, 0), sp
    assert float(sp[1]) == 0.0
