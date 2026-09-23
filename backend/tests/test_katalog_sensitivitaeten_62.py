"""Test zu Befund 13 (reviews/BEFUNDE_62.md): Sensitivitäten S094–S098 im Katalogeintrag
kwra_id: 62 (Stadtklima / Wärmeinseln), T-0541.

Quelle ist die Arbeitsmappe `docs/Schadensbaum/KWRA-Schadensbaum_X_UBA-klimawirkungsketten.xlsx`,
Blatt „Klimawirkungsketten": Zeile 279 (W124, #62) ordnet sieben Sensitivitäten zu
(S094; S095; S096; S097; S098; S099; S100); die Namen S094–S098 stehen in den Stammzeilen
258–262. S099/S100 sind Bestand (bereits vor T-0541 im Katalog geführt).

Läuft mit pytest oder direkt: ``python tests/test_katalog_sensitivitaeten_62.py``.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.data import catalog  # noqa: E402

# Namen zeichengleich mit den Stammzeilen 258–262 der Arbeitsmappe (S094–S098);
# S099/S100 sind Bestand aus dem Katalog.
_ERWARTETE_SENSITIVITY_NAMES = [
    "Verwendete Baumaterialien auf Gebäudeebene",  # S094, Zeile 258
    "Begrünung von Gebäuden",  # S095, Zeile 259
    "Bauliche, organisatorische und finanzielle Vorsorge der öffentlichen Hand",  # S096, Zeile 260
    "Zustand von (Schutz-)Infrastrukturen",  # S097, Zeile 261
    "Verwendete Baumaterialien von (Schutz-)Infrastrukturen",  # S098, Zeile 262
    "Begrünung von Städten / Siedlungen",  # S099, Bestand
    "Grad der Versiegelung",  # S100, Bestand
]


def _eintrag_62() -> dict:
    treffer = [p for p in catalog.PLANNED_RISKS if p["kwra_id"] == 62]
    assert len(treffer) == 1, "genau ein PLANNED_RISKS-Eintrag mit kwra_id: 62 erwartet"
    return treffer[0]


def test_sensitivity_names_hat_sieben_eintraege():
    eintrag = _eintrag_62()
    assert len(eintrag["sensitivity_names"]) == 7


def test_sensitivity_names_reihenfolge_s094_bis_s100():
    eintrag = _eintrag_62()
    assert eintrag["sensitivity_names"] == _ERWARTETE_SENSITIVITY_NAMES


if __name__ == "__main__":
    test_sensitivity_names_hat_sieben_eintraege()
    test_sensitivity_names_reihenfolge_s094_bis_s100()
    print("OK")
