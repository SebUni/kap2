"""Screening-Index der angrenzenden Gemeinden (T-1133, Vorhaben T-1010, A5).

Prüft die reine Funktion ``nachbar_screening_aus`` mit Ersatzdaten (Muster
``test_klasse_b_lite.py``): ``Gemeinde`` trägt eine PostGIS-Spalte, deshalb keine
Datenbank. Die räumliche Abfrage (``nachbar_screening_fuer_kommune``) braucht
PostGIS und wird hier nicht geprüft.
"""
from __future__ import annotations

from app.data import catalog
from app.models.lite_models import Gemeinde, GemeindeLiteResult
from app.services.nachbarkommunen_screening import nachbar_screening_aus

CODE_MIT_ZEILE = "EXPECTED_ANNUAL_MORTALITY"
CODE_OHNE_ZEILE = "EXPECTED_ANNUAL_ALLERGY_DAYS"
VERBOTEN_BETRAG = ("cost", "eur", "outcome")
VERBOTEN_VERDICHTUNG = ("mittel", "summe", "max", "min")


def _gemeinde(ags: str, name: str) -> Gemeinde:
    return Gemeinde(ags=ags, name=name, bez="Gemeinde", bundesland="Sachsen")


def _zeile(ags: str, code: str, index: float) -> GemeindeLiteResult:
    return GemeindeLiteResult(ags=ags, risk_code=code, index_value=index,
                              outcome_value=7.0, outcome_unit="Fälle/Jahr",
                              cost_eur=987654321.0, drivers={})


def _daten():
    eigene = _gemeinde("14612000", "Dresden")
    nachbarn = [_gemeinde("14625010", "Bautzen-Nachbar"),
                _gemeinde("14627010", "Meißen-Nachbar")]
    ergebnisse = [
        _zeile("14612000", CODE_MIT_ZEILE, 61.5),
        _zeile("14625010", CODE_MIT_ZEILE, 38.25),
        _zeile("14627010", CODE_MIT_ZEILE, 72.0),
        _zeile("14612000", "EXPECTED_ANNUAL_MORBIDITY", 55.0),
        # Zeile einer fremden Gemeinde: darf nicht erscheinen.
        _zeile("09162000", CODE_MIT_ZEILE, 99.0),
    ]
    return eigene, nachbarn, ergebnisse


def _schluessel(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield k
            yield from _schluessel(v)
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            yield from _schluessel(v)


def test_ein_eintrag_je_code_aus_catalog():
    ausgabe = nachbar_screening_aus(*_daten())
    assert [e["code"] for e in ausgabe] == [r["code"] for r in catalog.RISKS]
    for e in ausgabe:
        assert set(e) == {"code", "name", "index_vorhanden", "eigener_index", "nachbarn"}
        for n in e["nachbarn"]:
            assert set(n) == {"ags", "name", "index"}


def test_index_gleich_gespeichertem_index_value():
    eigene, nachbarn, ergebnisse = _daten()
    gespeichert = {(z.risk_code, z.ags): z.index_value for z in ergebnisse}
    ausgabe = nachbar_screening_aus(eigene, nachbarn, ergebnisse)
    geprueft = 0
    for e in ausgabe:
        erwartet_eigen = gespeichert.get((e["code"], eigene.ags))
        assert e["eigener_index"] == erwartet_eigen
        assert {n["ags"] for n in e["nachbarn"]} == {g.ags for g in nachbarn}
        for n in e["nachbarn"]:
            assert n["index"] == gespeichert.get((e["code"], n["ags"]))
            if n["index"] is not None:
                geprueft += 1
    assert geprueft == 2
    by_code = {e["code"]: e for e in ausgabe}
    assert by_code[CODE_MIT_ZEILE]["eigener_index"] == 61.5
    assert 99.0 not in [n["index"] for n in by_code[CODE_MIT_ZEILE]["nachbarn"]]


def test_code_ohne_lite_zeile_ohne_index():
    ausgabe = {e["code"]: e for e in nachbar_screening_aus(*_daten())}
    assert ausgabe[CODE_MIT_ZEILE]["index_vorhanden"] is True
    ohne = ausgabe[CODE_OHNE_ZEILE]
    assert ohne["index_vorhanden"] is False
    assert ohne["eigener_index"] is None
    assert all(n["index"] is None for n in ohne["nachbarn"])
    assert ausgabe["EXPECTED_ANNUAL_UV_YLL"]["index_vorhanden"] is False


def test_kein_betrag_und_keine_verdichtung():
    ausgabe = nachbar_screening_aus(*_daten())
    schluessel = [k.lower() for k in _schluessel(ausgabe)]
    assert schluessel
    for k in schluessel:
        for wort in VERBOTEN_BETRAG + VERBOTEN_VERDICHTUNG:
            assert wort not in k, f"Schlüssel {k!r} enthält {wort!r}"
    assert "987654321" not in repr(ausgabe)


def test_ohne_eigene_gemeinde():
    ausgabe = nachbar_screening_aus(None, [], [])
    assert len(ausgabe) == len(catalog.RISKS)
    assert all(e["index_vorhanden"] is False and e["eigener_index"] is None
               and e["nachbarn"] == [] for e in ausgabe)
