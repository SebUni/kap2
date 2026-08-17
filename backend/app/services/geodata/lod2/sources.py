"""LoD2-Quellen-Registry: amtliche 3D-Gebäudemodelle (CityGML) der 16 Länder.

Die Länder publizieren LoD2 einzeln — es gibt KEIN offenes bundesweites
LoD2-DE (BKG-Produkt ist auf GeoBund/GeoLänder beschränkt). Vier Zugriffs-
mechanismen (dispatcht der Loader über die Felder dieser Registry):

  1. Direktes Kachel-URL-Muster (``url_builder``): NW, BY, BB, TH, RP, MV,
     BE, SN, BW. Kachelanker beachten — BW rastert 2 km auf UNGERADE
     Ostwerte (``tile_anchor=(1, 0)``).
  2. Kachel-Index (``index_url`` + ``index_url_prop``/``index_coord_re``):
     GeoJSON-Verzeichnis aller Kacheln mit Download-URL je Feature —
     NI (11 707 Kacheln), SH (13 805 Kacheln). Index-Geometrien in
     EPSG:25832; Koordinaten kommen aus dem Dateinamen (Regex) oder der
     Feature-Geometrie.
  3. Zweistufige Generierung (``prepare_page`` + ``prepare_endpoint``): ST —
     die Kachel-IDs stehen als GeoJSON in der Download-Seite (Label
     ``32{E}{N}``), der prepare-Endpunkt liefert die Download-URL zurück.
  4. Stadt-/Landesarchive (``archive="zip-city"``): HH (URL via CKAN-API),
     HB (statische URLs Bremen + Bremerhaven).

Phase 2 (kein maschinenlesbarer Zugang, OSM-Fallback): HE (Downloadcenter
ist session-basiert, INSPIRE-API liefert Liniengeometrien), SL (LVGL-Shop).

Alle Muster am 15.07.2026 per HTTP verifiziert (Stichproben-Kacheln).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

CKAN_HAMBURG = (
    "https://suche.transparenz.hamburg.de/api/3/action/package_show"
    "?id=3d-gebaeudemodell-lod2-de-hamburg"
)

_MV_DATASET = "8397b554-5cb9-4274-8be8-c20490d9a6e8"
_SN_SHARE = "AyJqXpJAZJXomCb"


@dataclass(frozen=True)
class Lod2Source:
    land: str                 # Wert wie kommune.bundesland / BUNDESLAND_BY_SNL
    crs: str                  # "EPSG:25832" | "EPSG:25833"
    tile_km: int              # Kachelkantenlänge km; 0 = Archiv (Gesamtstadt/-land)
    archive: str              # "gml" | "zip" | "zip-city"
    license: str
    phase: int                # 1 = angebunden, 2 = kein Maschinenzugang → OSM
    # (e_km, n_km) → Kandidaten-URLs (werden der Reihe nach probiert)
    url_builder: Callable[[int, int], list[str]] = field(default=lambda e, n: [])
    # Kachelraster-Anker: Ostwert-/Nordwert-Offset in km (BW: E ungerade)
    tile_anchor: tuple[int, int] = (0, 0)
    # Index-Quellen (NI, SH): GeoJSON-Verzeichnis aller Kacheln
    index_url: str = ""
    index_url_prop: str = ""  # Feature-Property mit der Download-URL
    index_coord_re: str = ""  # Regex mit 2 Gruppen (E, N in km) auf die URL;
                              # leer = Koordinaten aus der Feature-Geometrie (m)
    # Zweistufige Quellen (ST): Kachel-IDs aus Seiten-GeoJSON + prepare-Call
    prepare_page: str = ""
    prepare_endpoint: str = ""
    # Archiv-Quellen: statische URLs (HB) oder CKAN-Auflösung (HH)
    city_urls: tuple[str, ...] = ()
    ckan_api: str = ""
    note: str = ""            # Phase-2: Begründung / Einstiegs-URL


def _nrw_urls(e: int, n: int) -> list[str]:
    return [
        "https://www.opengeodata.nrw.de/produkte/geobasis/3dg/lod2_gml/"
        f"lod2_gml/LoD2_32_{e}_{n}_1_NW.gml"
    ]


def _bayern_urls(e: int, n: int) -> list[str]:
    return [
        f"https://download{i}.bayernwolke.de/a/lod2/citygml/{e}_{n}.gml"
        for i in (1, 2)
    ]


def _brandenburg_urls(e: int, n: int) -> list[str]:
    # Easting trägt das Zonenpräfix "33" im Dateinamen (EPSG:25833)
    return [
        "https://data.geobasis-bb.de/geobasis/daten/3d_gebaeude/lod2_gml/"
        f"lod2_33{e}-{n}.zip"
    ]


def _thueringen_urls(e: int, n: int) -> list[str]:
    return [
        f"https://geoportal.geoportal-th.de/3dgebaeude/LoD2/LoD2_32_{e}_{n}_2_TH.zip"
    ]


def _rlp_urls(e: int, n: int) -> list[str]:
    return [
        f"https://geobasis-rlp.de/data/geb3dlo/current/gml/LoD2_32_{e}_{n}_2_RP.gml"
    ]


def _mv_urls(e: int, n: int) -> list[str]:
    return [
        "https://www.geodaten-mv.de/dienste/gebaeude_download"
        f"?index=0&dataset={_MV_DATASET}&file=lod2_33_{e}_{n}_2_gml.zip"
    ]


def _berlin_urls(e: int, n: int) -> list[str]:
    return [f"https://gdi.berlin.de/data/a_lod2/atom/LoD2_{e}_{n}.zip"]


def _sachsen_urls(e: int, n: int) -> list[str]:
    return [
        "https://geocloud.landesvermessung.sachsen.de/index.php/s/"
        f"{_SN_SHARE}/download?files=lod2_33{e}_{n}_2_sn_citygml.zip"
    ]


def _bw_urls(e: int, n: int) -> list[str]:
    # 2-km-Gitter mit UNGERADEN Ostwerten (tile_anchor=(1, 0))
    return [
        f"https://opengeodata.lgl-bw.de/data/lod2/LoD2_32_{e}_{n}_2_bw.zip"
    ]


LOD2_SOURCES: dict[str, Lod2Source] = {
    # ── Direktes Kachel-URL-Muster ───────────────────────────────────────────
    "Nordrhein-Westfalen": Lod2Source(
        land="Nordrhein-Westfalen", crs="EPSG:25832", tile_km=1,
        archive="gml", license="dl-de/zero-2-0", phase=1,
        url_builder=_nrw_urls,
    ),
    "Bayern": Lod2Source(
        land="Bayern", crs="EPSG:25832", tile_km=2,
        archive="gml", license="CC BY 4.0", phase=1,
        url_builder=_bayern_urls,
    ),
    "Brandenburg": Lod2Source(
        land="Brandenburg", crs="EPSG:25833", tile_km=1,
        archive="zip", license="dl-de/by-2-0", phase=1,
        url_builder=_brandenburg_urls,
    ),
    "Thüringen": Lod2Source(
        land="Thüringen", crs="EPSG:25832", tile_km=2,
        archive="zip", license="dl-de/by-2-0", phase=1,
        url_builder=_thueringen_urls,
    ),
    "Rheinland-Pfalz": Lod2Source(
        land="Rheinland-Pfalz", crs="EPSG:25832", tile_km=2,
        archive="gml", license="dl-de/by-2-0", phase=1,
        url_builder=_rlp_urls,
    ),
    "Mecklenburg-Vorpommern": Lod2Source(
        land="Mecklenburg-Vorpommern", crs="EPSG:25833", tile_km=2,
        archive="zip", license="CC BY 4.0", phase=1,
        url_builder=_mv_urls,
    ),
    "Berlin": Lod2Source(
        land="Berlin", crs="EPSG:25833", tile_km=1,
        archive="zip", license="dl-de/zero-2-0", phase=1,
        url_builder=_berlin_urls,
    ),
    "Sachsen": Lod2Source(
        land="Sachsen", crs="EPSG:25833", tile_km=2,
        archive="zip", license="dl-de/by-2-0", phase=1,
        url_builder=_sachsen_urls,
    ),
    "Baden-Württemberg": Lod2Source(
        land="Baden-Württemberg", crs="EPSG:25832", tile_km=2,
        archive="zip", license="dl-de/by-2-0", phase=1,
        url_builder=_bw_urls, tile_anchor=(1, 0),
    ),
    # ── Kachel-Index (GeoJSON-Verzeichnis) ───────────────────────────────────
    "Niedersachsen": Lod2Source(
        land="Niedersachsen", crs="EPSG:25832", tile_km=2,
        archive="gml", license="CC BY 4.0", phase=1,
        index_url=("https://single-datasets.opengeodata.lgln.niedersachsen.de/"
                   "pro-download-indices/lod2/lgln-opengeodata-lod2.geojson"),
        index_url_prop="CityGML",
    ),
    "Schleswig-Holstein": Lod2Source(
        land="Schleswig-Holstein", crs="EPSG:25832", tile_km=1,
        archive="gml", license="CC BY 4.0", phase=1,
        index_url=("https://geodaten.schleswig-holstein.de/gaialight-sh/"
                   "_apps/dladownload/single.php"
                   "?file=LOD2_SH_Massendownload.geojson&id=4"),
        index_url_prop="data_link",
        index_coord_re=r"LoD2_32_(\d+)_(\d+)_1_SH",
    ),
    # ── Zweistufige Generierung ──────────────────────────────────────────────
    "Sachsen-Anhalt": Lod2Source(
        land="Sachsen-Anhalt", crs="EPSG:25832", tile_km=2,
        archive="zip", license="dl-de/by-2-0", phase=1,
        prepare_page="https://www.lvermgeo.sachsen-anhalt.de/de/gdp-download-lod2.html",
        prepare_endpoint=("https://www.lvermgeo.sachsen-anhalt.de/de/"
                          "mod/4,1965,501/ajax/1/prepare/"),
    ),
    # ── Stadt-/Landesarchive ─────────────────────────────────────────────────
    "Hamburg": Lod2Source(
        land="Hamburg", crs="EPSG:25832", tile_km=0,
        archive="zip-city", license="dl-de/by-2-0", phase=1,
        ckan_api=CKAN_HAMBURG,
    ),
    "Bremen": Lod2Source(
        land="Bremen", crs="EPSG:25832", tile_km=0,
        archive="zip-city", license="CC BY 4.0", phase=1,
        city_urls=(
            "https://gdi2.geo.bremen.de/inspire/download/LoD/data/LOD2_CITYGML_HB.zip",
            "https://gdi2.geo.bremen.de/inspire/download/LoD/data/LOD2_CITYGML_BHV.zip",
        ),
    ),
    # ── Phase 2: kein maschinenlesbarer Zugang ───────────────────────────────
    "Hessen": Lod2Source(
        land="Hessen", crs="EPSG:25832", tile_km=1,
        archive="zip", license="dl-de/zero-2-0", phase=2,
        note=("gds.hessen.de-Downloadcenter ist session-basiert (Intershop); "
              "INSPIRE-OGC-API liefert nur Liniengeometrien (bu-core3d)"),
    ),
    "Saarland": Lod2Source(
        land="Saarland", crs="EPSG:25832", tile_km=1,
        archive="zip", license="dl-de/by-2-0", phase=2,
        note="LVGL-Shop (Virtuemart, manueller Warenkorb); kein Direktzugang",
    ),
}


def source_for(bundesland: str | None) -> Lod2Source | None:
    """Phase-1-Quelle für das Land, sonst None (→ OSM-Fallback)."""
    if not bundesland:
        return None
    src = LOD2_SOURCES.get(bundesland)
    return src if src is not None and src.phase == 1 else None
