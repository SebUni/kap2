#!/usr/bin/env python3
"""
Stichprobe #60: Wohnfläche W_z je 100-m-Zensuszelle für die acht Anker-Kommunen.

Modellkontext (docs/methodik/60_gebaeudeschaeden_flusshochwasser.md, §3.2)
--------------------------------------------------------------------------
Datenebene GEBAEUDEWERT, Teil Wohnfläche:  W_z = Summe der Wohnfläche der
Gitterzelle z aus dem Zensus-2022-Gitter (100 m, offener Download ohne Schlüssel).
Datenpaket für den Stichprobenlauf der Kernformel (Vorhaben T-0284); es schließt
keinen Befund. Bericht, Ledger und Evidenz-Register werden nur gelesen.

Ausgabe
-------
  docs/evidenz/60_stichprobe/zensus_wohnflaeche.csv   (UTF-8, Trennzeichen ';')
  kommune;ags;land;gitter_id;wohnflaeche_m2;herkunft;quelle_url;zugriff

Datenquellen (alle ohne Schlüssel)
----------------------------------
Zensus 2022, 100-m-Gitter (Statistisches Bundesamt, Gitterzellen-Seite
https://www.zensus2022.de/DE/Ergebnisse-des-Zensus/gitterzellen.html):
  [Z1] Wohnungen nach Gebäudetyp und Größe — Spalte ``Insgesamt_Wohnungen``
       https://www.destatis.de/static/DE/zensus/gitterdaten/Wohnungen_nach_Gebaeudetyp_Groesse.zip
       (CSV im ZIP: Zensus2022_Wohnung_Gebaeudetyp_Groesse_100m-Gitter.csv)
  [Z2] Durchschnittliche Fläche je Wohnung — Spalte ``durchschnFlaechejeWohn`` (m²)
       https://www.destatis.de/static/DE/zensus/gitterdaten/Durchschnittliche_Flaeche_je_Wohnung_in_Gitterzellen.zip
       (CSV im ZIP: Zensus2022_Durchschn_Flaeche_je_Wohnung_100m-Gitter.csv)
Verwaltungsgrenzen: BKG, VG250 (Ebenen, Stichtag 01.01.), jüngster angebotener
Stand = Jahrgang 2026 (Stichtag 01.01.2026, bereitgestellt 21.07.2026), GeoPackage
in ETRS89/UTM32N (EPSG:25832):
  https://daten.gdz.bkg.bund.de/produkte/vg/vg250_ebenen_0101/2026/vg250_01-01.utm32s.gpkg.ebenen.zip
  Ebene vg250_gem (Gemeinden), nur GF = 4 (Landflächen mit Struktur);
  Ebene vg250_lan (Länder), nur GF = 4 — nur für die Ersatzregel „Land“.
  Lizenz: © GeoBasis-DE / BKG (2026), dl-de/by-2-0.

Ableitung der Wohnfläche (Vorgabe P1)
-------------------------------------
1. Vorrangmerkmal (Ticketvorgabe 4): Das Zensus-Gitter enthält ein Merkmal, das die
   gesamte Wohnfläche einer Zelle ergibt, nämlich
       W_z = Insgesamt_Wohnungen_z [Z1] × durchschnFlaechejeWohn_z [Z2]   (m²).
   Die mittlere Fläche je Wohnung bezieht sich auf alle Wohnungen der Zelle
   (bewohnt und leerstehend); W_z ist damit die gesamte Wohnfläche des
   Wohnungsbestands, nicht nur die bewohnte Fläche. Der Rückfall
   „Einwohner × Wohnfläche je Bewohner“ wird deshalb nicht benötigt.
   Modellgrenzen: Wohnungen in Nichtwohngebäuden ohne Wohnraum und gewerbliche
   Flächen sind nicht enthalten (Untergrenze des Gebäudewerts, vgl. 60-R24-01 (b));
   beide Zensuswerte sind von Destatis stochastisch überlagert (Geheimhaltung),
   das Produkt zweier überlagerter Werte streut in kleinen Zellen entsprechend.
   Das Kennzeichen KLAMMERN (eingeschränkte Aussagekraft; in [Z2] bundesweit nur
   3 Zellen) wird wie in backend/app/services/zensus_loader.py nicht als fehlend
   gewertet: der Wert gilt als veröffentlicht und wird verwendet.
2. Gebäudebestand: Eine Zelle ist besetzt, wenn Insgesamt_Wohnungen > 0. Zellen,
   die in [Z1] fehlen oder dort „–“ (Destatis: genau Null, wie zensus_loader.py)
   bzw. 0 tragen, haben keinen Wohnungsbestand und fallen weg.
   Befund Datenstand (Abruf 2026-09-17): In [Z1] ist Insgesamt_Wohnungen bundesweit
   nie „–“ und nie kleiner als 3 (kleinster veröffentlichter Wert 3, wie bei den
   Altersgruppen in zensus_loader.py). Zellen mit 1–2 Wohnungen erscheinen damit
   nicht als eigene Zeile und fehlen im Ergebnis — die Kommunensumme ist insoweit
   eine Untergrenze (Streulagen).
   Ersatzfälle im Lauf vom 2026-09-17: 342 von 18 638 Zellen (1,8 %); alle 342
   fehlen in [Z2] vollständig (keine Zeile, also geheim gehalten), kein Fall mit
   „–“ oder leerem Wert; fallback_land kam nicht vor.
3. Ersatzregel (§3.2), wenn die Zelle besetzt ist, aber die Fläche je Wohnung fehlt
   (Zelle nicht in [Z2], oder Wert „–“, „…“, leer bzw. geheim gehalten — „–“ ist
   bei einer Durchschnittsfläche in einer besetzten Zelle inhaltlich nicht Null
   und wird deshalb als fehlend behandelt):
     a) herkunft = fallback_kommune:
          W_z = Insgesamt_Wohnungen_z × Ā_Kommune,
          Ā_Kommune = Σ(Wohnungen × Fläche je Wohnung) / Σ Wohnungen über die Zellen
          derselben Kommune mit vollständigem Zensuswert (wohnungsgewichtet,
          ergibt die amtliche mittlere Fläche je Wohnung der Kommune im Gitter).
     b) herkunft = fallback_land, nur wenn die Kommune keine vollständige Zelle hat:
          Ā_Land analog über alle vollständigen Zellen im Begrenzungsrechteck der
          acht Kommunen, deren Mittelpunkt in der Landesfläche (vg250_lan) liegt.
          Modellgrenze: Landeswert aus dem Rechteck, nicht aus dem ganzen Land
          (Ressourcen-Regel §3.4); wird nur bei Bedarf in einem zweiten Lesedurchgang
          berechnet.
4. Zellkennung wie backend/app/services/zensus_loader.py, _gitter_id_from_row:
   'CRS3035RES100mN<y0>E<x0>' mit x0 = x_mp_100m − 50, y0 = y_mp_100m − 50.

Zuschnitt (Ticketvorgabe 2)
---------------------------
Eine Zelle gehört zur Kommune, wenn ihr Mittelpunkt (x0+50, y0+50 in EPSG:3035)
in der Gemeindefläche aus VG250 liegt.

Umsetzung ohne shapely/pyproj (Entscheidung des Supervisors zur Rückfrage T-0297,
Option b: in der Ausführungsumgebung waren die Pakete nicht installierbar). Die
Funktionalität ist hier selbst implementiert und im Skript gegen Referenzwerte
geprüft (``_selbsttest``):
  * GeoPackage lesen: sqlite3 (Standardbibliothek); Geometrie-Blob = GPKG-Kopf
    ('GP', Version, Flags, SRS-ID, Hüllrechteck nach Flag-Bits 1–3) + WKB
    (Polygon/MultiPolygon, auch ISO-Z-Varianten), selbst dekodiert mit struct.
  * EPSG:25832 → geographisch (ETRS89/GRS80): inverse transversale Mercator-
    Abbildung nach Krüger (n-Reihe 3. Ordnung, Genauigkeit < 1 mm innerhalb von
    ±6° um den Mittelmeridian; Karney 2011, J. Geodesy 85, 475–485, Gl. 11–19;
    k0 = 0,9996, λ0 = 9° O, FE = 500 000 m).
  * geographisch → EPSG:3035 (ETRS89-LAEA): ellipsoidische flächentreue
    Azimutalprojektion nach IOGP Guidance Note 7-2, Methode EPSG 9820
    (φ0 = 52° N, λ0 = 10° O, FE = 4 321 000 m, FN = 3 210 000 m).
    Selbsttest gegen das IOGP-Rechenbeispiel (50° N, 5° O → E 3 962 799,45 m,
    N 2 999 718,85 m) und Hin-/Rück-Probe der UTM-Formeln.
    ETRS89 ist für beide Systeme dasselbe Datum (GRS80) — keine Datumsverschiebung.
  * Punkt-in-Polygon: Strahlverfahren mit Gerade-Ungerade-Regel über alle Ringe
    (äußere Ringe und Löcher, alle Teilflächen einer Gemeinde); Kanten werden in
    500-m-Bänder nach y vorsortiert, damit je Punkt nur die Kanten seines Bandes
    geprüft werden. Mittelpunkte liegen auf 50-m-Rastern, ein Treffer exakt auf
    einer Kante ist praktisch ausgeschlossen.

Ressourcen-Regel §3.4 (Ticketvorgabe 5)
---------------------------------------
Kein nationaler Vollraster-Lauf: Die bundesweiten Zensus-CSVs werden zeilenweise
gelesen; behalten werden nur Zeilen, deren Mittelpunkt im Begrenzungsrechteck
(EPSG:3035) einer der acht Kommunen und damit im Gesamtrechteck liegt.
Verschnitten wird nur dort.

Rohdaten
--------
ZIP, CSV und VG250 liegen in backend/.cache/60_stichprobe/ (gitignored). Ein
vorhandener Download wird wiederverwendet; zugriff = Datum des Downloads der
Zensus-Dateien (Dateizeitstempel, JJJJ-MM-TT; bei zwei Dateien das spätere),
quelle_url = direkte Download-Adressen [Z1] und [Z2], getrennt durch „ | “.

Aufruf
------
  python3 backend/scripts/kalibrierung/stichprobe60_zensus.py
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import math
import os
import sqlite3
import struct
import sys
import urllib.request
import zipfile

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
CACHE = os.path.join(REPO, "backend", ".cache", "60_stichprobe")
OUT = os.path.join(REPO, "docs", "evidenz", "60_stichprobe", "zensus_wohnflaeche.csv")

URL_WOHNUNGEN = "https://www.destatis.de/static/DE/zensus/gitterdaten/Wohnungen_nach_Gebaeudetyp_Groesse.zip"
URL_FLAECHE = "https://www.destatis.de/static/DE/zensus/gitterdaten/Durchschnittliche_Flaeche_je_Wohnung_in_Gitterzellen.zip"
URL_VG250 = "https://daten.gdz.bkg.bund.de/produkte/vg/vg250_ebenen_0101/2026/vg250_01-01.utm32s.gpkg.ebenen.zip"
USER_AGENT = "KAP3-Stichprobe60/1.0 (Methodik #60)"

# Name in der Ausgabe → (AGS, Länderkürzel, erwarteter VG250-Name GEN).
# AGS aus VG250 2026 (vg250_gem, Feld AGS) nachgeschlagen; der Lauf bricht ab,
# wenn der VG250-Name zum Schlüssel nicht passt.
KOMMUNEN: list[tuple[str, str, str, str]] = [
    ("Grimma", "14729160", "SN", "Grimma"),
    ("Dresden", "14612000", "SN", "Dresden"),
    ("Deggendorf", "09271119", "BY", "Deggendorf"),
    ("Passau", "09262000", "BY", "Passau"),
    ("Halle (Saale)", "15002000", "ST", "Halle (Saale)"),
    ("Hitzacker", "03354009", "NI", "Hitzacker (Elbe)"),
    ("Rosenheim", "09163000", "BY", "Rosenheim"),
    ("Reichertshofen", "09186147", "BY", "Reichertshofen"),
]
LAND_SCHLUESSEL = {"SN": "14", "BY": "09", "ST": "15", "NI": "03"}

ZERO_MARKERS = {"–", "-"}
MISSING_MARKERS = {"", "…", "..."}


# ---------------------------------------------------------------------------
# Download
# ---------------------------------------------------------------------------

def _download(url: str) -> str:
    os.makedirs(CACHE, exist_ok=True)
    dest = os.path.join(CACHE, url.rsplit("/", 1)[1])
    if os.path.isfile(dest) and os.path.getsize(dest) > 0:
        return dest
    print(f"Lade {url}", file=sys.stderr)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    tmp = dest + ".tmp"
    with urllib.request.urlopen(req, timeout=600) as resp, open(tmp, "wb") as f:
        while True:
            chunk = resp.read(1 << 20)
            if not chunk:
                break
            f.write(chunk)
    os.replace(tmp, dest)
    return dest


def _extract(zip_path: str, must_contain: str, suffix: str) -> str:
    with zipfile.ZipFile(zip_path) as zf:
        names = [n for n in zf.namelist()
                 if n.lower().endswith(suffix) and must_contain.lower() in n.lower()]
        if not names:
            raise SystemExit(f"Keine Datei *{must_contain}*{suffix} in {zip_path}")
        name = names[0]
        dest = os.path.join(CACHE, os.path.basename(name))
        if not (os.path.isfile(dest) and os.path.getsize(dest) == zf.getinfo(name).file_size):
            with zf.open(name) as src, open(dest + ".tmp", "wb") as out:
                while True:
                    chunk = src.read(1 << 20)
                    if not chunk:
                        break
                    out.write(chunk)
            os.replace(dest + ".tmp", dest)
    return dest


def _zugriff(path: str) -> str:
    return dt.date.fromtimestamp(os.path.getmtime(path)).isoformat()


# ---------------------------------------------------------------------------
# Koordinaten: EPSG:25832 → geographisch → EPSG:3035 (ETRS89, GRS80)
# ---------------------------------------------------------------------------

A_GRS80 = 6378137.0
F_GRS80 = 1.0 / 298.257222101
E2 = 2 * F_GRS80 - F_GRS80 ** 2
E = math.sqrt(E2)

# Transversale Mercator (Krüger-n-Reihe)
_N = F_GRS80 / (2 - F_GRS80)
_AA = A_GRS80 / (1 + _N) * (1 + _N ** 2 / 4 + _N ** 4 / 64)
_ALPHA = (_N / 2 - 2 * _N ** 2 / 3 + 5 * _N ** 3 / 16,
          13 * _N ** 2 / 48 - 3 * _N ** 3 / 5,
          61 * _N ** 3 / 240)
_BETA = (_N / 2 - 2 * _N ** 2 / 3 + 37 * _N ** 3 / 96,
         _N ** 2 / 48 + _N ** 3 / 15,
         17 * _N ** 3 / 480)
_DELTA = (2 * _N - 2 * _N ** 2 / 3 - 2 * _N ** 3,
          7 * _N ** 2 / 3 - 8 * _N ** 3 / 5,
          56 * _N ** 3 / 15)
UTM_K0, UTM_FE, UTM_LON0 = 0.9996, 500000.0, math.radians(9.0)


def utm32_to_geo(east: float, north: float) -> tuple[float, float]:
    """EPSG:25832 → (φ, λ) im Bogenmaß."""
    xi = north / (UTM_K0 * _AA)
    eta = (east - UTM_FE) / (UTM_K0 * _AA)
    xi_p, eta_p = xi, eta
    for j, b in enumerate(_BETA, start=1):
        xi_p -= b * math.sin(2 * j * xi) * math.cosh(2 * j * eta)
        eta_p -= b * math.cos(2 * j * xi) * math.sinh(2 * j * eta)
    chi = math.asin(math.sin(xi_p) / math.cosh(eta_p))
    phi = chi + sum(d * math.sin(2 * j * chi) for j, d in enumerate(_DELTA, start=1))
    lam = UTM_LON0 + math.atan2(math.sinh(eta_p), math.cos(xi_p))
    return phi, lam


def geo_to_utm32(phi: float, lam: float) -> tuple[float, float]:
    """(φ, λ) → EPSG:25832 — nur für die Hin-/Rück-Probe im Selbsttest."""
    c = 2 * math.sqrt(_N) / (1 + _N)
    t = math.sinh(math.atanh(math.sin(phi)) - c * math.atanh(c * math.sin(phi)))
    dl = lam - UTM_LON0
    xi_p = math.atan(t / math.cos(dl))
    eta_p = math.atanh(math.sin(dl) / math.sqrt(1 + t * t))
    xi, eta = xi_p, eta_p
    for j, a in enumerate(_ALPHA, start=1):
        xi += a * math.sin(2 * j * xi_p) * math.cosh(2 * j * eta_p)
        eta += a * math.cos(2 * j * xi_p) * math.sinh(2 * j * eta_p)
    return UTM_FE + UTM_K0 * _AA * eta, UTM_K0 * _AA * xi


# LAEA (EPSG 9820)
LAEA_PHI0, LAEA_LON0 = math.radians(52.0), math.radians(10.0)
LAEA_FE, LAEA_FN = 4321000.0, 3210000.0


def _q(phi: float) -> float:
    s = math.sin(phi)
    return (1 - E2) * (s / (1 - E2 * s * s) - (1 / (2 * E)) * math.log((1 - E * s) / (1 + E * s)))


_QP = _q(math.pi / 2)
_BETA0 = math.asin(_q(LAEA_PHI0) / _QP)
_RQ = A_GRS80 * math.sqrt(_QP / 2)
_D = A_GRS80 * (math.cos(LAEA_PHI0) / math.sqrt(1 - E2 * math.sin(LAEA_PHI0) ** 2)) / (_RQ * math.cos(_BETA0))


def geo_to_laea(phi: float, lam: float) -> tuple[float, float]:
    beta = math.asin(_q(phi) / _QP)
    dl = lam - LAEA_LON0
    b = _RQ * math.sqrt(2 / (1 + math.sin(_BETA0) * math.sin(beta)
                             + math.cos(_BETA0) * math.cos(beta) * math.cos(dl)))
    x = LAEA_FE + b * _D * math.cos(beta) * math.sin(dl)
    y = LAEA_FN + (b / _D) * (math.cos(_BETA0) * math.sin(beta)
                              - math.sin(_BETA0) * math.cos(beta) * math.cos(dl))
    return x, y


def utm32_to_3035(east: float, north: float) -> tuple[float, float]:
    return geo_to_laea(*utm32_to_geo(east, north))


def _selbsttest() -> None:
    x, y = geo_to_laea(math.radians(50.0), math.radians(5.0))
    assert abs(x - 3962799.45) < 0.01 and abs(y - 2999718.85) < 0.01, (x, y)
    for lat, lon in ((47.5, 12.0), (51.05, 13.74), (53.15, 11.04), (48.57, 13.46)):
        e, n = geo_to_utm32(math.radians(lat), math.radians(lon))
        p, l = utm32_to_geo(e, n)
        assert abs(math.degrees(p) - lat) < 1e-8 and abs(math.degrees(l) - lon) < 1e-8, (lat, lon)
    # Mittelmeridian: E = 500 000 m, Norden = k0 · Meridianbogen (> 0)
    e, n = geo_to_utm32(math.radians(52.0), math.radians(9.0))
    assert abs(e - 500000.0) < 1e-6 and 5.7e6 < n < 5.8e6, (e, n)


# ---------------------------------------------------------------------------
# GeoPackage / WKB
# ---------------------------------------------------------------------------

def _gpkg_wkb(blob: bytes) -> bytes:
    if blob[:2] != b"GP":
        raise ValueError("kein GeoPackage-Geometrieblob")
    flags = blob[3]
    env = {0: 0, 1: 32, 2: 48, 3: 48, 4: 64}[(flags >> 1) & 0x07]
    return blob[8 + env:]


def _parse_wkb(wkb: bytes) -> list[list[tuple[float, float]]]:
    """Gibt alle Ringe (Polygon/MultiPolygon) als Koordinatenlisten zurück."""
    rings: list[list[tuple[float, float]]] = []

    def geom(off: int) -> int:
        bo = "<" if wkb[off] == 1 else ">"
        (typ,) = struct.unpack_from(bo + "I", wkb, off + 1)
        off += 5
        has_z = bool(typ & 0x80000000) or (1000 <= typ % 4000 < 2000) or (3000 <= typ % 4000 < 4000)
        has_m = bool(typ & 0x40000000) or (2000 <= typ % 4000 < 4000)
        base = (typ & 0x0FFFFFFF) % 1000
        dim = 2 + int(has_z) + int(has_m)
        if base == 3:
            (nr,) = struct.unpack_from(bo + "I", wkb, off)
            off += 4
            for _ in range(nr):
                (npt,) = struct.unpack_from(bo + "I", wkb, off)
                off += 4
                vals = struct.unpack_from(bo + "d" * (dim * npt), wkb, off)
                off += 8 * dim * npt
                rings.append([(vals[i], vals[i + 1]) for i in range(0, dim * npt, dim)])
            return off
        if base == 6:
            (ng,) = struct.unpack_from(bo + "I", wkb, off)
            off += 4
            for _ in range(ng):
                off = geom(off)
            return off
        raise ValueError(f"WKB-Typ {typ} nicht unterstützt")

    geom(0)
    return rings


class Flaeche:
    """Fläche aus Ringen in EPSG:3035 mit y-Band-Kantenindex für Punkt-in-Polygon."""

    BAND = 500.0

    def __init__(self, rings_3035: list[list[tuple[float, float]]]):
        xs = [p[0] for r in rings_3035 for p in r]
        ys = [p[1] for r in rings_3035 for p in r]
        self.bbox = (min(xs), min(ys), max(xs), max(ys))
        self.bands: dict[int, list[tuple[float, float, float, float]]] = {}
        for r in rings_3035:
            for (x1, y1), (x2, y2) in zip(r, r[1:] + r[:1]):
                if y1 == y2:
                    continue
                lo, hi = min(y1, y2), max(y1, y2)
                for b in range(int(math.floor(lo / self.BAND)), int(math.floor(hi / self.BAND)) + 1):
                    self.bands.setdefault(b, []).append((x1, y1, x2, y2))

    def in_bbox(self, x: float, y: float) -> bool:
        x0, y0, x1, y1 = self.bbox
        return x0 <= x <= x1 and y0 <= y <= y1

    def enthaelt(self, x: float, y: float) -> bool:
        if not self.in_bbox(x, y):
            return False
        inside = False
        for x1, y1, x2, y2 in self.bands.get(int(math.floor(y / self.BAND)), ()):
            if (y1 > y) != (y2 > y):
                if x < x1 + (y - y1) * (x2 - x1) / (y2 - y1):
                    inside = not inside
        return inside


def _lade_flaechen(gpkg: str, tabelle: str, schluessel: dict[str, str]) -> dict[str, Flaeche]:
    """schluessel: Ausgabekennung → AGS/Landesschlüssel (Feld AGS, GF = 4)."""
    con = sqlite3.connect(gpkg)
    cols = [r[1] for r in con.execute(f"PRAGMA table_info({tabelle})")]
    geomcol = con.execute(
        "SELECT column_name FROM gpkg_geometry_columns WHERE table_name = ?", (tabelle,)
    ).fetchone()[0]
    agscol = next(c for c in cols if c.upper() == "AGS")
    gfcol = next(c for c in cols if c.upper() == "GF")
    gencol = next(c for c in cols if c.upper() == "GEN")
    out: dict[str, Flaeche] = {}
    for kennung, ags in schluessel.items():
        rows = con.execute(
            f"SELECT {gencol}, {geomcol} FROM {tabelle} WHERE {agscol} = ? AND {gfcol} = 4", (ags,)
        ).fetchall()
        if not rows:
            raise SystemExit(f"{tabelle}: AGS {ags} ({kennung}) nicht gefunden")
        rings: list[list[tuple[float, float]]] = []
        for gen, blob in rows:
            for ring in _parse_wkb(_gpkg_wkb(blob)):
                rings.append([utm32_to_3035(e, n) for e, n in ring])
        out[kennung] = Flaeche(rings)
        out[kennung].gen = rows[0][0]  # type: ignore[attr-defined]
    con.close()
    return out


# ---------------------------------------------------------------------------
# Zensus-CSV zeilenweise
# ---------------------------------------------------------------------------

def _num(raw: str) -> float | None:
    """None = fehlend/geheim; '–' wird gesondert als Nullkennzeichen zurückgegeben."""
    s = raw.strip()
    if s in MISSING_MARKERS or s in ZERO_MARKERS:
        return None
    if "," in s:
        s = s.replace(".", "").replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return None


def _lies_gitter(path: str, spalte: str, rechtecke: list[tuple[float, float, float, float]]):
    """Liefert (gitter_id, x_mp, y_mp, rohwert) nur für Zeilen in einem der Rechtecke."""
    gx0 = min(r[0] for r in rechtecke)
    gy0 = min(r[1] for r in rechtecke)
    gx1 = max(r[2] for r in rechtecke)
    gy1 = max(r[3] for r in rechtecke)
    with open(path, encoding="utf-8-sig", newline="") as f:
        kopf = f.readline().rstrip("\r\n").split(";")
        ix, iy, iv = kopf.index("x_mp_100m"), kopf.index("y_mp_100m"), kopf.index(spalte)
        for line in f:
            parts = line.rstrip("\r\n").split(";")
            try:
                x = int(parts[ix])
                y = int(parts[iy])
            except (ValueError, IndexError):
                continue
            if not (gx0 <= x <= gx1 and gy0 <= y <= gy1):
                continue
            if not any(r[0] <= x <= r[2] and r[1] <= y <= r[3] for r in rechtecke):
                continue
            # Zellkennung wie zensus_loader._gitter_id_from_row
            gid = f"CRS3035RES100mN{y - 50}E{x - 50}"
            yield gid, x, y, parts[iv]


# ---------------------------------------------------------------------------
# Hauptablauf
# ---------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 2)[1])
    ap.add_argument("--out", default=OUT)
    args = ap.parse_args()

    _selbsttest()

    zip_w = _download(URL_WOHNUNGEN)
    zip_f = _download(URL_FLAECHE)
    zip_v = _download(URL_VG250)
    csv_w = _extract(zip_w, "100m", ".csv")
    csv_f = _extract(zip_f, "100m", ".csv")
    gpkg = _extract(zip_v, "vg250", ".gpkg")
    zugriff = max(_zugriff(zip_w), _zugriff(zip_f))
    quelle = f"{URL_WOHNUNGEN} | {URL_FLAECHE}"

    gem = _lade_flaechen(gpkg, "vg250_gem", {k[0]: k[1] for k in KOMMUNEN})
    for name, ags, land, gen in KOMMUNEN:
        if gem[name].gen != gen:  # type: ignore[attr-defined]
            raise SystemExit(f"VG250-Name für {ags}: {gem[name].gen!r}, erwartet {gen!r}")
    rechtecke = [gem[k[0]].bbox for k in KOMMUNEN]

    # 1) Wohnungen je Zelle, Zuordnung zur Kommune (Mittelpunkt in Gemeindefläche)
    zellen: dict[str, tuple[str, float]] = {}  # gid → (kommune, wohnungen)
    for gid, x, y, raw in _lies_gitter(csv_w, "Insgesamt_Wohnungen", rechtecke):
        n = _num(raw)
        if n is None or n <= 0:
            continue  # kein Wohnungsbestand ('–' = genau Null) oder Anzahl fehlt
        for name, *_ in KOMMUNEN:
            if gem[name].enthaelt(float(x), float(y)):
                zellen[gid] = (name, n)
                break

    # 2) Fläche je Wohnung für diese Zellen
    flaeche: dict[str, float] = {}
    for gid, _x, _y, raw in _lies_gitter(csv_f, "durchschnFlaechejeWohn", rechtecke):
        if gid in zellen:
            v = _num(raw)
            if v is not None and v > 0:
                flaeche[gid] = v

    # 3) Kommunenwerte (wohnungsgewichtet)
    summe_w: dict[str, float] = {}
    summe_n: dict[str, float] = {}
    for gid, (name, n) in zellen.items():
        if gid in flaeche:
            summe_w[name] = summe_w.get(name, 0.0) + n * flaeche[gid]
            summe_n[name] = summe_n.get(name, 0.0) + n
    a_kommune = {k: summe_w[k] / summe_n[k] for k in summe_w if summe_n[k] > 0}

    a_land: dict[str, float] | None = None

    def landeswert(land: str) -> float:
        nonlocal a_land
        if a_land is None:
            a_land = _landeswerte(gpkg, csv_w, csv_f, rechtecke)
        if land not in a_land:
            raise SystemExit(f"Kein Landeswert für {land} — Ersatzregel nicht anwendbar")
        return a_land[land]

    zeilen = []
    stat: dict[str, dict[str, int]] = {}
    reihenfolge = {k[0]: i for i, k in enumerate(KOMMUNEN)}
    meta = {k[0]: (k[1], k[2]) for k in KOMMUNEN}
    for gid, (name, n) in zellen.items():
        ags, land = meta[name]
        if gid in flaeche:
            w, herkunft = n * flaeche[gid], "zensus"
        elif name in a_kommune:
            w, herkunft = n * a_kommune[name], "fallback_kommune"
        else:
            w, herkunft = n * landeswert(land), "fallback_land"
        stat.setdefault(name, {}).setdefault(herkunft, 0)
        stat[name][herkunft] += 1
        zeilen.append((reihenfolge[name], gid, [name, ags, land, gid, f"{w:.2f}", herkunft, quelle, zugriff]))
    zeilen.sort(key=lambda z: (z[0], z[1]))

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", encoding="utf-8", newline="") as f:
        wr = csv.writer(f, delimiter=";", lineterminator="\n")
        wr.writerow(["kommune", "ags", "land", "gitter_id", "wohnflaeche_m2", "herkunft", "quelle_url", "zugriff"])
        for _, _, z in zeilen:
            wr.writerow(z)

    for name, *_ in KOMMUNEN:
        summe = sum(float(z[2][4]) for z in zeilen if z[2][0] == name)
        print(f"{name:16s} Zellen {sum(stat.get(name, {}).values()):6d} {stat.get(name, {})} "
              f"W = {summe / 1e6:8.3f} Mio m²  Ā = {a_kommune.get(name, float('nan')):.1f} m²/Whg",
              file=sys.stderr)
    print(f"geschrieben: {args.out} ({len(zeilen)} Zeilen)", file=sys.stderr)
    return 0


def _landeswerte(gpkg: str, csv_w: str, csv_f: str, rechtecke) -> dict[str, float]:
    """Ersatzregel Land: wohnungsgewichtete Fläche je Wohnung aller vollständigen
    Zellen im Begrenzungsrechteck, deren Mittelpunkt in der Landesfläche liegt."""
    gx = (min(r[0] for r in rechtecke), min(r[1] for r in rechtecke),
          max(r[2] for r in rechtecke), max(r[3] for r in rechtecke))
    laender = _lade_flaechen(gpkg, "vg250_lan", LAND_SCHLUESSEL)
    n_zelle: dict[str, tuple[float, int, int]] = {}
    for gid, x, y, raw in _lies_gitter(csv_w, "Insgesamt_Wohnungen", [gx]):
        n = _num(raw)
        if n and n > 0:
            n_zelle[gid] = (n, x, y)
    sw: dict[str, float] = {}
    sn: dict[str, float] = {}
    for gid, _x, _y, raw in _lies_gitter(csv_f, "durchschnFlaechejeWohn", [gx]):
        v = _num(raw)
        if gid not in n_zelle or v is None or v <= 0:
            continue
        n, x, y = n_zelle[gid]
        for land, fl in laender.items():
            if fl.enthaelt(float(x), float(y)):
                sw[land] = sw.get(land, 0.0) + n * v
                sn[land] = sn.get(land, 0.0) + n
                break
    return {k: sw[k] / sn[k] for k in sw if sn[k] > 0}


if __name__ == "__main__":
    sys.exit(main())
