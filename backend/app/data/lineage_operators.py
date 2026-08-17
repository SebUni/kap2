"""Operator-Schritte für Herkunftsdiagramme (Zellwerte + Formeln).

Einheitliches Beschreibungskonzept — jeder Operator gehört zu genau einer
Klasse (``op_kind``) mit festem Formulierungs-Template:

======================  =============================================  =========================================
Klasse                  Bedeutung                                      Titel-/Notiz-Muster
======================  =============================================  =========================================
``count``               Objekte zählen                                 "{Objekte} zählen" / "Anzahl der {Objekte} in der Zelle."
``ratio``               Verhältnis/Anteil bilden                       "{X}-Anteil berechnen" / "Berechnung: {Zähler} / {Nenner}"
``neighbor``            Auswertung der 8 Nachbarzellen                 "{X} der Nachbarzellen" / Satz + Berechnung
``distance``            reine Distanzmessung                           "Distanz messen" / "Entfernung zu {Ziel} in Metern."
``distance_score``      Distanz → Nähe-Score 0…1                       "Nähe-Score berechnen" / "Wandelt die Entfernung zu {Ziel} in einen Score 0…1 um; …"
``mean``                Mittelwertbildung                              "{Größe} mitteln" / "Mittelwert der {Größe} über {Objekte} der Zelle."
``lookup``              externer Rohwert ohne Verrechnung              "Regionalwert abrufen" bzw. "Rasterwert übernehmen" / Satz
``constant``            fester Platzhalterwert ohne Ortsauflösung      "Konstantwert übernehmen" / Satz benennt den Wert ausdrücklich als Platzhalter/Modellannahme
``derived_index``       abgeleiteter Spezialindex (Geometrie/Modell)   "{Größe} ableiten" / methodenspezifischer Satz
``weighted_sum``        benanntes Modell mit gewichteten Termen        Modellname / Satz + $$Formel$$
``add``/``multiply``/…  arithmetische Verkettung                       Symbol als Label / "Berechnung: …" bzw. $$Formel$$
======================  =============================================  =========================================

Der Autorentext liegt unter ``note``; der finale Tooltip (Titel + Notiz +
maschinell erzeugter "Eingaben:"-Zeile) wird zentral in
``lineage_graph._enrich_tooltips`` komponiert. Die Datenquelle (OSM/DWD/…)
steht deshalb NICHT redundant in der Notiz — sie erscheint automatisch in
der Eingaben-Zeile; genannt werden nur Details darüber hinaus (Tags,
Produkte, Schwellen).
"""

from __future__ import annotations

from typing import Any

OperatorStep = dict[str, Any]

# ── Zell-Ebene: Berechnungsschritte vor Zwischenwert-Knoten ─────────────────

