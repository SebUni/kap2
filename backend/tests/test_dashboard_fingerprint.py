"""Tests für den Dashboard-Artefakt-Fingerprint (reine Hash-Funktion)."""

from __future__ import annotations

import copy

from app.services import dashboard_cache
from app.services.dashboard_cache import ARTIFACTS, _WEEKLY_ARTIFACTS, etag_for, fingerprint_hash


def _payload() -> dict:
    return {
        "model_version": "2026.07-x",
        "cells": ["2026-07-06 12:00:00", 31234],
        "measures": [
            (1, "gruendach", '{"count": 5}', 2027),
            (2, "baumpflanzung", "{}", None),
        ],
        "params": [("heat.cost_per_outcome", "42.0"), ("model.ref_hitzetote", "1.5")],
        "kommune": [601866, 297.8, "Sachsen", None, "62649"],
    }


def test_hash_is_stable():
    assert fingerprint_hash(_payload()) == fingerprint_hash(copy.deepcopy(_payload()))


def test_hash_changes_on_measure_config():
    p = _payload()
    p["measures"][0] = (1, "gruendach", '{"count": 6}', 2027)
    assert fingerprint_hash(p) != fingerprint_hash(_payload())


def test_hash_changes_on_param_override():
    p = _payload()
    p["params"][0] = ("heat.cost_per_outcome", "99.0")
    assert fingerprint_hash(p) != fingerprint_hash(_payload())


def test_hash_changes_on_population_and_model_version():
    p = _payload()
    p["kommune"][0] = 601867
    assert fingerprint_hash(p) != fingerprint_hash(_payload())
    q = _payload()
    q["model_version"] = "2026.08-y"
    assert fingerprint_hash(q) != fingerprint_hash(_payload())


def test_hash_changes_on_cells_marker():
    p = _payload()
    p["cells"] = ["2026-07-07 08:00:00", 31234]
    assert fingerprint_hash(p) != fingerprint_hash(_payload())


def test_weekly_extra_changes_hash():
    base = fingerprint_hash(_payload(), None)
    weekly = fingerprint_hash(_payload(), "week:2026-28")
    assert base != weekly
    assert fingerprint_hash(_payload(), "week:2026-28") == weekly


def test_etag_format_and_artifact_names():
    assert etag_for("abc123") == '"da-abc123"'
    assert set(_WEEKLY_ARTIFACTS) <= set(ARTIFACTS)
    assert "risk_histogram" in ARTIFACTS and "profile" in ARTIFACTS


def test_summary_schema_version_erzwingt_rebuild(tmp_path, monkeypatch):
    """Eine Erhöhung von ``_SUMMARY_SCHEMA_VERSION`` muss ``risk_summary`` und
    ``cost_summary`` neu bauen, weil sich der Fingerprint ändert (alter
    Cache-Eintrag sonst gültig bliebe, obwohl sich der Payload-Aufbau geändert
    hat)."""
    monkeypatch.setattr(dashboard_cache, "_CACHE_BASE", str(tmp_path))
    monkeypatch.setattr(dashboard_cache, "fingerprint_payload", lambda db, kommune_id: {"x": 1})

    for name in ("risk_summary", "cost_summary"):
        calls = {"n": 0}

        def _fake_build(db, kommune_id, artefakt_name, calls=calls):
            calls["n"] += 1
            return {"n": calls["n"]}

        monkeypatch.setattr(dashboard_cache, "_build", _fake_build)

        dashboard_cache.artifact_file(None, 1, name)
        assert calls["n"] == 1

        # Gleicher Fingerprint (keine Schema-Erhöhung) → kein zweiter Build.
        dashboard_cache.artifact_file(None, 1, name)
        assert calls["n"] == 1

        # Schema-Version erhöht → neuer Fingerprint → genau ein weiterer Build.
        monkeypatch.setattr(
            dashboard_cache, "_SUMMARY_SCHEMA_VERSION",
            dashboard_cache._SUMMARY_SCHEMA_VERSION + 1,
        )
        dashboard_cache.artifact_file(None, 1, name)
        assert calls["n"] == 2
