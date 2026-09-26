"""#95 Berlin: Jahresbetrag im Weg des Endpunkts cost-summary (T-1429-cto, Ersatz für T-1372-cto).

Der Endpunkt GET /api/kommune/{id}/cost-summary reicht ``cost.by_risk`` unverändert aus
``risk_engine.aggregate`` weiter (``measure_service.build_cost_summary``). Dieser Test füttert
``aggregate`` mit den gepinnten Zellen aus ``golden95_zellen_11000000.csv.gz`` (Zellen nach Rasterwert
zusammengefasst; Mortalität und Morbidität sind linear in der Bevölkerung je Band), liest
``["cost"]["by_risk"]`` und prüft die Summe von EXPECTED_ANNUAL_MORTALITY und EXPECTED_ANNUAL_MORBIDITY

(i) gegen ``_jahresbetrag("11000000")`` des Golden-Tests (auf 1 € genau),
(ii) gegen 342,67 Mio. € aus Bericht §3.0 (± 1 Mio. €).

Ohne Datenbank, ohne Server. Sichtbar mit ``-s``.
"""

from __future__ import annotations

import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import numpy as np  # noqa: E402

from app.data import catalog  # noqa: E402
from app.services.engine import override_context  # noqa: E402
from app.services.engine import risk_engine  # noqa: E402
from app.services.engine.impact import health as H  # noqa: E402
from app.services.engine.impact.base import CellContext  # noqa: E402
from test_methodik_95_golden_betraege import (  # noqa: E402
    BANDS, BERLIN, BERLIN_EUR, BERLIN_TOL, GH_PUNKTE, LAND, MORB, MORT, SIGMA_K,
    _jahresbetrag, _zellen,
)


def _aggregat_zellen(ags: str) -> tuple[list[dict], float]:
    """Je Rasterwert-Gruppe eine Zelle für ``aggregate`` (Outcome = YLL bzw. Fälle der Gruppe)."""
    gids, cis, klima = _zellen(ags)
    gruppen: dict[tuple[float, float], dict[str, float]] = {}
    for gid, ci in zip(gids, cis):
        acc = gruppen.setdefault(klima[gid], dict.fromkeys(BANDS, 0.0))
        for b in BANDS:
            acc[b] += float(ci["pop_age_bands"][b])
    xs, ws = np.polynomial.hermite.hermgauss(GH_PUNKTE)
    mort_risk, morb_risk = catalog.RISKS_BY_CODE[MORT], catalog.RISKS_BY_CODE[MORB]
    regional = {"bundesland": LAND[ags]}
    zellen, gesamt_pop = [], 0.0
    for (t, hd), bands in gruppen.items():
        pop = sum(bands.values())

        def ctx(temp):
            return CellContext(
                ci={"pop": pop, "summer_temp_cell": temp, "pop_age_bands": bands},
                hev={"hazards": {"HEAT_WAVE": hd}, "exposures": {}, "vulnerabilities": {}},
                hev_norm={"hazards": {}, "exposures": {}, "vulnerabilities": {}},
                indices={}, regional=regional)

        yll = sum(w * H.mortality(mort_risk, ctx(t + math.sqrt(2) * SIGMA_K * x))["outcome"]
                  for x, w in zip(xs, ws)) / math.sqrt(math.pi)
        faelle = H.morbidity(morb_risk, ctx(t))["outcome"]
        zellen.append({"inputs": {"pop": pop},
                       "risks": {MORT: {"index": 0.0, "outcome": yll},
                                 MORB: {"index": 0.0, "outcome": faelle}}})
        gesamt_pop += pop
    return zellen, gesamt_pop


def test_berlin_by_risk_95():
    override_context.set_overrides({})
    zellen, pop = _aggregat_zellen(BERLIN)
    by_risk = risk_engine.aggregate(zellen, pop, 891.0)["cost"]["by_risk"]
    zeilen = {e["code"]: e for e in by_risk}
    mort, morb = zeilen[MORT]["cost_eur"], zeilen[MORB]["cost_eur"]
    summe = mort + morb
    print(f"by_risk Berlin #95: {MORT} cost_eur = {mort:,.2f} €; "
          f"{MORB} cost_eur = {morb:,.2f} €; Summe = {summe:,.2f} € ({summe / 1e6:.2f} Mio. €)")
    golden = _jahresbetrag(BERLIN)
    assert abs(summe - golden) <= 1.0, f"Endpunktweg {summe:.2f} € ≠ Golden {golden:.2f} €"
    assert abs(summe - BERLIN_EUR) <= BERLIN_TOL, f"{summe / 1e6:.2f} Mio. €"
