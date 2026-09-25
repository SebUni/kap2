"""T-1137: Gewissheit der Klimawirkungen und Evidenz der Wirkung je Maßnahme (Zeile 19, A3).

Prüft ``app.services.massnahmen_gewissheit``:
(a) jeder Maßnahmencode aus ``catalog.MEASURES`` kommt genau einmal vor, mit den vier Angaben,
(b) die Klimawirkungen je Maßnahme entsprechen ``linked_risk_codes`` und
    ``qualitative_risk_codes``; jede Gewissheitsstufe wird zur Laufzeit mit
    ``gewissheit.gewissheitsstufe(code)`` verglichen (kein fest eingetragener Wert),
(c) ``wirkung_evidenz`` ist die hinterlegte Klasse oder der Text „keine Evidenzklasse hinterlegt",
(d) die Ausgabe enthält rekursiv keinen Schlüssel ``hinweis`` und keinen verbundenen Wert.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.data import catalog  # noqa: E402
from app.services import gewissheit  # noqa: E402
from app.services import massnahmen_gewissheit as mg  # noqa: E402


def _schluessel(obj) -> set[str]:
    """Alle Schlüssel in beliebig verschachtelten Dicts und Listen."""
    if isinstance(obj, dict):
        gefunden = set(obj)
        for v in obj.values():
            gefunden |= _schluessel(v)
        return gefunden
    if isinstance(obj, (list, tuple)):
        gefunden: set[str] = set()
        for v in obj:
            gefunden |= _schluessel(v)
        return gefunden
    return set()


def test_a_jeder_massnahmencode_genau_einmal():
    ergebnis = mg.massnahmen_gewissheit()
    codes = [e["code"] for e in ergebnis]
    katalog = [m["code"] for m in catalog.MEASURES]
    assert sorted(codes) == sorted(katalog)
    for code in katalog:
        assert codes.count(code) == 1
    for e in ergebnis:
        assert set(e) == {"code", "name", "klimawirkungen", "wirkung_evidenz"}
        assert e["name"] == catalog.MEASURES_BY_CODE[e["code"]]["name"]


def test_b_klimawirkungen_mit_gewissheitsstufe_zur_laufzeit():
    for e in mg.massnahmen_gewissheit():
        m = catalog.MEASURES_BY_CODE[e["code"]]
        erwartet = [(c, False) for c in (m.get("linked_risk_codes") or [])] + [
            (c, True) for c in (m.get("qualitative_risk_codes") or [])
        ]
        assert [(k["code"], k["qualitativ"]) for k in e["klimawirkungen"]] == erwartet
        for k in e["klimawirkungen"]:
            assert set(k) == {"code", "name", "gewissheitsstufe", "qualitativ"}
            assert isinstance(k["qualitativ"], bool)
            assert k["name"] == catalog.RISKS_BY_CODE[k["code"]]["name"]
            assert k["gewissheitsstufe"] == gewissheit.gewissheitsstufe(k["code"])
            assert k["gewissheitsstufe"] in gewissheit.GEWISSHEITSSTUFEN


def test_c_wirkung_evidenz_hinterlegt_oder_vermerk():
    for e in mg.massnahmen_gewissheit():
        m = catalog.MEASURES_BY_CODE[e["code"]]
        klasse = (m.get("evidence_classes") or {}).get("default_reduction")
        herleitung = ((m.get("evidence_derivations") or m.get("evidence_derivation") or {})
                      .get("default_reduction"))
        if klasse:
            assert e["wirkung_evidenz"] == klasse
        elif isinstance(herleitung, dict) and herleitung.get("evidence_class"):
            assert e["wirkung_evidenz"] == herleitung["evidence_class"]
        else:
            assert e["wirkung_evidenz"] == "keine Evidenzklasse hinterlegt"


def test_c_ohne_evidence_classes_greift_vermerk():
    ohne = {"code": "X", "name": "X", "evidence_derivations": {"capex_fixed": {"wert": "1"}}}
    assert mg._wirkung_evidenz(ohne) == "keine Evidenzklasse hinterlegt"
    mit = {"code": "Y", "name": "Y", "evidence_classes": {"default_reduction": "abgeschaetzt"}}
    assert mg._wirkung_evidenz(mit) == "abgeschaetzt"


def test_d_kein_hinweis_und_kein_verbundener_wert():
    ergebnis = mg.massnahmen_gewissheit()
    schluessel = _schluessel(ergebnis)
    assert "hinweis" not in schluessel
    for verboten in ("niedrigste_gewissheit", "hoechste_gewissheit", "minimum", "maximum"):
        assert verboten not in schluessel
