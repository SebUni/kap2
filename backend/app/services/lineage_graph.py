"""Baut Herkunfts-Graphen (Quellen → Zwischen → H/E/V → Risiko) für Info-Fenster."""

from __future__ import annotations

from typing import Any

from app.data import catalog
from app.data.lineage_operators import CELL_DIRECT, CELL_OPERATORS, formula_operators_for
from app.data.pathway_descriptions import chain_label, get_pathway_description
from app.services.engine import formulas
from app.services.engine.formulas import risk_pathway_meta, risk_recipe
from app.services.engine.impact.environment import LINEAGE_SPECS as ENV_SPECS
from app.services.engine.impact.health import LINEAGE_SPECS as HEALTH_SPECS
from app.services.engine.impact.monetary import LINEAGE_SPECS as MONETARY_SPECS
from app.services.engine.impact.params import IMPACT_GLOBAL_SPECS, IMPACT_PARAM_SPECS

# Label/Einheit/Quelle der Schicht-B-Parameter für die Parameterknoten im Diagramm
_IMPACT_PARAM_BY_KEY: dict[tuple[str, str], dict] = {
    (s["risk"], s["key"]): s for s in IMPACT_PARAM_SPECS
}
_IMPACT_GLOBAL_BY_KEY: dict[str, dict] = {s["key"]: s for s in IMPACT_GLOBAL_SPECS}

# ── Kanonische Quellen ────────────────────────────────────────────────────────

SOURCE_IDS = {
    "osm": ("OSM", "OpenStreetMap"),
    "dwd": ("DWD", "Deutscher Wetterdienst"),
    "zensus": ("Zensus", "Zensus / Bevölkerungsdaten"),
    "dem": ("DEM", "Digitales Geländemodell"),
    "bsh": ("BSH", "Bundesamt für Seeschifffahrt"),
    "param": ("Parameter", "Modellannahme"),
    "computed": ("Berechnet", "Abgeleitet aus Zellgrößen"),
}

INTERMEDIATE_LABELS: dict[str, str] = {
    "imp_frac": "Versiegelungsgrad (Zelle)",
    "imp_lu": "Versiegelung (Landnutzung)",
    "bldg_cov": "Gebäudeanteil",
    "road_cov": "Straßenanteil",
    "green_frac": "Grünanteil",
    "forest_frac": "Waldanteil",
    "farmland_frac": "Ackeranteil",
    "water_frac": "Wasseranteil",
    "water_adj": "Gewässernähe (Nachbarschaft)",
    "water_prox": "Gewässernähe (Distanz)",
    "uhi_delta": "UHI-ΔT",
    "canopy_frac": "Baumkronenanteil",
    "svf": "Himmelsichtfaktor",
    "avg_height": "Mittlere Gebäudehöhe",
    "vent_score": "Belüftungsgrad",
    "slope_deg": "Hangneigung",
    "slope_factor": "Hangneigung (Proxy)",
    "slope_proxy": "Hangneigung (Proxy)",
    "mean_elevation_m": "Mittlere Höhe",
    "snow_elevation_factor": "Höhenfaktor Schnee",
    "depression_factor": "Senkenfaktor",
    "depression_proxy": "Senken-Proxy",
    "twi_norm": "Topographisches Feuchte-Index",
    "flow_accum": "Flussakkumulation",
    "pop": "Einwohner (Zelle)",
    "pop_density": "Bevölkerungsdichte",
    "area_km2": "Zellfläche",
    "area_ha": "Zellfläche (ha)",
    "industrial": "Industriefläche (abgeleitet)",
    "healthcare_access_score": "Gesundheitszugang",
    "transport_hub_count": "Verkehrsknoten",
    "hot_days": "Heiße Tage/Jahr",
    "frost_days": "Frosttage",
    "heavy_rain_index": "Starkregenindex",
    "storm_days": "Sturmtage",
    "mean_temp_rise": "Temperaturanstieg",
    "soil_moisture_decline": "Bodenfeuchte-Rückgang",
    "surface_water_heating": "Gewässererwärmung",
    "glacier_loss_rate": "Gletscherschwund",
    "glacier_frac": "Gletscheranteil",
    "snow_decline_rate_pct": "Schneedecken-Rückgang",
    "snow_days": "Schneedeckentage",
    "mean_temp": "Jahresmitteltemperatur",
    "sea_level_rise": "Meeresspiegelanstieg",
    "area_m2": "Zellfläche (m²)",
    "share_over_65": "Anteil ≥ 65 Jahre",
    "share_under_18": "Anteil < 18 Jahre",
    "living_area_per_person": "Wohnfläche je Person",
    "owner_share": "Eigentümerquote",
    "net_cold_rent": "Nettokaltmiete",
    "building_age_mean": "Mittleres Gebäudealter",
    "dist_hospital_m": "Distanz Krankenhaus",
    "dist_doctor_m": "Distanz Arzt/Klinik",
    "dist_pharmacy_m": "Distanz Apotheke",
    "dyke_prox": "Deichnähe",
    "emergency_access_score": "Notfall-Erreichbarkeit",
    "bldg_count": "Gebäudeanzahl",
    "energy_infra_count": "Energieanlagen (Anzahl)",
    "water_wastewater_count": "Wasser-/Abwasseranlagen (Anzahl)",
    "communication_count": "Kommunikationsanlagen (Anzahl)",
}

# cell_key → (intermediate_keys, source_ids)
CELL_INPUT_LINEAGE: dict[str, tuple[list[str], list[str]]] = {
    "imp_frac": (["bldg_cov", "road_cov", "imp_lu"], ["osm"]),
    "imp_lu": ([], ["osm"]),
    "bldg_cov": ([], ["osm"]),
    "road_cov": ([], ["osm"]),
    "green_frac": ([], ["osm"]),
    "forest_frac": ([], ["osm"]),
    "farmland_frac": ([], ["osm"]),
    "water_frac": ([], ["osm"]),
    "water_adj": ([], ["osm"]),
    "water_prox": ([], ["osm"]),
    "glacier_frac": ([], ["osm"]),
    "canopy_frac": ([], ["osm"]),
    "svf": ([], ["osm"]),
    "avg_height": ([], ["osm"]),
    "bldg_count": ([], ["osm"]),
    "energy_infra_count": ([], ["osm"]),
    "water_wastewater_count": ([], ["osm"]),
    "communication_count": ([], ["osm"]),
    "transport_hub_count": ([], ["osm"]),
    "uhi_delta": (
        ["bldg_cov", "road_cov", "green_frac", "forest_frac", "water_frac", "canopy_frac", "svf"],
        ["osm", "param"],
    ),
    # Quellen fließen über die Teil-Zwischenwerte (slope_deg ← DEM, vent_score ← OSM)
    "slope_factor": (["slope_deg", "vent_score"], []),
    "slope_proxy": (["slope_deg", "vent_score"], []),
    "slope_deg": ([], ["dem"]),
    "vent_score": ([], ["osm"]),
    "mean_elevation_m": ([], ["dem"]),
    "snow_elevation_factor": (["mean_elevation_m"], ["dem"]),
    "depression_factor": (["imp_frac", "water_adj", "vent_score"], ["osm", "dem"]),
    "depression_proxy": (["imp_frac", "water_adj", "vent_score"], ["osm", "dem"]),
    "twi_norm": ([], ["dem"]),
    "flow_accum": ([], ["dem"]),
    "pop": ([], ["zensus"]),
    "pop_density": (["pop", "area_km2"], ["zensus", "computed"]),
    "area_km2": ([], []),
    "area_ha": ([], []),
    "industrial": (["bldg_cov", "road_cov", "imp_frac"], ["osm"]),
    "healthcare_access_score": ([], ["osm"]),
    "hot_days": ([], ["dwd"]),
    "frost_days": ([], ["dwd"]),
    "heavy_rain_index": ([], ["dwd"]),
    "storm_days": ([], ["dwd"]),
    "mean_temp_rise": ([], ["dwd"]),
    "mean_temp": ([], ["dwd"]),
    "soil_moisture_decline": ([], ["dwd"]),
    "surface_water_heating": ([], ["dwd"]),
    "glacier_loss_rate": ([], ["dwd"]),
    "snow_decline_rate_pct": ([], ["dwd"]),
    "snow_days": ([], ["dwd"]),
    "sea_level_rise": ([], ["bsh"]),
    "area_m2": ([], []),
    "share_over_65": ([], ["zensus"]),
    "share_under_18": ([], ["zensus"]),
    "living_area_per_person": ([], ["zensus"]),
    "owner_share": ([], ["zensus"]),
    "net_cold_rent": ([], ["zensus"]),
    "building_age_mean": ([], ["zensus"]),
    "dist_hospital_m": ([], ["osm"]),
    "dist_doctor_m": ([], ["osm"]),
    "dist_pharmacy_m": ([], ["osm"]),
    "dyke_prox": ([], ["osm"]),
    "emergency_access_score": ([], ["osm"]),
}

