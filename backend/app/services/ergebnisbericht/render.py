"""HTML-Vorstufe und Druck des PDF-Ergebnisberichts (HTML → Playwright-Chromium → A4).

Dieselbe Druckkette wie ``scripts/html_to_pdf.py`` für die Methodik-PDFs, hier als Funktion im
Backend, damit Befehl und Dienst sie ohne Umweg über ein Skript nutzen.
"""

from __future__ import annotations

import datetime as dt
import os
from html import escape
from pathlib import Path

from app.services.ergebnisbericht.beispiel import Beispielkommune
from app.services.ergebnisbericht.sammler import Berichtsdaten, sammle
from app.services.ergebnisbericht.teile import TEILE

_CSS = os.path.join(os.path.dirname(__file__), "stil.css")

FOOTER = (
    '<div style="width:100%; font-size:7pt; font-family:\'DejaVu Sans\',sans-serif;'
    ' color:#5a6675; text-align:center; margin:0 14mm;">'
    '<span class="pageNumber"></span> / <span class="totalPages"></span></div>'
)


def teile_lesen(spec: str) -> list[int]:
    """„0,1,4,7,8“ → [0, 1, 4, 7, 8]; unbekannte Teile sind ein Fehler."""
    teile = []
    for teil in spec.split(","):
        teil = teil.strip()
        if not teil:
            continue
        nr = int(teil)
        if nr not in TEILE:
            raise ValueError(f"Teil {nr} ist noch nicht umgesetzt; verfügbar: "
                             f"{', '.join(str(t) for t in sorted(TEILE))}")
        if nr not in teile:
            teile.append(nr)
    if not teile:
        raise ValueError("Keine Teile angegeben")
    return teile


def html_dokument(daten: Berichtsdaten, teile: list[int]) -> str:
    with open(_CSS, encoding="utf-8") as fh:
        css = fh.read()
    k = daten.kommune
    abschnitte = "\n".join(f'<section class="teil">\n{TEILE[nr](daten)}\n</section>' for nr in teile)
    return f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<title>Ergebnisbericht Klimarisiken — {escape(k.name)} ({escape(k.ags)})</title>
<style>
{css}
</style>
</head>
<body>
<header class="titel">
<div class="art">Ergebnisbericht Klimarisiken</div>
<div class="kommune">{escape(k.name)}</div>
<div>Amtlicher Gemeindeschlüssel {escape(k.ags)} · {escape(daten.stand.bericht)}</div>
</header>
{abschnitte}
</body>
</html>
"""


def drucke_pdf(html_pfad: Path, pdf_pfad: Path) -> None:
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch()
        try:
            page = browser.new_page()
            page.goto(html_pfad.resolve().as_uri(), wait_until="load")
            page.pdf(
                path=str(pdf_pfad),
                format="A4",
                print_background=True,
                margin={"top": "13mm", "bottom": "17mm", "left": "14mm", "right": "14mm"},
                display_header_footer=True,
                header_template="<span></span>",
                footer_template=FOOTER,
            )
        finally:
            browser.close()


def erzeuge(kommune: Beispielkommune, teile: list[int], aus: str | os.PathLike,
            heute: dt.date | None = None) -> tuple[Path, Path]:
    """Schreibt HTML-Vorstufe und PDF; gibt (pdf, html) zurück."""
    pdf_pfad = Path(aus)
    pdf_pfad.parent.mkdir(parents=True, exist_ok=True)
    html_pfad = pdf_pfad.with_suffix(".html")
    daten = sammle(kommune, heute=heute)
    html_pfad.write_text(html_dokument(daten, teile), encoding="utf-8")
    drucke_pdf(html_pfad, pdf_pfad)
    return pdf_pfad, html_pfad
