"""Gemeinsame Klasse-B-Testwirkung für die Sichtprüfung und die Lite-Ansichten.

Verwechslungssperre Klasse A/B (Vorhaben T-0563): Der ausgelieferte Katalog führt
keine Wirkung mit ``"euro_layer": False``. Damit die Sperre trotzdem an einem echten
Klasse-B-Fall geprüft werden kann, legt dieses Modul eine Testwirkung an und trägt sie
per monkeypatch in ``catalog.RISKS`` und ``catalog.RISKS_BY_CODE`` ein. Der Katalog
selbst bleibt unverändert; nach dem Test stellt monkeypatch den Ausgangszustand her.
"""

from __future__ import annotations

from app.data import catalog

KLASSE_B_CODE = "TEST_KLASSE_B_SICHTPRUEFUNG"
KLASSE_B_NAME = "Testwirkung Klasse B (Sichtprüfung)"
KOSTENSATZ = 1000.0


def klasse_b_wirkung() -> dict:
    """Klasse-B-Wirkung (``euro_layer: False``) mit Kostensatz > 0 — ohne die Sperre
    trüge sie einen Betrag in Summe, Nutzen und Exporte."""
    return {
        "code": KLASSE_B_CODE,
        "name": KLASSE_B_NAME,
        "group": "heat",
        "outcome_unit": "Fälle/Jahr",
        "ref_value": 10.0,
        "scale": "pop",
        "cost_per_outcome_eur": KOSTENSATZ,
        "cost_dimension": "health",
        "cost_source": "Testquelle",
        "euro_layer": False,
    }


def wirkung_einhaengen(monkeypatch) -> dict:
    """Trägt die Testwirkung in ``catalog.RISKS`` und ``catalog.RISKS_BY_CODE`` ein."""
    risk = klasse_b_wirkung()
    monkeypatch.setitem(catalog.RISKS_BY_CODE, risk["code"], risk)
    monkeypatch.setattr(catalog, "RISKS", list(catalog.RISKS) + [risk])
    return risk
