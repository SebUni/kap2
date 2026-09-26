"""T-1363-cto: dritte Evidenzklasse „berechnet“ (Vorgabe P1, Vorhaben T-1350 #95).

Der Nutzer soll in der Parameterliste unterscheiden können, ob ein Wert aus einer
Quelle stammt („belegt“), von KAP3 abgeschätzt ist („abgeschaetzt“) oder aus amtlichen
Daten berechnet ist („berechnet“, Anzeige „berechnet aus amtlichen Daten“).

Geprüft wird:
(a) ``EVIDENCE_CLASSES`` führt genau die drei Klassen,
(b) die Registry übernimmt ein explizit hinterlegtes „berechnet“ unverändert,
(c) Gewissheitsstufe und Unsicherheits-Zusammenschau zählen „berechnet“ wie „belegt“
    (heutiger Stand; die dritte Klasse ändert keine Stufe und keine Zählung still),
(d) die Maßnahmen-Gewissheit gibt eine hinterlegte Klasse „berechnet“ unverändert aus,
(e) Typ und Anzeige im Frontend kennen die dritte Klasse.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.data import catalog  # noqa: E402
from app.services import (  # noqa: E402
    gewissheit,
    massnahmen_gewissheit,
    parameter_registry,
    unsicherheits_zusammenschau,
)

TESTCODE = "TEST_BERECHNET_RISIKO"
FRONTEND = Path(__file__).resolve().parents[2] / "frontend" / "src"


# ── (a) drei Klassen ────────────────────────────────────────────────────────────

def test_evidence_classes_fuehrt_drei_klassen():
    assert parameter_registry.EVIDENCE_CLASSES == ("belegt", "abgeschaetzt", "berechnet")


def test_belegte_klassen_sind_belegt_und_berechnet():
    assert parameter_registry.BELEGTE_KLASSEN == {"belegt", "berechnet"}


# ── (b) Registry übernimmt „berechnet“ ─────────────────────────────────────────

@pytest.mark.parametrize("references", [None, [{"key": "x"}]])
def test_registry_uebernimmt_berechnet(references):
    p = parameter_registry._base_param(
        "test.berechnet", layer_code="X", layer_category="risks", label="L", value=1,
        references=references, evidence_class="berechnet",
    )
    assert p["evidence_class"] == "berechnet"


def test_unbekannte_klasse_faellt_auf_regel_zurueck():
    ohne = parameter_registry._base_param(
        "test.a", layer_code="X", layer_category="risks", label="L", value=1,
        evidence_class="erfunden",
    )
    mit = parameter_registry._base_param(
        "test.b", layer_code="X", layer_category="risks", label="L", value=1,
        references=[{"key": "x"}], evidence_class="erfunden",
    )
    assert ohne["evidence_class"] == "abgeschaetzt"
    assert mit["evidence_class"] == "belegt"


# ── (c) Gewissheit und Zusammenschau zählen „berechnet“ wie „belegt“ ───────────

def _konstruiertes_risiko(monkeypatch, klassen: list[str]) -> list[dict]:
    monkeypatch.setitem(catalog.RISKS_BY_CODE, TESTCODE, {"code": TESTCODE, "name": "Test"})
    params = [
        {"id": f"risks.{TESTCODE}.p{i}", "layer_code": TESTCODE,
         "layer_category": "risks", "evidence_class": k}
        for i, k in enumerate(klassen)
    ]

    def fake_catalog_parameters(layer_code=None, layer_category=None):
        return [p for p in params if layer_code in (None, p["layer_code"])]

    monkeypatch.setattr(parameter_registry, "catalog_parameters", fake_catalog_parameters)
    return params


@pytest.mark.parametrize("mit_berechnet, nur_belegt", [
    (["berechnet", "berechnet"], ["belegt", "belegt"]),
    (["berechnet", "abgeschaetzt"], ["belegt", "abgeschaetzt"]),
    (["berechnet", "abgeschaetzt", "abgeschaetzt"], ["belegt", "abgeschaetzt", "abgeschaetzt"]),
    (["belegt", "berechnet", "abgeschaetzt"], ["belegt", "belegt", "abgeschaetzt"]),
])
def test_gewissheit_zaehlt_berechnet_wie_belegt(monkeypatch, mit_berechnet, nur_belegt):
    _konstruiertes_risiko(monkeypatch, nur_belegt)
    erwartet = gewissheit.gewissheitsstufe(TESTCODE)
    _konstruiertes_risiko(monkeypatch, mit_berechnet)
    assert gewissheit.gewissheitsstufe(TESTCODE) == erwartet


def test_alle_berechnet_ergibt_hoch(monkeypatch):
    _konstruiertes_risiko(monkeypatch, ["berechnet", "berechnet", "berechnet"])
    assert gewissheit.gewissheitsstufe(TESTCODE) == "hoch"


def test_zusammenschau_zaehlt_berechnet_nicht_als_unbelegt():
    code = next(iter(catalog.RISKS_BY_CODE))
    parameter = [
        {"id": "a", "layer_code": code, "evidence_class": "berechnet"},
        {"id": "b", "layer_code": code, "evidence_class": "belegt"},
        {"id": "c", "layer_code": code, "evidence_class": "abgeschaetzt"},
    ]
    stufen = {c: "mittel" for c in catalog.RISKS_BY_CODE}
    eintraege = unsicherheits_zusammenschau.unsicherheits_zusammenschau(
        1, _parameter=parameter, _stufen=stufen,
    )["handlungsfelder"]
    feld = catalog.RISKS_BY_CODE[code].get("kwra_field") or "ohne Handlungsfeld"
    eintrag = next(e for e in eintraege if e["handlungsfeld"] == feld)
    assert eintrag["parameter_nicht_belegt"] == 1


def test_katalog_heute_unveraendert():
    """Heute trägt kein Registry-Parameter „berechnet“ — die Stufen bleiben, wie sie sind.

    Folgepakete (T-1350 #8/#9) setzen die Klasse an die drei berechneten Blöcke von #95;
    dieser Test hält nur fest, dass jede heutige Klasse gültig ist.
    """
    klassen = {p["evidence_class"] for p in parameter_registry.catalog_parameters()}
    assert klassen <= set(parameter_registry.EVIDENCE_CLASSES)


# ── (d) Maßnahmen-Gewissheit gibt „berechnet“ durch ─────────────────────────────

def test_massnahmen_gewissheit_gibt_berechnet_durch():
    m = {"code": "X", "evidence_classes": {"default_reduction": "berechnet"}}
    assert massnahmen_gewissheit._wirkung_evidenz(m) == "berechnet"


# ── (e) Frontend kennt die dritte Klasse ───────────────────────────────────────

def test_frontend_typ_fuehrt_berechnet():
    typen = (FRONTEND / "types" / "index.ts").read_text(encoding="utf-8")
    assert "export type EvidenceClass = 'belegt' | 'abgeschaetzt' | 'berechnet'" in typen


def test_frontend_anzeige_berechnet_aus_amtlichen_daten():
    tabelle = (FRONTEND / "components" / "ParameterTable.tsx").read_text(encoding="utf-8")
    assert "p.evidence_class === 'berechnet'" in tabelle
    assert "'berechnet aus amtlichen Daten'" in tabelle
