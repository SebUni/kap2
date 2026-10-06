"""Die Teile des PDF-Ergebnisberichts als HTML-Abschnitte.

Gliederung: ``dokumente/produkt/pdf-ergebnisbericht-gliederung.md`` (Firmen-Repo), Teile 0 bis 9.
Der Formatpilot (T-1414) setzt die Teile 0, 1, 4 (nur #95), 7 und 8 um, Teil 2 kommt aus der
Konformitäts-Checkliste (T-1416, ``konformitaet.py``), Teil 3 aus den Klimakennwerten des
Sammlers (T-1417, ``klima.py``), Teil 6 aus den Maßnahmenzeilen (T-1419, ``massnahmen.py``),
Teil 9 aus den Anlagen des Sammlers und der Namensregel der Downloads (T-1420). Jeder Teil ist eine
Funktion ``(Berichtsdaten) -> str``; ``TEILE`` ordnet die Nummern zu.

Harte Regeln der Gliederung, die hier schon gelten: kein Euro-Feld mit Null oder leer (wo kein
Betrag steht, steht der Grund), jede Summe nennt ihren Nenner („x von y Klimawirkungen in Euro
beziffert“), jeder Teil trägt seinen Stand, kein Pfad aus dem Produkt-Repo im Text.

Auszeichnung, an der ``test_ergebnisbericht_regeln.py`` die Regeln prüft (T-1415):

- jeder Euro-Betrag steht in ``<span class="betrag">`` mit den Attributen ``data-berichtsstand``,
  ``data-methodikstand`` und ``data-datenstand`` (``_betrag``); ein Betrag, der gerundet 0 € zeigt,
  bricht die Erzeugung ab, statt still eine Null zu drucken;
- jedes Element ``.summe`` enthält ``<span class="nenner">x von y Klimawirkungen in Euro
  beziffert</span>`` (``_nenner``);
- jeder Teil endet mit der Standzeile ``<p class="stand">`` (``_stand``).
"""

from __future__ import annotations

import math
import os
from html import escape
from typing import Callable

from app.services.ergebnisbericht.beispiel import MORB, MORT
from app.services.ergebnisbericht.klima import (
    JAHR_START, JAHRE_PROJEKTION, SZENARIEN, Klimazahl,
)
from app.services.ergebnisbericht.konformitaet import (
    STATUS, fundstelle_ohne_datei, kundensatz, lies_checkliste, umschreibe,
)
from app.services.ergebnisbericht.massnahmen import (
    HORIZONT_ENDE, QUALITATIV, blockname, rangfolge,
)
from app.services.ergebnisbericht.raum import UEBRIG
from app.services.ergebnisbericht.sammler import (
    DATENSTAENDE, VERWEIS_METHODIK, Berichtsdaten, anlage_kennung,
)
from app.services.download_namen import download_dateiname
from app.services.kurzfassung_markdown import _de_euro

UEBERSCHRIFTEN = {
    0: "Teil 0 · Kopf und Identität",
    1: "Teil 1 · Beschlussfähige Zusammenfassung",
    2: "Teil 2 · Rechtlicher und methodischer Rahmen",
    3: "Teil 3 · Klimatische Ausgangslage",
    4: "Teil 4 · Betroffenheitsanalyse je Klimawirkung",
    5: "Teil 5 · Raumergebnis",
    6: "Teil 6 · Maßnahmen",
    7: "Teil 7 · Parameter- und Quellenverzeichnis",
    8: "Teil 8 · Grenzen und Vollständigkeitsanzeige",
    9: "Teil 9 · Anhang",
}

SCREENING_SATZ = "Screening-Analyse, kein Ersatz für ein Detailgutachten."

# Bezeichnungen wie in der Parameterliste des Produkts (frontend/src/utils/evidenceLabel.ts);
# für Abschätzungen der Wortlaut der Gliederung (Teil 7: „ausgewiesene Abschätzung“).
_KLASSE = {
    "belegt": "belegt",
    "berechnet": "berechnet aus anderen Parametern",
    "abgeschaetzt": "ausgewiesene Abschätzung von KAP3",
}


def de_zahl(wert: float, stellen: int = 0) -> str:
    """Deutsche Zahlschreibweise (Tausenderpunkt, Dezimalkomma)."""
    return f"{wert:,.{stellen}f}".replace(",", "⁣").replace(".", ",").replace("⁣", ".")


def de_euro(wert: float) -> str:
    """Betrag in der Schreibweise des Produkts (ganze Euro, Tausenderpunkt, „€“)."""
    return _de_euro(wert)


def _h(text: object) -> str:
    return escape(str(text))


def _kopf(nr: int) -> str:
    return f'<h1 id="teil-{nr}">{_h(UEBERSCHRIFTEN[nr])}</h1>\n'


def _stand(d: Berichtsdaten) -> str:
    return f'<p class="stand">{_h(d.stand.zeile())}</p>\n'


def _betrag(d: Berichtsdaten, wert: float) -> str:
    """Euro-Betrag als ``<span class="betrag">`` mit Berichts-, Methodik- und Datenstand.

    Harte Regel 1: Eine Null im Euro-Feld ist verboten. Zeigt der Betrag gerundet 0 € (oder ist er
    nicht positiv), bricht die Erzeugung ab — der Teil muss dann statt des Betrags den Grund nennen.
    """
    gueltig = isinstance(wert, (int, float)) and math.isfinite(wert) and wert > 0
    text = de_euro(wert) if gueltig else ""
    if not gueltig or text.startswith("0 "):
        raise ValueError(f"Euro-Betrag {wert!r} ergäbe eine Null oder ein leeres Feld im Bericht; "
                         f"harte Regel 1 verbietet das — hier gehört der Grund hin")
    s = d.stand
    berichtsstand = f"{s.bericht} vom {s.erstellt:%d.%m.%Y}"
    methodikstand = f"{s.methodik} (Modellstand {s.modell})"
    return (f'<span class="betrag" data-berichtsstand="{_h(berichtsstand)}"'
            f' data-methodikstand="{_h(methodikstand)}"'
            f' data-datenstand="{_h(s.daten)}">{_h(text)}</span>')