# Kurzbeschreibung, wie Zwischenwerte aus Eingaben berechnet werden
INTERMEDIATE_TOOLTIPS: dict[str, str] = {
    "imp_frac": "Versiegelungsgrad = Gebäude- + Straßenanteil (OSM), ggf. mit Landnutzungs-Fallback.",
    "imp_lu": "Versiegelungsanteil aus OSM-Landnutzungsklassen der Zelle.",
    "bldg_cov": "Anteil der Zellfläche, die von Gebäudegrundrissen bedeckt ist (OSM).",
    "road_cov": "Anteil der Zellfläche, der von Straßen bedeckt ist (OSM).",
    "green_frac": "Anteil Grünflächen (Wiesen, Parks, Gärten) in der Zelle (OSM).",
    "forest_frac": "Waldanteil der Zelle (OSM natural=wood/forest).",
    "farmland_frac": "Acker- und landwirtschaftlicher Anteil (OSM).",
    "water_frac": "Wasserflächenanteil der Zelle (OSM).",
    "water_adj": "Wasseranteil in der 8-Nachbarschaft (max. benachbarter Wasseranteil).",
    "water_prox": "Gewässernähe als Score aus Distanz zum nächsten Gewässer (OSM).",
    "canopy_frac": "Baumkronenanteil aus OSM-Baumdaten.",
    "svf": "Himmelsichtfaktor aus Gebäudehöhen und -anordnung (OSM).",
    "avg_height": "Mittlere Gebäudehöhe in der Zelle (OSM).",
    "vent_score": "Frischluft-Anteil: offene/grüne Nachbarzellen / 8 Nachbarn.",
    "uhi_delta": (
        "Städtische Wärmeinsel ΔT (K): Versiegelung, Gebäude, Albedo, "
        "abzüglich Kühlung durch Grün, Wasser, Bäume und Straßenschlucht."
    ),
    "slope_deg": "Hangneigung aus Digitalem Geländemodell (DEM).",
    "slope_factor": "Hangneigung normiert als Risikofaktor (DEM + Belüftung).",
    "slope_proxy": "Hangneigung als Proxy (DEM + Belüftung).",
    "mean_elevation_m": "Mittlere Geländehöhe der Zelle (DEM).",
    "snow_elevation_factor": "Höhenmodulation für Schnee/Gletscher (aus Geländehöhe).",
    "depression_factor": "Senkenneigung: Versiegelung + Gewässernähe − Belüftung.",
    "depression_proxy": "Senken-Proxy aus Versiegelung, Gewässernähe und Belüftung.",
    "twi_norm": "Topographischer Feuchteindex (TWI) aus DEM, normiert.",
    "flow_accum": "Flussakkumulation aus DEM (Wasserfluss-Akkumulation).",
    "pop": "Einwohnerzahl der Zelle, anteilig aus Zensus-Raster verteilt.",
    "pop_density": "Bevölkerungsdichte = Einwohner / Zellfläche (km²).",
    "area_km2": "Zellfläche in km² aus Zellgröße (m).",
    "area_ha": "Zellfläche in Hektar aus Zellgröße (m).",
    "industrial": "Industrieflächen-Proxy aus Gebäude-, Straßen- und Versiegelungsanteil.",
    "healthcare_access_score": "Gesundheitszugang aus Distanz zu Ärzten/Krankenhäusern (OSM).",
    "hot_days": "Anzahl heißer Tage pro Jahr (DWD, regional).",
    "frost_days": "Anzahl Frosttage pro Jahr (DWD, regional).",
    "heavy_rain_index": "Starkregenindex (DWD, regional).",
    "storm_days": "Sturmtage pro Jahr (DWD, regional).",
    "mean_temp_rise": "Temperaturanstieg gegenüber Referenzperiode (DWD, regional).",
    "mean_temp": "Jahresmitteltemperatur (DWD, regional).",
    "soil_moisture_decline": "Bodenfeuchte-Rückgang (DWD, regional).",
    "surface_water_heating": "Gewässererwärmung (DWD, regional).",
    "glacier_loss_rate": "Gletscherschwund-Rate (Parameter/DWD).",
    "glacier_frac": "Gletscheranteil der Zelle (OSM).",
    "snow_decline_rate_pct": "Trend Schneedecken-Rückgang (DWD, regional).",
    "snow_days": "Schneedeckentage pro Jahr (DWD, regional).",
    "sea_level_rise": "Meeresspiegelanstieg (BSH, regional).",
    "area_m2": "Zellfläche in m² aus der Rastergeometrie (100 × 100 m).",
    "share_over_65": "Anteil der Bevölkerung ab 65 Jahren (Zensus-Raster).",
    "share_under_18": "Anteil der Bevölkerung unter 18 Jahren (Zensus-Raster).",
    "living_area_per_person": "Wohnfläche je Person (Zensus-Raster).",
    "owner_share": "Eigentümerquote der Wohnungen (Zensus-Raster).",
    "net_cold_rent": "Mittlere Nettokaltmiete (Zensus-Raster).",
    "building_age_mean": "Mittleres Gebäudealter (Zensus-/OSM-Daten).",
    "dist_hospital_m": "Distanz zum nächsten Krankenhaus in Metern (OSM).",
    "dist_doctor_m": "Distanz zur nächsten Arztpraxis/Klinik in Metern (OSM).",
    "dist_pharmacy_m": "Distanz zur nächsten Apotheke in Metern (OSM).",
    "dyke_prox": "Nähe-Score zu Deich-/Küstenschutzanlagen aus der Distanz (OSM).",
    "emergency_access_score": "Erreichbarkeit von Feuerwehr/Rettung als Score aus der Distanz (OSM).",
}

COMPUTED_TOOLTIPS: dict[str, str] = {
    "pop_density": "Einwohner (Zensus) geteilt durch Zellfläche (km²).",
    "area_km2": "Zellgröße (m)² umgerechnet in km².",
    "area_ha": "Zellgröße (m)² umgerechnet in Hektar.",
    "industrial": "Kombination aus Gebäude-, Straßen- und Versiegelungsanteil.",
}

COMPUTED_RESOLVER_LINEAGE: dict[str, tuple[list[str], list[str]]] = {
    "industrial": (["bldg_cov", "road_cov", "imp_frac"], ["osm"]),
    "area_ha": ([], []),
    "area_km2": ([], []),
    "pop_density": (["pop", "area_km2"], ["zensus"]),
}

# Benannte Modellparameter, die als "param"-Quelle in CELL_INPUT_LINEAGE auftauchen
CELL_PARAM_LABELS: dict[str, tuple[str, str]] = {
    "uhi_delta": (
        "UHI-Koeffizienten (α, β, γ, δ)",
        "VDI 3787 Bl.1 / Oke 1982 — editierbar in der Konfiguration (uhi.*)",
    ),
}

COLLAPSE_GROUPS = [
    {"id": "sources", "label": "Quellen", "default_collapsed": False},
    {"id": "intermediates", "label": "Zwischenergebnisse", "default_collapsed": False},
    {"id": "indicators", "label": "H / E / V", "default_collapsed": False},
    {"id": "pathways", "label": "Wirkungsketten", "default_collapsed": False},
    {"id": "outcome", "label": "Ergebnis", "default_collapsed": False},
]


def _regional_source(label: str) -> str:
    ll = label.lower()
    if "zensus" in ll or "bevölkerung" in ll or "demo" in ll:
        return "zensus"
    if "bsh" in ll or "meeresspiegel" in ll:
        return "bsh"
    if "dwd" in ll or "wetter" in ll or "temperatur" in ll or "schnee" in ll or "regen" in ll:
        return "dwd"
    return "dwd"


