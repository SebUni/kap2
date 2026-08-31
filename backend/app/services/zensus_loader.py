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
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from typing import Any
from urllib.request import Request, urlopen

from shapely.geometry import box
from shapely.ops import transform
import pyproj

from app.config import settings

log = logging.getLogger(__name__)

# Destatis-Wertekennzeichen. Der Gedankenstrich „–"/„-" bedeutet **genau Null**
# (nichts vorhanden / auf Null geändert) → als 0 hinterlegen, NICHT als fehlend.
# Nur echt fehlende/geheime Werte („…", leer) werden zu None.
ZERO_MARKERS = {"–", "-"}
MISSING_MARKERS = {"", "…", "..."}
# Spaltennamen gemäß Destatis CSV „Gebaeude_nach_Baujahr_in_Mikrozensus_Klassen“
BUILDING_AGE_CLASSES: list[tuple[str, int]] = [
    ("Vor1919", 1900),
    ("a1919bis1948", 1933),
    ("a1949bis1978", 1963),
    ("a1979bis1990", 1984),
    ("a1991bis2000", 1995),
    ("a2001bis2010", 2005),
    ("a2011bis2019", 2015),
    ("a2020undspaeter", 2022),
]

# Zensus-2022-Altersgruppen im 100-m-Gitter (5-Jahres-Klassen) → die vier
# Altersbänder der RKI-/Winklmayr-Expositions-Wirkungs-Kurven.
#
# WICHTIG — abweichende Bedeutung von „–" in diesem Datensatz: Destatis
# unterdrückt Besetzungszahlen < 3, der kleinste je publizierte Bandwert ist 3
# (verifiziert 2026-08-02 über alle 3.088.037 Zellen: Werte 0/1/2 kommen nicht
# vor). „–" heißt hier also „0, 1 oder 2" und NICHT „genau Null" wie in den
# übrigen Zensus-Datensätzen. Die Bandsummen decken deshalb nur 89,8 % der
# Bevölkerung ab (100 % in Zellen ≥150 Ew., 30 % in Zellen <10 Ew.).
#
# Zusätzlich sind Bänder und ``Insgesamt_Bevoelkerung`` NICHT additiv konsistent
# (Destatis perturbiert beide unabhängig; 875.414 Zellen haben ein negatives
# Residuum). Ein „Restbevölkerung = Insgesamt − Σ Bänder" ist daher nicht
# rekonstruierbar.
#
# Konsequenz für die Nutzung: Die Bänder liefern ausschließlich die
# **Zusammensetzung**, das **Niveau** kommt aus dem ``population``-Datensatz.
# Das ist messbar korrekt — der 65+-Anteil an der Bevölkerung beträgt in den
# rohen Bandsummen nur 19,6 %, der 65+-Anteil *innerhalb* der Bänder aber
# 21,9 % und trifft damit den amtlichen Wert (~22 %).
AGE_BAND_COLUMNS: dict[str, tuple[str, ...]] = {
    "u65": ("unter5", "a5bis9", "a10bis14", "a15bis19", "a20bis24", "a25bis29",
            "a30bis34", "a35bis39", "a40bis44", "a45bis49", "a50bis54",
            "a55bis59", "a60bis64"),
    "a65_74": ("a65bis69", "a70bis74"),
    "a75_84": ("a75bis79", "a80bis84"),
    "a85p": ("a85bis89", "a90undaelter"),
}
ALL_AGE_COLUMNS: tuple[str, ...] = tuple(
    c for cols in AGE_BAND_COLUMNS.values() for c in cols
)
# Unterhalb dieses Deckungsgrades (Σ Bänder / Einwohner) ist die Zusammensetzung
# der Zelle zu stark von der Unterdrückung verzerrt → regionaler Rückfall.
AGE_BAND_MIN_COVERAGE = 0.5

REQUIRED_KEYS = (
    "population",
    "share_over_65",
    "share_under_18",
    "living_area_per_person",
    "owner_share",
    "net_cold_rent",
    "building_age",
)

OPTIONAL_KEYS = ("avg_age", "avg_household_size", "age_groups")

