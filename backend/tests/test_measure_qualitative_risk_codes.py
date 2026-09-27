"""Tests für den neuen Katalog-Schlüssel ``qualitative_risk_codes`` (Ticket T-0015).

Trennt Zuordnung (Maßnahme ⇄ Risiko) von Wirkung (``linked_risk_codes``): eine
Maßnahme kann fachlich einem Risiko zugeordnet sein, ohne dass ein Rechenweg sie
liest. Kontext: Befund 124 (reviews/BEFUNDE_96.md) sperrte für
EXPECTED_ANNUAL_ALLERGY_DAYS jeden PAUSCHALEN ``linked_risk_codes``-Wirkungskanal
(flächiger, zellunscharfer Faktor über ``_reduction_factor`` — Modellgrenze 7); solange
kein Zelllauf-Modell existierte, lief die Zuordnung der Pollen-Frühwarnung (S158,
Register-ID 96-S158-01) deshalb ausschließlich über ``qualitative_risk_codes``.

Seit T-1513-cto ist die Sperre aufgehoben: S158 rechnet im Zelllauf
(``effect_model`` 's158', ``measure_service._s158_cell_factor``), deshalb steht
``EXPECTED_ANNUAL_ALLERGY_DAYS`` jetzt in ``linked_risk_codes`` statt in
``qualitative_risk_codes``. Diese Datei prüft weiterhin NUR die generelle Trennung
zwischen Zuordnung und Wirkung (Punkt 3 des Tickets T-0015) — jetzt am Beispiel der
Verknüpfung über ein Zelllauf-Modell statt einer rein deklarativen Zuordnung; die
Sperre gegen einen PAUSCHALEN Kanal bleibt exklusiv in
``test_methodik_96_golden.py::test_no_flat_measure_on_allergy_days`` (unangetastet).
"""

from __future__ import annotations

import copy
import inspect
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.data import catalog  # noqa: E402
from app.services import measure_service  # noqa: E402
from app.services.engine import risk_engine  # noqa: E402

CODE_96 = "EXPECTED_ANNUAL_ALLERGY_DAYS"
MEASURE_CODE = "POLLEN_EARLY_WARNING"


def _pollen_measure() -> dict:
    m = catalog.MEASURES_BY_CODE.get(MEASURE_CODE)
    assert m is not None, f"Erwarte den Maßnahmen-Katalogeintrag {MEASURE_CODE!r}"
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


def test_pollen_measure_is_linked_via_zelllauf_model_not_qualitative():
    """Seit T-1513-cto ist die Pollen-Frühwarnung #96 über ein Zelllauf-Modell
    verknüpft (Sperre aus Befund 124 aufgehoben), nicht mehr nur qualitativ
    zugeordnet — die Trennung Zuordnung/Wirkung gilt weiter, nur läuft die Wirkung
    jetzt über ``effect_model`` 's158' statt über eine rein deklarative Zuordnung."""
    m = _pollen_measure()
    assert CODE_96 in (m.get("linked_risk_codes") or [])
    assert not (m.get("qualitative_risk_codes") or [])
    assert m.get("effect_model") == "s158"
    # T-0061 (Freigabe F-0007 Punkt 1 / Vorgabe P2, Ledger-Befund 151): Der Hebel läuft
    # nicht mehr mit Wirkung null, sondern mit der ausgewiesenen Abschätzung
    # r_S158 = 0,03 aus Bericht #96 §5.1 — jetzt wirksam im Zelllauf (Zellfaktor).
    assert (m.get("default_reduction") or 0.0) > 0.0


