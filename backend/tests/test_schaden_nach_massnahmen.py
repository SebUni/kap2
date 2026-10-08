"""Karte „Erwartete Schäden je Risiko“: feste Bedeutung der Spalte „Schaden/Jahr“ (T-1816).

Das Frontend hat keinen Testläufer (``frontend/package.json``: nur ``dev``, ``build``,
``preview``, ``typecheck``). Die Entscheidung, welche Beträge die Karte zeigt, steht deshalb in
einer reinen Funktion ohne React, ``frontend/src/utils/schadenNachMassnahmen.ts``. Dieser
Test bündelt sie mit dem ``esbuild`` aus ``frontend/node_modules`` und führt sie mit ``node``
aus, also die Quelle selbst und keine Nachbildung in Python. Fehlt eines von beiden, wird
übersprungen.

Zwei Ladestände (Abnahmekriterium 3):

1. nur ``riskSummary``: keine Spalte „nach Maßnahmen“;
2. ``riskSummary`` mit abweichendem ``costSummary``: Spalte vorhanden, Betrag nur bei Abweichung.

Dass die Komponente „Schaden/Jahr“ aus ``riskSummary`` liest und nie aus ``costSummary``,
prüft ein Quelltext-Test (kein ``costSummary?.by_risk``/``klimawirkungen`` als Ersatz mehr).
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
FRONTEND = REPO / "frontend"
QUELLE = FRONTEND / "src" / "utils" / "schadenNachMassnahmen.ts"
KOMPONENTE = FRONTEND / "src" / "components" / "dashboard" / "CostTablesSection.tsx"
RADAR = FRONTEND / "src" / "components" / "dashboard" / "RiskRadarSection.tsx"
ESBUILD = FRONTEND / "node_modules" / ".bin" / "esbuild"
NODE = shutil.which("node")

pytestmark = pytest.mark.skipif(
    not ESBUILD.exists() or NODE is None,
    reason="esbuild (frontend/node_modules) oder node fehlt",
)


def _zeile(code: str, eur: float | None, kwra_id: int | None) -> dict:
    return {"code": code, "name": code, "cost_eur": eur, "kwra_id": kwra_id,
            "outcome": 1.0, "outcome_unit": "x", "cost_dimension": "d", "index": 1.0}


def _eintrag(kwra_id: int, codes: list[str], eur: float, teile: list[dict]) -> dict:
    return {"kwra_id": kwra_id, "name": f"K{kwra_id}", "bezeichnung": f"K{kwra_id} (#{kwra_id})",
            "cost_eur": eur, "has_euro_layer": True, "codes": codes, "teile": teile}


def _kosten(hitze: float, hitze_a: float, hitze_b: float, pollen: float) -> dict:
    """#95 mit zwei Teilzeilen, #96 als einzelne Zeile (wie in Warmsen)."""
    a, b = _zeile("H_A", hitze_a, 95), _zeile("H_B", hitze_b, 95)
    p = _zeile("P", pollen, 96)
    return {
        "by_risk": [a, b, p],
        "klimawirkungen": [_eintrag(95, ["H_A", "H_B"], hitze, [a, b]),
                           _eintrag(96, ["P"], pollen, [])],
    }


# Zahlen von Warmsen aus dem Ticket: 144.393 € ohne, 135.838 € mit Maßnahmen.
OHNE = _kosten(144392.88, 100000.0, 44392.88, 2281.0)
MIT = {**_kosten(135838.0, 93000.0, 42838.0, 2281.0), "damages_with_measures_eur": 138119.0}
GLEICH = {**_kosten(144392.6, 100000.0, 44392.6, 2281.0), "damages_with_measures_eur": 146674.0}

SKRIPT = """
import {{ schadenNachMassnahmen, gesamtNachMassnahmen }} from {quelle}
const e = {eingabe}
const r = schadenNachMassnahmen(e.ausgang, e.mit, 20)
console.log(JSON.stringify({{
  hatSpalte: r.hatSpalte,
  summe: Object.fromEntries(r.summe),
  zeile: Object.fromEntries(r.zeile),
  gesamt: gesamtNachMassnahmen(e.gesamt, e.mit),
}}))
"""


