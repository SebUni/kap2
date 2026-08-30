# Gegenprüfung Rev. 5 — Befundliste mit Bewertung

Stand 22.08.2026 · Prüfgrundlage: `AUFGABE_METHODIK_SCHADENSRECHNUNG.md` (13 Leitfragen) · Prüfobjekt: `METHODIK_M0_GESUNDHEIT.pdf` Rev. 5
Prüfer: unabhängiger Agent (nur PDF-Text, HTML-Formeln, Kalibrierdateien, Aufgabenbeschreibung — kein Entwicklungs-Kontext).
Darunter die Bewertung der Befunde durch den Autor (nachgerechnet / bestätigt / eingeschränkt).

## Bewertung durch den Autor

**Bestätigte Fehler (Rev. 6 zwingend):**
- **#2 Morbiditätsformel 95-A** — korrekt erkannt und gravierend: Die relative Elastizität 5,4 % bezieht sich bei K&Z auf *alle* Einweisungen (Basis ≈ 57.000/100.000·Jahr), wurde aber auf die hitzespezifische Baseline r₀ ≈ 3,5/100.000 angewandt ⇒ ein Hitzetag liefert 0,19 statt 3,1 Fälle je 100.000 (Faktor 8–16 zu niedrig). Fix: absolute Elastizität 3,106 Einweisungen/100.000 je Hitzetag (konditional 1,408) direkt als Zusatzterm; HD_ref als bevölkerungsgewichtetes Bundesmittel der Referenzperiode herleiten.
- **#1/#11 €-Pfad 96-A** — bestätigt: € muss aus der ausgewiesenen physischen Größe (ΔTage) × Tageskostensatz folgen, beide Formeln müssen dieselben Faktoren (P̂) tragen, und S_ref ist nicht beziffert (ΔS/S_ref 0,15–0,25 vs. d_Saison-Saisonlängen 90 Tage ⇒ 0,4–0,5 inkonsistent). Fix: S_ref als Patienten-Saison (Birke+Gräser ≈ 90 Tage) setzen, ΔS aus Phänologie-Verfrühung nur der relevanten Taxa, c_Tag = c_Jahr/d_Saison.
- **#3 v_vers bandübergreifend** — bestätigt: β_pfl/β_iso sind mit 85+- bzw. 65+-Mitteln zentriert und dürfen nur auf diese Bänder wirken; auf F (Einweisungen) ist keiner der drei Effekte belegt ⇒ Default 1.
- **#4 zirkuläre Altersvalidierung** — bestätigt: f_a aus der RKI-Altersverteilung ⇒ Prüfung gegen dieselbe Verteilung ist keine Validierung. Fix: Rückrechnungskette zeigen, unabhängig gegen Berlin/Hessen 2018 (85+-Raten 260–320/100.000) prüfen.
- **#6 VOLY-Obergrenze** — nachgerechnet: 79.500 × 1,4638 × 1,2140 × 1,1719 = 165,6 T€ (nicht 169,5; der Wert stammte aus einer Variante mit Preisstand 2025). Korrektur.
- **#7 r₀,ₐ-Verhältnis** — bestätigt: 1:5:8:10 ≠ 1,9/6,3/10,8/15,6 (= 1:3,3:5,7:8,2); Altersaufteilung muss aus GENESIS 23131-0002 (Gastzugang prüfen) kommen, sonst konsistent und als Abschätzung gekennzeichnet.
- **#8 β_pfl-Kette** — bestätigt: Exzess-Faktor 1,32 und Verhältnis 2,85 sind aus den genannten O/E-Werten nicht reproduzierbar; Kette neu und Schritt für Schritt aufbauen (Heimrate, Nicht-Heim-Rate aus m_85+ und q̄ exakt).
- **#13–#16, #20, #21** — reine Konsistenzfehler (veralteter 1,44-Satz, „Normalverteilungs-Quantile" in (a), „× VSL" in den Ketten-Kästen, #101/#102, M5, Fußzeile 18.08., 2026 im κ-Fit, 84.600 €): alle korrigieren.

**Bestätigt mit Entscheidungsbedarf:**
- **#9 Außenberufs-Anteil (#98)** — der Prüfer hat recht, dass W186 diesen Knoten nicht enthält. Konflikt zwischen §1.1 („nur Excel-Knoten") und G4 (Review 3: empirisch belegte Sensitivitäten ergänzen). Vorschlag: Außenberuf als dokumentierte Erweiterung über S154 (Expositionsverhalten) führen **oder** streichen — Entscheidung des Auftraggebers; bis dahin aus dem Basiswert nehmen.
- **#17 regionale c_kal vs. G1** — sachlich richtig benannt: Vier Faktoren aus Landesstatistik sind eine kontrollierte Abweichung vom „ein Skalar"-Grundsatz (begründet durch den RKI-Regionenzuschnitt). Rev. 6 muss das als Grundsatzabweichung ausweisen, die Bundesland→Region-Zuordnung abdrucken und den Süd-Faktor 1,74 diskutieren (BW/BY-Kontrast, Oberrheingraben).
- **#5 „konservativ"** — richtig: Der höhere Faktor ist der höhere Schaden; Wortwahl und Wahl des Kalibrierfensters (Vollreihe vs. 2012+) neu begründen; Jensen-Lücke (Mittelsommer + intra-saisonale Streuung ≠ Erwartungswert über Jahre) quantifizieren (#28).
- **#10 k_UV** — die „+11,3 %/Dekade Dortmund" stammt aus der Sekundärzusammenfassung der Lorenz-2024-Studie; gegen den Volltext verifizieren, Default setzen.
- **#12 Altersbänder 85+ aus Zensus-Gitter** — prüfen, ob `pop_age_bands` auf 100 m die 85+-Klasse trägt; wenn nur „80+", Split-Quoten aus Kreisdaten herleiten und als Abweichung dokumentieren.

