"""Teil 9 des PDF-Ergebnisberichts: Anhang mit Anlagen und Exporten (T-1420).

Der Test erzeugt wie der Regeltest den Bericht für ``--beispiel warmsen`` mit allen vorhandenen
Teilen über den Befehl ``python -m app.cli ergebnisbericht`` und liest die HTML-Vorstufe. Geprüft:

(a) Teil 9 nennt je in Euro bezifferter Klimawirkung ihren Methodik-Bericht als Anlage, mit Titel
    und Revision — beide unabhängig vom Renderer aus Überschrift und Statuszeile des Berichts
    gelesen;
(b) Teil 9 nennt GeoPackage, Maßnahmen-Excel und Parameter-Excel mit dem Dateinamen, den die
    Namensregel der Downloads (Paket 11, ``download_namen.download_dateiname``) für Warmsen liefert;
(c) jeder Verweis auf eine Methodenbeschreibung in den Teilen 0 bis 8 („Bericht #95“,
    „Methodik-Bericht #95“, „Methodenbeschreibung“) nennt eine Anlage aus Teil 9, und kein Teil
    nennt einen Pfad. Gegenproben belegen, dass die Prüffunktion an beiden Verstößen scheitert.
"""

from __future__ import annotations

import glob
import os
import re
import subprocess
import sys

import pytest

HIER = os.path.dirname(os.path.abspath(__file__))
BACKEND = os.path.dirname(HIER)
REPO = os.path.dirname(BACKEND)
sys.path.insert(0, BACKEND)
sys.path.insert(0, HIER)

from test_ergebnisbericht_regeln import Element, baum  # noqa: E402

AUS_PDF = "/tmp/kap2-ergebnisbericht/teil9.pdf"
AUS_HTML = "/tmp/kap2-ergebnisbericht/teil9.html"
METHODIK = os.path.join(REPO, "docs", "methodik")

# Warmsen (Beispielkommune): Name und amtlicher Gemeindeschlüssel.
NAME, AGS = "Warmsen", "03256034"
EXPORTE_ERWARTET = {
    "geodaten": ("gpkg", "geodaten_Warmsen_03256034.gpkg"),
    "massnahmen": ("xlsx", "massnahmen_Warmsen_03256034.xlsx"),
    "parameter": ("xlsx", "parameter_Warmsen_03256034.xlsx"),
}

VERWEIS = re.compile(r"(Anlage (M\d+), )?(?:Methodik-)?Bericht #(\d+)")
METHODENBESCHREIBUNG = re.compile(r"Methodenbeschreibung")
# Pfad im Produkt-Repo (Internetadressen amtlicher Quellen sind kein Pfad in diesem Sinn).
PFAD = re.compile(r"docs/|reviews/|BEFUNDE_|\bbackend/|\bfrontend/|\b[\w-]+\.md\b")
BLOCK = {"p", "li", "td", "th", "h1", "h2", "h3", "div"}


# ── Bericht erzeugen ────────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def wurzel() -> Element:
    from app.services.ergebnisbericht.teile import TEILE

    for pfad in (AUS_PDF, AUS_HTML):
        if os.path.exists(pfad):
            os.remove(pfad)
    lauf = subprocess.run(
        [sys.executable, "-m", "app.cli", "ergebnisbericht", "--beispiel", "warmsen",
         "--teile", ",".join(str(nr) for nr in sorted(TEILE)), "--aus", AUS_PDF],
        cwd=BACKEND, capture_output=True, text=True, timeout=600,
    )
    assert lauf.returncode == 0, lauf.stdout[-2000:] + lauf.stderr[-4000:]
    with open(AUS_HTML, encoding="utf-8") as fh:
        return baum(fh.read())


def teile_nach_nummer(wurzel: Element) -> dict[int, Element]:
    ergebnis = {}
    for sec in wurzel.alle():
        if sec.tag != "section" or "teil" not in sec.klassen:
            continue
        kopf = next((e for e in sec.alle() if e.tag == "h1"), None)
        m = re.fullmatch(r"teil-(\d+)", (kopf.attrs.get("id") if kopf else "") or "")
        if m:
            ergebnis[int(m.group(1))] = sec
    return ergebnis