# Beim Assessment tatsächlich geladene Datensätze: alle Pflichtdatensätze plus
# die Altersgruppen (optional, mit Rückfall auf die gebietsweite Aufteilung).
DEFAULT_LOAD_KEYS = (*REQUIRED_KEYS, "age_groups")


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
    # 5-Jahres-Altersgruppen — Grundlage der altersgeschichteten Hitzemortalität.
    # ``required=False``: fällt der Download aus, greift der Rückfall über
    # ``share_over_65`` (siehe ``_age_bands_from_share``), statt das Assessment
    # zu blockieren. Siehe AGE_BAND_COLUMNS zur Unterdrückungs-Semantik.
    "age_groups": ZensusDatasetDef(
        key="age_groups",
        zip_url="https://www.destatis.de/static/DE/zensus/gitterdaten/Alter_5er-Jahresgruppen_100mGitter.zip",
        csv_glob="100m",
        csv_filename="Zensus2022_Alter_5er-Jahresgruppen_100m-Gitter.csv",
        required=False,
        value_columns=["Insgesamt_Bevoelkerung", *ALL_AGE_COLUMNS],
    ),
}

# In-RAM-Zellcache: je Dataset nur EIN bbox-Eintrag (Within-Run-Sharing);
# über Läufe hinweg dienen die CSVs auf Platte als Quelle (Streaming-Read).
_bbox_cache: dict[str, dict[str, dict[str, Any]]] = {}


def clear_bbox_cache() -> None:
    """Leert den In-RAM-Zellcache (Aufräumen am Ende eines Assessment-Laufs)."""
    _bbox_cache.clear()


def _dataset_dir(key: str) -> str:
    return os.path.join(settings.ZENSUS_DATA_DIR, "extract", key)


def _dataset_path(key: str) -> str:
    d = ZENSUS_DATASETS[key]
    return os.path.join(_dataset_dir(key), d.csv_filename)


def _parse_float(raw: str | None, *, dash_zero: bool = False) -> float | None:
    if raw is None:
        return None
    s = str(raw).strip()
    if s in ZERO_MARKERS:
        # „–" = genau Null: bei Messwerten 0, bei IDs/Koordinaten weiterhin fehlend.
        return 0.0 if dash_zero else None
    if s in MISSING_MARKERS:
        return None
    s = s.replace(".", "").replace(",", ".") if "," in s and s.count(",") == 1 else s.replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return None


def _parse_int(raw: str | None, *, dash_zero: bool = False) -> int | None:
    v = _parse_float(raw, dash_zero=dash_zero)
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


def _is_statistically_uncertain(row: dict) -> bool:
    """KLAMMERN = eingeschränkte Aussagekraft, Wert wird trotzdem veröffentlicht."""
    return (row.get("werterlaeuternde_Zeichen") or "").strip() == "KLAMMERN"


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


def dataset_mtime(key: str) -> float | None:
    """mtime der lokalen CSV (None = fehlt) — Änderungsdetektion für /zensus/sync."""
    try:
        return os.path.getmtime(_dataset_path(key))
    except OSError:
        return None


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
    workers = min(len(keys), 4)
    with ThreadPoolExecutor(max_workers=workers) as ex:
        paths = list(ex.map(ensure_zensus_dataset, keys))
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
            parsed: dict[str, Any] = {"x": x, "y": y}
            uncertain = _is_statistically_uncertain(row)
            if uncertain:
                parsed["statistically_uncertain"] = True
            d = ZENSUS_DATASETS[key]
            # „–" = genau Null bei Zähl-/Anteilsgrößen (0 Personen, 0 % Anteil, 0 Gebäude).
            # Bei Durchschnittswerten (Nettokaltmiete, Wohnfläche/Person) bedeutet „–"
            # mangels Fällen „kein Wert" (nicht 0 €/m²) → weiterhin None, damit der
            # Resilienz-Index nicht durch implausible Nullen verzerrt wird.
            dz = key not in ("net_cold_rent", "living_area_per_person")
            for col in d.value_columns:
                if col == "Insgesamt_Gebaeude":
                    parsed[col] = _parse_int(row.get(col), dash_zero=True)
                elif col in {c[0] for c in BUILDING_AGE_CLASSES}:
                    parsed[col] = _parse_int(row.get(col), dash_zero=True)
                else:
                    parsed[col] = _parse_float(row.get(col), dash_zero=dz)
            if key == "building_age":
                parsed["building_age_mean"] = _mean_building_year(parsed)
            # „–" ist jetzt 0 (genau Null, wird behalten); nur echt fehlende/geheime
            # Werte („…"/leer → None) lassen die Zelle entfallen.
            if key != "building_age" and key != "population":
                primary = d.value_columns[0]
                if parsed.get(primary) is None:
                    continue
            out[gid] = parsed

    _bbox_cache[key] = {cache_key: out}  # Single-Entry je Dataset (RAM-Deckel)
    return out


