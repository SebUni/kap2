"""Einheitliche Download-Namen (T-1424), ohne Datenbankserver.

Regel: ``<art>_<Name der Kommune, dateinamensicher>_<Gemeindeschlüssel>.<endung>``.
Die Routenfunktionen werden direkt mit einer Ersatz-Session aufgerufen (Muster
``test_ergebnis_interpretation_api.py``); den Gemeindeschlüssel liefert seit
T-1469 die VG250-Abfrage ``download_namen._ags_aus_gemeinden`` (ersetzt in den
Tests), nicht mehr ``inkar_loader.resolve_ags`` (Overpass).
"""

from __future__ import annotations

from pathlib import Path

import pytest
from fastapi import HTTPException

from app.api.routes import ergebnis_interpretation as interpretation_route
from app.api.routes import export as export_route
from app.api.routes import parameters as parameter_route
from app.models.models import ExportStatus, GeoExportJob, Kommune
from app.services import download_namen, inkar_loader
from app.services.download_namen import dateinamensicher, download_dateiname

REPO = Path(__file__).resolve().parents[2]
TAB = REPO / "frontend" / "src" / "components" / "interpretation" / "ErgebnisseInterpretierenTab.tsx"


# ── (a) Namensregel ────────────────────────────────────────────────────────────

def test_regel_mit_gemeindeschluessel():
    assert download_dateiname("massnahmen", "Bad Tölz", "09173112", "xlsx") == "massnahmen_Bad-Toelz_09173112.xlsx"


def test_regel_ohne_gemeindeschluessel():
    assert download_dateiname("massnahmen", "Bad Tölz", None, "xlsx") == "massnahmen_Bad-Toelz.xlsx"
    assert download_dateiname("massnahmen", "Bad Tölz", "", "xlsx") == "massnahmen_Bad-Toelz.xlsx"


@pytest.mark.parametrize("name, erwartet", [
    ("Straßkirchen", "Strasskirchen"),
    ("Übersee", "Uebersee"),
    ("Frankfurt (Oder)", "Frankfurt-Oder"),
    ("Halle (Saale)/Süd", "Halle-Saale-Sued"),
    ("Sankt Wendel ", "Sankt-Wendel"),
    ("Rödermark, Stadt", "Roedermark-Stadt"),
    ("Montréal", "Montreal"),
])
def test_dateinamensicher(name, erwartet):
    assert dateinamensicher(name) == erwartet


def test_leerer_name_faellt_auf_kommune_zurueck():
    assert download_dateiname("parameter", None, "09173112", "xlsx") == "parameter_Kommune_09173112.xlsx"


# ── (b) Routen setzen Content-Disposition nach der Regel ─────────────────────

class _Kommune:
    id = 7
    name = "Bad Tölz"
    osm_id = "R12345"


class _Abfrage:
    def __init__(self, ergebnis):
        self._ergebnis = ergebnis

    def filter(self, *_args, **_kwargs):
        return self

    def first(self):
        return self._ergebnis


class _Session:
    def __init__(self, **je_modell):
        self._je_modell = je_modell

    def query(self, modell):
        return _Abfrage(self._je_modell.get(modell.__name__))

    def rollback(self):
        pass


@pytest.fixture
def ags(monkeypatch):
    download_namen._AGS_CACHE.clear()
    monkeypatch.setattr(download_namen, "_ags_aus_gemeinden",
                         lambda db, kommune: "09173112" if getattr(kommune, "id", None) == 7 else None)
    yield
    download_namen._AGS_CACHE.clear()


def _header(antwort) -> str:
    return antwort.headers["content-disposition"]


def test_route_massnahmen_excel(ags, monkeypatch):
    monkeypatch.setattr(export_route, "export_measures_xlsx", lambda db, kid: b"xlsx")
    antwort = export_route.export_measures(7, db=_Session(Kommune=_Kommune()))
    assert "massnahmen_Bad-Toelz_09173112.xlsx" in _header(antwort)
    assert _header(antwort).startswith("attachment")


def test_route_parameter_excel(ags, monkeypatch):
    monkeypatch.setattr(parameter_route, "export_parameters_xlsx", lambda db, kid, name: b"xlsx")
    antwort = parameter_route.export_parameters(7, db=_Session(Kommune=_Kommune()))
    assert "parameter_Bad-Toelz_09173112.xlsx" in _header(antwort)


