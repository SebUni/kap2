"""Fest verdrahteter Fachkatalog (einmalig portiert aus den KAP3-CSVs).

Dieser Katalog ist die EINZIGE Quelle der Wahrheit für klimatische Einflüsse (Hazards),
räumliche Expositionen, Sensitivitäten, Risiken und Maßnahmen. Es gibt bewusst keinen
Laufzeit-CSV-Parser und kein generisches Katalogsystem – die Inhalte sind als
Python-Konstanten hinterlegt (siehe Plan).

Konventionen
------------
* Klimatische Einflüsse/räumliche Expositionen/Sensitivitäten werden pro 100m-Zelle in ihrer
  ABSOLUTEN Einheit berechnet und angezeigt (``unit``).
* ``norm_min`` / ``norm_max`` definieren die Referenzskala, die AUSSCHLIESSLICH
  für die Risikoberechnung genutzt wird (Normalisierung auf 0..1). Sie hat keinen
  Einfluss auf die Darstellung der H/E/V-Werte.
* ``spatial=False`` markiert Indikatoren ohne lokalen räumlichen Proxy – diese
  bekommen einen regionalen/nationalen Konstantwert und werden in UI + Handbuch
  als „nicht räumlich aufgelöst" gekennzeichnet.
* Risiken werden über Wirkungsketten komponiert (siehe ``build_pathways`` und
  ``PATHWAY_WEIGHTS``; reproduziert die Logik aus ``risk_composition.csv`` +
  ``pathway_weight_defaults.csv`` deterministisch aus den H/E/V-Listen).
"""

from __future__ import annotations

# ── KWRA-Risikogruppen (max. 5) – für Spinnendiagramme & Risiko-Gruppierung ────

KWRA_GROUPS: list[dict] = [
    {"code": "heat", "challenge": "KWRA_CHALLENGE_HEAT",
     "label": "Hitze", "color": "#ef4444",
     "description": "Extreme Hitze, Gesundheit und urbane Überwärmung."},
    {"code": "drought", "challenge": "KWRA_CHALLENGE_DROUGHT_LOW_WATER",
     "label": "Trockenheit & Niedrigwasser", "color": "#f59e0b",
     "description": "Trockenheit, Niedrigwasser und sinkende Grundwasserstände."},
    {"code": "flood", "challenge": "KWRA_CHALLENGE_FLOOD",
     "label": "Hochwasser & Starkregen", "color": "#3b82f6",
     "description": "Hochwasser, Starkregen und Sturzfluten."},
    {"code": "gradual", "challenge": "KWRA_CHALLENGE_GRADUAL_CHANGE",
     "label": "Gradueller Wandel", "color": "#22c55e",
     "description": "Gradueller Temperatur-/Meeresspiegelanstieg, Ökosysteme."},
    {"code": "compound", "challenge": "KWRA_CHALLENGE_COMPOUND_SYSTEMIC",
     "label": "Verbund & Kaskaden", "color": "#8b5cf6",
     "description": "Verbund-, Kaskaden- und systemische Risiken."},
]

CHALLENGE_TO_GROUP = {g["challenge"]: g["code"] for g in KWRA_GROUPS}


# ── Klimatische Einflüsse (Hazards) ────────────────────────────────────────────
# unit = absolute Einheit; norm_* = Referenzskala nur für Risikoberechnung.
# spatial = ob lokal räumlich auflösbar; proxy/source = Tooltip + Handbuch.

HAZARDS: list[dict] = [
    {"code": "HEAT_WAVE", "name": "Hitzeextreme / Hitzewellen",
     "unit": "Tage/Jahr", "norm_min": 0.0, "norm_max": 40.0, "spatial": True,
     "description": "Akute oder anhaltende extreme Hitzeereignisse.",
     "proxy": "DWD-CDC heiße-Tage-Raster (1 km, am Kommune-Zentroid) + UHI-Modell (ΔT) pro 100m-Zelle aus OSM (siehe Handbuch).",
     "source": "DWD CDC (Raster) + UHI-Modell (OSM)",
     "source_detail": "Normierungs-Obergrenze 40 heiße Tage/Jahr orientiert sich an der "
        "beobachteten und projizierten Zunahme heißer Tage (Tmax ≥ 30 °C) in Deutschland "
        "(DWD Nationaler Klimareport). Die Zell-Werte stammen aus dem DWD-CDC-Raster zzgl. "
        "UHI-Aufschlag; editierbar.",
     "source_refs": ["DWD_Klimareport"]},
]


# ── Räumliche Expositionen ────────────────────────────────────────────────────

EXPOSURES: list[dict] = [
    {"code": "POPULATION_DENSITY", "name": "Bevölkerungsdichte",
     "unit": "Pers./km²", "norm_min": 0.0, "norm_max": 8000.0, "spatial": True,
     "description": "Räumliche Dichte der Bevölkerung.",
     "proxy": "Zensus-2022-100m-Gitter: Bevölkerungszahl je Zelle / Fläche.",
     "source": "Zensus 2022 (100m-Gitter, Destatis)",
     "source_detail": "Werte und Normierungsskala basieren auf dem Zensus 2022 (Destatis) im "
        "100-Meter-Gitter (Bevölkerungszahl, Altersanteile ≥65/<18 Jahre bzw. sozioökonomische "
        "Merkmale je Zelle). Die Referenzskala (norm_min/norm_max) ist eine dokumentierte "
        "Modellwahl auf Basis typischer Wertespannen dieser amtlichen Gitterdaten; editierbar.",
     "source_refs": ["Zensus_2022"]},
    {"code": "AGE_STRUCTURE", "name": "Altersstruktur (Ältere, Kinder)",
     "unit": "%", "norm_min": 0.0, "norm_max": 50.0, "spatial": True,
     "description": "Anteil altersbedingt vulnerabler Bevölkerungsgruppen.",
     "proxy": "Zensus-100m: Anteil ≥65 Jahre + Anteil <18 Jahre je Zelle.",
     "source": "Zensus 2022 (100m-Gitter, Destatis)",
     "source_detail": "Werte und Normierungsskala basieren auf dem Zensus 2022 (Destatis) im "
        "100-Meter-Gitter (Bevölkerungszahl, Altersanteile ≥65/<18 Jahre bzw. sozioökonomische "
        "Merkmale je Zelle). Die Referenzskala (norm_min/norm_max) ist eine dokumentierte "
        "Modellwahl auf Basis typischer Wertespannen dieser amtlichen Gitterdaten; editierbar.",
     "source_refs": ["Zensus_2022"]},
    {"code": "VULNERABLE_GROUPS_POPULATION", "name": "Vulnerable Gruppen (Personen)",
     "unit": "Pers.", "norm_min": 0.0, "norm_max": 2000.0, "spatial": True,
     "description": "Bevölkerungsgruppen mit erhöhter Schadenswahrscheinlichkeit.",
     "proxy": "Zensus-100m: Bevölkerung × (Anteil ≥65 + Anteil <18) je Zelle.",
     "source": "Zensus 2022 (100m-Gitter, Destatis)",
     "source_detail": "Werte und Normierungsskala basieren auf dem Zensus 2022 (Destatis) im "
        "100-Meter-Gitter (Bevölkerungszahl, Altersanteile ≥65/<18 Jahre bzw. sozioökonomische "
        "Merkmale je Zelle). Die Referenzskala (norm_min/norm_max) ist eine dokumentierte "
        "Modellwahl auf Basis typischer Wertespannen dieser amtlichen Gitterdaten; editierbar.",
     "source_refs": ["Zensus_2022"]},
]


# ── Sensitivitäten ──────────────────────────────────────────────────────────────
# Die meisten sind Index 0..100 (höher = verwundbarer). Anpassungskapazitäten
# (z. B. Frühwarnung, Redundanz) werden invertiert gespeichert, sodass ein hoher
# Wert immer „mehr Risiko" bedeutet.

VULNERABILITIES: list[dict] = [
    {"code": "HEALTHCARE_ACCESS", "name": "Zugang zu Gesundheitsdiensten (invers)", "unit": "Index",
     "norm_min": 0.0, "norm_max": 100.0, "spatial": True,
     "description": "Erreichbarkeit von Gesundheitsdiensten (hoher Wert = schlechter Zugang).",
     "proxy": "100 · (1 − (0,5·prox(KH) + 0,35·prox(Arzt) + 0,15·prox(Apo))); prox = 1 − min(dist,20km)/20km; dist = Luftlinie × 1,3.",
     "source": "OSM"},
    {"code": "HEAT_SENSITIVITY", "name": "Hitzesensitivität", "unit": "Index",
     "norm_min": 0.0, "norm_max": 100.0, "spatial": True,
     "description": "Gesundheitliche Empfindlichkeit gegenüber Hitze.",
     "proxy": "Altersstruktur + UHI-Intensität + geringer Grünanteil pro Zelle.",
     "source": "Zensus + UHI-Modell"},
]


# ── Risiken ──────────────────────────────────────────────────────────────────────
# group = KWRA-Gruppe (Code); cost_dimension ∈ {health, monetary, environment, operational}
# hazards/exposures/vulnerabilities = Listen (erste = primär).
# ref_value = Outcome-Wert bei Index=100 für eine Referenzkommune mit 100.000 Ew.
# scale = wie der Outcome mit der Kommune skaliert: pop | area | flat.
# Für cost_dimension=='monetary' ist ref_value in €/Jahr (Schadenkosten).

RISKS: list[dict] = [
    # KWRA-1:1-Klammer (M0): 1 Klimawirkung = kwra_id; #95 „Hitzebelastung" wird
    # als zwei Teil-Ausweise geführt (Mortalität + Erkrankungen), weil der
    # Ergebnis-Kontrakt genau ein natives Ergebnis je Risiko-Code verlangt
    # (Präsentations-Fusion; docs/ROADMAP.md §5, Plan AP3a).
    {"code": "EXPECTED_ANNUAL_MORTALITY", "name": "Hitzebelastung — Mortalität",
     "kwra_id": 95, "kwra_name": "Hitzebelastung", "kwra_field": "Menschliche Gesundheit", "stage": 0,
     # Rev. 7 (Bericht #95 §3.6): native Ergebnisgröße sind verlorene Lebensjahre
     # (YLL); Todesfälle laufen als Teil-Ausweis (runner materialisiert "deaths").
     "outcome_unit": "YLL/Jahr", "group": "heat", "cost_dimension": "health",
     # Gefahrenliste = was die Schadensfunktion TATSÄCHLICH rechnet. Vorher standen
     # hier zusätzlich COLD_EXTREME und COMPOUND_EVENT, die nie in die Rechnung
     # eingingen — der Name „(Hitze)“ und die Metadaten stimmen jetzt überein.
     "hazards": ["HEAT_WAVE"],
     "exposures": ["POPULATION_DENSITY", "VULNERABLE_GROUPS_POPULATION", "AGE_STRUCTURE"],
     "vulnerabilities": ["HEALTHCARE_ACCESS"],
     # Herleitung ref_value (Sanity-Anker, YLL/100k): 18 Todesfälle/100k (≈ 1,7×
     # schlimmstes beobachtetes Jahr, 2018: ~8.700 Tote) × mittlere Restlebens-
     # erwartung je Hitze-Sterbefall 8,79 Jahre (RKI-Altersanteile 6,5/12,9/25,2/
     # 55,5 % × L̄_a 23,39/15,59/8,90/5,44) ≈ 158 YLL/100k.
     # cost_per_outcome_eur: VOLY 160.800 €₂₀₂₄ (UBA MK 4.0; Herleitung s. _RISK_COST_RATES).
     "ref_value": 158.0, "scale": "pop", "cost_per_outcome_eur": 160800.0,
     "source": "Bericht #95 Rev. 7 (Winklmayr 2022 / RKI EB 19/2025 / UBA MK 4.0)",
     "source_detail": "Sanity-Anker in YLL je 100.000 EW: 18 Todesfälle/100k (≈ 1,7× "
                      "schlimmstes beobachtetes Jahr; 2018 revidiert: 8.500 ≈ 10,2/100k) "
                      "× mittlere Restlebenserwartung je Hitze-Sterbefall 8,79 Jahre "
                      "(RKI-Altersanteile 6,5/12,9/25,2/55,5 % × L̄_a 23,39/15,59/8,90/"
                      "5,44) ≈ 158 YLL/100k. Kein Rechenweg — Schicht B rechnet die "
                      "Schadensfunktion; der Anker dient der Sanity-Prüfung (Faktor 5).",
     "source_refs": ["RKI_EpidBull_19_2025", "Winklmayr_2022",
                     "Destatis_Sterbetafeln_2022_2024"],
     "description": "Verlorene Lebensjahre (YLL) durch hitzebedingte Sterblichkeit nach "
                    "der altersgeschichteten Expositions-Wirkungs-Kurve des RKI "
                    "(empirische Wochenquantile, vier Altersbänder, drei Regionen; "
                    "Todesfälle als Teil-Ausweis). Bewerteter Schaden — Konto K1 "
                    "Gesundheit (Modellstand M0, Untergrenze).",
     "priority": 1},
    {"code": "EXPECTED_ANNUAL_MORBIDITY", "name": "Hitzebelastung — Erkrankungen",
     "kwra_id": 95, "kwra_name": "Hitzebelastung", "kwra_field": "Menschliche Gesundheit", "stage": 0,
     "outcome_unit": "Fälle/Jahr", "group": "heat", "cost_dimension": "health",
     # Gefahrenliste an die Formel angeglichen: gerechnet wird ausschließlich mit HEAT_WAVE.
     # DISEASE_VECTOR_SUSCEPTIBILITY entfernt: kein Beleg in der Schadensbaum-
     # Sensitivitätsliste S152–S158 der Klimawirkung #95 (W182).
     "hazards": ["HEAT_WAVE"],
     "exposures": ["POPULATION_DENSITY", "VULNERABLE_GROUPS_POPULATION"],
     "vulnerabilities": ["HEAT_SENSITIVITY", "HEALTHCARE_ACCESS"],
     # Herleitung ref_value (Sanity-Anker, Fälle/100k): Baseline 3,54/100k·a
     # (Bericht #95 §3.4, bevölkerungsgewichtete Summe der r_0,a); Hitzejahr mit
     # e_HD-Obergrenze ≈ 4,5/100k — Anker auf das Hitzejahr gesetzt.
     # cost_per_outcome_eur: c_Fall 7.152 €₂₀₂₄ (Destatis-Kostennachweis, Proxy).
     "ref_value": 4.5, "scale": "pop", "cost_per_outcome_eur": 7152.0,
     "source": "Bericht #95 Rev. 7 (Destatis T67 / Karlsson & Ziebarth 2018)",
     "source_detail": "Sanity-Anker in Fällen je 100.000 EW: Baseline 3,54/100k·a "
                      "(bevölkerungsgewichtete Summe der r_0,a, Bericht #95 §3.4); "
                      "Hitzejahr mit e_HD-Obergrenze ≈ 4,5/100k. Kein Rechenweg — der "
                      "Anker dient der Sanity-Prüfung (Faktor 5).",
     "source_refs": ["Destatis_T67_Hitzeeinweisungen", "Karlsson_Ziebarth_2018"],
     "description": "Hitzeassoziierte Erkrankungsfälle (Krankenhauseinweisungen): "
                    "altersgeschichtete Baseline × Hitzetage-Term um die Referenzlast "
                    "(Bericht #95 §3.4). Bewerteter Schaden — Konto K1 (M0, Untergrenze).",
     "priority": 1},
    # EXPECTED_TOTAL_DAMAGE_EAD_EUR (Gesamtschäden/EAD) wurde ENTFERNT: Der Gesamtschaden
    # ist kein eigenständiges HxVxE-Risiko mehr, sondern die SUMME der monetär bewerteten
    # Einzelrisiken (risk_engine.aggregate → cost.total_eur). Das eigene EAD-Risiko war per
    # Konstruktion ~die Summe der Sektorschäden und verdoppelte diese in total_eur (siehe
    # docs/MODELL_KRITIK.md §3.7). Maßnahmen, die früher auf EAD wirkten, sind auf die
    # konkreten Sektorschadens-Risiken umverdrahtet.
]


# ── Roadmap-Stufen + geplante (gesperrte) Risiken ─────────────────────────────
# Öffentliche Stufen-Labels (docs/ROADMAP.md §5 / docs/ROADMAP_PUBLIC.html).
# stage 0 = aktueller M0-Release „Sommer 2026".
STAGE_LABELS: dict[int, str] = {
    0: "Sommer 2026",
    1: "Herbst 2026",
    2: "Spätherbst 2026",
    3: "Jahreswechsel 2026/27",
    4: "Frühjahr 2027",
    5: "Perspektive",
}

