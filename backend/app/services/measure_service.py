"""Maßnahmen-Engine (generalisiert für alle KAP3-Maßnahmen).

Eine Maßnahme reduziert ihre Zielkomponente(n) (``effect_target`` ∈ hazard/
exposure/vulnerability) in den abgedeckten Zellen, deckungs-skaliert. Da der
Risiko-Index multiplikativ in H·E·V ist, lässt sich die Wirkung auf die
verknüpften Risiken (``linked_risk_codes``) analytisch als Skalierung des Index
abbilden:

    factor = (1 - r_applied) ** n_targets
    neuer_Index = Basis-Index × factor

mit ``r_applied`` aus ``default_reduction`` und Deckungsgrad der Zelle.
Kosten/Nutzen je Maßnahme werden aus den Katalog-Kostensätzen plus der
monetarisierten Schadensreduktion (für monetäre Risiken) bestimmt.
"""

from __future__ import annotations

import logging

from geoalchemy2 import functions as func
from sqlalchemy import case, literal
from sqlalchemy.orm import Session

from app.data import catalog, sources
from app.models.models import (
    AdaptationMeasure, CellAssessment, GridCell, MeasureImpact, Kommune,
)
from app.services import parameter_registry
from app.services.engine import risk_engine

log = logging.getLogger(__name__)


def _coverage(db: Session, measure: AdaptationMeasure) -> tuple[dict[int, float], float]:
    """Deckungsgrad (0..1) je Zelle plus abgedeckte Gesamtfläche (m²).

    Die Fläche wird als Σ (cell_size_m² · frac) über alle schneidenden Zellen
    bestimmt; die 3857-Verzerrung kürzt sich im frac-Verhältnis heraus. Sie wird
    hier zentral berechnet, weil sowohl die Kosten- als auch die Wirkungs-
    skalierung (unit_factor) die Gesamtfläche vor der Zell-Schleife brauchen.
    """
    cell_area = func.ST_Area(func.ST_Transform(GridCell.geometry, 3857))
    inter = func.ST_Area(func.ST_Transform(
        func.ST_Intersection(GridCell.geometry, measure.geometry), 3857))
    frac = case((cell_area > 0, inter / cell_area), else_=literal(0.0))
    rows = (
        db.query(GridCell.id, GridCell.cell_size_m, frac.label("frac"))
        .filter(GridCell.kommune_id == measure.kommune_id,
                func.ST_Intersects(GridCell.geometry, measure.geometry))
        .all()
    )
    frac_map: dict[int, float] = {}
    covered_area_m2 = 0.0
    for r in rows:
        f = max(0.0, min(1.0, float(r.frac)))
        frac_map[r.id] = f
        size = float(r.cell_size_m or 100)
        covered_area_m2 += (size ** 2) * f
    return frac_map, covered_area_m2


def _reduction_factor(mdef: dict, fraction: float, unit_factor: float = 1.0) -> float:
    """Kombinierter Skalierungsfaktor (0..1) für den Risiko-Index einer Zelle.

    ``unit_factor`` (0..1) skaliert die Wirkung von Stück-Maßnahmen anhand der
    Anzahl gegenüber dem Richtwert (min(1, Anzahl/Richtwert)); für Flächen-
    maßnahmen ist er 1.0 und lässt die bisherige Rechnung unverändert.
    """
    base_r = float(mdef.get("default_reduction", 0.0))
    if mdef.get("coverage_scaling") == "saturating":
        r = base_r * min(1.0, fraction * 1.5)
    else:
        r = base_r * fraction
    r = r * unit_factor
    r = max(0.0, min(0.95, r))
    n = max(1, len(mdef.get("effect_target", []) or []))
    return (1.0 - r) ** n


def _resolve_count(
    mdef: dict, config: dict | None, covered_area_m2: float
) -> tuple[int, bool, int]:
    """Stückzahl, Default-Flag und Richtwert-Anzahl einer Maßnahme.

    Flächenmaßnahmen (``unit_label`` is None) haben keine Stück-Logik ⇒
    (0, False, 0). Fehlt ``config["count"]``, greift die Richtwert-Anzahl aus der
    Dichte als Default (``is_default=True``), damit Bestandsmaßnahmen ohne
    Frontend-Eingabe weiter sinnvoll rechnen.
    """
    if mdef.get("unit_label") is None:
        return 0, False, 0
    density = float(mdef.get("unit_density_per_ha") or 0.0)
    recommended = max(1, round(density * covered_area_m2 / 10_000))
    raw = (config or {}).get("count")
    if raw is None:
        return recommended, True, recommended
    return max(0, int(round(float(raw)))), False, recommended


