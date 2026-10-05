"""Excel-Import der Maßnahmen prüft die config-Wertebereiche (T-1719-cto, Befund 251 C).

Läuft ohne Datenbank: die Sitzung ist ein Ersatzobjekt.
"""
import io
import json
from unittest.mock import MagicMock

from openpyxl import Workbook

from app.services.export_service import import_measures_xlsx

WKT = "POINT (13.4 52.5)"


def _xlsx(configs: list) -> io.BytesIO:
    wb = Workbook()
    ws = wb.active
    ws.title = "Maßnahmen"
    ws.append(["ID", "Name", "Typ", "Jahr", "Beschreibung", "Konfiguration", "Geometrie"])
    for n, cfg in enumerate(configs, start=1):
        ws.append([n, f"M{n}", "LOW_ALLERGEN_TREE_SELECTION", 2030, "", json.dumps(cfg), WKT])
    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)
    return buf


def _importiere(configs: list):
    db = MagicMock()
    res = import_measures_xlsx(db, 1, _xlsx(configs))
    return db, res


def test_import_weist_anteil_ersetzt_ueber_eins_ab():
    db, res = _importiere([{"anteil_ersetzt": 1.5}])
    assert res["imported"] == 0
    assert res["skipped"] == 1
    assert len(res["errors"]) == 1
    assert "Zeile 2" in res["errors"][0] and "anteil_ersetzt" in res["errors"][0]
    db.add.assert_not_called()


def test_import_legt_anteil_ersetzt_halb_an():
    db, res = _importiere([{"anteil_ersetzt": 0.5}])
    assert res["imported"] == 1
    assert res["errors"] == []
    db.add.assert_called_once()


def test_import_weist_unbekannten_ersatzfall_ab():
    db, res = _importiere([{"ersatzfall": "anders"}])
    assert res["imported"] == 0
    assert len(res["errors"]) == 1
    assert "Zeile 2" in res["errors"][0] and "ersatzfall" in res["errors"][0]
    db.add.assert_not_called()


def test_import_gueltige_zeilen_neben_fehlerzeile():
    db, res = _importiere([
        {"ersatzfall": "vorgezogen"}, {"anteil_ersetzt": 0}, {"anteil_ersetzt": 1.0},
    ])
    assert res["imported"] == 2
    assert res["skipped"] == 1
    assert "Zeile 3" in res["errors"][0]