CELL_OPERATORS: dict[str, list[OperatorStep]] = {
    # — Klasse count: Objekte zählen —
    "bldg_count": [{
        "op_kind": "count",
        "label": "Gebäude zählen",
        "note": "Anzahl der Gebäude-Polygone in der Zelle.",
    }],
    "energy_infra_count": [{
        "op_kind": "weighted_sum",
        "label": "Energie-Kritikalität gewichten",
        "note": ("Gewichtete Kritikalitätspunkte mit Sättigung: stärkstes Asset voll, "
                 "Restsumme zu 50 % (w_max + 0,5·(Σ w·n − w_max)). Umspannwerke/Kraftwerke "
                 "hoch, Leitungen je kV-Klasse pro Zellquerung, Masten/Tragwerke = 0 "
                 "(Bestandteil der Leitung, keine Doppelzählung)."),
    }],
    "water_wastewater_count": [{
        "op_kind": "weighted_sum",
        "label": "Wasser-Kritikalität gewichten",
        "note": ("Gewichtete Kritikalitätspunkte mit Sättigung (stärkstes Asset voll, "
                 "Restsumme zu 50 %); Kläranlage/Wasserwerk hoch, Pumpwerk/Speicher niedriger."),
    }],
    "communication_count": [{
        "op_kind": "weighted_sum",
        "label": "Kommunikations-Kritikalität gewichten",
        "note": ("Gewichtete Kritikalitätspunkte mit Sättigung (stärkstes Asset voll, "
                 "Restsumme zu 50 %); Rechenzentrum/Vermittlung hoch, Mobilfunkmast/"
                 "Antenne niedriger."),
    }],
    "transport_hub_count": [{
        "op_kind": "weighted_sum",
        "label": "Verkehrsknoten-Kritikalität gewichten",
        "note": ("Gewichtete Kritikalitätspunkte mit Sättigung (stärkstes Asset voll, "
                 "Restsumme zu 50 %); Bahnhof hoch, Haltepunkt/ÖPNV-Station niedriger."),
    }],
    "energy_infra_classes": [{
        "op_kind": "count",
        "label": "Energieanlagen je Klasse zählen",
        "note": ("Anzahl der OSM-Energieobjekte je Anlagenklasse (Umspannwerk, "
                 "Kraftwerk, Leitung je kV-Klasse …) in der Zelle."),
    }],
    "water_wastewater_classes": [{
        "op_kind": "count",
        "label": "Wasseranlagen je Klasse zählen",
        "note": "Anzahl der Wasser-/Abwasseranlagen je Anlagenklasse in der Zelle.",
    }],
    "communication_classes": [{
        "op_kind": "count",
        "label": "Kommunikationsanlagen je Klasse zählen",
        "note": "Anzahl der Kommunikationsanlagen je Anlagenklasse in der Zelle.",
    }],
    "transport_hub_classes": [{
        "op_kind": "count",
        "label": "Verkehrsknoten je Klasse zählen",
        "note": "Anzahl der Verkehrsknoten je Anlagenklasse in der Zelle.",
    }],

    # — Klasse ratio: Anteil an der Zellfläche bzw. an einer Bezugsmenge —
    "bldg_cov": [{
        "op_kind": "ratio",
        "label": "Gebäude-Anteil berechnen",
        "note": "Berechnung: Gebäudegrundrissfläche / Zellfläche",
    }],
    "road_cov": [{
        "op_kind": "ratio",
        "label": "Straßen-Anteil berechnen",
        "note": "Berechnung: Straßenfläche / Zellfläche",
    }],
    "imp_lu": [{
        "op_kind": "ratio",
        "label": "Versiegelungs-Anteil berechnen",
        "note": ("Versiegelung aus den Landnutzungsklassen der Zelle.\n"
                 "Berechnung: versiegelte Landnutzungsfläche / Zellfläche"),
    }],
    "green_frac": [{
        "op_kind": "ratio",
        "label": "Grünflächen-Anteil berechnen",
        "note": ("Wiesen, Parks und Gärten der Zelle.\n"
                 "Berechnung: Grünfläche / Zellfläche"),
    }],
    "forest_frac": [{
        "op_kind": "ratio",
        "label": "Wald-Anteil berechnen",
        "note": "Berechnung: Waldfläche / Zellfläche",
    }],
    "farmland_frac": [{
        "op_kind": "ratio",
        "label": "Acker-Anteil berechnen",
        "note": ("Landwirtschaftliche Nutzflächen der Zelle.\n"
                 "Berechnung: Ackerfläche / Zellfläche"),
    }],
    "water_frac": [{
        "op_kind": "ratio",
        "label": "Wasserflächen-Anteil berechnen",
        "note": ("Berechnung: Wasserfläche / Zellfläche\n"
                 "Angehoben auf Mindestwerte aus Nachbar-Wasseranteil (×0,5) und "
                 "Gewässernähe-Score (×0,3), damit Uferzellen nicht auf 0 fallen."),
    }],
    "canopy_frac": [{
        "op_kind": "ratio",
        "label": "Baumkronen-Anteil berechnen",
        "note": "Berechnung: Baumkronenfläche / Zellfläche",
    }],
    "glacier_frac": [{
        "op_kind": "ratio",
        "label": "Gletscher-Anteil berechnen",
        "note": "Berechnung: Gletscherfläche / Zellfläche",
    }],
    "share_over_65": [{
        "op_kind": "lookup",
        "label": "Rasterwert übernehmen",
        "note": ("Anteil der Personen ≥ 65 Jahre, direkt aus dem Zensus-Raster "
                 "übernommen (Feld AnteilUeber65) — keine eigene Berechnung."),
    }],
    "share_under_18": [{
        "op_kind": "lookup",
        "label": "Rasterwert übernehmen",
        "note": ("Anteil der Personen < 18 Jahre, direkt aus dem Zensus-Raster "
                 "übernommen (Feld AnteilUnter18) — keine eigene Berechnung."),
    }],
    "owner_share": [{
        "op_kind": "lookup",
        "label": "Rasterwert übernehmen",
        "note": ("Eigentümerquote der Zelle, direkt aus dem Zensus-Raster "
                 "übernommen (Feld Eigentuemerquote) — keine eigene Berechnung."),
    }],

    # — Klasse neighbor: Auswertung der 8 Nachbarzellen —
    "water_adj": [{
        "op_kind": "max",
        "label": "Maximum",
        "note": ("Kombinierte Gewässernähe der Zelle.\n"
                 "Berechnung: max(Wasseranteil der 8 Nachbarzellen; "
                 "Gewässernähe-Score; Wasseranteil der Zelle)"),
    }],
    "vent_score": [{
        "op_kind": "neighbor",
        "label": "Anteil offener Nachbarzellen",
        "note": ("Frischluftzufuhr aus dem Umfeld.\n"
                 "Berechnung: offene oder grüne Nachbarzellen / 8 Nachbarn"),
    }],

    # — Klasse distance: reine Distanzmessung —
    "dist_hospital_m": [{
        "op_kind": "distance",
        "label": "Distanz messen",
        "note": "Entfernung zum nächsten Krankenhaus in Metern.",
    }],
    "dist_doctor_m": [{
        "op_kind": "distance",
        "label": "Distanz messen",
        "note": "Entfernung zur nächsten Arztpraxis oder Klinik in Metern.",
    }],
    "dist_pharmacy_m": [{
        "op_kind": "distance",
        "label": "Distanz messen",
        "note": "Entfernung zur nächsten Apotheke in Metern.",
    }],

    # — Klasse distance_score: Distanz → Score 0…1 —
    "water_prox": [{
        "op_kind": "distance_score",
        "label": "Nähe-Score berechnen",
        "note": ("Wandelt die Entfernung zum nächsten echten Gewässer in einen "
                 "Nähe-Score 0…1 um; 0 = weit entfernt, 1 = direkt benachbart.\n"
                 "Berechnung: max(0; 1 − Distanz / 500 m)\n"
                 "Entwässerungsgräben (ditch/drain) zählen nicht als echtes "
                 "Gewässer, sondern liefern nur einen sehr schwachen, über die "
                 "Grabendichte der Zelle skalierten Zusatzbeitrag."),
    }],
    "healthcare_access_score": [{
        "op_kind": "weighted_sum",
        "label": "Erreichbarkeit gewichten",
        "note": ("Gewichtete Summe der Nähe-Scores zur nächsten Einrichtung "
                 "je Typ; Nähe = max(0; 1 − effektive Distanz / Maximaldistanz), "
                 "Distanzen mit Straßenumweg-Faktor.\n"
                 "Berechnung: 0,50 · Nähe Krankenhaus + 0,35 · Nähe Arzt "
                 "+ 0,15 · Nähe Apotheke"),
    }],
    "dyke_prox": [{
        "op_kind": "distance_score",
        "label": "Nähe-Score berechnen",
        "note": ("Wandelt die Entfernung zu Deich- und Küstenschutzanlagen in einen "
                 "Nähe-Score 0…1 um; 0 = weit entfernt, 1 = direkt benachbart."),
    }],
    "emergency_access_score": [{
        "op_kind": "distance_score",
        "label": "Nähe-Score berechnen",
        "note": ("Wandelt die Entfernung zu Feuerwehr und Rettungsdiensten in einen "
                 "Erreichbarkeits-Score 0…1 um; 0 = weit entfernt, "
                 "1 = direkt benachbart."),
    }],

    # — Klasse mean: Mittelwertbildung —
    "avg_height": [{
        "op_kind": "mean",
        "label": "Gebäudehöhe mitteln",
        "note": ("Flächengewichteter Mittelwert der Gebäudehöhe (Gewicht = "
                 "Grundriss∩Zelle); Höhen aus amtlichen LoD2-Modellen "
                 "(measuredHeight), wo verfügbar, sonst OSM-Heuristik."),
    }],
    "mean_elevation_m": [{
        "op_kind": "mean",
        "label": "Geländehöhe mitteln",
        "note": "Mittelwert der Geländehöhe über die Höhenrasterpunkte der Zelle.",
    }],
    "building_age_mean": [{
        "op_kind": "mean",
        "label": "Mittleres Baujahr ableiten",
        "note": ("Gebäudegewichtetes Mittel der Klassenmitten aus den "
                 "Zensus-Baujahrsklassen der Zelle; Zellen mit Gebäuden, aber "
                 "ohne Baujahrsangabe (Zensus-Datenschutz) werden aus der "
                 "umgebenden 1-km-Zelle imputiert."),
    }],
    "net_cold_rent": [{
        "op_kind": "lookup",
        "label": "Rasterwert übernehmen",
        "note": ("Mittlere Nettokaltmiete je m², direkt aus dem Zensus-Raster "
                 "übernommen (Feld durchschnMieteQM) — der Mittelwert stammt "
                 "von Destatis, keine eigene Berechnung."),
    }],
    "living_area_per_person": [{
        "op_kind": "lookup",
        "label": "Rasterwert übernehmen",
        "note": ("Mittlere Wohnfläche je Bewohner, direkt aus dem Zensus-Raster "
                 "übernommen (Feld durchschnFlaechejeBew) — der Mittelwert "
                 "stammt von Destatis, keine eigene Berechnung."),
    }],

    # — Klasse lookup: externer Rohwert ohne weitere Verrechnung —
    "pop": [{
        "op_kind": "lookup",
        "label": "Rasterwert übernehmen",
        "note": ("Einwohnerzahl direkt aus dem Zensus-Raster übernommen — das "
                 "Berechnungsgitter ist deckungsgleich mit dem 100-m-Zensusgitter."),
    }],
    "area_km2": [{
        "op_kind": "lookup",
        "label": "Rasterwert übernehmen",
        "note": "Zellfläche in km² aus der Rastergeometrie: 100 × 100 m.",
    }],
    "area_m2": [{
        "op_kind": "lookup",
        "label": "Rasterwert übernehmen",
        "note": "Zellfläche in m² aus der Rastergeometrie: 100 × 100 m.",
    }],
    "hot_days": [{
        "op_kind": "lookup",
        "label": "Regionalwert abrufen",
        "note": ("Anzahl heißer Tage ≥ 30 °C pro Jahr aus dem DWD-CDC-Raster "
                 "(1 km) am Kommune-Zentroid; Fallback Bundesland-Mittel. "
                 "Gilt für alle Zellen gleich."),
    }],
    "frost_days": [{
        "op_kind": "lookup",
        "label": "Regionalwert abrufen",
        "note": ("Anzahl Frosttage pro Jahr aus dem DWD-CDC-Raster am "
                 "Kommune-Zentroid; Fallback Proxy aus der Jahresmitteltemperatur. "
                 "Gilt für alle Zellen gleich."),
    }],
    "heavy_rain_index": [{
        "op_kind": "lookup",
        "label": "Regionalwert abrufen",
        "note": ("Starkregen-Häufigkeit aus DWD-CDC-Rastern am Kommune-Zentroid.\n"
                 "Berechnung: min(100; Tage ≥ 20 mm · 4 + Tage ≥ 30 mm · 6)\n"
                 "Ohne Rasterwert Fallback-Proxy aus der Jahresmitteltemperatur."),
    }],
    "storm_days": [{
        "op_kind": "lookup",
        "label": "Regionalwert abrufen",
        "note": ("Sturmtage pro Jahr (Böen ≥ 25 m/s) aus dem ERA5-Raster am "
                 "Kommune-Zentroid; ohne Raster regionaler Konstantwert "
                 "(editierbarer Fallback)."),
    }],
    "mean_temp": [{
        "op_kind": "lookup",
        "label": "Regionalwert abrufen",
        "note": "Jahresmitteltemperatur der Region (DWD-Gebietsmittel des Bundeslands).",
    }],
    "glacier_loss_rate": [{
        "op_kind": "lookup",
        "label": "Regionalwert abrufen",
        "note": "Gletscherschwund-Rate der Region.",
    }],
    "snow_decline_rate_pct": [{
        "op_kind": "lookup",
        "label": "Regionalwert abrufen",
        "note": "Trend des Schneedecken-Rückgangs der Region.",
    }],
    "snow_days": [{
        "op_kind": "lookup",
        "label": "Regionalwert abrufen",
        "note": "Schneedeckentage pro Jahr der Region.",
    }],
    "sea_level_rise": [{
        "op_kind": "lookup",
        "label": "Regionalwert abrufen",
        "note": "Regionaler Meeresspiegelanstieg aus Pegeldaten.",
    }],

    # — Klasse derived_index: abgeleiteter Spezialindex —
    "svf": [{
        "op_kind": "derived_index",
        "label": "Himmelssichtfaktor ableiten",
        "note": ("Anteil des sichtbaren Himmels 0…1 per Horizontwinkel-"
                 "Verfahren (SVF = 1 − (1/N)·Σ sin²γ, N=16 Richtungen, "
                 "100-m-Radius) auf einem 5-m-Gebäudehöhenraster; enge "
                 "Straßenschluchten ergeben kleine Werte."),
    }],
    "slope_deg": [{
        "op_kind": "derived_index",
        "label": "Hangneigung ableiten",
        "note": ("Steigung des Geländes in Grad aus dem Höhenraster "
                 "(Horn-Operator über die Nachbarzellen)."),
    }],
    "twi": [{
        "op_kind": "derived_index",
        "label": "Feuchteindex (TWI) berechnen",
        "note": ("Topographischer Feuchteindex: Neigung des Geländes, Wasser zu "
                 "sammeln.\n"
                 "Berechnung: TWI = ln(A / tan β); A = Flussakkumulation · "
                 "Zellfläche, β = Hangneigung"),
    }],
    "twi_norm": [{
        "op_kind": "derived_index",
        "label": "Feuchteindex (TWI) normieren",
        "note": ("Min-Max-Normierung des TWI über alle Zellen der Kommune → 0…1 "
                 "(zellrelative Skala, kein fester Grenzwert)."),
    }],
    "sink_depth_m": [{
        "op_kind": "derived_index",
        "label": "Senkentiefe ableiten",
        "note": ("Wie tief liegt die Zelle unter ihrem Umfeld?\n"
                 "Berechnung: max(0; mittlere Höhe der 8 Nachbarzellen − Zellhöhe)"),
    }],
    "flow_accum": [{
        "op_kind": "derived_index",
        "label": "Flussakkumulation ableiten",
        "note": ("Dem Geländegefälle folgend akkumulierter Wasserfluss durch die "
                 "Zelle (D8-Verfahren, Einheit: Anzahl Oberlieger-Zellen)."),
    }],
    "snow_elevation_factor": [{
        "op_kind": "derived_index",
        "label": "Höhenfaktor ableiten",
        "note": "Höhenmodulation für Schnee- und Gletscherindikatoren aus der Geländehöhe.",
    }],
    "slope_factor": [{
        "op_kind": "derived_index",
        "label": "Hangfaktor ableiten",
        "note": ("Hangneigung min-max-normiert über alle Zellen der Kommune → 0…1. "
                 "Ohne Geländemodell Fallback: 0,3 + 0,4 · (1 − Belüftung)."),
    }],
    "slope_proxy": [{
        "op_kind": "derived_index",
        "label": "Hangfaktor ableiten",
        "note": ("Proxy ohne Geländemodell.\n"
                 "Berechnung: 0,3 + 0,4 · (1 − Belüftung)"),
    }],
    "albedo": [{
        "op_kind": "mean",
        "label": "Albedo mitteln",
        "note": ("Flächengewichteter Mittelwert der Albedo-Tabellenwerte je "
                 "Landnutzungsklasse (z. B. Wasser dunkel, Sand hell) über die "
                 "Flächenanteile der Zelle."),
    }],
    "water_dist_m": [{
        "op_kind": "distance",
        "label": "Distanz messen",
        "note": ("Entfernung zum nächsten echten Gewässer in Metern; "
                 "Entwässerungsgräben (ditch/drain) zählen nicht."),
    }],
    "building_count_zensus": [{
        "op_kind": "lookup",
        "label": "Rasterwert übernehmen",
        "note": "Gebäudeanzahl der Zelle aus dem Zensus-Raster übernommen.",
    }],
    "pop_over_65": [{
        "op_kind": "multiply",
        "label": "×",
        "note": "Berechnung: Einwohner der Zelle · Anteil ≥ 65 Jahre / 100",
        "input_keys": ["pop", "share_over_65"],
    }],
    "pop_under_18": [{
        "op_kind": "multiply",
        "label": "×",
        "note": "Berechnung: Einwohner der Zelle · Anteil < 18 Jahre / 100",
        "input_keys": ["pop", "share_under_18"],
    }],

    # — Regionale Proxy-Ableitungen (ehrlich als Proxy ausgewiesen) —
    "drought_days": [{
        "op_kind": "formula",
        "label": "Proxy-Formel",
        "note": ("Berechnung: 8 + 1,2 · heiße Tage\n"
                 "Proxy, solange keine echten Trockentage angebunden sind; Basis "
                 "und Faktor editierbar (drought_base, drought_factor)."),
    }],
    "dry_index": [{
        "op_kind": "formula",
        "label": "Proxy-Formel",
        "note": ("Berechnung: min(1; heiße Tage / 25)\n"
                 "Proxy-Trockenheitsindex 0…1; Divisor editierbar "
                 "(dry_index_divisor)."),
    }],
    "low_flow_days": [{
        "op_kind": "lookup",
        "label": "Regionalwert abrufen",
        "note": ("Tage unter mittlerem Niedrigwasser (MNW) am nächsten "
                 "PEGELONLINE-Pegel; ohne Pegel Fallback-Proxy 10 + heiße Tage."),
    }],
    "mean_temp_rise": [{
        "op_kind": "formula",
        "label": "Proxy-Formel",
        "note": ("Berechnung: 1,6 + 0,1 · (Jahresmittel − 9,5 °C)\n"
                 "Proxy, solange der DWD-Klimaatlas nicht angebunden ist; Basis "
                 "editierbar (mean_temp_rise_base)."),
    }],
    "soil_moisture_decline": [{
        "op_kind": "formula",
        "label": "Proxy-Formel",
        "note": ("Berechnung: 20 + heiße Tage\n"
                 "Proxy, solange der UFZ-Dürremonitor nicht angebunden ist."),
    }],
    "surface_water_heating": [{
        "op_kind": "formula",
        "label": "Proxy-Formel",
        "note": ("Berechnung: 1,5 + 0,2 · (Jahresmittel − 9,5 °C)\n"
                 "Proxy für die Gewässererwärmung, solange keine "
                 "Satelliten-Wassertemperaturen angebunden sind."),
    }],

    # — Klasse weighted_sum: benanntes Modell —
    "uhi_delta": [{
        "op_kind": "weighted_sum",
        "label": "UHI-Modell",
        "note": (
            "Städtische Wärmeinsel: Aufheizung durch Versiegelung und Gebäude, "
            "Kühlung durch Grün, Wasser und Baumkronen, Aufschlag für enge "
            "Straßenschluchten. Die Flächenanteile sind dimensionslos (0…1) — "
            "die Einheit Kelvin steckt in den Koeffizienten α…ε und τ "
            "(editierbare UHI-Parameter, jeweils in K).\n"
            r"$$\Delta T\,[\mathrm{K}] = \alpha\,(1-\text{Albedo})\cdot\text{Versiegelung}"
            r" + \beta\,h\cdot\text{Gebäude}"
            r" - \gamma\,(1{,}8\cdot\text{Wald} + \text{Wiese} + 0{,}5\cdot\text{Acker})"
            r" - \delta\cdot\text{Wasser} - 10\,\tau\cdot\text{Bäume}"
            r" + \varepsilon\,h\,(1-\text{Himmelssicht})$$"
            "\nDabei: h = Gebäudehöhe/15 m (max. 2, dimensionslos); "
            "Wiese = Grünanteil ohne Wald; Ergebnis nie unter 0 K."
        ),
    }],

    # — Arithmetische Verkettungen (add/multiply/divide/max/scale_factor) —
    "imp_frac": [
        {
            "op_kind": "scale_factor",
            "label": "×",
            "factor": 0.95,
            "param_label": "Fahrbahnanteil an Straßenfläche",
            "note": ("Straßenanteil mit 0,95 gewichten — nur die Fahrbahn zählt "
                     "als versiegelt, nicht der gesamte Straßenraum."),
            "input_keys": ["road_cov"],
        },
        {
            "op_kind": "add",
            "label": "+",
            "note": ("Berechnung: Versiegelung = Gebäude-Anteil + 0,95 · Straßen-Anteil\n"
                     "Fällt auf den Landnutzungs-Anteil zurück, wenn Gebäude-/"
                     "Straßendaten fehlen; Untergrenze 2 %."),
            "input_keys": ["bldg_cov", "road_cov", "imp_lu"],
        },
    ],
    "share_vulnerable": [{
        "op_kind": "add",
        "label": "+",
        "note": ("Berechnung: Anteil Vulnerable = Anteil ≥ 65 + Anteil < 18\n"
                 "Gedeckelt bei 100 %."),
        "input_keys": ["share_over_65", "share_under_18"],
    }],
    "depression_factor": [{
        "op_kind": "weighted_sum",
        "label": "Senkenfaktor kombinieren",
        "note": ("Senkenneigung — sammelt sich Wasser in der Zelle?\n"
                 "Berechnung: min(1; 0,55 · TWI normiert + 0,45 · Senkentiefe "
                 "normiert)\n"
                 "Ohne Geländemodell Fallback: 0,5 · Versiegelung + "
                 "0,5 · Gewässernähe − 0,2 · Belüftung."),
    }],
    "depression_proxy": [{
        "op_kind": "add",
        "label": "+",
        "note": ("Senken-Proxy ohne Geländemodell.\n"
                 "Berechnung: Senke = Versiegelung + Gewässernähe − Belüftung"),
    }],
    "pop_density": [{
        "op_kind": "divide",
        "label": "÷",
        "note": ("Bevölkerungsdichte der Zelle.\n"
        r"$$\text{Einwohner} / \text{Fläche}\ [\mathrm{km}^{2}]$$"),
        "input_keys": ["pop", "area_km2"],
    }],
    "area_ha": [{
        "op_kind": "divide",
        "label": "÷",
        "note": ("Zellfläche von m² in Hektar umgerechnet.\n"
                 "Berechnung: Fläche / 10.000"),
    }],
    "industrial": [{
        "op_kind": "max",
        "label": "Maximum",
        "note": ("Industrieflächen-Anteil aus den Flächenanteilen der Zelle.\n"
        r"$$\max\bigl(0,\ \text{Versiegelung} - \text{Gebäude} - \text{Straßen}\bigr)$$"),
    }],
}

