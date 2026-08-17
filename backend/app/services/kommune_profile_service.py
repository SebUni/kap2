"""Kommunen-Profil: Basisdaten + Klimakennzahlen mit Deutschland-Vergleich.

Liefert den Datenkopf des Dashboards: Lage, Fläche, Einwohner, Höhenlage sowie
je Klimametrik den Kommune-Wert (bevorzugt DWD-CDC-Raster am Zentroid, sonst
Bundesland-Gebietsmittel) neben dem belegten Deutschland-Referenzwert
(``app.data.germany_climate_reference``) samt Delta.

Die Bezugsperioden unterscheiden sich systematisch (CDC-Klimatologie = Mittel
der letzten verfügbaren Jahre, DE-Referenz i. d. R. 1991–2020) — deshalb wird
``period`` je Referenz mitgeliefert und im Frontend ausgewiesen, statt die
Differenz zu verschweigen.
"""

from __future__ import annotations

import logging
from typing import Optional

from geoalchemy2.shape import to_shape
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.config import settings
from app.data import sources
from app.data.germany_climate_reference import GERMANY_CLIMATE_REFERENCE
from app.models.models import CellAssessment, Kommune
from app.services.climate import dwd_cdc_grid, dwd_data

log = logging.getLogger(__name__)


def centroid_of(kommune: Kommune) -> Optional[tuple[float, float]]:
    """Zentroid der Gemeindegrenze als (lon, lat), ``None`` ohne Grenze."""
    if kommune.boundary is None:
        return None
    try:
        c = to_shape(kommune.boundary).centroid
        return (float(c.x), float(c.y))
    except Exception as exc:
        log.warning("Zentroid-Berechnung fehlgeschlagen (kommune=%s): %s", kommune.id, exc)
        return None


def ensure_population(db: Session, kommune: Kommune) -> Optional[int]:
    """Bevölkerung sicherstellen: Lazy-Backfill als SQL-Summe der Zell-Zensuswerte."""
    if kommune.population:
        return kommune.population
    try:
        pop = (
            db.query(func.sum(CellAssessment.data["inputs"]["pop"].as_float()))
            .filter(CellAssessment.kommune_id == kommune.id)
            .scalar()
        )
    except Exception as exc:
        log.warning("Populations-Backfill fehlgeschlagen (kommune=%s): %s", kommune.id, exc)
        return None
    if pop and pop > 0:
        kommune.population = int(round(pop))
        db.commit()
    return kommune.population


def _elevation_stats(db: Session, kommune_id: int) -> Optional[dict]:
    """Höhenlage als Aggregat über die Zell-Höhen (``auxiliary.MEAN_ELEVATION``)."""
    elev = CellAssessment.data["auxiliary"]["MEAN_ELEVATION"].as_float()
    try:
        row = (
            db.query(func.avg(elev), func.min(elev), func.max(elev))
            .filter(CellAssessment.kommune_id == kommune_id)
            .first()
        )
    except Exception as exc:
        log.warning("Höhen-Aggregat fehlgeschlagen (kommune=%s): %s", kommune_id, exc)
        return None
    if not row or row[0] is None:
        return None
    return {
        "mean_m": round(float(row[0]), 1),
        "min_m": round(float(row[1]), 1),
        "max_m": round(float(row[2]), 1),
        "source": "Digitales Höhenmodell (Terrarium-DEM), Mittel über 100-m-Zellen",
    }


def _metric(code: str, value: Optional[float], basis: str) -> dict:
    """Eine Klimametrik-Zeile mit DE-Referenz, Delta und Quellen aufbauen."""
    ref = GERMANY_CLIMATE_REFERENCE.get(code, {})
    de_val = ref.get("value")
    delta = delta_pct = None
    if value is not None and de_val is not None:
        delta = round(value - de_val, 1)
        if de_val:
            delta_pct = round(delta / de_val * 100.0, 1)
    return {
        "code": code,
        "label": ref.get("label") or code,
        "unit": ref.get("unit") or "",
        "value": round(value, 1) if value is not None else None,
        "data_basis": basis if value is not None else "unavailable",
        "germany": (
            {"value": de_val, "period": ref.get("period")} if de_val is not None else None
        ),
        "delta": delta,
        "delta_pct": delta_pct,
        "references": sources.resolve(ref.get("source_refs")),
    }


