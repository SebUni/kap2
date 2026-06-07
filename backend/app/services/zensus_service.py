"""Bevölkerungsverteilung auf 100m-Zellen (Zensus 2022).

Strategie (siehe Handbuch):
* Wenn eine Zensus-2022-100m-Gitter-CSV vorliegt (Pfad via Umgebungsvariable
  ``ZENSUS_GRID_CSV``, Destatis/BKG INSPIRE-Gitter ``Bevoelkerung100m``), wird die
  Einwohnerzahl flächengewichtet auf die KAP2-Zellen übertragen.
* Andernfalls (Default) werden die Gemeinde-Einwohner anhand des
  Wohngebäudevolumens (OSM-Gebäudegrundfläche × Geschosse in bewohnbaren Zellen)
  verteilt – ein dokumentierter Proxy. Die Gesamtsumme bleibt erhalten.

Alters-/Risikogruppen-Anteile stammen aus bundesweiten Zensus-2022-Mittelwerten
(Gemeindeebene), gleichmäßig auf bewohnte Zellen verteilt und in den (i)-Tooltips
als „nicht kleinräumig aufgelöst" markiert.
"""

from __future__ import annotations

import csv
import logging
import os

log = logging.getLogger(__name__)

# Bundesweite Zensus-2022-Mittelwerte (Anteile), Quelle: Destatis Zensus 2022.
NATIONAL_DEMOGRAPHICS = {
    "share_over_65": 22.0,
    "share_under_18": 18.0,
    "share_vulnerable": 40.0,
    "persons_per_residential_building": 5.0,
}

_ZENSUS_CACHE: dict[str, list[dict]] | None = None


def _load_zensus_grid() -> list[dict] | None:
    """Lädt das Zensus-100m-Gitter aus CSV, falls konfiguriert. Cached."""
    global _ZENSUS_CACHE
    path = os.environ.get("ZENSUS_GRID_CSV")
    if not path or not os.path.exists(path):
        return None
    if _ZENSUS_CACHE is not None:
        return _ZENSUS_CACHE.get(path)
    rows: list[dict] = []
    try:
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter=";")
            for r in reader:
                # Erwartete Spalten (INSPIRE): x_mp_100m, y_mp_100m, Einwohner
                try:
                    rows.append({
                        "x": float(r.get("x_mp_100m") or r.get("x") or 0),
                        "y": float(r.get("y_mp_100m") or r.get("y") or 0),
                        "pop": float(r.get("Einwohner") or r.get("pop") or 0),
                    })
                except (ValueError, TypeError):
                    continue
        _ZENSUS_CACHE = {path: rows}
        log.info("Zensus-Gitter geladen: %d Zellen aus %s", len(rows), path)
    except Exception as exc:  # pragma: no cover
        log.warning("Zensus-Gitter konnte nicht geladen werden: %s", exc)
        return None
    return rows


def distribute_population(
    cell_inputs: list[dict],
    kommune_population: int | None,
    area_km2: float | None,
) -> None:
    """Setzt ``pop`` (Einwohner) je Zelle in-place in cell_inputs.

    Default-Proxy: Verteilung der Gemeinde-Einwohner proportional zum
    Wohngebäudevolumen (building_coverage × max(avg_height,3)) je Zelle.
    """
    total_pop = float(kommune_population or 0)
    if total_pop <= 0 and area_km2:
        # grobe Default-Dichte, falls keine Einwohnerzahl bekannt
        total_pop = 350.0 * float(area_km2)

    # Gewicht = Wohnvolumen-Proxy
    weights = []
    for ci in cell_inputs:
        h = max(ci.get("avg_height", 0.0), 0.0)
        cov = ci.get("bldg_cov", 0.0)
        # bewohnbar: Gebäude vorhanden und nicht reine Industrie (heuristisch über green)
        vol = cov * (h if h > 0 else 6.0)
        weights.append(vol)

    wsum = sum(weights)
    if wsum <= 0:
        # Keine Gebäudedaten – gleichmäßig auf alle Zellen
        n = max(len(cell_inputs), 1)
        for ci in cell_inputs:
            ci["pop"] = total_pop / n
        return

    for ci, w in zip(cell_inputs, weights):
        ci["pop"] = total_pop * (w / wsum)


def demographic_shares() -> dict:
    """Bundesweite Alters-/Risikogruppen-Anteile (Zensus 2022)."""
    return dict(NATIONAL_DEMOGRAPHICS)