@pytest.fixture(scope="module")
def teil9(wurzel) -> Element:
    teile = teile_nach_nummer(wurzel)
    assert 9 in teile, "Teil 9 fehlt im Bericht"
    return teile[9]


def _text(e: Element) -> str:
    return re.sub(r"\s+", " ", e.text()).strip()


def _zelle(zeile: Element, klasse: str) -> str:
    zellen = zeile.mit_klasse(klasse)
    assert zellen, f"Zelle .{klasse} fehlt in {_text(zeile)!r}"
    return _text(zellen[0])


def _anlagen(teil9: Element) -> dict[str, Element]:
    return {z.attrs["id"].removeprefix("anlage-"): z for z in teil9.mit_klasse("anlage")}


# ── (a) Methodik-Berichte als Anlage mit Titel und Revision ─────────────────────

def _bericht_kopf(nr: int) -> tuple[str, str]:
    """Titel (Überschrift nach dem Gedankenstrich) und Revision aus der Statuszeile."""
    dateien = glob.glob(os.path.join(METHODIK, f"{nr}_*.md"))
    assert dateien, f"Methodik-Bericht #{nr} nicht gefunden"
    with open(sorted(dateien)[0], encoding="utf-8") as fh:
        zeilen = fh.read(4000).splitlines()
    titel = zeilen[0].removeprefix("# ").split(" — ", 1)[1].strip()
    status = next(z for z in zeilen if z.startswith("Status:"))
    revision = re.search(r"Rev\. \d+, Fortschreibung \d+", status).group(0)
    return titel, revision


def test_a_je_bezifferter_klimawirkung_eine_anlage(teil9):
    from app.services.ergebnisbericht.beispiel import beispiel
    from app.services.ergebnisbericht.sammler import sammle

    d = sammle(beispiel("warmsen"))
    beziffert = [int(w["kwra_id"]) for w in d.klimawirkungen_im_bericht]
    assert beziffert, "Der Bericht beziffert keine Klimawirkung; (a) liefe ins Leere"
    anlagen = _anlagen(teil9)
    for nr in beziffert:
        zeile = anlagen.get(f"M{nr}")
        assert zeile is not None, f"Keine Anlage für den Methodik-Bericht #{nr} in Teil 9"
        assert zeile.attrs.get("data-kwra") == str(nr)
        titel, revision = _bericht_kopf(nr)
        assert _zelle(zeile, "titel") == titel
        assert _zelle(zeile, "revision") == revision
        assert _zelle(zeile, "kennung") == f"Anlage M{nr}"


def test_a_revision_ist_die_aus_der_statuszeile():
    """#95 steht heute auf Rev. 8, Fortschreibung 7 — die Anlage darf keinen älteren Stand nennen."""
    assert _bericht_kopf(95) == ("Hitzebelastung", "Rev. 8, Fortschreibung 7")


# ── (b) Exporte mit Dateinamen nach der Namensregel ────────────────────────────

def test_b_exporte_mit_dateinamen_der_namensregel(teil9):
    from app.services.download_namen import download_dateiname

    zeilen = {z.attrs.get("data-art"): z for z in teil9.mit_klasse("export")}
    assert set(zeilen) == set(EXPORTE_ERWARTET)
    for art, (endung, erwartet) in EXPORTE_ERWARTET.items():
        assert download_dateiname(art, NAME, AGS, endung) == erwartet
        assert _zelle(zeilen[art], "dateiname") == erwartet


def test_b_bezeichnungen_der_exporte(teil9):
    text = _text(teil9)
    for bezeichnung in ("GeoPackage", "Maßnahmen-Excel", "Parameter-Excel"):
        assert bezeichnung in text


# ── (c) Verweise in den Teilen 0 bis 8 nennen eine Anlage, keinen Pfad ─────────