def _senior_band_counts(parsed: dict[str, Any]) -> dict[str, float]:
    """Veröffentlichte Besetzungszahlen der drei Senioren-Bänder einer Zelle."""
    out: dict[str, float] = {}
    for band in ("a65_74", "a75_84", "a85p"):
        out[band] = sum(
            float(parsed.get(col) or 0.0) for col in AGE_BAND_COLUMNS[band]
        )
    return out


# Nationale Binnenaufteilung der 65+-Bevölkerung, direkt aus dem Zensus-Gitter
# aggregiert (2026-08-02: 8.109.078 / 5.761.381 / 2.336.663 = 16.207.122).
# Letzter Rückfall, wenn weder Zelle noch Gebiet genug besetzte Bänder haben.
NATIONAL_SENIOR_SPLIT: dict[str, float] = {
    "a65_74": 0.5003, "a75_84": 0.3555, "a85p": 0.1442,
}

# ── Band u20 (Methodik #96 §3.2: Prävalenz-Schichtung braucht u20, nicht u18) ──
# Die 5-Jahres-Gruppen des Zensus liefern u20 direkt; wie beim Senioren-Split
# legt die gut besetzte Menge (hier: u65) das Niveau fest und die 5-Jahres-
# Gruppen nur die Binnenaufteilung u20 / 20–64.
U20_COLUMNS: tuple[str, ...] = ("unter5", "a5bis9", "a10bis14", "a15bis19")

# Nationaler u20-Anteil AN DER u65-BEVÖLKERUNG (Bevölkerung 31.12.2023,
# Destatis 12411: u20 15.583.456 / u65 64.747.448 = 0,2407) — letzter Rückfall.
NATIONAL_U20_SHARE_OF_U65: float = 0.2407


def _u20_share_of_u65(parsed: dict[str, Any], fallback: float) -> float:
    """Anteil u20 an u65 aus den 5-Jahres-Gruppen der Zelle (sonst ``fallback``)."""
    u20 = sum(float(parsed.get(col) or 0.0) for col in U20_COLUMNS)
    u65 = sum(float(parsed.get(col) or 0.0) for col in AGE_BAND_COLUMNS["u65"])
    if u65 <= 0.0:
        return fallback
    return max(0.0, min(1.0, u20 / u65))


def _area_u20_share(ages: dict[str, dict[str, Any]]) -> float:
    """Gebietsweiter u20-Anteil an u65 als Rückfall für dünn besetzte Zellen."""
    u20 = u65 = 0.0
    for parsed in ages.values():
        u20 += sum(float(parsed.get(col) or 0.0) for col in U20_COLUMNS)
        u65 += sum(float(parsed.get(col) or 0.0) for col in AGE_BAND_COLUMNS["u65"])
    return u20 / u65 if u65 > 0 else NATIONAL_U20_SHARE_OF_U65


def _senior_split(counts: dict[str, float], fallback: dict[str, float]) -> dict[str, float]:
    """Anteile der drei Senioren-Bänder an 65+; ``fallback`` bei zu dünner Besetzung."""
    total = sum(counts.values())
    if total <= 0:
        return dict(fallback)
    return {b: counts[b] / total for b in counts}


