"""Rev.-7-Kalibrierlauf für #95 — Auflösung der Befund-1-Hauptkomponente OHNE Zell-Lauf.

Kontext (reviews/BEFUNDE_95.md, §6-Eskalation): Der Kalibrier-Prüfstein (≥ 11/16 Länder
im Band 0,75–1,35) war mit dem Rev.-6-Näherungslauf (Landes-FLÄCHENmittel) nicht erfüllt;
der dokumentierte Modellentscheid lautete „Zell-Lauf + regionale ERF-Nachschätzung".
Dieser Lauf setzt die im Bericht §4 benannte, keyless mögliche Messung um:

  **Bevölkerungsgewichtete Sommermitteltemperatur je Bundesland und Jahr** aus
  DWD-CDC-JJA-Rastern (1 km) am Gemeinde-Repräsentanzpunkt × Zensus-Gemeindebevölkerung.

Damit wird die dominante Bias-Komponente (Bevölkerung wohnt wärmer als das Flächenmittel,
Rev. 6: ×1,11–1,26, pauschal ×0,82 korrigiert) DIREKT im Kalibriermodell aufgelöst statt
pauschal geschätzt — inklusive ihrer regionalen Heterogenität (Stadtstaaten vs.
Flächenländer, Alpenvorland). Verbleibender dokumentierter Rest: UHI-Feinstruktur
unterhalb der Gemeinde (Konvexität ≈ ×1,03, zweiter Ordnung) — wird als Kennzahl mit
ausgegeben.

Teil 2 (nur falls Prüfstein weiter < 11/16): regionale ERF-Nachschätzung — ein
multiplikativer Skalar s_R auf β_85+ je ERF-Region (N/M/S), gefittet OHNE die
Validierungsjahre (Holdout: Verteilungsprüfung auf Σ 2018/2019/2022 out-of-sample).

Datenquellen (offen, keyless):
  - DWD CDC grids_germany/seasonal/air_temperature_mean/14_JJA/ (1-km-ASCII, GK3/31467,
    Zehntel-°C) — Cache: $KAP2_DWD_CACHE oder <tempdir>/kap2_dwd_jja
  - VG250 GeoPackage (lokal, backend/data/vg250/…) — Gemeinde-Repräsentanzpunkte
  - backend/data/lite/zensus_gemeinde.json — Zensus-2022-Bevölkerung je AGS

Ausgabe (backend/data/kalibrierung/):
  sommermittel_bundesland_povw.csv   jahr, bundesland, t_sommer_povw  (Anlage Rev. 7)
  temperatur_offsets_bundesland.csv  bundesland, offset_povw_minus_flaeche_K (Mittel 1992–2024)
  c_kal_rev7_ergebnis.md             alle Kennzahlen (Fits, Holdout, Prüfstein, Anker)
  c_kal_rev7_verteilung.csv          Länder-Verhältnisse der Verteilungsprüfung

Aufruf: backend/.venv nicht nötig — Repo-venv:  .venv/bin/python backend/scripts/kalibrierung/calibrate_heat_mortality_rev7.py
"""
from __future__ import annotations

import csv
import gzip
import math
import os
import sys
import tempfile
import urllib.request
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, ROOT)
sys.path.insert(0, HERE)
DATA = os.path.join(ROOT, "data", "kalibrierung")

from calibrate_heat_mortality import RKI4_BY_BUNDESLAND, RKI_2025, _read, _rki  # noqa: E402
from calibrate_heat_mortality_rev6 import (  # noqa: E402
    BASELINE_MORTALITY_PER_100K, RKI_AGE_SHARES, derive_fa, ls_origin, model_year,
)
from app.services.engine.impact.health import (  # noqa: E402
    AGE_BANDS, REGION_BY_BUNDESLAND, REGION_BETA_85P, REGION_THRESHOLD,
)

YEARS = range(1992, 2026)  # inkl. 2025 (nur für die Sensitivität "inkl. vorläufig 2025"; Befund 77)
GRID_URL = ("https://opendata.dwd.de/climate_environment/CDC/grids_germany/seasonal/"
            "air_temperature_mean/14_JJA/grids_germany_seasonal_air_temp_mean_{y}14.asc.gz")
