"""KWRA-Charakterisierungsgruppe je Klimawirkung (Konformitäts-Checkliste Zeile 7).

KWRA 2021 (Teilbericht 6, Kap. 6.2, S. 140–143, Tabelle 27) teilt Klimawirkungen mit
sehr dringenden Handlungserfordernissen in fünf Gruppen ein — Umsetzung, Entwicklung,
Entwicklung unter Unsicherheit, Innovation, Innovation unter Unsicherheit — nach zwei
Fragen: Reichen die Maßnahmen aus, um das Restrisiko auf ein gesetztes Niveau zu
senken (Anpassungspotenzial)? Und wie sicher ist die Aussage (Gewissheit)?

Das Produkt bildet beide Fragen aus Größen ab, die es selbst führt:

* **Anpassungspotenzial** = relative Risikominderung der Maßnahmen, die der Katalog
  dieser Klimawirkung quantitativ zuordnet (``catalog.MEASURES``, Schlüssel
  ``linked_risk_codes``), bei voller Abdeckung — siehe ``anpassungspotenzial``.
* **Gewissheit** = Gewissheitsstufe aus ``app.services.gewissheit`` (Zeile 8).

Abweichungen von der KWRA (Modellgrenze, bewusst ausgewiesen):

* Die KWRA misst gegen ein normativ gesetztes Restrisiko und trennt „beschlossene"
  von „weiterreichenden" Maßnahmen. Das Produkt kennt weder einen Restrisiko-Zielwert
  noch diese Trennung; es misst die relative Minderung durch die im Katalog
  hinterlegten Maßnahmen. Die Schwellen ``SCHWELLE_UMSETZUNG`` und
  ``SCHWELLE_ENTWICKLUNG`` sind deshalb eine **Abschätzung von KAP3** (siehe
  ``SCHWELLEN``), keine KWRA-Werte.
* Die KWRA zählt eine Gewissheit ab „mittel" als ausreichend, um nicht „unter
  Unsicherheit" zu fallen (TB6 S. 141, dritter Spiegelstrich); das übernimmt das
  Produkt unverändert. „Umsetzung" kennt die KWRA ohne Unsicherheitsvariante.
* Die beispielhafte Zuordnung der KWRA (Tabelle 27) beruht auf Expertenbewertungen
  und reagiert laut KWRA „in hohem Maße sensitiv" auf die gesetzten Zielwerte
  (S. 143); die hier abgeleitete Gruppe kann davon abweichen.
"""

from __future__ import annotations

from app.data import catalog
from app.services import gewissheit

#: Die fünf KWRA-Charakterisierungsgruppen (TB6 Kap. 6.2, Gruppen I–V).
CHARAKTERISIERUNGSGRUPPEN = (
    "Umsetzung",
    "Entwicklung",
    "Entwicklung unter Unsicherheit",
    "Innovation",
    "Innovation unter Unsicherheit",
)

#: Gewissheitsstufen, die als ausreichend gelten (KWRA TB6 S. 141: „mittel" reicht).
AUSREICHENDE_GEWISSHEIT = ("mittel", "hoch")
UNZUREICHENDE_GEWISSHEIT = ("sehr gering", "gering")

#: Ab dieser relativen Minderung reichen die hinterlegten Maßnahmen (Gruppe I).
SCHWELLE_UMSETZUNG = 0.5
#: Ab dieser relativen Minderung gibt es einen Hebel, der sich weiterentwickeln lässt.
SCHWELLE_ENTWICKLUNG = 0.1

