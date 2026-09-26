"""Die Wirkungsmechanismus-Vorschau #95 bildet Rev. 8 ab: Kühlräume S157 und Schutzprogramme δ_VG (T-1390).

Die Sollwerte stammen aus Kapitel 7 des Berichts (Zeilen ``id:`` und ``wert:``), nicht aus dem Test.
"""
import importlib.util
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SKRIPT = ROOT / "scripts" / "wirkungsmechanismus_preview.py"
BERICHT = ROOT / "docs" / "methodik" / "95_hitzebelastung.md"

NEUE_KENNUNGEN = ("heat.ror_s157", "heat.g_s157", "heat.delta_hap", "heat.delta_vg", "heat.delta_vg_morb")


def _modul():
    spec = importlib.util.spec_from_file_location("wm_preview_rev8", SKRIPT)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def _kapitel7() -> str:
    text = BERICHT.read_text(encoding="utf-8")
    m = re.search(r"^## 7 .*?$(.*?)^## 8 ", text, re.M | re.S)
    assert m, "Kapitel 7 nicht gefunden"
    return m.group(1)


def _zahl(wert):
    """Einzelne Zahl oder None (Dict, Liste, Text)."""
    if isinstance(wert, bool):
        return None
    if isinstance(wert, (int, float)):
        return float(wert)
    if isinstance(wert, str):
        try:
            return float(wert.strip())
        except ValueError:
            return None
    return None


def _bericht_werte() -> dict:
    werte = {}
    for block in re.split(r"^parameter:\s*$", _kapitel7(), flags=re.M)[1:]:
        pid = re.search(r"^\s+id:\s*(\S+)", block, re.M)
        wert = re.search(r"^\s+wert:\s*(.*)$", block, re.M)
        if pid and wert:
            roh = wert.group(1).split("#", 1)[0].strip()
            werte[pid.group(1)] = roh
    return werte


@pytest.fixture(scope="module")
def plan():
    return _modul()._graph_95_plan()


def test_kapitel7_liefert_die_neuen_bloecke():
    werte = _bericht_werte()
    for pid in NEUE_KENNUNGEN:
        assert pid in werte, pid


def test_neue_kennungen_in_der_parameterliste(plan):
    _, params = plan
    ids = {p["id"] for p in params}
    fehlend = [pid for pid in NEUE_KENNUNGEN if pid not in ids]
    assert not fehlend, f"fehlt in _graph_95_plan(): {fehlend}"


def test_einzelwerte_gleich_dem_bericht(plan):
    _, params = plan
    bericht = _bericht_werte()
    verglichen = 0
    abweichend = []
    for p in params:
        if p["id"] not in bericht:
            continue
        soll, ist = _zahl(bericht[p["id"]]), _zahl(p["value"])
        if soll is None or ist is None:
            continue
        verglichen += 1
        if abs(soll - ist) > 1e-9:
            abweichend.append((p["id"], ist, soll))
    assert not abweichend, f"Skript weicht von Kapitel 7 ab (id, Skript, Bericht): {abweichend}"
    assert verglichen > 0


@pytest.mark.parametrize("wort", ["Kühlräume", "Schutzprogramme"])
def test_knoten_fuer_die_massnahme(plan, wort):
    graph, _ = plan
    labels = [n.get("label", "") for n in graph["nodes"]]
    assert any(wort in lab for lab in labels), f"kein Knoten mit „{wort}“"