def mit_anlage(text: str) -> str:
    """Verweis auf einen Methodik-Bericht mit seiner Anlage aus Teil 9 (harte Regel 4, T-1420):
    „Bericht #95 §3.5“ → „Anlage M95, Methodik-Bericht #95 §3.5“. Reiner Text, noch unmaskiert."""
    return VERWEIS_METHODIK.sub(
        lambda m: f"Anlage {anlage_kennung(m.group(1))}, Methodik-Bericht #{m.group(1)}", text)


def _nenner(d: Berichtsdaten) -> str:
    """Nenner einer Summe (harte Regel 2): „x von y Klimawirkungen in Euro beziffert“."""
    return f'<span class="nenner">{_h(d.beziffert_text)}</span>'


def _preisstand(d: Berichtsdaten, betrag: float) -> str:
    return f"{_betrag(d, betrag)} je Jahr (Preisstand 2024)"


# ── Teil 0 ──────────────────────────────────────────────────────────────────────

def teil_0(d: Berichtsdaten) -> str:
    k, e, s = d.kommune, d.ergebnis95, d.stand
    zeilen = [
        ("Kommune", f"{k.name} ({k.kreis}, {k.bundesland})"),
        ("Amtlicher Gemeindeschlüssel", k.ags),
        ("Gebietsstand", "Gemeindegrenze nach VG250 (BKG), Gebietsstand 01.01. der aktuellen Ausgabe"),
        ("Einwohner (Zensus 2022)", f"{de_zahl(e.einwohner)}, davon {de_zahl(e.einwohner_ab65)} ab 65 Jahren"),
        ("Berichtsversion", s.bericht),
        ("Methodikversion", f"{s.methodik} (Modellstand {s.modell})"
                            + "".join(mit_anlage(f"; Methodik-Bericht #{a.nr} (Teil 9)")
                                      for a in getattr(d, "anlagen", []))),
        ("Erstellt am", f"{s.erstellt:%d.%m.%Y}"),
    ]
    html = [_kopf(0), '<table class="kopf">']
    html += [f"<tr><th>{_h(a)}</th><td>{_h(b)}</td></tr>" for a, b in zeilen]
    html.append("</table>")
    html.append("<h2>Datenstände je Quelle</h2>")
    html.append('<table class="kopf">')
    html += [f"<tr><th>{_h(a)}</th><td>{_h(b)}</td></tr>" for a, b in DATENSTAENDE]
    html.append("</table>")
    html.append(f'<p class="hinweis">{_h(SCREENING_SATZ)}</p>')
    html.append(_stand(d))
    return "\n".join(html)


# ── Teil 1 ──────────────────────────────────────────────────────────────────────

def teil_1(d: Berichtsdaten) -> str:
    k, e = d.kommune, d.ergebnis95
    summe = sum(w["betrag_eur"] for w in d.klimawirkungen_im_bericht)
    band = e.band_eur
    band_satz = (f" Band {_betrag(d, band[0])} bis {_betrag(d, band[1])}, abgeleitet aus der "
                 f"Bandbreite des Kostensatzes je verlorenem Lebensjahr." if band else "")
    # Kernsätze als HTML: Beträge tragen ihre Auszeichnung, alles Übrige ist maskiert.
    kernsaetze = [
        f"Die in Euro bezifferten Klimaschäden in {_h(k.name)} betragen mindestens "
        f"{_preisstand(d, summe)}; {_nenner(d)}.{band_satz}",
        _h(f"Größte bezifferte Klimawirkung ist die Hitzebelastung: rechnerisch "
           f"{de_zahl(e.todesfaelle, 2)} hitzebedingte Todesfälle und {de_zahl(e.einweisungen, 2)} "
           f"Krankenhauseinweisungen im Jahr."),
        _h(f"Von den {de_zahl(e.einwohner)} Einwohnern sind {de_zahl(e.einwohner_ab65)} 65 Jahre "
           f"oder älter; auf sie entfällt der größte Teil der Hitzesterblichkeit."),
        _h("Der Betrag ist eine Untergrenze: Klimawirkungen ohne Euro-Bezifferung gehen nicht in "
           "die Summe ein (Teil 8)."),
        _h("Unsicherheit: Der Betrag hängt linear am Kostensatz je verlorenem Lebensjahr; die "
           "Modellgrenzen stehen mit Zahl in Teil 8."),
    ]
    html = [_kopf(1), "<h2>Kernsätze</h2>", "<ol>"]
    html += [f"<li>{s}</li>" for s in kernsaetze]
    html.append("</ol>")
    html.append("<h2>Höchste Risiken</h2>")
    html.append('<table><tr><th>Klimawirkung (KWRA)</th><th>Handlungsfeld</th>'
                '<th class="zahl">Betrag je Jahr</th></tr>')
    for w in sorted(d.klimawirkungen_im_bericht, key=lambda w: -w["betrag_eur"]):
        html.append(f"<tr><td>#{w['kwra_id']} {_h(w['kwra_name'])}</td><td>{_h(w['kwra_field'])}</td>"
                    f'<td class="zahl">{_betrag(d, w["betrag_eur"])}</td></tr>')
    html.append(f'<tr class="summe"><td colspan="2">Summe ({_nenner(d)})</td>'
                f'<td class="zahl">{_betrag(d, summe)}</td></tr>')
    html.append("</table>")
    html.append("<h2>Wirtschaftlichste Maßnahmen</h2>")
    html.append("<p>In dieser Fassung des Berichts ist keine Maßnahme bewertet: Die Maßnahmen "
                "mit Kosten und vermiedenem Schaden folgen mit Teil 6. Deshalb steht hier noch "
                "keine Rangfolge.</p>")
    html.append(_stand(d))
    return "\n".join(html)


# ── Teil 2 ──────────────────────────────────────────────────────────────────────

