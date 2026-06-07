"""Zensus 2022 INSPIRE 100m grid: autoload, parse, bbox-filtered lookup."""

from __future__ import annotations

import csv
import io
import logging
import math
import os
import re
import tempfile
import zipfile
from dataclasses import dataclass, field
from typing import Any
from urllib.request import Request, urlopen

from shapely.geometry import box
from shapely.ops import transform
import pyproj

from app.config import settings

log = logging.getLogger(__name__)

MISSING_MARKERS = {"–", "-", "", "…", "..."}
BUILDING_AGE_CLASSES: list[tuple[str, int]] = [
    ("Vor1919", 1900),
    ("a1919bis1949", 1934),
    ("a1950bis1959", 1954),
    ("a1960bis1969", 1964),
    ("a1970bis1979", 1974),
    ("a1980bis1989", 1984),
    ("a1990bis1999", 1994),
    ("a2000bis2009", 2004),
    ("a2010bis2015", 2012),
    ("a2016undspaeter", 2020),
]

REQUIRED_KEYS = (
    "population",
    "share_over_65",
    "share_under_18",
    "living_area_per_person",
    "owner_share",
    "net_cold_rent",
    "building_age",
)

OPTIONAL_KEYS = ("avg_age", "avg_household_size")


@dataclass
class ZensusDatasetDef:
    key: str
    zip_url: str
    csv_glob: str  # substring to find 100m csv in zip
    csv_filename: str  # expected local filename
    required: bool = True
    value_columns: list[str] = field(default_factory=list)


ZENSUS_DATASETS: dict[str, ZensusDatasetDef] = {
    "population": ZensusDatasetDef(
        key="population",
        zip_url="https://www.destatis.de/static/DE/zensus/gitterdaten/Zensus2022_Bevoelkerungszahl.zip",
        csv_glob="100m",
        csv_filename="Zensus2022_Bevoelkerungszahl_100m-Gitter.csv",
        value_columns=["Einwohner"],
    ),
    "share_over_65": ZensusDatasetDef(
        key="share_over_65",
        zip_url="https://www.destatis.de/static/DE/zensus/gitterdaten/Anteil_ab_65-jaehrige_in_Gitterzellen.zip",
        csv_glob="100m",
        csv_filename="Zensus2022_Anteil_ueber_65_100m-Gitter.csv",
        value_columns=["AnteilUeber65"],
    ),
    "share_under_18": ZensusDatasetDef(
        key="share_under_18",
        zip_url="https://www.destatis.de/static/DE/zensus/gitterdaten/Anteil_unter_18-jaehrige_in_Gitterzellen.zip",
        csv_glob="100m",
        csv_filename="Zensus2022_Anteil_unter_18_100m-Gitter.csv",
        value_columns=["AnteilUnter18"],
    ),
    "living_area_per_person": ZensusDatasetDef(
        key="living_area_per_person",
        zip_url="https://www.destatis.de/static/DE/zensus/gitterdaten/Durchschnittliche_Wohnflaeche_je_Bewohner_in_Gitterzellen.zip",
        csv_glob="100m",
        csv_filename="Zensus2022_Durchschn_Flaeche_je_Bewohner_100m-Gitter.csv",
        value_columns=["durchschnFlaechejeBew"],
    ),
    "owner_share": ZensusDatasetDef(
        key="owner_share",
        zip_url="https://www.destatis.de/static/DE/zensus/gitterdaten/Eigentuemerquote_in_Gitterzellen.zip",
        csv_glob="100m",
        csv_filename="Zensus2022_Eigentuemerquote_100m-Gitter.csv",
        value_columns=["Eigentuemerquote"],
    ),
    "net_cold_rent": ZensusDatasetDef(
        key="net_cold_rent",
        zip_url="https://www.destatis.de/static/DE/zensus/gitterdaten/Zensus2022_Durchschn_Nettokaltmiete.zip",
        csv_glob="100m",
        csv_filename="Zensus2022_Durchschn_Nettokaltmiete_100m-Gitter.csv",
        value_columns=["durchschnMieteQM"],
    ),
    "building_age": ZensusDatasetDef(
        key="building_age",
        zip_url="https://www.destatis.de/static/DE/zensus/gitterdaten/Gebaeude_nach_Baujahr_in_Mikrozensus_Klassen.zip",
        csv_glob="100m",
        csv_filename="Zensus2022_Baujahr_JZ_100m-Gitter.csv",
        value_columns=["Insgesamt_Gebaeude"] + [c[0] for c in BUILDING_AGE_CLASSES],
    ),
    "avg_age": ZensusDatasetDef(
        key="avg_age",
        zip_url="https://www.destatis.de/static/DE/zensus/gitterdaten/Durchschnittsalter_in_Gitterzellen.zip",
        csv_glob="100m",
        csv_filename="Zensus2022_Durchschnittsalter_100m-Gitter.csv",
        required=False,
        value_columns=["Durchschnittsalter"],
    ),
    "avg_household_size": ZensusDatasetDef(
        key="avg_household_size",
        zip_url="https://www.destatis.de/static/DE/zensus/gitterdaten/Durchschnittliche_Haushaltsgroesse_in_Gitterzellen.zip",
        csv_glob="100m",
        csv_filename="Zensus2022_Durchschn_Haushaltsgroesse_100m-Gitter.csv",
        required=False,
        value_columns=["DurchschnHHGroesse"],
    ),
}

