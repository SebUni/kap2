#!/usr/bin/env python3
"""#98 Anlage [73], Teil »Räumliche Streuung von k_UV« (Befund 449).

Misst, ob die Streuung des Rasterquotienten q = ΔGlobal ÷ ΔSSD über die
Gemeindepunkte räumliches Signal ist oder Schätzrauschen zweier Trends, und wendet
die Entscheidungsregel der Festlegung an (Gesamtschau zu T-1115 vom 27.09.2026,
»Räumliche Streuung von k_UV (Befund 449): Messung und Entscheidungsregel«):

  Vorweg  Bundeswert reproduzieren: |q_Bund − 0,6683| ≤ 0,003, sonst Abbruch ohne
          Anlage (keine Ersatzzahl).
  (a)     q je Kreis (AGS Stellen 1–5) und je Land als gewichtetes Mittel der
          Punktquotienten; Perzentile 5/10/50/90/95 der Kreiswerte (ungewichtet über
          die Kreise, relativ zu q_Bund) und die 16 Landeswerte.
  (b)     Rangtreue: Spearman über die Kreise nach Euro-Betrag je Einwohner,
          proportional zu Σ (Gewicht × q) ÷ Einwohner, einmal mit q_Bund, einmal mit
          q je Kreis.
  (c)     Zeitstabilität: Spearman zwischen q je Kreis aus den Trends 1997–2009 und
          2010–2022; q = Quotient der gewichteten Kreistrends (Globalstrahlung ÷
          Sonnenscheindauer); einbezogen sind Kreise mit positivem SSD-Trend in
          beiden Hälften.
  Regel   Zweig 1 bei Rangtreue ≥ 0,90; Zweig 2 bei Rangtreue < 0,90 und
          Zeitstabilität < 0,50; Zweig 3 sonst. Schwellen: Setzungen von KAP3.

Punktmenge, Stabilitätsausschluss (SSD-Trend ≥ 1 %/Dek.) und Gewicht
(Baseline-Fälle × ΔSSD der Normalperioden, €-gewichtetes Mittel aus MM und C44) sind
dieselben wie beim Bundeswert in ``k_uv_herleitung.py``; dessen Leser ``_rad_grid``,
``_ssd_grid`` und ``_trend`` werden importiert, ``k_uv_herleitung.{py,md,csv}``
bleiben unverändert. Abweichung vom Lauf vom 01.09.2026 (steht auch in der Anlage):
Gemeindepunkte aus ``backend/.cache/60_stichprobe/DE_VG250.gpkg`` (Gebietsstand
2026), Einwohner und 65+-Anteil aus ``zensus2022_demografie_ab65.csv`` nach der Regel
des Produkts (#95 §3.3, Anteil 60–66 mit 2/7) statt ``data/lite/zensus_gemeinde.json``.

Zwischenablage der DWD-Raster nur in ``backend/.cache/`` (Globalstrahlung) und
``backend/data/dwd_cdc/`` (Sonnenscheindauer, Disk-Cache des Produkts), beide in
``.gitignore``.

Ausgaben (backend/data/kalibrierung/):
    k_uv_raumstreuung.md    Anlage: Punktmenge, Reproduktion, Kreis-/Landeswerte,
                            Rangtreue, Zeitstabilität, Schwellen, Zweig
    k_uv_raumstreuung.csv   Kreiswerte (eine Zeile je Kreis)

Aufruf (venv des Produkts): python backend/scripts/kalibrierung/k_uv_raumstreuung.py
"""
from __future__ import annotations

import csv
import os
import sqlite3
import sys

import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import k_uv_herleitung as H  # noqa: E402  (Leser _rad_grid, _ssd_grid, _trend)

DATA = os.path.join(ROOT, "data", "kalibrierung")
GPKG = os.path.join(ROOT, ".cache", "60_stichprobe", "DE_VG250.gpkg")
# Globalstrahlungs-Raster nicht unter ~/.cache, sondern im ignorierten Repo-Cache.
H.RAD_CACHE = os.path.join(ROOT, ".cache", "k_uv_raumstreuung", "rad")

Q_BUND_ANLAGE = 0.6683          # k_uv_herleitung.md, Abschnitt 2 (Rasterquotient)
TOLERANZ = 0.003                # Festlegung: sonst gilt keine der folgenden Zahlen
EUR_ANTEIL_MM_ANLAGE = 0.4316   # k_uv_herleitung.md, Abschnitt 2 (MM-Anteil)
SCHWELLE_RANG = 0.90            # Setzung von KAP3 (Festlegung)
SCHWELLE_ZEIT = 0.50            # Setzung von KAP3 (Festlegung)
HAELFTEN = (list(range(1997, 2010)), list(range(2010, 2023)))
ZENSUS_STICHTAG = "2022-05-15"  # Stichtag des Zensus 2022, Vergleich mit VG250-Feld WSK
MINUS = "−"


# ── Schreibweise nach kap3-stil ─────────────────────────────────────────────
def _z(x: float, n: int = 4) -> str:
    s = f"{x:,.{n}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return s.replace("-", MINUS)