# Direkte Quell-Zuordnung (Quelle je Zwischenwert; Ableitungs-Operator s. oben)
CELL_DIRECT: dict[str, list[str]] = {
    "canopy_frac": ["osm"],
    "svf": ["lod2", "osm"],
    "avg_height": ["lod2", "osm"],
    "albedo": ["osm"],
    "glacier_frac": ["osm"],
    "water_dist_m": ["osm"],
    "flow_accum": ["dem"],
    "mean_elevation_m": ["dem"],
    "sink_depth_m": ["dem"],
    "snow_elevation_factor": ["dem"],
    "building_count_zensus": ["zensus"],
    "frost_days": ["dwd"],
    "heavy_rain_index": ["dwd"],
    "storm_days": ["era5"],
    "mean_temp": ["dwd"],
    "low_flow_days": ["pegelonline"],
    "glacier_loss_rate": ["dwd"],
    "snow_decline_rate_pct": ["dwd"],
    "snow_days": ["dwd"],
    "sea_level_rise": ["bsh"],
    # mean_temp_rise / soil_moisture_decline / surface_water_heating /
    # drought_days / dry_index sind Proxys aus mean_temp bzw. hot_days —
    # sie laufen bewusst über CELL_INPUT_LINEAGE statt einer Direktquelle.
}

# ── Formel-Ebene: explizite Schritte vor Indikator-Knoten ───────────────────

_CONST_NOTE_PREFIX = (
    "Platzhalterwert ohne ortsaufgelöste Datengrundlage — Modellannahme, "
    "keine Messung. "
)


def _const_step(note: str) -> list[OperatorStep]:
    """Ehrlicher Konstantwert-Schritt (op_kind constant, meta.placeholder).

    Für Indikatoren, deren Rezept nur aus einem festen Annahmewert besteht:
    Der Wert erscheint links als benannter Parameterknoten, der Schritt
    kennzeichnet ihn ausdrücklich als Platzhalter (per Ratchet-Test
    test_constant_indicators_are_marked_placeholder erzwungen).
    """
    return [{
        "op_kind": "constant",
        "label": "Konstantwert übernehmen",
        "placeholder": True,
        "note": _CONST_NOTE_PREFIX + note,
    }]


