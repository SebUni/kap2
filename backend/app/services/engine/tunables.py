"""Modellweite Stellschrauben (Single Source) + Registry-Specs für "model"/"regional".

Bisher lagen diese Werte als verstreute Literale in der Engine (risk_engine, sanity,
measure_service, risk_zone_service, inputs). Hier sind sie zentralisiert und über die
Parameter-Registry editier-/override-fähig (IDs ``model.<key>`` bzw. ``regional.<key>``).

Wichtig: Die ``effective_*``-Helfer lesen den Override zur LAUFZEIT — Aufrufer müssen
also innerhalb eines gültigen Override-Kontexts laufen (``set_overrides`` im
Assessment-Lauf bzw. ``override_scope`` in Request-Pfaden).

Bewusste Abgrenzung (keine Parameter):
- ``CELL_AREA_KM2``/``CELL_AREA_M2`` (physische Rastergröße, keine Annahme),
- die "je 100k"-Divisoren der Schicht-B-Raten in ``impact/health.py`` und
  ``impact/monetary.py`` — dort ist "je 100.000" Teil der EINHEIT des jeweiligen
  Ratenparameters (wie "Prozent"), nicht die Kalibrier-Referenz. Eine Kopplung an
  ``model.ref_population`` würde die Einheiten-Labels dieser Parameter falsch machen.
"""

from __future__ import annotations

from app.services.engine.override_context import get_override

# ── Defaults (Single Source für Engine-Importe) ────────────────────────────────
REF_POPULATION_DEFAULT = 100_000.0   # Referenzbevölkerung der ref_value-Kalibrierung
REF_AREA_KM2_DEFAULT = 50.0          # Referenzfläche der area-skalierten ref_values
RISK_THRESHOLD_DEFAULT = 50.0        # Index-Schwelle "Risikozone"
MEASURE_COVERAGE_SATURATION_DEFAULT = 1.5   # Sättigungsfaktor Flächendeckung
MEASURE_REDUCTION_CAP_DEFAULT = 0.95        # Obergrenze Risikoreduktion je Zelle


def effective_ref_population() -> float:
    return float(get_override("model.ref_population", REF_POPULATION_DEFAULT))


def effective_ref_area_km2() -> float:
    return float(get_override("model.ref_area_km2", REF_AREA_KM2_DEFAULT))


def effective_risk_threshold() -> float:
    return float(get_override("model.risk_threshold", RISK_THRESHOLD_DEFAULT))


def effective_measure_saturation() -> float:
    return float(get_override("model.measure_coverage_saturation",
                              MEASURE_COVERAGE_SATURATION_DEFAULT))


def effective_measure_reduction_cap() -> float:
    return float(get_override("model.measure_reduction_cap", MEASURE_REDUCTION_CAP_DEFAULT))


def regional_fallback(key: str, default: float) -> float:
    """Override-fähiger regionaler Proxy-/Fallback-Wert (ID ``regional.<key>``)."""
    return float(get_override(f"regional.{key}", default))


