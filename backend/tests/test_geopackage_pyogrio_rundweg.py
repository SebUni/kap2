"""GeoPackage-Rundweg über echtes pyogrio (Verwechslungssperre 2/5, T-0826).

Anders als test_klasse_b_geopackage.py und test_geopackage_nullwerte.py wird
hier weder pyogrio noch ``_write_layer`` ersetzt: ``build_geopackage`` schreibt
mit echten shapely-Polygonen eine .gpkg-Datei in ``tmp_path``, und die Schicht
``bewertung_100m`` wird mit pyogrio zurückgelesen.

Geprüft wird:
(1) ``<Klasse-B-Code>_cost_eur`` enthält in jeder Zeile genau
    ``catalog.NO_EURO_LAYER_TEXT``;
(2) ``<Klasse-B-Code>_outcome`` ist eine numerische Spalte;
(3) für die Zelle ohne Wert ist ``<code>_outcome`` gelesen NULL, nicht 0.0 —
    None, oder NaN, dessen Zeile pyogrio über den Filter ``IS NULL`` als
    NULL-Zeile ausweist (Feature-ID).

Die Zelle ohne Wert steht bewusst an erster Stelle: ``_write_layer`` bestimmt
den Spaltentyp an ``col[0]``; ist der None, läuft die Spalte über den
Float-Zweig, und numpy macht aus None ein NaN.

Ohne Datenbank: die Session wird gedoppelt (Muster aus test_klasse_b_geopackage.py).
"""

from __future__ import annotations

import math

import numpy as np
import pyogrio
import pyogrio.raw
import pytest
from shapely.geometry import Polygon, box

from app.data import catalog
from app.models.models import CellAssessment, GridCell, Kommune
from app.services import geodata_export_service as gx

from tests.test_klasse_b_geopackage import KLASSE_B_CODE, _FakeDB, _klasse_b_eintrag

LAYER = "bewertung_100m"


@pytest.fixture
def gpkg(monkeypatch, tmp_path):
    monkeypatch.setattr(catalog, "RISKS", list(catalog.RISKS) + [_klasse_b_eintrag()])
    klasse_a = next(r["code"] for r in catalog.RISKS if catalog.risk_has_euro_layer(r))
    daten = {"risks": {
        klasse_a: {"index": 30.0, "outcome": 2, "cost_eur": 5.0},
        KLASSE_B_CODE: {"index": 40.0, "outcome": 1.5, "cost_eur": 0.0},
    }}
    zeilen = [
        # Zelle ohne Wert zuerst: col[0] ist None.
        (CellAssessment(data={}),
         GridCell(gitter_id="G0", x_3035=1.0, y_3035=1.0, geometry=box(13.0, 51.0, 13.001, 51.001))),
        (CellAssessment(data=daten),
         GridCell(gitter_id="G1", x_3035=2.0, y_3035=1.0, geometry=box(13.001, 51.0, 13.002, 51.001))),
        (CellAssessment(data=daten),
         GridCell(gitter_id="G2", x_3035=3.0, y_3035=1.0, geometry=box(13.002, 51.0, 13.003, 51.001))),
    ]
    grenze = Polygon([(12.99, 50.99), (13.01, 50.99), (13.01, 51.01), (12.99, 51.01)])
    kommune = Kommune(id=1, name="K", bundesland="SN", area_km2=2.0, population=500, boundary=grenze)
    db = _FakeDB({Kommune: [kommune], CellAssessment: zeilen})
    pfad = tmp_path / "rundweg.gpkg"
    monkeypatch.setattr(gx, "assessment_is_done", lambda db, kid: True)
    monkeypatch.setattr(gx, "_build_output_path", lambda kid, eid: str(pfad))
    # Geometrien sind bereits shapely-Objekte; to_shape reicht sie durch.
    monkeypatch.setattr(gx, "to_shape", lambda g: g)
    ergebnis = gx.build_geopackage(db, 1, 1)
    assert ergebnis == str(pfad)
    assert pfad.is_file()
    return str(pfad), klasse_a


def _lesen(pfad: str, **kw):
    meta, fids, geom, werte = pyogrio.raw.read(pfad, layer=LAYER, return_fids=True, **kw)
    spalten = dict(zip(meta["fields"], werte))
    return meta, fids, geom, spalten


def test_rundweg_schicht_hat_drei_zeilen_mit_geometrie(gpkg):
    pfad, _ = gpkg
    assert LAYER in [name for name, _typ in pyogrio.list_layers(pfad)]
    _meta, fids, geom, spalten = _lesen(pfad)
    assert len(fids) == 3
    assert all(g is not None for g in geom)
    assert list(spalten["gitter_id"]) == ["G0", "G1", "G2"]


def test_klasse_b_cost_eur_ist_in_jeder_zeile_der_vermerk(gpkg):
    pfad, _ = gpkg
    _meta, _fids, _geom, spalten = _lesen(pfad)
    spalte = spalten[f"{KLASSE_B_CODE}_cost_eur"]
    assert len(spalte) == 3
    assert all(isinstance(w, str) for w in spalte), list(spalte)
    assert all(w == catalog.NO_EURO_LAYER_TEXT for w in spalte), list(spalte)


def test_klasse_b_outcome_ist_numerisch(gpkg):
    pfad, _ = gpkg
    info = pyogrio.read_info(pfad, layer=LAYER)
    typen = dict(zip(info["fields"], info["dtypes"]))
    feld = f"{KLASSE_B_CODE}_outcome"
    assert np.issubdtype(np.dtype(typen[feld]), np.number), typen[feld]
    _meta, _fids, _geom, spalten = _lesen(pfad)
    assert np.issubdtype(spalten[feld].dtype, np.number), spalten[feld].dtype
    assert float(spalten[feld][1]) == 1.5
    assert float(spalten[feld][2]) == 1.5


def _ist_null(pfad: str, feld: str, fid, wert) -> bool:
    """NULL = None, oder NaN mit NULL-Kennung der Zeile aus pyogrio (Filter ``IS NULL``)."""
    if wert is None:
        return True
    if isinstance(wert, float) and math.isnan(wert):
        _m, null_fids, _g, _s = _lesen(pfad, where=f'"{feld}" IS NULL')
        return int(fid) in {int(f) for f in null_fids}
    return False


def test_zelle_ohne_wert_outcome_ist_null_nicht_null_komma_null(gpkg):
    pfad, klasse_a = gpkg
    _meta, fids, _geom, spalten = _lesen(pfad)
    for code in (KLASSE_B_CODE, klasse_a):
        feld = f"{code}_outcome"
        wert = spalten[feld][0]
        wert = None if wert is None else float(wert)
        assert wert != 0.0, (feld, wert)
        assert _ist_null(pfad, feld, fids[0], wert), (feld, wert)
        # Gegenprobe: Zellen mit Wert sind keine NULL-Zeilen.
        _m, null_fids, _g, _s = _lesen(pfad, where=f'"{feld}" IS NULL')
        assert [int(f) for f in null_fids] == [int(fids[0])], (feld, list(null_fids))
