import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import kommune, assessment, measures, config, export, catalog as catalog_route, admin, parameters
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

app.include_router(kommune.router, prefix="/api/kommune", tags=["Kommune"])
app.include_router(assessment.router, prefix="/api", tags=["Assessment"])
app.include_router(measures.router, prefix="/api", tags=["Maßnahmen"])
app.include_router(config.router, prefix="/api", tags=["Konfiguration"])
app.include_router(export.router, prefix="/api", tags=["Export/Import"])
app.include_router(catalog_route.router, prefix="/api", tags=["Katalog"])
app.include_router(parameters.router, prefix="/api", tags=["Parameter"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])


@app.on_event("startup")
def _ensure_tables():
    """Stellt sicher, dass alle Tabellen existieren (DB-Reset-freundlich)."""
    try:
        from app.db.database import Base, engine
        import app.models.models  # noqa: F401  (Modelle registrieren)
        Base.metadata.create_all(bind=engine)
        _migrate_config_columns(engine)
        logging.getLogger("app").info("DB-Tabellen sichergestellt (create_all)")
    except Exception as exc:  # pragma: no cover
        logging.getLogger("app").error("create_all fehlgeschlagen: %s", exc)


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


@app.get("/api/health")
def health():
    return {"status": "ok"}
