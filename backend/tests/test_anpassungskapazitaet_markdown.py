"""Tests für die Markdown-Ausgabe der Anpassungskapazität (T-0763)."""

from app.data.anpassungskapazitaet import (
    KOMPONENTEN,
    MINDERUNGSSAETZE,
    OPTIONAL_SATZ,
    REGEL_GESAMTSTUFE,
)
from app.services.anpassungskapazitaet import bewerte_anpassungskapazitaet
from app.services.anpassungskapazitaet_markdown import anpassungskapazitaet_als_markdown


def _ausgabe() -> str:
    bewertung = bewerte_anpassungskapazitaet(
        {"organisation": 2, "technik": 3, "finanzen": 1, "oekosystem": 2}
    )
    return anpassungskapazitaet_als_markdown(bewertung)


def test_erste_zeile_ist_ueberschrift():
    assert _ausgabe().splitlines()[0] == "## Anpassungskapazität (optionaler Analyseschritt)"


def test_erste_nicht_leere_zeile_danach_ist_optional_satz():
    zeilen = _ausgabe().splitlines()[1:]
    assert next(z for z in zeilen if z.strip()) == OPTIONAL_SATZ


def test_tabelle_mit_allen_komponenten():
    zeilen = _ausgabe().splitlines()
    i = zeilen.index("| Komponente | Reifegrad | Stufe |")
    rest = "\n".join(zeilen[i + 1:])
    for k in KOMPONENTEN:
        assert "| " + k["label"] + " |" in rest


def test_gesamtstufe_zeile():
    assert "**Gesamtstufe:** im Aufbau" in _ausgabe().splitlines()


def test_saetze_und_verweis_woertlich():
    text = _ausgabe()
    assert MINDERUNGSSAETZE[1] in text
    assert REGEL_GESAMTSTUFE in text
    assert "docs/ANPASSUNGSKAPAZITAET.md" in text
    assert "Quelle: " in text
    assert "Herleitung: " in text


def test_nicht_bewertete_komponente():
    text = anpassungskapazitaet_als_markdown(bewerte_anpassungskapazitaet({"organisation": 2}))
    assert "| Technisches Vermögen | nicht bewertet |  |" in text
    assert MINDERUNGSSAETZE[None] in text
