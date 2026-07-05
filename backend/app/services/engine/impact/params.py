"""Registry-Spezifikation der Schicht-B-Impact-Parameter (editierbar, override-fähig).

Reine Datenstruktur: ``parameter_registry`` baut daraus die Registry-Einträge mit den
IDs ``risks.<CODE>.impact.<key>`` (risikospezifisch) bzw. ``impact.<key>`` (global) und
löst ``source_refs`` gegen ``sources.py`` auf. So erscheinen die Parameter automatisch in
der Konfigurations-UI (Gruppe Klimarisiken), im Parameter-Excel und im Info-Tooltip —
ohne dass ``impact/*`` die Registry importieren muss (Zyklus-Vermeidung).

Jeder Eintrag: {risk (Code oder ""), key, value, label, unit, source, source_detail,
source_refs}. Die Defaults sind auf publizierte Größenordnungen kalibrierte, editierbare
Modellparameter (RKI/Winklmayr 2022; UBA MK3.1; GDV/BBK; Prognos 2023).
"""

from __future__ import annotations

_HEAT_AF = ("Nichtlineare attributable Fraktion AF = 1−exp(−β·(Hitzetage−Schwelle)+). "
            "β und Schwelle kalibriert auf die RKI-/Winklmayr-Größenordnung (~20 Hitzetage → "
            "~1 % hitzeattributable Sterblichkeit; ~4.500–8.700 Hitzetote/Jahr in DE).")