def teil_2(d: Berichtsdaten, checkliste: str | os.PathLike | None = None) -> str:
    """Rechtlicher und methodischer Rahmen, erzeugt aus der Konformitäts-Checkliste (T-1416).

    Je Anforderungszeile der Checkliste eine Tabellenzeile ``tr.anforderung[data-nr]`` mit Status
    (``td.status``) und Kundensatz (``td.luecke``, bei „erfüllt“ ein Strich; bei „teilweise“ und
    „offen“ der Kundensatz aus ``konformitaet_kundentext.py`` statt der internen Spalte „Lücke“,
    T-1530). ``checkliste`` ist für den Test: eine Kopie mit geändertem Status ändert die Ausgabe
    dieser Zeile.
    """
    zeilen = lies_checkliste(checkliste)
    zaehlung = {s: sum(1 for z in zeilen if z.status == s) for s in STATUS}
    html = [_kopf(2)]
    html.append(
        f"<p>Diese Tabelle stellt {len(zeilen)} Anforderungen aus dem Klimaanpassungsgesetz (KAnG), "
        f"der Klimawirkungs- und Risikoanalyse 2021 für Deutschland (KWRA 2021), der ISO 14091 "
        f"und der Methodenkonvention 4.0 des Umweltbundesamts dem Stand des Produkts gegenüber: "
        f"{zaehlung['erfüllt']} erfüllt, {zaehlung['teilweise']} teilweise, "
        f"{zaehlung['offen']} offen. Wo eine Anforderung nicht voll erfüllt ist, nennt die "
        f"Spalte „Lücke“, was fehlt.</p>")
    html.append(
        f"<p>Die KWRA 2021 bewertet 102 Klimawirkungen. Dieser Bericht erfasst die Klimawirkungen "
        f"des Produktkatalogs ({_h(d.beziffert_text)}).</p>")
    html.append('<table class="konformitaet"><tr><th>Nr</th><th>Anforderung</th><th>Quelle</th>'
                '<th>Fundstelle</th><th>Status</th><th>Lücke</th></tr>')
    for z in zeilen:
        luecke = kundensatz(z.nr, z.status) if z.status != "erfüllt" else "—"
        html.append(
            f'<tr class="anforderung" data-nr="{z.nr}"><td>{z.nr}</td>'
            f"<td>{_h(umschreibe(z.anforderung))}</td><td>{_h(z.quelle)}</td>"
            f"<td>{_h(fundstelle_ohne_datei(z.fundstelle))}</td>"
            f'<td class="status">{_h(z.status)}</td><td class="luecke">{_h(luecke)}</td></tr>')
    html.append("</table>")
    html.append(_stand(d))
    return "\n".join(html)


# ── Teil 3 ──────────────────────────────────────────────────────────────────────

class _Fussnoten:
    """Quelle und Datenstand je Zahl als Fußnote; gleiche Paare teilen sich eine Nummer."""

    def __init__(self) -> None:
        self.paare: list[tuple[str, str]] = []

    def nummer(self, z: Klimazahl) -> int:
        paar = (z.quelle, z.datenstand)
        if paar not in self.paare:
            self.paare.append(paar)
        return self.paare.index(paar) + 1

    def zahl(self, z: Klimazahl, stellen: int = 1) -> str:
        """Zahl als ``span.klimazahl`` mit ``data-quelle`` und ``data-datenstand`` und Fußnote;
        ohne Wert steht der Grund (``span.grund``)."""
        if z.wert is None:
            return f'<span class="grund">{_h(z.grund)}</span>'
        return (f'<span class="klimazahl" data-quelle="{_h(z.quelle)}"'
                f' data-datenstand="{_h(z.datenstand)}">{_h(de_zahl(z.wert, stellen))}'
                f'<sup class="fn">{self.nummer(z)}</sup></span>')

    def html(self) -> str:
        zeilen = [f'<li class="fussnote" data-nr="{i}">Quelle: {_h(q)}. Datenstand: {_h(s)}.</li>'
                  for i, (q, s) in enumerate(self.paare, 1)]
        return '<ol class="fussnoten">' + "".join(zeilen) + "</ol>"


def teil_3(d: Berichtsdaten) -> str:
    """Klimatische Ausgangslage (T-1417): je in Euro bezifferter Klimawirkung eine Zeile
    ``tr.klimawirkung[data-kwra]`` mit Beobachtung (``td.beobachtung``) und Projektion
    (``td.rcp45``, ``td.rcp85``). Jede Zahl trägt Quelle und Datenstand als Attribut und Fußnote."""
    k = d.kommune
    fn = _Fussnoten()
    html = [_kopf(3)]
    html.append(
        f"<p>Die Tabelle zeigt je Klimawirkung, die dieser Bericht in Euro beziffert, den "
        f"Klimakennwert, der ihren Betrag treibt: gemessen in {_h(k.name)} (Deutscher "
        f"Wetterdienst, Climate Data Center) und projiziert bis 2065 unter zwei Szenarien. "
        f"RCP 4.5 steht für moderaten Klimaschutz, RCP 8.5 für eine Entwicklung weiter wie "
        f"bisher.</p>")
    kopf = "".join(f'<th class="zahl">{_h(SZENARIEN[sz])} {j}</th>'
                   for sz in SZENARIEN for j in JAHRE_PROJEKTION)
    html.append('<table class="klima"><tr><th>Klimawirkung (KWRA)</th><th>Kennwert</th>'
                f'<th class="zahl">Beobachtung {_h(k.name)}, 2016–2025</th>{kopf}</tr>')
    for z in d.klima:
        zellen = "".join(f'<td class="zahl {sz}" data-jahr="{j}">{fn.zahl(z.projektion[sz][j])}</td>'
                         for sz in SZENARIEN for j in JAHRE_PROJEKTION)
        html.append(
            f'<tr class="klimawirkung" data-kwra="{z.kwra_id}"><td>#{z.kwra_id} {_h(z.kwra_name)}</td>'
            f"<td>{_h(z.kennwert)}</td>"
            f'<td class="zahl beobachtung">{fn.zahl(z.beobachtung)}</td>{zellen}</tr>')
    html.append("</table>")
    for z in d.klima:
        if z.beobachtung.wert is None:
            continue
        land = k.bundesland
        anstieg = {sz: Klimazahl(z.projektion[sz][JAHRE_PROJEKTION[-1]].wert - z.start[sz].wert,
                                 z.start[sz].quelle, z.start[sz].datenstand)
                   for sz in SZENARIEN}
        html.append(
            f"<p>#{z.kwra_id} {_h(z.kwra_name)}: Die Projektion ist eine Reihe für {_h(land)}, "
            f"nicht für {_h(k.name)}. Sie beginnt {JAHR_START} bei "
            f"{fn.zahl(z.start['rcp45'])} {_h(z.einheit)} und steigt bis {JAHRE_PROJEKTION[-1]} "
            f"unter RCP 4.5 um {fn.zahl(anstieg['rcp45'])}, unter RCP 8.5 um "
            f"{fn.zahl(anstieg['rcp85'])} {_h(z.einheit)}. Gemessen hat der Deutsche Wetterdienst "
            f"in {_h(k.name)} {fn.zahl(z.beobachtung)} {_h(z.einheit)} im Mittel der Jahre "
            f"2016–2025. Übertragbar auf die Kommune ist der Anstieg, nicht der absolute Wert der "
            f"Landesreihe: Wer die Landeswerte direkt mit der Messung vergleicht, liest den "
            f"Unterschied zwischen Kommune und Land fälschlich als Klimawandel.</p>")
    html.append("<p>Der Euro-Betrag in Teil 4 rechnet mit dem beobachteten Klima 2016–2025; die "
                "Projektion zeigt, in welche Richtung sich die Belastung verschiebt, und geht "
                "nicht in den Betrag ein (Teil 8). Einen Kartenausschnitt enthält diese Fassung "
                "nicht.</p>")
    html.append(fn.html())
    html.append(_stand(d))
    return "\n".join(html)


