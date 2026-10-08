"""Das Etikett des #96-Tabs der Wirkungsmechanismus-Vorschau trägt keinen festen Berichtsstand (T-1863)."""
import importlib.util
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKRIPT = ROOT / "scripts" / "wirkungsmechanismus_preview.py"
BERICHT = ROOT / "docs" / "methodik" / "96_aeroallergene.md"
HTML = ROOT / "docs" / "methodik" / "96_aeroallergene_wirkungsmechanismus.html"


def _modul():
    spec = importlib.util.spec_from_file_location("wm_preview", SKRIPT)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def _revision_aus_bericht() -> str:
    return re.search(r"^Status:\s*\*\*(Rev\.\s*\d+)", BERICHT.read_text(encoding="utf-8"), re.M).group(1)


def test_revision_stammt_aus_der_statuszeile():
    assert _modul().bericht_stand("96")["revision"] == _revision_aus_bericht()


def test_etikett_des_ziel_tabs_nennt_revision_aus_dem_bericht():
    rev = _revision_aus_bericht()
    label = _modul().build_payload("96")["tabs"][0]["label"]
    assert f"Bericht {rev})" in label, label


def test_quelltext_traegt_keine_feste_revision_im_etikett():
    text = SKRIPT.read_text(encoding="utf-8")
    assert "Ziel-Modell (Bericht Rev." not in text


def test_erzeugte_vorschau_zeigt_die_revision_des_berichts():
    html = HTML.read_text(encoding="utf-8")
    assert f"Ziel-Modell (Bericht {_revision_aus_bericht()})" in html
