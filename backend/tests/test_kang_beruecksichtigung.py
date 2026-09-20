"""Test der Nachweisrechnung je KAnG-Handlungsfeld (Ticket T-0462, Teil 2 des
Nachweises nach § 8 Abs. 1 KAnG, Vorhaben T-0445).

Deckt ab:
  (a) nachweis_fachuebergreifend(...) liefert ein dict mit genau den Schlüsseln
      handlungsfelder / zusammenfassung / abgrenzung.
  (b) handlungsfelder enthält genau einen Eintrag je Paar aus Cluster-Code und
      Feld-Code aus catalog.KANG_CLUSTERS, jeder Eintrag mit genau den Schlüsseln
      cluster/feld/status/risiken/schaden_eur/massnahmen; status ist immer einer
      der drei Werte 'berücksichtigt', 'offen', 'nicht betroffen'.
  (c) zusammenfassung hat genau die Schlüssel betroffen_n / beruecksichtigt_n /
      offen_n / offene_handlungsfelder / integrierende_massnahmen.
  (d) abgrenzung ist eine Zeichenkette mit den Teilzeichenketten
      'Träger öffentlicher Aufgaben', 'bescheinigt keine Rechtskonformität'
      und '§ 8 Abs. 1 KAnG'.
  (e) Leere Eingabe: alle Einträge 'nicht betroffen', betroffen_n 0,
      integrierende_massnahmen leer.
  (f) Ein Risiko mit Schaden, keine Maßnahme: genau ein Eintrag 'offen', alle
      übrigen 'nicht betroffen', betroffen_n 1, offen_n 1, genau ein Eintrag in
      offene_handlungsfelder.

Läuft mit pytest oder direkt: ``python tests/test_kang_beruecksichtigung.py``.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest  # noqa: E402

from app.data import catalog  # noqa: E402
from app.services.kang_beruecksichtigung import (  # noqa: E402
    nachweis_fachuebergreifend,
)

STATUS_WERTE = {"berücksichtigt", "offen", "nicht betroffen"}


def _erwartete_paare() -> list[tuple[str, str]]:
    return [
        (cluster["code"], feld["code"])
        for cluster in catalog.KANG_CLUSTERS
        for feld in cluster["fields"]
    ]


# ── (a) Rückgabestruktur ────────────────────────────────────────────────────────

def test_rueckgabe_hat_genau_die_drei_schluessel():
    nachweis = nachweis_fachuebergreifend({}, [])
    assert isinstance(nachweis, dict)
    assert set(nachweis.keys()) == {"handlungsfelder", "zusammenfassung", "abgrenzung"}


# ── (b) Handlungsfelder ─────────────────────────────────────────────────────────

def test_genau_ein_eintrag_je_cluster_feld_paar():
    nachweis = nachweis_fachuebergreifend(
        {"EXPECTED_ANNUAL_MORTALITY": 1000.0}, ["HEAT_ACTION_PLANS"]
    )
    paare = [(e["cluster"], e["feld"]) for e in nachweis["handlungsfelder"]]
    erwartet = _erwartete_paare()
    assert sorted(paare) == sorted(erwartet)
    assert len(paare) == len(set(paare)) == len(erwartet)


def test_jeder_eintrag_hat_genau_die_sechs_schluessel_und_gueltigen_status():
    nachweis = nachweis_fachuebergreifend(
        {"EXPECTED_ANNUAL_MORTALITY": 1000.0}, ["HEAT_ACTION_PLANS"]
    )
    for eintrag in nachweis["handlungsfelder"]:
        assert set(eintrag.keys()) == {
            "cluster", "feld", "status", "risiken", "schaden_eur", "massnahmen",
        }, eintrag
        assert eintrag["status"] in STATUS_WERTE, eintrag


# ── (c) Zusammenfassung ─────────────────────────────────────────────────────────

def test_zusammenfassung_hat_genau_die_fuenf_schluessel():
    nachweis = nachweis_fachuebergreifend({}, [])
    assert set(nachweis["zusammenfassung"].keys()) == {
        "betroffen_n",
        "beruecksichtigt_n",
        "offen_n",
        "offene_handlungsfelder",
        "integrierende_massnahmen",
    }


# ── (d) Abgrenzung ──────────────────────────────────────────────────────────────

def test_abgrenzung_nennt_adressat_grenze_und_norm():
    abgrenzung = nachweis_fachuebergreifend({}, [])["abgrenzung"]
    assert isinstance(abgrenzung, str)
    assert "Träger öffentlicher Aufgaben" in abgrenzung
    assert "bescheinigt keine Rechtskonformität" in abgrenzung
    assert "§ 8 Abs. 1 KAnG" in abgrenzung


# ── (e) Leere Eingabe ───────────────────────────────────────────────────────────

def test_leere_eingabe_ist_ueberall_nicht_betroffen():
    nachweis = nachweis_fachuebergreifend({}, [])
    assert all(
        e["status"] == "nicht betroffen" for e in nachweis["handlungsfelder"]
    )
    assert nachweis["zusammenfassung"]["betroffen_n"] == 0
    assert nachweis["zusammenfassung"]["integrierende_massnahmen"] == []


# ── (f) Ein betroffenes Feld ohne Maßnahme ──────────────────────────────────────

def test_ein_risiko_ohne_massnahme_ergibt_genau_ein_offenes_feld():
    nachweis = nachweis_fachuebergreifend({"EXPECTED_ANNUAL_MORTALITY": 1000.0}, [])

    offene = [e for e in nachweis["handlungsfelder"] if e["status"] == "offen"]
    uebrige = [e for e in nachweis["handlungsfelder"] if e["status"] != "offen"]
    assert len(offene) == 1
    assert all(e["status"] == "nicht betroffen" for e in uebrige)

    zusammenfassung = nachweis["zusammenfassung"]
    assert zusammenfassung["betroffen_n"] == 1
    assert zusammenfassung["offen_n"] == 1
    assert len(zusammenfassung["offene_handlungsfelder"]) == 1


# ── Ergänzend: Zuordnung, Summe und Berücksichtigung ────────────────────────────

def test_massnahme_im_selben_feld_macht_das_feld_beruecksichtigt():
    nachweis = nachweis_fachuebergreifend(
        {"EXPECTED_ANNUAL_MORTALITY": 1000.0}, ["HEAT_ACTION_PLANS"]
    )
    treffer = [
        e for e in nachweis["handlungsfelder"]
        if e["status"] == "berücksichtigt"
    ]
    assert len(treffer) == 1
    assert treffer[0]["risiken"] == ["EXPECTED_ANNUAL_MORTALITY"]
    assert treffer[0]["schaden_eur"] == 1000.0
    assert treffer[0]["massnahmen"] == ["HEAT_ACTION_PLANS"]
    assert nachweis["zusammenfassung"]["beruecksichtigt_n"] == 1
    assert nachweis["zusammenfassung"]["offen_n"] == 0
    assert nachweis["zusammenfassung"]["offene_handlungsfelder"] == []


def test_schaden_null_macht_ein_feld_nicht_betroffen():
    nachweis = nachweis_fachuebergreifend({"EXPECTED_ANNUAL_MORTALITY": 0.0}, [])
    assert all(
        e["status"] == "nicht betroffen" for e in nachweis["handlungsfelder"]
    )
    assert nachweis["zusammenfassung"]["betroffen_n"] == 0


def test_unbekannte_codes_werfen_key_error():
    with pytest.raises(KeyError):
        nachweis_fachuebergreifend({"GIBT_ES_NICHT": 1.0}, [])
    with pytest.raises(KeyError):
        nachweis_fachuebergreifend({}, ["GIBT_ES_NICHT"])


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))
