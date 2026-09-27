"""Teil 2 des PDF-Ergebnisberichts wird aus der Konformitäts-Checkliste erzeugt (T-1416, T-1530).

Abnahme:

(a) Teil 2 hat genau so viele Anforderungszeilen wie ``docs/KONFORMITAET_CHECKLISTE.md``;
(b) jede Zeile trägt den Status der Checkliste als „erfüllt“, „teilweise“ oder „offen“, bei
    „teilweise“ und „offen“ mit dem Kundensatz aus ``konformitaet_kundentext.py`` (T-1530) statt
    des internen Lückensatzes;
(c) eine Kopie der Checkliste mit geändertem Status einer Zeile ändert die Ausgabe dieser Zeile —
    der Teil ist erzeugt, nicht von Hand geschrieben. Geändert wird nur die Kopie in ``tmp_path``.
    Ändert der Statuswechsel den Status einer „teilweise“- oder „offen“-Zeile, bekommt
    ``KUNDENTEXT`` für diese Zeile per Monkeypatch einen zum neuen Status passenden Kundensatz
    mit — sonst bräche die Erzeugung wegen des in T-1530 geforderten Abgleichs ab.

Die Checkliste wird hier mit einem eigenen, einfachen Zähler gelesen, nicht mit ``lies_checkliste``,
damit der Test den Leser mitprüft.
"""

from __future__ import annotations

import datetime as dt
import html
import os
import re
import shutil
import sys
from types import SimpleNamespace

import pytest

HIER = os.path.dirname(os.path.abspath(__file__))
BACKEND = os.path.dirname(HIER)
REPO = os.path.dirname(BACKEND)
sys.path.insert(0, BACKEND)
sys.path.insert(0, HIER)

from app.services.ergebnisbericht import konformitaet  # noqa: E402
from app.services.ergebnisbericht.konformitaet import (  # noqa: E402
    CHECKLISTE, ERSATZSATZ, lies_checkliste, lueckensatz,
)
from app.data.konformitaet_kundentext import KUNDENTEXT  # noqa: E402
from app.services.ergebnisbericht.sammler import Stand  # noqa: E402
from app.services.ergebnisbericht.teile import TEILE, teil_2  # noqa: E402
from test_ergebnisbericht_regeln import REGELN, baum, html_text  # noqa: E402

PFAD = os.path.join(REPO, "docs", "KONFORMITAET_CHECKLISTE.md")
ZEILE = re.compile(r'<tr class="anforderung" data-nr="(\d+)">(.*?)</tr>', re.S)
ZELLE_STATUS = re.compile(r'<td class="status">(.*?)</td>', re.S)
ZELLE_LUECKE = re.compile(r'<td class="luecke">(.*?)</td>', re.S)


def _daten():
    stand = Stand("Fassung 0.1", "#95 Rev. 9", "M", "Zensus 2022", dt.date(2026, 9, 27))
    return SimpleNamespace(stand=stand, beziffert_text="1 von 139 Klimawirkungen in Euro beziffert")


def _checkliste_roh(pfad: str) -> dict[int, str]:
    """Nr → Status aus der Tabelle unter „## Tabelle“, mit eigenem Zähler."""
    with open(pfad, encoding="utf-8") as fh:
        text = fh.read()
    abschnitt = text.split("\n## Tabelle\n", 1)[1].split("\n### ", 1)[0]
    ergebnis = {}
    for zeile in abschnitt.splitlines():
        m = re.match(r"\|\s*(\d+)\s*\|", zeile)
        if m:
            ergebnis[int(m.group(1))] = zeile.strip().strip("|").split("|")[4].strip()
    return ergebnis


def _zeilen(teil: str) -> dict[int, tuple[str, str]]:
    """Nr → (Status, Lückensatz) aus dem erzeugten Teil 2."""
    ergebnis = {}
    for nr, inhalt in ZEILE.findall(teil):
        status = html.unescape(ZELLE_STATUS.search(inhalt).group(1))
        luecke = html.unescape(ZELLE_LUECKE.search(inhalt).group(1))
        ergebnis[int(nr)] = (status, luecke)
    return ergebnis


@pytest.fixture(scope="module")
def teil() -> str:
    return teil_2(_daten())


def test_checkliste_ist_die_echte():
    assert os.path.samefile(CHECKLISTE, PFAD)


def test_teil_2_ist_im_bericht():
    assert TEILE[2] is teil_2


# (a) ─────────────────────────────────────────────────────────────────────────

def test_a_gleich_viele_zeilen_wie_checkliste(teil):
    roh = _checkliste_roh(PFAD)
    assert len(roh) >= 25
    zeilen = _zeilen(teil)
    assert len(zeilen) == len(roh)
    assert sorted(zeilen) == sorted(roh)
    assert len(ZEILE.findall(teil)) == len(roh)


# (b) ─────────────────────────────────────────────────────────────────────────

