"""Taxonomie und Klassifikation der KRITIS-Infrastruktur-Assets (OSM).

Zentrale Quelle für die vier gewichteten Infrastruktur-Layer
(ENERGY_INFRASTRUCTURE, WATER_WASTEWATER_INFRA, TRANSPORT_HUBS,
COMMUNICATION_INFRA):

- ``ASSET_CLASSES``: Anlagenklassen je Sektor mit Default-Gewicht
  (Kritikalitätspunkte je Zelle) und Default-Ersatzwert (EUR) inkl.
  Infokasten-Doku (``source_detail``/``source_refs``),
- reine Klassifikationsfunktionen von OSM-Tags auf Klassen-Keys
  (ohne Shapely-Abhängigkeit, unit-testbar),
- ``resolve_weights``: Auflösung override-fähiger Gewichte über
  ``exposures.<CODE>.param.w_<klasse>``.

formulas.py (Parameter-Registry) und engine/impact/params.py
(Ersatzwerte ``<sektor>_value_<klasse>_eur``) generieren ihre Specs aus
dieser Taxonomie, damit Registry, Resolver und Monetarisierung nie
divergieren.

Tragwerke (Masten, Portale, Schalter …) und Dach-PV werden bewusst gar
nicht klassifiziert (``None``): Masten sind Bestandteil der ohnehin je
Zellquerung gezählten Leitung — sie mitzuzählen war die Doppelzählung,
die einzelne Umspannwerk-/Trassenzellen künstlich aufgebläht hat.
"""
from __future__ import annotations

# Exposure-Code je Sektor (Katalog-Codes, siehe app/data/catalog.py).
SECTOR_EXPOSURE: dict[str, str] = {
    "energy": "ENERGY_INFRASTRUCTURE",
    "water": "WATER_WASTEWATER_INFRA",
    "transport": "TRANSPORT_HUBS",
    "comm": "COMMUNICATION_INFRA",
}

# Schlüssel für die je Zelle materialisierten Klassen-Zählungen.
SECTOR_CLASSES_KEY: dict[str, str] = {
    "energy": "energy_infra_classes",
    "water": "water_wastewater_classes",
    "transport": "transport_hub_classes",
    "comm": "communication_classes",
}

# Infokasten-Quellen (Keys aus app/data/sources.py) für die generierten
# Parameter: Klassengewichte (formulas.py) bzw. Ersatzwerte (impact/params.py).
WEIGHT_SOURCE_REFS = ["OSM_Data", "BBK_KRITIS"]
VALUE_SOURCE_REFS = ["Prognos_Klimaschaeden_2023", "BBK_KRITIS"]

