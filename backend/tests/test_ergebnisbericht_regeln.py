"""Regeltest des PDF-Ergebnisberichts (T-1415): die harten Regeln der Gliederung an HTML und PDF.

Der Test erzeugt im Ordner ``backend/`` mit dem Python der Testlauf-Umgebung den Bericht für
``--beispiel warmsen`` mit **allen** vorhandenen Teilen (``render.TEILE``) und prüft an der
HTML-Vorstufe und am Text aus ``scripts/pdf_text.py``:

1. Kein Element ``.betrag`` ist leer oder zeigt 0; im ganzen Text steht kein Euro-Betrag 0
   („0 €“, „0,00 €“, „0 Euro“).
2. Jedes Element ``.summe`` enthält ein ``.nenner`` nach dem Muster
   ``\\d+ von \\d+ Klimawirkungen in Euro beziffert``.
3. Jedes ``.betrag`` trägt nicht leere Attribute ``data-berichtsstand``, ``data-methodikstand`` und
   ``data-datenstand``; jeder Teil (``section.teil``) hat eine Standzeile ``.stand``.
4. Der Text enthält weder ``docs/`` noch ``reviews/`` noch ``BEFUNDE_``.
5. Der Text enthält keinen Begriff der Stufen B und C der Transparenzgrenze.

Zu jeder Regel gibt es eine Gegenprobe: ein absichtlich verletztes HTML-Stück, das dieselbe
Prüffunktion durchfallen lässt. Ein regelkonformes Stück besteht alle fünf Prüfungen; so ist
belegt, dass jede Gegenprobe an ihrer eigenen Verletzung scheitert und nicht an etwas anderem.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from html.parser import HTMLParser

import pytest

HIER = os.path.dirname(os.path.abspath(__file__))
BACKEND = os.path.dirname(HIER)
REPO = os.path.dirname(BACKEND)
sys.path.insert(0, BACKEND)

AUS_PDF = "/tmp/kap2-ergebnisbericht/regeln.pdf"
AUS_HTML = "/tmp/kap2-ergebnisbericht/regeln.html"

NENNER_MUSTER = re.compile(r"\d+ von \d+ Klimawirkungen in Euro beziffert")
STAND_ATTRIBUTE = ("data-berichtsstand", "data-methodikstand", "data-datenstand")
# Euro-Betrag 0: „0 €“, „0,00 €“, „-0 €“, „0 Euro“, „0 EUR“ — nicht die letzte Null von „100.000 €“.
EURO_NULL = re.compile(r"(?<![\d.,])[-−]?0(?:[.,]0+)?\s?(?:€|EUR\b|Euro\b)")
VERBOTENE_PFADE = ("docs/", "reviews/", "BEFUNDE_")
# Stufen B und C der Transparenzgrenze (Gliederung, Abschnitt 4), Wortliste aus dem Ticket.
STUFE_B_C = ("Eich-Stichprobe", "Zwischentabelle", "Sensitivitätslauf", "Befund-Ledger",
             "Quellcode", "Erstellungskosten", ".py")


# ── HTML als Baum (nur Standardbibliothek) ──────────────────────────────────────

_LEER = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source",
         "track", "wbr"}


@dataclass
class Element:
    tag: str
    attrs: dict[str, str]
    kinder: list["Element | str"] = field(default_factory=list)

    @property
    def klassen(self) -> set[str]:
        return set((self.attrs.get("class") or "").split())

    def text(self) -> str:
        if self.tag in ("style", "script"):
            return ""
        return "".join(k if isinstance(k, str) else k.text() for k in self.kinder)

    def alle(self):
        yield self
        for k in self.kinder:
            if isinstance(k, Element):
                yield from k.alle()

    def mit_klasse(self, klasse: str) -> list["Element"]:
        return [e for e in self.alle() if klasse in e.klassen]


class _Baumbauer(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.wurzel = Element("#wurzel", {})
        self.stapel = [self.wurzel]

    def handle_starttag(self, tag, attrs):
        el = Element(tag, {k: (v or "") for k, v in attrs})
        self.stapel[-1].kinder.append(el)
        if tag not in _LEER:
            self.stapel.append(el)

    def handle_startendtag(self, tag, attrs):
        self.stapel[-1].kinder.append(Element(tag, {k: (v or "") for k, v in attrs}))

    def handle_endtag(self, tag):
        for i in range(len(self.stapel) - 1, 0, -1):
            if self.stapel[i].tag == tag:
                del self.stapel[i:]
                return

    def handle_data(self, data):
        self.stapel[-1].kinder.append(data)


def baum(html: str) -> Element:
    p = _Baumbauer()
    p.feed(html)
    p.close()
    return p.wurzel


def html_text(wurzel: Element) -> str:
    """Sichtbarer Text der HTML-Vorstufe plus Attributwerte (Verweise wie ``href`` zählen mit)."""
    teile = [wurzel.text()]
    for e in wurzel.alle():
        teile += [v for k, v in e.attrs.items() if k != "class"]
    return re.sub(r"\s+", " ", " ".join(teile))


# ── Die fünf Regeln als Prüffunktionen: Rückgabe ist die Liste der Verstöße ─────

def regel_1_keine_null(wurzel: Element, texte: list[str]) -> list[str]:
    verstoesse = []
    for b in wurzel.mit_klasse("betrag"):
        inhalt = b.text().strip()
        if not inhalt:
            verstoesse.append("leeres .betrag")
        elif not re.search(r"[1-9]", inhalt):
            verstoesse.append(f".betrag zeigt Null: {inhalt!r}")
    for text in texte:
        for m in EURO_NULL.finditer(text):
            verstoesse.append(f"Euro-Betrag 0 im Text: …{text[max(0, m.start() - 40):m.end() + 10]}…")
    return verstoesse


def regel_2_nenner(wurzel: Element, texte: list[str]) -> list[str]:
    verstoesse = []
    for s in wurzel.mit_klasse("summe"):
        nenner = s.mit_klasse("nenner")
        if not nenner:
            verstoesse.append(f".summe ohne .nenner: {s.text().strip()[:80]!r}")
        elif not any(NENNER_MUSTER.fullmatch(n.text().strip()) for n in nenner):
            verstoesse.append(f".nenner ohne Muster: {[n.text().strip() for n in nenner]!r}")
    return verstoesse


def regel_3_stand(wurzel: Element, texte: list[str]) -> list[str]:
    verstoesse = []
    for b in wurzel.mit_klasse("betrag"):
        for attr in STAND_ATTRIBUTE:
            if not (b.attrs.get(attr) or "").strip():
                verstoesse.append(f".betrag {b.text().strip()!r} ohne {attr}")
    teile = [e for e in wurzel.alle() if e.tag == "section" and "teil" in e.klassen]
    if not teile:
        verstoesse.append("kein Teil (section.teil) gefunden")
    for t in teile:
        if not t.mit_klasse("stand"):
            kopf = next((e.text().strip() for e in t.alle() if e.tag == "h1"), "?")
            verstoesse.append(f"Teil ohne Standzeile .stand: {kopf!r}")
    return verstoesse


def regel_4_keine_pfade(wurzel: Element, texte: list[str]) -> list[str]:
    return [f"{wort!r} im Text" for text in texte for wort in VERBOTENE_PFADE if wort in text]


def regel_5_keine_stufe_b_c(wurzel: Element, texte: list[str]) -> list[str]:
    return [f"{wort!r} im Text" for text in texte for wort in STUFE_B_C
            if wort.lower() in text.lower()]


REGELN = {
    1: regel_1_keine_null,
    2: regel_2_nenner,
    3: regel_3_stand,
    4: regel_4_keine_pfade,
    5: regel_5_keine_stufe_b_c,
}


# ── Der echte Bericht ───────────────────────────────────────────────────────────

@dataclass
class Bericht:
    wurzel: Element
    html_text: str
    pdf_text: str


@pytest.fixture(scope="module")
def bericht() -> Bericht:
    from app.services.ergebnisbericht.teile import TEILE

    for pfad in (AUS_PDF, AUS_HTML):
        if os.path.exists(pfad):
            os.remove(pfad)
    alle_teile = ",".join(str(nr) for nr in sorted(TEILE))
    lauf = subprocess.run(
        [sys.executable, "-m", "app.cli", "ergebnisbericht", "--beispiel", "warmsen",
         "--teile", alle_teile, "--aus", AUS_PDF],
        cwd=BACKEND, capture_output=True, text=True, timeout=600,
    )
    assert lauf.returncode == 0, lauf.stdout[-2000:] + lauf.stderr[-4000:]
    text = subprocess.run(
        [sys.executable, os.path.join(REPO, "scripts", "pdf_text.py"), AUS_PDF],
        capture_output=True, text=True, timeout=120,
    )
    assert text.returncode == 0, text.stderr[-2000:]
    with open(AUS_HTML, encoding="utf-8") as fh:
        wurzel = baum(fh.read())
    return Bericht(wurzel, html_text(wurzel), re.sub(r"\s+", " ", text.stdout))


def test_bericht_hat_alle_teile_und_betraege(bericht):
    from app.services.ergebnisbericht.teile import TEILE

    teile = [e for e in bericht.wurzel.alle() if e.tag == "section" and "teil" in e.klassen]
    assert len(teile) == len(TEILE)
    # Ohne ausgezeichnete Beträge und Summen liefen die Regeln 1 bis 3 ins Leere.
    assert bericht.wurzel.mit_klasse("betrag")
    assert bericht.wurzel.mit_klasse("summe")


@pytest.mark.parametrize("nr", sorted(REGELN))
def test_regel_im_bericht(bericht, nr):
    verstoesse = REGELN[nr](bericht.wurzel, [bericht.html_text, bericht.pdf_text])
    assert verstoesse == [], f"Regel {nr} verletzt:\n" + "\n".join(verstoesse)


def test_nenner_auch_im_pdf_text(bericht):
    """Jede Summe der Vorstufe kommt mit ihrem Nenner im PDF an."""
    summen = len(bericht.wurzel.mit_klasse("summe"))
    assert len(NENNER_MUSTER.findall(bericht.pdf_text)) >= summen


# ── Gegenproben: absichtlich verletzte HTML-Stücke ──────────────────────────────

STAND = ('data-berichtsstand="Fassung 0.1 vom 27.09.2026" '
         'data-methodikstand="#95 Rev. 9, Fortschreibung 7" '
         'data-datenstand="Zensus 2022, DWD 2016–2025, Preisstand 2024"')


def _stueck(inhalt: str) -> str:
    return f'<html><body><section class="teil"><h1>Teil 9 · Probe</h1>{inhalt}</section></body></html>'


REGELKONFORM = _stueck(
    f'<table><tr><td>#95 Hitzebelastung</td><td><span class="betrag" {STAND}>123.456 €</span></td></tr>'
    f'<tr class="summe"><td>Summe (<span class="nenner">1 von 139 Klimawirkungen in Euro beziffert'
    f'</span>)</td><td><span class="betrag" {STAND}>123.456 €</span></td></tr></table>'
    '<p class="stand">Stand: Bericht Fassung 0.1 vom 27.09.2026</p>'
)

GEGENPROBEN = {
    # Regel 1: einmal ein .betrag mit Null, einmal ein leerer, einmal eine Null im Fließtext.
    "1-betrag-null": (1, _stueck(f'<span class="betrag" {STAND}>0 €</span><p class="stand">Stand</p>')),
    "1-betrag-leer": (1, _stueck(f'<span class="betrag" {STAND}> </span><p class="stand">Stand</p>')),
    "1-text-null": (1, _stueck('<p>Schaden: 0,00 € je Jahr.</p><p class="stand">Stand</p>')),
    # Regel 2: eine Summe ohne Nenner und eine mit einem Nenner in falscher Form.
    "2-ohne-nenner": (2, _stueck('<table><tr class="summe"><td>Summe</td></tr></table>'
                                 '<p class="stand">Stand</p>')),
    "2-nenner-falsch": (2, _stueck('<table><tr class="summe"><td><span class="nenner">alle '
                                   'Klimawirkungen</span></td></tr></table><p class="stand">Stand</p>')),
    # Regel 3: ein Betrag ohne Datenstand und ein Teil ohne Standzeile.
    "3-betrag-ohne-stand": (3, _stueck(
        '<span class="betrag" data-berichtsstand="Fassung 0.1" data-methodikstand="#95" '
        'data-datenstand="">123 €</span><p class="stand">Stand</p>')),
    "3-teil-ohne-stand": (3, _stueck(f'<span class="betrag" {STAND}>123 €</span>')),
    # Regel 4: ein Pfad aus dem Produkt-Repo, einmal im Text, einmal als Verweis.
    "4-docs-text": (4, _stueck('<p>Methode siehe docs/methodik/95_hitzebelastung.md.</p>'
                               '<p class="stand">Stand</p>')),
    "4-befunde-verweis": (4, _stueck('<p><a href="reviews/BEFUNDE_95.md">Prüfakte</a></p>'
                                     '<p class="stand">Stand</p>')),
    # Regel 5: ein Begriff der Stufe B und einer der Stufe C.
    "5-stufe-b": (5, _stueck('<p>Die Eich-Stichprobe umfasst acht Kommunen.</p><p class="stand">Stand</p>')),
    "5-stufe-c": (5, _stueck('<p>Berechnet in schadensfunktion.py.</p><p class="stand">Stand</p>')),
}


def _pruefe(nr: int, html: str) -> list[str]:
    wurzel = baum(html)
    return REGELN[nr](wurzel, [html_text(wurzel)])


@pytest.mark.parametrize("nr", sorted(REGELN))
def test_regelkonformes_stueck_besteht(nr):
    assert _pruefe(nr, REGELKONFORM) == []


@pytest.mark.parametrize("name", sorted(GEGENPROBEN))
def test_gegenprobe_faellt_durch(name):
    nr, html = GEGENPROBEN[name]
    assert _pruefe(nr, html), f"Gegenprobe {name} hätte Regel {nr} verletzen müssen"


def test_jede_regel_hat_gegenprobe():
    assert {nr for nr, _ in GEGENPROBEN.values()} == set(REGELN)


def test_renderer_verweigert_null_betrag():
    """Die Quelle der Regel 1: ``_betrag`` druckt keine Null, sondern bricht ab."""
    import datetime as dt
    from types import SimpleNamespace

    from app.services.ergebnisbericht.sammler import Stand
    from app.services.ergebnisbericht.teile import _betrag

    d = SimpleNamespace(stand=Stand("Fassung 0.1", "#95", "M", "Zensus 2022", dt.date(2026, 9, 27)))
    assert "123 €" in _betrag(d, 123.0)
    for wert in (0, 0.0, 0.4, -5.0, float("nan")):
        with pytest.raises(ValueError):
            _betrag(d, wert)
