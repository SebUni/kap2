"""Schnittstelle der Interpretationsbelege (T-1140), ohne Datenbankserver.

Die Routenfunktionen werden direkt mit einer Ersatz-Session aufgerufen (Muster
``test_klasse_b_lite.py``): ``Kommune`` trägt eine PostGIS-Spalte, und die
Nachbarschaftsabfrage braucht PostGIS; beides ist unter SQLite nicht verfügbar.
"""

from __future__ import annotations

from datetime import date

import pytest
from fastapi import HTTPException

from app.api.routes import ergebnis_interpretation as route
from app.data.diversitaet_aspekte import DIVERSITAET_JE_KLIMAWIRKUNG
from app.data.kra_leitfragen import LEITFRAGEN
from app.data.massnahmen_umsetzung import MASSNAHMEN_UMSETZUNG
from app.services.handlungsfeld_abhaengigkeiten import abhaengigkeiten_der_kommune
from app.services.massnahmen_gewissheit import massnahmen_gewissheit

ERWARTET = {
    ("GET", "/kommune/{kommune_id}/interpretation/nachbarkommunen"),
    ("GET", "/kommune/{kommune_id}/interpretation/nachweise"),
    ("POST", "/kommune/{kommune_id}/interpretation/nachweise"),
    ("DELETE", "/kommune/{kommune_id}/interpretation/nachweise/{nachweis_id}"),
    ("GET", "/kommune/{kommune_id}/interpretation/abhaengigkeiten"),
    ("GET", "/interpretation/massnahmen-gewissheit"),
    ("GET", "/interpretation/massnahmen-umsetzung"),
    ("GET", "/interpretation/diversitaet"),
    ("GET", "/interpretation/leitfragen"),
}


class _Abfrage:
    def __init__(self, ergebnis):
        self._ergebnis = ergebnis

    def filter(self, *_args, **_kwargs):
        return self

    def first(self):
        return self._ergebnis


class _Session:
    """Ersatz-Session: ``query(Kommune)…first()`` liefert die hinterlegte Kommune."""

    def __init__(self, kommune=None):
        self.kommune = kommune

    def query(self, _modell):
        return _Abfrage(self.kommune)


class _Kommune:
    id = 1
    name = "Beispielstadt"


def test_routen_genau_die_liste():
    paare = {
        (methode, r.path)
        for r in route.router.routes
        for methode in r.methods
    }
    assert paare == ERWARTET


def test_main_bindet_router_geschuetzt_ein():
    from app import main

    pfade = {r.path for r in main.app.routes}
    for _methode, pfad in ERWARTET:
        assert "/api" + pfad in pfade


@pytest.mark.parametrize("aufruf", [
    lambda db: route.get_nachbarkommunen(99, db),
    lambda db: route.get_nachweise(99, db),
    lambda db: route.post_nachweis(
        99, route.NachweisEingabe(art="fachabteilung", stelle="Umweltamt", datum=date(2026, 9, 1)), db,
    ),
    lambda db: route.delete_nachweis(99, 1, db),
    lambda db: route.get_abhaengigkeiten(99, db),
])
def test_unbekannte_kommune_404(aufruf):
    with pytest.raises(HTTPException) as fehler:
        aufruf(_Session(kommune=None))
    assert fehler.value.status_code == 404


def test_value_error_des_nachweisdienstes_400():
    eingabe = route.NachweisEingabe(art="unbekannt", stelle="Umweltamt", datum=date(2026, 9, 1))
    with pytest.raises(HTTPException) as fehler:
        route.post_nachweis(1, eingabe, _Session(kommune=_Kommune()))
    assert fehler.value.status_code == 400
    assert "Nachweisart" in fehler.value.detail


def test_value_error_leere_stelle_400():
    eingabe = route.NachweisEingabe(art="fachabteilung", stelle="  ", datum=date(2026, 9, 1))
    with pytest.raises(HTTPException) as fehler:
        route.post_nachweis(1, eingabe, _Session(kommune=_Kommune()))
    assert fehler.value.status_code == 400


def test_nachbarkommunen_reicht_dienst_durch(monkeypatch):
    erwartet = [{"code": "X", "index_vorhanden": False}]
    gesehen = {}

    def _ersatz(db, kommune):
        gesehen["kommune"] = kommune
        return erwartet

    monkeypatch.setattr(route, "nachbar_screening_fuer_kommune", _ersatz)
    kommune = _Kommune()
    assert route.get_nachbarkommunen(1, _Session(kommune=kommune)) is erwartet
    assert gesehen["kommune"] is kommune


def test_nachweise_reicht_dienst_durch(monkeypatch):
    erwartet = [{"art": "fachabteilung", "status": "nicht erfasst"}]
    monkeypatch.setattr(route.ergebnis_nachweise, "nachweise", lambda db, kid: erwartet)
    assert route.get_nachweise(1, _Session(kommune=_Kommune())) is erwartet


def test_datenmodule_und_dienste_unveraendert():
    assert route.get_massnahmen_umsetzung() is MASSNAHMEN_UMSETZUNG
    assert route.get_diversitaet() is DIVERSITAET_JE_KLIMAWIRKUNG
    assert route.get_leitfragen() is LEITFRAGEN
    assert route.get_massnahmen_gewissheit() == massnahmen_gewissheit()
    assert route.get_abhaengigkeiten(1, _Session(kommune=_Kommune())) == abhaengigkeiten_der_kommune()
