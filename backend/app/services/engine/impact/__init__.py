"""Impact-Framework (Schicht B, Stufe 3): per-Zell-Outcome/Kosten je Risiko.

Design (MODELL_KRITIK §5/§6): Jedes Risiko liefert je Zelle einen absoluten Outcome
und – monetarisiert – Kosten. Die Kommune-Aggregation summiert diese Zell-Werte
(``risk_engine.aggregate``), statt P90-Index × Gesamtbevölkerung zu rechnen
(behebt den Karte↔Dashboard-Widerspruch aus §3.6).

Per-Risk-Dispatch statt globalem Feature-Flag: Risiken mit registrierter
``impact_function`` (ab Stufe 4, gruppenweise) nutzen diese; alle übrigen rechnen den
bisherigen linearen Weg ``ref·Index/100·Zellskalierung`` (``legacy_cell_impact``). So
lässt sich Schicht B risikoweise ausrollen, ohne dass die Aggregation zwei Pfade braucht.
"""

from __future__ import annotations

from typing import Callable

# Registry: Risiko-Code → Impact-Funktion. Wird ab Stufe 4 (health/monetary/…) befüllt.
# Signatur: fn(risk: dict, index: float, cell_pop: float, cell_area_km2: float) -> dict
#           mit Rückgabe {"outcome": float, "cost_eur": float}.
IMPACT_FUNCTIONS: dict[str, Callable] = {}


def has(code: str) -> bool:
    """True, wenn für ``code`` eine eigene Schicht-B-Impact-Funktion registriert ist."""
    return code in IMPACT_FUNCTIONS


def compute_cell_impacts(
    risk: dict, index: float, cell_pop: float, cell_area_km2: float | None = None
) -> dict:
    """Outcome + Kosten einer Zelle für ein Risiko (dispatch: registriert → sonst legacy)."""
    fn = IMPACT_FUNCTIONS.get(risk["code"])
    if fn is not None:
        return fn(risk, index, cell_pop, cell_area_km2)
    from app.services.engine.impact.legacy import legacy_cell_impact
    return legacy_cell_impact(risk, index, cell_pop, cell_area_km2)
