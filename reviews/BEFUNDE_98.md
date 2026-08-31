# Befund-Ledger #98 — UV-bedingte Gesundheitsschädigungen (insbesondere Hautkrebs)

Angelegt 30.08.2026 (Migration M0 Rev. 5 → `docs/methodik/98_uv_schaedigungen.md`);
Statusstand nach der **Rev.-1-Autor-Fassung** (`/risiko-auto 98`, 30.08.2026).
**Startbestand** = alle #98-relevanten Befunde der M0-Gegenprüfung; neue Befunde werden
fortlaufend ab 201 nummeriert (Kollisionfreiheit zur M0-Zählung und zu #96 [101–114]).

**Nummern-Konvention (wie #96, Befund 106):** Zeilen ohne Präfix (15, 16, 37, 41, 43)
tragen die Nummern der `Gegenpruefung_Rev5_Befundliste.md` (Fassung 4.0); Zeilen mit
Präfix **GP-** (GP-9, GP-22, GP-26/34, GP-28, GP-29, GP-30, GP-32) die Nummern der
nummerierten Liste bzw. Lücken-Liste in `docs/METHODIK_M0_GESUNDHEIT_Gegenpruefung_Rev5.md`
(GP-10 ≡ Befundliste 16, hier unter 16 geführt).
Zurückgestellte A-Befunde blockieren die Abnahme.

| Nr | Befund (Stelle · Kurzfassung) | Kat. | Status | Umsetzungsnachweis | Begründung bei Abweichung |
|---|---|---|---|---|---|
| GP-9 | r_out/Außenberufe: kein Knoten der W186-Kette; q_out/q̄_out ohne Wert und Quelle | A | übernommen (Alternative des Vorschlags) | Kap. 1 Knoten-Bilanz (eigene Zeile mit Begründung) + §3.4/Register 98-OUT-01: **Sensitivitätsband, Basiswert-Default 1**; OR primär verifiziert (1,77 [1,37–2,30] [43]); q̄_out = 0,070 vollständig hergeleitet ([572+2.643]/45.909 Tsd., VGR 2023 [70]); Ebene als „neu anzulegen" gekennzeichnet; Log 10 | Basiswert-Aufnahme erforderte Arbeitsmappen-Fortschreibung + AP-Punkt (§1/LF 14) — als dokumentierter Ersetzungsweg benannt, nicht still vollzogen |
| 15 | Attributionsschritt fehlt (#98 bucht 100 % des Dosistrends als klimabedingt; Widerspruch zur #96-Logik) | A | übernommen | §3.2: a_attr,UV = 0,75 (Band 0,5–1,0) als gekennzeichnete Abschätzung mit Begründung (Lorenz-Wolkenbefund vs. Aerosol-Argument — exakt der Befund-Vorschlag); Register 98-E20-03; Log 3; Attributionslogik jetzt konsistent zu #96 | — |
| 16 (≡ GP-10) | k_UV: „11,3 %/Dekade Dortmund" unbelegt; kein Default-Wert | A | **übernommen (abweichend gelöst)** | §3.2 Anker #k-uv: Default 0,84 = verifizierter Dosistrend 4,9 %/Dek. [31] ÷ **eigener** NRW-SSD-Trend 5,81 %/Dek. im selben Fenster 1997–2022 (Skript + CSV [69]) — Raster-konsistente Paarung; Band 0,4–1,0 mit 0,43 (M0-Stations-Paarung) als unterer Stütze; Satelliten-Plausibilisierung; Test `beispiel_98_klimasignal`; Log 2 | Der Befund-Vorschlag „k_UV aus der DWD-Station Dortmund selbst rechnen" ist über das Gebietsmittel (Produktdatenfamilie) gelöst — konsistenter als eine Stations-Paarung, da das Modell k_UV auf Raster-SSD anwendet; Volltext-Fundstelle des Stationstrends bleibt Ersetzungspfad |
| GP-22 (98-Teil) | 98-B-Alternative ohne vollständige Parameter | B | übernommen | Kap. 9: 98-B als dokumentierte Alternative bis zur Quelle (M0 Kap. 4); §3.9-Vollpflicht erst bei Umsetzungsgrundlage | — |
| GP-26/34 (98-Teil) | Maßnahme „UV-Schutz" ohne Effektgröße (NB-Verhältnis ist keine) | B | übernommen | §5: UV-Schutz/Kommunikation ehrlich **qualitativ**; SCS-Förderung mit belegtem Sparpotenzial (−18,8 % [8,4–23,1], DiD [34]), nach Runde-1-Befund 203 ebenfalls qualitativ geführt (Kostenwirkung im Basiswert); Log 12 | Shih/Doran/Collins-Inzidenzreduktionen nicht keyless verifizierbar — statt unverifizierter Übernahme ein anderer, primär verifizierter quantifizierter Hebel |
| GP-28 (98-Teil) | native Ergebnisgröße nicht deklariert | B | übernommen | §3-Kopf: **YLL nativ**; ΔFälle je Entität + € Teil-Ausweise; Raten §6 | — |
| GP-29 (98-Teil) | R36 (und S154/S155) nur benannt, nirgends verrechnet/begründet | A | übernommen | Kap. 1: vollständige Knoten-Bilanz (E20, S154, S155, S158, R35, R36 + Außenberufs-Zeile) mit „rechnet in / Default 1 + Begründung" | — |
| GP-30 (98-Teil) | G6/G8-Spezifikation | B | übernommen | §6: Infokästen (inkl. Latenz-Pflichttext), Raten-Darstellung (YLL je 1.000 EW), Quartier-Aggregat, Versionsstempel; Ebenen §3.6 (SSD neu, u20, Außenberufs-Ebene) | — |
| GP-32 (98-Teil) | v_verhalten/v_verh im Text, in keiner Zeichentabelle | B | übernommen | §3.5-Zeichentabelle: v_verh definiert (Default 1, Band, Register 98-S154-01); keine undefinierten Zeichen | — |
| 37 | SSD_heute/SSD_ref: Mittelungszeiträume nicht definiert | A | übernommen | §3.2: Klimanormalperioden je Zelle festgelegt (exakt der Vorschlag); Referenzwerte je Region gemessen (CSV [69]); Rasterverfügbarkeit ab 1961 als Integrationscheck + Gebietsmittel-Fallback dokumentiert (§3.6) | — |
| 41 | Entitäten-Split 2015 altersinvariant auf 2023er-Raten | B | übernommen | §3.1: als dokumentierte Annahme mit Richtungsabschätzung (SCC-Anteil bei Alten unterschätzt → ΔFälle-Unterschätzung in alten Kommunen — exakt der Vorschlag); Band 0,30–0,50 ⇒ BAF_C44 1,73–1,95; Sekundärangaben-Kennzeichnung + Ersetzungspfad | altersabhängige Splits in [27] nicht keyless verifizierbar |
| 43 | λ_e (Periodenquotient) und L̄_e (Median-Approximation) unmarkiert | B | übernommen | §3.4: beide Approximationen gekennzeichnet mit Richtung (λ: Überschätzung bei steigender Inzidenz; L̄: leichte Überschätzung bei Rechtsschiefe) — einheitlich zur #95-Befund-22-Lösung | — |

## Review-Runde 1 (unabhängige Gegenprüfung, 30.08.2026) — neue Befunde 201–210

Lints: Beispiel-Blöcke 5/5 grün; Knoten-/Kanten-Abgleich gegen beide xlsx bestanden
(W186: E20/S154/S155/S158/R35/R36; Netzwerkliste Z99 ohne Kanten; K1/R9/P52 wie zitiert);
Anlage [69] reproduziert (Skript-Lauf 30.08.2026, CSV identisch); Preisstand einheitlich
€2024. Primärquellen stichprobenverifiziert: Lorenz 2024 (4,9/3,2 %/Dek. Dortmund,
7,5/5,8 Uccle ✓), Schmitt 2011 (1,77 [1,37–2,30]; Kohorten 1,68 [1,08–2,63] ✓),
Speckemeier 2022 (5.326/9.038; 4.660/5.890; DiD −18,8 % [−23,1; −8,4] ✓), KID 2025
Tab. 3.13.1/3.14.1 (27.430/3.169, roh 32,9; 242.820/1.332, roh 276,0/307,5;
Sterbealter 78/76 bzw. 88/85 ✓ — Fußnote: Median ✓).

| Nr | Befund (Stelle · Art · Kurzfassung · Vorschlag) | Kat. | Status | Umsetzungsnachweis | Begründung bei Abweichung |
|---|---|---|---|---|---|
| 201 | §3.3/§3.5/§7 · Widerspruch: Formel \(F = c_{\text{kal},e}\cdot\sum_a \text{pop}_a I_{e,a}/10^5\) **und** normierte Tabellenwerte. Nachrechnung: Tabellen-\(I_{e,a}\) sind bereits normiert (C44 gewichtete Rate 291,0 ≈ amtlich 290,96; MM 32,9); wörtliche Umsetzung von Formel + Registry (uv.i_raten **und** uv.c_kal) normiert doppelt → C44-Baseline −6,9 % (226.112 statt 242.820). Golden-Test `beispiel_98_baseline_normierung` rechnet ohne c_kal — Formel, Text („bereits in den Tabellenwerten enthalten") und Registry widersprechen sich. Vorschlag: entweder Rohablesewerte in Tabelle/Registry + c_kal in der Formel, oder c_kal aus Formel/Registry streichen (nur als Herleitungs-Protokoll führen). | B | **übernommen** | §3.3: Tabellen/Registry auf ROH-Ablesewerte umgestellt (uv.i_raten_roh), c_kal wirkt in der Formel (MM 1,022 / C44 0,945); Test `beispiel_98_baseline_normierung` prüft Roh × c_kal = amtliche Fallzahlen; Zeichentabelle präzisiert — Variante 1 des Vorschlags | — |
| 202 | §3.1/[27] · Widerspruch (Quellen, §3.8 „Widersprüche benennen"): Das wertetragend zitierte KID-2025-C44-Kapitel selbst gibt „knapp drei Viertel Basaliome … etwa ein Viertel Plattenepithelkarzinome" (2021–2023) an ⇒ \(w_{\text{SCC}}\) ≈ 0,25 — **unterhalb** der Bandunterkante 0,30; bei 0,25 wäre BAF_C44 = 1,675 < 1,73 (Band verletzt, C44-Zusatz −8 %). Der Bericht stützt 0,384 allein auf die 2015er-BfS-Sekundärangabe und benennt den Widerspruch in der eigenen Primärquelle nicht. Vorschlag: Widerspruch ausweisen, Band auf ≈ 0,25–0,50 weiten, Basiswert-Wahl begründen (oder auf KID-2025-Split wechseln). | B | **übernommen** | §3.1: Widerspruch benannt (KID-2025 „¼ PEK" vs. BfS-2015 0,384); Basiswert auf w_SCC = 0,25 (Primärquelle) gewechselt, Band 0,25–0,50; BAF_C44 = 1,675; alle Folgewerte neu (ΔFälle C44 20.118, € 378 Mio); Log 9 aktualisiert | — |
| 203 | §5/Log 7+12 · Fehler (LF-4-Klasse „Maßnahmeneffekt schon im Basiswert"): Basis-\(c_{\text{MM}}\) = SCS-detektierte Kosten für **100 %** der Fälle (6.724 €); der quantifizierte Hebel wendet zusätzlich −18,8 % „multiplikativ auf \(c_{\text{MM}}\) des zusätzlich gescreenten Fall-Anteils" an → zusätzlich gescreente Fälle würden mit 5.460 € unter dem empirischen SCS-Wert bepreist; der SCS-Nutzen steckt für alle Fälle bereits im Basiswert, der Hebel hat modellintern kein Headroom. Der „Doppelzählungs-Wächter"-Text behauptet das Gegenteil. Vorschlag: Basiswert als detektionsmix-gewichteten Satz (Mix-Anteil = Parameter) und Hebel = Mix-Verschiebung × (nicht-SCS − SCS)-Differenz bzw. DiD-Effekt auf den nicht-SCS-Anteil; oder Hebel ehrlich als „im Basiswert bereits eingerechnet / qualitativ" führen. | B | **übernommen** | §5/Kap. 1/Register/Log 12: SCS-Hebel auf **qualitativ** zurückgestuft (Kostenwirkung bereits im Basiswert — LF-4-Wächter greift jetzt korrekt); Detektionsmix-Parameter als quantifizierender Ersetzungspfad definiert (Hebel = Mix-Verschiebung × Kostendifferenz) | — |
| 204 | §3.3 · Lücke (§3.9 „komplette Rechenkette mit allen Zwischenwerten"): Die Roh-Ablesewerte je 5-Jahres-Gruppe (F/M) aus Abb. 3.13.2/3.14.3 stehen nirgends (kein Anlagen-CSV, keine Tabelle) — die behauptete Validierung „32,6 / 312,4 vor Normierung" ist aus dem Bericht nicht reproduzierbar; die 50/50-Geschlechtsgewichtung für 20–64/65–74/75–84 ist unbegründet (reale Männeranteile ≈ 0,47/0,44), nur 85+ ist belegt (0,348). #95-Präzedenz (Winklmayr-Ablesung) dokumentierte die Ablesewerte. Vorschlag: Ablese-CSV als Anlage (Gruppe × Geschlecht × Wert) + Gewichtungsrechnung; 50/50 durch belegte Männeranteile je Band ersetzen oder als Annahme mit Richtung kennzeichnen. | B | **übernommen** | Anlage `kid2025_ablesewerte.csv` (alle 5-Jahres-Ablesewerte F/M) + §3.3-Auszug; 50/50 ersetzt durch geschlechtsspezifische Bevölkerungsgewichte je Altersjahr (Tab. 12411-06 [48]); Validierung reproduzierbar (−2,2 %/+5,9 %) | — |
| 205 | §3.5-Zeichentabelle/§7 uv.v_verh · Lücke (§3.9 gilt auch für Bandgrenzen): \(v_{\text{verh}}\)-Band „+0,25…+0,60 **je Komforttag**" vs. Parameter-Band **[1,0, 1,6]** — die Übersetzung (s je Komforttag → Multiplikator auf was? über wie viele Komforttage?) ist nirgends definiert; die M0-Herleitungskette von s ≈ +0,45 (1,2 min/°C, 44 min Mittel, ΔT ≈ 10 °C ⇒ +27 %, Kleidung +15 %) wurde nicht in den Bericht migriert, obwohl die Markdown-Datei jetzt die Quelle ist. Vorschlag: Herleitung + Wirkungsort-Formel (analog r_out) in §3.4/§3.5 aufnehmen, Bandgrenze 1,6 herleiten oder korrigieren. | B | **übernommen** | §3.4: v_verh-Kette vollständig migriert (1,2 min/°C × ΔT 10 °C ⇒ +27 % Außenzeit; Dosis-Zeit-Kopplung R² 0,75–0,79; Kleidung +15 % ⇒ Tageswert +45 %, Kern +25–60 %); Definition als Tages-Multiplikator an Komforttagen, Jahreswirkung = Szenario; YAML-Kommentar angepasst | — |
| 206 | §3.4 r_out · Fehler (klein): Text sagt „wirkt nur auf den **SCC-Anteil des C44-Zusatzes**", die Formel gewichtet aber mit dem Fall-Anteil \(w_{\text{SCC}}\) = 0,384 statt mit dem BAF-gewichteten Zusatz-Anteil 0,384·2,5/1,822 = 0,527 → Beispielkommune +2,0 % statt korrekt +2,7 %. Vorschlag: \((1-w^{Z}) + w^{Z}\cdot\frac{1+q(\text{OR}-1)}{1+\bar q(\text{OR}-1)}\) mit \(w^{Z}\) = SCC-Anteil am Zusatz, oder Textbeschreibung anpassen. | C | **übernommen** | §3.4: Formel auf w_Z = w_SCC·2,5/BAF_C44 = 0,373 umgestellt; Beispiel +1,9 %; Test angepasst — exakt der Vorschlag | — |
| 207 | §4 Sanity-Band · Fehler (klein): Obergrenze „≈ 630 Mio € (k_UV 1,0 × a_attr 1,0 × **obere c_e**)" — nachgerechnet ergibt die genannte Kombination 687 Mio €; 630 Mio entsteht nur, wenn allein c_MM (nicht c_C44) auf die Obergrenze gesetzt wird. Zahl oder Klammerdefinition korrigieren. | C | **übernommen** | §4: Obergrenze neu gerechnet (653 Mio mit beiden oberen c_e) und Kombination explizit definiert; Nicht-Kumulation der übrigen Bänder benannt | — |
| 208 | §3.2/§3.5/§4 · Rundungsfehler: „ΔDosis DE 4,94 %" (3×) — exakt 7,82 % × (4,9/5,81) × 0,75 = 4,946 % ⇒ 4,95 %; der eigene Golden-Test setzt 4,95. Vereinheitlichen. | C | **übernommen** | einheitlich 4,95 % (Text §3.2/§3.5, Testkommentar) | — |
| 209 | §3.6/[69] · Lücke (klein): Der dokumentierte Zell-Fallback „Bundesland-Gebietsmittel [69] je Zelle" ist durch die Anlage nicht gedeckt — `ssd_trend_region.csv` enthält nur deutschland/nrw/nord/mitte/sued, keine Bundesland-Zeilen (Skript-Docstring nennt „…/Bundesland" als Ausgabe). CSV um Bundesländer ergänzen oder Fallback-Text auf Regionsmittel ändern. | C | **übernommen** | Skript um Bundesland-Zeilen erweitert (land:*), CSV neu erzeugt — Fallback jetzt durch die Anlage gedeckt; [69] aktualisiert | — |
| 210 | §3.4/§4 · Approximation nicht gekennzeichnet (§3.9): \(\Delta F = F_{2023}\cdot\text{BAF}\cdot\Delta\text{Dosis}\) wendet den relativen Exzess auf die bereits dosiserhöhte 2023er-Baseline an; der attributable Anteil wäre BAF·ΔD/(1+BAF·ΔD) → systematische Überzeichnung ≈ +9 % (C44) / +3 % (MM). Innerhalb der Bänder unerheblich, aber als gekennzeichnete Approximation (Richtung: Überschätzung) ausweisen — analog GP-Befund 43. | C | **übernommen** | §3.4: PAF-Approximation gekennzeichnet (exakte Form BAF·ΔD/(1+BAF·ΔD); Richtung Überschätzung +3 %/+8 %, innerhalb der Bänder) | — |

## Review-Runde 2 (unabhängige Gegenprüfung / Re-Review, 30.08.2026) — neue Befunde 211–212

Re-Review-Ergebnis: Lints grün (5/5 Beispiel-Blöcke ausgeführt und bestanden; Anlage [69]
per Skript-Lauf reproduziert, CSV byte-identisch inkl. land:*-Zeilen; Preisstand einheitlich
€2024; W186-Knotenzeile erneut gegen die Arbeitsmappe geprüft ✓). Umsetzungen 201–203 und
205–210 verifiziert (u. a. 202-Folgewerte nachgerechnet: BAF_C44 1,675, ΔF C44 20.118,
€ 378 Mio, Band 119/653 Mio ✓; 206: w_Z 0,373, +1,9 % ✓; 207: 653 Mio ✓). Umsetzung 204
nur teilweise: Ablese-CSV vorhanden und Geschlechtsgewichte belegbar (Bandsummen exakt
gegen Destatis/Eurostat 31.12.2023 reproduziert; MM alle Bänder sowie C44 65–74/75–84/85+
auf ±0,2 % exakt reproduziert), aber die C44-Bandrate 20–64 ist fehlerhaft aggregiert
(→ 212). Regression Startbestand (Stichprobe 15, 16, 37, 41, 43, GP-28, GP-29, GP-32):
keine Rückfälle.

| Nr | Befund (Stelle · Art · Kurzfassung · Vorschlag) | Kat. | Status | Umsetzungsnachweis | Begründung bei Abweichung |
|---|---|---|---|---|---|
| 211 | §4 (Kalibrier-Bullet + Verteilungsprüfungs-Bullet), Register 98-R35-01, Log 15 · Widerspruch (Revisionsrückstand aus 201/204): §4 nennt die Kalibrier-Skalare weiterhin „c_kal,MM = 1,008; c_kal,C44 = 0,931" und Log 15 „(1,008/0,931)" — §3.3, Zeichentabelle und Registry (uv.c_kal) sagen **1,022/0,945**; außerdem stehen in §4 und Register 98-R35-01 noch die Alt-Validierungswerte „MM −0,8 %/C44 +7,4 %" (Stand 50/50-Gewichtung, alte normierte Tabelle) neben den neuen „−2,2 %/+5,9 %" — zwei widersprüchliche Ergebnisse für dieselbe Prüfung im selben Abschnitt. Vorschlag: alle vier Stellen auf die Rev.-Werte ziehen (bzw. nach 212 neu rechnen), Alt-Werte streichen. | C | **übernommen** | §4 (beide Stellen), Log 15, Log 5 und Register 98-R35-01 auf die aktuellen Werte gezogen (1,022/0,999; Validierung −2,2 %/+0,1 %) — keine Alt-Skalare mehr im Bericht | — |
| 212 | §3.3 (I_C44,20–64 = 154,2), Anlage `kid2025_ablesewerte.csv`, §7 uv.i_raten_roh/uv.c_kal, §4 Validierung · Fehler (Ableitung, §3.9/LF 6): Die C44-Bandrate 20–64 wurde nur über die Bevölkerung **30–64** gemittelt — die 9,30 Mio 20–29-Jährigen fehlen im Nenner (die Anlage hat für C44 keine Ablesewerte unter 30–34). Exakte Reproduktion mit den geschlechtsspezifischen Altersjahres-Gewichten (Destatis 31.12.2023 = Eurostat demo_pjan 2024; Bandsummen identisch zum Bericht): Nenner 30–64 ⇒ 154,17 ≈ Berichtswert 154,2; korrekt (20–29 mit Rate ≈ 0) ⇒ **125,0**. Folgen: (a) c44_roh = 242.716 statt 257.072 ⇒ c_kal,C44 ≈ **1,000** statt 0,945 — die ausgewiesene Ablese-Abweichung „+5,9 %" ist ein Artefakt dieses Fehlers (korrigiert ≈ −0,0 %); (b) Bundessumme unverändert (Normierung), aber die **Altersverteilung** der C44-Baseline ist verzerrt: Band 20–64 trägt relativ **+16,5 %** zu viel, die Bänder 65+/u20 je **−5,6 %** zu wenig — junge Kommunen erhalten zu viel, alte zu wenig C44-Zusatz (C44 ≈ 56 % der €-Summe); (c) MM ist korrekt gerechnet (voller Nenner) — Regel uneinheitlich und nirgends dokumentiert; die u20-Werte (MM 0,5 / C44 2,0) stehen ohne Ablesewert in der Anlage und ohne Herleitungsweg im Bericht (§3.9). Vorschlag: I_C44,20–64 auf 125,0 korrigieren (bzw. 20–24/25–29 aus Abb. 3.14.3 ablesen und CSV ergänzen), c_kal,C44/Validierung/YAML/Golden-Test `beispiel_98_baseline_normierung` neu rechnen; Aggregationsregel (Gruppen ohne Ablesewert = Rate 0 im vollen Band-Nenner) und u20-Herkunft in §3.3 dokumentieren. | B | **übernommen** | §3.3: Bandmittelung über die volle 20–64-Bevölkerung; C44 20–24/25–29 als gekennzeichnete Ansätze (5, Band 0–15) in Tabelle + Anlage-CSV; u20-Ansätze (0,5/2,0, Band 0–5) ebenfalls in der CSV mit Herleitungsvermerk; korrigierte Bandrate 125,9, c_kal,C44 = 0,999, Validierung +0,1 % (Artefakt beseitigt); Test/YAML/Zeichentabelle konsistent | — |

## Review-Runde 3 (unabhängige Gegenprüfung / Re-Review, 30.08.2026) — keine neuen Befunde

Prüfumfang gemäß §6 (Re-Review): Umsetzungen 211/212, Regression 201–210 + Startbestand
(Stichprobe), Lints vollständig. Ergebnis: **Null-Runde.**

- **212 verifiziert:** Bandsummen und Männeranteil 85+ exakt gegen Eurostat demo_pjan 2024
  (= Destatis 31.12.2023) reproduziert (u20 15.583.456 · 20–64 49.163.992 · 65–74 9.569.640
  · 75–84 6.294.744 · 85+ 2.844.213; M 85+ 990.292). Bandraten aus der Anlage-CSV mit
  geschlechtsspezifischen Altersjahres-Gewichten unabhängig nachgerechnet: C44 20–64 =
  125,95 ≈ 125,9 (voller Band-Nenner inkl. 20–29) ✓; alle übrigen Bänder identisch (MM
  24,7/64,0/94,9/88,5; C44 617,6/1.267,2/1.479,5) ✓. Folgewerte: c44_roh 243.158,
  c_kal,C44 = 0,9986 ≈ 0,999 ✓; mm_roh 26.837, c_kal,MM 1,022 ✓; Validierung −2,2 %/+0,1 %
  ✓ (Artefakt +5,9 % beseitigt). Anlage-CSV enthält C44 20–24/25–29 = 5 und u20-Ansätze
  0,5/2,0 jeweils mit Vermerk „angesetzt (unter Ablesegrenze)" + Kopfkommentar (Befund 212);
  §3.3-Kennzeichnung (Bänder 0–15 bzw. 0–5, Aggregationsregel voller Nenner), Zeichentabelle,
  YAML `uv.i_raten_roh`/`uv.c_kal` und Log 5/15 konsistent.
- **211 verifiziert:** keine Alt-Skalare (1,008/0,931/0,945) und keine Alt-Validierungswerte
  (−0,8 %/+7,4 %, 32,6/312,4, 154,2) mehr im Bericht (Volltext-Grep leer).
- **Lints:** 5/5 Beispiel-Blöcke ausgeführt und grün (`beispiel_98_klimasignal`,
  `_baseline_normierung`, `_lambda_l_kosten`, `_bundessumme`, `_beispielzelle`);
  Knoten-/Kanten-Abgleich erneut direkt gegen beide xlsx (W186 Z409: E20/S154/S155/S158/
  R35/R36 ✓; Netzwerkliste Z99: Buchungsobjekt Ebene B, K1, keine Kanten ✓; Monetarisierung
  Z103: R9, YLL×VOLY/P52 ✓; Abgleich-Protokoll: nur P52, kein #98-Punkt ✓); Zeichentabelle
  und 13 Parameter-Blöcke vollständig; Preisstand einheitlich €2024; [69]-CSV deckt den
  Bundesland-Fallback (land:*-Zeilen) ✓.
- **Regression 201–210 + Startbestand:** Stichproben nachgerechnet — 207-Band 119/653 Mio €
  exakt reproduziert (obere Kombination 652,8 Mio); 210-Richtungswerte +3 %/+8,3 % ✓;
  206 w_Z = 0,373, Beispiel +1,9 % ✓; 202 BAF_C44 1,675, ΔF C44 20.118, € 378 Mio
  (Behandlung 124 + Mortalität 254) ✓; §4-Sanity (6,8 % KKR; YLL-Anteil ≈ 4 % von ≈ 40.600)
  ✓; 203/205/208/209 textlich verifiziert; keine Rückfälle im Startbestand (Stichprobe
  GP-9, 15, 16, 37, 41, 43).

Damit sind alle Befunde 201–212 geschlossen und verifiziert; keine offenen A-/B-Befunde.

## Fortschreibungs-Konformität (30.08.2026)

Prüfung gegen die Aufgaben-Fortschreibung vom 30.08.2026 (§3.4-Ressourcen-Regel:
kein nationaler Vollraster-Lauf; §3.1-Datenebenen-Anlagepflicht): Bericht #98
**konform** — Konformitätsvermerk im Berichtskopf ergänzt (redaktionell, keine
Modellwert-Änderung; kein Review-Loop erforderlich). Kern: die SSD-Ebene (DWD sunshine_duration 1 km, Register 98-E20-01) und die Branchenanteils-Ebene (98-OUT-01, Proxy) sind als „neu anzulegen“ spezifiziert und werden von /integriere-risiko verpflichtend angelegt (§3.1-Anlagepflicht); alle übrigen Zellgrößen sind vorhanden oder regional/national.

## Integration (`/integriere-risiko 98`, 31.08.2026) — neuer Befund 213

| Nr | Befund (Stelle · Art · Kurzfassung) | Kat. | Status | Umsetzungsnachweis | Begründung bei Abweichung |
|---|---|---|---|---|---|
| 213 | §3.2 vs. §7 `uv.k_uv` · Rundungsdivergenz **innerhalb des Berichts**: Der maschinenlesbare Parameter-Block gibt `wert: 0.84`, die §3.2-Prosa und die Beispiel-Blöcke rechnen mit der ungerundeten Kette 4,9/5,81 = **0,8434**. Daraus folgt ΔDosis DE = 4,927 % (Kap. 7) statt der im Text genannten 4,95 % — alle Ergebniswerte des Berichts (ΔF, YLL, €) liegen um **0,5 % relativ** über dem, was die Registry-Werte produzieren. | B | **offen (Bericht)** — Integration NICHT blockiert | Die Registry führt `k_uv = 0,84` **exakt wie Kap. 7**; kein stiller Code-Fix (Eiserne Regel 5). Golden-Test `test_delta_dosis_uses_change_not_level` nagelt beide Stände fest (Produktion 4,9266 %, Bericht-Prosa 4,95 %, Abstand < 0,5 %) — die Divergenz kann nicht unbemerkt wachsen. Die Sanity-Anker der Kap.-4-Bänder bleiben mit den Produktionswerten eingehalten (ΔF 810,7 MM / 20.045,5 C44, YLL 1.574,0, € 376,5 Mio ∈ [119, 653] Mio). | Auflösung gehört in den Bericht, nicht in den Code: entweder `uv.k_uv: 0.8434` (Herleitungswert, §3.9-konform) oder die §3.2-Ergebniswerte auf die gerundete Kette umstellen. Ein Review muss das entscheiden. |

**Integrationsergebnis §3.1/§3.2/§3.4 (Verifikation, ein Satz je Punkt):**

- **§3.1-Anlagepflicht — Ebene SSD/UV_RADIATION (98-E20-01) angelegt:** Das
  DWD-CDC-Jahresraster `sunshine_duration` ist **ab 1961 verfügbar** (verifiziert
  31.08.2026); die 60 Jahresraster wurden **einmalig** zu zwei Normalperioden-Mitteln
  vorgemittelt (`scripts/kalibrierung/dwd_ssd_normalperioden.py` →
  `data/kalibrierung/ssd_normalperioden.npz`; Flächenmittel 1.544,0 → 1.664,7 h,
  **+7,90 %** — unabhängige Bestätigung der Gebietsmittel-Anlage 1.544,0/1.664,8/+7,82 %),
  das Produkt liest nur diese Anlage (`climate/ssd_normalperioden.py`,
  `inputs.apply_ssd_normalperioden` → Zellgrößen `ssd_ref`/`ssd_neu`), und der im
  Bericht §3.6 dokumentierte Bundesland-Fallback greift nur noch für Zellen außerhalb
  des Rasters. Der Fallback ist damit **nicht** mehr der Regelfall.
- **§3.1 — Ebene Außenbeschäftigten-Anteil (98-OUT-01) bleibt geparkt:** Der Bericht
  führt sie ausdrücklich als Sensitivitätsband ohne keyless Zellquelle (INKAR/SVB);
  entsprechend ist `r_out_enabled = 0` und der Modifikator **exakt** neutral
  (Golden-Test `test_r_out_modifier_is_parked_and_neutral` prüft Neutralität, die
  +1,9-%-Bericht-Rechnung bei eingeschaltetem Schalter und die Zentrierung q = q̄ ⇒ 1).
- **§3.4-Ressourcen-Regel eingehalten:** Kein Integrationsschritt erforderte einen
  nationalen 100-m-Vollraster-Lauf; die Vormittelung lief einmalig auf dem
  1-km-DWD-Raster, die Verifikation auf Gemeindepunkten (Freiburg 1.740 → 1.825 h,
  Hamburg 1.490 → 1.620 h, Leipzig 1.503 → 1.723 h) und die Sanity-Prüfung analytisch
  auf der Bundes-Altersstruktur.
- **§3.2-Geschlossene Betrachtungsebene eingehalten:** #98 bildet **kein**
  Zentrierungs-/Referenzmittel über eine höhere Ebene. ΔDosis ist je Zelle gemessen
  (Rasterablesung), die Baseline ist bevölkerungs-/altersproportional, und die einzige
  Zentrierung (q̄_out des geparkten r_out) stammt aus **amtlicher Statistik**
  (VGR-Erwerbstätige 2023) — nach §3.2 Buchstabe (a) zulässig.
