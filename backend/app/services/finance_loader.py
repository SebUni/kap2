"""Kommunale Finanz-Kennzahlen für den Dashboard-Kopf (Regionalstatistik GENESIS).

Liefert je Kommune (AGS via ``inkar_loader.resolve_ags``):
  - **BIP** in jeweiligen Preisen — amtlich nur auf KREISebene verfügbar
    (``REGIONALSTATISTIK_TABLE_GDP``, Mio. €); letztes verfügbares Jahr.
  - **Kommunaler Haushalt** — Auszahlungen der Kern-/Extrahaushalte auf
    GEMEINDEebene (``REGIONALSTATISTIK_TABLE_BUDGET``, 1000 €); Ø der letzten
    ``REGIONALSTATISTIK_BUDGET_AVG_YEARS`` verfügbaren Jahre.

Abgrenzung zu ``inkar_loader._parse_ffcsv_value``: der dortige Parser ist
bewusst grob (erster Zahlenwert, LOSES Kreis-Präfix-Matching) und für
Jahres-SERIEN ungeeignet — eine Kreiszeile dürfte hier nie als Gemeindewert
durchgehen. :func:`parse_ffcsv_series` matcht deshalb Regionalschlüssel EXAKT
(inkl. 12-stelliger ARS über die Trailing-Zero-Regel) und ist jahressensitiv.

Robustheit wie beim Schwestermodul: ohne Zugangsdaten/AGS/Netz wird ``None``
geliefert, nie eine Exception — die Chips im Dashboard-Kopf sind optionaler
Zusatz. Disk-Cache je Kommune (``finance_osm_<id>.json``) inkl. aufgelöstem
AGS, damit Overpass nicht wiederholt befragt wird; leere Ergebnisse werden mit
KURZER TTL gecacht (Server-Hänger/Fehlkonfiguration friert die Anzeige sonst
30 Tage ein).
"""

from __future__ import annotations

import json
import logging
import os
import re
import threading
import time

from app.config import settings
from app.services import inkar_loader

log = logging.getLogger(__name__)

# Einheit der BIP-Tabelle 82000-* (Kennzahl BIP802): Tsd. € → Chip-Einheit Mio. €.
# (Der Kommunalhaushalt kommt in € aus dem Bulk-Store, s. finance_bulk.)
_GDP_UNIT_TO_MEUR = 0.001      # Tsd. € → Mio. €

# Leere Ergebnisse nur kurz cachen (Retry am Folgetag), volle Ergebnisse mit
# der langen Standard-TTL (jährliche Daten).
_EMPTY_TTL_S = 24 * 3600

# je osm-Relation: (ts, BIP-Payload|None, aufgelöster AGS|None)
_mem_cache: dict[str, tuple[float, dict | None, str | None]] = {}
_cache_lock = threading.Lock()

_YEAR_RE = re.compile(r"^(19|20)\d{2}$")


def _digits(cell: str) -> str:
    return re.sub(r"\D", "", cell)


def _region_matches(cell: str, target: str) -> bool:
    """Exaktes Regionalschlüssel-Matching (8-stelliger AGS bzw. 5-stelliger Kreis).

    12-stellige ARS gelten als Treffer, wenn sie der Schlüssel + nur Nullen sind
    (Kreis ``14730`` ≙ ARS ``147300000000``); ein Gemeinde-Suffix (z. B. ``…310``)
    macht die Zeile für den Kreis NICHT passend — und umgekehrt.
    """
    d = _digits(cell)
    if not d or not target:
        return False
    if d == target:
        return True
    return len(d) > len(target) and d.startswith(target) and set(d[len(target):]) == {"0"}


# Fehlwert-Marker der GENESIS-Flatfiles (siehe Doku ``readCsv``: na_values).
_MISSING = {"", "-", ".", "..", "...", "…", "x", "/"}


def _to_number(cell: str) -> float | None:
    """Deutsche Zahl → float; Fehlwert-Marker → ``None``.

    Anders als ``inkar_loader._to_float`` KEIN Jahres-Filter: hier ist die
    Wertspalte namentlich bekannt (``value``), ein Messwert wie ``2000`` darf
    nicht als „Jahr" verworfen werden. Tausenderpunkt/Dezimalkomma wie im
    ffcsv (``1.234,5`` → ``1234.5``)."""
    c = cell.strip().strip('"')
    if c in _MISSING:
        return None
    s = c.replace(".", "").replace(",", ".") if "," in c else c
    try:
        return float(s)
    except (ValueError, TypeError):
        return None