_bbox_cache: dict[str, dict[str, dict[str, Any]]] = {}


def _dataset_dir(key: str) -> str:
    return os.path.join(settings.ZENSUS_DATA_DIR, "extract", key)


def _dataset_path(key: str) -> str:
    d = ZENSUS_DATASETS[key]
    return os.path.join(_dataset_dir(key), d.csv_filename)


def _parse_float(raw: str | None) -> float | None:
    if raw is None:
        return None
    s = str(raw).strip()
    if s in MISSING_MARKERS:
        return None
    s = s.replace(".", "").replace(",", ".") if "," in s and s.count(",") == 1 else s.replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return None


def _parse_int(raw: str | None) -> int | None:
    v = _parse_float(raw)
    if v is None:
        return None
    return int(v)


def _gitter_id_from_row(row: dict) -> str | None:
    for k in ("GITTER_ID_100m", "GITTER_ID_100M", "gitter_id_100m"):
        if row.get(k):
            return str(row[k]).strip()
    x = _parse_int(row.get("x_mp_100m"))
    y = _parse_int(row.get("y_mp_100m"))
    if x is not None and y is not None:
        x0 = x - 50
        y0 = y - 50
        return f"CRS3035RES100mN{y0}E{x0}"
    return None


def _is_suppressed(row: dict) -> bool:
    flag = (row.get("werterlaeuternde_Zeichen") or "").strip()
    return flag == "KLAMMERN"


def is_dataset_ready(key: str, *, min_bytes: int = 10_000) -> bool:
    path = _dataset_path(key)
    if not os.path.isfile(path) or os.path.getsize(path) < min_bytes:
        return False
    try:
        with open(path, encoding="utf-8") as f:
            header = f.readline()
        return "GITTER_ID" in header or "x_mp_100m" in header
    except OSError:
        return False


def _download_zip(url: str, dest: str) -> None:
    req = Request(url, headers={"User-Agent": settings.ZENSUS_USER_AGENT})
    with urlopen(req, timeout=settings.ZENSUS_DOWNLOAD_TIMEOUT_S) as resp:
        data = resp.read()
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "wb") as f:
        f.write(data)


def _extract_100m_csv(zip_path: str, dest_csv: str, csv_hint: str) -> None:
    with zipfile.ZipFile(zip_path) as zf:
        candidates = [
            n for n in zf.namelist()
            if n.lower().endswith(".csv") and "100m" in n.lower()
        ]
        if not candidates:
            candidates = [n for n in zf.namelist() if n.lower().endswith(".csv")]
        if not candidates:
            raise ValueError(f"Keine CSV in ZIP: {zip_path}")
        name = next((n for n in candidates if csv_hint.lower() in n.lower()), candidates[0])
        raw = zf.read(name)
    os.makedirs(os.path.dirname(dest_csv), exist_ok=True)
    tmp = dest_csv + ".tmp"
    with open(tmp, "wb") as f:
        f.write(raw)
    os.replace(tmp, dest_csv)


