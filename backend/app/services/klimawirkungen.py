"""Eine Regel für jede Klimawirkung: ``klimawirkungen(by_risk)`` (T-1470-cto).

Die Kostentabelle „Erwartete Schäden je Risiko" fasst Zeilen mit derselben ``kwra_id`` zu einer
Summenzeile zusammen — bisher als reine Frontend-Regel (``bloecke()`` in ``CostTablesSection.tsx``,
T-1432-ceo). Diese Funktion ist dieselbe Regel im Backend, damit jede Klimawirkung (amtlicher Name +
Nummer + Jahresbetrag) auch dort als ein Eintrag vorliegt, wo Kartenebenen, Exporte oder andere
Verbraucher nicht durchs Frontend gehen (T-1461-ceo Punkt 3, Pakete 6/7/8/10).

Regel (identisch zu ``bloecke()``):
- Klasse-A-Zeilen (``has_euro_layer`` nicht ``False``) mit derselben ``kwra_id`` bilden einen Eintrag.
  Fehlt ``kwra_id`` in der Zeile, wird sie aus ``catalog.RISKS_BY_CODE[code]`` ergänzt.
- ``cost_eur`` ist die Summe der Teilzeilen mit Betrag (``cost_eur`` nicht ``None``) ohne die Codes in
  ``catalog.NON_ADDITIVE_RISK_CODES`` (Doppelzählung §3.7); bei Klasse B, oder wenn keine Teilzeile
  einen Betrag trägt, ist ``cost_eur`` ``None`` — nie 0 (Vorgabe P2, T-1560-ceo).
- ``risk_class`` ist bei einer Teilzeile deren Klasse, bei mehreren die höchste (``hoch`` > ``mittel``
  > ``gering``); Teilzeilen ohne Klasse zählen nicht mit, trägt keine Teilzeile eine Klasse ist das
  Feld ``None`` (T-1560-ceo).
- ``teile`` listet die Teilzeilen nur, wenn es mindestens zwei sind; eine Klimawirkung mit genau
  einer Zeile bekommt keine Summenzeile (``teile: []``).
- Klasse-B-Zeilen bleiben je Zeile ein eigener Eintrag, tragen aber ebenfalls Name und Nummer.
- Sortierung: Klasse A nach ``cost_eur`` absteigend, Klasse-A-Einträge ohne Betrag dahinter (in
  Eingabereihenfolge), danach Klasse B in der Reihenfolge des Backends (``by_risk``-Eingabereihenfolge).
"""

from __future__ import annotations

from app.data import catalog

_RISK_CLASS_RANG = {"hoch": 2, "mittel": 1, "gering": 0}


def _hoechste_risk_class(rows: list[dict]) -> str | None:
    klassen = [r["risk_class"] for r in rows if r.get("risk_class") in _RISK_CLASS_RANG]
    if not klassen:
        return None
    return max(klassen, key=lambda k: _RISK_CLASS_RANG[k])


def _kwra_id(row: dict) -> int | None:
    """``kwra_id`` der Zeile — fehlt sie, aus dem Katalog nachschlagen (Ticket-Vorgabe)."""
    if "kwra_id" in row:
        return row["kwra_id"]
    katalog_zeile = catalog.RISKS_BY_CODE.get(row["code"], {})
    return katalog_zeile.get("kwra_id")


def _kwra_name(row: dict) -> str:
    """Amtlicher Name der Klimawirkung aus dem Katalog, sonst der Zeilenname."""
    katalog_zeile = catalog.RISKS_BY_CODE.get(row["code"], {})
    return katalog_zeile.get("kwra_name") or row.get("name")


def _bezeichnung(name: str, kwra_id: int | None) -> str:
    if kwra_id is None:
        return name
    return f"{name} (#{kwra_id})"


def _eintrag(kwra_id: int | None, name: str, rows: list[dict], has_euro_layer: bool) -> dict:
    if has_euro_layer:
        betraege = [r["cost_eur"] for r in rows
                    if r["cost_eur"] is not None and r["code"] not in catalog.NON_ADDITIVE_RISK_CODES]
        cost_eur = sum(betraege) if betraege else None
    else:
        cost_eur = None
    return {
        "kwra_id": kwra_id,
        "name": name,
        "bezeichnung": _bezeichnung(name, kwra_id),
        "cost_eur": cost_eur,
        "risk_class": _hoechste_risk_class(rows),
        "has_euro_layer": has_euro_layer,
        "codes": [r["code"] for r in rows],
        "teile": rows if len(rows) > 1 else [],
    }


def klimawirkungen(by_risk: list[dict]) -> list[dict]:
    """Eine Klimawirkung, ein Eintrag — Klasse A gruppiert nach ``kwra_id``, Klasse B je Zeile.

    ``by_risk`` bleibt unverändert; diese Funktion liest nur.
    """
    klasse_a_rows = [r for r in by_risk if r.get("has_euro_layer") is not False]
    klasse_b_rows = [r for r in by_risk if r.get("has_euro_layer") is False]

    # Klasse A: Zeilen mit gleicher kwra_id (sofern vorhanden) zu einer Gruppe fassen,
    # in der Reihenfolge des ersten Auftretens; kwra_id None gruppiert nicht (jede
    # solche Zeile bleibt ein eigener Eintrag).
    gruppen: dict[int, list[dict]] = {}
    reihenfolge: list[tuple[int | None, list[dict]]] = []
    for row in klasse_a_rows:
        kwra_id = _kwra_id(row)
        if kwra_id is not None and kwra_id in gruppen:
            gruppen[kwra_id].append(row)
            continue
        rows = [row]
        if kwra_id is not None:
            gruppen[kwra_id] = rows
        reihenfolge.append((kwra_id, rows))

    klasse_a = [
        _eintrag(kwra_id, _kwra_name(rows[0]), rows, has_euro_layer=True)
        for kwra_id, rows in reihenfolge
    ]
    klasse_a.sort(key=lambda e: (e["cost_eur"] is None, -(e["cost_eur"] or 0.0)))

    klasse_b = [
        _eintrag(_kwra_id(row), _kwra_name(row), [row], has_euro_layer=False)
        for row in klasse_b_rows
    ]

    return klasse_a + klasse_b
