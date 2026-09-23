"""Test der ausgebbaren Nachweisfassung in Markdown (Ticket T-0463, Teil 3 des
Nachweises nach § 8 Abs. 1 KAnG, Vorhaben T-0445).

Deckt ab:
  (a) Die fünf Überschriften stehen genau einmal, in genau dieser Reihenfolge:
      '# Nachweis der fachübergreifenden und integrierten Berücksichtigung
      (§ 8 Abs. 1 KAnG)', '## Betroffene Handlungsfelder',
      '## Offene Handlungsfelder', '## Integrierende Maßnahmen',
      '## Abgrenzung'.
  (b) Die Tabelle unter 'Betroffene Handlungsfelder' hat genau so viele
      Datenzeilen wie Einträge mit Status ungleich 'nicht betroffen'.
  (c) Die Tabelle unter 'Offene Handlungsfelder' hat genau so viele
      Datenzeilen wie ``zusammenfassung['offene_handlungsfelder']`` Einträge.
  (d) '## Abgrenzung' enthält den Wert von ``nachweis['abgrenzung']`` als
      zusammenhängende Teilzeichenkette.

Läuft mit pytest oder direkt: ``python tests/test_kang_nachweis_markdown.py``.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.services.kang_beruecksichtigung import (  # noqa: E402
    nachweis_fachuebergreifend,
)
from app.services.kang_nachweis_markdown import nachweis_markdown  # noqa: E402

UEBERSCHRIFTEN = [
    "# Nachweis der fachübergreifenden und integrierten Berücksichtigung (§ 8 Abs. 1 KAnG)",
    "## Betroffene Handlungsfelder",
    "## Offene Handlungsfelder",
    "## Integrierende Maßnahmen",
    "## Abgrenzung",
]


def _erzeuge_nachweis() -> dict:
    return nachweis_fachuebergreifend({"EXPECTED_ANNUAL_MORTALITY": 1000.0}, [])


def _abschnitt(text: str, ueberschrift: str, naechste: str | None) -> str:
    start = text.index(ueberschrift) + len(ueberschrift)
    if naechste is None:
        return text[start:]
    ende = text.index(naechste, start)
    return text[start:ende]


def _datenzeilen(tabellentext: str) -> list[str]:
    zeilen = [z for z in tabellentext.splitlines() if z.strip().startswith("|")]
    # Kopfzeile + Trennzeile abziehen, wenn vorhanden.
    if len(zeilen) >= 2 and set(zeilen[1].replace("|", "").replace(" ", "")) <= {"-", ":"}:
        return zeilen[2:]
    return zeilen[1:] if zeilen else []


# ── (a) Überschriften: genau einmal, genau diese Reihenfolge ───────────────────

def test_ueberschriften_genau_einmal_und_in_reihenfolge():
    nachweis = _erzeuge_nachweis()
    text = nachweis_markdown(nachweis)
    positionen = []
    for ueberschrift in UEBERSCHRIFTEN:
        assert text.count(ueberschrift) == 1, ueberschrift
        positionen.append(text.index(ueberschrift))
    assert positionen == sorted(positionen)


# ── (b) Tabelle 'Betroffene Handlungsfelder' ────────────────────────────────────

def test_tabelle_betroffene_handlungsfelder_hat_richtige_zeilenzahl():
    nachweis = _erzeuge_nachweis()
    text = nachweis_markdown(nachweis)
    erwartete_anzahl = len(
        [e for e in nachweis["handlungsfelder"] if e["status"] != "nicht betroffen"]
    )
    abschnitt = _abschnitt(
        text, "## Betroffene Handlungsfelder", "## Offene Handlungsfelder"
    )
    assert len(_datenzeilen(abschnitt)) == erwartete_anzahl
    assert erwartete_anzahl > 0  # Testdaten liefern mindestens einen betroffenen Fall.


# ── (c) Tabelle 'Offene Handlungsfelder' ────────────────────────────────────────

def test_tabelle_offene_handlungsfelder_hat_richtige_zeilenzahl():
    nachweis = _erzeuge_nachweis()
    text = nachweis_markdown(nachweis)
    erwartete_anzahl = len(nachweis["zusammenfassung"]["offene_handlungsfelder"])
    abschnitt = _abschnitt(
        text, "## Offene Handlungsfelder", "## Integrierende Maßnahmen"
    )
    assert len(_datenzeilen(abschnitt)) == erwartete_anzahl
    assert erwartete_anzahl > 0  # Testdaten liefern mindestens ein offenes Feld.


# ── (d) Abschnitt 'Abgrenzung' ───────────────────────────────────────────────────

def test_abschnitt_abgrenzung_enthaelt_abgrenzungstext():
    nachweis = _erzeuge_nachweis()
    text = nachweis_markdown(nachweis)
    abschnitt = _abschnitt(text, "## Abgrenzung", None)
    assert nachweis["abgrenzung"] in abschnitt


# ── (e) Deutsche Zahlenschreibweise und Verweis auf die Methodenbeschreibung ───

def test_deutsche_zahlenschreibweise_und_methodenverweis():
    nachweis = nachweis_fachuebergreifend({"EXPECTED_ANNUAL_MORTALITY": 1000.0}, [])
    text = nachweis_markdown(nachweis)
    assert "1.000,00" in text
    assert "1,000.00" not in text
    assert "NACHWEIS_FACHUEBERGREIFEND_KANG.md" in text


if __name__ == "__main__":
    import pytest

    raise SystemExit(pytest.main([__file__, "-v"]))
