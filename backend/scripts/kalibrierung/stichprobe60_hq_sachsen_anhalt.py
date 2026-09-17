#!/usr/bin/env python3
"""
Stichprobe #60: Überflutungsanteil a_{z,s} und Wassertiefe h_{z,s} je 100-m-Zelle
aus den Hochwassergefahrenkarten Sachsen-Anhalt für Halle (Saale).

Modellkontext (docs/methodik/60_gebaeudeschaeden_flusshochwasser.md, §3.2)
--------------------------------------------------------------------------
Datenebenen HQ_FLAECHE und HQ_TIEFE. Datenpaket für den Stichprobenlauf der
Kernformel (Vorhaben T-0284); es schließt keinen Befund. Bericht, Ledger und
Evidenz-Register werden nur gelesen.

Ausgabe
-------
  docs/evidenz/60_stichprobe/hq_sachsen_anhalt.csv   (UTF-8, Trennzeichen ';')
  kommune;szenario;gitter_id;a_anteil;h_m;h_herkunft;quelle_flaeche_url;quelle_tiefe_url;zugriff

Datenquelle (ohne Schlüssel, ohne Konto) — Vektor-Download, keine WMS-Karte
---------------------------------------------------------------------------
Hochwassergefahrenkarten nach § 74 WHG des Landesbetriebs für Hochwasserschutz und
Wasserwirtschaft Sachsen-Anhalt (LHW), GeoFachDatenServer Sachsen-Anhalt
(verlinkt von https://lhw.sachsen-anhalt.de/service/hochwasserkarten). Kostenfreier
Download der Wassertiefenklassen als Shapefile in 10-km-Kacheln (EPSG:25832) nach
Zustimmung zu den Nutzungsbedingungen (Parameter confirm=true, ohne Anmeldung):
  HQhäufig ← https://www.geofachdatenserver.de/de/hochwassergefahrenkarte-hq10-download.html
             (Szenario „hohe Wahrscheinlichkeit“ = HQ10, an der Elbe HQ20; Datei wt_max10_*)
  HQ100    ← https://www.geofachdatenserver.de/de/hochwassergefahrenkarte-hq100-download.html
             (Datei wt_max100_*)
  HQextrem ← https://www.geofachdatenserver.de/de/hochwassergefahrenkarte-hq200-download.html
             (Szenario „niedrige Wahrscheinlichkeit“ = HQ200 ohne Hochwasserschutzanlagen;
             die Seite …-hqextrem-download.html verlangt eine Anmeldung, die Karte
             „Hochwasser mit niedriger Wahrscheinlichkeit“ verlinkt auf …-hq200-download.html)
Die Auswahlkacheln stehen als GeoJSON in der Downloadseite; eine Kachel wird über
  https://www.geofachdatenserver.de/de/mod/4,212,500/ajax/1/prepare/?confirm=true&items=<id>&format=zip
angefordert (Antwort: Link auf das ZIP). Stand der Daten laut Attribut „Stand“: 2025-11-21.
Da die Tiefenklassen-Polygone die Überflutungsfläche vollständig abdecken, ist dieselbe
Datei Quelle für Fläche und Tiefe (quelle_flaeche_url = quelle_tiefe_url = Downloadseite).
Nutzungsbedingungen: https://www.geofachdatenserver.de/de/nutzungshinweise-download.html
(im ZIP als 673_nutzungshinweis_stand_01_2015.pdf).

Attribut „Klasse“ (1–5) → Tiefenklasse
--------------------------------------
Die Polygone entstehen per RasterToPolygon aus einem 1-m-Raster (Metadaten im .shp.xml;
Stützpunktabstand 1 m). Die Bedeutung der Codes steht nicht in den Metadaten; sie folgt
den fünf Intensitätsklassen des LHW („Je dunkler der Blauton, desto größer die
Wassertiefe“, https://www.geofachdatenserver.de/de/lhw-informationen-karteninhalte.html)
und wurde am 17.09.2026 gegen die Darstellung des WebGIS geprüft: GetMap der Ebene
lhw_hwrmrl_wt_hq100 in einem Punkt im Inneren eines Polygons Klasse 5 (UTM32 704971/5707734)
zeigt RGB (0, 49, 202), in Klasse 3 (703524/5702044) RGB (101, 151, 253) — höhere Klasse,
dunklerer Blauton. Zuordnung (Klassenmittel LAWA 2024, Untergrenze der offenen Klasse):
  1: 0–0,5 m → 0,25 · 2: >0,5–1 m → 0,75 · 3: >1–2 m → 1,5 · 4: >2–4 m → 3,0 · 5: >4 m → 4,0
Modellgrenze: Die Zuordnung 1/2/4 ist aus der Reihenfolge erschlossen, nicht einzeln
gegen die Legende gemessen.

Regeln (§3.2)
-------------
* Zelle: 100 m × 100 m in EPSG:3035, Kennung 'CRS3035RES100mN<y0>E<x0>' wie
  backend/app/services/zensus_loader.py.
* a = überflutete Teilfläche / 10 000 m² (Summe aller Klassenpolygone in der Zelle;
  Überlappung an Kachelrändern wird bei 1 gekappt, Zahl im Lauf ausgegeben).
* h = flächengewichtetes Mittel der Klassenmittel über den überfluteten Teil der Zelle.
* Ersatz ohne Tiefe: fallback_kommune = Klassenmittel der flächengewichteten
  Median-Klasse der Kommune im selben Szenario; fehlt sie, bricht der Lauf ab
  (für Sachsen-Anhalt ist keine amtliche Klassenverteilung hinterlegt; nichts erfinden).
  Da jede Fläche aus einem Klassenpolygon stammt, tritt der Ersatz hier nicht auf.
* Zuschnitt: Mittelpunkt der Zelle in der Gemeindefläche aus VG250 (BKG, jüngster Stand,
  Download und Punkt-in-Polygon aus stichprobe60_zensus.py).
* Markierungen: Karte vorhanden, keine überflutete Zelle → eine Zeile 'keine', 0, 0,
  nicht_ueberflutet; keine Kachel der Downloadseite schneidet die Gemeinde oder keine
  Kachel enthält Polygone → nicht_kartiert.

Umsetzung
---------
Shapefile (Typ 5, Polygon) wird mit struct gelesen; Ringe außerhalb des
Begrenzungsrechtecks der Gemeinde werden verworfen, die übrigen Stützpunkte mit den
Formeln aus stichprobe60_zensus.py von EPSG:25832 nach EPSG:3035 gerechnet und mit dem
Gitterverschnitt aus stichprobe60_hq_sachsen.py (Sutherland–Hodgman, Gaußsche
Trapezformel mit Vorzeichen; Shapefile-Außenringe im Uhrzeigersinn) je Zelle verdichtet.

Schutz gegen vertauschte Szenarien (Nacharbeit R1)
-------------------------------------------------
Jede Szenarioseite hat einen eigenen Download-Endpunkt; die Kachel-IDs sind auf allen
Seiten gleich. Der erste Lauf forderte alle Szenarien über den HQ100-Endpunkt an und
schrieb drei identische Blöcke. Deshalb: (a) die Shapefile-Namen im ZIP müssen zum
Szenario passen (wt_max10_ / wt_max100_ / wt_max200_); (b) der verdichtete
Zwischenstand trägt Szenario und Dateinamen und wird beim Laden dagegen geprüft;
(c) Abbruch, wenn zwei Szenarien dieselben Zellen mit denselben Anteilen und Tiefen
liefern oder nicht Fläche(HQhäufig) ≤ Fläche(HQ100) ≤ Fläche(HQextrem) mit
Fläche(HQhäufig) < Fläche(HQextrem) gilt.

Ressourcen-Regel §3.4
---------------------
Nur die 10-km-Kacheln, die das Begrenzungsrechteck der Gemeinde schneiden; nur Ringe in
diesem Rechteck. Rohdaten (ZIP je Kachel) und die verdichteten Zellflächen je Szenario
liegen in backend/.cache/60_stichprobe/ (gitignored); vorhandene Dateien werden
wiederverwendet, zugriff = Dateidatum.

Aufruf
------
  python3 backend/scripts/kalibrierung/stichprobe60_hq_sachsen_anhalt.py
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import re
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
OUT = os.path.join(REPO, "docs", "evidenz", "60_stichprobe", "hq_sachsen_anhalt.csv")
BASIS = "https://www.geofachdatenserver.de/de/"
ZELLE = 100.0

KOMMUNEN = [("Halle (Saale)", "15002000", "Halle (Saale)")]
# Szenario → Kennung der Downloadseite
SZENARIEN = [("HQhäufig", "hq10"), ("HQ100", "hq100"), ("HQextrem", "hq200")]
KLASSEN = {1: 0.25, 2: 0.75, 3: 1.5, 4: 3.0, 5: 4.0}


def seite_url(kennung: str) -> str:
    return f"{BASIS}hochwassergefahrenkarte-{kennung}-download.html"


def _get(url: str) -> bytes:
    for versuch in range(5):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": zs.USER_AGENT})
            with urllib.request.urlopen(req, timeout=600) as r:
                return r.read()
        except Exception as e:  # noqa: BLE001 — Netz/Dienstfehler: wiederholen
            if versuch == 4:
                raise
            print(f"  Wiederholung ({e})", file=sys.stderr)
            time.sleep(10 * (versuch + 1))
    raise AssertionError


def _cache_datei(name: str, url_fn) -> str:
    pfad = os.path.join(CACHE, name)
    if not (os.path.isfile(pfad) and os.path.getsize(pfad) > 0):
        os.makedirs(CACHE, exist_ok=True)
        daten = _get(url_fn())
        with open(pfad + ".tmp", "wb") as f:
            f.write(daten)
        os.replace(pfad + ".tmp", pfad)
    return pfad


def kacheln(kennung: str) -> tuple[str, list[tuple[str, str, tuple[float, float, float, float]]]]:
    """Download-Endpunkt der Seite und (id, label, bbox EPSG:25832) aller Auswahlkacheln."""
    pfad = _cache_datei(f"hq_st_seite_{kennung}.html", lambda: seite_url(kennung))
    with open(pfad, encoding="utf-8") as f:
        text = f.read()
    if "MapDownloadSelector" not in text:
        raise SystemExit(f"{seite_url(kennung)}: kein Kartendownloader (Anmeldung verlangt?)")
    # Jede Szenarioseite hat ihren eigenen Endpunkt (hq10 4,214 · hq100 4,212 · hq200 4,210);
    # die Kachel-IDs sind über die Seiten gleich.
    ep = set(re.findall(r"'(https://www\.geofachdatenserver\.de/de/mod/[\d,]+/ajax/1/prepare/\?)'", text))
    if len(ep) != 1:
        raise SystemExit(f"{seite_url(kennung)}: Download-Endpunkt nicht eindeutig {ep}")
    out = []
    for m in re.finditer(r'"bbox":\[([-\d.,]+)\].*?"properties": \{"id": "(\d+)","label": "([^"]+)"\}', text):
        bb = tuple(float(v) for v in m.group(1).split(","))
        out.append((m.group(2), m.group(3), bb))
    return ep.pop(), out


DATEI = {"hq10": "wt_max10_", "hq100": "wt_max100_", "hq200": "wt_max200_"}


def kachel_zip(kennung: str, endpunkt: str, kid: str, label: str) -> str:
    def link() -> str:
        antwort = _get(f"{endpunkt}confirm=true&items={kid}&format=zip").decode("utf-8").strip()
        if not antwort.startswith("http"):
            raise SystemExit(f"Download {kennung} {label}: unerwartete Antwort {antwort[:200]!r}")
        print(f"  Lade {kennung} {label}", file=sys.stderr)
        return antwort
    pfad = _cache_datei(f"hq_st_kachel_{kennung}_{label}.zip", link)
    with zipfile.ZipFile(pfad) as z:
        shp = [n for n in z.namelist() if n.lower().endswith(".shp")]
    if shp and not all(os.path.basename(n).startswith(DATEI[kennung]) for n in shp):
        raise SystemExit(f"{pfad}: Datei {shp} passt nicht zum Szenario {kennung}")
    return pfad


def shp_lesen(zip_pfad: str):
    """Liefert [(klasse, [ring, …])] mit Ringen in EPSG:25832."""
    with zipfile.ZipFile(zip_pfad) as z:
        namen = z.namelist()
        shp = next((n for n in namen if n.lower().endswith(".shp")), None)
        if shp is None:
            return []
        s = z.read(shp)
        d = z.read(shp[:-4] + ".dbf")
    n, hl, rl = struct.unpack("<xxxxIHH", d[:12])
    felder, i, off = {}, 32, 1
    while d[i] != 13:
        name = d[i:i + 11].split(b"\0")[0].decode()
        laenge = d[i + 16]
        felder[name] = (off, laenge)
        off += laenge
        i += 32
    ko, kl = felder["Klasse"]
    klassen = [int(d[hl + r * rl + ko:hl + r * rl + ko + kl]) for r in range(n)]
    out, pos, r = [], 100, 0
    while pos < len(s):
        _, clen = struct.unpack(">ii", s[pos:pos + 8])
        rec = s[pos + 8:pos + 8 + clen * 2]
        pos += 8 + clen * 2
        typ = struct.unpack("<i", rec[:4])[0]
        klasse = klassen[r]
        r += 1
        if typ != 5:
            continue
        npart, npt = struct.unpack("<ii", rec[36:44])
        idx = list(struct.unpack(f"<{npart}i", rec[44:44 + 4 * npart])) + [npt]
        o = 44 + 4 * npart
        xy = struct.unpack(f"<{2 * npt}d", rec[o:o + 16 * npt])
        ringe = [[(xy[2 * j], xy[2 * j + 1]) for j in range(idx[p], idx[p + 1])] for p in range(npart)]
        out.append((klasse, ringe))
    return out


def bbox_utm(gpkg: str, ags: str) -> tuple[float, float, float, float]:
    con = sqlite3.connect(gpkg)
    geomcol = con.execute(
        "SELECT column_name FROM gpkg_geometry_columns WHERE table_name = 'vg250_gem'").fetchone()[0]
    xs, ys = [], []
    for (blob,) in con.execute(f"SELECT {geomcol} FROM vg250_gem WHERE AGS = ? AND GF = 4", (ags,)):
        for ring in zs._parse_wkb(zs._gpkg_wkb(blob)):
            xs += [p[0] for p in ring]
            ys += [p[1] for p in ring]
    con.close()
    return min(xs) - 200, min(ys) - 200, max(xs) + 200, max(ys) + 200


def szenario_verdichten(kommune: str, kennung: str, bb) -> tuple[dict, str]:
    """{'kacheln': n, 'polygone': n, 'zellen': {'x0,y0': {klasse: fläche}}}, zugriff."""
    pfad = os.path.join(CACHE, f"hq_st_zellen_{kommune.split()[0]}_{kennung}.json")
    if os.path.isfile(pfad):
        with open(pfad, encoding="utf-8") as f:
            erg = json.load(f)
        # Zwischenstand nur verwenden, wenn er nachweislich aus den Dateien dieses Szenarios stammt
        dateien = erg.get("dateien")
        if (erg.get("kennung") != kennung or not isinstance(dateien, list)
                or (erg.get("polygone") and not dateien)
                or not all(os.path.basename(n).startswith(DATEI[kennung]) for n in dateien)):
            raise SystemExit(f"{pfad}: Zwischenstand gehört nicht zum Szenario {kennung} "
                             f"(kennung {erg.get('kennung')!r}, dateien {dateien!r}) — Datei löschen, neu laufen")
        return erg, zs._zugriff(pfad)
    x0, y0, x1, y1 = bb
    endpunkt, alle = kacheln(kennung)
    treffer = [k for k in alle
               if k[2][0] < x1 and k[2][2] > x0 and k[2][1] < y1 and k[2][3] > y0]
    zellen: dict[str, dict[str, float]] = {}
    polygone = 0
    dateien: list[str] = []
    for kid, label, _ in sorted(treffer, key=lambda k: k[1]):
        zpfad = kachel_zip(kennung, endpunkt, kid, label)
        with zipfile.ZipFile(zpfad) as z:
            dateien += [n for n in z.namelist() if n.lower().endswith(".shp")]
        for klasse, ringe in shp_lesen(zpfad):
            if klasse not in KLASSEN:
                raise SystemExit(f"{kennung} {label}: unbekannte Klasse {klasse}")
            roh: dict = {}
            for ring in ringe:
                xs = [p[0] for p in ring]
                ys = [p[1] for p in ring]
                if max(xs) < x0 or min(xs) > x1 or max(ys) < y0 or min(ys) > y1:
                    continue
                pts = [zs.utm32_to_3035(e, n) for e, n in ring]
                if len(pts) > 1 and pts[0] == pts[-1]:
                    pts = pts[:-1]
                sn.ring_zellflaechen(pts, roh)
                polygone += 1
            for (cx, cy), fl in roh.items():
                fl = -fl  # Shapefile: Außenring im Uhrzeigersinn
                if fl <= 1e-6:
                    continue
                z = zellen.setdefault(f"{cx},{cy}", {})
                z[str(klasse)] = z.get(str(klasse), 0.0) + fl
        print(f"  {kommune} {kennung} {label}: {len(zellen)} Zellen", file=sys.stderr)
    erg = {"kennung": kennung, "dateien": sorted(dateien), "kacheln": len(treffer),
           "polygone": polygone, "bbox": list(bb), "zellen": zellen}
    os.makedirs(CACHE, exist_ok=True)
    with open(pfad + ".tmp", "w", encoding="utf-8") as f:
        json.dump(erg, f)
    os.replace(pfad + ".tmp", pfad)
    return erg, zs._zugriff(pfad)


def _selbsttest() -> None:
    # Uhrzeigersinn-Quadrat 150 × 150 m ab (50, 50) → negative Flächen je Zelle
    roh: dict = {}
    sn.ring_zellflaechen([(50, 50), (50, 200), (200, 200), (200, 50)], roh)
    assert abs(-roh[(0, 0)] - 2500) < 1e-6 and abs(-sum(roh.values()) - 22500) < 1e-6, roh


def plausibel(name: str, plausi: dict[str, tuple[float, frozenset]]) -> None:
    """Bricht ab, wenn Szenarien identisch sind oder die Flächen nicht mit der Seltenheit wachsen.

    Fehlerbild des ersten Laufs: alle drei Szenarien aus denselben HQ100-Kacheln.
    Verlangt: Fläche(HQhäufig) ≤ Fläche(HQ100) ≤ Fläche(HQextrem), nicht alle gleich,
    und keine zwei Szenarien mit denselben Zellen, Anteilen und Tiefen.
    """
    namen = [s for s, _ in SZENARIEN if s in plausi]
    for i, s1 in enumerate(namen):
        for s2 in namen[i + 1:]:
            if plausi[s1][1] and plausi[s1][1] == plausi[s2][1]:
                raise SystemExit(f"{name}: {s1} und {s2} liefern dieselben Zellen, Anteile und "
                                 "Tiefen — vermutlich dieselben Kacheln geladen; Cache prüfen.")
    fl = [plausi[s][0] if s in plausi else 0.0 for s, _ in SZENARIEN]
    if not (fl[0] <= fl[1] <= fl[2]) or fl[0] == fl[2]:
        raise SystemExit(f"{name}: Flächen je Szenario unplausibel "
                         + ", ".join(f"{s} {f:.3f} km²" for (s, _), f in zip(SZENARIEN, fl)))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 2)[1])
    ap.add_argument("--out", default=OUT)
    args = ap.parse_args()

    zs._selbsttest()
    sn._selbsttest_verschnitt()
    _selbsttest()

    gpkg = zs._extract(zs._download(zs.URL_VG250), "vg250", ".gpkg")
    gem = zs._lade_flaechen(gpkg, "vg250_gem", {k[0]: k[1] for k in KOMMUNEN})
    for name, ags, gen in KOMMUNEN:
        if gem[name].gen != gen:  # type: ignore[attr-defined]
            raise SystemExit(f"VG250-Name für {ags}: {gem[name].gen!r}, erwartet {gen!r}")

    zeilen = []
    for name, ags, _gen in KOMMUNEN:
        fl = gem[name]
        bb = bbox_utm(gpkg, ags)
        plausi: dict[str, tuple[float, frozenset]] = {}
        for szen, kennung in SZENARIEN:
            daten, zugriff = szenario_verdichten(name, kennung, bb)
            url = seite_url(kennung)
            if daten["kacheln"] == 0 or daten["polygone"] == 0:
                zeilen.append([name, szen, "keine", "0", "0", "nicht_kartiert", url, url, zugriff])
                print(f"{name} {szen}: nicht kartiert", file=sys.stderr)
                continue
            zell = []
            kapp = 0
            for key, teile in daten["zellen"].items():
                cx, cy = (int(float(v)) for v in key.split(","))
                if not fl.enthaelt(cx + 50.0, cy + 50.0):
                    continue
                a = sum(teile.values()) / (ZELLE * ZELLE)
                if a > 1.0:
                    kapp += 1
                    a = 1.0
                if a < 5e-7:
                    continue
                kl_fl = {KLASSEN[int(k)]: v for k, v in teile.items()}
                tief = sum(kl_fl.values())
                h = sum(k * v for k, v in kl_fl.items()) / tief if tief > 0 else None
                zell.append((f"CRS3035RES100mN{cy}E{cx}", a, h, kl_fl))
            if not zell:
                zeilen.append([name, szen, "keine", "0", "0", "nicht_ueberflutet", url, url, zugriff])
                print(f"{name} {szen}: nicht überflutet", file=sys.stderr)
                continue
            gesamt_kl: dict[float, float] = {}
            for *_, kl_fl in zell:
                for k, v in kl_fl.items():
                    gesamt_kl[k] = gesamt_kl.get(k, 0.0) + v
            median = sn._median_klasse(gesamt_kl)
            stat = {"karte": 0, "fallback_kommune": 0}
            for gid, a, h, _ in sorted(zell):
                if h is not None:
                    herk = "karte"
                elif median is not None:
                    h, herk = median, "fallback_kommune"
                else:
                    raise SystemExit(f"{name} {szen}: keine Kartentiefe in der Kommune — "
                                     "fallback_land ohne amtliche Klassenverteilung; eskalieren.")
                stat[herk] += 1
                zeilen.append([name, szen, gid, f"{a:.6f}", f"{h:.4f}", herk, url, url, zugriff])
            summe = sum(z[1] for z in zell) * ZELLE * ZELLE / 1e6
            plausi[szen] = (summe, frozenset((g, round(a, 6), round(h or 0.0, 4)) for g, a, h, _ in zell))
            print(f"{name} {szen:9s} Zellen {len(zell):6d} {stat} gekappt {kapp} "
                  f"Fläche {summe:7.3f} km²  Median-Klasse {median}  Kacheln {daten['kacheln']}",
                  file=sys.stderr)
        plausibel(name, plausi)

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
