"""Euro je Zelle ungerundet (T-1804-cto, Mangel 2 der Schlussprüfung T-1773).

Vorgabe des CEO: Die Summe der Zell-Euro ist über die ungerundeten Zellwerte an den
Kommunenbetrag gebunden; gerundet wird nur in der Anzeige. Der Test fährt je Maßnahme
(Frühwarnung #96 S158, Stadtbaumwahl) 1.200 Zellen und prüft: Summe der gespeicherten
Zellwerte = ``cost_from_outcome`` der Summe der (ungerundeten) vermiedenen Tage, auf
± 0,01 €. Die Zellwerte sind so gewählt, dass eine Rundung auf 0,01 € je Zelle die
Summe um mehr als 0,01 € verschöbe (im Test selbst nachgewiesen).
"""

from __future__ import annotations

import pytest

from app.data import catalog
from app.services import measure_service

from test_massnahme_s158_ausgabe import CODE as S158_CODE
from test_massnahme_s158_ausgabe import RISK, _cell, _run
from test_massnahme_stadtbaum_ausgabe import ANTEIL_ERSETZT, _allee_cell, _run_cells

N_ZELLEN = 1200


def _erwartet_und_gerundet(tage_je_zelle: list[float]) -> tuple[float, float]:
    risk = catalog.RISKS_BY_CODE[RISK]
    erwartet = measure_service.risk_engine.cost_from_outcome(risk, sum(tage_je_zelle))
    gerundet = sum(round(measure_service.risk_engine.cost_from_outcome(risk, t), 2)
                   for t in tage_je_zelle)
    return erwartet, gerundet


def test_fruehwarnung_summe_zell_euro_gleich_kommunenbetrag(monkeypatch):
    # Betroffene 100,3 + Variation: Euro je Zelle liegen nie auf einem Cent-Wert.
    cells = {cid: _cell(betroffene=100.3 + 0.0007 * cid, delta_birke=0.5, delta_graeser=0.5)
             for cid in range(1, N_ZELLEN + 1)}
    frac_map = {cid: 1.0 for cid in cells}

    tage_je_zelle: dict[int, float] = {}
    original = measure_service._s158_cell_effect

    def _spy(*a, **k):
        res = original(*a, **k)
        if res[1] is not None:
            tage_je_zelle[id(a[2])] = res[1]  # a[2] = Zelldaten; Mehrfachaufruf je Zelle
        return res

    monkeypatch.setattr(measure_service, "_s158_cell_effect", _spy)
    summary, added = _run(cells, frac_map, monkeypatch)

    tage = list(tage_je_zelle.values())
    assert len(tage) == N_ZELLEN
    erwartet, gerundet = _erwartet_und_gerundet(tage)
    assert abs(gerundet - erwartet) > 0.01  # Rundung je Zelle würde die Summe verschieben

    summe = sum((o.savings or {})["s158_avoided_eur"] for o in added)
    assert len([o for o in added if "s158_avoided_eur" in (o.savings or {})]) == N_ZELLEN
    assert summe == pytest.approx(erwartet, abs=0.01)
    assert summe == pytest.approx(summary["s158_avoided_days_eur"], abs=0.01)


def test_stadtbaumwahl_summe_zell_euro_gleich_kommunenbetrag(monkeypatch):
    cells = {}
    for cid in range(1, N_ZELLEN + 1):
        zelle = _allee_cell()
        zelle["betroffene"] = 100.07  # Euro je Zelle ≈ 88,163: Rundung verliert je Zelle ≈ 0,003 €
        cells[cid] = zelle

    tage_je_zelle: dict[int, float] = {}
    original = measure_service._stadtbaum_cell_effect

    def _spy(*a, **k):
        res = original(*a, **k)
        if res[1] is not None:
            tage_je_zelle[id(a[2])] = res[1]  # a[2] = Zelldaten; Mehrfachaufruf je Zelle
        return res

    monkeypatch.setattr(measure_service, "_stadtbaum_cell_effect", _spy)
    _, added = _run_cells(cells, {"anteil_ersetzt": ANTEIL_ERSETZT}, monkeypatch)

    tage = list(tage_je_zelle.values())
    assert len(tage) == N_ZELLEN
    erwartet, gerundet = _erwartet_und_gerundet(tage)
    assert abs(gerundet - erwartet) > 0.01

    summe = sum((o.savings or {})["stadtbaum_avoided_eur"] for o in added)
    assert len([o for o in added if "stadtbaum_avoided_eur" in (o.savings or {})]) == N_ZELLEN
    assert summe == pytest.approx(erwartet, abs=0.01)


if __name__ == "__main__":
    import sys

    sys.exit(pytest.main([__file__, "-q"]))
