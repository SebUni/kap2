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


#: Parameter-ID-Muster eines nutzergesetzten Kostensatzes (``parameter_registry``).
_COST_RATE_PARAM_SUFFIX = ".cost_per_outcome"
_COST_RATE_PARAM_PREFIX = "risks."


def overridden_cost_rate_codes(db, kommune_id: int) -> set[str]:
    """Wirkungskategorien, deren Kostensatz die Kommune selbst gesetzt hat.

    Ein Override macht einen unbelegten Kostensatz **nicht** belegt: Der Wert ist
    der Beleg der Kommune, nicht unserer. Er wird im Hinweistext zusätzlich
    benannt (Entscheidung CEO, 20.09.2026). Fehlt die Datenbank oder schlägt die
    Abfrage fehl, wird nichts behauptet (leere Menge).
    """
    try:
        from app.services import parameter_registry

        overrides = parameter_registry.load_db_overrides(db, kommune_id)
    except Exception:  # Export/Kontext dürfen an der Zusatzangabe nicht scheitern
        return set()
    out: set[str] = set()
    for o in overrides or []:
        pid = str(o.get("parameter_id") or "")
        if pid.startswith(_COST_RATE_PARAM_PREFIX) and pid.endswith(_COST_RATE_PARAM_SUFFIX):
            out.add(pid[len(_COST_RATE_PARAM_PREFIX):-len(_COST_RATE_PARAM_SUFFIX)])
    return out


def qualifier_text(lb: dict | None, overridden_codes: Iterable[str] = ()) -> str | None:
    """Der Qualifizierungstext zu einer Euro-Summe — wörtlich wie im Dashboard/API.

    ``None``, wenn es nichts zu qualifizieren gibt (``lb`` ist ``None``). Sonst der
    unveränderte ``note``-Text aus :func:`lower_bound`; tragen betroffene
    Kategorien einen nutzergesetzten Kostensatz, folgt ein zusätzlicher Satz, der
    das benennt.
    """
    if not lb:
        return None
    text = lb.get("note") or ""
    ov = set(overridden_codes or ())
    if not ov:
        return text
    betroffen = [c for c in (lb.get("categories") or []) if c.get("code") in ov]
    if not betroffen:
        return text
    namen = ", ".join(c.get("name", c.get("code", "")) for c in betroffen)
    return text + (
        f" Bei {len(betroffen)} dieser Kategorien ({namen}) ist der Kostensatz "
        f"vom Nutzer gesetzt (Override der Kommune); dieser Wert gilt weiterhin "
        f"als unbelegt, weil er nicht durch eine Quelle des Modells gedeckt ist."
    )
