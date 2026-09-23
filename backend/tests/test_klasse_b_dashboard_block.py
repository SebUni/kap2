"""Verwechslungssperre Klasse A/B, Teilpaket 2: Dashboard-Rangliste (T-0823, Vorhaben T-0563).

Liest RiskRadarSection.tsx und frontend/src/types/index.ts als Text (ohne Node/Browser)
und prüft:

(1) der Text „Ohne Euro-Bezifferung (Screening)“ kommt in RiskRadarSection.tsx vor;
(2) die Liste, aus der die Rangliste „Größte Schadenstreiber“ gerendert wird, entsteht
    nur aus Einträgen mit ``has_euro_layer !== false`` (ein reiner ``.filter`` auf die
    by_risk-Liste, dessen Bedingung ``has_euro_layer !== false`` konjunktiv enthält —
    kein ``||``, kein Zusammenfügen mit weiteren Listen);
(3) die Klasse-B-Einträge (``has_euro_layer === false``) werden in einem eigenen Block
    nach dieser Überschrift gerendert, dessen map-Callback keinen Index-Parameter hat
    (kein Rang für Klasse B);
(4) im Typ von ``by_risk`` in types/index.ts ist ``cost_eur`` als ``number | null``
    deklariert.

Kommentare werden vor der Prüfung entfernt, damit ein Kommentar allein keinen Treffer
erzeugt. Muster: test_klasse_b_nebenansichten.py (T-0518).
"""
from __future__ import annotations

import re
from pathlib import Path

FRONTEND = Path(__file__).resolve().parents[2] / "frontend" / "src"
RISK_RADAR = FRONTEND / "components" / "dashboard" / "RiskRadarSection.tsx"
TYPES = FRONTEND / "types" / "index.ts"

UEBERSCHRIFT = "Ohne Euro-Bezifferung (Screening)"
RANGLISTE = "Größte Schadenstreiber"


def _code(pfad: Path) -> str:
    """Quelltext ohne Block-/JSX-Kommentare und ohne reine Zeilenkommentare."""
    text = re.sub(r"/\*.*?\*/", "", pfad.read_text(encoding="utf-8"), flags=re.S)
    return "\n".join(z for z in text.splitlines() if not z.lstrip().startswith("//"))


def _definition(code: str, name: str) -> str:
    m = re.search(rf"\bconst\s+{name}\s*=\s*([^\n]+)", code)
    assert m, f"RiskRadarSection.tsx: Definition von {name} nicht gefunden"
    return m.group(1).strip()


def _abschnitt_top_risiken(code: str) -> str:
    """Der Quelltext der Karte „Größte Schadenstreiber“ (TopRisksCard)."""
    start = code.find("function TopRisksCard")
    assert start != -1, "RiskRadarSection.tsx: TopRisksCard nicht gefunden"
    ende = code.find("\nfunction ", start + 1)
    ende2 = code.find("\nexport function ", start + 1)
    kandidaten = [e for e in (ende, ende2) if e != -1]
    return code[start: min(kandidaten) if kandidaten else len(code)]


def test_ueberschrift_screening_block_vorhanden():
    assert UEBERSCHRIFT in _code(RISK_RADAR), (
        f"RiskRadarSection.tsx: Überschrift „{UEBERSCHRIFT}“ fehlt")


def test_rangliste_nur_klasse_a():
    karte = _abschnitt_top_risiken(_code(RISK_RADAR))
    pos_titel = karte.find(RANGLISTE)
    assert pos_titel != -1, f"RiskRadarSection.tsx: Überschrift „{RANGLISTE}“ fehlt"
    # Die erste Liste, die nach der Überschrift gerendert wird, ist die Rangliste.
    m = re.search(r"\{\s*(\w+)\.map\(", karte[pos_titel:])
    assert m, "RiskRadarSection.tsx: Rangliste (…map) nach der Überschrift nicht gefunden"
    liste = m.group(1)
    definition = _definition(karte, liste)
    f = re.fullmatch(
        r"\w+\.filter\(\s*\(?\s*\w+\s*\)?\s*=>\s*(.+?)\)(?:\.slice\([^()]*\))?", definition)
    assert f, (f"Rangliste „{liste}“ entsteht nicht als reiner Filter der by_risk-Liste: "
               f"{definition}")
    bedingung = f.group(1)
    assert re.search(r"has_euro_layer\s*!==\s*false", bedingung), (
        f"Rangliste „{liste}“ filtert nicht auf has_euro_layer !== false: {bedingung}")
    assert "||" not in bedingung, (
        f"Rangliste „{liste}“ lässt über || weitere Einträge zu: {bedingung}")


def test_klasse_b_eigener_block_ohne_index():
    karte = _abschnitt_top_risiken(_code(RISK_RADAR))
    pos = karte.find(UEBERSCHRIFT)
    assert pos != -1, f"TopRisksCard: Überschrift „{UEBERSCHRIFT}“ fehlt"
    nach = karte[pos:]
    maps = list(re.finditer(r"(\w+)\.map\(\s*(\(?[^=()]*\)?)\s*=>", nach))
    assert maps, f"Kein map-Aufruf nach „{UEBERSCHRIFT}“"
    block = None
    for m in maps:
        definition = _definition(karte, m.group(1))
        if re.search(r"has_euro_layer\s*===\s*false", definition):
            block = m
            break
    assert block, (f"Nach „{UEBERSCHRIFT}“ wird keine Liste mit has_euro_layer === false "
                   "gerendert")
    parameter = [p for p in block.group(2).strip("() ").split(",") if p.strip()]
    assert len(parameter) == 1, (
        f"map-Callback des Screening-Blocks hat einen Index-Parameter: {block.group(0)}")
    # Klasse B steht nicht vor der Überschrift in der Rangliste.
    vor = karte[:karte.find(UEBERSCHRIFT)]
    assert not re.search(rf"\b{block.group(1)}\.map\(", vor), (
        "Klasse-B-Einträge werden schon vor der Screening-Überschrift gerendert")


def test_by_risk_cost_eur_nullable():
    code = _code(TYPES)
    m = re.search(r"by_risk\s*:\s*\{(.*?)\}\s*\[\]", code, flags=re.S)
    assert m, "types/index.ts: Typ von by_risk nicht gefunden"
    assert re.search(r"\bcost_eur\s*:\s*number\s*\|\s*null\b", m.group(1)), (
        "types/index.ts: cost_eur in by_risk ist nicht als number | null deklariert")