IMPACT_PARAM_SPECS: list[dict] = [
    # ── Hitzemortalität ─────────────────────────────────────────────────────────
    {"risk": "EXPECTED_ANNUAL_MORTALITY", "key": "baseline_mort_per_100k", "value": 1130.0,
     "label": "Basissterblichkeit", "unit": "Tote/100k·a",
     "source": "Destatis / RKI (Größenordnung rohe Sterberate)",
     "source_detail": "Rohe Sterberate in DE ~11/1.000/Jahr; auf diese Basis wird die "
                      "hitzeattributable Fraktion angewandt (Outcome = Bevölkerung · "
                      "Basissterblichkeit/100k · AF · g(V̂)).",
     "source_refs": ["RKI_Hitzemortalitaet"]},
    {"risk": "EXPECTED_ANNUAL_MORTALITY", "key": "beta_per_hotday", "value": 0.0008,
     "label": "AF-Steigung je Hitzetag", "unit": "1/Hitzetag",
     "source": "RKI JoHM S4/2023 (Winklmayr u. a. 2022)", "source_detail": _HEAT_AF,
     "source_refs": ["RKI_Hitzemortalitaet"]},
    {"risk": "EXPECTED_ANNUAL_MORTALITY", "key": "hotday_threshold", "value": 8.0,
     "label": "Hitzetage-Schwelle", "unit": "Hitzetage/Jahr",
     "source": "RKI JoHM S4/2023 (Winklmayr u. a. 2022)",
     "source_detail": "Schwelle, ab der Hitzetage zur Exzessmortalität beitragen "
                      "(Akklimatisierungsniveau). Editierbar.",
     "source_refs": ["RKI_Hitzemortalitaet"]},

    # ── Hitzemorbidität ─────────────────────────────────────────────────────────
    {"risk": "EXPECTED_ANNUAL_MORBIDITY", "key": "rate_per_100k", "value": 8000.0,
     "label": "Basis-Morbiditätsrate", "unit": "Fälle/100k·a",
     "source": "UBA MK3.1 / RKI (Modellannahme)",
     "source_detail": "Basisrate hitzeassoziierter Behandlungsfälle je 100k; die attributable "
                      "Fraktion (Hitzetage) reduziert sie auf die klimabedingten Fälle. "
                      "Dokumentierte, editierbare Modellannahme.",
     "source_refs": ["RKI_Hitzemortalitaet"]},
    {"risk": "EXPECTED_ANNUAL_MORBIDITY", "key": "beta_per_hotday", "value": 0.0016,
     "label": "AF-Steigung je Hitzetag", "unit": "1/Hitzetag", "source": "RKI/Winklmayr",
     "source_detail": _HEAT_AF, "source_refs": ["RKI_Hitzemortalitaet"]},
    {"risk": "EXPECTED_ANNUAL_MORBIDITY", "key": "hotday_threshold", "value": 8.0,
     "label": "Hitzetage-Schwelle", "unit": "Hitzetage/Jahr", "source": "RKI/Winklmayr",
     "source_detail": "Akklimatisierungsschwelle für hitzeassoziierte Morbidität.",
     "source_refs": ["RKI_Hitzemortalitaet"]},

    # ── Verletzte (Flut/Sturm/Hangrutsch) ───────────────────────────────────────
    {"risk": "EXPECTED_ANNUAL_INJURIES", "key": "rate_per_100k", "value": 150.0,
     "label": "Verletztenrate je Ereignisintensität", "unit": "Verletzte/100k",
     "source": "GDV/BBK (Modellannahme)",
     "source_detail": "Verletzte je 100k Einwohner bei voller (normierter) Flut-/Sturm-/"
                      "Hangrutsch-Intensität; skaliert linear mit der Hazard-Intensität der Zelle.",
     "source_refs": ["BBK_Hochwasserschutzfibel", "Prognos_Klimaschaeden_2023"]},

    # ── Psychische Gesundheit ───────────────────────────────────────────────────
    {"risk": "EXPECTED_ANNUAL_MENTAL_HEALTH", "key": "rate_per_100k", "value": 1500.0,
     "label": "Basisrate psychischer Fälle", "unit": "Fälle/100k·a",
     "source": "RKI / UBA (Modellannahme)",
     "source_detail": "Basisrate klimaassoziierter psychischer Belastungsfälle je 100k; "
                      "Treiber = Hitze-AF plus Extremereignis-/Kaskadenanteil. Editierbar.",
     "source_refs": ["RKI_Hitzemortalitaet"]},
    {"risk": "EXPECTED_ANNUAL_MENTAL_HEALTH", "key": "beta_per_hotday", "value": 0.0012,
     "label": "AF-Steigung je Hitzetag", "unit": "1/Hitzetag", "source": "RKI/Winklmayr",
     "source_detail": _HEAT_AF, "source_refs": ["RKI_Hitzemortalitaet"]},
    {"risk": "EXPECTED_ANNUAL_MENTAL_HEALTH", "key": "hotday_threshold", "value": 10.0,
     "label": "Hitzetage-Schwelle", "unit": "Hitzetage/Jahr", "source": "Modellannahme",
     "source_detail": "Schwelle für den hitzegetriebenen Anteil psychischer Belastung.",
     "source_refs": ["RKI_Hitzemortalitaet"]},

    # ── Betroffene / Evakuierte ─────────────────────────────────────────────────
    {"risk": "EXPECTED_ANNUAL_AFFECTED_EVACUATED", "key": "rate_per_100k", "value": 2500.0,
     "label": "Betroffenenrate je Ereignisintensität", "unit": "Personen/100k",
     "source": "BBK / Prognos (Modellannahme)",
     "source_detail": "Betroffene/evakuierte Personen je 100k bei voller (normierter) Flut-/"
                      "Sturmflut-/Feuerintensität der Zelle. Editierbar.",
     "source_refs": ["BBK_Hochwasserschutzfibel", "Prognos_Klimaschaeden_2023"]},

    # ── Wärmebelastungsstunden ──────────────────────────────────────────────────
    {"risk": "EXPECTED_THERMAL_STRESS_HOURS", "key": "hours_ref_per_100k", "value": 400.0,
     "label": "Belastungsstunden bei Referenz-Hitze", "unit": "Stunden/Jahr je 100k",
     "source": "UBA MK3.1 (Modellannahme)",
     "source_detail": "Wärmebelastungsstunden je 100k Einwohner bei den Referenz-Hitzetagen; "
                      "skaliert linear mit den Zell-Hitzetagen.",
     "source_refs": ["RKI_Hitzemortalitaet"]},
    {"risk": "EXPECTED_THERMAL_STRESS_HOURS", "key": "reference_hotdays", "value": 20.0,
     "label": "Referenz-Hitzetage", "unit": "Hitzetage/Jahr", "source": "DWD/Modellannahme",
     "source_detail": "Bezugsniveau der Hitzetage, bei dem die Referenz-Belastungsstunden gelten.",
     "source_refs": ["DWD_CDC_Starkregen"]},

    # ── Schadstoff-Belastungsstunden ────────────────────────────────────────────
    {"risk": "EXPECTED_POLLUTANT_EXPOSURE_HOURS", "key": "hours_ref_per_100k", "value": 250.0,
     "label": "Schadstoffstunden bei Referenz-Hitze", "unit": "Stunden/Jahr je 100k",
     "source": "UBA (Modellannahme)",
     "source_detail": "Schadstoff-Belastungsstunden (bodennahes Ozon/Feinstaub) je 100k bei "
                      "Referenz-Hitzetagen; Ozonbildung korreliert mit Hitze.",
     "source_refs": ["RKI_Hitzemortalitaet"]},
    {"risk": "EXPECTED_POLLUTANT_EXPOSURE_HOURS", "key": "reference_hotdays", "value": 20.0,
     "label": "Referenz-Hitzetage", "unit": "Hitzetage/Jahr", "source": "DWD/Modellannahme",
     "source_detail": "Bezugsniveau der Hitzetage für die Referenz-Schadstoffstunden.",
     "source_refs": ["DWD_CDC_Starkregen"]},

    # ── Monetäre Sektorschäden: max. Jahresverlustrate je Risiko (Schicht B §6.2) ──
    {"risk": "EXPECTED_BUILDING_DAMAGE_EUR", "key": "max_loss_rate", "value": 0.008,
     "label": "Max. Jahresverlustrate", "unit": "Anteil/a", "source": "GDV/Prognos (Modellannahme)",
     "source_detail": "Anteil des Gebäude-Assetwerts, der bei voller Hazard-Intensität "
                      "jährlich als Schaden anfällt; über die konvexe Schadenskurve mit der "
                      "Intensität skaliert.", "source_refs": ["Prognos_Klimaschaeden_2023"]},
    {"risk": "EXPECTED_TRANSPORT_DAMAGE_EUR", "key": "max_loss_rate", "value": 0.02,
     "label": "Max. Jahresverlustrate", "unit": "Anteil/a", "source": "Prognos (Modellannahme)",
     "source_detail": "Verlustrate des Verkehrsasset-Ersatzwerts bei voller Intensität.",
     "source_refs": ["Prognos_Klimaschaeden_2023"]},
    {"risk": "EXPECTED_ENERGY_INFRA_DAMAGE_EUR", "key": "max_loss_rate", "value": 0.02,
     "label": "Max. Jahresverlustrate", "unit": "Anteil/a", "source": "Prognos/dena (Modellannahme)",
     "source_detail": "Verlustrate des Energieasset-Ersatzwerts bei voller Intensität.",
     "source_refs": ["Prognos_Klimaschaeden_2023"]},
    {"risk": "EXPECTED_TELECOM_DAMAGE_EUR", "key": "max_loss_rate", "value": 0.02,
     "label": "Max. Jahresverlustrate", "unit": "Anteil/a", "source": "Prognos (Modellannahme)",
     "source_detail": "Verlustrate des Telekom-Asset-Ersatzwerts bei voller Intensität.",
     "source_refs": ["Prognos_Klimaschaeden_2023"]},
    {"risk": "EXPECTED_WATER_WASTEWATER_DAMAGE_EUR", "key": "max_loss_rate", "value": 0.015,
     "label": "Max. Jahresverlustrate", "unit": "Anteil/a", "source": "Prognos/DWA (Modellannahme)",
     "source_detail": "Verlustrate des Ver-/Entsorgungsasset-Ersatzwerts bei voller Intensität.",
     "source_refs": ["Prognos_Klimaschaeden_2023"]},
    {"risk": "EXPECTED_AGRICULTURAL_DAMAGE_EUR", "key": "max_loss_rate", "value": 0.15,
     "label": "Max. Ertragsverlustrate", "unit": "Anteil/a", "source": "Prognos/StatBA (Modellannahme)",
     "source_detail": "Anteil des Ertragswerts je ha, der bei voller Dürre-/Hitzeintensität "
                      "verloren geht.", "source_refs": ["Prognos_Klimaschaeden_2023"]},
    {"risk": "EXPECTED_SOIL_LOSS_DEGRADATION_EUR", "key": "max_loss_rate", "value": 0.01,
     "label": "Max. Jahresverlustrate", "unit": "Anteil/a", "source": "Prognos (Modellannahme)",
     "source_detail": "Anteil des Bodenwerts je ha, der bei voller Erosionsintensität jährlich "
                      "degradiert.", "source_refs": ["Prognos_Klimaschaeden_2023"]},
    {"risk": "EXPECTED_ECOSYSTEM_SERVICE_LOSS", "key": "max_loss_rate", "value": 0.08,
     "label": "Max. Leistungsverlustrate", "unit": "Anteil/a", "source": "TEEB-DE (Modellannahme)",
     "source_detail": "Anteil der jährlichen Ökosystemleistung je ha, der bei voller "
                      "Degradationsintensität verloren geht.", "source_refs": ["TEEB_DE_Naturkapital"]},
    {"risk": "EXPECTED_FISHERIES_ECONOMIC_LOSS_EUR", "key": "max_loss_rate", "value": 0.20,
     "label": "Max. Ertragsverlustrate", "unit": "Anteil/a", "source": "Modellannahme",
     "source_detail": "Anteil des Fischereiwerts je Gewässer-ha bei voller Wärme-/"
                      "Niedrigwasserintensität.", "source_refs": ["Prognos_Klimaschaeden_2023"]},
    {"risk": "EXPECTED_AQUACULTURE_DAMAGE_EUR", "key": "max_loss_rate", "value": 0.25,
     "label": "Max. Ertragsverlustrate", "unit": "Anteil/a", "source": "Modellannahme",
     "source_detail": "Anteil des Aquakulturwerts je Gewässer-ha bei voller Wärme-/"
                      "Niedrigwasserintensität.", "source_refs": ["Prognos_Klimaschaeden_2023"]},
    {"risk": "EXPECTED_CLIMATE_MIGRATION_COSTS_EUR", "key": "cost_ref_per_100k", "value": 400_000.0,
     "label": "Referenz-Migrationskosten je 100k", "unit": "€/Jahr je 100k",
     "source": "Prognos (Modellannahme)",
     "source_detail": "Klimabedingte Umsiedlungs-/Verdrängungskosten je 100k Einwohner bei "
                      "voller (normierter) Küsten-/Flut-/Dürreintensität. In DE geringe, aber "
                      "ausgewiesene Größenordnung.", "source_refs": ["Prognos_Klimaschaeden_2023"]},

    # ── Umwelt-Flächen-/Artenverlust (Schicht B §6.4) ───────────────────────────
    {"risk": "EXPECTED_BIODIVERSITY_LOSS", "key": "species_loss_per_ha", "value": 0.0006,
     "label": "Artenverlustrate je ha", "unit": "Arten/ha·a", "source": "BfN/UBA (Modellannahme)",
     "source_detail": "Lokal verlorene Arten je ha Naturfläche bei voller Intensität "
                      "(Wärme/Dürre/Feuer); über den Kostensatz (€/Art) monetarisiert.",
     "source_refs": ["TEEB_DE_Naturkapital"]},
    {"risk": "EXPECTED_HABITAT_LOSS", "key": "loss_rate", "value": 0.02,
     "label": "Habitatverlustrate", "unit": "ha/ha·a", "source": "BfN (Modellannahme)",
     "source_detail": "Anteil der exponierten Naturfläche, der bei voller Intensität "
                      "(Dürre/Feuer/Meeresspiegel) jährlich als Habitat verloren geht.",
     "source_refs": ["TEEB_DE_Naturkapital"]},
    {"risk": "EXPECTED_SOIL_DEGRADATION", "key": "loss_rate", "value": 0.03,
     "label": "Bodendegradationsrate", "unit": "ha/ha·a", "source": "BGR/UBA (Modellannahme)",
     "source_detail": "Anteil der Ackerfläche, der bei voller Intensität (Dürre/Erosion/"
                      "Versalzung) jährlich degradiert.", "source_refs": ["TEEB_DE_Naturkapital"]},
    {"risk": "EXPECTED_VEGETATION_DAMAGE", "key": "loss_rate", "value": 0.05,
     "label": "Vegetationsschadensrate", "unit": "ha/ha·a", "source": "Waldzustandsbericht (Modellannahme)",
     "source_detail": "Anteil der Wald-/Agrarfläche mit Vegetationsschaden bei voller "
                      "Intensität (Dürre/Hitze/Feuer).", "source_refs": ["TEEB_DE_Naturkapital"]},
]

