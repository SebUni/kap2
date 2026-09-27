"""Klimatische Ausgangslage für Teil 3 des PDF-Ergebnisberichts (T-1417).

Je in Euro bezifferter Klimawirkung ein Kennwert mit Beobachtung (DWD-CDC) und Projektion unter
RCP 4.5 und RCP 8.5. Die Werte kommen aus denselben Quellen wie im Produkt:

- **Beobachtung:** die gepinnten Zelldaten der Beispielkommune (DWD-CDC-Raster 1 km, Mittel der
  Jahre 2016–2025), einwohnergewichtet — derselbe Wert, mit dem der Jahresbetrag #95 rechnet
  (``Ergebnis95.hitzetage_mittel``).
- **Projektion:** ``climate.dwd_data.get_climate_projection`` für das Bundesland der Kommune, also
  die Landesreihe, mit der das Produkt die Projektion 2025–2065 zeigt.

Beobachtung und Projektion liegen auf verschiedenen Ebenen (Kommune gegen Land). Teil 3 sagt das
und nennt zusätzlich den Anstieg gegenüber 2025, weil nur der Anstieg von der Landesreihe auf die
Kommune übertragbar ist; ein Vergleich der absoluten Werte würde die Lage verfälschen.

Fehlt für eine Klimawirkung ein Kennwert, steht statt der Zahl der Grund (harte Regel 1).
"""

from __future__ import annotations

from dataclasses import dataclass

# Jahre, für die Teil 3 die Projektion zeigt; 2025 ist das Startjahr der Reihe.
JAHR_START = 2025
JAHRE_PROJEKTION = (2040, 2065)
SZENARIEN = {"rcp45": "RCP 4.5", "rcp85": "RCP 8.5"}

QUELLE_BEOBACHTUNG = ("Deutscher Wetterdienst, Climate Data Center (DWD-CDC), Jahresraster "
                      "„heiße Tage“ 1 km, einwohnergewichtet über die bewohnten Zellen der Kommune")
STAND_BEOBACHTUNG = "Mittel der Jahre 2016–2025, Raster abgerufen am 26.09.2026"
QUELLE_PROJEKTION = ("Ensemble nach IPCC AR6, DWD KlimaFolgenOnline und ReKliEs-DE, regionalisiert "
                     "über das Landesmittel der heißen Tage ({land})")
# Letzte Änderung der Projektionstabelle im Produkt (Versionsverlauf, 07.06.2026).
STAND_PROJEKTION = "Projektionstabelle des Produkts, Stand 07.06.2026, gleitendes Mittel über 5 Jahre"


@dataclass(frozen=True)
class Klimazahl:
    """Eine Zahl in Teil 3 mit Quelle und Datenstand; ``wert`` None heißt: ``grund`` steht dort."""
    wert: float | None
    quelle: str
    datenstand: str
    grund: str = ""


@dataclass(frozen=True)
class Klimazeile:
    kwra_id: int
    kwra_name: str
    kennwert: str
    einheit: str
    beobachtung: Klimazahl
    # Szenario → Jahr → Zahl; zusätzlich der Startwert 2025 der Landesreihe je Szenario.
    projektion: dict[str, dict[int, Klimazahl]]
    start: dict[str, Klimazahl]


def _hitzetage(kommune, beobachtet: float, kwra_id: int, kwra_name: str) -> Klimazeile:
    from app.services.climate.dwd_data import get_climate_projection

    proj = get_climate_projection(kommune.bundesland)
    jahre = proj["years"]
    quelle_p = QUELLE_PROJEKTION.format(land=kommune.bundesland)
    projektion: dict[str, dict[int, Klimazahl]] = {}
    start: dict[str, Klimazahl] = {}
    for sz in SZENARIEN:
        reihe = proj["scenarios"][sz]["hot_days"]
        start[sz] = Klimazahl(reihe[jahre.index(JAHR_START)], quelle_p, STAND_PROJEKTION)
        projektion[sz] = {j: Klimazahl(reihe[jahre.index(j)], quelle_p, STAND_PROJEKTION)
                          for j in JAHRE_PROJEKTION}
    return Klimazeile(
        kwra_id=kwra_id, kwra_name=kwra_name,
        kennwert="Heiße Tage je Jahr (Höchsttemperatur mindestens 30 °C)", einheit="Tage",
        beobachtung=Klimazahl(beobachtet, QUELLE_BEOBACHTUNG, STAND_BEOBACHTUNG),
        projektion=projektion, start=start,
    )


def _ohne_kennwert(kwra_id: int, kwra_name: str) -> Klimazeile:
    grund = ("Für diese Klimawirkung führt das Produkt noch keinen Klimakennwert mit "
             "Beobachtung und Projektion.")
    leer = Klimazahl(None, "—", "—", grund)
    return Klimazeile(
        kwra_id=kwra_id, kwra_name=kwra_name, kennwert=grund, einheit="",
        beobachtung=leer,
        projektion={sz: {j: leer for j in JAHRE_PROJEKTION} for sz in SZENARIEN},
        start={sz: leer for sz in SZENARIEN},
    )


def klimazeilen(kommune, ergebnis95, klimawirkungen: list[dict]) -> list[Klimazeile]:
    """Eine Zeile je in Euro bezifferter Klimawirkung, in der Reihenfolge des Berichts."""
    zeilen = []
    for w in klimawirkungen:
        if w["kwra_id"] == 95:
            zeilen.append(_hitzetage(kommune, ergebnis95.hitzetage_mittel, 95, w["kwra_name"]))
        else:
            zeilen.append(_ohne_kennwert(w["kwra_id"], w["kwra_name"]))
    return zeilen
