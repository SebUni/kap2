"""Tests für die Querverbindungs-Auswertung und den Katalog-Endpunkt (T-0457).

Prüft wörtlich gegen das Abnahmekriterium: Route registriert, Auswertungsform,
genau ein Eintrag je kwra_id aus catalog.RISKS und catalog.PLANNED_RISKS
zusammengenommen, Wertebereiche der Zählfelder und der Netzrolle.
"""
from pathlib import Path

from app.data import catalog
from app.data import kwra_querverbindungen as kq
from app.services.querverbindungen import querverbindungs_auswertung


def test_route_registriert():
    catalog_py = Path(__file__).resolve().parents[1] / "app" / "api" / "routes" / "catalog.py"
    quelltext = catalog_py.read_text(encoding="utf-8")
    assert '@router.get("/catalog/querverbindungen"' in quelltext


def test_auswertung_hat_genau_die_erwarteten_schluessel():
    ergebnis = querverbindungs_auswertung()
    assert set(ergebnis.keys()) == {
        "klimawirkungen", "kennzahlen", "systembereich_matrix",
        "abdeckung", "quelle", "modellgrenze",
    }


def test_klimawirkungen_genau_ein_eintrag_je_kwra_id():
    ergebnis = querverbindungs_auswertung()
    erwartete_ids = {r["kwra_id"] for r in catalog.RISKS} | {p["kwra_id"] for p in catalog.PLANNED_RISKS}
    ids = [e["kwra_id"] for e in ergebnis["klimawirkungen"]]
    assert len(ids) == len(set(ids))
    assert set(ids) == erwartete_ids


def test_klimawirkungen_eintraege_haben_erwartete_form():
    ergebnis = querverbindungs_auswertung()
    for eintrag in ergebnis["klimawirkungen"]:
        assert set(eintrag.keys()) >= {
            "kwra_id", "name", "netzrolle", "ausgehende_benannte", "eingehende_benannte",
        }
        assert eintrag["netzrolle"] in ("stark ausgehend", "stark eingehend", None)
        assert isinstance(eintrag["ausgehende_benannte"], int)
        assert isinstance(eintrag["eingehende_benannte"], int)
        assert eintrag["ausgehende_benannte"] >= 0
        assert eintrag["eingehende_benannte"] >= 0


def test_summe_ausgehende_benannte_hoechstens_zahl_der_beziehungen():
    # Obergrenze = Zahl der benannten Beziehungen im Datenmodul (27 seit T-0936).
    ergebnis = querverbindungs_auswertung()
    summe = sum(e["ausgehende_benannte"] for e in ergebnis["klimawirkungen"])
    assert summe <= len(kq.BENANNTE_BEZIEHUNGEN)
