"""Block-Kennung und Kennzeichnung der 14 Parameter-Blöcke von #96 (T-1480, Vorgabe P1).

Kapitel 7 von ``docs/methodik/96_aeroallergene.md`` trägt je Block eine ``kennzeichnung``
(``quelle`` | ``abschaetzung_kap3`` | ``berechnet``). Die Registry führt sie als
``evidence_class`` (``belegt`` | ``abgeschaetzt`` | ``berechnet``) und die Block-Kennung
im Feld ``methodik_block``. Geprüft wird:

1. Die Menge der ``pollen.*``-Kennungen der Registry ist genau die Menge der 14 Blöcke,
   gezählt über verschiedene Kennungen: 3 × belegt, 9 × abgeschätzt, 2 × berechnet.
2. Jeder #96-Parameter der Registry trägt Kennung und Klasse seines Blocks; Katalog-Blöcke
   stehen am Risiko (pollen.c_tag) bzw. an der Maßnahme POLLEN_EARLY_WARNING (pollen.r_s158).
3. pollen.t_warn_s158 = 0,75 ist ein Spec des Risikos, kein Feld der Maßnahme; seit
   T-1513-cto editierbar (wirkt auf den S158-Maßnahmen-Faktor, nicht auf die Zelle).
4. pollen.d_saison und pollen.c_jahr_direkt stehen in der Parameterliste, sind nicht
   editierbar und rechnen nicht in der Schadensfunktion.
5. Jeder belegte Block löst seine Quelle in sources.SOURCE_REFERENCES auf; jeder
   abgeschätzte Block trägt eine Herleitung mit Wert, Band und Sensitivität.
6. Der Wert jedes Parameters stimmt mit dem ``wert`` seines Blocks überein.
"""

from __future__ import annotations

import os
import re
import sys
from collections import Counter

import yaml

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.data import catalog, sources  # noqa: E402
from app.services import parameter_registry  # noqa: E402
from app.services.engine import impact, override_context  # noqa: E402
from app.services.engine.impact.base import CellContext  # noqa: E402

REPORT = os.path.join(os.path.dirname(__file__), "..", "..",
                      "docs", "methodik", "96_aeroallergene.md")
CODE = "EXPECTED_ANNUAL_ALLERGY_DAYS"
_KLASSE = {"quelle": "belegt", "abschaetzung_kap3": "abgeschaetzt", "berechnet": "berechnet"}

# Schlüssel der Mehrfach-Blöcke → Suffix der Registry-ID.
_SUFFIX = {"u20": "u20", "20-64": "a20_64", "65-74": "a65_74", "75-84": "a75_84",
           "85+": "a85p", "birkengruppe": "birke", "graeser": "graeser",
           "vorgezogen": "vorgezogen", "nachpflanzung": "nachpflanzung"}


def _kapitel7() -> str:
    with open(os.path.abspath(REPORT), encoding="utf-8") as fh:
        text = fh.read()
    start = text.index("## 7 Parameter-Blöcke")
    ende = text.index("\n## 8 ", start)
    return text[start:ende]


def _bloecke() -> dict[str, dict]:
    """Block-Kennung → Block (aus dem YAML-Abschnitt von Kapitel 7)."""
    yaml_teil = "\n".join(re.findall(r"```yaml\n(.*?)```", _kapitel7(), re.S))
    bloecke = {}
    for teil in re.split(r"^parameter:\n", yaml_teil, flags=re.M):
        if not teil.strip():
            continue
        b = yaml.safe_load(teil)
        bloecke[b["id"]] = b
    return bloecke


def _nach_block() -> dict[str, list[dict]]:
    nach_block: dict[str, list[dict]] = {}
    for p in parameter_registry.catalog_parameters():
        if (p.get("methodik_block") or "").startswith("pollen."):
            nach_block.setdefault(p["methodik_block"], []).append(p)
    return nach_block


def test_block_kennungen_sind_genau_die_14_aus_kapitel_7():
    soll = set(_bloecke())
    roh = re.findall(r"^  id: (pollen\.\S+)", _kapitel7(), re.M)
    assert len(roh) == 14 and set(roh) == soll, sorted(roh)
    ist = set(_nach_block())
    assert ist == soll, (f"fehlen in der Registry: {sorted(soll - ist)}; "
                         f"nicht in Kapitel 7: {sorted(ist - soll)}")


