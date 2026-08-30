#!/usr/bin/env python3
"""
Sommermitteltemperatur (Jun–Aug) je Bundesland und Jahr aus DWD-Gebietsmitteln.

Datenquelle (offen, keyless)
----------------------------
DWD Climate Data Center, monatliche Gebietsmittel der Lufttemperatur:
  https://opendata.dwd.de/climate_environment/CDC/regional_averages_DE/monthly/air_temperature_mean/
    regional_averages_tm_06.txt   (Juni)
    regional_averages_tm_07.txt   (Juli)
    regional_averages_tm_08.txt   (August)
Format: 1 Kopfzeile (Erstellungsdatum), dann Spaltenzeile
  Jahr;Monat;Brandenburg/Berlin;Brandenburg;Baden-Wuerttemberg;Bayern;Hessen;
  Mecklenburg-Vorpommern;Niedersachsen;Niedersachsen/Hamburg/Bremen;
  Nordrhein-Westfalen;Rheinland-Pfalz;Schleswig-Holstein;Saarland;Sachsen;
  Sachsen-Anhalt;Thueringen/Sachsen-Anhalt;Thueringen;Deutschland;
Lizenz: GeoNutzV / DL-DE->Zero-2.0 (Quellenvermerk: Deutscher Wetterdienst).

Sommermittel = arithmetisches Mittel der drei Monatsmittel Jun/Jul/Aug
(Monate gleich gewichtet; die Tageszahlen 30/31/31 werden nicht berücksichtigt —
Abweichung zum tagesgewichteten Mittel < 0,02 K).

Zuordnung der Bundesländer (DWD führt Stadtstaaten nicht getrennt)
-------------------------------------------------------------------
  Berlin   -> Spalte "Brandenburg/Berlin"            (Berlin liegt vollständig in
                                                      Brandenburg; Unterschied zu
                                                      "Brandenburg" < 0,02 K)
  Hamburg  -> Spalte "Niedersachsen/Hamburg/Bremen"  (keine eigene Reihe; die
  Bremen   -> Spalte "Niedersachsen/Hamburg/Bremen"   Kombination ist das einzige
                                                      DWD-Gebietsmittel, das die
                                                      Stadtstaaten enthält)
  alle anderen: gleichnamige Spalte (Umlaute: Baden-Wuerttemberg -> Baden-Württemberg,
  Thueringen -> Thüringen). Die Kombi-Spalte "Thueringen/Sachsen-Anhalt" wird nicht
  verwendet, da beide Länder einzeln vorliegen.
Die Zuordnung wird zusätzlich in sommermittel_bundesland_zuordnung.csv abgelegt.

Plausibilisierung (--plausibilisierung)
---------------------------------------
Vergleicht für die Stadtstaaten die DWD-Kombi-Gebietsmittel mit den Sommermitteln
der Stationen aus dwd_wochenquantile.py (Hamburg-Fuhlsbüttel 1975, Bremen 691,
Berlin-Tempelhof 433; Referenz Hannover 2014, Potsdam 3987) über 1992–2020:
mittlere Differenz, Std der Differenz und Korrelation der Jahreswerte.

Ausgabe (--out-dir, Default backend/data/kalibrierung/)
-------------------------------------------------------
  sommermittel_bundesland.csv             jahr, bundesland, t_sommer   (Long-Format)
  sommermittel_bundesland_zuordnung.csv   bundesland, dwd_spalte, hinweis
  sommermittel_plausibilisierung.csv      (nur mit --plausibilisierung)

Aufruf:
  python backend/scripts/kalibrierung/dwd_sommermittel.py --cache-dir /pfad/zum/cache \
      [--years 1992 2025] [--plausibilisierung]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from dwd_wochenquantile import default_cache_dir, fetch_to_file, load_tmk  # noqa: E402

BASE_URL = (
    "https://opendata.dwd.de/climate_environment/CDC/regional_averages_DE/"
    "monthly/air_temperature_mean/"
)
MONTHS = {6: "regional_averages_tm_06.txt", 7: "regional_averages_tm_07.txt", 8: "regional_averages_tm_08.txt"}
DEFAULT_YEARS = (1992, 2025)

# Projektname -> (DWD-Spalte, Hinweis)
MAPPING: dict[str, tuple[str, str]] = {
    "Baden-Württemberg": ("Baden-Wuerttemberg", "eigene DWD-Reihe"),
    "Bayern": ("Bayern", "eigene DWD-Reihe"),
    "Berlin": ("Brandenburg/Berlin", "keine eigene DWD-Reihe; Kombi Brandenburg/Berlin"),
    "Brandenburg": ("Brandenburg", "eigene DWD-Reihe"),
    "Bremen": ("Niedersachsen/Hamburg/Bremen", "keine eigene DWD-Reihe; Kombi Niedersachsen/Hamburg/Bremen"),
    "Hamburg": ("Niedersachsen/Hamburg/Bremen", "keine eigene DWD-Reihe; Kombi Niedersachsen/Hamburg/Bremen"),
    "Hessen": ("Hessen", "eigene DWD-Reihe"),
    "Mecklenburg-Vorpommern": ("Mecklenburg-Vorpommern", "eigene DWD-Reihe"),
    "Niedersachsen": ("Niedersachsen", "eigene DWD-Reihe"),
    "Nordrhein-Westfalen": ("Nordrhein-Westfalen", "eigene DWD-Reihe"),
    "Rheinland-Pfalz": ("Rheinland-Pfalz", "eigene DWD-Reihe"),
    "Saarland": ("Saarland", "eigene DWD-Reihe"),
    "Sachsen": ("Sachsen", "eigene DWD-Reihe"),
    "Sachsen-Anhalt": ("Sachsen-Anhalt", "eigene DWD-Reihe"),
    "Schleswig-Holstein": ("Schleswig-Holstein", "eigene DWD-Reihe"),
    "Thüringen": ("Thueringen", "eigene DWD-Reihe"),
    "Deutschland": ("Deutschland", "DWD-Gebietsmittel Deutschland"),
}

# Stationen für die Plausibilisierung der Kombi-Spalten (IDs siehe dwd_wochenquantile.py)
PLAUSI_STATIONS = [
    ("Hamburg", 1975, "Hamburg-Fuhlsbüttel"),
    ("Bremen", 691, "Bremen"),
    ("Niedersachsen", 2014, "Hannover"),
    ("Berlin", 433, "Berlin-Tempelhof"),
    ("Brandenburg", 3987, "Potsdam"),
]


def read_regional_file(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, sep=";", skiprows=1, skipinitialspace=True, encoding="latin-1")
    df = df.loc[:, [c for c in df.columns if not str(c).startswith("Unnamed")]]
    df.columns = [str(c).strip() for c in df.columns]
    df = df.rename(columns={"Jahr": "jahr", "Monat": "monat"})
    for c in df.columns:
        if c not in ("jahr", "monat"):
            df[c] = pd.to_numeric(df[c], errors="coerce")
            df.loc[df[c] <= -900, c] = np.nan  # Sicherheitsnetz, falls -999 auftaucht
    return df


def build_summer_means(cache_dir: Path, session: requests.Session, years: range) -> tuple[pd.DataFrame, list[str]]:
    frames = []
    for m, fname in MONTHS.items():
        path = fetch_to_file(BASE_URL + fname, cache_dir / fname, session, timeout=120)
        df = read_regional_file(path)
        assert (df["monat"] == m).all(), f"{fname}: unerwartete Monatsspalte"
        frames.append(df.drop(columns="monat").set_index("jahr"))
    cols = frames[0].columns
    for f in frames[1:]:
        assert list(f.columns) == list(cols), "Spalten der Monatsdateien unterscheiden sich"
    stacked = pd.concat(frames, keys=list(MONTHS), names=["monat", "jahr"])
    # nur Jahre mit allen drei Monaten
    n_months = stacked.groupby(level="jahr").count()
    summer = stacked.groupby(level="jahr").mean()
    summer = summer.where(n_months == 3)
    summer = summer.loc[[y for y in summer.index if years.start <= y < years.stop]]

    notes = []
    missing_years = [y for y in years if y not in summer.index]
    if missing_years:
        notes.append(f"Jahre ohne vollständige Jun/Jul/Aug-Daten: {missing_years}")

    rows = []
    for bl, (col, _) in MAPPING.items():
        if col not in summer.columns:
            notes.append(f"Spalte '{col}' für {bl} fehlt in den DWD-Dateien")
            continue
        for y, v in summer[col].items():
            if pd.notna(v):
                rows.append(dict(jahr=int(y), bundesland=bl, t_sommer=round(float(v), 2)))
    out = pd.DataFrame(rows).sort_values(["jahr", "bundesland"]).reset_index(drop=True)
    return out, notes


def plausibilisierung(out: pd.DataFrame, cache_dir: Path, session: requests.Session) -> pd.DataFrame:
    rows = []
    for bl, sid, name in PLAUSI_STATIONS:
        tmk = load_tmk(sid, cache_dir, session)
        st = []
        for y in range(1992, 2021):
            days = pd.date_range(f"{y}-06-01", f"{y}-08-31", freq="D")
            v = tmk.reindex(days)
            if v.isna().sum() <= 5:
                st.append((y, float(v.mean())))
        st = pd.Series(dict(st), name="station")
        ref = out[out["bundesland"] == bl].set_index("jahr")["t_sommer"]
        both = pd.concat([st, ref.rename("gebietsmittel")], axis=1).dropna()
        diff = both["station"] - both["gebietsmittel"]
        rows.append(
            dict(
                bundesland=bl,
                dwd_spalte=MAPPING[bl][0],
                station_id=sid,
                station=name,
                jahre=f"{both.index.min()}–{both.index.max()}",
                n=len(both),
                diff_mittel_K=round(float(diff.mean()), 2),
                diff_std_K=round(float(diff.std(ddof=1)), 2),
                korrelation=round(float(both["station"].corr(both["gebietsmittel"])), 3),
            )
        )
    return pd.DataFrame(rows)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cache-dir", type=Path, default=default_cache_dir())
    ap.add_argument("--out-dir", type=Path, default=Path(__file__).resolve().parents[2] / "data" / "kalibrierung")
    ap.add_argument("--years", type=int, nargs=2, default=DEFAULT_YEARS, metavar=("VON", "BIS"))
    ap.add_argument("--plausibilisierung", action="store_true", help="Kombi-Spalten gegen Stationsdaten prüfen")
    args = ap.parse_args(argv)

    years = range(args.years[0], args.years[1] + 1)
    args.cache_dir.mkdir(parents=True, exist_ok=True)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    session = requests.Session()
    session.headers["User-Agent"] = "kap2-kalibrierung/1.0 (DWD opendata)"

    out, notes = build_summer_means(args.cache_dir, session, years)
    out_path = args.out_dir / "sommermittel_bundesland.csv"
    out.to_csv(out_path, index=False, float_format="%.2f")

    zuord = pd.DataFrame(
        [dict(bundesland=bl, dwd_spalte=col, hinweis=hint) for bl, (col, hint) in MAPPING.items()]
    )
    zuord_path = args.out_dir / "sommermittel_bundesland_zuordnung.csv"
    zuord.to_csv(zuord_path, index=False)

    print(f"Jahre: {out['jahr'].min()}–{out['jahr'].max()}, Zeilen: {len(out)}, Länder: {out['bundesland'].nunique()}")
    for n in notes:
        print(f"  [hinweis] {n}")
    pd.set_option("display.width", 200)
    wide = out.pivot(index="jahr", columns="bundesland", values="t_sommer")
    print(wide[["Deutschland", "Bayern", "Berlin", "Hamburg", "Nordrhein-Westfalen"]].loc[[y for y in (2003, 2018, 2019, 2022, 2023, 2024, 2025) if y in wide.index]].to_string())
    print(f"\nGeschrieben: {out_path}\n             {zuord_path}")

    if args.plausibilisierung:
        pl = plausibilisierung(out, args.cache_dir, session)
        pl_path = args.out_dir / "sommermittel_plausibilisierung.csv"
        pl.to_csv(pl_path, index=False)
        print("\n=== Plausibilisierung Kombi-Spalten (Station − Gebietsmittel, 1992–2020) ===")
        print(pl.to_string(index=False))
        print(f"Geschrieben: {pl_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
