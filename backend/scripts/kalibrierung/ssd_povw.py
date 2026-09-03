#!/usr/bin/env python3
"""Bevölkerungsgewichtete SSD-Normalperiodenänderung für #98 §3.2/§4 (Befund 223).

**Warum diese Anlage existiert.** Das Produktionsmodell rechnet die
klimaattribuierte Dosisänderung je Zelle und summiert Zellen zur Kommune:

    ΔF = Σ_Zellen F_Zelle · BAF · ΔDosis_Zelle ,   ΔDosis_Zelle ∝ ΔSSD_Zelle

Die wirksame nationale ΔSSD ist damit das **bevölkerungsgewichtete** Mittel der
relativen Zelländerungen — nicht das flächengewichtete DWD-Gebietsmittel
(+7,82 %), mit dem der Bericht bis Rev. 2 alle Bundessummen und Sanity-Bänder
gerechnet hat. Aufgabe §3.4 verlangt ausdrücklich „Kalibriermodell =
Produktionsmodell … unzulässig, sobald das Produktionsmodell … bevölkerungs-
gewichtete Exposition hat" (Ledger-Befund 223; dieselbe Fehlerklasse hat #95 in
Rev. 8 mit ``sommermittel_bundesland_povw.csv`` gelöst).

**Ressourcen-Regel (§3.4) gewahrt.** Kein nationaler 100-m-Vollraster-Lauf: Die
Gewichtung läuft auf der ausdrücklich erlaubten **Gemeindepunkt-Ebene**: der
VG250-Layer ``vg250_pk`` (Gebietsstand **01.01.2025**) führt 10.949 amtliche
Gemeindepunkte (Verwaltungssitz mit
Dezimalkoordinaten), von denen **10.824** eine Zensus-Gemeindebevölkerung UND einen
Rasterwert haben und in die Gewichtung eingehen. Das sind 10.824 Rasterablesungen
statt ~3,6 Mio Zellen.

**Gekennzeichnete Näherungen (§3.9, Befund 235).** (a) Gewichtet wird mit **Köpfen**,
das Produktionsmodell summiert aber **Baseline-Fälle**; weil die Altersstruktur
regional variiert, ist der exakte Bezug die fallgewichtete ΔSSD (Abweichung auf
Landesebene +0,11 % MM / +0,19 % C44 relativ). (b) Die gesamte Gemeindebevölkerung
wird an **einem** Punkt abgelesen (Berlin 3,59 Mio an einer 1-km-Zelle); gegen ein
Boxmittel gerechnet −0,28 % relativ. Beide sind klein und teils gegenläufig.

**Kalibriermodell = Produktionsmodell.** Die SSD-Werte werden über dieselbe
Produktfunktion gelesen, die auch die Schadensfunktion benutzt
(``app.services.climate.ssd_normalperioden.ssd_at``) — die Anlage kann sich
nicht von der Produktion entkoppeln.

Ausgaben (backend/data/kalibrierung/):
    ssd_povw.csv   je Gebiet: flächengewichtet, bevölkerungsgewichtet, Δ
    ssd_povw.md    Kennzahlen, Bundes-/Regionswerte, Wirkung auf die Bundessumme

Aufruf: python backend/scripts/kalibrierung/ssd_povw.py
Quellen: BKG VG250 (DL-DE->BY-2.0), Zensus 2022 (Destatis), DWD-CDC
``sunshine_duration`` 1 km (DL-DE->Zero-2.0) via ``ssd_normalperioden.npz``.
"""
from __future__ import annotations

import csv
import json
import os
import sqlite3
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, ROOT)
DATA = os.path.join(ROOT, "data", "kalibrierung")
GPKG = os.path.join(ROOT, "data", "vg250", "DE_VG250.gpkg")
GEMEINDEN = os.path.join(ROOT, "data", "lite", "zensus_gemeinde.json")

# Regionszuordnung wie ``dwd_ssd_trend.py``/Bericht §3.2 (Nord/Mitte/Süd).
REGION = {
    "01": "nord", "02": "nord", "03": "nord", "04": "nord", "13": "nord",
    "05": "mitte", "06": "mitte", "07": "mitte", "10": "mitte", "11": "mitte",
    "12": "mitte", "14": "mitte", "15": "mitte", "16": "mitte",
    "08": "sued", "09": "sued",
}
LAND = {
    "01": "Schleswig-Holstein", "02": "Hamburg", "03": "Niedersachsen",
    "04": "Bremen", "05": "Nordrhein-Westfalen", "06": "Hessen",
    "07": "Rheinland-Pfalz", "08": "Baden-Württemberg", "09": "Bayern",
    "10": "Saarland", "11": "Berlin", "12": "Brandenburg",
    "13": "Mecklenburg-Vorpommern", "14": "Sachsen", "15": "Sachsen-Anhalt",
    "16": "Thüringen",
}

