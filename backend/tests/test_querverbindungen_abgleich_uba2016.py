"""Tests gegen docs/QUERVERBINDUNGEN_ABGLEICH_UBA2016.md (T-0942-cto, Konformitätszeile 9, A2).

Die Tabelle im Abschnitt „## Abgleich“ muss eins zu eins den Einträgen in
``BENANNTE_BEZIEHUNGEN`` mit Ebene „Klimawirkung“ plus den gegenseitigen Beziehungen aus
``RUECKKOPPLUNGEN`` entsprechen. Eine Beziehung, die in beiden Modulen steht, ist genau eine Zeile.
Jede Zeile trägt ein Urteil aus {„bestätigt“, „teilweise“, „nicht dargestellt“}.
"""
import re
from pathlib import Path

from app.data.kwra_querverbindungen import BENANNTE_BEZIEHUNGEN
from app.data.kwra_rueckkopplungen import RUECKKOPPLUNGEN

DOKU_PFAD = Path(__file__).resolve().parents[2] / "docs" / "QUERVERBINDUNGEN_ABGLEICH_UBA2016.md"
URTEILE = {"bestätigt", "teilweise", "nicht dargestellt"}
SPALTEN = ["Nr", "Von", "Nach", "Richtung", "Herkunft", "Urteil", "Beleg in UBA 2016"]


def _abschnitt(text: str, ueberschrift: str) -> str:
    zeilen = text.splitlines()
    start = next(i + 1 for i, z in enumerate(zeilen) if z.strip() == ueberschrift)
    ende = next((j for j in range(start, len(zeilen)) if zeilen[j].startswith("## ")), len(zeilen))
    return "\n".join(zeilen[start:ende])


def _tabelle() -> tuple[list[str], list[list[str]]]:
    abschnitt = _abschnitt(DOKU_PFAD.read_text(encoding="utf-8"), "## Abgleich")
    zeilen = [z.strip() for z in abschnitt.splitlines() if z.strip().startswith("|")]
    zellen = [[c.strip() for c in z.strip("|").split("|")] for z in zeilen]
    kopf, trenner, daten = zellen[0], zellen[1], zellen[2:]
    assert all(set(c) <= set("-: ") for c in trenner)
    return kopf, daten


def _id(zelle: str) -> int | None:
    treffer = re.match(r"#(\d+)\b", zelle)
    return int(treffer.group(1)) if treffer else None


def _schluessel(von: int | None, nach: int | None, richtung: str) -> tuple:
    if richtung == "gegenseitig":
        return ("gegenseitig", frozenset((von, nach)))
    return ("gerichtet", von, nach)


def _erwartet() -> dict[tuple, set[str]]:
    """Schlüssel der Beziehung → Kennungen der RUECKKOPPLUNGEN-Einträge, aus denen sie stammt."""
    erwartet: dict[tuple, set[str]] = {}
    for b in BENANNTE_BEZIEHUNGEN:
        if b["ebene"] == "Klimawirkung":
            schluessel = _schluessel(b["quelle_kwra_id"], b["ziel_kwra_id"], b["richtung"])
            assert schluessel not in erwartet, f"doppelte Beziehung im Datenmodul: {schluessel}"
            erwartet[schluessel] = set()
    for rk in RUECKKOPPLUNGEN:
        kanten = {(k["von_kwra_id"], k["nach_kwra_id"]) for k in rk["kanten"]}
        for von, nach in kanten:
            if (nach, von) in kanten and von < nach:
                erwartet.setdefault(_schluessel(von, nach, "gegenseitig"), set()).add(rk["id"])
    return erwartet


def test_spalten():
    kopf, _ = _tabelle()
    assert kopf == SPALTEN


def test_zeilen_eins_zu_eins_wie_datenmodule():
    _, daten = _tabelle()
    erwartet = _erwartet()
    gefunden = [_schluessel(_id(z[1]), _id(z[2]), z[3]) for z in daten]
    assert len(gefunden) == len(set(gefunden)), "eine Beziehung steht mehrfach in der Tabelle"
    assert set(gefunden) == set(erwartet)
    assert len(daten) == len(erwartet)


def test_gegenseitige_beziehungen_nennen_rueckkopplung():
    _, daten = _tabelle()
    erwartet = _erwartet()
    for z in daten:
        for rk_id in erwartet[_schluessel(_id(z[1]), _id(z[2]), z[3])]:
            assert f"RUECKKOPPLUNGEN {rk_id}" in z[4], z


def test_jedes_urteil_zulaessig():
    _, daten = _tabelle()
    assert daten
    for z in daten:
        assert z[5] in URTEILE, z


def test_nummern_fortlaufend_und_beleg_mit_seite():
    _, daten = _tabelle()
    assert [int(z[0]) for z in daten] == list(range(1, len(daten) + 1))
    for z in daten:
        assert re.search(r"S\. \d+", z[6]), z


def test_ergebniszeile_passt_zur_tabelle():
    text = DOKU_PFAD.read_text(encoding="utf-8")
    _, daten = _tabelle()
    zahl = {u: sum(1 for z in daten if z[5] == u) for u in URTEILE}
    assert (f"{zahl['bestätigt']} × bestätigt, {zahl['teilweise']} × teilweise, "
            f"{zahl['nicht dargestellt']} × nicht dargestellt") in _abschnitt(text, "## Ergebnis")
