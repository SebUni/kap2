"""Kuratierte Wirkungsketten je Risiko — mit Begründung und Quelle.

Hintergrund (MODELL_KRITIK §3.1/3.5): Die frühere ``build_pathways``-Logik erzeugte
Wirkungsketten **kartesisch** aus den H/E/V-Listen. Das hatte zwei Probleme:
1. Es entstanden fachlich sinnlose Ketten (z. B. Kälte-Hazard × Hitze-Sensitivität).
2. Die Index-Höhe hing von der ANZAHL erzeugter Pfade ab (Verdünnungs-Artefakt).

Beides wird hier behoben: Jedes Risiko trägt eine **kuratierte** Liste von Ketten, die
sich am Wirkungsketten-Ansatz (Klimasignal → Klimawirkung → Exposition × Sensitivität)
der KWRA 2021 und des GIZ Vulnerability Sourcebook orientiert. Jede Kette hat eine
nachlesbare Begründung (``note``) und eine Quelle (``ref`` → ``sources.py``). Wo die
KWRA die konkrete Indikator-Kombination nicht wörtlich ausweist, ist die Kette nach dem
methodischen H×E×V-Schema hergeleitet (``ref="GIZ_Vulnerability_Sourcebook"``) und im
``note`` als Herleitung gekennzeichnet.

Die Aggregation nutzt das **Maximum** der gewichteten Ketten (``risk_engine``), nicht
mehr den gewichteten Mittelwert — die Kettenzahl beeinflusst den Index daher nicht mehr.

Datenstruktur je Risiko:
    "cluster": KWRA-Handlungsfeld/Cluster (Anzeige-/Kontexttext)
    "ref":     Default-Quellen-Key (sources.py) für die Ketten dieses Risikos
    "chains":  Liste von (hazard, exposure, vulnerability, pathway_type, note[, ref])

``pathway_type`` bestimmt das Gewicht (catalog.PATHWAY_WEIGHTS) und das Anzeige-Label.
Genau EIN Pfad je Risiko ist ``primary`` (Gewicht 1,0, die dominante Kette).
"""

from __future__ import annotations

# Kürzel für wiederkehrende Herleitungs-Quellen
_KWRA = "UBA_KWRA_2021"
_GIZ = "GIZ_Vulnerability_Sourcebook"

CURATED_PATHWAYS: dict[str, dict] = {
    # ══ Cluster Wirtschaft & Gesundheit — Handlungsfeld Menschliche Gesundheit (KWRA TB 5) ══
    "EXPECTED_ANNUAL_MORTALITY": {
        "cluster": "Menschliche Gesundheit (KWRA 2021, Teilbericht 5)",
        "ref": _KWRA,
        "chains": [
            ("HEAT_WAVE", "AGE_STRUCTURE", "HEALTHCARE_ACCESS", "primary",
             "Hitzewellen sind laut KWRA die Klimawirkung mit dem höchsten und am besten "
             "belegten Mortalitätsrisiko in Deutschland. Die Altersstruktur ist die "
             "Leitgröße: Laut RKI entfallen rund 55 % der hitzebedingten Sterbefälle auf "
             "die Gruppe ab 85 Jahren, die nur rund 3 % der Bevölkerung stellt."),
            ("HEAT_WAVE", "VULNERABLE_GROUPS_POPULATION", "HEALTHCARE_ACCESS", "alternate_exposure",
             "Die Exzessmortalität konzentriert sich auf vulnerable Gruppen (Hochbetagte, "
             "Vorerkrankte); die Versorgungslage entscheidet über den Verlauf."),
            ("HEAT_WAVE", "POPULATION_DENSITY", "HEALTHCARE_ACCESS", "alternate_exposure",
             "Dicht besiedelte, wärmebelastete Räume tragen die höchste absolute Last — "
             "dort verstärkt die städtische Wärmeinsel die Exposition."),
        ],
    },
    "EXPECTED_ANNUAL_MORBIDITY": {
        "cluster": "Menschliche Gesundheit (KWRA 2021, Teilbericht 5)",
        "ref": _KWRA,
        "chains": [
            ("HEAT_WAVE", "POPULATION_DENSITY", "HEAT_SENSITIVITY", "primary",
             "Hitzebedingte Erkrankungen (Herz-Kreislauf, Niere) sind die dominante "
             "hitzeassoziierte Morbidität; Ballungsräume mit sensiblen Personen führen."),
            # Die frühere Vektoren-Kette (DISEASE_VECTOR_SUSCEPTIBILITY) ist
            # entfallen: kein Beleg in der Schadensbaum-Sensitivitätsliste von
            # #95 (W182: S152–S158); Vektoren gehören zur Klimawirkung #97.
            ("HEAT_WAVE", "VULNERABLE_GROUPS_POPULATION", "HEALTHCARE_ACCESS", "alternate_exposure",
             "Vorerkrankte und hochaltrige Menschen tragen die höchste Erkrankungslast "
             "(S153/S152); Versorgungszugang und gekühlte Aufenthaltsräume (S157/R36) "
             "entscheiden über den Verlauf."),
            # Die frühere DROUGHT-Kette ist entfallen: Die Schadensfunktion rechnet
            # ausschließlich mit HEAT_WAVE, und der Risikoname sagt das jetzt auch.
            # Eine Kette, die im absoluten Outcome nicht vorkommt, gehört nicht in
            # die Kuratierung.
        ],
    },
    # Die drei Verletzten-Kanäle waren bis Modellversion 6 EIN Risiko mit einem
    # max() über drei Gefahren. Verletzte aus Flut und Sturm sind aber additive
    # Ereignisse — die Ketten sind daher auf je ein eigenes Risiko aufgeteilt,
    # jede mit eigener primary-Kette.

    # ══ Cluster Infrastrukturen (KWRA TB 4) ══

    # ── Infrastruktur-Ausfälle (Betriebsstunden) — KWRA TB 4, Kaskaden TB 6 ──

    # ══ Cluster Land — Landwirtschaft, Boden, Wald, Biologische Vielfalt (KWRA TB 2) ══

    # ══ Cluster Wasser — Wasserhaushalt, Fischerei (KWRA TB 3) ══

    # ══ Cluster Wirtschaft — Folge-/Sekundärkosten (KWRA TB 5/6) ══
}


