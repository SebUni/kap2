"""#98 S155: Eingabe „Jahre seit Beginn“ J an der Maßnahme (T-1938-cto, Befund 503, Vorhaben T-1662-ceo).

Der Bericht #98 §5 (Parametertabelle, Zeile J; Integrationsauflage Punkt 3) verlangt J als Eingabe: Nach J Jahren
wird der Anteil min(1, J/a_erk) angerechnet, ohne Eingabe zeigt das Produkt die volle Wirkung und die Anteile nach
10, 20 und 30 Jahren. Die Eingabe ist das Feld ``jahre_seit_beginn`` der Maßnahmenkonfiguration von
``UV_PROTECTION_PUBLIC_SPACE``. Dieser Test misst für Berlin (Zelle des Golden-Tests) ohne Datenbank:

(a) J = 10, 20 und 30: ``s155_angerechnet_eur`` ist auf 1 € gleich dem Eintrag ``eur`` derselben J in ``s155_rampe``
    und, auf Hunderter gerundet, 34.700, 69.400 und 104.000 €;
(b) mit Eingabe ist der Nutzen der Maßnahme (``Zellkosten · (1 − Faktor)``, dasselbe Feld wie in
    ``test_methodik_98_s155_aggregat.py``) auf 1 € gleich ``s155_angerechnet_eur``;
(c) ohne Eingabe fehlt ``s155_angerechnet_eur`` (oder ist None), ``s155_avoided_eur`` bleibt 252.500 € ± 50;
(d) eine negative oder nicht numerische Eingabe weist die Konfigurationsprüfung mit Fehlermeldung ab.

Ohne Datenbank, sichtbar mit ``-s``.
"""

from __future__ import annotations

import os
import sys
from importlib import import_module

import pytest
from pydantic import ValidationError

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.data import catalog  # noqa: E402
from app.schemas.schemas import MeasureCreate, MeasureUpdate  # noqa: E402
from app.services import measure_service as ms  # noqa: E402

_b98 = import_module("test_methodik_98_golden_betraege")
_ep98 = import_module("test_methodik_98_endpunkt_berlin")

CODE = "UV_PROTECTION_PUBLIC_SPACE"
FELD = "jahre_seit_beginn"
HUNDERTER = {10: 34_700, 20: 69_400, 30: 104_000}


def _berlin():
    eintrag, pop = _ep98._gespeicherte_zelle()
    mdef = catalog.MEASURES_BY_CODE[CODE]
    _, eur, fehlt = ms._s155_cell_effect(mdef, 1.0, eintrag)
    assert fehlt is False and eur is not None
    return mdef, eintrag, pop, eur


def _summary(config: dict | None) -> dict:
    mdef, _, _, eur = _berlin()
    return ms._s155_summary_fields(mdef, eur[0], eur[1], False, config)


def _nutzen(config: dict | None) -> float:
    """``annual_benefit_damage_eur`` der Berliner Zelle (Zellschleife von ``measure_service``)."""
    mdef, eintrag, pop, _ = _berlin()
    risk = catalog.RISKS_BY_CODE[_b98.CODE]
    r = ms._with_cell_q_pfl(eintrag, {"pop": pop})
    faktor = ms._measure_cell_factor(mdef, config, _b98.CODE, 1.0, 1.0, r)
    return ms._cell_cost(risk, r, pop) * (1.0 - faktor)


def test_katalog_fuehrt_das_feld():
    mdef = catalog.MEASURES_BY_CODE[CODE]
    assert FELD in mdef["config_inputs"]
    assert mdef["config_inputs"][FELD]["einheit"] == "Jahre"
    assert FELD in mdef["config_input_help"]


@pytest.mark.parametrize("j", [10, 20, 30])
def test_angerechnet_gleich_rampe_und_hunderter(j):
    s = _summary({FELD: j})
    rampe = {e["jahre"]: e["eur"] for e in s["s155_rampe"]}
    angerechnet = s["s155_angerechnet_eur"]
    print(f"S155 Berlin J={j}: s155_angerechnet_eur {angerechnet:,.2f} € | s155_rampe {rampe[j]:,.2f} €")
    assert abs(angerechnet - rampe[j]) <= 1.0
    assert round(angerechnet, -2) == HUNDERTER[j]
    assert s["s155_jahre_seit_beginn"] == j
    assert abs(s["s155_avoided_eur"] - 252_500) <= 50      # die volle Wirkung bleibt daneben stehen


@pytest.mark.parametrize("j", [10, 20, 30])
def test_nutzen_mit_eingabe_gleich_angerechnet(j):
    config = {FELD: j}
    angerechnet = _summary(config)["s155_angerechnet_eur"]
    nutzen = _nutzen(config)
    print(f"S155 Berlin J={j}: annual_benefit_damage_eur {nutzen:,.2f} € | s155_angerechnet_eur "
          f"{angerechnet:,.2f} €")
    assert abs(nutzen - angerechnet) <= 1.0


@pytest.mark.parametrize("config", [None, {}, {FELD: None}, {FELD: ""}, {"anderes": 1}])
def test_ohne_eingabe_wie_bisher(config):
    s = _summary(config)
    assert s.get("s155_angerechnet_eur") is None
    assert abs(s["s155_avoided_eur"] - 252_500) <= 50
    assert [e["jahre"] for e in s["s155_rampe"]] == [10, 20, 30]
    voll = s["s155_avoided_eur"]
    assert abs(_nutzen(config) - voll) <= 0.01 * voll        # Nutzen = volle Wirkung (Aggregat-Test, 1 %)


def test_lange_laufzeit_ist_die_volle_wirkung():
    """J ≥ a_erk beider Entitäten (75 Jahre): angerechnet = volle Wirkung."""
    s = _summary({FELD: 100})
    assert abs(s["s155_angerechnet_eur"] - s["s155_avoided_eur"]) <= 1.0


@pytest.mark.parametrize("wert", [-1, -0.5, "zehn", "10", [10], {"j": 10}, True, float("nan"),
                                  float("inf")])
def test_ungueltige_eingabe_wird_abgewiesen(wert):
    with pytest.raises(ValidationError) as fehler:
        MeasureCreate(name="UV", measure_type=CODE, geometry_geojson={}, config={FELD: wert})
    assert "jahre_seit_beginn" in str(fehler.value)
    with pytest.raises(ValidationError):
        MeasureUpdate(config={FELD: wert})


@pytest.mark.parametrize("wert", [None, 0, 0.0, 10, 25.5])
def test_gueltige_eingabe_wird_angenommen(wert):
    m = MeasureCreate(name="UV", measure_type=CODE, geometry_geojson={}, config={FELD: wert})
    assert m.config[FELD] == wert
