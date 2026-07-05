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
]
