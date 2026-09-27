"""Kennzeichnung der 30 Parameter-Blöcke von #95 in der Parameterliste (T-1371, Vorgabe P1).

Kapitel 7 von ``docs/methodik/95_hitzebelastung.md`` trägt je Block eine ``kennzeichnung``
(``quelle`` | ``abschaetzung_kap3`` | ``berechnet``). Die Registry führt sie als
``evidence_class`` (``belegt`` | ``abgeschaetzt`` | ``berechnet``). Geprüft wird:

1. Die Zählung der Blöcke in Kapitel 7 ist 10 × belegt, 17 × abgeschätzt, 3 × berechnet
   (Runde 31: ``heat.beta_iso`` steht auf ``quelle``, ``heat.anteil_60_66`` ist als
   Abschätzung neu; Fortsetzung Teil 2, T-1537: ``heat.s_gek`` und
   ``heat.delta_kuehlzentren`` als Abschätzung, ``heat.h_heim`` berechnet; Teil 3, T-1538:
   ``heat.vg_in_kalibrierjahren`` und ``heat.kappung_vg`` als Abschätzung; Gegenprüfung
   T-1584: ``heat.s_gek_kalib`` als Abschätzung). Die Registry führt alle Blöcke mit
   derselben Zählung (Parameter angelegt in T-1606).
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


def _bloecke_mit_parameter() -> dict[str, dict]:
    """Blöcke aus Kapitel 7; seit T-1606 hat jeder einen Registry-Parameter."""
    return _bloecke()


def _zaehlung(klassen: Counter) -> dict[str, int]:
    return {k: klassen[k] for k in ("belegt", "abgeschaetzt", "berechnet")}


def test_zaehlung_der_kennzeichnungen_in_kapitel_7_10_17_3():
    kapitel_7 = Counter(_KLASSE[b["kennzeichnung"]] for b in _bloecke().values())
    print(_zaehlung(kapitel_7))
    assert _zaehlung(kapitel_7) == {"belegt": 10, "abgeschaetzt": 17, "berechnet": 3}


def test_zaehlung_der_kennzeichnungen_in_der_registry_10_17_3():
    soll = Counter(_KLASSE[b["kennzeichnung"]] for b in _bloecke_mit_parameter().values())
    nach_block = _nach_block()
    ist = Counter()
    for bid in _bloecke_mit_parameter():
        klassen = {p["evidence_class"] for p in nach_block[bid]}
        assert len(klassen) == 1, (bid, klassen)
        ist[klassen.pop()] += 1
    print(_zaehlung(ist))
    assert _zaehlung(ist) == {"belegt": 10, "abgeschaetzt": 17, "berechnet": 3}
    assert dict(soll) == dict(ist)


def test_jeder_parameter_traegt_die_klasse_seines_blocks():
    nach_block = _nach_block()
    abweichungen = []
    for bid, block in _bloecke_mit_parameter().items():
        soll = _KLASSE[block["kennzeichnung"]]
        for p in nach_block[bid]:
            if p["evidence_class"] != soll:
                abweichungen.append((bid, p["id"], soll, p["evidence_class"]))
    assert not abweichungen, abweichungen


def test_belegte_bloecke_nennen_ihre_quelle():
    nach_block = _nach_block()
    ohne = []
    for bid, block in _bloecke_mit_parameter().items():
        if block["kennzeichnung"] != "quelle":
            continue
        for p in nach_block[bid]:
            if not (p.get("source") or p.get("source_detail")):
                ohne.append((bid, p["id"]))
    assert not ohne, ohne


if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main([__file__, "-q", "-s"]))
