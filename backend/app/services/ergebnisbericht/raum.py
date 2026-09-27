"""Räumliche Aufteilung von #95 nach Ortsteilen (T-1564-cto, Paket 5b von T-1418-cto).

``raumzeilen(kommune, flaechen=None)`` ordnet jede bewohnte 100-m-Zelle der gepinnten Zelldaten
genau einer Zeile zu — einem Ortsteil oder dem „übrigen Gemeindegebiet“ — und rechnet #95 je Zeile
mit ``beispiel.rechne_95`` und einem Filter auf die Zellkennungen. Nur Daten, keine Darstellung.

Regeln (Planung T-1418-cto):

- **Zellmitte:** aus der Zellkennung ``CRS3035RES100mN<y>E<x>`` die linke untere Ecke in EPSG:3035,
  plus 50 m in beide Richtungen, mit ``pyproj`` nach EPSG:4326 (Länge, Breite) übertragen.
- **Eine Ebene je Gemeinde:** Unter den Ebenen (``admin_level`` 9 und 10) gilt die, deren Flächen
  die meisten Einwohner abdecken; bei Gleichstand 10.
- **Überlappung:** Liegt eine Zellmitte in mehreren Flächen der gewählten Ebene, gilt die kleinere
  Fläche (Fläche in EPSG:3035 gerechnet).
- **Rest:** Zellen, deren Mitte in keiner Fläche liegt, bilden die Zeile „übriges Gemeindegebiet“.
- **Ohne Fläche:** Führt die Quelle keine Fläche, gibt es genau eine Zeile für die ganze Kommune.
- Eine Fläche ohne bewohnte Zelle bekommt keinen Betrag, sondern einen Grund.

Die Altersbänder bleiben über alle Zellen der Gemeinde aufbereitet (Ersatzregel 65+ gebietsweit);
deshalb summieren sich Einwohner, Todesfälle, verlorene Lebensjahre, Einweisungen und Jahresbetrag
über alle Zeilen auf die Werte der ganzen Kommune.
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field
from functools import lru_cache

from app.services.ergebnisbericht.beispiel import KALIB, Beispielkommune, rechne_95, zellen

UEBRIG = "übriges Gemeindegebiet"
GRUND_OHNE_ZELLE = "In dieser Fläche liegt keine bewohnte Zelle des Zensus-Gitters."
_ZELLKENNUNG = re.compile(r"^CRS3035RES100mN(\d+)E(\d+)$")
HALBE_ZELLE_M = 50.0


@dataclass
class Raumzeile:
    """Eine Zeile der Aufteilung: Ortsteil, übriges Gemeindegebiet oder ganze Kommune."""
    name: str
    art: str                       # "ortsteil" | "uebrig" | "gemeinde"
    ebene: int | None              # admin_level der Fläche, sonst None
    zellkennungen: tuple[str, ...]
    einwohner: float
    einwohner_ab65: float
    hitzetage: float | None        # einwohnergewichtet
    todesfaelle: float | None
    yll: float | None
    einweisungen: float | None
    jahresbetrag_eur: float | None
    jahresbetrag_je_1000_eur: float | None = None
    todesfaelle_je_1000: float | None = None
    einweisungen_je_1000: float | None = None
    grund: str | None = None       # nur, wenn es keinen Betrag gibt
    osm_relation: int | None = None
    extra: dict = field(default_factory=dict)


def zellmitte_3035(zellkennung: str) -> tuple[float, float]:
    """Zellmitte (x = Rechtswert, y = Hochwert) in EPSG:3035 aus der Zellkennung."""
    m = _ZELLKENNUNG.match(zellkennung)
    if not m:
        raise ValueError(f"Unbekannte Zellkennung {zellkennung!r}")
    nord, ost = float(m.group(1)), float(m.group(2))
    return ost + HALBE_ZELLE_M, nord + HALBE_ZELLE_M


@lru_cache(maxsize=1)
def _nach_4326():
    from pyproj import Transformer
    return Transformer.from_crs("EPSG:3035", "EPSG:4326", always_xy=True)


@lru_cache(maxsize=1)
def _nach_3035():
    from pyproj import Transformer
    return Transformer.from_crs("EPSG:4326", "EPSG:3035", always_xy=True)


def zellmitte_4326(zellkennung: str) -> tuple[float, float]:
    """Zellmitte als (Länge, Breite) in EPSG:4326."""
    x, y = zellmitte_3035(zellkennung)
    return _nach_4326().transform(x, y)


def gepinnte_flaechen(ags: str) -> dict:
    """Gepinnte Ortsteilgrenzen (Paket 5a); fehlt die Datei, eine leere FeatureCollection."""
    pfad = os.path.join(KALIB, f"ortsteile_{ags}.geojson")
    if not os.path.exists(pfad):
        return {"type": "FeatureCollection", "features": []}
    with open(pfad, encoding="utf-8") as fh:
        return json.load(fh)


def _features(flaechen) -> list[dict]:
    if flaechen is None:
        return []
    if isinstance(flaechen, dict):
        return list(flaechen.get("features") or [])
    return list(flaechen)


def raumzeilen(kommune: Beispielkommune, flaechen=None) -> list[Raumzeile]:
    """#95 je Ortsteil, absolut und je 1.000 Einwohner.

    ``flaechen``: GeoJSON-FeatureCollection (oder Liste von Features) in EPSG:4326 mit den
    Eigenschaften ``name`` und ``admin_level``; ohne Argument die gepinnte Datei der Kommune.
    """
    from shapely.geometry import Point, shape
    from shapely.ops import transform
    from shapely.prepared import prep

    if flaechen is None:
        flaechen = gepinnte_flaechen(kommune.ags)
    gids, cis, _ = zellen(kommune.ags)
    einw = {g: float(ci["pop"]) for g, ci in zip(gids, cis)}
    punkte = {g: Point(zellmitte_4326(g)) for g in gids}

    # Flächen je Ebene, mit Zellen, deren Mitte darin liegt
    kandidaten = []
    for i, f in enumerate(_features(flaechen)):
        p = f.get("properties") or {}
        form = shape(f["geometry"])
        flaeche_m2 = transform(_nach_3035().transform, form).area
        pf = prep(form)
        drin = [g for g in gids if pf.contains(punkte[g])]
        kandidaten.append({
            "i": i, "name": str(p.get("name") or f"Fläche {i + 1}"),
            "ebene": p.get("admin_level"), "osm_relation": p.get("osm_relation"),
            "flaeche_m2": flaeche_m2, "zellen": drin,
        })

    if not kandidaten:
        e = rechne_95(kommune)
        return [_zeile(kommune.name, "gemeinde", None, gids, e)]

    # Eine Ebene je Gemeinde: meiste abgedeckte Einwohner, bei Gleichstand 10
    ebenen = sorted({k["ebene"] for k in kandidaten}, key=lambda x: (x is None, x))

    def abgedeckt(ebene) -> float:
        zs = set().union(*(k["zellen"] for k in kandidaten if k["ebene"] == ebene))
        return sum(einw[g] for g in zs)

    ebene = max(ebenen, key=lambda eb: (abgedeckt(eb), eb == 10))
    gewaehlt = [k for k in kandidaten if k["ebene"] == ebene]

    # Zuordnung: bei Überlappung die kleinere Fläche
    zuordnung: dict[str, int] = {}
    for k in sorted(gewaehlt, key=lambda k: (k["flaeche_m2"], k["i"])):
        for g in k["zellen"]:
            zuordnung.setdefault(g, k["i"])

    zeilen: list[Raumzeile] = []
    for k in gewaehlt:
        eigene = tuple(g for g in gids if zuordnung.get(g) == k["i"])
        if sum(einw[g] for g in eigene) <= 0:
            zeilen.append(Raumzeile(
                name=k["name"], art="ortsteil", ebene=k["ebene"], zellkennungen=eigene,
                einwohner=0.0, einwohner_ab65=0.0, hitzetage=None, todesfaelle=None, yll=None,
                einweisungen=None, jahresbetrag_eur=None, grund=GRUND_OHNE_ZELLE,
                osm_relation=k["osm_relation"]))
            continue
        z = _zeile(k["name"], "ortsteil", k["ebene"], eigene, rechne_95(kommune, eigene))
        z.osm_relation = k["osm_relation"]
        zeilen.append(z)

    rest = tuple(g for g in gids if g not in zuordnung)
    if rest:
        zeilen.append(_zeile(UEBRIG, "uebrig", None, rest, rechne_95(kommune, rest)))
    return zeilen


def _je_1000(wert: float, einwohner: float) -> float | None:
    return wert / einwohner * 1000.0 if einwohner > 0 else None


def _zeile(name: str, art: str, ebene, gids, e) -> Raumzeile:
    return Raumzeile(
        name=name, art=art, ebene=ebene, zellkennungen=tuple(gids),
        einwohner=e.einwohner, einwohner_ab65=e.einwohner_ab65,
        hitzetage=e.hitzetage_mittel, todesfaelle=e.todesfaelle, yll=e.yll,
        einweisungen=e.einweisungen, jahresbetrag_eur=e.jahresbetrag_eur,
        jahresbetrag_je_1000_eur=_je_1000(e.jahresbetrag_eur, e.einwohner),
        todesfaelle_je_1000=_je_1000(e.todesfaelle, e.einwohner),
        einweisungen_je_1000=_je_1000(e.einweisungen, e.einwohner),
    )
