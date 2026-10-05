"""Gepinnte Zelldaten für den Golden-Test der Beträge #96 (Bericht §3.0, Zelllauf Berlin).

Schreibt je Gemeinde alle bewohnten 100-m-Zellen innerhalb der Gemeindegrenze (VG250 Bericht #95 [65]) mit den
Eingängen, die ``zensus_loader.apply_zensus_to_cell_inputs`` für die Altersbänder von #96 braucht, nach
``backend/data/kalibrierung/golden96_zellen_<AGS>.csv.gz``:

  gitter_id, einwohner            Zensus-2022-Gitter 100 m Bericht #95 [67], Datensatz „population“
  anteil_ueber65                  Datensatz „share_over_65“ (leer = geheimgehalten „–“)
  unter5 … a90undaelter           Datensatz „age_groups“, alle 19 5er-Jahresgruppen
                                  (die vier unter 20 tragen die Aufteilung u20 / 20–64, §3.2)

Anders als die Anlage #95 (``golden_95_zelldaten.py``) trägt diese Anlage auch die 5er-Gruppen unter 65
und keine Klimawerte: #96 rechnet in Berlin mit einer Region (δ gleich in allen Zellen), und der
Vegetationsfaktor P̂ mittelt im Ausgangsstand auf 1 (§3.0 Ebene 7) — die Summe braucht keine OSM-Daten.

Eine Zusatzzeile ``gitter_id = __ausserhalb__`` (einwohner 0) trägt die Summen aller 19 Gruppen der
Zellen im Rechteck um die Gemeinde, die außerhalb der Grenze liegen. Der Loader bildet die gebietsweiten
Rückfälle (``_area_senior_split``, ``_area_u20_share``) aus diesem Rechteck; mit der Zusatzzeile ergeben
sie sich aus der Anlage genau so wie im Zelllauf des Berichts.

Geladen wird wie in der Anlage #95, mit denselben Funktionen aus ``docs/methodik/anlagen/95_zellvergleich.py``
(Gemeindegebiet, Punkt-in-Polygon mit den Zellmitten, Zensus-Gitter).

Aufruf (aus dem Repo-Wurzelverzeichnis, Interpreter der Projektumgebung):
    ~/.venvs/kap2/bin/python backend/scripts/golden_96_zelldaten.py --gemeinde 11000000 [--cache VERZEICHNIS]
"""
from __future__ import annotations

import argparse
import csv
import gzip
import io
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from golden_95_zelldaten import AUSSERHALB, REPO, ZIEL, _zahl, _zellvergleich  # noqa: E402


def zellen_schreiben(zv, ags: str, cache: Path) -> Path:
    config = zv.REPO / "backend" / "app" / "config.py"
    vg250_url = zv._literal_aus_datei(config, "VG250_GPKG_URL")

    polys, name, stand = zv.gemeindegebiet(ags, cache, vg250_url)
    ringe3035 = [[zv.LAEA3035.vor(*zv.UTM32.zurueck(x, y)) for x, y in r] for p in polys for r in p]
    innen = zv.Innen(ringe3035)
    xmin, ymin, xmax, ymax = innen.bbox
    bbox = (int(xmin) - 150, int(ymin) - 150, int(xmax) + 150, int(ymax) + 150)

    zl = zv.zensus_loader_laden(cache)
    spalten = tuple(zl.ALL_AGE_COLUMNS)
    zensus = {k: zl.load_dataset_bbox(k, bbox) for k in ("population", "share_over_65", "age_groups")}
    gids = sorted(gid for gid, r in zensus["population"].items()
                  if (r.get("Einwohner") or 0) > 0 and innen(r["x"], r["y"]))
    gset = set(gids)

    aussen = {c: 0.0 for c in spalten}
    for gid, parsed in zensus["age_groups"].items():
        if gid not in gset:
            for c in spalten:
                aussen[c] += float(parsed.get(c) or 0.0)

    ziel = ZIEL / f"golden96_zellen_{ags}.csv.gz"
    # Inhalt erst sammeln, dann ohne Zeitstempel packen: gleiche Daten ergeben dieselbe Datei.
    fh = io.StringIO()
    w = csv.writer(fh, lineterminator="\n")
    w.writerow(("gitter_id", "einwohner", "anteil_ueber65", *spalten))
    for gid in gids:
        ag = zensus["age_groups"].get(gid, {})
        w.writerow([gid, _zahl(zensus["population"][gid]["Einwohner"]),
                    _zahl(zensus["share_over_65"].get(gid, {}).get("AnteilUeber65")),
                    *(_zahl(ag.get(c)) for c in spalten)])
    w.writerow([AUSSERHALB, "0", "", *(_zahl(aussen[c]) for c in spalten)])
    with open(ziel, "wb") as roh, gzip.GzipFile(filename="", mode="wb", fileobj=roh,
                                                compresslevel=9, mtime=0) as gz:
        gz.write(fh.getvalue().encode("utf-8"))
    print(f"{ags} {name} (VG250 {stand}): {len(gids)} Zellen, "
          f"{sum(float(zensus['population'][g]['Einwohner']) for g in gids):.0f} Einwohner "
          f"-> {ziel.relative_to(REPO)}")
    return ziel


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--gemeinde", action="append", required=True, help="AGS (8 Stellen), mehrfach")
    ap.add_argument("--cache", default=os.environ.get("KAP3_CACHE",
                                                      str(Path.home() / ".cache" / "kap3" / "95_zellvergleich")))
    args = ap.parse_args()
    zv = _zellvergleich()
    for ags in args.gemeinde:
        zellen_schreiben(zv, ags.strip(), Path(args.cache).expanduser())


if __name__ == "__main__":
    main()
