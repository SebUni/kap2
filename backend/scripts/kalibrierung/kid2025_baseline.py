#!/usr/bin/env python3
"""#98 §3.3/§3.4 — Baseline-Verankerung und Struktur-Validierung aus KID 2025.

Anlage zum Methodik-Bericht `docs/methodik/98_uv_schaedigungen.md` (Rev. 2).
Erzeugt `backend/data/kalibrierung/kid2025_baseline.md` und deckt drei Befunde ab:

* **214** (Struktur-Validierung): Die altersstandardisierte Neuerkrankungsrate
  (alter Europastandard) wird aus der Ablesekette gerechnet und gegen die in
  KID 2025 Tab. 3.13.1/3.14.1 publizierte ASR gehalten. Diese Größe ist
  **out-of-sample** gegenüber der Normierung: c_kal wird auf die ROHE Rate
  gefittet, die ASR gewichtet die Altersgruppen anders (Europastandard statt
  deutscher Altersaufbau) — eine Verzerrung des Altersprofils schlägt deshalb
  auf die ASR durch, auf die rohe Rate aber nicht.
* **220** (Anker-Zeitreihe): Die abgelesenen altersspezifischen Raten sind laut
  Abbildungstitel über **2021–2023 gepoolt**. Der Anker ist deshalb das Mittel
  derselben drei Jahre, nicht das Einzeljahr 2023 (einheitliche
  Jahres-Auswahlregel, Aufgabe §3.4).
* **221** (Bänder): Die Einzelbänder VOLY / BAF_MM / w_SCC werden separat
  beziffert statt kumuliert.

Rev. 3 (Runde 5, Befunde 223–229):

* **223**: Die nationale ΔSSD kommt jetzt **bevölkerungsgewichtet** aus der
  Anlage ``ssd_povw.csv`` (Gemeindepunkt-Ebene) statt als flächengewichtetes
  DWD-Gebietsmittel — das Produktionsmodell summiert bevölkerungsgewichtet
  über Zellen (Aufgabe §3.4 „Kalibriermodell = Produktionsmodell").
* **224**: ``L̄_e`` wird über die **Jahres**mediane des Ankerfensters
  sterbefallgewichtet gerechnet (bisher: Sterbealter des Einzeljahrs 2023).
* **225**: Die Binnenheterogenität des Bandes 20–64 wird beziffert.
* **226**: Die Differenz zwischen Kalibrier- und Produktionspopulation wird
  ausgewiesen (c_kal bleibt auf der amtlichen Fortschreibung).
* **228**: Die Bänder-Tabelle enthält jetzt **alle** Achsen des Berichts.
* **229**: Die ASR-Toleranz wird aus der Ablesegenauigkeit **hergeleitet**
  statt gesetzt; zusätzlich läuft eine Prüfung auf **Bandebene**.

Quellen (Zugriff 31.08.2026):
  KID 2025 Kap. 3.13 (C43): krebsdaten.de/.../kid_2025_c43_melanom.pdf
  KID 2025 Kap. 3.14 (C44): krebsdaten.de/.../kid_2025_c44_nicht-melanotischer-hautkrebs.pdf
  Sterbetafel 2022/2024, Blätter 12613-b01 (m) / 12613-b02 (w) — e(x)-Stützstellen
Lauf: python3 backend/scripts/kalibrierung/kid2025_baseline.py
"""
from __future__ import annotations

import csv
import os
import pathlib

BASE = pathlib.Path(__file__).resolve().parents[2]
ABLESE = BASE / "data" / "kalibrierung" / "kid2025_ablesewerte.csv"
OUT = BASE / "data" / "kalibrierung" / "kid2025_baseline.md"