# ── Registry-Specs: Kategorie "model" ──────────────────────────────────────────
# Felder wie in impact/params.py: key/value/label/unit/source/source_detail/source_refs.
MODEL_PARAM_SPECS: list[dict] = [
    {"key": "ref_population", "value": REF_POPULATION_DEFAULT,
     "label": "Referenzbevölkerung (ref_value-Kalibrierung)", "unit": "Einwohner",
     "source": "Modellkonvention (je-100.000-EW-Referenz, dokumentiert)",
     "source_detail": "Die Referenzwerte (ref_value) bevölkerungsskalierter Risiken sind als "
        "Outcome einer 100.000-Einwohner-Referenzkommune kalibriert — angelehnt an die "
        "epidemiologische Berichtskonvention \"je 100.000 Einwohner\" (RKI/Destatis) und die "
        "je-100k-Größenordnungen der KWRA/Prognos-Schadensstudien. Wirkungsorte: "
        "Legacy-/flat-Outcome-Skalierung (risk_engine._scale_factor), €-Bewertung flat-"
        "skalierter Ausfallrisiken (risk_engine, §8/B6) und Sanity-Anker (impact/sanity.py). "
        "Eine Änderung reskaliert alle daraus abgeleiteten Outcomes invers (halbe Referenz = "
        "doppeltes Outcome je Einwohner) — primär Transparenz-, kein Tuning-Parameter. "
        "Bewusst NICHT gekoppelt: Schicht-B-Raten mit fester Einheit \"je 100k\" "
        "(z. B. Basissterblichkeit) — dort ist je-100k Teil der Einheit.",
     "source_refs": ["RKI_Hitzemortalitaet", "UBA_KWRA_2021"]},
    {"key": "ref_area_km2", "value": REF_AREA_KM2_DEFAULT,
     "label": "Referenzfläche (ref_value-Kalibrierung)", "unit": "km²",
     "source": "Modellkonvention (Referenz-Flächenkommune, dokumentiert)",
     "source_detail": "Referenzfläche, auf die flächenskalierte ref_values kalibriert sind "
        "(Outcome = ref_value · Fläche/50 km²). Größenordnung einer mittleren deutschen "
        "Flächenkommune: Bundesfläche ~357.600 km² auf ~10.750 Gemeinden ≈ 33 km² im Mittel "
        "(Median kleiner, Flächengemeinden deutlich größer); 50 km² als runder Referenzwert. "
        "Wirkungsorte wie bei der Referenzbevölkerung (risk_engine._scale_factor, sanity).",
     "source_refs": ["Zensus_2022"]},
    {"key": "risk_threshold", "value": RISK_THRESHOLD_DEFAULT,
     "label": "Risikozonen-Schwelle", "unit": "Index",
     "source": "Modellwahl (Screening-Schwelle, dokumentiert)",
     "source_detail": "Zellen mit Risikoindex ≥ Schwelle gelten als Risikozone "
        "(Connected-Component-Cluster in risk_zone_service) und zählen in die Kennzahl "
        "share_above_threshold des Aggregats. Herleitung: mit der Umstellung der Index-"
        "Komposition auf die Max-Wirkungskette (MODELL_KRITIK §3.1) liegen Indizes ~Faktor "
        "1,5–2 höher als beim früheren gewichteten Mittel; die Schwelle wurde von 40 auf 50 "
        "angehoben, um dasselbe reale Belastungsniveau zu markieren. Wirkt live (keine "
        "Neuberechnung), Risikozonen werden beim nächsten Abruf neu geclustert.",
     "source_refs": []},
    {"key": "measure_coverage_saturation", "value": MEASURE_COVERAGE_SATURATION_DEFAULT,
     "label": "Sättigungsfaktor Flächendeckung (Maßnahmen)", "unit": "–",
     "source": "Modellwahl (abnehmender Grenznutzen, dokumentiert)",
     "source_detail": "Für Maßnahmen mit coverage_scaling=\"saturating\" gilt "
        "r = Risikoreduktion · min(1; Deckungsgrad · Faktor): Die volle Wirkung ist bereits "
        "bei 1/1,5 ≈ 67 % Flächendeckung erreicht. Bildet den abnehmenden Grenznutzen von "
        "System-/Netzwerkmaßnahmen ab (z. B. Netzredundanz, Frühwarnung: Wirkung entsteht "
        "aus der Systemabdeckung, nicht aus dem letzten Flächenprozent). Dokumentierte "
        "Modellwahl, editierbar; 1,0 = strikt proportionale Wirkung.",
     "source_refs": []},
    {"key": "measure_reduction_cap", "value": MEASURE_REDUCTION_CAP_DEFAULT,
     "label": "Obergrenze Risikoreduktion je Zelle (Maßnahmen)", "unit": "Anteil",
     "source": "Modellwahl (Restrisiko-Prinzip, dokumentiert)",
     "source_detail": "Kappung der kombinierten Wirkung je Zelle und Maßnahme auf maximal "
        "95 % Indexreduktion: Kein Maßnahmenmix eliminiert ein Klimarisiko vollständig "
        "(Restrisiko-Konzept der Klimaanpassung, vgl. IPCC-AR6-Begriff residual risk). "
        "Verhindert zugleich, dass extreme Parameter-Kombinationen (hohe default_reduction × "
        "Mehrfach-Wirkungsziele) ein Risiko rechnerisch auf 0 stellen.",
     "source_refs": ["IPCC_AR6_WG1"]},
]

