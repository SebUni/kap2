"""BKG VG250: Gemeindegeometrien laden und in die Tabelle ``gemeinden`` schreiben.

Quelle: VG250 GeoPackage (dl-de/by-2-0), Layer ``vg250_gem`` in EPSG:25832.
Das GeoPackage trägt KEINE Einwohner/Fläche inline — die Fläche wird planar aus
der 25832-Geometrie berechnet, die Bevölkerung später aus dem Zensus-Aggregat
(``zensus_gemeinde``) nachgetragen. GF==4 filtert echte Landgemeinden.
"""
from __future__ import annotations

import json
import logging
import os
import zipfile

import httpx
from geoalchemy2.shape import from_shape
from pyproj import Transformer
from shapely import wkb
from shapely.geometry import MultiPolygon, mapping
from shapely.ops import transform as shp_transform
from sqlalchemy.orm import Session

from app.config import settings
from app.models.lite_models import Gemeinde

log = logging.getLogger(__name__)

# SN_L (Landschlüssel) → Bundeslandname
BUNDESLAND_BY_SNL = {
    "01": "Schleswig-Holstein", "02": "Hamburg", "03": "Niedersachsen",
    "04": "Bremen", "05": "Nordrhein-Westfalen", "06": "Hessen",
    "07": "Rheinland-Pfalz", "08": "Baden-Württemberg", "09": "Bayern",
    "10": "Saarland", "11": "Berlin", "12": "Brandenburg",
    "13": "Mecklenburg-Vorpommern", "14": "Sachsen", "15": "Sachsen-Anhalt",
    "16": "Thüringen",
}

_SIMPLIFY_TOL_DEG = 0.0008  # ~80 m — glättet für Artefakt-Export/Tiles


def _gpkg_path() -> str:
    return os.path.join(settings.VG250_CACHE_DIR, "DE_VG250.gpkg")


def ensure_vg250(force: bool = False) -> str:
    """Stellt das entpackte VG250-GeoPackage sicher (Download + Entpacken)."""
    gpkg = _gpkg_path()
    if os.path.exists(gpkg) and not force:
        return gpkg
    os.makedirs(settings.VG250_CACHE_DIR, exist_ok=True)
    zip_path = os.path.join(settings.VG250_CACHE_DIR, "vg250.zip")
    if not os.path.exists(zip_path) or os.path.getsize(zip_path) < 1_000_000:
        log.info("Lade VG250 von %s", settings.VG250_GPKG_URL)
        with httpx.stream("GET", settings.VG250_GPKG_URL,
                          timeout=settings.LITE_DOWNLOAD_TIMEOUT_S,
                          follow_redirects=True) as r:
            r.raise_for_status()
            with open(zip_path, "wb") as fh:
                for chunk in r.iter_bytes(1 << 20):
                    fh.write(chunk)
    with zipfile.ZipFile(zip_path) as z:
        inner = next(n for n in z.namelist() if n.endswith("DE_VG250.gpkg"))
        with z.open(inner) as src, open(gpkg, "wb") as dst:
            while chunk := src.read(1 << 20):
                dst.write(chunk)
    log.info("VG250-GeoPackage bereit: %s", gpkg)
    return gpkg


def _read_features(gpkg: str):
    """Yield (ags, name, bez, bundesland, shapely_geom_25832) je Landgemeinde."""
    import pyogrio.raw as raw

    meta, _, geoms, fields = raw.read(
        gpkg, layer="vg250_gem", columns=["AGS", "GEN", "BEZ", "GF", "SN_L"],
    )
    names = list(meta["fields"])
    col = {n: fields[i] for i, n in enumerate(names)}
    for i in range(len(geoms)):
        gf = col["GF"][i]
        try:
            gf_int = int(gf)
        except (TypeError, ValueError):
            gf_int = None
        if gf_int != 4:  # nur „mit Struktur Land"
            continue
        ags = str(col["AGS"][i] or "").strip()
        if len(ags) != 8:
            continue
        geom = wkb.loads(bytes(geoms[i]))
        if geom.geom_type == "Polygon":
            geom = MultiPolygon([geom])
        yield (
            ags,
            str(col["GEN"][i] or "").strip(),
            str(col["BEZ"][i] or "").strip(),
            BUNDESLAND_BY_SNL.get(str(col["SN_L"][i] or "").zfill(2)),
            geom,
        )


def ingest_gemeinden(db: Session, bundesland: str | None = None) -> int:
    """VG250 → ``gemeinden`` (Upsert nach AGS). Optional auf ein Bundesland
    gefiltert (Testläufe). Gibt die Zahl geschriebener Gemeinden zurück."""
    gpkg = ensure_vg250()
    to_4326 = Transformer.from_crs("EPSG:25832", "EPSG:4326", always_xy=True)
    stand = "2024"  # VG250-Ausgabe 01-01

    existing = {g.ags for g in db.query(Gemeinde.ags).all()}
    written = 0
    batch = 0
    for ags, name, bez, bl, geom25832 in _read_features(gpkg):
        if bundesland and bl != bundesland:
            continue
        area_km2 = round(geom25832.area / 1_000_000.0, 3)  # planar, 25832 in m
        geom4326 = shp_transform(lambda x, y, z=None: to_4326.transform(x, y), geom25832)
        rep = geom4326.representative_point()
        simplified = geom4326.simplify(_SIMPLIFY_TOL_DEG, preserve_topology=True)

        values = dict(
            name=name, bez=bez, bundesland=bl, area_km2=area_km2,
            geometry=from_shape(geom4326, srid=4326),
            geometry_simplified=json.dumps(mapping(simplified)),
            rep_lon=round(rep.x, 6), rep_lat=round(rep.y, 6),
            vg250_stand=stand,
        )
        if ags in existing:
            db.query(Gemeinde).filter(Gemeinde.ags == ags).update(values)
        else:
            db.add(Gemeinde(ags=ags, **values))
            existing.add(ags)
        written += 1
        batch += 1
        if batch >= 500:
            db.commit()
            batch = 0
    db.commit()
    log.info("VG250-Ingest: %d Gemeinden geschrieben%s", written,
             f" (nur {bundesland})" if bundesland else "")
    return written
