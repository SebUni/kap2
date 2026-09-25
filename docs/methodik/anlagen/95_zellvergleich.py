#!/usr/bin/env python3
"""Zellvergleich #95: Rechenkette (eine Zelle) gegen alle bewohnten 100-m-Zellen einer Kommune.

Anlage zu docs/methodik/95_hitzebelastung.md, Abschnitt 3.0 („eine Zelle statt aller Zellen“).
Aufruf (Beispielkommune Berlin):

    python3 docs/methodik/anlagen/95_zellvergleich.py --gemeinde 11000000

Was das Skript rechnet, Schritt für Schritt, jeder Schritt auf den vorigen:

  Kette  Rechenkette 3.0: eine Temperatur (Punkt der Kommune), Einwohner je Altersband aus Ebene 1.
  (a)    Temperatur je Zelle: jede bewohnte 100-m-Zelle bekommt ihren Wert aus dem 1-km-Raster [33];
         Einwohnersumme und Altersstruktur bleiben die der Kette (Einwohner der Zelle nur als Gewicht).
  (b)    Einwohnersumme: wie (a), aber mit der Einwohnersumme des Zensus-Gitters [67].
  (c)    Altersbänder je Zelle wie im Produkt: Bänder nach zensus_loader.apply_zensus_to_cell_inputs.
  (d)    Feinstruktur unter 1 km: Streuung sigma = 0,5 K um den Rasterwert (wie §4), Gauß-Hermite
         mit 21 Punkten; wirkt nur auf die Mortalität (die Morbidität hängt an den Hitzetagen).

Parameter: Kapitel 7 des Berichts (Zeilen „wert:“), Wochenquantile aus der Tabelle §3.2 wie die
Rechenkette (mit --wochenquantile produkt aus backend/data/kalibrierung/wochenquantile_region.csv
[33,50]), Ebene 1 aus backend/data/kalibrierung/bevoelkerung_bundesland_altersband.csv [48].

Daten (werden geladen und im Cache-Verzeichnis außerhalb des Repos abgelegt, Vorgabe
~/.cache/kap3/95_zellvergleich, änderbar mit --cache oder der Umgebungsvariablen KAP3_CACHE):
  - Zensus-2022-Gitter 100 m [67]: Download-Adressen und Einlese-Logik aus
    backend/app/services/zensus_loader.py (importiert, nicht geändert),
  - DWD-CDC-Raster 1 km [33]: Monatsmittel der Lufttemperatur Juni–August und Jahresraster hot_days,
    je die zehn jüngsten verfügbaren Jahre wie dwd_cdc_grid.climatology_grid / sample_climatology,
  - Gemeindegebiet: BKG VG250, Ebene vg250_gem, GF = 4 (Adresse aus backend/app/config.py).

Das Skript braucht nur die Python-Standardbibliothek. Weil numpy, shapely und pyproj auf den
Prüfrechnern fehlen können, sind die Koordinatenumrechnungen hier nachgebaut (EPSG:3035 LAEA,
EPSG:25832 UTM, EPSG:31467 Gauß-Krüger mit Helmert-Parametern EPSG:1777). Abweichung gegenüber
pyproj: wenige Meter; bei 1-km-Rasterzellen ändert das die Faktoren nicht in der dritten Stelle.
Fehlen die Drittpakete, werden sie beim Import von zensus_loader durch Platzhalter ersetzt; der
Loader ruft sie für das Einlesen nicht auf.
"""
from __future__ import annotations

import argparse
import ast
import csv
import gzip
import importlib
import math
import os
import sqlite3
import struct
import sys
import types
import urllib.error
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
BERICHT = REPO / "docs" / "methodik" / "95_hitzebelastung.md"
KALIB = REPO / "backend" / "data" / "kalibrierung"
BANDS = ("u65", "a65_74", "a75_84", "a85p")
BAND_LABEL = {"u65": "u65", "a65_74": "65–74", "a75_84": "75–84", "a85p": "85+"}
BERICHT_BAND = {"u65": "u65", "65-74": "a65_74", "75-84": "a75_84", "85+": "a85p"}

# Landschlüssel -> Land (amtlich, wie vg250_loader.BUNDESLAND_BY_SNL)
LAND = {
    "01": "Schleswig-Holstein", "02": "Hamburg", "03": "Niedersachsen", "04": "Bremen",
    "05": "Nordrhein-Westfalen", "06": "Hessen", "07": "Rheinland-Pfalz",
    "08": "Baden-Württemberg", "09": "Bayern", "10": "Saarland", "11": "Berlin",
    "12": "Brandenburg", "13": "Mecklenburg-Vorpommern", "14": "Sachsen",
    "15": "Sachsen-Anhalt", "16": "Thüringen",
}
# Gemeinden, die ein ganzes Land sind: Ebene 1 kommt aus der Landeszeile der Fortschreibung.
STADTSTAAT = {"11000000": "Berlin", "02000000": "Hamburg"}
# Punkt der Rechenkette 3.0 (Berlin-Mitte, 52,520 °N, 13,405 °E)
KETTENPUNKT = {"11000000": (52.520, 13.405)}


# ── Zahlen im Stil von KAP3 ──────────────────────────────────────────────────

def de(x: float, stellen: int) -> str:
    s = f"{x:,.{stellen}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def de_int(x: float) -> str:
    return de(round(x), 0)


# ── Parameter aus dem Bericht und aus dem Produkt (nur lesen) ─────────────────

