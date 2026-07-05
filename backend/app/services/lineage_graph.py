"""Baut Herkunfts-Graphen (Quellen → Zwischen → H/E/V → Risiko) für Info-Fenster."""

from __future__ import annotations

from typing import Any

from app.data import catalog
from app.data.lineage_operators import CELL_DIRECT, CELL_OPERATORS, formula_operators_for
from app.data.pathway_descriptions import chain_label, get_pathway_description
from app.services.engine import formulas
from app.services.engine.formulas import risk_pathway_meta, risk_recipe

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
    "slope_factor": (["slope_deg", "vent_score"], ["dem", "osm"]),
    "slope_proxy": (["slope_deg", "vent_score"], ["dem", "osm"]),
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
                        input_ids.append(self.ensure_source("param"))
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
            if key.startswith("__") or not key:
                return self.ensure_source("param")
            if indicator_code and indicator_category:
                pid = f"{indicator_category}.{indicator_code}.param.{key}"
            else:
                pid = key
            return self.ensure_parameter(
                pid,
                inp.get("label", key),
                unit=inp.get("unit", ""),
                source=inp.get("source") or "Modellannahme (Formelrezept)",
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
            lines.append(_SCALE_FORMULAS.get(scale, _SCALE_FORMULAS["flat"]))
            return "\n".join(lines)
        if kind == "multiply":
            return tooltip or "Multiplikation: Gefahr × Betroffenheit × Empfindlichkeit"
        if kind in ("average", "max"):
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
        lines = [label]
        if ref is not None:
            lines.append(f"Referenzfall: {ref:g} {unit}".strip())
        if formula:
            lines.append(f"Berechnung: {formula}")
        elif incoming:
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
    "flat": "Index/100 · ×1",
}

_SCALE_SOURCES = {
    "pop": "Referenz-Outcome bei Index 100 / 100.000 Ew. (Risikokatalog)",
    "area": "Referenz-Outcome bei Index 100 / 50 km² (Risikokatalog)",
    "flat": "Referenz-Outcome bei Index 100 (Index-Outcome, Risikokatalog)",
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
            "tooltip": "Gefahr × Betroffenheit × Empfindlichkeit",
        },
    )
    return op_id


def _add_operator_average(b: "LineageBuilder") -> str:
    op_id = "op:max:index"
    b.add_node(
        op_id, "operator", "",
        column=0, collapse_group="outcome",
        meta={
            "op_kind": "max",
            "label": "Maximum",
            "tooltip": (
                "Stärkste Wirkungskette (0–100): Index = 100 · max(Gewicht · Ĥ · Ê · V̂). "
                "Die Kette mit dem höchsten gewichteten Produkt bestimmt den Index; die "
                "Kettenzahl beeinflusst ihn nicht."
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
    """Gewichte werden auf Kanten (Pfad → Mittelung) gelegt."""
    return f"op:weight:{pathway_idx}"


PIPELINE_OP_KINDS = frozenset({
    "count", "coverage", "neighbor", "divide", "add", "clamp",
    "scale_factor", "max", "min", "weighted_sum", "formula", "multiply",
})


def _is_pipeline_node(n: dict) -> bool:
    t = n.get("type")
    if t in ("source", "intermediate", "parameter"):
        return True
    if t == "operator":
        kind = (n.get("meta") or {}).get("op_kind")
        cg = n.get("collapse_group", "")
        if cg == "intermediates" and kind in PIPELINE_OP_KINDS:
            return True
    return False


def _assign_pipeline_columns(graph: dict) -> dict:
    """Links→rechts-Spalten für Quellen, Operatoren und Zwischenwerte."""
    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])
    nodes_by_id = {n["id"]: n for n in nodes}
    pipeline_ids = {n["id"] for n in nodes if _is_pipeline_node(n)}

    cols: dict[str, int] = {}
    for n in nodes:
        if n["id"] in pipeline_ids and n["type"] in ("source", "parameter"):
            cols[n["id"]] = 0

    for _ in range(len(pipeline_ids) + 8):
        changed = False
        for e in edges:
            tgt = e["target"]
            src = e["source"]
            if tgt not in pipeline_ids:
                continue
            src_node = nodes_by_id.get(src)
            if not src_node:
                continue
            if src not in pipeline_ids and src_node["type"] not in ("source", "parameter", "intermediate", "operator"):
                continue
            pred_col = cols.get(src)
            if pred_col is None:
                if src_node["type"] in ("source", "parameter"):
                    pred_col = 0
                else:
                    continue
            new_col = pred_col + 1
            if new_col > cols.get(tgt, -1):
                cols[tgt] = new_col
                changed = True
        if not changed:
            break

    for n in nodes:
        if n["id"] in cols:
            n["column"] = cols[n["id"]]

    max_pipe = max(cols.values()) if cols else 1
    max_int = max(
        (cols[n["id"]] for n in nodes if n["type"] == "intermediate" and n["id"] in cols),
        default=max_pipe,
    )
    has_pathways = any(n["type"] == "pathway" for n in nodes)

    for n in nodes:
        t = n["type"]
        if t in ("hazard", "exposure", "vulnerability"):
            n["column"] = max_int + 1
        elif t == "pathway":
            n["column"] = max_int + 3
        elif t == "operator":
            kind = (n.get("meta") or {}).get("op_kind")
            oid = n["id"]
            if n["id"] in cols:
                continue
            if kind == "multiply" and oid.startswith("op:mul:path:"):
                n["column"] = max_int + 2
            elif kind == "average":
                n["column"] = max_int + 4
            elif kind in ("scaling", "multiplier"):
                n["column"] = max_int + 6 if has_pathways else 4
            elif kind == "norm":
                n["column"] = max_int + 2
        elif t == "aggregation":
            n["column"] = max_int + 5 if has_pathways else 3
        elif t == "outcome":
            n["column"] = max_int + 7 if has_pathways else 4
        elif t == "norm":
            n["column"] = max_int + 2

    return graph


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


def _assign_formula_chain_columns(graph: dict) -> dict:
    """Spalten für Formelketten: Indikator → Operator → Indikator."""
    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])
    nodes_by_id = {n["id"]: n for n in nodes}

    for _ in range(len(nodes) + 4):
        changed = False
        for e in edges:
            src_n = nodes_by_id.get(e["source"])
            tgt_n = nodes_by_id.get(e["target"])
            if not src_n or not tgt_n:
                continue
            src_col = src_n.get("column")
            if src_col is None:
                continue
            if tgt_n["type"] == "operator" and src_n["type"] in (
                "hazard", "exposure", "vulnerability", "intermediate",
            ):
                new_col = src_col + 1
                if new_col > tgt_n.get("column", -1):
                    tgt_n["column"] = new_col
                    changed = True
            if src_n["type"] == "operator" and tgt_n["type"] in (
                "hazard", "exposure", "vulnerability",
            ):
                new_col = src_col + 1
                if new_col > tgt_n.get("column", -1):
                    tgt_n["column"] = new_col
                    changed = True
        if not changed:
            break
    return graph