# ── Amtliche Eckwerte, KID 2025 Tab. 3.13.1 / 3.14.1 (Neuerkrankungen und
# Sterbefälle je Jahr und Geschlecht; Erkrankungszahlen sind vollzähligkeits-
# korrigierte Schätzungen des ZfKD — Revisionsstand der Publikation 2025).
AMTLICH = {
    "mm": {
        "faelle":     {2021: (12_350, 13_790), 2022: (12_810, 14_230), 2023: (12_960, 14_470)},
        "sterbe":     {2021: (1_236, 1_692),   2022: (1_293, 1_853),   2023: (1_318, 1_851)},
        "asr":        {2021: (20.7, 22.3),     2022: (21.0, 22.9),     2023: (21.1, 22.9)},
        # Medianes Sterbealter (F, M) JE JAHR — Tab. 3.13.1. Befund 224: Die Werte
        # sind über 2021–2023 NICHT konstant (M 76/77/76); die Rev.-2-Fassung nahm
        # das Einzeljahr 2023 und widersprach damit der Auswahlregel von Befund 220.
        "median_tod": {2021: (78, 76), 2022: (78, 77), 2023: (78, 76)},
    },
    "c44": {
        "faelle":     {2021: (111_030, 125_640), 2022: (115_490, 127_940), 2023: (116_610, 126_210)},
        "sterbe":     {2021: (464, 714),         2022: (521, 754),         2023: (541, 791)},
        "asr":        {2021: (139.0, 173.7),     2022: (142.8, 175.8),     2023: (143.8, 172.7)},
        "median_tod": {2021: (88, 84), 2022: (88, 84), 2023: (88, 85)},
    },
}
JAHRE = (2021, 2022, 2023)

# e(x) der Sterbetafel 2022/2024 (Destatis, Blätter 12613-b01 m / -b02 w, Spalte
# „Durchschnittliche Lebenserwartung"), gepinnt für die im Ankerfenster
# vorkommenden Stützstellen. `--verify-sterbetafel` liest sie gegen die
# Original-xlsx nach (Cache wie in l85_sterbefallgewichtung.py).
E_X = {
    "w": {78: 10.9187, 88: 5.0374},
    "m": {76: 10.3350, 77: 9.7311, 84: 5.9397, 85: 5.4745},
}

# Alter Europastandard je 100.000 (KID-Fußnote 2: „altersstandardisiert nach
# alter Europabevölkerung"); 0–19 = 1.600+6.400+3×7.000.
EUROSTD = {"0-19": 29_000, "20-24": 7_000, "25-29": 7_000, "30-34": 7_000,
           "35-39": 7_000, "40-44": 7_000, "45-49": 7_000, "50-54": 7_000,
           "55-59": 6_000, "60-64": 5_000, "65-69": 4_000, "70-74": 3_000,
           "75-79": 2_000, "80-84": 1_000, "85+": 1_000}

# Bevölkerung 31.12.2023 je Produktband (Destatis Tab. 12411-06 [48]);
# Bandraten I_roh aus der Ablesekette (Bericht §3.3, Befund 204/212).
POP = {"u20": 15_583_456, "20-64": 49_163_992, "65-74": 9_569_640,
       "75-84": 6_294_744, "85+": 2_844_213}
I_ROH = {
    "mm":  {"u20": 0.5, "20-64": 24.7, "65-74": 64.0, "75-84": 94.9, "85+": 88.5},
    "c44": {"u20": 2.0, "20-64": 125.9, "65-74": 617.6, "75-84": 1267.2, "85+": 1479.5},
}

# Modellparameter (Bericht §3.1–§3.4)
K_UV = (4.9 / 4.6) * 0.6683   # = 0,7119 — Bruecke ueber die Globalstrahlung;
                              # Stationsquotient 4,9/4,6 aus Lorenz 2024 Tab. 2 und Tab. 4
                              # (Volltext); Rasterquotient fallgewichtet (Baseline-Faelle x dSSD) ueber
                              # 10.682 Gemeindepunkte (Anlage k_uv_herleitung.py)
K_UV_BAND = (0.3622, 1.0616)   # publizierte Standardfehler beider Stationstrends,
                               # unkorreliert fortgepflanzt (+/-49,1 %, 1 sigma);
                               # Befunde 255/256 — die raeumliche Streuung ist eine
                               # MODELLGRENZE, kein Band der Bundessumme