def _bloecke(teil: Element):
    """Kleinste Blockelemente mit eigenem Text (ein Verweis wird in seinem Block beurteilt)."""
    for e in teil.alle():
        if e.tag in BLOCK and not any(k.tag in BLOCK for k in e.alle() if k is not e):
            yield e


def verweis_verstoesse(teil: Element, anlagen: set[str]) -> tuple[list[str], int]:
    """(Verstöße, Zahl der geprüften Verweise) in einem Teil."""
    verstoesse, n = [], 0
    for block in _bloecke(teil):
        text = _text(block)
        for m in VERWEIS.finditer(text):
            n += 1
            kennung, nr = m.group(2), m.group(3)
            if kennung is None:
                verstoesse.append(f"Verweis ohne Anlage: …{text[max(0, m.start() - 40):m.end() + 20]}…")
            elif kennung != f"M{nr}" or kennung not in anlagen:
                verstoesse.append(f"Anlage {kennung} (für #{nr}) steht nicht in Teil 9")
        if METHODENBESCHREIBUNG.search(text):
            n += 1
            genannt = set(re.findall(r"Anlage (M\d+)", text))
            if not genannt or not genannt <= anlagen:
                verstoesse.append(f"Methodenbeschreibung ohne Anlage aus Teil 9: {text[:80]!r}")
    for e in teil.alle():
        for wert in [v for k, v in e.attrs.items() if k != "class"]:
            if PFAD.search(wert):
                verstoesse.append(f"Pfad im Attribut: {wert!r}")
    for m in PFAD.finditer(_text(teil)):
        verstoesse.append(f"Pfad im Text: {m.group(0)!r}")
    return verstoesse, n


def test_c_verweise_nennen_anlage_und_keinen_pfad(wurzel, teil9):
    anlagen = set(_anlagen(teil9))
    assert anlagen, "Teil 9 nennt keine Anlage"
    teile = teile_nach_nummer(wurzel)
    assert set(range(9)) <= set(teile), f"Teile fehlen: {sorted(set(range(9)) - set(teile))}"
    alle, geprueft = [], 0
    for nr in range(9):
        verstoesse, n = verweis_verstoesse(teile[nr], anlagen)
        alle += [f"Teil {nr}: {v}" for v in verstoesse]
        geprueft += n
    assert alle == [], "\n".join(alle)
    # Ohne Verweis liefe (c) ins Leere: Teil 0 (Methodikversion), 4 und 7 verweisen heute.
    assert geprueft > 0


def test_c_teil0_nennt_die_anlage(wurzel):
    text = _text(teile_nach_nummer(wurzel)[0])
    assert "Anlage M95, Methodik-Bericht #95" in text


def _stueck(inhalt: str) -> Element:
    return baum(f'<section class="teil"><h1 id="teil-4">Teil 4</h1>{inhalt}</section>')


GEGENPROBEN = {
    "ohne-anlage": "<p>Kostensatz nach Bericht #95 §3.5.</p>",
    "fremde-anlage": "<p>Siehe Anlage M96, Methodik-Bericht #96 §2.</p>",
    "falsche-kennung": "<p>Siehe Anlage M98, Methodik-Bericht #95 §2.</p>",
    "methodenbeschreibung": "<p>Die Methodenbeschreibung liegt beim Hersteller.</p>",
    "pfad-text": "<p>Methode siehe docs/methodik/95_hitzebelastung.md.</p>",
    "pfad-verweis": '<p><a href="95_hitzebelastung.md">Methode</a></p>',
}


@pytest.mark.parametrize("name", sorted(GEGENPROBEN))
def test_gegenprobe_faellt_durch(name):
    verstoesse, _ = verweis_verstoesse(_stueck(GEGENPROBEN[name]), {"M95"})
    assert verstoesse, f"Gegenprobe {name} hätte durchfallen müssen"


def test_regelkonformes_stueck_besteht():
    verstoesse, n = verweis_verstoesse(
        _stueck("<p>Setzung von KAP3 (Anlage M95, Methodik-Bericht #95 §3.5).</p>"), {"M95"})
    assert verstoesse == [] and n == 1
