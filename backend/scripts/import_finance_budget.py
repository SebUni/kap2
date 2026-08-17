#!/usr/bin/env python3
"""Bulk-Import der kommunalen Auszahlungen (Regionalstatistik 71717) für den
Dashboard-Chip „Kommunaler Haushalt" — regelmäßiger, server-seitiger Betreiber-Lauf.

Was das Skript tut:
  1. Setzt bei GENESIS/regionalstatistik.de einen Batch-Job für Statistik 71717
     ab (die Tabelle ist für den Direkt-Dialog zu groß), pollt bis „Fertig" und
     lädt die komplette Bundestabelle als ffcsv.
  2. Extrahiert je Berichtsgemeinde die Kennzahl AUSZ001 („Auszahlungen insgesamt,
     bereinigt", EUR) und baut einen kompakten Lookup (Kreis + Name → Jahresreihe).
  3. **Selbstheilend:** Der neue Stand wird validiert (Mindestabdeckung + Anker-
     Kommunen) und nur bei Erfolg ATOMAR über den Live-Store gelegt. Schlägt
     Download/Parsing/Validierung fehl, bleibt der ALTE Store unangetastet.

Der Chip liest ausschließlich diesen Store (netzfrei); ein fehlgeschlagener Lauf
lässt die zuletzt gültigen Werte stehen.

Voraussetzungen: gültige Regionalstatistik-Zugangsdaten in ``.env``
(``REGIONALSTATISTIK_USERNAME``/``…_PASSWORD``) sowie ``REGIONALSTATISTIK_BUDGET_ENABLED=True``.

Aufruf (aus ``backend/``):  ``python -m scripts.import_finance_budget``
Exit-Code 0 = neuer Stand übernommen, 1 = Lauf fehlgeschlagen (alter Stand bleibt).

Server-seitige Zeitsteuerung (Beispiel crontab — monatlich, jährliche Daten):
  # 5. jeden Monats, 03:30, Log anhängen
  30 3 5 * * cd /opt/lampp/htdocs/kap2/backend && \
      /pfad/zum/python -m scripts.import_finance_budget >> data/inkar/budget_import.log 2>&1
Alternativ als systemd-Timer (OnCalendar=monthly). Läuft ohne DB und ohne
Interaktion.
"""

from __future__ import annotations

import logging
import sys


def main() -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    from app.services import finance_bulk
    from app.config import settings

    if not settings.REGIONALSTATISTIK_BUDGET_ENABLED:
        logging.warning("REGIONALSTATISTIK_BUDGET_ENABLED=False — Import übersprungen.")
        return 1
    ok = finance_bulk.run_import()
    print("Import erfolgreich — neuer Stand übernommen." if ok
          else "Import fehlgeschlagen — bestehender Stand bleibt erhalten.",
          file=sys.stderr)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
