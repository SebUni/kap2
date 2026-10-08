#!/usr/bin/env python3
"""Bevölkerungsgewichtete SSD-Normalperiodenänderung für #98 §3.2/§4 (Befund 223).

**Warum diese Anlage existiert.** Das Produktionsmodell rechnet die
klimaattribuierte Dosisänderung je Zelle und summiert Zellen zur Kommune:

    ΔF = Σ_Zellen F_Zelle · BAF · ΔDosis_Zelle ,   ΔDosis_Zelle ∝ ΔSSD_Zelle

Die wirksame nationale ΔSSD ist damit das **bevölkerungsgewichtete** Mittel der
relativen Zelländerungen — nicht das flächengewichtete DWD-Gebietsmittel
(+7,82 %), mit dem der Bericht bis Rev. 2 alle Bundessummen und Sanity-Bänder
gerechnet hat. Aufgabe §3.4 verlangt ausdrücklich „Kalibriermodell =
Produktionsmodell … unzulässig, sobald das Produktionsmodell … bevölkerungs-
gewichtete Exposition hat" (Ledger-Befund 223; dieselbe Fehlerklasse hat #95 in
Rev. 8 mit ``sommermittel_bundesland_povw.csv`` gelöst).

**Ressourcen-Regel (§3.4) gewahrt.** Kein nationaler 100-m-Vollraster-Lauf: Die
Gewichtung läuft auf der ausdrücklich erlaubten **Gemeindepunkt-Ebene**: der
VG250-Layer ``vg250_pk`` (Gebietsstand **01.01.2025**) führt 10.949 amtliche
Gemeindepunkte (Verwaltungssitz mit
Dezimalkoordinaten), von denen **10.824** eine Zensus-Gemeindebevölkerung UND einen
Rasterwert haben und in die Gewichtung eingehen. Das sind 10.824 Rasterablesungen
statt ~3,6 Mio Zellen.

**Gekennzeichnete Näherungen (§3.9, Befund 235).** (a) Gewichtet wird mit **Köpfen**,
das Produktionsmodell summiert aber **Baseline-Fälle**; weil die Altersstruktur
regional variiert, ist der exakte Bezug die fallgewichtete ΔSSD (Abweichung auf
Landesebene +0,11 % MM / +0,19 % C44 relativ). (b) Die gesamte Gemeindebevölkerung
wird an **einem** Punkt abgelesen (Berlin 3,59 Mio an einer 1-km-Zelle); gegen ein
Boxmittel gerechnet −0,28 % relativ. Beide sind klein und teils gegenläufig.

**Kalibriermodell = Produktionsmodell.** Die SSD-Werte werden über dieselbe
Produktfunktion gelesen, die auch die Schadensfunktion benutzt
(``app.services.climate.ssd_normalperioden.ssd_at``) — die Anlage kann sich
nicht von der Produktion entkoppeln.

Ausgaben (backend/data/kalibrierung/):
    ssd_povw.csv   je Gebiet: Gemeinden, Bevölkerung, ΔSSD bevölkerungsgewichtet und ungewichtetes Punktmittel
    ssd_povw.md    Kennzahlen, Bundes-, Landes- und Regionswerte, Wirkung auf die Bundessummen

Aufruf: python backend/scripts/kalibrierung/ssd_povw.py
Quellen: BKG VG250 (DL-DE->BY-2.0), Zensus 2022 (Destatis), DWD-CDC
``sunshine_duration`` 1 km (DL-DE->Zero-2.0) via ``ssd_normalperioden.npz``.
"""
from __future__ import annotations

import csv
import json
import os
import sqlite3
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, ROOT)
DATA = os.path.join(ROOT, "data", "kalibrierung")
GPKG = os.path.join(ROOT, "data", "vg250", "DE_VG250.gpkg")
GEMEINDEN = os.path.join(ROOT, "data", "lite", "zensus_gemeinde.json")

