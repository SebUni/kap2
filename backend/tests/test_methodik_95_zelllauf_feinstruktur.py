"""#95 — Der Zelllauf rechnet die Wärmeinsel-Feinstruktur σ (Bericht §3.0 Wirkung (d)).

Der Zelllauf ``impact.health.mortality`` mittelt die Mortalität je Zelle über eine Streuung
σ = ``health.SIGMA_K`` (0,58 K) um das Sommermittel der Zelle, Gauß-Hermite mit
``health.GH_PUNKTE`` Punkten — derselbe Weg wie die Rechnung des Ergebnisberichts
(``ergebnisbericht/beispiel.py``). Geprüft wird hier:

1. Eine Zelle mit festem Sommermittel liefert dieselben Fälle (YLL, Todesfälle gesamt, 85+ und
   75–84) wie die ausgeschriebene σ-Rechnung (Gauß-Hermite über ``mortality_punkt``), relative
   Toleranz 1e-9.
2. Die Beispielkommune Warmsen liefert im Ergebnisbericht (``beispiel.rechne_95``) dieselben
   Todesfälle wie der Zelllauf auf den gleichen Zellgruppen.
3. σ steht im Code an genau einer Stelle (``health.py``).
4. Die Feinstruktur hebt den Betrag (die Kurve ist gekrümmt), die Morbidität bleibt ohne sie.

Läuft ohne Datenbank.
"""

from __future__ import annotations

import math
import os
import re
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.data import catalog  # noqa: E402
from app.services.engine import override_context  # noqa: E402
from app.services.engine.impact import health as H  # noqa: E402
from app.services.engine.impact.base import CellContext  # noqa: E402

MORT = "EXPECTED_ANNUAL_MORTALITY"
BANDS_TESTZELLE = {"u65": 700.0, "a65_74": 150.0, "a75_84": 110.0, "a85p": 40.0}
SCHLUESSEL = ("outcome", "deaths", "deaths_a85p", "deaths_a75_84")


def _ctx(temp: float, bundesland: str, hd: float = 10.0, bands: dict | None = None) -> CellContext:
    bands = bands or BANDS_TESTZELLE
    return CellContext(
        ci={"pop": sum(bands.values()), "summer_temp_cell": temp, "pop_age_bands": bands},
        hev={"hazards": {"HEAT_WAVE": hd}, "exposures": {}, "vulnerabilities": {}},
        hev_norm={"hazards": {}, "exposures": {}, "vulnerabilities": {}},
        indices={}, regional={"bundesland": bundesland})


def _sigma_rechnung(risk: dict, temp: float, bundesland: str, **kw) -> dict:
    """Die σ-Rechnung wie in ``beispiel.py`` (vor der Umstellung): Gauß-Hermite über die Punktrechnung."""
    xs, ws = np.polynomial.hermite.hermgauss(H.GH_PUNKTE)
    out = dict.fromkeys(SCHLUESSEL, 0.0)
    for x, w in zip(xs, ws):
        r = H.mortality_punkt(risk, _ctx(temp + math.sqrt(2) * H.SIGMA_K * x, bundesland, **kw))
        for k in SCHLUESSEL:
            out[k] += w * r[k] / math.sqrt(math.pi)
    return out


@pytest.fixture(autouse=True)
def _ohne_overrides():
    override_context.set_overrides({})
    yield
    override_context.set_overrides({})


@pytest.mark.parametrize("temp,land", [
    (18.8, "Niedersachsen"),   # kühle Zelle (Region nord): die Wärmeinsel-Feinstruktur zählt stark
    (19.96, "Berlin"),         # Bevölkerungsmittel Berlin (Region mitte)
    (21.5, "Bayern"),          # warme Zelle (Region sued)
])
def test_zelllauf_gleich_sigma_rechnung(temp, land):
    risk = catalog.RISKS_BY_CODE[MORT]
    soll = _sigma_rechnung(risk, temp, land)
    ist = H.mortality(risk, _ctx(temp, land))
    for k in SCHLUESSEL:
        assert soll[k] > 0.0, k
        assert ist[k] == pytest.approx(soll[k], rel=1e-9), k


