"""Kurzfassung für politische Entscheidungsträger als Markdown (T-0452,
Konformitätszeile 20, ISO 14091 — zielgruppenspezifische Kommunikation).

Neben den ausführlichen Methodik-Berichten für die Fachöffentlichkeit erzeugt
dieses Modul eine Kurzfassung mit genau fünf festen Abschnitten in dieser
Reihenfolge:

1. ``Gesamtrisiko`` — ein Satz,
2. ``Die fünf teuersten Klimawirkungen`` — Tabelle mit höchstens fünf Zeilen,
3. ``Erwartete Schadenssumme`` — Summe mit Szenario und Zeitbezug,
4. ``Die fünf wirksamsten Maßnahmen`` — Tabelle mit höchstens fünf Zeilen,
5. ``Methode und Grenzen`` — höchstens fünf Sätze.

Es wird nichts neu berechnet: Jede Zahl stammt unverändert aus den vorhandenen
Diensten — ``measure_service.get_risk_aggregate`` (Aggregat ohne Maßnahmen),
``cost_projection_service.project_costs`` (Projektion 2025–2065) und
``measure_service.build_cost_summary`` (Maßnahmendienst). Dieses Modul wählt
nur aus, sortiert nach den dort gelieferten Beträgen und formatiert.

Bewusst nicht enthalten: Kartendarstellungen und der Untergrenzen-Hinweis aus
T-0440 (späteres Paket).
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from app.data import catalog
from app.services.engine import tunables

if TYPE_CHECKING:  # nur für die Typangabe; der Formatter läuft ohne Datenbank
    from sqlalchemy.orm import Session

MAX_ZEILEN = 5

# Szenario der Schadenssumme: der pessimistische Fall (KWRA 2021 bewertet das
# Klimarisiko im pessimistischen Fall), ohne Maßnahmen, unabgezinst (0 % RZPR).
SZENARIO = "rcp85"

UEBERSCHRIFT_GESAMTRISIKO = "Gesamtrisiko"
UEBERSCHRIFT_KLIMAWIRKUNGEN = "Die fünf teuersten Klimawirkungen"
UEBERSCHRIFT_SCHADENSSUMME = "Erwartete Schadenssumme"
UEBERSCHRIFT_MASSNAHMEN = "Die fünf wirksamsten Maßnahmen"
UEBERSCHRIFT_METHODE = "Methode und Grenzen"

# Höchstens fünf Sätze, ohne Abkürzungen mit Punkt (zählbar).
METHODE_UND_GRENZEN = (
    "Die Beträge stammen aus der rasterbasierten Klimarisikoanalyse des Produkts, "
    "die für jede Klimawirkung Klimasignal, Exposition und Sensitivität verknüpft und "
    "in Euro bewertet. "
    "Die Zukunftswerte schreiben die heutigen Schäden mit dem regionalisierten "
    "Klimasignal des Deutschen Wetterdienstes fort. "
    "Klimawirkungen ohne Bewertung in Euro sind in den Summen nicht enthalten. "
    "Alle Zahlen sind Schätzungen mit Unsicherheit und ersetzen keine detaillierte "
    "örtliche Fachplanung. "
    "Herleitung, Quellen und Parameter stehen in den ausführlichen Methodik-Berichten "
    "für die Fachöffentlichkeit."
)


def _de_euro(wert: float) -> str:
    """Geldbetrag in deutscher Schreibweise, auf ganze Euro gerundet angezeigt
    (Punkt als Tausendertrennzeichen); Entscheidung des CEO vom 20.09.2026."""
    return f"{wert:,.0f}".replace(",", ".") + " €"


def _teuerste_klimawirkungen(aggregat: dict) -> list[dict]:
    """Die höchstens fünf Klimawirkungen mit dem höchsten Betrag.

    ``cost.by_risk`` ist im Aggregat bereits nach Betrag absteigend sortiert
    (Klasse A zuerst). Übernommen werden nur Wirkungen mit Euro-Schicht, die in
    die Gesamtsumme eingehen (nicht-additive Teilkennzahlen würden doppelt zählen).
    """
    zeilen = [
        r for r in aggregat["cost"]["by_risk"]
        if r.get("has_euro_layer") and r.get("cost_eur") is not None
        and r["code"] not in catalog.NON_ADDITIVE_RISK_CODES
    ]
    return zeilen[:MAX_ZEILEN]


def _wirksamste_massnahmen(kostenuebersicht: dict) -> list[dict]:
    """Die höchstens fünf Maßnahmen mit dem höchsten jährlichen Nutzen in Euro
    (``annual_benefit_eur`` aus dem Maßnahmendienst); Maßnahmen ohne bezifferten
    Nutzen in Euro (Klasse B) oder ohne Nutzen bleiben außen vor."""
    zeilen = [
        m for m in kostenuebersicht["measures"]["rows"]
        if m.get("benefit_has_euro_layer", True) and (m.get("annual_benefit_eur") or 0) > 0
    ]
    zeilen.sort(key=lambda m: m["annual_benefit_eur"], reverse=True)
    return zeilen[:MAX_ZEILEN]


def _abschnitt_gesamtrisiko(name: str, aggregat: dict) -> str:
    gesamt = aggregat["cost"]["total_eur"] or 0.0
    top = _teuerste_klimawirkungen(aggregat)
    if top:
        return (
            f"Ohne weitere Anpassung erwartet {name} heute Klimaschäden von "
            f"{_de_euro(gesamt)} pro Jahr, am stärksten durch die Klimawirkung "
            f"„{top[0]['name']}“."
        )
    return (
        f"Ohne weitere Anpassung erwartet {name} heute Klimaschäden von "
        f"{_de_euro(gesamt)} pro Jahr."
    )


def _abschnitt_klimawirkungen(aggregat: dict) -> str:
    zeilen = [
        "| Klimawirkung | Erwarteter Schaden pro Jahr | Risikoklasse |",
        "| --- | --- | --- |",
    ]
    for r in _teuerste_klimawirkungen(aggregat):
        klasse = tunables.RISK_CLASS_LABELS.get(r.get("risk_class"), r.get("risk_class") or "—")
        zeilen.append(f"| {r['name']} | {_de_euro(r['cost_eur'])} | {klasse} |")
    return "\n".join(zeilen)


def _abschnitt_schadenssumme(projektion: dict) -> str:
    jahre = projektion["years"]
    block = projektion["scenarios"][SZENARIO]
    summe = block["no_measures"]["cumulative"][-1]
    return (
        f"Im Szenario {block['label']} summieren sich die erwarteten Klimaschäden "
        f"ohne Maßnahmen von {jahre[0]} bis {jahre[-1]} auf {_de_euro(summe)} "
        f"(nicht abgezinst)."
    )


def _abschnitt_massnahmen(kostenuebersicht: dict) -> str:
    zeilen = [
        "| Maßnahme | Nutzen pro Jahr | Investition | Betrieb pro Jahr |",
        "| --- | --- | --- | --- |",
    ]
    auswahl = _wirksamste_massnahmen(kostenuebersicht)
    for m in auswahl:
        zeilen.append(
            f"| {m['name']} | {_de_euro(m['annual_benefit_eur'])} | "
            f"{_de_euro(m['capex_eur'])} | {_de_euro(m['opex_annual_eur'])} |"
        )
    tabelle = "\n".join(zeilen)
    if not auswahl:
        tabelle += "\n\nFür diese Kommune ist noch keine Maßnahme mit bezifferter Wirkung geplant."
    return tabelle


def kurzfassung_markdown(name: str, aggregat: dict, projektion: dict,
                         kostenuebersicht: dict) -> str:
    """Formatiert die Kurzfassung aus den unveränderten Dienstergebnissen.

    ``aggregat``: Rückgabe von ``get_risk_aggregate(..., apply_measures=False)``;
    ``projektion``: Rückgabe von ``project_costs``; ``kostenuebersicht``:
    Rückgabe von ``build_cost_summary``.
    """
    teile = [
        f"# Kurzfassung Klimarisiko: {name}",
        "",
        f"## {UEBERSCHRIFT_GESAMTRISIKO}",
        "",
        _abschnitt_gesamtrisiko(name, aggregat),
        "",
        f"## {UEBERSCHRIFT_KLIMAWIRKUNGEN}",
        "",
        _abschnitt_klimawirkungen(aggregat),
        "",
        f"## {UEBERSCHRIFT_SCHADENSSUMME}",
        "",
        _abschnitt_schadenssumme(projektion),
        "",
        f"## {UEBERSCHRIFT_MASSNAHMEN}",
        "",
        _abschnitt_massnahmen(kostenuebersicht),
        "",
        f"## {UEBERSCHRIFT_METHODE}",
        "",
        METHODE_UND_GRENZEN,
        "",
    ]
    return "\n".join(teile)


def kurzfassung_fuer_kommune(db: Session, kommune) -> str:
    """Holt die drei Dienstergebnisse der Kommune und formatiert die Kurzfassung."""
    from app.services import cost_projection_service, measure_service

    aggregat = measure_service.get_risk_aggregate(db, kommune.id, apply_measures=False)
    projektion = cost_projection_service.project_costs(
        db, kommune.id, kommune.bundesland or "Sachsen")
    kostenuebersicht = measure_service.build_cost_summary(db, kommune.id)
    return kurzfassung_markdown(kommune.name, aggregat, projektion, kostenuebersicht)
