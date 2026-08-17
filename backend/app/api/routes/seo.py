"""Auslieferung der statischen SEO-Seiten, Sitemap und robots.txt (Root-Pfade).

In Produktion würde ein Reverse-Proxy ``/klimarisiken/*`` direkt auf die
generierten Dateien mappen; hier liefert FastAPI sie aus, damit Crawler
vollständiges HTML ohne JavaScript erhalten.
"""
import os

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, PlainTextResponse, Response

from app.config import settings

router = APIRouter()


def _lite(*parts: str) -> str:
    return os.path.join(settings.LITE_DATA_DIR, *parts)


@router.get("/robots.txt", response_class=PlainTextResponse)
def robots():
    path = _lite("robots.txt")
    if not os.path.exists(path):
        return PlainTextResponse("User-agent: *\nDisallow:\n")
    with open(path, encoding="utf-8") as fh:
        return PlainTextResponse(fh.read())


@router.get("/sitemap.xml")
def sitemap():
    path = _lite("sitemap.xml")
    if not os.path.exists(path):
        raise HTTPException(404, "Keine Sitemap")
    with open(path, encoding="utf-8") as fh:
        return Response(fh.read(), media_type="application/xml")


@router.get("/klimarisiken/{bundesland}/{page}", response_class=FileResponse)
def gemeinde_page(bundesland: str, page: str):
    # Pfad-Traversal verhindern.
    safe_bl = "".join(c for c in bundesland if c.isalnum() or c == "-")
    safe_page = "".join(c for c in page if c.isalnum() or c in "-.")
    if not safe_page.endswith(".html"):
        safe_page += ".html"
    path = _lite("pages", safe_bl, safe_page)
    if not os.path.exists(path):
        raise HTTPException(404, "Seite nicht gefunden")
    return FileResponse(path, media_type="text/html")