# ── Teil 4 ──────────────────────────────────────────────────────────────────────

def _parameter_quelle(d: Berichtsdaten, param_id: str) -> str:
    """Kennzeichnung eines Parameters wie in Teil 7 (Quelle oder ausgewiesene Abschätzung von KAP3),
    aus denselben Parameterdaten (``d.parameter``, ``_herkunft``), nicht als fester Text (Vorgabe P1).

    Eine unbekannte Kennung liefert keine leere Quellenzelle: Ein Bericht mit leerem Feld wird nicht
    erzeugt (P1, Entscheidung des CEO, 27.09.2026), deshalb bricht die Erzeugung mit ``ValueError``
    ab und nennt die Kennung.
    """
    for p in d.parameter:
        if p.get("id") == param_id:
            return _herkunft(p)
    raise ValueError(f"Parameter {param_id!r} ist in d.parameter nicht enthalten")


def teil_4(d: Berichtsdaten) -> str:
    k, e = d.kommune, d.ergebnis95
    html = [_kopf(4)]
    html.append(f"<h2>#95 Hitzebelastung</h2>")
    html.append("<p>Handlungsfeld Menschliche Gesundheit · Klasse A (in Euro beziffert) · "
                "bewerteter Schaden im Konto K1 Gesundheit.</p>")
    html.append("<h3>Rechenkette</h3>")
    html.append('<table><tr><th>Ebene</th><th class="zahl">Wert</th><th>Quelle</th></tr>')
    kette = [
        ("Einwohner", de_zahl(e.einwohner), "Zensus 2022, 100-m-Zellen"),
        ("davon ab 65 Jahren", de_zahl(e.einwohner_ab65), "Zensus 2022, Altersgruppen"),
        ("Bewohnte Zellen", de_zahl(e.zellen), "Zensus 2022, Gitter 100 m"),
        ("Sommermittel (einwohnergewichtet)", f"{de_zahl(e.t_sommer_mittel, 1)} °C",
         "DWD, Raster 1 km, 2016–2025"),
        ("Hitzetage je Jahr (einwohnergewichtet)", de_zahl(e.hitzetage_mittel, 1),
         "DWD, Raster 1 km, 2016–2025"),
        ("Hitzebedingte Todesfälle je Jahr", de_zahl(e.todesfaelle, 2),
         "Expositions-Wirkungs-Kurve des RKI, vier Altersbänder"),
        ("Verlorene Lebensjahre je Jahr", de_zahl(e.yll, 2), "Todesfälle × Restlebenserwartung "
         "(Destatis-Sterbetafeln)"),
        ("× Kostensatz je Lebensjahr", _betrag(d, e.voly_eur),
         _parameter_quelle(d, f"risks.{MORT}.cost_per_outcome")),
        ("= Betrag Sterblichkeit", _betrag(d, e.betrag_mortalitaet_eur), "Rechnung"),
        ("Hitzebedingte Krankenhauseinweisungen je Jahr", de_zahl(e.einweisungen, 2),
         "Destatis, Karlsson und Ziebarth 2018"),
        ("× Kostensatz je Fall", _betrag(d, e.c_fall_eur),
         _parameter_quelle(d, f"risks.{MORB}.cost_per_outcome")),
        ("= Betrag Erkrankungen", _betrag(d, e.betrag_morbiditaet_eur), "Rechnung"),
    ]
    # Beträge kommen aus _betrag (schon ausgezeichnet und maskiert); alle übrigen Werte werden maskiert.
    html += [f'<tr><td>{_h(a)}</td><td class="zahl">'
             f'{b if b.startswith("<span class=") else _h(b)}</td><td>{_h(c)}</td></tr>'
             for a, b, c in kette]
    html.append(f'<tr class="summe"><td>Jahresbetrag #95</td><td class="zahl">'
                f'{_betrag(d, e.jahresbetrag_eur)}</td><td>Summe beider Beträge der '
                f'Hitzebelastung; im Bericht {_nenner(d)}</td></tr>')
    html.append("</table>")
    html.append(f"<p>Jahresbetrag der Hitzebelastung in {_h(k.name)}: "
                f"<strong>{_preisstand(d, e.jahresbetrag_eur)}</strong>. "
                f"Der Betrag gilt für die ganze Kommune; die Aufteilung nach Ortsteilen steht in "
                f"<a href=\"#teil-5\">Teil 5</a>.</p>")
    html.append(_stand(d))
    return "\n".join(html)


# ── Teil 5 ──────────────────────────────────────────────────────────────────────

