"""Ratchet der Evidenzklasse: belegt vs. begründete Abschätzung (Vorgabe P1).

Jeder Parameter der Registry trägt maschinenlesbar ``evidence_class``
("belegt"/"abgeschaetzt"). Für eine Abschätzung verlangt P1 zusätzlich eine
Herleitung als **Datenfeld** (``evidence_derivation`` mit ``wert``, ``band``,
``sensitivitaet``) — ein Code-Kommentar erfüllt die Vorgabe nicht.

``KNOWN_WITHOUT_DERIVATION`` friert den heutigen Ist-Bestand der Abschätzungen
ohne Herleitung als Ratchet ein:

- kein Parameter außerhalb dieser Menge darf als Abschätzung ohne Herleitung
  stehen (ein NEU hinzugefügter Parameter ohne Quelle und ohne Abschätzungs-
  vermerk fällt genau hierhin und macht den Test rot),
- jeder Eintrag der Menge muss den Mangel noch aufweisen (jede Herleitungs-Batch
  MUSS die Liste hier mitschrumpfen — bis sie leer ist).

Aufruf als Skript listet die offenen IDs (Futter für den Fortsetzungs-Prompt):
    python tests/test_parameter_evidence_class.py --list
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.services import parameter_registry  # noqa: E402

# ── Ratchet-Bestand (gemessene Ausgangslage, wird in Folgetickets abgebaut) ─────
KNOWN_WITHOUT_DERIVATION: set[str] = {
    "impact.floor_height_m",
    "measures.HEAT_ACTION_PLANS.benefit_per_m2_year",
    "measures.HEAT_ACTION_PLANS.capex_fixed",
    "measures.HEAT_ACTION_PLANS.capex_per_m2",
    "measures.HEAT_ACTION_PLANS.capex_per_unit",
    "measures.HEAT_ACTION_PLANS.opex_fixed_year",
    "measures.HEAT_ACTION_PLANS.opex_per_m2_year",
    "measures.HEAT_ACTION_PLANS.opex_per_unit_year",
    "measures.HEAT_ACTION_PLANS.unit_density_per_ha",
    "measures.POLLEN_EARLY_WARNING.benefit_per_m2_year",
    "measures.POLLEN_EARLY_WARNING.capex_fixed",
    "measures.POLLEN_EARLY_WARNING.capex_per_m2",
    "measures.POLLEN_EARLY_WARNING.default_reduction",
    "measures.POLLEN_EARLY_WARNING.opex_fixed_year",
    "measures.POLLEN_EARLY_WARNING.opex_per_m2_year",
    "measures.VULNERABLE_GROUP_PROGRAMS.benefit_per_m2_year",
    "measures.VULNERABLE_GROUP_PROGRAMS.capex_fixed",
    "measures.VULNERABLE_GROUP_PROGRAMS.capex_per_m2",
    "measures.VULNERABLE_GROUP_PROGRAMS.capex_per_unit",
    "measures.VULNERABLE_GROUP_PROGRAMS.opex_fixed_year",
    "measures.VULNERABLE_GROUP_PROGRAMS.opex_per_m2_year",
    "measures.VULNERABLE_GROUP_PROGRAMS.opex_per_unit_year",
    "measures.VULNERABLE_GROUP_PROGRAMS.unit_density_per_ha",
    "model.measure_coverage_saturation",
    "model.risk_threshold",
    "regional.glacier_loss_rate",
    "risks.EXPECTED_ANNUAL_ALLERGY_DAYS.impact.birch_group_share_default",
    "risks.EXPECTED_ANNUAL_MORTALITY.impact.beta_dist_km",
}

VALID_CLASSES = {"belegt", "abgeschaetzt"}
DERIVATION_FIELDS = ("wert", "band", "sensitivitaet")


def _params() -> list[dict]:
    return parameter_registry.catalog_parameters()


def _has_derivation(p: dict) -> bool:
    d = p.get("evidence_derivation")
    if not isinstance(d, dict):
        return False
    return all(str(d.get(f) or "").strip() for f in DERIVATION_FIELDS)


def _estimates_without_derivation() -> set[str]:
    return {
        p["id"] for p in _params()
        if p.get("evidence_class") == "abgeschaetzt" and not _has_derivation(p)
    }


# ── (a) Klasse vorhanden und gültig ─────────────────────────────────────────────

def test_every_parameter_has_valid_evidence_class():
    bad = sorted(
        (p["id"], p.get("evidence_class"))
        for p in _params() if p.get("evidence_class") not in VALID_CLASSES
    )
    assert not bad, f"Parameter ohne gültige evidence_class (belegt/abgeschaetzt): {bad}"


# ── (b) Ratchet: Abschätzung braucht eine Herleitung ────────────────────────────

def test_estimates_outside_ratchet_have_derivation():
    extra = _estimates_without_derivation() - KNOWN_WITHOUT_DERIVATION
    assert not extra, (
        "Abschätzung ohne Herleitung (evidence_derivation mit wert/band/"
        f"sensitivitaet) und nicht im Ratchet-Bestand: {sorted(extra)}"
    )


# ── (c) Ratchet schrumpft ───────────────────────────────────────────────────────

def test_ratchet_shrinks():
    stale = KNOWN_WITHOUT_DERIVATION - _estimates_without_derivation()
    assert not stale, (
        "Bereits belegt oder hergeleitet, bitte aus KNOWN_WITHOUT_DERIVATION "
        f"entfernen (Ratchet festziehen): {sorted(stale)}"
    )


# ── Skript-Modus: offene IDs listen (Fortsetzungs-Prompt) ───────────────────────

if __name__ == "__main__":
    if "--list" in sys.argv:
        open_ids = sorted(_estimates_without_derivation())
        print(f"Abschätzungen ohne Herleitung: {len(open_ids)}")
        for pid in open_ids:
            print(f"  {pid}")
        sys.exit(0)

    import traceback

    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"PASS {t.__name__}")
        except Exception:
            failed += 1
            print(f"FAIL {t.__name__}")
            traceback.print_exc()
    sys.exit(1 if failed else 0)