def bericht_parameter() -> dict:
    """Zeilen „id:“ und „wert:“ aus Kapitel 7 des Berichts."""
    text = BERICHT.read_text(encoding="utf-8")
    kap7 = text[text.index("## 7 "):text.index("## 8 ")]
    out: dict = {}
    pid = None
    for zeile in kap7.splitlines():
        z = zeile.split("#")[0].strip()
        if z.startswith("id:"):
            pid = z[3:].strip()
        elif z.startswith("wert:") and pid:
            roh = z[5:].strip()
            if roh.startswith("{"):
                werte = {}
                for teil in roh.strip("{}").split(","):
                    k, v = teil.split(":")
                    werte[k.strip()] = float(v)
                out[pid] = werte
            else:
                try:
                    out[pid] = float(roh)
                except ValueError:
                    out[pid] = roh.strip('"')
            pid = None
    return out


def _literal_aus_datei(pfad: Path, name: str):
    """Wert einer Zuweisung ``name = <Literal>`` bzw. ``name: T = <Literal>`` (ohne Import)."""
    baum = ast.parse(pfad.read_text(encoding="utf-8"))
    for knoten in ast.walk(baum):
        if isinstance(knoten, ast.AnnAssign) and isinstance(knoten.target, ast.Name):
            if knoten.target.id == name and knoten.value is not None:
                return ast.literal_eval(knoten.value)
        if isinstance(knoten, ast.Assign):
            for ziel in knoten.targets:
                if isinstance(ziel, ast.Name) and ziel.id == name:
                    return ast.literal_eval(knoten.value)
    raise KeyError(f"{name} nicht in {pfad}")