# Abschnitt »Eingangsdaten« der Anlage (T-1823, Nachträge 2 und 8 des CEO zu T-1662):
# Herkunft, Lizenz und Abrufbefehl je Eingangsdatei, damit die Anlage ohne
# Probeverzeichnis nachrechenbar ist. Steht gleichlautend in ssd_povw.md.
EINGANGSDATEN = """## Eingangsdaten

Das Skript liest zwei Dateien, die nicht im Repository liegen (`backend/data/vg250/` und `backend/data/lite/` stehen in `.gitignore`), und die Normalperioden-Raster `backend/data/kalibrierung/ssd_normalperioden.npz`, die im Repository liegen. Alle Pfade gelten ab dem Wurzelverzeichnis des Repositorys. Die Abrufbefehle legen die Dateien dorthin, wo `ssd_povw.py` sie erwartet; danach läuft `python backend/scripts/kalibrierung/ssd_povw.py` ohne Zwischenstände aus einem Probeverzeichnis.

### VG250 (GeoPackage)

- **Pfad:** `backend/data/vg250/DE_VG250.gpkg`, Ebene `vg250_pk` (Verwaltungspunkte), Gebietsstand 01.01.2025.
- **Herkunft:** Bundesamt für Kartographie und Geodäsie (BKG), Verwaltungsgebiete 1:250 000 (VG250), Ausgabe Stand 01.01., UTM32s-GeoPackage. Bezugsadresse: https://daten.gdz.bkg.bund.de/produkte/vg/vg250_ebenen_0101/2025/vg250_01-01.utm32s.gpkg.ebenen.zip (Katalogseite: https://gdz.bkg.bund.de/index.php/default/verwaltungsgebiete-1-250-000-ebenen-stand-01-01-vg250-ebenen-01-01.html).
- **Lizenz:** Datenlizenz Deutschland – Namensnennung – Version 2.0 (dl-de/by-2-0), Quelle: BKG.
- **Abrufbefehl** (aus dem Wurzelverzeichnis des Repositorys):

```
python3 -c "import io,os,urllib.request,zipfile;z=zipfile.ZipFile(io.BytesIO(urllib.request.urlopen('https://daten.gdz.bkg.bund.de/produkte/vg/vg250_ebenen_0101/2025/vg250_01-01.utm32s.gpkg.ebenen.zip',timeout=600).read()));n=[x for x in z.namelist() if x.endswith('DE_VG250.gpkg')][0];os.makedirs('backend/data/vg250',exist_ok=True);open('backend/data/vg250/DE_VG250.gpkg','wb').write(z.read(n))"
```

- **Gemessen am 07.10.2026:** Die so entpackte Datei hat SHA-256 `f229550c80180a11de7d235d8387b96fe535bdf60cb633ff2532009362d784e9` und 10.949 Punkte in `vg250_pk`, wie im Kopf dieser Anlage.
- **Gebietsstand beachten:** Die Adresse `…/aktuell/` und der Standardabruf des Produkts (`vg250_loader.ensure_vg250`) liefern den jeweils neuesten Gebietsstand, am 07.10.2026 den Stand 2026 mit 10.939 Punkten. Für die Zahlen dieser Anlage gilt der Stand 2025.

### Zensus-Gemeindedatei (JSON)

- **Pfad:** `backend/data/lite/zensus_gemeinde.json`, ein Eintrag je Gemeindeschlüssel (AGS, 8 Stellen); das Skript liest daraus das Feld `population` (Einwohner, Zensus 2022, Stichtag 15.05.2022).
- **Herkunft:** keine amtliche Einzeldatei, sondern eine Ableitung des Produkts: Die Gitterdaten 100 m des Zensus 2022 (Statistische Ämter des Bundes und der Länder) werden auf die Gemeindeflächen der VG250 aufsummiert (`app.services.lite.zensus_gemeinde.aggregate`, Phase C des Lite-Batches). Bezugsadressen der Gitterdateien: https://www.destatis.de/static/DE/zensus/gitterdaten/Zensus2022_Bevoelkerungszahl.zip, dazu `Anteil_ab_65-jaehrige_in_Gitterzellen.zip`, `Anteil_unter_18-jaehrige_in_Gitterzellen.zip` und `Gebaeude_nach_Baujahr_in_Mikrozensus_Klassen.zip` im selben Verzeichnis (https://www.destatis.de/static/DE/zensus/gitterdaten/). Diese drei gehen in die Datei ein, nicht in diese Anlage.
- **Lizenz:** Datenlizenz Deutschland – Namensnennung – Version 2.0 (dl-de/by-2-0), © Statistische Ämter des Bundes und der Länder.
- **Abrufbefehl**, erst die Gitterdateien (legt die CSV unter `backend/data/zensus/extract/<Schlüssel>/` ab):

```
cd backend && python3 -c "from app.services import zensus_loader as zl;[zl.ensure_zensus_dataset(k) for k in ('population','share_over_65','share_under_18','building_age')]"
```

  dann die Aggregation, die die JSON-Datei an den oben genannten Pfad schreibt: als Administrator `POST /api/admin/lite-batch` mit dem Inhalt `{"bundesland": null, "force_zensus": true}`. Der Batch liest die VG250-Datei aus dem Abschnitt davor; sie muss deshalb vorher an ihrem Pfad liegen, sonst lädt er den neuesten Gebietsstand.
- **Grenze dieser Fassung:** Der Aggregationsschritt braucht die Datenbank des Produkts (PostGIS-Tabelle `gemeinden`) und schreibt die Gemeindedatei `backend/data/lite/zensus_gemeinde.json`, die `ssd_povw.py` liest. Ohne die Datenbank lässt er sich nicht ausführen; die beiden Befehle sind in diesem Lauf nicht ausgeführt worden. Die Anlage `ssd_povw.md` ist deshalb von Hand fortgeschrieben und nicht neu erzeugt; der Abschnitt steht in Skript und Anlage gleichlautend.
"""

