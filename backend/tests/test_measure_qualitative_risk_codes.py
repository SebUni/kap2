"""Tests für den neuen Katalog-Schlüssel ``qualitative_risk_codes`` (Ticket T-0015).

Trennt Zuordnung (Maßnahme ⇄ Risiko) von Wirkung (``linked_risk_codes``): eine
Maßnahme kann fachlich einem Risiko zugeordnet sein, ohne dass ein Rechenweg sie
liest. Kontext: Befund 124 (reviews/BEFUNDE_96.md) sperrt für
EXPECTED_ANNUAL_ALLERGY_DAYS jeden ``linked_risk_codes``-Wirkungskanal (flächiger,
zellunscharfer Pauschalfaktor — Modellgrenze 7); die Zuordnung der Pollen-
Frühwarnung (S158, Register-ID 96-S158-01) läuft deshalb ausschließlich über
``qualitative_risk_codes``.

Diese Datei prüft NUR die Trennung selbst (Punkt 3 des Tickets); die Sperre aus
Befund 124 bleibt exklusiv in ``test_methodik_96_golden.py::test_no_flat_measure_on_allergy_days``
(unangetastet).
"""

from __future__ import annotations

import copy
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.data import catalog  # noqa: E402
from app.services import measure_service  # noqa: E402
from app.services.engine import risk_engine  # noqa: E402

CODE = "EXPECTED_ANNUAL_ALLERGY_DAYS"


def _pollen_measure() -> dict:
    m = next((m for m in catalog.MEASURES
              if CODE in (m.get("qualitative_risk_codes") or [])), None)
    assert m is not None, (
        "Erwarte eine Maßnahme mit qualitative_risk_codes ⊇ {EXPECTED_ANNUAL_ALLERGY_DAYS}")
    return m


def test_qualitative_measure_has_no_linked_risk_codes_overlap_anywhere():
    """Punkt 3 (zweiter Teil): kein MEASURES-Eintrag führt denselben Code in
    ``linked_risk_codes`` UND ``qualitative_risk_codes`` (wertunabhängige Sperre,
    keine Zeitbombe bei künftigen Parameter-Overrides)."""
    bad = []
    for m in catalog.MEASURES:
        linked = set(m.get("linked_risk_codes") or [])
        qualitative = set(m.get("qualitative_risk_codes") or [])
        overlap = linked & qualitative
        if overlap:
            bad.append((m["code"], sorted(overlap)))
    assert not bad, f"Risikocode gleichzeitig linked UND qualitative: {bad}"


def test_pollen_measure_is_assigned_qualitatively_not_linked():
    """Die neue Pollen-Frühwarnung ist #96 zugeordnet, aber nicht verknüpft."""
    m = _pollen_measure()
    assert CODE not in (m.get("linked_risk_codes") or [])
    assert m.get("default_reduction") == 0.0


def test_qualitative_measure_does_not_change_cell_outcome_or_cost():
    """Punkt 3 (erster Teil): outcome/cost_eur der Zelle sind mit und ohne die
    qualitative Maßnahme bitgleich — geprüft über denselben Mechanismus, den
    ``measure_service._adjusted_cell_data`` für das Mit-Maßnahmen-Aggregat nutzt
    (Z. 567–579: ``_reduction_factor`` je Maßnahme, multipliziert nur für Codes aus
    ``linked_risk_codes``; ``qualitative_risk_codes`` geht in diese Schleife nicht ein).
    """
    mdef = _pollen_measure()

    cell = {"inputs": {"pop": 1000.0},
            "risks": {CODE: {"index": 30.0, "outcome": 500.0, "cost_eur": 3100.0}}}

    # Basis-Aggregat ohne jede Maßnahme.
    base = risk_engine.aggregate([copy.deepcopy(cell)], 1000.0, 10.0)

    # Mit-Maßnahmen-Pfad NACHGEBILDET wie measure_service._adjusted_cell_data
    # (Z. 567–579): volle Abdeckung (fraction=1.0), Faktor je Maßnahme, aber nur für
    # in linked_risk_codes gelistete Codes multiplikativ verrechnet.
    factor = measure_service._reduction_factor(mdef, fraction=1.0, unit_factor=1.0)
    cell_factors: dict[str, float] = {}
    for code in mdef.get("linked_risk_codes", []):
        cell_factors[code] = cell_factors.get(code, 1.0) * factor

    scaled = copy.deepcopy(cell)
    for rcode, r in scaled["risks"].items():
        f = cell_factors.get(rcode, 1.0)
        r["index"] = r["index"] * f
        if "outcome" in r:
            r["outcome"] = r["outcome"] * f
        if "cost_eur" in r:
            r["cost_eur"] = r["cost_eur"] * f
    with_measure = risk_engine.aggregate([scaled], 1000.0, 10.0)

    assert base["risks"][CODE]["outcome"] == with_measure["risks"][CODE]["outcome"]
    assert base["risks"][CODE]["cost_eur"] == with_measure["risks"][CODE]["cost_eur"]
    # Gegenprobe: die Maßnahme hat überhaupt eine (potenziell) wirksame Konfiguration
    # (default_reduction 0.0 allein wäre ein zu schwacher Test) — mit einem
    # HYPOTHETISCH linked Code würde derselbe Mechanismus sehr wohl skalieren, sobald
    # default_reduction > 0 wäre. Wir bestätigen daher zusätzlich, dass der Code schlicht
    # nie in die Faktor-Schleife gelangt:
    assert CODE not in cell_factors


if __name__ == "__main__":
    import pytest

    sys.exit(pytest.main([__file__, "-q"]))
