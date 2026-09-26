"""Umsetzungsebene je Maßnahme (app/data/massnahmen_umsetzung.py, T-1132-cto, A9 der Gegenprobe Zeile 19).

Seit T-1193-ceo auch das Feld ``ebenen`` und die im Repo abgelegten Quellen samt Textabbild."""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.data import catalog  # noqa: E402
from app.data.massnahmen_umsetzung import EBENEN_WERTE, MASSNAHMEN_UMSETZUNG  # noqa: E402

CODES = sorted(MASSNAHMEN_UMSETZUNG)


def test_genau_ein_eintrag_je_katalogcode():
    katalog_codes = [m["code"] for m in catalog.MEASURES]
    assert len(katalog_codes) == len(set(katalog_codes))
    assert set(MASSNAHMEN_UMSETZUNG) == {m["code"] for m in catalog.MEASURES}


@pytest.mark.parametrize("code", CODES)
def test_schluessel(code):
    eintrag = MASSNAHMEN_UMSETZUNG[code]
    assert {"umsetzung", "partner", "beleg"} <= set(eintrag)


@pytest.mark.parametrize("code", CODES)
def test_umsetzung_und_partner(code):
    eintrag = MASSNAHMEN_UMSETZUNG[code]
    assert eintrag["umsetzung"] in ("kommune_allein", "mit_partnern")
    partner = eintrag["partner"]
    assert isinstance(partner, list)
    assert all(isinstance(p, str) and p.strip() for p in partner)
    assert bool(partner) == (eintrag["umsetzung"] == "mit_partnern")


@pytest.mark.parametrize("code", CODES)
def test_beleg_quelle_mit_seite_oder_abschaetzung(code):
    beleg = MASSNAHMEN_UMSETZUNG[code]["beleg"]
    assert isinstance(beleg, dict)
    hat_quelle = bool(str(beleg.get("quelle", "")).strip()) and bool(str(beleg.get("seite", "")).strip())
    hat_abschaetzung = bool(beleg.get("abschaetzung"))
    assert hat_quelle or hat_abschaetzung
    if hat_abschaetzung:
        herleitung = str(beleg.get("herleitung", "")).strip()
        # mindestens ein Satz: Text mit Satzschlusszeichen
        assert len(herleitung.split()) >= 3
        assert herleitung[-1] in ".!?"


# --- Feld ebenen (T-1193-ceo) ---------------------------------------------------------------------------------


@pytest.mark.parametrize("code", CODES)
def test_ebenen_werte(code):
    ebenen = MASSNAHMEN_UMSETZUNG[code]["ebenen"]
    assert isinstance(ebenen, list) and ebenen
    assert len(ebenen) == len(set(ebenen))
    assert set(ebenen) <= set(EBENEN_WERTE)


@pytest.mark.parametrize("code", CODES)
def test_jede_ebene_ist_begruendet(code):
    eintrag = MASSNAHMEN_UMSETZUNG[code]
    begruendung = eintrag["beleg"].get("ebenen_begruendung", "")
    for ebene in eintrag["ebenen"]:
        assert f"{ebene}:" in begruendung, f"{code}: Ebene {ebene} ohne Begründung"


def test_kreisebene_kommt_vor():
    assert any("kreis" in e["ebenen"] for e in MASSNAHMEN_UMSETZUNG.values())


@pytest.mark.parametrize("code", CODES)
def test_gesundheitsamt_nennt_kreis_und_kreisfreie_stadt(code):
    eintrag = MASSNAHMEN_UMSETZUNG[code]
    for partner in eintrag["partner"]:
        if "Gesundheitsamt" in partner:
            assert "kreisangehörigen Gemeinden beim Landkreis" in partner
            assert "kreisfreien Städten bei der Stadt selbst" in partner
            assert "kreis" in eintrag["ebenen"]


# --- Abgelegte Quellen und Seitenangaben -----------------------------------------------------------------------

REPO = Path(__file__).resolve().parents[2]


def _quellen(beleg):
    if beleg.get("quelle"):
        yield beleg
    yield from beleg.get("weitere_quellen", [])


def _textabbild(quelle):
    m = re.search(r"abgelegt unter (docs/quellen/\S+?\.pdf)", quelle)
    assert m, "Quelle ohne Ablage im Repo"
    pdf = REPO / m.group(1)
    txt = pdf.with_suffix(".txt")
    assert pdf.is_file() and txt.is_file()
    seiten = re.split(r"^=== Seite (\d+) ===$", txt.read_text(encoding="utf-8"), flags=re.M)
    return {int(seiten[i]): seiten[i + 1] for i in range(1, len(seiten) - 1, 2)}


def _norm(text):
    text = re.sub("­\\s*", "", text)  # weiches Trennzeichen am Zeilenende
    text = re.sub(r"(\w)-\n\s*(\w)", r"\1\2", text)
    return " ".join(text.split())


def _seitenzahlen(seite):
    zahlen = set()
    for teil in str(seite).split(","):
        grenzen = [int(x) for x in re.split("[–-]", teil.strip())]
        zahlen.update(range(grenzen[0], grenzen[-1] + 1))
    return zahlen


@pytest.mark.parametrize("code", CODES)
def test_seitenangaben_stehen_im_textabbild(code):
    for q in _quellen(MASSNAHMEN_UMSETZUNG[code]["beleg"]):
        seiten = _textabbild(q["quelle"])
        cited = _seitenzahlen(q["seite"])
        assert cited <= set(seiten), f"{code}: Seite fehlt im Textabbild"
        text = _norm(" ".join(seiten[s] for s in cited))
        for zitat in re.findall("„([^„“]+)“", q.get("fundstelle", "")):
            zitat = _norm(zitat.replace("…", "")).strip(" ,")
            assert zitat in text, f"{code}: Zitat nicht auf den genannten Seiten: {zitat}"
