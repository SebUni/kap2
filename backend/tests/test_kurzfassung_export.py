"""T-0452: Kurzfassung für politische Entscheidungsträger (Checkliste Zeile 20).

Prüft ``app.services.kurzfassung_markdown.kurzfassung_markdown`` auf festen
Dienstergebnissen (je sieben Klimawirkungen und Maßnahmen, damit die
Fünf-Zeilen-Grenze greifen muss):
(a) die fünf Überschriften kommen in der festen Reihenfolge je genau einmal vor,
(b) die Tabellen in Abschnitt 2 und 4 haben höchstens fünf Datenzeilen,
(c) Abschnitt 5 enthält höchstens fünf Sätze.
Zusätzlich: die ausgewiesenen Zahlen sind die unveränderten Dienstwerte.
"""

from __future__ import annotations

import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.services.kurzfassung_markdown import kurzfassung_markdown  # noqa: E402

UEBERSCHRIFTEN = [
    "Gesamtrisiko",
    "Die fünf teuersten Klimawirkungen",
    "Erwartete Schadenssumme",
    "Die fünf wirksamsten Maßnahmen",
    "Methode und Grenzen",
]


def _aggregat() -> dict:
    klasse_a = [
        {"code": f"X{i}", "name": f"Wirkung {i}", "cost_eur": 1_000_000.0 - i * 100_000,
         "has_euro_layer": True, "risk_class": "hoch"}
        for i in range(7)
    ]
    klasse_b = [{"code": "B1", "name": "Screening", "cost_eur": None,
                 "has_euro_layer": False, "risk_class": "mittel"}]
    return {"cost": {"total_eur": 5_234_567.89, "by_risk": klasse_a + klasse_b}}


def _projektion() -> dict:
    return {
        "years": [2025, 2045, 2065],
        "scenarios": {
            "rcp45": {"label": "RCP 4.5 (moderater Klimaschutz)",
                      "no_measures": {"cumulative": [1.0, 2.0, 3.0]}},
            "rcp85": {"label": "RCP 8.5 (weiter wie bisher)",
                      "no_measures": {"cumulative": [5.0e6, 1.1e8, 2.5e8]}},
        },
    }


def _kostenuebersicht() -> dict:
    zeilen = [
        {"name": f"Maßnahme {i}", "annual_benefit_eur": 10_000.0 * (i + 1),
         "capex_eur": 50_000.0, "opex_annual_eur": 1_000.0,
         "benefit_has_euro_layer": True}
        for i in range(7)
    ]
    return {"measures": {"rows": zeilen}}


def _dokument() -> str:
    return kurzfassung_markdown("Musterstadt", _aggregat(), _projektion(), _kostenuebersicht())


def _abschnitte(text: str) -> dict[str, str]:
    teile = re.split(r"^## (.+)$", text, flags=re.MULTILINE)
    return {teile[i].strip(): teile[i + 1] for i in range(1, len(teile), 2)}


def _datenzeilen(abschnitt: str) -> list[str]:
    zeilen = [z for z in abschnitt.splitlines() if z.startswith("|")]
    return [z for z in zeilen[1:] if not re.fullmatch(r"\|( *-+ *\|)+", z)]


def test_a_fuenf_ueberschriften_in_reihenfolge_je_genau_einmal():
    gefunden = re.findall(r"^## (.+)$", _dokument(), flags=re.MULTILINE)
    for u in UEBERSCHRIFTEN:
        assert gefunden.count(u) == 1, f"Überschrift {u!r}: {gefunden.count(u)}-mal"
    assert gefunden == UEBERSCHRIFTEN


def test_b_tabellen_hoechstens_fuenf_datenzeilen():
    abschnitte = _abschnitte(_dokument())
    for u in (UEBERSCHRIFTEN[1], UEBERSCHRIFTEN[3]):
        daten = _datenzeilen(abschnitte[u])
        assert 0 < len(daten) <= 5, (u, daten)


def test_c_methode_und_grenzen_hoechstens_fuenf_saetze():
    text = _abschnitte(_dokument())[UEBERSCHRIFTEN[4]].strip()
    saetze = [s for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]
    assert 1 <= len(saetze) <= 5, saetze


def test_zahlen_unveraendert_aus_den_diensten():
    abschnitte = _abschnitte(_dokument())
    gesamt = abschnitte[UEBERSCHRIFTEN[0]].strip()
    assert "5.234.568 €" in gesamt
    assert len(re.findall(r"[.!?](?:\s|$)", gesamt)) == 1  # genau ein Satz
    # teuerste Klimawirkung zuerst, Klasse B nie in der Tabelle
    daten = _datenzeilen(abschnitte[UEBERSCHRIFTEN[1]])
    assert daten[0].startswith("| Wirkung 0 | 1.000.000 € |")
    assert all("Screening" not in z for z in daten)
    summe = abschnitte[UEBERSCHRIFTEN[2]]
    assert "250.000.000 €" in summe and "RCP 8.5" in summe
    assert "2025" in summe and "2065" in summe
    # wirksamste Maßnahme (höchster Nutzen) zuerst
    massnahmen = _datenzeilen(abschnitte[UEBERSCHRIFTEN[3]])
    assert massnahmen[0].startswith("| Maßnahme 6 | 70.000 € |")
