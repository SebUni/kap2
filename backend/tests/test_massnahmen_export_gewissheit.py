"""T-1425: Maßnahmen-Excel trägt die Spalten „Gewissheit“ und „Umsetzung“ wie die Oberfläche.

Ohne Datenbank (Session-Doppel). Prüft (a) die beiden letzten Kopfzellen, (b) je Maßnahmenzeile
nicht leere Werte, gleich dem Text aus denselben Quellen wie die Oberfläche
(``massnahmen_gewissheit``, ``MASSNAHMEN_UMSETZUNG``), (c) Reimport ergibt dieselben Maßnahmen.
"""

from __future__ import annotations

import io

import pytest

openpyxl = pytest.importorskip("openpyxl")
if not hasattr(openpyxl, "__version__"):
    pytest.skip("echtes openpyxl nötig", allow_module_level=True)

from geoalchemy2.shape import from_shape  # noqa: E402
from shapely.geometry import Point  # noqa: E402

from app.data import catalog  # noqa: E402
from app.data.massnahmen_umsetzung import MASSNAHMEN_UMSETZUNG  # noqa: E402
from app.models.models import (  # noqa: E402
    AdaptationMeasure, ConfigParameter, Kommune, MeasureImpact,
)
from app.services import export_service, measure_service  # noqa: E402
from app.services import massnahmen_gewissheit as mg  # noqa: E402

KOMMUNE_ID = 1
EVIDENZ = {"abgeschaetzt": "abgeschätzt (KAP3)", "berechnet": "berechnet aus anderen Parametern",
           "belegt": "belegt"}
EBENE_LABEL = {"gemeinde": "Gemeinde", "kreis": "Kreis", "land": "Land"}


class _Q:
    def __init__(self, rows):
        self._rows = list(rows)

    def filter(self, *a, **k):
        return self

    def limit(self, *a, **k):
        return self

    def all(self):
        return list(self._rows)

    def first(self):
        return self._rows[0] if self._rows else None


class _DB:
    def __init__(self, rows):
        self._rows = rows
        self.added = []

    def query(self, model, *a, **k):
        return _Q(self._rows.get(model, []))

    def add(self, obj):
        self.added.append(obj)

    def commit(self):
        pass


@pytest.fixture
def exportiert(monkeypatch):
    codes = [m["code"] for m in catalog.MEASURES[:5]]
    massnahmen = [
        AdaptationMeasure(
            id=i, kommune_id=KOMMUNE_ID, name=f"Maßnahme {i}", measure_type=c,
            geometry=from_shape(Point(8.0 + i / 100, 50.0), srid=4326), config={"count": i},
            implementation_year=2027, description="", impact_summary={})
        for i, c in enumerate(codes, start=1)
    ]
    kommune = Kommune(id=KOMMUNE_ID, name="Testheim", osm_id="R1", population=5000, area_km2=10.0)
    db = _DB({AdaptationMeasure: massnahmen, MeasureImpact: [], ConfigParameter: [],
              Kommune: [kommune]})
    cov = catalog.euro_coverage(catalog.RISKS)
    agg = {"cost": {"total_eur": 0.0, "by_risk": [],
                    "euro_coverage": {"covered": cov.covered, "total": cov.total, "text": cov.text}},
           "groups": {}}
    monkeypatch.setattr(measure_service, "get_risk_aggregate", lambda *a, **k: agg)
    monkeypatch.setattr(
        measure_service, "ensure_fresh_impact_summary",
        lambda _db, m: {"capex_eur": 1.0, "opex_annual_eur": 1.0, "annual_benefit_eur": 1.0,
                        "count": (m.config or {}).get("count")})
    daten = export_service.export_measures_xlsx(db, KOMMUNE_ID)
    return massnahmen, daten


def test_a_kopfzeile_endet_mit_gewissheit_und_umsetzung(exportiert):
    _, daten = exportiert
    ws = openpyxl.load_workbook(io.BytesIO(daten))["Maßnahmen"]
    assert [c.value for c in ws[1]][-2:] == ["Gewissheit", "Umsetzung"]


def test_b_zellen_gleich_dem_wert_der_oberflaeche(exportiert):
    massnahmen, daten = exportiert
    ws = openpyxl.load_workbook(io.BytesIO(daten))["Maßnahmen"]
    gew = {g["code"]: g for g in mg.massnahmen_gewissheit()}
    zeilen = list(ws.iter_rows(min_row=2, values_only=True))
    assert len(zeilen) == len(massnahmen)
    for z in zeilen:
        code = z[2]
        assert z[-2] and z[-1]
        g = gew[code]
        erwartet = [k["name"] + ": " + k["gewissheitsstufe"] + (" (qualitativ)" if k["qualitativ"] else "")
                    for k in g["klimawirkungen"]]
        teile = z[-2].split("\n")
        assert teile[:-1] == erwartet
        ev = g["wirkung_evidenz"]
        assert teile[-1] == EVIDENZ.get(ev, ev)
        u = MASSNAHMEN_UMSETZUNG[code]
        b = u.get("beleg") or {}
        if b.get("quelle"):
            beleg = "Quelle: " + b["quelle"] + (", S. " + b["seite"] if b.get("seite") else "")
        elif b.get("abschaetzung"):
            beleg = "Abschätzung von KAP3" + (": " + b["herleitung"] if b.get("herleitung") else "")
        else:
            beleg = ""
        zeilen_u = [
            "Kommune allein" if u.get("umsetzung") == "kommune_allein" else "mit Partnern",
            "Ebenen: " + (", ".join(EBENE_LABEL.get(e, e) for e in u.get("ebenen") or []) or "–"),
        ]
        if u.get("partner"):
            zeilen_u.append("Partner: " + ", ".join(u["partner"]))
        if beleg:
            zeilen_u.append(beleg)
        assert z[-1] == "\n".join(zeilen_u)


def test_c_reimport_ergibt_dieselben_massnahmen(exportiert):
    massnahmen, daten = exportiert
    ziel = _DB({})
    ergebnis = export_service.import_measures_xlsx(ziel, KOMMUNE_ID, io.BytesIO(daten))
    assert ergebnis["imported"] == len(massnahmen) and ergebnis["skipped"] == 0
    assert [(m.name, m.measure_type, m.implementation_year, m.config) for m in ziel.added] == [
        (m.name, m.measure_type, m.implementation_year, m.config) for m in massnahmen]