CACHE = os.environ.get("KAP2_DWD_CACHE") or os.path.join(tempfile.gettempdir(), "kap2_dwd_jja")

BUNDESLAND_BY_PREFIX = {
    "01": "Schleswig-Holstein", "02": "Hamburg", "03": "Niedersachsen", "04": "Bremen",
    "05": "Nordrhein-Westfalen", "06": "Hessen", "07": "Rheinland-Pfalz",
    "08": "Baden-Württemberg", "09": "Bayern", "10": "Saarland", "11": "Berlin",
    "12": "Brandenburg", "13": "Mecklenburg-Vorpommern", "14": "Sachsen",
    "15": "Sachsen-Anhalt", "16": "Thüringen",
}


# ── Teil A: Gemeindepunkte (GK3) + Bevölkerung ───────────────────────────────

def load_gemeinden() -> list[tuple[str, str, float, float, float]]:
    """[(ags, bundesland, x_gk3, y_gk3, pop)] für alle Landgemeinden mit Zensus-Pop."""
    import json

    import pyogrio.raw as raw
    from pyproj import Transformer
    from shapely import wkb as shp_wkb

    gpkg = os.path.join(ROOT, "data", "vg250",
                        "vg250_01-01.utm32s.gpkg.ebenen", "vg250_ebenen_0101",
                        "DE_VG250.gpkg")
    demo = json.load(open(os.path.join(ROOT, "data", "lite", "zensus_gemeinde.json")))
    tr = Transformer.from_crs(25832, 31467, always_xy=True)

    meta, _, geoms, fields = raw.read(gpkg, layer="vg250_gem",
                                      columns=["AGS", "GF", "SN_L"])
    names = list(meta["fields"])
    col = {n: fields[i] for i, n in enumerate(names)}
    out: list[tuple[str, str, float, float, float]] = []
    missing_pop = 0
    for i in range(len(geoms)):
        try:
            if int(col["GF"][i]) != 4:
                continue
        except (TypeError, ValueError):
            continue
        ags = str(col["AGS"][i] or "").strip()
        if len(ags) != 8:
            continue
        bl = BUNDESLAND_BY_PREFIX.get(ags[:2])
        if not bl:
            continue
        d = demo.get(ags)
        pop = float(d["population"]) if d and d.get("population") else 0.0
        if pop <= 0:
            missing_pop += 1
            continue
        g = shp_wkb.loads(bytes(geoms[i]))
        p = g.representative_point()
        x, y = tr.transform(p.x, p.y)
        out.append((ags, bl, x, y, pop))
    print(f"Gemeinden mit Bevölkerung: {len(out)} (ohne Zensus-Pop übersprungen: {missing_pop})",
          file=sys.stderr)
    return out


# ── Teil B: JJA-Raster → bevölkerungsgewichtete Landesreihen ─────────────────

def _grid(year: int):
    import time
    os.makedirs(CACHE, exist_ok=True)
    f = os.path.join(CACHE, f"jja_{year}.asc.gz")
    if not os.path.exists(f) or os.path.getsize(f) == 0:
        for attempt in range(4):
            try:
                urllib.request.urlretrieve(GRID_URL.format(y=year), f)
                break
            except Exception:
                if os.path.exists(f):
                    os.remove(f)
                if attempt == 3:
                    raise
                time.sleep(3 * (attempt + 1))
    with gzip.open(f, "rt") as fh:
        hdr = {}
        while True:
            pos = fh.tell()
            line = fh.readline()
            parts = line.split()
            if parts and parts[0].lower() in ("ncols", "nrows", "xllcorner", "yllcorner",
                                              "cellsize", "nodata_value"):
                hdr[parts[0].lower()] = float(parts[1])
            else:
                fh.seek(pos)
                break
        rows = [line.split() for line in fh if line.strip()]
    return hdr, rows


