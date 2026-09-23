"""Tests für T-0530: `deploy/test-deploy.sh` führt die Deploy-Tests vor dem eigentlichen
Deploy aus und bricht bei Rot ab, bevor gebaut oder ausgeliefert wird.

Anlass: Aus T-0484 blieb die Frage offen, ob die Deploy-Tests vor jedem Deploy laufen sollen.
Ja — sonst fällt Drift zwischen Skript und Tests erst beim Ausliefern auf.
"""

from __future__ import annotations

import re

from _deploy_anker import anker_index, ausschnitt, skript_text


def test_deploy_tests_laufen_vor_bau_und_auslieferung():
    """Der Schritt `deploy-tests` steht nach dem Checkout und vor jedem Bau-/Auslieferungsschritt."""
    text = skript_text()
    checkout = anker_index(text, 'SCHRITT="git"')
    tests = anker_index(text, 'SCHRITT="deploy-tests"')
    assert checkout < tests
    for spaeter in (
        'SCHRITT="backend-abhaengigkeiten"',
        'SCHRITT="frontend-build"',
        'SCHRITT="datenbank"',
        'SCHRITT="dienst"',
        'SCHRITT="status"',
    ):
        assert tests < anker_index(text, spaeter), spaeter


def test_deploy_tests_brechen_bei_rot_ab():
    """Rot endet in `false` (ERR-Falle), nicht in einer Warnung mit Weiterlauf."""
    block = ausschnitt('SCHRITT="deploy-tests"', 'SCHRITT="backend-abhaengigkeiten"')
    kopf = anker_index(block, "-m pytest -q -p no:cacheprovider --tb=line tests/test_deploy_*.py; then")
    zweig = block[kopf : anker_index(block, "\nfi", kopf)]
    assert re.search(r"^\s*false\s*$", zweig, re.M), zweig
    anker_index(zweig, "!! Deploy-Tests rot -- Abbruch vor Bau und Auslieferung")
