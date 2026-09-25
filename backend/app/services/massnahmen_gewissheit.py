"""Gewissheit der Klimawirkungen und Evidenz der Wirkung je Maßnahme (Checkliste Zeile 19, A3).

ISO 14091 (Sekundärquelle UBA, „Klimarisikoanalysen auf kommunaler Ebene", Abschnitt
2.2.6, S. 29) verlangt, Unsicherheiten auch bei der Formulierung von Handlungsoptionen
zu berücksichtigen. Dieser Dienst stellt deshalb je Maßnahme aus ``catalog.MEASURES``
die vorhandenen Angaben **nebeneinander**:

* ``klimawirkungen`` — je verknüpfter Klimawirkung (``linked_risk_codes``) und je nur
  qualitativ verknüpfter Klimawirkung (``qualitative_risk_codes``) der Code, der Name,
  die Gewissheitsstufe aus ``gewissheit.gewissheitsstufe`` und ``qualitativ``,
* ``wirkung_evidenz`` — die hinterlegte Evidenzklasse der Wirkung (``default_reduction``)
  aus ``evidence_classes`` oder, falls dort keine steht, ein Feld ``evidence_class`` der
  Herleitung in ``evidence_derivation(s)``; sonst ``KEINE_EVIDENZKLASSE``.

Bewusst nicht enthalten: ein über die Klimawirkungen verbundener Wert (Minimum, Maximum
o. ä.) und ein Hinweis zur Interpretation je Maßnahme. Beides sind fachliche
Festlegungen des CMO (Anmerkung M-0005) und nicht Teil dieses Dienstes.
"""

from __future__ import annotations

from app.data import catalog
from app.services import gewissheit

#: Das Katalogfeld, das die Wirkung einer Maßnahme trägt.
WIRKUNGSFELD = "default_reduction"

KEINE_EVIDENZKLASSE = "keine Evidenzklasse hinterlegt"


def _wirkung_evidenz(massnahme: dict) -> str:
    """Evidenzklasse der Wirkung einer Maßnahme, so wie sie im Katalog hinterlegt ist.

    Die Struktur ist je Maßnahme verschieden: ``evidence_classes`` (Feld → Klasse),
    ``evidence_derivations`` oder ``evidence_derivation`` (Feld → Herleitung); manche
    Maßnahmen haben keine ``evidence_classes``.
    """
    klasse = (massnahme.get("evidence_classes") or {}).get(WIRKUNGSFELD)
    if klasse:
        return klasse
    herleitungen = (massnahme.get("evidence_derivations")
                    or massnahme.get("evidence_derivation") or {})
    herleitung = herleitungen.get(WIRKUNGSFELD)
    if isinstance(herleitung, dict) and herleitung.get("evidence_class"):
        return herleitung["evidence_class"]
    return KEINE_EVIDENZKLASSE


def _klimawirkung(code: str, *, qualitativ: bool) -> dict:
    risiko = catalog.RISKS_BY_CODE.get(code) or {}
    return {
        "code": code,
        "name": risiko.get("name", code),
        "gewissheitsstufe": gewissheit.gewissheitsstufe(code),
        "qualitativ": qualitativ,
    }


def massnahmen_gewissheit() -> list[dict]:
    """Je Maßnahme aus ``catalog.MEASURES`` genau ein Eintrag, in Katalogreihenfolge.

    Rückgabe::

        [{"code", "name",
          "klimawirkungen": [{"code", "name", "gewissheitsstufe", "qualitativ"}, …],
          "wirkung_evidenz": <Evidenzklasse oder KEINE_EVIDENZKLASSE>}, …]
    """
    eintraege: list[dict] = []
    for m in catalog.MEASURES:
        klimawirkungen = [
            _klimawirkung(c, qualitativ=False) for c in (m.get("linked_risk_codes") or [])
        ] + [
            _klimawirkung(c, qualitativ=True) for c in (m.get("qualitative_risk_codes") or [])
        ]
        eintraege.append({
            "code": m["code"],
            "name": m.get("name", m["code"]),
            "klimawirkungen": klimawirkungen,
            "wirkung_evidenz": _wirkung_evidenz(m),
        })
    return eintraege
