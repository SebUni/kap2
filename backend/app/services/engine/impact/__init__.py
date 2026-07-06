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

from app.data import catalog
from app.services.engine.impact.legacy import legacy_cell_impact

# Registry: Risiko-Code → Impact-Funktion (Signatur ``fn(risk, ctx: CellContext) -> dict``
# mit Rückgabe {"outcome", "cost_eur"}). Ab Stufe 4 gruppenweise befüllt; Risiken ohne
# Eintrag rechnen den linearen Legacy-Weg.
IMPACT_FUNCTIONS: dict[str, Callable] = {}


def _register() -> None:
    from app.services.engine.impact.health import HEALTH_IMPACTS
    from app.services.engine.impact.monetary import MONETARY_IMPACTS
    from app.services.engine.impact.environment import ENVIRONMENT_IMPACTS
    IMPACT_FUNCTIONS.update(HEALTH_IMPACTS)
    IMPACT_FUNCTIONS.update(MONETARY_IMPACTS)
    IMPACT_FUNCTIONS.update(ENVIRONMENT_IMPACTS)


_register()


def has(code: str) -> bool:
    """True, wenn für ``code`` eine eigene Schicht-B-Impact-Funktion registriert ist."""
    return code in IMPACT_FUNCTIONS


def lineage_kind(risk: dict) -> str:
    """Kategorisiert ein Risiko nach seinem tatsächlichen Schicht-B-Rechenweg.

    Grundlage für Wirkungsdiagramm (``lineage_graph``) und Formeltexte
    (``formulas.risk_recipe``): health | environment | monetary | indirect |
    restoration | consolidated_zero | index_only | flat.
    """
    from app.services.engine.impact.environment import ENVIRONMENT_IMPACTS
    from app.services.engine.impact.health import HEALTH_IMPACTS
    from app.services.engine.impact.monetary import MONETARY_IMPACTS

    code = risk["code"]
    if code in HEALTH_IMPACTS:
        return "health"
    if code in ENVIRONMENT_IMPACTS:
        return "environment"
    if code in MONETARY_IMPACTS:
        return "monetary"
    if code == "EXPECTED_INDIRECT_ECONOMIC_LOSS_EUR":
        return "indirect"
    if code == "EXPECTED_RESTORATION_COSTS_EUR":
        return "restoration"
    if code in catalog.CONSOLIDATED_INTO_INDIRECT_CODES:
        return "consolidated_zero"
    if code in catalog.INDEX_ONLY_RISK_CODES:
        return "index_only"
    return "flat"


def compute_cell_impacts(
    risk: dict, index: float, cell_pop: float, cell_area_km2: float | None = None
) -> dict:
    """Legacy-Einzelweg (Index + Bevölkerung) — für die Aggregat-Nachrechnung von
    Alt-Zelldaten ohne materialisierten Outcome. Bewusst OHNE Dispatch: Alt-Daten
    entstanden vor den Schicht-B-Funktionen und werden identisch (legacy) reproduziert."""
    return legacy_cell_impact(risk, index, cell_pop, cell_area_km2)


def compute_all_cell_impacts(ctx) -> dict[str, dict]:
    """Outcome + Kosten je Risiko für EINE Zelle (voller Dispatch, für den Runner).

    Registrierte Schicht-B-Funktionen erhalten die volle ``CellContext``; alle übrigen
    Risiken rechnen den linearen Legacy-Weg aus Zell-Index und -Bevölkerung.
    """
    out: dict[str, dict] = {}
    for risk in catalog.RISKS:
        code = risk["code"]
        fn = IMPACT_FUNCTIONS.get(code)
        if fn is not None:
            out[code] = fn(risk, ctx)
        else:
            out[code] = legacy_cell_impact(risk, ctx.indices.get(code, 0.0), ctx.pop)
    # k_indirekt-Konsolidierung der Folgekosten (nach den direkten Sektorschäden).
    from app.services.engine.impact.monetary import consolidate_indirect
    consolidate_indirect(out, ctx)
    return out
