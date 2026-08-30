#!/usr/bin/env python3
"""
Pollensaison-Spreizung ΔS je Region aus DWD-Phänologie-Jahresmeldern (#96, §3.9 „Gemessen").

Modellkontext (docs/methodik/96_aeroallergene.md, §3)
-----------------------------------------------------
Das Aeroallergene-Modell rechnet die klimabedingte Verlängerung der
Patienten-Pollensaison als messbare **Spreizung** zwischen phänologischen
Saison-Markern (Differenz der Blühbeginn-/Vollblüte-Termine), nicht als bloße
Verfrühung — eine reine Parallelverschiebung der Saison erzeugt keine
zusätzlichen Symptomtage:

  Birkengruppe (Hasel/Erle/Birke, Bet-v-1-Kreuzreaktivität):
      span_B = Jultag(Hänge-Birke, Blüte Beginn) − Jultag(Schwarz-Erle, Blüte Beginn)
      ΔS_B   = mean(span_B | 1991–2020) − mean(span_B | 1961–1990)
      (Erle-Blühbeginn = KWRA-Indikator GE-KL-07; rückt die Erle stärker vor als
       die Birke, wird das Symptomfenster der Birkengruppen-Patienten vorn länger.)

  Gräser (Saison-Sukzession früh → spät):
      span_G = Jultag(Wiesen-Knäuelgras, Vollblüte) − Jultag(Wiesen-Fuchsschwanz, Vollblüte)
      ΔS_G   analog.
      (Vollblüte (Phase 6) statt Blüte Beginn: bei den Gräser-Jahresmeldern die
       mit Abstand meldungsstärkste Phase; als Spreizungs-Differenz ist die
       Phasenwahl konsistent, solange beide Marker dieselbe Phase nutzen.)

  Sensitivität: span_H = Birke − Hasel (Hasel als frühester Front-Marker).

Konservativ nicht enthalten (dokumentierte Untergrenze im Bericht §6):
Saisonende-Verlängerung im Herbst (kein Phänologie-Marker) und
Intensitätszunahme (Pollenmenge).

Datenquelle (offen, keyless)
----------------------------
DWD Climate Data Center, Phänologie-Jahresmelder (historisch):
  https://opendata.dwd.de/climate_environment/CDC/observations_germany/phenology/annual_reporters/wild/historical/
  PH_Jahresmelder_Wildwachsende_Pflanze_<Art>_<von>_<bis>_hist.txt
  Spalten: Stations_id;Referenzjahr;Qualitaetsniveau;Objekt_id;Phase_id;
           Eintrittsdatum;Eintrittsdatum_QB;Jultag;eor
  Stationsliste (mit Bundesland):
  https://opendata.dwd.de/climate_environment/CDC/help/PH_Beschreibung_Phaenologie_Stationen_Jahresmelder.txt
Lizenz: GeoNutzV / DL-DE->Zero-2.0 (Quellenvermerk: Deutscher Wetterdienst).

Vorgehen
--------
1. Regionen wie #95 (health.REGION_BY_BUNDESLAND): Nord = HB, HH, MV, NI, SH ·
   Mitte = BE, BB, HE, NW, RP, SL, SN, ST, TH · Süd = BW, BY.
2. Je (Station, Jahr) wird eine Spanne nur gebildet, wenn beide Marker im selben
   Jahr an derselben Station gemeldet sind (Plausibilitätsfenster je Art, s. u.).
3. **Gepaarte Stationen**: eine Station zählt nur, wenn sie in BEIDEN
   Normalperioden (1961–1990, 1991–2020) mindestens --min-years gültige
   Spannen-Jahre hat — das neutralisiert Netzverschiebungen.
4. Je Station: Periodenmittel und Δ = mean(P1) − mean(P0); je Region: Mittel der
   Stations-Δ (gleichgewichtet) + Streuung. Zusätzlich Einzelart-Verfrühungen
   (Erle = GE-KL-07, Hasel, Birke) zur Plausibilisierung gegen Endler 2020 /
   KWRA TB5 („Hasel/Erle bis 26 Tage früher").

Ausgabe (--out-dir, Default backend/data/kalibrierung/)
-------------------------------------------------------
  pollensaison_region.csv    region, komponente, n_stationen, mittel_ref, mittel_neu,
                             delta_tage, sd_delta_stationen
  pollensaison_meta.csv      Artefakt-/Filter-Metadaten, Einzelart-Verfrühungen

Rohdaten werden NICHT ins Repository gelegt, sondern in --cache-dir
(Default: $KAP2_DWD_CACHE oder <tempdir>/kap2_dwd_phaeno). Wiederholte Läufe
laden nichts neu.

Aufruf:
  python backend/scripts/kalibrierung/dwd_pollensaison.py --cache-dir /pfad [--out-dir ...]
"""
from __future__ import annotations

