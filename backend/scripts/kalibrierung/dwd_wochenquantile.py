#!/usr/bin/env python3
"""
Empirische Wochen-Anomalie-Quantile q_w je Region (intra-saisonal) aus DWD-Tageswerten.

Hintergrund
-----------
Das Hitzemortalitätsmodell rechnet die 13 Sommerwochen (Juni–August) als

    T_w = T̄_Sommer + q_w ,   w = 1 … 13

wobei q_w die empirischen Quantile der Abweichung des Wochenmittels vom
Sommermittel DESSELBEN Jahres sind (intra-saisonale Streuung). Die
zwischenjährliche Streuung der Sommermittel wird NICHT verwendet, sondern nur
zur Kontrolle mit ausgegeben.

Datenquelle (offen, keyless)
----------------------------
DWD Climate Data Center, historische Tageswerte (KL):
  https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/daily/kl/historical/
  - Stationsliste: KL_Tageswerte_Beschreibung_Stationen.txt
  - Daten:         tageswerte_KL_<id>_<von>_<bis>_hist.zip
                   -> produkt_klima_tag_<von>_<bis>_<id>.txt
  Feld TMK = Tagesmittel der Lufttemperatur in °C, -999 = fehlend.
Lizenz: GeoNutzV / DL-DE->Zero-2.0 (Quellenvermerk: Deutscher Wetterdienst).

Vorgehen
--------
1. Je Region 7 Stationen mit lückenarmen Tagesdaten 1991–2020 (Regionen-
   zuschnitt wie Winklmayr u. a. 2022, Dtsch Arztebl Int 119: 451–7).
2. Je Station und Jahr: Sommer = 1. Juni … 31. August (92 Tage) ->
   13 Wochenblöcke à 7 Tage (Tage 1–7, 8–14, …, 85–91; Tag 92 verworfen) ->
   Wochenmittel; Sommermittel = Mittel der 13 Wochenmittel;
   Anomalie = Wochenmittel − Sommermittel.
   Jahre mit > 5 fehlenden Tagen im Sommer werden verworfen.
3. Je Region werden alle Anomalien gepoolt (Stationen × Jahre × 13 Wochen);
   Quantile an p_w = (w − 0,5)/13 (lineare Interpolation, numpy-Default).
   Vergleich: Gauß-Quantile σ·Φ⁻¹(p_w).

Ausgabe (--out-dir, Default backend/data/kalibrierung/)
-------------------------------------------------------
  wochenquantile_region.csv     region, w, p, q_w_emp, q_w_gauss
  wochenquantile_meta.csv       region, stations, n_station_years, sigma, skew,
                                sigma_interannual (+ Zusatzspalten)
  wochenquantile_stationen.csv  Stationsdetails (gültige Jahre, Lücken, σ je Station)

Rohdaten-Zips werden NICHT ins Repository gelegt, sondern in --cache-dir
(Default: $KAP2_DWD_CACHE oder <tempdir>/kap2_dwd). Wiederholte Läufe laden nichts neu.

Aufruf:
  python backend/scripts/kalibrierung/dwd_wochenquantile.py \
      --cache-dir /pfad/zum/cache [--out-dir ...] [--years 1991 2020]
"""
from __future__ import annotations

import argparse
import io
import os
import re
import sys
import tempfile
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
import requests
from scipy.stats import norm, skew as sp_skew

BASE_URL = (
    "https://opendata.dwd.de/climate_environment/CDC/observations_germany/"
    "climate/daily/kl/historical/"
)
STATION_LIST_FILE = "KL_Tageswerte_Beschreibung_Stationen.txt"
LISTING_CACHE_FILE = "kl_hist_listing.html"

N_WEEKS = 13
DAYS_PER_WEEK = 7
MAX_MISSING_DAYS = 5  # Jahre mit > 5 fehlenden Sommertagen werden verworfen
DEFAULT_YEARS = (1991, 2020)

