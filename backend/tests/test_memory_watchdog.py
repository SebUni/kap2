"""Tests für den PSS-Prozessbaum-Watchdog (Fake-/proc, kein echtes System)."""

from __future__ import annotations

import os

from app.tasks.memory_watchdog import (
    RssWatchdog, pid_alive, proc_start_ticks, process_tree_pss_mb,
)


def _mk_proc(proc_root, pid: int, ppid: int, *, start_ticks: int = 100,
             pss_kb: int | None = None, rss_kb: int | None = None,
             comm: str = "python3") -> None:
    d = proc_root / str(pid)
    d.mkdir()
    # /proc/<pid>/stat: comm in Klammern (darf ')' enthalten!), danach
    # state ppid pgrp session tty tpgid flags 6×flt 4×time prio nice threads
    # itreal starttime  → starttime ist Feld 22 (Index 19 nach state).
    tail = f"S {ppid} 0 0 0 0 0 0 0 0 0 0 0 0 0 20 0 1 0 {start_ticks} 0"
    (d / "stat").write_text(f"{pid} ({comm}) {tail}")
    if pss_kb is not None:
        (d / "smaps_rollup").write_text(
            f"00000000-ffffffff ---p 00000000 00:00 0    [rollup]\nPss:  {pss_kb} kB\n"
        )
    if rss_kb is not None:
        (d / "status").write_text(f"Name:\t{comm}\nVmRSS:\t    {rss_kb} kB\n")


def test_tree_pss_sums_root_and_descendants(tmp_path):
    _mk_proc(tmp_path, 100, 1, pss_kb=1024)
    _mk_proc(tmp_path, 101, 100, pss_kb=512)
    _mk_proc(tmp_path, 102, 101, pss_kb=512)   # Enkel
    _mk_proc(tmp_path, 999, 1, pss_kb=99999)   # fremder Prozess: zählt nicht
    mb = process_tree_pss_mb(100, proc_root=str(tmp_path))
    assert abs(mb - 2.0) < 0.01


def test_tree_falls_back_to_rss_without_smaps_rollup(tmp_path):
    _mk_proc(tmp_path, 200, 1, rss_kb=2048)
    mb = process_tree_pss_mb(200, proc_root=str(tmp_path))
    assert abs(mb - 2.0) < 0.01


def test_comm_with_parenthesis_and_spaces(tmp_path):
    _mk_proc(tmp_path, 300, 7, start_ticks=4242, comm="weird) (name")
    assert proc_start_ticks(300, proc_root=str(tmp_path)) == 4242


def test_pid_alive_checks_start_ticks(tmp_path):
    _mk_proc(tmp_path, 400, 1, start_ticks=1111)
    assert pid_alive(400, 1111, proc_root=str(tmp_path)) is True
    assert pid_alive(400, 2222, proc_root=str(tmp_path)) is False  # PID-Reuse
    assert pid_alive(401, 1111, proc_root=str(tmp_path)) is False  # existiert nicht
    assert pid_alive(None, 1111, proc_root=str(tmp_path)) is False
    assert pid_alive(400, None, proc_root=str(tmp_path)) is True   # Ticks unbekannt


def test_watchdog_breach_fires_exactly_once(tmp_path):
    _mk_proc(tmp_path, 500, 1, pss_kb=3 * 1024)  # 3 MB
    breaches: list[float] = []
    wd = RssWatchdog(500, limit_mb=2.0, on_breach=breaches.append,
                     proc_root=str(tmp_path))
    wd.check_once(now=0.0)
    wd.check_once(now=1.0)
    wd.check_once(now=2.0)
    assert len(breaches) == 1
    assert breaches[0] > 2.0


def test_watchdog_below_limit_never_fires(tmp_path):
    _mk_proc(tmp_path, 600, 1, pss_kb=1024)
    breaches: list[float] = []
    wd = RssWatchdog(600, limit_mb=2.0, on_breach=breaches.append,
                     proc_root=str(tmp_path))
    for t in range(5):
        wd.check_once(now=float(t))
    assert breaches == []


def test_watchdog_escalates_when_still_over_limit(tmp_path):
    _mk_proc(tmp_path, 700, 1, pss_kb=3 * 1024)
    breaches: list[float] = []
    escalations: list[float] = []
    wd = RssWatchdog(700, limit_mb=2.0, on_breach=breaches.append,
                     on_escalate=escalations.append, escalate_after_s=30.0,
                     proc_root=str(tmp_path))
    wd.check_once(now=0.0)     # Breach
    wd.check_once(now=10.0)    # noch keine Eskalation
    assert escalations == []
    wd.check_once(now=31.0)    # > escalate_after_s ununterbrochen drüber
    wd.check_once(now=40.0)    # Eskalation feuert nur einmal
    assert len(breaches) == 1
    assert len(escalations) == 1


def test_watchdog_callback_errors_are_swallowed(tmp_path):
    _mk_proc(tmp_path, 800, 1, pss_kb=3 * 1024)

    def boom(_mb: float) -> None:
        raise RuntimeError("callback kaputt")

    wd = RssWatchdog(800, limit_mb=2.0, on_breach=boom, proc_root=str(tmp_path))
    wd.check_once(now=0.0)  # darf nicht raisen
