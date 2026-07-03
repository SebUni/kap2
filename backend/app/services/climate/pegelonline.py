"""BfG / PEGELONLINE (WSV): Niedrigwasser am nächsten Pegel — Treiber ``low_flow_days``.

Report §B2.6: statt des Proxys ``10 + hot_days`` wird der Treiber
``low_flow_days`` (Niedrigwassertage/Jahr) aus dem **nächstgelegenen WSV-Pegel**
abgeleitet (offene REST-API, ohne Schlüssel).

Definition (dokumentierte Näherung wegen API-Grenzen): PEGELONLINE hält nur ein
Rohdatenfenster von ~30 Tagen (15-min-Wasserstände) online vor und liefert je
Pegel den ``MNW`` (Mittel der Niedrigwasserstände, 10-jährige Kennzahl) als
stabilen, stationsspezifischen Schwellwert. ``low_flow_days`` = Anteil der Tage im
verfügbaren Fenster, an denen der Tages-Mindestwasserstand unter dem MNW liegt,
hochgerechnet auf ein Jahr. Das ist ein echtes, ortsbezogenes hydrologisches
Signal (nächster Pegel + dessen Niedrigwasser-Kennzahl) — kein deterministischer
Hitze-Proxy mehr.

Robuster Fallback: fehlt Netz/Pegel/MNW, gibt es zu wenig Messdaten, oder ist der
nächste Pegel weiter als :data:`settings.PEGELONLINE_MAX_DISTANCE_KM` entfernt,
liefert :func:`low_flow_days_at` ``None`` → der Aufrufer nutzt den bisherigen
Proxy. Es wird nie eine Exception nach oben gereicht.
"""

from __future__ import annotations

import json
import logging
import math
import os
import threading
import time

import httpx

from app.config import settings

log = logging.getLogger(__name__)

_MIN_DAYS = 14  # Mindest-Tage im Fenster für eine stabile Schätzung

_mem: dict[str, tuple[float, object]] = {}
_cache_lock = threading.Lock()


def _mem_get(key: str):
    with _cache_lock:
        v = _mem.get(key)
        if v and time.time() - v[0] < settings.PEGELONLINE_CACHE_TTL_S:
            return v[1]
    return None


def _mem_put(key: str, val) -> None:
    with _cache_lock:
        _mem[key] = (time.time(), val)


def _base() -> str:
    return settings.PEGELONLINE_API_BASE.rstrip("/")


# ── Stationsliste (Disk-Cache, groß & stabil) ─────────────────────────────────

def _stations() -> list[dict]:
    cached = _mem_get("stations")
    if cached is not None:
        return cached  # type: ignore[return-value]

    path = os.path.join(settings.PEGELONLINE_CACHE_DIR, "stations.json")
    data: list[dict] | None = None
    try:
        if (
            os.path.exists(path)
            and time.time() - os.path.getmtime(path) < settings.PEGELONLINE_CACHE_TTL_S
        ):
            with open(path, encoding="utf-8") as fh:
                data = json.load(fh)
    except Exception:
        data = None

    if data is None:
        try:
            with httpx.Client(timeout=settings.PEGELONLINE_TIMEOUT_S) as client:
                resp = client.get(f"{_base()}/stations.json")
                resp.raise_for_status()
                data = resp.json()
            os.makedirs(settings.PEGELONLINE_CACHE_DIR, exist_ok=True)
            with open(path, "w", encoding="utf-8") as fh:
                json.dump(data, fh)
        except Exception as exc:
            log.warning("PEGELONLINE Stations-Abruf fehlgeschlagen: %s", exc)
            data = []

    stations = [
        s for s in (data or [])
        if s.get("latitude") is not None and s.get("longitude") is not None
    ]
    _mem_put("stations", stations)
    return stations


def _haversine_km(lon1: float, lat1: float, lon2: float, lat2: float) -> float:
    r = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlmb = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlmb / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def nearest_station(lon: float, lat: float) -> tuple[dict | None, float | None]:
    """Nächstgelegener Pegel (mit Koordinaten) und Distanz in km."""
    best, best_d = None, None
    for s in _stations():
        try:
            d = _haversine_km(lon, lat, float(s["longitude"]), float(s["latitude"]))
        except (TypeError, ValueError):
            continue
        if best_d is None or d < best_d:
            best, best_d = s, d
    return best, best_d


# ── Niedrigwasser-Ableitung am Pegel ──────────────────────────────────────────