# Geplante KWRA-Klimawirkungen: im Produkt sichtbar, aber gesperrt („Klimarisiko
# folgt <Stufe>"). Bewusst NICHT in RISKS/Index-Maps/Engine/Ratchets. Die
# H/V/E-Namenslisten stammen 1:1 aus docs/KWAR/KWRA-2021_Klimawirkungen.xlsx,
# Sheet „Wirkungsmechanismen" (= Schadensbaum-Digitalisat); Stufen-Zuordnung aus
# docs/ROADMAP.md §5. #96/#98 tragen stage 0: Sie gehören zum Sommer-Release und
# wechseln nach der Methodik-Freigabe (docs/METHODIK_M0_GESUNDHEIT.pdf) von hier
# in RISKS. Zusammen mit kwra_id 95 (aktiv) sind alle 52 Roadmap-Klimawirkungen
# genau einmal vertreten (Test: tests/test_planned_risks.py).
PLANNED_RISKS: list[dict] = [
    {"kwra_id": 96, "name": "Allergische Reaktionen durch Aeroallergene pflanzlicher Herkunft",
     "cluster": "gesundheit", "kwra_field": "Menschliche Gesundheit", "stage": 0,
     "hazard_names": [],
     "upstream_names": ["Vegetation", "Ausbreitung von Pflanzenarten mit allergenem Potenzial", "Pollenflug"],
     "sensitivity_names": ["Individueller Gesundheitszustand", "Individuelles Gefahrenbewusstsein", "Monitoring von Gesundheitsgefahren und Frühwarnsysteme"],
     "exposure_names": ["Vorkommen von Bevölkerung", "Vorkommen von Gesundheitsinfrastruktur"]},
    {"kwra_id": 98, "name": "UV-bedingte Gesundheitsschädigungen (insbesondere Hautkrebs)",
     "cluster": "gesundheit", "kwra_field": "Menschliche Gesundheit", "stage": 0,
     "hazard_names": ["UV-Strahlung"],
     "upstream_names": [],
     "sensitivity_names": ["Individuelles Gefahrenbewusstsein", "Freizeitverhalten"],
     "exposure_names": ["Vorkommen von Bevölkerung", "Vorkommen von Gesundheitsinfrastruktur"]},
    {"kwra_id": 62, "name": "Stadtklima / Wärmeinseln",
     "cluster": "infrastruktur", "kwra_field": "Bauwesen", "stage": 1,
     "hazard_names": ["Hitze", "Sonnenscheindauer"],
     "upstream_names": ["Vegetation in Siedlungen"],
     "sensitivity_names": ["Begrünung von Städten / Siedlungen", "Grad der Versiegelung"],
     "exposure_names": ["Vorkommen von Bau- und Immobilienunternehmen", "Vorkommen von Gebäuden", "Vorkommen von Siedlungsinfrastrukturen"]},
    {"kwra_id": 63, "name": "Innenraumklima",
     "cluster": "infrastruktur", "kwra_field": "Bauwesen", "stage": 1,
     "hazard_names": ["Hitze", "Kälte / Frost", "Luftfeuchtigkeit", "Sonnenscheindauer", "Nässe"],
     "upstream_names": [],
     "sensitivity_names": ["Verwendete Baumaterialien auf Gebäudeebene", "Begrünung von Gebäuden"],
     "exposure_names": ["Vorkommen von Bau- und Immobilienunternehmen", "Vorkommen von Gebäuden", "Vorkommen von Siedlungsinfrastrukturen"]},
    {"kwra_id": 61, "name": "Vegetation in Siedlungen",
     "cluster": "infrastruktur", "kwra_field": "Bauwesen", "stage": 1,
     "hazard_names": [],
     "upstream_names": ["Verschiebung von Arealen"],
     "sensitivity_names": ["Begrünung von Städten / Siedlungen", "Grad der Versiegelung", "Bauliche, organisatorische und finanzielle Vorsorge der öffentlichen Hand"],
     "exposure_names": ["Vorkommen von Bau- und Immobilienunternehmen", "Vorkommen von Gebäuden", "Vorkommen von Siedlungsinfrastrukturen"]},
    {"kwra_id": 60, "name": "Schäden an Gebäuden aufgrund von Flusshochwasser",
     "cluster": "infrastruktur", "kwra_field": "Bauwesen", "stage": 1,
     "hazard_names": ["Hagel", "Starkregen", "Starkwind", "Schnee- und Eisdruck", "Hitze", "Kälte / Frost"],
     "upstream_names": ["Wasserstand der Meere", "Abfluss und Wasserstand von Oberflächengewässern", "Gravitative Massenbewegungen", "Grundwasserstand", "Einschränkungen der Funktionsfähigkeit von Kanalnetzen und Vorflutern"],
     "sensitivity_names": ["Zustand von Gebäuden und Infrastrukturen", "Verwendete Baumaterialien auf Gebäudeebene", "Bauliche, organisatorische und finanzielle Vorsorge der Eigentümer und Nutzer", "Zustand von (Schutz-)Infrastrukturen", "Investitionen der Bau- und Immobilienwirtschaft in exponierten Gebieten"],
     "exposure_names": ["Vorkommen von Bau- und Immobilienunternehmen", "Vorkommen von Gebäuden", "Vorkommen von Siedlungsinfrastrukturen"]},
    {"kwra_id": 50, "name": "Belastung oder Versagen von Hochwasserschutzsystemen",
     "cluster": "wasser", "kwra_field": "Wasserhaushalt, Wasserwirtschaft", "stage": 1,
     "hazard_names": [],
     "upstream_names": ["Hochwasser", "Sturzfluten"],
     "sensitivity_names": ["Art und Zustand von Hochwasserschutzinfrastruktur"],
     "exposure_names": ["Vorkommen von Oberflächengewässer und Grundwasser", "Vorkommen von Abwasser- und Entwässerungssystemen", "Vorkommen von Infrastruktur an Binnengewässern"]},
    {"kwra_id": 51, "name": "Sturzfluten (Versagen von Entwässerungseinrichtungen und Überflutungsschutzsystemen)",
     "cluster": "wasser", "kwra_field": "Wasserhaushalt, Wasserwirtschaft", "stage": 1,
     "hazard_names": ["Starkregen"],
     "upstream_names": [],
     "sensitivity_names": ["Topographie und Landnutzung", "Gewässereigenschaften"],
     "exposure_names": ["Vorkommen von Oberflächengewässer und Grundwasser", "Vorkommen von Abwasser- und Entwässerungssystemen", "Vorkommen von Infrastruktur an Binnengewässern"]},
    {"kwra_id": 47, "name": "Überlastung der Entwässerungseinrichtungen in überflutungsgefährdeten Gebieten",
     "cluster": "wasser", "kwra_field": "Küsten- und Meeresschutz", "stage": 1,
     "hazard_names": [],
     "upstream_names": ["Meeresspiegelhöhe", "Sturmfluten"],
     "sensitivity_names": ["Art und Zustand von Bauwerken und Küsteninfrastruktur"],
     "exposure_names": ["Vorkommen von Küsten, Wattenmeere, Ästuare", "Vorkommen von Meeren", "Vorkommen von Bauwerken und Infrastruktur in der Küstenzone"]},
    {"kwra_id": 55, "name": "Grundwasserstand und Grundwasserqualität",
     "cluster": "wasser", "kwra_field": "Wasserhaushalt, Wasserwirtschaft", "stage": 1,
     "hazard_names": ["Durchschnittlicher Niederschlag"],
     "upstream_names": ["Mittlerer Abfluss", "Niedrigwasser", "Biologische Wasserqualität", "Chemische Wasserqualität", "Versalzung des Bodens, des Grundwassers und von Flussmündungen"],
     "sensitivity_names": ["Bodeneigenschaften und Geologie", "Grundwasserleiter", "Stoffeintrag aus Landwirtschaft und Industrie"],
     "exposure_names": ["Vorkommen von Oberflächengewässer und Grundwasser", "Vorkommen von Abwasser- und Entwässerungssystemen", "Vorkommen von Infrastruktur an Binnengewässern"]},
    {"kwra_id": 53, "name": "Gewässertemperatur und Eisbedeckung und biologische Wasserqualität",
     "cluster": "wasser", "kwra_field": "Wasserhaushalt, Wasserwirtschaft", "stage": 1,
     "hazard_names": ["Durchschnittstemperatur", "Hitze", "Kälte / Frost", "Schneeschmelze", "Sonnenscheindauer", "Trockenheit", "Nässe", "Starkregen"],
     "upstream_names": ["Mittlerer Abfluss"],
     "sensitivity_names": ["Gewässerstruktur (Beschattung, Gewässerbett, Verengungen)"],
     "exposure_names": ["Vorkommen von Oberflächengewässer und Grundwasser", "Vorkommen von Abwasser- und Entwässerungssystemen", "Vorkommen von Infrastruktur an Binnengewässern"]},
    {"kwra_id": 13, "name": "Wassermangel im Boden",
     "cluster": "land", "kwra_field": "Boden", "stage": 1,
     "hazard_names": ["Hitze", "Trockenheit"],
     "upstream_names": ["Grundwasserstand"],
     "sensitivity_names": ["Bodeneigenschaften", "Topographie und Landnutzung", "Bewässerung"],
     "exposure_names": ["Vorkommen von Bodenart und Bodentyp", "Vorkommen von unversiegelter Fläche"]},
    {"kwra_id": 19, "name": "Produktionsfunktionen",
     "cluster": "land", "kwra_field": "Boden", "stage": 1,
     "hazard_names": [],
     "upstream_names": ["Bodenwasserhaushalt", "Bodenwärmehaushalt", "Bodenstoffhaushalt", "Bodenbiologie", "Bodenstruktur", "Erosion", "Gravitative Massenbewegungen", "Versalzung des Bodens, des Grundwassers und von Flussmündungen", "Nährstoffspeicherfunktionen (C, N, etc.)", "Filter- / Pufferfunktionen (Wasser, Schadstoffe, etc.)"],
     "sensitivity_names": ["Bodeneigenschaften", "Bodenbearbeitung", "Topographie und Landnutzung"],
     "exposure_names": ["Vorkommen von Bodenart und Bodentyp", "Vorkommen von unversiegelter Fläche"]},
    {"kwra_id": 21, "name": "Abiotischer Stress (Pflanzen)",
     "cluster": "land", "kwra_field": "Landwirtschaft", "stage": 1,
     "hazard_names": ["Hitze", "Früh- und Spätfröste", "Wechselfrost", "Hagel", "Starkwind", "Starkregen", "Trockenheit"],
     "upstream_names": ["Erosion", "Bodenwasserhaushalt", "Beeinträchtigung der Vitalität von Pflanzen"],
     "sensitivity_names": ["Anbaufrucht", "Dünger- und Pestizideinsatz", "Züchterischer Fortschritt", "Vorhandensein von Hagelschutz"],
     "exposure_names": ["Vorkommen von landwirtschaftlicher Nutzfläche", "Vorkommen von Anbauart", "Vorkommen von Tierhaltung", "Vorkommen von landwirtschaftlicher Infrastruktur"]},
    {"kwra_id": 25, "name": "Ertragsausfälle",
     "cluster": "land", "kwra_field": "Landwirtschaft", "stage": 1,
     "hazard_names": [],
     "upstream_names": ["Bodenwasserhaushalt", "Pflanzengesundheit", "Agrophänologie", "Bewässerungswasser", "Bodenfunktionen"],
     "sensitivity_names": [],
     "exposure_names": ["Vorkommen von landwirtschaftlicher Nutzfläche", "Vorkommen von Anbauart", "Vorkommen von Tierhaltung", "Vorkommen von landwirtschaftlicher Infrastruktur"]},
    {"kwra_id": 10, "name": "Bodenerosion durch Wasser",
     "cluster": "land", "kwra_field": "Boden", "stage": 1,
     "hazard_names": ["Nässe", "Starkregen", "Trockenheit"],
     "upstream_names": ["Rutschungen und Muren", "Hochwasser", "Sturzfluten"],
     "sensitivity_names": ["Bodenart und Bodentyp", "Topographie und Landnutzung"],
     "exposure_names": ["Vorkommen von Bodenart und Bodentyp", "Vorkommen von unversiegelter Fläche"]},
    {"kwra_id": 11, "name": "Bodenerosion durch Wind",
     "cluster": "land", "kwra_field": "Boden", "stage": 1,
     "hazard_names": ["Starkwind", "Trockenheit"],
     "upstream_names": [],
     "sensitivity_names": ["Bodenart und Bodentyp", "Topographie und Landnutzung"],
     "exposure_names": ["Vorkommen von Bodenart und Bodentyp", "Vorkommen von unversiegelter Fläche"]},
    {"kwra_id": 8, "name": "Schäden an Wäldern",
     "cluster": "land", "kwra_field": "Biologische Vielfalt", "stage": 2,
     "hazard_names": ["Durchschnittstemperatur"],
     "upstream_names": ["Beeinträchtigung der Vitalität von Pflanzen", "Beeinträchtigung der Vitalität von Tieren"],
     "sensitivity_names": ["Habitat-, Biotop-, Ökosystemeigenschaften", "Topographie und Landnutzung"],
     "exposure_names": ["Vorkommen von Arealen, Arten und Populationen", "Vorkommen von Biotopen, Habitaten und Ökosystemen"]},
    {"kwra_id": 27, "name": "Hitze- und Trockenstress",
     "cluster": "land", "kwra_field": "Wald- und Forstwirtschaft", "stage": 2,
     "hazard_names": ["Hitze", "Trockenheit"],
     "upstream_names": ["Bodenwasserhaushalt", "Beeinträchtigung der Vitalität von Pflanzen"],
     "sensitivity_names": ["Baumart", "Baumalter / Altersstruktur"],
     "exposure_names": ["Vorkommen von Waldfläche", "Vorkommen von Baumarten"]},
    {"kwra_id": 30, "name": "Waldbrandrisiko",
     "cluster": "land", "kwra_field": "Wald- und Forstwirtschaft", "stage": 2,
     "hazard_names": ["Trockenheit", "Hitze"],
     "upstream_names": [],
     "sensitivity_names": ["Baumart", "Baumalter / Altersstruktur"],
     "exposure_names": ["Vorkommen von Waldfläche", "Vorkommen von Baumarten"]},
    {"kwra_id": 28, "name": "Stress durch Schädlinge / Krankheiten",
     "cluster": "land", "kwra_field": "Wald- und Forstwirtschaft", "stage": 2,
     "hazard_names": ["Durchschnittstemperatur", "Starkregen", "Hitze", "Nässe", "Trockenheit", "Früh- und Spätfröste"],
     "upstream_names": ["Bodenwasserhaushalt", "Forstphänologische Phasen und Wachstumsperiode", "Beeinträchtigung der Vitalität von Pflanzen"],
     "sensitivity_names": ["Baumart", "Baumalter / Altersstruktur"],
     "exposure_names": ["Vorkommen von Waldfläche", "Vorkommen von Baumarten"]},
    {"kwra_id": 31, "name": "Nutzfunktion: Holzertrag",
     "cluster": "land", "kwra_field": "Wald- und Forstwirtschaft", "stage": 2,
     "hazard_names": ["CO2-Konzentration"],
     "upstream_names": ["Bodenwasserhaushalt", "Forstphänologische Phasen und Wachstumsperiode", "Vitalität / Mortalitätseffekte", "Baumartenzusammensetzung", "Schäden an Wäldern", "Areale, Arten und Populationen"],
     "sensitivity_names": ["Waldstruktur", "Standortbedingungen", "Topographie und Landnutzung", "Forstliche Bewirtschaftung"],
     "exposure_names": ["Vorkommen von Waldfläche", "Vorkommen von Baumarten"]},
    {"kwra_id": 7, "name": "Schäden an wassergebundenen Habitaten und Feuchtgebieten",
     "cluster": "land", "kwra_field": "Biologische Vielfalt", "stage": 2,
     "hazard_names": ["Trockenheit"],
     "upstream_names": ["Beeinträchtigung der Vitalität von Pflanzen", "Beeinträchtigung der Vitalität von Tieren", "Abfluss und Wasserstand von Oberflächengewässern", "Grundwasserstand"],
     "sensitivity_names": ["Habitat-, Biotop-, Ökosystemeigenschaften", "Topographie und Landnutzung"],
     "exposure_names": ["Vorkommen von Arealen, Arten und Populationen", "Vorkommen von Biotopen, Habitaten und Ökosystemen"]},
    {"kwra_id": 35, "name": "Verbreitung von Fischarten in Fließgewässern",
     "cluster": "wasser", "kwra_field": "Fischerei", "stage": 2,
     "hazard_names": [],
     "upstream_names": ["Gewässerzustand der Meere", "Gewässerzustand von Oberflächengewässern", "Abfluss und Wasserstand von Oberflächengewässern", "Strömungen und Gezeitendynamik", "Sturmfluten", "Beeinträchtigung der Vitalität von Tieren", "Fischgesundheit", "Areale, Arten und Populationen", "Phänologie und Verhalten", "Reproduktion, Wachstum und Sterblichkeit kommerziell genutzter Arten"],
     "sensitivity_names": ["Fischbestand", "Eigenschaften von Oberflächengewässern", "Meerwasserqualität und Küsteneigenschaften"],
     "exposure_names": ["Vorkommen von kommerziell relevanten Fischarten und -populationen", "Vorkommen von Aquakulturen", "Vorkommen von fischereiwirtschaftlicher Infrastruktur"]},
    {"kwra_id": 2, "name": "Ausbreitung invasiver Arten",
     "cluster": "land", "kwra_field": "Biologische Vielfalt", "stage": 2,
     "hazard_names": [],
     "upstream_names": ["Vegetation", "Tierwelt"],
     "sensitivity_names": ["Habitat-, Biotop-, Ökosystemeigenschaften", "Topographie und Landnutzung"],
     "exposure_names": ["Vorkommen von Arealen, Arten und Populationen", "Vorkommen von Biotopen, Habitaten und Ökosystemen"]},
    {"kwra_id": 39, "name": "Wasserqualität und Grundwasserversalzung",
     "cluster": "wasser", "kwra_field": "Küsten- und Meeresschutz", "stage": 2,
     "coastal": True,
     "hazard_names": ["CO2-Konzentration", "Durchschnittstemperatur", "Hitze", "Trockenheit", "Sonnenscheindauer", "Durchschnittliche Windgeschwindigkeit", "Starkwind"],
     "upstream_names": ["Sturmfluten", "Meeresspiegelhöhe", "Strömungen und Gezeitendynamik"],
     "sensitivity_names": ["Meerwasserqualität", "Stoffeintrag direkt ins Meer (Öl, Abwasser, etc.)", "Stoffeintrag über Oberflächengewässer"],
     "exposure_names": ["Vorkommen von Küsten, Wattenmeere, Ästuare", "Vorkommen von Meeren", "Vorkommen von Bauwerken und Infrastruktur in der Küstenzone"]},
    {"kwra_id": 44, "name": "Naturräumliche Veränderungen an Küsten",
     "cluster": "wasser", "kwra_field": "Küsten- und Meeresschutz", "stage": 2,
     "coastal": True,
     "hazard_names": [],
     "upstream_names": ["Sturmfluten", "Meeresspiegelhöhe", "Strömungen und Gezeitendynamik", "Gewässerzustand der Meere"],
     "sensitivity_names": ["Küstentopographie"],
     "exposure_names": ["Vorkommen von Küsten, Wattenmeere, Ästuare", "Vorkommen von Meeren", "Vorkommen von Bauwerken und Infrastruktur in der Küstenzone"]},
    {"kwra_id": 46, "name": "Beschädigung oder Zerstörung von Siedlung und Infrastruktur an der Küste",
     "cluster": "wasser", "kwra_field": "Küsten- und Meeresschutz", "stage": 2,
     "coastal": True,
     "hazard_names": ["Starkregen", "Starkwind"],
     "upstream_names": ["Höhere Belastung oder Versagen von Küstenschutzsystemen", "Meeresspiegelhöhe", "Strömungen und Gezeitendynamik", "Sturmfluten"],
     "sensitivity_names": ["Art und Zustand von Bauwerken und Küsteninfrastruktur"],
     "exposure_names": ["Vorkommen von Küsten, Wattenmeere, Ästuare", "Vorkommen von Meeren", "Vorkommen von Bauwerken und Infrastruktur in der Küstenzone"]},
    {"kwra_id": 71, "name": "Schiffbarkeit der Binnenschifffahrtsstraßen (Niedrigwasser)",
     "cluster": "infrastruktur", "kwra_field": "Verkehr, Verkehrsinfrastruktur", "stage": 2,
     "hazard_names": [],
     "upstream_names": ["Niedrigwasser", "Oberflächengewässer: Eisbedeckung", "Schäden an Binnenwasserstraßen, Häfen und maritimen Einrichtungen"],
     "sensitivity_names": ["Flussgebietseigenschaften", "Anthropogene Beeinflussung von Binnenwasserstraßen (z.B. Stauung, Einleitungen)"],
     "exposure_names": ["Vorkommen von Verkehrsteilnehmern", "Vorkommen von Verkehrsmitteln", "Vorkommen von Verkehrsinfrastrukturen"]},
    {"kwra_id": 82, "name": "Beeinträchtigung des Warenverkehrs über Wasserstraßen (Inland)",
     "cluster": "wirtschaft", "kwra_field": "Industrie und Gewerbe", "stage": 2,
     "hazard_names": [],
     "upstream_names": ["Schiffbarkeit der Wasserstraßen"],
     "sensitivity_names": ["Bauliche, organisatorische und finanzielle Vorsorge der Unternehmen", "Größe des Unternehmens / Anzahl und Größe der Standorte", "Abhängigkeit von Just-in-Time-Logistik"],
     "exposure_names": ["Vorkommen von Unternehmen und Betriebsstätten", "Vorkommen von betrieblichen Infrastrukturen"]},
    {"kwra_id": 74, "name": "Schäden / Hindernisse bei Straßen und Schienenwegen (Hochwasser)",
     "cluster": "infrastruktur", "kwra_field": "Verkehr, Verkehrsinfrastruktur", "stage": 3,
     "hazard_names": ["Starkregen", "Starkwind", "Hitze", "Kälte / Frost", "Wechselfrost"],
     "upstream_names": ["Hochwasser", "Sturzfluten", "Meeresspiegelhöhe", "Sturmfluten", "Grundwasserstand", "Schäden an Gebäuden und Infrastrukturen"],
     "sensitivity_names": ["Bauliche und organisatorische Vorsorge an Infrastrukturen", "Zustand von Infrastrukturen", "Verwendete Baumaterialien / Gestaltung", "Begrünung von Infrastrukturen"],
     "exposure_names": ["Vorkommen von Verkehrsteilnehmern", "Vorkommen von Verkehrsmitteln", "Vorkommen von Verkehrsinfrastrukturen"]},
    {"kwra_id": 75, "name": "Schäden / Hindernisse bei Straßen und Schienenwegen (Gravitative Massenbewegungen)",
     "cluster": "infrastruktur", "kwra_field": "Verkehr, Verkehrsinfrastruktur", "stage": 3,
     "hazard_names": ["Starkregen", "Starkwind"],
     "upstream_names": ["Gravitative Massenbewegungen", "Schäden durch Windwurf", "Schäden an Gebäuden und Infrastrukturen"],
     "sensitivity_names": ["Bauliche und organisatorische Vorsorge an Infrastrukturen", "Zustand von Infrastrukturen", "Verwendete Baumaterialien / Gestaltung", "Begrünung von Infrastrukturen"],
     "exposure_names": ["Vorkommen von Verkehrsteilnehmern", "Vorkommen von Verkehrsmitteln", "Vorkommen von Verkehrsinfrastrukturen"]},
    {"kwra_id": 76, "name": "Schäden an Verkehrsleitsystemen, Oberleitungen und Stromversorgungsanlagen",
     "cluster": "infrastruktur", "kwra_field": "Verkehr, Verkehrsinfrastruktur", "stage": 3,
     "hazard_names": ["Hagel", "Blitz", "Kälte / Frost", "Schnee- und Eisdruck", "Starkregen", "Starkwind"],
     "upstream_names": ["Meeresspiegelhöhe", "Sturmfluten", "Hochwasser", "Sturzfluten", "Gravitative Massenbewegungen"],
     "sensitivity_names": ["Bauliche und organisatorische Vorsorge an Infrastrukturen", "Zustand von Infrastrukturen", "Verwendete Baumaterialien / Gestaltung", "Begrünung von Infrastrukturen"],
     "exposure_names": ["Vorkommen von Verkehrsteilnehmern", "Vorkommen von Verkehrsmitteln", "Vorkommen von Verkehrsinfrastrukturen"]},
    {"kwra_id": 59, "name": "Schäden an Gebäuden aufgrund von Starkregen",
     "cluster": "infrastruktur", "kwra_field": "Bauwesen", "stage": 3,
     "hazard_names": ["Hagel", "Starkregen", "Starkwind", "Schnee- und Eisdruck", "Hitze", "Kälte / Frost"],
     "upstream_names": ["Abfluss und Wasserstand von Oberflächengewässern", "Gravitative Massenbewegungen", "Grundwasserstand", "Einschränkungen der Funktionsfähigkeit von Kanalnetzen und Vorflutern"],
     "sensitivity_names": ["Zustand von Gebäuden und Infrastrukturen", "Verwendete Baumaterialien auf Gebäudeebene", "Bauliche, organisatorische und finanzielle Vorsorge der Eigentümer und Nutzer", "Zustand von (Schutz-)Infrastrukturen", "Investitionen der Bau- und Immobilienwirtschaft in exponierten Gebieten"],
     "exposure_names": ["Vorkommen von Bau- und Immobilienunternehmen", "Vorkommen von Gebäuden", "Vorkommen von Siedlungsinfrastrukturen"]},
    {"kwra_id": 52, "name": "Einschränkungen der Funktionsfähigkeit von Kanalnetzen und Vorflutern und Kläranlagen",
     "cluster": "wasser", "kwra_field": "Wasserhaushalt, Wasserwirtschaft", "stage": 3,
     "hazard_names": [],
     "upstream_names": ["Abfluss und Wasserstand von Oberflächengewässern", "Gewässerzustand von Oberflächengewässern", "Grundwasser", "Wassernutzung"],
     "sensitivity_names": ["Art und Zustand der Entwässerungssysteme (Kläranlagen, Kanalisationsnetz)"],
     "exposure_names": ["Vorkommen von Oberflächengewässer und Grundwasser", "Vorkommen von Abwasser- und Entwässerungssystemen", "Vorkommen von Infrastruktur an Binnengewässern"]},
    {"kwra_id": 54, "name": "Chemische Wasserqualität",
     "cluster": "wasser", "kwra_field": "Wasserhaushalt, Wasserwirtschaft", "stage": 3,
     "hazard_names": ["Durchschnittstemperatur", "Trockenheit", "Starkregen", "Hitze", "Sonnenscheindauer"],
     "upstream_names": ["Mittlerer Abfluss"],
     "sensitivity_names": ["Stoffeintrag aus Landwirtschaft und Industrie (Stickstoff, Phosphor, Pestizide)"],
     "exposure_names": ["Vorkommen von Oberflächengewässer und Grundwasser", "Vorkommen von Abwasser- und Entwässerungssystemen", "Vorkommen von Infrastruktur an Binnengewässern"]},
    {"kwra_id": 85, "name": "Wasserbedarf",
     "cluster": "wirtschaft", "kwra_field": "Industrie und Gewerbe", "stage": 3,
     "hazard_names": ["Durchschnittstemperatur", "Hitze", "Durchschnittlicher Niederschlag", "Trockenheit", "Luftfeuchtigkeit"],
     "upstream_names": ["Wassernutzung", "Schäden an gewerblicher und industrieller Infrastruktur"],
     "sensitivity_names": ["Bauliche, organisatorische und finanzielle Vorsorge der Unternehmen", "Größe des Unternehmens / Anzahl und Größe der Standorte", "Wasser-, Energie- und Rohstoffintensität der Produktion"],
     "exposure_names": ["Vorkommen von Unternehmen und Betriebsstätten", "Vorkommen von betrieblichen Infrastrukturen"]},
    {"kwra_id": 78, "name": "Beeinträchtigung der Versorgung mit Rohstoffen und Zwischenprodukten (international)",
     "cluster": "wirtschaft", "kwra_field": "Industrie und Gewerbe", "stage": 3,
     "hazard_names": ["Globales Klima"],
     "upstream_names": ["Ertrag und Qualität der Ernteprodukte", "Leistung von Viehhaltung, Milchwirtschaft", "Güter und Dienstleistungen des Waldes", "Fangbedingungen und Fangmengen", "Schäden an gewerblicher und industrieller Infrastruktur", "Beeinträchtigung des landgestützten Warenverkehrs", "Beeinträchtigung des Warenverkehrs über Wasserstraßen"],
     "sensitivity_names": ["Bauliche, organisatorische und finanzielle Vorsorge der Unternehmen", "Größe des Unternehmens / Anzahl und Größe der Standorte", "Abhängigkeit von (einzelnen) Zulieferern", "Länge der Wertschöpfungsketten"],
     "exposure_names": ["Vorkommen von Unternehmen und Betriebsstätten", "Vorkommen von betrieblichen Infrastrukturen"]},
    {"kwra_id": 87, "name": "Leistungseinbußen von Beschäftigten",
     "cluster": "wirtschaft", "kwra_field": "Industrie und Gewerbe", "stage": 3,
     "hazard_names": [],
     "upstream_names": ["Hitzebelastung", "Hoher Krankenstand / Belastung der Rettungsdienste, Krankenhäuser und Ärzte"],
     "sensitivity_names": ["Bauliche, organisatorische und finanzielle Vorsorge der Unternehmen", "Arbeitsbedingungen der Beschäftigten (z.B. Anzahl der Außeneinsätze)"],
     "exposure_names": ["Vorkommen von Unternehmen und Betriebsstätten", "Vorkommen von betrieblichen Infrastrukturen"]},
    {"kwra_id": 100, "name": "Atembeschwerden (aufgrund von Luftverunreinigungen)",
     "cluster": "gesundheit", "kwra_field": "Menschliche Gesundheit", "stage": 3,
     "hazard_names": [],
     "upstream_names": ["Bodennahes Ozon", "Luftqualität (Smog)"],
     "sensitivity_names": ["Individueller Gesundheitszustand", "Individuelles Gefahrenbewusstsein", "Monitoring von Gesundheitsgefahren und Frühwarnsysteme"],
     "exposure_names": ["Vorkommen von Bevölkerung", "Vorkommen von Gesundheitsinfrastruktur"]},
    {"kwra_id": 102, "name": "Auswirkungen auf das Gesundheitssystem",
     "cluster": "gesundheit", "kwra_field": "Menschliche Gesundheit", "stage": 3,
     "hazard_names": [],
     "upstream_names": ["Hitze- und kälteabhängige Erkrankungen oder Mortalitäten", "Vektorübertragene Krankheiten", "Gesundheitliche Auswirkungen von UV-Strahlung", "Gesundheitliche Auswirkungen von aerogenen Stoffen", "Gesundheitliche Auswirkungen verminderter Bade- und Trinkwasserqualität und Lebensmittelsicherheit", "Unfallfolgen"],
     "sensitivity_names": ["Ausstattung der Rettungs- und Krankendienste", "Innovationen im medizinischen Bereich (Impfstoffe, Behandlungsmöglichkeiten)", "Typ und Zustand der Gesundheitsinfrastruktur"],
     "exposure_names": ["Vorkommen von Bevölkerung", "Vorkommen von Gesundheitsinfrastruktur"]},
    {"kwra_id": 3, "name": "Verlust an genetischer Vielfalt",
     "cluster": "land", "kwra_field": "Biologische Vielfalt", "stage": 4,
     "hazard_names": [],
     "upstream_names": ["Beeinträchtigung der Vitalität von Pflanzen", "Beeinträchtigung der Vitalität von Tieren"],
     "sensitivity_names": ["Habitat-, Biotop-, Ökosystemeigenschaften"],
     "exposure_names": ["Vorkommen von Arealen, Arten und Populationen", "Vorkommen von Biotopen, Habitaten und Ökosystemen"]},
    {"kwra_id": 4, "name": "Verschiebung von Arealen und Rückgang der Bestände",
     "cluster": "land", "kwra_field": "Biologische Vielfalt", "stage": 4,
     "hazard_names": ["Durchschnittstemperatur", "Durchschnittlicher Niederschlag"],
     "upstream_names": ["Beeinträchtigung der Vitalität von Pflanzen", "Beeinträchtigung der Vitalität von Tieren", "Verschiebung von Arealen", "Ausbreitung invasiver Arten"],
     "sensitivity_names": ["Habitat-, Biotop-, Ökosystemeigenschaften", "Topographie und Landnutzung"],
     "exposure_names": ["Vorkommen von Arealen, Arten und Populationen", "Vorkommen von Biotopen, Habitaten und Ökosystemen"]},
    {"kwra_id": 5, "name": "Schäden an Küstenökosystemen",
     "cluster": "land", "kwra_field": "Biologische Vielfalt", "stage": 4,
     "coastal": True,
     "hazard_names": [],
     "upstream_names": ["Naturräumliche Schäden an Küsten"],
     "sensitivity_names": ["Habitat-, Biotop-, Ökosystemeigenschaften", "Topographie und Landnutzung"],
     "exposure_names": ["Vorkommen von Arealen, Arten und Populationen", "Vorkommen von Biotopen, Habitaten und Ökosystemen"]},
    {"kwra_id": 9, "name": "Ökosystemleistungen",
     "cluster": "land", "kwra_field": "Biologische Vielfalt", "stage": 4,
     "hazard_names": [],
     "upstream_names": ["Areale, Arten und Populationen", "Biotope, Habitate, Ökosysteme"],
     "sensitivity_names": ["Habitat-, Biotop-, Ökosystemeigenschaften", "Topographie und Landnutzung"],
     "exposure_names": ["Vorkommen von Arealen, Arten und Populationen", "Vorkommen von Biotopen, Habitaten und Ökosystemen"]},
    {"kwra_id": 12, "name": "Rutschungen und Muren",
     "cluster": "land", "kwra_field": "Boden", "stage": 4,
     "hazard_names": ["Starkregen", "Nässe"],
     "upstream_names": [],
     "sensitivity_names": ["Topographie und Landnutzung", "Boden- und Gesteinsschichtung"],
     "exposure_names": ["Vorkommen von Bodenart und Bodentyp", "Vorkommen von unversiegelter Fläche"]},
    {"kwra_id": 29, "name": "Schäden durch Windwurf",
     "cluster": "land", "kwra_field": "Wald- und Forstwirtschaft", "stage": 4,
     "hazard_names": ["Starkwind", "Trockenheit"],
     "upstream_names": ["Beeinträchtigung der Vitalität von Pflanzen"],
     "sensitivity_names": ["Baumhöhe"],
     "exposure_names": ["Vorkommen von Waldfläche", "Vorkommen von Baumarten"]},
    {"kwra_id": 32, "name": "Nutzfunktion: Erholung",
     "cluster": "land", "kwra_field": "Wald- und Forstwirtschaft", "stage": 4,
     "hazard_names": ["CO2-Konzentration"],
     "upstream_names": ["Bodenwasserhaushalt", "Forstphänologische Phasen und Wachstumsperiode", "Vitalität / Mortalitätseffekte", "Baumartenzusammensetzung", "Schäden an Wäldern", "Areale, Arten und Populationen"],
     "sensitivity_names": ["Waldstruktur", "Standortbedingungen", "Topographie und Landnutzung", "Forstliche Bewirtschaftung"],
     "exposure_names": ["Vorkommen von Waldfläche", "Vorkommen von Baumarten"]},
    {"kwra_id": 45, "name": "Höhere Belastung oder Versagen von Küstenschutzsystemen",
     "cluster": "wasser", "kwra_field": "Küsten- und Meeresschutz", "stage": 4,
     "coastal": True,
     "hazard_names": ["Starkregen", "Starkwind"],
     "upstream_names": ["Meeresspiegelhöhe", "Strömungen und Gezeitendynamik", "Sturmfluten"],
     "sensitivity_names": ["Art und Zustand von Deichen und anderer Schutzinfrastruktur"],
     "exposure_names": ["Vorkommen von Küsten, Wattenmeere, Ästuare", "Vorkommen von Meeren", "Vorkommen von Bauwerken und Infrastruktur in der Küstenzone"]},
    {"kwra_id": 56, "name": "Mangel an Bewässerungswasser",
     "cluster": "wasser", "kwra_field": "Wasserhaushalt, Wasserwirtschaft", "stage": 4,
     "hazard_names": [],
     "upstream_names": ["Grundwasser", "Gewässerzustand von Oberflächengewässern"],
     "sensitivity_names": [],
     "exposure_names": ["Vorkommen von Oberflächengewässer und Grundwasser", "Vorkommen von Abwasser- und Entwässerungssystemen", "Vorkommen von Infrastruktur an Binnengewässern"]},
    {"kwra_id": 94, "name": "Wirtschaftliche Chancen und Risiken für die Tourismuswirtschaft",
     "cluster": "wirtschaft", "kwra_field": "Tourismuswirtschaft", "stage": 4,
     "hazard_names": [],
     "upstream_names": ["Touristische Nachfrage", "Kosten für Tourismusanbieter"],
     "sensitivity_names": ["Grad der Spezialisierung von Tourismusanbietern", "Standortgebundenheit", "Wetterabhängigkeit"],
     "exposure_names": ["Vorkommen von lokalen Tourismusanbietern", "Vorkommen von touristischen Infrastrukturen"]},
]

