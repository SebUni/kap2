"""Tests für die KWRA-Querverbindungen (app/data/kwra_querverbindungen).

Prüft die aus Teilbericht 6, Kapitel 3.4 der KWRA 2021 übertragenen Netzrollen,
benannten Einzelbeziehungen, Kennzahlen und die Systembereichs-Matrix wörtlich
gegen das Abnahmekriterium (T-0456).
"""
from app.data import kwra_querverbindungen as k


# ── NETZROLLEN ────────────────────────────────────────────────────────────────

def test_netzrollen_gesamtzahl():
    # 25 aus der Arbeitsmappe + #7 und #8 aus der Hochrisiko-Auswertung (S. 87, T-0938)
    assert len(k.NETZROLLEN) == 27


def test_netzrollen_rollenverteilung():
    ausgehend = [e for e in k.NETZROLLEN if e["rolle"] == "stark ausgehend"]
    eingehend = [e for e in k.NETZROLLEN if e["rolle"] == "stark eingehend"]
    assert len(ausgehend) == 13
    assert len(eingehend) == 14


def test_netzrollen_kwra_id_eindeutig_und_im_bereich():
    ids = [e["kwra_id"] for e in k.NETZROLLEN]
    assert len(ids) == len(set(ids))
    assert all(1 <= i <= 102 for i in ids)


def test_netzrollen_mehrwertig_und_zentral_mit_seitenbeleg():
    """T-0937 (C3/A8/A6): eine Klimawirkung kann Sender und Empfänger zugleich sein
    (TB 6 Kap. 3.4, Fn. 21, S. 84); #4 ist beides (S. 87, 88), #49 Hochwasser ist die
    zentrale Klimawirkung der Gesamtbetrachtung (S. 84, 88)."""
    je_id = {e["kwra_id"]: e for e in k.NETZROLLEN}
    assert je_id[4]["rollen"] == ["stark ausgehend", "stark eingehend"]
    assert je_id[49]["zentral"] is True
    for e in k.NETZROLLEN:
        assert e["rollen"], e
        assert set(e["rollen"]) <= {"stark ausgehend", "stark eingehend"}, e
        assert e["rolle"] == e["rollen"][0], e
        assert isinstance(e["zentral"], bool), e
        if len(e["rollen"]) == 2 or e["zentral"] is True:
            assert "S. " in e["beleg_rolle"], e


def test_netzrollen_auswertungen_gesamt_und_hochrisiko_getrennt():
    """T-0938 (A12): TB 6 Kap. 3.4 betrachtet die Querverbindungen der hoch bewerteten
    Klimawirkungen gesondert (S. 86–87); jede Netzrolle sagt, aus welcher Auswertung sie
    stammt, und die Befunde der Hochrisiko-Auswertung stehen in HOCHRISIKO_BEFUNDE."""
    for e in k.NETZROLLEN:
        assert e["auswertungen"], e
        assert set(e["auswertungen"]) <= {"gesamt", "hochrisiko"}, e
        if "hochrisiko" in e["auswertungen"]:
            assert "S. 87" in e["beleg_auswertung"], e
    je_id = {e["kwra_id"]: e for e in k.NETZROLLEN}
    assert "hochrisiko" in je_id[5]["auswertungen"]
    je_name = {e["name"]: e for e in k.NETZROLLEN}
    for name in (
        "Schäden an Feuchtgebieten und wassergebundenen Habitaten",
        "Schäden an Wäldern",
    ):
        assert name in je_name, name
        assert "hochrisiko" in je_name[name]["auswertungen"], name
    biodiv = [
        b for b in k.HOCHRISIKO_BEFUNDE
        if b["name"] == "Biologische Vielfalt" and ({86, 87} & set(b["seiten"]))
    ]
    assert len(biodiv) == 1


# ── BENANNTE_BEZIEHUNGEN ─────────────────────────────────────────────────────