#: Schwellen mit Herleitung (Vorgabe P1: Abschätzung als solche ausgewiesen).
SCHWELLEN = {
    "SCHWELLE_UMSETZUNG": {
        "wert": SCHWELLE_UMSETZUNG,
        "art": "Abschätzung von KAP3",
        "herleitung": (
            "Die KWRA setzt als Ziel, das Restrisiko im pessimistischen Fall von hoch auf "
            "mittel zu senken (TB6 S. 141), also um eine von drei Stufen. Übertragen auf eine "
            "relative Minderung gilt: Senken die im Katalog hinterlegten Maßnahmen das Risiko "
            "mindestens um die Hälfte, reichen sie aus, und es geht um die Umsetzung."
        ),
        "band": (
            "0,4-0,6 (0,5 als Übertragung von „eine von drei Stufen“ auf eine relative "
            "Minderung; die Bandbreite ist eine Setzung von KAP3, nicht aus einer Quelle "
            "abgeleitet)."
        ),
        "sensitivitaet": (
            "Bestimmt, ab welcher Minderung eine Klimawirkung als „Umsetzung“ gilt statt "
            "als „Entwicklung“. Wirkt nur auf die Einordnung (Konformitätszeile 7), nicht "
            "auf Risikoindizes oder Euro-Beträge."
        ),
    },
    "SCHWELLE_ENTWICKLUNG": {
        "wert": SCHWELLE_ENTWICKLUNG,
        "art": "Abschätzung von KAP3",
        "herleitung": (
            "Unterhalb von zehn Prozent Minderung gibt es im Katalog keinen Hebel mit "
            "nennenswerter belegter oder abgeschätzter Wirkung; das Ziel ist dann nur mit "
            "tiefgreifender Anpassung erreichbar (KWRA-Gruppe Innovation). Ab zehn Prozent "
            "gibt es einen Hebel, den weiterreichende Maßnahmen ausbauen können "
            "(KWRA-Gruppe Entwicklung)."
        ),
        "band": (
            "0,05-0,2 (0,1 als runde Grenze für „nennenswerte Wirkung“; die Bandbreite ist "
            "eine Setzung von KAP3, nicht aus einer Quelle abgeleitet)."
        ),
        "sensitivitaet": (
            "Bestimmt, ab welcher Minderung eine Klimawirkung als „Entwicklung“ statt "
            "als „Innovation“ gilt. Wirkt nur auf die Einordnung (Konformitätszeile 7), "
            "nicht auf Risikoindizes oder Euro-Beträge."
        ),
    },
}

#: Entscheidungstabelle: (Untergrenze p, Obergrenze p exklusiv, Gewissheitsstufen, Gruppe).
#: Genau eine Zeile je Gruppe; die Zeilen überdecken [0, 1] × alle vier Stufen lückenlos
#: und ohne Überschneidung.
ENTSCHEIDUNGSTABELLE: tuple[tuple[float, float, tuple[str, ...], str], ...] = (
    (SCHWELLE_UMSETZUNG, float("inf"), gewissheit.GEWISSHEITSSTUFEN, "Umsetzung"),
    (SCHWELLE_ENTWICKLUNG, SCHWELLE_UMSETZUNG, AUSREICHENDE_GEWISSHEIT, "Entwicklung"),
    (SCHWELLE_ENTWICKLUNG, SCHWELLE_UMSETZUNG, UNZUREICHENDE_GEWISSHEIT,
     "Entwicklung unter Unsicherheit"),
    (float("-inf"), SCHWELLE_ENTWICKLUNG, AUSREICHENDE_GEWISSHEIT, "Innovation"),
    (float("-inf"), SCHWELLE_ENTWICKLUNG, UNZUREICHENDE_GEWISSHEIT,
     "Innovation unter Unsicherheit"),
)


def anpassungspotenzial(risk_code: str, *, _massnahmen: list[dict] | None = None) -> float:
    """Relative Risikominderung (0..1) durch die im Katalog hinterlegten Maßnahmen.

    Maßnahmen sind alle Einträge aus ``catalog.MEASURES``, deren
    ``linked_risk_codes`` den Code enthält (nur diese wirken im Rechenweg auf das
    Risiko; ``qualitative_risk_codes`` tragen keine Wirkung und zählen nicht).
    Je Maßnahme gilt bei voller Abdeckung derselbe Faktor wie in
    ``measure_service._reduction_factor``: f = (1 − r)^n mit r = ``default_reduction``
    (auf 0..1 begrenzt) und n = Zahl der ``effect_target``-Komponenten (mindestens 1).
    Mehrere Maßnahmen wirken multiplikativ: p = 1 − Π f. Ohne Maßnahme ist p = 0.
    """
    if risk_code not in catalog.RISKS_BY_CODE:
        raise KeyError(f"Unbekannter Risiko-Code: {risk_code}")
    massnahmen = catalog.MEASURES if _massnahmen is None else _massnahmen
    rest = 1.0
    for m in massnahmen:
        if risk_code not in (m.get("linked_risk_codes") or []):
            continue
        r = max(0.0, min(1.0, float(m.get("default_reduction") or 0.0)))
        n = max(1, len(m.get("effect_target") or []))
        rest *= (1.0 - r) ** n
    return 1.0 - rest