# Globale Schicht-B-Parameter (ID ``impact.<key>``): Assetwerte, Konsolidierungsfaktoren,
# Kurvenexponent. Editier- und override-fähig, in der Registry unter Kategorie "impact".
IMPACT_GLOBAL_SPECS: list[dict] = [
    {"key": "building_value_eur_m2", "value": 2000.0, "label": "Gebäudewert je m² BGF",
     "unit": "€/m²", "source": "Destatis Baupreise / GDV (Größenordnung)",
     "source_detail": "Wiederherstellungswert je m² Bruttogeschossfläche; multipliziert mit "
                      "der geschätzten Geschossfläche der Zelle (Bebauungsgrad × Fläche × Geschosse).",
     "source_refs": ["Prognos_Klimaschaeden_2023"]},
    {"key": "transport_asset_value_eur", "value": 500_000.0, "label": "Ersatzwert Verkehrsknoten",
     "unit": "€/Stück", "source": "Prognos (Modellannahme)",
     "source_detail": "Mittlerer Ersatzwert je Verkehrsknoten (OSM-Zählung je Zelle).",
     "source_refs": ["Prognos_Klimaschaeden_2023"]},
    {"key": "energy_asset_value_eur", "value": 800_000.0, "label": "Ersatzwert Energieanlage",
     "unit": "€/Stück", "source": "Prognos/dena (Modellannahme)",
     "source_detail": "Mittlerer Ersatzwert je Energieanlage (OSM-KRITIS-Zählung je Zelle).",
     "source_refs": ["Prognos_Klimaschaeden_2023"]},
    {"key": "telecom_asset_value_eur", "value": 400_000.0, "label": "Ersatzwert Telekom-Anlage",
     "unit": "€/Stück", "source": "Prognos (Modellannahme)",
     "source_detail": "Mittlerer Ersatzwert je Kommunikationsanlage je Zelle.",
     "source_refs": ["Prognos_Klimaschaeden_2023"]},
    {"key": "water_asset_value_eur", "value": 600_000.0, "label": "Ersatzwert Wasseranlage",
     "unit": "€/Stück", "source": "Prognos/DWA (Modellannahme)",
     "source_detail": "Mittlerer Ersatzwert je Ver-/Entsorgungsanlage je Zelle.",
     "source_refs": ["Prognos_Klimaschaeden_2023"]},
    {"key": "agri_value_eur_ha", "value": 12_000.0, "label": "Agrar-Ertragswert je ha",
     "unit": "€/ha", "source": "StatBA Agrar (Größenordnung)",
     "source_detail": "Ertrags-/Bodenwert je ha landwirtschaftlicher Fläche.",
     "source_refs": ["Prognos_Klimaschaeden_2023"]},
    {"key": "soil_value_eur_ha", "value": 30_000.0, "label": "Bodenwert je ha",
     "unit": "€/ha", "source": "BGR/Modellannahme",
     "source_detail": "Bodenwert je ha (Wiederherstellung/Bodenfunktion) für Erosions-/"
                      "Degradationsschäden.", "source_refs": ["Prognos_Klimaschaeden_2023"]},
    {"key": "esl_value_eur_ha", "value": 3000.0, "label": "Ökosystemleistungswert je ha·a",
     "unit": "€/ha·a", "source": "TEEB-DE / Grunewald",
     "source_detail": "Jährlicher Wert der Ökosystemleistungen je ha Wald-/Grünfläche.",
     "source_refs": ["TEEB_DE_Naturkapital"]},
    {"key": "fisheries_value_eur_ha", "value": 5000.0, "label": "Fischerei-/Aquakulturwert je ha·a",
     "unit": "€/ha·a", "source": "Modellannahme",
     "source_detail": "Jährlicher Ertragswert je ha Gewässer-/Aquakulturfläche.",
     "source_refs": ["Prognos_Klimaschaeden_2023"]},
    {"key": "k_indirect", "value": 0.25, "label": "k_indirekt (Folgekosten-Multiplikator)",
     "unit": "Anteil", "source": "Prognos 2023 (I/O-Analyse)",
     "source_detail": "Indirekte Verluste (Betriebs-/Lieferkettenunterbrechung, Standort, "
                      "verzögerte Schäden) als Anteil der DIREKTEN Sektorschäden — konsolidiert "
                      "die früher einzeln (doppelt) gezählten Folgekosten-Risiken. Band ~0,18–0,5.",
     "source_refs": ["Prognos_Klimaschaeden_2023"]},
    {"key": "restoration_share", "value": 0.15, "label": "Restaurierungsquote",
     "unit": "Anteil", "source": "Modellannahme",
     "source_detail": "Wiederherstellungskosten als Anteil der direkten Sektorschäden. "
                      "Teilkennzahl (Teilmenge) — NICHT additiv in die Gesamtsumme.",
     "source_refs": ["Prognos_Klimaschaeden_2023"]},
    {"key": "damage_exponent", "value": 1.5, "label": "Schadenskurven-Exponent",
     "unit": "–", "source": "HOWAS21/JRC (Größenordnung)",
     "source_detail": "Konvexität der Schadenskurve (Schaden ∝ Intensität^Exponent). >1 = "
                      "überproportionaler Schaden bei hoher Intensität (Tiefe-Schaden-Kurven).",
     "source_refs": ["Prognos_Klimaschaeden_2023"]},
]