# Anlagenklassen: weight = Kritikalitätspunkte je Vorkommen in einer Zelle
# (Linien: je Zellquerung), value_eur = Ersatz-/Wiederbeschaffungswert für den
# monetären Schadenspfad. Größenordnungen aus Netzbetreiber-/BBK-Praxiswerten,
# Details je Klasse in source_detail.
ASSET_CLASSES: dict[str, dict[str, dict]] = {
    "energy": {
        "substation_transmission": {
            "label": "Umspannwerk (Übertragungsnetz)",
            "weight": 8.0,
            "value_eur": 5_000_000.0,
            "source_detail": (
                "OSM power=substation mit substation=transmission oder Spannungsebene "
                "≥ 110 kV. Höchste Kritikalität: Ausfall trennt ganze Netzregionen; "
                "Ersatzwert ~5 Mio. € (110/380-kV-Umspannwerk, Netzbetreiber-Größenordnung)."
            ),
        },
        "substation_distribution": {
            "label": "Umspannwerk (Verteilnetz)",
            "weight": 4.0,
            "value_eur": 750_000.0,
            "source_detail": (
                "OSM power=substation ohne Übertragungsnetz-Merkmal (Mittelspannung "
                "oder Spannungsebene unbekannt). Versorgt Stadtteile/Ortslagen; "
                "Ersatzwert ~0,75 Mio. €."
            ),
        },
        "substation_minor": {
            "label": "Ortsnetzstation",
            "weight": 1.0,
            "value_eur": 50_000.0,
            "source_detail": (
                "OSM substation=minor_distribution oder Spannungsebene < 20 kV "
                "(Trafohäuschen). Lokal begrenzte Wirkung; Ersatzwert ~50 T€."
            ),
        },
        "plant": {
            "label": "Kraftwerk",
            "weight": 8.0,
            "value_eur": 20_000_000.0,
            "source_detail": (
                "OSM power=plant (Erzeugungsanlage als Gesamtobjekt, inkl. "
                "Freiflächen-PV/Windparks). Ersatzwert konservativ ~20 Mio. € "
                "(kleine bis mittlere Anlage)."
            ),
        },
        "generator_wind": {
            "label": "Windenergieanlage",
            "weight": 1.5,
            "value_eur": 1_500_000.0,
            "source_detail": (
                "OSM power=generator mit generator:source=wind (Einzelanlage). "
                "Ersatzwert ~1,5 Mio. €/MW-Klasse Onshore."
            ),
        },
        "generator_other": {
            "label": "Erzeuger (sonstige)",
            "weight": 0.5,
            "value_eur": 200_000.0,
            "source_detail": (
                "OSM power=generator sonstiger Quelle (Biogas, Wasser, BHKW …). "
                "Dach-PV (generator:source=solar) wird bewusst nicht gezählt "
                "(Massendaten ohne KRITIS-Relevanz). Ersatzwert ~200 T€."
            ),
        },
        "transformer": {
            "label": "Transformator (Einzelobjekt)",
            "weight": 0.5,
            "value_eur": 50_000.0,
            "source_detail": (
                "OSM power=transformer als Einzelpunkt (meist innerhalb von "
                "Stationen). Geringes Eigengewicht, da die umgebende Station "
                "bereits gezählt wird; Ersatzwert ~50 T€."
            ),
        },
        "line_ehv": {
            "label": "Höchstspannungsleitung (je Zellquerung)",
            "weight": 6.0,
            "value_eur": 150_000.0,
            "source_detail": (
                "OSM power=line/cable mit Spannungsebene ≥ 220 kV, je gequerte "
                "Rasterzelle. Übertragungsnetz-Trasse; Ersatzwert ~150 T€ je "
                "~100 m Trassenabschnitt (Mast + Beseilung anteilig)."
            ),
        },
        "line_hv": {
            "label": "Hochspannungsleitung (je Zellquerung)",
            "weight": 3.0,
            "value_eur": 60_000.0,
            "source_detail": (
                "OSM power=line mit 60–220 kV oder ohne voltage-Tag (power=line "
                "ist per OSM-Konvention Übertragungs-/Hochspannungsnetz), je "
                "gequerte Rasterzelle. Ersatzwert ~60 T€ je Zellabschnitt."
            ),
        },
        "line_mv": {
            "label": "Mittelspannungs-/Ortsnetzleitung (je Zellquerung)",
            "weight": 0.3,
            "value_eur": 20_000.0,
            "source_detail": (
                "OSM power=minor_line/cable bzw. Spannungsebene < 60 kV, je "
                "gequerte Rasterzelle. Verteilnetz, redundanzreich; Ersatzwert "
                "~20 T€ je Zellabschnitt."
            ),
        },
    },
    "water": {
        "wastewater_plant": {
            "label": "Kläranlage",
            "weight": 10.0,
            "value_eur": 5_000_000.0,
            "source_detail": (
                "OSM man_made=wastewater_plant. Zentrale Abwasserbehandlung, "
                "Ausfall mit unmittelbarer Umwelt-/Gesundheitswirkung; "
                "Ersatzwert ~5 Mio. € (kleine/mittlere Anlage)."
            ),
        },
        "water_works": {
            "label": "Wasserwerk",
            "weight": 10.0,
            "value_eur": 5_000_000.0,
            "source_detail": (
                "OSM man_made=water_works. Trinkwasseraufbereitung/-gewinnung; "
                "Ersatzwert ~5 Mio. €."
            ),
        },
        "pumping_station": {
            "label": "Pumpwerk",
            "weight": 4.0,
            "value_eur": 400_000.0,
            "source_detail": (
                "OSM man_made=pumping_station (Wasser/Abwasser). Kritisch für "
                "Druckzonen und Entwässerung, aber meist redundant ausgelegt; "
                "Ersatzwert ~400 T€."
            ),
        },
        "water_tower": {
            "label": "Wasserturm",
            "weight": 3.0,
            "value_eur": 1_000_000.0,
            "source_detail": (
                "OSM man_made=water_tower. Druckhaltung/Speicher; Ersatzwert "
                "~1 Mio. €."
            ),
        },
        "reservoir": {
            "label": "Trinkwasserspeicher",
            "weight": 2.0,
            "value_eur": 300_000.0,
            "source_detail": (
                "OSM man_made=reservoir_covered/storage_tank. Hochbehälter und "
                "gedeckte Speicher; Ersatzwert ~300 T€."
            ),
        },
    },
    "transport": {
        "railway_station": {
            "label": "Bahnhof",
            "weight": 8.0,
            "value_eur": 5_000_000.0,
            "source_detail": (
                "OSM railway=station. Regionaler Verkehrsknoten mit "
                "Bündelungsfunktion; Ersatzwert ~5 Mio. € (Empfangsgebäude + "
                "Verkehrsanlagen anteilig)."
            ),
        },
        "railway_halt": {
            "label": "Haltepunkt",
            "weight": 3.0,
            "value_eur": 500_000.0,
            "source_detail": (
                "OSM railway=halt. Halt ohne Knotenfunktion; Ersatzwert ~500 T€."
            ),
        },
        "public_transport_station": {
            "label": "ÖPNV-Station",
            "weight": 4.0,
            "value_eur": 1_000_000.0,
            "source_detail": (
                "OSM public_transport=station (sofern nicht bereits als Bahnhof "
                "erfasst). Ersatzwert ~1 Mio. €."
            ),
        },
        "bus_station": {
            "label": "Busbahnhof",
            "weight": 4.0,
            "value_eur": 1_000_000.0,
            "source_detail": (
                "OSM amenity=bus_station. Zentraler Umsteigeknoten des "
                "Busverkehrs; Ersatzwert ~1 Mio. €."
            ),
        },
    },
    "comm": {
        "data_center": {
            "label": "Rechenzentrum",
            "weight": 10.0,
            "value_eur": 10_000_000.0,
            "source_detail": (
                "OSM telecom=data_center oder building=data_center. Höchste "
                "IT-/TK-Kritikalität; Ersatzwert ~10 Mio. € (kleines RZ)."
            ),
        },
        "exchange": {
            "label": "Vermittlungsstelle",
            "weight": 6.0,
            "value_eur": 2_000_000.0,
            "source_detail": (
                "OSM telecom=exchange. Knotenpunkt des Festnetzes/FTTH; "
                "Ersatzwert ~2 Mio. €."
            ),
        },
        "comm_tower": {
            "label": "Fernmeldeturm",
            "weight": 6.0,
            "value_eur": 2_000_000.0,
            "source_detail": (
                "OSM man_made=communications_tower. Richtfunk-/Rundfunkknoten "
                "mit großem Versorgungsradius; Ersatzwert ~2 Mio. €."
            ),
        },
        "mast": {
            "label": "Mobilfunkmast",
            "weight": 2.0,
            "value_eur": 250_000.0,
            "source_detail": (
                "OSM man_made=mast bzw. tower/tower:type=communication. "
                "Einzelner Funkstandort, Zellen überlappen; Ersatzwert ~250 T€."
            ),
        },
        "antenna": {
            "label": "Antennenstandort",
            "weight": 1.0,
            "value_eur": 50_000.0,
            "source_detail": (
                "OSM man_made=antenna bzw. communication:*-Nodes ohne "
                "Mast-/Turmobjekt. Kleinststandort; Ersatzwert ~50 T€."
            ),
        },
    },
}