import argparse
import csv
import os
import statistics
import sys
import tempfile
import urllib.request
from collections import defaultdict
from pathlib import Path

BASE = ("https://opendata.dwd.de/climate_environment/CDC/observations_germany/"
        "phenology/annual_reporters/wild/historical")
STATION_URL = ("https://opendata.dwd.de/climate_environment/CDC/help/"
               "PH_Beschreibung_Phaenologie_Stationen_Jahresmelder.txt")

# Art -> (Dateiname, Phase_id, Plausibilitätsfenster Jultag)
SPECIES = {
    "hasel": ("PH_Jahresmelder_Wildwachsende_Pflanze_Hasel_1930_2024_hist.txt", 5, (1, 150)),
    "erle": ("PH_Jahresmelder_Wildwachsende_Pflanze_Schwarz-Erle_1936_2024_hist.txt", 5, (1, 160)),
    # Birke: Phase 5 (Blüte Beginn) hat eine Meldelücke 1960–1990; Marker ist daher
    # Phase 4 (Blattentfaltung) — bei der Birke nahezu blühsynchron. Der Offset
    # Phase 5 − Phase 4 wird in den Überlappungsjahren gemessen und als Meta-Zeile
    # ausgegeben (konstanter Offset kürzt sich in der Spreizungs-Differenz heraus).
    "birke": ("PH_Jahresmelder_Wildwachsende_Pflanze_Haenge-Birke_1930_2024_hist.txt", 4, (60, 180)),
    "birke_bluete": ("PH_Jahresmelder_Wildwachsende_Pflanze_Haenge-Birke_1930_2024_hist.txt", 5, (60, 180)),
    "gras_frueh": ("PH_Jahresmelder_Wildwachsende_Pflanze_Wiesen-Fuchsschwanz_1936_2024_hist.txt", 6, (100, 220)),
    "gras_spaet": ("PH_Jahresmelder_Wildwachsende_Pflanze_Wiesen-Knaeuelgras_1936_2024_hist.txt", 6, (100, 250)),
}

# Spannen: (früher Marker, später Marker, Plausibilitätsfenster der Spanne in Tagen)
SPANS = {
    "birkengruppe": ("erle", "birke", (0, 120)),
    "graeser": ("gras_frueh", "gras_spaet", (0, 90)),
    "birkengruppe_hasel": ("hasel", "birke", (0, 140)),  # Sensitivität
}

REGION_BY_BUNDESLAND = {
    "Bremen": "nord", "Hamburg": "nord", "Mecklenburg-Vorpommern": "nord",
    "Niedersachsen": "nord", "Schleswig-Holstein": "nord",
    "Berlin": "mitte", "Brandenburg": "mitte", "Hessen": "mitte",
    "Nordrhein-Westfalen": "mitte", "Rheinland-Pfalz": "mitte", "Saarland": "mitte",
    "Sachsen": "mitte", "Sachsen-Anhalt": "mitte", "Thüringen": "mitte",
    "Baden-Württemberg": "sued", "Bayern": "sued",
}

P0 = (1961, 1990)  # Referenz-Normalperiode
P1 = (1991, 2020)  # aktuelle Normalperiode


def fetch(url: str, dest: Path) -> Path:
    if not dest.exists() or dest.stat().st_size == 0:
        print(f"lade {url.rsplit('/', 1)[-1]} …", file=sys.stderr)
        urllib.request.urlretrieve(url, dest)
    return dest


