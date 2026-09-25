"""Tests für app.data.bevoelkerungsentwicklung (T-1164-cto); laufen ohne Datenbank und ohne Netz."""

from app.data import bevoelkerungsentwicklung as b


def test_muenchen_felder_und_werte():
    e = b.entwicklung("09162000")
    assert sorted(e) == [
        "einwohner_alt", "einwohner_neu", "jahr_alt", "jahr_neu", "quelle", "veraenderung_prozent",
    ]
    assert e["jahr_neu"] > e["jahr_alt"] >= 2011
    assert e["einwohner_neu"] > 1_000_000
    assert e["veraenderung_prozent"] == round(
        (e["einwohner_neu"] - e["einwohner_alt"]) / e["einwohner_alt"] * 100, 1
    )
    assert "Destatis" in e["quelle"]


def test_unbekannter_ags_gibt_none():
    assert b.entwicklung("00000000") is None


def test_modellgrenze_nennt_vorausberechnung_und_urbanisierung():
    assert b.MODELLGRENZE.strip()
    assert "Vorausberechnung" in b.MODELLGRENZE
    assert "Urbanisierung" in b.MODELLGRENZE


def test_alle_eintraege_plausibel():
    daten = b._laden()["gemeinden"]
    assert len(daten) > 10000
    for ags, (alt, neu) in daten.items():
        assert len(ags) == 8 and ags.isdigit()
        assert alt > 0 and neu >= 0