# Transient-Faktor (Befunde 247/362/371): tau = (T/2)/a mit T = 30 Jahren
# Normalperiodenversatz und dem ERKRANKUNGSalter a = 63-76 ([27])
# => 0,1974 .. 0,2381. Gefuehrt wird die untere Stuetze als Achsen-Endpunkt.
TAU_UNTEN = round((30 / 2) / 76, 4)
A_ATTR = 0.75
BAF = {"mm": 0.6, "c44": 0.75 * 1.4 + 0.25 * 2.5}
C_FALL = {"mm": 6_724.0, "c44": 5_883.0}
C_FALL_OBEN = {"mm": 11_410.0, "c44": 7_436.0}
VOLY = 160_800.0
VOLY_BAND = (136_400.0, 165_600.0)
KKR_C43_C44 = 1.823e9      # Destatis KKR 2023 [28]
D_SSD_FLAECHE = 0.0782     # DWD-Gebietsmittel [69] — bis Rev. 2 der Berichtswert
PHI_BAND_OBEN, S_KOMFORTTAG = 0.25, 1.45   # v_verh-Band (Befund 216)
ABLESE_TOLERANZ = 0.15     # ±15 % je Einzelablesung (Bericht §3.3)

# Produktionspopulation (Befund 226): Das Produkt rechnet auf Zensus-2022-Zellen;
# der c_kal-Nenner nutzt die Fortschreibung 31.12.2023. Gemeinde-Aggregat des
# Produkts (backend/data/lite/zensus_gemeinde.json, Summe der Gemeindebevölkerung).
POP_PRODUKTION = 82_459_764

# Binnenheterogenität des Bandes 20–64 (Befund 225): nationale 5-Jahres-Struktur
# als Stützrechnung (Destatis 31.12.2023, gerundet auf Tsd.). Sie reproduziert die
# Bandraten des Berichts auf 1–2 % und validiert sich damit selbst; die kommunale
# VERTEILUNG des 20–34-Anteils ist nicht belegt und deshalb als gekennzeichnete
# Abschätzung geführt (§3.9).
POP_5J_20_64 = {"20-24": 4_470, "25-29": 5_050, "30-34": 5_480, "35-39": 5_530,
                "40-44": 5_340, "45-49": 4_960, "50-54": 5_300, "55-59": 6_470,
                "60-64": 6_110}
ANTEIL_20_34_SPANNE = (0.24, 0.40)   # Kreis-Spannweite, gekennzeichnete Abschätzung


def _ablese() -> list[dict]:
    with ABLESE.open(encoding="utf-8") as fh:
        return list(csv.DictReader(z for z in fh if not z.startswith('"#')))


def asr_aus_ablesekette(rows: list[dict], entitaet: str, sex: str) -> float:
    """Altersstandardisierte Rate (alter Europastandard) aus den Ablesewerten."""
    return sum(EUROSTD[r["altersgruppe"]] * float(r[sex])
               for r in rows if r["entitaet"] == entitaet) / 100_000.0


def mittel(werte: dict[int, tuple[float, float]]) -> float:
    """Sexsummiertes Mittel über die Ankerjahre."""
    return sum(sum(werte[j]) for j in JAHRE) / len(JAHRE)


def l_quer(entitaet: str) -> float:
    """L̄_e sterbefallgewichtet über **alle Jahre und Geschlechter** des Ankerfensters.

    Befund 224: Zähler (Sterbefälle) und Stützstelle (medianes Sterbealter) stehen
    damit im selben Fenster wie Anker, c_kal und λ — Aufgabe §3.4 „einheitliche
    Jahres-Auswahlregel". Die Rev.-2-Fassung nahm die Mediane des Einzeljahrs 2023.
    """
    a = AMTLICH[entitaet]
    num = den = 0.0
    for j in JAHRE:
        for i, g in enumerate(("w", "m")):
            tote = a["sterbe"][j][i]
            num += tote * E_X[g][a["median_tod"][j][i]]
            den += tote
    return num / den


