"""Regel K, Schritt 3: Registry führt Eingänge, ``enthaelt_abschaetzung`` und Anzeigetext (T-1900-cto).

Der Test liest zur Laufzeit aus ``docs/methodik/querschnitt_kennzeichnung.md`` die Tabelle der
11 berechneten Blöcke (Kopfzeile ``| Bericht | Block-ID | Eingänge |``) und prüft je Zeile für
jeden Registry-Parameter, dessen ``methodik_block`` die Block-ID ist:

1. ``evidence_class`` gleich der übersetzten Spalte „Kennzeichnung nach der Regel“;
2. ``parameter_registry.anzeigetext(p)`` gleich der Spalte „Anzeigetext“ ohne „“;
3. bei ``berechnet``: ``abgeleitet_aus`` gleich den Einträgen der Spalte „Eingänge“, die Blöcke
   des Berichts sind (Quellenschlüssel ohne eigenen Block zählen nicht, Festlegung b), und
   ``eingaenge`` als {block, anzeigetext} in derselben Reihenfolge.

Einzige zulässige Zeile ohne Registry-Parameter ist ``uv.ssd_delta_region`` (ohne eigene Stelle,
Übernahmeliste der Querschnittsdatei, Zeile „Kennzeichnung der 11 Parameter“). Dazu heat.c_kal
(fünf Eingänge, dreimal „Quelle“, zweimal „Abschätzung von KAP3“), uv.c_kal und ein synthetischer
Zweistufen-Fall für ``enthaelt_abschaetzung`` über alle Rechenstufen.
"""

from __future__ import annotations

import os
import re
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from regel_k_tabelle import KLASSE, KOPF, QUERSCHNITT  # noqa: E402
from app.services import parameter_registry  # noqa: E402
from app.services.engine.impact import params as impact_params  # noqa: E402

OHNE_STELLE = {"uv.ssd_delta_region"}
BLOCK_ID = re.compile(r"^(?:heat|pollen|uv)\.[a-z0-9_]+$")


def _zellen(zeile: str) -> list[str]:
    return [c.strip().replace(chr(96), "") for c in zeile.strip().strip("|").split("|")]


def _quelltext() -> str:
    with open(os.path.abspath(QUERSCHNITT), encoding="utf-8") as fh:
        return fh.read()


def _tabelle() -> list[dict[str, str]]:
    """Zeilen der Tabelle der 11 Blöcke als Spalte → Zelle (ohne Backticks)."""
    zeilen = _quelltext().splitlines()
    start = next(i for i, z in enumerate(zeilen) if z.startswith(KOPF))
    kopf = _zellen(zeilen[start])
    out = []
    for z in zeilen[start + 2:]:          # Zeile start + 1 ist die Trennzeile |---|
        if not z.startswith("|"):
            break
        out.append(dict(zip(kopf, _zellen(z))))
    return out


def _bericht_bloecke(bericht: str) -> set[str]:
    """Block-IDs des Berichts: alle ``id:`` in Kapitel 7 (Eingänge sind Blöcke, wenn sie dort stehen)."""
    namen = {"95": "95_hitzebelastung", "96": "96_aeroallergene", "98": "98_uv_schaedigungen"}
    pfad = os.path.join(os.path.dirname(QUERSCHNITT), f"{namen[bericht]}.md")
    with open(os.path.abspath(pfad), encoding="utf-8") as fh:
        text = fh.read()
    start = text.index("## 7 Parameter-Blöcke")
    return set(re.findall(r"^\s+id: (\S+)", text[start:text.index("\n## 8 ", start)], re.M))


@pytest.fixture(scope="module")
def registry() -> list[dict]:
    return parameter_registry.catalog_parameters()


@pytest.fixture(scope="module")
def zeilen() -> list[dict[str, str]]:
    z = _tabelle()
    assert len(z) == 11, [r["Block-ID"] for r in z]
    return z


def _je_block(registry: list[dict], block: str) -> list[dict]:
    return [p for p in registry if p["methodik_block"] == block]


def test_tabelle_nennt_die_elf_bloecke(zeilen):
    assert {r["Block-ID"] for r in zeilen} == {
        "heat.c_kal", "heat.beta_pfl", "heat.h_heim", "pollen.d_saison", "pollen.c_tag",
        "uv.ssd_delta_region", "uv.k_uv", "uv.baf", "uv.lambda", "uv.l_rest", "uv.c_kal"}


