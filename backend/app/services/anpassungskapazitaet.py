"""Bewertung der Anpassungskapazität nach ISO 14091 (Checklistenzeile 18, Teil B,
Ticket T-0762, Vorhaben T-0448).

Die Kommune stuft jede der vier Komponenten selbst auf einer Skala 0 bis 3 ein. Dieses
Modul wendet nur die Engpassregel an: Die Gesamtstufe ist das Minimum der vier Stufen,
sobald alle vier bewertet sind, sonst None. Es rechnet keine Prozentzahl und führt keine
weiteren Parameter ein (P1, A-0034). Alle Texte stammen aus ``app.data.anpassungskapazitaet``.
"""

from __future__ import annotations

from app.data.anpassungskapazitaet import (
    HERLEITUNG_REIFEGRADE,
    KOMPONENTEN,
    MINDERUNGSSAETZE,
    OPTIONAL_SATZ,
    QUELLE_KOMPONENTEN,
    REGEL_GESAMTSTUFE,
    REIFEGRADE,
)

LABEL_NICHT_BEWERTET = "nicht bewertet"

_STUFE_LABELS: dict[int, str] = {int(r["stufe"]): str(r["label"]) for r in REIFEGRADE}


def _stufe_label(stufe: int | None) -> str:
    return LABEL_NICHT_BEWERTET if stufe is None else _STUFE_LABELS[stufe]


def bewerte_anpassungskapazitaet(einschaetzung: dict) -> dict:
    """Bewertet die Anpassungskapazität nach der Engpassregel.

    ``einschaetzung`` bildet Komponentencodes auf die Stufe 0, 1, 2, 3 oder None ab;
    fehlende Codes gelten als None. Unbekannte Codes oder unzulässige Stufen werfen
    ``ValueError``.
    """
    codes = [k["code"] for k in KOMPONENTEN]
    unbekannt = [c for c in einschaetzung if c not in codes]
    if unbekannt:
        raise ValueError(f"Unbekannte Komponente(n): {', '.join(map(str, unbekannt))}")

    stufen: dict[str, int | None] = {}
    for code in codes:
        wert = einschaetzung.get(code)
        if wert is not None and (
            isinstance(wert, bool) or not isinstance(wert, int) or wert not in _STUFE_LABELS
        ):
            raise ValueError(f"Unzulässige Stufe für {code}: {wert!r} (erlaubt: 0, 1, 2, 3, None)")
        stufen[code] = wert

    komponenten = [
        {
            "code": k["code"],
            "label": k["label"],
            "stufe": stufen[k["code"]],
            "stufe_label": _stufe_label(stufen[k["code"]]),
        }
        for k in KOMPONENTEN
    ]

    if any(s is None for s in stufen.values()):
        gesamtstufe = None
        engpaesse: list[str] = []
    else:
        gesamtstufe = min(stufen.values())
        engpaesse = [c for c in codes if stufen[c] == gesamtstufe]

    return {
        "optional_hinweis": OPTIONAL_SATZ,
        "komponenten": komponenten,
        "gesamtstufe": gesamtstufe,
        "gesamtstufe_label": _stufe_label(gesamtstufe),
        "engpaesse": engpaesse,
        "minderung": MINDERUNGSSAETZE[gesamtstufe],
        "regel": REGEL_GESAMTSTUFE,
        "quelle": QUELLE_KOMPONENTEN,
        "herleitung": HERLEITUNG_REIFEGRADE,
    }
