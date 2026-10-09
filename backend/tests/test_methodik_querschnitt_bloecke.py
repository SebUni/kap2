"""Führt die Python-Blöcke der Querschnittsdateien aus und vergleicht ihre dokumentierte Ausgabe (T-1851-ceo).

`lint_methodik.py` überspringt Querschnittsdateien; ohne diesen Test kippt ein Rechenblock unbemerkt.
Jeder Block ```python (auch ```python test: <name>) läuft in einem eigenen leeren Namensraum. Folgt ihm,
nur durch Leerzeilen oder höchstens eine Textzeile getrennt, ein Ausgabe-Block (``` oder ```text),
wird die Standardausgabe zeilenweise damit verglichen (Leerraum am Zeilenende zählt nicht).
"""
import contextlib
import glob
import io
import os
import re
import traceback

import pytest

_METHODIK = os.path.join(os.path.dirname(__file__), "..", "..", "docs", "methodik")
_DATEIEN = sorted(glob.glob(os.path.join(_METHODIK, "querschnitt_*.md")))
_KOPF_PYTHON = re.compile(r"^```python(\s.*)?$")


def _blockende(zeilen, start):
    """Index der schließenden ```-Zeile zum Block, der bei `start` (Zeile nach dem Kopf) beginnt."""
    i = start
    while i < len(zeilen) and zeilen[i].rstrip() != "```":
        i += 1
    return i


def _bloecke(zeilen):
    """Liefert (kopfzeile_index, code, ausgabe_zeilen oder None) je Python-Block."""
    i = 0
    while i < len(zeilen):
        if not _KOPF_PYTHON.match(zeilen[i].rstrip()):
            i += 1
            continue
        kopf = i
        ende = _blockende(zeilen, i + 1)
        code = "\n".join(zeilen[i + 1:ende])
        j = ende + 1
        while j < len(zeilen) and not zeilen[j].strip():
            j += 1
        if j < len(zeilen) and not zeilen[j].startswith("```"):  # höchstens ein Textabsatz (Zeilenumbruch im Satz erlaubt)
            while j < len(zeilen) and zeilen[j].strip() and not zeilen[j].startswith("```"):
                j += 1
            while j < len(zeilen) and not zeilen[j].strip():
                j += 1
        ausgabe = None
        if j < len(zeilen) and zeilen[j].rstrip() in ("```", "```text"):
            e2 = _blockende(zeilen, j + 1)
            ausgabe = zeilen[j + 1:e2]
        yield kopf, code, ausgabe
        i = ende + 1


def bloecke_pruefen(pfad) -> list[str]:
    pfad = str(pfad)
    name = os.path.basename(pfad)
    with open(pfad, encoding="utf-8") as f:
        zeilen = f.read().split("\n")
    meldungen = []
    for kopf, code, soll in _bloecke(zeilen):
        zeile = kopf + 1
        puffer = io.StringIO()
        try:
            with contextlib.redirect_stdout(puffer):
                exec(compile(code, f"{name}:{zeile}", "exec"), {"__name__": "__block__"})
        except BaseException as exc:  # auch SystemExit und AssertionError melden
            letzte = traceback.format_exception_only(type(exc), exc)[-1].strip()
            stelle = ""
            for rahmen in traceback.extract_tb(exc.__traceback__):
                if rahmen.filename == f"{name}:{zeile}":  # tiefste Stelle im Block
                    codezeilen = code.split("\n")
                    stelle = (f", Datei-Zeile {zeile + rahmen.lineno}: "
                              f"{codezeilen[rahmen.lineno - 1].strip()}")
            meldungen.append(f"{name}, Zeile {zeile}: Ausnahme {letzte}{stelle}")
            continue
        if soll is None:
            continue
        ist_zeilen = puffer.getvalue().split("\n")
        if ist_zeilen and ist_zeilen[-1] == "":
            ist_zeilen.pop()
        ist_zeilen = [z.rstrip() for z in ist_zeilen]
        soll_zeilen = [z.rstrip() for z in soll]
        for n in range(max(len(ist_zeilen), len(soll_zeilen))):
            a = ist_zeilen[n] if n < len(ist_zeilen) else "<fehlt>"
            b = soll_zeilen[n] if n < len(soll_zeilen) else "<fehlt>"
            if a != b:
                meldungen.append(
                    f"{name}, Zeile {zeile}: Ausgabezeile {n + 1} weicht ab: dokumentiert {b!r}, erhalten {a!r}")
                break
    return meldungen


def _zaehle(pfad):
    with open(pfad, encoding="utf-8") as f:
        return sum(1 for _ in _bloecke(f.read().split("\n")))


@pytest.mark.parametrize("pfad", _DATEIEN, ids=[os.path.basename(p) for p in _DATEIEN])
def test_querschnitt_bloecke_laufen_und_stimmen(pfad):
    assert _zaehle(pfad) >= 1
    assert bloecke_pruefen(pfad) == []


def test_bestand_ist_nicht_leer():
    assert any(p.endswith("querschnitt_diskontrate.md") for p in _DATEIEN)


def test_rot_seite_geaenderte_ziffer_im_ausgabe_block(tmp_path):
    quelle = os.path.join(_METHODIK, "querschnitt_diskontrate.md")
    with open(quelle, encoding="utf-8") as f:
        text = f.read()
    marke = "Barwertfaktor 40,19"
    vorn, trenner, ausgabe = text.partition("```text\n")  # Ziffer nur im Ausgabe-Block ändern
    assert trenner and marke in ausgabe
    kopie = tmp_path / "querschnitt_diskontrate.md"
    kopie.write_text(vorn + trenner + ausgabe.replace(marke, "Barwertfaktor 40,18", 1), encoding="utf-8")
    meldungen = bloecke_pruefen(kopie)
    assert len(meldungen) == 1
    assert "querschnitt_diskontrate.md" in meldungen[0]
