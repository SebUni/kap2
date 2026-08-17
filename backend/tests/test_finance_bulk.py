"""Tests des finance_bulk (Bulk-Import Gemeindefinanzen 71717 → Chip-Store).

Netz-/DB-frei: geprüft werden der ffcsv-Parser (Ebene FGEMEIN, Kennzahl AUSZ001),
die Namensnormierung/der Kreis+Name-Schlüssel, die Validierung, der atomare
selbstheilende Swap (alter Stand bleibt bei ungültigem Import) und der Lookup.
"""

from __future__ import annotations

import gzip
import json
import os

import pytest

from app.config import settings
from app.services import finance_bulk

# Reales 71717-ffcsv-Layout (spaltenbenannt).
HDR = (
    "statistics_code;statistics_label;time_code;time_label;time;"
    "1_variable_code;1_variable_label;1_variable_attribute_code;1_variable_attribute_label;"
    "value;value_unit;value_variable_code;value_variable_label"
)


def _row(year, code, label, value, *, level="FGEMEIN", vvc="AUSZ001", unit="EUR"):
    return (f"71717;Rechnungsergebnisse;JAHR;Jahr;{year};{level};Ebene;"
            f"{code};{label};{value};{unit};{vvc};Auszahlungen")


def _csv(*rows):
    return "\n".join([HDR, *rows])


# ── Namensnormierung ────────────────────────────────────────────────────────────

def test_norm_name_strips_rechtsform_and_brackets():
    assert finance_bulk._norm_name("Oschatz, Stadt") == "oschatz"
    assert finance_bulk._norm_name("Stadt Oschatz") == "oschatz"
    assert finance_bulk._norm_name("Rhede (Ems)") == "rhede"
    assert finance_bulk._norm_name("Reischach, Verwaltungsgemeinschaft") == "reischach"
    assert finance_bulk._norm_name("  LEIPZIG , Stadt ") == "leipzig"


# ── build_lookup ────────────────────────────────────────────────────────────────

def test_build_lookup_filters_level_and_variable():
    text = _csv(
        _row(2021, "F1471300000", "Leipzig, Stadt", "2400000000"),
        _row(2022, "F1471300000", "Leipzig, Stadt", "2500000000"),
        # falsche Kennzahl → ignoriert
        _row(2022, "F1471300000", "Leipzig, Stadt", "999", vvc="AINVD78"),
        # falsche Ebene (Kreis) → ignoriert
        _row(2022, "F14713", "Leipzig, Stadt", "111", level="FKREISE"),
        # Fehlwert → übersprungen
        _row(2020, "F1471300000", "Leipzig, Stadt", "."),
    )
    lk = finance_bulk.build_lookup(text)
    assert set(lk) == {"14713|leipzig"}
    assert lk["14713|leipzig"]["series"] == {2021: 2400000000.0, 2022: 2500000000.0}


def test_build_lookup_keys_by_kreis_and_name():
    text = _csv(
        _row(2022, "F1473002300", "Oschatz, Stadt", "26697485"),
        _row(2022, "F1472900400", "Böhlen, Stadt", "17938471"),
    )
    lk = finance_bulk.build_lookup(text)
    assert "14730|oschatz" in lk and "14729|böhlen" in lk
    assert lk["14730|oschatz"]["series"][2022] == 26697485.0


# ── Validierung ─────────────────────────────────────────────────────────────────

def test_validate_rejects_sparse_or_missing_anchor():
    ok, _ = finance_bulk._validate({"14713|leipzig": {"series": {2022: 2e9}}})
    assert ok is False  # zu wenige Gemeinden
    big = {f"{i:05d}|x{i}": {"series": {2022: 1.0}} for i in range(4000)}
    ok, _ = finance_bulk._validate(big)
    assert ok is False  # Anker fehlen


# ── Lookup ──────────────────────────────────────────────────────────────────────

def test_budget_for_kommune_matches_and_averages(monkeypatch, tmp_path):
    store = tmp_path / "budget.json.gz"
    monkeypatch.setattr(finance_bulk, "_STORE_PATH", str(store))
    monkeypatch.setattr(finance_bulk, "_mem", None, raising=False)
    monkeypatch.setattr(settings, "REGIONALSTATISTIK_BUDGET_ENABLED", True)
    monkeypatch.setattr(settings, "REGIONALSTATISTIK_BUDGET_AVG_YEARS", 3)
    lookup = {"14730|oschatz": {"label": "Oschatz, Stadt",
                                "series": {2020: 10.0, 2021: 20.0, 2022: 30.0, 2023: 40.0}}}
    finance_bulk._write_store(lookup)

    # AGS-Suffix egal (Match über kreis5+Name); „Stadt Oschatz" normalisiert gleich.
    r = finance_bulk.budget_for_kommune("14730230", "Stadt Oschatz")
    assert r["years"] == [2021, 2022, 2023]
    assert r["avg_expenditure_eur"] == pytest.approx(30.0)
    assert r["level"] == "gemeinde"
    # Unbekannt / disabled → None.
    assert finance_bulk.budget_for_kommune("14730230", "Nirgendwo") is None
    monkeypatch.setattr(settings, "REGIONALSTATISTIK_BUDGET_ENABLED", False)
    assert finance_bulk.budget_for_kommune("14730230", "Oschatz") is None


# ── Atomarer, selbstheilender Swap ──────────────────────────────────────────────

def _anchored_csv():
    # genug Gemeinden + Anker Leipzig/Dresden für die Validierung.
    rows = [_row(2022, "F1471300000", "Leipzig, Stadt", "2000000000"),
            _row(2022, "F1461200000", "Dresden, Stadt", "2000000000")]
    rows += [_row(2022, f"F{i:07d}00", f"Ort{i}", "1000") for i in range(3100)]
    return _csv(*rows)


def test_run_import_atomic_and_self_healing(monkeypatch, tmp_path):
    store = tmp_path / "budget.json.gz"
    monkeypatch.setattr(finance_bulk, "_STORE_PATH", str(store))
    monkeypatch.setattr(finance_bulk, "_clear_finance_osm_cache", lambda: None)

    # 1) Gültiger Import → Store entsteht.
    assert finance_bulk.run_import(text=_anchored_csv()) is True
    assert store.exists()
    with open(store, "rb") as fh:
        first = json.loads(gzip.decompress(fh.read()))
    assert first["meta"]["count"] >= 3000

    # 2) Ungültiger Import (leer / Anker fehlen) → alter Store BLEIBT unverändert.
    mtime = os.path.getmtime(store)
    assert finance_bulk.run_import(text="nur;müll") is False
    assert finance_bulk.run_import(text=_csv(_row(2022, "F1471300000", "X", "1"))) is False
    assert os.path.getmtime(store) == mtime  # nicht überschrieben
    with open(store, "rb") as fh:
        assert json.loads(gzip.decompress(fh.read()))["meta"]["count"] == first["meta"]["count"]


if __name__ == "__main__":
    import sys
    sys.exit(pytest.main([__file__, "-q"]))
