"""Nationale Gesundheits-Referenzwerte: Kalibrier- und Validierungsanker.

Analog zu :mod:`app.data.germany_climate_reference`, aber für die Gesundheits-
Schadensfunktionen (``services/engine/impact/health.py``). Zwei Aufgaben:

1. **Kalibrierung** — Der über alle deutschen Zellen summierte Outcome muss in
   der Größenordnung der publizierten nationalen Schätzung liegen. Dafür trägt
   die Engine genau *einen* freien Skalierungsfaktor je Kanal
   (``risks.<CODE>.impact.calibration``); alle übrigen Koeffizienten stammen aus
   der Literatur.
2. **Validierung** — Die modellierte **Altersverteilung** muss die publizierte
   treffen. Das ist der eigentliche Prüfstein der Altersschichtung: Ein Modell
   kann die Gesamtzahl über den Skalierungsfaktor immer treffen, die Verteilung
   über die Altersbänder aber nur, wenn die Expositions-Wirkungs-Kurven je Band
   stimmen.

Die Zahlen sind Punktschätzer der jeweiligen Quelle, keine Modellannahmen. Wo
keine belastbare Quelle vorliegt, steht bewusst ``None`` (Muster aus
``germany_climate_reference``), damit die Lücke sichtbar bleibt statt durch eine
erfundene Zahl gefüllt zu werden.
"""

from __future__ import annotations

# ── Hitzebedingte Sterbefälle je Jahr (RKI / Winklmayr u. a.) ─────────────────
# Statistisch signifikante Jahre aus Winklmayr u. a. 2022 (Tabelle + eTabelle,
# Dtsch Arztebl Int 119:451-7), fortgeschrieben aus den RKI-Wochenberichten.
# Nicht signifikante Jahre sind bewusst nicht enthalten — sie sind mit Null
# verträglich und würden als „Messwerte“ missverstanden.
HEAT_DEATHS_BY_YEAR: dict[int, int] = {
    1994: 10_100,
    2003: 9_500,
    2006: 7_500,
    2010: 4_500,
    2013: 3_000,
    2015: 6_000,
    2018: 8_700,
    2019: 6_900,
    2020: 3_700,
}

# Referenzband für die Kalibrierung: Mittel der signifikanten Hitzejahre.
# Der nationale Modellsummenwert soll hier hineinfallen.
HEAT_DEATHS_REFERENCE: dict = {
    "value": round(sum(HEAT_DEATHS_BY_YEAR.values()) / len(HEAT_DEATHS_BY_YEAR)),
    "min": 3_000,
    "max": 10_100,
    "unit": "Todesfälle/Jahr",
    "period": "1992–2020 (signifikante Hitzejahre)",
    "label": "Hitzebedingte Sterbefälle Deutschland",
    "source_refs": ["Winklmayr_2022", "RKI_Hitzemortalitaet"],
}

# ── Altersverteilung der hitzebedingten Sterbefälle ───────────────────────────
# RKI-Wochenberichte Sommer 2026 (Stand KW 29, rund 9.800 Sterbefälle) — das
# jüngste Jahr mit publizierter Aufschlüsselung nach Altersgruppen.
# Schlüssel = Altersbänder der Engine (``zensus_loader.AGE_BAND_COLUMNS``).
HEAT_DEATHS_BY_AGE_BAND: dict[str, int] = {
    "u65": 630,
    "a65_74": 1_260,
    "a75_84": 2_460,
    "a85p": 5_420,
}

HEAT_DEATH_AGE_SHARES: dict[str, float] = {
    band: n / sum(HEAT_DEATHS_BY_AGE_BAND.values())
    for band, n in HEAT_DEATHS_BY_AGE_BAND.items()
}

HEAT_DEATHS_AGE_REFERENCE: dict = {
    "value": HEAT_DEATH_AGE_SHARES,
    "unit": "Anteil an den hitzebedingten Sterbefällen",
    "period": "2026 (bis KW 29)",
    "label": "Altersverteilung hitzebedingter Sterbefälle",
    "source_refs": ["RKI_Wochenbericht_Hitzemortalitaet"],
}