def _lauf(tmp_path: Path, ausgang: dict, mit: dict | None, gesamt: float, quelle: Path = QUELLE) -> dict:
    eingabe = json.dumps({"ausgang": ausgang, "mit": mit, "gesamt": gesamt})
    eintritt = tmp_path / "eintritt.ts"
    eintritt.write_text(SKRIPT.format(quelle=json.dumps(str(quelle)), eingabe=eingabe), encoding="utf-8")
    ziel = tmp_path / "gebuendelt.mjs"
    bau = subprocess.run(
        [str(ESBUILD), str(eintritt), "--bundle", "--format=esm", "--platform=node",
         f"--outfile={ziel}", "--log-level=error"],
        capture_output=True, text=True, timeout=60)
    assert bau.returncode == 0, bau.stderr
    out = subprocess.run([NODE, str(ziel)], capture_output=True, text=True, timeout=60)
    assert out.returncode == 0, out.stderr
    return json.loads(out.stdout)


def test_ladestand_nur_risk_summary_keine_spalte(tmp_path: Path) -> None:
    r = _lauf(tmp_path, OHNE, None, 146673.88)
    assert r == {"hatSpalte": False, "summe": {}, "zeile": {}, "gesamt": None}


def test_ladestand_mit_abweichendem_cost_summary_zeigt_spalte(tmp_path: Path) -> None:
    r = _lauf(tmp_path, OHNE, MIT, 146673.88)
    assert r["hatSpalte"] is True
    # Summenzeile #95 und beide Teilzeilen weichen ab; #96 ist gleich und bleibt leer.
    assert r["summe"] == {"H_A|H_B": 135838.0}
    assert r["zeile"] == {"H_A": 93000.0, "H_B": 42838.0}
    assert "P" not in r["zeile"]
    assert r["gesamt"] == 138119.0


def test_geladenes_cost_summary_ohne_abweichung_keine_spalte(tmp_path: Path) -> None:
    # Unterschied unter einem Euro: die Karte zeigt ganze Euro, also keine Abweichung.
    r = _lauf(tmp_path, OHNE, GLEICH, 146673.88 + 0.3)
    assert r["hatSpalte"] is False
    assert r["summe"] == {} and r["zeile"] == {}


def test_klasse_b_ohne_betrag_keine_abweichung(tmp_path: Path) -> None:
    ausgang = _kosten(100.0, 60.0, 40.0, 5.0)
    ausgang["by_risk"][2]["cost_eur"] = None
    ausgang["klimawirkungen"][1]["cost_eur"] = None
    mit = {**ausgang, "damages_with_measures_eur": 100.0}
    r = _lauf(tmp_path, ausgang, mit, 100.0)
    assert r["hatSpalte"] is False


def test_komponente_liest_schaden_je_jahr_nur_aus_risk_summary() -> None:
    text = KOMPONENTE.read_text(encoding="utf-8")
    for verboten in ("costSummary?.by_risk", "costSummary?.klimawirkungen",
                     "costSummary?.damages_with_measures_eur", "costSummary.klimawirkungen"):
        assert verboten not in text, f"Ersatz der Ausgangslage durch cost-summary: {verboten}"
    assert "riskSummary.cost.klimawirkungen" in text
    assert "nach Maßnahmen" in text


def test_schadenstreiber_karte_liest_betraege_nur_aus_risk_summary() -> None:
    """T-1863: TopRisksCard (RiskRadarSection) fällt nicht auf costSummary zurück."""
    text = RADAR.read_text(encoding="utf-8")
    for verboten in ("costSummary?.by_risk", "costSummary?.klimawirkungen",
                     "costSummary.by_risk", "costSummary.klimawirkungen",
                     "costSummary?.by_risk ||", "costSummary?.klimawirkungen ||"):
        assert verboten not in text, f"Rückfall auf cost-summary: {verboten}"
    assert "riskSummary?.cost.klimawirkungen" in text
    assert "schadenNachMassnahmen(" in text
    assert "nach Maßnahmen" in text
