"""Rechenkette und „eine Methodik“ im Lint (Aufsichtsrat, 24.09.2026; Aufgabe §4, §8 E1, Fortschreibung 7).

Jeder Methodik-Bericht beginnt Kapitel 3 mit der Rechenkette von der amtlichen Quelle bis zum Euro-Betrag — je Ebene
Rechenschritt, Zahl für eine Beispielkommune und Quelle, höchstens zehn Ebenen (mehr nur begründet), nachgerechnet von
einem Beispiel-Block. Ein Kapitel 9 (Ansatz-Vergleich) gibt es nicht mehr. Die Tests decken beide Richtungen ab.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from lint_methodik import Lint, ansatzkapitel_entfaellt, rechenkette  # noqa: E402

BLOCK = "```python test: rechenkette_95\nwert = 12400 * 0.021\nassert round(wert) == 260\n```\n"


def _kette(zeilen: list[tuple[str, str, str, str]], *, kopf: str = "Wert (Beispielkommune Leipzig)", davor: str = "",
           block: str = BLOCK, zusatz: str = "") -> str:
    tabelle = [f"| Ebene | Rechenschritt | {kopf} | Quelle |", "|---|---|---|---|"]
    tabelle += [f"| {a} | {b} | {c} | {d} |" for a, b, c, d in zeilen]
    return ("## 2 Evidenz-Register\nText.\n\n## 3 Modell\n\n" + davor + "### 3.0 Rechenkette\n\n" + "\n".join(tabelle)
            + "\n\n" + zusatz + block + "\n### 3.1 Formeln\n\nText.\n\n## 4 Kalibrierung\n")


GUT = [("1", "Einwohner ab 75 Jahren", "12.400", "Zensus 2022, Tabelle 1000A-2002"),
       ("2", "× zusätzliche Sterbefälle je Einwohner und Jahr", "× 0,021", "Register 95-S152-01"),
       ("3", "= zusätzliche Sterbefälle je Jahr", "= 260", "Rechnung"),
       ("4", "× Kosten je Fall", "× 4.600 €", "UBA MK 4.0"),
       ("5", "= bewerteter Schaden (Konto K1) je Jahr", "= 1,2 Mio. €", "Rechnung")]


def _rot(src: str) -> list[str]:
    lint = Lint()
    rechenkette(src, lint)
    return lint.fehler


def test_vollstaendige_kette_bleibt_gruen():
    assert _rot(_kette(GUT)) == []


def test_fehlender_abschnitt_wird_rot():
    fehler = _rot("## 3 Modell\n\n### 3.1 Formeln\n\nText.\n\n## 4 Kalibrierung\n")
    assert fehler and "fehlt in Kapitel 3" in fehler[0]


def test_kette_muss_am_anfang_stehen():
    assert any("am Anfang von Kapitel 3" in f for f in _rot(_kette(GUT, davor="### 3.1 Vorab\n\nText.\n\n")))


def test_ebene_ohne_quelle_oder_wert_wird_rot():
    zeilen = list(GUT)
    zeilen[1] = ("2", "× zusätzliche Sterbefälle", "× 0,021", "")
    zeilen[2] = ("3", "= zusätzliche Sterbefälle", "offen", "Rechnung")
    fehler = _rot(_kette(zeilen))
    assert any("Ebene 2: Quelle" in f for f in fehler)
    assert any("Ebene 3: Wert" in f for f in fehler)


def test_kette_endet_beim_euro_betrag():
    assert any("Euro-Betrag" in f for f in _rot(_kette(GUT[:3])))


def test_mehr_als_zehn_ebenen_nur_begruendet():
    lang = [(str(i), f"Schritt {i}", f"{i},5", "Rechnung") for i in range(1, 12)] + [("12", "= Schaden", "= 3,4 Mio. €", "Rechnung")]
    assert any("mehr als 10 Ebenen" in f for f in _rot(_kette(lang)))
    begruendet = _kette(lang, zusatz="**Mehr als zehn Ebenen:** Die Altersbänder einzeln zu führen ist nötig, weil ein "
                                     "Mittelwert die hochbetagten Kommunen um ein Drittel unterschätzt.\n\n")
    assert _rot(begruendet) == []


def test_beispielkommune_und_beispielblock_sind_pflicht():
    fehler = _rot(_kette(GUT, kopf="Wert", block=""))
    assert any("Beispielkommune" in f for f in fehler)
    assert any("Beispiel-Block" in f for f in fehler)


def test_kapitel_9_entfaellt():
    lint = Lint()
    ansatzkapitel_entfaellt("## 8 Quellen\nText.\n\n## 9 Ansatz-Vergleich\nText.\n", lint)
    assert lint.fehler and "Entscheidungslog" in lint.fehler[0]
    lint = Lint()
    ansatzkapitel_entfaellt("## 8 Quellen\nText.\n\n## Entscheidungslog\nText.\n", lint)
    assert lint.fehler == []


if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main([__file__, "-q"]))
