"""Bewertungsdienst Anpassungskapazität (T-0762, Vorhaben T-0448)."""

import pytest

from app.data.anpassungskapazitaet import (
    HERLEITUNG_REIFEGRADE,
    KOMPONENTEN,
    MINDERUNGSSAETZE,
    OPTIONAL_SATZ,
    QUELLE_KOMPONENTEN,
    REGEL_GESAMTSTUFE,
)
from app.services.anpassungskapazitaet import bewerte_anpassungskapazitaet


def test_alle_bewertet_engpass():
    r = bewerte_anpassungskapazitaet(
        {"organisation": 2, "technik": 3, "finanzen": 1, "oekosystem": 2}
    )
    assert r["gesamtstufe"] == 1
    assert r["engpaesse"] == ["finanzen"]
    assert r["minderung"] == MINDERUNGSSAETZE[1]
    assert r["optional_hinweis"] == OPTIONAL_SATZ
    assert r["regel"] == REGEL_GESAMTSTUFE
    assert r["quelle"] == QUELLE_KOMPONENTEN
    assert r["herleitung"] == HERLEITUNG_REIFEGRADE
    assert [k["code"] for k in r["komponenten"]] == [k["code"] for k in KOMPONENTEN]
    for k in r["komponenten"]:
        assert set(k) == {"code", "label", "stufe", "stufe_label"}


def test_teilbewertung():
    r = bewerte_anpassungskapazitaet({"organisation": 2})
    assert r["gesamtstufe"] is None
    assert r["engpaesse"] == []
    assert r["minderung"] == MINDERUNGSSAETZE[None]
    for k in r["komponenten"]:
        if k["code"] != "organisation":
            assert k["stufe"] is None
            assert k["stufe_label"] == "nicht bewertet"


def test_unbekannter_code():
    with pytest.raises(ValueError):
        bewerte_anpassungskapazitaet({"foo": 1})


def test_unzulaessige_stufe():
    with pytest.raises(ValueError):
        bewerte_anpassungskapazitaet({"technik": 4})
