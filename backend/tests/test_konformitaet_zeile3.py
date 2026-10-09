"""T-1871: Zeile 3 der Konformitäts-Checkliste ist gegen die genannten Belege abgesichert.

Die Gegenprobe gegen KWRA 2021, Teilbericht 1, Kap. 2.1.3 (mit Tabelle 3) und Kap. 1.3
(Abschnitt „Gegenprobe Zeile 3“ in der Checkliste) hat ergeben, dass die Belege die
Anforderungen nur teilweise tragen. Der Status der Zeile 3 folgt den Urteilen A1 bis A6.

Prüft wörtlich gegen docs/KONFORMITAET_CHECKLISTE.md:
- es gibt genau eine Zeile, die mit '| 3 |' beginnt, mit sieben Spalten,
- die Tabelle unter „Gegenprobe Zeile 3“ hat je genau eine Zeile A1 bis A6 mit
  einem zulässigen Urteil,
- die Statusspalte der Zeile 3 ist genau dann 'erfüllt', wenn A1 bis A6 alle
  'trägt' lauten, sonst 'teilweise',
- die Lücke ist bei 'teilweise' benannt (nicht leer, nicht '—') und endet mit dem
  Verweis auf den Einzelnachweis, bei 'erfüllt' genau '—',
- die Beleg-Spalte ist genau die erwartete Liste, und jede Datei existiert.
"""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CHECKLISTE = REPO_ROOT / "docs" / "KONFORMITAET_CHECKLISTE.md"

ERWARTETE_BELEGE = (
    "docs/evidenz/register.md, "
    "docs/methodik/95_hitzebelastung.md, "
    "frontend/src/components/ParameterTable.tsx"
)

ABSCHNITT_KOPF = "### Gegenprobe Zeile 3 gegen "
URTEILE = ("trägt", "trägt teilweise", "trägt nicht")
ANFORDERUNGEN = [f"A{n}" for n in range(1, 7)]
VERWEIS = "Einzelnachweis: Abschnitt „Gegenprobe Zeile 3“."


def _zeile_3() -> str:
    zeilen = [
        zeile
        for zeile in CHECKLISTE.read_text(encoding="utf-8").splitlines()
        if zeile.startswith("| 3 |")
    ]
    assert len(zeilen) == 1, (
        f"Erwartet genau eine Zeile, die mit '| 3 |' beginnt, gefunden: {len(zeilen)}"
    )
    return zeilen[0]


def _spalten(zeile: str) -> list[str]:
    # Markdown-Tabellenzeile: führendes und abschließendes '|' erzeugen leere
    # Rand-Elemente beim Split, die wir verwerfen.
    teile = zeile.split("|")
    assert teile[0].strip() == ""
    assert teile[-1].strip() == ""
    return teile[1:-1]


def _gegenprobe_zeilen() -> list[list[str]]:
    """Tabellenzeilen A… des Abschnitts „Gegenprobe Zeile 3“ (bis zur nächsten Überschrift)."""
    zeilen = CHECKLISTE.read_text(encoding="utf-8").splitlines()
    starts = [i for i, z in enumerate(zeilen) if z.startswith(ABSCHNITT_KOPF)]
    assert len(starts) == 1, f"Erwartet genau einen Abschnitt '{ABSCHNITT_KOPF}', gefunden: {len(starts)}"
    zeilen_a = []
    for zeile in zeilen[starts[0] + 1:]:
        if zeile.startswith(("# ", "## ", "### ", "#### ")):
            break
        if zeile.startswith("| A"):
            spalten = [s.strip() for s in _spalten(zeile)]
            assert len(spalten) == 5, f"Erwartet 5 Spalten, gefunden: {len(spalten)} -> {zeile[:60]}"
            zeilen_a.append(spalten)
    return zeilen_a


def _urteile() -> dict[str, str]:
    zeilen_a = _gegenprobe_zeilen()
    nummern = [spalten[0] for spalten in zeilen_a]
    for nr in ANFORDERUNGEN:
        assert nummern.count(nr) == 1, f"Erwartet genau eine Zeile {nr}, gefunden: {nummern.count(nr)}"
    assert sorted(nummern) == sorted(ANFORDERUNGEN), f"Unerwartete Zeilen: {nummern}"
    return {spalten[0]: spalten[4] for spalten in zeilen_a}


def test_zeile_3_hat_sieben_spalten():
    spalten = _spalten(_zeile_3())
    assert len(spalten) == 7, f"Erwartet 7 Spalten, gefunden: {len(spalten)} -> {spalten}"


def test_gegenprobe_hat_je_eine_zeile_a1_bis_a6_mit_zulaessigem_urteil():
    urteile = _urteile()
    for nr, urteil in urteile.items():
        assert urteil in URTEILE, f"{nr}: unzulässiges Urteil {urteil!r}"


def test_zeile_3_status_folgt_den_urteilen():
    urteile = _urteile()
    status = _spalten(_zeile_3())[4].strip()
    alle_tragen = all(urteile[nr] == "trägt" for nr in ANFORDERUNGEN)
    erwartet = "erfüllt" if alle_tragen else "teilweise"
    assert status == erwartet, (
        f"Status der Zeile 3 ist {status!r}, nach den Urteilen A1–A6 erwartet {erwartet!r} ({urteile})"
    )


def test_zeile_3_luecke_passt_zum_status():
    spalten = _spalten(_zeile_3())
    status = spalten[4].strip()
    luecke = spalten[6].strip()
    assert status in ("erfüllt", "teilweise"), f"unerwarteter Status {status!r}"
    if status == "erfüllt":
        assert luecke == "—", "Status 'erfüllt' verlangt die Lücke '—'"
    else:
        assert luecke not in ("", "—"), "Status 'teilweise' verlangt eine benannte Lücke"
        assert luecke.endswith(VERWEIS), f"Lücke endet nicht mit {VERWEIS!r}"


def test_zeile_3_beleg_ist_exakt():
    spalten = _spalten(_zeile_3())
    assert spalten[5].strip() == ERWARTETE_BELEGE


def test_zeile_3_belegte_pfade_existieren():
    pfade = [pfad.strip() for pfad in ERWARTETE_BELEGE.split(",")]
    assert len(pfade) == 3
    for pfad in pfade:
        datei = REPO_ROOT / pfad
        assert datei.is_file(), f"Beleg-Datei fehlt: {pfad}"