def _unit_effect_factor(count: int, recommended_count: int) -> float:
    """Wirkungs-Skalierung 0..1 aus Anzahl vs. Richtwert (1.0 ohne Stück-Logik)."""
    if recommended_count > 0:
        return min(1.0, count / recommended_count)
    return 1.0


# Kostenkomponenten je Block (CAPEX einmalig / OPEX jährlich). quantity_kind:
# fixed = mengenunabhängige Pauschale (Menge 1), unit = Stückzahl (Einheit = unit_label),
# area = Fläche (Einheit m²).
_CAPEX_COMPONENTS: tuple[tuple[str, str, str], ...] = (
    ("capex_fixed", "Grundkosten (Planung/Konzept)", "fixed"),
    ("capex_per_unit", "Investition je {unit}", "unit"),
    ("capex_per_m2", "Investition je m²", "area"),
)
_OPEX_COMPONENTS: tuple[tuple[str, str, str], ...] = (
    ("opex_fixed_year", "Feste Betriebskosten/Jahr", "fixed"),
    ("opex_per_unit_year", "Betrieb & Unterhalt je {unit}/Jahr", "unit"),
    ("opex_per_m2_year", "Betrieb & Unterhalt je m²/Jahr", "area"),
)


def _component_source(mdef: dict, field: str) -> tuple[str, str, bool]:
    """(Quelle, Herleitung/Detail, overridden) einer Kostenkomponente.

    ``source`` ist das kurze Inline-Label (z. B. "Berliner Wasserbetriebe"),
    ``detail`` die ausführliche Herleitung/Volltext-Quelle für den Hover-Tooltip:
    woher der Zahlenwert stammt bzw. – wenn er nicht direkt einer Quelle entnommen
    ist – wie er hergeleitet/plausibilisiert wurde. Ein kommunaler
    ``custom_source``-Override hat beim Kurz-Label Vorrang.
    """
    custom = (mdef.get("custom_sources") or {}).get(field)
    detail = (mdef.get("source_details") or {}).get(field) or ""
    if custom:
        return custom, detail, True
    source = (mdef.get("sources") or {}).get(field) or mdef.get("source") or ""
    return source, detail, False


def compute_costs(mdef: dict, count: int, area_m2: float) -> dict:
    """Kosten-Rohdaten (capex + opex) mit Komponenten-Breakdown.

    CAPEX  = capex_fixed + count·capex_per_unit + area·capex_per_m2,
    OPEX/a = opex_fixed_year + count·opex_per_unit_year + area·opex_per_m2_year.
    Nur Komponenten, deren Katalogfeld ``is not None`` ist, tauchen auf; ``0.0``
    gilt als anwendbar (z. B. kostenlose Bauverbote). Jede Komponente trägt
    Einzelpreis, Menge, Betrag und Quelle inkl. Override-Flag.
    """
    unit_label = mdef.get("unit_label") or "Einheit"

    def _block(specs: tuple[tuple[str, str, str], ...]) -> dict:
        components: list[dict] = []
        total = 0.0
        for field, label_tpl, kind in specs:
            unit_price = mdef.get(field)
            if unit_price is None:
                continue
            unit_price = float(unit_price)
            if kind == "unit":
                quantity, quantity_unit = count, unit_label
            elif kind == "area":
                quantity, quantity_unit = round(float(area_m2), 2), "m²"
            else:  # fixed
                quantity, quantity_unit = 1, "pauschal"
            amount = round(unit_price * quantity, 2)
            total += amount
            source, source_detail, overridden = _component_source(mdef, field)
            refs = sources.resolve((mdef.get("source_refs") or {}).get(field))
            components.append({
                "param": field,
                "label": label_tpl.format(unit=unit_label),
                "unit_price": unit_price,
                "quantity": quantity,
                "quantity_unit": quantity_unit,
                "amount_eur": amount,
                "source": source,
                "source_detail": source_detail,
                "references": refs,
                "overridden": overridden,
            })
        return {"total_eur": round(total, 2), "components": components}

    return {
        "capex": _block(_CAPEX_COMPONENTS),
        "opex": _block(_OPEX_COMPONENTS),
    }