def load_stations(cache: Path) -> dict[int, str]:
    """Stations_id -> Region (über Bundesland)."""
    f = fetch(STATION_URL, cache / "stationen_jahresmelder.txt")
    region_by_id: dict[int, str] = {}
    with open(f, encoding="latin-1") as fh:
        next(fh)  # Header
        for line in fh:
            parts = [p.strip() for p in line.split(";")]
            if len(parts) < 11 or not parts[0].isdigit():
                continue
            land = parts[10]
            reg = REGION_BY_BUNDESLAND.get(land)
            if reg:
                region_by_id[int(parts[0])] = reg
    return region_by_id


def load_species(cache: Path, key: str) -> dict[tuple[int, int], int]:
    """(Stations_id, Jahr) -> Jultag (Mittel bei Mehrfachmeldung)."""
    fname, phase, (lo, hi) = SPECIES[key]
    f = fetch(f"{BASE}/{fname}", cache / fname)
    vals: dict[tuple[int, int], list[int]] = defaultdict(list)
    with open(f, encoding="latin-1") as fh:
        next(fh)
        for line in fh:
            parts = [p.strip() for p in line.split(";")]
            if len(parts) < 8:
                continue
            try:
                sid, year, ph, jultag = int(parts[0]), int(parts[1]), int(parts[4]), int(parts[7])
            except ValueError:
                continue
            if ph != phase or not (lo <= jultag <= hi):
                continue
            vals[(sid, year)].append(jultag)
    return {k: round(statistics.mean(v)) for k, v in vals.items()}


