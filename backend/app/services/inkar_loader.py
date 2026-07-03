"""Kommunale Sozioökonomie (BBSR INKAR / Regionalstatistik GENESIS) je AGS.

Leitet ortsaufgelöste, editierbare Verwundbarkeitsindizes für
``FINANCIAL_ADAPTATION_CAPACITY`` und ``PLANNING_IMPLEMENTATION_CAPACITY`` ab
(0..100, invers: geringe Finanz-/Planungskraft ⇒ hoher Verwundbarkeitswert).

Rohgrößen (Regionalstatistik GENESIS-Online REST, je Gemeinde-/Kreis-AGS):
  - Steuereinnahmekraft der Gemeinden (Realsteuervergleich), €/Einwohner
  - Arbeitslosenquote, %

Der AGS der Kommune wird aus der OSM-Grenz-Relation (``Kommune.osm_id``) über
Overpass aufgelöst (Tag ``de:amtlicher_gemeindeschluessel`` bzw.
``de:regionalschluessel``).

Robuster Fallback: fehlt der AGS, die Zugangsdaten oder das Netz, gibt
:func:`socioeconomic_for_kommune` ein leeres Dict zurück; die Indikatoren
fallen dann auf den neutralen, editierbaren Wert 50 zurück
("Modellannahme (mangels lokaler Daten)"). Es wird nie eine Exception nach oben
gereicht — Sozioökonomie ist optionaler Zusatz, kein harter Berechnungsschritt.
"""

from __future__ import annotations

import json
import logging
import os
import re
import threading
import time
from typing import Any

import httpx

from app.config import settings

log = logging.getLogger(__name__)

# ── Normierungsanker (nationale Spannen, Report §3-Logik: Index aus Spatialdaten) ──
# Steuereinnahmekraft €/Einwohner: ~500 (schwach) … ~1500 (stark).
TAX_LO_EUR = 500.0
TAX_HI_EUR = 1500.0
# Arbeitslosenquote %: ~2 (niedrig) … ~12 (hoch).
UNEMPLOYMENT_LO_PCT = 2.0
UNEMPLOYMENT_HI_PCT = 12.0

_mem_cache: dict[str, tuple[float, dict | None]] = {}
_cache_lock = threading.Lock()


def _clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


def _inverse_index(value: float, lo: float, hi: float) -> float:
    """Kapazitätsgröße → Verwundbarkeitsindex (hoher Rohwert = geringe Verwundbarkeit)."""
    if hi <= lo:
        return 50.0
    frac = (float(value) - lo) / (hi - lo)
    return round(_clamp(100.0 * (1.0 - frac), 0.0, 100.0), 1)


def _direct_index(value: float, lo: float, hi: float) -> float:
    """Belastungsgröße → Verwundbarkeitsindex (hoher Rohwert = hohe Verwundbarkeit)."""
    if hi <= lo:
        return 50.0
    frac = (float(value) - lo) / (hi - lo)
    return round(_clamp(100.0 * frac, 0.0, 100.0), 1)


def socioeconomic_indices(raw: dict) -> dict:
    """Rohgrößen → {financial_adaptation, planning_capacity} (0..100, invers).

    Reine Funktion (ohne Netz) — Kern der Ableitung, unit-testbar.
    """
    tax = raw.get("tax_capacity_eur_per_capita")
    unemp = raw.get("unemployment_rate_pct")

    fin_parts: list[float] = []
    plan_parts: list[float] = []
    if tax is not None:
        tax_idx = _inverse_index(tax, TAX_LO_EUR, TAX_HI_EUR)
        fin_parts.append(tax_idx)
        plan_parts.append(tax_idx)  # Planungskapazität v.a. an Finanzkraft der Kommune
    if unemp is not None:
        fin_parts.append(_direct_index(unemp, UNEMPLOYMENT_LO_PCT, UNEMPLOYMENT_HI_PCT))

    out: dict[str, float] = {}
    if fin_parts:
        out["financial_adaptation"] = round(sum(fin_parts) / len(fin_parts), 1)
    if plan_parts:
        out["planning_capacity"] = round(sum(plan_parts) / len(plan_parts), 1)
    return out


# ── AGS-Auflösung aus der OSM-Grenz-Relation ──────────────────────────────────

_AGS_TAG_KEYS = ("de:amtlicher_gemeindeschluessel", "de:regionalschluessel")


def resolve_ags(osm_id: str | None) -> str | None:
    """Amtlichen Gemeindeschlüssel (bis 8-stellig) aus der OSM-Relation lesen."""
    if not osm_id:
        return None
    m = re.search(r"\d+", str(osm_id))
    if not m:
        return None
    rid = m.group(0)
    query = f"[out:json][timeout:60];relation({rid});out tags;"
    try:
        with httpx.Client(timeout=settings.REGIONALSTATISTIK_TIMEOUT_S) as client:
            resp = client.post(
                settings.OVERPASS_URL,
                data={"data": query},
                headers={"User-Agent": settings.NOMINATIM_USER_AGENT},
            )
            resp.raise_for_status()
            elements = resp.json().get("elements", [])
    except Exception as exc:  # Netz/Timeout/Parsing → kein AGS
        log.warning("resolve_ags: Overpass-Abfrage für osm_id=%s fehlgeschlagen: %s", osm_id, exc)
        return None

    for el in elements:
        tags = el.get("tags", {})
        for key in _AGS_TAG_KEYS:
            val = tags.get(key)
            if val:
                digits = re.sub(r"\D", "", val)
                if digits:
                    return digits[:8]
    log.info("resolve_ags: kein AGS-Tag in OSM-Relation %s", rid)
    return None


