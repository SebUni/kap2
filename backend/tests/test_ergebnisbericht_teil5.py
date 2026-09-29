"""Teil 5 des PDF-Ergebnisberichts: Raumergebnis (T-1565).

Abnahme für ``--beispiel warmsen --teile 4,5``: je Zeile aus ``raum.raumzeilen`` eine Tabellenzeile
mit Einwohnern, davon ab 65, Todesfällen und Einweisungen (absolut und je 1.000 Einwohner) und dem
Jahresbetrag (absolut und je 1.000 Einwohner) als ``span.betrag``; die Summenzeile zeigt denselben
Jahresbetrag wie Teil 4; Quelle, Stand und Lizenz der Ortsteilgrenzen stehen im Text; Teil 4 verweist
auf Teil 5. Gegenproben mit künstlichen Zeilen: Zeile ohne bewohnte Zelle zeigt den Grund; ohne
Ortsteilfläche steht genau eine Zeile für die Kommune.
"""

from __future__ import annotations

import datetime as dt
import os
import subprocess
import sys

import pytest

HIER = os.path.dirname(os.path.abspath(__file__))
BACKEND = os.path.dirname(HIER)
sys.path.insert(0, BACKEND)
sys.path.insert(0, HIER)

from test_ergebnisbericht_regeln import REGELN, Element, baum, html_text  # noqa: E402

AUS_PDF = "/tmp/kap2-ergebnisbericht/teil5.pdf"
AUS_HTML = "/tmp/kap2-ergebnisbericht/teil5.html"


def _teil(wurzel: Element, nr: int) -> Element:
    treffer = [t for t in wurzel.alle() if t.tag == "section" and "teil" in t.klassen
               and any(e.tag == "h1" and e.attrs.get("id") == f"teil-{nr}" for e in t.alle())]
    assert len(treffer) == 1
    return treffer[0]


@pytest.fixture(scope="module")
def bericht() -> Element:
    for pfad in (AUS_PDF, AUS_HTML):
        if os.path.exists(pfad):
            os.remove(pfad)
    lauf = subprocess.run(
        [sys.executable, "-m", "app.cli", "ergebnisbericht", "--beispiel", "warmsen",
         "--teile", "4,5", "--aus", AUS_PDF],
        cwd=BACKEND, capture_output=True, text=True, timeout=600)
    assert lauf.returncode == 0, lauf.stdout[-2000:] + lauf.stderr[-4000:]
    with open(AUS_HTML, encoding="utf-8") as fh:
        return baum(fh.read())


@pytest.fixture(scope="module")
def teil5(bericht) -> Element:
    return _teil(bericht, 5)


@pytest.fixture(scope="module")
def teil4(bericht) -> Element:
    return _teil(bericht, 4)


def _zeilen(teil: Element) -> list[Element]:
    return [e for e in teil.alle() if e.tag == "tr" and "raumzeile" in e.klassen]


def _zellen(tr: Element) -> list[Element]:
    return [e for e in tr.alle() if e.tag == "td"]


def test_eine_zeile_je_raumzeile_mit_allen_feldern(teil5):
    from app.services.ergebnisbericht.beispiel import beispiel
    from app.services.ergebnisbericht.raum import raumzeilen
    from app.services.ergebnisbericht.teile import de_zahl

    soll = raumzeilen(beispiel("warmsen"))
    zeilen = _zeilen(teil5)
    assert len(zeilen) == len(soll) > 1
    for z, tr in zip(soll, zeilen):
        c = _zellen(tr)
        assert c[1].text() == de_zahl(z.einwohner)
        assert c[2].text() == de_zahl(z.einwohner_ab65)
        if z.grund:
            assert c[3].mit_klasse("grund")
            continue
        assert len(c) == 10
        assert c[4].text() == de_zahl(z.todesfaelle, 2)
        assert c[5].text() == de_zahl(z.todesfaelle_je_1000, 2)
        assert c[6].text() == de_zahl(z.einweisungen, 2)
        assert c[7].text() == de_zahl(z.einweisungen_je_1000, 2)
        assert len(c[8].mit_klasse("betrag")) == 1 and len(c[9].mit_klasse("betrag")) == 1


