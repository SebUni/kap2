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
    "schadenskosten_eur"}``. ``mittlerer_index`` ist das arithmetische Mittel der
    Risikoindizes der Klimawirkungen des Bereichs (``None`` ohne Werte).
    """
    codes: dict[str, list[str]] = {b: [] for b in catalog.KWRA_SYSTEMBEREICHE}
    indizes: dict[str, list[float]] = {b: [] for b in catalog.KWRA_SYSTEMBEREICHE}
    kosten: dict[str, float | None] = {b: None for b in catalog.KWRA_SYSTEMBEREICHE}

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
        kosten[bereich] = (kosten[bereich] or 0.0) + float(r["cost_eur"] or 0.0)

    return {
        b: {
            "anzahl_klimawirkungen": len(codes[b]),
            "risk_codes": codes[b],
            "mittlerer_index": (round(sum(indizes[b]) / len(indizes[b]), 2)
                                if indizes[b] else None),
            "schadenskosten_eur": None if kosten[b] is None else round(kosten[b], 2),
        }
        for b in catalog.KWRA_SYSTEMBEREICHE
    }