GRUND_OHNE_ORTSTEILE = "Die Quelle führt für diese Kommune keine Ortsteilgrenzen."


def _anzeigename(z, gibt_ortsteile: bool) -> str:
    """Die Zeile ohne Ortsteilfläche heißt „übriges Gemeindegebiet“, sobald es Ortsteile gibt
    (eine Zeile mit dem Namen der Kommune läse sich neben ihnen wie eine Summe)."""
    if z.art == "gemeinde" and gibt_ortsteile:
        return UEBRIG
    return z.name


def teil_5(d: Berichtsdaten) -> str:
    """Raumergebnis (T-1565): #95 je Ortsteil, absolut und je 1.000 Einwohner. Eine Zeile ohne
    bewohnte Zelle nennt den Grund statt eines Betrags; die Summenzeile trägt den Nenner."""
    k = d.kommune
    zeilen = list(d.raum)
    gibt_ortsteile = any(z.art == "ortsteil" for z in zeilen)
    html = [_kopf(5)]
    if gibt_ortsteile:
        html.append(
            f"<p>Die Tabelle teilt die Hitzebelastung (#95) von {_h(k.name)} nach Ortsteilen auf: "
            f"jede bewohnte 100-m-Zelle des Zensus zählt zu dem Ortsteil, in dem ihre Mitte liegt. "
            f"Neben den absoluten Werten stehen die Raten je 1.000 Einwohner, weil sie Ortsteile "
            f"unterschiedlicher Größe vergleichbar machen. Die Zwischengrößen (Einwohner, davon ab "
            f"65 Jahren, Hitzetage je Jahr) stehen als eigene Spalten.</p>")
    else:
        html.append(
            f"<p>Die Quelle führt für {_h(k.name)} keine Ortsteilgrenzen. Deshalb steht hier genau "
            f"eine Zeile für die ganze Kommune; eine Aufteilung nach Ortsteilen ist für diese "
            f"Kommune nicht möglich.</p>")
    zahl = 'class="zahl"'
    html.append(
        '<table class="raum"><tr><th>Ortsteil</th><th class="zahl">Einwohner</th>'
        '<th class="zahl">davon ab 65 Jahren</th><th class="zahl">Hitzetage je Jahr</th>'
        '<th class="zahl">Todesfälle je Jahr</th><th class="zahl">Todesfälle je 1.000 Einwohner</th>'
        '<th class="zahl">Einweisungen je Jahr</th><th class="zahl">Einweisungen je 1.000 Einwohner</th>'
        '<th class="zahl">Jahresbetrag</th><th class="zahl">Jahresbetrag je 1.000 Einwohner</th></tr>')
    for z in zeilen:
        name = _anzeigename(z, gibt_ortsteile)
        if z.jahresbetrag_eur is None or z.grund:
            grund = _h(z.grund or "Für diese Zeile liegt kein Betrag vor.")
            html.append(
                f'<tr class="raumzeile" data-art="{_h(z.art)}"><td>{_h(name)}</td>'
                f'<td {zahl}>{_h(de_zahl(z.einwohner))}</td>'
                f'<td {zahl}>{_h(de_zahl(z.einwohner_ab65))}</td>'
                f'<td colspan="7" class="grund">{grund}</td></tr>')
            continue
        html.append(
            f'<tr class="raumzeile" data-art="{_h(z.art)}"><td>{_h(name)}</td>'
            f'<td {zahl}>{_h(de_zahl(z.einwohner))}</td>'
            f'<td {zahl}>{_h(de_zahl(z.einwohner_ab65))}</td>'
            f'<td {zahl}>{_h(de_zahl(z.hitzetage, 1))}</td>'
            f'<td {zahl}>{_h(de_zahl(z.todesfaelle, 2))}</td>'
            f'<td {zahl}>{_h(de_zahl(z.todesfaelle_je_1000, 2))}</td>'
            f'<td {zahl}>{_h(de_zahl(z.einweisungen, 2))}</td>'
            f'<td {zahl}>{_h(de_zahl(z.einweisungen_je_1000, 2))}</td>'
            f'<td {zahl}>{_betrag(d, z.jahresbetrag_eur)}</td>'
            f'<td {zahl}>{_betrag(d, z.jahresbetrag_je_1000_eur)}</td></tr>')
    bezifferte = [z for z in zeilen if z.jahresbetrag_eur is not None and not z.grund]
    if bezifferte:
        ew = sum(z.einwohner for z in zeilen)
        ab65 = sum(z.einwohner_ab65 for z in zeilen)
        tote = sum(z.todesfaelle for z in bezifferte)
        einw = sum(z.einweisungen for z in bezifferte)
        summe = sum(z.jahresbetrag_eur for z in bezifferte)
        html.append(
            f'<tr class="summe"><td>Summe {_nenner(d)}</td><td {zahl}>{_h(de_zahl(ew))}</td>'
            f'<td {zahl}>{_h(de_zahl(ab65))}</td><td {zahl}>—</td>'
            f'<td {zahl}>{_h(de_zahl(tote, 2))}</td><td {zahl}>{_h(de_zahl(tote / ew * 1000, 2))}</td>'
            f'<td {zahl}>{_h(de_zahl(einw, 2))}</td><td {zahl}>{_h(de_zahl(einw / ew * 1000, 2))}</td>'
            f'<td {zahl}>{_betrag(d, summe)}</td><td {zahl}>{_betrag(d, summe / ew * 1000)}</td></tr>')
    html.append("</table>")
    if gibt_ortsteile:
        uebrig = [z for z in zeilen if _anzeigename(z, True) == UEBRIG]
        if uebrig:
            rest = (f"In der Zeile „{_h(UEBRIG)}“ stehen {_h(de_zahl(sum(z.einwohner for z in uebrig)))} "
                    f"Einwohner, deren Zelle in keiner Ortsteilfläche liegt; sie gehören zu keinem "
                    f"Ortsteil und sind vom Ortsteilvergleich nicht abgedeckt.")
        else:
            rest = "Alle bewohnten Zellen liegen in einer Ortsteilfläche."
        html.append(
            "<p>Was die Unterschiede zwischen den Ortsteilen treibt, sind zwei Größen: der Anteil "
            "der Einwohner ab 65 Jahren, weil die Hitzesterblichkeit mit dem Alter steigt, und die "
            "Zahl der Hitzetage je Zelle, weil sie die Belastung der Zelle bestimmt; je höher "
            "beides, desto höher die Rate je 1.000 Einwohner. Raten kleiner Ortsteile beruhen auf "
            f"wenigen Menschen und schwanken deshalb stärker. {rest}</p>")
    html.append(
        "<p>Die Ortsteilgrenzen stammen aus OpenStreetMap (Overpass API, Lizenz ODbL 1.0), Stand der "
        "Daten 27.09.2026, abgerufen am 27.09.2026. © OpenStreetMap-Mitwirkende. Eine Karte "
        "enthält diese Fassung nicht.</p>")
    html.append(_stand(d))
    return "\n".join(html)


