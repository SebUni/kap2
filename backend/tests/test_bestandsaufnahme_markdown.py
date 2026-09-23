"""Test der Markdown-Fassung der Bestandsaufnahme (Ticket T-0757, Vorhaben T-0447).

(a) Die vier Überschriften stehen je genau einmal in der vorgegebenen Reihenfolge.
(b) Jede Größe mit Wert steht mit Label, Wert, Einheit und Quelle in der Tabelle ihrer Gruppe.
(c) Unter '## Datenlücken' steht jeder luecke_satz wörtlich genau einmal.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.data import sources  # noqa: E402
from app.data.bestandsaufnahme import LAUFZEITSATZ_VORLAGE, LUECKENSATZ_VORLAGE  # noqa: E402
from app.services.bestandsaufnahme_markdown import bestandsaufnahme_markdown  # noqa: E402

UEBERSCHRIFTEN = [
    "## Vulnerable Personengruppen",
    "## Klimasensible Strukturen",
    "## Vergangene Klimarisiken",
    "## Datenlücken",
]

_L_KIND = "Kinder und Jugendliche unter 18 Jahren"
_L_ALT = "Ältere Menschen ab 65 Jahren"
_L_ENERGIE = "Energieinfrastruktur"
_L_KH = "Krankenhäuser"
_L_PFLEGE = "Pflegebedürftige Menschen"
_L_SCHAD = "Vergangene Schadensereignisse durch Wetterextreme"

ERGEBNIS = {
    "kommune_id": 1,
    "name": "Testdorf",
    "groessen": [
        {"code": "aeltere_ab_65", "gruppe": "vulnerable_personen", "label": _L_ALT,
         "einheit": "%", "wert": 21.456, "quellen": ["Zensus_2022"], "luecke_satz": ""},
        {"code": "kinder_unter_18", "gruppe": "vulnerable_personen", "label": _L_KIND,
         "einheit": "%", "wert": None, "quellen": ["Zensus_2022"],
         "luecke_satz": LAUFZEITSATZ_VORLAGE.format(label=_L_KIND)},
        {"code": "pflegebeduerftige", "gruppe": "vulnerable_personen", "label": _L_PFLEGE,
         "einheit": "", "wert": None, "quellen": [],
         "luecke_satz": LUECKENSATZ_VORLAGE.format(label=_L_PFLEGE)},
        {"code": "energie", "gruppe": "klimasensible_strukturen", "label": _L_ENERGIE,
         "einheit": "Vorkommen", "wert": 1234, "quellen": ["OSM_Data", "BBK_KRITIS"],
         "luecke_satz": ""},
        {"code": "krankenhaeuser", "gruppe": "klimasensible_strukturen", "label": _L_KH,
         "einheit": "Anzahl", "wert": 3, "quellen": ["OSM_Data"], "luecke_satz": ""},
        {"code": "schadensereignisse", "gruppe": "vergangene_ereignisse", "label": _L_SCHAD,
         "einheit": "", "wert": None, "quellen": [],
         "luecke_satz": LUECKENSATZ_VORLAGE.format(label=_L_SCHAD)},
    ],
}


def _abschnitt(md: str, ueberschrift: str) -> str:
    start = md.index(ueberschrift) + len(ueberschrift)
    rest = md[start:]
    ende = rest.find("\n## ")
    return rest if ende < 0 else rest[:ende]


def test_ueberschriften_einmal_in_reihenfolge():
    md = bestandsaufnahme_markdown(ERGEBNIS)
    zeilen = md.splitlines()
    for u in UEBERSCHRIFTEN:
        assert zeilen.count(u) == 1, u
    pos = [md.index(u) for u in UEBERSCHRIFTEN]
    assert pos == sorted(pos)


def test_groessen_mit_wert_in_gruppentabelle():
    md = bestandsaufnahme_markdown(ERGEBNIS)
    erwartet = [
        ("## Vulnerable Personengruppen", _L_ALT, "21,46", "%", ["Zensus_2022"]),
        ("## Klimasensible Strukturen", _L_ENERGIE, "1.234", "Vorkommen", ["OSM_Data", "BBK_KRITIS"]),
        ("## Klimasensible Strukturen", _L_KH, "3", "Anzahl", ["OSM_Data"]),
    ]
    for ueberschrift, label, wert, einheit, keys in erwartet:
        abschnitt = _abschnitt(md, ueberschrift)
        zeile = next(z for z in abschnitt.splitlines() if z.startswith(f"| {label} |"))
        zellen = [c.strip() for c in zeile.strip("|").split(" | ")]
        assert zellen[1] == wert and zellen[2] == einheit
        for q in sources.resolve(keys):
            assert q["ieee"] in zeile


def test_datenluecken_saetze_wortlich_einmal():
    md = bestandsaufnahme_markdown(ERGEBNIS)
    luecken = _abschnitt(md, "## Datenlücken")
    saetze = [g["luecke_satz"] for g in ERGEBNIS["groessen"] if g["luecke_satz"]]
    assert len(saetze) == 3
    assert any("nicht abrufbar" in s for s in saetze)
    for satz in saetze:
        assert luecken.count(satz) == 1, satz
        assert md.count(satz) == 1, satz


if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main([__file__, "-q"]))
