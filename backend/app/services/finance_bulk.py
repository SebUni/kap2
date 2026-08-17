"""Bulk-Import der kommunalen Auszahlungen (Regionalstatistik 71717) für den
Dashboard-Kopf-Chip „Kommunaler Haushalt".

**Warum Bulk statt Live:** Statistik 71717 ist für den GENESIS-Direkt-Dialog zu
groß (Fehler-Code 98) und nur über den Job/Batch-Pfad abrufbar, der die KOMPLETTE
Bundestabelle (~8–160 MB) liefert und Minuten braucht — mit dem On-Demand-Dashboard
unvereinbar. Dieser Importer zieht die Tabelle daher periodisch (Betreiber-Cron,
:mod:`scripts.import_finance_budget`), extrahiert je Berichtsgemeinde die
Kennzahl ``AUSZ001`` („Auszahlungen insgesamt, bereinigt", EUR) und legt einen
kompakten Lookup lokal ab (``budget_71717.json.gz``). Der Chip liest nur noch
diesen Cache (schnell, netzfrei).

**Schlüssel = Kreis + Name, nicht AGS:** Der GENESIS-Regionalcode ist NICHT der
amtliche Gemeindeschlüssel — er kodiert den GemeindeVERBAND (Oschatz amtlich
``14730230``, GENESIS-Code ``F1473002300`` = Kreis ``14730`` + Verbandsschlüssel
``0230``). Ein arithmetisches AGS-Mapping gibt es daher nicht. Zuverlässig ist
dagegen ``kreis5`` (die ersten 5 Ziffern = Kreis, stimmt mit dem AGS überein) plus
der normalisierte Gemeindename. Ebene ``FGEMEIN`` (Berichtseinheiten:
Einheitsgemeinden, Ämter, Verwaltungsgemeinschaften) ist die saubere Quelle;
amtsangehörige Einzelgemeinden berichten unter ihrer Berichtseinheit und haben
darum ggf. keinen eigenen Chip (optionaler Zusatz).

**Selbstheilung:** Der neue Stand wird erst temporär geschrieben und validiert
(Plausibilitätsschwellen + Anker-Kommunen); nur wenn er gültig ist, ersetzt er
atomar (``os.replace``) den Live-Stand. Schlägt Download, Parsing oder Validierung
fehl, bleibt der ALTE Stand unangetastet. Idempotent, DB-frei, server-seitig.
"""

from __future__ import annotations

import gzip
import io
import json
import logging
import os
import re
import tempfile
import threading
import time
import unicodedata
import zipfile

import httpx

from app.config import settings
from app.services import inkar_loader

log = logging.getLogger(__name__)

_STORE_PATH = os.path.join(settings.REGIONALSTATISTIK_CACHE_DIR, "budget_71717.json.gz")

# Regionalebene der Berichtseinheiten (Einheitsgemeinden/Ämter/VGs).
_LEVEL = "FGEMEIN"
_MISSING = {"", "-", ".", "..", "...", "…", "x", "/"}

_mem: dict | None = None
_mem_mtime: float = 0.0
_mem_lock = threading.Lock()


# ── Namensnormierung / Schlüssel ────────────────────────────────────────────────

def _norm_name(name: str) -> str:
    """Gemeindename → Vergleichsschlüssel (klein, ohne Rechtsform-Zusätze).

    „Oschatz, Stadt" / „Stadt Oschatz" / „Oschatz (Sachsen)" → ``oschatz``.
    Umlaute bleiben erhalten (beide Seiten identisch normiert)."""
    s = name.strip().lower()
    s = s.split(",")[0]                        # „…, Stadt/Amt/VG" abschneiden
    s = re.sub(r"\s*\(.*?\)", "", s)           # Klammerzusätze „(Ems)"
    s = re.sub(r"^(stadt|gemeinde|markt|flecken)\s+", "", s)  # führende Rechtsform
    s = re.sub(r"\s+", " ", s).strip()
    return s