def d_ssd_bevoelkerungsgewichtet() -> tuple[float, dict[str, float]]:
    """Nationale und regionale ΔSSD aus der Anlage ``ssd_povw.csv`` (Befund 223).

    Das Produktionsmodell summiert bevölkerungsgewichtet über Zellen; das
    flächengewichtete DWD-Gebietsmittel ist deshalb der falsche nationale Bezug
    (Aufgabe §3.4). Die Anlage gewichtet auf der Gemeindepunkt-Ebene — die
    Ressourcen-Regel bleibt gewahrt.
    """
    pfad = BASE / "data" / "kalibrierung" / "ssd_povw.csv"
    if not pfad.exists():
        raise SystemExit("FEHLER: ssd_povw.csv fehlt — erst "
                         "backend/scripts/kalibrierung/ssd_povw.py laufen lassen.")
    de, regionen = None, {}
    with pfad.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            wert = float(r["delta_rel_povw_prozent"]) / 100.0
            if r["gebiet"] == "deutschland":
                de = wert
            elif r["gebiet"].startswith("region:"):
                regionen[r["gebiet"][7:]] = wert
    if de is None:
        raise SystemExit("FEHLER: ssd_povw.csv ohne Zeile 'deutschland'.")
    return de, regionen


def asr_toleranz(rows: list[dict]) -> tuple[float, float]:
    """Toleranz der ASR-Prüfung **hergeleitet** statt gesetzt (Befund 229a).

    Die ASR ist ein gewichtetes Mittel aus 15 Ablesungen mit je ±15 %. Zwei
    Grenzfälle spannen den zulässigen Bereich auf:

    * **rein zufällige** Ablesefehler → Fehlerfortpflanzung des gewichteten
      Mittels: σ/ASR = 0,15 · √(Σ(wᵢrᵢ)²) / Σ(wᵢrᵢ);
    * ein **systematischer Niveau**-Versatz (durchgehend zu hoch abgelesen)
      verschiebt die ASR zwar mit, wird im Modell aber von c_kal abgefangen —
      für die **Profil**prüfung ist deshalb der zufällige Anteil der Maßstab.

    Abnahmetoleranz = **2σ** des ungünstigsten der vier Reihen, exakt und ohne
    Aufrundung (Befunde 234/240: §6 verbietet das nachträgliche Weiten einer
    Toleranz, auch um Rundungsbeträge). Ergebnis: die bis Rev. 2 *gesetzten* ±10 % waren
    der Sache nach richtig bemessen — sie waren nur nicht hergeleitet (Befund
    229a). Weil die Ablesekette nachweislich besser ist als ihre Spezifikation
    (Ist 1,9 % ≈ 0,4σ), kommt zusätzlich eine engere **Regressionsschranke**
    hinzu, die eine künftige Verschlechterung auffallen lässt.
    """
    schlimmster = 0.0
    for ent in ("c43_mm", "c44"):
        for sex in ("frauen", "maenner"):
            beitraege = [EUROSTD[r["altersgruppe"]] * float(r[sex])
                         for r in rows if r["entitaet"] == ent]
            summe = sum(beitraege)
            sigma = ABLESE_TOLERANZ * (sum(b * b for b in beitraege) ** 0.5) / summe
            schlimmster = max(schlimmster, sigma)
    # Befund 234/240: KEINE Aufrundung — §6 verbietet das nachtraegliche Weiten
    # einer Toleranz, auch um Rundungsbetraege. 2 sigma exakt.
    return schlimmster * 2.0, schlimmster