# ── Teil 6 ──────────────────────────────────────────────────────────────────────

def _euro_oder(d: Berichtsdaten, wert: float, sonst: str) -> str:
    """Betrag als ``span.betrag``; zeigt er gerundet keinen ganzen Euro, steht ``sonst`` als Text
    (harte Regel 1: keine Null im Euro-Feld)."""
    if isinstance(wert, (int, float)) and math.isfinite(wert) and round(wert) >= 1:
        return _betrag(d, wert)
    return f'<span class="grund">{_h(sonst)}</span>'


def _zeilen_html(zeilen: list[str]) -> str:
    """Mehrzeiliger Zellentext (wie im Maßnahmen-Excel) als ``div.zeile`` je Zeile."""
    return "".join(f'<div class="zeile">{_h(z)}</div>' for z in zeilen)


def _verhaeltnis(v: float | None) -> str:
    if v is None:
        return "Kosten offen"
    return "ohne Kosten" if math.isinf(v) else de_zahl(v, 1)


def teil_6(d: Berichtsdaten) -> str:
    """Maßnahmen (T-1419): je Maßnahme ein Block ``div.massnahme[data-code][data-rang]``, geordnet
    nach ``massnahmen.rangfolge``. Kennzahlen stehen in ``td.capex``, ``td.opex``,
    ``td.vermieden``, ``td.verhaeltnis``, ``td.gewissheit``, ``td.umsetzung`` und ``td.ort``; die
    Kostenkomponenten in ``tr.komponente`` mit ``td.quelle``. Eine qualitative Maßnahme trägt
    ``data-qualitativ`` und ``span.qualitativ`` statt eines Betrags für ihre Wirkung."""
    k = d.kommune
    zeilen = rangfolge(list(d.massnahmen))
    html = [_kopf(6)]
    if not zeilen:
        html.append(f"<p>Für {_h(k.name)} ist in dieser Fassung des Berichts keine Maßnahme "
                    f"angelegt. Deshalb steht hier keine Rangfolge; Kosten und vermiedene Schäden "
                    f"folgen, sobald Maßnahmen verortet sind.</p>")
        html.append(_stand(d))
        return "\n".join(html)
    n_q = sum(1 for z in zeilen if z.qualitativ)
    n_offen = sum(1 for z in zeilen if not z.qualitativ and z.nutzen_kosten is None)
    html.append(
        f"<p>Die Maßnahmen stehen in der Reihenfolge ihres Nutzen-Kosten-Verhältnisses, das "
        f"wirtschaftlichste zuerst. Das Verhältnis teilt den Nutzen über den Zeitraum vom "
        f"Umsetzungsjahr bis {HORIZONT_ENDE} (vermiedene Schäden und Zusatznutzen je Jahr mal "
        f"Jahre) durch die Kosten im selben Zeitraum (CAPEX einmal, OPEX je Jahr mal Jahre); "
        f"ein Verhältnis über 1 heißt, die Maßnahme spart mehr Schaden, als sie kostet. Beträge "
        f"sind nicht abgezinst, die Wirkung gilt als gleichbleibend. Jede Kostenkomponente nennt "
        f"ihre Quelle. Gewissheit und Umsetzung stehen wie in der Maßnahmentabelle des Produkts."
        + (f" {n_offen} Maßnahme(n) zeigen „Kosten offen“: Ihre Kosten sind noch nicht "
           f"bestimmt, deshalb steht für sie kein Verhältnis; sie stehen zwischen den "
           f"bezifferten und den qualitativen Maßnahmen." if n_offen else "")
        + (f" {n_q} Maßnahme(n) sind qualitativ bewertet: Für sie liegt keine Wirkung in Euro "
           f"vor; sie stehen am Ende, ohne Rang nach Euro." if n_q else "")
        + "</p>")
    for rang, z in enumerate(zeilen, 1):
        attr = f' data-code="{_h(z.code)}" data-rang="{rang}"'
        if z.qualitativ:
            attr += ' data-qualitativ="ja"'
        html.append(f'<div class="massnahme"{attr}>')
        html.append(f"<h2>{rang}. {_h(z.name)}</h2>")
        html.append('<table class="massnahme-kennzahlen">')
        ort = z.ort + (f" (abgedeckte Fläche {de_zahl(z.flaeche_m2)} m²)"
                       if z.flaeche_m2 and z.flaeche_m2 >= 1 else "")
        html.append(f'<tr><th>Ort</th><td class="ort">{_h(ort)}</td></tr>')
        html.append(f"<tr><th>Umsetzungsjahr</th><td>{z.umsetzungsjahr}</td></tr>")
        if z.kosten_offen:
            capex = ("–" + (f' <span class="grund">{_h(z.kosten_vermerk)}</span>'
                            if z.kosten_vermerk else ""))
        else:
            capex = _euro_oder(d, z.capex_eur, "keine Investition im Katalog hinterlegt")
        html.append(f'<tr><th>CAPEX (einmalig)</th><td class="capex">{capex}</td></tr>')
        html.append(f'<tr><th>OPEX je Jahr</th><td class="opex">'
                    f'{_euro_oder(d, z.opex_eur, "keine Betriebskosten im Katalog hinterlegt")}</td></tr>')
        if z.qualitativ:
            html.append(f'<tr><th>Vermiedene Schäden je Jahr</th><td class="vermieden">'
                        f'<span class="qualitativ">{QUALITATIV}</span>: {_h(z.vermerk)}</td></tr>')
            html.append('<tr><th>Nutzen-Kosten-Verhältnis</th><td class="verhaeltnis">keines, '
                        'weil die Wirkung nicht in Euro beziffert ist</td></tr>')
        else:
            vermieden = (_betrag(d, z.vermiedene_schaeden_eur) if z.vermiedene_schaeden_eur
                         and round(z.vermiedene_schaeden_eur) >= 1 else
                         '<span class="grund">keine vermiedenen Schäden in Euro beziffert</span>')
            html.append(f'<tr><th>Vermiedene Schäden je Jahr</th><td class="vermieden">'
                        f'{vermieden}</td></tr>')
            if z.zusatznutzen_eur and round(z.zusatznutzen_eur) >= 1:
                html.append(f'<tr><th>Zusätzlicher Nutzen je Jahr</th><td class="zusatz">'
                            f'{_betrag(d, z.zusatznutzen_eur)}</td></tr>')
            html.append(f'<tr><th>Nutzen-Kosten-Verhältnis ({z.umsetzungsjahr}–{HORIZONT_ENDE})'
                        f'</th><td class="verhaeltnis">{_h(_verhaeltnis(z.nutzen_kosten))}'
                        + (f': {_h(z.kosten_vermerk)}' if z.kosten_offen and z.kosten_vermerk else "")
                        + '</td></tr>')
        html.append(f'<tr><th>Gewissheit</th><td class="gewissheit">'
                    f'{_zeilen_html(z.gewissheit.split(chr(10)))}</td></tr>')
        html.append(f'<tr><th>Umsetzung</th><td class="umsetzung">'
                    f'{_zeilen_html(z.umsetzung.split(chr(10)))}</td></tr>')
        html.append("</table>")
        if z.extra.get("stadtbaum_s_unbek_hinweis"):
            html.append(f'<p class="hinweis">{_h(z.extra["stadtbaum_s_unbek_hinweis"])}</p>')
        if z.komponenten:
            html.append('<table class="kostenkomponenten"><tr><th>Kostenart</th><th>Komponente</th>'
                        '<th class="zahl">Einzelpreis</th><th class="zahl">Menge</th>'
                        '<th class="zahl">Betrag</th><th>Quelle</th></tr>')
            for c in z.komponenten:
                menge = f"{de_zahl(c.menge, 0 if float(c.menge).is_integer() else 2)} {c.mengeneinheit}"
                html.append(
                    f'<tr class="komponente" data-block="{_h(c.block)}"><td>{_h(blockname(c.block))}</td>'
                    f"<td>{_h(c.bezeichnung)}</td>"
                    f'<td class="zahl">{_euro_oder(d, c.einzelpreis_eur, "ohne Kosten")}</td>'
                    f'<td class="zahl">{_h(menge.strip())}</td>'
                    f'<td class="zahl">{_euro_oder(d, c.betrag_eur, "ohne Kosten")}</td>'
                    f'<td class="quelle">{_h(c.quelle)}</td></tr>')
            html.append("</table>")
        html.append("</div>")
    html.append(_stand(d))
    return "\n".join(html)


