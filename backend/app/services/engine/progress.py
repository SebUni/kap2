"""Gemeinsame Fortschrittsskala für Assessment-Läufe (0–100 %, strikt monoton)."""

from __future__ import annotations

# ── Phasengrenzen (nicht überlappend, aufsteigend) ──────────────────────────
ZENSUS = (0.0, 2.0)
OSM_LANDUSE = (2.0, 5.0)
OSM_BUILDINGS = (5.0, 8.0)
OSM_WATER = (8.0, 10.0)
TERRAIN_DEM = (10.0, 12.0)
TERRAIN_ELEV = (12.0, 22.0)
TERRAIN_HYDRO = (22.0, 28.0)
CELL_SURFACE = (28.0, 58.0)
CELL_NEIGHBORS = (58.0, 61.0)
ZENSUS_APPLY = (61.0, 62.0)
RISK_COMPOSE = (62.0, 95.0)
FINALIZE = (95.0, 98.0)


def lerp(lo: float, hi: float, fraction: float) -> float:
    """Interpolate within [lo, hi] for fraction in [0, 1]."""
    return lo + max(0.0, min(1.0, fraction)) * (hi - lo)


class MonotonicProgress:
    """Wraps a progress callback and guarantees non-decreasing percentages."""

    def __init__(self, callback):
        self._callback = callback
        self._pct = 0.0

    def __call__(self, pct: float, phase: str | None = None, detail: str | None = None):
        pct = max(self._pct, round(pct, 1))
        self._pct = pct
        self._callback(pct, phase, detail)