def wochenquantile(region: str, herkunft: str = "bericht") -> list[float]:
    """q_w,Region: Tabelle §3.2 des Berichts (wie die Rechenkette 3.0, Ebene 4) oder, mit
    herkunft="produkt", die Anlage wochenquantile_region.csv wie health._load_week_anomalies."""
    if herkunft == "bericht":
        name = {"nord": "Nord", "mitte": "Mitte", "sued": "Süd"}[region]
        kopf = "| \\(q_{w,\\text{" + name + "}}\\) [K] |"
        zeile = next(z for z in BERICHT.read_text(encoding="utf-8").splitlines() if z.startswith(kopf))
        werte = [float(v.strip().replace("−", "-").replace("+", "").replace(",", "."))
                 for v in zeile[len(kopf):].strip(" |").split("|")]
        assert len(werte) == 13
        return werte
    zeilen = {}
    with open(KALIB / "wochenquantile_region.csv", newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            if row["region"] == region:
                zeilen[int(row["w"])] = float(row["q_w_emp"])
    return [zeilen[w] for w in sorted(zeilen)]


# ── Koordinaten (Standardbibliothek; EPSG-Formeln) ────────────────────────────

GRS80 = (6378137.0, 1 / 298.257222101)
BESSEL = (6377397.155, 1 / 299.1528128)


def _e2(ell):
    f = ell[1]
    return f * (2 - f)


class LAEA:
    """EPSG:3035 (ETRS89-LAEA), Guidance Note 7-2, Methode 9820."""

    def __init__(self, lat0=52.0, lon0=10.0, fe=4321000.0, fn=3210000.0, ell=GRS80):
        self.a = ell[0]
        self.e2 = _e2(ell)
        self.e = math.sqrt(self.e2)
        self.lon0 = math.radians(lon0)
        self.fe, self.fn = fe, fn
        p0 = math.radians(lat0)
        self.qp = self._q(math.pi / 2)
        self.b0 = math.asin(self._q(p0) / self.qp)
        self.rq = self.a * math.sqrt(self.qp / 2)
        self.d = self.a * (math.cos(p0) / math.sqrt(1 - self.e2 * math.sin(p0) ** 2)) / (
            self.rq * math.cos(self.b0))

    def _q(self, phi):
        s, e = math.sin(phi), self.e
        return (1 - self.e2) * (s / (1 - self.e2 * s * s)
                                - (1 / (2 * e)) * math.log((1 - e * s) / (1 + e * s)))

    def vor(self, lon, lat):
        phi, lam = math.radians(lat), math.radians(lon) - self.lon0
        beta = math.asin(self._q(phi) / self.qp)
        b = self.rq * math.sqrt(2 / (1 + math.sin(self.b0) * math.sin(beta)
                                     + math.cos(self.b0) * math.cos(beta) * math.cos(lam)))
        x = self.fe + b * self.d * math.cos(beta) * math.sin(lam)
        y = self.fn + (b / self.d) * (math.cos(self.b0) * math.sin(beta)
                                      - math.sin(self.b0) * math.cos(beta) * math.cos(lam))
        return x, y

    def zurueck(self, x, y):
        dx, dy = x - self.fe, y - self.fn
        rho = math.hypot(dx / self.d, self.d * dy)
        c = 2 * math.asin(rho / (2 * self.rq))
        sb0, cb0 = math.sin(self.b0), math.cos(self.b0)
        beta = math.asin(math.cos(c) * sb0 + (self.d * dy * math.sin(c) * cb0) / rho)
        lam = self.lon0 + math.atan2(dx * math.sin(c),
                                     self.d * rho * cb0 * math.cos(c)
                                     - self.d ** 2 * dy * sb0 * math.sin(c))
        e2 = self.e2
        phi = (beta + (e2 / 3 + 31 * e2 ** 2 / 180 + 517 * e2 ** 3 / 5040) * math.sin(2 * beta)
               + (23 * e2 ** 2 / 360 + 251 * e2 ** 3 / 3780) * math.sin(4 * beta)
               + (761 * e2 ** 3 / 45360) * math.sin(6 * beta))
        return math.degrees(lam), math.degrees(phi)


class TM:
    """Transversale Mercatorprojektion (Krüger-Reihen bis n^3)."""

    def __init__(self, lon0, k0, fe, fn, ell):
        a, f = ell
        n = f / (2 - f)
        self.e = math.sqrt(_e2(ell))
        self.lon0, self.k0, self.fe, self.fn = math.radians(lon0), k0, fe, fn
        self.A = a / (1 + n) * (1 + n ** 2 / 4 + n ** 4 / 64)
        self.al = (n / 2 - 2 * n ** 2 / 3 + 5 * n ** 3 / 16, 13 * n ** 2 / 48 - 3 * n ** 3 / 5,
                   61 * n ** 3 / 240)
        self.be = (n / 2 - 2 * n ** 2 / 3 + 37 * n ** 3 / 96, n ** 2 / 48 + n ** 3 / 15,
                   17 * n ** 3 / 480)
        self.de = (2 * n - 2 * n ** 2 / 3 - 2 * n ** 3, 7 * n ** 2 / 3 - 8 * n ** 3 / 5,
                   56 * n ** 3 / 15)

    def vor(self, lon, lat):
        phi, lam = math.radians(lat), math.radians(lon) - self.lon0
        t = math.sinh(math.atanh(math.sin(phi)) - self.e * math.atanh(self.e * math.sin(phi)))
        xi_ = math.atan2(t, math.cos(lam))
        eta_ = math.atanh(math.sin(lam) / math.sqrt(1 + t * t))
        xi = xi_ + sum(a * math.sin(2 * j * xi_) * math.cosh(2 * j * eta_)
                       for j, a in enumerate(self.al, 1))
        eta = eta_ + sum(a * math.cos(2 * j * xi_) * math.sinh(2 * j * eta_)
                         for j, a in enumerate(self.al, 1))
        return self.fe + self.k0 * self.A * eta, self.fn + self.k0 * self.A * xi

    def zurueck(self, x, y):
        xi = (y - self.fn) / (self.k0 * self.A)
        eta = (x - self.fe) / (self.k0 * self.A)
        xi_ = xi - sum(b * math.sin(2 * j * xi) * math.cosh(2 * j * eta)
                       for j, b in enumerate(self.be, 1))
        eta_ = eta - sum(b * math.cos(2 * j * xi) * math.sinh(2 * j * eta)
                         for j, b in enumerate(self.be, 1))
        chi = math.asin(math.sin(xi_) / math.cosh(eta_))
        phi = chi + sum(d * math.sin(2 * j * chi) for j, d in enumerate(self.de, 1))
        lam = self.lon0 + math.atan2(math.sinh(eta_), math.cos(xi_))
        return math.degrees(lam), math.degrees(phi)


def _geo_zu_xyz(lon, lat, ell):
    a, e2 = ell[0], _e2(ell)
    p, l = math.radians(lat), math.radians(lon)
    n = a / math.sqrt(1 - e2 * math.sin(p) ** 2)
    return n * math.cos(p) * math.cos(l), n * math.cos(p) * math.sin(l), n * (1 - e2) * math.sin(p)


def _xyz_zu_geo(x, y, z, ell):
    a, e2 = ell[0], _e2(ell)
    lon = math.atan2(y, x)
    p = math.hypot(x, y)
    lat = math.atan2(z, p * (1 - e2))
    for _ in range(10):
        n = a / math.sqrt(1 - e2 * math.sin(lat) ** 2)
        lat = math.atan2(z + e2 * n * math.sin(lat), p)
    return math.degrees(lon), math.degrees(lat)


# EPSG:1777 „DHDN to WGS 84 (2)“, Position Vector: tx, ty, tz [m], rx, ry, rz [″], ds [ppm]
_HELMERT = (598.1, 73.7, 418.2, 0.202, 0.045, -2.455, 6.7)
_GK3 = TM(9.0, 1.0, 3500000.0, 0.0, BESSEL)


def wgs84_zu_gk3(lon, lat):
    """WGS84 -> DHDN / Gauß-Krüger Zone 3 (EPSG:31467), wie das Raster der DWD-Klimadaten."""
    tx, ty, tz, rx, ry, rz, ds = _HELMERT
    s = 1 + ds * 1e-6
    sek = math.pi / 180 / 3600
    rx, ry, rz = rx * sek, ry * sek, rz * sek
    xw, yw, zw = _geo_zu_xyz(lon, lat, GRS80)
    u, v, w = xw - tx, yw - ty, zw - tz
    # Umkehr von X_wgs = T + s·R·X_dhdn (R orthogonal in erster Ordnung: R^-1 = R^T)
    xd = (u + rz * v - ry * w) / s
    yd = (-rz * u + v + rx * w) / s
    zd = (ry * u - rx * v + w) / s
    lon_d, lat_d = _xyz_zu_geo(xd, yd, zd, BESSEL)
    return _GK3.vor(lon_d, lat_d)


LAEA3035 = LAEA()
UTM32 = TM(9.0, 0.9996, 500000.0, 0.0, GRS80)


# ── Download mit Cache ────────────────────────────────────────────────────────

def lade(url: str, ziel: Path, *, pflicht: bool = True) -> Path | None:
    if ziel.exists() and ziel.stat().st_size > 0:
        return ziel
    ziel.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "kap3-methodik/95-zellvergleich"})
    try:
        with urllib.request.urlopen(req, timeout=600) as resp, open(str(ziel) + ".tmp", "wb") as fh:
            while block := resp.read(1 << 20):
                fh.write(block)
    except urllib.error.HTTPError as exc:
        if exc.code == 404 and not pflicht:
            return None
        raise
    os.replace(str(ziel) + ".tmp", ziel)
    return ziel


