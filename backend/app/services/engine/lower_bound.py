"""Untergrenzen-Kennzeichnung ausgewiesener Euro-Summen (UBA MK 4.0, Anforderung 25).

Wirkungskategorien, für die kein belegter Kostensatz vorliegt, gehen heute mit
0 €/Outcome-Einheit in die Schadenssumme ein (Sicherheitsnetz in
``catalog._enrich_risk_cost_sources``: Quelle ``Modellannahme (Kostensatz,
unbelegt)``). Ihr Schadensbeitrag fehlt damit im ausgewiesenen Betrag. Die
Methodenkonvention verlangt, solche Lücken zu benennen und die Summe als
konservative Schätzung bzw. Untergrenze kenntlich zu machen, statt die fehlende
Wirkung stillschweigend wegzulassen.

Abgrenzung: Die bewusst mit 0 € geführten Index-Risiken (Quelle „Bewusst nicht
monetarisiert (Doppelzählung)“) sind **keine** Lücke — ihr Schadensgehalt steckt
bereits in anderen Risiken. Sie zählen hier nicht mit.
"""

from __future__ import annotations

from collections.abc import Iterable

from app.data import catalog

#: Quelle, die das Sicherheitsnetz einem nicht-monetären Risiko ohne belegten
#: Kostensatz setzt (``parameter_registry`` zeigt sie als Parameterquelle an).
UNSOURCED_COST_SOURCE = "Modellannahme (Kostensatz, unbelegt)"


def cost_rate_is_unsourced(risk: dict) -> bool:
    """True, wenn der Kostensatz dieser Wirkungskategorie keinen Beleg trägt.

    Monetäre Risiken (ref_value bereits in €/Jahr) haben keinen eigenen
    Kostensatz-Parameter und gelten nie als unbelegt.
    """
    if not risk or catalog.risk_is_monetary(risk):
        return False
    source = (risk.get("cost_source") or "").strip()
    if source == UNSOURCED_COST_SOURCE:
        return True
    # Fallback für Katalogeinträge, die die Anreicherung nicht durchlaufen haben:
    # Kostensatz 0,0 € ohne jede Quellenangabe.
    return not source and float(risk.get("cost_per_outcome_eur") or 0.0) == 0.0


def unsourced_categories(risk_codes: Iterable[str]) -> list[dict]:
    """Die Wirkungskategorien aus ``risk_codes`` mit unbelegtem Kostensatz."""
    out: list[dict] = []
    for code in risk_codes:
        risk = catalog.RISKS_BY_CODE.get(code)
        if cost_rate_is_unsourced(risk):
            out.append({"code": code, "name": risk.get("name", code)})
    return out


def lower_bound(risk_codes: Iterable[str]) -> dict | None:
    """Untergrenzen-Hinweis zu einer Euro-Summe über ``risk_codes``.

    ``None``, wenn jede einfließende Wirkungskategorie einen belegten Kostensatz
    trägt — dann ist die Summe keine Untergrenze in diesem Sinne. Sonst ein
    maschinenlesbarer Block mit Zählwert, betroffenen Kategorien und Begründung.
    """
    codes = list(risk_codes)
    missing = unsourced_categories(codes)
    if not missing:
        return None
    names = ", ".join(m["name"] for m in missing)
    note = (
        f"{len(missing)} von {len(codes)} einfließenden Wirkungskategorien "
        f"tragen einen Kostensatz ohne Beleg und gehen deshalb mit 0 € in diese "
        f"Summe ein ({names}). Der ausgewiesene Betrag ist damit eine "
        f"konservative Untergrenze des tatsächlichen Schadens "
        f"(UBA-Methodenkonvention 4.0, Anforderung 25)."
    )
    return {
        "unsourced_categories": len(missing),
        "total_categories": len(codes),
        "categories": missing,
        "note": note,
    }