def _assign_intermediate_columns(graph: dict) -> dict:
    """Staffelt Zwischenwerte und Pipeline-Knoten (delegiert an _assign_pipeline_columns)."""
    return _assign_pipeline_columns(graph)


def _finalize_graph(graph: dict) -> dict:
    graph = _assign_pipeline_columns(graph)
    graph = _assign_formula_chain_columns(graph)
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


def _find_terminal_id(nodes: list[dict]) -> str | None:
    for n in nodes:
        if n["type"] == "outcome":
            return n["id"]
    norm_ops = [
        n for n in nodes
        if n["type"] == "operator" and (n.get("meta") or {}).get("op_kind") == "norm"
    ]
    if norm_ops:
        return max(norm_ops, key=lambda n: n.get("column", 0))["id"]
    norms = [n for n in nodes if n["type"] == "norm"]
    if norms:
        return max(norms, key=lambda n: n.get("column", 0))["id"]
    return None


def _prune_lineage(graph: dict) -> dict:
    """Entfernt Knoten, die nicht auf dem Pfad zum Endknoten (Outcome/Norm) liegen."""
    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])
    terminal_id = _find_terminal_id(nodes)
    if not terminal_id:
        return _finalize_graph(graph)

    rev: dict[str, list[str]] = {}
    for e in edges:
        rev.setdefault(e["target"], []).append(e["source"])

    reachable: set[str] = set()
    stack = [terminal_id]
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
    input_ids: list[str] = []
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
        if inp.get("prov") == formulas.PARAM and inp.get("key", "").startswith("__"):
            continue
        if inp.get("prov") == formulas.PARAM:
            pid = f"{category}.{code}.param.{inp.get('key', 'value')}"
            b.ensure_parameter(
                pid,
                inp.get("label", inp.get("key", "")),
                unit=inp.get("unit", ""),
                source=inp.get("source") or "Modellannahme (Formelrezept)",
            )
            continue
        iid = b.expand_recipe_input_to_id(inp, indicator_code=code, indicator_category=category)
        key = inp.get("key", "")
        if key and not key.startswith("__"):
            cell_key_map[key] = iid
        input_ids.append(iid)

    steps = formula_operators_for(code, recipe.get("formula", ""))
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


def build_risk_lineage(code: str) -> dict:
    """Deduzierter Graph: Quellen → Zwischen → H/E/V → Pfade → Aggregation → Outcome."""
    risk = catalog.RISKS_BY_CODE[code]
    recipe = risk_recipe(risk)
    b = LineageBuilder()

    # Expand all H/E/V used in pathways (deduplicated via shared ind: IDs)
    hev_codes: set[tuple[str, str]] = set()
    for p in catalog.build_pathways(risk):
        hev_codes.add(("hazards", p["hazard"]))
        hev_codes.add(("exposures", p["exposure"]))
        hev_codes.add(("vulnerabilities", p["vulnerability"]))

    for cat, icode in hev_codes:
        sub = build_indicator_lineage(icode, cat, include_norm=False)
        _merge_builder(b, sub)

    pathways_meta = risk_pathway_meta(risk)
    avg_id = _add_operator_average(b)
    agg_id = "agg:index"
    b.add_node(
        agg_id, "aggregation",
        "Gesamt-Index",
        column=4, collapse_group="outcome",
        meta={
            "formula": recipe.get("formula_index", ""),
            "pathway_count": len(pathways_meta),
        },
    )
    b.add_edge(avg_id, agg_id)

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
            path_id, avg_id,
            meta={
                "op_kind": "weight",
                "weight": p["weight"],
                "parameter_id": f"pathway_weights.{p['type']}",
                "source": "pathway_weight_defaults (Risikokatalog)",
            },
        )

    out_id = "out:come"
    ref = float(risk.get("ref_value", 0.0))
    unit = risk.get("outcome_unit", "")
    risk_name = risk.get("name", code)
    scale_id = _add_operator_scaling(b, code, ref, unit, risk.get("scale", "pop"))
    b.add_node(
        out_id, "outcome",
        risk_name,
        column=5, collapse_group="outcome",
        meta={
            "formula": recipe.get("formula_outcome", ""),
            "unit": unit,
            "is_outcome": True,
        },
    )
    b.add_edge(agg_id, scale_id)
    b.add_edge(scale_id, out_id)

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
