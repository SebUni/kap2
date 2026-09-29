"""Gemeindegrenze über Overpass: User-Agent und innere Ringe (T-1590).

``_fetch_via_overpass`` ist der dritte Rückfall von ``fetch_kommune_boundary``.
Die Antwort von Overpass ist per Monkeypatch auf ``httpx.AsyncClient.post``
ersetzt; kein Netz, keine Datenbank.
"""

from __future__ import annotations

import asyncio

import httpx

from app.config import settings
from app.services import osm_service

URL = "https://overpass.example/api/interpreter"


def _member(role: str, ring: list[tuple[float, float]]) -> dict:
    return {
        "type": "way",
        "role": role,
        "geometry": [{"lon": lon, "lat": lat} for lon, lat in ring],
    }


AUSSEN = [(0.0, 0.0), (10.0, 0.0), (10.0, 10.0), (0.0, 10.0), (0.0, 0.0)]
INNEN = [(4.0, 4.0), (6.0, 4.0), (6.0, 6.0), (4.0, 6.0), (4.0, 4.0)]
AUSSEN_2 = [(20.0, 0.0), (30.0, 0.0), (30.0, 10.0), (20.0, 10.0), (20.0, 0.0)]


class _Antwort:
    def __init__(self, daten: dict):
        self._daten = daten

    def raise_for_status(self) -> None:
        return None

    def json(self) -> dict:
        return self._daten


def _abrufen(monkeypatch, members: list[dict]):
    """Ruft ``_fetch_via_overpass`` mit ersetzter Antwort; liefert (Ergebnis, Aufrufe)."""
    aufrufe: list[dict] = []

    async def _post(self, url, **kwargs):
        aufrufe.append({"url": url, **kwargs})
        return _Antwort({"elements": [{"type": "relation", "id": 1, "members": members}]})

    monkeypatch.setattr(httpx.AsyncClient, "post", _post)
    ergebnis = asyncio.run(osm_service._fetch_via_overpass("1", "relation", URL))
    return ergebnis, aufrufe


def test_anfrage_sendet_user_agent(monkeypatch):
    _, aufrufe = _abrufen(monkeypatch, [_member("outer", AUSSEN)])
    assert len(aufrufe) == 1
    assert aufrufe[0]["headers"]["User-Agent"] == settings.NOMINATIM_USER_AGENT


def test_innerer_ring_wird_loch_des_polygons(monkeypatch):
    ergebnis, _ = _abrufen(monkeypatch, [_member("outer", AUSSEN), _member("inner", INNEN)])
    assert ergebnis["type"] == "MultiPolygon"
    assert len(ergebnis["coordinates"]) == 1
    polygon = ergebnis["coordinates"][0]
    assert len(polygon) == 2
    assert [tuple(p) for p in polygon[0]] == AUSSEN
    assert [tuple(p) for p in polygon[1]] == INNEN


def test_innerer_ring_landet_im_passenden_polygon(monkeypatch):
    ergebnis, _ = _abrufen(
        monkeypatch,
        [_member("outer", AUSSEN), _member("outer", AUSSEN_2), _member("inner", INNEN)],
    )
    assert [len(p) for p in ergebnis["coordinates"]] == [2, 1]


def test_nur_aussenringe_geometrie_wie_vorher(monkeypatch):
    ergebnis, _ = _abrufen(monkeypatch, [_member("outer", AUSSEN), _member("outer", AUSSEN_2)])
    assert ergebnis == {"type": "MultiPolygon", "coordinates": [[AUSSEN], [AUSSEN_2]]}


def test_ein_aussenring_geometrie_wie_vorher(monkeypatch):
    ergebnis, _ = _abrufen(monkeypatch, [_member("outer", AUSSEN)])
    assert ergebnis == {"type": "MultiPolygon", "coordinates": [[AUSSEN]]}
