"""Quellentest für docs/quellen/kang-laender/ (Ticket T-0800).

Zu jeder Pflicht-Aussage der Übersicht docs/KANG_ZUSTAENDIGKEIT_LAENDER.md liegt ein
Textabbild der zitierten Landesnorm im Repo, damit Prüfer an der Quelle prüfen können:
  (a) Für jede Datenzeile mit ``Pflicht`` ``ja`` oder ``nein`` sowie für Berlin und
      Mecklenburg-Vorpommern existiert ``docs/quellen/kang-laender/<slug>.md``
      (Landesname klein, Umlaute als ae/oe/ue, ß als ss, Leerzeichen als ``-``).
  (b) Jede Datei beginnt mit den Kopfzeilen ``Quelle: https://…``, ``Abgerufen: JJJJ-MM-TT``
      und ``Grundlage: <verkündeter Text | Beschlussempfehlung | Entwurf | Gesetzesbegründung>``
      und enthält danach mindestens 200 Zeichen Text.
  (c) Bei ``Pflicht`` ``ja``/``nein`` enthält die Datei die erste Paragrafenangabe aus
      ``Rechtsgrundlage`` (Muster ``§\\s*\\d+[a-z]?``, verglichen ohne Leerzeichen).

Läuft mit pytest oder direkt: ``python tests/test_kang_quellen.py``.
"""

from __future__ import annotations

import os
import re

WURZEL = os.path.join(os.path.dirname(__file__), "..", "..")
DOKU = os.path.join(WURZEL, "docs", "KANG_ZUSTAENDIGKEIT_LAENDER.md")
QUELLEN = os.path.join(WURZEL, "docs", "quellen", "kang-laender")
KOPF = "| Land | Rechtsgrundlage | Fundstelle | Zuständige Stelle | Pflicht | Stand |"
ZUSATZ = ("Berlin", "Mecklenburg-Vorpommern")
GRUNDLAGEN = (
    "verkündeter Text",
    "Beschlussempfehlung",
    "Entwurf",
    "Gesetzesbegründung",
    "Gesetzesbeschluss",
    "amtliche konsolidierte Fassung",
)


def _slug(land: str) -> str:
    s = land.lower()
    for alt, neu in (("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("ß", "ss"), (" ", "-")):
        s = s.replace(alt, neu)
    return s


def _datenzeilen() -> list[list[str]]:
    with open(DOKU, encoding="utf-8") as f:
        zeilen = [z.strip() for z in f]
    start = zeilen.index(KOPF)
    daten = []
    for z in zeilen[start + 2:]:
        if not z.startswith("|"):
            break
        daten.append([c.strip() for c in z.strip("|").split("|")])
    return daten


def _pflichtzeilen() -> list[list[str]]:
    return [z for z in _datenzeilen() if z[4] in ("ja", "nein")]


def _erwartete_laender() -> list[str]:
    laender = [z[0] for z in _pflichtzeilen()]
    return laender + [land for land in ZUSATZ if land not in laender]


def _lies(land: str) -> str:
    pfad = os.path.join(QUELLEN, _slug(land) + ".md")
    assert os.path.isfile(pfad), f"Textabbild fehlt: {pfad}"
    with open(pfad, encoding="utf-8") as f:
        return f.read()


def test_slug():
    assert _slug("Baden-Württemberg") == "baden-wuerttemberg"
    assert _slug("Mecklenburg-Vorpommern") == "mecklenburg-vorpommern"


def test_pflichtlaender_vorhanden():
    assert _pflichtzeilen(), "keine Zeile mit Pflicht ja/nein in der Übersicht"


def test_dateien_und_kopfzeilen():
    for land in _erwartete_laender():
        zeilen = _lies(land).split("\n")
        assert len(zeilen) > 3, land
        assert re.fullmatch(r"Quelle: https://\S+", zeilen[0].rstrip()), (land, zeilen[0])
        assert re.fullmatch(r"Abgerufen: \d{4}-\d{2}-\d{2}", zeilen[1].rstrip()), (land, zeilen[1])
        m = re.fullmatch(r"Grundlage: (.+)", zeilen[2].rstrip())
        assert m and m.group(1) in GRUNDLAGEN, (land, zeilen[2])
        rest = "\n".join(zeilen[3:]).strip()
        assert len(rest) >= 200, (land, len(rest))


def test_erste_paragrafenangabe_enthalten():
    for z in _pflichtzeilen():
        land, rechtsgrundlage = z[0], z[1]
        m = re.search(r"§\s*\d+[a-z]?", rechtsgrundlage)
        assert m, (land, rechtsgrundlage)
        erwartet = re.sub(r"\s+", "", m.group(0))
        text = re.sub(r"\s+", "", _lies(land))
        assert erwartet in text, (land, erwartet)


if __name__ == "__main__":
    test_slug()
    test_pflichtlaender_vorhanden()
    test_dateien_und_kopfzeilen()
    test_erste_paragrafenangabe_enthalten()
    print("ok")