def _vz(x: float, n: int = 0) -> str:
    """Relative Abweichung in Prozent mit Vorzeichen, ohne Einheit, z. B. +12 / −8."""
    s = _z(x * 100, n)
    return s if s.startswith(MINUS) else "+" + s


def _pz(x: float, n: int = 0) -> str:
    """Relative Abweichung mit Vorzeichen, z. B. +12 % / −8 %."""
    return _vz(x, n) + " %"


def _spanne(a: float, b: float, n: int = 0) -> str:
    """Spanne mit Vorzeichen, Einheit einmal am Ende (kap3-stil): −38 … +43 %."""
    return f"{_vz(a, n)} … {_vz(b, n)} %"


def _liste(teile: list[str]) -> str:
    """Aufzählung im Satz: a, b und c."""
    return teile[0] if len(teile) == 1 else ", ".join(teile[:-1]) + " und " + teile[-1]


def _datum(wsk: str) -> str:
    """VG250-Feld WSK (ISO) als Datum im Text: 2026-01-01T… → 01.01.2026."""
    j, m, t = wsk[:10].split("-")
    return f"{t}.{m}.{j}"


def _tsd(n: int) -> str:
    return f"{n:,}".replace(",", ".")


# ── Messbausteine ───────────────────────────────────────────────────────────
def _rang(x: np.ndarray) -> np.ndarray:
    """Ränge 1..n, bei Gleichstand der Mittelrang."""
    x = np.asarray(x, dtype=float)
    r = np.empty(len(x))
    r[np.argsort(x, kind="mergesort")] = np.arange(1, len(x) + 1)
    _, inv = np.unique(x, return_inverse=True)
    return (np.bincount(inv, weights=r) / np.bincount(inv))[inv]


def spearman(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.corrcoef(_rang(a), _rang(b))[0, 1])


def _trend_matrix(jahre: list[int], m: np.ndarray) -> np.ndarray:
    """Relativer Trend in %/Dekade je Spalte (OLS-Steigung ÷ Mittel), wie H._trend."""
    x = np.asarray(jahre, dtype=float)
    xm = x - x.mean()
    steigung = (xm[:, None] * (m - m.mean(axis=0))).sum(axis=0) / (xm ** 2).sum()
    return steigung * 10 / m.mean(axis=0) * 100


def _zweig(rang: float, zeit: float, s_rang: float = SCHWELLE_RANG,
           s_zeit: float = SCHWELLE_ZEIT) -> int:
    if rang >= s_rang:
        return 1
    return 2 if zeit < s_zeit else 3


