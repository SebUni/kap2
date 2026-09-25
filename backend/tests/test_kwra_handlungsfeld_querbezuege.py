"""Tests für die Ablesung der Querbezüge zwischen den 13 Handlungsfeldern (T-0934-cto).

Quelle: KWRA 2021, Teilbericht 6, Kap. 3.4, Abbildung 8 (S. 83), Fließtext S. 84–85.
"""
from app.data import kwra_handlungsfeld_querbezuege as h
from app.data import kwra_querverbindungen as k


def test_genau_13_handlungsfelder():
    namen = [e["name"] for e in h.HANDLUNGSFELDER]
    assert len(namen) == 13
    assert len(set(namen)) == 13


def test_meiste_ausgehende_wasserhaushalt():
    assert h.meiste_ausgehende() == "Wasserhaushalt, Wasserwirtschaft"
    # eindeutig: kein anderes Handlungsfeld erreicht denselben Wert
    werte = sorted((e["ausgehend"] for e in h.HANDLUNGSFELDER), reverse=True)
    assert werte[0] > werte[1]


def test_meiste_eingehende_tourismus():
    assert h.meiste_eingehende() == "Tourismuswirtschaft"
    werte = sorted((e["eingehend"] for e in h.HANDLUNGSFELDER), reverse=True)
    assert werte[0] > werte[1]


def test_rangaussagen_stimmen_mit_kennzahlen_ueberein():
    assert h.meiste_ausgehende() == k.KENNZAHLEN["handlungsfeld_meiste_ausgehende_beziehungen"]
    assert h.meiste_eingehende() == k.KENNZAHLEN["handlungsfeld_meiste_eingehende_beziehungen"]


def test_nur_aus_bzw_nur_eingehend_laut_hinweistext():
    felder = {e["name"]: e for e in h.HANDLUNGSFELDER}
    assert felder["Küsten- und Meeresschutz"]["eingehend"] == 0
    assert felder["Küsten- und Meeresschutz"]["ausgehend"] > 0
    assert felder["Tourismuswirtschaft"]["ausgehend"] == 0
    assert felder["Tourismuswirtschaft"]["eingehend"] > 0
    nur_aus = [n for n, e in felder.items() if e["eingehend"] == 0]
    nur_ein = [n for n, e in felder.items() if e["ausgehend"] == 0]
    assert nur_aus == ["Küsten- und Meeresschutz"]
    assert nur_ein == ["Tourismuswirtschaft"]


def test_summen_ausgehend_gleich_eingehend_und_hoechstens_257():
    aus = sum(e["ausgehend"] for e in h.HANDLUNGSFELDER)
    ein = sum(e["eingehend"] for e in h.HANDLUNGSFELDER)
    assert aus == ein
    assert aus <= k.KENNZAHLEN["querverbindungen_gesamt"]
    assert "251" in h.ABLESUNG


def test_anzahlen_nicht_negativ_ganzzahlig():
    for e in h.HANDLUNGSFELDER:
        assert isinstance(e["ausgehend"], int) and e["ausgehend"] >= 0
        assert isinstance(e["eingehend"], int) and e["eingehend"] >= 0


def test_ablesung_ausgewiesen_mit_abbildung_und_seite():
    assert "Abbildung 8" in h.ABLESUNG
    assert "S. 83" in h.ABLESUNG
    assert "Ablesung" in h.ABLESUNG
    assert "Abbildung 8" in h.QUELLE
