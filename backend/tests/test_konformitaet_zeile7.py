"""T-0990: Zeile 7 der Konformitäts-Checkliste bleibt auf 'teilweise' und trägt die
berichtigte Fundstelle.

Prüft wörtlich gegen docs/KONFORMITAET_CHECKLISTE.md:
- es gibt genau eine Zeile, die mit '| 7 |' beginnt,
- diese Zeile hat sieben Spalten,
- fünfte Spalte (Status) ist genau 'teilweise',
- vierte Spalte (Fundstelle) ist genau der erwartete Wortlaut,
- siebte Spalte (Lücke) enthält 'Gegenprobe Zeile 7',
- jeder Pfad der sechsten Spalte existiert als Datei im Repo.
"""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CHECKLISTE = REPO_ROOT / "docs" / "KONFORMITAET_CHECKLISTE.md"

FUNDSTELLE = (
    "kwra2021_teilbericht_6_integrierte_auswertung_bf_211027_0.pdf, "
    "Kap. 6.2 (S. 140–145)"
)


def _zeile_7() -> str:
    zeilen = [
        zeile
        for zeile in CHECKLISTE.read_text(encoding="utf-8").splitlines()
        if zeile.startswith("| 7 |")
    ]
    assert len(zeilen) == 1, (
        f"Erwartet genau eine Zeile, die mit '| 7 |' beginnt, gefunden: {len(zeilen)}"
    )
    return zeilen[0]


def _spalten(zeile: str) -> list[str]:
    teile = zeile.split("|")
    assert teile[0].strip() == ""
    assert teile[-1].strip() == ""
    return teile[1:-1]


def test_zeile_7_hat_sieben_spalten():
    spalten = _spalten(_zeile_7())
    assert len(spalten) == 7, f"Erwartet 7 Spalten, gefunden: {len(spalten)} -> {spalten}"


def test_zeile_7_status_ist_teilweise():
    spalten = _spalten(_zeile_7())
    assert spalten[4].strip() == "teilweise"


def test_zeile_7_fundstelle_ist_exakt():
    spalten = _spalten(_zeile_7())
    assert spalten[3].strip() == FUNDSTELLE


def test_zeile_7_luecke_verweist_auf_gegenprobe():
    spalten = _spalten(_zeile_7())
    assert "Gegenprobe Zeile 7" in spalten[6]


def test_zeile_7_belegte_pfade_existieren():
    pfade = [pfad.strip() for pfad in _spalten(_zeile_7())[5].split(",")]
    assert pfade and all(pfade)
    for pfad in pfade:
        datei = REPO_ROOT / pfad
        assert datei.is_file(), f"Beleg-Datei fehlt: {pfad}"
