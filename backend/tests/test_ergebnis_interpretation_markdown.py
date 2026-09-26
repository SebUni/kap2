"""Interpretationsbericht als Markdown (T-1141), ohne Datenbank.

Die Daten stammen aus den datenbankfreien Diensten und Datenmodulen; nur die
Nachbarkommunen (PostGIS) und die Nachweise (Datenbank) werden als Dienstergebnis
nachgebaut.
"""

from __future__ import annotations

import re
from datetime import date

from app.data.diversitaet_aspekte import DIVERSITAET_JE_KLIMAWIRKUNG
from app.data.kra_leitfragen import LEITFRAGEN
from app.data.massnahmen_umsetzung import MASSNAHMEN_UMSETZUNG
from app.services import charakterisierung
from app.services.ergebnis_interpretation_markdown import interpretationsbericht_markdown
from app.services.ergebnis_nachweise import NACHWEIS_ARTEN, NICHT_ERFASST
from app.services.handlungsfeld_abhaengigkeiten import abhaengigkeiten_der_kommune
from app.services.massnahmen_gewissheit import massnahmen_gewissheit
from app.services.unsicherheits_zusammenschau import unsicherheits_zusammenschau

UEBERSCHRIFTEN = [
    "## Leitfragen",
    "## Unsicherheit der Daten",
    "## Abhängigkeiten über Handlungsfelder",
    "## Nachbarkommunen",
    "## Handlungsbedarf und Handlungsoptionen",
    "## Gender und Diversität",
    "## Einbeziehung",
]

DATUM = re.compile(r"\d{1,2}\.\d{1,2}\.\d{4}|\d{4}-\d{2}-\d{2}")


def _nachweise(eintraege_je_art: dict[str, list[dict]] | None = None) -> list[dict]:
    """Rückgabe wie ``ergebnis_nachweise.nachweise``."""
    eintraege_je_art = eintraege_je_art or {}
    return [
        {
            "art": code,
            "bezeichnung": bezeichnung,
            "eintraege": eintraege_je_art.get(code, []),
            "status": None if eintraege_je_art.get(code) else NICHT_ERFASST,
        }
        for code, bezeichnung in NACHWEIS_ARTEN.items()
    ]


def _daten(nachweise: list[dict]) -> dict:
    return {
        "leitfragen": LEITFRAGEN,
        "unsicherheit": unsicherheits_zusammenschau(1),
        "abhaengigkeiten": abhaengigkeiten_der_kommune(),
        "nachbarkommunen": [
            {"code": "EXPECTED_ANNUAL_MORTALITY", "name": "Hitzebelastung — Mortalität",
             "index_vorhanden": True, "eigener_index": 42.0,
             "nachbarn": [{"ags": "00000001", "name": "Nachbarort", "index": 37.5}]},
        ],
        "charakterisierungen": charakterisierung.charakterisierungen(),
        "massnahmen_gewissheit": massnahmen_gewissheit(),
        "massnahmen_umsetzung": MASSNAHMEN_UMSETZUNG,
        "diversitaet": DIVERSITAET_JE_KLIMAWIRKUNG,
        "nachweise": nachweise,
    }


def _abschnitt(text: str, ueberschrift: str) -> str:
    rest = text.split(ueberschrift + "\n", 1)[1]
    return rest.split("\n## ", 1)[0]


def test_leitfragen_abschnitt_nennt_stelle_im_produkt_und_keinen_code_pfad():
    text = interpretationsbericht_markdown("Testort", _daten(_nachweise()))
    abschnitt = _abschnitt(text, "## Leitfragen")
    assert not re.search(r"\bapp\.[a-z_]+", abschnitt)
    beantwortet = [f for f in LEITFRAGEN if f["beantwortet_durch"] != "nicht beantwortet"]
    assert beantwortet
    for f in beantwortet:
        assert f"beantwortet in: {f['stelle_im_produkt']}" in abschnitt, f["nr"]


def test_sieben_ueberschriften_in_reihenfolge():
    text = interpretationsbericht_markdown("Beispielkommune", _daten(_nachweise()))
    gefunden = [z for z in text.splitlines() if z.startswith("## ")]
    assert gefunden == UEBERSCHRIFTEN


def test_ohne_nachweise_viermal_nicht_erfasst_und_kein_datum():
    text = interpretationsbericht_markdown("Beispielkommune", _daten(_nachweise()))
    einbeziehung = _abschnitt(text, "## Einbeziehung")
    assert einbeziehung.count("nicht erfasst") == 4
    assert not DATUM.search(einbeziehung)


def test_mit_nachweis_stelle_und_datum():
    nachweise = _nachweise({
        "fachabteilung": [
            {"id": 1, "stelle": "Umweltamt", "datum": date(2026, 9, 1), "vermerk": None},
        ],
    })
    einbeziehung = _abschnitt(
        interpretationsbericht_markdown("Beispielkommune", _daten(nachweise)),
        "## Einbeziehung",
    )
    assert "Umweltamt" in einbeziehung
    assert "01.09.2026" in einbeziehung
    assert einbeziehung.count("nicht erfasst") == 3


def test_keine_euro_betraege():
    nachweise = _nachweise({
        "land": [{"id": 2, "stelle": "Landesamt", "datum": date(2026, 8, 3), "vermerk": "gelesen"}],
    })
    text = interpretationsbericht_markdown("Beispielkommune", _daten(nachweise))
    assert "€" not in text
    assert "EUR" not in text
