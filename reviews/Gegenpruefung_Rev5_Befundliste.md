# Gegenprüfung: Methodik-Bericht M0 Rev. 5 gegen AUFGABE_METHODIK_SCHADENSRECHNUNG.md

**Fassung 4.0 — Übergabefassung an das Methodik-Team, Prüfgrundlage vollständig** · Prüfdatum: 22.08.2026 · Prüfgrundlage: Aufgabenbeschreibung §2–§4 (Leitfragen 1–13), die Quell-Arbeitsmappen KWRA-Schadensbaum_X_UBA-klimawirkungsketten.xlsx und KWRA-Monetarisierung.xlsx **sowie docs/METHODIK_GRUNDSAETZE.md (G1–G14, nachgereicht — Befund 31 damit geschlossen)** · Geprüftes Dokument: METHODIK_M0_GESUNDHEIT.pdf, Rev. 5 vom 22.08.2026 · Alle Nachrechnungen reproduzierbar (Rechenwege in den Befunden angegeben).

**Aufbau:** **Teil 1** = Befundliste (Befunde 1–56; Durchgang 1: 1–31 · Durchgang 2: 32–49 · Durchgang 3 / Arbeitsmappen: 50–54 · Durchgang 4 / Grundsätze-Dokument: 55–56 + Statusupdates). Offen sind 54 Befunde (46 ersetzt durch 51, 31 geschlossen). **Teil 2** = Übergabepaket: Arbeitspakete, Abnahmekriterien, Abdeckungsmatrix, übernahmefertige Bausteine inkl. Fortschreibungstexten für die Grundsatz-Dokumente, Infokasten-Entwürfe, verbleibende Grenzen, Rückmeldeformat. Ziel-Revision: **Rev. 6** bis 28.08.2026.

