"""PSS-Watchdog für den Assessment-Kind-Prozessbaum (nur Linux, /proc).

PSS statt RSS: Die Rechenphasen forken Worker über einem großen gemeinsamen
Heap. RSS zählt Copy-on-Write-geteilte Seiten in JEDEM Prozess voll — 8 Worker
über einem 1-GB-Eltern-Heap sähen nach 8 GB aus und der Wächter würde gesunde
Läufe abbrechen. PSS (``/proc/<pid>/smaps_rollup``, Kernel ≥ 4.14) teilt
geteilte Seiten anteilig zu und misst damit den echten Gesamtverbrauch.
Fallback ist VmRSS je Prozess (Überschätzung, nur für sehr alte Kernel).
"""

from __future__ import annotations

import logging
import os
import threading
import time
from typing import Callable

log = logging.getLogger(__name__)


def _read_file(path: str) -> str | None:
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            return fh.read()
    except OSError:
        return None


def _stat_fields_after_comm(proc_root: str, pid: int) -> list[str] | None:
    """Felder von /proc/<pid>/stat ab Feld 3 (state).

    ``comm`` steht in Klammern und darf Leerzeichen und ``)`` enthalten —
    deshalb am LETZTEN ``)`` trennen statt naiv zu splitten.
    """
    raw = _read_file(os.path.join(proc_root, str(pid), "stat"))
    if not raw:
        return None
    try:
        return raw.rsplit(")", 1)[1].split()
    except IndexError:
        return None


def proc_ppid(pid: int, proc_root: str = "/proc") -> int | None:
    fields = _stat_fields_after_comm(proc_root, pid)
    if not fields or len(fields) < 2:
        return None
    try:
        return int(fields[1])  # Feld 4 (ppid); fields[0] = state
    except ValueError:
        return None


def proc_start_ticks(pid: int, proc_root: str = "/proc") -> int | None:
    """Prozess-Startzeit in Kernel-Ticks (Feld 22) — disambiguiert PID-Reuse."""
    fields = _stat_fields_after_comm(proc_root, pid)
    if not fields or len(fields) < 20:
        return None
    try:
        return int(fields[19])  # Feld 22 gesamt = Index 19 nach state
    except ValueError:
        return None


def pid_alive(pid: int | None, start_ticks: int | None, proc_root: str = "/proc") -> bool:
    """True, wenn der Prozess existiert und (falls bekannt) die Startzeit passt."""
    if not pid:
        return False
    ticks = proc_start_ticks(pid, proc_root)
    if ticks is None:
        return False
    if start_ticks is not None and ticks != start_ticks:
        return False  # PID wurde wiederverwendet
    return True


def _tree_pids(root_pid: int, proc_root: str) -> set[int]:
    ppid_map: dict[int, int] = {}
    try:
        entries = os.listdir(proc_root)
    except OSError:
        return {root_pid}
    for name in entries:
        if not name.isdigit():
            continue
        ppid = proc_ppid(int(name), proc_root)
        if ppid is not None:
            ppid_map[int(name)] = ppid
    tree = {root_pid}
    changed = True
    while changed:  # Fork-Hierarchie ist flach; konvergiert in wenigen Runden
        changed = False
        for pid, ppid in ppid_map.items():
            if ppid in tree and pid not in tree:
                tree.add(pid)
                changed = True
    return tree


def _pss_kb(pid: int, proc_root: str) -> int | None:
    raw = _read_file(os.path.join(proc_root, str(pid), "smaps_rollup"))
    if not raw:
        return None
    for line in raw.splitlines():
        if line.startswith("Pss:"):
            try:
                return int(line.split()[1])
            except (IndexError, ValueError):
                return None
    return None


def _rss_kb(pid: int, proc_root: str) -> int:
    raw = _read_file(os.path.join(proc_root, str(pid), "status"))
    if not raw:
        return 0
    for line in raw.splitlines():
        if line.startswith("VmRSS:"):
            try:
                return int(line.split()[1])
            except (IndexError, ValueError):
                return 0
    return 0


def process_tree_pss_mb(root_pid: int, proc_root: str = "/proc") -> float:
    """Summiertes PSS in MB über ``root_pid`` und alle Nachfahren."""
    total_kb = 0
    for pid in _tree_pids(root_pid, proc_root):
        pss = _pss_kb(pid, proc_root)
        total_kb += pss if pss is not None else _rss_kb(pid, proc_root)
    return total_kb / 1024.0


class RssWatchdog(threading.Thread):
    """Daemon-Thread: misst den Prozessbaum und meldet Budget-Überschreitung.

    ``on_breach(mb)`` feuert genau einmal (soll den sanften Abbruch auslösen).
    Bleibt der Verbrauch danach ``escalate_after_s`` Sekunden ununterbrochen
    über dem Limit (z. B. Worker hängt in einem C-Call und erreicht den
    Abbruch-Check nie), feuert einmalig ``on_escalate(mb)``.
    """

    def __init__(
        self,
        root_pid: int,
        limit_mb: float,
        on_breach: Callable[[float], None],
        *,
        interval_s: float = 3.0,
        proc_root: str = "/proc",
        on_escalate: Callable[[float], None] | None = None,
        escalate_after_s: float = 30.0,
    ) -> None:
        super().__init__(daemon=True, name="rss-watchdog")
        self._root_pid = root_pid
        self._limit_mb = float(limit_mb)
        self._on_breach = on_breach
        self._interval_s = max(0.01, float(interval_s))
        self._proc_root = proc_root
        self._on_escalate = on_escalate
        self._escalate_after_s = float(escalate_after_s)
        # Nicht "_stop" nennen: das würde die interne Methode Thread._stop()
        # überschreiben, die CPython in threading._after_fork() aufruft —
        # jeder Fork (cow_pool) spammte dann "Exception ignored: TypeError".
        self._stop_evt = threading.Event()
        self._breach_fired = False
        self._escalated = False
        self._over_since: float | None = None
        self.last_mb: float = 0.0

    def stop(self) -> None:
        self._stop_evt.set()

    def check_once(self, now: float | None = None) -> float:
        """Eine Messung + Auswertung (auch für Tests direkt aufrufbar)."""
        mb = process_tree_pss_mb(self._root_pid, self._proc_root)
        self.last_mb = mb
        now = time.monotonic() if now is None else now
        if mb > self._limit_mb:
            if self._over_since is None:
                self._over_since = now
            if not self._breach_fired:
                self._breach_fired = True
                log.warning(
                    "RAM-Watchdog: %.0f MB > Limit %.0f MB — sanfter Abbruch",
                    mb, self._limit_mb,
                )
                self._safe(self._on_breach, mb)
            elif (
                self._on_escalate is not None
                and not self._escalated
                and now - self._over_since >= self._escalate_after_s
            ):
                self._escalated = True
                log.error(
                    "RAM-Watchdog: weiterhin %.0f MB > Limit %.0f MB nach %.0fs — Eskalation",
                    mb, self._limit_mb, self._escalate_after_s,
                )
                self._safe(self._on_escalate, mb)
        else:
            self._over_since = None
        return mb

    def run(self) -> None:  # pragma: no cover - Thread-Schleife; Logik via check_once getestet
        while not self._stop_evt.wait(self._interval_s):
            try:
                self.check_once()
            except Exception:
                log.exception("RAM-Watchdog-Messung fehlgeschlagen")

    @staticmethod
    def _safe(fn: Callable[[float], None], mb: float) -> None:
        try:
            fn(mb)
        except Exception:
            log.exception("RAM-Watchdog-Callback fehlgeschlagen")
