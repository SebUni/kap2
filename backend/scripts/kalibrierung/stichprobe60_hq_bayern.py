#!/usr/bin/env python3
"""
Stichprobe #60: Überflutungsanteil a_{z,s} und Wassertiefe h_{z,s} je 100-m-Zelle
aus den Hochwassergefahrenkarten Bayern für Deggendorf, Passau, Rosenheim und
Reichertshofen.

Modellkontext (docs/methodik/60_gebaeudeschaeden_flusshochwasser.md, §3.2)
--------------------------------------------------------------------------
Datenebenen HQ_FLAECHE und HQ_TIEFE. Datenpaket für den Stichprobenlauf der
Kernformel (Vorhaben T-0284); es schließt keinen Befund. Bericht, Ledger und
Evidenz-Register werden nur gelesen.

Ausgabe
-------
  docs/evidenz/60_stichprobe/hq_bayern.csv   (UTF-8, Trennzeichen ';')
  kommune;szenario;gitter_id;a_anteil;h_m;h_herkunft;quelle_flaeche_url;quelle_tiefe_url;zugriff

Datenquelle (ohne Schlüssel, ohne Konto) — WMS über Legendenfarben, Pixel 5 m
-----------------------------------------------------------------------------
Hochwassergefahrenkarten nach § 74 WHG, Bayerisches Landesamt für Umwelt (LfU),
Darstellungsdienste des UmweltAtlas Bayern (Nutzung über Dienste geldleistungsfrei):
  Fläche: https://www.lfu.bayern.de/gdi/wms/wasser/ueberschwemmungsgebiete
          Ebenen hwgf_hqhaeufig, hwgf_hq100, hwgf_hqextrem („Hochwassergefahrenflächen …“),
          dazu hwgg_hq100 („Hochwassergeschützte Gebiete HQ100“)
  Tiefe:  https://www.lfu.bayern.de/gdi/wms/wasser/wassertiefen
          Ebenen wt_hqhaeufig, wt_hq100, wt_hqextrem, wt_hwgg_hq100 („Wassertiefen für …“)
          Legenden https://www.lfu.bayern.de/gdi/legende/wasser/wassertiefen/<ebene>.png
Warum WMS: Das LfU bietet für die Hochwassergefahrenflächen und Wassertiefen weder
WFS noch Download an (geprüft 17.09.2026: Übersicht Downloaddienste
https://www.lfu.bayern.de/umweltdaten/geodatendienste/index_download.htm und CSW
https://geoportal.bayern.de/csw/gdi, Suchbegriffe „Hochwassergefahren“ und
„Wassertiefe“ — nur WMS-Einträge; Seite „Hochwassergefahrenkarten zum Herunterladen“
bietet nur PDF 1:10 000). Die BfG (geoportal.bafg.de/arcgis1/rest/services/HWRMRL/
HWRMRL_DE_L{H,M,L}) führt abfragbare Flächen, für Bayern aber nur den Berichtsstand
REP_YEAR 2013 (Import 2015) und ohne Wassertiefen; sie ist damit nicht die geltende
Karte und wird nicht verwendet.
Verfahren nach Ticket-Vorgabe: GetMap in EPSG:25832, Pixel genau 5 m × 5 m,
Format image/bmp (unkomprimiert, weißer Hintergrund), Kacheln 1000 × 1000 px.
  * Fläche: jedes nicht weiße Pixel der hwgf-Ebene gilt als überflutet (25 m²).
  * Tiefe: Pixel der wt-Ebene werden der nächstliegenden Legendenfarbe zugeordnet
    (Toleranz TOLERANZ je Farbkanal, Reihenfolge der Legendenfelder von oben:
    >0–0,5 · >0,5–1 · >1–2 · >2–4 · >4 · „nicht ermittelt“). Pixel ohne passende Farbe
    (Kantenglättung, Beschriftung) und „nicht ermittelt“ tragen keine Tiefe.
  * HQ100 mit hochwassergeschützten Gebieten (Nacharbeit R1, wie stichprobe60_hq_sachsen.py,
    dort HWS = „ja“): Fläche = pixelweise Vereinigung von hwgf_hq100 und hwgg_hq100
    („Hochwassergeschützte Gebiete HQ100“), beide im selben Kachelraster, jedes Pixel
    höchstens einmal. Tiefe = Klasse aus wt_hq100; zeigt wt_hq100 dort nichts oder
    „nicht ermittelt“, gilt die Klasse aus wt_hwgg_hq100 („Wassertiefen für HQ100 in
    geschützten Gebieten“, eigene Legendenfarben mit denselben fünf Klassengrenzen,
    ohne Feld „nicht ermittelt“; die Farben werden je Ebene aus ihrer Legende gelesen).
    Modellgrenze: Die geschützten Flächen gehören zur veröffentlichten Überflutungsfläche
    des Szenarios und gelten damit als überflutet bei Versagen des Schutzes.
Modellgrenzen: Pixelzuordnung über den Pixelmittelpunkt; Überdeckung durch Signaturen
der Karte ist nicht auszuschließen.
Befund zur Tiefenlücke (Lauf 17.09.2026, Ersatztiefe fallback_kommune bei HQ100):
  * Deggendorf 2 082 von 2 351 Zellen. 892 davon liegen in hwgf_hq100, dort zeigt
    wt_hq100 weder eine Klasse noch „nicht ermittelt“ (Ebene leer), während wt_hqhaeufig
    und wt_hqextrem an denselben Stellen Tiefen führen (Stichprobe UTM32 794180/5411633:
    Fläche voll, wt_hq100 leer). Ursache ist eine Lücke der veröffentlichten HQ100-
    Tiefenkarte, kein Deichschutz. 6 Zellen „nicht ermittelt“. 1 184 Zellen liegen nur in
    hwgg_hq100; wt_hwgg_hq100 ist dort leer (im 20-km-Rechteck 0,0016 km²).
  * Passau 107 von 964 Zellen, alle „nicht ermittelt“ (nach LfU-Beschreibung z. B.
    Staustufen).
  Die Ersatzregel des Tickets wird unverändert angewandt; andere Szenarien werden nicht
  zur Tiefe herangezogen.

Regeln (§3.2)
-------------
* Zelle: 100 m × 100 m in EPSG:3035, Kennung 'CRS3035RES100mN<y0>E<x0>' wie
  backend/app/services/zensus_loader.py. Pixelmittelpunkt EPSG:25832 → EPSG:3035 mit
  den geprüften Formeln aus stichprobe60_zensus.py (gleiches Datum ETRS89).
* a = überflutete Pixelfläche / 10 000 m², bei 1 gekappt.
* h = flächengewichtetes Mittel der Klassenmittel über die Pixel mit Tiefenklasse,
  LAWA: 0–0,5 → 0,25 · >0,5–1 → 0,75 · >1–2 → 1,5 · >2–4 → 3,0 · >4 → 4,0.
* Ersatz für a > 0 ohne Tiefe: fallback_kommune = Klassenmittel der flächengewichteten
  Median-Tiefenklasse der Kommune im selben Szenario; fehlt sie, fallback_land — für
  Bayern ist keine amtlich veröffentlichte Klassenverteilung hinterlegt, der Lauf
  bricht dann ab (nichts erfinden, Eskalation).
* Zuschnitt: Zelle gehört zur Kommune, wenn ihr Mittelpunkt in der Gemeindefläche aus
  VG250 (BKG, Stand 01.01.2026, dl-de/by-2-0) liegt; wie stichprobe60_zensus.py.
* Markierungen: keine überflutete Zelle, aber Karteninhalt im Rechteck der Kommune →
  'keine', 0, 0, nicht_ueberflutet; liefert die Flächenebene im ganzen Rechteck kein
  einziges Pixel → nicht_kartiert.

Ressourcen-Regel §3.4
---------------------
Kein Landeslauf: Abgerufen wird je Kommune und Ebene nur das Begrenzungsrechteck der
Gemeindefläche (EPSG:25832, auf 5 m gerundet). Rohdaten: je Kommune und Ebene die
verdichteten Zellzählungen als JSON in backend/.cache/60_stichprobe/ (gitignored);
vorhandene Dateien werden wiederverwendet, zugriff = Dateidatum.

Aufruf
------
  python3 backend/scripts/kalibrierung/stichprobe60_hq_bayern.py
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import sqlite3
import struct
import sys
import time
import urllib.parse
import urllib.request
import zlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stichprobe60_zensus as zs  # noqa: E402
from stichprobe60_hq_sachsen import _median_klasse  # noqa: E402

REPO = zs.REPO
CACHE = zs.CACHE
OUT = os.path.join(REPO, "docs", "evidenz", "60_stichprobe", "hq_bayern.csv")
WMS_F = "https://www.lfu.bayern.de/gdi/wms/wasser/ueberschwemmungsgebiete"
WMS_T = "https://www.lfu.bayern.de/gdi/wms/wasser/wassertiefen"
LEGENDE = "https://www.lfu.bayern.de/gdi/legende/wasser/wassertiefen/{}.png"
ZELLE = 100
PIXEL = 5
KACHEL = 1000
TOLERANZ = 12

KOMMUNEN = [
    ("Deggendorf", "09271119", "Deggendorf"),
    ("Passau", "09262000", "Passau"),
    ("Rosenheim", "09163000", "Rosenheim"),
    ("Reichertshofen", "09186147", "Reichertshofen"),
]
# Szenario → (Flächenebenen, Tiefenebenen in Vorrangreihenfolge)
SZENARIEN = [("HQhäufig", ["hwgf_hqhaeufig"], ["wt_hqhaeufig"]),
             ("HQ100", ["hwgf_hq100", "hwgg_hq100"], ["wt_hq100", "wt_hwgg_hq100"]),
             ("HQextrem", ["hwgf_hqextrem"], ["wt_hqextrem"])]
# Legendenfelder von oben → Klassenmittel (None = „nicht ermittelt“)
KLASSEN_LEGENDE = [0.25, 0.75, 1.5, 3.0, 4.0, None]


def _get(url: str, params: dict | None = None) -> bytes:
    if params:
        url = url + "?" + urllib.parse.urlencode(params)
    for versuch in range(5):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": zs.USER_AGENT})
            with urllib.request.urlopen(req, timeout=300) as r:
                return r.read()
        except Exception as e:  # noqa: BLE001 — Netz/Dienstfehler: wiederholen
            if versuch == 4:
                raise
            print(f"  Wiederholung ({e})", file=sys.stderr)
            time.sleep(10 * (versuch + 1))
    raise AssertionError


# ---------------------------------------------------------------------------
# Bilddekodierung ohne Zusatzpakete
# ---------------------------------------------------------------------------

def png_rgb(data: bytes) -> tuple[int, int, list[list[tuple[int, int, int, int]]]]:
    """Kleiner PNG-Dekoder (8 Bit, Farbtypen 2, 3, 6) — nur für Legendenbilder."""
    assert data[:8] == b"\x89PNG\r\n\x1a\n"
    pos, idat, pal, trns = 8, b"", None, None
    while pos < len(data):
        n = struct.unpack(">I", data[pos:pos + 4])[0]
        typ, body = data[pos + 4:pos + 8], data[pos + 8:pos + 8 + n]
        if typ == b"IHDR":
            w, h, tiefe, ft = struct.unpack(">IIBB", body[:10])
        elif typ == b"PLTE":
            pal = [tuple(body[i:i + 3]) for i in range(0, len(body), 3)]
        elif typ == b"tRNS":
            trns = body
        elif typ == b"IDAT":
            idat += body
        pos += 12 + n
    if tiefe != 8 or ft not in (2, 3, 6):
        raise SystemExit(f"Legende: PNG-Format {tiefe}/{ft} nicht unterstützt")
    bpp = {2: 3, 3: 1, 6: 4}[ft]
    roh = zlib.decompress(idat)
    zeilen, vor, p = [], bytearray(w * bpp), 0
    for _ in range(h):
        f, z = roh[p], bytearray(roh[p + 1:p + 1 + w * bpp])
        p += 1 + w * bpp
        for i in range(len(z)):
            a = z[i - bpp] if i >= bpp else 0
            b = vor[i]
            c = vor[i - bpp] if i >= bpp else 0
            if f == 1:
                z[i] = (z[i] + a) & 255
            elif f == 2:
                z[i] = (z[i] + b) & 255
            elif f == 3:
                z[i] = (z[i] + (a + b) // 2) & 255
            elif f == 4:
                pa, pb, pc = abs(b - c), abs(a - c), abs(a + b - 2 * c)
                z[i] = (z[i] + (a if pa <= pb and pa <= pc else b if pb <= pc else c)) & 255
        vor = z
        px = []
        for x in range(w):
            if ft == 2:
                px.append((z[3 * x], z[3 * x + 1], z[3 * x + 2], 255))
            elif ft == 6:
                px.append(tuple(z[4 * x:4 * x + 4]))
            else:
                r, g, bl = pal[z[x]]
                al = trns[z[x]] if trns and z[x] < len(trns) else 255
                px.append((r, g, bl, al))
        zeilen.append(px)
    return w, h, zeilen


def legendenfarben(ebene: str) -> list[tuple[tuple[int, int, int], float | None]]:
    """Farben der Legendenfelder von oben nach unten (Spalte in der Feldmitte)."""
    pfad = os.path.join(CACHE, f"hq_by_legende_{ebene}.png")
    if not os.path.isfile(pfad):
        os.makedirs(CACHE, exist_ok=True)
        with open(pfad, "wb") as f:
            f.write(_get(LEGENDE.format(ebene)))
    with open(pfad, "rb") as f:
        w, h, bild = png_rgb(f.read())
    farben: list[tuple[int, int, int]] = []
    letzte = None
    for y in range(h):
        r, g, b, a = bild[y][min(20, w - 1)]
        c = (r, g, b) if a > 200 and (r, g, b) != (255, 255, 255) else None
        if c is not None and c != letzte and c not in farben:
            farben.append(c)
        letzte = c
    # wt_hwgg_hq100 führt kein Feld „nicht ermittelt“ (5 Felder, gleiche Klassengrenzen)
    if len(farben) not in (len(KLASSEN_LEGENDE) - 1, len(KLASSEN_LEGENDE)):
        raise SystemExit(f"Legende {ebene}: {len(farben)} Felder {farben}, erwartet 5 oder 6")
    return list(zip(farben, KLASSEN_LEGENDE))


def bmp_pixel(data: bytes):
    """Liefert (w, h, zeile(y) → bytes BGR von oben nach unten)."""
    if data[:2] != b"BM":
        raise SystemExit(f"WMS-Antwort ist kein BMP: {data[:300]!r}")
    off = struct.unpack("<I", data[10:14])[0]
    w, h = struct.unpack("<ii", data[18:26])
    bpp = struct.unpack("<H", data[28:30])[0]
    if bpp not in (24, 32):
        raise SystemExit(f"BMP mit {bpp} Bit nicht unterstützt")
    k = bpp // 8
    step = ((w * k + 3) // 4) * 4
    oben_nach_unten = h < 0
    h = abs(h)

    def zeile(y: int) -> bytes:
        yy = y if oben_nach_unten else h - 1 - y
        z = data[off + yy * step: off + yy * step + w * k]
        return z if k == 3 else bytes(b for i, b in enumerate(z) if i % 4 != 3)

    return w, h, zeile


# ---------------------------------------------------------------------------
# Abruf und Verdichtung je Kommune und Ebene
# ---------------------------------------------------------------------------

def ebene_verdichten(kommune: str, quellen, bbox_utm, farben) -> tuple[dict, str]:
    """{'pixel': n, 'zellen': {'x0,y0': {klasse|'f'|'n': anzahl}}}.

    quellen: Liste (WMS, Ebene) in Vorrangreihenfolge, alle im selben Kachelraster abgerufen.
    farben None = Flächenebenen, sonst je Quelle eine Legendenfarbliste: ein Pixel zählt einmal, wenn es in irgendeiner Ebene nicht
    weiß ist (pixelweises ODER, keine Doppelzählung). Sonst Tiefenebenen: es gilt die erste
    Ebene mit einer Tiefenklasse; „nicht ermittelt“ ('n') nur, wenn keine Ebene eine Klasse hat.
    """
    name = "+".join(e for _, e in quellen)
    pfad = os.path.join(CACHE, f"hq_by_{kommune}_{name}.json")
    if os.path.isfile(pfad):
        with open(pfad, encoding="utf-8") as f:
            return json.load(f), zs._zugriff(pfad)
    e0, n0, e1, n1 = bbox_utm
    zellen: dict[str, dict[str, int]] = {}
    pixel = unklassiert = 0
    weiss = b"\xff\xff\xff"
    cache_farbe: dict[tuple[int, bytes], str | None] = {}

    def klasse(i: int, px: bytes) -> str | None:
        if (i, px) not in cache_farbe:
            b, g, r = px
            best = None
            for (fr, fg, fb), kl in farben[i]:
                if max(abs(r - fr), abs(g - fg), abs(b - fb)) <= TOLERANZ:
                    best = "n" if kl is None else str(kl)
                    break
            cache_farbe[(i, px)] = best
        return cache_farbe[(i, px)]

    for ke in range(e0, e1, KACHEL * PIXEL):
        for kn in range(n0, n1, KACHEL * PIXEL):
            bilder = []
            for wms, ebene in quellen:
                data = _get(wms, {
                    "SERVICE": "WMS", "VERSION": "1.3.0", "REQUEST": "GetMap", "LAYERS": ebene,
                    "STYLES": "", "CRS": "EPSG:25832",
                    "BBOX": f"{ke},{kn},{ke + KACHEL * PIXEL},{kn + KACHEL * PIXEL}",
                    "WIDTH": str(KACHEL), "HEIGHT": str(KACHEL), "FORMAT": "image/bmp",
                    "TRANSPARENT": "FALSE", "BGCOLOR": "0xFFFFFF"})
                w, h, zeile = bmp_pixel(data)
                assert (w, h) == (KACHEL, KACHEL), (w, h)
                bilder.append(zeile)
            leer = weiss * KACHEL
            for y in range(KACHEL):
                zz_ = [(i, z) for i, z in enumerate(zeile(y) for zeile in bilder) if z != leer]
                if not zz_:
                    continue
                north = kn + KACHEL * PIXEL - (y + 0.5) * PIXEL
                for x in range(KACHEL):
                    werte = [(i, z[3 * x:3 * x + 3]) for i, z in zz_]
                    werte = [(i, px) for i, px in werte if px != weiss]
                    if not werte:
                        continue
                    if farben is None:
                        schl = "f"
                    else:
                        kls = [klasse(i, px) for i, px in werte]
                        schl = next((k for k in kls if k not in (None, "n")), None)
                        if schl is None:
                            schl = "n" if "n" in kls else None
                        if schl is None:
                            unklassiert += 1
                            continue
                    pixel += 1
                    ex, ey = zs.utm32_to_3035(ke + (x + 0.5) * PIXEL, north)
                    key = f"{int(math.floor(ex / ZELLE) * ZELLE)},{int(math.floor(ey / ZELLE) * ZELLE)}"
                    zz = zellen.setdefault(key, {})
                    zz[schl] = zz.get(schl, 0) + 1
            print(f"  {kommune} {name}: Kachel {ke},{kn} — {pixel} Pixel", file=sys.stderr)
    erg = {"pixel": pixel, "unklassiert": unklassiert, "bbox_utm": list(bbox_utm), "zellen": zellen}
    os.makedirs(CACHE, exist_ok=True)
    with open(pfad + ".tmp", "w", encoding="utf-8") as f:
        json.dump(erg, f)
    os.replace(pfad + ".tmp", pfad)
    return erg, zs._zugriff(pfad)


def bbox_utm(gpkg: str, ags: str) -> tuple[int, int, int, int]:
    con = sqlite3.connect(gpkg)
    geomcol = con.execute(
        "SELECT column_name FROM gpkg_geometry_columns WHERE table_name = 'vg250_gem'").fetchone()[0]
    xs, ys = [], []
    for (blob,) in con.execute(f"SELECT {geomcol} FROM vg250_gem WHERE AGS = ? AND GF = 4", (ags,)):
        for ring in zs._parse_wkb(zs._gpkg_wkb(blob)):
            xs += [p[0] for p in ring]
            ys += [p[1] for p in ring]
    con.close()
    rd = lambda v, up: int((math.ceil if up else math.floor)(v / PIXEL) * PIXEL)  # noqa: E731
    return rd(min(xs) - 100, False), rd(min(ys) - 100, False), rd(max(xs) + 100, True), rd(max(ys) + 100, True)


# ---------------------------------------------------------------------------
# Hauptablauf
# ---------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 2)[1])
    ap.add_argument("--out", default=OUT)
    args = ap.parse_args()

    zs._selbsttest()
    gpkg = zs._extract(zs._download(zs.URL_VG250), "vg250", ".gpkg")
    gem = zs._lade_flaechen(gpkg, "vg250_gem", {k[0]: k[1] for k in KOMMUNEN})
    for name, ags, gen in KOMMUNEN:
        if gem[name].gen != gen:  # type: ignore[attr-defined]
            raise SystemExit(f"VG250-Name für {ags}: {gem[name].gen!r}, erwartet {gen!r}")

    zeilen = []
    for name, ags, _gen in KOMMUNEN:
        fl = gem[name]
        bb = bbox_utm(gpkg, ags)
        for szen, ef, et in SZENARIEN:
            farben = [legendenfarben(e) for e in et]
            df, zf = ebene_verdichten(name, [(WMS_F, e) for e in ef], bb, None)
            dtf, zt = ebene_verdichten(name, [(WMS_T, e) for e in et], bb, farben)
            url_f = f"{WMS_F}?SERVICE=WMS&REQUEST=GetMap&LAYERS={','.join(ef)}"
            url_t = f"{WMS_T}?SERVICE=WMS&REQUEST=GetMap&LAYERS={','.join(et)}"
            zugriff = max(zf, zt)
            if df["pixel"] == 0:
                zeilen.append([name, szen, "keine", "0", "0", "nicht_kartiert", url_f, url_t, zugriff])
                print(f"{name:14s} {szen:9s} nicht kartiert", file=sys.stderr)
                continue
            zell = []
            kapp = 0
            for key, teile in df["zellen"].items():
                cx, cy = (int(v) for v in key.split(","))
                if not fl.enthaelt(cx + 50.0, cy + 50.0):
                    continue
                a = teile.get("f", 0) * PIXEL * PIXEL / (ZELLE * ZELLE)
                if a > 1.0:
                    kapp += 1
                    a = 1.0
                if a <= 0:
                    continue
                kl_fl = {float(k): v for k, v in dtf["zellen"].get(key, {}).items() if k != "n"}
                tief = sum(kl_fl.values())
                h = sum(k * v for k, v in kl_fl.items()) / tief if tief > 0 else None
                zell.append((f"CRS3035RES100mN{cy}E{cx}", a, h, kl_fl))
            if not zell:
                zeilen.append([name, szen, "keine", "0", "0", "nicht_ueberflutet", url_f, url_t, zugriff])
                print(f"{name:14s} {szen:9s} nicht überflutet ({df['pixel']} Pixel im Rechteck)",
                      file=sys.stderr)
                continue
            gesamt_kl: dict[float, float] = {}
            for *_, kl_fl in zell:
                for k, v in kl_fl.items():
                    gesamt_kl[k] = gesamt_kl.get(k, 0.0) + v
            median = _median_klasse(gesamt_kl)
            stat = {"karte": 0, "fallback_kommune": 0}
            for gid, a, h, _ in sorted(zell):
                if h is not None:
                    herk = "karte"
                elif median is not None:
                    h, herk = median, "fallback_kommune"
                else:
                    raise SystemExit(
                        f"{name} {szen}: Zellen ohne Tiefe und keine Kartentiefe in der Kommune — "
                        "fallback_land verlangt eine amtlich veröffentlichte Klassenverteilung "
                        "Bayerns, die nicht vorliegt. Eskalieren, nichts erfinden.")
                stat[herk] += 1
                zeilen.append([name, szen, gid, f"{a:.6f}", f"{h:.4f}", herk, url_f, url_t, zugriff])
            summe = sum(z[1] for z in zell) * ZELLE * ZELLE / 1e6
            print(f"{name:14s} {szen:9s} Zellen {len(zell):6d} {stat} gekappt {kapp} "
                  f"Fläche {summe:7.3f} km²  Median-Klasse {median}  "
                  f"Tiefe unklassiert {dtf['unklassiert']}", file=sys.stderr)

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
