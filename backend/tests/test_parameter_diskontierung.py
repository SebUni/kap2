"""Vorgabe P1: RZPR und Komponente der relativen Preise stehen getrennt in der Parameterliste.

UBA Methodenkonvention 4.0, Kap. 2.2.3, S. 14–15. Wert und Herleitung kommen aus
``app.data.diskontierung``, nicht aus einer zweiten Zahl.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.data import diskontierung, sources  # noqa: E402
from app.services import parameter_registry  # noqa: E402

_IDS = {
    "diskontierung.rzpr_0",
    "diskontierung.rzpr_1",
    "diskontierung.relative_preise",
}


def _nach_id(**kw) -> dict[str, dict]:
    return {p["id"]: p for p in parameter_registry.catalog_parameters(**kw)}


def test_kategorie_liefert_genau_die_drei_kennungen():
    assert {p["id"] for p in parameter_registry.catalog_parameters(layer_category="diskontierung")} == _IDS


def test_ohne_filter_enthalten():
    assert _IDS <= set(_nach_id())


def test_werte_aus_dem_datenmodul_und_nicht_editierbar():
    ps = _nach_id()
    assert ps["diskontierung.rzpr_0"]["value"] == diskontierung.PURE_TIME_PREFERENCE_RATES[0]
    assert ps["diskontierung.rzpr_1"]["value"] == diskontierung.PURE_TIME_PREFERENCE_RATES[1]
    assert ps["diskontierung.relative_preise"]["value"] == diskontierung.RELATIVE_PRICE_COMPONENT
    for pid in _IDS:
        assert ps[pid]["editable"] is False
        assert ps[pid]["layer_category"] == "diskontierung"


def test_rzpr_belegt_mit_neuer_quelle():
    assert "UBA_MK40_Diskontierung" in sources.SOURCE_REFERENCES
    for pid in ("diskontierung.rzpr_0", "diskontierung.rzpr_1"):
        p = _nach_id()[pid]
        assert p["evidence_class"] == "belegt"
        assert [r["key"] for r in p["references"]] == ["UBA_MK40_Diskontierung"]
        assert "Kap. 2.2.3" in p["source"] and "S. 14–15" in p["source"]


def test_relative_preise_abgeschaetzt_mit_herleitung():
    p = _nach_id()["diskontierung.relative_preise"]
    assert p["evidence_class"] == "abgeschaetzt"
    assert p["evidence_derivation"] == diskontierung.RELATIVE_PRICE_COMPONENT_SPEC["evidence_derivation"]


def test_wert_folgt_der_konstante(monkeypatch):
    monkeypatch.setattr(diskontierung, "PURE_TIME_PREFERENCE_RATES", (0.02, 0.03))
    monkeypatch.setattr(diskontierung, "RELATIVE_PRICE_COMPONENT", 0.005)
    ps = _nach_id()
    assert ps["diskontierung.rzpr_0"]["value"] == 0.02
    assert ps["diskontierung.rzpr_1"]["value"] == 0.03
    assert ps["diskontierung.relative_preise"]["value"] == 0.005