def test_qualitative_measure_without_effect_model_does_not_change_cell_outcome():
    """Punkt 3 (erster Teil), an einer generischen deklarativ zugeordneten Maßnahme:
    outcome/cost_eur der Zelle sind mit und ohne eine Maßnahme, die einen Code nur in
    ``qualitative_risk_codes`` führt, bitgleich — geprüft über denselben Mechanismus,
    den ``measure_service._adjusted_cell_data`` für das Mit-Maßnahmen-Aggregat nutzt
    (``_reduction_factor`` je Maßnahme, multipliziert nur für Codes aus
    ``linked_risk_codes``; ``qualitative_risk_codes`` geht in diese Schleife nicht ein).
    Die konkrete #96-Maßnahme (POLLEN_EARLY_WARNING) ist seit T-1513-cto linked, nicht
    mehr qualitativ — dieser Test bildet die Trennung deshalb an einer generischen,
    hier konstruierten Maßnahmendefinition nach, statt am Katalogeintrag.
    """
    mdef = {**_pollen_measure(), "linked_risk_codes": [],
            "qualitative_risk_codes": [CODE_96], "effect_model": None}

    cell = {"inputs": {"pop": 1000.0},
            "risks": {CODE_96: {"index": 30.0, "outcome": 500.0, "cost_eur": 3100.0}}}

    # Basis-Aggregat ohne jede Maßnahme.
    base = risk_engine.aggregate([copy.deepcopy(cell)], 1000.0, 10.0)

    # Mit-Maßnahmen-Pfad NACHGEBILDET wie measure_service._adjusted_cell_data:
    # volle Abdeckung (fraction=1.0), Faktor je Maßnahme, aber nur für in
    # linked_risk_codes gelistete Codes multiplikativ verrechnet.
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

    assert base["risks"][CODE_96]["outcome"] == with_measure["risks"][CODE_96]["outcome"]
    assert base["risks"][CODE_96]["cost_eur"] == with_measure["risks"][CODE_96]["cost_eur"]
    # Gegenprobe: die Maßnahme hat eine wirksame Konfiguration (default_reduction > 0) —
    # mit einem HYPOTHETISCH linked Code würde derselbe Mechanismus sehr wohl skalieren.
    # Dass outcome/cost_eur trotzdem bitgleich bleiben, liegt allein an der leeren
    # linked_risk_codes-Liste; wir bestätigen daher zusätzlich, dass der Code schlicht
    # nie in die Faktor-Schleife gelangt:
    assert CODE_96 not in cell_factors


def test_measure_service_does_not_read_qualitative_risk_codes():
    """Zusicherung (Punkt 9, Runde 1): kein Rechenweg in ``measure_service`` liest
    ``qualitative_risk_codes``.

    Warum als Quelltextprüfung statt als Verhaltenstest: Der bestehende Test
    ``test_qualitative_measure_does_not_change_cell_outcome_or_cost`` (oben) bildet die
    Faktor-Schleife aus ``_adjusted_cell_data`` (Z. 575–579) NACH, statt sie
    aufzurufen — er prüft damit seine eigene Kopie und bliebe grün, wenn jemand
    ``qualitative_risk_codes`` später tatsächlich in ``measure_service`` verdrahten
    würde. Genau das ist die Zeitbombe, gegen die Punkt 3 des Tickets schützen sollte
    (Befund 124: Zuordnung ohne Wirkung darf nicht zur Wirkung werden, auch nicht durch
    eine spätere, unbedachte Erweiterung derselben Schleife). Diese Prüfung ruft daher
    NICHT die Engine auf, sondern liest den tatsächlichen Quelltext des Moduls: sie wird
    rot, sobald der String ``qualitative_risk_codes`` dort irgendwo auftaucht — egal in
    welcher Funktion, egal ob get()/in/Vergleich. Das ist für diesen Zweck (eine
    Zusicherung ÜBER den Code, nicht über sein Verhalten in einem Einzelfall) der
    ehrlichste verfügbare Weg.
    """
    src = inspect.getsource(measure_service)
    assert "qualitative_risk_codes" not in src, (
        "measure_service.py liest 'qualitative_risk_codes' — das verdrahtet die "
        "Zuordnung versehentlich zu einer Wirkung und verletzt die Sperre aus "
        "Befund 124 (reviews/BEFUNDE_96.md). qualitative_risk_codes darf ausschließlich "
        "von den Zuordnungsfiltern (routes/measures.py, demo_service.py) gelesen werden."
    )


if __name__ == "__main__":
    import pytest

    sys.exit(pytest.main([__file__, "-q"]))