# power=*-Werte ohne Eigengewicht: Tragwerke/Schaltelemente sind Bestandteil
# der je Zellquerung gezählten Leitung bzw. der gezählten Station.
_POWER_SUPPORT_VALUES = frozenset({
    "tower", "pole", "portal", "catenary_mast", "insulator", "terminal",
    "connection", "switch", "busbar", "bay", "cable_distribution_cabinet",
    "street_cabinet",
})

# Spannungsgrenzen (kV) für die Leitungs-/Umspannwerk-Klassifikation.
_KV_EHV = 220.0   # Höchstspannung (Übertragungsnetz 220/380 kV)
_KV_HV = 60.0     # Hochspannung (typ. 110 kV)
_KV_SUBSTATION_TRANSMISSION = 110.0
_KV_SUBSTATION_MINOR = 20.0


def parse_voltage_kv(tags: dict) -> float | None:
    """Maximale Spannungsebene aus OSM-Tags in kV (None wenn nicht auswertbar).

    OSM tagt in Volt; Mehrfachwerte sind ``;``-separiert ("220000;110000").
    Nicht-numerische Angaben ("medium") werden ignoriert.
    """
    for key in ("voltage", "voltage:primary"):
        raw = tags.get(key)
        if raw is None or str(raw).strip() == "":
            continue
        best: float | None = None
        for part in str(raw).split(";"):
            try:
                v = float(part.strip())
            except ValueError:
                continue
            if best is None or v > best:
                best = v
        if best is not None and best > 0:
            return best / 1000.0
    return None


