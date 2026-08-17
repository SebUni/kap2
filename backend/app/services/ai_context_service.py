"""Baut den kompakten Daten-Kontext für den KI-Assistenten.

Ziel: maximale Aussagekraft bei minimalen Tokens. Deshalb ausschließlich
aggregierte Werte (nie Zell-Rohdaten) und dichtes deutsches Klartext-Format
(Key-Value-Zeilen statt JSON — spart ~30–40 % Tokens und wird vom Modell besser
wörtlich zitiert). Der gesamte Block bleibt i. d. R. deutlich unter ~1.500 Tokens.

Datenschutz: Der Block enthält nur aggregierte Kommunalstatistik (Einwohnerzahl,
Fläche, Klimakennzahlen, Risikoindizes, Schadenssummen) — keine personenbezogenen
Daten. Er wird ausschließlich serverseitig erzeugt; Nutzereingaben fließen nicht ein.
"""
from __future__ import annotations

import logging

from sqlalchemy.orm import Session

from app.models.models import AdaptationMeasure, Kommune
from app.services import kommune_profile_service, measure_service

log = logging.getLogger("app")

# Nur diese Klima-Kennzahlen in den Kontext (die risikorelevantesten) — hält den
# Block schlank. Reihenfolge = Ausgabereihenfolge.
_CLIMATE_CODES = [
    "hot_days", "tropical_nights", "frost_days", "precipitation_mm",
    "heavy_rain_days", "storm_days", "dry_days",
]


def _num(value, decimals: int = 1) -> str:
    """Deutsche Zahl (Komma, Tausenderpunkt), gerundet; '?' bei None."""
    if value is None:
        return "?"
    try:
        f = float(value)
    except (TypeError, ValueError):
        return str(value)
    if decimals == 0 or f == int(f):
        s = f"{int(round(f)):,}".replace(",", ".")
    else:
        s = f"{f:,.{decimals}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return s


def _euro(value) -> str:
    """Kompakte €-Angabe (Mio./Tsd.), deutsch."""
    try:
        f = float(value or 0)
    except (TypeError, ValueError):
        return "?"
    if f >= 1_000_000:
        return f"{_num(f / 1_000_000, 2)} Mio. €"
    if f >= 1_000:
        return f"{_num(f / 1_000, 0)} Tsd. €"
    return f"{_num(f, 0)} €"


def _profile_lines(db: Session, kommune: Kommune) -> list[str]:
    finance = None
    try:
        from app.services import finance_loader
        finance = finance_loader.finance_for_kommune(kommune.osm_id, kommune.name)
    except Exception as exc:  # Finance ist optional — Zeile entfällt bei Fehler
        log.info("ai_context: finance_loader übersprungen (kommune=%s): %s", kommune.id, exc)

    prof = kommune_profile_service.build_profile(db, kommune, finance=finance)
    lines: list[str] = []

    region = ", ".join(x for x in (prof.get("bundesland"), prof.get("landkreis")) if x)
    head = f"KOMMUNE: {prof.get('name')}"
    if region:
        head += f" ({region})"
    lines.append(head)

    basis = []
    if prof.get("population"):
        basis.append(f"{_num(prof['population'], 0)} Einwohner")
    if prof.get("area_km2"):
        basis.append(f"{_num(prof['area_km2'], 1)} km²")
    elev = prof.get("elevation") or {}
    if elev.get("min") is not None and elev.get("max") is not None:
        basis.append(f"Höhe {_num(elev['min'], 0)}–{_num(elev['max'], 0)} m")
    if basis:
        lines.append("BASIS: " + " | ".join(basis))

    budget = prof.get("municipal_budget") or {}
    if budget.get("value") is not None:
        lines.append(
            f"HAUSHALT: Auszahlungen Ø {_euro(budget['value'])}/Jahr"
        )

    climate = {c.get("code"): c for c in (prof.get("climate") or [])}
    climate_parts = []
    for code in _CLIMATE_CODES:
        c = climate.get(code)
        if not c or c.get("value") is None:
            continue
        delta = c.get("delta")
        d = f" ({'+' if (delta or 0) >= 0 else ''}{_num(delta, 1)} vs. DE)" if delta is not None else ""
        climate_parts.append(f"{c.get('label')}: {_num(c['value'], 1)} {c.get('unit', '')}{d}")
    if climate_parts:
        lines.append("KLIMA (IST): " + " | ".join(climate_parts))

    return lines


