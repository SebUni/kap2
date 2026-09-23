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

    1. n = Anzahl dieser Parameter, b = Anzahl davon mit ``evidence_class == "belegt"``
       (jeder andere Wert, insbesondere ``"abgeschaetzt"``, zählt als unbelegt).
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
    belegt = sum(1 for k in klassen if k == "belegt")
    anteil = belegt / n if n else 0.0
    if anteil == 0:
        return "sehr gering"
    if anteil < 0.5:
        return "gering"
    if anteil < 1:
        return "mittel"
    return "hoch"


def gewissheitsstufen() -> dict[str, str]:
    """Gewissheitsstufe für jeden Code aus ``catalog.RISKS_BY_CODE``."""
    # Ein einziger Registry-Durchlauf für alle Risiken (gleiche Regel wie oben).
    alle = parameter_registry.catalog_parameters(layer_category="risks")
    return {code: gewissheitsstufe(code, _parameter=alle) for code in catalog.RISKS_BY_CODE}