class LineageBuilder:
    def __init__(self) -> None:
        self.nodes: dict[str, dict] = {}
        self.edges: list[dict] = []
        self._edge_keys: set[tuple[str, str, str | None]] = set()

    def add_node(
        self,
        node_id: str,
        ntype: str,
        label: str,
        *,
        column: int = 0,
        collapse_group: str = "intermediates",
        meta: dict | None = None,
    ) -> str:
        if node_id not in self.nodes:
            self.nodes[node_id] = {
                "id": node_id,
                "type": ntype,
                "label": label,
                "column": column,
                "collapse_group": collapse_group,
                "meta": meta or {},
            }
        return node_id

    def add_edge(
        self,
        source: str,
        target: str,
        *,
        label: str | None = None,
        parameter_id: str | None = None,
        meta: dict | None = None,
    ) -> None:
        key = (source, target, label)
        if key in self._edge_keys:
            return
        self._edge_keys.add(key)
        edge: dict[str, Any] = {
            "id": f"e:{source}:{target}:{len(self.edges)}",
            "source": source,
            "target": target,
            "label": label,
            "parameter_id": parameter_id,
        }
        if meta:
            edge["meta"] = meta
        self.edges.append(edge)

    def _wire_operator_chain(
        self,
        prefix: str,
        steps: list[dict],
        input_ids: list[str],
        target_id: str,
        *,
        cell_key_map: dict[str, str] | None = None,
    ) -> None:
        cell_key_map = dict(cell_key_map or {})
        step_outputs: dict[str, str] = dict(cell_key_map)
        last_op: str | None = None

        for i, step in enumerate(steps):
            op_id = f"op:{step['op_kind']}:{prefix}:{i}"
            _add_operator_compute(self, op_id, step)
            # Skalierungs-Konstanten ohne Registry-Parameter sind am Operator
            # nicht editierbar — der Faktor erscheint deshalb als benannter
            # (schreibgeschützter) Parameterknoten vor dem Operator.
            if (
                step.get("op_kind") in ("scaling", "scale_factor")
                and not step.get("parameter_id")
            ):
                factor = step.get("value", step.get("factor"))
                if factor is not None:
                    pnid = self.ensure_const_parameter(
                        f"const:{prefix}:{i}",
                        step.get("param_label") or "Skalierungsfaktor",
                        value=factor, unit=step.get("unit", "×"),
                        source="Modellkonstante (fest im Rechenmodell verdrahtet)",
                    )
                    self.add_edge(pnid, op_id)
            input_keys = step.get("input_keys")

            if input_keys:
                for ik in input_keys:
                    src_id = step_outputs.get(ik) or cell_key_map.get(ik) or f"int:{ik}"
                    self.add_edge(src_id, op_id)
                for ik in input_keys:
                    step_outputs[ik] = op_id
            elif i == 0:
                for pid in input_ids:
                    self.add_edge(pid, op_id)
            elif last_op:
                self.add_edge(last_op, op_id)

            last_op = op_id

        if last_op:
            self.add_edge(last_op, target_id)

    def ensure_source(self, src_key: str) -> str:
        nid = f"src:{src_key}"
        label, desc = SOURCE_IDS.get(src_key, (src_key.upper(), src_key))
        self.add_node(nid, "source", label, column=0, collapse_group="sources",
                      meta={"description": desc, "prov": "extern"})
        return nid

    def ensure_parameter(
        self,
        parameter_id: str,
        label: str,
        *,
        unit: str = "",
        source: str = "",
    ) -> str:
        nid = f"src:param:{parameter_id}"
        self.add_node(
            nid, "parameter", label, column=0, collapse_group="sources",
            meta={
                "parameter_id": parameter_id,
                "unit": unit,
                "description": source or "Modellannahme",
                "prov": "param",
            },
        )
        return nid

    def ensure_const_parameter(
        self,
        node_key: str,
        label: str,
        *,
        value: Any = None,
        unit: str = "",
        source: str = "",
        parameter_id: str | None = None,
    ) -> str:
        """Benannter Parameterknoten für Modellkonstanten.

        Zeigt Namen + Wert im Diagramm; editierbar nur, wenn eine
        ``parameter_id`` auf einen Registry-Parameter verweist (override-fähig).
        """
        nid = f"src:param:{node_key}"
        meta: dict[str, Any] = {
            "unit": unit,
            "description": source or "Modellannahme",
            "prov": "param",
        }
        if parameter_id:
            meta["parameter_id"] = parameter_id
        if value is not None:
            meta["value"] = value
        self.add_node(nid, "parameter", label, column=0, collapse_group="sources", meta=meta)
        return nid

    def expand_cell_key(self, key: str, *, _visited: set[str] | None = None) -> str:
        """Expandiert Zell-Schlüssel → Zwischenknoten → Quellen. Gibt Knoten-ID zurück."""
        if _visited is None:
            _visited = set()
        if key in _visited:
            return f"int:{key}"
        _visited.add(key)

        int_id = f"int:{key}"
        label = INTERMEDIATE_LABELS.get(key, key)
        self.add_node(int_id, "intermediate", label, column=1, collapse_group="intermediates",
                      meta={"cell_key": key})

        input_ids: list[str] = []
        cell_key_map: dict[str, str] = {}
        if key in CELL_DIRECT:
            for src in CELL_DIRECT[key]:
                input_ids.append(self.ensure_source(src))
        else:
            spec = CELL_INPUT_LINEAGE.get(key)
            if not spec:
                input_ids.append(self.ensure_source("osm"))
            else:
                intermediates, sources = spec
                for src in sources:
                    if src == "param":
                        p_label, p_desc = CELL_PARAM_LABELS.get(
                            key, ("Modellparameter", "Modellannahme"),
                        )
                        input_ids.append(self.ensure_const_parameter(
                            f"cell:{key}", p_label, source=p_desc,
                        ))
                    else:
                        input_ids.append(self.ensure_source(src))
                for sub in intermediates:
                    sub_id = self.expand_cell_key(sub, _visited=_visited)
                    cell_key_map[sub] = sub_id
                    input_ids.append(sub_id)

        steps = CELL_OPERATORS.get(key)
        if steps:
            self._wire_operator_chain(
                key, steps, input_ids, int_id, cell_key_map=cell_key_map,
            )
        else:
            for pid in input_ids:
                self.add_edge(pid, int_id)
        return int_id

    def ensure_indicator(self, code: str, category: str) -> str:
        """Indikator-Untergraph einmalig aufbauen und Knoten-ID zurückgeben."""
        ind_id = f"ind:{code}"
        if ind_id in self.nodes:
            return ind_id
        sub = build_indicator_lineage(code, category, include_norm=False)
        _merge_builder(self, sub)
        return ind_id

    def expand_computed(self, resolver_key: str, *, _visited: set[str] | None = None) -> str:
        spec = COMPUTED_RESOLVER_LINEAGE.get(resolver_key)
        if not spec:
            return self.ensure_source("computed")
        int_id = f"int:computed:{resolver_key}"
        label = INTERMEDIATE_LABELS.get(resolver_key, resolver_key)
        self.add_node(int_id, "intermediate", label, column=1, collapse_group="intermediates",
                      meta={"cell_key": resolver_key})
        intermediates, sources = spec
        input_ids: list[str] = []
        cell_key_map: dict[str, str] = {}
        for src in sources:
            input_ids.append(self.ensure_source(src))
        for sub in intermediates:
            sub_id = self.expand_cell_key(sub, _visited=_visited or set())
            cell_key_map[sub] = sub_id
            input_ids.append(sub_id)
        steps = CELL_OPERATORS.get(resolver_key)
        if steps:
            self._wire_operator_chain(
                f"computed:{resolver_key}", steps, input_ids, int_id,
                cell_key_map=cell_key_map,
            )
        else:
            for pid in input_ids:
                self.add_edge(pid, int_id)
        return int_id

    def expand_recipe_input_to_id(
        self,
        inp: dict,
        *,
        indicator_code: str | None = None,
        indicator_category: str | None = None,
    ) -> str:
        """Expandiert einen Rezept-Input und gibt die Blatt-Knoten-ID zurück."""
        prov = inp.get("prov", formulas.EXTERN)
        src_type = inp.get("source", "cell")
        key = inp.get("key", "")

        if src_type == "const" or prov == formulas.PARAM:
            # Jeder Formel-Parameter wird benannt (Label + Wert) angezeigt;
            # editierbar (parameter_id) nur, wenn override-fähig in der Registry.
            label = inp.get("label") or key or "Modellannahme"
            if key.startswith("__") or not key:
                return self.ensure_const_parameter(
                    f"const:{indicator_code or 'global'}:{label}", label,
                    value=inp.get("value"), unit=inp.get("unit", ""),
                    source=inp.get("doc_source") or "Modellannahme (Formelrezept)",
                )
            pid: str | None = None
            if inp.get("overridable"):
                pid = (
                    f"{indicator_category}.{indicator_code}.param.{key}"
                    if indicator_code and indicator_category
                    else key
                )
            return self.ensure_const_parameter(
                f"param:{indicator_category or ''}.{indicator_code or ''}.{key}", label,
                value=inp.get("value"), unit=inp.get("unit", ""),
                source=inp.get("doc_source") or "Modellannahme (Formelrezept)",
                parameter_id=pid,
            )

        if src_type == "regional":
            return self.ensure_source(_regional_source(inp.get("label", "")))

        if src_type == "demo":
            return self.ensure_source("zensus")

        if src_type == "computed":
            resolver = inp.get("value") or key
            return self.expand_computed(str(resolver))

        if src_type == "hev":
            ref_code = str(inp.get("value") or key).upper()
            if ref_code in catalog.HAZARDS_BY_CODE:
                cat = "hazards"
            elif ref_code in catalog.EXPOSURES_BY_CODE:
                cat = "exposures"
            elif ref_code in catalog.VULNERABILITIES_BY_CODE:
                cat = "vulnerabilities"
            else:
                cat = "hazards"
            return self.ensure_indicator(ref_code, cat)

        if src_type == "cell" or src_type == "auxiliary":
            cell_key = key if key and not key.startswith("__") else None
            if not cell_key:
                label = inp.get("label", "")
                for ck in CELL_INPUT_LINEAGE:
                    if ck in label.lower().replace(" ", "_"):
                        cell_key = ck
                        break
            if cell_key:
                return self.expand_cell_key(cell_key)
            return self.ensure_source("osm")

        return self.ensure_source("osm")

    def expand_recipe_input(self, inp: dict, target_id: str) -> None:
        sid = self.expand_recipe_input_to_id(inp)
        self.add_edge(sid, target_id)

    def build(self) -> dict:
        return {
            "nodes": list(self.nodes.values()),
            "edges": self.edges,
            "collapse_groups": COLLAPSE_GROUPS,
        }


