"""T-0460, fortgeschrieben mit T-0741: Zeile 9 der Konformitäts-Checkliste ist gegen
die genannten Belege abgesichert.

T-0460 hatte Zeile 9 auf 'erfüllt' gesetzt. Die Gegenprobe gegen KWRA 2021,
Teilbericht 6, Kap. 3.4 (T-0741, Abschnitt „Gegenprobe Zeile 9“ in der Checkliste)
hat ergeben, dass die vier Belege die Anforderung nur teilweise tragen; Status und
Lücke wurden deshalb auf 'teilweise' bzw. eine ausformulierte Lücke umgestellt.

Prüft wörtlich gegen docs/KONFORMITAET_CHECKLISTE.md:
- es gibt genau eine Zeile, die mit '| 9 |' beginnt,
- diese Zeile hat sieben Spalten,
- fünfte Spalte (Status) ist genau 'teilweise',
- sechste Spalte (Fundstelle/Beleg) ist genau die vier erwarteten Pfade,
- siebte Spalte (Lücke) ist nicht leer und nicht '—',
- jeder der vier genannten Pfade existiert als Datei im Repo.
"""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CHECKLISTE = REPO_ROOT / "docs" / "KONFORMITAET_CHECKLISTE.md"

ERWARTETE_BELEGE = (
    "backend/app/data/kwra_querverbindungen.py, "
    "backend/app/services/querverbindungen.py, "
    "docs/QUERVERBINDUNGEN_KLIMAWIRKUNGEN.md, "
    "frontend/src/components/dashboard/RiskInteractionSection.tsx"
)


def _zeile_9() -> str:
    zeilen = [
        zeile
        for zeile in CHECKLISTE.read_text(encoding="utf-8").splitlines()
        if zeile.startswith("| 9 |")
    ]
    assert len(zeilen) == 1, (
        f"Erwartet genau eine Zeile, die mit '| 9 |' beginnt, gefunden: {len(zeilen)}"
    )
    return zeilen[0]


def _spalten(zeile: str) -> list[str]:
    # Markdown-Tabellenzeile: führendes und abschließendes '|' erzeugen leere
    # Rand-Elemente beim Split, die wir verwerfen.
    teile = zeile.split("|")
    assert teile[0].strip() == ""
    assert teile[-1].strip() == ""
    return teile[1:-1]


def test_zeile_9_hat_sieben_spalten():
    spalten = _spalten(_zeile_9())
    assert len(spalten) == 7, f"Erwartet 7 Spalten, gefunden: {len(spalten)} -> {spalten}"


def test_zeile_9_status_ist_teilweise():
    spalten = _spalten(_zeile_9())
    assert spalten[4].strip() == "teilweise"


def test_zeile_9_beleg_ist_exakt():
    spalten = _spalten(_zeile_9())
    assert spalten[5].strip() == ERWARTETE_BELEGE


def test_zeile_9_luecke_ist_benannt():
    luecke = _spalten(_zeile_9())[6].strip()
    assert luecke not in ("", "—"), "Status 'teilweise' verlangt eine benannte Lücke"


def test_zeile_9_belegte_pfade_existieren():
    pfade = [pfad.strip() for pfad in ERWARTETE_BELEGE.split(",")]
    assert len(pfade) == 4
    for pfad in pfade:
        datei = REPO_ROOT / pfad
        assert datei.is_file(), f"Beleg-Datei fehlt: {pfad}"