def _key(kreis5: str, name: str) -> str:
    return f"{kreis5}|{_norm_name(name)}"


def _to_number(cell: str) -> float | None:
    c = cell.strip().strip('"')
    if c in _MISSING:
        return None
    s = c.replace(".", "").replace(",", ".") if "," in c else c
    try:
        return float(s)
    except (ValueError, TypeError):
        return None


# ── Parsing des ffcsv → Lookup ──────────────────────────────────────────────────

def build_lookup(text: str) -> dict[str, dict]:
    """71717-ffcsv → ``{"<kreis5>|<name>": {"label", "series": {year: eur}}}``.

    Nur Ebene ``FGEMEIN`` und Kennzahl ``AUSZ001``; Fehlwerte werden übersprungen.
    """
    lines = text.splitlines()
    if len(lines) < 2:
        return {}
    header = [c.strip().strip('"') for c in lines[0].split(";")]
    col = {n: i for i, n in enumerate(header)}
    need = ("1_variable_code", "1_variable_attribute_code", "1_variable_attribute_label",
            "time", "value", "value_variable_code")
    if any(n not in col for n in need):
        return {}
    li, ci, lbi = col["1_variable_code"], col["1_variable_attribute_code"], col["1_variable_attribute_label"]
    ti, vi, vvi = col["time"], col["value"], col["value_variable_code"]

    out: dict[str, dict] = {}
    for line in lines[1:]:
        c = line.split(";")
        if len(c) <= vvi:
            continue
        if c[li].strip().strip('"') != _LEVEL or c[vvi].strip().strip('"') != settings.REGIONALSTATISTIK_BUDGET_VARIABLE:
            continue
        code = re.sub(r"\D", "", c[ci])
        year_s = c[ti].strip().strip('"')
        if len(code) < 5 or not re.match(r"^(19|20)\d{2}$", year_s):
            continue
        val = _to_number(c[vi])
        if val is None:
            continue
        label = c[lbi].strip().strip('"')
        entry = out.setdefault(_key(code[:5], label), {"label": label, "series": {}})
        entry["series"][int(year_s)] = val
    return out


# ── Validierung ─────────────────────────────────────────────────────────────────

# Anker: müssen vorhanden und grob plausibel sein (Kreis5|Name → grobe Untergrenze €).
_ANCHORS = {
    "14713|leipzig": 1e9,     # kreisfreie Großstadt
    "14612|dresden": 1e9,
}


def _validate(lookup: dict) -> tuple[bool, str]:
    """Plausibilitätscheck vor dem atomaren Swap. (ok, Begründung)."""
    if len(lookup) < 3000:
        return False, f"zu wenige Berichtsgemeinden ({len(lookup)})"
    for key, floor in _ANCHORS.items():
        entry = lookup.get(key)
        if not entry or not entry["series"]:
            return False, f"Anker fehlt: {key}"
        if max(entry["series"].values()) < floor:
            return False, f"Anker {key} unplausibel niedrig"
    return True, f"{len(lookup)} Berichtsgemeinden, Anker ok"


# ── GENESIS-Job/Batch-Transport ─────────────────────────────────────────────────

def _post(client: httpx.Client, ep: str, data: dict, timeout: float | None = None) -> httpx.Response:
    body = {"language": "de", **data}
    kw = {} if timeout is None else {"timeout": timeout}
    return client.post(f"{settings.REGIONALSTATISTIK_API_BASE.rstrip('/')}/{ep}",
                       headers=inkar_loader._auth_headers(), data=body, **kw)


