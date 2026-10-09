"""Toter Rechen-Worker endet als Fehler, nicht als Hänger (T-1953-cto).

Der Deploy e22ff6dc blieb bei 95 % (Risikokomposition) stehen: Stirbt ein Kind von
``multiprocessing.Pool``, wartet ``imap_unordered`` unbegrenzt. Der gemeinsame Rechen-Pool
(``app.services.engine.parallel``) läuft jetzt über ``ProcessPoolExecutor`` und meldet einen
toten Worker als ``RechenWorkerBeendet``. Läuft ohne Datenbank (Sitzung ist eine Attrappe).

Jeder Test hat eine eigene Zeitgrenze (SIGALRM): hängt der Pool, endet der Test als Fehlschlag.
"""
from __future__ import annotations

import os
import signal
import sys
import time
from contextlib import contextmanager
from types import SimpleNamespace

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.services.engine import parallel  # noqa: E402
from app.services.engine.parallel import RechenWorkerBeendet, cow_pool  # noqa: E402

GRENZE_S = 60


@contextmanager
def _zeitgrenze(sekunden: int = GRENZE_S):
    """Bricht den Hauptfaden nach ``sekunden`` ab — ein Hänger wird so zum Fehlschlag."""
    def _abbruch(*_):
        raise TimeoutError(f"Zeitgrenze von {sekunden} s überschritten — der Aufruf hängt")

    alt = signal.signal(signal.SIGALRM, _abbruch)
    signal.alarm(sekunden)
    try:
        yield
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, alt)


def _quadrat(i: int) -> tuple[int, int]:
    return i, i * i


def _stirbt_bei_sieben(i: int) -> tuple[int, int]:
    if i == 7:
        os._exit(1)  # Prozessende ohne Python-Fehler, wie OOM-Killer oder Signal
    time.sleep(0.01)
    return i, i * i


def _wirft_fachfehler(i: int) -> int:
    if i == 3:
        raise ValueError("Fachfehler im Worker")
    return i


def test_gesunder_pool_liefert_alle_ergebnisse():
    with _zeitgrenze():
        with cow_pool(2) as pool:
            ergebnis = dict(pool.map_unordered(_quadrat, range(40), chunksize=5))
    assert ergebnis == {i: i * i for i in range(40)}


def test_worker_mit_os_exit_endet_mit_ausnahme_und_haengt_nicht():
    start = time.monotonic()
    with _zeitgrenze():
        with pytest.raises(RechenWorkerBeendet) as info:
            with cow_pool(2) as pool:
                list(pool.map_unordered(_stirbt_bei_sieben, range(200), chunksize=2))
    assert time.monotonic() - start < GRENZE_S
    meldung = str(info.value)
    assert "Rechen-Worker unerwartet beendet" in meldung
    assert "_stirbt_bei_sieben" in meldung


def test_python_fehler_im_worker_wird_unveraendert_weitergereicht():
    with _zeitgrenze():
        with pytest.raises(ValueError, match="Fachfehler im Worker"):
            with cow_pool(2) as pool:
                list(pool.map_unordered(_wirft_fachfehler, range(10), chunksize=1))


def test_gc_ist_nach_dem_pool_wieder_freigegeben():
    import gc

    with _zeitgrenze():
        with pytest.raises(RechenWorkerBeendet):
            with cow_pool(2) as pool:
                list(pool.map_unordered(_stirbt_bei_sieben, range(50), chunksize=1))
    assert gc.get_freeze_count() == 0


def test_alle_rechenstufen_laufen_ueber_den_gemeinsamen_pool():
    """Keine Stufe baut einen eigenen Prozess-Pool (Quelltext der vier Aufrufstellen)."""
    wurzel = os.path.join(os.path.dirname(__file__), "..", "app")
    stellen = [
        "services/terrain_service.py",
        "services/engine/inputs.py",
        "services/engine/runner.py",
    ]
    for rel in stellen:
        with open(os.path.join(wurzel, rel), encoding="utf-8") as f:
            text = f.read()
        assert "imap_unordered" not in text, rel
        assert "pool.map_unordered(" in text, rel
    assert parallel.ProcessPoolExecutor is not None


# --- Bewertung: Status ``error`` mit Meldung --------------------------------------------------

class _Abfrage:
    def __init__(self, zeilen, skalar=False):
        self._zeilen = zeilen
        self._skalar = skalar

    def filter(self, *_):
        return self

    def first(self):
        return self._zeilen[0] if self._zeilen else None

    def all(self):
        return list(self._zeilen)

    def scalar(self):
        return self._skalar


class _Sitzung:
    """Attrappe: Statuszeile fehlt anfangs, eine Gitterzelle, keine Kommune."""

    def __init__(self, zellen):
        self._zellen = zellen
        self.status_zeile = None
        self.commits = 0
        self.geschlossen = False

    def query(self, modell, *_):
        from app.models.models import GridCell, ProjectStatus

        if modell is ProjectStatus:
            return _Abfrage([self.status_zeile] if self.status_zeile else [])
        if modell is GridCell:
            return _Abfrage(self._zellen)
        return _Abfrage([], skalar=False)

    def add(self, objekt):
        from app.models.models import ProjectStatus

        if isinstance(objekt, ProjectStatus):
            self.status_zeile = objekt

    def commit(self):
        self.commits += 1

    def rollback(self):
        pass

    def refresh(self, *_):
        pass

    def close(self):
        self.geschlossen = True


def test_bewertung_mit_totem_rechen_worker_bekommt_status_error(monkeypatch):
    from geoalchemy2.shape import from_shape
    from shapely.geometry import Polygon

    from app.models.models import AssessmentStatus
    from app.services import parameter_registry
    from app.services.engine import runner
    from app.tasks import assessment_worker

    flaeche = Polygon([(9.2, 52.6), (9.3, 52.6), (9.3, 52.7), (9.2, 52.7)])
    zelle = SimpleNamespace(
        id=1, gitter_id="g1", x_3035=4000000, y_3035=3000000, row_idx=1, col_idx=1,
        cell_size_m=100, geometry=from_shape(flaeche, srid=4326), kommune_id=1,
    )
    sitzung = _Sitzung([zelle])

    monkeypatch.setattr("app.db.database.SessionLocal", lambda: sitzung)
    monkeypatch.setattr(parameter_registry, "load_db_overrides", lambda *_a, **_k: [])
    # Eingabestufe überspringen; die Risikokomposition (Rechenstufe) bekommt 200 Zellen
    # und einen Worker, der bei Zelle 7 mit os._exit(1) endet.
    monkeypatch.setattr(runner, "gather_cell_inputs",
                        lambda *a, **k: ([{"i": i} for i in range(200)], {}))
    monkeypatch.setattr(runner, "_risk_worker", _stirbt_bei_sieben)
    monkeypatch.setattr(runner, "_CHUNK", 2)
    monkeypatch.setattr(parallel, "n_workers", lambda: 2)
    monkeypatch.setattr(runner, "n_workers", lambda: 2)

    alt = signal.getsignal(signal.SIGTERM)
    try:
        with _zeitgrenze():
            exit_code = assessment_worker.worker_main(1)
    finally:
        signal.signal(signal.SIGTERM, alt)

    status = sitzung.status_zeile
    assert exit_code == assessment_worker.EXIT_FAILED
    assert status.status == AssessmentStatus.ERROR
    assert "Rechen-Worker unerwartet beendet" in status.message
    assert status.message.startswith("Fehler: ")
    assert status.finished_at is not None
    assert status.worker_pid is None
    assert sitzung.geschlossen
