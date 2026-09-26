# Methodik-Bericht #96 — Allergische Reaktionen durch Aeroallergene pflanzlicher Herkunft

Status: **Rev. 3 (08.09.2026, Revision nach Vorgabe P2 des Aufsichtsrats — F-0007 Punkt 1:
Wirkungsabschätzung des S158-Hebels statt „qualitativ"/Wirkung null, §5.1 + Modellgrenze 8 +
Entscheidungslog 20; Review der Rev. 3 steht aus, Ledger-Befund 151)** · Rev. 2 abgenommen ·
Rev. 2: **(P̂-Zentrierung auf die eigene Kommune statt auf ein Bundesmittel —
Aufgabe §3.2 „geschlossene Betrachtungsebene", Nutzer-Entscheid 31.08.2026;
Log 18/19) — ABNAHMEREIF & INTEGRIERT (Null-Runde: Review Runde 10; Befunde
116–150 behoben)** · 31.08.2026 · Rev. 1 war abnahmereif (Null-Runde
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

> **Revisionsstand.** **Rev. 3 (08.09.2026)** = Wirkungsabschätzung des S158-Hebels
> (Pollen-Frühwarnung): Der Hebel läuft nicht mehr „qualitativ" mit Wirkung null, sondern
> mit \(r_{\text{S158}}\) = 0,03 (Band 0,005–0,10) als §3.9-Abschätzung — **Vorgabe P2 des
> Aufsichtsrats (F-0007 Punkt 1)**, Aufgabe §3.5 i. d. F. 06.09.2026. Betroffen: Kap. 1
> (Knoten-Bilanz S158), §2 (Register 96-S158-01), §3.6-Zeichentabelle, **§5.1 (neu)**,
> §6 Modellgrenze 8 (neu), §7 (`pollen.r_s158`), Entscheidungslog 15/20. Der Katalogwert
> `default_reduction` bleibt in dieser Revision 0,0 (Code-Nachzug L2 als eigener Schritt);
> die Sperre aus Befund 124 (kein pauschaler `linked_risk_codes`-Kanal) bleibt bestehen.
> **Rev. 2 (31.08.2026)** = Bezugsebene der P̂-Zentrierung:
> \(\bar G\) ist nicht mehr ein bundesweites Referenzmittel, sondern das
> betroffenengewichtete Mittel der **betrachteten Kommune**, im Lauf aus ihren
> eigenen Zellen gebildet (Aufgabe §3.2 „geschlossene Betrachtungsebene",
> Nutzer-Entscheid; Log 18). Damit gilt Σ B·P̂ = Σ B je Kommune **exakt**, ein
> Registry-/Bundeswert entfällt ersatzlos, und ohne Referenz bleibt P̂ ≡ 1.
> Folgeentscheidung Log 19: **kein** eingefrorener Referenzzustand — ein
> flächiger Vegetations-Niveaueffekt bleibt bewusst unbuchbar (§5,
> Modellgrenze 7). Gleiche Linie beim Ĝ-Gewicht \(w_B\): erst
> Registry-Parameter (Kopplung an \(p_B\)/\(p_G\) tot), dann Laufzeit-Ableitung
> (verschob den Schicht-A-Hazard), jetzt **Definitionskonstante der Ebene mit
> testgebundener Kopplung** — editierbar bleibt nur, was die Evidenz hergibt
> (Ledger-Befunde 138/142/144). Betroffen: §3.3, §3.4-Sensitivität, §3.6-Zeichentabelle, §5,
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
| S158 | Monitoring von Gesundheitsgefahren / Frühwarnsysteme | Maßnahmen-Hebel (**abgeschätzt**, §5.1) | Pollen-Frühwarnung (DWD/PID-Gefahrenindex); Ebene EARLY_WARNING_SYSTEMS (§5); Wirkungsfaktor \(r_{\text{S158}}\) = 0,03 (0,005–0,10), §3.9 ABGESCHÄTZT | wirkt **nur** im Maßnahmen-Modul, nicht im Basiswert des Schadens (dort weiterhin Default 1); keine publizierte Interventions-Effektgröße — deshalb Abschätzung statt Nullwirkung (Log 15/20, Vorgabe P2) |
| R35 | Vorkommen von Bevölkerung | Schicht A + B | \(\text{pop}_a\) (Zensus 2022, 100 m; neue Ebene u20 — §3.2) | — |
| R36 | Vorkommen von Gesundheitsinfrastruktur | Schicht A (Screening) | Ebene HEALTHCARE_ACCESS im Index (§3.6) | Basiswert Default 1: AR ist ein ambulantes Krankheitsbild; für einen Distanz-Effekt auf AR-Behandlungstage existiert keine Evidenz (§3.2: unbelegte Modulatoren Default 1; Log 16) |

KWRA-Indikator (intensive Betrachtung „Blühbeginn der Erle"): **GE-KL-07** „Tag des
Blühbeginns der Erle im Jahr" — geht direkt als Front-Marker in \(\Delta S_B\) ein (§3.1).
KWRA-Einstufung ohne Anpassung je Zeitscheibe mit Fundstelle: Tabelle im Unterabschnitt
„Risiko ohne (weitere) Anpassung“, Aussage (c). Handlungserfordernis dennoch **sehr dringend**
(KWRA-2021-Mappe, Blatt `Klimawirkungen`, Zelle AG98; Anpassungsdauer 10–50 Jahre, Zelle U98 —
lange Anpassungsvorlaufzeiten: Stadtbaum-Generationen) [15].

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

### Risiko ohne (weitere) Anpassung

**(a) Zuordnung der Zahlen.** Alle Zahlen des Basiswerts in diesem Bericht — Betroffene, zusätzliche
Symptomtage und die daraus bewerteten Euro-Beträge in K1-Morbidität, für die Beispielkommune Berlin
755.753 Tage und 4,69 Mio. € je Jahr (Preisstand 2024) in der Rechenkette §3.0 — gehören zum KWRA-Zustand
**„Risiko ohne (weitere) Anpassung“**, und zwar zur Zeitscheibe Gegenwart: M0 weist das Ist-Klima aus
(Normalperioden 1961–1990 gegen 1991–2020, Kapitel 6). Der heute schon umgesetzte Anpassungsstand steckt
in den gemessenen Größen, nicht in einem eigenen Faktor: Die Prävalenz \(p_{\text{AR},a}\) stammt aus
DEGS1 [1] und KiGGS Welle 2 [2], die Kosten je Betroffenem aus der TOTALL-Erhebung 2014 [65]. Beide sind
unter der Versorgung ihres Erhebungszeitraums erhoben; was Betroffene damals schon taten (Medikation,
Meiden von Pollen), steckt in diesen Zahlen. Die KWRA zählt solche individuelle Anpassung (Meiden bestimmter
Orte, Lüften, Pollen-Apps) zum bereits bestehenden Stand (Teilbericht 5, S. 180 [15]). Eine Wirkung der
heutigen Pollenflug-Warnung rechnet der Basiswert weder heraus noch hinzu (S158 im Basiswert Default 1,
Knoten-Bilanz). Die heutige Stadtbaum- und Vegetationsausstattung wirkt über \(\hat G\) nur auf die
Verteilung der Zusatztage innerhalb der Kommune. Weil \(\hat P\) auf die eigene Kommune zentriert ist
(\(\sum B \hat P = \sum B\), §3.3, Log 18/19), gilt: Die Vegetation hebt oder senkt den Basiswert der Kommune nicht
(Modellgrenze 7). Eine Kommune, die schon allergenarm pflanzt, sieht das heute nur in der Verteilung.

**(b) Zustand „mit Anpassung“.** Der Bericht stellt ihn nur als Wirkung der beiden Maßnahmen-Hebel auf den
Basiswert dar, nicht als eigenen Basiswert:

- **Pollen-Frühwarnung S158** (§5.1, Abschätzung von KAP3 nach Vorgabe P2): Sie wirkt nur an gewarnten Tagen
  (DWD-Pollenflug-Gefahrenindex mindestens „mittel“ [70], je Pollengruppe) und nur in Zellen im
  Geltungsbereich. Dort mindert sie \(r_{\text{S158}} \cdot t_{\text{warn}}\) = 0,03 × 0,75 = 2,25 % der
  Zusatztage. Beispielkommune Berlin, ganze Stadt im Geltungsbereich: 17.004 vermiedene Tage und
  ≈ 105.400 € je Jahr (Preisstand 2024).
- **Allergenarme Stadtbaumwahl** (§5, Log 24): Sie senkt \(\hat P\) einer Zelle um 0,14 je Senkung von
  \(\hat G/\bar G\) um 0,2. Die Summe der Kommune bleibt gleich (Modellgrenze 7); die Wirkung ist eine
  Umverteilung zwischen Zellen.

Im Produkt sind beide Wirkungen heute nicht sichtbar (Sperre aus Befund 124; Integrationsauflagen S158 und
Stadtbaumwahl in §5.1 und §5). Einen Wert „mit Anpassung“ gibt es dort erst nach der Integration und nur, wenn
eine Kommune Maßnahmen wählt. Die KWRA-Stufen „mit Anpassung“ (Restrisiko, Blatt `Klimawirkungen`, Zeile 98,
Spalten AB bis AF: gering · gering · mittel · gering · mittel) übernimmt der Bericht nicht als Zahl: Sie
bewerten die Maßnahmen des Bundes (Aktionsplan Anpassung III und weiterreichende Maßnahmen; Blatt
`Lesehinweise`, Zeile 27), nicht die Hebel einer Kommune.

**(c) KWRA-Stufe ohne Anpassung und Gewissheit je Zeitscheibe.**

| Zeitscheibe (KWRA) | Fall | Risiko ohne Anpassung | Zelle | Gewissheit | Zelle |
|---|---|---|---|---|---|
| Gegenwart (Bezug 1971–2000) | — | gering | N98 | nicht ausgewiesen | — |
| Mitte des Jahrhunderts (2031–2060) | optimistisch | mittel | O98 | mittel | S98 |
| Mitte des Jahrhunderts (2031–2060) | pessimistisch | hoch | P98 | mittel | S98 |
| Ende des Jahrhunderts (2071–2100) | optimistisch | mittel | Q98 | mittel | T98 |
| Ende des Jahrhunderts (2071–2100) | pessimistisch | hoch | R98 | mittel | T98 |

Fundstelle: `docs/KWAR/KWRA-2021_Klimawirkungen.xlsx`, Blatt `Klimawirkungen` (ID 96 in Spalte A), Zeile 98, Spalten N bis R
(Risiko ohne Anpassung) und Spalten S und T (Gewissheit Mitte und Ende). Gleichlautend im zuständigen
Teilbericht: `docs/KWAR/kwra2021_teilbericht_5_cluster_wirtschaft_gesundheit_bf_211027_0.pdf`, Tabelle 55,
S. 179 [15]. Optimistisch und pessimistisch sind das 85. und das 15. Perzentil des Modellensembles unter
RCP8.5 (Teilbericht 5, S. 177). Für die Gegenwart weist die KWRA keine Gewissheit aus: Tabelle 55 lässt das
Feld leer, die Mappe hat dafür keine Spalte. Beide Digitalisate widersprechen sich hier nicht; die Bewertungen
stehen nach der Vorrangregel am Ende der Aufgabe ohnehin nur in der KWRA-2021-Mappe.

**Warum die eigene Quellenlage von der KWRA-Gewissheit abweicht.** Die KWRA-Gewissheit „mittel“ bewertet,
wie sicher die Projektion für 2031–2060 und 2071–2100 ist; der Basiswert dieses Berichts rechnet dagegen die
Gegenwart aus gemessenen Größen (Phänologie an über 1.000 DWD-Stationen, Prävalenz aus Surveys), und seine
Unsicherheit liegt nicht in einer Klimaprojektion, sondern vor allem im Klimaanteil \(a_{\text{attr}}\) = 0,50
(0,19–0,84), übertragen aus einer nordamerikanischen Studie [9] (Berlin 1,78–7,87 Mio. € je Jahr, §3.0), und im
Sensibilisierungsprofil \(p_B/p_G\) (Abschätzung von KAP3, §3.4).

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
| 96-S158-01 | S158 Pollen-Frühwarnung → Symptomlast | keine quantifizierte Interventions-Effektgröße publiziert ⇒ **Abschätzung** \(r_{\text{S158}}\) = 0,03 (Band 0,005–0,10) aus der offengelegten Dreifaktor-Kette §5.1 | — (keine Interventionsstudie; §3.8-Datenlücke ausdrücklich benannt) | Wirkungsort/Kette: §5.1 (`#s158-wirkung`); Ebene EARLY_WARNING_SYSTEMS (DWD/PID-Gefahrenindex) | Setzung für deutsche Kommunen; **§3.9 ABGESCHÄTZT**, im Produkt als „Abschätzung von KAP3" gekennzeichnet | gewarnte Tage (DWD-Index mindestens „mittel“, je Pollengruppe), zellscharf im Geltungsbereich; Personenteil pauschal (Modellgrenze 8 der Abschätzung) | **Maßnahmen-Hebel (abgeschätzt, §5.1)** — kein Basiswert der Schadensformel | Log 15/20 |
| 96-R36-01 | R36 Gesundheitsinfrastruktur → AR-Outcome | keine Evidenz für Distanz-/Kapazitätseffekt auf ambulante AR-Behandlung | — | — | AR wird ambulant/selbstmediziert behandelt | HEALTHCARE_ACCESS (Schicht A) | **bewusst inaktiv** (Basiswert Default 1) | Log 16 |

## 3 Modell (§2.3) — Ansatz 96-A, Schicht B

**Native Ergebnisgröße (§3.6, deklariert): zusätzliche Symptomtage \(\Delta\text{Tage}\) je
Jahr** (klimaattribuiert). Teil-Ausweise unter der KWRA-Klammer: Betroffene \(B\), €.
Kein Mortalitätspfad (Konto-Einbettung Kap. 1).

**Gemeinsamer Preisstand aller Kostensätze dieses Berichts: €2024**; Umrechnungsfaktoren je
Satz in der Zeichentabelle (Destatis-VPI-Jahresmittel, 2020 = 100: 2000 = 75,9 · 2014 = 94,0 ·
2024 = 119,3 [19]).

### 3.0 Rechenkette

Die Rechenkette erzählt die Methodik von der amtlichen Quelle bis zum Euro-Betrag am Beispiel
einer Kommune. Die Formeln in 3.1–3.5 sind die genaue Fassung derselben Kette und keine zweite
Methodik; alle Parameter sind die unveränderten Werte aus Kapitel 7. **Beispielkommune: Berlin**
(Gemeinde 11000000, Land Berlin, damit Region Mitte nach Log 5), dieselbe Kommune wie in #95,
damit die M0-Berichte an einer Kommune vergleichbar sind.

**Wirkungskette in einem Satz:** Der Klimawandel zieht die Pollensaison auseinander (frühe
Blüher rücken stärker vor als späte); wer Heuschnupfen hat, hat dadurch mehr Tage mit
Beschwerden, und jeder zusätzliche Beschwerdetag kostet Behandlung.

| Ebene | Rechenschritt | Wert (Beispielkommune Berlin) | Quelle |
|---|---|---|---|
| 1 | Einwohner je Altersband \(\text{pop}_a\) (u20 · 20–64 · 65–74 · 75–84 · 85+); u20 = unter 5 + 5–10 + 10–15 + 15–20, 20–64 = u65 − u20 | 673.277 · 2.288.153 · 339.490 · 253.528 · 107.933 (zusammen 3.662.381); u20 = 173.699 + 176.060 + 163.535 + 159.983 | Tab. 12411-09-01-4-B, Stichtag 31.12.2023, Basis Zensus 2022 [68], Gemeinde Berlin, Altersgruppen (20); dieselben Zahlen nach Altersjahren in Destatis Tab. 12411-09 [69] |
| 2 | Anteil mit ärztlich diagnostiziertem Heuschnupfen (12 Monate) \(p_{\text{AR},a}\) je Band | 8,8 · 13,2 · 6,7 · 5,0 · 5,0 % | KiGGS W2 [2], DEGS1 [1], bevölkerungsgewichtet (§3.2); Kap. 7 `pollen.p_ar` |
| 3 | Betroffene \(B = \sum_a \text{pop}_a \times p_{\text{AR},a}\) | 59.248 + 302.036 + 22.746 + 12.676 + 5.397 = **402.103 Betroffene** (11,0 % der Einwohner) | Ebenen 1 und 2 |
| 4 | Klimasignal der Region: Verlängerung der Saison als Spreizung \(\Delta S_B\) (Erle → Birke) und \(\Delta S_G\) (Fuchsschwanz → Knäuelgras), 1991–2020 gegen 1961–1990 | Region Mitte: \(\Delta S_B\) = 4,20 Tage, \(\Delta S_G\) = 4,08 Tage | DWD-Phänologie, `pollensaison_region.csv`, Zeilen `mitte` [67] (§3.1); Kap. 7 `pollen.delta_s_region` |
| 5 | Gewichtet mit dem Anteil der Betroffenen, die auf die jeweilige Saison reagieren: \(p_B \Delta S_B + p_G \Delta S_G\) | 0,55 × 4,20 + 0,75 × 4,08 = 2,31 + 3,06 = 5,37 Tage | \(p_B\), \(p_G\): Abschätzung von KAP3, Rangfolge nach [3] (§3.4, Log 8); Kap. 7 `pollen.p_sens_gruppen` |
| 6 | Zusätzliche Symptomtage je Betroffenem \(\delta = f \times \text{Ebene 5} \times a_{\text{attr}}\) (Anteil der Saisontage mit Beschwerden, Anteil des Klimawandels am Trend) | 0,70 × 5,37 × 0,50 = **1,8795 Tage** je Betroffenem und Jahr | \(f\): Abschätzung von KAP3 (§3.4, Log 7); \(a_{\text{attr}}\): Anderegg [9] (Log 11); Kap. 7 `pollen.f_symptomtage`, `pollen.a_attr` |
| 7 | Vegetationsfaktor \(\hat P\) je Zelle (allergene Bäume und Grünflächen), zentriert auf das betroffenengewichtete Mittel der eigenen Kommune | je Zelle ab 0,3 (keine allergene Vegetation) bis über 1 (Allee, Park); Mittel über Berlin genau **1**, also \(\sum B \hat P = \sum B\) = 402.103 | \(\lambda\) = 0,7 aus Werchan [54,55], Bogawski [56] (§3.3, §3.4, Log 12, 17, 18); Kap. 7 `pollen.lambda_veg` |
| 8 | Zusätzliche Symptomtage \(\Delta\text{Tage} = B \times \delta \times \hat P\) (native Ergebnisgröße) | 402.103 × 1,8795 × 1 = **755.753 Tage je Jahr** (u20 111.357 · 20–64 567.677 · 65–74 42.751 · 75–84 23.825 · 85+ 10.143) | Ebenen 3, 6 und 7 |
| 9 | Kostensatz je Symptomtag \(c_{\text{Tag}} = c_{\text{Jahr,direkt}} / d_{\text{Saison}}\) mit \(d_{\text{Saison}} = f \times (p_B L_B + p_G L_G)\) | 266,90 € / (0,70 × (0,55 × 30 + 0,75 × 60)) = 266,90 € / 43,05 Tage = **6,20 € je Tag** (Preisstand 2024) | TOTALL [65], VPI [19]; \(L_B\), \(L_G\): Abschätzung von KAP3 nach [51] (§3.5); Kap. 7 `pollen.c_jahr_direkt`, `pollen.d_saison`, `pollen.c_tag` |
| 10 | Bewerteter Schaden (Konto K1, nur Morbidität) je Jahr = \(\Delta\text{Tage} \times c_{\text{Tag}}\) | 755.753 × 6,20 € = **4,69 Mio. € je Jahr (Preisstand 2024)**, das sind 1,28 € je Einwohner; der Zelllauf des Produkts ergibt 4,59 Mio. € (Unterschied unten) | Ebenen 8 und 9 |

**Warum \(f\) im Euro-Betrag keine Rolle spielt.** \(f\) steht in Ebene 6 (mehr Tage) und in
Ebene 9 (mehr Tage in der Referenzsaison, also billigerer Tag); in Ebene 10 kürzt es sich
deshalb heraus (§3.5). Es wirkt nur auf die Zahl der Tage.

**Ebene 7: Warum der Vegetationsfaktor auf der Ebene der Kommune herausfällt.** \(\hat P\) ist so
gebaut, dass sein mit den Betroffenen gewichtetes Mittel über die Zellen der eigenen Kommune
genau 1 ist (\(\bar G\) aus den eigenen Zellen, Log 17 und 18). Für die Summe über Berlin gilt
deshalb \(\sum B \hat P = \sum B\), gleich wie grün die Stadt ist. Der Vegetationsfaktor ändert
also nicht, *wie viele* Symptomtage Berlin hat, sondern nur, *wo* sie anfallen: Eine Zelle an
einer Birkenallee mit doppelt so viel allergener Vegetation wie im Mittel bekommt
\(\hat P\) = 1 + 0,7 × (2 − 1) = 1,7, eine Zelle ohne kartierte Vegetation 1 − 0,7 = 0,3. Eine
insgesamt grünere Kommune hat damit nicht mehr Tage als eine graue; das trägt die Evidenz nicht
(Log 18, Modellgrenze 7 in §6).

**Kommune statt Zellen: was die Kette verfälscht und was nicht.** Das Produkt rechnet je
100-m-Zelle mit der Bevölkerung aus dem Zensus-Gitter (Stichtag 15.05.2022) und summiert; die
Kette rechnet mit der Fortschreibung für ganz Berlin (Stichtag 31.12.2023, Ebene 1). **Die Kette
überschätzt Berlin um 2,0 %.** Zwei Schritte sind auf der Ebene der Kommune exakt: \(\delta\) ist
in der ganzen Kommune gleich (eine Region), und \(\hat P\) mittelt auf 1 (Ebene 7). Wirkungen wie
in #95 für die Temperatur je Zelle und die Feinstruktur unter 1 km gibt es in #96 deshalb nicht.
Was bleibt, ist die Bevölkerung. Nachgerechnet mit allen 40.669 bewohnten 100-m-Zellen innerhalb
der Gemeindegrenze Berlins nach der Logik des Produkts (`zensus_loader.apply_zensus_to_cell_inputs`,
u20 je Zelle aus den 5er-Jahresgruppen, §3.2; Gemeindegebiet, Gitter und Ersatzregel mit den
Funktionen aus `docs/methodik/anlagen/95_zellvergleich.py`, Lauf 26.09.2026), ergeben sich zwei
Wirkungen, jede auf die vorige gerechnet:
(1) **Einwohnersumme: × 0,981.** Das Gitter zählt 3.593.357 Einwohner, die Fortschreibung
3.662.381 (#95 Befund 99).
(2) **Altersbänder je Zelle wie im Produkt: × 0,999 = 0,9969 × 1,0021.** Der erste Faktor ist der
Altersaufbau im Gitter (u20 658.325 · 20–64 2.240.635 · 65–74 334.709 · 75–84 262.921 ·
85+ 96.767; Anteil u20 an den unter 65-Jährigen 22,71 % gegen 22,73 % in Ebene 1), gemessen mit
der Ersatzregel aus #95 §3.3 für Zellen mit geheimgehaltenem Anteil 65+. Der zweite Faktor ist
eine Eigenheit des Produkts: In 4.774 Zellen mit 99.098 Einwohnern setzt es 65+ = 0 (#95
Befund 104). In #96 wirkt sie **nach oben**: Die dort nach der Ersatzregel fehlenden 12.921
Menschen ab 65 zählt das Produkt in den Bändern u20 und 20–64 mit 8,8 % und 13,2 % statt mit
6,7 % und 5,0 % Prävalenz. In #95 senkt dieselbe Eigenheit den Betrag.
Zusammen 0,981 × 0,999 = 0,980: Der Zelllauf ergibt für Berlin 394.106 Betroffene, 740.723
zusätzliche Symptomtage und **4,59 Mio. € je Jahr (Preisstand 2024)**, 2,0 % weniger als die
Kette; mit der Ersatzregel statt der Eigenheit wären es 4,58 Mio. €. Die Kette zeigt den
Rechenweg, der Betrag für Berlin ist der Zelllauf des Produkts.
Außerdem verliert die Kette die Verteilung innerhalb der Stadt: Zwischen einer vegetationsarmen
Zelle (0,3) und einer Allee-Zelle (1,7) liegt der Faktor 5,7. Wer wissen will, welches Quartier
die Tage trägt, braucht die Zellen.
Die Altersbänder müssen die der Kommune sein: Rechnete man Berlin mit dem Bundesanteil der unter
20-Jährigen (24,07 %, letzter Rückfall des Produkts, §3.2) statt mit dem eigenen (22,73 %), kämen
39.482 Menschen mehr in das Band mit 8,8 % statt 13,2 % Prävalenz, und \(B\) läge um 1.737
(0,43 %) **zu niedrig**, weil Berlin weniger junge Menschen hat als der Bund. Je Prozentpunkt
u20-Anteil sind es 1.303 Betroffene (0,32 %). Größer wird dieser Fehler bei Kommunen, deren
Altersaufbau stärker vom Bund oder Land abweicht (Universitätsstadt, Kurort): Dort gehören die
Altersbänder der Kommune in Ebene 1, nie die des Landes.

**Stärkster Treiber** ist der Klimaanteil \(a_{\text{attr}}\) (Ebene 6): Sein Band 0,19–0,84
(Anderegg [9]) setzt Tage und Euro für Berlin auf das 0,38- bis 1,68-Fache, also 1,78–7,87 Mio. €
je Jahr. Weiter reicht nur das Band des Kostensatzes nach oben (Obergrenze 23,66 € je Tag aus
Schramm [7] für mittelschwer bis schwer Erkrankte, damit 17,9 Mio. €); es ist einseitig und
wirkt nur auf den Euro-Betrag, nicht auf die Tage (§3.5).

```python test: rechenkette_96
# Rechenkette 3.0, Beispielkommune Berlin; Parameter = Kapitel 7 (unveraendert)
u65, a6574, a7584, a85p = 2_961_430, 339_490, 253_528, 107_933   # 12411-09-01-4-B [68]
u20 = 173_699 + 176_060 + 163_535 + 159_983                        # unter 5 ... 15-20 [68, 69]
pop = {"u20": u20, "20-64": u65 - u20, "65-74": a6574, "75-84": a7584, "85+": a85p}
assert pop["u20"] == 673_277 and pop["20-64"] == 2_288_153
assert sum(pop.values()) == 3_662_381
anteil_u20 = u20 / u65
assert abs(anteil_u20 - 0.2273) < 1e-4
p_ar = {"u20": 0.088, "20-64": 0.132, "65-74": 0.067, "75-84": 0.050, "85+": 0.050}
b_band = {k: pop[k] * p_ar[k] for k in pop}
for k, soll in {"u20": 59_248, "20-64": 302_036, "65-74": 22_746,
                "75-84": 12_676, "85+": 5_397}.items():
    assert abs(b_band[k] - soll) < 1
B = sum(b_band.values())
assert abs(B - 402_103) < 1
assert abs(B / sum(pop.values()) - 0.110) < 0.001
dS_B, dS_G = 4.20, 4.08          # pollensaison_region.csv, Region mitte
p_B, p_G, f, a_attr = 0.55, 0.75, 0.70, 0.50
gew = p_B * dS_B + p_G * dS_G
assert abs(gew - 5.37) < 1e-9
delta = f * gew * a_attr
assert abs(delta - 1.8795) < 1e-9
# Ebene 7: Zentrierung auf die eigene Kommune -> Summe gegen P^ invariant
lam = 0.7
zellen = [(1_000, 0.00), (4_000, 0.10), (2_500, 0.30), (500, 0.60)]  # (B, G^)
g_bar = sum(b * g for b, g in zellen) / sum(b for b, _ in zellen)
p_hat = [1 + lam * (g / g_bar - 1) for _, g in zellen]
assert abs(sum(b * p for (b, _), p in zip(zellen, p_hat)) - sum(b for b, _ in zellen)) < 1e-9
assert abs(p_hat[0] - 0.3) < 1e-9 and abs((1 + lam * (2 - 1)) - 1.7) < 1e-9
tage = B * delta * 1.0
assert abs(tage - 755_753) < 1
tage_band = {k: v * delta for k, v in b_band.items()}
for k, soll in {"u20": 111_357, "20-64": 567_677, "65-74": 42_751,
                "75-84": 23_825, "85+": 10_143}.items():
    assert abs(tage_band[k] - soll) < 1
d_saison = f * (p_B * 30 + p_G * 60)
assert abs(d_saison - 43.05) < 1e-9
c_tag = 6.20                      # Kap. 7 pollen.c_tag (= 266,90 / 43,05, gerundet)
assert abs(266.90 / d_saison - c_tag) < 0.01
euro = tage * c_tag
assert abs(euro / 1e6 - 4.69) < 0.005
assert abs(euro / sum(pop.values()) - 1.28) < 0.005
# Grenze der Kommunenrechnung (Bundes- statt Kommunenanteil u20) und staerkster Treiber
assert abs(0.01 * u65 * (0.132 - 0.088) - 1_303) < 1
anteil_bund = 15_583_456 / 64_747_448
assert abs(anteil_bund - 0.2407) < 1e-4
mehr_u20 = round(u65 * anteil_bund) - pop["u20"]
verschiebung = mehr_u20 * (0.132 - 0.088)
assert abs(mehr_u20 - 39_482) < 2
assert abs(verschiebung - 1_737) < 1 and abs(verschiebung / B - 0.0043) < 0.0001
assert abs(euro * 0.19 / 0.50 / 1e6 - 1.78) < 0.005
assert abs(euro * 0.84 / 0.50 / 1e6 - 7.87) < 0.005
assert abs(tage * 23.66 / 1e6 - 17.9) < 0.05
# Zelllauf des Produkts (Lauf 26.09.2026, 40.669 Zellen): Bandsummen und Zerlegung
zell = {"u20": 658_325, "20-64": 2_240_635, "65-74": 334_709, "75-84": 262_921, "85+": 96_767}
assert sum(zell.values()) == 3_593_357
assert abs(zell["u20"] / (zell["u20"] + zell["20-64"]) - 0.2271) < 1e-4
B_zell = sum(zell[k] * p_ar[k] for k in zell)
assert abs(B_zell - 394_106) < 1
assert abs(B_zell * delta - 740_723) < 1
assert abs(B_zell * delta * c_tag / 1e6 - 4.59) < 0.005
f_ew = 3_593_357 / 3_662_381
assert abs(f_ew - 0.981) < 0.0005
B_regel = 393_298.8                 # Ersatzregel #95 §3.3 statt 65+ = 0
assert abs(B_regel / (B * f_ew) - 0.9969) < 0.0001 and abs(B_zell / B_regel - 1.0021) < 0.0001
assert abs(B_zell / B - 0.980) < 0.0005 and abs(1 - B_zell / B - 0.020) < 0.0005
assert abs(B_regel * delta * c_tag / 1e6 - 4.58) < 0.005
assert 707_318 - 694_397 == 12_921
```

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
  **Begründung des Zahlenwerts ohne Fundstelle** (§3.8: Datenlücke ausdrücklich
  benannt): Eine bundesweite Gattungsstatistik der Siedlungsgehölze existiert
  nicht, und kommunale Baumkataster sind weder einheitlich noch keyless
  aggregierbar — es wird daher **keine** Prozentzahl aus der Literatur zitiert.
  Der Ansatz 0,12 ist eine **Setzung zwischen zwei Ankern**: Straßenbaum-
  bestände enthalten Birke/Erle als Nebenbaumarten (unteres Bandende 0,05),
  Park- und Gehölzstrukturen mit Hasel/Hainbuche liegen deutlich höher (oberes
  Bandende 0,25); der Basiswert ist die Mitte dieser Spanne. Band 0,05–0,25. **Ergebnis-Sensitivität** (Bandbreite über den dokumentierten
  Zelltypen-Satz Allee/Park · Wohnblock · Grünanlage · Mischlage, jeweils
  \(\hat G/\bar G\) bei s_unbek 0,05 → 0,25):
  gehölzreich 0,665 → 0,752 (**+13,0 %**), vegetationsarm 0,255 → 0,258
  (+0,9 %), grünlastig 2,014 → 1,918 (**−4,7 %**), Mischlage 1,066 → 1,072
  (+0,6 %) — die Wirkung hängt vom Vegetationsprofil der Zelle ab und liegt für
  gehölzgeprägte Zellen im **zweistelligen Prozentbereich**, für die übrigen
  darunter. Die **Kommunensumme bleibt unverändert** (Zentrierung); betroffen ist
  ausschließlich die Verteilung innerhalb der Kommune. Reproduzierbar mit dem
  Golden-Test `test_s_unbekannt_sensitivity_band`. Ersetzbar durch ein
  kommunales Baumkataster (Fortschreibungsvermerk); Gräser-Proxy = Grün-/Wiesenanteil der Zelle;
  Gewichte aus den δ-Beiträgen: \(w_B\) = 0,55·4,79/(0,55·4,79 + 0,75·4,06) =
  2,6345/5,6795 = **0,464**. \(w_B\) ist **kein Registry-Parameter**, sondern
  eine **Definitionskonstante der Ebene** (`indicators.POLLEN_G_WEIGHT_BIRKE`):
  Sie gehört zur Ebenen-Definition und darf sich zur Laufzeit nicht bewegen —
  sonst verschöbe ein Schicht-B-Parameter den Schicht-A-Hazard (Ledger-Befunde
  138/142). Die **Kopplung an \(p_B\)/\(p_G\)/\(\Delta S_{\text{DE}}\) ist
  testgebunden** (§3.9: Kopplung benennen und bei Änderung neu rechnen) — der
  Golden-Test `test_veg_weight_derives_from_delta_contributions` wird rot,
  sobald einer dieser Werte ohne Nachziehen der Konstante geändert wird; ein
  zweiter Test (`test_layer_is_independent_of_layer_b_parameters`) hält die
  Schichtentrennung fest. \(\bar G\) dagegen wird im Lauf
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
| \(w_B\) | Gewicht der Gehölz-Komponente in \(\hat G\) (Gräser: \(1-w_B\)) | — | **0,464** = \(p_B\Delta S_{B,\text{DE}}/(p_B\Delta S_{B,\text{DE}} + p_G\Delta S_{G,\text{DE}})\) = 2,6345/5,6795 = 0,46386 (auf 3 NK gerundet); **Definitionskonstante der Ebene, kein Registry-Parameter** (`POLLEN_G_WEIGHT_BIRKE`) — zur Laufzeit unveränderlich, damit Schicht-B-Parameter den Schicht-A-Hazard nicht bewegen; die Kopplung an \(p_B\)/\(p_G\)/\(\Delta S_{\text{DE}}\) ist testgebunden (§3.9); herleitung:#p-hat |
| \(\hat G_{\text{Zelle}}/\bar G\) | Anteil allergener Vegetation, normiert auf das **Kommunenmittel** (Ebene POLLEN_LOAD) | — | OSM-Gehölz-/Grünstruktur; \(\bar G\) = betroffenengewichtetes Mittel der **eigenen Kommune** ⇒ Mittel = 1 per Konstruktion (§3.3, Rev. 2); herleitung:#p-hat |
| \(J\) | Jultag des Phaseneintritts (DWD-Phänologie) | Tag | DWD-CDC Jahresmelder [33] |
| \(L_B,\ L_G\) | Saisonlänge Birkengruppe/Gräser (nach EAACI-Kriterium) | Tage | **30** (20–45) / **60** (45–80) — gekennzeichnete Abschätzung §3.5 [51]; herleitung:#d-saison |
| \(\lambda\) | Gewicht der lokalen Vegetations-Modulation | — | **0,7** (0,3–1,0) = \(2(R-1)/(R+1)\) × \(a_{\text{veg}}\) — Kette §3.4 (Lesart dokumentiert), gekennzeichnete Abschätzung [54–56]; register:96-W024-01; herleitung:#lambda-veg |
| \(p_{\text{AR},a}\) | 12-Monats-Prävalenz allergische Rhinitis je Band | — | **8,8/13,2/6,7/5,0/5,0 %** (u20/20–64/65–74/75–84/85+); Gewichtung §3.2 [1,2,48]; register:96-R35-01; herleitung:#p-ar |
| \(p_B,\ p_G\) | Anteil der AR-Patienten mit Birkengruppen-/Gräser-Saison | — | **0,55** (0,4–0,7) / **0,75** (0,6–0,85) — gekennzeichnete Abschätzung (§3.4) [3]; register:96-R35-02; herleitung:#p-sens |
| \(\hat P_{\text{Zelle}}\) | lokaler Pollen-Hazard-Faktor (auf die **Kommune** zentriert; in ΔTage **und** €) | — | \(1+\lambda(\hat G/\bar G - 1)\); Spanne bei \(\hat G/\bar G\) = 0,5…1,5: 0,65…1,35; ohne Kommunen-Referenz \(\hat P \equiv 1\) (§3.3); berechnet |
| \(\text{pop}_a\) | Bevölkerung der Zelle je Band | Personen | Zensus 2022, 100 m (+ Ebene u20 neu); register:96-R35-01 |
| \(r_{\text{S158}}\) | Wirkungsfaktor der Pollen-Frühwarnung **je gewarntem Tag** (**nur Maßnahmen-Modul**, nicht im Basiswert) | — | **0,03** (Band 0,005–0,10) = \(q_{\text{reich}} q_{\text{handel}} e_{\text{Tag}}\) = 0,35·0,40·0,20 — **§3.9 ABGESCHÄTZT, keine Primärquelle** (Vorgabe P2); Kette, Bandenden und Sensitivität in §5.1; register:96-S158-01; herleitung:#s158-wirkung |
| \(t_{\text{warn},g}\) | Anteil der zusätzlichen Symptomtage der Pollengruppe \(g\) (B, G), an denen der DWD-Index mindestens „mittel“ meldet (gewarnte Tage; nur Maßnahmen-Modul; nicht zu verwechseln mit dem Ĝ-Gewicht \(w_B\)) | — | **0,75** (Band 0,50–1,00), beide Gruppen — **§3.9 ABGESCHÄTZT**; Schwelle nach DWD [70], Ersetzungspfad \(\min(1;\ m_{g,V}/f)\) aus [71]; herleitung:#s158-wirkung |
| \(m_{g,V}\) | Anteil **aller** Tage der Dekaden mit Zusatztagen, an denen der DWD-Index der Gruppe \(g\) im DWD-Gebiet \(V\) mindestens „mittel“ meldet (nur Ersetzungspfad von \(t_{\text{warn}}\)) | — | noch nicht ausgewertet; Quelle DWD-Pollenflugstatistik [71]; wird über \(m_{g,V}/f\) umgerechnet, nie direkt eingesetzt; herleitung:#s158-wirkung |
| \(V\) | Gebiet des DWD-Pollenflug-Gefahrenindex (12 Gebiete mit 27 Vorhersageflächen [72]), für das [71] den Anteil ausweist; **nicht** die Modellregion \(R\) (Nord/Mitte/Süd, §3.3). Jedes Gebiet liegt in genau einer Modellregion | — | Zuordnung Zelle → DWD-Gebiet über das Bundesland (und das Teilgebiet) der Zelle; herleitung:#s158-wirkung |
| \(A_{\text{Zelle}}\) | Geltungsbereich der Pollen-Frühwarnung: 1, wenn die Zelle im Gebiet der kommunalen Warnkanäle liegt, sonst 0 (Eingabe im Maßnahmen-Modul) | — | Eingabe des Nutzers, kein Parameter; herleitung:#s158-wirkung |
| \(\delta_B,\ \delta_G\) | Zusatztage je Betroffenem der Birkengruppe bzw. der Gräser, \(\delta_B + \delta_G = \delta_R\) | Tage/(Betroffener·Jahr) | Teilung von \(\delta_R\) nach den beiden Summanden (§3.3); Berlin 0,8085 / 1,0710; herleitung:#s158-wirkung |

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
  um Δ\(\hat G/\bar G\) = −0,2 senkt, senkt \(\hat P\) **dieser Zelle** um
  \(\lambda \times 0{,}2\) = 0,14 (Band 0,06–0,20 über das λ-Band 0,3–1,0); in einer Zelle mit
  \(\hat P\) = 1 sind das 14 % ihrer Zusatztage. Artenwahl nach GALK-/allergologischer Liste [6].
  **Abschätzung am Zahlenbeispiel (§3.9 ABGESCHÄTZT, Log 24):** Eine Allee-Zelle in Berlin mit
  100 Betroffenen und \(\hat G/\bar G\) = 2 hat \(\hat P\) = 1,7 und 100 × 1,8795 × 1,7 = 319,5
  Zusatztage; nach der Pflanzung ist \(\hat G/\bar G\) = 1,8, \(\hat P\) = 1,56, also 293,2 Tage.
  **Wirkung: −26,3 Tage je Jahr (−8,2 %), ≈ 163 € je Jahr** (\(c_{\text{Tag}}\) = 6,20 €); Band über
  λ: −11,3 Tage (λ = 0,3) bis −37,6 Tage (λ = 1,0). **Sensitivität:** linear in λ und in der
  Senkung Δ\(\hat G/\bar G\); stärkster Treiber ist λ (Faktor 3,3 zwischen den Bandenden).
  **Wirkungsort:** ausschließlich über \(\hat G\) der Zelle, die im Zelllauf neu berechnet wird.
  **Reichweite des Hebels (Rev. 2, Log 19) — Modellgrenze der Abschätzung:** Buchbar ist die
  **Umverteilung** — ein Programm, das gezielt die belasteten Zellen entschärft (Hotspots an
  Alleen/Parks in dicht bewohnten Blöcken), senkt die Symptomtage dort, wo viele Betroffene
  wohnen. Die **Kommunensumme bleibt dabei gleich**: \(\bar G\) wird in jedem Lauf neu gebildet,
  und \(\sum B\hat P = \sum B\) gilt für jedes Vegetationsfeld (§3.3); die 26,3 Tage verteilen sich
  auf die übrigen Zellen. Das ist keine Nullwirkung im Sinn von P2: Die Wirkung je Zelle ist oben
  mit Zahl, Band und Sensitivität abgeschätzt, und die gleichbleibende Summe folgt rechnerisch aus
  der Zentrierung; sie ist die dokumentierte Grenze der Evidenz (Modellgrenze 7), keine gesetzte
  Null. **Produktstand, ehrlich benannt:** Im Produkt ist die Wirkung heute **nicht** sichtbar. Die
  Sperre aus Befund 124 lässt keine Maßnahme auf #96 zu (`linked_risk_codes` leer,
  `test_no_flat_measure_on_allergy_days`), eine Katalogmaßnahme zur Stadtbaumwahl gibt es nicht, und
  das Maßnahmen-Modul rechnet \(\hat G\) nicht neu. **Integrationsauflage (Stadtbaumwahl)**, im
  Rahmen der Auflage aus §3.3 (nur zellscharfe Änderung von \(\hat G\) mit Neuberechnung, nie ein
  Faktor): Der CTO braucht (1) die vom Nutzer gewählten Zellen, (2) die Senkung des allergenen
  Gehölzanteils in diesen Zellen (Beispiel: \(\hat G/\bar G\) um 0,2), (3) den Zelllauf mit
  neu gebildetem \(\bar G\) und neuem \(\hat P\) je Zelle und (4) als Ausgabe die Änderung der
  Zusatztage und Euro je Zelle, gekennzeichnet als „Abschätzung von KAP3“, mit dem Hinweis, dass die
  Kommunensumme gleich bleibt (Modellgrenze 7). Ein **flächiges**
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
- **Pollenmonitoring / Frühwarnung (S158): abgeschätzt** — bis Rev. 2 als „qualitativ"
  (Wirkung null) geführt; seit der Fortschreibung der Aufgabe §3.5 (06.09.2026, Vorgabe P2
  des Aufsichtsrats) mit einer begründeten Abschätzung \(r_{\text{S158}}\) = **0,03**
  (Band 0,005–0,10) hinterlegt. Vollständige Herleitung, Bandenden, Sensitivität und
  Modellgrenze: **§5.1** (`#s158-wirkung`). Die Ebene EARLY_WARNING_SYSTEMS
  (DWD/PID-Gefahrenindex) bleibt zugleich Screening-/Informationsebene der Schicht A und
  geht **nicht** in den Basiswert der Schadensformel ein (dort weiterhin Default 1).
- **R7-Weiche:** nicht einschlägig — keine Vorsorge-Buchung berührt (#96 hat keine
  K8-Gegenbuchung in der Netzwerkliste); Stadtbaum-Programmkosten sind kommunale
  Maßnahmenkosten außerhalb der Schadenskonten (Anzeige im Maßnahmen-Modul, keine
  K-Buchung).

### 5.1 Wirkungsabschätzung S158 Pollen-Frühwarnung (Anker `#s158-wirkung`) — §3.9 **ABGESCHÄTZT**

**Anlass und Geltung.** Vorgabe P2 des Aufsichtsrats (Freigabe F-0007, 06.09.2026) und die
daraus folgende Fortschreibung der Aufgabe §3.5: Ein Maßnahmen-Hebel ohne publizierte
Interventions-Effektgröße läuft **nicht mehr als „qualitativ" mit Wirkung null**, sondern
erhält eine begründete Abschätzung nach §3.9 (Zahlenwert mit Begründung, Bandbreite,
Ergebnis-Sensitivität), die im Produkt als „Abschätzung von KAP3" mit Herleitung ausgewiesen
wird. Die Registerfeststellung 96-S158-01 („keine quantifizierte Interventions-Effektgröße
publiziert") bleibt sachlich unverändert richtig — sie ist ab hier der **Anlass** der
Abschätzung, nicht ihr Ersatz. Die Entscheidung Log 15 („qualitativ") wird damit bewusst
überstimmt; Entscheidungslog **Nr. 20**, Ledger-Befund **151**.

**§3.9-Kategorie ABGESCHÄTZT — keine Primärquelle.** Für Einführung oder Ausbau kommunaler
Pollen-Frühwarnung existiert keine Interventions- oder quasi-experimentelle Studie mit einer
Effektgröße auf Symptomtage; anders als beim Hitzewarnsystem (#95, Register 95-S158-01:
Feldbusch 2025, Urban 2025) ist die Evidenzlage hier leer. Deshalb wird — wie bei
\(s_{\text{unbek}}\) (§3.3) — **keine Effektzahl aus der Literatur zitiert** (§3.8-Datenlücke,
ausdrücklich benannt). Der Zahlenwert entsteht aus einer offengelegten Wirkungskette; jeder
ihrer drei Faktoren ist eine **Setzung zwischen zwei benannten Ankern**, der Basiswert die
Mitte der jeweiligen Spanne. Kategorien-Disziplin (§3.9): Keiner der Faktoren ist eine aus
einer fremden Größe umgedeutete Zahl — es sind ausgewiesene Annahmen, keine
Beobachtungswerte.

**Wirkungsort (§3.5, definiert).** Die Warnung ändert weder die Pollenmenge noch die
Vegetation \(\hat G\), sondern das Verhalten der Betroffenen an den belasteten Tagen
(Lüften/Aufenthalt im Freien, rechtzeitig statt nachlaufend begonnene Bedarfsmedikation).
Sie wirkt daher auf den klimaattribuierten Zusatzblock \(\Delta\text{Tage}_{\text{Zelle}}\), und
zwar **nur auf dessen gewarnten Teil** (Festlegung unten), und über die strikte
Proportionalität (§3.3) im gleichen Verhältnis auf €. Sie wirkt **nicht** auf \(\Delta S\)
(gemessenes Klimasignal), **nicht** auf \(B\) (Prävalenz) und **nicht** über \(\hat G/\lambda\).
**Doppelzählungs-Wächter:** kein zweiter Kanal zur allergenarmen Stadtbaumwahl (die wirkt
ausschließlich über \(\hat G\)) und keine Überschneidung mit R36 (HEALTHCARE_ACCESS, Default 1);
die Kalibrierjahre enthalten keinen Frühwarn-Effekt, der bereits eingerechnet wäre
(\(c_{\text{kal}} \equiv 1\), kein Fit).

**An welchen Tagen und ab welcher Belastung die Warnung wirkt (Festlegung, T-1239).**

- **Belastungsschwelle: Pollenflug-Gefahrenindex des DWD mindestens „mittlere Belastung“
  (Stufe 2)** für mindestens eine Pollenart der Gruppe im DWD-Gebiet \(V\) der Zelle. Der DWD
  stuft je Pollenart nach dem Tagesmittel der Pollen je m³ Luft ein [70]:

  | Pollenart | keine | gering | mittel | hoch |
  |---|---|---|---|---|
  | Hasel, Erle (Birkengruppe) | 0 | 1–10 | 11–100 | über 100 |
  | Birke (Birkengruppe) | 0 | 1–10 | 11–50 | über 50 |
  | Gräser | 0 | 1–5 | 6–30 | über 30 |

  Gewarnt ist ein Tag ab „mittel“, also ab 11 Pollen je m³ (Hasel, Erle, Birke) bzw. ab 6 Pollen
  je m³ (Gräser); die Zwischenstufe „gering bis mittel“ zählt nicht, „mittel bis hoch“ und
  „hoch“ zählen mit. Begründung der Stufe (Setzung von KAP3, die Stufen selbst sind DWD [70]):
  Die Warnung ist ein Handlungsanstoß. „gering“ ist die unterste Stufe mit Pollenflug überhaupt;
  ein Anstoß schon dort käme an fast jedem Saisontag und verlöre seine Wirkung als Warnung.
  „mittel“ ist die niedrigste Stufe darüber. Eine strengere Schwelle („hoch“) verkürzt die gewarnten Tage; sie liegt im
  unteren Band von \(t_{\text{warn}}\) (unten).
- **Tagesmenge je Pollengruppe.** Die zusätzlichen Symptomtage je Betroffenem teilen sich
  genau nach den beiden Gruppen der Formel in §3.3:
  \(\delta_{B} = f \cdot p_B \cdot \Delta S_{B,R} \cdot a_{\text{attr}}\) (Birkengruppe) und
  \(\delta_{G} = f \cdot p_G \cdot \Delta S_{G,R} \cdot a_{\text{attr}}\) (Gräser),
  \(\delta_B + \delta_G = \delta_R\). Für Berlin (Region Mitte, §3.0 Ebene 6):
  0,70 × 0,55 × 4,20 × 0,50 = **0,8085 Tage** (Birkengruppe) und 0,70 × 0,75 × 4,08 × 0,50 =
  **1,0710 Tage** (Gräser), zusammen 1,8795 Tage. Die Zusatztage liegen am Anfang der jeweiligen
  Saison (Erle/Hasel bzw. Wiesenfuchsschwanz blühen früher, §3.1); die Referenzsaison ist
  \(L_B\) = 30 und \(L_G\) = 60 Tage lang (§3.5). Gewarnt ist davon der Anteil
  \(t_{\text{warn},g}\), an dem der Index die Schwelle erreicht. (Das Zeichen ist eigens gewählt:
  \(w_B\) ist in §3.3 schon das Gewicht der Gehölze in \(\hat G\), 0,464; Ledger-Befund 161.)
- **Anteil gewarnter Zusatztage \(t_{\text{warn},g}\) = 0,75 (Band 0,50–1,00) für beide Gruppen —
  §3.9 ABGESCHÄTZT.** Gemeint ist der Anteil **unter den zusätzlichen Symptomtagen**, nicht unter
  allen Kalendertagen: Die Zusatztage enthalten mit \(f\) schon die Auswahl der Tage, an denen
  Beschwerden auftreten (§3.4). Oberer Anker 1,00: Beschwerden treten nur an Tagen ab „mittel“ auf;
  dann ist jeder zusätzliche Symptomtag ein gewarnter Tag. Das hat Rev. 3 stillschweigend unterstellt.
  Unterer Anker 0,50: Die Zusatztage liegen am Saisonanfang, wo die Konzentration erst ansteigt;
  nur jeder zweite Symptomtag erreicht „mittel“ (deckt auch die strengere Schwelle „hoch“ ab).
  Der Basiswert ist die Mitte. Beide Gruppen tragen denselben Wert, weil es keine Auswertung je
  Gruppe gibt; eine Setzung je Gruppe wäre Scheingenauigkeit.
- **Ersetzungspfad für \(t_{\text{warn},g}\), ohne Verdünnung.** Die Pollenflugstatistik des DWD [71]
  (Anteil der Meldungen je Belastungsstufe in Zehntagesmitteln, je Pollenart und Gebiet,
  1997–2026) liefert für die Dekaden, in denen die Zusatztage liegen, je DWD-Gebiet \(V\) den Anteil \(m_{g,V}\)
  **aller** Tage mit Index ab „mittel“. Das ist nicht \(t_{\text{warn}}\): Setzte man \(m_{g,V}\)
  direkt ein, wählte die Rechnung die Tage zweimal aus (einmal über \(f\), einmal über \(m\)), und
  die Wirkung fiele um den Faktor \(f\) zu tief aus. Umgerechnet wird deshalb
  \(t_{\text{warn},g,V} = \min(1;\ m_{g,V}/f)\), unter der Annahme, dass die Beschwerden an den Tagen
  mit der höchsten Belastung auftreten (Pollenflug treibt die Symptomlast, Pfaar [52], qualitativ).
  Zahlenbeispiel: Meldet [71] für die Dekaden der Zusatztage \(m\) = 0,525, dann ist
  \(t_{\text{warn}}\) = 0,525 / 0,70 = 0,75, der heutige Basiswert; direkt eingesetzt ergäbe
  \(m\) = 0,525 nur 70 % der Wirkung. Treten die Beschwerden unabhängig von der Belastung auf, ist
  \(m\) selbst der richtige Wert; das widerspricht [52] und ist deshalb nur die Untergrenze.

**Wirkt \(e_{\text{Tag}}\) schon je gewarntem Tag? Ja.** Seine Anker beschreiben die Minderung an
einem Tag, an dem die Person handelt: 0,10 „Expositionsvermeidung deckt nur einen Teil des Tages
ab“, 0,30 „Expositionsvermeidung und rechtzeitig begonnene Bedarfsmedikation“. Handeln kann sie
nur an einem Tag, an dem gewarnt wird. \(r_{\text{S158}} = q_{\text{reich}} q_{\text{handel}}
e_{\text{Tag}}\) ist damit die **Wirkung je gewarntem Tag**; der Wert 0,03 in Kapitel 7 bleibt.
Rev. 3 hat ihn auf alle Zusatztage gerechnet und damit \(t_{\text{warn}} = 1\) unterstellt. Die
Tagesauswahl wendet den Effekt **nicht doppelt** an: \(t_{\text{warn}}\) zählt Tage,
\(q_{\text{reich}}\) und \(q_{\text{handel}}\) zählen Menschen, \(e_{\text{Tag}}\) misst die Minderung
an einem Tag, jede Größe kommt genau einmal vor. Sie **verdünnt** ihn auch nicht: \(e_{\text{Tag}}\)
= 0,20 wirkt voll an jedem gewarnten Tag und gar nicht an den übrigen, statt auf alle Tage verteilt
zu werden, und \(t_{\text{warn}}\) ist ein Anteil unter den Symptomtagen, nicht unter allen Tagen
(Ersetzungspfad oben). Der **wirksame Wert** über alle Zusatztage sinkt dadurch von 0,03 auf
0,03 × 0,75 = **0,0225**; Entscheidungslog Nr. 23, Ledger-Befunde 157 und 165.

**Formel (zellscharf, im Zelllauf).**

$$ \Delta\text{Tage}^{\,\text{mit S158}}_{\text{Zelle}} \;=\; \Delta\text{Tage}_{\text{Zelle}} \;-\; A_{\text{Zelle}} \cdot r_{\text{S158}} \cdot \sum_{g \in \{B,\,G\}} t_{\text{warn},g} \cdot \Delta\text{Tage}_{g,\text{Zelle}}, \qquad \Delta\text{Tage}_{g,\text{Zelle}} \;=\; B_{\text{Zelle}} \cdot \delta_g \cdot \hat P_{\text{Zelle}} $$

mit \(r_{\text{S158}} = q_{\text{reich}} \cdot q_{\text{handel}} \cdot e_{\text{Tag}}\). \(A_{\text{Zelle}}\)
ist 1, wenn die Zelle im Geltungsbereich der kommunalen Warnkanäle liegt, sonst 0;
\(q_{\text{reich}}\) ist die Reichweite unter den Betroffenen **innerhalb** dieses Bereichs, deshalb
zählt die Fläche nicht doppelt. In Worten: Von den Zusatztagen einer Zelle zählt je Gruppe nur der
gewarnte Teil, und davon wird der Anteil \(r_{\text{S158}}\) vermieden.

**Was die Formel heute von einem Faktor unterscheidet — und was nicht.** Mit den heutigen Werten
ist \(t_{\text{warn}}\) für beide Gruppen gleich (0,75). Die Formel mindert dann jede Zelle im
Geltungsbereich um denselben Anteil ihrer Zusatztage, 0,03 × 0,75 = 2,25 %. Das Ergebnis ist
deshalb heute **zahlengleich** mit einem Faktor 0,0225 auf die gespeicherten Zusatztage der Zellen
im Geltungsbereich; für Berlin ergeben beide Wege 16.666 Tage (Zelllauf, unten). Die Festlegung
ändert heute den **Wert**, nicht die Verteilung: 2,25 % statt der 3 % von Rev. 3, weil nur noch
gewarnte Tage zählen. Die Verteilung ändert erst der Ersetzungspfad: Mit \(t_{\text{warn},g,V}\) je
Gruppe und DWD-Gebiet \(V\) hängt der Anteil am Gebiet und an der Mischung aus Birken- und
Gräsertagen (Nord, Mitte und Süd teilen \(\delta\) verschieden, §3.3). Innerhalb eines
DWD-Gebiets \(V\) bleibt er auch dann für alle Zellen gleich, weil \(\hat P\) die Zusatztage beider
Gruppen im gleichen Verhältnis hebt und jedes DWD-Gebiet in genau einer Modellregion \(R\) liegt,
also überall dieselbe Teilung von \(\delta\) hat. Die Bedingung ist erfüllt: Die Gebiete folgen den
Ländergrenzen, zusammengefasst sind nur Länder derselben Modellregion (Schleswig-Holstein und
Hamburg, Niedersachsen und Bremen: Nord; Brandenburg und Berlin, Rheinland-Pfalz und Saarland:
Mitte; Gebietsliste [72], Regionen nach §3.3). Das ist der Teil, der vom Pauschalfaktor bleibt
(Modellgrenze 8, §6; Ledger-Befund 163).

**Kette und Zahlenwert.**

| Faktor | Bedeutung | Basiswert | unterer Anker | oberer Anker |
|---|---|---|---|---|
| \(q_{\text{reich}}\) | Anteil der AR-Betroffenen im Geltungsbereich, den das Warnangebot in der Saison tatsächlich erreicht | **0,35** | 0,20 — bereitgestellter Index ohne aktive Kanäle | 0,55 — aktive Kanäle (App-Push, Presse, Schul-/Kita-Information) |
| \(q_{\text{handel}}\) | Anteil der Erreichten, der die Information in eine Handlung übersetzt | **0,40** | 0,25 — Kenntnisnahme ohne Verhaltensänderung | 0,60 — Betroffene mit hohem Leidensdruck und eingeübter Bedarfsmedikation |
| \(e_{\text{Tag}}\) | relative Minderung der Symptomlast an einem gewarnten Zusatztag bei tatsächlich geändertem Verhalten | **0,20** | 0,10 — Expositionsvermeidung deckt nur einen Teil des Tages ab | 0,30 — Expositionsvermeidung **und** rechtzeitig begonnene Bedarfsmedikation |
| \(t_{\text{warn},g}\) | Anteil der zusätzlichen Symptomtage der Gruppe mit Index mindestens „mittel“ (gewarnte Tage) | **0,75** | 0,50 — Saisonanfang, Konzentration steigt erst an | 1,00 — jeder Symptomtag liegt ab „mittel“ |

\(r_{\text{S158}} = 0{,}35 \cdot 0{,}40 \cdot 0{,}20 = 0{,}028\) ⇒ **Basiswert
\(r_{\text{S158}}\) = 0,03 (3 %) je gewarntem Tag**, wirksam über alle Zusatztage
0,03 × 0,75 = 0,0225 — ausdrücklich **größer null**: Die fehlende Interventionsstudie begründet die
Kennzeichnung als Abschätzung, nicht eine Nullwirkung.

**Bandbreite mit zwei benannten Bandenden:**

- unteres Bandende **„Aushang-Fall“** (Index wird bereitgestellt, aber nicht aktiv verteilt,
  keine eingeübte Handlung): 0,20 · 0,25 · 0,10 = **0,005 (0,5 %)** je gewarntem Tag, mit
  \(t_{\text{warn}}\) = 0,50 wirksam 0,0025;
- oberes Bandende **„aktivierte Warnkette“** (aktive Kanäle, eingeübte Bedarfsmedikation,
  hohe Handlungsbereitschaft): 0,55 · 0,60 · 0,30 = 0,099 ⇒ **0,10 (10 %)** je gewarntem Tag, mit
  \(t_{\text{warn}}\) = 1,00 wirksam ebenso 0,10.

Band \(r_{\text{S158}} \in [0{,}005;\ 0{,}10]\) je gewarntem Tag (unverändert), wirksam
\([0{,}0025;\ 0{,}10]\); der Basiswert liegt bewusst näher am unteren Ende (Untergrenzen-Zusage
Kap. 1).

**Beispielkommune Berlin (wie §3.0, Schritt 1), Geltungsbereich ganze Stadt (\(A\) = 1).**

| Schritt | Rechnung | Wert |
|---|---|---|
| 1 | Zusatztage Birkengruppe \(B \times \delta_B\) | 402.103 × 0,8085 = **325.100 Tage** |
| 2 | Zusatztage Gräser \(B \times \delta_G\) | 402.103 × 1,0710 = **430.652 Tage** (zusammen 755.753 wie §3.0 Ebene 8) |
| 3 | davon gewarnt (\(t_{\text{warn}}\) = 0,75) | 243.825 + 322.989 = **566.814 Tage** |
| 4 | vermieden (\(r_{\text{S158}}\) = 0,03) | 566.814 × 0,03 = **17.004 Tage je Jahr** (2,25 % der Zusatztage) |
| 5 | in Euro (\(c_{\text{Tag}}\) = 6,20 €) | 17.004 × 6,20 € = **≈ 105.400 € je Jahr** (Preisstand 2024) |

Band: 1.889 Tage (≈ 11.700 €) bis 75.575 Tage (≈ 468.600 €) je Jahr. Der Zelllauf des Produkts
(740.723 Tage, §3.0) ergibt 16.666 Tage und ≈ 103.300 €, Zelle für Zelle gerechnet und ebenso als
Faktor 0,0225 auf die Summe: heute zahlengleich (siehe oben). Rev. 3 hätte ohne Tagesauswahl 22.673 Tage
und ≈ 140.600 € ausgewiesen, ein Drittel mehr. Zellscharf: Eine Allee-Zelle mit 100 Betroffenen
und \(\hat P\) = 1,7 hat 100 × 1,8795 × 1,7 = 319,5 Zusatztage; im Geltungsbereich werden davon
7,19 Tage (≈ 45 €) vermieden, außerhalb (\(A\) = 0) keine.

**Ergebnis-Sensitivität (§3.9).** Alle vier Faktoren wirken linear. **Stärkster Treiber ist
\(e_{\text{Tag}}\)**: zwischen seinen Ankern liegt der Faktor 3 (für Berlin 8.502–25.507 Tage,
≈ 52.700–158.100 €), vor \(q_{\text{reich}}\) (Faktor 2,75), \(q_{\text{handel}}\) (2,4) und
\(t_{\text{warn}}\) (2,0; 11.336–22.673 Tage). Der Schadenswert selbst bleibt unberührt, solange die Maßnahme
nicht gewählt ist. Bezogen auf die §4-Bundessumme von ≈ 110 Mio. €₂₀₂₄ je Jahr entspricht der
Basiswert bei flächendeckender Umsetzung **≈ 2,5 Mio. € je Jahr** vermiedener Behandlungskosten
(Band ≈ 0,28–11,0 Mio. €). Ob sich die Maßnahme trägt, rechnet das Maßnahmen-Modul gegen die
Vorhaltekosten (Katalog `POLLEN_EARLY_WARNING`: 15.000 € Anschaffung je Station, 4.000 € je
Station und Jahr Betrieb); die Abschätzung macht die Wirkung dafür sichtbar, statt sie als Null
auszuweisen.

```python test: beispiel_96_s158_wirkung
# S158 nach Tagen und Belastung (T-1239), Beispielkommune Berlin wie Rechenkette 3.0
q_reich, q_handel, e_tag = 0.35, 0.40, 0.20
r_roh = q_reich * q_handel * e_tag
assert abs(r_roh - 0.028) < 1e-9 and round(r_roh, 2) == 0.03   # je gewarntem Tag, > 0
r = 0.03                                                     # Kap. 7 pollen.r_s158
t_warn = 0.75                                                # Kap. 7 pollen.t_warn_s158
assert abs(r * t_warn - 0.0225) < 1e-12                           # ein wirksamer Wert (Befund 165)
# Bandenden je gewarntem Tag (unveraendert) und wirksam
unten, oben = 0.20 * 0.25 * 0.10, 0.55 * 0.60 * 0.30
assert abs(unten - 0.005) < 1e-9 and round(oben, 2) == 0.10
assert abs(unten * 0.50 - 0.0025) < 1e-12
# Tagesmenge je Pollengruppe, Region Mitte (§3.0 Ebenen 4-6)
f, p_B, p_G, a_attr, dS_B, dS_G = 0.70, 0.55, 0.75, 0.50, 4.20, 4.08
d_B, d_G = f * p_B * dS_B * a_attr, f * p_G * dS_G * a_attr
assert abs(d_B - 0.8085) < 1e-9 and abs(d_G - 1.0710) < 1e-9
assert abs(d_B + d_G - 1.8795) < 1e-9
B, c_tag = 402_103, 6.20
t_B, t_G = B * d_B, B * d_G
assert abs(t_B - 325_100) < 1 and abs(t_G - 430_652) < 1 and abs(t_B + t_G - 755_753) < 1
A = 1                                                        # ganze Stadt im Geltungsbereich
gewarnt = t_warn * t_B + t_warn * t_G
assert abs(gewarnt - 566_814) < 1
vermieden = A * r * gewarnt
assert abs(vermieden - 17_004) < 1 and abs(vermieden / (t_B + t_G) - 0.0225) < 1e-9
assert abs(vermieden * c_tag - 105_400) < 100
# Band (Aushang-Fall mit t_warn 0,50; aktivierte Warnkette mit t_warn 1,00)
t = t_B + t_G
assert abs(unten * 0.50 * t - 1_889) < 1 and abs(unten * 0.50 * t * c_tag - 11_700) < 50
assert abs(0.10 * 1.00 * t - 75_575) < 1 and abs(0.10 * 1.00 * t * c_tag - 468_600) < 50
# Zelllauf des Produkts, Rev. 3 zum Vergleich, eine Allee-Zelle
assert abs(740_723 * r * t_warn - 16_666) < 1 and abs(740_723 * r * t_warn * c_tag - 103_300) < 50
assert abs(r * t - 22_673) < 1 and abs(r * t * c_tag - 140_600) < 50
zelle = 100 * 1.8795 * 1.7
assert abs(zelle - 319.5) < 0.05 and abs(A * r * t_warn * zelle - 7.19) < 0.005
assert abs(A * r * t_warn * zelle * c_tag - 45) < 0.5 and 0 * r * t_warn * zelle == 0
# Sensitivitaet: e_Tag staerkster Treiber (Faktor 3), dann q_reich, q_handel, t_warn
spannen = {"e_tag": 0.30 / 0.10, "q_reich": 0.55 / 0.20, "q_handel": 0.60 / 0.25, "t_warn": 1.00 / 0.50}
assert max(spannen, key=spannen.get) == "e_tag"
assert abs(spannen["q_reich"] - 2.75) < 1e-9 and abs(spannen["q_handel"] - 2.4) < 1e-9
assert abs(vermieden * 0.10 / 0.20 - 8_502) < 1 and abs(vermieden * 0.30 / 0.20 - 25_507) < 1
assert abs(vermieden * 0.10 / 0.20 * c_tag - 52_700) < 50
assert abs(vermieden * 0.30 / 0.20 * c_tag - 158_100) < 50
assert abs(vermieden * 0.50 / 0.75 - 11_336) < 1 and abs(vermieden * 1.00 / 0.75 - 22_673) < 1
# Ersetzungspfad ohne Verduennung (Befund 162): DWD-Anteil aller Tage m -> t_warn = min(1, m/f)
m = 0.525
assert abs(min(1.0, m / f) - t_warn) < 1e-9
assert abs(m / t_warn - f) < 1e-9                            # m direkt eingesetzt: nur 70 % der Wirkung
assert min(1.0, 0.80 / f) == 1.0                             # Deckel bei 1
# Heute zahlengleich mit einem Faktor auf die gespeicherten Zusatztage (Befund 163)
faktor = r * t_warn
zellen = [(100, 1.7), (250, 1.0), (40, 0.3)]                 # (Betroffene, P^) im Geltungsbereich
for b_z, p_z in zellen:
    tage_g = [b_z * d_B * p_z, b_z * d_G * p_z]
    formel = A * r * sum(t_warn * x for x in tage_g)
    assert abs(formel - faktor * sum(tage_g)) < 1e-9
# Nach dem Ersetzungspfad: je Region verschieden, weil Nord, Mitte, Sued delta verschieden teilen
tw_B, tw_G = 0.60, 0.90                                      # Beispielwerte je Gruppe, keine Festlegung
def gewarnt_anteil(dS_b, dS_g):
    return (tw_B * p_B * dS_b + tw_G * p_G * dS_g) / (p_B * dS_b + p_G * dS_g)
nord, sued = gewarnt_anteil(3.96, 4.78), gewarnt_anteil(5.94, 3.70)
assert abs(nord - 0.787) < 0.001 and abs(sued - 0.738) < 0.001
# Bundessumme (§4-Sanity ~110 Mio EUR_2024 je Jahr)
bund = 110e6
assert abs(r * t_warn * bund / 1e6 - 2.5) < 0.03
assert abs(unten * 0.50 * bund / 1e6 - 0.28) < 0.01 and abs(0.10 * bund / 1e6 - 11.0) < 0.01
```

**Integrationsauflage (S158).** Der CTO verknüpft die Maßnahme nach der Abnahme so, dass sie im
Zelllauf rechnet, nicht als Faktor auf gespeicherte Ergebnisse. Er braucht dafür:

1. die Zusatztage je Zelle **getrennt nach Gruppe**, \(\Delta\text{Tage}_{B,\text{Zelle}}\) und
   \(\Delta\text{Tage}_{G,\text{Zelle}}\) (heute führt die Schicht-B-Funktion nur ihre Summe);
2. den Anteil gewarnter Tage \(t_{\text{warn},g}\) (Kapitel 7 `pollen.t_warn_s158`, 0,75 für beide
   Gruppen; nach dem Ersetzungspfad \(t_{\text{warn},g,V} = \min(1;\ m_{g,V}/f)\) je
   DWD-Gebiet \(V\) aus [71], dazu die Zuordnung Zelle → DWD-Gebiet (über Bundesland und
   Teilgebiet der Zelle, Gebietsliste [72]) — **nicht** den DWD-Anteil \(m_{g,V}\) selbst, der die Wirkung um
   den Faktor \(f\) verdünnen würde);
3. den Wirkungsfaktor je gewarntem Tag \(r_{\text{S158}}\) (Kapitel 7 `pollen.r_s158`, 0,03);
4. den Geltungsbereich \(A_{\text{Zelle}}\) als Eingabe im Maßnahmen-Modul (ganze Kommune oder
   ausgewählte Gebiete);
5. als Ausgabe die vermiedenen Tage und Euro je Zelle und für die Kommune, gekennzeichnet als
   „Abschätzung von KAP3“ (Vorgabe P1).

Die Sperre aus Befund 124 gilt weiter: `linked_risk_codes` für `EXPECTED_ANNUAL_ALLERGY_DAYS` bleibt
leer, der Test `test_no_flat_measure_on_allergy_days` bleibt grün, `default_reduction` im Katalog
bleibt 0,0, bis der CTO die Rechnung im Zelllauf gebaut hat. Mit den heutigen Werten wäre ein
Faktor 0,0225 auf die gespeicherten Zusatztage der Zellen im Geltungsbereich zahlengleich (siehe
„Was die Formel heute von einem Faktor unterscheidet“). Verlangt wird der Zelllauf mit getrennten
Gruppen trotzdem, weil nur er den Ersetzungspfad ohne Umbau aufnimmt: Mit
\(t_{\text{warn},g,V}\) je Gruppe und DWD-Gebiet gäbe ein einziger Katalogfaktor für alle
Kommunen den falschen Wert.

**Modellgrenze der Abschätzung (Bauform) — nicht Grund für eine Null.** Tage und Belastung sind
jetzt festgelegt, der Geltungsbereich ist zellscharf. Pauschal bleibt der Personenteil
\(q_{\text{reich}} q_{\text{handel}} e_{\text{Tag}}\): Reichweite, Handlungsbereitschaft und
Tageswirkung sind je Zelle nicht beobachtbar und gelten in allen Zellen gleich; dazu
\(t_{\text{warn}}\), solange keine Auswertung je DWD-Gebiet \(V\) vorliegt. Heute mindert die
Maßnahme deshalb jede Zelle im Geltungsbereich um denselben Anteil (2,25 %), zahlengleich mit einem
Faktor. Das ist die **Modellgrenze der Abschätzung** (§6, Modellgrenze 8); sie wird dokumentiert,
nicht als Argument für Wirkung null verwendet (Aufgabe §3.5, Fortschreibung 06.09.2026).
**Ersetzungspfad:** eine Vorher-Nachher-/DiD-Auswertung von Symptomtagebuch-Daten (Patient's
Hayfever Diary) gegen die Einführung kommunaler Warnkanäle ersetzt den Personenteil durch eine
gemessene Effektgröße, die DWD-Pollenflugstatistik [71] den Anteil \(t_{\text{warn}}\) (umgerechnet
über \(m_{g,V}/f\), siehe oben); bis dahin ist die Kette oben der vollständige Nachweis des Werts.

**Abgrenzung zu Modellgrenze 7 / Ledger-Befund 124 — beide bleiben bestehen.**
Modellgrenze 7 verbietet einen **Vegetations-Niveaueffekt**: Ein flächiges Pflanzprogramm
darf nicht über \(\hat G/\lambda\) gebucht werden, weil die λ-Evidenz intra-urban ist.
\(r_{\text{S158}}\) ist kein Vegetationskanal, sondern eine Verhaltens-/Expositionsminderung an
gewarnten Tagen, inhaltlich also keine Verletzung von Modellgrenze 7. Die Sperre aus Befund 124
bleibt **unangetastet** (Integrationsauflage oben). Die Divergenz Bericht ⇄ Code ist
**ausgewiesen und im Ledger geführt** (Befunde 151 und 156), nicht still (Eiserne Regel 5).

**Produkt-Kennzeichnung (§3.6/Vorgabe P1).** In der nutzersichtbaren Parameterliste tragen
\(r_{\text{S158}}\) und \(t_{\text{warn}}\) den Vermerk „Abschätzung von KAP3“ mit dieser Herleitung (Schwelle
„mittel“ nach DWD [70], vier Faktoren mit je zwei Ankern, Band, Sensitivität, Modellgrenze 8,
Ersetzungspfad); eine Herleitung allein als Code-Kommentar genügt nicht.

## 6 Szenario-Anwendung & Modellgrenzen (§3.2/§3.6)

**Jahresbeträge ohne Abzinsung.** Alle Euro-Beträge dieses Berichts sind Jahresbeträge ohne Abzinsung: Sie
gelten für ein Jahr im Ist-Klima zum Preisstand 2024 und werden weder über mehrere Jahre summiert noch auf
einen Barwert abgezinst. Die Diskontrate für mehrjährige Rechnungen legt T-1116 fest.

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
8. **Bauform der S158-Abschätzung: was vom Pauschalfaktor bleibt** (§5.1, Vorgabe P2;
   neu gefasst mit T-1239): Seit der Festlegung wirkt die Warnung nur an gewarnten Tagen
   (DWD-Index mindestens „mittel“ [70]), je Pollengruppe und im Zelllauf nur in Zellen im
   Geltungsbereich (\(A_{\text{Zelle}}\)). **Pauschal bleibt** der Personenteil
   \(r_{\text{S158}} = q_{\text{reich}} q_{\text{handel}} e_{\text{Tag}}\) = 0,03 je gewarntem Tag
   (0,005–0,10): Reichweite, Handlungsbereitschaft und Tageswirkung sind je Zelle nicht
   beobachtbar und gelten in allen Zellen gleich. Ebenso pauschal ist vorerst der Anteil
   gewarnter Tage \(t_{\text{warn}}\) = 0,75 (0,50–1,00), gleich für beide Gruppen und alle Regionen.
   Innerhalb des Geltungsbereichs mindert die Maßnahme deshalb jede Zelle um denselben Anteil
   (2,25 %). **Heute ist das zahlengleich mit einem Faktor 0,0225** auf die Zusatztage der Zellen im
   Geltungsbereich: Die Festlegung hat den Wert geändert (nur gewarnte Tage, 2,25 % statt 3 %),
   nicht die Verteilung. Auch nach dem Ersetzungspfad bleibt je DWD-Gebiet \(V\) ein einheitlicher
   Anteil, weil \(\hat P\) beide Gruppen im gleichen Verhältnis hebt und jedes DWD-Gebiet in genau
   einer Modellregion \(R\) liegt ([72], §3.3); er unterscheidet sich dann nur zwischen Gebieten. Das ist eine **Modellgrenze der Abschätzung**, kein Grund für eine
   Nullwirkung; Ersetzungspfad: gemessene Effektgröße aus einer Vorher-Nachher-/DiD-Auswertung von
   Symptomtagebuch-Daten für den Personenteil, DWD-Pollenflugstatistik [71] für
   \(t_{\text{warn},g,V} = \min(1;\ m_{g,V}/f)\).
   Abgrenzung: **Modellgrenze 7 bleibt bestehen** — \(r_{\text{S158}}\) läuft **nicht** über
   \(\hat G/\lambda\) (Verhaltens-, kein Vegetationskanal). **Die Sperre aus Befund 124 bleibt
   bestehen:** kein pauschaler `linked_risk_codes`-Kanal auf #96, Verknüpfung nur im Zelllauf nach
   der Integrationsauflage (S158) in §5.1.

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
  kennzeichnung: quelle   # amtliche DWD-Messreihe [33], ausgewertet mit Anlage [67]
  abgeleitet_aus: []
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
  kennzeichnung: quelle   # Anderegg 2021 [9]
  abgeleitet_aus: []
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
  kennzeichnung: quelle   # DEGS1/KiGGS W2 [1,2]; 80-84 und 85+ extrapoliert, gekennzeichnet in 3.2
  abgeleitet_aus: []
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
  kennzeichnung: abschaetzung_kap3   # Herleitung 3.4 #p-sens
  abgeleitet_aus: []
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
  kennzeichnung: abschaetzung_kap3   # Herleitung 3.5 #d-saison
  abgeleitet_aus: []
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
  kennzeichnung: abschaetzung_kap3   # Herleitung 3.4 #f-sympt
  abgeleitet_aus: []
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
  kennzeichnung: abschaetzung_kap3   # Herleitung 3.4 #lambda-veg
  abgeleitet_aus: []
parameter:
  # Baustein der Ebene POLLEN_LOAD (Detailspezifikation der Integration, §3.3).
  # w_B ist KEIN Parameter-Block: Es ist eine Definitionskonstante der Ebene
  # (indicators.POLLEN_G_WEIGHT_BIRKE = 0,464, hergeleitet aus den delta-
  # Beitraegen). Ein Registry-Wert haette die Kopplung an p_B/p_G tot gestellt
  # (Befund 138), eine Laufzeit-Ableitung haette den Schicht-A-Hazard bewegt
  # (Befund 142) — die Kopplung ist stattdessen testgebunden (§3.9).
  id: pollen.s_unbekannt
  wert: 0.12     # Birkengruppen-Anteil der OSM-Kronen OHNE genus/species-Tag
  einheit: "-"
  band: [0.05, 0.25]   # §3.9 ABGESCHAETZT: keine Primaerquelle (s. #p-hat)
  herkunft: herleitung:#p-hat
  quelle: modellannahme   # bewusst KEIN Quellen-Key: es gibt keine Primaerquelle
  preisstand: null
  bandzuordnung: [u20, 20-64, 65-74, 75-84, 85+]
  endpunkt: morbiditaet
  kennzeichnung: abschaetzung_kap3   # Herleitung 3.3 #p-hat; geht in jedem Lauf in G-Dach ein, daher keine rolle
  abgeleitet_aus: []
parameter:
  # Maßnahmen-Wirkungsfaktor S158 (Vorgabe P2 / Aufgabe §3.5 i. d. F. 06.09.2026).
  # KEIN Parameter der Schadensformel: wirkt ausschliesslich im Maßnahmen-Modul
  # (Katalog POLLEN_EARLY_WARNING, default_reduction). Der Katalogwert steht in
  # dieser Revision noch auf 0,0 — Code-Nachzug als eigener Schritt (L2), damit
  # die Parameterliste den Faktor vorher als „Abschätzung von KAP3" kennzeichnet
  # (Vorgabe P1); Divergenz Bericht ⇄ Code ausgewiesen im Ledger (Befund 151).
  id: pollen.r_s158
  wert: 0.03     # = 0,35 x 0,40 x 0,20 (Dreifaktor-Kette §5.1)
  einheit: "-"
  band: [0.005, 0.10]   # §3.9 ABGESCHAETZT: "Aushang-Fall" ... "aktivierte Warnkette"
  herkunft: herleitung:#s158-wirkung
  quelle: modellannahme   # bewusst KEIN Quellen-Key: keine Interventionsstudie publiziert
  preisstand: null
  bandzuordnung: [u20, 20-64, 65-74, 75-84, 85+]
  endpunkt: morbiditaet
  kennzeichnung: abschaetzung_kap3   # Herleitung 5.1 #s158-wirkung; rolle abschaetzung gibt es nach Aufgabe 4 nicht
  abgeleitet_aus: []
parameter:
  # Anteil gewarnter Zusatztage fuer S158 (T-1239): Tage mit DWD-Pollenflug-
  # Gefahrenindex mindestens "mittel" [70], je Pollengruppe; gleicher Wert fuer
  # Birkengruppe und Graeser. KEIN Parameter der Schadensformel, nur Maßnahmen-Modul.
  # Anteil unter den Symptomtagen (nicht unter allen Tagen); Zeichen t_warn, nicht w_B
  # (w_B ist das Ĝ-Gewicht 0,464, Befund 161).
  id: pollen.t_warn_s158
  wert: 0.75     # Mitte der Anker 0,50 (Saisonanfang) und 1,00 (jeder Symptomtag gewarnt)
  einheit: "-"
  band: [0.50, 1.00]   # §3.9 ABGESCHAETZT; Ersetzungspfad min(1; m/f) aus DWD-Pollenflugstatistik [71]
  herkunft: herleitung:#s158-wirkung
  quelle: modellannahme   # Schwelle nach DWD [70]; der Anteil selbst ist Setzung von KAP3
  preisstand: null
  bandzuordnung: [u20, 20-64, 65-74, 75-84, 85+]
  endpunkt: morbiditaet
  kennzeichnung: abschaetzung_kap3   # Herleitung 5.1 #s158-wirkung
  abgeleitet_aus: []
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
  kennzeichnung: quelle   # Cardell 2016 [65], mit VPI [19] auf 2024
  abgeleitet_aus: []
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
  kennzeichnung: berechnet   # = f x (p_B L_B + p_G L_G) = 0,70 x 61,5
  abgeleitet_aus: [pollen.f_symptomtage, pollen.p_sens_gruppen, pollen.l_saison]
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
  kennzeichnung: berechnet   # = c_jahr_direkt / d_saison = 266,90 / 43,05
  abgeleitet_aus: [pollen.c_jahr_direkt, pollen.d_saison]
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
- **[15]** UBA (Hrsg.), KWRA 2021, Teilbericht 5: Risiken und Anpassung in den Clustern Wirtschaft
  und Gesundheit (Climate Change 24/2021, Dessau-Roßlau, Juni 2021), Kap. 4.2.2 (Aeroallergene;
  GE-KL-07-Projektion ≈ 2 Wochen früher bis 2100, RCP8.5, S. 177–178; Tabelle 55 Klimarisiko ohne
  Anpassung und Gewissheit, S. 179; beschlossene Maßnahmen APA III, S. 180), umweltbundesamt.de
  (lokal: `docs/KWAR/kwra2021_teilbericht_5_cluster_wirtschaft_gesundheit_bf_211027_0.pdf`; Seitenzahlen
  = PDF-Seiten = Druckseiten). Aufbereitet in `docs/KWAR/KWRA-2021_Klimawirkungen.xlsx`, Blatt
  `Klimawirkungen`, Zeile 98.
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
- **[68]** Statistische Ämter des Bundes und der Länder, Regionaldatenbank Deutschland,
  Tab. 12411-09-01-4-B „Bevölkerung nach Geschlecht und Altersgruppen (20) – Stichtag 31.12. –
  regionale Ebenen", Stichtag 31.12.2023, Fortschreibung auf Basis Zensus 2022; Abruf
  22.08.2026 über GENESIS-REST; https://www.regionalstatistik.de/genesis//online?operation=table&code=12411-09-01-4-B;
  Anlage `backend/data/kalibrierung/bevoelkerung_bundesland_altersband.csv` (.md mit
  Verarbeitung), Zeile Berlin: u65 2.961.430 · 65–74 339.490 · 75–84 253.528 · 85+ 107.933.
  Die Tabelle führt 20 Altersgruppen; für u20 zählen unter 5 · 5–10 · 10–15 · 15–20 =
  173.699 · 176.060 · 163.535 · 159.983 = 673.277 (der Auszug im Repo fasst sie in u65 zusammen).
  Lizenz dl-de/by-2-0. Rechenkette Ebene 1 (§3.0), wie #95.
- **[69]** Statistisches Bundesamt (Destatis), Statistischer Bericht „Bevölkerungsfortschreibung
  auf Basis Zensus 2022 — 2023", Tab. 12411-09 „Bevölkerung am 31.12.2023 nach Altersjahren,
  Bundesländern, Nationalität und Geschlecht" (Blatt `csv-12411-09`, Bundesland Berlin,
  Nationalität und Geschlecht insgesamt), XLSX,
  https://www.destatis.de/DE/Themen/Gesellschaft-Umwelt/Bevoelkerung/Bevoelkerungsstand/Publikationen/Downloads-Bevoelkerungsstand/statistischer-bericht-bevoelkerungsfortschreibung-zensus-2022-jaehrlich-5124108237005.xlsx?__blob=publicationFile
  (Abruf 26.09.2026; Permalink https://web.archive.org/web/20260926002751/https://www.destatis.de/DE/Themen/Gesellschaft-Umwelt/Bevoelkerung/Bevoelkerungsstand/Publikationen/Downloads-Bevoelkerungsstand/statistischer-bericht-bevoelkerungsfortschreibung-zensus-2022-jaehrlich-5124108237005.xlsx?__blob=publicationFile).
  Dieselbe Fortschreibung wie [68], nach Altersjahren und ohne Anmeldung
  abrufbar; Kontrolle: Summe 3.662.381, u65 2.961.430 und die drei Seniorenbänder stimmen auf
  die Person mit [68] überein. Lizenz dl-de/by-2-0. Rechenkette Ebene 1 (§3.0).
- **[70]** Deutscher Wetterdienst, „Pollen — Einstufung der Belastungsintensitäten“ (Tabelle der
  Belastungsstufen keine · gering · mittel · hoch je Pollenart, Pollen je m³ Luft im Tagesmittel;
  Hasel/Erle 11–100 mittel, über 100 hoch; Birke 11–50 mittel, über 50 hoch; Gräser 6–30 mittel,
  über 30 hoch), https://www.dwd.de/DE/leistungen/gefahrenindizespollen/erklaerungen.html
  (Abruf 26.09.2026; Permalink https://web.archive.org/web/20260223181518/https://www.dwd.de/DE/leistungen/gefahrenindizespollen/erklaerungen.html).
  Belastungsschwelle der S158-Festlegung (§5.1).
- **[71]** Deutscher Wetterdienst, „Pollenflugstatistik“ (Zehntagesmittel des Anteils der
  Meldungen je Belastungsstufe, je Pollenart und Gebiet, 1997–2026; Daten Stiftung Deutscher
  Polleninformationsdienst), https://www.dwd.de/DE/leistungen/pollen/pollenstatistik.html
  (Abruf 26.09.2026; Permalink https://web.archive.org/web/20260310113821/https://www.dwd.de/DE/leistungen/pollen/pollenstatistik.html).
  Liefert den Anteil \(m_{g,V}\) aller Tage ab „mittel“; Ersetzungspfad für den Anteil gewarnter
  Symptomtage \(t_{\text{warn},g,V} = \min(1;\ m_{g,V}/f)\) je DWD-Gebiet \(V\) (§5.1); im Bericht noch nicht
  ausgewertet.
- **[72]** Deutscher Wetterdienst, Open Data „Pollenflug-Gefahrenindex für Deutschland“ (Datei
  s31fg.json; Gebiete und Teilgebiete mit Kennung: 10 Schleswig-Holstein und Hamburg (11, 12),
  20 Mecklenburg-Vorpommern, 30 Niedersachsen und Bremen (31, 32), 40 Nordrhein-Westfalen (41–43),
  50 Brandenburg und Berlin, 60 Sachsen-Anhalt (61, 62), 70 Thüringen (71, 72), 80 Sachsen (81, 82),
  90 Hessen (91, 92), 100 Rheinland-Pfalz und Saarland (101–103), 110 Baden-Württemberg (111–113),
  120 Bayern (121–124); 12 Gebiete mit 27 Vorhersageflächen, Mecklenburg-Vorpommern sowie
  Brandenburg und Berlin ohne Teilgebiete),
  https://opendata.dwd.de/climate_environment/health/alerts/s31fg.json
  (Abruf 26.09.2026; Permalink https://web.archive.org/web/20260823013619/https://opendata.dwd.de/climate_environment/health/alerts/s31fg.json).
  Gebietszeichen \(V\) und die Bedingung „jedes DWD-Gebiet in genau einer Modellregion“ (§5.1).

## Entscheidungslog

Einträge 1: M0-Entscheidung (rückwirkend dokumentiert). Einträge 2–16: Rev.-1-Entscheidungen
(`/risiko-auto 96`, Gate 1, 30.08.2026); Eintrag 17: Revision nach Review-Runde 1 (Befund 101);
**Einträge 18–19: Rev. 2 (31.08.2026)** — Bezugsebene der P̂-Zentrierung (Nutzer-Entscheid,
Aufgabe §3.2) und die daraus folgende Fixierungs-/Maßnahmenfrage.
**Eintrag 20: Rev. 3 (08.09.2026)** — Wirkungsabschätzung des S158-Hebels nach Vorgabe P2 des
Aufsichtsrats (F-0007 Punkt 1); bewusste Überstimmung von Eintrag 15 (Ledger-Befund 151).
**Einträge 21–22: Fortschreibung 7 (25.09.2026, T-1238)** — Kapitel 9 entfällt (Ledger-Befund
152), Rechenkette §3.0 (Ledger-Befund 153).
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
| 15 | S158 Pollenmonitoring? | **Maßnahmen-Hebel qualitativ** (§3.5); Stadtbaumwahl als mechanischer Hebel über Ĝ quantifiziert — **durch Nr. 20 überstimmt (08.09.2026, Vorgabe P2)**: der Hebel ist jetzt abgeschätzt statt null | keine Interventions-Effektgröße publiziert (Befunde 26/34); ehrlich statt gesetzt | gesetzte Dämpfungsannahme (Rev.-5-„v_monitor" — gestrichen, Befund 32) | Hebelliste ehrlich; Wirkung bis Rev. 2 null |
| 16 | R36 im Basiswert? | **Default 1** (nur Schicht A) | ambulantes Krankheitsbild; keine Evidenz für Distanzeffekt (§3.2) | Sensitivitätsband analog #95-β_d | Basiswert schlanker |
| 17 ⚠ | Ḡ-Gewichtsregel (P̂-Zentrierung)? | **betroffenengewichtetes Mittel über bewohnte Zellen** (Formel §3.3; Bezugsebene in Rev. 2 durch Log 18 auf die Kommune festgelegt) | macht die Bundessumme per Konstruktion invariant gegen λ und Ĝ×pop-Korrelation (Befund 101); c_kal ≡ 1 hat keinen nachgeschalteten Fit, der eine Fehlgewichtung auffangen würde | flächen-/zellgewichtetes Mittel (Bundessumme würde mit Ĝ×pop-Korrelation driften) | Sanity-Rechnung §4 exakt; P̂ verteilt nur um |
| 18 ⚠ | Bezugsebene der P̂-Zentrierung: Bund oder Kommune? | **die eigene Kommune** — Ḡ = betroffenengewichtetes Mittel über die Zellen der betrachteten Kommune, im Lauf gebildet (kein Registry-/Bundeswert); ohne Referenz P̂ ≡ 1 | (a) **Evidenz-Reichweite**: λ stammt aus intra-urbanen Messungen (Werchan Berlin [54,55], Bogawski [56]) — sie tragen Umverteilung INNERHALB einer Stadt, nicht interkommunale Niveauunterschiede; (b) **Aufgabe §3.2 „geschlossene Betrachtungsebene"** (Fortschreibung 31.08.2026, Nutzer-Entscheid): Referenzmittel nie aus Aggregation über eine höhere Ebene; (c) ein Bundesmittel wäre nur mit einem per §3.4 unzulässigen Bundeslauf bestimmbar | Bundesmittel aus Stichprobe (Rev. 1; verworfen: Skalentransfer unbelegt + Ebenenbruch) · amtlicher Vegetations-Referenzwert (existiert nicht) | Kommunensumme jetzt EXAKT invariant gegen λ (statt näherungsweise); Vegetationsstruktur verschiebt nur INNERHALB der Kommune — interkommunal wirkt sie nicht mehr; die Wirkung ist **nullsummig umverteilend** (betroffenengewichtet erwartungstreu), NICHT „konservativ" im Sinne einer Unterschätzung (§3.3(3), Modellgrenze 7) |
| 19 ⚠ | Ḡ-Fixierung (Befund 113) unter der kommunalen Zentrierung? | **kein Pinning** — Ḡ wird in jedem Lauf aus dem aktuellen Vegetationszustand der Kommune gebildet; der flächige Niveaueffekt bleibt bewusst unbuchbar (§5, Modellgrenze 7) | Ein eingefrorener Referenzwert würde einem flächigen Programm einen Niveaueffekt zubuchen, den die λ-Evidenz (intra-urbane Gradienten) nicht trägt — Befund 113 war an das Bundesmittel gebunden und ist mit der kommunalen Zentrierung keine Fixierungs-, sondern eine Evidenzfrage; die Produktmechanik (measure_service skaliert gespeicherte Outcomes) ist KEIN Beleg, sondern begründet die Integrationsauflage: keine pauschal verknüpfte Maßnahme, sonst würde genau der unbelegte Niveaueffekt gebucht (Befund 124/129; Test test_no_flat_measure_on_allergy_days) | Baseline-Pinning je Kommune (verworfen: bucht unbelegten Niveaueffekt) · Emissions-/Ausbreitungsmodell (Ersetzungspfad §6, Datenlage fehlt) | Maßnahme wirkt als Umverteilung (gezielte Hotspot-Entschärfung), nicht als flächiger Niveauhebel |
| 20 ⚠ | S158-Hebel: „qualitativ" (Wirkung null) beibehalten oder abschätzen? | **Abschätzung statt Nullwirkung** — \(r_{\text{S158}}\) = 0,03 (Band 0,005–0,10), Dreifaktor-Kette §5.1, §3.9 ABGESCHÄTZT; Wirkungsort multiplikativ auf ΔTage (Maßnahmen-Modul), Bauform-Grenze als Modellgrenze 8 dokumentiert; Katalogwert `default_reduction` bleibt in diesem Schritt 0,0 (Code-Nachzug L2 nach der P1-Kennzeichnung) | **Vorgabe P2 des Aufsichtsrats (F-0007 Punkt 1)** und Aufgabe §3.5 i. d. F. 06.09.2026: Ein Hebel ohne publizierte Effektgröße läuft nicht mehr als „qualitativ" mit Wirkung null; das Fehlen der Studie ist der Anlass der Abschätzung, nicht ihr Ersatz. Bewusste Überstimmung von Log 15 (Ledger-Befund 151) | Log 15 beibehalten (verworfen: widerspricht P2) · Effektzahl aus fremder Domäne übertragen, z. B. Hitzewarn-Effekt aus #95 (verworfen: Kategorienfehler §3.9 — anderer Endpunkt, andere Handlungskette) | Maßnahmen-Ausweis ≈ 3 % des K1-Werts (bundesweit ≈ 3,3 Mio. €/a; Band 0,55–11,0); Schadenswert selbst unverändert; Befund-124-Sperre (linked_risk_codes leer) bleibt bestehen |
| 21 | Kapitel 9 (Familien-Einordnung und Verworfen-Liste) nach Fortschreibung 7? | **gestrichen**; es bleibt genau eine Methodik (96-A, Familie „K1-Gesundheit bottom-up“ mit Prototyp #95), die verworfenen Ansätze stehen hier | **96-B (Neophyten-Szenario Ambrosia; Lake [23], Born [25], Hamaoui [24])** ersetzt 96-A nicht, weil es nur eine Art abbildet, Birke und Gräser als Hauptlast fehlen und es 2041–2060 statt heute projiziert (Ergänzungsmodul ab M1, Register 96-W024-02, Log 13). **96-C (nationaler Kostenanker, top-down)** ist nach §3.1 ausgeschieden, weil er einen Verteilschlüssel mit Deutschland-Nenner und einen normativ gesetzten Klimaanteil braucht. | Kapitel 9 behalten (verworfen: Fortschreibung 7, eine Methodik je Risiko; Ledger-Befund 152) | keine Zahlenwirkung |
| 22 | Quelle von u20 für die Beispielkommune Berlin in der Rechenkette? | **Direkt aus Tab. 12411-09-01-4-B [68]**: u20 = unter 5 + 5–10 + 10–15 + 15–20 = 673.277, 20–64 = u65 − u20 = 2.288.153; die Zahlen nach Altersjahren stehen gleichlautend in Destatis Tab. 12411-09 [69] | Die Tabelle, aus der Ebene 1 schon u65 und die Seniorenbänder nimmt, führt die vier Gruppen selbst: gleicher Stichtag, gleiche Basis Zensus 2022, und ein Sachbearbeiter, der [68] öffnet, kommt auf dieselbe Zahl. | Anteil u20 aus dem Berliner Landesbericht A I 3 – j / 23 (verworfen: noch auf Basis Zensus 2011, 3.070.537 statt 2.961.430 unter 65-Jährige, Mischung zweier Basen; Runde 0 des Managers) · Bundesanteil 24,07 % (Rückfall des Produkts; für Berlin 1.737 Betroffene oder 0,43 % zu wenig) | u20 673.277 statt 677.877 im ersten Entwurf; Betroffene 402.103, Tage 755.753, bewerteter Schaden 4,69 Mio. € je Jahr (§3.0) |
| 23 ⚠ | S158: an welchen Tagen und ab welcher Belastung wirkt die Warnung, und gilt \(e_{\text{Tag}}\) je gewarntem Tag? | **Nur an gewarnten Tagen:** DWD-Pollenflug-Gefahrenindex mindestens „mittel“ [70], je Pollengruppe; Anteil gewarnter Symptom-Zusatztage \(t_{\text{warn}}\) = 0,75 (0,50–1,00, §3.9 ABGESCHÄTZT; eigenes Zeichen, weil \(w_B\) das Ĝ-Gewicht ist; Ersetzungspfad \(\min(1;\ m_{g,V}/f)\), nie \(m_{g,V}\) direkt); \(r_{\text{S158}}\) = 0,03 gilt je gewarntem Tag, Formel zellscharf im Zelllauf mit Geltungsbereich \(A_{\text{Zelle}}\) (§5.1) | Die Anker von \(e_{\text{Tag}}\) beschreiben die Minderung an einem Tag, an dem gehandelt wird, also an einem gewarnten Tag; Rev. 3 hat sie auf alle Zusatztage gerechnet und damit \(t_{\text{warn}} = 1\) unterstellt. Befund 124 verbietet eine Wirkung auf alle Tage pauschal. Mit der Tagesauswahl wirkt jede Größe genau einmal (Tage, Menschen, Tageswirkung) | \(e_{\text{Tag}}\) als Mittel über alle Zusatztage lesen und \(t_{\text{warn}}\) weglassen (verworfen: widerspricht den eigenen Ankern, Befund 124 bliebe verletzt) · \(e_{\text{Tag}}\) durch \(t_{\text{warn}}\) teilen, damit der wirksame Wert gleich bleibt (verworfen: hebt die Wirkung am gewarnten Tag ohne Beleg an) · Schwelle „hoch“ (verworfen als Basiswert: steckt im unteren Band von \(t_{\text{warn}}\)) · DWD-Anteil aller Tage \(m_{g,V}\) direkt einsetzen (verworfen: wählt die Tage über \(f\) und \(m\) zweimal aus und verdünnt um den Faktor \(f\); Befund 162) | wirksamer Wert über alle Zusatztage 0,03 → 0,03 × 0,75 = 0,0225 (0,028 ist nur das Kettenprodukt vor dem Runden); heute zahlengleich mit einem Faktor 0,0225 auf die Zusatztage im Geltungsbereich, geändert ist der Wert, nicht die Verteilung; Berlin 17.004 statt 22.673 vermiedene Tage, ≈ 105.400 statt ≈ 140.600 € je Jahr; Kapitel 7: `pollen.r_s158` unverändert, `pollen.t_warn_s158` neu; Ledger-Befunde 156, 157, 161, 162, 163, 165, 167 (DWD-Gebiet \(V\) statt \(R\)) |
| 24 | Allergenarme Stadtbaumwahl: Wirkung abschätzen oder verwerfen (P2)? | **Abschätzen, zellscharf über \(\hat G\):** −0,14 auf \(\hat P\) je Senkung von \(\hat G/\bar G\) um 0,2 (Band 0,06–0,20 über λ); Berliner Allee-Zelle mit 100 Betroffenen −26,3 Tage und ≈ 163 € je Jahr (Band −11,3 bis −37,6 Tage); die gleichbleibende Kommunensumme ist Modellgrenze der Abschätzung (Modellgrenze 7) | P2 geht Methodik-Regeln vor; die Wirkung je Zelle ist mechanisch aus \(\hat P\) ableitbar und im Bericht mit Zahl, Band und Sensitivität abgeschätzt; die gleichbleibende Kommunensumme folgt aus der Zentrierung und ist keine gesetzte Null. Im Produkt ist die Wirkung heute nicht sichtbar (Sperre aus Befund 124, keine Katalogmaßnahme); sichtbar wird sie über die Integrationsauflage (Stadtbaumwahl) in §5. Die Kommunensumme ist per Zentrierung invariant (Log 18/19), und ein Niveaueffekt ist unbelegt und durch Befund 124 gesperrt | mit einem Satz verwerfen (verworfen: die Wirkung je Zelle ist ableitbar, eine Verwerfung ließe sie ohne Zahl) · Niveaueffekt für die Kommune schätzen (verworfen: λ-Evidenz intra-urban, Modellgrenze 7, Befund 124) | keine Wirkung auf den Schadenswert; der Satz, die Umverteilung senke den kommunalen Ausweis, ist ersetzt (Ledger-Befund 158); die P2-Begründung stützt sich nicht mehr auf eine Produktanzeige (Ledger-Befund 164) |
| 25 | Kennzeichnung der Parameter-Blöcke (Aufgabe §4): welcher Wert je Block, und wo trägt ein Block ein Feld `rolle`? | **13 von 13 gekennzeichnet:** `quelle` für \(\Delta S\), \(a_{\text{attr}}\), \(p_{\text{AR}}\), \(c_{\text{jahr}}\); `abschaetzung_kap3` für \(p_B/p_G\), \(L\), \(f\), \(\lambda\), \(s_{\text{unbek}}\), \(r_{\text{S158}}\), \(t_{\text{warn}}\) (Herleitung je Block im Kommentar); `berechnet` für \(d_{\text{Saison}}\) (aus f, p_sens, L) und \(c_{\text{Tag}}\) (aus c_jahr, d_Saison); **kein** Feld `rolle` | \(\Delta S\) ist eine amtliche Messreihe, die Anlage [67] nur auswertet; \(p_{\text{AR}}\) folgt je Band einer Quelle, die Extrapolation 80+ ist in §3.2 gekennzeichnet; \(c_{\text{jahr}}\) ist der Quellwert, nur im Preisstand umgerechnet. Von den vier Rollen nach §4 trifft keine zu: \(s_{\text{unbek}}\) geht in jedem Lauf in \(\hat G\) ein und ist damit ein gewöhnlicher Rechenparameter, keine Sensitivitätsgröße; eine Rolle „abschaetzung“ kennt §4 nicht, die Abschätzung trägt \(r_{\text{S158}}\) schon in `kennzeichnung` | \(s_{\text{unbek}}\) mit `rolle: sensitivitaet` (verworfen: sagte, der Wert diene nur der Sensitivität) · \(r_{\text{S158}}\) mit `rolle: abschaetzung` (verworfen: kein zulässiger Wert nach §4) · \(p_{\text{AR}}\) als `abschaetzung_kap3` (verworfen: vier von fünf Bändern tragen einen Quellwert; die Extrapolation ist am Band gekennzeichnet) | keine Wirkung auf Zahlen; kein `wert:` in Kapitel 7 geändert; Ledger-Befund 173 |