**Lücken (Rev. 6 abzuarbeiten):** #23/#24 (Zentrierungsmittel q̄_1P, d̄_KH, Ḡ, HD_ref beziffern; „[38–43] werden verifiziert" durch verifizierte Fundstellen ersetzen; [45]–[47] Autoren/DOI), #25 (Validierungsergebnisse tatsächlich berichten: Altersanteile, Morbiditäts-Bundessumme, J30/KKR-Sanity), #26 (Maßnahmen-Effektgrößen beziffern), #27 (#96 altersspezifische Prävalenzen aus DEGS1), #28 (Bezugsperioden/Szenarioeingang definieren), #29 (S154/R36-Knoten: entweder verrechnen oder begründet als nicht-quantifizierbar markieren), #30 (G6/G8 als Spezifikation), #31 (YLL-Obergrenze, Band), #32 (alle Hilfsgrößen in Zeichentabellen; Kriterien K1–K6 umbenennen, z. B. P1–P6), #33 (Datenverfügbarkeit Alter × Haushaltsgröße auf 100 m klären).

**Nicht geteilt / eingeschränkt:** #22 (G14 nur für Ansatz A) ist eine bewusst dokumentierte Scope-Entscheidung — bleibt, wird aber in §2 der Aufgabenbeschreibung als Präzisierung nachgezogen. #19 (Entitätenzahlen 2015 > 2023) ist ein echter Quellenwiderspruch (BfS-Schätzung 2015 vs. ZfKD-Registerdaten 2023 mit anderer Zählweise) und wird benannt, nicht „korrigiert".

---

# Gegenprüfung METHODIK_M0_GESUNDHEIT.pdf — Revision 5 (Stand 22.08.2026)

Prüfgrundlage: AUFGABE_METHODIK_SCHADENSRECHNUNG.md (Abschn. 2, 3.1–3.9, 4 / Leitfragen 1–13), METHODIK_GRUNDSAETZE.md (G1–G14).
Geprüft: PDF-Volltext (pdftotext), LaTeX-Formeln und Zeichentabellen aus docs/render/METHODIK_M0_GESUNDHEIT.html, Kalibrierdateien in backend/data/kalibrierung/ (Skripte in backend/scripts/kalibrierung/ vorhanden).

Vorab — was nachgerechnet wurde und stimmt: β_iso = 1,3/(1+0,40·1,3) = 0,855 ≈ 0,86 ✓ · β_pfl = 2,5/(1+0,149·2,5) = 1,82 ✓, Wirkung 0,73 / 1,27 ✓ · q̄_pfl = 424.300/2.844.213 = 0,149 ✓ · VOLY-Kette 79.500 × 1,4638 × 1,1792 × 1,1719 = 160.815 ✓, Einzelfaktoren (VPI 119,3/81,5; KKS 26.837/22.106 = 1,2140^0,85; (43.110/35.770)^0,85) ✓, Untergrenze 136,4 T€ ✓ · VSL 3,06 × 2,023 = 6,19 Mio. ✓, 6,19/0,1608 = 38,5 LJ ✓, 4,7/0,1608 = 29,2 ✓ · L̄_85+ (M) = 4,97 ✓, Gewichtung (990.292·4,97 + 1.853.921·5,69)/2.844.213 = 5,44 ✓ · m_a alle vier Werte ✓, Summen 83.456.045 EW / 1.028.206 Sterbefälle ✓, u65-Abweichung +18 % ✓ · Mini-Beispiel e^(0,0625·2,8)−1 = 0,191, × 40 = 7,6 ✓ · 0,018 × 5,44 × 160.800 = 15.746 ✓ · T67 1.400/83,46 Mio. = 1,68/100.000 ✓ · r₀ = 1,68 + 1,21…2,67 = 2,9–4,4 ✓ (0,168·7,2 = 1,21; 3,106·0,119·7,2 = 2,66) · c_kal 1,027 / R² 0,56 / 17 von 27 / Regionalfaktoren 0,618·0,705·1,089·1,737 / „11 von 16 Länder im Band 0,75–1,35" / Ausreißer SH/HH ×1,9–2,2, BB/BY ×1,6 — alle identisch mit c_kal_ergebnis_emp_4reg.md ✓ · σ_intra 2,36/2,58/2,57, Schiefe, Quantiltabelle (z. B. Nord w=1 −4,17) identisch mit wochenquantile_meta.csv / wochenquantile_region.csv ✓ · L̄_e Melanom 10,58 / C44 5,30 ✓ · λ_MM = 0,116, λ_C44 = 0,0055 ✓ · 98-C-Topf 22,98 Mrd. ✓ · λ_roh = 2(R−1)/(R+1): 0,84 / 1,01 ✓ · d_Saison 0,70·(0,75·60+0,55·30) = 43 ✓ · Quellenverweise [1]–[62] existieren alle im Kap. 6 und sind thematisch richtig zugeordnet.

