"""Starkregenereignisse aus dem DWD-Katalog CatRaRe (Datenmodul, T-1165, A7).

Der Katalog listet radarbasierte Starkregenereignisse in Deutschland ab 2001. Das Modul
liest zur Laufzeit nur die mitgelieferte Datei ``catrare_ereignisse.csv`` (keine
Netzabfrage, keine Einstellungen, keine neue Abhängigkeit außer ``shapely``).

Aufbereitung (einmalig, außerhalb der Laufzeit)
-----------------------------------------------
1. Quelle: ``CatRaRE_2001_2025_T5_Eta_v2026_01.csv`` (Katalog T5, Version v2026.01,
   Ereignisse oberhalb einer Wiederkehrzeit von 5 Jahren) von
   https://opendata.dwd.de/climate_environment/CDC/event_catalogues/germany/precipitation/CatRaRE_v2026.01/data/
   (Abruf 25.09.2026; Last-Modified der Datei: 01.04.2026 10:05:10 GMT).
2. Je Zeile des Originals wurden übernommen: ``KEY_FIELD`` → ``id``, ``Date_START`` →
   ``beginn`` (ISO 8601, UTC), ``Duration`` → ``dauer_h``, ``SRImax`` → ``sri_max``.
   Der Katalog wurde nicht gefiltert: alle 40 636 Ereignisse stehen in der Datei,
   auch solche, deren Maximum knapp außerhalb Deutschlands liegt.
3. ``lon``/``lat`` stammen aus dem Maximum-Pixel des Ereignisses (``x_RRmaxPRJ``,
   ``y_RRmaxPRJ``, polarstereographisch, RADOLAN/RADKLIM-Projektion: Kugel mit
   Radius 6 370 040 m, wahre Breite 60° N, Zentralmeridian 10° O). Umgerechnet nach
   WGS84 mit der Umkehrformel des DWD:
   ``lon = atan2(x, -y) + 10°``,
   ``lat = asin((R²(1+sin 60°)² − (x²+y²)) / (R²(1+sin 60°)² + (x²+y²)))``.
   Stichprobe gegen die Ortsangaben des Katalogs: Höchenschwand 47,71° N / 8,21° O,
   Lichtenfels 51,15° N / 8,83° O, Briesen 51,80° N / 14,24° O. Gerundet auf 4
   Nachkommastellen (rund 10 m).
"""

from __future__ import annotations

import csv
from functools import lru_cache
from pathlib import Path

import numpy as np
import shapely
from shapely.geometry.base import BaseGeometry

_DATEI = Path(__file__).with_name("catrare_ereignisse.csv")

QUELLE = (
    "Deutscher Wetterdienst (DWD): Heavy precipitation events Version 2026.01 exceeding "
    "return period of 5 years based on RADKLIM-RW Version 2017.002 (CatRaRE T5, v2026.01), "
    "DOI 10.5676/DWD/CatRaRE_T5_Eta_v2026.01, Datei CatRaRE_2001_2025_T5_Eta_v2026_01.csv, "
    "https://opendata.dwd.de/climate_environment/CDC/event_catalogues/germany/precipitation/"
    "CatRaRE_v2026.01/data/CatRaRE_2001_2025_T5_Eta_v2026_01.csv, "
    "Lizenz CC BY 4.0, © Deutscher Wetterdienst 2026; Abruf 25.09.2026 "
    "(Dateistand 01.04.2026), 40 636 Ereignisse aus den Jahren 2001 bis 2025."
)

MODELLGRENZE = (
    "Der Katalog trägt keine Schäden: Er zeigt, wo und wann es radarbasiert sehr stark "
    "geregnet hat (Wiederkehrzeit über 5 Jahre), nicht, was das gekostet hat. Er trägt "
    "kein Hochwasser (keine Pegel, keine Flussüberschwemmung) und keine Hitze. Er beginnt "
    "erst 2001; frühere Ereignisse fehlen. Ein Ereignis wird einer Fläche über einen "
    "einzigen Punkt zugeordnet, den Ort des Niederschlagsmaximums, nicht über die "
    "Ausdehnung des Ereignisses: Ein Ereignis, das eine Fläche nur streift, aber dessen "
    "Maximum außerhalb liegt, wird ihr nicht zugerechnet, und umgekehrt. Schadensdaten "
    "bleiben beim Lückensatz der Größe schadensereignisse."
)


@lru_cache(maxsize=1)
def _lade() -> tuple[list[dict], np.ndarray, np.ndarray]:
    ereignisse: list[dict] = []
    with _DATEI.open(encoding="utf-8", newline="") as f:
        for z in csv.DictReader(f):
            ereignisse.append(
                {
                    "id": z["id"],
                    "beginn": z["beginn"],
                    "lon": float(z["lon"]),
                    "lat": float(z["lat"]),
                    "dauer_h": int(z["dauer_h"]),
                    "sri_max": int(z["sri_max"]) if z["sri_max"].isdigit() else None,
                }
            )
    lon = np.array([e["lon"] for e in ereignisse])
    lat = np.array([e["lat"] for e in ereignisse])
    return ereignisse, lon, lat


def ereignisse_in_flaeche(flaeche: BaseGeometry) -> list[dict]:
    """Ereignisse, deren Mittelpunkt (Maximum-Pixel) in ``flaeche`` liegt.

    ``flaeche``: shapely-Geometrie in WGS84 (lon/lat). Rückgabe: Kopien der Ereignis-
    Einträge (``id``, ``beginn``, ``lon``, ``lat``, ``dauer_h``, ``sri_max``) in der
    Reihenfolge des Katalogs; leere Liste, wenn keines darin liegt.
    """
    ereignisse, lon, lat = _lade()
    if flaeche is None or flaeche.is_empty:
        return []
    innen = shapely.intersects_xy(flaeche, lon, lat)
    return [dict(ereignisse[i]) for i in np.flatnonzero(innen)]
