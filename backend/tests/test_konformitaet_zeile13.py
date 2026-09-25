"""T-0465: Zeile 13 der Konformitäts-Checkliste ist gegen die genannten Belege
abgesichert. T-0927-cto: Nach der Gegenprobe am Text von § 8 Abs. 1 KAnG steht der
Status auf 'teilweise', und die Lücke ist benannt.

Prüft wörtlich gegen docs/KONFORMITAET_CHECKLISTE.md:
- es gibt genau eine Zeile, die mit '| 13 |' beginnt,
- diese Zeile hat sieben Spalten,
- fünfte Spalte (Status) ist genau 'teilweise',
- sechste Spalte (Fundstelle/Beleg) ist genau die vier erwarteten Pfade,
- siebte Spalte (Lücke) ist weder leer noch '—',
- jeder der vier genannten Pfade existiert als Datei im Repo.
"""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CHECKLISTE = REPO_ROOT / "docs" / "KONFORMITAET_CHECKLISTE.md"

ERWARTETE_BELEGE = (
    "backend/app/data/kang_handlungsfelder.py, "
    "backend/app/services/kang_beruecksichtigung.py, "
    "backend/app/services/kang_nachweis_markdown.py, "
    "docs/NACHWEIS_FACHUEBERGREIFEND_KANG.md"
)


def _zeile_13() -> str:
    zeilen = [
        zeile
        for zeile in CHECKLISTE.read_text(encoding="utf-8").splitlines()
        if zeile.startswith("| 13 |")
    ]
    assert len(zeilen) == 1, (
        f"Erwartet genau eine Zeile, die mit '| 13 |' beginnt, gefunden: {len(zeilen)}"
    )
    return zeilen[0]


def _spalten(zeile: str) -> list[str]:
    # Markdown-Tabellenzeile: führendes und abschließendes '|' erzeugen leere
    # Rand-Elemente beim Split, die wir verwerfen.
    teile = zeile.split("|")
    assert teile[0].strip() == ""
    assert teile[-1].strip() == ""
    return teile[1:-1]


def test_zeile_13_hat_sieben_spalten():
    spalten = _spalten(_zeile_13())
    assert len(spalten) == 7, f"Erwartet 7 Spalten, gefunden: {len(spalten)} -> {spalten}"


def test_zeile_13_status_ist_teilweise():
    # T-0927-cto: Gegenprobe am Text von § 8 Abs. 1 KAnG, Status auf 'teilweise'.
    spalten = _spalten(_zeile_13())
    assert spalten[4].strip() == "teilweise"


def test_zeile_13_beleg_ist_exakt():
    spalten = _spalten(_zeile_13())
    assert spalten[5].strip() == ERWARTETE_BELEGE


def test_zeile_13_luecke_ist_benannt():
    luecke = _spalten(_zeile_13())[6].strip()
    assert luecke not in ("", "—"), "Status 'teilweise' verlangt eine benannte Lücke"


def test_zeile_13_belegte_pfade_existieren():
    pfade = [pfad.strip() for pfad in ERWARTETE_BELEGE.split(",")]
    assert len(pfade) == 4
    for pfad in pfade:
        datei = REPO_ROOT / pfad
        assert datei.is_file(), f"Beleg-Datei fehlt: {pfad}"
