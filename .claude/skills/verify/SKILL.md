---
name: verify
description: KAP2 end-to-end im Browser verifizieren (Vite + FastAPI + Playwright headless)
---

# KAP2 verifizieren

## Server

Meist laufen beide schon — erst prüfen:

```bash
curl -s -o /dev/null -w '%{http_code}' http://localhost:5173/   # Vite-Frontend
curl -s -o /dev/null -w '%{http_code}' http://localhost:8000/api/health  # FastAPI-Backend
```

Sonst `./start-dev.sh` (beides) oder `cd frontend && npm run dev` (Landing/Demo
funktioniert dank Snapshot `oschatz-landing.json` ohne Backend).

## Browser-Automation

Playwright ist NUR als Python-Paket in miniconda installiert (kein npm-Paket!):

```bash
/home/basti/miniconda3/bin/python script.py   # from playwright.sync_api import sync_playwright
```

Chromium-Binaries liegen in `~/.cache/ms-playwright`.

## Flows

- **Landing** `/`: zwei MapLibre-Widgets (`canvas.maplibregl-canvas`), Snapshot-Daten, kein Login.
- **Login** `/login`: Dev-Admin `basti.attack@gmail.com` / `kap2-admin-dev`
  (`input[type=email]`, `input[type=password]`, `button[type=submit]`).
  Achtung: Admin landet nach Login auf `/admin/users` — danach explizit `/app` ansteuern.
- **Produktkarte**: auf `/app` in `input[placeholder*="Kommune"]` z. B. "Oschatz" tippen,
  Dropdown-Eintrag **anklicken** (Tastatur ArrowDown/Enter wählt nicht aus),
  dann Tab `Karte`. Ladeoverlay "Karte wird geladen" abwarten (kann >30 s dauern,
  Assessment läuft ggf. serverseitig).
- **Deutschland-Karte** `/deutschland`: öffentlich, Gemeinde-Choropleth.
