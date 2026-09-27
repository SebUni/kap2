"""Kennzeichnung der Kostensätze in Teil 4 wie in Teil 7 (T-1491, Vorgabe P1).

Der Formatpilot (T-1414) hatte in der Rechenkette von Teil 4 für die Zeilen „× Kostensatz je
Lebensjahr“ und „× Kostensatz je Fall“ feste Quellentexte stehen, während Teil 7 dieselben
Parameter über ``evidence_class`` als „ausgewiesene Abschätzung von KAP3“ bzw. mit Quelle führt.
Dieser Test erzeugt beide Teile für die Beispielkommune Warmsen und stellt fest, dass die
Kennzeichnung, die in Teil 7 für den jeweiligen Parameter steht, auch im Quellentext der
zugehörigen Zeile in Teil 4 steht — also aus denselben Parameterdaten kommt, nicht aus
abgeschriebenem Text.
"""

from __future__ import annotations

import os
import re
import sys

HIER = os.path.dirname(os.path.abspath(__file__))
BACKEND = os.path.dirname(HIER)
sys.path.insert(0, BACKEND)

from app.services.ergebnisbericht import teile  # noqa: E402
from app.services.ergebnisbericht.beispiel import MORB, MORT, beispiel  # noqa: E402
from app.services.ergebnisbericht.sammler import sammle  # noqa: E402

# Zeile der Rechenkette (Teil 4) → Zeile des Parameterverzeichnisses (Teil 7), über denselben
# Registry-Parameter ``risks.<code>.cost_per_outcome``.
ZEILEN = [
    ("Kostensatz je Lebensjahr", "× Kostensatz je Lebensjahr", MORT),
    ("Kostensatz je Fall", "× Kostensatz je Fall", MORB),
]


def _teil4_quelle(html: str, ebene: str) -> str:
    """Quellentext der Rechenketten-Zeile ``ebene`` in Teil 4."""
    muster = rf"<tr><td>{re.escape(ebene)}</td><td[^>]*>.*?</td><td>(.*?)</td></tr>"
    treffer = re.search(muster, html)
    assert treffer, f"Zeile {ebene!r} nicht in Teil 4 gefunden"
    return treffer.group(1)


def _teil7_kennzeichnung(d, param_id: str) -> str:
    """Kennzeichnung (Quelle oder ausgewiesene Abschätzung von KAP3), wie Teil 7 sie für den
    Parameter ``param_id`` aus ``d.parameter`` bildet (dieselbe Funktion, die Teil 7 nutzt)."""
    for p in d.parameter:
        if p.get("id") == param_id:
            return teile._herkunft(p)
    raise AssertionError(f"Parameter {param_id!r} nicht in d.parameter gefunden")


def test_kostensaetze_in_teil4_wie_in_teil7():
    d = sammle(beispiel("warmsen"))
    html4 = teile.teil_4(d)
    html7 = teile.teil_7(d)
    assert html7  # Teil 7 wird erzeugt (und damit dieselben Parameterdaten geprüft)

    for _, ebene_teil4, code in ZEILEN:
        erwartet = _teil7_kennzeichnung(d, f"risks.{code}.cost_per_outcome")
        quelle_teil4 = _teil4_quelle(html4, ebene_teil4)
        assert erwartet in quelle_teil4, (
            f"Kennzeichnung aus Teil 7 ({erwartet!r}) steht nicht im Quellentext von Teil 4 "
            f"({quelle_teil4!r}) für {ebene_teil4!r}"
        )
        # Rot-Probe-Gegenstück: der alte feste Text darf dort nicht mehr allein stehen.
        assert quelle_teil4 != "UBA Methodenkonvention 4.0"
        assert quelle_teil4 != "Destatis-Kostennachweis 2023"