# Modellparameter für die Wirkungsrechnung (Bericht §3.1–§3.4, Rev. 3).
K_UV, A_ATTR = (4.9 / 4.6) * 0.6683, 0.75   # k_UV rasterskaliert (Befunde 238/245/252)
BAF = {"mm": 0.6, "c44": 0.75 * 1.4 + 0.25 * 2.5}
ANKER = {"mm": (26_140 + 27_040 + 27_430) / 3,
         "c44": (236_670 + 243_430 + 242_820) / 3}
LAMBDA = {"mm": (2928 + 3146 + 3169) / 3 / ANKER["mm"],
          "c44": (1178 + 1275 + 1332) / 3 / ANKER["c44"]}
L_REST = {"mm": 10.4569, "c44": 5.4787}          # Befund 224 (Ankerfenster)
C_FALL = {"mm": 6_724.0, "c44": 5_883.0}
VOLY = 160_800.0
D_SSD_FLAECHE = 0.0782                            # DWD-Gebietsmittel [69]


def gemeindepunkte() -> list[tuple[str, float, float]]:
    """AGS + Dezimalkoordinaten der amtlichen Gemeindepunkte (VG250 ``vg250_pk``)."""
    con = sqlite3.connect(GPKG)
    try:
        rows = con.execute(
            "SELECT AGS, LON_DEZ, LAT_DEZ FROM vg250_pk "
            "WHERE AGS IS NOT NULL AND LON_DEZ IS NOT NULL").fetchall()
    finally:
        con.close()
    return [(str(a).zfill(8), float(x), float(y)) for a, x, y in rows]


