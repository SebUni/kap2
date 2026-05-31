import logging
import logging.handlers
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import kommune, assessment, measures, config, export, catalog as catalog_route

# ── Logging: stdout + file ────────────────────────────────────────────────────
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "kap2.log")

_fmt = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

# File handler (rotating, max 5 MB, keep 3 backups)
_fh = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=5_000_000, backupCount=3, encoding="utf-8")
_fh.setFormatter(_fmt)
_fh.setLevel(logging.DEBUG)

# Attach file handler to root logger so ALL loggers write to file
root = logging.getLogger()
root.setLevel(logging.DEBUG)
root.addHandler(_fh)

# Prevent uvicorn loggers from propagating (avoids double entries)
for _name in ("uvicorn", "uvicorn.access", "uvicorn.error"):
    _lg = logging.getLogger(_name)
    _lg.addHandler(_fh)
    _lg.propagate = False

logging.getLogger("app").setLevel(logging.DEBUG)

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
)

app.include_router(kommune.router, prefix="/api/kommune", tags=["Kommune"])
app.include_router(assessment.router, prefix="/api", tags=["Assessment"])
app.include_router(measures.router, prefix="/api", tags=["Maßnahmen"])
app.include_router(config.router, prefix="/api", tags=["Konfiguration"])
app.include_router(export.router, prefix="/api", tags=["Export/Import"])
app.include_router(catalog_route.router, prefix="/api", tags=["Katalog"])


@app.on_event("startup")
def _ensure_tables():
    """Stellt sicher, dass alle Tabellen existieren (DB-Reset-freundlich)."""
    try:
        from app.db.database import Base, engine
        import app.models.models  # noqa: F401  (Modelle registrieren)
        Base.metadata.create_all(bind=engine)
        logging.getLogger("app").info("DB-Tabellen sichergestellt (create_all)")
    except Exception as exc:  # pragma: no cover
        logging.getLogger("app").error("create_all fehlgeschlagen: %s", exc)


@app.get("/api/health")
def health():
    return {"status": "ok"}
