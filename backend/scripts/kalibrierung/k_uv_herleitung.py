#!/usr/bin/env python3
"""#98 §3.2 — Herleitung von k_UV (Ledger-Befunde 230/238/245/252/255/256).

\\(k_{UV}\\) übersetzt eine relative SSD-Änderung in eine relative Änderung der
erythemwirksamen Dosis:  ΔDosis_Zelle = ΔSSD_Zelle · k_UV · a_attr

**Das Skalenproblem.** Der publizierte Dosistrend ist eine **Stations**messung, das
Modell wendet k_UV auf die **Raster**-ΔSSD der Zelle an. Beide Skalen unterscheiden
sich **metrikabhängig** — dieses Skript belegt das an der Messzelle selbst:
Das 1-km-Raster gibt den Stationstrend der *Globalstrahlung* nahezu exakt wieder,
den der *Sonnenscheindauer* nur zu rund 60 %. Ursache laut Quelle: „GR is largely
unaffected by current TCO levels but is primarily influenced by … AOD and cloudiness.
SunD, on the other hand, is mainly influenced by cloudiness alone."

**Die Brücke.** Die Globalstrahlung liegt in **beiden** Messfamilien vor:

    k_UV = (ΔDosis / ΔGlobal)|Station  ×  (ΔGlobal / ΔSSD)|Raster

Beide Quotienten sind skalenfrei; ihr Produkt ist die Elastizität auf Rasterskala.

**Messort ist Bochum, nicht Dortmund (Befund 252).** Lorenz u. a. 2024 messen die UV-
Dosis in Dortmund, Globalstrahlung und Sonnenscheindauer aber an der DWD-Station
**1117 Bochum** („10 km from the UV monitoring station", Kap. 2). Der Rasterquotient
gehört deshalb an die **Bochumer** Zelle.

**Gewichtung mit dem RICHTIGEN Feld (Befund 266).** Das Produktionsmodell
multipliziert k_UV mit der **Normalperioden-ΔSSD** (1961–90 → 1991–2020), nicht mit
dem SSD-Trend 1997–2022. Beide Felder korrelieren nur schwach (r ≈ 0,24). Der
nationale k_UV ist deshalb der mit ``Baseline-Fällen × ΔSSD_Normalperiode``
gewichtete Mittelwert
des Quotienten — genau die Größe, mit der die Zellsummen gebildet werden.

**Bundesweiter Bezug (Befunde 255/256/278).** Das Band kam bis Rev. 6 aus Min/Max über
acht handverlesene Städte — eine *räumliche* Streuung, als Band der *Bundes*summe
gebucht. Richtig ist: Für die Bundessumme zählt der mit **Baseline-Fällen ×
ΔSSD_Normalperiode** gewichtete Rasterquotient über alle Gemeindepunkte — dasselbe
Gewicht, mit dem das Produktionsmodell ΔF summiert (Kopfgewichtung wäre um 1 %
daneben, Befund 278); die
räumliche Streuung ist eine **Modellgrenze** der kommunalen Differenzierung, kein
Bundesband. Das Band selbst kommt aus den **publizierten Standardfehlern** der beiden
Stationstrends.

**Ressourcen-Regel (§3.4).** Punktablesungen auf Gemeindepunkt-Ebene, kein
Vollraster-Lauf.

Ausgaben (backend/data/kalibrierung/):
    k_uv_herleitung.csv   Jahresreihen an der Messzelle + Trends je Gemeindepunkt
    k_uv_herleitung.md    Kette, Band, Modellgrenze, verworfene Varianten

Aufruf: python backend/scripts/kalibrierung/k_uv_herleitung.py
Quellen: Lorenz u. a. 2024, doi:10.1007/s43630-024-00658-8, Tab. 2 und Tab. 4
(Volltext, Open Access); DWD-CDC `sunshine_duration` und `radiation_global` 1 km
(DL-DE->Zero-2.0); BKG VG250 `vg250_pk`; Zensus 2022.
"""
from __future__ import annotations

import csv
import json
import os
import sqlite3
import sys

import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, ROOT)
DATA = os.path.join(ROOT, "data", "kalibrierung")
GPKG = os.path.join(ROOT, "data", "vg250", "DE_VG250.gpkg")
GEMEINDEN = os.path.join(ROOT, "data", "lite", "zensus_gemeinde.json")
RAD_CACHE = os.path.expanduser("~/.cache/kap2-kalibrierung/rad")
RAD_BASE = ("https://opendata.dwd.de/climate_environment/CDC/grids_germany/"
            "annual/radiation_global/")