def _station_mnw(uuid: str) -> float | None:
    """MNW (Mittel der Niedrigwasserstände, cm) des Pegels aus den Kennzahlen."""
    url = f"{_base()}/stations/{uuid}/W.json?includeCharacteristicValues=true"
    try:
        with httpx.Client(timeout=settings.PEGELONLINE_TIMEOUT_S) as client:
            resp = client.get(url)
            resp.raise_for_status()
            meta = resp.json()
    except Exception as exc:
        log.warning("PEGELONLINE W-Kennzahlen %s fehlgeschlagen: %s", uuid, exc)
        return None
    for cv in meta.get("characteristicValues") or []:
        if cv.get("shortname") == "MNW" and cv.get("value") is not None:
            try:
                return float(cv["value"])
            except (TypeError, ValueError):
                return None
    return None


def _recent_low_flow_days(uuid: str, mnw: float) -> float | None:
    """Tages-Minima im ~30-Tage-Fenster unter MNW zählen und auf ein Jahr skalieren."""
    url = f"{_base()}/stations/{uuid}/W/measurements.json?start=P30D"
    try:
        with httpx.Client(timeout=settings.PEGELONLINE_TIMEOUT_S) as client:
            resp = client.get(url)
            resp.raise_for_status()
            points = resp.json()
    except Exception as exc:
        log.warning("PEGELONLINE Messreihe %s fehlgeschlagen: %s", uuid, exc)
        return None

    day_min: dict[str, float] = {}
    for p in points or []:
        ts, val = p.get("timestamp"), p.get("value")
        if not ts or val is None:
            continue
        day = ts[:10]
        try:
            fval = float(val)
        except (TypeError, ValueError):
            continue
        day_min[day] = min(day_min.get(day, float("inf")), fval)

    if len(day_min) < _MIN_DAYS:
        return None
    frac = sum(1 for v in day_min.values() if v < mnw) / len(day_min)
    # Liegen die Tages-Minima fast durchgängig unter dem MNW, ist der Pegel
    # geregelt/tidebeeinflusst oder das Pegelnull verschoben — der MNW-Bezug ist
    # dann nicht belastbar (unplausibel als „Niedrigwasser"). → Proxy nutzen.
    if frac > 0.5:
        return None
    # Auf ein Jahr hochrechnen, auf einen plausiblen Jahres-Maximalwert deckeln.
    return round(min(frac * 365.0, 90.0), 1)


def low_flow_days_at(lon: float, lat: float) -> float | None:
    """Niedrigwassertage/Jahr am nächsten Pegel. ``None`` → Aufrufer nutzt Proxy."""
    lon_r, lat_r = round(lon, 3), round(lat, 3)
    ckey = f"lfd:{lon_r}:{lat_r}"
    cached = _mem_get(ckey)
    if cached is not None:
        return cached  # type: ignore[return-value]

    vpath = os.path.join(settings.PEGELONLINE_CACHE_DIR, f"lfd_{lon_r}_{lat_r}.json")
    try:
        if (
            os.path.exists(vpath)
            and time.time() - os.path.getmtime(vpath) < settings.PEGELONLINE_CACHE_TTL_S
        ):
            with open(vpath, encoding="utf-8") as fh:
                val = json.load(fh).get("value")
            _mem_put(ckey, val)
            return val
    except Exception:
        pass

    result: float | None = None
    try:
        station, dist = nearest_station(lon, lat)
        if station and dist is not None and dist <= settings.PEGELONLINE_MAX_DISTANCE_KM:
            mnw = _station_mnw(station["uuid"])
            if mnw is not None:
                result = _recent_low_flow_days(station["uuid"], mnw)
                if result is not None:
                    log.info(
                        "PEGELONLINE low_flow_days=%.1f via Pegel %s (%.0f km, MNW=%.0f cm)",
                        result, station.get("longname"), dist, mnw,
                    )
    except Exception as exc:
        log.warning("PEGELONLINE low_flow_days_at fehlgeschlagen: %s", exc)
        result = None

    try:
        os.makedirs(settings.PEGELONLINE_CACHE_DIR, exist_ok=True)
        with open(vpath, "w", encoding="utf-8") as fh:
            json.dump({"value": result}, fh)
    except Exception as exc:
        log.debug("PEGELONLINE Wert-Cache-Write übersprungen: %s", exc)
    _mem_put(ckey, result)
    return result