def _risk_lines(db: Session, kommune_id: int) -> list[str]:
    try:
        agg = measure_service.get_risk_aggregate(db, kommune_id, apply_measures=False)
    except Exception as exc:
        log.info("ai_context: kein Risiko-Aggregat (kommune=%s): %s", kommune_id, exc)
        return ["HINWEIS: Für diese Kommune liegt noch keine abgeschlossene Berechnung vor."]

    lines: list[str] = []

    groups = agg.get("groups") or {}
    if groups:
        parts = [
            f"{g.get('label')}: Index {_num(g.get('exposed_index', g.get('index')), 0)} ({g.get('risk_class')})"
            for g in groups.values()
        ]
        lines.append("RISIKOGRUPPEN (Index 0–100, exponiert): " + " | ".join(parts))

    cost = agg.get("cost") or {}
    total = cost.get("total_eur")
    if total is not None:
        lines.append(f"ERWARTETER SCHADEN GESAMT (ohne Maßnahmen): {_euro(total)}/Jahr")

    by_risk = [r for r in (cost.get("by_risk") or []) if (r.get("cost_eur") or 0) > 0]
    by_risk = by_risk[:8]  # Top-Kostentreiber; Liste ist bereits absteigend sortiert
    if by_risk:
        lines.append("TOP-EINZELRISIKEN (Schaden/Jahr, Index, Klasse):")
        for r in by_risk:
            lines.append(
                f"- {r.get('name')}: {_euro(r.get('cost_eur'))}, "
                f"Index {_num(r.get('index'), 0)}, {r.get('risk_class')}"
            )

    return lines


def _measure_lines(db: Session, kommune_id: int) -> list[str]:
    measures = (
        db.query(AdaptationMeasure)
        .filter(
            AdaptationMeasure.kommune_id == kommune_id,
            AdaptationMeasure.demo_session_id.is_(None),
        )
        .limit(10)
        .all()
    )
    if not measures:
        return []
    lines = ["GEWÄHLTE MASSNAHMEN:"]
    for m in measures:
        s = m.impact_summary or {}
        capex = s.get("capex_eur")
        opex = s.get("opex_annual_eur")
        benefit = s.get("annual_benefit_eur")
        parts = []
        if capex is not None:
            parts.append(f"CAPEX {_euro(capex)}")
        if opex is not None:
            parts.append(f"OPEX {_euro(opex)}/a")
        if benefit is not None:
            parts.append(f"Nutzen {_euro(benefit)}/a")
        suffix = f" ({', '.join(parts)})" if parts else ""
        lines.append(f"- {m.name} [{m.measure_type}]{suffix}")
    return lines


def build_context(db: Session, kommune_id: int | None) -> str:
    """Kompakter deutscher Daten-Kontext für die aktuell gewählte Kommune.

    Ohne Kommune-Auswahl: kurzer Hinweis, dass nur allgemeine Fragen möglich sind.
    """
    if kommune_id is None:
        return (
            "HINWEIS: Aktuell ist keine Kommune ausgewählt. Es können nur allgemeine "
            "Fragen zu Klimafolgen und Klimaanpassung beantwortet werden — keine "
            "kommunenspezifischen Zahlen."
        )

    kommune = db.query(Kommune).filter(Kommune.id == kommune_id).first()
    if not kommune:
        return "HINWEIS: Die angeforderte Kommune wurde nicht gefunden."

    lines: list[str] = []
    try:
        lines += _profile_lines(db, kommune)
    except Exception as exc:
        log.warning("ai_context: Profil-Aufbau fehlgeschlagen (kommune=%s): %s", kommune_id, exc)
        lines.append(f"KOMMUNE: {kommune.name}")
    lines += _risk_lines(db, kommune_id)
    lines += _measure_lines(db, kommune_id)

    return "\n".join(lines)
