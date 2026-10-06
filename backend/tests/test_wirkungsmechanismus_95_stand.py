"""Die Wirkungsmechanismus-Vorschau #95 liest aus dem Bericht nur die Revision (T-1365, T-1679)."""
import importlib.util
import re
from pathlib import Path

import pytest

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


def test_payload_zeigt_revision_ohne_umsetzungsstand():
    m = _modul()
    stand = m.bericht_stand("95")
    payload = m.build_payload("95")
    assert stand["revision"] in payload["tabs"][0]["label"]
    assert stand["revision"] in payload["subtitle"]
    assert "integration" not in stand


def test_keine_festen_staende_mehr_im_skript():
    text = SKRIPT.read_text(encoding="utf-8")
    assert "Bericht Rev. 7)" not in text
    assert "Integration vollzogen" not in text
    assert "laut Methodik-Bericht Rev. 7" not in text
    # T-1679: kein fester Umsetzungsstand in Etiketten, Untertiteln, Notizen oder Bannern
    assert "integriert" not in text
    assert "der Integration" not in text


@pytest.mark.parametrize("nr", ["95", "96", "98"])
def test_payload_ohne_umsetzungsstand(nr):
    payload = _modul().build_payload(nr)
    texte = [payload["subtitle"], payload["banner"]]
    texte += [t["label"] for t in payload["tabs"]] + [t.get("note", "") for t in payload["tabs"]]
    for t in texte:
        assert "integriert" not in t.lower() and "Integration" not in t, t


def test_banner_gibt_nur_die_revision_wieder():
    m = _modul()
    stand = m.bericht_stand("95")
    banner = m.build_payload("95")["banner"]
    assert stand["revision"] in banner
    assert stand["status"] == stand["revision"] or stand["status"] not in banner
