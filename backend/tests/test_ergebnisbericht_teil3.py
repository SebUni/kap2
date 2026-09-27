"""Teil 3 des PDF-Ergebnisberichts: Klimatische Ausgangslage (T-1417).

Abnahme für ``--beispiel warmsen``:

(a) je in Euro bezifferter Klimawirkung genau eine Tabellenzeile mit Beobachtungswert (DWD-CDC) und
    Projektionswerten für RCP 4.5 und RCP 8.5;
(b) jede Zahl in Teil 3 trägt Quelle und Datenstand (Attribute ``data-quelle`` und
    ``data-datenstand``, sichtbar als Fußnote);
(c) kein Tabellenfeld ist leer; fehlt ein Wert, steht der Grund (Gegenprobe mit einer Klimawirkung
    ohne Kennwert).

Teil 3 wird über die CLI mit dem Python der Testlauf-Umgebung erzeugt (nur die HTML-Vorstufe wird
gelesen); die Werte werden unabhängig aus den gepinnten Zelldaten und der Projektionstabelle
nachgerechnet.
"""

from __future__ import annotations

import csv
import gzip
import os
import re
import subprocess
import sys

import pytest

HIER = os.path.dirname(os.path.abspath(__file__))
BACKEND = os.path.dirname(HIER)
sys.path.insert(0, BACKEND)
sys.path.insert(0, HIER)

from test_ergebnisbericht_regeln import REGELN, Element, baum, html_text  # noqa: E402

AUS_PDF = "/tmp/kap2-ergebnisbericht/teil3.pdf"
AUS_HTML = "/tmp/kap2-ergebnisbericht/teil3.html"
ZELLDATEN = os.path.join(BACKEND, "data", "kalibrierung", "golden95_zellen_03256034.csv.gz")
ZAHL = re.compile(r"^\d{1,3}(?:\.\d{3})*(?:,\d+)?$")


def _zahl(text: str) -> float:
    return float(text.replace(".", "").replace(",", "."))


def _ohne_fussnote(e: Element) -> str:
    return "".join(k for k in e.kinder if isinstance(k, str)).strip()


@pytest.fixture(scope="module")
def teil3() -> Element:
    for pfad in (AUS_PDF, AUS_HTML):
        if os.path.exists(pfad):
            os.remove(pfad)
    lauf = subprocess.run(
        [sys.executable, "-m", "app.cli", "ergebnisbericht", "--beispiel", "warmsen",
         "--teile", "1,3", "--aus", AUS_PDF],
        cwd=BACKEND, capture_output=True, text=True, timeout=600,
    )
    assert lauf.returncode == 0, lauf.stdout[-2000:] + lauf.stderr[-4000:]
    with open(AUS_HTML, encoding="utf-8") as fh:
        wurzel = baum(fh.read())
    teile = [e for e in wurzel.alle() if e.tag == "section" and "teil" in e.klassen]
    treffer = [t for t in teile if any(e.tag == "h1" and e.attrs.get("id") == "teil-3"
                                       for e in t.alle())]
    assert len(treffer) == 1
    return treffer[0]


@pytest.fixture(scope="module")
def bezifferte() -> list[int]:
    """Kennungen der in Euro bezifferten Klimawirkungen aus dem Sammler (dieselbe Liste, über die
    Teil 1 seine Summe bildet)."""
    from app.services.ergebnisbericht.beispiel import beispiel
    from app.services.ergebnisbericht.sammler import sammle

    d = sammle(beispiel("warmsen"))
    return [w["kwra_id"] for w in d.klimawirkungen_im_bericht]


def _zeilen(teil: Element) -> list[Element]:
    return [e for e in teil.alle() if e.tag == "tr" and "klimawirkung" in e.klassen]


# (a) ─────────────────────────────────────────────────────────────────────────

def test_a_eine_zeile_je_bezifferter_klimawirkung(teil3, bezifferte):
    assert bezifferte, "ohne bezifferte Klimawirkung liefe der Test ins Leere"
    kennungen = [int(z.attrs["data-kwra"]) for z in _zeilen(teil3)]
    assert kennungen == bezifferte


def test_a_beobachtung_und_beide_szenarien_je_zeile(teil3):
    for z in _zeilen(teil3):
        zellen = [e for e in z.alle() if e.tag == "td"]
        klassen = [c.klassen for c in zellen]
        assert sum("beobachtung" in k for k in klassen) == 1, z.attrs
        assert sum("rcp45" in k for k in klassen) >= 1, z.attrs
        assert sum("rcp85" in k for k in klassen) >= 1, z.attrs
        for c in zellen:
            if c.klassen & {"beobachtung", "rcp45", "rcp85"}:
                zahlen = c.mit_klasse("klimazahl")
                assert len(zahlen) == 1, c.text()
                assert ZAHL.match(_ohne_fussnote(zahlen[0])), c.text()


def test_a_kopfzeile_nennt_dwd_und_szenarien(teil3):
    text = teil3.text()
    assert "RCP 4.5" in text and "RCP 8.5" in text
    assert "Deutscher Wetterdienst" in text and "Climate Data Center" in text


