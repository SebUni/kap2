"""Zaunform „python test: <name>“ wird nur in der Exportkopie zum gewöhnlichen Python-Zaun."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

import methodik_zaeune as z  # noqa: E402

F = "`" * 3


def test_nur_der_test_zaun_wird_umgeschrieben():
    text = (
        "Text davor\n"
        f"{F}python test: beispiel_x\n"
        "a = 1\n"
        f"{F}\n"
        "\n"
        f"{F}python\n"
        "b = 2\n"
        f"{F}\n"
    )
    erwartet = text.replace(f"{F}python test: beispiel_x", f"{F}python")
    ergebnis = z.zaeune_normalisieren(text)
    assert ergebnis == erwartet
    assert f"{F}python test:" not in ergebnis
    assert ergebnis.count(f"{F}python\n") == 2
    assert len(ergebnis.splitlines()) == len(text.splitlines())


def test_ohne_test_zaun_bleibt_text_gleich():
    text = f"{F}python\nx = 1\n{F}\nkein python test: hier\n"
    assert z.zaeune_normalisieren(text) == text
