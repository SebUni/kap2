"""Auswertung über die fünf KWRA-Systembereiche (Konformitäts-Checkliste Zeile 10).

KWRA 2021 (Teilbericht 6, Kap. 7 „Querbetrachtung der Systembereiche“) vergleicht
die Klimarisiken über fünf übergeordnete Systembereiche hinweg. Das Produkt ordnet
jede Klimawirkung über ``catalog.RISK_SYSTEMBEREICH`` genau einem dieser Bereiche
zu; diese Funktion verdichtet ein Risiko-Aggregat (``get_risk_aggregate``) je
Bereich zu Zahl der Klimawirkungen, Risikohöhe und Schadenskosten.

Die produktspezifische Gruppierung (``group``, KAnG-Handlungsfelder) bleibt davon
unberührt.
"""

from __future__ import annotations

from app.data import catalog
from app.data.kwra_systembereich_zuordnung import SYSTEMBEREICH_JE_KWRA_ID


def _katalog_ids_je_bereich() -> dict[str, set[int]]:
    """KWRA-IDs aller Katalog-Klimawirkungen (gerechnet und Roadmap) je Systembereich."""
    ids = ({p["kwra_id"] for p in catalog.PLANNED_RISKS}
           | {s["kwra_id"] for s in catalog.RISKS_BY_CODE.values()})
    je: dict[str, set[int]] = {b: set() for b in catalog.KWRA_SYSTEMBEREICHE}
    for i in ids:
        je[SYSTEMBEREICH_JE_KWRA_ID[i]].add(i)
    return je


def systembereich_auswertung(agg: dict) -> dict[str, dict]:
    """Klimawirkungen, Risikohöhe und Schadenskosten je KWRA-Systembereich.

    ``agg`` ist ein Risiko-Aggregat mit ``agg["cost"]["by_risk"]`` (Einträge mit
    ``code``, ``cost_eur``, optional ``index`` und ``has_euro_layer``).

    Regeln wie in ``cost_projection_service._group_costs``:

    * Nicht-additive Sammelrisiken (``catalog.NON_ADDITIVE_RISK_CODES``) werden
      ausgeschlossen — weder gezählt noch summiert —, damit die Summe der fünf
      Bereichssummen der ausgewiesenen Gesamtsumme entspricht.
    * Klasse-B-Wirkungen (Screening ohne Euro-Bezifferung) zählen als
      Klimawirkung, tragen aber keinen Euro-Betrag bei. Ein Bereich ohne jede
      Klasse-A-Wirkung erhält ``schadenskosten_eur = None`` (nie 0 €).

    Rückgabe: alle fünf Bereiche in der Reihenfolge ``catalog.KWRA_SYSTEMBEREICHE``,
    je ``{"anzahl_klimawirkungen", "risk_codes", "mittlerer_index",
    "schadenskosten_eur", "klimawirkungen_im_katalog", "euro_beziffert"}``.
    ``klimawirkungen_im_katalog`` zählt alle Klimawirkungen des Katalogs (gerechnet
    und Roadmap) des Bereichs nach der KWRA-Zuordnung, ``euro_beziffert`` nennt den
    Ausschnitt als Text („x von y Klimawirkungen in Euro beziffert“).``mittlerer_index`` ist das arithmetische Mittel der
    Risikoindizes der Klimawirkungen des Bereichs (``None`` ohne Werte).
    """
    codes: dict[str, list[str]] = {b: [] for b in catalog.KWRA_SYSTEMBEREICHE}
    indizes: dict[str, list[float]] = {b: [] for b in catalog.KWRA_SYSTEMBEREICHE}
    kosten: dict[str, float | None] = {b: None for b in catalog.KWRA_SYSTEMBEREICHE}
    euro: dict[str, int] = {b: 0 for b in catalog.KWRA_SYSTEMBEREICHE}
    im_katalog = {b: len(i) for b, i in _katalog_ids_je_bereich().items()}

    for r in agg["cost"]["by_risk"]:
        code = r["code"]
        if code in catalog.NON_ADDITIVE_RISK_CODES:
            continue
        bereich = catalog.RISK_SYSTEMBEREICH[code]
        codes[bereich].append(code)
        if r.get("index") is not None:
            indizes[bereich].append(float(r["index"]))
        spec = catalog.RISKS_BY_CODE.get(code)
        if (r.get("has_euro_layer") is False
                or (spec is not None and not catalog.risk_has_euro_layer(spec))):
            continue
        euro[bereich] += 1
        kosten[bereich] = (kosten[bereich] or 0.0) + float(r["cost_eur"] or 0.0)

    return {
        b: {
            "anzahl_klimawirkungen": len(codes[b]),
            "risk_codes": codes[b],
            "mittlerer_index": (round(sum(indizes[b]) / len(indizes[b]), 2)
                                if indizes[b] else None),
            "schadenskosten_eur": None if kosten[b] is None else round(kosten[b], 2),
            "klimawirkungen_im_katalog": im_katalog[b],
            "euro_beziffert": (f"{euro[b]} von {im_katalog[b]} Klimawirkungen "
                               "in Euro beziffert"),
        }
        for b in catalog.KWRA_SYSTEMBEREICHE
    }
