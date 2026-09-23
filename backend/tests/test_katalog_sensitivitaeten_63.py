"""Test zur Vorrangregel (docs/AUFGABE_METHODIK_SCHADENSRECHNUNG.md, Abschnitt
„Vorrang zwischen den UBA-Digitalisaten", Beispielfall #63): Sensitivitäten S092–S094
im Katalogeintrag kwra_id: 63 (Innenraumklima), T-0564.

Quelle ist die Arbeitsmappe `docs/Schadensbaum/KWRA-Schadensbaum_X_UBA-klimawirkungsketten.xlsx`,
Blatt „Klimawirkungsketten": Zeile 278 (W123, #63), Spalte J (Kopfzelle J1:
`Input_Namen_Sensitivitäten`) ordnet drei Sensitivitäten zu (S092, S093, S094, Spalte F
derselben Zeile). Die KWRA-2021-Mappe (Blatt „Wirkungsmechanismen", Zeile 68, ID 63, Spalte G)
nennt stattdessen „Verwendete Baumaterialien auf Gebäudeebene · Begrünung von Gebäuden"; nach der
Vorrangregel gilt die Schadensbaum-Mappe.

Läuft mit pytest oder direkt: ``python tests/test_katalog_sensitivitaeten_63.py``.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.data import catalog  # noqa: E402

# Namen zeichengleich mit Zeile 278, Spalte J der Schadensbaum-Mappe (S092–S094).
_ERWARTETE_SENSITIVITY_NAMES = [
    "Bauliche, organisatorische und finanzielle Vorsorge der Eigentümer und Nutzer von "
    "Gebäuden und Infrastrukturen",  # S092
    "Zustand von Gebäuden und Infrastrukturen",  # S093
    "Verwendete Baumaterialien auf Gebäudeebene",  # S094
]


def _eintrag_63() -> dict:
    treffer = [p for p in catalog.PLANNED_RISKS if p["kwra_id"] == 63]
    assert len(treffer) == 1, "genau ein PLANNED_RISKS-Eintrag mit kwra_id: 63 erwartet"
    return treffer[0]


def test_sensitivity_names_hat_drei_eintraege():
    eintrag = _eintrag_63()
    assert len(eintrag["sensitivity_names"]) == 3


def test_sensitivity_names_reihenfolge_s092_bis_s094():
    eintrag = _eintrag_63()
    assert eintrag["sensitivity_names"] == _ERWARTETE_SENSITIVITY_NAMES


if __name__ == "__main__":
    test_sensitivity_names_hat_drei_eintraege()
    test_sensitivity_names_reihenfolge_s092_bis_s094()
    print("OK")