# ── Teil 7 ──────────────────────────────────────────────────────────────────────

def _wert(p: dict) -> str:
    v = p.get("value")
    if isinstance(v, bool) or v is None:
        return "—"
    if isinstance(v, (int, float)):
        v = float(v)
        if v.is_integer():
            return de_zahl(v, 0)
        # höchstens vier gültige Stellen, ohne angehängte Nullen (0,0065 bleibt 0,0065)
        stellen = max(0, 3 - math.floor(math.log10(abs(v))))
        text = de_zahl(round(v, stellen), stellen)
        return text.rstrip("0").rstrip(",") if "," in text else text
    return "Tabelle (13 Sommerwochen je Region)"


def _herkunft(p: dict) -> str:
    klasse = p.get("evidence_class") or "belegt"
    quelle = p.get("source") or ""
    if klasse == "abgeschaetzt":
        herleitung = (p.get("evidence_derivation") or {}).get("wert") or p.get("evidence_note") or quelle
        return mit_anlage(f"{_KLASSE[klasse]}: {herleitung}")
    return mit_anlage(f"{_KLASSE.get(klasse, 'belegt')}: {quelle}")


def teil_7(d: Berichtsdaten) -> str:
    html = [_kopf(7)]
    html.append("<p>Jeder Parameter der Rechnung mit Wert, Einheit und Quelle oder dem Vermerk "
                "„ausgewiesene Abschätzung von KAP3“ samt Herleitung.</p>")
    html.append("<h2>#95 Hitzebelastung</h2>")
    html.append('<table class="parameter"><tr><th>Parameter</th><th class="zahl">Wert</th>'
                '<th>Einheit</th><th>Quelle oder Abschätzung</th></tr>')
    for p in d.parameter:
        label = str(p.get("label") or "").removeprefix("Schadensfunktion: ")
        html.append(f"<tr><td>{_h(label)}</td><td class=\"zahl\">{_h(_wert(p))}</td>"
                    f"<td>{_h(p.get('unit') or '')}</td><td>{_h(_herkunft(p))}</td></tr>")
    html.append("</table>")
    html.append(_stand(d))
    return "\n".join(html)


# ── Teil 8 ──────────────────────────────────────────────────────────────────────