def build_povw_series(gemeinden) -> tuple[dict, dict]:
    """t_povw[(J, BL)] und Offsets vs. Flächenmittel-CSV (Rev.-6-Basis)."""
    t_flaeche = {(int(r["jahr"]), r["bundesland"]): float(r["t_sommer"])
                 for r in _read("sommermittel_bundesland.csv")}
    t_povw: dict[tuple[int, str], float] = {}
    offs_acc: dict[str, list[float]] = defaultdict(list)

    for year in YEARS:
        hdr, rows = _grid(year)
        ncols, nrows = int(hdr["ncols"]), int(hdr["nrows"])
        x0, y0, cs = hdr["xllcorner"], hdr["yllcorner"], hdr["cellsize"]
        nodata = hdr.get("nodata_value", -999.0)
        num: dict[str, float] = defaultdict(float)
        den: dict[str, float] = defaultdict(float)
        miss = 0
        for _, bl, x, y, pop in gemeinden:
            cx = int((x - x0) // cs)
            cy = int((y - y0) // cs)
            ri = nrows - 1 - cy
            v = None
            if 0 <= ri < nrows and 0 <= cx < ncols:
                raw_v = float(rows[ri][cx])
                if raw_v != nodata:
                    v = raw_v / 10.0  # Zehntel-°C
            if v is None:
                # Nachbarschafts-Fallback (Küsten-/Randzellen)
                for dxy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                    rj, cj = ri + dxy[0], cx + dxy[1]
                    if 0 <= rj < nrows and 0 <= cj < ncols:
                        raw_v = float(rows[rj][cj])
                        if raw_v != nodata:
                            v = raw_v / 10.0
                            break
            if v is None:
                miss += 1
                continue
            num[bl] += pop * v
            den[bl] += pop
        for bl in num:
            t = num[bl] / den[bl]
            t_povw[(year, bl)] = round(t, 3)
            if year <= 2024 and (year, bl) in t_flaeche:
                # Offset-Kennzahl bleibt Ø 1992–2024 (2025 nur für die inkl.-2025-Sensitivität)
                offs_acc[bl].append(t - t_flaeche[(year, bl)])
        if miss:
            print(f"  {year}: {miss} Gemeindepunkte ohne Rasterwert", file=sys.stderr)
        print(f"  {year} ok", file=sys.stderr)

    offsets = {bl: sum(v) / len(v) for bl, v in offs_acc.items()}
    return t_povw, offsets


# ── Teil C: komplette Rev.-6-Auswertung auf der neuen Temperaturbasis ────────

def run_evaluation(t_sommer: dict, fa: dict, tag_suffix: str,
                   beta_scale: dict[str, float] | None = None) -> dict:
    """Fits, Holdout, Verteilungsprüfung, Altersverteilung, Berlin-Anker."""
    de, bl_rki = _rki()
    de_no2025 = {J: v for J, v in de.items() if J != RKI_2025[0]}
    q_w: dict[str, list[float]] = defaultdict(list)
    for r in sorted(_read("wochenquantile_region.csv"), key=lambda r: (r["region"], int(r["w"]))):
        q_w[r["region"]].append(float(r["q_w_emp"]))
    pop = {r["bundesland"]: {b: float(r[b]) for b in AGE_BANDS}
           for r in _read("bevoelkerung_bundesland_altersband.csv")}

    scale = beta_scale or {}

    def my_model_year(J):
        if scale:
            # β-Skalierung je ERF-Region: eigene Variante von model_year
            out = {}
            for bl_name, bands in pop.items():
                reg = REGION_BY_BUNDESLAND[bl_name]
                t0, beta85 = REGION_THRESHOLD[reg], REGION_BETA_85P[reg] * scale.get(reg, 1.0)
                t_bar = t_sommer[(J, bl_name)]
                by_band = {}
                for band in AGE_BANDS:
                    beta = beta85 * fa[band]
                    excess = sum(math.exp(beta * max(0.0, t_bar + q - t0)) - 1.0
                                 for q in q_w[reg])
                    by_band[band] = (bands[band] * BASELINE_MORTALITY_PER_100K[band]
                                     / 1e5 * excess / 52.0)
                out[bl_name] = by_band
            return out
        return model_year(J, t_sommer, q_w, pop, fa)

    cache: dict[int, dict] = {}

    def my(J):
        if J not in cache:
            cache[J] = my_model_year(J)
        return cache[J]

    def nat(J):
        return sum(sum(b.values()) for b in my(J).values())

    def years_sig(src, y0, y1):
        return sorted(J for J, (ew, lo, hi) in src.items()
                      if lo > 0 and y0 <= J <= y1 and all((J, b) in t_sommer for b in pop))

    res: dict = {"tag": tag_suffix, "lines": []}
    lines = res["lines"]

    runs = {}
    for tag, src, y0, y1 in [("fenster_2012_2024", de_no2025, 2012, 2024),
                             ("vollreihe_1992_2024", de_no2025, 1992, 2024),
                             ("vollreihe_inkl2025", de, 1992, 2025)]:
        ys = years_sig(src, y0, y1)
        c = ls_origin([(src[J][0], nat(J)) for J in ys])
        mean_rki = sum(src[J][0] for J in ys) / len(ys)
        r2 = 1 - (sum((src[J][0] - c * nat(J)) ** 2 for J in ys)
                  / sum((src[J][0] - mean_rki) ** 2 for J in ys))
        n_in = sum(1 for J in ys if src[J][1] <= c * nat(J) <= src[J][2])
        runs[tag] = (c, r2, ys, n_in)
        lines.append(f"- **{tag}**: c_kal = {c:.3f} · R² = {r2:.3f} · {n_in}/{len(ys)} Jahre im RKI-PI")
    res["runs"] = runs
    c_base = runs["fenster_2012_2024"][0]

    # Holdout
    ys_fit = years_sig(de_no2025, 1992, 2015)
    c_hold = ls_origin([(de_no2025[J][0], nat(J)) for J in ys_fit])
    ys_test = years_sig(de_no2025, 2016, 2024)
    n_in_t = sum(1 for J in ys_test
                 if de_no2025[J][1] <= c_hold * nat(J) <= de_no2025[J][2])
    devs = [100 * (c_hold * nat(J) - de_no2025[J][0]) / de_no2025[J][0] for J in ys_test]
    lines.append(f"- Holdout: Fit 1992–2015 → c = {c_hold:.3f}; Prüfung 2016–2024: "
                 f"{n_in_t}/{len(ys_test)} im PI (Abw. {min(devs):+.0f}…{max(devs):+.0f} %)")
    res["holdout"] = (c_hold, n_in_t, len(ys_test))

    # Regionale Diagnose-Faktoren (Fenster)
    c_reg = {}
    for reg in sorted(set(RKI4_BY_BUNDESLAND.values())):
        pairs = []
        for (J, b), (ew, lo, hi) in bl_rki.items():
            if (RKI4_BY_BUNDESLAND.get(b) == reg and lo > 0 and 2012 <= J <= 2024
                    and (J, b) in t_sommer):
                pairs.append((ew, sum(my(J)[b].values())))
        c_reg[reg] = ls_origin(pairs)
    lines.append("- c_reg-Diagnose (Fenster): "
                 + ", ".join(f"{k} = {v:.3f}" for k, v in c_reg.items()))
    res["c_reg"] = c_reg

    # Verteilungsprüfung / PRÜFSTEIN: Σ Hitzejahre, je Land
    VAL = (2018, 2019, 2022)
    rows_nat, rows_reg = [], []
    n_nat = n_reg = 0
    for b in sorted(pop):
        m_nat = sum(c_base * sum(my(J)[b].values()) for J in VAL)
        m_reg = sum(c_reg[RKI4_BY_BUNDESLAND[b]] * sum(my(J)[b].values()) for J in VAL)
        r = sum(bl_rki[(J, b)][0] for J in VAL if (J, b) in bl_rki)
        v_nat = m_nat / r if r else float("nan")
        v_reg = m_reg / r if r else float("nan")
        rows_nat.append((b, RKI4_BY_BUNDESLAND[b], round(v_nat, 2)))
        rows_reg.append((b, RKI4_BY_BUNDESLAND[b], round(v_reg, 2)))
        if 0.75 <= v_nat <= 1.35:
            n_nat += 1
        if 0.75 <= v_reg <= 1.35:
            n_reg += 1
    lines.append(f"- **Prüfstein (nationaler Skalar c = {c_base:.3f}): {n_nat}/16 Länder "
                 f"im Band 0,75–1,35** · mit c_reg-Diagnosefaktoren: {n_reg}/16")
    res["pruefstein"] = (n_nat, n_reg, rows_nat, rows_reg)

    # Altersverteilung
    ys = runs["fenster_2012_2024"][2]
    tot = {b: sum(my(J)[bl][b] for J in ys for bl in pop) for b in AGE_BANDS}
    s = sum(tot.values())
    ages = {b: 100 * tot[b] / s for b in AGE_BANDS}
    lines.append("- Altersverteilungs-Ist: "
                 + " / ".join(f"{ages[b]:.1f}" for b in AGE_BANDS)
                 + " % (RKI 6,5/12,9/25,2/55,5; Toleranz ±5 pp)")
    res["ages"] = ages

    # Berlin-Anker 2018, 85+
    d_b85 = c_base * my(2018)["Berlin"]["a85p"]
    rate = 1e5 * d_b85 / pop["Berlin"]["a85p"]
    lines.append(f"- Berlin 2018, 85+ (nationaler Skalar): {rate:.0f} je 100.000 "
                 f"(RKI-Referenz 260–320)")
    res["berlin"] = rate

    # Rest-Bias: UHI-Feinstruktur-Konvexität (mittelwerttreu, σ = 0,5 K).
    # Nur im unskalierten Lauf aussagekräftig (model_year kennt keine β-Skalare).
    if not scale:
        for J in (2018, 2022):
            base = nat(J)
            su = sum(sum(b.values()) for b in
                     model_year(J, t_sommer, q_w, pop, fa, uhi_sigma=0.5).values())
            lines.append(f"- Rest-Bias UHI-Konvexität {J}: ×{su / base:.3f} (σ = 0,5 K, "
                         f"mittelwerttreu — verbleibende dokumentierte Näherung)")
    return res


def main() -> None:
    fa = derive_fa()
    gemeinden = load_gemeinden()
    t_povw, offsets = build_povw_series(gemeinden)

    with open(os.path.join(DATA, "sommermittel_bundesland_povw.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["jahr", "bundesland", "t_sommer_povw"])
        for (J, bl), t in sorted(t_povw.items()):
            w.writerow([J, bl, t])
    with open(os.path.join(DATA, "temperatur_offsets_bundesland.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["bundesland", "offset_povw_minus_flaeche_K"])
        for bl, o in sorted(offsets.items()):
            w.writerow([bl, round(o, 3)])

    import hashlib
    def _pin(path):
        h = hashlib.sha256(open(path, "rb").read()).hexdigest()[:12]
        return f"{os.path.basename(path)} sha256:{h}"
    pins = [_pin(os.path.join(ROOT, "data", "lite", "zensus_gemeinde.json")),
            _pin(os.path.join(ROOT, "data", "vg250", "vg250_01-01.utm32s.gpkg.ebenen",
                              "vg250_ebenen_0101", "DE_VG250.gpkg"))]
    lines = ["# Rev.-7-Kalibrierlauf #95 — bevölkerungsgewichtete Temperaturen", "",
             f"Gemeinden mit Zensus-Bevölkerung: **{len(gemeinden)}** · Daten-Pins: "
             + " · ".join(pins), "",
             "## Temperatur-Offsets (bevölkerungsgewichtet − Flächenmittel, Ø 1992–2024):"]
    de_off = (sum(offsets[bl] * sum(1 for g in gemeinden if g[1] == bl) for bl in offsets)
              / len(gemeinden))
    pop_tot = defaultdict(float)
    for _, bl, _, _, p in gemeinden:
        pop_tot[bl] += p
    de_off_pw = sum(offsets[bl] * pop_tot[bl] for bl in offsets) / sum(pop_tot.values())
    for bl in sorted(offsets):
        lines.append(f"- {bl}: {offsets[bl]:+.2f} K")
    lines.append(f"- **Deutschland (bevölkerungsgewichtet): {de_off_pw:+.2f} K** "
                 f"(Rev.-6-Abschätzung war +0,2…+0,4 K)")
    lines.append("")

    lines.append("## Lauf A — Basis Rev. 7 (bevölkerungsgewichtete Reihen, ERF unverändert):")
    res_a = run_evaluation(t_povw, fa, "povw")
    lines += res_a["lines"]

    result_final = res_a
    scale_final: dict[str, float] = {}
    if res_a["pruefstein"][0] < 11:
        lines += ["", "## Lauf B — regionale ERF-Nachschätzung (β-Skalar je N/M/S; "
                      "Fit OHNE Validierungsjahre 2018/2019/2022 — Holdout):"]
        de, bl_rki = _rki()
        # Alternierende Gittersuche: s_R je ERF-Region, c national per LS,
        # Zielfunktion = Summe der quadrierten Log-Verhältnisse der Land-Jahre
        # (Fenster 2012–2024 OHNE 2018/2019/2022).
        q_w: dict[str, list[float]] = defaultdict(list)
        for r in sorted(_read("wochenquantile_region.csv"),
                        key=lambda r: (r["region"], int(r["w"]))):
            q_w[r["region"]].append(float(r["q_w_emp"]))
        pop = {r["bundesland"]: {b: float(r[b]) for b in AGE_BANDS}
               for r in _read("bevoelkerung_bundesland_altersband.csv")}
        HOLD = {2018, 2019, 2022}
        fit_obs = [((J, b), ew) for (J, b), (ew, lo, hi) in bl_rki.items()
                   if lo > 0 and 2012 <= J <= 2024 and J not in HOLD
                   and (J, b) in t_povw]
        n_by_reg = defaultdict(int)
        for (J, b), _ew in fit_obs:
            n_by_reg[REGION_BY_BUNDESLAND[b]] += 1
        lines.append(f"- Fit-Set (signifikante Land-Jahre 2012–2024 ohne 2018/19/22): "
                     + ", ".join(f"{r} = {n_by_reg[r]}" for r in ("nord", "mitte", "sued")))

        def model_bl(J, b, s):
            reg = REGION_BY_BUNDESLAND[b]
            t0 = REGION_THRESHOLD[reg]
            beta85 = REGION_BETA_85P[reg] * s.get(reg, 1.0)
            t_bar = t_povw[(J, b)]
            tot = 0.0
            for band in AGE_BANDS:
                beta = beta85 * fa[band]
                excess = sum(math.exp(beta * max(0.0, t_bar + q - t0)) - 1.0
                             for q in q_w[reg])
                tot += pop[b][band] * BASELINE_MORTALITY_PER_100K[band] / 1e5 * excess / 52.0
            return tot

        def objective(s):
            pairs = [(ew, model_bl(J, b, s)) for (J, b), ew in fit_obs]
            c = ls_origin(pairs)
            err = sum((math.log(max(c * m, 1e-9)) - math.log(ew)) ** 2
                      for ew, m in pairs if ew > 0)
            return err, c

        # Identifikations-Diagnose (Vorlauf mit allen drei Skalaren frei zeigte:
        # s_Nord nicht identifizierbar — Zielfunktion flach über 0,4–1,0, weil die
        # kleinen Nord-Länder kaum signifikante Fit-Jahre außerhalb der Hitzejahre
        # liefern; s_Mitte-Optimum = 1,0. Nachgeschätzt wird daher NUR die in der
        # Verteilungsprüfung diagnostizierte Süd-Schieflage — minimal-invasiv,
        # §3.4-konform: Wirkungsfunktion dort nachschätzen, wo die Prüfung
        # Schieflage zeigt UND die Daten den Parameter identifizieren.
        s_cur = {"nord": 1.0, "mitte": 1.0, "sued": 1.0}
        best = None
        for k in [round(0.40 + 0.05 * i, 2) for i in range(37)]:  # 0,40–2,20
            err, _c = objective(dict(s_cur, sued=k))
            if best is None or err < best[0]:
                best = (err, k)
        s_cur["sued"] = best[1]
        err, c_fit = objective(s_cur)
        # Stabilität: Zielfunktionsprofile (Nord/Mitte zur Dokumentation der
        # Identifikationslage, Süd um das Optimum)
        for reg in ("nord", "mitte", "sued"):
            prof = []
            for k in [round(max(0.4, s_cur[reg] - 0.3) + 0.1 * i, 2) for i in range(7)]:
                e, _ = objective(dict(s_cur, **{reg: k}))
                prof.append(f"{k}:{e:.2f}")
            lines.append(f"- Zielfunktionsprofil s_{reg}: " + " · ".join(prof))
        lines.append("- Identifikation: s_Nord flach (nicht identifizierbar, bleibt 1,0); "
                     "s_Mitte-Optimum = 1,0 (bleibt 1,0); nachgeschätzt nur s_Süd "
                     "(diagnostizierte Schieflage, klar identifiziert)")
        lines.append(f"- Nachschätzung (Fit ohne Hitzejahre): s_Nord = {s_cur['nord']:.2f} · "
                     f"s_Mitte = {s_cur['mitte']:.2f} · s_Süd = {s_cur['sued']:.2f} "
                     f"⇒ β_85+ = {REGION_BETA_85P['nord']*s_cur['nord']:.4f} / "
                     f"{REGION_BETA_85P['mitte']*s_cur['mitte']:.4f} / "
                     f"{REGION_BETA_85P['sued']*s_cur['sued']:.4f} K⁻¹")
        # Befund 78: strenge Voll-Holdout-Variante — auch der Niveau-Skalar ohne
        # die Prüfjahre 2018/2019/2022 gefittet; Prüfstein damit erneut messen.
        de_full, bl_rki_full = _rki()
        fen_wo = [J for J in range(2012, 2025)
                  if J not in HOLD and J in de_full and de_full[J][1] > 0
                  and all((J, b) in t_povw for b in pop)]
        c_wo = ls_origin([(de_full[J][0],
                           sum(model_bl(J, b, s_cur) for b in pop)) for J in fen_wo])
        n_wo = 0
        for b in sorted(pop):
            m = sum(c_wo * model_bl(J, b, s_cur) for J in (2018, 2019, 2022))
            r = sum(bl_rki_full[(J, b)][0] for J in (2018, 2019, 2022)
                    if (J, b) in bl_rki_full)
            if r and 0.75 <= m / r <= 1.35:
                n_wo += 1
        lines.append(f"- Voll-Holdout-Sensitivität (Befund 78): Niveau-Skalar ohne "
                     f"2018/19/22 gefittet → c = {c_wo:.3f}; Prüfstein damit "
                     f"**{n_wo}/16** (vollständig out-of-sample)")
        # Befund 80: c_kal-Bandgrenzen aus dem s_Süd-Profil-Band herleiten
        for k in (1.45, 1.85):
            _e, c_k = objective(dict(s_cur, sued=k))
            # c auf dem vollen Fenster mit s_Süd = k
            ys_k = [J for J in range(2012, 2025) if J in de_full and de_full[J][1] > 0
                    and all((J, b) in t_povw for b in pop)]
            c_full_k = ls_origin([(de_full[J][0],
                                   sum(model_bl(J, b, dict(s_cur, sued=k)) for b in pop))
                                  for J in ys_k])
            lines.append(f"- c_kal-Band-Stütze (Befund 80): s_Süd = {k} → c = {c_full_k:.3f}")
        res_b = run_evaluation(t_povw, fa, "povw+erf", beta_scale=s_cur)
        lines += res_b["lines"]
        if res_b["pruefstein"][0] > res_a["pruefstein"][0]:
            result_final = res_b
            scale_final = s_cur

    n_nat = result_final["pruefstein"][0]
    lines += ["", f"## Ergebnis: Prüfstein (nationaler Skalar) = **{n_nat}/16** "
                  f"(Anforderung ≥ 11/16) — {'BESTANDEN' if n_nat >= 11 else 'NICHT bestanden'}"
                  + (f"; ERF-Skalare {scale_final}" if scale_final else " (ohne ERF-Nachschätzung)")]

    with open(os.path.join(DATA, "c_kal_rev7_ergebnis.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(os.path.join(DATA, "c_kal_rev7_verteilung.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["bundesland", "region4", "verhaeltnis_national", "verhaeltnis_creg"])
        for (b, reg, v_nat), (_, _, v_reg) in zip(result_final["pruefstein"][2],
                                                  result_final["pruefstein"][3]):
            w.writerow([b, reg, v_nat, v_reg])
    print("\n".join(lines))


if __name__ == "__main__":
    main()
