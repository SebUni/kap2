# Methodik-Bericht #95 — Hitzebelastung

Status: **Rev. 8, Fortschreibung 7 — in Revision** (A-0048; Ledger-Runde 31, Divergenzen aus der Integration,
Vorhaben T-1534-cmo; zuletzt abgenommen vom methodik_manager am 26.09.2026 nach der Null-Runde 30; seit der Fortsetzung
der Runde 31, Teil 2, hat der Hebel S157 eine Voreinstellung und die öffentlichen Kühlzentren einen eigenen Hebel; Teil 3
ergänzt die Eingabe zum Doppelzählungs-Wächter, den Block der Kappung 0,794 und die Bänder und Sensitivitäten von \(f_a\)
und \(\bar L_a\), ohne einen Betrag zu ändern; die Gegenprüfung steht aus) · 27.09.2026 ·
Rev. 8 vom 30.08.2026 (§3.4-Ressourcen-Regel, q_pfl-Ebene angelegt, q_1P geparkt, L̄_85+ exakt 4,16 J; Befunde
86–94 behoben) hat Fortschreibung 7 in den Ledger-Runden 10–29 um die Rechenkette 3.0, den Pflichtabschnitt „Risiko
ohne (weitere) Anpassung“, die Kennzeichnung der Parameter, die Ersatzregel für den Anteil 65+, den Berlin-Anker und
die Maßnahmen-Hebel S157 und Schutzprogramme vulnerable Gruppen ergänzt; im Produkt stehen die Ersatzregel (Befund
116), die Kennzeichnung der Parameter und die beiden Hebel noch aus ·
Instruktionsquelle: `docs/AUFGABE_METHODIK_SCHADENSRECHNUNG.md` (v2) · Umsetzungsgrundlage:
**Ansatz 95-A** (RKI-Expositions-Wirkungs-Funktion, bottom-up; Entscheidungslog Nr. 1)

> **Revisionsstand.** Rev. 8 = Fortschreibung nach der Integration (30.08.2026,
> Nutzer-Entscheid + Fortschreibung der Aufgabe v2 vom 30.08.2026): (1) die
> **Ressourcen-Regel** (§3.4 der Aufgabe) ersetzt den früher vorgesehenen
> nationalen 100-m-Zell-Lauf als finalen Abgleich durch **kommunale
> Stichproben-Abgleiche** (Log 34); (2) die **Datenebenen-Anlagepflicht** (§3.1
> der Aufgabe) — die q_pfl-Ebene ist vollständig als „neu anzulegen"
> spezifiziert, q_1P als „geparkt" mit Watchlist (Log 35, §3.6); (3) die
> \(\bar L_{85+}\)-Approximation (Befund 22) ist durch die **exakte
> sterbefallgewichtete Rechnung** ersetzt: 4,16 J statt 5,44 J (Log 36, §3.5,
> Anlage `l85_sterbefallgewichtung.md`). Rev. 7 = Auflösung der §6-Eskalation aus Rev. 6 (Kalibrier-
> Prüfstein) über die in §4 benannte keyless Messung — bevölkerungsgewichtete
> Kalibrier-Zeitreihen (Gemeindepunkt × Zensus-Bevölkerung) statt Flächenmittel — plus
> Holdout-Nachschätzung der Süd-ERF; Entscheidungslog Nr. 31–33. Rev. 6 = Migration des
> #95-Anteils von M0 Rev. 5
> (`docs/render/METHODIK_M0_GESUNDHEIT.html`) in das §4-Format **plus** Abarbeitung der
> Befunde aus `reviews/Gegenpruefung_Rev5_Befundliste.md`; Status je Befund in
> `reviews/BEFUNDE_95.md`. Diese Markdown-Datei ist die Quelle für #95 (§2.7).
> Alle Ermessensentscheidungen im **Entscheidungslog** (Ende der Datei).
> Anlagen: `backend/scripts/kalibrierung/` (Rev. 5: `calibrate_heat_mortality.py`,
> Rev. 6: `calibrate_heat_mortality_rev6.py`, Rev. 7: `calibrate_heat_mortality_rev7.py`)
> + `backend/data/kalibrierung/` (`c_kal_rev7_ergebnis.md`, `c_kal_rev7_verteilung.csv`,
> `sommermittel_bundesland_povw.csv`, `temperatur_offsets_bundesland.csv`,
> `wochenquantile_region.csv`; Rev.-6-Stände bleiben zur Reproduzierbarkeit).

## 1 Wirkungskette & Knoten-Bilanz (§2.1)

Kette laut Arbeitsmappe (Sheet „Klimawirkungsketten" Z405, Knoten **W182**; Konfidenz mittel —
containerweiter Sensitivitätspfeil). Rollen/Kanten: Sheet „Schadensbaum-Netzwerkliste" Z96
(Id 95): **Buchungsobjekt — Ebene A**, Handlungserfordernis **sehr dringend**. Die
Knoten-Treue wurde in der Gegenprüfung (Durchgang 3) direkt gegen die xlsx bestätigt,
einschließlich der Netzwerklisten-Kante **#63 → #95**.

### Knoten-Bilanz

