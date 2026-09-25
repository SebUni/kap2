"""Vorgabe P1: Einordnungsschwellen stehen in der nutzersichtbaren Parameterliste (T-0892).

Charakterisierungsgruppe (Zeile 7): ``SCHWELLE_UMSETZUNG``, ``SCHWELLE_ENTWICKLUNG``.
Gewissheitsstufe (Zeile 8): ``SCHWELLE_MITTEL`` (Zeile ``anteil < SCHWELLE_MITTEL``).
Wert und Herleitung kommen aus den Modulen, nicht aus einer zweiten Zahl.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest  # noqa: E402

from app.data import catalog  # noqa: E402
from app.services import charakterisierung, gewissheit, parameter_registry  # noqa: E402

# (Parameter-Kennung, Modul, Name der Konstante)
_ERWARTET = [
    ("charakterisierung.schwelle_umsetzung", charakterisierung, "SCHWELLE_UMSETZUNG"),
    ("charakterisierung.schwelle_entwicklung", charakterisierung, "SCHWELLE_ENTWICKLUNG"),
    ("gewissheit.schwelle_mittel", gewissheit, "SCHWELLE_MITTEL"),
]


def _nach_id() -> dict[str, dict]:
    return {p["id"]: p for p in parameter_registry.catalog_parameters()}


@pytest.mark.parametrize("pid,modul,name", _ERWARTET)
def test_schwelle_ist_in_der_parameterliste(pid, modul, name):
    p = _nach_id().get(pid)
    assert p is not None, f"{pid} fehlt in catalog_parameters()"
    assert p["value"] == getattr(modul, name)
    assert p["default_value"] == getattr(modul, name)
    assert p["evidence_class"] == "abgeschaetzt"
    assert p["evidence_derivation"], f"{pid} ohne Herleitung"
    assert p["evidence_derivation"]["wert"] == modul.SCHWELLEN[name]["herleitung"]
    assert p["source_detail"]
    assert p["editable"] is False
    assert p["layer_category"] != "risks"


def test_wert_folgt_der_konstante(monkeypatch):
    """Der Wert wird gelesen, nicht als zweite Zahl geführt."""
    monkeypatch.setattr(charakterisierung, "SCHWELLE_UMSETZUNG", 0.77)
    monkeypatch.setattr(gewissheit, "SCHWELLE_MITTEL", 0.33)
    p = _nach_id()
    assert p["charakterisierung.schwelle_umsetzung"]["value"] == 0.77
    assert p["gewissheit.schwelle_mittel"]["value"] == 0.33


def test_risks_ebene_der_gewissheit_bleibt_unberuehrt():
    ids = {p["id"] for p in parameter_registry.catalog_parameters(layer_category="risks")}
    assert not {pid for pid, _, _ in _ERWARTET} & ids


def test_gewissheitsregel_nutzt_die_schwelle(monkeypatch):
    """Die Ableitungsregel liest ``SCHWELLE_MITTEL`` (keine zweite Zahl im Code)."""
    code = next(iter(catalog.RISKS_BY_CODE))
    params = [{"layer_code": code, "evidence_class": k}
              for k in ("belegt", "abgeschaetzt", "abgeschaetzt")]  # Anteil 1/3
    assert gewissheit.gewissheitsstufe(code, _parameter=params) == "gering"
    monkeypatch.setattr(gewissheit, "SCHWELLE_MITTEL", 0.3)
    assert gewissheit.gewissheitsstufe(code, _parameter=params) == "mittel"