PLANNED_BY_KWRA_ID = {p["kwra_id"]: p for p in PLANNED_RISKS}


def planned_available_from(p: dict) -> str:
    """Öffentliches Verfügbarkeits-Label eines geplanten Risikos."""
    return STAGE_LABELS.get(int(p.get("stage", 5)), STAGE_LABELS[5])



# ── Monetarisierung der Risiken (Helfer) ─────────────────────────────────────────
# Kernprinzip (Product-Owner-Vorgabe): Der Gesamtschaden ist die SUMME der monetär
# bewerteten Einzelrisiken. JEDES Risiko fließt monetär ein; ein nicht-monetärer
# Outcome (Tote, Fälle, Stunden, ha, Arten, Index) wird über einen eigenständigen,
# editierbaren Kostensatz ``cost_per_outcome_eur`` (€ je Outcome-Einheit) bewertet.
# Ein Risiko bleibt NUR dann unmonetarisiert (Kostensatz 0 → trägt 0 € bei), wenn
# eine Monetarisierung eine Doppelzählung wäre (reine Screening-Index-Risiken); das
# ist im jeweiligen ``cost_source_detail`` begründet.

# Reine Screening-/Index-Risiken: Outcome IST der HxVxE-Index. Sie werden bewusst
# NICHT monetarisiert (Kostensatz 0), weil ihr Schaden bereits über die konkreten
# Mortalitäts-/Morbiditäts-/Schadens-/Ausfallrisiken erfasst ist – eine eigene
# €-Bewertung wäre eine Doppelzählung (siehe docs/MODELL_KRITIK.md §6).
INDEX_ONLY_RISK_CODES: frozenset[str] = frozenset(
    r["code"] for r in RISKS if r.get("outcome_unit") == "Index"
)


# Direkte Sektorschäden (Schicht B, §6.2): ihre Zell-Kosten bilden die Basis für den
# k_indirekt-Multiplikator (indirekte Folgekosten) und die Restaurierungs-Teilkennzahl.
DIRECT_SECTOR_RISK_CODES: frozenset[str] = frozenset({
    "EXPECTED_BUILDING_DAMAGE_EUR",
    "EXPECTED_TRANSPORT_DAMAGE_EUR",
    "EXPECTED_ENERGY_INFRA_DAMAGE_EUR",
    "EXPECTED_TELECOM_DAMAGE_EUR",
    "EXPECTED_WATER_WASTEWATER_DAMAGE_EUR",
    "EXPECTED_AGRICULTURAL_DAMAGE_EUR",
    "EXPECTED_SOIL_LOSS_DEGRADATION_EUR",
    "EXPECTED_ECOSYSTEM_SERVICE_LOSS",
    "EXPECTED_FISHERIES_ECONOMIC_LOSS_EUR",
    "EXPECTED_AQUACULTURE_DAMAGE_EUR",
})

# Folgekosten, die in den k_indirekt-Multiplikator konsolidiert werden (ihre eigene
# €-Bewertung wird 0 gesetzt, um die Doppelzählung aus MODELL_KRITIK §3.7 zu beenden).
CONSOLIDATED_INTO_INDIRECT_CODES: frozenset[str] = frozenset({
    "EXPECTED_SUPPLY_SHORTAGE_COSTS_EUR",
    "EXPECTED_LOCATION_DISADVANTAGE_EUR",
    "EXPECTED_DELAYED_DAMAGE_COSTS_EUR",
})

# Nicht additive Teilkennzahlen: eine Teilmenge bereits gezählter Schäden
# (Restaurierung = Anteil der direkten Sektorschäden). Werden ausgewiesen, aber NICHT
# in ``total_eur`` addiert (sonst Doppelzählung, §3.7).
NON_ADDITIVE_RISK_CODES: frozenset[str] = frozenset({
    "EXPECTED_RESTORATION_COSTS_EUR",
})


def risk_is_monetary(risk: dict) -> bool:
    """True, wenn der ref_value bereits in €/Jahr vorliegt (cost_dimension monetary)."""
    return risk.get("cost_dimension") == "monetary"


def risk_default_cost_per_outcome(risk: dict) -> float:
    """Default-Kostensatz (€ je Outcome-Einheit) eines nicht-monetären Risikos."""
    return float(risk.get("cost_per_outcome_eur") or 0.0)


def risk_contributes_to_total(risk: dict) -> bool:
    """True, wenn das Risiko einen €-Beitrag zur Gesamtschadenssumme liefert.

    Monetäre Risiken tragen immer bei; nicht-monetäre nur, wenn ein positiver
    Kostensatz hinterlegt ist. Reine Index-Risiken (Kostensatz 0) sind damit
    automatisch von der Summe ausgenommen (dokumentierte Vermeidung von
    Doppelzählung).
    """
    if risk["code"] in NON_ADDITIVE_RISK_CODES:
        return False   # Teilkennzahl (z. B. Restaurierung) – nicht in die Summe
    if risk_is_monetary(risk):
        return True
    return risk_default_cost_per_outcome(risk) > 0.0


def cost_unit_label(outcome_unit: str) -> str:
    """Einheit des Kostensatz-Parameters: „€ je <Outcome-Einheit ohne /Jahr>“."""
    base = (outcome_unit or "").replace("/Jahr", "").strip()
    if not base or base == "€":
        return "€"
    if base == "Index":
        return "€ je Index-Punkt"
    return f"€ je {base}"


# ── Risiko-Quellenanreicherung (source_detail + IEEE-Referenzen) ──────────────────
# Zentral gepflegte Herleitungstexte + Bibliografie-Verweise je Risiko, sodass der
# (i)-Tooltip an JEDEM Referenzwert erklärt, wie der Wert zustande kommt und worauf er
# sich stützt. Ableitung erfolgt anhand des ``source``-Labels; reine Modellannahmen und
# Index=Outcome-Risiken erhalten einen ehrlichen Erklärtext OHNE (erfundene) Quelle.

def _enrich_risk_sources() -> None:
    def eur(v: float) -> str:
        return f"{int(round(v)):,}".replace(",", ".") + " €"

    def scale_word(s: str) -> str:
        return {"pop": "der Bevölkerung", "area": "der betroffenen Fläche",
                "flat": "pauschal (mengenunabhängig)"}.get(s, s)

    # Belastbar dokumentierte Einzelrisiken mit maßgeschneidertem Herleitungstext.
    BESPOKE: dict[str, tuple[str, list[str]]] = {
        "EXPECTED_ANNUAL_MORTALITY": (
            "Worst-Case-Anker 18/100.000 bei Index=100 ≈ 1,7× des bislang schlimmsten "
            "beobachteten Jahres (2018: ~8.700 Hitzetote ≈ 10,5/100.000; RKI-Methodik nach "
            "Winklmayr u. a. 2022, RKI-Sachstandsbericht Klimawandel & Gesundheit 2023). Die "
            "UBA-Klimawirkungs- und Risikoanalyse 2021 (Handlungsfeld Gesundheit) bestätigt die "
            "zunehmende Hitzemortalität. Eine typische Kommune mit P90-Index 20-40 ergibt "
            "3,6-7,2/100.000 (statistikkonform). Die monetäre Bewertung erfolgt über den "
            "separaten, editierbaren Kostensatz-Parameter „Kostensatz (Monetarisierung)“ "
            "– nicht mehr über diesen Referenzwert.",
            ["RKI_Hitzemortalitaet", "UBA_KWRA_2021"]),
        "EXPECTED_ANNUAL_MORTALITY_FLOOD": (
            "Anker aus der kuratierten nationalen Ereignisliste: 2021 Ahr/Erft 189, "
            "2002 Elbe 21, 2013 rund 4 Todesopfer — annualisiert über 1990–2024 rund "
            "6 Todesfälle/Jahr bundesweit (≈ 0,007/100.000). Der Referenzwert 0,6/100.000 "
            "beschreibt den Ereignisfall (Index = 100), nicht das Jahresmittel. WICHTIG: "
            "Die Verteilung ist extrem tail-lastig — allein 2021 trägt rund 80 % der "
            "Todesfälle des Zeitraums; ein Erwartungswert beschreibt hier keine typische "
            "Jahreslage. Nicht zu verwechseln mit der DLRG-Ertrinkungsstatistik (~400/Jahr): "
            "Die betrifft nahezu ausschließlich Freizeitertrinken ohne Hochwasserbezug und "
            "würde die Flutmortalität um zwei Größenordnungen überschätzen.",
            ["CEDIM_Hochwasser_2021", "Jonkman_2008_LossOfLife", "Destatis_Todesursachen_23211"]),
        "EXPECTED_ANNUAL_MORTALITY_STORM": (
            "Anker aus der kuratierten Sturm-Ereignisliste: Kyrill 2007 mit 13 Todesopfern "
            "in Deutschland (europaweit 47), Friederike 2018 mit 8–10, Sabine 2020 mit "
            "wenigen. Größenordnung 5–15 in einem schweren Sturmjahr, annualisiert rund "
            "1/Jahr. Amtliche Gegenprobe: ICD-10 X37 (Opfer eines Sturms) in der "
            "Todesursachenstatistik.",
            ["DWD_Sturmereignisse", "Destatis_Todesursachen_23211"]),
        "EXPECTED_ANNUAL_INJURIES": (
            "NICHT-TÖDLICH Verletzte durch Hochwasser/Starkregen; die Todesfälle stehen im "
            "eigenen Kanal, damit nichts doppelt bewertet wird. Amtliche Bezugsgröße ist "
            "die ICD-10-Außenursache X38 (Opfer einer Überschwemmung) in der "
            "Krankenhausstatistik — in der deutschen Kodierpraxis als Nebendiagnose, "
            "weshalb die DRG-Nebendiagnosen-Tabelle (23141) und nicht die "
            "Hauptdiagnose-Tabelle die belastbare Quelle ist. Ein erheblicher Teil der "
            "Verletzungen entsteht erst bei den Aufräumarbeiten.",
            ["Destatis_Krankenhausdiagnosen_23131", "BBK_Hochwasserschutzfibel"]),
        "EXPECTED_ANNUAL_INJURIES_STORM": (
            "Nicht-tödlich Verletzte durch Stürme (ICD-10 X37 Sturm, X33 Blitzschlag). "
            "Das Verhältnis Verletzte je Todesfall ist bei Sturm hoch — viele Verletzte, "
            "wenige Tote — und schließt Verletzungen bei Dachreparaturen nach dem Ereignis "
            "ein. Bis Modellversion 6 war dieser Kanal mit Flut und Hangrutsch in EIN "
            "Risiko gefaltet, verknüpft über ein Maximum; das unterschätzte Kommunen, die "
            "mehreren Gefahren ausgesetzt sind, weil Verletzte aus verschiedenen Gefahren "
            "additiv und nicht alternativ auftreten.",
            ["Destatis_Krankenhausdiagnosen_23131", "DWD_Sturmereignisse"]),
        "EXPECTED_ANNUAL_INJURIES_LANDSLIDE": (
            "Nicht-tödlich Verletzte durch Hangrutschungen (ICD-10 X36). Außerhalb steilen "
            "Geländes liegt der Kanal nahe null — das ist ehrlich und informativ, kein "
            "Mangel. Zuvor Teil des zusammengefassten Verletzten-Risikos.",
            ["Destatis_Krankenhausdiagnosen_23131"]),
        "EXPECTED_BUILDING_DAMAGE_EUR": (
            "Nationale jährliche Gebäudeschäden (Hochwasser + Sturm/Hagel) ~3,5 Mrd €/a ÷ 832 "
            "(100.000-Einwohner-Einheiten in DE) ≈ 4,2 Mio €/100.000 → 4,5 Mio € bei Index=100. "
            "Größenordnung belegt durch Prognos/GWS/IÖW 2023 „Kosten durch Klimawandelfolgen in "
            "Deutschland“ (BMWK/BMUV): Ahrtal 2021 mit Anteil Bauwesen + Privathaushalte 20,9 "
            "von 40,5 Mrd €. Skaliert mit der Bevölkerung; editierbar.",
            ["Prognos_Klimaschaeden_2023"]),
        "EXPECTED_TRANSPORT_DAMAGE_EUR": (
            "Nationale jährliche Verkehrsinfrastruktur-Schäden ~1,5 Mrd €/a ÷ 832 ≈ 1,8 Mio "
            "€/100.000 bei Index=100. Größenordnung belegt durch Prognos/GWS/IÖW 2023 (BMWK/"
            "BMUV): Ahrtal 2021 mit Verkehrsanteil 6,8 von 40,5 Mrd € (~17 %). Skaliert mit "
            "der Bevölkerung; editierbar.",
            ["Prognos_Klimaschaeden_2023"]),
        "EXPECTED_AQUACULTURE_DAMAGE_EUR": (
            "Punktwert 200.000 € je ~50 km² Gewässerfläche bei Index=100 (Aquakultur ist in "
            "DE sehr klein). Für diese Einzelposition liegt keine belastbare Prognos-Zahl vor "
            "⇒ editierbare Modellannahme (nur Größenordnung), ohne eigene Quelle.",
            []),
    }

    for r in RISKS:
        if r.get("source_detail"):
            continue
        code, src = r["code"], r.get("source", "")
        rv = r.get("ref_value", 0.0)
        unit = r.get("outcome_unit", "")
        cost = r.get("cost_per_outcome_eur")
        if code in BESPOKE:
            detail, refs = BESPOKE[code]
        elif "UBA MK3.1" in src:  # Gesundheits-Outcomes (Kostensatz aus UBA-Methodenkonvention)
            detail = (
                f"Punktwert {rv:g} {unit} je Referenzkommune (100.000 Ew.) bei Index=100. Der "
                f"zugehörige Kostensatz ({eur(cost)}/Fall) ist an den Gesundheits-Kostensätzen "
                "der UBA-Methodenkonvention 3.1 (2020) orientiert. Für die Fallzahl selbst liegt "
                "keine belastbare nationale Pro-Kopf-Statistik vor ⇒ editierbare Modellannahme "
                "mit UBA MK3.1 als Kostensatz-Anker.")
            refs = ["UBA_Methodenkonvention_MK3.1"]
        elif "Belastungsstunden" in src:  # reine Belastungsindikatoren ohne Kostensatz
            detail = (
                f"Reiner Belastungsindikator ohne monetären Kostensatz (cost_per_outcome_eur=0). "
                f"Punktwert {rv:g} {unit} je Referenzkommune bei Index=100 als editierbare "
                "Modellannahme; keine belastbare Messreihe hinterlegt (unbelegt).")
            refs = []
        elif src.startswith("Prognos"):  # monetäre Schadens-/Verlustrisiken
            detail = (
                f"Schadensanker {eur(rv)} je Referenzeinheit bei Index=100. Die Größenordnung "
                "ist der Studie Prognos/GWS/IÖW 2023 „Kosten durch Klimawandelfolgen in "
                "Deutschland“ (BMWK/BMUV) entnommen, die die nationalen Schäden extremer "
                "Wetterereignisse (u. a. Dürre-/Hitzesommer 2018/2019, Flut 2021) systematisiert "
                f"und für Sektoren modelliert. Skaliert mit {scale_word(r.get('scale',''))}; "
                "editierbar.")
            refs = ["Prognos_Klimaschaeden_2023"]
        elif "BBK KRITIS" in src:  # KRITIS-Ausfallzeiten
            detail = (
                f"Ausfall-/Störungsanker {rv:g} {unit} je Referenzkommune bei Index=100. Mangels "
                "kommunaler Ausfallstatistik ist der Wert eine editierbare Modellannahme; "
                "Größenordnung und Systemabgrenzung sind an den KRITIS-Betrachtungen des BBK "
                "(Bundesamt für Bevölkerungsschutz und Katastrophenhilfe) angelehnt.")
            refs = ["BBK_KRITIS"]
        elif "Index=Outcome" in src:  # normierter Index IST der Outcome
            detail = (
                f"Index-Risiko: Der normierte Risiko-Index IST hier der Outcome (ref_value=100 "
                "per Konstruktion). Das ist eine bewusste, dokumentierte und editierbare "
                "Modellwahl (kein extern belegter Absolutkennwert); die inhaltliche "
                "Belastbarkeit stammt aus den zugrunde liegenden H/E/V-Komponenten.")
            refs = []
        elif "BfN" in src:  # ökologische Flächenrisiken
            detail = (
                f"Punktwert {rv:g} {unit} je Referenzkommune (Flächenbezug) bei Index=100 als "
                "editierbare Modellannahme. Ein belastbarer nationaler Pro-Fläche-Kennwert fehlt; "
                "die Größenordnung ist qualitativ am UBA-KWRA-2021-Handlungsfeld Biologische "
                "Vielfalt/Boden sowie an BfN-Befunden orientiert.")
            refs = ["UBA_KWRA_2021"]
        else:
            continue
        r["source_detail"] = detail
        if refs:
            r["source_refs"] = refs


