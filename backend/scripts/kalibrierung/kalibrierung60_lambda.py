#!/usr/bin/env python3
"""
Kalibrierung #60 (Gebäudeschäden Flusshochwasser): A*, M0 und der Niveau-Skalar lambda
reproduzierbar aus den Evidenzdateien (Werkzeugbefund 87).

Rechenweg wie im Bericht docs/methodik/60_gebaeudeschaeden_flusshochwasser.md:

  §4.1/§4.1a  A_ver = arithmetisches Mittel der 23 Jahreswerte 2002–2024
              (docs/evidenz/60_gdv_jahresreihe_2002_2024.csv, Spalte wert_mrd_eur;
              Kleinste-Quadrate-Schätzer bei zeitkonstanter Modellsumme)
  §4.2        A* = A_ver · w_wg · u · phi_fluss · kappa · pi
  §4.3        M0 = w_wohn · Wert je Wohngebäude · (339.000 · r_GK3+GK4 + 1.380.000 · r_GK2)
              mit den Klassenraten aus docs/evidenz/60_stichprobe/m0_klassenraten.csv,
              Zeilen gk3_gk4;alle und gk2;alle, Spalte rate_exponiert_hqextrem_1_pro_a
  §4.4        lambda = A* / M0

Die Vergleichswerte werden zur Laufzeit aus §4.4 des Berichts gelesen (Satz
"lambda = A*/M0 = <A*> / <M0> = <lambda>"); die Stellenzahl jedes Werts ist die dort
ausgewiesene. Weicht ein gerundeter Rechenwert vom Bericht ab, bricht das Skript per
assert ab.

Aufruf (aus dem Repo-Wurzelverzeichnis oder von überall):
    python3 backend/scripts/kalibrierung/kalibrierung60_lambda.py
"""
from __future__ import annotations

import csv
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
JAHRESREIHE = REPO / "docs/evidenz/60_gdv_jahresreihe_2002_2024.csv"
KLASSENRATEN = REPO / "docs/evidenz/60_stichprobe/m0_klassenraten.csv"
BERICHT = REPO / "docs/methodik/60_gebaeudeschaeden_flusshochwasser.md"

# §4.2 Folgefaktoren vom Anker zum Modellumfang (Zentralwerte; Abschätzungen von KAP3,
# Herleitung und Bänder im Bericht §4.2, Parameterliste §4.8)
W_WG = 0.65        # Anteil Wohngebäude an der Sach-Schadensumme
U = 1.54           # Hochrechnung auf den unversicherten Bestand (1/0,65)
PHI_FLUSS = 0.50   # Anteil flussseitig an Starkregen + Überschwemmung
KAPPA = 1.15       # Leistung -> Wiederherstellungskosten
PI = 1.07          # Preisstand 2024 -> 2026 (aus B4, Register 60-R24-01)

# §4.3 Mengengerüst und Wert je exponiertem Wohngebäude (Register 60-R17-01/60-R24-01,
# Destatis Tab. 2.1.3 für den Typ-Mix; Bericht §4.3 Punkte 1 und 2)
ADRESSEN_GK34 = 339_000
ADRESSEN_GK2 = 1_380_000
THETA_EFH = 0.596            # nationaler Typ-Mix EFH/ZFH (Wohnflächenanteil), gerundet wie im Bericht
N_EFH, N_MFH = 1950.0, 1533.0  # Wertsätze EUR2026/m2 BGF
WOHNFLAECHE = 208.0          # m2 je Wohngebäude
BGF_FAKTOR = 1.30            # BGF je m2 Wohnfläche
W_WOHN = 0.872               # Wohngebäudeanteil je Adresse (19,7 Mio. / 22,6 Mio.)

RATEN_SPALTE = "rate_exponiert_hqextrem_1_pro_a"  # Wahl des Nenners: Bericht §4.3 Punkt 3


def zahl(text: str) -> float:
    """Deutsche Dezimalschreibweise (Komma) in float."""
    return float(text.strip().replace(".", "").replace(",", "."))