JAHRE = list(range(1997, 2023))       # Messfenster von Lorenz u. a. 2024

# ── Publizierte Stationstrends, Lorenz u. a. 2024 (Volltext) ─────────────────
# Tab. 2: UV-Messung Dortmund. Tab. 4: GR/SunD/TCO an DWD-Station 1117 Bochum.
DOSIS = 4.9;      DOSIS_SE = 1.8     # H_er,day  %/Dek., Tab. 2 (CI 1,4–8,4)
GLOBAL = 4.6;     GLOBAL_SE = 1.5    # GR_int    %/Dek., Tab. 4 (CI 1,6–7,7)
SUND_STATION = 11.3                  # SunD      %/Dek., Tab. 4 (CI 6,7–15,9)
TCO_SOMMER = -0.9                    # TCO Apr–Sept %/Dek., Tab. 4, signifikant

STATION = (7.2050, 51.4842)          # DWD 1117 Bochum — Messort von GR und SunD
NRW_GEBIETSMITTEL = 5.81             # %/Dek., Anlage [69] — Nenner bis Rev. 3


def _rad_grid(jahr: int):
    """Globalstrahlungs-Jahresraster (.zip mit ``[header]``-Sektion, eigener Leser)."""
    import io
    import urllib.request
    import zipfile

    os.makedirs(RAD_CACHE, exist_ok=True)
    pfad = os.path.join(RAD_CACHE, f"{jahr}.asc")
    if not os.path.exists(pfad):
        roh = urllib.request.urlopen(
            RAD_BASE + f"grids_germany_annual_radiation_global_{jahr}.zip",
            timeout=180).read()
        zf = zipfile.ZipFile(io.BytesIO(roh))
        name = [x for x in zf.namelist() if x.lower().endswith(".asc")][0]
        with open(pfad, "wb") as fh:
            fh.write(zf.read(name))
    hdr: dict[str, float] = {}
    rows: list[list[float]] = []
    for line in open(pfad, encoding="latin-1"):
        t = line.strip()
        if not t or t.startswith("["):
            continue
        teile = t.split()
        if (len(teile) == 2 and teile[0].upper() in
                ("NCOLS", "NROWS", "XLLCORNER", "YLLCORNER", "CELLSIZE",
                 "NODATA_VALUE")):
            hdr[teile[0].upper()] = float(teile[1])
        elif "=" not in t or len(teile) > 2:
            try:
                rows.append([float(v) for v in teile])
            except ValueError:
                pass
    return hdr, np.array(rows)


def _ssd_grid(jahr: int):
    from app.services.climate import dwd_cdc_grid as g

    g._PARAM_DIR.setdefault("sunshine_duration", "sunshine_duration")
    g._PARAM_NO_UNDERSCORE = frozenset(
        set(g._PARAM_NO_UNDERSCORE) | {"sunshine_duration"})
    parsed = g._parse_grid("sunshine_duration", jahr)
    if parsed is None:
        raise SystemExit(f"FEHLER: SSD-Raster {jahr} fehlt.")
    return parsed


def _trend(reihe: list[float]) -> float:
    """Relativer Trend in %/Dekade (lineare Regression ÷ Mittel)."""
    arr = np.array(reihe)
    return float(np.polyfit(JAHRE, arr, 1)[0] * 10 / arr.mean() * 100)


def gemeindepunkte() -> list[tuple[str, float, float, float]]:
    con = sqlite3.connect(GPKG)
    try:
        rows = con.execute("SELECT AGS, LON_DEZ, LAT_DEZ FROM vg250_pk "
                           "WHERE AGS IS NOT NULL AND LON_DEZ IS NOT NULL").fetchall()
    finally:
        con.close()
    pop = json.load(open(GEMEINDEN, encoding="utf-8"))
    out = []
    for ags, lon, lat in rows:
        a = str(ags).zfill(8)
        p = (pop.get(a) or {}).get("population")
        if p:
            out.append((a, float(lon), float(lat), float(p)))
    return out


def _o65(punkte) -> "np.ndarray":
    """65+-Anteil je Gemeinde (Zensus-Aggregat des Produkts)."""
    gem = json.load(open(GEMEINDEN, encoding="utf-8"))
    return np.array([((gem.get(a) or {}).get("share_over_65") or 0.0) / 100.0
                     for a, *_ in punkte])


