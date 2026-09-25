"""Bevölkerungsentwicklung je Gemeinde als Datenmodul (Checklistenzeile 16, A2, Ticket T-1164-cto).

Das Modul liefert je amtlichem Gemeindeschlüssel (AGS, 8 Stellen) die Einwohnerzahl zu zwei
Stichtagen und die Veränderung in Prozent. Es ist keine Methodik und rechnet nur diese eine
Prozentzahl. Zur Laufzeit gibt es keinen Netzabruf und keinen Schlüssel: gelesen wird allein die
Datei ``bevoelkerungsentwicklung.json`` neben diesem Modul.

Quelle: Statistisches Bundesamt (Destatis), Gemeindeverzeichnis-Informationssystem GV-ISys,
Jahresausgaben „Gemeinden in Deutschland nach Fläche, Bevölkerung und Postleitzahl“ (Excel,
ohne Anmeldung und ohne Schlüssel abrufbar):

- 31.12.2017: https://www.destatis.de/DE/Themen/Laender-Regionen/Regionales/Gemeindeverzeichnis/Administrativ/Archiv/GVAuszugJ/31122017_Auszug_GV.xlsx
- 31.12.2023: https://www.destatis.de/DE/Themen/Laender-Regionen/Regionales/Gemeindeverzeichnis/Administrativ/Archiv/GVAuszugJ/31122023_Auszug_GV.xlsx

Lizenz: Die Dateien tragen den Vermerk „Vervielfältigung und Verbreitung, auch auszugsweise, mit
Quellenangabe gestattet“ (© Statistisches Bundesamt, im Auftrag der Herausgebergemeinschaft
Statistische Ämter des Bundes und der Länder). Die Quelle wird bei jeder Ausgabe genannt.

Warum 2017 und 2023 und nicht 2011 und 2025: Die Bevölkerung im GV-ISys beruht bis Berichtsjahr 2023
auf der Fortschreibung des Zensus 2011, ab Berichtsjahr 2024 auf dem Zensus 2022; die Ausgabe
31.12.2011 beruht noch auf früheren Zählungen, und ab Berichtsjahr 2016 gilt eine geänderte
Fortschreibungsmethode. Nur innerhalb einer Basis und einer Methode ist ein Vergleich ohne
Sprung möglich. Das älteste Jahr ohne diese Einschränkungen ist 2017, das jüngste 2023.

Aufbereitung (einmalig, Ergebnis liegt im Repo; nicht Teil des Laufzeitcodes):

1. Beide Excel-Dateien von der Adresse oben laden, jeweils das zweite Blatt öffnen.
2. Nur Zeilen mit Satzart ``60`` (Gemeinde) mit Fläche und Bevölkerung nehmen. AGS = Land (Spalte C)
   + Regierungsbezirk (D) + Kreis (E) + Gemeinde (G); Fläche in Spalte I, Bevölkerung
   „insgesamt“ in Spalte J.
3. Nur AGS behalten, die in beiden Ausgaben vorkommen und deren Fläche sich um höchstens 3 %
   unterscheidet (sonst hat sich der Gebietsstand geändert, etwa durch Eingemeindung, und die
   beiden Zahlen gehören nicht zum selben Gebiet).
4. Als ``{"jahr_alt": 2017, "jahr_neu": 2023, "gemeinden": {AGS: [Einwohner_alt, Einwohner_neu]}}``
   ohne Leerzeichen als JSON schreiben.

Abrufzeit der Aufbereitung: 25.09.2026, 16:14 Uhr UTC (Stand der Dateien: 2017 vom 05.12.2023,
2023 vom 29.10.2024 auf dem Server von Destatis).
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import TypedDict

_DATEI = Path(__file__).with_name("bevoelkerungsentwicklung.json")

QUELLE = (
    "Statistisches Bundesamt (Destatis), Gemeindeverzeichnis-Informationssystem GV-ISys, "
    "Gemeinden nach Fläche und Bevölkerung, Stichtage 31.12.2017 und 31.12.2023 "
    "(Fortschreibung auf Basis des Zensus 2011); Vervielfältigung mit Quellenangabe gestattet"
)

MODELLGRENZE = (
    "Die Zahl zeigt nur, wie sich die Einwohnerzahl der Gemeinde zwischen zwei vergangenen "
    "Stichtagen verändert hat. Sie ist keine Vorausberechnung: Sie sagt nicht, wie viele Menschen "
    "künftig in der Kommune leben werden. Urbanisierung, also die Verschiebung zwischen Stadt und "
    "Land, ist nicht erfasst, weil sich dafür keine offene Quelle ohne Schlüssel gefunden hat. "
    "Alters- und Haushaltsstruktur bleiben unberücksichtigt. Gemeinden, deren Gebiet sich "
    "zwischen den Stichtagen geändert hat (etwa durch Eingemeindung), und Gemeinden ohne Wert zu "
    "beiden Stichtagen haben keinen Eintrag. Die Bevölkerung beruht auf der Fortschreibung des "
    "Zensus 2011; der Zensus 2022 ist bewusst nicht vermischt, weil sonst ein Sprung in der "
    "Zählbasis als Wachstum oder Schrumpfung erschiene."
)


class Entwicklung(TypedDict):
    jahr_alt: int
    jahr_neu: int
    einwohner_alt: int
    einwohner_neu: int
    veraenderung_prozent: float
    quelle: str


@lru_cache(maxsize=1)
def _laden() -> dict:
    with _DATEI.open(encoding="utf-8") as f:
        return json.load(f)


def entwicklung(ags: str) -> Entwicklung | None:
    """Einwohner zu zwei Stichtagen und Veränderung in Prozent (eine Nachkommastelle).

    ``None``, wenn der 8-stellige AGS unbekannt ist oder keinen vergleichbaren Wert hat.
    """
    daten = _laden()
    paar = daten["gemeinden"].get(str(ags))
    if paar is None:
        return None
    alt, neu = paar
    return {
        "jahr_alt": daten["jahr_alt"],
        "jahr_neu": daten["jahr_neu"],
        "einwohner_alt": alt,
        "einwohner_neu": neu,
        "veraenderung_prozent": round((neu - alt) / alt * 100, 1),
        "quelle": QUELLE,
    }
