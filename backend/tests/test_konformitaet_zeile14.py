"""T-0753: Zeile 14 der Konformitäts-Checkliste ist auf 'erfüllt' gesetzt und gegen
die genannten Belege abgesichert.

Prüft wörtlich gegen docs/KONFORMITAET_CHECKLISTE.md:
- es gibt genau eine Zeile, die mit '| 14 |' beginnt,
- diese Zeile hat sieben Spalten,
- fünfte Spalte (Status) ist genau 'erfüllt',
- sechste Spalte (Fundstelle/Beleg) ist genau die vier erwarteten Pfade,
- siebte Spalte (Lücke) ist genau '—',
- jeder der vier genannten Pfade existiert als Datei im Repo.
"""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CHECKLISTE = REPO_ROOT / "docs" / "KONFORMITAET_CHECKLISTE.md"

ERWARTETE_BELEGE = (
    "docs/KANG_ZUSTAENDIGKEIT_LAENDER.md, "
    "backend/app/data/kang_zustaendigkeit.py, "
    "backend/app/api/routes/kommune.py, "
    "frontend/src/components/dashboard/KangZustaendigkeit.tsx"
)


def _zeile_14() -> str:
    zeilen = [
        zeile
        for zeile in CHECKLISTE.read_text(encoding="utf-8").splitlines()
        if zeile.startswith("| 14 |")
    ]
    assert len(zeilen) == 1, (
        f"Erwartet genau eine Zeile, die mit '| 14 |' beginnt, gefunden: {len(zeilen)}"
    )
    return zeilen[0]


def _spalten(zeile: str) -> list[str]:
    # Markdown-Tabellenzeile: führendes und abschließendes '|' erzeugen leere
    # Rand-Elemente beim Split, die wir verwerfen.
    teile = zeile.split("|")
    assert teile[0].strip() == ""
    assert teile[-1].strip() == ""
    return teile[1:-1]


def test_zeile_14_hat_sieben_spalten():
    spalten = _spalten(_zeile_14())
    assert len(spalten) == 7, f"Erwartet 7 Spalten, gefunden: {len(spalten)} -> {spalten}"


def test_zeile_14_status_ist_erfuellt():
    spalten = _spalten(_zeile_14())
    assert spalten[4].strip() == "erfüllt"


def test_zeile_14_beleg_ist_exakt():
    spalten = _spalten(_zeile_14())
    assert spalten[5].strip() == ERWARTETE_BELEGE


def test_zeile_14_luecke_ist_leer():
    spalten = _spalten(_zeile_14())
    assert spalten[6].strip() == "—"


def test_zeile_14_belegte_pfade_existieren():
    pfade = [pfad.strip() for pfad in ERWARTETE_BELEGE.split(",")]
    assert len(pfade) == 4
    for pfad in pfade:
        datei = REPO_ROOT / pfad
        assert datei.is_file(), f"Beleg-Datei fehlt: {pfad}"
