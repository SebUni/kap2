"""Test der Brücke KWRA-Handlungsfeld → KAnG-Handlungsfeld (Ticket T-0461, Teil 1
des Nachweises nach § 8 Abs. 1 KAnG, Vorhaben T-0445).

Deckt ab:
  (a) Die Schlüsselmenge von KWRA_FELD_ZU_KANG ist genau die Menge der Werte des
      Feldes "kwra_field" aller Einträge aus catalog.RISKS und catalog.PLANNED_RISKS
      zusammen — kein Schlüssel mehr und keiner weniger.
  (b) Jeder Wert ist ein dict mit genau den Schlüsseln cluster/feld/begruendung;
      cluster ist der Code eines Eintrags aus catalog.KANG_CLUSTERS, feld der Code
      eines Feldes genau dieses Clusters, begruendung eine Zeichenkette mit
      mindestens 20 Zeichen.
  (c) handlungsfeld_fuer_risiko(code) liefert für jeden Code aus
      catalog.RISKS_BY_CODE und für jeden Code (kwra_id) aus catalog.PLANNED_RISKS
      genau das Paar (cluster, feld) des zu seinem kwra_field hinterlegten Eintrags
      und wirft für den Code 'GIBT_ES_NICHT' einen KeyError.

Läuft mit pytest oder direkt: ``python tests/test_kang_handlungsfelder.py``.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest  # noqa: E402

from app.data import catalog  # noqa: E402
from app.data.kang_handlungsfelder import (  # noqa: E402
    KWRA_FELD_ZU_KANG,
    handlungsfeld_fuer_risiko,
)


def _alle_kwra_felder() -> set[str]:
    felder = {r["kwra_field"] for r in catalog.RISKS}
    felder |= {p["kwra_field"] for p in catalog.PLANNED_RISKS}
    return felder


# ── (a) Schlüsselmenge ─────────────────────────────────────────────────────────

def test_schluesselmenge_ist_genau_alle_kwra_felder():
    assert set(KWRA_FELD_ZU_KANG.keys()) == _alle_kwra_felder()


# ── (b) Struktur jedes Werts ────────────────────────────────────────────────────

def test_jeder_eintrag_hat_gueltige_struktur():
    kang_felder_je_cluster = {
        cluster["code"]: {feld["code"] for feld in cluster["fields"]}
        for cluster in catalog.KANG_CLUSTERS
    }

    for kwra_feld, eintrag in KWRA_FELD_ZU_KANG.items():
        assert set(eintrag.keys()) == {"cluster", "feld", "begruendung"}, kwra_feld

        cluster_code = eintrag["cluster"]
        assert cluster_code in kang_felder_je_cluster, (
            f"{kwra_feld}: Cluster {cluster_code!r} ist kein Eintrag aus "
            "catalog.KANG_CLUSTERS"
        )

        feld_code = eintrag["feld"]
        assert feld_code in kang_felder_je_cluster[cluster_code], (
            f"{kwra_feld}: Feld {feld_code!r} gehört nicht zum Cluster {cluster_code!r}"
        )

        begruendung = eintrag["begruendung"]
        assert isinstance(begruendung, str)
        assert len(begruendung) >= 20, (
            f"{kwra_feld}: Begründung ist kürzer als 20 Zeichen"
        )


# ── (c) handlungsfeld_fuer_risiko ───────────────────────────────────────────────

def test_handlungsfeld_fuer_aktive_risiken():
    for code, risiko in catalog.RISKS_BY_CODE.items():
        erwartet = KWRA_FELD_ZU_KANG[risiko["kwra_field"]]
        assert handlungsfeld_fuer_risiko(code) == (
            erwartet["cluster"],
            erwartet["feld"],
        )


def test_handlungsfeld_fuer_geplante_risiken():
    for planung in catalog.PLANNED_RISKS:
        code = planung["kwra_id"]
        erwartet = KWRA_FELD_ZU_KANG[planung["kwra_field"]]
        assert handlungsfeld_fuer_risiko(code) == (
            erwartet["cluster"],
            erwartet["feld"],
        )


def test_unbekannter_code_wirft_key_error():
    with pytest.raises(KeyError):
        handlungsfeld_fuer_risiko("GIBT_ES_NICHT")


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))