_enrich_risk_sources()


# ── Monetarisierungs-Kostensätze je Risiko (Quellen + Herleitung) ─────────────────
# Setzt für JEDES nicht-monetäre Risiko den Kostensatz ``cost_per_outcome_eur`` (€ je
# Outcome-Einheit) samt ``cost_source``/``cost_source_detail``/``cost_source_refs`` für
# den eigenständigen Registry-Parameter „Kostensatz (Monetarisierung)“. Damit fließt
# jedes Risiko monetär in den Gesamtschaden ein. Reine Screening-Index-Risiken bleiben
# bewusst bei 0 € (Vermeidung von Doppelzählung – im Detailtext begründet).
# Quellenprimat: OECD-VSL (Mortalität), UBA-Methodenkonvention 3.1 (Gesundheit/Umwelt),
# EWI-VoLL 2015 (Energie-/Ausfallkosten), BBK-KRITIS (Ausfallzeiten), Prognos 2023
# (indirekte/verkehrliche Folgen), TEEB-DE/BfN (Ökosystem-/Flächenwerte).

# CODE -> (Kostensatz €/Outcome, Kurz-Quelle, Referenz-Keys, Herleitungstext).
_RISK_COST_RATES: dict[str, tuple[float, str, list[str], str]] = {
    # ── Gesundheit: Personenschäden (Kostensatz je Fall/Person) ──
    "EXPECTED_ANNUAL_MORTALITY": (
        160_800.0, "UBA MK 4.0 / Amann 2020a (VOLY, €2024)",
        ["UBA_MK40_Amann_2020_VOLY"],
        "Sterblichkeit wird nach der UBA-Methodenkonvention 4.0 bewertet: verlorene "
        "Lebensjahre (YLL) × Wert eines Lebensjahres (VOLY) 160.800 €₂₀₂₄. Herleitung "
        "(Bericht #95 §3.5): Amann 2020a Tab. 3.15: 79.500 €₂₀₀₅ × VPI 2005→2024 "
        "1,4638 × Kaufkraft-Raumtransfer EU27→DE 1,1792 × Einkommensentwicklung^0,85 "
        "1,1719; Band 136.400–165.600 €. Preisstand 2024. Das bewertet altersgerecht — "
        "ein Sterbefall mit 6 verbleibenden Lebensjahren zählt anders als einer mit 40 — "
        "und fällt bei altenlastigen Risiken (Hitze) rund Faktor 5 vorsichtiger aus als "
        "der pauschale VSL (Sensitivität: VSL 6,19 Mio €₂₀₂₄ MK-konsistent, ÷ VOLY = "
        "38,5 Lebensjahre ✓; EU-Referenz 4,7 Mio €). Ersetzt den früheren VSL-Punktwert "
        "3,5 Mio €/Todesfall (Rev.-7-Integration; Ledger-Befund 76)."),
    "EXPECTED_ANNUAL_MORBIDITY": (
        7_152.0, "Destatis Kostennachweis 2023 (indexiert €2024)",
        ["Destatis_Kostennachweis_2023"],
        "Behandlungskostensatz je hitzeassoziiertem Krankenhausfall: 6.996 €₂₀₂₃ "
        "(bereinigte Kosten je Behandlungsfall, Kostennachweis der Krankenhäuser 2023) "
        "× VPI 119,3/116,7 = 7.152 €₂₀₂₄ (Bericht #95 §3.5). PROXY: Durchschnitt aller "
        "Krankenhausfälle — hitzeassoziierte Fälle haben einen anderen Fallmix; "
        "DRG-basierte Sätze als benannte Sensitivität. Abgrenzung (§8/B4): erfasst die "
        "KLINISCHEN Fälle; die subklinische Produktivitätslast thermischer/Schadstoff-"
        "Belastung ist getrennt über die Belastungsstunden-Risiken bewertet — keine "
        "Doppelzählung."),
    "EXPECTED_ANNUAL_INJURIES": (
        12_000.0, "UBA MK3.1 2020", ["UBA_Methodenkonvention_MK3.1"],
        "12.000 € je Verletztem (Behandlung, Reha, temporärer Erwerbsausfall) als "
        "editierbarer Punktwert; Größenordnung an den Gesundheits-/Unfallkostensätzen der "
        "UBA-Methodenkonvention 3.1 orientiert. Zählt ausschließlich NICHT-TÖDLICH "
        "Verletzte — die Todesfälle sind über eigene Risiken mit dem VSL bewertet."),
    "EXPECTED_ANNUAL_INJURIES_STORM": (
        12_000.0, "UBA MK3.1 2020", ["UBA_Methodenkonvention_MK3.1"],
        "Wie Verletzte (Flut): 12.000 € je nicht-tödlich Verletztem."),
    "EXPECTED_ANNUAL_INJURIES_LANDSLIDE": (
        12_000.0, "UBA MK3.1 2020", ["UBA_Methodenkonvention_MK3.1"],
        "Wie Verletzte (Flut): 12.000 € je nicht-tödlich Verletztem."),
    "EXPECTED_ANNUAL_MORTALITY_FLOOD": (
        3_500_000.0, "OECD 2012 (VSL)", ["OECD_VSL_2012", "Jonkman_2008_LossOfLife"],
        "VSL-Punktwert 3,5 Mio € wie bei der Hitzemortalität. Dokumentierte Folge dieser "
        "Wahl: Ein einheitlicher VSL bewertet einen Fluttod und einen Hitzetod gleich, "
        "obwohl Hitzetote weit überwiegend im Band 85+ mit kurzer Restlebenserwartung "
        "auftreten und Flutopfer ein breites Altersspektrum treffen. Nach Lebensjahren "
        "gerechnet wäre ein Fluttod ein Vielfaches wert — die Wahl verschiebt damit das "
        "€-Ranking zwischen Anpassungsmaßnahmen und ist bewusst so getroffen."),
    "EXPECTED_ANNUAL_MORTALITY_STORM": (
        3_500_000.0, "OECD 2012 (VSL)", ["OECD_VSL_2012", "DWD_Sturmereignisse"],
        "VSL-Punktwert 3,5 Mio € wie bei der Hitzemortalität (gleiche Einschränkung zur "
        "Altersstruktur wie bei der Flut-Mortalität)."),
    "EXPECTED_ANNUAL_MENTAL_HEALTH": (
        4_000.0, "UBA MK3.1 2020", ["UBA_Methodenkonvention_MK3.1"],
        "4.000 € je psychischem Belastungsfall (Diagnostik, Therapie, Ausfallzeiten) als "
        "editierbarer Punktwert, an den Gesundheits-Kostensätzen der UBA-Methoden"
        "konvention 3.1 orientiert. Keine belastbare Einzelstatistik ⇒ Modellannahme."),
    "EXPECTED_ANNUAL_AFFECTED_EVACUATED": (
        2_500.0, "UBA MK3.1 / BBK", ["UBA_Methodenkonvention_MK3.1", "BBK_KRITIS"],
        "2.500 € je betroffener/evakuierter Person (Notunterbringung, Versorgung, "
        "Einsatz-/Betreuungskosten) als editierbarer Punktwert; Größenordnung an "
        "UBA MK3.1 und BBK-Bevölkerungsschutz-Kennzahlen orientiert."),
    "EXPECTED_THERMAL_STRESS_HOURS": (
        400.0, "UBA MK3.1 2020 (Modellannahme)", ["UBA_Methodenkonvention_MK3.1"],
        "400 € je aggregierter Belastungsstunde als editierbare Modellannahme — bewusst nur "
        "der ARBEITSPRODUKTIVITÄTS-/Komfortverlust thermischer Belastung, an den "
        "Produktivitätskosten-Ansätzen der UBA-Methodenkonvention 3.1 orientiert. Abgrenzung "
        "gegen Doppelzählung (§8/B4): Der klinische Behandlungs-/Krankheitsanteil ist im "
        "Risiko „Erwartete Morbidität (Hitze)“ (Kostensatz je Fall) erfasst und hier "
        "ausgeklammert — Belastungsstunden zählen nur die subklinische Produktivitätslast."),
    "EXPECTED_POLLUTANT_EXPOSURE_HOURS": (
        300.0, "UBA MK3.1 2020 (Modellannahme)", ["UBA_Methodenkonvention_MK3.1"],
        "300 € je aggregierter Schadstoff-Expositionsstunde als editierbare Modellannahme — "
        "bewusst nur der Produktivitäts-/Komfortverlust, an UBA-MK3.1-Luftschadstoff-"
        "Kostensätzen orientiert. Abgrenzung gegen Doppelzählung (§8/B4): Der klinische "
        "Anteil (Atemwegs-/Herz-Kreislauf-Behandlung) ist über die Morbidität erfasst und "
        "hier ausgeklammert."),
    # ── Operativ: Ausfallstunden (Kostensatz je Ausfallstunde, aggregiert) ──
    "EXPECTED_CI_OUTAGE_HOURS": (
        40_000.0, "BBK KRITIS / EWI-VoLL 2015", ["BBK_KRITIS", "EWI_VoLL_2015"],
        "40.000 € je aggregierter Ausfallstunde kritischer Infrastruktur (gemischtes "
        "Sektorportfolio) als editierbare Modellannahme; hergeleitet als konservativer "
        "Bruchteil des EWI-VoLL (nationale Stromausfallkosten ~430 Mio €/h) auf "
        "Kommunalebene, ergänzt um BBK-KRITIS-Systemabgrenzung. Bislang 0 € ⇒ jetzt bewertet."),
    "EXPECTED_ENERGY_OUTAGE_HOURS": (
        120_000.0, "EWI-VoLL 2015", ["EWI_VoLL_2015"],
        "120.000 € je Stromausfallstunde als editierbare Modellannahme, hergeleitet aus "
        "dem Value of Lost Load (EWI 2015: Haushalte ~11,92 €/kWh; nationale Ausfallkosten "
        "~430 Mio €/h) heruntergerechnet auf die Last einer ~100.000-Ew.-Kommune. "
        "Bislang 0 € ⇒ jetzt bewertet."),
    "EXPECTED_WATER_SUPPLY_OUTAGE_HOURS": (
        60_000.0, "BBK KRITIS (Modellannahme)", ["BBK_KRITIS"],
        "60.000 € je Ausfallstunde der Wasserversorgung (Ersatzversorgung, Gesundheits-/"
        "Betriebsfolgen) als editierbare Modellannahme, Systemabgrenzung an BBK-KRITIS "
        "angelehnt. Bislang 0 € ⇒ jetzt bewertet."),
    "EXPECTED_WASTEWATER_OUTAGE_HOURS": (
        25_000.0, "BBK KRITIS (Modellannahme)", ["BBK_KRITIS"],
        "25.000 € je Ausfallstunde der Abwasserentsorgung (Umwelt-/Hygienefolgen, "
        "Notbetrieb) als editierbare Modellannahme, an BBK-KRITIS angelehnt. "
        "Bislang 0 € ⇒ jetzt bewertet."),
    "EXPECTED_COMMUNICATION_OUTAGE_HOURS": (
        50_000.0, "BBK KRITIS (Modellannahme)", ["BBK_KRITIS"],
        "50.000 € je Ausfallstunde der Kommunikationsnetze (Wirtschafts-, Notruf- und "
        "Koordinationsfolgen) als editierbare Modellannahme, an BBK-KRITIS angelehnt. "
        "Bislang 0 € ⇒ jetzt bewertet."),
    "EXPECTED_TRANSPORT_DISRUPTION_HOURS": (
        30_000.0, "Prognos 2023 / BBK", ["Prognos_Klimaschaeden_2023", "BBK_KRITIS"],
        "30.000 € je Stunde Verkehrsunterbrechung (aggregierte Zeit-/Wertschöpfungskosten "
        "gestörter Personen- und Güterverkehre) als editierbare Modellannahme, "
        "Größenordnung an Prognos-2023-Folgekosten und BBK-KRITIS angelehnt. "
        "Bislang 0 € ⇒ jetzt bewertet."),
    "EXPECTED_SUPPLY_CHAIN_DISRUPTION_HOURS": (
        40_000.0, "Prognos 2023 (Modellannahme)", ["Prognos_Klimaschaeden_2023"],
        "40.000 € je Stunde Lieferkettenunterbrechung (Produktions-/Wertschöpfungsausfall) "
        "als editierbare Modellannahme, an den indirekten Wirtschaftsfolgen aus Prognos "
        "2023 orientiert. Bislang 0 € ⇒ jetzt bewertet."),
    "EXPECTED_ADMIN_OUTAGE_HOURS": (
        15_000.0, "BBK KRITIS (Modellannahme)", ["BBK_KRITIS"],
        "15.000 € je administrativer Ausfallstunde (verzögerte Verwaltungs-/Daseins"
        "vorsorge-Leistungen) als editierbare Modellannahme, an BBK-KRITIS angelehnt. "
        "Bislang 0 € ⇒ jetzt bewertet."),
    "EXPECTED_FUNCTIONAL_FAILURE_DURATION": (
        30_000.0, "BBK KRITIS (Modellannahme)", ["BBK_KRITIS"],
        "30.000 € je Stunde Funktionsausfall (kaskadierende System-/Versorgungsfolgen) als "
        "editierbare Modellannahme, an BBK-KRITIS-Kaskadenbetrachtungen angelehnt. "
        "Bislang 0 € ⇒ jetzt bewertet."),
    # ── Umwelt: physische Verluste (Kostensatz je Art / ha) ──
    "EXPECTED_BIODIVERSITY_LOSS": (
        500_000.0, "TEEB-DE / UBA KWRA 2021", ["TEEB_DE_Naturkapital", "UBA_KWRA_2021"],
        "500.000 € je verlorener Art (Wiederherstellungs-/Erhaltungsprogramm-Größenordnung) "
        "als editierbare Modellannahme, am Naturkapital-/Ökosystemleistungs-Bewertungsrahmen "
        "von TEEB-DE orientiert. Abgrenzung: bewertet den physischen Artverlust, nicht den "
        "laufenden Leistungsausfall (der über „Verlust von Ökosystemleistungen“ läuft) – "
        "keine Doppelzählung. Bislang 0 € ⇒ jetzt bewertet."),
    "EXPECTED_HABITAT_LOSS": (
        80_000.0, "TEEB-DE (Modellannahme)", ["TEEB_DE_Naturkapital"],
        "80.000 € je ha verlorenem Habitat (Renaturierungs-/Wiederherstellungskosten) als "
        "editierbare Modellannahme, an TEEB-DE-Bewertungen orientiert. Abgrenzung zum "
        "laufenden Ökosystemleistungs-Verlust (eigener monetärer Posten) im Sinne der "
        "Vermeidung von Doppelzählung. Bislang 0 € ⇒ jetzt bewertet."),
    "EXPECTED_SOIL_DEGRADATION": (
        10_000.0, "TEEB-DE / UBA MK3.1", ["TEEB_DE_Naturkapital", "UBA_Methodenkonvention_MK3.1"],
        "10.000 € je ha degradiertem Boden — bewusst nur der ÖKOLOGISCHE Bodenfunktionswert "
        "(Wasserhaushalt, Lebensraum, Kohlenstoffspeicher), an TEEB-DE/UBA MK3.1 orientiert. "
        "Abgrenzung gegen Doppelzählung (§8/B5): Der ökonomische Boden-/Ertragswert derselben "
        "Fläche ist über das monetäre Risiko „Bodenverluste / -degradation (€)“ "
        "(EXPECTED_SOIL_LOSS_DEGRADATION_EUR, Bodenwert je ha × Erosionsintensität) erfasst; "
        "dieses Umweltrisiko bewertet nur den davon getrennten Naturhaushaltsanteil. "
        "Editierbar."),
    "EXPECTED_VEGETATION_DAMAGE": (
        20_000.0, "TEEB-DE (Modellannahme)", ["TEEB_DE_Naturkapital"],
        "20.000 € je ha geschädigter Vegetation (Wiederbegrünungs-/Wiederherstellungs"
        "kosten) als editierbare Modellannahme, an TEEB-DE-Bewertungen orientiert. "
        "Bislang 0 € ⇒ jetzt bewertet."),
}

_INDEX_EXCLUSION_DETAIL = (
    "Bewusst NICHT monetarisiert (Kostensatz 0 €): Dieses Risiko ist ein reines "
    "Screening-Index-Risiko; sein Schadensgehalt ist bereits über die konkreten "
    "monetär bewerteten Risiken (Mortalität/Morbidität, Sektor-/Ausfall-/Flächen"
    "schäden) erfasst. Eine eigene €-Bewertung wäre eine Doppelzählung und ist "
    "deshalb aus der Gesamtschadenssumme ausgenommen (siehe docs/MODELL_KRITIK.md §6). "
    "Editierbar: Wird ein positiver Kostensatz gesetzt, fließt das Risiko additiv ein.")


def _enrich_risk_cost_sources() -> None:
    for r in RISKS:
        if risk_is_monetary(r):
            continue  # ref_value ist bereits €/Jahr → kein Kostensatz-Parameter
        code = r["code"]
        if code in _RISK_COST_RATES:
            rate, src, refs, detail = _RISK_COST_RATES[code]
            r["cost_per_outcome_eur"] = rate
            r["cost_source"] = src
            r["cost_source_detail"] = detail
            r["cost_source_refs"] = refs
        elif code in INDEX_ONLY_RISK_CODES:
            r["cost_per_outcome_eur"] = 0.0
            r["cost_source"] = "Bewusst nicht monetarisiert (Doppelzählung)"
            r["cost_source_detail"] = _INDEX_EXCLUSION_DETAIL
            r["cost_source_refs"] = ["UBA_KWRA_2021"]
        else:
            # Sicherheitsnetz: nicht-monetäres Risiko ohne Kostensatz-Eintrag.
            r.setdefault("cost_per_outcome_eur", 0.0)
            r["cost_source"] = r.get("cost_source") or "Modellannahme (Kostensatz, unbelegt)"
            r["cost_source_detail"] = r.get("cost_source_detail") or (
                "Für dieses Risiko ist noch kein belegter Kostensatz hinterlegt; "
                "Bewertung als editierbare Modellannahme.")


_enrich_risk_cost_sources()


# ── Quellenanreicherung Hazards/Expositionen/Sensitivitäten ──────────────────────
# Leitet je Indikator einen source_detail (Herkunft/Proxy + Bedeutung der Normierungs-
# skala) und – wo eine reale Datengrundlage im source-Label steckt – IEEE/Wayback-Verweise
# ab. Reine Annahme-/qualitative Werte bleiben ehrlich ohne Referenz. Bereits inline
# belegte Einträge (Kern-Hazards, Zensus) werden übersprungen.