def fetch_budget_table() -> str | None:
    """Volle 71717-Tabelle über den Job/Batch-Pfad als ffcsv-Text (oder ``None``).

    Ablauf: ``data/tablefile?job=true`` → Auftragsnamen aus der Antwort ziehen →
    **direkt** ``data/resultfile`` pollen (JSON = noch nicht fertig, ZIP = fertig)
    und die eine CSV entpacken. Bewusst NICHT über ``catalogue/jobs`` gepollt:
    dieser Endpoint liefert bei leerer/instabiler Job-Liste HTTP 404 und ist auf
    dem trägen RS-Server unzuverlässig — ``data/resultfile`` ist die robuste,
    idempotente Statusquelle.

    Getrennte Timeouts: kurzer Connect (schneller Abbruch bei Server-Hängern,
    dann nächster Poll), langer Read (der fertige Abruf lädt viele MB). Bei
    Submit-/Netz-Fehler oder Zeitüberschreitung → ``None`` (Store bleibt).
    """
    if inkar_loader._auth_headers() is None:
        log.warning("finance_bulk: keine Regionalstatistik-Zugangsdaten")
        return None
    table = settings.REGIONALSTATISTIK_TABLE_BUDGET
    to = httpx.Timeout(settings.REGIONALSTATISTIK_JOB_DOWNLOAD_S, connect=30.0)
    try:
        with httpx.Client(timeout=to, follow_redirects=True) as client:
            # Submit mit Retries — der RS-Server hängt sporadisch beim Anlegen.
            # Ohne startyear liefert GENESIS nur das AKTUELLSTE Jahr → mehrere
            # Jahre anfordern (rollierendes Fenster), damit der Ø sinnvoll ist.
            startyear = str(time.localtime().tm_year - (settings.REGIONALSTATISTIK_BUDGET_AVG_YEARS + 4))
            name = None
            for attempt in range(settings.REGIONALSTATISTIK_JOB_SUBMIT_TRIES):
                try:
                    sub = _post(client, "data/tablefile", {
                        "name": table, "area": "all", "format": "ffcsv",
                        "compress": "true", "transpose": "false", "job": "true",
                        "startyear": startyear,
                    }, timeout=httpx.Timeout(settings.REGIONALSTATISTIK_JOB_SUBMIT_S, connect=30.0)).json()
                except (httpx.RequestError, ValueError) as exc:
                    log.info("finance_bulk: Submit-Versuch %d fehlgeschlagen (%s), retry …",
                             attempt + 1, type(exc).__name__)
                    time.sleep(settings.REGIONALSTATISTIK_JOB_POLL_S)
                    continue
                status = sub.get("Status", {})
                if status.get("Code") == 99:
                    name = status["Content"].split(":")[-1].strip()
                    break
                log.warning("finance_bulk: Job nicht erstellt: %s", status.get("Content", sub))
                return None
            if not name:
                log.warning("finance_bulk: Submit nach %d Versuchen fehlgeschlagen",
                            settings.REGIONALSTATISTIK_JOB_SUBMIT_TRIES)
                return None
            log.info("finance_bulk: Job %s erstellt, polle data/resultfile …", name)

            deadline = time.time() + settings.REGIONALSTATISTIK_JOB_MAX_WAIT_S
            while time.time() < deadline:
                time.sleep(settings.REGIONALSTATISTIK_JOB_POLL_S)
                try:
                    resp = _post(client, "data/resultfile", {
                        "name": name, "area": "all", "compress": "true", "format": "ffcsv",
                    })
                except httpx.RequestError as exc:
                    log.info("finance_bulk: Poll-Fehler (retry): %s", exc)
                    continue
                body = resp.content
                if body[:2] == b"PK":
                    with zipfile.ZipFile(io.BytesIO(body)) as zf:
                        log.info("finance_bulk: Ergebnis %s abgerufen (%d Bytes)", name, len(body))
                        return zf.read(zf.namelist()[0]).decode("utf-8-sig", "replace")
                # sonst: JSON „noch nicht fertig / keine Objekte" → weiter warten
            log.warning("finance_bulk: Job %s nicht rechtzeitig fertig", name)
            return None
    except Exception as exc:
        log.warning("finance_bulk: Abruf fehlgeschlagen: %s", exc)
        return None


# ── Atomarer, selbstheilender Import ────────────────────────────────────────────

