"""Ausgebbare Fassung der Bestandsaufnahme in Markdown (Ticket T-0757,
ISO 14091, Checklistenzeile 16, Teil 4, Vorhaben T-0447).

Reine Funktion ohne Datenbank und ohne Netz. Formatiert ausschließlich das Dict
aus ``app.services.bestandsaufnahme_service.bestandsaufnahme_fuer_kommune``;
rechnet nichts nach. Größen mit Wert stehen in der Tabelle ihrer Gruppe, jede
Größe ohne Wert steht mit ihrem ``luecke_satz`` unter „Datenlücken“.
"""

from __future__ import annotations

from app.data import sources
from app.data.bevoelkerungsentwicklung import MODELLGRENZE
from app.data.catrare import MODELLGRENZE as MODELLGRENZE_CATRARE
from app.services.kang_nachweis_markdown import _de_betrag

TITEL = "# Bestandsaufnahme"

EINLEITUNG = (
    "Die Bestandsaufnahme ist der Risikoberechnung vorgeschaltet: Sie erfasst "
    "vulnerable Personengruppen, klimasensible Strukturen und vergangene "
    "Klimarisiken der Kommune, bevor Risiken bewertet werden."
)

# (Gruppenschlüssel, Überschrift) in Ausgabereihenfolge.
GRUPPEN = [
    ("vulnerable_personen", "## Vulnerable Personengruppen"),
    ("natuerliche_systeme", "## Natürliche Systeme"),
    ("klimasensible_strukturen", "## Klimasensible Strukturen"),
    ("vergangene_ereignisse", "## Vergangene Klimarisiken"),
    ("trends", "## Trends"),
]

# Modellgrenzen je Gruppe, wörtlich unter der Tabelle der Gruppe.
GRUPPEN_MODELLGRENZEN = {"vergangene_ereignisse": MODELLGRENZE_CATRARE, "trends": MODELLGRENZE}

UEBERSCHRIFT_LUECKEN = "## Datenlücken"


def _de_wert(wert: float | int) -> str:
    """Deutsche Zahlenschreibweise: Ganzzahlen ohne, Gleitkommazahlen mit zwei Nachkommastellen."""
    if isinstance(wert, int):
        return f"{wert:,}".replace(",", ".")
    return _de_betrag(wert)


def _zelle(text: str) -> str:
    return str(text).replace("|", "\\|").replace("\n", " ")


def _quellen_klartext(keys: list[str]) -> str:
    eintraege = sources.resolve(keys)
    if not eintraege:
        return "—"
    return "; ".join(e["ieee"] for e in eintraege)


def _tabelle(groessen: list[dict]) -> str:
    zeilen = [
        "| Größe | Wert | Einheit | Quelle |",
        "| --- | --- | --- | --- |",
    ]
    for g in groessen:
        zeilen.append("| {label} | {wert} | {einheit} | {quelle} |".format(
            label=_zelle(g["label"]),
            wert=_de_wert(g["wert"]),
            einheit=_zelle(g.get("einheit") or "—"),
            quelle=_zelle(_quellen_klartext(g.get("quellen") or [])),
        ))
    return "\n".join(zeilen)


def _zusatz_zeile(g: dict) -> str:
    """Beide Stichtage mit Einwohnerzahl und die Veränderung (Größe „Bevölkerungsentwicklung“)."""
    z = g["zusatz"]
    return (
        f"Einwohner am 31.12.{z['jahr_alt']}: {_de_wert(z['einwohner_alt'])}; "
        f"am 31.12.{z['jahr_neu']}: {_de_wert(z['einwohner_neu'])}; "
        f"Veränderung: {_de_wert(g['wert'])} {g.get('einheit') or ''}".rstrip()
    )


def _datum_de(iso: str) -> str:
    """ISO-Zeitstempel (``2025-06-29T14:50:00``) als Datum ``29.06.2025``."""
    j, m, t = str(iso)[:10].split("-")
    return f"{t}.{m}.{j}"


def _zusatz_starkregen(g: dict) -> str:
    return f"Jüngstes Ereignis: {_datum_de(g['zusatz']['juengstes_beginn'])}"


def bestandsaufnahme_markdown(ergebnis: dict) -> str:
    """Formatiert das Ergebnis von ``bestandsaufnahme_fuer_kommune`` als Markdown."""
    groessen = ergebnis["groessen"]

    teile = [TITEL, "", EINLEITUNG, ""]
    for gruppe, ueberschrift in GRUPPEN:
        mit_wert = [g for g in groessen if g["gruppe"] == gruppe and g["wert"] is not None]
        teile += [ueberschrift, ""]
        teile += [_tabelle(mit_wert) if mit_wert else "Für diese Gruppe liegt kein Wert vor.", ""]
        hinweise = [
            f"- {g['label']}: {g['hinweis']}"
            for g in groessen
            if g["gruppe"] == gruppe and g["wert"] is None and g.get("hinweis")
        ]
        if hinweise:
            teile += ["\n".join(hinweise), ""]
        for g in mit_wert:
            if g.get("zusatz"):
                zeile = _zusatz_starkregen(g) if g["code"] == "starkregenereignisse" else _zusatz_zeile(g)
                teile += [zeile, ""]
        if gruppe in GRUPPEN_MODELLGRENZEN:
            teile += [GRUPPEN_MODELLGRENZEN[gruppe], ""]

    saetze: list[str] = []
    for g in groessen:
        satz = g.get("luecke_satz") or ""
        if g["wert"] is None and satz and satz not in saetze:
            saetze.append(satz)
    teile += [UEBERSCHRIFT_LUECKEN, ""]
    teile += ["\n".join(f"- {s}" for s in saetze) if saetze else "Keine Datenlücken.", ""]
    return "\n".join(teile)
