"""Tests für die Schema-Version des Aggregat-Caches (T-1532-ceo).

Ein Aggregat, das unter einem alten Stempel (nur ``MODEL_VERSION``, ohne
``AGG_SCHEMA_VERSION``) gespeichert wurde, darf nach einer Strukturänderung
(T-1470-cto: neues Feld ``klimawirkungen`` in ``cost``) nicht mehr ausgeliefert
werden.
"""

from __future__ import annotations

import os

from app.data import catalog
from app.services import aggregate_cache, file_cache


def test_old_stamp_is_discarded_and_load_returns_none(tmp_path, monkeypatch):
    monkeypatch.setattr(aggregate_cache, "_CACHE_BASE", str(tmp_path))

    kommune_id = 1
    cache_dir = aggregate_cache._cache_dir(kommune_id)
    agg_path = aggregate_cache._agg_path(kommune_id, apply_measures=False)

    # Alten Zustand simulieren: nur MODEL_VERSION als Stempel, kein AGG_SCHEMA_VERSION.
    os.makedirs(cache_dir, exist_ok=True)
    file_cache.write_text(os.path.join(cache_dir, ".model_version"), catalog.MODEL_VERSION)
    file_cache.write_gzip_json(agg_path, {"risks": {}, "cost": {}})
    assert os.path.exists(agg_path)

    result = aggregate_cache.load(kommune_id, apply_measures=False)

    assert result is None
    assert not os.path.exists(agg_path)


def test_new_stamp_survives_and_load_returns_result(tmp_path, monkeypatch):
    monkeypatch.setattr(aggregate_cache, "_CACHE_BASE", str(tmp_path))

    kommune_id = 2
    payload = {"risks": {}, "cost": {"klimawirkungen": 42.0}}
    aggregate_cache.store(kommune_id, apply_measures=False, result=payload)

    assert aggregate_cache.load(kommune_id, apply_measures=False) == payload