def _classify_substation(tags: dict) -> str:
    kind = tags.get("substation", "")
    kv = parse_voltage_kv(tags)
    if kind == "transmission" or (kv is not None and kv >= _KV_SUBSTATION_TRANSMISSION):
        return "substation_transmission"
    if kind == "minor_distribution" or (kv is not None and kv < _KV_SUBSTATION_MINOR):
        return "substation_minor"
    return "substation_distribution"


def _classify_generator(tags: dict) -> str | None:
    src = tags.get("generator:source", "")
    if src == "solar":
        return None  # Dach-PV-Filter; Freiflächen-PV ist als power=plant erfasst
    if src == "wind":
        return "generator_wind"
    return "generator_other"


def classify_power_node(tags: dict) -> str | None:
    """Klasse eines power=*-Punktobjekts (None = zählt nicht)."""
    val = tags.get("power", "")
    if not val or val in _POWER_SUPPORT_VALUES:
        return None
    if val == "substation":
        return _classify_substation(tags)
    if val == "plant":
        return "plant"
    if val == "generator":
        return _classify_generator(tags)
    if val == "transformer":
        return "transformer"
    if val == "converter":
        # HVDC-Konverterstation: funktional ein Übertragungsnetz-Knoten.
        return "substation_transmission"
    return None


def classify_power_line(tags: dict) -> str | None:
    """Klasse eines linienförmigen power=*-Ways (je Zellquerung gezählt)."""
    val = tags.get("power", "")
    if val in _POWER_SUPPORT_VALUES:
        return None  # busbar & Co: Bestandteil der Station
    kv = parse_voltage_kv(tags)
    if kv is not None:
        if kv >= _KV_EHV:
            return "line_ehv"
        if kv >= _KV_HV:
            return "line_hv"
        return "line_mv"
    if val == "line":
        # Ohne voltage-Tag: power=line ist per OSM-Konvention Hoch-/Höchstspannung.
        return "line_hv"
    return "line_mv"  # minor_line/cable ohne Spannungsangabe


