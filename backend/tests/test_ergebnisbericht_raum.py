"""#95 je Ortsteil für die Beispielkommune Warmsen (T-1564-cto, Paket 5b von T-1418-cto).

Prüft ``app.services.ergebnisbericht.raum.raumzeilen`` ohne Datenbank und ohne Netzzugriff mit der gepinnten Datei
``ortsteile_03256034.geojson`` und mit künstlichen Flächensätzen, gebaut aus den Zellkoordinaten:

- jede bewohnte Zelle liegt in genau einer Zeile (Ortsteil oder „übriges Gemeindegebiet“);
- Einwohner, Todesfälle, verlorene Lebensjahre, Einweisungen und Jahresbetrag summieren sich über alle Zeilen auf
  ``rechne_95`` für die ganze Kommune, der Betrag auf 1 € genau;
- jede Zeile mit Einwohnern trägt Jahresbetrag, Todesfälle und Einweisungen auch je 1.000 Einwohner;
- eine Fläche ohne bewohnte Zelle hat keinen Betrag, sondern einen Grund;
- ohne Ortsteilfläche gibt es genau eine Zeile für die ganze Kommune.
"""
from __future__ import annotations

import json
import os
import sys

import pytest

HIER = os.path.dirname(os.path.abspath(__file__))
BACKEND = os.path.dirname(HIER)
sys.path.insert(0, BACKEND)

from app.services.ergebnisbericht import beispiel as B  # noqa: E402
from app.services.ergebnisbericht import raum as R  # noqa: E402

GEOJSON = os.path.join(BACKEND, "data", "kalibrierung", "ortsteile_03256034.geojson")


@pytest.fixture(scope="module")
def kommune():
    return B.beispiel("warmsen")


@pytest.fixture(scope="module")
def gesamt(kommune):
    return B.rechne_95(kommune)


@pytest.fixture(scope="module")
def bewohnt(kommune):
    gids, cis, _ = B.zellen(kommune.ags)
    return [g for g, ci in zip(gids, cis) if float(ci["pop"]) > 0]


def _pruefe(zeilen, gesamt, bewohnt):
    # Jede bewohnte Zelle in genau einer Zeile
    zaehler: dict[str, int] = {}
    for z in zeilen:
        for g in z.zellkennungen:
            zaehler[g] = zaehler.get(g, 0) + 1
    for g in bewohnt:
        assert zaehler.get(g) == 1, f"Zelle {g} liegt in {zaehler.get(g, 0)} Zeilen"

    # Summen gleich der ganzen Kommune
    def summe(attr):
        return sum(getattr(z, attr) or 0.0 for z in zeilen)

    assert summe("einwohner") == pytest.approx(gesamt.einwohner, abs=1e-6)
    assert summe("einwohner_ab65") == pytest.approx(gesamt.einwohner_ab65, abs=1e-6)
    assert summe("todesfaelle") == pytest.approx(gesamt.todesfaelle, rel=1e-9, abs=1e-9)
    assert summe("yll") == pytest.approx(gesamt.yll, rel=1e-9, abs=1e-9)
    assert summe("einweisungen") == pytest.approx(gesamt.einweisungen, rel=1e-9, abs=1e-9)
    assert abs(summe("jahresbetrag_eur") - gesamt.jahresbetrag_eur) < 1.0

    for z in zeilen:
        if z.einwohner > 0:
            assert z.jahresbetrag_eur is not None and z.grund is None
            assert z.jahresbetrag_je_1000_eur == pytest.approx(z.jahresbetrag_eur / z.einwohner * 1000)
            assert z.todesfaelle_je_1000 == pytest.approx(z.todesfaelle / z.einwohner * 1000)
            assert z.einweisungen_je_1000 == pytest.approx(z.einweisungen / z.einwohner * 1000)
            assert z.hitzetage is not None and z.hitzetage > 0
            assert z.yll is not None and z.einwohner_ab65 >= 0
        else:
            assert z.jahresbetrag_eur is None
            assert z.grund and z.grund.strip()


# --- Künstliche Flächen aus den Zellkoordinaten -------------------------------------------------------------------

def _rechteck(x0, y0, x1, y1, name, ebene=10):
    """Rechteck in EPSG:3035 → GeoJSON-Feature in EPSG:4326."""
    ecken = [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)]
    ring = [list(R._nach_4326().transform(x, y)) for x, y in ecken]
    return {"type": "Feature", "properties": {"name": name, "admin_level": ebene},
            "geometry": {"type": "Polygon", "coordinates": [ring]}}


@pytest.fixture(scope="module")
def raster(bewohnt):
    """Linke untere Ecken der bewohnten Zellen in EPSG:3035."""
    ecken = [(x - 50.0, y - 50.0) for x, y in (R.zellmitte_3035(g) for g in bewohnt)]
    xs = sorted({x for x, _ in ecken})
    ys = sorted({y for _, y in ecken})
    return ecken, xs, ys


