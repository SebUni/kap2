# Methodik-Bericht #96 — Allergische Reaktionen durch Aeroallergene pflanzlicher Herkunft

Status: **Rev. 4 (26.09.2026, Fortschreibung 7 der Aufgabe für M0, A-0048),
ABGENOMMEN durch den methodik_manager am 30.09.2026;
abgeglichen mit der Übernahme Ü-1 bis Ü-13 am 06.10.2026 (§3.6 Zeile δ,
§5 Absatz „Vorgabe für das Produkt (Befund 230)“). Die Schritte der Revision stehen im Block
„Revisionsstand“ unten; Prüfungen, Befunde und Null-Runde stehen nur im Ledger
`reviews/BEFUNDE_96.md`.** ·
Stand früherer Revisionen (Rev. 3, Rev. 2, Rev. 1): Block „Revisionsstand“ unten ·
Instruktionsquelle: `docs/AUFGABE_METHODIK_SCHADENSRECHNUNG.md` (v2) · Umsetzungsgrundlage:
**Ansatz 96-A** (Prävalenz, also Anteil der Betroffenen an der Bevölkerung, × gemessene Pollensaison-Spreizung, bottom-up; Entscheidungslog Nr. 1)
· Familie: **K1-Gesundheit bottom-up** (Prototyp #95; §2.6 — kein erneuter Drei-Ansätze-Vergleich)

> **Konformitätsvermerk zu den Aufgaben-Fortschreibungen 30./31.08.2026**
> (Ressourcen-Regel §3.4, Datenebenen-Anlagepflicht §3.1, geschlossene
> Betrachtungsebene §3.2; Nutzer-Entscheide, vgl. #95 Rev. 8):
> Dieser Bericht ist geprüft konform — er plant **keinen** nationalen
> 100-m-Vollraster-Lauf als Prüf-/Abgleichinstrument; die P̂-Zentrierung nutzt
> seit Rev. 2 ausschließlich das Mittel der **eigenen Kommune** (§3.3, Log 18/19); die Ebenen POLLEN_LOAD (OSM-Vegetation, §3.3), POPULATION_U20 (§3.2) und CANOPY_BIRCH_FRACTION **führt das Produkt** (§3.1-Anlagepflicht erfüllt); alle übrigen Zellgrößen sind vorhanden oder regional/national — keine Zellgröße läuft auf einem unspezifizierten Neutral-Fallback.

> **Revisionsstand.** **Rev. 4 (26.09.2026)** = Fortschreibung 7 der Aufgabe für M0 (A-0048, P3) in
> vier Schritten, jeweils ohne Änderung eines Basiswerts oder eines Parameterwerts in Kapitel 7. **Schritt 1 (T-1238):** Rechenkette §3.0
> an der Beispielkommune Berlin mit Zelllauf des Produkts; Kapitel 9 gestrichen (Log 21/22, Befunde
> 152–155). **Schritt 2 (T-1239):** S158 wirkt nur an gewarnten Tagen (DWD-Index mindestens „mittel“
> [70]), neuer Block `pollen.t_warn_s158` = 0,75, wirksamer Wert 0,03 × 0,75 = 2,25 % der Zusatztage im
> Geltungsbereich; allergenarme Stadtbaumwahl als Abschätzung je Zelle; betroffen §2, §3.6, §5, §5.1,
> §6 Modellgrenze 8, §7 (Log 23/24, Befunde 156–167). **Schritt 3 (T-1240):** Kap. 1 Unterabschnitt
> „Risiko ohne (weitere) Anpassung“ mit KWRA-Stufen und Gewissheit je Zeitscheibe; Kap. 6 Satz zu
> Jahresbeträgen ohne Abzinsung; Kap. 7 `kennzeichnung` in allen 13 Blöcken; Quellen [15] (Vollzitat)
> und [73] (neu); Kap. 1 (a) mit Erhebungsjahren und Lücke bis heute, Unsicherheit in drei Bändern (Log 25,
> Befunde 168–181). **Schritt 4 (T-1323, T-1362):** Bezugswert Ḡ₀ der Zentrierung im Ausgangsstand
> festgehalten, die allergenarme Stadtbaumwahl senkt damit die Summe der Kommune; betroffen §3.3, §3.4,
> §3.6, §5, Ebene 7, Kap. 1 (b), Modellgrenze 7, Quelle [74] (Log 26, Log 19 verworfen, Befund 182).
> **Nachzug (T-1330):** Befunde 183–185 aus Runde 13 — Untergrenze 4,38 Mio. € in Kap. 1, Restrisiko-Werte
> AB bis AF in Kap. 1 (b) mit Maßnahmenpaket und Zeitscheibe, Publikationslinks für [15] und [73] in Kap. 8.
> **Runde 14 (T-1330):** Befunde 186–194 — Stadtbaumwahl über den Kronenanteil gerechnet (§5, Kap. 1 (b),
> Log 26: −1.179 statt −2.541 Tage), Lesart im Ausgangsstand (Kap. 1 (a), Ebene 7, §3.3), DEGS1-Wert 40–49 Jahre
> 14,4 % statt 14,3 % (20–64 bleibt 13,2 %), Fundstellen [6], [15], [68], [70], min(1; m/f) als Abschätzung, Zeichen Ḡ₀ für den Bezugswert.
> **Runde 15 (T-1330):** Befunde 195–197 — Stadtbaumwahl mit der vollen Ebenendefinition: Senkung im Term,
> in dem die Kronen im Ausgangsstand stehen (Kronen ohne Gattungs-Tag nur mit 0,12), Grenze
> Ĝ′ ≥ 0,536 × Grünanteil (§5, Integrationsauflage, Kap. 1 (b), Log 24/26); Berliner Zelle mit 0,2 × Ḡ₀ / 0,464;
> Schreibweise „Pp.“. Befund 198 (QUELLEN.md) liegt außerhalb des Rahmens und ist an den CMO zurückgestellt.
> **Runde 16 (T-1427):** Befunde 199–200 — Abgrenzung in §5.1 auf die Regel nach Log 26 (Vegetationsmaßnahme,
> auch flächig, nur im Zelllauf über Ĝ′ bei festgehaltenem Ḡ₀; r_S158 als Verhaltenskanal), Log 24 nachgezogen;
> flächiges Programm in §5 mit der Bedingung „keine Kronen ohne Gattungs-Tag“ (sonst 6,5 % als Obergrenze).
> **Runde 17 (T-1427):** Befunde 201–204 — Sensitivität von p_B/p_G in §3.4 nachgerechnet (−11,7 % bis +11,7 %
> und −11,4 % bis +7,6 % statt ±6 % und ±8 %), k̄_unbek beim flächigen Programm, Komma in der Statuszeile,
> u20 in §3.2 aus 5er-Jahresgruppen; Sensitivität von f in §3.4 und Log 7 nachgerechnet (Befund 206).
> **Runde 25 (T-1633):** Befunde 241–245 — Zelllauf §3.0 mit der Ersatzregel des Produkts: 4,58 Mio. €
> je Jahr, Bandsummen mit dem Produktcode nachgemessen (Anlage `96_zelllauf_bandsummen.py`), Unterschied
> zur Kette und Toleranz ± 0,005 Mio. €; S158 im Zelllauf 16.632 Tage; Schwelle, ab der sich die
> Frühwarnung gegen den Betrieb trägt (§5.1).
> **Runde 26 (T-1634):** Befunde 246–252 — Stadtbaumwahl: s_unbek kommunenweit und eine Eingabe a als
> Modellgrenzen mit Richtung und Größe, Grenze je Term, Boden 0,536 × Grünanteil ohne eigenen Parameter,
> Toleranz und Block der Allee-Zelle, Wertebereich 0 bis 1 für anteil_ersetzt (§5).
> **Runde 27 (T-1635):** Befund 253 — Kosten der Stadtbaumwahl je Baum als Abschätzung von KAP3: 60 € bei
> ohnehin fälliger Nachpflanzung, 4.436 € bei vorgezogenem Ersatz (Preisstand 2024; §5, Kap. 7 Abschnitt 7.1
> `pollen.stadtbaum_kosten`, Quellen [75]–[82], VPI 2022 in [19]); Kapitel 7 führt damit 14 Blöcke. Herleitung der
> Artenwahl (Linde statt Birke) und der Fällung, Amortisation der Nachpflanzung mit wachsender Krone (18 Jahre),
> Abfrage des Falls im Produkt (Log 27). Kein Basiswert und kein bestehender Wert in Kapitel 7 geändert; der
> Betrag für Berlin bleibt.
> **Runde 29 (T-1638):** Befunde 254–257 aus Runde 28 — jeder statistische Fachbegriff ist bei erster Verwendung
> in Klartext erklärt (Prüfpunkt E4; Liste in Befund 255), mit Rechnung für die Streuung der Stationen (§3.1);
> Log 20 mit dem Produktstand der Sperre aus Befund 124; Hinweis aus [81] zur Linde in Reihen (§5); Fundstelle
> der verworfenen Zahlen in Log 22. Keine Zahl der Rechnung geändert.
> **Runden 30–32 (T-1650, T-1651):** Befunde 258–264 — Klimaanteil \(a_{\text{attr}}\) 0,27 statt 0,50: Mitte der Spanne
> 19–35 % für die Saisonlänge 1990–2018 aus [9], Abschätzung von KAP3, Band 0,19–0,41 (Befund 258). Neuer Basiswert
> Berlin 408.106 Tage und 2,53 Mio. € je Jahr (Kette), 2,47 Mio. € (Zelllauf); Bund ≈ 60 Mio. € je Jahr; §4 vergleicht
> beim selben \(a_{\text{attr}}\) (Log 28); §5 und §5.1 nachgezogen (Allee-Zelle −14,2 Tage, Amortisation 24 Jahre; S158 Berlin
> 9.182 Tage, Schwellen 0,056 und 0,0016). Dazu Begriffstabelle (259), L-Band beim stärksten Treiber (260), Form im
> Ledger (261), Zahlen aus den Blöcken in §5 (262, 263) und Significance von [9] (264). Code folgt Bericht: Übernahme
> Ü-13 beim CTO.
> **Code-Stand (29.09.2026, Befund 245):** `POLLEN_EARLY_WARNING` führt `EXPECTED_ANNUAL_ALLERGY_DAYS` in
> `linked_risk_codes` und rechnet mit `default_reduction` = 0,03 im Zelllauf (Modell `s158`, §5.1
> „Produktstand“); die allergenarme Stadtbaumwahl rechnet als `LOW_ALLERGEN_TREE_SELECTION` im Zelllauf
> (§5). Der Zelllauf rechnet 65+ mit der Ersatzregel aus #95 §3.3 (§3.0).
> **Stand der früheren Revisionen** (bis Rev. 4 in der Statuszeile geführt, Befund 181): Rev. 3 (08.09.2026)
> hatte noch kein eigenes Review (Ledger-Befund 151); sie ist in Rev. 4 fortgeschrieben und wird mit ihr
> geprüft. Rev. 2 (31.08.2026) war
> abnahmereif und ist integriert (Null-Runde: Review Runde 10; Befunde 116–150 behoben); Rev. 1 war abnahmereif
> (Null-Runde Runde 3) und ist integriert.
> **Rev. 3 (08.09.2026)** = Wirkungsabschätzung des S158-Hebels
> (Pollen-Frühwarnung): Der Hebel läuft nicht mehr „qualitativ" mit Wirkung null, sondern
> mit \(r_{\text{S158}}\) = 0,03 (Band 0,005–0,10) als §3.9-Abschätzung — **Vorgabe P2 des
> Aufsichtsrats (F-0007 Punkt 1)**, Aufgabe §3.5 i. d. F. 06.09.2026. Betroffen: Kap. 1
> (Knoten-Bilanz S158), §2 (Register 96-S158-01), §3.6-Zeichentabelle, **§5.1 (neu)**,
> §6 Modellgrenze 8 (neu), §7 (`pollen.r_s158`), Entscheidungslog 15/20. Der Katalogwert
> `default_reduction` bleibt in dieser Revision 0,0 (Code-Nachzug L2 als eigener Schritt);
> die Sperre aus Befund 124 (kein pauschaler `linked_risk_codes`-Kanal) bleibt bestehen.
> **Rev. 2 (31.08.2026)** = Bezugsebene der P̂-Zentrierung:
> Der Bezugswert der Zentrierung (heute Ḡ₀, Log 26) ist nicht mehr ein bundesweites Referenzmittel, sondern das
> betroffenengewichtete Mittel der **betrachteten Kommune**, im Lauf aus ihren
> eigenen Zellen gebildet (Aufgabe §3.2 „geschlossene Betrachtungsebene",
> Nutzer-Entscheid; Log 18). Damit gilt Σ B·P̂ = Σ B je Kommune **exakt**, ein
> Registry-/Bundeswert entfällt ersatzlos, und ohne Referenz bleibt P̂ ≡ 1.
> Folgeentscheidung Log 19: **kein** eingefrorener Referenzzustand — ein
> flächiger Vegetations-Niveaueffekt bleibt bewusst unbuchbar (§5,
> Modellgrenze 7); in Rev. 4 durch Log 26 überstimmt (Ḡ₀ festgehalten). Gleiche Linie beim Ĝ-Gewicht \(w_B\): erst
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
| E09 | Trockenheit (eine Ebene tief, Eingang von W025) | **bewusst inaktiv** | — | keine quantifizierte Trockenheit→Pollen-ERF (ERF heißt Expositions-Wirkungs-Funktion: um wie viel die Pollenbelastung je Einheit Trockenheit steigt); Wirkrichtung intensitätserhöhend — konsistent zur konservativen Nicht-Ansetzung der Intensität (Log 14; Rev.-5-Befund 52) |
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
408.106 Tage und 2,53 Mio. € je Jahr (Preisstand 2024) in der Rechenkette §3.0 — gehören zum KWRA-Zustand
**„Risiko ohne (weitere) Anpassung“**, und zwar zur Zeitscheibe Gegenwart: M0 weist das Ist-Klima aus
(Normalperioden 1961–1990 gegen 1991–2020, Kapitel 6). Der umgesetzte Anpassungsstand steckt über die
Erhebungsjahre der gemessenen Größen im Basiswert, nicht in einem eigenen Faktor:

- **Prävalenz \(p_{\text{AR},a}\):** Erwachsene aus DEGS1, erhoben 2008–2011 ([1], S. 698, Abschnitt Methoden),
  Kinder und Jugendliche aus KiGGS Welle 2, erhoben 2014–2017 ([2], S. 3, Abstract). Gezählt ist, wer in den
  letzten zwölf Monaten Beschwerden hatte, also unter der Versorgung und dem Verhalten dieser Jahre.
- **Kosten je Betroffenem:** aus der schwedischen TOTALL-Studie (18–65 Jahre, Kosten in Preisen von 2014; einen
  Erhebungszeitraum nennt der Artikel nicht, Abschnitt Materials and methods [65]), 1:1 auf Deutschland
  übertragen (§3.5, Modellgrenze 6). Im Euro-Betrag steckt damit der schwedische Versorgungsstand um 2014,
  nicht der deutsche.
- **Anteil der Saisontage mit Beschwerden \(f\):** eine Abschätzung von KAP3 ohne Erhebungsjahr (§3.4); er
  kürzt sich im Euro-Pfad heraus.

Der Basiswert trägt also den Anpassungsstand dieser Erhebungsjahre, nicht den von heute. Das entspricht der
Regel der KWRA für den Zustand ohne Anpassung: „Bei der Bewertung der Klimarisiken wurden
nur bestehende und umgesetzte Anpassungsmaßnahmen als Teil der Sensitivität berücksichtigt. Bisher nur geplante
und zukünftig mögliche Anpassungsoptionen und -maßnahmen wurden nicht einbezogen.“ (Teilbericht 1, S. 68 [73]). **Die Lücke
bis heute:** Anpassung, die seit den Erhebungsjahren hinzugekommen ist, fehlt im Basiswert. Dazu gehören
möglicherweise die Pollen-Apps, die Teilbericht 5, S. 180 [15] für den Stand 2021 als „bereits“ im Einsatz
beschreibt; wie weit sie 2008–2017 verbreitet waren, weiß der Bericht nicht, er behauptet deshalb nicht, dass sie im
Basiswert stecken. Die Richtung der Lücke ist **nicht bestimmbar**: Bei den Tagen würde mehr Vermeidung die Zahl
der Betroffenen mit Beschwerden senken; die 12-Monats-Prävalenz der Kinder und Jugendlichen ist zwischen der
KiGGS-Basiserhebung (2003–2006) und Welle 2 aber ohne wesentliche Veränderung geblieben ([2], S. 3). Bei den
Euro-Beträgen kann mehr Anpassung die Kosten je Betroffenem senken (weniger schwere Verläufe) oder heben (mehr
Medikation); eine Quelle, die das für Deutschland beziffert, gibt es nicht, und schon die Übertragung aus
Schweden wirkt nach Modellgrenze 6 in beide Richtungen. Die Maßnahmen des Aktionsplans Anpassung III, die
Teilbericht 5 ab S. 180 aufführt, gehören zum Restrisiko in (b). Eine Wirkung der
heutigen Pollenflug-Warnung rechnet der Basiswert weder heraus noch hinzu (S158 im Basiswert Default 1,
Knoten-Bilanz). Die heutige Stadtbaum- und Vegetationsausstattung wirkt über \(\hat G\) nur auf die
Verteilung der Zusatztage innerhalb der Kommune. Weil \(\hat P\) auf die eigene Kommune zentriert ist, also so
gebaut, dass sein mit den Betroffenen gewichtetes Mittel über die Zellen der Kommune genau 1 ist (im Ausgangsstand \(\sum B \hat P = \sum B\), §3.3, Log 18, 26), gilt: Die Vegetation hebt oder senkt den Basiswert der Kommune nicht
(Modellgrenze 7). Eine Kommune, die schon allergenarm pflanzt, sieht das heute nur in der Verteilung.

**(b) Zustand „mit Anpassung“.** Der Bericht stellt ihn nur als Wirkung der beiden Maßnahmen-Hebel auf den
Basiswert dar, nicht als eigenen Basiswert:

- **Pollen-Frühwarnung S158** (§5.1, Abschätzung von KAP3 nach Vorgabe P2): Sie wirkt nur an gewarnten Tagen
  (DWD-Pollenflug-Gefahrenindex mindestens „mittel“ [70], je Pollengruppe) und nur in Zellen im
  Geltungsbereich. Dort mindert sie \(r_{\text{S158}} \cdot t_{\text{warn}}\) = 0,03 × 0,75 = 2,25 % der
  Zusatztage. Beispielkommune Berlin, ganze Stadt im Geltungsbereich: 9.182 vermiedene Tage und
  ≈ 56.900 € je Jahr (Preisstand 2024).
- **Allergenarme Stadtbaumwahl** (§5, Log 24): Sie senkt den Kronenanteil allergener Bäume einer Zelle;
  \(\hat G\) sinkt um 0,464 × diese Änderung bei Kronen mit Gattungs-Tag der Birkengruppe, bei Kronen
  ohne Gattungs-Tag nur um 0,464 × 0,12 × diese Änderung, so wie der Ausgangsstand sie zählt
  (Ebenendefinition §3.3), \(\hat P\) um 0,14 je Senkung von
  \(\hat G/\bar G_0\) um 0,2. Weil der Bezugswert Ḡ₀ im Ausgangsstand festgehalten wird, sinkt die
  Summe der Kommune um die Senkung in den bepflanzten Zellen (Rechenbeispiel §5: vier Zellen,
  8.000 Betroffene, 637 Tage und ≈ 3.950 € weniger je Jahr; Richtung des Fehlers in
  Modellgrenze 7).

Beide Hebel rechnen im Zelllauf, als Katalogmaßnahmen
„Pollen-Frühwarnung“ und „Allergenarme Stadtbaumwahl“ (§5.1 und §5). Einen
Wert „mit Anpassung“ gibt es dort nur, wenn eine Kommune Maßnahmen wählt. Die KWRA-Stufen „mit Anpassung“ (Restrisiko, Blatt `Klimawirkungen`, Zeile 98,
Spalten AB bis AF, Maßnahmenpaket und Zeitscheibe nach Kopfzeile 2 der Mappe) sind:

- AB: Aktionsplan Anpassung III (APA III), 2020–2030: gering
- AC und AD: APA III, Mitte des Jahrhunderts, optimistisch und pessimistisch: gering und mittel
- AE und AF: weiterreichende Maßnahmen, Mitte des Jahrhunderts, optimistisch und pessimistisch: gering und mittel

Für das Ende des Jahrhunderts führt die Mappe kein Restrisiko; die Zeilen „Ende des Jahrhunderts“ in (c) gelten
nur ohne Anpassung. Der Bericht übernimmt diese Stufen nicht als Zahl: Sie bewerten die Maßnahmen des Bundes
(APA III und weiterreichende Maßnahmen; Blatt `Lesehinweise`, Zeile 27), nicht die Hebel einer Kommune.

**(c) KWRA-Stufe ohne Anpassung und Gewissheit je Zeitscheibe.**

| Zeitscheibe (KWRA) | Fall | Risiko ohne Anpassung | Zelle | Gewissheit | Zelle |
|---|---|---|---|---|---|
| Gegenwart (jüngere Gegenwart, qualitative Bewertung; Teilbericht 1, S. 68, Fn. 7) | — | gering | N98 | nicht ausgewiesen | — |
| Mitte des Jahrhunderts (2031–2060) | optimistisch | mittel | O98 | mittel | S98 |
| Mitte des Jahrhunderts (2031–2060) | pessimistisch | hoch | P98 | mittel | S98 |
| Ende des Jahrhunderts (2071–2100) | optimistisch | mittel | Q98 | mittel | T98 |
| Ende des Jahrhunderts (2071–2100) | pessimistisch | hoch | R98 | mittel | T98 |

Fundstelle: `docs/KWAR/KWRA-2021_Klimawirkungen.xlsx`, Blatt `Klimawirkungen` (ID 96 in Spalte A), Zeile 98, Spalten N bis R
(Risiko ohne Anpassung) und Spalten S und T (Gewissheit Mitte und Ende). Gleichlautend im zuständigen
Teilbericht: `docs/KWAR/kwra2021_teilbericht_5_cluster_wirtschaft_gesundheit_bf_211027_0.pdf`,
Tabelle 55, S. 179 [15]. Die Stufen sind eine qualitative Bewertung. Optimistisch und pessimistisch sind dort die für die
Klimawirkung günstigere und die ungünstigere Szenarienkombination; für die Mitte des Jahrhunderts aus Klima-
und sozioökonomischen Projektionen, für das Ende nur aus Klimaprojektionen (Teilbericht 1, S. 68 [73]).
Fußnote 7 derselben Seite grenzt die Bewertung von der quantitativen Analyse ab: „zum Beispiel wurde bei der
quantitativen Analyse als Gegenwart der Bezugszeitraum (1971 bis 2000) und meist der untere Rand des RCP8.5
Szenarios für den optimistischen Fall verwendet; bei der qualitativen Bewertung hingegen wurde unter dem
optimistischen Fall meist die jüngere Gegenwart und ein schwächerer oder moderater Klimawandel verstanden“.
Wir lesen das so: Die Zeitscheibe Gegenwart der Stufen meint die jüngere Gegenwart, nicht den Bezugszeitraum
1971–2000. Dieser Bezugszeitraum und die Perzentile des Modellensembles (Perzentil: der Wert, unter dem ein
bestimmter Anteil der Rechnungen der verschiedenen Klimamodelle liegt) in Teilbericht 5, S. 177 (Indikator GE-KL-07 S. 176, Projektion S. 178) gehören
zur quantitativen Auswertung des Indikators GE-KL-07, nicht zu den Stufen. Der Basiswert dieses Berichts
(Ist-Klima, Normalperiode 1991–2020 gegen 1961–1990) passt damit zur Zeitscheibe Gegenwart der Bewertung.
Für die Gegenwart weist die KWRA keine Gewissheit aus: In Tabelle 55, S. 179, steht in der Zeile „Gewissheit“ nur
unter 2031–2060 und 2071–2100 je „mittel“; das Feld Gegenwart ist leer, die Mappe hat dafür keine Spalte. Beide Digitalisate widersprechen sich hier nicht; die Bewertungen
stehen nach der Vorrangregel am Ende der Aufgabe ohnehin nur in der KWRA-2021-Mappe.

**Warum die eigene Quellenlage von der KWRA-Gewissheit abweicht.** Die KWRA-Gewissheit „mittel“ bewertet,
wie sicher die Projektion für 2031–2060 und 2071–2100 ist. Der Basiswert dieses Berichts rechnet dagegen die
Gegenwart aus gemessenen Größen (Phänologie an über 1.000 DWD-Stationen, Prävalenz aus Surveys). Seine
Unsicherheit liegt nicht in einer Klimaprojektion, sondern in drei Bändern (Beispielkommune Berlin, Basis
408.106 Tage und 2,53 Mio. € je Jahr, §3.0):

- **Klimaanteil \(a_{\text{attr}}\)** = 0,27 (0,19–0,41), Abschätzung von KAP3 aus einer nordamerikanischen Studie [9]:
  die Mitte der dort genannten Spanne für die Länge der Pollensaison 1990–2018 (Kap. 2, Befund 258). Stärkster
  Treiber für Tage und Euro gleichermaßen, 1,78–3,84 Mio. € je Jahr (−30 % bis +52 %).
- **Kostensatz \(c_{\text{Tag}}\)** = 6,20 € je Tag, Band bis 23,66 € (Schramm [7], mittelschwer bis schwer
  Erkrankte): wirkt nur auf den Euro-Betrag und nur nach oben, bis 9,7 Mio. € je Jahr; die Tage ändert er nicht.
- **Sensibilisierungsprofil \(p_B/p_G\)** (Abschätzung von KAP3, §3.4; Bänder 0,4–0,7 und 0,6–0,85): wirkt fast
  nur auf die Tage, 313.718–486.992 Tage (−23 % bis +19 %). Im Euro-Betrag kürzt es sich fast heraus, weil es
  über \(d_{\text{Saison}}\) auch im Kostensatz je Tag steht: 2,37–2,74 Mio. € (−6 % bis +8 %).

## 2 Evidenz-Register (§2.2)

Risikoübergreifend wiederverwendbare Zeilen zusätzlich in `docs/evidenz/register.md`.
Nur Zeilen mit Entscheidung **Basiswert** kommen in den Formeln (§3) vor. Spalte „E-Regel":
die Aufgabe definiert keine §2.8-E-Regeln (Lücken-Vermerk §2.8) — die
Spalte verweist auf die Entscheidungslog-Nummer.

| Register-ID | Knoten → Outcome | Effektgröße | Studientyp | Quelle | Übertragbarkeit | Datenlage je Zelle | Entscheidung | E-Regel |
|---|---|---|---|---|---|---|---|---|
| 96-W025-01 | W025/#1 Phänologie → Saison-Spreizung | \(\Delta S_B\) = 3,96/4,20/5,94 · \(\Delta S_G\) = 4,78/4,08/3,70 Tage (N/M/S; 1961–90 → 1991–2020) | amtliche Messreihe (DWD-Phänologie), eigene Auswertung (Skript [67]) | DWD-CDC Jahresmelder [33]; `pollensaison_region.csv` [67] | DE-weit, 1.083/1.085 gepaarte Stationen; Marker-Wahl §3.1 (Birke Phase 4 — Log 3) | regional (N/M/S je Bundesland, wie #95) | **Basiswert** | Log 2–5 |
| 96-W025-02 | Klimawandel → Anteil am Saisontrend | \(a_{\text{attr}}\) = 0,27 (Band 0,19–0,41), Abschätzung von KAP3. IQR heißt Interquartilsabstand: die Spanne, in der die mittlere Hälfte der Schätzungen liegt, je ein Viertel liegt darunter und darüber. Die Studie schätzt den Anteil mit 22 Klimamodellen je Kennzahl und Zeitraum und nennt vier solche Spannen: Saisonbeginn 35–66 % (1990–2018) und 45–84 % (2003–2018), Saisonlänge 19–35 % (1990–2018) und 22–41 % (2003–2018) ([9], Results und Abb. 3). \(\Delta S\) ist eine Verlängerung der Saison (§3.1), deshalb gilt die Saisonlänge; die rund 50 % im Abstract von [9] gelten Beginn und Länge zusammen. Eine Zahl für die Mitte der Schätzungen zur Länge nennt der Text nicht, Abb. 3 zeigt sie nur als Kasten. KAP3 nimmt deshalb die Mitte der Spanne 1990–2018: (0,19 + 0,35) ÷ 2 = 0,27; das Band 0,19–0,41 umfasst beide Spannen der Länge | Attributionsstudie (Beobachtung × Klimamodelle; sie trennt den Anteil des Klimawandels von anderen Ursachen) | Anderegg 2021, PNAS [9] | Nordamerika 1990–2018; Übertragung auf DE als dokumentierte Annahme (einzige publizierte Attribution) | Literatur-Band | **Basiswert** | Log 11 |
| 96-W025-03 | Intensitätszunahme (Pollenmenge, Herbst-Verlängerung) | Pollenintegral +20,9 % [9]; CO₂-Effekt Ambrosia +61…131 % [21,22]; Herbst-Spreizung der Kräuterpollen [6] | Beobachtung/Experiment | [6,9,21,22] | belegt, aber ohne DE-ERF je Zelle | — | **bewusst inaktiv** (Untergrenze; §6 Modellgrenze 1) | Log 4/14 |
| 96-W025-04 | E09 Trockenheit → Pollenfreisetzung/-transport | Wirkrichtung intensitätserhöhend; keine quantifizierte ERF | — | Rev.-5-Befund 52 | — | — | **bewusst inaktiv** | Log 14 |
| 96-W024-01 | W024 lokale allergene Vegetation → Symptomlast | \(\lambda\) = 0,7 (0,3–1,0); Kette §3.4: Fallen-Differenzen 245 %/306 % (14 Fallen Berlin; Zuwachs-Lesart ⇒ \(R\) = 3,45/4,06, Verhältnis-Lesart im Band) ⇒ \(\lambda_{\text{roh}}\) 1,10–1,21 × vegetationserklärter Anteil 0,6 (0,4–0,8) | Messreihen (Pollenfallen), Symptomgradient, Lidar-Studie | Werchan 2017 [54], Werchan 2018 [55], Bogawski 2019 [56] | Berlin/Posen; **gekennzeichnete Abschätzung** (§3.9) | OSM-Vegetation; Ebene POLLEN_LOAD **neu anzulegen** (§3.3) | **Basiswert** | Log 12 |
| 96-W024-02 | W024 Neophyten (Ambrosia) → Sensibilisierung | DE-Sensibilisierung 0–10 % → 15–25 % (2041–2060, 66 % klimabedingt); Kosten 193–1.190 Mio. €/a bei Voll-Etablierung | Projektion (Europa-Modell); Kostenmodell | Lake 2017 [23]; Hamaoui-Laguel 2015 [24]; Born 2012 [25] | Zeithorizont 2041–2060 ≠ M0-Ausweis „heute" | JKI-Fundkarten regional | **bewusst inaktiv** (Modul 96-B ab M1; §8-Verworfen-Liste) | Log 13 |
| 96-R35-01 | R35 Bevölkerung → Betroffene (Prävalenz) | \(p_{\text{AR},a}\): u20 8,8 % · 20–64 13,2 % · 65–74 6,7 % · 75–84 5,0 % · 85+ 5,0 % (12-Monats, ärztlich diagnostiziert; Herleitung §3.2) | bevölkerungsrepräsentative Surveys | DEGS1: Langen 2013, Tab. 3 [1]; KiGGS W2: Thamm 2018 [2]; Gewichte: Destatis 31.12.2023 [48] | DE; DEGS1 endet bei 79 (80–84 und 85+ extrapoliert, gekennzeichnet in §3.2) | Zensus-Altersbänder; Ebene u20 **neu anzulegen** (§3.2) | **Basiswert** | Log 10 |
| 96-R35-02 | Sensibilisierungsprofil der AR-Patienten (Birkengruppe/Gräser) | \(p_B\) = 0,55 (0,4–0,7) · \(p_G\) = 0,75 (0,6–0,85) | **gekennzeichnete Abschätzung** (§3.9); Stütze: Bevölkerungs-Sensibilisierung Gräser 19,4 % > Birke 17,4 % (Rangfolge) | Haftenberger 2013, Tab. 2/Abb. 1 [3] | Anteil *unter AR-Patienten* nicht direkt publiziert (Rev.-5-Befund 36a); Ersetzungspfad: PID-/Versorgungsdaten | national | **Basiswert** (Sensitivität §3.4) | Log 8 |
| 96-K1-01 | Behandlungskosten je Betroffenem und Jahr (direkt) | 210,3 €₂₀₁₄ (populationsbasiert, alle Schweregrade) ⇒ 266,90 €₂₀₂₄ (§3.5) | Bevölkerungs-Fragebogenstudie (n = 3.501) | Cardell 2016 (TOTALL) [65] | Schweden 18–65, Preisstand Feb. 2014 (CPI-adjustiert); Raumtransfer Schweden → Deutschland 1:1 dokumentiert | national | **Basiswert** | Log 9 |
| 96-K1-02 | Behandlungskosten moderate–schwere SAR (direkt) | Erwachsene 42 % × 1.543 = 648 €₂₀₀₀ ⇒ 1.019 €₂₀₂₄; Kinder 60–78 % × 1.089 ⇒ 1.027–1.335 €₂₀₂₄ | Querschnitt, also Erhebung zu einem Zeitpunkt (500 Patienten, fachärztlich) | Schramm 2003 [7] (Abstract-Zahlen primärverifiziert) | DE; **moderate–schwere** SAR — Überschätzungsrichtung je Durchschnittspatient | national | **Sensitivitätsband** (Obergrenze \(c_{\text{Tag}}\)) | Log 9 |
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
| 6 | Zusätzliche Symptomtage je Betroffenem \(\delta = f \times \text{Ebene 5} \times a_{\text{attr}}\) (Anteil der Saisontage mit Beschwerden, Anteil des Klimawandels am Trend) | 0,70 × 5,37 × 0,27 = **1,01493 Tage** je Betroffenem und Jahr | \(f\): Abschätzung von KAP3 (§3.4, Log 7); \(a_{\text{attr}}\): Abschätzung von KAP3, Mitte der Spanne 19–35 % für die Saisonlänge 1990–2018 aus Anderegg [9] (Kap. 2, Log 11, Befund 258); Kap. 7 `pollen.f_symptomtage`, `pollen.a_attr` |
| 7 | Vegetationsfaktor \(\hat P\) je Zelle (allergene Bäume und Grünflächen), zentriert auf den Bezugswert Ḡ₀, das betroffenengewichtete Mittel der eigenen Kommune im Ausgangsstand | je Zelle ab 0,3 (keine allergene Vegetation) bis über 1 (Allee, Park); Mittel über Berlin im Ausgangsstand genau **1**, also \(\sum B \hat P = \sum B\) = 402.103 | \(\lambda\) = 0,7 aus Werchan [54,55], Bogawski [56], Lesart als örtlicher Anteil Hugg [74] (§3.3, §3.4, Log 12, 17, 18, 26); Kap. 7 `pollen.lambda_veg` |
| 8 | Zusätzliche Symptomtage \(\Delta\text{Tage} = B \times \delta \times \hat P\) (native Ergebnisgröße) | 402.103 × 1,01493 × 1 = **408.106 Tage je Jahr** (u20 60.133 · 20–64 306.546 · 65–74 23.085 · 75–84 12.866 · 85+ 5.477; die gerundeten Bänder ergeben 408.107, mit den ungerundeten Betroffenen 402.103,45 sind es 408.106,9) | Ebenen 3, 6 und 7 |
| 9 | Kostensatz je Symptomtag \(c_{\text{Tag}} = c_{\text{Jahr,direkt}} / d_{\text{Saison}}\) mit \(d_{\text{Saison}} = f \times (p_B L_B + p_G L_G)\) | 266,90 € / (0,70 × (0,55 × 30 + 0,75 × 60)) = 266,90 € / 43,05 Tage = **6,20 € je Tag** (Preisstand 2024) | TOTALL [65], VPI [19]; \(L_B\), \(L_G\): Abschätzung von KAP3 nach [51] (§3.5); Kap. 7 `pollen.c_jahr_direkt`, `pollen.d_saison`, `pollen.c_tag` |
| 10 | Bewerteter Schaden (Konto K1, nur Morbidität) je Jahr = \(\Delta\text{Tage} \times c_{\text{Tag}}\) | 408.106 × 6,20 € = **2,53 Mio. € je Jahr (Preisstand 2024)**, das sind 0,69 € je Einwohner; der Zelllauf des Produkts ergibt 2,47 Mio. € (Unterschied und Toleranz unten). | Ebenen 8 und 9 |

**Warum \(f\) im Euro-Betrag keine Rolle spielt.** \(f\) steht in Ebene 6 (mehr Tage) und in
Ebene 9 (mehr Tage in der Referenzsaison, also billigerer Tag); in Ebene 10 kürzt es sich
deshalb heraus (§3.5). Es wirkt nur auf die Zahl der Tage.

**Ebene 7: Warum der Vegetationsfaktor im Ausgangsstand auf der Ebene der Kommune herausfällt.**
\(\hat P\) ist so gebaut, dass sein mit den Betroffenen gewichtetes Mittel über die Zellen der
eigenen Kommune im Ausgangsstand genau 1 ist (Bezugswert Ḡ₀ aus den eigenen Zellen, Log 17, 18
und 26). Für die Summe über Berlin gilt deshalb heute \(\sum B \hat P = \sum B\), gleich wie grün
die Stadt ist. Im Ausgangsstand ändert der Vegetationsfaktor
also nicht, *wie viele* Symptomtage Berlin hat, sondern nur, *wo* sie anfallen: Eine Zelle an
einer Birkenallee mit doppelt so viel allergener Vegetation wie im Mittel bekommt
\(\hat P\) = 1 + 0,7 × (2 − 1) = 1,7, eine Zelle ohne kartierte Vegetation 1 − 0,7 = 0,3. Eine
insgesamt grünere Kommune hat damit nicht mehr Tage als eine graue; das trägt die Evidenz nicht
(Log 18, Modellgrenze 7 in §6). Anders eine Maßnahme: Ḡ₀ wird für Maßnahmen festgehalten; eine
allergenarme Pflanzung senkt deshalb die Summe (§5).

**Kommune statt Zellen: was die Kette verfälscht und was nicht.** Das Produkt rechnet je
100-m-Zelle mit der Bevölkerung aus dem Zensus-Gitter (Stichtag 15.05.2022) und summiert; die
Kette rechnet mit der Fortschreibung für ganz Berlin (Stichtag 31.12.2023, Ebene 1). **Die Kette
liegt für Berlin um 2,2 % über dem Zelllauf.** Zwei Schritte sind auf der Ebene der Kommune exakt:
\(\delta\) ist in der ganzen Kommune gleich (eine Region), und \(\hat P\) mittelt auf 1 (Ebene 7).
Wirkungen wie in #95 für die Temperatur je Zelle und die Feinstruktur unter 1 km gibt es in #96
deshalb nicht. Was bleibt, ist die Bevölkerung. Gemessen ist das mit dem Produktcode an allen
40.669 bewohnten 100-m-Zellen innerhalb der Gemeindegrenze Berlins, gepinnt in
`backend/data/kalibrierung/golden96_zellen_11000000.csv.gz`. Die Altersbänder je Zelle kommen aus
`zensus_loader.apply_zensus_to_cell_inputs`, mit der Ersatzregel aus #95 §3.3 für Zellen mit
geheimgehaltenem Anteil 65+ und mit u20 je Zelle aus den 5er-Jahresgruppen (§3.2). Tage und Euro
kommen aus `impact.compute_all_cell_impacts`. Anlage `docs/methodik/anlagen/96_zelllauf_bandsummen.py`,
Aufruf `bash scripts/testlauf.sh docs/methodik/anlagen/96_zelllauf_bandsummen.py -q -s`, Lauf
30.09.2026, mit \(a_{\text{attr}}\) aus Kapitel 7 (Block `pollen.a_attr`). Die Bandsummen des Gitters sind u20 655.066 · 20–64 2.230.974 · 65–74 341.087 ·
75–84 267.692 · 85+ 98.539 (zusammen 3.593.357; die gerundeten Bänder ergeben 3.593.358). Zwei
Wirkungen erklären den Unterschied, jede auf die vorige gerechnet:
(1) **Einwohnersumme: × 0,9812 (−1,88 %).** Das Gitter zählt 3.593.357 Einwohner, die
Fortschreibung 3.662.381 (#95 Befund 99).
(2) **Altersbänder je Zelle: × 0,9969 (−0,31 %).** Im Gitter sind mit der Ersatzregel 19,7 % der
Einwohner 65 Jahre und älter, in der Fortschreibung 19,1 %. Mehr Menschen stehen damit in den
Bändern mit 6,7 % und 5,0 % Prävalenz statt mit 8,8 % und 13,2 %, und die mittlere Prävalenz sinkt
von 10,98 % auf 10,95 %. Der Anteil u20 an den unter 65-Jährigen ist fast gleich (22,70 % gegen
22,73 % in Ebene 1).
Zusammen 0,9812 × 0,9969 = 0,9781: Der Zelllauf ergibt für Berlin 393.299 Betroffene, 399.171
zusätzliche Symptomtage und **2,47 Mio. € je Jahr (Preisstand 2024)**. Das sind 2,19 % oder
0,06 Mio. € weniger als die Kette mit 2,53 Mio. €, davon 0,05 Mio. € aus der Einwohnersumme und
0,01 Mio. € aus den Altersbändern. **Toleranz des Zelllaufs: ± 0,005 Mio. €.** Der Zelllauf ist auf
den gepinnten Zelldaten deterministisch: Dieselben Zellen und derselbe Code ergeben dieselbe Zahl,
gemessen 2,4749 Mio. €. Die Toleranz ist deshalb nur die Rundung auf zwei Nachkommastellen, wie im
Golden-Test `backend/tests/test_methodik_96_golden_betraege.py`; der Messwert liegt 0,0049 Mio. €
neben dem Berichtswert. Mehr Spiel wie in Bericht #95 (± 1 Mio. € für Berlin) braucht #96 nicht,
weil der Betrag der Kommune hier nur von den Einwohnern je Band abhängt. Ein neuer Datenstand
(anderes Gitter, andere Gemeindezeile für die Ersatzregel) ist eine neue Messung mit der Anlage,
keine Frage der Toleranz. Die Kette zeigt den Rechenweg, der Betrag für Berlin ist der Zelllauf
des Produkts.
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

**Stärkster Treiber** ist der Klimaanteil \(a_{\text{attr}}\) (Ebene 6): Sein Band 0,19–0,41
(Anderegg [9], Kap. 2) setzt Tage und Euro für Berlin auf das 0,70- bis 1,52-Fache (−30 % bis +52 %), also 1,78–3,84 Mio. €
je Jahr. Nachgeprüft an den übrigen Bändern aus Kapitel 7: \(f\) (0,50–0,85) wirkt nur auf die Tage, −29 % bis
+21 %; \(p_B/p_G\) wirkt auf die Tage −23 % bis +19 % und auf den Euro-Betrag −6 % bis +8 % (Kap. 1); \(L_B/L_G\)
(20–45 und 45–80 Tage, Kap. 7 `pollen.l_saison`) wirkt über \(d_{\text{Saison}}\) nur auf den Euro-Betrag, −27 % bis
+37 % (1,84–3,48 Mio. €); \(\lambda\)
ändert die Summe der Kommune im Ausgangsstand nicht (Ebene 7). Weiter reicht nur das Band des Kostensatzes nach oben (Obergrenze 23,66 € je Tag aus
Schramm [7] für mittelschwer bis schwer Erkrankte, damit 9,7 Mio. €); es ist einseitig und
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
p_B, p_G, f, a_attr = 0.55, 0.75, 0.70, 0.27   # a_attr: Kap. 7 pollen.a_attr (Befund 258)
gew = p_B * dS_B + p_G * dS_G
assert abs(gew - 5.37) < 1e-9
delta = f * gew * a_attr
assert abs(delta - 1.01493) < 1e-9
# Ebene 7: Zentrierung auf G0 der eigenen Kommune -> Summe im Ausgangsstand gegen P^ invariant
# (mit Massnahme sinkt sie, G0 festgehalten: Beispiel beispiel_96_stadtbaum_kommunensumme, Kap. 5)
lam = 0.7
zellen = [(1_000, 0.00), (4_000, 0.10), (2_500, 0.30), (500, 0.60)]  # (B, G^)
g_bar = sum(b * g for b, g in zellen) / sum(b for b, _ in zellen)
p_hat = [1 + lam * (g / g_bar - 1) for _, g in zellen]
assert abs(sum(b * p for (b, _), p in zip(zellen, p_hat)) - sum(b for b, _ in zellen)) < 1e-9
assert abs(p_hat[0] - 0.3) < 1e-9 and abs((1 + lam * (2 - 1)) - 1.7) < 1e-9
tage = B * delta * 1.0
assert abs(tage - 408_106) < 1 and abs(402_103 * delta - 408_106) < 0.5
tage_band = {k: v * delta for k, v in b_band.items()}
for k, soll in {"u20": 60_133, "20-64": 306_546, "65-74": 23_085,
                "75-84": 12_866, "85+": 5_477}.items():
    assert abs(tage_band[k] - soll) < 1
d_saison = f * (p_B * 30 + p_G * 60)
assert abs(d_saison - 43.05) < 1e-9
c_tag = 6.20                      # Kap. 7 pollen.c_tag (= 266,90 / 43,05, gerundet)
assert abs(266.90 / d_saison - c_tag) < 0.01
euro = tage * c_tag
assert abs(euro / 1e6 - 2.53) < 0.005
assert abs(euro / sum(pop.values()) - 0.69) < 0.005
# Grenze der Kommunenrechnung (Bundes- statt Kommunenanteil u20) und staerkster Treiber
assert abs(0.01 * u65 * (0.132 - 0.088) - 1_303) < 1
anteil_bund = 15_583_456 / 64_747_448
assert abs(anteil_bund - 0.2407) < 1e-4
mehr_u20 = round(u65 * anteil_bund) - pop["u20"]
verschiebung = mehr_u20 * (0.132 - 0.088)
assert abs(mehr_u20 - 39_482) < 2
assert abs(verschiebung - 1_737) < 1 and abs(verschiebung / B - 0.0043) < 0.0001
assert abs(euro * 0.19 / a_attr / 1e6 - 1.78) < 0.005 and abs(0.19 / a_attr - 0.70) < 0.005
assert abs(euro * 0.41 / a_attr / 1e6 - 3.84) < 0.005 and abs(0.41 / a_attr - 1.52) < 0.005
assert abs(tage * 23.66 / 1e6 - 9.7) < 0.05
L_lo, L_hi = 0.55 * 20 + 0.75 * 45, 0.55 * 45 + 0.75 * 80   # Kap. 7 pollen.l_saison, Bandenden (Befund 260)
assert abs(euro * 61.5 / L_hi / 1e6 - 1.84) < 0.005 and abs(euro * 61.5 / L_lo / 1e6 - 3.48) < 0.005
assert round((61.5 / L_hi - 1) * 100) == -27 and round((61.5 / L_lo - 1) * 100) == 37
# Zelllauf des Produkts mit Ersatzregel #95 §3.3 (40.669 Zellen, gepinnte Zelldaten; Anlage
# 96_zelllauf_bandsummen.py, Lauf 30.09.2026): Bandsummen, Zerlegung, Toleranz
zell = {"u20": 655_066, "20-64": 2_230_974, "65-74": 341_087, "75-84": 267_692, "85+": 98_539}
assert abs(sum(zell.values()) - 3_593_357) <= 1          # gerundete Baender ergeben 3.593.358
assert abs(zell["u20"] / (zell["u20"] + zell["20-64"]) - 0.2270) < 1e-4
B_zell = sum(zell[k] * p_ar[k] for k in zell)
assert abs(B_zell - 393_299) < 1
assert abs(B_zell * delta - 399_171) < 1
euro_zell = B_zell * delta * c_tag
tol_zell = 0.005                    # Mio. EUR: Rundung, der Lauf ist deterministisch
assert abs(euro_zell / 1e6 - 2.47) < tol_zell
assert abs(euro_zell * 0.50 / a_attr / 1e6 - 4.58) < tol_zell   # heutiger Produktwert mit 0,50 bis Ue-13
f_ew = 3_593_357 / 3_662_381
assert abs(f_ew - 0.9812) < 0.00005
f_alter = B_zell / (B * f_ew)
assert abs(f_alter - 0.9969) < 0.00005
assert abs(B_zell / B - 0.9781) < 0.00005 and abs(1 - B_zell / B - 0.0219) < 0.00005
assert abs((euro - euro_zell) / 1e6 - 0.06) < 0.005
assert abs(euro * (1 - f_ew) / 1e6 - 0.05) < 0.005
assert abs(euro * f_ew * (1 - f_alter) / 1e6 - 0.01) < 0.005
ab65_zell = (zell["65-74"] + zell["75-84"] + zell["85+"]) / sum(zell.values())
assert abs(ab65_zell - 0.197) < 0.0005 and abs((a6574 + a7584 + a85p) / sum(pop.values()) - 0.191) < 0.0005
assert abs(B_zell / sum(zell.values()) - 0.1095) < 0.00005 and abs(B / sum(pop.values()) - 0.1098) < 0.00005
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

SD ist die Standardabweichung: der typische Abstand, um den die Spreizung einer einzelnen Station vom Mittel
abweicht, für die Birkengruppe 7,46 Tage. SE ist der Standardfehler: wie genau das Mittel über alle Stationen bestimmt
ist, die Standardabweichung geteilt durch die Wurzel aus der Zahl der Stationen, 7,46 ÷ √1.083 = 7,46 ÷ 32,9 = 0,23
Tage (Gräser 5,98 ÷ √1.085 = 0,18 Tage). Einzelne Stationen streuen stark, das Mittel ist trotzdem auf wenige Zehntel
Tage genau.

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
# Standardfehler = Standardabweichung / Wurzel(Zahl der Stationen):
assert abs(7.46 / 1083 ** 0.5 - 0.23) < 0.005 and abs(5.98 / 1085 ** 0.5 - 0.18) < 0.005
# Abstand des Mittels von null in Standardfehlern (§4): rund 21 und 23
assert round(de_b / 0.23) == 21 and round(de_g / 0.18) == 23
```

### 3.2 Betroffene je Zelle: altersspezifische Prävalenz (Anker `#p-ar`)

$$ B_{\text{Zelle}} \;=\; \sum_a \text{pop}_a \cdot p_{\text{AR},a} $$

**Konvention:** Die auf eine Nachkommastelle gerundeten Band-Prävalenzen sind die
verbindlichen Produktwerte (Registry `pollen.p_ar`); alle Summen dieses Berichts nutzen
sie (Befund 105).

**Bänder und Herleitung** (Rev.-5-Befunde 27/35): Das Produkt führt die Zensus-Bänder
u65/65–74/75–84/85+; für die Prävalenz-Schichtung wird zusätzlich die Ebene **u20 neu
angelegt** (Zensus-2022-Gitter, 5er-Jahresgruppen 0–4, 5–9, 10–14, 15–19; §3.1-Kennzeichnung „neu
anzulegen"); das Band 20–64 ergibt sich je Zelle als u65 − u20.
**Datenebene:** Das Produkt führt die Ebene `POPULATION_U20` —
aus dem Zensus-Gitterdatensatz „Alter in 5er-Jahresgruppen";
u20 wird aus `unter5 + a5bis9 + a10bis14 + a15bis19` als **Binnenaufteilung der
u65-Menge** gebildet (dasselbe Zwei-Quellen-Prinzip wie bei den Senioren-Bändern:
die gut besetzte u65-Menge legt das Niveau fest, die Feingruppen nur die
Aufteilung; Rückfall Zelle → Gebiet → national 0,2407). Prävalenzwerte (12-Monats,
ärztlich diagnostiziert) aus DEGS1 Tab. 3 [1] und KiGGS W2 [2], bevölkerungsgewichtet auf
die Produktbänder (Gewichte: Bevölkerung 31.12.2023 nach Altersjahren [48]):

- **u20 = 8,8 %** (KiGGS W2, 0–17; die 18/19-Jährigen erhalten den Kinder- statt des
  höheren DEGS1-Werts 14,6 % — dokumentiert **unterschätzend**, Log 10).
- **20–64 = 13,2 %**: (9.301.783·14,6 + 10.947.845·17,2 + 10.275.235·14,4 + 12.293.757·10,1
  + 6.345.372·8,2) / 49.163.992 = 13,19 ≈ 13,2 % (DEGS1-Dekadenwerte 14,6/17,2/14,4/10,1;
  60–64 mit dem 60–69-Wert 8,2).
- **65–74 = 6,7 %**: (5.180.675·8,2 + 4.388.965·5,0)/9.569.640 = 6,73 (65–69 → 8,2;
  70–74 → 5,0).
- **75–84 = 5,0 %** (DEGS1 70–79; 80–84 = Extrapolation, also über das Ende der Messwerte hinaus fortgeschrieben, gekennzeichnet).
- **85+ = 5,0 %** (Extrapolation über das DEGS1-Ende 79 hinaus, gekennzeichnet; Richtung
  unklar — Prävalenz fällt mit Alter, Untererfassung bei Hochaltrigen möglich).

```python test: beispiel_96_praevalenz_gewichtung
# p_AR 20-64 und 65-74: bevoelkerungsgewichtete DEGS1-Werte (Bev. 31.12.2023)
pop = {"20-29": 9_301_783, "30-39": 10_947_845, "40-49": 10_275_235,
       "50-59": 12_293_757, "60-64": 6_345_372, "65-69": 5_180_675, "70-74": 4_388_965}
p = {"20-29": 14.6, "30-39": 17.2, "40-49": 14.4, "50-59": 10.1, "60-64": 8.2,
     "65-69": 8.2, "70-74": 5.0}
g2064 = sum(pop[k]*p[k] for k in ["20-29","30-39","40-49","50-59","60-64"]) / \
        sum(pop[k] for k in ["20-29","30-39","40-49","50-59","60-64"])
g6574 = (pop["65-69"]*p["65-69"] + pop["70-74"]*p["70-74"]) / (pop["65-69"] + pop["70-74"])
assert abs(g2064 - 13.19) < 0.01
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

$$ \Delta\text{Tage}_{\text{Zelle}} \;=\; B_{\text{Zelle}} \cdot \delta_R \cdot \hat P_{\text{Zelle}}, \qquad \hat P_{\text{Zelle}} \;=\; 1 + \lambda \cdot \bigl( \hat G_{\text{Zelle}}/\bar G_0 - 1 \bigr) $$

- \(\hat P\) steht in **beiden** Pfaden (ΔTage **und** €) — natives Outcome und €-Wert
  bleiben strikt proportional (Rev.-5-Befund 12).
- **Zentrierung — Bezugswert Ḡ₀, Gewichtsregel und Bezugsebene definiert** (Befund 101; Log 17,
  **Rev. 2: Bezugsebene = die betrachtete Kommune**, Log 18; **Rev. 4: Bezugswert im Ausgangsstand
  festgehalten**, Log 26; Anker `#p-hat`):
  Der Bezugswert der Zentrierung heißt Ḡ₀. Ḡ₀ ist das **betroffenengewichtete Mittel über die
  bewohnten Zellen der eigenen Kommune im Ausgangsstand ohne die bewerteten Maßnahmen**
  (\(\hat G^{0}_{\text{Zelle}}\) = heutiger Vegetationsstand der Zelle):

  $$ \bar G_0 \;:=\; \frac{\sum_{\text{Zellen}} B_{\text{Zelle}} \cdot \hat G^{0}_{\text{Zelle}}}{\sum_{\text{Zellen}} B_{\text{Zelle}}} \qquad\Rightarrow\qquad \sum_{\text{Zellen}} B_{\text{Zelle}} \cdot \hat P^{0}_{\text{Zelle}} \;=\; \sum_{\text{Zellen}} B_{\text{Zelle}} \ \ \text{exakt (Ausgangsstand)}. $$

  **Ḡ₀ wird im Lauf des Ausgangsszenarios gebildet und für jedes Maßnahmenszenario
  festgehalten.** Eine Maßnahme ändert \(\hat G\) der Zellen, die sie trifft, zu \(\hat G'\),
  aber nicht Ḡ₀. Für die Kommune gilt dann

  $$ \sum_{\text{Zellen}} B \cdot \hat P' \;=\; (1-\lambda)\sum_{\text{Zellen}} B \;+\; \lambda \sum_{\text{Zellen}} B \cdot \frac{\hat G'}{\bar G_0}, \qquad \text{Senkung} \;=\; \lambda \cdot \frac{\sum_{\text{Zellen}} B \cdot (\hat G - \hat G')}{\bar G_0}. $$

  Senkt die Maßnahme \(\hat G\), sinkt die Kommunensumme; Rechenbeispiel in §5. 
  Ḡ ohne Index steht im Bericht nur noch für den in jedem Lauf neu gebildeten Wert der verworfenen Regel (Log 19).

  Mit dieser Gewichtung ist die **Kommunensumme im Ausgangsstand per Konstruktion invariant**, sie
  ändert sich also nicht, gleich wie groß \(\lambda\) ist und gleich welche Korrelation zwischen \(\hat G\)
  und Bevölkerung besteht (Korrelation: ein gleichgerichteter Zusammenhang, etwa wenn dicht bewohnte
  Zellen systematisch weniger Grün haben) — ein flächen- oder zellgewichtetes Mittel hätte diese
  Eigenschaft nicht (unbewohnte Waldzellen bzw. Stadtvegetation würden das mit den Betroffenen
  gewichtete Mittel von \(\hat P\) von 1 wegziehen, und da \(c_{\text{kal}} \equiv 1\) keinen Fit
  nachschaltet, also keine nachträgliche Anpassung des Niveaus an eine gemessene Summe (§4), würde das
  die Summe direkt verschieben); die §4-Sanity-Rechnung (mit \(\hat P\)-Mittel = 1) gilt damit
  **exakt je Kommune**, \(\hat P\) verteilt im Ausgangsstand ausschließlich **innerhalb** der
  Kommune um.

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
  Bundeslauf bestimmbar. Beides entfällt: \(\bar G_0\) entsteht im Lauf des Ausgangsstands aus den
  eigenen Zellen (`inputs.kommunale_pollen_referenz`).
  (3) **Konsequenz — ehrlich benannt, nicht beschönigt:** Die Vegetationsstruktur des
  Ausgangsstands verschiebt die **Kommunensumme nicht**; \(\hat P\) ist im Ausgangsstand
  **nullsummig umverteilend** (nicht „konservativ" im Sinne einer Unterschätzung — es ist
  betroffenengewichtet erwartungstreu, das heißt: über alle Betroffenen der Kommune gemittelt ist
  \(\hat P\) genau 1, die Kommune bekommt dadurch weder zu hoch noch zu niedrig gerechnete Tage). Der Ausweis differenziert damit **innerhalb**
  der Kommune (Hotspots an Alleen/Parks gegenüber vegetationsarmen Blöcken) und
  bleibt zwischen Kommunen bei dem, was Prävalenz und gemessenes Klimasignal
  hergeben. Eine Maßnahme dagegen wird am festgehaltenen Ḡ₀ gemessen und senkt die
  Kommunensumme, wenn sie \(\hat G\) senkt (§5, Modellgrenze 7 in §6, Log 26).
  (4) **Fehlt die Referenz** (Zelle ohne Kommunen-Kontext, Alt-Daten), bleibt
  \(\hat P \equiv 1\) — **kein Ersatz-Bundeswert** (Aufgabe §3.2).
  (5) **Fallback der Ebene selbst** (§3.1): Eine Zelle ohne kartierte OSM-Kronen
  und ohne Grünfläche erhält \(\hat G = 0\) — das ist die inhaltlich richtige
  Lesart („keine allergene Vegetation kartiert"), kein fehlender Wert; sie
  bekommt damit das kleinstmögliche \(\hat P = 1-\lambda\) (bei \(\lambda\) = 0,7:
  0,3). **Proxy-Grenze, dokumentiert** (Proxy: eine Ersatzgröße, die für eine nicht gemessene Größe
  steht, hier kartierte Kronen und Grünflächen für die örtliche Pollenmenge): OSM-Baumkataster sind lückenhaft — eine
  unkartierte Zelle ist von einer vegetationsfreien nicht unterscheidbar; die
  Zentrierung fängt das teilweise auf (fehlen Kronen flächendeckend, sinkt
  \(\bar G_0\) mit). Richtung: In Kommunen mit schwacher OSM-Erfassung
  differenziert \(\hat P\) schwächer; die Kommunensumme bleibt unberührt. Ebenen-Definition: OSM-basierter Anteil allergener Gehölze
  (Birke/Erle/Hasel-anteilige Baumkronen-/Gehölzfläche) + Grünflächenanteil als
  Gräser-Proxy, **neu anzulegen** (§3.1) — die Gewichtsregel ist hiermit festgelegt,
  die Arten-/OSM-Detailspezifikation steht unten. **Referenzzustand — Befund 113 unter der kommunalen Zentrierung**
  (Rev. 4, Log 26; Log 19 verworfen): Ḡ₀ wird im Ausgangsszenario aus dem heutigen
  Vegetationszustand der Kommune gebildet und in jedem Maßnahmenszenario festgehalten.
  Das ist die Fixierung, die Befund 113 vorgeschlagen hatte, jetzt auf der Ebene der
  Kommune. Bildete man Ḡ im Maßnahmenlauf neu (so Log 19 bis Rev. 4), höbe die neue
  Zentrierung jede Senkung genau auf: Im Rechenbeispiel in §5 bliebe die Summe bei 8.000,
  obwohl weniger Pollen fliegen. Das wäre die Nullwirkung, die Vorgabe P2 ausschließt.
  Den Einwand aus Log 19, die \(\lambda\)-Evidenz trage nur Gradienten innerhalb einer Stadt,
  beantwortet Log 26: Ein Programm der Kommune wird mit dem Ausgangsstand derselben Kommune
  verglichen, also innerhalb einer Stadt. Genau dort misst Hugg 2017 [74] den Anteil der
  örtlichen Quellen an der Pollenlast (Gräser, Helsinki und Espoo, abgeleitet 0,22–0,94;
  Richtung des Fehlers in Modellgrenze 7). Der Vergleich zwischen Kommunen bleibt unberührt
  (Log 18). **Produktseitige Konsequenz** (Befunde 124 und 231):
  Eine pauschal auf diesen Risiko-Code verknüpfte Maßnahme (`linked_risk_codes`) mit einem
  Wirkungsfaktor auf die gespeicherten Zell-Outcomes würde jede Zelle mit demselben Faktor
  senken, unabhängig von ihrem \(\hat G\) und davon, ob die Maßnahme sie trifft. Daher gilt als
  **Integrationsauflage**: Mit #96 ist **keine** pauschal wirkende Maßnahme verknüpft; eine
  Verknüpfung wirkt nur über eine Rechnung je Zelle, nie über einen kommunenweiten
  Reduktionsfaktor. Zwei Maßnahmen sind so verknüpft: Die
  allergenarme Stadtbaumwahl ändert \(\hat G\) der gewählten Zellen zu \(\hat G'\), und das
  Maßnahmen-Modul rechnet \(\hat P\) und die Zusatztage dieser Zellen bei festgehaltenem Ḡ₀ neu
  (§5); die Pollen-Frühwarnung rechnet die gewarnten Tage je Pollengruppe und Zelle (§5.1).
  Beide rechnen frisch aus den gespeicherten Eingaben der Zelle. Testseitig gebunden:
  `test_no_flat_measure_on_allergy_days` (für #96 nur die Zelllauf-Modelle `s158` und `stadtbaum`).
  \(\hat P \equiv 1\) ist **kein zulässiger stiller Fallback** —
  das Produkt führt die Ebene (Kartenebenen-Pflicht §3.6).
  **Ebene `POLLEN_LOAD` (§3.1-Anlagepflicht).** Detailspezifikation
  der Ebene (Gewichtsregel oben):
  \(\hat G_z = w_B\,[k_{\text{Birke},z} +
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
  \(\hat G/\bar G_0\) bei s_unbek 0,05 → 0,25, Ḡ₀ je Wert von s_unbek im Ausgangsstand gebildet):
  gehölzreich 0,665 → 0,752 (**+13,0 %**), vegetationsarm 0,255 → 0,258
  (+0,9 %), grünlastig 2,014 → 1,918 (**−4,7 %**), Mischlage 1,066 → 1,072
  (+0,6 %) — die Wirkung hängt vom Vegetationsprofil der Zelle ab und liegt für
  gehölzgeprägte Zellen im **zweistelligen Prozentbereich**, für die übrigen
  darunter. Die **Kommunensumme bleibt im Ausgangsstand unverändert** (Zentrierung auf Ḡ₀);
  betroffen ist dort ausschließlich die Verteilung innerhalb der Kommune. Reproduzierbar mit dem
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
  Schichtentrennung fest. \(\bar G_0\) dagegen wird im Lauf
  des Ausgangsszenarios aus den Zellen der jeweiligen Kommune gebildet (`inputs.kommunale_pollen_referenz`;
  Rev. 2, Log 18, 26) — damit gilt im Ausgangsstand \(\sum_z B_z \hat P_z = \sum_z B_z\) **exakt**
  (Golden-Test `test_reference_is_closed_within_the_kommune`) und die Betrachtungsebene
  bleibt geschlossen. Zur Plausibilisierung der Ebene dokumentiert das Skript
  `pollen_g_bar.py` (Anlagen `pollen_g_bar.csv`/`.md`) Größenordnung und Streuung von
  \(\hat G\) über drei Siedlungstypen: Offenbach am Main 0,174 · Freising 0,180 ·
  Weyarn 0,270 (2.896 bewohnte Zellen) — der Stadt-Land-Kontrast ist die erwartete
  Richtung und belegt, dass die Ebene misst, was sie soll.
- Werte je Region: \(\delta\) = **1,09 / 1,01 / 1,14** Tage je Betroffenem·Jahr (N/M/S;
  DE-gewichtet 1,07) mit den Basiswerten \(f\) = 0,70, \(p_B\) = 0,55, \(p_G\) = 0,75,
  \(a_{\text{attr}}\) = 0,27.
- **Saison-Fenster überlappen nicht:** \(\Delta S_B\) wirkt im Februar–April (Front der
  Birkengruppe), \(\Delta S_G\) im Mai–Juni (Gräser-Sukzession) — die Addition zählt keine
  Tage doppelt. (Zur Überlappung in \(d_{\text{Saison}}\) s. §3.5 — dort ist die additive
  Form €-konservativ; Rev.-5-Befund 36b.)

```python test: beispiel_96_delta_je_region
f, pB, pG, a = 0.70, 0.55, 0.75, 0.27
DS = {"nord": (3.96, 4.78), "mitte": (4.20, 4.08), "sued": (5.94, 3.70), "de": (4.79, 4.06)}
soll = {"nord": 1.089, "mitte": 1.015, "sued": 1.142, "de": 1.073}
for r, (db, dg) in DS.items():
    delta = f * (pB*db + pG*dg) * a
    assert abs(delta - soll[r]) < 0.002
```

### 3.4 Sensitivität der Basiswerte f, p_B/p_G, λ (Anker `#f-sympt`, `#p-sens`, `#lambda-veg`)

- **\(f\) = 0,70 (Band 0,50–0,85) — reine Modellannahme** (§3.9 „Abgeschätzt"; Log 7;
  Rev.-5-Befund 14): Anteil der Saisontage, an denen ein Patient symptomatisch/behandelnd
  ist. Die Pollen-Symptom-Korrelationen r = 0,48–0,79 (Pfaar 2020 [52]; r ist der Korrelationskoeffizient,
  0 heißt kein Zusammenhang, 1 heißt, Pollenflug und Beschwerden steigen und fallen vollständig gemeinsam) stützen nur
  **qualitativ**, dass Pollenflug die Symptomlast treibt — sie sind **kein** Zahlenwert für
  \(f\) (Kategorienfehler der Rev. 5, behoben). Der von der Gegenprüfung benannte Kandidat
  Bastl 2020 [53] wurde im Volltext geprüft: die Studie vergleicht
  Symptom-Score-Berechnungsmethoden und publiziert **keinen** Anteil symptomatischer
  Saisontage — \(f\) bleibt Annahme mit Band und Ersetzungspfad (PHD-Tagesdaten).
  **Entlastung:** \(f\) kürzt sich im €-Pfad vollständig heraus (§3.5) und wirkt nur auf
  den nativen ΔTage-Ausweis: am Band 0,50–0,85 um −28,6 % bis +21,4 % (0,50 / 0,70 und 0,85 / 0,70).
- **\(p_B\) = 0,55 (0,4–0,7), \(p_G\) = 0,75 (0,6–0,85) — gekennzeichnete Abschätzung**
  (Log 8; Rev.-5-Befund 36a): benötigt wird der Anteil der AR-Patienten mit
  Birkengruppen- bzw. Gräser-relevanter Saison; publiziert sind nur
  Bevölkerungs-Sensibilisierungen (Haftenberger [3]: Gräserpollen 19,4 %, Birke 17,4 %,
  Erle 16,5 %, Hasel 16,2 % — Rangfolge Gräser > Birkengruppe konsistent zur Setzung).
  Sensitivität (Region Mitte, \(p_B \Delta S_B + p_G \Delta S_G\) = 5,37 Tage): \(p_B\) 0,4–0,7 verschiebt
  \(\delta\) um −11,7 % bis +11,7 % (±0,15 × 4,20 = ±0,63 Tage), \(p_G\) 0,6–0,85 um −11,4 % bis +7,6 %
  (−0,15 × 4,08 = −0,612 Tage, +0,10 × 4,08 = +0,408 Tage), zusammen −23 % bis +19 % (Kap. 1, Absatz „Warum die eigene Quellenlage …“).
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
  (0,84 × 0,4 = 0,34 … 1,21 × 0,8 = 0,97, gerundet). Die **Kommunensumme** ist im Ausgangsstand gegen \(\lambda\)
  invariant (Ḡ₀-Gewichtung §3.3) — dort wirkt die Lesart nur innerhalb der
  Kommune verteilend. Die Senkung durch eine Maßnahme ist dagegen proportional zu
  \(\lambda\) (§5); \(\lambda\) ist dort als Anteil der örtlichen Quellen an der Pollenlast
  gelesen, belegt mit Hugg 2017 [74] (Log 26, Modellgrenze 7). Richtung unabhängig
  gestützt durch den Symptomgradienten Zentrum→Peripherie [55] und die
  Lidar-Birkendichte-Kopplung [56].
- **Altersinvarianz (explizite §3.2-Annahme; Befund 109):** \(f\), \(p_B/p_G\) und
  \(\lambda\) sind **altersinvariant** angesetzt („gleiche relative Elastizität über
  alle Bänder"; Elastizität heißt: um wie viel Prozent sich eine Größe ändert, wenn sich eine andere um ein Prozent ändert); real sind Sensibilisierungsprofile altersabhängig — die Bänder decken
  diese Streuung, das absolute Altersmuster entsteht über \(p_{\text{AR},a}\)
  (für \(c_{\text{Tag}}\) ist die bandeinheitliche Vereinfachung in §3.5 dokumentiert).

### 3.5 Monetarisierung (K1) und Aggregation (Anker `#c-tag`, `#d-saison`)

$$ \text{€}_{\text{Zelle}} \;=\; \Delta\text{Tage}_{\text{Zelle}} \cdot c_{\text{Tag}}, \qquad c_{\text{Tag}} = \frac{c_{\text{Jahr,direkt}}}{d_{\text{Saison}}}, \qquad d_{\text{Saison}} = f \cdot \bigl( p_B L_B + p_G L_G \bigr), \qquad \text{Kommune} = \sum_{\text{Zellen}} $$

- **\(c_{\text{Jahr,direkt}}\) = 266,90 €** (Preisstand 2024; Log 9): TOTALL [65] —
  bevölkerungsbasierte Stichprobe (Schweden, 18–65, alle Schweregrade): direkte Kosten
  **210,3 €** je Betroffenem·Jahr (Preisstand Feb. 2014, CPI-adjustiert laut Studie);
  Indexierung ×119,3/94,0 = ×1,2691 ⇒ 266,90 € (Preisstand 2024). Raumtransfer Schweden→Deutschland 1:1
  als dokumentierte Annahme (vergleichbare Preisniveaus; ohne Kaufkraft-Korrektur — Band).
  **Warum nicht Schramm als Basis:** Schramm [7] misst **moderate–schwere**, fachärztlich
  behandelte SAR (Erwachsene direkt: 42 % × 1.543 = 648,1 €₂₀₀₀ ⇒ ×119,3/75,9 = **1.018,6
  €** (Preisstand 2024); Kinder 60–78 % × 1.089 ⇒ 1.027–1.335 €, Preisstand 2024) — auf **alle** 12-Monats-
  diagnostizierten Betroffenen angewendet wäre das eine bekannte Überschätzung um grob
  Faktor 4 und würde die Untergrenzen-Zusage verletzen (dieselbe Logik wie #95-Befund 62).
  Schramm bildet daher die **Obergrenze** des \(c_{\text{Tag}}\)-Bands und das Kinder-Band. Die
  gewählte Basis 266,90 € liegt damit 74 % unter der Schramm-Kette (266,90 / 1.018,6 − 1 = −73,8 %).
- **\(d_{\text{Saison}}\) = 0,70 × (0,55·30 + 0,75·60) = 43,05 Tage** je Betroffenem und
  Referenzsaison (Saisonlängen \(L_B\) = 30 (20–45), \(L_G\) = 60 (45–80) Tage — **gekennzeichnete
  Abschätzungen** (§3.9) typischer deutscher Saisonfenster **nach dem** EAACI-Saisonkriterium
  aus Pfaar 2017 [51]; die Quelle definiert das Kriterium (Pollenschwellen), publiziert
  aber keine festen Längenwerte — Bänder decken die Spannweite; Befund 111). Die additive Form zählt bei Doppelt-Sensibilisierten
  überlappende Mai-Wochen doppelt ⇒ \(d_{\text{Saison}}\) eher **überzeichnet** ⇒
  \(c_{\text{Tag}}\) eher **unterschätzt** ⇒ €-Pfad konservativ (Rev.-5-Befund 36b,
  dokumentiert statt korrigiert).
- **\(c_{\text{Tag}}\) = 266,90 / 43,05 = 6,20 € je Tag** (Preisstand 2024; Band 6,20–23,66; Obergrenze =
  Schramm-Kette 1.018,6/43,05). Einheitlich über alle Altersbänder (Vereinfachung
  dokumentiert; Kinder-Schramm-Band liegt innerhalb der Obergrenze).
  **Produktverankerung:** Maßgeblicher Produktwert ist
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
pB, pG, LB, LG, a, c = 0.55, 0.75, 30, 60, 0.27, 266.90
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
# Betroffene ~107,4; Delta-Tage ~109; EUR ~676/Jahr
pbar = 10.74 / 100          # gewichtete Bundes-Praevalenz (§3.2)
b = 1000 * pbar
delta_mitte = 0.70 * (0.55*4.20 + 0.75*4.08) * 0.27
dt = b * delta_mitte
assert abs(b - 107.4) < 0.1
assert abs(dt - 109.0) < 0.5
assert abs(dt * 6.20 - 676) < 5
```

### 3.6 Zeichentabelle (alphabetisch; §3.2-Form)

| Zeichen | Name | Einheit | Wert / Herkunft |
|---|---|---|---|
| \(a\) | Altersband u20 · 20–64 · 65–74 · 75–84 · 85+ (u20 neu; 20–64 = u65 − u20) | — | Zensus-Altersbänder + neue Ebene u20 (§3.2) |
| \(a_{\text{attr}}\) | klimaattribuierter Anteil des Saisontrends | — | **0,27** (Band 0,19–0,41; Abschätzung von KAP3: Mitte des IQR 19–35 % der Saisonlänge 1990–2018 aus den Schätzungen von 22 Klimamodellen; Interquartilsabstand erklärt in Kap. 2) [9]; register:96-W025-02 |
| \(B_{\text{Zelle}}\) | Betroffene (aktive allergische Rhinitis) der Zelle | Personen | berechnet (§3.2) |
| \(c_{\text{Jahr,direkt}}\) | direkte Behandlungskosten je Betroffenem und Jahr (populationsbasiert) | €₂₀₂₄ | **266,90** = 210,3 €₂₀₁₄ × 119,3/94,0 (Band bis 1.018,6 = Schramm-Kette; Kinder 1.027–1.335) [7,19,65]; register:96-K1-01/-02; herleitung:#c-tag |
| \(c_{\text{Tag}}\) | Behandlungskostensatz je Symptomtag | €₂₀₂₄/Tag | **6,20** = 266,90/43,05 (Band 6,20–23,66); herleitung:#c-tag |
| \(d_{\text{Saison}}\) | Symptomtage je Betroffenem und Referenzsaison | Tage | **43,05** = 0,70 × (0,55·30 + 0,75·60); additive Form €-konservativ (§3.5); herleitung:#d-saison |
| \(\delta_R\) | zusätzliche Symptomtage je Betroffenem und Jahr, Region R | Tage/Jahr | **1,09/1,01/1,14** (N/M/S; DE 1,07); berechnet (§3.3) |
| \(\Delta S_{B,R},\ \Delta S_{G,R}\) | gemessene Saison-Spreizung Birkengruppe/Gräser je Region (1961–90 → 1991–2020) | Tage | 3,96/4,20/5,94 · 4,78/4,08/3,70 (N/M/S); `pollensaison_region.csv` [33,67]; register:96-W025-01; herleitung:#delta-s |
| \(\Delta\text{Tage}_{\text{Zelle}}\) | zusätzliche Symptomtage — **nativer Ausweis** | Tage/Jahr | Ergebnis |
| \(\text{€}_{\text{Zelle}}\) | bewerteter Schaden K1 (Ursache Allergene) — Teil-Ausweis | €₂₀₂₄/Jahr | Ergebnis = ΔTage × \(c_{\text{Tag}}\) (§3.5) |
| \(f\) | Anteil symptomatischer Saisontage | — | **0,70** (Band 0,50–0,85) — **Modellannahme** (§3.4; kürzt sich im €-Pfad); [52] nur qualitative Stütze; herleitung:#f-sympt |
| \(k_{\text{Birke},z},\ k_{\text{unbek},z}\) | Kronenflächenanteil der Zelle: sicher der Birkengruppe zugeordnet bzw. ohne Gattungs-Tag | — | OSM `natural=tree` mit `genus`/`species`/`taxon` (Betula/Alnus/Corylus/Carpinus) × Kronendurchmesser ÷ Zellfläche; Ebenen POLLEN_LOAD/CANOPY_BIRCH_FRACTION (§3.3); herleitung:#p-hat |
| \(\text{Grün}_z\) | Grün-/Wiesenflächenanteil der Zelle (Gräser-Proxy) | — | OSM-Landnutzung (vorhandene Produktgröße `green_frac`); herleitung:#p-hat |
| \(s_{\text{unbek}}\) | Birkengruppen-Anteil der Kronen **ohne** OSM-Gattungs-Tag | — | **0,12** (Band 0,05–0,25) — **§3.9 ABGESCHÄTZT, keine Primärquelle**: Straßenbaumkataster sind kommunal und nicht keyless aggregierbar; Begründung + gemessene Sensitivität in §3.3 (`#p-hat`). Wirkt im Ausgangsstand nur auf die Verteilung, nicht auf die Kommunensumme (Zentrierung auf Ḡ₀); herleitung:#p-hat |
| \(w_B\) | Gewicht der Gehölz-Komponente in \(\hat G\) (Gräser: \(1-w_B\)) | — | **0,464** = \(p_B\Delta S_{B,\text{DE}}/(p_B\Delta S_{B,\text{DE}} + p_G\Delta S_{G,\text{DE}})\) = 2,6345/5,6795 = 0,46386 (auf 3 NK gerundet); **Definitionskonstante der Ebene, kein Registry-Parameter** (`POLLEN_G_WEIGHT_BIRKE`) — zur Laufzeit unveränderlich, damit Schicht-B-Parameter den Schicht-A-Hazard nicht bewegen; die Kopplung an \(p_B\)/\(p_G\)/\(\Delta S_{\text{DE}}\) ist testgebunden (§3.9); herleitung:#p-hat |
| \(\hat G_{\text{Zelle}}/\bar G_0\) | Anteil allergener Vegetation, normiert auf das **Kommunenmittel im Ausgangsstand** (Ebene POLLEN_LOAD) | — | OSM-Gehölz-/Grünstruktur; \(\bar G_0\) (Ḡ₀) = betroffenengewichtetes Mittel der **eigenen Kommune** im Ausgangsstand ohne die bewerteten Maßnahmen, für jedes Maßnahmenszenario festgehalten ⇒ Mittel = 1 im Ausgangsstand per Konstruktion (§3.3, Log 18, 26); herleitung:#p-hat |
| \(J\) | Jultag des Phaseneintritts (DWD-Phänologie) | Tag | DWD-CDC Jahresmelder [33] |
| \(L_B,\ L_G\) | Saisonlänge Birkengruppe/Gräser (nach EAACI-Kriterium) | Tage | **30** (20–45) / **60** (45–80) — gekennzeichnete Abschätzung §3.5 [51]; herleitung:#d-saison |
| \(\lambda\) | Gewicht der lokalen Vegetations-Modulation | — | **0,7** (0,3–1,0) = \(2(R-1)/(R+1)\) × \(a_{\text{veg}}\) — Kette §3.4 (Lesart dokumentiert), gekennzeichnete Abschätzung [54–56]; register:96-W024-01; herleitung:#lambda-veg |
| \(p_{\text{AR},a}\) | 12-Monats-Prävalenz allergische Rhinitis je Band | — | **8,8/13,2/6,7/5,0/5,0 %** (u20/20–64/65–74/75–84/85+); Gewichtung §3.2 [1,2,48]; register:96-R35-01; herleitung:#p-ar |
| \(p_B,\ p_G\) | Anteil der AR-Patienten mit Birkengruppen-/Gräser-Saison | — | **0,55** (0,4–0,7) / **0,75** (0,6–0,85) — gekennzeichnete Abschätzung (§3.4) [3]; register:96-R35-02; herleitung:#p-sens |
| \(\hat P_{\text{Zelle}}\) | lokaler Pollen-Hazard-Faktor (auf die **Kommune** zentriert; in ΔTage **und** €) | — | \(1+\lambda(\hat G/\bar G_0 - 1)\); Spanne bei \(\hat G/\bar G_0\) = 0,5…1,5: 0,65…1,35; Kommunensumme im Ausgangsstand gleich \(\sum B\), mit Maßnahme kleiner (§3.3, §5); ohne Kommunen-Referenz \(\hat P \equiv 1\) (§3.3); berechnet |
| \(\text{pop}_a\) | Bevölkerung der Zelle je Band | Personen | Zensus 2022, 100 m (+ Ebene u20 neu); register:96-R35-01 |
| \(r_{\text{S158}}\) | Wirkungsfaktor der Pollen-Frühwarnung **je gewarntem Tag** (**nur Maßnahmen-Modul**, nicht im Basiswert) | — | **0,03** (Band 0,005–0,10) = \(q_{\text{reich}} q_{\text{handel}} e_{\text{Tag}}\) = 0,35·0,40·0,20 — **§3.9 ABGESCHÄTZT, keine Primärquelle** (Vorgabe P2); Kette, Bandenden und Sensitivität in §5.1; register:96-S158-01; herleitung:#s158-wirkung |
| \(t_{\text{warn},g}\) | Anteil der zusätzlichen Symptomtage der Pollengruppe \(g\) (B, G), an denen der DWD-Index mindestens „mittel“ meldet (gewarnte Tage; nur Maßnahmen-Modul; nicht zu verwechseln mit dem Ĝ-Gewicht \(w_B\)) | — | **0,75** (Band 0,50–1,00), beide Gruppen — **§3.9 ABGESCHÄTZT**; Schwelle nach DWD [70], Ersetzungspfad \(\min(1;\ m_{g,V}/f)\) aus [71]; herleitung:#s158-wirkung |
| \(m_{g,V}\) | Anteil **aller** Tage der Dekaden mit Zusatztagen, an denen der DWD-Index der Gruppe \(g\) im DWD-Gebiet \(V\) mindestens „mittel“ meldet (nur Ersetzungspfad von \(t_{\text{warn}}\)) | — | im Bericht nicht ausgewertet; Quelle DWD-Pollenflugstatistik [71]; wird über \(m_{g,V}/f\) umgerechnet, nie direkt eingesetzt; herleitung:#s158-wirkung |
| \(V\) | Gebiet des DWD-Pollenflug-Gefahrenindex (12 Gebiete mit 27 Vorhersageflächen [72]), für das [71] den Anteil ausweist; **nicht** die Modellregion \(R\) (Nord/Mitte/Süd, §3.3). Jedes Gebiet liegt in genau einer Modellregion | — | Zuordnung Zelle → DWD-Gebiet über das Bundesland (und das Teilgebiet) der Zelle; herleitung:#s158-wirkung |
| \(A_{\text{Zelle}}\) | Geltungsbereich der Pollen-Frühwarnung: Anteil der Zellfläche im Gebiet der kommunalen Warnkanäle, von 0 (außerhalb) bis 1 (ganz im Gebiet); im Maßnahmen-Modul der Deckungsgrad der Zelle durch die Geometrie der Maßnahme (Befund 232) | — | Eingabe des Nutzers, kein Parameter; herleitung:#s158-wirkung |
| \(\delta_B,\ \delta_G\) | Zusatztage je Betroffenem der Birkengruppe bzw. der Gräser, \(\delta_B + \delta_G = \delta_R\) | Tage/(Betroffener·Jahr) | Teilung von \(\delta_R\) nach den beiden Summanden (§3.3); Berlin 0,43659 / 0,57834 (\(a_{\text{attr}}\) = 0,27); herleitung:#s158-wirkung |

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
amtliche Anker-Zeitreihe**, an die ein Faktor für das Niveau angepasst (gefittet) werden könnte; die
Bundesregierung bestätigt, dass J30-scharfe Krankheitskosten nicht vorliegen
(BT-Drs. 19/22797, Antwort zu Frage 5 [66]). Das Modell ist stattdessen vollständig
messungs- und prävalenzverankert: \(\Delta S\) amtlich gemessen (DWD), \(p_{\text{AR}}\)
amtlicher Survey (RKI), \(c_{\text{Jahr}}\) populationsbasiert [65]. **Kalibriermodell =
Produktionsmodell** ist trivial erfüllt (lineares Modell ohne Fit-Schritt; kein
Näherungslauf involviert).

**Sanity-Bänder (Unter- und Obergrenze; Rev.-5-Befund 49):**

- **Physisch (native Größe):** Untergrenze > 0 ist **messfest**: \(\Delta S_B\) DE
  = +4,79 Tage (SE 0,23; 1.083 Stationen), \(\Delta S_G\) = +4,06 (SE 0,18; SE ist der
  Standardfehler des Mittels, §3.1). Beide Mittel liegen mehr als 20 Standardfehler über null
  (4,79 ÷ 0,23 ≈ 21; 4,06 ÷ 0,18 ≈ 23). Schon ab etwa zwei Standardfehlern gilt ein Mittel
  üblicherweise als nicht zufällig von null verschieden; ein Zufallsergebnis ist hier damit praktisch
  ausgeschlossen. \(\delta\)-Band aus dem Band des Klimaanteils \(a_{\text{attr}}\) (0,19–0,41, Kap. 2):
  0,76–1,63 Tage je Betroffenem·Jahr (Basis 1,07). **Größenordnung gegen [9], beim selben \(a_{\text{attr}}\)
  (Befund 258, Log 28):** [9] misst für Nordamerika 1990–2018 „lengthening of the pollen season by ∼8 d“
  (Results and Discussion, Absatz zu Abb. 1); der Klimaanteil daran ist 8 Tage × \(a_{\text{attr}}\). Das Modell setzt je
  Betroffenem \(\delta\) = 0,70 × 5,6795 Tage × \(a_{\text{attr}}\) = 3,98 Tage × \(a_{\text{attr}}\) an. Der Anteil steht auf beiden
  Seiten und kürzt sich: 3,98 Tage liegen unter 8 Tagen, also liegt \(\delta\) bei jedem \(a_{\text{attr}}\) darunter, bei
  rund der Hälfte. Am Basiswert 0,27 sind es 1,07 gegen 2,16 Tage, über das Band 0,76–1,63 Tage gegen
  1,52–3,28 Tage. Das prüft nur die Größenordnung: Die 8 Tage gelten der ganzen Saison in Nordamerika,
  \(\delta\) den Beschwerdetagen eines Betroffenen in Deutschland (mit \(f\) = 0,70 und den Anteilen \(p_B\), \(p_G\) < 1).
  Ein Quotient \(\delta \div f\) wird deshalb nicht gebildet.
- **Monetär:** Bundessumme = 8,96 Mio. Betroffene × 1,07 Tage × 6,20 € ≈ **60 Mio.
  € je Jahr** (Preisstand 2024; 9,62 Mio. Symptomtage; Band ≈ 42–91 Mio. € über das Band des Klimaanteils
  0,19–0,41; obere \(c_{\text{Tag}}\)-Sensitivität 23,66 € ⇒ ≈ 228 Mio. €). **Anteil an den Behandlungskosten,
  beim selben \(a_{\text{attr}}\) wie oben:** \(\delta/d_{\text{Saison}}\) = 1,07/43,05 = **2,5 %**. Er zerlegt sich wie der
  physische Vergleich: \(\delta/d_{\text{Saison}} = (\sum p\,\Delta S \div \sum p\,L) \times a_{\text{attr}}\) =
  (5,6795 ÷ 61,5) × 0,27, also 9,2 % Saisonverlängerung im Modell mal Klimaanteil. Einen belegten Wert für die
  Verlängerung als Anteil der Saison, gegen den die 9,2 % zu stellen wären, gibt es nicht: [9] nennt rund 8 Tage,
  aber keine mittlere Saisonlänge (gelesen: Significance, Abstract, Einleitung, Results and Discussion, Methods),
  [6] beschreibt die
  Verlängerung ohne Zahl. Der Vergleich ist deshalb **kein Prüfstein**. Zur Einordnung das Ergebnis der früheren
  M0-Herleitung (Anteil der Saisonverschiebung 0,15–0,25 mal Attribution): Ihre untere Grenze
  0,15 × 0,19 = 2,85 %, also ≈ 2,9 %, liegt knapp über den 2,5 % des Modells. Das Modell liegt damit eher zu
  niedrig, in derselben Richtung wie die Aussage in §3.5, der Euro-Betrag sei eine Untergrenze. Das Band jener
  Herleitung war keine publizierte Spanne und entfällt, weil Log 2 den Anteil der Saisonverschiebung als nicht
  hergeleitet verwirft (Log 28). Kein Parameter ist geändert, um einen Vergleich zu bestehen, und kein Band
  geweitet (Aufgabe §5). **Getrennt davon die amtlichen Rahmen:** Bundessumme ≪ Krankheitskosten des J-Kapitels (16,5 Mrd. €, KKR 2015 [66]) und
  deutlich unter dem Asthma-Vergleichswert (1,9 Mrd. €, KKR 2015 [66]). Eine amtliche
  **J30-Untergrenze existiert nicht** — dokumentierte Datenlücke mit Beleg [66]
  (Ersetzungspfad: exakte J30-Beträge aus GENESIS 23631/GBE-Bund interaktiv ziehen,
  Registry-Vermerk).
- **Impliziter Baseline-Check:** Betroffene × \(c_{\text{Jahr,direkt}}\) = 8,96 Mio. ×
  266,90 € ≈ 2,39 Mrd. € (Preisstand 2024) als implizite AR-Behandlungskosten-Basis — plausible
  Größenordnung zwischen Asthma-KKR (1,9 Mrd. [66]) und J-Kapitel (16,5 Mrd. [66]);
  mit der Schramm-Obergrenze wären es 9,1 Mrd. — erkennbar zu hoch, bestätigt die
  Basiswert-Wahl (Log 9).

```python test: beispiel_96_bundessumme
betroffene = 8_959_105          # §3.2-Konvention: gerundete Band-p (verbindliche Produktwerte)
a_attr     = 0.27                                    # Kap. 7 pollen.a_attr (Befund 258)
gew_de     = 0.55*4.79 + 0.75*4.06
delta_de   = 0.70 * gew_de * a_attr
dt = betroffene * delta_de
assert abs(delta_de - 1.073) < 0.002
assert abs(dt / 1e6 - 9.62) < 0.01                   # 9,62 Mio Symptomtage/Jahr
assert abs(dt * 6.20 / 1e6 - 60) < 1                 # ~60 Mio EUR_2024/Jahr
assert abs(dt * 6.20 * 0.19 / a_attr / 1e6 - 42) < 1 and abs(dt * 6.20 * 0.41 / a_attr / 1e6 - 91) < 1
assert abs(dt * 23.66 / 1e6 - 228) < 1               # obere c_Tag-Sensitivitaet
# (a) physisch beim selben a_attr: 0,70 x 5,6795 = 3,98 Tage x a_attr gegen 8 Tage x a_attr [9]
assert abs(0.70 * gew_de - 3.98) < 0.005 and 0.70 * gew_de < 8
assert abs(8 * a_attr - 2.16) < 1e-9 and abs(delta_de - 1.07) < 0.005
assert (round(0.70 * gew_de * 0.19, 2), round(0.70 * gew_de * 0.41, 2)) == (0.76, 1.63)
assert (round(8 * 0.19, 2), round(8 * 0.41, 2)) == (1.52, 3.28)
# (b) monetaer: delta / d_Saison = (Summe p dS / Summe p L) x a_attr; kein Pruefstein ohne belegten Wert
d_saison = 0.70 * (0.55*30 + 0.75*60)
assert abs(delta_de / d_saison - gew_de / 61.5 * a_attr) < 1e-12
assert abs(gew_de / 61.5 * 100 - 9.2) < 0.05          # 9,2 % Saisonverlaengerung im Modell
assert abs(delta_de / d_saison * 100 - 2.5) < 0.05    # impliziter Klimaanteil 2,5 %
assert abs(0.15 * 0.19 - 0.0285) < 1e-12              # untere Grenze der M0-Herleitung, ~2,9 %
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
  Regionale Streuung der \(\Delta S\)-Werte: \(\Delta S_B\) −17 % bis +24 %, \(\Delta S_G\)
  −9 % bis +18 % um das Bundesmittel; \(\delta\) je Region nur −5 % bis +6 % (1,01–1,14
  gegen 1,07) —
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
  \(\hat G_{\text{Zelle}}\) — multiplikativ via \(\hat P = 1+\lambda(\hat G/\bar G_0-1)\)
  auf ΔTage **und** € (zellscharf; Bezugswert Ḡ₀ aus dem Ausgangsstand festgehalten, §3.3,
  Log 26). **Die Eingabe ist die Änderung des Kronenanteils der Birkengruppe**, nicht eine
  anteilige Senkung von \(\hat G\): Nach der Ebenendefinition (§3.3) ist
  \(\hat G\) = 0,464 × (Kronenanteil mit Gattungs-Tag der Birkengruppe + 0,12 × Kronenanteil ohne
  Gattungs-Tag) + 0,536 × Grünanteil, also \(\hat G_z = w_B\,[k_{\text{Birke},z} +
  s_{\text{unbek}}\,k_{\text{unbek},z}] + (1-w_B)\,\text{Grün}_z\) mit \(w_B\) = 0,464 und
  \(s_{\text{unbek}}\) = 0,12. Ein Austausch allergener Bäume senkt nur den Kronen-Summanden, und
  zwar **in dem Term, in dem die ersetzten Kronen im Ausgangsstand stehen**:
  \(\Delta\hat G = -0{,}464 \cdot (\Delta k_{\text{Birke}} + 0{,}12 \cdot \Delta k_{\text{unbek}})\).
  Kronen mit Gattungs-Tag der Birkengruppe zählen voll, Kronen ohne Gattungs-Tag (in OSM der
  Regelfall) nur mit 0,12, so wie der Ausgangsstand sie gezählt hat. Der Grünanteil (Gräser)
  bleibt. **Grenze je Term (Befund 248):** Ersetzt werden kann höchstens, was in einem Term steht,
  \(\Delta k_{\text{Birke}} \le k_{\text{Birke}}\) und \(\Delta k_{\text{unbek}} \le k_{\text{unbek}}\).
  Daraus folgt, dass die Senkung höchstens so groß ist wie der Kronen-Summand im Ausgangsstand,
  also \(\hat G' \ge 0{,}536 \times\) Grünanteil; der Beitrag der Gehölze sinkt nie unter null. Eine
  Grenze nur für den ganzen Kronen-Summanden ergibt, solange jede Senkung in ihrem Term bleibt,
  dieselbe Zahl (gemessen am Produktcode, Befund 248). Sie ließe aber zu, dass zu viel ersetzte Kronen
  des einen Terms im anderen abgezogen werden, etwa Kronen mit Gattungs-Tag, die es nicht gibt.
  **Der Boden 0,536 × Grünanteil ist kein eigener Parameter (Befund 249):** 0,536 = 1 − \(w_B\) ist
  die Definitionskonstante der Ebene (§3.3), der Grünanteil ist die Zelleingabe. Das Produkt hält
  den Boden zusätzlich direkt. Er greift dort in zwei Fällen: wenn das gespeicherte \(\hat G\) durch
  die Rundung auf fünf Stellen um höchstens 0,000005 neben seinen Kronentermen liegt (gemessen
  höchstens 0,000004, an der Allee-Zelle unten weniger als 0,01 Tage), und wenn ein älterer Ausgangslauf
  \(s_{\text{unbek}}\) nicht je Zelle trägt, die Kommune den Wert danach erhöht hat und die ersetzten Kronen groß genug sind.
  Dann rechnet die Senkung mit dem neuen Wert, \(\hat G\) mit dem alten (Absatz „Vorgabe für das Produkt (Befund 230)“
  unten, Befund 252), und der Boden greift, sobald die Senkung den Kronen-Summanden des alten \(\hat G\) übersteigt. In einer Zelle nur mit Kronen ohne Gattungs-Tag und bei einer Erhöhung von 0,12 auf 0,25 ist das der Fall, wenn mehr als 0,12/0,25 = 0,48 ihrer Kronen ersetzt werden. Ein gesenkter Wert löst ihn nie aus. Der Boden verdeckt den gemischten Stand nur; behoben ist dieser erst mit einem neuen Zelllauf.
  Kennt die Kommune die Gattungen ihrer Bäume selbst (Baumkataster), gehen diese Angaben schon in
  den Ausgangsstand und in Ḡ₀ ein, nicht erst in das Maßnahmenszenario; sonst würde die Senkung
  an Kronen gerechnet, die der Ausgangsstand nur mit 0,12 kennt. Die Effektgröße ist damit
  **mechanisch**: Sinkt \(\hat G/\bar G_0\) einer Zelle so um 0,2, sinkt \(\hat P\) **dieser Zelle** um
  \(\lambda \times 0{,}2\) = 0,14 (Band 0,06–0,20 über das λ-Band 0,3–1,0); in einer Zelle mit
  \(\hat P\) = 1 sind das 14 % ihrer Zusatztage. Dafür braucht es 0,2 × Ḡ₀ / 0,464 weniger
  Kronenanteil mit Gattungs-Tag der Birkengruppe in der Zelle; bei Ḡ₀ = 0,18125 (Rechenbeispiel
  unten) sind das 0,078, also 7,8 Pp. weniger Kronenfläche. Artenwahl nach GALK-/allergologischer
  Liste [6].
  **Abschätzung am Zahlenbeispiel (§3.9 ABGESCHÄTZT, Log 24):** Eine Allee-Zelle in Berlin mit
  100 Betroffenen und \(\hat G/\bar G_0\) = 2 hat \(\hat P\) = 1,7 und 100 × 1,01493 × 1,7 = 172,5
  Zusatztage; nach der Pflanzung (Kronenanteil mit Gattungs-Tag der Birkengruppe um
  0,2 × Ḡ₀ / 0,464 gesenkt; bei Ḡ₀ = 0,18125 der Beispielkommune wären das 0,078, das Ḡ₀ Berlins
  weist der Bericht nicht aus) ist \(\hat G/\bar G_0\) = 1,8, \(\hat P\) = 1,56, also 158,3 Tage.
  **Wirkung: −14,2 Tage je Jahr (−8,2 %), ≈ 88 € je Jahr** (\(c_{\text{Tag}}\) = 6,20 €); Band über
  λ: −6,1 Tage (λ = 0,3) bis −20,3 Tage (λ = 1,0). **Sensitivität:** linear in λ und in der
  Senkung des Kronenanteils; stärkster Treiber ist λ (Faktor 3,3 zwischen den Bandenden).
  **Wirkungsort:** ausschließlich über \(\hat G\) der Zelle, die im Zelllauf neu berechnet wird.
  **Wirkung auf die Kommunensumme (Rev. 4, Log 26; Log 19 verworfen):** Weil Ḡ₀ festgehalten
  wird, ändern sich die übrigen Zellen nicht. Die Kommunensumme sinkt um genau die Senkung in den
  bepflanzten Zellen, \(\lambda \cdot \sum B\,(\hat G - \hat G')/\bar G_0\) Betroffene (§3.3), mal
  \(\delta_R\) in Tagen. Die Berliner Allee-Zelle oben senkt die Summe Berlins also um 14,2 Tage und
  ≈ 88 € je Jahr; die Tage verteilen sich nicht auf andere Zellen. Unter der früheren Regel
  (Ḡ in jedem Lauf neu gebildet, Log 19) stimmte die Aussage nicht, eine solche Pflanzung senke
  die Summe der Kommune; mit festgehaltenem Ḡ₀ stimmt sie.
  **Toleranz der Allee-Zelle (Befund 250):** ± 0,05 Tage und ± 0,5 €, die halbe Einheit der
  letzten genannten Stelle; so bindet auch der Golden-Test des Produkts die Zelle. Block
  `beispiel_96_stadtbaum_allee` unten rechnet sie nach.

  **Modellgrenze: \(s_{\text{unbek}}\) gilt für die ganze Kommune (Befund 246).** Das Produkt liest
  kein Baumkataster je Zelle ein. Kronen ohne Gattungs-Tag zählen deshalb in jeder Zelle mit
  demselben \(s_{\text{unbek}}\) = 0,12. Liegt der wahre Anteil der Birkengruppe an diesen Kronen in
  einer Zelle höher, rechnet das Produkt dort Zusatztage und Senkung zu klein, liegt er niedriger, zu
  groß. **Richtung:** Nach den Ankern von \(s_{\text{unbek}}\) (§3.3) liegen Straßenbäume am unteren
  Bandende (0,05), Parks und Gehölze mit Hasel und Hainbuche am oberen (0,25). Für eine Allee aus
  Straßenbäumen ohne Gattungs-Tag rechnet das Produkt also eher zu viel Last und zu viel Senkung.
  Vegetationsarme Zellen führen kaum Kronen; ihr \(\hat G/\bar G_0\) ändert sich über das ganze Band
  um weniger als 1 % (§3.3: +0,9 %). Im Ausgangsstand bleibt die Kommunensumme gleich: Was die
  Allee-Zellen zu viel tragen, fehlt über ein höheres Ḡ₀ den übrigen Zellen, auch den
  vegetationsarmen. Mit einer Maßnahme gibt es diesen Ausgleich nicht, der Fehler der Senkung bleibt
  ganz stehen. **Größe an der Allee-Zelle:** Die Allee-Zelle oben führt ihre Kronen mit
  Gattungs-Tag; \(s_{\text{unbek}}\) geht dort nicht ein, der Fehler ist null. Stehen dieselben
  Kronen (Kronenanteil 0,3625) in OSM ohne Gattungs-Tag, wie meist, rechnet das Produkt mit 0,12:
  \(\hat G\) = 0,2145, 114,5 Zusatztage im Ausgangsstand und 1,71 vermiedene Tage (≈ 10,57 € je Jahr)
  für dieselbe Pflanzung. Mit einem Wert für diese Zelle wären es bei 0,05 109,9 und 0,71 Tage
  (≈ 4,40 €), bei 0,25 123,1 und 3,55 Tage (≈ 22,02 €). Die Zusatztage liegen damit 4,2 % zu hoch
  bis 7,0 % zu niedrig, die vermiedenen Tage um den Faktor 2,4 zu hoch bis 2,08 zu niedrig; die
  Senkung ist linear in \(s_{\text{unbek}}\). Ḡ₀ bleibt dabei fest (Log 26); ein eigener Wert in nur
  einer Zelle bewegt Ḡ₀ ohnehin kaum, in Berlin (393.299 Betroffene, §3.0) um weniger als 0,00001.
  **Ersetzungspfad:** das Baumkataster der Kommune je Zelle im Ausgangsstand (§3.3).

```python test: beispiel_96_stadtbaum_allee
lam, delta, c_tag = 0.7, 1.01493, 6.20       # Kap. 7 pollen.lambda_veg, Ebene 6, Kap. 7 pollen.c_tag
w_b, g0, B = 0.464, 0.18125, 100            # Ebenendefinition §3.3, Ḡ₀ der Beispielkommune, Betroffene
tol_tage, tol_euro = 0.05, 0.5               # Toleranz der Allee-Zelle (Befund 250), wie der Golden-Test
k = 0.3625                                   # Kronenanteil mit Gattungs-Tag = Grünanteil der Allee-Zelle
g_vor = w_b * k + (1 - w_b) * k              # G^ im Ausgangsstand
assert abs(g_vor / g0 - 2.0) < 1e-12
dk = 0.2 * g0 / w_b                          # Senkung des Kronenanteils: G^/G0 sinkt um 0,2
a = dk / k                                   # Eingabe anteil_ersetzt im Produkt (0 bis 1)
assert abs(dk - 0.078125) < 1e-12 and 0 < a <= 1


def tage(g, l=lam):                          # Zusatztage der Zelle, G0 festgehalten
    return B * delta * (1 + l * (g / g0 - 1))


g_nach = g_vor - w_b * min(a * k, k)         # Grenze je Term (Befund 248)
assert abs(g_nach / g0 - 1.8) < 1e-12
assert abs(tage(g_vor) - 172.5) < tol_tage and abs(tage(g_nach) - 158.3) < tol_tage
senkung = tage(g_vor) - tage(g_nach)
assert abs(senkung - 14.2) < tol_tage and abs(senkung / tage(g_vor) - 0.082) < 0.0005
assert abs(senkung * c_tag - 88) < tol_euro
assert abs(tage(g_vor, 0.3) - tage(g_nach, 0.3) - 6.1) < tol_tage
assert abs(tage(g_vor, 1.0) - tage(g_nach, 1.0) - 20.3) < tol_tage
# Grenze je Term gegen Grenze fuer den ganzen Kronen-Summanden (Befund 248): im Bereich gleich
for x in (0.0, 0.25, 0.5, a, 1.0):
    assert w_b * min(x * k, k) == min(w_b * x * k, w_b * k)
# s_unbek kommunenweit (Befund 246): dieselben Kronen ohne Gattungs-Tag, dieselbe Pflanzung a
g_s = {s: w_b * s * k + (1 - w_b) * k for s in (0.05, 0.12, 0.25)}
vor = {s: tage(g) for s, g in g_s.items()}
verm = {s: tage(g) - tage(g - w_b * s * min(a * k, k)) for s, g in g_s.items()}
assert abs(g_s[0.12] - 0.2145) < 0.0001
assert abs(vor[0.12] - 114.5) < tol_tage and abs(vor[0.05] - 109.9) < tol_tage
assert abs(vor[0.25] - 123.1) < tol_tage
assert abs(verm[0.12] - 1.71) < 0.005 and abs(verm[0.05] - 0.71) < 0.005
assert abs(verm[0.25] - 3.55) < 0.005
assert abs(verm[0.12] * c_tag - 10.57) < 0.01 and abs(verm[0.05] * c_tag - 4.40) < 0.01
assert abs(verm[0.25] * c_tag - 22.02) < 0.01
assert abs(vor[0.12] / vor[0.05] - 1.042) < 0.0005     # Ausgangsstand 4,2 % zu hoch
assert abs(1 - vor[0.12] / vor[0.25] - 0.070) < 0.0005  # oder 7,0 % zu niedrig
assert abs(verm[0.12] / verm[0.05] - 2.4) < 0.005      # Senkung Faktor 2,4 zu hoch
assert abs(verm[0.25] / verm[0.12] - 2.08) < 0.005     # oder Faktor 2,08 zu niedrig
assert 100 / 393_299 * (g_s[0.25] - g_s[0.05]) < 1e-5  # Ḡ₀ Berlins bewegt sich kaum (§3.0)
# a ueber 1 (Befund 251): Produkt bildet a * Deckungsgrad * k und kappt dann je Term am Kronenanteil
def verm_a(x, deckung):
    return tage(g_vor) - tage(g_vor - w_b * min(x * deckung * k, k))


for x in (1.0, 1.5, 2.0):                              # voll gedeckt: zaehlt wie 1
    assert abs(verm_a(x, 1.0) - 65.9) < tol_tage
assert abs(verm_a(1.0, 0.5) - 33.0) < tol_tage          # halb gedeckt: a = 1
assert abs(verm_a(1.5, 0.5) - 49.4) < tol_tage          # a = 1,5 senkt mehr als a = 1
assert abs(verm_a(2.0, 0.5) - 65.9) < tol_tage         # a = 2,0 das Doppelte (1/Deckungsgrad)
assert abs(verm_a(2.0, 0.5) / verm_a(1.0, 0.5) - 1 / 0.5) < 1e-9
# s_unbek nach dem Ausgangslauf ueberschrieben, 0,12 -> 0,25 (Befund 252)
gemischt = tage(g_s[0.12]) - tage(g_s[0.12] - w_b * 0.25 * min(a * k, k))
assert abs(gemischt - 3.55) < 0.005 and abs(vor[0.12] - 114.5) < tol_tage
boden = (1 - w_b) * k                                  # Boden bei a = 1
assert abs(tage(g_s[0.12]) - tage(max(boden, g_s[0.12] - w_b * 0.25 * k)) - 7.91) < 0.005
assert abs(tage(g_s[0.25]) - tage(boden) - 16.48) < 0.005
# eine Eingabe a fuer Kronen mit und ohne Gattungs-Tag (Befund 247), gleiche ersetzte Kronenflaeche
kb = ku = 0.20
s = 0.12
produkt = w_b * (a * kb + s * a * ku)                  # Produkt: beide Terme um a
nur_mit_tag = w_b * a * (kb + ku)                      # nur Baeume mit Gattungs-Tag ersetzt
nur_ohne_tag = w_b * s * a * (kb + ku)                 # nur Baeume ohne Gattungs-Tag ersetzt
assert abs(produkt / nur_mit_tag - 0.56) < 1e-12
assert abs(produkt / nur_ohne_tag - 4.67) < 0.005
```

  **Rechenbeispiel Kommunensumme (§3.9 ABGESCHÄTZT; vier Zellen wie in Ebene 7, \(\delta_R\) =
  1,01493 Tage je Betroffenem aus Ebene 6, \(c_{\text{Tag}}\) = 6,20 € aus Kapitel 7
  `pollen.c_tag`, λ = 0,7 aus Kapitel 7 `pollen.lambda_veg`).** Eine Kommune hat vier bewohnte
  Zellen mit B = 1.000 / 4.000 / 2.500 / 500 Betroffenen und \(\hat G\) = 0 / 0,10 / 0,30 / 0,60.
  Zelle 3 (Grünanlage) hat den Kronenanteil mit Gattungs-Tag der Birkengruppe 0,30 und den
  Grünanteil 0,30, Zelle 4 (Park mit Birken) 0,60 und 0,60; Kronen ohne Gattungs-Tag gibt es im
  Beispiel nicht. Nach §3.3 ist das \(\hat G\) = 0,464 × 0,30 + 0,536 × 0,30 = 0,30
  und 0,464 × 0,60 + 0,536 × 0,60 = 0,60.

  | Schritt | Rechnung | Ergebnis |
  |---|---|---|
  | 1 Bezugswert im Ausgangsstand | Ḡ₀ = (1.000 × 0 + 4.000 × 0,10 + 2.500 × 0,30 + 500 × 0,60) / 8.000 = 1.450 / 8.000 | **Ḡ₀ = 0,18125** |
  | 2 \(\hat P\) vorher | 1 + 0,7 × (\(\hat G\)/0,18125 − 1) | 0,300 / 0,686 / 1,459 / 2,617 |
  | 3 Summe vorher | 300 + 2.745 + 3.647 + 1.309 | Σ B·P̂ = **8.000** = Σ B |
  | 4 Tage und Euro vorher | 8.000 × 1,01493; × 6,20 € | **8.119 Tage**, 50.341 € |
  | 5 Maßnahme | Zellen 3 und 4: ein Drittel der allergenen Bäume durch allergenarme Arten ersetzt, Kronenanteil der Birkengruppe 0,30 → 0,20 und 0,60 → 0,40, Grünanteil unverändert; \(\hat G'\) = 0,30 − 0,464 × 0,10 und 0,60 − 0,464 × 0,20 | \(\hat G'\) = 0,2536 und 0,5072; Ḡ₀ bleibt 0,18125 |
  | 6 \(\hat P\) nachher | 1 + 0,7 × (0,2536/0,18125 − 1); 1 + 0,7 × (0,5072/0,18125 − 1) | 1,279 und 2,259; Zellen 1 und 2 unverändert |
  | 7 Summe nachher | 300 + 2.745 + 3.199 + 1.129 | Σ B·P̂′ = **7.373** |
  | 8 Tage und Euro nachher | 7.372,8 × 1,01493; × 6,20 € | **7.483 Tage**, 46.394 € |
  | 9 Senkung | 8.119,44 − 7.482,88; Kontrolle: 0,7 × (2.500 × 0,0464 + 500 × 0,0928) / 0,18125 × 1,01493 | **−637 Tage je Jahr (−7,8 %), ≈ 3.950 € je Jahr** (Preisstand 2024) |

  **Sensitivität:** Die Senkung ist linear in λ und in der Summe \(\sum B\,(\hat G - \hat G')\);
  stärkster Treiber ist λ: bei λ = 0,3 sind es 273 Tage und ≈ 1.690 €, bei λ = 1,0 909 Tage
  und ≈ 5.640 €. **Was die einfachere Rechnung verfälschen würde:** Setzte man „ein Drittel der
  Bäume ersetzt“ gleich mit einem Drittel weniger \(\hat G\) (0,30 → 0,20, 0,60 → 0,40), sänke
  auch der Gräser-Anteil mit, und die Senkung wäre mit 1.372 Tagen mehr als doppelt so groß
  (Faktor 1 / 0,464). Stehen die ersetzten Bäume in OSM **ohne Gattungs-Tag**, kennt der
  Ausgangsstand sie nur mit 0,12 ihrer Kronenfläche. Zöge man trotzdem 0,464 × ΔKronenanteil voll
  ab, sänke \(\hat G\) bis zu 1 / 0,12 ≈ 8-mal stärker, als der Ausgangsstand den Bäumen
  zugeschrieben hat. Beispiel: Kronenanteil 0,30, alles ohne Tag, Senkung 0,10. Im Ausgangsstand
  tragen die Gehölze 0,464 × 0,12 × 0,30 = 0,017 zu \(\hat G\) bei; voll abgezogen würden 0,046,
  der Beitrag der Gehölze würde negativ. Richtig abgezogen werden 0,464 × 0,12 × 0,10 = 0,0056.
  **Gegenprobe zur verworfenen Regel (Log 19):** Bildete man Ḡ nach der Maßnahme neu,
  wäre es 1.287,6 / 8.000 = 0,16095, und die Summe läge wieder genau bei 8.000 — die Senkung wäre
  null, obwohl in zwei Zellen weniger allergene Bäume stehen. Auch ein **flächiges** Programm,
  das in allen Zellen ein Fünftel der allergenen Kronen mit Gattungs-Tag ersetzt, senkt jetzt die Summe, um
  λ × 0,464 × 0,2 × (betroffenengewichteter Kronenanteil) / Ḡ₀; sind Kronen- und Grünanteil im
  Mittel gleich groß und gibt es keine Kronen ohne Gattungs-Tag, sind das 0,7 × 0,464 × 0,2 = 6,5 %.
  Gibt es Kronen ohne Gattungs-Tag, ist Ḡ₀ um 0,464 × 0,12 × \(\bar k_{\text{unbek}}\) (betroffenengewichtetes Mittel von \(k_{\text{unbek},z}\), dem Kronenflächenanteil ohne Gattungs-Tag) größer, die
  Senkung kleiner, und 6,5 % sind eine Obergrenze. Gerechnet wird es trotzdem im Zelllauf
  über \(\hat G'\), nie als pauschaler Faktor (Integrationsauflage unten).

```python test: beispiel_96_stadtbaum_kommunensumme
lam, delta, c_tag = 0.7, 1.01493, 6.20       # Kap. 7 pollen.lambda_veg, Ebene 6, Kap. 7 pollen.c_tag
B = [1_000, 4_000, 2_500, 500]              # Betroffene je Zelle (wie Ebene 7)
G_vor = [0.00, 0.10, 0.30, 0.60]            # G^ im Ausgangsstand
w_b = 0.464                                  # Gewicht der Kronen in G^ (Ebenendefinition §3.3)
krone = [0.00, 0.00, 0.30, 0.60]             # Kronenanteil Birkengruppe (Zellen 3, 4)
gruen = [0.00, 0.00, 0.30, 0.60]             # Grünanteil (Zellen 3, 4)
for i in (2, 3):
    assert abs(w_b * krone[i] + (1 - w_b) * gruen[i] - G_vor[i]) < 1e-12
d_krone = [0.00, 0.00, -0.10, -0.20]         # ein Drittel der allergenen Kronen ersetzt
G_nach = [g + w_b * d for g, d in zip(G_vor, d_krone)]   # nur der Kronen-Summand sinkt
assert abs(G_nach[2] - 0.2536) < 1e-12 and abs(G_nach[3] - 0.5072) < 1e-12
g0 = sum(b * g for b, g in zip(B, G_vor)) / sum(B)   # Bezugswert im Ausgangsstand
assert abs(g0 - 0.18125) < 1e-12
p_vor = [1 + lam * (g / g0 - 1) for g in G_vor]
p_nach = [1 + lam * (g / g0 - 1) for g in G_nach]    # G0 festgehalten
s_vor = sum(b * p for b, p in zip(B, p_vor))
s_nach = sum(b * p for b, p in zip(B, p_nach))
assert abs(s_vor - sum(B)) < 1e-9          # Ausgangsstand: Summe B*P^ = Summe B
assert s_nach < s_vor                        # Maßnahme senkt die Kommunensumme
assert abs(s_nach - 7_372.8) < 0.01
tage_vor, tage_nach = s_vor * delta, s_nach * delta
assert abs(tage_vor - 8_119.4) < 0.5 and abs(tage_nach - 7_482.9) < 0.1
senkung = tage_vor - tage_nach
assert abs(senkung - 636.6) < 0.1 and abs(senkung / tage_vor - 0.078) < 0.001
assert abs(senkung - lam * sum(b * (v - n) for b, v, n in zip(B, G_vor, G_nach)) / g0 * delta) < 1e-6
assert abs(tage_vor * c_tag - 50_341) < 1 and abs(tage_nach * c_tag - 46_394) < 1
assert abs(senkung * c_tag - 3_947) < 5
k = senkung / lam
assert abs(k * 0.3 - 273) < 1 and abs(k * 1.0 - 909) < 1
assert abs(k * 0.3 * c_tag - 1_690) < 5 and abs(k * 1.0 * c_tag - 5_640) < 5
assert abs(senkung / w_b - 1371.9) < 0.1    # anteilige Senkung von G^ waere Faktor 1/w_b zu hoch
g_neu = sum(b * g for b, g in zip(B, G_nach)) / sum(B)   # verworfene Regel (Log 19)
assert abs(g_neu - 0.16095) < 1e-12
assert abs(sum(b * (1 + lam * (g / g_neu - 1)) for b, g in zip(B, G_nach)) - sum(B)) < 1e-9
assert abs(lam * w_b * 0.2 - 0.065) < 0.001   # flaechig ein Fuenftel der Kronen, Krone = Gruen
s_unbek, k_unbek, dk_unbek = 0.12, 0.30, -0.10   # Fall ohne Gattungs-Tag (Befund 195)
beitrag = w_b * s_unbek * k_unbek                # Beitrag der Gehoelze im Ausgangsstand
assert abs(beitrag - 0.0167) < 1e-4
assert beitrag + w_b * dk_unbek < 0              # voll abgezogen: Beitrag waere negativ
assert abs(w_b * s_unbek * dk_unbek + 0.0056) < 1e-4   # richtig: nur im Term s_unbek
assert beitrag + w_b * s_unbek * dk_unbek >= 0   # Grenze: Beitrag der Gehoelze nie unter null
```

  **Kosten der Stadtbaumwahl (Anker `#stadtbaum-kosten`, Befund 253, §3.9 ABGESCHÄTZT; Kap. 7
  `pollen.stadtbaum_kosten`).** Die Kosten wirken nicht auf den Schadensbetrag von #96, nur auf die
  Wirtschaftlichkeit der Maßnahme im Maßnahmen-Modul (Kosten der Kommune außerhalb der Schadenskonten,
  R7-Weiche unten). Gerechnet wird je ersetztem Baum, getrennt nach zwei Fällen:
  1. **Nachpflanzung ohnehin:** Der allergene Baum fällt ohnehin, etwa aus Alters- oder
     Verkehrssicherheitsgründen, und die Kommune pflanzt am selben Standort nach. Fällung, Pflanzung und
     Anwuchspflege fallen dann in jedem Fall an. Der Maßnahme zuzurechnen sind nur die **Mehrkosten der
     Artenwahl**: der Preisunterschied zwischen der allergenarmen Art und der Art, die sonst gepflanzt
     würde, in gleicher Pflanzqualität. Die Preisliste einer Baumschule [79] (gültig ab 14.02.2024,
     Laubbäume S. 26 f.) ordnet Hochstämme mit 18–20 cm Stammumfang vier Preisgruppen zu: I 395 €,
     II 455 €, III 485 €, IV 580 € je Stück. Hergeleitet wird der Punktwert aus zwei Fragen:
     *Welcher Baum wird ersetzt?* Ersetzt werden Bäume der Birkengruppe (Birke, Erle, Hasel, Hainbuche;
     §3.3). Unter den Straßenbäumen ist das vor allem die Birke: In Berlin ist sie die einzige Gattung der
     Gruppe unter den sieben Hauptgattungen, 12.209 von 432.769 Straßenbäumen (Stand 31.12.2021, [78],
     Anlage); in Hannover mussten Straßenbirken „auffällig häufig“ gefällt werden, 66 Stück, „über 10 %
     des Gesamtbestands“ ([82], S. 19). Die Hainbuche, in Hannover 4 % der Straßenbäume ([82], S. 9), und
     die Baumhasel gehören ebenfalls zur Birkengruppe; sie sind Bäume, die ersetzt werden, keine
     Ersatzarten. *Was wird stattdessen gepflanzt?* Am häufigsten die Linde: Sie ist die häufigste
     Straßenbaumgattung Berlins (35 %, [78], Anlage) und in Hannover die häufigste Art unter den
     1.054 jungen Straßenbäumen der Jahre 2023 und 2024 (184 Linden, [82], S. 10). Ihr allergenes
     Potenzial ist niedrig: Winterlinde und Sommerlinde stehen bei Cariñanos u. a. [81], Tab. 3, auf „Low“,
     ebenso die Robinie. Im Text schränkt [81] das ein (Abschnitt 4, Discussion): „Linden (Tilia spp.) is
     widely used in walk-alignments, so that its moderate allergenicity can be increased when forming dense
     groups“. In dichten Reihen kann die Linde also mäßig allergen wirken. Richtung für diesen Bericht:
     \(\hat G\) zählt nur Kronen der Birkengruppe und Grünflächen (§3.3), Lindenpollen gehen in die Rechnung
     nicht ein. Eine dichte Lindenreihe senkt die gerechneten Tage der Birkengruppe voll, bringt aber eine
     kleine eigene Pollenlast mit, die nicht gerechnet ist; der Nutzen der Stadtbaumwahl ist dort eher
     überzeichnet. Beziffern lässt sich das nicht, weil [81] keine Zahl dafür nennt. Die 60 € unten ändert
     das nicht, sie sind ein Preisunterschied. [81] ist in [6] als Nr. 104 zitiert; [6] selbst nennt keine Arten, sondern
     verweist auf die GALK-Liste der Zukunftsbäume und eine allergologische Liste (S. 100 f.). In [79]
     stehen Birke (Betula pendula) in Gruppe I, Hainbuche und Baumhasel in Gruppe II, Winterlinde
     ‚Greenspire‘, Sommerlinde und Robinie ‚Frisia‘ in Gruppe II, die Kugelakazie (Robinia
     ‚Umbraculifera‘) in Gruppe I. **Abschätzung von KAP3: 60 € je Baum (Preisstand 2024), Band 0–185 €.**
     Der Punktwert ist der typische Fall, eine Linde statt einer Birke: 455 € − 395 € = 60 €. 0 € gilt,
     wenn eine Linde eine Hainbuche oder Baumhasel ersetzt (beide Gruppe II) oder eine Kugelakazie eine
     Birke (beide Gruppe I); 185 € gilt, wenn statt einer Birke aus anderen Gründen eine Sorte der
     teuersten Gruppe IV gewählt wird (580 € − 395 €). Das sind weniger als 2 % der Pflanzkosten
     unten. Die Pflege des angewachsenen Baums setzt der Bericht für beide Arten gleich an, weil keine
     Quelle einen Unterschied belegt; das ist eine Grenze der Abschätzung. Welche Art allergenarm ist,
     bewerten die Listen nicht einheitlich; [81] nennt die Linde, und die Abschätzung legt die Art der
     Kommune nicht fest.
  2. **Vorgezogener Ersatz:** Ein gesunder allergener Baum wird gefällt, um ihn früher zu ersetzen. Dann
     trägt die Maßnahme alles, Fällung, Pflanzung und Anwuchspflege.
     **Pflanzung mit dreijähriger Anwuchspflege: 3.636 € je Baum (Preisstand 2024), Band 2.400–5.600 €.**
     Das sind Mittel und Spanne der Hamburger Straßenbaumpflanzungen 2024 [75]. Die Pflege ist darin
     enthalten: Die Fertigstellungs- und Entwicklungspflege ist „für in der Regel drei Jahre“ Teil der
     Pflanzkosten [77], Pflanzung und Pflege werden nicht getrennt ausgewiesen [76]. Gegenprobe
     Beispielkommune Berlin: rund 3.000 € brutto je Straßenbaum einschließlich einer rund dreijährigen
     Entwicklungspflege (Ausschreibung Herbst 2022) [78], mit dem VPI [19] auf 2024 gerechnet
     3.000 € × 119,3 / 110,2 = 3.248 €, im Band. Hamburg 2025: 3.120 € im Mittel [76].
     **Fällung: Abschätzung von KAP3, 800 € je Baum (Preisstand 2024), Band 400–1.600 €**, mit
     Verkehrssicherung, Abfuhr und Fräsen des Stubbens. Eine amtliche oder verbandliche Zahl je Baum fand
     sich in den durchsuchten Quellen nicht: Hamburg erhebt Fällkosten nicht gesondert, sie stecken in
     großen Ausschreibungen zusammen mit der Baumpflege ([77], S. 1). Durchsucht, ohne Fällkosten je Baum,
     wurden außerdem [75], [76], [78] und [82], die Seite des Bezirksamts Spandau zu Gehwegüberfahrten
     (Fällkosten nur als Posten des Leistungsbescheids), die Gebührenseite der Stadt Köln zur Fällung
     städtischer Bäume (nur Genehmigungsgebühren), die EU-Bekanntmachung eines Berliner Rahmenvertrags
     über Baumpflege und Fällung (nur ein Gesamtwert, kein Preis je Baum), die Richtwerte von GALK und SVK
     nach Methode Koch (nur Herstellungskosten der Pflanzung) und die Regelwerke der FLL zu Bäumen (keine
     frei zugänglichen Kostenkennwerte für Fällungen); Adressen in Befund 253. Die Bandenden sind deshalb aus den
     Arbeitsschritten gesetzt: 400 € für einen kleinen Baum im Sammelauftrag, ohne Hubarbeitsbühne und
     ohne eigene Sperrung, 1.600 € für einen großen Baum an der Fahrbahn, abgetragen von der
     Hubarbeitsbühne, mit Sperrung und Fräsen des Stubbens. Der Punktwert ist das geometrische Mittel
     der Bandenden, √(400 × 1.600) = 800 €: Das Band spannt den Faktor 4, und 800 € liegen von beiden
     Enden um den Faktor 2 entfernt. Das arithmetische Mittel, 1.000 €, läge ungleich näher am oberen
     Ende (Faktor 1,6) als am unteren (Faktor 2,5). Die Fällung wirkt nur auf den vorgezogenen Ersatz,
     um −9 … +18 % über ihr Band; auf die Nachpflanzung ohnehin wirkt sie nicht.
     **Zusammen: 4.436 € je Baum (Preisstand 2024), Band 2.800–7.200 €.** Die Bandenden sind addiert,
     gelten also für beide Enden zugleich. Die Fällung macht 18 % des Punktwerts aus.

  **Rechenbeispiel Allee-Zelle.** Die Pflanzung oben senkt den Kronenanteil der 100-m-Zelle
  (10.000 m²) um 0,078, also um 781 m² Kronenfläche. Das Produkt setzt für OSM-Bäume ohne Angabe
  einen Kronendurchmesser von 8 m an (`backend/app/services/climate/heat/osm_data.py`), also 50,3 m²
  Krone je Baum; 781 ÷ 50,3 ≈ 15,5, das sind 16 Bäume. Der Nutzen der Pflanzung oben beträgt 88 €
  vermiedene Behandlungskosten je Jahr (Band über λ 38–126 €), solange die Kronen der sonst stehenden
  Birken voll ausgebildet sind.
  - *Vorgezogener Ersatz:* 16 × 4.436 € ≈ 71.000 € einmalig (Band 44.800–115.200 €). Die gefällten
    Birken sind ausgewachsen, der Nutzen gilt also vom ersten Jahr an. Ohne Zins deckt er die Kosten
    erst nach über 800 Jahren. Über die Pollenallergie allein trägt sich ein vorgezogener Ersatz nicht,
    er braucht andere Gründe.
  - *Nachpflanzung ohnehin:* 16 × 60 € = 960 € (Band 0–2.960 €). Verglichen wird hier mit jungen Birken,
    die sonst gepflanzt würden. Ihre Kronen wachsen erst heran, so lange ist auch der Nutzen kleiner.
    Gerechnet ist das mit dem Kronenwachstum junger Straßenlinden in Reihen nach Larsen und
    Kristoffersen [80], Tab. 3: Kronenradius = 0,1358 × Alter − 0,0008 × Alter² (Meter, Jahre); ein
    Baum mit 18–20 cm Stammumfang ist bei der Pflanzung rund 10 Jahre alt ([80], S. 209). Der Radius
    wächst so von 1,28 m bei der Pflanzung auf 4 m, also die 8 m Kronendurchmesser des Produkts, nach
    28 Jahren. Der Nutzen je Jahr ist 88 € × (Radius ÷ 4 m)², höchstens 88 €: im 1. Jahr 11 €, im
    10. Jahr 32 €, im 20. Jahr 62 €. Aufsummiert sind die 960 € nach **24 Jahren** gedeckt. Mit voller
    Krone ab dem ersten Jahr wären es 11 Jahre; diese einfachere Rechnung zeigte die Amortisation also
    gut doppelt so früh. Band: 20 Jahre (λ = 1,0) bis 39 Jahre (λ = 0,3); mit 185 € je Baum 47 Jahre, mit
    185 € je Baum und λ = 0,3 zusammen 92 Jahre. *Über die Lebensdauer:* Ein Berliner Straßenbaum steht
    rechnerisch im Mittel rund 69 Jahre (Bestand ÷ Fällungen je Jahr: 432.769 Straßenbäume ÷ 6.269
    Fällungen im Jahr 2021, [78], Anlage). In
    69 Jahren summiert sich der Nutzen auf 4.905 €, das 5,1-Fache der 960 €; am ungünstigen Rand
    (185 € je Baum, λ = 0,3) auf 2.108 € gegen 2.960 €, dort trägt sich die Artenwahl nicht mehr. Birken stehen kürzer als der Durchschnitt
    (Hannover, oben). Würden die sonst gepflanzten Birken alle 20 Jahre neu gepflanzt, begänne ihr
    Kronenwachstum jedes Mal von vorn: Die Amortisation stiege von 24 auf 32 Jahre, denn die 24 Jahre liegen über den 20 Jahren bis
    zum nächsten Ersatz; der Nutzen über 69 Jahre sänke auf 2.225 €, das 2,3-Fache, am ungünstigen Rand auf
    956 € gegen 2.960 €. Am Punktwert trägt sich die Artenwahl bei ohnehin fälliger Nachpflanzung also über
    die Lebensdauer des Baums, auch bei Ersatz alle 20 Jahre; am ungünstigen Rand trägt sie sich in keinem
    der beiden Fälle. Für die Birke selbst liefert [80] keine Kurve. Wächst eine junge Birke schneller als eine
    Linde, käme der Nutzen früher, und die 24 Jahre sind eine Obergrenze; wächst sie langsamer, käme er
    später. Blüte zählt die Ebene nicht, nur Kronenfläche (§3.3). Blühte eine junge Birke erst fünf Jahre nach der Pflanzung, verschöbe sich die
    Amortisation von 24 auf 25 Jahre, nach zehn Jahren auf 27 Jahre.

  **Stärkster Treiber** ist der Fall, nicht das Band: Der vorgezogene Ersatz kostet das 74-Fache der
  Artenwahl. Innerhalb des vorgezogenen Ersatzes treiben die Pflanzkosten am Standort (−28 … +44 % über
  ihr Band), die Fällung bewegt −9 … +18 %.
  **Was die einfachere Rechnung verfälschen würde:** Rechnete man für jeden ersetzten Baum die vollen
  4.436 €, erschiene die Artenwahl bei einer ohnehin fälligen Nachpflanzung 74-mal so teuer, wie sie
  ist; rechnete man immer nur 60 €, erschiene ein vorgezogener Ersatz fast kostenlos. Rechnete man bei
  der Nachpflanzung mit voller Krone ab dem ersten Jahr, erschiene die Amortisation nach 11 statt nach
  24 Jahren. Eine Vereinfachung bleibt und ist benannt: Dass ein vorgezogen gefällter Baum später
  ohnehin ersetzt worden wäre, rechnet der Bericht nicht gegen; für alte Bäume sind 4.436 € deshalb eine
  Obergrenze. Bei der Nachpflanzung wirkt die Maßnahme erst, wenn der alte Baum fällt; als Anteil
  \(a\) gibt die Kommune deshalb nur die Kronen an, die im betrachteten Zeitraum ersetzt werden. Ob die
  Baumschulliste [79] die Umsatzsteuer enthält, sagt sie nicht (gelesen: Titelseite, Inhalt,
  Laubbäume S. 26 f.); an 60 € macht das höchstens 11 € aus.
  **Vorgabe für das Produkt** (Befund 253, Übernahme Ü-11): Das Produkt
  fragt den Fall ab, Nachpflanzung ohnehin oder vorgezogener Ersatz, und rechnet mit 60 €
  oder 4.436 € je Baum; die Zahl der Bäume gibt die Kommune ein. Ohne Angabe des Falls zeigt es beide
  Beträge nebeneinander und keine Kosten-Nutzen-Kennzahl, eine stille Vorgabe auf einen der beiden Fälle
  gibt es nicht. Im Fall der Nachpflanzung sagt es dazu, dass der Nutzen je Jahr erst mit voller Krone
  gilt (Amortisation am Punktwert nach 24 Jahren).

```python test: beispiel_96_stadtbaum_kosten
import math
preis = {"I": 395, "II": 455, "III": 485, "IV": 580}   # Preisliste [79], Hochstamm StU 18-20 cm, ab 14.02.2024
nach = preis["II"] - preis["I"]                         # Nachpflanzung ohnehin: Mehrkosten der Artenwahl
nach_band = (0, preis["IV"] - preis["I"])
assert nach == 60 and nach_band == (0, 185)
pflanz, pflanz_band = 3_636, (2_400, 5_600)             # Hamburg 2024 [75], mit dreijaehriger Anwuchspflege
faell, faell_band = 800, (400, 1_600)                   # Faellung: Abschaetzung von KAP3
vor = pflanz + faell                                    # vorgezogener Ersatz
vor_band = (pflanz_band[0] + faell_band[0], pflanz_band[1] + faell_band[1])
assert vor == 4_436 and vor_band == (2_800, 7_200)
assert abs(faell / vor - 0.18) < 0.005 and nach / pflanz < 0.02
assert round(vor / nach) == 74
berlin = 3_000 * 119.3 / 110.2                          # Berlin, Herbst 2022 [78], VPI [19] 2022 -> 2024
assert abs(berlin - 3_248) < 0.5 and pflanz_band[0] <= berlin <= pflanz_band[1]
assert round((pflanz_band[0] - pflanz) / vor, 2) == -0.28 and round((pflanz_band[1] - pflanz) / vor, 2) == 0.44
assert round((faell_band[0] - faell) / vor, 2) == -0.09 and round((faell_band[1] - faell) / vor, 2) == 0.18
# Allee-Zelle (oben): Kronenanteil sinkt um 0,2 x G0 / w_B in einer 100-m-Zelle
dk, zelle = 0.2 * 0.18125 / 0.464, 10_000
krone_m2 = math.pi * (8 / 2) ** 2                       # Produkt: 8 m Kronendurchmesser ohne OSM-Angabe
n = dk * zelle / krone_m2
assert abs(dk * zelle - 781.25) < 1e-9 and abs(krone_m2 - 50.3) < 0.05 and abs(n - 15.5) < 0.05
baeume = math.ceil(n)
assert baeume == 16
assert baeume * vor == 70_976 and (baeume * vor_band[0], baeume * vor_band[1]) == (44_800, 115_200)
assert baeume * nach == 960 and baeume * nach_band[1] == 2_960
nutzen, nutzen_band = 88, (6.1 * 6.20, 20.3 * 6.20)   # Allee-Zelle, EUR je Jahr, Band ueber lambda
assert round(nutzen_band[0]) == 38 and round(nutzen_band[1]) == 126
assert baeume * vor / nutzen > 800                      # vorgezogen: volle Krone ab dem ersten Jahr
assert round(baeume * nach / nutzen, 1) == 10.9          # Nachpflanzung mit voller Krone ab Jahr 1 (zu frueh)
assert 0.19 * nach < 11.5                               # Umsatzsteuer an der Differenz hoechstens 11 EUR
# Punktwert der Artenwahl: Linde (II) statt Birke (I) [79]; Birke 12.209 von 432.769 Strassenbaeumen [78]
assert preis["II"] - preis["I"] == nach and round(151_764 / 432_769, 2) == 0.35   # Linde 35 % in Berlin [78]
# Nachpflanzung: Krone der sonst gepflanzten Birke waechst (Linden-Kurve [80], Tab. 3, Reihen)
def radius(alter):
    return 0.1358 * alter - 0.0008 * alter ** 2


def nutzen_jahr(t, voll=nutzen):                         # t = Jahre nach der Pflanzung, Alter bei Pflanzung 10
    return voll * min(1.0, (radius(10 + t) / 4) ** 2)


def amortisation(kosten, voll=nutzen, start=1, zyklus=None):
    summe = 0.0
    for t in range(1, 500):
        tt = t if zyklus is None else (t - 1) % zyklus + 1
        if tt >= start:
            summe += nutzen_jahr(tt, voll)
        if summe >= kosten:
            return t


assert abs(radius(10) - 1.28) < 0.005 and radius(38) >= 4 > radius(37)   # volle Krone nach 28 Jahren
assert round(nutzen_jahr(1)) == 11 and round(nutzen_jahr(10)) == 32 and round(nutzen_jahr(20)) == 62
assert amortisation(baeume * nach) == 24                # statt 11 mit voller Krone ab Jahr 1
assert amortisation(baeume * nach, nutzen_band[1]) == 20 and amortisation(baeume * nach, nutzen_band[0]) == 39
assert amortisation(baeume * nach_band[1]) == 47 and amortisation(baeume * nach_band[1], nutzen_band[0]) == 92
standzeit = 432_769 / 6_269                              # Berlin 2021: Bestand / Faellungen [78]
assert round(standzeit) == 69
summe69 = sum(nutzen_jahr(t) for t in range(1, 70))
assert round(summe69) == 4_905 and round(summe69 / (baeume * nach), 1) == 5.1
assert round(sum(nutzen_jahr(t, nutzen_band[0]) for t in range(1, 70))) == 2_108
kette = sum(nutzen_jahr((t - 1) % 20 + 1) for t in range(1, 70))            # Birken alle 20 Jahre neu
assert round(kette) == 2_225 and round(kette / (baeume * nach), 1) == 2.3
assert amortisation(baeume * nach, zyklus=20) == 32
assert round(sum(nutzen_jahr((t - 1) % 20 + 1, nutzen_band[0]) for t in range(1, 70))) == 956
assert amortisation(baeume * nach, start=6) == 25 and amortisation(baeume * nach, start=11) == 27   # Bluete spaeter
# Faellung: geometrisches Mittel der Bandenden
assert math.sqrt(faell_band[0] * faell_band[1]) == faell
assert round(1_000 / faell_band[0], 1) == 2.5 and round(faell_band[1] / 1_000, 1) == 1.6
```

  **Zusammen mit S158:** Die Stadtbaumwahl wirkt auf die Quelle (\(\hat P\)), die Frühwarnung auf
  das Verhalten an gewarnten Tagen (§5.1). Im Zelllauf werden beide multiplikativ gerechnet: Die
  Frühwarnung mindert die Tage \(B \cdot \delta_g \cdot \hat P'\), die nach der Pflanzung noch
  anfallen; so zählt kein vermiedener Tag doppelt, weil die Frühwarnung nur auf Tage wirkt, die die
  Pflanzung nicht schon vermieden hat. Befunde 124 und 129 bleiben: keine pauschal verknüpfte
  Maßnahme, gerechnet wird im Zelllauf.
  **Vorgabe für das Produkt (Befund 230):** Die Wirkung erscheint im
  Produkt als Katalogmaßnahme „Allergenarme Stadtbaumwahl“, die im Zelllauf rechnet. Die
  Kommune zeichnet die Zellen als Geometrie der Maßnahme und gibt einen Anteil \(a\) ein, im Produkt
  das Feld `anteil_ersetzt`: den Anteil der allergenen Kronen, die dort ersetzt werden.
  **Wertebereich 0 bis 1** (0 < \(a\) ≤ 1; 1 heißt: alle allergenen Kronen der Zelle). Eine Eingabe
  über 1 hat keine Bedeutung. Das Produkt weist sie bei Anlage und Änderung einer Maßnahme und im
  Excel-Import ab (dort als Fehlerzeile mit Zeilennummer). Trägt eine früher gespeicherte Maßnahme
  noch \(a\) über 1, rechnet die Zelle keinen Betrag und nennt die Eingabe, die zu berichtigen ist
  (Befund 251, Übernahme Ü-9). Ohne diese Sperre bildete der Rechenweg erst \(a\) × Deckungsgrad ×
  Kronenanteil und kappte dann je Term am Kronenanteil; bei teilweiser Deckung senkte eine Eingabe
  über 1 dann mehr als \(a\) = 1, bis zum 1/Deckungsgrad-Fachen, ohne dass es sichtbar wurde.
  Gemessen an der Allee-Zelle: Bei Deckungsgrad 1 ergäben \(a\) = 1, 1,5 und 2,0 ohne Sperre je
  65,9 vermiedene Tage; bei Deckungsgrad 0,5 ergäbe \(a\) = 1 33,0 Tage, \(a\) = 1,5 49,4 Tage und \(a\) = 2,0
  65,9 Tage, das Doppelte. Je Zelle sinkt der Kronenanteil mit
  Gattungs-Tag um \(a\) × Deckungsgrad × \(k_{\text{Birke},z}\) und der ohne Gattungs-Tag um
  \(a\) × Deckungsgrad × \(k_{\text{unbek},z}\), jeweils in seinem eigenen Term und höchstens bis auf
  null (Grenze je Term oben); die Senkung folgt also der Mischung der Zelle im Ausgangsstand. Eine
  Eingabe getrennt nach Kronen mit und ohne Gattungs-Tag, wie sie Punkt (2) unten verlangt, hat das
  Produkt nicht. **Das ist eine Modellgrenze (Befund 247), deren Richtung offen ist:** In der
  Allee-Zelle oben stehen nur Kronen mit Gattungs-Tag, dort ist der Fehler null, ebenso wenn die
  ersetzten Bäume gemischt sind wie die Zelle. Führt eine Zelle gleich viel Kronen mit und ohne
  Gattungs-Tag und werden bei gleicher ersetzter Kronenfläche nur Bäume mit Tag ersetzt, rechnet das
  Produkt das 0,56-Fache der Senkung; werden nur Bäume ohne Tag ersetzt, das 4,67-Fache (Block
  `beispiel_96_stadtbaum_allee`). Daraus rechnet das Produkt
  \(\hat G'\) nach der Formel unten, \(\hat P\) mit dem Ḡ₀, das im Ausgangslauf gespeichert wurde, und die
  Zusatztage der Zelle neu. Ausgewiesen werden die vermiedenen Tage je Zelle und die vermiedenen Tage
  und Euro der Kommune, gekennzeichnet als „Abschätzung von KAP3“ mit dem Hinweis auf die Richtung des
  Fehlers in λ (Modellgrenze 7). Fehlt die Eingabe \(a\) oder führen die gewählten Zellen keine Kronen,
  steht ein Vermerk statt 0 €. Für die Allee-Zelle und das Rechenbeispiel der Kommune oben ergibt das
  Produkt dieselben Zahlen mit dem Klimaanteil 0,27 (Übernahme Ü-13): 14,2 Tage und ≈ 88 € je Jahr;
  637 Tage und ≈ 3.950 € je Jahr. Liegen Frühwarnung und Stadtbaumwahl in derselben Zelle, rechnet die
  Frühwarnung ihre vermiedenen Tage und Euro auf die Tage nach der Pflanzung (Absatz oben; Allee-Zelle
  3,56 statt 3,88 Tage, 3,56 × 6,20 € = 22,09 € statt 24,07 €; Befund 240, Übernahme Ü-7). Je Zelle
  gibt das Produkt die vermiedenen Tage und Euro aus, Euro = Tage × 6,20 € (Allee-Zelle: Stadtbaumwahl
  88,10 €, Frühwarnung allein 24,07 €); die Summe der ungerundeten Zellwerte ist der Euro-Betrag der
  Kommune, gerundet wird nur in der Anzeige (Befund 237, Übernahme Ü-4). Die Kosten der Maßnahme führt
  es je gewähltem Fall wie im Absatz „Kosten der Stadtbaumwahl“ oben (Befund 253, Übernahmen Ü-11 und
  Ü-12). Gattungswissen der Kommune geht nur kommunenweit über \(s_{\text{unbek}}\) ein (Befund 246,
  Modellgrenze oben). Nach Log 26 gehören \(\hat G\), \(\hat G'\) und Ḡ₀ zum selben Ausgangsstand;
  ein neues \(s_{\text{unbek}}\) ist ein neuer Ausgangsstand und braucht einen neuen Zelllauf. Das
  Produkt rechnet die Senkung deshalb mit dem \(s_{\text{unbek}}\), das im Ausgangslauf je Zelle
  gespeichert ist. Überschreibt die Kommune den Wert danach, sagt ein Hinweis neben dem Betrag, dass
  er erst mit einem neuen Zelllauf gilt; trägt ein älterer Ausgangslauf den Wert noch nicht, rechnet
  die Maßnahme mit dem Wert von heute und bittet, den Ausgangslauf neu zu rechnen (Befund 252,
  Übernahme Ü-10). Gemessen an der Allee-Zelle ohne Gattungs-Tag (Ausgangslauf mit 0,12, danach
  0,25): 1,71 vermiedene Tage von 114,5 wie ohne Überschreibung; erst ein neuer Zelllauf mit 0,25
  ergibt 3,55 von 123,1 Tagen. Mischte die Rechnung beide Stände, wiese sie 3,55 von 114,5 Tagen
  aus.
  **Integrationsauflage (Stadtbaumwahl)**, im
  Rahmen der Auflage aus §3.3 (nur zellscharfe Änderung von \(\hat G\) mit Neuberechnung, nie ein
  Faktor): Die Rechnung braucht (1) die vom Nutzer gewählten Zellen, (2) als Eingabe die Änderung des
  Kronenanteils der Birkengruppe in diesen Zellen (Beispiel: 0,30 → 0,20), getrennt nach Kronen mit
  und ohne Gattungs-Tag; \(\hat G'\) folgt aus der vollen Ebenendefinition
  \(\hat G_z = w_B\,[k_{\text{Birke},z} + s_{\text{unbek}}\,k_{\text{unbek},z}] + (1-w_B)\,\text{Grün}_z\)
  (§3.3). Die Senkung wird in dem Term abgezogen, in dem die ersetzten Kronen im Ausgangsstand
  stehen, \(\hat G' = \hat G - 0{,}464 \cdot (\Delta k_{\text{Birke}} + 0{,}12 \cdot \Delta
  k_{\text{unbek}})\), mit der Grenze je Term \(\Delta k_{\text{Birke}} \le k_{\text{Birke}}\) und
  \(\Delta k_{\text{unbek}} \le k_{\text{unbek}}\), daraus \(\hat G' \ge 0{,}536 \times\) Grünanteil
  (Beitrag der Gehölze nie unter null; Befunde 248, 249), nie aus einer anteiligen Senkung von \(\hat G\) und nie mit 0,464 voll
  auf Kronen, die der Ausgangsstand ohne Gattungs-Tag führt; eigene Gattungsangaben der Kommune
  gehen schon in den Ausgangsstand und in Ḡ₀ ein, (3) den Zelllauf mit
  dem im Ausgangsszenario gebildeten und festgehaltenen Ḡ₀ und neuem \(\hat P\) je Zelle und (4) als
  Ausgabe die Änderung der Zusatztage und Euro je Zelle und für die Kommune, gekennzeichnet als
  „Abschätzung von KAP3“, mit dem Hinweis auf die Richtung des Fehlers in λ (Modellgrenze 7).
  Die Grenze der Abschätzung liegt nicht mehr in der Summe, sondern in λ: Die Quelle für den
  örtlichen Anteil betrifft Gräser, nicht Bäume, und Ferntransport entkoppelt lokale Vegetation
  und lokalen Pollenflug teilweise (Modellgrenze 2/7). Das ist eine **Evidenz-**, keine
  Modellierungsgrenze; sie ist mit einer Emissions-/Ausbreitungs-Evidenz
  auflösbar (Ersetzungspfad, §6). Evidenz-Charakter: die
  Vegetations-Symptom-Kopplung ist beobachtend belegt [54–56] — **kein**
  Interventions-RCT (randomisierte kontrollierte Studie: Das Los entscheidet, wer die Maßnahme bekommt,
  und der Unterschied zur Gruppe ohne Maßnahme ist ihre Wirkung); als mechanischer Hebel mit gekennzeichneter Effektkette geführt
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
Effektgröße auf Symptomtage. Eine Interventionsstudie führt die Maßnahme gezielt ein und misst ihre
Wirkung; eine quasi-experimentelle Studie vergleicht ohne Losentscheid Menschen oder Orte, die eine
Maßnahme ohnehin bekommen haben, mit vergleichbaren ohne sie; anders als beim Hitzewarnsystem (#95, Register 95-S158-01:
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

**An welchen Tagen und ab welcher Belastung die Warnung wirkt (Festlegung, Log 23/24).**

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
  0,70 × 0,55 × 4,20 × 0,27 = **0,43659 Tage** (Birkengruppe) und 0,70 × 0,75 × 4,08 × 0,27 =
  **0,57834 Tage** (Gräser), zusammen 1,01493 Tage. Die Zusatztage liegen am Anfang der jeweiligen
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
  \(t_{\text{warn},g,V} = \min(1;\ m_{g,V}/f)\). **Abschätzung von KAP3 (§3.9 ABGESCHÄTZT):** Die
  Formel legt die Beschwerdetage auf die Tage mit der höchsten Belastung (Pollenflug treibt die
  Symptomlast, Pfaar [52], qualitativ). Herleitung: Von allen Saisontagen sind der Anteil \(f\)
  Beschwerdetage und der Anteil \(m\) gewarnte Tage. Liegen die Beschwerdetage so weit wie möglich
  auf gewarnten Tagen, ist von ihnen der Anteil \(m/f\) gewarnt, höchstens alle.
  **Richtung des Fehlers:** Das ist die größtmögliche Überlappung und damit eine Obergrenze. Treten
  Beschwerden auch an Tagen unter „mittel“ auf (etwa bei stark sensibilisierten Personen), ist der
  wahre Anteil kleiner, und die Formel überzeichnet \(t_{\text{warn}}\) und die Wirkung von S158.
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
ist der Anteil der Zellfläche im Geltungsbereich der kommunalen Warnkanäle: 1 für eine Zelle ganz im
Gebiet, 0 außerhalb, dazwischen für eine Zelle am Rand des Gebiets. Für den Randfall gelten die
Betroffenen als gleichmäßig über die Zelle verteilt; im Produkt ist \(A_{\text{Zelle}}\) der Deckungsgrad
der Zelle durch die Geometrie der Maßnahme (Befund 232). \(q_{\text{reich}}\) ist die Reichweite unter den Betroffenen **innerhalb** dieses Bereichs, deshalb
zählt die Fläche nicht doppelt. In Worten: Von den Zusatztagen einer Zelle zählt je Gruppe nur der
gewarnte Teil, und davon wird der Anteil \(r_{\text{S158}}\) vermieden.

**Was die Formel heute von einem Faktor unterscheidet — und was nicht.** Mit den heutigen Werten
ist \(t_{\text{warn}}\) für beide Gruppen gleich (0,75). Die Formel mindert dann jede Zelle im
Geltungsbereich um denselben Anteil ihrer Zusatztage, 0,03 × 0,75 = 2,25 %. Das Ergebnis ist
deshalb heute **zahlengleich** mit einem Faktor 0,0225 auf die gespeicherten Zusatztage der Zellen
im Geltungsbereich; für Berlin ergeben beide Wege 8.981 Tage (Zelllauf, unten). Die Festlegung
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
| 1 | Zusatztage Birkengruppe \(B \times \delta_B\) | 402.103 × 0,43659 = **175.554 Tage** |
| 2 | Zusatztage Gräser \(B \times \delta_G\) | 402.103 × 0,57834 = **232.552 Tage** (zusammen 408.106 wie §3.0 Ebene 8) |
| 3 | davon gewarnt (\(t_{\text{warn}}\) = 0,75) | 131.666 + 174.414 = **306.080 Tage** |
| 4 | vermieden (\(r_{\text{S158}}\) = 0,03) | 306.080 × 0,03 = **9.182 Tage je Jahr** (2,25 % der Zusatztage) |
| 5 | in Euro (\(c_{\text{Tag}}\) = 6,20 €) | 9.182 × 6,20 € = **≈ 56.900 € je Jahr** (Preisstand 2024) |

Band: 1.020 Tage (≈ 6.300 €) bis 40.811 Tage (≈ 253.000 €) je Jahr. Der Zelllauf des Produkts
(399.171 Tage, §3.0) ergibt 8.981 Tage und ≈ 55.700 €, Zelle für Zelle gerechnet und ebenso als
Faktor 0,0225 auf die Summe: heute zahlengleich (siehe oben). Rev. 3 hätte ohne Tagesauswahl 12.243 Tage
und ≈ 75.900 € ausgewiesen, ein Drittel mehr. Zellscharf: Eine Allee-Zelle mit 100 Betroffenen
und \(\hat P\) = 1,7 hat 100 × 1,01493 × 1,7 = 172,5 Zusatztage; im Geltungsbereich werden davon
3,88 Tage (≈ 24 €) vermieden, außerhalb (\(A\) = 0) keine.

**Ergebnis-Sensitivität (§3.9).** Alle vier Faktoren wirken linear. **Stärkster Treiber ist
\(e_{\text{Tag}}\)**: zwischen seinen Ankern liegt der Faktor 3 (für Berlin 4.591–13.774 Tage,
≈ 28.500–85.400 €), vor \(q_{\text{reich}}\) (Faktor 2,75), \(q_{\text{handel}}\) (2,4) und
\(t_{\text{warn}}\) (2,0; 6.122–12.243 Tage). Der Schadenswert selbst bleibt unberührt, solange die Maßnahme
nicht gewählt ist. Bezogen auf die §4-Bundessumme von ≈ 60 Mio. € je Jahr (Preisstand 2024) entspricht der
Basiswert bei flächendeckender Umsetzung **≈ 1,3 Mio. € je Jahr** vermiedener Behandlungskosten
(Band ≈ 0,15–6,0 Mio. €). Ob sich die Maßnahme trägt, rechnet das Maßnahmen-Modul gegen die
Vorhaltekosten (Katalog `POLLEN_EARLY_WARNING`: 15.000 € Anschaffung je Station, 4.000 € je
Station und Jahr Betrieb); ab welchem Punkt im Band das der Fall ist, steht nach dem folgenden
Block.

```python test: beispiel_96_s158_wirkung
# S158 nach Tagen und Belastung (Log 23), Beispielkommune Berlin wie Rechenkette 3.0
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
f, p_B, p_G, a_attr, dS_B, dS_G = 0.70, 0.55, 0.75, 0.27, 4.20, 4.08
d_B, d_G = f * p_B * dS_B * a_attr, f * p_G * dS_G * a_attr
assert abs(d_B - 0.43659) < 1e-9 and abs(d_G - 0.57834) < 1e-9
assert abs(d_B + d_G - 1.01493) < 1e-9
B, c_tag = 402_103, 6.20
t_B, t_G = B * d_B, B * d_G
assert abs(t_B - 175_554) < 1 and abs(t_G - 232_552) < 1 and abs(t_B + t_G - 408_106) < 1
A = 1                                                        # ganze Stadt im Geltungsbereich
gewarnt = t_warn * t_B + t_warn * t_G
assert abs(gewarnt - 306_080) < 1
vermieden = A * r * gewarnt
assert abs(vermieden - 9_182) < 1 and abs(vermieden / (t_B + t_G) - 0.0225) < 1e-9
assert abs(vermieden * c_tag - 56_900) < 100
# Band (Aushang-Fall mit t_warn 0,50; aktivierte Warnkette mit t_warn 1,00)
t = t_B + t_G
assert abs(unten * 0.50 * t - 1_020) < 1 and abs(unten * 0.50 * t * c_tag - 6_300) < 50
assert abs(0.10 * 1.00 * t - 40_811) < 1 and abs(0.10 * 1.00 * t * c_tag - 253_000) < 50
# Zelllauf des Produkts, Rev. 3 zum Vergleich, eine Allee-Zelle
assert abs(399_171 * r * t_warn - 8_981) < 1 and abs(399_171 * r * t_warn * c_tag - 55_700) < 50
assert abs(r * t - 12_243) < 1 and abs(r * t * c_tag - 75_900) < 50
zelle = 100 * 1.01493 * 1.7
assert abs(zelle - 172.5) < 0.05 and abs(A * r * t_warn * zelle - 3.88) < 0.005
assert abs(A * r * t_warn * zelle * c_tag - 24) < 0.5 and 0 * r * t_warn * zelle == 0
# Sensitivitaet: e_Tag staerkster Treiber (Faktor 3), dann q_reich, q_handel, t_warn
spannen = {"e_tag": 0.30 / 0.10, "q_reich": 0.55 / 0.20, "q_handel": 0.60 / 0.25, "t_warn": 1.00 / 0.50}
assert max(spannen, key=spannen.get) == "e_tag"
assert abs(spannen["q_reich"] - 2.75) < 1e-9 and abs(spannen["q_handel"] - 2.4) < 1e-9
assert abs(vermieden * 0.10 / 0.20 - 4_591) < 1 and abs(vermieden * 0.30 / 0.20 - 13_774) < 1
assert abs(vermieden * 0.10 / 0.20 * c_tag - 28_500) < 50
assert abs(vermieden * 0.30 / 0.20 * c_tag - 85_400) < 50
assert abs(vermieden * 0.50 / 0.75 - 6_122) < 1 and abs(vermieden * 1.00 / 0.75 - 12_243) < 1
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
# Bundessumme (§4-Sanity ~60 Mio EUR_2024 je Jahr, Block beispiel_96_bundessumme)
bund = 8_959_105 * f * (p_B * 4.79 + p_G * 4.06) * a_attr * c_tag
assert abs(bund / 1e6 - 60) < 1
assert abs(r * t_warn * bund / 1e6 - 1.3) < 0.05
assert abs(unten * 0.50 * bund / 1e6 - 0.15) < 0.005 and abs(0.10 * bund / 1e6 - 6.0) < 0.05
```

**Ab wann sich die Frühwarnung trägt (Befund 244).** Der Nutzen je Jahr ist der wirksame Wert
\(r_{\text{S158}} \cdot t_{\text{warn}}\) mal dem Schadenswert im Geltungsbereich; Euro folgen den
Tagen im gleichen Verhältnis (§3.3). Die Frühwarnung trägt ihren Betrieb, sobald dieser Nutzen die
Betriebskosten erreicht: 4.000 € je Station und Jahr (Katalog `POLLEN_EARLY_WARNING`,
Modellannahme). Die Schwelle ist damit: wirksamer Wert ≥ Zahl der Stationen × 4.000 € ÷
Schadenswert je Jahr.

- **Kommune mit 100.000 Einwohnern im Bundes-Altersmix** (Beispielgröße im Produkttext):
  Schadenswert des Berichts 100.000 × 10,74 % × 1,07343 Tage × 6,20 € = 71.477 € je Jahr (§3.2, §4;
  der Produkttext rechnet mit demselben \(a_{\text{attr}}\) = 0,27). Der Nutzen reicht von
  179 € (wirksam 0,0025) über 1.608 € am Basiswert (0,0225) bis 7.148 € (0,10) je Jahr. Eine Station
  trägt sich ab einem wirksamen Wert von 4.000 € ÷ 71.477 € = **0,056**, dem 2,49-Fachen des
  Basiswerts, also \(r_{\text{S158}}\) = 0,075 bei \(t_{\text{warn}}\) = 0,75. Darunter, auch am Basiswert,
  trägt sie sich nicht; von 0,056 bis zum oberen Bandende trägt sie sich, dort für eine Station. Kein
  Faktor allein an seinem oberen Anker reicht (höchstens 2.359 €, \(q_{\text{reich}}\) = 0,55; \(e_{\text{Tag}}\)
  = 0,30 ergibt 2.252 €), auch keine zwei (höchstens 3.538 €); drei der vier Faktoren am oberen Anker
  reichen (4.503–5.307 €).
- **Berlin** (Zelllauf 399.171 Tage × 6,20 € = 2,47 Mio. € je Jahr, ganze Stadt im
  Geltungsbereich): Eine Station trägt sich ab einem wirksamen Wert von 4.000 € ÷ 2,47 Mio. € =
  **0,0016**. Das liegt unter dem unteren Bandende 0,0025, eine Station trägt sich also im ganzen
  Band. Der Nutzen deckt den Betrieb von 1 Station am unteren Bandende (≈ 6.190 €), von 13 am
  Basiswert (≈ 55.700 €) und von 61 am oberen Bandende (≈ 247.500 €).

Bei \(n\) Stationen gilt das \(n\)-Fache der Schwelle. Die Schwelle ist **nur gegen den Betrieb**
gerechnet. Die Anschaffung (15.000 € je Station, Katalog) ist nicht auf Jahre umgelegt, weil es für
die Nutzungsdauer einer Pollenmessstation weder eine Quelle noch eine Abschätzung von KAP3 gibt;
jede Umlage hebt die Schwelle um 15.000 € ÷ Nutzungsdauer je Station und Jahr. Der gegenteilige
Satz, die Maßnahme trage sich an keiner Stelle des Bands, stimmt deshalb nicht. Der Katalogtext
der Frühwarnung (Feld `sensitivitaet`) gibt diesen Absatz wieder; das Band bleibt
(Befund 244).

```python test: beispiel_96_s158_schwelle
# Ab wann traegt sich die Fruehwarnung gegen den Betrieb (Befund 244)? Groessen aus §5.1
r, t_warn = 0.03, 0.75                          # Kap. 7 pollen.r_s158, pollen.t_warn_s158
wirksam = r * t_warn
unten, oben = 0.20 * 0.25 * 0.10 * 0.50, 0.10 * 1.00   # Band wirksam (unveraendert)
assert abs(unten - 0.0025) < 1e-12 and abs(oben - 0.10) < 1e-12
opex, c_tag = 4_000, 6.20                       # EUR je Station und Jahr (Katalog); Kap. 7 pollen.c_tag
def schwelle(schaden, stationen=1):
    return stationen * opex / schaden           # wirksamer Wert, ab dem der Nutzen den Betrieb traegt
# (a) Beispielgroesse des Produkttexts: 100.000 Einwohner im Bundes-Altersmix
import itertools
delta_de = 0.70 * (0.55 * 4.79 + 0.75 * 4.06) * 0.27           # §4, Kap. 7 pollen.a_attr
s_100k = 100_000 * 0.1074 * delta_de * c_tag                    # Wert des Berichts, §3.2 und §4
assert abs(s_100k - 71_477) < 1
assert abs(unten * s_100k - 179) < 1 and abs(oben * s_100k - 7_148) < 1
assert abs(wirksam * s_100k - 1_608) < 1
s_a = schwelle(s_100k)
assert abs(s_a - 0.056) < 0.0005 and unten < s_a < oben
assert wirksam * s_100k < opex                  # am Basiswert traegt sie sich nicht
assert abs(s_a / wirksam - 2.49) < 0.005 and abs(s_a / t_warn - 0.075) < 0.0005
assert int(oben * s_100k // opex) == 1          # oberes Bandende: eine Station
basis = {"q_reich": 0.35, "q_handel": 0.40, "e_tag": 0.20, "t_warn": 0.75}
anker = {"q_reich": 0.55, "q_handel": 0.60, "e_tag": 0.30, "t_warn": 1.00}   # obere Anker (§5.1)
def nutzen_anker(oben_an):
    w = 1.0
    for name, wert in basis.items():
        w *= anker[name] if name in oben_an else wert
    return w * s_100k
eins, zwei, drei = ([nutzen_anker(c) for c in itertools.combinations(basis, n)] for n in (1, 2, 3))
assert round(max(eins)) == 2_359 and max(eins) < opex and round(nutzen_anker(("e_tag",))) == 2_252
assert round(max(zwei)) == 3_538 and max(zwei) < opex
assert (round(min(drei)), round(max(drei))) == (4_503, 5_307) and min(drei) > opex
# (b) Berlin, Zelllauf (§3.0), ganze Stadt im Geltungsbereich
s_berlin = 2_474_857.71                        # Zelllauf §3.0, Anlage 96_zelllauf_bandsummen.py
assert abs(s_berlin - 399_171 * c_tag) < 5
s_b = schwelle(s_berlin)
assert abs(s_b - 0.0016) < 0.00005 and s_b < unten    # traegt sich im ganzen Band
assert int(unten * s_berlin // opex) == 1 and abs(unten * s_berlin - 6_190) < 5
assert int(wirksam * s_berlin // opex) == 13 and abs(wirksam * s_berlin - 55_700) < 50
assert int(oben * s_berlin // opex) == 61 and abs(oben * s_berlin - 247_500) < 50
# n Stationen: n-fache Schwelle
assert abs(schwelle(s_berlin, 13) - 13 * s_b) < 1e-12 and schwelle(s_berlin, 14) > wirksam
```

**Integrationsauflage (S158).** Die Maßnahme ist so verknüpft, dass sie im
Zelllauf rechnet, nicht als Faktor auf gespeicherte Ergebnisse. Die Rechnung braucht dafür:

1. die Zusatztage je Zelle **getrennt nach Gruppe**, \(\Delta\text{Tage}_{B,\text{Zelle}}\) und
   \(\Delta\text{Tage}_{G,\text{Zelle}}\), nicht nur ihre Summe;
2. den Anteil gewarnter Tage \(t_{\text{warn},g}\) (Kapitel 7 `pollen.t_warn_s158`, 0,75 für beide
   Gruppen; nach dem Ersetzungspfad \(t_{\text{warn},g,V} = \min(1;\ m_{g,V}/f)\) je
   DWD-Gebiet \(V\) aus [71], dazu die Zuordnung Zelle → DWD-Gebiet (über Bundesland und
   Teilgebiet der Zelle, Gebietsliste [72]) — **nicht** den DWD-Anteil \(m_{g,V}\) selbst, der die Wirkung um
   den Faktor \(f\) verdünnen würde);
3. den Wirkungsfaktor je gewarntem Tag \(r_{\text{S158}}\) (Kapitel 7 `pollen.r_s158`, 0,03);
4. den Geltungsbereich \(A_{\text{Zelle}}\) als Eingabe im Maßnahmen-Modul (ganze Kommune oder
   ausgewählte Gebiete, gezeichnet als Geometrie der Maßnahme; je Zelle ihr Deckungsgrad von 0 bis 1);
5. als Ausgabe die vermiedenen Tage und Euro je Zelle und für die Kommune, gekennzeichnet als
   „Abschätzung von KAP3“ (Vorgabe P1).

**Verknüpfung im Zelllauf (Befund 231).** Die Rechnung läuft im Zelllauf.
`POLLEN_EARLY_WARNING` führt `EXPECTED_ANNUAL_ALLERGY_DAYS` in `linked_risk_codes` mit dem
Zelllauf-Modell `s158`, `qualitative_risk_codes` ist leer, `default_reduction` = 0,03
(`backend/app/data/catalog.py`, Ledger-Befund 215). Die Sperre aus Befund 124 ist damit erfüllt, nicht
aufgehoben: Der Test `test_no_flat_measure_on_allergy_days` lässt für #96 nur Maßnahmen zu, die im
Zelllauf rechnen, und keine rechnet über einen pauschalen Reduktionsfaktor. Die Zusatztage je Gruppe
holt das Maßnahmen-Modul je Zelle frisch aus den gespeicherten Eingaben der Zelle (Punkt 1); im
Geltungsbereich ändert die Frühwarnung Karten- und Ergebniswerte von #96. Ausgewiesen werden die
vermiedenen Tage je Zelle und die vermiedenen Tage und Euro der Kommune, gekennzeichnet als „Abschätzung
von KAP3“ (Punkt 5); ohne Aufteilung nach Gruppe steht ein Vermerk statt 0 €. Den
Ersetzungspfad aus Punkt 2 rechnet das Produkt erst mit den Daten [71] und [72]; ohne sie gilt
0,75 für beide Gruppen und alle Gebiete (Modellgrenze 8, Befund 233). Euro je Zelle aus Punkt 5
sind Tage × 6,20 € (Befund 237). Mit 0,75 für alle Gruppen und Gebiete wäre ein
Faktor 0,0225 auf die gespeicherten Zusatztage der Zellen im Geltungsbereich zahlengleich (siehe
„Was die Formel heute von einem Faktor unterscheidet“). Verlangt war der Zelllauf mit getrennten
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
Hayfever Diary) gegen die Einführung kommunaler Warnkanäle (DiD, Differenz-von-Differenzen: die Änderung der
Symptomtage in Kommunen, die einen Warnkanal einführen, abzüglich der Änderung im selben Zeitraum in Kommunen
ohne ihn; was übrig bleibt, ist die Wirkung des Warnkanals) ersetzt den Personenteil durch eine
gemessene Effektgröße, die DWD-Pollenflugstatistik [71] den Anteil \(t_{\text{warn}}\) (umgerechnet
über \(m_{g,V}/f\), siehe oben); ohne diese Daten ist die Kette oben der vollständige Nachweis des Werts.

**Abgrenzung zu Modellgrenze 7 / Ledger-Befund 124.**
Nach Modellgrenze 7 (Log 26) wirkt eine Vegetationsmaßnahme, auch eine flächige, nur im Zelllauf:
Sie ändert \(\hat G\) der Zellen, die sie trifft, zu \(\hat G'\), und \(\hat P\) wird bei
festgehaltenem Ḡ₀ neu gerechnet. So senkt auch ein flächiges Pflanzprogramm die Summe der Kommune
(§5, Stadtbaumwahl). Nie wirkt sie als pauschaler Faktor auf alle Zellen (Befunde 124 und 129).
\(r_{\text{S158}}\) läuft nicht über \(\hat G/\lambda\): Die Frühwarnung ändert keine Bäume und
keine Pollenlast, sie ist eine Verhaltens- und Expositionsminderung an gewarnten Tagen, also ein
Verhaltenskanal und kein Vegetationskanal. Die Sperre aus Befund 124
bleibt **unangetastet**: Die Frühwarnung ist mit #96 nur über ihr Zelllauf-Modell verknüpft
(Absatz „Verknüpfung im Zelllauf (Befund 231)“ oben). Divergenzen Bericht ⇄ Code sind **ausgewiesen und im Ledger geführt**
(Befunde 151 und 156 und die Befunde ab 230), nicht still (Eiserne Regel 5).

**Produkt-Kennzeichnung (§3.6/Vorgabe P1).** In der nutzersichtbaren Parameterliste tragen
\(r_{\text{S158}}\) und \(t_{\text{warn}}\) den Vermerk „Abschätzung von KAP3“ mit dieser Herleitung (Schwelle
„mittel“ nach DWD [70], vier Faktoren mit je zwei Ankern, Band, Sensitivität, Modellgrenze 8,
Ersetzungspfad); eine Herleitung allein als Code-Kommentar genügt nicht.

## 6 Szenario-Anwendung & Modellgrenzen (§3.2/§3.6)

**Jahresbeträge ohne Abzinsung.** Alle Euro-Beträge dieses Berichts sind Jahresbeträge ohne Abzinsung: Sie
gelten für ein Jahr im Ist-Klima zum Preisstand 2024 und werden weder über mehrere Jahre summiert noch auf
einen Barwert abgezinst. Die Diskontrate für mehrjährige Rechnungen legt dieser Bericht nicht fest.

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
5. Attributions-Übertrag Nordamerika→DE: Der Klimaanteil 0,27 ist die Mitte der Spanne 19–35 % für die Saisonlänge
   1990–2018 aus den Schätzungen von 22 Klimamodellen in [9], eine Abschätzung von KAP3 mit dem Band 0,19–0,41 aus
   beiden Spannen der Länge (Interquartilsabstand erklärt in Kap. 2, Befund 258). Ob der Anteil in Deutschland
   ebenso hoch ist, belegt keine Quelle; §4 zeigt nur, dass \(\delta\) in der Größenordnung unter dem Klimaanteil
   der Saisonverlängerung aus [9] liegt.
6. Kostensatz: **Proxy** (§3.5) — Umlage der Jahreskosten (inkl. perennialer AR) auf
   Saisontage und Durchschnitts- statt Grenzkosten wirken überschätzend, ausgelassene
   Selbstmedikation Nicht-Diagnostizierter und fehlender Kaufkraft-Aufschlag
   unterschätzend; Raumtransfer Schweden → Deutschland; Schweregrad-Mix (TOTALL populationsbasiert =
   Basis; Schramm moderate–schwer = Obergrenze); exakte deutsche J30-KKR-Werte nicht
   regulär publiziert [66].
7. **Vegetation: im Ausgangsstand nullsummig, mit Maßnahme summenwirksam** (Rev. 2, Log 18;
   Rev. 4, Log 26; Log 19 verworfen): Im Ausgangsstand ist \(\hat P\) auf den Bezugswert Ḡ₀
   der eigenen Kommune zentriert und **nullsummig umverteilend** — die heutige
   Vegetationsstruktur differenziert *innerhalb* der Kommune, verschiebt aber deren Summe nicht,
   und zwischen Kommunen wirkt sie nicht. Eine Maßnahme, die \(\hat G\) senkt, wird am
   festgehaltenen Ḡ₀ gemessen und senkt die Summe um \(\lambda \cdot \sum B\,(\hat G - \hat G')/\bar G_0\)
   Betroffene (§5, Rechenbeispiel). **Richtung des Fehlers:** λ ist dabei als Anteil der
   örtlichen Quellen an der Pollenlast gelesen, 1 − λ als regionaler Hintergrund. Belegt ist das
   mit Hugg 2017 [74] (Gräser, je acht Messstellen in Helsinki und Espoo; abgeleitet 0,22–0,94,
   drei von vier Werten im Band 0,3–1,0; Rechnung in Kap. 8 [74]). Zwei Fehler wirken gegeneinander: Die Bezugsstelle der
   Quelle liegt selbst in der Stadt, die abgeleiteten Werte sind Untergrenzen, und λ = 0,7
   **unterzeichnet** die Senkung eher. Birkenpollen fliegen weiter als Gräserpollen (Modellgrenze 2);
   für Bäume kann der örtliche Anteil kleiner sein, und λ **überzeichnet** die Senkung dann. Einen
   Birkenbeleg mit Zahl gibt es nicht; welche Richtung überwiegt, ist nicht bestimmbar, das Band
   0,3–1,0 deckt beide. **Ersetzungspfad:** eine Emissions-/Ausbreitungs-Evidenz
   (Pollenquellstärke je Vegetationsfläche × Ausbreitungsmodell) würde den örtlichen Anteil je
   Pollenart bestimmen und λ für Bäume ersetzen.
8. **Bauform der S158-Abschätzung: was vom Pauschalfaktor bleibt** (§5.1, Vorgabe P2;
   Log 23/24): Die Warnung wirkt nur an gewarnten Tagen
   (DWD-Index mindestens „mittel“ [70]), je Pollengruppe und im Zelllauf nur in Zellen im
   Geltungsbereich (\(A_{\text{Zelle}}\)). **Pauschal bleibt** der Personenteil
   \(r_{\text{S158}} = q_{\text{reich}} q_{\text{handel}} e_{\text{Tag}}\) = 0,03 je gewarntem Tag
   (0,005–0,10): Reichweite, Handlungsbereitschaft und Tageswirkung sind je Zelle nicht
   beobachtbar und gelten in allen Zellen gleich. Ebenso pauschal ist vorerst der Anteil
   gewarnter Tage \(t_{\text{warn}}\) = 0,75 (0,50–1,00), gleich für beide Gruppen und alle Regionen.
   Die Umrechnung \(\min(1;\ m/f)\) rechnet das Produkt erst mit den Daten [71] und [72] und der
   Zuordnung Zelle → DWD-Gebiet; ohne sie gilt überall 0,75 (Befund 233).
   Innerhalb des Geltungsbereichs mindert die Maßnahme deshalb jede Zelle um denselben Anteil
   (2,25 %). **Heute ist das zahlengleich mit einem Faktor 0,0225** auf die Zusatztage der Zellen im
   Geltungsbereich: Die Festlegung hat den Wert geändert (nur gewarnte Tage, 2,25 % statt 3 %),
   nicht die Verteilung. Auch nach dem Ersetzungspfad bleibt je DWD-Gebiet \(V\) ein einheitlicher
   Anteil, weil \(\hat P\) beide Gruppen im gleichen Verhältnis hebt und jedes DWD-Gebiet in genau
   einer Modellregion \(R\) liegt ([72], §3.3); er unterscheidet sich dann nur zwischen Gebieten. Das ist eine **Modellgrenze der Abschätzung**, kein Grund für eine
   Nullwirkung; Ersetzungspfad: gemessene Effektgröße aus einer Vorher-Nachher-/DiD-Auswertung
   (Differenz-von-Differenzen mit Vergleichskommunen ohne Warnkanal, §5.1) von
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
  band: null   # Standardabweichung (SD) und Standardfehler (SE) je Zeile in der CSV, §3.1; Birke-Marker-Offset bis −1,3 Tage (§3.1)
  herkunft: register:96-W025-01
  quelle: dwd_cdc_phaenologie_jahresmelder
  preisstand: null
  bandzuordnung: [u20, 20-64, 65-74, 75-84, 85+]
  endpunkt: morbiditaet
  kennzeichnung: quelle   # amtliche DWD-Messreihe [33], ausgewertet mit Anlage [67]
  abgeleitet_aus: []
parameter:
  id: pollen.a_attr
  wert: 0.27
  einheit: "-"
  band: [0.19, 0.41]
  herkunft: register:96-W025-02
  quelle: anderegg2021
  preisstand: null
  bandzuordnung: [u20, 20-64, 65-74, 75-84, 85+]
  endpunkt: morbiditaet
  kennzeichnung: abschaetzung_kap3   # Herleitung Kap. 2 (96-W025-02): Mitte des IQR 19–35 % der Saisonlaenge 1990–2018 aus Anderegg 2021 [9], Results; Band 0,19–0,41 umfasst beide Laengen-Spannen (Befund 258)
  abgeleitet_aus: []
parameter:
  id: pollen.p_ar
  wert: {u20: 0.088, 20-64: 0.132, 65-74: 0.067, 75-84: 0.050, 85+: 0.050}
  einheit: "-"
  band: null   # 80–84 und 85+ extrapoliert ueber das DEGS1-Ende 79 (gekennzeichnet, §3.2)
  herkunft: register:96-R35-01
  quelle: langen2013_thamm2018_destatis2023
  preisstand: null
  bandzuordnung: [u20, 20-64, 65-74, 75-84, 85+]
  endpunkt: morbiditaet
  kennzeichnung: quelle   # DEGS1/KiGGS W2 [1,2]; 80–84 und 85+ extrapoliert, gekennzeichnet in 3.2
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
  # Baustein der Ebene POLLEN_LOAD (Detailspezifikation in §3.3).
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
  # (Katalog POLLEN_EARLY_WARNING, default_reduction). Code-Stand 29.09.2026:
  # default_reduction = 0,03 (backend/app/data/catalog.py); seit 27.09.2026 mit
  # #96 verknuepft ueber das Zelllauf-Modell s158, nie als pauschaler Faktor
  # (Integrationsauflage S158 in §5.1; Ledger-Befunde 151, 178, 215, 231).
  # Kettenprodukt 0,35 x 0,40 x 0,20 = 0,028, gerundet 0,03 (§5.1); der Kommentar
  # an der wert-Zeile meint diese Rundung (Befund 220).
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
  # Anteil gewarnter Zusatztage fuer S158 (Log 23): Tage mit DWD-Pollenflug-
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
  band: [266.90, 1018.6]   # Obergrenze Schramm (moderate-schwere SAR); Kinder 1.027–1.335 (§3.5)
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
  kennzeichnung: berechnet   # = f x (p_B L_B + p_G L_G) = 0,70 x (0,55 x 30 + 0,75 x 60) = 43,05 (§3.5)
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

### 7.1 Kosten der Maßnahmen (keine Größe der Schadens- oder Wirkungsrechnung)

Die Blöcke oben tragen die Rechnung vom Klimasignal bis zum Euro-Betrag und die Wirkung der Maßnahmen. Der
Block hier trägt nur die Kosten einer Maßnahme: Er ändert weder den Schadensbetrag von #96 noch die vermiedenen
Tage, sondern nur die Wirtschaftlichkeit im Maßnahmen-Modul (§5, Absatz „Kosten der Stadtbaumwahl“, Befund 253).
Mit ihm führt Kapitel 7 14 Blöcke (Log 25, Log 27).

```yaml
parameter:
  # Kosten der Stadtbaumwahl je ersetztem Baum (Vorgabe P2, Befund 253). Katalog
  # LOW_ALLERGEN_TREE_SELECTION, Kostenfeld je Stueck (Uebernahme Ue-11).
  # vorgezogen = Pflanzung mit dreijaehriger Anwuchspflege 3.636 (Hamburg 2024 [75],
  # Band 2.400-5.600) + Faellung 800 (Abschaetzung von KAP3: geometrisches Mittel des
  # Bands 400-1.600, Bandenden aus den Arbeitsschritten, in den durchsuchten Quellen
  # keine Kostenangabe je Baum, Liste in Befund 253);
  # nachpflanzung = Mehrkosten der Artenwahl im typischen Fall Linde statt Birke,
  # Preisgruppe II - I = 455 - 395 [79] (Birke meistgefaellt [78], [82]; Linde meistgepflanzt
  # [78], [82], allergen "Low" [81]); Band 0 (Linde statt Hainbuche, beide II) bis
  # IV - I = 185. Das Produkt fragt den Fall ab, keine stille Vorgabe (Ue-11).
  # Herleitung §5 #stadtbaum-kosten, Log 27.
  id: pollen.stadtbaum_kosten
  wert: {vorgezogen: 4436, nachpflanzung: 60}
  einheit: "EUR/Baum"
  band: {vorgezogen: [2800, 7200], nachpflanzung: [0, 185]}   # Bandenden addiert (vorgezogen)
  herkunft: herleitung:#stadtbaum-kosten
  quelle: hamburg_drs23_294_leick2024   # Pflanzkosten [75], Preisgruppen [79], Arten [78], [81], [82]; Faellung ohne Quelle
  preisstand: "2024"
  bandzuordnung: null   # Kosten der Kommune, keine Altersbaender
  endpunkt: null        # kein Endpunkt: wirkt nicht auf Tage oder Schadensbetrag
  kennzeichnung: abschaetzung_kap3   # Pflanzkosten belegt [75]; Faellung und Artenwahl abgeschaetzt
  abgeleitet_aus: []
```

## 8 Quellen (§3.8 — #96-relevanter Auszug; Nummern [1]–[56] = M0-Zählung, [65]–[82] neu)

Zugriff 17./18.08.2026 ([1]–[3], [65], [66]: 30.08.2026, Volltext/Abstract gegengelesen). Nennt ein Eintrag ein
eigenes Abrufdatum, gilt dieses.
**Archiv-Snapshots:** wie #95 (Kap. 8) — Wayback-Permalinks stehen an der Quelle;
wo keiner steht, sind DOI-/amtliche Links die persistenten Referenzen.

- **[1]** U. Langen, R. Schmitz, H. Steppuhn, „Häufigkeit allergischer Erkrankungen in
  Deutschland (DEGS1)", Bundesgesundheitsbl 56(5–6):698–706, 2013. doi:10.1007/s00103-012-1652-7
  — **Tab. 3** (12-Monats-Prävalenz Heuschnupfen gesamt: 14,6/17,2/14,4/10,1/8,2/5,0 % für
  18–29/30–39/40–49/50–59/60–69/70–79; gesamt 12,0 %; Volltext gegengelesen 30.08.2026; 40–49 Jahre am Textabbild
  `docs/quellen/methodik/96/01_Langen2013_DEGS1_Allergien.md` berichtigt 26.09.2026, Befund 188).
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
  Gesundheit). doi:10.25646/11648 — Spreizungs-Mechanismus wörtlich (S. 90:
  „Spreizung der Pollensaison … Verlängerung [der Expositionszeit]"); Birkenpollengruppe (S. 89);
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
  American pollen seasons", PNAS 118(7):e2013284118, 2021. doi:10.1073/pnas.2013284118.
  Abstract: „Human forcing of the climate system contributed ∼50 % (interquartile range: 19–84 %)
  of the trend in pollen seasons and ∼8 % (4–14 %) of the trend in pollen concentrations.“ Results and Discussion, Absatz zu Abb. 1: „We also
  found significant advances of ∼20 d in pollen season start date and lengthening of the pollen season by ∼8 d over
  the same period“. Results and Discussion, Absatz zu Abb. 3: „Anthropogenic forcing contributed to an estimated
  35–66 % (interquartile range) of the full trend and 45–84 % of the recent trend in pollen season start date and
  19–35 % and 22–41 % of the trend in pollen season length over the 1990–2018 and 2003–2018 periods, respectively
  (Fig. 3).“ Abb. 3: „Data are plotted from 22 climate models“. Zitate wörtlich, nur das Prozentzeichen nach kap3-stil mit
  Leerzeichen. Die rund 50 % des Abstracts gelten Beginn und Länge
  zusammen; für die Länge nennt der Text nur die Spannen, keinen einzelnen Wert für die Mitte der Schätzungen (gelesen: Significance, Abstract, Einleitung, Results and
  Discussion, Methods). Der Bericht nimmt deshalb die Mitte der Spanne 1990–2018, 0,27 (Kap. 2, Befund 258).
  Significance: „We use an ensemble of climate models to test the role of climate change and find that it is the
  dominant driver of changes in pollen season length and a significant contributor to increasing pollen
  concentrations.“ Der Satz nennt keine Zahl; beziffert ist der Anteil nur mit den Spannen oben, und [9] nennt sie
  selbst „likely conservative estimates“ (Results and Discussion). Der Klimaanteil 0,27 ist damit eher zu niedrig als
  zu hoch angesetzt, in derselben Richtung wie §4.
  Textabbild `docs/quellen/methodik/96/09_Anderegg2021_Pollensaison.md` (Abruf 30.09.2026, SHA-256 d02d5a7b…f903).
  Volltext frei bei Europe PMC (PMC7896283), https://europepmc.org/articles/PMC7896283.
- **[10]** C. Ziello u. a., „Changes to Airborne Pollen Counts across Europe", PLoS ONE
  7(4):e34076, 2012. doi:10.1371/journal.pone.0034076
- **[15]** UBA (Hrsg.), KWRA 2021, Teilbericht 5: Risiken und Anpassung in den Clustern Wirtschaft
  und Gesundheit (Climate Change 24/2021, Dessau-Roßlau, Juni 2021), Kap. 4.2.2 (Aeroallergene;
  Indikator GE-KL-07, Blühbeginn der Erle, S. 176; Bezugsperiode 1971–2000 und 15./85. Perzentil des
  RCP8.5-Ensembles S. 177; Projektion „um rund zwei Wochen früher“ bis Ende des Jahrhunderts S. 178; Tabelle 55 Klimarisiko ohne
  Anpassung und Gewissheit, S. 179; beschlossene Maßnahmen APA III, S. 180),
  https://www.umweltbundesamt.de/publikationen/KWRA-Teil-5-Wirtschaft-Gesundheit (Abruf 26.09.2026; Permalink
  https://web.archive.org/web/20260519124624/https://www.umweltbundesamt.de/publikationen/KWRA-Teil-5-Wirtschaft-Gesundheit)
  (lokal: `docs/KWAR/kwra2021_teilbericht_5_cluster_wirtschaft_gesundheit_bf_211027_0.pdf`; Seitenzahlen
  = PDF-Seiten = Druckseiten). Aufbereitet in `docs/KWAR/KWRA-2021_Klimawirkungen.xlsx`, Blatt
  `Klimawirkungen`, Zeile 98.
- **[19]** Destatis, VPI für Deutschland, lange Reihen (2020 = 100): 2000 = **75,9** ·
  2014 = **94,0** · 2022 = 110,2 · 2023 = 116,7 · 2024 = 119,3 (Statistischer Bericht „VPI lange Reihen",
  destatis.de; Werte gegen die publizierte Basis-2020-Tabelle geprüft 30.08.2026). Der Wert 2022 (Kosten der
  Stadtbaumwahl, §5) aus der Tabelle „Verbraucherpreisindex: Gesamtindex und 12 Abteilungen“, Jahresdurchschnitte,
  Stand 10.09.2026, https://www.destatis.de/DE/Themen/Wirtschaft/Preise/Verbraucherpreisindex/Tabellen/Verbraucherpreise-12Kategorien.html
  (Abruf 29.09.2026; Permalink https://web.archive.org/web/20260922153607/https://www.destatis.de/DE/Themen/Wirtschaft/Preise/Verbraucherpreisindex/Tabellen/Verbraucherpreise-12Kategorien.html);
  dieselbe Tabelle bestätigt 2023 = 116,7 und 2024 = 119,3.
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
  22.08.2026 über die GENESIS-REST-Schnittstelle der Regionaldatenbank (GENESIS-WS-2020,
  `data/tablefile`, ffcsv) mit angemeldetem Konto; der Gastzugang antwortet mit 401 (geprüft 26.09.2026),
  deshalb ist das Original nicht archiviert, und die Werte sind aus den Altersjahren von [69]
  nachgerechnet (`docs/quellen/methodik/96/QUELLEN.md`); https://www.regionalstatistik.de/genesis//online?operation=table&code=12411-09-01-4-B;
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
  Belastungsschwelle der S158-Festlegung (§5.1). Abgelegte Textabbilder:
  `docs/quellen/methodik/96/70_DWD_Pollen_Einstufung_live_20260926.md` (Abruf 26.09.2026),
  `docs/quellen/methodik/96/70_DWD_Pollen_Einstufung_Wayback_20260223.md` (Wayback-Stand 23.02.2026),
  dazu `docs/quellen/pollen/dwd_einstufung_belastungsintensitaeten_live.txt` (Hasel Z. 14, Birke Z. 17,
  Gräser Z. 18) und `docs/quellen/pollen/dwd_einstufung_belastungsintensitaeten_wayback_20260223181518.txt`.
- **[71]** Deutscher Wetterdienst, „Pollenflugstatistik“ (Zehntagesmittel des Anteils der
  Meldungen je Belastungsstufe, je Pollenart und Gebiet, 1997–2026; Daten Stiftung Deutscher
  Polleninformationsdienst), https://www.dwd.de/DE/leistungen/pollen/pollenstatistik.html
  (Abruf 26.09.2026; Permalink https://web.archive.org/web/20260310113821/https://www.dwd.de/DE/leistungen/pollen/pollenstatistik.html).
  Liefert den Anteil \(m_{g,V}\) aller Tage ab „mittel“; Ersetzungspfad für den Anteil gewarnter
  Symptomtage \(t_{\text{warn},g,V} = \min(1;\ m_{g,V}/f)\) je DWD-Gebiet \(V\) (§5.1); der Bericht wertet sie
  nicht aus (Modellgrenze 8).
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
- **[73]** Kahlenborn, W.; Linsenmeier, M.; Porst, L. u. a. (adelphi, Eurac Research, Bosch & Partner, GWS,
  BBSR, DWD, BfG, BSH): Klimawirkungs- und Risikoanalyse 2021 für Deutschland, Teilbericht 1: Grundlagen.
  Hrsg. Umweltbundesamt, Climate Change 20/2021, Dessau-Roßlau, Juni 2021 (sprachliche Korrekturen Oktober
  2021); Forschungskennzahl 3717 48 102 0. S. 68 mit Fußnote 7 (nur
  bestehende und umgesetzte Anpassung im Zustand ohne Anpassung; optimistischer und pessimistischer Fall;
  Gegenwart der qualitativen Bewertung),
  https://www.umweltbundesamt.de/publikationen/KWRA-Teil-1-Grundlagen (Abruf 26.09.2026; Permalink
  https://web.archive.org/web/20260311080137/https://www.umweltbundesamt.de/publikationen/KWRA-Teil-1-Grundlagen)
  (lokal: `docs/KWAR/kwra2021_teilbericht_1_grundlagen_bf_211027_0.pdf`, Druckseite 68 = PDF-Seite 69).
- **[74]** T. T. Hugg, J. Hjort, H. Antikainen, J. Rusanen, M. Tuokila, S. Korkonen, J. Weckström,
  M. S. Jaakkola, J. J. K. Jaakkola, „Urbanity as a determinant of exposure to grass pollen in Helsinki
  Metropolitan area, Finland“, PLoS ONE 12(10):e0186348, 2017. doi:10.1371/journal.pone.0186348 (PMC5638505),
  https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0186348 (Abruf 26.09.2026; Permalink
  https://web.archive.org/web/20250629111255/https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0186348).
  Gräser, je acht Messstellen in Helsinki und Espoo entlang eines Stadt-Land-Gefälles; Tabelle 3, S. 6 (Mittelwerte
  je Messstelle, Pollen je m³): Helsinki 1 „Most urban“ 2,55/4,38, Espoo 1 „Most urban“ 3,59/5,40
  (vormittags/nachmittags); Abstract, S. 1; Conclusions, S. 13. Beleg der Lesart von λ als Anteil der örtlichen
  Quellen (Log 26, Modellgrenze 7). **Rechnung von KAP3 aus Tabelle 3:** Der Hintergrund ist die städtischste
  Messstelle, verglichen wird mit dem Mittel aller acht Messstellen; λ = 1 − Hintergrund ÷ Mittel. Mittel aller acht:
  Helsinki 5,79 (vormittags) und 5,61 (nachmittags), Espoo 26,41 und 84,92 Pollen je m³. Damit Helsinki
  1 − 2,55 / 5,79 = 0,56 und 1 − 4,38 / 5,61 = 0,22, Espoo 1 − 3,59 / 26,41 = 0,86 und 1 − 5,40 / 84,92 = 0,94:
  abgeleitet 0,22–0,94, drei von vier Werten im Band 0,3–1,0 (§3.3, Modellgrenze 7, Log 26).
- **[75]** Bürgerschaft der Freien und Hansestadt Hamburg, Drucksache 23/294 vom 13.05.2025, Schriftliche Kleine
  Anfrage des Abgeordneten Sandro Kappe (CDU) vom 05.05.2025 und Antwort des Senats, „Stadtgrün, Klimaschutz und
  nachhaltige Stadtentwicklung: Herausforderungen und Handlungsfelder in Hamburg“, Antwort zu Frage 11, S. 4: „Die
  Pflanzkosten für Straßenbäume im Jahr 2024 lagen in Abhängigkeit von den jeweiligen Bedingungen am Pflanzort
  zwischen 2.400 Euro und 5.600 Euro. Der Durchschnittswert liegt rechnerisch bei 3.636 Euro.“
  https://www.buergerschaft-hh.de/parldok/dokument/90909/23_00294_stadtgruen_klimaschutz_und_nachhaltige_stadtentwicklung_herausforderungen_und_handlungsfelder_in_hamburg
  (Abruf 29.09.2026; Permalink https://web.archive.org/web/20260929162654/https://www.buergerschaft-hh.de/parldok/dokument/90909/23_00294_stadtgruen_klimaschutz_und_nachhaltige_stadtentwicklung_herausforderungen_und_handlungsfelder_in_hamburg).
  Pflanzung mit Anwuchspflege, Kosten der Stadtbaumwahl (§5, Kap. 7 `pollen.stadtbaum_kosten`).
- **[76]** Bürgerschaft der Freien und Hansestadt Hamburg, Drucksache 23/5166 vom 08.09.2026, Schriftliche Kleine
  Anfrage des Abgeordneten Sandro Kappe (CDU) vom 31.08.2026 und Antwort des Senats, „Umwelt-, Klima- und
  Infrastrukturpolitik in Hamburg – Sachstände, Kosten und konkrete Umsetzung“, Antwort zu Frage 11, S. 6: „Die
  durchschnittlichen Pflanzkosten für das Jahr 2025 betrugen 3.120 Euro. Pflanzung und Pflege werden nicht getrennt
  ausgewiesen, siehe hierzu Drs. 22/339 beziehungsweise zuletzt Drs. 23/2662.“
  https://www.buergerschaft-hh.de/parldok/dokument/105068/23_05166_umwelt_klima_und_infrastrukturpolitik_in_hamburg_sachstaende_kosten_und_konkrete_umsetzung
  (Abruf 29.09.2026; Permalink https://web.archive.org/web/20260929162705/https://www.buergerschaft-hh.de/parldok/dokument/105068/23_05166_umwelt_klima_und_infrastrukturpolitik_in_hamburg_sachstaende_kosten_und_konkrete_umsetzung).
- **[77]** Bürgerschaft der Freien und Hansestadt Hamburg, Drucksache 22/339 vom 23.06.2020, Große Anfrage der
  Abgeordneten Sandro Kappe u. a. (CDU) und Fraktion vom 26.05.2020 und Antwort des Senats, „Die Pflicht kommt vor der
  Kür – Wie viele gefällte Bäume wurden unter dem rot-grünen Senat in Hamburg nicht nachgepflanzt?“. Vorbemerkung,
  S. 1: „Fällkosten werden im Rahmen der Pflege und Unterhaltung für öffentliche Flächen in den Bezirksämtern nicht
  gesondert erhoben. In der Regel handelt es sich um große Ausschreibungen, die Baumpflege und Baumfällungen gemeinsam
  enthalten.“ Antwort zu Fragen 5 und 6, S. 4: „In den Pflanzkosten ist die Fertigstellungs- und Entwicklungspflege
  für in der Regel drei Jahre enthalten.“
  https://www.buergerschaft-hh.de/parldok/dokument/70465/die_pflicht_kommt_vor_der_kuer_wie_viele_gefaellte_baeume_wurden_unter_dem_rot_gruenen_senat_in_hamburg_nicht_nachgepflanzt.pdf
  (Abruf 29.09.2026; Permalink https://web.archive.org/web/20240706153940/https://www.buergerschaft-hh.de/parldok/dokument/70465/die_pflicht_kommt_vor_der_kuer_wie_viele_gefaellte_baeume_wurden_unter_dem_rot_gruenen_senat_in_hamburg_nicht_nachgepflanzt.pdf).
- **[78]** Abgeordnetenhaus Berlin, Drucksache 19/13426, Schriftliche Anfrage des Abgeordneten Danny Freymark (CDU)
  vom 28.09.2022 „Straßenbäume in Berlin“ und Antwort der Senatsverwaltung für Umwelt, Mobilität, Verbraucher- und
  Klimaschutz vom 12.10.2022, Antwort zu 4, S. 6 (PDF-Seite 7): „Im Rahmen der Stadtbaumkampagne kostet derzeit eine
  Straßenbaumpflanzung einschließlich einer rd. dreijährigen Entwicklungspflege etwa 3.000 Euro brutto (Ausschreibung
  Herbst 2022).“ https://pardok.parlament-berlin.de/starweb/adis/citat/VT/19/SchrAnfr/S19-13426.pdf
  (Abruf 29.09.2026; Permalink https://web.archive.org/web/20250719053309/https://pardok.parlament-berlin.de/starweb/adis/citat/VT/19/SchrAnfr/S19-13426.pdf).
  Gegenprobe der Pflanzkosten für die Beispielkommune (§5). Anlagen (GRIS-Auszüge der Senatsverwaltung):
  „Bestandsveränderung in Berlin und den Bezirken einschl. Zu- und Abgänge 2021“, Stand 31.12.2021, PDF-Seite 17,
  Zeile Berlin gesamt: Bestand 01.01. 430.358, Neupflanzungen 2.972, Fällungen 6.269, Bestand 31.12. 432.769;
  „Bestand nach Hauptgattungen in den Berliner Bezirken“, Stand 31.12.2021, PDF-Seite 24, Zeile Berlin gesamt:
  Linde 151.764 (35 %), Ahorn 87.341, Eiche 38.700, Platane 24.737, Kastanie 20.380, Birke 12.209, Robinie
  10.802. Mittlere Standzeit und Artenwahl der Stadtbaumwahl (§5).
- **[79]** Leick Pflanzen & Gärten (Baumschule), Preisliste „gültig ab dem 14.02.2024“, Laubbäume, S. 26 f.
  (PDF-Seiten 27 und 28): Preis je Stück nach Stammumfang in 1 m Höhe, 18–20 cm: Preisgruppe I 395,00 €,
  II 455,00 €, III 485,00 €, IV 580,00 €. Artenzeilen (Name, Preisgruppe, darunter der deutsche Name), PDF-Seite 27
  (gedruckt S. 26): „Betula pendula I“ / „Weißbirke“; „Carpinus betulus II“ / „Weißbuche, Hainbuche“; „Corylus
  colurna II“ / „Baumhasel“. PDF-Seite 28 (gedruckt S. 27): „Robinia pseudoacacia 'Frisia' II“ / „Goldakazie“;
  „Robinia pseudoacacia 'Umbraculifera' I“ / „Kugelakazie“; „Tilia cordata 'Greenspire' II“ / „Winterlinde
  'Greenspire'“; „Tilia platyphyllos II“ / „Sommerlinde“. Beide Seiten tragen die Preistabelle „18 – 20 395,00
  455,00 485,00 580,00“. Ob die Preise die Umsatzsteuer enthalten, nennt die Liste nicht.
  https://www.leick.de/wp-content/uploads/2022/03/Preisliste_2022.pdf (Dateiname von 2022, Inhalt ab 14.02.2024;
  Abruf 29.09.2026; Permalink der zitierten Fassung https://web.archive.org/web/20260929162721/https://www.leick.de/wp-content/uploads/2022/03/Preisliste_2022.pdf;
  der ältere Wayback-Stand vom 27.11.2022 zeigt die Vorgängerliste). Mehrkosten der Artenwahl (§5).
- **[80]** F. K. Larsen, P. Kristoffersen, „Tilia’s Physical Dimensions Over Time“, Journal of Arboriculture
  28(5):209–214, 2002. doi:10.48044/jauf.2002.031. S. 209, Materials and Methods: „If tree size at the time of
  establishment was not known, then 10 years, which corresponds to a trunk circumference of 18 to 20 cm (7 to 8 in.),
  was added to the age.“ S. 211, Table 3, Growth formulas: „Crown radius, shaded 0.1358 –0.0008“ (b1, b2; Linden in
  Reihen in Kopenhagen, n = 463, r² = 0,9356; r² heißt Bestimmtheitsmaß: der Anteil der Streuung der Messwerte, den die Formel erklärt, 1 hieße vollständig). Die Formel ist nach dem Methodenteil Y = b1 × d + b2 × d² mit
  d = Alter; die Fußnote von Table 3 („Y = b1 + b2d²“) lässt das erste d aus, Table 2 (Wachstumsraten
  b1 + 2 × b2 × d: 0,1358 und −0,0016) bestätigt die Lesart. https://auf.isa-arbor.com/content/isa/28/5/209.full.pdf
  (Abruf 29.09.2026; Permalink https://web.archive.org/web/20260425090058/https://auf.isa-arbor.com/content/isa/28/5/209.full.pdf).
  Kronenwachstum für die Amortisation der Nachpflanzung (§5).
- **[81]** P. Cariñanos, F. Grilo, P. Pinho u. a., „Estimation of the Allergenic Potential of Urban Trees and Urban
  Parks: Towards the Healthy Design of Urban Green Spaces of the Future“, Int J Environ Res Public Health
  16(8):1357, 2019. doi:10.3390/ijerph16081357 (PMC6517926; in [6] als Nr. 104 zitiert). Table 3 „Attributes,
  origin, allergenicity and hardiness zones of the 20 most-frequent species in Mediterranean parks“, Spalte
  Allergenicity Level: „Tilia cordata … Low“, „Tilia platyphyllos … Low“, „Robinia pseudoacacia … Low“,
  „Acer campestre … Moderate“. Abschnitt 4 (Discussion): „Linden (Tilia spp.) is widely used in walk-alignments,
  so that its moderate allergenicity can be increased when forming dense groups“ (Befund 256).
  https://www.mdpi.com/1660-4601/16/8/1357 (Abruf des Volltexts 29.09.2026 über
  Europe PMC, https://www.ebi.ac.uk/europepmc/webservices/rest/PMC6517926/fullTextXML; Permalink
  https://web.archive.org/web/20260425042213/https://www.mdpi.com/1660-4601/16/8/1357). Lizenz CC BY 4.0.
  Allergenes Potenzial der Ersatzarten (§5).
- **[82]** Landeshauptstadt Hannover, „Stadtbäume der Landeshauptstadt Hannover. Jahresbericht 2023/2024“, Anlage 1
  zu einer Drucksache, Sachgebiet 67.33, Stand 12.11.2025. S. 9, Abb. 10 „Anteile der Haupt-Straßenbaumarten 2024“
  (Hainbuche 4 %, Linde 24 %, Eiche 22 %); S. 10: „Von den in den letzten beiden Jahren neu gepflanzten 1.054 jungen
  Straßenbäumen waren 184 Linden“; S. 19, Fällungen: „Bei den Straßenbäumen mussten auffällig häufig Birken
  (66 Stück = über 10 % des Gesamtbestands) gefällt werden“.
  https://www.hannover.de/content/download/1059971/file/Jahresbericht%20Stadtb%C3%A4ume%202023-2024%20Anlage.pdf
  (Abruf 29.09.2026; Permalink https://web.archive.org/web/20260515080623/https://www.hannover.de/content/download/1059971/file/Jahresbericht%20Stadtb%C3%A4ume%202023-2024%20Anlage.pdf).
  Welche Bäume ersetzt und welche gepflanzt werden (§5).

## Entscheidungslog

Einträge 1: M0-Entscheidung (rückwirkend dokumentiert). Einträge 2–16: Rev.-1-Entscheidungen
(`/risiko-auto 96`, Gate 1, 30.08.2026); Eintrag 17: Revision nach Review-Runde 1 (Befund 101);
**Einträge 18–19: Rev. 2 (31.08.2026)** — Bezugsebene der P̂-Zentrierung (Nutzer-Entscheid,
Aufgabe §3.2) und die daraus folgende Fixierungs-/Maßnahmenfrage.
**Eintrag 20: Rev. 3 (08.09.2026)** — Wirkungsabschätzung des S158-Hebels nach Vorgabe P2 des
Aufsichtsrats (F-0007 Punkt 1); bewusste Überstimmung von Eintrag 15 (Ledger-Befund 151).
**Einträge 21–22: Fortschreibung 7 (25.09.2026, T-1238)** — Kapitel 9 entfällt (Ledger-Befund
152), Rechenkette §3.0 (Ledger-Befund 153).
**Einträge 23–24: Fortschreibung 7, Schritt 2 (26.09.2026, T-1239)** — S158 nach Tagen und Belastung,
allergenarme Stadtbaumwahl als Abschätzung je Zelle (Ledger-Befunde 156–167).
**Eintrag 25: Fortschreibung 7, Schritt 3 (26.09.2026, T-1240)** — Kennzeichnung der Parameter-Blöcke (Ledger-Befunde
168–181).
**Eintrag 26: Rev. 4 (26.09.2026, T-1362)** — Bezugswert Ḡ₀ im Ausgangsstand festgehalten;
bewusste Überstimmung von Eintrag 19 (Ledger-Befund 182).
**Eintrag 27: Runde 27 (29.09.2026, T-1635)** — Kosten der Stadtbaumwahl nach Vorgabe P2 (Ledger-Befund 253);
Vermerk an Eintrag 25 zur Zahl der Blöcke.
**Überstimmungsweg für alle Einträge:** „Entscheidung Nr. X ändern auf …" → Delta-Lauf
(Neurechnung betroffener Kopplungen + Re-Review + PDF-Neuexport). ⚠ = Ermessensfall.

| Nr | Frage | angewendete Entscheidung | Begründung | Alternative | Auswirkung |
|---|---|---|---|---|---|
| 1 | Methodischer Ansatz für #96? | **96-A** Prävalenz × gemessene Saison-Spreizung (Familie K1-Gesundheit bottom-up) | einziger Ansatz, der das Gesamtrisiko abdeckt und mechanistisch attribuiert (M0 Kap. 5) | 96-B (Modul ab M1); 96-C per §3.1 ausgeschieden | Gesamtmodell |
| 2 ⚠ | Klimasignal-Konstruktion? | **Spreizung zwischen Saison-Markern** (Erle→Birke; Fuchsschwanz→Knäuelgras), gemessen aus gepaarten DWD-Stationen | reine Verschiebung erzeugt keine Zusatztage; Spreizung ist messbar und RKI-konform [6]; behebt Rev.-5-Befund 11 (ΔS/S_ref nicht hergeleitet) | M0-Ratio ΔS/S_ref aus Trend-Zitaten (nicht reproduzierbar) | Klimasignal G14-fest; δ = 1,07 Tage (DE-gewichtet, §3.3) statt implizit ~4–5 Tage in M0 (verworfen) |
| 3 ⚠ | Birken-Marker? | **Phase 4 (Blattentfaltung)** — Phase 5 hat Meldelücke 1960–1990; Offset-Diagnose (+3,29 Tage; Trend bis zu ≈ 1,3 Tage, §3.1) ins Band | einzige durchgängige Birken-Reihe; Offset kürzt sich in der Spreizungs-Differenz bis auf den Trend | Phase 5 (Meldelücke 1960–1990, §3.1) oder Literaturwert | ΔS_B-Band: untere Bandgrenze bis zu ≈ 1,3 Tage tiefer (§3.1) |
| 4 ⚠ | Gräser-Saisonende? | **konstant** (nur Sukzessions-Spreizung Fuchsschwanz→Knäuelgras) | kein Phänologie-Marker fürs Saisonende; Herbst-Verlängerung [6] bewusst nicht angesetzt | Literatur-Zuschlag für Herbst-Verlängerung | Untergrenze (§6 Grenze 1) |
| 5 | Regionenzuschnitt? | **Bundesland → N/M/S wie #95** (`health.REGION_BY_BUNDESLAND`) | Produktkonsistenz; ΔS-Regionalstreuung −17 % bis +24 % (δ −5 % bis +6 %, Kap. 4) | Naturraumgruppen (feiner) | einheitliche Regionslogik |
| 6 ⚠ | Kalibrierfaktor? | **c_kal ≡ 1 — dokumentierte Ausnahme** von §3.4: keine amtliche Anker-Zeitreihe existiert [66]; Modell voll messungs-/prävalenzverankert; Sanity-Bänder ersetzen den Fit | ein Fit ohne Anker wäre Scheinkalibrierung; BT-Drs. belegt die Lücke | J30-KKR-Anker bei Integration interaktiv ziehen (Registry-Vermerk) | kein Fit-Schritt; §4-Bänder tragen die Validierung |
| 7 ⚠ | f-Herleitung? | **Modellannahme 0,70 (0,50–0,85)**; Pfaar-r nur qualitativ; Bastl [53] geprüft — liefert die Größe nicht | behebt Kategorienfehler (Rev.-5-Befund 14) exakt entlang des Gegenprüfungs-Vorschlags | f aus PHD-Tagesdaten (Ersetzungspfad) | nur nativer Ausweis −28,6 % bis +21,4 % (§3.4); € unabhängig von f (§3.5) |
| 8 ⚠ | p_B/p_G? | **0,55/0,75 als gekennzeichnete Abschätzung** (Rangfolge-Stütze [3]); additive Saisonform als €-konservativ dokumentiert | Anteil unter AR-Patienten nicht publiziert (Befund 36a); Überlappungskorrektur würde € erhöhen (36b) | PID-/Versorgungsdaten (Ersetzungspfad) | δ: p_B −11,7 % bis +11,7 %, p_G −11,4 % bis +7,6 %, zusammen −23 % bis +19 % (Region Mitte, §3.4); Euro nur −6 % bis +8 % (Kap. 1, Absatz „Warum die eigene Quellenlage …“) |
| 9 ⚠ | Kostensatz-Basis? | **TOTALL 266,90 €₂₀₂₄ (populationsbasiert)**; Schramm nur Obergrenze/Kinder-Band | Schramm (moderate–schwer) auf alle Betroffenen = bekannte Überschätzung um grob Faktor 4 (§3.5) — verletzt Untergrenzen-Zusage (#95-Befund-62-Lehre); impliziter Baseline-Check §4 bestätigt | Schramm als Basis (M0-Linie; 9,1 Mrd. implizite Basis, Kap. 4 — verworfen) | € −74 % ggü. Schramm-Basis (§3.5) |
| 10 ⚠ | Prävalenz-Bänder? | **u20-Ebene neu** (Zensus 5er-Jahresgruppen 0–4, 5–9, 10–14, 15–19); 18/19 mit KiGGS-Wert (unterschätzend); 75–84 und 85+ = 5,0 %, davon 80–84 und 85+ extrapoliert (gekennzeichnet, §3.2) | behebt Rev.-5-Befunde 27/35 entlang Variante (a) der Gegenprüfung | Misch-Prävalenz je Zelle ohne u20-Ebene | Alterslast korrekt verteilt |
| 11 | Attribution? | **a_attr = 0,27 (Band 0,19–0,41), Abschätzung von KAP3** [9] | Mitte der Spanne 19–35 % für die Saisonlänge 1990–2018 aus [9] (Results and Discussion, Absatz zu Abb. 3), weil ΔS eine Verlängerung der Saison ist (§3.1); die rund 50 % im Abstract von [9] gelten Beginn und Länge zusammen, einen Wert für die Mitte der Länge nennt [9] nicht (Kap. 2, Kap. 8, Befund 258); das Band umfasst beide Spannen der Länge (19–35 % und 22–41 %) | 0,50 aus dem Abstract (verworfen, Befund 258: gilt Beginn und Länge zusammen) · 1,0 (volle Anrechnung — nicht belegbar) | zentraler Hebel −30 % bis +52 % (§3.0); Berlin 2,53 Mio. € je Jahr (Kette, §3.0), Bundessumme ≈ 60 Mio. € je Jahr (§4) |
| 12 | Vegetations-Modulation? | **λ = 0,7 (0,3–1,0)** (aktualisiert Runde 2, Befund 110: wörtliche Zuwachs-Lesart der Werchan-Prozente; Verhältnis-Lesart im Band), P̂ in beiden Pfaden; Ḡ₀-Zentrierung §3.3 | Kette #lambda-veg reproduzierbar; Kommunensumme im Ausgangsstand λ-invariant (§3.4; seit Log 18 je Kommune, damit auch die Bundessumme) — Lesart wirkt im Ausgangsstand nur verteilend (mit Maßnahme ist die Senkung proportional zu λ, Log 26) | Verhältnis-Lesart als Basiswert (in M0 λ = 0,6; verworfen, geht als untere Lesart ins Band ein, §3.4) | lokale Differenzierung: \(\hat P\) = 0,65…1,35 bei \(\hat G/\bar G_0\) = 0,5…1,5 (§3.6); zwischen vegetationsarmer Zelle (0,3) und Allee-Zelle (1,7) der Faktor 5,7 (§3.0) |
| 13 | Ambrosia (W024)? | **bewusst inaktiv in M0**, Modul 96-B ab M1 | Zeithorizont 2041–2060 ≠ „heute"; Teilausschnitt | sofortiges Zusatzmodul | Untergrenze |
| 14 | E09 Trockenheit / Intensität? | **bewusst inaktiv** (Register 96-W025-03/-04) | keine quantifizierte ERF; Wirkrichtung erhöhend → konservativ | Sensitivitätsband nach Literatur | Untergrenze |
| 15 | S158 Pollenmonitoring? | **Maßnahmen-Hebel qualitativ** (§3.5); Stadtbaumwahl als mechanischer Hebel über Ĝ quantifiziert — **durch Nr. 20 überstimmt (08.09.2026, Vorgabe P2)**: der Hebel ist jetzt abgeschätzt statt null | keine Interventions-Effektgröße publiziert (Befunde 26/34); ehrlich statt gesetzt | gesetzte Dämpfungsannahme (Rev.-5-„v_monitor" — gestrichen, Befund 32) | Hebelliste ehrlich; Wirkung bis Rev. 2 null |
| 16 | R36 im Basiswert? | **Default 1** (nur Schicht A) | ambulantes Krankheitsbild; keine Evidenz für Distanzeffekt (§3.2) | Sensitivitätsband analog #95-β_d | Basiswert schlanker |
| 17 ⚠ | Ḡ₀-Gewichtsregel (P̂-Zentrierung)? | **betroffenengewichtetes Mittel über bewohnte Zellen** (Formel §3.3; Bezugsebene in Rev. 2 durch Log 18 auf die Kommune festgelegt) | macht die Bundessumme per Konstruktion invariant gegen λ und Ĝ×pop-Korrelation (Befund 101); c_kal ≡ 1 hat keinen nachgeschalteten Fit, der eine Fehlgewichtung auffangen würde | flächen-/zellgewichtetes Mittel (Bundessumme würde mit Ĝ×pop-Korrelation driften) | Sanity-Rechnung §4 exakt; P̂ verteilt im Ausgangsstand nur um (Maßnahmen: Log 26) |
| 18 ⚠ | Bezugsebene der P̂-Zentrierung: Bund oder Kommune? | **die eigene Kommune** — Ḡ₀ = betroffenengewichtetes Mittel über die Zellen der betrachteten Kommune, im Lauf gebildet (kein Registry-/Bundeswert); ohne Referenz P̂ ≡ 1 | (a) **Evidenz-Reichweite**: λ stammt aus intra-urbanen Messungen (Werchan Berlin [54,55], Bogawski [56]) — sie tragen Umverteilung INNERHALB einer Stadt, nicht interkommunale Niveauunterschiede; (b) **Aufgabe §3.2 „geschlossene Betrachtungsebene"** (Fortschreibung 31.08.2026, Nutzer-Entscheid): Referenzmittel nie aus Aggregation über eine höhere Ebene; (c) ein Bundesmittel wäre nur mit einem per §3.4 unzulässigen Bundeslauf bestimmbar | Bundesmittel aus Stichprobe (Rev. 1; verworfen: Skalentransfer unbelegt + Ebenenbruch) · amtlicher Vegetations-Referenzwert (existiert nicht) | Kommunensumme jetzt EXAKT invariant gegen λ (statt näherungsweise); Vegetationsstruktur verschiebt nur INNERHALB der Kommune — interkommunal wirkt sie nicht mehr; die Wirkung ist **nullsummig umverteilend** (betroffenengewichtet erwartungstreu, also im Mittel über die Betroffenen weder zu hoch noch zu niedrig, §3.3), NICHT „konservativ" im Sinne einer Unterschätzung (§3.3(3), Modellgrenze 7); gilt für den Ausgangsstand, Maßnahmen werden am festgehaltenen Ḡ₀ gemessen (Log 26) |
| 19 ⚠ | Ḡ-Fixierung (Befund 113) unter der kommunalen Zentrierung? | **Verworfen durch Log 26 (26.09.2026), weil ein in jedem Lauf neu gebildetes Ḡ jede Senkung durch eine Maßnahme aufhebt und damit die Nullwirkung setzt, die Vorgabe P2 ausschließt.** Ursprüngliche Entscheidung: **kein Pinning** — Ḡ wird in jedem Lauf aus dem aktuellen Vegetationszustand der Kommune gebildet; der flächige Niveaueffekt bleibt bewusst unbuchbar (§5, Modellgrenze 7) | (ursprüngliche Begründung, durch Log 26 überholt) Ein eingefrorener Referenzwert würde einem flächigen Programm einen Niveaueffekt zubuchen, den die λ-Evidenz (intra-urbane Gradienten) nicht trägt — Befund 113 war an das Bundesmittel gebunden und ist mit der kommunalen Zentrierung keine Fixierungs-, sondern eine Evidenzfrage; die Produktmechanik (measure_service skaliert gespeicherte Outcomes) ist KEIN Beleg, sondern begründet die Integrationsauflage: keine pauschal verknüpfte Maßnahme, sonst würde genau der unbelegte Niveaueffekt gebucht (Befund 124/129; Test test_no_flat_measure_on_allergy_days) | Baseline-Pinning je Kommune (verworfen: bucht unbelegten Niveaueffekt) · Emissions-/Ausbreitungsmodell (Ersetzungspfad §6, Datenlage fehlt) | Maßnahme wirkt als Umverteilung (gezielte Hotspot-Entschärfung), nicht als flächiger Niveauhebel |
| 20 ⚠ | S158-Hebel: „qualitativ" (Wirkung null) beibehalten oder abschätzen? | **Abschätzung statt Nullwirkung** — \(r_{\text{S158}}\) = 0,03 (Band 0,005–0,10), Dreifaktor-Kette §5.1, §3.9 ABGESCHÄTZT; Wirkungsort multiplikativ auf ΔTage (Maßnahmen-Modul), Bauform-Grenze als Modellgrenze 8 dokumentiert; Katalogwert `default_reduction` blieb in Rev. 3 zunächst 0,0 (Code-Nachzug L2 nach der P1-Kennzeichnung; überholt, Code-Stand vom 29.09.2026 im Revisionsstand, Befund 245) | **Vorgabe P2 des Aufsichtsrats (F-0007 Punkt 1)** und Aufgabe §3.5 i. d. F. 06.09.2026: Ein Hebel ohne publizierte Effektgröße läuft nicht mehr als „qualitativ" mit Wirkung null; das Fehlen der Studie ist der Anlass der Abschätzung, nicht ihr Ersatz. Bewusste Überstimmung von Log 15 (Ledger-Befund 151) | Log 15 beibehalten (verworfen: widerspricht P2) · Effektzahl aus fremder Domäne übertragen, z. B. Hitzewarn-Effekt aus #95 (verworfen: Kategorienfehler §3.9 — anderer Endpunkt, andere Handlungskette) | Maßnahmen-Ausweis ≈ 2,25 % des K1-Werts (bundesweit ≈ 2,5 Mio. € je Jahr; Band ≈ 0,28–11,0 Mio. €, §5.1); Schadenswert selbst unverändert; Befund-124-Sperre bleibt bestehen, erfüllt über das Zelllauf-Modell `s158` (§5.1, Absatz „Verknüpfung im Zelllauf“; Befunde 231, 254) |
| 21 | Kapitel 9 (Familien-Einordnung und Verworfen-Liste) nach Fortschreibung 7? | **gestrichen**; es bleibt genau eine Methodik (96-A, Familie „K1-Gesundheit bottom-up“ mit Prototyp #95), die verworfenen Ansätze stehen hier | **96-B (Neophyten-Szenario Ambrosia; Lake [23], Born [25], Hamaoui [24])** ersetzt 96-A nicht, weil es nur eine Art abbildet, Birke und Gräser als Hauptlast fehlen und es 2041–2060 statt heute projiziert (Ergänzungsmodul ab M1, Register 96-W024-02, Log 13). **96-C (nationaler Kostenanker, top-down)** ist nach §3.1 ausgeschieden, weil er einen Verteilschlüssel mit Deutschland-Nenner und einen normativ gesetzten Klimaanteil braucht. | Kapitel 9 behalten (verworfen: Fortschreibung 7, eine Methodik je Risiko; Ledger-Befund 152) | keine Zahlenwirkung |
| 22 | Quelle von u20 für die Beispielkommune Berlin in der Rechenkette? | **Direkt aus Tab. 12411-09-01-4-B [68]**: u20 = unter 5 + 5–10 + 10–15 + 15–20 = 673.277, 20–64 = u65 − u20 = 2.288.153; die Zahlen nach Altersjahren stehen gleichlautend in Destatis Tab. 12411-09 [69] | Die Tabelle, aus der Ebene 1 schon u65 und die Seniorenbänder nimmt, führt die vier Gruppen selbst: gleicher Stichtag, gleiche Basis Zensus 2022, und ein Sachbearbeiter, der [68] öffnet, kommt auf dieselbe Zahl. | Anteil u20 aus dem Berliner Landesbericht A I 3 – j / 23 (verworfen: noch auf Basis Zensus 2011, 3.070.537 statt 2.961.430 unter 65-Jährige = 673.277 + 2.288.153 nach §3.0 Ebene 1, Mischung zweier Basen; Runde 0 des Managers, Befund 154). Fundstelle: Amt für Statistik Berlin-Brandenburg, Statistischer Bericht A I 3 – j / 23 „Bevölkerung in Berlin 2023“, Juni 2024, Tab. 3.1, S. 6: 702.852 unter 20-Jährige von 3.070.537 unter 65-Jährigen (Summe der Altersjahre 0 bis 19 und 0 bis 64), Anteil 22,89 %; Adresse und Wayback-Permalink in Ledger-Befund 257 · Bundesanteil 24,07 % (verworfen; Rückfall des Produkts; für Berlin 1.737 Betroffene oder 0,43 % zu wenig, §3.0) | u20 673.277 (§3.0 Ebene 1) statt 677.877 im ersten Entwurf (= 2.961.430 × 702.852 ÷ 3.070.537, Befunde 154, 257); Betroffene 402.103, Tage 408.106, bewerteter Schaden 2,53 Mio. € je Jahr (§3.0) |
| 23 ⚠ | S158: an welchen Tagen und ab welcher Belastung wirkt die Warnung, und gilt \(e_{\text{Tag}}\) je gewarntem Tag? | **Nur an gewarnten Tagen:** DWD-Pollenflug-Gefahrenindex mindestens „mittel“ [70], je Pollengruppe; Anteil gewarnter Symptom-Zusatztage \(t_{\text{warn}}\) = 0,75 (0,50–1,00, §3.9 ABGESCHÄTZT; eigenes Zeichen, weil \(w_B\) das Ĝ-Gewicht ist; Ersetzungspfad \(\min(1;\ m_{g,V}/f)\), nie \(m_{g,V}\) direkt); \(r_{\text{S158}}\) = 0,03 gilt je gewarntem Tag, Formel zellscharf im Zelllauf mit Geltungsbereich \(A_{\text{Zelle}}\) (§5.1) | Die Anker von \(e_{\text{Tag}}\) beschreiben die Minderung an einem Tag, an dem gehandelt wird, also an einem gewarnten Tag; Rev. 3 hat sie auf alle Zusatztage gerechnet und damit \(t_{\text{warn}} = 1\) unterstellt. Befund 124 verbietet eine Wirkung auf alle Tage pauschal. Mit der Tagesauswahl wirkt jede Größe genau einmal (Tage, Menschen, Tageswirkung) | \(e_{\text{Tag}}\) als Mittel über alle Zusatztage lesen und \(t_{\text{warn}}\) weglassen (verworfen: widerspricht den eigenen Ankern, Befund 124 bliebe verletzt) · \(e_{\text{Tag}}\) durch \(t_{\text{warn}}\) teilen, damit der wirksame Wert gleich bleibt (verworfen: hebt die Wirkung am gewarnten Tag ohne Beleg an) · Schwelle „hoch“ (verworfen als Basiswert: steckt im unteren Band von \(t_{\text{warn}}\)) · DWD-Anteil aller Tage \(m_{g,V}\) direkt einsetzen (verworfen: wählt die Tage über \(f\) und \(m\) zweimal aus und verdünnt um den Faktor \(f\); Befund 162) | wirksamer Wert über alle Zusatztage 0,03 → 0,03 × 0,75 = 0,0225 (0,028 ist nur das Kettenprodukt vor dem Runden); heute zahlengleich mit einem Faktor 0,0225 auf die Zusatztage im Geltungsbereich, geändert ist der Wert, nicht die Verteilung; Berlin 9.182 statt 12.243 vermiedene Tage, ≈ 56.900 statt ≈ 75.900 € je Jahr (§5.1); Kapitel 7: `pollen.r_s158` unverändert, `pollen.t_warn_s158` neu; Ledger-Befunde 156, 157, 161, 162, 163, 165, 167 (DWD-Gebiet \(V\) statt \(R\)) |
| 24 | Allergenarme Stadtbaumwahl: Wirkung abschätzen oder verwerfen (P2)? | (Die Aussagen zur gleichbleibenden Kommunensumme sind durch Log 26 überholt: Mit festgehaltenem Ḡ₀ sinkt die Summe, Rechenbeispiel §5.) **Abschätzen, zellscharf über \(\hat G\):** −0,14 auf \(\hat P\) je Senkung von \(\hat G/\bar G_0\) um 0,2 (Band 0,06–0,20 über λ; Eingabe ist die Änderung des Kronenanteils, abgezogen im Term, in dem die Kronen im Ausgangsstand stehen, Kronen ohne Gattungs-Tag nur mit 0,12, Befunde 186, 195); Berliner Allee-Zelle mit 100 Betroffenen −14,2 Tage und ≈ 88 € je Jahr (Band −6,1 bis −20,3 Tage, §5); ursprünglich war die gleichbleibende Kommunensumme als Modellgrenze der Abschätzung gesetzt, seit Log 26 senkt die Maßnahme die Summe (Modellgrenze 7) | P2 geht Methodik-Regeln vor; die Wirkung je Zelle ist mechanisch aus \(\hat P\) ableitbar und im Bericht mit Zahl, Band und Sensitivität abgeschätzt; die Summe der Kommune sinkt am festgehaltenen Ḡ₀ mit (Log 26), eine Nullwirkung ist nicht gesetzt. Am 27.09.2026 ging sie als Katalogmaßnahme in den Zelllauf, nach der Integrationsauflage (Stadtbaumwahl) in §5 (Absatz „Vorgabe für das Produkt (Befund 230)“). Die ursprüngliche Begründung (Summe der Kommune per Zentrierung gleichbleibend nach Log 18/19, flächige Wirkung gesperrt) ist durch Log 26 überholt; Befund 124 sperrt nur den pauschalen Faktor, gerechnet wird im Zelllauf über Ĝ′ | mit einem Satz verwerfen (verworfen: die Wirkung je Zelle ist ableitbar, eine Verwerfung ließe sie ohne Zahl) · eigenen Parameter für eine flächige Wirkung schätzen (ursprünglich verworfen mit der λ-Evidenz aus Messungen innerhalb einer Stadt; seit Log 26 läuft die flächige Wirkung über λ am festgehaltenen Ḡ₀, ein zweiter Parameter bleibt verworfen, Log 26) | keine Wirkung auf den Schadenswert im Ausgangsstand, mit Maßnahme sinkt er (Log 26); der Satz, die Umverteilung senke den kommunalen Ausweis, ist ersetzt (Ledger-Befund 158); die P2-Begründung stützt sich nicht mehr auf eine Produktanzeige (Ledger-Befund 164) |
| 25 | Kennzeichnung der Parameter-Blöcke (Aufgabe §4): welcher Wert je Block, und wo trägt ein Block ein Feld `rolle`? | (Stand Schritt 3. Seit Runde 27 führt Kapitel 7 14 Blöcke: dazu `pollen.stadtbaum_kosten` im Abschnitt 7.1, gekennzeichnet `abschaetzung_kap3`, Log 27.) **13 von 13 gekennzeichnet (Kapitel 7):** `quelle` für \(\Delta S\), \(a_{\text{attr}}\), \(p_{\text{AR}}\), \(c_{\text{jahr}}\); `abschaetzung_kap3` für \(p_B/p_G\), \(L\), \(f\), \(\lambda\), \(s_{\text{unbek}}\), \(r_{\text{S158}}\), \(t_{\text{warn}}\) (Herleitung je Block im Kommentar); `berechnet` für \(d_{\text{Saison}}\) (aus f, p_sens, L) und \(c_{\text{Tag}}\) (aus c_jahr, d_Saison); **kein** Feld `rolle` | \(\Delta S\) ist eine amtliche Messreihe, die Anlage [67] nur auswertet; \(p_{\text{AR}}\) folgt je Band einer Quelle, die Extrapolation 80+ ist in §3.2 gekennzeichnet; \(c_{\text{jahr}}\) ist der Quellwert, nur im Preisstand umgerechnet. Von den vier Rollen nach §4 trifft keine zu: \(s_{\text{unbek}}\) geht in jedem Lauf in \(\hat G\) ein und ist damit ein gewöhnlicher Rechenparameter, keine Sensitivitätsgröße; eine Rolle „abschaetzung“ kennt §4 nicht, die Abschätzung trägt \(r_{\text{S158}}\) schon in `kennzeichnung` | \(s_{\text{unbek}}\) mit `rolle: sensitivitaet` (verworfen: sagte, der Wert diene nur der Sensitivität) · \(r_{\text{S158}}\) mit `rolle: abschaetzung` (verworfen: kein zulässiger Wert nach §4) · \(p_{\text{AR}}\) als `abschaetzung_kap3` (verworfen: vier von fünf Bändern tragen einen Quellwert; die Extrapolation ist am Band gekennzeichnet) | keine Wirkung auf Zahlen; kein `wert:` in Kapitel 7 geändert; Ledger-Befund 173 |
| 26 ⚠ | Bezugswert der Zentrierung bei Maßnahmen: Ḡ in jedem Lauf neu bilden (Log 19) oder im Ausgangsstand festhalten? | **Festhalten (Weg (a), Festlegung CMO in T-1323):** Ḡ₀ = betroffenengewichtetes Mittel über die bewohnten Zellen der eigenen Kommune im Ausgangsstand ohne die bewerteten Maßnahmen, im Ausgangsszenario gebildet und für jedes Maßnahmenszenario festgehalten; Formel bleibt \(\hat P = 1 + \lambda(\hat G/\bar G_0 - 1)\) (§3.3). Im Ausgangsstand gilt weiter \(\sum B\hat P = \sum B\) exakt; mit Maßnahme sinkt die Summe um \(\lambda \cdot \sum B(\hat G - \hat G')/\bar G_0\) (Rechenbeispiel §5: 8.119 → 7.483 Tage, −637 Tage, ≈ 3.950 € je Jahr; Eingabe ist die Änderung des Kronenanteils, abgezogen im Term, in dem die Kronen im Ausgangsstand stehen, Kronen ohne Gattungs-Tag nur mit 0,12, Befunde 186, 195) | (1) **Vorgabe P2:** Ein in jedem Lauf neu gebildetes Ḡ hebt jede Senkung genau auf (Rechenbeispiel §5: Summe bliebe 8.000); weniger Quellbäume hießen dann nicht weniger Pollen — das wäre eine gesetzte Nullwirkung. (2) **Einwand aus Log 19 beantwortet:** Log 19 sah die λ-Evidenz nur für Gradienten innerhalb einer Stadt. Eine Maßnahme wird mit dem Ausgangsstand derselben Kommune verglichen, also innerhalb einer Stadt. Die Lesart von λ als Anteil der örtlichen Quellen an der Pollenlast einer Zelle (1 − λ = regionaler Hintergrund) belegt Hugg 2017 [74], Tabelle 3: städtischste gegenüber allen acht Messstellen, λ = 1 − Hintergrund ÷ Mittel, abgeleitet 0,22–0,94, drei von vier Werten im Band 0,3–1,0 (§3.3, Modellgrenze 7); Conclusions: „The local sources, such as unmanaged open lands, may substantially contribute to pollen exposure.“ (3) Log 17 und 18 bleiben: Gewichtsregel und Bezugsebene Kommune; zwischen Kommunen wirkt die Vegetation weiter nicht. (4) Befunde 124 und 129 bleiben: keine pauschal verknüpfte Maßnahme, gerechnet wird im Zelllauf | Ḡ in jedem Lauf neu (Log 19; verworfen: Nullwirkung, P2) · Summe gleich lassen, Wirkung nur je Zelle (Weg (b); verworfen vom CMO: weniger Quellbäume heißt weniger Pollen) · zweiter Parameter für den Niveaueffekt (verworfen: die Quelle liegt im Band von λ, T-1323 Punkt 1) | Basiswert (Ausgangsstand) unverändert, kein `wert:` in Kapitel 7 geändert; Stadtbaumwahl senkt jetzt die Kommunensumme; Richtung des Fehlers in λ: Modellgrenze 7 (Bezugsstelle in der Stadt → λ unterzeichnet eher; Gräser statt Birke → λ überzeichnet für Bäume eher; nicht bestimmbar, welche überwiegt); Log 19 verworfen; Ledger-Befund 182 |
| 27 | Kosten der Stadtbaumwahl (Vorgabe P2, Befund 253): eine Zahl oder nach Fall getrennt, woher die Werte, und wo stehen sie in Kapitel 7? | **Je ersetztem Baum nach Fall getrennt, Preisstand 2024:** Nachpflanzung ohnehin 60 € (Mehrkosten der Artenwahl im typischen Fall Linde statt Birke, Preisgruppe II − I [79]; Birke meistgefällt, Linde meistgepflanzt [78], [82], allergen „Low“ [81]); vorgezogener Ersatz 4.436 € (Pflanzung mit Anwuchspflege 3.636 € [75] plus Fällung 800 €, Abschätzung von KAP3); Block `pollen.stadtbaum_kosten` im eigenen Abschnitt 7.1; im Produkt Abfrage des Falls ohne stille Vorgabe (Ü-11); Amortisation der Nachpflanzung mit wachsender Krone, 24 Jahre am Punktwert (§5) | Die beiden Fälle unterscheiden sich um den Faktor 74; eine Zahl für beide stellte einen der Fälle falsch dar. Die Kosten wirken weder auf Tage noch auf den Schadensbetrag und stehen deshalb getrennt von den Größen der Schadens- und Wirkungsrechnung. Für die Fällung fand sich in den durchsuchten Quellen keine Kostenangabe je Baum (§5, Liste in Befund 253), deshalb eine Abschätzung von KAP3 mit dem geometrischen Mittel des Bands. Bei der Nachpflanzung ist der Vergleich ein junger Baum, dessen Krone erst wächst [80] | eine Zahl, 4.436 €, für alle Fälle (verworfen: die Artenwahl bei Nachpflanzung erschiene 74-mal zu teuer) · 4.436 € als Vorgabe, 60 € als Überschreibung (verworfen: stille Vorgabe auf den teuren Fall) · Fällkosten aus Preisportalen von Anbietern (verworfen: keine amtliche oder verbandliche Quelle, Herkunft nicht prüfbar) · Block im ersten yaml-Abschnitt von Kapitel 7 (verworfen: Kosten sind keine Größe der Schadensrechnung; gemessen schlügen dort vier statt ein Kennzeichnungstest fehl) · Amortisation mit voller Krone ab dem ersten Jahr (verworfen: 11 statt 24 Jahre, gut doppelt so früh, §5) | keine Wirkung auf Tage, Schadensbetrag und Berlin (2,53 Mio. € Kette, 2,47 Mio. € Zelllauf, §3.0); kein bestehender `wert:` in Kapitel 7 geändert, ein Block mehr (14); Ledger-Befund 253, Übernahmen Ü-11 und Ü-12 |
| 28 | Befund 258, §4: Wie wird \(\delta\) nach dem Wechsel auf \(a_{\text{attr}}\) = 0,27 gegen [9] geprüft, und was wird aus dem Band der Klimaanteile an den Behandlungskosten? | **Beide Vergleiche beim selben \(a_{\text{attr}}\)** (Festlegung des methodik_manager, T-1651): physisch 3,98 Tage × \(a_{\text{attr}}\) gegen 8 Tage × \(a_{\text{attr}}\) ([9], Results and Discussion, Abb. 1), am Basiswert 1,07 gegen 2,16 Tage, im Band 0,76–1,63 gegen 1,52–3,28 Tage; monetär \(\delta/d_{\text{Saison}}\) = (Σ p ΔS ÷ Σ p L) × \(a_{\text{attr}}\), im Modell 9,2 % Saisonverlängerung mal 0,27 = 2,5 %; ohne belegten Vergleichswert kein Prüfstein, §4 nennt das Ergebnis der M0-Herleitung (2,5 % gegen ≈ 2,9 %); deren Band entfällt | Der Anteil steht auf beiden Seiten und kürzt sich; so prüft §4 die Größenordnung von \(\delta\) unabhängig vom gewählten Anteil. Das Band der M0-Herleitung war aus dem Anteil der Saisonverschiebung gebildet, den Log 2 als nicht hergeleitet verwirft | Nur die Zahl tauschen (1,07 gegen die frühere Schätzung „≈ 4 Tage“) oder \(\delta \div f\) gegen 8 Tage × Band stellen: verworfen, weil das Beschwerdetage und Saisontage vermischt | §4: \(\delta\) liegt bei jedem \(a_{\text{attr}}\) bei rund der Hälfte des Klimaanteils der Saisonverlängerung aus [9]; Bundessumme ≈ 60 Mio. € je Jahr (Band ≈ 42–91 Mio. €); kein Parameter geändert, kein Band geweitet |