def test_summenzeile_zeigt_jahresbetrag_wie_teil4(teil4, teil5):
    summe4 = teil4.mit_klasse("summe")[0].mit_klasse("betrag")[0].text()
    summen = teil5.mit_klasse("summe")
    assert len(summen) == 1 and summen[0].mit_klasse("nenner")
    assert _zellen(summen[0])[8].mit_klasse("betrag")[0].text() == summe4


def test_text_nennt_quelle_stand_und_lizenz(teil5):
    text = teil5.text()
    assert "OpenStreetMap" in text and "© OpenStreetMap-Mitwirkende" in text
    assert "27.09.2026" in text
    assert "übriges Gemeindegebiet" in text


def test_teil4_verweist_auf_teil5(teil4):
    assert "enthält diese Fassung nicht" not in teil4.text()
    assert "Teil 5" in teil4.text()


def test_datenstandszeile_ortsteilgrenzen():
    from app.services.ergebnisbericht.sammler import DATENSTAENDE
    zeile = dict(DATENSTAENDE)["Ortsteilgrenzen"]
    assert "ODbL" in zeile and "27.09.2026" in zeile and "11:19" in zeile


def _daten(raum):
    from types import SimpleNamespace
    from app.services.ergebnisbericht.beispiel import beispiel
    from app.services.ergebnisbericht.sammler import Stand
    return SimpleNamespace(
        kommune=beispiel("warmsen"), raum=raum,
        beziffert_text="1 von 102 Klimawirkungen in Euro beziffert",
        stand=Stand("Fassung 0.1", "#95", "M", "Zensus 2022", dt.date(2026, 9, 27)))


def _zeile(name, art, ew=1000.0, grund=None):
    from app.services.ergebnisbericht.raum import Raumzeile
    if grund:
        return Raumzeile(name=name, art=art, ebene=10, zellkennungen=(), einwohner=0.0,
                         einwohner_ab65=0.0, hitzetage=None, todesfaelle=None, yll=None,
                         einweisungen=None, jahresbetrag_eur=None, grund=grund)
    return Raumzeile(name=name, art=art, ebene=None, zellkennungen=("x",), einwohner=ew,
                     einwohner_ab65=ew * 0.2, hitzetage=11.0, todesfaelle=0.5, yll=5.0,
                     einweisungen=1.5, jahresbetrag_eur=ew * 100.0,
                     jahresbetrag_je_1000_eur=100000.0, todesfaelle_je_1000=0.5 / ew * 1000,
                     einweisungen_je_1000=1.5 / ew * 1000)


def _baum(teil_html):
    return baum(f'<html><body><section class="teil">{teil_html}</section></body></html>')


def test_gegenprobe_zeile_ohne_zelle_zeigt_grund():
    from app.services.ergebnisbericht.raum import GRUND_OHNE_ZELLE
    from app.services.ergebnisbericht.teile import teil_5
    d = _daten([_zeile("Nord", "ortsteil"), _zeile("Leer", "ortsteil", grund=GRUND_OHNE_ZELLE),
                _zeile("Warmsen", "gemeinde")])
    w = _baum(teil_5(d))
    zeilen = _zeilen(w)
    assert [_zellen(z)[0].text() for z in zeilen] == ["Nord", "Leer", "übriges Gemeindegebiet"]
    leer = zeilen[1]
    assert GRUND_OHNE_ZELLE in leer.text() and not leer.mit_klasse("betrag")
    assert REGELN[1](w, [html_text(w)]) == []


def test_gegenprobe_ohne_ortsteilflaeche_eine_zeile_fuer_die_kommune():
    from app.services.ergebnisbericht.teile import teil_5
    w = _baum(teil_5(_daten([_zeile("Warmsen", "gemeinde")])))
    zeilen = _zeilen(w)
    assert [_zellen(z)[0].text() for z in zeilen] == ["Warmsen"]
    assert "keine Ortsteilgrenzen" in w.text()


def test_keine_verbotenen_woerter(teil5):
    text = teil5.text()
    for wort in ("Zwischentabelle", "Sensitivitätslauf", ".py"):
        assert wort not in text


@pytest.mark.parametrize("nr", sorted(REGELN))
def test_harte_regeln_an_teil_5(teil5, nr):
    wurzel = Element("#wurzel", {}, [teil5])
    assert REGELN[nr](wurzel, [html_text(wurzel)]) == []
