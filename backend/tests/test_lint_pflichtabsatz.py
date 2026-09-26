"""Test für T-1263: Pflichtabsatz „Risiko ohne (weitere) Anpassung“ in Kapitel 1.

Der Aufsichtsrat hat den Absatz am 25.09.2026 für jeden Methodik-Bericht beschlossen (T-1121). Rot wird der Lint,
wenn zwischen `## 1 …` und der nächsten `##`-Überschrift keine Zeile mit `### Risiko ohne (weitere) Anpassung`
beginnt — steht der Absatz nur in einem anderen Kapitel oder fehlt Kapitel 1, gilt er als fehlend. Kapitel 10 ff.
zählen nicht als Kapitel 1.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from lint_methodik import PFLICHTABSATZ_KAP1_ROT, Lint, pflichtabsatz_ohne_anpassung  # noqa: E402

ROT = "Pflichtabsatz „Risiko ohne (weitere) Anpassung“ fehlt in Kapitel 1"


def _lauf(src: str) -> Lint:
    lint = Lint()
    pflichtabsatz_ohne_anpassung(src, lint)
    return lint


def test_rot_text_woertlich():
    assert PFLICHTABSATZ_KAP1_ROT == ROT


def test_absatz_in_kapitel_1_gruen():
    src = "## 1 Wirkungskette\nText\n### Knoten-Bilanz\nx\n### Risiko ohne (weitere) Anpassung\nText\n## 2 Evidenz\n"
    assert _lauf(src).fehler == []


def test_absatz_fehlt_rot():
    src = "## 1 Wirkungskette\nText\n### Knoten-Bilanz\nx\n## 2 Evidenz\n"
    assert _lauf(src).fehler == [ROT]


def test_absatz_nur_in_anderem_kapitel_rot():
    src = "## 1 Wirkungskette\nText\n## 2 Evidenz\n### Risiko ohne (weitere) Anpassung\nText\n"
    assert _lauf(src).fehler == [ROT]


def test_kapitel_10_ist_nicht_kapitel_1():
    src = "## 10 Anhang\n### Risiko ohne (weitere) Anpassung\nText\n## 1 Wirkungskette\nText\n## 2 Evidenz\n"
    assert _lauf(src).fehler == [ROT]


def test_ohne_kapitel_1_rot():
    assert _lauf("## 2 Evidenz\n### Risiko ohne (weitere) Anpassung\n").fehler == [ROT]


if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main([__file__, "-q"]))
