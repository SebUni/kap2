"""Ausgebbare Fassung der Anpassungskapazität in Markdown (Checklistenzeile 18, Teil C,
Ticket T-0763, Vorhaben T-0448).

Dieses Modul formatiert ausschließlich das von
``app.services.anpassungskapazitaet.bewerte_anpassungskapazitaet`` gelieferte dict. Es
rechnet nichts nach und kennt die Datenkonstanten nur über das dict.

Bewusst **nicht** Teil dieses Pakets: Anbindung an ``export_service.py``, eine Route oder
eine Datei unter ``docs/methodik/``.
"""

from __future__ import annotations

TITEL = "## Anpassungskapazität (optionaler Analyseschritt)"

METHODENVERWEIS = "Methodenbeschreibung: siehe `docs/ANPASSUNGSKAPAZITAET.md`."


def _tabelle(komponenten: list[dict]) -> str:
    zeilen = [
        "| Komponente | Reifegrad | Stufe |",
        "| --- | --- | --- |",
    ]
    for k in komponenten:
        stufe = "" if k["stufe"] is None else str(k["stufe"])
        zeilen.append("| {} | {} | {} |".format(k["label"], k["stufe_label"], stufe))
    return "\n".join(zeilen)


def anpassungskapazitaet_als_markdown(bewertung: dict) -> str:
    """Formatiert die Bewertung aus ``bewerte_anpassungskapazitaet`` als Markdown.

    Aufbau: Überschrift, Optional-Hinweis, Tabelle der Komponenten (nicht bewertete
    Komponenten mit „nicht bewertet“ und leerer Stufe), Gesamtstufe, Minderungssatz,
    Regel, Quelle, Herleitung und Verweis auf ``docs/ANPASSUNGSKAPAZITAET.md``.
    """
    teile = [
        TITEL,
        "",
        bewertung["optional_hinweis"],
        "",
        _tabelle(bewertung["komponenten"]),
        "",
        "**Gesamtstufe:** " + bewertung["gesamtstufe_label"],
        "",
        bewertung["minderung"],
        "",
        bewertung["regel"],
        "",
        "Quelle: " + bewertung["quelle"],
        "",
        "Herleitung: " + bewertung["herleitung"],
        "",
        METHODENVERWEIS,
        "",
    ]
    return "\n".join(teile)
