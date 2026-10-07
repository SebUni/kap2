"""Die Wirkungsmechanismus-Vorschau #98 folgt dem Bericht und trägt keinen festen Stand (T-1822)."""
import importlib.util
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKRIPT = ROOT / "scripts" / "wirkungsmechanismus_preview.py"
BERICHT = ROOT / "docs" / "methodik" / "98_uv_schaedigungen.md"


def _modul():
    spec = importlib.util.spec_from_file_location("wm_preview", SKRIPT)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def test_revision_stammt_aus_der_statuszeile():
    soll = re.search(r"^Status:\s*\*\*(Rev\.\s*\d+)", BERICHT.read_text(encoding="utf-8"), re.M).group(1)
    assert _modul().bericht_stand("98")["revision"] == soll


def test_banner_und_untertitel_zeigen_revision_ohne_umsetzungsstand():
    m = _modul()
    rev = m.bericht_stand("98")["revision"]
    payload = m.build_payload("98")
    assert rev in payload["banner"]
    assert rev in payload["subtitle"]
    for t in (payload["banner"], payload["subtitle"]):
        assert "integriert" not in t.lower() and "Integration" not in t, t
        assert "Rev. 1 " not in t and "Rev. 1)" not in t


def test_knoten_aus_kapitel_1_sind_vorhanden():
    lineage = _modul().build_payload("98")["tabs"][0]["lineage"]
    knoten = lineage["nodes"]
    text = repr(knoten)
    assert "HEALTHCARE_ACCESS" in text and "R36" in text
    assert "S154" in text and "S155" in text and "S158" in text
    ids = {n["id"] for n in knoten}
    assert "param:uv.s_komforttag" in ids
    assert "param:uv.s155_dosisminderung" in ids
    assert "ind:VERH" not in ids


def test_kein_verhalten_im_pfad_label():
    lineage = _modul().build_payload("98")["tabs"][0]["lineage"]
    pfad = [n for n in lineage["nodes"] if n["id"] == "pathway:0"][0]
    assert "Verhalten" not in repr(pfad)