def _indicator_node_type(category: str) -> str:
    if category == "hazards":
        return "hazard"
    if category == "exposures":
        return "exposure"
    if category == "vulnerabilities":
        return "vulnerability"
    return "intermediate"


def _incoming_labels(
    node_id: str,
    edges: list[dict],
    nodes_by_id: dict[str, dict],
) -> list[str]:
    labels: list[str] = []
    for e in edges:
        if e["target"] != node_id:
            continue
        src = nodes_by_id.get(e["source"])
        if src:
            labels.append(src["label"])
    return labels


def _indicator_tooltip(code: str, unit: str) -> str:
    recipe = formulas.get_recipe(code)
    formula = recipe.get("formula", "")
    inputs = [
        inp.get("label", inp.get("key", ""))
        for inp in recipe.get("inputs", [])
        if inp.get("key") != "__source"
    ]
    lines = [f"Berechnung: {formula}" if formula else "Berechnung aus Eingabewerten"]
    if inputs:
        lines.append(f"Eingaben: {', '.join(inputs)}")
    if unit:
        lines.append(f"Einheit: {unit}")
    lo = catalog.INDICATOR_BY_CODE.get(code, {}).get("norm_min")
    hi = catalog.INDICATOR_BY_CODE.get(code, {}).get("norm_max")
    if lo is not None and hi is not None:
        lines.append(f"Normierung: Skala {lo}…{hi}")
    return "\n".join(lines)


def _tooltip_for_node(
    node: dict,
    nodes_by_id: dict[str, dict],
    edges: list[dict],
) -> str:
    ntype = node["type"]
    meta = node.get("meta") or {}
    label = node["label"]
    nid = node["id"]
    incoming = _incoming_labels(nid, edges, nodes_by_id)

    if ntype == "source":
        desc = meta.get("description", "Externe Datenquelle")
        return f"{label}\n{desc}\nWird als Eingabe in nachfolgende Merkmale eingespeist."

    if ntype == "intermediate":
        cell_key = meta.get("cell_key", "")
        if nid.startswith("int:computed:"):
            resolver = nid.split("int:computed:", 1)[-1]
            base = COMPUTED_TOOLTIPS.get(resolver, f"Berechneter Zwischenwert ({label}).")
        else:
            base = INTERMEDIATE_TOOLTIPS.get(cell_key, f"Zellbezogener Zwischenwert ({label}).")
        if incoming:
            return f"{base}\nEingaben: {', '.join(incoming)}"
        return base

    if ntype in ("hazard", "exposure", "vulnerability"):
        code = meta.get("code", "")
        if code:
            return _indicator_tooltip(code, meta.get("unit", ""))
        formula = meta.get("formula", "")
        if formula:
            lines = [f"Berechnung: {formula}"]
            if incoming:
                lines.append(f"Eingaben: {', '.join(incoming)}")
            return "\n".join(lines)

    if ntype == "pathway":
        chain = meta.get("chain_label", "")
        type_label = meta.get("type_label", "")
        weight = meta.get("weight")
        lines = [label]
        if chain:
            lines.append(f"Zusammensetzung: {chain}")
        if type_label:
            lines.append(f"Typ: {type_label}")
        weight_str = f"{weight:g}" if isinstance(weight, (int, float)) else "Gewicht"
        lines.append(
            f"Berechnung: {weight_str} · normierte Gefahr · Betroffenheit · Empfindlichkeit"
        )
        return "\n".join(lines)

    if ntype == "operator":
        kind = meta.get("op_kind", "")
        tooltip = meta.get("tooltip", "")
        label_op = meta.get("label", "")
        if kind == "scaling":
            src = meta.get("source", "")
            val = meta.get("value")
            unit = meta.get("unit", "")
            scale = meta.get("scale", "pop")
            lines = ["Skalierung", f"Referenzwert: {val:g} {unit}".strip()]
            if src:
                lines.append(f"Quelle: {src}")
            lines.append(f"Berechnung: {_SCALE_FORMULAS.get(scale, _SCALE_FORMULAS['flat'])}")
            return "\n".join(lines)
        if kind == "multiply":
            return tooltip or "Multiplikation: Gefahr × Betroffenheit × Empfindlichkeit"
        if kind == "max":
            return tooltip or (
                "Stärkste Wirkungskette (0–100): Index = 100 · max(Gewicht · Ĥ · Ê · V̂)."
            )
        if kind == "norm":
            lo, hi = meta.get("norm_min"), meta.get("norm_max")
            unit = meta.get("unit", "")
            src = meta.get("source", "")
            lines = [
                "Normierung",
                f"Untergrenze {lo} {unit} → normiert 0".strip(),
                f"Obergrenze {hi} {unit} → normiert 1".strip(),
            ]
            if src:
                lines.append(f"Quelle: {src}")
            return "\n".join(lines)
        if kind in ("count", "coverage", "neighbor", "clamp", "add", "divide",
                    "scale_factor", "max", "min", "weighted_sum", "formula"):
            lines = [label_op or kind]
            if tooltip:
                lines.append(tooltip)
            if incoming:
                lines.append(f"Eingaben: {', '.join(incoming)}")
            return "\n".join(lines)
        if kind == "multiplier":
            return _tooltip_for_node(
                {**node, "meta": {**meta, "op_kind": "scaling"}}, nodes_by_id, edges,
            )

    if ntype == "aggregation":
        short = meta.get("short", "stärkste Wirkungskette (Maximum)")
        formula = meta.get("formula", "")
        lines = [f"{label}: {short}"]
        if formula:
            lines.append(f"Berechnung: {formula}")
        if incoming:
            lines.append(f"Eingaben: {', '.join(incoming)}")
        return "\n".join(lines)

    if ntype in ("outcome", "norm"):
        if meta.get("is_norm"):
            lo, hi = meta.get("norm_min"), meta.get("norm_max")
            unit = meta.get("unit", "")
            return (
                f"Normiertes Ergebnis auf Skala {lo}…{hi} {unit}".strip()
                + (f"\nEingaben: {', '.join(incoming)}" if incoming else "")
            )
        formula = meta.get("formula", "")
        ref = meta.get("ref_value")
        unit = meta.get("unit", "")
        result_kind = meta.get("result_kind")
        lines = [label]
        if result_kind == "index":
            header = meta.get("formula_header", "")
            lines.append("Screening-Ergebnis (Schicht A), dimensionslos 0–100.")
            if header:
                lines.append(header)
        elif result_kind == "native":
            lines.append(f"Absolutes Ergebnis (Schicht B) in {unit}".strip() + ".")
        elif result_kind == "eur":
            lines.append("Monetäres Ergebnis (Schicht B) in €/Jahr.")
            cost_src = meta.get("cost_source", "")
            if cost_src:
                lines.append(f"Kostensatz-Quelle: {cost_src}")
        if ref is not None:
            lines.append(f"Referenzfall: {ref:g} {unit}".strip())
        if formula:
            lines.append(f"Berechnung: {formula}")
        elif incoming and result_kind is None:
            lines.append(f"Eingaben: {', '.join(incoming)}")
        return "\n".join(lines)

    if incoming:
        return f"{label}\nEingaben: {', '.join(incoming)}"
    return label


def _add_operator_compute(
    b: "LineageBuilder",
    op_id: str,
    step: dict,
    *,
    collapse_group: str = "intermediates",
) -> str:
    meta: dict[str, Any] = {
        "op_kind": step["op_kind"],
        "label": step.get("label", ""),
        "tooltip": step.get("tooltip", ""),
    }
    for k, v in step.items():
        if k not in ("op_kind", "label", "tooltip", "input_keys"):
            meta[k] = v
    b.add_node(op_id, "operator", "", column=0, collapse_group=collapse_group, meta=meta)
    return op_id


_SCALE_FORMULAS = {
    "pop": "Index/100 · Einwohner_zelle/100.000",
    "area": "Index/100 · Fläche/50 km²",
    "flat": "Outcome = Referenz · (P90-Index/100)",
}

_SCALE_SOURCES = {
    "pop": "Referenz-Outcome bei Index 100 / 100.000 Ew. (Risikokatalog)",
    "area": "Referenz-Outcome bei Index 100 / 50 km² (Risikokatalog)",
    "flat": "Referenz-Outcome bei P90-Index 100, kommunenweit (Risikokatalog)",
}


