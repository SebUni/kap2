"""Formtest für docs/KANG_ZUSTAENDIGKEIT_LAENDER.md (Ticket T-0750, Vorhaben T-0664).

Prüft die Tabelle der Zuständigkeiten nach § 12 Abs. 1 KAnG:
  (a) Kopfzeile ``| Land | Rechtsgrundlage | Fundstelle | Zuständige Stelle | Pflicht | Stand |``.
  (b) Die ersten Zellen der Datenzeilen sind genau ``set(BUNDESLAENDER)``, jedes Land einmal.
  (c) Jede Datenzeile hat sechs Zellen; ``Stand`` passt auf ``^\\d{4}-\\d{2}-\\d{2}$``.
  (d) ``Pflicht`` ist ``ja``/``nein`` (dann ``§`` in ``Rechtsgrundlage`` und ``Fundstelle``
      beginnt mit ``https://``) oder ``keine Bestimmung getroffen`` (dann lautet
      ``Rechtsgrundlage`` wörtlich ``keine Bestimmung getroffen, Stand <Stand>``).

Läuft mit pytest oder direkt: ``python tests/test_kang_zustaendigkeit_doku.py``.
"""

from __future__ import annotations

import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.services.osm_service import BUNDESLAENDER  # noqa: E402

DOKU = os.path.join(
    os.path.dirname(__file__), "..", "..", "docs", "KANG_ZUSTAENDIGKEIT_LAENDER.md"
)
KOPF = "| Land | Rechtsgrundlage | Fundstelle | Zuständige Stelle | Pflicht | Stand |"
KEINE = "keine Bestimmung getroffen"


def _zellen(zeile: str) -> list[str]:
    return [z.strip() for z in zeile.strip().strip("|").split("|")]


def _datenzeilen() -> list[list[str]]:
    with open(DOKU, encoding="utf-8") as f:
        zeilen = [z.rstrip("\n") for z in f]
    assert KOPF in [z.strip() for z in zeilen], "Tabellenkopf fehlt"
    start = [z.strip() for z in zeilen].index(KOPF)
    trenner = zeilen[start + 1].strip()
    assert re.fullmatch(r"\|(\s*:?-+:?\s*\|)+", trenner), "Trennzeile fehlt"
    daten = []
    for z in zeilen[start + 2:]:
        if not z.strip().startswith("|"):
            break
        daten.append(_zellen(z))
    return daten


def test_laender_genau_einmal():
    laender = [z[0] for z in _datenzeilen()]
    assert set(laender) == set(BUNDESLAENDER)
    assert len(laender) == len(set(laender))


def test_zeilenform():
    for z in _datenzeilen():
        assert len(z) == 6, z
        land, rechtsgrundlage, fundstelle, _stelle, pflicht, stand = z
        assert re.fullmatch(r"\d{4}-\d{2}-\d{2}", stand), (land, stand)
        if pflicht in ("ja", "nein"):
            assert "§" in rechtsgrundlage, land
            assert fundstelle.startswith("https://"), land
        else:
            assert pflicht == KEINE, (land, pflicht)
            assert rechtsgrundlage == f"{KEINE}, Stand {stand}", land


if __name__ == "__main__":
    test_laender_genau_einmal()
    test_zeilenform()
    print("ok")