@pytest.fixture(scope="module")
def zwei_rechtecke(raster):
    """West-Rechteck über die ganze Höhe, Ost-Rechteck nur über die südliche Hälfte (der Nordosten bleibt
    „übriges Gemeindegebiet“), dazu eine Fläche 100 km entfernt ohne bewohnte Zelle."""
    _, xs, ys = raster
    xm, ym = xs[len(xs) // 2], ys[len(ys) // 2]
    x0, x1, y0, y1 = xs[0], xs[-1] + 100, ys[0], ys[-1] + 100
    return {"type": "FeatureCollection", "features": [
        _rechteck(x0, y0, xm, y1, "West"),
        _rechteck(xm, y0, x1, ym, "Südost"),
        _rechteck(x1 + 100_000, y0, x1 + 101_000, y0 + 1_000, "Leer"),
    ]}


def test_zellmitte_aus_kennung():
    x, y = R.zellmitte_3035("CRS3035RES100mN3274700E4213600")
    assert (x, y) == (4213650.0, 3274750.0)
    lon, lat = R.zellmitte_4326("CRS3035RES100mN3274700E4213600")
    assert 5.5 < lon < 15.5 and 47.0 < lat < 55.5


def test_ohne_argument_liest_gepinnte_datei(kommune, gesamt, bewohnt):
    zeilen = R.raumzeilen(kommune)
    _pruefe(zeilen, gesamt, bewohnt)
    with open(GEOJSON, encoding="utf-8") as fh:
        daten = json.load(fh)
    namen = {f["properties"]["name"] for f in daten["features"]}
    ortsteile = [z for z in zeilen if z.art == "ortsteil"]
    assert ortsteile, "die gepinnte Datei enthält Flächen, also muss es Ortsteilzeilen geben"
    assert {z.name for z in ortsteile} <= namen
    assert all(z.ebene in (9, 10) for z in ortsteile)
    assert len({z.ebene for z in ortsteile}) == 1, "je Gemeinde gilt genau eine Ebene"
    assert all(z.name == R.UEBRIG for z in zeilen if z.art != "ortsteil")
    # Ausdrücklich übergebene Datei ergibt dasselbe
    assert [(z.name, z.jahresbetrag_eur) for z in R.raumzeilen(kommune, daten)] == \
        [(z.name, z.jahresbetrag_eur) for z in zeilen]


def test_ohne_flaeche_eine_zeile(kommune, gesamt, bewohnt):
    zeilen = R.raumzeilen(kommune, {"type": "FeatureCollection", "features": []})
    assert len(zeilen) == 1
    z = zeilen[0]
    assert z.art == "gemeinde" and z.name == kommune.name
    assert z.jahresbetrag_eur == pytest.approx(gesamt.jahresbetrag_eur, abs=1e-6)
    _pruefe(zeilen, gesamt, bewohnt)


def test_zwei_rechtecke_und_leere_flaeche(kommune, gesamt, bewohnt, zwei_rechtecke):
    zeilen = R.raumzeilen(kommune, zwei_rechtecke)
    _pruefe(zeilen, gesamt, bewohnt)
    nach_name = {z.name: z for z in zeilen}
    assert set(nach_name) == {"West", "Südost", "Leer", R.UEBRIG}
    assert nach_name["West"].einwohner > 0 and nach_name["Südost"].einwohner > 0
    assert nach_name[R.UEBRIG].einwohner > 0
    leer = nach_name["Leer"]
    assert leer.einwohner == 0 and leer.jahresbetrag_eur is None and leer.grund


def test_ueberlappung_kleinere_flaeche(kommune, gesamt, bewohnt, raster, zwei_rechtecke):
    """Ein kleines Rechteck im West-Rechteck bekommt dessen Zellen; keine Zelle zählt doppelt."""
    ecken, xs, ys = raster
    x, y = ecken[0]
    klein = _rechteck(x, y, x + 100, y + 100, "Klein")
    daten = {"type": "FeatureCollection", "features": [*zwei_rechtecke["features"], klein]}
    zeilen = R.raumzeilen(kommune, daten)
    _pruefe(zeilen, gesamt, bewohnt)
    nach_name = {z.name: z for z in zeilen}
    zelle = [g for g in bewohnt if R.zellmitte_3035(g) == (x + 50, y + 50)]
    assert nach_name["Klein"].zellkennungen == tuple(zelle)
    owner = [z.name for z in zeilen if zelle[0] in z.zellkennungen]
    assert owner == ["Klein"]


def test_ebene_mit_meisten_einwohnern(kommune, gesamt, bewohnt, raster, zwei_rechtecke):
    """Eine Ebene-9-Fläche über die ganze Gemeinde deckt mehr Einwohner ab als die Ebene 10 → Ebene 9 gilt."""
    _, xs, ys = raster
    gross = _rechteck(xs[0], ys[0], xs[-1] + 100, ys[-1] + 100, "Ganz", ebene=9)
    daten = {"type": "FeatureCollection", "features": [*zwei_rechtecke["features"], gross]}
    zeilen = R.raumzeilen(kommune, daten)
    _pruefe(zeilen, gesamt, bewohnt)
    assert [(z.name, z.ebene) for z in zeilen] == [("Ganz", 9)]


def test_gleichstand_ebene_10(kommune, gesamt, bewohnt, raster):
    """Decken beide Ebenen dieselben Einwohner ab, gilt Ebene 10."""
    _, xs, ys = raster
    box = (xs[0], ys[0], xs[-1] + 100, ys[-1] + 100)
    daten = {"type": "FeatureCollection", "features": [
        _rechteck(*box, "Neun", ebene=9), _rechteck(*box, "Zehn", ebene=10)]}
    zeilen = R.raumzeilen(kommune, daten)
    _pruefe(zeilen, gesamt, bewohnt)
    assert [(z.name, z.ebene) for z in zeilen] == [("Zehn", 10)]


def test_filter_ohne_argument_unveraendert(kommune, gesamt, bewohnt):
    gids, _, _ = B.zellen(kommune.ags)
    mit = B.rechne_95(kommune, gids)
    assert mit.jahresbetrag_eur == pytest.approx(gesamt.jahresbetrag_eur, rel=1e-12)
    assert mit.zellen == gesamt.zellen
