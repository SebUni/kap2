"""Bundesvergleich der fünf KWRA-Systembereiche (Konformitäts-Checkliste Zeile 10).

Führt die quellenfest übernommenen Bausteine aus KWRA 2021, Teilbericht 6, Kap. 7
(S. 146–154) zu einer Auslieferung zusammen:

* ``kwra_kap7_risiko`` — Risiko ohne Anpassung, Gewissheit, Handlungserfordernisse,
  klimatische Einflüsse (A2, A6, A7, A9);
* ``kwra_kap7_anpassung`` — Wirksamkeit, Klimarisiko mit Anpassung, Anpassungsdauer,
  Grenzen der Anpassung (A3–A5);
* ``kwra_kap7_schluesse`` — Schlüsse für die Anpassungsplanung und methodische Grenze
  des Vergleichs (A10, A11).

Es wird nichts gerechnet; die Werte sind die der Bundesanalyse und nicht der
Produkt-Risikoindex (dazu ``systembereiche.systembereich_auswertung``).
"""

from __future__ import annotations

from copy import deepcopy

from app.data import catalog
from app.data import kwra_kap7_anpassung as anpassung
from app.data import kwra_kap7_risiko as risiko
from app.data import kwra_kap7_schluesse as schluesse


def bundesanalyse_vergleich() -> dict:
    """Bundesvergleich je Systembereich in der Reihenfolge ``catalog.KWRA_SYSTEMBEREICHE``.

    Rückgabe: ``{"quelle", "bereiche", "schluesse", "methodische_grenze", "abbildung_24"}``;
    je Bereich ``systembereich``, ``risiko`` (Risiko-Block der Bundesanalyse) und
    ``anpassung`` (vier Anpassungsblöcke).
    """
    bereiche = [
        {
            "systembereich": name,
            "risiko": deepcopy(risiko.BEREICHSVERGLEICH_RISIKO[name]),
            "anpassung": deepcopy(anpassung.BEREICHSVERGLEICH_ANPASSUNG[name]),
        }
        for name in catalog.KWRA_SYSTEMBEREICHE
    ]
    return {
        "quelle": risiko.QUELLE,
        "bereiche": bereiche,
        "schluesse": deepcopy(schluesse.SCHLUESSE_ANPASSUNGSPLANUNG),
        "methodische_grenze": deepcopy(schluesse.METHODISCHE_GRENZE),
        "abbildung_24": deepcopy(risiko.ABBILDUNG_24),
    }
