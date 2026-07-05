"""Plausibilitätsanker: Schicht-B-Summe gegen die ref_value-Größenordnung prüfen.

Die ``ref_value``/``scale`` eines Risikos sind nach der Umstellung auf Schadensfunktionen
kein Rechenweg mehr, sondern **Kalibrier-/Sanity-Anker** (MODELL_KRITIK §6.6): Der über
Zellen summierte Impact-Outcome sollte in derselben Größenordnung liegen wie die grobe
Referenzschätzung ``ref_value · (Gesamtbevölkerung/100.000)``. Grobe Abweichungen (Faktor
> ``TOLERANCE``) deuten auf eine Fehlkalibrierung eines Parameters hin und werden geloggt.
"""

from __future__ import annotations

import logging

from app.data import catalog

log = logging.getLogger(__name__)

TOLERANCE = 5.0  # zulässiger Faktor Abweichung zwischen Summe und Referenzschätzung


def ref_estimate(risk: dict, total_pop: float, area_km2: float) -> float:
    """Grobe Referenzschätzung des Outcomes (ref_value × Kommune-Skalierung)."""
    ref = float(risk.get("ref_value", 0.0))
    scale = risk.get("scale", "pop")
    if scale == "pop":
        return ref * (total_pop / 100_000.0)
    if scale == "area":
        return ref * (area_km2 / 50.0)
    return ref


def check(code: str, outcome_sum: float, total_pop: float, area_km2: float) -> float | None:
    """Verhältnis Summe/Referenz; loggt bei grober Abweichung. ``None`` ohne Referenz."""
    risk = catalog.RISKS_BY_CODE.get(code)
    if risk is None:
        return None
    est = ref_estimate(risk, total_pop, area_km2)
    if est <= 0.0:
        return None
    ratio = outcome_sum / est
    if ratio > TOLERANCE or ratio < 1.0 / TOLERANCE:
        log.warning(
            "Sanity: %s Schicht-B-Summe %.2f weicht um Faktor %.1f von der "
            "ref_value-Schätzung %.2f ab (Parameter prüfen).",
            code, outcome_sum, ratio if ratio >= 1 else 1.0 / ratio, est,
        )
    return round(ratio, 3)
