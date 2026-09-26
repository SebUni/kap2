"""T-1139-cto: Leitfragen der UBA-Broschüre und ihre Stelle im Produkt (Checkliste Zeile 19, A1).

Prüft ``app.data.kra_leitfragen``:
(a) jeder Eintrag hat die fünf Schlüssel, keiner ist leer,
(b) jede ``seite`` ist eine ganze Zahl von 1 bis 40 (die Broschüre hat 40 Seiten),
(c) jede Fundstelle ungleich „nicht beantwortet“ lässt sich mit ``importlib.import_module``
    laden, und das Attribut existiert.
"""

from __future__ import annotations

import importlib
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.data.kra_leitfragen import LEITFRAGEN, QUELLE  # noqa: E402

SCHLUESSEL = ("nr", "wortlaut", "seite", "beantwortet_durch", "stelle_im_produkt", "begruendung")


def test_quelle_hat_titel_url_und_abrufdatum():
    for feld in ("titel", "url", "abgerufen"):
        assert QUELLE.get(feld), feld


def test_leitfragen_vorhanden():
    assert LEITFRAGEN


def test_jeder_eintrag_hat_alle_schluessel_nicht_leer():
    for eintrag in LEITFRAGEN:
        for schluessel in SCHLUESSEL:
            assert schluessel in eintrag, (eintrag.get("nr"), schluessel)
            wert = eintrag[schluessel]
            assert wert is not None and wert != "", (eintrag.get("nr"), schluessel)


def test_seite_ist_ganze_zahl_von_1_bis_40():
    for eintrag in LEITFRAGEN:
        seite = eintrag["seite"]
        assert isinstance(seite, int) and not isinstance(seite, bool), eintrag["nr"]
        assert 1 <= seite <= 40, eintrag["nr"]


def test_fundstellen_lassen_sich_laden():
    for eintrag in LEITFRAGEN:
        fundstelle = eintrag["beantwortet_durch"]
        if fundstelle == "nicht beantwortet":
            continue
        modul, sep, attribut = fundstelle.partition(":")
        assert sep and modul.startswith("app.") and attribut, (eintrag["nr"], fundstelle)
        geladen = importlib.import_module(modul)
        assert hasattr(geladen, attribut), (eintrag["nr"], fundstelle)


CODE_PFAD = re.compile(r"\bapp\.[a-z_]+")


def test_kein_code_pfad_in_begruendung_und_stelle_im_produkt():
    for eintrag in LEITFRAGEN:
        for feld in ("begruendung", "stelle_im_produkt"):
            assert not CODE_PFAD.search(eintrag[feld]), (eintrag["nr"], feld)


def test_stelle_im_produkt_passt_zum_stand():
    for eintrag in LEITFRAGEN:
        if eintrag["beantwortet_durch"] == "nicht beantwortet":
            assert eintrag["stelle_im_produkt"] == "nicht beantwortet", eintrag["nr"]
        else:
            assert eintrag["stelle_im_produkt"] != "nicht beantwortet", eintrag["nr"]
