# Evidenz-Register (risikoübergreifend)

Zentrales Register nach Aufgabe §2.2/§7: ein belegter Zusammenhang wird **einmal** recherchiert
und je Risiko nur referenziert (Register-ID). Erstbefüllung 26.08.2026 aus der Migration von
M0 Rev. 5 (#95); Stand Rev. 6 (26.08.2026); die Entscheidungsspalte je Risiko führt der jeweilige Methodik-Bericht
(Kap. 2) — hier stehen die wiederverwendbaren Evidenz-Zeilen mit Verwendungsnachweis.

Regeln (§2.2): In Formeln nur Zeilen mit Entscheidung „Basiswert" (im jeweiligen Bericht);
Fall-Kontroll-Effektgrößen sind nie Maßnahmen-Effektgrößen; fehlende Evidenz zu einem
Ketten-Knoten ist eine Zeile mit Entscheidung „bewusst inaktiv" — keine stillen Lücken.

| Register-ID | Knoten → Outcome | Effektgröße | Studientyp | Quelle | Übertragbarkeit | Datenlage je Zelle | verwendet in |
|---|---|---|---|---|---|---|---|
| 95-E02-01 | Hitze → Mortalität | RR-ERF: T₀ 19,7/20,2/20,8 °C; β₈₅₊ 0,0634/0,0625/0,0531 K⁻¹ (N/M/S) | publizierte ERF (amtl. Übersterblichkeit) | Winklmayr u. a. 2022, Dtsch Arztebl Int 119:451 | DE 1992–2021; Skalentransfer Region→Zelle dokumentierte Grenze | Zelltemperatur (DWD 1 km + UHI) | #95 (Basiswert) |
| 95-E02-02 | Hitzetage → Krankenhauseinweisungen | konditional +2,4 %/Hitzetag (Basis, Rev. 6); unkonditional +5,4 % (Obergrenze) | quasi-experimentell (Panel 1999–2008) | Karlsson & Ziebarth 2018, JEEM 91:93 (IZA-DP 7875) | DE; Alterstabelle nicht publiziert (top-kodiert > 75) | DWD hot_days (1 km, ohne UHI-Verschiebung — Bericht §3.4) | #95 (Basiswert, konditional; Log 19) |
| 95-S152-01 | Altersstruktur → Hitzemortalität | fₐ 0,357/0,588/0,631/1,0 (Rückrechnung Rev. 6, Bericht §3.3a); mₐ; L̄ₐ | amtliche Statistik + Rückrechnung | RKI EB 19/2025; Destatis Sterbetafel/-fälle | DE; Kette vollständig im Bericht | Zensus-2022-Altersbänder | #95 (Basiswert) — wiederverwendbar für alle altersgeschichteten K1-Risiken |
| 95-S152-02 | Soziale Isolation (allein lebend) → Hitzemortalität | OR ≈ 2,3 ⇒ β_iso 0,90 (zentriert, q̄ = 0,346, Mikrozensus 2023) | Fall-Kontrolle | Semenza u. a. 1996, NEJM 335:84; Destatis Mikrozensus 2023 | Chicago 1995; Übertragung als dokumentierte Annahme | Zensus-2022-Haushaltsgitter (Kreuzung ×65+ zu verifizieren) | #95 (Basiswert; Bandzuordnung Befund 44) |
| 95-S153-01 | Pflegeheim/Bettlägerigkeit → Hitzemortalität | OR Heim vs. Nicht-Heim 3,0 (2,2–6,0) ⇒ β_pfl 1,54; q̄_pfl,85+ 0,149 | Kohorte (Fouillet); Meta (Bouchama, Stütze); Klenk: ERF im Heim-Setting | Fouillet 2006; Bouchama 2007; Klenk 2010; Pflegestatistik 2023 | F/DE; Kette vollständig (Bericht §3.3b) | OSM-Pflegeeinrichtungen × Pflegestatistik (Proxy) | #95 (Basiswert, nur D-Pfad, nur 85+) |
| 95-S153-04 | Pflegeheim → Hospitalisierung | OR 0,96 [0,67–1,36] n. s. — kein Effekt (Gegenevidenz) | Case-Crossover (Flandern, 10 Heime 2013–2017) | IJERPH 18:10697, 2021 | Heimbewohner versterben vor Ort statt Einweisung | — | #95 (bewusst inaktiv: β_pfl nicht im F-Pfad) |
| 95-R36-01 | Krankenhaus-Distanz → Notfall-Mortalität | +≈1 %/10 km ⇒ β_d ≈ 0,001/km (bewusst schwach) | Beobachtung (transportierte Notfälle) | Nicholl u. a. 2007, Emerg Med J 24:665 | UK; misst transportierte Notfälle — Übertragbarkeit zu schwach für Basiswert | HEALTHCARE_ACCESS-Distanz | #95 (Sensitivitätsband, Basiswert-Default 1) |
| 95-S158-01 | Hitzewarnsystem/Aktionsplan → Mortalität | δ_HAP 0,95 (0,85–1,00); DiD RR 1,00/adj. 0,85; Europa: HAF-Reduktion 25,2 % [19,8–31,9] (Einführungseffekt, Urban 2025) | Interventions-/quasi-experimentell | Feldbusch u. a. 2025 (Env Int 203:109746); ERL 2025 | DE-Städte/Europa; [45]/[46] Volltext gegengelesen (T2.4) | kommunal | #95 (Maßnahmen-Hebel) |
| 95-S157-01 | Klimaanlagen in Pflegeheimen → Mortalität | rOR ≈ 0,93 an Extremhitzetagen | Case-Crossover (73.578 Todesfälle) | Katz u. a. 2026, JAMA Intern Med 186:243 | Ontario 2010–2023 | Heim-Ebene | #95 (Maßnahmen-Hebel) |
| 96-R35-01 | Bevölkerung → Betroffene (AR-Prävalenz, altersspezifisch) | p_AR 12-Monats: u20 8,8 % · 20–64 13,2 % · 65–74 6,7 % · 75+ 5,0 % (gewichtet aus DEGS1 Tab. 3: 14,6/17,2/14,3/10,1/8,2/5,0 für 18–29…70–79) | bevölkerungsrepräsentative Surveys | Langen u. a. 2013 (DEGS1); Thamm u. a. 2018 (KiGGS W2); Gewichte Destatis 31.12.2023 | DE; DEGS1 endet bei 79 (Extrapolation 75+ gekennzeichnet) | Zensus-Altersbänder + neue Ebene u20 | #96 (Basiswert) — wiederverwendbar für alle prävalenzbasierten K1-Risiken |
| 96-W025-01 | Phänologie → Pollensaison-Spreizung | ΔS_Birkengruppe 3,96/4,20/5,94 · ΔS_Gräser 4,78/4,08/3,70 Tage (N/M/S; 1961–90 → 1991–2020; gepaarte Stationen) | amtliche Messreihe, eigene Auswertung (`dwd_pollensaison.py`) | DWD-CDC Phänologie-Jahresmelder; `pollensaison_region.csv` | DE-weit, 1.083/1.085 Stationen; Birke über Phase 4 (Marker-Offset dokumentiert) | regional (Bundesland → N/M/S) | #96 (Basiswert) |
| 96-W025-02 | Klimawandel → Anteil am Pollensaison-Trend | a_attr 0,50 (IQR 0,19–0,84) | Attributionsstudie | Anderegg u. a. 2021, PNAS | Nordamerika; Übertragung dokumentierte Annahme | Literatur-Band | #96 (Basiswert) — Kandidat für weitere Phänologie-Risiken |
| 96-W024-01 | Lokale allergene Vegetation → Symptomlast | λ 0,7 (0,3–1,0); Fallen-Differenzen 245 %/306 % (Zuwachs-Lesart, Bericht §3.4) | Pollenfallen-Messreihen, Symptomgradient, Lidar | Werchan 2017/2018; Bogawski 2019 | Berlin/Posen; gekennzeichnete Abschätzung; Prozent-Lesart dokumentiert | OSM-Vegetation (Ebene POLLEN_LOAD, neu) | #96 (Basiswert) |
| 96-K1-01 | AR → direkte Behandlungskosten je Betroffenem | 210,3 €₂₀₁₄/Jahr (populationsbasiert, alle Schweregrade) ⇒ 266,90 €₂₀₂₄; Obergrenze Schramm (moderate–schwer): 1.019 €₂₀₂₄ Erw., Kinder 1.027–1.335 | Bevölkerungs-Fragebogenstudie (TOTALL); Querschnitt (Schramm) | Cardell u. a. 2016; Schramm u. a. 2003 | SE→DE-Raumtransfer 1:1 dokumentiert; Schramm-Schweregrad-Skew dokumentiert | national | #96 (Basiswert + Sensitivitätsband) |
| 96-S158-01 | S158 Pollen-Frühwarnung → Symptomlast | keine quantifizierte Interventions-Effektgröße publiziert ⇒ **Abschätzung** r_S158 = 0,03 (Band 0,005–0,10; Kette q_reich 0,35 × q_handel 0,40 × e_Tag 0,20) | — (keine Interventionsstudie; §3.8-Datenlücke ausdrücklich benannt) | Herleitung: Bericht #96 §5.1 (`#s158-wirkung`); Ebene EARLY_WARNING_SYSTEMS (DWD/PID-Gefahrenindex) | §3.9 ABGESCHÄTZT — Setzung für deutsche Kommunen, im Produkt als „Abschätzung von KAP3" auszuweisen (Vorgabe P2, F-0007) | kommunal (Pauschalfaktor — Modellgrenze der Abschätzung) | #96 (Maßnahmen-Hebel, abgeschätzt; ersetzt die Führung „qualitativ"/Wirkung null seit 08.09.2026) |
| 98-E20-04 | UV-Dosis → Hautkrebs-Inzidenz (BAF) | SCC 2,5 ± 0,7 · BCC 1,4 ± 0,4 · MM 0,6 ± 0,4 (%-Inzidenz je +1 % Dosis) | biologisch-epidemiologisches Standardmodell | Slaper 1996 (Nature); RIVM 2023-0426; Madronich 2021 | international etabliert | — | #98 (Basiswert) |
| 98-E20-02 | SSD-Trend → erythemwirksame Dosis | k_UV 0,84 (0,4–1,0) = 4,9 %/Dek. (Lorenz 2024, Dortmund) ÷ 5,81 %/Dek. (NRW-SSD 1997–2022, eigene Messung) | Messreihe × eigene Trendrechnung | Lorenz 2024 (doi:10.1007/s43630-024-00658-8); dwd_ssd_trend.py | Dortmund/NRW→DE; Paarungs-Lesart dokumentiert (Bericht §3.2) | berechnet | #98 (Basiswert) |
| 98-OUT-01 | Berufliche Außenexposition → SCC | OR 1,77 [1,37–2,30] (Fall-Kontrolle), 1,68 [1,08–2,63] (Kohorten); q̄_out 0,070 (VGR 2023) | Meta-Analyse (BK-5103-Grundlage) | Schmitt 2011 (Br J Dermatol 164:291); Destatis VGR | DE; kein Knoten der W186-Kette (Bericht Kap. 1) | INKAR/SVB-Branchen (Ebene neu) | #98 (Sensitivitätsband, Default 1) — wiederverwendbar (#87/K2, Außenberufe-Hitze) |
| 98-K1-01 | Hautkrebs-Fall → Erstjahres-Behandlungskosten | MM 5.326/9.038 €₂₀₁₅ (SCS-/nicht-SCS-detektiert) ⇒ 6.724/11.410 €₂₀₂₄; NMSC 4.660/5.890 ⇒ 5.883/7.436; SCS-DiD −18,8 % [8,4–23,1] | Krankenkassen-Routinedaten (DiD) | Speckemeier 2022 (BMC Health Serv Res 22:749) | DE, Kohorte 2014/15; Proxy-Kennzeichnung (Bericht §3.4) | national | #98 (Basiswert + Band; Maßnahmen-Hebel SCS) |

### #60 — Schäden an Gebäuden aufgrund von Flusshochwasser (Erstaufschlag 11.09.2026)

Skelett aus `/neu-risiko 60`: eine Zeile je Knoten der Kette W117 samt W085 (Bericht
`docs/methodik/60_gebaeudeschaeden_flusshochwasser.md`, Kap. 1/2). Evidenz ist noch nicht
recherchiert; Entscheidungen stehen im Bericht auf `offen`. Einzige bezifferte Zeile: 60-S092-01
(Abschätzung von KAP3 nach Vorgabe P2).

| Register-ID | Knoten → Outcome | Effektgröße | Studientyp | Quelle | Übertragbarkeit | Datenlage je Zelle | verwendet in |
|---|---|---|---|---|---|---|---|
| 60-W085-01 | W085 Hochwasser → Überflutungswahrscheinlichkeit/-tiefe am Gebäude | offen | offen | offen | offen | offen (Ebene §3.1) | #60 (offen) |
| 60-E12-01 | E12 Schneeschmelze → W085 | offen | offen | offen | offen | offen | #60 (offen) |
| 60-E07-01 | E07 Nässe → W085 | offen | offen | offen | offen | offen | #60 (offen) |
| 60-E08-01 | E08 Starkregen → W085 / Gebäudeschaden | offen | offen | offen | offen | offen | #60 (offen) |
| 60-S072-01 | S072 Boden-/Vegetationsbedeckung → Abfluss | offen | offen | offen | offen | offen | #60 (offen) |
| 60-S073-01 | S073 Flächenversiegelung → Abfluss | offen | offen | offen | offen | offen | #60 (offen) |
| 60-S074-01 | S074 Topographie → Wassertiefe am Gebäude | offen | offen | offen | offen | offen | #60 (offen) |
| 60-R17-01 | R17 Oberflächengewässer → Exposition | offen | offen | offen | offen | offen | #60 (offen) |
| 60-R18-01 | R18 Entwässerungssysteme → Gebäudeschaden | offen | offen | offen | offen | offen | #60 (offen) |
| 60-R19-01 | R19 Infrastruktur an Binnengewässern → Gebäudeschaden | offen | offen | offen | offen | offen | #60 (offen) |
| 60-E10-01 | E10 Hagel → Gebäudeschaden | offen | offen | offen | offen | offen | #60 (offen) |
| 60-E17-01 | E17 Starkwind → Gebäudeschaden | offen | offen | offen | offen | offen | #60 (offen) |
| 60-E14-01 | E14 Schnee- und Eisdruck → Gebäudeschaden | offen | offen | offen | offen | offen | #60 (offen) |
| 60-E02-01 | E02 Hitze → Gebäudeschaden | offen | offen | offen | offen | offen | #60 (offen) |
| 60-E03-01 | E03 Kälte / Frost → Gebäudeschaden | offen | offen | offen | offen | offen | #60 (offen) |
| 60-W074-01 | W074 Meeresspiegelhöhe → Gebäudeschaden | offen | offen | offen | offen | offen | #60 (offen) |
| 60-W077-01 | W077 Sturmfluten → Gebäudeschaden | offen | offen | offen | offen | offen | #60 (offen) |
| 60-W087-01 | W087 Sturzfluten → Gebäudeschaden | offen | offen | offen | offen | offen | #60 (offen) |
| 60-W008-01 | W008 Bergsturz, Felssturz, Steinschlag → Gebäudeschaden | offen | offen | offen | offen | offen | #60 (offen) |
| 60-W006-01 | W006 Rutschungen und Muren → Gebäudeschaden | offen | offen | offen | offen | offen | #60 (offen) |
| 60-W091-01 | W091 Grundwasserstand → Gebäudeschaden | offen | offen | offen | offen | offen | #60 (offen) |
| 60-W100-01 | W100 Kanalnetze/Vorfluter → Gebäudeschaden | offen | offen | offen | offen | offen | #60 (offen) |
| 60-S092-01 | S092 Objektschutz der Eigentümer → Gebäudeschaden (K3) | keine nach §3.5 zulässige Effektgröße belegt ⇒ **Abschätzung** r_S092 = 0,035 (Band 0,0075–0,112; Kette Δq 0,10 × s_bem 0,50 × e_bem 0,70) | — (keine Interventionsstudie belegt) | Herleitung: Bericht #60 §5.1 (`#s092-wirkung`) | §3.9 ABGESCHÄTZT — im Produkt als „Abschätzung von KAP3" auszuweisen (Vorgabe P2) | kommunal (Pauschalfaktor — Modellgrenze der Abschätzung) | #60 (Vorschlag Maßnahmen-Hebel, abgeschätzt) |
| 60-S093-01 | S093 Gebäudezustand → Schadensgrad | offen | offen | offen | offen | offen | #60 (offen) |
| 60-S094-01 | S094 Baumaterialien → Schadensgrad | offen | offen | offen | offen | offen | #60 (offen) |
| 60-S096-01 | S096 Vorsorge öffentliche Hand → Überflutungswahrscheinlichkeit | offen | offen | offen | offen | offen | #60 (offen; R7 mit #50) |
| 60-S097-01 | S097 Zustand Schutzinfrastruktur → Versagenswahrscheinlichkeit | offen | offen | offen | offen | offen | #60 (offen; R7 mit #50) |
| 60-S098-01 | S098 Baumaterialien Schutzinfrastruktur → Versagenswahrscheinlichkeit | offen | offen | offen | offen | offen | #60 (offen; R7 mit #50) |
| 60-S104-01 | S104 Investitionen in exponierten Gebieten → Bestandsentwicklung | offen | offen | offen | offen | offen | #60 (offen) |
| 60-R24-01 | R24 Gebäude → Mengengerüst (Gebäudewerte) | offen | offen | offen | offen | offen (Ebene §3.1) | #60 (offen) |
| 60-R23-01 | R23 Bau- und Immobilienunternehmen → Gebäudeschaden | offen | offen | offen | offen | offen | #60 (offen) |
| 60-R25-01 | R25 Siedlungsinfrastrukturen → Gebäudeschaden | offen | offen | offen | offen | offen | #60 (offen) |

### #61 — Vegetation in Siedlungen (Erstaufschlag 11.09.2026)

Skelett aus `/neu-risiko 61`: eine Zeile je Knoten der Kette W127 samt W030 (Bericht
`docs/methodik/61_vegetation_in_siedlungen.md`, Kap. 1/2). Evidenz ist noch nicht recherchiert;
Entscheidungen stehen im Bericht auf `offen`. Einzige bezifferte Zeile: 61-S099-01 (Abschätzung von
KAP3 nach Vorgabe P2). **Keine Zeile aus #60 wiederverwendet:** Die gemeinsamen Knoten S096, R23, R24,
R25 haben dort ein anderes Outcome (Überflutung/Gebäudeschaden), hier Grünunterhalt-Mehrkosten.

| Register-ID | Knoten → Outcome | Effektgröße | Studientyp | Quelle | Übertragbarkeit | Datenlage je Zelle | verwendet in |
|---|---|---|---|---|---|---|---|
| 61-W030-01 | W030 Arealverschiebung / Standortstress → Vitalitätsverlust Stadtvegetation | offen | offen | offen | offen | offen (Ebene §3.1) | #61 (offen) |
| 61-E01-01 | E01 Durchschnittstemperatur → W030 | offen | offen | offen | offen | offen | #61 (offen) |
| 61-E06-01 | E06 Durchschnittlicher Niederschlag → W030 | offen | offen | offen | offen | offen | #61 (offen) |
| 61-S010-01 | S010 Habitat-/Biotoptyp → Grünunterhalt-Mehrkosten | offen | offen | offen | offen | offen | #61 (offen) |
| 61-S011-01 | S011 Habitat-/Biotopzustand → Grünunterhalt-Mehrkosten | offen | offen | offen | offen | offen | #61 (offen) |
| 61-S012-01 | S012 Tierart → Grünunterhalt-Mehrkosten | offen | offen | offen | offen | offen | #61 (offen) |
| 61-S013-01 | S013 Pflanzenart → Ausfall-/Ersatzpflanzungsrate | offen | offen | offen | offen | offen | #61 (offen) |
| 61-S014-01 | S014 Topographie → Grünunterhalt-Mehrkosten | offen | offen | offen | offen | offen | #61 (offen) |
| 61-S015-01 | S015 Boden-/Vegetationsbedeckung → Grünunterhalt-Mehrkosten | offen | offen | offen | offen | offen | #61 (offen) |
| 61-S016-01 | S016 Flächenversiegelung → Standortstress Straßenbäume | offen | offen | offen | offen | offen | #61 (offen) |
| 61-S017-01 | S017 Zerschneidung durch Verkehrswege → Grünunterhalt-Mehrkosten | offen | offen | offen | offen | offen | #61 (offen) |
| 61-S018-01 | S018 Anthropogene Verbreitung von Arten → Grünunterhalt-Mehrkosten | offen | offen | offen | offen | offen | #61 (offen) |
| 61-S019-01 | S019 Ausbreitungskorridore → Grünunterhalt-Mehrkosten | offen | offen | offen | offen | offen | #61 (offen) |
| 61-S020-01 | S020 Landwirtschaftliche Nutzung → Grünunterhalt-Mehrkosten | offen | offen | offen | offen | offen | #61 (offen) |
| 61-R03-01 | R03 Areale, Arten, Populationen → Mengengerüst | offen | offen | offen | offen | offen | #61 (offen) |
| 61-R04-01 | R04 Biotope, Habitate, Ökosysteme → Mengengerüst | offen | offen | offen | offen | offen | #61 (offen) |
| 61-S096-01 | S096 Vorsorge öffentliche Hand → Grünunterhalt-Mehrkosten | offen | offen | offen | offen | offen | #61 (offen; R7) |
| 61-S099-01 | S099 Begrünung von Städten/Siedlungen → Mengengerüst und Mehrkosten neuer Flächen | Maßnahmen: keine Effektgröße belegt ⇒ **Abschätzung** v_neu = 0,60 (Band 0,40–0,90, Stadtgrün) · v_geb = 0,30 (Band 0,10–0,60, Dach-/Fassadengrün); Mengengerüst offen | — (keine Studie belegt) | Herleitung: Bericht #61 §5.1 (`#s099-wirkung`) | §3.9 ABGESCHÄTZT — im Produkt als „Abschätzung von KAP3" auszuweisen (Vorgabe P2) | kommunal (Pauschalfaktor — Modellgrenze der Abschätzung) | #61 (Vorschlag Mengengerüst + Maßnahmen-Hebel, abgeschätzt) |
| 61-R23-01 | R23 Bau- und Immobilienunternehmen → Grünunterhalt-Mehrkosten | offen | offen | offen | offen | offen | #61 (offen) |
| 61-R24-01 | R24 Gebäude → Mengengerüst Gebäudegrün | offen | offen | offen | offen | offen (Ebene §3.1) | #61 (offen) |
| 61-R25-01 | R25 Siedlungsinfrastrukturen → Mengengerüst Straßenbegleitgrün (K4) | offen | offen | offen | offen | offen (Ebene §3.1) | #61 (offen) |

### #50 — Belastung oder Versagen von Hochwasserschutzsystemen (Erstaufschlag 11.09.2026)

Skelett aus `/neu-risiko 50`: eine Zeile je Knoten der Kette W103 samt W085/W087 (Bericht
`docs/methodik/50_hochwasserschutzsysteme.md`, Kap. 1/2). Evidenz ist noch nicht recherchiert;
Entscheidungen stehen im Bericht auf `offen`. Einzige bezifferte Zeile: 50-S076-01 (Abschätzung von
KAP3 nach Vorgabe P2). **Keine Zeile aus #60 wiederverwendet:** Die gemeinsamen Knoten W085, W087, E07,
E08, E12, S072–S074, R17–R19 haben dort das Outcome Überflutung/Gebäudeschaden, hier Belastung bzw.
Versagen des Schutzsystems.

| Register-ID | Knoten → Outcome | Effektgröße | Studientyp | Quelle | Übertragbarkeit | Datenlage je Zelle | verwendet in |
|---|---|---|---|---|---|---|---|
| 50-W085-01 | W085 Hochwasser → Belastung des Schutzsystems | offen | offen | offen | offen | offen (Ebene §3.1) | #50 (offen) |
| 50-W087-01 | W087 Sturzfluten → Belastung des Überflutungsschutzes | offen | offen | offen | offen | offen | #50 (offen) |
| 50-E12-01 | E12 Schneeschmelze → W085 | offen | offen | offen | offen | offen | #50 (offen) |
| 50-E07-01 | E07 Nässe → W085 / Durchfeuchtung Deichkörper | offen | offen | offen | offen | offen | #50 (offen) |
| 50-E08-01 | E08 Starkregen → W085/W087 | offen | offen | offen | offen | offen | #50 (offen) |
| 50-S072-01 | S072 Boden-/Vegetationsbedeckung → Abfluss | offen | offen | offen | offen | offen | #50 (offen) |
| 50-S073-01 | S073 Flächenversiegelung → Abfluss | offen | offen | offen | offen | offen | #50 (offen) |
| 50-S074-01 | S074 Topographie → geschützte Fläche hinter der Schutzlinie | offen | offen | offen | offen | offen | #50 (offen) |
| 50-S076-01 | S076 Art und Zustand der Schutzinfrastruktur → Versagenswahrscheinlichkeit | Basis offen; Maßnahmen: keine nach §3.5 zulässige Effektgröße belegt ⇒ **Abschätzung** r_deich = 0,35 (Band 0,15–0,63; a_def 0,50 × e_def 0,70) · r_ret = 0,24 (Band 0,08–0,48; s_vol 0,60 × e_ret 0,40) | — (keine Interventionsstudie belegt) | Herleitung: Bericht #50 §5.1 (`#s076-wirkung`) | §3.9 ABGESCHÄTZT — im Produkt als „Abschätzung von KAP3" auszuweisen (Vorgabe P2) | kommunal (Pauschalfaktor — Modellgrenze der Abschätzung) | #50 (Vorschlag Vulnerabilität + Maßnahmen-Hebel, abgeschätzt; R7-Weiche) |
| 50-R17-01 | R17 Oberflächengewässer → Exposition | offen | offen | offen | offen | offen | #50 (offen) |
| 50-R18-01 | R18 Entwässerungssysteme → Versagen Überflutungsschutz | offen | offen | offen | offen | offen | #50 (offen) |
| 50-R19-01 | R19 Infrastruktur an Binnengewässern → Mengengerüst (Schutzanlagen) | offen | offen | offen | offen | offen (Ebene §3.1) | #50 (offen) |