def _add_operator_scaling(
    b: "LineageBuilder",
    risk_code: str,
    ref: float,
    unit: str,
    scale: str = "pop",
) -> str:
    op_id = f"op:scaling:{risk_code}"
    b.add_node(
        op_id, "operator", "",
        column=0, collapse_group="outcome",
        meta={
            "op_kind": "scaling",
            "parameter_id": f"risks.{risk_code}.ref_value",
            "value": ref,
            "unit": unit,
            "scale": scale,
            "source": _SCALE_SOURCES.get(scale, _SCALE_SOURCES["flat"]),
            "tooltip": "Skalierung des Indexes auf den Referenz-Outcome.",
        },
    )
    return op_id


def _add_operator_multiply(b: "LineageBuilder", op_id: str) -> str:
    b.add_node(
        op_id, "operator", "",
        column=0, collapse_group="pathways",
        meta={
            "op_kind": "multiply",
            "label": "×",
            "tooltip": (
                "Gefahr × Betroffenheit × Empfindlichkeit (jeweils normiert 0…1; "
                "Normierungsgrenzen im Diagramm des jeweiligen Einflusses).\n"
                r"$$\hat{H} \cdot \hat{E} \cdot \hat{V}$$"
            ),
        },
    )
    return op_id


def _add_operator_max(b: "LineageBuilder") -> str:
    op_id = "op:max:index"
    b.add_node(
        op_id, "operator", "",
        column=0, collapse_group="outcome",
        meta={
            "op_kind": "max",
            "label": "Maximum",
            "tooltip": (
                "Stärkste Wirkungskette (0–100): Die Kette mit dem höchsten gewichteten "
                "Produkt bestimmt den Index; die Kettenzahl beeinflusst ihn nicht.\n"
                r"$$\mathrm{Index} = 100 \cdot \max_{p}\,\bigl(w_{p} \cdot \hat{H} \cdot \hat{E} \cdot \hat{V}\bigr)$$"
            ),
        },
    )
    return op_id


def _add_operator_multiplier(
    b: "LineageBuilder",
    risk_code: str,
    ref: float,
    unit: str,
    scale: str = "pop",
) -> str:
    return _add_operator_scaling(b, risk_code, ref, unit, scale)


def _add_operator_norm(
    b: "LineageBuilder",
    code: str,
    category: str,
    lo: float,
    hi: float,
    unit: str,
    source: str = "",
) -> str:
    op_id = f"op:norm:{code}"
    b.add_node(
        op_id, "operator", "",
        column=0, collapse_group="outcome",
        meta={
            "op_kind": "norm",
            "norm_min": lo,
            "norm_max": hi,
            "unit": unit,
            "param_min_id": f"{category}.{code}.norm_min",
            "param_max_id": f"{category}.{code}.norm_max",
            "source": source or "Risikokatalog (Normierungsskala)",
        },
    )
    return op_id


def _add_operator_weight(
    b: "LineageBuilder",
    pathway_idx: int,
    pathway_type: str,
    weight: float,
) -> str:
    """Gewichte werden auf Kanten (Pfad → Maximum) gelegt."""
    return f"op:weight:{pathway_idx}"




def _assign_layout_rows(graph: dict) -> dict:
    """Horizontale Zeilen pro Zwischenwert-Kette (meta.layout_row)."""
    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])

    row_by_int: dict[str, int] = {}
    row_cursor = 0
    for n in sorted(nodes, key=lambda x: x.get("label", "")):
        if n["type"] != "intermediate":
            continue
        ck = (n.get("meta") or {}).get("cell_key") or n["id"]
        if ck not in row_by_int:
            row_by_int[ck] = row_cursor
            row_cursor += 1

    node_row: dict[str, int] = {}
    for n in nodes:
        if n["type"] == "intermediate":
            ck = (n.get("meta") or {}).get("cell_key") or n["id"]
            node_row[n["id"]] = row_by_int.get(ck, 0)

    incoming: dict[str, list[str]] = {}
    outgoing: dict[str, list[str]] = {}
    for e in edges:
        incoming.setdefault(e["target"], []).append(e["source"])
        outgoing.setdefault(e["source"], []).append(e["target"])

    pipeline_types = {"source", "parameter", "intermediate", "operator"}

    def rows_of(node_ids: list[str]) -> list[int]:
        return [node_row[nid] for nid in node_ids if nid in node_row]

    for _ in range(len(nodes) + 2):
        changed = False
        for n in nodes:
            nid = n["id"]
            if nid in node_row or n["type"] not in pipeline_types:
                continue
            preds = rows_of(incoming.get(nid, []))
            if preds:
                if n["type"] == "operator" and len(preds) > 1:
                    node_row[nid] = max(preds)
                else:
                    node_row[nid] = preds[0]
                changed = True
        for n in nodes:
            nid = n["id"]
            if nid in node_row or n["type"] not in ("source", "parameter"):
                continue
            succ_rows = rows_of(outgoing.get(nid, []))
            if succ_rows:
                node_row[nid] = min(succ_rows)
                changed = True
        if not changed:
            break

    for _ in range(len(nodes) + 2):
        changed = False
        for e in edges:
            src, tgt = e["source"], e["target"]
            if tgt in node_row and src not in node_row:
                sn = next((n for n in nodes if n["id"] == src), None)
                if sn and sn["type"] in pipeline_types:
                    node_row[src] = node_row[tgt]
                    changed = True
            elif src in node_row and tgt not in node_row:
                tn = next((n for n in nodes if n["id"] == tgt), None)
                if tn and tn["type"] in pipeline_types:
                    node_row[tgt] = node_row[src]
                    changed = True
        if not changed:
            break

    for n in nodes:
        rid = node_row.get(n["id"])
        if rid is not None:
            n.setdefault("meta", {})["layout_row"] = rid

    return graph


def _assign_columns(graph: dict) -> dict:
    """Longest-Path-Layering: col(n) = max(col(pred)) + 1 (Quellen/Parameter = 0).

    Garantiert col(src) < col(tgt) für JEDE Kante (Pfeile strikt links→rechts);
    Ergebnisknoten ohne ausgehende Kante werden rechtsbündig auf die maximale
    Spalte gesetzt (Index-/€-Ergebnis nebeneinander am rechten Rand).
    """
    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])
    cols: dict[str, int] = {n["id"]: 0 for n in nodes}
    for _ in range(len(nodes) + 4):
        changed = False
        for e in edges:
            src, tgt = e["source"], e["target"]
            if src in cols and tgt in cols:
                new_col = cols[src] + 1
                if new_col > cols[tgt]:
                    cols[tgt] = new_col
                    changed = True
        if not changed:
            break
    has_outgoing = {e["source"] for e in edges}
    max_col = max(cols.values(), default=0)
    for n in nodes:
        if n["type"] == "outcome" and n["id"] not in has_outgoing:
            cols[n["id"]] = max_col
        n["column"] = cols.get(n["id"], 0)
    return graph


def _finalize_graph(graph: dict) -> dict:
    graph = _assign_columns(graph)
    graph = _assign_layout_rows(graph)
    return _enrich_tooltips(graph)


def _enrich_tooltips(graph: dict) -> dict:
    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])
    nodes_by_id = {n["id"]: n for n in nodes}
    for n in nodes:
        meta = n.setdefault("meta", {})
        if not meta.get("tooltip"):
            meta["tooltip"] = _tooltip_for_node(n, nodes_by_id, edges)
    return graph


def _find_result_ids(nodes: list[dict]) -> list[str]:
    """Alle Ergebnisknoten (Outcome); Fallback: rechtester Norm-Op/Norm-Knoten."""
    result_ids = [n["id"] for n in nodes if n["type"] == "outcome"]
    if result_ids:
        return result_ids
    norm_ops = [
        n for n in nodes
        if n["type"] == "operator" and (n.get("meta") or {}).get("op_kind") == "norm"
    ]
    if norm_ops:
        return [max(norm_ops, key=lambda n: n.get("column", 0))["id"]]
    norms = [n for n in nodes if n["type"] == "norm"]
    if norms:
        return [max(norms, key=lambda n: n.get("column", 0))["id"]]
    return []


def _prune_lineage(graph: dict) -> dict:
    """Entfernt Knoten, die auf keinem Pfad zu einem Ergebnisknoten liegen."""
    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])
    result_ids = _find_result_ids(nodes)
    if not result_ids:
        return _finalize_graph(graph)

    rev: dict[str, list[str]] = {}
    for e in edges:
        rev.setdefault(e["target"], []).append(e["source"])

    reachable: set[str] = set()
    stack = list(result_ids)
    while stack:
        nid = stack.pop()
        if nid in reachable:
            continue
        reachable.add(nid)
        stack.extend(rev.get(nid, []))

    nodes2 = [n for n in nodes if n["id"] in reachable]
    ids = {n["id"] for n in nodes2}
    edges2 = [e for e in edges if e["source"] in ids and e["target"] in ids]
    return _finalize_graph({**graph, "nodes": nodes2, "edges": edges2})


