"""Deutschland-Referenzwerte für den Kommune-vs-Bundesmittel-Vergleich im Dashboard.

Jede Metrik trägt den bundesweiten Mittelwert samt Bezugsperiode und Quellen-Keys
(``source_refs`` → ``app.data.sources.SOURCE_REFERENCES``). Die Kommune-Werte im
Profil-Endpunkt stammen je nach Verfügbarkeit aus dem DWD-CDC-Raster am Zentroid
(Mittel der letzten verfügbaren Jahre) oder aus dem Bundesland-Gebietsmittel —
die Bezugsperiode der DE-Referenz wird deshalb je Wert mitgeliefert und im
Frontend ausgewiesen (Periodeninkonsistenz nicht verschweigen).

Werte: DWD vieljährige Mittelwerte 1991–2020 (Flächenmittel Deutschland) bzw.
DWD-CDC-Rasterklimatologien; Schneedeckentage als Mittel der 2020er Jahre
(konsistent zur Zeitreihe in ``services/climate/dwd_data.py``).
"""

from __future__ import annotations

GERMANY_CLIMATE_REFERENCE: dict[str, dict] = {
    "mean_temp_annual": {
        "value": 9.3,
        "unit": "°C",
        "period": "1991–2020",
        "label": "Jahresmitteltemperatur",
        "source_refs": ["DWD_VieljaehrigeMittel_1991_2020"],
    },
    "precipitation_mm": {
        "value": 791.0,
        "unit": "mm/Jahr",
        "period": "1991–2020",
        "label": "Jahresniederschlag",
        "source_refs": ["DWD_VieljaehrigeMittel_1991_2020"],
    },
    "hot_days": {
        "value": 8.8,
        "unit": "Tage/Jahr",
        "period": "1991–2020",
        "label": "Heiße Tage (Tmax ≥ 30 °C)",
        "source_refs": ["DWD_VieljaehrigeMittel_1991_2020", "DWD_Klimastatusbericht"],
    },
    "summer_days": {
        "value": 43.5,
        "unit": "Tage/Jahr",
        "period": "1991–2020",
        "label": "Sommertage (Tmax ≥ 25 °C)",
        "source_refs": ["DWD_VieljaehrigeMittel_1991_2020"],
    },
    "frost_days": {
        "value": 79.5,
        "unit": "Tage/Jahr",
        "period": "1991–2020",
        "label": "Frosttage (Tmin < 0 °C)",
        "source_refs": ["DWD_VieljaehrigeMittel_1991_2020"],
    },
    "tropical_nights": {
        "value": 0.6,
        "unit": "Nächte/Jahr",
        "period": "1991–2020",
        "label": "Tropennächte (Tmin ≥ 20 °C)",
        "source_refs": ["DWD_Klimastatusbericht"],
    },
    "snow_days": {
        "value": 22.0,
        "unit": "Tage/Jahr",
        "period": "2020er Jahre",
        "label": "Schneedeckentage (≥ 1 cm)",
        "source_refs": ["DWD_CDC_Rasterklimatologie"],
    },
    # Kein belastbares publiziertes DE-Flächenmittel für Starkregentage ≥ 20 mm
    # gefunden — value=None: das Frontend zeigt dann nur den Kommune-Wert ohne
    # DE-Vergleich. Nachtragen, sobald ein zitierfähiger Wert vorliegt.
    "precip_ge20_days": {
        "value": None,
        "unit": "Tage/Jahr",
        "period": None,
        "label": "Starkregentage (≥ 20 mm)",
        "source_refs": ["DWD_CDC_Rasterklimatologie"],
    },
}
