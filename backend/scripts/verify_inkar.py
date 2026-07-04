#!/usr/bin/env python
"""Live-Verifikation der Regionalstatistik/INKAR-Anbindung (Report §B3).

Prüft gegen die echte GENESIS-API (regionalstatistik.de):
  1. Login (POST /helloworld/logincheck, Header-Auth).
  2. Für einen Beispiel-AGS: Steuerkraft- und Arbeitslosen-Tabelle abrufen,
     Roh-ffcsv (Kopf) anzeigen, parsen und in die V-Indizes normieren.

Aufruf (mit gesetzten Zugangsdaten in backend/.env):
    cd backend && PYTHONPATH=. python scripts/verify_inkar.py [AGS]

Standard-AGS: 05315 (Köln). Bei gültigen Zugangsdaten sollten die Tabellen
konkrete Werte liefern; sonst zeigt das Skript die GENESIS-Fehlermeldung.
"""

from __future__ import annotations

import sys

import httpx

from app.config import settings
from app.services import inkar_loader as ik


def main(ags: str = "05315") -> int:
    base = settings.REGIONALSTATISTIK_API_BASE.rstrip("/")
    headers = ik._auth_headers()
    print(f"Base: {base}")
    print(f"Auth: {'token' if settings.REGIONALSTATISTIK_TOKEN else 'username/password'} "
          f"| konfiguriert: {headers is not None}")
    if headers is None:
        print("→ Keine Zugangsdaten in .env — Ableitung würde neutralen Fallback (50) nutzen.")
        return 2

    with httpx.Client(timeout=60, follow_redirects=True) as c:
        r = c.post(f"{base}/helloworld/logincheck", headers=headers, data={"language": "de"})
        print(f"\nLOGINCHECK {r.status_code}: {r.text[:200]}")
        login_ok = r.status_code == 200 and "Fehler" not in r.text
        print("→ Login gültig:", login_ok)

    for label, code in (("Steuerkraft", settings.REGIONALSTATISTIK_TABLE_TAX),
                        ("Arbeitslosenquote", settings.REGIONALSTATISTIK_TABLE_UNEMPLOYMENT)):
        print(f"\n=== {label} ({code}) für AGS {ags} ===")
        with httpx.Client(timeout=90, follow_redirects=True) as c:
            r = c.post(f"{base}/data/table", headers=headers, data={
                "name": code, "area": "all", "format": "ffcsv", "language": "de",
                "compress": "false", "transpose": "false", "regionalkey": ags,
            })
        ctype = r.headers.get("content-type", "")
        print(f"HTTP {r.status_code} {ctype[:30]}")
        if "json" in ctype:
            print("GENESIS-Meldung:", r.text[:300])
            continue
        head = "\n".join(r.text.splitlines()[:6])
        print("ffcsv-Kopf:\n" + head)
        print("→ geparster Wert:", ik._parse_ffcsv_value(r.text, ags))

    print("\n=== Abgeleitete Indizes (socioeconomic_for_kommune-Pfad) ===")
    raw = ik.fetch_socioeconomic(ags)
    print("Rohgrößen:", raw)
    print("Indizes  :", ik.socioeconomic_indices(raw or {}))
    return 0 if raw else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1] if len(sys.argv) > 1 else "05315"))