# ── GENESIS-Abfrage (Regionalstatistik) mit Disk-/Memory-Cache ────────────────

def _cache_path(ags: str) -> str:
    return os.path.join(settings.REGIONALSTATISTIK_CACHE_DIR, f"socio_{ags}.json")


def _read_disk_cache(ags: str) -> dict | None:
    path = _cache_path(ags)
    try:
        if not os.path.exists(path):
            return None
        if time.time() - os.path.getmtime(path) > settings.REGIONALSTATISTIK_CACHE_TTL_S:
            return None
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return None


def _write_disk_cache(ags: str, data: dict) -> None:
    try:
        os.makedirs(settings.REGIONALSTATISTIK_CACHE_DIR, exist_ok=True)
        with open(_cache_path(ags), "w", encoding="utf-8") as fh:
            json.dump(data, fh)
    except Exception as exc:
        log.debug("inkar disk-cache write skipped: %s", exc)


def _genesis_table_value(table_code: str, ags: str) -> float | None:
    """Zahlenwert für einen AGS aus einer GENESIS-Tabelle (ffcsv), best-effort.

    GENESIS liefert bei ``format=ffcsv`` eine ``;``-separierte Flat-Datei. Wir
    suchen die Zeile, deren Regionalschlüssel den (Präfix-)AGS enthält, und
    nehmen den ersten numerischen Messwert. Bei jeglichem Problem → ``None``.
    """
    if not (settings.REGIONALSTATISTIK_USERNAME and settings.REGIONALSTATISTIK_PASSWORD):
        return None
    url = f"{settings.REGIONALSTATISTIK_API_BASE.rstrip('/')}/data/table"
    params = {
        "username": settings.REGIONALSTATISTIK_USERNAME,
        "password": settings.REGIONALSTATISTIK_PASSWORD,
        "name": table_code,
        "area": "all",
        "format": "ffcsv",
        "language": "de",
        "compress": "false",
    }
    try:
        with httpx.Client(timeout=settings.REGIONALSTATISTIK_TIMEOUT_S) as client:
            resp = client.get(url, params=params)
            resp.raise_for_status()
            text = resp.text
    except Exception as exc:
        log.warning("GENESIS-Abfrage %s fehlgeschlagen: %s", table_code, exc)
        return None

    return _parse_ffcsv_value(text, ags)


def _parse_ffcsv_value(text: str, ags: str) -> float | None:
    """Erste numerische Zelle der Zeile, deren Regionalschlüssel zu ``ags`` passt."""
    ags = re.sub(r"\D", "", ags)
    kreis = ags[:5]
    best: float | None = None
    for line in text.splitlines():
        cells = [c.strip().strip('"') for c in line.split(";")]
        # Regionalschlüssel steht i.d.R. in einer der ersten Spalten.
        row_keys = [re.sub(r"\D", "", c) for c in cells[:4] if re.sub(r"\D", "", c)]
        if not any(k == ags or (len(k) >= 5 and k[:5] == kreis) for k in row_keys):
            continue
        for c in cells:
            num = _to_float(c)
            if num is not None:
                best = num
                break
        if best is not None:
            break
    return best


def _to_float(cell: str) -> float | None:
    s = cell.replace(".", "").replace(",", ".") if "," in cell else cell
    try:
        val = float(s)
    except (ValueError, TypeError):
        return None
    # reine Jahres-/Schlüsselzahlen aussortieren
    if val.is_integer() and (1900 <= val <= 2100):
        return None
    return val


def fetch_socioeconomic(ags: str) -> dict | None:
    """Rohgrößen {tax_capacity_eur_per_capita, unemployment_rate_pct} für einen AGS.

    Disk- und Memory-Cache (TTL). ``None``, wenn keine Werte verfügbar.
    """
    if not ags:
        return None
    with _cache_lock:
        cached = _mem_cache.get(ags)
        if cached and time.time() - cached[0] < settings.REGIONALSTATISTIK_CACHE_TTL_S:
            return cached[1]

    disk = _read_disk_cache(ags)
    if disk is not None:
        with _cache_lock:
            _mem_cache[ags] = (time.time(), disk or None)
        return disk or None

    raw: dict[str, float] = {}
    tax = _genesis_table_value(settings.REGIONALSTATISTIK_TABLE_TAX, ags)
    if tax is not None:
        raw["tax_capacity_eur_per_capita"] = tax
    unemp = _genesis_table_value(settings.REGIONALSTATISTIK_TABLE_UNEMPLOYMENT, ags)
    if unemp is not None:
        raw["unemployment_rate_pct"] = unemp

    result = raw or None
    _write_disk_cache(ags, raw)  # auch leeres Ergebnis cachen (kein Re-Fetch-Sturm)
    with _cache_lock:
        _mem_cache[ags] = (time.time(), result)
    return result


def socioeconomic_for_kommune(osm_id: str | None, bundesland: str | None = None) -> dict:
    """Öffentlicher Einstieg: AGS auflösen → INKAR abrufen → Indizes ableiten.

    Gibt bei jedem Fehlschlag ``{}`` zurück (neutraler Fallback in indicators.py).
    """
    try:
        ags = resolve_ags(osm_id)
        if not ags:
            return {}
        raw = fetch_socioeconomic(ags)
        if not raw:
            return {}
        indices = socioeconomic_indices(raw)
        if indices:
            indices["ags"] = ags
        return indices
    except Exception as exc:  # niemals den Assessment-Lauf abbrechen
        log.warning("socioeconomic_for_kommune fehlgeschlagen (osm_id=%s): %s", osm_id, exc)
        return {}
