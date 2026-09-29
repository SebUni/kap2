"""Sammler des PDF-Ergebnisberichts: alles, was die Teile brauchen, an einer Stelle.

Die Teile rechnen nichts selbst; sie formatieren, was der Sammler liefert. So trägt jede
Zahl im Bericht denselben Stand (Berichts-, Methodik- und Datenstand, harte Regel 3 der
Gliederung).
"""

from __future__ import annotations

import datetime as dt
import glob
import os
import re
from dataclasses import dataclass, field

from app.services.ergebnisbericht.beispiel import (
    MORB, MORT, Beispielkommune, Ergebnis95, rechne_95,
)

BERICHTSVERSION = "Fassung 0.1 (Formatpilot)"

_METHODIK_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "docs", "methodik")

DATENSTAENDE = [
    ("Einwohner und Altersgruppen", "Zensus 2022, Gitterdaten 100 m, Stichtag 15.05.2022"),
    ("Sommermittel und Hitzetage", "Deutscher Wetterdienst, Climate Data Center, Raster 1 km, "
                                    "Mittel der Sommer 2016–2025"),
    ("Gemeindegrenze", "BKG, Verwaltungsgebiete 1 : 250 000 (VG250), Gebietsstand 01.01. der "
                       "aktuellen Ausgabe, abgerufen am 26.09.2026"),
    ("Ortsteilgrenzen", "OpenStreetMap über Overpass API, ODbL 1.0, © OpenStreetMap-Mitwirkende; "
                        "Stand der OSM-Daten 27.09.2026, 11:19 Uhr UTC (Zeitstempel der Datenbasis), "
                        "abgerufen am 27.09.2026"),
    ("Kostensätze", "Preisstand 2024"),
]


@dataclass
class Stand:
    bericht: str
    methodik: str
    modell: str
    daten: str
    erstellt: dt.date

    def zeile(self) -> str:
        return (f"Stand: Bericht {self.bericht} vom {self.erstellt:%d.%m.%Y} · "
                f"Methodik {self.methodik} · Daten {self.daten}")


@dataclass(frozen=True)
class Anlage:
    """Methodik-Bericht als Anlage des Ergebnisberichts (Teil 9, T-1420).

    ``kennung`` hängt nur an der Nummer des Berichts (``M95``), nicht an der Reihenfolge: So
    bleibt ein Verweis „Anlage M95“ in den Teilen 0 bis 8 gleich, wenn weitere Berichte dazukommen.
    """
    nr: int
    titel: str
    revision: str

    @property
    def kennung(self) -> str:
        return anlage_kennung(self.nr)


def anlage_kennung(nr: int | str) -> str:
    return f"M{int(nr)}"


# Verweis auf einen Methodik-Bericht im Text der Teile („Bericht #95 §3.5“, „Methodik-Bericht #95“).
VERWEIS_METHODIK = re.compile(r"(?:Methodik-)?Bericht #(\d+)")


def methodik_anlage(nr: int) -> Anlage:
    """Titel und Revision des Methodik-Berichts ``nr`` aus Überschrift und Statuszeile.

    Fehlt der Bericht oder seine Revision, bricht die Erzeugung ab: Ein Bericht, der auf eine
    Methodenbeschreibung verweist, die er nicht beilegen kann, wird nicht erzeugt (harte Regel 4).
    """
    treffer = sorted(glob.glob(os.path.join(_METHODIK_DIR, f"{int(nr)}_*.md")))
    if not treffer:
        raise ValueError(f"Methodik-Bericht #{nr} fehlt; ohne ihn fehlt die Anlage in Teil 9")
    with open(treffer[0], encoding="utf-8") as fh:
        kopf = fh.read(4000)
    ueberschrift = re.search(r"^# (.+)$", kopf, re.MULTILINE)
    revision = re.search(r"Rev\. \d+(?:, Fortschreibung \d+)?", kopf)
    if not ueberschrift or not revision:
        raise ValueError(f"Methodik-Bericht #{nr}: Überschrift oder Revision in der Statuszeile fehlt")
    titel = ueberschrift.group(1).split(" — ", 1)[-1].strip()
    return Anlage(int(nr), titel, revision.group(0))


