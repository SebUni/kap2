"""Block-Kennung, Klasse und Herleitung der Parameter-Blöcke von #98 (T-1820-cto, Vorgabe P1).

Kapitel 7 von ``docs/methodik/98_uv_schaedigungen.md`` trägt je Block ``id``, ``wert`` und
``kennzeichnung`` (``quelle`` | ``abschaetzung_kap3`` | ``berechnet``). Der Test liest sie
aus dem Bericht selbst und prüft je Block, außer den benannten Ausnahmen:

1. genau eine Stelle im Code: ein Registry-Spec oder ein Katalogfeld, bei Map-Blöcken je
   Schlüssel eine (``<name>_<schlüssel>``, etwa ``baf_mm``);
2. gleicher Wert bei gleicher Rundung (Nachkommastellen des Berichtswerts);
3. Klasse in der Ausgabe der Parameterliste: quelle → belegt, abschaetzung_kap3 → abgeschaetzt,
   berechnet → berechnet. Für die Blöcke unter den 11 (``uv.k_uv``, ``uv.baf``, ``uv.lambda``,
   ``uv.l_rest``, ``uv.c_kal``) gilt die Spalte „Kennzeichnung nach der Regel“ der Tabelle in
   ``docs/methodik/querschnitt_kennzeichnung.md`` (Kopfzeile ``| Bericht | Block-ID | Eingänge |``),
   gelesen zur Laufzeit (T-1898-cto); für alle übrigen Blöcke Kapitel 7;
4. bei abgeschätzten Blöcken (in der Klasse der Parameterliste, also nach Regel K) eine
   Herleitung (Wert, Band, Sensitivität) in der Parameterliste.

Die drei Blöcke der Maßnahme S155 (``uv.s155_dosisminderung``, ``uv.s155_a_erk_mm``,
``uv.s155_a_erk_c44``) tragen ihre Stelle an der Katalog-Maßnahme ``UV_PROTECTION_PUBLIC_SPACE``
(``methodik_bloecke``, Paket 5/7, T-1824-cto) und werden wie alle anderen geprüft.

Benannte Ausnahme:

* ohne eigene Stelle im Code, weil keiner der drei Blöcke im Produkt eigens wirkt (Befund 497
  im Ledger 98; der Test stellt fest, dass es dabei bleibt): ``uv.ssd_delta_region`` (Wert ist
  eine CSV der Kalibrierung, die kein Produktcode liest; je Zelle wirkt die Ebene UV_RADIATION),
  ``uv.i_raten_roh`` (dieselben Werte wie ``uv.i_mm`` und ``uv.i_c44``, die wirken),
  ``uv.r_out_sensitivitaet`` (abgeleitetes Band ohne Spec; r_out wirkt über ``uv.or_out``,
  ``uv.qbar_out`` und ``uv.r_out_enabled``).
"""

from __future__ import annotations

import os
import re
import sys

import yaml

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from regel_k_tabelle import soll_klasse  # noqa: E402
from app.services import parameter_registry  # noqa: E402

REPORT = os.path.join(os.path.dirname(__file__), "..", "..",
                      "docs", "methodik", "98_uv_schaedigungen.md")
CSV = os.path.join(os.path.dirname(__file__), "..", "data", "kalibrierung", "ssd_povw.csv")
CODE = "EXPECTED_ANNUAL_UV_YLL"

# Maßnahme S155 (Paket 5/7 des Abgleich-Vorhabens T-1662-ceo): Blöcke an der Katalog-Maßnahme.
S155 = {"uv.s155_dosisminderung", "uv.s155_a_erk_mm", "uv.s155_a_erk_c44"}
# Ohne eigene Stelle im Code (Abweichungen, siehe Modulkopf).
OHNE_STELLE = {"uv.ssd_delta_region", "uv.i_raten_roh", "uv.r_out_sensitivitaet"}


def _kapitel7() -> str:
    with open(os.path.abspath(REPORT), encoding="utf-8") as fh:
        text = fh.read()
    start = text.index("## 7 Parameter-Blöcke")
    ende = text.index("\n## 8 ", start)
    return text[start:ende]


def _bloecke() -> dict[str, dict]:
    yaml_teil = "\n".join(re.findall(r"```yaml\n(.*?)```", _kapitel7(), re.S))
    bloecke = {}
    for teil in re.split(r"^parameter:\n", yaml_teil, flags=re.M):
        if teil.strip():
            b = yaml.safe_load(teil)
            bloecke[b["id"]] = b
    return bloecke


def _stellen() -> dict[str, list[dict]]:
    """Block-Kennung → Parameter der Parameterliste (Registry), die sie tragen.

    Enthält auch ``uv.voly`` (Kostensatz am Risiko im Katalog).
    """
    nach_block: dict[str, list[dict]] = {}
    for p in parameter_registry.catalog_parameters():
        bid = p.get("methodik_block") or ""
        if bid.startswith("uv."):
            nach_block.setdefault(bid, []).append(p)
    return nach_block


def _geprueft() -> dict[str, dict]:
    return {bid: b for bid, b in _bloecke().items()
            if bid not in OHNE_STELLE}


def _soll() -> dict[str, str]:
    """Block-ID → erwartete Registry-Klasse der geprüften Blöcke: Regel K für die 11, sonst Kapitel 7."""
    return soll_klasse("98", _geprueft())


