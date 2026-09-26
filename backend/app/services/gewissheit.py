"""Kategoriale Gewissheitsstufe je Klimawirkung (Konformitäts-Checkliste Zeile 8).

KWRA 2021 (Teilbericht 6, Kap. 3.3, Tabelle 17) weist die Bewertungsgewissheit je
Klimawirkung auf einer einheitlichen Skala aus. Das Produkt leitet diese Stufe hier
aus den maschinenlesbaren Evidenzklassen (``evidence_class``, Vorgabe P1) der
Parameter ab, die ``parameter_registry`` zu einem Risiko führt — damit ist sie für
jede Klimawirkung nach derselben Regel gebildet und handlungsfeldübergreifend
vergleichbar.
"""

from __future__ import annotations

from app.data import catalog
from app.services import parameter_registry

#: Vierstufige Skala, aufsteigend nach Gewissheit.
GEWISSHEITSSTUFEN = ("sehr gering", "gering", "mittel", "hoch")

#: Ab diesem Anteil belegter Parameter gilt die Gewissheit mindestens als „mittel".
SCHWELLE_MITTEL = 0.5

#: Zahlenschwellen der Ableitungsregel mit Herleitung (Vorgabe P1: Abschätzung als
#: solche ausgewiesen). Die Grenzen 0 („kein Parameter belegt") und 1 („alle belegt")
#: sind Wesen der Stufen „sehr gering" und „hoch", keine wählbaren Schwellen.
SCHWELLEN = {
    "SCHWELLE_MITTEL": {
        "wert": SCHWELLE_MITTEL,
        "art": "Abschätzung von KAP3",
        "herleitung": (
            "Die KWRA weist die Bewertungsgewissheit auf einer Skala aus (TB6 Kap. 3.3, "
            "Tabelle 17), nennt aber keinen Zahlenschnitt für einen Anteil belegter "
            "Parameter. KAP3 setzt die Grenze zwischen „gering“ und „mittel“ bei der Hälfte: "
            "Ist mindestens die Hälfte der Parameter eines Risikos belegt, stützt sich die "
            "Aussage überwiegend auf Quellen, sonst überwiegend auf Abschätzungen."
        ),
        "band": (
            "0,4-0,6 (0,5 als natürlicher Schnitt „überwiegend belegt“; die Bandbreite ist "
            "eine Setzung von KAP3, nicht aus einer Quelle abgeleitet)."
        ),
        "sensitivitaet": (
            "Wirkt nur auf die Stufe „gering“ gegenüber „mittel“ und über die "
            "Charakterisierungsgruppe (Zeile 7) darauf, ob eine Klimawirkung „unter "
            "Unsicherheit“ geführt wird. Keine Rückwirkung auf Euro-Beträge."
        ),
    },
}


def _risiko_parameter(risk_code: str) -> list[dict]:
    """Parameter, die die Registry diesem Risiko selbst zuordnet (``layer_code``)."""
    return [
        p for p in parameter_registry.catalog_parameters(
            layer_code=risk_code, layer_category="risks",
        )
        if p.get("layer_code") == risk_code
    ]


def gewissheitsstufe(risk_code: str, *, _parameter: list[dict] | None = None) -> str:
    """Gewissheitsstufe einer Klimawirkung auf der Skala sehr gering/gering/mittel/hoch.

    Ableitungsregel (benutzt ausschließlich die ``evidence_class``-Werte der
    Parameter, die ``parameter_registry.catalog_parameters`` mit
    ``layer_code == risk_code`` zu diesem Risiko führt):

    1. n = Anzahl dieser Parameter, b = Anzahl davon mit ``evidence_class`` in
       ``parameter_registry.BELEGTE_KLASSEN`` (``"belegt"`` und ``"berechnet"``;
       jeder andere Wert, insbesondere ``"abgeschaetzt"``, zählt als unbelegt).
    2. Anteil a = b / n; ohne Parameter (n = 0) gilt a = 0.
    3. Stufe:
       - a == 0          → ``"sehr gering"`` (kein Parameter belegt),
       - 0 < a < 0,5     → ``"gering"`` (weniger als die Hälfte belegt),
       - 0,5 ≤ a < 1     → ``"mittel"`` (mindestens die Hälfte, aber nicht alle belegt),
       - a == 1          → ``"hoch"`` (alle Parameter belegt).

    Liefert immer genau einen Wert aus ``GEWISSHEITSSTUFEN``, nie ``None``.
    Unbekannte Risikocodes lösen ``KeyError`` aus.
    """
    if risk_code not in catalog.RISKS_BY_CODE:
        raise KeyError(f"Unbekannter Risiko-Code: {risk_code}")
    params = _risiko_parameter(risk_code) if _parameter is None else [
        p for p in _parameter if p.get("layer_code") == risk_code
    ]
    klassen = [p.get("evidence_class") for p in params]
    n = len(klassen)
    belegt = sum(1 for k in klassen if k in parameter_registry.BELEGTE_KLASSEN)
    anteil = belegt / n if n else 0.0
    if anteil == 0:
        return "sehr gering"
    if anteil < SCHWELLE_MITTEL:
        return "gering"
    if anteil < 1:
        return "mittel"
    return "hoch"


def gewissheitsstufen() -> dict[str, str]:
    """Gewissheitsstufe für jeden Code aus ``catalog.RISKS_BY_CODE``."""
    # Ein einziger Registry-Durchlauf für alle Risiken (gleiche Regel wie oben).
    alle = parameter_registry.catalog_parameters(layer_category="risks")
    return {code: gewissheitsstufe(code, _parameter=alle) for code in catalog.RISKS_BY_CODE}
