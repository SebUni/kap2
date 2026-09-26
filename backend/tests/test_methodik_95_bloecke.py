"""Abgleich Registry ⇄ Parameter-Blöcke des Berichts #95 (T-1370, Übernahmeliste (f)).

Kapitel 7 von ``docs/methodik/95_hitzebelastung.md`` führt 23 maschinenlesbare
Parameter-Blöcke (``parameter:`` / ``id: heat.…``). Jeder Registry-Parameter der
Hitzebelastung trägt im Feld ``methodik_block`` die Kennung seines Blocks. Geprüft wird:

1. Die Menge der ``methodik_block``-Werte der Registry ist genau die Menge der 23
   Block-Kennungen aus Kapitel 7 — kein Block ohne Parameter, keine erfundene Kennung.
2. Der Wert jedes Registry-Parameters stimmt mit dem ``wert`` seines Blocks überein
   (Divergenz = Meldung an den CMO, nie stiller Code-Fix; Eiserne Regel 5).
3. ``heat.q_wochenquantile`` und ``heat.gamma_hoehe`` sind Registry-Parameter;
   γ_h wirkt als Überschreibung auf die Zelltemperatur.
"""

from __future__ import annotations

import os
import re
import sys

import yaml

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.services import parameter_registry  # noqa: E402
from app.services.engine import override_context  # noqa: E402

REPORT = os.path.join(os.path.dirname(__file__), "..", "..",
                      "docs", "methodik", "95_hitzebelastung.md")

# Schlüssel der Mehrfach-Blöcke (Region/Altersband) → Suffix der Registry-ID.
_SUFFIX = {"nord": "nord", "mitte": "mitte", "sued": "sued",
           "u65": "u65", "65-74": "a65_74", "75-84": "a75_84", "85+": "a85p"}


def _kapitel7() -> str:
    with open(os.path.abspath(REPORT), encoding="utf-8") as fh:
        text = fh.read()
    start = text.index("## 7 Parameter-Blöcke")
    ende = text.index("\n## 8 ", start)
    return text[start:ende]


def _bloecke() -> dict[str, dict]:
    """Block-Kennung → Block (aus dem YAML-Abschnitt von Kapitel 7)."""
    yaml_teil = re.search(r"```yaml\n(.*?)```", _kapitel7(), re.S).group(1)
    teile = re.split(r"^parameter:\n", yaml_teil, flags=re.M)
    bloecke = {}
    for teil in teile:
        if not teil.strip():
            continue
        b = yaml.safe_load(teil)
        bloecke[b["id"]] = b
    return bloecke


def _registry() -> list[dict]:
    return parameter_registry.catalog_parameters()


def test_block_kennungen_der_registry_sind_genau_die_23_aus_kapitel_7():
    soll = set(_bloecke())
    # Gegenzählung ohne YAML-Parser: jede "id:"-Zeile nach "parameter:".
    roh = re.findall(r"^parameter:\n  id: (\S+)", _kapitel7(), re.M)
    assert len(roh) == 23 and set(roh) == soll, sorted(roh)
    ist = {p["methodik_block"] for p in _registry() if p.get("methodik_block")}
    assert ist == soll, (f"fehlen in der Registry: {sorted(soll - ist)}; "
                         f"nicht in Kapitel 7: {sorted(ist - soll)}")


def test_werte_der_registry_stimmen_mit_den_bloecken_ueberein():
    bloecke = _bloecke()
    nach_block: dict[str, list[dict]] = {}
    for p in _registry():
        if p.get("methodik_block"):
            nach_block.setdefault(p["methodik_block"], []).append(p)
    abweichungen = []
    for bid, block in bloecke.items():
        params = nach_block[bid]
        wert = block["wert"]
        if isinstance(wert, dict):
            for schluessel, soll in wert.items():
                treffer = [p for p in params
                           if p["id"].endswith("_" + _SUFFIX[schluessel])]
                if len(treffer) != 1 or treffer[0]["value"] != soll:
                    abweichungen.append((bid, schluessel, soll,
                                         [p["value"] for p in treffer]))
            continue
        assert len(params) == 1, (bid, [p["id"] for p in params])
        ist = params[0]["value"]
        if bid == "heat.delta_hap":
            # Maßnahme HEAT_ACTION_PLANS führt die Minderung 1 − δ_HAP.
            ist = round(1.0 - ist, 10)
        if isinstance(wert, str):
            gleich = ist == wert
        else:
            # Der Block rundet (heat.g_s157: 0,29 = 0,2936 aus der Formel, T-1367).
            stellen = len(repr(float(wert)).split(".")[1])
            gleich = round(float(ist), stellen) == float(wert)
        if not gleich:
            abweichungen.append((bid, wert, ist))
    assert not abweichungen, abweichungen


def test_konstanten_q_wochenquantile_und_gamma_hoehe_in_der_registry():
    by_id = {p["id"]: p for p in _registry()}
    q = by_id["risks.EXPECTED_ANNUAL_MORTALITY.impact.q_wochenquantile"]
    g = by_id["risks.EXPECTED_ANNUAL_MORTALITY.impact.gamma_hoehe"]
    assert q["methodik_block"] == "heat.q_wochenquantile"
    assert g["methodik_block"] == "heat.gamma_hoehe"
    assert q["editable"] is False          # Tabelle 3 × 13, kein Einzelwert
    assert g["editable"] is True and g["value"] == 0.0065
    for p in (q, g):
        assert p["source_detail"] and p["evidence_class"] == "belegt"


def test_gamma_hoehe_wirkt_auf_die_zelltemperatur():
    from app.services.engine.inputs import apply_cell_temperature
    from shapely.geometry import Point

    def lauf() -> list[float]:
        cells = [{"uhi_delta_mean": 0.0, "mean_elevation_m": h} for h in (0.0, 200.0)]
        grid = [{"geometry": Point(0, 0), "x_3035": 100, "y_3035": 100},
                {"geometry": Point(0, 0), "x_3035": 200, "y_3035": 100}]
        import app.services.climate.dwd_cdc_grid as dwd
        alt = dwd.climatology_grid
        dwd.climatology_grid = lambda *a, **k: (_ for _ in ()).throw(OSError())
        try:
            apply_cell_temperature(cells, grid, {"summer_temp_mean": 18.0})
        finally:
            dwd.climatology_grid = alt
        return [c["summer_temp_cell"] for c in cells]

    basis = lauf()
    assert basis == [18.65, 17.35]         # ± 0,0065 K/m × 100 m
    with override_context.override_scope(
            {"risks.EXPECTED_ANNUAL_MORTALITY.impact.gamma_hoehe": 0.01}):
        assert lauf() == [19.0, 17.0]


if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main([__file__, "-q"]))