def test_registry_folgt_der_tabelle_je_parameter(registry, zeilen):
    ohne_parameter = set()
    for zeile in zeilen:
        block = zeile["Block-ID"]
        soll_klasse = KLASSE[zeile["Kennzeichnung nach der Regel"]]
        soll_text = zeile["Anzeigetext"].strip("„“")
        soll_aus = [e for e in zeile["Eingänge"].split(" · ") if e in _bericht_bloecke(zeile["Bericht"])]
        ps = _je_block(registry, block)
        if not ps:
            ohne_parameter.add(block)
            continue
        for p in ps:
            assert p["evidence_class"] == soll_klasse, (p["id"], p["evidence_class"], soll_klasse)
            assert parameter_registry.anzeigetext(p) == soll_text, (p["id"], soll_text)
            if soll_klasse == "berechnet":
                assert p["abgeleitet_aus"] == soll_aus, (p["id"], p["abgeleitet_aus"], soll_aus)
                assert [e["block"] for e in p["eingaenge"]] == soll_aus, p["id"]
            else:
                assert p["abgeleitet_aus"] == [], (p["id"], "abgeleitet_aus nur bei berechnet")
                assert p["eingaenge"] == [], p["id"]
    assert ohne_parameter == OHNE_STELLE, ohne_parameter


def test_zeile_ohne_registry_parameter_verweist_auf_die_uebernahmeliste(zeilen):
    """uv.ssd_delta_region hat keine Stelle im Produkt; die Übernahmeliste sagt das ausdrücklich."""
    uebernahme = _quelltext().split("\n## Übernahmeliste an den CTO", 1)[1].split("\n## ", 1)[0]
    zeile = next(z for z in uebernahme.splitlines()
                 if z.startswith("| Kennzeichnung der 11 Parameter"))
    assert "uv.ssd_delta_region ohne eigene Stelle" in zeile
    assert [r["Anzeigetext"] for r in zeilen if r["Block-ID"] == "uv.ssd_delta_region"] == ["„Quelle“"]


def test_jeder_parameter_traegt_die_drei_felder(registry):
    for p in registry:
        assert isinstance(p["abgeleitet_aus"], list), p["id"]
        assert isinstance(p["enthaelt_abschaetzung"], bool), p["id"]
        assert isinstance(p["eingaenge"], list), p["id"]
        if p["evidence_class"] != "berechnet":
            assert p["abgeleitet_aus"] == [] and p["eingaenge"] == [], p["id"]
        assert parameter_registry.anzeigetext(p) in {
            "Quelle", "Abschätzung von KAP3", "berechnet aus Quellen",
            "berechnet, enthält Abschätzung von KAP3"}, p["id"]


def test_heat_c_kal_fuenf_eingaenge_mit_abschaetzung(registry):
    ps = _je_block(registry, "heat.c_kal")
    assert len(ps) == 1
    p = ps[0]
    assert [e["block"] for e in p["eingaenge"]] == [
        "heat.t0_region", "heat.beta_85plus_region", "heat.f_alter",
        "heat.m_basissterberate", "heat.q_wochenquantile"]
    assert [e["anzeigetext"] for e in p["eingaenge"]] == [
        "Quelle", "Abschätzung von KAP3", "Abschätzung von KAP3", "Quelle", "Quelle"]
    assert p["enthaelt_abschaetzung"] is True
    assert parameter_registry.anzeigetext(p) == "berechnet, enthält Abschätzung von KAP3"
    assert parameter_registry.zaehlt_als_belegt(p) is False


def test_uv_c_kal_zaehlt_als_belegt_und_eingang_ohne_stelle_hat_klasse(registry):
    ps = _je_block(registry, "uv.c_kal")
    assert {p["id"] for p in ps} and all(parameter_registry.zaehlt_als_belegt(p) for p in ps)
    for p in ps:
        assert p["enthaelt_abschaetzung"] is False
        assert p["eingaenge"] == [{"block": "uv.i_raten_roh", "anzeigetext": "Quelle"}]
    # uv.i_raten_roh hat keine Stelle in der Registry, seine Klasse steht in der Klassentabelle.
    assert not _je_block(registry, "uv.i_raten_roh")
    assert impact_params.KLASSE_OHNE_STELLE["uv.i_raten_roh"] == "belegt"


def test_abgeleitet_aus_der_spezifikation_nennt_nur_parameter_ids():
    for nr, bloecke in (("95", ["heat.c_kal"]), ("98", ["uv.baf", "uv.c_kal"])):
        ids = _bericht_bloecke(nr) | set(impact_params.KLASSE_OHNE_STELLE)
        for b in bloecke:
            assert set(impact_params.ABGELEITET_AUS[b]) <= ids, b
    assert set(impact_params.ABGELEITET_AUS) == {"heat.c_kal", "uv.baf", "uv.c_kal"}


