"""Test für T-0902: `parameter_bloecke()` erkennt Kostensätze über die ganze
Einheit, und Kalibrieranker dürfen einen eigenen Preisstand tragen.

Anlass: Der Lint prüfte nur das erste Wort der Einheit auf die Zeichenfolge
`EUR`. Ein Block mit `einheit: "Mrd. €/a"` (oder `"Mrd. EUR/a"`) und
`preisstand: null` lief damit grün durch — ein Schlupfloch, über das ein
Kalibrieranker in fremdem Preisstand die Regel „Preisstand einheitlich“ umging.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from lint_methodik import Lint, parameter_bloecke  # noqa: E402


def _block(pid: str, einheit: str, preisstand: str, rolle: str | None = None,
           kennzeichnung: str = "quelle",
           abgeleitet_aus: str | None = None) -> str:
    zeilen = [
        "parameter:",
        f"  id: {pid}",
        "  wert: 1.0",
        f'  einheit: "{einheit}"',
        "  band: [1.0, 1.0]",
        "  herkunft: herleitung:§4.1",
        f"  kennzeichnung: {kennzeichnung}",
    ]
    if abgeleitet_aus is not None:
        zeilen.append(f"  abgeleitet_aus: {abgeleitet_aus}")
    if rolle:
        zeilen.append(f"  rolle: {rolle}")
    zeilen += [
        '  quelle: "Testquelle"',
        f"  preisstand: {preisstand}",
        "  bandzuordnung: [alle]",
        "  endpunkt: K3",
        "---",
    ]
    return "\n".join(zeilen) + "\n"


def _bericht(*bloecke: str) -> str:
    return "## 7 Parameter-Blöcke\n\n" + "".join(bloecke) + "\n## 8 Ende\n"


def _preisstand_fehler(src: str) -> list[str]:
    lint = Lint()
    parameter_bloecke(src, lint)
    return [f for f in lint.fehler if f.startswith("Preisstand")]


def test_a_euro_zeichen_nach_erstem_wort_ohne_preisstand_ist_rot():
    fehler = _preisstand_fehler(_bericht(_block("t.x", "Mrd. €/a", "null")))
    assert len(fehler) == 1
    assert fehler[0].startswith("Preisstand bei Kostensatz t.x")


def test_b_eur_nach_erstem_wort_ohne_preisstand_ist_rot():
    fehler = _preisstand_fehler(_bericht(_block("t.x", "Mrd. EUR/a", "null")))
    assert len(fehler) == 1
    assert fehler[0].startswith("Preisstand bei Kostensatz t.x")


def test_c_kalibrieranker_mit_eigenem_preisstand_ist_gruen():
    src = _bericht(
        _block("t.kosten", "EUR/Fall", "2026"),
        _block("t.anker", "Mrd. €2024/a", "2024", rolle="kalibrierung"),
    )
    assert _preisstand_fehler(src) == []


def test_d_abweichender_preisstand_ohne_kalibrierrolle_bleibt_rot():
    src = _bericht(
        _block("t.kosten", "EUR/Fall", "2026"),
        _block("t.anker", "Mrd. €2024/a", "2024"),
    )
    fehler = _preisstand_fehler(src)
    assert len(fehler) == 1
    assert fehler[0].startswith("Preisstand einheitlich")


def test_einheit_ohne_euro_braucht_keinen_preisstand():
    assert _preisstand_fehler(_bericht(_block("t.y", "1/a", "null"))) == []


# T-0952: kennzeichnung kennt drei Werte, berechnet verlangt abgeleitet_aus.

def _kennzeichnung_fehler(src: str) -> list[str]:
    lint = Lint()
    parameter_bloecke(src, lint)
    return [f for f in lint.fehler
            if f.startswith(("Kennzeichnung", "abgeleitet_aus"))]


def test_e_berechnet_mit_abgeleitet_aus_ist_gruen():
    src = _bericht(
        _block("t.a", "1/a", "null"),
        _block("t.b", "1/a", "null", kennzeichnung="abschaetzung_kap3"),
        _block("t.c", "1/a", "null", kennzeichnung="berechnet",
               abgeleitet_aus="[t.a, t.b]"),
    )
    assert _kennzeichnung_fehler(src) == []


def test_f_berechnet_ohne_oder_mit_leerem_abgeleitet_aus_ist_rot():
    ohne = _kennzeichnung_fehler(_bericht(
        _block("t.c", "1/a", "null", kennzeichnung="berechnet")))
    assert len(ohne) == 1
    assert ohne[0].startswith("abgeleitet_aus bei berechnet t.c")
    for leer in ("[]", "[ ]"):
        fehler = _kennzeichnung_fehler(_bericht(
            _block("t.c", "1/a", "null", kennzeichnung="berechnet",
                   abgeleitet_aus=leer)))
        assert len(fehler) == 1
        assert fehler[0].startswith("abgeleitet_aus bei berechnet t.c")


def test_g_fremder_kennzeichnungswert_ist_rot():
    fehler = _kennzeichnung_fehler(_bericht(
        _block("t.d", "1/a", "null", kennzeichnung="schaetzung")))
    assert len(fehler) == 1
    assert fehler[0].startswith("Kennzeichnung t.d")


if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main([__file__, "-q"]))
