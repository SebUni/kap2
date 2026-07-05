"""Legacy-Impact: der bisherige lineare Weg ``ref·Index/100·Zellskalierung``.

Fallback für alle Risiken ohne eigene Schicht-B-Impact-Funktion. Rechnet exakt wie
``risk_engine.cell_outcome`` + Monetarisierung über den Kostensatz — aber je Zelle,
sodass ``risk_engine.aggregate`` die Zell-Werte zur Kommune-Summe addieren kann.

Kein Top-Level-Import von ``impact`` in ``risk_engine`` (Zyklus-Vermeidung): dieses
Modul importiert ``risk_engine``, nicht umgekehrt; ``aggregate`` lädt ``impact`` lazy.
"""

from __future__ import annotations

from app.services.engine import risk_engine


def legacy_cell_impact(
    risk: dict, index: float, cell_pop: float, cell_area_km2: float | None = None
) -> dict:
    """Outcome + Kosten einer Zelle nach dem linearen Referenzwert-Modell."""
    area = cell_area_km2 if cell_area_km2 is not None else risk_engine.CELL_AREA_KM2
    outcome = risk_engine.cell_outcome(risk, index, cell_pop, area)
    return {"outcome": outcome, "cost_eur": risk_engine.cost_from_outcome(risk, outcome)}
