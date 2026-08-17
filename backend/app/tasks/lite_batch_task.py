"""Admin-getriggerter Deutschland-Batch: Gemeinde-Grobrisiken vorberechnen.

Phasen (Plan §4): A Preflight · B Gemeinde-Ingest (VG250) · C Zensus-Aggregat ·
D INKAR (Kreis, neutraler Fallback ohne Zugangsdaten) · E Scoring (raw, je
Bundesland DWD-Batch) · F Normierung (p5/p95) + Outcome/Kosten · G Artefakte.

Läuft in einem Daemon-Thread (wie ``assessment_task``); Fortschritt in
``lite_batch_runs``. Abbrechbar über ein ``threading.Event`` je Run.
"""
from __future__ import annotations

import logging
import threading
from datetime import datetime

from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models.lite_models import Gemeinde, GemeindeLiteResult, LiteBatchRun
from app.services.lite import dwd_batch, lite_artifacts, lite_scoring, vg250_loader, zensus_gemeinde

log = logging.getLogger(__name__)

_DWD_PARAMS = ["hot_days", "summer_days", "precipGE20mm_days", "precipGE30mm_days", "precipitation"]

# Laufende Runs: run_id → Abbruch-Event
_running: dict[int, threading.Event] = {}
_lock = threading.Lock()


def request_abort(run_id: int) -> bool:
    with _lock:
        ev = _running.get(run_id)
    if ev:
        ev.set()
        return True
    return False


def _set(db: Session, run: LiteBatchRun, **kw) -> None:
    for k, v in kw.items():
        setattr(run, k, v)
    db.commit()


def _aborted(ev: threading.Event, db: Session, run: LiteBatchRun) -> bool:
    if ev.is_set():
        _set(db, run, status="aborted", message="Vom Admin abgebrochen",
             finished_at=datetime.utcnow())
        return True
    return False