def _measure_custom_sources(db_overrides: list[dict], measure_code: str) -> dict[str, str]:
    """Per-Feld ``custom_source``-Overrides einer Maßnahme (measures.<code>.<field>)."""
    prefix = f"measures.{measure_code}."
    out: dict[str, str] = {}
    for o in db_overrides:
        pid = o.get("parameter_id") or ""
        cs = o.get("custom_source")
        if cs and pid.startswith(prefix):
            out[pid[len(prefix):]] = cs
    return out


def compute_impact(db: Session, measure_id: int) -> dict:
    """Berechnet die Wirkung einer Maßnahme, speichert MeasureImpact und gibt
    eine Zusammenfassung (Index-Reduktion, Kosten, Nutzen) zurück."""
    measure = db.query(AdaptationMeasure).filter(AdaptationMeasure.id == measure_id).first()
    if not measure:
        raise ValueError(f"Maßnahme {measure_id} nicht gefunden")

    mdef = catalog.MEASURES_BY_CODE.get(measure.measure_type)
    if not mdef:
        raise ValueError(f"Unbekannter Maßnahmentyp: {measure.measure_type}")

    db_overrides = parameter_registry.load_db_overrides(db, measure.kommune_id)
    overrides = parameter_registry.overrides_map(db_overrides)
    mdef = parameter_registry.resolve_measure_def(mdef, overrides)
    mdef = {**mdef, "custom_sources": _measure_custom_sources(db_overrides, measure.measure_type)}

    coverage, covered_area_m2 = _coverage(db, measure)
    if not coverage:
        db.query(MeasureImpact).filter(MeasureImpact.measure_id == measure_id).delete()
        no_coverage = {"measure_id": measure_id, "affected_cells": 0, "message": "Keine überlappenden Zellen"}
        measure.impact_summary = no_coverage
        db.commit()
        return no_coverage

    # Anzahl/Wirkungsskalierung brauchen die Gesamtfläche vor der Zell-Schleife.
    count, count_is_default, recommended_count = _resolve_count(mdef, measure.config, covered_area_m2)
    unit_factor = _unit_effect_factor(count, recommended_count)

    linked = mdef.get("linked_risk_codes", [])
    cell_ids = list(coverage.keys())
    assessments = {
        ca.grid_cell_id: ca for ca in
        db.query(CellAssessment).filter(CellAssessment.grid_cell_id.in_(cell_ids)).all()
    }

    # Basis-Aggregat (für monetäre Nutzenbewertung)
    all_cells = db.query(CellAssessment).filter(
        CellAssessment.kommune_id == measure.kommune_id).all()
    total_index_by_risk: dict[str, float] = {}
    for ca in all_cells:
        for code in linked:
            total_index_by_risk[code] = total_index_by_risk.get(code, 0.0) + \
                float((ca.data or {}).get("risks", {}).get(code, {}).get("index", 0.0))

    base_agg = get_risk_aggregate(db, measure.kommune_id, apply_measures=False)

    db.query(MeasureImpact).filter(MeasureImpact.measure_id == measure_id).delete()

    covered_base_index: dict[str, float] = {}
    covered_new_index: dict[str, float] = {}

    for cid, frac in coverage.items():
        ca = assessments.get(cid)
        if not ca:
            continue
        factor = _reduction_factor(mdef, frac, unit_factor)
        deltas = {}
        for code in linked:
            base_idx = float((ca.data or {}).get("risks", {}).get(code, {}).get("index", 0.0))
            new_idx = base_idx * factor
            deltas[code] = round(new_idx - base_idx, 3)
            covered_base_index[code] = covered_base_index.get(code, 0.0) + base_idx
            covered_new_index[code] = covered_new_index.get(code, 0.0) + new_idx
        db.add(MeasureImpact(measure_id=measure_id, grid_cell_id=cid, indicator_deltas=deltas))

    # Kosten (CAPEX + OPEX, je fix/Stück/Fläche; None-Felder erzeugen keine Komponente)
    cost_breakdown = compute_costs(mdef, count, covered_area_m2)
    capex = cost_breakdown["capex"]["total_eur"]
    opex_annual = cost_breakdown["opex"]["total_eur"]
    annual_benefit_direct = float(mdef.get("benefit_per_m2_year") or 0.0) * covered_area_m2

    # Monetarisierte Schadensreduktion (nur monetäre Risiken)
    annual_benefit_damage = 0.0
    for code in linked:
        risk = catalog.RISKS_BY_CODE.get(code)
        if not risk or risk.get("cost_dimension") != "monetary":
            continue
        total_idx = total_index_by_risk.get(code, 0.0)
        if total_idx <= 0:
            continue
        risk_cost = base_agg["risks"].get(code, {}).get("cost_eur", 0.0)
        reduced_share = (covered_base_index.get(code, 0.0) - covered_new_index.get(code, 0.0)) / total_idx
        annual_benefit_damage += risk_cost * max(0.0, reduced_share)

    avg_reduction = 0.0
    if covered_base_index:
        tot_b = sum(covered_base_index.values())
        tot_n = sum(covered_new_index.values())
        avg_reduction = round((tot_b - tot_n) / tot_b * 100.0, 1) if tot_b > 0 else 0.0

    summary = {
        "measure_id": measure_id,
        "measure_type": measure.measure_type,
        "affected_cells": len(coverage),
        "affected_area_m2": round(covered_area_m2, 1),
        "linked_risk_codes": linked,
        "avg_index_reduction_pct": avg_reduction,
        "capex_eur": round(capex, 2),
        "opex_annual_eur": round(opex_annual, 2),
        "annual_benefit_eur": round(annual_benefit_direct + annual_benefit_damage, 2),
        "count": count,
        "count_is_default": count_is_default,
        "recommended_count": recommended_count,
        "unit_label": mdef.get("unit_label"),
        "unit_factor": round(unit_factor, 4),
        "cost_breakdown": cost_breakdown,
    }

    # Persistiert am Maßnahmen-Objekt (bereits in der Session geladen) statt an
    # einer per Nachfrage-Query gesuchten MeasureImpact-Zelle - so unabhängig von
    # Flush-Reihenfolge/Autoflush-Konfiguration die einzige Quelle der Wahrheit
    # für Export/cost-summary, ohne dass diese neu rechnen müssen.
    measure.impact_summary = summary
    db.commit()

    return summary


