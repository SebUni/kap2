"""Fasst die Unsicherheit je Handlungsfeld nebeneinander zusammen (Konformitäts-Checkliste Zeile 19).

Abhängigkeiten zwischen Handlungsfeldern behandelt dieser Dienst nicht; dafür siehe
``backend/app/services/handlungsfeld_abhaengigkeiten.py``.

ISO 14091 (Sekundärquelle UBA, „Klimarisikoanalysen auf kommunaler Ebene", Abschnitt
2.2.6 „Ergebnisse interpretieren", S. 29f.) verlangt, bestehende Unsicherheiten bei der
Interpretation der Analyseergebnisse ausdrücklich zu berücksichtigen, bevor daraus
Handlungsoptionen formuliert werden. Bisher stand die Unsicherheit nur je Parameter
(Evidenz-Register) und je Klimawirkung (Gewissheitsstufe, Zeile 8) zur Verfügung.
Dieser Dienst fasst sie je Kommune über alle Handlungsfelder zusammen.

Je Handlungsfeld (KWRA-Handlungsfeld ``kwra_field`` der Klimawirkungen aus
``catalog.RISKS``) genau drei Angaben:

* ``niedrigste_gewissheit`` — die niedrigste Gewissheitsstufe
  (``gewissheit.GEWISSHEITSSTUFEN``) unter den Klimawirkungen des Handlungsfelds,
* ``parameter_nicht_belegt`` — Zahl der Parameter dieser Klimawirkungen, deren
  ``evidence_class`` weder ``"belegt"`` noch ``"berechnet"`` ist
  (``parameter_registry.BELEGTE_KLASSEN``; dieselbe Parametermenge wie in
  ``gewissheit.gewissheitsstufe``),
* ``klimawirkungen_niedrigste_stufe`` — die Codes der Klimawirkungen, die genau diese
  niedrigste Stufe tragen.

Dazu die Liste ``handlungsfelder_vorsicht`` der Handlungsfelder mit niedrigster Stufe
``gering`` oder ``sehr gering`` und, sobald diese nicht leer ist, der ``hinweis``.

Abgrenzung: Die Gewissheitsstufen und Evidenzklassen sind Eigenschaften des Katalogs,
nicht der Kommune; die Zusammenschau ist deshalb für jede Kommune gleich, solange alle
Klimawirkungen des Katalogs für sie gerechnet werden. Ein Vergleich zwischen Kommunen
(regionsübergreifend) ist nicht Teil dieses Dienstes.
"""

from __future__ import annotations

from app.data import catalog
from app.services import gewissheit, parameter_registry

#: Stufen, die vorsichtige Interpretation verlangen (KWRA TB6 S. 141: ab „mittel" reicht).
VORSICHT_STUFEN = ("sehr gering", "gering")

HINWEIS_VORSICHT = (
    "In den genannten Handlungsfeldern ist die Gewissheit der Ergebnisse gering oder "
    "sehr gering: Viele Parameter sind nicht belegt, sondern abgeschätzt. Die Ergebnisse "
    "dieser Handlungsfelder erfordern eine vorsichtige Interpretation, bevor daraus "
    "Handlungsoptionen abgeleitet werden."
)


def handlungsfelder() -> list[str]:
    """Alle Handlungsfelder des Katalogs (``kwra_field`` aus ``catalog.RISKS``),
    jedes genau einmal, in Katalogreihenfolge."""
    felder: list[str] = []
    for r in catalog.RISKS:
        feld = r.get("kwra_field") or "ohne Handlungsfeld"
        if feld not in felder:
            felder.append(feld)
    return felder


def unsicherheits_zusammenschau(
    kommune_id: int,
    *,
    _stufen: dict[str, str] | None = None,
    _parameter: list[dict] | None = None,
) -> dict:
    """Unsicherheits-Zusammenschau über alle Handlungsfelder für eine Kommune.

    Rückgabe::

        {"kommune_id": …,
         "handlungsfelder": [{"handlungsfeld", "niedrigste_gewissheit",
                               "parameter_nicht_belegt",
                               "klimawirkungen_niedrigste_stufe"}, …],
         "handlungsfelder_vorsicht": [<Handlungsfeld>, …],
         "hinweis": <Text mit „vorsichtige Interpretation"> oder None}

    ``_stufen`` (Code → Gewissheitsstufe) und ``_parameter`` (Parameterliste wie aus
    ``parameter_registry.catalog_parameters``) erlauben es, bereits berechnete bzw.
    konstruierte Eingaben zu übergeben (Sammelaufruf, Test).
    """
    parameter = (parameter_registry.catalog_parameters(layer_category="risks")
                 if _parameter is None else _parameter)
    stufen = (
        {code: gewissheit.gewissheitsstufe(code, _parameter=parameter)
         for code in catalog.RISKS_BY_CODE}
        if _stufen is None else _stufen
    )
    rang = {s: i for i, s in enumerate(gewissheit.GEWISSHEITSSTUFEN)}

    eintraege: list[dict] = []
    for feld in handlungsfelder():
        codes = [r["code"] for r in catalog.RISKS
                 if (r.get("kwra_field") or "ohne Handlungsfeld") == feld]
        niedrigste = min((stufen[c] for c in codes), key=lambda s: rang[s])
        nicht_belegt = sum(
            1 for p in parameter
            if p.get("layer_code") in codes
            and p.get("evidence_class") not in parameter_registry.BELEGTE_KLASSEN
        )
        eintraege.append({
            "handlungsfeld": feld,
            "niedrigste_gewissheit": niedrigste,
            "parameter_nicht_belegt": nicht_belegt,
            "klimawirkungen_niedrigste_stufe": [c for c in codes if stufen[c] == niedrigste],
        })

    vorsicht = [e["handlungsfeld"] for e in eintraege
                if e["niedrigste_gewissheit"] in VORSICHT_STUFEN]
    return {
        "kommune_id": kommune_id,
        "handlungsfelder": eintraege,
        "handlungsfelder_vorsicht": vorsicht,
        "hinweis": HINWEIS_VORSICHT if vorsicht else None,
    }
