"""Overpass-Ausweich-Server bei Gemeindegrenze und AGS-Auflösung (T-1954).

Hauptserver 504, erster Ausweich-Server ``httpx.ConnectError``: der zweite
Ausweich-Server antwortet. Geprüft wird die Aufrufreihenfolge. Kein Netz.
"""

from __future__ import annotations

import asyncio

import httpx

from app.config import settings
from app.services import inkar_loader, osm_service

HAUPT = settings.OVERPASS_URL
ERSTER, ZWEITER = settings.OVERPASS_FALLBACK_URLS[0], settings.OVERPASS_FALLBACK_URLS[1]
AUSSEN = [(0.0, 0.0), (10.0, 0.0), (10.0, 10.0), (0.0, 10.0), (0.0, 0.0)]


def _antwort(url: str, nutzlast: dict):
    req = httpx.Request("POST", url)
    if url == HAUPT:
        return httpx.Response(504, request=req)
    if url == ERSTER:
        raise httpx.ConnectError("Verbindung abgewiesen", request=req)
    return httpx.Response(200, request=req, json=nutzlast)


def test_gemeindegrenze_naechster_server_nach_504_und_connecterror(monkeypatch):
    aufgerufen: list[str] = []
    nutzlast = {"elements": [{"type": "relation", "id": 1, "members": [
        {"type": "way", "role": "outer",
         "geometry": [{"lon": lon, "lat": lat} for lon, lat in AUSSEN]},
    ]}]}

    async def _post(self, url, **kwargs):
        aufgerufen.append(url)
        return _antwort(url, nutzlast)

    async def _nichts(s):
        return None

    async def _ohne_nominatim(*a, **k):
        return None

    monkeypatch.setattr(httpx.AsyncClient, "post", _post)
    monkeypatch.setattr(osm_service.asyncio, "sleep", _nichts)
    monkeypatch.setattr(osm_service, "_fetch_via_nominatim", _ohne_nominatim)

    ergebnis = asyncio.run(osm_service.fetch_kommune_boundary("1", "relation"))

    assert ergebnis["type"] == "MultiPolygon"
    assert aufgerufen == [HAUPT, ERSTER, ZWEITER]


def test_resolve_ags_naechster_server_nach_504_und_connecterror(monkeypatch):
    aufgerufen: list[str] = []
    nutzlast = {"elements": [{"tags": {"de:amtlicher_gemeindeschluessel": "03256034"}}]}

    class _Client:
        def __init__(self, *a, **k):
            pass

        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def post(self, url, **kwargs):
            aufgerufen.append(url)
            return _antwort(url, nutzlast)

    monkeypatch.setattr(inkar_loader.httpx, "Client", _Client)
    monkeypatch.setattr(inkar_loader.time, "sleep", lambda s: None)

    assert inkar_loader.resolve_ags("relation/123") == "03256034"
    assert aufgerufen == [HAUPT, ERSTER, ZWEITER]
