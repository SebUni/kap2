"""Tests der Roadmap-Stufen + geplanten (gesperrten) Klimawirkungen (M0, docs/ROADMAP.md §5).

Deckt ab:
  (a) Vollständigkeit: genau 51 geplante KWRA-Klimawirkungen in catalog.PLANNED_RISKS.
  (b) 1:1-Klammer: kwra_ids über RISKS + PLANNED_RISKS = 52 eindeutige IDs
      (Nr. 95 aktiv, 51 geplant, keine Kollision aktiv ⇄ geplant).
  (c) Jede Stufe existiert in STAGE_LABELS (öffentliche Verfügbarkeits-Labels).
  (d) planned_available_from liefert das Stufen-Label (Stage 1 → "Herbst 2026").
  (e) Jeder Eintrag ist vollständig: Name, Cluster, KWRA-Handlungsfeld und
      mindestens eine nichtleere Treiberliste (hazard_names/upstream_names)
      aus dem KWRA-Schadensbaum-Digitalisat.
  (f) #96/#98 (Aeroallergene, UV) tragen Stage 0 — sie gehören zum Sommer-Release
      und wechseln nach der Methodik-Freigabe von PLANNED_RISKS in RISKS.

Läuft mit pytest oder direkt: ``python tests/test_planned_risks.py``.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.data import catalog  # noqa: E402

_CLUSTERS = {"land", "wasser", "infrastruktur", "wirtschaft", "gesundheit"}


# ── (a) Vollständigkeit ────────────────────────────────────────────────────────

def test_planned_risks_count_is_51():
    assert len(catalog.PLANNED_RISKS) == 51


# ── (b) 1:1-Klammer aktiv + geplant = 52 eindeutige KWRA-IDs ───────────────────

def test_kwra_ids_are_52_unique_without_collision():
    active_ids = {r["kwra_id"] for r in catalog.RISKS}
    planned_ids = [p["kwra_id"] for p in catalog.PLANNED_RISKS]
    # aktive Klammer: beide Teil-Ausweise (Mortalität/Morbidität) tragen die #95.
    assert active_ids == {95}
    # geplant: 51 eindeutige IDs, keine davon kollidiert mit der aktiven #95.
    assert len(planned_ids) == len(set(planned_ids)) == 51
    assert 95 not in planned_ids
    assert len(active_ids | set(planned_ids)) == 52
    # Index-Map deckt exakt die geplanten IDs ab.
    assert set(catalog.PLANNED_BY_KWRA_ID) == set(planned_ids)


# ── (c) Stufen sind gelabelt ───────────────────────────────────────────────────

def test_every_stage_has_public_label():
    for p in catalog.PLANNED_RISKS:
        assert p["stage"] in catalog.STAGE_LABELS, (p["kwra_id"], p["stage"])
    for r in catalog.RISKS:
        assert r["stage"] in catalog.STAGE_LABELS, (r["code"], r["stage"])


# ── (d) Verfügbarkeits-Label ───────────────────────────────────────────────────

def test_planned_available_from_returns_stage_label():
    stage1 = next(p for p in catalog.PLANNED_RISKS if p["stage"] == 1)
    assert catalog.planned_available_from(stage1) == "Herbst 2026"
    for p in catalog.PLANNED_RISKS:
        assert catalog.planned_available_from(p) == catalog.STAGE_LABELS[p["stage"]]


# ── (e) Eintrags-Vollständigkeit (Schadensbaum-Digitalisat) ────────────────────

def test_every_planned_entry_is_complete():
    problems: list[str] = []
    for p in catalog.PLANNED_RISKS:
        kid = p.get("kwra_id")
        if not (p.get("name") or "").strip():
            problems.append(f"#{kid}: leerer name")
        if p.get("cluster") not in _CLUSTERS:
            problems.append(f"#{kid}: unbekanntes cluster {p.get('cluster')!r}")
        if not (p.get("kwra_field") or "").strip():
            problems.append(f"#{kid}: leeres kwra_field")
        drivers = [n for n in (p.get("hazard_names") or []) if str(n).strip()]
        drivers += [n for n in (p.get("upstream_names") or []) if str(n).strip()]
        if not drivers:
            problems.append(f"#{kid}: weder hazard_names noch upstream_names gefüllt")
    assert not problems, "Unvollständige PLANNED_RISKS-Einträge:\n  " + "\n  ".join(problems)


# ── (f) #96/#98 gehören zum Sommer-Release (Stage 0) ───────────────────────────

def test_kwra_96_and_98_are_stage_0():
    for kid in (96, 98):
        p = catalog.PLANNED_BY_KWRA_ID[kid]
        assert p["stage"] == 0, (kid, p["stage"])
        assert catalog.planned_available_from(p) == catalog.STAGE_LABELS[0]


if __name__ == "__main__":
    import sys

    import pytest

    sys.exit(pytest.main([__file__, "-q"]))
