---
description: Erzeugt das Lese-PDF eines Methodik-Berichts (KaTeX-Formelsatz, M0-Optik) aus der Markdown-Quelle
argument-hint: <risiko-nr>
---

Risiko-Nummer: $ARGUMENTS

Führe `scripts/export_methodik_pdf.sh $ARGUMENTS` aus und melde den erzeugten PDF-Pfad.

Pipeline: pandoc (Markdown → HTML, KaTeX aus `frontend/node_modules`) → Playwright-Chromium
(HTML → A4-PDF). Stil: `scripts/methodik_report.css` (angelehnt an
`docs/render/METHODIK_M0_GESUNDHEIT.html`); Druck-Treiber: `scripts/html_to_pdf.py`.

Das Skript erzeugt anschließend automatisch die **Wirkungsmechanismus-Vorschau**
`docs/methodik/<slug>_wirkungsmechanismus.html` (`scripts/wirkungsmechanismus_preview.py`):
eine eigenständige HTML-Datei, die das echte Produkt-Wirkungsdiagramm (KAP3,
`LineageFlowDiagram`) rendert — für integrierte Risiken direkt aus Backend/Registry, für
noch nicht integrierte aus dem im Bericht hergeleiteten Modell (Banner kennzeichnet das).
Melde auch diesen Pfad. Für ein neues Risiko ohne Vorschau-Definition erscheint nur ein
Hinweis — dann im Generator einen Graph-Builder ergänzen. Frontend-Bundle:
`frontend/vite.preview.config.ts` (baut automatisch, falls `frontend/preview-dist/` fehlt;
nach Änderungen an Diagramm-Komponenten einmal neu bauen).

Fehlerbehandlung:

- **Abhängigkeiten fehlen:** melde den fehlenden Baustein samt Installationsbefehl
  (pandoc: `sudo apt install pandoc`; Playwright: `pip install playwright && playwright
  install chromium`; KaTeX: `npm install` im Ordner `frontend/`) — installiere nichts
  selbst mit sudo.
- **Layout-Probleme (überlaufende Tabellen, abgeschnittene Inhalte):** Die Markdown-Quelle
  bleibt unangetastet. Zuerst prüfen, ob eine Anpassung in `scripts/methodik_report.css`
  das Problem generisch löst (Schriftgrad, Umbruchregeln). Nur wenn es ein Einzelfall einer
  Datei ist: Kopie im Scratchpad anlegen, dort die Darstellung anpassen und die Kopie an den
  regulären Zielpfad exportieren. Melde, was angepasst wurde.
- **Formeln nicht gerendert** (rohes TeX im PDF): prüfen, ob die Formel gültiges
  KaTeX-kompatibles TeX ist; Delimiter sind `$…$`, `$$…$$`, `\(…\)`.
- **Nach jedem Export:** Stichprobe rendern (`pdftoppm -png -r 60`) und auf Überläufe/
  Layoutbrüche sichten, bevor Vollzug gemeldet wird.

Das PDF ist reiner Export für Menschen — die Quelle ist und bleibt die Markdown-Datei.
