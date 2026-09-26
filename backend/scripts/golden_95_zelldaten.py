"""Gepinnte Zelldaten für den Golden-Test der Beträge #95 (Bericht §3.0 und Tabelle §3.3).

Schreibt je Beispielkommune alle bewohnten 100-m-Zellen innerhalb der Gemeindegrenze (VG250 [65]) mit
den Eingängen, die der Jahresbetrag #95 braucht, nach
``backend/data/kalibrierung/golden95_zellen_<AGS>.csv.gz``:

  gitter_id, einwohner            Zensus-2022-Gitter 100 m [67], Datensatz „population“
  anteil_ueber65                  Datensatz „share_over_65“ (leer = geheimgehalten „–“)
  a65bis69 … a90undaelter         Datensatz „age_groups“, die sechs 5er-Jahresgruppen ab 65
  t_sommer                        Sommermittel Juni–August aus dem DWD-Raster 1 km [33], zehn jüngste Jahre
  hitzetage                       Hitzetage aus dem DWD-Raster 1 km [33], zehn jüngste Jahre

Eine Zusatzzeile ``gitter_id = __ausserhalb__`` (einwohner 0) trägt die Summe der sechs Gruppen ab 65
aller Zellen im Rechteck um die Gemeinde, die außerhalb der Grenze liegen. Der Loader bildet die
gebietsweite Aufteilung der Menschen ab 65 (``_area_senior_split``) aus diesem Rechteck; mit der
Zusatzzeile ergibt sie sich aus der Anlage genau so wie im Zelllauf des Berichts.

Geladen wird wie im Zelllauf des Berichts, mit denselben Funktionen aus
``docs/methodik/anlagen/95_zellvergleich.py`` (Gemeindegebiet, Zensus-Gitter, DWD-Raster); fehlt ein
Rasterwert, gilt wie dort der Wert am Punkt der Kette.

Aufruf (aus dem Repo-Wurzelverzeichnis, Interpreter der Projektumgebung):
    ~/.venvs/kap2/bin/python backend/scripts/golden_95_zelldaten.py --gemeinde 11000000 --gemeinde 03256034
        [--cache VERZEICHNIS] [--bis-jahr JAHR]
"""
from __future__ import annotations

import argparse
import csv
import gzip
import importlib.util
import io
import os
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
ZELLVERGLEICH = REPO / "docs" / "methodik" / "anlagen" / "95_zellvergleich.py"
ZIEL = REPO / "backend" / "data" / "kalibrierung"
SPALTEN65 = ("a65bis69", "a70bis74", "a75bis79", "a80bis84", "a85bis89", "a90undaelter")
KOPF = ("gitter_id", "einwohner", "anteil_ueber65", *SPALTEN65, "t_sommer", "hitzetage")
AUSSERHALB = "__ausserhalb__"