def _enrich_hev_sources() -> None:
    # Schlüsselwort im source-Label -> (Bibliografie-Key, Anzeigename).
    KEYWORD_REFS: tuple[tuple[str, str, str], ...] = (
        ("OSM", "OSM_Data", "OpenStreetMap (ODbL)"),
        ("DWD", "DWD_CDC", "DWD Climate Data Center"),
        ("Copernicus", "Copernicus_C3S", "Copernicus C3S"),
        ("Sentinel", "Copernicus_C3S", "Copernicus C3S"),
        ("Zensus", "Zensus_2022", "Zensus 2022 (Destatis)"),
        ("INKAR", "BBSR_INKAR", "BBSR INKAR"),
        ("BBSR", "BBSR_INKAR", "BBSR INKAR"),
        ("UHI", "VDI3787_Stadtklima", "VDI 3787 Bl.1"),
        ("UBA", "UBA_KWRA_2021", "UBA KWRA 2021"),
    )

    for items in (HAZARDS, EXPOSURES, VULNERABILITIES):
        for m in items:
            if m.get("source_detail"):
                continue
            src = m.get("source", "")
            proxy = m.get("proxy", "").strip()
            unit = m.get("unit", "")
            nmin, nmax = m.get("norm_min", 0.0), m.get("norm_max", 0.0)

            refs: list[str] = []
            names: list[str] = []
            for kw, key, name in KEYWORD_REFS:
                if kw in src and key not in refs:
                    refs.append(key)
                    names.append(name)

            if refs:
                closing = f"Datengrundlage(n): {', '.join(names)}."
            else:
                closing = ("Mangels belastbarer Einzelquelle beruht der Wert auf einer "
                           "dokumentierten Modell-/Regionalannahme (unbelegt).")

            proxy_txt = f"Datengrundlage/Proxy: {proxy} " if proxy else ""
            if m.get("spatial", True):
                lead = f"Wert je 100-m-Zelle in {unit} (absolute Einheit). "
            else:
                lead = (f"Nicht räumlich aufgelöst: regionaler/nationaler Konstantwert "
                        f"in {unit}. ")
            scale_txt = (f"Die Referenzskala norm_min={nmin:g}…norm_max={nmax:g} {unit} dient "
                         "ausschließlich der Risiko-Normierung (0..1), nicht der Anzeige, und ist "
                         "eine dokumentierte, editierbare Modellwahl. ")
            m["source_detail"] = lead + proxy_txt + scale_txt + closing
            if refs:
                m["source_refs"] = refs


_enrich_hev_sources()


# ── Pathway-Gewichte (aus pathway_weight_defaults.csv) ──────────────────────────
# Gewichte sind eine transparente Modellwahl (Rangfolge primär > parallel > alternativ >
# compound), keine externe Quelle; degressiv gestaffelt nach Pfadtyp-Nähe zum Primärpfad.
# Quelle: Modellwahl (Pfadgewichtung, dokumentiert) — siehe REVIEW_WIRKUNGSMECHANISMEN.md §5.

PATHWAY_WEIGHT_SOURCE = "Modellwahl (Pfadgewichtung, dokumentiert)"

PATHWAY_WEIGHTS: dict[str, float] = {
    "primary": 1.0,
    "aligned": 0.85,
    "alternate_hazard": 0.75,
    "alternate_exposure": 0.70,
    "alternate_vulnerability": 0.70,
    "compound_he": 0.65,
    "compound_hv": 0.60,
    "compound_ev": 0.55,
    "compound_multi": 0.50,
}


def build_pathways(risk: dict) -> list[dict]:
    """Kuratierte Wirkungsketten eines Risikos (``pathway_curation.CURATED_PATHWAYS``).

    Jede Kette ist fachlich begründet und quellenbelegt (KWRA 2021 / GIZ Vulnerability
    Sourcebook); die frühere kartesische Erzeugung aus den H/E/V-Listen ist ersetzt
    (MODELL_KRITIK §3.5 — sinnlose Mischketten + pfadzahl-abhängige Verdünnung). Der
    Index ist das MAXIMUM der gewichteten Ketten (``risk_engine.cell_risk_indices``),
    nicht mehr der gewichtete Mittelwert.

    Gibt Liste von {hazard, exposure, vulnerability, pathway_type, weight, justification,
    justification_ref, cluster} zurück. Fällt für (theoretisch) unkuratierte Risiken auf
    die reine Primärkette H0×E0×V0 zurück, statt sinnlose Ketten zu erzeugen.
    """
    from app.data.pathway_curation import CURATED_PATHWAYS

    H = risk["hazards"]
    E = risk["exposures"]
    V = risk["vulnerabilities"]
    if not H or not E or not V:
        return []

    pw = PATHWAY_WEIGHTS
    spec = CURATED_PATHWAYS.get(risk["code"])
    if not spec:
        return [{
            "hazard": H[0], "exposure": E[0], "vulnerability": V[0],
            "pathway_type": "primary", "weight": pw["primary"],
            "justification": "Primärkette (keine Kuratierung hinterlegt).",
            "justification_ref": None, "cluster": None,
        }]

    cluster = spec.get("cluster")
    default_ref = spec.get("ref")
    paths: list[dict] = []
    for ch in spec["chains"]:
        h, e, v, ptype, note = ch[0], ch[1], ch[2], ch[3], ch[4]
        ref = ch[5] if len(ch) > 5 else default_ref
        paths.append({
            "hazard": h, "exposure": e, "vulnerability": v,
            "pathway_type": ptype, "weight": pw[ptype],
            "justification": note, "justification_ref": ref, "cluster": cluster,
        })
    return paths


# ── Maßnahmen ────────────────────────────────────────────────────────────────────
# effect_target: Liste aus {hazard, exposure, vulnerability} – worauf die Maßnahme wirkt.
# default_reduction: Reduktion der normalisierten Zielkomponente bei VOLLER Abdeckung
#   der Zelle (0..1). coverage_scaling: 'linear' oder 'saturating'.
# linked_risk_codes: Risiken, die neu berechnet werden.
#
# Kostenmodell — symmetrisch CAPEX (einmalig) / OPEX (jährlich), je fix / Stück / Fläche.
# MECE: jeder Euro ist entweder einmalige Investition (CAPEX) oder wiederkehrende Betriebs-
# und Unterhaltskosten (OPEX); innerhalb beider Blöcke disjunkt nach Bezugsgröße (mengen-
# unabhängig / je Stück / je m²). Nicht anwendbar = None, NICHT 0.0 — 0.0 heißt "anwendbar,
# aber kostenlos" (z. B. planungsrechtliche Bauverbote).
#   capex_fixed          € einmalig, mengenunabhängig (Planung/Konzept/Einrichtung)
#   capex_per_unit       €/Stück      einmalig je Einheit (unit_label)
#   capex_per_m2         €/m²         einmalig je Polygonfläche
#   opex_fixed_year      €/a          wiederkehrend, mengenunabhängig (Betrieb/Koordination)
#   opex_per_unit_year   €/(Stück·a)  wiederkehrend je Einheit (Betrieb & Unterhalt)
#   opex_per_m2_year     €/(m²·a)     wiederkehrend je Fläche (Betrieb & Unterhalt)
#   unit_label           z. B. "Brunnen", "Station", "km"; None ⇒ keine Stück-Logik
#   unit_density_per_ha  Stück/ha Richtwert-Dichte (gesetzt wenn unit_label);
#                         Richtwert-Anzahl = max(1, round(density · Fläche_ha)),
#                         skaliert die Wirkung über u = min(1, Anzahl/Richtwert)
#   source / sources     Kurz-Key-Fallback bzw. per-Feld-Kurzquelle (Keys = Feldnamen
#                         inkl. default_reduction, unit_density_per_ha)
#   source_details       per-Feld-Langtext (Hover-Tooltip): woher der Wert stammt bzw. wie
#                         er hergeleitet/plausibilisiert wurde (Keys = Feldnamen)
# CAPEX  = capex_fixed + Anzahl × capex_per_unit + Fläche × capex_per_m2
# OPEX/a = opex_fixed_year + Anzahl × opex_per_unit_year + Fläche × opex_per_m2_year
# benefit_per_m2_year (Nutzen-Seite) bleibt unverändert vom Kostenmodell getrennt.
# default_reduction: je Maßnahme mit Wirkmechanismus-Herleitung dokumentiert (inline oder
#   zentral in _MEASURE_EFFECT_DOCS unten); wo Wirksamkeitsstudien existieren, darauf
#   kalibriert (z. B. Hitzeaktionspläne 0,25 nach Urban u. a. 2025). Kommune kann Werte
#   über PUT /kommune/{id}/parameters mit eigener Quelle überschreiben.
# Kostenquellen: recherchierte Kennwerte je Feld (sources/source_details/source_refs);
#   bewusste 0-Werte erklärt _enrich_measure_zero_cost_docs() maßnahmen­spezifisch.
#   Vollständigkeit („kein Parameter ohne Infokasten") erzwingt der Ratchet-Test
#   backend/tests/test_parameter_docs_complete.py.

MEASURES: list[dict] = [
    # Herleitung capex_per_unit: eine einzelne Ortsnetzstation kostet ~18.000-50.000 € (400-kVA-
    # Trafo bis eigene MS-Station inkl. Verkabelung; ront.info, ms-elektro), eine vollständige
    # Mittelspannungs-Netzverstärkung ~0,8-3 Mio € (Bayernwerk-Projekte). Der Wert 250.000 €/
    # "Station" steht für ein Verstärkungs-/Redundanzpaket je Netzknoten (Stationsausbau +
    # redundante Einspeisung + Kabelabschnitt), plausibilisiert zwischen Einzelstation und
    # Vollausbau (BNetzA/dena-Größenordnung).
    # Herleitung capex_per_unit: keine belastbare Einzelquelle für die hitzefeste Ertüchtigung/
    # Kühlung energiebezogener Anlagen (Transformatoren, Umspannwerke) — Modellannahme.
    # Größenordnung sechsstellig je Anlage (Zusatzkühlung/Redundanz); Punktwert 120.000 €.
    # Herleitung capex_per_m2: schlüsselfertige Aufdach-PV ~1.015-1.200 €/kWp (2026), Batterie-
    # speicher ~315-500 €/kWh (HTW-Stromspeicher-Inspektion 2025; 42watt). Bei ~6 m² Modul-
    # fläche je kWp entspricht das ~170-200 €/m² Modulfläche; über die Bruttodachfläche inkl.
    # Speicheranteil → Punktwert 150 €/m². opex_per_m2_year: ~1-2 % Betrieb/Versicherung.
    # Herleitung capex_per_m2/opex_per_m2_year: Mischmaßnahme Dach- + Fassadenbegrünung.
    # Extensives Gründach 40-70 €/m² Herstellung, Unterhalt 0,50-5 €/m²/a (BuGG-Marktreport;
    # 11880-dachdecker/co2online 2026); bodengebundene Fassadenbegrünung 15-35 €/m²
    # (co2online/gartenbau.org 2025). 55 €/m² Investition + 4 €/m²/a Unterhalt als Blend im
    # oberen Bereich (Gründach dominiert die Fläche).
    # Herleitung capex_per_m2: Objektschutz ist eigentlich objekt-/öffnungsbezogen, nicht
    # flächenbezogen — die BBK-Hochwasserschutzfibel (BMWSB 2022) beschreibt die Maßnahmen
    # qualitativ ohne €/m²-Kennwert. €/m² ist hier eine Modell-Abstraktion, plausibilisiert
    # anhand Einzelmaßnahmenkosten: Rückstauklappe fachkundig ~2.000-3.000 €, mobile
    # Kellerfenster-Schotts 800-1.200 €/Fenster (kostencheck/glaserei.org 2026), zzgl.
    # Abdichtung/Barrieren. Auf typische geschützte Gebäudegrundfläche umgelegt → 40 €/m².
    # Herleitung capex_per_m2: Entsiegelung (Aufbruch + Entsorgung + Begrünung) ~25-40 €/m²
    # je nach aufzubrechendem Material (Sieker, bauindex-online 2026); kommunale
    # Förderprogramme setzen bis 40 €/m² an (Bremen), OÖ 30 €/m² pauschal → Punktwert 35 €/m².
    # Herleitung capex_per_m2: sonnenreflektierende Dachbeschichtung 10-30 €/m², Acryl-
    # beschichtung im Mittel ~18 €/m² (asphalt-shop/steelmonks 2026) → Punktwert 20 €/m².
    # opex_per_m2_year: Modellannahme (anteilige Nachbeschichtung ~alle 10-15 Jahre).
    # Herleitung capex_per_m2: heller/hitzeresilienter Asphalt verursacht ~3-5 €/m² Mehrkosten
    # gegenüber Normalasphalt (45-60 €/m²), d. h. 20-50 % teurer (strasse-und-autobahn.de,
    # bauindex 2026). Der Wert 30 €/m² entspricht eher einer Deckschichterneuerung mit hellem
    # Belag als nur den Mehrkosten; plausibilisiert im Bereich Teilerneuerung.
    # Herleitung capex_per_m2: Muldenversickerung 10-45 €/m², Mulden-Rigolen-System 60-85 €/m²
    # abflusswirksamer Fläche (DWA-A 138; baupreislexikon 2026) → Punktwert 45 €/m² an der
    # oberen Grenze reiner Mulden bzw. unterer Grenze kombinierter Systeme.
    # opex_per_m2_year: DWA-Betriebskennwert 0,50-0,75 €/m² abflusswirksamer Fläche;
    # bezogen auf die (deutlich kleinere) Anlagenfläche selbst höher → Punktwert 2 €/m²/a.
    # Herleitung capex_per_unit: keine belastbare Standardquelle für die Ertüchtigung eines
    # kritischen Verkehrsknotens (Schutz vor Überflutung/Hitze/Ausfall) — Modellannahme in
    # niedriger sechsstelliger Größenordnung je Knoten → 80.000 €.
    # Herleitung capex_per_m2: Biotopverbund (Trittsteine, Hecken, Säume, Vernetzungsstrukturen)
    # hat keinen einheitlichen Flächenkennwert; günstige lineare Vernetzungselemente
    # (vgl. Hecken 5-20 €/lfm) auf die verbundene Fläche umgelegt → niedrige €/m². Punktwert
    # 8 €/m² als Modellannahme, plausibilisiert.
    # Herleitung capex_per_m2: Auenrenaturierung streut extrem nach Intensität. Extensive
    # Deichrückverlegung/Flächenrückgabe ~0,3-3 €/m² (WWF/BfN Mittlere Elbe: 6,5 Mio € auf
    # 2.300 ha ≈ 2.826 €/ha ≈ 0,28 €/m²); aktive/technische Renaturierung mit Erdbau und
    # Strukturanreicherung liegt bei ~5-20 €/m² (UBA: kleine Maßnahmen ~10 €/lfm bis techn.
    # Umbau 600+ €/lfm Gewässerlauf). Punktwert 12 €/m² für moderat-intensive Renaturierung
    # mit Erdbau; Modellannahme, plausibilisiert.
    # Herleitung capex_per_m2: Hecken kosten 15-55 €/lfm komplett gepflanzt, Windschutzhecken
    # 5-20 €/lfm (gartenbau-kosten/kostencheck 2026). Als €/m² über die geschützte Feldfläche
    # ist das eine Modell-Umlage (Hecken belegen nur Ränder, Terrassen sind teurer) → 10 €/m²
    # als Mischwert; Modellannahme, plausibilisiert anhand Heckenpreisen.
    # Herleitung capex_per_m2/maintenance: Humusaufbau erfolgt v. a. über Zwischenfrüchte/
    # Begrünung; Saatgut 20-60 €/ha, Prämien bis 220 €/ha (KTBL/LfL; ÖPUL) ≈ 0,002-0,022 €/m².
    # Punktwerte auf 0,02 €/m² (Etablierung, ~200 €/ha) bzw. 0,02 €/m²/a (laufende Begrünung,
    # ~200 €/ha/a) angepasst — Alt-Katalogwerte (2 bzw. 0,3 €/m²) lagen ~2 Größenordnungen zu hoch.
    # Herleitung capex_per_m2: trockenresistente Sorten verursachen im Wesentlichen nur einen
    # Saatgut-Mehrpreis (Saatgut gesamt ~50-200 €/ha; KTBL ≈ 0,005-0,02 €/m²). Punktwerte auf
    # 0,02 €/m² bzw. 0,02 €/m²/a gesenkt (obere Grenze der Saatgutspanne) — Alt-Katalogwerte
    # (1 bzw. 0,2 €/m²) lagen weit über jedem realen Sortenaufpreis.
    # Herleitung capex_per_m2: KTBL-Richtwert für neue Bewässerungssysteme ~5.000 €/ha
    # (Tröpfchen am teuersten, 18 €/mm/ha; profi.de/Thünen). Punktwert 0,5 €/m² (=5.000 €/ha)
    # = KTBL-Bewässerungsrichtwert; ein zusätzlicher Speicheranteil würde ihn erhöhen. Alt-
    # Katalogwert 5 €/m² (=50.000 €/ha) lag ~Faktor 10 darüber und wurde gesenkt.
    # Herleitung capex_per_m2: Waldumbau/Wiederbewaldung kostet je nach Baumart und Zaun
    # 3.000-20.000 €/ha, mit Vollzaun/intensiver Pflege bis 30.000 €/ha (Landesforsten RLP:
    # Douglasie ~7.600 €/ha, Eiche/Buche >20.000 €/ha; Ø ~12.700 €/ha) ≈ 0,3-3 €/m². Punktwert
    # 1,5 €/m² (=15.000 €/ha) nahe dem Durchschnitt inkl. Zaun — Alt-Katalogwert 4 €/m²
    # (=40.000 €/ha) lag oberhalb selbst intensiver Fälle und wurde gesenkt.
    # Herleitung capex_per_m2: präventive Waldbrandmaßnahmen (Wundstreifen/Riegel, Löschwasser-
    # entnahmestellen, Monitoring) sind überwiegend punktuell/linear und je Fläche günstig;
    # kein belastbarer Flächen-Kennwert auffindbar. Punktwert 1 €/m² als Modellannahme, für
    # großflächige Anwendung tendenziell zu hoch.
    # Herleitung capex_fixed: Praxisrichtwert Erstellung Hitzeschutz-/Hitzeaktionsplan
    # Mittelstadt (~80.000 EW): 80.000-150.000 € zzgl. halbe Personalstelle
    # (klimastadtraum.de, Kommunalberatung; UBA-Projekt "HAP-DE" und Fulda-Arbeitshilfe
    # nennen selbst keine Kostenzahlen) → Punktwert 100.000 € (unterer Mittelwert).
    {"code": "HEAT_ACTION_PLANS", "name": "Hitzeaktionspläne",
     "description": "Kommunale Hitzeaktionspläne.", "measure_type": "organizational",
     # default_reduction 0,05 (Rev.-7-Integration, Bericht #95 §5): δ_HAP = 0,95 auf den
     # Wochen-Exzess (RR−1) ⇒ linear −5 % Outcome (Band 0–0,15). Die 25,2 % von Urban
     # u. a. 2025 sind der EINFÜHRUNGSEFFEKT über drei Jahrzehnte, nicht der marginale
     # Spielraum gegenüber dem heutigen deutschen Stand — c_kal ist auf Jahre mit
     # laufendem DWD-Warnsystem kalibriert (Doppelzählungs-Wächter, Befund 33/68).
     "effect_target": ["vulnerability"], "default_reduction": 0.05, "coverage_scaling": "saturating",
     "linked_risk_codes": ["EXPECTED_ANNUAL_MORTALITY", "EXPECTED_ANNUAL_MORBIDITY"],
     "capex_fixed": 100000.0, "capex_per_unit": None, "capex_per_m2": None,
     "opex_fixed_year": 20000.0, "opex_per_unit_year": None, "opex_per_m2_year": None, "benefit_per_m2_year": 0.0,
     "unit_label": None, "unit_density_per_ha": None,
     "source": "klimastadtraum.de (Praxisrichtwert) / Modellannahme",
     "sources": {"opex_fixed_year": "Modellannahme (laufende Fortschreibung/Koordination)",
                 "capex_fixed": "klimastadtraum.de (Praxisrichtwert Hitzeaktionsplan)",
                 "default_reduction": "Bericht #95 §5: δ_HAP = 0,95 (Band 0,85–1,00), marginal"},
     "source_refs": {"default_reduction": ["Feldbusch_2025_HHWS",
                                           "Urban_HHAP_Wirksamkeit_2025"]},
     "source_details": {
        "default_reduction": "δ_HAP = 0,95 multiplikativ auf den Wochen-Exzess (RR−1) ⇒ "
            "linear −5 % Outcome (Band 0–15 %; Bericht #95 §5, abgenommen Rev. 7). Evidenz: "
            "DiD über 15 deutsche Städte (Feldbusch u. a. 2025: RR 1,00 [0,98–1,01], "
            "adjustiert 0,85) — der MARGINALE Spielraum gegenüber dem heutigen deutschen "
            "Stand. Die 25,2 % (95 %-KI 19,8–31,9) von Urban u. a. 2025 (102 Städte, "
            "14 Länder, 1990–2019) sind der Einführungseffekt über drei Jahrzehnte und "
            "stecken bereits im Basiswert: Der Kalibrierfaktor ist auf Jahre mit laufendem "
            "DWD-Warnsystem gefittet — ein Hebel in dieser Größe würde doppelt buchen "
            "(Doppelzählungs-Wächter). Ersetzt den früheren Wert 0,25 (Rev.-7-Integration).",
        "opex_fixed_year":
            "Modellannahme für den laufenden Betrieb des Hitzeaktionsplans: jährliche Fortschreibung, Koordination der Warnkette und saisonaler Betrieb (Hitzetelefon). Entspricht grob der anteiligen halben Personalstelle, die klimastadtraum.de bereits für die Erstellung nennt. Punktwert 20.000 €/a (rund 20 % der einmaligen Erstellungskosten); editierbar.",
        "capex_fixed": "Praxisrichtwert für die Erstellung eines kommunalen "
        "Hitzeschutz-/Hitzeaktionsplans einer Mittelstadt (~80.000 EW): 80.000–150.000 € "
        "zzgl. rund einer halben Personalstelle (klimastadtraum.de, Kommunalberatung). Die "
        "einschlägigen Leitfäden (UBA-Projekt \"HAP-DE\", Fulda-Arbeitshilfe) beschreiben die "
        "Planerstellung, nennen aber selbst keine Kostenzahlen. Punktwert 100.000 € als "
        "unterer Mittelwert der Spanne."}},
    # Herleitung capex_per_unit: keine belastbare Primärquelle für "Kühlraum"-Herrichtung
    # als Gesamtpaket auffindbar (Modellannahme); plausibilisiert anhand Marktpreisen
    # gewerblicher Split-Klimaanlagen 1.500-5.000 € Gerät+Einbau (ADAC/Heizcenter 2026)
    # zzgl. Ausstattung/Trinkwasserstation/Beschilderung ~2.000-3.000 € → Punktwert 8.000 €
    # (Modellannahme, mangels belastbarer Quelle für die Gesamtmaßnahme).
    # Herleitung capex_fixed: kommunales Starkregen-/Hochwasser-Frühwarnsystem — Machbarkeits-
    # studie ~5.000 €, Messnetzkonzept bis ~100.000 € (LEADER-gefördert), laufender Betrieb
    # 30.000-40.000 €/a (kommunal.de/Hydrotec 2025); Großprojekt Landkreis Fulda >800.000 €.
    # Punktwert 60.000 € für Aufbau eines mittleren Systems (Konzept + Basis-Sensorik).
    # Herleitung capex_per_m2/opex_per_m2_year: kein einheitlicher Kennwert für
    # "Ausbau Stadtgrün" als Sammelmaßnahme auffindbar (Modellannahme, mangels belastbarer
    # Quelle) — Plausibilisierung anhand Institut für Stadtgrün/Fachsymposium 2013
    # (Unterhaltung 0,65-85 €/m²/a je nach Pflegeintensität: Rasen bis Wechselflor) und
    # Berliner Stadtbaumkampagne (~3.000 €/Baum inkl. 3 Jahre Pflege); 25 €/m² Investition
    # bzw. 3 €/m² Unterhalt liegen im plausiblen Bereich für Grünfläche mittlerer Dichte
    # (Baumbestand + Rasen/Strauchflächen, keine intensive Zierbepflanzung).
    # Herleitung capex_fixed: Erstellung kommunaler Evakuierungs-/Notfallpläne — der BBK
    # (Bundesamt für Bevölkerungsschutz und Katastrophenhilfe) liefert Rahmenempfehlungen/
    # Leitfäden, aber keine Kostenkennwerte. Modellannahme als einmaliges Planungs-/
    # Konzeptbudget (Analyse, Planwerk, Übungen) → 40.000 €.
    # Herleitung: rein planungsrechtliche Maßnahme (Bauverbot/Rückhaltung in Gefahrenzonen über
    # Bauleitplanung); direkte Umsetzungskosten ≈ 0 €/m² (0,0 = anwendbar, aber kostenlos —
    # nicht "unbelegt"). Etwaige Entschädigungs-/Opportunitätskosten sind hier nicht abgebildet.
    # Herleitung capex_per_m2: Freihaltung von Frischluftkorridoren ist überwiegend Planung/
    # Flächensicherung (Bebauungsverzicht, gelegentliche Gehölzpflege) ohne baulichen Aufwand;
    # kein Marktkennwert. Punktwert 2 €/m² als niedrige Modellannahme (Planungs-/Pflegeanteil).
    # Herleitung capex_per_m2: Schwammstadt ist ein Bündel (Entsiegelung 25-40 €/m² + Mulden-
    # Rigolen 60-85 €/m² + Baumrigolen/Retention), kein einzelner Kennwert. Plausibilisiert
    # als Mischwert im unteren Bereich der Kombinationsmaßnahmen (Hamburg RISA, DWA-A 138)
    # → Punktwert 40 €/m². Modellannahme für die Sammelmaßnahme.
    # Herleitung capex_per_m2: offene Retentionsflächen/Erdbecken kosten ~26-50 €/m³ nutzbaren
    # Rückhalts (Praxisbeispiele, agrarheute/Sieker 2026); bei flacher Bauweise (~1 m Tiefe)
    # entspricht das grob €/m² → Punktwert 30 €/m². opex_per_m2_year: Unterhalt offener
    # Erd-/Betonbecken ~0,50 €/m²/a (Sieker); Katalogwert 1,0 €/m²/a mit Puffer für Mahd/
    # Entschlammung.
    # Herleitung capex_per_m2: großflächige, offene Polder/Hochwasserrückhaltung liegen am
    # unteren Ende der Retentionskostenspanne (viel Fläche, wenig Bauwerk) → Punktwert 25 €/m²,
    # abgeleitet aus den Regenrückhaltebecken-Praxiswerten (Sieker/agrarheute 2026).
    # Herleitung capex_per_m2: Flächen-/Muldenversickerung 10-45 €/m² abflusswirksamer Fläche
    # (DWA-A 138; baupreislexikon 2026) → Punktwert 30 €/m² im mittleren Bereich.
    # Herleitung capex_per_m2: DGM-basierte Abflusslenkung ist überwiegend Planung/geringfügige
    # Geländemodellierung (Bordsteine, Mulden, Wege als Notwasserwege) ohne einheitlichen
    # Baukennwert → Punktwert 8 €/m² als niedrige Modellannahme. Mangels belastbarer Quelle.
    # Herleitung capex_per_m2: künstliche Grundwasseranreicherung (Sickerbecken/-gräben) ohne
    # einheitlichen €/m²-Kennwert; an der unteren Versickerungskostenspanne (DWA-A 138)
    # orientiert → Punktwert 10 €/m². Überwiegend Modellannahme.
    # Herleitung capex_per_unit: Rohrnetzsanierung offene Bauweise 80-150 €/lfm, grabenlose
    # Inliner-Verfahren (CIPP) 50-90 €/lfm (DVGW W 392 / energie|wasser-praxis). Ein
    # "Abschnitt" ≈ 1 km Leitung → 50-150 T€; Punktwert 90.000 € (Mittel, gemischtes Verfahren).
    # Herleitung capex_per_unit: umfassende Deichsanierung/-verstärkung kostet nach Praxis-
    # projekten ~1,25-2,1 Mio €/km an Flussdeichen (Sachsen-Anhalt/Hessen 2024-2026,
    # volksstimme/rp-darmstadt) und ~4 Mio €/km an See-/Küstendeichen (NLWKN Generalplan
    # Küstenschutz: ~500 Mio € für ~125 km). Punktwert 1.250.000 €/km = konservativer unterer
    # Rand der belegten Flussdeich-Spanne (Alt-Katalogwert 300.000 €/km war Faktor 4-13 zu
    # niedrig und wurde angehoben).
    # Herleitung capex_per_unit: keine belastbare Einzelquelle für "Salzwasserbarriere" als
    # Standardanlage — Modellannahme. Kleine lokale Bauwerke gegen Salzwasserintrusion
    # (Sohlschwellen, Regelungswehre) liegen im niedrigen sechsstelligen Bereich, große
    # Sturmflutsperrwerke (z. B. Emssperrwerk) dagegen im dreistelligen Mio-Bereich und sind
    # hier NICHT gemeint. Punktwert 150.000 €/Anlage als lokale Kleinbarriere.
    # Herleitung capex_fixed: organisatorisch-finanzielle Maßnahme (Risikoanalyse, Priorisierung
    # von Investitionsbudgets) ohne baulichen Anteil; kein Marktkennwert. Modellannahme in
    # Höhe eines Beratungs-/Konzeptbudgets → 30.000 €.
    # Herleitung capex_fixed: Anreizprogramm (z. B. Förderung/Prämien für private Vorsorge);
    # kein einheitlicher Kennwert. Modellannahme in Höhe eines Programm-Aufsetzbudgets → 25.000 €.
    # Herleitung capex_per_unit: betriebliche Kühlkonzepte (Prozess-/Gebäudekühlung in Industrie/
    # Gewerbe) sind stark anlagenspezifisch; keine belastbare Standard-Quelle. Modellannahme in
    # sechsstelliger Größenordnung je Anlage → 70.000 €.
    # Herleitung capex_fixed: Lieferketten-Resilienz (Zweitlieferanten, Lager-/Redundanzkonzepte,
    # Notfallplanung) ist organisatorisch; kein Marktkennwert. Modellannahme als Konzept-/
    # Aufbaubudget → 40.000 €. Organisatorische Maßnahme: Modellannahme ist erwarteter Regelfall.
    # Herleitung capex_fixed: gezielte Schutzprogramme für vulnerable Gruppen (Hitzetelefon,
    # aufsuchende Betreuung, Aufklärung) sind organisatorisch; kein einheitlicher Kennwert.
    # Modellannahme als Programmbudget (Konzeption/Koordination) → 35.000 €.
    {"code": "VULNERABLE_GROUP_PROGRAMS", "name": "Schutzprogramme vulnerable Gruppen",
     "description": "Gezielte Programme für vulnerable Gruppen.", "measure_type": "organizational",
     "effect_target": ["vulnerability"], "default_reduction": 0.22, "coverage_scaling": "saturating",
     # SOCIAL_INEQUALITY_AMPLIFICATION_RISK_INDEX ist geparkt (M5) — Link auf den
     # zweiten Teil-Ausweis von #95 umgehängt (Schutzprogramme senken die
     # Erkrankungslast vulnerabler Gruppen ebenso wie die Mortalität).
     "linked_risk_codes": ["EXPECTED_ANNUAL_MORTALITY", "EXPECTED_ANNUAL_MORBIDITY"],
     "capex_fixed": 35000.0, "capex_per_unit": None, "capex_per_m2": None,
     "opex_fixed_year": 10000.0, "opex_per_unit_year": None, "opex_per_m2_year": None, "benefit_per_m2_year": 0.0,
     "unit_label": None, "unit_density_per_ha": None,
     "source": "Modellannahme (Programmbudget)",
     "sources": {"opex_fixed_year": "Modellannahme (laufender Programmbetrieb)",
                 "capex_fixed": "Modellannahme (organisatorisches Programmbudget)",
                 "default_reduction": "Urban u. a. 2025 (HHAP-Kernbaustein) / RKI-Risikogruppen"},
     "source_refs": {"default_reduction": ["Urban_HHAP_Wirksamkeit_2025", "RKI_Hitzemortalitaet"]},
     "source_details": {
        "default_reduction": "Wirkmechanismus: Hitzemortalität konzentriert sich stark auf "
            "Risikogruppen (Hochaltrige, Pflegebedürftige, Vorerkrankte — RKI/Winklmayr); "
            "aufsuchende Programme (Hitzetelefon, Pflegeheim-Protokolle, Nachbarschaftshilfe) "
            "adressieren genau diese Gruppe und sind Kernbaustein wirksamer Hitzeaktionspläne "
            "(Gesamtpaket: −25,2 % Hitzemortalität, Urban u. a. 2025). Angesetzt: 22 % Reduktion "
            "des verknüpften Mortalitäts-/Ungleichheitsrisikos — nahe an der HHAP-Gesamtwirkung, "
            "da die Zielgruppe den Großteil der Übersterblichkeit trägt. Editierbar.",
        "opex_fixed_year":
            "Modellannahme für den laufenden Betrieb der Schutzprogramme für vulnerable Gruppen (aufsuchende Beratung, Netzwerkpflege) — überwiegend Personalaufwand, daher höherer Jahresanteil. Punktwert 10.000 €/a; kein belastbarer Kostenkennwert; editierbar.",
        "capex_fixed": "Gezielte Schutzprogramme für vulnerable Gruppen (z. B. Hitzetelefon, "
            "aufsuchende Betreuung, Aufklärung in Pflegeeinrichtungen) sind organisatorisch "
            "ohne baulichen Anteil; ein einheitlicher Kennwert existiert nicht. Modellannahme "
            "als einmaliges Programmbudget (Konzeption/Koordination) → 35.000 €."}},
    # Herleitung capex_fixed: angepasste Arbeitszeitmodelle bei Hitze verursachen im Kern nur
    # organisatorischen Aufwand (Dienstplanung, Betriebsvereinbarung); kein Marktkennwert.
    # Modellannahme als geringes Einführungs-/Konzeptbudget → 10.000 €.
    # Herleitung capex_per_m2/opex_per_m2_year: keine belastbare €/m²-Quelle für die
    # Mischmaßnahme "Schatten/Wasser" auffindbar (Modellannahme, mangels belastbarer
    # Quelle) — Einzelkomponenten (Sonnensegel-Masten ~160-350 €/Stück, Sonnensegel ab
    # ~70 €/Stück, sonnensegel-guru.de 2026; Wasserspielplatz-Projekt Stuttgart Süd-
    # heimer Platz ~230.000 € Gesamtinvestition ohne Flächenangabe) bestätigen nur die
    # Größenordnung, ergeben aber keinen sauberen Flächen-Kennwert.
    # Herleitung capex_fixed: adaptive Bewirtschaftung (Fangregeln, Schonzeiten, Monitoring) ist
    # rein organisatorisch; kein Marktkennwert. Modellannahme als Monitoring-/Konzeptbudget →
    # 20.000 €. Überwiegend Modellannahme ist im Fischerei-Cluster der erwartete Regelfall.
    # Herleitung capex_per_unit: Fischaufstiegsanlagen kosten je nach Bauart und Gewässergröße
    # stark unterschiedlich — ein Beispiel nennt ~600.000 € je Anlage, kompakte technische
    # Pässe (Denil/Schlitzpass) an kleinen Querbauwerken liegen deutlich darunter (Wikipedia/
    # LfU Bayern/BAW). Punktwert 200.000 €/Anlage als repräsentativer Mittelwert über kleine
    # bis größere Anlagen (Alt-Katalogwert 50.000 € bildete nur den kleinsten Pass ab).
    # Herleitung capex_per_unit: keine belastbare Standardquelle für die Resilienz-Ertüchtigung
    # einer Aquakulturanlage (Sauerstoff-/Kühlungstechnik, Notstrom, Wasseraufbereitung) —
    # Modellannahme in sechsstelliger Größenordnung je Anlage → 60.000 €.
    # Herleitung capex_per_m2: Laichhabitat-/Gewässerrenaturierung liegt je nach Aufwand bei
    # ~10 €/lfm (kleine Maßnahmen) bis 600+ €/lfm (technischer Umbau) Gewässerlauf (UBA);
    # flächenbezogen für Kies-/Strukturanreicherung Größenordnung einstellige €/m². Punktwert
    # 10 €/m² für moderate Struktur-/Substratanreicherung; Modellannahme, plausibilisiert.
    # Herleitung capex_fixed: organisatorischer Gewässerschutz (Gewässermonitoring, Uferrand-
    # streifen-/Einleiter-Management, Kooperationen) ohne einheitlichen Bau-Kennwert.
    # Modellannahme als Konzept-/Monitoringbudget → 25.000 €.
    # Herleitung capex_per_unit: Berliner Wasserbetriebe: Errichtung inkl. Trinkwasser-
    # anschluss ~10-16 T€/Standort → Punktwert 14.000 €. Unabhängig bestätigt durch
    # Presseberichte (Berliner Zeitung/Tagesspiegel 2026): 12.000-15.000 €/Brunnen.
    # Herleitung opex_per_unit_year: Betrieb/Wartung/Beprobung ~2,5-5 T€/a → 3.500 €.
    # Presseberichte nennen ~4.500 €/a für Wartung/Beprobung (innerhalb der Spanne).
]


