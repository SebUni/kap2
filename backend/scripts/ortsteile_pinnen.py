"""Gepinnte Ortsteilgrenzen einer Gemeinde aus OpenStreetMap (PDF-Ergebnisbericht, Paket 5a von T-1418-cto).

Fragt über Overpass (``config.OVERPASS_URL``) alle Relationen ``boundary=administrative`` mit ``admin_level``
9 oder 10 im Rechteck um die Gemeinde ab, setzt ihre Flächen aus den Wegen zusammen (``_merge_rings`` aus
``app/services/osm_service.py``) und übernimmt nur Flächen, die zu mindestens 50 % in der Gemeindegrenze aus
VG250 liegen (Loader und Adresse wie in ``golden_95_zelldaten.py``: ``gemeindegebiet`` aus
``docs/methodik/anlagen/95_zellvergleich.py``, ``config.VG250_GPKG_URL``). Beide Ebenen werden gepinnt; welche
der Bericht zeigt, entscheidet Paket 2.

Ergebnis: ``backend/data/kalibrierung/ortsteile_<AGS>.geojson``, eine FeatureCollection in EPSG:4326 mit den
Kopfangaben ``stand_osm_base`` (``osm3s.timestamp_osm_base`` der Overpass-Antwort) und ``abgerufen`` (Datum).
Je Feature: ``name``, ``admin_level``, ``osm_relation``, ``anteil_in_gemeinde``. Findet OSM keine Fläche, ist
das Ergebnis eine leere FeatureCollection; eigene Grenzen werden nicht erfunden.

Aufruf (aus dem Repo-Wurzelverzeichnis, Interpreter der Projektumgebung):
    ~/.venvs/kap2/bin/python backend/scripts/ortsteile_pinnen.py --gemeinde 03256034 [--cache VERZEICHNIS]
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import httpx
from shapely.geometry import MultiPolygon, Polygon, mapping
from shapely.ops import transform, unary_union

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "backend"))

from app.config import settings  # noqa: E402
from app.services.osm_service import _merge_rings  # noqa: E402

ZELLVERGLEICH = REPO / "docs" / "methodik" / "anlagen" / "95_zellvergleich.py"
ZIEL = REPO / "backend" / "data" / "kalibrierung"
MINDESTANTEIL = 0.5
RAND_GRAD = 0.02  # Rand um das Gemeinderechteck für die Abfrage (rund 2 km)
# overpass-api.de lehnt Anfragen ohne eigenen User-Agent mit HTTP 406 ab.
USER_AGENT = "kap3-ortsteile-pinnen/1.0"


def _zellvergleich():
    spec = importlib.util.spec_from_file_location("zellvergleich_95", ZELLVERGLEICH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _overpass(query: str) -> dict:
    resp = httpx.post(settings.OVERPASS_URL, data={"data": query},
                      headers={"User-Agent": USER_AGENT}, timeout=180.0)
    resp.raise_for_status()
    return resp.json()


def _ringe(members: list, rolle: str) -> list[list]:
    teile = [[(pt["lon"], pt["lat"]) for pt in m["geometry"]]
             for m in members if m.get("type") == "way" and m.get("role", "") == rolle and m.get("geometry")]
    return [r for r in _merge_rings(teile) if len(r) >= 4]


def flaeche_aus_relation(element: dict):
    """Fläche (EPSG:4326) aus einer Relation mit ``out geom``: äußere und innere Ringe zusammensetzen,
    jeden inneren Ring der äußeren Fläche zuordnen, in der er liegt."""
    members = element.get("members", [])
    aussen = [Polygon(r).buffer(0) for r in _ringe(members, "outer")]
    aussen = [p for p in aussen if not p.is_empty]
    if not aussen:
        return None
    flaeche = unary_union(aussen)
    for r in _ringe(members, "inner"):
        loch = Polygon(r).buffer(0)
        if not loch.is_empty:
            flaeche = flaeche.difference(loch)
    if flaeche.is_empty:
        return None
    if isinstance(flaeche, Polygon):
        return flaeche
    teile = [g for g in getattr(flaeche, "geoms", []) if isinstance(g, Polygon)]
    return MultiPolygon(teile) if teile else None


def _runden(geom, stellen: int = 7):
    def r(x, y, z=None):
        return round(x, stellen), round(y, stellen)
    return transform(r, geom)


def ortsteile_pinnen(zv, ags: str, cache: Path) -> Path:
    config = zv.REPO / "backend" / "app" / "config.py"
    vg250_url = zv._literal_aus_datei(config, "VG250_GPKG_URL")
    polys, name, stand_vg250 = zv.gemeindegebiet(ags, cache, vg250_url)

    def utm_zu_geo(x, y, z=None):
        return zv.UTM32.zurueck(x, y)

    def geo_zu_utm(lon, lat, z=None):
        return zv.UTM32.vor(lon, lat)

    gemeinde_utm = unary_union([Polygon(p[0], p[1:]).buffer(0) for p in polys])
    lon_min, lat_min, lon_max, lat_max = transform(utm_zu_geo, gemeinde_utm).bounds
    s, w, n, o = lat_min - RAND_GRAD, lon_min - RAND_GRAD, lat_max + RAND_GRAD, lon_max + RAND_GRAD
    query = (f'[out:json][timeout:120];'
             f'rel["boundary"="administrative"]["admin_level"~"^(9|10)$"]({s:.5f},{w:.5f},{n:.5f},{o:.5f});'
             f'out geom;')
    antwort = _overpass(query)
    stand_osm = antwort["osm3s"]["timestamp_osm_base"]

    features = []
    for el in antwort.get("elements", []):
        if el.get("type") != "relation":
            continue
        tags = el.get("tags", {})
        flaeche = flaeche_aus_relation(el)
        if flaeche is None or not tags.get("name", "").strip():
            continue
        flaeche_utm = transform(geo_zu_utm, flaeche)
        if flaeche_utm.area <= 0:
            continue
        anteil = flaeche_utm.intersection(gemeinde_utm).area / flaeche_utm.area
        if anteil < MINDESTANTEIL:
            continue
        features.append({
            "type": "Feature",
            "properties": {
                "name": tags["name"].strip(),
                "admin_level": int(tags["admin_level"]),
                "osm_relation": int(el["id"]),
                "anteil_in_gemeinde": round(anteil, 4),
                "flaeche_km2": round(flaeche_utm.area / 1e6, 3),
            },
            "geometry": mapping(_runden(flaeche)),
        })
    features.sort(key=lambda f: (f["properties"]["admin_level"], f["properties"]["name"],
                                 f["properties"]["osm_relation"]))

    daten = {
        "type": "FeatureCollection",
        "name": f"ortsteile_{ags}",
        "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}},
        "gemeinde": {"ags": ags, "name": name, "vg250_stand": stand_vg250},
        "quelle": "OpenStreetMap über Overpass API",
        "lizenz": "ODbL 1.0, © OpenStreetMap-Mitwirkende",
        "stand_osm_base": stand_osm,
        "abgerufen": datetime.now(timezone.utc).date().isoformat(),
        "mindestanteil_in_gemeinde": MINDESTANTEIL,
        "features": features,
    }
    ziel = ZIEL / f"ortsteile_{ags}.geojson"
    ziel.write_text(json.dumps(daten, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    ebenen = {lv: sum(1 for f in features if f["properties"]["admin_level"] == lv) for lv in (9, 10)}
    print(f"{ags} {name} (VG250 {stand_vg250}, OSM {stand_osm}): {len(features)} Flächen "
          f"(Ebene 9: {ebenen[9]}, Ebene 10: {ebenen[10]}) -> {ziel.relative_to(REPO)}")
    for f in features:
        p = f["properties"]
        print(f"  {p['admin_level']:>2}  r{p['osm_relation']:<10} {p['anteil_in_gemeinde']:.4f}  {p['name']}")
    return ziel


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--gemeinde", action="append", required=True, help="AGS (8 Stellen), mehrfach")
    ap.add_argument("--cache", default=os.environ.get("KAP3_CACHE",
                                                      str(Path.home() / ".cache" / "kap3" / "95_zellvergleich")))
    args = ap.parse_args()
    zv = _zellvergleich()
    for ags in args.gemeinde:
        ortsteile_pinnen(zv, ags.strip(), Path(args.cache).expanduser())


if __name__ == "__main__":
    main()
