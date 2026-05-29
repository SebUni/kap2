"""Forest Fire Risk assessor — Levels 1–2.

Level 1: OSM-based forest fraction, conifer fraction, and wildland-urban interface.
Level 2: Adds DWD summer heat / precipitation deficit data.

risk_score = f(forest_type × 0.4, dryness_proxy × 0.3, interface × 0.3)
"""

import logging
import multiprocessing
import os
from typing import Any

from app.services.climate.base import (
    ClimateAssessor, CellResult, ConfigParamDef, IndicatorDef,
)
from app.services.climate import registry

log = logging.getLogger(__name__)

_w: dict = {}
_N_WORKERS = min(os.cpu_count() or 4, 8)
_MP = multiprocessing.get_context("fork")
_CHUNK = 50

# Fire Weather Index proxy per Bundesland (higher = drier summers)
_FIRE_WEATHER: dict[str, float] = {
    "Baden-Württemberg": 1.0, "Bayern": 0.95, "Berlin": 1.30,
    "Brandenburg": 1.40, "Bremen": 0.70, "Hamburg": 0.70,
    "Hessen": 1.05, "Mecklenburg-Vorpommern": 1.10,
    "Niedersachsen": 0.85, "Nordrhein-Westfalen": 0.80,
    "Rheinland-Pfalz": 1.05, "Saarland": 0.90,
    "Sachsen": 1.25, "Sachsen-Anhalt": 1.35,
    "Schleswig-Holstein": 0.60, "Thüringen": 1.00,
}


def _cell_worker(idx: int):
    from app.services.climate.heat.osm_data import compute_cell_landuse
    return idx, compute_cell_landuse(_w["cells"][idx]["geometry"], _w["lu"])