def gruppe_aus(potenzial: float, gewissheitsstufe: str) -> str:
    """Wendet ``ENTSCHEIDUNGSTABELLE`` an (Tabelle siehe ``charakterisierungsgruppe``).

    Liefert genau einen Wert aus ``CHARAKTERISIERUNGSGRUPPEN``. Eine unbekannte
    Gewissheitsstufe oder eine Kombination ohne Tabellenzeile löst ``ValueError`` aus
    — nie ``None``.
    """
    if gewissheitsstufe not in gewissheit.GEWISSHEITSSTUFEN:
        raise ValueError(f"Unbekannte Gewissheitsstufe: {gewissheitsstufe!r}")
    for unten, oben, stufen, gruppe in ENTSCHEIDUNGSTABELLE:
        if unten <= potenzial < oben and gewissheitsstufe in stufen:
            return gruppe
    raise ValueError(
        f"Keine Zeile der Entscheidungstabelle für p={potenzial!r}, "
        f"Gewissheit={gewissheitsstufe!r}"
    )


def charakterisierungsgruppe(
    risk_code: str,
    *,
    _gewissheitsstufe: str | None = None,
    _massnahmen: list[dict] | None = None,
) -> str:
    """KWRA-Charakterisierungsgruppe einer Klimawirkung.

    Eingangsgrößen sind ausschließlich
    (a) das Anpassungspotenzial p = ``anpassungspotenzial(risk_code)`` (relative
        Risikominderung der im Katalog zu dieser Klimawirkung hinterlegten Maßnahmen) und
    (b) die Gewissheitsstufe g = ``gewissheit.gewissheitsstufe(risk_code)`` (Zeile 8).

    Entscheidungstabelle (``ENTSCHEIDUNGSTABELLE``; Schwellen 0,5 und 0,1 sind eine
    Abschätzung von KAP3, Herleitung in ``SCHWELLEN``; „Gewissheit ausreichend" ab
    „mittel" nach KWRA TB6 S. 141):

    | Anpassungspotenzial p | Gewissheitsstufe g            | Gruppe                         |
    |-----------------------|-------------------------------|--------------------------------|
    | p ≥ 0,5               | beliebig                      | Umsetzung                      |
    | 0,1 ≤ p < 0,5         | mittel, hoch                  | Entwicklung                    |
    | 0,1 ≤ p < 0,5         | sehr gering, gering           | Entwicklung unter Unsicherheit |
    | p < 0,1               | mittel, hoch                  | Innovation                     |
    | p < 0,1               | sehr gering, gering           | Innovation unter Unsicherheit  |

    Liefert immer genau einen Wert aus ``CHARAKTERISIERUNGSGRUPPEN``, nie ``None``;
    für dieselben Eingaben immer dasselbe Ergebnis. Unbekannte Codes → ``KeyError``.
    Die Parameter ``_gewissheitsstufe`` und ``_massnahmen`` erlauben es, bereits
    berechnete Eingaben bzw. konstruierte Maßnahmen zu übergeben (Sammelaufruf, Test).
    """
    p = anpassungspotenzial(risk_code, _massnahmen=_massnahmen)
    g = (gewissheit.gewissheitsstufe(risk_code)
         if _gewissheitsstufe is None else _gewissheitsstufe)
    return gruppe_aus(p, g)


def charakterisierungen() -> dict[str, dict]:
    """Für jeden Code aus ``catalog.RISKS_BY_CODE``: Gruppe mit ihren beiden Eingaben."""
    stufen = gewissheit.gewissheitsstufen()
    return {
        code: {
            "anpassungspotenzial": round(anpassungspotenzial(code), 4),
            "gewissheit": stufen[code],
            "gruppe": charakterisierungsgruppe(code, _gewissheitsstufe=stufen[code]),
        }
        for code in catalog.RISKS_BY_CODE
    }


def regel() -> dict:
    """Die Ableitungsregel für die API: Gruppen, Tabelle, Schwellen, Quelle, Grenzen."""
    def _grenze(x: float) -> float | None:
        return None if x in (float("inf"), float("-inf")) else x

    return {
        "gruppen": list(CHARAKTERISIERUNGSGRUPPEN),
        "entscheidungstabelle": [
            {"potenzial_ab": _grenze(u), "potenzial_unter": _grenze(o),
             "gewissheit": list(s), "gruppe": gr}
            for u, o, s, gr in ENTSCHEIDUNGSTABELLE
        ],
        "schwellen": SCHWELLEN,
        "quelle": ("UBA (Hrsg.): KWRA 2021, Teilbericht 6, Kap. 6.2 "
                   "„Charakterisierung der Handlungserfordernisse“, S. 140–143, Tabelle 27"),
        "modellgrenze": (
            "Die KWRA misst gegen ein normativ gesetztes Restrisiko und trennt beschlossene "
            "von weiterreichenden Maßnahmen; das Produkt misst die relative Minderung durch "
            "die im Katalog hinterlegten Maßnahmen. Die Gruppe kann deshalb von der "
            "beispielhaften Zuordnung der KWRA (Tabelle 27) abweichen."
        ),
    }
