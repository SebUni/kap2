"""Demo-Kommune: Konfiguration, anonyme Sessions, Ebenen-Whitelist, Sweep.

Konzept (Plan §3): Die Demo ist das echte Produkt-UI auf einer vom Admin
vorberechneten Kommune — read-only bis auf Maßnahmen. Alle Einschränkungen
werden SERVERSEITIG erzwungen:
- nur die Demo-Kommune, nur GET + Maßnahmen-Schreibpfade
- nur die 3 Demo-Risiken und deren H/E/V-Ebenen (Rest: 403 bzw. gestrippt)
- Parameter read-only; für gesperrte Ebenen ohne Wert/Quelle
- Maßnahmen session-gebunden (Cookie ohne Max-Age + TTL-Sweep) und limitiert
"""
import logging
import threading
import time
import uuid
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.data import catalog
from app.models.demo_models import AppSetting, DemoSession
from app.models.models import AdaptationMeasure

log = logging.getLogger(__name__)

DEMO_COOKIE = "kap2_demo"
_SETTINGS_KEY = "demo_config"

DEFAULT_CONFIG = {
    "kommune_id": None,
    # Default-Auswahl: Hitze-Gesundheit + Starkregen-Gebäude + Landwirtschaft (Dürre)
    "risk_codes": [
        "EXPECTED_ANNUAL_MORTALITY",
        "EXPECTED_BUILDING_DAMAGE_EUR",
        "EXPECTED_AGRICULTURAL_DAMAGE_EUR",
    ],
    "measure_limit": 10,
    "session_ttl_h": 24,
}


# ── Konfiguration (app_settings, Admin-Tab „Demo") ─────────────────────────

def get_config(db: Session) -> dict:
    row = db.query(AppSetting).filter(AppSetting.key == _SETTINGS_KEY).first()
    cfg = dict(DEFAULT_CONFIG)
    if row and isinstance(row.value, dict):
        cfg.update(row.value)
    return cfg


def set_config(db: Session, updates: dict) -> dict:
    cfg = get_config(db)
    cfg.update({k: v for k, v in updates.items() if k in DEFAULT_CONFIG})
    risk_codes = [c for c in cfg.get("risk_codes", []) if c in catalog.RISKS_BY_CODE]
    if len(risk_codes) != 3:
        raise ValueError("Demo braucht genau 3 gültige Risiko-Codes")
    cfg["risk_codes"] = risk_codes
    row = db.query(AppSetting).filter(AppSetting.key == _SETTINGS_KEY).first()
    if row:
        row.value = cfg
    else:
        db.add(AppSetting(key=_SETTINGS_KEY, value=cfg))
    db.commit()
    return cfg


def demo_kommune_id(db: Session) -> int | None:
    return get_config(db).get("kommune_id")


# ── Ebenen-Whitelist ────────────────────────────────────────────────────────

def enabled_layers(risk_codes: list[str]) -> set[str]:
    """Demo-Risiken + Vereinigung ihrer Hazards/Expositionen/Vulnerabilitäten.

    Alles andere (inkl. Auxiliary-Ebenen) ist in der Demo gesperrt: Name
    sichtbar, aber keine Werte, Quellen oder Wirkungsmechanismen.
    """
    codes: set[str] = set()
    for rc in risk_codes:
        risk = catalog.RISKS_BY_CODE.get(rc)
        if not risk:
            continue
        codes.add(rc)
        codes.update(risk.get("hazards", []))
        codes.update(risk.get("exposures", []))
        codes.update(risk.get("vulnerabilities", []))
    return codes


# ── Parameter-/Katalog-Filterung (Plan §3.5, §3.6) ─────────────────────────

def filter_parameters(params: list[dict], enabled: set[str]) -> list[dict]:
    """Parameter für den Demo-Modus transformieren:
    - alle: ``editable=False``, ``demo_locked=True`` (Hinweis „nur Vollversion")
    - Ebene nicht freigeschaltet: Wert/Einheit/Quelle/Referenzen entfernen
      (``demo_hidden=True``) — sichtbar, DASS es sie gibt, aber nicht der Inhalt.
    """
    out: list[dict] = []
    for p in params:
        q = dict(p)
        q["editable"] = False
        q["demo_locked"] = True
        if p.get("layer_code") and p["layer_code"] not in enabled:
            q["demo_hidden"] = True
            for k in ("value", "default_value", "unit", "source", "source_detail",
                      "references", "custom_source"):
                q.pop(k, None)
        out.append(q)
    return out


