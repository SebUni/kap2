"""Tests für die KWRA-Rückkopplungen (app/data/kwra_rueckkopplungen).

Prüft die aus Teilbericht 6, Kapitel 3.4 (S. 82, 85–86, Abbildung 9) übertragenen
gegenseitigen Wechselwirkungen und den einzigen Rückkopplungskreislauf
Hitzebelastung – Bedarf an Kühlenergie – Stadtklima/Wärmeinseln (T-0935-cto, A11).
"""
from app.data import catalog
from app.data import kwra_rueckkopplungen as r


def _kreislaeufe():
    return [e for e in r.RUECKKOPPLUNGEN if e["art"] == "kreislauf"]


def test_genau_ein_kreislauf():
    assert len(_kreislaeufe()) == 1


def test_kreislauf_enthaelt_95_62_und_kuehlenergie():
    (kreislauf,) = _kreislaeufe()
    ids = {k["kwra_id"] for k in kreislauf["knoten"]}
    namen = {k["name"] for k in kreislauf["knoten"]}
    assert 95 in ids
    assert 62 in ids
    assert "Bedarf an Kühlenergie" in namen
    assert r.KREISLAUF is kreislauf


def test_kreislauf_knoten_aus_arbeitsmappe():
    (kreislauf,) = _kreislaeufe()
    assert {(k["kwra_id"], k["name"]) for k in kreislauf["knoten"]} == {
        (95, "Hitzebelastung"),
        (65, "Bedarf an Kühlenergie"),
        (62, "Stadtklima/Wärmeinseln"),
    }


def test_kreislauf_kanten_nach_abbildung_9():
    (kreislauf,) = _kreislaeufe()
    kanten = {(k["von_kwra_id"], k["nach_kwra_id"]) for k in kreislauf["kanten"]}
    assert kanten == {(62, 95), (95, 65), (65, 62), (62, 65)}
    assert kreislauf["abbildung"] == "Abbildung 9"


def test_kreislauf_ist_geschlossen():
    """Von jedem Knoten aus führt ein gerichteter Weg zurück zu ihm selbst."""
    (kreislauf,) = _kreislaeufe()
    nachfolger: dict[int, set[int]] = {}
    for k in kreislauf["kanten"]:
        nachfolger.setdefault(k["von_kwra_id"], set()).add(k["nach_kwra_id"])
    for start in (k["kwra_id"] for k in kreislauf["knoten"]):
        gesehen, offen = set(), list(nachfolger.get(start, ()))
        while offen:
            n = offen.pop()
            if n not in gesehen:
                gesehen.add(n)
                offen.extend(nachfolger.get(n, ()))
        assert start in gesehen


def test_jeder_eintrag_hat_seite_85_oder_86():
    assert r.RUECKKOPPLUNGEN
    for e in r.RUECKKOPPLUNGEN:
        assert 85 in e["seiten"] or 86 in e["seiten"], e["id"]


def test_arten_und_kennungen():
    assert all(e["art"] in {"wechselwirkung", "kreislauf"} for e in r.RUECKKOPPLUNGEN)
    ids = [e["id"] for e in r.RUECKKOPPLUNGEN]
    assert len(ids) == len(set(ids))
    assert len([e for e in r.RUECKKOPPLUNGEN if e["art"] == "wechselwirkung"]) == 2


def test_wechselwirkungen_sind_gegenseitig():
    for e in r.RUECKKOPPLUNGEN:
        if e["art"] != "wechselwirkung":
            continue
        a, b = (k["kwra_id"] for k in e["knoten"])
        kanten = {(k["von_kwra_id"], k["nach_kwra_id"]) for k in e["kanten"]}
        assert kanten == {(a, b), (b, a)}, e["id"]


def test_kanten_verweisen_auf_knoten_und_ids_im_bereich():
    for e in r.RUECKKOPPLUNGEN:
        ids = {k["kwra_id"] for k in e["knoten"]}
        assert all(1 <= i <= 102 for i in ids)
        for k in e["kanten"]:
            assert k["von_kwra_id"] in ids and k["nach_kwra_id"] in ids


def test_katalogstand_der_kreislaufknoten():
    katalog = {x["kwra_id"] for x in catalog.RISKS if x.get("kwra_id") is not None}
    katalog |= set(catalog.PLANNED_BY_KWRA_ID)
    assert 95 in katalog
    assert 62 in katalog
    assert 65 not in katalog


def test_quelle_nennt_kapitel_und_abbildung():
    assert "Analyse der Querverbindungen" in r.QUELLE
    assert "Abbildung 9" in r.QUELLE
    assert "Vernetzung der Klimawirkungen" not in r.QUELLE