def run_batch(run_id: int) -> None:
    ev = threading.Event()
    with _lock:
        _running[run_id] = ev
    db = SessionLocal()
    try:
        run = db.query(LiteBatchRun).filter(LiteBatchRun.id == run_id).first()
        if not run:
            return
        params = run.params or {}
        bundesland = params.get("bundesland") or None
        force_zensus = bool(params.get("force_zensus"))
        _set(db, run, status="running", started_at=datetime.utcnow())

        # ── A Preflight ────────────────────────────────────────────────────
        _set(db, run, phase="A: Preflight", progress_pct=2, message="VG250/Zensus prüfen")
        vg250_loader.ensure_vg250()
        if _aborted(ev, db, run):
            return

        # ── B Gemeinde-Ingest ──────────────────────────────────────────────
        _set(db, run, phase="B: Gemeinden", progress_pct=8, message="VG250 einlesen")
        vg250_loader.ingest_gemeinden(db, bundesland=bundesland)
        gemeinden = db.query(Gemeinde)
        if bundesland:
            gemeinden = gemeinden.filter(Gemeinde.bundesland == bundesland)
        gemeinden = gemeinden.all()
        total = len(gemeinden)
        _set(db, run, total=total)
        if _aborted(ev, db, run):
            return

        # ── C Zensus-Aggregat ──────────────────────────────────────────────
        _set(db, run, phase="C: Zensus", progress_pct=15, message="Zensus 100m→Gemeinde")
        zensus_gemeinde.aggregate(db, gemeinden, force=force_zensus)
        if _aborted(ev, db, run):
            return

        # ── D INKAR (Kreis) ────────────────────────────────────────────────
        # Ohne GENESIS-Zugangsdaten neutraler Fallback (50) — im Scoring gesetzt.
        _set(db, run, phase="D: Sozioökonomie", progress_pct=22)

        # ── E Scoring (raw), je Bundesland DWD-Batch ───────────────────────
        _set(db, run, phase="E: Scoring", progress_pct=25, message="Klimatreiber + H×E×V")
        by_bl: dict[str, list[Gemeinde]] = {}
        for g in gemeinden:
            by_bl.setdefault(g.bundesland or "?", []).append(g)

        raw_store: dict[str, dict[str, dict]] = {}  # ags → {risk: {raw, drivers}}
        processed = 0
        for bl, group in by_bl.items():
            if _aborted(ev, db, run):
                return
            points = [(g.rep_lon, g.rep_lat) for g in group]
            dwd_vals = {p: dwd_batch.sample_many(p, points) for p in _DWD_PARAMS}
            for i, g in enumerate(group):
                dwd = {p: dwd_vals[p][i] for p in _DWD_PARAMS}
                gd = {"population": g.population, "area_km2": g.area_km2,
                      "demographics": g.demographics}
                raw_store[g.ags] = lite_scoring.compute_raw(gd, dwd, socio=None)
                processed += 1
            _set(db, run, processed=processed,
                 progress_pct=25 + 45 * processed / max(total, 1),
                 message=f"Scoring {bl} ({processed}/{total})")
        dwd_batch.free_grid_cache()

        # ── F Normierung (p5/p95) + Outcome/Kosten ─────────────────────────
        _set(db, run, phase="F: Normierung", progress_pct=75, message="Nationale Skalierung")
        raw_by_risk: dict[str, list[float]] = {c: [] for c in lite_scoring.LITE_RISK_CODES}
        for scores in raw_store.values():
            for code in lite_scoring.LITE_RISK_CODES:
                raw_by_risk[code].append(scores[code]["raw"])
        bounds = lite_scoring.normalize_index(raw_by_risk)

        # Alte Ergebnisse dieser Gemeinden ersetzen (idempotent).
        ags_all = list(raw_store.keys())
        db.query(GemeindeLiteResult).filter(
            GemeindeLiteResult.ags.in_(ags_all)).delete(synchronize_session=False)
        db.commit()

        gmap = {g.ags: g for g in gemeinden}
        rows = []
        for ags, scores in raw_store.items():
            g = gmap[ags]
            for code in lite_scoring.LITE_RISK_CODES:
                raw = float(scores[code]["raw"])
                index = float(lite_scoring.raw_to_index(raw, bounds[code]))
                outcome, cost, unit = lite_scoring.outcome_and_cost(
                    code, index, float(g.population or 0), float(g.area_km2 or 0))
                rows.append(GemeindeLiteResult(
                    ags=ags, risk_code=code, raw_score=raw, index_value=index,
                    outcome_value=float(outcome), outcome_unit=unit, cost_eur=float(cost),
                    drivers=scores[code]["drivers"], batch_id=run_id))
            if len(rows) >= 2000:
                db.bulk_save_objects(rows)
                db.commit()
                rows = []
        if rows:
            db.bulk_save_objects(rows)
            db.commit()

        # ── G Artefakte ────────────────────────────────────────────────────
        _set(db, run, phase="G: Artefakte", progress_pct=90, message="values/meta/GeoJSON")
        lite_artifacts.write_all(db)

        # ── H Studie + SEO-Seiten ──────────────────────────────────────────
        _set(db, run, phase="H: Studie & SEO", progress_pct=95, message="Studie + Gemeinde-Seiten")
        from app.services.lite import study_service, seo_pages
        study = study_service.build_study(db)
        seo_pages.generate(db, bl_means=study["bundesland_means"])

        _set(db, run, status="done", phase="Fertig", progress_pct=100,
             message=f"{total} Gemeinden berechnet", finished_at=datetime.utcnow())
        log.info("Lite-Batch #%d fertig: %d Gemeinden", run_id, total)
    except Exception as exc:
        log.exception("Lite-Batch #%d fehlgeschlagen", run_id)
        try:
            run = db.query(LiteBatchRun).filter(LiteBatchRun.id == run_id).first()
            if run:
                _set(db, run, status="error", message=str(exc)[:500],
                     finished_at=datetime.utcnow())
        except Exception:
            pass
    finally:
        with _lock:
            _running.pop(run_id, None)
        db.close()


def start_batch_thread(run_id: int) -> None:
    threading.Thread(target=run_batch, args=(run_id,), name=f"lite-batch-{run_id}",
                     daemon=True).start()


def recover_stale_runs() -> None:
    """Verwaiste ``running``-Läufe nach Serverneustart als Fehler markieren."""
    try:
        with SessionLocal() as db:
            stale = db.query(LiteBatchRun).filter(LiteBatchRun.status == "running").all()
            for r in stale:
                r.status = "error"
                r.message = "Server neu gestartet — Lauf abgebrochen"
                r.finished_at = datetime.utcnow()
            if stale:
                db.commit()
    except Exception:
        log.exception("recover_stale_runs fehlgeschlagen")