def test_zaehlung_der_kennzeichnungen_3_9_2():
    bloecke = _bloecke()
    soll = Counter(_KLASSE[b["kennzeichnung"]] for b in bloecke.values())
    nach_block = _nach_block()
    ist = Counter()
    for bid in bloecke:
        klassen = {p["evidence_class"] for p in nach_block[bid]}
        assert len(klassen) == 1, (bid, klassen)
        ist[klassen.pop()] += 1
    zaehlung = {"belegt": ist["belegt"], "abgeschaetzt": ist["abgeschaetzt"],
                "berechnet": ist["berechnet"]}
    print(f"{len(bloecke)} verschiedene Block-Kennungen pollen.*: {zaehlung}")
    assert zaehlung == {"belegt": 3, "abgeschaetzt": 9, "berechnet": 2}
    assert dict(soll) == dict(ist)
    # Mehrfach-Blöcke: gezählt werden Kennungen, nicht Registry-Zeilen.
    assert len(nach_block["pollen.delta_s_region"]) == 6
    assert len(nach_block["pollen.p_ar"]) == 5


def test_jeder_parameter_des_risikos_traegt_block_und_klasse():
    bloecke = _bloecke()
    ohne, falsch = [], []
    for p in parameter_registry.catalog_parameters(layer_code=CODE):
        if ".impact." not in p["id"] and not p["id"].endswith(".cost_per_outcome"):
            continue
        bid = p.get("methodik_block")
        if bid not in bloecke:
            ohne.append(p["id"])
        elif p["evidence_class"] != _KLASSE[bloecke[bid]["kennzeichnung"]]:
            falsch.append((p["id"], bid, p["evidence_class"]))
    assert not ohne, ohne
    assert not falsch, falsch


def test_katalog_bloecke_am_risiko_und_an_der_massnahme():
    by_id = {p["id"]: p for p in parameter_registry.catalog_parameters()}
    c_tag = by_id[f"risks.{CODE}.cost_per_outcome"]
    assert c_tag["methodik_block"] == "pollen.c_tag" and c_tag["value"] == 6.20
    assert c_tag["evidence_class"] == "berechnet"
    c_jahr = by_id[f"risks.{CODE}.impact.c_jahr_direkt"]
    assert c_jahr["methodik_block"] == "pollen.c_jahr_direkt" and c_jahr["layer_code"] == CODE
    r = by_id["measures.POLLEN_EARLY_WARNING.default_reduction"]
    assert r["methodik_block"] == "pollen.r_s158" and r["evidence_class"] == "abgeschaetzt"
    assert r["value"] == 0.03


def test_t_warn_ist_spec_des_risikos_nicht_der_massnahme():
    by_id = {p["id"]: p for p in parameter_registry.catalog_parameters()}
    t = by_id[f"risks.{CODE}.impact.t_warn_s158"]
    assert t["value"] == 0.75 and t["methodik_block"] == "pollen.t_warn_s158"
    # Seit T-1513-cto editierbar (Nachtrag CEO T-1431-ceo, 27.09.2026): die Wirkung von
    # S158 im Maßnahmen-Modul ist gebaut, eine Überschreibung wirkt auf den Zellfaktor.
    assert t["evidence_class"] == "abgeschaetzt" and t["editable"] is True
    massnahme = [p for p in by_id if p.startswith("measures.POLLEN_EARLY_WARNING.")]
    assert len(massnahme) == 9, massnahme
    assert not [p for p in massnahme if "t_warn" in p]
    assert "t_warn_s158" not in catalog.MEASURES_BY_CODE["POLLEN_EARLY_WARNING"]