def main() -> None:
    from app.services.climate import ssd_normalperioden as ssd

    pop_je_ags = {k: float(v.get("population") or 0.0)
                  for k, v in json.load(open(GEMEINDEN, encoding="utf-8")).items()}
    punkte = gemeindepunkte()

    # Akkumulatoren je Gebiet: [Σ pop, Σ pop·Δrel, Σ Δrel, n]
    acc: dict[str, list[float]] = {}
    ohne_raster = ohne_pop = 0
    for ags, lon, lat in punkte:
        pop = pop_je_ags.get(ags)
        if pop is None or pop <= 0:
            ohne_pop += 1
            continue
        paar = ssd.ssd_at(lon, lat)
        if paar is None or paar[0] <= 0:
            ohne_raster += 1
            continue
        ref, neu = paar
        d = (neu - ref) / ref
        for gebiet in ("deutschland", f"land:{LAND[ags[:2]]}",
                       f"region:{REGION[ags[:2]]}"):
            a = acc.setdefault(gebiet, [0.0, 0.0, 0.0, 0.0])
            a[0] += pop
            a[1] += pop * d
            a[2] += d
            a[3] += 1

    de = acc["deutschland"]
    povw_de = de[1] / de[0]
    flaeche_de = de[2] / de[3]        # ungewichtetes Gemeindepunkt-Mittel

    rows = []
    for gebiet in sorted(acc):
        a = acc[gebiet]
        rows.append({
            "gebiet": gebiet,
            "gemeinden": int(a[3]),
            "bevoelkerung": round(a[0]),
            "delta_rel_povw_prozent": round(a[1] / a[0] * 100, 3),
            "delta_rel_punktmittel_prozent": round(a[2] / a[3] * 100, 3),
        })
    with open(os.path.join(DATA, "ssd_povw.csv"), "w", newline="",
              encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    def bundessumme(d_ssd: float) -> tuple[dict, float, float, float]:
        dd = d_ssd * K_UV * A_ATTR
        df = {e: ANKER[e] * BAF[e] * dd for e in ANKER}
        yll = sum(df[e] * LAMBDA[e] * L_REST[e] for e in df)
        beh = sum(df[e] * C_FALL[e] for e in df)
        return df, yll, beh, beh + yll * VOLY

    z = ["# #98 — Bevölkerungsgewichtete SSD-Normalperiodenänderung (Befund 223)\n",
         "Erzeugt von `backend/scripts/kalibrierung/ssd_povw.py`. Gewichtung auf der",
         "**Gemeindepunkt-Ebene** (§3.4 ausdrücklich zulässig; kein 100-m-Vollraster-Lauf):",
         f"{int(de[3]):,}".replace(",", ".")
         + " amtliche Gemeindepunkte (BKG VG250 `vg250_pk`, Gebietsstand 01.01.2025)",
         "mit Zensus-2022-Gemeindebevölkerung; SSD über die **Produktfunktion**",
         "`ssd_normalperioden.ssd_at` gelesen (Kalibriermodell = Produktionsmodell).\n",
         # Punktmengen-Kette gemessen, nicht fortgeschrieben (Befund 396): Der
         # Bericht nennt alle Stufen; die ersten beiden entstehen hier beim Join.
         "**Punktmengen-Kette (Befund 396):** VG250 `vg250_pk` führt "
         + f"{len(punkte):,}".replace(",", ".")
         + " amtliche Gemeindepunkte; davon "
         + f"{len(punkte) - ohne_pop:,}".replace(",", ".")
         + f" mit Zensus-2022-Einwohnerzahl ({ohne_pop} ohne) und davon "
         + f"{int(de[3]):,}".replace(",", ".")
         + f" mit SSD-Rasterwert ({ohne_raster} ohne) — diese gehen in die Gewichtung ein.\n",
         "## 1 Nationale ΔSSD\n",
         "| Aggregation | ΔSSD DE | Bezug |",
         "|---|---|---|",
         f"| DWD-Gebietsmittel (**flächen**gewichtet, Anlage [69]) | **{D_SSD_FLAECHE*100:.2f} %** | bisheriger Berichtswert |",
         f"| Gemeindepunkte, ungewichtet | {flaeche_de*100:.2f} % | Kontrolle: nahe am Flächenmittel |",
         f"| Gemeindepunkte, **bevölkerungsgewichtet** | **{povw_de*100:.2f} %** | wirksamer Wert des Produktionsmodells |",
         "",
         f"Korrektur gegenüber dem Flächenmittel: **{povw_de/D_SSD_FLAECHE-1:+.1%}**.",
         "Ursache: Die einwohnerstarken Länder (NRW, Hessen, Niedersachsen) haben",
         "überdurchschnittliche Zuwächse, die dünn besiedelten Küsten- und",
         "Nordostländer unterdurchschnittliche.\n",
         "## 2 Je Region und Bundesland\n",
         "| Gebiet | Gemeinden | Bevölkerung | ΔSSD bev.-gew. | ΔSSD Punktmittel |",
         "|---|---|---|---|---|"]
    for r in rows:
        z.append(f"| {r['gebiet']} | {r['gemeinden']:,} | {r['bevoelkerung']:,} | "
                 f"**{r['delta_rel_povw_prozent']:.2f} %** | "
                 f"{r['delta_rel_punktmittel_prozent']:.2f} % |".replace(",", "."))

    z.append("\n## 3 Wirkung auf die Bundessummen (Basiswerte, L̄ nach Befund 224)\n")
    z.append("| Größe | flächengewichtet (Vergleich) | **bevölkerungsgewichtet (Basiswert)** | Δ |")
    z.append("|---|---|---|---|")
    a_df, a_y, a_b, a_e = bundessumme(D_SSD_FLAECHE)
    n_df, n_y, n_b, n_e = bundessumme(povw_de)
    for name, alt, neu, fmt in (
            ("ΔDosis DE", D_SSD_FLAECHE * K_UV * A_ATTR, povw_de * K_UV * A_ATTR, "{:.4%}"),
            ("ΔF MM", a_df["mm"], n_df["mm"], "{:,.0f}"),
            ("ΔF C44", a_df["c44"], n_df["c44"], "{:,.0f}"),
            ("YLL", a_y, n_y, "{:,.0f}"),
            ("€ Mio", a_e / 1e6, n_e / 1e6, "{:,.0f}")):
        z.append(f"| {name} | {fmt.format(alt)} | **{fmt.format(neu)}** | "
                 f"{neu/alt-1:+.1%} |".replace(",", "."))
    z.append("")
    z.append(f"Nicht zugeordnet: {ohne_pop} Gemeindepunkte ohne Zensus-Bevölkerung, "
             f"{ohne_raster} ohne Rasterwert (beide gehen nicht in die Gewichtung ein).")

    out = "\n".join(z)
    with open(os.path.join(DATA, "ssd_povw.md"), "w", encoding="utf-8") as fh:
        fh.write(out)
    print(out)


if __name__ == "__main__":
    main()