def parse_ffcsv_series(
    text: str, key: str, kreis_level: bool = False, value_variable: str | None = None
) -> dict[int, float]:
    """GENESIS-Flatfile-CSV (``data/tablefile``, ffcsv) → ``{Jahr: Wert}`` für
    genau einen Regionalschlüssel.

    Das reale ffcsv ist spaltenbenannt (englische Keys, unabhängig von der
    Sprache): ``time`` (Jahr), ``value`` (Messwert), ``value_variable_code``
    (Kennzahl-Code) und je Merkmal ``N_variable_attribute_code`` (u. a. der
    Regionalschlüssel). Es wird strikt über diese Spalten geparst — nicht mehr
    heuristisch über „letzte Zahl der Zeile": Tabellen wie ``82000-01-01-4``
    liefern pro Region/Jahr MEHRERE Wertzeilen (BIP gesamt / je Erwerbstätigem /
    pro Kopf), sodass ``value_variable`` die gewünschte Kennzahl auswählt.

    - ``kreis_level``: Schlüssel auf 5 Stellen kürzen (Kreis- statt Gemeindewert).
    - ``value_variable``: nur Zeilen mit diesem ``value_variable_code`` (z. B.
      ``"BIP802"``); ``None`` = keine Einschränkung (Tabelle mit einer Kennzahl).

    Region-Matching strikt (``_region_matches``): eine Kreiszeile geht nie als
    Gemeindewert durch und umgekehrt. Fehlt der erwartete Spaltenkopf
    (``time``/``value``), wird ``{}`` geliefert (nie eine Exception).
    """
    target = _digits(key)
    if kreis_level:
        target = target[:5]
    if not target:
        return {}

    lines = [ln for ln in text.splitlines() if ln.strip()]
    if len(lines) < 2:
        return {}

    header = [c.strip().strip('"') for c in lines[0].split(";")]
    col = {name: i for i, name in enumerate(header)}
    time_i = col.get("time")
    value_i = col.get("value")
    if time_i is None or value_i is None:
        return {}
    vvc_i = col.get("value_variable_code")
    attr_is = [i for name, i in col.items() if name.endswith("_variable_attribute_code")]

    series: dict[int, float] = {}
    for line in lines[1:]:
        cells = [c.strip().strip('"') for c in line.split(";")]
        if max(time_i, value_i) >= len(cells):
            continue
        if not any(a < len(cells) and _region_matches(cells[a], target) for a in attr_is):
            continue
        if value_variable and vvc_i is not None:
            if vvc_i >= len(cells) or cells[vvc_i] != value_variable:
                continue
        if not _YEAR_RE.match(cells[time_i]):
            continue
        val = _to_number(cells[value_i])
        if val is not None:
            series[int(cells[time_i])] = val

    return series


def average_last_n(series: dict[int, float], n: int) -> tuple[float, list[int]] | None:
    """Mittel der letzten ``n`` verfügbaren Jahre + die zugehörige Jahresliste."""
    if not series or n <= 0:
        return None
    years = sorted(series)[-n:]
    return sum(series[y] for y in years) / len(years), years


def _genesis_table_ffcsv(table_code: str, regionalkey: str) -> str | None:
    """Roher ffcsv-Text einer GENESIS-Tabelle für einen Regionalschlüssel.

    Dünner Delegat auf :func:`inkar_loader._genesis_download_ffcsv` — beide
    Module teilen so denselben verifizierten Transport (data/tablefile,
    Token-Header-Auth, ZIP-Entpackung)."""
    return inkar_loader._genesis_download_ffcsv(table_code, regionalkey)


def _cache_path(osm_digits: str) -> str:
    return os.path.join(settings.REGIONALSTATISTIK_CACHE_DIR, f"finance_osm_{osm_digits}.json")


def _read_cache(osm_digits: str) -> dict | None:
    try:
        path = _cache_path(osm_digits)
        if not os.path.exists(path):
            return None
        with open(path, encoding="utf-8") as fh:
            blob = json.load(fh)
        age = time.time() - os.path.getmtime(path)
        payload = blob.get("payload")
        ttl = settings.REGIONALSTATISTIK_CACHE_TTL_S if payload else _EMPTY_TTL_S
        if age > ttl:
            # Stale — aber den aufgelösten AGS weiterreichen (spart Overpass).
            return {"stale": True, "ags": blob.get("ags")}
        return {"stale": False, "ags": blob.get("ags"), "payload": payload}
    except Exception:
        return None


