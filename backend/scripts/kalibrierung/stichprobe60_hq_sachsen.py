#!/usr/bin/env python3
"""
Stichprobe #60: Überflutungsanteil a_{z,s} und Wassertiefe h_{z,s} je 100-m-Zelle
aus den Hochwassergefahrenkarten Sachsen für Grimma und Dresden.

Modellkontext (docs/methodik/60_gebaeudeschaeden_flusshochwasser.md, §3.2)
--------------------------------------------------------------------------
Datenebenen HQ_FLAECHE und HQ_TIEFE. Datenpaket für den Stichprobenlauf der
Kernformel (Vorhaben T-0284); es schließt keinen Befund. Bericht, Ledger und
Evidenz-Register werden nur gelesen.

Ausgabe
-------
  docs/evidenz/60_stichprobe/hq_sachsen.csv   (UTF-8, Trennzeichen ';')
  kommune;szenario;gitter_id;a_anteil;h_m;h_herkunft;quelle_flaeche_url;quelle_tiefe_url;zugriff

Datenquelle (ohne Schlüssel, ohne Konto)
----------------------------------------
Hochwassergefahrenkarten nach § 74 WHG, Freistaat Sachsen (LfULG, LUIS),
Kartendienst „hochwassergefaehrdung“ (Metadaten GeoMIS
https://geomis.sachsen.de/geomis-client/?lang=de#/datasets/iso/722b4ee6-eccb-46d6-864a-67333f1503d8
bzw. .../e744aa2d-f46f-4047-826a-ed095c987df7 für das Extremhochwasser).
Derselbe Dienst ist als WFS 2.0 angeboten
  https://luis.sachsen.de/arcgis/services/wasser/hochwassergefaehrdung/MapServer/WFSServer
und als ArcGIS-REST-Abfrageschnittstelle
  https://luis.sachsen.de/arcgis/rest/services/wasser/hochwassergefaehrdung/MapServer
Gelesen werden **Vektordaten** (Polygone mit Attribut Wassertiefenklasse) über die
REST-Abfrage desselben Dienstes (JSON statt GML, sonst identischer Inhalt; die Ebenen
tragen dort dieselben Namen wie im WFS). Keine WMS-Karte, keine Legendenfarben.
Ebenen und Szenariozuordnung:
  HQhäufig  ← Ebene 6  „Gefaehrdung_bei_HQ20_25“   (Fläche und Tiefenklasse WT_KLASSIF;
              Sachsen führt als häufiges Szenario HQ20 bzw. HQ25, T_KLASSIF)
  HQ100     ← Ebene 8  „Gefaehrdung_bei_HQ100“     (Fläche und Tiefenklasse)
  HQextrem  ← Fläche: Ebene 10 „Extremhochwasser“ (nur Ausdehnung, ohne Tiefenattribut;
              T_KLASSIF je Gewässerabschnitt HQ200, HQ300, HQE, „2 x HQ100“ …)
              Tiefe:  Ebene 9  „Gefaehrdung_bei_HQ200_300“ (Tiefenklassen), nur Polygone,
              die mit einem Extremhochwasser-Polygon derselben Zelle eine HWSK-Nummer
              teilen UND dasselbe T_KLASSIF tragen (d. h. die Tiefenkarte gehört zum
              selben Extremszenario desselben Gewässerabschnitts). Sonst gilt die Zelle
              als „ohne Tiefenangabe“ (Ersatzregel unten).
Kennung der Quelle in der CSV: quelle_flaeche_url / quelle_tiefe_url = REST-URL der
jeweiligen Ebene (…/MapServer/<id>).

Regeln (§3.2)
-------------
* Zelle: 100 m × 100 m in EPSG:3035, Kennung 'CRS3035RES100mN<y0>E<x0>' wie
  backend/app/services/zensus_loader.py (_gitter_id_from_row).
* a = überflutete Teilfläche / 10 000 m². Überlappen sich Polygone desselben
  Szenarios (zwei Gewässerabschnitte/HWSK mit gemeinsamer Mündungsfläche), wird die
  Summe bei 1 gekappt (Modellgrenze: Überlappungsfläche wird nicht als Vereinigung
  gerechnet; die Zahl gekappter Zellen wird im Lauf ausgegeben).
* h = flächengewichtetes Mittel der Klassenmittel über den überfluteten Teil der
  Zelle, Klassen nach LAWA 2024: 0–0,5 → 0,25 · >0,5–1 → 0,75 · >1–2 → 1,5 ·
  >2–4 → 3,0 · >4 → 4,0 (Untergrenze der offenen Klasse).
* Polygone mit HWS = „ja“ (hochwassergeschütztes Gebiet, Legende „… (hochwassergeschützt)“)
  gehören zur veröffentlichten Überflutungsfläche des Szenarios und werden mitgezählt.
  Modellgrenze: Die Fläche gilt damit als überflutet bei Versagen des Schutzes.
* Ersatz für a > 0 ohne Tiefe: h_herkunft = fallback_kommune = Klassenmittel der
  flächengewichteten Median-Tiefenklasse aller Zellen mit Kartentiefe derselben
  Kommune im selben Szenario; fehlt sie, fallback_land — für Sachsen ist keine
  amtlich veröffentlichte Klassenverteilung hinterlegt, der Lauf bricht dann ab
  (nichts erfinden, Eskalation).
* Zuschnitt: Zelle gehört zur Kommune, wenn ihr Mittelpunkt in der Gemeindefläche
  aus VG250 (BKG, Stand 01.01.2026, bereitgestellt 21.07.2026, dl-de/by-2-0) liegt;
  Download und Punkt-in-Polygon wie stichprobe60_zensus.py (wiederverwendet).
* Markierungen: keine überflutete Zelle bei vorhandener Karte → eine Zeile 'keine',
  0, 0, nicht_ueberflutet; liefert der Dienst im Rechteck der Kommune für die Ebene
  kein einziges Objekt → 'nicht_kartiert'.

Umsetzung ohne shapely/pyproj
-----------------------------
Wie bei T-0297 (Entscheidung des Supervisors, Option b) sind pyproj und shapely in der
Ausführungsumgebung nicht vorhanden. Umprojektion: der Dienst liefert die Geometrie
mit outSR=3035 (ETRS89-LAEA; Quelle EPSG:25833, gleiches Datum ETRS89, keine
Datumsverschiebung); VG250 wird mit den geprüften Formeln aus stichprobe60_zensus.py
nach EPSG:3035 gerechnet. Verschnitt: Polygonringe werden rekursiv an den 100-m-
Gitterlinien mit Sutherland–Hodgman gegen Halbebenen geteilt, bis ein Stück in genau
einer Zelle liegt; Fläche per Gaußscher Trapezformel mit Vorzeichen (Löcher ziehen
ab). Selbsttest in _selbsttest_verschnitt.

Ressourcen-Regel §3.4
---------------------
Kein Vollraster-Lauf: Abgefragt wird je Kommune und Ebene nur das Begrenzungsrechteck
der Gemeindefläche (EPSG:3035, räumlicher Filter beim Dienst), seitenweise nach
OBJECTID. Rohdaten: je Kommune und Ebene die verdichteten Zellflächen als JSON in
backend/.cache/60_stichprobe/ (gitignored); vorhandene Dateien werden
wiederverwendet, zugriff = Dateidatum.

Aufruf
------
  python3 backend/scripts/kalibrierung/stichprobe60_hq_sachsen.py
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import math
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stichprobe60_zensus as zs  # noqa: E402

REPO = zs.REPO
CACHE = zs.CACHE
OUT = os.path.join(REPO, "docs", "evidenz", "60_stichprobe", "hq_sachsen.csv")
REST = "https://luis.sachsen.de/arcgis/rest/services/wasser/hochwassergefaehrdung/MapServer"
ZELLE = 100.0

KOMMUNEN = [("Grimma", "14729160", "Grimma"), ("Dresden", "14612000", "Dresden")]
# Szenario → (Flächenebene, Tiefenebene)
SZENARIEN = [("HQhäufig", 6, 6), ("HQ100", 8, 8), ("HQextrem", 10, 9)]
FELDER = "OBJECTID,HWSK,T_KLASSIF,WT_KLASSIF"
FELDER_OHNE_TIEFE = "OBJECTID,HWSK,T_KLASSIF"

# Untergrenze der Klasse → Klassenmittel (LAWA 2024)
KLASSEN = {0.0: 0.25, 0.5: 0.75, 1.0: 1.5, 2.0: 3.0, 4.0: 4.0}


def klassenmittel(txt: str | None) -> float | None:
    if not txt:
        return None
    zahlen = re.findall(r"\d+(?:,\d+)?", txt)
    if not zahlen:
        return None
    unten = float(zahlen[0].replace(",", "."))
    return KLASSEN.get(unten)


# ---------------------------------------------------------------------------
# Verschnitt Polygon × 100-m-Gitter
# ---------------------------------------------------------------------------

def _clip(ring, achse: int, wert: float, unten: bool):
    """Sutherland–Hodgman gegen Halbebene koord[achse] <= wert (unten) bzw. >= wert."""
    out = []
    n = len(ring)
    if n == 0:
        return out
    prev = ring[-1]
    pin = (prev[achse] <= wert) if unten else (prev[achse] >= wert)
    for cur in ring:
        cin = (cur[achse] <= wert) if unten else (cur[achse] >= wert)
        if cin != pin:
            t = (wert - prev[achse]) / (cur[achse] - prev[achse])
            p = (prev[0] + t * (cur[0] - prev[0]), prev[1] + t * (cur[1] - prev[1]))
            out.append((wert, p[1]) if achse == 0 else (p[0], wert))
        if cin:
            out.append(cur)
        prev, pin = cur, cin
    return out


def _flaeche(ring) -> float:
    s = 0.0
    x1, y1 = ring[-1]
    for x2, y2 in ring:
        s += x1 * y2 - x2 * y1
        x1, y1 = x2, y2
    return s / 2.0


def ring_zellflaechen(ring, ziel: dict) -> None:
    """Addiert die vorzeichenbehaftete Fläche des Rings je Zelle (x0, y0) zu ziel."""
    stapel = [ring]
    while stapel:
        r = stapel.pop()
        if len(r) < 3:
            continue
        xs = [p[0] for p in r]
        ys = [p[1] for p in r]
        cx0 = math.floor(min(xs) / ZELLE)
        cx1 = math.ceil(max(xs) / ZELLE) - 1
        cy0 = math.floor(min(ys) / ZELLE)
        cy1 = math.ceil(max(ys) / ZELLE) - 1
        if cx1 < cx0:
            cx1 = cx0
        if cy1 < cy0:
            cy1 = cy0
        if cx0 == cx1 and cy0 == cy1:
            a = _flaeche(r)
            if a:
                k = (int(cx0 * ZELLE), int(cy0 * ZELLE))
                ziel[k] = ziel.get(k, 0.0) + a
            continue
        if cx1 - cx0 >= cy1 - cy0:
            achse, schnitt = 0, ((cx0 + cx1 + 1) // 2) * ZELLE
        else:
            achse, schnitt = 1, ((cy0 + cy1 + 1) // 2) * ZELLE
        stapel.append(_clip(r, achse, schnitt, True))
        stapel.append(_clip(r, achse, schnitt, False))


def polygon_zellflaechen(rings) -> dict:
    roh: dict = {}
    for ring in rings:
        pts = [(float(p[0]), float(p[1])) for p in ring]
        if len(pts) > 1 and pts[0] == pts[-1]:
            pts = pts[:-1]
        ring_zellflaechen(pts, roh)
    gesamt = sum(roh.values())
    vz = -1.0 if gesamt < 0 else 1.0
    return {k: v * vz for k, v in roh.items() if v * vz > 1e-6}


def _selbsttest_verschnitt() -> None:
    # Quadrat 150 × 150 m ab (50, 50): 2500 / 5000 / 5000 / 10 000 m²
    q = [[(50, 50), (200, 50), (200, 200), (50, 200), (50, 50)]]
    f = polygon_zellflaechen(q)
    soll = {(0, 0): 2500, (100, 0): 5000, (0, 100): 5000, (100, 100): 10000}
    assert set(f) == set(soll) and all(abs(f[k] - soll[k]) < 1e-6 for k in soll), f
    # Uhrzeigersinn (Esri) mit Loch 20 × 20 m in Zelle (100, 100)
    q = [[(50, 50), (50, 200), (200, 200), (200, 50), (50, 50)],
         [(120, 120), (140, 120), (140, 140), (120, 140), (120, 120)]]
    f = polygon_zellflaechen(q)
    assert abs(f[(100, 100)] - 9600) < 1e-6 and abs(sum(f.values()) - 22100) < 1e-6, f
    # konkaves U über drei Zellen: Gesamtfläche bleibt erhalten
    u = [[(10, 10), (290, 10), (290, 90), (210, 90), (210, 30), (90, 30), (90, 90), (10, 90)]]
    f = polygon_zellflaechen(u)
    assert abs(sum(f.values()) - (280 * 80 - 120 * 60)) < 1e-6, f
    assert abs(f[(100, 0)] - 100 * 20) < 1e-6, f
    assert klassenmittel("> 0,5-1,0 m") == 0.75 and klassenmittel("0-0,5 m") == 0.25
    assert klassenmittel("> 4,0 m") == 4.0 and klassenmittel(">2-4") == 3.0


# ---------------------------------------------------------------------------
# Abruf und Verdichtung je Kommune und Ebene
# ---------------------------------------------------------------------------

def _get_json(url: str, params: dict) -> dict:
    daten = urllib.parse.urlencode(params).encode()
    for versuch in range(5):
        try:
            req = urllib.request.Request(url, data=daten, headers={"User-Agent": zs.USER_AGENT})
            with urllib.request.urlopen(req, timeout=600) as r:
                d = json.loads(r.read().decode("utf-8"))
            if "error" in d:
                raise RuntimeError(d["error"])
            return d
        except Exception as e:  # noqa: BLE001 — Netz/Dienstfehler: wiederholen
            if versuch == 4:
                raise
            print(f"  Wiederholung ({e})", file=sys.stderr)
            time.sleep(10 * (versuch + 1))
    raise AssertionError


def ebene_verdichten(kommune: str, ebene: int, bbox) -> tuple[dict, str]:
    """Liefert ({'anzahl': n, 'zellen': {'x0,y0': {'hwsk|tk|klasse': fläche}}}, zugriff)."""
    pfad = os.path.join(CACHE, f"hq_sn_{kommune}_{ebene}.json")
    if os.path.isfile(pfad):
        with open(pfad, encoding="utf-8") as f:
            return json.load(f), zs._zugriff(pfad)
    x0, y0, x1, y1 = bbox
    felder = FELDER_OHNE_TIEFE if ebene == 10 else FELDER
    zellen: dict[str, dict[str, float]] = {}
    anzahl, offset, seite = 0, 0, 1000
    while True:
        d = _get_json(f"{REST}/{ebene}/query", {
            "where": "1=1", "geometry": f"{x0},{y0},{x1},{y1}",
            "geometryType": "esriGeometryEnvelope", "inSR": "3035", "outSR": "3035",
            "spatialRel": "esriSpatialRelIntersects", "outFields": felder,
            "returnGeometry": "true", "geometryPrecision": "2",
            "orderByFields": "OBJECTID", "resultOffset": str(offset),
            "resultRecordCount": str(seite), "f": "json",
        })
        feats = d.get("features", [])
        for ft in feats:
            at = ft["attributes"]
            geom = ft.get("geometry") or {}
            if not geom.get("rings"):
                continue
            kl = klassenmittel(at.get("WT_KLASSIF")) if ebene != 10 else None
            schl = f"{at.get('HWSK') or ''}|{at.get('T_KLASSIF') or ''}|{'' if kl is None else kl}"
            for (cx, cy), fl in polygon_zellflaechen(geom["rings"]).items():
                if not (x0 - ZELLE <= cx <= x1 and y0 - ZELLE <= cy <= y1):
                    continue
                z = zellen.setdefault(f"{cx},{cy}", {})
                z[schl] = z.get(schl, 0.0) + fl
        anzahl += len(feats)
        offset += len(feats)
        if offset % 20000 < seite:
            print(f"  {kommune} Ebene {ebene}: {anzahl} Objekte", file=sys.stderr)
        if not feats or not d.get("exceededTransferLimit"):
            break
    erg = {"anzahl": anzahl, "bbox": list(bbox), "zellen": zellen}
    os.makedirs(CACHE, exist_ok=True)
    with open(pfad + ".tmp", "w", encoding="utf-8") as f:
        json.dump(erg, f)
    os.replace(pfad + ".tmp", pfad)
    return erg, zs._zugriff(pfad)


def _hwsk(s: str) -> set[str]:
    return {t.strip() for t in s.split("/") if t.strip()}


def _median_klasse(flaechen: dict[float, float]) -> float | None:
    gesamt = sum(flaechen.values())
    if gesamt <= 0:
        return None
    lauf = 0.0
    for kl in sorted(flaechen):
        lauf += flaechen[kl]
        if lauf >= gesamt / 2:
            return kl
    return max(flaechen)


# ---------------------------------------------------------------------------
# Hauptablauf
# ---------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 2)[1])
    ap.add_argument("--out", default=OUT)
    args = ap.parse_args()

    zs._selbsttest()
    _selbsttest_verschnitt()

    gpkg = zs._extract(zs._download(zs.URL_VG250), "vg250", ".gpkg")
    gem = zs._lade_flaechen(gpkg, "vg250_gem", {k[0]: k[1] for k in KOMMUNEN})
    for name, ags, gen in KOMMUNEN:
        if gem[name].gen != gen:  # type: ignore[attr-defined]
            raise SystemExit(f"VG250-Name für {ags}: {gem[name].gen!r}, erwartet {gen!r}")

    auftraege = sorted({(k[0], e) for k in KOMMUNEN for _, ef, et in SZENARIEN for e in (ef, et)})
    with ThreadPoolExecutor(max_workers=3) as pool:
        futs = {a: pool.submit(ebene_verdichten, a[0], a[1], gem[a[0]].bbox) for a in auftraege}
        daten = {a: f.result() for a, f in futs.items()}

    zeilen = []
    for name, _ags, _gen in KOMMUNEN:
        fl = gem[name]
        for szen, ef, et in SZENARIEN:
            (df, zf), (dt_, zt) = daten[(name, ef)], daten[(name, et)]
            url_f, url_t = f"{REST}/{ef}", f"{REST}/{et}"
            zugriff = max(zf, zt)
            zell: list[tuple[str, float, float | None]] = []  # gid, a, h
            kapp = 0
            for key, teile in df["zellen"].items():
                cx, cy = (int(v) for v in key.split(","))
                if not fl.enthaelt(cx + 50.0, cy + 50.0):
                    continue
                flut = sum(teile.values())
                a = flut / (ZELLE * ZELLE)
                if a > 1.0:
                    kapp += 1
                    a = 1.0
                if a < 5e-7:
                    continue
                kl_fl: dict[float, float] = {}
                if ef == et:
                    for s, v in teile.items():
                        k = s.split("|")[2]
                        if k:
                            kl_fl[float(k)] = kl_fl.get(float(k), 0.0) + v
                else:
                    ext = [(_hwsk(s.split("|")[0]), s.split("|")[1]) for s in teile]
                    for s, v in dt_["zellen"].get(key, {}).items():
                        hw, tk, k = s.split("|")
                        if k and any(tk == etk and _hwsk(hw) & ehw for ehw, etk in ext):
                            kl_fl[float(k)] = kl_fl.get(float(k), 0.0) + v
                tief = sum(kl_fl.values())
                h = sum(k * v for k, v in kl_fl.items()) / tief if tief > 0 else None
                zell.append((f"CRS3035RES100mN{cy}E{cx}", a, h, kl_fl))
            if df["anzahl"] == 0:
                zeilen.append([name, szen, "keine", "0", "0", "nicht_kartiert", url_f, url_t, zugriff])
                print(f"{name:8s} {szen:9s} nicht kartiert", file=sys.stderr)
                continue
            if not zell:
                zeilen.append([name, szen, "keine", "0", "0", "nicht_ueberflutet", url_f, url_t, zugriff])
                print(f"{name:8s} {szen:9s} nicht überflutet ({df['anzahl']} Objekte im Rechteck)",
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
                        "Sachsens, die nicht vorliegt. Eskalieren, nichts erfinden.")
                stat[herk] += 1
                zeilen.append([name, szen, gid, f"{a:.6f}", f"{h:.4f}", herk, url_f, url_t, zugriff])
            summe = sum(z[1] for z in zell) * ZELLE * ZELLE / 1e6
            print(f"{name:8s} {szen:9s} Zellen {len(zell):6d} {stat} gekappt {kapp} "
                  f"Fläche {summe:7.3f} km²  Median-Klasse {median}  Objekte {df['anzahl']}",
                  file=sys.stderr)

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