def stellen(text: str) -> int:
    """Nachkommastellen einer im Bericht ausgewiesenen Zahl."""
    text = text.strip()
    return len(text.split(",", 1)[1]) if "," in text else 0


def lies_jahresreihe() -> list[float]:
    with JAHRESREIHE.open(encoding="utf-8", newline="") as f:
        zeilen = list(csv.DictReader(f, delimiter=";"))
    jahre = [int(z["jahr"]) for z in zeilen]
    assert jahre == list(range(2002, 2025)), f"Jahresreihe unvollständig: {jahre}"
    return [zahl(z["wert_mrd_eur"]) for z in zeilen]


def lies_klassenrate(klasse: str) -> float:
    with KLASSENRATEN.open(encoding="utf-8", newline="") as f:
        treffer = [z for z in csv.DictReader(f, delimiter=";")
                   if z["klasse"] == klasse and z["kommune"] == "alle"]
    assert len(treffer) == 1, f"Zeile {klasse};alle nicht eindeutig in {KLASSENRATEN}"
    return float(treffer[0][RATEN_SPALTE])


def lies_bericht_44() -> dict[str, str]:
    """Liest A*, M0 und lambda als Text aus §4.4 des Berichts."""
    text = BERICHT.read_text(encoding="utf-8")
    m = re.search(r"^### 4\.4 .*?$(.*?)^### ", text, re.S | re.M)
    assert m, "Abschnitt 4.4 im Bericht nicht gefunden"
    abschnitt = m.group(1)
    z = r"(\d+(?:,\d+)?)"
    m = re.search(r"\\\(\\lambda = A\^\{\*\}/M_0\\\)\s*=\s*" + z + r"\s*/\s*" + z
                  + r"\s*=\s*\*\*" + z + r"\*\*", abschnitt)
    assert m, "Satz 'lambda = A*/M0 = ... / ... = ...' in §4.4 nicht gefunden"
    return {"A*": m.group(1), "M0": m.group(2), "lambda": m.group(3)}


def main() -> int:
    reihe = lies_jahresreihe()
    a_ver = sum(reihe) / len(reihe)
    a_stern = a_ver * W_WG * U * PHI_FLUSS * KAPPA * PI

    r_gk34 = lies_klassenrate("gk3_gk4")
    r_gk2 = lies_klassenrate("gk2")
    n_mix = THETA_EFH * N_EFH + (1 - THETA_EFH) * N_MFH
    wert_geb = WOHNFLAECHE * BGF_FAKTOR * n_mix
    m0 = W_WOHN * wert_geb * (ADRESSEN_GK34 * r_gk34 + ADRESSEN_GK2 * r_gk2) / 1e9

    lam = a_stern / m0

    print(f"Eingang Jahresreihe: {JAHRESREIHE.relative_to(REPO)} ({len(reihe)} Jahre)")
    print(f"Eingang Klassenraten: {KLASSENRATEN.relative_to(REPO)} "
          f"(gk3_gk4 {r_gk34:.9f}/a, gk2 {r_gk2:.9f}/a)")
    print(f"A_ver  = {a_ver:.6f} Mrd. EUR/a")
    print(f"A*     = {a_stern:.6f} Mrd. EUR2026/a")
    print(f"M0     = {m0:.6f} Mrd. EUR2026/a")
    print(f"lambda = {lam:.6f}")

    bericht = lies_bericht_44()
    for name, wert in (("A*", a_stern), ("M0", m0), ("lambda", lam)):
        soll_text = bericht[name]
        k = stellen(soll_text)
        ist = round(wert, k)
        soll = zahl(soll_text)
        assert abs(ist - soll) < 0.5 * 10 ** -(k + 3), (
            f"{name}: gerechnet {ist:.{k}f}, Bericht §4.4 {soll_text}")
        print(f"Abgleich §4.4: {name} gerechnet {ist:.{k}f} = Bericht {soll_text} ({k} Stellen)")
    print("OK: A*, M0 und lambda stimmen mit §4.4 des Berichts überein.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
