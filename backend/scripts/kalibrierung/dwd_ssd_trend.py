#!/usr/bin/env python3
"""
Sonnenscheindauer-Trend (SSD) je Region aus DWD-Gebietsmitteln (#98, §3.9 „Gemessen").

Modellkontext (docs/methodik/98_uv_schaedigungen.md, §3)
--------------------------------------------------------
Das UV-Modell 98-A rechnet die klimabedingte relative Dosisänderung als

    ΔDosis = [SSD(1991–2020) − SSD(1961–1990)] / SSD(1961–1990) × k_UV × a_attr,UV

mit den Klimanormalperioden als Mittelungsfenstern (Rev.-5-Befund 37: Einzeljahre sind
wegen der SSD-Variabilität ungeeignet). Der Übersetzungsfaktor k_UV (SSD-Trend →
erythemwirksame Dosis) wird empirisch gestützt über das Verhältnis des publizierten
Dosistrends der BfS-Messreihe Dortmund 1997–2022 (+4,9 %/Dekade, Lorenz u. a. 2024,
doi:10.1007/s43630-024-00658-8) zum hier gemessenen SSD-Trend Nordrhein-Westfalens im
selben Fenster (lineare Regression, %/Dekade relativ zum Fenster-Mittel).

Datenquelle (offen, keyless)
----------------------------
DWD Climate Data Center, Gebietsmittel Sonnenscheindauer (Jahreswerte, Bundesländer):
  https://opendata.dwd.de/climate_environment/CDC/regional_averages_DE/annual/sunshine_duration/regional_averages_sd_year.txt
Lizenz: GeoNutzV / DL-DE->Zero-2.0 (Quellenvermerk: Deutscher Wetterdienst).

Ausgabe (--out-dir, Default backend/data/kalibrierung/)
-------------------------------------------------------
  ssd_trend_region.csv   gebiet (nord/mitte/sued/deutschland/nrw/Bundesland),
                         ssd_ref_1961_1990, ssd_neu_1991_2020, delta_rel_prozent,
                         trend_1997_2022_prozent_je_dekade
Regionen wie #95/#96 (health.REGION_BY_BUNDESLAND); Regionsmittel = ungewichtetes
Mittel der Bundesland-Gebietsmittel (dokumentiert; die Zellrechnung des Produkts
nutzt das 1-km-Raster, diese Werte sind Referenz-/Sanity-Größen).

Aufruf: python backend/scripts/kalibrierung/dwd_ssd_trend.py [--out-dir ...]
"""
from __future__ import annotations

import argparse
import csv
import statistics
import urllib.request
from pathlib import Path

URL = ("https://opendata.dwd.de/climate_environment/CDC/regional_averages_DE/"
       "annual/sunshine_duration/regional_averages_sd_year.txt")

REGION_BY_SPALTE = {
    "nord": ["Mecklenburg-Vorpommern", "Niedersachsen/Hamburg/Bremen", "Schleswig-Holstein"],
    "mitte": ["Brandenburg/Berlin", "Hessen", "Nordrhein-Westfalen", "Rheinland-Pfalz",
              "Saarland", "Sachsen", "Thueringen/Sachsen-Anhalt"],
    "sued": ["Baden-Wuerttemberg", "Bayern"],
}
P0, P1 = (1961, 1990), (1991, 2020)
TREND_FENSTER = (1997, 2022)  # Lorenz-2024-Fenster (k_UV-Kette)


def lin_trend_pct_per_decade(years: list[int], vals: list[float]) -> float:
    n = len(years)
    mx, my = statistics.mean(years), statistics.mean(vals)
    b = sum((x - mx) * (y - my) for x, y in zip(years, vals)) / sum((x - mx) ** 2 for x in years)
    return b * 10.0 / my * 100.0


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", default=str(Path(__file__).resolve().parents[2] / "data" / "kalibrierung"))
    args = ap.parse_args()
    out = Path(args.out_dir); out.mkdir(parents=True, exist_ok=True)

    raw = urllib.request.urlopen(URL, timeout=60).read().decode("latin-1").splitlines()
    hdr = [h.strip() for h in raw[1].split(";")]
    series: dict[str, dict[int, float]] = {h: {} for h in hdr[2:] if h}
    for line in raw[2:]:
        parts = [p.strip() for p in line.split(";")]
        if len(parts) < 3 or not parts[0].isdigit():
            continue
        year = int(parts[0])
        for h, v in zip(hdr[2:], parts[2:]):
            if h and v:
                try:
                    series[h][year] = float(v)
                except ValueError:
                    pass

    def mean_window(col: str, win: tuple[int, int]) -> float:
        xs = [v for y, v in series[col].items() if win[0] <= y <= win[1]]
        assert len(xs) == win[1] - win[0] + 1, (col, win, len(xs))
        return statistics.mean(xs)

    rows = []
    laender = sorted({c for cols in REGION_BY_SPALTE.values() for c in cols})
    ziele = [("deutschland", ["Deutschland"]), ("nrw", ["Nordrhein-Westfalen"])] + \
            [(r, cols) for r, cols in REGION_BY_SPALTE.items()] + \
            [(f"land:{c}", [c]) for c in laender]   # Bundesland-Zeilen (Zell-Fallback, Bericht §3.6)
    for name, cols in ziele:
        m0 = statistics.mean(mean_window(c, P0) for c in cols)
        m1 = statistics.mean(mean_window(c, P1) for c in cols)
        ys = list(range(TREND_FENSTER[0], TREND_FENSTER[1] + 1))
        tr = statistics.mean(
            lin_trend_pct_per_decade(ys, [series[c][y] for y in ys]) for c in cols)
        rows.append({
            "gebiet": name,
            "ssd_ref_1961_1990": round(m0, 1),
            "ssd_neu_1991_2020": round(m1, 1),
            "delta_rel_prozent": round((m1 - m0) / m0 * 100.0, 2),
            "trend_1997_2022_prozent_je_dekade": round(tr, 2),
        })

    with open(out / "ssd_trend_region.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    for r in rows:
        print(r)


if __name__ == "__main__":
    main()