FORMULA_OPERATORS: dict[str, list[OperatorStep]] = {
    # ── Hazards ─────────────────────────────────────────────────────────────
    "HEAT_WAVE": [
        {
            "op_kind": "scaling",
            "label": "Skalierung",
            "factor": 1.5,
            "value": 1.5,
            "unit": "×",
            # bewusst KEINE parameter_id: der Faktor ist in indicators.py fest
            # verdrahtet (Modellkonstante), ein Registry-Override wäre wirkungslos.
            # Er erscheint stattdessen als (nicht editierbarer) Parameterknoten.
            "param_label": "UHI-Gewichtung",
            "note": "UHI-ΔT mit festem Gewichtungsfaktor 1,5 skalieren (Modellkonstante).",
            "input_keys": ["uhi_delta"],
        },
        {
            "op_kind": "add",
            "label": "+",
            "note": ("Heiße Tage + skalierte UHI-ΔT; Ergebnis auf 0…40 begrenzt.\n"
                     r"$$\min\bigl(40,\ H_{\mathrm{Tage}} + 1{,}5 \cdot \Delta T_{\mathrm{UHI}}\bigr)$$"),
            "input_keys": ["hot_days", "uhi_delta"],
        },
    ],
    "HEAVY_RAIN_FLOOD": [
        {
            "op_kind": "multiply",
            "label": "×",
            "note": ("Starkregen × Versiegelung × Feuchteindex × Senke — die "
                     "Faktoren sind gedämpft (0,4/0,5/0,6-Sockel), damit kein "
                     "Einzelfaktor das Ergebnis allein auf 0 zieht; auf 0…100 "
                     "begrenzt.\n"
                r"$$\min\bigl(100,\ \text{Starkregen} \cdot (0{,}4 + \text{Versiegelung}) \cdot (0{,}5 + 0{,}5\,\mathrm{TWI}) \cdot (0{,}6 + \text{Senke})\bigr)$$"),
        },
    ],
    "MEAN_TEMPERATURE_RISE": [
        {
            "op_kind": "scale_factor", "label": "×", "factor": 0.08,
            "param_label": "Gewichtung UHI-ΔT",
            "note": ("UHI-ΔT mit Faktor 0,08 gewichten (Modellkonstante) — nur "
                     "ein kleiner Teil der lokalen Wärmeinsel wirkt auf den "
                     "langjährigen Temperaturanstieg."),
            "input_keys": ["uhi_delta"],
        },
        {
            "op_kind": "add", "label": "+",
            "note": ("Regionaler Anstieg plus gewichtete Wärmeinsel.\n"
                     r"$$\Delta T_{\mathrm{regional}} + 0{,}08 \cdot \Delta T_{\mathrm{UHI}}$$"),
            "input_keys": ["mean_temp_rise", "uhi_delta"],
        },
    ],
    "SEA_LEVEL_RISE": [{
        "op_kind": "lookup", "label": "Küstenwert übernehmen",
        "note": ("Regionaler Meeresspiegelanstieg aus Pegeldaten, für alle "
                 "Zellen der Kommune gleich; nur Küstenkommunen, im "
                 "Binnenland 0."),
        "input_keys": ["sea_level_rise"],
    }],
    "GLACIER_SNOW_LOSS": [
        {
            "op_kind": "multiply", "label": "×",
            "note": ("Gletscher-Term: Schwundrate · Gletscheranteil der Zelle.\n"
                     r"$$\text{Schwundrate} \cdot \text{Gletscheranteil}$$"),
            "input_keys": ["glacier_loss_rate", "glacier_frac"],
        },
        {
            "op_kind": "multiply", "label": "×",
            "note": ("Schnee-Term: Rückgangsrate, höhenmoduliert und über die "
                     "Schneedeckentage gedeckelt.\n"
                     r"$$\text{Schneerückgang} \cdot (0{,}25 + 0{,}75 \cdot h) \cdot \min\bigl(1;\ \text{Schneetage}/45\bigr)$$"
                     "\nDabei: h = Höhenfaktor 0…1 aus dem Geländemodell."),
            "input_keys": ["snow_decline_rate_pct", "snow_elevation_factor", "snow_days"],
        },
        {
            "op_kind": "add", "label": "+",
            "note": "Summe aus Gletscher- und Schnee-Term.",
            "input_keys": ["glacier_loss_rate", "snow_decline_rate_pct"],
        },
    ],
    "SOIL_MOISTURE_DECLINE": [{
        "op_kind": "multiply", "label": "×",
        "note": ("Regionaler Bodenfeuchte-Rückgang, verstärkt in Zellen mit "
                 "viel Acker- und Grünfläche (vegetationsgeprägte Böden "
                 "trocknen stärker aus).\n"
                 r"$$\text{Regional} \cdot \bigl(0{,}5 + 0{,}6 \cdot (\text{Acker} + \text{Grün})\bigr)$$"),
        "input_keys": ["soil_moisture_decline", "farmland_frac", "green_frac"],
    }],
    "COLD_EXTREME": [{
        "op_kind": "multiply", "label": "×",
        "note": ("Frosttage, gemildert durch die städtische Wärmeinsel.\n"
                 r"$$\text{Frosttage} \cdot \bigl(1 - 0{,}3 \cdot \min(\Delta T_{\mathrm{UHI}}/5;\ 1)\bigr)$$"),
        "input_keys": ["frost_days", "uhi_delta"],
    }],
    "DROUGHT": [{
        "op_kind": "multiply", "label": "×",
        "note": ("Trockentage, verstärkt in Zellen mit viel Acker- und "
                 "Grünfläche; Ergebnis auf 0…60 begrenzt.\n"
                 r"$$\min\bigl(60;\ \text{Trockentage} \cdot (0{,}6 + 0{,}7 \cdot (\text{Acker} + \text{Grün}))\bigr)$$"),
        "input_keys": ["drought_days", "farmland_frac", "green_frac"],
    }],
    "EXTRATROPICAL_STORM": [{
        "op_kind": "multiply", "label": "×",
        "note": ("Sturmtage, verstärkt in offenen, gut belüfteten Lagen "
                 "(windexponiert).\n"
                 r"$$\text{Sturmtage} \cdot (0{,}8 + 0{,}5 \cdot \text{Belüftung})$$"),
        "input_keys": ["storm_days", "vent_score"],
    }],
    "WILDFIRE": [{
        "op_kind": "multiply", "label": "×",
        "note": ("Waldanteil, verstärkt durch die regionale Trockenheit; "
                 "Ergebnis auf 0…100 begrenzt.\n"
                 r"$$\min\bigl(100;\ \text{Wald} \cdot 100 \cdot (0{,}4 + \text{Trockenheit})\bigr)$$"),
        "input_keys": ["forest_frac", "dry_index"],
    }],
    "LANDSLIDE": [{
        "op_kind": "multiply", "label": "×",
        "note": ("Hangfaktor, verstärkt durch die Starkregen-Häufigkeit; "
                 "Ergebnis auf 0…100 begrenzt.\n"
                 r"$$\min\bigl(100;\ \text{Hangfaktor} \cdot 100 \cdot \text{Starkregen}/100\bigr)$$"),
        "input_keys": ["slope_factor", "heavy_rain_index"],
    }],
    "SOIL_SALINIZATION": [{
        "op_kind": "multiply", "label": "×",
        "note": ("Gedämpfte Produktformel — jeder Faktor hebt an, keiner kann "
                 "das Ergebnis allein auf 0 ziehen; gedeckelt bei 1.\n"
                 r"$$\min\bigl(1;\ B \cdot (0{,}35 + 0{,}65\,\text{Senke}) \cdot (0{,}45 + 0{,}55\,\text{Acker}) \cdot (0{,}55 + 0{,}45\,\text{Trockenheit}) \cdot K\bigr)$$"
                 "\nDabei: B = Basis (Küste 0,4 / Binnen 0,05); K = an der "
                 "Küste 0,5 + 0,5 · Gewässernähe, im Binnenland 0,55 + 0,45 · "
                 "(1 − Höhe/80 m)."),
        "input_keys": ["depression_factor", "farmland_frac", "dry_index",
                       "water_prox", "mean_elevation_m"],
    }],
    "SURFACE_WATER_HEATING": [{
        "op_kind": "multiply", "label": "×",
        "note": ("Regionale Gewässererwärmung, verstärkt in Zellen mit "
                 "Wasserflächen.\n"
                 r"$$\text{Gewässererwärmung} \cdot (0{,}5 + \text{Wasseranteil})$$"),
        "input_keys": ["surface_water_heating", "water_frac"],
    }],
    "LOW_FLOW_NIEDRIGWASSER": [{
        "op_kind": "multiply", "label": "×",
        "note": ("Niedrigwasser-Tage, verstärkt durch Trockenheit und "
                 "Gewässernähe; Ergebnis auf 0…60 begrenzt.\n"
                 r"$$\min\bigl(60;\ \text{NW-Tage} \cdot (0{,}6 + 0{,}4\,\text{Trockenheit}) \cdot (1 + 0{,}3\,\text{Gewässernähe})\bigr)$$"),
        "input_keys": ["low_flow_days", "dry_index", "water_prox"],
    }],
    "OCEAN_WARMING": _const_step(
        "Erwärmung der Meeresoberfläche, bundesweit einheitlich; "
        "gilt nur in Küstenzellen, im Binnenland 0."),
    "OCEAN_ACIDIFICATION": _const_step(
        "Versauerung der Meere (ΔpH), bundesweit einheitlich; "
        "gilt nur in Küstenzellen, im Binnenland 0."),
    "PERMAFROST_THAW": _const_step(
        "Permafrost existiert in Deutschland nur in alpinen Hochlagen — "
        "der Wert ist deshalb bundesweit 0."),
    "TROPICAL_CYCLONE": _const_step(
        "Tropische Wirbelstürme erreichen Deutschland nur als seltene "
        "Ausläufer — nationaler Kleinstwert, keine Ortsauflösung."),
    "STORM_SURGE": _const_step(
        "Sturmflut-Häufigkeit pro Jahr, einheitlich für alle Küstenzellen; "
        "im Binnenland 0."),
    "SALTWATER_INTRUSION": _const_step(
        "Salzwassereinbruch ins Grundwasser, einheitlich für alle "
        "Küstenzellen; im Binnenland 0."),
    "COASTAL_EROSION": _const_step(
        "Küstenrückgang in m/Jahr, einheitlich für alle Küstenzellen; "
        "im Binnenland 0."),
    "CASCADE_EVENT": _const_step(
        "Qualitativer Index für Kaskadeneffekte (Folgeausfälle über "
        "Sektoren hinweg) — nicht ortsaufgelöst modelliert."),

    # ── Exposures ───────────────────────────────────────────────────────────
    "SUPPLY_CHAIN_NODES": [
        {"op_kind": "scale_factor", "label": "×", "factor": 6,
         "param_label": "Gewichtung Industriefläche",
         "note": "Industriefläche mit Faktor 6 gewichten (Modellkonstante)."},
        {"op_kind": "scale_factor", "label": "×", "factor": 0.004,
         "param_label": "Gewichtung Gebäudeanzahl",
         "note": "Gebäudeanzahl mit Faktor 0,004 gewichten (Modellkonstante)."},
        {"op_kind": "add", "label": "+",
         "note": ("Summe der beiden Terme.\n"
                  r"$$6 \cdot \text{Industrie} + 0{,}004 \cdot \text{Gebäude}$$")},
    ],
    "AGE_STRUCTURE": [{
        "op_kind": "add", "label": "+",
        "note": ("Berechnung: Anteil ≥ 65 + Anteil < 18\n"
                 "Fehlen Zellwerte, gilt der Gemeindewert aus dem Zensus."),
        "input_keys": ["share_over_65", "share_under_18"],
    }],
    "OUTDOOR_THERMAL_EXPOSURE": [{
        "op_kind": "add", "label": "+",
        "note": ("Angenommene Aufenthaltsdauer im Freien (h/Tag): Grünflächen "
                 "laden zu längerem Aufenthalt ein.\n"
                 "Berechnung: 2 + 3 · Grünanteil"),
        "input_keys": ["green_frac"],
    }],
    "VULNERABLE_GROUPS_POPULATION": [{
        "op_kind": "multiply", "label": "×",
        "note": ("Vulnerable Personen der Zelle.\n"
                 r"$$\text{Einwohner} \cdot \text{Anteil Vulnerable} / 100$$"),
        "input_keys": ["pop", "share_vulnerable"],
    }],
    "BUILDING_STOCK": [{
        "op_kind": "multiply", "label": "×",
        "note": ("Gebäudegrundrissfläche der Zelle in m².\n"
                 r"$$\text{Gebäudeanteil} \cdot \text{Zellfläche}\ [\mathrm{m}^{2}]$$"),
        "input_keys": ["bldg_cov", "area_m2"],
    }],
    "BUILDING_USE_TYPES": [{
        "op_kind": "count", "label": "Gebäude zählen",
        "note": ("Anzahl der OSM-Gebäude der Zelle als Proxy für die "
                 "Nutzungsvielfalt — eine Differenzierung nach Nutzungsart "
                 "erfolgt nicht."),
        "input_keys": ["bldg_count"],
    }],
    "LOCATION_HAZARD_ZONES": [{
        "op_kind": "multiply", "label": "×",
        "note": ("Bebaute Fläche in Gefahrenlagen: Senken (Überflutung) oder "
                 "starke Wärmeinsel.\n"
                 r"$$\text{Fläche}\,[\mathrm{ha}] \cdot \text{Gebäudeanteil} \cdot \max\bigl(\text{Senke};\ \min(\Delta T_{\mathrm{UHI}}/6;\ 1)\bigr)$$"),
        "input_keys": ["area_ha", "bldg_cov", "depression_factor", "uhi_delta"],
    }],
    "ENERGY_INFRASTRUCTURE": [{
        "op_kind": "lookup", "label": "Kritikalitätspunkte übernehmen",
        "note": ("Die anlagenklassen-gewichteten Kritikalitätspunkte der Zelle "
                 "(Sättigungsformel, siehe vorgelagerter Schritt) werden "
                 "unverändert als Exposition übernommen."),
        "input_keys": ["energy_infra_count"],
    }],
    "WATER_WASTEWATER_INFRA": [{
        "op_kind": "lookup", "label": "Kritikalitätspunkte übernehmen",
        "note": ("Die anlagenklassen-gewichteten Kritikalitätspunkte der Zelle "
                 "(Sättigungsformel, siehe vorgelagerter Schritt) werden "
                 "unverändert als Exposition übernommen."),
        "input_keys": ["water_wastewater_count"],
    }],
    "TRANSPORT_HUBS": [{
        "op_kind": "lookup", "label": "Kritikalitätspunkte übernehmen",
        "note": ("Die anlagenklassen-gewichteten Kritikalitätspunkte der Zelle "
                 "(Sättigungsformel, siehe vorgelagerter Schritt) werden "
                 "unverändert als Exposition übernommen."),
        "input_keys": ["transport_hub_count"],
    }],
    "COMMUNICATION_INFRA": [{
        "op_kind": "lookup", "label": "Kritikalitätspunkte übernehmen",
        "note": ("Die anlagenklassen-gewichteten Kritikalitätspunkte der Zelle "
                 "(Sättigungsformel, siehe vorgelagerter Schritt) werden "
                 "unverändert als Exposition übernommen."),
        "input_keys": ["communication_count"],
    }],
    "HEALTHCARE_INFRASTRUCTURE": [{
        "op_kind": "scale_factor", "label": "×", "factor": 100,
        "param_label": "Skalierung auf Index",
        "note": "Berechnung: Erreichbarkeits-Score · 100 → Index 0…100",
        "input_keys": ["healthcare_access_score"],
    }],
    "INDUSTRIAL_COMMERCIAL_AREAS": [{
        "op_kind": "multiply", "label": "×",
        "note": ("Industrie- und Gewerbefläche der Zelle in Hektar.\n"
                 r"$$\text{Fläche}\,[\mathrm{ha}] \cdot \text{Industrieanteil}$$"),
        "input_keys": ["area_ha", "industrial"],
    }],
    "AGRICULTURAL_LAND": [{
        "op_kind": "multiply", "label": "×",
        "note": ("Landwirtschaftliche Fläche der Zelle in Hektar.\n"
                 r"$$\text{Fläche}\,[\mathrm{ha}] \cdot \text{Ackeranteil}$$"),
        "input_keys": ["area_ha", "farmland_frac"],
    }],
    "FOREST_AREA": [{
        "op_kind": "multiply", "label": "×",
        "note": ("Waldfläche der Zelle in Hektar.\n"
                 r"$$\text{Fläche}\,[\mathrm{ha}] \cdot \text{Waldanteil}$$"),
        "input_keys": ["area_ha", "forest_frac"],
    }],
    "BIODIVERSITY_HOTSPOTS": [{
        "op_kind": "multiply", "label": "×",
        "note": ("Naturnahe Fläche (Wald + Wasser), mit 0,5 gewichtet — nicht "
                 "jede Wald-/Wasserfläche ist ein Hotspot.\n"
                 r"$$\text{Fläche}\,[\mathrm{ha}] \cdot (\text{Wald} + \text{Wasser}) \cdot 0{,}5$$"),
        "input_keys": ["area_ha", "forest_frac", "water_frac"],
    }],
    "EROSION_PRONE_SOILS": [{
        "op_kind": "multiply", "label": "×",
        "note": ("Erosionsgefährdete Ackerfläche: Acker in Hanglage.\n"
                 r"$$\text{Fläche}\,[\mathrm{ha}] \cdot \text{Ackeranteil} \cdot \text{Hangfaktor}$$"),
        "input_keys": ["area_ha", "farmland_frac", "slope_factor"],
    }],
    "COASTAL_RIPARIAN_ZONES": [{
        "op_kind": "multiply", "label": "×",
        "note": ("Ufer- und Küstenzonen: gewässernahe Fläche, feuchtegeprägt "
                 "über den Feuchteindex.\n"
                 r"$$\text{Fläche}\,[\mathrm{ha}] \cdot \text{Gewässernähe} \cdot (0{,}5 + 0{,}5\,\mathrm{TWI})$$"
                 "\nGewässernähe = kombinierter Score aus Nachbarschafts- und "
                 "Distanzbewertung (Maximum)."),
        "input_keys": ["area_ha", "water_adj", "twi_norm"],
    }],
    "FLOODPLAINS": [{
        "op_kind": "multiply", "label": "×",
        "note": ("Überflutungsflächen: Senken nahe Gewässern.\n"
                 r"$$\text{Fläche}\,[\mathrm{ha}] \cdot \text{Senke} \cdot \max\bigl(\text{Gewässernähe};\ s\bigr)$$"
                 "\nDabei: s = Sockel 0,3 bei Gewässern in der Nachbarschaft, "
                 "sonst 0,1 — Senken ohne kartiertes Gewässer bleiben als "
                 "potenzielle Überflutungsfläche sichtbar."),
        "input_keys": ["area_ha", "depression_factor", "water_prox"],
    }],
    "COASTAL_STORM_SURGE_EXPOSURE": [{
        "op_kind": "multiply", "label": "×",
        "note": ("Bebaute Fläche in Sturmflut-Lagen; nur Küstenkommunen, im "
                 "Binnenland 0.\n"
                 r"$$\text{Fläche}\,[\mathrm{ha}] \cdot \text{Gebäudeanteil}$$"),
        "input_keys": ["area_ha", "bldg_cov"],
    }],
    "GROUNDWATER_DEPENDENT_ECOSYSTEMS": [{
        "op_kind": "multiply", "label": "×",
        "note": ("Grundwasserabhängige Vegetation: Wald- und Grünflächen, "
                 "verstärkt in Gewässernähe.\n"
                 r"$$\text{Fläche}\,[\mathrm{ha}] \cdot (\text{Wald} + \text{Grün}) \cdot (0{,}3 + \text{Gewässernähe})$$"),
        "input_keys": ["area_ha", "forest_frac", "green_frac", "water_adj"],
    }],
    "FISHERIES_AQUACULTURE_AREAS": [{
        "op_kind": "scale_factor", "label": "×", "factor": 5,
        "param_label": "Gewichtung Wasserfläche",
        "note": ("Wasseranteil der Zelle mit Faktor 5 gewichtet "
                 "(Modellkonstante) als Proxy für Fischerei- und "
                 "Aquakulturflächen."),
        "input_keys": ["water_frac"],
    }],
    "FISH_SPAWNING_HABITATS": [{
        "op_kind": "multiply", "label": "×",
        "note": ("Laichhabitate: Wasserflächen, ersatzweise gewässernahe "
                 "Flächen mit halbem Gewicht.\n"
                 r"$$\text{Fläche}\,[\mathrm{ha}] \cdot \max\bigl(\text{Wasseranteil};\ 0{,}5 \cdot \text{Gewässernähe}\bigr)$$"),
        "input_keys": ["area_ha", "water_frac", "water_prox"],
    }],

    # ── Vulnerabilities ─────────────────────────────────────────────────────
    "CRITICAL_INFRA_CONDITION": _const_step(
        "Der bauliche Zustand kritischer Infrastruktur ist nicht "
        "flächendeckend offen verfügbar — neutraler Wert 50 (Skalenmitte)."),
    "SUPPLY_CHAIN_DEPENDENCY": _const_step(
        "Die Lieferkettenabhängigkeit der lokalen Wirtschaft ist nicht "
        "ortsaufgelöst erfasst — neutraler Wert 50 (Skalenmitte)."),
    "REDUNDANCY_BACKUP": _const_step(
        "Redundanz- und Backup-Kapazitäten (invers) sind nicht ortsaufgelöst "
        "erfasst — neutraler Wert 50 (Skalenmitte)."),
    "INFRA_DEPENDENCY_CHAIN": _const_step(
        "Abhängigkeitsketten zwischen Infrastrukturen sind nicht "
        "ortsaufgelöst erfasst — neutraler Wert 50 (Skalenmitte)."),
    "SALTWATER_INTRUSION_RISK": _const_step(
        "Salzwasserintrusions-Empfindlichkeit als Zweistufen-Annahme: "
        "Küste 40, Binnenland 10."),
    "AQUACULTURE_TECHNICAL_VULNERABILITY": _const_step(
        "Die technische Verwundbarkeit von Aquakulturanlagen ist nicht "
        "ortsaufgelöst erfasst — neutraler Wert 50 (Skalenmitte)."),
    "FISHERIES_MANAGEMENT_CAPACITY": _const_step(
        "Die Management-Kapazität der Fischerei (invers) ist nicht "
        "ortsaufgelöst erfasst — Annahmewert 45 (leicht besser als neutral)."),
    "BUILDING_STABILITY": [{
        "op_kind": "weighted_sum", "label": "Stabilitäts-Index kombinieren",
        "note": ("Invers: hoch = empfindliche Bausubstanz. Basis 50, plus "
                 "20 · Gebäudeanteil (dichte Bebauung), plus 10 bei mittlerer "
                 "Gebäudehöhe über 18 m, plus Altersfaktor "
                 "min(30; (heute − Baujahr)/100 · 30); Ergebnis 0…100."),
        "input_keys": ["bldg_cov", "avg_height", "building_age_mean"],
    }],
    "MATERIAL_HEAT_SENSITIVITY": [{
        "op_kind": "scale_factor", "label": "×", "factor": 100,
        "param_label": "Skalierung auf Index",
        "note": ("Berechnung: Versiegelungsgrad · 100 → Index 0…100\n"
                 "Versiegelte Materialien (Asphalt, Beton) speichern Hitze."),
        "input_keys": ["imp_frac"],
    }],
    "VULNERABLE_GROUPS_SHARE": [{
        "op_kind": "lookup", "label": "Anteil übernehmen",
        "note": ("Der Anteil vulnerabler Gruppen der Zelle wird direkt als "
                 "Index übernommen (Prozentwert 0…100)."),
        "input_keys": ["share_vulnerable"],
    }],
    "INCOME_SOCIAL_RESILIENCE": [{
        "op_kind": "mean", "label": "Teil-Scores kombinieren",
        "note": ("Invers: hoch = geringe soziale Resilienz. Drei Teil-Scores "
                 "je 0…100: Mietbelastung (Miete/18 € · 100), 100 − "
                 "Eigentümerquote, 100 − Wohnfläche/60 m² · 100 — gemittelt "
                 "über die verfügbaren Werte; ohne Zensus-Daten Fallback 45."),
        "input_keys": ["net_cold_rent", "owner_share", "living_area_per_person"],
    }],
    "HEALTHCARE_ACCESS": [{
        "op_kind": "formula", "label": "Zugang invertieren",
        "note": ("Berechnung: 100 · (1 − Erreichbarkeits-Score)\n"
                 "Invers: hohe Werte bedeuten schlechten Zugang zu "
                 "Gesundheitseinrichtungen."),
        "input_keys": ["healthcare_access_score"],
    }],
    "WILDFIRE_SUSCEPTIBILITY": [{
        "op_kind": "multiply", "label": "×",
        "note": ("Waldanteil, verstärkt durch Trockenheit; Ergebnis auf 0…100 "
                 "begrenzt.\n"
                 r"$$\min\bigl(100;\ \text{Wald} \cdot 100 \cdot (0{,}5 + \text{Trockenheit}/2)\bigr)$$"),
        "input_keys": ["forest_frac", "dry_index"],
    }],
    "BIODIVERSITY_RESILIENCE": [{
        "op_kind": "formula", "label": "Index invertieren",
        "note": ("Berechnung: 100 − 60 · (Waldanteil + Grünanteil)\n"
                 "Invers: viel Wald und Grün = hohe Resilienz = niedriger "
                 "Index; begrenzt auf 0…100."),
        "input_keys": ["forest_frac", "green_frac"],
    }],
    "SOIL_SENSITIVITY": [{
        "op_kind": "weighted_sum", "label": "Bodenempfindlichkeit gewichten",
        "note": ("Hanglage und Ackernutzung machen Böden empfindlich; "
                 "Ergebnis auf 0…100 begrenzt.\n"
                 r"$$\min\bigl(100;\ 60 \cdot \text{Hangfaktor} + 40 \cdot \text{Ackeranteil}\bigr)$$"),
        "input_keys": ["slope_factor", "farmland_frac"],
    }],
    "SINGLE_SITE_DEPENDENCY": [{
        "op_kind": "scale_factor", "label": "×", "factor": 200,
        "param_label": "Gewichtung Industrieanteil",
        "note": ("Industrieanteil mit Faktor 200 gewichten (Modellkonstante); "
                 "Ergebnis auf 0…100 begrenzt — Zellen mit viel Industrie "
                 "hängen eher an einzelnen Standorten.\n"
                 r"$$\min\bigl(100;\ 200 \cdot \text{Industrieanteil}\bigr)$$"),
        "input_keys": ["industrial"],
    }],
    "FINANCIAL_ADAPTATION_CAPACITY": [{
        "op_kind": "lookup", "label": "Sozioökonomie-Index übernehmen",
        "note": ("Invers: hoch = geringe finanzielle Anpassungskapazität. "
                 "Aus BBSR-INKAR-Kennzahlen (Steuerkraft, Arbeitslosigkeit) "
                 "je Gemeinde; ohne auflösbare Kennzahl neutraler Fallback 50. "
                 "Ein Override ersetzt den Wert in allen Zellen "
                 "(Override > Ableitung > Fallback)."),
        "input_keys": ["financial_adaptation"],
    }],
    "HEAT_SENSITIVITY": [{
        "op_kind": "weighted_sum", "label": "Hitzeempfindlichkeit gewichten",
        "note": ("Vulnerable Bevölkerung, Wärmeinsel und Grünmangel; Ergebnis "
                 "auf 0…100 begrenzt.\n"
                 r"$$\min\bigl(100;\ \text{Vulnerable} + 6 \cdot \Delta T_{\mathrm{UHI}} + 20 \cdot (1 - \text{Grün})\bigr)$$"),
        "input_keys": ["share_vulnerable", "uhi_delta", "green_frac"],
    }],
    "AIR_QUALITY_RISK": [{
        "op_kind": "weighted_sum", "label": "Luftbelastung gewichten",
        "note": ("Versiegelung und Verkehrsflächen als Proxy für die "
                 "Luftschadstoff-Belastung; Ergebnis auf 0…100 begrenzt.\n"
                 r"$$\min\bigl(100;\ 60 \cdot \text{Versiegelung} + 200 \cdot \text{Straßenanteil}\bigr)$$"),
        "input_keys": ["imp_frac", "road_cov"],
    }],
    "DISEASE_VECTOR_SUSCEPTIBILITY": [{
        "op_kind": "multiply", "label": "×",
        "note": ("Wasserflächen (Brutstätten) und Wärme begünstigen "
                 "Krankheitsüberträger; Ergebnis auf 0…100 begrenzt.\n"
                 r"$$\min\bigl(100;\ \text{Wasseranteil} \cdot 100 \cdot T_{\mathrm{Jahr}}/12\bigr)$$"),
        "input_keys": ["water_frac", "mean_temp"],
    }],
    "GROUNDWATER_DEPENDENCY": [{
        "op_kind": "weighted_sum", "label": "Abhängigkeit gewichten",
        "note": ("Acker- und Grünflächen hängen am Grundwasser; Ergebnis auf "
                 "0…100 begrenzt.\n"
                 r"$$\min\bigl(100;\ 50 \cdot (\text{Acker} + \text{Grün})\bigr)$$"),
        "input_keys": ["farmland_frac", "green_frac"],
    }],
    "WATER_STRESS_INDEX": [{
        "op_kind": "weighted_sum", "label": "Wasserstress gewichten",
        "note": ("Versiegelung (Abfluss statt Versickerung), "
                 "Bevölkerungsdichte (Verbrauch) und Trockenheit; Ergebnis "
                 "auf 0…100 begrenzt.\n"
                 r"$$\min\bigl(100;\ 40\,\text{Versiegelung} + 40 \cdot \min(\rho/4000;\ 1) + 20\,\text{Trockenheit}\bigr)$$"
                 "\nDabei: ρ = Einwohner je km²."),
        "input_keys": ["imp_frac", "pop_density", "dry_index"],
    }],
    "IRRIGATION_DEPENDENCY": [{
        "op_kind": "multiply", "label": "×",
        "note": ("Ackerflächen, verstärkt durch Trockenheit — "
                 "Bewässerungsbedarf; Ergebnis auf 0…100 begrenzt.\n"
                 r"$$\min\bigl(100;\ \text{Acker} \cdot 100 \cdot (0{,}5 + \text{Trockenheit}/2)\bigr)$$"),
        "input_keys": ["farmland_frac", "dry_index"],
    }],
    "EROSION_SUSCEPTIBILITY": [{
        "op_kind": "multiply", "label": "×",
        "note": ("Hanglagen ohne schützende Vegetation; Ergebnis auf 0…100 "
                 "begrenzt.\n"
                 r"$$\min\bigl(100;\ \text{Hangfaktor} \cdot 100 \cdot (1 - \text{Grünanteil})\bigr)$$"),
        "input_keys": ["slope_factor", "green_frac"],
    }],
    "LEVEE_CONDITION": [{
        "op_kind": "weighted_sum", "label": "Deichzustand modulieren",
        "note": ("Invers: hoch = schlechter Hochwasserschutz. Basis 50 "
                 "(Küste) / 30 (Binnen); in hochwasserexponierten Zellen: "
                 "Basis + 40 · Exposition · (1 − Deichnähe) − 25 · Deichnähe, "
                 "begrenzt 0…100. Exposition = max(Gewässernähe; Feuchteindex; "
                 "Senke), an der Küste 1. Ein Override ersetzt den Wert in "
                 "allen Zellen — auch die OSM-Ableitung und den "
                 "Küstenaufschlag."),
        "input_keys": ["dyke_prox", "water_prox"],
    }],
    "SEALING_DEGREE": [{
        "op_kind": "scale_factor", "label": "×", "factor": 100,
        "param_label": "Skalierung auf Index",
        "note": "Berechnung: Versiegelungsgrad · 100 → Index 0…100",
        "input_keys": ["imp_frac"],
    }],
    "UHI_INTENSITY": [{
        "op_kind": "lookup", "label": "Modellwert übernehmen",
        "note": ("Die UHI-ΔT der Zelle (Kelvin) aus dem OSM-Wärmeinselmodell "
                 "wird direkt als Kartenwert übernommen."),
        "input_keys": ["uhi_delta"],
    }],
    "GREEN_SPACE_SHARE": [{
        "op_kind": "formula", "label": "Defizit invertieren",
        "note": ("Berechnung: 100 − 100 · Grünanteil\n"
                 "Invers: wenig Grün = hoher Index (Grünflächen-Defizit)."),
        "input_keys": ["green_frac"],
    }],
    "EARLY_WARNING_SYSTEMS": [{
        "op_kind": "formula", "label": "Zur Skalenmitte dämpfen",
        "note": ("Berechnung: 50 + (Katastrophenschutz-Index − 50) · 0,6\n"
                 "Invers: hoch = schwache Frühwarnung. Zur Skalenmitte "
                 "gedämpft, weil die Feuerwehr-Nähe Frühwarnsysteme (Sirenen, "
                 "Warn-Apps, Pegelmessnetze) nur schwach abbildet; ohne "
                 "OSM-Notfalldaten Fallback 40 (Deutschland ist über MoWaS/"
                 "Cell Broadcast/Sirenen grundversorgt). Ein Override ersetzt "
                 "den Wert in allen Zellen."),
        "input_keys": ["emergency_access_score"],
    }],
    "EMERGENCY_MANAGEMENT": [{
        "op_kind": "formula", "label": "Erreichbarkeit invertieren",
        "note": ("Berechnung: 100 · (1 − Notfall-Erreichbarkeit)\n"
                 "Invers: schlechte Erreichbarkeit von Feuerwehr/Rettung = "
                 "hoher Index; ohne OSM-Notfalldaten Fallback 40 (leicht "
                 "besser als neutral wegen des flächendeckenden deutschen "
                 "Feuerwehrsystems). Ein Override ersetzt den Wert in allen "
                 "Zellen."),
        "input_keys": ["emergency_access_score"],
    }],
    "PLANNING_IMPLEMENTATION_CAPACITY": [{
        "op_kind": "lookup", "label": "Finanzkraft-Index übernehmen",
        "note": ("Invers: hoch = geringe Planungs-/Umsetzungskapazität. Aus "
                 "der BBSR-INKAR-Finanzkraft (Steuerkraft je Einwohner) der "
                 "Gemeinde; ohne auflösbare Kennzahl neutraler Fallback 50. "
                 "Ein Override ersetzt den Wert in allen Zellen "
                 "(Override > Ableitung > Fallback)."),
        "input_keys": ["planning_capacity"],
    }],
    "FISHERIES_TEMPERATURE_SENSITIVITY": [{
        "op_kind": "multiply", "label": "×",
        "note": ("Wasserflächen, verstärkt durch die Gewässererwärmung; "
                 "Ergebnis auf 0…100 begrenzt.\n"
                 r"$$\min\bigl(100;\ \text{Wasseranteil} \cdot 100 \cdot \Delta T_{\mathrm{Gewässer}}/3\bigr)$$"),
        "input_keys": ["water_frac", "surface_water_heating"],
    }],
    "INFRA_CRITICALITY": [
        {"op_kind": "multiply", "label": "×",
         "note": "Jeder KRITIS-Sektor mit seinem Kritikalitätsgewicht multipliziert."},
        {
            "op_kind": "add",
            "label": "+",
            "note": (
                "Gewichtete Summe aus Energie, Wasser, IT/Kommunikation, Gesundheit "
                "und Verkehr; Ergebnis auf 0…100 begrenzt.\n"
                r"$$\min\Bigl(100,\ \sum_{i} w_{i} \cdot n_{i}\Bigr)$$"
            ),
        },
    ],
    "POPULATION_DENSITY": [{
        "op_kind": "divide",
        "label": "÷",
        "note": ("Bevölkerungsdichte aus Einwohnern und Zellfläche.\n"
        r"$$\text{Einwohner} / \text{Fläche}\ [\mathrm{km}^{2}]$$"),
        "input_keys": ["pop", "area_km2"],
    }],
    "COMPOUND_EVENT": [{
        "op_kind": "max",
        "label": "Maximum",
        "note": ("Maximum aus normierten Hitze-, Dürre- und Starkregen-Indizes.\n"
        r"$$\max\bigl(\hat{H}_{\text{Hitze}},\ \hat{H}_{\text{Dürre}},\ \hat{H}_{\text{Starkregen}}\bigr)$$"),
    }],
}


