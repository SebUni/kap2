"""#96 Berlin: Jahresbetrag im Weg des Endpunkts cost-summary (T-1484-cto, Muster T-1429-cto).

Der Endpunkt GET /api/kommune/{id}/cost-summary reicht ``cost.by_risk`` unverändert aus
``risk_engine.aggregate`` weiter (``measure_service.build_cost_summary``). Dieser Test füttert
``aggregate`` mit den gepinnten Zellen aus ``golden96_zellen_11000000.csv.gz`` (Altersbänder je
Zelle nach der Produktlogik aus ``zensus_loader.apply_zensus_to_cell_inputs``, danach vor dem
Aufruf über alle Zellen summiert — Symptomtage und Euro sind linear in der Bevölkerung je Band,
Berlin liegt in einer Region), liest ``["cost"]["by_risk"]`` und prüft, dass genau eine Zeile
kwra_id 96 trägt und ihr ``cost_eur`` auf 1 € mit ``_rechnen(_zellbaender(BERLIN))`` aus dem
Golden-Test übereinstimmt (4,58 Mio. € je Jahr, §3.0, Zelllauf mit Ersatzregel).

Ohne Datenbank, ohne Server. Sichtbar mit ``-s``.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.data import catalog  # noqa: E402
from app.services.engine import override_context  # noqa: E402
from app.services.engine import risk_engine  # noqa: E402
from app.services.engine import impact  # noqa: E402
from app.services.engine.impact.base import CellContext  # noqa: E402
from test_methodik_96_golden_betraege import (  # noqa: E402
    BERLIN, CODE, TOL_MIO, ZELL_EUR_MIO, _rechnen, _zellbaender,
)


def _aggregat_zellen(ags: str) -> tuple[list[dict], float]:
    """Eine einzige Zelle mit den über ganz Berlin summierten Altersbändern (Outcome linear)."""
    override_context.set_overrides({})
    baender = _zellbaender(ags)
    pop = sum(baender.values())
    b = {k: float(v) for k, v in baender.items()}
    b["u65"] = b["u20"] + b["a20_64"]
    ctx = CellContext(
        ci={"pop": pop, "pop_age_bands": b},
        hev={"hazards": {}, "exposures": {}, "vulnerabilities": {}},
        hev_norm={"hazards": {}, "exposures": {}, "vulnerabilities": {}},
        indices={}, regional={"bundesland": "Berlin"})
    outcome = impact.compute_all_cell_impacts(ctx)[CODE]["outcome"]
    zellen = [{"inputs": {"pop": pop}, "risks": {CODE: {"index": 0.0, "outcome": outcome}}}]
    return zellen, pop


def test_berlin_by_risk_96():
    override_context.set_overrides({})
    zellen, pop = _aggregat_zellen(BERLIN)
    by_risk = risk_engine.aggregate(zellen, pop, 891.0)["cost"]["by_risk"]
    zeilen_96 = [e for e in by_risk if e.get("kwra_id") == 96]
    assert len(zeilen_96) == 1, f"{len(zeilen_96)} Zeilen mit kwra_id 96 statt genau einer"
    cost_eur = zeilen_96[0]["cost_eur"]
    _, _, golden = _rechnen(_zellbaender(BERLIN))
    print(f"by_risk Berlin #96 ({zeilen_96[0]['code']}): cost_eur = {cost_eur:,.2f} € "
          f"({cost_eur / 1e6:.2f} Mio. €); Golden = {golden:,.2f} €")
    assert abs(cost_eur - golden) <= 1.0, f"Endpunktweg {cost_eur:.2f} € ≠ Golden {golden:.2f} €"
    assert abs(cost_eur / 1e6 - ZELL_EUR_MIO) < TOL_MIO, f"{cost_eur / 1e6:.4f} Mio. €"
    assert catalog.RISKS_BY_CODE[CODE]["kwra_id"] == 96
