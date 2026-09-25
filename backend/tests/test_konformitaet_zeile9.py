"""T-0460, fortgeschrieben mit T-0741 und T-0946: Zeile 9 der Konformitäts-Checkliste ist
gegen die genannten Belege abgesichert.

T-0460 hatte Zeile 9 auf 'erfüllt' gesetzt. Die Gegenprobe gegen KWRA 2021,
Teilbericht 6, Kap. 3.4 (T-0741, Abschnitt „Gegenprobe Zeile 9“ in der Checkliste)
hat ergeben, dass die Belege die Anforderung nur teilweise tragen. T-0946 hat die
Gegenprobe nach den Teilpaketen von T-0870 mit neuen Urteilen fortgeschrieben; der
Status der Zeile 9 folgt seitdem den Urteilen der Tabelle A1 bis A13.

Prüft wörtlich gegen docs/KONFORMITAET_CHECKLISTE.md:
- es gibt genau eine Zeile, die mit '| 9 |' beginnt, mit sieben Spalten,
- die Tabelle unter „Gegenprobe Zeile 9“ hat je genau eine Zeile A1 bis A13 mit
  einem zulässigen Urteil,
- die Statusspalte der Zeile 9 ist genau dann 'erfüllt', wenn A1 bis A12 alle
  'trägt' lauten, sonst 'teilweise' (A13 ist als nicht einschlägig begründet),
- die Lücke ist bei 'teilweise' benannt, bei 'erfüllt' '—',
- die Beleg-Spalte ist genau die erwartete Liste, und jede Datei existiert.
"""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CHECKLISTE = REPO_ROOT / "docs" / "KONFORMITAET_CHECKLISTE.md"

ERWARTETE_BELEGE = (
    "backend/app/data/kwra_querverbindungen.py, "
    "backend/app/data/kwra_rueckkopplungen.py, "
    "backend/app/data/kwra_handlungsfeld_querbezuege.py, "
    "backend/app/services/querverbindungen.py, "
    "docs/QUERVERBINDUNGEN_KLIMAWIRKUNGEN.md, "
    "docs/QUERVERBINDUNGEN_ABGLEICH_UBA2016.md, "
    "frontend/src/components/dashboard/RiskInteractionSection.tsx, "
    "frontend/src/components/dashboard/QuerverbindungenHandlungsfelder.tsx, "
    "frontend/src/components/dashboard/RueckkopplungKreislauf.tsx"
)

ABSCHNITT_KOPF = "### Gegenprobe Zeile 9 gegen"
URTEILE = ("trägt", "trägt teilweise", "trägt nicht")
ANFORDERUNGEN = [f"A{n}" for n in range(1, 14)]
FUER_STATUS = [f"A{n}" for n in range(1, 13)]  # A13: nicht einschlägig


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


def _gegenprobe_zeilen() -> list[list[str]]:
    """Tabellenzeilen A… des Abschnitts „Gegenprobe Zeile 9“ (bis zur nächsten Überschrift)."""
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


def test_zeile_9_hat_sieben_spalten():
    spalten = _spalten(_zeile_9())
    assert len(spalten) == 7, f"Erwartet 7 Spalten, gefunden: {len(spalten)} -> {spalten}"


def test_gegenprobe_hat_je_eine_zeile_a1_bis_a13_mit_zulaessigem_urteil():
    urteile = _urteile()
    for nr, urteil in urteile.items():
        assert urteil in URTEILE, f"{nr}: unzulässiges Urteil {urteil!r}"


def test_zeile_9_status_folgt_den_urteilen_a1_bis_a12():
    urteile = _urteile()
    status = _spalten(_zeile_9())[4].strip()
    alle_tragen = all(urteile[nr] == "trägt" for nr in FUER_STATUS)
    erwartet = "erfüllt" if alle_tragen else "teilweise"
    assert status == erwartet, (
        f"Status der Zeile 9 ist {status!r}, nach den Urteilen A1–A12 erwartet {erwartet!r} "
        f"({ {nr: urteile[nr] for nr in FUER_STATUS} })"
    )


def test_zeile_9_luecke_passt_zum_status():
    spalten = _spalten(_zeile_9())
    status = spalten[4].strip()
    luecke = spalten[6].strip()
    if status == "erfüllt":
        assert luecke == "—", "Status 'erfüllt' verlangt die Lücke '—'"
    else:
        assert luecke not in ("", "—"), "Status 'teilweise' verlangt eine benannte Lücke"


def test_zeile_9_beleg_ist_exakt():
    spalten = _spalten(_zeile_9())
    assert spalten[5].strip() == ERWARTETE_BELEGE


def test_zeile_9_belegte_pfade_existieren():
    pfade = [pfad.strip() for pfad in ERWARTETE_BELEGE.split(",")]
    assert len(pfade) == 9
    for pfad in pfade:
        datei = REPO_ROOT / pfad
        assert datei.is_file(), f"Beleg-Datei fehlt: {pfad}"
