"""Rev.-6-Kalibrierläufe für #95 (Befunde 1, 19, 20, 21, 24, 32, 47 des Ledgers
reviews/BEFUNDE_95.md). Companion zu calibrate_heat_mortality.py — das Rev.-5-Skript
bleibt unverändert (Reproduzierbarkeit der Rev.-5-Zahlen); dieses Skript rechnet:

  1. f_a-Rückrechnung aus RKI-Altersverteilung 2026 + m_a 2023 (lineare Näherung,
     gekennzeichnet; Befund 32) — Formel: f_a ∝ Anteil_a / (pop_a·m_a), normiert auf 85+.
  2. c_kal national, neue f_a: Basis = Fenster 2012–2024 (ohne vorläufiges 2025; Befunde
     21/24), Vollreihe 1992–2024 als Sensitivität; zusätzlich Vollreihe inkl. 2025.
  3. Regionale c_reg (RKI-4-Zuschnitt) mit EINHEITLICHEM Signifikanzfilter (Bundesland-
     PI-Untergrenze > 0) und je Fenster (Befund 47).
  4. Zeitlicher Holdout: Fit 1992–2015 → Prüfung 2016–2024 (Befund 19).
  5. Altersverteilungs-Ist: modellierte Bandanteile vs. RKI 6,5/12,9/25,2/55,5 % (Befund 20).
  6. Unabhängiger Anker: Berlin 2018, 85+-Rate je 100.000 (RKI-Referenz 260–320).
  7. Befund-1-Bias-Band: Elastizität der Modellsumme gegen +0,2/+0,4 K (Bevölkerungs-
     gewichtung) und Konvexitätseffekt einer mittelwerttreuen UHI-Streuung (sigma 0,5 K).

Ausgabe: c_kal_rev6_ergebnis.md (+ CSVs) in backend/data/kalibrierung/.
"""
from __future__ import annotations

import csv
import math
import os
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, ROOT)
sys.path.insert(0, HERE)
DATA = os.path.join(ROOT, "data", "kalibrierung")

from calibrate_heat_mortality import RKI4_BY_BUNDESLAND, RKI_2025, _read, _rki  # noqa: E402
from app.services.engine.impact.health import (  # noqa: E402
    AGE_BANDS, REGION_BY_BUNDESLAND, REGION_BETA_85P, REGION_THRESHOLD,
)

BASELINE_MORTALITY_PER_100K = {"u65": 213.2, "a65_74": 1737.9, "a75_84": 4812.3, "a85p": 14800.2}
RKI_AGE_SHARES = {"u65": 0.065, "a65_74": 0.129, "a75_84": 0.252, "a85p": 0.555}   # RKI 2026 [12]
DEATHS_2023 = {"u65": 138_024, "a65_74": 166_312, "a75_84": 302_921, "a85p": 420_949}  # [49]


def derive_fa() -> dict[str, float]:
    """Befund 32: f_a proportional Anteil_a/(pop_a*m_a) = Anteil_a/Sterbefaelle_a, auf 85+=1."""
    raw = {b: RKI_AGE_SHARES[b] / DEATHS_2023[b] for b in AGE_BANDS}
    return {b: round(raw[b] / raw["a85p"], 3) for b in AGE_BANDS}


def model_year(J, t_sommer, q_w, pop, fa, t_shift=0.0, uhi_sigma=0.0):
    out = {}
    # Gauss-Hermite-artige 5-Punkt-Naeherung fuer mittelwerttreue UHI-Streuung
    if uhi_sigma > 0:
        offs = [(-2 * uhi_sigma, 0.0668), (-uhi_sigma, 0.2417), (0.0, 0.383),
                (uhi_sigma, 0.2417), (2 * uhi_sigma, 0.0668)]
    else:
        offs = [(0.0, 1.0)]
    for bl_name, bands in pop.items():
        reg = REGION_BY_BUNDESLAND[bl_name]
        t0, beta85 = REGION_THRESHOLD[reg], REGION_BETA_85P[reg]
        t_bar = t_sommer[(J, bl_name)] + t_shift
        by_band = {}
        for band in AGE_BANDS:
            beta = beta85 * fa[band]
            excess = sum(w * (math.exp(beta * max(0.0, t_bar + o + q - t0)) - 1.0)
                         for q in q_w[reg] for o, w in offs)
            by_band[band] = bands[band] * BASELINE_MORTALITY_PER_100K[band] / 1e5 * excess / 52.0
        out[bl_name] = by_band
    return out