# Regionen nach Winklmayr u. a. 2022 (Dtsch Arztebl Int):
#   nord : HB, HH, MV, NI, SH
#   mitte: BE, BB, NW, RP, SL, HE, SN, ST, TH
#   sued : BW, BY
# (station_id, Name, Bundesland-Kürzel). IDs geprüft gegen die DWD-Stationsliste
# (Stand 2026-08). Hinweis: die im Auftrag genannte ID 1279 ist NICHT Emden,
# sondern Möhrendorf-Kleinseebach (BY); Emden (1219 bis 1998 / 5839 ab 1997) deckt
# 1991–2020 nicht durchgehend ab -> ersetzt durch Norderney 3631 (NI-Küste).
# Schleswig 4466 ergänzt, damit SH in "nord" vertreten ist.
REGIONS: dict[str, list[tuple[int, str, str]]] = {
    "nord": [
        (1975, "Hamburg-Fuhlsbüttel", "HH"),
        (691, "Bremen", "HB"),
        (2014, "Hannover", "NI"),
        (3631, "Norderney", "NI"),
        (4625, "Schwerin", "MV"),
        (1757, "Greifswald", "MV"),
        (4466, "Schleswig", "SH"),
    ],
    "mitte": [
        (433, "Berlin-Tempelhof", "BE"),
        (3987, "Potsdam", "BB"),
        (1420, "Frankfurt/Main", "HE"),
        (2667, "Köln/Bonn", "NW"),
        (1048, "Dresden-Klotzsche", "SN"),
        (1270, "Erfurt-Weimar", "TH"),
        (4336, "Saarbrücken-Ensheim", "SL"),
    ],
    "sued": [
        (3379, "München-Stadt", "BY"),
        (4931, "Stuttgart-Echterdingen", "BW"),
        (3668, "Nürnberg", "BY"),
        (1443, "Freiburg", "BW"),
        (232, "Augsburg", "BY"),
        (4104, "Regensburg", "BY"),
        (2712, "Konstanz", "BW"),
    ],
}


# --------------------------------------------------------------------------- #
# Download / Cache
# --------------------------------------------------------------------------- #
def default_cache_dir() -> Path:
    env = os.environ.get("KAP2_DWD_CACHE")
    if env:
        return Path(env)
    return Path(tempfile.gettempdir()) / "kap2_dwd"


def fetch_to_file(url: str, dest: Path, session: requests.Session, timeout: int = 300) -> Path:
    """Lädt url nach dest, falls dest noch nicht existiert (Download-Cache)."""
    if dest.exists() and dest.stat().st_size > 0:
        return dest
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")
    with session.get(url, stream=True, timeout=timeout) as r:
        r.raise_for_status()
        with open(tmp, "wb") as fh:
            for chunk in r.iter_content(chunk_size=1 << 16):
                fh.write(chunk)
    tmp.replace(dest)
    return dest


def resolve_zip_name(station_id: int, cache_dir: Path, session: requests.Session) -> str:
    """Ermittelt den aktuellen Zip-Dateinamen (Enddatum wechselt jährlich) über das
    Verzeichnislisting; fällt bei Offline-Betrieb auf vorhandene Cache-Dateien zurück."""
    pat = re.compile(rf"tageswerte_KL_{station_id:05d}_\d{{8}}_\d{{8}}_hist\.zip")
    listing = cache_dir / LISTING_CACHE_FILE
    try:
        fetch_to_file(BASE_URL, listing, session, timeout=120)
        names = sorted(set(pat.findall(listing.read_text(errors="replace"))))
        if names:
            return names[-1]
    except requests.RequestException as exc:  # pragma: no cover - Netzfehler
        print(f"  [warn] Listing nicht abrufbar ({exc}); suche im Cache", file=sys.stderr)
    local = sorted(p.name for p in cache_dir.glob("zips/*.zip") if pat.fullmatch(p.name))
    if local:
        return local[-1]
    raise FileNotFoundError(f"Keine Zip-Datei für Station {station_id:05d} gefunden")


def load_station_list(cache_dir: Path, session: requests.Session) -> pd.DataFrame:
    dest = fetch_to_file(BASE_URL + STATION_LIST_FILE, cache_dir / STATION_LIST_FILE, session, 120)
    rows = []
    with open(dest, encoding="latin-1") as fh:
        for line in fh.readlines()[2:]:
            m = re.match(
                r"^(\d{5})\s+(\d{8})\s+(\d{8})\s+(-?\d+)\s+(-?[\d.]+)\s+(-?[\d.]+)\s+(.+?)\s{2,}(\S.*?)\s{2,}",
                line,
            )
            if m:
                rows.append(
                    dict(
                        station_id=int(m.group(1)),
                        von=m.group(2),
                        bis=m.group(3),
                        hoehe_m=int(m.group(4)),
                        lat=float(m.group(5)),
                        lon=float(m.group(6)),
                        name=m.group(7).strip(),
                        bundesland=m.group(8).strip(),
                    )
                )
    return pd.DataFrame(rows).set_index("station_id")