def period_mean(years_vals: dict[int, float], period: tuple[int, int], min_years: int):
    xs = [v for y, v in years_vals.items() if period[0] <= y <= period[1]]
    if len(xs) < min_years:
        return None, len(xs)
    return statistics.mean(xs), len(xs)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache-dir", default=os.environ.get(
        "KAP2_DWD_CACHE", os.path.join(tempfile.gettempdir(), "kap2_dwd_phaeno")))
    ap.add_argument("--out-dir", default=str(Path(__file__).resolve().parents[2] / "data" / "kalibrierung"))
    ap.add_argument("--min-years", type=int, default=8,
                    help="Mindestzahl gültiger Spannen-Jahre je Station und Normalperiode (Default 8)")
    args = ap.parse_args()

    cache = Path(args.cache_dir); cache.mkdir(parents=True, exist_ok=True)
    out = Path(args.out_dir); out.mkdir(parents=True, exist_ok=True)

    region_by_id = load_stations(cache)
    data = {k: load_species(cache, k) for k in SPECIES}

    region_rows: list[dict] = []
    meta_rows: list[dict] = []

    # 1) Spannen (Saison-Spreizung)
    for span_key, (early, late, (slo, shi)) in SPANS.items():
        spans: dict[int, dict[int, int]] = defaultdict(dict)  # sid -> {jahr: spanne}
        for (sid, year), j_early in data[early].items():
            j_late = data[late].get((sid, year))
            if j_late is None:
                continue
            span = j_late - j_early
            if not (slo <= span <= shi):
                continue
            spans[sid][year] = span

        per_region: dict[str, list[tuple[float, float, float]]] = defaultdict(list)
        for sid, yv in spans.items():
            reg = region_by_id.get(sid)
            if reg is None:
                continue
            m0, n0 = period_mean(yv, P0, args.min_years)
            m1, n1 = period_mean(yv, P1, args.min_years)
            if m0 is None or m1 is None:
                continue
            per_region[reg].append((m0, m1, m1 - m0))

        for reg in ("nord", "mitte", "sued"):
            triples = per_region[reg]
            if not triples:
                continue
            deltas = [t[2] for t in triples]
            region_rows.append({
                "region": reg, "komponente": span_key, "n_stationen": len(triples),
                "mittel_ref_1961_1990": round(statistics.mean(t[0] for t in triples), 2),
                "mittel_neu_1991_2020": round(statistics.mean(t[1] for t in triples), 2),
                "delta_tage": round(statistics.mean(deltas), 2),
                "sd_delta_stationen": round(statistics.stdev(deltas), 2) if len(deltas) > 1 else 0.0,
            })
        alle = [t for reg in per_region.values() for t in reg]
        if alle:
            deltas = [t[2] for t in alle]
            region_rows.append({
                "region": "deutschland", "komponente": span_key, "n_stationen": len(alle),
                "mittel_ref_1961_1990": round(statistics.mean(t[0] for t in alle), 2),
                "mittel_neu_1991_2020": round(statistics.mean(t[1] for t in alle), 2),
                "delta_tage": round(statistics.mean(deltas), 2),
                "sd_delta_stationen": round(statistics.stdev(deltas), 2) if len(deltas) > 1 else 0.0,
            })

    # 2) Einzelart-Verfrühungen (Plausibilisierung GE-KL-07 gegen Endler 2020)
    for art in ("hasel", "erle", "birke", "gras_frueh", "gras_spaet"):
        by_station: dict[int, dict[int, int]] = defaultdict(dict)
        for (sid, year), j in data[art].items():
            by_station[sid][year] = j
        per_region = defaultdict(list)
        for sid, yv in by_station.items():
            reg = region_by_id.get(sid)
            if reg is None:
                continue
            m0, _ = period_mean(yv, P0, args.min_years)
            m1, _ = period_mean(yv, P1, args.min_years)
            if m0 is None or m1 is None:
                continue
            per_region[reg].append(m1 - m0)
        for reg in ("nord", "mitte", "sued"):
            if per_region[reg]:
                meta_rows.append({
                    "kennzahl": f"verfruehung_{art}", "region": reg,
                    "n_stationen": len(per_region[reg]),
                    "wert_tage": round(statistics.mean(per_region[reg]), 2),
                })
        alle = [d for v in per_region.values() for d in v]
        if alle:
            meta_rows.append({"kennzahl": f"verfruehung_{art}", "region": "deutschland",
                              "n_stationen": len(alle), "wert_tage": round(statistics.mean(alle), 2)})

    # 3) Marker-Diagnose Birke: Offset Blüte Beginn (5) − Blattentfaltung (4)
    #    in den Überlappungs-Stationsjahren; Trendprüfung über zwei Halbperioden.
    offsets: dict[int, list[int]] = defaultdict(list)
    for (sid, year), j5 in data["birke_bluete"].items():
        j4 = data["birke"].get((sid, year))
        if j4 is not None and -30 <= j5 - j4 <= 30:
            offsets[year].append(j5 - j4)
    off_all = [o for v in offsets.values() for o in v]
    if off_all:
        h1 = [o for y, v in offsets.items() if 1991 <= y <= 2005 for o in v]
        h2 = [o for y, v in offsets.items() if 2006 <= y <= 2020 for o in v]
        meta_rows.append({"kennzahl": "birke_offset_bluete_minus_blattentfaltung",
                          "region": "deutschland", "n_stationen": len(off_all),
                          "wert_tage": round(statistics.mean(off_all), 2)})
        if h1 and h2:
            meta_rows.append({"kennzahl": "birke_offset_trend_1991_2005_vs_2006_2020",
                              "region": "deutschland", "n_stationen": f"{len(h1)}/{len(h2)}",
                              "wert_tage": f"{statistics.mean(h1):.2f} vs {statistics.mean(h2):.2f}"})

    meta_rows.append({"kennzahl": "min_years_je_periode", "region": "-",
                      "n_stationen": "-", "wert_tage": args.min_years})
    meta_rows.append({"kennzahl": "perioden", "region": "-", "n_stationen": "-",
                      "wert_tage": f"{P0[0]}-{P0[1]} vs {P1[0]}-{P1[1]}"})

    with open(out / "pollensaison_region.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(region_rows[0].keys()))
        w.writeheader(); w.writerows(region_rows)
    with open(out / "pollensaison_meta.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["kennzahl", "region", "n_stationen", "wert_tage"])
        w.writeheader(); w.writerows(meta_rows)

    for r in region_rows:
        print(r)
    print("—")
    for m in meta_rows:
        print(m)


if __name__ == "__main__":
    main()
