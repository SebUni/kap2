#!/usr/bin/env python3
"""
Stichprobe #60: Überflutungsanteil a_{z,s} und Wassertiefe h_{z,s} je 100-m-Zelle
aus den Hochwassergefahrenkarten Niedersachsen für Hitzacker (Elbe).

Modellkontext (docs/methodik/60_gebaeudeschaeden_flusshochwasser.md, §3.2)
--------------------------------------------------------------------------
Datenebenen HQ_FLAECHE und HQ_TIEFE. Datenpaket für den Stichprobenlauf der
Kernformel (Vorhaben T-0284); es schließt keinen Befund. Bericht, Ledger und
Evidenz-Register werden nur gelesen.

Ausgabe
-------
  docs/evidenz/60_stichprobe/hq_niedersachsen.csv   (UTF-8, Trennzeichen ';')
  kommune;szenario;gitter_id;a_anteil;h_m;h_herkunft;quelle_flaeche_url;quelle_tiefe_url;zugriff
  Spalte kommune = 'Hitzacker' (amtlich 'Hitzacker (Elbe)', AGS 03354009).

Datenquelle (ohne Schlüssel, ohne Konto) — Vektor-Download, keine WMS-Karte
--------------------------------------------------------------------------
Hochwassergefahrenkarten nach § 74 WHG / HWRM-RL 2. Zyklus (2016–2021), NLWKN,
Datenlizenz Deutschland – Namensnennung 2.0 (Lizenzdatei in jedem Archiv).
Linkliste des NLWKN (Stand 31.12.2019, geprüft 17.09.2026):
  https://www.nlwkn.niedersachsen.de/download/174298/Datendownload_und_WMS_Dienst_der_GIS-Daten_der_Gefahren-_und_Risikokarten.pdf
Shapefile-Archive (Stand der Dateien 06.09.2021, EPSG:4647 = ETRS89/UTM 32 mit
Zonenpräfix 32 im Rechtswert):
  Fläche: https://www.umweltkarten-niedersachsen.de/Download_OE/HWSchutz/HWRMRL_Z2_Risikogebiete_<S>.zip
          https://www.umweltkarten-niedersachsen.de/Download_OE/HWSchutz/HWRMRL_Z2_Gefahrengebiete_<S>.zip
  Tiefe:  https://www.umweltkarten-niedersachsen.de/Download_OE/HWSchutz/HWRMRL_Z2_Wassertiefen_<S>.zip
  <S> = HQhaeufig | HQ100 | HQextrem.
Derselbe Inhalt liegt im Kartendienst
  https://www.umweltkarten-niedersachsen.de/arcgis/rest/services/Hochwasserschutz_WFS/MapServer
(Ebenen 14–16 „Grenzen der Risikogebiete“, 17–19 „Grenzen der nachrichtlichen Gebiete“
= Überflutungsgebiete ohne zu erwartende signifikante Schäden, 20–22 Wassertiefen); die
Wassertiefen sind dort aber nur als Rasterbild abrufbar, im Download dagegen als Polygone
mit Klasse. Deshalb wird der Download gelesen; eine WMS-Karte über Legendenfarben ist
nicht nötig und wird nicht verwendet. WasserBLIcK/BfG wird nicht gebraucht.
Die Archive werden nicht vollständig geladen: Das ZIP-Inhaltsverzeichnis und die
benötigten Teile werden mit HTTP-Range-Abrufen gelesen; im Archiv HQextrem liegen je
Gewässer unkomprimierte Unterarchive, von denen nur die gelesen werden, deren
Shapefile-Rechteck (Kopf der .shx) das Rechteck der Kommune schneidet.

Zuordnung
---------
* Überflutungsfläche eines Szenarios = Polygone aus Risikogebiete_<S> und
  Gefahrengebiete_<S> (Risikogebiete mit, nachrichtliche Gebiete ohne zu erwartende
  signifikante Schäden). Beide Ebenen werden je Zelle addiert und bei 1 gekappt
  (Modellgrenze wie stichprobe60_hq_sachsen.py: Überlappung nicht als Vereinigung
  gerechnet; die Zahl gekappter Zellen wird im Lauf ausgegeben).
* Tiefe: Wassertiefen_<S>, Feld ClassID 1–5 (ClassTx „0 - 0,5 m“ … „> 4 m“, gegen die
  Klassenmittel geprüft). Die Tiefenpolygone umfassen laut Ebenenbeschreibung auch
  geschützte Bereiche hinter Hochwasserschutzanlagen (grob ermittelt, nicht hydraulisch
  berechnet). Gezählt wird Tiefe nur, soweit die Zelle zur Überflutungsfläche gehört;
  die Tiefenfläche außerhalb der Überflutungsfläche wird im Lauf ausgegeben.
  Modellgrenze: Tiefe und Fläche werden zellweise, nicht polygonweise verschnitten —
  das flächengewichtete Mittel der Zelle nimmt alle Tiefenpolygone der Zelle.

Befunde des Laufs 17.09.2026
----------------------------
* HQhäufig 488 Zellen (4,097 km²), HQ100 490 Zellen (4,137 km²), HQextrem 1 235 Zellen
  (11,619 km²); alle Tiefen aus der Karte, kein Ersatzwert nötig; Tiefenfläche außerhalb
  der Überflutungsfläche im Rechteck 0,000 km².
* HQextrem: Die Risikogebiete von Elbe, Jeetzel und Nachbargewässern überlappen
  (Rückstaubereiche); 741 Zellen werden bei a = 1 gekappt, davon sind 44 nicht schon von
  einem einzelnen Risikogebiet zu ≥ 99 % bedeckt. Nur für diese 44 kann a überschätzt
  sein (Modellgrenze). In überlappenden Zellen gehen die Tiefenpolygone beider Gewässer
  in das Mittel ein. Tiefen HQextrem gelesen aus den Unterarchiven Jeetzel, Mittelelbe, Sude.
* Das Teilarchiv Wassertiefen_HQextrem_Kueste_Tideweser_Z2 ist mit Deflate64 gepackt und
  für zipfile nicht lesbar; es betrifft die Tideweser (rund 150 km westlich) und nicht
  Hitzacker. Der Lauf meldet solche Archive als „NICHT LESBAR“; die Landesverteilung für
  fallback_land bricht in diesem Fall ab, statt unvollständig zu rechnen.

Regeln (§3.2)
-------------
* Zelle: 100 m × 100 m in EPSG:3035, Kennung 'CRS3035RES100mN<y0>E<x0>' wie
  backend/app/services/zensus_loader.py (_gitter_id_from_row).
* a = überflutete Teilfläche / 10 000 m².
* h = flächengewichtetes Mittel der Klassenmittel: 0–0,5 → 0,25 · >0,5–1 → 0,75 ·
  >1–2 → 1,5 · >2–4 → 3,0 · >4 → 4,0.
* Ersatz für a > 0 ohne Tiefe: fallback_kommune = Klassenmittel der flächengewichteten
  Median-Klasse aller Tiefenflächen in Zellen der Kommune im selben Szenario; fehlt sie,
  fallback_land = Klassenmittel der Median-Klasse der amtlichen Klassenverteilung des
  Landes (Summe des Attributs FLAECHE je ClassID über alle Datensätze des Archivs
  Wassertiefen_<S>).
* Zuschnitt: Zelle gehört zur Kommune, wenn ihr Mittelpunkt in der Gemeindefläche aus
  VG250 (BKG, Stand 01.01.2026) liegt; Download und Punkt-in-Polygon wie
  stichprobe60_zensus.py (wiederverwendet).
* Markierungen: keine überflutete Zelle bei vorhandener Karte → eine Zeile 'keine', 0, 0,
  nicht_ueberflutet; schneidet kein einziges Flächenpolygon das Rechteck der Kommune →
  'nicht_kartiert'.

Umsetzung ohne shapely/pyproj
-----------------------------
Shapefile (Typ 5, Polygon) wird zeilenweise aus dem Archivstrom gelesen; Datensätze,
deren Rechteck das Rechteck der Kommune (UTM 32, 200 m Rand) nicht schneidet, werden
übersprungen. Ringe werden in UTM an diesem Rechteck geschnitten (Sutherland–Hodgman),
dann nach EPSG:3035 umgerechnet (Formeln aus stichprobe60_zensus.py, ETRS89 ohne
Datumswechsel) und mit dem Gitterverschnitt aus stichprobe60_hq_sachsen.py je Zelle
flächig verteilt. Esri-Konvention: Außenringe im Uhrzeigersinn, Löcher gegen ihn.

Ressourcen-Regel §3.4
---------------------
Gerechnet wird nur im Rechteck der Kommune. Rohdaten: je Kommune und Archiv die
verdichteten Zellflächen als JSON in backend/.cache/60_stichprobe/ (gitignored);
vorhandene Dateien werden wiederverwendet, zugriff = Dateidatum.

Aufruf
------
  python3 backend/scripts/kalibrierung/stichprobe60_hq_niedersachsen.py
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import math
import os
import sqlite3
import struct
import sys
import time
import urllib.request
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stichprobe60_hq_sachsen as sn  # noqa: E402
import stichprobe60_zensus as zs  # noqa: E402

REPO = zs.REPO
CACHE = zs.CACHE
OUT = os.path.join(REPO, "docs", "evidenz", "60_stichprobe", "hq_niedersachsen.csv")
DL = "https://www.umweltkarten-niedersachsen.de/Download_OE/HWSchutz/HWRMRL_Z2_"
ZELLE = 100.0
RAND = 200.0
ZONE = 32_000_000.0

# Ausgabename, AGS, Name in VG250
KOMMUNEN = [("Hitzacker", "03354009", "Hitzacker (Elbe)")]
# Szenario → Dateikürzel
SZENARIEN = [("HQhäufig", "HQhaeufig"), ("HQ100", "HQ100"), ("HQextrem", "HQextrem")]
KLASSE_ID = {1: 0.25, 2: 0.75, 3: 1.5, 4: 3.0, 5: 4.0}
UNLESBAR: list[str] = []  # Unterarchive, die zipfile nicht entpacken kann


# ---------------------------------------------------------------------------
# Archive über HTTP-Range
# ---------------------------------------------------------------------------

class RangeDatei(io.RawIOBase):
    """Lesbare, suchbare Sicht auf [basis, basis+laenge) einer entfernten Datei."""

    def __init__(self, url: str, basis: int = 0, laenge: int | None = None):
        self.url, self.basis, self.pos = url, basis, 0
        if laenge is None:
            req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": zs.USER_AGENT})
            with urllib.request.urlopen(req, timeout=120) as r:
                laenge = int(r.headers["Content-Length"])
        self.laenge = laenge

    def readable(self): return True
    def seekable(self): return True
    def tell(self): return self.pos

    def seek(self, off, woher=0):
        self.pos = off if woher == 0 else (self.pos + off if woher == 1 else self.laenge + off)
        return self.pos

    def readinto(self, puffer):
        if self.pos >= self.laenge:
            return 0
        ende = min(self.laenge, self.pos + len(puffer)) - 1
        for versuch in range(5):
            try:
                req = urllib.request.Request(self.url, headers={
                    "User-Agent": zs.USER_AGENT,
                    "Range": f"bytes={self.basis + self.pos}-{self.basis + ende}"})
                with urllib.request.urlopen(req, timeout=300) as r:
                    if r.status != 206:
                        raise RuntimeError(f"Range nicht unterstützt ({r.status})")
                    d = r.read()
                break
            except Exception as e:  # noqa: BLE001 — Netzfehler: wiederholen
                if versuch == 4:
                    raise
                print(f"  Wiederholung ({e})", file=sys.stderr)
                time.sleep(10 * (versuch + 1))
        puffer[:len(d)] = d
        self.pos += len(d)
        return len(d)


def _zip(url: str, basis: int = 0, laenge: int | None = None) -> zipfile.ZipFile:
    return zipfile.ZipFile(io.BufferedReader(RangeDatei(url, basis, laenge), 8 << 20))


def shapefiles(url: str, rechteck) -> list[tuple[zipfile.ZipFile, str]]:
    """(Archiv, Basisname) aller Shapefiles, deren Kopfrechteck das Rechteck schneidet;
    unkomprimierte Unterarchive werden über ihren Datenversatz direkt geöffnet."""
    z = _zip(url)
    out = []
    for info in z.infolist():
        n = info.filename
        if n.lower().endswith(".shx"):
            kopf = z.open(info).read(100)
            x0, y0, x1, y1 = struct.unpack("<4d", kopf[36:68])
            if x0 <= rechteck[2] and x1 >= rechteck[0] and y0 <= rechteck[3] and y1 >= rechteck[1]:
                out.append((z, n[:-4]))
        elif n.lower().endswith(".zip"):
            if info.compress_type != zipfile.ZIP_STORED:
                raise SystemExit(f"{url}: Unterarchiv {n} ist komprimiert")
            z.fp.seek(info.header_offset)
            lh = z.fp.read(30)
            nl, el = struct.unpack("<HH", lh[26:30])
            daten = info.header_offset + 30 + nl + el
            out += [(zi, b) for zi, b in _unter(url, daten, info.compress_size, rechteck)]
    return out


def _unter(url, basis, laenge, rechteck):
    z = _zip(url, basis, laenge)
    out = []
    for info in z.infolist():
        if info.filename.lower().endswith(".shx"):
            try:
                kopf = z.open(info).read(100)
            except NotImplementedError:
                # z. B. Deflate64 (Methode 9), von zipfile nicht lesbar
                UNLESBAR.append(f"{info.filename} (Methode {info.compress_type})")
                print(f"  NICHT LESBAR: {info.filename} Kompression {info.compress_type}", file=sys.stderr)
                continue
            x0, y0, x1, y1 = struct.unpack("<4d", kopf[36:68])
            if x0 <= rechteck[2] and x1 >= rechteck[0] and y0 <= rechteck[3] and y1 >= rechteck[1]:
                out.append((z, info.filename[:-4]))
    return out


def dbf_saetze(z: zipfile.ZipFile, basis: str):
    """Liefert die Attributsätze der .dbf als Liste von dicts (Texte gestutzt)."""
    with z.open(basis + ".dbf") as f:
        kopf = f.read(32)
        nrec, hl, rl = struct.unpack("<IHH", kopf[4:12])
        rest = f.read(hl - 32)
        felder, i = [], 0
        while rest[i] != 0x0D:
            felder.append((rest[i:i + 11].split(b"\0")[0].decode("ascii"), rest[i + 16]))
            i += 32
        out = []
        for _ in range(nrec):
            s = f.read(rl)
            d, p = {}, 1
            for name, laenge in felder:
                d[name] = s[p:p + laenge].decode("utf-8", "replace").strip()
                p += laenge
            out.append(d)
    return out


# ---------------------------------------------------------------------------
# Shapefile-Datensätze → Zellflächen
# ---------------------------------------------------------------------------

def _ring_im_rechteck(ring, r):
    for achse, wert, unten in ((0, r[0], False), (0, r[2], True), (1, r[1], False), (1, r[3], True)):
        ring = sn._clip(ring, achse, wert, unten)
        if len(ring) < 3:
            return []
    return ring


def datensatz_zellflaechen(inhalt: bytes, rechteck) -> dict:
    """Polygon-Datensatz (Typ 5/15/25) → {(x0, y0): Fläche} in EPSG:3035, im Rechteck."""
    typ = struct.unpack("<i", inhalt[:4])[0]
    if typ == 0:
        return {}
    if typ not in (5, 15, 25):
        raise SystemExit(f"Shapefile-Typ {typ} nicht unterstützt")
    nparts, npts = struct.unpack("<ii", inhalt[36:44])
    teile = list(struct.unpack(f"<{nparts}i", inhalt[44:44 + 4 * nparts])) + [npts]
    xy = struct.unpack(f"<{2 * npts}d", inhalt[44 + 4 * nparts:44 + 4 * nparts + 16 * npts])
    roh: dict = {}
    for a, b in zip(teile, teile[1:]):
        xs, ys = xy[2 * a:2 * b:2], xy[2 * a + 1:2 * b:2]
        if min(xs) > rechteck[2] or max(xs) < rechteck[0] or min(ys) > rechteck[3] or max(ys) < rechteck[1]:
            continue
        ring = list(zip(xs, ys))
        if len(ring) > 1 and ring[0] == ring[-1]:
            ring = ring[:-1]
        ring = _ring_im_rechteck(ring, rechteck)
        if not ring:
            continue
        # Esri: Außenring im Uhrzeigersinn → negative Gaußfläche; Vorzeichen umkehren
        sn.ring_zellflaechen([zs.utm32_to_3035(x - ZONE, y) for x, y in reversed(ring)], roh)
    return {k: v for k, v in roh.items() if abs(v) > 1e-6}


def archiv_verdichten(kommune: str, datei: str, rechteck, tiefe: bool) -> tuple[dict, str]:
    """{'anzahl': Datensätze im Rechteck, 'zellen': {'x0,y0': {schlüssel: Fläche}}}.
    Schlüssel = Klassenmittel (Tiefe) bzw. APSFR_CODE des Risikogebiets (Fläche)."""
    pfad = os.path.join(CACHE, f"hq_ni_{kommune}_{datei}.json")
    if os.path.isfile(pfad):
        with open(pfad, encoding="utf-8") as f:
            return json.load(f), zs._zugriff(pfad)
    url = f"{DL}{datei}.zip"
    zellen: dict[str, dict[str, float]] = {}
    anzahl = 0
    for z, basis in shapefiles(url, rechteck):
        saetze = dbf_saetze(z, basis)
        with z.open(basis + ".shp") as f:
            f.read(100)
            nr = 0
            while True:
                kopf = f.read(8)
                if len(kopf) < 8:
                    break
                laenge = struct.unpack(">i", kopf[4:8])[0] * 2
                inhalt = f.read(laenge)
                attr = saetze[nr]
                nr += 1
                if len(inhalt) < 36 or struct.unpack("<i", inhalt[:4])[0] == 0:
                    continue
                x0, y0, x1, y1 = struct.unpack("<4d", inhalt[4:36])
                if x0 > rechteck[2] or x1 < rechteck[0] or y0 > rechteck[3] or y1 < rechteck[1]:
                    continue
                if tiefe:
                    kl = KLASSE_ID.get(int(float(attr["ClassID"])))
                    if kl is None or sn.klassenmittel(attr["ClassTx"]) != kl:
                        raise SystemExit(f"{basis}: Klasse {attr['ClassID']} / {attr['ClassTx']!r} unbekannt")
                    schl = str(kl)
                else:
                    schl = attr.get("APSFR_CODE", "")
                teile = datensatz_zellflaechen(inhalt, rechteck)
                if teile:
                    anzahl += 1
                for (cx, cy), fl in teile.items():
                    zz = zellen.setdefault(f"{cx},{cy}", {})
                    zz[schl] = zz.get(schl, 0.0) + fl
        print(f"  {kommune} {basis}: {nr} Datensätze gelesen", file=sys.stderr)
    erg = {"anzahl": anzahl, "rechteck": list(rechteck), "zellen": zellen}
    os.makedirs(CACHE, exist_ok=True)
    with open(pfad + ".tmp", "w", encoding="utf-8") as f:
        json.dump(erg, f)
    os.replace(pfad + ".tmp", pfad)
    return erg, zs._zugriff(pfad)


def landesverteilung(datei: str) -> dict[float, float]:
    """Amtliche Klassenverteilung des Landes: Summe FLAECHE je Klasse im Archiv."""
    pfad = os.path.join(CACHE, f"hq_ni_land_{datei}.json")
    if os.path.isfile(pfad):
        with open(pfad, encoding="utf-8") as f:
            return {float(k): v for k, v in json.load(f).items()}
    vert: dict[float, float] = {}
    UNLESBAR.clear()
    teile = shapefiles(f"{DL}{datei}.zip", (-1e12, -1e12, 1e12, 1e12))
    if UNLESBAR:
        raise SystemExit(f"{datei}: Landesverteilung unvollständig, nicht lesbar: {UNLESBAR}. "
                         "Eskalieren, nichts erfinden.")
    for z, basis in teile:
        for s in dbf_saetze(z, basis):
            kl = KLASSE_ID[int(float(s["ClassID"]))]
            vert[kl] = vert.get(kl, 0.0) + float(s["FLAECHE"])
    with open(pfad, "w", encoding="utf-8") as f:
        json.dump(vert, f)
    return vert


def rechteck_utm(gpkg: str, ags: str) -> tuple[float, float, float, float]:
    con = sqlite3.connect(gpkg)
    geomcol = con.execute(
        "SELECT column_name FROM gpkg_geometry_columns WHERE table_name = 'vg250_gem'").fetchone()[0]
    xs, ys = [], []
    for (blob,) in con.execute(f"SELECT {geomcol} FROM vg250_gem WHERE AGS = ? AND GF = 4", (ags,)):
        for ring in zs._parse_wkb(zs._gpkg_wkb(blob)):
            xs += [p[0] for p in ring]
            ys += [p[1] for p in ring]
    con.close()
    return (math.floor(min(xs) - RAND) + ZONE, math.floor(min(ys) - RAND),
            math.ceil(max(xs) + RAND) + ZONE, math.ceil(max(ys) + RAND))


def _selbsttest_datensatz() -> None:
    # Quadrat 150 × 150 m im Uhrzeigersinn, Loch 20 × 20 m; Gesamtfläche 22 100 m²
    e0, n0 = ZONE + 600000.0, 5900000.0
    aussen = [(e0, n0), (e0, n0 + 150), (e0 + 150, n0 + 150), (e0 + 150, n0), (e0, n0)]
    loch = [(e0 + 60, n0 + 60), (e0 + 80, n0 + 60), (e0 + 80, n0 + 80), (e0 + 60, n0 + 80), (e0 + 60, n0 + 60)]
    pts = aussen + loch
    inhalt = (struct.pack("<i4d", 5, 0, 0, 0, 0) + struct.pack("<ii", 2, len(pts))
              + struct.pack("<ii", 0, len(aussen))
              + struct.pack(f"<{2 * len(pts)}d", *[c for p in pts for c in p]))
    f = datensatz_zellflaechen(inhalt, (e0 - 1000, n0 - 1000, e0 + 1000, n0 + 1000))
    assert abs(sum(f.values()) / 22100 - 1) < 1e-3, f  # UTM-Maßstab k ≈ 0,9997 (100 km vom Mittelmeridian)
    # Beschnitt am Rechteck: nur die linke Hälfte (75 × 150 m) zählt
    f = datensatz_zellflaechen(inhalt, (e0 - 1000, n0 - 1000, e0 + 75, n0 + 1000))
    assert abs(sum(f.values()) / (75 * 150 - 15 * 20) - 1) < 1e-3, f


# ---------------------------------------------------------------------------
# Hauptablauf
# ---------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 2)[1])
    ap.add_argument("--out", default=OUT)
    args = ap.parse_args()

    zs._selbsttest()
    sn._selbsttest_verschnitt()
    _selbsttest_datensatz()

    gpkg = zs._extract(zs._download(zs.URL_VG250), "vg250", ".gpkg")
    gem = zs._lade_flaechen(gpkg, "vg250_gem", {k[0]: k[1] for k in KOMMUNEN})
    zeilen = []
    for name, ags, gen in KOMMUNEN:
        if gem[name].gen != gen:  # type: ignore[attr-defined]
            raise SystemExit(f"VG250-Name für {ags}: {gem[name].gen!r}, erwartet {gen!r}")
        fl = gem[name]
        rechteck = rechteck_utm(gpkg, ags)
        for szen, kurz in SZENARIEN:
            quellen = [f"Risikogebiete_{kurz}", f"Gefahrengebiete_{kurz}"]
            flaechen = [archiv_verdichten(name, q, rechteck, False) for q in quellen]
            dt_, zt = archiv_verdichten(name, f"Wassertiefen_{kurz}", rechteck, True)
            url_f, url_t = f"{DL}{quellen[0]}.zip", f"{DL}Wassertiefen_{kurz}.zip"
            zugriff = max([z for _, z in flaechen] + [zt])
            if sum(d["anzahl"] for d, _ in flaechen) == 0:
                zeilen.append([name, szen, "keine", "0", "0", "nicht_kartiert", url_f, url_t, zugriff])
                print(f"{name} {szen:9s} nicht kartiert", file=sys.stderr)
                continue
            flut: dict[str, float] = {}
            groesst: dict[str, float] = {}
            for d, _ in flaechen:
                for key, teile in d["zellen"].items():
                    flut[key] = flut.get(key, 0.0) + sum(teile.values())
                    groesst[key] = max([groesst.get(key, 0.0)] + list(teile.values()))
            zell, kapp, kapp_teil, tiefe_aussen = [], 0, 0, 0.0
            for key, t in dt_["zellen"].items():
                if key not in flut:
                    tiefe_aussen += sum(t.values())
            for key, fla in flut.items():
                cx, cy = (int(v) for v in key.split(","))
                if not fl.enthaelt(cx + 50.0, cy + 50.0):
                    continue
                a = fla / (ZELLE * ZELLE)
                if a > 1.0:
                    kapp, a = kapp + 1, 1.0
                    if groesst[key] < 0.99 * ZELLE * ZELLE:
                        kapp_teil += 1
                if a < 5e-7:
                    continue
                kl_fl = {float(k): v for k, v in dt_["zellen"].get(key, {}).items() if v > 0}
                tief = sum(kl_fl.values())
                h = sum(k * v for k, v in kl_fl.items()) / tief if tief > 0 else None
                zell.append((f"CRS3035RES100mN{cy}E{cx}", a, h, kl_fl))
            if not zell:
                zeilen.append([name, szen, "keine", "0", "0", "nicht_ueberflutet", url_f, url_t, zugriff])
                print(f"{name} {szen:9s} nicht überflutet", file=sys.stderr)
                continue
            gesamt_kl: dict[float, float] = {}
            for *_, kl_fl in zell:
                for k, v in kl_fl.items():
                    gesamt_kl[k] = gesamt_kl.get(k, 0.0) + v
            median = sn._median_klasse(gesamt_kl)
            stat = {"karte": 0, "fallback_kommune": 0, "fallback_land": 0}
            for gid, a, h, _ in sorted(zell):
                if h is not None:
                    herk = "karte"
                elif median is not None:
                    h, herk = median, "fallback_kommune"
                else:
                    h, herk = sn._median_klasse(landesverteilung(f"Wassertiefen_{kurz}")), "fallback_land"
                stat[herk] += 1
                zeilen.append([name, szen, gid, f"{a:.6f}", f"{h:.4f}", herk, url_f, url_t, zugriff])
            summe = sum(z[1] for z in zell) * ZELLE * ZELLE / 1e6
            print(f"{name} {szen:9s} Zellen {len(zell):5d} {stat} gekappt {kapp} "
                  f"(davon ohne ein einzelnes Risikogebiet ≥ 0,99: {kapp_teil}) "
                  f"Fläche {summe:6.3f} km²  Median-Klasse {median}  Tiefenfläche außerhalb "
                  f"der Überflutungsfläche {tiefe_aussen / 1e6:.3f} km² (Rechteck)", file=sys.stderr)

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", encoding="utf-8", newline="") as f:
        wr = csv.writer(f, delimiter=";", lineterminator="\n")
        wr.writerow(["kommune", "szenario", "gitter_id", "a_anteil", "h_m", "h_herkunft",
                     "quelle_flaeche_url", "quelle_tiefe_url", "zugriff"])
        wr.writerows(zeilen)
    print(f"geschrieben: {args.out} ({len(zeilen)} Zeilen)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