# ── Gemeindegebiet aus VG250 (GeoPackage über sqlite3) ────────────────────────

def _wkb_polygone(buf: bytes, pos: int = 0):
    """Liest WKB (Polygon/MultiPolygon, auch mit Z/M) -> Liste von Polygonen (Liste von Ringen)."""
    endian = "<" if buf[pos] == 1 else ">"
    (typ,) = struct.unpack_from(endian + "I", buf, pos + 1)
    pos += 5
    dims = 2
    if typ & 0x80000000 or typ & 0x40000000:  # EWKB-Flags
        dims += (1 if typ & 0x80000000 else 0) + (1 if typ & 0x40000000 else 0)
        typ &= 0xFFFF
    elif typ > 1000:
        dims += {1: 1, 2: 1, 3: 2}[typ // 1000]
        typ %= 1000
    if typ == 3:
        (nringe,) = struct.unpack_from(endian + "I", buf, pos)
        pos += 4
        ringe = []
        for _ in range(nringe):
            (npkt,) = struct.unpack_from(endian + "I", buf, pos)
            pos += 4
            werte = struct.unpack_from(endian + "d" * (npkt * dims), buf, pos)
            pos += 8 * npkt * dims
            ringe.append([(werte[i], werte[i + 1]) for i in range(0, len(werte), dims)])
        return [ringe], pos
    if typ == 6:
        (nteile,) = struct.unpack_from(endian + "I", buf, pos)
        pos += 4
        polys = []
        for _ in range(nteile):
            teil, pos = _wkb_polygone(buf, pos)
            polys.extend(teil)
        return polys, pos
    raise ValueError(f"WKB-Typ {typ} nicht unterstützt")


def gemeindegebiet(ags: str, cache: Path, vg250_url: str):
    """Polygone (EPSG:25832) der Gemeinde mit GF = 4 aus VG250, dazu Name und Stand."""
    zip_pfad = lade(vg250_url, cache / "vg250" / "vg250.zip")
    gpkg = cache / "vg250" / "DE_VG250.gpkg"
    if not gpkg.exists():
        with zipfile.ZipFile(zip_pfad) as z:
            inner = next(n for n in z.namelist() if n.endswith("DE_VG250.gpkg"))
            with z.open(inner) as src, open(str(gpkg) + ".tmp", "wb") as dst:
                while block := src.read(1 << 20):
                    dst.write(block)
        os.replace(str(gpkg) + ".tmp", gpkg)
    with zipfile.ZipFile(zip_pfad) as z:
        stand = next((n.split("/")[0] for n in z.namelist() if n.endswith("DE_VG250.gpkg")), "?")
    con = sqlite3.connect(f"file:{gpkg}?mode=ro", uri=True)
    try:
        (spalte,) = con.execute(
            "SELECT column_name FROM gpkg_geometry_columns WHERE table_name = 'vg250_gem'").fetchone()
        zeilen = con.execute(
            f'SELECT GEN, BEZ, "{spalte}" FROM vg250_gem WHERE AGS = ? AND GF = 4', (ags,)).fetchall()
    finally:
        con.close()
    if not zeilen:
        raise SystemExit(f"Gemeinde {ags} nicht in VG250 (vg250_gem, GF = 4) gefunden")
    polys = []
    for _, _, blob in zeilen:
        flags = blob[3]
        env = {0: 0, 1: 32, 2: 48, 3: 48, 4: 64}[(flags >> 1) & 7]
        teil, _ = _wkb_polygone(blob, 8 + env)
        polys.extend(teil)
    return polys, f"{zeilen[0][1]} {zeilen[0][0]}", stand


def flaeche_km2(polys) -> float:
    def ring(r):
        return 0.5 * abs(sum(x1 * y2 - x2 * y1 for (x1, y1), (x2, y2) in zip(r, r[1:] + r[:1])))
    return sum(ring(p[0]) - sum(ring(h) for h in p[1:]) for p in polys) / 1e6


class Innen:
    """Punkt-in-Polygon (gerade/ungerade Regel) mit Kanten, nach 1-km-Streifen einsortiert."""

    def __init__(self, ringe, streifen=1000.0):
        self.s = streifen
        self.kanten: dict[int, list] = {}
        xs, ys = [], []
        for r in ringe:
            for (x1, y1), (x2, y2) in zip(r, r[1:] + r[:1]):
                if y1 == y2:
                    continue
                for k in range(int(min(y1, y2) // streifen), int(max(y1, y2) // streifen) + 1):
                    self.kanten.setdefault(k, []).append((x1, y1, x2, y2))
            xs += [p[0] for p in r]
            ys += [p[1] for p in r]
        self.bbox = (min(xs), min(ys), max(xs), max(ys))

    def __call__(self, px, py) -> bool:
        innen = False
        for x1, y1, x2, y2 in self.kanten.get(int(py // self.s), ()):
            if (y1 > py) != (y2 > py) and px < x1 + (py - y1) * (x2 - x1) / (y2 - y1):
                innen = not innen
        return innen


# ── Zensus-Gitter über das Produktmodul zensus_loader ────────────────────────

def zensus_loader_laden(cache: Path):
    sys.path.insert(0, str(REPO / "backend"))

    def platzhalter(*_a, **_k):
        raise RuntimeError("Drittpaket fehlt; wird für das Einlesen nicht gebraucht")

    for name in ("shapely", "shapely.geometry", "shapely.ops", "pyproj"):
        try:
            importlib.import_module(name)
        except ImportError:
            mod = types.ModuleType(name)
            mod.__path__ = []
            for attr in ("box", "transform", "CRS", "Transformer"):
                setattr(mod, attr, platzhalter)
            sys.modules[name] = mod
    # Eigene Einstellungen statt app.config: Cache außerhalb des Repos, sonst wie im Produkt.
    cfg = types.ModuleType("app.config")
    cfg.settings = types.SimpleNamespace(
        ZENSUS_DATA_DIR=str(cache / "zensus"), ZENSUS_AUTO_DOWNLOAD=True,
        ZENSUS_FORCE_REFRESH=False, ZENSUS_DOWNLOAD_TIMEOUT_S=600, ZENSUS_SRID=3035,
        ZENSUS_USER_AGENT="kap2-climate-planner/1.0 (zensus-autoload)")
    import app  # noqa: F401  (Paket backend/app)
    sys.modules["app.config"] = cfg
    return importlib.import_module("app.services.zensus_loader")


# ── DWD-CDC-Raster wie dwd_cdc_grid (ohne numpy) ──────────────────────────────

_MONAT = {6: "06_Jun", 7: "07_Jul", 8: "08_Aug"}


class DwdRaster:
    def __init__(self, cache: Path, monats_basis: str, jahres_basis: str, bis_jahr: int, n: int):
        self.cache, self.mb, self.jb, self.bis, self.n = cache / "dwd_cdc", monats_basis, jahres_basis, bis_jahr, n
        self.jahre_benutzt: dict[str, list[int]] = {}

    def _url(self, param, jahr):
        if param.startswith("air_temp_mean_"):
            m = int(param[-2:])
            return (f"{self.mb.rstrip('/')}/air_temperature_mean/{_MONAT[m]}/"
                    f"grids_germany_monthly_air_temp_mean_{jahr}{m:02d}.asc.gz")
        return f"{self.jb.rstrip('/')}/{param}/grids_germany_annual_{param}_{jahr}_17.asc.gz"

    def _jahresraster(self, param):
        """Die n jüngsten verfügbaren Jahre ab bis_jahr rückwärts (höchstens n + 5 Versuche)."""
        gefunden = []
        jahr, versuche = self.bis, 0
        while len(gefunden) < self.n and versuche < self.n + 5 and jahr > 1950:
            pfad = lade(self._url(param, jahr), self.cache / f"{param}_{jahr}.asc.gz", pflicht=False)
            if pfad is not None:
                gefunden.append((jahr, pfad))
            jahr -= 1
            versuche += 1
        self.jahre_benutzt[param] = sorted(j for j, _ in gefunden)
        return gefunden

    @staticmethod
    def _werte(pfad: Path, zellen: set):
        with gzip.open(pfad, "rt", encoding="latin-1") as fh:
            kopf = {}
            for _ in range(6):
                k, v = fh.readline().split()
                kopf[k.upper()] = float(v)
            zeilen_noetig = {r for r, _ in zellen}
            werte = {}
            for r in range(int(kopf["NROWS"])):
                zeile = fh.readline()
                if r in zeilen_noetig:
                    teile = zeile.split()
                    for rr, c in zellen:
                        if rr == r:
                            v = float(teile[c])
                            werte[(r, c)] = None if v == kopf["NODATA_VALUE"] else v
        return kopf, werte

    def _kopf(self, param):
        _, pfad = self._jahresraster(param)[0]
        with gzip.open(pfad, "rt", encoding="latin-1") as fh:
            return {k.upper(): float(v) for k, v in (fh.readline().split() for _ in range(6))}

    @staticmethod
    def _index(kopf, x, y):
        col = int((x - kopf["XLLCORNER"]) / kopf["CELLSIZE"])
        row = int(kopf["NROWS"]) - 1 - int((y - kopf["YLLCORNER"]) / kopf["CELLSIZE"])
        if 0 <= row < int(kopf["NROWS"]) and 0 <= col < int(kopf["NCOLS"]):
            return row, col
        return None

    def klimatologie(self, params, punkte_gk3):
        """Mittel über alle Raster (Monate × Jahre) je Punkt wie climatology_grid + sample_grid_points."""
        kopf = self._kopf(params[0])
        idx = [self._index(kopf, x, y) for x, y in punkte_gk3]
        zellen = {i for i in idx if i is not None}
        summe = {z: 0.0 for z in zellen}
        anzahl = {z: 0 for z in zellen}
        for p in params:
            skala = 0.1 if p.startswith("air_temp") else 1.0  # Monatsraster in 1/10 °C
            for _, pfad in self._jahresraster(p):
                _, werte = self._werte(pfad, zellen)
                for z, v in werte.items():
                    if v is not None:
                        summe[z] += v * skala
                        anzahl[z] += 1
        return [None if i is None or anzahl[i] == 0 else summe[i] / anzahl[i] for i in idx]

    def am_punkt(self, param, x, y):
        """sample_climatology: Mittel der Jahre am Punkt, auf 0,1 gerundet."""
        return self.klimatologie([param], [(x, y)])[0]


# ── Modell §3.3–§3.5 ──────────────────────────────────────────────────────────

def gauss_hermite(n: int):
    """Stützstellen und Gewichte (Gewichtsfunktion e^{-x^2}), Newton-Verfahren."""
    x, w = [0.0] * n, [0.0] * n
    pim4 = math.pi ** -0.25
    z = 0.0
    for i in range((n + 1) // 2):
        if i == 0:
            z = math.sqrt(2 * n + 1) - 1.85575 * (2 * n + 1) ** -0.16667
        elif i == 1:
            z -= 1.14 * n ** 0.426 / z
        elif i == 2:
            z = 1.86 * z - 0.86 * x[0]
        elif i == 3:
            z = 1.91 * z - 0.91 * x[1]
        else:
            z = 2.0 * z - x[i - 2]
        for _ in range(200):
            p1, p2 = pim4, 0.0
            for j in range(1, n + 1):
                p3, p2 = p2, p1
                p1 = z * math.sqrt(2.0 / j) * p2 - math.sqrt((j - 1) / j) * p3
            pp = math.sqrt(2.0 * n) * p2
            z1, z = z, z - p1 / pp
            if abs(z - z1) < 1e-14:
                break
        x[i], x[n - 1 - i] = z, -z
        w[i] = w[n - 1 - i] = 2.0 / (pp * pp)
    assert abs(sum(w) - math.sqrt(math.pi)) < 1e-10
    return x, w


class Modell:
    def __init__(self, par: dict, region: str, herkunft_q: str = "bericht"):
        self.q = wochenquantile(region, herkunft_q)
        self.t0 = par["heat.t0_region"][region]
        b85 = par["heat.beta_85plus_region"][region]
        g = lambda pid: {BERICHT_BAND[k]: v for k, v in par[pid].items()}  # noqa: E731
        f = g("heat.f_alter")
        self.beta = {b: b85 * f[b] for b in BANDS}
        self.m, self.L, self.r0 = g("heat.m_basissterberate"), g("heat.l_restlebenserwartung"), g("heat.r0_einweisungsrate")
        self.c_kal, self.voly, self.c_fall = par["heat.c_kal"], par["heat.voly"], par["heat.c_fall"]
        self.e_hd, self.hd_ref = par["heat.e_hd"], par["heat.hd_ref"]
        self._memo: dict = {}

    def _exzess(self, band, t):
        return sum(math.exp(self.beta[band] * max(0.0, t + qw - self.t0)) - 1 for qw in self.q)

    def yll_je_person(self, band, t, sigma=0.0, gh=None):
        """YLL je Einwohner des Bands bei Sommermittel t (v_vers = 1, Rechenkette Ebene 6)."""
        key = (band, t, sigma)
        if key not in self._memo:
            if sigma > 0:
                xs, ws = gh
                ex = sum(w * self._exzess(band, t + math.sqrt(2) * sigma * x)
                         for x, w in zip(xs, ws)) / math.sqrt(math.pi)
            else:
                ex = self._exzess(band, t)
            self._memo[key] = self.c_kal * self.m[band] / 100_000 / 52 * ex * self.L[band]
        return self._memo[key]

    def euro(self, zellen, sigma=0.0, gh=None):
        """Summe € (Preisstand 2024) über Zellen (pop je Band, T, HD): YLL × VOLY + F × c_Fall."""
        mort = morb = 0.0
        for pop, t, hd in zellen:
            faktor = max(0.0, 1 + self.e_hd * (hd - self.hd_ref))
            for b in BANDS:
                if pop[b] > 0:
                    mort += pop[b] * self.yll_je_person(b, t, sigma, gh)
                    morb += pop[b] * self.r0[b] / 100_000 * faktor
        return mort * self.voly + morb * self.c_fall


# ── Hauptprogramm ─────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--gemeinde", required=True, help="Amtlicher Gemeindeschlüssel (8 Stellen)")
    ap.add_argument("--punkt", help="Punkt der Rechenkette als BREITE,LÄNGE (Vorgabe: Berlin-Mitte "
                                   "für 11000000, sonst Schwerpunkt des Gemeindegebiets)")
    ap.add_argument("--einwohner", help="Ebene 1 als u65,65-74,75-84,85+ (Vorgabe: Landeszeile der "
                                       "Fortschreibung bei Stadtstaaten, sonst Gitter-Summe × "
                                       "Altersstruktur des Landes)")
    ap.add_argument("--sigma", type=float, default=0.5, help="Feinstruktur unter 1 km in K (§4)")
    ap.add_argument("--wochenquantile", choices=("bericht", "produkt"), default="bericht",
                    help="q_w aus Tabelle §3.2 (wie Rechenkette 3.0) oder aus wochenquantile_region.csv "
                         "(wie das Produkt); die Faktoren ändern sich dadurch erst in der fünften Stelle")
    ap.add_argument("--bis-jahr", type=int, default=datetime.now(timezone.utc).year - 1,
                    help="jüngstes DWD-Jahr (Vorgabe wie Produkt: Vorjahr)")
    ap.add_argument("--cache", default=os.environ.get("KAP3_CACHE",
                                                      str(Path.home() / ".cache" / "kap3" / "95_zellvergleich")))
    args = ap.parse_args()

    ags = args.gemeinde.strip()
    cache = Path(args.cache).expanduser()
    land = LAND[ags[:2]]
    region = _literal_aus_datei(REPO / "backend/app/services/engine/impact/health.py",
                                "REGION_BY_BUNDESLAND").get(land, "mitte")
    config = REPO / "backend" / "app" / "config.py"
    vg250_url = _literal_aus_datei(config, "VG250_GPKG_URL")
    dwd = DwdRaster(cache, _literal_aus_datei(config, "DWD_CDC_MONTHLY_BASE"),
                    _literal_aus_datei(config, "DWD_CDC_GRID_BASE"), args.bis_jahr,
                    _literal_aus_datei(config, "DWD_CDC_CLIMATOLOGY_YEARS"))
    modell = Modell(bericht_parameter(), region, args.wochenquantile)

    # Gemeindegebiet: VG250 (EPSG:25832) -> EPSG:3035, dort Punkt-in-Polygon mit den Zellmitten
    polys, name, stand = gemeindegebiet(ags, cache, vg250_url)
    ringe3035 = [[LAEA3035.vor(*UTM32.zurueck(x, y)) for x, y in r] for p in polys for r in p]
    innen = Innen(ringe3035)
    xmin, ymin, xmax, ymax = innen.bbox
    bbox = (int(xmin) - 150, int(ymin) - 150, int(xmax) + 150, int(ymax) + 150)

    zl = zensus_loader_laden(cache)
    zensus = {k: zl.load_dataset_bbox(k, bbox) for k in ("population", "share_over_65", "age_groups")}
    gids = [gid for gid, r in zensus["population"].items()
            if (r.get("Einwohner") or 0) > 0 and innen(r["x"], r["y"])]
    gids.sort()
    grid_cells = [{"gitter_id": g} for g in gids]
    cell_inputs = [{} for _ in gids]
    zl.apply_zensus_to_cell_inputs(cell_inputs, grid_cells, zensus)

    # Temperatur und Hitzetage je Zelle (Zellmitte -> WGS84 -> GK3)
    geo = [LAEA3035.zurueck(zensus["population"][g]["x"], zensus["population"][g]["y"]) for g in gids]
    gk3 = [wgs84_zu_gk3(lon, lat) for lon, lat in geo]
    t_zelle = dwd.klimatologie([f"air_temp_mean_{m:02d}" for m in (6, 7, 8)], gk3)
    hd_zelle = dwd.klimatologie(["hot_days"], gk3)

    # Punkt der Rechenkette: wie summer_mean_temp_at / hot_days_at (Rundung wie im Produkt)
    if args.punkt:
        lat_p, lon_p = (float(v) for v in args.punkt.split(","))
        punkt_herkunft = "Vorgabe --punkt"
    elif ags in KETTENPUNKT:
        lat_p, lon_p = KETTENPUNKT[ags]
        punkt_herkunft = "Rechenkette 3.0"
    else:
        gross = max(ringe3035, key=lambda r: flaeche_km2([[r]]))  # größte Teilfläche
        lon_p, lat_p = LAEA3035.zurueck(sum(x for x, _ in gross) / len(gross),
                                        sum(y for _, y in gross) / len(gross))
        punkt_herkunft = "Mittel der Außengrenze (Näherung, --punkt setzen)"
    px, py = wgs84_zu_gk3(lon_p, lat_p)
    monate = [round(dwd.am_punkt(f"air_temp_mean_{m:02d}", px, py), 1) for m in (6, 7, 8)]
    t_punkt = round(sum(monate) / 3, 2)
    hd_punkt = round(dwd.am_punkt("hot_days", px, py), 1)

    # Ebene 1
    with open(KALIB / "bevoelkerung_bundesland_altersband.csv", newline="", encoding="utf-8") as fh:
        landzeile = {r["bundesland"]: {b: float(r[b]) for b in BANDS} for r in csv.DictReader(fh)}[land]
    ew = [float(ci["pop"]) for ci in cell_inputs]
    sum_ew = sum(ew)
    if args.einwohner:
        ebene1 = dict(zip(BANDS, (float(v) for v in args.einwohner.split(","))))
        e1_herkunft = "Vorgabe --einwohner"
    elif ags in STADTSTAAT:
        ebene1 = landzeile
        e1_herkunft = f"Fortschreibung 31.12.2023, Zeile {land}"
    else:
        s = sum(landzeile.values())
        ebene1 = {b: sum_ew * landzeile[b] / s for b in BANDS}
        e1_herkunft = f"Gitter-Summe × Altersstruktur {land} (Wirkung (b) ist dann 1)"
    sum_e1 = sum(ebene1.values())

    fehlend = sum(1 for t in t_zelle if t is None) + sum(1 for h in hd_zelle if h is None)
    t_z = [t if t is not None else t_punkt for t in t_zelle]
    hd_z = [h if h is not None else hd_punkt for h in hd_zelle]
    gh = gauss_hermite(21)

    # Schritte
    eur_kette = modell.euro([(ebene1, t_punkt, hd_punkt)])
    anteil = [e / sum_ew for e in ew]
    zell_a = [({b: ebene1[b] * a for b in BANDS}, t, h) for a, t, h in zip(anteil, t_z, hd_z)]
    zell_b = [({b: ebene1[b] * e / sum_e1 for b in BANDS}, t, h) for e, t, h in zip(ew, t_z, hd_z)]
    baender = [{b: float(ci["pop_age_bands"][b]) for b in BANDS} for ci in cell_inputs]
    zell_c = [(bd, t, h) for bd, t, h in zip(baender, t_z, hd_z)]
    eur = {"kette": eur_kette, "a": modell.euro(zell_a), "b": modell.euro(zell_b),
           "c": modell.euro(zell_c), "d": modell.euro(zell_c, args.sigma, gh)}

    # Eigenheit des Produkts (Befund 104): Zellen ohne Anteil 65+ -> 65+ = 0; Ersatz mit dem Anteil der übrigen Zellen
    ohne = [i for i, ci in enumerate(cell_inputs) if not ci.get("share_over_65")]
    mit = [i for i in range(len(gids)) if i not in set(ohne)]
    anteil65 = sum(cell_inputs[i]["pop_over_65"] for i in mit) / sum(ew[i] for i in mit)
    ersatz = []
    area_split = zl._area_senior_split(zensus["age_groups"])
    ohne_set = set(ohne)
    for i, (bd, t, h) in enumerate(zell_c):
        if i in ohne_set:
            p65 = ew[i] * anteil65
            counts = zl._senior_band_counts(zensus["age_groups"].get(gids[i], {}))
            split = zl._senior_split(counts, area_split) if counts else dict(area_split)
            bd = {"u65": ew[i] - p65, **{b: p65 * split[b] for b in BANDS[1:]}}
        ersatz.append((bd, t, h))
    eur_ersatz = modell.euro(ersatz)

    # Ausgabe
    def mio(v):  # kap3-stil: ab einer Million in Mio. €, darunter ausgeschrieben
        return de(v / 1e6, 2) + " Mio. €" if v >= 1e6 else de_int(v) + " €"
    t_mittel = sum(e * t for e, t in zip(ew, t_z)) / sum_ew
    waermer = sum(e for e, t in zip(ew, t_z) if t > t_punkt) / sum_ew
    bandsumme = {b: sum(bd[b] for bd in baender) for b in BANDS}
    print(f"Zellvergleich #95 — Gemeinde {ags} {name} (Land {land}, ERF-Region {region})")
    print(f"Gemeindegebiet: VG250 {stand}, vg250_gem GF = 4, {de(flaeche_km2(polys), 1)} km²")
    print(f"Zensus-Gitter 100 m: {de_int(len(gids))} bewohnte Zellen, {de_int(sum_ew)} Einwohner")
    print(f"DWD-Jahre: Temperatur {dwd.jahre_benutzt['air_temp_mean_06'][0]}–"
          f"{dwd.jahre_benutzt['air_temp_mean_06'][-1]}, hot_days {dwd.jahre_benutzt['hot_days'][0]}–"
          f"{dwd.jahre_benutzt['hot_days'][-1]}; Zellen ohne Rasterwert: {fehlend}")
    print(f"Punkt der Kette ({punkt_herkunft}, {de(lat_p, 3)} °N, {de(lon_p, 3)} °E): "
          f"{de(t_punkt, 2)} °C, {de(hd_punkt, 1)} Hitzetage")
    print(f"Zellen: Bevölkerungsmittel {de(t_mittel, 2)} °C ({de(min(t_z), 2)}–{de(max(t_z), 2)} °C), "
          f"wärmer als der Punkt: {de(100 * waermer, 1)} % der Einwohner")
    print(f"Ebene 1 ({e1_herkunft}): " + " · ".join(de_int(ebene1[b]) for b in BANDS)
          + f" = {de_int(sum_e1)}")
    print("Bänder nach Produktlogik: " + " · ".join(de_int(bandsumme[b]) for b in BANDS)
          + " = " + de_int(sum(bandsumme.values())) + "; gegen Ebene 1 × "
          + " · ".join(de(bandsumme[b] / ebene1[b], 3) for b in BANDS))
    print()
    print(f"Wochenquantile: {'Tabelle §3.2' if args.wochenquantile == 'bericht' else 'wochenquantile_region.csv'}")
    print(f"Kette (ein Punkt, Ebene 1): {mio(eur['kette'])} je Jahr (Preisstand 2024)")
    schritte = [("a", "(a) Temperatur je Zelle", "kette"), ("b", "(b) Einwohnersumme", "a"),
                ("c", "(c) Altersbänder je Zelle wie im Produkt", "b"),
                ("d", f"(d) Feinstruktur σ = {de(args.sigma, 1)} K", "c")]
    for k, text, vor in schritte:
        print(f"{text}: {mio(eur[k])} × {de(eur[k] / eur[vor], 3)}  (genau {de(eur[k] / eur[vor], 5)})")
    print(f"zusammen: × {de(eur['d'] / eur['kette'], 3)}  (genau {de(eur['d'] / eur['kette'], 5)})")
    print(f"(a) und (d) zusammen (Temperatur, Befund 101): × {de(eur['a'] / eur['kette'] * eur['d'] / eur['c'], 3)}")
    print()
    print(f"Eigenheit in (c), Befund 104: {de_int(len(ohne))} Zellen mit {de_int(sum(ew[i] for i in ohne))} "
          f"Einwohnern ohne Anteil 65+ (65+ = 0 gesetzt)")
    print(f"  Ersatz mit dem Anteil 65+ der übrigen Zellen ({de(100 * anteil65, 2)} %): {mio(eur_ersatz)}; "
          f"Produkt gegen Ersatz × {de(eur['c'] / eur_ersatz, 4)}, Rest (Ersatz gegen (b)) × "
          f"{de(eur_ersatz / eur['b'], 4)}")
    print(f"  Zelllauf ohne Eigenheit (Ersatz, dazu (d)): {mio(eur_ersatz * eur['d'] / eur['c'])}")
    with open(KALIB / "sommermittel_bundesland_povw.csv", newline="", encoding="utf-8") as fh:
        reihe = [float(r["t_sommer_povw"]) for r in csv.DictReader(fh)
                 if r["bundesland"] == land and args.bis_jahr - 9 <= int(r["jahr"]) <= args.bis_jahr]
    if reihe:
        print(f"Reihe {land} in sommermittel_bundesland_povw.csv [50], {args.bis_jahr - 9}–{args.bis_jahr}: "
              f"Mittel {de(sum(reihe) / len(reihe), 2)} °C ({len(reihe)} Sommer)")


if __name__ == "__main__":
    main()