def test_route_geopackage(ags, tmp_path):
    datei = tmp_path / "export_17.gpkg"
    datei.write_bytes(b"gpkg")

    class _Job:
        id = 17
        kommune_id = 7
        status = ExportStatus.DONE
        file_path = str(datei)

    assert GeoExportJob.__name__ == "GeoExportJob" and Kommune.__name__ == "Kommune"
    antwort = export_route.download_export(7, 17, db=_Session(GeoExportJob=_Job(), Kommune=_Kommune()))
    assert "geodaten_Bad-Toelz_09173112.gpkg" in _header(antwort)


def test_route_interpretationsbericht(ags, monkeypatch):
    monkeypatch.setattr(interpretation_route, "interpretationsbericht_fuer_kommune", lambda db, k: "# Bericht\n")
    antwort = interpretation_route.get_interpretationsbericht(7, db=_Session(Kommune=_Kommune()))
    assert "ergebnisse-interpretieren_Bad-Toelz_09173112.md" in _header(antwort)
    assert antwort.body == "# Bericht\n".encode()


def test_route_ohne_gemeindeschluessel(monkeypatch):
    download_namen._AGS_CACHE.clear()
    monkeypatch.setattr(download_namen, "_ags_aus_gemeinden", lambda db, kommune: None)
    monkeypatch.setattr(export_route, "export_measures_xlsx", lambda db, kid: b"xlsx")
    antwort = export_route.export_measures(7, db=_Session(Kommune=_Kommune()))
    assert 'filename="massnahmen_Bad-Toelz.xlsx"' in _header(antwort)


def test_route_massnahmen_ohne_kommune_404(monkeypatch):
    """Wie export_parameters (T-1471): 404 vor export_measures_xlsx, nicht danach."""
    aufrufe = {"n": 0}

    def _nicht_erwartet(_db, _kid):
        aufrufe["n"] += 1
        return b"xlsx"

    monkeypatch.setattr(export_route, "export_measures_xlsx", _nicht_erwartet)
    with pytest.raises(HTTPException) as exc:
        export_route.export_measures(99, db=_Session(Kommune=None))
    assert exc.value.status_code == 404
    assert aufrufe["n"] == 0


def test_gemeindeschluessel_fehlschlag_bricht_download_nicht_ab(monkeypatch):
    download_namen._AGS_CACHE.clear()

    def _kaputt(_db, _kommune):
        raise RuntimeError("keine Datenbankverbindung (z. B. ohne PostGIS)")

    monkeypatch.setattr(download_namen, "_ags_aus_gemeinden", _kaputt)
    ergebnis = download_namen.download_dateiname_fuer("parameter", _Session(), _Kommune(), "xlsx")
    assert ergebnis == "parameter_Bad-Toelz.xlsx"


def test_route_massnahmen_ohne_overpass(monkeypatch):
    """Der Gemeindeschlüssel kommt aus der VG250-Tabelle; resolve_ags (Overpass) wird
    dabei nicht mehr angerufen (T-1469)."""
    download_namen._AGS_CACHE.clear()
    aufrufe = {"n": 0}

    def _attrappe(_osm_id):
        aufrufe["n"] += 1
        raise RuntimeError("Overpass darf hier nicht mehr gerufen werden")

    monkeypatch.setattr(inkar_loader, "resolve_ags", _attrappe)
    monkeypatch.setattr(download_namen, "_ags_aus_gemeinden",
                         lambda db, kommune: "09173112" if getattr(kommune, "id", None) == 7 else None)
    monkeypatch.setattr(export_route, "export_measures_xlsx", lambda db, kid: b"xlsx")

    antwort = export_route.export_measures(7, db=_Session(Kommune=_Kommune()))

    assert "massnahmen_Bad-Toelz_09173112.xlsx" in _header(antwort)
    assert aufrufe["n"] == 0


# ── (c) Frontend bildet den Namen nicht mehr aus der Kennung ──────────────────

def test_frontend_nutzt_keine_kennung_im_namen():
    quelltext = TAB.read_text(encoding="utf-8")
    assert "ergebnisse-interpretieren-${kommuneId" not in quelltext