def build_indicator_lineage(code: str, category: str, *, include_norm: bool = True) -> dict:
    """Quellen → Zwischen → Indikator → (optional) Normierung."""
    b = LineageBuilder()
    meta = catalog.INDICATOR_BY_CODE.get(code) or catalog.AUXILIARY_BY_CODE.get(code, {})
    name = meta.get("name", code)
    ntype = _indicator_node_type(category) if category != "auxiliary" else "intermediate"

    ind_id = f"ind:{code}"
    b.add_node(
        ind_id, ntype, name, column=2, collapse_group="indicators",
        meta={
            "code": code,
            "unit": meta.get("unit", ""),
            "formula": formulas.get_recipe(code).get("formula", ""),
            "norm_min": meta.get("norm_min"),
            "norm_max": meta.get("norm_max"),
        },
    )

    recipe = formulas.get_recipe(code)
    steps = formula_operators_for(code, recipe.get("formula", ""))
    input_ids: list[str] = []
    param_ids: list[str] = []
    cell_key_map: dict[str, str] = {}
    for inp in recipe.get("inputs", []):
        if inp.get("key") == "__source":
            src_label = inp.get("label", "")
            if "OSM" in src_label:
                sid = b.ensure_source("osm")
            elif "DWD" in src_label:
                sid = b.ensure_source("dwd")
            else:
                sid = b.ensure_source("param")
            input_ids.append(sid)
            continue
        if inp.get("prov") == formulas.PARAM:
            # Trägt ein Operator-Schritt den Wert bereits sichtbar (z. B. Skalierung
            # ×1,5 bei HEAT_WAVE), keinen doppelten Parameterknoten erzeugen.
            val = inp.get("value")
            if val is not None and any(
                st.get("factor") == val or st.get("value") == val for st in steps
            ):
                continue
            pnid = b.expand_recipe_input_to_id(
                inp, indicator_code=code, indicator_category=category,
            )
            param_ids.append(pnid)
            input_ids.append(pnid)
            continue
        iid = b.expand_recipe_input_to_id(inp, indicator_code=code, indicator_category=category)
        key = inp.get("key", "")
        if key and not key.startswith("__"):
            cell_key_map[key] = iid
        input_ids.append(iid)

    if steps and input_ids:
        b._wire_operator_chain(
            f"ind:{code}", steps, input_ids, ind_id, cell_key_map=cell_key_map,
        )
        for i, step in enumerate(steps):
            pid = step.get("parameter_id")
            if pid and step.get("op_kind") in ("scaling", "multiplier"):
                param_nid = b.ensure_parameter(
                    pid,
                    step.get("label", "Skalierung"),
                    unit=step.get("unit", ""),
                    source="Modellannahme (Formelrezept)",
                )
                op_id = f"op:{step['op_kind']}:ind:{code}:{i}"
                b.add_edge(param_nid, op_id)
        # Parameterknoten, die die Verkettung über input_keys nicht angeschlossen
        # hat, explizit an den ersten Operator hängen (sonst hingen sie lose).
        first_op_id = f"op:{steps[0]['op_kind']}:ind:{code}:0"
        connected = {e["source"] for e in b.edges}
        for pnid in param_ids:
            if pnid not in connected:
                b.add_edge(pnid, first_op_id)
    else:
        for iid in input_ids:
            b.add_edge(iid, ind_id)

    if include_norm and meta.get("norm_min") is not None:
        lo, hi = meta.get("norm_min"), meta.get("norm_max")
        unit = meta.get("unit", "")
        op_id = _add_operator_norm(
            b, code, category, lo, hi, unit, meta.get("source", ""),
        )
        b.add_edge(ind_id, op_id)
        out_id = f"out:norm:{code}"
        b.add_node(
            out_id, "outcome", "Normierter Wert",
            column=0, collapse_group="outcome",
            meta={
                "result_kind": "index",
                "unit": "0–1",
                "formula": f"normiert({lo}…{hi} {unit}) → 0…1".strip(),
                "is_outcome": True,
            },
        )
        b.add_edge(op_id, out_id)

    return _prune_lineage(b.build())


def _merge_builder(target: LineageBuilder, other: dict) -> None:
    for n in other["nodes"]:
        target.add_node(
            n["id"], n["type"], n["label"],
            column=n.get("column", 0),
            collapse_group=n.get("collapse_group", "intermediates"),
            meta=n.get("meta"),
        )
    for e in other["edges"]:
        target.add_edge(
            e["source"], e["target"],
            label=e.get("label"),
            parameter_id=e.get("parameter_id"),
            meta=e.get("meta"),
        )


# ── Schicht B: Bausteine für den Impact-Zweig des Wirkungsdiagramms ─────────────

def _risk_lineage_kind(risk: dict) -> str:
    """Kategorisiert das Risiko nach seinem tatsächlichen Schicht-B-Rechenweg."""
    from app.services.engine import impact
    return impact.lineage_kind(risk)


def _impact_param_node(b: LineageBuilder, risk_code: str, key: str) -> str:
    spec = _IMPACT_PARAM_BY_KEY.get((risk_code, key), {})
    return b.ensure_parameter(
        f"risks.{risk_code}.impact.{key}",
        spec.get("label", key),
        unit=spec.get("unit", ""),
        source=spec.get("source", "Modellannahme (Schicht B)"),
    )


def _global_param_node(b: LineageBuilder, key: str) -> str:
    spec = _IMPACT_GLOBAL_BY_KEY.get(key, {})
    return b.ensure_parameter(
        f"impact.{key}",
        spec.get("label", key),
        unit=spec.get("unit", ""),
        source=spec.get("source", "Modellannahme (Schicht B)"),
    )


def _add_op(
    b: LineageBuilder,
    op_id: str,
    op_kind: str,
    label: str,
    tooltip: str,
    *,
    collapse_group: str = "outcome",
) -> str:
    b.add_node(op_id, "operator", "", column=0, collapse_group=collapse_group,
               meta={"op_kind": op_kind, "label": label, "tooltip": tooltip})
    return op_id


def _add_intensity_op(
    b: LineageBuilder, code: str, hazards: list[str], *, op_id: str | None = None,
) -> str:
    op_id = op_id or f"op:intensity:{code}"
    _add_op(
        b, op_id, "intensity", "Intensität",
        "Normierte Hazard-Intensität (0–1) mit FIXEN Katalog-Referenzgrenzen — "
        "unabhängig von der editierbaren Screening-Normierung (§3.3). Bei mehreren "
        "Gefahren zählt die stärkste (Maximum).",
    )
    for h in hazards:
        b.add_edge(b.ensure_indicator(h, "hazards"), op_id)
    return op_id


def _add_af_op(b: LineageBuilder, code: str, driver: dict) -> str:
    op_id = f"op:af:{code}"
    _add_op(
        b, op_id, "af", "AF",
        "Attributable Fraktion: Anteil des Outcomes, der den Hitzetagen zuzurechnen "
        "ist (0…1). Unterhalb der Schwelle 0, oberhalb sättigend (RKI/Winklmayr 2022).\n"
        r"$$AF = 1 - e^{-\beta\,(H_{\mathrm{Tage}} - H_{0})_{+}}$$",
    )
    b.add_edge(b.ensure_indicator(driver["hazard"], "hazards"), op_id)
    for pkey in driver.get("params", []):
        b.add_edge(_impact_param_node(b, code, pkey), op_id)
    return op_id


def _add_driver_op(b: LineageBuilder, code: str, driver: dict) -> str:
    """Treiber-Operator des Schicht-B-Zweigs, exakt nach ``LINEAGE_SPECS``."""
    kind = driver["kind"]
    if kind == "intensity":
        return _add_intensity_op(b, code, driver["hazards"])
    if kind == "af":
        return _add_af_op(b, code, driver)
    if kind == "ratio":
        op_id = f"op:ratio:{code}"
        _add_op(
            b, op_id, "ratio", "÷ Referenz",
            "Linearer Treiber: Hitzetage der Zelle ÷ Referenz-Hitzetage.\n"
            r"$$\mathrm{Treiber} = H_{\mathrm{Tage}} / H_{\mathrm{Referenz}}$$",
        )
        b.add_edge(b.ensure_indicator(driver["hazard"], "hazards"), op_id)
        for pkey in driver.get("params", []):
            b.add_edge(_impact_param_node(b, code, pkey), op_id)
        return op_id
    if kind == "af_plus_event":
        af_id = _add_af_op(b, code, driver)
        ev_id = _add_intensity_op(
            b, code, driver["event_hazards"], op_id=f"op:eventintensity:{code}",
        )
        add_id = f"op:afevent:{code}"
        _add_op(
            b, add_id, "add", "+",
            "Treiber = AF + Ereignis-Anteil · Ereignisintensität (gedeckelt bei 1).",
        )
        b.add_edge(af_id, add_id)
        b.add_edge(ev_id, add_id)
        # Ereignis-Anteil als editierbarer Parameterknoten (risks.<code>.impact.<key>).
        share_param = driver.get("event_share_param")
        if share_param:
            b.add_edge(_impact_param_node(b, code, share_param), add_id)
        return add_id
    raise ValueError(f"Unbekannter Schicht-B-Treiber: {kind}")