def test_benannte_beziehungen_gesamtzahl():
    assert len(k.BENANNTE_BEZIEHUNGEN) == 27


def _richtung_zwischen(id_a: int, id_b: int) -> list[str]:
    """Richtungen aller Einträge zwischen zwei Klimawirkungen (Reihenfolge egal)."""
    return [
        b["richtung"] for b in k.BENANNTE_BEZIEHUNGEN
        if {b["quelle_kwra_id"], b["ziel_kwra_id"]} == {id_a, id_b}
    ]


def test_benannte_beziehungen_richtung_und_seitenbeleg():
    """T-0936: jede Beziehung trägt eine Richtung und eine Seitenangabe; die im Fließtext
    von TB 6 Kap. 3.4 genannten Beziehungen (S. 82, 85, 86) sind mit Richtung erfasst."""
    for b in k.BENANNTE_BEZIEHUNGEN:
        assert b["richtung"] in {"gerichtet", "gegenseitig"}, b
        assert "S. " in b["beleg"], b

    # Gewässertemperatur (#53) ↔ Mangelndes Kühlwasser (#68), S. 82, 85
    assert _richtung_zwischen(53, 68) == ["gegenseitig"]
    # Bedarf an Kühlenergie (#65) ↔ Stadtklima/Wärmeinseln (#62), S. 85
    assert _richtung_zwischen(65, 62) == ["gegenseitig"]
    # Verschiebung von Arealen (#4) ↔ Vegetation in Siedlungen (#61), S. 86
    assert _richtung_zwischen(4, 61) == ["gegenseitig"]
    # Wassermangel im Boden (#13) → Schäden in Wäldern (#8), S. 82
    wald = [
        b for b in k.BENANNTE_BEZIEHUNGEN
        if b["quelle_kwra_id"] == 13 and b["ziel_kwra_id"] == 8
    ]
    assert len(wald) == 1
    assert wald[0]["richtung"] == "gerichtet"
    assert "Kühlwasser" in next(
        b["ziel"] for b in k.BENANNTE_BEZIEHUNGEN if b["ziel_kwra_id"] == 68
    )


def test_benannte_beziehungen_ebenenverteilung():
    klimawirkung = [b for b in k.BENANNTE_BEZIEHUNGEN if b["ebene"] == "Klimawirkung"]
    gemischt = [b for b in k.BENANNTE_BEZIEHUNGEN if b["ebene"] == "gemischt"]
    handlungsfeld = [b for b in k.BENANNTE_BEZIEHUNGEN if b["ebene"] == "Handlungsfeld"]
    assert len(klimawirkung) == 15
    assert len(gemischt) == 7
    assert len(handlungsfeld) == 5


def test_benannte_beziehungen_ids_im_bereich_oder_none():
    for b in k.BENANNTE_BEZIEHUNGEN:
        q = b.get("quelle_kwra_id")
        z = b.get("ziel_kwra_id")
        assert q is None or 1 <= q <= 102
        assert z is None or 1 <= z <= 102


# ── KENNZAHLEN ────────────────────────────────────────────────────────────────

def test_kennzahlen_querverbindungen_gesamt():
    assert k.KENNZAHLEN["querverbindungen_gesamt"] == 257


# ── SYSTEMBEREICH_MATRIX ─────────────────────────────────────────────────────

def test_systembereich_matrix_form():
    assert len(k.SYSTEMBEREICH_MATRIX) == 5
    for quellbereich, ziele in k.SYSTEMBEREICH_MATRIX.items():
        # 5 Zielbereiche + der Schlüssel "summe_ausgehend"
        assert len(ziele) == 6
        assert "summe_ausgehend" in ziele


# ── QUELLE ────────────────────────────────────────────────────────────────────

def test_quelle_enthaelt_arbeitsmappe():
    assert "KWRA-2021_Klimawirkungen.xlsx" in k.QUELLE