def _ctx() -> CellContext:
    """Zelle mit 1.000 Einwohnern in Hessen (Region Mitte), Ĝ gleich dem Referenzmittel."""
    bands = {"u20": 180.0, "a20_64": 600.0, "a65_74": 110.0, "a75_84": 80.0, "a85p": 30.0}
    bands["u65"] = bands["u20"] + bands["a20_64"]
    return CellContext(
        ci={"pop": 1000.0, "pop_age_bands": bands},
        hev={"hazards": {"POLLEN_LOAD": 0.2}, "exposures": {}, "vulnerabilities": {}},
        hev_norm={"hazards": {}, "exposures": {}, "vulnerabilities": {}},
        indices={}, regional={"bundesland": "Hessen", "pollen_g_bar": 0.2})


def test_nicht_rechnende_bloecke_aendern_keine_rechnung():
    """d_saison und c_jahr_direkt: nicht editierbar, rechnen nicht in der Schadensfunktion.

    t_warn_s158 steht seit T-1513-cto NICHT mehr in dieser Schleife — es ist editierbar
    (test_t_warn_ist_spec_des_risikos_nicht_der_massnahme), weil eine Überschreibung
    seither den Maßnahmen-Faktor von S158 bewegt (measure_service._s158_cell_factor).
    Der Basiswert der Zelle (diese Funktion hier) bleibt aber unberührt: S158 wirkt
    ausschließlich im Maßnahmen-Modul, nicht in ``impact.compute_all_cell_impacts``.
    """
    by_id = {p["id"]: p for p in parameter_registry.catalog_parameters()}
    d = by_id[f"risks.{CODE}.impact.d_saison"]
    assert d["evidence_class"] == "berechnet" and d["value"] == 43.05
    for key in ("d_saison", "c_jahr_direkt"):
        assert by_id[f"risks.{CODE}.impact.{key}"]["editable"] is False, key
    override_context.set_overrides({})
    try:
        basis = impact.compute_all_cell_impacts(_ctx())[CODE]
        assert basis["outcome"] > 0 and basis["cost_eur"] > 0
        for key, val in (("d_saison", 60.0), ("c_jahr_direkt", 500.0),
                         ("t_warn_s158", 1.0)):
            override_context.set_overrides({f"risks.{CODE}.impact.{key}": val})
            got = impact.compute_all_cell_impacts(_ctx())[CODE]
            assert got["outcome"] == basis["outcome"], key
            assert got["cost_eur"] == basis["cost_eur"], key
    finally:
        override_context.set_overrides({})


def test_belegte_bloecke_loesen_ihre_quelle_auf():
    nach_block = _nach_block()
    ohne = []
    for bid, block in _bloecke().items():
        if block["kennzeichnung"] != "quelle":
            continue
        for p in nach_block[bid]:
            keys = [r.get("key") for r in p.get("references") or []]
            if not keys or not all(k in sources.SOURCE_REFERENCES for k in keys):
                ohne.append((bid, p["id"], keys))
    assert not ohne, ohne


def test_abgeschaetzte_bloecke_tragen_herleitung():
    nach_block = _nach_block()
    ohne = []
    for bid, block in _bloecke().items():
        if block["kennzeichnung"] != "abschaetzung_kap3":
            continue
        for p in nach_block[bid]:
            h = p.get("evidence_derivation") or {}
            fehlt = [f for f in ("wert", "band", "sensitivitaet") if not h.get(f)]
            if fehlt:
                ohne.append((bid, p["id"], fehlt))
    assert not ohne, ohne


def test_werte_stimmen_mit_den_bloecken_ueberein():
    nach_block = _nach_block()
    abweichungen = []
    for bid, block in _bloecke().items():
        wert = block["wert"]
        for p in nach_block[bid]:
            if isinstance(wert, dict):
                treffer = [v for k, v in wert.items() if p["id"].endswith("_" + _SUFFIX[k])]
                if len(treffer) != 1 or abs(p["value"] - float(treffer[0])) > 1e-9:
                    abweichungen.append((bid, p["id"], p["value"], wert))
            elif isinstance(wert, str):
                continue  # pollen.delta_s_region: Verweis auf die Kalibrier-Anlage
            elif abs(p["value"] - float(wert)) > 1e-9:
                abweichungen.append((bid, p["id"], p["value"], wert))
    assert not abweichungen, abweichungen


if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main([__file__, "-q", "-s"]))