def _fmt_eur_de(value: float) -> str:
    """1234567.0 → "1.234.567" (deutsches Tausenderformat, ohne Nachkommastellen)."""
    if value == int(value):
        return f"{int(value):,}".replace(",", ".")
    return f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def _enrich_measure_zero_cost_docs() -> None:
    """Herleitung für bewusste 0-Werte des Maßnahmen-Kostenmodells (je Maßnahme).

    Nutzeranforderung: Auch eine 0 braucht einen Infokasten, der erklärt, WARUM sie 0
    ist. Die Texte sind maßnahmen-spezifisch (nennen den tatsächlichen Kostenträger der
    Maßnahme) und werden nur gesetzt, wo noch keine handgeschriebene Herleitung existiert
    — individuelle ``source_details``-Einträge (z. B. Netzverstärkung) haben Vorrang.
    """
    for m in MEASURES:
        sources_map = m.setdefault("sources", {})
        details = m.setdefault("source_details", {})

        # capex_fixed == 0: Kosten skalieren vollständig über Stück-/Flächenkostensätze.
        if m.get("capex_fixed") == 0.0 and not details.get("capex_fixed"):
            unit_label = m.get("unit_label") or "Stück"
            carriers: list[str] = []
            if m.get("capex_per_unit"):
                carriers.append(
                    f"Stückkostensatz ({_fmt_eur_de(m['capex_per_unit'])} €/{unit_label})")
            if m.get("capex_per_m2"):
                carriers.append(
                    f"Flächenkostensatz ({_fmt_eur_de(m['capex_per_m2'])} €/m²)")
            if carriers:
                detail = (
                    "0 € ist bewusst gesetzt: Diese Maßnahme hat keinen investiven "
                    f"Sockelbetrag — die Investition skaliert vollständig über den "
                    f"{' und den '.join(carriers)} dieser Maßnahme; Planungs-/Nebenkosten "
                    "sind in diesen Einheitssätzen einkalkuliert. Ein zusätzlicher "
                    "Grundkosten-Betrag würde im MECE-Kostenmodell (CAPEX = fix + "
                    "Anzahl × Stücksatz + Fläche × Flächensatz) doppelt zählen. Editierbar, "
                    "falls die Kommune ein separates Planungs-/Grundbudget ansetzen will."
                )
            elif m.get("opex_fixed_year"):
                detail = (
                    "0 € ist bewusst gesetzt: Diese organisatorische Maßnahme erfordert "
                    "keine Bauinvestition; ihr Aufwand ist als laufende feste "
                    f"Betriebskosten ({_fmt_eur_de(m['opex_fixed_year'])} €/Jahr, "
                    "opex_fixed_year) modelliert. Editierbar, falls einmalige "
                    "Aufbaukosten (z. B. Erstkonzept) separat budgetiert werden."
                )
            else:
                detail = (
                    "0 € ist bewusst gesetzt: Die Maßnahme wirkt planungsrechtlich/"
                    "organisatorisch ohne modellierte Bauinvestition; der geringe "
                    "Verwaltungsaufwand ist nicht als eigener Kostenblock angesetzt. "
                    "Editierbar, falls die Kommune Umsetzungskosten budgetieren will."
                )
            details["capex_fixed"] = detail
            sources_map.setdefault(
                "capex_fixed", "Modellentscheidung (Kostenstruktur, dokumentiert)")

        # benefit_per_m2_year == 0: Hauptnutzen läuft über vermiedene Schäden (E3),
        # nicht über dieses Feld — sonst Doppelzählung.
        if m.get("benefit_per_m2_year") == 0.0 and not details.get("benefit_per_m2_year"):
            details["benefit_per_m2_year"] = (
                "0 €/(m²·a) ist bewusst gesetzt: Der Hauptnutzen der Maßnahme — vermiedene "
                "Klimaschäden — wird NICHT über dieses Feld gerechnet, sondern als "
                "Reduktion der Zellschadenskosten der verknüpften Risiken "
                "(Risikoreduktion × Zellkosten, measure_service). Dieses Feld bildet nur "
                "direkte marktfähige Zusatznutzen ab (z. B. Energieertrag, eingesparte "
                "Wasser-/Energiekosten). Für diese Maßnahme ist kein solcher "
                "flächenbezogener Zusatznutzen belegt — ein Wert > 0 ohne Beleg wäre eine "
                "Doppelzählung des Schadensnutzens."
            )
            sources_map.setdefault(
                "benefit_per_m2_year", "Modellentscheidung (Nutzen-Abgrenzung, dokumentiert)")


_enrich_measure_zero_cost_docs()


