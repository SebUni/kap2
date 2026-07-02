"""Zentrale Logging-Konfiguration – alle Backend-Logs nach backend/logs/."""

from __future__ import annotations

import logging
import logging.handlers
import os

_BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(_BACKEND_DIR, "logs")

_LOG_FMT = logging.Formatter(
    "%(asctime)s %(levelname)s %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def _rotating_handler(filename: str) -> logging.Handler:
    os.makedirs(LOG_DIR, exist_ok=True)
    handler = logging.handlers.RotatingFileHandler(
        os.path.join(LOG_DIR, filename),
        maxBytes=5_000_000,
        backupCount=3,
        encoding="utf-8",
    )
    handler.setFormatter(_LOG_FMT)
    handler.setLevel(logging.DEBUG)
    return handler


def setup_logging() -> None:
    """Schreibt App- und Uvicorn-Logs ausschließlich nach backend/logs/."""
    if getattr(setup_logging, "_configured", False):
        return

    app_handler = _rotating_handler("kap2.log")
    uvicorn_handler = _rotating_handler("uvicorn.log")
    access_handler = _rotating_handler("access.log")

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    root.handlers.clear()
    root.addHandler(app_handler)

    for name in ("uvicorn", "uvicorn.error"):
        logger = logging.getLogger(name)
        logger.handlers.clear()
        logger.addHandler(uvicorn_handler)
        logger.propagate = False
        logger.setLevel(logging.INFO)

    access_logger = logging.getLogger("uvicorn.access")
    access_logger.handlers.clear()
    access_logger.addHandler(access_handler)
    access_logger.propagate = False
    access_logger.setLevel(logging.INFO)

    logging.getLogger("app").setLevel(logging.DEBUG)

    setup_logging._configured = True