def ensure_zensus_dataset(key: str) -> str:
    """Ensure local CSV exists; download from Destatis if needed. Returns path."""
    if key not in ZENSUS_DATASETS:
        raise KeyError(f"Unbekannter Zensus-Datensatz: {key}")

    path = _dataset_path(key)
    if is_dataset_ready(key) and not settings.ZENSUS_FORCE_REFRESH:
        return path

    if not settings.ZENSUS_AUTO_DOWNLOAD:
        raise FileNotFoundError(
            f"Zensus-Datensatz '{key}' fehlt unter {path} und ZENSUS_AUTO_DOWNLOAD=false"
        )

    d = ZENSUS_DATASETS[key]
    log.info("Lade Zensus-Datensatz '%s' von Destatis …", key)
    with tempfile.TemporaryDirectory() as tmpdir:
        zip_path = os.path.join(tmpdir, f"{key}.zip")
        _download_zip(d.zip_url, zip_path)
        _extract_100m_csv(zip_path, path, d.csv_filename)
    log.info("Zensus '%s' gespeichert: %s (%d bytes)", key, path, os.path.getsize(path))
    _bbox_cache.pop(key, None)
    return path


def ensure_zensus_datasets(keys: list[str] | None = None) -> list[str]:
    keys = list(keys or REQUIRED_KEYS)
    paths = []
    for key in keys:
        paths.append(ensure_zensus_dataset(key))
    return paths


def bbox_3035_from_wgs_geoms(geoms: list) -> tuple[int, int, int, int]:
    proj_wgs = pyproj.CRS("EPSG:4326")
    proj_laea = pyproj.CRS(f"EPSG:{settings.ZENSUS_SRID}")
    to_laea = pyproj.Transformer.from_crs(proj_wgs, proj_laea, always_xy=True)
    laea_geoms = [transform(to_laea.transform, g) for g in geoms]
    combined = laea_geoms[0]
    for g in laea_geoms[1:]:
        combined = combined.union(g)
    minx, miny, maxx, maxy = combined.bounds
    pad = 100
    return (
        int(math.floor(minx)) - pad,
        int(math.floor(miny)) - pad,
        int(math.ceil(maxx)) + pad,
        int(math.ceil(maxy)) + pad,
    )


def load_dataset_bbox(key: str, bbox: tuple[int, int, int, int]) -> dict[str, dict[str, Any]]:
    """Load rows whose centroid falls in bbox. Cached per (key, bbox)."""
    cache_key = f"{key}:{bbox}"
    if cache_key in _bbox_cache.get(key, {}):
        return _bbox_cache[key][cache_key]

    path = ensure_zensus_dataset(key)
    xmin, ymin, xmax, ymax = bbox
    out: dict[str, dict[str, Any]] = {}

    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            x = _parse_int(row.get("x_mp_100m"))
            y = _parse_int(row.get("y_mp_100m"))
            if x is None or y is None:
                continue
            if not (xmin <= x <= xmax and ymin <= y <= ymax):
                continue
            gid = _gitter_id_from_row(row)
            if not gid:
                continue
            if _is_suppressed(row):
                out[gid] = {"suppressed": True}
                continue
            parsed: dict[str, Any] = {"x": x, "y": y}
            d = ZENSUS_DATASETS[key]
            for col in d.value_columns:
                if col == "Insgesamt_Gebaeude":
                    parsed[col] = _parse_int(row.get(col))
                elif col in {c[0] for c in BUILDING_AGE_CLASSES}:
                    parsed[col] = _parse_int(row.get(col))
                else:
                    parsed[col] = _parse_float(row.get(col))
            if key == "building_age":
                parsed["building_age_mean"] = _mean_building_year(parsed)
            out[gid] = parsed

    _bbox_cache.setdefault(key, {})[cache_key] = out
    return out