# ── Anteil der Wärmeinsel an der sommerlichen Sterblichkeit ───────────────────
# Unabhängige Gegenprobe für das ΔT-Modell (nicht für die Wirkungskurve):
# Iungman u. a. 2023 schätzen 4,33 % [3,37; 5,27] der sommerlichen Sterbefälle in
# 93 europäischen Städten als der städtischen Wärmeinsel zurechenbar.
UHI_ATTRIBUTABLE_SHARE_REFERENCE: dict = {
    "value": 0.0433,
    "min": 0.0337,
    "max": 0.0527,
    "unit": "Anteil der sommerlichen Sterbefälle",
    "period": "2015, 93 europäische Städte",
    "label": "Der Wärmeinsel zurechenbarer Anteil",
    "source_refs": ["Iungman_2023_UHI"],
}

# ── Todesfälle durch Hochwasser (kuratierte Ereignisliste) ────────────────────
# Die Verteilung ist extrem tail-lastig: Ein einziges Ereignis (2021) trägt den
# Großteil der Todesfälle der letzten Jahrzehnte. Ein Jahresmittel beschreibt
# deshalb eine Verteilung, die in den meisten Jahren null ist — das gehört
# überall dorthin, wo die Zahl auftaucht.
FLOOD_DEATH_EVENTS: dict[int, int] = {
    2021: 189,   # Ahr/Erft (RLP + NRW)
    2013: 4,     # Elbe/Donau, deutscher Anteil
    2002: 21,    # Elbe (Sachsen)
    1997: 0,     # Oder — Todesopfer nahezu ausschließlich PL/CZ
}
FLOOD_DEATHS_REFERENCE: dict = {
    "value": round(sum(FLOOD_DEATH_EVENTS.values()) / 35.0, 1),
    "unit": "Todesfälle/Jahr (annualisiert)",
    "period": "1990–2024",
    "label": "Hochwasserbedingte Todesfälle Deutschland",
    "source_refs": ["CEDIM_Hochwasser_2021", "Destatis_Todesursachen_23211"],
    "note": ("Stark tail-dominiert — allein 2021 trägt rund 80 % der Todesfälle "
             "des Zeitraums. Der Erwartungswert beschreibt keine typische Jahreslage."),
}

# ── Todesfälle durch Stürme (kuratierte Ereignisliste) ────────────────────────
STORM_DEATH_EVENTS: dict[int, int] = {
    2007: 13,    # Kyrill (deutscher Anteil; europaweit 47)
    2018: 8,     # Friederike
    2020: 2,     # Sabine
}
STORM_DEATHS_REFERENCE: dict = {
    "value": round(sum(STORM_DEATH_EVENTS.values()) / 20.0, 1),
    "unit": "Todesfälle/Jahr (annualisiert)",
    "period": "2005–2024",
    "label": "Sturmbedingte Todesfälle Deutschland",
    "source_refs": ["DWD_Sturmereignisse", "Destatis_Todesursachen_23211"],
}

# ── Altersspezifische Basissterblichkeit ──────────────────────────────────────
# Ersetzt die bisherige pauschale Rate von 1.130/100k. Ohne Altersdifferenzierung
# kann die Altersverteilung der hitzebedingten Sterbefälle nicht getroffen werden:
# Die 85+-Gruppe stellt rund 3 % der Bevölkerung, aber rund 55 % der Hitzetoten.
# Werte: Destatis-Sterbefälle je 100.000 Einwohner der jeweiligen Altersgruppe.
BASELINE_MORTALITY_PER_100K: dict[str, float] = {
    "u65": 180.0,
    "a65_74": 1_800.0,
    "a75_84": 4_600.0,
    "a85p": 15_500.0,
}
BASELINE_MORTALITY_REFERENCE: dict = {
    "value": BASELINE_MORTALITY_PER_100K,
    "unit": "Sterbefälle/100.000·Jahr",
    "period": "2023",
    "label": "Altersspezifische Basissterblichkeit",
    "source_refs": ["Destatis_Sterbefaelle_Altersgruppen"],
}


def heat_deaths_reference_band() -> tuple[float, float]:
    """(min, max) der publizierten Jahreswerte — Zielband der Kalibrierung."""
    return float(HEAT_DEATHS_REFERENCE["min"]), float(HEAT_DEATHS_REFERENCE["max"])