def teil_8(d: Berichtsdaten) -> str:
    e = d.ergebnis95
    html = [_kopf(8)]
    html.append("<h2>Vollständigkeit</h2>")
    html.append(f"<p>In der Summe dieses Berichts: {_h(d.beziffert_text)}. Die Summe läuft nur "
                f"über Klimawirkungen mit Euro-Betrag (Klasse A). Alle übrigen Klimawirkungen "
                f"fehlen in der Summe; der Gesamtwert ist deshalb eine <strong>Untergrenze</strong>.</p>")
    html.append("<h2>Aktive Schadenskonten</h2>")
    html.append("<p>#95 Hitzebelastung bucht in das Konto K1 Gesundheit (verlorene Lebensjahre "
                "und Krankenhauseinweisungen). Weitere Folgen der Hitze für die Gesundheit sind "
                "im Betrag nicht enthalten; auch deshalb ist er eine Untergrenze.</p>")
    html.append("<h2>Benannte Modellgrenzen</h2>")
    grenzen = []
    if e.band_eur:
        grenzen.append(
            f"Kostensatz je verlorenem Lebensjahr: {_betrag(d, e.voly_eur)}, Band "
            f"{_betrag(d, e.band_voly_eur[0])} bis {_betrag(d, e.band_voly_eur[1])}; der "
            f"Jahresbetrag liegt damit zwischen {_betrag(d, e.band_eur[0])} und "
            f"{_betrag(d, e.band_eur[1])}.")
    # Grenzen als HTML: Beträge tragen ihre Auszeichnung, die übrigen Sätze werden maskiert.
    grenzen += [_h(g) for g in [
        "Kostensatz je Krankenhausfall: Durchschnitt aller Krankenhausfälle als Ersatz, weil ein "
        "Satz für hitzebedingte Einweisungen nicht veröffentlicht ist (ausgewiesene Abschätzung "
        "von KAP3, Teil 7).",
        "Temperatur je Zelle: Rasterwert 1 km mit einer Feinstruktur von 0,58 K darunter; lokale "
        "Wärmeinseln einzelner Straßenzüge sind darin nur gemittelt enthalten.",
        "Zeitraum: Klima der Sommer 2016–2025; die Projektion bis 2065 ist nicht Teil dieses "
        "Betrags.",
    ]]
    html.append("<ul>")
    html += [f"<li>{g}</li>" for g in grenzen]
    html.append("</ul>")
    html.append(_stand(d))
    return "\n".join(html)


# ── Teil 9 ──────────────────────────────────────────────────────────────────────

# Exporte der Anwendung: (Art nach der Namensregel, Endung, Bezeichnung, Inhalt). Die Art ist
# dieselbe, die die Download-Routen an ``download_namen`` geben (T-1424).
EXPORTE = [
    ("geodaten", "gpkg", "GeoPackage",
     "Ergebnisse je bewohnter 100-m-Zelle zum Öffnen in einem Geoinformationssystem"),
    ("massnahmen", "xlsx", "Maßnahmen-Excel",
     "Maßnahmen mit Kosten, vermiedenen Schäden, Gewissheit und Umsetzung"),
    ("parameter", "xlsx", "Parameter-Excel",
     "alle Parameter der Rechnung mit Wert, Einheit und Quelle oder ausgewiesener Abschätzung"),
]


def export_dateiname(d: Berichtsdaten, art: str, endung: str) -> str:
    """Dateiname eines Exports nach der Namensregel der Downloads (T-1424)."""
    return download_dateiname(art, d.kommune.name, d.kommune.ags, endung)


def teil_9(d: Berichtsdaten) -> str:
    """Anhang (T-1420): je Methodik-Bericht eine Zeile ``tr.anlage[data-kwra][id=anlage-M…]`` mit
    ``td.kennung``, ``td.titel`` und ``td.revision``; je Export eine Zeile ``tr.export[data-art]``
    mit ``td.dateiname`` nach der Namensregel. Die Teile 0 bis 8 verweisen auf die Kennung
    („Anlage M95“), nie auf einen Pfad."""
    k = d.kommune
    anlagen = list(getattr(d, "anlagen", []))
    html = [_kopf(9)]
    html.append("<h2>Anlagen: Methodik-Berichte</h2>")
    html.append(
        "<p>Jede Klimawirkung, die dieser Bericht in Euro beziffert, ist in einem Methodik-Bericht "
        "beschrieben: Rechenkette von der amtlichen Quelle bis zum Euro-Betrag, jeder Parameter mit "
        "Quelle, Modellgrenzen. Die Methodik-Berichte gehen als Anlagen mit diesem Bericht an die "
        "Kommune. Wo die Teile 0 bis 8 auf eine Methodenbeschreibung verweisen, nennen sie die "
        "Kennung der Anlage aus dieser Tabelle.</p>")
    if anlagen:
        html.append('<table class="anlagen"><tr><th>Anlage</th><th>Methodik-Bericht</th>'
                    '<th>Titel</th><th>Revision</th></tr>')
        for a in anlagen:
            html.append(
                f'<tr class="anlage" id="anlage-{_h(a.kennung)}" data-kwra="{a.nr}">'
                f'<td class="kennung">Anlage {_h(a.kennung)}</td><td>#{a.nr}</td>'
                f'<td class="titel">{_h(a.titel)}</td><td class="revision">{_h(a.revision)}</td></tr>')
        html.append("</table>")
    else:
        html.append("<p>Dieser Bericht verweist auf keinen Methodik-Bericht; deshalb liegt keine "
                    "Anlage bei.</p>")
    html.append("<h2>Exporte</h2>")
    html.append(
        f"<p>Die Daten dieses Berichts gibt es für {_h(k.name)} zusätzlich als Dateien zum "
        f"Herunterladen in der Anwendung. Die Dateinamen folgen einer Regel: Art des Dokuments, "
        f"Name der Kommune und amtlicher Gemeindeschlüssel.</p>")
    html.append('<table class="exporte"><tr><th>Export</th><th>Inhalt</th><th>Dateiname</th></tr>')
    for art, endung, bezeichnung, inhalt in EXPORTE:
        html.append(
            f'<tr class="export" data-art="{_h(art)}"><td>{_h(bezeichnung)}</td><td>{_h(inhalt)}</td>'
            f'<td class="dateiname">{_h(export_dateiname(d, art, endung))}</td></tr>')
    html.append("</table>")
    html.append(_stand(d))
    return "\n".join(html)


TEILE: dict[int, Callable[[Berichtsdaten], str]] = {
    0: teil_0, 1: teil_1, 2: teil_2, 3: teil_3, 4: teil_4, 5: teil_5, 6: teil_6, 7: teil_7,
    8: teil_8, 9: teil_9,
}
