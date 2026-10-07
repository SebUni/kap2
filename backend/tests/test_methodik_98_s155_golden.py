"""Golden-Test des Prüfblocks ``beispiel_98_s155_wirkung`` (Bericht #98 §5, Z. 1381–1421)
an den Produktwegen — nicht am Beispiel-Block selbst (der läuft über den Berichts-Test in
``test_methodik_98_golden.py``).

Abgleich-Paket 5/7 (T-1824-cto, Vorhaben T-1662-ceo): bindet für die Beispielkommune Berlin

- die Wirkung W(h) bei h = 0,018 auf **252.500 € ± 50** (Z. 1396–1398),
- das Band h 0,005 / 0,045 auf **70.100 / 631.200 € ± 50** (Z. 1403),
- die Rampe J = 10 / 20 / 30 auf **34.700 / 69.400 / 104.000 € ± 50** (Z. 1409).

Die Eingaben kommen aus den Produktwegen: der bewertete Schaden je Entität aus
``health.uv_yll`` (Schlüssel ``eur_mm``/``eur_c44``, dieselbe Zelle wie
``test_methodik_98_golden_betraege.py``), ``h`` und die Einlaufzeiten ``a_erk`` aus der
Katalog-Maßnahme ``UV_PROTECTION_PUBLIC_SPACE``, ``BAF_e`` aus der Parameterliste; die
Wirkung rechnet ``health.s155_wirkung`` bzw. der Zellweg ``measure_service._s155_cell_effect``.
Eine eigene Formel steht hier nicht.

Die Bandgrenzen 0,005 und 0,045 sind die Werte des Prüfblocks (Z. 1401); als Zahlen führt sie
der Katalog im Feld ``default_reduction_band``, der Test vergleicht beide.
"""

from __future__ import annotations

import os
import sys
from importlib import import_module

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.data import catalog  # noqa: E402
from app.services import measure_service, parameter_registry  # noqa: E402
from app.services.engine.impact import health as H  # noqa: E402

_betraege = import_module("test_methodik_98_golden_betraege")

MASSNAHME = "UV_PROTECTION_PUBLIC_SPACE"
TOL = 50.0                      # Toleranz des Prüfblocks (Euro)
H_BASIS, H_UNTEN, H_OBEN = 0.018, 0.005, 0.045


def _massnahme() -> dict:
    return catalog.MEASURES_BY_CODE[MASSNAHME]


def _baf() -> tuple[float, float]:
    werte = {p["id"].rsplit(".", 1)[1]: p["value"]
             for p in parameter_registry.catalog_parameters(layer_code=_betraege.CODE)
             if p["id"].rsplit(".", 1)[1] in ("baf_mm", "baf_c44")}
    return werte["baf_mm"], werte["baf_c44"]


def _w(h: float, jahre: float | None = None) -> float:
    r = _betraege.betrag_berlin()["res"]
    m = _massnahme()
    baf_mm, baf_c44 = _baf()
    return H.s155_wirkung(r["eur_mm"], r["eur_c44"], h, baf_mm, baf_c44, jahre,
                          m["a_erk_mm"], m["a_erk_c44"])


def test_massnahme_traegt_die_werte_des_berichts():
    m = _massnahme()
    assert m["default_reduction"] == H_BASIS
    assert (m["a_erk_mm"], m["a_erk_c44"]) == (66.0, 75.0)
    assert tuple(m["default_reduction_band"]) == (H_UNTEN, H_OBEN)
    assert m["effect_model"] == "s155" and m["linked_risk_codes"] == [_betraege.CODE]
    assert _baf() == (0.60, 1.675)


def test_bewerteter_schaden_je_entitaet_ist_der_basiswert_berlin():
    """Ebene 10: 5,14 / 6,53 / 11,68 Mio. € — der Basiswert bleibt unverändert."""
    r = _betraege.betrag_berlin()
    assert abs(r["res"]["eur_mm"] - r["mm_eur"]) < 1e-6
    assert abs(r["res"]["eur_c44"] - r["c44_eur"]) < 1e-6
    assert abs((r["res"]["eur_mm"] + r["res"]["eur_c44"]) / 1e6 - 11.68) < 0.005