**Gesamturteil:** Rev. 5 erfüllt die Anforderungen in weiten Teilen und hat die zentralen Grundsatzprüfungen bestanden (siehe Abschnitt „Bestanden"). Nach **vier Prüfdurchgängen** sind **56 Befunde** erfasst, davon **54 offen** (23 A / 19 B / 14 C erfasst; Befund 46 ersetzt durch 51, Befund 31 geschlossen). Wichtig zur Prüfhistorie: In den Durchgängen 1–2 lagen weder die Quell-Arbeitsmappen noch das Grundsatz-Dokument vor — beide wurden in den Durchgängen 3–4 nachgereicht und abgeglichen. Der Abgleich **bestätigt** die Knoten-Treue der drei Wirkungsketten, die Konten-Einbettung und die G-Nummerierung, **löst** die Befunde 26, 31 und 46 auf bzw. präzisiert sie, und ergibt sieben neue Befunde. Die gewichtigsten darunter: Die verbindliche Monetarisierungs-Arbeitsmappe schreibt weiterhin VSL 3,5 Mio. € vor, während der Bericht YLL × VOLY rechnet (Befund 50); die §1.2-Weitergaben-Tabelle für #95 widerspricht den echten Kanten der Netzwerkliste, insbesondere fehlt die #95→#101-Partitionsregel für K1 (Befund 51); und das Grundsatz-Dokument selbst trägt mit der G1↔G5-Spannung die Wurzel der regionalen Kalibrierfaktoren in sich (Befund 55). Die gravierendsten Befunde insgesamt: 1, 2, 11, 32, 35, 50, 51.

---

## Bestanden (zur Entlastung des Berichts, Leitfragen in Klammern)

- **Verteilschlüssel-Test (LF 2):** Alle drei A-Ansätze strikt bottom-up; Kommune ohne Treiber → ~0. Verteilschlüssel-Ansätze korrekt als Negativ-Beispiele geführt. ✓
- **OR-Übersetzungen (LF 5):** β_iso = 2,3−1 geteilt durch [1 + 0,40·1,3] = 0,86 ✓ (nachgerechnet); r_out,e in #98 korrekt zentriert ✓; β_pfl-Formel arithmetisch konsistent (1,821; Zellwerte 0,73/1,27 reproduziert) ✓.
- **Tails (LF 7):** Empirische intra-saisonale Wochenquantile aus 21 Stationen × 30 Sommern, inkl. des ehrlichen Befunds, dass die vermutete Rechtsschiefe nicht auftritt und stattdessen σ zu klein gesetzt war — genau die geforderte Arbeitsweise. ✓
- **VSL/VOLY-Konsistenz (LF 9):** 6,19 Mio. ÷ 160,8 T€ = 38,5 Jahre; beide VSL-Stützpunkte geführt. ✓ (aber Befund 10 zum Band.)
- **Ländliche Anker (LF 8):** MV 1,22 / Thüringen 1,04 gegen Berlin 1,05 — der in Review 3 geforderte Stadt-Land-Check ist da. ✓ (aber Befund 19 zur Unabhängigkeit.)
- **Maßnahmen (LF 5):** Umstellung von Fall-Kontroll-ORs auf Interventionsevidenz, Doppelzählungs-Wächter gegen die Kalibrierjahre explizit. ✓ (aber Befund 18 zur Quellenverifikation.)
- **Kein-Doppelkanal (LF 4):** Grün-/Baumkronenanteil ausdrücklich nicht als zweite Vulnerabilität; UHI-Mittelwerttreue sauber erklärt. ✓
- **R9/Konten (LF 4):** K1-Partition, Abgrenzungen mit Zielrisiko/Konto/Stufe benannt; #96 ohne Mortalität. ✓

---

## Kategorie A — materielle Befunde (vor 28.08. beheben oder entscheiden)

### Befund 1 — Kalibriermodell ≠ Produktionsmodell; „Näherung konservativ" hat die falsche Richtung
- **Stelle:** Kap. 2, 95-A(c), „Kalibrierlauf (Rev. 5)".
- **Art:** Fehler.
- **Begründung:** Die Faktoren c_kal wurden aus einem Näherungsmodell auf Bundesland-Ebene gefittet (DWD-Flächenmittel je Land, ohne UHI). Das Produktionsmodell rechnet mit bevölkerungslokalen 100-m-Zelltemperaturen inkl. UHI-Feinstruktur. Beide Näherungsfehler wirken in **dieselbe** Richtung: (a) Die ERF ist konvex (Exponential mit Schwellen-Knick) — eine mittelwerttreue UHI-Umverteilung *erhöht* die Modellsumme, die die Näherung nicht sieht; (b) Bevölkerung konzentriert sich in wärmeren Lagen (Städte, Tallagen), das Flächenmittel je Land unterschätzt also die Bevölkerungs-Exposition. Beides macht die Näherungs-Modellsumme zu klein → c_kal zu groß → das kalibrierte **Produktionsmodell überschätzt**. Die Kennzeichnung „Näherung konservativ" ist damit falschherum (im Sprachgebrauch des Berichts heißt konservativ „Untergrenze", §1.2).
- **Vorschlag:** Kalibrierlauf mit dem Zellmodell wiederholen — die dafür nötige Bundeslauf-Infrastruktur ist laut 95-B(b) („vorhandene Lite-Infrastruktur") verfügbar. Falls das bis 28.08. nicht geht: Differenz Näherung ↔ Zellmodell für 2–3 Beispieljahre quantifizieren und als Korrektur-/Unsicherheitsband auf c_kal ausweisen; die Richtungsangabe im Text korrigieren.

### Befund 2 — Vier regionale c_kal (0,618–1,737) verstoßen gegen Anforderung 3.4 („EIN Skalar") und patchen einen Strukturfehler statt ihn zu beheben
- **Stelle:** Kap. 2, 95-A(c) G12-Verteilungsprüfung + Zeichentabelle (c_kal).
- **Art:** Widerspruch (zur Aufgabe 3.4) + methodischer Fehler.
- **Begründung:** Aufgabe 3.4 verlangt den nationalen Anker als **einen** Skalar. Der Bericht führt vier Regionalfaktoren ein, weil die Verteilung mit einem Skalar nicht passt (Norden ×1,6–3,6 über, BW ×0,56 unter). Ein Süd-Faktor von 1,737 bedeutet: Das Modell unterschätzt den Süden strukturell um ~74 % — die Ursache benennt der Bericht selbst (3-Regionen-ERF nach Winklmayr 2022 vs. 4-Regionen-Rechnung des RKI seit 2025). Einen bekannten Strukturfehler der Wirkungsfunktion über Niveaufaktoren zuzuschmieren, verletzt den Geist von 3.4 („Kalibrierung ist kein Verteilungsnachweis") in umgekehrter Richtung: Die Kalibrierung wird zum Verteilungsinstrument.
- **Vorschlag:** Ursache statt Symptom beheben: Sofern die EB-19/2025-Methodik regionale Schwellen/Steigungen für die vier RKI-Regionen ausweist, diese als ERF-Parameter übernehmen; andernfalls T₀/β je RKI-Region auf den Bundesland-Reihen des Anhangs nachschätzen. Erwartung danach: c_kal je Region ≈ 1; verbleibende Faktoren sind dann echte Modellbias-Korrektur. Falls die regionale Kalibrierung bewusst beibehalten wird: Grundsatz-Dokument fortschreiben (begründete Ausnahme von „ein Skalar" mit Kriterium, wann regionale Faktoren zulässig sind) — nicht stillschweigend abweichen.

### Befund 3 — Regionen-Zuordnung nirgends definiert (3 ERF-Regionen × 4 Kalibrier-Regionen)
- **Stelle:** Kap. 2, 95-A(b)/(c).
- **Art:** Lücke.
- **Begründung:** β/T₀ folgen den Winklmayr-Regionen Nord/Mitte/Süd, c_kal den RKI-Regionen Norden/Osten/Westen/Süden. Weder die Zuordnung Bundesland → Region (für den Kalibrierlauf) noch Zelle → Region (für die Produktion, Grenzverlauf!) ist im Bericht definiert. Ein Prüfer kann den Kalibrierlauf so nicht reproduzieren (§3.9); zwei überlagerte Regionsschemata erzeugen zudem Kanten-Artefakte an Regionsgrenzen.
- **Vorschlag:** Zuordnungstabellen in den Bericht (Bundesland → ERF-Region und → Kalibrier-Region; Zellen über Bundesland- oder Koordinatenregel). Entfällt weitgehend, wenn Befund 2 über einheitliche 4 Regionen gelöst wird.

### Befund 4 — r_0,a: genannte Raten widersprechen dem genannten Verhältnis; Herkunft des Verhältnisses fehlt
- **Stelle:** Kap. 2, Zeichentabelle r_0,a.
- **Art:** Fehler + Lücke (Herleitungspflicht 3.9).
- **Begründung:** Nachrechnung: Die Raten 1,9 / 6,3 / 10,8 / 15,6 je 100.000 ergeben bevölkerungsgewichtet 3,54 ✓ (Summenanker stimmt), entsprechen aber dem Verhältnis **1 : 3,3 : 5,7 : 8,2** — nicht dem im Text behaupteten „1 : 5 : 8 : 10". Echtes 1:5:8:10 bei Summe 3,5 ergäbe 1,53 / 7,63 / 12,21 / 15,26. Eine der beiden Angaben ist falsch. Zudem ist die Herkunft des „Kreislauf-Ratenverhältnisses" (welcher Datensatz, welche Zahlen?) nicht angegeben — 3.9 verlangt bei Abschätzungen die Begründung des Zahlenwerts.
- **Vorschlag:** (a) Text und Zahlen konsistent machen und den Rechenweg (Normierung auf 3,5) zeigen. (b) Verhältnis mit Quelle belegen: Vollstationäre Kreislauf-Einweisungsraten (ICD I00–I99) je Altersgruppe sind offen über GBE-Bund/GENESIS 23131 abrufbar — Zahlen zitieren. (c) Der Ersetzungspfad (T67 nach Alter, sobald abrufbar) ist als Registry-Hinweis in Ordnung, ersetzt aber nicht die jetzige Herleitung.

### Befund 5 — Wahl der Hitzetag-Elastizität (unkonditional 0,054) unbegründet; Faktor > 2 im Ergebnis
- **Stelle:** Kap. 2, Zeichentabelle e_HD,a.
- **Art:** Lücke.
- **Begründung:** K&Z liefern 0,054 (unkonditional), 0,024 (konditional), 0,061 (Hitzewellentag). Die Basiswahl „unkonditional" wird nicht begründet, verändert F_Zelle aber um mehr als Faktor 2. Zusätzlich ist ungeklärt, ob die an anderer Stelle genannte Harvesting-Korrektur (−25 %) auf die Morbidität angewendet wird.
- **Vorschlag:** Wahl explizit begründen. Empfehlung: konditional (0,024) als Basis — konsistent zur Konservativitäts-Linie des Berichts und näher am marginalen Effekt eines *zusätzlichen* Hitzetags —, unkonditional als Obergrenze des Bands; Harvesting-Behandlung für F in einem Satz festlegen.

### Befund 6 — HD_ref ohne Zahlenwert
- **Stelle:** Kap. 2, Formel F_Zelle + Zeichentabelle HD, HD_ref.
- **Art:** Lücke (3.9 nennt Defaults/Referenzwerte ausdrücklich).
- **Begründung:** Die Formel [1 + e_HD·(HD − HD_ref)₊] ist ohne HD_ref-Wert nicht auswertbar. Sachlogisch muss HD_ref die Hitzetag-Last der Periode sein, aus der die Baseline r_0,a stammt (K&Z-Basisperiode 1999–2008: Ø 7,2 Tage/Jahr) — sonst wird der in r_0 bereits enthaltene Durchschnittseffekt doppelt gezählt (LF 4).
- **Vorschlag:** HD_ref = 7,2 Tage/Jahr setzen, Herleitung (ein Satz: Basisperiode der Baseline) in die Zeichentabelle; als räumlich konstanten Registry-Parameter führen.

### Befund 7 — v_vers wirkt unverändert auf die Morbidität: β_d und β_pfl sind dort unbelegt bzw. widerlegt
- **Stelle:** Kap. 2, Formel F_Zelle (Faktor v_vers).
- **Art:** Fehler (Verstoß gegen G4/3.2 „nur belegte Sensitivitäten").
- **Begründung:** (a) β_d stammt aus Mortalitätsevidenz (Nicholl: transportierte Notfälle); für *Einweisungen* ist die Richtung eher invers (Distanz = Zugangsbarriere → weniger Einweisungen, höhere Schwere). (b) Für β_pfl auf Einweisungen existiert Gegen­evidenz: Die belgische Case-Crossover-Studie (10 Pflegeheime, 2013–2017) findet bei Hitzewellen einen signifikanten Mortalitätseffekt (OR 1,61), aber **keinen** Hospitalisierungseffekt (OR 0,96, n. s.) — Heimbewohner versterben eher vor Ort, statt eingewiesen zu werden. Beide Faktoren im F-Pfad sind damit nicht „empirisch belegt".
- **Vorschlag:** Für F einen eigenen Modifikator-Satz definieren: nur β_iso behalten (Isolation wirkt plausibel auf beide Endpunkte), β_d und β_pfl im F-Pfad auf 1 setzen; Begründung mit der belgischen Studie (Quelle ins Verzeichnis: „Impact of Heat Waves on Hospitalisation and Mortality in Nursing Homes: A Case-Crossover Study", Int J Environ Res Public Health 18:10697, 2021, doi:10.3390/ijerph182010697).

### Befund 8 — β_pfl wirkt über alle Altersbänder, ist aber nur für 85+ hergeleitet
- **Stelle:** Kap. 2, Formel v_vers / D_a.
- **Art:** Fehler.
- **Begründung:** v_vers multipliziert D_a für **alle** Bänder; q̄_pfl = 0,149 ist aber der Heimbewohner-Anteil **der 85+-Bevölkerung**, und die OR-Herleitung (Fouillet, Bouchama, Klenk) betrifft Hochaltrige/Pflegebedürftige. Auf u65 angewendet ist der Faktor sinnentstellt (u65-Zellwerte ohne Heim werden pauschal ×0,73 gedämpft).
- **Vorschlag:** Modifikator bandspezifisch machen: v_vers,a mit bandspezifischen q̄_pfl,a aus der Pflegestatistik (vollstationäre Quoten existieren auch für 65–74 und 75–84); mindestens aber β_pfl auf die Bänder 75–84/85+ beschränken und das dokumentieren.

### Befund 9 — β_pfl-Herleitungskette an drei Stellen nicht reproduzierbar bzw. falsch zugeordnet
- **Stelle:** Kap. 2, Zeichentabelle β_pfl.
- **Art:** Fehler (Reproduzierbarkeit, 3.9).
- **Begründung:** (a) Der „Exzess-Faktor 1,32" folgt nicht aus den genannten O/E-Werten: Heime 1,9 ÷ Wohnung ≥75 1,9 = 1,0; ÷ Kliniken 1,5 = 1,27 — wie 1,32 entsteht (Gewichtung?), steht nicht da. (b) Der Schritt „Bouchama … Referenzgruppe selbst zu 56 % pflegebedürftig ⇒ effektiv ≈ 3" ist behauptet, nicht gerechnet. (c) Klenk 2010 (+62 % bei ≥ 34 °C) misst die Temperatur-Steigung **innerhalb** von Heimen, nicht das Niveau Heim vs. Nicht-Heim — als Stütze für das Niveau-OR („stützt 1,9") falsch zugeordnet (LF 10: falsch zugeordneter Beleg).
- **Vorschlag:** Rechenkette für 1,32 und für die Bouchama-Adjustierung ausschreiben (Zwischenwerte); Klenk-Zitat umwidmen (Beleg für die ERF-Gültigkeit im Heim-Setting, nicht für das Niveau); der gewählte Wert 3,5 mit Band 2,2–6,0 kann bestehen bleiben, wenn die Kette steht.

### Befund 10 — VOLY: Bandobergrenze 169,5 T€ nicht reproduzierbar; Preisstand-Label inkonsistent
- **Stelle:** §1.2 (VOLY-Herleitung) + Zeichentabelle VOLY.
- **Art:** Fehler.
- **Begründung:** Nachrechnung der genannten Faktoren: Zentralwert 160,8 T€ ✓ und Untergrenze 136,4 T€ ✓ reproduzieren exakt. Die Obergrenze „Raumtransfer ohne Elastizität" ergibt aber 79.500 × 1,4638 × 1,2140 × 1,1719 = **165,6 T€** (bzw. 170,3 T€, wenn auch die Einkommensfortschreibung ohne Elastizität gemeint ist) — nicht 169,5 T€. Zudem: Alle Indexendpunkte sind 2024 (VPI 119,3; BIP/Kopf 2024), das Ergebnis ist als „€₂₀₂₅" etikettiert.
- **Vorschlag:** Definieren, welche Faktorkombination die Obergrenze bildet, Rechnung zeigen, Wert korrigieren (165,6 oder 170,3). Preisstand ehrlich als €2024 labeln oder mit VPI 2024→2025 auf €2025 fortschreiben (ein zusätzlicher Faktor, eine Zeile).

### Befund 11 — #96: Kernparameter ΔS/S_ref nicht hergeleitet — 96-A ist damit nicht G14-fertig
- **Stelle:** Kap. 3, 96-A(b) Klimasignal.
- **Art:** Lücke (Herleitungspflicht 3.9 / LF 13 — der gravierendste G14-Verstoß im Bericht).
- **Begründung:** ΔS/S_ref ist **das** Klimasignal des Ansatzes und steht nur als nationales Band „≈ 0,15–0,25 (heute)" mit dem Hinweis „regional aus Stationsdaten". Es fehlen: die Definition von S_ref (Referenz-Saisonlänge — welche Arten, welches Kriterium, welcher Zahlenwert?), ΔBlühbeginn und ΔSaisonende als Zahlen je Region, und — anders als bei der Hitze (wochenquantile_region.csv) — Skript und Ergebnisdatei. Ohne S_ref ist nicht einmal prüfbar, ob 0,15–0,25 aus den zitierten Trends (−17…−26 Tage Blühbeginn, +19 Tage Vegetationsperiode) überhaupt folgt.
- **Vorschlag:** Analog zur Hitze durchziehen: DWD-Phänologie-CDC (Jahresmelder, Blühbeginn Hasel/Erle/Birke, Gräser-Blühbeginn/-ende je Naturraum/Bundesland) → S_ref-Definition festlegen (z. B. EAACI-Saisonkriterium konsistent zu d_Saison), ΔS je Region 1991–2020 vs. 1961–1990 berechnen, Ergebnis als CSV + Skriptpfad in den Bericht. Bis dahin ist 96-A als „Empfehlung mit offener Herleitung" zu kennzeichnen — nach eigener G14-Definition des Berichts nicht abnahmereif.

### Befund 12 — #96: natives Outcome und €-Wert nicht mehr proportional (P̂ nur im €-Pfad)
- **Stelle:** Kap. 3, 96-A(b), Formeln €_Zelle vs. ΔTage_Zelle.
- **Art:** Widerspruch (Beweislastregel 3.2 / LF 3).
- **Begründung:** €_Zelle enthält den Vegetationsfaktor P̂_Zelle, der native Karten-Ausweis ΔTage_Zelle nicht. Damit lässt sich der €-Wert einer Zelle nicht mehr auf ihre physische Größe zurückführen (€ ÷ Kostensatz ≠ Tage der Zelle) — genau das, was die Kernformel-Logik („Beweislastregel") verhindern soll.
- **Vorschlag:** P̂_Zelle in **beide** Formeln (empfohlen — die lokale Vegetationsmodulation ist ja gerade das Differenzierungsargument des Ansatzes); alternativ aus beiden, dann wirkt Vegetation nur in Schicht A.

### Befund 13 — #96: c_Jahr ohne Zahlen für direkten Anteil und Inflationsschritt
- **Stelle:** Kap. 3, Inputs/Zeichentabelle c_Jahr.
- **Art:** Lücke (3.9: „jede Umrechnung als Rechenschritt").
- **Begründung:** Angesetzt werden soll „nur der direkte Anteil, inflationsbereinigt" von Schramm 2003 (1.089–1.543 €, Preisstand ≈ 2000). Weder der direkte Anteil (Schramm weist die Aufteilung direkt/indirekt aus — welche Zahl?) noch der Inflationsfaktor 2000→2025 noch der resultierende €-Wert stehen im Bericht. Der Parameter, der in die €-Formel eingeht, hat damit keinen Zahlenwert.
- **Vorschlag:** Schramm-Tabelle zitieren (direkter Kostenanteil SAR), VPI-Faktor 2000→2025 aus der Destatis-Reihe (dieselbe Quelle wie in §1.2, ≈ ×1,55) als Rechenschritt, Ergebniswert mit Band in die Zeichentabelle.

### Befund 14 — #96: f = 0,70 aus Korrelationskoeffizienten abgeleitet — Kategorienfehler
- **Stelle:** Kap. 3, Zeichentabelle d_Saison (Faktor f).
- **Art:** Fehler.
- **Begründung:** Ein Korrelationskoeffizient r = 0,48–0,79 (Pollen-Symptom-Korrelation, Pfaar 2020) misst lineare Kovariation, nicht den „Anteil symptomatischer Tage an Saisontagen". f = 0,70 aus der Mitte des r-Bands zu nehmen, ist keine Herleitung, sondern eine Zahlenübertragung zwischen inkommensurablen Größen.
- **Vorschlag:** f aus Symptomlast-Daten ableiten — Bastl u. a. 2020 [53] liefern tagesgenaue Symptomlast-Indizes für Deutschland (Anteil Tage über Symptomschwelle je Saison wäre die passende Größe); alternativ f als reine Modellannahme mit Band führen und die r-Werte nur als qualitative Stütze (Pollen treibt Symptome) zitieren, nicht als Zahlenquelle.

### Befund 15 — #98: Attributionsschritt fehlt — 100 % des Dosistrends werden als „klimabedingt" gebucht, #96 attribuiert nur ~50 %
- **Stelle:** Kap. 4, 98-A(b) ΔDosis; Vergleich mit Kap. 3 (a_attr).
- **Art:** Widerspruch (zwischen Risiken) + Lücke.
- **Begründung:** Bei #96 wird der Saisontrend über Anderegg mit ≈ 50 % (19–84 %) dem Klimawandel zugerechnet. Bei #98 geht der volle beobachtete SSD-/Dosistrend als klimaattribuiert in ΔFälle ein — ohne Attributionsdiskussion. Das europäische „Brightening" seit den 1980ern ist aber zu einem relevanten Teil Aerosol-/Luftreinhalteeffekt (anthropogen, aber keine Klimawirkung im KWRA-Sinn); Lorenz 2024 nennt als Ursache „v. a. Bewölkungsabnahme", quantifiziert die Aufteilung Wolken/Aerosol jedoch nicht vollständig. Zwei Risiken im selben Bericht mit unvereinbarer Attributionslogik sind in jeder fachlichen Prüfung angreifbar.
- **Vorschlag:** Attributionsfaktor a_attr,UV einführen (Band, z. B. 0,5–1,0; Zentralwert begründen — Lorenz' Wolken-Befund spricht für einen hohen Wert, das Aerosol-Argument gegen 1,0) und die Diskrepanz zur #96-Logik explizit auflösen; mindestens als dokumentierte Sensitivität mit Wirkung auf ΔFälle ausweisen.

### Befund 16 — #98: k_UV ohne festgelegten Basiswert und ohne Fundstelle für die 11,3 %/Dekade
- **Stelle:** Kap. 4, Zeichentabelle k_UV + (c) Klimaanteil-Anker.
- **Art:** Lücke (3.9: exakte Fundstelle + Basiswert).
- **Begründung:** k_UV wird als „≈ 0,4–0,5" geführt; die Formel braucht einen Wert. Die Herleitung 4,9 %/Dekade ÷ 11,3 %/Dekade = 0,43 ist plausibel, aber die SSD-Trendzahl 11,3 %/Dekade für Dortmund ist nirgends bequellt (das DWD-Bundesmittel [33] liefert ≈ +1,5 %/Dekade — die 11,3 müssen aus Lorenz 2024 selbst stammen).
- **Vorschlag:** Basiswert k_UV = 0,43 setzen (= 4,9/11,3, Rechenschritt zeigen), Band 0,4–0,5 plus Satelliten-Stütze; Fundstelle der 11,3 %/Dekade in Lorenz 2024 (Tabelle/Seite) zitieren.

### Befund 17 — Zentrierungs-Mittelwerte ohne Zahl/Herleitung: d̄_KH, q̄_1P, q̄_out
- **Stelle:** Kap. 2 (d̄_KH, q̄_1P), Kap. 4 (q̄_out, q_out).
- **Art:** Lücke (3.9 nennt „Zentrierungs-Mittelwerte (q̄, d̄)" ausdrücklich; LF 13).
- **Begründung:** (a) d̄_KH (mittlere Krankenhaus-Distanz) hat keinen Zahlenwert — dabei ist er aus der vorhandenen Ebene HEALTHCARE_ACCESS als bevölkerungsgewichtetes Bundesmittel direkt berechenbar. (b) q̄_1P „≈ 0,40" ist gesetzt statt aus dem Zensus-2022-Haushaltsgitter exakt berechnet. (c) Für #98 fehlen Datenquelle und Werte für q_out je Zelle/Kommune **und** q̄_out vollständig — welcher offene Datensatz liefert den Außenbeschäftigten-Anteil (Kandidat: Beschäftigtenstatistik der BA je Kreis, Wirtschaftszweige Landwirtschaft/Bau; als Proxy kennzeichnen)?
- **Vorschlag:** Je Größe: Datensatz, Aggregationsregel, Zahlenwert, Skriptpfad (analog wochenquantile_region.csv). Für q_out den Beschaffungsweg (offen, keyless) konkret benennen oder den Faktor bis dahin auf 1 (Band dokumentiert).

### Befund 18 — Quellen [45]–[47] unverifiziert und bibliografisch unvollständig — tragen aber δ_HAP und die Maßnahmen-Effektgrößen
- **Stelle:** Kap. 6, [45]–[47]; Kap. 2 Maßnahmen-Hebel.
- **Art:** Lücke (3.8: „Sekundärfunde vor Übernahme im Volltext verifizieren"; jede Quelle mit Autor/Jahr/Titel/Organ/URL).
- **Begründung:** Der Bericht kennzeichnet die drei Quellen selbst als „über Suchergebnisse identifiziert". Da δ_HAP = 0,95 (0,85–1,00) und der Klimaanlagen-Interventionseffekt direkt daraus abgeleitet sind, hängt ein Formelparameter an unverifizierten Belegen.
- **Vorschlag:** Verifizierte Vollzitate übernehmen (im Zuge dieser Prüfung recherchiert):
  - **[45]** H. Feldbusch, A. Schneider, F. Matthies-Wiesler, A. Matzarakis, A. Peters, S. Breitner-Busch, V. Huber, „Assessing the effectiveness of the heat health warning system in preventing mortality in 15 German cities: A difference-in-differences approach", *Environment International* 203:109746, 2025. doi:10.1016/j.envint.2025.109746 (CC BY, Open Access; Datenzeitraum 1993–2020 — im Bericht steht „1993 bis 2020" implizit korrekt).
  - **[46]** G. M. Katz, K. A. Brown, V. Giannakeas, N. M. Stall, „Air Conditioning in Nursing Homes and Mortality During Extreme Heat", *JAMA Internal Medicine* 186(2):243–251, 2026 (online 15.12.2025). doi:10.1001/jamainternmed.2025.6595 (Open Access, PMC12706679; relativer OR 0,93 bestätigt).
  - **[47]** „The effectiveness of heat prevention plans in reducing heat-related mortality across Europe", *Environmental Research Letters*, 2025. doi:10.1088/1748-9326/ae2775 (Open Access; Autorenliste beim Wayback-Snapshot vom Artikel übernehmen).
  Wayback-Permalinks bei Übernahme in sources.py (Ratchet) ergänzen; die im Bericht zitierten Effektzahlen gegen die Volltexte gegenlesen (Stichprobe dieser Prüfung: RR 1,00/0,85 [45] und rOR 0,93 [46] stimmen).

---

## Kategorie B — sollte behoben werden

### Befund 19 — G12-Verteilungsprüfung ist teilweise in-sample
- **Stelle:** Kap. 2, 95-A(c), G12-Prüfung.
- **Art:** Lücke (3.4: „unabhängige Prüfung").
- **Begründung:** Die vier Regionalfaktoren wurden per Kleinste-Quadrate auf denselben Bundesland-Jahren gefittet, an denen anschließend die Verteilung geprüft wird („11 von 16 Länder im Band"). Nach dem Fit von 4 Niveauparametern ist diese Prüfung kein unabhängiger Verteilungsnachweis mehr.
- **Vorschlag:** Zeitlicher Holdout (Fit 1992–2015, Prüfung 2016–2024) oder Leave-one-out je Bundesland; Ergebnis in bundesland_validierung ergänzen. Die Altersverteilungs-Prüfung bleibt als unabhängige Achse — siehe Befund 20.

### Befund 20 — Altersverteilungs-Validierung: nur Soll beschrieben, kein Ist-Ergebnis
- **Stelle:** Kap. 2, 95-A(c), „Validierung Altersverteilung".
- **Art:** Lücke.
- **Begründung:** Der Absatz beschreibt, **dass** die modellierten Bandanteile gegen die RKI-Verteilung (6,5/12,9/25,2/55,5 %) zu prüfen sind — das Ergebnis dieser Prüfung fehlt, obwohl der Kalibrierlauf (Rev. 5) sie hätte mitliefern können. Sie ist nach Befund 19 die wichtigste verbleibende unabhängige Prüfung.
- **Vorschlag:** Modellierte Bandanteile aus dem Kalibrierlauf ausweisen (eine Zeile: Modell x/x/x/x % vs. RKI 6,5/12,9/25,2/55,5 %) und bewerten.

### Befund 21 — „Konservativ" wird in zwei entgegengesetzten Bedeutungen verwendet; Vollreihe-vs.-Fenster-Entscheidung daran aufgehängt
- **Stelle:** §1.2 („bewusst konservativ" = Untergrenze) vs. Kap. 2(c) („konservativ wird der Vollreihen-Wert geführt" = 2021–2025 um +50–65 % überschätzend).
- **Art:** Widerspruch (Terminologie) + offene methodische Entscheidung.
- **Begründung:** Der Vollreihen-Faktor 1,027 überschätzt die aktuelle Ära systematisch (Anpassungssignal); das Fenster 2012–2025 (0,890, R² 0,63) ist konsistent zur Herkunfts-Ära der β (2012–2021) und senkt die Werte um ~13 %. „Konservativ" kann beides rechtfertigen — je nach Definition.
- **Vorschlag:** Begriff einmal definieren (Vorschlag: konservativ = unterschätzend, wie in §1.2) und die Wahl neu begründen. Empfehlung: Fenster 2012–2025 als Basis (aktuelle ERF-Ära, beste Prognosegüte für den Ausweis „erwarteter Jahresschaden heute"), Vollreihe als obere Sensitivität; mittelfristig Zeittrend der ERF explizit (der Bericht benennt die Lücke bereits).

### Befund 22 — L̄_85+ mit Bevölkerungs- statt Sterbefallgewichten
- **Stelle:** Kap. 2, Zeichentabelle L̄_a (85+-Herleitung).
- **Art:** Fehler (klein, Richtung: Überschätzung).
- **Begründung:** Die 85+-Restlebenserwartung wird über e(85)/e(90)/e(95) mit **Bevölkerungs**gewichten (754.258/197.380/38.654) gemittelt. Verlorene Lebensjahre je *Sterbefall* verlangen die Gewichtung mit der Altersverteilung der **Sterbefälle** im Band — die liegt weiter oben, L̄ fällt entsprechend niedriger aus (Richtung sicher, Größenordnung wenige Zehntel Jahre; mit Datensatz [49] direkt berechenbar).
- **Vorschlag:** Mit Sterbefällen 2023 je Teilband (85–89/90–94/95+) neu gewichten; Konsistenz-Bonus: dieselbe Logik wie „Todesfälle je Altersband × Restlebenserwartung".

### Befund 23 — Preisstände der Kostensätze inkonsistent
- **Stelle:** Kap. 2 (c_Fall €2023), Kap. 3 (Schramm €2000), Kap. 4 (Speckemeier: AOK-Daten ~2017–2019, unindexiert), §1.2 (VOLY €2024/„2025").
- **Art:** Lücke (3.3: Preisstand und Konsistenz; LF 9).
- **Begründung:** Die €-Summe einer Kommune addiert Kostensätze aus vier verschiedenen Preisständen. Bei 4–6 % kumulierter Inflation je Lücke ist das kein Rundungsthema mehr.
- **Vorschlag:** Gemeinsamer Preisstand €2025 für alle Kostensätze; VPI-Umrechnungsfaktoren je Satz als Rechenschritt in die Zeichentabellen (dieselbe Destatis-Reihe wie in §1.2).

### Befund 24 — Vorläufiger 2025-Wert in der Kalibrierreihe
- **Stelle:** Kap. 2(c), Ankerreihe („2025: 2.500, RKI-Wochenbericht KW 38") und „27 signifikante Jahre 1992–2025".
- **Art:** Lücke (3.4: laufende/vorläufige Jahre gesondert behandeln).
- **Begründung:** 2026 wird korrekt ausgeschlossen; 2025 stammt aber ebenfalls aus dem (vorläufigen) Wochenbericht, nicht aus der revidierten Reihe (die bis 2024 reicht). Die Revisionen 2015/2018/2019 (+500…+1.000) zeigen, dass Wochenbericht-Werte sich merklich verschieben können.
- **Vorschlag:** c_kal-Sensitivität ohne 2025 ausweisen (eine Zahl); 2025 bei Erscheinen der revidierten Fassung nachziehen (Registry-Vermerk).

### Befund 25 — Datenverfügbarkeits-Prüfpunkte für zwei Zellgrößen offen
- **Stelle:** Kap. 2, Inputs (q_1P: „Zensus-2022-Haushaltsgitter", q_pfl: „OSM-Pflegeeinrichtungen × Pflegestatistik").
- **Art:** Lücke (LF 12 Umsetzbarkeit; 3.1 Proxy-Kennzeichnung).
- **Begründung:** (a) Ob die Kreuzung „Einpersonenhaushalte × 65+" im offenen 100-m-Gitter des Zensus 2022 tatsächlich vorliegt, ist zu verifizieren — publiziert sind Haushaltsgrößen und Altersstruktur, die Kreuzung auf Gitterebene möglicherweise nicht; dann ist q_1P ein Proxy (Gesamt-1P-Anteil × Kreis-Alterskorrektur) und muss so gekennzeichnet werden. (b) OSM-Vollständigkeit bei Pflegeeinrichtungen variiert regional; der Skalierungsschritt gegen die Kreis-Pflegestatistik fängt das teilweise, sollte aber als Proxy-Eigenschaft dokumentiert sein.
- **Vorschlag:** Beide Verfügbarkeiten vor Implementierung prüfen (ein Satz Ergebnis in den Bericht); Fallback-Definitionen jetzt schon festschreiben.

---

## Kategorie C — formal/redaktionell

### Befund 26 — Kopfzeilen Kap. 2/4 widersprechen §1.2 („Übersterblichkeit × VSL" / „Mortalitätsanteil × VSL")
- **Art:** Widerspruch (redaktionell). **Begründung:** Die Konto-Zeilen der Risikokapitel zitieren noch den VSL-Weg, §1.2/G2 schreiben YLL × VOLY vor. **Vorschlag:** Entweder als Originalwortlaut der Monetarisierungs-Arbeitsmappe kennzeichnen („Umsetzung nach §1.2: YLL × VOLY") oder Text angleichen.

### Befund 27 — Kap. 5 nennt noch „Faktor 1,44"
- **Art:** Widerspruch (redaktionell). **Begründung:** Die Empfehlungsbegründung #95 („national kalibriert, Faktor 1,44") ist durch Rev. 5 überholt (0,618–1,737 bzw. 1,027). **Vorschlag:** Kap.-5-Text auf den Rev.-5-Stand aktualisieren.

### Befund 28 — „Eine native Ergebnisgröße je Risiko-Code" nicht deklariert
- **Art:** Lücke (3.6). **Begründung:** #95 weist YLL, Fälle und € aus, #98 YLL und ΔFälle — welcher davon **die** native Größe ist und wie die übrigen als Teil-Ausweise unter der KWRA-Klammer laufen, steht nirgends. **Vorschlag:** Je Risiko ein Satz: 95 → nativ YLL/Jahr (Fälle = Teil-Ausweis Morbidität); 96 → nativ ΔTage; 98 → nativ YLL (ΔFälle = Teil-Ausweis).

### Befund 29 — Knoten-Bilanz fehlt: R36 rechnet in #96/#98 nirgends, S154/S155 in #96 nur benannt
- **Art:** Lücke (LF 1). **Begründung:** R36 (Gesundheitsinfrastruktur) steht in den Wirkungsketten von #96 und #98, taucht aber weder in Schicht-A-Index noch Formeln auf; S154/S155 bei #96 analog. Bewusst inaktive Knoten sind zulässig (Handlungsfeld-Vererbung, die die Aufgabe selbst als Unschärfe benennt) — aber es muss dastehen. **Vorschlag:** Je Risiko eine kleine Knoten-Bilanz-Tabelle: Knoten → rechnet in (Schicht A / Schicht B / Maßnahmen-Hebel / bewusst inaktiv + Begründung). Beantwortet Leitfrage 1 systematisch für alle künftigen Risiken mit.

### Befund 30 — G14-Geltungsbereich (nur Ansatz A) weicht von Aufgabe 3.9 („ohne Ausnahme") ab
- **Art:** Widerspruch (dokumentiert). **Begründung:** Der Bericht beschränkt die volle Herleitungspflicht auf den empfohlenen Ansatz; 3.9 kennt keine Ausnahme. Die Beschränkung ist pragmatisch vertretbar (Alternativen sind keine Umsetzungsgrundlage), aber derzeit eine einseitige Abweichung von der Prüfgrundlage. **Vorschlag:** Einvernehmlich auflösen — bevorzugt die Aufgabe präzisieren („Herleitungspflicht gilt für die Umsetzungsgrundlage; dokumentierte Alternativen bis zur Quelle"), sonst die Alternativ-Parameter nachziehen. **Status-Update (Durchgang 4):** Verschärft — auch G14 im nachgereichten Grundsatz-Dokument kennt **keine** Geltungsbereichs-Ausnahme („Kein Formelzeichen ohne abgeschlossene Herleitung im Bericht selbst"); der Bericht schränkt einseitig auf zwei Ebenen ein. Übernahmefertiger Fortschreibungstext für METHODIK_GRUNDSAETZE.md liegt in T2.4 bei.

### Befund 31 — Prüfhinweis: docs/METHODIK_GRUNDSAETZE.md lag der Gegenprüfung nicht bei
- **Art:** Lücke (Prüfbarkeit). **Begründung:** Die Anforderungen 3.6 (Raten-Darstellung, UI-Abgrenzungen, Versionsstempel) verweisen auf G10–G13, die ausgelagert sind; ohne das Dokument sind sie nur indirekt prüfbar. **Vorschlag:** Für die finale Gegenprüfung beilegen; diese Befundliste deckt die G10–G13-Punkte nur, soweit sie im Bericht selbst sichtbar werden. **Status-Update (Durchgang 4): GESCHLOSSEN** — Dokument nachgereicht und geprüft; Ergebnis im Durchgang-4-Abschnitt (Bestätigung der G-Nummerierung und der G6/G8-Inhalte; zwei neue Befunde 55/56).

---

## Nachtrag — zweiter Prüfdurchgang (Befunde 32–49)

Ergebnis einer zweiten, vertieften Passage mit Fokus auf: vollständige Anwendung der 3.9-Beispielliste, Bandkonsistenz aller Modifikatoren, Szenario-/Zeitbezug, Maßnahmen-Implementierbarkeit und Formelketten-Konsistenz zwischen den Risiken.

### Kategorie A (Ergänzung)

#### Befund 32 — Altersfaktoren f_a ohne Rückrechnung übernommen — der in Aufgabe 3.9 wörtlich genannte Beispielfall; zusätzlich Kopplung an die neuen m_a
- **Stelle:** Kap. 2, Inputs + Zeichentabelle f_a (0,404 / 0,577 / 0,620 / 1,0 — „aus publizierter Altersverteilung zurückgerechnet").
- **Art:** Lücke (Herleitungspflicht 3.9) + latenter Folgefehler.
- **Begründung:** Aufgabe 3.9 nennt als Beispiel für „Abgeleitet" ausdrücklich: „**Altersverteilung → Altersfaktoren**" — mit vollständiger Rechenkette und Zwischenwerten. Genau diese Rückrechnung (RKI-Altersverteilung der Hitzetoten + Bevölkerungsanteile + Basissterberaten → Steigungsverhältnisse) steht nirgends im Bericht; die vier Werte erscheinen nur in der Zeichentabelle. Verschärfend: Die Rückrechnung hängt von den Basissterberaten m_a ab — und die wurden in Rev. 5 selbst korrigiert (u65 +18,4 %, übrige −3…+5 %). Wurden die f_a mit den **alten** Konstanten zurückgerechnet, sind sie mit den neuen m_a inkonsistent; das u65-Band würde dann um grob den Korrekturfaktor verzerrt.
- **Vorschlag:** Rückrechnung als Rechenkette in den Bericht (Formel, RKI-Anteile je Band, Zwischenwerte, Ergebnis) und mit den Rev.-5-m_a neu durchführen; Abweichung zu den bisherigen 0,404/0,577/0,620 ausweisen. Anschließend Validierung Altersverteilung (Befund 20) neu laufen lassen — beide hängen zusammen.

#### Befund 35 — #96: Prävalenz-Altersgruppen (Kinder/Erwachsene) passen nicht auf die Altersbänder des Produkts; benötigte u18-Ebene fehlt
- **Stelle:** Kap. 3, 96-A(a)/(b) („Betroffene = Σ pop_a · p_AR,a, altersspezifisch, G3").
- **Art:** Lücke (LF 12 Umsetzbarkeit; 3.1 Kennzeichnung „neu anzulegen").
- **Begründung:** Die Prävalenzen liegen für Kinder (KiGGS: 8,8 %) und Erwachsene (DEGS1: 12,0 %) vor; das Produkt führt laut Kap. 2 aber die Altersbänder u65 / 65–74 / 75–84 / 85+ (mit 65+-Fallback). Eine u18-Bevölkerungsebene, ohne die „altersspezifisch" nicht rechenbar ist, existiert im Bericht nicht und ist nirgends als „neu anzulegen" gekennzeichnet. Der empfohlene Ansatz ist damit in seiner Kernformel derzeit nicht implementierbar wie beschrieben.
- **Vorschlag:** Entweder (a) u18-Ebene aus dem offenen Zensus-2022-Gitter (10-Jahres-Altersklassen) als neue Ebene kennzeichnen und die Bandzuordnung (u18 → Kinder-Prävalenz; Rest → Erwachsenen-Prävalenz) definieren, oder (b) eine bevölkerungsgewichtete Misch-Prävalenz je Zelle herleiten (Rechenschritt zeigen). Variante (a) ist sauberer und deckt G3 wirklich ab.

### Kategorie B (Ergänzung)

#### Befund 33 — δ_HAP: Wirkungsort im Modell nicht definiert (auf β oder auf das Ergebnis?)
- **Stelle:** Kap. 2, Maßnahmen-Hebel („Setzung: δ_HAP zentral 0,95"); Maßnahmen-Angriffspunkte („Dämpfungsfaktor auf β").
- **Art:** Lücke.
- **Begründung:** Der Absatz „Maßnahmen-Angriffspunkte" spricht von einer Dämpfung **auf β**, die Evidenz ([45], [47]) misst aber Ergebnis-Effekte (RR der Mortalität). Wegen der Exponentialform sind beide Anwendungen nicht identisch (Nachrechnung: β×0,95 dämpft den Exzess je nach Wochenhitze um 5,1–5,7 %, Ergebnis×0,95 konstant um 5,0 %) — klein im Zentralwert, aber definitionsbedürftig, sobald das Band (0,85) gezogen wird.
- **Vorschlag:** δ_HAP als multiplikativen Faktor auf den Exzess (RR − 1) definieren — konsistent zur Studienart der Evidenz — und die β-Formulierung im Maßnahmen-Absatz streichen.

#### Befund 34 — Maßnahmen ohne modellwirksame Effektgröße: #96 Stadtbaumwahl, #98 UV-Schutz
- **Stelle:** Kap. 3 und Kap. 4, Maßnahmen-Angriffspunkte.
- **Art:** Lücke (Aufgabe 2.6: Hebel „mit Effektgrößen belegt").
- **Begründung:** Für „Allergenarme Stadtbaumwahl" ist als Beleg nur die GALK-/Artenliste genannt — eine Auswahlliste, keine Effektgröße; für „UV-Schutz im öffentlichen Raum" nur Nutzen-Kosten-Verhältnisse (2,2–8,7 : 1) — ein BCR ist keine im Modell anwendbare Dosis- oder Inzidenzwirkung. Beide Hebel sind damit derzeit nicht rechenbar.
- **Vorschlag:** Stadtbaumwahl als **modellendogenen** Hebel formalisieren: Ersatz von x % allergener Arten → ΔĜ_allergen → Wirkung über λ (Rechenweg angeben; das ist zulässig, muss aber so deklariert werden — die „Effektgröße" ist dann die Vegetationssensitivität λ selbst, Befund zur λ-Herleitung beachten). UV-Schutz: Programm-Evaluationen mit Verhaltens-/Dosisendpunkten heranziehen (z. B. SunSmart-Evaluationen) oder den Hebel ehrlich als „qualitativ, nicht quantifiziert" führen; das BCR nur als Wirtschaftlichkeits-Kontext zitieren.

#### Befund 36 — d_Saison-Kette: p_G/p_B nicht direkt aus DEGS1 ablesbar; Saison-Überlappung wird doppelt gezählt
- **Stelle:** Kap. 3, Zeichentabelle d_Saison (d = f · (p_G·L_G + p_B·L_B); p_G = 0,75, p_B = 0,55 „(DEGS1 [3])").
- **Art:** Lücke + kleiner Fehler.
- **Begründung:** (a) DEGS1/Haftenberger [3] weist Sensibilisierungsprävalenzen der **Allgemeinbevölkerung** aus; benötigt wird der Anteil **unter AR-Patienten**, der gegen Gräser bzw. Birke reagiert — eine andere Größe, deren Umrechnung nicht gezeigt ist. (b) Die additive Form p_G·L_G + p_B·L_B zählt bei Doppelt-Sensibilisierten die überlappenden Wochen (Birke/Gräser, v. a. Mai) doppelt; korrekt wäre die Vereinigungsmenge der Saisonfenster je Sensibilisierungsprofil.
- **Vorschlag:** p_G/p_B aus einer geeigneten Quelle für AR-Patienten belegen (Versorgungsdaten/PID) oder die Umrechnung Bevölkerungs-Sensibilisierung → Patientenanteil als Rechenschritt zeigen; Überlappungskorrektur einbauen (senkt d_Saison leicht — Richtung konservativ) oder als dokumentierte Überzeichnung ausweisen.

#### Befund 37 — #98: Mittelungszeiträume für SSD_heute und SSD_ref je Zelle nicht definiert
- **Stelle:** Kap. 4, 98-A(b), ΔDosis-Formel.
- **Art:** Lücke (3.9; Reproduzierbarkeit).
- **Begründung:** ΔDosis = (SSD_heute − SSD_ref)/SSD_ref × k_UV ist ohne Definition der Fenster nicht auswertbar: Ist SSD_ref das Zell-Mittel 1961–1990 und SSD_heute das Zell-Mittel 1991–2020 (analog zum zitierten Gebietsmittel-Vergleich)? Einzeljahre wären wegen der SSD-Variabilität (Rekordjahre ~2.020 h) ungeeignet.
- **Vorschlag:** Beide Fenster als Klimanormalperioden je Zelle festlegen (1961–90 vs. 1991–2020), Datenverfügbarkeit des 1-km-Rasters ab 1961 bestätigen, in die Zeichentabelle aufnehmen.

#### Befund 38 — UHI-Verschiebung des hot_days-Rasters: Umrechnungsregel nicht im Bericht
- **Stelle:** Kap. 2, Inputs („DWD-CDC-Raster hot_days (1 km) + UHI-Verschiebung") und Zeichentabelle HD.
- **Art:** Lücke (3.9).
- **Begründung:** Wie aus dem 24-h-UHI-Zuschlag (in K) eine Verschiebung der Hitzetage-**Zählung** (Tmax > 30 °C) wird, ist nicht hergeleitet — die Ebene existiert offenbar im Produkt, aber der Bericht muss die Regel enthalten (z. B. Verschiebung der Tmax-Verteilung um die Tag-Komponente des UHI und Neuauszählung; mit welcher Verteilungsannahme?). Ohne Regel ist HD je Zelle nicht reproduzierbar, und die Tag-/Nacht-Aufteilung des UHI (das 24-h-Mittel enthält beide) ist genau hier entscheidend.
- **Vorschlag:** Umrechnungsregel dokumentieren (welche UHI-Komponente, welche Verteilungsannahme, Mittelwerttreue analog Temperatur) und mit ein bis zwei Zell-Beispielen belegen.

#### Befund 39 — Szenario-Anwendung für 95-A und 98-A nicht spezifiziert; Stationaritätsannahme der q_w unbenannt
- **Stelle:** Kernformel §1.2 („je Klimaszenario") vs. Kap. 2/4 (nur Ist-Klima beschrieben).
- **Art:** Lücke (3.2 „Zeitbezug sauber: Jahreswerte, Szenariojahre").
- **Begründung:** 96-B nennt Szenario-Deltas, 96-A die GE-KL-07-Projektion — für die empfohlenen Ansätze 95-A und 98-A fehlt dagegen die Angabe, wie ein Klimaszenario eingeht. Naheliegend ist der T̄-Shift je Zelle bei unveränderten Anomalie-Quantilen q_w — das ist aber eine Stationaritätsannahme (Hitzewellen-Variabilität nimmt in Projektionen zu) und muss als solche dokumentiert werden; für #98 analog die SSD-Fortschreibung (Eleftheratos-Trend?).
- **Vorschlag:** Je empfohlenem Ansatz einen Absatz „Szenario-Anwendung": Eingangsgröße, die verschoben wird, konstant gehaltene Größen, Stationaritätsannahmen mit Band. Für M0 reicht der Ist-Ausweis — dann explizit sagen, dass Szenariofähigkeit ab welcher Stufe kommt.

#### Befund 40 — Wochenquantile repräsentieren das mittlere Jahr; die Hitzejahr-Residuen (2006 −52 %, 2015 −42 %) sind das Symptom
- **Stelle:** Kap. 2, 95-A(b) Quantil-Herleitung + (c) Kalibrierlauf-Residuen.
- **Art:** Lücke (dokumentierte Modellgrenze fehlt; Verbesserung möglich).
- **Begründung:** Die 13 Quantile aus der gepoolten Anomalie-Klimatologie bilden näherungsweise das **mittlere** sortierte Sommerprofil ab; Jahre mit ausgeprägten Hitzewellen bei moderatem Sommermittel (2006: Juli-Extrem; 2015) haben real heißere obere Wochen, als der reine Mittelwert-Shift erzeugt. Genau diese Jahre unterschätzt der Kalibrierlauf massiv — die Residuen belegen die Modellgrenze, der Bericht zieht daraus aber keine Konsequenz (weder Erklärung noch Gegenmaßnahme benannt).
- **Vorschlag:** Mindestens: die Residuen 2006/2015 explizit dieser Modellgrenze zuschreiben (ein Absatz). Besser: Kopplung der oberen Quantile an das Sommermittel des Jahres prüfen (Regression q₁₂/q₁₃ auf T̄_Jahr aus derselben Stationsklimatologie — Daten liegen vor); als Sensitivität ausweisen.

#### Befund 41 — Entitäten-Split 2015 wird altersinvariant auf 2023er C44-Raten angewendet
- **Stelle:** Kap. 4, Inputs (Entitäten-Split BCC/SCC/MM, 2015, BfS) + Formel Ie,a.
- **Art:** Lücke.
- **Begründung:** Der BCC/SCC-Split stammt aus 2015 und wird als Aggregat auf die altersspezifischen C44-Raten 2023 gelegt. SCC ist stärker altersassoziiert als BCC; ein altersinvarianter Split verschiebt bei sehr alten Kommunen die Entitäten-Mischung — und damit über BAF (2,5 vs. 1,4) und Letalität den klimaattribuierten Zusatz.
- **Vorschlag:** Prüfen, ob Baldermann & Lorenz [27] altersabhängige Splits hergeben; sonst die Altersinvarianz als dokumentierte Annahme mit Richtungsabschätzung führen (SCC-Anteil bei Alten unterschätzt → ΔFälle-Unterschätzung in alten Kommunen).

#### Befund 44 — Erweiterung zu Befund 8: Bandbeschränkung gilt auch für β_iso — v_vers durchgängig als v_vers,a definieren
- **Stelle:** Kap. 2, Formel v_vers.
- **Art:** Fehler (Erweiterung).
- **Begründung:** Nicht nur β_pfl (Befund 8), auch β_iso ist bandfremd angewendet: q_1P ist der Anteil Einpersonenhaushalte **65+**, die Semenza-Evidenz betrifft Ältere — der Faktor multipliziert aber auch das u65-Band. Die saubere Lösung ist eine einzige: v_vers,a je Altersband definieren, mit bandspezifischen q̄ und dokumentierter Bandzuordnung je Faktor (β_d: alle Bänder; β_iso: 65+; β_pfl: 75+/85+).
- **Vorschlag:** v_vers,a einführen; eine kleine Tabelle „Faktor × Band × q̄_a" ersetzt drei Einzeldiskussionen.

#### Befund 47 — Kalibrier-Fits uneinheitlich gefiltert und Sensitivitäten unvollständig
- **Stelle:** Kap. 2, 95-A(c).
- **Art:** Widerspruch (Methodenkonsistenz) + Lücke.
- **Begründung:** (a) Der nationale Fit läuft „über die 27 **signifikanten** Jahre", der regionale Fit „über **alle** Bundesland-Jahre 1992–2024" — zwei verschiedene Auswahlregeln für denselben Parameter-Typ, unbegründet. (b) Die Fenster-Sensitivität (2012–2025: 0,890) existiert nur national; die operativen Größen sind aber die Regionalfaktoren — deren Fenster-Varianten fehlen.
- **Vorschlag:** Eine Auswahlregel für beide Ebenen festlegen (Empfehlung: Signifikanzfilter auch regional, da insignifikante Jahre v. a. Rauschen beitragen) und die Fenster-Sensitivität je Region ausweisen.

### Kategorie C (Ergänzung)

#### Befund 42 — c_Fall = 6.996 € ist der Durchschnitt **aller** Krankenhausfälle — Proxy nicht als Proxy gekennzeichnet
- **Stelle:** Kap. 2, Zeichentabelle c_Fall. **Art:** Lücke (3.1). **Begründung:** Hitzeassoziierte Einweisungen (überwiegend hochaltrige Herz-Kreislauf-/Nieren-Fälle) haben einen anderen Fallmix als der Bundesdurchschnitt aller Diagnosen; der Kostennachweis-Mittelwert ist ein Proxy. **Vorschlag:** Als Proxy kennzeichnen; optional DRG-/Diagnosegruppen-basierte Kostensätze als Sensitivität benennen.

#### Befund 43 — λ_e als Querschnittsverhältnis und L̄_e über medianes Sterbealter: Approximationen kennzeichnen (Erweiterung zu Befund 22)
- **Stelle:** Kap. 4, Zeichentabellen λ_e, L̄_e. **Art:** Lücke (Kennzeichnung). **Begründung:** λ_e = Sterbefälle ÷ Neuerkrankungen desselben Jahres ist bei steigender Inzidenz keine Kohorten-Letalität (Periodenapproximation); L̄_e = e(medianes Sterbealter) approximiert den Mittelwert über die Sterbealter-Verteilung. Beide Vereinfachungen sind vertretbar, stehen aber unmarkiert neben voll hergeleiteten Größen. **Vorschlag:** Je ein Halbsatz „Periodenapproximation"/„Median-Approximation" mit Richtung; #95-Analogie (Befund 22: Sterbefall- statt Bevölkerungsgewichtung) einheitlich lösen.

#### Befund 45 — Maßnahmen-Absatz Kap. 2 referenziert die abgeschaffte Größe „v_access"
- **Stelle:** Kap. 2, „Maßnahmen-Angriffspunkte" („v_access-Verbesserung"). **Art:** Widerspruch (redaktionell). **Begründung:** v_access wurde in Rev. 3 durch v_vers mit belegten Faktoren ersetzt; der Maßnahmen-Absatz (und 95-C: „wie 95-A (v_access)") hängt am alten Stand. **Vorschlag:** Auf v_vers,a bzw. die konkreten Faktoren umschreiben.

#### Befund 46 — Weitergabe-Ziel #101 (Kap. 2) vs. #102 (§1.2) inkonsistent
- **Stelle:** Kap. 2 Kopf („Weitergaben an #87 und #101") vs. §1.2-Tabelle („Systemvorhaltung → #102"). **Art:** Widerspruch (redaktionell, ggf. sachlich). **Begründung:** Entweder Tippfehler oder zwei verschiedene Zielrisiken — dann muss je Weitergabe das Ziel benannt sein (R9-Abgrenzung verlangt eindeutige Verweise). **Vorschlag:** Gegen die Monetarisierungs-Arbeitsmappe klären und vereinheitlichen.

#### Befund 48 — Anlagen der Herleitungen liegen der Prüfung nicht bei (Erweiterung zu Befund 31)
- **Stelle:** Kap. 2 (wochenquantile_region.csv, calibrate_heat_mortality.py, bundesland_validierung_*.csv, c_kal_ergebnis_*.md). **Art:** Lücke (Aufgabe 2.7: „ohne Rückfragen prüfbar"). **Begründung:** Die Rev.-5-Herleitungen verweisen auf Skripte/CSV im Repo; für eine externe Gegenprüfung (wie diese) sind sie Teil der Prüfgrundlage. Die Stichproben-Nachrechnungen dieser Prüfung ersetzen keine Durchsicht der Läufe. **Vorschlag:** Anlagenpaket (Skripte + Ergebnisdateien) dem Bericht beilegen oder als Anhang exportieren.

#### Befund 49 — #96: Sanity-Prüfung hat nur eine Obergrenze („≪ Destatis-KKR J30")
- **Stelle:** Kap. 3, 96-A(c) Kosten-Sanity. **Art:** Lücke (3.4: Unter- **und** Obergrenzen). **Begründung:** Anders als bei #95 (T67-Untergrenze, K&Z-Obergrenze) existiert für #96 keine Untergrenze — „deutlich kleiner als der Gesamttopf" ist als Plausibilisierung schwach. **Vorschlag:** Untergrenze definieren (Kandidat: klimaattribuierter Anteil der ambulanten J30-Verordnungskosten aus offenen GKV-/GBE-Daten) oder begründet dokumentieren, dass keine amtliche Untergrenze verfügbar ist.

---

## Durchgang 3 — Quellenabgleich gegen die Arbeitsmappen (Befunde 50–54)

Grundlage: KWRA-Schadensbaum_X_UBA-klimawirkungsketten.xlsx und KWRA-Monetarisierung.xlsx (erhalten 22.08.2026). Alle nachfolgenden Aussagen sind direkt aus den Sheets extrahiert.

### Quellenabgleich — bestätigt (Entlastung des Berichts)

- **Knoten-Treue der drei Wirkungsketten exakt:** W182 (Hitzebelastung): E02 · S152/S153/S154/S155/S157/S158 · R35/R36 · W124 ✓. W186 (UV): E20 · S154/S155/S158 · R35/R36 · keine vorgelagerten Wirkungen ✓. W189 (Aeroallergene): keine direkten Einflüsse · S158 · R35/R36 · W024+W025 ✓; W024: E01 · S010–S020 · R03/R04 ✓. Die §1.1-Zählung „25 Einflüsse" und „36 räumliche Faktoren" reproduziert aus dem Ketten-Sheet ✓.
- **Netzwerklisten-Ergänzungen korrekt referiert:** #63 → #95 (Innenraumklima) ✓ und #1 → #96 (Vegetationsperiode/Phänologie) ✓ stehen genau so in der Netzwerkliste.
- **Konten-Einbettung exakt:** #95 = Buchungsobjekt Ebene A, K1, „K1-Mortalität; K1-Morbidität" ✓ · #96 = Ebene B, K1, **nur** „K1-Morbidität" ✓ · #98 = Ebene B, K1, Mortalität + Morbidität ✓; Handlungserfordernis aller drei „sehr dringend" ✓; K1-Ursachenpartition (Hitze · Allergene · … · Extremereignisse) ✓.
- **Kernformel §1.2 wortgleich** mit dem Schadenskonten-System-Sheet ✓; R1–R11 vorhanden, R9-Verwendung im Bericht korrekt ✓.
- **Befund 46 aufgelöst:** Das Abgleich-Protokoll belegt die #95-Output-Kanten P8 (95 → 87) und P47 (95 → 101) — der Kap.-2-Kopf „Weitergaben an #87 und #101 laut Abgleich" ist **richtig**; die fehlerhafte Seite ist die §1.2-Tabelle (jetzt präzise gefasst in Befund 51). Befund 46 wird durch Befund 51 ersetzt.
- **Befund 26 präzisiert:** Die Kopfzeilen-Formulierungen „Übersterblichkeit × VSL" (Kap. 2) und „Mortalitätsanteil × VSL" (Kap. 4) sind **wörtliche Zitate** der Spalte „Bewertungsansatz/Kostensatz" der Risiken-Monetarisierung (Zeilen 95/98). Lösung: als Arbeitsmappen-Zitat kennzeichnen mit Verweis „Umsetzung nach §1.2 (YLL × VOLY)" — der eigentliche Konflikt ist Befund 50.

### Befund 50 — VSL-Divergenz zwischen Bericht und verbindlicher Monetarisierungs-Arbeitsmappe ungelöst
- **Stelle:** §1.2 des Berichts vs. Arbeitsmappe: K1-Definition („Mortalität (VSL je Todesfall)"; „Kostensatz-Typ: VSL (Nutzer-Setzung 3,5 Mio. €/Todesfall)"), Annahme A1 („Wohlfahrtsperspektive, daher VSL 3,5 Mio. €"), Zeile 95 („hitzebedingte Übersterblichkeit × VSL (Nutzer-Setzung 3,5 Mio. €/Fall …)").
- **Art:** Widerspruch (Quelle-of-truth) — Kategorie **A**.
- **Begründung:** Der Bericht erklärt die Monetarisierungs-Arbeitsmappe zur verbindlichen Bewertungslogik und rechnet zugleich Mortalität als YLL × VOLY (160,8 T€) — die Arbeitsmappe schreibt an drei Stellen VSL 3,5 Mio. € fest. Rev. 2 hatte zugesagt, die Arbeitsmappe werde „nachgezogen"; das ist nicht geschehen. Zudem taucht der Arbeitsmappen-Wert 3,5 Mio. € in der Rev.-5-Sensitivitätsrechnung (4,7 / 6,19 Mio. €) gar nicht mehr auf. Eine verbindliche Quelle darf nicht stillschweigend überstimmt werden — dieselbe Governance-Mechanik wie in Befund 2/30.
- **Vorschlag:** Arbeitsmappe fortschreiben (K1-Definition und Kostensatz-Typ auf YLL × VOLY nach MK 4.0; A1 aktualisieren; VSL-Stützpunkte 3,5 / 4,7 / 6,19 Mio. € als benannte Sensitivitäten) und die Änderung als neuen Punkt ins Abgleich-Protokoll aufnehmen; im Bericht den Fortschreibungsverweis setzen. Bis dahin ist die Aussage „die Bewertungslogik folgt der Monetarisierungs-Arbeitsmappe" unzutreffend.

### Befund 51 — §1.2-Weitergaben-Tabelle #95 widerspricht der Quelle in drei Punkten; die #95→#101-Partitionsregel fehlt (ersetzt Befund 46)
- **Stelle:** §1.2, Tabelle „Explizit NICHT hier gebucht (R9)", Zeile #95.
- **Art:** Fehler + Lücke — Kategorie **A**.
- **Begründung:** (a) Die echten Output-Kanten von #95 sind → #87 (Abgleich P8) und → **#101** (Abgleich P47). #101 fehlt in der Tabelle vollständig — dabei buchen #95 **und** #101 beide K1-Mortalität/-Morbidität; genau dort entsteht die Doppelzählungsfrage. Die Arbeitsmappe enthält die Partitionsregel bereits ausformuliert: Zeile 101, Spalte „Nicht enthalten": „**Hitzetote (ID 95)**". Ohne dieses Zitat bleibt die Berichtsaussage „jeder Todesfall zählt genau einmal" unbelegt. (b) „Systemvorhaltung → #102" ist **keine** Kante von #95, sondern ein Konto-Ausschluss der K1-Definition („Systemvorhaltung (→K8 via ID 102)"); #102 hat als einzige Eingangskante #49 Hochwasser. (c) „Kühlkosten → #65" läuft laut Quelle über die R7-Weiche des Treibers #63 („100-%-Regel je Raumbestand: gekühlte Flächen buchen Kühl-Mehrkosten (K8, ID 65); ungekühlte Flächen buchen verbleibende K1-/K2-Schäden"), nicht als Weitergabe von #95.
- **Vorschlag:** Tabelle zweiteilen: Spalte „Output-Kanten (Abgleich-Protokoll)": #87 (P8, K2) · #101 (P47, K1 — mit Partitionszitat „Hitzetote sind bei #101 ausgeschlossen"); Spalte „Konto-Ausschlüsse / verwandte Buchungen": #102 (K1-Definition), #65 (über die #63-R7-Weiche). Kap.-2-Kopf bleibt unverändert (korrekt).

### Befund 52 — E09 „Trockenheit" ist Einfluss von W025, wird aber weder verarbeitet noch als bewusst inaktiv deklariert (#96)
- **Stelle:** Kap. 3, Wirkungskette und Formeln 96-A.
- **Art:** Lücke (Leitfrage 1: „nicht mehr, nicht weniger") — Kategorie **A**.
- **Begründung:** Laut Ketten-Sheet hat W025 „Pollenflug" **zwei** Einflüsse: E01 Durchschnittstemperatur **und E09 Trockenheit**. Der Bericht operationalisiert W025 ausschließlich über den Temperatur-/Phänologiepfad (GE-KL-07, Vegetationsperiode); der Trockenheitspfad (erhöhte Pollenfreisetzung und -transport an trockenen Tagen) rechnet nirgends und ist an keiner Stelle als bewusst inaktiv begründet — ein Knoten der verbindlichen Kette bleibt damit unadressiert.
- **Vorschlag:** In der Knoten-Bilanz (Befund 29) als „bewusst inaktiv" führen mit Begründung: kein belastbarer M0-ERF-Baustein; Wirkrichtung intensitätserhöhend — konsistent zur bereits dokumentierten, konservativen Nicht-Ansetzung der Intensitätszunahme (dokumentierte Untererfassung). Optional als Sensitivitätsband, sobald eine quantifizierte Trockenheits-Pollen-Beziehung belegt ist.

### Befund 53 — R7-Weiche für den S157-Hebel („gekühlte Räume") nicht referenziert
- **Stelle:** Kap. 2, Maßnahmen-Hebel S157; Quelle: Rechenregel R7 und Zeile 63 der Risiken-Monetarisierung; Zeile 95 führt R7 ausdrücklich als anzuwendende Regel für #95.
- **Art:** Lücke — Kategorie **B**.
- **Begründung:** Die Arbeitsmappe schreibt für gekühlte/ungekühlte Räume die 100-%-Aufteilung vor: gekühlte Flächen buchen Kühl-Mehrkosten (K8, #65), ungekühlte die verbleibenden K1-/K2-Schäden — nie beides je Einheit. Der Klimaanlagen-Hebel des Berichts (rOR ≈ 0,93) senkt K1-Schäden; ab Stufe M5 bucht #65 die Kühlkosten. Ohne R7-Verweis droht dann je Einheit die Doppelbuchung „vermiedener Schaden + Vorsorgekosten" — genau der Fall, den R7 verhindert.
- **Vorschlag:** Ein Satz am S157-Hebel: Wirkung nur auf den gekühlten Bestandsanteil, je Einheit Entweder-oder gemäß R7 (Verweis auf die #63-Weiche); im M5-Ausblick den Übergabepunkt an #65 benennen.

### Befund 54 — W124-Eingangsknoten nicht auf das Stadtmodell gemappt
- **Stelle:** §1.3 (Zelltemperatur/UHI).
- **Art:** Lücke (klein) — Kategorie **C**.
- **Begründung:** W124 hat laut Kette die Eingänge E02 **und E19 Sonnenscheindauer**, S094–S100, R23–R25 sowie W127 (Vegetation in Siedlungen). §1.3 beschreibt das Stadtmodell physikalisch (Albedo/Versiegelung, Gebäudemasse, Grün/Wasser/Baumkronen ≈ W127, SVF, Wind), mappt die Komponenten aber nicht auf diese Knoten; E19 ist nicht erkennbar abgebildet. Da W124 vorgelagert ist (0 € per R2) und produktseitig implementiert, kein M0-Blocker — aber die Knoten-Bilanz-Logik (Befund 29) sollte auch hier gelten.
- **Vorschlag:** Kleine Mapping-Tabelle „Stadtmodell-Komponente → W124-Knoten" in §1.3 oder Verweis auf die W124-Produktdokumentation; E19 als „implizit im DWD-Temperaturraster enthalten, nicht separat modelliert" deklarieren.

**AP-Zuordnung der neuen Befunde:** 50 → AP5 (plus Arbeitsmappen-Pflege + Abgleich-Protokoll-Eintrag) · 51 → AP12 (§1.2-Tabelle; ersetzt dort Befund 46) · 52 → AP7 / Knoten-Bilanz (AP11) · 53 → AP9 · 54 → AP11.

---

## Durchgang 4 — Abgleich docs/METHODIK_GRUNDSAETZE.md (Befunde 55–56 + Statusupdates)

Das Grundsatz-Dokument wurde am 22.08. nachgereicht; damit liegt die Prüfgrundlage erstmals vollständig vor.

### Abgleich — bestätigt (Entlastung)

- **G-Nummerierung konsistent:** Alle G-Referenzen des Berichts (G2, G3, G4/G9, G5/G11, G5/G12, G4/G10, G6, G8, G13, G14) treffen inhaltlich die richtigen Grundsätze des Dokuments ✓.
- **Die in Durchgang 1 nur indirekt prüfbaren 3.6-Anforderungen sind im Dokument spezifiziert:** G6 verlangt die Raten-Darstellung (je 1.000 EW / je ha + aggregierte Ebene) und G8 exakt die drei UI-Elemente (Benennung, Vollständigkeitsanzeige, Versionsstempel) — deckungsgleich mit T2.2-Kriterium 7 ✓. Zu liefern bleiben die Texte (AP11).
- **G9 kodifiziert die OR-Übersetzungsformel** wortgleich mit der in Durchgang 1 hergeleiteten Korrektur ✓; **G2** enthält das Konsistenzpaar 6,19 Mio. € ÷ 160,8 T€ ≈ 38 LJ ✓; die **Checkliste (1–10)** ist deckungsgleich mit Aufgabe §3 ✓.

### Befund 55 — Interner Widerspruch G1 ↔ G5: „ein einziger Skalar" vs. „Kalibrierfaktoren … regional differenzieren" — die Wurzel von Befund 2
- **Stelle:** METHODIK_GRUNDSAETZE.md, G1 („Bundes- oder Landesstatistik geht … als **ein einziger Skalar** auf die Deutschland-Summe ein") vs. G5 (nennt „Kalibrierfaktoren per Kleinste-Quadrate" in einer Reihe mit regional differenzierbaren Parametern: „Regional differenzieren, wo die Datenlage es trägt").
- **Art:** Widerspruch (im Grundsatz-Dokument selbst) — Kategorie **B**.
- **Begründung:** Genau diese Unschärfe hat die vier regionalen c_kal ermöglicht: Der Bericht beruft sich für den Regionalisierungs-Beschluss auf „G5/G12" — und kann das, weil G5 die Kalibrierfaktoren nicht von der Regionalisierungs-Erlaubnis ausnimmt, während G1 den einen Skalar fordert. Ein Grundsatz-Dokument, das beide Lesarten trägt, kann seine Governance-Funktion (Befund 2: keine stille Abweichung) nicht erfüllen.
- **Vorschlag:** G5 präzisieren (übernahmefertiger Text in T2.4): Regional differenziert werden **physikalische/gemessene Modellparameter** (Streuungen, Schwellen, Steigungen, Übersetzungsfaktoren); **Kalibrierfaktoren bleiben ein Niveau-Skalar je Modell (G1)**. Zeigt die G12-Prüfung regionale Schieflagen, wird die Wirkungsfunktion regional nachgeschätzt — nicht die Kalibrierung regionalisiert; regionale Kalibrierfaktoren höchstens als dokumentierte, befristete Übergangslösung mit Fortschreibungsvermerk.

### Befund 56 — G11-Begründung ist durch die eigene Rev.-5-Messung überholt
- **Stelle:** METHODIK_GRUNDSAETZE.md, G11 („Gauß unterschätzt rechte Schwänze **systematisch**").
- **Art:** Fehler (empirisch falsifizierte Begründung; die Regel selbst bleibt richtig) — Kategorie **C**.
- **Begründung:** Die Rev.-5-Herleitung (21 Stationen, 2.730 Wochen-Anomalien) hat gezeigt: Bei Sommer-**Wochenmitteln** ist die Verteilung praktisch symmetrisch (Schiefe −0,003…−0,089; Gauß- vs. empirische Quantile max. 0,12 K Differenz) — der maßgebliche Fehler der gesetzten Verteilung war die zu kleine Streuung (2,0 statt 2,36–2,58 K), nicht die Schiefe. Ein fortgeschriebenes Grundsatz-Dokument sollte keine vom eigenen Projekt widerlegte Pauschalbegründung enthalten.
- **Vorschlag:** Begründung aktualisieren (Text in T2.4): Regel unverändert (empirische Quantile, intra-saisonal), weil sie Streuungs- **und** Formfehler zugleich vermeidet; Schiefe-Hinweis auf Tages-/Ereignisgrößen beschränken, den Wochenmittel-Befund als Beleg zitieren.

**AP-Zuordnung:** 55 → AP1 (Governance-Seite von Befund 2; Fortschreibung parallel zum Kalibrierlauf) · 56 → AP12. Statusupdates: **31 geschlossen** · **30 verschärft** (Fortschreibungstext liegt bei) · Abnahmekriterium 8 erweitert um die Grundsatz-Dokument-Synchronität.

---

## Priorisierung für die verbleibenden Tage bis 28.08. (final, Stand Durchgang 4)

| Reihenfolge | Befunde | Warum zuerst |
|---|---|---|
| 1 | 2 + 3 + 1, dann 47; parallel **55** (G1/G5-Fortschreibung, Textbaustein liegt bei) | ERF-Regionen/Kalibrierung sind das Fundament — jede spätere Zahl hängt daran; Rechenläufe brauchen Vorlauf |
| 2 | 32 (mit 20), 4, 11, 35, 10, 50 | G14-Verstöße an Kernparametern + Quelle-of-truth: f_a-Rückrechnung, r_0,a, #96-Klimasignal, #96-Altersbänder, VOLY-Band, Arbeitsmappen-Fortschreibung VSL→YLL×VOLY |
| 3 | 5–9, 44, 12–17, 33, 36–38, 51, 52 | Formel-/Herleitungs-/Kettenkorrekturen, jeweils Stunden-Aufwand |
| 4 | 18 (Zitate liegen bei), 19, 21–25, 34, 39–41, 53 | Validierung, Quellen, Preisstände, Szenario-/Maßnahmen-Spezifikation, R7-Verweis |
| 5 | 26–30, 42–43, 45, 48–49, 54, **56** | Redaktion, Kennzeichnungen, Grundsatz-Textpflege (31 geschlossen, 46 ersetzt durch 51) |

---
---

# Teil 2 — Übergabepaket für das Methodik-Team

Dieser Teil macht die Befundliste (Teil 1) abarbeitbar: Arbeitspakete mit konkreten Deliverables in der PDF, Abnahmekriterien, die Abdeckungsmatrix gegen die Aufgabenstellung, übernahmefertige Bausteine (Zahlenwerte, Zitate, Textentwürfe) und das Rückmeldeformat. Ziel: Nach Abarbeitung bildet die PDF die Methodik vollständig im Sinne von AUFGABE_METHODIK_SCHADENSRECHNUNG.md §2 und §3 ab und besteht die Leitfragen 1–13 ohne Rückfragen.

## T2.1 Arbeitspakete (Befunde gebündelt, mit Deliverable in der PDF)

| AP | Befunde | Deliverable in der PDF (Rev. 6) | Abhängigkeit / Aufwand |
|---|---|---|---|
| **AP1 Kalibrierung neu** | 1, 2, 3, 19, 21, 24, 47 | §2(c) vollständig neu: 4-Regionen-ERF (T₀/β je RKI-Region, Quelle EB 19/2025 bzw. Nachschätzung dokumentiert), Kalibrierlauf mit dem **Zellmodell**, einheitlicher Signifikanzfilter, Fenster-Sensitivität je Region, zeitlicher Holdout (Fit 1992–2015 / Prüfung 2016–2024), Regionszuordnungstabelle Bundesland→Region und Zelle→Region, aktualisierte CSVs als Anlage | zuerst starten — alle €-Werte hängen daran; 1–2 Tage Rechen-/Doku-Arbeit |
| **AP2 Altersschichtung Mortalität** | 32, 22, 20 | Rechenkette f_a (Formel, RKI-Anteile, Zwischenwerte, Ergebnis mit neuen m_a), L̄_a mit Sterbefallgewichten neu, Ist-Ergebnis der Altersverteilungs-Validierung als Tabelle (Modell vs. RKI 6,5/12,9/25,2/55,5 %) | nach AP1-Lauf (gleicher Batch); 0,5 Tag |
| **AP3 Modifikatoren v_vers,a** | 7, 8, 9, 17, 25, 44 | Tabelle „Faktor × Altersband × q̄_a" (β_d: alle Bänder; β_iso: 65+; β_pfl: 75–84/85+ mit bandspezifischen Pflegequoten); Rechenketten für 1,32-Schritt und Bouchama-Adjustierung; F-Pfad nur β_iso; Zahlenwerte für d̄_KH, q̄_1P (Zensus exakt), q̄_pfl,a; Datenverfügbarkeits-Ergebnis q_1P×65+ / OSM-Heime mit Fallback-Definition | unabhängig; 0,5–1 Tag |
| **AP4 Morbidität #95** | 4, 5, 6, 38, 42 | r_0,a konsistent (Option A oder B aus T2.4) mit GENESIS-Quelle; e_HD-Basiswahl begründet (Empfehlung: konditional 0,024, Band bis 0,054); HD_ref = 7,2 d mit Ein-Satz-Herleitung; UHI→hot_days-Umrechnungsregel mit Zellbeispiel; c_Fall als Proxy gekennzeichnet | unabhängig; 0,5 Tag |
| **AP5 Monetarisierung** | 10, 23 | VOLY-Band korrigiert (T2.4) und Preisstand-Label €2024 bzw. Fortschreibung; alle Kostensätze auf gemeinsamen Preisstand €2025 mit VPI-Faktoren in den Zeichentabellen | unabhängig; 2–3 h |
| **AP6 #96 Klimasignal** | 11, 39 (Teil) | S_ref-Definition, ΔBlühbeginn/ΔSaisonende je Region aus DWD-Phänologie-CDC, Ergebnis-CSV + Skriptpfad (analog wochenquantile_region.csv), Szenario-Absatz (GE-KL-07-Projektion) | kritischster #96-Pfad; 1 Tag |
| **AP7 #96 Formeln & Daten** | 12, 13, 14, 35, 36, 49 | P̂_Zelle in beide Formeln; c_Jahr mit direktem Anteil + Inflationsfaktor als Zahlen; d_Saison-Kette repariert (f aus Symptomlast-Daten [53] oder als Annahme; p_G/p_B mit Umrechnung; Überlappungskorrektur); u18-Ebene als „neu anzulegen" gekennzeichnet mit Bandzuordnung; Sanity-Untergrenze oder begründete Ausnahme | nach AP6; 1 Tag |
| **AP8 #98** | 15, 16, 37, 17 (q_out), 41, 43 | Attributionsfaktor a_attr,UV mit Band und Begründung; k_UV = 0,43 mit Fundstelle; SSD-Fenster als Normalperioden je Zelle; q_out-Datenquelle (BA-Beschäftigtenstatistik je Kreis, als Proxy) + q̄_out; Entitäten-Split-Annahme gekennzeichnet; λ_e/L̄_e-Approximationen gekennzeichnet | unabhängig; 0,5–1 Tag |
| **AP9 Maßnahmen & Quellen** | 33, 34, 18 | δ_HAP definiert als Faktor auf (RR−1); Stadtbaumwahl als modellendogener Hebel über ΔĜ→λ formalisiert; UV-Schutz ehrlich als qualitativ oder mit Verhaltens-/Dosisevidenz; Vollzitate [45]–[47] + Belgien-Studie übernehmen (T2.4), Wayback-Snapshots | unabhängig; 0,5 Tag |
| **AP10 Szenario-Absätze** | 39 | Je empfohlenem Ansatz ein Absatz „Szenario-Anwendung" (verschobene Größe, konstante Größen, Stationaritätsannahmen) — oder explizite Aussage, ab welcher Stufe Szenariofähigkeit kommt | nach AP1/AP6; 2 h |
| **AP11 Architektur/UI** | 28, 29, 40 (Doku-Teil) | Deklaration der nativen Ergebnisgröße je Risiko; Knoten-Bilanz-Tabelle je Risiko (Template T2.4); Absatz zur Modellgrenze „mittleres Jahr" mit Zuschreibung der 2006/2015-Residuen (optional: q-T̄-Kopplung als Sensitivität); Infokasten-Texte (Entwürfe T2.5) | unabhängig; 0,5 Tag |
| **AP12 Redaktion & Anlagen** | 26, 27, 30, 31, 45, 46, 48 | Kopfzeilen Kap. 2/4 (VSL→Verweis §1.2), Kap.-5-Text (1,44 raus), v_access-Reste, #101/#102 geklärt, G14-Scope einvernehmlich in Aufgabe/Grundsätze festgehalten, Anlagenpaket (Skripte/CSVs) beigelegt | zum Schluss, ein Durchgang; 2–3 h |

## T2.2 Abnahmekriterien (Definition of Done für Rev. 6)

Der Bericht gilt als „rund", wenn alle sieben Kriterien erfüllt sind. Kriterien 2, 3 und 6 sind **Prüfsteine mit offenem Ausgang** — sie können auch scheitern; dann gilt die Eskalationsregel.

1. **Befund-Abdeckung:** Alle A-Befunde geschlossen; B-Befunde geschlossen oder mit begründeter Zurückstellung im Rückmeldeformat (T2.7); C-Befunde umgesetzt.
2. **Kalibrier-Prüfstein (AP1):** Kalibrierlauf mit dem Produktionsmodell (Zellmodell) und 4-Regionen-ERF: ≥ 11 von 16 Ländern im Band 0,75–1,35 **ohne** zusätzliche Sonderfaktoren; verbleibende Ausreißer physikalisch erklärt; Holdout-Prüfung dokumentiert. *Eskalation bei Scheitern:* nicht nachkalibrieren, sondern Modellentscheid (ERF-Form/Regionen) zurück in die Methodikrunde.
3. **Alters-Prüfstein (AP2):** Modellierte Bandanteile innerhalb ±5 Prozentpunkte je Band gegenüber der RKI-Verteilung (Toleranz vor dem Lauf fixieren, nicht danach). *Eskalation:* f_a-/Schichtungslogik überarbeiten, nicht die Toleranz.
4. **G14-Check:** Für jedes Formelzeichen jeder Zeichentabelle der empfohlenen Ansätze referenziert „Wert/Herkunft" eine abgeschlossene Herleitung im Bericht — kein „wird ergänzt", kein Wert ohne Rechenweg. (Stichprobe der Gegenprüfung wird wiederholt.)
5. **Quellen-Check:** [45]–[47] im Volltext verifiziert (Zahlen gegengelesen) mit Wayback-Permalink; neue Quellen (Belgien-Studie) vollständig; [38]–[43] gemäß bestehender Ratchet-Zusage.
6. **Sanity-Bänder:** Je Risiko Unter- **und** Obergrenze aus amtlicher Statistik, oder begründete dokumentierte Ausnahme (#96). Bundessummen der drei Modelle liegen in ihren Bändern.
7. **UI/G8-Texte:** Die drei Pflicht-Infokästen (T2.5), die Benennung „bewerteter Schaden — Konto K1", Vollständigkeitsanzeige und Versionsstempel stehen als Texte im Bericht (nicht nur als Absichtserklärung).
8. **Quellen-Synchronität (erweitert, Durchgang 3+4):** Bericht, Quell-Arbeitsmappen **und Grundsatz-Dokument** widersprechen sich in keinem verbindlichen Punkt. Jede bewusste Fortschreibung (insbesondere VSL → YLL × VOLY, Befund 50) ist in der Monetarisierungs-Arbeitsmappe nachgezogen **und** als Punkt im Abgleich-Protokoll dokumentiert; die §1.2-Weitergaben unterscheiden Output-Kanten und Konto-Ausschlüsse quellgetreu (Befund 51); jeder Ketten-Knoten der drei Risiken rechnet oder ist in der Knoten-Bilanz als bewusst inaktiv begründet (Befunde 29, 52, 54); in METHODIK_GRUNDSAETZE.md sind die G1/G5-Präzisierung, der G14-Geltungsbereich und die G11-Begründung fortgeschrieben (Befunde 55, 30, 56 — Textbausteine in T2.4).

## T2.3 Abdeckungsmatrix gegen die Aufgabenstellung

**Aufgabe §2 (Aufgabenumfang):**

| Anforderung | Status Rev. 5 | Offen über Befunde |
|---|---|---|
| 2.1 Wirkungskette strikt aus Arbeitsmappe + R9-Abgrenzung | ✅ im Kern | 29 (Knoten-Bilanz), 46 (#101/#102) |
| 2.2 Schicht-A-Index aus den Knoten | ✅ | 29 (inaktive Knoten deklarieren) |
| 2.3 Schicht-B als Menge × Rate × Preis, vollständig | ✅ Struktur | 12 (Proportionalität #96), 35 (u18), 6/38 (fehlende Regeln) |
| 2.4 Kalibrierung der Absolutwerte | 🔧 | 1–3, 19–21, 24, 47 (AP1/AP2) |
| 2.5 Drei Ansätze + Kriterienraster + Empfehlung | ✅ | 27 (Text veraltet), 30 (G14-Scope) |
| 2.6 Maßnahmen mit Effektgrößen belegt | 🔧 teilweise | 18, 33, 34 (AP9) |
| 2.7 Ohne Rückfragen prüfbar | 🔧 teilweise | 31, 48 (Anlagen), plus alle Reproduzierbarkeits-Befunde (9, 10, 32) |

**Aufgabe §3 (Anforderungskatalog):**

| Abschnitt | Status | Offene Befunde |
|---|---|---|
| 3.1 Eingangsgrößen (Quelle, Auflösung, Kennzeichnung, Proxies) | ✅ überwiegend | 17, 25, 35, 42 |
| 3.2 Verrechnung (Formeln, bottom-up, physische Größe, Alter, YLL, belegte Sensitivitäten, Zentrierung, OR-Übersetzung, Doppelkanäle, Tails, messen statt setzen, Zeitbezug) | ✅ in den Grundzügen — die Stärken von Rev. 5 liegen hier | 4–9, 12–14, 22, 32, 36–40, 44 |
| 3.3 Konten-Disziplin | ✅ | 10, 23 (Preisstände), 26, 46 (redaktionell) |
| 3.4 Kalibrierung/Validierung (ein Skalar, Revisionsstand, unabhängige Prüfung, Sanity-Bänder) | 🔧 | 1–3, 19, 20, 21, 24, 47, 49 |
| 3.5 Maßnahmen (Interventionsevidenz, marginal, Doppelzählungs-Wächter) | ✅ Prinzip umgesetzt | 18, 33, 34 |
| 3.6 Architektur/Produkt (Screening-Trennung, eine native Größe, Kartenebenen/Raten, UI, Ratchet) | ✅ soweit im Bericht prüfbar | 28, 29, 31 |
| 3.7 Vergleich der drei Ansätze | ✅ | 27 |
| 3.8 Quellen (Vollzitate, Verifikation, Widersprüche, Lücken) | 🔧 teilweise | 18 (übernahmefertig gelöst), 9, 16 |
| 3.9 Herleitungspflicht ohne Ausnahme | 🔧 — größter Restposten | 4, 6, 10, 11, 13, 16, 17, 32, 37, 38 (+ 30 Scope-Klärung) |

**Leitfragen 1–13 → Befunde:** LF1 → 29 · LF2 → bestanden · LF3 → 12 · LF4 → 6 (HD_ref-Doppelzählung), bestanden bei Grün/UHI und R9 · LF5 → bestanden (β_iso, r_out), offen 7/8/44 (Bandzuordnung) · LF6 → 32, 35, 41, 44 · LF7 → bestanden (Quantile), offen 40 · LF8 → 1–3, 19, 20, 24 · LF9 → 10, 23, 42 · LF10 → 9 (Klenk-Zuordnung), 16, 18 · LF11 → 4, 10 (nicht aufgehende Rechnungen), 45/46 (Zeichen-Konsistenz) · LF12 → 17, 25, 35, 37 · LF13 → siehe 3.9.

## T2.4 Übernahmefertige Bausteine

**Zahlenwerte / Korrekturen (geprüft, direkt einsetzbar):**

- **β_iso = 0,86** (Band ≈ 0,3–1,4): bereits korrekt in Rev. 5 — keine Änderung, nur zur Bestätigung.
- **k_UV = 0,43** (= 4,9 %/Dekade ÷ 11,3 %/Dekade), Band 0,40–0,50; Fundstelle der 11,3 %/Dekade in Lorenz 2024 ergänzen (Befund 16).
- **HD_ref = 7,2 Tage/Jahr** (Basisperiode der K&Z-Baseline 1999–2008; verhindert Doppelzählung des Durchschnittseffekts in r_0).
- **VOLY-Band:** Untergrenze 136,4 T€ ✓; Obergrenze je nach Definition **165,6 T€** (Raumtransfer ohne Elastizität, Einkommen mit 0,85) oder **170,3 T€** (beide ohne Elastizität) — der bisherige Wert 169,5 T€ reproduziert mit keiner Lesart. Preisstand-Label: €2024 (VPI- und BIP-Endpunkte 2024) oder mit VPI 2024→2025 fortschreiben.
- **r_0,a — zwei konsistente Optionen:** (A) Raten 1,9 / 6,3 / 10,8 / 15,6 behalten und den Verhältnistext auf „≈ 1 : 3,3 : 5,7 : 8,2" korrigieren, oder (B) Verhältnis 1 : 5 : 8 : 10 behalten → Raten 1,53 / 7,63 / 12,21 / 15,26 (Normierung auf Bundessumme 3,5/100.000 gezeigt). In beiden Fällen: Quelle für das Altersprofil (GENESIS 23131 / GBE, Kreislauf-Einweisungsraten je Altersgruppe) mit Zahlen zitieren.
- **c_kal-Sensitivität:** Fenster ÷ Vollreihe = 0,890/1,027 = **−13,3 %** — als bezifferter Satz in §2(c).
- **δ_HAP:** definiert als multiplikativer Faktor auf den Wochen-Exzess (RR − 1); zentral 0,95, Band 0,85–1,00 (Nachrechnung: Anwendung auf β wiche je nach Wochenhitze um bis zu 0,7 %-Punkte ab — deshalb Ergebnisebene, konsistent zur Studienart).

**Vollzitate zur Übernahme in Kap. 6 (verifiziert):**

- **[45]** H. Feldbusch, A. Schneider, F. Matthies-Wiesler, A. Matzarakis, A. Peters, S. Breitner-Busch, V. Huber, „Assessing the effectiveness of the heat health warning system in preventing mortality in 15 German cities: A difference-in-differences approach", *Environment International* 203:109746, 2025. doi:10.1016/j.envint.2025.109746 (Open Access, CC BY; Daten 1993–2020; RR gepoolt 1,00 [0,98–1,01], mit Meta-Variablen 0,85 [0,75–0,97] — gegengelesen ✓).
- **[46]** G. M. Katz, K. A. Brown, V. Giannakeas, N. M. Stall, „Air Conditioning in Nursing Homes and Mortality During Extreme Heat", *JAMA Internal Medicine* 186(2):243–251, 2026 (online 15.12.2025). doi:10.1001/jamainternmed.2025.6595 (Open Access; 73.578 Todesfälle 2010–2023; rOR 0,93 — gegengelesen ✓).
- **[47]** „The effectiveness of heat prevention plans in reducing heat-related mortality across Europe", *Environmental Research Letters*, 2025. doi:10.1088/1748-9326/ae2775 (Open Access; 102 Standorte, 14 Länder, 1990–2019; Autorenliste beim Wayback-Snapshot vom Artikel übernehmen).
- **[neu]** „Impact of Heat Waves on Hospitalisation and Mortality in Nursing Homes: A Case-Crossover Study", *Int J Environ Res Public Health* 18(20):10697, 2021. doi:10.3390/ijerph182010697 (Flandern, 10 Heime 2013–2017; Mortalität OR 1,61 [1,10–2,37], Hospitalisierung OR 0,96 [0,67–1,36] n. s. — Beleg für Befund 7: β_pfl nicht im F-Pfad).

**Tabellen-Skelett v_vers,a (Befunde 7/8/44, AP3):**

| Faktor | Evidenz | wirkt auf Bänder | wirkt auf | q̄ / d̄ (Herleitung nachtragen) |
|---|---|---|---|---|
| β_d = 0,001/km | Nicholl 2007 (Mortalität, transportierte Notfälle) | alle | nur D_a | d̄_KH = ⟨aus HEALTHCARE_ACCESS, bevölkerungsgewichtet⟩ |
| β_iso = 0,86 | Semenza 1996 (Ältere) | 65–74 / 75–84 / 85+ | D_a und F | q̄_1P = ⟨Zensus 2022 exakt⟩ |
| β_pfl = ⟨je Band⟩ | Fouillet 2006 / Bouchama 2007 / Katz 2026 | 75–84 / 85+ | nur D_a | q̄_pfl,a = ⟨Pflegestatistik je Band⟩ |

**Template Knoten-Bilanz (Befund 29, je Risiko eine Tabelle):**

| Knoten | rechnet in | Wo (Formel/Ebene) | falls inaktiv: Begründung |
|---|---|---|---|
| z. B. R36 (#96) | bewusst inaktiv | — | Handlungsfeld-Vererbung (dokumentierte KWRA-Unschärfe §1.1); kein risikospezifischer Wirkmechanismus belegt |

**Fortschreibungstexte für die Grundsatz-Dokumente (Durchgang 4, übernahmefertig):**

- **G5-Ergänzung (Befund 55, löst die G1↔G5-Spannung):** „Abgrenzung zu G1: Regional differenziert werden physikalische bzw. gemessene *Modellparameter* (Streuungen, Schwellen, Steigungen, Übersetzungsfaktoren). *Kalibrierfaktoren* bleiben ein einziger Niveau-Skalar je Modell (G1). Zeigt die Verteilungsprüfung (G12) regionale Schieflagen, ist die *Wirkungsfunktion* regional nachzuschätzen — nicht die Kalibrierung zu regionalisieren. Regionale Kalibrierfaktoren sind allenfalls eine dokumentierte, befristete Übergangslösung mit Fortschreibungsvermerk und Ablaufdatum."
- **G14-Ergänzung (Befund 30):** „Geltungsbereich: Die Herleitungspflicht gilt vollständig für jeden Ansatz, der Umsetzungsgrundlage ist. Dokumentierte Alternativen und ausgeschiedene Negativ-Beispiele werden bis zur Quelle geführt; wird eine Alternative später Umsetzungsgrundlage, gilt G14 vor der Implementierung vollständig." (Denselben Satz in Aufgabe §3.9 spiegeln.)
- **G11-Begründung aktualisieren (Befund 56):** „Empirischer Stand (Rev. 5, 21 DWD-Stationen, 2.730 Wochen-Anomalien): Bei Sommer-Wochenmitteln ist die Anomalieverteilung praktisch symmetrisch; der maßgebliche Fehler gesetzter Verteilungen lag in der zu kleinen Streuung (2,0 statt 2,36–2,58 K), nicht in der Schiefe. Die Regel bleibt unverändert — empirische Quantile vermeiden Streuungs- und Formfehler zugleich; bei Tages- und Ereignisgrößen bleibt die Rechtsschiefe relevant."
- **Monetarisierungs-Arbeitsmappe (Befund 50):** K1-Definition und Kostensatz-Typ auf „YLL × VOLY nach MK 4.0 (VOLY ⟨Wert nach Befund 10⟩; VSL-Stützpunkte 3,5 / 4,7 / 6,19 Mio. € als Sensitivitäten)" umstellen; Annahme A1 entsprechend anpassen; neuer Abgleich-Protokoll-Punkt „K1-Mortalitätsbewertung VSL → YLL×VOLY (Review 2 / MK 4.0)".

## T2.5 Entwürfe der Pflicht-Infokästen (G8 — produktreif formulieren, hier als Startfassung)

**Infokasten 1 — am Gesamtwert: „Was dieser Betrag enthält — und was nicht."**
„Dieser Wert ist der *bewertete Schaden im Konto K1 Gesundheit* (Modellstand M0). Er umfasst Behandlungskosten und den Wert verlorener Lebensjahre — nicht enthalten sind u. a. Arbeitsproduktivität (folgt in Stufe M3), Sach- und Infrastrukturschäden sowie Vorsorgekosten (spätere Stufen). Der ausgewiesene Betrag ist deshalb eine bewusste **Untergrenze**; er wird mit jeder Ausbaustufe vollständiger — nie kleiner. Berechnet mit Modellstand M0, Stand ⟨Datum⟩."

**Infokasten 2 — am Mortalitäts-Kostensatz: „Warum verlorene Lebensjahre statt Todesfälle × Kopfpauschale?"**
„Sterblichkeit bewerten wir nach der UBA-Methodenkonvention 4.0: verlorene Lebensjahre × Wert eines Lebensjahres (⟨VOLY⟩ €). Das bewertet altersgerecht — ein Sterbefall mit 6 verbleibenden Lebensjahren zählt anders als einer mit 40 — und fällt deutlich vorsichtiger aus als der pauschale ‚Wert eines statistischen Lebens' (Faktor ≈ 5 bei Hitze). Die Vergleichsrechnung mit dem Pauschalwert weisen wir als Sensitivität aus."

**Infokasten 3 — bei #98: „Eingelaufenes Risiko und Latenz."**
„Hautkrebs entsteht mit Jahrzehnten Verzögerung. Der hier ausgewiesene klimabedingte Zusatz beschreibt das *eingelaufene Risiko der heutigen Strahlungslage*, nicht die Fälle eines einzelnen Jahres. Der wichtigste Treiber neben der Strahlung — verändertes Freizeitverhalten in längeren Warmphasen — ist wissenschaftlich nicht belastbar beziffert und daher **nicht** eingerechnet: Auch dieser Wert ist eine Untergrenze."

## T2.6 Verbleibende dokumentierte Grenzen (nach vollständiger Abarbeitung — für Entscheidungsbogen und Unsicherheits-Kapitel)

Diese Punkte sind nach Rev. 6 keine Mängel, sondern erklärte Modellgrenzen; sie gehören in den Entscheidungsbogen, damit die Abnahme sie mitträgt:

1. **#95 Skalentransfer:** Die ERF ist auf Regions-Gebietsmitteln geschätzt und wird auf Zelltemperaturen angewendet; c_kal fängt das Niveau, nicht die Form.
2. **#95 ERF-Zeittrend:** Anpassungssignal 2021–2025 nicht modelliert; Wahl Vollreihe vs. Fenster bleibt eine Setzung mit ±13 % Wirkung (Sensitivität ausgewiesen).
3. **#95 Jahresvariabilität:** Quantile bilden das mittlere Jahr ab; Hitzewellen-Jahre mit moderatem Sommermittel werden strukturell unterschätzt (2006/2015-Residuen).
4. **#96 d_Saison:** bleibt auch nach Reparatur eine Schätzkette ohne direkten Messwert; Pollen-Hazard je Zelle bleibt Proxy (kein flächiges Messnetz).
5. **#98 Verhaltenspfad:** Der von der KWRA benannte Hauptpfad ist unquantifiziert; das Modell rechnet nur den Dosispfad → strukturelle Untergrenze; Latenz macht die Jahres-Attribution konzeptionell unscharf.
6. **Übergreifend:** M0 = K1-only-Untergrenze mit asymmetrischer Unsicherheit nach oben; UHI-Modellgüte als gemeinsamer Treiber von #95-Feinstruktur.

## T2.7 Rückmeldeformat je Befund

Bitte je Befund eine Zeile zurückmelden; die Gegenprüfung der Rev. 6 prüft dann gegen diese Tabelle plus die Abnahmekriterien T2.2:

| Befund | Status (übernommen / abweichend gelöst / zurückgestellt) | Umsetzungsnachweis (Kapitel/Formel/Anlage in Rev. 6) | Begründung bei Abweichung oder Zurückstellung |
|---|---|---|---|
| 1 | | | |
| … | | | |

**Zwei Regeln dazu:** (1) „Abweichend gelöst" ist zulässig, wenn die Lösung die zugrunde liegende Anforderung anders erfüllt — die Anforderung selbst darf nur über eine Fortschreibung von docs/METHODIK_GRUNDSAETZE.md bzw. der Aufgabenbeschreibung geändert werden (Mechanik aus Befund 2/30: begründete, dokumentierte Ausnahme statt stiller Abweichung). (2) Zurückstellungen von A-Befunden blockieren die Abnahme; Zurückstellungen von B/C-Befunden brauchen einen Zieltermin.
