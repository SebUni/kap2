"""Test des Bestandsaufnahme-Dienstes (Ticket T-0755, Vorhaben T-0447).

Deckt ab: (a) 21 Einträge in Katalogreihenfolge mit allen Feldern,
(b) bevölkerungsgewichteter 65+-Anteil, (c) Katalog-Lücken, (d) fehlende
Arbeitslosenquote → Laufzeitsatz, (e) Kommunen-Einstieg ohne Netzdienst.
Feste Eingaben, kein Netz, keine Datenbank.
"""

from __future__ import annotations

import socket
from types import SimpleNamespace

import pytest

from app.data import bestandsaufnahme as katalog
from app.services import bestandsaufnahme_service as dienst

FELDER = ["code", "gruppe", "label", "einheit", "wert", "quellen", "luecke_satz"]
LUECKEN = ["pflegebeduerftige", "alleinlebende_aeltere", "vorerkrankte",
           "wohnungslose", "kitas_schulen", "schadensereignisse",
           "gewaesser", "wald", "boeden", "schutzgebiete", "lieferketten"]

ZELLEN = [
    {"pop": 100.0, "share_over_65": 20.0, "share_under_18": 10.0,
     "energy_infra_classes": {"substation": 1}, "water_wastewater_classes": {},
     "transport_hub_classes": {"station": 2}, "communication_classes": {}},
    {"pop": 300.0, "share_over_65": 10.0, "share_under_18": 20.0,
     "energy_infra_classes": {"line": 2}, "water_wastewater_classes": {"pump": 1},
     "transport_hub_classes": {}, "communication_classes": {"mast": 3}},
]
SOZIO = {"unemployment_rate_pct": 5.4}


def _nach_code(eintraege):
    return {e["code"]: e for e in eintraege}


def test_a_zweiundzwanzig_eintraege_in_katalogreihenfolge():
    eintraege = dienst.bestandsaufnahme_aus_daten(ZELLEN, SOZIO)
    assert len(eintraege) == 22
    assert [e["code"] for e in eintraege] == [g["code"] for g in katalog.BESTANDSAUFNAHME_GROESSEN]
    for e, g in zip(eintraege, katalog.BESTANDSAUFNAHME_GROESSEN):
        assert list(e.keys()) == FELDER + (["hinweis"] if "hinweis" in g else [])
        assert (e["gruppe"], e["label"], e["einheit"], e["quellen"]) == (
            g["gruppe"], g["label"], g["einheit"], g["quellen"])


def test_b_anteil_ab_65_bevoelkerungsgewichtet():
    e = _nach_code(dienst.bestandsaufnahme_aus_daten(ZELLEN, SOZIO))
    assert e["aeltere_ab_65"]["wert"] == 12.5
    assert e["aeltere_ab_65"]["luecke_satz"] == ""
    assert e["kinder_unter_18"]["wert"] == 17.5
    assert e["energie"]["wert"] == 3
    assert e["wasser_abwasser"]["wert"] == 1
    assert e["verkehrsknoten"]["wert"] == 2
    assert e["kommunikation"]["wert"] == 3
    assert e["arbeitslosenquote"]["wert"] == 5.4


def test_b_keine_zelle_mit_wert_ergibt_none():
    e = _nach_code(dienst.bestandsaufnahme_aus_daten([{"pop": 50.0}], {}))
    assert e["aeltere_ab_65"]["wert"] is None
    assert e["aeltere_ab_65"]["luecke_satz"] == katalog.LAUFZEITSATZ_VORLAGE.format(
        label="Ältere Menschen ab 65 Jahren")
    # Feld fehlt in der Zelle → None, nie 0.
    assert e["energie"]["wert"] is None
    assert e["krankenhaeuser"]["wert"] is None


def test_c_katalog_luecken():
    e = _nach_code(dienst.bestandsaufnahme_aus_daten(ZELLEN, SOZIO))
    kat = {g["code"]: g for g in katalog.BESTANDSAUFNAHME_GROESSEN}
    for code in LUECKEN:
        assert e[code]["wert"] is None
        assert e[code]["luecke_satz"] == kat[code]["luecke"]
        assert e[code]["luecke_satz"] == katalog.LUECKENSATZ_VORLAGE.format(label=kat[code]["label"])


def test_d_fehlende_arbeitslosenquote():
    e = _nach_code(dienst.bestandsaufnahme_aus_daten(ZELLEN, {}))
    assert e["arbeitslosenquote"]["wert"] is None
    assert e["arbeitslosenquote"]["luecke_satz"] == (
        "Für die Größe Arbeitslose (Arbeitslosenquote) war die Datenquelle für diese "
        "Kommune nicht abrufbar; der Wert fehlt in dieser Bestandsaufnahme."
    )