# Regionszuordnung wie ``dwd_ssd_trend.py``/Bericht §3.2 (Nord/Mitte/Süd).
REGION = {
    "01": "nord", "02": "nord", "03": "nord", "04": "nord", "13": "nord",
    "05": "mitte", "06": "mitte", "07": "mitte", "10": "mitte", "11": "mitte",
    "12": "mitte", "14": "mitte", "15": "mitte", "16": "mitte",
    "08": "sued", "09": "sued",
}
LAND = {
    "01": "Schleswig-Holstein", "02": "Hamburg", "03": "Niedersachsen",
    "04": "Bremen", "05": "Nordrhein-Westfalen", "06": "Hessen",
    "07": "Rheinland-Pfalz", "08": "Baden-Württemberg", "09": "Bayern",
    "10": "Saarland", "11": "Berlin", "12": "Brandenburg",
    "13": "Mecklenburg-Vorpommern", "14": "Sachsen", "15": "Sachsen-Anhalt",
    "16": "Thüringen",
}

# Modellparameter für die Wirkungsrechnung (Bericht §3.1–§3.4, Rev. 15; k_UV nach Log Nr. 29).
K_UV, A_ATTR = (4.9 / 4.6) * 0.6683, 0.75   # k_UV rasterskaliert (Befunde 238/245/252)
BAF = {"mm": 0.6, "c44": 0.75 * 1.4 + 0.25 * 2.5}
ANKER = {"mm": (26_140 + 27_040 + 27_430) / 3,
         "c44": (236_670 + 243_430 + 242_820) / 3}
LAMBDA = {"mm": (2928 + 3146 + 3169) / 3 / ANKER["mm"],
          "c44": (1178 + 1275 + 1332) / 3 / ANKER["c44"]}
