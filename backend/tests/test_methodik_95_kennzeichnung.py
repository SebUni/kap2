"""Kennzeichnung der 23 Parameter-Blöcke von #95 in der Parameterliste (T-1371, Vorgabe P1).

Kapitel 7 von ``docs/methodik/95_hitzebelastung.md`` trägt je Block eine ``kennzeichnung``
(``quelle`` | ``abschaetzung_kap3`` | ``berechnet``). Die Registry führt sie als
``evidence_class`` (``belegt`` | ``abgeschaetzt`` | ``berechnet``). Geprüft wird:

1. Die Zählung der Blöcke ist 9 × belegt, 11 × abgeschätzt, 3 × berechnet.
2. Jeder Registry-Parameter eines Blocks trägt die Klasse seines Blocks.
3. Jeder als „belegt“ gekennzeichnete Block hat eine Quellenangabe in der Parameterliste.
"""

from __future__ import annotations

import os
import sys
from collections import Counter

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.services import parameter_registry  # noqa: E402
from test_methodik_95_bloecke import _bloecke  # noqa: E402

_KLASSE = {"quelle": "belegt", "abschaetzung_kap3": "abgeschaetzt", "berechnet": "berechnet"}


def _nach_block() -> dict[str, list[dict]]:
    nach_block: dict[str, list[dict]] = {}
    for p in parameter_registry.catalog_parameters():
        if p.get("methodik_block"):
            nach_block.setdefault(p["methodik_block"], []).append(p)
    return nach_block


def test_zaehlung_der_kennzeichnungen_9_11_3():
    soll = Counter(_KLASSE[b["kennzeichnung"]] for b in _bloecke().values())
    nach_block = _nach_block()
    ist = Counter()
    for bid in _bloecke():
        klassen = {p["evidence_class"] for p in nach_block[bid]}
        assert len(klassen) == 1, (bid, klassen)
        ist[klassen.pop()] += 1
    zaehlung = {"belegt": ist["belegt"], "abgeschaetzt": ist["abgeschaetzt"],
                "berechnet": ist["berechnet"]}
    print(zaehlung)
    assert zaehlung == {"belegt": 9, "abgeschaetzt": 11, "berechnet": 3}
    assert dict(soll) == dict(ist)


def test_jeder_parameter_traegt_die_klasse_seines_blocks():
    nach_block = _nach_block()
    abweichungen = []
    for bid, block in _bloecke().items():
        soll = _KLASSE[block["kennzeichnung"]]
        for p in nach_block[bid]:
            if p["evidence_class"] != soll:
                abweichungen.append((bid, p["id"], soll, p["evidence_class"]))
    assert not abweichungen, abweichungen


def test_belegte_bloecke_nennen_ihre_quelle():
    nach_block = _nach_block()
    ohne = []
    for bid, block in _bloecke().items():
        if block["kennzeichnung"] != "quelle":
            continue
        for p in nach_block[bid]:
            if not (p.get("source") or p.get("source_detail")):
                ohne.append((bid, p["id"]))
    assert not ohne, ohne


if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main([__file__, "-q", "-s"]))
