# Methodik-Bericht #96 — Allergische Reaktionen durch Aeroallergene pflanzlicher Herkunft

Status: **Rev. 2 (P̂-Zentrierung auf die eigene Kommune statt auf ein Bundesmittel —
Aufgabe §3.2 „geschlossene Betrachtungsebene", Nutzer-Entscheid 31.08.2026;
Log 18/19) — im Review** · 31.08.2026 · Rev. 1 war abnahmereif (Null-Runde
Runde 3) und ist integriert ·
Instruktionsquelle: `docs/AUFGABE_METHODIK_SCHADENSRECHNUNG.md` (v2) · Umsetzungsgrundlage:
**Ansatz 96-A** (Prävalenz × gemessene Pollensaison-Spreizung, bottom-up; Entscheidungslog Nr. 1)
· Familie: **K1-Gesundheit bottom-up** (Prototyp #95; §2.6 — kein erneuter Drei-Ansätze-Vergleich)

> **Konformitätsvermerk zu den Aufgaben-Fortschreibungen 30./31.08.2026**
> (Ressourcen-Regel §3.4, Datenebenen-Anlagepflicht §3.1, geschlossene
> Betrachtungsebene §3.2; Nutzer-Entscheide, vgl. #95 Rev. 8):
> Dieser Bericht ist geprüft konform — er plant **keinen** nationalen
> 100-m-Vollraster-Lauf als Prüf-/Abgleichinstrument; die P̂-Zentrierung nutzt
> seit Rev. 2 ausschließlich das Mittel der **eigenen Kommune** (§3.3, Log 18/19); die Ebenen POLLEN_LOAD (OSM-Vegetation, §3.3), POPULATION_U20 (§3.2) und CANOPY_BIRCH_FRACTION **sind mit der Integration am 31.08.2026 angelegt** (§3.1-Anlagepflicht erfüllt); alle übrigen Zellgrößen sind vorhanden oder regional/national — keine Zellgröße läuft auf einem unspezifizierten Neutral-Fallback.

> **Revisionsstand.** **Rev. 2 (31.08.2026)** = Bezugsebene der P̂-Zentrierung:
> \(\bar G\) ist nicht mehr ein bundesweites Referenzmittel, sondern das
> betroffenengewichtete Mittel der **betrachteten Kommune**, im Lauf aus ihren
> eigenen Zellen gebildet (Aufgabe §3.2 „geschlossene Betrachtungsebene",
> Nutzer-Entscheid; Log 18). Damit gilt Σ B·P̂ = Σ B je Kommune **exakt**, ein
> Registry-/Bundeswert entfällt ersatzlos, und ohne Referenz bleibt P̂ ≡ 1.
> Folgeentscheidung Log 19: **kein** eingefrorener Referenzzustand — ein
> flächiger Vegetations-Niveaueffekt bleibt bewusst unbuchbar (§5,
> Modellgrenze 7). Betroffen: §3.3, §3.4-Sensitivität, §3.6-Zeichentabelle, §5,
> §6, Entscheidungslog 17–19. Rev. 1 = Migration des #96-Anteils von M0 Rev. 5
> (`docs/render/METHODIK_M0_GESUNDHEIT.html`, Kap. 3) in das §4-Format **plus** Abarbeitung
> der #96-relevanten Befunde aus `reviews/Gegenpruefung_Rev5_Befundliste.md`
> (11–14, 22, 26–30, 32, 34–36, 49, 52); Status je Befund in `reviews/BEFUNDE_96.md`.
> Diese Markdown-Datei ist die Quelle für #96 (§2.7). Alle Ermessensentscheidungen im
> **Entscheidungslog** (Ende der Datei). Anlagen:
> `backend/scripts/kalibrierung/dwd_pollensaison.py` +
> `backend/data/kalibrierung/pollensaison_region.csv` / `pollensaison_meta.csv`.

## 1 Wirkungskette & Knoten-Bilanz (§2.1)

Kette laut Arbeitsmappe (Sheet „Klimawirkungsketten" Z412, Knoten **W189**; Konfidenz mittel —
containerweiter Sensitivitätspfeil, Container-Expansion „Vegetation"). Rollen/Kanten: Sheet
„Schadensbaum-Netzwerkliste" Z97 (Id 96): **Buchungsobjekt — Ebene B**, Handlungserfordernis
**sehr dringend**; eingehende Kante der Netzwerkliste: **#1** „Veränderung der Länge der
Vegetationsperiode und Phänologie" (Treiber 0 €). W189 hat **keine direkten klimatischen
Einflüsse** — der Klimapfad läuft vollständig über die vorgelagerten Wirkungen W024/W025
(deren Eingänge eine Ebene tief: E01 Durchschnittstemperatur, **E09 Trockenheit** [nur W025],
S010–S020 Habitat/Landnutzung, R03/R04).

### Knoten-Bilanz

| Knoten | Name | rechnet in | Wo (Formel/Ebene) | falls inaktiv: Begründung |
|---|---|---|---|---|
| W025 | Pollenflug (vorgelagert, 0 € per R2; Eingänge E01, E09) | Schicht A + B | Saison-Spreizung \(\Delta S_B, \Delta S_G\) (DWD-Phänologie, §3.1); Ebene POLLEN_LOAD (neu) | — |
| W024 | Ausbreitung von Pflanzenarten mit allergenem Potenzial (0 €; E01, S010–S020, R03/R04) | Schicht B (lokal) + dokumentierte Alternative | lokale allergene Vegetation \(\hat G\) im Faktor \(\hat P_{\text{Zelle}}\) (§3.3); Neophyten-Pfad (Ambrosia) = Modul 96-B ab M1 | Ambrosia-Arealmodell bewusst nicht in M0 (Log 13) |
| #1/W022 | Phänologie/Vegetationsperiode (Netzwerklisten-Kante; Treiber 0 €) | Schicht B | die ΔS-Messung (§3.1) **ist** die Operationalisierung dieses Knotens (KWRA-Indikator GE-KL-07 = Front-Marker) | — |
| E01 | Durchschnittstemperatur (eine Ebene tief, via W024/W025) | implizit in Schicht B | steckt im **gemessenen** Phänologie-Signal ΔS; kein eigener Temperatur-Term (Kein-Doppelkanal §3.2) | — |
| E09 | Trockenheit (eine Ebene tief, Eingang von W025) | **bewusst inaktiv** | — | keine quantifizierte Trockenheit→Pollen-ERF; Wirkrichtung intensitätserhöhend — konsistent zur konservativen Nicht-Ansetzung der Intensität (Log 14; Rev.-5-Befund 52) |
| S010–S020 | Habitat-/Landnutzungs-Sensitivitäten (Eingänge W024) | teilweise Schicht B | nicht separat parametrisiert; wirken über die lokale allergene Vegetation \(\hat G\) (analog W124-Komponenten-Logik in #95) | — |
| R03/R04 | Vorkommen von Arealen/Arten bzw. Biotopen (Eingänge W024/W025) | Schicht B (via \(\hat G\)) | OSM-Vegetationsdaten der Zelle | — |
| S158 | Monitoring von Gesundheitsgefahren / Frühwarnsysteme | Maßnahmen-Hebel (**qualitativ**) | Pollen-Frühwarnung (DWD/PID-Gefahrenindex); Ebene EARLY_WARNING_SYSTEMS (§5) | im Basiswert Default 1: keine quantifizierte Interventions-Effektgröße (§3.5; Log 15) |
| R35 | Vorkommen von Bevölkerung | Schicht A + B | \(\text{pop}_a\) (Zensus 2022, 100 m; neue Ebene u20 — §3.2) | — |
| R36 | Vorkommen von Gesundheitsinfrastruktur | Schicht A (Screening) | Ebene HEALTHCARE_ACCESS im Index (§3.6) | Basiswert Default 1: AR ist ein ambulantes Krankheitsbild; für einen Distanz-Effekt auf AR-Behandlungstage existiert keine Evidenz (§3.2: unbelegte Modulatoren Default 1; Log 16) |

KWRA-Indikator (intensive Betrachtung „Blühbeginn der Erle"): **GE-KL-07** „Tag des
Blühbeginns der Erle im Jahr" — geht direkt als Front-Marker in \(\Delta S_B\) ein (§3.1).
KWRA-Einstufung: Risiko Gegenwart „gering", Mitte des Jahrhunderts „mittel" (starker Wandel
„hoch"); Handlungserfordernis dennoch **sehr dringend** (lange Anpassungsvorlaufzeiten:
Stadtbaum-Generationen) [15].

### Weitergaben (zweispaltig; Quelle: Netzwerkliste + Abgleich-Protokoll)

| Output-Kanten (Abgleich-Protokoll) | Konto-Ausschlüsse / verwandte Buchungen (K1-Definition) |
|---|---|
| **keine** — die Netzwerkliste führt für #96 keine Output-Kanten, das Abgleich-Protokoll keinen Punkt zu #96. (W-Ebene: W189 speist W196/W197 „Belastung der Gesundheitsinfrastruktur" — auf Buchungsebene läuft Systemlast über die K1-Definition, s. rechts) | **Arbeitsausfall/Produktivität → K2** via **#87** (ab Stufe M3) — Monetarisierung ID 96 (Blattzeile 101), Spalte „Nicht enthalten": „Arbeitsausfall (K2)"; **Systemvorhaltung → K8 via ID 102** (K1-Definition; keine Kante von #96) |

### Konto-Einbettung

- **Konto:** K1 Gesundheit, **Ursache: Allergene** (R9-Partition; jeder Fall zählt genau
  einmal); Baustein **nur K1-Morbidität** (Risiken-Monetarisierung, ID 96 = Blattzeile 101:
  „Zusätzliche Fallzahlen/Behandlungstage × Behandlungskostensätze") — **keine
  Mortalitätskomponente** (kein YLL/VOLY-Pfad in diesem Bericht).
- **Anzuwendende Rechenregeln:** R9 (Ursachenpartition; laut Monetarisierung, Spalte „Regeln").
- **Nur K1 aktiv (M0):** bewusste **Untergrenze** („konservativ" heißt in diesem Bericht
  durchgängig *unterschätzend*, wie in #95 §4); der größte Teil der volkswirtschaftlichen
  Allergie-Last (Produktivität, Präsentismus [8,65]) folgt per R9 in K2/#87 ab M3 — nichts
  geht verloren, nichts wird doppelt gezählt.

## 2 Evidenz-Register (§2.2)

Risikoübergreifend wiederverwendbare Zeilen zusätzlich in `docs/evidenz/register.md`.
Nur Zeilen mit Entscheidung **Basiswert** kommen in den Formeln (§3) vor. Spalte „E-Regel":
die §2.8-E-Regeln sind in der Aufgabe noch nicht definiert (Lücken-Vermerk §2.8) — die
Spalte verweist auf die Entscheidungslog-Nummer.

| Register-ID | Knoten → Outcome | Effektgröße | Studientyp | Quelle | Übertragbarkeit | Datenlage je Zelle | Entscheidung | E-Regel |
|---|---|---|---|---|---|---|---|---|
| 96-W025-01 | W025/#1 Phänologie → Saison-Spreizung | \(\Delta S_B\) = 3,96/4,20/5,94 · \(\Delta S_G\) = 4,78/4,08/3,70 Tage (N/M/S; 1961–90 → 1991–2020) | amtliche Messreihe (DWD-Phänologie), eigene Auswertung (Skript [67]) | DWD-CDC Jahresmelder [33]; `pollensaison_region.csv` [67] | DE-weit, 1.083/1.085 gepaarte Stationen; Marker-Wahl §3.1 (Birke Phase 4 — Log 3) | regional (N/M/S je Bundesland, wie #95) | **Basiswert** | Log 2–5 |
| 96-W025-02 | Klimawandel → Anteil am Saisontrend | \(a_{\text{attr}}\) = 0,50 (IQR 0,19–0,84) | Attributionsstudie (Beobachtung × Klimamodelle) | Anderegg 2021, PNAS [9] | Nordamerika 1990–2018; Übertragung auf DE als dokumentierte Annahme (einzige publizierte Attribution) | Literatur-Band | **Basiswert** | Log 11 |
| 96-W025-03 | Intensitätszunahme (Pollenmenge, Herbst-Verlängerung) | Pollenintegral +20,9 % [9]; CO₂-Effekt Ambrosia +61…131 % [21,22]; Herbst-Spreizung der Kräuterpollen [6] | Beobachtung/Experiment | [6,9,21,22] | belegt, aber ohne DE-ERF je Zelle | — | **bewusst inaktiv** (Untergrenze; §6 Modellgrenze 1) | Log 4/14 |
| 96-W025-04 | E09 Trockenheit → Pollenfreisetzung/-transport | Wirkrichtung intensitätserhöhend; keine quantifizierte ERF | — | Rev.-5-Befund 52 | — | — | **bewusst inaktiv** | Log 14 |
| 96-W024-01 | W024 lokale allergene Vegetation → Symptomlast | \(\lambda\) = 0,7 (0,3–1,0); Kette §3.4: Fallen-Differenzen 245 %/306 % (14 Fallen Berlin; Zuwachs-Lesart ⇒ \(R\) = 3,45/4,06, Verhältnis-Lesart im Band) ⇒ \(\lambda_{\text{roh}}\) 1,10–1,21 × vegetationserklärter Anteil 0,6 (0,4–0,8) | Messreihen (Pollenfallen), Symptomgradient, Lidar-Studie | Werchan 2017 [54], Werchan 2018 [55], Bogawski 2019 [56] | Berlin/Posen; **gekennzeichnete Abschätzung** (§3.9) | OSM-Vegetation; Ebene POLLEN_LOAD **neu anzulegen** (§3.3) | **Basiswert** | Log 12 |
| 96-W024-02 | W024 Neophyten (Ambrosia) → Sensibilisierung | DE-Sensibilisierung 0–10 % → 15–25 % (2041–2060, 66 % klimabedingt); Kosten 193–1.190 Mio. €/a bei Voll-Etablierung | Projektion (Europa-Modell); Kostenmodell | Lake 2017 [23]; Hamaoui-Laguel 2015 [24]; Born 2012 [25] | Zeithorizont 2041–2060 ≠ M0-Ausweis „heute" | JKI-Fundkarten regional | **bewusst inaktiv** (Modul 96-B ab M1; §8-Verworfen-Liste) | Log 13 |
| 96-R35-01 | R35 Bevölkerung → Betroffene (Prävalenz) | \(p_{\text{AR},a}\): u20 8,8 % · 20–64 13,2 % · 65–74 6,7 % · 75–84 5,0 % · 85+ 5,0 % (12-Monats, ärztlich diagnostiziert; Herleitung §3.2) | bevölkerungsrepräsentative Surveys | DEGS1: Langen 2013, Tab. 3 [1]; KiGGS W2: Thamm 2018 [2]; Gewichte: Destatis 31.12.2023 [48] | DE; DEGS1 endet bei 79 (75+-Extrapolation gekennzeichnet) | Zensus-Altersbänder; Ebene u20 **neu anzulegen** (§3.2) | **Basiswert** | Log 10 |
| 96-R35-02 | Sensibilisierungsprofil der AR-Patienten (Birkengruppe/Gräser) | \(p_B\) = 0,55 (0,4–0,7) · \(p_G\) = 0,75 (0,6–0,85) | **gekennzeichnete Abschätzung** (§3.9); Stütze: Bevölkerungs-Sensibilisierung Gräser 19,4 % > Birke 17,4 % (Rangfolge) | Haftenberger 2013, Tab. 2/Abb. 1 [3] | Anteil *unter AR-Patienten* nicht direkt publiziert (Rev.-5-Befund 36a); Ersetzungspfad: PID-/Versorgungsdaten | national | **Basiswert** (Sensitivität §3.4) | Log 8 |
| 96-K1-01 | Behandlungskosten je Betroffenem und Jahr (direkt) | 210,3 €₂₀₁₄ (populationsbasiert, alle Schweregrade) ⇒ 266,90 €₂₀₂₄ (§3.5) | Bevölkerungs-Fragebogenstudie (n = 3.501) | Cardell 2016 (TOTALL) [65] | Schweden 18–65, Preisstand Feb. 2014 (CPI-adjustiert); Raumtransfer SE→DE 1:1 dokumentiert | national | **Basiswert** | Log 9 |
| 96-K1-02 | Behandlungskosten moderate–schwere SAR (direkt) | Erwachsene 42 % × 1.543 = 648 €₂₀₀₀ ⇒ 1.019 €₂₀₂₄; Kinder 60–78 % × 1.089 ⇒ 1.027–1.335 €₂₀₂₄ | Querschnitt (500 Patienten, fachärztlich) | Schramm 2003 [7] (Abstract-Zahlen primärverifiziert) | DE; **moderate–schwere** SAR — Überschätzungsrichtung je Durchschnittspatient | national | **Sensitivitätsband** (Obergrenze \(c_{\text{Tag}}\)) | Log 9 |
| 96-S158-01 | S158 Pollen-Frühwarnung → Symptomlast | keine quantifizierte Interventions-Effektgröße publiziert | — | DWD/PID-Gefahrenindex (Ebene) | — | kommunal | **Maßnahmen-Hebel (qualitativ)** | Log 15 |
| 96-R36-01 | R36 Gesundheitsinfrastruktur → AR-Outcome | keine Evidenz für Distanz-/Kapazitätseffekt auf ambulante AR-Behandlung | — | — | AR wird ambulant/selbstmediziert behandelt | HEALTHCARE_ACCESS (Schicht A) | **bewusst inaktiv** (Basiswert Default 1) | Log 16 |

## 3 Modell (§2.3) — Ansatz 96-A, Schicht B

**Native Ergebnisgröße (§3.6, deklariert): zusätzliche Symptomtage \(\Delta\text{Tage}\) je
Jahr** (klimaattribuiert). Teil-Ausweise unter der KWRA-Klammer: Betroffene \(B\), €.
Kein Mortalitätspfad (Konto-Einbettung Kap. 1).

**Gemeinsamer Preisstand aller Kostensätze dieses Berichts: €2024**; Umrechnungsfaktoren je
Satz in der Zeichentabelle (Destatis-VPI-Jahresmittel, 2020 = 100: 2000 = 75,9 · 2014 = 94,0 ·
2024 = 119,3 [19]).

### 3.1 Klimasignal: gemessene Saison-Spreizung ΔS (Anker `#delta-s`)

**Konstruktionsprinzip (Log 2):** Eine reine Parallel-**Verschiebung** der Pollensaison
erzeugt keine zusätzlichen Symptomtage — mehr Expositionstage entstehen nur, wenn die Saison
**länger** wird. Messbar ist das aus den DWD-Phänologie-Jahresmeldern als **Spreizung**
zwischen Saison-Markern (der RKI-Sachstandsbericht beschreibt genau diesen Mechanismus:
„Verfrühung der Baumpollen- und Verlängerung der Kräuterpollensaison … eine **Spreizung der
Pollensaison** — und damit eine Verlängerung [der Expositionszeit]" [6]):

$$ \Delta S_B \;=\; \overline{\bigl[J_{\text{Birke}} - J_{\text{Erle}}\bigr]}^{\,1991\text{–}2020} - \overline{\bigl[J_{\text{Birke}} - J_{\text{Erle}}\bigr]}^{\,1961\text{–}1990}, \qquad \Delta S_G \;=\; \Delta\overline{\bigl[J_{\text{Knäuelgras}} - J_{\text{Fuchsschwanz}}\bigr]} $$

\(J\) = Jultag des Phasen-Eintritts. **Birkengruppe** (Bet-v-1-Kreuzreaktivität
Hasel/Erle/Birke [6]): Front-Marker = **Erle Blüte Beginn** (= KWRA-Indikator GE-KL-07),
Kern-Marker = Birke; rückt die Erle stärker vor als die Birke, verlängert sich das
Symptomfenster der Birkengruppen-Patienten vorn. **Gräser:** Sukzessions-Spreizung
früh → spät (Wiesen-Fuchsschwanz → Wiesen-Knäuelgras, jeweils Vollblüte).

Messung (Skript `dwd_pollensaison.py` [67]; gepaarte Stationen mit ≥ 8 Spannen-Jahren in
**beiden** Normalperioden; Regionen wie #95 über das Bundesland, Log 5):

| Region | \(\Delta S_B\) [Tage] | n (Stationen) | \(\Delta S_G\) [Tage] | n | Sensitivität: Front ab Hasel |
|---|---|---|---|---|---|
| Nord | +3,96 | 257 | +4,78 | 200 | +8,14 |
| Mitte | +4,20 | 421 | +4,08 | 465 | +8,48 |
| Süd | +5,94 | 405 | +3,70 | 420 | +8,77 |
| Deutschland | +4,79 (SD 7,46; SE 0,23) | 1.083 | +4,06 (SD 5,98; SE 0,18) | 1.085 | +8,51 |

- **Birken-Marker = Phase 4 (Blattentfaltung)** statt Phase 5 (Blüte Beginn), weil Phase 5
  eine Meldelücke 1960–1990 hat (Log 3). Diagnose in den Überlappungsjahren: Offset
  Blüte − Blattentfaltung = +3,29 Tage (n = 46.027); Halbperioden-Trend 4,23 → 2,92 Tage —
  die Birkenblüte rückt relativ zur Blattentfaltung leicht vor, \(\Delta S_B\) ist damit um
  bis zu ≈ 1,3 Tage **überzeichnet** → ins Band aufgenommen (untere Bandgrenze).
- **Gräser-Saisonende konstant** (kein Phänologie-Marker für das Saisonende; Log 4): die
  belegte Herbst-Verlängerung der Kräuter-/Gräsersaison [6] ist **nicht** angesetzt —
  dokumentierte Untergrenze (§6).
- Plausibilisierung der Einzelart-Verfrühungen gegen die Literatur (Meta-CSV [67]):
  Hasel −14,6 · Erle −11,5 (= GE-KL-07) · Birke −6,4 Tage (Normalperiodenvergleich) —
  konsistent mit Endler 2020/KWRA TB5 („Hasel/Erle **bis zu** 26 Tage früher 1961–2017;
  Birke 1–1,5 Wochen") [4,5].

```python test: beispiel_96_spreizung_konsistenz
# Spreizung = Differenz der Einzelart-Verfruehungen (DE, gerundet auf Messgenauigkeit):
# Birke -6,4 vs. Erle -11,5 => Birkengruppe +5,1 (CSV: +4,79 — Stationspaarung differiert)
assert abs((-6.4) - (-11.5) - 5.1) < 0.01
# Graeser: -5,09 vs. -8,72 => +3,63 (CSV: +4,06 — Stationspaarung differiert)
assert abs((-5.09) - (-8.72) - 3.63) < 0.01
# Die CSV-Werte selbst (gepaarte Stationen) sind massgeblich:
de_b, de_g = 4.79, 4.06
assert 3.0 < de_b < 6.5 and 3.0 < de_g < 5.5
```

### 3.2 Betroffene je Zelle: altersspezifische Prävalenz (Anker `#p-ar`)

$$ B_{\text{Zelle}} \;=\; \sum_a \text{pop}_a \cdot p_{\text{AR},a} $$

**Konvention:** Die auf eine Nachkommastelle gerundeten Band-Prävalenzen sind die
verbindlichen Produktwerte (Registry `pollen.p_ar`); alle Summen dieses Berichts nutzen
sie (Befund 105).

**Bänder und Herleitung** (Rev.-5-Befunde 27/35): Das Produkt führt die Zensus-Bänder
u65/65–74/75–84/85+; für die Prävalenz-Schichtung wird zusätzlich die Ebene **u20 neu
angelegt** (Zensus-2022-Gitter, 10-Jahres-Klassen 0–9 + 10–19; §3.1-Kennzeichnung „neu
anzulegen"); das Band 20–64 ergibt sich je Zelle als u65 − u20.
**Ergebnis der Integration (31.08.2026):** Ebene `POPULATION_U20` **angelegt** —
der Zensus-Gitterdatensatz „Alter in 5er-Jahresgruppen" liegt bereits im Produkt;
u20 wird aus `unter5 + a5bis9 + a10bis14 + a15bis19` als **Binnenaufteilung der
u65-Menge** gebildet (dasselbe Zwei-Quellen-Prinzip wie bei den Senioren-Bändern:
die gut besetzte u65-Menge legt das Niveau fest, die Feingruppen nur die
Aufteilung; Rückfall Zelle → Gebiet → national 0,2407). Prävalenzwerte (12-Monats,
ärztlich diagnostiziert) aus DEGS1 Tab. 3 [1] und KiGGS W2 [2], bevölkerungsgewichtet auf
die Produktbänder (Gewichte: Bevölkerung 31.12.2023 nach Altersjahren [48]):

- **u20 = 8,8 %** (KiGGS W2, 0–17; die 18/19-Jährigen erhalten den Kinder- statt des
  höheren DEGS1-Werts 14,6 % — dokumentiert **unterschätzend**, Log 10).
- **20–64 = 13,2 %**: (9.301.783·14,6 + 10.947.845·17,2 + 10.275.235·14,3 + 12.293.757·10,1
  + 6.345.372·8,2) / 49.163.992 = 13,16 ≈ 13,2 % (DEGS1-Dekadenwerte 14,6/17,2/14,3/10,1;
  60–64 mit dem 60–69-Wert 8,2).
- **65–74 = 6,7 %**: (5.180.675·8,2 + 4.388.965·5,0)/9.569.640 = 6,73 (65–69 → 8,2;
  70–74 → 5,0).
- **75–84 = 5,0 %** (DEGS1 70–79; 80–84 = Extrapolation, gekennzeichnet).
- **85+ = 5,0 %** (Extrapolation über das DEGS1-Ende 79 hinaus, gekennzeichnet; Richtung
  unklar — Prävalenz fällt mit Alter, Untererfassung bei Hochaltrigen möglich).

```python test: beispiel_96_praevalenz_gewichtung
# p_AR 20-64 und 65-74: bevoelkerungsgewichtete DEGS1-Werte (Bev. 31.12.2023)
pop = {"20-29": 9_301_783, "30-39": 10_947_845, "40-49": 10_275_235,
       "50-59": 12_293_757, "60-64": 6_345_372, "65-69": 5_180_675, "70-74": 4_388_965}
p = {"20-29": 14.6, "30-39": 17.2, "40-49": 14.3, "50-59": 10.1, "60-64": 8.2,
     "65-69": 8.2, "70-74": 5.0}
g2064 = sum(pop[k]*p[k] for k in ["20-29","30-39","40-49","50-59","60-64"]) / \
        sum(pop[k] for k in ["20-29","30-39","40-49","50-59","60-64"])
g6574 = (pop["65-69"]*p["65-69"] + pop["70-74"]*p["70-74"]) / (pop["65-69"] + pop["70-74"])
assert abs(g2064 - 13.16) < 0.01
assert abs(g6574 - 6.73) < 0.01
# Bundes-Betroffene mit gerundeten Bandwerten:
band_pop = {"u20": 15_583_456, "20-64": 49_163_992, "65-74": 9_569_640,
            "75-84": 6_294_744, "85+": 2_844_213}
band_p   = {"u20": 8.8, "20-64": 13.2, "65-74": 6.7, "75-84": 5.0, "85+": 5.0}
betroffene = sum(band_pop[b]*band_p[b]/100 for b in band_pop)
# Konvention (Befund 105): die GERUNDETEN Band-Praevalenzen sind die verbindlichen
# Produktwerte (Registry pollen.p_ar); mit ihnen: 8.959.105 (= §4-Wert 8,96 Mio;
# ungerundete Gewichte ergaeben 8.944.994 — Abweichung < 0,2 %)
assert abs(betroffene - 8_959_105) < 1
```

### 3.3 Zusatztage und lokale Modulation (nativer Ausweis)

Zusätzliche Symptomtage je Betroffenem und Jahr (Region \(R\)):

$$ \delta_R \;=\; f \cdot \bigl( p_B\,\Delta S_{B,R} + p_G\,\Delta S_{G,R} \bigr) \cdot a_{\text{attr}} $$

$$ \Delta\text{Tage}_{\text{Zelle}} \;=\; B_{\text{Zelle}} \cdot \delta_R \cdot \hat P_{\text{Zelle}}, \qquad \hat P_{\text{Zelle}} \;=\; 1 + \lambda \cdot \bigl( \hat G_{\text{Zelle}}/\bar G - 1 \bigr) $$

- \(\hat P\) steht in **beiden** Pfaden (ΔTage **und** €) — natives Outcome und €-Wert
  bleiben strikt proportional (Rev.-5-Befund 12).
- **Zentrierung — Gewichtsregel und Bezugsebene definiert** (Befund 101; Log 17,
  **Rev. 2: Bezugsebene = die betrachtete Kommune**, Log 18; Anker `#p-hat`):
  \(\bar G\) ist das **betroffenengewichtete Mittel über die bewohnten Zellen der
  betrachteten Kommune**,

  $$ \bar G \;:=\; \frac{\sum_{\text{Zellen}} B_{\text{Zelle}} \cdot \hat G_{\text{Zelle}}}{\sum_{\text{Zellen}} B_{\text{Zelle}}} \qquad\Rightarrow\qquad \sum_{\text{Zellen}} B_{\text{Zelle}} \cdot \hat P_{\text{Zelle}} \;=\; \sum_{\text{Zellen}} B_{\text{Zelle}} \ \ \text{exakt}. $$

  Mit dieser Gewichtung ist die **Kommunensumme per Konstruktion invariant** gegen
  \(\lambda\) und gegen jede Korrelation zwischen \(\hat G\) und Bevölkerung — ein
  flächen- oder zellgewichtetes Mittel hätte diese Eigenschaft nicht (unbewohnte
  Waldzellen bzw. Stadtvegetation würden \(E_{\text{Betroffene}}[\hat P] \ne 1\)
  erzeugen und, da \(c_{\text{kal}} \equiv 1\) keinen Fit nachschaltet, die Summe
  direkt verschieben); die §4-Sanity-Rechnung (mit \(\hat P\)-Mittel = 1) gilt damit
  **exakt je Kommune**, \(\hat P\) verteilt ausschließlich **innerhalb** der Kommune um.

  **Warum die Kommune und nicht Deutschland die Bezugsebene ist** (Rev. 2, Log 18):
  (1) **Reichweite der Evidenz.** Der \(\lambda\)-Term ist ausschließlich aus
  **intra-urbanen** Messanordnungen abgeleitet — Werchan misst Unterschiede zwischen
  Standorten *innerhalb* Berlins (14 Pollenfallen [54]) bzw. den Symptomgradienten
  innerhalb derselben Stadt [55], Bogawski koppelt Baumkronen an lokale
  Konzentrationen [56]. Diese Evidenz trägt eine Umverteilung innerhalb einer Stadt;
  sie trägt **nicht** die Aussage, eine insgesamt grünere Kommune habe mehr
  Symptomtage als eine graue. Letzteres wäre ein unbelegter Skalentransfer — die
  interkommunalen Unterschiede stecken bereits in \(B_{\text{Zelle}}\) (Bevölkerung
  × altersspezifische Prävalenz) und in \(\Delta S_R\) (regional gemessen).
  (2) **Geschlossene Betrachtungsebene** (Aufgabe §3.2, Fortschreibung 31.08.2026):
  Ein Bundesmittel über alle Zellen wäre eine modellinterne Aggregation über eine
  **höhere Ebene als die Betrachtungsebene**; das Ergebnis einer Kommune hinge dann
  an Daten außerhalb ihrer selbst und wäre nur mit einem (per §3.4 unzulässigen)
  Bundeslauf bestimmbar. Beides entfällt: \(\bar G\) entsteht im Lauf aus den
  eigenen Zellen (`inputs.kommunale_pollen_referenz`).
  (3) **Konsequenz — ehrlich benannt, nicht beschönigt:** Die Vegetationsstruktur
  verschiebt die **Kommunensumme nicht**; \(\hat P\) ist **nullsummig
  umverteilend** (nicht „konservativ" im Sinne einer Unterschätzung — es ist
  betroffenengewichtet erwartungstreu). Der Ausweis differenziert damit **innerhalb**
  der Kommune (Hotspots an Alleen/Parks gegenüber vegetationsarmen Blöcken) und
  bleibt zwischen Kommunen bei dem, was Prävalenz und gemessenes Klimasignal
  hergeben. Für die Maßnahmen-Lesart siehe §5 und Modellgrenze 7 in §6.
  (4) **Fehlt die Referenz** (Zelle ohne Kommunen-Kontext, Alt-Daten), bleibt
  \(\hat P \equiv 1\) — **kein Ersatz-Bundeswert** (Aufgabe §3.2).
  (5) **Fallback der Ebene selbst** (§3.1): Eine Zelle ohne kartierte OSM-Kronen
  und ohne Grünfläche erhält \(\hat G = 0\) — das ist die inhaltlich richtige
  Lesart („keine allergene Vegetation kartiert"), kein fehlender Wert; sie
  bekommt damit das kleinstmögliche \(\hat P = 1-\lambda\) (bei \(\lambda\) = 0,7:
  0,3). **Proxy-Grenze, dokumentiert:** OSM-Baumkataster sind lückenhaft — eine
  unkartierte Zelle ist von einer vegetationsfreien nicht unterscheidbar; die
  Zentrierung fängt das teilweise auf (fehlen Kronen flächendeckend, sinkt
  \(\bar G\) mit). Richtung: In Kommunen mit schwacher OSM-Erfassung
  differenziert \(\hat P\) schwächer; die Kommunensumme bleibt unberührt. Ebenen-Definition: OSM-basierter Anteil allergener Gehölze
  (Birke/Erle/Hasel-anteilige Baumkronen-/Gehölzfläche) + Grünflächenanteil als
  Gräser-Proxy, **neu anzulegen** (§3.1) — die Gewichtsregel ist hiermit festgelegt,
  nur die Arten-/OSM-Detailspezifikation ist Integrationsumfang. **Referenzzustand — Befund 113 unter der Rev.-2-Konstruktion aufgelöst**
  (Log 19): \(\bar G\) wird in **jedem** Lauf aus dem dann gültigen
  Vegetationszustand der Kommune gebildet; ein „eingefrorener" Referenzwert wird
  **bewusst nicht** geführt. Begründung: Ein Pinning würde einem **flächigen**
  Vegetationsprogramm (alle Zellen gleichmäßig allergenärmer) einen
  **Niveaueffekt** auf die Kommunensumme zubuchen — und genau den trägt die
  \(\lambda\)-Evidenz nicht (intra-urbane Gradienten, s. o.; verstärkt durch
  Modellgrenze 2: Ferntransport entkoppelt lokale Vegetation und lokalen
  Pollenflug teilweise). Befund 113 war an das **Bundesmittel** gebunden, das
  ein solches Programm ohne Fixierung ebenfalls verschoben hätte; mit der
  kommunalen Zentrierung ist die Frage keine Fixierungs-, sondern eine
  **Evidenzfrage** — und sie ist mit „nicht buchbar" beantwortet (§5,
  Modellgrenze 7). **Produktseitige Konsequenz — als Anforderung, nicht als Beleg** (Befund 124):
  Das Maßnahmen-Modul rechnet \(\hat P\) nicht neu, sondern skaliert die
  gespeicherten Zell-Outcomes mit dem Wirkungsfaktor der Maßnahme
  (`measure_service._adjusted_cell_data`). Das ist **kein Nachweis** der
  Nicht-Buchbarkeit — im Gegenteil: Eine pauschal auf diesen Risiko-Code
  verknüpfte Maßnahme (`linked_risk_codes`) würde exakt den flächigen
  Niveaueffekt buchen, den Modellgrenze 7 für unbelegt erklärt. Daher gilt als
  **Integrationsauflage**: Für #96 ist **keine** pauschal wirkende Maßnahme
  verknüpft; eine künftige Verknüpfung darf nur den **Umverteilungsanteil**
  abbilden (zellscharfe Änderung von \(\hat G\) mit anschließender
  Neuberechnung), nie einen kommunenweiten Reduktionsfaktor. Testseitig
  gebunden: `test_no_flat_measure_on_allergy_days`.
  Bis zur Anlage der Ebene ist \(\hat P \equiv 1\) **kein zulässiger stiller Fallback** —
  die Ebene ist Teil des Integrationsumfangs (Kartenebenen-Pflicht §3.6).
  **Ergebnis der Integration (31.08.2026; §3.1-Anlagepflicht):** Ebene
  `POLLEN_LOAD` **angelegt**. Detailspezifikation (vom Bericht ausdrücklich der
  Integration überlassen): \(\hat G_z = w_B\,[k_{\text{Birke},z} +
  s_{\text{unbek}}\,k_{\text{unbek},z}] + (1-w_B)\,\text{Grün}_z\) — Kronenflächen
  aus OSM-Baumpunkten (`natural=tree`) mit Gattungs-Tag `genus`/`species`/`taxon`
  der Birkengruppe (*Betula/Alnus/Corylus/Carpinus*); Kronen **ohne** Gattungs-Tag
  (in OSM der Regelfall) gehen mit dem Anteil
  \(s_{\text{unbek}}\) = 0,12 ein (Registry `birch_group_share_default`).
  **§3.9-Kategorie ABGESCHÄTZT — keine Primärquelle:** Für den Gattungsmix
  ungetaggter OSM-Bäume gibt es keine belastbare offene Erhebung
  (Straßenbaumkataster sind kommunal, uneinheitlich, nicht keyless aggregierbar).
  Begründung des Zahlenwerts: Birke und Erle liegen in veröffentlichten
  kommunalen Straßenbaum-Erhebungen typischerweise im einstelligen
  Prozentbereich, Hasel/Hainbuche kommen in Grün- und Parkanlagen hinzu ⇒ 0,12
  mit Band 0,05–0,25. **Gemessene Ergebnis-Sensitivität** (Testzellen,
  s_unbek 0,05 → 0,25): \(\hat G/\bar G\) der gehölzreichen Zelle 0,571 → 0,643
  (+12,6 %), der grünlastigen 1,514 → 1,439 (−5,0 %); die **Kommunensumme bleibt
  unverändert** (Zentrierung), betroffen ist nur die Verteilung. Ersetzbar durch
  ein kommunales Baumkataster (Fortschreibungsvermerk); Gräser-Proxy = Grün-/Wiesenanteil der Zelle;
  Gewichte aus den δ-Beiträgen: \(w_B\) = 0,55·4,79/(0,55·4,79 + 0,75·4,06) =
  2,6345/5,6795 = **0,464**. Wie \(\bar G\) ist \(w_B\) **kein
  Registry-Parameter**, sondern eine im Lauf gerechnete abgeleitete Größe
  (`indicators.pollen_load`) — so bleibt die Kopplung an \(p_B\)/\(p_G\)
  lebendig (§3.9; Ledger-Befund 138). \(\bar G\) wird im Lauf
  aus den Zellen der jeweiligen Kommune gebildet (`inputs.kommunale_pollen_referenz`;
  Rev. 2, Log 18) — damit gilt \(\sum_z B_z \hat P_z = \sum_z B_z\) **exakt**
  (Golden-Test `test_reference_is_closed_within_the_kommune`) und die Betrachtungsebene
  bleibt geschlossen. Zur Plausibilisierung der Ebene dokumentiert das Skript
  `pollen_g_bar.py` (Anlagen `pollen_g_bar.csv`/`.md`) Größenordnung und Streuung von
  \(\hat G\) über drei Siedlungstypen: Offenbach am Main 0,174 · Freising 0,180 ·
  Weyarn 0,270 (2.896 bewohnte Zellen) — der Stadt-Land-Kontrast ist die erwartete
  Richtung und belegt, dass die Ebene misst, was sie soll.
- Werte je Region: \(\delta\) = **2,02 / 1,88 / 2,12** Tage je Betroffenem·Jahr (N/M/S;
  DE-gewichtet 1,99) mit den Basiswerten \(f\) = 0,70, \(p_B\) = 0,55, \(p_G\) = 0,75,
  \(a_{\text{attr}}\) = 0,50.
- **Saison-Fenster überlappen nicht:** \(\Delta S_B\) wirkt im Februar–April (Front der
  Birkengruppe), \(\Delta S_G\) im Mai–Juni (Gräser-Sukzession) — die Addition zählt keine
  Tage doppelt. (Zur Überlappung in \(d_{\text{Saison}}\) s. §3.5 — dort ist die additive
  Form €-konservativ; Rev.-5-Befund 36b.)

```python test: beispiel_96_delta_je_region
f, pB, pG, a = 0.70, 0.55, 0.75, 0.50
DS = {"nord": (3.96, 4.78), "mitte": (4.20, 4.08), "sued": (5.94, 3.70), "de": (4.79, 4.06)}
soll = {"nord": 2.017, "mitte": 1.880, "sued": 2.115, "de": 1.988}
for r, (db, dg) in DS.items():
    delta = f * (pB*db + pG*dg) * a
    assert abs(delta - soll[r]) < 0.002
```

### 3.4 Sensitivität der Basiswerte f, p_B/p_G, λ (Anker `#f-sympt`, `#p-sens`, `#lambda-veg`)

- **\(f\) = 0,70 (Band 0,50–0,85) — reine Modellannahme** (§3.9 „Abgeschätzt"; Log 7;
  Rev.-5-Befund 14): Anteil der Saisontage, an denen ein Patient symptomatisch/behandelnd
  ist. Die Pollen-Symptom-Korrelationen r = 0,48–0,79 (Pfaar 2020 [52]) stützen nur
  **qualitativ**, dass Pollenflug die Symptomlast treibt — sie sind **kein** Zahlenwert für
  \(f\) (Kategorienfehler der Rev. 5, behoben). Der von der Gegenprüfung benannte Kandidat
  Bastl 2020 [53] wurde im Volltext geprüft: die Studie vergleicht
  Symptom-Score-Berechnungsmethoden und publiziert **keinen** Anteil symptomatischer
  Saisontage — \(f\) bleibt Annahme mit Band und Ersetzungspfad (PHD-Tagesdaten).
  **Entlastung:** \(f\) kürzt sich im €-Pfad vollständig heraus (§3.5) und wirkt nur auf
  den nativen ΔTage-Ausweis (±29 % am Band).
- **\(p_B\) = 0,55 (0,4–0,7), \(p_G\) = 0,75 (0,6–0,85) — gekennzeichnete Abschätzung**
  (Log 8; Rev.-5-Befund 36a): benötigt wird der Anteil der AR-Patienten mit
  Birkengruppen- bzw. Gräser-relevanter Saison; publiziert sind nur
  Bevölkerungs-Sensibilisierungen (Haftenberger [3]: Gräserpollen 19,4 %, Birke 17,4 %,
  Erle 16,5 %, Hasel 16,2 % — Rangfolge Gräser > Birkengruppe konsistent zur Setzung).
  Sensitivität: ±0,15 auf \(p_G\) bzw. \(p_B\) verschiebt \(\delta\) um ±8 % bzw. ±6 %.
  Ersetzungspfad: PID-/Versorgungsdaten (Registry-Vermerk).
- **\(\lambda\) = 0,7 (0,3–1,0) — Herleitungskette** (Anker `#lambda-veg`; Befunde
  102/110): Werchan 2017 [54] misst über 14 Pollenfallen in Berlin die Spanne der
  Pollensedimentation zwischen höchstem und niedrigstem Standort; Original-Wortlaut
  (Abstract, primär verifiziert): „the observed **differences** between the trap with the
  overall highest and … lowest amount … were in the case of birch pollen **245 %**, grass
  pollen **306 %**“. **Lesart (dokumentiert, Befund 110):** Der Basiswert folgt der
  wörtlichen **Zuwachs**-Lesart (Differenz = 245 % des niedrigsten Werts ⇒ Verhältnis
  \(R_B\) = 3,45, \(R_G\) = 4,06); die in M0 verwendete **Verhältnis**-Lesart
  (\(R\) = 2,45/3,06) geht als untere Lesart ins Band ein — der Abstract-Wortlaut ist
  nicht eindeutig, eine Fundstelle im Volltext, die die Lesart entscheidet, steht aus
  (Ersetzungspfad). Unter einem linearen Gradienten zwischen den Extremstandorten ist die
  relative Spanne um den Mittelwert

  $$ \lambda_{\text{roh}} \;=\; \frac{R-1}{(R+1)/2} \;=\; \frac{2\,(R-1)}{R+1} \;=\; 1{,}10\ (R_B)\ \dots\ 1{,}21\ (R_G) \qquad (\text{Verhältnis-Lesart: } 0{,}84\dots1{,}01). $$

  Davon ist nur ein Teil durch die lokale Vegetation erklärt (Rest: Ferntransport, Wind):
  vegetationserklärter Anteil \(a_{\text{veg}}\) = 0,6 (0,4–0,8; **gekennzeichnete
  Abschätzung** §3.9) ⇒ \(\lambda\) = 1,10…1,21 × 0,6 = 0,66…0,73, **Basiswert 0,7**;
  Band **0,3–1,0** = Vereinigung beider Lesarten × \(a_{\text{veg}}\)-Band
  (0,84 × 0,4 = 0,34 … 1,21 × 0,8 = 0,97, gerundet). Die **Kommunensumme** ist gegen \(\lambda\)
  invariant (Ḡ-Gewichtung §3.3, Rev. 2) — die Lesart wirkt nur innerhalb der
  Kommune verteilend. Richtung unabhängig
  gestützt durch den Symptomgradienten Zentrum→Peripherie [55] und die
  Lidar-Birkendichte-Kopplung [56].
- **Altersinvarianz (explizite §3.2-Annahme; Befund 109):** \(f\), \(p_B/p_G\) und
  \(\lambda\) sind **altersinvariant** angesetzt („gleiche relative Elastizität über
  alle Bänder"); real sind Sensibilisierungsprofile altersabhängig — die Bänder decken
  diese Streuung, das absolute Altersmuster entsteht über \(p_{\text{AR},a}\)
  (für \(c_{\text{Tag}}\) ist die bandeinheitliche Vereinfachung in §3.5 dokumentiert).

### 3.5 Monetarisierung (K1) und Aggregation (Anker `#c-tag`, `#d-saison`)

$$ \text{€}_{\text{Zelle}} \;=\; \Delta\text{Tage}_{\text{Zelle}} \cdot c_{\text{Tag}}, \qquad c_{\text{Tag}} = \frac{c_{\text{Jahr,direkt}}}{d_{\text{Saison}}}, \qquad d_{\text{Saison}} = f \cdot \bigl( p_B L_B + p_G L_G \bigr), \qquad \text{Kommune} = \sum_{\text{Zellen}} $$

- **\(c_{\text{Jahr,direkt}}\) = 266,90 €₂₀₂₄** (Log 9): TOTALL [65] —
  bevölkerungsbasierte Stichprobe (Schweden, 18–65, alle Schweregrade): direkte Kosten
  **210,3 €** je Betroffenem·Jahr (Preisstand Feb. 2014, CPI-adjustiert laut Studie);
  Indexierung ×119,3/94,0 = ×1,2691 ⇒ 266,90 €₂₀₂₄. Raumtransfer Schweden→Deutschland 1:1
  als dokumentierte Annahme (vergleichbare Preisniveaus; ohne Kaufkraft-Korrektur — Band).
  **Warum nicht Schramm als Basis:** Schramm [7] misst **moderate–schwere**, fachärztlich
  behandelte SAR (Erwachsene direkt: 42 % × 1.543 = 648,1 €₂₀₀₀ ⇒ ×119,3/75,9 = **1.018,6
  €₂₀₂₄**; Kinder 60–78 % × 1.089 ⇒ 1.027–1.335 €₂₀₂₄) — auf **alle** 12-Monats-
  diagnostizierten Betroffenen angewendet wäre das eine bekannte Überschätzung um grob
  Faktor 4 und würde die Untergrenzen-Zusage verletzen (dieselbe Logik wie #95-Befund 62).
  Schramm bildet daher die **Obergrenze** des \(c_{\text{Tag}}\)-Bands und das Kinder-Band.
- **\(d_{\text{Saison}}\) = 0,70 × (0,55·30 + 0,75·60) = 43,05 Tage** je Betroffenem und
  Referenzsaison (Saisonlängen \(L_B\) = 30 (20–45), \(L_G\) = 60 (45–80) Tage — **gekennzeichnete
  Abschätzungen** (§3.9) typischer deutscher Saisonfenster **nach dem** EAACI-Saisonkriterium
  aus Pfaar 2017 [51]; die Quelle definiert das Kriterium (Pollenschwellen), publiziert
  aber keine festen Längenwerte — Bänder decken die Spannweite; Befund 111). Die additive Form zählt bei Doppelt-Sensibilisierten
  überlappende Mai-Wochen doppelt ⇒ \(d_{\text{Saison}}\) eher **überzeichnet** ⇒
  \(c_{\text{Tag}}\) eher **unterschätzt** ⇒ €-Pfad konservativ (Rev.-5-Befund 36b,
  dokumentiert statt korrigiert).
- **\(c_{\text{Tag}}\) = 266,90 / 43,05 = 6,20 €₂₀₂₄/Tag** (Band 6,20–23,66; Obergrenze =
  Schramm-Kette 1.018,6/43,05). Einheitlich über alle Altersbänder (Vereinfachung
  dokumentiert; Kinder-Schramm-Band liegt innerhalb der Obergrenze).
  **Produktverankerung** (Integration 31.08.2026): Maßgeblicher Produktwert ist
  \(c_{\text{Tag}}\) (editierbarer Kostensatz des Risikos, Default 6,20);
  \(c_{\text{Jahr,direkt}}\) ist der **Herleitungsschritt** dahinter und folgt
  implizit als \(c_{\text{Tag}} \cdot d_{\text{Saison,ref}}\) = 6,20 · 43,05 =
  266,91 € — die 1-Cent-Differenz zu 266,90 € ist reine Rundung des
  Cent-genauen Kostensatzes (+3,7·10⁻⁵ relativ, testgebunden). Ändert der
  Nutzer \(f\), \(p_B\), \(p_G\), \(L_B\) oder \(L_G\), läuft
  \(c_{\text{Tag}}\) über \(d_{\text{Saison}}\) mit (Kopplung §3.9,
  Golden-Tests `test_f_cancels_in_euro_path` /
  `test_cost_rate_follows_season_length_chain`).
- **Proxy-Kennzeichnung \(c_{\text{Tag}}\)** (§3.1: Durchschnitts-Kostensatz für einen
  spezifischen Fallmix; Befund 103) mit Richtungsdiskussion: **überschätzende Kanäle** —
  (a) TOTALL erfasst allergische Rhinitis insgesamt (inkl. perennialer AR), die
  Jahreskosten werden aber vollständig auf die 43,05 Pollensaisontage umgelegt;
  (b) Durchschnitts- statt Grenzkosten: fixe Jahreskomponenten (Diagnostik, Arztkontakt)
  skalieren nicht mit der Saisonlänge — der Kostensatz je *zusätzlichem* Tag liegt darunter.
  **Unterschätzende Kanäle** — (c) Betroffene = nur ärztlich Diagnostizierte
  (Selbstmedikation Nicht-Diagnostizierter fehlt in der Menge, deren Kosten in TOTALL
  anteilig enthalten sind); (d) schwedisches Preisniveau ohne Kaufkraft-Aufschlag.
  **Präzisierte Untergrenzen-Aussage:** die Untergrenzen-Eigenschaft des Gesamtausweises
  trägt die **Mengen-Seite** (ΔTage strukturell unterschätzend: Intensität, Herbst, E09,
  Ambrosia nicht angesetzt) — der **Kostensatz** ist ein zweiseitiges Band, dessen
  Basiswert die untere belegte Stütze (populationsbasiert) nutzt; ein
  Grenzkosten-\(c_{\text{Tag}}\) als echte Untergrenze ist mangels Quelle nicht
  herleitbar (dokumentierte Lücke; Ersetzungspfad: saisonale Kostenaufschlüsselung).
- **\(f\)-Kürzung:** \(\text{€} = B \cdot \frac{p_B \Delta S_B + p_G \Delta S_G}{p_B L_B + p_G L_G} \cdot a_{\text{attr}} \cdot \hat P \cdot c_{\text{Jahr,direkt}}\) — der weichste
  Parameter \(f\) beeinflusst den €-Ausweis **nicht**.

```python test: beispiel_96_kostenkette
# TOTALL 210,3 EUR_2014 -> EUR_2024; d_Saison; c_Tag; Schramm-Obergrenze (VPI [19])
c_jahr = 210.3 * 119.3 / 94.0
assert abs(c_jahr - 266.90) < 0.05
d_sais = 0.70 * (0.55*30 + 0.75*60)
assert abs(d_sais - 43.05) < 0.001
assert abs(c_jahr / d_sais - 6.20) < 0.01
schramm = 0.42 * 1543 * 119.3 / 75.9
assert abs(schramm - 1018.6) < 1.0
assert abs(schramm / d_sais - 23.66) < 0.02
kind_lo, kind_hi = 0.60 * 1089 * 119.3/75.9, 0.78 * 1089 * 119.3/75.9
assert abs(kind_lo - 1027) < 2 and abs(kind_hi - 1335) < 2
```

```python test: beispiel_96_f_kuerzung
# Der f-Parameter kuerzt sich im EUR-Pfad vollstaendig heraus
pB, pG, LB, LG, a, c = 0.55, 0.75, 30, 60, 0.50, 266.90
def euro_pro_betroffenem(f, dsB, dsG):
    delta = f * (pB*dsB + pG*dsG) * a          # Tage
    c_tag = c / (f * (pB*LB + pG*LG))          # EUR/Tag
    return delta * c_tag
e1 = euro_pro_betroffenem(0.50, 4.20, 4.08)
e2 = euro_pro_betroffenem(0.85, 4.20, 4.08)
assert abs(e1 - e2) < 1e-9
```

```python test: beispiel_96_beispielzelle
# Beispielzelle: 1.000 EW im Bundes-Altersmix, Region Mitte, P^=1
# Betroffene ~107,4; Delta-Tage ~202; EUR ~1.251/Jahr
pbar = 10.74 / 100          # gewichtete Bundes-Praevalenz (§3.2)
b = 1000 * pbar
delta_mitte = 0.70 * (0.55*4.20 + 0.75*4.08) * 0.50
dt = b * delta_mitte
assert abs(b - 107.4) < 0.1
assert abs(dt - 201.9) < 0.5
assert abs(dt * 6.20 - 1252) < 5
```

### 3.6 Zeichentabelle (alphabetisch; §3.2-Form)

| Zeichen | Name | Einheit | Wert / Herkunft |
|---|---|---|---|
| \(a\) | Altersband u20 · 20–64 · 65–74 · 75–84 · 85+ (u20 neu; 20–64 = u65 − u20) | — | Zensus-Altersbänder + neue Ebene u20 (§3.2) |
| \(a_{\text{attr}}\) | klimaattribuierter Anteil des Saisontrends | — | **0,50** (IQR 0,19–0,84) [9]; register:96-W025-02 |
| \(B_{\text{Zelle}}\) | Betroffene (aktive allergische Rhinitis) der Zelle | Personen | berechnet (§3.2) |
| \(c_{\text{Jahr,direkt}}\) | direkte Behandlungskosten je Betroffenem und Jahr (populationsbasiert) | €₂₀₂₄ | **266,90** = 210,3 €₂₀₁₄ × 119,3/94,0 (Band bis 1.018,6 = Schramm-Kette; Kinder 1.027–1.335) [7,19,65]; register:96-K1-01/-02; herleitung:#c-tag |
| \(c_{\text{Tag}}\) | Behandlungskostensatz je Symptomtag | €₂₀₂₄/Tag | **6,20** = 266,90/43,05 (Band 6,20–23,66); herleitung:#c-tag |
| \(d_{\text{Saison}}\) | Symptomtage je Betroffenem und Referenzsaison | Tage | **43,05** = 0,70 × (0,55·30 + 0,75·60); additive Form €-konservativ (§3.5); herleitung:#d-saison |
| \(\delta_R\) | zusätzliche Symptomtage je Betroffenem und Jahr, Region R | Tage/Jahr | **2,02/1,88/2,12** (N/M/S; DE 1,99); berechnet (§3.3) |
| \(\Delta S_{B,R},\ \Delta S_{G,R}\) | gemessene Saison-Spreizung Birkengruppe/Gräser je Region (1961–90 → 1991–2020) | Tage | 3,96/4,20/5,94 · 4,78/4,08/3,70 (N/M/S); `pollensaison_region.csv` [33,67]; register:96-W025-01; herleitung:#delta-s |
| \(\Delta\text{Tage}_{\text{Zelle}}\) | zusätzliche Symptomtage — **nativer Ausweis** | Tage/Jahr | Ergebnis |
| \(\text{€}_{\text{Zelle}}\) | bewerteter Schaden K1 (Ursache Allergene) — Teil-Ausweis | €₂₀₂₄/Jahr | Ergebnis = ΔTage × \(c_{\text{Tag}}\) (§3.5) |
| \(f\) | Anteil symptomatischer Saisontage | — | **0,70** (Band 0,50–0,85) — **Modellannahme** (§3.4; kürzt sich im €-Pfad); [52] nur qualitative Stütze; herleitung:#f-sympt |
| \(k_{\text{Birke},z},\ k_{\text{unbek},z}\) | Kronenflächenanteil der Zelle: sicher der Birkengruppe zugeordnet bzw. ohne Gattungs-Tag | — | OSM `natural=tree` mit `genus`/`species`/`taxon` (Betula/Alnus/Corylus/Carpinus) × Kronendurchmesser ÷ Zellfläche; Ebenen POLLEN_LOAD/CANOPY_BIRCH_FRACTION (§3.3); herleitung:#p-hat |
| \(\text{Grün}_z\) | Grün-/Wiesenflächenanteil der Zelle (Gräser-Proxy) | — | OSM-Landnutzung (vorhandene Produktgröße `green_frac`); herleitung:#p-hat |
| \(s_{\text{unbek}}\) | Birkengruppen-Anteil der Kronen **ohne** OSM-Gattungs-Tag | — | **0,12** (Band 0,05–0,25) — **§3.9 ABGESCHÄTZT, keine Primärquelle**: Straßenbaumkataster sind kommunal und nicht keyless aggregierbar; Begründung + gemessene Sensitivität in §3.3 (`#p-hat`). Wirkt nur auf die Verteilung, nicht auf die Kommunensumme (Zentrierung); herleitung:#p-hat |
| \(w_B\) | Gewicht der Gehölz-Komponente in \(\hat G\) (Gräser: \(1-w_B\)) | — | **0,464** = \(p_B\Delta S_{B,\text{DE}}/(p_B\Delta S_{B,\text{DE}} + p_G\Delta S_{G,\text{DE}})\) = 2,6345/5,6795 = 0,46386 (auf 3 NK gerundet); **abgeleitete Größe, kein Registry-Parameter** — im Lauf aus den aktuellen \(p_B\)/\(p_G\) gerechnet (`indicators.pollen_load`), damit die Kopplung §3.9 lebendig bleibt (Golden-Test bindet die Kette inkl. Override); herleitung:#p-hat |
| \(\hat G_{\text{Zelle}}/\bar G\) | Anteil allergener Vegetation, normiert auf das **Kommunenmittel** (Ebene POLLEN_LOAD) | — | OSM-Gehölz-/Grünstruktur; \(\bar G\) = betroffenengewichtetes Mittel der **eigenen Kommune** ⇒ Mittel = 1 per Konstruktion (§3.3, Rev. 2); herleitung:#p-hat |
| \(J\) | Jultag des Phaseneintritts (DWD-Phänologie) | Tag | DWD-CDC Jahresmelder [33] |
| \(L_B,\ L_G\) | Saisonlänge Birkengruppe/Gräser (nach EAACI-Kriterium) | Tage | **30** (20–45) / **60** (45–80) — gekennzeichnete Abschätzung §3.5 [51]; herleitung:#d-saison |
| \(\lambda\) | Gewicht der lokalen Vegetations-Modulation | — | **0,7** (0,3–1,0) = \(2(R-1)/(R+1)\) × \(a_{\text{veg}}\) — Kette §3.4 (Lesart dokumentiert), gekennzeichnete Abschätzung [54–56]; register:96-W024-01; herleitung:#lambda-veg |
| \(p_{\text{AR},a}\) | 12-Monats-Prävalenz allergische Rhinitis je Band | — | **8,8/13,2/6,7/5,0/5,0 %** (u20/20–64/65–74/75–84/85+); Gewichtung §3.2 [1,2,48]; register:96-R35-01; herleitung:#p-ar |
| \(p_B,\ p_G\) | Anteil der AR-Patienten mit Birkengruppen-/Gräser-Saison | — | **0,55** (0,4–0,7) / **0,75** (0,6–0,85) — gekennzeichnete Abschätzung (§3.4) [3]; register:96-R35-02; herleitung:#p-sens |
| \(\hat P_{\text{Zelle}}\) | lokaler Pollen-Hazard-Faktor (auf die **Kommune** zentriert; in ΔTage **und** €) | — | \(1+\lambda(\hat G/\bar G - 1)\); Spanne bei \(\hat G/\bar G\) = 0,5…1,5: 0,65…1,35; ohne Kommunen-Referenz \(\hat P \equiv 1\) (§3.3); berechnet |
| \(\text{pop}_a\) | Bevölkerung der Zelle je Band | Personen | Zensus 2022, 100 m (+ Ebene u20 neu); register:96-R35-01 |

### 3.7 Schicht A (getrennt; nie auf €-Pfaden)

Screening-Index über die kuratierte Kette: \(\hat H\)(W025: POLLEN_LOAD) ×
\(\hat E\)(R35: POPULATION_DENSITY / AGE_STRUCTURE) × \(\hat V\)(S158:
EARLY_WARNING_SYSTEMS; R36: HEALTHCARE_ACCESS);
\(\text{Index} = 100 \cdot \max_p (w_p \hat H_p \hat E_p \hat V_p)\)
(Worst-Pathway-Prinzip; Normierungen editierbar, testseitig von €-Pfaden getrennt).

## 4 Kalibrierung & Validierung (§2.4/§3.4)

**Kalibrierfaktor (Log 6):** \(c_{\text{kal}}\) **entfällt** (≡ 1) — **dokumentierte
Ausnahme** von der §3.4-Kalibrierfaktor-Regel: Anders als bei #95 (RKI-Jahresreihe
hitzebedingter Todesfälle) existiert für klimaattribuierte Allergie-Morbidität **keine
amtliche Anker-Zeitreihe**, gegen die ein Niveau-Skalar gefittet werden könnte; die
Bundesregierung bestätigt, dass J30-scharfe Krankheitskosten nicht vorliegen
(BT-Drs. 19/22797, Antwort zu Frage 5 [66]). Das Modell ist stattdessen vollständig
messungs- und prävalenzverankert: \(\Delta S\) amtlich gemessen (DWD), \(p_{\text{AR}}\)
amtlicher Survey (RKI), \(c_{\text{Jahr}}\) populationsbasiert [65]. **Kalibriermodell =
Produktionsmodell** ist trivial erfüllt (lineares Modell ohne Fit-Schritt; kein
Näherungslauf involviert).

**Sanity-Bänder (Unter- und Obergrenze; Rev.-5-Befund 49):**

- **Physisch (native Größe):** Untergrenze > 0 ist **messfest**: \(\Delta S_B\) DE
  = +4,79 Tage (SE 0,23; 1.083 Stationen), \(\Delta S_G\) = +4,06 (SE 0,18) — beide
  hochsignifikant von 0 verschieden. \(\delta\)-Band aus dem Attributions-IQR:
  0,76–3,34 Tage je Betroffenem·Jahr (Basis 1,99). Externe Obergrenzen-Plausibilisierung:
  Anderegg [9] misst +8 Tage Saisonlänge (Nordamerika, ~30 Jahre) — klimaattribuiert ≈
  4 Tage; unsere angesetzten 1,99 Tage je Patient (mit Sensibilisierungs-Gewichten < 1)
  liegen **darunter** ⇒ konservativ konsistent.
- **Monetär:** Bundessumme = 8,96 Mio. Betroffene × 1,99 Tage × 6,20 € ≈ **110 Mio.
  €₂₀₂₄/Jahr** (Band ≈ 42–186 Mio. über den Attributions-IQR; obere
  \(c_{\text{Tag}}\)-Sensitivität 23,66 € ⇒ ≈ 420 Mio.). Einordnung gegen amtliche Rahmen:
  impliziter Klimaanteil an den AR-Behandlungskosten = \(\delta/d_{\text{Saison}}\) =
  1,99/43,05 = **4,6 %** — innerhalb des publizierten Bands klimaattribuierter
  Allergiekosten-Anteile (≈ 3–20 %, M0-Herleitung aus \(\Delta S/S\)-Trends × Attribution
  [4–6,9]); Bundessumme ≪ Krankheitskosten des J-Kapitels (16,5 Mrd. €, KKR 2015 [66]) und
  deutlich unter dem Asthma-Vergleichswert (1,9 Mrd. €, KKR 2015 [66]). Eine amtliche
  **J30-Untergrenze existiert nicht** — dokumentierte Datenlücke mit Beleg [66]
  (Ersetzungspfad: exakte J30-Beträge aus GENESIS 23631/GBE-Bund interaktiv ziehen,
  Registry-Vermerk vor Integration).
- **Impliziter Baseline-Check:** Betroffene × \(c_{\text{Jahr,direkt}}\) = 8,96 Mio ×
  266,90 € ≈ 2,39 Mrd. €₂₀₂₄ als implizite AR-Behandlungskosten-Basis — plausible
  Größenordnung zwischen Asthma-KKR (1,9 Mrd. [66]) und J-Kapitel (16,5 Mrd. [66]);
  mit der Schramm-Obergrenze wären es 9,1 Mrd. — erkennbar zu hoch, bestätigt die
  Basiswert-Wahl (Log 9).

```python test: beispiel_96_bundessumme
betroffene = 8_959_105          # §3.2-Konvention: gerundete Band-p (verbindliche Produktwerte)
delta_de   = 0.70 * (0.55*4.79 + 0.75*4.06) * 0.50
dt = betroffene * delta_de
assert abs(delta_de - 1.988) < 0.002
assert abs(dt / 1e6 - 17.8) < 0.1                    # 17,8 Mio Symptomtage/Jahr
assert abs(dt * 6.20 / 1e6 - 110) < 2                # ~110 Mio EUR_2024/Jahr
assert abs(delta_de / 43.05 * 100 - 4.62) < 0.05     # impliziter Klimaanteil 4,6 %
assert 0.03 <= delta_de / 43.05 <= 0.20              # im publizierten a_klima-Band
```

- **Verteilschlüssel-Test (§3.1):** strikt bottom-up — Zelle ohne Bevölkerung → 0;
  \(\Delta S\) ist je Region **gemessen** (kein Deutschland-Nenner, keine Indexmasse);
  \(\hat P\) mittelwertzentriert. **Anders als der #95-Morbiditätssockel ist ΔTage
  vollständig klimaattribuiert — es existiert kein bevölkerungsproportionaler Sockel; der
  Lackmustest gilt hier uneingeschränkt** (eine Kommune in einer Region ohne gemessene
  Saison-Spreizung erhielte ~0).
- **Unabhängige Verteilungsprüfung:** Die kritischste Achse ist das **Klimasignal je
  Region** (nicht die Altersverteilung — die folgt konstruktiv DEGS1 und wäre als Prüfung
  zirkulär, dokumentiert): Einzelart-Verfrühungen aus den eigenen gepaarten Stationen
  gegen unabhängig publizierte Werte: Hasel −14,6 Tage (Endler/KWRA: „bis zu 26" als
  Stationsspitzen, Mittel darunter — konsistent), Birke −6,4 (Endler: 1–1,5 Wochen für
  1991–2017 — konsistent), Vorfrühlings-Verschiebung DWD ≈ −17 Tage [5] als Rahmen ✓.
  Regionale Streuung der \(\Delta S\)-Werte gering (±20 % um das Bundesmittel) —
  die Zellverteilung wird von \(\text{pop} \times p_{\text{AR}} \times \hat P\) dominiert.
  **Toleranzen je Referenz (vorab fixiert, nur Referenzen mit definierter
  Vergleichsgröße; Befund 108):** (a) früheste Frühblüher (Hasel) gegen die
  DWD-Vorfrühlings-Verschiebung −17 Tage (Normalperiodenvergleich [5]): Toleranz ±50 %
  ⇒ Fenster 8,5–25,5 Tage; Ist **14,6 ✓**. (b) Birke gegen Endler 1–1,5 Wochen
  (7–10,5 Tage, Zeitraum 1991–2017 [4]; Fensterdifferenz dokumentiert): Toleranz ±50 %
  der Spannengrenzen ⇒ 3,5–15,8 Tage; Ist **6,4 ✓**. (c) „Hasel/Erle bis zu 26 Tage"
  [4] ist ein Stationsspitzen-Wert („bis zu") und dient nur als Obergrenzen-Rahmen:
  Ist 14,6/11,5 < 26 ✓ — kein Spannen-Test.
- **Unsicherheiten:** Marker-Approximation Birke Phase 4 (≤ 1,3 Tage, im Band);
  Phänologie ≠ Pollenflug (Ferntransport [6]); \(f\)/\(p_B\)/\(p_G\)-Bänder (§3.4);
  Attribution Nordamerika→DE; Raumtransfer der TOTALL-Kosten; kein flächiges
  Pollenmessnetz (\(\hat P\) bleibt Proxy).

## 5 Maßnahmen-Hebel (§2.5/§3.5)

- **Allergenarme Stadtbaumwahl (W024-Pfad):** Wirkungsort **definiert**: senkt
  \(\hat G_{\text{Zelle}}\) — multiplikativ via \(\hat P = 1+\lambda(\hat G/\bar G-1)\)
  auf ΔTage **und** € (marginal, zellscharf). Die Effektgröße ist **mechanisch**: ein
  Pflanzprogramm, das den allergenen Gehölzanteil einer Zelle **relativ zur Kommune**
  um Δ\(\hat G/\bar G\) = −0,2 senkt, reduziert die Last **dieser Zelle** um
  \(\lambda \times 0{,}2\) = 14 % (Band 6–20 % über das λ-Band); Artenwahl nach
  GALK-/allergologischer Liste [6].
  **Reichweite des Hebels (Rev. 2, Log 19):** Buchbar ist die **Umverteilung** —
  ein Programm, das gezielt die belasteten Zellen entschärft (Hotspots an
  Alleen/Parks in dicht bewohnten Blöcken), verschiebt Symptomtage von vielen
  Betroffenen zu wenigen und senkt damit den kommunalen Ausweis. Ein **flächiges**
  Programm, das alle Zellen gleichmäßig allergenärmer macht, ändert
  \(\hat G/\bar G\) nicht und ist damit **nicht als Niveaueffekt buchbar** — die
  λ-Evidenz (intra-urbane Gradienten) trägt keine Aussage über das Pollenniveau
  einer ganzen Stadt, und Ferntransport entkoppelt lokale Vegetation und lokalen
  Pollenflug zusätzlich (Modellgrenze 2/7). Das ist eine **Evidenz-**, keine
  Modellierungsgrenze; sie ist mit einer Emissions-/Ausbreitungs-Evidenz
  auflösbar (Ersetzungspfad, §6). Evidenz-Charakter: die
  Vegetations-Symptom-Kopplung ist beobachtend belegt [54–56] — **kein**
  Interventions-RCT; als mechanischer Hebel mit gekennzeichneter Effektkette geführt
  (Doppelzählungs-Wächter: wirkt nur über \(\hat G\), kein zweiter Vegetationskanal).
- **Pollenmonitoring / Frühwarnung (S158): qualitativ** (§3.5-Regel: Hebel ohne
  quantifizierte Effektgröße laufen ehrlich als „qualitativ"; Rev.-5-Befunde 26/34):
  keine publizierte Interventions-Effektgröße für Einführung/Ausbau kommunaler
  Pollen-Frühwarnung auf Symptomtage; Ebene EARLY_WARNING_SYSTEMS (DWD/PID-Gefahrenindex)
  wird als Screening-/Informationsebene geführt, im Basiswert Default 1.
- **R7-Weiche:** nicht einschlägig — keine Vorsorge-Buchung berührt (#96 hat keine
  K8-Gegenbuchung in der Netzwerkliste); Stadtbaum-Programmkosten sind kommunale
  Maßnahmenkosten außerhalb der Schadenskonten (Anzeige im Maßnahmen-Modul, keine
  K-Buchung).

## 6 Szenario-Anwendung & Modellgrenzen (§3.2/§3.6)

**Szenario-Anwendung 96-A:** Verschoben wird ausschließlich das Klimasignal
\(\Delta S_{B/G,R}\) (Fortschreibung der Phänologie-Reihen bzw. GE-KL-07-Projektion:
Blühbeginn Erle ≈ 2 Wochen früher bis 2100, RCP8.5 [15]; die Spreizungs-Projektion
erfordert artdifferenzierte Phänologie-Modelle — Stufe M1+). Konstant gehalten:
Prävalenzen, \(f\), \(p_B/p_G\), \(\lambda\), Kostensätze, Bevölkerung.
**Stationaritätsannahmen (dokumentiert):** (1) Sensibilisierungs-Prävalenzen stationär —
gegenläufige Evidenz (Neophyten [23], CO₂ [21,22]) macht das zur Untergrenze;
(2) konstantes \(a_{\text{attr}}\). **M0 weist das Ist-Klima aus** (Normalperiodenvergleich
1961–90 → 1991–2020); Szenariofähigkeit folgt mit der Klimaprojektions-Anbindung.

**Modellgrenzen (dokumentiert):**
1. **Nur Saisonlängen-Effekt:** Intensitätszunahme (Pollenintegral +20,9 % [9], CO₂-Effekte
   [21,22]), Herbst-Verlängerung der Kräuterpollensaison [6] und Trockenheits-Pfad (E09)
   sind bewusst nicht angesetzt — strukturelle **Untergrenze** (Register 96-W025-03/-04).
2. Phänologie ≠ Pollenflug: Ferntransport kann Saisonstart vor Ort vorziehen [6]; die
   Marker-Spreizung misst die lokale Blühsukzession.
3. \(\hat P\) bleibt Proxy (kein flächiges Pollenmessnetz); Ebene POLLEN_LOAD neu.
4. Birken-Marker Phase 4 (Offset-Trend ≤ 1,3 Tage, ins Band aufgenommen, §3.1).
5. Attributions-Übertrag Nordamerika→DE (IQR 0,19–0,84 als Band ausgewiesen).
6. Kostensatz: **Proxy** (§3.5) — Umlage der Jahreskosten (inkl. perennialer AR) auf
   Saisontage und Durchschnitts- statt Grenzkosten wirken überschätzend, ausgelassene
   Selbstmedikation Nicht-Diagnostizierter und fehlender Kaufkraft-Aufschlag
   unterschätzend; Raumtransfer SE→DE; Schweregrad-Mix (TOTALL populationsbasiert =
   Basis; Schramm moderate–schwer = Obergrenze); exakte deutsche J30-KKR-Werte nicht
   regulär publiziert [66].
7. **Kein flächiger Vegetations-Niveaueffekt** (Rev. 2, Log 18/19): \(\hat P\) ist
   auf die eigene Kommune zentriert und damit **nullsummig umverteilend** — die
   Vegetationsstruktur differenziert *innerhalb* der Kommune, verschiebt aber deren
   Summe nicht. Ein flächiges Pflanzprogramm ist deshalb **nicht** als Niveaueffekt
   buchbar (§5). Grund ist die Reichweite der λ-Evidenz (intra-urbane Gradienten
   [54–56]), nicht die Modellform; Ferntransport (Modellgrenze 2) stützt die
   Zurückhaltung. **Ersetzungspfad:** eine Emissions-/Ausbreitungs-Evidenz
   (Pollenquellstärke je Vegetationsfläche × Ausbreitungsmodell) würde einen
   quantifizierten Niveaueffekt tragen und wäre dann ein eigener, zu belegender
   Modellterm — bis dahin bleibt die Kommunensumme vegetationsunabhängig.

**Infokasten-/UI-Texte (§3.6 — Teil des Berichts):**

> **Infokasten 1 — am Gesamtwert:** „Dieser Wert ist der *bewertete Schaden im Konto K1
> Gesundheit (Ursache: Allergene)* (Modellstand M0). Er umfasst die klimabedingt
> zusätzlichen Behandlungs­kosten der Pollenallergie — nicht enthalten sind u. a.
> Arbeitsausfall und Produktivität (folgt in Stufe M3), die Zunahme der Pollen*intensität*
> sowie neue allergene Arten wie Ambrosia (spätere Stufen). Der ausgewiesene Betrag ist
> deshalb eine bewusste **Untergrenze**; er wird mit jeder Ausbaustufe vollständiger — nie
> kleiner. Berechnet mit Modellstand M0, Stand ⟨Datum⟩."
>
> **Infokasten 2 — an der nativen Größe:** „Wir weisen zusätzliche Symptomtage aus: Tage,
> an denen Pollenallergikerinnen und -allergiker wegen der klimabedingt verlängerten
> Pollensaison zusätzlich Beschwerden haben. Die Saisonverlängerung ist aus über 1.000
> DWD-Phänologie-Stationen gemessen (Vergleich der Klimanormalperioden 1961–1990 und
> 1991–2020), nicht geschätzt."
>
> **Pflicht-Elemente:** Benennung „bewerteter Schaden — Konto K1 (Ursache: Allergene)"
> (nie „Gesamtschaden"); Vollständigkeitsanzeige „Stufe M0: 1 von 8 Konten aktiv" mit
> Roadmap-Aufklappliste; Versionsstempel „berechnet mit Modellstand M0 — Untergrenze".

**Raten-Darstellung und Aggregation** (§3.6): Kartenausweis als **Raten** — nativ:
**zusätzliche Symptomtage je 1.000 EW und Jahr**; Teil-Ausweise: Betroffene je 1.000 EW,
€ je EW und Jahr; dazu die aggregierte Darstellungsebene **Quartier/Gemeindeteil**
(bestehende Aggregat-Mechanik); Kommune = Summe der Zellen bleibt die Rechenebene.
Kartenebenen: POLLEN_LOAD (neu), Saisonsignal \(\Delta S_R\) (regional, als Ebene
sichtbar), ΔTage-Rate (Ergebnis).

## 7 Parameter-Blöcke (maschinenlesbar, §4)

```yaml
parameter:
  id: pollen.delta_s_region
  wert: "backend/data/kalibrierung/pollensaison_region.csv"
  einheit: "Tage"
  band: null   # SD/SE je Zeile in der CSV; Birke-Marker-Offset bis -1,3 d (§3.1)
  herkunft: register:96-W025-01
  quelle: dwd_cdc_phaenologie_jahresmelder
  preisstand: null
  bandzuordnung: [u20, 20-64, 65-74, 75-84, 85+]
  endpunkt: morbiditaet
parameter:
  id: pollen.a_attr
  wert: 0.50
  einheit: "-"
  band: [0.19, 0.84]
  herkunft: register:96-W025-02
  quelle: anderegg2021
  preisstand: null
  bandzuordnung: [u20, 20-64, 65-74, 75-84, 85+]
  endpunkt: morbiditaet
parameter:
  id: pollen.p_ar
  wert: {u20: 0.088, 20-64: 0.132, 65-74: 0.067, 75-84: 0.050, 85+: 0.050}
  einheit: "-"
  band: null   # 75+/85+ Extrapolation ueber DEGS1-Ende 79 (gekennzeichnet, §3.2)
  herkunft: register:96-R35-01
  quelle: langen2013_thamm2018_destatis2023
  preisstand: null
  bandzuordnung: [u20, 20-64, 65-74, 75-84, 85+]
  endpunkt: morbiditaet
parameter:
  id: pollen.p_sens_gruppen
  wert: {birkengruppe: 0.55, graeser: 0.75}
  einheit: "-"
  band: {birkengruppe: [0.4, 0.7], graeser: [0.6, 0.85]}   # gekennzeichnete Abschaetzung §3.4
  herkunft: register:96-R35-02
  quelle: haftenberger2013
  preisstand: null
  bandzuordnung: [u20, 20-64, 65-74, 75-84, 85+]
  endpunkt: morbiditaet
parameter:
  id: pollen.l_saison
  wert: {birkengruppe: 30, graeser: 60}
  einheit: "Tage"
  band: {birkengruppe: [20, 45], graeser: [45, 80]}   # gekennzeichnete Abschaetzung nach EAACI-Kriterium (§3.5, Befund 111)
  herkunft: herleitung:#d-saison
  quelle: pfaar2017_eaaci
  preisstand: null
  bandzuordnung: [u20, 20-64, 65-74, 75-84, 85+]
  endpunkt: morbiditaet
parameter:
  id: pollen.f_symptomtage
  wert: 0.70
  einheit: "-"
  band: [0.50, 0.85]   # Modellannahme (§3.4); kuerzt sich im EUR-Pfad; nur nativer Ausweis
  herkunft: herleitung:#f-sympt
  quelle: modellannahme_pfaar2020_qualitativ
  preisstand: null
  bandzuordnung: [u20, 20-64, 65-74, 75-84, 85+]
  endpunkt: morbiditaet
parameter:
  id: pollen.lambda_veg
  wert: 0.7
  einheit: "-"
  band: [0.3, 1.0]   # Vereinigung beider Prozent-Lesarten x a_veg-Band (§3.4, Befund 110)
  herkunft: register:96-W024-01
  quelle: werchan2017_werchan2018_bogawski2019
  preisstand: null
  bandzuordnung: [u20, 20-64, 65-74, 75-84, 85+]
  endpunkt: morbiditaet
parameter:
  # Baustein der Ebene POLLEN_LOAD (Detailspezifikation der Integration, §3.3).
  # w_B ist KEIN Parameter-Block: als abgeleitete Größe (p_B*dS_B,DE / Summe)
  # wird es im Lauf gerechnet (indicators.pollen_load) — ein Registry-Wert
  # haette die Kopplung an p_B/p_G tot gestellt (Ledger-Befund 138).
  id: pollen.s_unbekannt
  wert: 0.12     # Birkengruppen-Anteil der OSM-Kronen OHNE genus/species-Tag
  einheit: "-"
  band: [0.05, 0.25]   # §3.9 ABGESCHAETZT: keine Primaerquelle (s. #p-hat)
  herkunft: herleitung:#p-hat
  quelle: modellannahme   # bewusst KEIN Quellen-Key: es gibt keine Primaerquelle
  preisstand: null
  bandzuordnung: [u20, 20-64, 65-74, 75-84, 85+]
  endpunkt: morbiditaet
parameter:
  id: pollen.c_jahr_direkt
  wert: 266.90
  einheit: "EUR/Jahr"
  band: [266.90, 1018.6]   # Obergrenze Schramm (moderate-schwere SAR); Kinder 1027-1335
  herkunft: register:96-K1-01
  quelle: cardell2016_totall_schramm2003
  preisstand: "2024"
  bandzuordnung: [u20, 20-64, 65-74, 75-84, 85+]
  endpunkt: morbiditaet
parameter:
  id: pollen.d_saison
  wert: 43.05
  einheit: "Tage"
  band: null   # = f x (p_B L_B + p_G L_G); additive Form EUR-konservativ (§3.5)
  herkunft: herleitung:#d-saison
  quelle: pfaar2017_eaaci
  preisstand: null
  bandzuordnung: [u20, 20-64, 65-74, 75-84, 85+]
  endpunkt: morbiditaet
parameter:
  id: pollen.c_tag
  wert: 6.20
  einheit: "EUR/Tag"
  band: [6.20, 23.66]
  herkunft: herleitung:#c-tag
  quelle: cardell2016_totall
  preisstand: "2024"
  bandzuordnung: [u20, 20-64, 65-74, 75-84, 85+]
  endpunkt: morbiditaet
```

## 8 Quellen (§3.8 — #96-relevanter Auszug; Nummern [1]–[56] = M0-Zählung, [65]–[67] neu)

Zugriff 17./18.08.2026 ([1]–[3], [65], [66]: 30.08.2026, Volltext/Abstract gegengelesen).
**Archiv-Snapshots:** wie #95 (Kap. 8) — deterministisch über die `sources.py`-Ratchet-
Mechanik bei Integration; bis dahin sind DOI-/amtliche Links die persistenten Referenzen.

- **[1]** U. Langen, R. Schmitz, H. Steppuhn, „Häufigkeit allergischer Erkrankungen in
  Deutschland (DEGS1)", Bundesgesundheitsbl 56(5–6):698–706, 2013. doi:10.1007/s00103-012-1652-7
  — **Tab. 3** (12-Monats-Prävalenz Heuschnupfen gesamt: 14,6/17,2/14,3/10,1/8,2/5,0 % für
  18–29/30–39/40–49/50–59/60–69/70–79; gesamt 12,0 %; Volltext gegengelesen 30.08.2026).
- **[2]** R. Thamm u. a., „Allergische Erkrankungen bei Kindern und Jugendlichen in
  Deutschland (KiGGS Welle 2)", J Health Monit 3(3):3–18, 2018. doi:10.17886/RKI-GBE-2018-075
  (12-Monats-Prävalenz Heuschnupfen 0–17: 8,8 %).
- **[3]** M. Haftenberger u. a., „Prävalenz von Sensibilisierungen gegen Inhalations- und
  Nahrungsmittelallergene (DEGS1)", Bundesgesundheitsbl 56(5–6):687–697, 2013.
  doi:10.1007/s00103-012-1658-1 — Tab. 2/Abb. 1: Gräserpollen 19,4 %, Birke 17,4 %,
  Erle 16,5 %, Hasel 16,2 %, Inhalationsallergene (SX1) 33,6 % (Volltext gegengelesen).
- **[4]** C. Endler (2020), Phänologie-Auswertung zit. n. KWRA 2021 Teilbericht 5, S. 174
  (Hasel/Erle bis 26 Tage früher 1961–2017; Birke/Gräser 1–1,5 Wochen 1991–2017),
  umweltbundesamt.de (lokal: `docs/KWAR/kwra2021_teilbericht_5_cluster_wirtschaft_gesundheit_bf_211027_0.pdf`, S. 174).
- **[5]** DWD, „Thema des Tages: Frühlingsbeginn — phänologische Uhr", 19.03.2023, dwd.de
  (Vorfrühling 3. März → 14. Februar; Vegetationsruhe 120 → 101 Tage, Normalperioden);
  DWD Nationaler Klimareport, 6. Aufl. 2022.
- **[6]** K.-C. Bergmann u. a., „Auswirkungen des Klimawandels auf allergische Erkrankungen
  in Deutschland", J Health Monit 8(S4):82–110, 2023 (RKI-Sachstandsbericht Klimawandel und
  Gesundheit). doi:10.25646/11648 — Spreizungs-Mechanismus wörtlich (S. 12 f.:
  „Spreizung der Pollensaison … Verlängerung [der Expositionszeit]"); Birkenpollengruppe;
  Ferntransport; GALK-/Artenlisten (Volltext gegengelesen 30.08.2026).
- **[7]** B. Schramm u. a., „Cost of illness of atopic asthma and seasonal allergic
  rhinitis in Germany: 1-yr retrospective study", Eur Respir J 21(1):116–122, 2003.
  doi:10.1183/09031936.03.00019502 — Abstract primärverifiziert (NCBI E-Utilities,
  30.08.2026): SAR 1.089 €/Kind · 1.543 €/Erwachsenem p. a.; Kinder 60–78 % direkte
  Kosten; Erwachsene 58 % indirekt (⇒ 42 % direkt).
- **[8]** T. Zuberbier u. a., „Economic burden of inadequate management of allergic
  diseases in the EU: a GA²LEN review", Allergy 69(10):1275–1279, 2014.
  doi:10.1111/all.12470 (indirekte Kosten — bleibt per R9 bei K2/#87).
- **[9]** W. R. L. Anderegg u. a., „Anthropogenic climate change is worsening North
  American pollen seasons", PNAS 118(7):e2013284118, 2021. doi:10.1073/pnas.2013284118
  (Saisonbeginn ≈ −20 Tage, Länge +8 Tage, Pollenintegral +20,9 %; ≈ 50 % [19–84 %] des
  Saisontrends anthropogen).
- **[10]** C. Ziello u. a., „Changes to Airborne Pollen Counts across Europe", PLoS ONE
  7(4):e34076, 2012. doi:10.1371/journal.pone.0034076
- **[15]** UBA (Hrsg.), KWRA 2021, Teilbericht 5 (CC 26/2021), Kap. 4.2.2 (Aeroallergene;
  GE-KL-07-Projektion ≈ 2 Wochen früher bis 2100, RCP8.5), umweltbundesamt.de (lokal:
  `docs/KWAR/`).
- **[19]** Destatis, VPI für Deutschland, lange Reihen (2020 = 100): 2000 = **75,9** ·
  2014 = **94,0** · 2023 = 116,7 · 2024 = 119,3 (Statistischer Bericht „VPI lange Reihen",
  destatis.de; Werte gegen die publizierte Basis-2020-Tabelle geprüft 30.08.2026).
- **[20]** Destatis, Krankheitskostenrechnung (Berichtsjahre 2015/2020/2023; GENESIS-Tabellen
  23631-0001/-0003, www-genesis.destatis.de); J30-scharfe Beträge nur interaktiv abrufbar —
  dokumentierte Lücke, s. [66].
- **[21]** P. Wayne u. a., Ann Allergy Asthma Immunol 88:279–282, 2002.
  doi:10.1016/S1081-1206(10)62009-1 (Ambrosia-Pollen unter CO₂-Anreicherung).
- **[22]** L. H. Ziska, F. A. Caulfield, Aust J Plant Physiol 27:893–898, 2000.
  doi:10.1071/PP00032
- **[23]** I. R. Lake u. a., „Climate Change and Future Pollen Allergy in Europe",
  Environ Health Perspect 125(3):385–391, 2017. doi:10.1289/EHP173
- **[24]** L. Hamaoui-Laguel u. a., Nat Clim Change 5:766–771, 2015. doi:10.1038/nclimate2652
- **[25]** W. Born, O. Gebhardt, J. Gmeiner, F. Ruëff, „Gesundheitskosten der Beifuß-Ambrosie
  in Deutschland", Umweltmed Forsch Prax 17(2):71–80, 2012 (ecomed Medizin, ISSN 1430-8681;
  kein DOI vergeben — Verlags-/UFZ-Nachweis; 193–1.190 Mio. €/Jahr bei Voll-Etablierung).
- **[26]** I. Lake, F. Colon, N. Jones, Lancet Planet Health 2:S16, 2018.
  doi:10.1016/S2542-5196(18)30101-3 (Konferenz-Abstract — nur Bandobergrenze der
  Alternative 96-B).
- **[33]** DWD Climate Data Center (CDC): Phänologie-Jahresmelder, wildwachsende Pflanzen
  (historisch), opendata.dwd.de — Hasel/Schwarz-Erle/Hänge-Birke (Blüte Beginn bzw.
  Blattentfaltung), Wiesen-Fuchsschwanz/Wiesen-Knäuelgras (Vollblüte);
  Stationsliste Jahresmelder; Lizenz DL-DE->Zero-2.0.
- **[48]** Destatis, Statistischer Bericht „Bevölkerungsfortschreibung auf Basis Zensus
  2022, Berichtsjahr 2023" (Tab. 12411-06: Bevölkerung 31.12.2023 nach Altersjahren;
  XLSX, destatis.de; Abruf 30.08.2026) — Gewichte der Prävalenz-Bänder (§3.2); Bandsummen
  identisch mit #95 (u65 64.747.448 · 65–74 9.569.640 · 75–84 6.294.744 · 85+ 2.844.213).
- **[51]** O. Pfaar, K.-C. Bergmann u. a., „Defining pollen exposure times for clinical
  trials of allergen immunotherapy — an EAACI position paper", Allergy 72:713–722, 2017.
  doi:10.1111/all.13092 (definiert die EAACI-Saisonkriterien Birke/Gräser — publiziert
  keine festen Längenwerte; L_B/L_G sind gekennzeichnete Abschätzungen, §3.5).
- **[52]** O. Pfaar u. a., „Pollen season is reflected on symptom load for grass and birch
  pollen-induced allergic rhinitis", Allergy 75:1099, 2020. doi:10.1111/all.14111 —
  **nur qualitative Stütze** (Pollen treibt Symptomlast); r-Werte sind kein f-Zahlenwert
  (§3.4; Rev.-5-Befund 14).
- **[53]** K. Bastl, U. Berger, M. Kmenta, „Translating the Burden of Pollen Allergy Into
  Numbers", J Med Internet Res 22(2):e16767, 2020. doi:10.2196/16767 — Volltext geprüft
  (PMC7060495, 30.08.2026): vergleicht Symptom-Score-Berechnungsmethoden, publiziert
  keinen Anteil symptomatischer Saisontage (§3.4).
- **[54]** B. Werchan u. a., „Spatial distribution of allergenic pollen through a large
  metropolitan area", Environ Monit Assess 189:169, 2017. doi:10.1007/s10661-017-5876-8
  (Berlin, 14 Fallen; Abstract-Wortlaut: „differences … were … 245 %“ Birke, „306 %“ Gräser zwischen Extremstandorten — Lesart-Diskussion §3.4).
- **[55]** B. Werchan u. a., „Spatial distribution of pollen-induced symptoms within a
  large metropolitan area — Berlin", Aerobiologia 34:539, 2018. doi:10.1007/s10453-018-9529-3
- **[56]** P. Bogawski u. a., „Lidar-Derived Tree Crown Parameters … Local Birch Pollen
  Concentrations", Forests 10:1154, 2019. doi:10.3390/f10121154
- **[65]** L.-O. Cardell u. a., „TOTALL: high cost of allergic rhinitis — a national
  Swedish population-based questionnaire study", npj Prim Care Respir Med 26:15082, 2016.
  doi:10.1038/npjpcrm.2015.82 (PMC4741287, Volltext gegengelesen 30.08.2026:
  bevölkerungsbasiert 18–65, n = 3.501; direkte Kosten **210,3 €**, indirekte 750,8 €
  je Betroffenem·Jahr; Preise CPI-adjustiert auf Februar 2014).
- **[66]** Deutscher Bundestag, Drucksache 19/22797 (Antwort der Bundesregierung,
  23.09.2020), Antwort zu Frage 5: KKR 2015 — Atmungssystem 16,5 Mrd. €, Asthma 1,9 Mrd. €;
  „Genauere Angaben zu Krankheitskosten allergischer Erkrankungen liegen nicht vor."
  dserver.bundestag.de/btd/19/227/1922797.pdf (Abruf 30.08.2026).
- **[67]** Pollensaison-Auswertung: `backend/scripts/kalibrierung/dwd_pollensaison.py` +
  `backend/data/kalibrierung/pollensaison_region.csv` / `pollensaison_meta.csv`
  (gepaarte Stationen, Normalperioden 1961–1990 vs. 1991–2020; Lauf 30.08.2026).

## 9 Familien-Einordnung & Verworfen-Liste (§2.6 — kein erneuter Drei-Ansätze-Vergleich)

#96 ist Folge-Risiko der Familie **„K1-Gesundheit bottom-up"** (Prototyp #95; vollständiger
Ansatz-Vergleich für #96 bereits in M0 Rev. 5 Kap. 3/5). Verworfene Alternativen (je ein
Satz Grund, §2.6; Parameter der Alternativen bis zur Quelle in M0 Kap. 3 dokumentiert):

- **96-B — Neophyten-Szenario (Ambrosia; Lake [23], Born [25], Hamaoui [24]):** bildet nur
  einen Teilausschnitt ab (eine Art; Birke/Gräser als Hauptlast fehlen) und projiziert
  2041–2060 statt „heute" — **Ergänzungsmodul ab M1** (Register 96-W024-02), kein Ersatz.
- **96-C — Nationaler Kostenanker, top-down:** per §3.1 ausgeschieden
  (Verteilschlüssel; Deutschland-Nenner; \(a_{\text{klima}}\) normativ) — nur
  Negativ-Beispiel.

## Entscheidungslog

Einträge 1: M0-Entscheidung (rückwirkend dokumentiert). Einträge 2–16: Rev.-1-Entscheidungen
(`/risiko-auto 96`, Gate 1, 30.08.2026); Eintrag 17: Revision nach Review-Runde 1 (Befund 101);
**Einträge 18–19: Rev. 2 (31.08.2026)** — Bezugsebene der P̂-Zentrierung (Nutzer-Entscheid,
Aufgabe §3.2) und die daraus folgende Fixierungs-/Maßnahmenfrage.
**Überstimmungsweg für alle Einträge:** „Entscheidung Nr. X ändern auf …" → Delta-Lauf
(Neurechnung betroffener Kopplungen + Re-Review + PDF-Neuexport). ⚠ = Ermessensfall.

| Nr | Frage | angewendete Entscheidung | Begründung | Alternative | Auswirkung |
|---|---|---|---|---|---|
| 1 | Methodischer Ansatz für #96? | **96-A** Prävalenz × gemessene Saison-Spreizung (Familie K1-Gesundheit bottom-up) | einziger Ansatz, der das Gesamtrisiko abdeckt und mechanistisch attribuiert (M0 Kap. 5) | 96-B (Modul ab M1); 96-C per §3.1 ausgeschieden | Gesamtmodell |
| 2 ⚠ | Klimasignal-Konstruktion? | **Spreizung zwischen Saison-Markern** (Erle→Birke; Fuchsschwanz→Knäuelgras), gemessen aus gepaarten DWD-Stationen | reine Verschiebung erzeugt keine Zusatztage; Spreizung ist messbar und RKI-konform [6]; behebt Rev.-5-Befund 11 (ΔS/S_ref nicht hergeleitet) | M0-Ratio ΔS/S_ref aus Trend-Zitaten (nicht reproduzierbar) | Klimasignal G14-fest; δ ≈ 2,0 statt implizit ~4–5 Tage |
| 3 ⚠ | Birken-Marker? | **Phase 4 (Blattentfaltung)** — Phase 5 hat Meldelücke 1960–90; Offset-Diagnose (+3,29 d; Trend −1,3 d) ins Band | einzige durchgängige Birken-Reihe; Offset kürzt sich in der Spreizungs-Differenz bis auf den Trend | Phase 5 (nur 1 gepaarte Station) oder Literaturwert | ΔS_B-Band −1,3 d |
| 4 ⚠ | Gräser-Saisonende? | **konstant** (nur Sukzessions-Spreizung Fuchsschwanz→Knäuelgras) | kein Phänologie-Marker fürs Saisonende; Herbst-Verlängerung [6] bewusst nicht angesetzt | Literatur-Zuschlag für Herbst-Verlängerung | Untergrenze (§6 Grenze 1) |
| 5 | Regionenzuschnitt? | **Bundesland → N/M/S wie #95** (`health.REGION_BY_BUNDESLAND`) | Produktkonsistenz; ΔS-Regionalstreuung gering (±20 %) | Naturraumgruppen (feiner) | einheitliche Regionslogik |
| 6 ⚠ | Kalibrierfaktor? | **c_kal ≡ 1 — dokumentierte Ausnahme** von §3.4: keine amtliche Anker-Zeitreihe existiert [66]; Modell voll messungs-/prävalenzverankert; Sanity-Bänder ersetzen den Fit | ein Fit ohne Anker wäre Scheinkalibrierung; BT-Drs. belegt die Lücke | J30-KKR-Anker bei Integration interaktiv ziehen (Registry-Vermerk) | kein Fit-Schritt; §4-Bänder tragen die Validierung |
| 7 ⚠ | f-Herleitung? | **Modellannahme 0,70 (0,50–0,85)**; Pfaar-r nur qualitativ; Bastl [53] geprüft — liefert die Größe nicht | behebt Kategorienfehler (Rev.-5-Befund 14) exakt entlang des Gegenprüfungs-Vorschlags | f aus PHD-Tagesdaten (Ersetzungspfad) | nur nativer Ausweis ±29 %; € unabhängig von f |
| 8 ⚠ | p_B/p_G? | **0,55/0,75 als gekennzeichnete Abschätzung** (Rangfolge-Stütze [3]); additive Saisonform als €-konservativ dokumentiert | Anteil unter AR-Patienten nicht publiziert (Befund 36a); Überlappungskorrektur würde € erhöhen (36b) | PID-/Versorgungsdaten (Ersetzungspfad) | δ ±8 % Sensitivität |
| 9 ⚠ | Kostensatz-Basis? | **TOTALL 266,90 €₂₀₂₄ (populationsbasiert)**; Schramm nur Obergrenze/Kinder-Band | Schramm (moderate–schwer) auf alle Betroffenen = bekannte ~4-fache Überschätzung — verletzt Untergrenzen-Zusage (#95-Befund-62-Lehre); impliziter Baseline-Check §4 bestätigt | Schramm als Basis (M0-Linie; 9,1 Mrd. implizite Basis — verworfen) | € −76 % ggü. Schramm-Basis |
| 10 ⚠ | Prävalenz-Bänder? | **u20-Ebene neu** (Zensus 10er-Klassen); 18/19 mit KiGGS-Wert (unterschätzend); 75+/85+ = 5,0 % Extrapolation (gekennzeichnet) | behebt Rev.-5-Befunde 27/35 entlang Variante (a) der Gegenprüfung | Misch-Prävalenz je Zelle ohne u20-Ebene | Alterslast korrekt verteilt |
| 11 | Attribution? | **a_attr = 0,50 (0,19–0,84)** [9] | einzige publizierte Attribution des Saisontrends; IQR als Band | 1,0 (volle Anrechnung — nicht belegbar) | zentraler Hebel ±62 % |
| 12 | Vegetations-Modulation? | **λ = 0,7 (0,3–1,0)** (aktualisiert Runde 2, Befund 110: wörtliche Zuwachs-Lesart der Werchan-Prozente; Verhältnis-Lesart im Band), P̂ in beiden Pfaden; Ḡ-Zentrierung §3.3 | Kette #lambda-veg reproduzierbar; Bundessumme λ-invariant — Lesart wirkt nur verteilend | Verhältnis-Lesart (M0): λ = 0,6 | lokale Differenzierung ±35 % |
| 13 | Ambrosia (W024)? | **bewusst inaktiv in M0**, Modul 96-B ab M1 | Zeithorizont 2041–2060 ≠ „heute"; Teilausschnitt | sofortiges Zusatzmodul | Untergrenze |
| 14 | E09 Trockenheit / Intensität? | **bewusst inaktiv** (Register 96-W025-03/-04) | keine quantifizierte ERF; Wirkrichtung erhöhend → konservativ | Sensitivitätsband nach Literatur | Untergrenze |
| 15 | S158 Pollenmonitoring? | **Maßnahmen-Hebel qualitativ** (§3.5); Stadtbaumwahl als mechanischer Hebel über Ĝ quantifiziert | keine Interventions-Effektgröße publiziert (Befunde 26/34); ehrlich statt gesetzt | gesetzte Dämpfungsannahme (Rev.-5-„v_monitor" — gestrichen, Befund 32) | Hebelliste ehrlich |
| 16 | R36 im Basiswert? | **Default 1** (nur Schicht A) | ambulantes Krankheitsbild; keine Evidenz für Distanzeffekt (§3.2) | Sensitivitätsband analog #95-β_d | Basiswert schlanker |
| 17 ⚠ | Ḡ-Gewichtsregel (P̂-Zentrierung)? | **betroffenengewichtetes Mittel über bewohnte Zellen** (Formel §3.3; Bezugsebene in Rev. 2 durch Log 18 auf die Kommune festgelegt) | macht die Bundessumme per Konstruktion invariant gegen λ und Ĝ×pop-Korrelation (Befund 101); c_kal ≡ 1 hat keinen nachgeschalteten Fit, der eine Fehlgewichtung auffangen würde | flächen-/zellgewichtetes Mittel (Bundessumme würde mit Ĝ×pop-Korrelation driften) | Sanity-Rechnung §4 exakt; P̂ verteilt nur um |
| 18 ⚠ | Bezugsebene der P̂-Zentrierung: Bund oder Kommune? | **die eigene Kommune** — Ḡ = betroffenengewichtetes Mittel über die Zellen der betrachteten Kommune, im Lauf gebildet (kein Registry-/Bundeswert); ohne Referenz P̂ ≡ 1 | (a) **Evidenz-Reichweite**: λ stammt aus intra-urbanen Messungen (Werchan Berlin [54,55], Bogawski [56]) — sie tragen Umverteilung INNERHALB einer Stadt, nicht interkommunale Niveauunterschiede; (b) **Aufgabe §3.2 „geschlossene Betrachtungsebene"** (Fortschreibung 31.08.2026, Nutzer-Entscheid): Referenzmittel nie aus Aggregation über eine höhere Ebene; (c) ein Bundesmittel wäre nur mit einem per §3.4 unzulässigen Bundeslauf bestimmbar | Bundesmittel aus Stichprobe (Rev. 1; verworfen: Skalentransfer unbelegt + Ebenenbruch) · amtlicher Vegetations-Referenzwert (existiert nicht) | Kommunensumme jetzt EXAKT invariant gegen λ (statt näherungsweise); Vegetationsstruktur verschiebt nur INNERHALB der Kommune — interkommunal wirkt sie nicht mehr; die Wirkung ist **nullsummig umverteilend** (betroffenengewichtet erwartungstreu), NICHT „konservativ" im Sinne einer Unterschätzung (§3.3(3), Modellgrenze 7) |
| 19 ⚠ | Ḡ-Fixierung (Befund 113) unter der kommunalen Zentrierung? | **kein Pinning** — Ḡ wird in jedem Lauf aus dem aktuellen Vegetationszustand der Kommune gebildet; der flächige Niveaueffekt bleibt bewusst unbuchbar (§5, Modellgrenze 7) | Ein eingefrorener Referenzwert würde einem flächigen Programm einen Niveaueffekt zubuchen, den die λ-Evidenz (intra-urbane Gradienten) nicht trägt — Befund 113 war an das Bundesmittel gebunden und ist mit der kommunalen Zentrierung keine Fixierungs-, sondern eine Evidenzfrage; die Produktmechanik (measure_service skaliert gespeicherte Outcomes) ist KEIN Beleg, sondern begründet die Integrationsauflage: keine pauschal verknüpfte Maßnahme, sonst würde genau der unbelegte Niveaueffekt gebucht (Befund 124/129; Test test_no_flat_measure_on_allergy_days) | Baseline-Pinning je Kommune (verworfen: bucht unbelegten Niveaueffekt) · Emissions-/Ausbreitungsmodell (Ersetzungspfad §6, Datenlage fehlt) | Maßnahme wirkt als Umverteilung (gezielte Hotspot-Entschärfung), nicht als flächiger Niveauhebel |