# ── Wirkungs-/Nutzen-Herleitungen je Maßnahme (Parameter-Vollerklärung) ─────────
# Je Eintrag: Feld → (Quellen-Kurzlabel, [Bibliografie-Keys], Herleitungstext).
# Zentrale Datenstruktur statt Inline-Edit je Maßnahme; Inline-``source_details``
# in den Maßnahmen-Dicts haben Vorrang (werden hier nicht überschrieben).
_MEASURE_EFFECT_DOCS: dict[str, dict[str, tuple[str, list[str], str]]] = {
    # ── Wasser/Starkregen ────────────────────────────────────────────────────────
    "DESEALING_SURFACE": {
        "default_reduction": ("Entsiegelungs-Wirkprinzip (Abflussbeiwert)", ["Bremen_Entsiegelung", "DWA_A138"],
            "Wirkmechanismus: Entsiegelung stellt die natürliche Versickerung wieder her — der "
            "Abflussbeiwert sinkt von ~0,9 (Asphalt/Beton) auf ~0,1-0,3 (begrünte Fläche), d. h. "
            "60-80 % des Oberflächenabflusses der entsiegelten Fläche entfallen (DWA-A-138-"
            "Kennwerte; Bremer Entsiegelungsprogramm). Zusätzlich kühlt die Fläche und speist "
            "Grundwasser. Angesetzt: 30 % Reduktion der verknüpften Überflutungs-/Hitzerisiken "
            "in den entsiegelten Zellen. Editierbare Modellannahme im belegten Wirkprinzip."),
        "benefit_per_m2_year": ("Gesplittete Abwassergebühr + Ökosystemleistung", ["BWB_Niederschlagswasserentgelt", "TEEB_DE_Naturkapital"],
            "Direkter Zusatznutzen: Entsiegelte Flächen entfallen aus dem Niederschlagswasser"
            "entgelt (z. B. 1,84 €/m²·a in Berlin, BWB) und erbringen Ökosystemleistungen "
            "(Versickerung, Kühlung, Grün; TEEB DE einige €/m²·a) → Punktwert 5 €/(m²·a). "
            "Kommunal unterschiedlich, editierbar."),
    },
    "SPONGE_CITY": {
        "default_reduction": ("Schwammstadt-Prinzip (RISA/DWA-Bemessung)", ["DWA_A138"],
            "Wirkmechanismus: Schwammstadt-Bündel (Entsiegelung, Mulden/Rigolen, Baumrigolen, "
            "Retentionsflächen) halten Niederschlag dezentral zurück und verdunsten ihn — "
            "bemessen nach DWA-A 138 nimmt das System Regen bis zum Bemessungsereignis nahezu "
            "vollständig auf und dämpft zugleich Hitze über Verdunstung. Angesetzt: 30 % "
            "Reduktion der verknüpften Überflutungs-/Gebäudeschadensrisiken in den umgestalteten "
            "Zellen (oberer Bereich der Flächenmaßnahmen, da Maßnahmenbündel). Editierbare "
            "Modellannahme im DWA-Bemessungsprinzip."),
        "benefit_per_m2_year": ("Gesplittete Abwassergebühr + Stadtgrün-Nutzen", ["BWB_Niederschlagswasserentgelt", "TEEB_DE_Naturkapital"],
            "Direkter Zusatznutzen: abgekoppelte Flächen sparen Niederschlagswasserentgelt "
            "(1,84 €/m²·a Berlin, BWB; bei Versickerung −50 bis −100 % der Gebühr) plus Grün-/"
            "Aufenthaltsnutzen der blau-grünen Elemente (TEEB DE) → 5 €/(m²·a); editierbar."),
    },
    "RETENTION_STORAGE": {
        "default_reduction": ("Retentions-Bemessung (DWA)", ["DWA_A138", "Agrarheute_Rueckhaltebecken"],
            "Wirkmechanismus: Rückhaltebecken/-flächen kappen die Abflussspitze — bis zur "
            "Bemessungsgröße wird der Scheitel vollständig zwischengespeichert und gedrosselt "
            "abgegeben (DWA-Regelwerk). Angesetzt: 28 % Reduktion der verknüpften Überflutungs"
            "risiken in den geschützten Zellen — knapp unter Mulden-Rigolen-Systemen, da "
            "zentrale Becken nur den kanalisierten Abfluss erfassen (wilder Abfluss bleibt). "
            "Editierbare Modellannahme im Bemessungsprinzip."),
        "benefit_per_m2_year": ("Gesplittete Abwassergebühr (angeschl. Flächen)", ["BWB_Niederschlagswasserentgelt"],
            "Direkter Zusatznutzen: Für die an die Retention angeschlossenen, abgekoppelten "
            "Flächen entfällt Niederschlagswasserentgelt (1,84 €/m²·a Berlin, BWB); auf die "
            "Beckenfläche bezogen (Einzugsfläche ≫ Beckenfläche) → 4 €/(m²·a). Editierbar."),
    },
    "RETENTION_POLDER_RESERVOIR": {
        "default_reduction": ("Polder-Scheitelkappung (Praxisnachweis)", ["Agrarheute_Rueckhaltebecken", "UBA_Gewaesserrenaturierung"],
            "Wirkmechanismus: Flutpolder und Speicherbecken kappen Hochwasserscheitel "
            "nachweislich — gesteuerte Polder senken den Scheitel des Bemessungshochwassers "
            "am Unterlieger messbar (Praxis der Länder-Hochwasserschutzprogramme). Angesetzt: "
            "30 % Reduktion der verknüpften Hochwasserrisiken in den geschützten Zellen; "
            "Extremereignisse jenseits des Poldervolumens bleiben (Restrisiko). Editierbare "
            "Modellannahme im belegten Wirkprinzip."),
        "benefit_per_m2_year": ("Modellannahme (Doppelnutzung Polderfläche)", [],
            "Direkter Zusatznutzen: Polder-/Speicherflächen sind außerhalb von Einstauereignissen "
            "land-/grünlandwirtschaftlich nutzbar und können Brauch-/Bewässerungswasser "
            "bereitstellen → 4 €/(m²·a) als konservative Doppelnutzungs-Annahme; editierbar."),
    },
    "INFILTRATION_AREAS": {
        "default_reduction": ("Versickerungs-Bemessung (DWA-A 138)", ["DWA_A138"],
            "Wirkmechanismus: Dezentrale Versickerungsflächen nehmen den Abfluss angeschlossener "
            "Flächen auf und führen ihn dem Grundwasser zu — nach DWA-A 138 auf das Bemessungs"
            "ereignis dimensioniert. Angesetzt: 25 % Reduktion der verknüpften Überflutungs-/"
            "hydrologischen Risiken in den abgedeckten Zellen (wie Mulden-Rigolen). Editierbare "
            "Modellannahme im DWA-Bemessungsprinzip."),
        "benefit_per_m2_year": ("Gesplittete Abwassergebühr", ["BWB_Niederschlagswasserentgelt"],
            "Direkter Zusatznutzen: abgekoppelte, versickernde Flächen sparen Niederschlags"
            "wasserentgelt (1,84 €/m²·a Berlin; ermäßigt −50 % bei bestimmten Versickerungs"
            "arten, BWB) → 3 €/(m²·a) bezogen auf die Anlagenfläche. Editierbar."),
    },
    "RUNOFF_ROUTING_DGM": {
        "default_reduction": ("Starkregen-Gefahrenkarten-Praxis (Notwasserwege)", ["DWA_A138"],
            "Wirkmechanismus: DGM-basierte Abflusslenkung (Notwasserwege, Bordsteine, "
            "Geländemodellierung) leitet den nicht mehr rückhaltbaren Extremabfluss gezielt "
            "über schadarme Korridore ab — Standardbaustein kommunaler Starkregen-Gefahren"
            "kartenkonzepte ergänzend zur DWA-Bemessung. Angesetzt: 20 % Reduktion der "
            "verknüpften Überflutungsrisiken (lenkt, speichert aber nicht). Editierbare, "
            "dokumentierte Modellannahme."),
        "benefit_per_m2_year": ("Modellannahme (multifunktionale Flächen)", [],
            "Direkter Zusatznutzen: Notwasserwege/multifunktionale Retentionsflächen sind im "
            "Normalfall als Straßenraum, Grün- oder Spielfläche nutzbar → 2 €/(m²·a) als "
            "konservative Mehrfachnutzungs-Annahme; editierbar."),
    },
    "GROUNDWATER_RECHARGE": {
        "default_reduction": ("Dargebotssicherung (DVGW-Wirkprinzip)", ["DVGW_W392"],
            "Wirkmechanismus: Gezielte Grundwasseranreicherung (Versickerung von Überschuss"
            "wasser, Uferfiltrat-Management) stützt das nutzbare Dargebot und die Grundwasser"
            "stände in Trockenperioden — der Puffer senkt hydrologischen Stress und Nutzungs"
            "konflikte in Dürrejahren. Angesetzt: 20 % Reduktion der verknüpften Wasser"
            "stressrisiken in den Anreicherungsgebieten. Editierbare, dokumentierte "
            "Modellannahme (Wirkung stark standortabhängig, Hydrogeologie)."),
        "benefit_per_m2_year": ("Modellannahme (gesichertes Rohwasser)", [],
            "Direkter Zusatznutzen: stabilere Rohwasserverfügbarkeit der Wasserversorgung "
            "(vermiedene Ersatzbeschaffung/Fernwasser in Dürrejahren) → 2 €/(m²·a) bezogen "
            "auf die Anreicherungsfläche; konservative Modellannahme, editierbar."),
    },
    # ── Gebäude/Begrünung ────────────────────────────────────────────────────────
    "GREEN_ROOFS_FACADES": {
        "default_reduction": ("BuGG (Retention/Kühlwirkung Gebäudegrün)", ["BuGG_Marktreport_2024", "co2online_Dachbegruenung"],
            "Wirkmechanismus: Extensive Gründächer halten 50-90 % des Jahresniederschlags "
            "zurück (BuGG) und senken die sommerliche Aufheizung des Gebäudes und der Umgebung "
            "(Verdunstung + Dämmwirkung; co2online). Auf die verknüpften Risiken (Wärme"
            "belastung, Gebäudeschäden) wirkt nur der begrünte Flächenanteil der Zelle → 18 % "
            "Reduktion angesetzt. Editierbare Modellannahme im belegten Wirkprinzip."),
        "benefit_per_m2_year": ("co2online/BuGG (Energie) + gespl. Abwassergebühr", ["co2online_Dachbegruenung", "BWB_Niederschlagswasserentgelt"],
            "Direkter Zusatznutzen: Dämm-/Kühlwirkung spart Heiz- und Kühlenergie (co2online: "
            "spürbare Reduktion des Energiebedarfs der obersten Geschosse, grob 2-5 €/m²·a) "
            "und Gründächer mindern das Niederschlagswasserentgelt (Berlin: −50 % von "
            "1,84 €/m²·a, BWB) zzgl. verlängerter Dachlebensdauer → Punktwert 6 €/(m²·a). "
            "Editierbar."),
    },
    "FLOOD_PROTECTION_BUILDING": {
        "default_reduction": ("BBK-Hochwasserschutzfibel (Objektschutz)", ["BBK_Hochwasserschutzfibel"],
            "Wirkmechanismus: Objektschutz am Gebäude (Rückstauklappen, druckdichte Fenster/"
            "Schotts, Abdichtung, angepasste Haustechnik) verhindert das Eindringen von Wasser "
            "bis zum Bemessungsniveau — die BBK-Hochwasserschutzfibel weist für konsequenten "
            "Objektschutz Schadensminderungen bis ~80 % am Einzelgebäude aus. Da je Zelle nur "
            "ein Teil der Gebäude nachgerüstet wird und Extremereignisse Schutzhöhen "
            "überschreiten, werden 35 % Reduktion des Gebäudeschadensrisikos angesetzt — "
            "höchster Wert der Gebäudemaßnahmen. Editierbar (BBK-Wirkprinzip)."),
        "benefit_per_m2_year": ("Modellannahme (Versicherbarkeit/Prämien)", [],
            "Direkter Zusatznutzen: Objektgeschützte Gebäude erreichen bessere Versicherbarkeit "
            "und niedrigere Elementarschaden-Prämien/Selbstbehalte (GDV-Zonierungslogik ZÜRS); "
            "grob 5-10 €/m² Wohnfläche·a Prämienvorteil in gefährdeten Lagen → Punktwert "
            "9 €/(m²·a) auf die geschützte Grundfläche. Modellannahme, editierbar."),
    },
    # ── Küste/Fluss/Boden ────────────────────────────────────────────────────────
    "LEVEE_REINFORCEMENT": {
        "default_reduction": ("NLWKN Generalplan (Bemessungsschutz)", ["NLWKN_Generalplan_Kuestenschutz"],
            "Wirkmechanismus: Deicherhöhung/-verstärkung stellt den Schutz auf das Bemessungs"
            "hochwasser (Küste: Bemessungswasserstand + Wellenauflauf, NLWKN-Generalplan) "
            "wieder her — hinter einem intakten Bemessungsdeich sinkt die Überflutungswahr"
            "scheinlichkeit drastisch. Angesetzt: 35 % Reduktion der verknüpften Hochwasser-/"
            "Sturmflutrisiken in den geschützten Zellen — bewusst nicht höher, weil Deiche "
            "binär versagen können (Versagensrisiko jenseits der Bemessung, Restrisiko-"
            "Prinzip). Editierbar."),
        "opex_per_unit_year": ("NLWKN/Länderpraxis (Deichunterhaltung)", ["NLWKN_Generalplan_Kuestenschutz", "VDI_2067_Blatt1"],
            "Deichunterhaltung ist Daueraufgabe (Mahd/Beweidung, Grasnarben-/Wühltierkontrolle, "
            "Deichschau, kleinere Instandsetzungen): Länderpraxis liegt in der Größenordnung "
            "5.000-15.000 €/km·a je nach Deichtyp. Punktwert 10.000 €/(km·a) ≈ 0,8 % der "
            "Investition — ohne diesen Posten wäre der Deich unrealistisch unterhaltsfrei."),
    },
    "SALTWATER_BARRIERS": {
        "default_reduction": ("Küstenschutz-Wirkprinzip (Sperrwerke/Siele)", ["NLWKN_Generalplan_Kuestenschutz"],
            "Wirkmechanismus: Sperrwerke, Siele und Rückschlagklappen blockieren das Eindringen "
            "von Salzwasser in Vorfluter und Entwässerungssysteme bei Sturmflut/hohen Tiden — "
            "Standardbausteine des Küstenschutzes (NLWKN). Angesetzt: 25 % Reduktion des "
            "Salzwasserintrusions-Risikos im geschützten Einzugsbereich; die schleichende "
            "Intrusion über Grundwasserleiter wird nur teilweise erfasst. Editierbare, "
            "dokumentierte Modellannahme."),
        "opex_per_unit_year": ("VDI 2067 (bewegl. Verschlussorgane)", ["VDI_2067_Blatt1", "NLWKN_Generalplan_Kuestenschutz"],
            "Bewegliche Verschlussorgane (Tore, Klappen, Antriebe) erfordern Wartung, Funktions"
            "proben und Korrosionsschutz: VDI-2067-Größenordnung ~2 % der Investition/Jahr → "
            "3.000 €/(Anlage·a) bei 150.000 € Investition."),
    },
    "EROSION_PROTECTION": {
        "default_reduction": ("LfL (konservierende Bodenbearbeitung/ABAG)", ["LfL_Pflanzenbau"],
            "Wirkmechanismus: Erosionsschutz (Begrünung, Zwischenfrüchte, konservierende "
            "Bearbeitung, Hangrinnen-Begrünung) senkt den Bodenabtrag über den Bedeckungs- und "
            "Bearbeitungsfaktor der Allgemeinen Bodenabtragsgleichung (ABAG) — konservierende "
            "Verfahren reduzieren den C-Faktor und damit den Abtrag um deutlich über 50 % "
            "(LfL-Pflanzenbau-Kennwerte). Angesetzt: 25 % Reduktion der verknüpften Erosions-/"
            "Bodenrisiken (nicht alle Flächen/Kulturen umstellbar). Editierbar."),
        "benefit_per_m2_year": ("Modellannahme (erhaltene Bodenfruchtbarkeit)", ["TEEB_DE_Naturkapital"],
            "Direkter Zusatznutzen: vermiedener Verlust an Bodenfruchtbarkeit und Nährstoffen "
            "(Oberboden-Neubildung dauert Jahrhunderte; TEEB DE bewertet Bodenfunktionen) "
            "0,02 €/(m²·a) = 200 €/ha·a als Werterhalt je Hektar Ackerfläche — von zuvor "
            "2 €/m² (= 20.000 €/ha, unplausibel) herabgesetzt; editierbar."),
    },
    "FLOODPLAIN_RENATURATION": {
        "default_reduction": ("UBA (Gewässer-/Auenrenaturierung)", ["UBA_Gewaesserrenaturierung"],
            "Wirkmechanismus: Reaktivierte Auen und rückverlegte Deiche geben dem Fluss "
            "Retentionsraum zurück — der Hochwasserscheitel wird gedämpft und verzögert "
            "(UBA-Renaturierungsleitfäden; Praxis der Aktionsprogramme an Elbe/Rhein). "
            "Angesetzt: 30 % Reduktion der verknüpften Hochwasserrisiken für die profitierenden "
            "Zellen; wirkt zusätzlich als Dürre-Puffer (Grundwasserstützung). Editierbare "
            "Modellannahme im belegten Wirkprinzip."),
        "benefit_per_m2_year": ("TEEB DE / UBA (Auen-Ökosystemleistungen)", ["TEEB_DE_Naturkapital", "UBA_Gewaesserrenaturierung"],
            "Direkter Zusatznutzen: intakte Auen liefern Ökosystemleistungen (Nährstoff"
            "rückhalt, Kohlenstoffspeicherung, Habitat/Erholung), die TEEB DE für Auen mit "
            "mehreren hundert €/ha·a bewertet. 0,03 €/(m²·a) = 300 €/ha·a entspricht dieser "
            "Spanne — von zuvor 3 €/m² (= 30.000 €/ha, unplausibel) herabgesetzt; editierbar."),
    },
    # ── Land-/Forstwirtschaft ────────────────────────────────────────────────────
    "MIXED_FORESTS": {
        "default_reduction": ("AGDW/Waldumbau (Mischbestands-Resilienz)", ["AGDW_Wiederbewaldung"],
            "Wirkmechanismus: Standortgerechte Mischbestände sind gegenüber Dürre, Sturmwurf, "
            "Borkenkäfer und Kronenfeuer deutlich widerstandsfähiger als Nadel-Reinbestände — "
            "der Kern der Wiederbewaldungs-/Waldumbauprogramme nach den Dürrejahren 2018-2020 "
            "(AGDW; Waldzustandserhebungen zeigen die höchsten Schäden in Fichten-Monokulturen). "
            "Angesetzt: 25 % Reduktion der verknüpften Wald-/Feuerrisiken auf den umgebauten "
            "Flächen über den Bestandszyklus. Editierbare Modellannahme."),
        "benefit_per_m2_year": ("Modellannahme (stabilere Erträge/Senke)", ["TEEB_DE_Naturkapital"],
            "Direkter Zusatznutzen: stabilere Holzerträge (geringere Kalamitätsverluste) und "
            "kontinuierliche Senken-/Ökosystemleistung des Waldes (TEEB DE bewertet Wald-"
            "Ökosystemleistungen mit mehreren hundert €/ha·a). 0,02 €/(m²·a) = 200 €/ha·a "
            "innerhalb der TEEB-Spanne — von zuvor 1,5 €/m² (= 15.000 €/ha, unplausibel) "
            "herabgesetzt; editierbar."),
    },
    "HUMUS_BUILDUP": {
        "default_reduction": ("LfL (Humus-Wasserspeicher)", ["LfL_Pflanzenbau"],
            "Wirkmechanismus: Humusaufbau (Zwischenfrüchte, Mulch, organische Düngung) erhöht "
            "die nutzbare Feldkapazität — je zusätzlichem Prozent Humus speichert der Boden "
            "grob 20-40 mm mehr pflanzenverfügbares Wasser (LfL-Kennwerte) und übersteht "
            "Trockenphasen länger. Angesetzt: 15 % Reduktion der verknüpften Dürre-/Boden"
            "risiken auf den aufgebauten Flächen — bewusst niedrig, da Humusaufbau Jahre "
            "braucht und langsam wirkt. Editierbar."),
        "benefit_per_m2_year": ("KTBL/LfL (Ertragsstabilität)", ["LfL_Pflanzenbau", "KTBL_Feldbewaesserung"],
            "Direkter Zusatznutzen: stabilere Erträge in Trockenjahren und eingesparte "
            "Düngung/Bewässerung (bessere Nährstoff- und Wasserhaltung; KTBL/LfL) → "
            "0,02 €/(m²·a) = 200 €/ha·a als Deckungsbeitrags-Vorteil in Trockenjahren — von "
            "zuvor 1,5 €/m² (= 15.000 €/ha, unplausibel) herabgesetzt; editierbar."),
    },
    "DROUGHT_RESISTANT_VARIETIES": {
        "default_reduction": ("LfL-Sortenversuche (Trockentoleranz)", ["LfL_Pflanzenbau"],
            "Wirkmechanismus: Trockentolerante Arten/Sorten (tiefwurzelnd, hitzetolerant, "
            "früh abreifend) halten die Ertragsbildung in Trockenjahren länger aufrecht — "
            "die LfL-Sortenversuche zeigen in Dürrejahren deutliche Ertragsunterschiede "
            "zwischen Sorten derselben Kultur. Angesetzt: 18 % Reduktion des dürregetriebenen "
            "Ertragsrisikos auf den umgestellten Flächen. Editierbare Modellannahme."),
        "benefit_per_m2_year": ("Modellannahme (Ertragsstabilität)", ["LfL_Pflanzenbau"],
            "Direkter Zusatznutzen: stabilere Erträge/Qualitäten in Trockenjahren ohne "
            "nennenswerte Mehrkosten des Saatguts. 0,02 €/(m²·a) = 200 €/ha·a als vorsichtiger "
            "Deckungsbeitrags-Vorteil im Feldmaßstab — von zuvor 1,5 €/m² (= 15.000 €/ha, "
            "unplausibel) herabgesetzt; editierbar."),
    },
    "WATER_STORAGE_EFFICIENT_IRRIGATION": {
        "default_reduction": ("KTBL (Tröpfchenbewässerung/Speicher)", ["KTBL_Feldbewaesserung"],
            "Wirkmechanismus: Effiziente Bewässerung (Tropf-/Mikrobewässerung spart gegenüber "
            "Beregnung 30-50 % Wasser, KTBL) kombiniert mit Speicherbecken überbrückt "
            "Trockenphasen und Entnahmeverbote — der Ertrag bleibt auch bei Niedrigwasser "
            "gesichert. Angesetzt: 22 % Reduktion des dürregetriebenen Ertragsrisikos auf den "
            "erschlossenen Flächen. Editierbare Modellannahme auf KTBL-Basis."),
        "benefit_per_m2_year": ("KTBL (Wasser-/Energieeinsparung)", ["KTBL_Feldbewaesserung"],
            "Direkter Zusatznutzen: 30-50 % geringerer Wasser- und Pumpenergieeinsatz "
            "gegenüber konventioneller Beregnung (KTBL: Bewässerung kostet mehrere hundert "
            "€/ha·a). 0,05 €/(m²·a) = 500 €/ha·a Einsparung bewässerungsintensiver Kulturen — "
            "von zuvor 2 €/m² (= 20.000 €/ha, unplausibel) herabgesetzt; editierbar."),
    },
    "WILDFIRE_PREVENTION": {
        "default_reduction": ("Waldbrandprävention (Länderpraxis)", ["AGDW_Wiederbewaldung"],
            "Wirkmechanismus: Waldbrandprävention (Brandschutzstreifen, Totholz-/Streu-"
            "Management, Löschwasserentnahmestellen, Früherkennung) senkt Zündwahrschein"
            "lichkeit und v. a. die Ausbreitungsgeschwindigkeit — kleingehaltene Brände "
            "statt Großfeuer (Waldbrandschutzkonzepte der Länder; Laub-/Mischwaldanteil "
            "wirkt zusätzlich brandhemmend, AGDW). Angesetzt: 25 % Reduktion des Waldbrand"
            "risikos in den gemanagten Zellen. Editierbare, dokumentierte Modellannahme."),
        "benefit_per_m2_year": ("Modellannahme (erhaltener Waldwert)", ["TEEB_DE_Naturkapital"],
            "Direkter Zusatznutzen: anteiliger Werterhalt von Holzvorrat und Waldfunktionen "
            "auch ohne Brandereignis (Versicherbarkeit, kontinuierliche Ökosystemleistung; "
            "TEEB DE). 0,01 €/(m²·a) = 100 €/ha·a — von zuvor 1 €/m² (= 10.000 €/ha, "
            "unplausibel) herabgesetzt; editierbar."),
    },
    "HABITAT_CONNECTIVITY": {
        "default_reduction": ("BfN-Biotopverbund-Prinzip", ["TEEB_DE_Naturkapital"],
            "Wirkmechanismus: Biotopverbund (Trittsteine, Korridore, Hecken) ermöglicht Arten "
            "das Ausweichen und Nachwandern bei Klimastress — fragmentierte Populationen "
            "sterben lokal aus, vernetzte können sich verschieben (Kernargument des bundes"
            "weiten Biotopverbunds nach § 21 BNatSchG). Angesetzt: 20 % Reduktion der "
            "verknüpften Biodiversitäts-/Fragmentierungsrisiken in den vernetzten Zellen. "
            "Editierbare, dokumentierte Modellannahme."),
        "benefit_per_m2_year": ("TEEB DE (Leistungen vernetzter Flächen)", ["TEEB_DE_Naturkapital"],
            "Direkter Zusatznutzen: Verbundstrukturen (Hecken, Säume) liefern Bestäubung, "
            "Schädlingsregulation, Windschutz und Erosionsminderung für angrenzende Nutz"
            "flächen (TEEB DE). 0,02 €/(m²·a) = 200 €/ha·a der Verbundfläche — von zuvor "
            "1,5 €/m² (= 15.000 €/ha, unplausibel) herabgesetzt; editierbar."),
    },
    # ── Fischerei/Aquakultur & Anreizprogramme ──────────────────────────────────
    "ADAPTIVE_FISHERIES_MANAGEMENT": {
        "default_reduction": ("Modellannahme (Befischungsdruck als Stellhebel)", [],
            "Wirkmechanismus: Unter Wärme-/Sauerstoffstress ist der Befischungsdruck der am "
            "schnellsten steuerbare Stressor — angepasste Fangquoten, Schonzeiten in Hitze"
            "phasen und Echtzeit-Monitoring senken die Gesamtbelastung der Bestände und "
            "sichern die Reproduktion. Angesetzt: 20 % Reduktion des Bestandsstress-/Ertrags"
            "risikos im bewirtschafteten Gebiet. Keine Kalibrierstudie — editierbare, "
            "dokumentierte Modellannahme."),
    },
    "AQUACULTURE_RESILIENCE_SYSTEMS": {
        "default_reduction": ("Modellannahme (Technik gegen O₂-/Hitzeverluste)", [],
            "Wirkmechanismus: Belüfter, Sauerstoffeintrag, Beschattung/Kühlung und Sensorik "
            "verhindern die typischen Sommerverluste in Teich-/Kreislaufanlagen (Sauerstoff"
            "mangel und Temperaturspitzen sind die Hauptschadensursachen der Aquakultur in "
            "Hitzejahren). Angesetzt: 25 % Reduktion des Aquakultur-Schadensrisikos in den "
            "ausgerüsteten Anlagenzellen. Editierbare, dokumentierte Modellannahme."),
        "opex_per_unit_year": ("VDI 2067 + Energie (Belüftung/Sensorik)", ["VDI_2067_Blatt1"],
            "Belüfter/Pumpen/Sensorik laufen im Sommer dauerhaft: Wartung nach VDI-2067-"
            "Größenordnung plus erheblicher Stromverbrauch → ~6-8 % der Investition/Jahr; "
            "Punktwert 4.000 €/(Anlage·a) bei 60.000 € Investition."),
    },
    "FISHERIES_SPAWNING_HABITAT_RESTORATION": {
        "default_reduction": ("UBA/LfU (Laichhabitat-Renaturierung)", ["UBA_Gewaesserrenaturierung", "LfU_Bayern_Fischaufstieg"],
            "Wirkmechanismus: Wiederhergestellte Kieslaichplätze, Flachwasser- und Beschattungs"
            "zonen erhöhen Reproduktionserfolg und bieten Temperatur-Refugien — Renaturierung "
            "ist der Kernhebel der WRRL-Programme für klimastabile Fischbestände (UBA/LfU). "
            "Angesetzt: 22 % Reduktion des Bestandsstressrisikos in den renaturierten "
            "Gewässerzellen. Editierbare Modellannahme im belegten Wirkprinzip."),
        "benefit_per_m2_year": ("TEEB/UBA (Gewässer-Ökosystemleistungen)", ["TEEB_DE_Naturkapital", "UBA_Gewaesserrenaturierung"],
            "Direkter Zusatznutzen: renaturierte Gewässerabschnitte liefern Selbstreinigung, "
            "Habitat- und Erholungsleistungen (TEEB DE/UBA). 0,02 €/(m²·a) = 200 €/ha·a der "
            "renaturierten Fläche — von zuvor 2 €/m² (= 20.000 €/ha, unplausibel) "
            "herabgesetzt; editierbar."),
    },
    "FISHERIES_WATER_QUALITY_PROTECTION": {
        "default_reduction": ("Modellannahme (O₂-Haushalt in Warmphasen)", ["UBA_Gewaesserrenaturierung"],
            "Wirkmechanismus: Warmes Wasser hält weniger Sauerstoff — Nährstoff- und "
            "Einleitungsmanagement (Uferrandstreifen, Kläranlagen-Feinsteuerung, Einleit"
            "stopps in Hitzephasen) senkt die Sauerstoffzehrung genau dann, wenn die Bestände "
            "am verwundbarsten sind. Angesetzt: 20 % Reduktion der verknüpften Gewässergüte-/"
            "Bestandsrisiken. Editierbare, dokumentierte Modellannahme."),
    },
    "FISH_PASSAGE_RESTORATION": {
        "default_reduction": ("LfU Bayern (Durchgängigkeit/Ausweichwanderung)", ["LfU_Bayern_Fischaufstieg"],
            "Wirkmechanismus: Durchgängige Gewässer ermöglichen Fischen die Ausweichwanderung "
            "in kühlere, sauerstoffreichere Ober-/Nebenläufe während Hitze- und Niedrigwasser"
            "phasen — ohne Durchgängigkeit kollabieren eingeschlossene Populationen in "
            "aufgeheizten Stauräumen (LfU-Praxishandbuch Fischaufstieg; WRRL-Kernmaßnahme). "
            "Angesetzt: 22 % Reduktion des Bestandsstressrisikos im wieder angebundenen "
            "Gewässersystem. Editierbare Modellannahme."),
        "opex_per_unit_year": ("LfU/VDI 2067 (Unterhaltung Fischaufstieg)", ["LfU_Bayern_Fischaufstieg", "VDI_2067_Blatt1"],
            "Fischaufstiegsanlagen brauchen laufende Unterhaltung (Geschwemmsel-Räumung, "
            "Kontrolle der Leitströmung, Funktionsmonitoring nach LfU-Handbuch): VDI-2067-"
            "Größenordnung ~1,5 % der Investition/Jahr → 3.000 €/(Anlage·a) bei 200.000 €."),
    },
    "PREVENTION_INCENTIVES": {
        "default_reduction": ("Modellannahme (Anreizprogramm, Teilnahmequote)", ["BBK_Hochwasserschutzfibel"],
            "Wirkmechanismus: Förder-/Prämienanreize aktivieren private Eigenvorsorge "
            "(Objektschutz, Elementarversicherung — Maßnahmen der BBK-Fibel), aber nur bei "
            "einem Teil der Eigentümer (Teilnahmequoten und Mitnahmeeffekte begrenzen die "
            "Wirkung). Angesetzt: 12 % Reduktion der verknüpften Gebäudeschadensrisiken — "
            "bewusst der niedrigste Wert aller Maßnahmen (indirekter Wirkpfad). Editierbare, "
            "dokumentierte Modellannahme."),
    },
    "RISK_BASED_INVESTMENTS": {
        "default_reduction": ("Modellannahme (risikobasierte Priorisierung)", [],
            "Wirkmechanismus: Risikobasierte Investitionsplanung lenkt begrenzte kommunale "
            "Mittel dorthin, wo je Euro die größte Schadensminderung entsteht (Priorisierung "
            "nach Risikokarten statt Gießkanne) — die Wirkung entsteht indirekt über besser "
            "platzierte Folgeinvestitionen. Angesetzt: 15 % Reduktion der verknüpften Risiken "
            "im priorisierten Gebiet. Keine Kalibrierstudie — editierbare, dokumentierte "
            "Modellannahme."),
    },
}


