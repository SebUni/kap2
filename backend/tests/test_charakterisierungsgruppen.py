"""T-0450: KWRA-Charakterisierungsgruppe je Klimawirkung (Konformitäts-Checkliste Zeile 7).

Prüft ``app.services.charakterisierung``:
(a) für jede der fünf Gruppen gibt es eine Eingangskombination (Anpassungspotenzial,
    Gewissheitsstufe), die genau diese Gruppe liefert,
(b) jede Klimawirkung des Katalogs, die eine Dringlichkeitseinstufung trägt, erhält
    genau einen der fünf Werte und nie ``None``,
(c) für dieselben Eingaben liefert die Funktion zweimal dasselbe Ergebnis.

Die Dringlichkeitseinstufung (SD/D, KWRA TB6 Tabelle 25/26) führt der Katalog selbst
noch nicht (Checklistenzeile 6); sie wird hier über ``kwra_id`` aus
``docs/KATALOG_KRITIK.md`` Anhang A gelesen.
"""

from __future__ import annotations

import os
import re
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.data import catalog  # noqa: E402
from app.services import charakterisierung  # noqa: E402

FUENF = (
    "Umsetzung",
    "Entwicklung",
    "Entwicklung unter Unsicherheit",
    "Innovation",
    "Innovation unter Unsicherheit",
)

KRITIK = os.path.join(os.path.dirname(__file__), "..", "..", "docs", "KATALOG_KRITIK.md")

#: Je Gruppe eine Eingangskombination (p, Gewissheitsstufe).
BEISPIELE = {
    "Umsetzung": (0.6, "gering"),
    "Entwicklung": (0.3, "mittel"),
    "Entwicklung unter Unsicherheit": (0.3, "gering"),
    "Innovation": (0.0, "hoch"),
    "Innovation unter Unsicherheit": (0.0, "sehr gering"),
}


def _massnahme_mit(code: str, reduktion: float) -> list[dict]:
    return [{"code": "TEST_MASSNAHME", "linked_risk_codes": [code],
             "default_reduction": reduktion, "effect_target": ["vulnerability"]}]


def _dringlich_eingestufte_kwra_ids() -> set[int]:
    """KWRA-Nummern mit Dringlichkeit SD oder D aus Anhang A von KATALOG_KRITIK.md."""
    ids: set[int] = set()
    with open(KRITIK, encoding="utf-8") as fh:
        for zeile in fh:
            m = re.match(r"^\|\s*(\d+)\s*\|[^|]*\|[^|]*\|\s*(SD|D)\s*\|", zeile)
            if m:
                ids.add(int(m.group(1)))
    return ids


def test_konstanten_fuenf_gruppen():
    assert charakterisierung.CHARAKTERISIERUNGSGRUPPEN == FUENF


@pytest.mark.parametrize("gruppe", FUENF)
def test_a_jede_gruppe_hat_eine_eingangskombination(gruppe):
    p, g = BEISPIELE[gruppe]
    assert charakterisierung.gruppe_aus(p, g) == gruppe
    # Dieselbe Kombination über die Funktion je Klimawirkung: konstruierte Maßnahme mit
    # Minderung p und vorgegebene Gewissheitsstufe an einem echten Katalogcode.
    code = next(iter(catalog.RISKS_BY_CODE))
    ergebnis = charakterisierung.charakterisierungsgruppe(
        code, _gewissheitsstufe=g, _massnahmen=_massnahme_mit(code, p))
    assert ergebnis == gruppe


def test_b_jede_dringlich_eingestufte_klimawirkung_hat_genau_eine_gruppe():
    ids = _dringlich_eingestufte_kwra_ids()
    assert ids, "Anhang A in docs/KATALOG_KRITIK.md ohne SD/D-Zeilen"
    dringlich = [r["code"] for r in catalog.RISKS if r.get("kwra_id") in ids]
    assert dringlich, "Keine Klimawirkung des Katalogs trägt eine Dringlichkeitseinstufung"
    alle = charakterisierung.charakterisierungen()
    for code in dringlich:
        gruppe = charakterisierung.charakterisierungsgruppe(code)
        assert gruppe is not None, f"{code}: Gruppe ist None"
        assert gruppe in FUENF, f"{code}: unzulässiger Wert {gruppe!r}"
        assert alle[code]["gruppe"] == gruppe, f"{code}: Sammelaufruf weicht ab"


def test_c_gleiche_eingaben_gleiches_ergebnis():
    for code in catalog.RISKS_BY_CODE:
        assert (charakterisierung.charakterisierungsgruppe(code)
                == charakterisierung.charakterisierungsgruppe(code))
    for p, g in BEISPIELE.values():
        assert charakterisierung.gruppe_aus(p, g) == charakterisierung.gruppe_aus(p, g)


def test_docstring_tabelle_eine_zeile_je_gruppe():
    doc = charakterisierung.charakterisierungsgruppe.__doc__
    zeilen = [z.strip() for z in doc.splitlines() if z.strip().startswith("| ")]
    gruppen = [z.strip("|").split("|")[-1].strip() for z in zeilen[1:]]
    assert sorted(gruppen) == sorted(FUENF), gruppen
    assert sorted(z[3] for z in charakterisierung.ENTSCHEIDUNGSTABELLE) == sorted(FUENF)


def test_tabelle_ueberdeckt_alle_eingaben_eindeutig():
    for p in (0.0, 0.05, 0.1, 0.3, 0.5, 0.9, 1.0):
        for g in ("sehr gering", "gering", "mittel", "hoch"):
            treffer = [z for z in charakterisierung.ENTSCHEIDUNGSTABELLE
                       if z[0] <= p < z[1] and g in z[2]]
            assert len(treffer) == 1, (p, g, treffer)


def test_anpassungspotenzial_ohne_massnahme_null_und_multiplikativ():
    code = next(iter(catalog.RISKS_BY_CODE))
    assert charakterisierung.anpassungspotenzial(code, _massnahmen=[]) == 0.0
    zwei = _massnahme_mit(code, 0.5) + _massnahme_mit(code, 0.5)
    assert charakterisierung.anpassungspotenzial(code, _massnahmen=zwei) == pytest.approx(0.75)


def test_unbekannter_code():
    with pytest.raises(KeyError):
        charakterisierung.charakterisierungsgruppe("GIBT_ES_NICHT")