def _mean_building_year(parsed: dict[str, Any]) -> float | None:
    total = parsed.get("Insgesamt_Gebaeude") or 0
    if total <= 0:
        return None
    weighted = 0.0
    count = 0
    for col, mid_year in BUILDING_AGE_CLASSES:
        n = parsed.get(col)
        if n is None or n <= 0:
            continue
        weighted += n * mid_year
        count += n
    if count <= 0:
        return None
    return weighted / count


def load_zensus_for_cells(
    grid_cells: list[dict],
    keys: list[str] | None = None,
) -> dict[str, dict[str, dict[str, Any]]]:
    """Load all Zensus datasets for the bbox of grid cells."""
    keys = list(keys or REQUIRED_KEYS)
    geoms = [c["geometry"] for c in grid_cells]
    bbox = bbox_3035_from_wgs_geoms(geoms)
    return {key: load_dataset_bbox(key, bbox) for key in keys}


def apply_zensus_to_cell_inputs(
    cell_inputs: list[dict],
    grid_cells: list[dict],
    zensus: dict[str, dict[str, dict[str, Any]]] | None = None,
) -> None:
    """Set Zensus fields on each cell_input in-place."""
    if zensus is None:
        zensus = load_zensus_for_cells(grid_cells)

    gid_by_idx = {i: grid_cells[i].get("gitter_id") for i in range(len(grid_cells))}
    pop_data = zensus.get("population", {})
    over65 = zensus.get("share_over_65", {})
    under18 = zensus.get("share_under_18", {})
    living = zensus.get("living_area_per_person", {})
    owner = zensus.get("owner_share", {})
    rent = zensus.get("net_cold_rent", {})
    bage = zensus.get("building_age", {})

    for idx, ci in enumerate(cell_inputs):
        gid = gid_by_idx.get(idx) or ci.get("gitter_id")
        if not gid:
            continue

        p = pop_data.get(gid, {})
        if p.get("suppressed"):
            ci["pop"] = 0.0
        else:
            ci["pop"] = float(p.get("Einwohner") or 0.0)

        o65 = over65.get(gid, {})
        u18 = under18.get(gid, {})
        ci["share_over_65"] = None if o65.get("suppressed") else o65.get("AnteilUeber65")
        ci["share_under_18"] = None if u18.get("suppressed") else u18.get("AnteilUnter18")

        la = living.get(gid, {})
        ow = owner.get(gid, {})
        rt = rent.get(gid, {})
        ba = bage.get(gid, {})

        ci["living_area_per_person"] = None if la.get("suppressed") else la.get("durchschnFlaechejeBew")
        ci["owner_share"] = None if ow.get("suppressed") else ow.get("Eigentuemerquote")
        ci["net_cold_rent"] = None if rt.get("suppressed") else rt.get("durchschnMieteQM")
        ci["building_count_zensus"] = None if ba.get("suppressed") else ba.get("Insgesamt_Gebaeude")
        ci["building_age_mean"] = None if ba.get("suppressed") else ba.get("building_age_mean")
        ci["gitter_id"] = gid

        share_o = ci.get("share_over_65") or 0.0
        share_u = ci.get("share_under_18") or 0.0
        ci["share_vulnerable"] = min(100.0, share_o + share_u)
        pop = ci.get("pop") or 0.0
        ci["pop_over_65"] = pop * share_o / 100.0 if pop > 0 else 0.0
        ci["pop_under_18"] = pop * share_u / 100.0 if pop > 0 else 0.0


def demographic_shares() -> dict:
    """Fallback demografie (nur wenn Zensus-Zelle fehlt)."""
    from app.services.zensus_service import NATIONAL_DEMOGRAPHICS
    d = dict(NATIONAL_DEMOGRAPHICS)
    d["share_under_18"] = 18.0
    d.pop("share_under_6", None)
    return d
