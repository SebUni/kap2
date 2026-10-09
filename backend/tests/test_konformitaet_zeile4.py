"""T-1872: Zeile 4 der Konformitäts-Checkliste ist gegen ihren Beleg abgesichert.

Zeile 4 stand auf 'erfüllt'. Die Gegenprobe gegen KWRA 2021, Teilbericht 1, Kap. 2.1.4.1
(Abschnitt „Gegenprobe Zeile 4“ in der Checkliste) hat ergeben, dass der Beleg die
begriffliche und methodische Trennung von Sensitivität und räumlicher Exposition nur
teilweise trägt (A1, A2 und A4 „trägt teilweise“). Der Status der Zeile 4 folgt seitdem den
Urteilen der Tabelle A1 bis A6.

Prüft wörtlich gegen docs/KONFORMITAET_CHECKLISTE.md:
- es gibt genau eine Zeile, die mit '| 4 |' beginnt, mit sieben Spalten,
- die Tabelle unter „Gegenprobe Zeile 4“ hat je genau eine Zeile A1 bis A6 mit einem
  zulässigen Urteil,
- die Statusspalte der Zeile 4 ist genau dann 'erfüllt', wenn A1 bis A6 alle 'trägt'
  lauten, sonst 'teilweise'; festgeschrieben ist heute 'teilweise',
- die Lücke ist bei 'teilweise' nicht leer und nicht '—', nennt den Pfad des Belegs und
  endet mit dem Verweis auf den Einzelnachweis; bei 'erfüllt' ist sie genau '—',
- die Beleg-Spalte ist genau die erwartete Datei, und sie existiert.
"""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CHECKLISTE = REPO_ROOT / "docs" / "KONFORMITAET_CHECKLISTE.md"

ERWARTETE_BELEGE = "docs/methodik/95_hitzebelastung.md"
ERWARTETER_STATUS = "teilweise"
VERWEIS = "Einzelnachweis: Abschnitt „Gegenprobe Zeile 4“."

ABSCHNITT_KOPF = "### Gegenprobe Zeile 4 gegen"
URTEILE = ("trägt", "trägt teilweise", "trägt nicht")
ANFORDERUNGEN = [f"A{n}" for n in range(1, 7)]


def _zeile_4() -> str:
    zeilen = [
        zeile
        for zeile in CHECKLISTE.read_text(encoding="utf-8").splitlines()
        if zeile.startswith("| 4 |")
    ]
    assert len(zeilen) == 1, (
        f"Erwartet genau eine Zeile, die mit '| 4 |' beginnt, gefunden: {len(zeilen)}"
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
    """Tabellenzeilen A… des Abschnitts „Gegenprobe Zeile 4“ (bis zur nächsten Überschrift)."""
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


def test_zeile_4_hat_sieben_spalten():
    spalten = _spalten(_zeile_4())
    assert len(spalten) == 7, f"Erwartet 7 Spalten, gefunden: {len(spalten)} -> {spalten}"


def test_gegenprobe_hat_je_eine_zeile_a1_bis_a6_mit_zulaessigem_urteil():
    urteile = _urteile()
    for nr, urteil in urteile.items():
        assert urteil in URTEILE, f"{nr}: unzulässiges Urteil {urteil!r}"


def test_zeile_4_status_folgt_den_urteilen_a1_bis_a6():
    urteile = _urteile()
    status = _spalten(_zeile_4())[4].strip()
    alle_tragen = all(urteile[nr] == "trägt" for nr in ANFORDERUNGEN)
    erwartet = "erfüllt" if alle_tragen else "teilweise"
    assert status == erwartet, (
        f"Status der Zeile 4 ist {status!r}, nach den Urteilen A1–A6 erwartet {erwartet!r} ({urteile})"
    )


def test_zeile_4_status_ist_festgeschrieben():
    status = _spalten(_zeile_4())[4].strip()
    assert status == ERWARTETER_STATUS, (
        f"Status der Zeile 4 ist {status!r}, festgeschrieben ist {ERWARTETER_STATUS!r}"
    )


def test_zeile_4_luecke_passt_zum_status():
    spalten = _spalten(_zeile_4())
    status = spalten[4].strip()
    luecke = spalten[6].strip()
    if status == "erfüllt":
        assert luecke == "—", "Status 'erfüllt' verlangt die Lücke '—'"
    else:
        assert luecke not in ("", "—"), "Status 'teilweise' verlangt eine benannte Lücke"
        assert ERWARTETE_BELEGE in luecke, "Die Lücke nennt den betroffenen Pfad"
        assert luecke.endswith(VERWEIS), f"Die Lücke endet mit {VERWEIS!r}"


def test_zeile_4_beleg_ist_exakt():
    spalten = _spalten(_zeile_4())
    assert spalten[5].strip() == ERWARTETE_BELEGE


def test_zeile_4_belegte_pfade_existieren():
    pfade = [pfad.strip() for pfad in ERWARTETE_BELEGE.split(",")]
    assert len(pfade) == 1
    for pfad in pfade:
        datei = REPO_ROOT / pfad
        assert datei.is_file(), f"Beleg-Datei fehlt: {pfad}"