def main() -> int:
    from pyproj import Transformer

    from app.services import zensus_loader as zl
    from app.services.climate import ssd_normalperioden as snp
    from app.services.engine.impact.health import (UV_INCIDENCE_C44,
                                                   UV_INCIDENCE_MM)

    if not os.path.exists(GPKG):
        print(f"BLOCKIERT: Eingang fehlt: {GPKG}")
        return 2
    if not os.path.exists(zl.DEMOGRAFIE_AB65_CSV):
        print(f"BLOCKIERT: Eingang fehlt: {zl.DEMOGRAFIE_AB65_CSV}")
        return 2

    # ── Punktmenge ──────────────────────────────────────────────────────────
    con = sqlite3.connect(GPKG)
    try:
        roh = con.execute("SELECT AGS, LON_DEZ, LAT_DEZ, BEZ, GEN FROM vg250_pk "
                          "WHERE AGS IS NOT NULL AND LON_DEZ IS NOT NULL").fetchall()
        # Die Länderebene führt den Bodensee als eigene Fläche: Namen ohne Zusatz.
        laender = dict(con.execute("SELECT DISTINCT AGS, GEN FROM vg250_lan "
                                   "WHERE GEN NOT LIKE '%Bodensee%'").fetchall())
        kreise = dict(con.execute("SELECT DISTINCT AGS, GEN FROM vg250_krs").fetchall())
        kreis_bez = dict(con.execute("SELECT DISTINCT AGS, BEZ FROM vg250_krs").fetchall())
        # WSK = Wirksamkeit der letzten Änderung, je Gemeinde und je Kreis.
        wsk_gem = dict(con.execute("SELECT AGS, MAX(WSK) FROM vg250_gem GROUP BY AGS").fetchall())
        wsk_krs = dict(con.execute("SELECT AGS, MAX(WSK) FROM vg250_krs GROUP BY AGS").fetchall())
    finally:
        con.close()
    n_vg = len(roh)
    teil = zl.ANTEIL_60_66_DEFAULT                      # 2/7, Regel #95 §3.3
    demo = zl._demografie_ab65()
    name = {str(r[0]).zfill(8): r[4] for r in roh}
    punkte, ohne = [], {"gf": [], "geheim": [], "neu": [], "keine": []}
    for ags, lon, lat, bez, _gen in roh:
        a = str(ags).zfill(8)
        zeile, ebene = zl.demografie_zeile_ab65(a)
        if ebene == "gemeinde":
            punkte.append((a, float(lon), float(lat), zeile[0],
                           zl.anteil_ab65_gemeinde(zeile, teil)))
        # Die Kreiszeile liefert den 65+-Anteil, aber nicht die Einwohner der
        # Gemeinde — ohne Einwohner kein Gewicht. Grund je Punkt aus den Daten:
        elif ebene is None:
            ohne["keine"].append(a)                     # weder Gemeinde- noch Kreiszeile
        elif bez == "Gemeindefreies Gebiet":
            ohne["gf"].append(a)
        elif a in demo:
            ohne["geheim"].append(a)                    # Zensuszeile ».«
        elif (wsk_gem.get(a) or "") > ZENSUS_STICHTAG:
            ohne["neu"].append(a)                       # nach dem Stichtag neu gebildet
        else:
            raise SystemExit(f"Punkt {a} ohne Gemeindezeile: Grund nicht aus den Daten ablesbar")
    n_kreis = len(roh) - len(punkte) - len(ohne["keine"])
    # Zensus-Gemeinden ohne Punkt im Gebietsstand 2026, Grund je Posten aus den Daten.
    fehlend = {k: v[0] for k, v in demo.items()
               if v is not None and len(k) == 8 and k not in name}
    ew_ohne_punkt = sum(fehlend.values())
    ew_gemeinden = sum(v[0] for k, v in demo.items() if v is not None and len(k) == 8)
    # Schlüsselwechsel: ein Kreis ohne Zensuszeile mit genau einem Punkt und genau eine
    # fehlende Zensus-Gemeinde desselben Landes, deren Kreis dieselbe Wirksamkeit trägt.
    wechsel: dict[str, str] = {}
    for n in sorted(k for k in kreise if k not in demo):
        neu = [a for a in name if a[:5] == n]
        alt = [k for k in fehlend if k[:2] == n[:2] and wsk_krs.get(k[:5]) == wsk_krs[n]]
        if len(neu) != 1 or len(alt) != 1:
            raise SystemExit(f"Kreis {n} ohne Zensuszeile: Zuordnung nicht eindeutig")
        wechsel[alt[0]] = neu[0]
    aufgegangen = [k for k in fehlend if k not in wechsel]
    # Beleg: Im Kreis jeder dieser Gemeinden trägt eine Gemeinde des Gebietsstands 2026
    # eine Änderung mit Wirksamkeit nach dem Zensusstichtag.
    ohne_beleg = [k for k in aufgegangen
                  if not any((wsk_gem.get(a) or "") > ZENSUS_STICHTAG
                             for a in name if a[:5] == k[:5])]
    if ohne_beleg:
        raise SystemExit(f"Zensus-Gemeinden ohne Punkt und ohne Änderung im Kreis: {ohne_beleg}")
    n_pop = len(punkte)
    ags = np.array([p[0] for p in punkte])
    lon = np.array([p[1] for p in punkte])
    lat = np.array([p[2] for p in punkte])
    ew = np.array([p[3] for p in punkte])
    o65 = np.array([p[4] for p in punkte])

    # ── Raster 1997–2022 an den Punkten ─────────────────────────────────────
    tr = Transformer.from_crs("EPSG:4326", "EPSG:31467", always_xy=True)
    gx, gy = tr.transform(lon, lat)
    reihen: dict[str, np.ndarray] = {}
    nodata_pkt = np.zeros(n_pop, dtype=bool)
    nd_jahre = {"ssd": np.zeros(n_pop, dtype=int), "rad": np.zeros(n_pop, dtype=int)}
    for key, loader in (("ssd", H._ssd_grid), ("rad", H._rad_grid)):
        werte = []
        for jahr in H.JAHRE:
            hdr, arr = loader(jahr)
            col = ((gx - hdr["XLLCORNER"]) / hdr["CELLSIZE"]).astype(int)
            row = ((gy - hdr["YLLCORNER"]) / hdr["CELLSIZE"]).astype(int)
            v = arr[arr.shape[0] - 1 - row, col].astype(float)
            nd = v == hdr.get("NODATA_VALUE", -999.0)
            nodata_pkt |= nd
            nd_jahre[key] += nd
            werte.append(v)
        reihen[key] = np.array(werte)                   # (Jahre, Punkte)
    t_ssd = _trend_matrix(H.JAHRE, reihen["ssd"])
    t_rad = _trend_matrix(H.JAHRE, reihen["rad"])
    # Gegenprobe gegen den importierten Leser H._trend an einem Punkt.
    assert abs(H._trend(list(reihen["ssd"][:, 0])) - t_ssd[0]) < 1e-9

    d_norm = np.array([((pr[1] - pr[0]) / pr[0]) if (pr := snp.ssd_at(x, y)) and pr[0] > 0
                       else np.nan for x, y in zip(lon, lat)])
    # Dieselben Regeln wie k_uv_herleitung.py (Befund 297): gilt / stabil.
    gilt = (np.isfinite(t_ssd) & np.isfinite(t_rad) & (t_ssd > 0)
            & np.isfinite(d_norm) & (d_norm > 0))
    stabil = gilt & (t_ssd > 1.0)
    n_gilt, n_stab = int(gilt.sum()), int(stabil.sum())

    # ── Gewicht: Baseline-Fälle × ΔSSD, €-gewichtet aus MM und C44 ──────────
    u65, p65 = ew * (1 - o65), ew * o65
    bands = {"u20": u65 * zl.NATIONAL_U20_SHARE_OF_U65,
             "a20_64": u65 * (1 - zl.NATIONAL_U20_SHARE_OF_U65),
             "a65_74": p65 * zl.NATIONAL_SENIOR_SPLIT["a65_74"],
             "a75_84": p65 * zl.NATIONAL_SENIOR_SPLIT["a75_84"],
             "a85p": p65 * zl.NATIONAL_SENIOR_SPLIT["a85p"]}
    f_mm = sum(bands[b] * UV_INCIDENCE_MM[b] / 1e5 for b in bands)
    f_c44 = sum(bands[b] * UV_INCIDENCE_C44[b] / 1e5 for b in bands)
    # €-Anteil MM: wortgleich aus k_uv_herleitung.py main() (Befund 290); dort
    # lokal definiert und deshalb nicht importierbar — Gegenprobe gegen die Anlage.
    anker = {"mm": (26_140 + 27_040 + 27_430) / 3, "c44": (236_670 + 243_430 + 242_820) / 3}
    lam = {"mm": (2928 + 3146 + 3169) / 3 / anker["mm"],
           "c44": (1178 + 1275 + 1332) / 3 / anker["c44"]}
    l_yll = {"mm": 10.4569, "c44": 5.4787}
    baf = {"mm": 0.6, "c44": 1.675}
    c_fall = {"mm": 6724.0, "c44": 5883.0}
    eur = {e: anker[e] * baf[e] * (c_fall[e] + lam[e] * l_yll[e] * 160_800.0) for e in anker}
    a_mm = eur["mm"] / sum(eur.values())
    if abs(a_mm - EUR_ANTEIL_MM_ANLAGE) > 5e-5:
        print(f"BLOCKIERT: €-Anteil MM {a_mm:.4f} weicht von der Anlage ab")
        return 2
    s = stabil
    w_mm = np.where(s, f_mm * d_norm, 0.0)
    w_c44 = np.where(s, f_c44 * d_norm, 0.0)
    gew = a_mm * w_mm / w_mm.sum() + (1 - a_mm) * w_c44 / w_c44.sum()   # Σ = 1
    q_pkt = np.where(s, t_rad / np.where(s, t_ssd, 1.0), 0.0)
    q_mm = float((w_mm * q_pkt).sum() / w_mm.sum())
    q_c44 = float((w_c44 * q_pkt).sum() / w_c44.sum())
    q_bund_roh = a_mm * q_mm + (1 - a_mm) * q_c44
    q_bund = round(q_bund_roh, 4)
    assert abs(float((gew * q_pkt).sum()) - q_bund_roh) < 1e-12
    abw = q_bund - Q_BUND_ANLAGE
    print(f"Punkte {n_vg} -> {n_pop} -> {n_gilt} -> {n_stab}; NODATA-Punkte "
          f"{int(nodata_pkt.sum())} (stabil {int((nodata_pkt & s).sum())})")
    print(f"q_Bund = {q_bund:.4f} (MM {q_mm:.4f}, C44 {q_c44:.4f}); Abweichung {abw:+.4f}")
    if abs(abw) > TOLERANZ:
        print("BLOCKIERT: q_Bund liegt mehr als 0,003 neben 0,6683 — keine Anlage.")
        return 1

    # ── (a) Kreis- und Landeswerte ──────────────────────────────────────────
    def gruppen(stellen: int) -> dict[str, np.ndarray]:
        schl = np.array([a[:stellen] for a in ags])
        return {k: np.flatnonzero(s & (schl == k)) for k in sorted(set(schl[s]))}

    kr = gruppen(5)
    la = gruppen(2)
    k_ids = list(kr)
    g_k = np.array([gew[kr[k]].sum() for k in k_ids])
    q_k = np.array([(gew[kr[k]] * q_pkt[kr[k]]).sum() / gew[kr[k]].sum() for k in k_ids])
    ew_k = np.array([ew[kr[k]].sum() for k in k_ids])
    n_k = np.array([len(kr[k]) for k in k_ids])
    q_l = {k: float((gew[i] * q_pkt[i]).sum() / gew[i].sum()) for k, i in la.items()}
    perz = {p: float(np.percentile(q_k, p)) for p in (5, 10, 50, 90, 95)}

    # ── (b) Rangtreue: € je Einwohner ∝ Σ (Gewicht × q) ÷ Einwohner ──────────
    eur_bund = g_k * q_bund_roh / ew_k
    eur_kreis = g_k * q_k / ew_k
    rangtreue = spearman(eur_bund, eur_kreis)

    # ── (c) Zeitstabilität: q je Kreis aus den Halbzeit-Trends ───────────────
    idx = {j: i for i, j in enumerate(H.JAHRE)}
    q_h = []
    ssd_pos = np.ones(len(k_ids), dtype=bool)
    for jahre in HAELFTEN:
        zeilen = [idx[j] for j in jahre]
        th_ssd = _trend_matrix(jahre, reihen["ssd"][zeilen])
        th_rad = _trend_matrix(jahre, reihen["rad"][zeilen])
        tk_ssd = np.array([(gew[kr[k]] * th_ssd[kr[k]]).sum() / gew[kr[k]].sum() for k in k_ids])
        tk_rad = np.array([(gew[kr[k]] * th_rad[kr[k]]).sum() / gew[kr[k]].sum() for k in k_ids])
        ssd_pos &= tk_ssd > 0
        q_h.append(np.where(tk_ssd != 0, tk_rad / np.where(tk_ssd != 0, tk_ssd, 1.0), np.nan))
    n_zeit = int(ssd_pos.sum())
    zeitstab = spearman(q_h[0][ssd_pos], q_h[1][ssd_pos])
    k_zeit_raus = [kreise.get(k, k) for k, ok in zip(k_ids, ssd_pos) if not ok]

    # ── Kreise des Gebietsstands ohne Kreiswert, Grund aus den Daten ─────────
    kreis_von = np.array([a[:5] for a in ags])

    def punkt_grund(j: int) -> str:
        if not (np.isfinite(t_ssd[j]) and np.isfinite(t_rad[j])):
            return "hat keine auswertbare Trendreihe"
        if t_ssd[j] <= 0:
            return (f"hat einen SSD-Trend 1997–2022 von {_z(t_ssd[j], 2)} %/Dekade und "
                    "fällt an »SSD-Trend > 0« heraus")
        if not (np.isfinite(d_norm[j]) and d_norm[j] > 0):
            return "fällt an »ΔSSD der Normalperioden > 0« heraus"
        return f"hat einen SSD-Trend von {_z(t_ssd[j], 2)} %/Dekade, unter 1 %/Dekade"

    krs_raus = []
    for k in sorted(set(kreise) - set(k_ids)):
        i = np.flatnonzero(kreis_von == k)
        if len(i) == 0:
            g = "sein Punkt hat keine eigene Gemeindezeile im Zensus und damit kein Gewicht"
        elif len(i) == 1:
            g = f"sein einziger Punkt mit Gewicht {punkt_grund(int(i[0]))}"
        else:
            g = f"keiner seiner {len(i)} Punkte mit Gewicht bleibt in der Menge"
        krs_raus.append(f"{kreise[k]} ({k}): {g}")

    # ── NODATA in der stabilen Menge ─────────────────────────────────────────
    nd_s = np.flatnonzero(nodata_pkt & s)
    nd_voll = bool(len(nd_s)) and all(nd_jahre["rad"][j] == len(H.JAHRE)
                                      and nd_jahre["ssd"][j] == 0 for j in nd_s)
    if len(nd_s) and not (nd_voll and np.all(q_pkt[nd_s] == 0)):
        raise SystemExit("NODATA in der stabilen Menge anders als in allen Jahren der "
                         "Globalstrahlung: Text der Anlage passt nicht")
    nd_krs = sorted({ags[j][:5] for j in nd_s})
    nd_anteil = [float(gew[[j for j in nd_s if ags[j][:5] == k]].sum() / gew[kr[k]].sum())
                 for k in nd_krs]
    nd_bund = float(gew[nd_s].sum())
    print(f"Ohne Gewicht: {({k: len(v) for k, v in ohne.items()})}; Wechsel {wechsel}; "
          f"aufgegangen {len(aufgegangen)} ({sum(fehlend[k] for k in aufgegangen):.0f} EW)")
    print(f"Kreise ohne Wert: {krs_raus}; Zeitstabilität ohne: {k_zeit_raus}")
    print(f"NODATA stabil: {[name[ags[j]] for j in nd_s]}; Kreisanteile {nd_anteil}; "
          f"Bund {nd_bund:.6f}")

    r_rang, r_zeit = round(rangtreue, 2), round(zeitstab, 2)
    zweig = _zweig(r_rang, r_zeit)
    zweig_roh = _zweig(rangtreue, zeitstab)
    print(f"Kreise {len(k_ids)}; Rangtreue {rangtreue:.4f}; Zeitstabilität {zeitstab:.4f} "
          f"über {n_zeit} Kreise; Zweig {zweig} (ungerundet {zweig_roh})")

    # ── CSV: Kreiswerte ──────────────────────────────────────────────────────
    ew_quote = float(g_k.sum() / ew_k.sum())
    with open(os.path.join(DATA, "k_uv_raumstreuung.csv"), "w", newline="",
              encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["ags5", "kreis", "land", "punkte", "einwohner", "gewicht_anteil",
                    "q_kreis", "q_kreis_rel_bund", "q_1997_2009", "q_2010_2022",
                    "ssd_trend_positiv_beide", "index_eur_je_ew_bundeswert",
                    "index_eur_je_ew_kreiswert"])
        for i, k in enumerate(k_ids):
            w.writerow([k, kreise.get(k, ""), laender.get(k[:2], ""), int(n_k[i]),
                        int(ew_k[i]), f"{g_k[i]:.6f}", f"{q_k[i]:.4f}",
                        f"{q_k[i] / q_bund_roh - 1:.4f}", f"{q_h[0][i]:.4f}",
                        f"{q_h[1][i]:.4f}", int(ssd_pos[i]),
                        f"{g_k[i] / ew_k[i] / ew_quote:.4f}",
                        f"{g_k[i] * q_k[i] / q_bund_roh / ew_k[i] / ew_quote:.4f}"])

    # ── Anlage ───────────────────────────────────────────────────────────────
    p: list[str] = []
    p.append("# #98 — Räumliche Streuung von k_UV (Befund 449)\n")
    p.append("Teil von Anlage [73]. Erzeugt von "
             "`backend/scripts/kalibrierung/k_uv_raumstreuung.py`; die Kreiswerte stehen "
             "in `backend/data/kalibrierung/k_uv_raumstreuung.csv`. Grundlage ist die "
             "Festlegung der Gesamtschau zu T-1115 vom 27.09.2026 (»Räumliche Streuung "
             "von k_UV (Befund 449): Messung und Entscheidungsregel«). Punktmenge, "
             "Stabilitätsausschluss und Gewicht sind dieselben wie beim Bundeswert in "
             "`k_uv_herleitung.md`; die Leser der DWD-Raster sind aus "
             "`k_uv_herleitung.py` übernommen, dessen Anlage bleibt unverändert.\n")
    p.append("Gefragt ist, ob die Streuung des Rasterquotienten q = ΔGlobalstrahlung ÷ "
             "ΔSonnenscheindauer über die Gemeindepunkte ein räumliches Muster ist oder "
             "Schätzrauschen zweier Trends über 26 Jahre. Ein Wert je Kreis verschöbe die "
             "Reihenfolge der Kreise auch dann, wenn er nur Rauschen ist; wie stark, misst "
             "die Rangtreue. Dass der Bundeswert die Reihenfolge der Kommunen falsch "
             "darstellt (Aufgabe §8 E3, Zweig 3 der Festlegung), belegt aber nur ein "
             "beständiges Muster; das misst die Zeitstabilität.\n")
    p.append("**Abweichung vom Lauf vom 01.09.2026.** Die Gemeindepunkte kommen aus "
             "`backend/.cache/60_stichprobe/DE_VG250.gpkg`, Ebene `vg250_pk` "
             f"({_tsd(n_vg)} Punkte, Gebietsstand 2026); `backend/data/vg250/` gibt es "
             "auf dem Server nicht. Einwohner und 65+-Anteil je Gemeinde kommen aus "
             "`backend/data/kalibrierung/zensus2022_demografie_ab65.csv` über "
             "`zensus_loader.demografie_zeile_ab65` und `anteil_ab65_gemeinde` mit dem "
             "Anteil 2/7 der Gruppe 60–66, der Regel des Produkts (#95 §3.3). Sie "
             "ersetzen `backend/data/lite/zensus_gemeinde.json`, das auf dem Server "
             "fehlt. Deshalb weicht die Zahl der Punkte vom Lauf vom 01.09.2026 ab "
             "(dort 10.853 mit Einwohnerzahl). Ob der Bundeswert trotzdem derselbe ist, "
             "prüft Abschnitt 2.\n")

    p.append("## 1 Punktmengen-Kette\n")
    p.append(f"- **{_tsd(n_vg)}** Gemeindepunkte in `vg250_pk`")
    neu = sorted(ohne["neu"], key=lambda a: (wsk_gem[a], name[a]))
    p.append(f"- **{_tsd(n_pop)}** davon mit eigener Gemeindezeile im Zensus 2022, also "
             f"mit Einwohnerzahl und 65+-Anteil. Ohne Gewicht bleiben "
             f"{_tsd(n_vg - n_pop)} Punkte. {_tsd(n_kreis)} davon haben nur eine "
             "Kreiszeile, und die nennt den 65+-Anteil, aber nicht die Einwohner der Gemeinde:")
    p.append(f"  - {_tsd(len(ohne['gf']))} gemeindefreie Gebiete.")
    p.append("  - " + _liste([f"{name[a]} ({a})" for a in ohne["geheim"]])
             + ": Der Zensus weist ».« aus (unbekannt oder geheim).")
    p.append(f"  - {_tsd(len(neu))} Gemeinden, die nach dem Zensusstichtag 15.05.2022 neu "
             "gebildet wurden und deshalb keine eigene Zeile haben (Wirksamkeit laut VG250): "
             + _liste([f"{name[a]} ({_datum(wsk_gem[a])})" for a in neu]) + ".")
    p.append("  - Gar keine Zeile hat "
             + _liste([f"{name[a]} ({a}), seit {_datum(wsk_krs[a[:5]])} "
                       f"{kreis_bez[a[:5]][:1].lower() + kreis_bez[a[:5]][1:]}; auch für "
                       f"seinen Kreis {a[:5]} hat der "
                       "Zensus keine Zeile" for a in ohne["keine"]]) + ".")
    p.append(f"- Umgekehrt haben {_tsd(len(fehlend))} Gemeinden des Zensus mit zusammen "
             f"{_tsd(int(round(ew_ohne_punkt)))} Einwohnern "
             f"({_z(ew_ohne_punkt / ew_gemeinden * 100, 2)} %) keinen Punkt im "
             "Gebietsstand 2026:")
    for alt, neu_a in wechsel.items():
        p.append(f"  - {name[neu_a]}, im Zensus {alt} mit {_tsd(int(fehlend[alt]))} Einwohnern "
                 f"({_z(fehlend[alt] / ew_ohne_punkt * 100, 0)} %), ist nicht aufgegangen, "
                 f"sondern hat den Schlüssel gewechselt: Die Stadt steht seit "
                 f"{_datum(wsk_krs[neu_a[:5]])} unter {neu_a}, dem Punkt ohne jede Zeile. "
                 f"VG250 trägt für den neuen Kreis {neu_a[:5]} und für den abgebenden Kreis "
                 f"{alt[:5]} ({kreise[alt[:5]]}) dieselbe Wirksamkeit.")
    p.append(f"  - {_tsd(len(aufgegangen))} Gemeinden mit "
             f"{_tsd(int(round(sum(fehlend[k] for k in aufgegangen))))} Einwohnern sind in "
             f"anderen Gemeinden aufgegangen: In jedem ihrer "
             f"{_tsd(len({k[:5] for k in aufgegangen}))} Kreise trägt VG250 für mindestens "
             "eine Gemeinde eine Änderung mit Wirksamkeit nach dem Zensusstichtag.")
    p.append(f"- **{_tsd(n_gilt)}** davon mit auswertbaren Trendreihen in beiden Rastern "
             "(endlicher SSD- und Globalstrahlungstrend 1997–2022, SSD-Trend > 0, "
             "ΔSSD der Normalperioden > 0)")
    p.append(f"- **{_tsd(n_stab)}** nach dem Stabilitätsausschluss (SSD-Trend ≥ 1 %/Dekade) "
             f"— die Menge, über die alle folgenden Zahlen laufen. Sie liegen in "
             f"**{_tsd(len(k_ids))}** Kreisen und **{_tsd(len(la))}** Ländern.")
    p.append(f"  - VG250 führt im Gebietsstand 2026 {_tsd(len(kreise))} Kreise. Es fehlen "
             + "; ".join(krs_raus) + ". "
             + ("Dieser Kreis fehlt" if len(krs_raus) == 1 else "Beide fehlen"
                if len(krs_raus) == 2 else "Diese Kreise fehlen")
             + " deshalb auch in den Kreiswerten, der Rangtreue und der Zeitstabilität.")
    if len(nd_s):
        p.append(f"  - {_tsd(len(nd_s))} Punkte der Menge liegen in allen "
                 f"{len(H.JAHRE)} Jahren des Globalstrahlungsrasters auf einer Zelle ohne Wert "
                 "(NODATA), im Raster der Sonnenscheindauer in keinem: "
                 + _liste([name[ags[j]] for j in nd_s]) + ". Ihr Globalstrahlungstrend ist "
                 "damit 0 und ihr Punktquotient genau 0. Das drückt die Werte ihrer "
                 f"{_tsd(len(nd_krs))} Kreise: Jeder liegt um den Gewichtsanteil dieser "
                 "Punkte im Kreis niedriger, als er ohne sie läge, hier um "
                 f"{_z(min(nd_anteil) * 100, 2 if min(nd_anteil) < 0.01 else 1)}–"
                 f"{_z(max(nd_anteil) * 100, 2 if max(nd_anteil) < 0.01 else 1)} %. Im "
                 f"Bundeswert tragen sie {_z(nd_bund * 100, 2)} % des Gewichts. Die Regel des "
                 "Bundeswerts schließt sie nicht aus; nach der Festlegung bleiben sie "
                 "deshalb in der Menge.")
    p.append("")

    p.append("## 2 Reproduktion des Bundeswerts\n")
    p.append(f"q_Bund = {_z(a_mm)} × {_z(q_mm)} (MM) + {_z(1 - a_mm)} × {_z(q_c44)} (C44) "
             f"= **{_z(q_bund)}**. Die Anlage `k_uv_herleitung.md` nennt 0,6683; die "
             f"Abweichung ist {_z(abw)} und liegt innerhalb der Toleranz von 0,003. "
             "Die folgenden Zahlen gelten damit.\n")

    p.append("## 3 Kreis- und Landeswerte\n")
    p.append("q je Kreis (AGS Stellen 1–5) und je Land ist das gewichtete Mittel der "
             "Punktquotienten, mit demselben Gewicht wie der Bundeswert: Baseline-Fälle × "
             "ΔSSD der Normalperioden, als €-gewichtetes Mittel aus MM und C44. Über "
             "alle Punkte ergibt dieses Mittel genau q_Bund.\n")
    p.append(f"Perzentile der {_tsd(len(k_ids))} Kreiswerte, ungewichtet über die Kreise "
             "(lineare Interpolation):\n")
    p.append("| Perzentil | q je Kreis | relativ zu q_Bund |")
    p.append("|---|---|---|")
    for pz, name in ((5, "5."), (10, "10."), (50, "50. (Median)"), (90, "90."), (95, "95.")):
        p.append(f"| {name} | {_z(perz[pz])} | {_pz(perz[pz] / q_bund_roh - 1)} |")
    p.append("")
    p.append("Zwischen dem 10. und 90. Perzentil liegen die Kreiswerte bei "
             f"{_spanne(perz[10] / q_bund_roh - 1, perz[90] / q_bund_roh - 1)} um "
             f"q_Bund, zwischen dem 5. und 95. Perzentil bei "
             f"{_spanne(perz[5] / q_bund_roh - 1, perz[95] / q_bund_roh - 1)}. Zum "
             "Vergleich die Gemeindepunkte (`k_uv_herleitung.md`, Abschnitt 4): 5./95. "
             "Perzentil 0,3225/1,1671.\n")
    p.append("Die 16 Landeswerte:\n")
    p.append("| Land | Punkte | q je Land | relativ zu q_Bund |")
    p.append("|---|---|---|---|")
    for k in sorted(la):
        p.append(f"| {laender.get(k, k)} | {_tsd(len(la[k]))} | {_z(q_l[k])} | "
                 f"{_pz(q_l[k] / q_bund_roh - 1)} |")
    p.append("")

    p.append("## 4 Rangtreue und Zeitstabilität\n")
    p.append("Die Rangkorrelation nach Spearman vergleicht zwei Reihenfolgen derselben "
             "Kreise: 1 heißt gleiche Reihenfolge, 0 kein Zusammenhang, −1 umgekehrte "
             "Reihenfolge.\n")
    p.append(f"- **Rangtreue: {_z(rangtreue, 2)}** über {_tsd(len(k_ids))} Kreise, von "
             f"{_tsd(len(kreise))} im Gebietsstand 2026; die fehlenden nennt Abschnitt 1. "
             "Verglichen wird die Reihenfolge der Kreise nach dem Euro-Betrag je "
             "Einwohner, proportional zu Σ (Gewicht × q) ÷ Einwohner, einmal mit q_Bund "
             "für alle Kreise und einmal mit q je Kreis. Einwohner sind die der Punkte in "
             "der Menge aus Abschnitt 1.")
    p.append(f"- **Zeitstabilität: {_z(zeitstab, 2)}** über {_tsd(n_zeit)} Kreise. "
             "Verglichen wird q je Kreis aus den Trends 1997–2009 mit q je Kreis aus den "
             "Trends 2010–2022. q ist dabei jeweils der Quotient der gewichteten "
             "Kreistrends (Globalstrahlung ÷ Sonnenscheindauer), mit dem Gewicht aus "
             "Abschnitt 3. Einbezogen sind die Kreise mit positivem SSD-Trend in beiden "
             "Hälften; "
             + ("1 Kreis fällt" if len(k_ids) - n_zeit == 1
                else f"{_tsd(len(k_ids) - n_zeit)} Kreise fallen") + " deshalb heraus"
             + (f" ({_liste(k_zeit_raus)}).\n" if k_zeit_raus else ".\n"))

    p.append("## 5 Entscheidungsregel und Schwellen\n")
    p.append("Zweig 1 gilt bei Rangtreue ≥ 0,90: Der Bundeswert bleibt, denn die "
             "Vereinfachung ändert die Reihenfolge der Kreise nicht wesentlich. Zweig 2 "
             "gilt bei Rangtreue < 0,90 und Zeitstabilität < 0,50: Der Bundeswert bleibt, "
             "weil die Kreiswerte über die Zeit nicht stabil und damit nicht belegt sind. "
             "Zweig 3 gilt bei Rangtreue < 0,90 und Zeitstabilität ≥ 0,50: Die "
             "Vereinfachung stellt die Reihenfolge der Kommunen falsch dar (E3), und "
             "k_UV wird regional, als eigener Methodik-Schritt.\n")
    p.append("Die Schwellen 0,90 und 0,50 sind Setzungen von KAP3 (Festlegung vom "
             "27.09.2026). Angewandt wird die Regel auf die Werte, wie sie hier auf zwei "
             "Stellen gerundet stehen. Mit anderen Schwellen gälte:\n")
    p.append("| Schwelle Rangtreue | Zeitstabilität 0,40 | Zeitstabilität 0,50 | "
             "Zeitstabilität 0,60 |")
    p.append("|---|---|---|---|")
    for sr in (0.85, 0.90, 0.95):
        zellen = [f"Zweig {_zweig(r_rang, r_zeit, sr, sz)}" for sz in (0.40, 0.50, 0.60)]
        p.append(f"| {_z(sr, 2)} | " + " | ".join(zellen) + " |")
    p.append("")
    if zweig != zweig_roh:
        p.append(f"Ungerundet ergäbe die Regel Zweig {zweig_roh}; die Werte liegen an "
                 "einer Schwelle.\n")
    p.append(f"Es gilt **Zweig {zweig}**. Es entscheidet das Ergebnis der Regel; eine "
             "Prüfung wendet sie an und entscheidet sie nicht neu.\n")

    p.append("## 6 Ergebnis\n")
    p.append(f"Reproduktion: q_Bund = {_z(q_bund)}\n")
    p.append(f"Rangtreue: Rangkorrelation = {_z(r_rang, 2)}\n")
    p.append(f"Zeitstabilität: Rangkorrelation = {_z(r_zeit, 2)}\n")
    p.append(f"Zweig: {zweig}")

    out = "\n".join(p) + "\n"
    with open(os.path.join(DATA, "k_uv_raumstreuung.md"), "w", encoding="utf-8") as fh:
        fh.write(out)
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