def test_a_werte_stimmen_mit_den_quellen(teil3):
    """#95: Beobachtung = einwohnergewichtete heiße Tage der Zelldaten; Projektion = Landesreihe."""
    from app.services.climate.dwd_data import get_climate_projection

    with gzip.open(ZELLDATEN, "rt", newline="", encoding="utf-8") as fh:
        zeilen = [r for r in csv.DictReader(fh) if r["gitter_id"] != "__ausserhalb__"]
    ew = sum(float(r["einwohner"]) for r in zeilen)
    beob = sum(float(r["hitzetage"]) * float(r["einwohner"]) for r in zeilen) / ew

    proj = get_climate_projection("Niedersachsen")
    z95 = next(z for z in _zeilen(teil3) if z.attrs["data-kwra"] == "95")
    zellen = [e for e in z95.alle() if e.tag == "td"]
    b = next(c for c in zellen if "beobachtung" in c.klassen)
    assert _zahl(_ohne_fussnote(b.mit_klasse("klimazahl")[0])) == pytest.approx(beob, abs=0.05)
    for sz in ("rcp45", "rcp85"):
        for c in (c for c in zellen if sz in c.klassen):
            jahr = int(c.attrs["data-jahr"])
            soll = proj["scenarios"][sz]["hot_days"][proj["years"].index(jahr)]
            assert _zahl(_ohne_fussnote(c.mit_klasse("klimazahl")[0])) == pytest.approx(soll)
    # RCP 8.5 liegt 2065 über RCP 4.5 — sonst wären die Spalten vertauscht.
    r45 = next(c for c in zellen if "rcp45" in c.klassen and c.attrs["data-jahr"] == "2065")
    r85 = next(c for c in zellen if "rcp85" in c.klassen and c.attrs["data-jahr"] == "2065")
    assert _zahl(_ohne_fussnote(r85.mit_klasse("klimazahl")[0])) > \
        _zahl(_ohne_fussnote(r45.mit_klasse("klimazahl")[0]))


# (b) ─────────────────────────────────────────────────────────────────────────

def test_b_jede_zahl_traegt_quelle_und_datenstand(teil3):
    zahlen = teil3.mit_klasse("klimazahl")
    assert zahlen
    fussnoten = {int(f.attrs["data-nr"]): f.text() for f in teil3.mit_klasse("fussnote")}
    for z in zahlen:
        assert z.attrs.get("data-quelle", "").strip(), z.text()
        assert z.attrs.get("data-datenstand", "").strip(), z.text()
        sup = z.mit_klasse("fn")
        assert len(sup) == 1, z.text()
        nr = int(sup[0].text())
        assert nr in fussnoten
        assert z.attrs["data-quelle"] in fussnoten[nr]
        assert z.attrs["data-datenstand"] in fussnoten[nr]
        # Datenstand nennt ein Jahr oder Datum.
        assert re.search(r"\d{4}", z.attrs["data-datenstand"]), z.attrs["data-datenstand"]


def test_b_keine_nackte_zahl_in_der_tabelle(teil3):
    """Jede Ziffernfolge in einer Datenzelle steht in einer .klimazahl (mit Quelle und Stand)."""
    for z in _zeilen(teil3):
        for c in (e for e in z.alle() if e.tag == "td"):
            if not c.klassen & {"beobachtung", "rcp45", "rcp85"}:
                continue
            ausserhalb = "".join(k for k in c.kinder if isinstance(k, str))
            assert not re.search(r"\d", ausserhalb), c.text()


def test_b_teil_hat_standzeile(teil3):
    assert teil3.mit_klasse("stand")


# (c) ─────────────────────────────────────────────────────────────────────────

def test_c_kein_tabellenfeld_leer(teil3):
    tabelle = next(e for e in teil3.alle() if e.tag == "table" and "klima" in e.klassen)
    for zelle in (e for e in tabelle.alle() if e.tag in ("td", "th")):
        assert zelle.text().strip(), "leeres Tabellenfeld in Teil 3"


def test_c_fehlender_kennwert_nennt_grund():
    """Gegenprobe: Eine bezifferte Klimawirkung ohne Kennwert bekommt eine Zeile mit Grund in
    jedem Feld, nie eine leere Zelle."""
    import datetime as dt
    from types import SimpleNamespace

    from app.services.ergebnisbericht.beispiel import beispiel
    from app.services.ergebnisbericht.klima import klimazeilen
    from app.services.ergebnisbericht.sammler import Stand
    from app.services.ergebnisbericht.teile import teil_3

    k = beispiel("warmsen")
    e = SimpleNamespace(hitzetage_mittel=11.3)
    wirkungen = [{"kwra_id": 95, "kwra_name": "Hitzebelastung"},
                 {"kwra_id": 96, "kwra_name": "Aeroallergene"}]
    d = SimpleNamespace(
        kommune=k, klima=klimazeilen(k, e, wirkungen),
        stand=Stand("Fassung 0.1", "#95", "M", "Zensus 2022", dt.date(2026, 9, 27)))
    wurzel = baum(f'<html><body><section class="teil">{teil_3(d)}</section></body></html>')
    zeilen = _zeilen(wurzel)
    assert [z.attrs["data-kwra"] for z in zeilen] == ["95", "96"]
    z96 = zeilen[1]
    for c in (e for e in z96.alle() if e.tag == "td"):
        assert c.text().strip()
        if c.klassen & {"beobachtung", "rcp45", "rcp85"}:
            assert c.mit_klasse("grund"), c.text()
            assert not c.mit_klasse("klimazahl")


# Harte Regeln an Teil 3 allein ────────────────────────────────────────────────

@pytest.mark.parametrize("nr", sorted(REGELN))
def test_harte_regeln_an_teil_3(teil3, nr):
    wurzel = Element("#wurzel", {}, [teil3])
    assert REGELN[nr](wurzel, [html_text(wurzel)]) == []
