"""ist_querschnitt und die Trennung in berichtsauswahl (nur das Lint-Skript, keine Backend-Abhängigkeit)."""
import importlib.util
import os

_PFAD = os.path.join(os.path.dirname(__file__), "..", "scripts", "lint_methodik.py")
_spec = importlib.util.spec_from_file_location("lint_methodik", _PFAD)
lint = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(lint)


def test_ist_querschnitt_nur_am_praefix():
    assert lint.ist_querschnitt("docs/methodik/querschnitt_gewissheit.md")
    assert lint.ist_querschnitt("querschnitt_x.md")
    assert not lint.ist_querschnitt("docs/methodik/95_hitze.md")
    assert not lint.ist_querschnitt("docs/methodik/95_querschnitt_x.md")


def test_berichtsauswahl_trennt(tmp_path, monkeypatch):
    for n in ("95_hitze.md", "96_pollen.md", "97_x_steckbrief.md",
              "querschnitt_gewissheit.md", "querschnitt_x.pdf"):
        (tmp_path / n).write_text("x", encoding="utf-8")
    monkeypatch.setattr(lint, "DOCS", str(tmp_path))
    berichte, steckbriefe, quer = lint.berichtsauswahl()
    assert [os.path.basename(p) for p in berichte] == ["95_hitze.md", "96_pollen.md"]
    assert [os.path.basename(p) for p in steckbriefe] == ["97_x_steckbrief.md"]
    assert [os.path.basename(p) for p in quer] == ["querschnitt_gewissheit.md"]
    b, s, q = lint.berichtsauswahl("querschnitt")
    assert b == [] and s == [] and len(q) == 1