def _enrich_measure_effect_docs() -> None:
    """Verdrahtet die zentralen Wirkungs-/Nutzen-Herleitungen in die Maßnahmen-Dicts.

    Inline gepflegte ``sources``/``source_details``/``source_refs`` je Maßnahme haben
    Vorrang; hier wird nur ergänzt, was dort fehlt.
    """
    for m in MEASURES:
        fields = _MEASURE_EFFECT_DOCS.get(m["code"])
        if not fields:
            continue
        sources_map = m.setdefault("sources", {})
        details = m.setdefault("source_details", {})
        refs_map = m.setdefault("source_refs", {})
        for field, (label, refs, text) in fields.items():
            sources_map.setdefault(field, label)
            details.setdefault(field, text)
            if refs and field not in refs_map:
                refs_map[field] = refs


_enrich_measure_effect_docs()


# ── Kategorisierung (Karten-Layerspalte: Zwischenebene) ──────────────────────────
# Geordnete Kategorie-Definitionen + Zuordnung je Code. Die Felder werden unten in
# die H/E/V/Maßnahmen-Dicts injiziert, sodass /catalog sie automatisch mitliefert.

HAZARD_CATEGORIES: list[dict] = [
    {"code": "temp", "label": "Hitze & Temperatur"},
    {"code": "drought", "label": "Trockenheit & Wasserarmut"},
    {"code": "flood", "label": "Starkregen & Hochwasser"},
    {"code": "storm", "label": "Sturm & Wind"},
    {"code": "coast", "label": "Küste & Meer"},
    {"code": "soil", "label": "Boden & Kryosphäre"},
    {"code": "fire", "label": "Brände"},
    {"code": "compound", "label": "Verbund & Kaskade"},
]

EXPOSURE_CATEGORIES: list[dict] = [
    {"code": "people", "label": "Bevölkerung & Gesundheit"},
    {"code": "building", "label": "Gebäude & Siedlung"},
    {"code": "infra", "label": "Kritische Infrastruktur"},
    {"code": "economy", "label": "Wirtschaft"},
    {"code": "nature", "label": "Land & Natur"},
    {"code": "water", "label": "Wasser & Küste"},
]

VULNERABILITY_CATEGORIES: list[dict] = [
    {"code": "technical", "label": "Bauliche & technische"},
    {"code": "social", "label": "Soziale & Gesundheit"},
    {"code": "watersoil", "label": "Wasser & Boden"},
    {"code": "nature", "label": "Natur & Ökosysteme"},
    {"code": "economy", "label": "Wirtschaft"},
    {"code": "governance", "label": "Governance & Vorsorge"},
    {"code": "fisheries", "label": "Fischerei"},
]

# KAnG-Cluster mit Handlungsfeldern (Reihenfolge wie im Gesetz)
KANG_CLUSTERS: list[dict] = [
    {"code": "infrastructure", "label": "Infrastruktur", "fields": [
        {"code": "energy", "label": "Energieinfrastruktur"},
        {"code": "buildings", "label": "Gebäude"},
        {"code": "transport", "label": "Verkehr und Verkehrsinfrastruktur"},
    ]},
    {"code": "land", "label": "Land und Landnutzung", "fields": [
        {"code": "biodiversity", "label": "Biologische Vielfalt"},
        {"code": "soil", "label": "Boden"},
        {"code": "agriculture", "label": "Landwirtschaft"},
        {"code": "forestry", "label": "Wald und Forstwirtschaft"},
    ]},
    {"code": "health", "label": "Menschliche Gesundheit und Pflege", "fields": [
        {"code": "health", "label": "Gesundheit und Pflege"},
    ]},
    {"code": "urban", "label": "Stadtentwicklung, Raumplanung & Bevölkerungsschutz", "fields": [
        {"code": "civil_protection", "label": "Bevölkerungs- und Katastrophenschutz"},
        {"code": "spatial_planning", "label": "Raumplanung"},
        {"code": "urban_dev", "label": "Stadt- und Siedlungsentwicklung"},
    ]},
    {"code": "water", "label": "Wasser", "fields": [
        {"code": "fisheries", "label": "Fischerei"},
        {"code": "coastal", "label": "Küsten- und Meeresschutz"},
        {"code": "water_management", "label": "Wasserhaushalt und Wasserwirtschaft"},
    ]},
    {"code": "economy", "label": "Wirtschaft", "fields": [
        {"code": "finance", "label": "Finanzwirtschaft"},
        {"code": "industry", "label": "Industrie und Gewerbe"},
    ]},
    {"code": "crosscutting", "label": "Übergreifende Handlungsfelder", "fields": [
        {"code": "general", "label": "Übergreifend"},
    ]},
]

_HAZARD_CATEGORY_MAP: dict[str, str] = {
    "MEAN_TEMPERATURE_RISE": "temp", "HEAT_WAVE": "temp", "COLD_EXTREME": "temp",
    "SURFACE_WATER_HEATING": "temp", "OCEAN_WARMING": "temp",
    "DROUGHT": "drought", "SOIL_MOISTURE_DECLINE": "drought", "LOW_FLOW_NIEDRIGWASSER": "drought",
    "HEAVY_RAIN_FLOOD": "flood", "LANDSLIDE": "flood",
    "EXTRATROPICAL_STORM": "storm", "TROPICAL_CYCLONE": "storm",
    "SEA_LEVEL_RISE": "coast", "STORM_SURGE": "coast", "COASTAL_EROSION": "coast",
    "SALTWATER_INTRUSION": "coast", "OCEAN_ACIDIFICATION": "coast",
    "SOIL_SALINIZATION": "soil", "GLACIER_SNOW_LOSS": "soil", "PERMAFROST_THAW": "soil",
    "WILDFIRE": "fire",
    "COMPOUND_EVENT": "compound", "CASCADE_EVENT": "compound",
}

_EXPOSURE_CATEGORY_MAP: dict[str, str] = {
    "POPULATION_DENSITY": "people", "AGE_STRUCTURE": "people",
    "OUTDOOR_THERMAL_EXPOSURE": "people", "VULNERABLE_GROUPS_POPULATION": "people",
    "BUILDING_STOCK": "building", "BUILDING_USE_TYPES": "building", "LOCATION_HAZARD_ZONES": "building",
    "ENERGY_INFRASTRUCTURE": "infra", "WATER_WASTEWATER_INFRA": "infra",
    "TRANSPORT_HUBS": "infra", "COMMUNICATION_INFRA": "infra",
    "HEALTHCARE_INFRASTRUCTURE": "people",
    "INDUSTRIAL_COMMERCIAL_AREAS": "economy", "SUPPLY_CHAIN_NODES": "economy",
    "AGRICULTURAL_LAND": "nature", "FOREST_AREA": "nature",
    "BIODIVERSITY_HOTSPOTS": "nature", "EROSION_PRONE_SOILS": "nature",
    "COASTAL_RIPARIAN_ZONES": "water", "FLOODPLAINS": "water",
    "COASTAL_STORM_SURGE_EXPOSURE": "water", "GROUNDWATER_DEPENDENT_ECOSYSTEMS": "water",
    "FISHERIES_AQUACULTURE_AREAS": "water", "FISH_SPAWNING_HABITATS": "water",
}

_VULNERABILITY_CATEGORY_MAP: dict[str, str] = {
    "BUILDING_STABILITY": "technical", "CRITICAL_INFRA_CONDITION": "technical",
    "MATERIAL_HEAT_SENSITIVITY": "technical", "INFRA_CRITICALITY": "technical",
    "REDUNDANCY_BACKUP": "technical", "INFRA_DEPENDENCY_CHAIN": "technical",
    "SEALING_DEGREE": "technical", "UHI_INTENSITY": "technical", "GREEN_SPACE_SHARE": "technical",
    "VULNERABLE_GROUPS_SHARE": "social", "INCOME_SOCIAL_RESILIENCE": "social",
    "HEALTHCARE_ACCESS": "social", "HEAT_SENSITIVITY": "social",
    "AIR_QUALITY_RISK": "social", "DISEASE_VECTOR_SUSCEPTIBILITY": "social",
    "GROUNDWATER_DEPENDENCY": "watersoil", "WATER_STRESS_INDEX": "watersoil",
    "IRRIGATION_DEPENDENCY": "watersoil", "EROSION_SUSCEPTIBILITY": "watersoil",
    "SOIL_SENSITIVITY": "watersoil", "LEVEE_CONDITION": "watersoil",
    "SALTWATER_INTRUSION_RISK": "watersoil",
    "BIODIVERSITY_RESILIENCE": "nature", "WILDFIRE_SUSCEPTIBILITY": "nature",
    "SINGLE_SITE_DEPENDENCY": "economy", "SUPPLY_CHAIN_DEPENDENCY": "economy",
    "FINANCIAL_ADAPTATION_CAPACITY": "economy",
    "EARLY_WARNING_SYSTEMS": "governance", "EMERGENCY_MANAGEMENT": "governance",
    "PLANNING_IMPLEMENTATION_CAPACITY": "governance",
    "FISHERIES_TEMPERATURE_SENSITIVITY": "fisheries",
    "AQUACULTURE_TECHNICAL_VULNERABILITY": "fisheries",
    "FISHERIES_MANAGEMENT_CAPACITY": "fisheries",
}

# Maßnahme → (KAnG-Cluster, Handlungsfeld)
_MEASURE_KANG_MAP: dict[str, tuple[str, str]] = {
    "GRID_REINFORCEMENT_REDUNDANCY": ("infrastructure", "energy"),
    "HEAT_RESISTANT_PLANT_COOLING": ("infrastructure", "energy"),
    "DECENTRALIZED_ENERGY_PV_STORAGE": ("infrastructure", "energy"),
    "GREEN_ROOFS_FACADES": ("infrastructure", "buildings"),
    "FLOOD_PROTECTION_BUILDING": ("infrastructure", "buildings"),
    "COOL_ROOFS": ("infrastructure", "buildings"),
    "HEAT_RESILIENT_PAVEMENT": ("infrastructure", "transport"),
    "CRITICAL_NODE_PROTECTION": ("infrastructure", "transport"),
    "HABITAT_CONNECTIVITY": ("land", "biodiversity"),
    "EROSION_PROTECTION": ("land", "soil"),
    "HUMUS_BUILDUP": ("land", "soil"),
    "DROUGHT_RESISTANT_VARIETIES": ("land", "agriculture"),
    "WATER_STORAGE_EFFICIENT_IRRIGATION": ("land", "agriculture"),
    "MIXED_FORESTS": ("land", "forestry"),
    "WILDFIRE_PREVENTION": ("land", "forestry"),
    "HEAT_ACTION_PLANS": ("health", "health"),
    "COOLING_ROOMS_DRINKING_WATER": ("health", "health"),
    "DRINKING_FOUNTAINS": ("health", "health"),
    "EARLY_WARNING_MEASURE": ("urban", "civil_protection"),
    "EVACUATION_EMERGENCY_PLANS": ("urban", "civil_protection"),
    "BUILDING_BANS_RISK_ZONES": ("urban", "spatial_planning"),
    "FRESH_AIR_CORRIDORS": ("urban", "spatial_planning"),
    "URBAN_GREEN": ("urban", "urban_dev"),
    "SPONGE_CITY": ("urban", "urban_dev"),
    "DESEALING_SURFACE": ("urban", "urban_dev"),
    "PUBLIC_SHADE_WATER": ("urban", "urban_dev"),
    "ADAPTIVE_FISHERIES_MANAGEMENT": ("water", "fisheries"),
    "FISH_PASSAGE_RESTORATION": ("water", "fisheries"),
    "AQUACULTURE_RESILIENCE_SYSTEMS": ("water", "fisheries"),
    "FISHERIES_SPAWNING_HABITAT_RESTORATION": ("water", "fisheries"),
    "FISHERIES_WATER_QUALITY_PROTECTION": ("water", "fisheries"),
    "LEVEE_REINFORCEMENT": ("water", "coastal"),
    "SALTWATER_BARRIERS": ("water", "coastal"),
    "DRAINAGE_SWALES": ("water", "water_management"),
    "FLOODPLAIN_RENATURATION": ("water", "water_management"),
    "RETENTION_STORAGE": ("water", "water_management"),
    "RETENTION_POLDER_RESERVOIR": ("water", "water_management"),
    "INFILTRATION_AREAS": ("water", "water_management"),
    "RUNOFF_ROUTING_DGM": ("water", "water_management"),
    "GROUNDWATER_RECHARGE": ("water", "water_management"),
    "LEAKAGE_REDUCTION": ("water", "water_management"),
    "RISK_BASED_INVESTMENTS": ("economy", "finance"),
    "PREVENTION_INCENTIVES": ("economy", "finance"),
    "INDUSTRIAL_COOLING_CONCEPTS": ("economy", "industry"),
    "SUPPLY_CHAIN_RESILIENCE": ("economy", "industry"),
    "VULNERABLE_GROUP_PROGRAMS": ("crosscutting", "general"),
    "HEAT_WORK_SCHEDULES": ("crosscutting", "general"),
}

# Felder injizieren (in-place), damit /catalog die Kategorien automatisch ausgibt.
for _h in HAZARDS:
    _h["category"] = _HAZARD_CATEGORY_MAP.get(_h["code"], "compound")
for _e in EXPOSURES:
    _e["category"] = _EXPOSURE_CATEGORY_MAP.get(_e["code"], "people")
for _v in VULNERABILITIES:
    _v["category"] = _VULNERABILITY_CATEGORY_MAP.get(_v["code"], "technical")
for _m in MEASURES:
    _cluster, _field = _MEASURE_KANG_MAP.get(_m["code"], ("crosscutting", "general"))
    _m["kang_cluster"] = _cluster
    _m["kang_field"] = _field


from app.data.catalog_auxiliary import AUXILIARY, AUXILIARY_CATEGORIES, AUXILIARY_BY_CODE

# ── Lookups ──────────────────────────────────────────────────────────────────────

HAZARDS_BY_CODE = {h["code"]: h for h in HAZARDS}
EXPOSURES_BY_CODE = {e["code"]: e for e in EXPOSURES}
VULNERABILITIES_BY_CODE = {v["code"]: v for v in VULNERABILITIES}
RISKS_BY_CODE = {r["code"]: r for r in RISKS}
MEASURES_BY_CODE = {m["code"]: m for m in MEASURES}

INDICATOR_BY_CODE = {
    **HAZARDS_BY_CODE,
    **EXPOSURES_BY_CODE,
    **VULNERABILITIES_BY_CODE,
    **AUXILIARY_BY_CODE,
}


def normalize_value(code: str, value: float) -> float:
    """Normalisiert einen absoluten H/E/V-Wert auf 0..1 anhand der Referenzskala.

    Wird AUSSCHLIESSLICH für die Risikoberechnung verwendet.
    """
    meta = INDICATOR_BY_CODE.get(code)
    if not meta:
        return 0.0
    lo = float(meta.get("norm_min", 0.0))
    hi = float(meta.get("norm_max", 1.0))
    if hi <= lo:
        return 0.0
    x = (float(value) - lo) / (hi - lo)
    return max(0.0, min(1.0, x))


def group_label(code: str) -> str:
    for g in KWRA_GROUPS:
        if g["code"] == code:
            return g["label"]
    return code


# ── Modellversion ────────────────────────────────────────────────────────────────
# Wird bei strukturellen Modelländerungen (Risiko-Set, Kostensätze, Aggregation)
# erhöht. Der Layer-Cache stempelt seine Dateien mit dieser Version und invalidiert
# automatisch, wenn sich die Version ändert (siehe services/layer_cache.py).
# 2026.08-m0-95rev7: Integration Methodik #95 Rev. 7 (YLL × VOLY, empirische
# Wochenquantile, v_vers, c_kal 0,581, Morbidität r_0,a × HD-Term) — invalidiert
# Layer-Caches, die den alten Todesfall-/VSL-Stand materialisiert haben.
MODEL_VERSION = "2026.08-m0-95rev7"