def main() -> None:
    from pyproj import Transformer

    tr = Transformer.from_crs("EPSG:4326", "EPSG:31467", always_xy=True)
    punkte = gemeindepunkte()
    xy = [tr.transform(x, y) for _, x, y, _ in punkte]
    sx, sy = tr.transform(*STATION)

    reihen: dict[str, dict] = {}
    for key, loader in (("ssd", _ssd_grid), ("rad", _rad_grid)):
        station: list[float] = []
        zellen: list[list[float]] = [[] for _ in punkte]
        for jahr in JAHRE:
            hdr, arr = loader(jahr)
            def lies(x: float, y: float) -> float:
                col = int((x - hdr["XLLCORNER"]) / hdr["CELLSIZE"])
                row = int((y - hdr["YLLCORNER"]) / hdr["CELLSIZE"])
                return float(arr[arr.shape[0] - 1 - row, col])
            station.append(lies(sx, sy))
            for i, (X, Y) in enumerate(xy):
                zellen[i].append(lies(X, Y))
        reihen[key] = {"station": station, "zellen": zellen}

    t_stat = {k: _trend(v["station"]) for k, v in reihen.items()}
    t_ssd = np.array([_trend(z) for z in reihen["ssd"]["zellen"]])
    t_rad = np.array([_trend(z) for z in reihen["rad"]["zellen"]])
    gew = np.array([p for *_, p in punkte])
    # AGGREGATIONSREGEL (§3.9; Befund 297). Seit der Umstellung auf die
    # Fallgewichtung (Befunde 266/278) ist q ein gewichtetes MITTEL DER
    # PUNKTQUOTIENTEN — nicht mehr ein Quotient getrennt summierter Zaehler und
    # Nenner. Damit schlagen Punkte mit verschwindendem SSD-Trend voll durch: 57
    # Punkte (0,08 % Gewicht) erreichen q bis 196 und heben den Bundeswert um
    # +2,3 %. Sie werden deshalb AUSGESCHLOSSEN — ihr Quotient ist numerisch
    # instabil, nicht klein. Schwelle: SSD-Trend >= 1 %/Dekade.
    gilt = np.isfinite(t_ssd) & np.isfinite(t_rad) & (t_ssd > 0)
    stabil = gilt & (t_ssd > 1.0)      # >= 1 %/Dekade SSD-Trend
    # Auf vier Nachkommastellen gefuehrt: Bericht, Registry und Anlage rechnen damit
    # dieselbe Kette (keine Rundungsdivergenz, Befund-213-Klasse).
    # Befund 266: Gewichtet wird mit pop x Normalperioden-DeltaSSD — dem Feld, mit
    # dem das Produktionsmodell k_UV multipliziert —, nicht mit dem SSD-Trend.
    from app.services.climate import ssd_normalperioden as snp
    d_norm = np.array([
        ((pr[1] - pr[0]) / pr[0]) if (pr := snp.ssd_at(lon, lat)) and pr[0] > 0
        else np.nan
        for _, lon, lat, _ in punkte])
    gilt = gilt & np.isfinite(d_norm) & (d_norm > 0)
    stabil = stabil & np.isfinite(d_norm) & (d_norm > 0)
    q_pkt = t_rad[stabil] / t_ssd[stabil]
    q_zelle = q_pkt
    # Befund 278: Gewichtet wird mit BASELINE-FAELLEN x DeltaSSD, nicht mit Koepfen —
    # das Produktionsmodell summiert DeltaF = F_z x BAF x DeltaDosis_z. Weil die
    # Altersstruktur regional variiert, sind Kopf- und Fallgewicht nicht identisch
    # (+0,8 % MM / +1,2 % C44). Die beiden Entitaeten ergaeben leicht verschiedene q;
    # gefuehrt wird das mit ihrem EUR-Anteil gewichtete Mittel, die Restdifferenz
    # (< 0,2 %) ist als Naeherung gekennzeichnet.
    from app.services.engine.impact.health import (UV_INCIDENCE_C44,
                                                   UV_INCIDENCE_MM)
    from app.services.zensus_loader import (NATIONAL_SENIOR_SPLIT,
                                            NATIONAL_U20_SHARE_OF_U65)
    o65 = _o65(punkte)
    u65, p65 = gew * (1 - o65), gew * o65
    bands = {"u20": u65 * NATIONAL_U20_SHARE_OF_U65,
             "a20_64": u65 * (1 - NATIONAL_U20_SHARE_OF_U65),
             "a65_74": p65 * NATIONAL_SENIOR_SPLIT["a65_74"],
             "a75_84": p65 * NATIONAL_SENIOR_SPLIT["a75_84"],
             "a85p": p65 * NATIONAL_SENIOR_SPLIT["a85p"]}
    f_mm = sum(bands[b] * UV_INCIDENCE_MM[b] / 1e5 for b in bands)
    f_c44 = sum(bands[b] * UV_INCIDENCE_C44[b] / 1e5 for b in bands)
    q_mm = float(((f_mm[stabil] * d_norm[stabil]) * q_pkt).sum()
                 / (f_mm[stabil] * d_norm[stabil]).sum())
    q_c44 = float(((f_c44[stabil] * d_norm[stabil]) * q_pkt).sum()
                  / (f_c44[stabil] * d_norm[stabil]).sum())
    # EUR-Anteil der Entitaeten — HERGELEITET, nicht gesetzt (Befund 290):
    # Anteil_e = dF_e x (c_e + lambda_e x L_e x VOLY) / Summe. Der Wert haengt nur
    # von Anker, BAF, Kostensatz, Letalitaet und L ab, nicht von k_UV (das kuerzt
    # sich heraus) — er ist damit stabil gegenueber der Kette, die ihn benutzt.
    _ANKER = {"mm": (26_140 + 27_040 + 27_430) / 3,
              "c44": (236_670 + 243_430 + 242_820) / 3}
    _LAM = {"mm": (2928 + 3146 + 3169) / 3 / _ANKER["mm"],
            "c44": (1178 + 1275 + 1332) / 3 / _ANKER["c44"]}
    _L = {"mm": 10.4569, "c44": 5.4787}
    _BAF = {"mm": 0.6, "c44": 1.675}
    _C = {"mm": 6724.0, "c44": 5883.0}
    _eur = {e: _ANKER[e] * _BAF[e] * (_C[e] + _LAM[e] * _L[e] * 160_800.0)
            for e in _ANKER}
    EUR_ANTEIL_MM = _eur["mm"] / sum(_eur.values())
    q_de = round(EUR_ANTEIL_MM * q_mm + (1 - EUR_ANTEIL_MM) * q_c44, 4)
    q_kopf = float(((gew[stabil] * d_norm[stabil]) * q_pkt).sum()
                   / (gew[stabil] * d_norm[stabil]).sum())
    # Ergebnis-Sensitivitaet der Ausschluss-Schwelle (§3.9; Befund 339). Bis
    # Rev. 13 wurde hier ein einzelner Vergleichswert berechnet und nirgends
    # verwendet — ein gesetzter Parameter, der 2,3 % des Ergebnisses bewegt,
    # trug damit weder Herleitung noch Band noch Sensitivitaet. Jetzt wird die
    # ganze Reihe **€-gewichtet** (wie q_de selbst) gerechnet und gedruckt.
    def _q_bei(schwelle: float) -> tuple[float, int]:
        m = gilt & (t_ssd > schwelle)
        if not m.any():
            return float("nan"), 0
        # q_pkt ist auf `stabil` gefiltert — je Schwelle neu bilden.
        qp = t_rad[m] / t_ssd[m]
        qm = float(((f_mm[m] * d_norm[m]) * qp).sum()
                   / (f_mm[m] * d_norm[m]).sum())
        qc = float(((f_c44[m] * d_norm[m]) * qp).sum()
                   / (f_c44[m] * d_norm[m]).sum())
        return EUR_ANTEIL_MM * qm + (1 - EUR_ANTEIL_MM) * qc, int(m.sum())

    SCHWELLEN = (0.0, 0.25, 0.5, 1.0, 2.0, 3.0)
    q_trend_gew = float((gew[gilt] * t_rad[gilt]).sum()
                        / (gew[gilt] * t_ssd[gilt]).sum())
    korr = float(np.corrcoef(t_ssd[gilt], d_norm[gilt])[0, 1])
    q_station = t_stat["rad"] / t_stat["ssd"]

    stationsquotient = DOSIS / GLOBAL
    k_uv = stationsquotient * q_de
    # Band: publizierte Standardfehler beider Stationstrends, unkorreliert
    # fortgepflanzt (konservativ — beide Reihen sind bewoelkungsgetrieben und
    # damit positiv korreliert, die reale Unsicherheit ist kleiner).
    rel = float(np.hypot(DOSIS_SE / DOSIS, GLOBAL_SE / GLOBAL))
    band = (round(k_uv * (1 - rel), 4), round(k_uv * (1 + rel), 4))

    with open(os.path.join(DATA, "k_uv_herleitung.csv"), "w", newline="",
              encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["groesse", "wert", "einheit", "quelle"])
        for name, val, src in (
                ("dosis_station_prozent_dekade", DOSIS, "Lorenz 2024 Tab. 2"),
                ("global_station_prozent_dekade", GLOBAL, "Lorenz 2024 Tab. 4"),
                ("sund_station_prozent_dekade", SUND_STATION, "Lorenz 2024 Tab. 4"),
                ("ssd_raster_messzelle_prozent_dekade", t_stat["ssd"], "DWD 1 km"),
                ("global_raster_messzelle_prozent_dekade", t_stat["rad"], "DWD 1 km"),
                ("rasterquotient_messzelle", q_station, "berechnet"),
                ("rasterquotient_de_fallgew", q_de, "berechnet, Baseline-Faelle x dSSD"),
                ("stationsquotient", stationsquotient, "Tab. 2 / Tab. 4"),
                ("k_uv", k_uv, "berechnet"),
                ("k_uv_band_unten", band[0], "SE-Fortpflanzung"),
                ("k_uv_band_oben", band[1], "SE-Fortpflanzung")):
            w.writerow([name, f"{val:.4f}", "%/Dek. bzw. -", src])

    p = []
    p.append("# #98 — Herleitung von k_UV (Befunde 230/238/245/252/255/256)\n")
    p.append("Erzeugt von `backend/scripts/kalibrierung/k_uv_herleitung.py`. "
             f"Fenster **{JAHRE[0]}–{JAHRE[-1]}**, identisch zu Lorenz u. a. 2024.\n")
    p.append("## 1 Die Skalen unterscheiden sich metrikabhängig\n")
    p.append("Messzelle = DWD-Station **1117 Bochum**, an der die Quelle "
             "Globalstrahlung und Sonnenscheindauer misst (die UV-Dosis wird 10 km "
             "entfernt in Dortmund gemessen).\n")
    p.append("| Größe | Station (Lorenz, Tab. 4) | 1-km-Raster an der Messzelle | Raster ÷ Station |")
    p.append("|---|---|---|---|")
    p.append(f"| Globalstrahlung (GR_int) | {GLOBAL:.1f} %/Dek. | "
             f"{t_stat['rad']:.2f} %/Dek. | **{t_stat['rad']/GLOBAL:.2f}** |")
    p.append(f"| Sonnenscheindauer (SunD) | {SUND_STATION:.1f} %/Dek. | "
             f"{t_stat['ssd']:.2f} %/Dek. | **{t_stat['ssd']/SUND_STATION:.2f}** |")
    p.append("")
    p.append("Das Raster gibt die **Globalstrahlung** nahezu exakt wieder, die "
             "**Sonnenscheindauer** nur zu rund 60 %. Eine direkte Paarung "
             "Stations-Zähler ÷ Raster-SSD-Nenner wäre deshalb ein Kategorienfehler "
             "(§3.9). Die Quelle nennt den physikalischen Grund: GR ist von AOD und "
             "Bewölkung bestimmt, SunD allein von Bewölkung — und die "
             "Rasterinterpolation glättet die Schwellenwert-Größe SunD stärker.\n")
    p.append("## 2 Die Brücke\n")
    p.append("$$ k_{UV} = \\frac{\\Delta Dosis}{\\Delta Global}\\bigg|_{Station} "
             "\\times \\frac{\\Delta Global}{\\Delta SSD}\\bigg|_{Raster} $$\n")
    p.append(f"- **Stationsquotient = {DOSIS:.1f} ÷ {GLOBAL:.1f} = "
             f"{stationsquotient:.4f}** — beide Werte publiziert (Tab. 2 bzw. Tab. 4). "
             "Das ist die quantitative Fassung der Abstract-Aussage 》Global radiation "
             "increases similarly to the UV data《.")
    # Es gehen die STABILEN Punkte ein (Befund 297) — nicht alle mit dSSD > 0.
    n_txt = f"{int(stabil.sum()):,}".replace(",", ".")
    p.append(f"- **Rasterquotient = {q_de:.4f}**, gewichtet mit "
             f"``Baseline-Fällen × ΔSSD_Normalperiode`` über {n_txt} Gemeindepunkten, "
             "also mit der Größe, die das Produktionsmodell summiert "
             "(Befund 266/278; Kopfgewichtung ergäbe " + f"{q_kopf:.4f}" + ", "
             f"MM allein {q_mm:.4f}, C44 allein {q_c44:.4f} — geführt wird das "
             f"€-gewichtete Mittel bei einem MM-Anteil von {EUR_ANTEIL_MM:.4f} "
             "— hergeleitet, nicht gesetzt (Befund 290) —, Restdifferenz < 0,2 % "
             "als Näherung gekennzeichnet). "
             f"An der Messzelle allein: {q_station:.4f}. Mit dem SSD-**Trend** "
             f"gewichtet ergäbe sich {q_trend_gew:.4f} ({q_de/q_trend_gew-1:+.1%}); "
             f"die beiden SSD-Felder korrelieren nur mit r = {korr:.2f}, die Wahl "
             "des Gewichts ist also nicht neutral.")
    # Befund 340: Die Fallgewichte bilden die kommunale Altersstruktur ueber
    # share_over_65 ab; innerhalb u65/65+ folgt die Aufteilung einem bundesweit
    # konstanten Schluessel. Das ist eine gekennzeichnete Naeherung, keine
    # Deckungsgleichheit mit den fuenf Baendern des Produktionsmodells.
    p.append(f"- **Gekennzeichnete Näherung (§3.9):** Die Fallgewichte bilden die "
             f"kommunale Altersstruktur über ``share_over_65`` ab; die Aufteilung "
             f"innerhalb u65 und 65+ folgt einem bundesweit konstanten Schlüssel "
             f"(``NATIONAL_SENIOR_SPLIT``), nicht den fünf Bändern des "
             f"Produktionsmodells. Wirkung gegen reine Kopfgewichtung: "
             f"{q_de/q_kopf-1:+.1%}.\n")
    # Befund 339: Ergebnis-Sensitivitaet der Ausschluss-Schwelle.
    p.append("### Punktmengen-Kette\n")
    p.append("Alle drei Stufen gemessen, nicht fortgeschrieben (Befund 338):\n")
    _n_vg = len(punkte)
    _n_gilt = int(gilt.sum())
    _n_stab = int(stabil.sum())
    def _tsd(n: int) -> str:
        return f"{n:,}".replace(",", ".")
    p.append(f"- **{_tsd(_n_vg)}** Gemeindepunkte mit Einwohnerzahl "
             "(BKG VG250 ``vg250_pk`` × Zensus-Aggregat)")
    p.append(f"- **{_tsd(_n_gilt)}** davon mit auswertbaren Trendreihen in beiden "
             "Rastern (endlicher SSD- und Globalstrahlungstrend, ΔSSD > 0)")
    p.append(f"- **{_tsd(_n_stab)}** nach dem Stabilitätsausschluss (SSD-Trend "
             "≥ 1 %/Dekade) — die Menge, über die q und die Perzentile der "
             "Modellgrenze 9 laufen\n")
    p.append("### Ausschluss-Schwelle für instabile Punktquotienten\n")
    p.append("Punkte mit verschwindendem SSD-Trend erzeugen numerisch instabile "
             "Quotienten (der Nenner geht gegen null), nicht kleine. Die Schwelle "
             "ist eine **gekennzeichnete Abschätzung** (§3.9); geführt wird "
             "1 %/Dekade. Alle Werte €-gewichtet wie q selbst:\n")
    p.append("| Schwelle SSD-Trend | Punkte | q | Abweichung zur geführten Wahl |")
    p.append("|---|---|---|---|")
    _q_ref, _ = _q_bei(1.0)
    for _sw in SCHWELLEN:
        _q, _n = _q_bei(_sw)
        _mark = " **(geführt)**" if _sw == 1.0 else ""
        p.append(f"| ≥ {_sw:.2f} %/Dek.{_mark} | {_tsd(_n)} | {_q:.4f} | "
                 f"{_q/_q_ref-1:+.2%} |")
    p.append("")
    p.append(f"- **k_UV = {stationsquotient:.4f} × {q_de:.4f} = {k_uv:.4f}**\n")
    p.append("Der fallgewichtete Bundeswert ist der richtige Bezug für die "
             "Bundessumme — dieselbe Logik, die Befund 223 für ΔSSD festgestellt hat.\n")
    p.append("## 3 Band aus den publizierten Standardfehlern\n")
    p.append(f"SE(Dosis) = {DOSIS_SE:.1f} auf {DOSIS:.1f} = {DOSIS_SE/DOSIS:.1%}; "
             f"SE(Global) = {GLOBAL_SE:.1f} auf {GLOBAL:.1f} = {GLOBAL_SE/GLOBAL:.1%}. "
             f"Unkorreliert fortgepflanzt: **±{rel:.1%}** (1 σ) ⇒ Band "
             f"**{band[0]:.4f}–{band[1]:.4f}**.\n")
    p.append("Das ist die **konservative** Fassung: Beide Reihen sind "
             "bewölkungsgetrieben und damit positiv korreliert, die reale Unsicherheit "
             "des Quotienten ist kleiner. Bis Rev. 6 kam das Band aus Min/Max über acht "
             "handverlesene Städte — eine *räumliche* Streuung, fälschlich als Band der "
             "*Bundes*summe gebucht (Befunde 255/256).\n")
    p.append("## 4 Räumliche Streuung = Modellgrenze, nicht Bundesband\n")
    p.append(f"Verteilung über {int(stabil.sum()):,} Gemeindepunkte mit einem "
             "SSD-Trend ≥ 1 %/Dekade (darunter wird der Quotient numerisch "
             f"instabil; {int(gilt.sum() - stabil.sum()):,} Punkte ausgenommen):\n"
             .replace(",", "."))
    for label, wert in (("5. Perzentil", np.percentile(q_zelle, 5)),
                        ("10. Perzentil", np.percentile(q_zelle, 10)),
                        ("Median", np.median(q_zelle)),
                        ("90. Perzentil", np.percentile(q_zelle, 90)),
                        ("95. Perzentil", np.percentile(q_zelle, 95)),
                        ("bevölkerungsgewichtet (Bundeswert)", q_de)):
        p.append(f"- {label}: **{wert:.4f}**")
    p.append("")
    p.append("Über die Gemeindepunkte streut der Rasterquotient erheblich. Das "
             "verschiebt **einzelne Kommunen** gegeneinander, nicht die Bundessumme — "
             "es gehört deshalb in die Modellgrenzen (wie die Binnenheterogenität des "
             "Bandes 20–64), nicht in das Sanity-Band.\n")
    p.append("## 5 Verworfene Ketten\n")
    p.append(f"- NRW-Gebietsmittel {NRW_GEBIETSMITTEL:.2f} %/Dek. ⇒ "
             f"{DOSIS/NRW_GEBIETSMITTEL:.4f} (bis Rev. 3): Punkt-Zähler gegen "
             "Landesflächenmittel (Befund 230).")
    p.append(f"- Raster-SSD an der Messzelle ⇒ {DOSIS/t_stat['ssd']:.4f} "
             "(Rechnung mit der Messzelle Bochum; **nicht** der "
             "Rev.-4-Stand (Rev. 4: 0,7562)): Zähler weiter Station — "
             "halber Mismatch (Befund 238).")
    p.append("- Stationsquotient 0,867 aus 》roughly twice《 ⇒ 0,5782 (Rev. 5) bzw. "
             "1,0 aus 》similarly《 ⇒ 0,6667 (Rev. 6): beides Ersatzkonstruktionen für "
             "eine Größe, die der Volltext beziffert (Befund 252).\n")
    p.append("## 6 Ozon im Messfenster (Befunde 246/258)\n")
    p.append(f"Tab. 4 weist für Bochum einen **signifikanten** sommerlichen "
             f"Gesamtozon-Trend von **{TCO_SOMMER:+.1f} %/Dekade** (Apr–Sept, "
             "CI −1,75…−0,03) aus. Das Messfenster liegt also **nicht** in einer "
             "Ozon-Erholung; die Ozonentwicklung wirkte dosiserhöhend. Richtung der "
             "Zeitinvarianz-Annahme damit: ΔDosis eher **überschätzt**.\n")

    out = "\n".join(p)
    with open(os.path.join(DATA, "k_uv_herleitung.md"), "w", encoding="utf-8") as fh:
        fh.write(out)
    print(out)


if __name__ == "__main__":
    main()