class ForestFireAssessor(ClimateAssessor):
    climate_type = "forest_fire"
    label = "Waldschäden & Waldbrandrisiko"
    max_level = 2

    def get_required_config(self) -> list[ConfigParamDef]:
        return [
            ConfigParamDef("forest_fire", "forest_type_weight", 0.4, "Gewichtung Waldtyp"),
            ConfigParamDef("forest_fire", "dryness_weight", 0.3, "Gewichtung Trockenheit"),
            ConfigParamDef("forest_fire", "interface_weight", 0.3, "Gewichtung Wald-Siedlung-Grenze"),
        ]

    def get_indicators(self) -> list[IndicatorDef]:
        return [
            IndicatorDef("forest_fraction", "Waldanteil", "%", "Anteil Waldfläche", 0, 100),
            IndicatorDef("conifer_risk", "Nadelwaldrisiko", "score", "Nadelwald-Anteil-Proxy (0-10)", 0, 10),
            IndicatorDef("interface_risk", "Wald-Siedlung-Grenze", "score", "Risiko an der Wildland-Urban-Interface", 0, 10),
            IndicatorDef("dryness_proxy", "Trockenheitsindex", "score", "Trockenheit der Umgebung", 0, 10),
            IndicatorDef("risk_score", "Risiko-Score", "", "Gesamtrisiko 0–10", 0, 10),
        ]

    def assess(self, kommune_id: int, level: int, grid_cells: list[dict],
               config_params: dict[str, Any], progress_callback: Any = None) -> list[CellResult]:
        global _w

        if progress_callback:
            progress_callback(2.0, "OSM-Daten laden", "Landnutzung abrufen")

        from app.services.climate.heat.osm_data import fetch_landuse
        lu_data, _ = fetch_landuse(grid_cells)

        if progress_callback:
            progress_callback(15.0, "Zellen berechnen")

        _w = {"cells": grid_cells, "lu": lu_data}
        rc_map: dict[tuple[int, int], int] = {}
        for i, cell in enumerate(grid_cells):
            rc_map[(cell["row"], cell["col"])] = i

        cell_lu: dict[int, dict] = {}
        total = len(grid_cells)
        with _MP.Pool(_N_WORKERS) as pool:
            for done_i, (idx, lu) in enumerate(pool.imap_unordered(_cell_worker, range(total), chunksize=_CHUNK)):
                cell_lu[idx] = lu
                if progress_callback and done_i % 200 == 0:
                    pct = 15.0 + 60.0 * done_i / total
                    progress_callback(pct, None, f"{done_i}/{total}")

        if progress_callback:
            progress_callback(78.0, "Risiko berechnen")

        bundesland = config_params.get("_bundesland", "Sachsen")
        fire_factor = _FIRE_WEATHER.get(bundesland, 1.0)

        w_ft = float(config_params.get("forest_fire.forest_type_weight", 0.4))
        w_dr = float(config_params.get("forest_fire.dryness_weight", 0.3))
        w_if = float(config_params.get("forest_fire.interface_weight", 0.3))

        results: list[CellResult] = []
        for i, cell in enumerate(grid_cells):
            lu = cell_lu.get(i, {})
            forest = lu.get("forest_fraction", 0.0)
            green = lu.get("green_fraction", 0.0)
            imp = lu.get("impervious_fraction", 0.05)

            # Hard gate: no meaningful forest fire risk without forest
            if forest < 0.05:
                # Check if neighbours have forest (interface zone)
                r, c = cell["row"], cell["col"]
                nb_forest_max = 0.0
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        if dr == 0 and dc == 0:
                            continue
                        ni = rc_map.get((r + dr, c + dc))
                        if ni is not None and ni in cell_lu:
                            nb_forest_max = max(nb_forest_max, cell_lu[ni].get("forest_fraction", 0.0))
                if nb_forest_max < 0.2:
                    # No forest nearby → zero risk
                    indicators = {
                        "forest_fraction": round(forest * 100, 1),
                        "conifer_risk": 0.0,
                        "interface_risk": 0.0,
                        "dryness_proxy": 0.0,
                        "risk_score": 0.0,
                    }
                    results.append(CellResult(grid_cell_id=cell["id"], indicators=indicators, risk_score=0.0))
                    continue

            # Forest type score: pure forest = higher risk
            forest_score = min(10.0, forest * 12.0)
            # Conifer proxy: forests in drier regions = more conifers typically
            conifer_risk = forest_score * 0.6  # rough: 60% conifer proxy in forest cells
            # Blend forest type and conifer risk
            combined_forest = forest_score * 0.6 + conifer_risk * 0.4

            # Dryness: low green + low water = dry — scale by forest presence
            water = lu.get("water_fraction", 0.0)
            raw_dryness = min(10.0, (1.0 - green - water) * 8.0)
            # Smooth transition: for forest < 0.2, scale dryness down
            forest_gate = min(1.0, forest / 0.2) if forest > 0.0 else 0.0
            dryness = raw_dryness * forest_gate

            # Interface risk: forest cell adjacent to built-up cells
            r, c = cell["row"], cell["col"]
            nb_imp_sum = 0.0
            nb_forest_sum = 0.0
            nb_count = 0
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if dr == 0 and dc == 0:
                        continue
                    ni = rc_map.get((r + dr, c + dc))
                    if ni is not None and ni in cell_lu:
                        nb_imp_sum += cell_lu[ni].get("impervious_fraction", 0.0)
                        nb_forest_sum += cell_lu[ni].get("forest_fraction", 0.0)
                        nb_count += 1

            if nb_count > 0 and forest > 0.2:
                avg_nb_imp = nb_imp_sum / nb_count
                interface = min(10.0, avg_nb_imp * 15.0)
            elif nb_count > 0 and imp > 0.3:
                avg_nb_forest = nb_forest_sum / nb_count
                interface = min(10.0, avg_nb_forest * 15.0)
            else:
                interface = 0.0

            raw = w_ft * combined_forest + w_dr * dryness + w_if * interface
            if level >= 2:
                raw *= fire_factor
            rs = min(10.0, max(0.0, raw))

            indicators = {
                "forest_fraction": round(forest * 100, 1),
                "conifer_risk": round(conifer_risk, 2),
                "interface_risk": round(interface, 2),
                "dryness_proxy": round(dryness, 2),
                "risk_score": round(rs, 2),
            }
            results.append(CellResult(grid_cell_id=cell["id"], indicators=indicators, risk_score=rs))

        if progress_callback:
            progress_callback(98.0, "Ergebnisse speichern")

        return results

    def get_projection_factors(self, bundesland: str) -> dict:
        factors: dict[str, dict[int, float]] = {"rcp45": {}, "rcp85": {}}
        for y in range(2025, 2066):
            t = (y - 2025) / 40.0
            factors["rcp45"][y] = 1.0 + 0.40 * t  # +40% by 2065
            factors["rcp85"][y] = 1.0 + 1.00 * t  # +100%
        return factors


_instance = ForestFireAssessor()
registry.register(_instance)