def _write_cache(osm_digits: str, ags: str | None, payload: dict | None) -> None:
    try:
        os.makedirs(settings.REGIONALSTATISTIK_CACHE_DIR, exist_ok=True)
        with open(_cache_path(osm_digits), "w", encoding="utf-8") as fh:
            json.dump({"ags": ags, "payload": payload}, fh)
    except Exception as exc:
        log.debug("finance disk-cache write skipped: %s", exc)


def fetch_finance(ags: str) -> dict | None:
    """BIP (Kreis, live via GENESIS) für einen AGS — ohne Cache-Schicht.

    Nur noch BIP: Der Kommunalhaushalt (Statistik 71717) ist für den Live-Dialog
    zu groß und kommt aus dem lokalen Bulk-Store (:mod:`app.services.finance_bulk`,
    per Betreiber-Cron befüllt) — hier NICHT abgefragt.
    """
    gdp_text = _genesis_table_ffcsv(settings.REGIONALSTATISTIK_TABLE_GDP, ags[:5])
    if not gdp_text:
        return None
    series = parse_ffcsv_series(
        gdp_text, ags, kreis_level=True,
        value_variable=settings.REGIONALSTATISTIK_GDP_VARIABLE or None)
    if not series:
        return None
    year = max(series)
    # BIP je Einwohner (Kreis, EUR) — Basis für die Kommunen-Schätzung im Profil.
    pc = parse_ffcsv_series(
        gdp_text, ags, kreis_level=True,
        value_variable=settings.REGIONALSTATISTIK_GDP_PC_VARIABLE or None)
    return {"gdp": {
        "gdp_meur": round(series[year] * _GDP_UNIT_TO_MEUR, 1),
        "gdp_per_capita_eur": pc.get(year),
        "gdp_year": year,
        "level": "kreis",
    }}


def _gdp_for_osm(osm_digits: str, osm_id: str) -> tuple[dict | None, str | None]:
    """Gecachtes BIP-Payload + aufgelöster AGS für eine OSM-Relation.

    AGS wird auch ohne GENESIS-Zugang aufgelöst (aus Disk-Cache bzw. Overpass),
    damit der netzfreie Budget-Lookup ihn nutzen kann; BIP nur mit Zugangsdaten.
    """
    have_auth = inkar_loader._auth_headers() is not None

    with _cache_lock:
        cached = _mem_cache.get(osm_digits)
        if cached and time.time() - cached[0] < _EMPTY_TTL_S:
            return cached[1], cached[2]

    disk = _read_cache(osm_digits)
    if disk is not None and not disk.get("stale"):
        payload = disk.get("payload") or None
        ags = disk.get("ags")
        with _cache_lock:
            _mem_cache[osm_digits] = (time.time(), payload, ags)
        return payload, ags

    ags = (disk or {}).get("ags") or inkar_loader.resolve_ags(osm_id)
    if not ags:
        if have_auth:
            _write_cache(osm_digits, None, None)
        return None, None

    payload = fetch_finance(ags) if have_auth else None
    _write_cache(osm_digits, ags, payload)
    with _cache_lock:
        _mem_cache[osm_digits] = (time.time(), payload, ags)
    return payload, ags


def finance_for_kommune(osm_id: str | None, name: str | None = None) -> dict | None:
    """Öffentlicher Einstieg: BIP (GENESIS, gecacht) + Kommunalhaushalt (lokaler
    Bulk-Store, via ``name``). Gibt bei jedem Fehlschlag ``None`` zurück und wirft
    nie (Dashboard-Kopf ist optionaler Zusatz)."""
    try:
        if not osm_id:
            return None
        m = re.search(r"\d+", str(osm_id))
        if not m:
            return None
        osm_digits = m.group(0)

        # Nichts zu holen (kein GENESIS-Zugang für BIP UND kein Budget-Lookup
        # möglich) → früh raus, ohne Netz (AGS-Auflösung wäre sinnlos).
        have_auth = inkar_loader._auth_headers() is not None
        budget_wanted = settings.REGIONALSTATISTIK_BUDGET_ENABLED and bool(name)
        if not have_auth and not budget_wanted:
            return None

        gdp_payload, ags = _gdp_for_osm(osm_digits, osm_id)
        payload = dict(gdp_payload) if gdp_payload else {}

        # Kommunalhaushalt: netzfrei aus dem Bulk-Store (immer frisch, nicht im
        # osm-Cache — der Store wird unabhängig per Cron aktualisiert).
        from app.services import finance_bulk
        budget = finance_bulk.budget_for_kommune(ags, name)
        if budget:
            payload["budget"] = budget

        return payload or None
    except Exception as exc:
        log.warning("finance_for_kommune fehlgeschlagen (osm_id=%s): %s", osm_id, exc)
        return None