def load_tmk(station_id: int, cache_dir: Path, session: requests.Session) -> pd.Series:
    """Tagesmitteltemperatur TMK (°C) als Series mit DatetimeIndex; -999 -> NaN."""
    zip_name = resolve_zip_name(station_id, cache_dir, session)
    zip_path = fetch_to_file(BASE_URL + zip_name, cache_dir / "zips" / zip_name, session)
    with zipfile.ZipFile(zip_path) as zf:
        member = next(n for n in zf.namelist() if n.startswith("produkt_klima_tag_"))
        raw = zf.read(member)
    df = pd.read_csv(io.BytesIO(raw), sep=";", skipinitialspace=True)
    df.columns = [c.strip() for c in df.columns]
    s = pd.Series(
        df["TMK"].astype(float).values,
        index=pd.to_datetime(df["MESS_DATUM"].astype(str), format="%Y%m%d"),
        name="TMK",
    )
    s = s.where(s > -900)  # -999 = fehlend
    s = s[~s.index.duplicated(keep="first")].sort_index()
    return s


# --------------------------------------------------------------------------- #
# Auswertung
# --------------------------------------------------------------------------- #
def summer_week_means(tmk: pd.Series, year: int) -> tuple[np.ndarray | None, int]:
    """13 Wochenmittel (Tage 1–7, …, 85–91) des Sommers `year`; Tag 92 verworfen.
    Rückgabe (wochenmittel | None, anzahl_fehlender_tage). None bei > MAX_MISSING_DAYS."""
    days = pd.date_range(f"{year}-06-01", f"{year}-08-31", freq="D")  # 92 Tage
    vals = tmk.reindex(days).to_numpy(dtype=float)
    n_missing = int(np.isnan(vals).sum())
    if n_missing > MAX_MISSING_DAYS:
        return None, n_missing
    block = vals[: N_WEEKS * DAYS_PER_WEEK].reshape(N_WEEKS, DAYS_PER_WEEK)
    with np.errstate(all="ignore"):
        week_means = np.nanmean(block, axis=1)
    if np.isnan(week_means).any():  # kann bei <= 5 Lücken nicht passieren, Sicherheitsnetz
        return None, n_missing
    return week_means, n_missing


def evaluate_station(
    station_id: int, name: str, region: str, tmk: pd.Series, years: range
) -> tuple[pd.DataFrame, dict]:
    """Anomalien (long) und Stationskennzahlen für eine Station."""
    rows = []
    summer_means: dict[int, float] = {}
    dropped = []
    missing_total = 0
    for y in years:
        wk, n_miss = summer_week_means(tmk, y)
        if wk is None:
            dropped.append(f"{y}({n_miss})")
            continue
        missing_total += n_miss
        t_sommer = float(wk.mean())
        summer_means[y] = t_sommer
        for w in range(N_WEEKS):
            rows.append(
                dict(
                    region=region,
                    station_id=station_id,
                    jahr=y,
                    w=w + 1,
                    t_woche=float(wk[w]),
                    t_sommer=t_sommer,
                    anomalie=float(wk[w] - t_sommer),
                )
            )
    anom = pd.DataFrame(rows)
    sm = pd.Series(summer_means, dtype=float)
    info = dict(
        region=region,
        station_id=station_id,
        station=name,
        n_jahre_gueltig=int(len(sm)),
        jahre_verworfen=" ".join(dropped) if dropped else "",
        fehltage_summe_gueltige_jahre=missing_total,
        t_sommer_mittel=float(sm.mean()) if len(sm) else np.nan,
        sigma_intra=float(anom["anomalie"].std(ddof=1)) if len(anom) else np.nan,
        sigma_interannual=float(sm.std(ddof=1)) if len(sm) > 1 else np.nan,
    )
    return anom, info, sm