def test_zaehlt_als_belegt_und_belegte_klassen():
    z = parameter_registry.zaehlt_als_belegt
    assert z({"evidence_class": "belegt"}) is True
    assert z({"evidence_class": "abgeschaetzt"}) is False
    assert z({"evidence_class": "berechnet", "enthaelt_abschaetzung": False}) is True
    assert z({"evidence_class": "berechnet", "enthaelt_abschaetzung": True}) is False
    assert parameter_registry.BELEGTE_KLASSEN == frozenset({"belegt", "berechnet"})
    assert parameter_registry.EVIDENCE_CLASSES == ("belegt", "abgeschaetzt", "berechnet")


def test_anzeigetext_liefert_genau_einen_der_vier_texte():
    a = parameter_registry.anzeigetext
    assert a({"evidence_class": "belegt"}) == "Quelle"
    assert a({"evidence_class": "abgeschaetzt"}) == "Abschätzung von KAP3"
    assert a({"evidence_class": "berechnet", "enthaelt_abschaetzung": False}) == "berechnet aus Quellen"
    assert a({"evidence_class": "berechnet", "enthaelt_abschaetzung": True}) == \
        "berechnet, enthält Abschätzung von KAP3"


def test_kommentar_nennt_nicht_mehr_berechnet_aus_anderen_parametern():
    pfad = os.path.join(os.path.dirname(__file__), "..", "app", "services", "parameter_registry.py")
    with open(os.path.abspath(pfad), encoding="utf-8") as fh:
        quelle = fh.read()
    kopf = quelle.split("EVIDENCE_CLASSES = ", 1)[0]
    assert "berechnet aus anderen Parametern" not in kopf


def _synthetisch(klassen: dict[str, str]) -> list[dict]:
    return [parameter_registry._base_param(
        f"synth.{b}", layer_code="", layer_category="synth", label=b, value=1.0,
        evidence_class=k, methodik_block=b) for b, k in klassen.items()]


def test_zweistufenfall_reicht_die_abschaetzung_ueber_alle_rechenstufen_weiter():
    """c berechnet aus b, b berechnet aus a (abgeschätzt) und d (belegt): c enthält die Abschätzung."""
    klassen = {"s.a": "abgeschaetzt", "s.d": "belegt", "s.b": "berechnet", "s.c": "berechnet"}
    aus = {"s.b": ("s.d", "s.a"), "s.c": ("s.b",)}
    out = {p["methodik_block"]: p for p in parameter_registry._mit_eingaengen(
        _synthetisch(klassen), abgeleitet_aus=aus, klasse_ohne_stelle={})}
    assert out["s.b"]["enthaelt_abschaetzung"] is True
    assert out["s.c"]["enthaelt_abschaetzung"] is True
    assert out["s.c"]["abgeleitet_aus"] == ["s.b"]
    assert out["s.c"]["eingaenge"] == [
        {"block": "s.b", "anzeigetext": "berechnet, enthält Abschätzung von KAP3"}]
    assert out["s.b"]["eingaenge"] == [
        {"block": "s.d", "anzeigetext": "Quelle"}, {"block": "s.a", "anzeigetext": "Abschätzung von KAP3"}]
    assert parameter_registry.anzeigetext(out["s.c"]) == "berechnet, enthält Abschätzung von KAP3"
    assert parameter_registry.zaehlt_als_belegt(out["s.c"]) is False


def test_zweistufenfall_ohne_abschaetzung_bleibt_berechnet_aus_quellen():
    klassen = {"s.a": "belegt", "s.b": "berechnet", "s.c": "berechnet"}
    aus = {"s.b": ("s.a", "s.q"), "s.c": ("s.b",)}
    out = {p["methodik_block"]: p for p in parameter_registry._mit_eingaengen(
        _synthetisch(klassen), abgeleitet_aus=aus, klasse_ohne_stelle={"s.q": "belegt"})}
    assert out["s.c"]["enthaelt_abschaetzung"] is False
    assert parameter_registry.anzeigetext(out["s.c"]) == "berechnet aus Quellen"
    assert parameter_registry.zaehlt_als_belegt(out["s.c"]) is True


def test_berechnet_ohne_eintrag_in_abgeleitet_aus_ist_ein_fehler():
    with pytest.raises(ValueError):
        parameter_registry._mit_eingaengen(
            _synthetisch({"s.b": "berechnet"}), abgeleitet_aus={}, klasse_ohne_stelle={})


def test_gefilterte_liste_ohne_eingaenge_laedt_die_klassen_nach():
    """Fehlen die Blöcke der Eingänge in der Liste (gefiltert), kommen ihre Klassen aus der Registry."""
    roh = [p for p in parameter_registry._catalog_parameters_roh() if p["methodik_block"] == "uv.baf"]
    assert roh and all(p["eingaenge"] == [] for p in roh)
    ps = parameter_registry._mit_eingaengen(roh)
    assert all(p["eingaenge"] == [{"block": "uv.w_scc", "anzeigetext": "Quelle"}] for p in ps)
