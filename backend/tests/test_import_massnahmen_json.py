"""Excel-Import der Maßnahmen: nicht lesbares JSON in der Konfigurationsspalte (T-1800-cto, Mangel 4).

Läuft ohne Datenbank: die Sitzung ist ein Ersatzobjekt.
"""
import io
from unittest.mock import MagicMock

from openpyxl import Workbook

from app.services.export_service import import_measures_xlsx

WKT = "POINT (13.4 52.5)"


def _xlsx(zellen: list) -> io.BytesIO:
    wb = Workbook()
    ws = wb.active
    ws.title = "Maßnahmen"
    ws.append(["ID", "Name", "Typ", "Jahr", "Beschreibung", "Konfiguration", "Geometrie"])
    for n, zelle in enumerate(zellen, start=1):
        ws.append([n, f"M{n}", "LOW_ALLERGEN_TREE_SELECTION", 2030, "", zelle, WKT])
    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)
    return buf


def _importiere(zellen: list):
    db = MagicMock()
    res = import_measures_xlsx(db, 1, _xlsx(zellen))
    return db, res


def test_kaputtes_json_wird_fehlerzeile_ohne_massnahme():
    db, res = _importiere(["{kaputt"])
    assert res["imported"] == 0
    assert res["skipped"] == 1
    assert len(res["errors"]) == 1
    assert "Zeile 2" in res["errors"][0]
    db.add.assert_not_called()


def test_leere_zelle_legt_massnahme_mit_leerer_config_an():
    db, res = _importiere([None])
    assert res["imported"] == 1
    assert res["skipped"] == 0
    assert res["errors"] == []
    db.add.assert_called_once()
    assert db.add.call_args[0][0].config == {}


def test_kaputte_zeile_neben_gueltiger_zeile():
    db, res = _importiere(["{}", "nicht json"])
    assert res["imported"] == 1
    assert res["skipped"] == 1
    assert "Zeile 3" in res["errors"][0]
