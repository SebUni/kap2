"""Anlage für Stufe 2 der Ersatzregel 65+ (Bericht #95 §3.3, Log 41, Befund 116).

Liest aus der Zensus-2022-Regionaltabelle „Demografie“ [69] (Blatt „CSV-Demografie“) je Gemeinde
und je Kreis die Einwohner insgesamt, die Gruppe 60–66 und die Einwohner ab 67 (67–74 + 75 und
älter) und schreibt sie nach ``backend/data/kalibrierung/zensus2022_demografie_ab65.csv``.

Schlüssel: Gemeinde = AGS (8 Stellen, aus dem ARS: Stellen 1–5 und 10–12), Kreis = Kreisschlüssel
(5 Stellen). Zeichen nach der Zeichenerklärung von [69]: „–“ = genau null (zählt als 0), „.“ =
unbekannt oder geheim (Zeile ohne Werte; der Loader fällt dann auf die Kreiszeile zurück).
Dieselbe Lesart wie ``docs/methodik/anlagen/95_zellvergleich.py`` (``zensus_demografie``).

Aufruf (aus dem Repo-Wurzelverzeichnis):
    python3 backend/scripts/zensus_demografie_ab65.py [--xlsx PFAD]
Ohne ``--xlsx`` wird die Tabelle von destatis.de geladen.
"""
from __future__ import annotations

import argparse
import csv
import re
import tempfile
import urllib.request
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

DEMOGRAFIE_URL = "https://www.destatis.de/static/DE/zensus/gitterdaten/Regionaltabelle_Demografie.xlsx"
KREISEBENE = "Stadtkreis/kreisfreie Stadt/Landkreis"
ZIEL = Path(__file__).resolve().parents[1] / "data" / "kalibrierung" / "zensus2022_demografie_ab65.csv"

_NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
_REL = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"


def lies_regionaltabelle(xlsx: Path) -> list[tuple[str, str, float | None, float | None, float | None]]:
    """Zeilen (schluessel, ebene, insgesamt, g60_66, ab67) aus dem Blatt „CSV-Demografie“ von [69]."""
    z = zipfile.ZipFile(xlsx)
    texte = ["".join(t.text or "" for t in si.iter(_NS + "t"))
             for si in ET.fromstring(z.read("xl/sharedStrings.xml")).iter(_NS + "si")]
    rid = next(s.get(_REL) for s in ET.fromstring(z.read("xl/workbook.xml")).iter(_NS + "sheet")
               if s.get("name") == "CSV-Demografie")
    ziel = next(r.get("Target") for r in ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
                if r.get("Id") == rid)
    kopf, zeilen = None, []
    for _, el in ET.iterparse(z.open("xl/" + ziel.lstrip("/").removeprefix("xl/"))):
        if el.tag != _NS + "row":
            continue
        zeile = {}
        for c in el.iter(_NS + "c"):
            v = c.find(_NS + "v")
            wert = "" if v is None else (texte[int(v.text)] if c.get("t") == "s" else v.text)
            zeile[re.match(r"[A-Z]+", c.get("r")).group()] = wert
        el.clear()
        if kopf is None:
            kopf = {name: sp for sp, name in zeile.items()}
            continue
        ebene = zeile.get(kopf["Regionalebene"])
        if ebene not in ("Gemeinde", KREISEBENE):
            continue

        def zahl(name):
            w = zeile.get(kopf[name], "").strip()
            return 0.0 if w == "–" else (float(w) if w.isdigit() else None)
        ges, g60, g67, g75 = (zahl(n) for n in ("0_Insgesamt_", "Alter_infr__09", "Alter_infr__10",
                                                 "Alter_infr__11"))
        ars = zeile[kopf["_RS"]]
        ok = None not in (ges, g60, g67, g75) and ges > 0
        schluessel = ars[:5] + ars[9:] if ebene == "Gemeinde" else ars[:5]
        zeilen.append((schluessel, "gemeinde" if ebene == "Gemeinde" else "kreis",
                       ges if ok else None, g60 if ok else None, (g67 + g75) if ok else None))
    return zeilen


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--xlsx", help="lokale Kopie der Regionaltabelle Demografie [69]")
    args = ap.parse_args()
    if args.xlsx:
        xlsx = Path(args.xlsx)
    else:
        xlsx = Path(tempfile.mkdtemp()) / "Regionaltabelle_Demografie.xlsx"
        urllib.request.urlretrieve(DEMOGRAFIE_URL, xlsx)
    zeilen = sorted(lies_regionaltabelle(xlsx), key=lambda r: (r[1], r[0]))

    def fmt(v):
        return "" if v is None else str(int(v))
    with open(ZIEL, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["schluessel", "ebene", "insgesamt", "g60_66", "ab67"])
        for s, e, ges, g60, ab67 in zeilen:
            w.writerow([s, e, fmt(ges), fmt(g60), fmt(ab67)])
    n_g = sum(1 for r in zeilen if r[1] == "gemeinde")
    print(f"{ZIEL}: {n_g} Gemeinden, {len(zeilen) - n_g} Kreise")


if __name__ == "__main__":
    main()