L_REST = {"mm": 10.4569, "c44": 5.4787}          # Befund 224 (Ankerfenster)
C_FALL = {"mm": 6_724.0, "c44": 5_883.0}
VOLY = 160_800.0
D_SSD_FLAECHE = 0.0782                            # DWD-Gebietsmittel [69]


def gemeindepunkte() -> list[tuple[str, float, float]]:
    """AGS + Dezimalkoordinaten der amtlichen Gemeindepunkte (VG250 ``vg250_pk``)."""
    con = sqlite3.connect(GPKG)
    try:
        rows = con.execute(
            "SELECT AGS, LON_DEZ, LAT_DEZ FROM vg250_pk "
            "WHERE AGS IS NOT NULL AND LON_DEZ IS NOT NULL").fetchall()
    finally:
        con.close()
    return [(str(a).zfill(8), float(x), float(y)) for a, x, y in rows]


def main() -> None:
    from app.services.climate import ssd_normalperioden as ssd

    pop_je_ags = {k: float(v.get("population") or 0.0)
                  for k, v in json.load(open(GEMEINDEN, encoding="utf-8")).items()}
    punkte = gemeindepunkte()

    # Akkumulatoren je Gebiet: [Σ pop, Σ pop·Δrel, Σ Δrel, n]
    acc: dict[str, list[float]] = {}
    ohne_raster = ohne_pop = 0
    for ags, lon, lat in punkte:
        pop = pop_je_ags.get(ags)
        if pop is None or pop <= 0:
            ohne_pop += 1
            continue
        paar = ssd.ssd_at(lon, lat)
        if paar is None or paar[0] <= 0:
            ohne_raster += 1
            continue
        ref, neu = paar
        d = (neu - ref) / ref
        for gebiet in ("deutschland", f"land:{LAND[ags[:2]]}",
                       f"region:{REGION[ags[:2]]}"):
            a = acc.setdefault(gebiet, [0.0, 0.0, 0.0, 0.0])
            a[0] += pop
            a[1] += pop * d
            a[2] += d
            a[3] += 1

    de = acc["deutschland"]
    povw_de = de[1] / de[0]
    flaeche_de = de[2] / de[3]        # ungewichtetes Gemeindepunkt-Mittel

    rows = []
    for gebiet in sorted(acc):
        a = acc[gebiet]
        rows.append({
            "gebiet": gebiet,
            "gemeinden": int(a[3]),
            "bevoelkerung": round(a[0]),
            "delta_rel_povw_prozent": round(a[1] / a[0] * 100, 3),
            "delta_rel_punktmittel_prozent": round(a[2] / a[3] * 100, 3),
        })
    with open(os.path.join(DATA, "ssd_povw.csv"), "w", newline="",
              encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    def bundessumme(d_ssd: float) -> tuple[dict, float, float, float]:
        dd = d_ssd * K_UV * A_ATTR
        df = {e: ANKER[e] * BAF[e] * dd for e in ANKER}
        yll = sum(df[e] * LAMBDA[e] * L_REST[e] for e in df)
        beh = sum(df[e] * C_FALL[e] for e in df)
        return df, yll, beh, beh + yll * VOLY

    z = ["# #98 — Bevölkerungsgewichtete SSD-Normalperiodenänderung (Befund 223)\n",
         "Erzeugt von `backend/scripts/kalibrierung/ssd_povw.py`. Gewichtung auf der",
         "**Gemeindepunkt-Ebene** (§3.4 ausdrücklich zulässig; kein 100-m-Vollraster-Lauf):",
         f"{int(de[3]):,}".replace(",", ".")
         + " amtliche Gemeindepunkte (BKG VG250 `vg250_pk`, Gebietsstand 01.01.2025)",
         "mit Zensus-2022-Gemeindebevölkerung; SSD über die **Produktfunktion**",
         "`ssd_normalperioden.ssd_at` gelesen (Kalibriermodell = Produktionsmodell).\n",
         # Punktmengen-Kette gemessen, nicht fortgeschrieben (Befund 396): Der
         # Bericht nennt alle Stufen; die ersten beiden entstehen hier beim Join.
         "**Punktmengen-Kette (Befund 396):** VG250 `vg250_pk` führt "
         + f"{len(punkte):,}".replace(",", ".")
         + " amtliche Gemeindepunkte; davon "
         + f"{len(punkte) - ohne_pop:,}".replace(",", ".")
         + f" mit Zensus-2022-Einwohnerzahl ({ohne_pop} ohne) und davon "
         + f"{int(de[3]):,}".replace(",", ".")
         + f" mit SSD-Rasterwert ({ohne_raster} ohne) — diese gehen in die Gewichtung ein.\n",
         "## 1 Nationale ΔSSD\n",
         "| Aggregation | ΔSSD DE | Bezug |",
         "|---|---|---|",
         f"| DWD-Gebietsmittel (**flächen**gewichtet, Anlage [69]) | **{D_SSD_FLAECHE*100:.2f} %** | bisheriger Berichtswert |",
         f"| Gemeindepunkte, ungewichtet | {flaeche_de*100:.2f} % | Kontrolle: nahe am Flächenmittel |",
         f"| Gemeindepunkte, **bevölkerungsgewichtet** | **{povw_de*100:.2f} %** | wirksamer Wert des Produktionsmodells |",
         "",
         f"Korrektur gegenüber dem Flächenmittel: **{povw_de/D_SSD_FLAECHE-1:+.1%}**.",
         "Ursache: Die einwohnerstarken Länder (NRW, Hessen, Niedersachsen) haben",
         "überdurchschnittliche Zuwächse, die dünn besiedelten Küsten- und",
         "Nordostländer unterdurchschnittliche.\n",
         "## 2 Je Region und Bundesland\n",
         "| Gebiet | Gemeinden | Bevölkerung | ΔSSD bev.-gew. | ΔSSD Punktmittel |",
         "|---|---|---|---|---|"]
    for r in rows:
        z.append(f"| {r['gebiet']} | {r['gemeinden']:,} | {r['bevoelkerung']:,} | "
                 f"**{r['delta_rel_povw_prozent']:.2f} %** | "
                 f"{r['delta_rel_punktmittel_prozent']:.2f} % |".replace(",", "."))

    z.append("\n## 3 Wirkung auf die Bundessummen (Basiswerte, L̄ nach Befund 224)\n")
    z.append("| Größe | flächengewichtet (Vergleich) | **bevölkerungsgewichtet (Basiswert)** | Δ |")
    z.append("|---|---|---|---|")
    a_df, a_y, a_b, a_e = bundessumme(D_SSD_FLAECHE)
    n_df, n_y, n_b, n_e = bundessumme(povw_de)
    for name, alt, neu, fmt in (
            ("ΔDosis DE", D_SSD_FLAECHE * K_UV * A_ATTR, povw_de * K_UV * A_ATTR, "{:.4%}"),
            ("ΔF MM", a_df["mm"], n_df["mm"], "{:,.0f}"),
            ("ΔF C44", a_df["c44"], n_df["c44"], "{:,.0f}"),
            ("YLL", a_y, n_y, "{:,.0f}"),
            ("€ Mio", a_e / 1e6, n_e / 1e6, "{:,.0f}")):
        z.append(f"| {name} | {fmt.format(alt)} | **{fmt.format(neu)}** | "
                 f"{neu/alt-1:+.1%} |".replace(",", "."))
    z.append("")
    z.append(f"Nicht zugeordnet: {ohne_pop} Gemeindepunkte ohne Zensus-Bevölkerung, "
             f"{ohne_raster} ohne Rasterwert (beide gehen nicht in die Gewichtung ein).")
    z.append("\n" + EINGANGSDATEN.rstrip("\n"))

    out = "\n".join(z)
    with open(os.path.join(DATA, "ssd_povw.md"), "w", encoding="utf-8") as fh:
        fh.write(out)
    print(out)


if __name__ == "__main__":
    main()
