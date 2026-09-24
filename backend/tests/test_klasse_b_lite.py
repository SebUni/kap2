"""Verwechslungssperre Klasse A/B in Studie und Gemeinde-Detail (T-0836, Vorhaben T-0563).

Die Lite-Ansicht (LitePanel.tsx) und die Studienseite (StudyPage.tsx) verzweigen
seit T-0518 auf ``has_euro_layer``/``cost_display``. Diese Datei prüft, dass das
Backend die Felder liefert und den gespeicherten Betrag einer Klasse-B-Wirkung
nicht ausgibt:

(a) ``study_service.build_study`` — Rangliste je Wirkung;
(b) ``public_lite.lite_gemeinde`` — Liste ``risks`` der Gemeinde;
(c) die von ``study_service`` geschriebene ``studie.csv`` — keine Euro-Spalte und
    der Betrag der Testwirkung in keiner Datenzeile.

Die Testwirkung stammt aus ``klasse_b_testwirkung``; sie wird zusätzlich in
``lite_scoring.LITE_RISK_CODES`` eingetragen (und in die gleichnamige, beim Import
gebundene Liste von ``study_service``). Statt einer Datenbank dient eine kleine
Ersatz-Session: ``Gemeinde`` trägt eine PostGIS-Spalte, die auf SQLite nicht anlegbar
ist, und beide Ausgaben lesen nur ``query(...).filter(...).all()/.first()``.
"""
from __future__ import annotations

import csv

import pytest

from app.config import settings
from app.data import catalog
from app.models.lite_models import Gemeinde, GemeindeLiteResult
from app.services.lite import lite_scoring, study_service
from app.api.routes import public_lite

from klasse_b_testwirkung import KLASSE_B_CODE, wirkung_einhaengen

AGS = "14612000"
KLASSE_A_CODE = "EXPECTED_ANNUAL_MORTALITY"
KLASSE_A_BETRAG = 123456.0
# Als Zeichenkette in keinem Indexwert oder sonstigen Feld zufällig enthalten.
KLASSE_B_BETRAG = 987654321.0


class _Query:
    def __init__(self, rows):
        self._rows = rows

    def filter(self, *args, **kwargs):
        return self

    def all(self):
        return list(self._rows)

    def first(self):
        return self._rows[0] if self._rows else None


class _Session:
    def __init__(self, gemeinden, results):
        self._gemeinden = gemeinden
        self._results = results

    def query(self, target):
        if target is Gemeinde:
            return _Query(self._gemeinden)
        if target is GemeindeLiteResult:
            return _Query(self._results)
        if target is Gemeinde.vg250_stand:
            return _Query([(g.vg250_stand,) for g in self._gemeinden])
        raise AssertionError(f"unerwartete Abfrage: {target!r}")


@pytest.fixture
def db(monkeypatch, tmp_path):
    wirkung_einhaengen(monkeypatch)
    codes = list(lite_scoring.LITE_RISK_CODES) + [KLASSE_B_CODE]
    monkeypatch.setattr(lite_scoring, "LITE_RISK_CODES", codes)
    monkeypatch.setattr(study_service, "LITE_RISK_CODES", codes)
    monkeypatch.setattr(settings, "LITE_DATA_DIR", str(tmp_path))
    assert KLASSE_A_CODE in codes
    assert catalog.risk_has_euro_layer(catalog.RISKS_BY_CODE[KLASSE_A_CODE])
    assert not catalog.risk_has_euro_layer(catalog.RISKS_BY_CODE[KLASSE_B_CODE])

    gemeinde = Gemeinde(ags=AGS, name="Dresden", bez="Stadt", bundesland="Sachsen",
                        population=560000, area_km2=328.8, vg250_stand="2024")
    results = [
        GemeindeLiteResult(ags=AGS, risk_code=KLASSE_A_CODE, index_value=61.5,
                           outcome_value=12.0, outcome_unit="Todesfälle/Jahr",
                           cost_eur=KLASSE_A_BETRAG, drivers={}),
        GemeindeLiteResult(ags=AGS, risk_code=KLASSE_B_CODE, index_value=44.5,
                           outcome_value=3.0, outcome_unit="Fälle/Jahr",
                           cost_eur=KLASSE_B_BETRAG, drivers={}),
    ]
    return _Session([gemeinde], results)


def _pruefe(zeile_b: dict, zeile_a: dict) -> None:
    assert zeile_b["has_euro_layer"] is False
    assert zeile_b["cost_display"] == catalog.NO_EURO_LAYER_TEXT
    assert zeile_b["cost_eur"] is None
    assert zeile_a["has_euro_layer"] is True
    assert zeile_a["cost_display"] == KLASSE_A_BETRAG


def test_studie_liefert_has_euro_layer_und_cost_display(db):
    study = study_service.build_study(db)
    zeilen_b = study["rankings"][KLASSE_B_CODE]
    zeilen_a = study["rankings"][KLASSE_A_CODE]
    assert zeilen_b and zeilen_a
    for zeile_b in zeilen_b:
        for zeile_a in zeilen_a:
            _pruefe(zeile_b, zeile_a)


def test_gemeinde_detail_liefert_has_euro_layer_und_cost_display(db):
    antwort = public_lite.lite_gemeinde(AGS, db=db)
    by_code = {r["code"]: r for r in antwort["risks"]}
    _pruefe(by_code[KLASSE_B_CODE], by_code[KLASSE_A_CODE])


def test_studie_csv_ohne_euro_spalte_und_ohne_betrag(db, tmp_path):
    study_service.build_study(db)
    with open(tmp_path / "studie.csv", encoding="utf-8", newline="") as fh:
        zeilen = list(csv.reader(fh, delimiter=";"))
    kopf, daten = zeilen[0], zeilen[1:]
    assert f"{KLASSE_B_CODE}_index" in kopf
    assert not [s for s in kopf if s.endswith("_cost_eur")]
    assert daten
    betrag = str(KLASSE_B_BETRAG)
    for zeile in daten:
        assert betrag not in ";".join(zeile)
