"""Tests gegen docs/QUERVERBINDUNGEN_KLIMAWIRKUNGEN.md (T-0458).

Prüft das Analysedokument zu Quellenlage, Netzrollen und Modellgrenze der
KWRA-Querverbindungen wörtlich gegen das Abnahmekriterium: vorhandene Überschriften,
Zeilenzahlen der drei Tabellen und Übereinstimmung der Netzrollen-KWRA-IDs mit dem
Datenmodul ``app.data.kwra_querverbindungen``.
"""
from pathlib import Path

from app.data import kwra_querverbindungen as k

DOKU_PFAD = Path(__file__).resolve().parents[2] / "docs" / "QUERVERBINDUNGEN_KLIMAWIRKUNGEN.md"

ERWARTETE_UEBERSCHRIFTEN = [
    "## Quellenlage",
    "## Netzrollen",
    "## Benannte Einzelbeziehungen",
    "## Querverbindungen zwischen den Systembereichen",
    "## Anwendung auf den Produktkatalog",
    "## Modellgrenze",
]


def _text() -> str:
    return DOKU_PFAD.read_text(encoding="utf-8")


def _abschnitt(text: str, ueberschrift: str) -> str:
    """Liefert den Text zwischen ``ueberschrift`` (Ebene ##) und der nächsten Ebene-2-Überschrift."""
    zeilen = text.splitlines()
    start = None
    for i, zeile in enumerate(zeilen):
        if zeile.strip() == ueberschrift:
            start = i + 1
            break
    assert start is not None, f"Überschrift nicht gefunden: {ueberschrift}"
    ende = len(zeilen)
    for j in range(start, len(zeilen)):
        if zeilen[j].startswith("## ") and zeilen[j].strip() != ueberschrift:
            ende = j
            break
    return "\n".join(zeilen[start:ende])


def _tabellenzeilen(abschnittstext: str) -> list[list[str]]:
    """Extrahiert die Datenzeilen der (ersten) Markdown-Tabelle im Abschnitt.

    Überspringt Kopfzeile und Trennzeile (``|---|---|...``).
    """
    zeilen = [z for z in abschnittstext.splitlines() if z.strip().startswith("|")]
    assert zeilen, "keine Markdown-Tabelle im Abschnitt gefunden"
    datenzeilen = []
    kopf_gesehen = False
    trenner_gesehen = False
    for zeile in zeilen:
        zellen = [z.strip() for z in zeile.strip().strip("|").split("|")]
        if not kopf_gesehen:
            kopf_gesehen = True
            continue
        if not trenner_gesehen and all(set(z) <= set("-: ") for z in zellen):
            trenner_gesehen = True
            continue
        datenzeilen.append(zellen)
    return datenzeilen


# ── Überschriften ─────────────────────────────────────────────────────────────

def test_ueberschriften_vorhanden():
    text = _text()
    for ueberschrift in ERWARTETE_UEBERSCHRIFTEN:
        assert ueberschrift in text, f"fehlt: {ueberschrift}"


# ── Netzrollen ────────────────────────────────────────────────────────────────

def test_netzrollen_tabelle_27_datenzeilen():
    abschnitt = _abschnitt(_text(), "## Netzrollen")
    zeilen = _tabellenzeilen(abschnitt)
    assert len(zeilen) == 27
    assert len(zeilen) == len(k.NETZROLLEN)


def test_netzrollen_ids_identisch_mit_datenmodul():
    abschnitt = _abschnitt(_text(), "## Netzrollen")
    zeilen = _tabellenzeilen(abschnitt)
    ids_doku = {int(zeile[0]) for zeile in zeilen}
    ids_modul = {e["kwra_id"] for e in k.NETZROLLEN}
    assert ids_doku == ids_modul


# ── Benannte Einzelbeziehungen ────────────────────────────────────────────────

def test_benannte_beziehungen_tabelle_27_datenzeilen():
    abschnitt = _abschnitt(_text(), "## Benannte Einzelbeziehungen")
    zeilen = _tabellenzeilen(abschnitt)
    assert len(zeilen) == 27
    assert len(zeilen) == len(k.BENANNTE_BEZIEHUNGEN)


# ── Querverbindungen zwischen den Systembereichen ────────────────────────────

def test_systembereiche_tabelle_5_datenzeilen():
    abschnitt = _abschnitt(_text(), "## Querverbindungen zwischen den Systembereichen")
    zeilen = _tabellenzeilen(abschnitt)
    assert len(zeilen) == 5


# ── Annahme der Auswertung und Einordnung ─────────────────────────────────────

def test_abschnitt_annahme_und_einordnung_nennt_aussagen():
    """T-0939 (A4, A10): Annahme (S. 82), Cluster-Einordnung und Kaskadeneffekte stehen in der Doku."""
    abschnitt = _abschnitt(_text(), "## Annahme der Auswertung und Einordnung")
    assert "Annahme der Auswertung (S. 82)" in abschnitt
    assert "nachgelagerten" in abschnitt
    assert "Cluster Wasser und Land" in abschnitt
    assert "Kaskadeneffekte" in abschnitt
    assert "AUSSAGEN" in abschnitt


# ── Quellenlage ───────────────────────────────────────────────────────────────

def test_quellenlage_enthaelt_gesamtzahl_und_pdf():
    abschnitt = _abschnitt(_text(), "## Quellenlage")
    assert "257" in abschnitt
    assert "kwra2021_teilbericht_6_integrierte_auswertung_bf_211027_0.pdf" in abschnitt
