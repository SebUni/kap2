"""Verwechslungssperre Klasse A/B im Dashboard (T-0517, Vorhaben T-0358).

Liest vier Dashboard-Komponenten als Text (ohne Node/Browser) und prüft:

(1) CostTablesSection.tsx und RiskDistributionSection.tsx zeigen an der Stelle des
    Schadenswerts einen Zweig auf ``has_euro_layer``, der ``cost_display`` ausgibt
    (Klasse B → Screening-Vermerk des Backends), und enthalten kein Literal ``'-'``
    (bzw. Gedankenstrich ``'–'``) und kein Literal ``'0 €'`` als Ersatzdarstellung;
(2) RiskRadarSection.tsx filtert Einträge nicht mehr allein über ``cost_eur > 0``
    aus der Liste;
(3) CostTablesSection.tsx und KommuneHeader.tsx geben ``euro_coverage.text`` aus, und
    in keiner der vier Dateien steht der Satzbaustein „Klimawirkungen in Euro
    beziffert“ als Literal — der Text kommt ausschließlich vom Backend.

Kommentare werden vor der Prüfung entfernt, damit ein Kommentar allein keinen
Treffer erzeugt.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

DASHBOARD = (Path(__file__).resolve().parents[2]
             / "frontend" / "src" / "components" / "dashboard")

COST_TABLES = "CostTablesSection.tsx"
RISK_DISTRIBUTION = "RiskDistributionSection.tsx"
RISK_RADAR = "RiskRadarSection.tsx"
KOMMUNE_HEADER = "KommuneHeader.tsx"
ALLE = [COST_TABLES, RISK_DISTRIBUTION, RISK_RADAR, KOMMUNE_HEADER]


def _roh(name: str) -> str:
    return (DASHBOARD / name).read_text(encoding="utf-8")


def _code(name: str) -> str:
    """Quelltext ohne Block-/JSX-Kommentare und ohne reine Zeilenkommentare."""
    text = re.sub(r"/\*.*?\*/", "", _roh(name), flags=re.S)
    return "\n".join(z for z in text.splitlines() if not z.lstrip().startswith("//"))


# Ternärer Zweig auf has_euro_layer, dessen einer Arm cost_display ausgibt —
# in beiden Reihenfolgen, innerhalb eines JSX-Ausdrucks (ohne schließende Klammer).
_ZWEIG = re.compile(
    r"has_euro_layer[^{}\n]*\?[^{}\n]*cost_display"
    r"|has_euro_layer[^{}\n]*\?[^{}\n]*:[^{}\n]*cost_display"
)

# Strich oder Gedankenstrich bzw. „0 €“ als String-Literal.
_STRICH = re.compile(r"""(['"`])\s*[-–—]\s*\1""")
_NULL_EURO = re.compile(r"""(['"`])\s*0\s*€\s*\1""")


@pytest.mark.parametrize("name", [COST_TABLES, RISK_DISTRIBUTION])
def test_schadenswert_zweig_auf_has_euro_layer(name):
    code = _code(name)
    assert _ZWEIG.search(code), (
        f"{name}: kein Zweig auf has_euro_layer, der cost_display ausgibt")
    # Der Zweig steht an der Stelle des Schadenswerts (Spalte/Karte „Schaden/Jahr“).
    pos_schaden = code.find("Schaden/Jahr")
    assert pos_schaden != -1, f"{name}: Schadenswert-Stelle „Schaden/Jahr“ fehlt"
    assert any(m.start() > pos_schaden for m in _ZWEIG.finditer(code)), (
        f"{name}: Zweig auf has_euro_layer steht nicht beim Schadenswert")


@pytest.mark.parametrize("name", [COST_TABLES, RISK_DISTRIBUTION])
def test_kein_strich_und_kein_null_euro_als_ersatz(name):
    code = _code(name)
    assert not _STRICH.search(code), f"{name}: Literal '-' als Ersatzdarstellung"
    assert not _NULL_EURO.search(code), f"{name}: Literal '0 €' als Ersatzdarstellung"


def test_top_risiken_filtern_nicht_allein_ueber_cost_eur():
    code = _code(RISK_RADAR)
    filter_aufrufe = re.findall(r"\.filter\(([^\n]*)\)", code)
    betroffen = [f for f in filter_aufrufe if "cost_eur" in f]
    assert betroffen, "RiskRadarSection.tsx: Filter der Top-Risiken nicht gefunden"
    for f in betroffen:
        assert "has_euro_layer" in f, (
            f"RiskRadarSection.tsx filtert allein über cost_eur: {f}")
    # Klasse B fällt nicht still weg, sondern wird eigens gelistet.
    assert re.search(r"\.filter\([^\n]*has_euro_layer\s*===\s*false", code), (
        "RiskRadarSection.tsx: Klasse-B-Einträge werden nicht gelistet")


@pytest.mark.parametrize("name", [COST_TABLES, KOMMUNE_HEADER])
def test_vollstaendigkeitsanzeige_aus_backend(name):
    code = _code(name)
    assert re.search(r"euro_coverage\??\.text", code), (
        f"{name}: euro_coverage.text wird nicht ausgegeben")


@pytest.mark.parametrize("name", ALLE)
def test_kein_satzbaustein_als_literal(name):
    assert "Klimawirkungen in Euro beziffert" not in _roh(name), (
        f"{name}: Satzbaustein als Literal statt euro_coverage.text vom Backend")