def _zellvergleich():
    spec = importlib.util.spec_from_file_location("zellvergleich_95", ZELLVERGLEICH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _zahl(v) -> str:
    if v is None:
        return ""
    f = float(v)
    return str(int(f)) if f == int(f) else repr(f)


def zellen_schreiben(zv, ags: str, cache: Path, bis_jahr: int) -> Path:
    config = zv.REPO / "backend" / "app" / "config.py"
    vg250_url = zv._literal_aus_datei(config, "VG250_GPKG_URL")
    dwd = zv.DwdRaster(cache, zv._literal_aus_datei(config, "DWD_CDC_MONTHLY_BASE"),
                       zv._literal_aus_datei(config, "DWD_CDC_GRID_BASE"), bis_jahr,
                       zv._literal_aus_datei(config, "DWD_CDC_CLIMATOLOGY_YEARS"))

    polys, name, stand = zv.gemeindegebiet(ags, cache, vg250_url)
    ringe3035 = [[zv.LAEA3035.vor(*zv.UTM32.zurueck(x, y)) for x, y in r] for p in polys for r in p]
    innen = zv.Innen(ringe3035)
    xmin, ymin, xmax, ymax = innen.bbox
    bbox = (int(xmin) - 150, int(ymin) - 150, int(xmax) + 150, int(ymax) + 150)

    zl = zv.zensus_loader_laden(cache)
    zensus = {k: zl.load_dataset_bbox(k, bbox) for k in ("population", "share_over_65", "age_groups")}
    gids = sorted(gid for gid, r in zensus["population"].items()
                  if (r.get("Einwohner") or 0) > 0 and innen(r["x"], r["y"]))
    gset = set(gids)

    geo = [zv.LAEA3035.zurueck(zensus["population"][g]["x"], zensus["population"][g]["y"]) for g in gids]
    gk3 = [zv.wgs84_zu_gk3(lon, lat) for lon, lat in geo]
    t_zelle = dwd.klimatologie([f"air_temp_mean_{m:02d}" for m in (6, 7, 8)], gk3)
    hd_zelle = dwd.klimatologie(["hot_days"], gk3)

    # Rückfall für Zellen ohne Rasterwert: Punkt der Kette wie im Zellvergleich
    if ags in zv.KETTENPUNKT:
        lat_p, lon_p = zv.KETTENPUNKT[ags]
    else:
        gross = max(ringe3035, key=lambda r: zv.flaeche_km2([[r]]))
        lon_p, lat_p = zv.LAEA3035.zurueck(sum(x for x, _ in gross) / len(gross),
                                           sum(y for _, y in gross) / len(gross))
    px, py = zv.wgs84_zu_gk3(lon_p, lat_p)
    t_punkt = round(sum(round(dwd.am_punkt(f"air_temp_mean_{m:02d}", px, py), 1) for m in (6, 7, 8)) / 3, 2)
    hd_punkt = round(dwd.am_punkt("hot_days", px, py), 1)

    aussen = {c: 0.0 for c in SPALTEN65}
    for gid, parsed in zensus["age_groups"].items():
        if gid not in gset:
            for c in SPALTEN65:
                aussen[c] += float(parsed.get(c) or 0.0)

    ziel = ZIEL / f"golden95_zellen_{ags}.csv.gz"
    # Inhalt erst sammeln, dann ohne Zeitstempel packen: gleiche Daten ergeben dieselbe Datei.
    fh = io.StringIO()
    w = csv.writer(fh, lineterminator="\n")
    w.writerow(KOPF)
    for gid, t, hd in zip(gids, t_zelle, hd_zelle):
        ag = zensus["age_groups"].get(gid, {})
        w.writerow([gid, _zahl(zensus["population"][gid]["Einwohner"]),
                    _zahl(zensus["share_over_65"].get(gid, {}).get("AnteilUeber65")),
                    *(_zahl(ag.get(c)) for c in SPALTEN65),
                    _zahl(t if t is not None else t_punkt), _zahl(hd if hd is not None else hd_punkt)])
    w.writerow([AUSSERHALB, "0", "", *(_zahl(aussen[c]) for c in SPALTEN65), "", ""])
    with open(ziel, "wb") as roh, gzip.GzipFile(filename="", mode="wb", fileobj=roh,
                                                compresslevel=9, mtime=0) as gz:
        gz.write(fh.getvalue().encode("utf-8"))
    print(f"{ags} {name} (VG250 {stand}): {len(gids)} Zellen, "
          f"{sum(float(zensus['population'][g]['Einwohner']) for g in gids):.0f} Einwohner, "
          f"DWD {dwd.jahre_benutzt['air_temp_mean_06'][0]}–{dwd.jahre_benutzt['air_temp_mean_06'][-1]} "
          f"-> {ziel.relative_to(REPO)}")
    return ziel


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--gemeinde", action="append", required=True, help="AGS (8 Stellen), mehrfach")
    ap.add_argument("--cache", default=os.environ.get("KAP3_CACHE",
                                                      str(Path.home() / ".cache" / "kap3" / "95_zellvergleich")))
    ap.add_argument("--bis-jahr", type=int, default=datetime.now(timezone.utc).year - 1)
    args = ap.parse_args()
    zv = _zellvergleich()
    for ags in args.gemeinde:
        zellen_schreiben(zv, ags.strip(), Path(args.cache).expanduser(), args.bis_jahr)


if __name__ == "__main__":
    main()