def test_e_kommune_ohne_netzdienst(monkeypatch):
    from app.services import inkar_loader

    def _netz_verboten(*_a, **_k):
        raise AssertionError("Netzdienst aufgerufen")

    monkeypatch.setattr(socket, "create_connection", _netz_verboten)
    monkeypatch.setattr(socket.socket, "connect", _netz_verboten)
    monkeypatch.setattr(inkar_loader, "resolve_ags", _netz_verboten)
    monkeypatch.setattr(inkar_loader, "fetch_socioeconomic", _netz_verboten)
    monkeypatch.setattr(inkar_loader, "socioeconomic_for_kommune", _netz_verboten)

    aufrufe = []

    def _entw(kommune):
        aufrufe.append(("entwicklung", kommune.id))
        return None

    def _zellen(db, kommune_id):
        aufrufe.append(("zellen", kommune_id))
        return ZELLEN

    def _sozio(kommune):
        aufrufe.append(("sozio", kommune.id))
        return SOZIO

    monkeypatch.setattr(dienst, "_zellen_der_kommune", _zellen)
    monkeypatch.setattr(dienst, "_sozialdaten", _sozio)
    monkeypatch.setattr(dienst, "_entwicklung", _entw)

    kommune = SimpleNamespace(id=7, name="Musterstadt", osm_id="R123", bundesland="Sachsen")
    ergebnis = dienst.bestandsaufnahme_fuer_kommune(object(), kommune)

    assert list(ergebnis.keys()) == ["kommune_id", "name", "bundesland", "groessen"]
    assert ergebnis["kommune_id"] == 7
    assert ergebnis["name"] == "Musterstadt"
    assert ergebnis["bundesland"] == "Sachsen"
    assert ergebnis["groessen"] == dienst.bestandsaufnahme_aus_daten(ZELLEN, SOZIO, None)
    assert aufrufe == [("zellen", 7), ("sozio", 7), ("entwicklung", 7)]


ENTWICKLUNG = {"jahr_alt": 2017, "jahr_neu": 2023, "einwohner_alt": 1000,
               "einwohner_neu": 1050, "veraenderung_prozent": 5.0, "quelle": "Q"}


def _ohne_db(monkeypatch, ags):
    from app.data import bevoelkerungsentwicklung
    from app.services import inkar_loader

    monkeypatch.setattr(dienst, "_zellen_der_kommune", lambda db, kid: ZELLEN)
    monkeypatch.setattr(dienst, "_sozialdaten", lambda k: SOZIO)
    monkeypatch.setattr(inkar_loader, "resolve_ags", lambda osm_id: ags)
    gefragt = []

    def _entwicklung(a):
        gefragt.append(a)
        return ENTWICKLUNG

    monkeypatch.setattr(bevoelkerungsentwicklung, "entwicklung", _entwicklung)
    return gefragt


def test_bevoelkerungsentwicklung_wert_und_jahre_per_stub(monkeypatch):
    gefragt = _ohne_db(monkeypatch, "14612000")
    kommune = SimpleNamespace(id=3, name="Dresden", osm_id="R191645")
    e = _nach_code(dienst.bestandsaufnahme_fuer_kommune(object(), kommune)["groessen"])
    g = e["bevoelkerungsentwicklung"]
    assert gefragt == ["14612000"]
    assert g["wert"] == 5.0
    assert g["luecke_satz"] == ""
    assert (g["zusatz"]["jahr_alt"], g["zusatz"]["jahr_neu"]) == (2017, 2023)
    assert (g["zusatz"]["einwohner_alt"], g["zusatz"]["einwohner_neu"]) == (1000, 1050)


def test_bevoelkerungsentwicklung_ohne_gemeinde_ags_ist_laufzeitsatz(monkeypatch):
    gefragt = _ohne_db(monkeypatch, "09")  # Land/Kreis, kein Gemeinde-AGS
    kommune = SimpleNamespace(id=3, name="Bayern", osm_id="R2145268")
    e = _nach_code(dienst.bestandsaufnahme_fuer_kommune(object(), kommune)["groessen"])
    g = e["bevoelkerungsentwicklung"]
    assert gefragt == []
    assert g["wert"] is None and "zusatz" not in g
    assert g["luecke_satz"] == katalog.LAUFZEITSATZ_VORLAGE.format(label="Bevölkerungsentwicklung")


def test_starkregenereignisse_anzahl_und_juengstes_datum_per_stub(monkeypatch):
    from shapely.geometry import box

    from app.data import catrare

    _ohne_db(monkeypatch, "14612000")
    flaeche = box(13.0, 51.0, 14.0, 52.0)
    monkeypatch.setattr(dienst, "_flaeche_der_kommune", lambda db, k: (flaeche, False))
    gefragt = []

    def _ereignisse(f):
        gefragt.append(f)
        return [{"id": "a", "beginn": "2005-07-01T10:00:00"},
                {"id": "b", "beginn": "2021-07-14T03:20:00"},
                {"id": "c", "beginn": "2013-06-02T18:00:00"}]

    monkeypatch.setattr(catrare, "ereignisse_in_flaeche", _ereignisse)
    kommune = SimpleNamespace(id=3, name="Dresden", osm_id="R191645")
    e = _nach_code(dienst.bestandsaufnahme_fuer_kommune(object(), kommune)["groessen"])
    g = e["starkregenereignisse"]
    assert gefragt == [flaeche]
    assert g["wert"] == 3
    assert g["luecke_satz"] == ""
    assert g["zusatz"] == {"juengstes_beginn": "2021-07-14T03:20:00"}
    assert e["schadensereignisse"]["wert"] is None


