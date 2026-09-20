"""Test des Methodendokuments zum Nachweis nach § 8 Abs. 1 KAnG (Ticket T-0464,
Teil 4 des Nachweises, Vorhaben T-0445).

``docs/NACHWEIS_FACHUEBERGREIFEND_KANG.md`` liegt außerhalb ``docs/methodik/``
und wird von keinem der Lints unter ``test_lint_*.py`` erfasst — dieser Test ist
sein einziges Prüfmittel. Deckt ab:

  (a) Die fünf Überschriften stehen genau einmal:
      '## Rechtsgrundlage und Adressat', '## Was das Produkt prüft',
      '## Was dem Träger öffentlicher Aufgaben überlassen bleibt',
      '## Felder des Nachweises', '## Modellgrenze'.
  (b) Die Menge der Werte in der ersten Spalte der Tabelle unter
      '## Felder des Nachweises' ist identisch mit der Vereinigung: den
      Schlüsseln des Rückgabewertes von ``nachweis_fachuebergreifend({}, [])``,
      den Schlüsseln eines beliebigen Eintrags aus dessen ``handlungsfelder``
      und den Schlüsseln aus dessen ``zusammenfassung``.
  (c) '## Rechtsgrundlage und Adressat' enthält
      'https://www.gesetze-im-internet.de/kang/__8.html'.
  (d) '## Was dem Träger öffentlicher Aufgaben überlassen bleibt' enthält den
      Wert von ``abgrenzung`` als zusammenhängende Teilzeichenkette.

Läuft mit pytest oder direkt: ``python tests/test_nachweis_fachuebergreifend_doku.py``.
"""

from __future__ import annotations

import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.services.kang_beruecksichtigung import (  # noqa: E402
    nachweis_fachuebergreifend,
)

DOKUMENT_PFAD = os.path.join(
    os.path.dirname(__file__), "..", "..", "docs", "NACHWEIS_FACHUEBERGREIFEND_KANG.md"
)

UEBERSCHRIFTEN = [
    "## Rechtsgrundlage und Adressat",
    "## Was das Produkt prüft",
    "## Was dem Träger öffentlicher Aufgaben überlassen bleibt",
    "## Felder des Nachweises",
    "## Modellgrenze",
]


def _dokument_text() -> str:
    with open(DOKUMENT_PFAD, encoding="utf-8") as f:
        return f.read()


def _abschnitt(text: str, ueberschrift: str) -> str:
    start = text.index(ueberschrift) + len(ueberschrift)
    rest = text[start:]
    naechste = re.search(r"^## ", rest, flags=re.MULTILINE)
    if naechste is None:
        return rest
    return rest[: naechste.start()]


def _erwartete_feldnamen() -> set[str]:
    nachweis = nachweis_fachuebergreifend({}, [])
    felder = set(nachweis.keys())
    assert nachweis["handlungsfelder"], "Testvoraussetzung: handlungsfelder nicht leer"
    felder |= set(nachweis["handlungsfelder"][0].keys())
    felder |= set(nachweis["zusammenfassung"].keys())
    return felder


def _erste_spalte_tabelle(abschnitt: str) -> set[str]:
    zeilen = [z for z in abschnitt.splitlines() if z.strip().startswith("|")]
    # Kopfzeile + Trennzeile abziehen.
    if len(zeilen) >= 2 and set(zeilen[1].replace("|", "").replace(" ", "")) <= {"-", ":"}:
        datenzeilen = zeilen[2:]
    else:
        datenzeilen = zeilen[1:] if zeilen else []
    namen = set()
    for zeile in datenzeilen:
        spalten = [s.strip() for s in zeile.strip().strip("|").split("|")]
        namen.add(spalten[0].strip("`"))
    return namen


# ── (a) Überschriften: genau einmal ─────────────────────────────────────────────

def test_ueberschriften_genau_einmal():
    text = _dokument_text()
    for ueberschrift in UEBERSCHRIFTEN:
        assert text.count(ueberschrift) == 1, ueberschrift


# ── (b) Feldtabelle gegen tatsächliche Schlüssel ────────────────────────────────

def test_feldtabelle_entspricht_tatsaechlichen_schluesseln():
    text = _dokument_text()
    abschnitt = _abschnitt(text, "## Felder des Nachweises")
    tabellenfelder = _erste_spalte_tabelle(abschnitt)
    assert tabellenfelder == _erwartete_feldnamen()


# ── (c) Rechtsgrundlage enthält die Gesetzesquelle ──────────────────────────────

def test_rechtsgrundlage_enthaelt_gesetzesquelle():
    text = _dokument_text()
    abschnitt = _abschnitt(text, "## Rechtsgrundlage und Adressat")
    assert "https://www.gesetze-im-internet.de/kang/__8.html" in abschnitt


# ── (d) Abschnitt zur Abgrenzung enthält den Abgrenzungstext ────────────────────

def test_abgrenzungsabschnitt_enthaelt_abgrenzungstext():
    nachweis = nachweis_fachuebergreifend({}, [])
    text = _dokument_text()
    abschnitt = _abschnitt(text, "## Was dem Träger öffentlicher Aufgaben überlassen bleibt")
    assert nachweis["abgrenzung"] in abschnitt


if __name__ == "__main__":
    import pytest

    raise SystemExit(pytest.main([__file__, "-v"]))
