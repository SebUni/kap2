"""Kundensätze der Konformitäts-Checkliste für Teil 2 des PDF-Ergebnisberichts (T-1530).

Teil 2 zeigt bei „teilweise“ und „offen“ den Kundensatz aus
``backend/app/data/konformitaet_kundentext.py`` statt der internen Spalte „Lücke“ aus
``docs/KONFORMITAET_CHECKLISTE.md`` (Entscheidung des CEO, 27.09.2026, Kontext T-1530).

Abnahme:

(1) ``KUNDENTEXT`` enthält genau die Zeilen der echten Checkliste, die den Status „teilweise“ oder
    „offen“ tragen, jeweils mit demselben Status.
(3) Kein Kundensatz enthält einen Dateipfad, eine Ticketkennung, einen Code-Bezeichner (Backtick,
    Funktionsaufruf mit ``()``, Wort mit Unterstrich) oder eines der Wörter „Repo“, „Test“,
    „Einzelnachweis“, „nicht gelesen“, „Primärtext“, „Gegenprobe“.
(2) Weicht auf einer Kopie der Checkliste unter ``tmp_path`` der Status einer Zeile vom Status in
    ``KUNDENTEXT`` ab, oder fehlt der Kundensatz ganz, bricht die Erzeugung von Teil 2
    (``teil_2(..., checkliste=kopie)``) mit einer Fehlermeldung ab, die die Zeilennummer nennt und
    auf ``konformitaet_kundentext.py`` verweist — nicht nur der isolierte Aufruf von ``kundensatz()``.
"""

from __future__ import annotations

import datetime as dt
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

from app.data.konformitaet_kundentext import KUNDENTEXT  # noqa: E402
from app.services.ergebnisbericht.konformitaet import (  # noqa: E402
    CHECKLISTE, kundensatz, lies_checkliste,
)
from app.services.ergebnisbericht.sammler import Stand  # noqa: E402
from app.services.ergebnisbericht.teile import teil_2  # noqa: E402

PFAD = os.path.join(REPO, "docs", "KONFORMITAET_CHECKLISTE.md")


def _daten():
    stand = Stand("Fassung 0.1", "#95 Rev. 9", "M", "Zensus 2022", dt.date(2026, 9, 27))
    return SimpleNamespace(stand=stand, beziffert_text="1 von 139 Klimawirkungen in Euro beziffert")


def test_checkliste_ist_die_echte():
    assert os.path.samefile(CHECKLISTE, PFAD)


# ── Punkt 1 ──────────────────────────────────────────────────────────────────

def test_kundentext_enthaelt_genau_die_nicht_erfuellten_zeilen():
    zeilen = lies_checkliste()
    erwartet = {z.nr: z.status for z in zeilen if z.status != "erfüllt"}
    tatsaechlich = {nr: status for nr, (status, _satz) in KUNDENTEXT.items()}
    assert tatsaechlich == erwartet


def test_kundentext_hat_status_teilweise_oder_offen():
    for nr, (status, _satz) in KUNDENTEXT.items():
        assert status in ("teilweise", "offen"), (nr, status)


# ── Punkt 3: Verbote als Muster ───────────────────────────────────────────────

VERBOTENE_WOERTER = ("Repo", "Test", "Einzelnachweis", "nicht gelesen", "Primärtext", "Gegenprobe")
MUSTER_PFAD = re.compile(r"[\w./-]+/[\w./-]+\.\w+")
MUSTER_TICKET = re.compile(r"\bT-\d+")
MUSTER_BACKTICK = re.compile(re.escape(chr(96)))
MUSTER_FUNKTIONSAUFRUF = re.compile(r"\b\w+\(\)")
# Ein Wort mit Unterstrich, wie ein Code-Bezeichner (nicht: Bindestrich, nicht: einzelne Ziffern).
MUSTER_UNTERSTRICH = re.compile(r"\b[A-Za-zÄÖÜäöüß]+_[A-Za-zÄÖÜäöüß_]+\b")
# Interne Anforderungskennung wie „A1“ oder „(A9)“ (T-1561).
MUSTER_ANFORDERUNGSKENNUNG = re.compile(r"\bA[0-9]+\b")


