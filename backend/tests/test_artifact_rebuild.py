"""Tests für Debounce/Coalescing des Artefakt-Rebuild-Orchestrators."""

from __future__ import annotations

import time

import pytest

from app.services import artifact_rebuild as ar


@pytest.fixture(autouse=True)
def isolate(monkeypatch):
    # Kein echter Worker-Thread/Kind-Prozess in Tests
    monkeypatch.setattr(ar, "ensure_worker_started", lambda: None)
    with ar._lock:
        ar._pending.clear()
    yield
    with ar._lock:
        ar._pending.clear()


def _due_now() -> float:
    return time.monotonic() + ar.DEBOUNCE_S + 1.0


def test_schedule_coalesces_multiple_requests():
    ar.schedule(7, artifacts=["profile"])
    ar.schedule(7, artifacts=["cost_summary"])
    due = ar.pop_due(_due_now())
    assert len(due) == 1
    kid, entry = due[0]
    assert kid == 7
    assert entry["artifacts"] == {"profile", "cost_summary"}
    assert entry["layers"] is False


def test_layers_flag_is_sticky():
    ar.schedule(7, layers=True)
    ar.schedule(7, layers=False)
    [(_, entry)] = ar.pop_due(_due_now())
    assert entry["layers"] is True


def test_artifacts_none_means_all_and_stays_all():
    ar.schedule(7, artifacts=["profile"])
    ar.schedule(7, artifacts=None)          # None = alle
    ar.schedule(7, artifacts=["cost_summary"])
    [(_, entry)] = ar.pop_due(_due_now())
    assert entry["artifacts"] is None


def test_debounce_window_holds_entries_back():
    ar.schedule(7)
    assert ar.pop_due(time.monotonic()) == []          # Fenster läuft noch
    assert len(ar.pop_due(_due_now())) == 1            # abgelaufen → fällig
    assert ar.pop_due(_due_now()) == []                # entnommen


def test_distinct_kommunen_are_independent():
    ar.schedule(1, layers=True)
    ar.schedule(2)
    due = dict(ar.pop_due(_due_now()))
    assert set(due.keys()) == {1, 2}
    assert due[1]["layers"] is True
    assert due[2]["layers"] is False
