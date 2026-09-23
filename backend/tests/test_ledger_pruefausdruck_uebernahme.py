"""Test für T-0692-cto: `ledger.parse()` übernimmt den Prüfausdruck eines
früheren Vorkommens, wenn das letzte Vorkommen keinen trägt.

Anlass (Vorhaben T-0665-ceo, Messung T-0691-cto): Eine Befundnummer steht im
Ledger mehrfach — in der Kopftabelle mit Prüfausdruck und später in einer
Rundentabelle, die den Befund nur mit Status führt. Maßgeblich für den Status
ist das letzte Vorkommen. Bisher gewann es aber vollständig: Der Prüfausdruck
der Kopftabelle ging verloren, und `--pruefe` führte den Befund als
„unbelegt geschlossen", obwohl er einen Prüfausdruck trägt. Beim Befundtext
übernimmt `parse()` das frühere Vorkommen schon; dasselbe gilt jetzt für den
Prüfausdruck.

Der Mini-Ledger enthält Befund 1 (Kopftabelle mit grünem Prüfausdruck, spätere
Rundentabelle ohne Prüfausdruck, geschlossen) und Befund 2 (nie ein
Prüfausdruck, geschlossen) als Gegenprobe: Nur Befund 2 darf unbelegt bleiben.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import ledger  # noqa: E402

MINI_LEDGER = """# Befunde 99 (Test)

## Kopftabelle

| Nr | Befund (Ort · Art) | Kat | Status | Nachweis | Prüfausdruck |
|---|---|---|---|---|---|
| 1 | Bericht Kap. 1 · Lücke — Beispielbefund mit Ausdruck | B | offen | – | `python3 -c "pass"` |
| 2 | Bericht Kap. 2 · Lücke — Beispielbefund ohne Ausdruck | B | offen | – | – |

## Runde 2

| Nr | Kat | Status | Nachweis |
|---|---|---|---|
| 1 | B | geschlossen | Rev. 2 |
| 2 | B | geschlossen | Rev. 2 |
"""


def test_pruefausdruck_aus_frueherem_vorkommen_wird_uebernommen(tmp_path: Path) -> None:
    pfad = tmp_path / "BEFUNDE_99.md"
    pfad.write_text(MINI_LEDGER, encoding="utf-8")

    befunde = {b.nr: b for b in ledger.parse(pfad)}

    # Endstand kommt weiter aus dem letzten Vorkommen (Rundentabelle) ...
    assert befunde["1"].lage == "geschlossen"
    assert befunde["1"].zeile == 14
    # ... der Prüfausdruck aus der Kopftabelle geht dabei nicht verloren.
    assert befunde["1"].pruefausdruck == 'python3 -c "pass"'

    unbelegt = [b.nr for b in befunde.values()
                if b.lage == "geschlossen" and not b.pruefausdruck]
    assert unbelegt == ["2"]


# T-0785-ceo: Die Kopftabelle hat für den Prüfausdruck Vorrang vor späteren Vorkommen.
MINI_LEDGER_KOPF = """# Befunde 98 (Test)

## Kopftabelle

| Nr | Befund (Ort · Art) | Kat | Status | Nachweis | Prüfausdruck |
|---|---|---|---|---|---|
| 1 | Bericht Kap. 1 · Lücke — Ausdruck in Kopftabelle | B | offen | – | `python3 -c "raise SystemExit(0)"` |
| 2 | Bericht Kap. 2 · Lücke — Kopftabelle ohne Ausdruck | B | offen | – | – |

## Runde 2

| Nr | Kat | Status | Nachweis | Prüfausdruck |
|---|---|---|---|---|
| 1 | B | geschlossen | Rev. 2 | `python3 -c "raise SystemExit(1)"` |
| 2 | B | geschlossen | Rev. 2 | `python3 -c "raise SystemExit(0)"` |
"""


def test_kopftabelle_hat_vorrang_beim_pruefausdruck(tmp_path: Path) -> None:
    pfad = tmp_path / "BEFUNDE_98.md"
    pfad.write_text(MINI_LEDGER_KOPF, encoding="utf-8")

    befunde = {b.nr: b for b in ledger.parse(pfad)}

    assert befunde["1"].pruefausdruck == 'python3 -c "raise SystemExit(0)"'
    assert befunde["2"].pruefausdruck == 'python3 -c "raise SystemExit(0)"'
    assert befunde["1"].lage == "geschlossen"