def _add_gv_op(b: LineageBuilder, risk: dict) -> str:
    op_id = f"op:gv:{risk['code']}"
    _add_op(
        b, op_id, "gv", "g(V̂)",
        "Vulnerabilitäts-Modifikator aus dem Mittel der normierten Sensitivitäten des "
        "Risikos: hebt/senkt den Zell-Outcome um Faktor 0,5…1,5.\n"
        r"$$g(\hat{V}) = 0{,}5 + \overline{\hat{V}}$$",
    )
    for vcode in risk.get("vulnerabilities", []):
        b.add_edge(b.ensure_indicator(vcode, "vulnerabilities"), op_id)
    return op_id


def _add_sum_cells_op(b: LineageBuilder, code: str) -> str:
    return _add_op(
        b, f"op:sumcells:{code}", "sum_cells", "Σ Zellen",
        "Summe der Zell-Outcomes über alle 100×100-m-Rasterzellen der Kommune (Schicht B).\n"
        r"$$O = \sum_{\mathrm{Zellen}} O_{z}$$",
    )


def _add_cost_op(b: LineageBuilder, risk: dict, *, extra_tooltip: str = "") -> str:
    code = risk["code"]
    rate = catalog.risk_default_cost_per_outcome(risk)
    unit = catalog.cost_unit_label(risk.get("outcome_unit", ""))
    src = risk.get("cost_source") or ""
    tooltip = (
        "Monetarisierung des Outcomes über den editierbaren Kostensatz.\n"
        r"$$\text{€} = O \cdot \text{Kostensatz}$$"
    )
    if src:
        tooltip += f"\nQuelle: {src}"
    if extra_tooltip:
        tooltip += f"\n{extra_tooltip}"
    op_id = f"op:cost:{code}"
    b.add_node(
        op_id, "operator", "",
        column=0, collapse_group="outcome",
        meta={
            "op_kind": "scaling",
            "label": "Kostensatz",
            "parameter_id": f"risks.{code}.cost_per_outcome",
            "value": rate,
            "unit": unit,
            "scale": "cost",
            "source": src or "Kostensatz (Risikokatalog)",
            "tooltip": tooltip,
        },
    )
    return op_id


def _area_basis(b: LineageBuilder, code: str, keys: list[str], label: str) -> str:
    if len(keys) == 1:
        return b.expand_cell_key(keys[0])
    labels = [INTERMEDIATE_LABELS.get(k, k) for k in keys]
    area_id = f"int:area:{code}"
    b.add_node(
        area_id, "intermediate", label,
        column=1, collapse_group="intermediates",
        meta={"tooltip": f"{label} = {' + '.join(labels)} (× 1 ha Zellfläche)."},
    )
    op_id = _add_op(
        b, f"op:addarea:{code}", "add", "+",
        f"Summe der Flächenanteile: {' + '.join(labels)}.",
        collapse_group="intermediates",
    )
    for k in keys:
        b.add_edge(b.expand_cell_key(k), op_id)
    b.add_edge(op_id, area_id)
    return area_id


def _asset_basis(b: LineageBuilder, code: str, asset: dict) -> str:
    kind = asset["kind"]
    label = asset.get("label", "Assetwert (Zelle)")
    if kind == "building":
        tip = ("Gebäude-Assetwert = Geschossfläche (Gebäudeanteil × Zellfläche × "
               "Geschosse aus mittlerer Höhe) × Gebäudewert je m².")
    elif kind == "count":
        tip = "Assetwert = Anzahl Anlagen in der Zelle × Ersatzwert je Stück."
    else:
        tip = "Assetwert = Flächenanteil × 1 ha Zellfläche × Wert je ha."
    asset_id = f"int:asset:{code}"
    b.add_node(
        asset_id, "intermediate", label,
        column=1, collapse_group="intermediates",
        meta={"tooltip": tip},
    )
    op_id = _add_op(b, f"op:asset:{code}", "multiply", "×", tip,
                    collapse_group="intermediates")
    for k in asset["cell_keys"]:
        b.add_edge(b.expand_cell_key(k), op_id)
    b.add_edge(_global_param_node(b, asset["value_param"]), op_id)
    b.add_edge(op_id, asset_id)
    return asset_id


def _build_impact_branch(
    b: LineageBuilder, risk: dict, kind: str, idx_id: str,
) -> None:
    """Schicht-B-Zweig: Quellen → Schadensfunktion → (natives Ergebnis) → €."""
    code = risk["code"]
    unit = risk.get("outcome_unit", "")

    def add_eur(formula: str, *, non_additive: bool = False) -> str:
        meta: dict[str, Any] = {
            "result_kind": "eur",
            "unit": "€/Jahr",
            "formula": formula,
            "is_outcome": True,
            "cost_source": risk.get("cost_source", ""),
        }
        if non_additive:
            meta["non_additive"] = True
        b.add_node("out:eur", "outcome", "Monetärer Schaden",
                   column=0, collapse_group="outcome", meta=meta)
        return "out:eur"

    def add_native(formula: str) -> str:
        b.add_node(
            "out:native", "outcome", unit or "Outcome",
            column=0, collapse_group="outcome",
            meta={"result_kind": "native", "unit": unit, "formula": formula,
                  "is_outcome": True},
        )
        return "out:native"

    if kind == "index_only":
        return

    if kind in ("health", "environment"):
        if kind == "health":
            spec = HEALTH_SPECS[code]
            basis = b.expand_cell_key("pop")
            product = "Bevölkerung · Rate · Treiber · g(V̂)"
            latex = r"$$O_{z} = \text{Bevölkerung}_{z} \cdot \text{Rate} \cdot \text{Treiber}_{z} \cdot g(\hat{V})$$"
        else:
            spec = ENV_SPECS[code]
            basis = _area_basis(b, code, spec["area_keys"], "Exponierte Naturfläche (Zelle)")
            product = "exponierte Fläche · Verlustrate · Intensität · g(V̂)"
            latex = r"$$O_{z} = \text{Fläche}_{z} \cdot \text{Verlustrate} \cdot I_{z} \cdot g(\hat{V})$$"
        mul_id = _add_op(b, f"op:mulB:{code}", "multiply", "×",
                         f"Zell-Outcome = {product}.\n{latex}")
        b.add_edge(basis, mul_id)
        b.add_edge(_impact_param_node(b, code, spec["rate_param"]), mul_id)
        b.add_edge(_add_driver_op(b, code, spec["driver"]), mul_id)
        b.add_edge(_add_gv_op(b, risk), mul_id)
        sum_id = _add_sum_cells_op(b, code)
        b.add_edge(mul_id, sum_id)
        native_id = add_native(f"Outcome = {product}, Σ Zellen")
        b.add_edge(sum_id, native_id)
        cost_id = _add_cost_op(b, risk)
        b.add_edge(native_id, cost_id)
        b.add_edge(cost_id, add_eur("€ = Outcome × Kostensatz"))
        return

    if kind == "monetary":
        spec = MONETARY_SPECS[code]
        if spec.get("basis_pop"):
            # Klimamigration: Bevölkerungs-Muster, Outcome ist direkt €.
            mul_id = _add_op(
                b, f"op:mulB:{code}", "multiply", "×",
                "Zell-Kosten (€) = (Einwohner/100.000) · Referenzkosten · Intensität · g(V̂).\n"
                r"$$K_{z} = \frac{\text{Einwohner}_{z}}{100\,000} \cdot \text{Referenzkosten} \cdot I_{z} \cdot g(\hat{V})$$",
            )
            b.add_edge(b.expand_cell_key("pop"), mul_id)
            b.add_edge(_impact_param_node(b, code, spec["rate_param"]), mul_id)
            b.add_edge(_add_driver_op(b, code, spec["driver"]), mul_id)
            b.add_edge(_add_gv_op(b, risk), mul_id)
            sum_id = _add_sum_cells_op(b, code)
            b.add_edge(mul_id, sum_id)
            b.add_edge(sum_id, add_eur(
                "€ = (Einwohner/100.000) · Referenzkosten · Intensität · g(V̂), Σ Zellen"))
            return
        basis = _asset_basis(b, code, spec["asset"])
        damage_id = _add_op(
            b, f"op:damage:{code}", "damage_curve", "Schadenskurve",
            "Konvexe Schadenskurve: überproportionaler Schaden bei hoher Intensität "
            "(HOWAS21/JRC).\n"
            r"$$s = I^{\,\gamma},\quad \gamma > 1$$",
        )
        b.add_edge(_add_intensity_op(b, code, spec["driver"]["hazards"]), damage_id)
        b.add_edge(_global_param_node(b, "damage_exponent"), damage_id)
        mul_id = _add_op(
            b, f"op:mulB:{code}", "multiply", "×",
            "Zell-Schaden (€) = Assetwert · max. Verlustrate · Schadenskurve(Intensität) · g(V̂).\n"
            r"$$S_{z} = A_{z} \cdot r_{\max} \cdot s(I_{z}) \cdot g(\hat{V})$$",
        )
        b.add_edge(basis, mul_id)
        b.add_edge(_impact_param_node(b, code, spec["loss_param"]), mul_id)
        b.add_edge(damage_id, mul_id)
        b.add_edge(_add_gv_op(b, risk), mul_id)
        sum_id = _add_sum_cells_op(b, code)
        b.add_edge(mul_id, sum_id)
        b.add_edge(sum_id, add_eur(
            "€ = Assetwert · Verlustrate · Schadenskurve(Intensität) · g(V̂), Σ Zellen"))
        return

    if kind in ("indirect", "restoration"):
        direct_id = "int:direct_sum"
        names = [
            catalog.RISKS_BY_CODE[c]["name"]
            for c in sorted(catalog.DIRECT_SECTOR_RISK_CODES)
        ]
        b.add_node(
            direct_id, "intermediate", "Direkte Sektorschäden (Σ €)",
            column=1, collapse_group="intermediates",
            meta={"tooltip": "Summe der direkten Sektorschäden je Zelle (Schicht B): "
                             + ", ".join(names) + "."},
        )
        sum_direct_id = _add_op(
            b, f"op:sumdirect:{code}", "sum_cells", "Σ",
            "Summiert die €-Zellschäden der zehn direkten Sektorrisiken.",
            collapse_group="intermediates",
        )
        b.add_edge(b.ensure_source("computed"), sum_direct_id)
        b.add_edge(sum_direct_id, direct_id)
        if kind == "indirect":
            param = _global_param_node(b, "k_indirect")
            mul_id = _add_op(
                b, f"op:kfactor:{code}", "multiply", "×",
                "Indirekte Folgekosten = k_indirekt · Σ direkte Sektorschäden "
                "(konsolidiert Betriebsunterbrechung, Lieferketten, Standortnachteil, "
                "verzögerte Schäden; Prognos 2023).",
            )
            formula = "€ = k_indirekt · Σ direkte Sektorschäden"
            non_additive = False
        else:
            param = _global_param_node(b, "restoration_share")
            mul_id = _add_op(
                b, f"op:kfactor:{code}", "multiply", "×",
                "Restaurierungskosten = Restaurierungsquote · Σ direkte Sektorschäden. "
                "Teilkennzahl (Teilmenge der direkten Schäden) — nicht additiv zur "
                "Gesamtsumme.",
            )
            formula = "€ = Restaurierungsquote · Σ direkte Sektorschäden (nicht additiv)"
            non_additive = True
        b.add_edge(direct_id, mul_id)
        b.add_edge(param, mul_id)
        b.add_edge(mul_id, add_eur(formula, non_additive=non_additive))
        return

    if kind == "consolidated_zero":
        add_eur("0 € — in k_indirekt (Indirekte wirtschaftliche Verluste) konsolidiert, "
                "um Doppelzählung zu vermeiden (§3.7)")
        return

    # "flat": kommunenweiter Outcome aus dem P90-Index (estimate_outcome_and_cost).
    # Einziger Fall, in dem sich der €-Wert tatsächlich aus dem Index ableitet.
    p90_id = _add_op(
        b, f"op:p90:{code}", "p90", "P90",
        "90. Perzentil der Zell-Indizes → kommunenweiter Screening-Index (0–100).\n"
        r"$$P_{90}(\text{Zell-Indizes})$$",
    )
    b.add_edge(idx_id, p90_id)
    ref = float(risk.get("ref_value", 0.0))
    scale_id = _add_operator_scaling(b, code, ref, unit, "flat")
    b.add_edge(p90_id, scale_id)
    native_id = add_native("Outcome = Referenz · (P90-Index/100), kommunenweit")
    b.add_edge(scale_id, native_id)
    cost_id = _add_cost_op(
        b, risk,
        extra_tooltip="€-Bewertung skaliert mit Einwohner/100.000 (VoLL-Kalibrierung, §8/B6).",
    )
    b.add_edge(native_id, cost_id)
    b.add_edge(cost_id, add_eur("€ = Outcome × Kostensatz × Einwohner/100.000"))


