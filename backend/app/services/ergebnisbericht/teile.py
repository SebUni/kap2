"""Die Teile des PDF-Ergebnisberichts als HTML-Abschnitte.

Gliederung: ``dokumente/produkt/pdf-ergebnisbericht-gliederung.md`` (Firmen-Repo), Teile 0 bis 9.
Der Formatpilot (T-1414) setzt die Teile 0, 1, 4 (nur #95), 7 und 8 um, Teil 2 kommt aus der
Konformitäts-Checkliste (T-1416, ``konformitaet.py``), Teil 3 aus den Klimakennwerten des
Sammlers (T-1417, ``klima.py``). Jeder Teil ist eine
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
    STATUS, fundstelle_ohne_datei, lies_checkliste, lueckensatz, umschreibe,
)
from app.services.ergebnisbericht.sammler import DATENSTAENDE, Berichtsdaten
from app.services.kurzfassung_markdown import _de_euro

UEBERSCHRIFTEN = {
    0: "Teil 0 · Kopf und Identität",
    1: "Teil 1 · Beschlussfähige Zusammenfassung",
    2: "Teil 2 · Rechtlicher und methodischer Rahmen",
    3: "Teil 3 · Klimatische Ausgangslage",
    4: "Teil 4 · Betroffenheitsanalyse je Klimawirkung",
    7: "Teil 7 · Parameter- und Quellenverzeichnis",
    8: "Teil 8 · Grenzen und Vollständigkeitsanzeige",
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
        ("Methodikversion", f"{s.methodik} (Modellstand {s.modell})"),
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
    (``td.status``) und Lückensatz (``td.luecke``, bei „erfüllt“ ein Strich). ``checkliste`` ist
    für den Test: eine Kopie mit geändertem Status ändert die Ausgabe dieser Zeile.
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
        f"<p>Die KWRA 2021 bewertet 102 Klimawirkungen; im Bericht sind davon die Klimawirkungen "
        f"des Produktkatalogs erfasst ({_h(d.beziffert_text)}).</p>")
    html.append('<table class="konformitaet"><tr><th>Nr</th><th>Anforderung</th><th>Quelle</th>'
                '<th>Fundstelle</th><th>Status</th><th>Lücke</th></tr>')
    for z in zeilen:
        luecke = lueckensatz(z.luecke) if z.status != "erfüllt" else "—"
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
    aus denselben Parameterdaten (``d.parameter``, ``_herkunft``), nicht als fester Text (Vorgabe P1)."""
    for p in d.parameter:
        if p.get("id") == param_id:
            return _herkunft(p)
    return ""


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
                f"Der Betrag gilt für die ganze Kommune; eine Aufteilung nach Ortsteilen enthält "
                f"diese Fassung nicht.</p>")
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
        return f"{_KLASSE[klasse]}: {herleitung}"
    return f"{_KLASSE.get(klasse, 'belegt')}: {quelle}"


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
        "Temperatur je Zelle: Rasterwert 1 km mit einer Feinstruktur von 0,5 K darunter; lokale "
        "Wärmeinseln einzelner Straßenzüge sind darin nur gemittelt enthalten.",
        "Zeitraum: Klima der Sommer 2016–2025; die Projektion bis 2065 ist nicht Teil dieses "
        "Betrags.",
    ]]
    html.append("<ul>")
    html += [f"<li>{g}</li>" for g in grenzen]
    html.append("</ul>")
    html.append(_stand(d))
    return "\n".join(html)


TEILE: dict[int, Callable[[Berichtsdaten], str]] = {
    0: teil_0, 1: teil_1, 2: teil_2, 3: teil_3, 4: teil_4, 7: teil_7, 8: teil_8,
}
