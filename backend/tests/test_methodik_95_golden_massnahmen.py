"""Golden-Test der Maßnahmen #95 (Hitzebelastung, Bericht Endstand Ledger Befund 165, Log 50)
im Zelllauf mit Gemeindeschlüssel, an den gepinnten Zelldaten aus
``test_methodik_95_golden_betraege.py``.

Bindet, nach dem Muster dieser Datei (Import ihrer Zell-Ladefunktion ``_zellen`` und ihrer
Konstanten, unverändert), drei Werte des Berichts ``docs/methodik/95_hitzebelastung.md`` an
den Produktcode, und einen vierten Wert der Kette (kein Zelllauf) aus
``test_massnahme_kuehlzentren_95.py``:

- **S157 (gekühlte Heimplätze) bei der Voreinstellung** ``s_gek = 0,11`` ohne Eingabe der
  Kommune (Bericht §5, Block ``heat.s_gek``, Befund 138): Berlin **1,1 Mio. € je Jahr**,
  Warmsen **475 € je Jahr** (§5 Absatz S157: „Im Zelllauf mit Gemeindeschlüssel 1,1 Mio. €;
  Warmsen (Zelllauf) 475 € je Jahr.").
- **Anpassungspotenzial der Hitzemortalität** mit S157 bei der Voreinstellung und dem
  Hitzeaktionsplan (Bericht §5, Anpassungspotenzial, Befunde 149 und 183): **0,064**, gleich in Berlin
  (a_85+ = 0,262 im Zelllauf) und in Warmsen (a_85+ = 0,224 im Zelllauf), obwohl der Altersaufbau
  unterschiedlich ist — „das Anpassungspotenzial in beiden Kommunen 0,064".
- **Öffentliche Kühlzentren bei der Voreinstellung, in der Kette** (Bericht §5, Block
  ``heat.delta_kuehlzentren``, Befunde 139/148): Berlin **0,75 Mio. € je Jahr**
  („169,5 Mio. € × 0,05 × 0,0883 = 0,75 Mio. €"), gerechnet mit ``_kz_eur`` aus
  ``test_massnahme_kuehlzentren_95.py`` (importiert, nicht geändert; diese Funktion rechnet
  mit einer gepinnten Berlin-Zelle der Kette, nicht mit dem Zelllauf).

Gerechnet wird wie in ``test_methodik_95_golden_betraege.py``: Zellen aus ``_zellen(ags)``
nach Rasterwert (Sommermittel, Hitzetage) gruppiert, Gauß-Hermite mit 21 Punkten und
Feinstruktur σ = 0,58 K je Gruppe auf ``impact.health.mortality`` — hier zusätzlich mit den
Teil-Ausweisen ``deaths_a85p``/``deaths_a75_84`` (Andockpunkte des Hebels S157, Bericht §5).
Aus den Summen über die Kommune bildet ``health.s157_avoided_deaths`` die vermiedene Menge
(Todesfälle); bewertet wird mit ``catalog.risk_default_cost_per_outcome`` (VOLY), wie im
Jahresbetrag der Beträge-Datei. Die Hilfsfunktionen der Beträge-Datei (``_zellen`` und ihre
Konstanten) werden importiert, nicht verändert.

Toleranz (Ticket-Vorgabe T-1618-cto, Abnahmekriterium): Der Bericht nennt für diese Werte
keine eigene Toleranz. Es gilt die größere von zwei Grenzen: der halben letzten Stelle des
Berichtswerts oder der Zelllauf-Toleranz des Berichts von 0,2898 % (§3.3, Befund 140) relativ
zum Berichtswert. Daraus: Berlin S157 ± 0,05 Mio. €, Warmsen S157 ± 1,38 €,
Anpassungspotenzial ± 0,0005, Kühlzentren-Kette ± 5.000 € (halbe letzte Stelle; die
Zelllauf-Toleranz wäre hier nur ± 2.173 €).
"""

from __future__ import annotations

import math
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.data import catalog  # noqa: E402
from app.services import measure_service  # noqa: E402
from app.services.engine import override_context  # noqa: E402
from app.services.engine.impact import health as H  # noqa: E402
from app.services.engine.impact.base import CellContext  # noqa: E402

from test_methodik_95_golden_betraege import (  # noqa: E402
    BANDS, BERLIN, GH_PUNKTE, LAND, MORT, SIGMA_K, WARMSEN, _zellen,
)
from test_massnahme_kuehlzentren_95 import _kz_eur  # noqa: E402

# Zielwerte des Berichts (§5, Zelllauf mit Gemeindeschlüssel bzw. Kette, Preisstand 2024).
S157_BERLIN_EUR, S157_BERLIN_TOL = 1_100_000.0, 50_000.0        # §5 Absatz S157, ± halbe Stelle
S157_WARMSEN_EUR, S157_WARMSEN_TOL = 475.0, 1.38                # §5 Absatz S157, Zelllauf-Toleranz
ANPASSUNG_ZIEL, ANPASSUNG_TOL = 0.064, 0.0005                   # §5 Anpassungspotenzial, ± halbe Stelle
KZ_KETTE_BERLIN_EUR, KZ_KETTE_BERLIN_TOL = 750_000.0, 5_000.0    # §5 Kühlzentren, ± halbe Stelle

# Voreinstellungen des Hebels S157 (Bericht §5, Block heat.s_gek / heat.s_gek_kalib).
S_GEK, S_GEK_KALIB = 0.11, 0.06


