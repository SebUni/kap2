"""Fehlender Gemeindeschlüssel im Assessment-Worker: keine stille Null (T-1814-ceo).

Findet der Worker keinen Gemeindeschlüssel, entfällt Stufe 2 der Ersatzregel 65+ (Bericht #95
§3.3). Das steht als WARNING mit dem Namen der Kommune im Log; das Assessment läuft weiter
(die Funktion gibt ``None`` zurück, statt zu werfen). Läuft ohne Datenbank: die Sitzung ist eine
Attrappe mit leerer Gemeindetabelle.
"""
from __future__ import annotations

import logging
import os
import sys
from types import SimpleNamespace

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from geoalchemy2.shape import from_shape  # noqa: E402
from shapely.geometry import Polygon  # noqa: E402

from app.tasks import assessment_worker  # noqa: E402

TEXT = "Stufe 2 der Ersatzregel 65+ entfällt"


class _AttrappeSitzung:
    """Sitzung mit Gemeindetabelle: leer (``zeilen=[]``) oder mit Treffer."""

    def __init__(self, zeilen=(), fehler=None):
        self.zeilen = list(zeilen)
        self.fehler = fehler
        self.rollbacks = 0

    def query(self, *_spalten):
        return self

    def filter(self, *_bedingungen):
        return self

    def first(self):
        if self.fehler:
            raise self.fehler
        return self.zeilen[0] if self.zeilen else None

    def rollback(self):
        self.rollbacks += 1


def _warmsen(mit_grenze=True):
    flaeche = Polygon([(9.2, 52.6), (9.3, 52.6), (9.3, 52.7), (9.2, 52.7)])
    return SimpleNamespace(
        name="Warmsen",
        boundary=from_shape(flaeche, srid=4326) if mit_grenze else None,
    )


def _warnungen(caplog):
    return [r for r in caplog.records if r.levelno == logging.WARNING and TEXT in r.getMessage()]


def test_leere_gemeindetabelle_warnt_mit_kommunenname(caplog):
    with caplog.at_level(logging.WARNING, logger=assessment_worker.log.name):
        ags = assessment_worker._gemeindeschluessel(_AttrappeSitzung(), _warmsen())
    assert ags is None  # Assessment läuft weiter, wie bisher
    treffer = _warnungen(caplog)
    assert len(treffer) == 1
    assert "Warmsen" in treffer[0].getMessage()


def test_abfragefehler_warnt_und_kippt_nichts(caplog):
    db = _AttrappeSitzung(fehler=RuntimeError("Tabelle gemeinden fehlt"))
    with caplog.at_level(logging.WARNING, logger=assessment_worker.log.name):
        ags = assessment_worker._gemeindeschluessel(db, _warmsen())
    assert ags is None
    assert db.rollbacks == 1
    treffer = _warnungen(caplog)
    assert len(treffer) == 1
    assert "Warmsen" in treffer[0].getMessage()
    assert "Tabelle gemeinden fehlt" in treffer[0].getMessage()


def test_kommune_ohne_grenze_warnt(caplog):
    with caplog.at_level(logging.WARNING, logger=assessment_worker.log.name):
        ags = assessment_worker._gemeindeschluessel(_AttrappeSitzung(), _warmsen(mit_grenze=False))
    assert ags is None
    assert len(_warnungen(caplog)) == 1


def test_treffer_liefert_schluessel_ohne_warnung(caplog):
    db = _AttrappeSitzung(zeilen=[("03256034",)])
    with caplog.at_level(logging.WARNING, logger=assessment_worker.log.name):
        ags = assessment_worker._gemeindeschluessel(db, _warmsen())
    assert ags == "03256034"
    assert _warnungen(caplog) == []
