"""resolve_ags: Gemeindeschlüssel aus OSM-Tags (Overpass-Antwort gestubbt, kein Netz)."""
import pytest

from app.services import inkar_loader


class _Resp:
    def __init__(self, tags):
        self._tags = tags

    def raise_for_status(self):
        pass

    def json(self):
        return {"elements": [{"tags": self._tags}]}


def _stub(monkeypatch, tags):
    class _Client:
        def __init__(self, *a, **k):
            pass

        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def post(self, *a, **k):
            return _Resp(tags)

    monkeypatch.setattr(inkar_loader.httpx, "Client", _Client)


@pytest.mark.parametrize(
    "tags, erwartet",
    [
        # Gemeinde 034 im Kreis 03256, Verbandsnummer 5408 nur Beispiel
        ({"de:regionalschluessel": "032565408034"}, "03256034"),
        # Berlin
        ({"de:regionalschluessel": "110000000000"}, "11000000"),
        ({"de:amtlicher_gemeindeschluessel": "03256034"}, "03256034"),
        ({"de:regionalschluessel": "032565408"}, None),
    ],
)
def test_resolve_ags(monkeypatch, tags, erwartet):
    _stub(monkeypatch, tags)
    assert inkar_loader.resolve_ags("relation/123") == erwartet