def _mortalitaet_summen(ags: str) -> tuple[float, float, float]:
    """YLL gesamt, Todesfälle 85+ und Todesfälle 75–84 im Zelllauf (Gauß-Hermite wie im
    Jahresbetrag der Beträge-Datei), aus den gepinnten Zelldaten dieser Kommune."""
    gids, cis, klima = _zellen(ags)
    gruppen: dict[tuple[float, float], dict[str, float]] = {}
    for gid, ci in zip(gids, cis):
        acc = gruppen.setdefault(klima[gid], dict.fromkeys(BANDS, 0.0))
        for b in BANDS:
            acc[b] += float(ci["pop_age_bands"][b])

    import numpy as np
    xs, ws = np.polynomial.hermite.hermgauss(GH_PUNKTE)
    mort_risk = catalog.RISKS_BY_CODE[MORT]
    regional = {"bundesland": LAND[ags]}
    override_context.set_overrides({})
    yll = deaths_a85p = deaths_a75_84 = 0.0
    for (t, hd), bands in gruppen.items():
        def ctx(temp):
            return CellContext(
                ci={"pop": sum(bands.values()), "summer_temp_cell": temp, "pop_age_bands": bands},
                hev={"hazards": {"HEAT_WAVE": hd}, "exposures": {}, "vulnerabilities": {}},
                hev_norm={"hazards": {}, "exposures": {}, "vulnerabilities": {}},
                indices={}, regional=regional)
        for x, w in zip(xs, ws):
            r = H.mortality(mort_risk, ctx(t + math.sqrt(2) * SIGMA_K * x))
            wgt = w / math.sqrt(math.pi)
            yll += wgt * r["outcome"]
            deaths_a85p += wgt * r["deaths_a85p"]
            deaths_a75_84 += wgt * r["deaths_a75_84"]
    return yll, deaths_a85p, deaths_a75_84


def _voly() -> float:
    """VOLY (€ je YLL) des Risikos, wie im Jahresbetrag der Beträge-Datei."""
    return catalog.risk_default_cost_per_outcome(catalog.RISKS_BY_CODE[MORT])


def _s157_eur(ags: str) -> float:
    """Nutzen des Hebels S157 bei der Voreinstellung, im Zelllauf (Bericht §5 Absatz S157)."""
    _, deaths_a85p, _ = _mortalitaet_summen(ags)
    avoided_deaths = H.s157_avoided_deaths(
        deaths_a85p, S_GEK, s_gek_kalib=S_GEK_KALIB, delta_hap=1.0, q_pfl=None)
    avoided_yll = avoided_deaths * H.AGE_LIFE_YEARS["a85p"]
    return avoided_yll * _voly()


def _hap_delta() -> float:
    """δ_HAP bei voller Deckung, aus der Maßnahmen-Engine (wie in test_massnahme_s157.py)."""
    override_context.set_overrides({})
    hap = catalog.MEASURES_BY_CODE[measure_service.S157_HAP_CODE]
    return measure_service._reduction_factor(hap, 1.0, 1.0)


def _anpassungspotenzial(ags: str) -> float:
    """Anpassungspotenzial der Hitzemortalität mit S157 (Voreinstellung) und Hitzeaktionsplan,
    a_85+ aus dem Zelllauf dieser Kommune (Bericht §5, Anpassungspotenzial, Befunde 149 und 183)."""
    yll, deaths_a85p, _ = _mortalitaet_summen(ags)
    a_85p = (deaths_a85p * H.AGE_LIFE_YEARS["a85p"]) / yll
    r_s157 = a_85p * H.h_heim() * max(S_GEK - S_GEK_KALIB, 0.0) * (1.0 - H.G_S157)
    return 1.0 - _hap_delta() * (1.0 - r_s157)


def test_s157_voreinstellung_berlin_1_1_mio_eur():
    """S157 bei der Voreinstellung s_gek = 0,11, Berlin (Zelllauf): 1,1 Mio. € je Jahr
    (Bericht §5 Absatz S157)."""
    eur = _s157_eur(BERLIN)
    assert abs(eur - S157_BERLIN_EUR) < S157_BERLIN_TOL, f"{eur / 1e6:.2f} Mio. €"


def test_s157_voreinstellung_warmsen_475_eur():
    """S157 bei der Voreinstellung s_gek = 0,11, Warmsen (Zelllauf): 475 € je Jahr
    (Bericht §5 Absatz S157)."""
    eur = _s157_eur(WARMSEN)
    assert abs(eur - S157_WARMSEN_EUR) < S157_WARMSEN_TOL, f"{eur:.2f} €"


def test_anpassungspotenzial_hitzemortalitaet_0_064():
    """Anpassungspotenzial der Hitzemortalität mit S157 (Voreinstellung) und
    Hitzeaktionsplan: 0,064, gleich in Berlin und in Warmsen trotz unterschiedlichem
    Altersaufbau (Bericht §5, Anpassungspotenzial, Befunde 149 und 183)."""
    p_berlin = _anpassungspotenzial(BERLIN)
    p_warmsen = _anpassungspotenzial(WARMSEN)
    assert abs(p_berlin - ANPASSUNG_ZIEL) < ANPASSUNG_TOL, f"{p_berlin:.4f}"
    assert abs(p_warmsen - ANPASSUNG_ZIEL) < ANPASSUNG_TOL, f"{p_warmsen:.4f}"


def test_kuehlzentren_voreinstellung_berlin_kette_0_75_mio_eur():
    """Öffentliche Kühlzentren bei der Voreinstellung, Berlin in der Kette (nicht im
    Zelllauf): 0,75 Mio. € je Jahr (Bericht §5 Kühlzentren: „169,5 Mio. € × 0,05 × 0,0883 =
    0,75 Mio. €")."""
    override_context.set_overrides({})
    eur = _kz_eur()
    assert abs(eur - KZ_KETTE_BERLIN_EUR) < KZ_KETTE_BERLIN_TOL, f"{eur / 1e6:.4f} Mio. €"


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-q"]))
