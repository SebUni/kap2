"""T-0446: Kategoriale Gewissheitsstufe je Klimawirkung (Konformitäts-Checkliste Zeile 8).

Prüft ``app.services.gewissheit.gewissheitsstufe``:
(a) für jeden Code aus ``catalog.RISKS_BY_CODE`` einer der vier Werte, nie ``None``,
(b) ein konstruiertes Risiko, dessen Parameter ausnahmslos ``belegt`` sind → ``hoch``,
(c) ein konstruiertes Risiko, dessen Parameter ausnahmslos unbelegt sind → ``sehr gering``.
"""

from __future__ import annotations

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.data import catalog  # noqa: E402
from app.services import gewissheit, parameter_registry  # noqa: E402

SKALA = {"sehr gering", "gering", "mittel", "hoch"}
TESTCODE = "TEST_KONSTRUIERTES_RISIKO"


def test_jeder_risikocode_hat_eine_stufe_der_skala():
    assert catalog.RISKS_BY_CODE, "Katalog ohne Risiken"
    stufen = gewissheit.gewissheitsstufen()
    for code in catalog.RISKS_BY_CODE:
        einzeln = gewissheit.gewissheitsstufe(code)
        assert einzeln is not None, f"{code}: Stufe ist None"
        assert einzeln in SKALA, f"{code}: {einzeln!r} liegt nicht auf der Skala"
        assert stufen.get(code) == einzeln, f"{code}: Sammel- und Einzelwert weichen ab"


def _konstruiertes_risiko(monkeypatch, klassen: list[str]) -> None:
    """Hängt ein Testrisiko an, dessen Registry-Parameter genau ``klassen`` tragen."""
    monkeypatch.setitem(catalog.RISKS_BY_CODE, TESTCODE, {"code": TESTCODE, "name": "Test"})
    params = [
        {"id": f"risks.{TESTCODE}.p{i}", "layer_code": TESTCODE,
         "layer_category": "risks", "evidence_class": k}
        for i, k in enumerate(klassen)
    ]

    def fake_catalog_parameters(layer_code=None, layer_category=None):
        return [p for p in params if layer_code in (None, p["layer_code"])]

    monkeypatch.setattr(parameter_registry, "catalog_parameters", fake_catalog_parameters)


def test_alle_parameter_belegt_ergibt_hoch(monkeypatch):
    _konstruiertes_risiko(monkeypatch, ["belegt", "belegt", "belegt"])
    assert gewissheit.gewissheitsstufe(TESTCODE) == "hoch"


def test_alle_parameter_unbelegt_ergibt_sehr_gering(monkeypatch):
    _konstruiertes_risiko(monkeypatch, ["abgeschaetzt", "abgeschaetzt", "abgeschaetzt"])
    assert gewissheit.gewissheitsstufe(TESTCODE) == "sehr gering"


@pytest.mark.parametrize("klassen, erwartet", [
    (["belegt", "abgeschaetzt", "abgeschaetzt"], "gering"),
    (["belegt", "abgeschaetzt"], "mittel"),
    ([], "sehr gering"),
])
def test_zwischenstufen_nach_regel(monkeypatch, klassen, erwartet):
    _konstruiertes_risiko(monkeypatch, klassen)
    assert gewissheit.gewissheitsstufe(TESTCODE) == erwartet