def build_risk_lineage(code: str) -> dict:
    """Zwei-Schichten-Graph eines Risikos (Wirkungsdiagramm).

    Schicht A: Quellen → Zwischen → H/E/V → Wirkungsketten → Maximum → KWRA-Index.
    Schicht B: Quellen → Schadensfunktion → natives Ergebnis → Kostensatz → €
    (Struktur je Risikokategorie, siehe ``_risk_lineage_kind``).
    """
    risk = catalog.RISKS_BY_CODE[code]
    recipe = risk_recipe(risk)
    kind = _risk_lineage_kind(risk)
    b = LineageBuilder()

    # Schicht A: alle H/E/V der kuratierten Ketten (dedupliziert über ind:-IDs)
    hev_codes: set[tuple[str, str]] = set()
    for p in catalog.build_pathways(risk):
        hev_codes.add(("hazards", p["hazard"]))
        hev_codes.add(("exposures", p["exposure"]))
        hev_codes.add(("vulnerabilities", p["vulnerability"]))

    for cat, icode in hev_codes:
        sub = build_indicator_lineage(icode, cat, include_norm=False)
        _merge_builder(b, sub)

    pathways_meta = risk_pathway_meta(risk)
    idx_id = "out:index"
    b.add_node(
        idx_id, "outcome", "KWRA-Index",
        column=0, collapse_group="outcome",
        meta={
            "result_kind": "index",
            "unit": "0–100",
            "formula": recipe.get("formula_index", ""),
            "formula_header": recipe.get("formula_index_header", ""),
            "pathway_count": len(pathways_meta),
            "is_outcome": True,
        },
    )

    if pathways_meta:
        max_id = _add_operator_max(b)
        b.add_edge(max_id, idx_id)
        for i, p in enumerate(pathways_meta):
            h_id = f"ind:{p['hazard']}"
            e_id = f"ind:{p['exposure']}"
            v_id = f"ind:{p['vulnerability']}"
            mul_id = f"op:mul:path:{i}"
            path_id = f"pathway:{i}"
            title = get_pathway_description(
                code, p["hazard"], p["exposure"], p["vulnerability"],
                p["type"],
                p["hazard_name"], p["exposure_name"], p["vulnerability_name"],
            )
            _add_operator_multiply(b, mul_id)
            b.add_node(
                path_id, "pathway", title,
                column=3, collapse_group="pathways",
                meta={
                    "pathway_type": p["type"],
                    "type_label": p["type_label"],
                    "weight": p["weight"],
                    "chain_label": chain_label(p["hazard_name"], p["exposure_name"], p["vulnerability_name"]),
                    "hazard_name": p["hazard_name"],
                    "exposure_name": p["exposure_name"],
                    "vulnerability_name": p["vulnerability_name"],
                    "justification": p.get("justification"),
                    "justification_ref": p.get("justification_ref"),
                    "cluster": p.get("cluster"),
                },
            )
            b.add_edge(h_id, mul_id)
            b.add_edge(e_id, mul_id)
            b.add_edge(v_id, mul_id)
            b.add_edge(mul_id, path_id)
            b.add_edge(
                path_id, max_id,
                meta={
                    "op_kind": "weight",
                    "weight": p["weight"],
                    # bewusst KEINE parameter_id: Pfadgewichte sind beim Import fest
                    # eingelesene Modellkonstanten (risk_engine._PATHWAYS) — kein
                    # editierbarer Registry-Parameter (Override wäre wirkungslos).
                    "source": "Pfadgewicht (Modellkonstante, Risikokatalog)",
                },
            )

    # Schicht B: absoluter Outcome + € (bzw. nur Index bei Screening-Risiken)
    _build_impact_branch(b, risk, kind, idx_id)

    return _prune_lineage(b.build())


def build_measure_lineage(code: str) -> dict:
    m = catalog.MEASURES_BY_CODE.get(code)
    if not m:
        return {"nodes": [], "edges": [], "collapse_groups": COLLAPSE_GROUPS}
    b = LineageBuilder()
    mid = f"measure:{code}"
    b.add_node(mid, "pathway", m["name"], column=2, collapse_group="indicators",
               meta={"effect_target": m.get("effect_target", [])})
    for tgt in m.get("effect_target", []):
        b.add_node(f"src:effect:{tgt}", "source", f"Wirkung auf {tgt}",
                   column=0, collapse_group="sources")
        b.add_edge(f"src:effect:{tgt}", mid)
    for rcode in m.get("linked_risk_codes", [])[:3]:
        rname = catalog.RISKS_BY_CODE.get(rcode, {}).get("name", rcode)
        rid = f"risk:{rcode}"
        b.add_node(rid, "aggregation", rname, column=4, collapse_group="outcome")
        b.add_edge(mid, rid, label=f"−{m.get('default_reduction', 0)*100:.0f}%")
    return _finalize_graph(b.build())


def build_for_layer(code: str, category: str) -> dict:
    if category == "risks":
        return build_risk_lineage(code)
    if category == "measures":
        return build_measure_lineage(code)
    if category in ("hazards", "exposures", "vulnerabilities", "auxiliary"):
        return build_indicator_lineage(code, category)
    return {"nodes": [], "edges": [], "collapse_groups": COLLAPSE_GROUPS}