@pytest.mark.parametrize("nr", sorted(KUNDENTEXT))
def test_kundensatz_ohne_verbotene_begriffe(nr):
    _status, satz = KUNDENTEXT[nr]
    for wort in VERBOTENE_WOERTER:
        assert wort not in satz, f"Zeile {nr}: verbotenes Wort {wort!r} im Kundensatz"
    assert not MUSTER_PFAD.search(satz), f"Zeile {nr}: Dateipfad im Kundensatz"
    assert not MUSTER_TICKET.search(satz), f"Zeile {nr}: Ticketkennung im Kundensatz"
    assert not MUSTER_BACKTICK.search(satz), f"Zeile {nr}: Backtick im Kundensatz"
    assert not MUSTER_FUNKTIONSAUFRUF.search(satz), f"Zeile {nr}: Funktionsaufruf im Kundensatz"
    assert not MUSTER_UNTERSTRICH.search(satz), \
        f"Zeile {nr}: Code-Bezeichner mit Unterstrich im Kundensatz"
    assert not MUSTER_ANFORDERUNGSKENNUNG.search(satz), \
        f"Zeile {nr}: interne Anforderungskennung im Kundensatz"


# ── Punkt 2 ────────────────────────────────────────────────────────────────────

def _kopie_mit_status(tmp_path, nr: int, neuer_status: str) -> str:
    kopie = tmp_path / "KONFORMITAET_CHECKLISTE.md"
    shutil.copy(PFAD, kopie)
    zeilen = kopie.read_text(encoding="utf-8").split("\n")
    for i, zeile in enumerate(zeilen):
        if re.match(rf"\|\s*{nr}\s*\|", zeile):
            zellen = zeile.split("|")
            zellen[5] = f" {neuer_status} "
            if neuer_status != "erfüllt" and zellen[7].strip() in ("", "—", "-"):
                zellen[7] = " Lücke für den Test. "
            zeilen[i] = "|".join(zellen)
            break
    else:
        raise AssertionError(f"Zeile {nr} nicht gefunden")
    kopie.write_text("\n".join(zeilen), encoding="utf-8")
    return str(kopie)


def test_status_abweichend_von_kundentext_bricht_teil_2_ab(tmp_path):
    # Zeile 2 ist im Kundentext als "teilweise" geführt; die Kopie hebt sie auf "offen" — der
    # Kundensatz ist damit veraltet, und die Erzeugung von Teil 2 muss daran abbrechen, nicht ihn
    # einfach zeigen.
    nr = 2
    assert KUNDENTEXT[nr][0] == "teilweise"
    kopie = _kopie_mit_status(tmp_path, nr, "offen")
    zeilen = {z.nr: z.status for z in lies_checkliste(kopie)}
    assert zeilen[nr] == "offen"
    with pytest.raises(ValueError, match=rf"Zeile {nr}.*konformitaet_kundentext\.py") as fehler:
        teil_2(_daten(), checkliste=kopie)
    assert f"Zeile {nr}" in str(fehler.value)
    assert "konformitaet_kundentext.py" in str(fehler.value)


def test_fehlender_kundensatz_bricht_teil_2_ab(tmp_path):
    # Zeile 5 ist heute "erfüllt" und hat deshalb keinen Eintrag in KUNDENTEXT; kippt ihr Status
    # auf "offen", fehlt der nötige Kundensatz ganz, und die Erzeugung von Teil 2 muss abbrechen.
    # (Bis T-1868 diente Zeile 14, bis T-1870 Zeile 1, bis T-1871 Zeile 3, bis T-1872 Zeile 4 als
    # Beispiel; alle stehen seit ihrer Gegenprobe auf "teilweise".)
    nr = 5
    assert nr not in KUNDENTEXT
    kopie = _kopie_mit_status(tmp_path, nr, "offen")
    zeilen = {z.nr: z.status for z in lies_checkliste(kopie)}
    assert zeilen[nr] == "offen"
    with pytest.raises(ValueError, match=rf"Zeile {nr}.*konformitaet_kundentext\.py") as fehler:
        teil_2(_daten(), checkliste=kopie)
    assert f"Zeile {nr}" in str(fehler.value)
    assert "konformitaet_kundentext.py" in str(fehler.value)


def test_passender_kundensatz_geht_durch():
    nr = 2
    status, satz = KUNDENTEXT[nr]
    assert kundensatz(nr, status) == satz
