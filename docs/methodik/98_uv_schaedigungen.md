# Methodik-Bericht #98 — UV-bedingte Gesundheitsschädigungen (insbesondere Hautkrebs)

Status: **Rev. 1 (Erstaufschlag im §4-Format; Migration des #98-Anteils von M0 Rev. 5 +
Abarbeitung der #98-Befunde der Gegenprüfung) — im Review** · 30.08.2026 ·
Instruktionsquelle: `docs/AUFGABE_METHODIK_SCHADENSRECHNUNG.md` (v2) · Umsetzungsgrundlage:
**Ansatz 98-A** (amtliche Inzidenz + Trend-Attribution über BAF; Entscheidungslog Nr. 1)
· Familie: **K1-Gesundheit bottom-up** (Prototyp #95; §2.6 — kein erneuter Drei-Ansätze-Vergleich)

> **Revisionsstand.** Rev. 1 = Migration des #98-Anteils von M0 Rev. 5
> (`docs/render/METHODIK_M0_GESUNDHEIT.html`, Kap. 4) in das §4-Format **plus** Abarbeitung
> der #98-relevanten Befunde der Gegenprüfung (GP-9/-10, 15, 16, 22, 26/34, 28–32, 37, 41,
> 43); Status je Befund in `reviews/BEFUNDE_98.md`. Diese Markdown-Datei ist die Quelle für
> #98 (§2.7). Alle Ermessensentscheidungen im **Entscheidungslog** (Ende der Datei).
> Anlagen: `backend/scripts/kalibrierung/dwd_ssd_trend.py` +
> `backend/data/kalibrierung/ssd_trend_region.csv` und
> `backend/data/kalibrierung/kid2025_ablesewerte.csv` (Roh-Ablesewerte §3.3).

## 1 Wirkungskette & Knoten-Bilanz (§2.1)

Kette laut Arbeitsmappe (Sheet „Klimawirkungsketten" Z409, Knoten **W186**; Konfidenz
**hoch** — einziger direkter Hazard-Pfeil E20, eindeutige Container-Zuordnung).
Rollen/Kanten: Sheet „Schadensbaum-Netzwerkliste" Z99 (Id 98): **Buchungsobjekt — Ebene B**,
Handlungserfordernis **sehr dringend**; keine Ein-/Ausgangskanten auf Risikoebene.
KWRA-Charakteristik: extensiv betrachtet (keine eigenen KWRA-Indikatoren); der Klimapfad
läuft laut KWRA wesentlich über das **Verhalten** („verhaltensbedingt steigende Exposition
in längeren, sonnigeren Warmphasen" — Monetarisierung ID 98, Blattzeile 103).

### Knoten-Bilanz

| Knoten | Name | rechnet in | Wo (Formel/Ebene) | falls inaktiv: Begründung |
|---|---|---|---|---|
| E20 | UV-Strahlung (direkter Hazard) | Schicht A + B | \(\Delta\text{Dosis}\) über SSD-Normalperiodenvergleich × \(k_{\text{UV}}\) × \(a_{\text{attr}}\) (§3.2); Ebene UV_RADIATION/SSD (neu) | — |
| S154 | Freizeitverhalten | **Sensitivitätsband** (Default 1) | \(v_{\text{verh}}\)-Band +0,25…+0,60 je Komforttag (§3.5) | keine quantifizierte Effektgröße „Mehr-Exposition je Komforttag" für DE [36]; US-Zeitverwendungs-Evidenz nur Band (§3.2: unbelegte Modulatoren Default 1; Log 11) |
| S155 | Gefahrenbewusstsein | Maßnahmen-Hebel (**qualitativ**) | UV-Schutz im öffentlichen Raum / UV-Index-Kommunikation (§5) | Basiswert: Nutzen-Kosten-Verhältnisse sind keine Effektgröße auf Dosis/Inzidenz (GP-26/34; Log 12) |
| S158 | Monitoring / Frühwarnsysteme | Maßnahmen-Hebel (**qualitativ**; Kostenwirkung bereits im Basiswert) | Früherkennungs-Förderung (SCS-Teilnahme); §5 — Befund 203 | Basiswert setzt bereits SCS-Kosten für alle Fälle an — additiver Hebel hätte kein Headroom; quantifizierbar erst mit Detektionsmix-Parameter (Ersetzungspfad) |
| R35 | Vorkommen von Bevölkerung | Schicht A + B | \(\text{pop}_a\) (Zensus 2022; Ebene u20 aus #96 mitgenutzt) | — |
| R36 | Vorkommen von Gesundheitsinfrastruktur | Schicht A (Screening) | Ebene HEALTHCARE_ACCESS im Index (§3.7) | Basiswert Default 1: keine Evidenz für einen Distanz-/Kapazitätseffekt auf Hautkrebs-Outcomes; Zugangseffekte stecken im SCS-Hebel (§3.2; Log 13) |
| — | Berufliche Außenexposition (**kein Knoten der W186-Kette**) | **Sensitivitätsband** (Basiswert-Default 1) | \(r_{\text{out}}\) (nur SCC-Anteil; §3.5); Ebene Außenbeschäftigten-Anteil **neu anzulegen** (INKAR/SVB-Branchen) | GP-9: Kettentreue („nicht mehr, nicht weniger") — Aufnahme in den Basiswert erforderte eine Fortschreibung der Arbeitsmappe + Abgleich-Protokoll-Punkt (dokumentierter Ersetzungsweg); Evidenz (BK 5103, Meta-OR 1,77 [43]) und \(\bar q_{\text{out}}\)-Herleitung liegen vollständig vor (Log 10) |

### Weitergaben (zweispaltig; Quelle: Netzwerkliste + Abgleich-Protokoll)

| Output-Kanten (Abgleich-Protokoll) | Konto-Ausschlüsse / verwandte Buchungen (K1-Definition) |
|---|---|
| **keine** — die Netzwerkliste führt für #98 keine Output-Kanten, das Abgleich-Protokoll keinen Punkt zu #98 (einzige K1-weite Fortschreibung: **P52** Mortalitätsbewertung YLL × VOLY, gilt für alle K1-Buchungsobjekte) | **R9-Partition** (Monetarisierung ID 98: „Doppelzählung mit anderen K1-Ursachen"): jeder Fall zählt genau einmal unter der Ursache UV; **Produktionsausfälle → K2** (K1-Definition), **Systemvorhaltung → K8 via ID 102** (K1-Definition; keine Kante von #98) |

### Konto-Einbettung

- **Konto:** K1 Gesundheit, **Ursache: UV** (R9-Partition); Bausteine **K1-Mortalität +
  K1-Morbidität** (Netzwerkliste Z99; Monetarisierung Blattzeile 103: „Zusätzliche
  Erkrankungsfälle × Behandlungskosten + Mortalitätsanteil als YLL × VOLY [MK 4.0;
  Fortschreibung P52; VSL nur Sensitivität]").
- **Anzuwendende Rechenregeln:** R9 (laut Monetarisierung, Spalte „Regeln").
- **Nur K1 aktiv (M0):** bewusste **Untergrenze** („konservativ" = *unterschätzend* wie in
  #95/#96); Augenschäden (Katarakt — im Monetarisierungs-Gegenstand genannt) und
  Produktivität (K2, ab M3) nicht enthalten — dokumentierte Untererfassung (§6).

## 2 Evidenz-Register (§2.2)

Risikoübergreifend wiederverwendbare Zeilen zusätzlich in `docs/evidenz/register.md`.
Nur Zeilen mit Entscheidung **Basiswert** kommen in den Formeln (§3) vor.

| Register-ID | Knoten → Outcome | Effektgröße | Studientyp | Quelle | Übertragbarkeit | Datenlage je Zelle | Entscheidung | E-Regel |
|---|---|---|---|---|---|---|---|---|
| 98-E20-01 | E20 SSD-Änderung (Klimanormalperioden) | DE +7,82 % (1.544,0 → 1.664,8 h); N/M/S +6,26/+8,42/+7,53 % | amtliche Messreihe, eigene Auswertung (Skript [69]) | DWD-CDC Gebietsmittel [33]; `ssd_trend_region.csv` [69] | DE-weit; Fenster 1961–90 vs. 1991–2020 (GP-Befund 37) | DWD sunshine_duration 1 km (Ebene **neu anzulegen**) | **Basiswert** | Log 4 |
| 98-E20-02 | SSD → erythemwirksame Dosis | \(k_{\text{UV}}\) = 0,84 (Band 0,4–1,0) = Dosistrend 4,9 %/Dek. [31] ÷ SSD-Trend NRW 1997–2022 5,81 %/Dek. [69] | publizierte Messreihe × eigene Trendrechnung (konsistentes Fenster/Gebiet) | Lorenz 2024 [31] (primär verifiziert); [69] | Dortmund/NRW → DE (Band); M0-Paarung 0,43 (Stations-SSD „11,3", unbelegt) = untere Bandstütze | berechnet | **Basiswert** | Log 2 |
| 98-E20-03 | Klimawandel → Anteil am SSD-/Dosistrend | \(a_{\text{attr,UV}}\) = 0,75 (Band 0,5–1,0) — **gekennzeichnete Abschätzung** | Einordnung (Lorenz: „starker Einfluss der Bewölkungsabnahme"; Aerosol-„Brightening" spricht gegen 1,0) | [31]; GP-Befund 15 | Attributionstudie für DE-UV existiert nicht (Lücke, Ersetzungspfad) | Literatur-Band | **Basiswert** | Log 3 |
| 98-E20-04 | Dosis → Inzidenz (Verstärkungsfaktoren) | BAF: SCC 2,5 ± 0,7 · BCC 1,4 ± 0,4 · MM 0,6 ± 0,4 (%-Inzidenz je +1 % Dosis) | biologisch-epidemiologisches Standardmodell; unabhängig bestätigt | Slaper 1996 [29]; RIVM 2023 [29]; Madronich 2021 [30] | international etabliert (Montreal-Protokoll-Folgenabschätzung) | — | **Basiswert** | Log 1 |
| 98-R35-01 | R35 Bevölkerung → Baseline-Fälle | \(I_{e,a}\) je Band (Ablesekette §3.3 aus KID-2025-Abb. 3.13.2/3.14.3, normiert auf amtliche Rohraten 2023) | amtliche Krebsregisterdaten (Abbildungs-Ablesung, gekennzeichnet) | ZfKD KID 2025, Kap. 3.13/3.14 [27] | DE 2021–2023; Ablese-Validierung MM −2,2 %/C44 +0,1 % vor Normierung (Befunde 204/212) | Zensus-Altersbänder (+ u20 aus #96) | **Basiswert** | Log 5 |
| 98-K1-01 | Fall → Erstjahres-Behandlungskosten | MM 5.326 (SCS-detektiert) / 9.038 €₍₂₀₁₅₎ (nicht-SCS); NMSC 4.660/5.890 — Basis = SCS-Werte ⇒ 6.724/5.883 €₂₀₂₄ | Krankenkassen-Routinedaten (AOK; DiD-Design) | Speckemeier 2022 [34] (Volltext-Abstract primär verifiziert; Kohorte Diagnose 2014/2015) | DE; **Proxy**: Gesamt- statt inkrementelle Kosten, nur Erstjahr (§3.4) | national | **Basiswert** (untere Stütze) + Band | Log 7 |
| 98-K1-02 | MM/C44 → Letalität, Restlebenserwartung | \(\lambda_{\text{MM}}\) = 0,1155 · \(\lambda_{\text{C44}}\) = 0,00549 (2023); \(\bar L_{\text{MM}}\) = 10,58 · \(\bar L_{\text{C44}}\) = 5,30 J. | amtliche Statistik + Approximationen (**gekennzeichnet**: Perioden- bzw. Median-Approximation, GP-Befund 43) | ZfKD 2023 [27]; Sterbetafel 2022/2024 [48] | DE | national | **Basiswert** | Log 8 |
| 98-S154-01 | S154 Verhalten → Mehr-Exposition je Komforttag | \(s\) ≈ +0,45 (Kernband +0,25…+0,60); Hitzetage > 30 °C: −5…−13 % Aktivität | Zeitverwendungs-/Dosimetrie-Evidenz (US) | Graff Zivin & Neidell 2014 [57]; [58,59] | US-Übertragbarkeit begrenzt; Ambient-Anteil steckt bereits in ΔDosis (Doppelzählungsschutz) | Zell-Komforttage (berechenbar) | **Sensitivitätsband** (Default 1) | Log 11 |
| 98-S155-01 | S155 UV-Schutzprogramme → Inzidenz | Nutzen-Kosten 2,2–8,7 : 1 (AUS/USA/EU) — **keine** Dosis-/Inzidenz-Effektgröße | Programm-Evaluationen | Shih/Doran/Collins [37] | keine deutsche Studie [37] | kommunal | **Maßnahmen-Hebel (qualitativ)** | Log 12 |
| 98-S158-01 | S158 Früherkennung (SCS) → Fallkosten/Letalität | −18,8 % [8,4–23,1] Erstjahreskosten je MM-Fall bei SCS-Detektion (belegt das Sparpotenzial); Letalitätswirkung nicht angesetzt | quasi-experimentell (DiD, Routinedaten) | Speckemeier 2022 [34] | DE; **Wirkung im Basiswert enthalten** (Basis-\(c_e\) = SCS-Werte; Befund 203) | kommunal (Teilnahmequoten) | **Maßnahmen-Hebel (qualitativ)** | Log 12 |
| 98-OUT-01 | Berufliche Außenexposition → SCC | OR 1,77 [1,37–2,30] (Fall-Kontroll-Pool; Kohorten 1,68 [1,08–2,63]); \(\bar q_{\text{out}}\) = 0,070 (VGR 2023: [572 + 2.643] / 45.909 Tsd. [70]) | Meta-Analyse (BK-5103-Grundlage) | Schmitt 2011 [43] (Abstract primär verifiziert); Destatis VGR [70] | DE; **kein Knoten der W186-Kette** (GP-9) | INKAR/SVB-Branchenanteile (Ebene neu; Proxy) | **Sensitivitätsband** (Basiswert-Default 1) | Log 10 |
| 98-R36-01 | R36 Gesundheitsinfrastruktur → Outcome | keine Evidenz für Distanz-/Kapazitätseffekt auf Hautkrebs-Inzidenz/-Letalität | — | — | Zugangseffekt steckt im SCS-Hebel | HEALTHCARE_ACCESS (Schicht A) | **bewusst inaktiv** (Default 1) | Log 13 |

## 3 Modell (§2.3) — Ansatz 98-A, Schicht B

**Native Ergebnisgröße (§3.6, deklariert): verlorene Lebensjahre (YLL) je Jahr** (GP-Befund
28). Teil-Ausweise unter der KWRA-Klammer: klimaattribuierte Zusatzfälle \(\Delta F_e\)
(je Entität), €.

**Gemeinsamer Preisstand aller Kostensätze dieses Berichts: €2024**; Umrechnungsfaktoren je
Satz in der Zeichentabelle (Destatis-VPI, 2020 = 100: 2015 = 94,5 · 2024 = 119,3 [19]).

### 3.1 Entitäten (§-Konvention)

\(e \in \{\text{MM}, \text{C44}\}\): malignes Melanom (ICD-10 C43) und nicht-melanotischer
Hautkrebs (C44). Innerhalb C44 wirken BAF und Außenberufs-Evidenz entitätsspezifisch
(SCC vs. BCC). **Split-Quellen im Widerspruch (§3.8, benannt — Befund 202):** das
wertetragende KID-2025-C44-Kapitel [27] gibt für 2021–2023 „knapp drei Viertel Basaliome …
etwa ein Viertel Plattenepithelkarzinome" an (\(w_{\text{SCC}}\) ≈ 0,25); die
2015er-BfS-Fallzahlen (BCC 158.840 · SCC 98.950, Sekundärangabe in [27]/[36]) ergäben
0,384. **Basiswert = 0,25** (aktuelle Registerdaten der Primärquelle), Band 0,25–0,50
(obere Stütze: BfS-2015-Split; mögliche Ursache der Differenz: Untererfassung/Meldepraxis
von SCC-Mehrfachtumoren — Volltext-Verifikation [36] als Ersetzungspfad). Der Split wird
**altersinvariant** angewendet (GP-Befund 41 — dokumentierte Annahme; Richtung: SCC-Anteil
steigt real mit dem Alter ⇒ Unterschätzung des Zusatzes in alten Kommunen):

$$ \text{BAF}_{\text{C44}} \;=\; 0{,}75 \cdot 1{,}4 + 0{,}25 \cdot 2{,}5 \;=\; 1{,}675 \qquad (\text{Band } 1{,}675\text{–}1{,}95 \text{ über } w_{\text{SCC}} = 0{,}25\text{–}0{,}50). $$

### 3.2 Klimasignal: Dosisänderung (Anker `#delta-dosis`, `#k-uv`)

$$ \Delta\text{Dosis}_{\text{Zelle}} \;=\; \frac{\text{SSD}_{\text{Zelle}}^{\,1991\text{–}2020} - \text{SSD}_{\text{Zelle}}^{\,1961\text{–}1990}}{\text{SSD}_{\text{Zelle}}^{\,1961\text{–}1990}} \cdot k_{\text{UV}} \cdot a_{\text{attr,UV}} $$

- **Mittelungsfenster = Klimanormalperioden je Zelle** (GP-Befund 37; Einzeljahre sind
  wegen der SSD-Variabilität ungeeignet — Rekordjahre ≈ 2.015–2.024 h [33]). Referenzwerte
  (Gebietsmittel, Skript [69]): DE 1.544,0 → 1.664,8 h = **+7,82 %**; Nord +6,26 % ·
  Mitte +8,42 % · Süd +7,53 %. Datenverfügbarkeit des 1-km-Rasters ab 1961: bei
  Integration verifizieren; bis dahin Bundesland-Gebietsmittel als Zell-Fallback
  (dokumentiert).
- **\(k_{\text{UV}}\) = 0,84 (Band 0,4–1,0)** — GP-Befund-10-Auflösung (Log 2): Die
  M0-Kette „4,9/11,3 = 0,43" beruhte auf einem **unbelegten** Dortmunder Stations-SSD-Trend.
  Belegt sind: Dosistrend **+4,9 %/Dekade** (Dortmund 1997–2022, signifikant; Lorenz 2024
  [31], Abstract primär verifiziert) und — eigene Messung im **selben Fenster** und
  **derselben Datenfamilie**, die das Produkt verwendet (DWD-Gebietsmittel) — SSD-Trend
  NRW 1997–2022 = **+5,81 %/Dekade** [69]:
  \(k_{\text{UV}} = 4{,}9 / 5{,}81 = 0{,}84\). Diese Paarung ist konsistent, weil das
  Modell \(k_{\text{UV}}\) auf **Raster-/Gebietsmittel-SSD** anwendet — nicht auf
  Stationswerte. Band: untere Stütze 0,43 (M0-Stations-Paarung, falls der
  11,3-%-Stationstrend im Volltext belegt wird — Ersetzungspfad), obere Stütze 1,0
  (Lorenz: Globalstrahlung ≈ parallel zur Dosis). Plausibilisierung: implizite
  Dosisänderung DE = 7,82 % × 0,84 ≈ 6,6 % über den Normalperiodenversatz ≈ 2,2 %/Dekade —
  innerhalb des Satelliten-Bands +1,2–3,6 %/Dekade [32] und unter dem Stationswert 4,9 ✓.
- **\(a_{\text{attr,UV}}\) = 0,75 (Band 0,5–1,0)** — GP-Befund-15-Auflösung (Log 3):
  Attributionsfaktor analog zur #96-Logik (dort 0,50, gemessen [9]); für UV existiert
  keine Attributionsstudie — **gekennzeichnete Abschätzung**: Lorenz nennt als
  Trendursache „v. a. Bewölkungsabnahme" (klimasystemische Größe → hoher Wert), das
  Aerosol-„Brightening" seit den 1980ern ist anthropogen, aber keine Klimawirkung im
  KWRA-Sinn (→ < 1,0). Zentral 0,75, beide Grenzen im Band; Ersetzungspfad:
  Wolken-/Aerosol-Zerlegung aus Reanalysen.
- Resultierende \(\Delta\text{Dosis}\) (Basiswerte): **DE 4,95 %** · Nord 3,96 % ·
  Mitte 5,33 % · Süd 4,76 %.

```python test: beispiel_98_klimasignal
# k_UV = Dosistrend / NRW-SSD-Trend (gleiche Fenster/Datenfamilie); Delta-Dosis je Region
k_uv = 4.9 / 5.81
assert abs(k_uv - 0.843) < 0.001
dssd = {"nord": 6.26, "mitte": 8.42, "sued": 7.53, "de": 7.82}
soll = {"nord": 3.96, "mitte": 5.33, "sued": 4.76, "de": 4.95}
for r, v in dssd.items():
    assert abs(v/100 * k_uv * 0.75 * 100 - soll[r]) < 0.01
# Plausibilisierung: implizite Dosisaenderung im Satelliten-Rahmen (1,2-3,6 %/Dekade x ~3 Dekaden Versatz)
assert 1.2 * 3 * 0.5 <= 7.82 * k_uv <= 3.6 * 3   # 6,6 % zwischen 1,8 und 10,8
```

### 3.3 Baseline-Fälle: altersspezifische Inzidenz (Anker `#i-raten`)

$$ F_{e,\text{Zelle}} \;=\; c_{\text{kal},e} \cdot \sum_a \text{pop}_a \cdot \frac{I_{e,a}}{100\,000} $$

**Ablesekette \(I_{e,a}\)** (Log 5; §3.9 „Abgeschätzt" mit Messanker — dieselbe Ablese-Kette
wie die #95-ERF-Steigungen aus Winklmayr-Abb. 3): Die altersspezifischen
Neuerkrankungsraten sind in KID 2025 nur als Abbildungen publiziert (Abb. 3.13.2 C43,
Abb. 3.14.3 C44; je 100.000, 2021–2023, nach Geschlecht); die ZfKD-Datenbankwerte sind
nicht keyless abrufbar (dokumentierte Datenlücke; Ersetzungspfad: ZfKD-Abfrage vor
Integration). **Roh-Ablesewerte je 5-Jahres-Gruppe und Geschlecht** (Ablese-Toleranz
±15 %, gitterlinien-gestützt): vollständig in der Anlage
`backend/data/kalibrierung/kid2025_ablesewerte.csv` (Befund 204); Auszug (F/M je 100.000):
C43: 20–24: 5/2 · 40–44: 25/16 · 60–64: 42/52 · 75–79: 66/120 · 85+: 61/140;
C44: 40–44: 90/55 · 60–64: 315/350 · 75–79: 865/1.420 · 85+: 1.100/2.190.

Aggregation auf die Produktbänder mit **geschlechtsspezifischen Bevölkerungsgewichten**
(Bevölkerung 31.12.2023 nach Altersjahren und Geschlecht, Tab. 12411-06 [48] — ersetzt die
frühere 50/50-Annahme, Befund 204). **Roh-Bandraten** (unnormiert):

| \(I_{e,a}^{\text{roh}}\) je 100.000 | u20 | 20–64 | 65–74 | 75–84 | 85+ | gewichtete Roh-Rate vs. amtliche Rohrate 2023 |
|---|---|---|---|---|---|---|
| MM (C43) | 0,5 | 24,7 | 64,0 | 94,9 | 88,5 | 32,16 vs. 32,87 (**−2,2 %**) |
| C44 | 2,0 | 125,9 | 617,6 | 1.267,2 | 1.479,5 | 291,36 vs. 290,96 (**+0,1 %**) |

**Ablesegrenze (Befund 212, gekennzeichnet):** Für u20 (beide Entitäten) und C44 20–29
liegen die Balken unter der Ablesegrenze der Abbildungen (< ≈ 15 je 100.000 bei
Achse 0–2.500); angesetzt sind **0,5** (MM u20, Band 0–5), **2,0** (C44 u20, Band 0–5)
und **5** (C44 20–24/25–29, Band 0–15) — gekennzeichnete Abschätzungen mit < 0,3 %
Wirkung auf die Bundes-Baseline; die Bandmittelung läuft über die **volle**
Band-Bevölkerung (20–64 inkl. der 20–29-Jährigen).

**Normierungsskalare (= Kalibrierung, §3.4-konform genau ein Skalar je Entität; wirken in
der Formel — die Tabellenwerte sind Rohwerte, Befund 201):**
\(c_{\text{kal,MM}}\) = 27.430/26.837 = **1,022** · \(c_{\text{kal,C44}}\) =
242.820/243.158 = **0,999** — damit reproduziert die Bundes-Baseline die ZfKD-Fallzahlen
2023 exakt. Ablese-Toleranz (vorab fixiert): ±15 % vor Normierung — **bestanden**.

```python test: beispiel_98_baseline_normierung
# Roh-Bandraten x c_kal reproduzieren die amtlichen Fallzahlen 2023 (Befund 201)
pop = {"u20": 15_583_456, "20-64": 49_163_992, "65-74": 9_569_640,
       "75-84": 6_294_744, "85+": 2_844_213}
i_mm  = {"u20": 0.5, "20-64": 24.7, "65-74": 64.0, "75-84": 94.9, "85+": 88.5}
i_c44 = {"u20": 2.0, "20-64": 125.9, "65-74": 617.6, "75-84": 1267.2, "85+": 1479.5}
mm_roh  = sum(pop[b] * i_mm[b]  / 1e5 for b in pop)
c44_roh = sum(pop[b] * i_c44[b] / 1e5 for b in pop)
assert abs(mm_roh - 26_837) < 60 and abs(c44_roh - 243_158) < 600
assert abs(27_430 / mm_roh - 1.022) < 0.003     # c_kal,MM
assert abs(242_820 / c44_roh - 0.999) < 0.003   # c_kal,C44 (Befund 212)
assert abs(mm_roh * 1.022 - 27_430) / 27_430 < 0.005
assert abs(c44_roh * 0.999 - 242_820) / 242_820 < 0.005
```

### 3.4 Klimaattribuierter Zusatz, Mortalität, Monetarisierung

$$ \Delta F_{e,\text{Zelle}} \;=\; F_{e,\text{Zelle}} \cdot \text{BAF}_e \cdot \Delta\text{Dosis}_{\text{Zelle}}, \qquad \text{YLL}_{\text{Zelle}} = \sum_e \Delta F_{e,\text{Zelle}} \cdot \lambda_e \cdot \bar L_e $$

**Gekennzeichnete Approximation (Befund 210, analog GP-Befund 43):** der relative Exzess
wird auf die bereits dosiserhöhte 2023er-Baseline angewendet; der attributable Anteil wäre
exakt \(\text{BAF} \cdot \Delta D / (1 + \text{BAF} \cdot \Delta D)\) — Richtung:
Überschätzung um ≈ +3 % (MM) bzw. ≈ +8 % (C44), innerhalb der Bänder.

$$ \text{€}_{\text{Zelle}} \;=\; \sum_e \Delta F_{e,\text{Zelle}} \cdot c_e \;+\; \text{YLL}_{\text{Zelle}} \cdot \text{VOLY}, \qquad \text{Kommune} = \sum_{\text{Zellen}} $$

- **\(\lambda_e\)** = Sterbefälle ÷ Neuerkrankungen 2023 [27]: MM 3.169/27.430 = **0,1155**;
  C44 1.332/242.820 = **0,00549** — **Perioden-Approximation, gekennzeichnet** (GP-Befund
  43): bei steigender Inzidenz keine Kohorten-Letalität; Richtung: Überschätzung des
  Mortalitätsanteils.
- **\(\bar L_e\)** = \(e(\text{medianes Sterbealter})\), sterbefallgewichtet über die
  Geschlechter [27,48]: MM (1.318·10,92 + 1.851·10,33)/3.169 = **10,58 J.**; C44
  (541·5,04 + 791·5,47)/1.332 = **5,30 J.** — **Median-Approximation, gekennzeichnet**
  (GP-Befund 43): bei rechtsschiefer Sterbealter-Verteilung leicht überschätzend.
- **\(c_e\)** (Log 7; Register 98-K1-01): Basis = Erstjahreskosten **SCS-detektierter**
  Fälle (Speckemeier [34], Kohorte 2014/2015, Preisstand-Annahme 2015):
  MM 5.326 × 119,3/94,5 = **6.724 €₂₀₂₄** (Band bis 11.410 = nicht-SCS-detektiert);
  C44 4.660 ⇒ **5.883 €₂₀₂₄** (Band bis 7.436). **Proxy-Kennzeichnung** (§3.1) mit
  Richtungsdiskussion: *überschätzend* — Gesamt- statt inkrementelle Kosten (enthält
  Grundversorgung der überwiegend alten Patienten); *unterschätzend* — nur Erstjahr
  (Folgejahre, Metastasen-Therapien fehlen), SCS-Werte als untere Detektionsweg-Stütze.
  Die Basiswert-Wahl folgt der Untergrenzen-Zusage (#95-Befund-62-Lehre).
- **VOLY = 160.800 €₂₀₂₄** (MK 4.0/P52; Kette in #95 §3.5 [19]); VSL nur Sensitivität.
- **Sensitivitätsband \(r_{\text{out}}\)** (nicht im Basiswert; Log 10; GP-Befund 9;
  Formel-Präzisierung Befund 206): der Außenberufs-Modifikator wirkt auf den
  **SCC-Anteil am C44-Zusatz** \(w^Z = w_{\text{SCC}} \cdot 2{,}5 / \text{BAF}_{\text{C44}}
  = 0{,}25 \cdot 2{,}5 / 1{,}675 = 0{,}373\):

  $$ r_{\text{out}} \;=\; (1 - w^Z) + w^Z \cdot \frac{1 + q_{\text{out}} (\text{OR}-1)}{1 + \bar q_{\text{out}} (\text{OR}-1)} $$

  OR = 1,77 [1,37–2,30] [43], \(\bar q_{\text{out}}\) = **0,070** =
  (572 + 2.643)/45.909 Tsd. Erwerbstätige 2023 (Land-/Forstwirtschaft/Fischerei +
  Baugewerbe, VGR [70]; **Proxy**: nicht alle Branchenbeschäftigten arbeiten im Freien,
  Außenberufe anderer Branchen fehlen — beide Richtungen). Mittelwertzentriert
  (Bundesmittel = 1) — verteilungsneutral zur Bundessumme; Beispiel Bau-/Agrar-Kommune
  \(q_{\text{out}}\) = 0,14: **+1,9 %** auf den C44-Zusatz.
- **Sensitivitätsband \(v_{\text{verh}}\)** (Default 1; Log 11; Register 98-S154-01;
  Herleitung migriert, Befund 205): definiert als **Tages-Multiplikator der persönlichen
  Dosis an Komforttagen**, multiplikativ auf \(\Delta\text{Dosis}\) der betroffenen Tage.
  Kette: Outdoor-Freizeit +1,2 min/°C (ATUS, n = 42.280; Basis 44 min/Tag [57]); ein
  Komforttag (ΔT ≈ +10 °C) ⇒ +12 min = **+27 %** Außenzeit; Zeit-im-Freien erklärt die
  persönliche Dosis nahezu proportional (R² 0,75–0,79 [59]); Kleidungskomponente +15 %
  (0–35 %, nur Richtung [59]) ⇒ Tages-Mehr-Dosis \(s\) ≈ **+45 %** (Kernband +25…+60 %;
  Hitzetage > 30 °C kehren das Vorzeichen um: −5…−13 % Aktivität [58]). Die
  **Jahreswirkung** hängt vom Komforttag-Anteil ab (Szenario-Stellgröße, keine Zellgröße
  in M0) — deshalb Default 1 und Band als Tageswert [1,25–1,60]; nicht im Basiswert
  (US-Übertragbarkeit; Ambient-Anteil bereits in ΔDosis — Doppelzählungsschutz).

```python test: beispiel_98_lambda_l_kosten
# Letalitaet, Restlebenserwartung, Kostenketten (Quellenwerte 2023 [27,48,34,19])
lam_mm, lam_c44 = 3169/27430, 1332/242820
assert abs(lam_mm - 0.1155) < 0.0003 and abs(lam_c44 - 0.00549) < 0.00002
l_mm = (1318*10.92 + 1851*10.33) / 3169
l_c44 = (541*5.04 + 791*5.47) / 1332
assert abs(l_mm - 10.58) < 0.005 and abs(l_c44 - 5.30) < 0.01
assert abs(5326 * 119.3/94.5 - 6724) < 2 and abs(4660 * 119.3/94.5 - 5883) < 2
assert abs(9038 * 119.3/94.5 - 11410) < 2 and abs(5890 * 119.3/94.5 - 7436) < 2
assert abs((572 + 2643)/45909 - 0.070) < 0.0005
# BAF_C44 aus KID-2025-Split (Befund 202); BfS-2015-Split als obere Bandstuetze
assert abs(0.75*1.4 + 0.25*2.5 - 1.675) < 0.001
assert abs(0.50*1.4 + 0.50*2.5 - 1.95) < 0.001
# r_out-Beispiel (Befund 206): SCC-Anteil am ZUSATZ w_Z = w_scc*2,5/BAF_C44
w_z = 0.25 * 2.5 / 1.675
assert abs(w_z - 0.373) < 0.001
m = (1 + 0.14*(1.77-1)) / (1 + 0.070*(1.77-1))
r = (1 - w_z) + w_z * m
assert abs(r - 1.019) < 0.001
```

```python test: beispiel_98_bundessumme
# Bundessummen: Baseline amtlich (ZfKD 2023), Delta-Dosis DE 4,95 %
dd = 0.0782 * (4.9/5.81) * 0.75
d_mm  = 27_430  * 0.6   * dd
d_c44 = 242_820 * 1.675 * dd
yll = d_mm * 0.1155 * 10.58 + d_c44 * (1332/242820) * 5.30
euro = d_mm * 6724 + d_c44 * 5883 + yll * 160_800
assert abs(d_mm - 814) < 3 and abs(d_c44 - 20_118) < 80
assert abs(yll - 1580) < 8
assert abs(euro / 1e6 - 378) < 3
# Sanity: Behandlungsanteil klein gegen KKR C43/C44 (1.823 Mio EUR 2023)
assert (d_mm * 6724 + d_c44 * 5883) / 1.823e9 < 0.10
```

```python test: beispiel_98_beispielzelle
# 1.000 EW im Bundesmix, Region Mitte (Delta-Dosis 5,33 %), P-Defaults
f_mm, f_c44 = 0.3287, 2.9096            # amtliche Rohraten je 1.000 EW (2023)
dd_m = 0.0533
d_mm  = f_mm  * 0.6   * dd_m
d_c44 = f_c44 * 1.675 * dd_m
yll = d_mm * 0.1155 * 10.58 + d_c44 * (1332/242820) * 5.30
euro = d_mm * 6724 + d_c44 * 5883 + yll * 160_800
assert abs(d_mm - 0.0105) < 0.0002
assert abs(d_c44 - 0.2598) < 0.003
assert abs(euro - 4880) < 60               # ~4.900 EUR je 1.000 EW und Jahr
```

### 3.5 Zeichentabelle (alphabetisch; §3.2-Form)

| Zeichen | Name | Einheit | Wert / Herkunft |
|---|---|---|---|
| \(a\) | Altersband u20 · 20–64 · 65–74 · 75–84 · 85+ (Ebenen wie #96 §3.2) | — | Zensus-Altersbänder + Ebene u20 |
| \(a_{\text{attr,UV}}\) | klimaattribuierter Anteil des SSD-/Dosistrends | — | **0,75** (0,5–1,0) — gekennzeichnete Abschätzung §3.2; register:98-E20-03 |
| \(\text{BAF}_e\) | biologischer Verstärkungsfaktor (%-Inzidenz je +1 % Dosis) | — | MM **0,6** (±0,4) · C44 **1,675** (1,675–1,95; §3.1) [29,30]; register:98-E20-04 |
| \(c_e\) | Erstjahres-Behandlungskosten je Fall (**Proxy**, §3.4) | €₂₀₂₄ | MM **6.724** (Band –11.410) · C44 **5.883** (–7.436) = [34]-Werte × 119,3/94,5 [19]; register:98-K1-01; herleitung:#c-e |
| \(c_{\text{kal},e}\) | Normierungsskalar der Ablesekette (ein Skalar je Entität; wirkt in der §3.3-Formel auf die Roh-Bandraten) | — | MM **1,022** · C44 **0,999**; herleitung:#i-raten |
| \(\Delta\text{Dosis}_{\text{Zelle}}\) | relative klimaattribuierte Dosisänderung | — | SSD-Normalperioden-Δ × \(k_{\text{UV}}\) × \(a_{\text{attr,UV}}\); DE 4,95 % (§3.2); berechnet |
| \(\Delta F_{e,\text{Zelle}}\) | klimaattribuierte Zusatzfälle (Teil-Ausweis) | 1/Jahr | berechnet |
| \(\text{€}_{\text{Zelle}}\) | bewerteter Schaden K1 (Ursache UV) — Teil-Ausweis | €₂₀₂₄/Jahr | Ergebnis (§3.4) |
| \(F_{e,\text{Zelle}}\) | Baseline-Neuerkrankungen der Zelle | 1/Jahr | berechnet (§3.3) |
| \(I_{e,a}^{\text{roh}}\) | Roh-Neuerkrankungsrate je Entität und Band (Ablesekette; Anlage-CSV) | 1/100.000·a | Tabelle §3.3 [27,48]; register:98-R35-01; herleitung:#i-raten |
| \(k_{\text{UV}}\) | Übersetzung SSD-Trend → erythemwirksame Dosis | — | **0,84** (0,4–1,0) = 4,9/5,81 (§3.2) [31,69]; register:98-E20-02; herleitung:#k-uv |
| \(\lambda_e\) | Letalitätsanteil (Perioden-Approximation, gekennzeichnet) | — | MM **0,1155** · C44 **0,00549** [27]; register:98-K1-02 |
| \(\bar L_e\) | verlorene Lebensjahre je Sterbefall (Median-Approximation, gekennzeichnet) | Jahre | MM **10,58** · C44 **5,30** [27,48]; register:98-K1-02 |
| \(\text{OR}_{\text{out}},\ q_{\text{out}},\ \bar q_{\text{out}},\ r_{\text{out}},\ w^Z\) | Außenberufs-Sensitivität (auf den SCC-Anteil am Zusatz \(w^Z\) = 0,373; **nicht im Basiswert**, §3.4) | — | OR **1,77** [1,37–2,30] [43]; \(\bar q_{\text{out}}\) = **0,070** [70]; register:98-OUT-01; herleitung:#q-out |
| \(\text{pop}_a\) | Bevölkerung der Zelle je Band | Personen | Zensus 2022, 100 m (+ u20); register:98-R35-01 |
| \(\text{SSD}\) | Sonnenscheindauer (Normalperioden-Mittel je Zelle) — Kartenebene **neu** | h/Jahr | DWD-CDC sunshine_duration 1 km [33]; Gebietsmittel-Referenzen [69]; register:98-E20-01 |
| \(v_{\text{verh}}\) | Verhaltens-Sensitivität — **Tages-Multiplikator an Komforttagen** (Default 1; Kette §3.4) | — | 1,25–1,60 als Tageswert; Jahreswirkung = Szenario (§3.4) [57–59]; register:98-S154-01 |
| \(\text{VOLY}\) | Wert eines verlorenen Lebensjahres | €₂₀₂₄ | **160.800** (Band 136,4–165,6 T€; Kette #95 §3.5) [19]; herleitung:#voly (in #95) |
| \(w_{\text{SCC}}\) | SCC-Anteil an C44 (altersinvariant, dokumentierte Annahme; Quellen-Widerspruch benannt §3.1) | — | **0,25** (Band 0,25–0,50) [27; obere Stütze 2015er-BfS-Split]; herleitung:#baf-c44 |
| \(\text{YLL}_{\text{Zelle}}\) | verlorene Lebensjahre — **nativer Ausweis** | Jahre/Jahr | Ergebnis |

### 3.6 Kartenebenen und Fallbacks

Ebenen: SSD/UV_RADIATION (neu: 1-km-Raster, Normalperioden-Mittel + Δ), u20 (aus #96),
Außenbeschäftigten-Anteil (neu, nur Sensitivität; INKAR/SVB-Proxy), YLL-Rate (Ergebnis).
Fallback SSD: solange das 1-km-Raster ab 1961 nicht angebunden ist, gilt das
Bundesland-Gebietsmittel [69] je Zelle (dokumentiert; Verlust der Feinstruktur — SSD
variiert v. a. Nord–Süd).

### 3.7 Schicht A (getrennt; nie auf €-Pfaden)

\(\hat H\)(E20: UV_RADIATION/SSD) × \(\hat E\)(R35: POPULATION_DENSITY / AGE_STRUCTURE) ×
\(\hat V\)(S154/S155/S158: Verhalten/Bewusstsein/Screening; R36: HEALTHCARE_ACCESS);
\(\text{Index} = 100 \cdot \max_p (w_p \hat H_p \hat E_p \hat V_p)\) (Worst-Pathway;
Normierungen editierbar, testseitig von €-Pfaden getrennt).

## 4 Kalibrierung & Validierung (§2.4/§3.4)

- **Kalibrierung = Baseline-Verankerung an der amtlichen Bundesinzidenz:** genau **ein
  Skalar je Entität** (\(c_{\text{kal,MM}}\) = 1,022; \(c_{\text{kal,C44}}\) = 0,999,
  §3.3) — die Bundes-Baseline reproduziert die ZfKD-Fallzahlen 2023 exakt. Eine
  Zeitreihen-Kalibrierung des **klimaattribuierten** Anteils ist nicht möglich: es
  existiert keine amtliche Reihe „UV-klimaattribuierte Fälle" (dokumentierte Ausnahme
  analog #96 §4); der Klimaanteil ist stattdessen messungsbasiert (SSD [69], Dosistrend
  [31], BAF [29,30]). **Kalibriermodell = Produktionsmodell** (lineares Modell, keine
  Näherungsläufe).
- **Sanity-Bänder (Unter- und Obergrenze):**
  Bundessummen (Basiswerte): \(\Delta F\) = **814 MM + 20.118 C44 ≈ 20.900 Fälle/Jahr**,
  **YLL ≈ 1.580/Jahr**, **€ ≈ 378 Mio €₂₀₂₄/Jahr** (Behandlung 124 + Mortalität 254).
  *Obergrenzen:* Behandlungs-€ = 6,8 % der amtlichen KKR C43/C44 (1.823 Mio €₂₀₂₃ [28]) ✓;
  klimaattribuierter Inzidenzanteil MM +3,0 %/C44 +8,3 % ≪ beobachteter
  Inzidenzanstieg (standardisierte MM-Rate 1999–2023 ≈ +55 %; C44-Hospitalisierungen
  2004–2024 +94,5 % [27,28]) ✓; YLL-Anteil = 1.580 / ≈ 40.600 Gesamt-Hautkrebs-YLL ≈ 4 %
  (konsistent zu BAF × ΔDosis) ✓. *Untergrenze:* SSD-Anstieg ist messfest > 0 (alle
  Regionen +6,3…+8,4 %, [69]); untere Bandkombination (k_UV 0,4 × a_attr 0,5) ergibt
  ≈ 119 Mio € > 0. Band gesamt ≈ **119–653 Mio €** (obere Kombination — Befund 207
  präzisiert: k_UV 1,0 × a_attr 1,0 × obere \(c_e\) für **beide** Entitäten = 653 Mio;
  Bänder von VOLY/BAF/\(w_{\text{SCC}}\) additiv separat ausgewiesen, nicht kumuliert).
- **Verteilschlüssel-Test (§3.1):** strikt bottom-up — Zelle ohne Bevölkerung → 0; das
  Klimasignal ist je Zelle/Region gemessen (kein Deutschland-Nenner). **Baseline-Fälle
  sind bevölkerungs-/altersproportional (kein Klimasignal); der klimaattribuierte
  Zusatz \(\Delta F\) trägt den vollen ΔDosis-Faktor** — Kommune ohne SSD-Anstieg → ~0 ✓
  (der native YLL-Ausweis und € enthalten nur den Zusatz, keinen Sockel).
- **Unabhängige Verteilungsprüfung** (vorab fixierte Toleranz): Ablese-Validierung der
  Altersraten gegen die amtlichen Rohraten (±15 %) — **bestanden** (Werte in der
  nächsten Zeile; danach normiert, §3.3). Mortalitäts-Querprüfung: ZfKD 2023 = 4.501
  Sterbefälle (3.169 + 1.332) vs. Destatis Todesursachen 2024 ≈ 4.600 [27,28] ✓.
  Ablese-Validierung (Roh-Bandraten vs. amtliche Rohraten, §3.3): MM **−2,2 %**, C44
  **+0,1 %** (nach Nenner-Korrektur Befund 212) — innerhalb ±15 %, danach ein
  Normierungsskalar je Entität. Regionale Achse:
  SSD-Regionalwerte sind eigene Messung [69]; eine unabhängige Länder-Inzidenz-Prüfung
  (GEKID-Atlas) ist nicht keyless — dokumentierte Lücke, Ersetzungspfad bei Integration.
- **Unsicherheiten:** k_UV-Paarung (Band 0,4–1,0 dominiert mit ±50 %); Attribution
  (±33 %); Ablesekette (±15 % vor Normierung, danach nur Verteilungsfehler); Latenz
  (§6); Entitäten-Split altersinvariant; \(c_e\)-Proxy; Augenschäden fehlen.

## 5 Maßnahmen-Hebel (§2.5/§3.5)

- **Früherkennungs-Förderung / SCS-Teilnahme (S158) — qualitativ** (Befund 203): Die
  DiD-Evidenz [34] belegt das Sparpotenzial (SCS-detektierte MM-Fälle: **−18,8 %
  [−23,1; −8,4]** Erstjahreskosten), aber der **Basiswert setzt bereits für alle Fälle
  die SCS-Kostensätze an** (Untergrenzen-Wahl §3.4) — ein zusätzlicher Hebel auf
  \(c_e\) würde den Maßnahmeneffekt doppeln (LF-4-Klasse: Maßnahmeneffekt schon im
  Basiswert). Quantifizierbar wird der Hebel erst mit einem **Detektionsmix-Parameter**
  (Anteil SCS-detektierter Fälle je Kommune als Basiswert-Größe, Hebel = Mix-Verschiebung
  × Kostendifferenz 11.410 − 6.724 €) — dokumentierter Ersetzungspfad; bis dahin
  qualitativ. Letalitätswirkung früherer Erkennung nicht angesetzt (dokumentiert).
- **UV-Schutz im öffentlichen Raum / Kommunikation (S155) — qualitativ** (§3.5-Regel;
  GP-Befunde 26/34): publizierte Nutzen-Kosten-Verhältnisse 2,2–8,7 : 1 [37] sind keine
  Effektgröße auf Dosis oder Inzidenz; keine deutsche Interventionsstudie [37]. Der Hebel
  läuft ehrlich als „qualitativ" (Verschattung senkt die effektive Dosis exponierter
  Gruppen — Wirkungsort wäre \(v_{\text{verh}}\)/lokale Dosis, sobald quantifiziert).
- **R7-Weiche:** nicht einschlägig (keine K8-Vorsorge-Gegenbuchung in der Netzwerkliste;
  kommunale Programmkosten laufen im Maßnahmen-Modul außerhalb der Schadenskonten).

## 6 Szenario-Anwendung & Modellgrenzen (§3.2/§3.6)

**Szenario-Anwendung 98-A:** Verschoben wird ausschließlich die Zell-SSD (Projektions-
raster bzw. Fortschreibung des Gebietsmittel-Trends; UV-B-Projektion +1,3 %/Dekade [32]
als Plausibilisierungsrahmen). Konstant: BAF, \(k_{\text{UV}}\), \(a_{\text{attr}}\),
Inzidenzraten, \(\lambda_e\), \(\bar L_e\), Kostensätze, Bevölkerung. **M0 weist das
Ist-Klima aus** (Normalperiodenvergleich). **Stationaritätsannahmen (dokumentiert):**
Inzidenz-Baseline stationär (real steigend — Untergrenze); Detektionsmix konstant.

**Modellgrenzen (dokumentiert):**
1. **Latenz:** Hautkrebs entsteht mit 20–40 Jahren Verzögerung [35] — \(\Delta F\) ist das
   „eingelaufene Risiko" der heutigen Dosislage, keine Vorhersage der Fälle *dieses*
   Jahres; die Jahres-Attribution ist konzeptionell unscharf (Infokasten-Pflichttext).
2. \(k_{\text{UV}}\)-Übersetzung: ein Messpunkt (Dortmund/NRW); Band 0,4–1,0 dominiert
   die Unsicherheit; Volltext-Fundstelle des Stations-SSD-Trends als Ersetzungspfad.
3. Attribution ohne DE-UV-Attributionsstudie (gekennzeichnete Abschätzung, Band).
4. Verhalten dominiert die reale Exposition (KWRA-Kernaussage) — \(v_{\text{verh}}\)
   bleibt Sensitivitätsband, der Basiswert bildet nur den Ambient-Dosispfad ab
   (Untergrenze der Verhaltens-These, Doppelzählungsschutz §3.4).
5. Ablesekette der Altersraten (±15 % vor Normierung); ZfKD-Datenbank als Ersetzungspfad.
6. Augenschäden (Katarakt) und K2-Produktivität nicht enthalten (Untergrenze).

**Infokasten-/UI-Texte (§3.6 — Teil des Berichts):**

> **Infokasten 1 — am Gesamtwert:** „Dieser Wert ist der *bewertete Schaden im Konto K1
> Gesundheit (Ursache: UV)* (Modellstand M0). Er umfasst die klimaattribuierten
> zusätzlichen Hautkrebs-Behandlungskosten und den Wert verlorener Lebensjahre — nicht
> enthalten sind u. a. Augenerkrankungen, Arbeitsproduktivität (Stufe M3) und
> Vorsorgekosten. Der ausgewiesene Betrag ist deshalb eine bewusste **Untergrenze**; er
> wird mit jeder Ausbaustufe vollständiger — nie kleiner. Berechnet mit Modellstand M0,
> Stand ⟨Datum⟩."
>
> **Infokasten 2 — zur Latenz (Pflichttext):** „UV-bedingter Hautkrebs entsteht mit
> 20–40 Jahren Verzögerung. Die ausgewiesenen Zusatzfälle beschreiben das mit der
> heutigen, klimabedingt erhöhten UV-Belastung ‚eingelaufene' Erkrankungsrisiko — nicht
> die exakten Fälle des laufenden Jahres."
>
> **Pflicht-Elemente:** Benennung „bewerteter Schaden — Konto K1 (Ursache: UV)" (nie
> „Gesamtschaden"); Vollständigkeitsanzeige „Stufe M0: 1 von 8 Konten aktiv" mit
> Roadmap-Aufklappliste; Versionsstempel „berechnet mit Modellstand M0 — Untergrenze".

**Raten-Darstellung und Aggregation** (§3.6): nativ **YLL je 1.000 EW und Jahr**;
Teil-Ausweise: Zusatzfälle je 1.000 EW (je Entität), € je EW und Jahr; Quartier-Aggregat;
Kommune = Summe der Zellen.

## 7 Parameter-Blöcke (maschinenlesbar, §4)

```yaml
parameter:
  id: uv.ssd_delta_region
  wert: "backend/data/kalibrierung/ssd_trend_region.csv"
  einheit: "%"
  band: null   # Normalperioden-Vergleich 1961-90 vs. 1991-2020 (GP-Befund 37)
  herkunft: register:98-E20-01
  quelle: dwd_cdc_gebietsmittel_ssd
  preisstand: null
  bandzuordnung: [u20, 20-64, 65-74, 75-84, 85+]
  endpunkt: beide
parameter:
  id: uv.k_uv
  wert: 0.84
  einheit: "-"
  band: [0.4, 1.0]   # untere Stuetze: M0-Stations-Paarung 0,43 (11,3 unbelegt); obere: Globalstrahlungs-Parallele
  herkunft: register:98-E20-02
  quelle: lorenz2024_dwd_ssd_trend
  preisstand: null
  bandzuordnung: [u20, 20-64, 65-74, 75-84, 85+]
  endpunkt: beide
parameter:
  id: uv.a_attr
  wert: 0.75
  einheit: "-"
  band: [0.5, 1.0]   # gekennzeichnete Abschaetzung (§3.2; GP-Befund 15)
  herkunft: register:98-E20-03
  quelle: lorenz2024_einordnung
  preisstand: null
  bandzuordnung: [u20, 20-64, 65-74, 75-84, 85+]
  endpunkt: beide
parameter:
  id: uv.baf
  wert: {mm: 0.6, c44: 1.675}
  einheit: "-"
  band: {mm: [0.2, 1.0], c44: [1.675, 1.95]}   # ueber w_scc-Band 0,25-0,50 (Befund 202)
  herkunft: register:98-E20-04
  quelle: slaper1996_rivm2023_madronich2021
  preisstand: null
  bandzuordnung: [u20, 20-64, 65-74, 75-84, 85+]
  endpunkt: beide
parameter:
  id: uv.w_scc
  wert: 0.25
  einheit: "-"
  band: [0.25, 0.50]   # KID-2025-Primaerangabe; obere Stuetze BfS-2015-Split (Widerspruch benannt §3.1)
  herkunft: herleitung:#baf-c44
  quelle: zfkd_kid2025_bfs2015
  preisstand: null
  bandzuordnung: [u20, 20-64, 65-74, 75-84, 85+]
  endpunkt: beide
parameter:
  id: uv.i_raten_roh
  wert: {mm: {u20: 0.5, 20-64: 24.7, 65-74: 64.0, 75-84: 94.9, 85+: 88.5},
         c44: {u20: 2.0, 20-64: 125.9, 65-74: 617.6, 75-84: 1267.2, 85+: 1479.5}}
  einheit: "1/100000a"
  band: null   # ROH-Ablesewerte (Anlage kid2025_ablesewerte.csv); Normierung via uv.c_kal in der Formel (Befund 201); ZfKD-Ersetzungspfad
  herkunft: register:98-R35-01
  quelle: zfkd_kid2025
  preisstand: null
  bandzuordnung: [u20, 20-64, 65-74, 75-84, 85+]
  endpunkt: beide
parameter:
  id: uv.lambda
  wert: {mm: 0.1155, c44: 0.00549}
  einheit: "-"
  band: null   # Perioden-Approximation, gekennzeichnet (GP-Befund 43)
  herkunft: register:98-K1-02
  quelle: zfkd_kid2025
  preisstand: null
  bandzuordnung: [u20, 20-64, 65-74, 75-84, 85+]
  endpunkt: mortalitaet
parameter:
  id: uv.l_rest
  wert: {mm: 10.58, c44: 5.30}
  einheit: "Jahre"
  band: null   # Median-Approximation, gekennzeichnet (GP-Befund 43)
  herkunft: register:98-K1-02
  quelle: zfkd_kid2025_sterbetafel2224
  preisstand: null
  bandzuordnung: [u20, 20-64, 65-74, 75-84, 85+]
  endpunkt: mortalitaet
parameter:
  id: uv.c_fall
  wert: {mm: 6724, c44: 5883}
  einheit: "EUR/Fall"
  band: {mm: [6724, 11410], c44: [5883, 7436]}   # SCS- vs. nicht-SCS-detektiert; Proxy §3.4
  herkunft: register:98-K1-01
  quelle: speckemeier2022
  preisstand: "2024"
  bandzuordnung: [u20, 20-64, 65-74, 75-84, 85+]
  endpunkt: morbiditaet
parameter:
  id: uv.voly
  wert: 160800
  einheit: "EUR/Jahr"
  band: [136400, 165600]
  herkunft: herleitung:#voly   # Kette in #95 §3.5 (P52)
  quelle: uba_mk40_amann2020a
  preisstand: "2024"
  bandzuordnung: [u20, 20-64, 65-74, 75-84, 85+]
  endpunkt: mortalitaet
parameter:
  id: uv.c_kal
  wert: {mm: 1.022, c44: 0.999}
  einheit: "-"
  band: null   # Normierungsskalar je Entitaet; wirkt in der §3.3-Formel auf uv.i_raten_roh (Befund 201)
  herkunft: herleitung:#i-raten
  quelle: zfkd_kid2025
  preisstand: null
  bandzuordnung: [u20, 20-64, 65-74, 75-84, 85+]
  endpunkt: beide
parameter:
  id: uv.r_out_sensitivitaet
  wert: 1.0
  einheit: "-"
  band: [1.0, 1.05]   # Basiswert-Default 1 (GP-Befund 9); Formel §3.4 (w_Z = 0,373; Befund 206)
  herkunft: register:98-OUT-01
  quelle: schmitt2011_destatis_vgr
  preisstand: null
  bandzuordnung: [u20, 20-64, 65-74, 75-84, 85+]
  endpunkt: beide
parameter:
  id: uv.v_verh_sensitivitaet
  wert: 1.0
  einheit: "-"
  band: [1.0, 1.6]   # TAGES-Multiplikator an Komforttagen (Kette §3.4, Befund 205); Jahreswirkung = Szenario; Default 1
  herkunft: register:98-S154-01
  quelle: graffzivin_neidell2014
  preisstand: null
  bandzuordnung: [u20, 20-64, 65-74, 75-84, 85+]
  endpunkt: beide
```

## 8 Quellen (§3.8 — #98-relevanter Auszug; Nummern = M0-Zählung, [69]–[70] neu)

Zugriff 17./18.08.2026 ([27], [31], [34], [43], [70]: 30.08.2026 primär
verifiziert/neu gezogen). **Archiv-Snapshots:** wie #95 Kap. 8 (Ratchet bei Integration).

- **[19]** UBA, „Methodenkonvention 4.0" (umweltbundesamt.de); Amann u. a. 2020a
  (VOLY-Kette vollständig in #95 §3.5, Archiv-Link dort); Destatis-VPI lange Reihen,
  destatis.de (2020 = 100: 2015 = 94,5 · 2024 = 119,3; geprüft gegen die
  Basis-2020-Tabelle).
- **[27]** Zentrum für Krebsregisterdaten (ZfKD)/GEKID, „Krebs in Deutschland für
  2021–2023" (KID 2025), Kap. 3.13 (C43) und 3.14 (C44), krebsdaten.de
  (PDF-Kapitel abgerufen 30.08.2026; Tab. 3.13.1/3.14.1: MM 2023 27.430 Neuerkrankungen /
  3.169 Sterbefälle, mittleres Sterbealter F 78/M 76; C44 2023 242.820 / 1.332, F 88/M 85;
  Abb. 3.13.2/3.14.3: altersspezifische Raten — Ablesekette §3.3); Entitäten-Split 2015
  (BCC 158.840 · SCC 98.950 · MM 35.495) nach S. Baldermann, C. Lorenz,
  Bundesgesundheitsbl 62:639–645, 2019, doi:10.1007/s00103-019-02934-w
  (**Sekundärangabe**, Volltext-Verifikation als Ersetzungspfad).
- **[28]** Destatis, Krankheitskostenrechnung C43–C44: 2023: 1.823 Mio. € (GENESIS
  23631-0003); Destatis PM N036 (28.05.2026): stationäre Hautkrebsfälle 2004–2024
  +94,5 %, Sterbefälle 2024: 4.600.
- **[29]** H. Slaper, G. J. M. Velders, J. S. Daniel, F. R. de Gruijl, J. C. van der Leun,
  „Estimates of ozone depletion and skin cancer incidence to examine the Vienna Convention
  achievements", Nature 384:256–258, 1996. doi:10.1038/384256a0; BAF-Werte (SCC 2,5 ± 0,7 ·
  BCC 1,4 ± 0,4 · CM 0,6 ± 0,4) dokumentiert in RIVM Letter Report 2023-0426, S. 21 f.
- **[30]** S. Madronich u. a., ACS Earth Space Chem 5(8):1876–1888, 2021.
  doi:10.1021/acsearthspacechem.1c00183 (unabhängige BAF-Bestätigung 2,6/1,4/0,6).
- **[31]** S. Lorenz, F. Heinzl, S. Bauer, M. Janßen, V. De Bock, A. Mangold,
  P. Scholz-Kreisel, D. Weiskopf, „Increasing solar UV radiation in Dortmund, Germany:
  data and trend analyses and comparison to Uccle, Belgium", Photochem Photobiol Sci
  23(12):2173–2199, 2024. doi:10.1007/s43630-024-00658-8 — Abstract primär verifiziert
  30.08.2026: H_er,day **+4,9 %/Dekade**, UVI_max +3,2 %/Dekade (Dortmund 1997–2022,
  signifikant); Uccle +7,5/+5,8; Trendursache „starker Einfluss der Bewölkungsabnahme";
  BfS-PM 017/2024.
- **[32]** R. Vitt u. a. (2020): UV-Index satellitengestützt +1,2–3,6 %/Dekade; K.
  Eleftheratos u. a. (2020): UV-B-Projektion +1,3 %/Dekade 2050–2100 — beide zit. n.
  KWRA 2021 TB5, umweltbundesamt.de (lokal: `docs/KWAR/`); nur Band-/Rahmenstützen,
  nicht wertetragend.
- **[33]** DWD Climate Data Center (CDC): Raster sunshine_duration (1 km);
  Gebietsmittel Sonnenscheindauer (regional_averages_sd_year.txt) — Grundlage von [69];
  Lizenz DL-DE->Zero-2.0.
- **[34]** C. Speckemeier u. a., „One-year follow-up healthcare costs of patients
  diagnosed with skin cancer in Germany: a claims data analysis", BMC Health Serv Res
  22:749, 2022. doi:10.1186/s12913-022-08141-9 (PMC9188701, Volltext-Abstract primär
  verifiziert 30.08.2026: AOK-Routinedaten, Diagnosekohorte 2014/2015; MM 5.326
  [SCS-detektiert] vs. 9.038 € [nicht-SCS]; NMSC 4.660 vs. 5.890 €; DiD: SCS senkt
  MM-Erstjahreskosten um 18,8 % [8,4–23,1]).
- **[35]** Leitlinienprogramm Onkologie, „S3-Leitlinie Prävention von Hautkrebs",
  Version 2.1, Sept. 2021, leitlinienprogramm-onkologie.de (Latenz „Jahrzehnte").
- **[36]** BfS, PM 005/2022, bfs.de; S. Baldermann, C. Lorenz, Bundesgesundheitsbl
  62:639–645, 2019. doi:10.1007/s00103-019-02934-w (Erratum doi:10.1007/s00103-019-03001-0;
  keine quantifizierte Mehr-Exposition je Komforttag publiziert).
- **[37]** S. T. Shih u. a. (2009/2017, Prev Med); C. M. Doran u. a. (2016, PLOS ONE);
  L. G. Collins u. a. (2024, Health Promot Int): Benefit-Cost 2,2–8,7 : 1 (AUS/USA/EU;
  Fundstellen via PubMed dokumentiert); Baldermann & Weiskopf 2020: keine deutsche
  Kosten-Nutzen-Studie — **keine Effektgrößen, nicht wertetragend** (§5; qualitativer
  Hebel).
- **[43]** J. Schmitt u. a., „Occupational ultraviolet light exposure increases the risk
  for the development of cutaneous squamous cell carcinoma: a systematic review and
  meta-analysis", Br J Dermatol 164(2):291–307, 2011. doi:10.1111/j.1365-2133.2010.10118.x
  — Abstract primär verifiziert 30.08.2026: Fall-Kontroll-Pool OR 1,77 [1,37–2,30],
  Kohorten 1,68 [1,08–2,63]; Grundlage BK 5103.
- **[48]** Destatis, Sterbetafel 2022/2024 (Blätter 12613-b01/-b02, destatis.de): e(78)F = 10,92 ·
  e(76)M = 10,33 · e(88)F = 5,04 · e(85)M = 5,47; Bevölkerung 31.12.2023 nach
  Altersjahren (Statistischer Bericht 5124108237005, Tab. 12411-06) — Gewichte §3.3;
  Männeranteil 85+ = 990.292/2.844.213 = 0,348.
- **[57]** J. Graff Zivin, M. Neidell, „Temperature and the Allocation of Time",
  J Labor Econ 32(1):1–26, 2014. doi:10.1086/671766 (ATUS; Outdoor-Freizeit ≈ +1,2 min/°C).
- **[58]** „Intraday adaptation to extreme temperatures in outdoor activity", Sci Rep 2023,
  ncbi.nlm.nih.gov/pmc/PMC9832153 (−5 % > 30 °C, −13 % > 35 °C); US-Dosimeterkohorte
  ncbi.nlm.nih.gov/pmc/PMC3566166.
- **[59]** J. Sun u. a., J Photochem Photobiol B 2014 (Kleidung, nur Richtung);
  A. W. Schmalwieser u. a., Br J Dermatol 2021, doi:10.1111/bjd.20703 (Zeit im Freien
  erklärt persönliche Dosis, R² 0,75–0,79).
- **[69]** SSD-Trend-Auswertung: `backend/scripts/kalibrierung/dwd_ssd_trend.py` +
  `backend/data/kalibrierung/ssd_trend_region.csv` (Normalperioden-Mittel je Bundesland
  **und** Region + linearer Trend 1997–2022; Lauf 30.08.2026; DE 1.544,0 → 1.664,8 h
  = +7,82 %; NRW-Trend 5,81 %/Dekade); Ablese-Anlage:
  `backend/data/kalibrierung/kid2025_ablesewerte.csv` (Befund 204).
- **[70]** Destatis, „Erwerbstätige und Arbeitnehmer nach Wirtschaftsbereichen
  (Inlandskonzept)", destatis.de (Abruf 30.08.2026): 2023 gesamt 45.909 Tsd.;
  Land-/Forstwirtschaft/Fischerei 572 Tsd.; Baugewerbe 2.643 Tsd. ⇒
  \(\bar q_{\text{out}}\) = 0,0700.

## 9 Familien-Einordnung & Verworfen-Liste (§2.6 — kein erneuter Drei-Ansätze-Vergleich)

#98 ist Folge-Risiko der Familie **„K1-Gesundheit bottom-up"** (Prototyp #95; vollständiger
Ansatz-Vergleich für #98 in M0 Rev. 5 Kap. 4/5). Verworfene Alternativen (§2.6):

- **98-B — Reine Dosis-Wirkungs-Kette (BfS-/Satelliten-UV-Klimatologie):** methodisch
  strengste Kette, aber die UV-Rasterbeschaffung ist ein eigenes Datenprojekt (keine freie
  Rasterklimatologie gefunden [31,36]) und der KWRA-Verhaltenspfad entfiele —
  dokumentierte Alternative für M1+ (Parameter bis zur Quelle in M0 Kap. 4).
- **98-C — Nationaler Kostenanker, top-down:** per §3.1 ausgeschieden (Verteilschlüssel;
  normatives \(a_{\text{klima}}\); Deutschland-Nenner) — nur Negativ-Beispiel.

## Entscheidungslog

Einträge 1: M0-Entscheidung (rückwirkend dokumentiert). Einträge 2–15: Rev.-1-
Entscheidungen (`/risiko-auto 98`, Gate 1, 30.08.2026); Aktualisierungen nach
Review-Runde 1 (Befunde 202/203) in den Zeilen 5, 9, 12 vermerkt.
**Überstimmungsweg:** „Entscheidung Nr. X ändern auf …" → Delta-Lauf (Neurechnung +
Re-Review + PDF-Neuexport). ⚠ = Ermessensfall.

| Nr | Frage | angewendete Entscheidung | Begründung | Alternative | Auswirkung |
|---|---|---|---|---|---|
| 1 | Methodischer Ansatz für #98? | **98-A** amtliche Inzidenz + BAF-Trend-Attribution (Familie K1-Gesundheit bottom-up) | jede Komponente amtlich/publiziert; minimale Datenanbindung (M0 Kap. 5) | 98-B (UV-Datenprojekt, M1+); 98-C ausgeschieden | Gesamtmodell |
| 2 ⚠ | k_UV-Paarung? | **0,84** = Dosistrend 4,9 [31] ÷ eigener NRW-SSD-Trend 5,81 [69] (gleiches Fenster, gleiche Datenfamilie wie das Produkt); Band 0,4–1,0 | M0-Kette 4,9/11,3 = 0,43 beruhte auf unbelegtem Stationstrend (GP-Befund 10/16); Raster-konsistente Paarung; Satelliten-Plausibilisierung ✓ | 0,43 (Stations-Paarung — untere Bandstütze; Volltext-Fundstelle als Ersetzungspfad) | Klimasignal ×1,95 ggü. M0; dominanter Bandtreiber |
| 3 ⚠ | Attribution des SSD-Trends? | **a_attr,UV = 0,75** (0,5–1,0), gekennzeichnete Abschätzung | GP-Befund 15 (Konsistenz zur #96-Logik); Lorenz-Wolkenbefund hoch, Aerosol-Brightening < 1,0 | 1,0 (M0, unattribuiert — verworfen) | −25 % ggü. M0-Logik; Band ±33 % |
| 4 | SSD-Fenster? | **Klimanormalperioden je Zelle** (1961–90 vs. 1991–2020) | GP-Befund 37; Einzeljahre zu variabel | gleitende Fenster | reproduzierbar |
| 5 ⚠ | Altersspezifische Inzidenz? | **Ablesekette aus KID-Abb.** (Roh-Ablesewerte als Anlage-CSV; geschlechtsspezifische Bevölkerungsgewichte [48]) + Normierung auf amtliche Rohraten (ein Skalar je Entität, wirkt in der Formel — Befunde 201/204) | ZfKD-Datenbank nicht keyless (dokumentierte Lücke); Winklmayr-Ablese-Präzedenz #95; Validierung −2,2 %/+0,1 % ∈ ±15 % (nach Befund 212) | warten auf ZfKD-Abfrage (blockiert M0) | Baseline exakt ZfKD-verankert |
| 6 | Native Ergebnisgröße? | **YLL/Jahr**; ΔFälle je Entität, € Teil-Ausweise | GP-Befund 28; K1-Mortalität + Morbidität | ΔFälle nativ | Ausweis |
| 7 ⚠ | Fallkosten-Basis? | **SCS-detektierte Erstjahreskosten** (MM 6.724 / C44 5.883 €₂₀₂₄); nicht-SCS als Obergrenze; Proxy gekennzeichnet; Preisstand-Annahme 2015 | Untergrenzen-Zusage (#95-Befund-62-Lehre); Gesamt- vs. inkrementelle Kosten diskutiert (§3.4) | nicht-SCS-Werte (M0-Wahl 9.038/5.890) | Behandlungs-€ −21 % ggü. M0-Wahl |
| 8 | λ_e / L̄_e? | exakte 2023-Quotienten + Sterbetafel-Kette; **Approximationen gekennzeichnet** | GP-Befund 43 (Perioden-/Median-Approximation, Richtung benannt) | Kohorten-Letalität (Datenprojekt) | Mortalitätspfad ehrlich |
| 9 ⚠ | Entitäten-Split C44? | **SCC 25 % altersinvariant** (aktualisiert nach Befund 202: KID-2025-Primärangabe; Band 0,25–0,50 mit BfS-2015-Split 0,384 als oberer Stütze; Widerspruch benannt §3.8) | Primärquelle vor Sekundärangabe; GP-Befund 41 (Altersinvarianz dokumentiert) | 0,384 (BfS 2015 — M0-Wahl) | BAF_C44 1,675 statt 1,82; C44-Zusatz −8 % |
| 10 ⚠ | Außenberufe (kein Ketten-Knoten)? | **Sensitivitätsband, Basiswert-Default 1**; Evidenz + q̄_out = 0,070 vollständig hergeleitet; Ersetzungsweg = Arbeitsmappen-Fortschreibung + AP-Punkt | GP-Befund 9 (Kettentreue „nicht mehr, nicht weniger"); Aufnahme in den Basiswert erfordert Quellen-Fortschreibung (§1/LF 14) — nicht still ergänzen | dokumentierte Kettenerweiterung mit sofortiger xlsx-Fortschreibung | Bundessumme unverändert (zentriert); Zell-Differenzierung ±2 % entfällt vorerst |
| 11 | Verhaltens-Modulation (S154)? | **Default 1**, Band +0,25…+0,60 je Komforttag dokumentiert | keine DE-Effektgröße [36]; US-Evidenz nur Band; Ambient-Anteil schon in ΔDosis (Doppelzählungsschutz) | v_verh im Basiswert | Untergrenze der KWRA-Verhaltens-These |
| 12 | Maßnahmen-Hebel? | **beide qualitativ** (aktualisiert nach Befund 203): UV-Schutz/Kommunikation ohne Effektgröße; SCS-Förderung mit belegtem Sparpotenzial, aber Kostenwirkung bereits im Basiswert (Untergrenzen-\(c_e\)) | GP-Befunde 26/34 + Befund 203 (LF-4-Wächter); Detektionsmix-Parameter als Ersetzungspfad | Mix-Parameter sofort einführen (Datenlücke: kommunale SCS-Quoten) | Hebelliste ehrlich; kein Doppelzählungsrisiko |
| 13 | R36 im Basiswert? | **Default 1** (nur Schicht A) | keine Evidenz; Zugangseffekt steckt im SCS-Hebel | Distanz-Sensitivität | Basiswert schlanker |
| 14 | Latenz-Behandlung? | „eingelaufenes Risiko" + Pflicht-Infokasten; kein Latenz-Discounting | [35]; Jahres-Attribution transparent unscharf | Kohorten-Latenzmodell (M2+) | Kommunikation ehrlich |
| 15 ⚠ | Kalibrierung? | **ein Normierungsskalar je Entität** (1,022/0,999) an der ZfKD-Bundesinzidenz; keine Zeitreihen-Kalibrierung des Klimaanteils (keine amtliche Reihe existiert — dokumentierte Ausnahme analog #96) | §3.4 („EIN Skalar"); Klimaanteil messungsbasiert (SSD/Dosis/BAF) | Fit an KKR-Kostenreihe (konfundiert durch Screening/Kodierung — verworfen) | Baseline amtlich exakt; Klimaanteil über Bänder |
