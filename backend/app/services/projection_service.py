"""Projektion der KWRA-Gruppen-Risikoindizes (2025–2065).

Skaliert die heutigen Gruppen-Indizes mit dem regionalisierten DWD-Hitzetrend
(RCP4.5 / RCP8.5) als übergreifendem Klimasignal. Vereinfachte, dokumentierte
Näherung (siehe Handbuch).
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.services.measure_service import get_risk_aggregate
from app.services.climate.dwd_data import get_climate_projection


def scenario_factors(proj: dict, scenario: str, group: str | None = None) -> list[float]:
    """Relative Klimasignal-Faktoren je Jahr, auf das Startjahr normiert.

    Gefahrengruppen-spezifisch, weil ein einziger Hitzetage-Trend die anderen
    Gruppen falsch fortschreibt:

    * ``heat`` — Verhältnis der **Expositions-Wirkungs-Kurve** bei der projizierten
      gegenüber der heutigen Sommertemperatur. Die Kurve ist oberhalb der
      Wirkschwelle konvex; eine lineare Skalierung mit den Hitzetagen unterschätzt
      künftige Sterbefälle daher systematisch.
    * sonst — weiter der Hitzetage-Trend als übergreifendes Klimasignal, weil für
      Starkregen und Sturm keine belastbare regionalisierte Projektionsreihe
      vorliegt (dokumentierte Vereinfachung).
    """
    if group == "heat":
        temps = proj["scenarios"][scenario].get("mean_temp") or []
        if len(temps) >= 2:
            return _erf_factors(temps)

    series = proj["scenarios"][scenario]["hot_days"]
    base = series[0] if series else 1.0
    return [(v / base if base else 1.0) for v in series]


def _erf_factors(mean_temps: list[float]) -> list[float]:
    """Faktoren aus der Wirkungskurve statt aus einem linearen Hitzetage-Verhältnis.

    Die Jahresmittel-Reihe liefert nur das *Erwärmungsdelta*; darauf wird die
    bevölkerungsgewichtete Sommertemperatur Deutschlands (19,01 °C, aus dem
    DWD-Monatsraster bestimmt) verschoben und die Kurve neu ausgewertet.
    """
    from math import exp

    from app.data.germany_health_reference import BASELINE_MORTALITY_PER_100K as M
    from app.services.engine.impact import health as H

    # Bundesweite Altersstruktur (Zensus-Gitter) als Gewichtung.
    share_65p, split = 0.2186, {"a65_74": 0.5003, "a75_84": 0.3555, "a85p": 0.1442}
    bands = {b: share_65p * f for b, f in split.items()}
    bands["u65"] = 1.0 - share_65p
    thr, beta85 = H.REGION_THRESHOLD["mitte"], H.REGION_BETA_85P["mitte"]

    def deaths(summer_temp: float) -> float:
        temps = H.weekly_temperatures(summer_temp, "mitte")
        total = 0.0
        for band in H.AGE_BANDS:
            beta = beta85 * H.AGE_BETA_FACTOR[band]
            excess = sum(exp(beta * max(0.0, t - thr)) - 1.0 for t in temps)
            total += bands[band] * (M[band] / 100_000.0) * excess
        return total

    base_summer = 19.01
    base_deaths = deaths(base_summer)
    if base_deaths <= 0:
        return [1.0] * len(mean_temps)
    t0 = mean_temps[0]
    return [round(deaths(base_summer + (t - t0)) / base_deaths, 4) for t in mean_temps]


def project_group_risks(db: Session, kommune_id: int, bundesland: str) -> dict:
    agg = get_risk_aggregate(db, kommune_id, apply_measures=False)
    groups = agg["groups"]

    proj = get_climate_projection(bundesland)
    years = proj["years"]

    out_groups = []
    for code, g in groups.items():
        base_idx = g["index"]
        f45 = scenario_factors(proj, "rcp45", code)
        f85 = scenario_factors(proj, "rcp85", code)
        out_groups.append({
            "code": code, "label": g["label"], "color": g["color"],
            "base_index": base_idx,
            "rcp45": [round(min(100.0, base_idx * f), 1) for f in f45],
            "rcp85": [round(min(100.0, base_idx * f), 1) for f in f85],
        })

    return {"years": years, "groups": out_groups,
            "source": "DWD KlimaFolgenOnline; Hitze über die Expositions-Wirkungs-Kurve "
                      "(RKI/Winklmayr), übrige Gruppen über den Hitzetage-Trend"}
