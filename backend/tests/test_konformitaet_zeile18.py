"""T-0765: Zeile 18 der Konformitäts-Checkliste ist auf 'erfüllt' gesetzt und gegen
die genannten Belege abgesichert.

Prüft wörtlich gegen docs/KONFORMITAET_CHECKLISTE.md:
- es gibt genau eine Zeile, die mit '| 18 |' beginnt,
- diese Zeile hat sieben Spalten,
- fünfte Spalte (Status) ist genau 'erfüllt',
- sechste Spalte (Fundstelle/Beleg) ist genau die fünf erwarteten Pfade,
- siebte Spalte (Lücke) ist genau der erwartete Satz,
- jeder der fünf genannten Pfade existiert als Datei im Repo.
"""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CHECKLISTE = REPO_ROOT / "docs" / "KONFORMITAET_CHECKLISTE.md"

ERWARTETE_BELEGE = (
    "backend/app/data/anpassungskapazitaet.py, "
    "backend/app/services/anpassungskapazitaet.py, "
    "backend/app/services/anpassungskapazitaet_markdown.py, "
    "backend/app/api/routes/anpassungskapazitaet.py, "
    "docs/ANPASSUNGSKAPAZITAET.md"
)
LUECKE = (
    "Keine Lücke im Produkt; der nach ISO 14091 optionale Schritt ist als "
    "Selbsteinschätzung der Kommune je Komponente und Reifegrad umgesetzt und im "
    "Bericht als optionaler Analyseschritt ausgewiesen."
)


def _zeile_18() -> str:
    zeilen = [
        zeile
        for zeile in CHECKLISTE.read_text(encoding="utf-8").splitlines()
        if zeile.startswith("| 18 |")
    ]
    assert len(zeilen) == 1, (
        f"Erwartet genau eine Zeile, die mit '| 18 |' beginnt, gefunden: {len(zeilen)}"
    )
    return zeilen[0]


def _spalten(zeile: str) -> list[str]:
    # Markdown-Tabellenzeile: führendes und abschließendes '|' erzeugen leere
    # Rand-Elemente beim Split, die wir verwerfen.
    teile = zeile.split("|")
    assert teile[0].strip() == ""
    assert teile[-1].strip() == ""
    return teile[1:-1]


def test_zeile_18_hat_sieben_spalten():
    spalten = _spalten(_zeile_18())
    assert len(spalten) == 7, f"Erwartet 7 Spalten, gefunden: {len(spalten)} -> {spalten}"


def test_zeile_18_status_ist_erfuellt():
    spalten = _spalten(_zeile_18())
    assert spalten[4].strip() == "erfüllt"


def test_zeile_18_beleg_ist_exakt():
    spalten = _spalten(_zeile_18())
    assert spalten[5].strip() == ERWARTETE_BELEGE


def test_zeile_18_luecke_ist_exakt():
    spalten = _spalten(_zeile_18())
    assert spalten[6].strip() == LUECKE


def test_zeile_18_belegte_pfade_existieren():
    pfade = [pfad.strip() for pfad in ERWARTETE_BELEGE.split(",")]
    assert len(pfade) == 5
    for pfad in pfade:
        datei = REPO_ROOT / pfad
        assert datei.is_file(), f"Beleg-Datei fehlt: {pfad}"
