# Methodik-Bericht #95 — Hitzebelastung

Status: **Rev. 8, Fortschreibung 7 — ABNAHMEREIF** (A-0048; Null-Runde der Gegenprüfung in
Ledger-Runde 23; Abnahme durch den methodik_manager steht aus) · 26.09.2026 · Rev. 8 vom 30.08.2026
(§3.4-Ressourcen-Regel, q_pfl-Ebene angelegt, q_1P geparkt, L̄_85+ exakt 4,16 J; Befunde 86–94 behoben) hat
Fortschreibung 7 in den Ledger-Runden 10–22 um die Rechenkette 3.0, den Pflichtabschnitt „Risiko ohne (weitere)
Anpassung“, die Kennzeichnung der Parameter, die Ersatzregel für den Anteil 65+ und den Berlin-Anker ergänzt; im
Produkt stehen die Ersatzregel (Befund 116) und die Kennzeichnung der Parameter noch aus ·
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
| S152 | Altersstruktur | Schicht B | \(\text{pop}_a\), \(f_a\), \(m_a\); Isolationsanteil \(q_{\text{1P}}\) | — |
| S153 | Vorerkrankungen / individuelle Sensitivität | Schicht B (teilweise) | Pflegeheim-Term \(\beta_{\text{pfl}}\) (nur Band 85+) | Kreis-Prävalenzen (Zi/GEDA) und GISD-Deprivation: Sensitivitätsband (Log Nr. 14) |
| S154 | Freizeitverhalten | bewusst inaktiv | — | exertional heat illness (junge Erwachsene) überwiegend ambulant; dokumentiert, nicht modelliert (Log Nr. 15) |
| S155 | Gefahrenbewusstsein | Maßnahmen-Hebel | \(\delta_{\text{HAP}}\)-Kette (mit S158) | — |
| S157 | Verfügbarkeit gekühlter Aufenthaltsräume | Maßnahmen-Hebel | Klimaanlagen-Effekt rOR ≈ 0,93 [46]; R7-Weiche §5 | — |
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
Pflegeheimen am \(\beta_{\text{pfl}}\)-Term und Schutzprogramme für vulnerable Gruppen über
\(v_{\text{vers},a}\). Im Produkt entsteht daraus der Wert „mit Anpassung" erst, wenn eine Kommune
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
| 95-S157-01 | S157 gekühlte Räume → Mortalität (Heime) | rOR ≈ 0,93 an Extremhitzetagen | Case-Crossover (Ontario, 73.578 Todesfälle) | [46] | Ontario 2010–2023 | Heim-Ebene | **Maßnahmen-Hebel** (R7-Weiche §5) | Log 10 |
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
  7 %.** Das Produkt rechnet jede 100-m-Zelle mit ihrer eigenen Temperatur (§3.1) und ihrer
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
  (c) **Altersbänder je Zelle wie im Produkt: × 0,982 = 0,9867 × 0,9948.** Der erste Faktor,
  Produkt gegen Regel, ist eine Eigenheit des Produkts: In 4.774 Zellen mit 99.098 Einwohnern ist
  der Anteil 65+ im Gitter geheimgehalten („–“), und das Produkt setzt dort 65+ = 0 (Befund 104).
  Gemessen ist er gegen die Ersatzregel aus §3.3 (Stufe 1 und 2, ohne (d)); gerundet ist es
  derselbe Faktor wie dort in der Tabelle (× 0,987, dort mit (d); Befund 121). Der zweite Faktor,
  der Rest, ist das, was die Altersbänder je Zelle nach dieser Regel gegenüber (b) ändern: wie
  alt die Einwohner im Gitter sind und in welchen Zellen die Älteren wohnen; er senkt den Betrag
  um 0,5 %.
  (d) **Wärmeinsel-Feinstruktur unter 1 km: × 1,021.** Modellrechnung mit derselben gesetzten
  Streuung σ = 0,5 K wie in §4, keine Messung; die gekrümmte Kurve hebt die Summe.
  Zusammen 0,948 × 0,981 × 0,982 × 1,021 = 0,932: Der Zelllauf ergibt für Berlin
  rund 338 Mio. € je Jahr (Preisstand 2024), 7 % weniger als die Kette; ohne die Eigenheit aus
  (c), also mit der Ersatzregel, wären es rund 343 Mio. € (342,67 Mio. €, Tabelle in §3.3). Die
  Kette zeigt den Rechenweg, der Betrag für Berlin ist der Zelllauf des Produkts. Die Wirkungen
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
assert abs(0.9867 * 0.9948 - 0.982) < 0.0005             # (c) = Produkt gegen Regel 3.3 x Rest (Befund 121)
gesamt = 0.948 * 0.981 * 0.982 * 1.021                   # Skript anlagen/95_zellvergleich.py
assert abs(gesamt - 0.932) < 0.001
assert abs((eur_mort + eur_morb) / 1e6 * gesamt - 338) < 1
assert abs((eur_mort + eur_morb) / 1e6 * gesamt / 0.9867 - 343) < 1  # mit Regel 3.3: 342,67
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
`backend/data/kalibrierung/wochenquantile_region.csv` [33,50].

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
Aufteilung des Gebiets). Heute setzt das Produkt 65+ = 0, wo der Anteil 65+ im Gitter
geheimgehalten ist („–“).
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
   Jahrgang voraus und ist eine Abschätzung von KAP3. Fehlt die Gemeinde in [69] (anderer
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
Option `--ersatz` jede Kommune zweimal, nach heutiger Produktlogik und mit der Regel, beide Male
wie der Zelllauf in §3.0 (Wirkungen (a)–(d)). Derselbe Aufruf gibt auch die Spanne aus, wenn die
Gruppe 60–66 gar nicht (0/7) oder ganz (7/7) zu den Menschen ab 65 zählt:

| Beispielkommune | Aufruf | Einwohner (Zensus-Gitter) | davon in Zellen mit geheimgehaltenem Anteil 65+ | Einwohner ab 65 heute | Einwohner ab 65 mit Regel | Jahresbetrag heute | Jahresbetrag mit Regel | Faktor heute gegen Regel | Spanne des Faktors (60–66 ganz oder gar nicht) |
|---|---|---|---|---|---|---|---|---|---|
| Berlin (AGS 11000000) | `python3 docs/methodik/anlagen/95_zellvergleich.py --gemeinde 11000000 --ersatz` | 3.593.357 | 2,8 % | 694.397 | 707.318 | 338,10 Mio. € | 342,67 Mio. € | × 0,987 | × 0,925–0,998 |
| Warmsen, Landkreis Nienburg (Weser) (AGS 03256034) | `python3 docs/methodik/anlagen/95_zellvergleich.py --gemeinde 03256034 --ersatz` | 3087 | 64,2 % | 508 | 697 | 138.543 € | 173.099 € | × 0,800 | × 0,622–0,904 |

Beträge je Jahr (Preisstand 2024). Warmsen zählt nach dem Zensus 2022 amtlich 3158 Einwohner
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

*Was eine einfachere Rechnung verfälschen würde.* Ließe das Produkt 65+ = 0 stehen (heutige
Produktlogik), zählte Warmsen 508 Einwohner ab 65, weniger als die 602 ab 67 allein, und der Betrag
läge um 20 % zu niedrig (Faktor × 0,800). Die Aufteilung der Gruppe 60–66 ist die größte
Unsicherheit der Regel: Zählt die ganze Gruppe oder gar nichts davon, liegt der Faktor in Warmsen
bei × 0,622–0,904, in Berlin bei × 0,925–0,998 (Tabelle oben). In jeder Lesart liegt der Betrag mit
Regel über dem heutigen; die Richtung der Korrektur hängt an der Aufteilung nicht.

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
  **1,21…2,66**/100.000·Jahr. (3) Summe: 1,68 + 1,21…2,67 ⇒ **3,5 (2,9–4,4)
  je 100.000·Jahr** [16,18,62]. Altersaufteilung:
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
assert abs(1.68 + u - 2.9) < 0.05 and abs(1.68 + o - 4.4) < 0.1
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
Einkommensentwicklung ^0,85 ×1,1719 ⇒ **160.800 €₂₀₂₄** (Preisstand-Label korrigiert,
Befund 10: alle Indexendpunkte sind 2024). **Band** (Befund 10, definiert): Untergrenze
136,4 T€ (ohne Raumtransfer: 79.500 × 1,4638 × 1,1719); Obergrenze **165,6 T€**
(Raumtransfer ohne Elastizität: 79.500 × 1,4638 × 1,2140 × 1,1719) — der Rev.-5-Wert
169,5 T€ reproduzierte mit keiner Faktorkombination und ist ersetzt. VSL nur Sensitivität:
6,19 Mio. €₂₀₂₄ (MK-konsistent; ÷ VOLY = 38,5 LJ, Konsistenz-Check ✓), 4,7 Mio. €₂₀₂₄
(EU-Referenz) und 3,5 Mio. € (Nutzer-Setzung der Arbeitsmappe vor Fortschreibung, Befund 50).
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

### 3.6 Zeichentabelle (alphabetisch; §3.2-Form)

| Zeichen | Name | Einheit | Wert / Herkunft |
|---|---|---|---|
| \(a\) | Altersband u65 · 65–74 · 75–84 · 85+ | — | Zensus-Altersbänder |
| \(c_{\text{Fall}}\) | Behandlungskostensatz je Fall (**Proxy**: Ø aller KH-Fälle) | €₂₀₂₄ | 7.152 = 6.996 €₂₀₂₃ × 119,3/116,7 [17,19]; register:95-E02-02 |
| \(c_{\text{kal}}\) | Kalibrierfaktor, **ein nationaler Skalar** (§3.4; Herleitung §4) — Fit auf bevölkerungsgewichteten Reihen, keine Pauschalkorrektur | — | **0,581** (Fenster 2012–2024, in-sample; Sensitivitäten: ohne Süd-Nachschätzung 0,661, Vollreihe 0,660, inkl. vorl. 2025 0,651, Voll-Holdout 0,567 → Prüfstein ebenfalls 12/16); herleitung:#c-kal, #t-povw [50] |
| \(D_a\) | hitzebedingte Todesfälle der Zelle im Band \(a\) (Teil-Ausweis) | 1/Jahr | berechnet |
| \(e_{\text{HD}}\) | rel. Mehr-Einweisungen je Hitzetag (> 30 °C), **konditional** | 1/Tag | 0,024 (Band 0,024–0,061; unkond. 0,054), K&Z Tab. 1 [18,62]; register:95-E02-02; Log 19 |
| \(f_a\) | Altersfaktor der RR-Steigung rel. zu 85+ | — | 0,357 / 0,588 / 0,631 / 1,0 — Rückrechnung §3.3a (lineare Näherung, gekennzeichnet); herleitung:#f-a |
| \(F_{\text{Zelle}}\) | hitzeassoziierte Erkrankungsfälle (Teil-Ausweis) | 1/Jahr | Ergebnis |
| \(\text{HD},\ \text{HD}_{\text{ref}}\) | Hitzetage der Zelle (DWD-CDC hot_days 1 km, ohne UHI — §3.4) / Referenz = K&Z-Basisperiode | Tage/Jahr | HD: DWD-CDC [33]; \(\text{HD}_{\text{ref}}\) = **7,2** (Ø 1999–2008 [18]); herleitung:#hd-ref |
| \(\bar L_a\) | Restlebenserwartung je Band (Sterbetafel 2022/2024; u65–75–84 Stützstellen e(60)/e(70)/e(80); **85+ exakt sterbefallgewichtet, Rev. 8**) | Jahre | 23,39 / 15,59 / 8,90 / **4,16** (85+-Band [4,16, 4,20]; Anlage l85_sterbefallgewichtung.csv) [48,49]; herleitung:#l-a |
| \(m_a\) | Basissterberate je Band (Sterbefälle 2023 ÷ Bev. 31.12.2023) | 1/100.000·a | 213,2 / 1.737,9 / 4.812,3 / 14.800,2 [49]; herleitung:#m-a |
| \(\text{pop}_a\) | Bevölkerung der Zelle je Band | Personen | Zensus 2022, 100 m; register:95-R35-01 |
| \(q_{\text{1P}},\ \bar q_{\text{1P}}\) | Anteil allein lebender 65+ der Zelle / Bundesmittel | — | Zelle: Zensus-2022-Haushaltsgitter (Fallback s. u.); \(\bar q\) = **0,346** (Mikrozensus 2023 [63]); Zensus-Gitterwert ersetzt bei Integration; herleitung:#qbar-1p |
| \(q_{\text{pfl}},\ \bar q_{\text{pfl}}\) | Heimbewohner-Anteil an der 85+-Bevölkerung / Bundesmittel | — | OSM × Pflegestatistik 2023 (**Proxy**, Fallback s. u.); \(\bar q\) = 424.300/2.844.213 = **0,149** [61]; herleitung:#qbar-pfl |
| \(q_{w,\text{Region}}\) | empirisches Anomalie-Quantil der Sommerwoche | K | Tabelle §3.2; wochenquantile_region.csv [33,50] |
| \(r_{0,a}\) | Baseline-Einweisungsrate je Band | 1/100.000·a | 1,9 / 6,3 / 10,8 / 15,6 (= 1:3,3:5,7:8,2; Summe 3,54; Band ×0,6–1,6 = Summen-Band 2,9–4,4 [×0,83–1,26] kombiniert mit Altersprofil-Unsicherheit ±25 % [Option-B-Profil §3.4] ⇒ ≈ ×0,6–1,6) — Herleitung §3.4, Altersprofil gekennzeichnete Abschätzung [16,18,62]; herleitung:#r0-a |
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
  Fälle [42]) würde doppelt buchen.