def _climate_metrics(bundesland: Optional[str], centroid: Optional[tuple[float, float]]) -> list[dict]:
    regional: dict = {}
    if bundesland:
        try:
            regional = dwd_data.get_regional_climate(bundesland) or {}
        except Exception as exc:
            log.warning("Regionalklima-Fallback fehlgeschlagen (%s): %s", bundesland, exc)

    lon, lat = centroid if centroid else (None, None)

    def cdc(fn) -> Optional[float]:
        if lon is None or lat is None:
            return None
        try:
            return fn(lon, lat)
        except Exception as exc:
            log.warning("DWD-CDC-Sampling fehlgeschlagen (%s): %s", fn.__name__, exc)
            return None

    def raster_or_regional(fn, regional_key: str) -> tuple[Optional[float], str]:
        v = cdc(fn)
        if v is not None:
            return v, "dwd_cdc_raster"
        return regional.get(regional_key), "regional_fallback"

    hot, hot_basis = raster_or_regional(dwd_cdc_grid.hot_days_at, "hot_days_per_year")
    summer, summer_basis = raster_or_regional(dwd_cdc_grid.summer_days_at, "summer_days_per_year")
    frost = cdc(dwd_cdc_grid.frost_days_at)
    precip_mm = cdc(dwd_cdc_grid.precipitation_at)
    precip20 = cdc(dwd_cdc_grid.precip_days_ge20_at)

    return [
        _metric("mean_temp_annual", regional.get("mean_temp_annual"), "regional_fallback"),
        _metric("precipitation_mm", precip_mm, "dwd_cdc_raster"),
        _metric("hot_days", hot, hot_basis),
        _metric("summer_days", summer, summer_basis),
        _metric("frost_days", frost, "dwd_cdc_raster"),
        _metric("tropical_nights", regional.get("tropical_nights_per_year"), "regional_fallback"),
        _metric("snow_days", regional.get("snow_days_per_year"), "regional_fallback"),
        _metric("precip_ge20_days", precip20, "dwd_cdc_raster"),
    ]


def _finance_sections(
    finance: dict | None, population: int | None = None
) -> tuple[dict | None, dict | None]:
    """finance_loader-Payload → Profil-Blöcke ``economy``/``municipal_budget``.

    BIP liegt amtlich nur auf Kreisebene vor; für den Kopf wird es zusätzlich auf
    die Kommune GESCHÄTZT (BIP je Einwohner des Kreises × Einwohner der Kommune) —
    ``estimated_municipal_eur``. Der amtliche Kreiswert (``gdp_meur``) bleibt für
    den Tooltip erhalten. Der kommunale Haushalt (Auszahlungen) liegt echt auf
    Gemeindeebene vor (Ø der letzten Jahre).
    """
    refs = sources.resolve(["Regionalstatistik_GENESIS"])
    economy = None
    budget = None
    gdp = (finance or {}).get("gdp")
    if gdp and gdp.get("gdp_meur") is not None:
        pc = gdp.get("gdp_per_capita_eur")
        estimated = round(pc * population) if (pc and population) else None
        economy = {
            "gdp_meur": gdp["gdp_meur"],
            "gdp_per_capita_eur": pc,
            "estimated_municipal_eur": estimated,
            "gdp_year": gdp.get("gdp_year"),
            "level": "kreis",
            "source": ("Regionalstatistik (GENESIS), Tabelle "
                       f"{settings.REGIONALSTATISTIK_TABLE_GDP} — BIP in jeweiligen "
                       "Preisen, Kreisebene"),
            "references": refs,
        }
    b = (finance or {}).get("budget")
    if b and b.get("avg_expenditure_eur") is not None:
        budget = {
            "avg_expenditure_eur": b["avg_expenditure_eur"],
            "years": b.get("years") or [],
            "level": "gemeinde",
            "source": ("Regionalstatistik (GENESIS), Tabelle "
                       f"{settings.REGIONALSTATISTIK_TABLE_BUDGET} — Auszahlungen "
                       "insgesamt (bereinigt) der kommunalen Kernhaushalte, "
                       "Gemeinde-/Berichtsebene"),
            "references": refs,
        }
    return economy, budget


def build_profile(db: Session, kommune: Kommune, finance: dict | None = None) -> dict:
    centroid = centroid_of(kommune)
    lon, lat = centroid if centroid else (None, None)
    population = ensure_population(db, kommune)
    economy, municipal_budget = _finance_sections(finance, population)
    return {
        "id": kommune.id,
        "name": kommune.name,
        "bundesland": kommune.bundesland,
        "landkreis": kommune.landkreis,
        "economy": economy,
        "municipal_budget": municipal_budget,
        "lat": round(lat, 4) if lat is not None else None,
        "lon": round(lon, 4) if lon is not None else None,
        "area_km2": kommune.area_km2,
        "population": population,
        "population_source": (
            "Zensus 2022 (Summe der 100-m-Gitterzellen)" if population else None
        ),
        "elevation": _elevation_stats(db, kommune.id),
        "climate": _climate_metrics(kommune.bundesland, centroid),
        "sources_note": (
            "Kommune-Werte: DWD-CDC-Jahresraster am Gemeindezentroid (Mittel der "
            "letzten verfügbaren Jahre); wo kein Raster vorliegt, DWD-Gebietsmittel "
            "des Bundeslands. DE-Referenz: DWD vieljährige Mittel (Periode je Wert "
            "angegeben)."
        ),
    }
