"""KAP2-Deutschlandstudie: Rankings, Bundesland-Vergleiche, Kernzahlen, CSV.

Aggregiert die vorberechneten ``gemeinde_lite_results`` zu Studien-Artefakten
(Plan §Phase H): ``studie.json`` (Rankings + Bundesland-Mittel + Kernzahlen),
``studie.csv`` (kompletter Datensatz, CC-BY „KAP2") und ``study_highlights.json``
(Headline-Fakten für die Landingpage).
"""
from __future__ import annotations

import csv
import json
import logging
import os
from collections import defaultdict

from sqlalchemy.orm import Session

from app.config import settings
from app.data import catalog
from app.models.lite_models import Gemeinde, GemeindeLiteResult
from app.services.lite.lite_scoring import LITE_RISK_CODES

log = logging.getLogger(__name__)


def _out(name: str) -> str:
    return os.path.join(settings.LITE_DATA_DIR, name)


def build_study(db: Session) -> dict:
    gem = {g.ags: g for g in db.query(Gemeinde).all()}
    results = db.query(GemeindeLiteResult).all()
    by_risk: dict[str, list[GemeindeLiteResult]] = defaultdict(list)
    for r in results:
        by_risk[r.risk_code].append(r)

    rankings = {}
    bl_means = {}
    for code in LITE_RISK_CODES:
        rows = by_risk.get(code, [])
        rows.sort(key=lambda r: r.index_value or 0, reverse=True)
        rankings[code] = [{
            "ags": r.ags, "name": gem[r.ags].name if r.ags in gem else r.ags,
            "bundesland": gem[r.ags].bundesland if r.ags in gem else None,
            "index": r.index_value, "outcome": r.outcome_value,
            "unit": r.outcome_unit, "cost_eur": r.cost_eur,
        } for r in rows[:20]]
        # Bundesland-Mittel
        acc: dict[str, list[float]] = defaultdict(list)
        for r in rows:
            bl = gem[r.ags].bundesland if r.ags in gem else None
            if bl:
                acc[bl].append(r.index_value or 0)
        bl_means[code] = {bl: round(sum(v) / len(v), 1) for bl, v in acc.items()}

    # Kernzahlen
    total_gem = len(gem)
    mort = by_risk.get("EXPECTED_ANNUAL_MORTALITY", [])
    high_heat = sum(1 for r in mort if (r.index_value or 0) > 70)
    building = by_risk.get("EXPECTED_BUILDING_DAMAGE_EUR", [])
    pop_starkregen = sum(gem[r.ags].population or 0 for r in building
                         if (r.index_value or 0) > 70 and r.ags in gem)
    agrar = by_risk.get("EXPECTED_AGRICULTURAL_DAMAGE_EUR", [])
    agrar.sort(key=lambda r: r.index_value or 0, reverse=True)
    top_agrar_bl = None
    if agrar and agrar[0].ags in gem:
        top_agrar_bl = gem[agrar[0].ags].bundesland

    facts = []
    if total_gem:
        facts.append(f"{round(100 * high_heat / total_gem)} % der Gemeinden weisen ein hohes "
                     f"Hitzemortalitätsrisiko auf (Index über 70).")
    if pop_starkregen:
        facts.append(f"Rund {pop_starkregen / 1_000_000:.1f} Mio. Menschen leben in Gemeinden "
                     f"mit hohem Gebäudeschadenrisiko durch Starkregen.")
    if top_agrar_bl:
        facts.append(f"Das höchste landwirtschaftliche Dürrerisiko liegt in {top_agrar_bl}.")

    stand = db.query(Gemeinde.vg250_stand).first()
    study = {
        "stand": stand[0] if stand else None,
        "gemeinde_count": total_gem,
        "risks": [{"code": c, "name": catalog.RISKS_BY_CODE[c]["name"],
                   "unit": catalog.RISKS_BY_CODE[c].get("outcome_unit", "")}
                  for c in LITE_RISK_CODES],
        "rankings": rankings,
        "bundesland_means": bl_means,
        "headline_facts": facts,
    }

    os.makedirs(settings.LITE_DATA_DIR, exist_ok=True)
    with open(_out("studie.json"), "w", encoding="utf-8") as fh:
        json.dump(study, fh, ensure_ascii=False)
    with open(_out("study_highlights.json"), "w", encoding="utf-8") as fh:
        json.dump({"headline_facts": facts, "stand": study["stand"],
                   "gemeinde_count": total_gem}, fh, ensure_ascii=False)
    _write_csv(db, gem, results)
    log.info("Studie: %d Gemeinden, %d Kernzahlen", total_gem, len(facts))
    return study


def _write_csv(db: Session, gem: dict, results: list) -> None:
    by_ags: dict[str, dict] = defaultdict(dict)
    for r in results:
        by_ags[r.ags][r.risk_code] = r.index_value
    path = _out("studie.csv")
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, delimiter=";")
        w.writerow(["ags", "gemeinde", "bundesland", "einwohner", "flaeche_km2"]
                   + [f"{c}_index" for c in LITE_RISK_CODES])
        for ags, g in sorted(gem.items()):
            row = [ags, g.name, g.bundesland, g.population, g.area_km2]
            row += [by_ags.get(ags, {}).get(c, "") for c in LITE_RISK_CODES]
            w.writerow(row)
