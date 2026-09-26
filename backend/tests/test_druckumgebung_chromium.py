"""Druckumgebung (T-1423): scripts/html_to_pdf.py erzeugt mit dem Python der
Testlauf-Umgebung per Playwright-Chromium ein PDF."""
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_html_to_pdf_erzeugt_pdf(tmp_path):
    eingabe = tmp_path / "eingabe.html"
    ausgabe = tmp_path / "ausgabe.pdf"
    eingabe.write_text(
        "<!doctype html><html><body><h1>Druckprobe</h1><p>Kurzer Text.</p></body></html>",
        encoding="utf-8",
    )
    lauf = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "html_to_pdf.py"), str(eingabe), str(ausgabe)],
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert lauf.returncode == 0, lauf.stderr
    assert ausgabe.is_file()
    assert ausgabe.read_bytes().startswith(b"%PDF-")