def filter_catalog(catalog_payload: dict, enabled: set[str], risk_codes: list[str]) -> dict:
    """Katalog für den Demo-Modus strippen: gesperrte H/E/V/Risiken/Auxiliary
    behalten nur Code/Name/Gruppe/Kategorie (+ ``demo_locked``) — keine
    Beschreibung, Quelle, Formel oder Wirkungskette. Maßnahmen bleiben, werden
    aber auf die freigeschalteten Risiken gefiltert."""
    # Struktur-Felder bleiben (Codes/Kategorien/HEV-Verknüpfung) — das Frontend
    # braucht sie zum Rendern der Listen. Sensibel und daher entfernt: description,
    # source, source_detail, references, proxy, Formeln, norm_min/max, ref_value.
    keep_meta = ("code", "name", "group", "category", "hazard_category",
                 "exposure_category", "vulnerability_category",
                 "hazards", "exposures", "vulnerabilities", "cost_dimension",
                 "outcome_unit", "unit", "priority")

    def strip(entry: dict) -> dict:
        code = entry.get("code")
        if code in enabled:
            return entry
        slim = {k: entry[k] for k in keep_meta if k in entry}
        slim["demo_locked"] = True
        return slim

    out = dict(catalog_payload)
    for key in ("hazards", "exposures", "vulnerabilities", "risks", "auxiliary"):
        if key in out:
            out[key] = [strip(e) for e in out[key]]
    if "measures" in out:
        wanted = set(risk_codes)
        out["measures"] = [m for m in out["measures"]
                           if wanted.intersection(m.get("linked_risk_codes", []))]
    return out


# ── Sessions ────────────────────────────────────────────────────────────────

def create_session(db: Session) -> DemoSession:
    session = DemoSession(id=str(uuid.uuid4()))
    db.add(session)
    db.commit()
    return session


def resolve_session(db: Session, session_id: str | None) -> DemoSession | None:
    """Session-ID → lebende Session (oder None). Aktualisiert last_seen
    höchstens einmal pro Minute (kein UPDATE je Request)."""
    if not session_id:
        return None
    session = db.query(DemoSession).filter(DemoSession.id == session_id).first()
    if not session:
        return None
    now = datetime.utcnow()
    ttl_h = get_config(db).get("session_ttl_h", 24)
    if (session.last_seen_at or session.created_at) < now - timedelta(hours=ttl_h):
        return None  # abgelaufen — Sweep räumt sie weg
    if (session.last_seen_at or session.created_at) < now - timedelta(minutes=1):
        session.last_seen_at = now
        db.commit()
    return session


def measure_count(db: Session, session_id: str) -> int:
    return db.query(AdaptationMeasure).filter(
        AdaptationMeasure.demo_session_id == session_id
    ).count()


def active_session_count(db: Session, ttl_h: int) -> int:
    cutoff = datetime.utcnow() - timedelta(hours=ttl_h)
    return db.query(DemoSession).filter(DemoSession.last_seen_at >= cutoff).count()


def sweep_expired(db: Session, ttl_h: int | None = None) -> int:
    """Abgelaufene Demo-Sessions + ihre Maßnahmen löschen.

    Die Maßnahmen werden EXPLIZIT entfernt: auf Bestands-DBs trägt
    ``adaptation_measures.demo_session_id`` keinen FK-Constraint (per ALTER
    ergänzt), sodass ein DB-Cascade nicht greifen würde. So bleibt der Sweep
    portabel und hinterlässt keine verwaisten Demo-Maßnahmen.
    """
    if ttl_h is None:
        ttl_h = get_config(db).get("session_ttl_h", 24)
    cutoff = datetime.utcnow() - timedelta(hours=ttl_h)
    expired_ids = [
        s.id for s in
        db.query(DemoSession.id).filter(DemoSession.last_seen_at < cutoff).all()
    ]
    if not expired_ids:
        return 0
    from app.models.models import MeasureImpact
    measure_ids = [
        m.id for m in
        db.query(AdaptationMeasure.id)
        .filter(AdaptationMeasure.demo_session_id.in_(expired_ids)).all()
    ]
    if measure_ids:
        db.query(MeasureImpact).filter(
            MeasureImpact.measure_id.in_(measure_ids)
        ).delete(synchronize_session=False)
        db.query(AdaptationMeasure).filter(
            AdaptationMeasure.id.in_(measure_ids)
        ).delete(synchronize_session=False)
    db.query(DemoSession).filter(
        DemoSession.id.in_(expired_ids)
    ).delete(synchronize_session=False)
    db.commit()
    log.info("Demo-Sweep: %d Sessions + %d Maßnahmen entfernt",
             len(expired_ids), len(measure_ids))
    return len(expired_ids)


# ── Stündlicher Sweep-Thread ────────────────────────────────────────────────

_sweeper_started = threading.Lock()
_sweeper_running = False


def ensure_sweeper_started() -> None:
    global _sweeper_running
    with _sweeper_started:
        if _sweeper_running:
            return
        _sweeper_running = True

    def _loop():
        from app.db.database import SessionLocal
        while True:
            time.sleep(3600)
            try:
                with SessionLocal() as db:
                    sweep_expired(db)
            except Exception:
                log.exception("Demo-Sweep fehlgeschlagen")

    threading.Thread(target=_loop, name="demo-sweeper", daemon=True).start()
