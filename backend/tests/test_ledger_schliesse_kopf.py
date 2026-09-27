"""Test für T-1533-ceo: `ledger.py --schliesse` darf beim Nachziehen der
Kopfzählung nur die Überschriftszeile selbst treffen, nicht jedes Vorkommen der
Zeichenkette im Fließtext.

Anlass (Urteil zu T-1498-methodik_manager, Frage 3 des Prüfers): Im Ledger von
#98 steht `## Geschlossene Befunde (243)` nicht nur als Überschrift, sondern
auch in Befundtexten und Prüfausdrücken (Befunde 365, 368, 388). Die beiden
`re.sub`-Aufrufe in `cmd_schliesse` liefen bisher unverankert über den ganzen
Text und ohne `count`-Grenze — jedes Vorkommen der Kopfzahl wurde mitgeschrieben,
auch mitten in Prosa und in Prüfausdrücken. Ein Prüfausdruck, der die Kopfzahl
sucht, bestätigte sich damit selbst; alte Befundtexte änderten sich nachträglich.

Der Mini-Ledger enthält Befund 1 (offen, grüner Prüfausdruck — wird geschlossen)
und Befund 2 (bereits geschlossen; sein Befundtext **und** seine
Prüfausdruck-Zelle enthalten die Zeichenkette `## Geschlossene Befunde (1)`
mitten in der Zeile, nicht als eigene Überschriftszeile). Nach dem Schließen
darf sich nur die echte Überschriftszeile ändern.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import ledger  # noqa: E402

LEDGER_PFAD = Path(__file__).resolve().parents[2] / "backend" / "scripts" / "ledger.py"

MINI_LEDGER = """# Befunde 99 (Test)

## Geschlossene Befunde (1)

| Nr | Befund (Ort · Art) | Kat | Status | Nachweis | Prüfausdruck |
|---|---|---|---|---|---|
| 1 | Bericht Kap. 1 · Lücke — Beispielbefund mit grünem Ausdruck | B | offen | – | `python3 -c "pass"` |
| 2 | Bericht Kap. 2 · Lücke — Text erwähnt mitten im Satz "## Geschlossene Befunde (1)" als Zitat | B | geschlossen | Rev. 1 | `echo "## Geschlossene Befunde (1)"` |
"""


def test_schliesse_zieht_nur_ueberschriftszeile_nach(tmp_path: Path) -> None:
    pfad = tmp_path / "BEFUNDE_99.md"
    pfad.write_text(MINI_LEDGER, encoding="utf-8")

    rc = ledger.cmd_schliesse(pfad)
    assert rc == 0

    text = pfad.read_text(encoding="utf-8")

    # Überschrift trägt die neue Zahl (beide Befunde jetzt geschlossen).
    ueberschriften = re.findall(r"^## Geschlossene Befunde \(\d+\)$", text, flags=re.M)
    assert ueberschriften == ["## Geschlossene Befunde (2)"]

    # Befundtext und Prüfausdruck-Zelle von Befund 2 sind zeichengleich unverändert
    # — insbesondere trägt keine der beiden noch die alte Kopfzahl, weil sie nie
    # verändert werden durften.
    assert ('Text erwähnt mitten im Satz "## Geschlossene Befunde (1)" als Zitat'
            in text)
    assert 'echo "## Geschlossene Befunde (1)"' in text

    befunde = {b.nr: b for b in ledger.parse(pfad)}
    assert befunde["1"].lage == "geschlossen"
    assert befunde["2"].lage == "geschlossen"


def test_rotprobe_alter_unverankerter_ausdruck_schlaegt_fehl(tmp_path: Path) -> None:
    """Belegt, dass der alte, nicht verankerte Ausdruck genau diesen Fall verletzt.

    Baut eine Kopie von `ledger.py` mit dem alten `re.sub` (ohne `^…$`/`re.M` und
    ohne `count=1`), führt darauf dieselbe Prüfung wie oben aus und erwartet,
    dass sie fehlschlägt — die Rotprobe für dieses Ticket.
    """
    alt_text = LEDGER_PFAD.read_text(encoding="utf-8")
    neu_zeile_1 = ('    t = re.sub(r"^## Offene Befunde \\(\\d+\\)$", '
                   'f"## Offene Befunde ({n_offen})", t,\n'
                   '               count=1, flags=re.M)\n')
    neu_zeile_2 = ('    t = re.sub(r"^## Geschlossene Befunde \\(\\d+\\)$", '
                   'f"## Geschlossene Befunde ({n_zu})", t,\n'
                   '               count=1, flags=re.M)\n')
    assert neu_zeile_1 in alt_text
    assert neu_zeile_2 in alt_text
    alt_variante = alt_text.replace(
        neu_zeile_1,
        '    t = re.sub(r"## Offene Befunde \\(\\d+\\)", '
        'f"## Offene Befunde ({n_offen})", t)\n',
    ).replace(
        neu_zeile_2,
        '    t = re.sub(r"## Geschlossene Befunde \\(\\d+\\)", '
        'f"## Geschlossene Befunde ({n_zu})", t)\n',
    )
    assert alt_variante != alt_text

    alte_kopie = tmp_path / "ledger_alt.py"
    alte_kopie.write_text(alt_variante, encoding="utf-8")

    ledger_pfad = tmp_path / "BEFUNDE_99.md"
    ledger_pfad.write_text(MINI_LEDGER, encoding="utf-8")

    code = f"""
import sys
sys.path.insert(0, {str(tmp_path)!r})
import ledger_alt as ledger
from pathlib import Path
rc = ledger.cmd_schliesse(Path({str(ledger_pfad)!r}))
text = Path({str(ledger_pfad)!r}).read_text(encoding="utf-8")
assert rc == 0
assert 'Text erwähnt mitten im Satz "## Geschlossene Befunde (1)" als Zitat' in text, \\
    "ROTPROBE: Befundtext wurde vom unverankerten Ausdruck mitgeschrieben"
"""
    r = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
    assert r.returncode != 0
    assert "ROTPROBE" in r.stdout + r.stderr
