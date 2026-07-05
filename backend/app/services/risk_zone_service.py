"""Risikozonen (Connected-Component-Analyse) für einen Risiko-Code.

Arbeitet auf dem Risiko-Index (0..100) aus ``CellAssessment.data['risks']`` und
identifiziert zusammenhängende Cluster mit Index ≥ Schwelle. Zonen werden bei
Bedarf für einen einzelnen ``risk_code`` (= ``layer_code``) berechnet.
"""

import json
import logging
from collections import deque
from datetime import datetime

from geoalchemy2 import functions as func
from sqlalchemy.orm import Session

from app.models.models import CellAssessment, GridCell, RiskZone, RiskZoneCell

log = logging.getLogger(__name__)

# Index ≥ Schwelle → "Risikozone". Angehoben von 40→50 mit der Umstellung auf die
# Max-Kombination (Stufe 1, MODELL_KRITIK §3.1): der Index bildet jetzt die stärkste
# Wirkungskette ab (früher gewichteter Mittelwert, ~Faktor 1,5–2 niedriger). Die
# Schwelle bleibt damit auf demselben realen Belastungsniveau wie zuvor.
RISK_THRESHOLD = 50.0
LEVEL = 1


def _load_cell_risk(db: Session, kommune_id: int, risk_code: str):
    rows = (
        db.query(CellAssessment, GridCell.row_idx, GridCell.col_idx, GridCell.cell_size_m)
        .join(GridCell, GridCell.id == CellAssessment.grid_cell_id)
        .filter(CellAssessment.kommune_id == kommune_id)
        .all()
    )
    cell_map: dict[int, dict] = {}
    grid_idx: dict[tuple[int, int], int] = {}
    for ca, row_idx, col_idx, size in rows:
        idx = float((ca.data or {}).get("risks", {}).get(risk_code, {}).get("index", 0.0))
        cell_map[ca.grid_cell_id] = {"row": row_idx, "col": col_idx, "risk": idx, "cell_size_m": size}
        grid_idx[(row_idx, col_idx)] = ca.grid_cell_id
    return cell_map, grid_idx


def compute_risk_zones(db: Session, kommune_id: int, risk_code: str,
                       threshold: float = RISK_THRESHOLD) -> list[dict]:
    cell_map, grid_idx = _load_cell_risk(db, kommune_id, risk_code)
    if not cell_map:
        return []

    at_risk = {cid for cid, info in cell_map.items() if info["risk"] >= threshold}
    _delete_old_zones(db, kommune_id, risk_code)
    if not at_risk:
        db.commit()
        return []

    visited: set[int] = set()
    components: list[list[int]] = []
    for seed in at_risk:
        if seed in visited:
            continue
        comp: list[int] = []
        queue = deque([seed])
        visited.add(seed)
        while queue:
            cid = queue.popleft()
            comp.append(cid)
            info = cell_map[cid]
            r, c = info["row"], info["col"]
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if dr == 0 and dc == 0:
                        continue
                    nb = grid_idx.get((r + dr, c + dc))
                    if nb in at_risk and nb not in visited:
                        visited.add(nb)
                        queue.append(nb)
        components.append(comp)

    components.sort(key=len, reverse=True)
    now = datetime.utcnow()
    result = []
    for zi, comp in enumerate(components):
        risks = [cell_map[c]["risk"] for c in comp]
        area = sum(cell_map[c]["cell_size_m"] ** 2 for c in comp)
        zone = RiskZone(
            kommune_id=kommune_id, layer_code=risk_code, level=LEVEL, zone_index=zi,
            cell_count=len(comp), mean_risk=round(sum(risks) / len(risks), 2),
            max_risk=round(max(risks), 2), area_m2=round(area, 0), calculated_at=now,
        )
        db.add(zone)
        db.flush()
        for c in comp:
            db.add(RiskZoneCell(risk_zone_id=zone.id, grid_cell_id=c,
                                risk_score=round(cell_map[c]["risk"], 2)))
        result.append({"zone_index": zi, "cell_count": len(comp),
                       "mean_risk": zone.mean_risk, "max_risk": zone.max_risk,
                       "area_m2": zone.area_m2})
    db.commit()
    return result


def get_risk_zones_geojson(db: Session, kommune_id: int, risk_code: str) -> dict:
    # Bei Bedarf neu berechnen, falls noch keine Zonen vorliegen
    existing = (
        db.query(RiskZone)
        .filter(RiskZone.kommune_id == kommune_id, RiskZone.layer_code == risk_code)
        .count()
    )
    if existing == 0:
        compute_risk_zones(db, kommune_id, risk_code)

    zones = (
        db.query(RiskZone)
        .filter(RiskZone.kommune_id == kommune_id, RiskZone.layer_code == risk_code)
        .order_by(RiskZone.zone_index)
        .all()
    )
    features = []
    for zone in zones:
        merged = (
            db.query(func.ST_AsGeoJSON(func.ST_Union(GridCell.geometry)))
            .join(RiskZoneCell, RiskZoneCell.grid_cell_id == GridCell.id)
            .filter(RiskZoneCell.risk_zone_id == zone.id)
            .scalar()
        )
        if not merged:
            continue
        features.append({
            "type": "Feature", "geometry": json.loads(merged),
            "properties": {"zone_index": zone.zone_index, "cell_count": zone.cell_count,
                           "mean_risk": zone.mean_risk, "max_risk": zone.max_risk,
                           "area_m2": zone.area_m2, "risk_code": risk_code},
        })
    return {"type": "FeatureCollection", "features": features}


def _delete_old_zones(db: Session, kommune_id: int, risk_code: str):
    for z in (db.query(RiskZone)
              .filter(RiskZone.kommune_id == kommune_id, RiskZone.layer_code == risk_code).all()):
        db.delete(z)
    db.flush()
