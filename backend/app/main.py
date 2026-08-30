import logging

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.deps import require_admin, require_kommune_access
from app.config import settings
from app.api.routes import (
    auth as auth_route, contact as contact_route, demo as demo_route,
    admin_demo as admin_demo_route, public_lite as public_lite_route,
    admin_lite as admin_lite_route, admin_users as admin_users_route,
    seo as seo_route,
    kommune, assessment, measures, config, export,
    catalog as catalog_route, admin, parameters,
    ai as ai_route,
)
from app.log_config import setup_logging

setup_logging()

app = FastAPI(
    title="KAP2 – Klimafolgen-Anpassungsplanung",
    version="0.1.0",
    description="Webbasiertes Tool zur Klimafolgen-Abschätzung und Anpassungsplanung für Kommunen",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Uncompressed-Length", "Content-Length"],
)

# Öffentlich: Login/Logout/Me (setzt bzw. löscht das Session-Cookie).
app.include_router(auth_route.router, prefix="/api/auth", tags=["Auth"])
# Öffentlich: Kontakt-/Beratungsanfrage (rate-limited).
app.include_router(contact_route.router, prefix="/api/public", tags=["Public"])
# Öffentlich: Demo-Session-Bootstrap + Meta (M0-Verschlankung: abschaltbar,
# nicht gemountete Pfade liefern 404; Admin-Demo-Konfiguration bleibt an).
if settings.DEMO_ENABLED:
    app.include_router(demo_route.router, prefix="/api/demo", tags=["Demo"])
# Öffentlich: Deutschland-Karte (statische Artefakte + Gemeinde-Lookup).
# Bleibt gemountet (Studien-Endpunkte tragen eigene STUDY_ENABLED-Guards);
# ohne Frontend-Route/Nav und ohne SEO-Seiten ist die Karte nicht verlinkt.
app.include_router(public_lite_route.router, prefix="/api/public/lite", tags=["Public"])
# Öffentlich: SEO-Seiten, Sitemap, robots.txt (Root-Pfade, crawlerbar).
if settings.LITE_PAGES_ENABLED:
    app.include_router(seo_route.router, tags=["SEO"])

# Produkt-Router: Login erzwungen; Routen mit {kommune_id} zusätzlich auf die
# Kommune-Zuordnung geprüft (Admin: alles). Details in app/api/deps.py.
_PROTECTED = [Depends(require_kommune_access)]
app.include_router(kommune.router, prefix="/api/kommune", tags=["Kommune"], dependencies=_PROTECTED)
app.include_router(assessment.router, prefix="/api", tags=["Assessment"], dependencies=_PROTECTED)
app.include_router(measures.router, prefix="/api", tags=["Maßnahmen"], dependencies=_PROTECTED)
app.include_router(config.router, prefix="/api", tags=["Konfiguration"], dependencies=_PROTECTED)
app.include_router(export.router, prefix="/api", tags=["Export/Import"], dependencies=_PROTECTED)
app.include_router(catalog_route.router, prefix="/api", tags=["Katalog"], dependencies=_PROTECTED)
app.include_router(parameters.router, prefix="/api", tags=["Parameter"], dependencies=_PROTECTED)
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"], dependencies=[Depends(require_admin)])
app.include_router(admin_demo_route.router, prefix="/api/admin", tags=["Admin"], dependencies=[Depends(require_admin)])
app.include_router(admin_lite_route.router, prefix="/api/admin", tags=["Admin"], dependencies=[Depends(require_admin)])
app.include_router(admin_users_route.router, prefix="/api/admin", tags=["Admin"], dependencies=[Depends(require_admin)])
# KI-Assistent: eigene Auth je Endpunkt (settings=admin, usage/chat=eingeloggt) → kein Router-Guard.
app.include_router(ai_route.router, prefix="/api/ai", tags=["KI-Assistent"])


@app.on_event("startup")
def _ensure_tables():
    """Stellt sicher, dass alle Tabellen existieren (DB-Reset-freundlich)."""
    try:
        from app.db.database import Base, engine
        import app.models.models  # noqa: F401  (Modelle registrieren)
        import app.models.auth_models  # noqa: F401  (users/user_sessions/user_kommunen)
        import app.models.demo_models  # noqa: F401  (demo_sessions/app_settings)
        import app.models.lite_models  # noqa: F401  (gemeinden/lite_results/batch_runs)
        Base.metadata.create_all(bind=engine)
        _migrate_measure_demo_column(engine)
        _migrate_config_columns(engine)
        _migrate_status_columns(engine)
        logging.getLogger("app").info("DB-Tabellen sichergestellt (create_all)")
    except Exception as exc:  # pragma: no cover
        logging.getLogger("app").error("create_all fehlgeschlagen: %s", exc)


