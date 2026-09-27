"""Gemeindeschlüssel in Bestandsaufnahme und Finanzdaten ohne Overpass (T-1492).

Bestandsaufnahme (``_sozialdaten``, ``_entwicklung``) und Finanzdaten
(``finance_loader._gdp_for_osm`` über ``finance_for_kommune``) holen den
achtstelligen Gemeindeschlüssel über dieselbe VG250-Abfrage wie die
Download-Namen (``download_namen.gemeindeschluessel``, T-1469). Die Tabelle
``gemeinden`` wird wie in ``test_download_namen.py`` über
``download_namen._ags_aus_gemeinden`` ersetzt; ``inkar_loader.resolve_ags``
(Overpass) ist eine Attrappe, die bei jedem Aufruf ``RuntimeError`` wirft und
ihre Aufrufe zählt. Kein Netz, keine Datenbank.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from app.data import bevoelkerungsentwicklung
from app.services import bestandsaufnahme_service as dienst
from app.services import download_namen, finance_bulk, finance_loader, inkar_loader

AGS_BAD_TOELZ = "09173112"
BAD_TOELZ = SimpleNamespace(id=7, name="Bad Tölz", osm_id="relation/936094", bundesland="Bayern")


class _Session:
    """Ersatz-Session; die VG250-Abfrage selbst ist ersetzt."""

    def rollback(self):
        pass


@pytest.fixture
def overpass(monkeypatch):
    """Attrappe für ``resolve_ags``: wirft bei jedem Aufruf und zählt mit."""
    aufrufe = {"n": 0}

    def _attrappe(*_a, **_k):
        aufrufe["n"] += 1
        raise RuntimeError("Overpass darf hier nicht mehr gerufen werden")

    monkeypatch.setattr(inkar_loader, "resolve_ags", _attrappe)
    download_namen._AGS_CACHE.clear()
    finance_loader._mem_cache.clear()
    yield aufrufe
    download_namen._AGS_CACHE.clear()
    finance_loader._mem_cache.clear()


def _gemeinden(monkeypatch, treffer: bool):
    monkeypatch.setattr(download_namen, "_ags_aus_gemeinden",
                        lambda db, kommune: AGS_BAD_TOELZ if treffer and kommune.id == 7 else None)


@pytest.fixture
def mitschnitt(monkeypatch):
    """Zeichnet auf, mit welchem Schlüssel die nachgelagerten Quellen gefragt werden."""
    gefragt: dict[str, list] = {"sozio": [], "entwicklung": [], "bip": [], "budget": []}

    def _sozio(ags):
        gefragt["sozio"].append(ags)
        return {"unemployment_rate_pct": 3.1}

    def _entw(ags):
        gefragt["entwicklung"].append(ags)
        return {"veraenderung_prozent": 2.0}

    def _bip(ags):
        gefragt["bip"].append(ags)
        return {"gdp": {"gdp_meur": 1.0, "gdp_year": 2022, "level": "kreis"}}

    def _budget(ags, name):
        gefragt["budget"].append(ags)
        return None

    monkeypatch.setattr(inkar_loader, "fetch_socioeconomic", _sozio)
    monkeypatch.setattr(bevoelkerungsentwicklung, "entwicklung", _entw)
    monkeypatch.setattr(finance_loader, "fetch_finance", _bip)
    monkeypatch.setattr(finance_bulk, "budget_for_kommune", _budget)
    monkeypatch.setattr(inkar_loader, "_auth_headers", lambda: {"username": "x", "password": "y"})
    monkeypatch.setattr(finance_loader, "_read_cache", lambda _d: None)
    monkeypatch.setattr(finance_loader, "_write_cache", lambda *a: None)
    return gefragt


def test_bestandsaufnahme_und_finanzen_nutzen_vg250_schluessel(overpass, mitschnitt, monkeypatch):
    _gemeinden(monkeypatch, treffer=True)
    db = _Session()

    assert dienst._sozialdaten(db, BAD_TOELZ) == {"unemployment_rate_pct": 3.1}
    assert dienst._entwicklung(db, BAD_TOELZ) == {"veraenderung_prozent": 2.0}
    payload = finance_loader.finance_for_kommune(BAD_TOELZ.osm_id, BAD_TOELZ.name, db=db, kommune=BAD_TOELZ)

    assert payload == {"gdp": {"gdp_meur": 1.0, "gdp_year": 2022, "level": "kreis"}}
    assert mitschnitt == {"sozio": [AGS_BAD_TOELZ], "entwicklung": [AGS_BAD_TOELZ],
                          "bip": [AGS_BAD_TOELZ], "budget": [AGS_BAD_TOELZ]}
    assert overpass["n"] == 0


def test_gdp_for_osm_liefert_vg250_schluessel(overpass, mitschnitt, monkeypatch):
    _gemeinden(monkeypatch, treffer=True)
    _payload, ags = finance_loader._gdp_for_osm("936094", BAD_TOELZ.osm_id, db=_Session(), kommune=BAD_TOELZ)
    assert ags == AGS_BAD_TOELZ
    assert overpass["n"] == 0


def test_schluessel_aus_platten_zwischenspeicher_hat_vorrang(overpass, mitschnitt, monkeypatch):
    """Ein veralteter Eintrag auf der Platte reicht seinen AGS weiter; die VG250-Abfrage entfällt."""
    gefragt_gemeinden = []

    def _gemeinden_zaehlend(db, kommune):
        gefragt_gemeinden.append(kommune.id)
        return AGS_BAD_TOELZ

    monkeypatch.setattr(download_namen, "_ags_aus_gemeinden", _gemeinden_zaehlend)
    monkeypatch.setattr(finance_loader, "_read_cache", lambda _d: {"stale": True, "ags": "09999999"})

    _payload, ags = finance_loader._gdp_for_osm("936094", BAD_TOELZ.osm_id, db=_Session(), kommune=BAD_TOELZ)

    assert ags == "09999999"
    assert gefragt_gemeinden == []
    assert overpass["n"] == 0


def test_ohne_treffer_in_gemeinden_wie_ohne_schluessel(overpass, mitschnitt, monkeypatch):
    _gemeinden(monkeypatch, treffer=False)
    db = _Session()

    assert dienst._sozialdaten(db, BAD_TOELZ) == {}
    assert dienst._entwicklung(db, BAD_TOELZ) is None
    assert finance_loader._gdp_for_osm("936094", BAD_TOELZ.osm_id, db=db, kommune=BAD_TOELZ) == (None, None)
    assert finance_loader.finance_for_kommune(BAD_TOELZ.osm_id, BAD_TOELZ.name, db=db, kommune=BAD_TOELZ) is None

    assert mitschnitt["sozio"] == [] and mitschnitt["entwicklung"] == [] and mitschnitt["bip"] == []
    assert mitschnitt["budget"] == [None]
    assert overpass["n"] == 0


def test_bestandsaufnahme_ohne_treffer_bricht_nicht_ab(overpass, mitschnitt, monkeypatch):
    _gemeinden(monkeypatch, treffer=False)
    monkeypatch.setattr(dienst, "_zellen_der_kommune", lambda db, kid: [])
    monkeypatch.setattr(dienst, "_starkregen", lambda db, k: {"starkregen": None,
                                                              "starkregen_ohne_flaeche": True,
                                                              "flaeche_genaehert": False})
    ergebnis = dienst.bestandsaufnahme_fuer_kommune(_Session(), BAD_TOELZ)
    assert ergebnis["groessen"] == dienst.bestandsaufnahme_aus_daten(
        [], {}, None, starkregen=None, starkregen_ohne_flaeche=True, flaeche_genaehert=False)
    assert overpass["n"] == 0


def test_abfragefehler_bricht_nicht_ab(overpass, mitschnitt, monkeypatch):
    def _kaputt(_db, _kommune):
        raise RuntimeError("keine Datenbankverbindung (z. B. ohne PostGIS)")

    monkeypatch.setattr(download_namen, "_ags_aus_gemeinden", _kaputt)
    db = _Session()
    assert dienst._sozialdaten(db, BAD_TOELZ) == {}
    assert dienst._entwicklung(db, BAD_TOELZ) is None
    assert finance_loader._gdp_for_osm("936094", BAD_TOELZ.osm_id, db=db, kommune=BAD_TOELZ) == (None, None)
    assert overpass["n"] == 0


if __name__ == "__main__":  # pragma: no cover
    pytest.main([__file__, "-q"])
