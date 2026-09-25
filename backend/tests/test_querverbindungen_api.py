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
        "klimawirkungen", "netzknoten_ausserhalb_katalog", "kennzahlen", "systembereich_matrix",
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


def test_summe_ausgehende_benannte_hoechstens_zahl_der_gezaehlten_richtungen():
    # Obergrenze = gezählte Richtungen: jede Beziehung einmal, eine „gegenseitige“
    # zweimal, weil sie bei beiden Klimawirkungen aus- und eingehend zählt (T-0937).
    ergebnis = querverbindungs_auswertung()
    obergrenze = sum(
        2 if b["richtung"] == "gegenseitig" else 1 for b in kq.BENANNTE_BEZIEHUNGEN
    )
    summe_aus = sum(e["ausgehende_benannte"] for e in ergebnis["klimawirkungen"])
    summe_ein = sum(e["eingehende_benannte"] for e in ergebnis["klimawirkungen"])
    assert summe_aus <= obergrenze
    assert summe_ein <= obergrenze


def test_gegenseitige_beziehung_zaehlt_bei_beiden_aus_und_eingehend():
    # Bedarf an Kühlenergie (#65) ↔ Stadtklima/Wärmeinseln (#62), TB 6 S. 85: #62 ist
    # im Katalog und zählt die Beziehung deshalb als ausgehend und als eingehend.
    je_id = {e["kwra_id"]: e for e in querverbindungs_auswertung()["klimawirkungen"]}
    assert je_id[62]["ausgehende_benannte"] == 2  # → #95 und ↔ #65
    assert je_id[62]["eingehende_benannte"] == 1  # ↔ #65


def test_netzrollen_mehrwertig_und_zentral_im_dienst():
    for e in querverbindungs_auswertung()["klimawirkungen"]:
        assert set(e["netzrollen"]) <= {"stark ausgehend", "stark eingehend"}
        assert (e["netzrolle"] is None) == (e["netzrollen"] == [])
        assert isinstance(e["zentral"], bool)


def test_netzknoten_ausserhalb_katalog():
    katalog_ids = {r["kwra_id"] for r in catalog.RISKS} | {p["kwra_id"] for p in catalog.PLANNED_RISKS}
    erwartet = {
        e["kwra_id"] for e in kq.NETZROLLEN if "gesamt" in e["auswertungen"]
    } - katalog_ids
    eintraege = querverbindungs_auswertung()["netzknoten_ausserhalb_katalog"]
    assert {e["kwra_id"] for e in eintraege} == erwartet
    for e in eintraege:
        assert set(e.keys()) == {"kwra_id", "name", "handlungsfeld", "netzrollen", "zentral", "hinweis"}
        assert e["hinweis"] == "nicht im Katalog"
    je_id = {e["kwra_id"]: e for e in eintraege}
    assert 49 in je_id
    assert je_id[49]["zentral"] is True