def _write_store(lookup: dict) -> None:
    """Store atomar schreiben (Temp + ``os.replace``)."""
    os.makedirs(os.path.dirname(_STORE_PATH), exist_ok=True)
    payload = {
        "meta": {
            "generated": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "table": settings.REGIONALSTATISTIK_TABLE_BUDGET,
            "variable": settings.REGIONALSTATISTIK_BUDGET_VARIABLE,
            "level": _LEVEL, "unit": "EUR", "count": len(lookup),
        },
        "gemeinden": lookup,
    }
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(_STORE_PATH), suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(gzip.compress(json.dumps(payload, ensure_ascii=False).encode("utf-8")))
        os.replace(tmp, _STORE_PATH)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)


def run_import(text: str | None = None) -> bool:
    """Kompletter Import mit selbstheilendem, atomarem Swap. ``True`` bei Erfolg.

    ``text`` optional (für Tests/Offline); sonst wird die Tabelle live gezogen.
    Bei Download-/Parse-/Validierungsfehler bleibt der bestehende Store erhalten.
    """
    text = text if text is not None else fetch_budget_table()
    if not text:
        log.warning("finance_bulk: kein Tabellentext — Store unverändert")
        return False
    lookup = build_lookup(text)
    ok, reason = _validate(lookup)
    if not ok:
        log.warning("finance_bulk: Validierung fehlgeschlagen (%s) — Store unverändert", reason)
        return False
    _write_store(lookup)
    with _mem_lock:
        global _mem, _mem_mtime
        _mem, _mem_mtime = None, 0.0  # Cache invalidieren
    # Kommunen-Finanzcache verwerfen, damit Chips die neuen Werte ziehen.
    _clear_finance_osm_cache()
    log.info("finance_bulk: Import ok — %s", reason)
    return True


def _clear_finance_osm_cache() -> None:
    try:
        d = settings.REGIONALSTATISTIK_CACHE_DIR
        for fn in os.listdir(d):
            if fn.startswith("finance_osm_") and fn.endswith(".json"):
                os.remove(os.path.join(d, fn))
    except Exception as exc:
        log.debug("finance_bulk: finance_osm-Cache-Reset übersprungen: %s", exc)


# ── Chip-Lookup ─────────────────────────────────────────────────────────────────

def _load_store() -> dict:
    """Store (mem-gecacht, invalidiert bei Datei-mtime-Änderung)."""
    global _mem, _mem_mtime
    try:
        mtime = os.path.getmtime(_STORE_PATH)
    except OSError:
        return {}
    with _mem_lock:
        if _mem is not None and mtime == _mem_mtime:
            return _mem
        try:
            with open(_STORE_PATH, "rb") as fh:
                _mem = json.loads(gzip.decompress(fh.read()).decode("utf-8")).get("gemeinden", {})
            _mem_mtime = mtime
        except Exception as exc:
            log.warning("finance_bulk: Store nicht lesbar: %s", exc)
            _mem, _mem_mtime = {}, mtime
        return _mem


def budget_for_kommune(ags: str | None, name: str | None) -> dict | None:
    """``{avg_expenditure_eur, years, level}`` aus dem Bulk-Store — netzfrei.

    Match über ``kreis5`` (= ``ags[:5]``) + normalisierten Namen; Ø der letzten
    ``REGIONALSTATISTIK_BUDGET_AVG_YEARS`` Jahre. ``None``, wenn nicht gefunden.
    """
    if not settings.REGIONALSTATISTIK_BUDGET_ENABLED or not ags or not name:
        return None
    ags = re.sub(r"\D", "", ags)
    if len(ags) < 5:
        return None
    entry = _load_store().get(_key(ags[:5], name))
    if not entry or not entry.get("series"):
        return None
    series = {int(y): v for y, v in entry["series"].items()}
    years = sorted(series)[-settings.REGIONALSTATISTIK_BUDGET_AVG_YEARS:]
    if not years:
        return None
    mean = sum(series[y] for y in years) / len(years)
    return {"avg_expenditure_eur": round(mean, 0), "years": years, "level": "gemeinde"}