# ── Geparkt (M0-Verschlankung): Kuratierungen der stillgelegten Risiken ──
# Kehren mit den Roadmap-Stufen zurück; bewusst außerhalb von CURATED_PATHWAYS,
# damit Ratchets und build_pathways nur den aktiven Katalog sehen.
_PARKED_CURATED_PATHWAYS: dict = {
    "EXPECTED_ANNUAL_MORTALITY_FLOOD": {
        "cluster": "Menschliche Gesundheit / Bevölkerungsschutz (KWRA 2021, Teilbericht 5)",
        "ref": _KWRA,
        "chains": [
            ("HEAVY_RAIN_FLOOD", "POPULATION_DENSITY", "EARLY_WARNING_SYSTEMS", "primary",
             "Sturzfluten in engen Steiltälern sind die tödlichste Ausprägung des "
             "Hochwasserrisikos; die Ahr-Flut 2021 forderte über 180 Todesopfer, während "
             "die flächenmäßig weit größere Elbeflut 2002 rund 21 forderte. Entscheidend "
             "sind Vorwarnzeit und Fluchtmöglichkeit."),
            ("HEAVY_RAIN_FLOOD", "LOCATION_HAZARD_ZONES", "EMERGENCY_MANAGEMENT", "alternate_exposure",
             "Bebauung in Gefahrenzonen erhöht die Zahl der Eingeschlossenen; das "
             "Notfallmanagement bestimmt, wie viele rechtzeitig erreicht werden."),
        ],
    },
    "EXPECTED_ANNUAL_MORTALITY_STORM": {
        "cluster": "Menschliche Gesundheit / Bevölkerungsschutz (KWRA 2021, Teilbericht 5)",
        "ref": _KWRA,
        "chains": [
            ("EXTRATROPICAL_STORM", "POPULATION_DENSITY", "BUILDING_STABILITY", "primary",
             "Sturmtote entstehen überwiegend im Freien und unterwegs — durch umstürzende "
             "Bäume, fliegende Trümmer und Bauteilversagen. Kyrill 2007 forderte in "
             "Deutschland 13 Todesopfer, Friederike 2018 acht bis zehn."),
            ("EXTRATROPICAL_STORM", "LOCATION_HAZARD_ZONES", "EARLY_WARNING_SYSTEMS", "alternate_exposure",
             "Exponierte Lagen und kurze Vorwarnzeiten erhöhen die Zahl der im Freien "
             "Überraschten."),
        ],
    },
    "EXPECTED_ANNUAL_INJURIES": {
        "cluster": "Menschliche Gesundheit / Bevölkerungsschutz (KWRA 2021, Teilbericht 5)",
        "ref": _KWRA,
        "chains": [
            ("HEAVY_RAIN_FLOOD", "POPULATION_DENSITY", "EMERGENCY_MANAGEMENT", "primary",
             "Starkregen und Sturzfluten sind laut KWRA die Hauptursache klimabedingter "
             "Verletzungen; Schadensausmaß hängt von Betroffenheit und Notfallmanagement ab. "
             "Ein erheblicher Teil entsteht erst bei den Aufräumarbeiten."),
            ("HEAVY_RAIN_FLOOD", "LOCATION_HAZARD_ZONES", "EARLY_WARNING_SYSTEMS", "alternate_exposure",
             "Bebauung in Gefahrenzonen erhöht die Zahl der Betroffenen; Frühwarnung "
             "reduziert sie."),
        ],
    },
    "EXPECTED_ANNUAL_INJURIES_STORM": {
        "cluster": "Menschliche Gesundheit / Bevölkerungsschutz (KWRA 2021, Teilbericht 5)",
        "ref": _KWRA,
        "chains": [
            ("EXTRATROPICAL_STORM", "LOCATION_HAZARD_ZONES", "EARLY_WARNING_SYSTEMS", "primary",
             "Stürme verursachen Verletzungen v. a. in exponierten Lagen; wirksame "
             "Frühwarnung reduziert die Betroffenheit."),
            ("EXTRATROPICAL_STORM", "POPULATION_DENSITY", "BUILDING_STABILITY", "alternate_exposure",
             "Dichte Bebauung mit älterer Bausubstanz erhöht das Risiko durch gelöste "
             "Bauteile und Dachschäden."),
        ],
    },
    "EXPECTED_ANNUAL_INJURIES_LANDSLIDE": {
        "cluster": "Menschliche Gesundheit / Bevölkerungsschutz (KWRA 2021, Teilbericht 5)",
        "ref": _KWRA,
        "chains": [
            ("LANDSLIDE", "POPULATION_DENSITY", "EMERGENCY_MANAGEMENT", "primary",
             "Hangrutschungen nach Starkregen gefährden bebaute Hanglagen — außerhalb "
             "steilen Geländes nahe null."),
        ],
    },
    "EXPECTED_ANNUAL_MENTAL_HEALTH": {
        "cluster": "Menschliche Gesundheit (KWRA 2021, Teilbericht 5)",
        "ref": _KWRA,
        "chains": [
            ("HEAT_WAVE", "POPULATION_DENSITY", "INCOME_SOCIAL_RESILIENCE", "primary",
             "Anhaltende Hitze erhöht psychische Belastung und Klinikeinweisungen; soziale "
             "Resilienz puffert die Wirkung ab — KWRA-Handlungsfeld Gesundheit."),
            ("DROUGHT", "VULNERABLE_GROUPS_POPULATION", "HEALTHCARE_ACCESS", "alternate_hazard",
             "Länger andauernde Dürre-/Krisenlagen wirken auf die psychische Gesundheit "
             "vulnerabler Gruppen; Versorgungszugang moderiert. Hergeleitet.", _GIZ),
            ("CASCADE_EVENT", "POPULATION_DENSITY", "INCOME_SOCIAL_RESILIENCE", "alternate_hazard",
             "Kaskadierende Extremereignisse (Evakuierung, Ausfall) sind eine belegte "
             "Ursache posttraumatischer Belastung. Hergeleitet nach H×E×V-Schema.", _GIZ),
        ],
    },
    "EXPECTED_ANNUAL_AFFECTED_EVACUATED": {
        "cluster": "Bevölkerungsschutz / Wasser (KWRA 2021, Teilbericht 3/5)",
        "ref": _KWRA,
        "chains": [
            ("HEAVY_RAIN_FLOOD", "LOCATION_HAZARD_ZONES", "EMERGENCY_MANAGEMENT", "primary",
             "Fluss- und Sturzfluten in Gefahrenzonen sind der Hauptauslöser für "
             "Evakuierungen; Notfallmanagement bestimmt Umfang und Dauer."),
            ("STORM_SURGE", "COASTAL_STORM_SURGE_EXPOSURE", "EARLY_WARNING_SYSTEMS", "alternate_hazard",
             "Sturmfluten an der Küste erzwingen großräumige Evakuierungen; Frühwarnung "
             "und Deichschutz begrenzen die Betroffenheit — KWRA-Cluster Wasser/Küste."),
            ("WILDFIRE", "POPULATION_DENSITY", "EMERGENCY_MANAGEMENT", "alternate_hazard",
             "Vegetationsbrände an der Siedlungsgrenze führen zu Räumungen; regional "
             "zunehmend relevante Nebenkette."),
        ],
    },
    "EXPECTED_THERMAL_STRESS_HOURS": {
        "cluster": "Menschliche Gesundheit / Bauwesen (KWRA 2021, Teilbericht 5)",
        "ref": _KWRA,
        "chains": [
            ("HEAT_WAVE", "OUTDOOR_THERMAL_EXPOSURE", "HEAT_SENSITIVITY", "primary",
             "Wärmebelastungsstunden entstehen dort, wo Hitze auf Aufenthalt im Freien "
             "und hitzeempfindliche Personen trifft — die direkte Dosis-Kette."),
            ("MEAN_TEMPERATURE_RISE", "POPULATION_DENSITY", "UHI_INTENSITY", "alternate_hazard",
             "Der langfristige Temperaturanstieg verstärkt über die städtische Wärmeinsel "
             "die Dauerbelastung in dichten Quartieren."),
            ("HEAT_WAVE", "OUTDOOR_THERMAL_EXPOSURE", "GREEN_SPACE_SHARE", "alternate_vulnerability",
             "Fehlende Grün-/Schattenflächen erhöhen die Belastungsdauer bei gleicher "
             "Hitze — steuerbare Sensitivität."),
        ],
    },
    "EXPECTED_POLLUTANT_EXPOSURE_HOURS": {
        "cluster": "Menschliche Gesundheit / Luft (KWRA 2021, Teilbericht 5)",
        "ref": _KWRA,
        "chains": [
            ("HEAT_WAVE", "POPULATION_DENSITY", "AIR_QUALITY_RISK", "primary",
             "Hitzeperioden treiben die bodennahe Ozon- und Feinstaubbildung; die "
             "Belastungsstunden konzentrieren sich in dicht besiedelten Belastungsräumen."),
            ("MEAN_TEMPERATURE_RISE", "OUTDOOR_THERMAL_EXPOSURE", "HEAT_SENSITIVITY", "alternate_hazard",
             "Steigende Mitteltemperaturen verlängern die Ozonsaison; im Freien Tätige und "
             "Sensible tragen die höchste Dosis."),
        ],
    },
    "MEDICAL_UNDERSUPPLY_RISK_INDEX": {
        "cluster": "Menschliche Gesundheit / Gesundheitsversorgung (KWRA 2021, Teilbericht 5)",
        "ref": _KWRA,
        "chains": [
            ("HEAT_WAVE", "VULNERABLE_GROUPS_POPULATION", "HEALTHCARE_ACCESS", "primary",
             "Hitzespitzen erhöhen die Nachfrage nach Notfall-/Pflegeleistungen; bei "
             "schlechtem Versorgungszugang entsteht eine Versorgungslücke (Screening-Index)."),
            ("CASCADE_EVENT", "POPULATION_DENSITY", "INFRA_DEPENDENCY_CHAIN", "alternate_hazard",
             "Kaskadierende Ausfälle (Strom, Verkehr) unterbrechen die medizinische "
             "Versorgungskette. Hergeleitet nach H×E×V-Schema.", _GIZ),
        ],
    },
    "SOCIAL_INEQUALITY_AMPLIFICATION_RISK_INDEX": {
        "cluster": "Integrierte Auswertung / Soziales (KWRA 2021, Teilbericht 6)",
        "ref": _KWRA,
        "chains": [
            ("HEAT_WAVE", "VULNERABLE_GROUPS_POPULATION", "VULNERABLE_GROUPS_SHARE", "primary",
             "Klimarisiken treffen einkommensschwache und vulnerable Gruppen überproportional "
             "(KWRA: soziale Ungleichheit als Querschnittsverstärker) — reiner Screening-Index."),
            ("DROUGHT", "POPULATION_DENSITY", "INCOME_SOCIAL_RESILIENCE", "alternate_hazard",
             "Preis-/Versorgungsfolgen von Dürre belasten geringe Einkommen stärker; "
             "soziale Resilienz moderiert. Hergeleitet.", _GIZ),
        ],
    },
    "EXPECTED_BUILDING_DAMAGE_EUR": {
        "cluster": "Bauwesen / Gebäude (KWRA 2021, Teilbericht 4)",
        "ref": _KWRA,
        "chains": [
            ("HEAVY_RAIN_FLOOD", "LOCATION_HAZARD_ZONES", "BUILDING_STABILITY", "primary",
             "Überflutung durch Starkregen/Hochwasser ist laut KWRA und GDV-Statistik der "
             "größte Treiber von Gebäudeschäden; entscheidend sind Lage und Bausubstanz."),
            ("EXTRATROPICAL_STORM", "BUILDING_STOCK", "BUILDING_STABILITY", "alternate_hazard",
             "Sturm/Starkwind schädigt Dächer und Fassaden über den gesamten Gebäudebestand — "
             "zweiter großer Schadentreiber der Wohngebäudeversicherung."),
            ("HEAT_WAVE", "BUILDING_STOCK", "FINANCIAL_ADAPTATION_CAPACITY", "alternate_hazard",
             "Hitze/Trockenheit verursacht Setzungs- und Materialschäden; die "
             "Anpassungsfähigkeit der Eigentümer moderiert die Schadenshöhe."),
        ],
    },
    "EXPECTED_TRANSPORT_DAMAGE_EUR": {
        "cluster": "Verkehr (KWRA 2021, Teilbericht 4)",
        "ref": _KWRA,
        "chains": [
            ("HEAVY_RAIN_FLOOD", "LOCATION_HAZARD_ZONES", "CRITICAL_INFRA_CONDITION", "primary",
             "Überflutung und Unterspülung sind laut KWRA der Hauptschadentreiber für "
             "Verkehrsinfrastruktur; der Erhaltungszustand bestimmt die Schadensanfälligkeit."),
            ("HEAT_WAVE", "TRANSPORT_HUBS", "MATERIAL_HEAT_SENSITIVITY", "alternate_hazard",
             "Hitze verformt Gleise und Asphalt (Blow-ups, Spurrinnen); Materialanfälligkeit "
             "der Knoten treibt die Reparaturkosten."),
            ("DROUGHT", "TRANSPORT_HUBS", "MATERIAL_HEAT_SENSITIVITY", "alternate_hazard",
             "Niedrigwasser schränkt die Binnenschifffahrt ein und schädigt Uferbauwerke — "
             "KWRA-Wirkung im Verkehrscluster."),
        ],
    },
    "EXPECTED_ENERGY_INFRA_DAMAGE_EUR": {
        "cluster": "Energiewirtschaft (KWRA 2021, Teilbericht 4)",
        "ref": _KWRA,
        "chains": [
            ("EXTRATROPICAL_STORM", "ENERGY_INFRASTRUCTURE", "CRITICAL_INFRA_CONDITION", "primary",
             "Stürme sind der Hauptschadentreiber für Freileitungen und Umspannanlagen; "
             "der Anlagenzustand bestimmt die Ausfall-/Schadenshöhe (KWRA Energiecluster)."),
            ("HEAVY_RAIN_FLOOD", "ENERGY_INFRASTRUCTURE", "CRITICAL_INFRA_CONDITION", "alternate_hazard",
             "Überflutung von Umspannwerken und Kraftwerksstandorten verursacht hohe "
             "Sachschäden — zweiter belegter Wirkpfad."),
            ("HEAT_WAVE", "ENERGY_INFRASTRUCTURE", "REDUNDANCY_BACKUP", "alternate_hazard",
             "Hitze mindert Kühl-/Übertragungskapazität und Transformatorlebensdauer; "
             "Redundanz begrenzt die Schadenswirkung."),
        ],
    },
    "EXPECTED_TELECOM_DAMAGE_EUR": {
        "cluster": "Telekommunikation (KWRA 2021, Teilbericht 4)",
        "ref": _KWRA,
        "chains": [
            ("EXTRATROPICAL_STORM", "COMMUNICATION_INFRA", "CRITICAL_INFRA_CONDITION", "primary",
             "Stürme beschädigen Masten, Antennen und Freileitungen der TK-Netze; der "
             "Anlagenzustand bestimmt die Schadensanfälligkeit."),
            ("HEAVY_RAIN_FLOOD", "COMMUNICATION_INFRA", "REDUNDANCY_BACKUP", "alternate_hazard",
             "Überflutung von Vermittlungsstellen/Kabelkanälen; Netzredundanz begrenzt "
             "Ausfall und Schaden."),
        ],
    },
    "EXPECTED_WATER_WASTEWATER_DAMAGE_EUR": {
        "cluster": "Wasserwirtschaft (KWRA 2021, Teilbericht 3/4)",
        "ref": _KWRA,
        "chains": [
            ("HEAVY_RAIN_FLOOD", "WATER_WASTEWATER_INFRA", "CRITICAL_INFRA_CONDITION", "primary",
             "Starkregen überlastet und beschädigt Kanäle, Pump- und Klärwerke; der "
             "Erhaltungszustand steuert die Schadenshöhe (KWRA Wasserwirtschaft)."),
            ("DROUGHT", "WATER_WASTEWATER_INFRA", "GROUNDWATER_DEPENDENCY", "alternate_hazard",
             "Anhaltende Trockenheit senkt Grundwasserstände und schädigt Brunnen/Leitungen "
             "grundwasserabhängiger Versorger."),
        ],
    },
    "EXPECTED_RESTORATION_COSTS_EUR": {
        "cluster": "Infrastrukturen / Wiederherstellung (KWRA 2021, Teilbericht 4)",
        "ref": _KWRA,
        "chains": [
            ("HEAVY_RAIN_FLOOD", "BUILDING_STOCK", "FINANCIAL_ADAPTATION_CAPACITY", "primary",
             "Wiederherstellungskosten folgen den direkten Flutschäden an Gebäuden und "
             "Infrastruktur; die Finanzkraft bestimmt Tempo und Umfang des Wiederaufbaus. "
             "Teilmenge der direkten Sektorschäden — im Modell nicht additiv gezählt."),
            ("EXTRATROPICAL_STORM", "FOREST_AREA", "PLANNING_IMPLEMENTATION_CAPACITY", "alternate_hazard",
             "Sturmwurf erfordert Aufräum-/Wiederbewaldungskosten; die Umsetzungskapazität "
             "der Verwaltung steuert die Wiederherstellung."),
            ("WILDFIRE", "BUILDING_STOCK", "FINANCIAL_ADAPTATION_CAPACITY", "alternate_hazard",
             "Brandschäden an der Siedlungsgrenze erzeugen Wiederaufbaukosten — regional "
             "relevante Nebenkette."),
        ],
    },
    "EXPECTED_CI_OUTAGE_HOURS": {
        "cluster": "Kritische Infrastrukturen (KWRA 2021, Teilbericht 4/6)",
        "ref": _KWRA,
        "chains": [
            ("HEAVY_RAIN_FLOOD", "ENERGY_INFRASTRUCTURE", "INFRA_CRITICALITY", "primary",
             "Überflutung kritischer Anlagen ist der häufigste Auslöser längerer "
             "KRITIS-Ausfälle; die Kritikalität bestimmt die Systemwirkung."),
            ("EXTRATROPICAL_STORM", "COMMUNICATION_INFRA", "REDUNDANCY_BACKUP", "alternate_hazard",
             "Sturm unterbricht Kommunikations-/Energieversorgung; Redundanz verkürzt die "
             "Ausfalldauer."),
            ("CASCADE_EVENT", "ENERGY_INFRASTRUCTURE", "INFRA_DEPENDENCY_CHAIN", "compound_hv",
             "Kaskadierende Ereignisse pflanzen Ausfälle entlang der Abhängigkeitsketten "
             "fort — Kernbefund der KWRA-Kaskadenanalyse (Teilbericht 6)."),
        ],
    },
    "EXPECTED_ENERGY_OUTAGE_HOURS": {
        "cluster": "Energiewirtschaft (KWRA 2021, Teilbericht 4)",
        "ref": _KWRA,
        "chains": [
            ("EXTRATROPICAL_STORM", "ENERGY_INFRASTRUCTURE", "CRITICAL_INFRA_CONDITION", "primary",
             "Sturmbedingte Netzausfälle dominieren die Stromausfallstunden; der "
             "Anlagenzustand bestimmt Häufigkeit und Dauer."),
            ("HEAT_WAVE", "ENERGY_INFRASTRUCTURE", "REDUNDANCY_BACKUP", "alternate_hazard",
             "Hitze mindert Übertragungs-/Kühlkapazität und erzwingt Lastabwürfe; Redundanz "
             "begrenzt die Ausfalldauer."),
            ("HEAVY_RAIN_FLOOD", "ENERGY_INFRASTRUCTURE", "CRITICAL_INFRA_CONDITION", "alternate_hazard",
             "Überflutete Umspannwerke fallen längerfristig aus — belegter Nebenpfad."),
        ],
    },
    "EXPECTED_WATER_SUPPLY_OUTAGE_HOURS": {
        "cluster": "Wasserwirtschaft (KWRA 2021, Teilbericht 3)",
        "ref": _KWRA,
        "chains": [
            ("DROUGHT", "WATER_WASTEWATER_INFRA", "GROUNDWATER_DEPENDENCY", "primary",
             "Dürre und sinkende Grundwasserstände sind laut KWRA der Hauptgrund für "
             "Einschränkungen der Trinkwasserversorgung; grundwasserabhängige Versorger führen."),
            ("HEAVY_RAIN_FLOOD", "WATER_WASTEWATER_INFRA", "WATER_STRESS_INDEX", "alternate_hazard",
             "Starkregen trübt/kontaminiert Rohwasser und zwingt zu Abschaltungen; "
             "Wasserstress verschärft die Lage."),
            ("CASCADE_EVENT", "WATER_WASTEWATER_INFRA", "INFRA_DEPENDENCY_CHAIN", "alternate_hazard",
             "Stromausfall legt Pumpen/Aufbereitung lahm — Kaskadenwirkung auf die "
             "Wasserversorgung."),
        ],
    },
    "EXPECTED_WASTEWATER_OUTAGE_HOURS": {
        "cluster": "Wasserwirtschaft / Abwasser (KWRA 2021, Teilbericht 3)",
        "ref": _KWRA,
        "chains": [
            ("HEAVY_RAIN_FLOOD", "WATER_WASTEWATER_INFRA", "CRITICAL_INFRA_CONDITION", "primary",
             "Starkregen überlastet Kanalnetz und Kläranlagen (Mischwasserüberläufe, "
             "Ausfall); der Anlagenzustand bestimmt die Ausfalldauer."),
            ("HEAT_WAVE", "WATER_WASTEWATER_INFRA", "SEALING_DEGREE", "alternate_hazard",
             "Hitze und hoher Versiegelungsgrad verschärfen Geruchs-/Betriebsprobleme und "
             "Trockenwetter-Ablagerungen im Kanal. Hergeleitet.", _GIZ),
        ],
    },
    "EXPECTED_COMMUNICATION_OUTAGE_HOURS": {
        "cluster": "Telekommunikation (KWRA 2021, Teilbericht 4)",
        "ref": _KWRA,
        "chains": [
            ("EXTRATROPICAL_STORM", "COMMUNICATION_INFRA", "CRITICAL_INFRA_CONDITION", "primary",
             "Sturmschäden an Masten/Leitungen dominieren die TK-Ausfallstunden; der "
             "Anlagenzustand steuert die Ausfalldauer."),
            ("HEAVY_RAIN_FLOOD", "COMMUNICATION_INFRA", "REDUNDANCY_BACKUP", "alternate_hazard",
             "Überflutete Vermittlungs-/Serverstandorte fallen aus; Netzredundanz "
             "verkürzt die Störung."),
        ],
    },
    "EXPECTED_TRANSPORT_DISRUPTION_HOURS": {
        "cluster": "Verkehr (KWRA 2021, Teilbericht 4)",
        "ref": _KWRA,
        "chains": [
            ("HEAVY_RAIN_FLOOD", "TRANSPORT_HUBS", "CRITICAL_INFRA_CONDITION", "primary",
             "Überflutete Straßen/Schienen sind der Hauptgrund klimabedingter "
             "Verkehrsunterbrechungen; der Erhaltungszustand bestimmt die Sperrdauer."),
            ("HEAT_WAVE", "TRANSPORT_HUBS", "MATERIAL_HEAT_SENSITIVITY", "alternate_hazard",
             "Hitzebedingte Langsamfahrstellen und Gleisverwerfungen unterbrechen den "
             "Betrieb; Materialanfälligkeit treibt die Dauer."),
            ("EXTRATROPICAL_STORM", "TRANSPORT_HUBS", "CRITICAL_INFRA_CONDITION", "alternate_hazard",
             "Sturm (umgestürzte Bäume, Oberleitungsschäden) legt den Bahn-/Straßenverkehr "
             "lahm — belegter Nebenpfad."),
        ],
    },
    "EXPECTED_SUPPLY_CHAIN_DISRUPTION_HOURS": {
        "cluster": "Industrie & Gewerbe (KWRA 2021, Teilbericht 5)",
        "ref": _KWRA,
        "chains": [
            ("HEAVY_RAIN_FLOOD", "SUPPLY_CHAIN_NODES", "SUPPLY_CHAIN_DEPENDENCY", "primary",
             "Überflutung von Logistikknoten unterbricht Lieferketten; die Abhängigkeit von "
             "einzelnen Knoten bestimmt die Wirkung (KWRA Industrie & Gewerbe)."),
            ("DROUGHT", "INDUSTRIAL_COMMERCIAL_AREAS", "SINGLE_SITE_DEPENDENCY", "alternate_hazard",
             "Niedrigwasser stört Rohstoff-/Kühlwasserversorgung und Schiffstransport; "
             "Ein-Standort-Abhängigkeit verschärft die Störung."),
            ("CASCADE_EVENT", "SUPPLY_CHAIN_NODES", "SUPPLY_CHAIN_DEPENDENCY", "compound_hv",
             "Kaskadierende Infrastrukturausfälle pflanzen sich in die Lieferkette fort. "
             "Hergeleitet nach H×E×V-Schema.", _GIZ),
        ],
    },
    "EXPECTED_ADMIN_OUTAGE_HOURS": {
        "cluster": "Bevölkerungsschutz / Verwaltung (KWRA 2021, Teilbericht 4/6)",
        "ref": _KWRA,
        "chains": [
            ("HEAVY_RAIN_FLOOD", "POPULATION_DENSITY", "EMERGENCY_MANAGEMENT", "primary",
             "Extremereignisse binden und überlasten die kommunale Verwaltung/Leitstellen; "
             "das Notfallmanagement bestimmt die Ausfallwirkung. Hergeleitet.", _GIZ),
            ("CASCADE_EVENT", "POPULATION_DENSITY", "PLANNING_IMPLEMENTATION_CAPACITY", "alternate_hazard",
             "Kaskadierende Ausfälle (Strom, IT) legen Verwaltungsdienste lahm; die "
             "Umsetzungskapazität steuert die Wiederherstellung."),
        ],
    },
    "EXPECTED_FUNCTIONAL_FAILURE_DURATION": {
        "cluster": "Kritische Infrastrukturen / Kaskaden (KWRA 2021, Teilbericht 6)",
        "ref": _KWRA,
        "chains": [
            ("CASCADE_EVENT", "ENERGY_INFRASTRUCTURE", "INFRA_DEPENDENCY_CHAIN", "primary",
             "Funktionsausfälle entstehen laut KWRA-Kaskadenanalyse, wenn Ausfälle über "
             "Abhängigkeitsketten fortlaufen; Energie ist der zentrale Knoten."),
            ("COMPOUND_EVENT", "WATER_WASTEWATER_INFRA", "INFRA_CRITICALITY", "alternate_hazard",
             "Kombinierte Ereignisse treffen mehrere Sektoren gleichzeitig; hohe "
             "Kritikalität verlängert die Ausfalldauer."),
        ],
    },
    "SYSTEMIC_DOMINO_RISK_INDEX": {
        "cluster": "Integrierte Auswertung / Kaskaden (KWRA 2021, Teilbericht 6)",
        "ref": _KWRA,
        "chains": [
            ("CASCADE_EVENT", "ENERGY_INFRASTRUCTURE", "INFRA_DEPENDENCY_CHAIN", "primary",
             "Systemische Domino-Effekte sind ein Kernbefund der KWRA (Teilbericht 6): "
             "Ausfälle springen über gekoppelte Infrastrukturen — reiner Screening-Index."),
            ("COMPOUND_EVENT", "WATER_WASTEWATER_INFRA", "REDUNDANCY_BACKUP", "alternate_hazard",
             "Gleichzeitige Belastung mehrerer Sektoren erhöht das Domino-Risiko; Redundanz "
             "dämpft die Ausbreitung."),
        ],
    },
    "EXPECTED_AGRICULTURAL_DAMAGE_EUR": {
        "cluster": "Landwirtschaft (KWRA 2021, Teilbericht 2)",
        "ref": _KWRA,
        "chains": [
            ("DROUGHT", "AGRICULTURAL_LAND", "IRRIGATION_DEPENDENCY", "primary",
             "Dürre/Bodentrockenheit ist laut KWRA der mit Abstand größte Treiber von "
             "Ertragsverlusten; bewässerungsabhängige Kulturen sind am stärksten betroffen."),
            ("HEAT_WAVE", "AGRICULTURAL_LAND", "WATER_STRESS_INDEX", "alternate_hazard",
             "Hitzestress in sensiblen Wachstumsphasen mindert Erträge; Wasserstress "
             "verstärkt die Wirkung."),
            ("HEAVY_RAIN_FLOOD", "AGRICULTURAL_LAND", "SOIL_SENSITIVITY", "alternate_hazard",
             "Starkregen/Überflutung und Auswaschung schädigen Bestände und Böden — "
             "gegenläufiger, aber belegter Nebenpfad."),
        ],
    },
    "EXPECTED_SOIL_LOSS_DEGRADATION_EUR": {
        "cluster": "Boden (KWRA 2021, Teilbericht 2)",
        "ref": _KWRA,
        "chains": [
            ("HEAVY_RAIN_FLOOD", "EROSION_PRONE_SOILS", "SOIL_SENSITIVITY", "primary",
             "Wassererosion durch Starkregen ist laut KWRA der Hauptmechanismus des "
             "Bodenverlusts; erosionsanfällige, empfindliche Böden führen."),
            ("DROUGHT", "AGRICULTURAL_LAND", "IRRIGATION_DEPENDENCY", "alternate_hazard",
             "Dürre fördert Winderosion und Humusabbau auf offenen Ackerflächen."),
            ("SOIL_SALINIZATION", "EROSION_PRONE_SOILS", "SOIL_SENSITIVITY", "alternate_hazard",
             "Versalzung (küstennah/bewässerungsbedingt) degradiert Böden dauerhaft — "
             "regionaler Nebenpfad."),
        ],
    },
    "EXPECTED_SOIL_DEGRADATION": {
        "cluster": "Boden (KWRA 2021, Teilbericht 2)",
        "ref": _KWRA,
        "chains": [
            ("DROUGHT", "EROSION_PRONE_SOILS", "SOIL_SENSITIVITY", "primary",
             "Dürre und Humusabbau mindern die Bodenfruchtbarkeit; empfindliche Böden "
             "degradieren am schnellsten (KWRA Handlungsfeld Boden)."),
            ("HEAVY_RAIN_FLOOD", "AGRICULTURAL_LAND", "IRRIGATION_DEPENDENCY", "alternate_hazard",
             "Starkregen-Erosion und Verschlämmung verschärfen die Degradation auf "
             "bewirtschafteten Flächen."),
        ],
    },
    "EXPECTED_VEGETATION_DAMAGE": {
        "cluster": "Wald- und Forstwirtschaft (KWRA 2021, Teilbericht 2)",
        "ref": _KWRA,
        "chains": [
            ("DROUGHT", "FOREST_AREA", "WATER_STRESS_INDEX", "primary",
             "Trocken-/Dürrejahre verursachen laut KWRA großflächige Wald-/Vegetationsschäden "
             "(Absterben, Schädlingsbefall); wasserstressanfällige Bestände führen."),
            ("WILDFIRE", "FOREST_AREA", "WILDFIRE_SUSCEPTIBILITY", "alternate_hazard",
             "Vegetationsbrände zerstören Bestände; die Brandanfälligkeit (Baumart, "
             "Trockenheit) bestimmt das Ausmaß."),
            ("HEAT_WAVE", "AGRICULTURAL_LAND", "WATER_STRESS_INDEX", "alternate_hazard",
             "Hitzestress schädigt Dauerkulturen und Grünland — belegter Nebenpfad."),
        ],
    },
    "EXPECTED_BIODIVERSITY_LOSS": {
        "cluster": "Biologische Vielfalt (KWRA 2021, Teilbericht 2)",
        "ref": _KWRA,
        "chains": [
            ("MEAN_TEMPERATURE_RISE", "BIODIVERSITY_HOTSPOTS", "BIODIVERSITY_RESILIENCE", "primary",
             "Die Klimaerwärmung verschiebt Areale und gefährdet klimasensible Arten; "
             "Hotspots mit geringer Resilienz verlieren am meisten (KWRA Biol. Vielfalt)."),
            ("DROUGHT", "FOREST_AREA", "BIODIVERSITY_RESILIENCE", "alternate_hazard",
             "Dürre destabilisiert Wald-Ökosysteme und deren Artengemeinschaften."),
            ("WILDFIRE", "BIODIVERSITY_HOTSPOTS", "WILDFIRE_SUSCEPTIBILITY", "alternate_hazard",
             "Brände vernichten Habitate in besonders schützenswerten Räumen."),
        ],
    },
    "EXPECTED_HABITAT_LOSS": {
        "cluster": "Biologische Vielfalt (KWRA 2021, Teilbericht 2/3)",
        "ref": _KWRA,
        "chains": [
            ("DROUGHT", "BIODIVERSITY_HOTSPOTS", "BIODIVERSITY_RESILIENCE", "primary",
             "Austrocknung von Feuchtlebensräumen ist ein zentraler Habitatverlust-Pfad; "
             "resilienzarme Hotspots sind am stärksten bedroht."),
            ("SEA_LEVEL_RISE", "COASTAL_RIPARIAN_ZONES", "EROSION_SUSCEPTIBILITY", "alternate_hazard",
             "Meeresspiegelanstieg und Küstenerosion verkleinern Watt-/Auen-Habitate — "
             "KWRA-Cluster Küste/Wasser."),
            ("WILDFIRE", "FOREST_AREA", "BIODIVERSITY_RESILIENCE", "alternate_hazard",
             "Brände zerstören Waldhabitate flächenhaft — belegter Nebenpfad."),
        ],
    },
    "ECOSYSTEM_DEGRADATION_RISK_INDEX": {
        "cluster": "Biologische Vielfalt / Ökosysteme (KWRA 2021, Teilbericht 2)",
        "ref": _KWRA,
        "chains": [
            ("MEAN_TEMPERATURE_RISE", "GROUNDWATER_DEPENDENT_ECOSYSTEMS", "BIODIVERSITY_RESILIENCE", "primary",
             "Erwärmung und sinkende Wasserverfügbarkeit degradieren grundwasserabhängige "
             "Ökosysteme; geringe Resilienz beschleunigt den Zustandsverlust (Screening-Index)."),
            ("DROUGHT", "FOREST_AREA", "SOIL_SENSITIVITY", "alternate_hazard",
             "Dürre und Bodendegradation mindern die Ökosystemfunktion in Wäldern."),
        ],
    },
    "ECOSYSTEM_FRAGMENTATION_RISK_INDEX": {
        "cluster": "Biologische Vielfalt (KWRA 2021, Teilbericht 2)",
        "ref": _KWRA,
        "chains": [
            ("MEAN_TEMPERATURE_RISE", "FOREST_AREA", "BIODIVERSITY_RESILIENCE", "primary",
             "Klimabedingte Arealverschiebungen und Nutzungsdruck zerschneiden Lebensräume; "
             "resilienzarme Waldflächen fragmentieren zuerst (Screening-Index)."),
            ("WILDFIRE", "BIODIVERSITY_HOTSPOTS", "GREEN_SPACE_SHARE", "alternate_hazard",
             "Brände und fehlende Vernetzungsflächen verstärken die Fragmentierung. "
             "Hergeleitet.", _GIZ),
        ],
    },
    "EXPECTED_ECOSYSTEM_SERVICE_LOSS": {
        "cluster": "Biologische Vielfalt / Ökosystemleistungen (KWRA 2021, Teilbericht 2)",
        "ref": _KWRA,
        "chains": [
            ("DROUGHT", "FOREST_AREA", "BIODIVERSITY_RESILIENCE", "primary",
             "Dürregeschädigte Wälder und Böden verlieren Kühl-, Wasser- und "
             "Kohlenstoffleistungen; resilienzarme Bestände zuerst (bewertet über ÖSL-Wert)."),
            ("HEAVY_RAIN_FLOOD", "FLOODPLAINS", "GREEN_SPACE_SHARE", "alternate_hazard",
             "Verlust von Auen-/Retentionsflächen mindert die Hochwasser-Regulationsleistung."),
            ("SEA_LEVEL_RISE", "GROUNDWATER_DEPENDENT_ECOSYSTEMS", "BIODIVERSITY_RESILIENCE", "alternate_hazard",
             "Salzwasserintrusion beeinträchtigt küstennahe Ökosystemleistungen — "
             "regionaler Nebenpfad."),
        ],
    },
    "ENVIRONMENTAL_FEEDBACK_RISK_INDEX": {
        "cluster": "Integrierte Auswertung / Rückkopplungen (KWRA 2021, Teilbericht 6)",
        "ref": _KWRA,
        "chains": [
            ("COMPOUND_EVENT", "FOREST_AREA", "BIODIVERSITY_RESILIENCE", "primary",
             "Kombinierte Störungen (Dürre + Feuer + Schädlinge) lösen sich selbst "
             "verstärkende Rückkopplungen aus (z. B. Kohlenstofffreisetzung) — Screening-Index."),
            ("WILDFIRE", "BIODIVERSITY_HOTSPOTS", "WILDFIRE_SUSCEPTIBILITY", "alternate_hazard",
             "Großbrände setzen gespeicherten Kohlenstoff frei und verstärken die Erwärmung. "
             "Hergeleitet.", _GIZ),
        ],
    },
    "HYDROLOGICAL_STRESS_RISK_INDEX": {
        "cluster": "Wasserhaushalt (KWRA 2021, Teilbericht 3)",
        "ref": _KWRA,
        "chains": [
            ("DROUGHT", "GROUNDWATER_DEPENDENT_ECOSYSTEMS", "WATER_STRESS_INDEX", "primary",
             "Dürre und sinkende Grund-/Niedrigwasserstände sind laut KWRA der zentrale "
             "Wasserstress-Treiber; wasserstressbelastete Räume führen (Screening-Index)."),
            ("HEAVY_RAIN_FLOOD", "FLOODPLAINS", "GROUNDWATER_DEPENDENCY", "alternate_hazard",
             "Das Gegenextrem Hochwasser belastet Auen und Wasserwirtschaft gleichermaßen."),
            ("SOIL_MOISTURE_DECLINE", "WATER_WASTEWATER_INFRA", "WATER_STRESS_INDEX", "alternate_hazard",
             "Rückläufige Bodenfeuchte verschärft die Wasserbilanz und den Versorgungsdruck."),
        ],
    },
    "EXPECTED_WATER_AIR_POLLUTION": {
        "cluster": "Wasserhaushalt / Luft (KWRA 2021, Teilbericht 3/5)",
        "ref": _KWRA,
        "chains": [
            ("HEAT_WAVE", "POPULATION_DENSITY", "AIR_QUALITY_RISK", "primary",
             "Hitze fördert Ozon-/Feinstaubbildung und Gewässererwärmung (Sauerstoffmangel); "
             "dicht besiedelte Belastungsräume führen (Screening-Index)."),
            ("HEAVY_RAIN_FLOOD", "FLOODPLAINS", "WATER_STRESS_INDEX", "alternate_hazard",
             "Starkregen spült Schad-/Nährstoffe in Gewässer (Einträge, Überläufe); "
             "Wasserstress verschärft die Wirkung."),
        ],
    },
    "EXPECTED_FISHERIES_ECONOMIC_LOSS_EUR": {
        "cluster": "Fischerei (KWRA 2021, Teilbericht 3)",
        "ref": _KWRA,
        "chains": [
            ("SURFACE_WATER_HEATING", "FISHERIES_AQUACULTURE_AREAS", "FISHERIES_TEMPERATURE_SENSITIVITY", "primary",
             "Erwärmung der Oberflächengewässer ist laut KWRA der Haupttreiber von "
             "Fischereiverlusten; temperatursensible Bestände/Betriebe führen."),
            ("LOW_FLOW_NIEDRIGWASSER", "FISHERIES_AQUACULTURE_AREAS", "FISHERIES_MANAGEMENT_CAPACITY", "alternate_hazard",
             "Niedrigwasser reduziert Lebensraum und Sauerstoff; die Bewirtschaftungskapazität "
             "moderiert den Ertragsverlust."),
            ("DROUGHT", "FISHERIES_AQUACULTURE_AREAS", "FISHERIES_TEMPERATURE_SENSITIVITY", "alternate_hazard",
             "Dürrebedingte Wasserknappheit verschärft Hitze- und Sauerstoffstress — "
             "belegter Nebenpfad."),
        ],
    },
    "EXPECTED_AQUACULTURE_DAMAGE_EUR": {
        "cluster": "Fischerei / Aquakultur (KWRA 2021, Teilbericht 3)",
        "ref": _KWRA,
        "chains": [
            ("SURFACE_WATER_HEATING", "FISHERIES_AQUACULTURE_AREAS", "AQUACULTURE_TECHNICAL_VULNERABILITY", "primary",
             "Warmwasserphasen verursachen Sauerstoffmangel und Verluste in Teich-/"
             "Anlagenaquakultur; die technische Anfälligkeit der Anlagen bestimmt den Schaden."),
            ("LOW_FLOW_NIEDRIGWASSER", "FISHERIES_AQUACULTURE_AREAS", "WATER_STRESS_INDEX", "alternate_hazard",
             "Niedrigwasser begrenzt Wasserzufuhr/Durchfluss der Anlagen; Wasserstress "
             "verschärft die Lage."),
            ("HEAVY_RAIN_FLOOD", "FISHERIES_AQUACULTURE_AREAS", "AQUACULTURE_TECHNICAL_VULNERABILITY", "alternate_hazard",
             "Überflutung schwemmt Bestände aus und beschädigt Anlagen — belegter Nebenpfad."),
        ],
    },
    "FISHERIES_STOCK_STRESS_RISK_INDEX": {
        "cluster": "Fischerei (KWRA 2021, Teilbericht 3)",
        "ref": _KWRA,
        "chains": [
            ("SURFACE_WATER_HEATING", "FISH_SPAWNING_HABITATS", "FISHERIES_TEMPERATURE_SENSITIVITY", "primary",
             "Gewässererwärmung stresst Laichhabitate und temperatursensible Bestände — "
             "zentraler Bestandsstress-Pfad (Screening-Index)."),
            ("OCEAN_WARMING", "FISHERIES_AQUACULTURE_AREAS", "BIODIVERSITY_RESILIENCE", "alternate_hazard",
             "Meereserwärmung verschiebt Fischbestände und belastet resilienzarme "
             "Ökosysteme — KWRA-Cluster Meere/Küste."),
        ],
    },
    "LOW_WATER_FISHERIES_IMPACT_INDEX": {
        "cluster": "Fischerei / Wasserhaushalt (KWRA 2021, Teilbericht 3)",
        "ref": _KWRA,
        "chains": [
            ("LOW_FLOW_NIEDRIGWASSER", "FISH_SPAWNING_HABITATS", "FISHERIES_TEMPERATURE_SENSITIVITY", "primary",
             "Niedrigwasser verkleinert und erwärmt Laichhabitate; temperatursensible "
             "Arten sind am stärksten betroffen (Screening-Index)."),
            ("DROUGHT", "FISHERIES_AQUACULTURE_AREAS", "GROUNDWATER_DEPENDENCY", "alternate_hazard",
             "Dürre senkt Zuflüsse/Grundwasserspeisung der Gewässer und verschärft den "
             "Niedrigwasserstress."),
        ],
    },
    "EXPECTED_INDIRECT_ECONOMIC_LOSS_EUR": {
        "cluster": "Industrie & Gewerbe / Volkswirtschaft (KWRA 2021, Teilbericht 5/6)",
        "ref": _KWRA,
        "chains": [
            ("CASCADE_EVENT", "INDUSTRIAL_COMMERCIAL_AREAS", "SUPPLY_CHAIN_DEPENDENCY", "primary",
             "Indirekte Verluste entstehen laut KWRA aus fortlaufenden Betriebs-/"
             "Lieferkettenunterbrechungen nach Extremereignissen; Ketten-Abhängigkeit treibt "
             "die Wirkung. Im Modell über k_indirekt aus den direkten Schäden abgeleitet."),
            ("DROUGHT", "SUPPLY_CHAIN_NODES", "FINANCIAL_ADAPTATION_CAPACITY", "alternate_hazard",
             "Niedrigwasser-/Dürrefolgen bremsen Produktion und Transport; Finanzkraft "
             "moderiert die Verluste."),
        ],
    },
    "EXPECTED_SUPPLY_SHORTAGE_COSTS_EUR": {
        "cluster": "Industrie & Gewerbe / Versorgung (KWRA 2021, Teilbericht 5)",
        "ref": _KWRA,
        "chains": [
            ("DROUGHT", "SUPPLY_CHAIN_NODES", "SUPPLY_CHAIN_DEPENDENCY", "primary",
             "Dürre-/Niedrigwasserlagen führen zu Rohstoff- und Versorgungsengpässen; "
             "die Ketten-Abhängigkeit bestimmt die Kostenwirkung. Folgekosten — im Modell "
             "über k_indirekt aus den direkten Schäden abgeleitet."),
            ("HEAT_WAVE", "AGRICULTURAL_LAND", "WATER_STRESS_INDEX", "alternate_hazard",
             "Hitze-/Ernteausfälle verteuern Agrarrohstoffe und Vorprodukte."),
        ],
    },
    "EXPECTED_CLIMATE_MIGRATION_COSTS_EUR": {
        "cluster": "Integrierte Auswertung / Migration (KWRA 2021, Teilbericht 6)",
        "ref": _KWRA,
        "chains": [
            ("SEA_LEVEL_RISE", "COASTAL_STORM_SURGE_EXPOSURE", "INCOME_SOCIAL_RESILIENCE", "primary",
             "Dauerhafte Küstenrisiken (Meeresspiegel, Sturmflut) können Verdrängung/"
             "Umsiedlung auslösen; geringe soziale Resilienz erhöht die Folgekosten. "
             "In DE geringe, aber ausgewiesene Größenordnung."),
            ("DROUGHT", "POPULATION_DENSITY", "FINANCIAL_ADAPTATION_CAPACITY", "alternate_hazard",
             "Wasserknappheit kann regionale Abwanderung begünstigen; Finanzkraft "
             "moderiert. Hergeleitet.", _GIZ),
        ],
    },
    "EXPECTED_LOCATION_DISADVANTAGE_EUR": {
        "cluster": "Finanzwirtschaft / Standort (KWRA 2021, Teilbericht 5)",
        "ref": _KWRA,
        "chains": [
            ("HEAVY_RAIN_FLOOD", "LOCATION_HAZARD_ZONES", "SINGLE_SITE_DEPENDENCY", "primary",
             "Wiederkehrende Gefahrenlagen mindern Standort-/Immobilienwerte und "
             "Versicherbarkeit; Ein-Standort-Abhängigkeit verschärft den Nachteil. "
             "Folgekosten — im Modell über k_indirekt abgeleitet."),
            ("HEAT_WAVE", "INDUSTRIAL_COMMERCIAL_AREAS", "FINANCIAL_ADAPTATION_CAPACITY", "alternate_hazard",
             "Hitzebelastete Standorte verlieren an Attraktivität; Anpassungskapazität "
             "puffert. Hergeleitet.", _GIZ),
        ],
    },
    "EXPECTED_DELAYED_DAMAGE_COSTS_EUR": {
        "cluster": "Integrierte Auswertung / verzögerte Schäden (KWRA 2021, Teilbericht 6)",
        "ref": _KWRA,
        "chains": [
            ("COMPOUND_EVENT", "BUILDING_STOCK", "PLANNING_IMPLEMENTATION_CAPACITY", "primary",
             "Verzögerte Schäden (Spätfolgen, aufgeschobene Instandsetzung) sind der "
             "zeitversetzte Anteil der direkten Schäden; die Umsetzungskapazität bestimmt "
             "die Nachlaufkosten. Abgrenzungsproblem — im Modell nicht additiv gezählt."),
            ("CASCADE_EVENT", "ENERGY_INFRASTRUCTURE", "FINANCIAL_ADAPTATION_CAPACITY", "alternate_hazard",
             "Kaskadenschäden zeigen sich teils erst später (Materialermüdung); Finanzkraft "
             "steuert die Behebung. Hergeleitet.", _GIZ),
        ],
    },
    "RESOURCE_CONFLICT_RISK_INDEX": {
        "cluster": "Integrierte Auswertung / Nutzungskonflikte (KWRA 2021, Teilbericht 6)",
        "ref": _KWRA,
        "chains": [
            ("DROUGHT", "AGRICULTURAL_LAND", "WATER_STRESS_INDEX", "primary",
             "Wasserknappheit verschärft laut KWRA Nutzungskonflikte zwischen Landwirtschaft, "
             "Versorgung und Ökologie; wasserstressbelastete Räume führen (Screening-Index)."),
            ("SOIL_MOISTURE_DECLINE", "POPULATION_DENSITY", "INCOME_SOCIAL_RESILIENCE", "alternate_hazard",
             "Rückläufige Wasserverfügbarkeit in dicht genutzten Räumen erhöht das "
             "Konfliktpotenzial; soziale Resilienz moderiert. Hergeleitet.", _GIZ),
        ],
    },
}