def ls_origin(pairs):
    num = sum(a * b for a, b in pairs)
    den = sum(b * b for _, b in pairs)
    return num / den if den else float("nan")


def main() -> None:
    fa = derive_fa()
    de, bl_rki = _rki()
    de_no2025 = {J: v for J, v in de.items() if J != RKI_2025[0]}
    t_sommer = {(int(r["jahr"]), r["bundesland"]): float(r["t_sommer"]) for r in _read("sommermittel_bundesland.csv")}
    q_w: dict[str, list[float]] = defaultdict(list)
    for r in sorted(_read("wochenquantile_region.csv"), key=lambda r: (r["region"], int(r["w"]))):
        q_w[r["region"]].append(float(r["q_w_emp"]))
    pop = {r["bundesland"]: {b: float(r[b]) for b in AGE_BANDS} for r in _read("bevoelkerung_bundesland_altersband.csv")}

    def years_sig(src, y0, y1):
        return sorted(J for J, (ew, lo, hi) in src.items()
                      if lo > 0 and y0 <= J <= y1 and all((J, b) in t_sommer for b in pop))

    cache: dict[int, dict] = {}

    def my(J):
        if J not in cache:
            cache[J] = model_year(J, t_sommer, q_w, pop, fa)
        return cache[J]

    def nat(J):
        return sum(sum(b.values()) for b in my(J).values())

    lines = [f"# Rev.-6-Kalibrierlauf #95 — Ergebnisse", "",
             f"f_a-Rückrechnung (Befund 32, lineare Näherung): "
             + ", ".join(f"{b} = {fa[b]}" for b in AGE_BANDS)]

    runs = {}
    for tag, src, y0, y1 in [("fenster_2012_2024", de_no2025, 2012, 2024),
                             ("vollreihe_1992_2024", de_no2025, 1992, 2024),
                             ("vollreihe_inkl2025", de, 1992, 2025)]:
        ys = years_sig(src, y0, y1)
        c = ls_origin([(src[J][0], nat(J)) for J in ys])
        mean_rki = sum(src[J][0] for J in ys) / len(ys)
        r2 = 1 - sum((src[J][0] - c * nat(J)) ** 2 for J in ys) / sum((src[J][0] - mean_rki) ** 2 for J in ys)
        n_in = sum(1 for J in ys if src[J][1] <= c * nat(J) <= src[J][2])
        runs[tag] = (c, r2, ys, n_in)
        lines.append(f"- **{tag}**: c_kal = {c:.3f} · R² = {r2:.3f} · {n_in}/{len(ys)} Jahre im RKI-PI")

    # Holdout (Befund 19): Fit 1992-2015 signifikant, Pruefung 2016-2024
    ys_fit = years_sig(de_no2025, 1992, 2015)
    c_fit = ls_origin([(de_no2025[J][0], nat(J)) for J in ys_fit])
    ys_test = years_sig(de_no2025, 2016, 2024)
    devs = [(J, de_no2025[J][0], round(c_fit * nat(J)),
             round(100 * (c_fit * nat(J) - de_no2025[J][0]) / de_no2025[J][0], 1),
             de_no2025[J][1] <= c_fit * nat(J) <= de_no2025[J][2]) for J in ys_test]
    n_in_t = sum(1 for d in devs if d[4])
    lines += ["", f"## Holdout (Befund 19): Fit 1992–2015 → c = {c_fit:.3f}; Prüfung 2016–2024:",
              "| Jahr | RKI | Modell×c | Abw. % | im PI |", "|---|---|---|---|---|"]
    lines += [f"| {j} | {r} | {m} | {a:+.1f} | {'ja' if i else 'nein'} |" for j, r, m, a, i in devs]
    lines.append(f"→ {n_in_t}/{len(devs)} Prüfjahre im RKI-Prädiktionsintervall (out-of-sample).")

    # Regionale Faktoren: einheitlicher Signifikanzfilter (BL-PI-lo > 0), je Fenster (Befund 47)
    lines += ["", "## Regionale c_reg (RKI-4-Zuschnitt), Signifikanzfilter BL-PI-Untergrenze > 0:"]
    creg_base = {}
    for tag, y0, y1 in [("fenster_2012_2024", 2012, 2024), ("vollreihe_1992_2024", 1992, 2024)]:
        c_reg = {}
        for reg in sorted(set(RKI4_BY_BUNDESLAND.values())):
            pairs = []
            for (J, b), (ew, lo, hi) in bl_rki.items():
                if RKI4_BY_BUNDESLAND.get(b) == reg and lo > 0 and y0 <= J <= y1 and (J, b) in t_sommer:
                    pairs.append((ew, sum(my(J)[b].values())))
            c_reg[reg] = ls_origin(pairs)
        lines.append(f"- **{tag}**: " + ", ".join(f"{k} = {v:.3f}" for k, v in c_reg.items()))
        if tag == "fenster_2012_2024":
            creg_base = c_reg

    # Verteilungspruefung mit Basis-Faktoren (Fenster), Hitzejahre
    VAL = (2018, 2019, 2022)   # Hitzejahre im Basisfenster
    lines += ["", f"## Verteilungsprüfung (Σ {VAL}, c_reg Fenster): Verhältnis Modell/RKI je Land:"]
    n_band = 0
    val_rows = []
    for b in sorted(pop):
        m = sum(creg_base[RKI4_BY_BUNDESLAND[b]] * sum(my(J)[b].values()) for J in VAL)
        r = sum(bl_rki[(J, b)][0] for J in VAL if (J, b) in bl_rki)
        v = m / r if r else float("nan")
        val_rows.append((b, RKI4_BY_BUNDESLAND[b], round(v, 2)))
        if 0.75 <= v <= 1.35:
            n_band += 1
    lines += [f"- {b} ({reg}): {v}" for b, reg, v in val_rows]
    lines.append(f"→ **{n_band}/16 Länder im Band 0,75–1,35**")

    # Altersverteilungs-Ist (Befund 20): ueber die Basisfenster-Jahre, national
    ys = runs["fenster_2012_2024"][2]
    tot = {b: sum(my(J)[bl][b] for J in ys for bl in pop) for b in AGE_BANDS}
    s = sum(tot.values())
    lines += ["", "## Altersverteilungs-Ist (Befund 20, Fenster 2012–2024):",
              "| Band | Modell % | RKI % |", "|---|---|---|"]
    for b in AGE_BANDS:
        lines.append(f"| {b} | {100 * tot[b] / s:.1f} | {100 * RKI_AGE_SHARES[b]:.1f} |")

    # Unabhaengiger Anker Berlin 2018, 85+ je 100.000 (Referenz 260-320 [14])
    c_base = runs["fenster_2012_2024"][0]
    d_b85 = creg_base["osten"] * my(2018)["Berlin"]["a85p"]
    rate = 1e5 * d_b85 / pop["Berlin"]["a85p"]
    lines += ["", f"## Unabhängiger Anker: Berlin 2018, Band 85+: Modell (c_reg Osten) = "
              f"{rate:.0f} je 100.000 (RKI-Referenz 260–320 [14]); national c = {c_base:.3f}"]

    # Befund-1-Bias-Band
    lines += ["", "## Befund-1-Bias-Band (Beispieljahre, Verhältnis Modellsumme):"]
    for J in (2018, 2022, 2003):
        base = nat(J)
        s02 = sum(sum(b.values()) for b in model_year(J, t_sommer, q_w, pop, fa, t_shift=0.2).values())
        s04 = sum(sum(b.values()) for b in model_year(J, t_sommer, q_w, pop, fa, t_shift=0.4).values())
        su = sum(sum(b.values()) for b in model_year(J, t_sommer, q_w, pop, fa, uhi_sigma=0.5).values())
        lines.append(f"- {J}: +0,2 K → ×{s02 / base:.3f} · +0,4 K → ×{s04 / base:.3f} · "
                     f"UHI-Streuung σ=0,5 K (mittelwerttreu) → ×{su / base:.3f}")

    with open(os.path.join(DATA, "c_kal_rev6_ergebnis.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(os.path.join(DATA, "c_kal_rev6_verteilung.csv"), "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["bundesland", "region4", "verhaeltnis_modell_rki"])
        w.writerows(val_rows)
    print("\n".join(lines))


if __name__ == "__main__":
    main()