def _adjusted_cell_data(db: Session, kommune_id: int, apply_measures: bool) -> list[dict]:
    """Liefert Per-Zell-Daten (ggf. mit angewandten Maßnahmen) für Aggregation."""
    assessments = db.query(CellAssessment).filter(
        CellAssessment.kommune_id == kommune_id).all()
    base = {ca.grid_cell_id: (ca.data or {}) for ca in assessments}

    if not apply_measures:
        return [dict(d) for d in base.values()]

    # Maßnahmen-Faktoren je Zelle/Risiko (multiplikativ kombiniert). Fläche, Anzahl
    # und unit_factor werden pro Maßnahme genauso bestimmt wie in compute_impact,
    # damit Dashboard ("mit Maßnahmen") und Sidebar nicht divergieren.
    factors: dict[int, dict[str, float]] = {}
    measures = db.query(AdaptationMeasure).filter(
        AdaptationMeasure.kommune_id == kommune_id).all()
    overrides = parameter_registry.overrides_map(
        parameter_registry.load_db_overrides(db, kommune_id)
    )
    for m in measures:
        mbase = catalog.MEASURES_BY_CODE.get(m.measure_type)
        if not mbase:
            continue
        mdef = parameter_registry.resolve_measure_def(mbase, overrides)
        frac_map, covered_area_m2 = _coverage(db, m)
        count, _, recommended = _resolve_count(mdef, m.config, covered_area_m2)
        unit_factor = _unit_effect_factor(count, recommended)
        for cid, frac in frac_map.items():
            factor = _reduction_factor(mdef, frac, unit_factor)
            cell_factors = factors.setdefault(cid, {})
            for code in mdef.get("linked_risk_codes", []):
                cell_factors[code] = cell_factors.get(code, 1.0) * factor

    out = []
    for cid, data in base.items():
        new_data = {"risks": {}}
        risks = data.get("risks", {})
        cell_factors = factors.get(cid, {})
        for code, r in risks.items():
            idx = float(r.get("index", 0.0)) * cell_factors.get(code, 1.0)
            new_data["risks"][code] = {"index": idx}
        out.append(new_data)
    return out


def get_risk_aggregate(db: Session, kommune_id: int, apply_measures: bool = False) -> dict:
    """Aggregiertes Risiko (mit/ohne Maßnahmen) inkl. Kosten."""
    kommune = db.query(Kommune).filter_by(id=kommune_id).first()
    total_pop = float(kommune.population or 0) if kommune else 0.0
    area_km2 = float(kommune.area_km2 or 0) if kommune else 0.0
    cell_data = _adjusted_cell_data(db, kommune_id, apply_measures)
    return risk_engine.aggregate(cell_data, total_pop, area_km2)
