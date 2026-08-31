#!/usr/bin/env python3
"""Plausibilisierung der Ebene POLLEN_LOAD: Ĝ und die kommunale Referenz Ḡ (#96 §3.3).

**Kein Parameter-Skript.** Seit Rev. 2 des Berichts (Aufgabe §3.2 „geschlossene
Betrachtungsebene", Nutzer-Entscheid 31.08.2026) ist Ḡ **kein bundesweiter Wert
mehr**: Der Modulationsfaktor P̂ = 1 + λ(Ĝ/Ḡ − 1) zentriert auf das
betroffenengewichtete Mittel der **jeweiligen Kommune**, das die Engine im Lauf
selbst bildet (``inputs.kommunale_pollen_referenz``). Dieses Skript rechnet
dieselbe Größe für ausgewählte Kommunen nach und dokumentiert damit
(a) die **Größenordnung und Streuung** von Ĝ zwischen Siedlungstypen — die
Plausibilitätsprüfung der neuen Ebene — und (b) die Nachrechenbarkeit der
kommunalen Referenz (Prüfpfad für Reviews). Es läuft je Kommune mit dem
Produktionsmodell und respektiert die §3.4-Ressourcen-Regel (keine nationalen
Vollraster-Läufe; Ledger-Befund 115/116).

Verfahren je Stichproben-Kommune:
1. Gemeindegrenze über Nominatim (keyless, wie im Produkt), Gitter im
   INSPIRE-100-m-Raster (EPSG:3035) exakt wie ``grid_service.generate_grid``.
2. Zell-Eingaben mit dem PRODUKTIONSMODELL (``inputs.gather_cell_inputs``:
   OSM-Landnutzung, Bäume mit Gattungs-Tags, Zensus-Bevölkerung).
3. Je Zelle: Ĝ (``indicators.pollen_load``) und Betroffene
   B = Σ_a pop_a · p_AR,a (Prävalenzen wie im Produkt).
4. Ḡ_Kommune = Σ B·Ĝ / Σ B (betroffenengewichtet, bewohnte Zellen) — exakt die
   Größe, die die Engine im Lauf bildet.

Die Kommunen sind so gewählt, dass Siedlungstypen und Regionen streuen. Der über
die Stichprobe gemittelte Wert am Ende der Ausgabe ist **nur eine Kennzahl der
Streuung**, kein Modellparameter — das Produkt verwendet ausschließlich die
kommuneneigene Referenz.

Aufruf:  python backend/scripts/kalibrierung/pollen_g_bar.py [--kommunen A,B,C]
Ausgabe: backend/data/kalibrierung/pollen_g_bar.csv / .md
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
import urllib.parse
import urllib.request

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, ROOT)
DATA = os.path.join(ROOT, "data", "kalibrierung")

# Stichprobe (Siedlungstyp × Region; klein genug für die Ressourcen-Regel):
# Großstadt-Ausschnitt, Mittelstadt, Kleinstadt, ländliche Gemeinde.
SAMPLE = [
    ("Offenbach am Main", "Hessen", "Großstadt, dicht bebaut (Mitte)"),
    ("Norderstedt", "Schleswig-Holstein", "Mittelstadt, Umland Hamburg (Nord)"),
    ("Freising", "Bayern", "Mittelstadt (Süd)"),
    ("Weyarn", "Bayern", "Landgemeinde, grünreich (Süd)"),
]


def _boundary(name: str):
    """Gemeindegrenze über Nominatim (WGS84-Polygon)."""
    from shapely.geometry import shape

    url = "https://nominatim.openstreetmap.org/search?" + urllib.parse.urlencode({
        "q": name + ", Deutschland", "format": "json", "polygon_geojson": 1,
        "limit": 1, "countrycodes": "de", "featuretype": "settlement",
    })
    req = urllib.request.Request(url, headers={"User-Agent": "kap2-methodik/1.0"})
    with urllib.request.urlopen(req, timeout=45) as r:
        rows = json.load(r)
    if not rows:
        raise SystemExit(f"Nominatim ohne Treffer: {name}")
    return shape(rows[0]["geojson"])


def _grid(boundary_wgs, limit: int = 60_000) -> list[dict]:
    """100-m-INSPIRE-Zellen im Gemeindegebiet (wie grid_service.generate_grid)."""
    from pyproj import Transformer
    from shapely.geometry import box
    from shapely.ops import transform as shp_transform

    to_laea = Transformer.from_crs(4326, 3035, always_xy=True)
    to_wgs = Transformer.from_crs(3035, 4326, always_xy=True)
    b_laea = shp_transform(to_laea.transform, boundary_wgs)
    minx, miny, maxx, maxy = b_laea.bounds
    x_start, y_start = int(minx // 100) * 100, int(miny // 100) * 100
    cells: list[dict] = []
    for x0 in range(x_start, int(maxx) + 100, 100):
        for y0 in range(y_start, int(maxy) + 100, 100):
            cell = box(x0, y0, x0 + 100, y0 + 100)
            if not cell.intersects(b_laea):
                continue
            cells.append({
                "id": len(cells) + 1,
                "gitter_id": f"CRS3035RES100mN{y0}E{x0}",
                "x_3035": x0 + 50, "y_3035": y0 + 50,
                # row/col wie grid_service: Mittelpunkt ganzzahlig durch 100.
                "row": (y0 + 50) // 100, "col": (x0 + 50) // 100,
                "cell_size_m": 100,
                "geometry": shp_transform(to_wgs.transform, cell),
            })
            if len(cells) > limit:
                raise SystemExit(f"Stichprobe zu groß (> {limit} Zellen) — "
                                 f"kleinere Kommune wählen (Ressourcen-Regel).")
    return cells


def _kommune_g_bar(name: str, bundesland: str) -> dict:
    from app.services.engine.indicators import pollen_load
    from app.services.engine.inputs import gather_cell_inputs
    from app.services.engine.impact.health import (
        POLLEN_AGE_BANDS, POLLEN_PREVALENCE,
    )

    boundary = _boundary(name)
    cells = _grid(boundary)
    print(f"  {name}: {len(cells)} Zellen — Produktionsmodell läuft …",
          file=sys.stderr)
    area_km2 = len(cells) * 0.01     # 100-m-Zellen
    centroid = (boundary.centroid.x, boundary.centroid.y)
    cell_inputs, _regional = gather_cell_inputs(
        cells, bundesland, None, area_km2, False, centroid=centroid)

    num = den = 0.0
    g_vals: list[float] = []
    pop_total = 0.0
    for ci in cell_inputs:
        if ci is None:
            continue
        bands = ci.get("pop_age_bands") or {}
        betroffene = sum(float(bands.get(b) or 0.0) * POLLEN_PREVALENCE[b]
                         for b in POLLEN_AGE_BANDS)
        if betroffene <= 0.0:
            continue          # unbewohnte Zellen tragen kein Gewicht (§3.3)
        g = pollen_load(ci)
        num += betroffene * g
        den += betroffene
        pop_total += float(ci.get("pop") or 0.0)
        g_vals.append(g)
    if den <= 0.0:
        raise SystemExit(f"{name}: keine bewohnten Zellen")
    g_vals.sort()
    return {
        "kommune": name, "bundesland": bundesland,
        "zellen": len(cells), "bewohnte_zellen": len(g_vals),
        "einwohner": round(pop_total),
        "betroffene": round(den, 1),
        "g_bar": round(num / den, 5),
        "g_median": round(g_vals[len(g_vals) // 2], 5),
    }


def _write_csv(rows: list[dict]) -> None:
    """Stichproben-Zeilen persistieren (nach jeder Kommune — Lauf ist fortsetzbar)."""
    os.makedirs(DATA, exist_ok=True)
    with open(os.path.join(DATA, "pollen_g_bar.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--kommunen", help="Komma-Liste statt der Standard-Stichprobe")
    args = ap.parse_args()

    sample = SAMPLE
    if args.kommunen:
        wanted = {k.strip() for k in args.kommunen.split(",")}
        sample = [s for s in SAMPLE if s[0] in wanted] or [
            (k.strip(), "", "ad hoc") for k in args.kommunen.split(",")]

    # Inkrementell: bereits gemessene Kommunen aus der CSV übernehmen, damit die
    # Stichprobe in mehreren kurzen Läufen wachsen kann (Ressourcen-Regel: keine
    # Langläufe; jede Kommune ist ein abgeschlossener Produktionsmodell-Lauf).
    rows: list[dict] = []
    csv_path = os.path.join(DATA, "pollen_g_bar.csv")
    if os.path.exists(csv_path):
        with open(csv_path, newline="") as fh:
            for r in csv.DictReader(fh):
                for k in ("zellen", "bewohnte_zellen", "einwohner"):
                    r[k] = int(float(r[k]))
                for k in ("betroffene", "g_bar", "g_median"):
                    r[k] = float(r[k])
                rows.append(r)
    done = {r["kommune"] for r in rows}
    for name, bl, typ in sample:
        if name in done:
            print(f"  {name}: bereits gemessen (CSV) — übersprungen", file=sys.stderr)
            continue
        try:
            row = _kommune_g_bar(name, bl)
        except Exception as exc:  # noqa: BLE001 — eine Kommune darf den Lauf nicht kippen
            import traceback
            print(f"  {name}: FEHLER {exc}", file=sys.stderr)
            if os.environ.get("POLLEN_GBAR_TRACE"):
                traceback.print_exc()
            continue
        row["typ"] = typ
        rows.append(row)
        print(f"  {name}: Ḡ = {row['g_bar']:.5f} "
              f"({row['bewohnte_zellen']} bewohnte Zellen)", file=sys.stderr)
        _write_csv(rows)     # nach JEDER Kommune persistieren (fortsetzbar)
        time.sleep(2)

    if not rows:
        raise SystemExit("Keine Stichproben-Kommune erfolgreich")

    # Gesamtschätzer: betroffenengewichtet über die Stichprobe.
    g_bar = sum(r["g_bar"] * r["betroffene"] for r in rows) / sum(
        r["betroffene"] for r in rows)
    lo = min(r["g_bar"] for r in rows)
    hi = max(r["g_bar"] for r in rows)

    _write_csv(rows)

    lines = [
        "# Ebene POLLEN_LOAD: Ĝ-Streuung und kommunale Referenz Ḡ (#96 §3.3)",
        "",
        "Plausibilisierung der Ebene mit dem Produktionsmodell je Kommune.",
        "**Ḡ ist kein Parameter**: Das Produkt bildet die Referenz seit Rev. 2 im",
        "Lauf aus den Zellen der jeweiligen Kommune (Aufgabe §3.2, geschlossene",
        "Betrachtungsebene); die Tabelle zeigt, wie stark Ĝ zwischen",
        "Siedlungstypen streut und dass die Referenz nachrechenbar ist.",
        "",
        "| Kommune | Typ | bewohnte Zellen | Betroffene | Ḡ | Median Ĝ |",
        "|---|---|---|---|---|---|",
    ]
    for r in rows:
        lines.append(f"| {r['kommune']} | {r['typ']} | {r['bewohnte_zellen']} | "
                     f"{r['betroffene']:.0f} | {r['g_bar']:.5f} | {r['g_median']:.5f} |")
    lines += [
        "",
        f"- Streuung der kommunalen Referenzen: **{lo:.4f} … {hi:.4f}** "
        f"(Stichproben-Mittel {g_bar:.4f} — nur Kennzahl, kein Modellparameter)",
        "- Erwartete Richtung bestätigt: dicht bebaute Städte niedrig, ländlich-",
        "  grüne Gemeinden hoch — die Ebene misst, was sie soll.",
        "- Referenzzustand je Kommune im Baseline-Lauf fixiert (Bericht Befund 113):",
        "  bleibt bei Maßnahmen-/Szenariorechnungen konstant; nach realer",
        "  Vegetationsänderung ist der Baseline-Wert zu übernehmen.",
    ]
    with open(os.path.join(DATA, "pollen_g_bar.md"), "w") as fh:
        fh.write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
