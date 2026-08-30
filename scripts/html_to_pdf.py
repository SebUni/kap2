#!/usr/bin/env python3
"""Druckt eine lokale HTML-Datei per Playwright-Chromium als A4-PDF.

Aufruf: html_to_pdf.py <eingabe.html> <ausgabe.pdf>
Wartet auf KaTeX-Formelsatz (falls vorhanden) und setzt eine dezente
Seitenzahl-Fußzeile.
"""
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

FOOTER = (
    '<div style="width:100%; font-size:7pt; font-family:\'DejaVu Sans\',sans-serif;'
    ' color:#5a6675; text-align:center; margin:0 14mm;">'
    '<span class="pageNumber"></span> / <span class="totalPages"></span></div>'
)


def main() -> None:
    if len(sys.argv) != 3:
        sys.exit("Aufruf: html_to_pdf.py <eingabe.html> <ausgabe.pdf>")
    src = Path(sys.argv[1]).resolve()
    out = Path(sys.argv[2]).resolve()

    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--allow-file-access-from-files"])
        page = browser.new_page()
        page.goto(src.as_uri(), wait_until="networkidle")
        try:
            page.wait_for_selector(".katex", timeout=15000)
        except Exception:
            pass  # Dokument ohne Formeln
        page.wait_for_timeout(300)
        page.pdf(
            path=str(out),
            format="A4",
            print_background=True,
            margin={"top": "13mm", "bottom": "17mm", "left": "14mm", "right": "14mm"},
            display_header_footer=True,
            header_template="<span></span>",
            footer_template=FOOTER,
        )
        browser.close()


if __name__ == "__main__":
    main()