def test_b_status_und_kundensatz_je_zeile(teil):
    roh = _checkliste_roh(PFAD)
    for nr, (status, satz) in _zeilen(teil).items():
        assert status in ("erfüllt", "teilweise", "offen"), (nr, status)
        assert status == roh[nr], (nr, status, roh[nr])
        if status in ("teilweise", "offen"):
            assert len(satz) > 20 and satz not in ("—", "-"), (nr, satz)
            kundentext_status, kundensatz = KUNDENTEXT[nr]
            assert kundentext_status == status, (nr, kundentext_status, status)
            assert satz == kundensatz, (nr, satz, kundensatz)
        else:
            assert satz == "—", (nr, satz)


def test_b_zaehlung_im_text(teil):
    werte = list(_checkliste_roh(PFAD).values())
    for status in ("erfüllt", "teilweise", "offen"):
        assert f"{werte.count(status)} {status}" in teil


# (c) ─────────────────────────────────────────────────────────────────────────

def _kopie_mit_status(tmp_path, nr: int, neu: str, luecke: str | None = None) -> str:
    kopie = tmp_path / "KONFORMITAET_CHECKLISTE.md"
    shutil.copy(PFAD, kopie)
    zeilen = kopie.read_text(encoding="utf-8").split("\n")
    for i, zeile in enumerate(zeilen):
        if re.match(rf"\|\s*{nr}\s*\|", zeile):
            zellen = zeile.split("|")
            zellen[5] = f" {neu} "
            if luecke is not None:
                zellen[7] = f" {luecke} "
            zeilen[i] = "|".join(zellen)
            break
    else:
        raise AssertionError(f"Zeile {nr} nicht gefunden")
    kopie.write_text("\n".join(zeilen), encoding="utf-8")
    return str(kopie)


@pytest.mark.parametrize("nr, neu, luecke, neuer_kundensatz", [
    # erfüllt → offen: neue Zeile braucht einen (im echten Bestand fehlenden) Kundensatz.
    (1, "offen", "Die Wirkungsketten fehlen im Produkt.",
     "Die Herleitung über Wirkungsketten fehlt im Produkt."),
    # offen → teilweise: der bestehende Kundensatz zu Zeile 12 passt im Status nicht mehr.
    (12, "teilweise", None,
     "Die Bundesstrategie wird im Produkt nur zum Teil abgebildet."),
    (2, "erfüllt", None, None),                              # teilweise → erfüllt, kein Kundensatz nötig
])
def test_c_statuswechsel_in_kopie_aendert_nur_diese_zeile(monkeypatch, tmp_path, teil, nr, neu, luecke,
                                                           neuer_kundensatz):
    vorher_datei = open(PFAD, encoding="utf-8").read()
    kopie = _kopie_mit_status(tmp_path, nr, neu, luecke)
    if neuer_kundensatz is not None:
        kundentext = dict(KUNDENTEXT)
        kundentext[nr] = (neu, neuer_kundensatz)
        monkeypatch.setattr(konformitaet, "KUNDENTEXT", kundentext)
    neu_teil = teil_2(_daten(), checkliste=kopie)
    alt, neu_zeilen = _zeilen(teil), _zeilen(neu_teil)
    assert neu_zeilen[nr][0] == neu
    assert neu_zeilen[nr] != alt[nr]
    for andere in alt:
        if andere != nr:
            assert neu_zeilen[andere] == alt[andere], andere
    # Die echte Checkliste bleibt unberührt.
    assert open(PFAD, encoding="utf-8").read() == vorher_datei


def test_c_unbekannter_status_bricht_ab(tmp_path):
    kopie = _kopie_mit_status(tmp_path, 3, "fast erfüllt")
    with pytest.raises(ValueError, match="unbekannter Status"):
        teil_2(_daten(), checkliste=kopie)


def test_c_teilweise_ohne_luecke_bricht_ab(tmp_path):
    kopie = _kopie_mit_status(tmp_path, 3, "teilweise", "—")
    with pytest.raises(ValueError, match="ohne Lücke"):
        lies_checkliste(kopie)


# Regeln der Gliederung an Teil 2 allein ────────────────────────────────────────

@pytest.mark.parametrize("nr", sorted(REGELN))
def test_harte_regeln_an_teil_2(teil, nr):
    wurzel = baum(f'<html><body><section class="teil">{teil}</section></body></html>')
    assert REGELN[nr](wurzel, [html_text(wurzel)]) == []


def test_beleg_spalte_nicht_im_teil(teil):
    assert "Beleg im Produkt" not in teil
    assert "backend/" not in teil and "frontend/" not in teil


def test_lueckensatz_filtert_interne_verweise():
    roh = ("Erster Satz ist sichtbar (siehe docs/X.md). Zweiter Satz nennt "
           + chr(96) + "funktion()" + chr(96) + ". Dritter Satz bleibt; Kostensatz 0 € fällt weg. "
           "Primärtext nicht gelesen (T-0531-ceo). Einzelnachweis: Abschnitt „Gegenprobe Zeile 7“.")
    satz = lueckensatz(roh)
    assert satz == "Erster Satz ist sichtbar. Dritter Satz bleibt. Primärtext nicht gelesen."
    assert lueckensatz("Nur docs/X.md intern.") == ERSATZSATZ
    assert "Kosten der Wiederherstellung" in lueckensatz("Es wird mit Wiederherstellungskosten bewertet.")