---

## A. Fehler

**1. Ansatz 96-A (b), Formeln €_Zelle und ΔTage_Zelle — Fehler.**
Die beiden Ergebnisgrößen sind nicht proportional: €_Zelle enthält P̂_Zelle (lokale Vegetation), aber nicht d_Saison; ΔTage_Zelle enthält d_Saison, aber nicht P̂_Zelle. Der €-Wert wird direkt aus c_Jahr × ΔS/S_ref gebildet und nicht aus der ausgewiesenen physischen Größe (ΔTage) × Tageskostensatz — ein Tageskostensatz fehlt (Kap. 6 nennt „Tageskosten-Quelle allergischer Rhinitis" selbst als Datenlücke). Damit ist die Beweislastregel (3.2: zwischen Klimasignal und Euro steht eine physische Größe; G7 Menge × Rate × Preis) im empfohlenen Ansatz nicht eingehalten; zwei Zellen mit gleichem ΔTage können unterschiedliche € zeigen. Zusätzlich setzt c_Jahr × ΔS/S_ref implizit voraus, dass die jährlichen Direktkosten proportional zur Saisonlänge wachsen (Diagnostik, Immuntherapie sind fix) — unbegründet.
Vorschlag: € = ΔTage × c_Tag (c_Tag aus Schramm 2003 ÷ Symptomtage oder Bastl 2020), P̂_Zelle in beide Formeln; Proportionalitätsannahme explizit mit Band.

**2. Ansatz 95-A (b), Morbiditätsformel F_Zelle — Fehler (Semantik von e_HD,a) und Lücke (HD_ref).**
e_HD = 0,054 ist die relative Mehr-Einweisung *aller* Diagnosen je Hitzetag (K&Z Tab. 1: +3,106/100.000/Tag = +5,4 % der Gesamt-Einweisungen ≈ 57/100.000/Tag). Im Bericht wird sie auf die *hitzeassoziierte* Baseline r₀ ≈ 3,5/100.000/Jahr angewandt: ein zusätzlicher Hitzetag liefert dann 0,054 × 3,5 = 0,19 Fälle/100.000 (bundesweit ≈ 160), während K&Z +1,4…+3,1/100.000 (≈ 1.170–2.500 bundesweit) messen — Faktor 8–16 zu niedrig. Der Sanity-Korridor „zwischen T67-Untergrenze und K&Z-Obergrenze" (1.400 … 20.000) ist so breit, dass er den Fehler nicht auffängt. HD_ref hat weder Zahlenwert noch Herleitung (Zeichentabelle: „Referenzwert"); damit ist der HD-Term auch nicht nachweislich mittelwertzentriert (G9) und der Zeitbezug von r₀ (T67 2004–2024, K&Z 1999–2008, Ø 7,2 Hitzetage) nicht an HD_ref gekoppelt.
Vorschlag: F_Zelle = Σ_a pop_a·[r₀,a/100.000 + ε_a·(HD − HD_ref)] mit ε = +1,4…3,1/100.000 je Hitzetag (K&Z absolut, altersverteilt wie r₀); HD_ref = bevölkerungsgewichtetes Bundesmittel der hot_days-Klimatologie der Baseline-Periode, Zahl ausweisen.

**3. Ansatz 95-A (b), v_vers in D_a und F_Zelle — Fehler (Bandbezug / Zentrierung).**
β_pfl ist als „Pflegeheim-Effekt (Band 85+)" mit q̄_pfl = 0,149 (Heimanteil *der 85+*) hergeleitet, β_iso mit q̄_1P (Einpersonenhaushalte *65+*). Die Formel multipliziert v_vers aber auf D_a *aller* Bänder inkl. u65. Für u65/65–74/75–84 liegt der wahre Heimanteil weit unter 0,149 ⇒ jede Zelle ohne Heim erhält für diese Bänder pauschal ×0,73 — der Faktor ist dort nicht zentriert (Bundesmittel ≠ 1, Verstoß G9) und verschiebt das Niveau, das c_kal dann unkenntlich auffängt. Gleiches v_vers steht außerdem in F_Zelle: Nicholl [38] misst Mortalität transportierter Notfälle, Klenk/Bouchama Mortalität — für *Einweisungen* ist kein Effekt belegt (eine größere Distanz senkt Einweisungen eher). Verstoß G4.
Vorschlag: v_vers,a bandspezifisch (β_pfl nur 85+, ggf. 75–84 mit eigenem q̄), für F_Zelle Default 1 oder eigene Evidenz.

**4. Ansatz 95-A (a)/(c), f_a und „Validierung Altersverteilung" — Fehler (Zirkelschluss) und Lücke.**
f_a = 0,404/0,577/0,620/1,0 ist „aus publizierter RKI-Altersverteilung zurückgerechnet" [11,12]. In (c) wird die modellierte Altersverteilung „gegen publizierte RKI-Verteilung (6,5/12,9/25,2/55,5 %)" als „eigentlicher Prüfstein" validiert — gegen dieselbe Größe, aus der f_a stammt. Das ist keine unabhängige Prüfung (G12, 3.4). Zudem wird kein Ergebnis berichtet (modellierte Anteile fehlen) und die Rückrechnung f_a selbst ist nicht als Rechenkette gezeigt (G14, abgeleiteter Parameter).
Vorschlag: Rechenkette f_a ausweisen; Altersprüfung gegen eine unabhängige Reihe (z. B. an der Heiden 2019 [14] 2001–2015, Berlin/Hessen 2018 85+: 260–320/100.000) und Ergebnis tabellieren.

