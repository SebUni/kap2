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

from app.data import catalog
from app.models.models import (
    AdaptationMeasure, CellAssessment, GridCell, MeasureImpact, Kommune,
)
from app.services.engine import risk_engine

log = logging.getLogger(__name__)


def _coverage(db: Session, measure: AdaptationMeasure) -> dict[int, float]:
    """Deckungsgrad (0..1) je Zelle für eine Maßnahmen-Geometrie."""
    cell_area = func.ST_Area(func.ST_Transform(GridCell.geometry, 3857))
    inter = func.ST_Area(func.ST_Transform(
        func.ST_Intersection(GridCell.geometry, measure.geometry), 3857))
    frac = case((cell_area > 0, inter / cell_area), else_=literal(0.0))
    rows = (
        db.query(GridCell.id, frac.label("frac"))
        .filter(GridCell.kommune_id == measure.kommune_id,
                func.ST_Intersects(GridCell.geometry, measure.geometry))
        .all()
    )
    return {r.id: max(0.0, min(1.0, float(r.frac))) for r in rows}


def _reduction_factor(mdef: dict, fraction: float) -> float:
    """Kombinierter Skalierungsfaktor (0..1) für den Risiko-Index einer Zelle."""
    base_r = float(mdef.get("default_reduction", 0.0))
    if mdef.get("coverage_scaling") == "saturating":
        r = base_r * min(1.0, fraction * 1.5)
    else:
        r = base_r * fraction
    r = max(0.0, min(0.95, r))
    n = max(1, len(mdef.get("effect_target", []) or []))
    return (1.0 - r) ** n


def compute_impact(db: Session, measure_id: int) -> dict:
    """Berechnet die Wirkung einer Maßnahme, speichert MeasureImpact und gibt
    eine Zusammenfassung (Index-Reduktion, Kosten, Nutzen) zurück."""
    measure = db.query(AdaptationMeasure).filter(AdaptationMeasure.id == measure_id).first()
    if not measure:
        raise ValueError(f"Maßnahme {measure_id} nicht gefunden")

    mdef = catalog.MEASURES_BY_CODE.get(measure.measure_type)
    if not mdef:
        raise ValueError(f"Unbekannter Maßnahmentyp: {measure.measure_type}")

    coverage = _coverage(db, measure)
    if not coverage:
        db.query(MeasureImpact).filter(MeasureImpact.measure_id == measure_id).delete()
        db.commit()
        return {"measure_id": measure_id, "affected_cells": 0, "message": "Keine überlappenden Zellen"}

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

    kommune = measure.kommune
    base_agg = get_risk_aggregate(db, measure.kommune_id, apply_measures=False)

    covered_area_m2 = 0.0
    db.query(MeasureImpact).filter(MeasureImpact.measure_id == measure_id).delete()

    covered_base_index: dict[str, float] = {}
    covered_new_index: dict[str, float] = {}

    for cid, frac in coverage.items():
        ca = assessments.get(cid)
        if not ca:
            continue
        factor = _reduction_factor(mdef, frac)
        cell_size = ca.grid_cell.cell_size_m if ca.grid_cell else 100
        covered_area_m2 += (cell_size ** 2) * frac
        deltas = {}
        for code in linked:
            base_idx = float((ca.data or {}).get("risks", {}).get(code, {}).get("index", 0.0))
            new_idx = base_idx * factor
            deltas[code] = round(new_idx - base_idx, 3)
            covered_base_index[code] = covered_base_index.get(code, 0.0) + base_idx
            covered_new_index[code] = covered_new_index.get(code, 0.0) + new_idx
        db.add(MeasureImpact(measure_id=measure_id, grid_cell_id=cid,
                             indicator_deltas=deltas, costs={}, savings={}))

    # Kosten
    investment = float(mdef.get("cost_per_unit", 0.0)) + float(mdef.get("cost_per_m2", 0.0)) * covered_area_m2
    annual_maintenance = float(mdef.get("maintenance_per_m2_year", 0.0)) * covered_area_m2
    annual_benefit_direct = float(mdef.get("benefit_per_m2_year", 0.0)) * covered_area_m2

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

    # in MeasureImpact-Summen für Export spiegeln (an erste Zelle gehängt)
    first_imp = db.query(MeasureImpact).filter(MeasureImpact.measure_id == measure_id).first()
    if first_imp:
        first_imp.costs = {"investment": round(investment, 2),
                           "annual_maintenance": round(annual_maintenance, 2)}
        first_imp.savings = {"annual_benefit_direct": round(annual_benefit_direct, 2),
                             "annual_benefit_damage": round(annual_benefit_damage, 2)}

    db.commit()

    avg_reduction = 0.0
    if covered_base_index:
        tot_b = sum(covered_base_index.values())
        tot_n = sum(covered_new_index.values())
        avg_reduction = round((tot_b - tot_n) / tot_b * 100.0, 1) if tot_b > 0 else 0.0

    return {
        "measure_id": measure_id,
        "measure_type": measure.measure_type,
        "affected_cells": len(coverage),
        "affected_area_m2": round(covered_area_m2, 1),
        "linked_risk_codes": linked,
        "avg_index_reduction_pct": avg_reduction,
        "investment_eur": round(investment, 2),
        "annual_maintenance_eur": round(annual_maintenance, 2),
        "annual_benefit_eur": round(annual_benefit_direct + annual_benefit_damage, 2),
    }


def _adjusted_cell_data(db: Session, kommune_id: int, apply_measures: bool) -> list[dict]:
    """Liefert Per-Zell-Daten (ggf. mit angewandten Maßnahmen) für Aggregation."""
    assessments = db.query(CellAssessment).filter(
        CellAssessment.kommune_id == kommune_id).all()
    base = {ca.grid_cell_id: (ca.data or {}) for ca in assessments}

    if not apply_measures:
        return [dict(d) for d in base.values()]

    # Maßnahmen-Faktoren je Zelle/Risiko (multiplikativ kombiniert)
    factors: dict[int, dict[str, float]] = {}
    measures = db.query(AdaptationMeasure).filter(
        AdaptationMeasure.kommune_id == kommune_id).all()
    for m in measures:
        mdef = catalog.MEASURES_BY_CODE.get(m.measure_type)
        if not mdef:
            continue
        coverage = _coverage(db, m)
        for cid, frac in coverage.items():
            factor = _reduction_factor(mdef, frac)
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
