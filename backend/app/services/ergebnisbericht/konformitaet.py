"""Konformitäts-Checkliste als Quelle für Teil 2 des PDF-Ergebnisberichts (T-1416).

Teil 2 „Rechtlicher und methodischer Rahmen“ wird bei jeder Erzeugung aus
``docs/KONFORMITAET_CHECKLISTE.md`` gelesen, nicht von Hand geschrieben: Ändert sich dort der
Status einer Zeile, ändert sich die Zeile im Bericht.

Übernommen werden Nr, Anforderung, Quelle, Fundstelle (ohne internen PDF-Dateinamen), Status und
Lücke. Die Spalte „Beleg im Produkt“ bleibt draußen, weil sie Pfade und Quelldateien nennt. Die
Lücke wird zum Kundentext umgeschrieben (``lueckensatz``): interne Verweise, Pfade, Code,
Ticketkennungen, Einzelnachweise, Begriffe der Stufen B und C der Transparenzgrenze und Euro-Beträge
von null fallen weg.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

CHECKLISTE = Path(__file__).resolve().parents[4] / "docs" / "KONFORMITAET_CHECKLISTE.md"

STATUS = ("erfüllt", "teilweise", "offen")
KOPF = ["Nr", "Anforderung", "Quelle", "Fundstelle", "Status", "Beleg im Produkt", "Lücke"]

ERSATZSATZ = ("Die Anforderung ist im Produkt nur zum Teil umgesetzt; die offenen Punkte sind in "
              "der internen Prüfung festgehalten.")

# Umschreibungen für den Kundentext: „Wiederherstellungskosten“ enthält das Sperrwort
# „Erstellungskosten“ der Stufe C als Teilwort.
_UMSCHREIBUNGEN = (
    ("Wiederherstellungskosten", "Kosten der Wiederherstellung"),
)

# Begriffe der Stufen B und C der Transparenzgrenze (Gliederung, Abschnitt 4).
_STUFE_B_C = ("Eich-Stichprobe", "Zwischentabelle", "Sensitivitätslauf", "Befund-Ledger",
              "Quellcode", "Erstellungskosten", ".py")
_EURO_NULL = re.compile(r"(?<![\d.,])[-−]?0(?:[.,]0+)?\s?(?:€|EUR\b|Euro\b)")
_INTERN = re.compile(
    r"docs/|reviews/|BEFUNDE_|" + chr(96) + r"|\.(?:md|py|tsx?|pdf|html)\b|\bT-\d{3,}|"
    r"Einzelnachweis|Gegenprobe Zeile|[\w./-]+/[\w./-]+\.\w+|\w+\(\)"
)
# Abkürzungen, nach deren Punkt kein Satz endet.
_ABKUERZUNGEN = {"z", "B", "Kap", "S", "Abs", "Nr", "Fn", "Abb", "bzw", "vgl", "ca", "u", "a",
                 "d", "h", "Tab", "Art", "ggf", "inkl", "insb"}


@dataclass(frozen=True)
class Anforderung:
    nr: int
    anforderung: str
    quelle: str
    fundstelle: str
    status: str
    luecke: str


def _zellen(zeile: str) -> list[str]:
    inhalt = zeile.strip()
    if inhalt.startswith("|"):
        inhalt = inhalt[1:]
    if inhalt.endswith("|"):
        inhalt = inhalt[:-1]
    return [z.strip() for z in inhalt.split("|")]


def lies_checkliste(pfad: str | Path | None = None) -> list[Anforderung]:
    """Die Anforderungszeilen der Tabelle unter „## Tabelle“ der Checkliste.

    Bricht ab bei fremdem Tabellenkopf, falscher Spaltenzahl, unbekanntem Status und bei
    „teilweise“ oder „offen“ ohne Lücke — ein solcher Fehler gehört in die Checkliste, nicht still
    in den Bericht.
    """
    text = Path(pfad or CHECKLISTE).read_text(encoding="utf-8")
    zeilen = text.splitlines()
    try:
        start = zeilen.index("## Tabelle")
    except ValueError as fehler:
        raise ValueError("Abschnitt „## Tabelle“ fehlt in der Konformitäts-Checkliste") from fehler
    tabelle: list[str] = []
    for zeile in zeilen[start + 1:]:
        if zeile.startswith("|"):
            tabelle.append(zeile)
        elif tabelle:
            break
    if len(tabelle) < 2 or _zellen(tabelle[0]) != KOPF:
        raise ValueError(f"Tabellenkopf der Konformitäts-Checkliste weicht ab: {tabelle[:1]!r}")
    ergebnis = []
    for zeile in tabelle[2:]:
        z = _zellen(zeile)
        if len(z) != len(KOPF):
            raise ValueError(f"Zeile mit {len(z)} statt {len(KOPF)} Spalten: {zeile[:60]!r}")
        nr, anforderung, quelle, fundstelle, status, _beleg, luecke = z
        if status not in STATUS:
            raise ValueError(f"Zeile {nr}: unbekannter Status {status!r} (erlaubt: {', '.join(STATUS)})")
        if status != "erfüllt" and luecke in ("", "—", "-"):
            raise ValueError(f"Zeile {nr}: Status {status!r} ohne Lücke")
        ergebnis.append(Anforderung(int(nr), anforderung, quelle, fundstelle, status, luecke))
    return ergebnis


def umschreibe(text: str) -> str:
    for alt, neu in _UMSCHREIBUNGEN:
        text = text.replace(alt, neu)
    return text


def fundstelle_ohne_datei(fundstelle: str) -> str:
    """„datei.pdf, Kap. 2.1.4.1“ → „Kap. 2.1.4.1“; der interne Dateiname gehört nicht in den Bericht."""
    return re.sub(r"^[^,]*\.pdf,\s*", "", fundstelle).strip()


def _ist_intern(text: str) -> bool:
    if _INTERN.search(text) or _EURO_NULL.search(text):
        return True
    klein = text.lower()
    return any(wort.lower() in klein for wort in _STUFE_B_C)


def _klammern_entfernen(text: str) -> str:
    """Klammern mit internem Inhalt fallen ganz weg, auch verschachtelte; andere bleiben."""
    auf, zu = "\x01", "\x02"
    muster = re.compile(r"\s*\(([^()]*)\)")
    while True:
        m = muster.search(text)
        if not m:
            break
        inhalt = m.group(1)
        if _ist_intern(inhalt.replace(auf, "(").replace(zu, ")")):
            text = text[:m.start()] + text[m.end():]
        else:
            vorspann = m.group(0)[: m.group(0).index("(")]
            text = text[:m.start()] + vorspann + auf + inhalt + zu + text[m.end():]
    return text.replace(auf, "(").replace(zu, ")")


def _saetze(text: str) -> list[str]:
    saetze, anfang = [], 0
    for m in re.finditer(r"[.!?]\s+", text):
        vorher = re.search(r"(\S+)$", text[anfang:m.start()])
        wort = vorher.group(1).lstrip("(„\"") if vorher else ""
        if wort in _ABKUERZUNGEN or len(wort) == 1 or wort.isdigit():
            continue
        saetze.append(text[anfang:m.end()].strip())
        anfang = m.end()
    rest = text[anfang:].strip()
    if rest:
        saetze.append(rest)
    return saetze


def _oberste_semikolons(satz: str) -> list[str]:
    teile, tiefe, anfang = [], 0, 0
    for i, zeichen in enumerate(satz):
        if zeichen in "(„":
            tiefe += 1
        elif zeichen in ")“" and tiefe:
            tiefe -= 1
        elif zeichen == ";" and tiefe == 0:
            teile.append(satz[anfang:i])
            anfang = i + 1
    teile.append(satz[anfang:])
    return [t.strip() for t in teile if t.strip()]


def lueckensatz(luecke: str) -> str:
    """Die Spalte „Lücke“ als Kundentext; leer, wenn die Zeile keine Lücke hat."""
    if luecke.strip() in ("", "—", "-"):
        return ""
    text = umschreibe(luecke)
    text = re.sub(r"laut docs/[^\s,;)]*[^\s,;).]", "laut interner Prüfung", text)
    text = _klammern_entfernen(text)
    behalten = []
    for satz in _saetze(text):
        teile = [t for t in _oberste_semikolons(satz) if not _ist_intern(t)]
        if not teile:
            continue
        s = "; ".join(t.rstrip(".;:, ") for t in teile).strip()
        if not s:
            continue
        s = s[0].upper() + s[1:]
        behalten.append(s + ".")
    ergebnis = " ".join(behalten)
    ergebnis = re.sub(r"\s+([,.;:])", r"\1", re.sub(r"\s+", " ", ergebnis)).strip()
    return ergebnis or ERSATZSATZ
