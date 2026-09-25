"""Test des Bestandsaufnahme-Dienstes (Ticket T-0755, Vorhaben T-0447).

Deckt ab: (a) 20 Einträge in Katalogreihenfolge mit allen Feldern,
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


def test_a_zwanzig_eintraege_in_katalogreihenfolge():
    eintraege = dienst.bestandsaufnahme_aus_daten(ZELLEN, SOZIO)
    assert len(eintraege) == 20
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

    def _zellen(db, kommune_id):
        aufrufe.append(("zellen", kommune_id))
        return ZELLEN

    def _sozio(kommune):
        aufrufe.append(("sozio", kommune.id))
        return SOZIO

    monkeypatch.setattr(dienst, "_zellen_der_kommune", _zellen)
    monkeypatch.setattr(dienst, "_sozialdaten", _sozio)

    kommune = SimpleNamespace(id=7, name="Musterstadt", osm_id="R123", bundesland="Sachsen")
    ergebnis = dienst.bestandsaufnahme_fuer_kommune(object(), kommune)

    assert list(ergebnis.keys()) == ["kommune_id", "name", "groessen"]
    assert ergebnis["kommune_id"] == 7
    assert ergebnis["name"] == "Musterstadt"
    assert ergebnis["groessen"] == dienst.bestandsaufnahme_aus_daten(ZELLEN, SOZIO)
    assert aufrufe == [("zellen", 7), ("sozio", 7)]


def test_sozialdaten_fehler_ergibt_leeres_dict(monkeypatch):
    from app.services import inkar_loader

    def _kaputt(*_a, **_k):
        raise RuntimeError("kein Netz")

    monkeypatch.setattr(inkar_loader, "resolve_ags", _kaputt)
    assert dienst._sozialdaten(SimpleNamespace(id=1, osm_id="R1")) == {}


if __name__ == "__main__":  # pragma: no cover
    pytest.main([__file__, "-q"])