def _paare(bid: str, wert, stellen: list[dict]) -> list[tuple[str, object, dict]]:
    """Paare (Schlüssel, Sollwert, Parameter): je Schlüssel genau ein Parameter."""
    name = bid.split(".", 1)[1]
    if not isinstance(wert, dict):
        assert len(stellen) == 1, (bid, [p["id"] for p in stellen])
        return [("", wert, stellen[0])]
    paare = []
    for k, v in wert.items():
        treffer = [p for p in stellen if p["id"].endswith(f".{name}_{k.replace('-', '_')}")]
        assert len(treffer) == 1, (bid, k, [p["id"] for p in stellen])
        paare.append((k, v, treffer[0]))
    assert len(stellen) == len(wert), (bid, [p["id"] for p in stellen])
    return paare


def _gleich(ist: float, soll: float) -> bool:
    text = repr(float(soll))
    stellen = len(text.split(".")[1]) if "." in text else 0
    return round(float(ist), stellen) == round(float(soll), stellen)


def test_bericht_fuehrt_22_bloecke_und_ausnahmen_sind_echte_bloecke():
    bloecke = _bloecke()
    roh = re.findall(r"^  id: (uv\.\S+)", _kapitel7(), re.M)
    assert len(roh) == 22 and set(roh) == set(bloecke), sorted(roh)
    assert S155 <= set(bloecke) and OHNE_STELLE <= set(bloecke)
    assert len(_geprueft()) == 19


def test_jeder_block_hat_genau_eine_stelle_im_code():
    nach_block = _stellen()
    ist, soll = set(nach_block), set(_geprueft())
    assert ist == soll, (f"fehlen in der Parameterliste: {sorted(soll - ist)}; "
                         f"nicht in Kapitel 7 geprüft: {sorted(ist - soll)}")
    for bid, b in _geprueft().items():
        _paare(bid, b["wert"], nach_block[bid])


def test_werte_stimmen_mit_den_bloecken_ueberein():
    nach_block = _stellen()
    abweichungen = []
    for bid, b in _geprueft().items():
        for k, soll, p in _paare(bid, b["wert"], nach_block[bid]):
            if not _gleich(p["value"], soll):
                abweichungen.append((bid, k, p["id"], p["value"], soll))
    assert not abweichungen, abweichungen


def test_klasse_in_der_parameterliste_folgt_der_kennzeichnung():
    nach_block = _stellen()
    falsch = []
    for bid, soll in _soll().items():
        for p in nach_block[bid]:
            if p["evidence_class"] != soll:
                falsch.append((bid, p["id"], p["evidence_class"], soll))
    assert not falsch, falsch


def test_abgeschaetzte_bloecke_tragen_herleitung():
    nach_block = _stellen()
    ohne = []
    for bid, klasse in _soll().items():
        if klasse != "abgeschaetzt":
            continue
        for p in nach_block[bid]:
            h = p.get("evidence_derivation") or {}
            fehlt = [f for f in ("wert", "band", "sensitivitaet") if not h.get(f)]
            if fehlt:
                ohne.append((bid, p["id"], fehlt))
    assert not ohne, ohne


def test_s155_bloecke_stehen_an_der_massnahme():
    """Jeder der drei S155-Blöcke hat genau eine Stelle: ein Feld in ``methodik_bloecke``."""
    from app.data import catalog

    m = catalog.MEASURES_BY_CODE["UV_PROTECTION_PUBLIC_SPACE"]
    assert set(m["methodik_bloecke"].values()) == S155
    assert len(m["methodik_bloecke"]) == 3
    nach_block = _stellen()
    for bid in S155:
        assert [p["id"] for p in nach_block[bid]] == [
            f"measures.UV_PROTECTION_PUBLIC_SPACE.{feld}"
            for feld, b in m["methodik_bloecke"].items() if b == bid]


def test_voly_steht_am_risiko_im_katalog():
    by_id = {p["id"]: p for p in parameter_registry.catalog_parameters()}
    v = by_id[f"risks.{CODE}.cost_per_outcome"]
    assert v["methodik_block"] == "uv.voly" and v["value"] == 160800.0
    assert v["evidence_class"] == "abgeschaetzt"


def test_bloecke_ohne_eigene_stelle_bleiben_abweichung():
    """Wer eine eigene Stelle anlegt, nimmt den Block aus OHNE_STELLE und prüft ihn voll."""
    nach_block = _stellen()
    bloecke = _bloecke()
    for bid in OHNE_STELLE:
        assert bid not in nach_block, bid
    assert os.path.exists(os.path.abspath(CSV))
    assert bloecke["uv.ssd_delta_region"]["wert"].endswith("ssd_povw.csv")
    # i_raten_roh trägt dieselben Werte wie i_mm und i_c44 (Doppelung im Bericht).
    roh = bloecke["uv.i_raten_roh"]["wert"]
    for ent, ziel in (("mm", "uv.i_mm"), ("c44", "uv.i_c44")):
        band = {"u20": "u20", "20-64": "a20_64", "65-74": "a65_74",
                "75-84": "a75_84", "85+": "a85p"}
        soll = {band[k]: v for k, v in roh[ent].items()}
        assert soll == bloecke[ziel]["wert"], ent
    # r_out_sensitivitaet: kein Parameter der Registry trägt den Namen.
    assert not [p for p in parameter_registry.catalog_parameters(layer_code=CODE)
                if "r_out_sens" in p["id"]]


if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main([__file__, "-q", "-s"]))
