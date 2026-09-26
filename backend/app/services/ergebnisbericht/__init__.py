"""PDF-Ergebnisbericht für eine Kommune (M2 Paket 4, Vorhaben T-1267-ceo).

Kette: Sammler (``sammler.py``) → Teile als HTML (``teile.py``) → HTML-Vorstufe mit Stylesheet
(``stil.css``) → Playwright-Chromium → A4-PDF (``render.py``). Aufruf über die CLI:

    python -m app.cli ergebnisbericht --beispiel warmsen --teile 0,1,4,7,8 --aus /tmp/bericht.pdf

Die HTML-Vorstufe liegt neben dem PDF (gleicher Name, Endung ``.html``).
"""

from app.services.ergebnisbericht.render import erzeuge  # noqa: F401
