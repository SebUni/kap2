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
        "systembereich_matrix_quelle", "abdeckung", "quelle", "modellgrenze",
        "handlungsfelder", "rueckkopplungen", "rueckkopplungen_quelle", "hochrisiko", "aussagen",
    }


def test_auswertung_liefert_handlungsfelder_rueckkopplungen_hochrisiko_aussagen():
    ergebnis = querverbindungs_auswertung()
    assert {"handlungsfelder", "rueckkopplungen", "hochrisiko", "aussagen"} <= set(ergebnis)
    assert ergebnis["rueckkopplungen"]
    for eintrag in ergebnis["rueckkopplungen"]:
        for knoten in eintrag["knoten"]:
            assert isinstance(knoten["im_katalog"], bool)
    katalog_ids = {r["kwra_id"] for r in catalog.RISKS} | {p["kwra_id"] for p in catalog.PLANNED_RISKS}
    je_id = {k["kwra_id"]: k["im_katalog"] for e in ergebnis["rueckkopplungen"] for k in e["knoten"]}
    assert je_id[95] is True and je_id[62] is True and je_id[65] is False
    assert all(v == (i in katalog_ids) for i, v in je_id.items())
    assert len(ergebnis["handlungsfelder"]["felder"]) == 13
    assert ergebnis["hochrisiko"] == kq.HOCHRISIKO_BEFUNDE
    assert ergebnis["aussagen"] == kq.AUSSAGEN
    for a in ergebnis["aussagen"].values():
        assert isinstance(a["seite"], int) and isinstance(a["seiten"], list)


def test_systembereich_matrix_quelle_nennt_tabelle_28_seite_153():
    # TB 6, Kap. 7: „Tabelle 28: Ausgehende und eingehende Querverbindungen der fünf
    # Systembereiche“ steht auf S. 153 (T-1127).
    quelle = querverbindungs_auswertung()["systembereich_matrix_quelle"]
    assert quelle["tabelle"] == 28
    assert quelle["seite"] == 153
    assert quelle == kq.SYSTEMBEREICH_MATRIX_QUELLE


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
        assert set(e.keys()) == {
            "kwra_id", "name", "handlungsfeld", "netzrollen", "zentral", "seiten", "hinweis",
        }
        assert e["hinweis"] == "nicht im Katalog"
    je_id = {e["kwra_id"]: e for e in eintraege}
    assert 49 in je_id
    assert je_id[49]["zentral"] is True


def test_seiten_je_netzrolle_in_beiden_listen():
    # Seitenbeleg aus TB 6 Kap. 3.4 je Netzrolle (T-1072): mit Netzrolle nicht leer, ohne leer.
    ergebnis = querverbindungs_auswertung()
    eintraege = ergebnis["klimawirkungen"] + ergebnis["netzknoten_ausserhalb_katalog"]
    assert any(e["netzrollen"] for e in eintraege)
    for e in eintraege:
        assert isinstance(e["seiten"], list)
        assert all(isinstance(s, int) and not isinstance(s, bool) for s in e["seiten"])
        if e["netzrollen"]:
            assert e["seiten"], e["kwra_id"]
        else:
            assert e["seiten"] == [], e["kwra_id"]