class _GitterDb:
    """Stub der Datenbank: ``query(...).filter(...).all()`` liefert die Gitterzeilen."""

    def __init__(self, zeilen):
        self._zeilen = zeilen

    def query(self, *_a):
        return self

    def filter(self, *_a):
        return self

    def all(self):
        return self._zeilen


def test_starkregenereignisse_ohne_flaeche_eigener_satz_nie_null(monkeypatch):
    from app.data import catrare

    _ohne_db(monkeypatch, "14612000")
    gefragt = []
    monkeypatch.setattr(catrare, "ereignisse_in_flaeche", lambda f: gefragt.append(f) or [])
    # Weder Kommune.boundary noch eine Gitterzelle.
    kommune = SimpleNamespace(id=3, name="Dresden", osm_id="R191645", boundary=None)
    g = _nach_code(dienst.bestandsaufnahme_fuer_kommune(_GitterDb([]), kommune)["groessen"])["starkregenereignisse"]
    assert gefragt == []
    assert g["wert"] is None and "zusatz" not in g
    assert g["luecke_satz"] == katalog.FLAECHE_FEHLT_SATZ_VORLAGE.format(label=g["label"])
    assert "Fläche der Kommune" in g["luecke_satz"]
    assert "nicht abrufbar" not in g["luecke_satz"]


def test_starkregenereignisse_abruf_gescheitert_bleibt_laufzeitsatz(monkeypatch):
    from shapely.geometry import box

    from app.data import catrare

    _ohne_db(monkeypatch, "14612000")
    monkeypatch.setattr(dienst, "_flaeche_der_kommune", lambda db, k: (box(13.0, 51.0, 14.0, 52.0), False))

    def _kaputt(f):
        raise RuntimeError("Katalog nicht erreichbar")

    monkeypatch.setattr(catrare, "ereignisse_in_flaeche", _kaputt)
    kommune = SimpleNamespace(id=3, name="Dresden", osm_id="R191645")
    g = _nach_code(dienst.bestandsaufnahme_fuer_kommune(object(), kommune)["groessen"])["starkregenereignisse"]
    assert g["wert"] is None
    assert g["luecke_satz"] == katalog.LAUFZEITSATZ_VORLAGE.format(label=g["label"])
    assert "Fläche der Kommune" not in g["luecke_satz"]


def _starkregen_mit_flaeche(monkeypatch, db, kommune):
    from app.data import catrare

    _ohne_db(monkeypatch, "14612000")
    gefragt = []

    def _ereignisse(f):
        gefragt.append(f)
        return [{"id": "a", "beginn": "2021-07-14T03:20:00"}]

    monkeypatch.setattr(catrare, "ereignisse_in_flaeche", _ereignisse)
    g = _nach_code(dienst.bestandsaufnahme_fuer_kommune(db, kommune)["groessen"])["starkregenereignisse"]
    return g, gefragt


def test_starkregenereignisse_huelle_der_gitterzellen_ist_genaehert(monkeypatch):
    from geoalchemy2.shape import from_shape
    from shapely.geometry import box

    zellen = [(from_shape(box(13.0, 51.0, 13.1, 51.1), srid=4326),),
              (from_shape(box(13.5, 51.5, 13.6, 51.6), srid=4326),)]
    kommune = SimpleNamespace(id=3, name="Dresden", osm_id="R191645", boundary=None)
    g, gefragt = _starkregen_mit_flaeche(monkeypatch, _GitterDb(zellen), kommune)
    assert len(gefragt) == 1 and gefragt[0].geom_type == "Polygon"  # konvexe Hülle
    assert g["wert"] == 1 and g["luecke_satz"] == ""
    assert g["zusatz"] == {"juengstes_beginn": "2021-07-14T03:20:00", "flaeche_genaehert": True}


def test_starkregenereignisse_mit_grenze_nicht_genaehert(monkeypatch):
    from geoalchemy2.shape import from_shape
    from shapely.geometry import MultiPolygon, box

    grenze = from_shape(MultiPolygon([box(13.0, 51.0, 14.0, 52.0)]), srid=4326)
    kommune = SimpleNamespace(id=3, name="Dresden", osm_id="R191645", boundary=grenze)
    g, gefragt = _starkregen_mit_flaeche(monkeypatch, object(), kommune)
    assert len(gefragt) == 1
    assert g["wert"] == 1
    assert "flaeche_genaehert" not in g["zusatz"]
    assert g["zusatz"] == {"juengstes_beginn": "2021-07-14T03:20:00"}


def test_sozialdaten_fehler_ergibt_leeres_dict(monkeypatch):
    from app.services import inkar_loader

    def _kaputt(*_a, **_k):
        raise RuntimeError("kein Netz")

    monkeypatch.setattr(inkar_loader, "resolve_ags", _kaputt)
    assert dienst._sozialdaten(SimpleNamespace(id=1, osm_id="R1")) == {}


if __name__ == "__main__":  # pragma: no cover
    pytest.main([__file__, "-q"])
