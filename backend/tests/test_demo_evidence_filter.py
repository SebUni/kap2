"""Demo-Filter: Evidenz-Inhalt gesperrter Ebenen bleibt verborgen.

``filter_parameters()`` entfernt für nicht freigeschaltete Ebenen den Inhalt —
dazu gehören auch ``evidence_note`` (Quellentext bzw. Abschätzungsvermerk) und
``evidence_derivation`` (Herleitung). ``evidence_class`` bleibt erhalten: im
Demo ist sichtbar, DASS es die Angabe gibt, nicht ihr Inhalt.

Geprüft wird ``demo_service.filter_parameters()`` direkt — nicht über den
HTTP-Endpunkt, dessen ``response_model`` die Schema-Defaults wieder auffüllt.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.services import demo_service  # noqa: E402

DERIVATION = {
    "wert": "0,42",
    "band": "0,30–0,55",
    "sensitivitaet": "±30 % auf das Endergebnis",
}


def _param(layer_code: str) -> dict:
    return {
        "id": f"layer.{layer_code}.weight",
        "name": "Gewicht",
        "layer_code": layer_code,
        "value": 0.42,
        "default_value": 0.42,
        "unit": "-",
        "source": "KAP3",
        "source_detail": "Interne Abschätzung KAP3",
        "references": [],
        "evidence_class": "abgeschaetzt",
        "evidence_note": "Interne Abschätzung KAP3",
        "evidence_derivation": dict(DERIVATION),
    }


def test_gesperrte_ebene_verbirgt_evidenz_inhalt():
    (out,) = demo_service.filter_parameters([_param("GESPERRT")], {"FREI"})
    assert out["demo_hidden"] is True
    assert "evidence_note" not in out
    assert "evidence_derivation" not in out
    assert out["evidence_class"] == "abgeschaetzt"


def test_freigeschaltete_ebene_behaelt_evidenz():
    (out,) = demo_service.filter_parameters([_param("FREI")], {"FREI"})
    assert out["evidence_class"] == "abgeschaetzt"
    assert out["evidence_note"] == "Interne Abschätzung KAP3"
    assert out["evidence_derivation"] == DERIVATION