# ── Registry-Specs: Kategorie "regional" (Proxy-/Fallback-Klimatreiber) ────────
# Diese Werte greifen NUR, wenn keine echten ortsaufgelösten Daten vorliegen bzw. als
# dokumentierte Proxy-Kalibrierung; welche Quelle je Kommune tatsächlich gezogen hat,
# zeigt die provenance im Kartentooltip (inputs.build_regional_context).
_REGIONAL_NOTE = (" Greift nur als Fallback/Proxy, wenn keine echten Daten vorliegen — "
                  "die tatsächliche Herkunft je Kommune zeigt die Provenienz im Kartentooltip.")

REGIONAL_FALLBACK_SPECS: list[dict] = [
    {"key": "storm_days", "value": 6.0,
     "label": "Fallback: Sturmtage pro Jahr", "unit": "Tage/Jahr",
     "source": "DWD-Größenordnung (Binnenland) / Fallback ohne ERA5-Raster",
     "source_detail": "Tage mit Windspitzen ≥ 8 Bft: im norddeutschen Binnenland ~5–10, in "
        "süddeutschen Becken ~2–5, an der Küste deutlich mehr (DWD-Klimastatusberichte). "
        "6 Tage/Jahr als Bundesmittel-Fallback, wenn kein ERA5-Sturmtage-Raster vorliegt "
        "(provenance \"regional_constant\" statt \"era5\")." + _REGIONAL_NOTE,
     "source_refs": ["DWD_Klimastatusbericht", "ERA5_C3S"]},
    {"key": "sea_level_rise", "value": 4.5,
     "label": "Fallback: Meeresspiegelanstieg (Küste)", "unit": "mm/Jahr",
     "source": "IPCC AR6 / Nordsee-Pegeltrends (Größenordnung)",
     "source_detail": "Globaler mittlerer Meeresspiegelanstieg zuletzt ~4,5 mm/Jahr "
        "(Satellitenaltimetrie 2013–2022, IPCC AR6/WMO); Nordsee-Pegeltrends liegen bei "
        "~2–4 mm/Jahr mit Beschleunigung. 4,5 mm/Jahr als vorsorgeorientierter Wert für "
        "Küstenkommunen (SEA_LEVEL_RISE-Hazard; Binnenkommunen: 0)." + _REGIONAL_NOTE,
     "source_refs": ["IPCC_AR6_WG1"]},
    {"key": "glacier_loss_rate", "value": 0.5,
     "label": "Gletscherschwund-Rate", "unit": "%/Jahr",
     "source": "Größenordnung bayerischer Gletscherberichte (konservativ)",
     "source_detail": "Die verbliebenen deutschen Alpengletscher verlieren aktuell grob "
        "1–3 % Fläche/Volumen pro Jahr (Bayerischer Gletscherbericht; starke Jahres-"
        "schwankungen). 0,5 %/Jahr als konservativer Modellwert; wirkt nur auf Zellen mit "
        "OSM natural=glacier und ist für fast alle Kommunen irrelevant." + _REGIONAL_NOTE,
     "source_refs": []},
    {"key": "heavy_rain_base", "value": 40.0,
     "label": "Proxy: Starkregenindex-Basis", "unit": "Index",
     "source": "Kalibrierung auf DWD-CDC-Starkregenraster (Fallback-Proxy)",
     "source_detail": "Fallback, wenn keine DWD-CDC-Raster (Tage ≥ 20/30 mm) am Zentroid "
        "vorliegen: Index = Basis + (Jahresmitteltemp − 9,5 °C) · Steigung. Die Basis 40 ist "
        "auf die echte Rasterauswertung kalibriert: DE-typisch ~8 Tage ≥ 20 mm + ~2 Tage "
        "≥ 30 mm ergeben Index ≈ 44." + _REGIONAL_NOTE,
     "source_refs": ["DWD_CDC_Starkregen"]},
    {"key": "heavy_rain_slope", "value": 4.0,
     "label": "Proxy: Starkregenindex-Steigung je °C", "unit": "Index/°C",
     "source": "Clausius-Clapeyron-Größenordnung (Proxy-Kalibrierung)",
     "source_detail": "Wärmere Luft hält ~7 %/K mehr Wasserdampf (Clausius-Clapeyron), "
        "Starkregenintensitäten steigen entsprechend bis überproportional (DWD/IPCC). Im "
        "Temperatur-Proxy wird das als +4 Indexpunkte je °C Abweichung von 9,5 °C "
        "Jahresmittel abgebildet." + _REGIONAL_NOTE,
     "source_refs": ["IPCC_AR6_WG1", "DWD_CDC_Starkregen"]},
    {"key": "mean_temp_rise_base", "value": 1.6,
     "label": "Basis-Temperaturanstieg Deutschland", "unit": "°C",
     "source": "DWD Klimareport / Monitoringbericht (beobachteter Anstieg)",
     "source_detail": "Deutschland hat sich gegenüber der vorindustriellen Referenz bereits "
        "um ~1,6–1,7 °C erwärmt (DWD, lineares Trendmittel Stand ~2022/23). Der Zellwert "
        "MEAN_TEMPERATURE_RISE nutzt diese Basis, moduliert um ±0,1 °C je °C Abweichung der "
        "regionalen Jahresmitteltemperatur von 9,5 °C plus UHI-Beitrag." + _REGIONAL_NOTE,
     "source_refs": ["DWD_Klimareport"]},
    {"key": "dry_index_divisor", "value": 25.0,
     "label": "Trockenheitsindex-Divisor (heiße Tage)", "unit": "Tage",
     "source": "Normierungskonvention (DWD-Spannbreite heißer Tage)",
     "source_detail": "Der dimensionslose Trockenheitsindex normiert die heißen Tage: "
        "dry_index = min(1; heiße Tage / 25). 25+ heiße Tage/Jahr markieren die maximal "
        "trockenheits-/hitzegeprägten Regionen Deutschlands (Oberrheingraben in Extremjahren "
        "~20–30 heiße Tage, DWD-CDC-Rasterklimatologie)." + _REGIONAL_NOTE,
     "source_refs": ["DWD_CDC_Rasterklimatologie"]},
    {"key": "drought_base", "value": 8.0,
     "label": "Proxy: Trockentage-Basis", "unit": "Tage",
     "source": "Modellannahme (Basis-Trockenperioden, Proxy)",
     "source_detail": "Basisniveau der Trockentage (drought_days = Basis + 1,2 · heiße "
        "Tage): auch ohne Hitzetage treten in Deutschland Trockenperioden in der "
        "Größenordnung ~1–2 Wochen/Jahr auf (längste Trockenperioden im DWD-Monitoring). "
        "Proxy-Kalibrierung, editierbar." + _REGIONAL_NOTE,
     "source_refs": ["DWD_Klimastatusbericht"]},
    {"key": "drought_factor", "value": 1.2,
     "label": "Proxy: Trockentage-Faktor je heißem Tag", "unit": "–",
     "source": "Modellannahme (Hitze-Trockenheits-Kopplung, Proxy)",
     "source_detail": "Kopplung der Trockentage an die heißen Tage (drought_days = 8 + "
        "1,2 · heiße Tage): sommerliche Hochdrucklagen erzeugen Hitze- und Trockenphasen "
        "gemeinsam; Regionen mit vielen heißen Tagen weisen im DWD-Monitoring auch die "
        "höchsten Trockenheitskennzahlen auf. Proxy-Kalibrierung, editierbar." + _REGIONAL_NOTE,
     "source_refs": ["DWD_Klimastatusbericht"]},
    {"key": "share_over_65", "value": 22.0,
     "label": "Fallback: Anteil Bevölkerung ≥ 65 Jahre", "unit": "%",
     "source": "Zensus 2022 / Destatis (Bundesmittel)",
     "source_detail": "Bundesweiter Anteil der Bevölkerung ab 65 Jahren ~22 % (Zensus 2022/"
        "Destatis-Fortschreibung). Greift je Zelle nur, wenn weder Zensus-Gitterdaten noch "
        "regionale Demografiewerte vorliegen; Eingang in AGE_STRUCTURE und vulnerable "
        "Gruppen." + _REGIONAL_NOTE,
     "source_refs": ["Zensus_2022"]},
    {"key": "share_under_18", "value": 18.0,
     "label": "Fallback: Anteil Bevölkerung < 18 Jahre", "unit": "%",
     "source": "Zensus 2022 / Destatis (Bundesmittel)",
     "source_detail": "Bundesweiter Anteil der Bevölkerung unter 18 Jahren ~17–18 % "
        "(Zensus 2022/Destatis). Greift je Zelle nur ohne Zensus-Gitter-/Regionaldaten; "
        "Eingang in AGE_STRUCTURE und vulnerable Gruppen." + _REGIONAL_NOTE,
     "source_refs": ["Zensus_2022"]},
]