| Knoten | Name | rechnet in | Wo (Formel/Ebene) | falls inaktiv: Begründung |
|---|---|---|---|---|
| E02 | Hitze | Schicht A + B | \(\bar T_{\text{Zelle}}, T_w\), HD; Ebene HEAT_WAVE | — |
| W124 | Stadtklima/Wärmeinseln (#62; 0 € per R2) | Schicht A + B | UHI-\(\Delta T\) der Zelltemperatur (§3.1), mittelwerttreu; Komponenten-Mapping s. u. | — |
| W123 | Innenraumklima (#63; Treiber 0 €) | teilweise Schicht B / bewusst inaktiv als eigener Knoten | Nachtkomponente des 24-h-Mittels (fehlende nächtliche Auskühlung) treibt die Innenraum-Belastung; zusätzlich Hebel S157 | eigenes Risiko mit Gebäudephysik folgt in Stufe M1 (Log Nr. 11) |
| S152 | Altersstruktur | Schicht B + Maßnahmen-Hebel | \(\text{pop}_a\), \(f_a\), \(m_a\); Isolationsanteil \(q_{\text{1P}}\); Maßnahmen-Hebel \(\delta_{\text{VG}}\) (§5, Befund 127): Die Schutzprogramme wählen ihre Zielgruppe nach dem Alter (ab 75) aus und wirken auf die Bänder 75–84 und 85+, deshalb docken sie am Knoten der Altersstruktur an; einen eigenen Knoten für vulnerable Gruppen führt Kette W182 nicht | — |
| S153 | Vorerkrankungen / individuelle Sensitivität | Schicht B (teilweise) | Pflegeheim-Term \(\beta_{\text{pfl}}\) (nur Band 85+) | Kreis-Prävalenzen (Zi/GEDA) und GISD-Deprivation: Sensitivitätsband (Log Nr. 14) |
| S154 | Freizeitverhalten | bewusst inaktiv | — | exertional heat illness (junge Erwachsene) überwiegend ambulant; dokumentiert, nicht modelliert (Log Nr. 15) |
| S155 | Gefahrenbewusstsein | Maßnahmen-Hebel | \(\delta_{\text{HAP}}\)-Kette (mit S158) | — |
| S157 | Verfügbarkeit gekühlter Aufenthaltsräume | Maßnahmen-Hebel | Klimaanlagen-Effekt rOR ≈ 0,93 [46], als Exzessfaktor \(g_{\text{S157}}\) auf den Exzess 85+ der Heimbewohner im gekühlten Anteil \(s_{\text{gek}}\) (Voreinstellung 0,11, §5); öffentliche Kühlzentren über \(\delta_{\text{KZ}}\) auf den Exzess der Bänder 75–84 und 85+ außerhalb der Heime (§5); R7-Weiche §5 | — |
| S158 | Monitoring / Frühwarnsysteme | Maßnahmen-Hebel + implizit im Basiswert | \(\delta_{\text{HAP}}\); Warnwirkung der Kalibrierjahre steckt in \(c_{\text{kal}}\) (Doppelzählungs-Wächter, §5) | — |
| R35 | Vorkommen von Bevölkerung | Schicht A + B | \(\text{pop}_a\) (Zensus 2022, 100 m) | — |
| R36 | Vorkommen von Gesundheitsinfrastruktur | Screening + Sensitivitätsband | Ebene HEALTHCARE_ACCESS (Schicht A); \(\beta_d\) als dokumentiertes Sensitivitätsband, nicht im Basiswert (Log Nr. 20) | Basiswert: Nicholl-Evidenz misst transportierte Notfälle — Hitzetote sterben überwiegend zu Hause; Übertragbarkeit zu schwach für den Absolutwert (§3.2: unbelegte Modulatoren Default 1) |

**W124-Komponenten-Mapping** (Befund 54): Albedo × Versiegelung → S100 Versiegelung;
Gebäudemasse/-höhe, Straßenschluchten (1−SVF) → S094 Baumaterialien/Bauform; Grün/Wasser/
Baumkronen → W127 Vegetation in Siedlungen; Durchlüftung (vent_score) → Zirkulationsanteil
des Containers; E19 Sonnenscheindauer: implizit im DWD-Temperaturraster enthalten, nicht
separat modelliert; S095–S099 wirken über die genannten physischen Komponenten (Vorsorge-/
Zustandsgrößen, nicht separat parametrisiert). W124 ist vorgelagert (0 € per R2) und
produktseitig implementiert.

KWRA-Indikatoren (intensive Betrachtung „Hitzebelastung älterer, alleinstehender Personen"):
GE-KL-01/02 (Hitzeperioden), BAU-KL-05 (UHImax), GE-SO-03/04/05 (Bevölkerung, 65+),
GE-SO-06 (Einpersonenhaushalte).

### Weitergaben (zweispaltig; Quelle: Netzwerkliste + Abgleich-Protokoll)

| Output-Kanten (Abgleich-Protokoll) | Konto-Ausschlüsse / verwandte Buchungen (K1-Definition) |
|---|---|
| → **#87** Leistungseinbußen von Beschäftigten (K2) — **P8** (AP Z12); Produktivitätsverluste folgen in Stufe M3 | Systemvorhaltung → K8 via **ID 102** (K1-Definition; keine Kante von #95 — einzige Eingangskante von #102 ist #49) |
| → **#101** Verletzungen und Todesfälle infolge von Extremereignissen (K1, Ursache Extremereignisse) — **P47** (AP Z146). **Partitionszitat** (ID 101, Blattzeile 106, Spalte „Nicht enthalten"): „**Hitzetote (ID 95)**" — jeder Todesfall zählt genau einmal (R9) | Kühlkosten → **ID 65** (K8) über die **R7-Weiche des Treibers #63**: „100-%-Regel je Raumbestand: gekühlte Flächen buchen Kühl-Mehrkosten (K8, ID 65); ungekühlte Flächen buchen verbleibende K1-/K2-Schäden" — keine Weitergabe von #95 |

### Konto-Einbettung

- **Konto:** K1 Gesundheit, **Ursache: Hitze** (R9-Partition); Bausteine K1-Mortalität +
  K1-Morbidität (Risiken-Monetarisierung, ID 95 = Blattzeile 100). Mortalitäts-Bewertung: **YLL × VOLY**,
  also verlorene Lebensjahre × Wert eines verlorenen Lebensjahres (MK 4.0; Log Nr. 2). YLL (englisch „years
  of life lost“) zählt je Hitzetoten die Jahre, die er nach der Sterbetafel im Mittel noch gelebt hätte
  (§3.3). VOLY (englisch „value of a life year“) ist der Eurobetrag für ein solches Jahr, hier 160.800 €
  (Preisstand 2024, §3.5). Die Monetarisierungs-Arbeitsmappe wurde entsprechend fortgeschrieben
  und die Änderung im Abgleich-Protokoll dokumentiert (Befund 50; Punkt P-neu s. Ledger).
- **Anzuwendende Rechenregeln:** R7 (Weiche gekühlte Räume, §5), R9 (Ursachenpartition).
- **Nur K1 aktiv (M0):** bewusst als Untergrenze (Begriff definiert in §4); K2 (#87) ab M3,
  K8 (#102, #65) ab Stufe M5 — nichts geht verloren, nichts wird doppelt gezählt.

### Risiko ohne (weitere) Anpassung

**KWRA-Stufe „ohne Anpassung“.** Die KWRA 2021 stuft die Klimawirkung „Hitzebelastung“ ohne (weitere)
Anpassung so ein: Gegenwart **hoch**; Mitte des Jahrhunderts (2031–2060) im optimistischen Fall **mittel**,
im pessimistischen Fall **hoch**; Ende des Jahrhunderts (2071–2100) im optimistischen Fall **mittel**, im
pessimistischen Fall **hoch**. Fundstelle: `docs/KWAR/KWRA-2021_Klimawirkungen.xlsx`, Blatt `Klimawirkungen`,
Zeile 97 (ID 95), Spalten N–R (Kopfzellen N2 „Risiko o. Anp. – Gegenwart“ bis R2 „Risiko o. Anp. – Ende
pessim.“); gleichlautend in Teilbericht 6, Tabelle 1, S. 41 [68].

**Gewissheit der KWRA-Bewertung.** Mitte des Jahrhunderts **hoch**, Ende des Jahrhunderts **mittel**
(dieselbe Zeile 97, Spalte S „Gewissheit – Mitte“ und Spalte T „Gewissheit – Ende“; gleichlautend in [68],
Tabelle 1, S. 41). Für die Gegenwart nennt die KWRA keine Gewissheit. Teilbericht 6 rechnet die vier Stufen
in Zahlen um (1 = sehr gering, 2 = gering, 3 = mittel, 4 = hoch; [68], S. 78, Fußnote 18); für die
Hitzebelastung ergibt das im Mittel beider Zeitscheiben (4 + 3) / 2 = 3,5. Damit zählt [68] auf S. 78–79
die Hitzebelastung zu den Klimawirkungen mit vergleichsweise hoher Gewissheit (gemittelter Wert 3,5 über
beide Zeitscheiben). Mappe und Teilbericht stimmen überein; die Vorrangregel der Aufgabe muss nicht
angewendet werden. **Warum die eigene Quellenlage davon abweicht:** Die KWRA bewertet, wie sicher die
Einstufung des *künftigen* Risikos in eine von drei Stufen ist, und hängt damit an Klimaprojektionen und an
der künftigen Bevölkerung; dieser Bericht rechnet das *heutige* Klima (§6) aus gemessenen Größen — den vom
RKI geschätzten Hitzetoten 2012–2024 und amtlichen Bevölkerungs- und Sterbezahlen — und weist seine
Unsicherheit deshalb nicht als Stufe aus, sondern als Band je Parameter (Kapitel 7), etwa beim
Kalibrierfaktor \(c_{\text{kal}}\) 0,55–0,67 um 0,581 (§4).

**(a) Zuordnung der Zahlen.** Alle in diesem Bericht ausgewiesenen Zahlen des Basiswerts —
zusätzliche Sterbefälle, YLL, Morbiditätsfälle und die daraus bewerteten Euro-Beträge in K1 — gehören
zum KWRA-Zustand **„Risiko ohne (weitere) Anpassung"**. Gemeint ist der heutige Anpassungsstand ohne
zusätzliche Maßnahmen. Er steckt im Basiswert über die Kalibrierung: \(c_{\text{kal}}\) ist an die vom RKI
geschätzten Hitzetoten der Jahre 2012–2024 angepasst (§4). Was in diesen Jahren an Anpassung schon wirkte,
etwa das laufende Hitzewarnsystem des DWD [45], ist damit im Niveau des Basiswerts enthalten
(Doppelzählungs-Wächter, §5). Weitere Maßnahmen sind im Basiswert nicht enthalten.

**(b) Zustand „mit Anpassung".** Dargestellt wird er nur als Wirkung einzelner Maßnahmen-Hebel auf den
Basiswert (§5): Hitzeaktionsplan und Frühwarnkette über \(\delta_{\text{HAP}}\), gekühlte Räume in
Pflegeheimen (S157) über \(g_{\text{S157}}\) auf den Exzess der Heimbewohner ab 85, öffentliche Kühlzentren
(ebenfalls S157) über \(\delta_{\text{KZ}}\) und Schutzprogramme für vulnerable Gruppen (Knoten S152) über
\(\delta_{\text{VG}}\), beide auf den Wochenexzess der Bänder 75–84 und 85+, beim Band 85+ nur außerhalb der Heime
(Befunde 122–128, 139). Im Produkt entsteht daraus der Wert „mit Anpassung" erst, wenn eine Kommune
Maßnahmen wählt. Ein KWRA-Restrisiko „mit Anpassung" als eigene Zahl weist der Bericht nicht aus; auch
die spontane Anpassung der Bevölkerung (abflachende Expositions-Wirkung über die Dekaden) ist nicht
modelliert, sondern als Modellgrenze in §6 geführt.

## 2 Evidenz-Register (§2.2)

Risikoübergreifend wiederverwendbare Zeilen zusätzlich in `docs/evidenz/register.md`.
Nur Zeilen mit Entscheidung **Basiswert** kommen in den Formeln (§3) vor. Spalte „E-Regel":
die §2.8-E-Regeln sind in der Aufgabe noch nicht definiert (Lücken-Vermerk §2.8) — die
Spalte verweist auf die Entscheidungslog-Nummer.

| Register-ID | Knoten → Outcome | Effektgröße | Studientyp | Quelle | Übertragbarkeit | Datenlage je Zelle | Entscheidung | E-Regel |
|---|---|---|---|---|---|---|---|---|
| 95-E02-01 | E02 Hitze → Mortalität | RR-Kurve: \(T_0\) 19,7/20,2/20,8 °C; \(\beta_{85+}\) 0,0634/0,0625/0,0531 K⁻¹ (N/M/S) | amtliche Statistik / publizierte ERF | Winklmayr 2022, Abb. 3 [11] | DE 1992–2021, 3 Regionen; Skalentransfer Region→Zelle als Modellgrenze (§6) | Zelltemperatur (DWD 1 km + UHI) | **Basiswert** | Log 1 |
| 95-E02-02 | E02 Hitzetage → Einweisungen | konditional +2,4 %/Hitzetag (+1,408/100.000·Tag); unkonditional +5,4 % | quasi-experimentell (Panel, 170 Mio. Fälle) | Karlsson & Ziebarth 2018 [18], IZA-DP 7875 Tab. 1 [62] | DE 1999–2008; Alterstabelle nicht publiziert (top-kodiert > 75) | DWD hot_days (§3.4) | **Basiswert** (konditional; Log 19) | Log 19 |
| 95-W124-01 | W124 Stadtklima → Zelltemperatur | UHI-\(\Delta T\), mittelwerttreu je 1-km-Zelle | Modell (OSM/SVF-Stadtmodell, produktseitig implementiert) | §3.1; Produktdoku | DE-weit, 100 m | vorhanden | **Basiswert** | Log 12 |
| 95-W123-01 | W123/#63 Innenraumklima → Mortalität | über Nachtkomponente des 24-h-Mittels abgebildet | Modellannahme | M0 Rev. 5 Kap. 2 | — | (24-h-Zelltemperatur) | **bewusst inaktiv** als eigener Knoten (bis M1) | Log 11 |
| 95-S152-01 | S152 Altersstruktur → Mortalität | \(f_a\) = 0,357/0,588/0,631/1,0 (Rückrechnung §3.3a); \(m_a\); \(\bar L_a\) | amtliche Statistik + Rückrechnung | RKI [12]; Destatis [48,49] | DE; Rückrechnungskette vollständig in §3.3a | Zensus-2022-Altersbänder | **Basiswert** | Log 22 |
| 95-S152-02 | S152/GE-SO-06 soziale Isolation → **Mortalität** | OR ≈ 2,3 „allein lebend" ⇒ \(\beta_{\text{iso}}\) = 0,90 (zentriert, \(\bar q\) = 0,346) | Fall-Kontrolle (als Vulnerabilität, nicht als Maßnahme) | Semenza 1996 [40]; Mikrozensus 2023 [63] | Chicago 1995 (Todesfälle); für Einweisungen keine Evidenz → F-Pfad Default 1 (Log 28) | Zensus-2022-Haushaltsgitter; Fallback §3.6 | **Basiswert** (Bänder 65+, nur D-Pfad) | Log 21/28 |
| 95-S153-01 | S153 Pflegebedürftigkeit/Heim → Mortalität | OR Heim vs. Nicht-Heim 3,0 (2,2–6,0) ⇒ \(\beta_{\text{pfl}}\) = 1,54 (Kette §3.3b) | Kohorte (Fouillet), Meta (Bouchama, Stütze), Klenk (ERF im Heim-Setting) | [41,44,60,61] | F 2003 / DE; Kette vollständig in §3.3b | OSM-Pflegeeinrichtungen × Pflegestatistik (Proxy, Fallback §3.6) | **Basiswert** (nur D-Pfad, nur Band 85+) | Log 23 |
| 95-S153-02 | S153 Vorerkrankungs-Prävalenzen (Kreis) → Mortalität | Zi-Versorgungsatlas/GEDA, zentriert | amtliche Statistik/Survey | M0 Rev. 5 (geprüfter Kandidat) | Kreisebene (gröber als Zelle) | Kreis | **Sensitivitätsband** | Log 14 |
| 95-S153-03 | S153 sozioökonomische Deprivation → Mortalität | GISD (RKI, Gemeindeebene) | Index | M0 Rev. 5 | Gemeindeebene | Gemeinde | **Sensitivitätsband** | Log 14 |
| 95-S153-04 | S153 Heim → Hospitalisierung | OR 0,96 [0,67–1,36] n. s. — **kein** Effekt | Case-Crossover (Flandern, 10 Heime) | [64] | Gegenevidenz: Heimbewohner versterben vor Ort statt Einweisung | — | **bewusst inaktiv** (β_pfl nicht im F-Pfad) | Log 24 |
| 95-S154-01 | S154 Freizeitverhalten → Morbidität (exertional) | zweite Fallspitze junger Erwachsener; überwiegend ambulant | Beschreibung [16,18] | M0 Rev. 5 | — | — | **bewusst inaktiv** | Log 15 |
| 95-S155-01 | S155 Gefahrenbewusstsein → Mortalität | Bestandteil der Warn-/Verhaltenskette (\(\delta_{\text{HAP}}\)) | Interventions-/quasi-exp. Evidenz | [45,47] | Städte-DiD DE; Europa-Review | kommunal | **Maßnahmen-Hebel** | Log 10 |
| 95-S152-03 | Schutzprogramme vulnerable Gruppen → Mortalität und Einweisungen 75+ | \(\delta_{\text{VG}}\) 0,931 (0,794–1,0) auf den Wochenexzess 75–84 und 85+ ohne Heimbewohner; auf die Einweisungen derselben Bänder \(\delta_{\text{VG,morb}}\) 1,0 (0,931–1,069) | Abschätzung von KAP3 aus Paketwirkung (Ländervergleich, Obergrenze; Kappung 0,794 (0,743–0,842) als eigener Block) und quasi-experimentellem Vergleich (Wirkung bei Erreichten); Doppelzählungs-Wächter mit Voreinstellung „nein“ aus der Verbreitung kommunaler Hitzeaktionspläne | [47], [70], [76] | Europa 1990–2019; Rom 2015 | kommunal | **Maßnahmen-Hebel** (abgeschätzt, §5) | Log 43 |
| 95-S157-01 | S157 gekühlte Räume → Mortalität (Heime) | rOR ≈ 0,93 (0,87–0,99) an Extremhitzetagen ⇒ Exzessfaktor \(g_{\text{S157}}\) 0,29; gekühlter Anteil der Heimplätze \(s_{\text{gek}}\) voreingestellt 0,11 (0,05–0,15) | Case-Crossover (Ontario, 73.578 Todesfälle); Anteil gekühlter Heime aus Umfrage und Baustatistik | [46], [71], [72] | Ontario 2010–2023; Deutschland 2025/2026 | Heim-Ebene; \(s_{\text{gek}}\) für die ganze Kommune | **Maßnahmen-Hebel** (R7-Weiche §5) | Log 10, 45 |
| 95-S157-02 | S157 öffentliche Kühlzentren → Mortalität 75+ außerhalb der Heime | \(\delta_{\text{KZ}}\) = 1 − \(r_{\text{KZ}} \times w_{\text{KZ}}\) = 1 − 0,05 × 0,71 × 3/24 = 0,9956 (0,982–0,9994) | Abschätzung von KAP3: Klimaanlagen-Effekt [46] × Dauer der Kühlwirkung aus einer Laborstudie [73]; Plausibilisierung an der Fall-Kontroll-Meta-Analyse [41] | [41], [46], [73] | eine Studie, die die Wirkung von Kühlzentren auf die Sterblichkeit misst, hat KAP3 nicht gefunden (Suche 27.09.2026); Übertragung aus Heimen und Labor | kommunal | **Maßnahmen-Hebel** (abgeschätzt, §5) | Log 46 |
| 95-S158-01 | S158 Frühwarnsysteme → Mortalität | DiD 15 dt. Städte: RR 1,00 [0,98–1,01]; adjustiert 0,85 [0,75–0,97]; Europa: HAF-Reduktion 25,2 % [19,8–31,9] (Einführungseffekt [47], Befund 68) | quasi-experimentell | [45,47] | DE/Europa; im Basiswert der Kalibrierjahre enthalten | kommunal | **Maßnahmen-Hebel** (\(\delta_{\text{HAP}}\) = 0,95, marginal) | Log 10 |
| 95-R35-01 | R35 Bevölkerung → Exposition | \(\text{pop}_a\) je Zelle | amtliche Statistik | Zensus 2022 (100-m-Gitter) | DE-weit | vorhanden | **Basiswert** | Log 1 |
| 95-R36-01 | R36 Gesundheitsinfrastruktur → Mortalität | +≈1 % Mortalität je +10 km KH-Distanz (transportierte Notfälle) | Beobachtung | Nicholl 2007 [38]; Hilfsfrist [39] | UK; Hitzetote sterben überwiegend zu Hause — Übertragbarkeit zu schwach für den Basiswert | HEALTHCARE_ACCESS-Distanz | **Sensitivitätsband** (Basiswert-Default 1) | Log 20 |

## 3 Modell (§2.3) — Ansatz 95-A, Schicht B

**Native Ergebnisgröße (§3.6, deklariert): verlorene Lebensjahre (YLL) je Jahr.**
Teil-Ausweise unter der KWRA-Klammer: hitzebedingte Todesfälle \(D\), Erkrankungsfälle \(F\)
(Morbidität), €.

**Gemeinsamer Preisstand aller Kostensätze dieses Berichts: €2024** (Befund 23);
Umrechnungsfaktoren je Satz in der Zeichentabelle (Destatis-VPI-Jahresmittel, 2020 = 100:
2023 = 116,7 · 2024 = 119,3 [19]).

### 3.0 Rechenkette

Die Rechenkette erzählt die Methodik von der amtlichen Quelle bis zum Euro-Betrag am Beispiel
einer Kommune. Die Formeln in 3.1–3.5 sind die genaue Fassung derselben Kette und keine zweite
Methodik; alle Parameter sind die Werte aus Kapitel 7. **Beispielkommune: Berlin** (Gemeinde
11000000, Land Berlin, damit ERF-Region Mitte nach §3.2). Temperatur und Hitzetage stammen aus
der 1-km-Rasterzelle Berlin-Mitte (52,520 °N, 13,405 °E), abgegriffen mit denselben
Produktfunktionen wie im Produkt (`dwd_cdc_grid.summer_mean_temp_at`, `hot_days_at`: Mittel der
zehn jüngsten verfügbaren Jahre, Abruf 25.09.2026).

| Ebene | Rechenschritt | Wert (Beispielkommune Berlin) | Quelle |
|---|---|---|---|
| 1 | Einwohner je Altersband \(\text{pop}_a\) (u65 · 65–74 · 75–84 · 85+) | 2.961.430 · 339.490 · 253.528 · 107.933 | Fortschreibung des Bevölkerungsstandes, Stichtag 31.12.2023, Basis Zensus 2022, Tab. 12411-09-01-4-B [48]; Anlage `bevoelkerung_bundesland_altersband.csv` (Befund 99) |
| 2 | Sommermittel der Temperatur \(\bar T\) (Juni–August, 24-h-Mittel) | 20,07 °C | DWD-CDC-Raster air_temperature_mean, 1 km [33] |
| 3 | Schwelle und Steigung der Region Mitte: \(T_0\); \(\beta_a = \beta_{85+} \times f_a\) | \(T_0\) = 20,2 °C; \(\beta_{85+}\) = 0,0625 K⁻¹ × \(f_a\) 0,357 · 0,588 · 0,631 · 1,0 = 0,0223 · 0,0368 · 0,0394 · 0,0625 K⁻¹ | Winklmayr 2022 [11] (§3.3); \(f_a\) Rückrechnung §3.3a [12,49] |
| 4 | Wochenexzess: 13 Sommerwochen \(T_w = \bar T + q_w\), je Woche Übersterblichkeit \(e^{\beta_a (T_w - T_0)_+} - 1\), summiert | 6 von 13 Wochen über 20,2 °C (20,58–24,67 °C); Summe 0,289 · 0,486 · 0,524 · 0,860 | Wochenquantile Mitte, Tabelle §3.2 [33,50] |
| 5 | Basissterbefälle je Woche: \(\text{pop}_a \times m_a / 100.000 / 52\) | \(m_a\) 213,2 · 1.737,9 · 4.812,3 · 14.800,2 je 100.000 ⇒ 121,4 · 113,5 · 234,6 · 307,2 Sterbefälle je Woche | Sterbefälle 2023 [49] (§3.5) |
| 6 | Zusätzliche Sterbefälle \(D_a\) = \(c_{\text{kal}}\) × \(v_{\text{vers},a}\) × Ebene 5 × Ebene 4 | 0,581 × 1 × … = 20,4 · 32,0 · 71,4 · 153,6 = **277,4 Todesfälle je Jahr** | \(c_{\text{kal}}\) Kalibrierung §4 [50]; \(v_{\text{vers}}\) §3.3 |
| 7 | Verlorene Lebensjahre: \(\text{YLL} = \sum_a D_a \times \bar L_a\) | \(\bar L_a\) 23,39 · 15,59 · 8,90 · 4,16 J ⇒ 476,3 + 499,5 + 635,4 + 638,8 = **2.250 YLL je Jahr** (native Ergebnisgröße) | Sterbetafel 2022/2024 [48], Sterbefälle 2023 [49] (§3.5) |
| 8 | Mortalität in Euro: YLL × VOLY | 2.250 × 160.800 € = 361,8 Mio. € (Preisstand 2024) | VOLY-Kette §3.5 [19] |
| 9 | Morbidität: Fälle \(F = \sum_a \text{pop}_a \times r_{0,a} / 100.000 \times [1 + e_{\text{HD}} (\text{HD} - \text{HD}_{\text{ref}})]\), dann × \(c_{\text{Fall}}\) | HD = 17,5 Tage; Faktor 1 + 0,024 × (17,5 − 7,2) = 1,247; \(r_{0,a}\) 1,9 · 6,3 · 10,8 · 15,6 ⇒ 70,2 + 26,7 + 34,2 + 21,0 = 152,0 Fälle × 7.152 € = 1,09 Mio. € (Preisstand 2024) | hot_days-Raster [33]; K&Z [18,62]; \(c_{\text{Fall}}\) [17,19] (§3.4, §3.5) |
| 10 | Bewerteter Schaden (Konto K1) je Jahr = Mortalität + Morbidität | 361,8 Mio. € + 1,09 Mio. € = **362,9 Mio. € je Jahr (Preisstand 2024)** | Ebenen 8 und 9 |

**Stärkster Treiber** ist die Temperatur: Ist der Sommer in Berlin 0,5 K kühler, sinkt der Betrag
um 23 %, ist er 0,5 K wärmer, steigt er um 27 %. Danach folgen das Band 85+ (55 % der Todesfälle)
und der Kalibrierfaktor \(c_{\text{kal}}\), der den Betrag im selben Verhältnis skaliert.

**Wo die Kette zusammenfasst und was eine gröbere Rechnung verfälschen würde:**

- **Ebene 4, Wochen statt Sommermittel.** Mit dem Sommermittel allein (20,07 °C liegt unter der
  Schwelle 20,2 °C) käme für Berlin null heraus, also −100 %. Die Hitzetoten entstehen in den
  sechs heißen Wochen; deshalb rechnet die Kette jede der 13 Sommerwochen einzeln. Der Teiler 52
  ist keine Vereinfachung: Die 39 Wochen außerhalb des Sommers tragen nach dem Modell nichts bei.
- **Ebenen 1, 2 und 6, eine Zelle statt aller Zellen: Die Kette überschätzt Berlin um rund
  6 %.** Das Produkt rechnet jede 100-m-Zelle mit ihrer eigenen Temperatur (§3.1) und ihrer
  eigenen Bevölkerung aus dem Zensus-Gitter und summiert. Die Kette setzt für die ganze Kommune
  die Zelle Berlin-Mitte und die Fortschreibung aus Ebene 1 an. Die Zelle Berlin-Mitte ist
  praktisch der Gemeindepunkt der Kalibrierung (§4): Dessen Reihe in
  `sommermittel_bundesland_povw.csv` [50] ergibt für die Sommer 2016–2025 im Mittel 20,06 °C.
  Nachgerechnet mit allen 40.669 bewohnten 100-m-Zellen innerhalb der Gemeindegrenze Berlins
  aus VG250 [65] (Zensus 2022, Gitterdaten [67]), jede mit ihrem Wert aus dem 1-km-Raster [33]
  und ihrer Bevölkerung nach der Logik des Produkts
  (`zensus_loader.apply_zensus_to_cell_inputs`: Einwohner × Anteil 65+, Aufteilung der 65+ aus
  den 5er-Jahresgruppen), ergeben sich vier Wirkungen, jede auf die vorige gerechnet.
  Die Rechnung liegt als Skript `docs/methodik/anlagen/95_zellvergleich.py` bei; Aufruf für Berlin:
  `python3 docs/methodik/anlagen/95_zellvergleich.py --gemeinde 11000000`
  (lädt Zensus-Gitter, DWD-Raster und VG250 in einen Cache außerhalb des Repos; mit
  `--gemeinde` und einem anderen Gemeindeschlüssel für jede Kommune):
  (a) **Temperatur je Zelle: × 0,948.** Das Bevölkerungsmittel liegt bei 19,96 °C, also 0,11 K
  unter Berlin-Mitte (Zellen 19,38–20,38 °C); drei Viertel der Einwohner wohnen kühler als
  Berlin-Mitte.
  (b) **Einwohnersumme: × 0,981.** Das Zensus-Gitter (Stichtag 15.05.2022) zählt in Berlin
  3.593.357 Einwohner, die Fortschreibung aus Ebene 1 (Stichtag 31.12.2023) 3.662.381
  (Befund 99).
  (c) **Altersbänder je Zelle wie im Produkt ohne Gemeindeschlüssel: × 0,984 = 0,9888 × 0,9948.** Der erste Faktor,
  ohne gegen mit Gemeindeschlüssel, ist die Modellgrenze aus §3.3: In 4.774 Zellen mit 99.098 Einwohnern ist
  der Anteil 65+ im Gitter geheimgehalten („–“); ohne Gemeindeschlüssel rechnet das Produkt dort nur Stufe 1 (Befund 141).
  Gemessen ist er gegen die Ersatzregel aus §3.3 (Stufe 1 und 2, ohne (d)); gerundet ist es
  derselbe Faktor wie dort in der Tabelle (× 0,989, dort mit (d); Befund 121). Der zweite Faktor,
  der Rest, ist das, was die Altersbänder je Zelle nach dieser Regel gegenüber (b) ändern: wie
  alt die Einwohner im Gitter sind und in welchen Zellen die Älteren wohnen; er senkt den Betrag
  um 0,5 %.
  (d) **Wärmeinsel-Feinstruktur unter 1 km: × 1,021.** Modellrechnung mit derselben gesetzten
  Streuung σ = 0,5 K wie in §4, keine Messung; die gekrümmte Kurve hebt die Summe.
  Zusammen 0,948 × 0,981 × 0,984 × 1,021 = 0,934: Ohne Gemeindeschlüssel ergibt der Zelllauf für Berlin
  rund 339 Mio. € je Jahr (Preisstand 2024); mit Gemeindeschlüssel, also mit der ganzen Ersatzregel, sind es
  rund 343 Mio. € (342,67 Mio. €, Tabelle in §3.3), 6 % weniger als die Kette. Die
  Kette zeigt den Rechenweg, der Betrag für Berlin ist der Zelllauf des Produkts mit Gemeindeschlüssel. Die Wirkungen
  (a) und (d) zusammen (× 0,967, aus den ungerundeten Faktoren) zeigen, dass das Zellmodell für Berlin unter dem Gemeindepunkt liegt; der Berlin-Anker
  in §4 rechnet damit (Befund 101).
- **Ebene 6, \(v_{\text{vers},a}\) = 1.** Auf Ebene der Kommune ist der Modifikator genau 1:
  \(\beta_{\text{iso}}\) wirkt heute nicht, weil \(q_{\text{1P}}\) mangels Zellquelle gleich dem
  Bundesmittel gesetzt ist (§3.6), und die Ebene \(q_{\text{pfl}}\) verteilt die Heimbewohner
  erwartungstreu auf die Zellen der Kommune. Innerhalb der Kommune verschiebt \(\beta_{\text{pfl}}\)
  nur, *wo* die Todesfälle anfallen. Abweichen kann die Zellsumme nur, wenn Heime systematisch in
  wärmeren oder kühleren Zellen liegen, und durch die Kappung bei 1 (nur abwärts). **Abschätzung
  von KAP3** für den Extremfall, dass alle Heimbewohner in Zellen 1 K über dem Mittel der Kommune
  wohnen und alle übrigen Menschen ab 85 am Mittel der Kommune: Heimzellen haben \(q_{\text{pfl}} = 1\) und damit
  \(v = 1 + 1{,}54 \times (1 - 0{,}149) = 2{,}31\), die übrigen \(q_{\text{pfl}} = 0\) und
  \(v = 1 - 1{,}54 \times 0{,}149 = 0{,}77\). Die Heimbewohner tragen also
  0,149 × 2,31 = 0,344 der Todesfälle 85+, die übrigen 0,851 × 0,77 = 0,656. Um 1 K wärmer steigt
  der Wochenexzess 85+ von 0,860 auf 1,375, also × 1,598. Todesfälle 85+:
  0,344 × 1,598 + 0,656 = 1,206, also +20,6 %. Das Band 85+ trägt 638,8 von 2.250 YLL (28,4 %),
  auf den Betrag wirken daher 28,4 % × 20,6 % = +5,8 %. Das ist eine Obergrenze; im Normalfall
  liegen Heime nicht systematisch wärmer, und die Wirkung ist deutlich kleiner.

```python test: rechenkette_95
# Rechenkette 3.0, Beispielkommune Berlin (Region Mitte); Parameter unveraendert aus Kapitel 7
import math
q = [-4.59, -3.04, -2.27, -1.64, -1.12, -0.57, -0.04, 0.51, 1.05, 1.65, 2.32, 3.16, 4.60]
pop = [2_961_430, 339_490, 253_528, 107_933]          # Ebene 1 (12411-09-01-4-B)
t_mittel, t0, b85, c_kal = 20.07, 20.2, 0.0625, 0.581  # Ebenen 2, 3, 6
fa = [0.357, 0.588, 0.631, 1.0]
m = [213.2, 1737.9, 4812.3, 14800.2]
L = [23.39, 15.59, 8.90, 4.16]
r0 = [1.9, 6.3, 10.8, 15.6]
voly, c_fall, e_hd, hd, hd_ref = 160_800, 7_152, 0.024, 17.5, 7.2

def exzess(beta, t):                                    # Ebene 4
    return sum(math.exp(beta * max(0.0, t + qw - t0)) - 1 for qw in q)

def yll(t):
    d = [c_kal * 1.0 * p * mm / 100_000 / 52 * exzess(b85 * f, t) for p, mm, f in zip(pop, m, fa)]
    return d, sum(di * li for di, li in zip(d, L))

assert sum(1 for qw in q if t_mittel + qw > t0) == 6
for f, soll in zip(fa, [0.289, 0.486, 0.524, 0.860]):
    assert abs(exzess(b85 * f, t_mittel) - soll) < 0.001
for p, mm, soll in zip(pop, m, [121.4, 113.5, 234.6, 307.2]):
    assert abs(p * mm / 100_000 / 52 - soll) < 0.05     # Ebene 5
d, y = yll(t_mittel)
for di, soll in zip(d, [20.4, 32.0, 71.4, 153.6]):
    assert abs(di - soll) < 0.05                        # Ebene 6
assert abs(sum(d) - 277.4) < 0.05
assert abs(y - 2250) < 1                                # Ebene 7
eur_mort = y * voly
assert abs(eur_mort / 1e6 - 361.8) < 0.05               # Ebene 8
faktor = max(0.0, 1 + e_hd * (hd - hd_ref))
fall = [p * r / 100_000 * faktor for p, r in zip(pop, r0)]
assert abs(faktor - 1.247) < 0.001 and abs(sum(fall) - 152.0) < 0.05
eur_morb = sum(fall) * c_fall
assert abs(eur_morb / 1e6 - 1.09) < 0.005               # Ebene 9
assert abs((eur_mort + eur_morb) / 1e6 - 362.9) < 0.05  # Ebene 10
# Staerkster Treiber und E3-Aussagen
assert abs(yll(t_mittel - 0.5)[1] / y - 0.77) < 0.005
assert abs(yll(t_mittel + 0.5)[1] / y - 1.27) < 0.005
assert abs(d[3] / sum(d) - 0.55) < 0.01
assert sum(c_kal * p * mm / 100_000 * (math.exp(b85 * f * max(0.0, t_mittel - t0)) - 1)
           for p, mm, f in zip(pop, m, fa)) == 0.0    # nur Sommermittel => null
# Eine Zelle statt aller Zellen (Zelllauf Berlin, Messwerte aus dem Text): (a) x (b) x (c) x (d)
assert abs(3_593_357 / sum(pop) - 0.981) < 0.0005        # (b) Einwohnersumme Gitter / Fortschreibung
assert abs(0.9888 * 0.9948 - 0.984) < 0.0005             # (c) = ohne gegen mit Gemeindeschluessel x Rest (Befunde 121, 141)
gesamt = 0.948 * 0.981 * 0.984 * 1.021                   # Skript anlagen/95_zellvergleich.py
assert abs(gesamt - 0.934) < 0.001
assert abs((eur_mort + eur_morb) / 1e6 * gesamt - 339) < 1
assert abs((eur_mort + eur_morb) / 1e6 * gesamt / 0.9888 - 343) < 1  # mit Regel 3.3: 342,67 (Befund 145)
assert abs(0.948 * 1.021 - 0.967) < 0.001                # (a) x (d), Befund 101 (ungerundet 0,9674)
# (d) nachgerechnet am Punkt: sigma 0,5 K, mittelwerttreu, Gauss-Hermite-Mittel
zs = [-2.0201828705, -0.9585724646, 0.0, 0.9585724646, 2.0201828705]
ws = [0.0199532421, 0.3936193232, 0.9453087205, 0.3936193232, 0.0199532421]
uhi = sum(w * yll(t_mittel + 0.5 * math.sqrt(2) * z)[1] for z, w in zip(zs, ws)) / sum(ws)
assert abs(uhi / y - 1.02) < 0.003
# Heim-Extremfall (Abschaetzung von KAP3): alle Heimbewohner 1 K ueber dem Mittel der Kommune
v_heim, v_rest = 1 + 1.54 * (1 - 0.149), 1 + 1.54 * (0 - 0.149)
g_heim, g_rest = 0.149 * v_heim, 0.851 * v_rest
assert abs(v_heim - 2.31) < 0.005 and abs(v_rest - 0.77) < 0.005
assert abs(g_heim - 0.344) < 0.001 and abs(g_rest - 0.656) < 0.001
steig = exzess(b85, t_mittel + 1) / exzess(b85, t_mittel)
assert abs(exzess(b85, t_mittel + 1) - 1.375) < 0.001 and abs(steig - 1.598) < 0.001
d85 = g_heim * steig + g_rest
assert abs(d85 - 1.206) < 0.001
anteil85 = d[3] * L[3] / y
assert abs(anteil85 - 0.284) < 0.001
assert abs(anteil85 * (d85 - 1) - 0.058) < 0.001        # +5,8 % auf den Betrag
```

### 3.1 Zelltemperatur (vorgelagerter Knoten W124; produktseitig implementiert)

$$ T_{\text{Zelle}} \;=\; T_{\text{DWD}} \;+\; \bigl[\, \Delta T_{\text{UHI}} - \overline{\Delta T_{\text{UHI}}}^{\,1\,\text{km}} \,\bigr] \;-\; \gamma_h \cdot ( h - \bar{h} ) $$

| Zeichen | Name | Einheit | Wert/Herkunft |
|---|---|---|---|
| \(T_{\text{DWD}}\) | DWD-CDC-Rasterwert air_temperature_mean (Jun–Aug) | °C | DWD, 1 km |
| \(\Delta T_{\text{UHI}}\) | Stadtklima-Zuschlag der Zelle (OSM/SVF-Stadtmodell) | K | Produktmodell; register:95-W124-01 |
| \(\overline{\Delta T_{\text{UHI}}}^{1\text{km}}\) | Mittel der Zuschläge derselben 1-km-Zelle (Mittelwerttreue) | K | berechnet |
| \(h,\ \bar h\) | Geländehöhe Zelle bzw. 1-km-Mittel (DGM) | m | Geländemodell |
| \(\gamma_h\) | Standard-Temperaturgradient | K/m | 0,0065 (ICAO) |

Mittelwerttreue: Das DWD-Raster enthält die Wärmeinsel bereits teilweise; das Stadtmodell
verteilt nur die Feinstruktur unterhalb 1 km. Beispiel: DWD-Wert 21,0 °C, Zell-Zuschläge
+0,5…+2,5 K mit Mittel +1,5 K ⇒ die Zellen erhalten 20,0…22,0 °C (**Spanne ±1 K** um das
1-km-Mittel); das 1-km-Mittel bleibt exakt der DWD-Wert. Kein Doppelkanal —
Grün-/Baumkronenanteil steckt genau hier und ist **nicht** zusätzlich Vulnerabilität
(Log Nr. 12).

### 3.2 Wochenverteilung (empirische intra-saisonale Quantile; §3.2-Tails)

Herleitung (Rev. 5): je Region 7 Stationen × 30 Sommer (1991–2020) = 2.730 Wochen-Anomalien
(Wochenmittel − Sommermittel desselben Jahres), Quantile an \(p_w=(w-0{,}5)/13\). Befund der
Messung: Verteilung praktisch symmetrisch (Schiefe −0,003/−0,015/−0,089), entscheidend ist die
Streuung \(\sigma_{\text{intra}}\) = 2,36/2,58/2,57 K (frühere Setzung 2,0 K zu klein);
zwischenjährliche Streuung wird nicht verwendet. Restannahme: UHI verschiebt nur den
Mittelwert. Skript/Daten: `backend/scripts/kalibrierung/dwd_wochenquantile.py`,
`backend/data/kalibrierung/wochenquantile_region.csv` [33,50]. Rechengrundlage ist die Datei (vier Nachkommastellen,
Befund 144); die folgende Tabelle ist die auf zwei Stellen gerundete Lesehilfe, mit der auch die Rechenkette §3.0 rechnet.
Mit der Datei ergibt die Kette für Berlin 362,80 statt 362,89 Mio. €, der Zelllauf 342,58 Mio. € statt 342,67 Mio. €,
für Warmsen 172.957 € statt 173.099 € (`95_zellvergleich.py --wochenquantile produkt`); der Unterschied liegt unter
0,1 % und innerhalb der Toleranz aus §3.3.

| \(w\) | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| \(q_{w,\text{Nord}}\) [K] | −4,17 | −2,81 | −2,00 | −1,45 | −0,99 | −0,50 | 0,00 | +0,42 | +0,89 | +1,54 | +2,10 | +2,83 | +4,22 |
| \(q_{w,\text{Mitte}}\) [K] | −4,59 | −3,04 | −2,27 | −1,64 | −1,12 | −0,57 | −0,04 | +0,51 | +1,05 | +1,65 | +2,32 | +3,16 | +4,60 |
| \(q_{w,\text{Süd}}\) [K] | −4,67 | −2,99 | −2,23 | −1,65 | −1,11 | −0,57 | −0,03 | +0,51 | +1,12 | +1,75 | +2,36 | +3,18 | +4,46 |

$$ T_w \;=\; \bar{T}_{\text{Zelle}} + q_{w,\text{Region}}, \qquad w = 1,\dots,13 $$

**Regionen-Zuordnung** (Befund 3): Die ERF-Region (Nord/Mitte/Süd, Winklmayr) einer Zelle
folgt dem Bundesland ihres Standorts (VG250): Nord = HB, HH, MV, NI, SH · Mitte = BE, BB,
NW, RP, SL, HE, SN, ST, TH · Süd = BW, BY (identisch im Produktionscode
`health.REGION_BY_BUNDESLAND` und im Kalibrierskript). Der RKI-4-Zuschnitt
(Norden/Osten/Westen/Süden, EB 19/2025) wird **nur diagnostisch** in der Verteilungsprüfung
verwendet (§4): Norden = SH, HH, MV, NI, HB · Osten = BB, BE, SN, ST, TH · Westen = NW, HE,
RP, SL · Süden = BW, BY.

### 3.3 Mortalität (nativer Ausweis YLL)

$$ D_{a} \;=\; c_{\text{kal}} \cdot v_{\text{vers},a} \cdot \text{pop}_a \cdot \frac{m_a}{100\,000} \cdot \frac{1}{52} \sum_{w=1}^{13} \left( e^{\,\beta_a (T_w - T_{0,\text{Region}})_+} - 1 \right), \qquad \beta_a = \beta_{85+,\text{Region}} \cdot f_a $$

$$ \text{YLL}_{\text{Zelle}} \;=\; \sum_a D_a \cdot \bar{L}_a $$

**Bandweiser Modifikator** (Befunde 8/44 — je Faktor nur die Bänder seiner Evidenz):

$$ v_{\text{vers},a} \;=\; \bigl[ 1 + \mathbb{1}_{a \ge 65} \cdot \beta_{\text{iso}} ( q_{\text{1P}} - \bar q_{\text{1P}} ) \bigr] \cdot \bigl[ 1 + \mathbb{1}_{a = 85+} \cdot \beta_{\text{pfl}} ( q_{\text{pfl}} - \bar q_{\text{pfl}} ) \bigr] $$

| Faktor | Evidenz | wirkt auf Bänder | wirkt auf | Zentrierungsmittel |
|---|---|---|---|---|
| \(\beta_{\text{iso}}\) = 0,90 | Semenza 1996 (Ältere, Todesfälle) [40] | 65–74 / 75–84 / 85+ | nur \(D_a\) (F: keine Morbiditätsevidenz, Log 28) | \(\bar q_{\text{1P}}\) = 0,346 [63] |
| \(\beta_{\text{pfl}}\) = 1,54 | Fouillet/Bouchama/Klenk [41,44,60,61] | nur 85+ | nur \(D_a\) (F: Gegenevidenz [64]) | \(\bar q_{\text{pfl}}\) = 0,149 [61] |
| \(\beta_d\) (Distanz) | Nicholl [38] — transportierte Notfälle | — (Sensitivitätsband, Log 20) | — | entfällt im Basiswert |

Alle Faktoren mittelwertzentriert (§3.2; Bundesmittel = 1 je Band) — damit kalibrierneutral.

**Einwohner je Altersband einer Zelle und Ersatzregel für den geheimgehaltenen Anteil 65+**
(Befund 104, Entscheidungslog Nr. 41). Das Produkt nimmt \(\text{pop}_a\) je Zelle aus dem
Zensus-Gitter [67]: Einwohner der Zelle × Anteil 65+ ergibt die Menschen ab 65; die
5er-Jahresgruppen der Zelle teilen sie auf die Bänder 65–74, 75–84 und 85+ auf (fehlen sie, die
Aufteilung des Gebiets). Wo der Anteil 65+ im Gitter geheimgehalten ist („–“), setzt das Produkt
die Ersatzregel ein, ohne Gemeindeschlüssel nur Stufe 1 (Modellgrenze unter der Tabelle).
**Regel (Abschätzung von KAP3, festgelegt vom methodik_manager):** Ist der Anteil 65+ einer
Zelle im Zensus-Gitter geheimgehalten („–“), ersetzt das Produkt ihn in zwei Stufen.
*Stufe 1:* Ist in der Zelle mindestens eine der sechs 5er-Jahresgruppen ab 65 im Altersgitter
veröffentlicht, gilt die Summe der veröffentlichten Gruppen ab 65 geteilt durch die Einwohner der
Zelle. Nicht veröffentlichte Gruppen (dort „–“, also 0, 1 oder 2 Personen) zählen als 0.
*Stufe 2:* Die übrigen geheimgehaltenen Zellen bekommen den Rest aus der Gemeindesumme. Das Gitter
der Gemeinde soll so viele Menschen ab 65 tragen, wie der Anteil der Gemeinde im Zensus 2022 [69]
verlangt:

1. Anteil ab 65 der Gemeinde: A_G = (Einwohner ab 67 + 2/7 der Gruppe 60–66) / Einwohner, alle
   drei Zahlen aus [69]. [69] trennt bei 67, nicht bei 65. Von den sieben Jahrgängen 60–66 zählen
   deshalb die Jahrgänge 65 und 66, also 2/7 der Gruppe; das setzt gleich viele Menschen je
   Jahrgang voraus und ist eine Abschätzung von KAP3 (Block `heat.anteil_60_66`, Anker `#ersatz-65`). Fehlt die Gemeinde in [69] (anderer
   Gebietsstand) oder steht dort „.“, gilt A_G der Kreiszeile aus [69] (Kreis mit denselben ersten
   fünf Stellen des Gemeindeschlüssels; Befund 119).
2. Zielzahl: Z = A_G × Einwohnersumme der Gemeinde im Zensus-Gitter.
3. Rest: R = Z − Einwohner ab 65 der Zellen mit veröffentlichtem Anteil − Einwohner ab 65 aus
   Stufe 1.
4. Jede Zelle der Stufe 2 bekommt denselben Anteil R / Einwohner aller Zellen der Stufe 2,
   begrenzt auf 0–100 %. Ist R kleiner als null, gilt 0.

Die Regel gilt auch für Gemeinden ohne Zelle mit veröffentlichtem Anteil 65+ (dann ist der erste
Abzug in Schritt 3 null). Die frühere Modellgrenze „keine Zelle mit veröffentlichtem Anteil,
kein Ersatzwert“ (30 Gemeinden mit zusammen 376 Einwohnern) fällt damit weg.

*Rechenbeispiel Warmsen* (Ausgabe von `--ersatz`, Zahlen gerundet): [69] zählt 3158 Einwohner,
388 im Alter von 60–66 und 602 ab 67. A_G = (602 + 2/7 × 388) / 3158 = 712,9 / 3158 = 22,57 %.
Das Gitter zählt 3087 Einwohner: Z = 22,57 % × 3087 = 697. Fest stehen 508 Einwohner ab 65 in den
Zellen mit veröffentlichtem Anteil und 36 aus Stufe 1: R = 697 − 508 − 36 = 153. Die 362 Zellen
der Stufe 2 zählen 1897 Einwohner, jede bekommt 153 / 1897 = 8,07 % Anteil 65+.

```python test: beispiel_95_ersatz_stufe2_warmsen
# Stufe 2 der Ersatzregel (§3.3), Warmsen: A_G aus [69], Zielzahl, Rest, Anteil je Zelle
a_g = (602 + 2 / 7 * 388) / 3158
assert abs(a_g - 0.2257) < 0.00005
z = a_g * 3087
assert round(z) == 697
r = 697 - 508 - 36
assert r == 153
assert abs(r / 1897 - 0.0807) < 0.00005
```

*Modellgrenzen.* Ist R kleiner als null, tragen die Zellen mit veröffentlichtem Anteil und Stufe 1
schon mehr Menschen ab 65, als der Anteil der Gemeinde verlangt; die Zellen der Stufe 2 bekommen
dann 0 %, der Überhang bleibt stehen. Gemessen (`python3 docs/methodik/anlagen/95_zellvergleich.py
--rangliste`) betrifft das 1342 der 10.811 Gemeinden mit Zellen der Stufe 2; in deren Zellen der
Stufe 2 wohnen 320.780 der bundesweit 8.739.209 Einwohner solcher Zellen (3,7 %). Der Überhang ist
klein: im Median 5 Einwohner ab 65 je Gemeinde, höchstens 195. In 3 Gemeinden ist R größer als die
Einwohner der Stufe 2 und der Anteil wird auf 100 % begrenzt (19 Einwohner). 68 Gemeinden haben
keine Gemeindezeile in [69] oder dort „.“ und nehmen A_G aus der Kreiszeile (5240 Einwohner in
Zellen der Stufe 2, 0,1 %); für sie gilt der Altersaufbau des Kreises statt der Gemeinde. Ohne
Ersatzwert bleibt nur eine Gemeinde, die weder eine Gemeinde- noch eine Kreiszeile hat: Hanau,
in VG250 unter dem Schlüssel 06415000, in [69] noch unter 06435014 im Main-Kinzig-Kreis. Ihre
Zellen der Stufe 2 (3893 Einwohner) rechnen wie heute mit 65+ = 0.
Innerhalb einer Gemeinde bekommen alle Zellen der Stufe 2 denselben Anteil; wo die Älteren unter
ihnen wohnen, weiß die Regel nicht.

*Gemessene Wirkung.* Das Skript `docs/methodik/anlagen/95_zellvergleich.py` rechnet mit der
Option `--ersatz` jede Kommune zweimal, ohne Gemeindeschlüssel (nur Stufe 1) und mit der ganzen Regel, beide Male
wie der Zelllauf in §3.0 (Wirkungen (a)–(d)). Derselbe Aufruf gibt auch die Spanne aus, wenn die
Gruppe 60–66 gar nicht (0/7) oder ganz (7/7) zu den Menschen ab 65 zählt:

| Beispielkommune | Aufruf | Einwohner (Zensus-Gitter) | davon in Zellen mit geheimgehaltenem Anteil 65+ | Einwohner ab 65 ohne Gemeindeschlüssel | Einwohner ab 65 mit Regel | Jahresbetrag ohne Gemeindeschlüssel | Jahresbetrag mit Regel | Faktor ohne Gemeindeschlüssel gegen Regel | Spanne des Faktors (60–66 ganz oder gar nicht) |
|---|---|---|---|---|---|---|---|---|---|
| Berlin (AGS 11000000) | `python3 docs/methodik/anlagen/95_zellvergleich.py --gemeinde 11000000 --ersatz` | 3.593.357 | 2,8 % | 696.648 | 707.318 | 338,84 Mio. € | 342,67 Mio. € | × 0,989 | × 0,927–1,000 |
| Warmsen, Landkreis Nienburg (Weser) (AGS 03256034) | `python3 docs/methodik/anlagen/95_zellvergleich.py --gemeinde 03256034 --ersatz` | 3087 | 64,2 % | 544 | 697 | 145.025 € | 173.099 € | × 0,838 | × 0,651–0,947 |

Beträge je Jahr (Preisstand 2024), gemessen am 27.09.2026. *Modellgrenze ohne Gemeindeschlüssel (Befund 141).* Das
Produkt braucht für Stufe 2 den Gemeindeschlüssel der Kommune. Ist die Kommune kein Gemeindeteil der VG250 [65], rechnet
es nur Stufe 1, und die Zellen der Stufe 2 behalten 65+ = 0. Der Betrag liegt dann in Berlin um 1,1 % (338,84 statt
342,67 Mio. €), in Warmsen um 16 % (145.025 statt 173.099 €) zu niedrig. Dieselbe Regel gilt überall, wo das Produkt
den Anteil ab 65 liest: Es ist eine Methodik, deshalb nutzen auch die Hitze-Kennzahlen der Übersicht und der Rückfallpfad
ohne Altersbänder den Ersatzwert (Befund 142).
*Toleranz (Befunde 140 und 145).* Ein Nachrechnen trifft den Betrag, wenn es um höchstens ± 0,29 % des Betrags
(1 Mio. € / 342,67 Mio. € = 0,2918 %) abweicht: Berlin ± 1 Mio. € um 342,67 Mio. €, Warmsen ± 505 € um 173.099 €. Die Toleranz deckt die Rundung der
Faktoren und der Wochenquantile ab (§3.2: mit der Datei 342,58 Mio. € und 172.957 €). 362,9, 342,67 und 343 Mio. € meinen
zwei Rechnungen: 362,9 ist die Kette an einem Punkt (§3.0), 342,67 der Zelllauf mit ungerundeten Faktoren, 343 derselbe
Zelllauf aus den gerundeten Faktoren im Prüfblock §3.0 (362,9 × 0,934 nach Teilung durch 0,9888 = 342,8; mit dem
ungerundeten Produkt 0,9343 der vier Faktoren, wie im Prüfblock, 342,9). Warmsen zählt nach dem Zensus 2022 amtlich 3158 Einwohner
[69], liegt also unter 10.000. Gewählt ist Warmsen, weil sie unter allen Gemeinden mit 2000 bis
unter 10.000 Einwohnern im Zensus-Gitter den höchsten Anteil der Einwohner in Zellen mit
geheimgehaltenem Anteil 65+ hat (Median der Gemeinden unter 10.000 Einwohnern 27,9 %; Aufruf
`python3 docs/methodik/anlagen/95_zellvergleich.py --rangliste`).

*Warum Stufe 2 den Rest aus der Gemeindesumme nimmt (Befund 117).* Das „–“ steht meist für Zellen
mit wenigen Älteren: Das Altersgitter derselben Zellen zählt in Berlin 85.046 Personen in
veröffentlichten 5er-Jahresgruppen, davon 2252 ab 65 (2,6 %), in Warmsen 692, davon 36 (5,2 %).
Die frühere Stufe 2 übertrug den einwohnergewichteten Anteil 65+ der Zellen mit veröffentlichtem
Anteil, in einer ländlichen Kommune vor allem kleine Zellen mit Älteren: in Warmsen 46,00 %. Damit
kam Warmsen auf 1416 Einwohner ab 65, mehr als die 990 ab 60 im Zensus 2022 [69], und der Betrag
auf mehr als das Doppelte: 305.088 € gegen 138.543 € (Messung der früheren Fassung, Befund-Ledger
Runde 17, T-1199; das Skript rechnet diese Fassung nicht mehr). Der Rest aus der Gemeindesumme
hält dagegen die amtliche Zahl der Gemeinde: Warmsen kommt auf 697 Einwohner ab 65, zwischen den
602 ab 67 und den 990 ab 60; Berlin auf 707.318, zwischen 624.505 ab 67 und 916.859 ab 60 [69].
Beide Summen treffen die Zielzahl Z, weil R in beiden Kommunen zwischen null und den Einwohnern
der Stufe 2 liegt.

*Was eine einfachere Rechnung verfälschen würde.* Rechnet das Produkt ohne Gemeindeschlüssel nur
Stufe 1, zählt Warmsen 544 Einwohner ab 65, weniger als die 602 ab 67 allein, und der Betrag liegt um
16 % zu niedrig (Faktor × 0,838). Mit 65+ = 0 (frühere Produktlogik vor Stufe 1) waren es
508 Einwohner ab 65 und 20 % zu wenig (Faktor × 0,800; Messung vom 25.09.2026, Befund-Ledger
Runde 19). Die Aufteilung der Gruppe 60–66 ist die größte Unsicherheit der Regel: Zählt die ganze
Gruppe oder gar nichts davon, liegt der Faktor in Warmsen bei × 0,651–0,947, in Berlin bei
× 0,927–1,000 (Tabelle oben). In jeder Lesart ist der Betrag mit der ganzen Regel mindestens so
hoch wie ohne Gemeindeschlüssel; in Berlin ist er bei 0/7 gleich (× 1,000, 696.649 gegen 696.648
Einwohner ab 65). Die Richtung der Korrektur hängt an der Aufteilung nicht.

*Stichtag.* Gitter und [69] zählen beide zum Stichtag 15.05.2022. Ebene 1 der Rechenkette (§3.0)
bleibt die Fortschreibung zum Stichtag 31.12.2023, weil die Basissterberaten m_a [49] Sterbefälle
2023 durch die Bevölkerung am 31.12.2023 teilen; Einwohner und Sterberate beziehen sich so auf
denselben Tag (Entscheidungslog Nr. 42, Befund 99). Der Unterschied zum Gitter steht in §3.0 als
Wirkung (b), in Berlin × 0,981. Der Code-Nachzug der Regel liegt beim cto (Befund 116).

**Herleitung der ERF-Steigungen \(\beta_{85+,\text{Region}}\)** (Anker `#beta-erf`;
Befund 60i): Winklmayr Abb. 3 publiziert Kurven, keine Steigungszahlen. Ablesekette:
relatives Risiko der 85+-Kurve bei 25 °C Wochenmittel je Region (2012–2021): RR ≈ 1,40
(Nord) / 1,35 (Mitte) / 1,25 (Süd); mit \(\beta = \ln(\text{RR})/(25 - T_0)\):
Nord \(\ln 1{,}40/5{,}3 = 0{,}0634\) · Mitte \(\ln 1{,}35/4{,}8 = 0{,}0625\) ·
Süd \(\ln 1{,}25/4{,}2 = 0{,}0531\) K⁻¹. **Rev. 7:** Der Süd-Wert ist per
Holdout-Nachschätzung modellintern auf \(0{,}0531 \times 1{,}65 = \mathbf{0{,}0876}\)
K⁻¹ angehoben (Verfahren, Identifikation und Band in §4, Anker `#beta-sued`;
Nord/Mitte unverändert — Basiswerte der Formeln sind 0,0634/0,0625/0,0876).

```python test: beispiel_95_beta_ablesekette
# beta = ln(RR bei 25 °C) / (25 - T0) je Region (Anker #beta-erf)
import math
for rr, t0, soll in [(1.40, 19.7, 0.0634), (1.35, 20.2, 0.0625), (1.25, 20.8, 0.0531)]:
    assert abs(math.log(rr) / (25.0 - t0) - soll) < 0.0002
```

**(a) Rückrechnung der Altersfaktoren \(f_a\)** (Befund 32; §3.9 „Abgeleitet"):
Für kleine \(\beta\,\Delta\) gilt je Band \(\text{Todesfälle}_a \propto \text{pop}_a \cdot
m_a \cdot \beta_a\), also \(f_a \propto \text{Anteil}_a / (\text{pop}_a \cdot m_a)\)
— **lineare Näherung, gekennzeichnet**; ihre Güte wird in §4 (Altersverteilungs-Ist) geprüft.
Mit den RKI-Anteilen 2026 (6,5/12,9/25,2/55,5 % [12]) und den Sterbefällen 2023
(\(\text{pop}_a m_a\) = 138.024/166.312/302.921/420.949 [49]):
\(f_a^{\text{roh}}\) = 0,065/138.024 = 4,709·10⁻⁷ · 0,129/166.312 = 7,757·10⁻⁷ ·
0,252/302.921 = 8,319·10⁻⁷ · 0,555/420.949 = 1,3184·10⁻⁶; normiert auf 85+ = 1:

$$ f_a \;=\; 0{,}357 \;/\; 0{,}588 \;/\; 0{,}631 \;/\; 1{,}0 $$

Die Rev.-5-Werte (0,404/0,577/0,620) waren mit den alten Basissterberaten gerechnet und sind
mit den korrigierten \(m_a\) inkonsistent (u65 −12 %); die Kopplung \(f_a \leftrightarrow
m_a\) (§3.9) ist hiermit neu gerechnet, der Kalibrierlauf (§4) nutzt die neuen Werte.

**Band von \(f_a\) (Abschätzung von KAP3, Befund 152).** Die Altersanteile der Hitzetoten schwanken von Sommer zu
Sommer. Dieselbe Rückrechnung mit den Anteilen eines einzelnen Sommers ergibt die Bandenden: Sommer 2025 (RKI-Wochenbericht
KW 38/2025 [74], Tabelle 1: 80 · 210 · 660 · 1.560 Hitzetote, also 3,2 · 8,4 · 26,3 · 62,2 %) ⇒ \(f_a\) = 0,156 · 0,341 ·
0,588 · 1,0; Sommer 2026 (Wochenbericht KW 37/2026 [75], Tabelle 1: 1.510 · 2.440 · 3.890 · 8.200, also 9,4 · 15,2 · 24,3 ·
51,1 %) ⇒ 0,562 · 0,753 · 0,659 · 1,0. Band je Altersband also u65 0,156–0,562, 65–74 0,341–0,753, 75–84 0,588–0,659;
85+ bleibt 1,0, weil alle Faktoren auf 85+ bezogen sind. Beide Sommer sind laufende Schätzungen des RKI, auf zehn
gerundet; das Band zeigt, wie weit ein einzelner Sommer von der Altersverteilung abweicht, mit der der Bericht rechnet.
Wie stark das den Betrag verschiebt, steht in §5 (Sensitivitäten des Basiswerts).

```python test: beispiel_95_fa_rueckrechnung
# f_a = (Anteil_a/Sterbefaelle_a), normiert auf 85+ (lineare Naeherung, §3.3a)
shares = {"u65": 0.065, "a65_74": 0.129, "a75_84": 0.252, "a85p": 0.555}
deaths = {"u65": 138_024, "a65_74": 166_312, "a75_84": 302_921, "a85p": 420_949}
raw = {b: shares[b] / deaths[b] for b in shares}
fa = {b: raw[b] / raw["a85p"] for b in raw}
for b, soll in [("u65", 0.357), ("a65_74", 0.588), ("a75_84", 0.631), ("a85p", 1.0)]:
    assert abs(fa[b] - soll) < 0.001
```

**(b) Pflegeheim-Term \(\beta_{\text{pfl}}\)** (Befund 9 — Kette vollständig):
OR (Heim vs. Nicht-Heim, 85+) = Exzess-Verhältnis × Basissterblichkeits-Verhältnis.
(1) Exzess-Verhältnis: Fouillet 2006, Tab. 2 (O/E nach Sterbeort): Heime 1,9 [1,7–2,1] vs.
Wohnung ≥ 75: 1,9 ⇒ **1,0** — der relative Hitze-Exzess ist gleich; das Mehr-Risiko der
Heimbewohner liegt im Niveau. (2) Basissterblichkeits-Verhältnis: Heim ≈ 0,34/Jahr
(0,65 %/Woche × 52, WIdO [61]); Nicht-Heim-85+ aus \(m_{85+}\) = 0,1480 und
\(\bar q_{\text{pfl}}\) = 0,149: \((0{,}1480 - 0{,}149 \cdot 0{,}34)/0{,}851 = 0{,}1144\)
⇒ 0,34/0,1144 = **2,97**. (3) OR = 1,0 × 2,97 ≈ **3,0** (Band 2,2–6,0; Stützen: Bouchama
[41] „nicht selbstversorgungsfähig" OR 2,97 — Referenzgruppe zu 56 % selbst pflegebedürftig,
daher nur qualitative Untergrenzen-Stütze ≈ 3; Klenk [44] belegt die **ERF-Gültigkeit im
Heim-Setting** (+26 %/+62 % bei 32–34/≥ 34 °C), nicht das Niveau — umgewidmet per Befund 9).
Übersetzung: \(\beta_{\text{pfl}} = (3{,}0-1)/[1 + 0{,}149\,(3{,}0-1)] = 2{,}0/1{,}298 =
\mathbf{1{,}54}\) (Band 1,0–2,9). Wirkung: 85+-Zelle ohne Heim ×0,77, mit \(q=0{,}30\) ×1,23.

```python test: beispiel_95_or_uebersetzungen
# beta_iso = (OR-1)/[1+q(OR-1)]; OR=2,3, q_1P=0,346 (Mikrozensus 2023) => 0,90
b_iso = (2.3 - 1) / (1 + 0.346 * (2.3 - 1))
assert abs(b_iso - 0.90) < 0.005
# beta_pfl-Kette (§3.3b): m_nichtheim, Verhaeltnis, OR=3,0 => 1,54
m_nh = (0.14800 - 0.149 * 0.34) / 0.851
assert abs(m_nh - 0.1144) < 0.0005
assert abs(0.34 / m_nh - 2.97) < 0.02
b_pfl = (3.0 - 1) / (1 + 0.149 * (3.0 - 1))
assert abs(b_pfl - 1.54) < 0.005
assert abs((1 + b_pfl * (0.0 - 0.149)) - 0.77) < 0.005    # 85+-Zelle ohne Heim
assert abs((1 + b_pfl * (0.30 - 0.149)) - 1.23) < 0.005   # q = 0,30
# Zentrierungsmittel: 424.300 vollstationaer 85+ / 2.844.213 EW 85+ = 0,149
assert abs(424_300 / 2_844_213 - 0.149) < 0.001
```

Semantik der Wochensumme: \(e^{\beta_a (T_w-T_0)_+}-1\) ist die relative Übersterblichkeit
(RR − 1) der Woche \(w\); multipliziert mit den Basissterbefällen der Woche
(\(\text{pop}_a m_a/52\)) ergibt sie deren zusätzliche Todesfälle; die Jahressumme sind die
13 Wochenbeiträge. Am Sommermittel (≈ 18,5 °C, unter allen Schwellen) käme fast überall null
heraus — deshalb die Quantil-Verteilung.

```python test: beispiel_95_wochenbeitrag
# Mini-Beispiel Band 85+, Region Mitte: T_w=23,0 °C, T_0=20,2 °C, beta=0,0625;
# 40 Basissterbefaelle der Woche => ~7,6 zusaetzliche Todesfaelle
import math
rr_minus_1 = math.exp(0.0625 * (23.0 - 20.2)) - 1
assert abs(rr_minus_1 - 0.19) < 0.005
assert abs(rr_minus_1 * 40 - 7.6) < 0.1
```

```python test: beispiel_95_zelle_yll
# Beispielzelle Region Mitte: 15 Personen 85+, D=0,018 Faelle/Jahr
# => 0,075 YLL (L_85+ = 4,16, Rev. 8); x VOLY 160.800 => ~12.040 EUR/Jahr
yll = 0.018 * 4.16
assert abs(yll - 0.0749) < 0.0005
assert abs(yll * 160_800 - 12_040) < 50
# Sensitivitaet VSL-Weg: 0,018 x 4,7 Mio. = 84.600 EUR (korrigiert, Befund 57)
assert abs(0.018 * 4_700_000 - 84_600) < 1
```

### 3.4 Morbidität (altersgeschichtet, §3.2-Struktur)

$$ F_{\text{Zelle}} \;=\; \sum_a \text{pop}_a \cdot \frac{r_{0,a}}{100\,000} \cdot \max\!\bigl( 0,\; 1 + e_{\text{HD}} \cdot (\text{HD} - \text{HD}_{\text{ref}}) \bigr) $$

- **HD-Term zweiseitig linear, bei 0 gedeckelt** (Befund 59): Zellen unter der Referenzlast
  reduzieren die Baseline anteilig (HD = 0 → Faktor 1 − 0,024·7,2 = 0,83); damit ist der
  Term bevölkerungsgewichtet erwartungstreu um die Referenz (kein Jensen-Rest des früheren
  Positivteils — der in \(r_0\) enthaltene Durchschnittseffekt wird nicht doppelt gezählt).
  **Dokumentierte Grenze:** Die verbleibende Baseline ist bevölkerungsproportional — der
  §3.1-Lackmustest („Kommune ohne Treiber → ~0") gilt für die **Mortalität**, nicht für den
  Morbiditäts-Sockel (nicht-wetterlicher T67-Kern: Anstrengung, Innenraum); eine
  Klimaanteil-Zerlegung des Sockels (hitzeproportionaler Anteil ≈ 0,51 aus der
  \(r_0\)-Herleitung) ist die dokumentierte Alternative (Log 29).
- **Modifikatoren im F-Pfad** (Befunde 7/58): **keine** — \(\beta_{\text{pfl}}\) hat
  Gegenevidenz (Flandern: Hospitalisierung OR 0,96 n. s. bei Mortalität OR 1,61 [64]),
  \(\beta_d\) ist für Einweisungen richtungsunklar, und für \(\beta_{\text{iso}}\) existiert
  nur Mortalitätsevidenz (Semenza misst Todesfälle) → alle Default 1 (§3.2: unbelegte
  Modulatoren; Log 28).
- **\(e_{\text{HD}}\) = 0,024 (konditional) als Basis** (Befund 5; Log 19): der konditionale
  Wert misst den marginalen Effekt eines *zusätzlichen* Hitzetags und ist konsistent zur
  Untergrenzen-Linie; unkonditional 0,054 als Obergrenze des Bands, Hitzewellentag 0,061.
  **Harvesting:** keine zusätzliche Korrektur auf \(F\) — die K&Z-Jahresaggregate enthalten
  die Verschiebeeffekte bereits (> 90 % Reduktion der Tageseffekte im Aggregat [18]).
- **\(\text{HD}_{\text{ref}}\) = 7,2 Tage/Jahr** (Befunde 6/60iii; Anker `#hd-ref`):
  bundesweites Mittel der Hitzetage (Tmax > 30 °C) der K&Z-Beobachtungsperiode 1999–2008 —
  Fundstelle: Karlsson & Ziebarth 2018 [18]/IZA-DP 7875 [62] (Beschreibung des Panels,
  „Ø 7,2 Hitzetage/Jahr"); das ist die Hitzetag-Last, unter der die Baseline \(r_{0,a}\)
  gemessen wurde — verhindert Doppelzählung des Durchschnittseffekts; räumlich konstanter
  Registry-Parameter.
- **HD-Datenquelle** (Befund 38): DWD-CDC-Raster hot_days (1 km), am Zell-/Kommune-Standort
  abgegriffen — **ohne UHI-Verschiebung**; das Produkt implementiert keine solche Umrechnung
  (Ist-Stand `inputs.py`: „dwd_cdc_raster"). Richtung: Unterschätzung der Morbidität in
  UHI-Lagen; UHI→hot_days-Umrechnung als dokumentierte Erweiterung (Fortschreibungsvermerk,
  Log 25). Die Rev.-5-Formulierung „+ UHI-Verschiebung" beschrieb Nicht-Implementiertes.
- Altersschichtung: hitzeassoziierte Einweisungen konzentrieren sich auf Ältere
  (Herz-Kreislauf/Nieren; T67-Raten steigen steil mit Alter [16,18]). K&Z ohne numerische
  Alterstabelle (Fig. 9; top-kodiert > 75) — \(e_{\text{HD}}\) als gleiche relative
  Elastizität über alle Bänder (dokumentierte Annahme, Band aus dem Fouillet-
  Altersgradienten); das absolute Altersmuster entsteht über \(r_{0,a}\).
- **\(r_{0,a}\)-Herleitung** (Befunde 4/60iv, Anker `#r0-a`): Gesamtrate \(r_0\) =
  T67-Kern + dauerhaft kodierter Kreislauf-Kern. (1) T67 direkt: Ø ≈ 1.400/Jahr ÷ 83,456
  Mio. = **1,68**/100.000·Jahr [16]. (2) Kreislauf-Kern: Herz-Kreislauf trägt **11,9 %**
  des Einweisungs-Exzesses (K&Z Tab. 3 [62]) — je Hitzetag konditional 0,119 × 1,408 =
  0,168 bzw. unkonditional 0,119 × 3,106 = 0,370 je 100.000; × 7,2 Hitzetage/Jahr =
  **1,21…2,66**/100.000·Jahr. (3) Summe: 1,68 + 1,21…2,66 ⇒ **3,5 (2,9–4,3)
  je 100.000·Jahr** [16,18,62]. Die Bandgrenzen sind 1,68 + 1,21 = 2,89 und 1,68 + 2,66 = 4,34;
  der Mittelwert 3,5 ist ihr geometrisches Mittel √(2,89 × 4,34) = 3,54, weil das Band als Faktor
  um den Mittelwert gelesen wird (Zeichentabelle §3.6); die Mitte der Spanne, 3,61, läge 2 % höher.
  Auf 3,54 sind die Altersraten normiert. Altersaufteilung:
  Raten **1,9 / 6,3 / 10,8 / 15,6** je 100.000 — bevölkerungsgewichtete Summe:
  (64.747.448·1,9 + 9.569.640·6,3 + 6.294.744·10,8 + 2.844.213·15,6)/83.456.045 = **3,54** ✓;
  das entspricht dem Verhältnis **1 : 3,3 : 5,7 : 8,2** (der Rev.-5-Text „1:5:8:10" war mit
  den Raten inkonsistent und ist ersetzt). Das Altersprofil ist eine **gekennzeichnete
  Abschätzung** (§3.9 „Abgeschätzt") am Steilheitsmuster der Kreislauf-Morbidität (qualitative
  Stütze: KHK-Sterblichkeit 65–79 ≈ 239 vs. 80+ ≈ 1.476 je 100.000, GBE); die
  altersspezifischen T67-/I00–I99-Raten (GENESIS 23131-0002 / GBE) sind nicht keyless
  abrufbar (dokumentierte Datenlücke) und ersetzen die Aufteilung, sobald verfügbar
  (Registry-Vermerk).

```python test: beispiel_95_r0_kette
# r_0-Zusatzterm (Anker #r0-a): Kreislauf-Anteil 11,9 % x Elastizitaet x 7,2 Tage
u = 0.119 * 1.408 * 7.2   # konditional
o = 0.119 * 3.106 * 7.2   # unkonditional
assert abs(u - 1.21) < 0.01 and abs(o - 2.66) < 0.01
assert abs(1.68 + u - 2.89) < 0.01 and abs(1.68 + o - 4.34) < 0.01
assert abs(((1.68 + u) * (1.68 + o)) ** 0.5 - 3.54) < 0.01   # Mittelwert = geometrisches Mittel
```

```python test: beispiel_95_r0_normierung
# r_0,a bevoelkerungsgewichtet = 3,54 je 100.000; Verhaeltnis 1:3,3:5,7:8,2 (§3.4)
pop = {"u65": 64_747_448, "a65_74": 9_569_640, "a75_84": 6_294_744, "a85p": 2_844_213}
r0 = {"u65": 1.9, "a65_74": 6.3, "a75_84": 10.8, "a85p": 15.6}
mean = sum(pop[b] * r0[b] for b in pop) / sum(pop.values())
assert abs(mean - 3.54) < 0.01
assert abs(r0["a65_74"] / r0["u65"] - 3.3) < 0.05
assert abs(r0["a75_84"] / r0["u65"] - 5.7) < 0.05
assert abs(r0["a85p"] / r0["u65"] - 8.2) < 0.05
```

### 3.5 Monetarisierung (K1) und Aggregation

$$ \text{€}_{\text{Zelle}} \;=\; \text{YLL}_{\text{Zelle}} \cdot \text{VOLY} \;+\; F_{\text{Zelle}} \cdot c_{\text{Fall}}, \qquad \text{Kommune} = \sum_{\text{Zellen}} \quad (\text{Ausweis: YLL / Fälle / €}) $$

VOLY-Herleitung (MK-4.0-Regel): Amann 2020a Tab. 3.15: 79.500 €₂₀₀₅; Anpassung VPI
2005→2024 ×1,4638 · Kaufkraft-Raumtransfer EU27→DE mit Elastizität 0,85 ×1,1792 ·
Einkommensentwicklung ^0,85 ×1,1719 ⇒ **160.800 € (Preisstand 2024)** (Preisstand-Label korrigiert,
Befund 10: alle Indexendpunkte sind 2024). **Band** (Befund 10, definiert): Untergrenze
136,4 T€ (ohne Raumtransfer: 79.500 × 1,4638 × 1,1719); Obergrenze **165,6 T€**
(Raumtransfer ohne Elastizität: 79.500 × 1,4638 × 1,2140 × 1,1719) — der Rev.-5-Wert
169,5 T€ reproduzierte mit keiner Faktorkombination und ist ersetzt. VSL nur Sensitivität:
6,19 Mio. € (Preisstand 2024; MK-konsistent; ÷ VOLY = 38,5 LJ, Konsistenz-Check ✓), 4,7 Mio. € (Preisstand 2024;
EU-Referenz) und 3,5 Mio. € (Nutzer-Setzung der Arbeitsmappe vor Fortschreibung, Befund 50).
\(c_{\text{Fall}}\) = 6.996 €₂₀₂₃ × (119,3/116,7) = **7.152 €₂₀₂₄** — **Proxy**
(Durchschnitt **aller** Krankenhausfälle; hitzeassoziierte Fälle haben einen anderen Fallmix;
Befund 42; DRG-basierte Sätze als Sensitivität benannt).

```python test: beispiel_95_voly_kette
# VOLY-Kette: 79.500 x 1,4638 x 1,1792 x 1,1719 = ~160.800 EUR (Preisstand 2024)
v = 79_500 * 1.4638 * 1.1792 * 1.1719
assert abs(v - 160_800) < 200
# Band: Untergrenze ohne Raumtransfer; Obergrenze Raumtransfer ohne Elastizitaet (Befund 10)
assert abs(79_500 * 1.4638 * 1.1719 - 136_400) < 200
assert abs(79_500 * 1.4638 * 1.2140 * 1.1719 - 165_600) < 200
# c_Fall auf 2024 indexiert: 6.996 x 119,3/116,7 = 7.152 (Befund 23)
assert abs(6_996 * 119.3 / 116.7 - 7_152) < 2
```

```python test: beispiel_95_basisraten
# m_a = Sterbefaelle 2023 / Bevoelkerung 31.12.2023 (je 100.000)
for tote, ew, soll in [(138_024, 64_747_448, 213.2), (166_312, 9_569_640, 1_737.9),
                       (302_921, 6_294_744, 4_812.3), (420_949, 2_844_213, 14_800.2)]:
    assert abs(tote / ew * 100_000 - soll) < 0.5
# L_85+ (Anker #l-a, Rev. 8 EXAKT sterbefallgewichtet; Anlage
# l85_sterbefallgewichtung.csv): Einzeljahres-Summen 85-94 + 95+-Rest je
# Geschlecht (12613-02) x e(x) (12613-b01/-b02) => m 3,963 / w 4,281;
# m/w-Kombination mit STERBEFAELLEN 2023 (161.178 M / 259.771 F) => 4,16
lm, lw = 3.963, 4.281
d_m, d_w = 161_178, 259_771
assert d_m + d_w == 420_949   # Kreuzcheck: Summe 85+ == Tab. 12613-03
lg = (d_m * lm + d_w * lw) / (d_m + d_w)
assert abs(lg - 4.159) < 0.002
# Alte Rev.-7-Kette zur Einordnung (Bevoelkerungsgewichte, Untergrenzen-
# Stuetzstellen; beide Naeherungsfehler wirkten aufwaerts, Befund 22): der
# MAENNER-Pfad ergab 4,97; mit weiblich 5,69 bevoelkerungsgewichtet kombiniert
# war der Rev.-7-Berichtswert 5,44
assert abs((754_258 * 5.47 + 197_380 * 3.55 + 38_654 * 2.37) / 990_292 - 4.97) < 0.01
assert abs((990_292 * 4.97 + 1_853_921 * 5.69) / 2_844_213 - 5.44) < 0.01
```

**\(\bar L_a\)-Kette** (Anker `#l-a`; Befund 60ii; **Rev. 8**): u65: \(e(60)\)
(86 % der u65-Sterbefälle entfallen auf 50–64); 65–74: \(e(70)\); 75–84: \(e(80)\)
(bandmittige Stützstellen, m/w bevölkerungsgewichtet — unverändert). **85+ exakt
sterbefallgewichtet** (löst Befund 22): reale Sterbefälle 2023 nach
Einzelaltersjahren 85–94 (Tab. 12613-02 [49]) × \(e(x)\) der Sterbetafel
2022/2024 [48]; die 95+-Restzeile („95 und älter") mit tafelintern
sterbefallgewichtetem \(\bar e(95{+})\) = 2,151 (m) / 2,455 (w) — die einzige
verbleibende, gekennzeichnete Restnäherung. Geschlechter-Kombination mit
**Sterbefällen** (161.178 M / 259.771 F; Kreuzcheck gegen Tab. 12613-03 exakt):
männlich 3,963 · weiblich 4,281 ⇒ **4,16 J** (Band [4,16, 4,20]: Obergrenze mit
e(95)-Stützstelle statt \(\bar e(95{+})\)). Die Rev.-7-Kette (5,44) trug zwei
gleichgerichtete Näherungsfehler — Bevölkerungs- statt Sterbefallgewichte und
Untergrenzen-Stützstellen —, daher fällt die Korrektur (−1,28 J, ≈ −8 % auf die
YLL-Bundessumme) größer aus als die frühere Abschätzung −0,3…−0,5 J.
Reproduzierbar: Skript `l85_sterbefallgewichtung.py`, Anlagen
`l85_sterbefallgewichtung.csv`/`.md` [50]. Kopplungen (§3.9) neu gerechnet:
Beispiel `beispiel_95_zelle_yll`, Zeichentabelle, §7-Block, Sanity-Anker.

**Band von \(\bar L_a\) (Abschätzung von KAP3, Befund 152).** Die Stützstellen e(60), e(70) und e(80) stehen für das
Mittel eines Bands. Derselbe Rechenweg wie für 85+ auch für die drei jüngeren Bänder — Sterbefälle 2023 je Altersjahr
([49], Blatt 12613-02, Familienstand „Insgesamt“; die Zeilen „unter 1“ mit e(0), „1 – 30“ und „95 und älter“ tafelintern
gewichtet) × e(x) der Sterbetafel 2022/2024 [48], männlich und weiblich mit ihren Sterbefällen kombiniert — ergibt 28,64 ·
15,31 · 8,54 J (85+ zur Kontrolle 4,159 wie oben; gemessen am 27.09.2026 aus den Drucken der beiden Tabellen im
Quellenarchiv). Das Band je Altersband reicht von der Stützstelle bis zu diesem Wert: u65 23,39–28,64 J, 65–74
15,31–15,59 J, 75–84 8,54–8,90 J, 85+ 4,16–4,20 J. Die sterbefallgewichteten Werte setzen voraus, dass Hitzetote
innerhalb eines Bands so alt sind wie alle Gestorbenen. Weil die Hitzewirkung mit dem Alter steigt (§3.3a), sind sie
älter: unter 65 deutlich, denn den hohen Wert 28,64 tragen die wenigen Sterbefälle unter 50; ab 65 kaum. Der
zutreffende Wert liegt deshalb für u65 im Band, für 65–74 und 75–84 am unteren Ende. Die Werte selbst ändert dieses
Paket nicht; wie stark die Bänder den Betrag verschieben, steht in §5 (Sensitivitäten des Basiswerts).

### 3.6 Zeichentabelle (alphabetisch; §3.2-Form)

| Zeichen | Name | Einheit | Wert / Herkunft |
|---|---|---|---|
| \(a\) | Altersband u65 · 65–74 · 75–84 · 85+ | — | Zensus-Altersbänder |
| \(c_{\text{Fall}}\) | Behandlungskostensatz je Fall (**Proxy**: Ø aller KH-Fälle) | €₂₀₂₄ | 7.152 = 6.996 €₂₀₂₃ × 119,3/116,7 [17,19]; register:95-E02-02 |
| \(c_{\text{kal}}\) | Kalibrierfaktor, **ein nationaler Skalar** (§3.4; Herleitung §4) — Fit auf bevölkerungsgewichteten Reihen, keine Pauschalkorrektur | — | **0,581** (Fenster 2012–2024, in-sample; Sensitivitäten: ohne Süd-Nachschätzung 0,661, Vollreihe 0,660, inkl. vorl. 2025 0,651, Voll-Holdout 0,567 → Prüfstein ebenfalls 12/16); herleitung:#c-kal, #t-povw [50] |
| \(D_a\) | hitzebedingte Todesfälle der Zelle im Band \(a\) (Teil-Ausweis) | 1/Jahr | berechnet |
| \(e_{\text{HD}}\) | rel. Mehr-Einweisungen je Hitzetag (> 30 °C), **konditional** | 1/Tag | 0,024 (Band 0,024–0,061; unkond. 0,054), K&Z Tab. 1 [18,62]; register:95-E02-02; Log 19 |
| \(f_a\) | Altersfaktor der RR-Steigung rel. zu 85+ | — | 0,357 / 0,588 / 0,631 / 1,0 — Rückrechnung §3.3a (lineare Näherung, gekennzeichnet); Band 0,156–0,562 / 0,341–0,753 / 0,588–0,659 / 1,0 aus den Altersanteilen der Sommer 2025 und 2026 [74, 75] (Befund 152); herleitung:#f-a |
| \(F_{\text{Zelle}}\) | hitzeassoziierte Erkrankungsfälle (Teil-Ausweis) | 1/Jahr | Ergebnis |
| \(g_{\text{S157}}\) | Exzessfaktor gekühlter Heimplätze: Anteil des Hitze-Exzesses, der mit Klimaanlage bleibt (Maßnahme §5) | — | 0,29 (Band 0–0,90) = (rOR × OR_ohne − 1)/(OR_ohne − 1), Abschätzung von KAP3 aus [46]; register:95-S157-01 |
| \(h_{\text{Heim}},\ h_{\text{Heim},z}\) | Anteil der Heimbewohner an den Todesfällen 85+ auf Ebene der Kommune / der Zelle \(z\) | — | Kommune: \(\bar q_{\text{pfl}}\,[1 + \beta_{\text{pfl}}(1 - \bar q_{\text{pfl}})]\) = 0,344 (Band 0,275–0,517); Zelle: \(q_{\text{pfl},z}\,[1 + \beta_{\text{pfl}}(1 - \bar q_{\text{pfl}})] / [1 + \beta_{\text{pfl}}(q_{\text{pfl},z} - \bar q_{\text{pfl}})]\), Rückfallwert 0,344 (§5, Befund 146); berechnet, Block `heat.h_heim` [61]; register:95-S153-01 |
| \(\text{HD},\ \text{HD}_{\text{ref}}\) | Hitzetage der Zelle (DWD-CDC hot_days 1 km, ohne UHI — §3.4) / Referenz = K&Z-Basisperiode | Tage/Jahr | HD: DWD-CDC [33]; \(\text{HD}_{\text{ref}}\) = **7,2** (Ø 1999–2008 [18]); herleitung:#hd-ref |
| \(\bar L_a\) | Restlebenserwartung je Band (Sterbetafel 2022/2024; u65–75–84 Stützstellen e(60)/e(70)/e(80); **85+ exakt sterbefallgewichtet, Rev. 8**) | Jahre | 23,39 / 15,59 / 8,90 / **4,16** (Band 23,39–28,64 / 15,31–15,59 / 8,54–8,90 / 4,16–4,20: Stützstelle bis sterbefallgewichteter Wert, §3.5, Befund 152; Anlage l85_sterbefallgewichtung.csv) [48,49]; herleitung:#l-a |
| \(\text{OR}_{\text{ohne}}\) | Odds des Todes an Extremhitzetagen in Heimen ohne Klimaanlage | — | 1,11 (1,06–1,16) [46]; register:95-S157-01 |
| \(m_a\) | Basissterberate je Band (Sterbefälle 2023 ÷ Bev. 31.12.2023) | 1/100.000·a | 213,2 / 1.737,9 / 4.812,3 / 14.800,2 [49]; herleitung:#m-a |
| \(\text{pop}_a\) | Bevölkerung der Zelle je Band | Personen | Zensus 2022, 100 m; register:95-R35-01 |
| \(q_{\text{1P}},\ \bar q_{\text{1P}}\) | Anteil allein lebender 65+ der Zelle / Bundesmittel | — | Zelle: Zensus-2022-Haushaltsgitter (Fallback s. u.); \(\bar q\) = **0,346** (Mikrozensus 2023 [63]); Zensus-Gitterwert ersetzt bei Integration; herleitung:#qbar-1p |
| \(q_{\text{pfl}},\ \bar q_{\text{pfl}}\) | Heimbewohner-Anteil an der 85+-Bevölkerung / Bundesmittel | — | OSM × Pflegestatistik 2023 (**Proxy**, Fallback s. u.); \(\bar q\) = 424.300/2.844.213 = **0,149** [61]; herleitung:#qbar-pfl |
| \(q_{w,\text{Region}}\) | empirisches Anomalie-Quantil der Sommerwoche | K | Tabelle §3.2; wochenquantile_region.csv [33,50] |
| \(r_{0,a}\) | Baseline-Einweisungsrate je Band | 1/100.000·a | 1,9 / 6,3 / 10,8 / 15,6 (= 1:3,3:5,7:8,2; Summe 3,54; Band ×0,6–1,6 = Summen-Band 2,9–4,3 [×0,83–1,23] kombiniert mit Altersprofil-Unsicherheit ±25 % [Option-B-Profil §3.4] ⇒ ≈ ×0,6–1,6) — Herleitung §3.4, Altersprofil gekennzeichnete Abschätzung [16,18,62]; herleitung:#r0-a |
| \(\text{rOR}\) | Verhältnis der Odds des Todes an Extremhitzetagen, Heime mit gegen ohne Klimaanlage (Maßnahme S157, §5) | — | 0,93 (0,87–0,99) = Kehrwert von 1,08 (1,01–1,15) [46]; register:95-S157-01 |
| \(r_{\text{KZ}},\ t_{\text{KZ}},\ w_{\text{KZ}}\) | öffentliche Kühlzentren: Reichweite (Anteil der Menschen ab 75 außerhalb der Heime, die an Hitzetagen hingehen) / geschützter Anteil des Tages / Wirkung bei Nutzern (Anteil ihres Exzesses, der wegfällt) | — | 0,05 (0,01–0,10), Setzung von KAP3 / 3/24 (2/24–6/24): 2 h Aufenthalt und 1 h Nachwirkung [73] / \(w_{\text{KZ}} = (1 - g_{\text{S157}}) \times t_{\text{KZ}}\) = 0,71 × 3/24 = 0,089, Abschätzung von KAP3 [46,73] (Befunde 139, 148); register:95-S157-02 |
| \(r_{\text{VG}},\ w_{\text{VG}}\) | Reichweite eines Schutzprogramms (Anteil der Menschen ab 75) / Wirkung bei Erreichten (Anteil des Exzesses, der wegfällt) | — | 0,20 (0,05–0,40), Setzung von KAP3 / 0,34 (0–0,68), Abschätzung von KAP3 = bereinigte Senkung des Anstiegs 24,4 Pp. ([70] Tabelle 3) geteilt durch den Anstieg ohne Programm 97,3 % und den Einschreibeanteil 0,728 (Befunde 128, 134); untere Grenze aus [70] Tabelle 2 (Befund 132), obere Grenze der rohe Unterschied 0,498 / 0,728 = 0,68; register:95-S152-03 |
| \(s_{\text{gek}}\) | gekühlter Anteil der Heimplätze der Kommune (Eingabe der Maßnahme, gilt für die ganze Kommune) | — | Voreinstellung **0,11** (Band 0,05–0,15), Abschätzung von KAP3 aus [71] und [72] (Block `heat.s_gek`, Befund 138); die Eingabe der Kommune im Produkt (`COOLING_ROOMS_DRINKING_WATER`) ersetzt sie; Beispiel 1 in §5; register:95-S157-01 |
| \(T_{0,\text{Region}}\) | Wirkschwelle Wochenmittel | °C | 19,7 / 20,2 / 20,8 (N/M/S), Winklmayr [11]; register:95-E02-01 |
| \(T_w\) | Wochenmitteltemperatur der Sommerwoche | °C | berechnet |
| \(\bar T_{\text{Zelle}}\) | Sommermitteltemperatur (24-h, §3.1) — Kartenebene | °C | DWD-CDC-Raster 1 km [33] + Stadtklima-Zuschlag, mittelwerttreu (§3.1); register:95-W124-01 |
| \(v_{\text{vers},a}\) | bandweiser Versorgungs-/Isolations-Modifikator (§3.3; Demografie steckt genau einmal in \(\text{pop}_a\)) | — | berechnet |
| \(\text{VOLY}\) | Wert eines verlorenen Lebensjahres | €₂₀₂₄ | 160.800 (Band 136,4–165,6 T€; Herleitung §3.5 [19]); herleitung:#voly |
| \(\text{YLL}_{\text{Zelle}}\) | verlorene Lebensjahre — **nativer Ausweis** | Jahre/Jahr | Ergebnis |
| \((x)_+,\ \mathbb{1}\) | Positivteil \(\max(0,x)\); Band-Indikator | — | Notation |
| \(\beta_a,\ \beta_{85+,\text{Region}}\) | RR-Steigung je Band; Basiswert 85+ je Region (Süd: Rev.-7-Nachschätzung) | K⁻¹ | **0,0634 / 0,0625 / 0,0876** (N/M/S; Süd = 0,0531 [11] × 1,65, Band 1,45–1,85); register:95-E02-01; herleitung:#beta-sued |
| \(\beta_d\) | Distanz-Effekt — **Sensitivitätsband, nicht im Basiswert** (Log 20) | 1/km | ≈ 0,001 (0–0,002) [38]; register:95-R36-01; Hilfsfrist [39] nur Screening |
| \(\beta_{\text{iso}}\) | Isolations-Effekt, OR-übersetzt: \((\text{OR}-1)/[1+\bar q(\text{OR}-1)]\); nur D-Pfad, Bänder 65+ | — | (2,3−1)/[1+0,346·1,3] = **0,90** (Band 0,3–1,4 = Übersetzung eines OR-Bands ≈ 1,4–3,7 — KI-Approximation, gekennzeichnete Abschätzung §3.9) [40,63]; register:95-S152-02 |
| \(\beta_{\text{pfl}}\) | Pflegeheim-Effekt (nur Band 85+, nur D-Pfad) | — | (3,0−1)/[1+0,149·2,0] = **1,54** (Band 1,0–2,9); Kette §3.3b [41,44,60,61]; register:95-S153-01 |
| \(\delta_{\text{HAP}}\) | Hitzeaktionsplan-Dämpfung — multiplikativ auf den Wochen-Exzess (RR−1); Maßnahme §5 | — | 0,95 (0,85–1,00) [45,47]; register:95-S158-01 |
| \(\delta_{\text{KZ}}\) | Dämpfung durch öffentliche Kühlzentren — multiplikativ auf den Wochen-Exzess der Bänder 75–84 und 85+ (85+ ohne Heimbewohner); Maßnahme §5 | — | 0,9956 (0,982–0,9994) = 1 − \(r_{\text{KZ}} \times w_{\text{KZ}}\) = 1 − 0,05 × 0,089; Abschätzung von KAP3 [41,46,73] (Block `heat.delta_kuehlzentren`, Befunde 139, 148); register:95-S157-02 |
| \(\delta_{\text{VG}}\) | Dämpfung durch Schutzprogramme vulnerable Gruppen — multiplikativ auf den Wochen-Exzess der Bänder 75–84 und 85+ (85+ ohne Heimbewohner); Maßnahme §5 | — | 0,931 (0,794–1,0) = 1 − \(r_{\text{VG}} \times w_{\text{VG}}\) = 1 − 0,20 × 0,3445 (\(w_{\text{VG}}\) ungerundet, gerundet 0,34), Wirkung höchstens bis zum Paketwert 0,794 [47]; Abschätzung von KAP3 [47,70]; register:95-S152-03 |
| \(\delta_{\text{VG,morb}}\) | Faktor der Schutzprogramme auf die Einweisungen (Morbidität) der Bänder 75–84 und 85+ ohne Heimbewohner; Maßnahme §5 | — | 1,0 (0,931–1,069), Abschätzung von KAP3: unten wie \(\delta_{\text{VG}}\), oben 1 + \(r_{\text{VG}} \times w_{\text{VG}}\) = 1 + 0,20 × 0,3445 = 1,069 (\(w_{\text{VG}}\) ungerundet; Befunde 131, 134); register:95-S152-03 |
| \(\Delta D_{\text{KZ}}\) | vermiedene Todesfälle 75–84 und 85+ außerhalb der Heime durch öffentliche Kühlzentren | 1/Jahr | berechnet (§5) |
| \(\Delta D_{\text{S157}}\) | vermiedene Todesfälle 85+ durch gekühlte Heimplätze | 1/Jahr | berechnet (§5) |
| \(\Delta D_{\text{VG}}\) | vermiedene Todesfälle 75–84 und 85+ außerhalb der Heime durch Schutzprogramme | 1/Jahr | berechnet (§5) |

**Datenebenen der \(v_{\text{vers}}\)-Zellgrößen** (Rev. 8; §3.1-Datenebenen-
Anlagepflicht der Aufgabe, ersetzt die Rev.-5-Fallback-Definitionen aus Befund 25 —
Verifikationsergebnis der Integration 30.08.2026: keine der beiden Zellgrößen war
produktseitig verfügbar):

- **\(q_{\text{pfl}}\) — Ebene `CARE_HOME_SHARE_85P` („neu anzulegen"; wird von
  `/integriere-risiko` angelegt):** Quelle OSM-Pflegeeinrichtungen
  (`amenity=nursing_home` sowie `social_facility=nursing_home|assisted_living`),
  keyless über den bestehenden kommunalen OSM-Ingest (kein nationaler Lauf).
  Zell-Ableitungsregel: Einrichtungs-Gewicht \(w_z\) je Zelle — Polygone mit
  ihrer Grundfläche in m², Punkt-Features mit dem **Mindestgewicht 400 m²**
  (typische Grundfläche eines kleinen Pflegeheims; auch Polygone werden auf
  dieses Minimum angehoben, damit Punkt- und Flächen-Tagging vergleichbar
  wiegen — gekennzeichnete Setzung); verteilt wird **nur über Zellen mit
  \(\text{pop}_{85+,z} > 0\)** (Heim-Gewichte in Zellen ohne erfasste
  85+-Bevölkerung — Zensus-Geheimhaltung kleiner Besetzungen — werden der
  Gewichtssumme entzogen, kein stiller Verlust an der Kappung); die
  Heimbewohner der Kommune
  \(\bar q_{\text{pfl}} \cdot \text{pop}_{85+,\text{Kommune}}\) werden
  proportional \(w_z\) auf diese Zellen verteilt; \(q_{\text{pfl},z} =
  \min(1, \text{Heimbewohner}_z / \text{pop}_{85+,z})\). **Normierung:** per
  Konstruktion kommunen-erwartungstreu (\(\sum_z q_{\text{pfl},z}\,
  \text{pop}_{85+,z} = \bar q_{\text{pfl}}\,\text{pop}_{85+}\), vor Kappung) —
  kalibrierneutral je Kommune; die Kappung bei 1 ist ein kleiner, dokumentierter
  Restfehler. **Bewusste Fortschreibung von Befund 25(b):** statt Skalierung auf
  Kreis-Summen der Pflegestatistik (Tab. 22421 je Kreis ist nicht keyless
  abrufbar) die Kommunen-Erwartungstreue mit dem Bundesmittel — regionale
  Heimquoten-Unterschiede zwischen Kommunen bleiben ununterschieden (Proxy,
  gekennzeichnet; Log 35). Fallback: Kommune ohne OSM-Pflegeeinrichtung →
  \(q_{\text{pfl}} = \bar q\) (OSM-Lücke nicht von „keine Heime"
  unterscheidbar — dokumentiert).
- **\(q_{\text{1P}}\) — Ebene `SINGLE_HH_SHARE_65P` („geparkt — Datenquelle
  fehlt"; §3.1):** Es existiert keine offene Zellquelle (Zensus-2022-Gitter ohne
  1P×65+-Kreuzung und ohne Gesamt-1P-Anteil; Mikrozensus nur Bundesebene).
  Bis zur Beschaffung gilt \(q_{\text{1P}} = \bar q_{\text{1P}}\) (Faktor 1,
  kalibrierneutral). **Watchlist:** Zensus-Gitterdaten-Nachlieferungen
  (destatis.de/gitterdaten) und Zensus-Datenbank-Haushaltstabellen auf
  Gemeinde-/100-m-Ebene; bei Verfügbarkeit greift Befund 25(a)
  (Gesamt-1P-Anteil × Alterskorrektur) bzw. die direkte Kreuzung.

### 3.7 Schicht A (getrennt; nie auf €-Pfaden)

Screening-Index über die kuratierten Ketten: \(\hat H\)(E02: HEAT_WAVE) × \(\hat E\)(R35:
POPULATION_DENSITY / AGE_STRUCTURE / VULNERABLE_GROUPS_POPULATION) × \(\hat V\)(S152–S158:
HEALTHCARE_ACCESS / HEAT_SENSITIVITY); \(\text{Index}=100\cdot\max_p(w_p\hat H_p\hat E_p\hat V_p)\)
(Worst-Pathway-Prinzip; Normierungen editierbar, testseitig von €-Pfaden getrennt).

## 4 Kalibrierung & Validierung (§2.4/§3.4)

**Begriff definiert** (Befund 21): „konservativ" heißt in diesem Bericht durchgängig
**unterschätzend** (Untergrenze), wie in §1.2 des M0-Rahmens.

**Nationaler Anker Mortalität** — revidierte RKI-Reihe (Epid Bull 19/2025, Anhang 1, CC BY);
**Auswahl der markanten Jahre** (Befund 63 — die vollständige Reihe steht in der xlsx-Anlage
`rki_eb19_2025_anhang_bundeslaender.xlsx`, die Fits nutzen **alle** signifikanten Jahre des
jeweiligen Fensters — 13 bzw. 26 Jahre, Einzeljahre in `c_kal_rev6_ergebnis.md`):
1994: 10.200 · 2003: 10.200 · 2006: 7.700 · 2010: 4.090 · 2013: 3.500 · 2015: 7.000 ·
2018: 8.500 · 2019: 6.800 · 2020: 3.700 · 2022: 4.500 · 2023: 3.100 · 2024: 2.800.
2025 (≈ 2.500, Wochenbericht KW 38) ist **vorläufig** und geht nicht in die Basis ein
(Befund 24; Sensitivität unten); 2026 (laufend) ausgeschlossen. Signifikant = untere
Prädiktionsgrenze > 0. Kommunale Zusatz-Anker: Hessen 2018 ≈ 920 / Berlin 2018 ≈ 460
(85+: 260–320 je 100.000 [14]) [11–14].

**Kalibrierbasis Rev. 7 — bevölkerungsgewichtete Sommermittel** (Anker `#t-povw`;
Auflösung der Befund-1-Hauptkomponente ohne Zell-Lauf): Die Kalibrier-Zeitreihen sind ab
Rev. 7 **bevölkerungsgewichtete** Sommermitteltemperaturen je Bundesland und Jahr —
DWD-CDC-JJA-Raster (1 km) am Repräsentanzpunkt jeder der **10.853** Gemeinden mit
Zensus-2022-Bevölkerung [65, 66] (96 VG250-Gemeinden ohne Zensus-Eintrag übersprungen; Daten-Pins
im Ergebnis-MD: `zensus_gemeinde.json` sha256 `124fd7a7a15b`, `DE_VG250.gpkg` sha256
`f229550c8018`) (Skript `calibrate_heat_mortality_rev7.py`, Anlagen
`sommermittel_bundesland_povw.csv`, `temperatur_offsets_bundesland.csv` [50]). Damit ist
die dominante Näherungsfehler-Komponente des Rev.-6-Laufs (Bevölkerung wohnt wärmer als
das Landes-Flächenmittel) **direkt gemessen statt pauschal korrigiert** — die
×0,82-Zentralkorrektur und ihr Band entfallen. Gemessene Offsets (bevölkerungsgewichtet −
Flächenmittel, Ø 1992–2024): **Deutschland +0,53 K**; stark heterogen (Hessen +1,05 ·
BW +0,84 · Berlin +0,85 · BY +0,57 · MV +0,01 K) — die Rev.-6-Abschätzung (+0,2…+0,4 K)
war zu niedrig, genau wie der Kovarianz-Vorbehalt (Befund 67) vermutete.
**Verbleibender dokumentierter Rest** (Fortschreibungsvermerk **kommunale
Stichproben-Abgleiche** — §3.4-Ressourcen-Regel: ein nationaler
100-m-Vollraster-Lauf ist als Prüf-/Abgleichinstrument unzulässig (Log 34);
nicht abnahmerelevant): UHI-Feinstruktur unterhalb der Gemeinde — Konvexitätsbeitrag als
**Modellrechnung gegen die weiterhin gesetzte** Streuung σ = 0,5 K: ×1,023–1,024
(mittelwerttreu; σ-Abschätzung wie in Rev. 6 aus der ±1-K-Spanne der Zellabweichungen um
das Gebietsmittel, Gleichverteilungsannahme ⇒ σ ≈ 2/√12 ≈ 0,5 K — **keine Messung**;
der Messpfad „σ aus dem Stadtmodell" gehört zum Stichproben-Abgleich) — sowie
intra-kommunale Bevölkerungsgewichtung.

**Kalibrierlauf Rev. 7** (Ergebnis `c_kal_rev7_ergebnis.md` [50]; Produktionsnähe:
Gemeindepunkt-Temperaturen aus derselben DWD-Rasterfamilie, die das Produkt je Zelle
nutzt):

- **Fit: ein nationaler Skalar \(c_{\text{kal}}\) = 0,581** (Anker `#c-kal`) — Kleinste
  Quadrate durch den Ursprung, **Fenster 2012–2024** (13 signifikante Jahre; R² = 0,65;
  8/13 Jahre im RKI-PI), mit nachgeschätzter Süd-ERF (s. u.). Das Fenster enthält die
  Prüfjahre 2018/2019/2022 — der Niveau-Skalar selbst ist damit **in-sample** gefittet
  (präzise Kennzeichnung, Befund 78; Voll-Holdout-Variante s. Verteilungsprüfung).
  Sensitivitäten: ohne Süd-Nachschätzung 0,661; Vollreihe 1992–2024: 0,660; inkl.
  vorläufigem 2025: **0,651** (povw-Reihe hierfür bis 2025 verlängert — 2025 bleibt
  außerhalb der Basis; Befund 77); Voll-Holdout (Fenster ohne 2018/19/22): **0,567**.
  **Band [0,55, 0,67]** — außenrundend aus der Stützen-Spanne 0,559–0,661: Untergrenze
  aus dem \(s_{\text{Süd}}\)-Profil-Band (s_Süd = 1,85 → c = 0,559; 1,45 → 0,604),
  Obergrenze aus ohne-Süd-/Vollreihen-Sensitivität (0,661/0,660); die Voll-Holdout-Stütze
  0,567 liegt im Band (Befund 80). Begründung der
  Fensterwahl unverändert (Befund 21, empirisch): der **zeitliche Holdout** (Fit
  1992–2015 → Prüfung 2016–2024) trifft out-of-sample nur 2/9 Jahre im PI und überschätzt
  systematisch (+7…+185 %) — die Vollreihe extrapoliert die heutige ERF-Ära schlecht.
  Es gibt **keine Pauschalkorrektur und keine regionalen Übergangsfaktoren mehr** —
  genau ein Skalar (§3.4).

- **ERF-Nachschätzung Süd** (Anker `#beta-sued`; §3.4-konforme Antwort auf die
  Rev.-6-Schieflage — „Wirkungsfunktion regional nachschätzen, nicht die Kalibrierung
  regionalisieren"): Ein multiplikativer Skalar \(s_R\) auf \(\beta_{85+,R}\),
  gefittet per Kleinste-Quadrate auf den Log-Verhältnissen der signifikanten
  Bundesland-Jahre 2012–2024 **ohne die Validierungsjahre 2018/2019/2022** (Holdout).
  **Identifikationsdiagnose** (Zielfunktionsprofile im Ergebnis-MD): Nord hat im Fit-Set
  **0** signifikante Land-Jahre (Profil flach — nicht identifizierbar, bleibt 1,0);
  Mitte-Optimum liegt exakt bei 1,0 (bleibt 1,0; 12 Beobachtungen); Süd ist mit 7
  Beobachtungen klar identifiziert (parabolisches Minimum): \(s_{\text{Süd}}\) =
  **1,65** (Profil-Band 1,45–1,85 — gekennzeichnete Bandregel nach §3.9, kein formales
  Konfidenzintervall: Bandränder dort, wo die Fit-Zielfunktion höchstens +10 % über dem
  Minimum liegt — Profilwerte 1,51 / 1,38 / 1,48 bei s = 1,45 / 1,65 / 1,85; die nächsten
  Gitterpunkte 1,35 / 1,95 liegen mit +20 / +16 % klar darüber) ⇒
  \(\beta_{85+,\text{Süd}} = 0{,}0531 \times 1{,}65 = \mathbf{0{,}0876}\) K⁻¹
  (Nord/Mitte unverändert 0,0634/0,0625). Einordnung: Die Nachschätzung ist ein
  **modellinterner** Parameter (ERF im Kontext bevölkerungsgewichteter Wochenmittel und
  empirischer Quantile), keine Korrektur der Winklmayr-Kurve; der Ablesewert 0,0531
  bleibt als Kettenstart dokumentiert (§3.3, Test `beispiel_95_beta_ablesekette`).
  **Benannter Widerspruch (§3.8, Befund 79):** die Nachschätzung **kehrt die publizierte
  Regionen-Rangfolge um** — bei Winklmayr ist Süd die flachste Kurve (0,0531;
  Adaptions-Deutung), nachgeschätzt die mit Abstand steilste (0,0876; effektives RR bei
  25 °C Wochenmittel ≈ 1,45 statt publiziert 1,25). Epidemiologisch ist das darum
  **nicht** als korrigierte Süd-ERF lesbar, sondern nur als Kompensationsparameter für
  Süd-spezifische Skalenstruktur (Topographie-Mischung kühler Voralpen- und warmer
  Ballungsräume selbst im bevölkerungsgewichteten Landesmittel); kommunale
  Stichproben-Abgleiche (Anker-Kommunen im Alpenvorland/Oberrheingraben, §3.4-
  Ressourcen-Regel) prüfen, welcher Anteil davon Topographie ist. Physikalische Deutung des BY/BW-Kontrasts
  (Alpenvorland vs. Oberrheingraben) siehe Verteilungsprüfung.

```python test: beispiel_95_beta_sued_nachschaetzung
# Rev. 7: beta_85+,Sued = Winklmayr-Ablesewert x Nachschaetzungs-Skalar (Holdout-Fit, §4)
assert abs(0.0531 * 1.65 - 0.0876) < 0.0001
# Nord/Mitte unveraendert (Identifikation: Nord 0 Fit-Jahre, Mitte-Optimum 1,0)
assert abs(0.0634 * 1.0 - 0.0634) < 1e-9 and abs(0.0625 * 1.0 - 0.0625) < 1e-9
```

- **Verteilungsprüfung / Kalibrier-Prüfstein — BESTANDEN** (Prüfgröße: Σ der Hitzejahre
  2018/2019/2022; ein nationaler Skalar, einheitlicher Signifikanzfilter): **12/16 Länder
  im Band 0,75–1,35** (Anforderung ≥ 11/16; Daten `c_kal_rev7_verteilung.csv`).
  **Out-of-sample-Kennzeichnung präzise (Befund 78):** out-of-sample ist die
  **Süd-Nachschätzung** (Fit-Jahre disjunkt von 2018/19/22); der Niveau-Skalar 0,581 ist
  auf dem Fenster **einschließlich** der Prüfjahre gefittet. Die strenge
  **Voll-Holdout-Variante** — auch der Niveau-Skalar ohne 2018/19/22 gefittet
  (c = 0,567) — besteht den Prüfstein ebenfalls mit **12/16**; das Bestehen hängt damit
  nicht an der In-Sample-Niveauwahl und ist in dieser Variante vollständig
  out-of-sample belegt. Die vier Restausreißer sind
  physikalisch erklärt: **SH 1,80 / HH 1,60** (kleine Fallzahlen, Küstenklima,
  DWD-Kombi-Gebietsmittel — wie in Rev. 6), **BY 1,43** (Alpenvorland-Feinstruktur:
  selbst das bevölkerungsgewichtete Landesmittel mischt kühle Voralpen- und warme
  Ballungsräume — das löst erst das Zellmodell), **BB 1,42** (knapp; Berlin-Umland-
  Pendlerstruktur). Die Rev.-6-Süd-Schieflage (Faktor ≈ 2) ist aufgelöst: BW 0,90 ✓.
  Die regionalen Diagnose-Faktoren (0,66–0,77) dienen nur noch der Beobachtung — **kein
  Produktausweis über Übergangsfaktoren mehr**.

- **Validierung Altersverteilung** (Ist-Ergebnis, Fenster 2012–2024): modellierte
  Bandanteile **6,3 / 12,6 / 24,7 / 56,4 %** vs. RKI 6,5 / 12,9 / 25,2 / 55,5 % — alle
  Bänder < 1 Prozentpunkt Abweichung (Toleranz ±5 pp, vorab fixiert: **bestanden**).
  Einschränkung unverändert: teilzirkulär (\(f_a\)-Rückrechnung), daher zusätzlich:

- **Zusatz-Anker** Berlin 2018, Band 85+ (nationaler Skalar 0,581): Modell =
  **221 je 100.000** gegen die RKI-Referenz 260–320 [14] — **unterschätzend (−15 %)**
  gegen die Untergrenze 260, etwas stärker als in Rev. 6 (−11 %). **Richtung gemessen**
  (Zellvergleich §3.0, Skript `docs/methodik/anlagen/95_zellvergleich.py --gemeinde 11000000`,
  Ledger Runde 16): Der Berlin-Gemeindepunkt (20,06 °C im Mittel 2016–2025) liegt 0,1 K
  über dem Bevölkerungsmittel der Zellen (19,96 °C). Für den Anker zählen nur die zwei
  Wirkungen, die den Gemeindepunkt betreffen: Temperatur je Zelle × 0,948 und Feinstruktur
  σ = 0,5 K × 1,021, zusammen × 0,967. Das Zellmodell liegt damit nicht über, sondern
  **unter** dem Gemeindepunkt-Wert: 221 × 0,967 ≈ **214 je 100.000**, also rund **−18 %**
  gegen die Untergrenze 260 (214 / 260 = 0,82). Die übrigen Wirkungen aus §3.0 (Einwohnersumme,
  Bänder je Zelle) betreffen die Bevölkerungsgrundlage, nicht den Gemeindepunkt. **Die Lücke
  bleibt unerklärt:** Die Wärmeinsel erklärt sie nicht, und der Bericht hat dafür keine
  gemessene Ursache; sie steht als offene Abweichung, nicht als Korrektur. Der Anker bleibt ein
  Anker, kein Wert aus Kapitel 7 ändert sich. Die Aussage bleibt „konservativ =
  unterschätzend": Das Modell liegt für Berlin unter der RKI-Referenz, nicht darüber.

- **Anker Morbidität / Sanity-Band:** Untergrenze Destatis T67 (Ø 1.400–1.500/Jahr, 2003:
  2.600); Obergrenze K&Z ≈ +2.500 Einweisungen/Hitzetag (Größenordnung 20.000±/Jahr).
  Modell-Bundessumme: Baseline 83,456 Mio. × 3,54/100.000 ≈ **2.950 Fälle/Jahr**; in einem
  Hitzejahr (+5 Tage über \(\text{HD}_{\text{ref}}\)) ≈ 3.300 (mit \(e_{\text{HD}}\)-
  Obergrenze 0,054: ≈ 3.750) — **innerhalb des Bands** [16,18].
- **Verteilschlüssel-Test (§3.1):** strikt bottom-up; die RKI-Reihe geht nur als
  Kalibrierskalar ein. **Mortalität:** Kommune ohne Hitzesignal → ~0 ✓. **Morbidität**
  (Befund 59a): Der nicht-wetterliche Baseline-Sockel ist bevölkerungsproportional und wird
  über den HD-Term nur moduliert (HD = 0 → ×0,83) — dokumentierte Grenze §3.4, keine
  Verteilschlüssel-Logik (kein nationaler Topf wird verteilt; die Zellrate ist lokal
  definiert).
- **Unsicherheiten:** Rest-Bias UHI-Feinstruktur (×1,02-Konvexität + intra-kommunale
  Gewichtung; kommunale Stichproben-Abgleiche als Fortschreibungsvermerk — §3.4-
  Ressourcen-Regel, kein nationaler Vollraster-Lauf);
  \(s_{\text{Süd}}\)-Profil-Band 1,45–1,85 (⇒ \(c_{\text{kal}}\) 0,604–0,559, Gegenläufigkeit,
  Bundessumme stabil); σ-Schätzgüte der Wochenquantile; Skalentransfer Region→Zelle;
  \(\bar e(95{+})\)-Restnäherung der exakten \(\bar L_{85+}\)-Rechnung (Band
  [4,16, 4,20], §3.5 — die frühere Approximation ist per Log 36 ersetzt);
  Harvesting (Jahresaggregat). Der
  Kovarianz-Vorbehalt (Befund 67) ist durch die direkte Messung der
  Bevölkerungsgewichtung materiell aufgelöst; die verbleibende Kovarianz
  (\(v_{\text{vers}}\) × UHI-Feinstruktur) wandert in den Rest-Bias.

## 5 Maßnahmen-Hebel (§2.5/§3.5)

Konservative **Interventionseffekte** (nicht Teil des Basiswerts); Fall-Kontroll-ORs
(Bouchama: Klimaanlage 0,23) sind keine Einführungswirkungen:

- **Hitzeaktionsplan / Frühwarnkette (S155/S158):** \(\delta_{\text{HAP}}\) zentral 0,95
  (Band 0,85–1,00), **definiert als multiplikativer Faktor auf den Wochen-Exzess (RR − 1)**
  — konsistent zur Studienart der Evidenz (Ergebnis-Effekte; Befund 33; die frühere
  β-Formulierung ist gestrichen; Anwendung auf β wiche je nach Wochenhitze um bis zu
  0,7 %-Punkte ab). Evidenz: DiD 15 dt. Städte RR 1,00 [0,98–1,01], adjustiert 0,85 [45];
  Europa-Analyse [47] (Zahlen korrigiert, Befund 68): HAF-Reduktion durch Präventionspläne
  **25,2 % [19,8–31,9]** (regional −11,9…−33,2 %, Länderspanne −10…−43 %; ohne 2003:
  15,2 % [4,1–23,7]) — das ist der **Einführungseffekt** über drei Jahrzehnte, nicht der
  marginale Spielraum gegenüber dem heutigen deutschen Stand; der Basiswert
  \(\delta_{\text{HAP}}\) = 0,95 (Band 0,85–1,00) bleibt daher [45]-gestützt und marginal.
  **Doppelzählungs-
  Wächter:** \(c_{\text{kal}}\) ist auf Jahre mit laufendem DWD-Warnsystem kalibriert — die
  durchschnittliche Warnwirkung steckt im Basiswert; ein Fouillet-großer Hebel (≈ 4.400
  Fälle [42]) würde doppelt buchen. Wählt die Kommune zugleich Schutzprogramme für vulnerable
  Gruppen, gilt auf den Bändern 75–84 und 85+ die Kappung am Paketwert, die beim Hebel
  \(\delta_{\text{VG}}\) steht (Befund 126). Wählt sie zugleich gekühlte Heimplätze (S157), wirkt
  \(g_{\text{S157}}\) auf den schon mit \(\delta_{\text{HAP}}\) gedämpften Heim-Exzess (Regel beim Hebel
  S157, Befund 129).
- **Gekühlte Räume / Klimaanlagen in Pflegeheimen (S157):** rOR ≈ 0,93 an Extremhitzetagen
  (Ontario [46]; Block `heat.ror_s157`, Befunde 122 und 124). **Was [46] misst:** 73.578 Todesfälle
  in 615 Heimen; an Extremhitzetagen (ab dem 90. Perzentil des Hitzeindex) steigen die Odds des Todes
  ohne Klimaanlage auf 1,11 (1,06–1,16), mit Klimaanlage auf 1,03 (0,98–1,07); das Verhältnis ohne
  gegen mit ist 1,08 (1,01–1,15), umgekehrt gelesen 0,93 (0,87–0,99). Der Faktor wirkt also auf das
  ganze Sterberisiko am Hitzetag. **Übersetzung auf den Exzess** (Abschätzung von KAP3, Block
  `heat.g_s157`): \(g_{\text{S157}} = (\text{rOR} \times \text{OR}_{\text{ohne}} - 1)/(\text{OR}_{\text{ohne}} - 1)
  = (0{,}93 \times 1{,}11 - 1)/0{,}11 = 0{,}29\): Mit Klimaanlage bleiben 29 % des Hitze-Exzesses,
  71 % fallen weg (Band 0–0,90 aus dem Band von rOR). Gesetzt ist, dass derselbe Anteil in allen
  Hitzewochen des Modells gilt, nicht nur an den Extremtagen von [46].
  **Warum \(\text{OR}_{\text{ohne}}\) = 1,11 fest bleibt (Befund 132):** Auch \(\text{OR}_{\text{ohne}}\) hat in [46]
  ein Konfidenzintervall, 1,06–1,16. Bei rOR 0,93 liegt \(g_{\text{S157}}\) damit zwischen 0 und
  \((0{,}93 \times 1{,}16 - 1)/0{,}16 = 0{,}49\). Zieht man beide Intervalle aus [46] zugleich (OR mit Klimaanlage
  0,98–1,07, ohne 1,06–1,16; beide log-normal und unabhängig), liegen 95 % der Werte zwischen 0 und 0,83 (97,5-%-Punkt
  0,833, nachgerechnet im Beispiel-Block `s157_berlin`). Beides liegt im Band 0–0,90; das Band
  ist also nicht enger, als [46] es trägt. Nur die Ecke rOR 0,99 mit \(\text{OR}_{\text{ohne}}\) 1,16 ergäbe 0,93;
  sie ist nicht angesetzt, weil ein hohes \(\text{OR}_{\text{ohne}}\) bei gleichem OR mit Klimaanlage rOR senkt, nicht hebt.
  **Formelzeile:**
  \(\Delta D_{\text{S157}} = D_{85+} \times h_{\text{Heim}} \times s_{\text{gek}} \times (1 - g_{\text{S157}})\),
  mit \(h_{\text{Heim}} = \bar q_{\text{pfl}} \times [1 + \beta_{\text{pfl}}(1 - \bar q_{\text{pfl}})] = 0{,}344\)
  (Anteil der Heimbewohner an den Todesfällen 85+, §3.0; je Zelle siehe unten) und \(s_{\text{gek}}\) dem gekühlten
  Anteil der Heimplätze, den die Kommune angibt; ohne Eingabe gilt die Voreinstellung 0,11 (unten). Der Faktor wirkt
  nur auf den Exzess des Bands 85+ und nur im gekühlten Anteil; die Basissterblichkeit und die übrigen Bänder bleiben
  unberührt. Andockpunkt im Produkt: Maßnahme `COOLING_ROOMS_DRINKING_WATER` („Kühle Räume / Kühlzentren").
  **Stand im Produkt (Befund 130, fortgeschrieben mit Befund 138):** Bis zur Integration war die Maßnahme geparkt
  (`backend/app/data/catalog_parked.py`) und hatte keine Wirkung, auch keine Nullwirkung; der geparkte Katalog setzte
  `default_reduction` 0.18 auf die Exposition. Seit der Integration (T-1367-cto) steht sie in
  `backend/app/data/catalog.py` ohne `default_reduction` und rechnet \(g_{\text{S157}}\) = 0,29 auf den Heim-Exzess;
  bis zur Voreinstellung zeigte sie ohne Eingabe der Kommune keinen Betrag (Log 44, fortgeschrieben durch Nr. 45).
  **Voreinstellung \(s_{\text{gek}}\) = 0,11 (Abschätzung von KAP3, Block `heat.s_gek`, Befund 138).** Eine
  Nullwirkung ist keine Voreinstellung (P2). Gibt die Kommune nichts ein, gilt:
  \(s_{\text{gek}}\) = 11 % der Pflegeheime mit Klimaanlage [71] × 1 = 0,11. Der Faktor 1 enthält zwei Setzungen von
  KAP3: Heime mit und ohne Klimaanlage sind gleich groß, und in einem Heim mit Klimaanlage sind alle Plätze gekühlt.
  **Band 0,05–0,15.** Unten die Hälfte, weil manche Heime nur einzelne Aufenthaltsräume, Speisesäle oder Flure kühlen
  [71] und die Umfrage mit 140 Rückmeldungen nicht repräsentativ ist. Oben 14,5 % der im Jahr 2025 fertiggestellten
  Gebäude des Sozialwesens mit einer Anlage zur Kühlung [72], außen gerundet; Setzung von KAP3: Der ältere Bestand an
  Heimen ist nicht besser ausgestattet als die Neubauten. **Sensitivität:** Berlin (Kette) 25,0 Mio. € × 0,11 = **2,7 Mio. € je
  Jahr** (Preisstand 2024; Band 1,2–3,7 Mio. €, 0,3–1,0 % des Jahresbetrags 362,9 Mio. €); im Zelllauf mit Gemeindeschlüssel 2,4 Mio. €;
  Warmsen (Zelllauf) 1.032 € je Jahr (Band 469–1.407 €). Gemessen mit `docs/methodik/anlagen/95_zellvergleich.py
  --ersatz`, YLL 85+ im Zelllauf: Berlin 556,27, Warmsen 0,2398 (27.09.2026; Beispiel-Block `s157_voreinstellung`).
  Gibt die Kommune ihren eigenen Anteil ein, gilt dieser. **Modellgrenze:** \(s_{\text{gek}}\) gilt für die ganze
  Kommune, unabhängig von der gezeichneten Fläche. Welche Heime gekühlt sind, weiß weder der Bericht noch das Produkt;
  eine Kommune mit bekannten gekühlten Heimen gibt deren Anteil an allen Heimplätzen der Kommune ein.
  **\(h_{\text{Heim}}\) je Zelle (Block `heat.h_heim`, Befund 146).** Das Produkt führt den Heimanteil
  \(q_{\text{pfl},z}\) je Zelle (Ebene `CARE_HOME_SHARE_85P`, §3.6). Dort gilt
  \(h_{\text{Heim},z} = q_{\text{pfl},z} \times [1 + \beta_{\text{pfl}}(1 - \bar q_{\text{pfl}})] / [1 + \beta_{\text{pfl}}(q_{\text{pfl},z} - \bar q_{\text{pfl}})]\):
  Heimbewohner der Zelle mal ihr Sterbefaktor, geteilt durch den Sterbefaktor aller Menschen ab 85 der Zelle, also
  dieselben Faktoren wie in \(v_{\text{vers}}\) (§3.3). Beispiel: eine Zelle mit \(q_{\text{pfl}}\) = 0,5 hat
  0,5 × 2,31 / (1 + 1,54 × 0,351) = 1,155 / 1,541 = 0,75. Bei \(q_{\text{pfl},z} = \bar q_{\text{pfl}}\) ergibt die Formel
  0,149 × 2,31 / 1 = 0,344; das ist der Rückfallwert für Zellen ohne eigenen Wert (Kommune ohne OSM-Pflegeeinrichtung,
  §3.6). Über die Kommune summiert zählt die Zellrechnung dieselben Heim-Todesfälle wie 0,344 × \(D_{85+}\), solange
  Heime nicht systematisch in wärmeren Zellen liegen (§3.0 Ebene 6, Obergrenze +5,8 %). **Was 0,344 in jeder Zelle
  verfälschen würde:** Eine Zelle ohne Heim bekäme Heim-Todesfälle und damit eine Wirkung von S157 zugeschrieben, eine
  Heimzelle zu wenig; die Karte zeigte die Wirkung am falschen Ort. Die Zellformel gilt überall, wo \(h_{\text{Heim}}\)
  steht (S157, Schutzprogramme, Kühlzentren).
  **S157 mit seiner Voreinstellung im Anpassungspotenzial (Befund 149).** Die Charakterisierung im Produkt zählt je
  Maßnahme, um welchen Anteil sie die ganze Hitzemortalität senkt. Für S157 bei der Voreinstellung ist das
  \(r_{\text{S157}} = a_{85+} \times h_{\text{Heim}} \times s_{\text{gek}} \times (1 - g_{\text{S157}})\)
  = 0,284 × 0,344 × 0,11 × 0,706 = 0,0076, mit \(a_{85+}\) = 638,8 / 2.250 YLL = 0,284, dem Anteil des Bands 85+ an den
  YLL der Rechenkette (§3.0 Ebene 7). Mit dem Hitzeaktionsplan (1 − 0,95 = 0,05) ergibt das
  1 − 0,95 × (1 − 0,0076) = 0,057 statt 0,050 ohne S157. \(a_{85+}\) hängt am Altersaufbau: In Warmsen ist er 0,224
  (Zelllauf), \(r_{\text{S157}}\) dann 0,0060 und das Anpassungspotenzial 0,056; die Gruppe nach KWRA (unter 0,1)
  ändert sich in beiden Fällen nicht. Anzeige und Quelle in der Parameterliste regelt T-1410-ceo. **Berlin**
  (Beispiel-Block `s157_berlin`, Kapitel 7): 153,6 Todesfälle 85+ × 0,344 = 52,9 Todesfälle von
  Heimbewohnern; sind alle Heimplätze gekühlt, fallen 52,9 × 0,71 = 37,4 weg, das sind 155 YLL und
  **25,0 Mio. € je Jahr** (Band 3,6–35,4 Mio. €); bei einem gekühlten Anteil von 10 % ein Zehntel davon.
  **Zusammen mit dem Hitzeaktionsplan (Befund 129):** \(\delta_{\text{HAP}}\) dämpft den Exzess aller
  Bänder, also auch den Heim-Exzess. Wählt die Kommune beide Hebel, wird \(\Delta D_{\text{S157}}\) deshalb
  aus \(D_{85+} \times \delta_{\text{HAP}}\) gerechnet statt aus \(D_{85+}\): Die beiden Faktoren werden
  multipliziert, nicht ihre Wirkungen addiert. Berlin, alle Heime gekühlt: Zusammen fallen
  1 − 0,95 × 0,294 = 72,1 % des Heim-Exzesses weg, das sind 38,1 der 52,9 Todesfälle. Davon entfallen
  auf S157 52,9 × 0,95 × 0,706 = 35,5 Todesfälle oder 23,7 Mio. € je Jahr. Addiert man stattdessen
  5 % und 70,6 %, wären es 75,6 %, also 1,9 Todesfälle oder 1,2 Mio. € je Jahr doppelt gebucht, bei
  \(\delta_{\text{HAP}}\) = 0,85 schon 3,7 Mio. €.
  **Beide Fassungen (Befund 124):** Legte man 0,93 unmittelbar auf den Exzess, fielen nur 7 % weg,
  2,5 Mio. € je Jahr, rund ein Zehntel. Das ist einfacher zu lesen, stellt [46] aber falsch dar, weil
  der Faktor dort das ganze Risiko am Hitzetag senkt; gewählt ist deshalb die Übersetzung.
  **Modellgrenze:** [46] misst Klimaanlagen in den Wohnbereichen der Heime; ein einzelner gekühlter
  Aufenthaltsraum oder ein öffentliches Kühlzentrum schützt weniger, weil nicht alle Bewohner ihn
  nutzen. Das trägt die Kommune über \(s_{\text{gek}}\) ein (nur tatsächlich gekühlte Heimplätze
  zählen). Öffentliche Kühlzentren außerhalb der Heime rechnet der eigene Hebel unten (\(\delta_{\text{KZ}}\), Befunde
  139 und 148); der Faktor aus [46] gilt dort nur für die Stunden im gekühlten Raum. **R7-Weiche**
  (Befund 53): Die Wirkung gilt nur für den gekühlten Bestandsanteil; je Einheit gilt
  Entweder-oder gemäß R7 („100-%-Regel je Raumbestand", Weiche des Treibers #63) — ab
  Stufe M5 bucht #65 die Kühl-Mehrkosten (K8), der Übergabepunkt ist dort zu referenzieren;
  keine Doppelbuchung „vermiedener Schaden + Vorsorgekosten".
- **Öffentliche Kühlzentren (Knoten S157, außerhalb der Heime; Befunde 139 und 148):** gekühlte, öffentlich
  zugängliche Räume für ältere Menschen, die zu Hause leben (kühle Orte, Kälteinseln in Gemeinderäumen, Kirchen oder
  Bibliotheken). Faktor \(\delta_{\text{KZ}}\) auf den Wochenexzess derselben Menschen wie beim Hebel Schutzprogramme
  (Block `heat.delta_kuehlzentren`), multiplikativ auf (RR − 1). **Formelzeile:**
  \(\Delta D_{\text{KZ}} = [D_{75\text{–}84} + D_{85+} \times (1 - h_{\text{Heim}})] \times (1 - \delta_{\text{KZ}})\),
  mit \(\delta_{\text{KZ}} = 1 - r_{\text{KZ}} \times w_{\text{KZ}}\) und
  \(w_{\text{KZ}} = (1 - g_{\text{S157}}) \times t_{\text{KZ}} = 0{,}71 \times 3/24 = 0{,}089\), also
  \(\delta_{\text{KZ}} = 1 - 0{,}05 \times 0{,}089 = 0{,}9956\) (**Abschätzung von KAP3**, Band 0,982–0,9994).
  **Herleitung:** Eine publizierte Effektgröße für Kühlzentren hat KAP3 nicht gefunden (Suche 27.09.2026); die Wirkung
  ist deshalb aus drei Stücken zusammengesetzt. (1) **Wirkung im gekühlten Raum** 0,71: In Heimen mit Klimaanlage fallen
  71 % des Hitze-Exzesses weg (\(1 - g_{\text{S157}}\), [46]); dort wirkt die Kühlung den ganzen Tag. (2) **Geschützter
  Anteil des Tages** \(t_{\text{KZ}}\) = 3/24: In der Laborstudie von Meade u. a. [73] ruhten 20 Menschen von 64 bis 79
  Jahren während einer neunstündigen simulierten Hitzewelle (Hitzeindex 37 °C) zwei Stunden in einem Raum mit rund
  23 °C. Am Ende der Kühlung lag ihre Körperkerntemperatur 0,8 °C (0,6–0,9) unter der Vergleichsgruppe, eine Stunde
  nach der Rückkehr in die Hitze noch 0,3 °C (0,2–0,4), in den Stunden 8 und 9 war sie gleich (Abstract, Teil Results).
  Die Kühlung schützt also für die Zeit des Aufenthalts und etwa eine Stunde danach: 2 h + 1 h = 3 h. Geteilt wird durch
  24 h, weil der Exzess des Modells am 24-h-Mittel hängt und Wohnungen nachts nicht auskühlen (§3.1). Band 2/24 (1 h
  Aufenthalt) bis 6/24 (5 h Aufenthalt). (3) **Reichweite** \(r_{\text{KZ}}\) = 5 % der Menschen ab 75 außerhalb der
  Heime (Band 1–10 %), Setzung von KAP3: ein Viertel der Reichweite eines Schutzprogramms (20 %), weil ein Kühlzentrum
  nur erreicht, wer in der Hitze das Haus verlässt. Gerade die am stärksten Gefährdeten tun das nicht: Bettlägerige
  haben ein 6,44-fach, Menschen, die nicht täglich aus dem Haus gehen, ein 3,35-fach erhöhtes Sterberisiko in
  Hitzewellen [41]. **Plausibilisierung:** Die Fall-Kontroll-Studien in [41] geben für den Besuch kühler Orte die Odds
  Ratio 0,34 (0,2–0,5), also 66 % weniger. Nach Log 10 überschätzen Fall-Kontroll-Odds-Ratios die Wirkung einer
  eingeführten Maßnahme 5- bis 10-fach: 0,66 / 10 bis 0,66 / 5 = 0,066–0,132; \(w_{\text{KZ}}\) = 0,089 liegt darin.
  **Berlin** (Beispiel-Block `kuehlzentren_berlin`, Kapitel 7): Die Bänder 75–84 und 85+ außerhalb der Heime tragen
  1.054 YLL, also 169,5 Mio. € (wie beim Hebel Schutzprogramme); × 0,05 × 0,089 = **0,75 Mio. € je Jahr** (Preisstand 2024; Band
  0,1–3,0 Mio. €), 0,2 % des Jahresbetrags 362,9 Mio. €. Im Zelllauf mit Gemeindeschlüssel 0,72 Mio. €, in Warmsen
  (Zelllauf) 320 € je Jahr. **Stärkster Treiber** ist die Reichweite: Über ihr Band 1–10 % wandert der Betrag von 0,15
  bis 1,50 Mio. €, über den geschützten Anteil des Tages 2/24–6/24 von 0,50 bis 1,50 Mio. €. **Was eine einfachere
  Rechnung verfälschen würde:** Den Faktor aus [46] ohne die Stunden anzusetzen (\(w_{\text{KZ}}\) = 0,71) hieße, ein
  Besuch im Kühlzentrum schütze wie eine Klimaanlage rund um die Uhr: 169,5 Mio. € × 0,05 × 0,71 = 6,0 Mio. €, achtmal
  so viel. **Zusammen mit Hitzeaktionsplan und Schutzprogrammen:** Die Faktoren werden auf den Bändern 75–84 und 85+
  (ohne Heim) multipliziert, und wie beim Hebel Schutzprogramme nehmen alle zusammen nie mehr weg als das gemessene
  Paket Deutschland [47]: \(\max(\delta_{\text{HAP}} \times \delta_{\text{VG}} \times \delta_{\text{KZ}};\ 0{,}794)\), mit der
  Kappung aus dem Block `heat.kappung_vg` (unten beim Hebel Schutzprogramme);
  zentral 0,95 × 0,931 × 0,9956 = 0,881, die Kappung greift nicht. Hatte die Kommune schon in den Kalibrierjahren
  Kühlzentren, gilt derselbe Doppelzählungs-Wächter wie bei \(\delta_{\text{VG}}\): eine eigene Frage ja oder nein für diese
  Maßnahme, Voreinstellung „nein“ aus demselben Grund, bei „ja“ \(\delta_{\text{KZ}}\) = 1 (Block
  `heat.vg_in_kalibrierjahren`). **Modellgrenze:** Jüngere
  Nutzer (etwa wohnungslose Menschen) und die Bänder unter 75 zählen nicht, das Ergebnis ist insoweit eine Untergrenze;
  die Wirkung ist aus Heimen und aus dem Labor übertragen. Wie \(\delta_{\text{VG}}\) wirkt der Hebel im abgedeckten Teil
  der Kommune. **Andockpunkt im Produkt:** dieselbe Maßnahme `COOLING_ROOMS_DRINKING_WATER` („Kühle Räume /
  Kühlzentren“); ihr Kostenmodell (je Raum, ein Raum je 20 ha nach dem Konzept „kühle Orte“) beschreibt öffentliche
  Kühlräume. Umsetzung beim CTO (eiserne Regel 5). **R7-Weiche:** wie bei S157, Kühl-Mehrkosten ab Stufe M5 bei #65.
- **Schutzprogramme vulnerable Gruppen (Knoten S152; Hitzetelefon, aufsuchende Betreuung,
  Besuchsdienste für Menschen ab 75 zu Hause):** Faktor \(\delta_{\text{VG}}\) auf den Wochenexzess der
  Bänder 75–84 und 85+ (Block `heat.delta_vg`, Befunde 123, 125–128), wie \(\delta_{\text{HAP}}\)
  multiplikativ auf (RR − 1). **Nicht** über \(v_{\text{vers},a}\): Das ist auf Ebene der Kommune genau 1
  (§3.0 Ebene 6), der Hebel wirkte dort nie. **Formelzeile:**
  \(\Delta D_{\text{VG}} = [D_{75\text{–}84} + D_{85+} \times (1 - h_{\text{Heim}})] \times (1 - \delta_{\text{VG}})\),
  mit \(\delta_{\text{VG}} = 1 - r_{\text{VG}} \times w_{\text{VG}} = 1 - 0{,}20 \times 0{,}34 = 0{,}931\)
  (**Abschätzung von KAP3**, Band 0,794–1,0). Heimbewohner ab 85 sind herausgenommen, weil für sie der
  Hebel S157 steht und ein Hausbesuchsprogramm sie nicht erreicht (Befund 125). Im Band 75–84 führt der
  Bericht keinen Heimanteil; das Band zählt ganz, der Fehler geht in Richtung einer etwas zu großen
  Wirkung (Modellgrenze). **Herleitung:** Eine publizierte Effektgröße nur für diesen Baustein gibt es
  nicht. (1) **Obergrenze.** Urban u. a. 2025 [47] messen die Wirkung der Hitzeschutzpläne als Ganzes:
  Ihre Auswertung nimmt nur an, ob ein Plan vorhanden ist (Abschnitt 2.2 und Stufe 2 der statistischen
  Auswertung); die Punktzahl über acht Kernelemente, darunter der Schutz vulnerabler Gruppen, beschreibt
  die Pläne, eine Wirkung je Baustein schätzen sie nicht. Der hitzebedingte Anteil der Sterbefälle sinkt um
  25,2 % (19,8–31,9 %; Zusammenfassung und Abb. 5), für Deutschland um 20,6 % (15,8–25,7 %; Tabelle 1,
  Westeuropa). Ein Baustein allein wirkt nicht stärker als das ganze Paket, also liegt
  \(\delta_{\text{VG}}\) nie unter 0,794 (Kappung). (2) **Wirkung bei Erreichten.** Liotta u. a. 2018 [70]
  vergleichen in Rom Stadtteile mit und ohne aufsuchendes Programm für Menschen ab 75. Verglichen werden
  alle Menschen ab 75 der Stadtteile (Tabelle 1: 6.483 mit, 5.724 ohne Programm), eingeschrieben waren
  4.720 (Abschnitt 3), also 72,8 %. Im Hitzesommer 2015 stieg die Sterberate gegenüber 2014 um 48,8 % mit
  gegen 97,3 % ohne Programm (Tabelle 2), roh also 48,5 Pp. weniger. Diesen rohen Vergleich bereinigen die Autoren
  selbst: Eine Regression über die 7 Stadtteile, nach Einwohnern gewichtet und bereinigt um die Sterberate vor dem
  Sommer und den Anteil ab 90 (Abschnitt 3), ergibt, dass das Programm den Anstieg um 24,4 Pp. senkt (Tabelle 3,
  Zeile „LLE program (no vs. yes)“: −24,372; die Tabelle setzt ein negatives Vorzeichen, Abschnitt 3 liest den Wert
  als geringeren Anstieg in den Stadtteilen mit Programm, und so ist er hier gelesen). Das ist halb so viel wie roh:
  Ein Teil des rohen Unterschieds ist Altersstruktur, denn ohne Programm sind 10,3 % der Einwohner 90 oder älter,
  mit Programm 9,0 % (Tabelle 1). **Wirkung bei Erreichten (Abschätzung von KAP3):** Auf die ganze Bevölkerung ab
  75 senkt das Programm den Anstieg um 24,4 / 97,3 = 0,25; auf die Erreichten umgerechnet ist
  \(w_{\text{VG}} = 24{,}4 / 97{,}3 / 0{,}728 = 0{,}34\). Die Senkung gilt schon für die ganze Bevölkerung ab 75; sie
  direkt mit der Reichweite zu multiplizieren, zöge die Reichweite zweimal ab (Befund 128). **Band 0–0,68.** Oben der
  rohe Unterschied ohne Bereinigung, 0,498 / 0,728 = 0,68: Er zählt die Altersstruktur als Wirkung mit und ist
  deshalb die obere Grenze. Das Intervall der Regression (19,7–29,0 Pp., also 0,28–0,41) trägt kein Band: Sein
  Standardfehler von 2,37 Pp. stammt aus 7 nach Einwohnern gewichteten Stadtteilen und ist zu eng für einen
  ökologischen Vergleich mit 336 Todesfällen im Sommer 2015, ohne Angaben zu Klimaanlagen und Urlaubsabwesenheit
  (Abschnitt 4, letzter Absatz, von [70]). **Untere Grenze aus Tabelle 2 (Befunde 132, 133):** Tabelle 2 von [70] führt den Anstieg
  der Sterberate (Zeile „Δ1: June–September 2015 vs. June–September 2014“) je Stadtteil. Ohne Programm: Centro
  Storico 37,38 %, Aventino 212,50 %, XX Settembre 162,59 %, Celio 130,30 %, im Mittel 97,3 % (Standardabweichung
  73,1 Pp.). Mit Programm: Trastevere 62,37 %, Testaccio 44,32 %, Esquilino 46,71 %, im Mittel 48,8 % (6,8 Pp.).
  Mittel und Standardabweichung sind nach Einwohnern gewichtet (Fußnote 1); die Zuordnung der Stadtteile steht auch
  in Tabelle 1. Centro Storico ohne Programm stieg also weniger als jeder Stadtteil mit Programm. Daraus:
  \(97{,}3 - 48{,}8 = 48{,}5\) Pp. Unterschied, Standardfehler \(\sqrt{73{,}1^2/4 + 6{,}8^2/3} = 36{,}8\),
  95-%-Intervall \(48{,}5 \pm 1{,}96 \times 36{,}8\) = −23,6 bis 120,6 Pp. Geteilt durch 97,3 ist die
  Wirkung auf die Bevölkerung ab 75 also 0,498 (−0,24 bis 1,24); das Verhältnis der Anstiege, 0,50, schließt die 1
  ein. Mit nur 3 und 4 Stadtteilen wäre das Intervall nach der t-Verteilung noch breiter. „Keine Wirkung“ liegt
  damit im Intervall, und die untere Grenze von \(w_{\text{VG}}\) ist 0 statt der früheren Setzung 0,30. Der
  Zentralwert 0,34 bleibt eine Abschätzung von KAP3 und ist nie null. Die „13 %“ aus Abschnitt 3 („25 deaths were
  averted“, 167 statt erwarteter 192 Todesfälle) beziehen sich auf alle Todesfälle des Sommers, nicht auf den
  Anstieg, und gehen deshalb nicht in \(w_{\text{VG}}\) ein. (3) **Reichweite** \(r_{\text{VG}}\) = 20 %
  der Menschen ab 75 (Band 5–40 %), Setzung von KAP3: Rom schreibt jeden Menschen ab 75 an und ruft ihn
  an (72,8 %); ein Hitzetelefon in Deutschland erreicht nur, wer sich anmeldet. **Berlin** (Beispiel-Block
  `schutzprogramme_berlin`, Kapitel 7): Das Band 75–84 trägt 635,4 YLL, das Band 85+ außerhalb der Heime
  638,8 × (1 − 0,344) = 419 YLL; zusammen 1.054 YLL, also 169,5 Mio. €. × (1 − 0,931) = **11,7 Mio. €
  je Jahr** weniger (Band 0–34,9 Mio. €), das sind 3,2 % (0–9,6 %) des Jahresbetrags 362,9 Mio. €.
  **Stärkster Treiber** ist die Wirkung bei Erreichten \(w_{\text{VG}}\), knapp vor der Reichweite: Über ihr Band
  0–0,68 wandert der Betrag von 0 bis 23,1 Mio. €, über die Reichweite 5–40 % von 2,9 bis 23,3 Mio. €. Erst wenn
  beide am oberen Ende liegen, greift die Kappung bei 34,9 Mio. €. **Morbidität (Befund 131, Block `heat.delta_vg_morb`):** Faktor \(\delta_{\text{VG,morb}}\) = 1,0
  (Band 0,931–1,069, **Abschätzung von KAP3**) auf die Einweisungen \(F_{75\text{–}84} + F_{85+} \times (1 - h_{\text{Heim}})\),
  gleiche Formelzeile wie oben mit \(F\) statt \(D\). Die Wirkung geht in beide Richtungen: Aufsuchende Betreuung
  verhindert Einweisungen, wie sie Todesfälle verhindert (untere Grenze 0,931 wie \(\delta_{\text{VG}}\)). Sie findet
  aber auch Menschen, die ohne Besuch zu Hause geblieben wären, und zieht deren Einweisung vor (obere Grenze
  \(1 + 0{,}20 \times 0{,}34 = 1{,}069\): so viele Einweisungen zusätzlich, wie Todesfälle wegfallen). Welche
  Richtung überwiegt, misst keine Quelle; der Zentralwert 1,0 setzt beide gleich. **Berlin:** 34,2 + 21,0 × 0,656
  = 48,0 Einweisungen ab 75 außerhalb der Heime × 7.152 € = 0,34 Mio. € je Jahr; über das Band ändert sich der
  Betrag um ± 0,02 Mio. € (± 0,007 % des Jahresbetrags). **Doppelzählungs-Wächter (Befund 150, Block
  `heat.vg_in_kalibrierjahren`):** Lief ein solches Programm in der Kommune schon in den Kalibrierjahren 2012–2024, ist es
  keine zusätzliche Maßnahme: Seine Wirkung gehört zum Anpassungsstand, den der Basiswert über \(c_{\text{kal}}\) abbildet
  (Kapitel 1 (a)), und es gilt \(\delta_{\text{VG}}\) = 1 (ebenso \(\delta_{\text{VG,morb}}\) = 1). Die Kommune beantwortet dazu
  eine Frage mit ja oder nein: „Lief das Programm schon in den Jahren 2012–2024?“ **Voreinstellung „nein“ (Abschätzung von
  KAP3).** Solche Programme waren in den Kalibrierjahren selten: Bundesweit gab es am 10.06.2024 18 veröffentlichte
  kommunale Hitzeaktionspläne; von den 53 Kreisen und kreisfreien Städten in Nordrhein-Westfalen hatten im Oktober 2023
  vier einen Hitzeaktionsplan, weit gefasst einschließlich gebündelter Maßnahmen zum Hitzeschutz, also 7,5 %; zehn
  erstellten einen, 25 planten ihn [76]. **Was die andere Voreinstellung bewirken würde:** Mit „ja“ zeigte jede Kommune
  ohne Antwort keine Wirkung der Schutzprogramme, Berlin 0 statt 11,7 Mio. € je Jahr; für die mehr als 90 % der Kommunen
  ohne ein älteres Programm wäre das eine Unterschätzung und eine Nullwirkung gegen P2. Mit „nein“ zählt eine Kommune,
  die das Programm schon hatte und die Frage nicht beantwortet, seine Wirkung doppelt, in Berlin wären das 11,7 Mio. € je
  Jahr. Auf Berliner Größe gerechnet ist der erwartete Fehler mit „nein“ kleiner: höchstens 7,5 % × 11,7 = 0,9 Mio. €
  gegen mindestens 92,5 % × 11,7 = 10,8 Mio. € mit „ja“. **Gegenargument:** Die Zahlen stammen vom Ende des
  Kalibrierfensters und aus einem Land und zählen Pläne, nicht einzelne Programme; wer schon vor 2020 ein Hitzetelefon
  ohne Hitzeaktionsplan betrieb, fehlt darin. Deshalb bleibt es eine Abschätzung von KAP3, die die Parameterliste so
  ausweist; wer ein älteres Programm hat, antwortet „ja“. Die Rechnung für Berlin nimmt die Voreinstellung; ob Berlin in den
  Kalibrierjahren ein solches Programm hatte, gibt Berlin selbst ein. Heimbewohner ab 85 zählen über S157 (siehe
  Formelzeile). **Zusammen mit dem Hitzeaktionsplan
  (Befund 126):** \(\delta_{\text{HAP}}\) stützt sich auf [45] und [47], und das Paket von [47] enthält
  den Schutz vulnerabler Gruppen. Ob \(\delta_{\text{HAP}}\) = 0,95 diesen Baustein schon enthält, lässt
  sich aus [45] nicht ausschließen. Wählt eine Kommune beide Hebel, gilt auf den Bändern 75–84 und 85+
  (ohne Heim) deshalb das Produkt beider Faktoren, höchstens aber bis zum Paketwert Deutschland:
  \(\max(\delta_{\text{HAP}} \times \delta_{\text{VG}};\ 0{,}794)\). Zentral ist das 0,95 × 0,931 = 0,885,
  die Kappung greift nicht; sie bleibt in der Formel, weil sie bei \(\delta_{\text{HAP}}\) = 0,85 greift (Produkt
  0,791, es gilt 0,794) und am oberen Ende des Bands von \(\delta_{\text{VG}}\).
  Zusammen können die beiden Hebel also nie mehr wegnehmen als das ganze gemessene Paket.
  **Kappung 0,794 (Block `heat.kappung_vg`, Befund 151).** Die Kappung begrenzt den Betrag und ist deshalb ein eigener
  Parameter (P1). **Herleitung:** Urban u. a. 2025 [47] messen für Deutschland, dass Hitzeschutzpläne den hitzebedingten
  Anteil der Sterbefälle um 20,6 % senken (15,8–25,7 %; Tabelle 1): 1 − 0,206 = 0,794, Band 1 − 0,257 = 0,743 bis
  1 − 0,158 = 0,842. Gekennzeichnet ist sie als **Abschätzung von KAP3**, nicht als Quellenwert: [47] misst das ganze
  Paket über alle Altersgruppen; dass derselbe Wert die Hebel auf den Bändern ab 75 ohne Heim begrenzt, setzt KAP3 (Log 40:
  der Wert steht für eine andere Größe). **Beziehung zu \(\delta_{\text{VG}}\):** 0,794 ist das untere Bandende von
  \(\delta_{\text{VG}}\), und zwar wegen der Kappung: Mit Reichweite und Wirkung am oberen Ende ihrer Bänder ergäbe sich
  1 − 0,40 × 0,68 = 0,728, die Kappung hebt das auf 0,794. **Wann sie greift (Befund 126, Runde 29):** allein bei Reichweite
  und Wirkung am oberen Ende; zusammen mit dem Hitzeaktionsplan schon bei \(\delta_{\text{HAP}}\) = 0,85 und dem Zentralwert
  (0,85 × 0,931 = 0,791, mit Kühlzentren 0,788); zentral (0,95 × 0,931 × 0,9956 = 0,881) greift sie nicht.
  **Sensitivität**, wo sie greift (Berlin, Reichweite und Wirkung am oberen Ende): 169,5 Mio. € × (1 − 0,794) = 34,9 Mio. €
  je Jahr, über das Band 0,743–0,842 von 26,8 bis 43,6 Mio. €. **Was eine Rechnung ohne Kappung verfälschen würde:**
  169,5 Mio. € × (1 − 0,728) = 46,1 Mio. €, also 11,2 Mio. € mehr, als das gemessene Paket für Deutschland hergibt
  (Beispiel-Block `sensitivitaeten_berlin`).
  Im Produkt steht die Maßnahme `VULNERABLE_GROUP_PROGRAMS` mit `default_reduction` 0.22
  auf Mortalität und Morbidität aller Bänder; die Abweichung führt Log 43 (Befund 45: die frühere Größe
  „v_access" existiert seit Rev. 3 nicht mehr).

**Sensitivitäten des Basiswerts im Vergleich zu den Hebeln (Befund 152; Beispiel-Block `sensitivitaeten_berlin`).** Die
Hebel oben verschieben den Jahresbetrag Berlin (Kette 362,9 Mio. €, Preisstand 2024) um 0,75 bis 11,7 Mio. €. Zwei
Parameter des Basiswerts, gemessen wie die Hebel an beiden Enden ihres Bands (Herleitung der Bänder in §3.3a und §3.5):

- **Sensitivität von f_alter** (Block `heat.f_alter`, \(f_a\)): Mit den Altersanteilen des Sommers 2025 (0,156 · 0,341 ·
  0,588 · 1,0) passt die Kalibrierung \(c_{\text{kal}}\) = 0,651 an, und der Betrag ist **310,2 Mio. €** je Jahr; mit denen
  des Sommers 2026 (0,562 · 0,753 · 0,659 · 1,0) ist \(c_{\text{kal}}\) = 0,534 und der Betrag **402,9 Mio. €**. Die Zahl
  der Hitzetoten bleibt dabei fast gleich (276,4 und 278,2 statt 277,4), weil die Kalibrierung sie an die RKI-Reihe
  bindet; es ändert sich, in welchem Alter sie sterben und wie viele Lebensjahre verloren gehen. Gemessen am 27.09.2026 mit
  `run_evaluation` aus `calibrate_heat_mortality_rev7.py` [50] (Fenster 2012–2024, \(s_{\text{Süd}}\) = 1,65), nur
  \(f_a\) ersetzt; mit \(f_a\) der Basis gibt derselbe Aufruf 0,581 zurück. 0,534 liegt unter dem Band von \(c_{\text{kal}}\)
  (0,55–0,67), weil dessen Band \(f_a\) nicht verändert. **Was eine einfachere Rechnung verfälschen würde:** \(f_a\) zu
  tauschen und \(c_{\text{kal}}\) = 0,581 stehen zu lassen, ergäbe 277,0 und 438,3 Mio. €, fast doppelt so weit, weil die
  Zahl der Hitzetoten dann nicht mehr zur RKI-Reihe passt.
- **Sensitivität von l_restlebenserwartung** (Block `heat.l_restlebenserwartung`, \(\bar L_a\)): am unteren Bandende
  (23,39 · 15,31 · 8,54 · 4,16 J) **357,3 Mio. €** je Jahr, am oberen (28,64 · 15,59 · 8,90 · 4,20 J) **381,1 Mio. €**.
  \(c_{\text{kal}}\) hängt nicht an \(\bar L_a\), weil die Kalibrierung Todesfälle anpasst, nicht Lebensjahre. Den größten
  Teil trägt das Band u65: 20,4 Todesfälle × 5,25 J = 107 YLL, also 17,2 Mio. €.

Beide Bänder sind breiter als jeder Hebel. Stärkster Treiber des Betrags bleibt die Temperatur (§3.0: −23 % und +27 %
bei 0,5 K weniger oder mehr); \(f_a\) verschiebt ihn um −15 % und +11 %, \(\bar L_a\) um −2 % und +5 %. Die Hebel wirken auf
denselben Basiswert und ändern sich mit ihm.

## 6 Szenario-Anwendung & Modellgrenzen (§3.2/§3.6)

**Szenario-Anwendung 95-A** (Befund 39): Verschoben wird ausschließlich
\(\bar T_{\text{Zelle}}\) (Zell-Sommermittel aus der Klimaprojektion des Szenariojahrs;
für HD analog das projizierte hot_days-Raster). Konstant gehalten: Anomalie-Quantile
\(q_w\), Schwellen \(T_0\), Steigungen \(\beta_a\), Bevölkerung und Modifikatoren.
**Stationaritätsannahmen (dokumentiert):** (1) \(q_w\)-Stationarität — Projektionen zeigen
zunehmende Hitzewellen-Variabilität, der reine Mittelwert-Shift ist daher eine Untergrenze;
(2) ERF-Stationarität — das Anpassungssignal (s. u.) wirkt gegenläufig. **M0 weist das
Ist-Klima aus**; Szenariofähigkeit folgt mit der Klimaprojektions-Anbindung (Stufe M1+).

**Jahresbeträge ohne Abzinsung.** Alle Euro-Beträge dieses Berichts sind Jahresbeträge ohne Abzinsung:
Sie gelten für ein Jahr im heutigen Klima (Preisstand 2024) und werden weder über mehrere Jahre summiert
noch auf einen Barwert abgezinst.

**Modellgrenzen (dokumentiert):**
1. Klimatologische Quantile bilden das **mittlere** Jahr ab — Jahre mit ausgeprägten
   Hitzewellen bei moderatem Sommermittel werden strukturell unterschätzt; genau das zeigen
   die Kalibrier-Residuen 2006 (−52 %) und 2015 (−42 %) — sie sind dieser Modellgrenze
   zuzuschreiben (Befund 40). Möglicher Ausbau: Kopplung der oberen Quantile an das
   Jahres-Sommermittel (Regression \(q_{12},q_{13}\) auf \(\bar T_J\) aus derselben
   Stationsklimatologie) als Sensitivität.
2. ERF-Zeittrend (Anpassungssignal): Expositions-Wirkung flacht über die Dekaden ab
   (+110 % → +43 % je Spitzenwoche 85+ [13]); nicht modelliert — Fensterwahl §4 mit ±15 %
   Wirkung, Sensitivität ausgewiesen.
3. Skalentransfer: ERF auf Regions-Gebietsmitteln geschätzt, auf Zelltemperaturen
   angewendet; \(c_{\text{kal}}\) fängt das Niveau, nicht die Form.
4. Kalibrier-Rest-Bias: UHI-Feinstruktur unterhalb der Gemeinde (Konvexität ×1,02, intra-kommunale Gewichtung) — kommunale Stichproben-Abgleiche als Fortschreibungsvermerk (§4; §3.4-Ressourcen-Regel: kein nationaler Vollraster-Lauf); Süd-ERF-Nachschätzung ist modellintern (Profil-Band 1,45–1,85).
5. UHI-Modellgüte als gemeinsamer Treiber der #95-Feinstruktur; HD ohne UHI-Verschiebung
   (Unterschätzung der Morbidität in UHI-Lagen, §3.4).

**Infokasten-/UI-Texte (§3.6 — Teil des Berichts):**

> **Infokasten 1 — am Gesamtwert:** „Dieser Wert ist der *bewertete Schaden im Konto K1
> Gesundheit* (Modellstand M0). Er umfasst Behandlungskosten und den Wert verlorener
> Lebensjahre — nicht enthalten sind u. a. Arbeitsproduktivität (folgt in Stufe M3), Sach-
> und Infrastrukturschäden sowie Vorsorgekosten (spätere Stufen). Der ausgewiesene Betrag
> ist deshalb eine bewusste **Untergrenze**; er wird mit jeder Ausbaustufe vollständiger —
> nie kleiner. Berechnet mit Modellstand M0, Stand ⟨Datum⟩."
>
> **Infokasten 2 — am Mortalitäts-Kostensatz:** „Sterblichkeit bewerten wir nach der
> UBA-Methodenkonvention 4.0: verlorene Lebensjahre × Wert eines Lebensjahres (160.800 €).
> Das bewertet altersgerecht — ein Sterbefall mit 6 verbleibenden Lebensjahren zählt anders
> als einer mit 40 — und fällt deutlich vorsichtiger aus als der pauschale ‚Wert eines
> statistischen Lebens' (Faktor ≈ 5 bei Hitze). Die Vergleichsrechnung mit dem Pauschalwert
> weisen wir als Sensitivität aus. Die 160.800 € gehen vom Wert der Methodenkonvention für den
> EU-Durchschnitt aus; die Übertragung auf deutsche Einkommen hat KAP3 selbst abgeschätzt, der Betrag
> ist deshalb eine Abschätzung von KAP3 (Spanne 136.400–165.600 €)."
>
> **Pflicht-Elemente:** Benennung „bewerteter Schaden — Konto K1" (nie „Gesamtschaden");
> Vollständigkeitsanzeige „Stufe M0: 1 von 8 Konten aktiv" mit Roadmap-Aufklappliste;
> Versionsstempel „berechnet mit Modellstand M0 — Untergrenze".

**Raten-Darstellung und Aggregation** (§3.6; Befund 65): Kartenausweis als **Raten**, nicht
als Zell-Rohwerte — nativ: **YLL je 1.000 EW und Jahr** (Teil-Ausweis zusätzlich: YLL je
1.000 EW 65+), Morbidität: Fälle je 1.000 EW und Jahr, €: € je EW und Jahr; dazu die
aggregierte Darstellungsebene **Quartier/Gemeindeteil** (bestehende Aggregat-Mechanik der
Plattform); Kommune = Summe der Zellen bleibt die Rechenebene.

## 7 Parameter-Blöcke (maschinenlesbar, §4)

**Kennzeichnung `berechnet` (Befunde 136 und 137).** `berechnet` heißt nur: Der Wert folgt aus anderen Blöcken dieses
Berichts. Das gilt für \(c_{\text{kal}}\) (Fit des Modells aus fünf Blöcken gegen die RKI-Reihe [50]) und für
\(\beta_{\text{pfl}}\) (Kette §3.3b aus \(m_{85+}\) und \(\bar q_{\text{pfl}}\)). \(\beta_{\text{iso}}\) ist die Odds Ratio
2,3 aus Semenza 1996 [40], nur umgerechnet mit dem amtlichen Anteil aus [63], und ist deshalb `quelle`. Im Produkt
lautet der Anzeigetext „berechnet aus anderen Parametern“, weil nicht alle Eingänge amtlich sind. Ein berechneter
Wert erbt die schwächste Kennzeichnung seiner Eingangsblöcke: \(c_{\text{kal}}\) stützt sich auf \(\beta_{85+}\)
(Süd-Nachschätzung) und \(f_a\), beide `abschaetzung_kap3`, und zählt damit wie eine Abschätzung; \(\beta_{\text{pfl}}\)
stützt sich auf \(m_{85+}\) und \(\bar q_{\text{pfl}}\), beide `quelle`, und zählt wie belegt. Ob diese Regel für alle
Klimawirkungen gilt, wird risikoübergreifend festgelegt; bis dahin zählt das Produkt `berechnet` wie „belegt“.

```yaml
parameter:
  id: heat.t0_region
  wert: {nord: 19.7, mitte: 20.2, sued: 20.8}
  einheit: "°C"
  band: null
  herkunft: register:95-E02-01
  quelle: winklmayr2022
  preisstand: null
  bandzuordnung: [u65, 65-74, 75-84, 85+]
  endpunkt: mortalitaet
  kennzeichnung: quelle   # Ablesewerte Winklmayr 2022, Abb. 3 [11]
  abgeleitet_aus: []
parameter:
  id: heat.beta_85plus_region
  wert: {nord: 0.0634, mitte: 0.0625, sued: 0.0876}
  einheit: "1/K"
  band: {sued: [0.0770, 0.0982]}   # Profil-Band s_Sued 1,45-1,85 (Bandregel +10 % Zielfunktion, Abschaetzung; §4 #beta-sued); Nord/Mitte Ablesekette
  herkunft: register:95-E02-01   # Sued zusaetzlich herleitung:#beta-sued (Rev.-7-Nachschaetzung)
  quelle: winklmayr2022_rev7_nachschaetzung
  preisstand: null
  bandzuordnung: [85+]
  endpunkt: mortalitaet
  kennzeichnung: abschaetzung_kap3   # Nord/Mitte Ablesewerte [11]; Sued KAP3-Nachschaetzung s_Sued 1,65 (§4 #beta-sued, Log 32)
  abgeleitet_aus: []
parameter:
  id: heat.f_alter
  wert: {u65: 0.357, 65-74: 0.588, 75-84: 0.631, 85+: 1.0}
  einheit: "-"
  band: {u65: [0.156, 0.562], 65-74: [0.341, 0.753], 75-84: [0.588, 0.659]}   # Abschaetzung von KAP3 (Befund 152): Rueckrechnung mit den Anteilen der Sommer 2025 [74] und 2026 [75]; 85+ = 1 per Definition. Sensitivitaet Berlin (Kette, c_kal neu gefittet 0,651 / 0,534) 310,2-402,9 Mio. EUR je Jahr (§5)
  herkunft: herleitung:#f-a
  quelle: rki_eb19_2025_destatis2023
  preisstand: null
  bandzuordnung: [u65, 65-74, 75-84, 85+]
  endpunkt: mortalitaet
  kennzeichnung: abschaetzung_kap3   # Rueckrechnung aus RKI-Anteilen [12] und Sterbefaellen [49] mit linearer Naeherung (§3.3a)
  abgeleitet_aus: []
parameter:
  id: heat.m_basissterberate
  wert: {u65: 213.2, 65-74: 1737.9, 75-84: 4812.3, 85+: 14800.2}
  einheit: "1/100000a"
  band: null
  herkunft: herleitung:#m-a
  quelle: destatis_sterbefaelle2023
  preisstand: null
  bandzuordnung: [u65, 65-74, 75-84, 85+]
  endpunkt: mortalitaet
  kennzeichnung: quelle   # Quotient amtlicher Summen: Sterbefaelle 2023 / Bevoelkerung 31.12.2023 [49]
  abgeleitet_aus: []
parameter:
  id: heat.l_restlebenserwartung
  wert: {u65: 23.39, 65-74: 15.59, 75-84: 8.90, 85+: 4.16}
  einheit: "Jahre"
  band: {u65: [23.39, 28.64], 65-74: [15.31, 15.59], 75-84: [8.54, 8.90], 85+: [4.16, 4.20]}   # Abschaetzung von KAP3 (Befund 152): Stuetzstelle bis sterbefallgewichteter Wert aus [49] Blatt 12613-02 und [48] (§3.5); 85+ Rev. 8 exakt, Obergrenze e(95)-Stuetzstelle statt e-quer(95+). Sensitivitaet Berlin (Kette) 357,3-381,1 Mio. EUR je Jahr (§5)
  herkunft: herleitung:#l-a
  quelle: destatis_sterbetafel2224
  preisstand: null
  bandzuordnung: [u65, 65-74, 75-84, 85+]
  endpunkt: mortalitaet
  kennzeichnung: abschaetzung_kap3   # Sterbetafel 2022/2024 [48]; u65/65-74/75-84 Stuetzstellen e(60)/e(70)/e(80) als Setzung von KAP3, 85+ exakt sterbefallgewichtet (§3.5 #l-a)
  abgeleitet_aus: []
parameter:
  id: heat.voly
  wert: 160800
  einheit: "EUR/Jahr"
  band: [136400, 165600]
  herkunft: herleitung:#voly
  quelle: uba_mk40_amann2020a
  preisstand: "2024"
  bandzuordnung: [u65, 65-74, 75-84, 85+]
  endpunkt: mortalitaet
  kennzeichnung: abschaetzung_kap3   # Ausgangswert 79.500 EUR2005 aus Amann 2020a Tab. 3.15; Elastizitaet 0,85 beim Raumtransfer Setzung von KAP3 (§3.5, Log 4)
  abgeleitet_aus: []
parameter:
  id: heat.c_fall
  wert: 7152
  einheit: "EUR/Fall"
  band: null   # Proxy (Durchschnitt aller KH-Faelle, §3.5); DRG-Saetze als Sensitivitaet
  herkunft: herleitung:#c-fall
  quelle: destatis_kostennachweis2023
  preisstand: "2024"
  bandzuordnung: [u65, 65-74, 75-84, 85+]
  endpunkt: morbiditaet
  kennzeichnung: abschaetzung_kap3   # Proxy von KAP3: Durchschnitt aller KH-Faelle aus Kostennachweis 2023 [17], mit VPI auf 2024 indexiert (§3.5, Log 17)
  abgeleitet_aus: []
parameter:
  id: heat.c_kal
  wert: 0.581   # Fit Fenster 2012-2024 auf bevoelkerungsgewichteten Reihen (Rev. 7, Log 31)
  einheit: "-"
  band: [0.55, 0.67]   # Herleitung §4 #c-kal, aussenrundend aus 0,559 (s_Sued=1,85) und 0,661 (ohne Sued); Voll-Holdout 0,567 im Band
  herkunft: herleitung:#c-kal
  quelle: rki_eb19_2025
  preisstand: null
  bandzuordnung: [u65, 65-74, 75-84, 85+]
  endpunkt: mortalitaet
  kennzeichnung: berechnet   # Kleinste-Quadrate-Fit des Modells gegen die RKI-Reihe 2012-2024 (§4 #c-kal)
  abgeleitet_aus: [heat.t0_region, heat.beta_85plus_region, heat.f_alter, heat.m_basissterberate, heat.q_wochenquantile]
  rolle: kalibrierung
parameter:
  id: heat.q_wochenquantile
  wert: "backend/data/kalibrierung/wochenquantile_region.csv"
  einheit: "K"
  band: null
  herkunft: herleitung:#q-w
  quelle: dwd_cdc_tageswerte
  preisstand: null
  bandzuordnung: [u65, 65-74, 75-84, 85+]
  endpunkt: mortalitaet   # Befund 73: speist nur den D-/Temperaturpfad
  kennzeichnung: quelle   # empirische Quantile aus DWD-CDC-Tageswerten ausgezaehlt (§3.2 #q-w, Log 5)
  abgeleitet_aus: []
parameter:
  id: heat.e_hd
  wert: 0.024
  einheit: "1/Tag"
  band: [0.024, 0.061]
  herkunft: register:95-E02-02
  quelle: karlsson_ziebarth2018
  preisstand: null
  bandzuordnung: [u65, 65-74, 75-84, 85+]
  endpunkt: morbiditaet
  kennzeichnung: quelle   # Karlsson & Ziebarth 2018 [18], IZA-DP 7875 Tab. 1 [62]
  abgeleitet_aus: []
parameter:
  id: heat.hd_ref
  wert: 7.2
  einheit: "Tage/Jahr"
  band: null
  herkunft: herleitung:#hd-ref
  quelle: karlsson_ziebarth2018
  preisstand: null
  bandzuordnung: [u65, 65-74, 75-84, 85+]
  endpunkt: morbiditaet
  kennzeichnung: quelle   # Panelbeschreibung Karlsson & Ziebarth 2018 [18]/[62] (§3.4 #hd-ref)
  abgeleitet_aus: []
parameter:
  id: heat.r0_einweisungsrate
  wert: {u65: 1.9, 65-74: 6.3, 75-84: 10.8, 85+: 15.6}
  einheit: "1/100000a"
  band: "x0.6-1.6"   # Altersprofil gekennzeichnete Abschaetzung (§3.4); GENESIS-Ersetzungspfad
  herkunft: herleitung:#r0-a
  quelle: destatis_t67_karlsson_ziebarth
  preisstand: null
  bandzuordnung: [u65, 65-74, 75-84, 85+]
  endpunkt: morbiditaet
  kennzeichnung: abschaetzung_kap3   # Altersprofil 1:3,3:5,7:8,2 gekennzeichnete Abschaetzung (§3.4 #r0-a, Log 16)
  abgeleitet_aus: []
parameter:
  id: heat.beta_iso
  wert: 0.90
  einheit: "-"
  band: [0.3, 1.4]
  herkunft: register:95-S152-02
  quelle: semenza1996_mikrozensus2023
  preisstand: null
  bandzuordnung: [65-74, 75-84, 85+]
  endpunkt: mortalitaet   # F-Pfad Default 1 (Log 28): keine Morbiditaetsevidenz
  kennzeichnung: quelle   # (OR-1)/[1+q(OR-1)] mit OR 2,3 aus Semenza 1996 [40] und q aus Mikrozensus 2023 [63]; Umrechnung ohne Setzung (§3.3, Log 40, Befund 136)
  abgeleitet_aus: [heat.qbar_1p]
parameter:
  id: heat.beta_pfl
  wert: 1.54
  einheit: "-"
  band: [1.0, 2.9]
  herkunft: register:95-S153-01
  quelle: fouillet2006_bouchama2007_klenk2010
  preisstand: null
  bandzuordnung: [85+]
  endpunkt: mortalitaet
  kennzeichnung: berechnet   # (OR-1)/[1+q(OR-1)], OR 3,0 aus der Kette §3.3b (Fouillet, WIdO [61]; Log 23)
  abgeleitet_aus: [heat.m_basissterberate, heat.qbar_pfl]
parameter:
  id: heat.beta_dist_sensitivitaet
  wert: 0.0
  einheit: "1/km"
  band: [0.0, 0.002]   # Sensitivitaetsband, Basiswert-Default 0 (Log 20)
  herkunft: register:95-R36-01
  quelle: nicholl2007
  preisstand: null
  bandzuordnung: [u65, 65-74, 75-84, 85+]
  endpunkt: mortalitaet
  kennzeichnung: abschaetzung_kap3   # Basiswert 0 = neutraler Default fuer unbelegte Modulatoren (§3.2, Log 20); Band nach Nicholl 2007
  abgeleitet_aus: []
  rolle: sensitivitaet
parameter:
  id: heat.qbar_1p
  wert: 0.346
  einheit: "-"
  band: null   # Mikrozensus 2023; Zensus-Gitterwert (bevoelkerungsgewichtet) ersetzt bei Integration
  herkunft: herleitung:#qbar-1p
  quelle: destatis_mikrozensus2023
  preisstand: null
  bandzuordnung: [65-74, 75-84, 85+]
  endpunkt: mortalitaet   # Befund 73: speist nur den D-/Temperaturpfad
  kennzeichnung: quelle   # Mikrozensus 2023 [63]
  abgeleitet_aus: []
parameter:
  id: heat.qbar_pfl
  wert: 0.149
  einheit: "-"
  band: null
  herkunft: herleitung:#qbar-pfl
  quelle: destatis_pflegestatistik2023
  preisstand: null
  bandzuordnung: [85+]
  endpunkt: mortalitaet
  kennzeichnung: quelle   # Quotient amtlicher Summen 424.300 / 2.844.213 [61]
  abgeleitet_aus: []
parameter:
  id: heat.delta_hap
  wert: 0.95
  einheit: "-"
  band: [0.85, 1.00]
  herkunft: register:95-S158-01
  quelle: feldbusch2025_erl2025
  preisstand: null
  bandzuordnung: [u65, 65-74, 75-84, 85+]
  endpunkt: mortalitaet
  kennzeichnung: abschaetzung_kap3   # zentral 0,95 zwischen DiD roh 1,00 und adjustiert 0,85 [45] (§5, Log 10)
  abgeleitet_aus: []
parameter:
  id: heat.gamma_hoehe
  wert: 0.0065
  einheit: "K/m"
  band: null
  herkunft: register:95-W124-01
  quelle: icao_standardatmosphaere
  preisstand: null
  bandzuordnung: [u65, 65-74, 75-84, 85+]
  endpunkt: mortalitaet   # Befund 73: speist nur den D-/Temperaturpfad
  kennzeichnung: quelle   # ICAO-Standardatmosphaere
  abgeleitet_aus: []
parameter:
  id: heat.ror_s157
  wert: 0.93
  einheit: "-"
  band: [0.87, 0.99]   # 95-%-KI aus [46]: rOR ohne/mit Klimaanlage 1,08 (1,01-1,15), umgekehrt 1/1,15 bis 1/1,01
  herkunft: register:95-S157-01
  quelle: katz2026
  preisstand: null
  bandzuordnung: [85+]
  endpunkt: mortalitaet
  kennzeichnung: quelle   # Kehrwert des rOR 1,08 aus Katz u. a. 2026 [46], keine Setzung (Log 40); Massnahme S157 (§5)
  abgeleitet_aus: []
parameter:
  id: heat.g_s157
  wert: 0.29
  einheit: "-"
  band: [0.0, 0.90]   # aus dem Band von heat.ror_s157: rOR 0,87 => 0 (Exzess ganz weg), rOR 0,99 => 0,90
  herkunft: register:95-S157-01
  quelle: katz2026
  preisstand: null
  bandzuordnung: [85+]
  endpunkt: mortalitaet
  kennzeichnung: abschaetzung_kap3   # (rOR x OR_ohne - 1)/(OR_ohne - 1) mit OR_ohne 1,11 [46]; Setzung: gilt in allen Hitzewochen (§5, Befund 124). Wirkt nur auf D_85+ x h_Heim x s_gek, mit heat.delta_hap zusammen auf D_85+ x delta_hap x h_Heim x s_gek (Befund 129); Andockpunkt Produkt COOLING_ROOMS_DRINKING_WATER
  abgeleitet_aus: [heat.ror_s157]
parameter:
  id: heat.delta_vg
  wert: 0.931
  einheit: "-"
  band: [0.794, 1.0]   # 1 - r x w mit r 0,05-0,40 und w 0-0,68 (unten aus [70] Tab. 2, Befund 132; oben roher Unterschied Tab. 2); Wirkung gekappt am Paketwert DE 0,794 [47] (Befund 128)
  herkunft: register:95-S152-03
  quelle: urban2025_liotta2018
  preisstand: null
  bandzuordnung: [75-84, 85+]
  endpunkt: mortalitaet   # Morbiditaet: eigener Block heat.delta_vg_morb (1,0, Band 0,931-1,069; §5, Befund 131)
  kennzeichnung: abschaetzung_kap3   # 1 - r_VG x w_VG = 1 - 0,20 x 0,34; w = 24,4 / 97,3 / 0,728 aus Liotta 2018 [70] Tab. 1-3 (um Vorsterblichkeit und Anteil ab 90 bereinigt, Befund 134), Obergrenze Paket Urban 2025 [47] Tab. 1 (DE 0,794); r Setzung von KAP3 (§5, Log 43). Faktor auf den Wochenexzess 75-84 und 85+ ohne Heimbewohner (D_85+ x (1 - h_Heim)), nicht v_vers,a; mit heat.delta_hap zusammen max(delta_hap x delta_vg; 0,794)
  abgeleitet_aus: []
parameter:
  id: heat.delta_vg_morb
  wert: 1.0
  einheit: "-"
  band: [0.931, 1.069]   # unten wie heat.delta_vg (Einweisungen verhindert), oben 1 + 0,20 x 0,34 (Einweisungen vorgezogen); Befunde 131, 134
  herkunft: register:95-S152-03
  quelle: urban2025_liotta2018
  preisstand: null
  bandzuordnung: [75-84, 85+]
  endpunkt: morbiditaet
  kennzeichnung: abschaetzung_kap3   # Richtung der Wirkung auf Einweisungen nicht gemessen; Zentralwert 1,0 setzt Verhindern und Vorziehen gleich (§5). Faktor auf F_75-84 + F_85+ x (1 - h_Heim); Berlin +-0,02 Mio. EUR je Jahr
  abgeleitet_aus: [heat.delta_vg]
parameter:
  id: heat.anteil_60_66
  wert: 0.2857   # 2/7: Jahrgaenge 65 und 66 von sieben Jahrgaengen 60-66 (Befund 141)
  einheit: "-"
  band: [0.0, 1.0]   # Gruppe 60-66 gar nicht (0/7) oder ganz (7/7); Faktor Berlin x 0,927-1,000, Warmsen x 0,651-0,947 (§3.3)
  herkunft: herleitung:#ersatz-65
  quelle: zensus2022_demografie
  preisstand: null
  bandzuordnung: [65-74, 75-84, 85+]
  endpunkt: mortalitaet
  kennzeichnung: abschaetzung_kap3   # gleich viele Menschen je Jahrgang angenommen; [69] trennt bei 67, nicht bei 65 (§3.3 Stufe 2, Log 41)
  abgeleitet_aus: []
parameter:
  id: heat.s_gek
  wert: 0.11   # Voreinstellung (Befund 138): 11 % der Pflegeheime mit Klimaanlage [71] x 1; Eingabe der Kommune ersetzt sie
  einheit: "-"
  band: [0.05, 0.15]   # unten die Haelfte (Teilkuehlung, Umfrage nicht repraesentativ [71]); oben 14,5 % der Neubauten des Sozialwesens 2025 [72], aussen gerundet
  herkunft: register:95-S157-01
  quelle: carevor9_2026_destatis2026
  preisstand: null
  bandzuordnung: [85+]
  endpunkt: mortalitaet
  kennzeichnung: abschaetzung_kap3   # Setzungen von KAP3: Heime mit und ohne Klimaanlage gleich gross, alle Plaetze eines Heims mit Klimaanlage gekuehlt; gilt fuer die ganze Kommune, unabhaengig von der gezeichneten Flaeche (Modellgrenze, §5, Log 45). Sensitivitaet Berlin (Kette) S157 2,7 Mio. EUR je Jahr, Band 1,2-3,7 Mio. EUR
  abgeleitet_aus: []
parameter:
  id: heat.h_heim
  wert: 0.344   # q_pfl x [1 + beta_pfl x (1 - q_pfl)] = 0,149 x 2,31 (Kommune); je Zelle q_pfl,z x [1 + beta_pfl (1 - q-quer)] / [1 + beta_pfl (q_pfl,z - q-quer)], 0,344 Rueckfallwert (Befund 146)
  einheit: "-"
  band: [0.275, 0.517]   # aus dem Band von heat.beta_pfl 1,0-2,9: 0,2758 und 0,5167, aussen gerundet
  herkunft: register:95-S153-01
  quelle: destatis_pflegestatistik2023_fouillet2006
  preisstand: null
  bandzuordnung: [85+]
  endpunkt: mortalitaet
  kennzeichnung: berechnet   # folgt aus heat.qbar_pfl (Pflegestatistik 2023 [61]) und heat.beta_pfl (Kette §3.3b [60,61]); wirkt in S157, Schutzprogrammen und Kuehlzentren (§5)
  abgeleitet_aus: [heat.qbar_pfl, heat.beta_pfl]
parameter:
  id: heat.delta_kuehlzentren
  wert: 0.9956   # 1 - r_KZ x w_KZ = 1 - 0,05 x 0,71 x 3/24 (Befunde 139, 148)
  einheit: "-"
  band: [0.982, 0.9994]   # r_KZ 0,01-0,10 und t_KZ 2/24-6/24: 1 - 0,10 x 0,71 x 6/24 = 0,98225 bis 1 - 0,01 x 0,71 x 2/24 = 0,99941
  herkunft: register:95-S157-02
  quelle: katz2026_meade2023_bouchama2007
  preisstand: null
  bandzuordnung: [75-84, 85+]
  endpunkt: mortalitaet
  kennzeichnung: abschaetzung_kap3   # w_KZ = (1 - g_S157) x t_KZ: 71 % Wirkung im gekuehlten Raum [46] fuer 2 h Aufenthalt + 1 h Nachwirkung [73] von 24 h; r_KZ Setzung von KAP3 (ein Viertel von r_VG); plausibilisiert an [41] (OR 0,34 kuehle Orte, 5- bis 10-fach ueberschaetzt, Log 10). Faktor auf D_75-84 + D_85+ x (1 - h_Heim); mit heat.delta_hap und heat.delta_vg zusammen max(Produkt; 0,794). Berlin 0,75 Mio. EUR je Jahr, Band 0,1-3,0 Mio. EUR (§5, Log 46)
  abgeleitet_aus: [heat.g_s157]
parameter:
  id: heat.kappung_vg
  wert: 0.794   # 1 - 0,206: Hitzeschutzplaene senken den hitzebedingten Anteil der Sterbefaelle in Deutschland um 20,6 % (Urban 2025 [47], Tabelle 1) (Befund 151)
  einheit: "-"
  band: [0.743, 0.842]   # aus dem Intervall 15,8-25,7 % derselben Zeile: 1 - 0,257 bis 1 - 0,158
  herkunft: register:95-S152-03
  quelle: urban2025
  preisstand: null
  bandzuordnung: [75-84, 85+]
  endpunkt: mortalitaet
  kennzeichnung: abschaetzung_kap3   # Setzung von KAP3 (Log 40, Log 48): der Paketwert fuer alle Altersgruppen begrenzt die Hebel auf D_75-84 + D_85+ x (1 - h_Heim): max(delta_hap x delta_vg x delta_kz; 0,794). Zugleich unteres Bandende von heat.delta_vg (ohne Kappung 1 - 0,40 x 0,68 = 0,728). Greift bei delta_hap 0,85 (0,791) und bei r, w am oberen Ende. Sensitivitaet Berlin dort 34,9 Mio. EUR, Band 26,8-43,6 Mio. EUR, ohne Kappung 46,1 Mio. EUR (§5)
  abgeleitet_aus: []
parameter:
  id: heat.vg_in_kalibrierjahren
  wert: 0   # Voreinstellung "nein" (Befund 150): Programm lief nicht schon 2012-2024; Eingabe der Kommune ja (1) / nein (0) ersetzt sie
  einheit: "-"
  band: [0, 1]   # nein oder ja; bei ja gilt delta_vg = delta_vg_morb = 1 (Schutzprogramme) bzw. delta_kz = 1 (Kuehlzentren), je Massnahme eine eigene Frage
  herkunft: register:95-S152-03
  quelle: lzg_nrw2024
  preisstand: null
  bandzuordnung: [75-84, 85+]
  endpunkt: mortalitaet
  kennzeichnung: abschaetzung_kap3   # 18 veroeffentlichte kommunale Hitzeaktionsplaene bundesweit am 10.06.2024, 4 von 53 Kreisen und kreisfreien Staedten in NRW im Oktober 2023 [76]; erwarteter Fehler Berlin-Groesse mit nein hoechstens 0,9 Mio. EUR, mit ja mindestens 10,8 Mio. EUR (§5, Log 47)
  abgeleitet_aus: []
```

```python test: s157_berlin
# Hebel S157 (gekuehlte Raeume in Heimen), Berlin, Werte aus Kette 3.0 und Kapitel 7 (Befunde 122, 124)
ror, or_ohne = 0.93, 1.11                     # [46]: rOR umgekehrt; OR ohne Klimaanlage
assert abs(1 / 1.08 - ror) < 0.005 and abs(1 / 1.15 - 0.87) < 0.001 and abs(1 / 1.01 - 0.99) < 0.001
g = lambda r: max(0.0, (r * or_ohne - 1) / (or_ohne - 1))
assert abs(g(ror) - 0.29) < 0.005 and g(0.87) == 0.0 and abs(g(0.99) - 0.90) < 0.005
d85, L85, voly = 153.6, 4.16, 160_800          # Ebene 6, Ebene 7, VOLY
h_heim = 0.149 * (1 + 1.54 * (1 - 0.149))      # Anteil Heimbewohner an Todesfaellen 85+
assert abs(h_heim - 0.344) < 0.001
s_gek = 1.0                                   # alle Heimplaetze gekuehlt
delta_d = d85 * h_heim * s_gek * (1 - g(ror))
assert abs(d85 * h_heim - 52.9) < 0.05 and abs(delta_d - 37.4) < 0.05
eur = delta_d * L85 * voly / 1e6
assert abs(delta_d * L85 - 155) < 1 and abs(eur - 25.0) < 0.05
assert abs(d85 * h_heim * (1 - g(0.99)) * L85 * voly / 1e6 - 3.6) < 0.05   # Band unten
assert abs(d85 * h_heim * (1 - g(0.87)) * L85 * voly / 1e6 - 35.4) < 0.05  # Band oben
naiv = d85 * h_heim * (1 - ror) * L85 * voly / 1e6                         # 0,93 direkt auf den Exzess
assert abs(naiv - 2.5) < 0.05 and 9 < eur / naiv < 11
# Befund 132: OR_ohne ueber sein KI 1,06-1,16 [46], g bleibt im Band 0-0,90
go = lambda o: max(0.0, (ror * o - 1) / (o - 1))
assert go(1.06) == 0.0 and abs(go(1.16) - 0.49) < 0.005 and go(1.16) < 0.90
# beide KI aus [46] zugleich, log-normal und unabhaengig: g = (OR_mit - 1)/(OR_ohne - 1), 97,5-%-Punkt 0,833
import math
Phi = lambda z: 0.5 * (1 + math.erf(z / 2 ** 0.5))
lm, sm = math.log(1.03), math.log(1.07 / 0.98) / 3.92   # OR mit Klimaanlage 1,03 (0,98-1,07)
lo, so = math.log(1.11), math.log(1.16 / 1.06) / 3.92   # OR ohne Klimaanlage 1,11 (1,06-1,16)
def p_unter(x, n=2000):                        # Anteil der Werte von g bis x, ueber OR_ohne integriert
    schritt = 16 / n
    return sum(math.exp(-z * z / 2) / (2 * math.pi) ** 0.5 * schritt
               * Phi((math.log(1 + x * (math.exp(lo + so * z) - 1)) - lm) / sm)
               for z in (-8 + schritt * (i + 0.5) for i in range(n)))
assert p_unter(0.0) > 0.025 and p_unter(0.83) < 0.975 < p_unter(0.835)   # 95 % zwischen 0 und 0,83
# zusammen mit dem Hitzeaktionsplan (Befund 129): S157 wirkt auf den schon mit delta_hap gedaempften Heim-Exzess
d_heim = d85 * h_heim                                        # 52,9 Todesfaelle von Heimbewohnern
for delta_hap, zu_viel in ((0.95, 1.25), (0.85, 3.75)):
    s157_mit_hap = d85 * delta_hap * h_heim * s_gek * (1 - g(ror))
    gesamt = d_heim * (1 - delta_hap) + s157_mit_hap         # multiplikativ: 1 - delta_hap x g
    assert abs(gesamt - d_heim * (1 - delta_hap * g(ror))) < 1e-9
    additiv = d_heim * ((1 - delta_hap) + (1 - g(ror)))
    assert abs((additiv - gesamt) * L85 * voly / 1e6 - zu_viel) < 0.05
s157_mit_hap = d85 * 0.95 * h_heim * s_gek * (1 - g(ror))
assert abs(1 - 0.95 * g(ror) - 0.721) < 0.001 and abs(d_heim * (1 - 0.95 * g(ror)) - 38.1) < 0.05
assert abs(s157_mit_hap - 35.5) < 0.05 and abs(s157_mit_hap * L85 * voly / 1e6 - 23.7) < 0.05
```

```python test: schutzprogramme_berlin
# Hebel Schutzprogramme vulnerable Gruppen, Berlin (Befund 123); Kette 3.0 bleibt 362,9 Mio. EUR
# Nacharbeit (Befunde 125, 126, 128): 85+ ohne Heimbewohner, w auf die Erreichten umgerechnet, Kappung am Paketwert
paket_de = 1 - 0.206                          # [47] Tabelle 1, Deutschland -20,6 %
dvg = lambda r, w: max(1 - r * w, paket_de)   # Baustein wirkt nie staerker als das Paket
anstieg_mit, anstieg_ohne = 0.488, 0.973      # [70] Tabelle 2: Anstieg Sterberate 2015 gegen 2014
einschreibung = 4720 / 6483                   # [70] Abschnitt 3 und Tabelle 1
assert abs(einschreibung - 0.728) < 0.001
w_bev = 1 - anstieg_mit / anstieg_ohne        # roher Unterschied, Wirkung auf die ganze Bevoelkerung ab 75
w_roh = w_bev / einschreibung                 # obere Grenze von w (Band 0-0,68)
assert abs(w_bev - 0.498) < 0.001 and abs(w_roh - 0.68) < 0.005
# Befund 134: bereinigt [70] Tab. 3, Zeile "LLE program (no vs. yes)": -24,372 Pp. (95-%-KI -29,029 bis -19,714)
w_ber = [x / 97.3 / einschreibung for x in (24.372, 19.714, 29.029)]
assert [round(x, 2) for x in w_ber] == [0.34, 0.28, 0.41] and w_ber[2] < 0.68
w, r = w_ber[0], 0.20                         # Zentralwert w 0,34 (Abschaetzung von KAP3)
delta_vg = dvg(r, w)
assert abs(delta_vg - 0.931) < 0.0005
assert dvg(0.40, 0.68) == paket_de and dvg(0.05, 0.0) == 1.0   # Band 0,794-1,0 (Befund 132)
# Befund 132: Intervall aus [70] Tabelle 2 (Standardabweichung zwischen 4 und 3 Stadtteilen)
diff, se = 97.3 - 48.8, (73.1 ** 2 / 4 + 6.8 ** 2 / 3) ** 0.5
assert abs(se - 36.8) < 0.05 and abs(diff - 1.96 * se + 23.6) < 0.1 and abs(diff + 1.96 * se - 120.6) < 0.1
assert diff - 1.96 * se < 0                   # keine Wirkung liegt im Intervall => w unten 0
d1_ohne, d1_mit = (37.38, 212.50, 162.59, 130.30), (62.37, 44.32, 46.71)   # [70] Tab. 2, Zeile Delta1 je Stadtteil
assert min(d1_ohne) < min(d1_mit)             # Centro Storico ohne Programm unter jedem Stadtteil mit Programm
assert abs((diff - 1.96 * se) / 97.3 + 0.24) < 0.005 and abs((diff + 1.96 * se) / 97.3 - 1.24) < 0.005
h_heim = 0.149 * (1 + 1.54 * (1 - 0.149))      # wie s157_berlin
yll = 635.4 + 638.8 * (1 - h_heim)             # 75-84 ganz, 85+ ohne Heimbewohner
eur_7585 = yll * 160_800 / 1e6                 # x VOLY
assert abs(yll - 1054) < 1 and abs(eur_7585 - 169.5) < 0.05
for d, soll in ((delta_vg, 11.7), (paket_de, 34.9), (1.0, 0.0)):
    assert abs(eur_7585 * (1 - d) - soll) < 0.05
assert abs(eur_7585 * (1 - delta_vg) / 362.9 - 0.032) < 0.001
assert abs(eur_7585 * (1 - paket_de) / 362.9 - 0.096) < 0.001
# staerkster Treiber: w ueber sein Band 0-0,68, knapp vor der Reichweite 5-40 % (Kappung dort nicht erreicht)
assert abs(eur_7585 * (1 - dvg(r, 0.68)) - 23.1) < 0.05 and dvg(r, 0.0) == 1.0
assert abs(eur_7585 * (1 - dvg(0.05, w)) - 2.9) < 0.05 and abs(eur_7585 * (1 - dvg(0.40, w)) - 23.3) < 0.05
assert 1 - 0.40 * w > paket_de
assert (23.1 - 0.0) > (23.3 - 2.9)
# Log 43: Katalogwert 0.22 auf alle Baender ergaebe rund 79,8 Mio. EUR; der Hebel ergibt rund 15 % davon
assert abs(eur_7585 * (1 - delta_vg) / 79.8 - 0.15) < 0.005
# verworfene Variante (Log 43): roher Unterschied als Zentralwert ergaebe 23,1 Mio. EUR, doppelt so viel
assert abs(w_roh - 0.68) < 0.005 and abs(eur_7585 * (1 - dvg(r, 0.68)) - 23.1) < 0.05   # mit dem Bandwert 0,68
f_75 = 34.2 + 21.0 * (1 - h_heim)             # Einweisungen ab 75 ausserhalb der Heime (Ebene 9)
assert abs(f_75 - 48.0) < 0.05 and abs(f_75 * 7152 / 1e6 - 0.34) < 0.005
morb_band = (delta_vg, 1 + r * w)             # heat.delta_vg_morb, Befunde 131, 134
assert abs(morb_band[0] - 0.931) < 0.0005 and abs(morb_band[1] - 1.069) < 0.0005
for m in morb_band:
    assert abs(abs(f_75 * 7152 * (1 - m) / 1e6) - 0.02) < 0.005   # +-0,02 Mio. EUR
alt = (635.4 + 638.8 * 1.0) * 160_800 / 1e6 * (1 - delta_vg)             # mit Heimbewohnern: doppelt zu S157
assert alt - eur_7585 * (1 - delta_vg) > 2
# gleichzeitige Wahl mit dem Hitzeaktionsplan (Befund 126)
for delta_hap, soll in ((0.95, 0.885), (0.85, 0.794)):
    assert abs(max(delta_hap * delta_vg, 0.794) - soll) < 0.001
assert 0.85 * delta_vg < 0.794                # bei delta_hap 0,85 greift die Kappung (0,791)
```

```python test: s157_voreinstellung
# Voreinstellung s_gek (Befund 138), h_Heim je Zelle (Befund 146), S157 im Anpassungspotenzial (Befund 149)
g = (0.93 * 1.11 - 1) / 0.11                  # wie s157_berlin, 1 - g = 0,706
qbar, beta, L85, voly = 0.149, 1.54, 4.16, 160_800
h = qbar * (1 + beta * (1 - qbar))            # heat.h_heim, Kommune
assert abs(h - 0.344) < 0.001
assert abs(qbar * (1 + 1.0 * (1 - qbar)) - 0.2758) < 0.0001 and abs(qbar * (1 + 2.9 * (1 - qbar)) - 0.5167) < 0.0001
h_zelle = lambda q: q * (1 + beta * (1 - qbar)) / (1 + beta * (q - qbar))   # je Zelle mit q_pfl,z
assert abs(h_zelle(qbar) - h) < 1e-12 and h_zelle(0.0) == 0.0 and abs(h_zelle(1.0) - 1.0) < 1e-12
assert abs(h_zelle(0.5) - 0.75) < 0.001 and abs(0.5 * 2.31 - 1.155) < 1e-9 and abs(1 + 1.54 * 0.351 - 1.541) < 0.001
# Summe der Heim-Todesfaelle je Zelle = h x Summe D_85+, wenn der Exzess je Person gleich ist (erwartungstreue Ebene)
pop85, qz = [100, 300, 50], [0.0, 0.149, 0.5]
qz[1] = (qbar * sum(pop85) - qz[2] * pop85[2]) / pop85[1]   # Mittel der Zellen = q-quer
d85z = [p * (1 + beta * (q - qbar)) for p, q in zip(pop85, qz)]
assert abs(sum(d * h_zelle(q) for d, q in zip(d85z, qz)) - h * sum(d85z)) < 1e-9
s_gek = 0.11                                  # heat.s_gek: 11 % der Heime mit Klimaanlage [71] x 1
assert 0.145 < 0.15 < 0.145 + 0.01           # Band oben: 14,5 % der Neubauten des Sozialwesens [72], aussen gerundet
s157 = lambda d85, s: d85 * h * s * (1 - g) * L85 * voly
assert abs(s157(153.6, 1.0) / 1e6 - 25.0) < 0.05                                 # alle Heime gekuehlt
assert abs(s157(153.6, s_gek) / 1e6 - 2.7) < 0.05                                # Voreinstellung, Kette
assert abs(s157(153.6, 0.05) / 1e6 - 1.2) < 0.05 and abs(s157(153.6, 0.15) / 1e6 - 3.7) < 0.05
assert abs(s157(153.6, 0.05) / 1e6 / 362.9 - 0.0034) < 0.0001 and abs(s157(153.6, 0.15) / 1e6 / 362.9 - 0.0103) < 0.0001
yll85_berlin, yll85_warmsen = 556.27, 0.2398   # Zelllauf mit Gemeindeschluessel, anlagen/95_zellvergleich.py --ersatz
zell = lambda y85, s: y85 * h * s * (1 - g) * voly
assert abs(zell(yll85_berlin, s_gek) / 1e6 - 2.4) < 0.05
assert abs(zell(yll85_warmsen, s_gek) - 1032) < 1
assert abs(zell(yll85_warmsen, 0.05) - 469) < 1 and abs(zell(yll85_warmsen, 0.15) - 1407) < 1
# Anpassungspotenzial: r_S157 = a_85+ x h x s_gek x (1 - g); mit Hitzeaktionsplan 1 - 0,95 x (1 - r)
a85 = 638.8 / 2250                            # Anteil 85+ an den YLL der Kette (Ebene 7)
r = a85 * h * s_gek * (1 - g)
assert abs(a85 - 0.284) < 0.0005 and abs(r - 0.0076) < 0.00005
assert abs(0.284 * 0.344 * 0.11 * 0.706 - 0.0076) < 0.00005
assert abs(1 - 0.95 * (1 - r) - 0.057) < 0.0005 and abs(1 - 0.95 - 0.050) < 1e-9
a85_w = yll85_warmsen / 1.0713               # Warmsen, Zelllauf (YLL gesamt 1,0713)
r_w = a85_w * h * s_gek * (1 - g)
assert abs(a85_w - 0.224) < 0.0005 and abs(r_w - 0.0060) < 0.00005 and abs(1 - 0.95 * (1 - r_w) - 0.056) < 0.0005
assert 1 - 0.95 * (1 - r) < 0.1               # Gruppe nach KWRA unveraendert (unter 0,1)
```

```python test: kuehlzentren_berlin
# Hebel oeffentliche Kuehlzentren (Befunde 139, 148): delta_KZ = 1 - r_KZ x w_KZ, w_KZ = (1 - g_S157) x t_KZ
w = 0.71 * 3 / 24                             # 71 % Wirkung im gekuehlten Raum [46], 2 h + 1 h von 24 h [73]
r = 0.05                                      # Reichweite, Setzung von KAP3 (ein Viertel von r_VG 0,20)
assert abs(w - 0.089) < 0.0005 and abs(r - 0.20 / 4) < 1e-12
delta_kz = 1 - r * w
assert abs(delta_kz - 0.9956) < 0.00005
assert abs(1 - 0.10 * 0.71 * 6 / 24 - 0.98225) < 1e-9 and abs(1 - 0.01 * 0.71 * 2 / 24 - 0.9994) < 0.00005
assert 0.066 <= w <= 0.132 and abs(0.66 / 10 - 0.066) < 1e-9   # Plausibilisierung an [41]: OR 0,34, 5- bis 10-fach
h = 0.149 * (1 + 1.54 * (1 - 0.149))          # wie s157_berlin
eur_7585 = (635.4 + 638.8 * (1 - h)) * 160_800 / 1e6   # 75-84 ganz, 85+ ohne Heimbewohner (wie schutzprogramme_berlin)
assert abs(eur_7585 - 169.5) < 0.05 and abs(635.4 + 638.8 * (1 - h) - 1054) < 1
kz = eur_7585 * (1 - delta_kz)
assert abs(kz - 0.75) < 0.005 and abs(kz / 362.9 - 0.002) < 0.0005
assert abs(eur_7585 * 0.01 * 0.71 * 2 / 24 - 0.1) < 0.005 and abs(eur_7585 * 0.10 * 0.71 * 6 / 24 - 3.0) < 0.05
# staerkster Treiber: Reichweite 1-10 % (0,15-1,50 Mio. EUR) vor Stunden 2/24-6/24 (0,50-1,50 Mio. EUR)
r_lo, r_hi = eur_7585 * 0.01 * w, eur_7585 * 0.10 * w
t_lo, t_hi = eur_7585 * r * 0.71 * 2 / 24, eur_7585 * r * 0.71 * 6 / 24
assert abs(r_lo - 0.15) < 0.005 and abs(r_hi - 1.50) < 0.005 and abs(t_lo - 0.50) < 0.005 and abs(t_hi - 1.50) < 0.005
assert r_hi - r_lo > t_hi - t_lo
# einfachere Rechnung: 0,71 ohne Stunden
naiv = eur_7585 * r * 0.71
assert abs(naiv - 6.0) < 0.05 and 7.5 < naiv / kz < 8.5
# Zelllauf mit Gemeindeschluessel (anlagen/95_zellvergleich.py --ersatz): YLL 75-84 und 85+
for y7584, y85, soll, tol in ((637.67, 556.27, 0.72e6, 0.005e6), (0.2905, 0.2398, 320, 1)):
    assert abs((y7584 + y85 * (1 - h)) * 160_800 * r * w - soll) < tol
# zusammen mit Hitzeaktionsplan und Schutzprogrammen: max(delta_hap x delta_vg x delta_kz; 0,794)
assert abs(max(0.95 * 0.931 * delta_kz, 0.794) - 0.881) < 0.0005 and 0.95 * 0.931 * delta_kz > 0.794
```

```python test: sensitivitaeten_berlin
# Befunde 150-152: Waechter-Voreinstellung, Kappung 0,794, Baender und Sensitivitaeten von f_a und L_a (Kette 3.0)
import math
q = [-4.59, -3.04, -2.27, -1.64, -1.12, -0.57, -0.04, 0.51, 1.05, 1.65, 2.32, 3.16, 4.60]
pop, m = [2_961_430, 339_490, 253_528, 107_933], [213.2, 1737.9, 4812.3, 14800.2]
L0, fa0, voly = [23.39, 15.59, 8.90, 4.16], [0.357, 0.588, 0.631, 1.0], 160_800
morb = sum(p * r / 100_000 for p, r in zip(pop, [1.9, 6.3, 10.8, 15.6])) * (1 + 0.024 * (17.5 - 7.2)) * 7152 / 1e6
exz = lambda b: sum(math.exp(b * max(0.0, 20.07 + x - 20.2)) - 1 for x in q)
tote = lambda c, fa: [c * p * mm / 100_000 / 52 * exz(0.0625 * f) for p, mm, f in zip(pop, m, fa)]
betrag = lambda c, fa, L=L0: sum(d * l for d, l in zip(tote(c, fa), L)) * voly / 1e6 + morb
basis = betrag(0.581, fa0)
assert abs(basis - 362.9) < 0.05
# Band von f_a: Rueckrechnung wie §3.3a mit den Anteilen eines Sommers [74], [75]
sterbe = [138_024, 166_312, 302_921, 420_949]
def fa_aus(n):
    roh = [x / sum(n) / s for x, s in zip(n, sterbe)]
    return [round(r / roh[3], 3) for r in roh]
fa25, fa26 = fa_aus([80, 210, 660, 1560]), fa_aus([1510, 2440, 3890, 8200])
assert fa25 == [0.156, 0.341, 0.588, 1.0] and fa26 == [0.562, 0.753, 0.659, 1.0]
assert fa_aus([65, 129, 252, 555]) == fa0
# c_kal neu gefittet (run_evaluation, calibrate_heat_mortality_rev7.py, gemessen 27.09.2026): 0,651 und 0,534
assert abs(betrag(0.651, fa25) - 310.2) < 0.05 and abs(betrag(0.534, fa26) - 402.9) < 0.05
assert abs(sum(tote(0.651, fa25)) - 276.4) < 0.05 and abs(sum(tote(0.534, fa26)) - 278.2) < 0.05
assert round(betrag(0.651, fa25) / basis - 1, 2) == -0.15 and round(betrag(0.534, fa26) / basis - 1, 2) == 0.11
# einfachere Rechnung: c_kal fest 0,581
assert abs(betrag(0.581, fa25) - 277.0) < 0.05 and abs(betrag(0.581, fa26) - 438.3) < 0.05
# Band von L_a: Stuetzstelle bis sterbefallgewichteter Wert (§3.5)
L_lo, L_hi = [23.39, 15.31, 8.54, 4.16], [28.64, 15.59, 8.90, 4.20]
assert abs(betrag(0.581, fa0, L_lo) - 357.3) < 0.05 and abs(betrag(0.581, fa0, L_hi) - 381.1) < 0.05
assert round(betrag(0.581, fa0, L_lo) / basis - 1, 2) == -0.02 and round(betrag(0.581, fa0, L_hi) / basis - 1, 2) == 0.05
d_u65 = tote(0.581, fa0)[0]
assert abs(d_u65 - 20.4) < 0.05 and abs(d_u65 * 5.25 - 107) < 0.5 and abs(d_u65 * 5.25 * voly / 1e6 - 17.2) < 0.05
# Kappung 0,794 (heat.kappung_vg): 1 - 0,206, Band aus 15,8-25,7 % [47] Tabelle 1
kapp, k_lo, k_hi = 1 - 0.206, 1 - 0.257, 1 - 0.158
assert abs(kapp - 0.794) < 1e-9 and abs(k_lo - 0.743) < 1e-9 and abs(k_hi - 0.842) < 1e-9
h = 0.149 * (1 + 1.54 * (1 - 0.149))
e7585 = (635.4 + 638.8 * (1 - h)) * voly / 1e6            # wie schutzprogramme_berlin: 169,5 Mio. EUR
assert abs(1 - 0.40 * 0.68 - 0.728) < 1e-9 and 1 - 0.40 * 0.68 < kapp   # ohne Kappung unter dem Paket
assert abs(0.85 * 0.931 - 0.791) < 0.0005 and abs(0.85 * 0.931 * 0.9956 - 0.788) < 0.0005
assert abs(0.95 * 0.931 * 0.9956 - 0.881) < 0.0005 and 0.95 * 0.931 * 0.9956 > kapp
assert abs(e7585 * (1 - kapp) - 34.9) < 0.05
assert abs(e7585 * (1 - k_hi) - 26.8) < 0.05 and abs(e7585 * (1 - k_lo) - 43.6) < 0.05
assert abs(e7585 * (1 - 0.728) - 46.1) < 0.05 and abs(e7585 * (0.794 - 0.728) - 11.2) < 0.05
# Doppelzaehlungs-Waechter (heat.vg_in_kalibrierjahren): Voreinstellung nein
anteil_ja = 4 / 53                                          # NRW, Oktober 2023 [76]
assert abs(anteil_ja - 0.075) < 0.0005
vg = e7585 * (1 - 0.931)                                    # 11,7 Mio. EUR
assert abs(vg - 11.7) < 0.05
assert abs(0.075 * 11.7 - 0.9) < 0.05 and abs(0.925 * 11.7 - 10.8) < 0.05   # erwarteter Fehler nein gegen ja
```

## 8 Quellen (§3.8 — #95-relevanter Auszug; Nummern [11]–[62] = M0-Zählung)

Zugriff 17./18.08.2026 ([47], [63], [64]: 26.08.2026). **Archiv-Snapshots** (Befund 61):
Diese Session erreicht web.archive.org nicht (Netz-Sandbox; Save-Versuch dokumentiert
fehlgeschlagen). Die Snapshots entstehen deterministisch über die bestehende
`sources.py`-Ratchet-Mechanik der Plattform (automatisierte Wayback-Permalink-Erzeugung,
maschinell testbewehrt — kein manueller Später-Schritt); bis zum Integrations-Ratchet sind
DOI-Links die persistenten Referenzen.

- **[11]** C. Winklmayr, S. Muthers, H. Niemann, H.-G. Mücke, M. an der Heiden, „Heat-related
  mortality in Germany from 1992 to 2021", Dtsch Arztebl Int 119:451–457, 2022.
  doi:10.3238/arztebl.m2022.0202
- **[12]** C. Winklmayr, M. an der Heiden, „Hitzebedingte Mortalität in Deutschland 2023 und
  2024", Epid Bull 19/2025:3–9. doi:10.25646/13135 (revidierte Reihe 1992–2024 inkl.
  Bundesländer-Excel); RKI-Wochenberichte 2025/2026.
- **[13]** M. an der Heiden u. a., „Hitzebedingte Mortalität — Hitzewellen in Deutschland
  1992–2017", Dtsch Arztebl Int 117:603–609, 2020. doi:10.3238/arztebl.2020.0603
- **[14]** M. an der Heiden u. a., Bundesgesundheitsblatt 62(5):571–579, 2019.
  doi:10.1007/s00103-019-02932-y; dies., Berlin/Hessen 2018, Epid Bull 23/2019:193–202.
- **[15]** UBA (Hrsg.), KWRA 2021, Teilbericht 5 (Climate Change 24/2021), Kap. 4.2.1 Hitzebelastung, S. 153–172, umweltbundesamt.de
  (lokal: `docs/KWAR/kwra2021_teilbericht_5_cluster_wirtschaft_gesundheit_bf_211027_0.pdf`).
- **[16]** Destatis, Pressemitteilungen ICD-T67: N035 (15.07.2024), Zahl der Woche 27
  (01.07.2025), N045 (02.07.2026), destatis.de/DE/Presse.
- **[17]** Destatis, „Kostennachweis der Krankenhäuser 2023", Fachserie/Statistischer
  Bericht 12-6-4 (bereinigte Kosten je Behandlungsfall ≈ 6.996 €), destatis.de.
- **[18]** M. Karlsson, N. R. Ziebarth, J Environ Econ Manage 91:93–117, 2018.
  doi:10.1016/j.jeem.2018.06.004
- **[19]** UBA, „Methodenkonvention 4.0", Abschn. 3.4 + Fn. 17–19; M. Amann u. a., IIASA
  2020a, Tab. 3.15 (VOLY 79.500 €₂₀₀₅; Archiv-Link vorhanden); Destatis-VPI lange Reihen
  (2020 = 100: 2005 81,5 · 2023 116,7 · 2024 119,3); Eurostat nama_10_pc; EUROCONTROL
  Standard Inputs (VSL 4,7 Mio. €, Preisstand 2024).
- **[33]** DWD Climate Data Center (CDC): Raster air_temperature_mean, hot_days;
  Gebietsmittel; Tageswerte 21 Stationen.
- **[38]** J. Nicholl u. a., Emerg Med J 24:665–668, 2007. doi:10.1136/emj.2007.047654 (+≈1 %/10 km).
- **[39]** M. P. Larsen u. a., Ann Emerg Med 22:1652–1658, 1993. doi:10.1016/S0196-0644(05)81302-2;
  T. D. Valenzuela u. a., Circulation 96:3308–3313, 1997. doi:10.1161/01.CIR.96.10.3308 (Hilfsfrist-Pfad).
- **[40]** J. C. Semenza u. a., N Engl J Med 335:84–90, 1996. doi:10.1056/NEJM199607113350203
  (OR ≈ 2,3 allein lebend).
- **[41]** A. Bouchama, M. Dehbi, G. Mohamed, F. Matthies, M. Shoukri, B. Menne, „Prognostic factors in heat wave
  related deaths: a meta-analysis“, Arch Intern Med 167(20):2170–2176, 2007. doi:10.1001/archinte.167.20.ira70009
  (Meta-Analyse von sechs Fall-Kontroll-Studien mit 1.065 Todesfällen; Abstract, Teil Results: bettlägerig OR 6,44
  (4,5–9,2), nicht täglich aus dem Haus OR 3,35 (1,6–6,9), Klimaanlage zu Hause OR 0,23 (0,1–0,6), Besuch kühler Orte
  OR 0,34 (0,2–0,5); Abstract gelesen am 27.09.2026 über Europe PMC,
  https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:17698676%20AND%20SRC:MED&resultType=core&format=json,
  SHA-256 des Abrufs c90cbb89…8785; Volltext nicht frei zugänglich). Verwendet in §3.3b und §5 (Kühlzentren).
- **[42]** A. Fouillet u. a., Int J Epidemiol 37:309–317, 2008. doi:10.1093/ije/dym253
  (Frankreich 2006: ≈ −4.400).
- **[44]** J. Klenk, C. Becker, K. Rapp, Age Ageing 39(2):245–251, 2010. doi:10.1093/ageing/afp248
  (+26 %/+62 % bei 32–33,9/≥ 34 °C).
- **[45]** H. Feldbusch, A. Schneider, F. Matthies-Wiesler, A. Matzarakis, A. Peters,
  S. Breitner-Busch, V. Huber, „Assessing the effectiveness of the heat health warning
  system in preventing mortality in 15 German cities: A difference-in-differences approach",
  Environment International 203:109746, 2025. doi:10.1016/j.envint.2025.109746 (Open Access,
  CC BY; Daten 1993–2020; RR 1,00 [0,98–1,01], adjustiert 0,85 [0,75–0,97] — Volltext
  gegengelesen, Gegenprüfung T2.4 ✓).
- **[46]** G. M. Katz, K. A. Brown, V. Giannakeas, N. M. Stall, „Air Conditioning in Nursing
  Homes and Mortality During Extreme Heat", JAMA Internal Medicine 186(2):243–251, 2026
  (online 15.12.2025). doi:10.1001/jamainternmed.2025.6595 (Open Access, PMC12706679;
  rOR 0,93 — Volltext gegengelesen, Gegenprüfung T2.4 ✓).
- **[47]** A. Urban, V. Huber, S. Henry, N. P. Plaza, L. Tušlová, S. Dasgupta, P. Masselot,
  I. Cvijanovic, M. Mistry, M. Pascal, F. de'Donato, C. Di Napoli, S. N. Gosling,
  S. Kohnová, J. Kyselý, S. Lüthi u. a., „The effectiveness of heat prevention plans in
  reducing heat-related mortality across Europe", Environmental Research Letters
  20:124071, 2025 (online 23.12.2025). doi:10.1088/1748-9326/ae2775 (Open Access;
  102 Standorte, 14 Länder, 1990–2019; HAF-Reduktion 25,2 % [19,8–31,9], regional
  −11,9…−33,2 %, ohne 2003: 15,2 % [4,1–23,7] — Effektzahlen aus dem Volltext korrigiert
  26.08.2026, Befund 68; die frühere Angabe „2–23 %" stammte aus einem in Rev. 5 nicht
  am Volltext belegten Zitat und steht nicht in der Studie). Fundstellen für §5 (Befund 128,
  Volltext PMC12724396, gelesen 26.09.2026): Deutschland −20,6 % (−25,7; −15,8) in Tabelle 1,
  Westeuropa; die Wirkung wird über einen Indikator „Plan vorhanden" geschätzt (Abschnitt 2.2 und
  Stufe 2 der statistischen Auswertung), eine Schätzung je Baustein enthält die Studie nicht.
- **[48]** Destatis, Statistischer Bericht „Sterbetafeln 2022/2024" (Juli 2025), Blätter
  12613-b01/-b02, destatis.de; Bevölkerungsgewichte: Fortschreibung 31.12.2023
  (regionalstatistik.de, Tab. 12411-09-01-4-B, Basis Zensus 2022).
- **[49]** Destatis, Statistischer Bericht „Sterbefälle 2023", Tab. 12613-03 (Gestorbene
  nach Altersgruppen; M+F = 1.028.206), destatis.de ÷ Bevölkerung 31.12.2023 (83.456.045).
- **[50]** Kalibrierläufe: `backend/scripts/kalibrierung/calibrate_heat_mortality.py`
  (Rev. 5), `calibrate_heat_mortality_rev6.py` (Rev. 6) und
  `calibrate_heat_mortality_rev7.py` (Rev. 7: DWD-CDC-JJA-Raster 1 km [33] ×
  VG250-Gemeindepunkte × Zensus-Gemeindebevölkerung) + `backend/data/kalibrierung/`
  (RKI-Anhang EB 19/2025, CC BY 4.0; `c_kal_rev7_ergebnis.md`, `c_kal_rev7_verteilung.csv`,
  `sommermittel_bundesland_povw.csv`, `temperatur_offsets_bundesland.csv`;
  Rev.-6-Stände zur Reproduzierbarkeit); Rev. 8: `l85_sterbefallgewichtung.py`
  (+ `.csv`/`.md` — L̄_85+ exakt aus Statistischen Berichten [48]/[49], keyless).
- **[60]** A. Fouillet u. a., Int Arch Occup Environ Health 80:16–24, 2006.
  doi:10.1007/s00420-006-0089-4, Tab. 2 (O/E nach Sterbeort: Heime 1,9 [1,7–2,1],
  Wohnung ≥ 75: 1,9, Kliniken 1,5).
- **[61]** Destatis, Pflegestatistik 2023 (GENESIS-Online, Tab. 22421-0001,
  www-genesis.destatis.de; PM 478/2024: 0,80 Mio. vollstationär; 85–<90: 218,7 Tsd.,
  90–<95: 142,6 Tsd., ≥ 95: 63,0 Tsd.); WIdO-Pflegereport (Sterberate Heimbewohner
  ≈ 0,6–0,7 %/Woche).
- **[62]** M. Karlsson, N. R. Ziebarth, IZA Discussion Paper 7875 (docs.iza.org/dp7875.pdf),
  Tab. 1/3, Fig. 9, App. A.
- **[63]** Destatis/BMFSFJ-Open-Data, „Anteil von Frauen und Männern ab 65 Jahren in
  Einpersonenhaushalten", Mikrozensus 2023 (Erstergebnisse): **34,6 %**
  (daten.bmbfsfj.bund.de, Indikator 132088; Zugriff 26.08.2026).
- **[64]** „Impact of Heat Waves on Hospitalisation and Mortality in Nursing Homes:
  A Case-Crossover Study", Int J Environ Res Public Health 18(20):10697, 2021.
  doi:10.3390/ijerph182010697 (Flandern, 10 Heime 2013–2017; Mortalität OR 1,61 [1,10–2,37],
  Hospitalisierung OR 0,96 [0,67–1,36] n. s.).
- **[65]** BKG, Verwaltungsgebiete 1:250.000 (VG250), GeoPackage `DE_VG250.gpkg`
  (Repo-Bestand `backend/data/vg250/`, sha256-Pin s. §4 `#t-povw`), gdz.bkg.bund.de —
  Datenlizenz Deutschland Namensnennung 2.0 (dl-de/by-2-0), © GeoBasis-DE / BKG.
- **[66]** Statistische Ämter des Bundes und der Länder, Zensus 2022 — Bevölkerung je
  Gemeinde, aufbereitet aus den Gitterdaten 100 m [67] durch das Modul
  `backend/app/services/lite/zensus_gemeinde.py`. Das Modul rechnet mit einer Näherung: Es fasst
  die 100-m-Zellen zu 1-km-Zellen zusammen und ordnet jede 1-km-Zelle ganz der Gemeinde aus
  VG250 [65] zu, in der ihr Mittelpunkt liegt. Kleine Gemeinden bekommen dadurch zu viele oder zu
  wenige Einwohner; Gemeinden, in denen kein Mittelpunkt einer 1-km-Zelle liegt, bekommen keine
  (die 96 VG250-Gemeinden ohne Zensus-Eintrag in §4, `#t-povw`). Die Aufbereitung
  `zensus_gemeinde.json` erzeugt das Modul im Datenverzeichnis des Backends; sie liegt nicht im
  Repo, ihr sha256-Pin `124fd7a7a15b` steht beim Kalibrierlauf in §4 (`#t-povw`). Die
  Regionaltabelle Demografie [69], Spalte „Insgesamt“, taugt als amtliche Gegenprobe nur mit
  diesem Vorbehalt: Für große Gemeinden passt sie, bei kleinen weicht [66] wegen der Zuordnung
  über den Mittelpunkt ab. zensus2022.de — dl-de/by-2-0.
- **[67]** Statistische Ämter des Bundes und der Länder, Zensus 2022 — Gitterdaten 100 m,
  Stichtag 15.05.2022: „Bevölkerungszahl in Gitterzellen“
  (https://www.destatis.de/static/DE/zensus/gitterdaten/Zensus2022_Bevoelkerungszahl.zip) und
  „Alter in 5er-Jahresgruppen“
  (https://www.destatis.de/static/DE/zensus/gitterdaten/Alter_5er-Jahresgruppen_100mGitter.zip),
  „Anteil ab 65-Jährige in Gitterzellen“
  (https://www.destatis.de/static/DE/zensus/gitterdaten/Anteil_ab_65-jaehrige_in_Gitterzellen.zip),
  abgerufen 25.09.2026 — dl-de/by-2-0. Verwendet für den Zellvergleich Berlin in §3.0
  (Skript `docs/methodik/anlagen/95_zellvergleich.py`).
- **[68]** W. Kahlenborn, L. Porst, M. Voß, L. Hölscher, S. Undorf, M. Wolf, K. Schönthaler,
  A. Crespi, K. Renner, M. Zebisch, U. Fritsch, I. Schauser, „Klimawirkungs- und Risikoanalyse 2021
  für Deutschland — Teilbericht 6: Integrierte Auswertung – Klimarisiken, Handlungserfordernisse und
  Forschungsbedarfe“, Umweltbundesamt, Climate Change 25/2021, Dessau-Roßlau, Juni 2021
  (Publikationsseite https://www.umweltbundesamt.de/publikationen/KWRA-Teil-6-Integrierte-Auswertung;
  PDF https://www.umweltbundesamt.de/sites/default/files/medien/479/publikationen/kwra2021_teilbericht_6_integrierte_auswertung_bf_211027_0.pdf,
  abgerufen 25.09.2026; im Repo `docs/KWAR/kwra2021_teilbericht_6_integrierte_auswertung_bf_211027_0.pdf`).
  Verwendet: Tabelle 1, S. 41 (Stufen und Gewissheit „Hitzebelastung“), Kapitel 3.3, S. 78–79 mit
  Fußnote 18 (Zahlenskala der Gewissheit). Aufbereitet in `docs/KWAR/KWRA-2021_Klimawirkungen.xlsx`.
- **[69]** Statistische Ämter des Bundes und der Länder, Zensus 2022 — Regionaltabelle „Demografie“
  (Ausgewählte Ergebnisse zur Demografie zum Stichtag 15.05.2022), Blatt „Demografie“, Spalten
  „Insgesamt“ und „Im Alter von … bis … Jahren: 60–66, 67–74, 75 und älter“, Zeilen ARS
  032565408034 (Warmsen: 3158 · 388 · 257 · 345) und 110000000000 (Berlin, Stadt: 3.596.999 ·
  292.354 · 261.676 · 362.829) (https://www.destatis.de/static/DE/zensus/gitterdaten/Regionaltabelle_Demografie.xlsx,
  abgerufen 25.09.2026; Archiv
  https://web.archive.org/web/20260925192632/https://www.destatis.de/static/DE/zensus/gitterdaten/Regionaltabelle_Demografie.xlsx)
  — dl-de/by-2-0. Verwendet in §3.3 (Stufe 2 der Ersatzregel für den geheimgehaltenen Anteil 65+).
  Das Skript `docs/methodik/anlagen/95_zellvergleich.py` liest dieselben Zahlen aus dem Blatt
  „CSV-Demografie“ (Spalten `0_Insgesamt_`, `Alter_infr__09` = 60–66, `Alter_infr__10` = 67–74,
  `Alter_infr__11` = 75 und älter); Zeichenerklärung dort: „–“ = genau null oder auf null geändert,
  „.“ = Zahlenwert unbekannt oder geheim.
- **[70]** G. Liotta, M. C. Inzerilli, L. Palombi, O. Madaro, S. Orlando, P. Scarcella, D. Betti,
  M. C. Marazzi, „Social Interventions to Prevent Heat-Related Mortality in the Older Adult in Rome,
  Italy: A Quasi-Experimental Study", International Journal of Environmental Research and Public
  Health 15(4):715, 2018. doi:10.3390/ijerph15040715 (Open Access, PMC5923757; Volltext gelesen
  26.09.2026, Befund 128: Sterberate ab 75 im Sommer 2015 gegenüber 2014 +48,8 % in Stadtteilen mit
  dem Programm „Long Live the Elderly", +97,3 % ohne, Tabelle 2; 167 und 169 Todesfälle, Abschnitt 3;
  Menschen ab 75 in den Stadtteilen 6.483 mit und 5.724 ohne Programm, Tabelle 1; eingeschrieben 4.720,
  Abschnitt 3, also 72,8 %; ökologischer Vergleich ganzer Stadtteile, Grenzen in Abschnitt 4, letzter
  Absatz; Anstieg je Stadtteil in Tabelle 2, Zeile Δ1, mit Fußnote 1 (Mittel und Standardabweichung nach Einwohnern
  gewichtet); bereinigte Regression in Tabelle 3, Zeile „LLE program (no vs. yes)“, trägt den Zentralwert von \(w_{\text{VG}}\); vollständig gelesen am 26.09.2026: Abschnitte
  2.1, 2.4, 3 und 4, Tabellen 1–3, im Volltext von Europe PMC,
  https://www.ebi.ac.uk/europepmc/webservices/rest/PMC5923757/fullTextXML, Befunde 133 und 134; abgerufen 26.09.2026; Archiv-Snapshot über den
  Integrationsschritt wie bei [46]). Verwendet in §5 (Schutzprogramme vulnerable Gruppen).
- **[71]** K. Gaede, „Pflegeheime improvisieren gegen die Hitze“, Care vor9 (Gloobi GmbH & Co. KG), 12.08.2026,
  https://www.carevor9.de/inside/pflegeheime-improvisieren-gegen-die-hitze (abgerufen 27.09.2026, 10:27 UTC, SHA-256
  2fc389e4…6664). Umfrage unter Pflegeeinrichtungen mit 140 Rückmeldungen, nicht repräsentativ: „Nur elf Prozent der
  Befragten haben eine Klimaanlage in ihrer Einrichtung. Einige haben zumindest einzelne Aufenthaltsräume, Speisesäle
  oder Flure klimatisiert“ (Abschnitt „Kälteinseln statt Vollklimatisierung“). Verwendet in §5 (Voreinstellung
  \(s_{\text{gek}}\)). Archiv: web.archive.org antwortete am 27.09.2026 nicht (Zeitüberschreitung, dann HTTP 429);
  Snapshot über den Integrationsschritt wie bei [46].
- **[72]** Statistisches Bundesamt (Destatis), „4,3 % der im Jahr 2025 fertiggestellten Wohngebäude haben eine Anlage
  zur Kühlung“, Zahl der Woche Nr. 27 vom 30.06.2026,
  https://www.destatis.de/DE/Presse/Pressemitteilungen/Zahl-der-Woche/2026/PD26_27_p002.html (abgerufen 27.09.2026,
  10:27 UTC, SHA-256 925adf71…081c): „Bei den 683 neuen Gebäuden des Sozialwesens waren es dagegen nur 14,5 % (2015:
  5,7 %). Hierzu zählen unter anderem Kitas und Pflegeeinrichtungen.“ (Abschnitt „Jedes dritte neue Gebäude im
  Bildungswesen und im Gesundheitswesen hat eine Anlage zur Kühlung“; Grundlage Tabellen 31121 in GENESIS-Online).
  Verwendet in §5 (Band von \(s_{\text{gek}}\)). Archiv wie [71].
- **[73]** R. D. Meade, S. R. Notley, A. P. Akerman, J. J. McCormick, K. E. King, R. J. Sigal, G. P. Kenny, „Efficacy of
  Cooling Centers for Mitigating Physiological Strain in Older Adults during Daylong Heat Exposure: A Laboratory-Based
  Heat Wave Simulation“, Environmental Health Perspectives 131(6):067003, 2023. doi:10.1289/EHP11651 (Open Access,
  PMC10234508; Abstract, Teile Methods und Results, Volltext nicht ausgewertet: 40 Menschen von 64 bis 79 Jahren, neun Stunden Hitzeindex
  37 °C, Kühlgruppe 2 h bei rund 23 °C in den Stunden 5–6; Kerntemperatur 0,8 °C (0,6–0,9) niedriger am Ende der
  Kühlung, 0,3 °C (0,2–0,4) eine Stunde danach, in den Stunden 8 und 9 gleich; gelesen am 27.09.2026 über Europe PMC,
  https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:10.1289/EHP11651&resultType=core&format=json,
  SHA-256 des Abrufs f3571bb0…1582). Verwendet in §5 (Kühlzentren, \(t_{\text{KZ}}\)). Archiv wie [71].
- **[74]** M. an der Heiden, B. Zacher, RKI-Geschäftsstelle für Klimawandel & Gesundheit, M. Diercke, V. Bremer,
  „Wochenbericht zur hitzebedingten Mortalität KW 38/2025 vom 02.10.2025“, Robert Koch-Institut. doi:10.25646/13466
  (https://edoc.rki.de/bitstream/handle/176904/12995/RKI-Wochenbericht_Hitzemortalit%C3%A4t_KW38_2025-10-02.pdf,
  abgerufen 27.09.2026, 11:02 UTC, HTTP 200, SHA-256 bf3e0f50…c9c8). Tabelle 1, Seite 1: Sommer 2025, kumulativ KW 15–38,
  Gesamt 2.500 [1.200; 3.700], Altersgruppen < 65: 80, 65–74: 210, 75–84: 660, 85+: 1.560 („auf die Zehnerstelle
  gerundet“). Verwendet in §3.3a (Band von \(f_a\)). Archiv wie [71]; die DOI ist die persistente Referenz.
- **[75]** M. an der Heiden, B. Zacher, RKI-Geschäftsstelle für Klimawandel & Gesundheit, M. Diercke, V. Bremer,
  „Wochenbericht zur hitzebedingten Mortalität KW 37/2026 vom 24.09.2026“, Robert Koch-Institut. doi:10.25646/14459
  (https://www.rki.de/DE/Themen/Gesundheit-und-Gesellschaft/Gesundheitliche-Einflussfaktoren-A-Z/H/Hitze/Bericht_Hitzemortalitaet.html,
  abgerufen 27.09.2026, 11:01 UTC, HTTP 200, SHA-256 76af8672…f1ce; die Seite wird wöchentlich überschrieben). Tabelle 1:
  Sommer 2026, kumulativ bis KW 37, Gesamt 16.000 [14.400; 17.600], < 65: 1.510, 65–74: 2.440, 75–84: 3.890, 85+: 8.200.
  Verwendet in §3.3a (Band von \(f_a\)). Archiv wie [71]; die DOI ist die persistente Referenz.
- **[76]** K. Müller, „Stand der kommunalen Hitzeaktionsplanung in Nordrhein-Westfalen“, Abstract zur
  Online-Informationsveranstaltung „Gesundheitsbezogener Hitzeschutz in Nordrhein-Westfalen: Status quo und Perspektiven
  2024“ des Landeszentrums Gesundheit Nordrhein-Westfalen (LZG.NRW), 10.06.2024
  (https://www.lzg.nrw.de/_php/login/dl.php?u=%2F_media%2Fpdf%2Fservice%2FVeranst%2F240610_hitze%2FMUELLER_Abstract.pdf,
  abgerufen 27.09.2026, 11:03 UTC, HTTP 200, SHA-256 b25987ca…622c): „In Deutschland gibt es bisher nur wenige
  veröffentlichte kommunale Hitzeaktionspläne, deutschlandweit insgesamt 18 (Stand 10.06.2024).“ Befragung der 53 Kreise und
  kreisfreien Städte in Nordrhein-Westfalen im September 2023, Begriff „weit gefasst“ (Planwerke und gebündelte Maßnahmen):
  „in vier Kommunen lag bereits ein Hitzeaktionsplan vor, zehn Kommunen erstellten einen Hitzeaktionsplan und 25 Kommunen
  planten die Erstellung (Stand: 13.10.2023)“. Verwendet in §5 (Voreinstellung des Doppelzählungs-Wächters). Archiv wie [71].

## Entscheidungslog

Einträge 1–18: in M0 (Rev. 1–5) getroffene Setzungen (rückwirkend dokumentiert bei der
Migration). Einträge 19–27: Rev.-6-Entscheidungen (`/risiko-auto`, Gate 1); Einträge 28–30:
Revision nach Review-Runde 1 (Befunde 58/59/62); Einträge 31–33: Rev.-7-Kalibrier-Revision
(Auflösung der §6-Eskalation, 30.08.2026). Einträge 37–38: verworfene Ansätze aus dem früheren
Kapitel 9 (Ansatz-Vergleich), das mit Fortschreibung 7 entfällt (eine Methodik je Risiko,
Befund 95); der gewählte Ansatz 95-A ist Nr. 1. Einträge 39–40: Fortschreibung 7, Schritt 2
(Pflichtabschnitt „Risiko ohne (weitere) Anpassung“, Kennzeichnung der Parameter; Befunde 107–111).
Eintrag 41: Ersatzregel für den geheimgehaltenen Anteil 65+ (T-1199, Befunde 104, 116 und 117;
Stufe 2 neu gefasst in T-1233, Befunde 99, 117 und 119). Eintrag 42: Stichtag der Einwohner je
Altersband in Ebene 1 (T-1233, Befunde 99 und 120). Eintrag 43: Schutzprogramme vulnerable Gruppen
gegenüber dem Katalogwert im Produkt (T-1295, Befunde 123 und 124; Zentralwert T-1333, Befund 134). Eintrag 44: Hebel S157
gegenüber der geparkten Maßnahme im Produkt (T-1329, Befund 130). Einträge 45–46: Voreinstellung \(s_{\text{gek}}\),
\(h_{\text{Heim}}\) je Zelle, S157 im Anpassungspotenzial und öffentliche Kühlzentren (T-1537, Befunde 138, 139, 146,
148 und 149; Eintrag 44 dadurch fortgeschrieben). Einträge 47–49: Doppelzählungs-Wächter mit Eingabe und
Voreinstellung, Kappung 0,794 als eigener Parameter, Bänder von \(f_a\) und \(\bar L_a\) (T-1538, Befunde 150–152).
**Überstimmungsweg für alle Einträge:** „Entscheidung Nr. X ändern auf …" → Delta-Lauf
(Neurechnung betroffener Kopplungen + Re-Review). ⚠ = Ermessensfall.

| Nr | Frage | angewendete Entscheidung | Begründung | Alternative | Auswirkung |
|---|---|---|---|---|---|
| 1 | Methodischer Ansatz für #95? | **95-A** RKI-ERF bottom-up | publizierte Kurve, implementiert, kalibrierbar (M0 Kap. 5) | 95-C; 95-B per §3.1 ausgeschieden | Gesamtmodell |
| 2 | Mortalitäts-Bewertung? | **YLL × VOLY** (MK 4.0); VSL nur Sensitivität | altersgerecht, konservativer (Faktor ≈ 5), MK-4.0-konform | VSL 3,5 / 4,7 / 6,19 Mio. € | −80 % ggü. VSL-Weg |
| 3 | Native Ergebnisgröße? | **YLL/Jahr**; D, F, € Teil-Ausweise | kommunizierbarer als Todesfall-Bruchteile je Zelle | Todesfälle/Jahr | Ausweis |
| 4 | VOLY-Zahlenwert? | **160.800 €₂₀₂₄** (Elastizität 0,85 auch beim Raumtransfer) | konsistent zur Einkommenselastizität; MK 4.0 legt sie nicht offen | Band 136,4–165,6 T€ | ±15 % €-Mortalität |
| 5 | Wochenverteilung? | **empirische intra-saisonale Quantile**, σ aus 21 Stationen | §3.2-Tails; gemessene σ 2,36–2,58 K statt Setzung 2,0 K | Gauß (Abweichung ≤ 0,12 K) | Tail-Treue |
| 6 | (ersetzt durch Nr. 26) | — | — | — | — |
| 7 | (ersetzt durch Nr. 26) | — | — | — | — |
| 8 | (ersetzt durch Nr. 19) | — | — | — | — |
| 9 | (ersetzt durch Nr. 23) | — | — | — | — |
| 10 | Maßnahmen-Effektgrößen? | **Interventionsevidenz, marginal**: \(\delta_{\text{HAP}}\) 0,95 auf (RR−1); Klimaanlagen rOR 0,93; Doppelzählungs-Wächter | Fall-Kontroll-ORs überschätzen Einführungswirkung 5–10× | Fouillet-großer Hebel (−4.400) — Doppelbuchung | Maßnahmenwerte klein, ehrlich |
| 11 | Kante #63 Innenraumklima? | **kein eigener Knoten in M0** — Nachtkomponente des 24-h-Mittels + Hebel S157 | Gebäudephysik-Risiko folgt in M1; Kante bleibt adressiert | eigener Innenraum-Term | Kette vollständig adressiert |
| 12 | Grünanteil als Vulnerabilität? | **nein** — steckt im UHI-Zuschlag | Kein-Doppelkanal (§3.2) | zweiter Grün-Kanal | keine Doppelzählung |
| 13 | (ersetzt durch Nr. 20) | — | — | — | — |
| 14 | Kreis-Prävalenzen / GISD? | **Sensitivitätsband**, nicht Basiswert | gröber als Zelle; Evidenz für Zellsteigung fehlt | zentrierter Modifikator im Basiswert | Basiswert schlanker |
| 15 | Exertional-Spitze (S154)? | **nicht modelliert** (dokumentiert, bewusst inaktiv) | überwiegend ambulant, keine Zellgröße | ambulanter Zusatzpfad | Untergrenze |
| 16 | \(r_{0,a}\)-Altersaufteilung? | Raten 1,9/6,3/10,8/15,6 (**= 1:3,3:5,7:8,2**, Summe 3,54) als gekennzeichnete Abschätzung | Rev.-5-Inkonsistenz behoben (Option A der Gegenprüfung); GENESIS-Alterssplit nicht keyless | Option B (echtes 1:5:8:10 → 1,53/7,63/12,21/15,26) | Morbiditäts-Altersprofil |
| 17 | Behandlungskostensatz? | **7.152 €₂₀₂₄** (indexiert), **als Proxy gekennzeichnet** | einzige offene, belegte Zahl; Preisstand harmonisiert | DRG-/Diagnosegruppen-Sätze (Sensitivität) | Morbiditäts-€ |
| 18 | Harvesting? | Mortalität: robust via RKI-Wochenmethodik; **F: keine zusätzliche Korrektur** (im K&Z-Jahresaggregat enthalten) | Jahresaggregat reduziert Tageseffekte > 90 % [18] | explizite −25 %-Korrektur auf F | keine Doppel-Korrektur |
| 19 ⚠ | \(e_{\text{HD}}\)-Basiswahl? | **konditional 0,024** als Basis; 0,054 Obergrenze | marginaler Effekt eines zusätzlichen Hitzetags; Untergrenzen-Linie (Befund 5) | unkonditional 0,054 (Rev.-5-Wahl) | F-Zusatzterm −55 % |
| 20 ⚠ | Distanzterm \(\beta_d\) im Basiswert? | **nein** — Sensitivitätsband (Default 0) | Evidenz misst transportierte Notfälle, Hitzetote sterben zu Hause; \(\bar d\) ohne Batch nicht herleitbar (Befunde 7/17) | 0,001/km mit \(\bar d\) aus Ebene bei Integration | ±1,5 % entfällt; ehrlicher |
| 21 ⚠ | \(\bar q_{\text{1P}}\)? | **0,346** (Mikrozensus 2023, amtlich [63]) | ersetzt Setzung 0,40; \(\beta_{\text{iso}}\) neu = 0,90 | 0,40 (Rev.-5-Setzung) | Zentrierung exakter |
| 22 | \(f_a\)? | **0,357/0,588/0,631/1,0** (Rückrechnung mit neuen \(m_a\), §3.3a) | Kette reproduzierbar; Kopplung \(f_a\leftrightarrow m_a\) neu gerechnet (Befund 32) | Rev.-5-Werte 0,404/0,577/0,620 | u65-Band −12 %; Altersvalidierung < 1 pp |
| 23 ⚠ | Pflegeheim-OR? | **3,0** (Band 2,2–6,0), Kette §3.3b; \(\beta_{\text{pfl}}\) = 1,54, nur 85+, nur D-Pfad | reproduzierbare Kette (Befund 9); Bänder = Evidenz (Befunde 8/44); F-Gegenevidenz [64] (Befund 7) | 3,5 (Rev.-5-Wahl, Kette nicht reproduzierbar) | 85+-Spreizung ±23 % statt ±27 % |
| 24 | \(\beta_{\text{pfl}}\)/\(\beta_d\) im F-Pfad? | **Default 1** (nur \(\beta_{\text{iso}}\) wirkt auf F) | Flandern-Studie: kein Hospitalisierungseffekt [64] | Rev.-5: volles \(v_{\text{vers}}\) auf F | F-Verteilung plausibler |
| 25 ⚠ | HD-Datenquelle? | **DWD-CDC hot_days ohne UHI-Verschiebung** (Ist-Stand Produkt) | keine implementierte Umrechnungsregel; Rev.-5-Text beschrieb Nicht-Implementiertes (Befund 38) | UHI→hot_days-Regel definieren und implementieren (Fortschreibung) | Morbidität in UHI-Lagen Untergrenze |
| 26 ⚠ | Kalibrierung: Skalar, Fenster, Regionen? | (Fensterwahl bleibt; Skalar-/Regionen-Teil **ersetzt durch Nr. 31–33**) ein nationaler Skalar, Fenster 2012–2024, ohne vorl. 2025 | §3.4; Holdout belegt Fensterwahl (2/9 out-of-sample bei Vollreihen-Fit) | Vollreihe als Basis | Fensterwahl unverändert in Rev. 7 |
| 27 | (ersetzt durch Nr. 30 nach Review-Runde 1, Befund 62) | — | — | — | — |
| 28 ⚠ | \(\beta_{\text{iso}}\) im F-Pfad? | **Default 1** — nur D-Pfad (Bänder 65+) | Semenza misst Todesfälle; für Einweisungen keine Evidenz (§3.2: unbelegte Modulatoren Default 1; Befund 58) | Morbiditätsevidenz nachtragen (Kandidat: Chicago-Einweisungsdaten) und Register-Zeile je Endpunkt trennen | F ohne Isolations-Spreizung |
| 29 ⚠ | F-Formel: HD-Term? | **zweiseitig linear, bei 0 gedeckelt**: \(\max(0,\,1+e_{\text{HD}}(\text{HD}-\text{HD}_{\text{ref}}))\); Lackmustest-Aussage auf Mortalität eingeschränkt, Morbiditäts-Sockel als dokumentierte Grenze | behebt den Jensen-Rest des Positivteils (Befund 59b); Sockel = nicht-wetterlicher T67-Kern | Klimaanteil-Zerlegung des Sockels (hitzeproportionaler Anteil ≈ 0,51 aus #r0-a) — dokumentierte Fortschreibungsoption | Zellen unter HD_ref bis −17 %; keine Doppelzählung |
| 30 ⚠ | Befund-1-Behandlung im Ausweis? | (**ersetzt durch Nr. 31**: die Pauschalkorrektur ×0,82 entfällt — die Bias-Komponente ist in Rev. 7 direkt gemessen) | Befund 62-Logik bleibt gültig, Umsetzung nun messungsbasiert | — | — |
| 31 ⚠ | Kalibrierbasis Rev. 7? | **bevölkerungsgewichtete Sommermittel je Land** (DWD-JJA-Raster × Gemeindepunkt × Zensus-Bevölkerung; Skript rev7) statt Flächenmittel + Pauschalkorrektur | setzt die in §4 (Rev. 6) benannte keyless Messung um; löst die Befund-1-Hauptkomponente direkt (DE +0,53 K, regional heterogen); §6-Eskalation ohne Zell-Lauf auflösbar | Zell-Lauf sofort (braucht Produktionsimplementierung — Kausalschleife mit der Abnahme) | c_kal 0,742 → 0,581; Prüfstein-Basis |
| 32 ⚠ | Regionale ERF-Nachschätzung? | **nur Süd**: \(s_{\text{Süd}}\) = 1,65 (Holdout-Fit ohne 2018/19/22; Profil-Band 1,45–1,85, Bandregel +10 % Zielfunktion) ⇒ \(\beta_{85+,\text{Süd}}\) = 0,0876 K⁻¹; Nord nicht identifizierbar (0 Fit-Jahre), Mitte-Optimum 1,0 | §3.4 („Wirkungsfunktion regional nachschätzen"); minimal-invasiv genau dort, wo Diagnose + Identifikation zusammenkommen; Einbrenn-Einwand aus Nr. 26 durch messungsbasierte Kalibrierbasis entkräftet | 3-Regionen-Nachschätzung (verworfen: Nord-Skalar läuft mangels Daten an den Gitterrand und zerstört die Nord-Prüfung) | Prüfstein 10/16 → **12/16 (bestanden)** |
| 33 | Regionale Übergangsfaktoren? | **entfallen** — Produktausweis mit genau einem nationalen Skalar | Prüfstein mit einem Skalar bestanden; §3.4-Ideal erreicht | c_reg beibehalten (unnötig geworden) | Süden im Ausweis über \(\beta_{\text{Süd}}\) statt Faktor ×1,6 |
| 34 ⚠ | Finaler Kalibrier-Abgleich ohne Zell-Lauf? | **kommunale Stichproben-Abgleiche** (Anker-Kommunen, Produktionsmodell) ersetzen den nationalen 100-m-Vollraster-Lauf überall im Bericht | Nutzer-Entscheid 30.08.2026 + §3.4-Ressourcen-Regel (Aufgaben-Fortschreibung): Vollraster-Läufe fressen zu viele Ressourcen und dürfen nie Prüf-/Abgleichvoraussetzung sein | nationaler Zell-Lauf (verworfen per Regel) | Rest-Bias-Prüfung (×1,02, Topographie-Anteil Süd) läuft über Stichproben statt Vollraster |
| 35 ⚠ | q_pfl-Ebene ohne Kreis-Pflegestatistik? | `CARE_HOME_SHARE_85P` aus OSM, **kommunen-erwartungstreu** auf q̄_pfl normiert (statt Kreis-Skalierung); q_1P-Ebene **geparkt** (keine offene Quelle) | §3.1-Anlagepflicht; Tab. 22421 je Kreis nicht keyless; Erwartungstreue hält die Kalibrierneutralität je Kommune | Kreis-Skalierung (nicht keyless) · dauerhafter Neutral-Fallback (per §3.1 unzulässig) | intra-kommunale 85+-Differenzierung aktiv; zwischen Kommunen weiter q̄ |
| 36 | L̄_85+ exakt statt Approximation? | **4,16 J** — Einzeljahres-Sterbefälle 85–94 × e(x), 95+-Rest tafelintern gewichtet, m/w sterbefallgewichtet kombiniert | Befund-22-Auflösung wie in §3.5 terminiert; Kreuzcheck 12613-02↔-03 exakt | Stützstellen-Variante (4,83 — behebt nur den Gewichte-Fehler, nicht die Untergrenzen-Stützstellen) | YLL-Bundessumme ≈ −8 %; €-Ausweis sinkt entsprechend (konservativ) |
| 37 | Ansatz 95-B (nationaler Anker, top-down)? | **verworfen** | 95-B verteilt eine feste nationale Zahl von Hitzetoten über einen Schlüssel und scheidet nach §3.1 aus, weil damit auch eine Kommune ohne Hitze Todesfälle erhielte. | — (Beschreibung M0 Rev. 5, Kap. 2) | keine |
| 38 | Ansatz 95-C (Personen-Hitzegradtage-Regression)? | **verworfen** | 95-C ersetzt die publizierte und kalibrierte RKI-Kurve durch eine lineare Regression mit aufgesetzter Krümmung (κ ≈ 1,2–1,5) und wäre gegenüber 95-A ein Rückschritt. | — (Beschreibung M0 Rev. 5, Kap. 2) | keine |
| 39 ⚠ | Satz „Bestand an Klimaanlagen und Hitzeaktionsplänen im Basiswert“ (Kapitel 1, Absatz (a))? | **gestrichen** — Absatz (a) sagt nur noch, was aus der Kalibrierung folgt: \(c_{\text{kal}}\) ist an die RKI-Reihe 2012–2024 angepasst, der Anpassungsstand dieser Jahre steckt damit im Niveau; genannt bleibt nur das DWD-Hitzewarnsystem mit Beleg [45] | Der Bericht hat keine Quelle für die Klimaanlagen-Quote und keine für die Verbreitung kommunaler Hitzeaktionspläne in den Kalibrierjahren; eine Behauptung ohne Beleg bleibt nicht stehen (P1) | Satz belegen: Klimaanlagen-Quote der Haushalte und Pflegeheime sowie Einführungsjahre der Hitzeaktionspläne gegen das Fenster 2012–2024 (Fortschreibung) | keine Zahl betroffen; Aussage (a) schmaler, aber belegt |
| 40 ⚠ | Kennzeichnung der Grenzfälle in Kapitel 7? | **`abschaetzung_kap3`**, sobald eine Setzung von KAP3 im Wert steckt (\(\beta_{85+}\) Süd-Nachschätzung, \(f_a\) lineare Näherung, VOLY-Elastizität beim Raumtransfer, \(c_{\text{Fall}}\) als Proxy aus dem Durchschnitt aller Krankenhausfälle, Stützstellen e(60)/e(70)/e(80) für die Bänder u65, 65–74 und 75–84 in \(\bar L_a\), \(r_{0,a}\)-Altersprofil, \(\delta_{\text{HAP}}\), Distanzterm); **`quelle`** für reine Rechnungen aus amtlichen oder gemessenen Zahlen ohne Setzung (Quotienten, ausgezählte Quantile); Prüfstein: Misst der Wert die Zielgröße selbst, ist die bloße Wahl zwischen Quellenwerten keine Setzung (\(e_{\text{HD}}\) konditional statt unkonditional, Log 19; Stationsauswahl für \(q_w\), Log 5) — steht er für eine andere Größe (Proxy) oder nähert er ein Bandmittel durch einen Punkt an, ist es eine; **`berechnet`** nur, wo der Wert aus anderen Blöcken folgt (\(c_{\text{kal}}\), \(\beta_{\text{pfl}}\)); eine nur umgerechnete Studienzahl ist `quelle` (\(\beta_{\text{iso}}\), Befund 136) | Die Parameterliste im Produkt (P1) soll eine Setzung nie als Quellenwert zeigen; gleiche Lesart wie die Blöcke in `60_*.md` („Quotient zweier amtlicher Summen“ = `quelle`) | alle aus Quellen abgeleiteten Werte als `abschaetzung_kap3` (überzeichnet die Unsicherheit amtlicher Quotienten) | keine Zahl betroffen; Anzeige „Quelle“ oder „Abschätzung von KAP3“ im Produkt |
| 41 ⚠ | Womit ersetzt das Produkt den Anteil 65+ einer Zelle, der im Zensus-Gitter geheimgehalten ist („–“)? | **zweistufige Ersatzregel, Abschätzung von KAP3** (§3.3, festgelegt vom methodik_manager in T-1199, Stufe 2 neu gefasst in T-1233): Stufe 1 Summe der veröffentlichten 5er-Jahresgruppen ab 65 der Zelle geteilt durch ihre Einwohner, sofern mindestens eine der sechs Gruppen veröffentlicht ist; Stufe 2 der Rest aus der Gemeindesumme: Zielzahl Z = A_G × Einwohnersumme der Gemeinde im Gitter mit A_G = (Einwohner ab 67 + 2/7 der Gruppe 60–66) / Einwohner aus dem Zensus 2022 [69] (fehlt die Gemeindezeile oder steht dort „.“, A_G der Kreiszeile, Befund 119), Rest R = Z − Einwohner ab 65 der Zellen mit veröffentlichtem Anteil − Einwohner ab 65 aus Stufe 1, jede übrige geheimgehaltene Zelle bekommt R / Einwohner dieser Zellen, begrenzt auf 0–100 % (R < 0 gibt 0); gilt auch für Gemeinden ohne Zelle mit veröffentlichtem Anteil (die frühere Modellgrenze, 30 Gemeinden mit 376 Einwohnern, entfällt) | Das „–“ ist Geheimhaltung, nicht null (Befund 104), steht aber meist für Zellen mit wenigen Älteren: Das Altersgitter derselben Zellen zeigt Berlin 2,6 %, Warmsen 5,2 % Personen ab 65. Die frühere Stufe 2 (einwohnergewichteter Anteil der Zellen mit veröffentlichtem Anteil, Warmsen 46,00 %) setzte in Warmsen 1416 Einwohner ab 65 an, mehr als die 990 ab 60 [69] (Befund 117). Der Rest aus der Gemeindesumme hält die amtliche Zahl der Gemeinde: Warmsen 697, Berlin 707.318 Einwohner ab 65, je zwischen „ab 67“ und „ab 60“ aus [69]. Lesart „mindestens eine Gruppe“ in Stufe 1, weil mit „alle sechs Gruppen“ Stufe 1 leer bliebe. **Gegenargumente:** (1) Aufteilung der Gruppe 60–66: [69] trennt bei 67; die 2/7 (Jahrgänge 65 und 66 von sieben, gleich viele Menschen je Jahrgang) sind eine Abschätzung von KAP3; zählt die Gruppe ganz oder gar nicht, liegt der Faktor ohne Gemeindeschlüssel gegen Regel in Warmsen bei × 0,651–0,947, in Berlin bei × 0,927–1,000 (Block `heat.anteil_60_66`). (2) Stichtag: Gitter und [69] zählen zum 15.05.2022, Ebene 1 der Rechenkette zum 31.12.2023 (Befund 99, Wirkung (b) in §3.0); die Regel gleicht die Zellen an den Zensus an, nicht an die Fortschreibung. (3) Ist R < 0, bleibt ein Überhang stehen (1342 Gemeinden, 3,7 % der Einwohner in Zellen der Stufe 2, im Median 5 Einwohner ab 65). (4) 68 Gemeinden ohne Gemeindezeile nehmen den Altersaufbau des Kreises; ohne jede Zeile rechnet nur Hanau (VG250 06415000, in [69] 06435014) wie heute | 65+ = 0 lassen (frühere Produktlogik vor Stufe 1, Historie; unterschätzt Warmsen: 508 gegen 602 ab 67 [69]) · Stufe 2 als einwohnergewichteter Anteil der Zellen mit veröffentlichtem Anteil (Fassung T-1199; verdoppelt ländliche Kommunen, Befund 117) · Gruppe 60–66 ganz oder gar nicht zählen (Spanne oben) | Berlin ohne Gemeindeschlüssel gegen Regel × 0,989, Warmsen × 0,838 (§3.3, `--ersatz`, gemessen 27.09.2026); Code-Nachzug beim cto nach dieser Fassung (Befund 116) |
| 42 ⚠ | Stichtag der Einwohner je Altersband in Ebene 1 der Rechenkette (§3.0)? | **Fortschreibung des Bevölkerungsstandes zum 31.12.2023, Basis Zensus 2022** (Tab. 12411-09-01-4-B [48]; festgelegt vom methodik_manager in T-1233, Befund 99) | Gleicher Stichtag wie der Nenner der Basissterberaten m_a [49] (Sterbefälle 2023 / Bevölkerung 31.12.2023): Einwohner und Sterberate beziehen sich auf denselben Tag. Der Abstand zum Zensus-Gitter (15.05.2022) ist als Wirkung (b) in §3.0 beziffert, in Berlin × 0,981. **Gegenargument:** Gitter und Ersatzregel in §3.3 zählen zum 15.05.2022; ein Sachbearbeiter sieht in §3.0 und §3.3 zwei Stichtage | Zensus-Tabelle 1000A zum 15.05.2022 (Stichtag gleich dem Gitter, aber verschieden vom Nenner von m_a; die Zensus-Datenbank war bis 05.10.2026 in Wartung, nach dem 05.10.2026 wird nicht umgestellt) | keine Zahl betroffen; Kapitel 7 und Kette (362,89 Mio. €) unverändert |
| 43 ⚠ | Wirkung der Schutzprogramme vulnerable Gruppen (`VULNERABLE_GROUP_PROGRAMS`) und ihr Andockpunkt? | **\(\delta_{\text{VG}}\) = 0,931 (Band 0,794–1,0) als Faktor auf den Wochenexzess der Bänder 75–84 und 85+ ohne Heimbewohner; auf die Einweisungen \(\delta_{\text{VG,morb}}\) = 1,0 (Band 0,931–1,069, Befund 131); mit \(\delta_{\text{HAP}}\) zusammen \(\max(\delta_{\text{HAP}} \times \delta_{\text{VG}};\ 0{,}794)\); Abschätzung von KAP3** (§5, Block `heat.delta_vg`, Befunde 123, 125–128, 134) | Der Katalog im Produkt setzt `default_reduction` 0.22 auf Mortalität und Morbidität aller Bänder und beruft sich auf das Gesamtpaket der Hitzeschutzpläne (Urban u. a. 2025 [47], −25,2 %). Das ist der Einführungseffekt des ganzen Pakets über drei Jahrzehnte; ein einzelner Baustein wirkt nicht stärker (für Deutschland ist das Paket −20,6 % [47, Tabelle 1], also Faktor 0,794, und \(\delta_{\text{VG}}\) liegt nie darunter), und er erreicht nur die Gemeldeten (Reichweite 20 %, Wirkung bei Erreichten 0,34 = 24,4 / 97,3 / 0,728 aus [70], Tabellen 1–3, bereinigt um die Sterberate vor dem Sommer und den Anteil ab 90). Heimbewohner ab 85 zählen über S157, nicht hier. Umgerechnet auf den Berlin-Betrag: 0.22 auf alle Bänder ergäbe rund 79,8 Mio. € je Jahr, \(\delta_{\text{VG}}\) ergibt 11,7 Mio. €, rund 15 %. **Kappung (Befund 126):** Ob \(\delta_{\text{HAP}}\) den Baustein schon enthält, lässt sich aus [45] nicht ausschließen; deshalb nehmen beide Hebel zusammen nie mehr weg als das Paket Deutschland (zentral 0,885, keine Kappung; sie greift bei \(\delta_{\text{HAP}}\) = 0,85). **Gegenargument:** Der Paketwert ist gemessen, die Reichweite ist eine Setzung; wer sie auf 40 % hebt, kommt auf 23,3 Mio. €, noch immer weniger als ein Drittel von 79,8 Mio. €; erst mit \(w_{\text{VG}}\) am oberen Bandende 0,68 erreicht er die Kappung bei 34,9 Mio. €. Andockpunkt nicht \(v_{\text{vers},a}\), weil es auf Ebene der Kommune genau 1 ist | 0.22 übernehmen (überzeichnet: Paketwert für einen Baustein, dazu auf Bänder und Morbidität ohne Evidenz); rohe Lesart als Zentralwert, Wirkung bei Erreichten aus dem rohen Unterschied der Anstiege, 0,68 = 0,498 / 0,728 aus [70] Tabelle 2 (Berlin 23,1 Mio. €; verworfen, weil der rohe Unterschied die höhere Altersstruktur der Stadtteile ohne Programm als Wirkung mitzählt und die Quelle selbst auf −24,4 Pp. bereinigt; bleibt als obere Grenze des Bands); Hebel streichen (P2 verbietet eine unbegründete Nullwirkung; die Maßnahme besteht im Produkt) | Kette 362,9 Mio. € unverändert (Hebel wirkt nur bei Wahl der Maßnahme); Abweichung Bericht ↔ Katalog (0.22 ↔ 0,931 auf 75+ ohne Heimbewohner, Kappung mit \(\delta_{\text{HAP}}\)) geht als Punkt in die Meldung an den cto (eiserne Regel 5) |
| 44 ⚠ | Wie steht der Hebel S157 zur geparkten Maßnahme `COOLING_ROOMS_DRINKING_WATER`? | (**Stand 26.09.2026, Historie; fortgeschrieben durch Nr. 45 und 46:** seit T-1367-cto ist die Maßnahme aktiv, \(s_{\text{gek}}\) hat die Voreinstellung 0,11, die Kühlzentren haben einen eigenen Hebel \(\delta_{\text{KZ}}\).) **Die Maßnahme bleibt im Produkt geparkt und hat heute keine Wirkung, auch keine Nullwirkung. Beim Aktivieren gilt \(g_{\text{S157}}\) = 0,29 (Band 0–0,90) auf den Heim-Exzess 85+ im gekühlten Anteil \(s_{\text{gek}}\), den die Kommune eingibt; Abschätzung von KAP3** (§5, Befund 130) | Der geparkte Katalog (`backend/app/data/catalog_parked.py`) führt die Maßnahme mit `default_reduction` 0.18 auf die Exposition (`effect_target: exposure`) für alle Menschen. [46] misst dagegen Klimaanlagen in Heimen: Mit ihnen bleiben 29 % des Heim-Exzesses (Faktor 0,29), 71 % fallen weg, und zwar nur bei Heimbewohnern ab 85 im gekühlten Anteil. 0.18 auf die Exposition ist also weder dieselbe Größe noch derselbe Personenkreis; wie groß ihre Wirkung in Euro wäre, hängt an der Expositionskette des Produkts und ist mit den 25,0 Mio. € für Berlin nicht vergleichbar. Wie viele Heimplätze gekühlt sind, weiß nur die Kommune, deshalb ist \(s_{\text{gek}}\) ihre Eingabe. Öffentliche Kühlzentren außerhalb der Heime bekommen beim Aktivieren eine eigene Abschätzung nach P2. **Gegenargument:** 0.18 wirkt auf alle Menschen und erfasst damit auch öffentliche Kühlzentren, die der Bericht heute nicht rechnet; wer sie ersetzt, verliert diesen Teil, bis die eigene Abschätzung vorliegt. Weil die Maßnahme geparkt ist, fehlt dadurch heute keiner Kommune eine Wirkung | 0.18 auf die Exposition übernehmen (ohne Beleg aus [46], anderer Personenkreis); S157 ohne Andockpunkt führen (die geparkte Maßnahme ist die einzige passende im Produkt) | Kette 362,9 Mio. € und S157 25,0 Mio. € unverändert; Empfehlung an den cto in der Meldung: beim Aktivieren von `COOLING_ROOMS_DRINKING_WATER` \(g_{\text{S157}}\) auf \(D_{85+} \times h_{\text{Heim}} \times s_{\text{gek}}\) statt 0.18 auf die Exposition (eiserne Regel 5) |
| 45 ⚠ | Was gilt für S157, wenn die Kommune keinen gekühlten Anteil eingibt, wie rechnet \(h_{\text{Heim}}\) in der Zelle, und mit welcher Wirkung zählt S157 im Anpassungspotenzial? | **Voreinstellung \(s_{\text{gek}}\) = 0,11 (Band 0,05–0,15) für die ganze Kommune, Abschätzung von KAP3** (Block `heat.s_gek`, Befund 138); **\(h_{\text{Heim},z} = q_{\text{pfl},z}\,[1 + \beta_{\text{pfl}}(1 - \bar q_{\text{pfl}})] / [1 + \beta_{\text{pfl}}(q_{\text{pfl},z} - \bar q_{\text{pfl}})]\) je Zelle, Rückfallwert 0,344** (Block `heat.h_heim`, Befund 146); **\(r_{\text{S157}} = a_{85+} \times h_{\text{Heim}} \times s_{\text{gek}} \times (1 - g_{\text{S157}})\) = 0,284 × 0,344 × 0,11 × 0,706 = 0,0076 im Anpassungspotenzial** (Befund 149; §5) | Eine Nullwirkung ist keine Voreinstellung (P2, A-0010): Ohne Eingabe zeigte S157 keinen Betrag und zählte im Anpassungspotenzial mit 0. 11 % der Pflegeheime haben eine Klimaanlage [71]; 14,5 % der Neubauten des Sozialwesens 2025 haben eine Anlage zur Kühlung [72]; den älteren Bestand setzt KAP3 nicht höher an. Welche Heime gekühlt sind, weiß nur die Kommune, deshalb gilt der Wert für ihre ganze Fläche. Das Produkt führt \(q_{\text{pfl}}\) je Zelle (Log 35); mit derselben Formel wie \(v_{\text{vers}}\) liegen die Heim-Todesfälle in den Zellen der Heime, summiert über die Kommune bleibt es 0,344 × \(D_{85+}\). **Gegenargumente:** (1) Die Umfrage [71] hat 140 Rückmeldungen und ist nicht repräsentativ; „Klimaanlage in der Einrichtung“ heißt nicht, dass alle Plätze gekühlt sind (deshalb unten 0,05). (2) \(a_{85+}\) stammt aus der Rechenkette Berlin (0,284); in Warmsen ist er 0,224, das Anpassungspotenzial dann 0,056 statt 0,057 | Nullwirkung behalten (S157 ohne Eingabe ohne Betrag; verstößt gegen P2) · 0,145 aus [72] als Zentralwert (Neubauten, überzeichnet den Bestand) · 0,344 in jeder Zelle (verteilt Heim-Todesfälle auf Zellen ohne Heim) · S157 mit \(1 - g_{\text{S157}}\) = 0,71 im Anpassungspotenzial (zählte den Heim-Exzess aller Heime als ganze Hitzemortalität, 0,71 / 0,0076 = rund 90-mal zu groß) | Kette 362,9 Mio. € unverändert; S157 Berlin (Kette) bei der Voreinstellung 2,7 Mio. € je Jahr (Preisstand 2024; Band 1,2–3,7 Mio. €), alle Heime gekühlt weiter 25,0 Mio. €; Warmsen (Zelllauf) 1.032 € je Jahr; Anpassungspotenzial der Hitzemortalität 0,057 statt 0,050; Umsetzung beim cto (eiserne Regel 5) |
| 46 ⚠ | Welche Wirkung haben öffentliche Kühlzentren außerhalb der Heime (Log 44, Zusage einer eigenen Abschätzung nach P2)? | **\(\delta_{\text{KZ}}\) = 1 − \(r_{\text{KZ}} \times w_{\text{KZ}}\) = 1 − 0,05 × 0,71 × 3/24 = 0,9956 (Band 0,982–0,9994) als Faktor auf den Wochenexzess der Bänder 75–84 und 85+ ohne Heimbewohner; mit \(\delta_{\text{HAP}}\) und \(\delta_{\text{VG}}\) zusammen \(\max(\delta_{\text{HAP}} \times \delta_{\text{VG}} \times \delta_{\text{KZ}};\ 0{,}794)\); Abschätzung von KAP3** (§5, Block `heat.delta_kuehlzentren`, Befunde 139, 148) | Eine Effektgröße für Kühlzentren hat KAP3 nicht gefunden (Suche 27.09.2026). Die Wirkung im gekühlten Raum ist gemessen (Klimaanlage in Heimen: 71 % des Exzesses fallen weg [46]), ebenso wie lange eine Kühlpause wirkt (2 h Kühlung wirken etwa 1 h nach [73]); daraus 0,71 × 3/24 = 0,089 für Nutzer. Die Reichweite ist eine Setzung: ein Viertel der Reichweite eines Schutzprogramms, weil nur hingeht, wer in der Hitze das Haus verlässt, und gerade die Gefährdetsten das nicht tun [41]. Plausibel gegen [41]: Besuch kühler Orte OR 0,34, nach Log 10 fünf- bis zehnfach überschätzt, also 0,066–0,132 für Nutzer. **Gegenargumente:** (1) Die Reichweite 5 % ist nicht gemessen; sie ist der stärkste Treiber (Berlin 0,15–1,50 Mio. € über 1–10 %). (2) Das Labor [73] misst die Körpertemperatur, nicht die Sterblichkeit. (3) Jüngere Nutzer zählen nicht (Untergrenze) | Nullwirkung (verstößt gegen P2) · Faktor aus [46] ohne die Stunden (0,71 für Nutzer; Berlin 6,0 statt 0,75 Mio. €, ein Besuch wirkte wie eine Klimaanlage rund um die Uhr) · Odds Ratio 0,34 aus [41] unmittelbar (Fall-Kontroll-Wert, Log 10) | Kette 362,9 Mio. € unverändert (Hebel wirkt nur bei Wahl der Maßnahme); Berlin (Kette) 0,75 Mio. € je Jahr (Preisstand 2024; Band 0,1–3,0 Mio. €), Warmsen (Zelllauf) 320 €; Andockpunkt `COOLING_ROOMS_DRINKING_WATER`, Umsetzung beim cto (eiserne Regel 5) |
| 47 ⚠ | Was gilt beim Doppelzählungs-Wächter der Schutzprogramme (und der Kühlzentren), bis die Kommune angibt, ob das Programm schon in den Kalibrierjahren lief? | **Eingabe ja/nein je Maßnahme, Voreinstellung „nein“, Abschätzung von KAP3** (Block `heat.vg_in_kalibrierjahren`, Befund 150; §5); bei „ja“ gilt \(\delta_{\text{VG}}\) = \(\delta_{\text{VG,morb}}\) = 1 bzw. \(\delta_{\text{KZ}}\) = 1 | Ein Programm, das schon 2012–2024 lief, ist keine zusätzliche Maßnahme; seine Wirkung gehört zum Anpassungsstand des Basiswerts (Kapitel 1 (a)). Solche Programme waren selten: 18 veröffentlichte kommunale Hitzeaktionspläne bundesweit am 10.06.2024, in Nordrhein-Westfalen 4 von 53 Kreisen und kreisfreien Städten im Oktober 2023, also 7,5 % [76]. Auf Berliner Größe ist der erwartete Fehler mit „nein“ höchstens 7,5 % × 11,7 = 0,9 Mio. €, mit „ja“ mindestens 92,5 % × 11,7 = 10,8 Mio. €. **Gegenargument:** Die Zahlen stammen vom Ende des Kalibrierfensters und aus einem Land und zählen Pläne, nicht einzelne Programme; ein älteres Hitzetelefon ohne Plan fehlt darin. Eine Kommune, die es hatte und nicht antwortet, zählt seine Wirkung doppelt | Voreinstellung „ja“ (jede Kommune ohne Antwort ohne Wirkung der Schutzprogramme, Berlin 0 statt 11,7 Mio. € je Jahr; Unterschätzung für mehr als 90 % der Kommunen und Nullwirkung gegen P2) · keine Eingabe, Wächter nur als Text (Stand bis T-1538; das Produkt kann ihn nicht anwenden) | Kette 362,9 Mio. € und Schutzprogramme Berlin 11,7 Mio. € je Jahr unverändert (Voreinstellung „nein“ rechnet wie bisher); Umsetzung beim cto (eiserne Regel 5) |
| 48 ⚠ | Ist die Kappung 0,794 ein eigener Parameter oder nur das Band von \(\delta_{\text{VG}}\)? | **eigener Block `heat.kappung_vg`: 0,794 (Band 0,743–0,842), Abschätzung von KAP3** (Befund 151; §5) | Ein Wert, der den Betrag begrenzt, ist ein Parameter mit Herleitung (P1). 0,794 = 1 − 0,206 aus [47], Tabelle 1 (Deutschland, 15,8–25,7 %); `abschaetzung_kap3`, weil der Paketwert aller Altersgruppen für die Hebel auf den Bändern ab 75 ohne Heim steht (Log 40). Er ist zugleich das untere Bandende von \(\delta_{\text{VG}}\) (ohne Kappung 0,728) und greift bei \(\delta_{\text{HAP}}\) = 0,85 (0,791) und bei Reichweite und Wirkung am oberen Ende. **Gegenargument:** Der Wert ist ein Zentralwert mit Intervall; eine feste Kappung verschiebt den Betrag dort, wo sie greift, über ihr Band um 26,8–43,6 Mio. € | nur im Band von \(\delta_{\text{VG}}\) führen (Grenze ohne eigenen Block, P1 verletzt) · Quellenwert `quelle` (verdeckt, dass der Paketwert für eine andere Größe steht) · ohne Kappung (Berlin am oberen Ende 46,1 statt 34,9 Mio. €) | keine Zahl betroffen; Kette 362,9 Mio. € unverändert; Umsetzung beim cto (Konstante `VG_PAKET_DE` wird Registry-Parameter) |
| 49 ⚠ | Welches Band tragen \(f_a\) und \(\bar L_a\), und wie stark verschieben sie den Betrag? | **\(f_a\): Rückrechnung mit den Altersanteilen der Sommer 2025 [74] und 2026 [75], 0,156–0,562 / 0,341–0,753 / 0,588–0,659 / 1,0; \(\bar L_a\): Stützstelle bis sterbefallgewichteter Wert, 23,39–28,64 / 15,31–15,59 / 8,54–8,90 / 4,16–4,20 J; beides Abschätzung von KAP3** (Befund 152; §3.3a, §3.5, §5) | Beide Blöcke hatten kein Band (\(\bar L_a\) nur für 85+). Die Altersanteile schwanken von Sommer zu Sommer; die Sterbefälle je Altersjahr [49] und die Sterbetafel [48] erlauben für alle Bänder denselben Rechenweg wie für 85+. Berlin (Kette): \(f_a\) 310,2–402,9 Mio. € mit neu gefittetem \(c_{\text{kal}}\) (0,651 und 0,534), \(\bar L_a\) 357,3–381,1 Mio. €. **Gegenargument:** Zwei Sommer sind keine Verteilung; die RKI-Zahlen sind laufende, gerundete Schätzungen. Die sterbefallgewichteten \(\bar L_a\) liegen für 65–74 und 75–84 unter den Stützstellen; der zutreffende Wert liegt dort am unteren Bandende | \(f_a\) tauschen und \(c_{\text{kal}}\) festhalten (277,0–438,3 Mio. €, fast doppelt so weit; die Zahl der Hitzetoten passte nicht mehr zur RKI-Reihe) · Band aus der Toleranz der Altersvalidierung ± 5 Pp. (nicht gemessen) | keine Zahl betroffen; Kette 362,9 Mio. € unverändert; Blöcke `heat.f_alter` und `heat.l_restlebenserwartung` tragen die Bänder |
