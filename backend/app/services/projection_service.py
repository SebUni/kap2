"""Projektion der KWRA-Gruppen-Risikoindizes (2025–2065).

Skaliert die heutigen Gruppen-Indizes mit dem regionalisierten DWD-Hitzetrend
(RCP4.5 / RCP8.5) als übergreifendem Klimasignal. Vereinfachte, dokumentierte
Näherung (siehe Handbuch).
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.services.measure_service import get_risk_aggregate
from app.services.climate.dwd_data import get_climate_projection


def project_group_risks(db: Session, kommune_id: int, bundesland: str) -> dict:
    agg = get_risk_aggregate(db, kommune_id, apply_measures=False)
    groups = agg["groups"]

    proj = get_climate_projection(bundesland)
    years = proj["years"]

    def factors(scenario: str) -> list[float]:
        series = proj["scenarios"][scenario]["hot_days"]
        base = series[0] if series else 1.0
        return [(v / base if base else 1.0) for v in series]

    f45 = factors("rcp45")
    f85 = factors("rcp85")

    out_groups = []
    for code, g in groups.items():
        base_idx = g["index"]
        out_groups.append({
            "code": code, "label": g["label"], "color": g["color"],
            "base_index": base_idx,
            "rcp45": [round(min(100.0, base_idx * f), 1) for f in f45],
            "rcp85": [round(min(100.0, base_idx * f), 1) for f in f85],
        })

    return {"years": years, "groups": out_groups,
            "source": "DWD KlimaFolgenOnline (Hitzetrend) als Skalierung der Gruppenindizes"}