def _anlagen(im_bericht: list[dict], parameter: list[dict]) -> list[Anlage]:
    """Je in Euro bezifferter Klimawirkung ihr Methodik-Bericht, dazu jeder weitere Bericht, auf
    den ein Parameter verweist (sonst zeigte ein Verweis in Teil 4 oder 7 ins Leere)."""
    nummern: list[int] = []
    for w in im_bericht:
        if int(w["kwra_id"]) not in nummern:
            nummern.append(int(w["kwra_id"]))
    for p in parameter:
        for m in VERWEIS_METHODIK.finditer(repr(p)):
            if int(m.group(1)) not in nummern:
                nummern.append(int(m.group(1)))
    return [methodik_anlage(nr) for nr in nummern]


@dataclass
class Berichtsdaten:
    kommune: Beispielkommune
    stand: Stand
    ergebnis95: Ergebnis95
    klimawirkungen_katalog: int
    klimawirkungen_im_bericht: list[dict]
    parameter: list[dict] = field(default_factory=list)
    klima: list = field(default_factory=list)   # Klimazeile je bezifferter Klimawirkung (Teil 3)
    raum: list = field(default_factory=list)    # Raumzeilen von #95 je Ortsteil (Teil 5)
    # Maßnahmenzeilen (Teil 6, ``massnahmen.massnahmenzeile``). Eine Beispielkommune rechnet
    # ohne Datenbank und hat keine angelegten Maßnahmen; Teil 6 sagt das dann ausdrücklich.
    massnahmen: list = field(default_factory=list)
    # Methodik-Berichte als Anlagen (Teil 9); Verweise in den Teilen 0 bis 8 nennen ihre Kennung.
    anlagen: list = field(default_factory=list)

    @property
    def beziffert_text(self) -> str:
        x = len(self.klimawirkungen_im_bericht)
        return f"{x} von {self.klimawirkungen_katalog} Klimawirkungen in Euro beziffert"


def methodikstand_95() -> str:
    """Revision des Methodik-Berichts #95 aus seiner Statuszeile (ohne Pfadangabe im Text)."""
    pfad = os.path.join(_METHODIK_DIR, "95_hitzebelastung.md")
    try:
        with open(pfad, encoding="utf-8") as fh:
            kopf = fh.read(2000)
    except OSError:
        kopf = ""
    m = re.search(r"Rev\. \d+, Fortschreibung \d+", kopf)
    return f"#95 {m.group(0)}" if m else "#95"


def _parameter_95() -> list[dict]:
    from app.services import parameter_registry as pr
    zeilen: list[dict] = []
    for code in (MORT, MORB):
        zeilen.extend(pr.catalog_parameters(layer_code=code))
    return zeilen


def sammle(kommune: Beispielkommune, heute: dt.date | None = None) -> Berichtsdaten:
    from app.data import catalog

    ergebnis = rechne_95(kommune)
    stand = Stand(
        bericht=BERICHTSVERSION,
        methodik=methodikstand_95(),
        modell=catalog.MODEL_VERSION,
        daten="Zensus 2022, DWD 2016–2025, Preisstand 2024",
        erstellt=heute or dt.date.today(),
    )
    kwra_ids = {r.get("kwra_id") for r in catalog.RISKS if r.get("kwra_id") is not None}
    mort = catalog.RISKS_BY_CODE[MORT]
    im_bericht = [{
        "kwra_id": mort["kwra_id"],
        "kwra_name": mort["kwra_name"],
        "kwra_field": mort.get("kwra_field", ""),
        "betrag_eur": ergebnis.jahresbetrag_eur,
    }]
    from app.services.ergebnisbericht.klima import klimazeilen
    from app.services.ergebnisbericht.raum import raumzeilen

    parameter = _parameter_95()
    return Berichtsdaten(
        kommune=kommune, stand=stand, ergebnis95=ergebnis,
        klimawirkungen_katalog=len(kwra_ids),
        klimawirkungen_im_bericht=im_bericht,
        parameter=parameter,
        klima=klimazeilen(kommune, ergebnis, im_bericht),
        raum=raumzeilen(kommune),
        anlagen=_anlagen(im_bericht, parameter),
    )