def test_wirkung_berlin_252500():
    """Z. 1396–1398: W(0,018) = 252.500 € ± 50, 2,2 % des Schadens; je Entität 55.600/196.900 €."""
    r = _betraege.betrag_berlin()["res"]
    baf_mm, baf_c44 = _baf()
    w = _w(H_BASIS)
    assert abs(w - 252_500) < TOL, f"{w:.1f} €"
    assert abs(w / (r["eur_mm"] + r["eur_c44"]) - 0.022) < 0.0005
    mm, c44 = H.s155_wirkung_je_entitaet(r["eur_mm"], r["eur_c44"], H_BASIS, baf_mm, baf_c44)
    assert abs(mm - 55_600) < TOL and abs(c44 - 196_900) < TOL


def test_band_berlin():
    """Z. 1403: h = 0,005 → 70.100 €, h = 0,045 → 631.200 € (je ± 50)."""
    unten, oben = _w(H_UNTEN), _w(H_OBEN)
    assert abs(unten - 70_100) < TOL, f"{unten:.1f} €"
    assert abs(oben - 631_200) < TOL, f"{oben:.1f} €"


def test_rampe_berlin():
    """Z. 1409: J = 10/20/30 → 34.700 / 69.400 / 104.000 € (je ± 50); a_erk MM 66, C44 75."""
    for jahre, soll in ((10, 34_700), (20, 69_400), (30, 104_000)):
        ist = _w(H_BASIS, jahre)
        assert abs(ist - soll) < TOL, f"J={jahre}: {ist:.1f} €"
    # nach a_erk,C44 Jahren (75) ist die volle Wirkung erreicht, davor nicht (Z. 1410)
    assert abs(_w(H_BASIS, 75) - _w(H_BASIS)) < 1e-6
    assert _w(H_BASIS, 65) < _w(H_BASIS)
    # ohne Zeitangabe gilt die volle Wirkung
    assert _w(H_BASIS, None) == _w(H_BASIS)


def test_zellweg_liefert_dieselbe_wirkung():
    """Der Zellweg der Maßnahme (``_s155_cell_effect``, Deckung 1) liefert W und einen Faktor < 1."""
    res = _betraege.betrag_berlin()["res"]
    faktor, eur, fehlt = measure_service._s155_cell_effect(_massnahme(), 1.0, res)
    assert not fehlt and eur is not None
    assert abs(sum(eur) - 252_500) < TOL
    assert 0.0 < 1.0 - faktor < 0.03          # Minderung des YLL-Outcomes, kleiner als BAF · h
    # halbe Deckung → halbe Wirkung; ohne Deckung keine Wirkung
    _, halb, _ = measure_service._s155_cell_effect(_massnahme(), 0.5, res)
    assert abs(sum(halb) - 126_250) < TOL
    assert measure_service._s155_cell_effect(_massnahme(), 0.0, res) == (1.0, None, False)
    # Alt-Zelle ohne Entitätswerte: Vermerk statt 0 €
    alt = {"outcome": 10.0}
    assert measure_service._s155_cell_effect(_massnahme(), 1.0, alt) == (1.0, None, True)


def test_summary_weist_abschaetzung_band_und_rampe_aus():
    res = _betraege.betrag_berlin()["res"]
    _, eur, _ = measure_service._s155_cell_effect(_massnahme(), 1.0, res)
    s = measure_service._s155_summary_fields(_massnahme(), eur[0], eur[1], False)
    assert s["s155_estimate_note"] == "Abschätzung von KAP3"
    assert abs(s["s155_avoided_eur"] - 252_500) < TOL
    assert abs(s["s155_band_eur"][0] - 70_100) < TOL and abs(s["s155_band_eur"][1] - 631_200) < TOL
    assert [round(z["eur"], -2) for z in s["s155_rampe"]] == [34_700, 69_400, 104_000]
    assert [z["jahre"] for z in s["s155_rampe"]] == [10, 20, 30]
    voll = measure_service._s155_summary_fields(_massnahme(), 0.0, 0.0, True)
    assert voll["benefit_missing_input"] == "uv_entity_split"
    assert measure_service._s155_summary_fields({"effect_model": "s158"}, 1.0, 1.0, False) == {}


if __name__ == "__main__":
    import pytest

    sys.exit(pytest.main([__file__, "-q"]))