def region_quantiles(anoms: np.ndarray) -> pd.DataFrame:
    w = np.arange(1, N_WEEKS + 1)
    p = (w - 0.5) / N_WEEKS
    sigma = float(np.std(anoms, ddof=1))
    q_emp = np.quantile(anoms, p)  # lineare Interpolation
    q_gauss = sigma * norm.ppf(p)
    return pd.DataFrame(dict(w=w, p=p, q_w_emp=q_emp, q_w_gauss=q_gauss))


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cache-dir", type=Path, default=default_cache_dir(), help="Ablage der Rohdaten-Zips")
    ap.add_argument(
        "--out-dir",
        type=Path,
        default=Path(__file__).resolve().parents[2] / "data" / "kalibrierung",
        help="Ablage der Ergebnis-CSVs",
    )
    ap.add_argument("--years", type=int, nargs=2, default=DEFAULT_YEARS, metavar=("VON", "BIS"))
    ap.add_argument("--write-anomalies", action="store_true", help="zusätzlich alle Einzel-Anomalien als CSV schreiben")
    args = ap.parse_args(argv)

    years = range(args.years[0], args.years[1] + 1)
    cache_dir: Path = args.cache_dir
    out_dir: Path = args.out_dir
    cache_dir.mkdir(parents=True, exist_ok=True)
    out_dir.mkdir(parents=True, exist_ok=True)
    session = requests.Session()
    session.headers["User-Agent"] = "kap2-kalibrierung/1.0 (DWD opendata)"

    print(f"Cache: {cache_dir}\nAusgabe: {out_dir}\nJahre: {years.start}–{years.stop - 1}")
    stations_meta = load_station_list(cache_dir, session)

    all_anoms: list[pd.DataFrame] = []
    station_rows: list[dict] = []
    summer_by_region: dict[str, dict[int, pd.Series]] = {}

    for region, stations in REGIONS.items():
        summer_by_region[region] = {}
        for sid, name, bl in stations:
            meta_name = stations_meta.loc[sid, "name"] if sid in stations_meta.index else "?"
            print(f"[{region}] {sid:05d} {name} ({bl}; DWD: {meta_name}) …", end=" ", flush=True)
            tmk = load_tmk(sid, cache_dir, session)
            anom, info, sm = evaluate_station(sid, name, region, tmk, years)
            info["bundesland"] = bl
            info["dwd_name"] = meta_name
            info["hoehe_m"] = int(stations_meta.loc[sid, "hoehe_m"]) if sid in stations_meta.index else None
            print(
                f"{info['n_jahre_gueltig']}/{len(years)} Jahre gültig"
                + (f", verworfen: {info['jahre_verworfen']}" if info["jahre_verworfen"] else "")
            )
            all_anoms.append(anom)
            station_rows.append(info)
            summer_by_region[region][sid] = sm

    anom_df = pd.concat(all_anoms, ignore_index=True)
    stations_df = pd.DataFrame(station_rows)[
        [
            "region", "station_id", "station", "bundesland", "dwd_name", "hoehe_m",
            "n_jahre_gueltig", "jahre_verworfen", "fehltage_summe_gueltige_jahre",
            "t_sommer_mittel", "sigma_intra", "sigma_interannual",
        ]
    ]

    q_rows, meta_rows = [], []
    region_keys = list(REGIONS) + ["deutschland"]
    for region in region_keys:
        if region == "deutschland":
            sub = anom_df
            sm_frame = pd.DataFrame({sid: s for r in summer_by_region.values() for sid, s in r.items()})
            st_list = [s for r in REGIONS.values() for s in r]
        else:
            sub = anom_df[anom_df["region"] == region]
            sm_frame = pd.DataFrame(summer_by_region[region])
            st_list = REGIONS[region]
        a = sub["anomalie"].to_numpy()
        q = region_quantiles(a)
        q.insert(0, "region", region)
        q_rows.append(q)

        # zwischenjährliche Streuung (NUR Kontrolle): Regionsmittel je Jahr über Stationen,
        # dann Std über Jahre; zusätzlich Mittel der stationsweisen Std.
        regional_summer = sm_frame.mean(axis=1, skipna=True)
        meta_rows.append(
            dict(
                region=region,
                stations="|".join(f"{sid}:{name}" for sid, name, _ in st_list),
                n_stations=len(st_list),
                n_station_years=int(sub[["station_id", "jahr"]].drop_duplicates().shape[0]),
                n_anomalies=int(len(a)),
                sigma=float(np.std(a, ddof=1)),
                skew=float(sp_skew(a, bias=False)),
                mean_anomaly=float(np.mean(a)),
                t_sommer_mittel=float(regional_summer.mean()),
                sigma_interannual=float(regional_summer.std(ddof=1)),
                sigma_interannual_station_mean=float(sm_frame.std(axis=0, ddof=1).mean()),
            )
        )

    q_df = pd.concat(q_rows, ignore_index=True)
    meta_df = pd.DataFrame(meta_rows)

    q_path = out_dir / "wochenquantile_region.csv"
    meta_path = out_dir / "wochenquantile_meta.csv"
    st_path = out_dir / "wochenquantile_stationen.csv"
    q_df.to_csv(q_path, index=False, float_format="%.4f")
    meta_df.to_csv(meta_path, index=False, float_format="%.4f")
    stations_df.to_csv(st_path, index=False, float_format="%.3f")
    if args.write_anomalies:
        anom_df.to_csv(out_dir / "wochenquantile_anomalien.csv", index=False, float_format="%.3f")

    pd.set_option("display.width", 200)
    print("\n=== Quantile q_w (°C) ===")
    print(q_df.pivot(index="w", columns="region", values="q_w_emp").round(3).to_string())
    print("\n=== Meta ===")
    print(meta_df.drop(columns=["stations"]).round(3).to_string(index=False))
    print(f"\nGeschrieben: {q_path}\n             {meta_path}\n             {st_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