def test_feinstruktur_hebt_den_betrag():
    risk = catalog.RISKS_BY_CODE[MORT]
    ohne = H.mortality_punkt(risk, _ctx(18.8, "Niedersachsen"))["outcome"]
    mit = H.mortality(risk, _ctx(18.8, "Niedersachsen"))["outcome"]
    assert mit > ohne


def test_gewichte_der_feinstruktur_summieren_sich_zu_eins():
    assert len(H.feinstruktur_knoten()) == H.GH_PUNKTE
    assert sum(w for _, w in H.feinstruktur_knoten()) == pytest.approx(1.0, rel=1e-12)
    assert sum(w * off for off, w in H.feinstruktur_knoten()) == pytest.approx(0.0, abs=1e-12)
    var = sum(w * off * off for off, w in H.feinstruktur_knoten())
    assert math.sqrt(var) == pytest.approx(H.SIGMA_K, rel=1e-9)


def test_beispielkommune_wie_zelllauf():
    """``beispiel.rechne_95`` (Ergebnisbericht) und der Zelllauf liefern für Warmsen dieselben Todesfälle."""
    from app.services.ergebnisbericht import beispiel

    kommune = beispiel.BEISPIELE["warmsen"]
    bericht = beispiel.rechne_95(kommune)
    gids, cis, klima = beispiel.zellen(kommune.ags)
    gruppen: dict[tuple[float, float], dict[str, float]] = {}
    for gid, ci in zip(gids, cis):
        acc = gruppen.setdefault(klima[gid], dict.fromkeys(beispiel.BANDS, 0.0))
        for b in beispiel.BANDS:
            acc[b] += float(ci["pop_age_bands"][b])
    risk = catalog.RISKS_BY_CODE[MORT]
    override_context.set_overrides({})
    tote = yll = 0.0
    for (t, hd), bands in gruppen.items():
        r = _sigma_rechnung(risk, t, kommune.bundesland, hd=hd, bands=bands)
        tote += r["deaths"]
        yll += r["outcome"]
    assert bericht.todesfaelle == pytest.approx(tote, rel=1e-9)
    assert bericht.yll == pytest.approx(yll, rel=1e-9)


def test_sigma_steht_an_genau_einer_stelle():
    """``SIGMA_K`` wird im Backend-Code nur in ``health.py`` zugewiesen; andere Dateien lesen es von dort."""
    wurzel = os.path.join(os.path.dirname(__file__), "..", "app")
    treffer = []
    for pfad, _, dateien in os.walk(wurzel):
        for name in dateien:
            if not name.endswith(".py"):
                continue
            voll = os.path.join(pfad, name)
            with open(voll, encoding="utf-8") as fh:
                for nr, zeile in enumerate(fh, 1):
                    if re.match(r"\s*(SIGMA_K|GH_PUNKTE)\s*(:[^=]+)?=", zeile):
                        treffer.append((os.path.relpath(voll, wurzel), nr, zeile.strip()))
    assert sorted(t[0] for t in treffer) == [os.path.join("services", "engine", "impact", "health.py")] * 2, treffer
    assert H.SIGMA_K == 0.58


def test_sigma_nicht_als_text_im_backend():
    """Auch der Wert als Text („0,58 K“, „0.58 K“) steht im Backend-Code nur in ``health.py`` — der
    Ergebnisbericht bildet ihn aus ``SIGMA_K`` (``teile._sigma_text``)."""
    wurzel = os.path.join(os.path.dirname(__file__), "..", "app")
    muster = re.compile(r"\b0[.,]58\s*K\b")
    treffer = []
    for pfad, _, dateien in os.walk(wurzel):
        for name in dateien:
            if name.endswith(".py"):
                voll = os.path.join(pfad, name)
                with open(voll, encoding="utf-8") as fh:
                    for nr, zeile in enumerate(fh, 1):
                        if muster.search(zeile):
                            treffer.append((os.path.relpath(voll, wurzel), nr))
    assert {t[0] for t in treffer} <= {os.path.join("services", "engine", "impact", "health.py")}, treffer


def test_bericht_nennt_sigma_aus_dem_code(monkeypatch):
    from app.services.ergebnisbericht import teile

    assert teile._sigma_text() == "0,58 K"
    monkeypatch.setattr(H, "SIGMA_K", 0.7)
    assert teile._sigma_text() == "0,70 K"


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-q"]))