@app.on_event("startup")
def _start_background_services():
    """Nach der Schema-Sicherung (Registrierungsreihenfolge): tote Assessment-
    Läufe heilen, Warteschlangen-Scheduler und Artefakt-Rebuild-Worker starten."""
    try:
        from app.tasks.assessment_task import recover_on_startup
        recover_on_startup()
    except Exception as exc:  # pragma: no cover
        logging.getLogger("app").error("recover_on_startup fehlgeschlagen: %s", exc)
    try:
        from app.services.artifact_rebuild import ensure_worker_started
        ensure_worker_started()
    except Exception as exc:  # pragma: no cover
        logging.getLogger("app").error("artifact_rebuild-Start fehlgeschlagen: %s", exc)
    try:
        from app.db.database import SessionLocal
        from app.services.auth_service import purge_expired
        from app.services import demo_service
        with SessionLocal() as db:
            n = purge_expired(db)
            demo_service.sweep_expired(db)
        if n:
            logging.getLogger("app").info("Auth: %d abgelaufene Sessions entfernt", n)
        if settings.DEMO_ENABLED:
            demo_service.ensure_sweeper_started()
    except Exception as exc:  # pragma: no cover
        logging.getLogger("app").error("Session-Purge/Demo-Sweeper fehlgeschlagen: %s", exc)
    try:
        from app.tasks.lite_batch_task import recover_stale_runs
        recover_stale_runs()
    except Exception as exc:  # pragma: no cover
        logging.getLogger("app").error("lite recover_stale_runs fehlgeschlagen: %s", exc)


def _migrate_config_columns(engine):
    """Fügt neue Spalten an config_parameters hinzu (bestehende DBs)."""
    from sqlalchemy import inspect, text

    insp = inspect(engine)
    if "config_parameters" not in insp.get_table_names():
        return
    cols = {c["name"] for c in insp.get_columns("config_parameters")}
    alters = []
    if "parameter_id" not in cols:
        alters.append("ADD COLUMN parameter_id VARCHAR(200)")
    if "source" not in cols:
        alters.append("ADD COLUMN source TEXT")
    if "custom_source" not in cols:
        alters.append("ADD COLUMN custom_source TEXT")
    if not alters:
        return
    dialect = engine.dialect.name
    with engine.begin() as conn:
        for clause in alters:
            if dialect == "postgresql":
                conn.execute(text(f"ALTER TABLE config_parameters {clause}"))
            else:
                col = clause.replace("ADD COLUMN ", "").split()[0]
                ctype = "VARCHAR(200)" if col == "parameter_id" else "TEXT"
                try:
                    conn.execute(text(f"ALTER TABLE config_parameters ADD COLUMN {col} {ctype}"))
                except Exception:
                    pass


def _migrate_measure_demo_column(engine):
    """Fügt adaptation_measures.demo_session_id hinzu (bestehende DBs)."""
    from sqlalchemy import inspect, text

    insp = inspect(engine)
    if "adaptation_measures" not in insp.get_table_names():
        return
    cols = {c["name"] for c in insp.get_columns("adaptation_measures")}
    if "demo_session_id" in cols:
        return
    with engine.begin() as conn:
        try:
            conn.execute(text(
                "ALTER TABLE adaptation_measures ADD COLUMN demo_session_id VARCHAR(36)"
            ))
        except Exception:  # pragma: no cover
            pass


def _migrate_status_columns(engine):
    """Fügt Kind-Prozess-Spalten an project_statuses hinzu (bestehende DBs)."""
    from sqlalchemy import inspect, text

    insp = inspect(engine)
    if "project_statuses" not in insp.get_table_names():
        return
    cols = {c["name"] for c in insp.get_columns("project_statuses")}
    spec = {
        "worker_pid": "INTEGER",
        "worker_start_ticks": "BIGINT",
        "abort_requested": "BOOLEAN NOT NULL DEFAULT FALSE",
        "queued_at": "TIMESTAMP",
        "recalc_recommended": "BOOLEAN NOT NULL DEFAULT FALSE",
    }
    missing = [(name, ddl) for name, ddl in spec.items() if name not in cols]
    if missing:
        with engine.begin() as conn:
            for name, ddl in missing:
                try:
                    conn.execute(text(f"ALTER TABLE project_statuses ADD COLUMN {name} {ddl}"))
                except Exception:  # pragma: no cover - Nicht-PG-Dialekte
                    pass
    if engine.dialect.name == "postgresql":
        # Enum-Erweiterung braucht Autocommit (ADD VALUE ist transaktionsbeschränkt).
        with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as conn:
            conn.execute(text("ALTER TYPE assessmentstatus ADD VALUE IF NOT EXISTS 'QUEUED'"))


@app.get("/api/health")
def health():
    return {"status": "ok"}