def _area_senior_split(ages: dict[str, dict[str, Any]]) -> dict[str, float]:
    """Gebietsweite 65+-Binnenaufteilung als Rückfall für dünn besetzte Zellen."""
    acc = {"a65_74": 0.0, "a75_84": 0.0, "a85p": 0.0}
    for parsed in ages.values():
        for band, n in _senior_band_counts(parsed).items():
            acc[band] += n
    return _senior_split(acc, NATIONAL_SENIOR_SPLIT)


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


def _building_year_fallbacks(
    bage: dict[str, dict[str, Any]],
) -> tuple[dict[tuple[int, int], float], float | None]:
    """Baujahr-Rückfallwerte aus dem gröberen 1km-Gitter.

    Viele 100m-Zellen tragen zwar Gebäude, aber (Zensus-Datenschutz) keine
    besetzten Baujahrsklassen → dort liefert ``_mean_building_year`` ``None``.
    Diese Lücken werden über das umgebende 1km-INSPIRE-Gitter aufgefüllt: je
    1km-Zelle wird das gewichtete mittlere Baujahr über ALLE 100m-Zellen mit
    bekanntem Baujahr gebildet (Gewicht = Gebäude je Klasse). Zusätzlich ein
    gebietsweiter Mittelwert als letzter Rückfall, falls auch die 1km-Zelle leer
    ist.

    Gibt ``(km_index, area_mean)`` zurück; Schlüssel des Index ist
    ``(x_mp // 1000, y_mp // 1000)``.
    """
    acc: dict[tuple[int, int], list[float]] = {}  # km-Zelle -> [gewichtete Summe, Anzahl]
    tot_w, tot_n = 0.0, 0
    for parsed in bage.values():
        x, y = parsed.get("x"), parsed.get("y")
        if x is None or y is None:
            continue
        km = (int(x) // 1000, int(y) // 1000)
        a = acc.setdefault(km, [0.0, 0])
        for col, mid_year in BUILDING_AGE_CLASSES:
            n = parsed.get(col)
            if n and n > 0:
                a[0] += n * mid_year
                a[1] += n
                tot_w += n * mid_year
                tot_n += n
    km_index = {km: w / n for km, (w, n) in acc.items() if n > 0}
    area_mean = (tot_w / tot_n) if tot_n > 0 else None
    return km_index, area_mean


def load_zensus_for_cells(
    grid_cells: list[dict],
    keys: list[str] | None = None,
) -> dict[str, dict[str, dict[str, Any]]]:
    """Load all Zensus datasets for the bbox of grid cells."""
    keys = list(keys or DEFAULT_LOAD_KEYS)
    geoms = [c["geometry"] for c in grid_cells]
    bbox = bbox_3035_from_wgs_geoms(geoms)
    workers = min(len(keys), 4)

    def _load(key: str) -> tuple[str, dict[str, dict[str, Any]]]:
        try:
            return key, load_dataset_bbox(key, bbox)
        except Exception as exc:
            # Optionale Datensätze dürfen das Assessment nicht blockieren; die
            # Aufrufer haben für jeden davon einen dokumentierten Rückfall.
            if ZENSUS_DATASETS[key].required:
                raise
            log.warning("Optionaler Zensus-Datensatz '%s' nicht verfügbar: %s", key, exc)
            return key, {}

    with ThreadPoolExecutor(max_workers=workers) as ex:
        pairs = list(ex.map(_load, keys))
    return {key: data for key, data in pairs}


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
    ages = zensus.get("age_groups", {})

    # 1km-Rückfallwerte für Zellen mit Gebäuden, aber ohne besetzte Baujahrsklassen.
    km_year_index, area_year_mean = _building_year_fallbacks(bage)
    # Gebietsweite 65+-Binnenaufteilung als Rückfall für unterdrückte Zellen.
    area_split = _area_senior_split(ages) if ages else dict(NATIONAL_SENIOR_SPLIT)
    area_u20 = _area_u20_share(ages) if ages else NATIONAL_U20_SHARE_OF_U65

    for idx, ci in enumerate(cell_inputs):
        gid = gid_by_idx.get(idx) or ci.get("gitter_id")
        if not gid:
            continue

        p = pop_data.get(gid, {})
        ci["pop"] = float(p.get("Einwohner") or 0.0)

        o65 = over65.get(gid, {})
        u18 = under18.get(gid, {})
        ci["share_over_65"] = o65.get("AnteilUeber65")
        ci["share_under_18"] = u18.get("AnteilUnter18")

        la = living.get(gid, {})
        ow = owner.get(gid, {})
        rt = rent.get(gid, {})
        ba = bage.get(gid, {})

        ci["living_area_per_person"] = la.get("durchschnFlaechejeBew")
        ci["owner_share"] = ow.get("Eigentuemerquote")
        ci["net_cold_rent"] = rt.get("durchschnMieteQM")
        ci["building_count_zensus"] = ba.get("Insgesamt_Gebaeude")
        ci["building_age_mean"] = ba.get("building_age_mean")
        # Imputation: Zelle hat Gebäude, aber kein Baujahr (Zensus-Datenschutz) →
        # mittleres Baujahr aus der umgebenden 1km-Zelle (bzw. gebietsweit) ansetzen,
        # damit der Layer nicht flächig Löcher zeigt, wo nachweislich Gebäude stehen.
        if ci["building_age_mean"] is None and (ba.get("Insgesamt_Gebaeude") or 0) > 0:
            x, y = ba.get("x"), ba.get("y")
            fb = km_year_index.get((int(x) // 1000, int(y) // 1000)) if x is not None and y is not None else None
            if fb is None:
                fb = area_year_mean
            if fb is not None:
                ci["building_age_mean"] = fb
                ci["building_age_imputed"] = True
        ci["zensus_uncertain"] = any(
            z.get("statistically_uncertain")
            for z in (o65, u18, la, ow, rt, ba)
            if z
        )
        ci["gitter_id"] = gid

        share_o = ci.get("share_over_65") or 0.0
        share_u = ci.get("share_under_18") or 0.0
        ci["share_vulnerable"] = min(100.0, share_o + share_u)
        pop = ci.get("pop") or 0.0
        ci["pop_over_65"] = pop * share_o / 100.0 if pop > 0 else 0.0
        ci["pop_under_18"] = pop * share_u / 100.0 if pop > 0 else 0.0

        # Altersbänder für die Expositions-Wirkungs-Rechnung. Bewusst aus ZWEI
        # Quellen: ``share_over_65`` (gut besetzt) legt die 65+-Menge fest, die
        # 5-Jahres-Gruppen nur deren Binnenaufteilung. So trägt jeder Datensatz
        # das, was er belastbar hergibt — siehe AGE_BAND_COLUMNS.
        senior_counts = _senior_band_counts(ages.get(gid, {})) if ages else {}
        split = _senior_split(senior_counts, area_split) if senior_counts else dict(area_split)
        pop_65p = ci["pop_over_65"]
        pop_u65 = max(0.0, pop - pop_65p)
        # u20/20–64 (Methodik #96 §3.2): Binnenaufteilung der u65-Menge aus den
        # 5-Jahres-Gruppen der Zelle, Rückfall Gebiet → national. ``u65`` bleibt
        # erhalten — die Hitze-Bänder (#95) lesen es unverändert.
        u20_share = (_u20_share_of_u65(ages.get(gid, {}), area_u20)
                     if ages else area_u20)
        ci["pop_age_bands"] = {
            "u65": pop_u65,
            "u20": pop_u65 * u20_share,
            "a20_64": pop_u65 * (1.0 - u20_share),
            "a65_74": pop_65p * split["a65_74"],
            "a75_84": pop_65p * split["a75_84"],
            "a85p": pop_65p * split["a85p"],
        }


def demographic_shares() -> dict:
    """Fallback demografie (nur wenn Zensus-Zelle fehlt)."""
    from app.services.zensus_service import NATIONAL_DEMOGRAPHICS
    d = dict(NATIONAL_DEMOGRAPHICS)
    d["share_under_18"] = 18.0
    d.pop("share_under_6", None)
    return d
