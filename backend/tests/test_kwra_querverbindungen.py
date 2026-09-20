"""Tests für die KWRA-Querverbindungen (app/data/kwra_querverbindungen).

Prüft die aus Teilbericht 6, Kapitel 3.4 der KWRA 2021 übertragenen Netzrollen,
benannten Einzelbeziehungen, Kennzahlen und die Systembereichs-Matrix wörtlich
gegen das Abnahmekriterium (T-0456).
"""
from app.data import kwra_querverbindungen as k


# ── NETZROLLEN ────────────────────────────────────────────────────────────────

def test_netzrollen_gesamtzahl():
    assert len(k.NETZROLLEN) == 25


def test_netzrollen_rollenverteilung():
    ausgehend = [e for e in k.NETZROLLEN if e["rolle"] == "stark ausgehend"]
    eingehend = [e for e in k.NETZROLLEN if e["rolle"] == "stark eingehend"]
    assert len(ausgehend) == 13
    assert len(eingehend) == 12


def test_netzrollen_kwra_id_eindeutig_und_im_bereich():
    ids = [e["kwra_id"] for e in k.NETZROLLEN]
    assert len(ids) == len(set(ids))
    assert all(1 <= i <= 102 for i in ids)


# ── BENANNTE_BEZIEHUNGEN ─────────────────────────────────────────────────────

def test_benannte_beziehungen_gesamtzahl():
    assert len(k.BENANNTE_BEZIEHUNGEN) == 20


def test_benannte_beziehungen_ebenenverteilung():
    klimawirkung = [b for b in k.BENANNTE_BEZIEHUNGEN if b["ebene"] == "Klimawirkung"]
    gemischt = [b for b in k.BENANNTE_BEZIEHUNGEN if b["ebene"] == "gemischt"]
    handlungsfeld = [b for b in k.BENANNTE_BEZIEHUNGEN if b["ebene"] == "Handlungsfeld"]
    assert len(klimawirkung) == 8
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