def formula_operators_for(code: str, formula: str) -> list[OperatorStep]:
    """Explizite Schritte oder generischer Formel-Operator als Fallback."""
    if code in FORMULA_OPERATORS:
        return FORMULA_OPERATORS[code]
    return [{
        "op_kind": "formula",
        "label": "Formel",
        # Kennzeichnet den Fallback maschinell — der Honesty-Ratchet
        # (test_indicator_graphs_are_honest) lässt ihn nur noch für die
        # explizit gelisteten Rest-Codes zu.
        "generic": True,
        # "Berechnung:"-Präfix, damit das Frontend die Formel als LaTeX rendert
        "note": (
            f"Berechnung: {formula}" if formula else f"Berechnung für {code}."
        ),
    }]


# ── Sonstige-Ebenen (auxiliary): Ebene → Zellwert-Kette ─────────────────────
#
# Gleiches Konzept wie FORMULA_OPERATORS, für die Karten-Ebenen der Kategorie
# "Sonstige": jeder Katalog-Code wird auf seine echten Zell-/Regionalkeys
# (Kette inkl. Quellen und Operatoren, s. CELL_OPERATORS/CELL_DIRECT und
# lineage_graph.CELL_INPUT_LINEAGE) abgebildet — exakt die Keys, aus denen
# engine/auxiliary.build_auxiliary() den Kartenwert liest.
#
# Felder je Eintrag:
#   keys     Zell-/Regionalkeys, deren Kette expandiert wird (Pflicht).
#   steps    optionale zusätzliche Operator-Schritte zwischen Kette und
#            Ergebnis (z. B. Invertierung); None = Wert wird direkt übernommen.
#   formula  ehrlicher Kurztext der Berechnung für Ergebnis-Tooltip und
#            Rezept-Panel; None = "Direkt übernommen aus <Quelle>".
#
# Die Karten zeigen ROHWERTE — deshalb enthält keine Sonstige-Kette einen
# Normierungs-Schritt (per Ratchet-Test test_auxiliary_graphs_are_honest
# erzwungen; ebenso die Vollständigkeit: jeder AUXILIARY-Code hat einen
# Eintrag). Ebenen mit inhärent normiertem Kartenwert (z. B. TWI_NORMALIZED)
# erklären das im Ableitungsschritt selbst.