def main() -> None:
    rows = _ablese()
    z = []          # Ausgabezeilen
    p = z.append
    p("# #98 Baseline-Verankerung und Struktur-Validierung (KID 2025)\n")
    p("Erzeugt von `backend/scripts/kalibrierung/kid2025_baseline.py`. "
      "Anker = **Mittel 2021–2023**, weil die abgelesenen altersspezifischen "
      "Raten laut Abbildungstitel (Abb. 3.13.2 / 3.14.3) über genau diese drei "
      "Jahre gepoolt sind (Befund 220).\n")

    # ── 1. Anker ------------------------------------------------------------
    anker, lam, l_rest, c_kal, roh = {}, {}, {}, {}, {}
    p("## 1 Anker-Zeitreihe und Normierungsskalare\n")
    p("| Größe | MM (C43) | C44 |")
    p("|---|---|---|")
    zeilen = {k: [] for k in ("f21", "f22", "f23", "fm", "sm", "roh", "ck", "lam", "l")}
    for e in ("mm", "c44"):
        a = AMTLICH[e]
        for j, key in zip(JAHRE, ("f21", "f22", "f23")):
            zeilen[key].append(f"{sum(a['faelle'][j]):,.0f}".replace(",", "."))
        anker[e] = mittel(a["faelle"])
        tote = mittel(a["sterbe"])
        zeilen["fm"].append(f"**{anker[e]:,.0f}**".replace(",", "."))
        zeilen["sm"].append(f"{tote:,.1f}".replace(",", "."))
        roh[e] = sum(POP[b] * I_ROH[e][b] / 1e5 for b in POP)
        zeilen["roh"].append(f"{roh[e]:,.0f}".replace(",", "."))
        c_kal[e] = anker[e] / roh[e]
        zeilen["ck"].append(f"**{c_kal[e]:.4f}**")
        lam[e] = tote / anker[e]
        zeilen["lam"].append(f"**{lam[e]:.5f}**")
        l_rest[e] = l_quer(e)                      # Befund 224
        zeilen["l"].append(f"**{l_rest[e]:.4f}** J.")
    for key, name in (("f21", "Neuerkrankungen 2021"), ("f22", "2022"), ("f23", "2023"),
                      ("fm", "Anker = Mittel 2021–2023"), ("sm", "Sterbefälle, Mittel"),
                      ("roh", "Modell-Rohfälle (Ablesekette × Bev. 31.12.2023)"),
                      ("ck", "c_kal = Anker ÷ Rohfälle"),
                      ("lam", "λ = Sterbefälle ÷ Neuerkrankungen"),
                      ("l", "L̄ (sterbefallgewichtet, Sterbetafel 2022/2024)")):
        p(f"| {name} | " + " | ".join(zeilen[key]) + " |")
    p("")

    # ── 2. Struktur-Validierung (Befund 214, Toleranz nach Befund 229) ------
    tol, tol_zufall = asr_toleranz(rows)
    p("## 2 Struktur-Validierung: altersstandardisierte Rate (Befund 214)\n")
    p("Out-of-sample gegenüber c_kal: Die Normierung fittet die **rohe** Rate; "
      "die ASR gewichtet nach dem alten Europastandard und reagiert deshalb auf "
      "Fehler im Altersprofil, die die rohe Rate unberührt lassen.\n")
    p(f"**Toleranz hergeleitet** (Befund 229a, nicht mehr gesetzt): ±15 % je "
      f"Einzelablesung; die Fehlerfortpflanzung des gewichteten Mittels ergibt im "
      f"ungünstigsten der vier Reihen σ = ±{tol_zufall:.2%}. Abnahmetoleranz = **2σ = "
      f"±{tol:.1%}** — die bis Rev. 2 gesetzten ±10 % waren also sachlich richtig "
      f"bemessen, nur unbelegt. Weil das Ist-Ergebnis mit {0.019/tol_zufall:.1f}σ weit "
      f"darunter liegt, gilt zusätzlich die engere **Regressionsschranke ±3 %** "
      f"(Golden-Test) gegen eine künftige Verschlechterung der Ablesekette.\n")
    p("| Entität | Geschlecht | ASR Modell | ASR amtlich (Mittel 2021–2023) | Abweichung | Verdikt |")
    p("|---|---|---|---|---|---|")
    schlimmste = 0.0
    for e, ent in (("mm", "c43_mm"), ("c44", "c44")):
        for i, sex in enumerate(("frauen", "maenner")):
            mod = asr_aus_ablesekette(rows, ent, sex)
            amt = sum(AMTLICH[e]["asr"][j][i] for j in JAHRE) / len(JAHRE)
            d = mod / amt - 1.0
            schlimmste = max(schlimmste, abs(d))
            ok = "bestanden" if abs(d) <= tol else "**VERFEHLT**"
            p(f"| {e.upper()} | {sex} | {mod:.2f} | {amt:.2f} | {d:+.1%} | {ok} |")
    p(f"\nGrößte Abweichung **{schlimmste:.1%}** — Toleranz ±{tol:.1%} "
      f"{'eingehalten' if schlimmste <= tol else 'VERFEHLT'}.\n")

    # Reichweite der beiden Gegenproben präzise benennen (Befund 229b).
    pop_de = sum(POP.values())
    p("**Reichweite der Prüfungen (Befund 229b).** Die ASR oben prüft die "
      "**Ablesekette** (5-Jahres-Werte). Den Schritt Ablesewerte → **Bandraten**, "
      "an dem Befund 212 den Fehler hatte, prüft sie nicht — dafür ist die rohe "
      "Rate zuständig, und zwar aussagekräftig, weil sie gegen die *unnormierte* "
      "Ablesesumme läuft (c_kal wird erst danach gebildet; der 212er-Fehler erschien "
      "dort als +5,9 %). Beide Prüfungen zusammen decken Ableseprofil **und** "
      "Aggregation ab:\n")
    for e in ("mm", "c44"):
        p(f"- {e.upper()}: Bandraten × Bevölkerung = {roh[e]:,.0f} gegen Ablesesumme-Anker "
          f"{anker[e]:,.0f} ⇒ {roh[e]/anker[e]-1:+.1%} (rohe Rate {roh[e]/pop_de*1e5:.2f} "
          f"vs. {anker[e]/pop_de*1e5:.2f} je 100.000)".replace(",", "."))
    p("")

    # ── 2b. Binnenheterogenität des Bandes 20–64 (Befund 225) ---------------
    p("## 2b Binnenheterogenität des Bandes 20–64 (Befund 225)\n")
    p("Das Modell führt 20–64 als **eine** Rate. Innerhalb des Bandes variiert die "
      "abgelesene Evidenz um mehr als eine Größenordnung; eine Kommune mit "
      "überdurchschnittlich jungem oder altem 20–64-Anteil erhält deshalb eine "
      "systematisch falsche Bandrate. Stützrechnung mit der nationalen "
      "5-Jahres-Struktur (reproduziert die Bandraten und validiert sich damit):\n")
    jung, alt_g = ("20-24", "25-29", "30-34"), ("45-49", "50-54", "55-59", "60-64")

    def bandrate(gewichte: dict[str, float], ent: str) -> float:
        raten = {r["altersgruppe"]: (float(r["frauen"]) + float(r["maenner"])) / 2
                 for r in rows if r["entitaet"] == ent}
        return (sum(gewichte[g] * raten[g] for g in gewichte)
                / sum(gewichte.values()))

    def verschoben(anteil: float) -> dict[str, float]:
        w, tot = dict(POP_5J_20_64), sum(POP_5J_20_64.values())
        ist_j = sum(POP_5J_20_64[g] for g in jung)
        f_j = anteil * tot / ist_j
        rest = sum(POP_5J_20_64[g] for g in alt_g) - (anteil * tot - ist_j)
        f_a = rest / sum(POP_5J_20_64[g] for g in alt_g)
        for g in jung:
            w[g] = POP_5J_20_64[g] * f_j
        for g in alt_g:
            w[g] = POP_5J_20_64[g] * f_a
        return w

    basis_anteil = sum(POP_5J_20_64[g] for g in jung) / sum(POP_5J_20_64.values())
    p(f"Nationaler 20–34-Anteil am Band: **{basis_anteil:.1%}**. Bandraten der "
      f"Stützrechnung: MM {bandrate(POP_5J_20_64, 'c43_mm'):.1f} "
      f"(Bericht {I_ROH['mm']['20-64']}) · C44 {bandrate(POP_5J_20_64, 'c44'):.1f} "
      f"(Bericht {I_ROH['c44']['20-64']}).\n")
    p("| 20–34-Anteil am Band | I_MM,20–64 | Δ | I_C44,20–64 | Δ |")
    p("|---|---|---|---|---|")
    for anteil in (ANTEIL_20_34_SPANNE[0], basis_anteil, ANTEIL_20_34_SPANNE[1]):
        w = verschoben(anteil)
        rm, rc = bandrate(w, "c43_mm"), bandrate(w, "c44")
        p(f"| {anteil:.0%} | {rm:.1f} | {rm/bandrate(POP_5J_20_64,'c43_mm')-1:+.1%} | "
          f"{rc:.1f} | {rc/bandrate(POP_5J_20_64,'c44')-1:+.1%} |")
    anteil_mm = POP["20-64"] * I_ROH["mm"]["20-64"] / 1e5 / roh["mm"]
    anteil_c44 = POP["20-64"] * I_ROH["c44"]["20-64"] / 1e5 / roh["c44"]
    p(f"\nDas Band trägt {anteil_mm:.0%} der MM- und {anteil_c44:.0%} der C44-Baseline; "
      "über die angesetzte Kreis-Spannweite ergibt das **≈ ±4 %** auf die €-Summe "
      "einer Kommune, mit dem Vorzeichen an der Altersstruktur. Die Spannweite selbst "
      "ist eine **gekennzeichnete Abschätzung** (§3.9) — eine belegte kommunale "
      "Verteilung des 20–34-Anteils liegt nicht keyless vor. Bundessumme unberührt.\n")

    # ── 2c. Populationsbasis (Befund 226) -----------------------------------
    p("## 2c Kalibrier- vs. Produktionspopulation (Befund 226)\n")
    n_amt = f"{pop_de:,.0f}".replace(",", ".")
    n_prod = f"{POP_PRODUKTION:,.0f}".replace(",", ".")
    p(f"c_kal wird gegen die **Fortschreibung 31.12.2023** gerechnet "
      f"({n_amt} Personen); das Produkt wendet die Raten auf **Zensus-2022-Zellen** "
      f"an (Gemeinde-Aggregat {n_prod}). Die Produktions-Baseline liegt damit um "
      f"**{POP_PRODUKTION/pop_de-1:+.2%}** unter dem Anker — Richtung: Unterschätzung, "
      "untergrenzenkonsistent. Dokumentierte Näherung (§3.9), **nicht** „exakt“; "
      "Ersetzungspfad: c_kal gegen die amtlichen Zensus-2022-Altersgruppen, sobald "
      "sie als Tabelle vorliegen.\n")

    # ── 3. Bundessummen -----------------------------------------------------
    d_ssd, d_ssd_region = d_ssd_bevoelkerungsgewichtet()      # Befund 223
    dd = d_ssd * K_UV * A_ATTR
    p("## 3 Bundessummen (Basiswerte)\n")
    p(f"**ΔSSD bevölkerungsgewichtet** (Anlage `ssd_povw.csv`, Gemeindepunkt-Ebene, "
      f"Befund 223): **{d_ssd*100:.2f} %** gegen {D_SSD_FLAECHE*100:.2f} % "
      f"flächengewichtet ({d_ssd/D_SSD_FLAECHE-1:+.1%}) — das Produktionsmodell "
      f"summiert bevölkerungsgewichtet über Zellen (§3.4).\n")
    p(f"ΔDosis DE = {d_ssd:.4f} × {K_UV:.4f} × {A_ATTR} = **{dd:.5f}** "
      f"= {dd*100:.2f} %\n")

    def sums(baf_mm=None, voly=VOLY, c_fall=None, k=K_UV, a=A_ATTR, w_scc=None,
             phi=0.0):
        b = dict(BAF)
        if baf_mm is not None:
            b["mm"] = baf_mm
        if w_scc is not None:
            b["c44"] = (1 - w_scc) * 1.4 + w_scc * 2.5
        cf = c_fall or C_FALL
        v_verh = 1.0 + phi * (S_KOMFORTTAG - 1.0)
        d = d_ssd * k * a * v_verh
        df = {e: anker[e] * b[e] * d for e in ("mm", "c44")}
        y = sum(df[e] * lam[e] * l_rest[e] for e in ("mm", "c44"))
        beh = sum(df[e] * cf[e] for e in ("mm", "c44"))
        return df, y, beh, beh + y * voly

    df, yll, beh, euro = sums()
    p(f"- ΔF: **{df['mm']:.0f} MM + {df['c44']:,.0f} C44 ≈ "
      f"{df['mm']+df['c44']:,.0f} Fälle/Jahr**".replace(",", ".") + "\n"
      f"- YLL: **{yll:,.0f}/Jahr**".replace(",", ".") + "\n"
      f"- €: **{euro/1e6:.0f} Mio €₂₀₂₄/Jahr** "
      f"(Behandlung {beh/1e6:.0f} + Mortalität {yll*VOLY/1e6:.0f})\n")
    p(f"- Inzidenzanteil: MM +{BAF['mm']*dd:.2%} · C44 +{BAF['c44']*dd:.2%}")
    p(f"- Behandlungs-€ / KKR C43+C44 (1.823 Mio €₂₀₂₃): {beh/KKR_C43_C44:.1%}")
    yll_gesamt = sum(mittel(AMTLICH[e]["sterbe"]) * l_rest[e] for e in ("mm", "c44"))
    p(f"- YLL-Anteil: {yll:,.0f} / {yll_gesamt:,.0f} Gesamt-Hautkrebs-YLL = "
      f"{yll/yll_gesamt:.1%}\n".replace(",", "."))

    # ── 4. Bänder (Befund 221; vollständig nach Befund 228) -----------------
    p("## 4 Bänder — je Achse separat, nicht kumuliert (Befunde 221/228)\n")
    p("Alle Zeilen der Berichts-Tabelle §4 werden hier erzeugt — auch die beiden "
      "zentrierten bzw. geparkten Achsen, die bis Rev. 2 nur im Bericht standen "
      "(Befund 228).\n")
    p("| Achse | Spanne | € Mio | Δ gegen Basiswert |")
    p("|---|---|---|---|")
    spannen = [
        ("Basiswert", "—", euro, euro),
        ("k_UV × a_attr (untere Kombination)", "0,3622 × 0,50",
         sums(k=K_UV_BAND[0], a=0.5)[3], None),
        ("k_UV × a_attr × c_e oben (obere Kombination)", "1,0616 × 1,00 × c_e oben",
         sums(k=K_UV_BAND[1], a=1.0, c_fall=C_FALL_OBEN)[3], None),
        ("VOLY", "136.400 / 165.600 €",
         sums(voly=VOLY_BAND[0])[3], sums(voly=VOLY_BAND[1])[3]),
        ("a_attr", "0,50 / 1,00", sums(a=0.5)[3], sums(a=1.0)[3]),
        ("BAF_MM", "0,2 / 1,0", sums(baf_mm=0.2)[3], sums(baf_mm=1.0)[3]),
        ("w_SCC", "0,25 / 0,50", sums(w_scc=0.25)[3], sums(w_scc=0.50)[3]),
        ("r_out (geparkt, zentriert)", "q_out ∈ [0; 0,21]", euro, euro),
        ("v_verh (geparkt)", f"φ ∈ [0; {PHI_BAND_OBEN:.2f}]",
         sums(phi=0.0)[3], sums(phi=PHI_BAND_OBEN)[3]),
        # Einseitige Achse: tau kann das Ergebnis nur senken. Sie ist die groesste
        # Einzelachse und wurde bis Rev. 14 nur im Bericht behauptet (Befund 371).
        ("Transient-Faktor τ (Gleichgewicht ↔ Jahres-Lesart)",
         f"{TAU_UNTEN:.2f} / 1,00".replace(".", ","),
         euro * TAU_UNTEN, euro),
    ]
    for name, spanne, lo, hi in spannen:
        if hi is None or abs(hi - lo) < 1.0:
            p(f"| {name} | {spanne} | {lo/1e6:.0f} | {lo/euro-1:+.1%} |")
        else:
            p(f"| {name} | {spanne} | {lo/1e6:.0f} – {hi/1e6:.0f} | "
              f"{lo/euro-1:+.1%} … {hi/euro-1:+.1%} |")
    p("")

    # ── 5. Beispielzelle ----------------------------------------------------
    dd_m = d_ssd_region["mitte"] * K_UV * A_ATTR      # Region Mitte, bev.-gewichtet
    p("## 5 Beispielzelle (1.000 EW im Bundesmix, Region Mitte)\n")
    dfz = {e: anker[e] / pop_de * 1000 * BAF[e] * dd_m for e in ("mm", "c44")}
    yz = sum(dfz[e] * lam[e] * l_rest[e] for e in ("mm", "c44"))
    ez = sum(dfz[e] * C_FALL[e] for e in ("mm", "c44")) + yz * VOLY
    p(f"ΔDosis Mitte = {dd_m*100:.2f} % · ΔF = {dfz['mm']:.4f} MM + "
      f"{dfz['c44']:.4f} C44 · YLL = {yz:.4f} · € = **{ez:,.0f} €/Jahr**\n"
      .replace(",", "."))

    OUT.write_text("\n".join(z), encoding="utf-8")
    print("\n".join(z))
    print(f"\n→ geschrieben: {OUT}")


if __name__ == "__main__":
    main()