- **Gekühlte Räume / Klimaanlagen in Pflegeheimen (S157):** rOR ≈ 0,93 an Extremhitzetagen
  (Ontario [46]), Andockpunkt am \(\beta_{\text{pfl}}\)-Term (nur 85+-Band). **R7-Weiche**
  (Befund 53): Die Wirkung gilt nur für den gekühlten Bestandsanteil; je Einheit gilt
  Entweder-oder gemäß R7 („100-%-Regel je Raumbestand", Weiche des Treibers #63) — ab
  Stufe M5 bucht #65 die Kühl-Mehrkosten (K8), der Übergabepunkt ist dort zu referenzieren;
  keine Doppelbuchung „vermiedener Schaden + Vorsorgekosten".
- **Schutzprogramme vulnerable Gruppen (S157):** Schwellen-/Expositionswirkung für die
  75+/85+-Bänder über die \(v_{\text{vers},a}\)-Faktoren (Befund 45: die frühere Größe
  „v_access" existiert seit Rev. 3 nicht mehr; Formulierung bereinigt).

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
  band: null
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
  band: {85+: [4.16, 4.20]}   # Rev. 8 exakt sterbefallgewichtet; Obergrenze: e(95)-Stuetzstelle statt e-quer(95+)
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
  kennzeichnung: berechnet   # (OR-1)/[1+q(OR-1)] mit OR 2,3 aus Semenza 1996 [40] (§3.3)
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
- **[15]** UBA (Hrsg.), KWRA 2021, Teilbericht 5 (CC 26/2021), Kap. 4.2, umweltbundesamt.de
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
  Standard Inputs (VSL 4,7 Mio. €₂₀₂₄).
- **[33]** DWD Climate Data Center (CDC): Raster air_temperature_mean, hot_days;
  Gebietsmittel; Tageswerte 21 Stationen.
- **[38]** J. Nicholl u. a., Emerg Med J 24:665–668, 2007. doi:10.1136/emj.2007.047654 (+≈1 %/10 km).
- **[39]** M. P. Larsen u. a., Ann Emerg Med 22:1652–1658, 1993. doi:10.1016/S0196-0644(05)81302-2;
  T. D. Valenzuela u. a., Circulation 96:3308–3313, 1997. doi:10.1161/01.CIR.96.10.3308 (Hilfsfrist-Pfad).
- **[40]** J. C. Semenza u. a., N Engl J Med 335:84–90, 1996. doi:10.1056/NEJM199607113350203
  (OR ≈ 2,3 allein lebend).
- **[41]** A. Bouchama u. a., Arch Intern Med 167:2170–2176, 2007. doi:10.1001/archinte.167.20.ira70009
  (Meta; Bettlägerigkeit 6,44).
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
  am Volltext belegten Zitat und steht nicht in der Studie).
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
Altersband in Ebene 1 (T-1233, Befunde 99 und 120).
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
| 40 ⚠ | Kennzeichnung der Grenzfälle in Kapitel 7? | **`abschaetzung_kap3`**, sobald eine Setzung von KAP3 im Wert steckt (\(\beta_{85+}\) Süd-Nachschätzung, \(f_a\) lineare Näherung, VOLY-Elastizität beim Raumtransfer, \(c_{\text{Fall}}\) als Proxy aus dem Durchschnitt aller Krankenhausfälle, Stützstellen e(60)/e(70)/e(80) für die Bänder u65, 65–74 und 75–84 in \(\bar L_a\), \(r_{0,a}\)-Altersprofil, \(\delta_{\text{HAP}}\), Distanzterm); **`quelle`** für reine Rechnungen aus amtlichen oder gemessenen Zahlen ohne Setzung (Quotienten, ausgezählte Quantile); Prüfstein: Misst der Wert die Zielgröße selbst, ist die bloße Wahl zwischen Quellenwerten keine Setzung (\(e_{\text{HD}}\) konditional statt unkonditional, Log 19; Stationsauswahl für \(q_w\), Log 5) — steht er für eine andere Größe (Proxy) oder nähert er ein Bandmittel durch einen Punkt an, ist es eine; **`berechnet`** nur, wo der Wert aus anderen Blöcken folgt (\(c_{\text{kal}}\), \(\beta_{\text{iso}}\), \(\beta_{\text{pfl}}\)) | Die Parameterliste im Produkt (P1) soll eine Setzung nie als Quellenwert zeigen; gleiche Lesart wie die Blöcke in `60_*.md` („Quotient zweier amtlicher Summen“ = `quelle`) | alle aus Quellen abgeleiteten Werte als `abschaetzung_kap3` (überzeichnet die Unsicherheit amtlicher Quotienten) | keine Zahl betroffen; Anzeige „Quelle“ oder „Abschätzung von KAP3“ im Produkt |
| 41 ⚠ | Womit ersetzt das Produkt den Anteil 65+ einer Zelle, der im Zensus-Gitter geheimgehalten ist („–“)? | **zweistufige Ersatzregel, Abschätzung von KAP3** (§3.3, festgelegt vom methodik_manager in T-1199, Stufe 2 neu gefasst in T-1233): Stufe 1 Summe der veröffentlichten 5er-Jahresgruppen ab 65 der Zelle geteilt durch ihre Einwohner, sofern mindestens eine der sechs Gruppen veröffentlicht ist; Stufe 2 der Rest aus der Gemeindesumme: Zielzahl Z = A_G × Einwohnersumme der Gemeinde im Gitter mit A_G = (Einwohner ab 67 + 2/7 der Gruppe 60–66) / Einwohner aus dem Zensus 2022 [69] (fehlt die Gemeindezeile oder steht dort „.“, A_G der Kreiszeile, Befund 119), Rest R = Z − Einwohner ab 65 der Zellen mit veröffentlichtem Anteil − Einwohner ab 65 aus Stufe 1, jede übrige geheimgehaltene Zelle bekommt R / Einwohner dieser Zellen, begrenzt auf 0–100 % (R < 0 gibt 0); gilt auch für Gemeinden ohne Zelle mit veröffentlichtem Anteil (die frühere Modellgrenze, 30 Gemeinden mit 376 Einwohnern, entfällt) | Das „–“ ist Geheimhaltung, nicht null (Befund 104), steht aber meist für Zellen mit wenigen Älteren: Das Altersgitter derselben Zellen zeigt Berlin 2,6 %, Warmsen 5,2 % Personen ab 65. Die frühere Stufe 2 (einwohnergewichteter Anteil der Zellen mit veröffentlichtem Anteil, Warmsen 46,00 %) setzte in Warmsen 1416 Einwohner ab 65 an, mehr als die 990 ab 60 [69] (Befund 117). Der Rest aus der Gemeindesumme hält die amtliche Zahl der Gemeinde: Warmsen 697, Berlin 707.318 Einwohner ab 65, je zwischen „ab 67“ und „ab 60“ aus [69]. Lesart „mindestens eine Gruppe“ in Stufe 1, weil mit „alle sechs Gruppen“ Stufe 1 leer bliebe. **Gegenargumente:** (1) Aufteilung der Gruppe 60–66: [69] trennt bei 67; die 2/7 (Jahrgänge 65 und 66 von sieben, gleich viele Menschen je Jahrgang) sind eine Abschätzung von KAP3; zählt die Gruppe ganz oder gar nicht, liegt der Faktor heute gegen Regel in Warmsen bei × 0,622–0,904, in Berlin bei × 0,925–0,998. (2) Stichtag: Gitter und [69] zählen zum 15.05.2022, Ebene 1 der Rechenkette zum 31.12.2023 (Befund 99, Wirkung (b) in §3.0); die Regel gleicht die Zellen an den Zensus an, nicht an die Fortschreibung. (3) Ist R < 0, bleibt ein Überhang stehen (1342 Gemeinden, 3,7 % der Einwohner in Zellen der Stufe 2, im Median 5 Einwohner ab 65). (4) 68 Gemeinden ohne Gemeindezeile nehmen den Altersaufbau des Kreises; ohne jede Zeile rechnet nur Hanau (VG250 06415000, in [69] 06435014) wie heute | 65+ = 0 lassen (heutige Produktlogik; unterschätzt Warmsen: 508 gegen 602 ab 67 [69]) · Stufe 2 als einwohnergewichteter Anteil der Zellen mit veröffentlichtem Anteil (Fassung T-1199; verdoppelt ländliche Kommunen, Befund 117) · Gruppe 60–66 ganz oder gar nicht zählen (Spanne oben) | Berlin heute gegen Regel × 0,987, Warmsen × 0,800 (§3.3, `--ersatz`); Code-Nachzug beim cto nach dieser Fassung (Befund 116) |
| 42 ⚠ | Stichtag der Einwohner je Altersband in Ebene 1 der Rechenkette (§3.0)? | **Fortschreibung des Bevölkerungsstandes zum 31.12.2023, Basis Zensus 2022** (Tab. 12411-09-01-4-B [48]; festgelegt vom methodik_manager in T-1233, Befund 99) | Gleicher Stichtag wie der Nenner der Basissterberaten m_a [49] (Sterbefälle 2023 / Bevölkerung 31.12.2023): Einwohner und Sterberate beziehen sich auf denselben Tag. Der Abstand zum Zensus-Gitter (15.05.2022) ist als Wirkung (b) in §3.0 beziffert, in Berlin × 0,981. **Gegenargument:** Gitter und Ersatzregel in §3.3 zählen zum 15.05.2022; ein Sachbearbeiter sieht in §3.0 und §3.3 zwei Stichtage | Zensus-Tabelle 1000A zum 15.05.2022 (Stichtag gleich dem Gitter, aber verschieden vom Nenner von m_a; die Zensus-Datenbank war bis 05.10.2026 in Wartung, nach dem 05.10.2026 wird nicht umgestellt) | keine Zahl betroffen; Kapitel 7 und Kette (362,89 Mio. €) unverändert |