AUX_LINEAGE: dict[str, dict[str, Any]] = {
    # — Bevölkerung & Wohnen (Zensus) — Werte kommen fertig aus dem
    # Destatis-100-m-Gitter (keine eigene Mittelung/Anteilsbildung); einzige
    # eigene Ableitungen: pop_over_65/pop_under_18 (Multiplikation) und
    # building_age_mean (Klassenmitten-Mittel).
    "POPULATION_COUNT": {"keys": ["pop"]},
    "SHARE_OVER_65": {"keys": ["share_over_65"]},
    "SHARE_UNDER_18": {"keys": ["share_under_18"]},
    "POPULATION_OVER_65": {"keys": ["pop_over_65"], "formula": "Einwohner der Zelle · Anteil ≥ 65 Jahre / 100"},
    "POPULATION_UNDER_18": {"keys": ["pop_under_18"], "formula": "Einwohner der Zelle · Anteil < 18 Jahre / 100"},
    "LIVING_AREA_PER_PERSON": {"keys": ["living_area_per_person"]},
    "NET_COLD_RENT": {"keys": ["net_cold_rent"]},
    "OWNER_SHARE": {"keys": ["owner_share"]},
    "BUILDING_COUNT_ZENSUS": {"keys": ["building_count_zensus"]},
    "BUILDING_AGE_MEAN": {
        "keys": ["building_age_mean"],
        "formula": ("Gebäudegewichtetes Mittel der Baujahrsklassen-Mitten aus "
                    "dem Zensus-Raster; Lücken aus der 1-km-Zelle imputiert"),
    },

    # — Gesundheit (OSM) —
    "HEALTHCARE_ACCESS_GRID": {
        "keys": ["healthcare_access_score"],
        "steps": [{
            "op_kind": "scale_factor", "label": "×", "factor": 100,
            "param_label": "Skalierung auf Index",
            "note": "Berechnung: Erreichbarkeits-Score · 100 → Index 0…100",
        }],
        "formula": "Erreichbarkeits-Score · 100 → Index 0…100",
    },
    "HEALTHCARE_INDEX_HOSPITAL": {
        "keys": ["dist_hospital_m"],
        "steps": [{
            "op_kind": "distance_score", "label": "Gewichteten Nähe-Beitrag berechnen",
            "note": ("Berechnung: 0,50 · Nähe Krankenhaus\n"
                     "Nähe = max(0; 1 − effektive Distanz / Maximaldistanz)."),
        }],
        "formula": "0,50 · Nähe Krankenhaus — Beitrag zum Erreichbarkeits-Score",
    },
    "HEALTHCARE_INDEX_DOCTOR": {
        "keys": ["dist_doctor_m"],
        "steps": [{
            "op_kind": "distance_score", "label": "Gewichteten Nähe-Beitrag berechnen",
            "note": ("Berechnung: 0,35 · Nähe Arzt/Klinik\n"
                     "Nähe = max(0; 1 − effektive Distanz / Maximaldistanz)."),
        }],
        "formula": "0,35 · Nähe Arzt/Klinik — Beitrag zum Erreichbarkeits-Score",
    },
    "HEALTHCARE_INDEX_PHARMACY": {
        "keys": ["dist_pharmacy_m"],
        "steps": [{
            "op_kind": "distance_score", "label": "Gewichteten Nähe-Beitrag berechnen",
            "note": ("Berechnung: 0,15 · Nähe Apotheke\n"
                     "Nähe = max(0; 1 − effektive Distanz / Maximaldistanz)."),
        }],
        "formula": "0,15 · Nähe Apotheke — Beitrag zum Erreichbarkeits-Score",
    },
    "HEALTHCARE_ACCESS_INDEX": {
        "keys": ["healthcare_access_score"],
        "steps": [{
            "op_kind": "formula", "label": "Zugang invertieren",
            "note": ("Berechnung: 100 · (1 − Erreichbarkeits-Score)\n"
                     "Hohe Werte bedeuten schlechten Zugang zu "
                     "Gesundheitseinrichtungen."),
        }],
        "formula": "100 · (1 − Erreichbarkeits-Score); hohe Werte = schlechter Zugang",
    },
    "HEALTHCARE_ACCESS_SCORE": {
        "keys": ["healthcare_access_score"],
        "formula": ("0,50 · Nähe Krankenhaus + 0,35 · Nähe Arzt + "
                    "0,15 · Nähe Apotheke (Score 0…1)"),
    },
    "HOSPITAL_DISTANCE_M": {"keys": ["dist_hospital_m"], "formula": "Entfernung zum nächsten Krankenhaus in Metern"},
    "DOCTOR_DISTANCE_M": {"keys": ["dist_doctor_m"], "formula": "Entfernung zur nächsten Arztpraxis/Klinik in Metern"},
    "PHARMACY_DISTANCE_M": {"keys": ["dist_pharmacy_m"], "formula": "Entfernung zur nächsten Apotheke in Metern"},

    # — Oberfläche & Bebauung (OSM) —
    "IMPERVIOUS_FRACTION": {"keys": ["imp_frac"], "formula": "Gebäudeanteil + 0,95 · Straßenanteil; Fallback Landnutzung"},
    "GREEN_FRACTION": {"keys": ["green_frac"], "formula": "Grünfläche / Zellfläche"},
    "WATER_FRACTION": {"keys": ["water_frac"], "formula": "Wasserfläche / Zellfläche"},
    "FOREST_FRACTION": {"keys": ["forest_frac"], "formula": "Waldfläche / Zellfläche"},
    "FARMLAND_FRACTION": {"keys": ["farmland_frac"], "formula": "Ackerfläche / Zellfläche"},
    "BUILDING_COVERAGE": {"keys": ["bldg_cov"], "formula": "Gebäudegrundrissfläche / Zellfläche"},
    "BUILDING_COUNT": {"keys": ["bldg_count"], "formula": "Anzahl der Gebäude-Polygone in der Zelle"},
    "ENERGY_INFRA_COUNT": {"keys": ["energy_infra_count"], "formula": "Gewichtete Kritikalitätspunkte der Energie-Assets der Zelle"},
    "WATER_WASTEWATER_COUNT": {"keys": ["water_wastewater_count"], "formula": "Gewichtete Kritikalitätspunkte der Wasser-/Abwasseranlagen"},
    "COMMUNICATION_INFRA_COUNT": {"keys": ["communication_count"], "formula": "Gewichtete Kritikalitätspunkte der Kommunikationsanlagen"},
    "AVG_BUILDING_HEIGHT": {"keys": ["avg_height"], "formula": "Flächengewichteter Mittelwert der Gebäudehöhen (LoD2, sonst OSM-Heuristik)"},
    "ROAD_COVERAGE": {"keys": ["road_cov"], "formula": "Straßenfläche / Zellfläche"},
    "TREE_CANOPY": {"keys": ["canopy_frac"], "formula": "Baumkronenfläche / Zellfläche"},
    "SKY_VIEW_FACTOR": {"keys": ["svf"], "formula": "SVF = 1 − (1/N) · Σ sin²γ; N = 16 Richtungen, 100-m-Radius"},
    "SURFACE_ALBEDO": {"keys": ["albedo"], "formula": "Flächengewichteter Albedo-Mittelwert der Landnutzungsklassen"},
    "INDUSTRIAL_FRACTION": {"keys": ["industrial"], "formula": "max(0; Versiegelung − Gebäudeanteil − Straßenanteil)"},
    "VENTILATION_SCORE": {"keys": ["vent_score"], "formula": "Offene/grüne Nachbarzellen / 8 Nachbarn"},

    # — Gelände & Hydrologie (DEM) —
    "MEAN_ELEVATION": {"keys": ["mean_elevation_m"], "formula": "Mittelwert der Geländehöhe über die Höhenrasterpunkte der Zelle"},
    "SLOPE_DEGREES": {"keys": ["slope_deg"], "formula": "Hangneigung in Grad aus dem Höhenraster (Horn-Operator)"},
    "SINK_DEPTH": {"keys": ["sink_depth_m"], "formula": "max(0; mittlere Nachbarhöhe − Zellhöhe)"},
    "TWI": {"keys": ["twi"], "formula": "TWI = ln(A / tan β); A = Flussakkumulation · Zellfläche, β = Hangneigung"},
    "TWI_NORMALIZED": {"keys": ["twi_norm"], "formula": "Min-Max-Normierung des TWI über alle Zellen der Kommune → 0…1"},
    "DEPRESSION_FACTOR": {
        "keys": ["depression_factor"],
        "formula": ("min(1; 0,55 · TWI normiert + 0,45 · Senkentiefe normiert); "
                    "ohne DEM: 0,5 · Versiegelung + 0,5 · Gewässernähe − 0,2 · Belüftung"),
    },
    "SLOPE_FACTOR": {
        "keys": ["slope_factor"],
        "formula": ("Hangneigung min-max-normiert über alle Zellen → 0…1; "
                    "ohne DEM: 0,3 + 0,4 · (1 − Belüftung)"),
    },
    "FLOW_ACCUMULATION": {"keys": ["flow_accum"], "formula": "D8-Abflussakkumulation aus dem Höhenraster (Anzahl Oberlieger-Zellen)"},

    # — Gewässer (OSM) —
    "WATER_DISTANCE": {"keys": ["water_dist_m"], "formula": "Entfernung zum nächsten echten Gewässer in Metern (ohne Gräben)"},
    "WATER_PROXIMITY": {"keys": ["water_prox"], "formula": "max(0; 1 − Distanz / 500 m); Gräben nur schwacher Zusatzbeitrag"},
    "WATER_ADJACENCY": {
        "keys": ["water_adj"],
        "formula": ("max(Wasseranteil der 8 Nachbarzellen; Gewässernähe-Score; "
                    "Wasseranteil der Zelle)"),
    },

    # — Klima regional (DWD u. a.) —
    "HOT_DAYS": {"keys": ["hot_days"], "formula": "DWD-CDC-Raster (1 km) am Kommune-Zentroid; Fallback Bundesland-Mittel"},
    "FROST_DAYS": {"keys": ["frost_days"], "formula": "DWD-CDC-Raster am Kommune-Zentroid; Fallback Proxy aus Jahresmitteltemperatur"},
    "MEAN_ANNUAL_TEMP": {"keys": ["mean_temp"], "formula": "DWD-Gebietsmittel des Bundeslands"},
    "DROUGHT_DAYS": {"keys": ["drought_days"], "formula": "Proxy: 8 + 1,2 · heiße Tage"},
    "DRYNESS_INDEX": {"keys": ["dry_index"], "formula": "Proxy: min(1; heiße Tage / 25)"},
    "STORM_DAYS": {"keys": ["storm_days"], "formula": "ERA5-Böenklimatologie (Tage ≥ 25 m/s) am Zentroid; Fallback regionaler Konstantwert"},
    "HEAVY_RAIN_INDEX": {"keys": ["heavy_rain_index"], "formula": "min(100; Tage ≥ 20 mm · 4 + Tage ≥ 30 mm · 6); Fallback Proxy aus Jahresmitteltemperatur"},
    "TEMPERATURE_RISE": {"keys": ["mean_temp_rise"], "formula": "Proxy: 1,6 + 0,1 · (Jahresmittel − 9,5 °C)"},
    "SOIL_MOISTURE_DECLINE": {"keys": ["soil_moisture_decline"], "formula": "Proxy: 20 + heiße Tage"},
    "LOW_FLOW_DAYS": {"keys": ["low_flow_days"], "formula": "Tage < MNW am nächsten Pegel; Fallback 10 + heiße Tage"},
    "SURFACE_WATER_HEATING_REGIONAL": {"keys": ["surface_water_heating"], "formula": "Proxy: 1,5 + 0,2 · (Jahresmittel − 9,5 °C)"},
    "SEA_LEVEL_RISE": {"keys": ["sea_level_rise"], "formula": "Regionaler Anstieg aus Pegeldaten; nur Küstenkommunen, sonst 0"},

    # ── Hitzemodell ───────────────────────────────────────────────────────────
    "SUMMER_MEAN_TEMP": {
        "keys": ["summer_temp_raster"],
        "formula": ("Mittel der DWD-Monatsraster Juni/Juli/August (1 km) über die "
                    "Klimatologie-Jahre, am Zellmittelpunkt abgegriffen"),
    },
    "SUMMER_NIGHT_TEMP": {
        "keys": ["summer_night_temp"],
        "formula": ("Mittel der DWD-Monatsraster der Tagesminima Juni/Juli/August "
                    "(1 km) — die Größe, auf die die Wärmeinsel am stärksten wirkt"),
    },
    "UHI_DELTA_DAY": {
        "keys": ["uhi_delta"],
        "formula": ("Tagesmaximum der Wärmeinsel aus Albedo, Versiegelung, "
                    "Gebäudedichte × Höhe, Sky-View-Faktor, Grün-, Baum- und "
                    "Wasseranteil"),
    },
    "UHI_DELTA_MEAN": {
        "keys": ["uhi_delta_mean"],
        "steps": [{
            "op_kind": "weighted_sum",
            "label": "Tag/Nacht gewichten",
            "note": ("Tages- und Nachtwärmeinsel zum 24-h-Mittel kombinieren, dann "
                     "mit dem Luftaustausch zum Umland dämpfen. Die Wirkungskurve "
                     "läuft über die Wochenmitteltemperatur und damit über Tag UND "
                     "Nacht — nicht über das Tagesmaximum.\n"
                     r"$$\Delta T_{\varnothing} = \bigl[(1-w)\,\Delta T_{\mathrm{Tag}}"
                     r" + w\,\Delta T_{\mathrm{Nacht}}\bigr]\cdot f_{\varnothing}"
                     r"\cdot (1 - r_{\mathrm{Lüftung}}\cdot v)$$"),
            "input_keys": ["uhi_delta", "uhi_delta_night", "vent_score"],
        }],
        "formula": ("Tag/Nacht-gewichtetes Wärmeinsel-Mittel, gedämpft durch die "
                    "Durchlüftung der Zelle"),
    },
    "CELL_SUMMER_TEMP": {
        "keys": ["summer_temp_cell"],
        "steps": [{
            "op_kind": "add",
            "label": "+",
            "note": ("Rasterwert plus Wärmeinsel-Abweichung plus Höhenkorrektur — "
                     "beide Zuschläge MITTELWERTTREU innerhalb der 1-km-Rasterzelle. "
                     "Das DWD-Raster enthält die Wärmeinsel bereits teilweise; würde "
                     "man das volle ΔT addieren, zählte man den erfassten Anteil "
                     "doppelt. So bleibt das 1-km-Mittel der gemessene Wert und nur "
                     "die Feinstruktur darunter stammt aus dem Stadtmodell.\n"
                     r"$$T_{\mathrm{Zelle}} = T_{\mathrm{Raster}}"
                     r" + \bigl(\Delta T_{\varnothing} - \overline{\Delta T_{\varnothing}}\bigr)"
                     r" - \gamma\,\bigl(h - \bar{h}\bigr)$$"),
            "input_keys": ["summer_temp_raster", "summer_temp_uhi_dev", "summer_temp_lapse"],
        }],
        "formula": "Rasterwert + mittelwerttreue Wärmeinsel-Abweichung + Höhenkorrektur",
    },
    "HEAT_EXCESS_WEEKS": {
        "keys": ["summer_temp_cell"],
        "steps": [{
            "op_kind": "erf",
            "label": "Übertemperatur summieren",
            "note": ("Summe der Wochenmitteltemperaturen über der regionalen "
                     "Wirkschwelle (19,7/20,2/20,8 °C je Region). Die Wochenwerte "
                     "sind die Quantile der Sommerverteilung um die Zelltemperatur — "
                     "am Mittelwert ausgewertet käme fast überall null heraus, denn "
                     "das deutsche Sommermittel liegt UNTER der Schwelle.\n"
                     r"$$E = \sum_{w=1}^{13} \bigl(T_{w} - T_{0}\bigr)_{+}$$"),
            "input_keys": ["summer_temp_cell"],
        }],
        "formula": "Summe der Übertemperatur aller Sommerwochen über der Wirkschwelle",
    },
    "HEAT_RELATIVE_RISK": {
        "keys": ["summer_temp_cell"],
        "steps": [{
            "op_kind": "erf",
            "label": "Wirkungskurve anwenden",
            "note": ("Relatives Sterberisiko nach RKI/Winklmayr, gemittelt über die "
                     "Altersbänder und mit deren Bevölkerung gewichtet.\n"
                     r"$$\mathrm{RR}_{a}(T) = e^{\beta_{a}\,(T - T_{0})_{+}}$$"),
            "input_keys": ["summer_temp_cell", "pop_age_bands"],
        }],
        "formula": "Bevölkerungsgewichtetes relatives Sterberisiko der Zelle",
    },
    "FLOOD_REGIME": {
        "keys": ["slope_factor", "depression_factor"],
        "steps": [{
            "op_kind": "multiply",
            "label": "×",
            "note": ("Sturzflut-Anteil aus Hangneigung und Senkenlage. Ohne Hydraulik "
                     "(keine Wassertiefe, keine Fließgeschwindigkeit) ist das Gelände "
                     "der einzige belastbare Unterscheider — und zugleich der "
                     "wichtigste: Enge Steiltäler erzeugen schnelle, tödliche Fluten, "
                     "flache Auen langsame.\n"
                     r"$$R = s \cdot \bigl(0{,}5 + 0{,}5\,d\bigr)$$"),
            "input_keys": ["slope_factor", "depression_factor"],
        }],
        "formula": "Hangneigung × (0,5 + 0,5 · Senkenfaktor), begrenzt auf 0…1",
    },
    "POPULATION_65_74": {
        "keys": ["pop_over_65"],
        "formula": ("Einwohner ≥ 65 der Zelle × Anteil des Bands 65–74 aus den "
                    "Zensus-5-Jahres-Gruppen"),
    },
    "POPULATION_75_84": {
        "keys": ["pop_over_65"],
        "formula": ("Einwohner ≥ 65 der Zelle × Anteil des Bands 75–84 aus den "
                    "Zensus-5-Jahres-Gruppen"),
    },
    "POPULATION_85_PLUS": {
        "keys": ["pop_over_65"],
        "formula": ("Einwohner ≥ 65 der Zelle × Anteil des Bands 85+ aus den "
                    "Zensus-5-Jahres-Gruppen"),
    },
}


def aux_formula_text(code: str, source: str = "") -> str:
    """Ehrlicher Berechnungstext einer Sonstige-Ebene (Tooltip + Rezept-Panel)."""
    spec = AUX_LINEAGE.get(code) or {}
    if spec.get("formula"):
        return str(spec["formula"])
    if source:
        return f"Direkt übernommen aus: {source}"
    return "Direkt aus der Datenquelle übernommen"
