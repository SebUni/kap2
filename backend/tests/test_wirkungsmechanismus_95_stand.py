"""Die Wirkungsmechanismus-Vorschau #95 liest Revision und Integrationsstand aus dem Bericht (T-1365)."""
import importlib.util
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKRIPT = ROOT / "scripts" / "wirkungsmechanismus_preview.py"
BERICHT = ROOT / "docs" / "methodik" / "95_hitzebelastung.md"


def _modul():
    spec = importlib.util.spec_from_file_location("wm_preview", SKRIPT)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def test_revision_stammt_aus_der_statuszeile():
    soll = re.search(r"^Status:\s*\*\*(Rev\.\s*\d+)", BERICHT.read_text(encoding="utf-8"), re.M).group(1)
    assert _modul().bericht_stand("95")["revision"] == soll


def test_payload_zeigt_revision_und_integrationsstand():
    m = _modul()
    stand = m.bericht_stand("95")
    payload = m.build_payload("95")
    assert stand["revision"] in payload["tabs"][0]["label"]
    assert stand["revision"] in payload["subtitle"]
    assert stand["integration"] in payload["banner"]
    assert stand["integration"].startswith("Im Produkt stehen noch aus:")


def test_keine_festen_staende_mehr_im_skript():
    text = SKRIPT.read_text(encoding="utf-8")
    assert "Bericht Rev. 7)" not in text
    assert "Integration vollzogen (30.08.2026)" not in text
    assert "laut Methodik-Bericht Rev. 7" not in text
