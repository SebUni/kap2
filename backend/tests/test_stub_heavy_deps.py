"""Regression: Das Ersatzmodul greift nur bei fehlenden Paketen (T-0590).

Geprüft wird:
(1) eine fehlende Wurzel aus ``ERSETZBAR`` wird beim Import durch ein
    Ersatzmodul abgedeckt — ohne Endlosrekursion (die frühere Prüfung in
    ``find_spec`` fragte über ``importlib.util.find_spec`` nach und lief dabei
    wieder in denselben Finder);
(2) eine installierte Wurzel wird nicht angetastet, auch wenn sie in
    ``ERSETZBAR`` steht.

Jeder Test arbeitet auf einer eigenen Kopie von ``sys.meta_path`` und räumt
``sys.modules`` wieder auf; der globale Finder aus der conftest bleibt unberührt.
"""

from __future__ import annotations

import importlib
import sys

import pytest

import _stub_heavy_deps

FEHLT = "kap2_gibt_es_nicht_t0590"
DA = "json"  # Standardbibliothek, immer installiert


@pytest.fixture
def eigener_finder(monkeypatch):
    """Hängt einen frischen Finder wie ``install()`` ein, mit Testwurzeln in ERSETZBAR."""
    ohne = [f for f in sys.meta_path if not isinstance(f, _stub_heavy_deps._FallbackFinder)]
    monkeypatch.setattr(sys, "meta_path", ohne)
    monkeypatch.setattr(_stub_heavy_deps._FallbackFinder, "ERSETZBAR",
                        _stub_heavy_deps._FallbackFinder.ERSETZBAR | {FEHLT, DA})
    _stub_heavy_deps.install()
    finder = [f for f in sys.meta_path if isinstance(f, _stub_heavy_deps._FallbackFinder)]
    yield finder
    for name in [n for n in sys.modules if n.split(".")[0] == FEHLT]:
        sys.modules.pop(name, None)


def test_fehlende_wurzel_bekommt_ersatzmodul(eigener_finder):
    assert len(eigener_finder) == 1
    assert FEHLT in eigener_finder[0].fehlend
    mod = importlib.import_module(FEHLT)
    assert isinstance(mod, _stub_heavy_deps._AnyModule)
    unter = importlib.import_module(f"{FEHLT}.unter")
    assert isinstance(unter, _stub_heavy_deps._AnyModule)


def test_installierte_wurzel_bleibt_unangetastet(eigener_finder):
    assert DA not in eigener_finder[0].fehlend
    assert eigener_finder[0].find_spec(DA) is None
    mod = importlib.import_module(DA)
    assert not isinstance(mod, _stub_heavy_deps._AnyModule)
    assert hasattr(mod, "dumps")