def classify_power_area(tags: dict) -> str | None:
    """Klasse eines flächigen power=*-Ways (Station/Kraftwerk als Polygon)."""
    return classify_power_node(tags)


def classify_water(tags: dict) -> str | None:
    mm = tags.get("man_made", "")
    if mm == "wastewater_plant":
        return "wastewater_plant"
    if mm == "water_works":
        return "water_works"
    if mm == "pumping_station":
        return "pumping_station"
    if mm == "water_tower":
        return "water_tower"
    if mm in ("reservoir_covered", "storage_tank"):
        return "reservoir"
    return None


def classify_transport(tags: dict) -> str | None:
    """Prioritätsreihenfolge dedupliziert Mehrfach-Tagging (station+public_transport)."""
    if tags.get("railway") == "station":
        return "railway_station"
    if tags.get("railway") == "halt":
        return "railway_halt"
    if tags.get("public_transport") == "station":
        return "public_transport_station"
    if tags.get("amenity") == "bus_station":
        return "bus_station"
    return None


def classify_comm(tags: dict) -> str | None:
    telecom = tags.get("telecom", "")
    if telecom == "data_centre" or telecom == "data_center" or tags.get("building") == "data_center":
        return "data_center"
    if telecom == "exchange":
        return "exchange"
    mm = tags.get("man_made", "")
    if mm == "communications_tower":
        return "comm_tower"
    is_comm_tower_tagged = (
        tags.get("tower") == "communication"
        or tags.get("tower:type") == "communication"
    )
    if mm == "mast" or is_comm_tower_tagged:
        return "mast"
    if mm == "antenna" or any(
        k == "communication" or k.startswith("communication:") for k in tags
    ):
        return "antenna"
    return None


def resolve_weights(sector: str) -> dict[str, float]:
    """Effektive Klassengewichte (Kommune-Overrides > Taxonomie-Default)."""
    from ..services.engine import override_context  # lazy: app/data bleibt schlank

    code = SECTOR_EXPOSURE[sector]
    return {
        cls: float(override_context.get_override(
            f"exposures.{code}.param.w_{cls}", spec["weight"],
        ))
        for cls, spec in ASSET_CLASSES[sector].items()
    }


# Sättigungsfaktor der Zell-Aggregation: das stärkste Einzelasset zählt voll,
# jede weitere Punktesumme nur anteilig. Begründung: eine Zelle, in der bereits
# ein Umspannwerk liegt, wird durch die dort zusammenlaufenden Stromkreise nur
# noch begrenzt "kritischer" — ohne Sättigung sammelt die Knotenzelle linear
# alles ein (Oschatz: UW + 8 Stromkreise + 3 Trafos) und drückt alle
# Trassenzellen an den unteren Skalenrand.
SATURATION_ALPHA = 0.5


def weighted_score(class_counts: dict[str, float], weights: dict[str, float]) -> float:
    """Kritikalitätspunkte einer Zelle: stärkstes Asset voll + gesättigter Rest.

    ``score = w_max + SATURATION_ALPHA · (Σ w·n − w_max)`` mit ``w_max`` =
    höchstes Klassengewicht eines in der Zelle vorhandenen Assets.
    """
    total = 0.0
    strongest = 0.0
    for cls, count in class_counts.items():
        if not count:
            continue
        w = weights.get(cls, 0.0)
        total += float(count) * w
        if w > strongest:
            strongest = w
    if total <= strongest:
        return total
    return strongest + SATURATION_ALPHA * (total - strongest)


def value_param_key(sector: str, cls: str) -> str:
    """Impact-Parameter-Key des Ersatzwerts einer Anlagenklasse."""
    return f"{sector}_value_{cls}_eur"
