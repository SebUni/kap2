"""Tests für die gemeinsamen Datei-Cache-Primitiven (Race-Fix, Stempel, tmp-Aufräumen)."""

from __future__ import annotations

import os
import time

from app.services import file_cache


def test_write_read_roundtrip(tmp_path):
    path = str(tmp_path / "sub" / "a.json.gz")
    file_cache.write_gzip_json(path, {"x": 1})
    assert file_cache.read_gzip_json(path) == {"x": 1}


def test_corrupt_file_reads_as_none(tmp_path):
    path = str(tmp_path / "b.json.gz")
    with open(path, "wb") as fh:
        fh.write(b"halb geschrieben, kein gzip")
    assert file_cache.read_gzip_json(path) is None


def test_version_stamp_invalidates_on_change(tmp_path):
    cache_dir = str(tmp_path / "k1")
    file_cache.ensure_version_stamp(cache_dir, "v1")
    file_cache.write_gzip_json(os.path.join(cache_dir, "art.json.gz"), {"a": 1})
    # Gleiche Version: Inhalt bleibt
    file_cache.ensure_version_stamp(cache_dir, "v1")
    assert os.path.exists(os.path.join(cache_dir, "art.json.gz"))
    # Neue Version: Verzeichnis geleert + neu gestempelt
    file_cache.ensure_version_stamp(cache_dir, "v2")
    assert not os.path.exists(os.path.join(cache_dir, "art.json.gz"))
    assert file_cache.read_text(os.path.join(cache_dir, ".model_version")) == "v2"


def test_cleanup_removes_only_stale_tmp(tmp_path):
    cache_dir = str(tmp_path)
    stale = os.path.join(cache_dir, "x.json.gz.tmp.123.456")
    fresh = os.path.join(cache_dir, "y.json.gz.tmp.123.456")
    keep = os.path.join(cache_dir, "z.json.gz")
    for p in (stale, fresh, keep):
        with open(p, "w") as fh:
            fh.write("x")
    old = time.time() - file_cache._TMP_MAX_AGE_S - 10
    os.utime(stale, (old, old))
    file_cache.cleanup_stale_tmp(cache_dir)
    assert not os.path.exists(stale)
    assert os.path.exists(fresh)
    assert os.path.exists(keep)


def test_write_survives_concurrent_dir_removal(tmp_path, monkeypatch):
    """Simuliert invalidate() zwischen makedirs und Write (der Live-Crash)."""
    target_dir = tmp_path / "k7"
    path = str(target_dir / "art.json.gz")

    real_makedirs = os.makedirs
    state = {"sabotaged": False}

    def sabotage(name, exist_ok=False):
        real_makedirs(name, exist_ok=exist_ok)
        if not state["sabotaged"]:
            state["sabotaged"] = True
            # Verzeichnis direkt nach dem Anlegen wieder wegreißen (rmtree-Race)
            import shutil
            shutil.rmtree(target_dir, ignore_errors=True)

    monkeypatch.setattr(file_cache.os, "makedirs", sabotage)
    file_cache.write_gzip_json(path, {"ok": True})  # darf nicht crashen (Retry)
    assert file_cache.read_gzip_json(path) == {"ok": True}
