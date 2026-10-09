"""Overpass-Abfrage der Hitze-Daten: 504 des Hauptservers führt zum Ausweich-Server."""
import httpx

from app.config import settings
from app.services.climate.heat import osm_data


def test_504_hauptserver_faellt_auf_ausweichserver(monkeypatch):
    aufgerufen: list[str] = []

    class _Client:
        def __init__(self, *a, **k):
            pass

        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def post(self, url, **kwargs):
            aufgerufen.append(url)
            req = httpx.Request("POST", url)
            if url == settings.OVERPASS_URL:
                return httpx.Response(504, request=req)
            return httpx.Response(200, request=req, json={"elements": []})

    monkeypatch.setattr(osm_data.httpx, "Client", _Client)
    monkeypatch.setattr("time.sleep", lambda s: None)

    data = osm_data._overpass_query("out;")

    assert data["elements"] == []
    assert aufgerufen[0] == settings.OVERPASS_URL
    assert aufgerufen[1] == settings.OVERPASS_FALLBACK_URLS[0]


def test_verbindungsfehler_am_ausweichserver_fuehrt_zum_naechsten(monkeypatch):
    """Hauptserver 504, erster Ausweich-Server ConnectError, zweiter Erfolg."""
    aufgerufen: list[str] = []
    haupt = settings.OVERPASS_URL
    erster, zweiter = settings.OVERPASS_FALLBACK_URLS[0], settings.OVERPASS_FALLBACK_URLS[1]

    class _Client:
        def __init__(self, *a, **k):
            pass

        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def post(self, url, **kwargs):
            aufgerufen.append(url)
            req = httpx.Request("POST", url)
            if url == haupt:
                return httpx.Response(504, request=req)
            if url == erster:
                raise httpx.ConnectError("Verbindung abgewiesen", request=req)
            return httpx.Response(200, request=req, json={"elements": []})

    monkeypatch.setattr(osm_data.httpx, "Client", _Client)
    monkeypatch.setattr("time.sleep", lambda s: None)

    data = osm_data._overpass_query("out;")

    assert data["elements"] == []
    assert aufgerufen == [haupt, erster, zweiter]
