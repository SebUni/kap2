#!/usr/bin/env python3
"""Normalperioden-Mittelraster der Sonnenscheindauer (SSD) für #98 §3.2.

Das UV-Modell rechnet die klimaattribuierte Dosisänderung **je Zelle**:

    ΔDosis_z = [SSD_z(1991–2020) − SSD_z(1961–1990)] / SSD_z(1961–1990) · k_UV · a_attr

Dafür braucht das Produkt die beiden Klimanormalperioden-Mittel am Zellstandort.
Die DWD-Jahresraster liegen ab 1961 vor (verifiziert 31.08.2026, Dateimuster
``grids_germany_annual_sunshine_duration_<YYYY>17.asc.gz`` — ohne Unterstrich wie
bei ``precipitation``). Sie zur Laufzeit zu laden wäre unvertretbar (60 Raster
à ~4 MB je Assessment); dieses Skript mittelt sie **einmal** und legt zwei
Mittelraster als Anlage ab. Das Produkt liest nur noch diese Anlage
(``climate/ssd_normalperioden.py``) — die Ressourcen-Regel (§3.4) bleibt gewahrt,
und der Lauf ist mit gepinnten Daten reproduzierbar (§7).

Ausgabe (backend/data/kalibrierung/):
    ssd_normalperioden.npz   ref (1961–1990), neu (1991–2020), Header, Jahreslisten
    ssd_normalperioden.md    Kennzahlen + Abgleich gegen die Gebietsmittel-Anlage

Aufruf: python backend/scripts/kalibrierung/dwd_ssd_normalperioden.py
"""
from __future__ import annotations

import os
import sys

import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, ROOT)
DATA = os.path.join(ROOT, "data", "kalibrierung")

REF_YEARS = range(1961, 1991)      # Klimanormalperiode 1961–1990
NEW_YEARS = range(1991, 2021)      # Klimanormalperiode 1991–2020


def _grids() -> tuple[dict, dict[int, np.ndarray]]:
    """Alle SSD-Jahresraster laden (Downloads werden vom Modul gecacht)."""
    from app.services.climate import dwd_cdc_grid as g

    # sunshine_duration folgt dem „ohne Unterstrich"-Dateimuster.
    g._PARAM_DIR.setdefault("sunshine_duration", "sunshine_duration")
    g._PARAM_NO_UNDERSCORE = frozenset(
        set(g._PARAM_NO_UNDERSCORE) | {"sunshine_duration"})

    header: dict | None = None
    out: dict[int, np.ndarray] = {}
    for year in list(REF_YEARS) + list(NEW_YEARS):
        parsed = g._parse_grid("sunshine_duration", year)
        if parsed is None:
            print(f"  {year}: nicht verfügbar — übersprungen", file=sys.stderr)
            continue
        hdr, arr = parsed
        if header is None:
            header = hdr
        elif (hdr["NCOLS"], hdr["NROWS"]) != (header["NCOLS"], header["NROWS"]):
            raise SystemExit(f"{year}: abweichende Rastergeometrie")
        out[year] = arr
        print(f"  {year} ok", file=sys.stderr)
    if header is None or not out:
        raise SystemExit("Kein SSD-Raster ladbar")
    return header, out


def _mean(grids: dict[int, np.ndarray], years, nodata: float) -> tuple[np.ndarray, list[int]]:
    """Zellweises Mittel über die Jahre; nodata bleibt nodata."""
    used = [y for y in years if y in grids]
    if not used:
        raise SystemExit(f"Keine Jahre für {years}")
    stack = np.stack([grids[y].astype("float64") for y in used])
    mask = np.any(stack == nodata, axis=0)
    mean = stack.mean(axis=0)
    mean[mask] = nodata
    return mean.astype("float32"), used


def main() -> None:
    header, grids = _grids()
    nodata = float(header.get("NODATA_VALUE", -999.0))
    ref, ref_years = _mean(grids, REF_YEARS, nodata)
    neu, neu_years = _mean(grids, NEW_YEARS, nodata)

    valid = (ref != nodata) & (neu != nodata) & (ref > 0)
    delta = np.full(ref.shape, np.nan, dtype="float32")
    delta[valid] = (neu[valid] - ref[valid]) / ref[valid] * 100.0

    os.makedirs(DATA, exist_ok=True)
    np.savez_compressed(
        os.path.join(DATA, "ssd_normalperioden.npz"),
        ref=ref, neu=neu,
        ncols=header["NCOLS"], nrows=header["NROWS"],
        xllcorner=header["XLLCORNER"], yllcorner=header["YLLCORNER"],
        cellsize=header["CELLSIZE"], nodata=nodata,
        ref_years=np.array(ref_years), neu_years=np.array(neu_years),
    )

    # Abgleich gegen die Gebietsmittel-Anlage (dwd_ssd_trend.py, DE +7,82 %).
    d_valid = delta[valid]
    lines = [
        "# SSD-Normalperioden-Mittelraster (#98 §3.2, Zellebene)",
        "",
        f"Quelle: DWD-CDC Jahresraster sunshine_duration (1 km, GK3), "
        f"{len(ref_years)} Jahre 1961–1990 und {len(neu_years)} Jahre 1991–2020.",
        "",
        f"- Rastergeometrie: {int(header['NCOLS'])}×{int(header['NROWS'])} Zellen, "
        f"{float(header['CELLSIZE']):.0f} m",
        f"- Flächenmittel SSD 1961–1990: **{ref[ref != nodata].mean():.1f} h/Jahr**",
        f"- Flächenmittel SSD 1991–2020: **{neu[neu != nodata].mean():.1f} h/Jahr**",
        f"- Flächenmittel der relativen Änderung: **{d_valid.mean():+.2f} %** "
        f"(Median {np.median(d_valid):+.2f} %, Spanne {d_valid.min():+.2f} … "
        f"{d_valid.max():+.2f} %)",
        "",
        "Abgleich mit der Gebietsmittel-Anlage `ssd_trend_region.csv` "
        "(DE +7,82 %): Die Rasterzahlen sind das FLÄCHEN-Mittel der Zellwerte, "
        "die CSV nutzt die DWD-Gebietsmittel-Zeitreihe — kleine Abweichungen sind "
        "erwartbar (unterschiedliche Aggregationswege), die Größenordnung muss "
        "übereinstimmen.",
        "",
        "Verwendung: `app/services/climate/ssd_normalperioden.py` liest die Anlage "
        "und liefert `ssd_at(lon, lat)` → (SSD_ref, SSD_neu) je Zellstandort; "
        "Fallback bei fehlender Anlage/Position: Bundesland-Gebietsmittel aus "
        "`ssd_trend_region.csv` (Bericht §3.6).",
    ]
    with open(os.path.join(DATA, "ssd_normalperioden.md"), "w") as fh:
        fh.write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
