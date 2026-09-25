"""T-0759: Zeile 16 der Konformitäts-Checkliste gegen die genannten Belege
abgesichert; seit der Gegenprobe T-0928-cto steht sie auf 'teilweise'.

Prüft wörtlich gegen docs/KONFORMITAET_CHECKLISTE.md:
- es gibt genau eine Zeile, die mit '| 16 |' beginnt,
- diese Zeile hat sieben Spalten,
- fünfte Spalte (Status) ist genau 'teilweise',
- sechste Spalte (Fundstelle/Beleg) ist genau die vier erwarteten Pfade,
- siebte Spalte (Lücke) ist genau der erwartete Satz,
- jeder der vier genannten Pfade existiert als Datei im Repo.
"""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CHECKLISTE = REPO_ROOT / "docs" / "KONFORMITAET_CHECKLISTE.md"

ERWARTETE_BELEGE = (
    "backend/app/data/bestandsaufnahme.py, "
    "backend/app/services/bestandsaufnahme_service.py, "
    "backend/app/services/bestandsaufnahme_markdown.py, "
    "docs/BESTANDSAUFNAHME.md"
)
ERWARTETE_LUECKE = (
    "Die Bestandsaufnahme erfasst vulnerable Personengruppen und klimasensible "
    "Strukturen nur zum Teil: vier von sieben Personengruppen und "
    "Kindertagesstätten und Schulen stehen ohne Wert mit Lückensatz, "
    "Naturschutzgebiete und Lieferketten fehlen. Trends wie demographischer "
    "Wandel und Urbanisierung, natürliche Systeme, vergangene Extremereignisse "
    "und ihre Schäden sowie vorhandene Untersuchungen der Kommune (etwa "
    "Hochwasser- und Starkregengefahrenkarten, Klimaanalysekarten) erhebt sie "
    "nicht, und sie identifiziert keine betroffenen Handlungsfelder. "
    "Sozioökonomische und geographische Rahmenbedingungen und den "
    "Temperaturverlauf zeigt nur das Kommunenprofil, dieser nur je Bundesland. "
    "Einzelnachweis: Abschnitt „Gegenprobe Zeile 16“."
)


def _zeile_16() -> str:
    zeilen = [
        zeile
        for zeile in CHECKLISTE.read_text(encoding="utf-8").splitlines()
        if zeile.startswith("| 16 |")
    ]
    assert len(zeilen) == 1, (
        f"Erwartet genau eine Zeile, die mit '| 16 |' beginnt, gefunden: {len(zeilen)}"
    )
    return zeilen[0]


def _spalten(zeile: str) -> list[str]:
    # Markdown-Tabellenzeile: führendes und abschließendes '|' erzeugen leere
    # Rand-Elemente beim Split, die wir verwerfen.
    teile = zeile.split("|")
    assert teile[0].strip() == ""
    assert teile[-1].strip() == ""
    return teile[1:-1]


def test_zeile_16_hat_sieben_spalten():
    spalten = _spalten(_zeile_16())
    assert len(spalten) == 7, f"Erwartet 7 Spalten, gefunden: {len(spalten)} -> {spalten}"


def test_zeile_16_status_ist_teilweise():
    # T-0928-cto: Gegenprobe am UBA-Abschnitt 2.1.2 stuft Zeile 16 auf 'teilweise'.
    spalten = _spalten(_zeile_16())
    assert spalten[4].strip() == "teilweise"


def test_zeile_16_beleg_ist_exakt():
    spalten = _spalten(_zeile_16())
    assert spalten[5].strip() == ERWARTETE_BELEGE


def test_zeile_16_luecke_ist_exakt():
    spalten = _spalten(_zeile_16())
    assert spalten[6].strip() == ERWARTETE_LUECKE


def test_zeile_16_belegte_pfade_existieren():
    pfade = [pfad.strip() for pfad in ERWARTETE_BELEGE.split(",")]
    assert len(pfade) == 4
    for pfad in pfade:
        datei = REPO_ROOT / pfad
        assert datei.is_file(), f"Beleg-Datei fehlt: {pfad}"