**5. Ansatz 95-A (c), Kalibrierlauf — Fehler (Übertragung c_kal, Richtung „konservativ").**
c_kal = 1,027 bzw. die Regionalfaktoren stammen aus einem Landesmittel-Näherungslauf „ohne UHI". Sie werden auf das 100-m-Zellmodell angewandt, das (i) bevölkerungsgewichtete statt flächengemittelte Temperaturen sieht (Städte liegen in wärmeren 1-km-Zellen) und (ii) mit konvexer RR-Kurve die mittelwerttreue UHI-Streuung ±1 K in einen positiven Nettoeffekt übersetzt. Beides erhöht die Modellsumme gegenüber dem Näherungslauf ⇒ mit demselben c_kal liegt die Zellsummen-Deutschlandsumme *über* dem Anker; die Bezeichnung „Näherung konservativ" gilt für den Rohwert, nicht für den daraus gewonnenen Faktor. Außerdem: „konservativ wird der Vollreihen-Wert [1,027] geführt, die Fenster-Variante [0,890] als Sensitivität" — der höhere Faktor ergibt den *höheren* Schaden; konservativ im Sinn von G8 („Untergrenze") wäre 0,890, zumal 2021–2025 um +48…+80 % überschätzt werden (Bericht: „+50…+65 %"; Datei: 2021 +79,5 %, 2023 +47,8 %).
Vorschlag: c_kal mit dem produktiven Zellmodell (nationaler Batch) fitten oder den Jensen-/Gewichtungsoffset quantifizieren; Wortwahl „konservativ" korrigieren oder 0,890 als Default.

**6. §1.2 und Zeichentabelle 95-A, VOLY-Band — Fehler (Rechenwert).**
Obergrenze „169,5 T€ (Raumtransfer ohne Elastizität)": 79.500 × 1,4638 × 1,2140 × 1,1719 = 165,6 T€; mit Raum- *und* Einkommensfaktor ohne Elastizität (1,2052) 170,3 T€. 169,5 ist aus keiner Kombination reproduzierbar.
Vorschlag: 165,6 T€ (oder Definition der Obergrenze anpassen).

**7. Zeichentabelle 95-A, r₀,a — Fehler (Verhältnis ≠ Werte) und Lücke (Quelle).**
„Altersaufteilung über Kreislauf-Ratenverhältnis 1 : 5 : 8 : 10" — die Werte 1,9/6,3/10,8/15,6 stehen im Verhältnis 1 : 3,3 : 5,7 : 8,2. Ein 1:5:8:10-Split mit bevölkerungsgewichtetem Mittel 3,5 ergäbe 1,53/7,63/12,2/15,3. Das Verhältnis selbst hat keine Quelle; der Text spricht von „Kreislauf-/Stoffwechsel", die Rechnung addiert nur Herz-Kreislauf (11,9 %, ohne Stoffwechsel 6,8 %/Atemwege 6,7 %). Die Altersverteilung ist messbar (Krankenhausdiagnosestatistik nach Alter, GENESIS 23131-0002 — Gastzugang ohne Registrierung ist zu prüfen, „Destatis-Login" ist m. W. nicht erforderlich), also per G5 zu messen.
Vorschlag: T67 bzw. I00–I99 je Altersgruppe aus GENESIS ziehen, Split als Rechenkette ausweisen; Diagnosegruppen konsistent benennen.

**8. Zeichentabelle 95-A, β_pfl-Herleitung — Fehler (zwei Zwischenwerte nicht reproduzierbar).**
(a) „O/E Heime 1,9 vs. Wohnung ≥ 75 1,9 / Kliniken 1,5 ⇒ Exzess-Faktor 1,32": 1,9/1,9 = 1,00; (1,9−1)/(1,7−1) = 1,29; 1,9/1,5 = 1,27 — 1,32 folgt aus keiner angegebenen Kombination (es bräuchte ein gewichtetes Nicht-Heim-O/E ≈ 1,68, das nicht genannt ist). (b) „Nicht-Heim-85+ 0,119/Jahr aus m85+ = 0,148 und q̄": (0,148 − 0,149·0,34)/0,851 = 0,114; 0,119 ergibt sich nur mit Heimrate 0,312 (0,6 %/Woche) — dann ist das Verhältnis 2,62, nicht 2,85; mit 0,34 ist es 2,97. Die Kette 1,32 × 2,85 = 3,8 ist also in beiden Gliedern unscharf; die Wahl OR = 3,5 bleibt Ermessen.
Vorschlag: Gewichtungsrechnung für 1,32 ausschreiben, eine Heimrate konsequent verwenden, Band daraus ableiten.

**9. Ansatz 98-A (b), r_out,e / Außenberufs-Anteil — Fehler (Kettentreue) und Lücke.**
Die Schadensbaum-Kette W186 nennt S154/S155/S158 und R35/R36. „Berufliche Außenexposition" ist kein Knoten dieser Kette; §1.1 verpflichtet auf „exakt die dort hinterlegten Knoten — nicht mehr, nicht weniger". Der Faktor fehlt zudem in der Eingangstabelle (a) (kein Knoten, keine Datenquelle, keine Auflösung) und q_out, q̄_out haben weder Wert noch Quelle (welcher Zensus-/Erwerbstätigen-Datensatz liefert den Außenbeschäftigten-Anteil je Zelle?).
Vorschlag: entweder als dokumentierte Kettenerweiterung (mit Begründung, warum die Arbeitsmappe hier ergänzt wird) samt Eingangszeile und q̄_out-Herleitung, oder Default 1 und als Sensitivität führen.

**10. Ansatz 98-A, k_UV — Fehler (unbelegter Zwischenwert) und Lücke (kein Default).**
„Dosis +4,9 %/Dek. bei SSD +11,3 %/Dek. (Dortmund) ⇒ k_UV ≈ 0,4–0,5": Der SSD-Trend +11,3 %/Dekade steht in keiner Quelle des Kap. 6 ([31] belegt nur die Dosis) und wäre das Vierfache des DWD-Bundestrends (+7,8 % in 30 Jahren ≈ +2,6 %/Dekade [33]). k_UV hat nur ein Band, keinen Default — im Produkt muss ein Wert stehen (G14 „gilt auch für Defaults").
Vorschlag: Fundstelle für den Dortmunder SSD-Trend (Lorenz 2024, Tab./Abb.) nachweisen oder k_UV aus der DWD-Station Dortmund selbst rechnen; Default 0,45 festlegen.

**11. Ansatz 96-A (b), ΔS/S_ref ≈ 0,15–0,25 — Fehler (nicht reproduzierbar) und Widerspruch zu d_Saison.**
Komponenten laut Zeichentabelle: Blühbeginn −17…−26 Tage, Saisonende +19 Tage ⇒ ΔS = 36…45 Tage. Für 0,15–0,25 müsste S_ref ≈ 145–300 Tage betragen; S_ref ist nirgends beziffert. Die d_Saison-Herleitung setzt dagegen L_B = 30, L_G = 60 Tage (S_ref ≈ 90 ⇒ ΔS/S_ref ≈ 0,4–0,5). Zudem ist „Blühbeginn Erle" kein Maß für die Birken-/Gräser-Saison der Patienten und „Vegetationsruhe 120 → 101" kein Pollensaison-Ende. Die Zahl, die das gesamte Klimasignal des Ansatzes trägt, ist damit nicht hergeleitet (G14). „Regional aus Stationsdaten" ist angekündigt, Regionalwerte fehlen.
Vorschlag: S_ref und ΔS je Pollengruppe (Birke, Gräser) nach EAACI-Kriterium aus DWD-Phänologie (Birke Blühbeginn, Gräser Blühbeginn/-ende) je Naturraum berechnen; Tabelle wie bei q_w.

**12. Ansatz 95-A (a), Altersbänder aus dem Zensus-Gitter — Fehler/Lücke (sofern das Gitter nur 10-Jahres-Klassen liefert).**
Das Zensus-2022-100-m-Gitter führt Alter in 10-Jahres-Klassen (… 60–69, 70–79, 80+). Die Bänder 65–74/75–84/85+ sind daraus nur per Split-Quoten herstellbar — die Tabelle nennt das als „Fallback: 65+-Anteil × nationale Senior-Splits". Damit wird Bundesstatistik zur räumlichen Verteilung der kritischsten Modellachse (85+) benutzt (3.1, G1), die Split-Quoten sind nicht hergeleitet (G14), und der Fall ist vermutlich Regel, nicht Fallback.
Vorschlag: Split aus Zensus-2022-Gemeindedaten (Einzelalter je Gemeinde, offen) statt national; Rechenregel und Werte ausweisen; oder Bänder auf das Gitter (60–69/70–79/80+) umstellen und f_a/m_a/L̄_a dafür neu herleiten.

## B. Widersprüche

**13. §5 Begründung vs. Rev. 5 — Widerspruch.** „national kalibriert (Faktor 1,44 gegen das Referenzband) … offen ist nur die Morbiditäts-Rekalibrierung" — Rev. 5 ersetzt 1,44 durch 1,027 bzw. Regionalfaktoren und listet weitere offene Punkte (ERF-Zeittrend). Text nachziehen.

**14. 95-A Eingangstabelle (a) vs. (b) — Widerspruch.** (a): „Normalverteilungs-Quantile um T̄_Zelle; Streuung σ_Region"; (b): empirische Quantile aus 21 Stationen. (a) korrigieren.

**15. Wirkungsketten-Kästen #95 und #98 vs. §1.2/G2 — Widerspruch.** #95: „Mortalität (Übersterblichkeit × VSL)"; #98: „Mortalitätsanteil × VSL" — die Formeln rechnen YLL × VOLY. Wenn Zitat der Monetarisierungs-Arbeitsmappe, als solches kennzeichnen und G2-Übersteuerung vermerken.

**16. R9-Abgrenzung #95 — Widerspruch.** §1.2-Tabelle: „Systemvorhaltung → #102 (ab M3)", Wirkungskette: „Weitergaben an #87 und #101". Außerdem „Kühlkosten → #65 (K8, M5)" — die Roadmap kennt M0–M4. Eindeutig machen.

**17. Regionale Kalibrierfaktoren vs. G1/3.4 — Widerspruch (undokumentierte Abweichung).** G1 und 3.4 fordern den nationalen Anker als *einen* Skalar auf die Deutschland-Summe; 3.1: Bundesstatistik nie zur räumlichen Verteilung. Rev. 5 fittet vier Faktoren (0,618 … 1,737, Spanne ×2,8) auf Bundesland-Jahre — Landesstatistik korrigiert damit die räumliche Verteilung zwischen Regionen. Das mag sachlich richtig sein (Winklmayr-3-Regionen vs. RKI-4-Regionen), ist aber eine Grundsatzabweichung, die als solche zu benennen ist (ggf. G1 ergänzen). Die Zuordnung Bundesland → Winklmayr-Region (N/M/S) und → RKI-Region (N/O/W/S) steht nicht im Bericht (nur in sommermittel_bundesland_zuordnung.csv). Ein Faktor 1,737 für den Süden heißt zudem: die publizierte Süd-Kurve (β 0,0531, T₀ 20,8) unterschätzt dort um 74 % — das verdient eine Ursachendiskussion statt nur eines Skalars.

**18. Preisstände — Widerspruch.** VOLY/VSL sind mit VPI und BIP bis *2024* angepasst, aber als „€₂₀₂₅" bezeichnet; c_Fall Preisstand 2023; c_e (Speckemeier, AOK-Daten ≈ 2017–2019) ohne Preisstand und ohne Inflationierung; c_Jahr „inflationsbereinigt" ohne Zahl. Ein gemeinsames Preisjahr fehlt (3.3, Leitfrage 9).

**19. Entitätenzahlen #98 — Widerspruch zwischen Quellen, nicht benannt.** Split 2015 (BfS): MM 35.495, BCC+SCC 257.790; ZfKD 2023: C43 27.430, C44 243.000. Die 2015-Werte liegen *über* den 2023-Werten (vermutlich inkl. In-situ/Mehrfachtumoren). 3.8 verlangt, Widersprüche zu benennen; die Split-Anteile sind so nicht auf die ZfKD-Basis übertragbar.

**20. Datum/Stand — Widerspruch.** Fußzeile „Stand 18.08.2026 … Web-Recherche 17./18.08.2026" vs. Kopf „22.08.2026 · Revision 5" (Quellen [48]–[62] mit Zugriff 22.08.). 95-C: κ „Fit an Extremjahre 2003/2018/2026" — 2026 ist laut (c) als laufende Saison ausgeschlossen.

**21. §1.2 Zellbeispiel — Widerspruch (klein).** „0,018 × 4,7 Mio. ≈ 84.100 €" — mit 0,018 sind es 84.600 €; 84.100 passt nur zu ungerundet 0,0179. Das Beispiel nennt außerdem weder T̄_Zelle noch c_kal und ist daher nicht nachrechenbar (Leitfrage 11).

**22. §1.6 vs. Aufgabe 2(5) — Widerspruch (Geltungsbereich).** Der Bericht beschränkt die Herleitungspflicht auf Ansatz A; die Aufgabe verlangt drei *vollständig* ausgearbeitete Ansätze. Für 95-C (κ, β_D, β_F, w_a), 96-B (m_man, r_sens-Interpolation) fehlen Zahlenwerte. Als dokumentierte Scope-Entscheidung vertretbar, aber als Abweichung zu kennzeichnen.

## C. Lücken

**23. G14/Leitfrage 13 — Zeichen ohne abgeschlossene Herleitung (empfohlene Ansätze).**
- q̄_1P „≈ 0,40": keine Rechnung (welche Zensus-Tabelle, Zähler/Nenner; Haushalte oder Personen?).
- d̄_KH: kein Wert, keine Aggregationsregel (bevölkerungsgewichtetes Bundesmittel der Ebene?).
- Ḡ_allergen: kein Wert (braucht nationalen OSM-Lauf); Ĝ ist „normiert 0…1" — es muss festgeschrieben sein, dass diese Normierung fixe Grenzen hat und nicht die editierbare Schicht-A-Norm (3.6).
- q̄_out, q_out: s. Befund 9.
- HD_ref: s. Befund 2; ebenso die Regel, wie ein 24-h-UHI-Zuschlag in zusätzliche Tmax>30-°C-Tage übersetzt wird („+ UHI-Verschiebung").
- q_pfl je Zelle: „OSM-Pflegeeinrichtungen × Destatis-Pflegestatistik" — OSM liefert i. d. R. keine Kapazität; die Zuteilung der Landes-Heimplätze auf OSM-Objekte ist nicht beschrieben.
- c_Jahr: kein Zahlenwert, kein Direktkostenanteil, keine Inflationsrechnung (Zeichentabelle nur „Stütze").
- k_UV, S_ref, ΔS regional: s. Befunde 10/11.
- L̄_a: nur die Männer-Kette ist gezeigt; e(85/90/95) und Bevölkerung der Frauen (F = 5,69) fehlen.
- λ_e, c_e: nur C44 gesamt (0,005; 5.890 €) — SCC und BCC haben um Größenordnungen verschiedene Letalität; die Formel ist je Entität definiert.
- I_e,a für SCC/BCC: ZfKD liefert C44 nur gesamt; Übertragungsregel des 2015-Splits auf Altersraten fehlt.
- δ_HAP (0,95): taucht in keiner Formel auf — auf welche Größe wirkt er (β? D_a? F?).

**24. „Später"-Verweise — Lücke (G14 ausdrücklich verboten).** Kap. 6: „Die in [38–43] genannten Effektgrößen werden bei der Implementierung gegen die Primärquellen verifiziert" — das betrifft die Basiswert-Parameter β_d, β_iso, β_pfl, OR_out des empfohlenen Ansatzes. [45]–[47] (Grundlage δ_HAP) sind ohne Autoren, „über Suchergebnisse identifiziert, vor Übernahme zu verifizieren". Destatis-J30/J45 „vor Implementierung ziehen". 3.8 verlangt Verifikation *vor* Übernahme.

**25. Validierung — Lücke (Leitfrage 3/8).** Angekündigte, aber nicht berichtete Prüfungen: modellierte Altersanteile (Befund 4); Bundessumme der Morbidität gegen T67/K&Z; Kosten-Sanity J30 (Betrag fehlt); ΔFälle-Bundessumme #98 gegen KKR. Ohne Zahlen sind die Sanity-Bänder nicht geprüft. Zusätzlich: Die Beschränkung der Kalibrierung auf „signifikante Jahre" (untere PI-Grenze > 0) schließt Jahre mit RKI ≈ 0 aus, in denen das Modell > 0 liefert — das verzerrt c_kal nach oben; Punktschätzer aller Jahre verwenden.

**26. Maßnahmen-Effektgrößen — Lücke (Aufgabe 2(6), 3.5, G10).** #95: „Hitzeschutzpläne in Pflegeeinrichtungen" ohne Effektgröße; Klimaanlage OR 0,93 aus unverifizierter Quelle [46]. #96: „Allergenarme Stadtbaumwahl" (wie viel ΔĜ je ersetztem Baum?) und „Pollenmonitoring" („dokumentierte Annahme" ohne Zahl). #98: Nutzen-Kosten 2,2–8,7 : 1 [37] ist keine Effektgröße auf Dosis oder Inzidenz; Shih/Doran/Collins liefern Inzidenzreduktionen, die zu zitieren wären. Für #96/#98 ist damit kein Hebel quantifiziert.

**27. Altersstruktur #96 — Lücke (G3, Leitfrage 6).** p_AR,a nur „Erwachsene 12,0 % · Kinder 8,8 %"; DEGS1 (Langen 2013) publiziert altersspezifische AR-Prävalenzen (stark fallend mit dem Alter). Mit zwei Klassen wird die Alterslast zwischen junger Innenstadt und alterndem Land systematisch falsch verteilt.

**28. Zeitbezug/Szenarien — Lücke (3.2 letzter Punkt).** Nirgends steht, welche Bezugsperiode T̄_Zelle (DWD-Monatsraster: welche Jahre?), SSD_heute, ΔS „heute" haben, noch wie Szenariojahre in eine der drei Wirkungsfunktionen eingehen (ΔT je Szenario? SSD-Projektion „+1,3 %/Dekade" ist genannt, aber nicht verdrahtet). Für #95 gilt zusätzlich: Wird T̄_Zelle als 30-jähriges Mittel angesetzt und nur die intra-saisonale Streuung, liefert das Modell den Schaden eines *mittleren* Sommers, nicht den Erwartungswert über Jahre (konvexe Kurve: Σ_Jahre f(T_j) > n·f(T̄)); c_kal wurde aber über reale Einzeljahre gefittet. Die Lücke ist aus den Kalibrierdaten quantifizierbar (Modell mit Mittelsommer vs. Mittel der 27 Jahresläufe). Latenz #98 ist dagegen sauber dokumentiert.

**29. Kettenvollständigkeit — Lücke (Leitfrage 1).** Nur benannt, nirgends verrechnet und ohne „neutral, weil"-Vermerk: S154 Freizeitverhalten (#95); S154/S155 und R36 (#96); R36 (#98). Eingangstabelle 95-A listet „4. Hitzetag in Folge +20 %", „Harvesting −25 %", „Rettungsdienst-Hilfsfrist" — gehen in keine Formel ein. Für jeden Knoten eine Zeile „verrechnet in … / neutral (G4) / Hebel".

**30. G6/G8 — Lücke.** Kartenebenen sind benannt (T̄_Zelle, HEAT_WAVE, POLLEN_LOAD, UV_RADIATION, YLL, ΔTage). Nicht spezifiziert: Raten-Darstellung „je 1.000 EW", aggregierte Quartier-Ebene, UI-Benennung „bewerteter Schaden — Konto K1", Vollständigkeitsanzeige, Versionsstempel (3.6 nennt alle drei; der Bericht nennt nur den Infokasten).

**31. YLL-Bewertung — Lücke (Unsicherheit).** L̄_a aus der Periodensterbetafel setzt für Hitzetote die Restlebenserwartung der Gesamtbevölkerung an; Hitzetote sind überwiegend vorerkrankt/gebrechlich (S153, Harvesting) — L̄_a ist damit eine Obergrenze. Kein Band, keine Sensitivität dokumentiert; das relativiert die Aussage „YLL-Weg … konservativ".

**32. Form — Lücke (Leitfrage 11).** Im Text verwendete, in keiner Zeichentabelle/Formel definierte Zeichen: v_access (95-A Maßnahmen), v_acc (95-C), v_monitor (96-A), v_verhalten/v_verh (98-A), „AF" als Dämpfungsziel (95-A), δ_HAP, σ_Region. Kriterienlabels K1–K6 (§1.4/§5) kollidieren mit den Schadenskonten K1–K8. Zeichentabelle 95-A: q_w,Region steht zwischen β_iso und β_pfl (nicht alphabetisch). β_d: nach G4 wäre bei fehlender hitzespezifischer Evidenz Default 0 (Band 0–0,002 enthält 0) und der Effekt als Sensitivität — der Bericht führt 0,001 als Default.

**33. Umsetzbarkeit q_1P — Lücke (Leitfrage 12).** „Anteil Einpersonenhaushalte 65+ der Zelle" braucht die Kreuzung Alter × Haushaltsgröße auf 100 m; ob das Zensus-2022-Haushaltsgitter sie liefert, ist nicht belegt. Falls nicht, ist q_1P ein Proxy (alle Einpersonenhaushalte) mit anderem q̄ und anderer Effektgröße.

---

## Gesamtbewertung nach Leitfragen

| Leitfrage | Status | Hauptgrund |
|---|---|---|
| 1 Vollständigkeit der Kette | teilweise | S154 (#95), S154/S155/R36 (#96), R36 (#98) nur benannt; Außenberuf (#98) außerhalb der Kette (Befunde 9, 29) |
| 2 Verteilschlüssel-Test | weitgehend erfüllt | A-Ansätze bottom-up; Ausnahmen: nationale Senior-Splits für Altersbänder (12), regionale c_kal aus Landesstatistik (17). 96-A differenziert lokal nur ±30 % |
| 3 Physische Zwischengröße | nicht erfüllt für #96 | € umgeht ΔTage (1); für #95/#98 erfüllt, aber Bundessummen nicht berichtet (25) |
| 4 Doppelzählung | überwiegend erfüllt | G13 (Grün/UHI) und Hebel-Wächter sauber; v_vers auf F ohne Beleg (3) |
| 5 Modifikatoren | teilweise | OR-Übersetzung formal korrekt; Zentrierung bei v_vers bandübergreifend verletzt (3), HD-Term ohne HD_ref (2), Zentrierungsmittel ohne Herleitung (23) |
| 6 Altersstruktur | #95/#98 erfüllt, #96 nicht | (27) |
| 7 Tails/Parameter | weitgehend erfüllt | empirische Quantile vorbildlich; messbare, aber gesetzte Werte: r₀-Split, q̄_1P, d̄_KH, Ḡ, S_ref (7, 23) |
| 8 Kalibrierung | teilweise | Revisionsstand ✓, Stadt-Land-Anker ✓; Altersprüfung zirkulär und ohne Ergebnis (4), c_kal-Übertragung und Jahresauswahl verzerrt (5, 25), Jensen-Lücke (28) |
| 9 Kostensätze | teilweise | VOLY/VSL-Konsistenz ✓; Preisjahre uneinheitlich, c_Jahr/c_e ohne Wert bzw. Preisstand (18, 23), VOLY-Band-Fehler (6) |
| 10 Quellen | teilweise | Zuordnung [n] stimmt; „später"-Verifikation für Basisparameter (24), unbelegter SSD-Trend (10), unbenannter Quellenwiderspruch (19) |
| 11 Form | teilweise | undefinierte Zeichen, K-Label-Kollision, Beispiel nicht nachrechenbar (21, 32) |
| 12 Umsetzbarkeit | weitgehend erfüllt | Daten offen/keyless; offen: Alter × Haushalt auf 100 m (33), q_pfl-Kapazitätsregel (23), Ĝ-Normierung fix? (23) |
| 13 Herleitungspflicht | nicht erfüllt | mindestens zwölf Zeichen der empfohlenen Ansätze ohne abgeschlossene Herleitung (23), dazu 24 |

Drei-Ansätze-Vergleich mit Kriterienraster: vorhanden (§5, sechs Kriterien + Aufwand), Verteilschlüssel-Ansätze korrekt als Negativbeispiele geführt — erfüllt; Scope-Einschränkung für B/C (22) kennzeichnen.

Fazit: Rev. 5 hat für #95 die zentralen Primärdaten-Ketten (VOLY, m_a, L̄_a, Wochenquantile, c_kal) tatsächlich geschlossen und belegbar gemacht — das ist ein echter Fortschritt. Nicht freigabefähig sind aber (i) die Morbiditätsformel 95-A (Befund 2), (ii) der €-Pfad 96-A (1, 11), (iii) die bandübergreifende v_vers-Anwendung (3), (iv) die zirkuläre Altersvalidierung (4) und (v) die verbleibenden „später"-Verweise und nicht hergeleiteten Zentrierungsmittel (23, 24). Die Befunde 6, 7, 8 sind Rechenkorrekturen ohne Strukturfolgen.
