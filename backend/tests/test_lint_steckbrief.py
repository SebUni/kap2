"""Test für T-0403: Der Methodik-Lint erkennt Steckbriefe und überspringt sie.

Anlass: `main()` in `backend/scripts/lint_methodik.py` bildet das Glob-Muster
`<nr>_*.md` bzw. `*.md` über `docs/methodik` und gibt jede Treffer-Datei an
`pruefe_bericht()`. Ein Steckbrief (Aufsichtsrats-Freigabe F-0030) fällt unter
beide Muster, hat aber sieben Abschnitte statt der neun Pflichtkapitel und eine
schlichte Parametertabelle statt Parameter-Blöcken — er würde also von jedem Lauf
für ein Format beanstandet, das so beschlossen ist.

Geprüft werden beide Richtungen an temporär angelegten Dateien:

1. Eine Datei, deren Name auf `_steckbrief.md` endet, wird von der
   Berichtsauswahl nicht als Euro-Bericht geprüft, erzeugt genau eine
   Ausgabezeile `UEBERSPRUNGEN (Steckbrief): …` und macht den Rückgabewert des
   Laufs nicht rot.
2. Eine Datei mit gewöhnlichem Berichtsnamen (`99_testrisiko.md`) durchläuft die
   Pflichtkapitel-Prüfung unverändert.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import lint_methodik  # noqa: E402

STECKBRIEF = """# Steckbrief #62 Stadtklima / Wärmeinseln

## 1 Kurzbeschreibung
Kurzformat nach F-0030: sieben Abschnitte, keine Pflichtkapitel.

## 2 Parameter
| Parameter | Wert | Quelle |
| --- | --- | --- |
| Beispiel | 1,0 | [1] |
"""

BERICHT = """# Testrisiko #99

## 1 Wirkungskette & Knoten-Bilanz
zu kurz
"""


def _lauf(tmp_path, monkeypatch, dateien: dict[str, str], argv: list[str],
          capsys):
    """Lint-Lauf gegen ein temporäres Methodik-Verzeichnis."""
    for name, inhalt in dateien.items():
        (tmp_path / name).write_text(inhalt, encoding="utf-8")
    monkeypatch.setattr(lint_methodik, "DOCS", str(tmp_path))
    monkeypatch.setattr(sys, "argv", ["lint_methodik.py", *argv])
    code = lint_methodik.main()
    return code, capsys.readouterr().out


def test_steckbrief_wird_uebersprungen_und_bleibt_gruen(tmp_path, monkeypatch,
                                                        capsys):
    code, ausgabe = _lauf(
        tmp_path, monkeypatch,
        {"62_stadtklima_waermeinseln_steckbrief.md": STECKBRIEF}, [], capsys)

    uebersprungen = [z for z in ausgabe.split("\n")
                     if z.startswith("UEBERSPRUNGEN (Steckbrief):")]
    assert len(uebersprungen) == 1
    assert "62_stadtklima_waermeinseln_steckbrief.md" in uebersprungen[0]
    # Nicht als Euro-Bericht geprüft: kein Prüfkopf, keine Beanstandung.
    assert "=== #62" not in ausgabe
    assert "Pflichtkapitel 1" not in ausgabe
    assert "ROT" not in ausgabe
    assert code == 0


def test_steckbrief_faellt_auch_unter_dem_nummern_muster_nicht_in_die_pruefung(
        tmp_path, monkeypatch, capsys):
    """Auch der Aufruf mit Risikonummer (`<nr>_*.md`) trifft den Steckbrief."""
    code, ausgabe = _lauf(
        tmp_path, monkeypatch,
        {"62_stadtklima_waermeinseln_steckbrief.md": STECKBRIEF}, ["62"],
        capsys)

    assert len([z for z in ausgabe.split("\n")
                if z.startswith("UEBERSPRUNGEN (Steckbrief):")]) == 1
    assert code == 0


def test_gewoehnlicher_bericht_durchlaeuft_die_pflichtkapitel_pruefung(
        tmp_path, monkeypatch, capsys):
    code, ausgabe = _lauf(tmp_path, monkeypatch,
                          {"99_testrisiko.md": BERICHT}, ["99"], capsys)

    assert "UEBERSPRUNGEN (Steckbrief):" not in ausgabe
    assert "99_testrisiko.md" in ausgabe
    # Pflichtkapitel-Prüfung unverändert: Kapitel 1 ist unter der Schwelle,
    # die Kapitel 2–8 fehlen ganz (Kapitel 9 ist nach §4 optional).
    assert "Pflichtkapitel 1 (Wirkungskette & Knoten-Bilanz) gefüllt" in ausgabe
    for n in range(2, 9):
        assert f"Pflichtkapitel {n}: Überschrift nicht gefunden" in ausgabe
    assert code == 1


def test_erkennung_nur_am_dateinamen_suffix():
    """Kein inhaltliches Raten — allein das Suffix entscheidet."""
    assert lint_methodik.ist_steckbrief("/x/62_stadtklima_steckbrief.md")
    assert not lint_methodik.ist_steckbrief("/x/62_stadtklima.md")
    assert not lint_methodik.ist_steckbrief("/x/steckbrief_62.md")


if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main([__file__, "-q"]))
