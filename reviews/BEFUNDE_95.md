# Befund-Ledger #95 — Hitzebelastung

Angelegt 26.08.2026 (Migration M0 Rev. 5 → `docs/methodik/95_hitzebelastung.md`); Statusstand
nach der **Rev.-6-Autor-Revision** (`/risiko-auto 95`, 26.08.2026). **Startbestand** = alle
#95-relevanten Befunde aus `reviews/Gegenpruefung_Rev5_Befundliste.md` (Fassung 4.0;
M0-Nummerierung 1–56 beibehalten, hier fortgesetzt).

Nicht übernommen, weil #96/#98-spezifisch (verbleiben in der M0-Liste bis zu deren
Migration): 11–16, 34–37, 41, 43, 49, 52. Ferner: 31 (geschlossen, Prüfgrundlage
nachgereicht), 46 (ersetzt durch 51). „Geschlossen (Prüfgrundlage v2)" = Fortschreibungstext
steht bereits in der Aufgabe v2 (Kalibrierfaktor-Regel ex G1/G5, G14-Geltungsbereich,
G11-Begründung). Zurückgestellte A-Befunde blockieren die Abnahme.

| Nr | Befund (Stelle · Kurzfassung) | Kat. | Status | Umsetzungsnachweis | Begründung bei Abweichung |
|---|---|---|---|---|---|
| 1 | Kalibrierlauf mit Näherungs- statt Produktionsmodell; „Näherung konservativ" falschherum | A | **abweichend gelöst** | §4 (Richtung korrigiert; Bias quantifiziert: Bevölkerungsgewichtung ×1,11–1,26, UHI-Konvexität ×1,03 → Korrekturband ×0,77–0,87 auf c_kal, als Unsicherheit ausgewiesen); Log 27; `c_kal_rev6_ergebnis.md` | Zell-Lauf braucht die Bundeslauf-Infrastruktur → Fortschreibungsvermerk mit Ablaufdatum (Integration); exakt der Fallback-Vorschlag der Gegenprüfung |
| 2 | Vier regionale c_kal verstoßen gegen §3.4 („EIN Skalar") | A | **abweichend gelöst** | §4 + Log 26: Methodik-Basis = **ein** Skalar 0,905; c_reg (0,841/0,879/1,064/1,995) nur als dokumentierte, **befristete Übergangslösung** für den Produktausweis (§3.4-Übergangsregel; Ablauf: Zell-Lauf); ERF-Nachschätzung nach dem Zell-Lauf | sofortige 4-Regionen-ERF-Nachschätzung würde den Befund-1-Bias in die ERF einbrennen (Reihenfolge dokumentiert) |
| 3 | Regionen-Zuordnung nirgends definiert | A | übernommen | §3.2 „Regionen-Zuordnung": Bundesland→ERF-Region und →RKI-4-Region ausgeschrieben; Zelle→Region über Bundesland (VG250) | — |
| 4 | r_0,a: Raten ↔ Verhältnis inkonsistent; Herkunft fehlt | A | übernommen (Teil b abweichend) | §3.4: Option A — Raten behalten, Verhältnis korrigiert (1:3,3:5,7:8,2), Normierungs-Rechenweg + Test `beispiel_95_r0_normierung` | (b) altersspezifische GENESIS-/GBE-Raten nicht keyless abrufbar → gekennzeichnete Abschätzung + Ersetzungspfad (dokumentierte Datenlücke, §3.9) |
| 5 | e_HD-Basiswahl unbegründet; Harvesting auf F ungeklärt | A | übernommen | §3.4: konditional 0,024 Basis (Empfehlung der Gegenprüfung), Band 0,024–0,061; Harvesting: keine Zusatzkorrektur (im K&Z-Jahresaggregat enthalten); Log 19 | — |
| 6 | HD_ref ohne Zahlenwert | A | übernommen | §3.4: HD_ref = 7,2 Tage/Jahr (K&Z-Basisperiode 1999–2008) + Parameter-Block `heat.hd_ref` | — |
| 7 | v_vers unverändert auf Morbidität | A | übernommen | §3.4: F-Pfad nur β_iso; β_pfl-Gegenevidenz [64] zitiert (Register 95-S153-04); β_d Default 1 | — |
| 8 | β_pfl über alle Bänder, nur 85+ hergeleitet | A | übernommen | §3.3: v_vers,a bandweise; β_pfl nur 85+ (Tabelle Faktor×Band) | 75–84-Ausweitung erst mit bandspezifischer Pflegequote (Fortschreibung) |
| 9 | β_pfl-Kette nicht reproduzierbar | A | übernommen | §3.3b: Kette vollständig (Exzess-Verhältnis 1,0 × Basissterblichkeits-Verhältnis 2,97 → OR 3,0; Bouchama qualitative Stütze; Klenk umgewidmet); Test-Block; Log 23 | OR 3,5 → 3,0 (der Rev.-5-Wert hing an der nicht reproduzierbaren 1,32-Kette) |
| 10 | VOLY-Obergrenze nicht reproduzierbar; Preisstand-Label | A | übernommen | §3.5: Obergrenze definiert = 165,6 T€ (Raumtransfer ohne Elastizität, Rechnung + Test); Label €2024 durchgängig | — |
| 17 | Zentrierungs-Mittelwerte ohne Zahl (d̄_KH, q̄_1P) | A | übernommen (d̄ abweichend) | q̄_1P = 0,346 (Mikrozensus 2023, amtlich [63]; Zensus-Gitterwert bei Integration); d̄_KH entfällt — β_d aus dem Basiswert (Sensitivitätsband, Log 20) | d̄_KH ohne Bundeslauf nicht herleitbar; Nicholl-Übertragbarkeit ohnehin zu schwach für den Basiswert (§3.2) |
| 18 | Quellen [45]–[47] unverifiziert/unvollständig | A | übernommen | Kap. 8: verifizierte Vollzitate [45]/[46] (Volltext gegengelesen, T2.4) übernommen; [64] neu | [47]-Autorenliste + Wayback-Permalinks bei Integration (Ratchet-Schritt) |
| 32 | f_a ohne Rückrechnung; Kopplung an neue m_a | A | übernommen | §3.3a: vollständige Kette (lineare Näherung, gekennzeichnet) → 0,357/0,588/0,631/1,0; Test `beispiel_95_fa_rueckrechnung`; Kalibrierlauf + Altersvalidierung neu (Rev.-6-Skript) | — |
| 50 | VSL-Divergenz Bericht ↔ Monetarisierungs-Arbeitsmappe | A | übernommen | Arbeitsmappe fortgeschrieben (Schadenskonten-System C10/C11, Rechenregeln C16/A1, Risiken-Monetarisierung J100) + **Abgleich-Protokoll P52**; Backup `docs/archiv/KWRA-Monetarisierung_vor-Fortschreibung-P-VSL-YLL_2026-08-26.xlsx`; Kap. 1 Konto-Einbettung | — |
| 51 | §1.2-Weitergaben #95 fehlerhaft; Partitionszitat fehlt | A | übernommen (Migration) | Kap. 1 „Weitergaben": zweispaltig, P8/P47, Partitionszitat „Hitzetote (ID 95)", #102/#65 als Konto-Ausschlüsse | — |
| 19 | G12-Prüfung teilweise in-sample | B | übernommen | §4: zeitlicher Holdout (Fit 1992–2015 → Prüfung 2016–2024: 2/9 im PI, +17…+161 %) dokumentiert; Ergebnis trägt die Fensterwahl | — |
| 20 | Altersvalidierung ohne Ist-Ergebnis | B | übernommen | §4: Ist 6,2/12,7/24,8/56,3 % vs. RKI 6,5/12,9/25,2/55,5 % (±5 pp vorab: bestanden); Teilzirkularität benannt + unabhängiger Berlin-2018-Anker (232 vs. 260–320) | — |
| 21 | „Konservativ" doppeldeutig; Vollreihe-vs.-Fenster | B | übernommen | §4: Begriff definiert (= unterschätzend); Basis Fenster 2012–2024 (0,905) mit Holdout-Begründung, Vollreihe 1,042 Sensitivität; Log 26 | — |
| 22 | L̄_85+ Bevölkerungs- statt Sterbefallgewichte | B | **abweichend gelöst** | §3.5: als Perioden-Approximation gekennzeichnet, Richtung + Band (−0,3…−0,5 J ≈ −4 % YLL-Summe); Parameter-Band | Sterbefall-Altersjahre (GENESIS 12613) nicht im Repo; exakte Neurechnung bei Integration (Registry-Vermerk) |
| 23 | Preisstände inkonsistent (#95-Teil) | B | übernommen | §3: gemeinsamer Preisstand €2024; c_Fall 7.152 = 6.996 × 119,3/116,7 (Rechenschritt + Test); VOLY €2024 | — |
| 24 | Vorläufiger 2025-Wert in der Kalibrierreihe | B | übernommen | §4: 2025 nicht in der Basis; Sensitivität inkl. 2025 = 1,029 beziffert; Nachzug bei revidierter RKI-Fassung (Registry-Vermerk) | — |
| 25 | Datenverfügbarkeit q_1P×65+ / OSM-Heime | B | übernommen | §3.6 „Fallback-Definitionen": beide Fallbacks festgeschrieben, Proxy-Kennzeichnung; Verifikation bei Integration terminiert | — |
| 33 | δ_HAP-Wirkungsort undefiniert | B | übernommen | §5: multiplikativ auf den Wochen-Exzess (RR−1) definiert; β-Formulierung gestrichen | — |
| 38 | UHI→hot_days-Regel nicht im Bericht | B | **abweichend gelöst** | §3.4: Ist-Stand dokumentiert — HD = DWD-CDC hot_days **ohne** UHI-Verschiebung (Produkt implementiert keine; `inputs.py`-Provenienz); Richtung benannt; Erweiterung als Fortschreibung; Log 25 | die Rev.-5-Formulierung beschrieb Nicht-Implementiertes — statt eine Regel zu erfinden, wird der Ist-Stand ehrlich ausgewiesen |
| 39 | Szenario-Anwendung 95-A fehlt (#95-Teil) | B | übernommen | §6: Absatz „Szenario-Anwendung" (T̄-Shift; q_w-/ERF-Stationarität als dokumentierte Annahmen; M0 = Ist-Ausweis, Szenariofähigkeit ab M1+) | — |
| 40 | 2006/2015-Residuen ohne Zuschreibung | B | übernommen | §6 Modellgrenze 1: Residuen der Quantil-Modellgrenze zugeschrieben; q-T̄-Kopplung als Ausbaupfad benannt | — |
| 44 | Bandzuordnung auch für β_iso; v_vers,a | B | übernommen | §3.3: v_vers,a mit Band-Indikatoren; β_iso nur 65+; Tabelle Faktor × Band × q̄ | — |
| 47 | Kalibrier-Fits uneinheitlich gefiltert | B | übernommen | Rev.-6-Skript: einheitlicher Signifikanzfilter (BL-PI > 0) auch regional; Fenster-Varianten je Region beziffert (§4) | — |
| 53 | R7-Weiche für S157 nicht referenziert | B | übernommen | §5: R7-Satz (gekühlter Bestandsanteil, Entweder-oder je Einheit, M5-Übergabepunkt #65) | — |
| 55 | G1↔G5-Widerspruch im Grundsatz-Dokument | B | geschlossen (Prüfgrundlage v2) | Aufgabe v2 §3.4 „Kalibrierfaktor-Regel (präzisiert)" | Berichts-Seite als Befund 2 gelöst (s. o.) |
| 26 | Kopfzeile zitiert „Übersterblichkeit × VSL" (#95-Teil) | C | übernommen (Migration) | Kap. 1 Konto-Einbettung; nach P52 zusätzlich in der Quelle selbst fortgeschrieben | — |
| 27 | Kap.-5-Text nennt „Faktor 1,44" | C | geschlossen (verifiziert) | Rev.-6-Kap.-9 nennt die Rev.-6-Werte; „1,44" kommt im Bericht nicht mehr vor | — |
| 28 | Native Ergebnisgröße nicht deklariert (#95-Teil) | C | übernommen (Migration) | Kap. 3: nativ = YLL/Jahr; D, F, € Teil-Ausweise | — |
| 29 | Knoten-Bilanz fehlt (#95-Teil) | C | übernommen (Migration) | Kap. 1 Knoten-Bilanz | #96/#98-Anteil außerhalb dieses Ledgers |
| 30 | G14-Geltungsbereich einseitig | C | geschlossen (Prüfgrundlage v2) | Aufgabe v2 §3.9 „Geltungsbereich" | — |
| 42 | c_Fall nicht als Proxy gekennzeichnet | C | übernommen | §3.5/§3.6: Proxy-Kennzeichnung + DRG-Sensitivität benannt | — |
| 45 | „v_access"-Reste | C | übernommen | §5: auf v_vers,a umgeschrieben | — |
| 48 | Anlagen lagen der Prüfung nicht bei | C | übernommen | Kopf + [50]: Anlagenpfade (Rev.-5- und Rev.-6-Skripte, Ergebnisdateien) verlinkt; im Repo prüfbar | — |
| 54 | W124-Knoten nicht aufs Stadtmodell gemappt | C | übernommen | Kap. 1: W124-Komponenten-Mapping (inkl. E19 „implizit im DWD-Raster") | — |
| 56 | G11-Begründung überholt | C | geschlossen (Prüfgrundlage v2) | Aufgabe v2 §3.2 Tails | — |
| 57 | §1.2-Beispiel „≈ 84.100 €" (korrekt 84.600) | C | übernommen (Migration) | Test `beispiel_95_zelle_yll` rechnet 84.600; Berichtstext korrigiert | — |

## Runde 1 — Review Rev. 6 (frische Session, 26.08.2026): neue Befunde 58–67

Lint-Stand: Zeichentabellen ✓ · Parameter-Blöcke ✓ · Beispiel-Blöcke 7/7 grün ✓ ·
Knoten-/Kanten-Abgleich direkt gegen beide xlsx ✓ (W182 Z405, Netzwerkliste Z96, P8/Z12,
P47/Z146, P52/Z151 verifiziert) · Preisstand €2024 einheitlich ✓ · **Quellen-Lint rot**
(Befund 61). Regression: 1, 2, 17, 22, 38 (abweichend gelöst) tragen — jeweils exakt der
Fallback-Vorschlag der Rev.-5-Gegenprüfung bzw. §3.9-Kennzeichnungsregel; 27/45 (geschlossen)
per Grep bestätigt; Kalibrier-Prüfstein bleibt laut Bericht selbst nicht bestanden
(§6-Eskalation dokumentiert — blockiert die Abnahme unabhängig vom Ledger-Status).

| Nr | Stelle | Art | Begründung | Vorschlag | Kat. | Status | Umsetzungsnachweis | Begründung bei Abweichung |
|---|---|---|---|---|---|---|---|---|
| 58 | §2 Register 95-S152-02 · §3.4 F-Formel · Parameter-Block `heat.beta_iso` (endpunkt: beide) | Fehler (Endpunkt-Zuordnung §3.2, LF 5) | Semenza 1996 [40] ist Fall-Kontroll-Evidenz zu Hitze-**Todesfällen**; für den F-Pfad steht nur „wirkt plausibel auf beide Endpunkte" — §3.2 verlangt Endpunkt-Deckung der Evidenz, unbelegte Modulatoren Default 1. Das zentrale Register (`docs/evidenz/register.md`) führt 95-S152-02 selbst nur als „→ Hitzemortalität" | β_iso im F-Pfad auf Default 1 (analog β_d/β_pfl, Log 24) **oder** Morbiditätsevidenz nachtragen (Kandidat: Semenza 1999, Chicago-Einweisungen) und Register-Zeile je Endpunkt trennen | B | **übernommen** | §3.4 (F-Pfad ohne Modifikatoren) · §2 (95-S152-02 nur Mortalität) · Parameter `heat.beta_iso` endpunkt: mortalitaet · Log 28 | Variante Default 1 gewählt; Morbiditätsevidenz-Nachtrag als dokumentierte Alternative im Log |
| 59 | §3.4 F-Formel ((HD−HD_ref)+) · §4 „Verteilschlüssel-Test" | Fehler/Lücke (§3.1 Lackmustest; §5-LF-4 HD_ref-Klasse) | (a) Für HD < 7,2 bucht die Formel den vollen nationalen Basissatz r_0,a — eine Kommune ohne Hitzetage erhält dieselbe Pro-Kopf-Hitzemorbidität wie eine mit 7; der Baseline-Anteil (≈ 2.950 Fälle, ≥ 70 % von F) verteilt sich rein bevölkerungsproportional; die §4-Behauptung „Kommune ohne Hitzesignal → ~0 ✓" gilt nur für die Mortalität. (b) Der Positivteil subtrahiert Zellen unter der Referenz nicht: bevölkerungsgewichtet ist E[1+e_HD(HD−HD_ref)+] > 1 — der in r_0 enthaltene Durchschnittseffekt wird teilweise doppelt gezählt (Jensen-Rest; Richtung Überschätzung, gegen die Untergrenzen-Linie) | Linearer Term 1+e_HD·(HD−HD_ref), bei 0 gedeckelt (oder dokumentierte HD-Skalierung des Basissatzes); §4-Behauptung auf die Mortalität einschränken | B | **übernommen** | §3.4: HD-Term zweiseitig linear mit Deckel 0 (kein Jensen-Rest); §4 Verteilschlüssel-Test auf Mortalität eingeschränkt, Morbiditäts-Sockel als dokumentierte Grenze; Log 29 | Klimaanteil-Zerlegung des Sockels als dokumentierte Fortschreibungsoption im Log |
| 60 | §2 (95-E02-01) · §3.6 Zeichentabelle (β_85+, T_0, L̄_a, HD_ref) · §3.4 (r_0) | Lücke (§3.9; LF 13) | Vier Herleitungsketten sind bei der Migration nicht in den Bericht übernommen: (i) β_85+ 0,0634/0,0625/0,0531 stehen nicht als Zahlen in Winklmayr Abb. 3, sondern sind Kurvenablesungen (RR ≈ 1,40/1,35/1,25 bei 25 °C; ln RR/(25−T_0)) — die Kette steht nur als Kommentar in `health.py`; (ii) L̄_a: Stützstellenwahl (u65 → e(60)) und m/w-Kombination zu 23,39/15,59/8,90/**5,44** fehlen (nur Männer-85+-Pfad 4,97 im Test); (iii) HD_ref = 7,2 ohne Fundstelle/Rechenweg; (iv) r_0-Zusatzterm „1,21…2,67" ohne Rechenkette (Teilrückfall zu Befund 4). Werte selbst nachgerechnet plausibel (β-Kette exakt reproduziert) | Ketten aus M0 Rev. 5 in Herleitungs-Anker übernehmen (#beta-erf, #l-a, #hd-ref, #r0-a) — der Bericht muss ohne M0-HTML prüfbar sein (§2.7) | B | **übernommen** | §3.3 Anker #beta-erf (Ablesekette + Test) · §3.5 Anker #l-a (Stützstellen, m/w-Kombination 5,44 + Test) · §3.4 #hd-ref (Fundstelle K&Z-Panelperiode) · §3.4 #r0-a (Zusatzterm-Kette 0,119×1,408…3,106×7,2 + Test) | — |
| 61 | Kap. 8 | Lücke (§3.8; §7-Lint „DOI/URL + Archiv" rot) | Kein Archiv-Snapshot für irgendeine Quelle („bei Integration" = Später-Verweis, Fertig-Regel §3.9); [47] ohne Autorenliste; [16], [17], [48], [49], [61] ohne URL/Tabellen-Permalink. Regression zu Befund 18 (Teil offen) | Wayback-Snapshots jetzt anlegen (keyless), [47]-Autoren ergänzen, Destatis-Quellen mit GENESIS-/PM-URL | B | **übernommen (Archiv abweichend)** | Kap. 8: [47]-Vollzitat (Urban, Huber u. a., ERL 20:124071; iopscience verifiziert 26.08.2026); URLs für [16], [17], [48], [49], [61] ergänzt | web.archive.org aus der Session nicht erreichbar (dokumentiert); Snapshots deterministisch über die bestehende, testbewehrte sources.py-Ratchet-Mechanik |
| 62 | §4 Befund-1-Behandlung · Log 27 · §6 Infokasten 1 | Widerspruch (Gate-1-Plausibilität; §3.6-UI) | Das Korrekturband ×0,77–0,87 läuft nur als Unsicherheit; der Produktausweis rechnet bis zum Zell-Lauf mit dem wissentlich um ~15–30 % überhöhten c_kal = 0,905. Das kollidiert mit „konservativ = unterschätzend" (§4) und mit Infokasten 1 („bewusste Untergrenze … wird mit jeder Ausbaustufe vollständiger — **nie kleiner**"): der terminierte Zell-Lauf wird den Mortalitäts-€-Wert voraussichtlich um 13–23 % senken. Die naheliegende Alternative — Korrektur zentral anwenden (c_eff ≈ 0,905×0,82 ≈ 0,74; Band als Unsicherheit) — fehlt im Log | Korrektur in den Ausweis übernehmen (zentral ×0,82 oder konservativ ×0,77) **oder** Infokasten-Zusage abschwächen; Log 27 um die Alternative ergänzen | B | **übernommen** | §4 + Log 30: Korrektur zentral — c_kal = 0,742 (0,905 × 0,82), Band 0,70–0,79, obere Sensitivität 0,905; c_reg konsistent ×0,82 (0,690/0,721/0,873/1,636); Parameter-Blöcke angepasst; Log 27 ersetzt | — |
| 63 | §4 Anker-Absatz | Lücke (§3.4 Anker-Zeitreihe/Transparenz) | Der Text listet 12 Jahre als „revidierte RKI-Reihe"; das Fenster 2012–2024 nutzt 13 signifikante Jahre (alle, inkl. 2012/2014/2016/2017/2021 mit 1.200–1.700), die Vollreihe 26 — der Fit ist aus dem Berichtstext nicht nachvollziehbar, nur aus der xlsx-Anlage | Reihe vervollständigen oder explizit als Auswahl kennzeichnen mit Anlagen-Verweis | C | **übernommen** | §4 Anker-Absatz: als Auswahl markanter Jahre gekennzeichnet; Fit-Jahresmengen (13/26) + Anlagenverweise | — |
| 64 | §4 „Unabhängiger Anker Berlin 2018" | Fehler (Kennzeichnung; §3.4 out-of-sample) | c_reg Osten ist auf den Bundesland-Jahren des Fensters **inkl. Berlin 2018** gefittet — das Niveau des Ankers ist teil-in-sample; unabhängig ist nur die 85+-Band-Aufteilung | Als teilabhängig kennzeichnen; Variante mit nationalem Skalar (≈ 239 je 100.000) zusätzlich ausweisen | C | **übernommen** | §4: Berlin-Anker als teil-in-sample gekennzeichnet; Variante nationaler Fit-Skalar (239) ergänzt; Geltung der ×0,82-Korrektur abgegrenzt | — |
| 65 | §6 (Produktkonformität) | Lücke (§3.6) | Der geforderte Raten-Ausweis (je 1.000 EW) und die aggregierte Darstellungsebene (Quartier/Gemeindeteil) sind für #95 nicht spezifiziert | Je Ausweis ein Satz (z. B. YLL je 1.000 EW 65+ und Jahr; Quartiersaggregat) | C | **übernommen** | §6 Raten-Darstellung und Aggregation: YLL je 1.000 EW (Teil: je 1.000 EW 65+), Fälle je 1.000 EW, € je EW; Quartier/Gemeindeteil-Aggregat | — |
| 66 | Kap. 1 Weitergaben (Partitionszitat) | Fehler (Referenz) | Beleg „Zeile 101": das Zitat steht in Blattzeile 106 (ID 101, Spalte „Nicht enthalten (gebucht in …)"); die Parallelreferenz „Z100" (ID 95) ist dagegen eine Blattzeile — Konvention uneinheitlich. Zitat selbst wortgetreu verifiziert | Einheitlich „ID 101 (Blattzeile 106)" | C | **übernommen** | Kap. 1: ID 101 (Blattzeile 106) und ID 95 = Blattzeile 100 vereinheitlicht | — |
| 67 | §3.3 („damit kalibrierneutral") · §4 Befund-1-Band | Lücke | Kalibrierneutralität zentrierter Modifikatoren gilt nur bei Unabhängigkeit von v_vers und Hitze-Exzess; q_1P/Heimdichte korrelieren räumlich mit UHI-Lagen (Städte) — die Kovarianz hebt die Zellmodell-Summe zusätzlich; das quantifizierte Befund-1-Band (nur Bevölkerungsgewichtung + Konvexität) unterschätzt den Näherungsfehler tendenziell | Kovarianz-Term beim Zell-Lauf mit ausweisen; bis dahin ein Satz im Unsicherheits-Absatz §4 | C | **übernommen** | §4 Unsicherheiten: Kovarianz-Vorbehalt (q_1P/Heimdichte × UHI) ergänzt; Ausweis beim Zell-Lauf terminiert | — |

## Runde 2 — Re-Review nach Rev.-6-Revision (frische Session, 26.08.2026): neue Befunde 68–74

Lint-Stand: Zeichentabellen ✓ (kein Später-Platzhalter) · Beispiel-Blöcke **9/9 grün** ✓ ·
Parameter-Blöcke vollständig, Kostensätze mit Preisstand ✓ (endpunkt-Metadaten: Befund 73) ·
Preisstand €2024 einheitlich ✓ · Knoten-/Kanten-Abgleich direkt gegen beide xlsx ✓ (W182 Z405:
E02/S152–S155/S157/S158/R35/R36/W124; NL Z96: In 62;63, Out 87;101, K1, Bausteine
Mortalität+Morbidität; AP P8/Z12, P47/Z146, P52/Z151; ID 95 = Z100, ID 101 = Z106 mit
Partitionszitat „Hitzetote (ID 95)"; R7-Zitat = ID 63/Z68 Spalte K; #102-Eingang nur #49) ·
Quellen-Lint: Archiv-Snapshots weiterhin offen (Runde-1-Adjudikation Befund 61 unverändert),
**[47]-Effektzahl rot** (Befund 68). Volle Prüfung LF 2/3/4/5/7/8/11/13 (Kalibrier-/Struktur-
Änderung), Rest Regression. Kalibrier-Rechenwege unabhängig nachgerechnet: c_fit 0,9047 ✓,
c_kal 0,742 ✓, c_reg-Fits 0,8409/0,8790/1,0645/1,9948 und ×0,82 = 0,690/0,721/0,873/1,636 ✓,
Verteilungsprüfung 8/16 (Fit-Basis) ✓, Berlin 232/239 ✓, β-Ablesekette/L̄_a/f_a/r_0 exakt ✓.
Primärquellen-Stichprobe K&Z/IZA-DP 7875 (Volltext): „annual average of 7.2 Hot Days" ✓,
Tab. 3: 1,4075 gesamt / 0,1680 Herz (= 11,9 %) ✓, konditional +2,4 % / unkonditional +5,4 %
(3,1063) ✓ — Regressionen 58–67 sowie Stichproben 3/4/9/10/16/20/22/23/24/32/47/53/57/66
tragen alle. Kalibrier-Prüfstein (≥ 11/16) laut Bericht selbst weiter nicht bestanden —
Eskalation §6 dokumentiert, blockiert die Abnahme unabhängig vom Ledger-Status.

| Nr | Stelle | Art | Begründung | Vorschlag | Kat. | Status | Umsetzungsnachweis | Begründung bei Abweichung |
|---|---|---|---|---|---|---|---|---|
| 68 | Kap. 8 [47] · §2 Register 95-S155-01/95-S158-01 · §5 (δ_HAP-Evidenz) | Fehler (§3.8 Sekundärfunde; LF 10 Zahlen ≠ Primärquelle) | „2–23 % vermiedene Todesfälle" steht **nicht** in Urban u. a. 2025 (ERL 20:124071; Volltext geprüft 26.08.2026): eigene Ergebnisse dort 25,2 % [19,8–31,9] HAF-Reduktion, regional −11,9…−33,2 %, Länderspanne −10…−43 %, Sensitivität ohne 2003 15,2 % [4,1–23,7] — keine dieser Spannen ist 2–23 %. Die Befund-18/61-Verifikation deckte nur die Zitat-Metadaten (Autorenliste), nicht die Effektzahl (Teil-Regression zu 18/61). δ_HAP-Basiswert hängt an [45] und bleibt davon unberührt | [47]-Zahlen korrekt zitieren (25,2 % bzw. Spannen) **oder** „2–23 %" der tatsächlichen Ursprungsquelle zuordnen (und diese verifizieren); Register-Zeilen + §5 + Kap.-8-Eintrag nachziehen; Wirkung auf δ_HAP-Band (0,85–1,00) prüfen | B | **übernommen** | §5 + Kap. 8 [47] + Register (Bericht §2 und docs/evidenz/register.md): Effektzahlen aus dem Volltext (HAF-Reduktion 25,2 % [19,8–31,9], regional −11,9…−33,2 %, ohne 2003: 15,2 %); Einordnung als Einführungseffekt — δ_HAP-Basis und Band bleiben [45]-gestützt | die frühere 2–23-%-Angabe als Rev.-5-Platzhalter-Herkunft im Quelleneintrag dokumentiert |
| 69 | §4 Befund-1-Korrektur (Kette hinter ×0,82) · Log 30 · Parameter `heat.c_kal`/`heat.c_reg_uebergang` | Lücke (§3.2 „messen statt setzen"; §3.9; LF 7/13) | Die seit Log 30 **lasttragende** Korrektur (skaliert jeden Mortalitäts-€) beruht auf zwei gesetzten Eingangsgrößen ohne Herleitung/Quelle/Begründung des Zahlenwerts: Bevölkerungsgewichtungs-Offset **+0,2…+0,4 K** und UHI-Streuung **σ = 0,5 K** (das Rev.-6-Skript rechnet nur die Elastizität der Modellsumme *gegen* diese Annahmen, nicht die Annahmen selbst). Beide sind mit vorhandenen keyless Daten messbar: bevölkerungs- vs. flächengewichtetes Sommermittel je Land aus DWD-1-km-Raster × Zensus-100-m-Gitter (ohne Zellmodell-Infrastruktur), σ_UHI aus dem produktseitig implementierten Stadtmodell. Zusätzlich ist die regionale Homogenität des Bias für c_reg („gleicher Bias") nur behauptet — der Bias hängt von der Urbanisierung ab (Stadtstaaten vs. Flächenländer), gerechnet wird nur national | Beide Größen messen und Korrektur + Band daraus ableiten; bis dahin §3.9-Kennzeichnung „Abgeschätzt" mit Begründung des Zahlenwerts, Ergebnis-Sensitivität und einem Satz zur Regionalannahme | B | **abweichend gelöst (Zwischenlösung)** | §4: beide Eingangsgrößen als gekennzeichnete Abschätzungen (§3.9) mit Begründungskette (Offset ≈ 0,77 × 0,3–0,5 K; σ ≈ Spanne/√12), Ergebnis-Sensitivität = Band 0,70–0,79, Regionalannahme-Satz; Messpfad (DWD-Zentroid × Einwohner; Stadtmodell-σ) als Teil des Zell-Laufs terminiert | Messung braucht den Raster-Batch (Lite-Daten enthalten nur Indizes, geprüft); exakt die im Befund vorgesehene Zwischenlösung |
| 70 | KWRA-Monetarisierung.xlsx: Risiken-Monetarisierung Z103 (ID 98) und Z106 (ID 101) vs. AP P52 (Z151) + Schadenskonten C10/C11 + Rechenregeln A1 | Widerspruch (LF 14 Quellen-Synchronität) | P52 erklärt die Umstellung VSL → YLL × VOLY für „**alle K1-Buchungsobjekte**", und Konto-Definition (C10/C11) sowie A1 sind fortgeschrieben; die Bewertungsbausteine anderer K1-Zeilen blieben aber stehen: Z103/ID 98 „Mortalitätsanteil × VSL", Z106/ID 101 „Todesfälle × VSL" — die Quelle widerspricht sich jetzt selbst; künftige Berichte (#98, #101) würden die veraltete Zeile zitieren. #95-Zahlen unberührt (nur Z100 nachgezogen) | Z103/Z106 (und ggf. weitere K1-Zeilen) auf „YLL × VOLY (P52)" nachziehen **oder** P52-Scope explizit einschränken (dann C10/C11 anpassen); Nachtrag im Abgleich-Protokoll | B | **übernommen** | Arbeitsmappe: Z103 (ID 98) und Z106 (ID 101) Bewertungsbausteine auf YLL × VOLY (P52) nachgezogen; P52-Protokolleintrag um den Nachzug ergänzt (26.08.2026); übrige K1-Zeilen ohne VSL-Nennung verifiziert | — |
| 71 | §4 Verteilungsprüfung („Länder-Verhältnisse … mit c_reg: 8/16") | Fehler (Kennzeichnung) | Die Verhältnisse sind mit den **Fit-Werten** (0,841/0,879/1,064/1,995) gerechnet (Skript/CSV; nur dazu passen HH 2,57 / SH 2,35 / BY 1,99); c_reg bezeichnet seit Log 30 aber die ×0,82-korrigierten Werte — damit gerechnet wären es **10/16** (nachgerechnet: BW 0,89 … HH 2,11). Ergebnisrelevanz gering: der Prüfstein ≥ 11/16 scheitert in beiden Lesarten | „mit den Fit-Faktoren (vor ×0,82)" präzisieren; optional die 10/16-Lesart als Fußnote | C | **übernommen** | §4: als Fit-Faktoren (vor ×0,82) präzisiert; 10/16-Lesart ergänzt | — |
| 72 | Entscheidungslog Nr. 26 | Lücke (Log-Konsistenz) | Als „angewendete Entscheidung" steht „ein nationaler Skalar **0,905**"; tatsächlich angewendet ist seit Nr. 30 **0,742** (0,905 = Fit). Die Ersetzungs-Konvention „(ersetzt durch Nr. X)" wurde nur auf Nr. 27 angewendet — Nr. 26 bleibt ohne Querverweis missverständlich | Querverweis in Nr. 26 ergänzen („Wert per Nr. 30 auf 0,742 korrigiert; 0,905 = Fit; übrige Teilentscheidungen unverändert") | C | **übernommen** | Log Nr. 26: Querverweis auf Nr. 30 (Fit 0,905 → Ausweis 0,742) | — |
| 73 | §7 Parameter-Blöcke `heat.qbar_1p`, `heat.q_wochenquantile`, `heat.gamma_hoehe` (endpunkt: beide) | Fehler (Metadaten; §4-Blockformat, LF 5) | q̄_1P wirkt seit Log 28 nur im D-Pfad (`heat.beta_iso` endpunkt: mortalitaet); Wochenquantile und Höhenkorrektur speisen nur den Temperatur-/Mortalitätspfad — der F-Pfad nutzt DWD hot_days ohne UHI-/Höhenverschiebung (§3.4) | endpunkt: mortalitaet setzen (bzw. je Block ein Satz, warum „beide" korrekt wäre) | C | **übernommen** | Parameter-Blöcke qbar_1p, q_wochenquantile, gamma_hoehe: endpunkt mortalitaet (mit Begründungskommentar) | — |
| 74 | §3.6 Zeichentabelle: β_iso „(Band 0,3–1,4)", r_0,a „(Band ×0,6–1,6)" + zugehörige Parameter-Blöcke | Lücke (§3.9: Bandgrenzen herleitungspflichtig) | Beide Bänder stehen ohne Rechenweg/Quelle — im Kontrast zu den hergeleiteten Bändern β_pfl 1,0–2,9 (aus OR 2,2–6,0), e_HD 0,024–0,061, VOLY 136,4–165,6, c_kal 0,70–0,79. Mutmaßlich Semenza-KI → β-Band bzw. Summen-Band 2,9–4,4 × Altersprofil-Alternative, aber das steht nirgends | je Band ein Herleitungssatz (OR-KI → β-Übersetzung; Kombination Summen-Band × Profilvarianten) oder Band anpassen | C | **übernommen** | §3.6 Zeichentabelle: Band-Herleitungssätze für β_iso (OR-Band ≈ 1,4–3,7, KI-Approximation) und r_0,a (Summen-Band × Profil-Unsicherheit), jeweils als gekennzeichnete Abschätzung | — |

## Runde 3 — Re-Review nach Runde-2-Revision (frische Session, 26.08.2026): neuer Befund 75

Lint-Stand: Beispiel-Blöcke **9/9 grün** ✓ · Zeichentabellen vollständig (kein
Später-Platzhalter, kein Platzhalter-Grep-Treffer) ✓ · Parameter-Blöcke vollständig
(Quelle, Preisstand bei Kostensätzen, Bandzuordnung/Endpunkt inkl. Befund-73-Korrekturen) ✓ ·
Preisstand €2024 einheitlich ✓ · Knoten-/Kanten-Abgleich direkt gegen beide xlsx ✓
(W182 Z405: E02/S152–S155/S157/S158/R35/R36/W124 vollständig in der Knoten-Bilanz; NL Z96:
In 62;63, Out 87;101, K1, Bausteine Mortalität+Morbidität; eingehende Kanten in #95 nur aus
62/63; #102-Eingang nur #49; AP P8/Z12, P47/Z146, P52/Z151 **inkl. Befund-70-Nachzugsvermerk**;
RM Z100/Z103/Z106 alle YLL × VOLY, keine VSL-Reste in K1-Bausteinen [VSL nur noch als
Sensitivitäts-Nennung P52]; R7-Zitat ID 63/Z68 Spalte K; Partitionszitat „Hitzetote (ID 95)"
Z106) · Quellen-Lint: Archiv-Snapshots unverändert offen (adjudizierte Abweichungslösung
Befund 61, dokumentierte sources.py-Ratchet-Mechanik) · **[47]-Effektzahlen gegen die
Primärquelle verifiziert** (iopscience-Abruf 26.08.2026): 25,2 % [19,8–31,9], regional
−11,9…−33,2 %, ohne 2003: 15,2 % [4,1–23,7], 102 Standorte/14 Länder/1990–2019 — Bericht,
Register (§2 + docs/evidenz/register.md) und Kap. 8 stimmen ✓. Diff-Prüfung: alle in der
Runden-Übergabe genannten Änderungen umgesetzt. **Regression 68–74: alle Schließungen
tragen** (70 direkt in der xlsx; 71 Fit-Faktoren-Kennzeichnung + 10/16-Lesart; 72
Log-26-Querverweis; 73 Endpunkt-Metadaten; 74 Band-Herleitungssätze — OR-Band 1,4→0,35≈0,3
[konservativ geweitet]/3,7→1,40 und ×0,83–1,26 × ±25 % ⇒ ×0,6–1,6 nachgerechnet);
Stichprobe Altbestand 27/45/57/58/59/60/61/62/63/64/65/66/67 ✓. Kalibrier-Zahlen gegen
Anlage `c_kal_rev6_ergebnis.md` abgeglichen (0,905/1,042/1,029; Holdout 2/9, +17…+161 %;
Bias ×1,11–1,26 und ×1,03 ⇒ Band ×0,77–0,87, zentral 0,82; 0,742; c_reg-Fits ×0,82 =
0,690/0,721/0,873/1,636; 8/16; Alters-Ist 6,2/12,7/24,8/56,3; Berlin 232/239) ✓ — seit
Runde 2 unverändert. Alle 14 Leitfragen mit Verdikt (LF 1–14: bestanden bzw. dokumentierte,
bereits adjudizierte Grenzen; einziger neuer Befund: 75, Kat. C). Entscheidungslog: Diff nur
Log-26-Querverweis — plausibel; keine ⚠-Entscheidung mit unplausibler Empfehlung, kein
Ermessensfall fälschlich als ✅. Kalibrier-Prüfstein (≥ 11/16) laut Bericht selbst weiter
nicht bestanden — Eskalation §6 dokumentiert (Modellentscheid Zell-Lauf + regionale
ERF-Nachschätzung), blockiert die Abnahme unabhängig vom Ledger-Status.

| Nr | Stelle | Art | Begründung | Vorschlag | Kat. | Status | Umsetzungsnachweis | Begründung bei Abweichung |
|---|---|---|---|---|---|---|---|---|
| 75 | §4 Befund-1-Korrektur, Begründungsketten der gekennzeichneten Abschätzungen (a)/(b) | Lücke (§3.8 „jede Zahl mit Quelle"; §2.7 „ohne Rückfragen prüfbar") | Zwei Elemente des seit Runde 2 neuen Textes sind nicht im Bericht verankert: (a) „DE-Bevölkerung lebt zu ≈ 77 % städtisch" ohne Quellenangabe; (b) die σ_UHI-Begründung beruft sich auf „die Feinstruktur-Spanne des §3.1-Beispiels (±1 K)" — §3.1 dieses Berichts enthält kein Beispiel (bei der Migration nicht übernommen; toter Binnenverweis, vgl. Befund-60-Muster). Ergebnisrelevanz gering: beide Größen sind als §3.9-Abschätzungen gekennzeichnet, das Band 0,70–0,79 ist die ausgewiesene Ergebnis-Sensitivität, der σ-Beitrag (×1,03) ist zweiter Ordnung | (a) Quelle ergänzen (Destatis-/Weltbank-Urbanisierungsgrad ≈ 77–78 %, Kap.-8-Eintrag); (b) Spanne direkt beziffern (Stadtmodell-Kennwert) oder das ±1-K-Beispiel aus M0 Rev. 5 in §3.1 übernehmen | C | **übernommen** | §3.1: Mittelwerttreue-Beispiel (±1-K-Spanne) aus M0 wiederhergestellt — Verweis trägt; 77-%-Zahl mit Weltbank-Indikator bequellt | — |
| 76 | Produktcode (Registry/Engine `EXPECTED_ANNUAL_MORTALITY`) ↔ Bericht Rev. 6 — sichtbar geworden in der Wirkungsmechanismus-Vorschau (30.08.2026) | Divergenz Bericht ↔ Code (Eiserne Regel 5; LF 14) | Das Produkt rechnet noch den Vor-Rev.-6-Stand: native Größe **Todesfälle/Jahr** statt YLL (Log 3/P52), Kostensatz-Pfad ohne YLL × VOLY, f_a 0,404/0,577/0,62 (Rev.-5, ersetzt durch 0,357/0,588/0,631 — Befund 32), Basissterberaten 180/1.800/4.600/15.500 statt 213,2/1.737,9/4.812,3/14.800,2, Gauß-σ 2,0 K statt empirischer Wochenquantile (Log 5), Kalibrierfaktor 1,44 statt 0,742 (Log 26/30) | **Kein stiller Code-Fix.** Auflösung ist exakt der Umfang von `/integriere-risiko 95` (Registry-Parameter aus §7, Schicht-B-Funktion, Golden-Tests); bei Integration diesen Befund mit Umsetzungsnachweis schließen und die Wirkungsmechanismus-Vorschau #95 gegen den Bericht abgleichen | A (blockiert nicht den Bericht, sondern markiert den offenen Integrationsschritt) | **geschlossen (Integration 30.08.2026):** Produkt rechnet den Rev.-7-Stand (YLL nativ × VOLY 160.800 €₂₀₂₄, Todesfälle als Teil-Ausweis; empirische Wochenquantile je Region; v_vers bandweise; c_kal 0,581; β_Süd 0,0876; f_a/m_a/L̄_a Rev.-7-Werte; Morbidität r_0,a × HD-Term, c_Fall 7.152 €). Verdrahtung: impact/params.py + impact/health.py + catalog.py (Kostensätze, ref_value, MODEL_VERSION 2026.08-m0-95rev7) + Lineage-Specs; Golden-/Kontrakt-Tests tests/test_methodik_95_golden.py (Berichts-Beispielblöcke laufen in CI), test_impact_health.py Rev.-7-Handrechnung; Gesamtsuite 282 grün, Ratchet 0 offen | — | — |

## Rev.-7-Autor-Revision (30.08.2026): Auflösung der §6-Eskalation (Kalibrier-Prüfstein)

Auslöser: `/integriere-risiko 95` wurde in Schritt 0 abgebrochen (Prüfstein nicht
bestanden, Abnahme blockiert). Statt des Modellentscheids „Zell-Lauf" wurde die im
Bericht §4 (Rev. 6) selbst benannte keyless Messung umgesetzt — **bevölkerungsgewichtete
Kalibrier-Zeitreihen** (DWD-JJA-Raster 1 km × VG250-Gemeindepunkt × Zensus-Bevölkerung;
`calibrate_heat_mortality_rev7.py`) — plus **Holdout-Nachschätzung der Süd-ERF**
(nur Süd: Nord nicht identifizierbar [0 Fit-Jahre], Mitte-Optimum 1,0; s_Süd = 1,65,
Fit ohne die Validierungsjahre 2018/2019/2022). Ergebnis:

- Gemessene Offsets bevölkerungsgewichtet − Flächenmittel: DE **+0,53 K** (Rev.-6-Band
  +0,2…+0,4 war zu niedrig — Kovarianz-Vorbehalt Befund 67 bestätigt und aufgelöst).
- **Kalibrier-Prüfstein: 12/16 Länder im Band 0,75–1,35 — BESTANDEN** (ein nationaler
  Skalar c_kal = 0,581, out-of-sample auf Σ 2018/2019/2022); Restausreißer SH/HH
  (Kleinzahlen/Küste), BY (Alpenvorland-Feinstruktur → Zellmodell), BB (knapp).
- ×0,82-Pauschalkorrektur und c_reg-Übergangsfaktoren **entfallen** (Log 31–33);
  Parameter-Blöcke/Zeichentabelle/§4 fortgeschrieben; neuer Golden-Test
  `beispiel_95_beta_sued_nachschaetzung`; Altersvalidierung 6,3/12,6/24,7/56,4 % ✓;
  Berlin-Anker 221/100k (−15 %, Richtung dokumentiert).
- Die Eskalations-Vermerke der Runden 1–3 sind damit **gegenstandslos, sobald ein
  Re-Review (volle Prüfung — Kalibrierung geändert, §6) die Rev. 7 bestätigt**; der
  Zell-Lauf bleibt als finaler Abgleich bei Integration (Rest-Bias UHI-Feinstruktur
  ×1,02, dokumentiert), ist aber nicht mehr abnahmerelevant.

| Nr | Befund (Stelle · Kurzfassung) | Kat. | Status | Umsetzungsnachweis | Begründung bei Abweichung |
|---|---|---|---|---|---|
| — | (kein neuer Befund — Autor-Revision; Prüfung durch Re-Review Runde 4) | — | — | Bericht §4 Rev. 7; `c_kal_rev7_ergebnis.md` | — |

## Runde 4 — Re-Review Rev. 7 (frische Session, 30.08.2026): neue Befunde 77–82

Volle Prüfung der Kalibrierung (§6: Kalibrierung geändert), übrige Abschnitte Regression.
Lint-Stand: Beispiel-Blöcke **10/10 grün** ✓ (inkl. neuem `beispiel_95_beta_sued_nachschaetzung`) ·
Zeichentabellen vollständig ✓ · Parameter-Blöcke vollständig (Quelle, Preisstand, Band/Endpunkt;
c_reg-Blöcke entfernt, β_Süd-Block mit Profil-Band 0,0770–0,0982 = 0,0531 × 1,45/1,85 ✓) ·
Preisstand €2024 einheitlich ✓ · Knoten-/Kanten-Abgleich direkt gegen beide xlsx ✓ (W182 Z405:
E02/S152–S155/S157/S158/R35/R36/W124; NL Z96: In 62;63, Out 87;101, K1, Bausteine
Mortalität+Morbidität; AP P8/Z12, P47/Z146, P52/Z151; RM Z100/Z103/Z106 YLL × VOLY,
Partitionszitat „Hitzetote (ID 95)" Z106) · Quellen: Archiv-Snapshots unverändert
(adjudizierte Abweichungslösung Befund 61). **Kalibrier-Nachrechnung unabhängig aus den
Anlagen-CSVs** (`sommermittel_bundesland_povw.csv` + Rev.-6-Funktionen): c_kal Fenster
0,5808 ✓ (ohne Süd 0,6615 ✓, Vollreihe 0,6596 ✓), R² 0,650 ✓, 8/13 im PI ✓; Prüfstein
**12/16 exakt reproduziert** (alle 16 Verhältnisse identisch zur CSV; Restausreißer SH 1,80 /
HH 1,60 / BY 1,43 / BB 1,42; BW 0,90) und **mit nationalem Skalar gerechnet** ✓;
s_Süd-Zielfunktionsprofil reproduziert (Minimum 1,65; Fit-Obs nord 0 / mitte 12 / süd 7 =
BW 2013/15/17/20/23 + BY 2013/15 — disjunkt von 2018/19/22 ✓); Robustheit: s_Süd-Optimum
bleibt 1,65 auch bei Fit inkl. der Holdout-Jahre; Altersvalidierung 6,3/12,6/24,7/56,4 ✓;
Berlin 221 ✓; DE-Offset +0,53 K (pop-gewichtet über BL) ✓; Gemeindepunkt-Logik
(Zehntel-°C, GK3-Indexierung, Nachbarschafts-Fallback, Gewichtung pop×T) geprüft ✓.
Entscheidungslog 31–33: Empfehlungen plausibel (Messung statt Zell-Lauf; nur-Süd-Nachschätzung
mit Identifikationsdiagnose; Übergangsfaktoren entfallen); Ersetzungs-Querverweise 26/30 ✓.
Regression 58–75 Stichproben (58/59/60/63/71/74/75) tragen; keine 0,742-/c_reg-Reste im
lasttragenden Text ✓. §3.4-Konformität der Süd-Nachschätzung: genau der vorgeschriebene Weg
(„Wirkungsfunktion regional nachschätzen, nicht Kalibrierung regionalisieren") ✓.
Kalibrier-Prüfstein: bestanden — bestätigt, einschließlich der ehrlichen
Voll-Holdout-Variante (Befund 78). Befund 76 (A, Integrationsschritt) unverändert offen.

| Nr | Stelle | Art | Begründung | Vorschlag | Kat. | Status |
|---|---|---|---|---|---|---|
| 77 | §4 Kalibrierlauf Rev. 7, Sensitivität „inkl. vorläufigem 2025: 0,660" | Fehler (§3.4 vorläufige Jahre; behauptete Prüfung nicht gerechnet) | Die Rev.-7-Temperaturreihe endet 2024 (Skript `YEARS = range(1992, 2025)`; `sommermittel_bundesland_povw.csv` ohne 2025-Zeilen) — der Lauf „vollreihe_inkl2025" ist konstruktionsbedingt identisch mit der Vollreihe, weil 2025 im Jahresfilter (`all((J,b) in t_sommer …)`) still herausfällt (Anlage: 0,754/0,754 bzw. 0,660/0,660 mit identischem R²). Die ausgewiesene Sensitivität wurde also nie gerechnet; Rev. 6 zeigte einen echten Effekt (1,042 → 1,029). Basis-Fit korrekt ohne 2025 (Befund 24 unberührt) | 2025-JJA-Raster in die povw-Reihe aufnehmen und Sensitivität echt rechnen **oder** Behauptung ersetzen durch „inkl. 2025 mangels 2025-Temperaturreihe nicht prüfbar (Nachzug bei Datenverfügbarkeit)" | B | behoben (Autor-Revision R4): povw-Reihe bis 2025 verlängert (nur Sensitivität; Offsets weiter Ø 1992–2024) — inkl.-2025 real gerechnet: c = 0,651 (16/27 im PI); §4 + Zeichentabelle aktualisiert · **✓ R5 bestätigt** (CSV enthält 16 × 2025-Zeilen; Nachrechnung aus den Anlagen: inkl. 2025 c = 0,6507 ≠ Vollreihe 0,6596 — echter Effekt; Offsets weiter Ø 1992–2024, Skript-Filter verifiziert; Lauf A 0,744 ≠ 0,754) |
| 78 | §4 Verteilungsprüfung „**BESTANDEN** (out-of-sample …)" · `calibrate_heat_mortality_rev7.py` (c_base) | Fehler/Lücke (Kennzeichnung; §3.4 „Prüfdaten ≠ Fitdaten", §6-Abnahmekriterium „out-of-sample") | Out-of-sample ist nur der s_Süd-Fit (Jahre disjunkt, verifiziert); der **Niveau-Skalar** c_kal = 0,581 ist auf dem Fenster 2012–2024 **einschließlich** der Prüfjahre 2018/2019/2022 gefittet — jedes Länder-Verhältnis skaliert direkt mit diesem teil-in-sample-Faktor. Die Klammer-Einschränkung („die nicht im Nachschätzungs-Fit lagen") deckt die BESTANDEN-Schlagzeile nicht. Materiell robust — nachgerechnet: mit vollständig holdout-gefittetem c (Fenster ohne 2018/19/22: c = 0,567) bleibt der Prüfstein bei **12/16** (BW 0,88 · NW 0,75 · SH 1,76 · HH 1,56 · BY 1,40 · BB 1,38); Lauf A analog 11/16 | Voll-Holdout-Variante (c = 0,567 → 12/16) in §4 + Anlage ausweisen und die BESTANDEN-Aussage darauf stützen; alternativ die out-of-sample-Formulierung präzisieren („Süd-Skalar out-of-sample, Niveau-Skalar in-sample, Robustheitsvariante bestanden") | B | behoben (Autor-Revision R4): Kennzeichnung präzisiert (Süd-Fit out-of-sample, Niveau-Skalar in-sample) + Voll-Holdout-Variante im Skript gerechnet: c = 0,567 → Prüfstein 12/16 (deckt sich mit der Review-Nachrechnung); §4 Fit- und Prüfstein-Bullets · **✓ R5 bestätigt** (Voll-Holdout unabhängig nachgerechnet: c = 0,5670 → 12/16, Länder-Verhältnisse identisch zur R4-Nachrechnung; In-sample-/Out-of-sample-Kennzeichnung in Fit- und Prüfstein-Bullet präzise) |
| 79 | §3.3/§4 `#beta-sued` (Einordnung) | Lücke (§3.8 Widersprüche benennen) | β_Süd = 0,0876 kehrt die publizierte Regionen-Rangfolge um: Winklmayr-Ablesung Nord 0,0634 > Mitte 0,0625 > Süd 0,0531 (Süd flachste Kurve — Adaptionsgradient); nachgeschätzt wird Süd mit Abstand steilste Region (effektives RR bei 25 °C: 1,445 statt publiziert 1,25). Der Bericht kennzeichnet die Nachschätzung als modellintern und dokumentiert Skalar + Band, benennt aber die **Ordnungsumkehr** und ihre Kandidat-Ursachen (Temperatur-Basis-Differenz RKI-Regionsmittel vs. Gemeinde-povw; T0-Süd 20,8; BY/BW-Klimamischung in einer ERF-Region) nicht ausdrücklich | Zwei Sätze in `#beta-sued`: Ordnungsumkehr benennen, Kandidat-Ursachen nennen, Konsequenz (Süd-Werte reagieren am stärksten auf Szenario-Shifts) einordnen | C | behoben (Autor-Revision R4): Ordnungsumkehr in §4 #beta-sued explizit benannt (Süd flachste → steilste Kurve; RR(25 °C) ≈ 1,45 statt 1,25; nur als Kompensationsparameter lesbar, Zell-Lauf prüft Topographie-Anteil) · **✓ R5 bestätigt** (RR(25 °C) = e^(0,0876×4,2) = 1,445 ✓ vs. publiziert 1,25 ✓; Kandidat-Ursachen + Szenario-Konsequenzhinweis über Kompensations-Einordnung abgedeckt) |
| 80 | §3.6/§7 `heat.c_kal` Band [0,55, 0,66] · Zeichentabellen-Referenz „herleitung:#c-kal" · s_Süd „Profil-Band ≈ 1,45–1,85" | Lücke (§3.9 Bandgrenzen herleitungspflichtig; Fertig-Regel) | (a) Band-Obergrenze 0,66 folgt aus den Sensitivitäten (0,660/0,661), die Untergrenze 0,55 steht ohne Rechenweg (nachgerechnet: c bei s_Süd = 1,85 → 0,559; bei 1,45 → 0,604); (b) der Anker `#c-kal` ist nirgends deklariert (§4 deklariert nur `#t-povw`/`#beta-sued`); (c) das s_Süd-Profil-Band 1,45–1,85 nennt kein Kriterium (welcher Zielfunktions-Zuwachs die Grenzen definiert; Profilwerte 1,505/1,385/1,481) — Muster von Befund 74 | Je ein Herleitungssatz: 0,55 = c am oberen s_Süd-Bandrand (0,559, gerundet); `#c-kal`-Anker an den Fit-Absatz setzen; Profil-Band-Kriterium beziffern (z. B. Δ-Zielfunktion ≤ +0,1) oder als Augenmaß-Abschätzung kennzeichnen | C | behoben (Autor-Revision R4): Anker `#c-kal` in §4 deklariert; Band [0,55, 0,66] hergeleitet (außenrundend aus 0,559 bei s_Süd = 1,85 und 0,661 ohne Süd; Stützen 0,604/0,567 im Band; Skript gibt Band-Stützen aus); YAML-Kommentar + §4-Unsicherheiten quantifiziert · **✓ R5 (a)/(b) bestätigt** (Stützen nachgerechnet: 1,45 → 0,6041, 1,85 → 0,5587; #c-kal in §4 deklariert); **Rest (c) → Befund 83** (s_Süd-Profil-Band-Kriterium weiter unbenannt); Rundungs-Widerspruch der neuen Band-Herleitung → Befund 85 |
| 81 | §4 „Konvexitätsbeitrag **gemessen** ×1,023–1,024 (σ = 0,5 K)" | Fehler (Kennzeichnung; §3.9) | „Gemessen" ist falsch: der Beitrag ist eine Modellrechnung **gegen die weiterhin gesetzte** σ = 0,5 K (Befund-69-Rest; der versprochene Messpfad „σ aus dem Stadtmodell" bleibt beim Zell-Lauf); die Rev.-6-Begründungskette der σ-Abschätzung (Spanne/√12, ±1-K-Beispiel) ist mit dem §4-Rewrite entfallen. Nicht lasttragend (reiner Dokumentations-Rest ohne Ausweis-Wirkung) | „gemessen" → „gerechnet gegen die §3.9-Abschätzung σ = 0,5 K (±1-K-Feinstruktur-Spanne, §3.1)"; ein Rückverweis genügt | C | behoben (Autor-Revision R4): „gemessen" → „Modellrechnung gegen die gesetzte σ = 0,5 K"; σ-Begründungskette (±1-K-Spanne, Gleichverteilung ⇒ 2/√12 ≈ 0,5 K) wieder im Text; Messpfad ausdrücklich beim Zell-Lauf · **✓ R5 bestätigt** („keine Messung" explizit; ×1,023–1,024 = Anlagenwerte; σ-Kette = die in R2/R3 adjudizierte Rev.-6-Kette) |
| 82 | §4 `#t-povw` („10.766 Landgemeinden") · Kap. 8 [50] | Lücke (Reproduzierbarkeit §7 „Daten-Pins"; §3.8) | (a) Der Skript-Lauf auf dem aktuellen Repo-Stand liefert **10.853** Gemeinden mit Zensus-Bevölkerung (96 ohne Pop übersprungen; keine AGS-Dubletten) — die Berichtszahl 10.766 ist nicht reproduzierbar (Zahl veraltet oder Eingangsdaten seit dem Lauf geändert; `zensus_gemeinde.json`/VG250-Stand nicht gepinnt). Gewichtungseffekt vernachlässigbar, aber die Kalibrier-Pipeline soll reproduzierbar sein; (b) VG250 (© BKG, dl-de/by-2-0) und `zensus_gemeinde.json` fehlen als eigene Quelleneinträge in Kap. 8 (nur im [50]-Fließtext erwähnt) | Zahl aus dem Lauf übernehmen bzw. Eingangsstände (VG250-Version, Zensus-JSON-Hash/Datum) im Ergebnis-MD pinnen; VG250-Quelleneintrag mit Lizenz ergänzen | C | behoben (Autor-Revision R4): Gemeindezahl korrigiert auf 10.853 (96 ohne Zensus-Eintrag), Daten-Pins (sha256 zensus_gemeinde.json 124fd7a7a15b / DE_VG250.gpkg f229550c8018) im Bericht und automatisch im Ergebnis-MD · **✓ R5 (a) bestätigt** (`load_gemeinden` erneut ausgeführt: 10.853 / 96 übersprungen / 0 Dubletten; beide sha256-Pins gegen die Repo-Dateien verifiziert); **Rest (b) → Befund 84** (VG250-/Zensus-JSON-Quelleneinträge mit Lizenz fehlen weiter) |

### Autor-Revision nach Runde 4 (30.08.2026, gleiche Autor-Session)

Alle sechs Befunde (B: 77/78, C: 79–82) behoben — Details je Zeile oben. Skript-Erweiterungen
in `calibrate_heat_mortality_rev7.py`: YEARS bis 2025 (nur Sensitivität), Voll-Holdout-Prüfstein,
c_kal-Band-Stützen (s_Süd = 1,45/1,85), Gemeindezahl + Daten-Pins im Ergebnis-MD; Kernergebnis
unverändert (c_kal = 0,581 · Prüfstein 12/16 · s_Süd = 1,65). Beispiel-Blöcke 10/10 grün.
Prüfung durch Re-Review Runde 5.

## Runde 5 — Delta-Re-Review nach Runde-4-Revision (frische Session, 30.08.2026): neue Befunde 83–85

Delta-Prüfung der Befunde 77–82 (Status je Zeile oben ergänzt) + Regressionscheck der
Rev.-7-Edits. Lint-Stand: Beispiel-Blöcke **10/10 grün** ✓. **Unabhängige Nachrechnung aus
den Anlagen-CSVs** (`sommermittel_bundesland_povw.csv` inkl. 2025 + Rev.-6-Funktionen):
Fenster c = 0,5808 (R² 0,650; 8/13) ✓ · Vollreihe 0,6596 (16/26) ✓ · **inkl. 2025 = 0,6507
(16/27), 2025 nachweislich im Fit-Set** — echter Effekt, Befund 77 behoben ✓ · Lauf A
0,6615/0,7438 ✓ · Prüfstein 12/16, alle 16 Verhältnisse identisch zur Verteilungs-CSV ✓ ·
**Voll-Holdout c = 0,5670 → 12/16** (Verhältnisse = R4-Nachrechnung: BW 0,88 · NW 0,75 ·
SH 1,76 · HH 1,56 · BY 1,40 · BB 1,38) ✓ · Band-Stützen s_Süd 1,45 → 0,6041 / 1,85 → 0,5587 ✓ ·
Altersvalidierung 6,3/12,6/24,7/56,4 ✓ · Berlin 221 ✓ · DE-Offset +0,53 K ✓ ·
`load_gemeinden` erneut ausgeführt: **10.853** Gemeinden / 96 ohne Zensus-Pop / 0 Dubletten ✓ ·
beide sha256-Daten-Pins (124fd7a7a15b / f229550c8018) gegen die Repo-Dateien verifiziert ✓.
Zahlen-Synchronität Bericht (Kopf, §4 Fit-/Prüfstein-Bullets, #beta-sued, #t-povw,
Zeichentabelle c_kal, YAML `heat.c_kal`): 0,581/0,661/0,660/0,651/0,567/0,559/0,604/12/16/
10.853 überall konsistent ✓; Anker `#c-kal`/`#t-povw`/`#beta-sued` deklariert ✓; keine
0,742-/c_reg-/„10.766"-Reste im lasttragenden Text ✓; RR(25 °C) der Ordnungsumkehr-Passage
nachgerechnet (e^(0,0876×4,2) = 1,445) ✓. Ergebnis: 77/78/79/81 vollständig bestätigt;
80 und 82 je mit einem offenen Teilaspekt (→ 83/84); ein kleiner neuer Widerspruch aus der
Band-Herleitung (→ 85). Keine neuen A-/B-Befunde. Befund 76 (A, Integrationsschritt)
unverändert offen.

| Nr | Stelle | Art | Begründung | Vorschlag | Kat. | Status |
|---|---|---|---|---|---|---|
| 83 | §4 `#beta-sued` „(Profil-Band ≈ 1,45–1,85)" · YAML `heat.beta_regional` Band-Kommentar · Log 32 | Lücke (Rest von Befund 80c; §3.9 Bandgrenzen herleitungspflichtig) | Das s_Süd-Profil-Band 1,45–1,85 nennt weiterhin kein Kriterium und keine Kennzeichnung als Abschätzung; die R4-Behebung deckte nur (a) c_kal-Band und (b) #c-kal-Anker. Anlage liefert die Basis längst: Zielfunktionsprofil 1,45:1,51 · 1,65:1,38 (Min.) · 1,85:1,48 → Bandränder bei Δ ≈ +0,13/+0,10 | Ein Satz: Kriterium beziffern (z. B. „Δ-Zielfunktion ≤ ≈ +0,13 gegenüber dem Minimum 1,38") **oder** als Augenmaß-Abschätzung (§3.9) kennzeichnen | C | behoben (Autor, nach R5): Bandregel benannt — Ränder bei Zielfunktion ≤ +10 % über Minimum (1,51/1,38/1,48; nächste Gitterpunkte +20/+16 %), als Abschätzung gekennzeichnet (§4 #beta-sued, YAML-Kommentar, Log 32) |
| 84 | Kap. 8 [50] | Lücke (Rest von Befund 82b; §3.8 „jede Quelle mit URL/Lizenz") | VG250 (© BKG, Lizenz dl-de/by-2-0) und `zensus_gemeinde.json` (Zensus-2022-Herkunft) fehlen weiterhin als eigene Quelleneinträge; [50] nennt sie nur im Fließtext („VG250-Gemeindepunkte × Zensus-Gemeindebevölkerung"), die R4-Behebungsnotiz zu 82 adressiert Teil (b) nicht | VG250-Eintrag (BKG, gdz.bkg.bund.de, dl-de/by-2-0) + Herkunftszeile für `zensus_gemeinde.json` (Zensus 2022) in Kap. 8 ergänzen | C | behoben (Autor, nach R5): Quelleneinträge [65] BKG VG250 (dl-de/by-2-0) und [66] Zensus 2022 Gemeindebevölkerung (dl-de/by-2-0) in Kap. 8; #t-povw referenziert [65, 66] |
| 85 | §4 c_kal-Band-Herleitung („außenrundend aus der Stützen-Spanne 0,559–0,661") · YAML `heat.c_kal` Kommentar | Widerspruch (klein; Regression aus der Befund-80-Behebung) | „Außenrundend" stimmt nur unten (0,559 → 0,55); oben ist 0,661 → 0,66 **einwärts** gerundet — das Band [0,55, 0,66] schließt die eigene Stütze 0,661 (ohne-Süd-Sensitivität) aus und legt die Vollreihen-Stütze 0,660 exakt auf den Rand. Materiell irrelevant (Δ = 0,001), aber die deklarierte Herleitungsregel widerspricht dem Ergebnis | Obergrenze 0,67 setzen (echt außenrundend) **oder** Formulierung ändern („auf 2 Dezimalen gerundet; obere Stützen 0,660/0,661") | C | behoben (Autor, nach R5): Band außenrundend auf [0,55, 0,67] geweitet (schließt Stütze 0,661 ein; §4 + YAML synchron) |

### Abschluss nach Runde 5 (30.08.2026)

Runde 5 = **NULL-RUNDE** (keine neuen A/B-Befunde); die drei C-Befunde 83–85 wurden
unmittelbar behoben (Ein-Zeilen-Fixes, Details je Zeile; Beispiel-Blöcke 10/10 grün).
Damit ist die §6-Eskalation aus Rev. 6 aufgelöst: Kalibrier-Prüfstein 12/16 bestanden,
auch in der Voll-Holdout-Variante. Der Bericht ist **abnahmereif**; offen bleibt allein
Befund 76 (A, Produkt-Rückstand) — er wird durch `/integriere-risiko 95` geschlossen.

## Integration Rev. 7 → Produkt (30.08.2026, /integriere-risiko 95)

Befund 76 geschlossen (s. Statuszeile). **Offene Fortschreibungsvermerke** (keine
Abnahme-/Integrationsblocker; Bericht §3.6/§4/Kap. 9):

| Nr | Vermerk | Kat. | Status |
|---|---|---|---|
| I-1 | Zellwerte q_1P/q_pfl nicht verfügbar — Zellen rechnen mit Bundesmitteln (kalibrierneutral) | C | **geschlossen (Rev.-8-Nachzug, 30.08.2026):** q_pfl-Ebene `CARE_HOME_SHARE_85P` angelegt — Producer `apply_care_home_share` (inputs.py; OSM-Ingest „infra3": nursing_home/assisted_living; 400 m²-Mindestgewicht; Verteilung nur über pop_85+ > 0; kommunen-erwartungstreu auf q̄), Kartenebene + AUX_LINEAGE, Consumer `_v_vers`. q_1P-Ebene `SINGLE_HH_SHARE_65P` bleibt **geparkt** mit Watchlist (keine offene Quelle; §3.1-konform) |
| I-2 | Zell-Lauf als finaler Kalibrier-Abgleich (national) | C | **geschlossen (Rev. 8, Log 34 / Aufgaben-Fortschreibung 30.08.2026):** nationale 100-m-Vollraster-Läufe sind per §3.4-Ressourcen-Regel unzulässig; ersetzt durch kommunale Stichproben-Abgleiche (Fortschreibungsvermerk §4/§6 des Berichts) |
| I-3 | L̄_85+-Neurechnung mit Sterbefallgewichten (Bericht §3.5, Befund 22) | C | **geschlossen (Rev.-8-Nachzug, 30.08.2026):** 4,16 J in params.py/health.py/catalog.py (ref_value 145)/Golden-Tests; MODEL_VERSION 2026.08-m0-95rev8; Gesamtsuite 282 grün — keine Divergenz Bericht ↔ Code mehr (Befund 92 ✓) |
| I-4 | Raten-Darstellung: Backend liefert rate_per_1000 + rate_unit im Risiko-Layer (layer_cache); Karten-UI-Umschalter (Rate/Absolut) ist Frontend-Ausbau | C | offen (Frontend) |

## Runde 6 — Delta-Review Rev. 8 (frische Session, 30.08.2026): neue Befunde 86–90

Delta-Prüfung der Rev.-8-Bereiche (L̄_85+ §3.5/Log 36 · Ressourcen-Regel-Bereinigung/Log 34 ·
Datenebenen §3.6/Log 35 · Log 34–36/Header/[50]) + Regression; Kalibrierung §4 unverändert
(Anlagen-mtimes vor Rev. 8; c_kal-Zahlen Zeichentabelle/YAML synchron — nur Regressions-Stichprobe).
Lint-Stand: Beispiel-Blöcke **10/10 grün** ✓ · Zeichentabelle L̄_a = 4,16 + Band [4,16, 4,20],
YAML `heat.l_restlebenserwartung` synchron ✓ · Preisstand €2024 unberührt ✓ · LF-14-Stichprobe
RM Z100/Z103/Z106 direkt gegen die xlsx (alle YLL × VOLY) ✓. **L̄_85+ unabhängig nachgerechnet**
(eigener Parser gegen die Quell-XLSX aus ~/.cache, nicht die Skriptfunktionen): Einzeljahre 85–94
m/w ✓ · 95+-Rest 15.251/48.899 ✓ · Kreuzcheck 12613-02↔-03 **exakt** (m 161.178, w 259.771,
Σ 420.949 = m_a-Basis) ✓ · ē(95+) tafelintern 2,151/2,455 ✓ · L̄ m 3,9627 / w 4,2814 ✓ ·
kombiniert (Sterbefallgewichte) 4,1594 → **4,16** ✓ · Sensitivität e(95)-Stützstelle 4,2021 →
Band [4,16, 4,20] ✓ · Log-36-Alternative „Stützstellen-Variante" 4,833 → 4,83 ✓ · YLL-Summen-
Effekt mit Ist-Bandanteilen −8,3 % ≈ „≈ −8 %" ✓ · Kopplung `beispiel_95_zelle_yll`
(0,075 YLL/12.040 €) ✓. Richtungslogik des Bands (ē(95+) < e(95), e fällt mit x) plausibel;
Restnäherung gekennzeichnet. **Ressourcen-Regel:** kein lasttragender Vollraster-Plan mehr im
Bericht (Grep „Zell-Lauf/Vollraster/Batch": nur Regel-/Historien-/Log-Alternativ-Stellen;
§4-Restabsätze, #beta-sued und §6 Modellgrenze 4 auf kommunale Stichproben-Abgleiche
umgestellt ✓; „das löst erst das Zellmodell" [BY] = Produktionsmodell je Kommune, zulässig).
**Datenebenen §3.6:** CARE_HOME_SHARE_85P mit Quelle/keyless/Ableitungsregel/Normierung/
Kappungs-Restfehler/Fallback vollständig nach §3.1; Erwartungstreue Σ q·pop = q̄·pop je Kommune
arithmetisch bestätigt; Kovarianz-Rest (v_vers × UHI) bereits in §4 dokumentiert (Befund 67);
Befund-25(b)-Fortschreibung (Kommunen-Erwartungstreue statt Kreis-Skalierung) plausibel —
Tab. 22421 je Kreis nicht keyless (deckt sich mit dem dokumentierten
Regionalstatistik-Zugangsstand), als Proxy gekennzeichnet ✓; SINGLE_HH_SHARE_65P „geparkt" +
Watchlist + dokumentierter Neutralwert §3.1-konform ✓. **Entscheidungslog 34–36** plausibel
(34/35 ⚠ mit Nutzer-Entscheid/Regelbezug; 36 deterministische Auflösung von Befund 22 wie
terminiert); Header/Revisionsvermerk konsistent; [50]-Ergänzung vorhanden (aber Pfad → Befund 86).
**Produktcode bewusst nicht still gefixt geprüft:** params.py/health.py/Golden-Test rechnen
weiter den Rev.-7-Stand 5,44 (erwartete Divergenz bis Re-Integration — Tracking-Lücke → Befund 90).
Regression 77–85 Stichproben (80/83/85: Band-/Anker-Texte unverändert konsistent) tragen.
Alle 14 Leitfragen mit Verdikt: LF 1/2/3/4/5/7/8/9/13 bestanden (Delta bzw. Regression),
LF 6 bestanden mit Befund 87 (staler Kopplungs-Rest), LF 10 bestanden mit Befund 86
(Anlagen-Pfad), LF 11 bestanden mit Befund 88 (Kommentar-Label), LF 12 bestanden mit
Befund 89 (Randdetails der neuen Ebene), LF 14 bestanden mit Befund 90 (Ledger-Vermerke
I-2/I-3 nicht fortgeschrieben).

| Nr | Stelle | Art | Begründung | Vorschlag | Kat. | Status |
|---|---|---|---|---|---|---|
| 86 | Kap. 8 [50] · Kopf-Anlagenblock · §3.5 `#l-a` · `l85_sterbefallgewichtung.py` (ROOT/DATA) | Fehler (Reproduzierbarkeit/Bundle; §2.7) | Die Rev.-8-Anlagen liegen nicht am dokumentierten Pfad: Skript-Docstring und [50] nennen `backend/data/kalibrierung/`, das Skript schreibt nach **`backend/scripts/data/kalibrierung/`** (ROOT = `dirname(__file__)/".."` — ein `..` zu wenig gegenüber der rev7-Konvention `"..", ".."`); im dokumentierten Anlagenverzeichnis fehlen `l85_sterbefallgewichtung.csv`/`.md`. Nebenbefund: das `.replace(",", ".")` der MD-Ausgabe erzeugt „(2023. DE)" statt „(2023, DE)". Inhaltlich reproduziert die Anlage exakt (s. o.) | ROOT auf `("..", "..")` korrigieren, Skript neu laufen lassen (Anlagen an den dokumentierten Pfad), Fehlstand in `backend/scripts/data/` entfernen; replace-Artefakt fixen | B | behoben (Autor-Revision R6): ROOT-Pfad im Skript korrigiert (`"..", ".."`), fehlplatzierte Dateien unter backend/scripts/data/ entfernt, Anlagen neu erzeugt am dokumentierten Pfad backend/data/kalibrierung/ · **✓ R7 bestätigt** (ROOT Z40 = `"..", ".."`; `backend/scripts/data/` existiert nicht mehr; Anlagen am dokumentierten Pfad, CSV unabhängig nachgerechnet: m 3,9627 / w 4,2814 / kombiniert 4,1594 → 4,16, Band [4,16, 4,20], Sterbefälle 161.178/259.771/420.949 — identisch zur R6-Verifikation); **Rest (replace-Artefakt „(2023. DE)") → Befund 91** |
| 87 | §4 Unsicherheiten-Bullet „\(\bar L_{85+}\)-Approximation (§3.5)" | Lücke (Rev.-8-Kopplung nicht nachgezogen) | Der Bullet listet weiter die „L̄_85+-Approximation" als Unsicherheit — die ist per Log 36 durch die exakte Rechnung ersetzt; verbleibend ist nur die gekennzeichnete ē(95+)-Restnäherung (Band [4,16, 4,20]). §3.5 nennt als neu gerechnete Kopplungen Beispiel/Zeichentabelle/§7/Sanity-Anker, nicht diesen §4-Satz | Bullet umformulieren: „ē(95+)-Restnäherung der L̄_85+-Rechnung (Band [4,16, 4,20], §3.5)" | C | behoben (Autor-Revision R6): §4-Unsicherheiten-Bullet auf die ē(95+)-Restnäherung (Band [4,16, 4,20]) umgestellt · **✓ R7 bestätigt** (Bericht Z649 f.: „ē(95+)-Restnäherung der exakten L̄_85+-Rechnung … die frühere Approximation ist per Log 36 ersetzt") |
| 88 | `beispiel_95_basisraten`, Einordnungs-Kommentar der Alt-Kette | Lücke (Kennzeichnung) | Kommentar „Alte Rev.-7-Kette … zur Einordnung: **5,44**" steht über einer Assert-Zeile, die den **Männer**-Pfad **4,97** rechnet; die Rev.-7-Labels (männlich 4,97 · weiblich 5,69 · kombiniert 5,44) sind beim Kürzen verloren — genannte Zahl ≠ gerechnete Zahl | Kommentar präzisieren: „Männer-Pfad 4,97 (m/w-kombiniert ergab 5,44)" | C | behoben (Autor-Revision R6): Kommentar präzisiert (Männer-Pfad 4,97, w 5,69, kombiniert 5,44) + zusätzliche Assert-Zeile für die 5,44-Kombination · **✓ R7 bestätigt** (beide Asserts nachgerechnet: Männer-Pfad 4,966 → 4,97; Kombination (990.292·4,97 + 1.853.921·5,69)/2.844.213 = 5,439 → 5,44; genannte Zahl = gerechnete Zahl je Zeile) |
| 89 | §3.6 `CARE_HOME_SHARE_85P`, Zell-Ableitungsregel | Lücke (§3.1 Spezifikationstiefe; Randfälle) | Zwei Randdetails unspezifiziert: (a) „Punkte mit Mindestgewicht" ohne Zahlenwert/Regel; (b) Zellen mit Heim, aber \(\text{pop}_{85+,z}=0\) (Zensus-Gitter-Geheimhaltung kleiner Besetzungen) — wohin die zugeteilten Heimbewohner fließen (Verlust analog Kappung? Nachbarzellen?), bleibt offen und berührt die Erwartungstreue-Aussage in Heim-Zellen | (a) Mindestgewicht beziffern oder ausdrücklich als Integrations-Festlegung kennzeichnen; (b) Randfall-Regel ergänzen (z. B. Umverteilung auf Nachbarzellen; Rest wie Kappung als dokumentierter Restfehler) | C | behoben (Autor-Revision R6): Mindestgewicht 400 m² beziffert (gekennzeichnete Setzung); Verteilung nur über Zellen mit pop_85+ > 0 (kein stiller Verlust) — §3.6 präzisiert · **✓ R7 bestätigt** (§3.6: 400 m² als gekennzeichnete Setzung inkl. Polygon-Anhebung; Heim-Gewichte in pop_85+ = 0-Zellen werden der Gewichtssumme entzogen → Kommunen-Erwartungstreue bleibt; Kappung weiterhin dokumentierter Restfehler) |
| 90 | Ledger-Vermerke I-2/I-3 (↔ Rev. 8 Log 34/36) · Produktcode `impact/params.py` Z234, `impact/health.py` Z96, `test_methodik_95_golden.py` Z79 | Widerspruch/Lücke (Eiserne Regel 5; §3.4-Ressourcen-Regel) | (a) I-2 plant weiterhin einen „Zell-Lauf als finalen Kalibrier-Abgleich … nach erster nationaler 100-m-Batchrechnung" — per Aufgaben-Fortschreibung/Log 34 unzulässig; als offener Aktionspunkt riskiert er genau die ausgeschlossene Vollraster-Rechnung. (b) I-3 ist berichtsseitig durch Rev. 8 erledigt, führt aber weiter „~0,3–0,5 J"/„offen" ohne Rev.-8-Verweis (real −1,28 J); die jetzt bestehende Divergenz Bericht ↔ Code (L̄_85+ 4,16 vs. 5,44; zusätzlich fehlende Ebene CARE_HOME_SHARE_85P) ist nirgends aktuell getrackt | I-2 auf kommunale Stichproben-Abgleiche (Log 34) umschreiben bzw. schließen; I-3 fortschreiben: „Berichtsseite Rev. 8 erledigt (−1,28 J); offen: Re-Integration 4,16 + Golden-Test + CARE_HOME_SHARE_85P — kein stiller Code-Fix" | B | behoben (Autor-Revision R6): I-2 geschlossen (Ressourcen-Regel), I-3 auf Rev.-8-Stand fortgeschrieben (Code-Nachzug mit der Rev.-8-Integration; Divergenz bis dahin dokumentiert), I-1 auf die Ebenen-Spezifikation umgestellt · **✓ R7 bestätigt (Ledger-Seite: I-1/I-2/I-3 wie gefordert)**; der unmittelbar anschließende Code-Nachzug (mtimes 22:43–22:44, nach dem Ledger-Stand 22:42) macht die I-3-Divergenz-Aussage jedoch bereits wieder stale und blieb ohne Integrationsvermerk **→ Befund 92** |

### Autor-Revision nach Runde 6 (30.08.2026)

Befunde 86–90 behoben (Details je Zeile). Anlagen neu erzeugt (Pfad korrekt),
Beispiel-Blöcke 10/10 grün. Prüfung durch Re-Review Runde 7.

## Runde 7 — Delta-Re-Review nach Runde-6-Revision (frische Session, 30.08.2026): neue Befunde 91–92

Delta-Prüfung der Befunde 86–90 (Status je Zeile oben ergänzt) + Regressionscheck der Edits.
Lint-Stand: Beispiel-Blöcke **10/10 grün** ✓ · `backend/scripts/data/` existiert nicht mehr ✓ ·
Anlagen `l85_sterbefallgewichtung.csv`/`.md` am dokumentierten Pfad `backend/data/kalibrierung/`,
alle Bericht-Pfadangaben (Kopf, §3.5 `#l-a`, [50]) konsistent ✓ · **CSV unabhängig
nachgerechnet** (Zeilensummen, nicht Skriptfunktionen): m 3,9627 / w 4,2814 / kombiniert
4,1594 → 4,16, Band [4,16, 4,20], Sterbefälle 161.178 / 259.771 / 420.949, ē(95+) 2,151/2,455 —
identisch zur Runde-6-Verifikation ✓ · Befund-88-Asserts nachgerechnet (4,966 → 4,97;
5,439 → 5,44) ✓ · §3.6-Randregeln (400 m², pop_85+ > 0) erwartungstreu-konsistent ✓ ·
§4-Bullet auf ē(95+)-Restnäherung umgestellt ✓ · Ressourcen-Regel-Stellen unverändert (Grep:
nur Regel-/Historien-Stellen) ✓ · `pytest test_methodik_95_golden.py test_impact_health.py`:
27/27 grün ✓. **Regression:** Der Rev.-8-**Code-Nachzug wurde bereits ausgeführt**
(engine/impact/params.py Z234 und health.py Z98 auf 4,16; Golden-Test Z79 auf 4,16;
`MODEL_VERSION = "2026.08-m0-95rev8"`; mtimes 22:43–22:44, unmittelbar **nach** dem
Ledger-Stand 22:42) — Werte-Divergenz Bericht ↔ Code besteht damit nicht mehr, aber das
Tracking hinkt hinterher und die Versions-Annotation behauptet eine nicht angelegte
Zellebene (→ Befund 92). Befunde 86–90: bestätigt (86 mit C-Rest → 91).

| Nr | Stelle | Art | Begründung | Vorschlag | Kat. | Status |
|---|---|---|---|---|---|---|
| 91 | `l85_sterbefallgewichtung.py` Z204 f. · Anlage `l85_sterbefallgewichtung.md` Z8 | Lücke (Rest von Befund 86, Nebenbefund) | Das im Befund-86-Vorschlag mitgenannte replace-Artefakt ist nicht gefixt: `.replace(",", ".")` läuft über den ganzen f-String und macht aus „(2023, DE)" weiterhin „**(2023. DE)**"; zudem erzeugt die MD durchgängig Punkt-Dezimalen (3.963, 4.159) im sonst komma-dezimalen Anlagenbestand. Rein kosmetisch, Zahlen korrekt | Tausender-Formatierung nur auf die Zahl anwenden (z. B. `f"{x:,.0f}".replace(",", ".")` je Wert) statt auf den Satz; optional Dezimalkomma für die J-Werte | C | behoben (Autor-Revision R7): Tausendertrenner-Ersetzung je Zahl statt über den ganzen Satz; Ergebnis-MD neu erzeugt („(2023, DE)" korrekt) · **✓ R8 bestätigt** (Skript Z204–206: replace läuft nur über den reinen Zahlen-String; MD Z8 „(2023, DE)" korrekt; CSV unabhängig nachgerechnet: m 3,9627 / w 4,2814 / kombiniert 4,1594 → 4,16, Sterbefälle 161.178/259.771/420.949 — Zahlen unverändert) |
| 92 | Ledger I-3 + fehlender Rev.-8-Integrationsvermerk · `catalog.py` Z2069 f. (MODEL_VERSION-Kommentar) ↔ `health.py` Z203 ff./Bericht §3.6 | Widerspruch/Lücke (Eiserne Regel 5 / LF 14 Tracking; Workflow „Null-Runde → integriere-risiko") | Der Rev.-8-Code-Nachzug (5,44 → 4,16 in params/health/Golden-Test; MODEL_VERSION-Bump auf 95rev8) wurde **vor** der Runde-7-Bestätigung und ohne Ledger-Fortschreibung ausgeführt: (a) I-3 behauptet weiter eine „bestehende Divergenz Bericht ↔ Code bis zum Nachzug" — sie existiert nicht mehr; ein Integrationsvermerk nach Rev.-7-Vorbild (Abschnitt mit Testnachweis) fehlt; (b) der MODEL_VERSION-Kommentar behauptet „neue Zellebene CARE_HOME_SHARE_85P" — es existiert **kein Producer** (nur der Consumer-Hook `ctx.ci.get("share_care_home_85p")` mit q̄-Fallback; health.py-Docstring sagt selbst „OSM-Pflegeeinrichtungen nicht geladen"; Bericht §3.6: „wird von /integriere-risiko angelegt"); wird die Ebene später ohne erneuten Bump angelegt, invalidiert der Layer-Cache nicht (bekannte Stale-Falle). Werte selbst konsistent (Tests 27/27 grün) | I-3 schließen bzw. fortschreiben („Code-Nachzug 30.08.2026 ausgeführt, 4,16 verdrahtet; offen: CARE_HOME_SHARE_85P-Producer") + Rev.-8-Integrationsvermerk mit Testnachweis; MODEL_VERSION-Kommentar korrigieren („Zellebene spezifiziert, Producer folgt") und beim Anlegen der Ebene erneut bumpen | B | behoben (Autor-Revision R7): Race Review ↔ Nachzug aufgelöst — parallel zur Runde 7 wurde auch der Ebenen-Producer angelegt (apply_care_home_share + OSM-Ingest „infra3" + Kartenebene/AUX_LINEAGE im selben MODEL_VERSION-Bump → keine Cache-Falle); I-1/I-3 geschlossen, Rev.-8-Integrationsvermerk unten; stale Texte in health._v_vers-Docstring und params.py (beta_iso/beta_pfl) nachgezogen · **✓ R8 teilbestätigt:** (a) I-1/I-3 mit Nachweis geschlossen + Rev.-8-Integrationsvermerk mit Testnachweis ✓; (c) MODEL_VERSION-Kommentar konsistent (Ebene + Bump im selben Stand) ✓; (d) health._v_vers-Docstring + params.py beta_iso/beta_pfl nachgezogen ✓; Suite 282 grün, Beispiel-Blöcke 10/10 ✓; **(b) Rückfall:** der Producer entspricht zwar textuell der §3.6-Spezifikation, ist aber in Produktion funktional tot (Koordinaten-Mismatch Mittelpunkt vs. Zellursprung — kein Heim matcht je eine Zelle) **→ Befund 93** |

### Integration Rev. 8 → Produkt (30.08.2026, Nachzug zur Rev.-8-Revision)

- **Werte:** L̄_85+ 5,44 → **4,16** (params.py `life_years_a85p`, health.py
  `AGE_LIFE_YEARS`, Golden-Test); Sanity-Anker `ref_value` 158 → **145 YLL/100k**
  (mittlere L̄ je Hitze-Sterbefall 8,08 J); MODEL_VERSION `2026.08-m0-95rev8`
  (invalidiert Layer-/Dashboard-Caches; Ebene und Bump im selben Stand).
- **Ebene `CARE_HOME_SHARE_85P` angelegt** (§3.1-Anlagepflicht, exakt nach §3.6
  Rev. 8): OSM-Ingest um nursing_home/assisted_living erweitert (Cache-Generation
  „infra3"), Producer `apply_care_home_share` (Grundfläche EPSG:3035, Mindest-
  gewicht 400 m², Verteilung nur über Zellen mit pop_85+ > 0, kommunen-
  erwartungstreu auf q̄_pfl, Kappung bei 1, Fallback Bundesmittel), Kartenebene
  in catalog_auxiliary + build_auxiliary + AUX_LINEAGE; Consumer `_v_vers`.
- **Tests:** Gesamtsuite 282 grün; Beispiel-Blöcke 10/10; Ratchet 0 offen.

## Runde 8 — Delta-Re-Review nach Runde-7-Revision (frische Session, 30.08.2026): neuer Befund 93

Delta-Prüfung der Befunde 91/92 (Status je Zeile oben ergänzt) + Regression. Lint-Stand:
`pytest tests/ -q` **282 passed** ✓ · Beispiel-Blöcke **10/10 grün** (Golden-Test
`test_report_example_blocks_green` extrahiert alle 10 Blöcke aus dem Bericht) ✓ ·
Anlage `l85_sterbefallgewichtung.md` neu erzeugt, Z8 korrekt „(2023, DE)", CSV unabhängig
nachgerechnet (m 3,9627 / w 4,2814 / kombiniert 4,1594 → 4,16, Band [4,16, 4,20],
Sterbefälle 161.178/259.771/420.949 — identisch zu R6/R7) ✓. **Befund-92-Abgleich Code ↔
§3.6 (Rev. 8):** OSM-Ingest (Overpass-Query nursing_home node/way + social_facility
nursing_home|assisted_living, Cache-Kind „infra3" → Query-Digest im Dateinamen, kein
Stale-Cache; Dedup über care_home_ids; `care_home_geoms` in `_empty_infra_features`) ✓ ·
Producer-Logik textuell spezifikationskonform (max(Fläche, 400 m²) in EPSG:3035 inkl.
Polygon-Anhebung; Verteilung q̄·Σpop85 proportional w nur über pop_85+ > 0-Zellen,
explizite 0-Werte für heimlose Zellen ⇒ Erwartungstreue vor Kappung; min(1,·);
Fallback ohne OSM-Heim = kein Key → Faktor 1; q̄ aus Registry `qbar_pfl` 0,149) ✓ ·
Aufruf nach `apply_zensus_to_cell_inputs` ✓ · Consumer `_v_vers` + Kartenebene
(catalog_auxiliary/auxiliary) + AUX_LINEAGE vorhanden und formelkonsistent ✓ ·
MODEL_VERSION-Kommentar (catalog.py Z2069 f.) konsistent ✓ · stale Texte nachgezogen
(health._v_vers-Docstring Rev.-8-Stand; params.py beta_iso „GEPARKT"-/beta_pfl-Ebenen-Text) ✓.
**Aber:** die Producer-Verdrahtung ist defekt — per Minimalreproduktion belegt (Heim exakt
im Zellmittelpunkt ⇒ `share_care_home_85p = None`): `coord_idx` wird mit `x_3035`/`y_3035`
gefüllt, das sind **Zellmittelpunkte** (grid_service.py Z62 f., x0+50; assessment_worker.py
Z180 reicht sie unverändert durch), der Heim-Zentroid-Key floort auf den **Zellursprung**
(`int(c.x // 100) * 100`) — Mittelpunkt ≡ 50 mod 100 vs. Ursprung ≡ 0 mod 100 matchen nie
→ Befund 93 (A). Übrige Regression (91, 87/88-Asserts in der Suite, Golden-/Kontrakt-Tests)
trägt.

| Nr | Stelle | Art | Begründung | Vorschlag | Kat. | Status |
|---|---|---|---|---|---|---|
| 93 | `engine/inputs.py` `apply_care_home_share` (coord_idx Z740–742 vs. Zentroid-Key Z762) ↔ Bericht §3.6 / Ledger I-1 / Log 35 / MODEL_VERSION-Kommentar | Fehler (Rückfall zu Befund 92(b)/I-1; Eiserne Regel 5; §3.1-Anlagepflicht) | Die Ebene `CARE_HOME_SHARE_85P` ist in Produktion **funktional tot**: `coord_idx` indiziert die Zellen über die Mittelpunkts-Koordinaten `x_3035`/`y_3035` (= Zellursprung + 50; grid_service.py Z62 f./assessment_worker.py Z180), der Heim-Lookup-Key ist auf den Zellursprung gefloort (`int(c.x // step) * step`) — die Keys liegen auf disjunkten Restklassen (50 vs. 0 mod 100) und matchen **nie** (Minimalreproduktion: Heim im Zellmittelpunkt ⇒ kein Wert gesetzt). Folge: `weights` bleibt leer → Early Return → jede Kommune läuft in den q̄-Fallback (Faktor 1), die Kartenebene ist überall None — genau der „dauerhafte Neutral-Fallback", den Log 35 als per §3.1 unzulässig verworfen hat; Ledger-I-1-Schließung („intra-kommunale 85+-Differenzierung aktiv") und MODEL_VERSION-Kommentar („neue Zellebene") treffen funktional nicht zu. €-Ausweis unverändert (Fallback kalibrierneutral); kein Test deckt den Producer (Suite deshalb grün — nur der Consumer `_v_vers` ist getestet) | **Kein stiller Fix** — Autor-Session: coord_idx-Keys auf dieselbe Konvention flooren wie den Zentroid-Key (`(int(x // step) * step, int(y // step) * step)` beim Befüllen) oder den Zentroid-Key auf Mittelpunkte heben; **Producer-Unit-Test** ergänzen (Key-Matching + Kommunen-Erwartungstreue Σ q·pop85 = q̄·Σpop85 vor Kappung); da sich Zellwerte ändern: **erneuter MODEL_VERSION-Bump** im selben Stand (Cache-Falle aus Befund 92); Ledger I-1/92(b) erst danach als bestätigt führen | A | behoben (Autor-Revision R8): Zellzuordnung auf konventions-unabhängige Index-Quantisierung int(v // 100) umgestellt (matcht Mittelpunkts- UND Ursprungs-Koordinaten); Producer-Unit-Tests ergänzt (test_care_home_share_producer_expectation_true: Mittelpunkts-Minimalreproduktion, Erwartungstreue Σ share·pop85 = q̄·Σpop85, pop85=0-Ausschluss, Kappung; + Fallback-Test ohne OSM-Heim); MODEL_VERSION erneut gebumpt (2026.08-m0-95rev8b — Stände mit leerer Ebene invalidiert); Gesamtsuite 284 grün · **✓ R9 bestätigt** (Index-Quantisierung `int(v // 100)` auf beiden Seiten verifiziert; R8-Minimalreproduktion [Heim exakt im Zellmittelpunkt] matcht jetzt: share 0,745 ✓; eigene Stichproben: Randlage x₀+0,3/y₀+99,7 → 0,745 ✓, Ursprungs-Fallback `col·step` → 0,745 ✓, Kappung p85=5 → 1,0 ✓, Heim in pop85=0-Zelle bei zweitem Heim → Gewicht entzogen, Rest erwartungstreu 0,149 ✓; grid_service-Mittelpunkts-Konvention x₀+50 und 100-m-Gitterausrichtung x_start = ⌊minx/100⌋·100 verifiziert — Quantisierung konventions-unabhängig korrekt; einziger Produktions-Caller Z701; MODEL_VERSION 2026.08-m0-95rev8b + Kommentar konsistent; Suite 284 passed / 10 skipped, Beispiel-Blöcke 10/10); **Rest (Nachweis-Claim „Kappung" ohne bindenden Testfall) → Befund 94** |

### Autor-Revision nach Runde 8 (30.08.2026)

Befund 93 (A) behoben — Details in der Statuszeile. Prüfung durch Re-Review Runde 9.

## Runde 9 — Delta-Re-Review nach Runde-8-Revision (frische Session, 30.08.2026): neuer Befund 94

Eng gescopter Delta-Re-Review Befund 93 + Regression (Bericht unverändert seit Runde 7,
mtime 22:41 vor der R8-Revision verifiziert). **Fix bestätigt:** Zellzuordnung in
`apply_care_home_share` jetzt per Index-Quantisierung `int(v // 100)` auf beiden Seiten —
Zellseite `(int(x_3035 // 100), int(y_3035 // 100))` (Mittelpunkt x₀+50 → x₀/100, da
grid_service-Gitter 100-m-ausgerichtet: x_start = ⌊minx/100⌋·100), Heimseite Zentroid
beliebig in [x₀, x₀+100) → derselbe Key; Fallback `col·step` (Ursprungs-Konvention) landet
ebenfalls auf `col`. Neuer Producer-Test `test_care_home_share_producer_expectation_true`
ausgeführt ✓ (Mittelpunkts-Minimalreproduktion = exakt der R8-Repro-Fall; Erwartungstreue
Σ share·pop85 = q̄·Σpop85 = 14,9; expliziter 0-Wert cis[1]; pop85=0-Zelle ohne Key) und
`test_care_home_share_no_osm_leaves_fallback` ✓. **Eigene Stichproben** (unabhängig vom
Test): Heim-Randlage (x₀+0,3 / y₀+99,7) → 0,745 ✓ · Ursprungs-Konvention-Zellen (nur
col/row, kein x_3035) → 0,745 ✓ · Kappung (p85=5, residents 14,9) → 1,0 ✓ · Heim in
pop85=0-Zelle einer Kommune mit zweitem Heim → Gewicht entzogen, verbleibende Zelle
erwartungstreu 0,149 ✓. MODEL_VERSION `2026.08-m0-95rev8b` gebumpt, Kommentar korrekt
(Ebene-Fix + Invalidierung leerer Stände) ✓ — Cache-Falle geschlossen. **Regression:**
`pytest backend/tests/ -q` **284 passed, 10 skipped** ✓ (282 + 2 neue Producer-Tests);
Beispiel-Blöcke 10/10 (Golden-Test zählt und exekutiert alle ```python test:``-Blöcke,
Grep bestätigt 10) ✓; Stichprobe 91 (Anlage „(2023, DE)" korrekt) ✓; Consumer-Verdrahtung
`_v_vers`/auxiliary/AUX_LINEAGE unverändert ✓. Einziger neuer Befund: 94 (C, Nachweis-
Präzision — Muster Befund 88). Keine neuen A-/B-Befunde.

| Nr | Stelle | Art | Begründung | Vorschlag | Kat. | Status |
|---|---|---|---|---|---|---|
| 94 | Ledger-Statuszeile 93 (Umsetzungsnachweis) · `test_methodik_95_golden.py` Abschnitt 4 | Lücke (Nachweis-Präzision; Muster Befund 88: genannter Prüfumfang ≠ geprüfter Umfang) | Der Umsetzungsnachweis zu 93 führt „**Kappung**" als vom Producer-Test abgedeckte Eigenschaft; im Test wird die Kappung aber nie bindend (Maximum share = 0,745 = min(1, 0,745) — der min-Aufruf läuft durch, der Kappungsast ist nicht regressionsgeschützt). Verhalten selbst korrekt (eigene Stichprobe: p85 = 5, residents 14,9 → share exakt 1,0), aber ein künftiger Regressionsbruch im Kappungsast bliebe testseitig unentdeckt | Bindenden Kappungs-Fall in den Producer-Test aufnehmen (z. B. Zelle p85 = 5 → share == 1.0) **oder** „Kappung" aus dem Nachweis-Claim streichen | C | behoben (Autor, nach R9): eigener Testfall test_care_home_share_cap_binds (pop85 = 5, Bewohner 12,7 → share exakt 1,0; Kappungs-Verlust als dokumentierter Restfehler mitgeprüft); Gesamtsuite 285 grün |

### Abschluss nach Runde 9 (30.08.2026)

Runde 9 ergab **keine neuen A-/B-Befunde** (§6-Konvergenzkriterium 3 erfüllt);
der einzige C-Befund 94 wurde unmittelbar behoben (Kappungs-Regressionstest,
Suite 285 grün). Der Bericht Rev. 8 ist damit **abnahmereif** und der
Produkt-Nachzug vollzogen (Integrationsvermerke Rev. 7/Rev. 8 oben): Werte,
Ebene CARE_HOME_SHARE_85P (Producer-getestet), Ledger konsistent — **keine
offenen Befunde** (I-1/I-2/I-3 geschlossen; q_1P-Ebene regulär geparkt mit
Watchlist).

## Runde 10 — Fortschreibung 7, Schritt 1 (T-1118, 25.09.2026): neue Befunde 95–100

Anlass: A-0048 / T-1113-cmo (Fortschreibung 7 der Aufgabe vom 24.09.2026). Ausgangslage vor jeder
Änderung am Bericht: `python3 backend/scripts/lint_methodik.py 95` meldet 161 grün und 4 ROT (Befunde
95–98). Befunde 99 und 100 sind bei der Arbeit an der Rechenkette aufgefallen.

| Nr | Stelle | Art | Begründung | Vorschlag | Kat. | Prüfausdruck | Status |
|---|---|---|---|---|---|---|---|
| 95 | Kapitel 9 (Ansatz-Vergleich) | Formverstoß (Fortschreibung 7: eine Methodik je Risiko) | Lint: „Kein Kapitel 9 (eine Methodik je Risiko)“ ROT; Kapitel 9 führt 95-A, 95-B und 95-C nebeneinander | Kapitel 9 streichen; 95-B und 95-C mit je einem Satz ins Entscheidungslog | B | `! grep -q '^## 9 ' docs/methodik/95_hitzebelastung.md` | behoben (T-1118): Kapitel 9 gestrichen; 95-B und 95-C als Entscheidungslog Nr. 37 und 38 mit je einem Satz, 95-A bleibt Nr. 1 |
| 96 | Kapitel 3, Anfang | Lücke (Aufgabe §4, §8 E1) | Lint: „### 3.0 Rechenkette“ fehlt; der Bericht erzählt den Weg von der amtlichen Quelle zum Euro-Betrag nirgends am Stück | Rechenkette 3.0 mit Beispielkommune, höchstens zehn Ebenen, und genau einem Beispiel-Block rechenkette_95 | A | `python3 -c "import sys; s=open('docs/methodik/95_hitzebelastung.md').read(); sys.exit(not ('### 3.0 Rechenkette' in s and s.count('python test: rechenkette_95') == 1))"` | behoben (T-1118): Abschnitt 3.0 Rechenkette, Beispielkommune Berlin, 10 Ebenen bis zum bewerteten Schaden K1, Beispiel-Block rechenkette_95 |
| 97 | §3.6 Zeichentabelle, Zeile Sommermitteltemperatur (T̄_Zelle) | Lücke (Herkunft) | Lint: Herkunft „DWD 1 km + UHI“ ohne Register-ID, Herleitung oder Quellennummer | Herkunft mit [33] und register:95-W124-01 | C | `python3 -c "import sys; z=[l for l in open('docs/methodik/95_hitzebelastung.md') if 'Sommermitteltemperatur (24-h' in l]; sys.exit(not (len(z) == 1 and 'register:95-W124-01' in z[0]))"` | behoben (T-1118): Herkunft DWD-CDC-Raster [33] plus Stadtklima-Zuschlag, register:95-W124-01 |
| 98 | §8 Quelle [47], Zeile 996 | verbotene Formulierung | Lint: verbotenes Wort in „Rev.-5-…zitat“ (Zeile 996) | sachlich ersetzen: nicht belegtes Zitat aus Rev. 5 | C | `! grep -q 'Platzhalter' docs/methodik/95_hitzebelastung.md` | behoben (T-1118): ersetzt durch „einem in Rev. 5 nicht am Volltext belegten Zitat“ |
| 99 | §3.0 Rechenkette, Ebene 1 | Abweichung vom Ticket (Datenstand) | Das Ticket verlangt Einwohner je Altersband aus dem Zensus 2022 (Stichtag 15.05.2022). Die Zensus-Datenbank (ergebnisse.zensus2022.de) ist laut Betreiber bis 05.10.2026 in Wartung, der API-Abruf am 25.09.2026 scheitert (HTTP 400). Verwendet ist die amtliche Fortschreibung auf Basis Zensus 2022, Stichtag 31.12.2023 (Tab. 12411-09-01-4-B, Anlage bevoelkerung_bundesland_altersband.csv); das ist derselbe Stichtag wie der Nenner der Basissterberaten m_a [49], also in sich stimmiger. Abstand zum Zensus-Stichtag: 19 Monate Fortschreibung | Entscheidung methodik_manager: Fortschreibung 31.12.2023 behalten (Stichtag gleich m_a) oder nach dem 05.10.2026 auf Zensus-Tabelle 1000A umstellen | C | `grep -q 'Stichtag 31.12.2023, Basis Zensus 2022' docs/methodik/95_hitzebelastung.md` | zurückgestellt (Entscheidung methodik_manager; Zensus-Datenbank bis 05.10.2026 in Wartung) |
| 100 | §8 Quelle [66] | falscher Pfad | [66] nennt die Repo-Aufbereitung backend/data/lite/zensus_gemeinde.json; die Datei gibt es auf dem Branch nicht (Verzeichnis backend/data/lite/ fehlt) | Pfad in [66] korrigieren oder Aufbereitung nachweisen | C | `test -f backend/data/lite/zensus_gemeinde.json` | zurückgestellt (Schritt 2 von T-1113, Quellenpflege) |

## Runde 11 — Nacharbeit 1 zu T-1118 nach Urteil methodik_manager (25.09.2026): neue Befunde 101–103

Urteil Runde 0: Nacharbeit mit zwei Punkten (E3 und P1), hier Befunde 102 und 103. Befund 101 hat sich
bei der Messung zu Befund 102 ergeben.

**Messung Zellvergleich Berlin** (Grundlage für 101 und 102; das Skript liegt nicht im Repo, weil T-1118
nur Bericht und Ledger zulässt): Alle 40.663 bewohnten 100-m-Zellen des Zensus 2022 innerhalb der
Stadtgrenze Berlin (Grenze aus OpenStreetMap/Nominatim, nur für die Zellauswahl; 891,1 km²; 3.595.270
Einwohner) aus den Gitterdaten [67]. Jede Zelle erhält ihren Wert aus der DWD-Klimatologie mit den
Produktfunktionen `dwd_cdc_grid.climatology_grid` („air_temp_mean“, Monate 6–8, bzw. „hot_days“, je 10
Jahre) und `sample_grid_points`. Formeln §3.3–§3.5 mit den Werten aus Kapitel 7, Bandsummen wie
Ebene 1. Ergebnisse: Berlin-Mitte 20,07 °C, Bevölkerungsmittel 19,96 °C (19,38–20,38 °C), Zellen
wärmer als Mitte: 24,8 % der Einwohner. Betrag Kette 362,89 Mio. €; Zellen mit Berliner
Altersstruktur 343,73 Mio. € (× 0,947); dazu Feinstruktur σ = 0,5 K (Gauß-Hermite, 21 Punkte) × 1,0204;
Altersgewichtung aus den 2.815 Zellen mit vollständigen Altersangaben (241.174 Einwohner; 85+ im
Mittel 19,926 °C statt 19,963 °C) × 0,988. Zusammen × 0,955, rund 347 Mio. €. Die Reihe des
Berlin-Gemeindepunkts in `sommermittel_bundesland_povw.csv` ergibt für 2016–2025 im Mittel 20,06 °C,
also dieselbe Lage wie Berlin-Mitte.

| Nr | Stelle | Art | Begründung | Vorschlag | Kat. | Prüfausdruck | Status |
|---|---|---|---|---|---|---|---|
| 101 | §4 Zusatz-Anker Berlin 2018 („das Zellmodell wird für Berlin … über dem Gemeindepunkt-Wert liegen“) | Widerspruch Messung ↔ Begründung | Der Zellvergleich zeigt das Gegenteil: Der Gemeindepunkt (20,06 °C) liegt 0,1 K über dem Bevölkerungsmittel. Das Zellmodell liegt mit Feinstruktur σ = 0,5 K und Altersgewichtung 4,5 % unter dem Gemeindepunkt-Wert. Die Unterschätzung des Ankers (−15 %) wird damit nicht kleiner, sondern größer (rund −19 %). Sie bleibt unerklärt. Kein Wert aus Kapitel 7 ist betroffen | Begründung in §4 neu fassen: Richtung gemessen, verbleibende Lücke offen benennen; Anker-Aussage „konservativ = unterschätzend“ bleibt | B | `! grep -q 'das Zellmodell wird für Berlin' docs/methodik/95_hitzebelastung.md` | zurückgestellt (Entscheidung methodik_manager; §4 gehört nicht zum Auftrag von T-1118, kein Wert betroffen) |
| 102 | §3.0, Zusammenfassung „eine Zelle statt aller Zellen“ | E3: Richtung und Größe nicht belegt, Widerspruch zu §4 (Urteil Runde 0, Punkt 1) | Der Text nannte +2,8 % (±1 K gleichverteilt, abweichend von σ = 0,5 K in §4) und −23 % je 0,5 K ohne gemessene Richtung | Zellvergleich messen, Richtung und Größe beziffern, Beziehung zu §4 benennen | B | `grep -q '0,947 × 1,020 × 0,988 = 0,955' docs/methodik/95_hitzebelastung.md` | behoben (T-1118 Nacharbeit 1): gemessen (a) −5,3 %, (b) +2,0 % Modellrechnung σ = 0,5 K wie §4, (c) −1,2 %; Kette überschätzt Berlin um rund 4,5 %; Widerspruch zu §4 als Befund 101; Quelle [67] neu; Block rechenkette_95 prüft die Verknüpfung und (b) am Punkt |
| 103 | §3.0, Abschätzung „+6 %“ (Heim-Extremfall) | P1: Abschätzung ohne Herleitung (Urteil Runde 0, Punkt 2) | Zahl stand ohne Rechenweg im Bericht | Herleitung Schritt für Schritt in den Text und in den Beispiel-Block | B | `grep -q '0,344 × 1,598 + 0,656 = 1,206' docs/methodik/95_hitzebelastung.md` | behoben (T-1118 Nacharbeit 1): Herleitung v 2,31/0,77, Anteile 0,344/0,656, Exzess × 1,598, 85+ × 1,206, Anteil YLL 28,4 % ⇒ +5,8 % als Obergrenze; im Block rechenkette_95 nachgerechnet |

## Runde 12 — Nacharbeit 2 zu T-1118 nach Urteil methodik_manager Runde 1 (25.09.2026): neue Befunde 104–106

Urteil Runde 1: Nacharbeit wegen E3 (Unterschied Fortschreibung ↔ Zensus-Gitter im Produkt nicht
ausgewiesen, Befund 105) und zweier Stilverstöße gegen kap3-stil (Befund 106).

**Messung Zellvergleich Berlin, Fassung 2** (ersetzt die Zerlegung aus Runde 11; Skript wieder nur im
Probeverzeichnis): wie Runde 11, aber jede Zelle mit ihrer Bevölkerung nach der Logik des Produkts
(`zensus_loader.apply_zensus_to_cell_inputs`): Einwohner aus „Bevölkerungszahl“ [67], 65+ = Einwohner ×
AnteilUeber65 aus „Anteil ab 65-Jährige in Gitterzellen“ (destatis.de/static/DE/zensus/gitterdaten/
Anteil_ab_65-jaehrige_in_Gitterzellen.zip), Aufteilung der 65+ aus den 5er-Jahresgruppen der Zelle,
sonst aus dem Gebiet. Bandsummen Produkt: 2.900.648 · 334.805 · 263.035 · 96.781 = 3.595.270, gegen
Ebene 1 × 0,980 · 0,986 · 1,038 · 0,897. Schritte, jeder auf den vorigen: Kette 362,89 Mio. € →
(a) Temperatur je Zelle, Berliner Altersstruktur 344,01 (× 0,948) → (b) Einwohnersumme Gitter
337,70 (× 0,982) → (c) Bänder je Zelle wie im Produkt 331,42 (× 0,981) → (d) Feinstruktur
σ = 0,5 K 338,22 (× 1,0205); zusammen × 0,932. Variante (c) mit Ersatz: Zellen ohne Anteil 65+
erhalten den Anteil 65+ der übrigen Berliner Zellen (19,87 %): 338,13 statt 331,42, also Produkt ×
0,980 gegenüber Ersatz, Rest × 1,001. Die frühere Wirkung „Altersverteilung −1,2 %“ aus Runde 11 stammte
aus den 2.815 Zellen mit vollständigen Altersangaben, einer verzerrten Teilmenge. Sie ist durch (c) ersetzt.

| Nr | Stelle | Art | Begründung | Vorschlag | Kat. | Prüfausdruck | Status |
|---|---|---|---|---|---|---|---|
| 99 | §3.0 Rechenkette, Ebene 1 | Abweichung vom Ticket (Datenstand), Nachtrag Runde 12 | Wie Runde 11. Gemessen: Das Produkt rechnet mit dem Zensus-Gitter (Stichtag 15.05.2022), in Berlin 3.595.270 Einwohner gegen 3.662.381 in Ebene 1 (× 0,982); Bänder nach Produktlogik × 0,980 · 0,986 · 1,038 · 0,897 (85+ zum Teil wegen Befund 104). Im Bericht als Wirkung (b) und (c) ausgewiesen | Entscheidung methodik_manager: Ebene 1 behalten und den Unterschied wie jetzt ausweisen, oder Ebene 1 auf die Zensus-Tabelle 1000A umstellen (nach dem 05.10.2026) | C | `grep -q 'Stichtag 31.12.2023, Basis Zensus 2022' docs/methodik/95_hitzebelastung.md` | zurückgestellt (Entscheidung methodik_manager) |
| 101 | §4 Zusatz-Anker Berlin 2018 | Widerspruch Messung ↔ Begründung, Nachtrag Runde 12 | Zahl aus Runde 11 berichtigt: Für die Aussage zum Gemeindepunkt zählen nur Temperatur je Zelle und Feinstruktur, zusammen × 0,967 (−3,3 %); die Unterschätzung des Ankers wächst damit von −15 % auf rund −18 %. Die übrigen Wirkungen betreffen die Bevölkerungsgrundlage, nicht den Gemeindepunkt | wie Runde 11 | B | `! grep -q 'das Zellmodell wird für Berlin' docs/methodik/95_hitzebelastung.md` | zurückgestellt (Entscheidung methodik_manager; §4 gehört nicht zum Auftrag von T-1118, kein Wert betroffen) |
| 102 | §3.0, Zusammenfassung „eine Zelle statt aller Zellen“ | Nachtrag Runde 12 | Zerlegung aus Runde 11 erweitert und berichtigt (siehe Befund 105); der Prüfausdruck aus Runde 11 prüfte die alte Zahlenfolge | — | B | `grep -q 'Die Kette überschätzt Berlin um rund' docs/methodik/95_hitzebelastung.md` | behoben (T-1118 Nacharbeit 2): Aussage und Richtung bleiben, Größe jetzt × 0,932 |
| 104 | Produkt: `zensus_loader.apply_zensus_to_cell_inputs` (share_o = … or 0.0) ↔ Bericht §3.3 (pop_a aus Zensus 2022) | Divergenz Bericht ↔ Code | Ist der Anteil 65+ einer Zelle im Gitter geheimgehalten („–“), setzt das Produkt 65+ = 0 und zählt alle Einwohner als u65. Das „–“ bedeutet dort nicht „keine Älteren“: Im Raum Berlin tragen dieselben Zellen im Altersgitter 1312 veröffentlichte Seniorenfelder mit Wert > 0. Berlin: 4770 Zellen, 99.026 Einwohner; Betrag × 0,980 (−2,0 %) gegenüber einem Ersatz mit dem Anteil 65+ des Gebiets. Die Wirkung in ländlichen Kommunen mit vielen kleinen Zellen ist nicht gemessen und kann größer sein | Code-Nachzug beim cto: bei fehlendem Anteil 65+ die 5er-Jahresgruppen der Zelle oder den Anteil des Gebiets verwenden; Regeln dafür im Bericht §3.3 festlegen | B | `! grep -q 'share_o = ci.get("share_over_65") or 0.0' backend/app/services/zensus_loader.py` | zurückgestellt (Code-Nachzug cto; Code liegt außerhalb des Dateirahmens von T-1118) |
| 105 | §3.0, Liste der Zusammenfassungen | E3: stille Vereinfachung (Urteil Runde 1) | Ebene 1 nimmt die Fortschreibung (3.662.381 Einwohner), das Produkt das Zensus-Gitter (3.595.270); der Unterschied und die Altersbänder nach Produktlogik fehlten in der Liste, die Aussage „rund 347 Mio. €“ war zu hoch | Unterschied messen und als eigene Wirkung ausweisen | B | `grep -q '0,948 × 0,982 × 0,981 × 1,020 = 0,932' docs/methodik/95_hitzebelastung.md` | behoben (T-1118 Nacharbeit 2): Wirkungen (b) Einwohnersumme × 0,982 und (c) Bänder je Zelle × 0,981 (davon Produkt-Eigenheit × 0,980, Befund 104) ausgewiesen; Zelllauf rund 338 Mio. € (Preisstand 2024), ohne Eigenheit rund 345 Mio. €; Block rechenkette_95 prüft die Verknüpfung |
| 106 | §3.0, Text und Block | Stil (kap3-stil, Urteil Runde 1) | Spannen mit „bis“ statt Halbgeviertstrich (Ebene 4, Temperaturspanne der Zellen); „Stadt“/„Stadtmittel“ statt „Kommune“ als Betrachtungsebene; Betrag mit vier gültigen Stellen und ohne Preisstand im Fließtext | Halbgeviertstrich, „Kommune“, Betrag gerundet mit Preisstand | C | `python3 -c "import re,sys; s=open('docs/methodik/95_hitzebelastung.md',encoding='utf-8').read(); t=s[s.index('### 3.0'):s.index('### 3.1')]; sys.exit(bool(re.search(r'[0-9] bis [0-9]', t)) or ('Stadtmittel' in t) or ('in der Stadt' in t))"` | behoben (T-1118 Nacharbeit 2): 20,58–24,67 °C, 19,38–20,38 °C, „Mittel der Kommune“, „rund 338 Mio. € je Jahr (Preisstand 2024)“ |

## Runde 13 — Fortschreibung 7, Schritt 2 (T-1119, 25.09.2026): neue Befunde 107–111

Anlass: A-0048 / T-1113-cmo, Pflichtinhalte der Fortschreibung 7. Ausgangslage vor jeder Änderung am Bericht:
`python3 backend/scripts/lint_methodik.py 95` meldet 202 Checks grün; die Befunde 107–111 sind Lücken gegenüber
Ticket und Aufgabe, die der Lint nicht prüft. **Vorrangregel (Aufgabe, Ende):** nicht angewendet, weil kein Widerspruch
besteht. KWRA-2021-Mappe `docs/KWAR/KWRA-2021_Klimawirkungen.xlsx`, Blatt `Klimawirkungen`, Zeile 97 (ID 95),
Spalten N–R: hoch · mittel · hoch · mittel · hoch; Spalten S/T: hoch/mittel. Teilbericht 6, Tabelle 1, S. 41 (als Bild
gelesen): gleichlautend, dazu Anpassungsdauer 10–50 Jahre wie Spalte U. Teilbericht 6, S. 78, Fußnote 18, und S. 79:
Skala 1–4, Hitzebelastung unter den Klimawirkungen mit gemitteltem Wert 3,5; (4 + 3) / 2 = 3,5 passt zur Mappe.

| Nr | Stelle | Art | Begründung | Vorschlag | Kat. | Prüfausdruck | Status |
|---|---|---|---|---|---|---|---|
| 107 | Kapitel 1 | Lücke (Pflichtabsatz der Aufgabe, Stand Commit 66361a51) | Unterabschnitt „Risiko ohne (weitere) Anpassung“ fehlt; keine KWRA-Stufe mit Fundstelle | Wortlaut aus 66361a51 als Text einfügen, KWRA-Stufe mit Blatt, Zeile, Spalte | B | `python3 -c "import sys; s=open('docs/methodik/95_hitzebelastung.md',encoding='utf-8').read(); i=s.find('### Risiko ohne (weitere) Anpassung'); sys.exit(not (s.count('### Risiko ohne (weitere) Anpassung') == 1 and 0 < i < s.index('## 2 Evidenz') and 'Zeile 97 (ID 95), Spalten N–R' in s))"` | behoben (T-1119): Unterabschnitt am Ende von Kapitel 1; Stufen Gegenwart hoch, Mitte mittel/hoch, Ende mittel/hoch mit Fundstelle Mappe und [68] Tab. 1 |
| 108 | Kapitel 1, Absatz (a) im Wortlaut von 66361a51 | P1: Behauptung ohne Beleg | Satz „… und dem vorhandenen Bestand an Klimaanlagen und Hitzeaktionsplänen kalibriert“: Der Bericht hat keine Quelle für die Klimaanlagen-Quote und keine für die Verbreitung der Hitzeaktionspläne in den Kalibrierjahren 2012–2024 | belegen oder streichen | B | `! grep -q 'Bestand an Klimaanlagen und Hitzeaktionsplänen kalibriert' docs/methodik/95_hitzebelastung.md` | behoben (T-1119): gestrichen, Entscheidungslog Nr. 39; (a) sagt nur, was aus der Kalibrierung folgt, und nennt das DWD-Hitzewarnsystem mit [45] |
| 109 | Kapitel 1 | Lücke (Fortschreibung 7: Gewissheit) | KWRA-Gewissheit je Zeitscheibe fehlte, ebenso der Unterschied zur eigenen Quellenlage | Gewissheit Mitte/Ende mit Fundstelle, Mittel 3,5 nach Teilbericht 6, S. 78–79, Satz zur Abweichung | B | `python3 -c "import sys; s=open('docs/methodik/95_hitzebelastung.md',encoding='utf-8').read(); sys.exit(not ('S. 78–79' in s and '(4 + 3) / 2 = 3,5' in s and 'Warum die eigene Quellenlage davon abweicht' in s))"` | behoben (T-1119): Mitte hoch, Ende mittel (Spalten S/T), Skala nach Fußnote 18, Mittel 3,5; Abweichung: Die KWRA bewertet die Einstufung des künftigen Risikos, der Bericht rechnet das heutige Klima aus gemessenen Größen und weist Bänder aus; Quelle [68] neu |
| 110 | Kapitel 6 | Lücke (Fortschreibung 7) | Kein Satz, dass die Beträge Jahresbeträge ohne Abzinsung sind | Satz ergänzen; Diskontrate nicht festlegen | C | `python3 -c "import sys; s=open('docs/methodik/95_hitzebelastung.md',encoding='utf-8').read(); t=s[s.index('## 6 '):s.index('## 7 ')]; sys.exit('Jahresbeträge ohne Abzinsung' not in t)"` | behoben (T-1119): Absatz „Jahresbeträge ohne Abzinsung“ nach der Szenario-Anwendung |
| 111 | Kapitel 7, alle 19 Blöcke | Formverstoß (Aufgabe §4, Felder `kennzeichnung`, `abgeleitet_aus`, `rolle`) | Feld `kennzeichnung` fehlte in allen Blöcken | Feld je Block; `abgeleitet_aus` bei `berechnet`; `rolle` für c_kal und Distanzterm | B | `python3 -c "import re,sys; s=open('docs/methodik/95_hitzebelastung.md',encoding='utf-8').read(); b=s[s.index('## 7 '):s.index('## 8 ')].split('parameter:')[1:]; sys.exit(not (len(b) == 23 and all(re.search(r'^ *kennzeichnung: (\S+)', x, re.M).group(1) in ('quelle', 'abschaetzung_kap3', 'berechnet') for x in b) and all(re.search(r'^ *abgeleitet_aus: .heat', x, re.M) for x in b if 'kennzeichnung: berechnet' in x)))"` | behoben (T-1119): 10 × quelle, 6 × abschaetzung_kap3, 3 × berechnet (c_kal, beta_iso, beta_pfl); rolle kalibrierung (c_kal), sensitivitaet (Distanzterm); Lesart der Grenzfälle im Entscheidungslog Nr. 40; keine `wert:`-Zeile geändert; Prüfausdruck in Runde 24 (T-1295) von 19 auf 22 Blöcke fortgeschrieben, weil drei Maßnahmen-Blöcke dazukamen (Befunde 122 und 123); in Runde 27 (T-1329) auf 23 Blöcke, weil `heat.delta_vg_morb` dazukam (Befund 131) |

## Runde 14 — Nacharbeit 1 zu T-1119 nach Urteil methodik_manager Runde 0 (25.09.2026): neue Befunde 112–114

Urteil Runde 0 (2026-09-25T15:30:32Z): Nacharbeit, neue Befunde B 1, C 2; die Abnahmepunkte (1) bis (6) sind erfüllt,
Golden-Test 12 von 12 grün. Die drei Befunde sind unverändert aus dem Urteil übernommen, vor jeder Änderung am Bericht.

| Nr | Stelle | Art | Begründung | Vorschlag | Kat. | Prüfausdruck | Status |
|---|---|---|---|---|---|---|---|
| 112 | Kap. 7, Block heat.c_fall (und heat.l_restlebenserwartung) ↔ Entscheidungslog Nr. 40 | Widerspruch (P1, Aufgabe §4) | Log 40 verlangt `abschaetzung_kap3`, sobald eine Setzung von KAP3 im Wert steckt. c_Fall ist nach §3.5, Zeichentabelle, Band-Kommentar und Log 17 ein Proxy (Ø aller KH-Fälle, Alternative DRG-Sätze), also eine Setzung von KAP3. Der Block trägt trotzdem `quelle`. Die Parameterliste im Produkt zeigt damit eine Setzung als Quellenwert. Die VOLY mit gleicher Bauart (Quellwert plus Übertragungsannahme von KAP3) steht dagegen auf `abschaetzung_kap3`. Dieselbe Frage stellt sich bei den bandmittigen Stützstellen e(60)/e(70)/e(80) in L̄_a (§3.5 #l-a). | c_fall auf `abschaetzung_kap3` setzen, die Herleitung #c-fall besteht. Für l_restlebenserwartung dieselbe Regel anwenden: entweder `abschaetzung_kap3` oder in Log 40 begründen, warum eine Stützstellenwahl keine Setzung ist. | B | `python3 -c "import sys; s=open('docs/methodik/95_hitzebelastung.md',encoding='utf-8').read(); k=s[s.index('## 7 '):s.index('## 8 ')].split('parameter:'); f=[x for x in k if 'id: heat.c_fall' in x][0]; l=[x for x in k if 'id: heat.l_restlebenserwartung' in x][0]; z=[x for x in s.splitlines() if x.startswith('\| 40 ')][0]; sys.exit(not ('kennzeichnung: abschaetzung_kap3' in f and ('kennzeichnung: abschaetzung_kap3' in l or 'Stützstelle' in z)))"` | behoben (T-1119 Nacharbeit 1): c_fall und l_restlebenserwartung auf `abschaetzung_kap3` (Proxy aus dem Durchschnitt aller KH-Fälle; Stützstellen e(60)/e(70)/e(80) für u65–84, 85+ exakt); Log 40 nennt beide Fälle, „Indexierung“ ist aus der `quelle`-Lesart gestrichen; Kapitel 7 jetzt 8 × quelle, 8 × abschaetzung_kap3, 3 × berechnet |
| 113 | Statuskopf, Z. 3–7 | Widerspruch | Der Kopf meldet „Rev. 8 … ABNAHMEREIF & INTEGRIERT (Review Runden 6–9 …)“. Das Ledger führt inzwischen die Runden 10–13 der Fortschreibung 7, und der Bericht ist in Revision. | Statuskopf auf den Stand der Fortschreibung 7 setzen, ohne Abnahmebehauptung | C | `python3 -c "import sys; s=open('docs/methodik/95_hitzebelastung.md',encoding='utf-8').read(); sys.exit(not ('ABNAHMEREIF & INTEGRIERT' not in s[:1500]))"` | behoben (T-1119 Nacharbeit 1): Statuszeile „Rev. 8, Fortschreibung 7 in Revision — nicht abnahmereif“, Abnahme durch den methodik_manager steht aus; Rev. 8 als Ausgangsstand mit Datum 30.08.2026 |
| 114 | Kap. 8, Quelle [68] | Lücke | Die URL zeigt auf die allgemeine Publikationsseite des UBA, nicht auf Teilbericht 6. Der Wayback-Snapshot über sources.py würde nur diese Übersichtsseite sichern. | URL der Publikationsseite von Climate Change 25/2021 eintragen | C | `python3 -c "import sys; s=open('docs/methodik/95_hitzebelastung.md',encoding='utf-8').read(); t=s[s.index('- **[68]**'):s.index('## Entscheidungslog')]; sys.exit('(http://www.umweltbundesamt.de/publikationen;' in t)"` | behoben (T-1119 Nacharbeit 1): Publikationsseite https://www.umweltbundesamt.de/publikationen/KWRA-Teil-6-Integrierte-Auswertung und PDF-Adresse (Dateiname gleich der Repo-Datei), abgerufen 25.09.2026 |

## Runde 15 — Gegenprüfung nach Fortschreibung 7 (frische Sitzung, 25.09.2026): Null-Runde

Nachweis: Firmen-Repo, `tickets/T-1119-methodik_manager.md`, Abschnitt „Urteil“, Eintrag „2026-09-25T15:49:38Z ·
Runde 1 · methodik_manager (opus/xhigh)“: Urteil **freigabe**, Verdikt `freigabe | runde=1 | lints=gruen |
ledger=gruen | golden=12/12 | lf=14/14 | neu_A=0 neu_B=0 neu_C=0 | null_runde=ja`. Die Gegenprüfung nach §5 in
frischer Sitzung hat die Nacharbeit aus Runde 14 (Befunde 112–114) geprüft und keinen neuen Befund der Kategorie A, B
oder C gefunden; „Runde 1“ ist die Zählung im Ticket, im Ledger ist es die Runde nach Runde 14. Merge des Schritts nach
`main`: Commit 31673734. Neue Befunde: keine. Zurückgestellt bleiben 99, 100, 101 und 104; keiner davon ist ein
A-Befund. Eingetragen mit T-1120-methodik_manager (Schritt 3), ohne Änderung am Bericht.

## Runde 16 — Zellvergleich Berlin als Skript (T-1198, 25.09.2026): neuer Befund 115

Anlass: T-1198-methodik_manager (Vorhaben T-1196-cmo). Die Messung „Zellvergleich Berlin, Fassung 2“ aus Runde 12 lag
nur im Probeverzeichnis. Sie liegt jetzt als Skript `docs/methodik/anlagen/95_zellvergleich.py` im Repo, Aufruf:
`python3 docs/methodik/anlagen/95_zellvergleich.py --gemeinde 11000000`. Das Skript braucht nur die
Python-Standardbibliothek. Die Daten lädt es in einen Cache außerhalb des Repos (Vorgabe `~/.cache/kap3/95_zellvergleich`,
Option `--cache`); eingecheckt ist davon nichts. Grundlagen: Zensus-Gitter 100 m [67] mit Download-Adressen und
Einlese-Logik aus `backend/app/services/zensus_loader.py` (importiert, `load_dataset_bbox` und
`apply_zensus_to_cell_inputs` unverändert aufgerufen), DWD-Raster [33] wie `dwd_cdc_grid.climatology_grid`, 2016–2025,
Gemeindegebiet BKG VG250 [65] (`vg250_gem`, AGS, GF = 4), Parameter aus Kapitel 7, Wochenquantile aus der Tabelle §3.2,
Reihe `sommermittel_bundesland_povw.csv` [50]. Mit `--gemeinde <AGS>` rechnet es jede Kommune; ohne Ebene 1 für eine
Kommune, die kein Stadtstaat ist, setzt es Gitter-Summe × Altersstruktur des Landes an (Option `--einwohner`), den Punkt
der Kette über `--punkt`. Probelauf Treuenbrietzen (12069632): 558 Zellen, läuft durch.

**Ergebnis Berlin (Lauf 25.09.2026):** VG250-Fläche 893,0 km², 40.669 bewohnte Zellen, 3.593.357 Einwohner; Punkt
Berlin-Mitte 20,07 °C und 17,5 Hitzetage; Bevölkerungsmittel 19,96 °C (19,38–20,38 °C), 24,8 % der Einwohner wärmer
als der Punkt. Kette 362,89 Mio. € → (a) Temperatur je Zelle 344,00 (× 0,948) → (b) Einwohnersumme 337,52 (× 0,981) →
(c) Bänder je Zelle wie im Produkt 331,30 (× 0,982) → (d) Feinstruktur σ = 0,5 K 338,10 (× 1,021, genau 1,02051);
zusammen × 0,932; (a) und (d) zusammen × 0,967. Bänder nach Produktlogik 2.898.960 · 334.709 · 262.921 · 96.767, gegen
Ebene 1 × 0,979 · 0,986 · 1,037 · 0,897. Eigenheit (Befund 104): 4774 Zellen mit 99.098 Einwohnern ohne Anteil 65+;
Ersatz mit dem Anteil der übrigen Zellen (19,87 %) 338,00, Produkt gegen Ersatz × 0,9802, Rest × 1,0014; Zelllauf ohne
Eigenheit 344,94 Mio. €. Reihe Berlin 2016–2025 im Mittel 20,06 °C. Gegenprobe mit
`--wochenquantile produkt` (Anlage `wochenquantile_region.csv` wie das Produkt): Kette 362,80 Mio. €, alle Faktoren
gleich bis zur dritten Stelle. Die Zahlen in den Nachträgen zu 99 und 104 aus Runde 12 (3.595.270 Einwohner, Bänder
× 0,980 · 0,986 · 1,038 · 0,897, 4770 Zellen mit 99.026 Einwohnern) sind damit durch diese Messung ersetzt; beide
bleiben zurückgestellt.

| Nr | Stelle | Art | Begründung | Vorschlag | Kat. | Prüfausdruck | Status |
|---|---|---|---|---|---|---|---|
| 105 | §3.0, Liste der Zusammenfassungen | Nachtrag Runde 16 | Zahlenfolge berichtigt (Befund 115); der Prüfausdruck aus Runde 12 prüfte die alte Folge | — | B | `grep -q '0,948 × 0,981 × 0,982 × 1,021 = 0,932' docs/methodik/95_hitzebelastung.md` | behoben (T-1198): Wirkungen (b) und (c) weiter ausgewiesen, Werte aus dem Skript; Zelllauf rund 338 Mio. €, ohne Eigenheit rund 345 Mio. € (Preisstand 2024) |
| 115 | §3.0, Wirkungen (b)–(d) und Beispiel-Block rechenkette_95 | Abweichung Messung Runde 12 ↔ Skript | Das Skript reproduziert (a) × 0,948 und zusammen × 0,932, weicht aber in der dritten Stelle ab: (b) × 0,981 statt 0,982, (c) × 0,982 statt 0,981, (d) × 1,021 statt 1,020. Ursache 1, Gemeindegrenze: Runde 11/12 nahm die Grenze aus OpenStreetMap/Nominatim (891,1 km², 40.663 Zellen, 3.595.270 Einwohner), das Skript die amtliche VG250 (893,0 km², 40.669 Zellen, 3.593.357 Einwohner). Das verschiebt (b) von 0,98168 auf 0,98115 und (c) von 0,98140 auf 0,98158 (andere Randzellen). Ursache 2, Rundung: (d) war schon in Runde 12 × 1,0205 (338,22/331,42 = 1,02052) und hätte als 1,021 stehen müssen, nicht als 1,020. Kette (362,89 Mio. €), Temperaturen und die Aussagen in §3.0 (rund 7 % Überschätzung, rund 338 bzw. 345 Mio. €, × 0,967 für Befund 101) bleiben gleich; kein Wert aus Kapitel 7 betroffen | Werte des Skripts in §3.0 und in den Block übernehmen, Pfad und Aufruf nennen | C | `python3 -c "import sys; s=open('docs/methodik/95_hitzebelastung.md',encoding='utf-8').read(); t=s[s.index('### 3.0'):s.index('### 3.1')]; sys.exit(not ('Einwohnersumme: × 0,981' in t and 'Produkt: × 0,982' in t and 'unter 1 km: × 1,021' in t and '3_593_357' in t and '3.595.270' not in t and 'python3 docs/methodik/anlagen/95_zellvergleich.py --gemeinde 11000000' in t))"` | behoben (T-1198): §3.0 (b) 3.593.357 Einwohner × 0,981, (c) × 0,982 = × 0,9802 Eigenheit (4774 Zellen, 99.098 Einwohner) × 1,0014 Rest, (d) × 1,021; Grenze VG250 [65] genannt; Skript und Aufruf in §3.0, [67] um den Datensatz Anteil 65+ ergänzt; Block rechenkette_95 nachgezogen |

## Runde 17 — Ersatzregel für den geheimgehaltenen Anteil 65+ (T-1199, 25.09.2026): Befund 104 behoben, neue Befunde 116–117

Anlass: T-1199-methodik_manager (Vorhaben T-1196-cmo). Der methodik_manager hat die Regel vorgegeben: Stufe 1 Summe der
veröffentlichten 5er-Jahresgruppen ab 65 der Zelle geteilt durch ihre Einwohner, Stufe 2 der einwohnergewichtete Anteil 65+
aller Zellen derselben Gemeinde mit veröffentlichtem Anteil. Sie steht jetzt als ein Satz in §3.3, gekennzeichnet als
Abschätzung von KAP3, mit Entscheidungslog Nr. 41; §3.0 (c) verweist darauf, Kapitel 7 ist unverändert, kein neuer
Parameter-Block. `backend/app/services/zensus_loader.py` ist nicht geändert; der Nachzug gehört dem cto (Befund 116).

**Lesart von Stufe 1.** „Veröffentlicht“ heißt: mindestens eine der sechs Gruppen a65bis69 … a90undaelter trägt eine Zahl
(das Gitter veröffentlicht erst ab 3 Personen; „–“ liest der Loader als 0 und zählt als 0). Die strenge Lesart „alle
sechs Gruppen“ ließe Stufe 1 leer: Probelauf über das ganze Gitter [67] (Datei `Zensus2022_Anteil_ueber_65_100m-Gitter.csv`,
Spalte AnteilUeber65 = „–“, verknüpft über GITTER_ID mit dem Altersgitter): 1.099.879 Zellen mit geheimgehaltenem Anteil
65+, davon 1.020.763 ohne veröffentlichte Gruppe ab 65, 79.116 mit einer bis vier, keine mit fünf oder sechs. Im selben
Probelauf haben 107 Zellen der Stufe 1 mehr veröffentlichte Personen ab 65 als Einwohner (Anteil über 100 %; in Berlin 1,
in Warmsen 0). Eine Kappung legt die Regel nicht fest; das Skript kappt nicht und weist die Zahl aus. Im Gitter kommt
„0“ als Anteil 65+ nicht vor (kleinster veröffentlichter Wert 0,34 %); „–“ und „fehlt“ sind damit dasselbe.

**Messung (Skript `docs/methodik/anlagen/95_zellvergleich.py`, neue Optionen `--ersatz` und `--rangliste`, Lauf 25.09.2026,
Cache außerhalb des Repos).** Beide Jahresbeträge sind der Zelllauf mit den Wirkungen (a)–(d) aus §3.0; der Betrag
„heute“ ist der Zelllauf aus §3.0 (Berlin 338,10 Mio. €).

- `python3 docs/methodik/anlagen/95_zellvergleich.py --gemeinde 11000000 --ersatz`: 3.593.357 Einwohner im Zensus-Gitter,
  davon 99.098 (2,8 %) in 4774 Zellen mit geheimgehaltenem Anteil 65+; Stufe 1 670 Zellen mit 24.269 Einwohnern (Anteil 65+
  im Mittel 9,28 %), Stufe 2 4104 Zellen mit 74.829 Einwohnern (19,87 %), ohne Ersatzwert 0; Altersgitter dieser Zellen
  85.046 Personen, davon 2252 ab 65 (2,6 %); Einwohner ab 65 heute 694.397 (19,3 %), mit Regel 711.519 (19,8 %);
  Jahresbetrag heute 338,10 Mio. €, mit Regel 344,17 Mio. € (Preisstand 2024), Faktor × 0,982. Nur Stufe 2 (Variante
  Runde 12): 344,94 Mio. €. Ohne `--ersatz` sind die Zahlen gleich wie in Runde 16; geändert ist nur die
  Schreibweise ganzer Zahlen unter 10.000 (ohne Tausenderpunkt, kap3-stil).
- `python3 docs/methodik/anlagen/95_zellvergleich.py --gemeinde 03256034 --ersatz` (Warmsen, Landkreis Nienburg (Weser),
  Niedersachsen, ERF-Region Nord): 3087 Einwohner im Zensus-Gitter (amtlich 3158 [69]), davon 1983 (64,2 %) in 374 Zellen
  mit geheimgehaltenem Anteil 65+; Stufe 1 12 Zellen mit 86 Einwohnern (41,86 %), Stufe 2 362 Zellen mit 1897 Einwohnern
  (46,00 %), ohne Ersatzwert 0; Altersgitter dieser Zellen 692 Personen, davon 36 ab 65 (5,2 %); Einwohner ab 65 heute 508
  (16,4 %), mit Regel 1416 (45,9 %); Jahresbetrag heute 138.543 €, mit Regel 305.088 € (Preisstand 2024), Faktor × 0,454.
  Nur Stufe 2: 304.669 €.
- `python3 docs/methodik/anlagen/95_zellvergleich.py --rangliste`: 10.828 Gemeinden mit Einwohnern im Gitter; Anteil der
  Einwohner in Zellen mit geheimgehaltenem Anteil 65+ bundesweit 12,5 %, in den 9239 Gemeinden unter 10.000 Einwohnern
  zusammen 23,6 %, Median je Gemeinde 27,9 %; 30 Gemeinden mit zusammen 376 Einwohnern haben keine Zelle mit veröffentlichtem
  Anteil (Modellgrenze der Regel). Höchster Anteil unter den Gemeinden mit 2000 bis unter 10.000 Einwohnern: Warmsen
  (64,2 %), dann Kollnburg (63,3 %) und Laar (63,1 %). Deshalb ist Warmsen die ländliche Beispielkommune.
- Gegenprobe amtlich [69] (Regionaltabelle Demografie des Zensus 2022, neu in Kapitel 8): Warmsen 60–66 · 67–74 · 75+ =
  388 · 257 · 345, also 602 ab 67 und 990 ab 60; Berlin 292.354 · 261.676 · 362.829, also 624.505 ab 67 und 916.859 ab 60.

**Befund aus der Messung (117).** Die Regel setzt in Warmsen mehr Menschen ab 65 an (1416), als dort Menschen ab 60 leben
(990). Die Prämisse der Regel („–“ ist Geheimhaltung, dieselben Zellen haben Ältere wie anderswo) trägt nur für einen kleinen
Teil der Zellen: Das Altersgitter der geheimgehaltenen Zellen zeigt 2,6 % (Berlin) und 5,2 % (Warmsen) Personen ab 65,
bundesweit im Probelauf 3,1 % in den geheimgehaltenen Zellen ab 20 Einwohnern (107.452 Zellen, 3.588.180 Einwohner, 97,7 %
davon im Altersgitter erfasst). Stufe 2 überträgt dagegen den Anteil der Zellen mit veröffentlichtem Anteil; in Zellen unter
20 Einwohnern ist er nach demselben Probelauf einwohnergewichtet 39,3 %, weil dort vor allem Zellen mit Älteren einen Anteil tragen. Die heutige
Produktlogik (65+ = 0) liegt in Warmsen unter den 602 ab 67 und unterschätzt ebenfalls, aber um weniger (508 gegen 1416).
Die 1312 veröffentlichten Seniorenfelder aus Befund 104 stimmen, betreffen aber in Berlin 670 von 4774 Zellen. Der Bericht
führt die Regel wie vorgegeben und nennt die Verfälschung an derselben Stelle (§3.3, „Was die Regel verfälscht“); still
korrigiert ist nichts.

| Nr | Stelle | Art | Begründung | Vorschlag | Kat. | Prüfausdruck | Status |
|---|---|---|---|---|---|---|---|
| 104 | §3.3 (Regelsatz) ↔ Produkt `zensus_loader.apply_zensus_to_cell_inputs` | Divergenz Bericht ↔ Code, Nachtrag Runde 17 | Der Bericht legt die Ersatzregel jetzt in §3.3 fest (Log 41). Die Messungen aus Runde 12 und 16 (4774 Zellen, 99.098 Einwohner, × 0,9802 gegen Stufe 2 allein) bleiben; die Wirkung der Regel ist für Berlin und Warmsen gemessen (× 0,982, × 0,454). Der Code-Teil steht als Befund 116 | — | B | `python3 -c "import sys; s=open('docs/methodik/95_hitzebelastung.md',encoding='utf-8').read(); t=s[s.index('### 3.3'):s.index('### 3.4')]; sys.exit(not ('**Regel (Abschätzung von KAP3, festgelegt vom methodik_manager):** Ist der Anteil 65+ einer' in t and 'ersetzt das Produkt ihn in Stufe 1 durch die Summe' in t and 'sonst in Stufe 2 durch den einwohnergewichteten Anteil 65+' in t and 'Hat eine Gemeinde keine Zelle mit veröffentlichtem Anteil 65+' in t))"` | behoben (T-1199): Berichtsteil; Regelsatz in §3.3 mit Kennzeichnung als Abschätzung von KAP3, Modellgrenze mit gemessener Häufigkeit, Wirkung Berlin und Warmsen mit Aufruf; Entscheidungslog Nr. 41; §3.0 (c) verweist auf §3.3 |
| 116 | Produkt: `zensus_loader.apply_zensus_to_cell_inputs` (share_o = … or 0.0) ↔ Bericht §3.3 (Ersatzregel) | Code-Nachzug (Eiserne Regel 5) | Das Produkt setzt bei geheimgehaltenem Anteil 65+ weiter 65+ = 0; der Bericht legt seit Runde 17 eine Ersatzregel fest. Nachzug erst nach der Entscheidung zu Befund 117, sonst wird eine Regel eingebaut, die ländliche Kommunen verdoppelt | Code-Nachzug beim cto nach Log 41 in der dann geltenden Fassung; Test mit Berlin und Warmsen aus §3.3 | B | `! grep -q 'share_o = ci.get("share_over_65") or 0.0' backend/app/services/zensus_loader.py` | zurückgestellt (Code-Nachzug cto; wartet auf die Entscheidung zu Befund 117) |
| 117 | §3.3, Ersatzregel Stufe 2 (Log 41) | Widerspruch Messung ↔ Regel (P3: Ergebnis stellt die Lage falsch dar) | Warmsen mit Regel 1416 Einwohner ab 65 (45,9 %) gegen 990 ab 60 und 602 ab 67 im Zensus 2022 [69]; Betrag × 2,20 gegenüber heute. Das Altersgitter der geheimgehaltenen Zellen zeigt 2,6 % (Berlin) bzw. 5,2 % (Warmsen) Personen ab 65; Stufe 2 überträgt den Anteil der Zellen mit veröffentlichtem Anteil (Warmsen 46,00 %), die in ländlichen Kommunen vor allem Zellen mit Älteren sind. In Berlin liegen heute (694.397) und Regel (711.519) beide zwischen 624.505 ab 67 und 916.859 ab 60 | Entscheidung methodik_manager: Stufe 2 ersetzen, etwa durch den Rest aus der Gemeindesumme des Zensus (Menschen ab 65 der Gemeinde [69] abzüglich der Zellen mit veröffentlichtem Anteil und der Stufe 1, verteilt auf die übrigen geheimgehaltenen Zellen), oder 65+ = 0 mit Stufe 1 lassen; Messung mit `--ersatz` für Berlin und Warmsen wiederholen | A | `! grep -q 'sonst in Stufe 2 durch den einwohnergewichteten Anteil 65+' docs/methodik/95_hitzebelastung.md` | zurückgestellt (Entscheidung methodik_manager; die Regel ist dessen Vorgabe aus T-1199 und steht wie vorgegeben im Bericht) |

## Runde 18 — Berlin-Anker, YLL/VOLY, VOLY-Infokasten (T-1200, 25.09.2026): Befund 101 behoben

Anlass: T-1200-methodik_manager (Vorhaben T-1196-cmo, Paket 3). Grundlage für 101 ist die Messung aus Runde 16 (Skript
`docs/methodik/anlagen/95_zellvergleich.py --gemeinde 11000000`): (a) Temperatur je Zelle × 0,948, (d) Feinstruktur
σ = 0,5 K × 1,021 (genau 1,02051), zusammen × 0,967 (0,948 × 1,02051 = 0,9674). Das bestätigt den Nachtrag aus Runde 12;
ein berichtigter Wert liegt nicht vor. Anker: 221 × 0,9674 = 213,8, rund 214 je 100.000; gegen die Untergrenze 260 der
RKI-Referenz 213,8 / 260 − 1 = −17,8 %, rund −18 % (bisher 221 / 260 − 1 = −15 %). Kein Wert aus Kapitel 7 geändert;
§3.0 verweist jetzt auf die neue Fassung in §4 statt auf einen Widerspruch. Ohne neuen Befund umgesetzt, weil vom Ticket
verlangt: YLL und VOLY in Kapitel 1, Konto-Einbettung, bei der ersten Verwendung erklärt; Infokasten 2 (§6) sagt in einem
Satz, dass die 160.800 € vom Wert der UBA-Methodenkonvention 4.0 für den EU-Durchschnitt ausgehen und die Übertragung auf
deutsche Einkommen eine Abschätzung von KAP3 ist (Elastizität 0,85, Log 4; Spanne 136.400–165.600 € wie §3.5), passend zur
Kennzeichnung `abschaetzung_kap3` des Blocks heat.voly. Die Zahl 4770 kommt im Bericht schon seit T-1198 nicht mehr vor
(dort 4774, aus dem Skript).

| Nr | Stelle | Art | Begründung | Vorschlag | Kat. | Prüfausdruck | Status |
|---|---|---|---|---|---|---|---|
| 101 | §4 Zusatz-Anker Berlin 2018 | Widerspruch Messung ↔ Begründung, Nachtrag Runde 18 | Begründung „das Zellmodell wird für Berlin … über dem Gemeindepunkt-Wert liegen“ war durch die Messung widerlegt (Runden 11, 12, 16) | wie Runde 11 | B | `! grep -q 'das Zellmodell wird für Berlin' docs/methodik/95_hitzebelastung.md` | behoben (T-1200): §4 neu gefasst — Richtung gemessen (Gemeindepunkt 20,06 °C, 0,1 K über dem Bevölkerungsmittel 19,96 °C; (a) × 0,948 und (d) × 1,021, zusammen × 0,967), Anker 221 × 0,967 ≈ 214 je 100.000, rund −18 % gegen 260; Lücke offen als unerklärt benannt; „konservativ = unterschätzend“ bleibt; Kapitel 7 unverändert |

## Runde 19 — Entscheidung methodik_manager zu den Befunden 117, 99 und 100 (T-1233, 25.09.2026): 117, 100 behoben, 99 entschieden

Anlass: T-1233-methodik_manager (Vorhaben T-1197-cmo). Der methodik_manager hat entschieden: Stufe 1 der Ersatzregel bleibt,
Stufe 2 wird der Rest aus der Gemeindesumme des Zensus 2022 [69] (Befund 117); Ebene 1 bleibt die Fortschreibung zum
Stichtag 31.12.2023 (Befund 99); Quelle [66] ohne falschen Repo-Pfad (Befund 100). Umgesetzt in §3.3 (Regel in vier
Schritten, Rechenbeispiel Warmsen mit Test `beispiel_95_ersatz_stufe2_warmsen`, Modellgrenzen gemessen, Tabelle mit
Einwohnern ab 65 und Spanne), Entscheidungslog Nr. 41, Quellen [66] und [69]. Kapitel 7 ist unverändert, kein neuer
Parameter-Block; die Faktoren (a)–(d) in §3.0 und der Jahresbetrag der Kette (362,89 Mio. €) bleiben.
`backend/app/services/zensus_loader.py` ist nicht geändert. Befund 104 bekommt einen Nachtrag: Sein Prüfausdruck aus
Runde 17 verlangte den Satz der früheren Stufe 2 und widerspricht damit dem Ausdruck von 117; er prüft jetzt die neue Fassung.

**Messung (Skript `docs/methodik/anlagen/95_zellvergleich.py`, Stufe 2 neu, liest [69] aus dem Blatt „CSV-Demografie“,
Lauf 25.09.2026, Cache außerhalb des Repos).**

- `--gemeinde 03256034 --ersatz` (Warmsen): A_G = (602 + 2/7 × 388) / 3158 = 22,57 %; Z = 22,57 % × 3087 = 697; fest 508
  (Zellen mit veröffentlichtem Anteil) + 36 (Stufe 1); R = 153; Anteil je Zelle der Stufe 2 153 / 1897 = 8,07 %. Einwohner
  ab 65 heute 508, mit Regel 697 (zwischen 602 ab 67 und 990 ab 60 [69]); Jahresbetrag heute 138.543 €, mit Regel
  173.099 € (Preisstand 2024), Faktor × 0,800; 60–66 gar nicht (0/7) × 0,904, ganz (7/7) × 0,622.
- `--gemeinde 11000000 --ersatz` (Berlin): A_G = 19,68 %; Z = 707.318; fest 694.397 + 2252; R = 10.669; Anteil 14,26 %.
  Einwohner ab 65 heute 694.397, mit Regel 707.318; Jahresbetrag heute 338,10 Mio. €, mit Regel 342,67 Mio. €, Faktor
  × 0,987; 0/7 × 0,998, 7/7 × 0,925. Kette unverändert 362,89 Mio. €.
- `--rangliste`: 10.811 Gemeinden mit Zellen der Stufe 2 (8.739.209 Einwohner in diesen Zellen); R < 0 in 1323 Gemeinden
  mit 320.504 Einwohnern in Zellen der Stufe 2 (3,7 %), Überhang im Median 5, höchstens 195 Einwohner ab 65; Anteil auf
  100 % begrenzt in 3 Gemeinden (19 Einwohner); keine Zeile in [69] oder „.“ in 69 Gemeinden (9133 Einwohner, 0,1 %). Die
  30 Gemeinden mit 376 Einwohnern ohne Zelle mit veröffentlichtem Anteil bekommen jetzt einen Wert; die frühere
  Modellgrenze entfällt.

| Nr | Stelle | Art | Begründung | Vorschlag | Kat. | Prüfausdruck | Status |
|---|---|---|---|---|---|---|---|
| 117 | §3.3, Ersatzregel Stufe 2 (Log 41) | Widerspruch Messung ↔ Regel, Nachtrag Runde 19 | Entscheidung methodik_manager (T-1233): Stufe 2 wird der Rest aus der Gemeindesumme [69] | wie Runde 17 | A | `! grep -q 'sonst in Stufe 2 durch den einwohnergewichteten Anteil 65+' docs/methodik/95_hitzebelastung.md` | behoben (T-1233): §3.3 legt Stufe 2 als Rest aus der Gemeindesumme fest (A_G mit 2/7 der Gruppe 60–66 als Abschätzung von KAP3, Z, R, Anteil begrenzt auf 0–100 %); Warmsen 697 statt 1416 Einwohner ab 65 (zwischen 602 ab 67 und 990 ab 60), Faktor × 0,800; Berlin × 0,987; Spanne 0/7–7/7 mit Aufruf; Modellgrenze R < 0 gemessen (1323 Gemeinden, 3,7 %); Log 41 neu mit Gegenargumenten Aufteilung 60–66 und Stichtag; Prüfausdruck unverändert |
| 99 | §3.0 Rechenkette, Ebene 1 | Abweichung vom Ticket (Datenstand), Nachtrag Runde 19 | Entscheidung methodik_manager (T-1233): Ebene 1 bleibt die Fortschreibung zum Stichtag 31.12.2023, Basis Zensus 2022; derselbe Stichtag gilt für den Nenner von m_a [49], der Unterschied zum Gitter steht als Wirkung (b) in §3.0; nach dem 05.10.2026 wird nicht umgestellt | — | C | `grep -q 'Stichtag 31.12.2023, Basis Zensus 2022' docs/methodik/95_hitzebelastung.md` | entschieden (methodik_manager) → geschlossen: Ebene 1 bleibt; §3.3 nennt den Stichtag der Ersatzregel (15.05.2022) neben Ebene 1 (31.12.2023); Prüfausdruck unverändert |
| 100 | §8 Quelle [66] | falscher Pfad, Nachtrag Runde 19 | [66] nannte den Repo-Pfad backend/data/lite/zensus_gemeinde.json, die Datei ist eine erzeugte Aufbereitung und liegt nicht im Repo | [66] nennt das erzeugende Modul und den sha256-Pin in §4 | C | `! grep -q 'backend/data/lite/zensus_gemeinde.json' docs/methodik/95_hitzebelastung.md && grep -q 'backend/app/services/lite/zensus_gemeinde.py' docs/methodik/95_hitzebelastung.md && test -f backend/app/services/lite/zensus_gemeinde.py` | behoben (T-1233): [66] nennt das Modul `backend/app/services/lite/zensus_gemeinde.py` (im Repo), sagt, dass die Aufbereitung `zensus_gemeinde.json` nicht im Repo liegt, verweist für den sha256-Pin `124fd7a7a15b` auf §4 (`#t-povw`) und nennt [69] als amtliche Gegenprobe; neuer Prüfausdruck auf den Bericht statt `test -f` auf die fehlende Datei |
| 104 | §3.3 (Regelsatz) ↔ Produkt `zensus_loader.apply_zensus_to_cell_inputs` | Divergenz Bericht ↔ Code, Nachtrag Runde 19 | Der Prüfausdruck aus Runde 17 verlangte den Satz der früheren Stufe 2 („sonst in Stufe 2 durch den einwohnergewichteten Anteil 65+“), den T-1233 mit Befund 117 entfernt; er wäre damit rot, obwohl der Berichtsteil von 104 weiter erfüllt ist. Der Ausdruck prüft jetzt die Regel in der Fassung T-1233 | — | B | `python3 -c "import sys; s=open('docs/methodik/95_hitzebelastung.md',encoding='utf-8').read(); t=s[s.index('### 3.3'):s.index('### 3.4')]; sys.exit(not ('**Regel (Abschätzung von KAP3, festgelegt vom methodik_manager):** Ist der Anteil 65+ einer' in t and '*Stufe 1:* Ist in der Zelle mindestens eine der sechs 5er-Jahresgruppen ab 65' in t and '*Stufe 2:* Die übrigen geheimgehaltenen Zellen bekommen den Rest aus der Gemeindesumme' in t and 'ist eine Abschätzung von KAP3' in t))"` | behoben (T-1233): Berichtsteil unverändert erfüllt — Regel in §3.3 mit Stufe 1 und Stufe 2 (neu), gekennzeichnet als Abschätzung von KAP3; Prüfausdruck auf die neue Fassung umgestellt, weil der Ausdruck aus Runde 17 dem von Befund 117 widerspricht; Code-Teil weiter Befund 116 |
| 116 | Produkt: `zensus_loader.apply_zensus_to_cell_inputs` (share_o = … or 0.0) ↔ Bericht §3.3 (Ersatzregel) | Code-Nachzug (Eiserne Regel 5), Nachtrag Runde 19 | Die Entscheidung zu Befund 117 liegt vor; das Produkt setzt weiter 65+ = 0 | Code-Nachzug beim cto nach Log 41 in der Fassung T-1233: Stufe 1 wie bisher, Stufe 2 Rest aus der Gemeindesumme [69] (A_G mit 2/7 der Gruppe 60–66, Z = A_G × Einwohnersumme im Gitter, R, Anteil begrenzt auf 0–100 %, R < 0 gibt 0), [69] je Gemeinde als Datenquelle; Test mit Berlin (707.318 Einwohner ab 65, 342,67 Mio. €) und Warmsen (697, 173.099 €) aus §3.3 | B | `! grep -q 'share_o = ci.get("share_over_65") or 0.0' backend/app/services/zensus_loader.py` | zurückgestellt (Code-Nachzug cto): Vorschlag auf Log 41 in der Fassung T-1233 fortgeschrieben; Code-Prüfausdruck unverändert |

## Runde 20 — Nacharbeit 1 zu T-1233 nach Urteil methodik_manager Runde 0 (25.09.2026): neue Befunde 118–119, behoben

Anlass: Urteil des methodik_manager zu T-1233 (Runde 0, 25.09.2026): Abnahmekriterium erfüllt, aber zwei neue Befunde der
Kategorie C aus der Gegenprüfung der geänderten Stellen (N1 → 118, N2 → 119), dazu vier Hinweise. Umgesetzt:

- 118: Quelle [66] nennt die Näherung des Moduls `backend/app/services/lite/zensus_gemeinde.py`: 100-m-Zellen werden zu
  1-km-Zellen zusammengefasst (Z. 31–72), jede 1-km-Zelle geht ganz an die Gemeinde, in der ihr Mittelpunkt liegt
  (Z. 106–125). [66] verweist auf die 96 VG250-Gemeinden ohne Zensus-Eintrag in §4 und nennt [69] als Gegenprobe nur mit
  diesem Vorbehalt.
- 119: Entscheidung methodik_manager: Fehlt die Gemeindezeile in [69] oder steht dort „.“, gilt A_G der Kreiszeile (erste
  fünf Stellen des AGS). Umgesetzt in §3.3 (Schritt 1 und Modellgrenzen), Log 41 (Regel und Gegenargument 4) und im Skript
  (`zensus_demografie` liest jetzt auch die Kreiszeilen, neue Funktion `demografie_fuer`, `--rangliste` zählt Kreiszeile
  und Rest ohne jede Zeile getrennt).
- Hinweise: (a) Kopf des Entscheidungslogs nennt für Eintrag 41 jetzt auch T-1233 und die Befunde 99, 117 und 119;
  (b) 305.088 € in §3.3 mit Fundort (Befund-Ledger Runde 17, T-1199), Zeilenumbruch gerichtet; (c) `--rangliste` gibt
  den Überhang als positiven Betrag aus; (d) Export folgt nach der Null-Runde, hier nicht erzeugt.

**Messung (Lauf 25.09.2026, Cache außerhalb des Repos).** `python3 docs/methodik/anlagen/95_zellvergleich.py --rangliste`:
R < 0 in 1342 von 10.811 Gemeinden mit Zellen der Stufe 2, darin 320.780 der 8.739.209 Einwohner solcher Zellen (3,7 %);
Überhang Median 5, größter 195 Einwohner ab 65; auf 100 % begrenzt 3 Gemeinden (19 Einwohner); A_G aus der Kreiszeile
68 Gemeinden (5240 Einwohner in Zellen der Stufe 2, 0,1 %); weder Gemeinde- noch Kreiszeile 1 Gemeinde (3893 Einwohner):
Hanau, in VG250 06415000, in [69] noch 06435014 im Main-Kinzig-Kreis (Abfrage über `zensus_demografie` und
`demografie_fuer` gegen `vg250_gem`, GF = 4). Die 69 Gemeinden ohne Gemeindezeile aus Runde 19 (9133 Einwohner) teilen
sich damit in 68 mit Kreiszeile (5240) und Hanau (3893). R < 0 steigt von 1323 auf 1342 Gemeinden, weil Gemeinden mit
Kreiszeile jetzt ein R haben. Berlin und Warmsen haben eine Gemeindezeile; beide `--ersatz`-Aufrufe geben dieselben Werte
wie in Runde 19 aus (Berlin 707.318, 342,67 Mio. €, × 0,987, × 0,925–0,998; Warmsen 697, 173.099 €, × 0,800,
× 0,622–0,904), die Tabelle in §3.3 bleibt.

| Nr | Stelle | Art | Begründung | Vorschlag | Kat. | Prüfausdruck | Status |
|---|---|---|---|---|---|---|---|
| 118 | §8 Quelle [66] | verschwiegene Näherung | „aufsummiert aus den Gitterdaten 100 m [67] auf die Gemeinden aus VG250 [65]“ verschwieg, dass das Modul auf 1-km-Zellen faltet und über den Mittelpunkt zuordnet (Ursache der 96 Gemeinden ohne Zensus-Eintrag in §4); [69] stand ohne Vorbehalt als Gegenprobe da | [66] nennt 1-km-Faltung und Zuordnung über den Mittelpunkt als Näherung, verweist auf die 96 Gemeinden in §4, Gegenprobe nur mit Vorbehalt | C | `python3 -c "import sys; s=open('docs/methodik/95_hitzebelastung.md',encoding='utf-8').read(); t=s[s.index('**[66]**'):s.index('**[67]**')]; sys.exit(not ('1-km' in t and 'Mittelpunkt' in t and '96 VG250-Gemeinden' in t and 'Vorbehalt' in t))"` | behoben (T-1233, Nacharbeit 1): [66] neu gefasst wie vorgeschlagen |
| 119 | §3.3 Modellgrenzen, Log 41 (P3) | Modellgrenze ohne Ersatz, obwohl Ersatzquelle vorhanden | 69 Gemeinden ohne Gemeindezeile in [69] oder mit „.“ rechneten in Stufe 2 weiter mit 65+ = 0 (9133 Einwohner), also mit der Logik, die der Bericht selbst als Unterschätzung ausweist; [69] führt Kreiszeilen | Entscheidung methodik_manager: ohne Gemeindezeile oder bei „.“ gilt A_G der Kreiszeile (ARS-Präfix 5 Stellen); Modellgrenze nur noch ohne Kreiszeile, neu gemessen | C | `grep -qF 'gilt A_G der Kreiszeile aus [69]' docs/methodik/95_hitzebelastung.md && grep -qF 'Kreiszeile, Befund 119' docs/methodik/95_hitzebelastung.md && grep -qF 'return demografie[ags[:5]], "Kreis"' docs/methodik/anlagen/95_zellvergleich.py` | behoben (T-1233, Nacharbeit 1): §3.3 Schritt 1 und Modellgrenzen, Log 41, Skript; 68 Gemeinden nehmen die Kreiszeile, ohne Ersatzwert bleibt nur Hanau (3893 Einwohner) |
| 116 | Produkt: `zensus_loader.apply_zensus_to_cell_inputs` (share_o = … or 0.0) ↔ Bericht §3.3 (Ersatzregel) | Code-Nachzug (Eiserne Regel 5), Nachtrag Runde 20 | Log 41 hat mit Befund 119 den Rückfall auf die Kreiszeile bekommen | Code-Nachzug beim cto nach Log 41 in der Fassung T-1233 einschließlich Nacharbeit 1: Stufe 1 wie bisher, Stufe 2 Rest aus der Gemeindesumme [69] (A_G mit 2/7 der Gruppe 60–66, ohne Gemeindezeile oder bei „.“ aus der Kreiszeile; Z = A_G × Einwohnersumme im Gitter, R, Anteil begrenzt auf 0–100 %, R < 0 gibt 0); Test mit Berlin (707.318 Einwohner ab 65, 342,67 Mio. €) und Warmsen (697, 173.099 €) aus §3.3 | B | `! grep -q 'share_o = ci.get("share_over_65") or 0.0' backend/app/services/zensus_loader.py` | zurückgestellt (Code-Nachzug cto): Vorschlag um den Rückfall auf die Kreiszeile fortgeschrieben; Code-Prüfausdruck unverändert |

## Runde 21 — Nacharbeit 2 zu T-1233 nach Urteil methodik_manager Runde 1 (25.09.2026): neuer Befund 120, behoben

Anlass: Urteil des methodik_manager zu T-1233 (Runde 1, 25.09.2026): Abnahmekriterium erfüllt, ein neuer Befund der
Kategorie C (N1 → 120): Die Entscheidung zu Befund 99 stand nur in der Prüfakte, nicht im Bericht (Gate 1). Umgesetzt:
neuer Entscheidungslog-Eintrag Nr. 42 ⚠ (Frage, Entscheidung, Begründung mit Gegenargument, Alternative Zensus-Tabelle
1000A, Auswirkung); der Absatz „Stichtag“ in §3.3 nennt den Grund in einem Satz (m_a [49] teilt Sterbefälle 2023 durch
die Bevölkerung am 31.12.2023) und die Wirkung (b) mit × 0,981; der Kopf des Entscheidungslogs nennt Eintrag 42. Der
Überstimmungsweg gilt wie für alle Einträge über den Kopf des Logs. Keine Zahl geändert, Kapitel 7 unverändert, Skript
unverändert.

| Nr | Stelle | Art | Begründung | Vorschlag | Kat. | Prüfausdruck | Status |
|---|---|---|---|---|---|---|---|
| 120 | §3.3 „Stichtag“ und §3.0 Ebene 1 ↔ Entscheidungslog | Lücke (Gate 1 der Aufgabe: Ermessensfall nicht im Bericht dokumentiert) | Die Entscheidung zu Befund 99 stand nur in der Prüfakte. Entschieden ist: Ebene 1 bleibt die Fortschreibung 31.12.2023 und wird nach dem 05.10.2026 nicht auf die Zensus-Tabelle 1000A (15.05.2022) umgestellt. Der Bericht sagte nur „bleibt (Befund 99)“, ohne Grund, Alternative und Überstimmungsweg | Neuer Log-Eintrag 42 ⚠ mit Begründung (gleicher Stichtag wie der Nenner von m_a [49]; Abstand zum Gitter als Wirkung (b), × 0,981 in Berlin), Alternative 1000A, Wirkung keine Zahl; Grund in einem Satz im Absatz „Stichtag“ in §3.3; Kopf des Logs nachziehen; Kapitel 7 unverändert | C | `python3 -c "import sys; s=open('docs/methodik/95_hitzebelastung.md',encoding='utf-8').read(); t=s[s.index('## Entscheidungslog'):]; sys.exit(not any('31.12.2023' in z and '1000A' in z and 'm_a' in z for z in t.splitlines() if z.startswith('\| 42')))"` | behoben (T-1233, Nacharbeit 2): Log-Eintrag 42 ⚠ angelegt, Absatz „Stichtag“ in §3.3 mit Grund, Kopf des Logs nachgezogen; Kapitel 7 unverändert |

## Runde 22 — Befund 121 aus dem Urteil zu T-1233 Runde 2 (T-1266, 25.09.2026): neuer Befund 121, behoben

Anlass: Urteil des methodik_manager zu T-1233 (Runde 2, 25.09.2026): Abnahmekriterium erfüllt, ein neuer Befund der
Kategorie C, eine Regression durch T-1233. T-1233 wurde nach drei Nacharbeitsrunden eskaliert; T-1266 ersetzt es. Die
Arbeit von T-1233 (Runden 19–21) ist Byte für Byte aus `origin/ticket/T-1233-methodik_manager` übernommen; Lint und
Ledger-Gate waren vor der Änderung grün (25 Befunde belegt, zurückgestellt nur 116). Runde 22 ist die siebte seit der
letzten Null-Runde (Runde 15), Zählung nach A-0046. Umgesetzt:

- Skript: Die Zeile „Eigenheit in (c)“ teilt (c) mit `--ersatz` gegen die Ersatzregel aus §3.3 auf (Stufe 1 und 2,
  ohne (d)): Produkt gegen Regel = Betrag (c) / Betrag mit Regel, Rest = Betrag mit Regel / Betrag (b). „Zelllauf ohne
  Eigenheit“ ist jetzt der Jahresbetrag mit Regel samt (d), derselbe Wert wie in der Tabelle in §3.3. Der Vergleich mit
  dem einheitlichen Anteil 65+ der übrigen Zellen ist entfernt. Ohne `--ersatz` nennt die Zeile nur Zellen und
  Einwohner, weil die Aufteilung [69] braucht.
- §3.0 (c): × 0,982 = 0,9867 × 0,9948, erster Faktor Produkt gegen Regel mit Verweis auf §3.3 und Befund 121, zweiter
  Faktor der Rest in einem Satz erklärt. Der Satz zum Zelllauf ohne die Eigenheit nennt rund 343 Mio. € (342,67 Mio. €,
  Tabelle in §3.3) statt rund 345 Mio. €. Beispielblock `rechenkette_95`: die zwei Zeilen mit den alten Faktoren rechnen
  mit 0,9867 und 0,9948 und mit 343 statt 345.

**Messung (Lauf 25.09.2026, Cache außerhalb des Repos).** `python3 docs/methodik/anlagen/95_zellvergleich.py --gemeinde
11000000 --ersatz`: Regel ohne (d) 335,78 Mio. €, Produkt gegen Regel × 0,9867, Rest × 0,9948 (Produkt der gerundeten
Faktoren 0,98157, (c) genau 0,98158); Zelllauf ohne Eigenheit 342,67 Mio. €. Warmsen (`--gemeinde 03256034 --ersatz`):
Regel ohne (d) 167.246 €, Produkt gegen Regel × 0,8004, Rest × 0,9159, Zelllauf ohne Eigenheit 173.099 €. Die Tabelle in
§3.3 bleibt (Berlin 338,10 Mio. €, 342,67 Mio. €, × 0,987, × 0,925–0,998; Warmsen 138.543 €, 173.099 €, × 0,800,
× 0,622–0,904); (a)–(d), die Kette (362,89 Mio. €) und Kapitel 7 sind unverändert.

| Nr | Stelle | Art | Begründung | Vorschlag | Kat. | Prüfausdruck | Status |
|---|---|---|---|---|---|---|---|
| 121 | §3.0 Wirkung (c) ↔ §3.3 (Regel Fassung T-1233) | Widerspruch (Regression durch T-1233) | §3.0 (c) teilt × 0,982 auf in „× 0,9802 durch eine Eigenheit des Produkts … (Befund 104; Ersatzregel dafür in §3.3)“ und „Der Rest, × 1,0014, sind Altersstruktur und Wohnlage der Älteren“. Gemessen ist das gegen den einheitlichen Anteil 65+ der übrigen Zellen (19,87 %, Skriptzeile „Eigenheit in (c), Befund 104“), also gegen genau die Annahme, die §3.3 mit Befund 117 verwirft. Für dieselbe Eigenheit nennt §3.3 in Berlin × 0,987 (heute gegen Regel). Damit läge der Rest bei rund × 0,995 statt × 1,0014, seine Richtung kehrt sich um. Der Adressat liest für eine Sache zwei Zahlen | (c) im Skript gegen die Regel aus §3.3 aufteilen (Stufe 1 und 2, ohne (d)) und die Zeile „Eigenheit in (c)“ entsprechend beschriften. §3.0 (c) mit den gemessenen Werten neu fassen und dort auf Befund 121 verweisen. (c) × 0,982, (a)–(d), die Kette (362,89 Mio. €) und Kapitel 7 bleiben unverändert | C | `python3 -c "import sys; s=open('docs/methodik/95_hitzebelastung.md',encoding='utf-8').read(); t=s[s.index('### 3.0'):s.index('### 3.1')]; sys.exit(not ('Der Rest, × 1,0014' not in t and 'Befund 121' in t))"` | behoben (T-1266): Skriptzeile „Eigenheit in (c)“ teilt mit `--ersatz` gegen die Regel aus §3.3 (Berlin × 0,9867 und × 0,9948); §3.0 (c) neu gefasst mit Verweis auf §3.3 und Befund 121, rund 343 Mio. € statt rund 345 Mio. €; Tabelle in §3.3, (a)–(d), Kette und Kapitel 7 unverändert |

## Runde 23 — Gegenprüfung nach Befund 121 (frische Sitzung, 26.09.2026): Null-Runde

Nachweis: Firmen-Repo, `tickets/T-1266-methodik_manager.md`, Abschnitt „Urteil“, Eintrag „2026-09-26T00:22:47Z ·
Runde 0 · methodik_manager (opus/xhigh)“: Urteil **freigabe** („**Urteil:** freigabe“). Eine eigene Zeile
`VERDIKT: …` wie in Runde 15 enthält dieses Urteil nicht; die Verdiktzeile ist der Schlusssatz der Begründung:
„Neue Befunde der Kategorien A, B und C gibt es keine, das ist eine Null-Runde; T-1234 trägt sie ein.“ Die
Gegenprüfung nach §5 in frischer Sitzung (Lints, 14 Leitfragen, E1–E5) hat die Arbeit aus Runde 22 (Befund 121) und
die übernommenen Runden 19–21 geprüft. „Runde 0“ ist die Zählung im Ticket, im Ledger ist es Runde 23, die Runde nach
Runde 22. Nach A-0046 ist sie die achte Runde seit der letzten Null-Runde (Runde 15); die Zählung endet hier, die Grenze
von zehn Runden ist nicht erreicht. Merge des Pakets nach `main`: Commit fc124562. Neue Befunde: keine.
Zurückgestellt bleibt 116 (Code-Nachzug beim cto); das ist kein A-Befund. Der Hinweis ohne Befund aus dem Urteil
(Aufruf in §3.0 ohne `--ersatz`) bleibt für die nächste inhaltliche Berührung vorgemerkt. Eingetragen mit
T-1234-methodik_manager; am Bericht ändert sich nur die Statuszeile (ABNAHMEREIF, Abnahme durch den methodik_manager
steht aus).

## Runde 24 — Nacharbeit aus der fachlichen Abnahme zu T-1234 (T-1295, 26.09.2026): neue Befunde 122–124, behoben

Anlass: fachliche Abnahme des methodik_manager im Urteil zu T-1234 (26.09.2026, `MANAGER-REVIEW: NACHARBEIT (2 Punkte)`,
Nacharbeitspunkte (a) und (b)); Vorgaben im Nachtrag des CMO in `tickets/T-1197-cmo.md`, Runde 1. Schritt B nach
`.claude/methodik-loop.md`: erst die Befunde, dann die Revision. Befund 124 ist ein Befund aus der Recherche zu (a): Er
weicht von der Lesart des Abnahmekriteriums ab (Faktor 0,93 unmittelbar auf den Exzess) und wird deshalb eigens geführt,
nicht still korrigiert. Der Prüfausdruck von Befund 111 zählte genau 19 Blöcke in Kapitel 7; mit den drei neuen Blöcken sind es 22, der Ausdruck ist darauf fortgeschrieben und in seiner Statuszeile vermerkt. Nach A-0046 ist Runde 24 die erste Runde seit der letzten Null-Runde (Runde 23).

Der Jahresbetrag Berlin der Kette (§3.0 Ebene 10, 362,9 Mio. €) bleibt unverändert: Beide Hebel wirken nur, wenn eine
Kommune die Maßnahme wählt (Zustand „mit Anpassung", §1(b)); der Basiswert ist der Zustand ohne weitere Anpassung.

| Nr | Stelle | Art | Begründung | Vorschlag | Kat. | Prüfausdruck | Status |
|---|---|---|---|---|---|---|---|
| 122 | §5 Hebel S157, Kapitel 7, Zeichentabelle §3.6 | Lücke (P1, §3.9: Parameter ohne Block, Band und Formel) | rOR ≈ 0,93 [46] stand nur als Text in §5 und im Register; kein Parameter-Block, keine Bandbreite aus dem Konfidenzintervall, keine Formel, wie der Faktor am Band 85+ andockt; das Produkt kann den Hebel so nicht rechnen und die Parameterliste zeigt ihn nicht | Block `heat.ror_s157` (0,93, Band aus dem KI von [46], `kennzeichnung:` nach Log 40), Formelzeile: Wirkung nur auf den Exzess 85+ der Heimbewohner im gekühlten Anteil; Zeichentabelle; Beispiel-Block Berlin in €; Andockpunkt im Produkt `COOLING_ROOMS_DRINKING_WATER` | B | `grep -qF 'id: heat.ror_s157' docs/methodik/95_hitzebelastung.md && grep -qF 'band: [0.87, 0.99]' docs/methodik/95_hitzebelastung.md && grep -qF 'python test: s157_berlin' docs/methodik/95_hitzebelastung.md && grep -qF 'COOLING_ROOMS_DRINKING_WATER' docs/methodik/95_hitzebelastung.md` | behoben (T-1295): Blöcke `heat.ror_s157` (0,93, Band 0,87–0,99, `quelle`) und `heat.g_s157` (0,29, `abschaetzung_kap3`), Formelzeile in §5, Zeichentabelle, Beispiel-Block `s157_berlin` (Berlin, alle Heime gekühlt: 25,0 Mio. € je Jahr weniger) |
| 123 | §5 Z. 995 und §1(b) Z. 125 (Schutzprogramme vulnerable Gruppen) | Nullwirkung behauptet (P2) und falsche Zuordnung | Der Hebel lief über \(v_{\text{vers},a}\), das auf Ebene der Kommune genau 1 ist (§3.0 Ebene 6): Die Wirkung war faktisch null, ohne Zahl und ohne Begründung. Zugeordnet war er S157 (gekühlte Räume), obwohl er Menschen ab 75 außerhalb der Heime betrifft. Im Produkt steht dazu `VULNERABLE_GROUP_PROGRAMS` mit `default_reduction` 0.22 ohne Gegenstück im Bericht | Block `heat.delta_vg` mit `kennzeichnung: abschaetzung_kap3`, Andockpunkt Faktor auf den Wochenexzess 75–84 und 85+, Zentralwert, Band und Sensitivität auf den Berlin-Betrag; Registerzeile; Log-Eintrag mit Gegenüberstellung zu 0.22; Zuordnung zu S157 in §5 und §1(b) gestrichen | B | `grep -qF 'id: heat.delta_vg' docs/methodik/95_hitzebelastung.md && grep -qF '95-S152-03' docs/evidenz/register.md && grep -qF 'default_reduction' docs/methodik/95_hitzebelastung.md && ! grep -qF 'Schutzprogramme vulnerable Gruppen (S157)' docs/methodik/95_hitzebelastung.md` | behoben (T-1295): Block `heat.delta_vg` (0,90, Band 0,80–0,985), Herleitung in §5, Beispiel-Block `schutzprogramme_berlin` (20,5 Mio. € je Jahr, Band 3,1–41,0 Mio. €), Register 95-S152-03, Log 43 ⚠, §1(b) und §5 ohne S157 und ohne \(v_{\text{vers},a}\); Zahlen in Runde 25 fortgeschrieben (Befunde 125 und 128: 0,864 statt 0,90, 23,1 statt 20,5 Mio. €) |
| 124 | §5 Hebel S157 ↔ Abnahmekriterium T-1295 (2) | Abweichung der Recherche von der Vorgabe (Lesart der Effektgröße) | [46] misst die Odds des Todes an Extremhitzetagen insgesamt: ohne Klimaanlage OR 1,11 (1,06–1,16), mit Klimaanlage 1,03 (0,98–1,07), Verhältnis rOR 1,08 (1,01–1,15), gelesen als 0,93 (0,87–0,99). Der Faktor wirkt also auf das Risiko am Hitzetag, nicht auf dessen Exzess. Unmittelbar auf den Exzess gelegt (Exzess × 0,93) senkte er den Heim-Exzess nur um 7 % statt um rund 71 % und unterschätzte die Wirkung in Berlin rund zehnfach (2,5 statt 25,0 Mio. € je Jahr bei vollem Ausbau) | Zentralwert 0,93 und Band aus [46] bleiben im Block; übersetzt wird er in einen Exzessfaktor \(g_{\text{S157}} = (\text{rOR} \times \text{OR}_{\text{ohne}} - 1)/(\text{OR}_{\text{ohne}} - 1)\) = 0,29, der nur auf den Exzess 85+ der Heimbewohner im gekühlten Anteil wirkt; beide Fassungen im Beispiel-Block und in §5 ausgewiesen, Wahl begründet | B | `grep -qF 'id: heat.g_s157' docs/methodik/95_hitzebelastung.md && grep -qF 'Befund 124' docs/methodik/95_hitzebelastung.md` | behoben (T-1295): Block `heat.g_s157`, Übersetzung und Vergleich beider Fassungen in §5 und im Beispiel-Block; zur Bestätigung durch den methodik_manager in der Meldung genannt |

## Runde 25 — Nacharbeit 1 zu T-1295 nach Urteil methodik_manager Runde 0 (26.09.2026): neue Befunde 125–128, behoben

Anlass: Urteil des methodik_manager zu T-1295 (26.09.2026, 02:44:44Z, `MANAGER-REVIEW: NACHARBEIT (4 Punkte)`,
`GEGENPRÜFUNG §5: KEINE NULL-RUNDE`), Nacharbeitspunkte (1) bis (4), dort als Befunde 125–128 vorgeschlagen. Schritt B
nach `.claude/methodik-loop.md`: erst die Befunde, dann die Revision. Befund 124 hat der methodik_manager im selben Urteil
fachlich bestätigt. Nach A-0046 ist Runde 25 die zweite Runde seit der letzten Null-Runde (Runde 23).

Zahlen, die sich ändern: \(w_{\text{VG}}\) 0,68 statt 0,5 (Befund 128), damit \(\delta_{\text{VG}}\) 0,864 statt 0,90 und
Band 0,794–0,985 statt 0,80–0,985 (Obergrenze der Wirkung gekappt am Paketwert Deutschland [47]); Berlin ohne
Heimbewohner 85+ (Befund 125): 1.054 statt 1.274 YLL, 169,5 statt 204,9 Mio. € Bezugsgröße, Wirkung 23,1 statt 20,5
Mio. € je Jahr (Band 2,5–34,9 Mio. €), 6,4 % (0,7–9,6 %) des Jahresbetrags. Der Jahresbetrag Berlin der Kette (§3.0
Ebene 10, 362,9 Mio. €) bleibt unverändert, weil der Hebel nur bei Wahl der Maßnahme wirkt. Kapitel 7 bekommt keinen
neuen Block; der Prüfausdruck von Befund 111 (22 Blöcke) bleibt.

| Nr | Stelle | Art | Begründung | Vorschlag | Kat. | Prüfausdruck | Status |
|---|---|---|---|---|---|---|---|
| 125 | §5 Hebel Schutzprogramme (Formelzeile, Doppelzählungs-Wächter), Kapitel 7 `heat.delta_vg` und `schutzprogramme_berlin`, Log 43, Register 95-S152-03 | Widerspruch (Doppelzählung Text ↔ Formel) | §5 sagte „Heimbewohner zählen über S157, nicht hier", die Formelzeile \(D_a^{\text{mit}} = D_a \times \delta_{\text{VG}}\) und der Beispiel-Block nahmen aber das ganze Band 85+ (635,4 + 638,8 YLL), also auch den Heimanteil \(h_{\text{Heim}}\) = 0,344. Wählt eine Kommune beide Hebel, zählte der Heim-Exzess zweimal; allein überzeichnete der Hebel Berlin um rund 3,5 Mio. € | Band 85+ um \((1 - h_{\text{Heim}})\) kürzen in Formelzeile, Block-Kommentar, Beispiel-Block, Sensitivität, Log 43 und Registerzeile; Band 75–84 bleibt ganz, weil der Bericht dort keinen Heimanteil führt (Modellgrenze, Richtung nach oben) | B | `grep -qF '638.8 * (1 - h_heim)' docs/methodik/95_hitzebelastung.md && ! grep -qF '(635.4 + 638.8) *' docs/methodik/95_hitzebelastung.md && grep -qF '(1 - h_{\text{Heim}})' docs/methodik/95_hitzebelastung.md` | behoben (T-1295, Nacharbeit 1): Formelzeile \(\Delta D_{\text{VG}} = [D_{75\text{–}84} + D_{85+} \times (1 - h_{\text{Heim}})] \times (1 - \delta_{\text{VG}})\); Berlin 1.054 YLL, 169,5 Mio. € Bezugsgröße; Block, Beispiel-Block, Log 43, Register nachgezogen |
| 126 | §5 Doppelzählungs-Wächter von \(\delta_{\text{HAP}}\) und \(\delta_{\text{VG}}\), Log 43 | Lücke (Doppelzählung bei gleichzeitiger Wahl ungeregelt) | \(\delta_{\text{HAP}}\) stützt sich auf [45, 47]; das Paket von Urban 2025 [47] enthält den Schutz vulnerabler Gruppen als Kernelement. Wählt eine Kommune Hitzeaktionsplan und Schutzprogramm zusammen, kann der Bericht diesen Baustein zweimal buchen; der Wächter nannte nur \(c_{\text{kal}}\) | Regel für die gleichzeitige Wahl: auf den Bändern 75–84 und 85+ (ohne Heim) multiplikativ, gekappt auf den Paketwert Deutschland 0,794 [47]; Satz in §5 bei beiden Hebeln und in Log 43; Beispiel-Block rechnet die Regel nach | B | `grep -qF 'max(delta_hap * delta_vg, 0.794)' docs/methodik/95_hitzebelastung.md && grep -qF 'Kappung' docs/methodik/95_hitzebelastung.md` | behoben (T-1295, Nacharbeit 1): Regel „das Produkt beider Faktoren, höchstens aber bis 0,794" in §5 bei beiden Hebeln und in Log 43; zentral 0,95 × 0,864 = 0,821, keine Kappung; bei \(\delta_{\text{HAP}}\) 0,85 gekappt; nachgerechnet in `schutzprogramme_berlin` |
| 127 | Knoten-Bilanz, Zeile S152 | Lücke (Knoten-Bilanz nicht nachgezogen) | Zeile S152 führte nur \(\text{pop}_a\), \(f_a\), \(m_a\), \(q_{\text{1P}}\) und „Schicht B"; \(\delta_{\text{VG}}\) fehlte als Maßnahmen-Hebel, obwohl §1(b) und §5 ihn S152 zuordnen. S152 heißt in der Arbeitsmappe „Altersstruktur"; einen eigenen Knoten für vulnerable Gruppen führt Kette W182 nicht | In der Zeile „Maßnahmen-Hebel \(\delta_{\text{VG}}\) (§5)" ergänzen und in einem Satz begründen, warum der Hebel an S152 andockt | C | `python3 -c "import sys; s=open('docs/methodik/95_hitzebelastung.md',encoding='utf-8').read(); z=[x for x in s.splitlines() if x.startswith('\| S152 ')]; sys.exit(not (len(z) == 1 and 'delta_{' in z[0] and 'W182' in z[0] and 'Maßnahmen-Hebel' in z[0]))"` | behoben (T-1295, Nacharbeit 1): Zeile S152 „Schicht B + Maßnahmen-Hebel", \(\delta_{\text{VG}}\) mit Begründung (Programme wählen nach Alter ab 75 aus; kein eigener Knoten in W182) |
| 128 | §5 Herleitung \(\delta_{\text{VG}}\), Zeichentabelle \(r_{\text{VG}}, w_{\text{VG}}\), Block `heat.delta_vg`, Register 95-S152-03, Quellen [47] und [70] | Quellenbeleg fehlt (P1, §3.9) und Rechenfehler (Reichweite doppelt abgezogen) | \(w_{\text{VG}}\) = 0,5 trug den Zentralwert, belegt nur aus dem Abstract von [70]. Nach dem Volltext (PMC5923757) ist der Vergleich ökologisch: verglichen werden alle Menschen ab 75 der Stadtteile (Tabelle 1: 6.483 mit, 5.724 ohne Programm), eingeschrieben waren 4.720 (Abschnitt 3 „Results"), also 72,8 %. Die Halbierung (Tabelle 2: +48,8 % gegen +97,3 %) ist damit schon eine Wirkung auf die ganze Bevölkerung; mit \(r_{\text{VG}}\) multipliziert, zog der Bericht die Reichweite zweimal ab. Für [47] fehlte die Fundstelle von Deutschland −20,6 % (15,8–25,7 %) und von „Bausteine nicht getrennt" | \(w_{\text{VG}}\) = 0,498 / 0,728 = 0,68 (Band 0,30–0,68) mit Fundstellen; \(\delta_{\text{VG}}\) = 1 − 0,20 × 0,68 = 0,864, Band 0,794–0,985 (Obergrenze der Wirkung am Paketwert Deutschland gekappt); Fundstellen [47]: Tabelle 1 (Western Europe, Germany) und Abschnitt 2.2 mit Stage 2 der Auswertung (Indikator „HPP vorhanden", keine Schätzung je Baustein) in §5 und Register | B | `grep -qF 'wert: 0.864' docs/methodik/95_hitzebelastung.md && grep -qF '4.720' docs/methodik/95_hitzebelastung.md && grep -qF '72,8 %' docs/evidenz/register.md && grep -qF 'Tabelle 1' docs/evidenz/register.md` | behoben (T-1295, Nacharbeit 1): \(w_{\text{VG}}\) 0,68 aus [70] Tabelle 1, Tabelle 2 und Abschnitt 3; \(\delta_{\text{VG}}\) 0,864 (0,794–0,985); Fundstellen [47] in §5 und Register; Zeichentabelle, Block, Beispiel-Block, Log 43 nachgezogen |

## Runde 26 — Nacharbeit 2 zu T-1295 nach Urteil methodik_manager Runde 1 (26.09.2026): neuer Befund 129, behoben

Anlass: Urteil des methodik_manager zu T-1295 (26.09.2026, 03:37:29Z, `MANAGER-REVIEW: NACHARBEIT (1 Punkt)`,
`GEGENPRÜFUNG §5: KEINE NULL-RUNDE`), dort als Befund 129 vorgeschlagen. Die Befunde 125–128 hat das Urteil als
abgearbeitet bestätigt. Schritt B nach `.claude/methodik-loop.md`: erst der Befund, dann die Revision. Nach A-0046 ist
Runde 26 die dritte Runde seit der letzten Null-Runde (Runde 23). Der Jahresbetrag Berlin der Kette (§3.0 Ebene 10,
362,9 Mio. €) bleibt unverändert, weil beide Hebel nur bei Wahl der Maßnahme wirken. Die Zahlen des Hebels S157 allein
(37,4 Todesfälle, 25,0 Mio. € bei vollem Ausbau) bleiben; neu ist nur die Rechnung bei gleichzeitiger Wahl. Kapitel 7
bekommt keinen neuen Block; der Prüfausdruck von Befund 111 (22 Blöcke) bleibt.

| Nr | Stelle | Art | Begründung | Vorschlag | Kat. | Prüfausdruck | Status |
|---|---|---|---|---|---|---|---|
| 129 | §5 Hebel S157 (Formelzeile \(\Delta D_{\text{S157}}\)) und Doppelzählungs-Wächter von \(\delta_{\text{HAP}}\), Kapitel 7 `s157_berlin` | Lücke (Doppelzählung bei gleichzeitiger Wahl von S157 und Hitzeaktionsplan) | \(\delta_{\text{HAP}}\) wirkt multiplikativ auf den Exzess aller Bänder, also auch auf den Heim-Exzess 85+; \(\Delta D_{\text{S157}}\) wurde aber vom ungedämpften \(D_{85+}\) abgezogen. Die Regel aus Befund 126 gilt nur für 75–84 und 85+ ohne Heim, für den Heimanteil fehlte eine Regel. Additiv gelesen nehmen beide Hebel in Berlin 5 % + 70,6 % = 75,6 % des Heim-Exzesses (52,9 Todesfälle) weg, multiplikativ 1 − 0,95 × 0,294 = 72,1 %: rund 1,9 Todesfälle oder 1,2 Mio. € je Jahr zu viel (das Urteil nennt gerundet 1,3 Mio. €; ungerundet 1,25 Mio. €), bei \(\delta_{\text{HAP}}\) = 0,85 rund 3,7 Mio. € | Regel in §5 beim Hebel S157: Bei gleichzeitiger Wahl wird \(\Delta D_{\text{S157}}\) aus \(D_{85+} \times \delta_{\text{HAP}}\) gerechnet (multiplikativ); Verweis beim Doppelzählungs-Wächter von \(\delta_{\text{HAP}}\); Zeile im Beispiel-Block `s157_berlin`, die die gemeinsame Wirkung nachrechnet | C | `grep -qF 'd85 * delta_hap * h_heim' docs/methodik/95_hitzebelastung.md && grep -qF 'Befund 129' docs/methodik/95_hitzebelastung.md` | behoben (T-1295, Nacharbeit 2): Regel multiplikativ in §5 beim Hebel S157 und beim Wächter von \(\delta_{\text{HAP}}\); Berlin, alle Heime gekühlt, mit Hitzeaktionsplan: zusammen 72,1 % des Heim-Exzesses (38,1 Todesfälle), davon S157 35,5 Todesfälle oder 23,7 Mio. € je Jahr; nachgerechnet in `s157_berlin` (1,25 und 3,75 Mio. € Unterschied zur additiven Lesart) |

## Runde 27 — Befunde aus dem Urteil zu T-1295 Runde 2 und den Nachträgen des CEO (T-1329, 26.09.2026): neue Befunde 130–132, behoben

Anlass: Urteil des methodik_manager zu T-1295 Runde 2 (26.09.2026, 04:23:57Z, Punkte a–c) und Nachträge des CEO in
T-1190 (26.09.2026, 03:00, Punkte −1 bis −3, und 03:35, Punkt −1). Der Stand von T-1295 (Runden 24–26, Bericht) ist
als Dateiinhalt aus 0d413f92 übernommen, im Register nur die Zeilen 95-S157-01 und 95-S152-03; 96-S158-01 bleibt wie
auf main (T-1329, Ersatz für T-1327). Schritt B nach `.claude/methodik-loop.md`: erst die Befunde, dann die Revision.
Nach A-0046 ist Runde 27 die vierte Runde seit der Null-Runde 23; die Grenze ist Runde 33. **Bewusste Abweichung vom
Auftrag des CMO:** Kapitel 7 bekommt mit `heat.delta_vg_morb` einen 23. Block, der Auftrag sagte „die 22 Blöcke
bleiben“. Ohne den Block stünde die Wirkung der Schutzprogramme auf die Einweisungen weiter ohne Zahl da und käme in
der Gegenprüfung als Befund zurück (P2, Befund 131); der Prüfausdruck von Befund 111 zählt jetzt 23 Blöcke.
Unverändert bleiben die Kette (Berlin 362,9 Mio. € je Jahr), S157 (25,0 Mio. €, Band 3,6–35,4 Mio. €) und der
Zentralwert der Schutzprogramme (23,1 Mio. €). Geändert ist nur das Band der Schutzprogramme: \(w_{\text{VG}}\) 0–0,68
statt 0,30–0,68, \(\delta_{\text{VG}}\) 0,794–1,0 statt 0,794–0,985, Berlin 0–34,9 statt 2,5–34,9 Mio. € (Befund 132,
Begründung dort).

| Nr | Stelle | Art | Begründung | Vorschlag | Kat. | Prüfausdruck | Status |
|---|---|---|---|---|---|---|---|
| 130 | §5 Hebel S157 (Andockpunkt, Modellgrenze), Entscheidungslog | Lücke (P2: Stand der Maßnahme im Produkt nicht eingeordnet) | §5 nannte `COOLING_ROOMS_DRINKING_WATER` als Andockpunkt, ohne zu sagen, dass die Maßnahme in `backend/app/data/catalog_parked.py` geparkt ist. Der Leser nahm an, das Produkt rechne S157 heute. Der geparkte Katalog setzt `default_reduction` 0.18 auf die Exposition, der Bericht den Faktor 0,29 auf den Heim-Exzess; die Gegenüberstellung fehlte, ebenso die Einordnung öffentlicher Kühlzentren außerhalb der Heime | Ein Satz in §5: geparkt, heute in keiner Kommune angeboten, heute keine Wirkung, auch keine Nullwirkung; Vermerk, dass öffentliche Kühlzentren außerhalb der Heime erst beim Aktivieren eine eigene Abschätzung nach P2 bekommen; Log-Eintrag mit Gegenargument (0.18 auf die Exposition gegen 0,29 auf den Heim-Exzess, \(s_{\text{gek}}\) als Eingabe der Kommune). Die Aktivierung ist eine Empfehlung an den cto, kein Code | C | `grep -qF 'catalog_parked' docs/methodik/95_hitzebelastung.md && grep -qF 'Befund 130' docs/methodik/95_hitzebelastung.md && grep -qF 'auch keine Nullwirkung' docs/methodik/95_hitzebelastung.md && grep -qF 'Eintrag 44' docs/methodik/95_hitzebelastung.md` | behoben (T-1329): §5 beim Andockpunkt („Heute geparkt“) und in der Modellgrenze; Log 44 ⚠ mit Gegenargument, Kopf des Logs nachgezogen; Kapitel 7 und Beträge unverändert |
| 131 | §5 Hebel Schutzprogramme (Morbidität), Kapitel 7 `heat.delta_vg`, Zeichentabelle | Nullwirkung behauptet (P2) | „keine Wirkung angesetzt, Richtung offen“ ließ die Wirkung auf die Einweisungen ohne Zahl und ohne Band bei null stehen; das Produkt hat dafür keinen Parameter | Block `heat.delta_vg_morb` mit Zentralwert 1,0 und Band in beide Richtungen, `kennzeichnung: abschaetzung_kap3`; Herleitung beider Grenzen und Sensitivität Berlin in € in §5; Zeichentabelle; Kommentar in `heat.delta_vg` mitziehen | B | `python3 -c "import sys; s=open('docs/methodik/95_hitzebelastung.md',encoding='utf-8').read(); k=s[s.index('## 7 '):s.index('## 8 ')].split('parameter:'); f=[x for x in k if 'id: heat.delta_vg_morb' in x]; sys.exit(not (len(f) == 1 and 'wert: 1.0' in f[0] and 'band: [0.864, 1.136]' in f[0] and 'kennzeichnung: abschaetzung_kap3' in f[0] and 'keine Wirkung angesetzt' not in s and 'VG,morb' in s))"` | behoben (T-1329): Block `heat.delta_vg_morb` 1,0 (Band 0,864–1,136, `abschaetzung_kap3`); unten wie \(\delta_{\text{VG}}\) (Einweisungen verhindert), oben 1 + 0,20 × 0,68 (Einweisungen vorgezogen); Berlin 48,0 Einweisungen ab 75 außerhalb der Heime, 0,34 Mio. € je Jahr, über das Band ± 0,05 Mio. €; Zeichentabelle, Kommentar in `heat.delta_vg`, Log 43 und Register nachgezogen |
| 132 | §5 Hebel S157 (\(g_{\text{S157}}\)) und Hebel Schutzprogramme (\(w_{\text{VG}}\)), Kapitel 7 `heat.delta_vg`, Zeichentabelle, Register 95-S152-03 | Band ohne Prüfung an der Quelle (P1, §3.9) | (a) \(g_{\text{S157}}\) rechnet mit \(\text{OR}_{\text{ohne}}\) = 1,11, ohne dessen Konfidenzintervall 1,06–1,16 aus [46]; ob das Band 0–0,90 es trägt, stand nicht da. (b) Die untere Grenze 0,30 von \(w_{\text{VG}}\) war von KAP3 gesetzt, obwohl [70] in Tabelle 2 die Streuung der Anstiege zwischen den Stadtteilen angibt. Ein Band darf nicht enger sein, als die Quelle es trägt | (a) Satz in §5, warum \(\text{OR}_{\text{ohne}}\) fest bleibt; (b) Intervall aus Tabelle 2 als Formelzeile mit Fundstelle, Band danach richten; schließt es keine Wirkung ein, reicht das Band bis dorthin, der Zentralwert bleibt | B | `grep -qF 'Befund 132' docs/methodik/95_hitzebelastung.md && grep -qF '23,6 bis 120,6' docs/methodik/95_hitzebelastung.md && grep -qF 'band: [0.794, 1.0]' docs/methodik/95_hitzebelastung.md && grep -qF '(0–0,68' docs/evidenz/register.md` | behoben (T-1329): (a) über \(\text{OR}_{\text{ohne}}\) 1,06–1,16 liegt \(g_{\text{S157}}\) bei 0–0,49, beide Intervalle aus [46] zugleich bei 0–0,83, beides im Band 0–0,90; \(\text{OR}_{\text{ohne}}\) bleibt fest, Band unverändert. (b) Unterschied der Anstiege 48,5 Pp., Standardfehler √(73,1²/4 + 6,8²/3) = 36,8, 95-%-Intervall −23,6 bis 120,6 Pp., schließt keine Wirkung ein; \(w_{\text{VG}}\) 0–0,68, \(\delta_{\text{VG}}\) 0,794–1,0, Berlin 0–34,9 Mio. € (0–9,6 %); Zentralwert 0,68 bleibt (Regression in [70], Results: p < 0,001; in Runde 28 berichtigt, Befunde 133 und 134); Beispiel-Blöcke `s157_berlin` und `schutzprogramme_berlin` rechnen beides nach |

## Runde 28 — Nacharbeit 1 zu T-1329 nach Urteil methodik_manager Runde 0 (26.09.2026): neue Befunde 133–134, 133 behoben, 134 zurückgestellt

Anlass: Urteil des methodik_manager zu T-1329 (26.09.2026, 06:16:19Z, `VERDIKT: KEINE NULL-RUNDE (1 Befund)`,
`MANAGER-REVIEW: NACHARBEIT (1 Punkt, dazu 4 Formhinweise)`), dort als Befund vorgeschlagen und hier als Befund 133
geführt. Die vier Formhinweise nennt das Urteil nicht einzeln; sie sind deshalb nicht bearbeitet. Schritt B nach
`.claude/methodik-loop.md`: erst die Befunde, dann die Revision. Nach A-0046 ist Runde 28 die fünfte Runde seit der
Null-Runde 23; die Grenze ist Runde 33. Volltext von [70] gelesen als JATS-XML von Europe PMC
(https://www.ebi.ac.uk/europepmc/webservices/rest/PMC5923757/fullTextXML), vollständig: Abschnitte 2.1, 2.4, 3 und 4, Tabellen 1–3 mit
Fußnoten; die übrigen Abschnitte (1, 2.2, 2.3, 5) nur nach Titel gesichtet. Beim Lesen von Tabelle 3 ist Befund 134
aufgefallen. Unverändert bleiben die Kette (Berlin 362,9 Mio. €), S157 (25,0 Mio. €), der Zentralwert der
Schutzprogramme (23,1 Mio. €) und ihr Band (0–34,9 Mio. €); Kapitel 7 behält 23 Blöcke.

| Nr | Stelle | Art | Begründung | Vorschlag | Kat. | Prüfausdruck | Status |
|---|---|---|---|---|---|---|---|
| 133 | §5 Hebel Schutzprogramme (untere Grenze \(w_{\text{VG}}\)), Quelle [70], Register 95-S152-03 | Quellenbeleg ungesichert (P1, eiserne Regel 3) | Die Werte aus [70] Tabelle 2 (Standardabweichung 73,1 und 6,8 Pp., 4 und 3 Stadtteile) und „25 vermiedene Todesfälle, 13 %“ stammten aus zwei Abrufen eines zusammenfassenden Abrufmodells, das sich bei den Todesfallzahlen widersprochen hatte. Eine Liste der gelesenen Abschnitte fehlte, „Methodenteil“ war keine Fundstelle. Einen Abschnitt „Limitations“, auf den §5 und [70] seit T-1295 verweisen, hat [70] nicht; die Grenzen stehen im letzten Absatz von Abschnitt 4. Die „13 %“ standen in §5 als Ergebnis der Regression, sie stammen aber aus dem Vergleich mit den erwarteten Todesfällen | Werte am Volltext nachlesen; Fundstellen mit Tabelle, Zeile, Fußnote und Abschnitt; gelesene Abschnitte nennen; „Limitations“ und „Methodenteil“ ersetzen; „13 %“ richtig zuordnen | B | `grep -qF '37,38 %' docs/methodik/95_hitzebelastung.md && grep -qF 'Fußnote 1' docs/methodik/95_hitzebelastung.md && grep -qF 'fullTextXML' docs/methodik/95_hitzebelastung.md && ! grep -qF 'Methodenteil' docs/methodik/95_hitzebelastung.md && ! grep -qF 'Limitations' docs/methodik/95_hitzebelastung.md` | behoben (T-1329, Nacharbeit 1): wörtlich bestätigt in Tabelle 2, Zeile „Δ1: June–September 2015 vs. June–September 2014 (%)“: ohne Programm Centro Storico 37,38; Aventino 212,50; XX Settembre 162,59; Celio 130,30; Mean (SD) 97.3 (73.1); mit Programm Trastevere 62,37; Testaccio 44,32; Esquilino 46,71; Mean (SD) 48.8 (6.8); Fußnote 1 „Weighted average for the population size in the summer of 2015“; Zuordnung der Stadtteile auch in Tabelle 1. Abschnitt 3: 167 und 169 Todesfälle, erwartet 192, „25 deaths were averted, a 13% reduction in mortality“, Regression „p < 0.001“. Die Rechnung (Standardfehler 36,8; −23,6 bis 120,6 Pp.) und das Band 0–0,68 bleiben. §5 nennt die Werte je Stadtteil mit Zeile und Fußnote und ordnet die „13 %“ den Todesfällen des Sommers zu. Die Grenzen verweisen auf Abschnitt 4, letzter Absatz. [70] nennt die gelesenen Abschnitte und die Adresse des Volltexts; das Register ist nachgezogen |
| 134 | §5 Hebel Schutzprogramme (Zentralwert \(w_{\text{VG}}\)), Log 43, Kapitel 7 `heat.delta_vg` | Abweichung der Recherche (Lesart der Quelle; P3) | Tabelle 3 von [70] gibt die bereinigte Wirkung des Programms auf den Anstieg: −24,372 Pp. (95-%-Intervall −29,029 bis −19,714), gewichtet nach Einwohnern und bereinigt um die Sterberate vor dem Sommer und den Anteil ab 90. Das ist halb so viel wie der rohe Unterschied von 48,5 Pp., auf dem der Zentralwert 0,68 beruht. Bereinigt ist \(w_{\text{VG}}\) 0,34 (0,28–0,41), \(\delta_{\text{VG}}\) 0,931, Berlin 11,7 statt 23,1 Mio. € je Jahr. Ein Teil des rohen Unterschieds ist Altersstruktur: Mit Programm sind 9,0 % der Einwohner 90 oder älter, ohne Programm 10,3 % (Tabelle 1); der Koeffizient ist 45,5 Pp. je Prozentpunkt (Tabelle 3). Beide Lesarten liegen im Band 0–0,68 | Entscheidung methodik_manager: Zentralwert auf die bereinigte Lesart senken (w 0,34, \(\delta_{\text{VG}}\) 0,931, Berlin 11,7 Mio. €; nachzuziehen sind §5, Block, Beispiel-Block, Zeichentabelle, Log 43, Register und die obere Grenze von \(\delta_{\text{VG,morb}}\), dann 1,069) oder die rohe Lesart mit Begründung in Log 43 halten. Eine Senkung kippt den Prüfausdruck von Befund 128 (`wert: 0.864`) in Runde 25; diese Runde bindet das Abnahmekriterium von T-1329 wörtlich. Deshalb ist die Senkung hier nicht umgesetzt (Zuschnitt, nicht Arbeit) | A | `grep -qF 'Entscheidung zu Befund 134' docs/methodik/95_hitzebelastung.md` | zurückgestellt (Entscheidung methodik_manager): beide Lesarten mit Betrag in §5, Log 43, Kapitel 7, Zeichentabelle und Register; Beispiel-Block `schutzprogramme_berlin` rechnet 0,34 (0,28–0,41) und 11,7 Mio. € nach; Zentralwert und Beträge unverändert |

## Runde 29 — Entscheidung zu Befund 134 und neuer Befund 135 aus dem Urteil zu T-1329 Runde 1 (T-1333, 26.09.2026): 134 und 135 behoben, Prüfausdrücke 128 und 131 fortgeschrieben

Anlass: Urteil des methodik_manager zu T-1329 Runde 1 (26.09.2026, 07:04:00Z, `VERDIKT: KEINE NULL-RUNDE (Befund 134
entschieden und offen, neuer Befund 135)`), Entscheidung zu 134: Zentralwert auf die bereinigte Lesart. Der Stand von
T-1329 (Runden 24–28, Bericht, Register) ist als Dateiinhalt aus 27a98a4f übernommen; die Runden 24–28 bleiben wörtlich
stehen, auch Runde 25 mit `wert: 0.864`. Weil der Prüfausdruck je Befund aus seinem letzten Vorkommen gilt, führt diese
Runde 128 und 131 mit fortgeschriebenem Ausdruck erneut (wie bei 111). Schritt B nach `.claude/methodik-loop.md`: erst
die Befunde, dann die Revision. Nach A-0046 ist Runde 29 die sechste Runde seit der Null-Runde 23; die Grenze ist
Runde 33. Kapitel 7 behält 23 Blöcke.

**Zahlen, die sich mit Absicht ändern (Befund 134):** \(w_{\text{VG}}\) 0,34 statt 0,68 (Band 0–0,68 bleibt),
\(\delta_{\text{VG}}\) 0,931 statt 0,864 (Band 0,794–1,0 bleibt), \(\delta_{\text{VG,morb}}\) Band 0,931–1,069 statt
0,864–1,136, zusammen mit \(\delta_{\text{HAP}}\) 0,885 statt 0,821. Berlin: **11,7 statt 23,1 Mio. € je Jahr** (3,2 %
statt 6,4 % des Jahresbetrags), Band 0–34,9 Mio. € unverändert, über die Reichweite 5–40 % 2,9–23,3 Mio. € statt
5,8–34,9 Mio. €; Einweisungen ± 0,02 statt ± 0,05 Mio. €; Log 43 11,7 von 79,8 Mio. € (rund 15 %). Begründung: Der
rohe Unterschied der Anstiege in [70] (48,5 Pp.) vermischt die Wirkung des Programms mit Altersstruktur und
Vorsterblichkeit; die Quelle bereinigt selbst (Tabelle 3, −24,4 Pp.), und ein Zentralwert am oberen Rand des eigenen
Bands verdoppelte den Nutzen. Unverändert bleiben die Kette (Berlin 362,9 Mio. €), S157 (25,0 Mio. €) und die 23 Blöcke.

**Abweichungen vom Auftrag (Zahlen aus dem Beispiel-Block `schutzprogramme_berlin`, der Block gilt):** (1) Kappung: Über
die Reichweite 5–40 % allein und zentral mit \(\delta_{\text{HAP}}\) 0,95 wird sie nicht mehr erreicht. Sie greift aber
weiter am oberen Bandende (\(w_{\text{VG}}\) 0,68, \(r_{\text{VG}}\) 40 %) und bei gleichzeitiger Wahl mit
\(\delta_{\text{HAP}}\) = 0,85: 0,85 × 0,931 = 0,791, es gilt 0,794. Formelzeile und Wort „Kappung“ bleiben (Befund
126). (2) Stärkster Treiber: Mit \(w_{\text{VG}}\) 0,34 bewegt das Band von \(w_{\text{VG}}\) (0–0,68) den Berlin-Betrag
um 0–23,1 Mio. €, die Reichweite (5–40 %) um 2,9–23,3 Mio. €. Beide sind etwa gleich stark, \(w_{\text{VG}}\) knapp
stärker; §5 nennt jetzt beide statt nur der Reichweite. (3) Formhinweis (a) aus dem Urteil (0,84 statt 0,83) ist nicht
übernommen: Unter log-normalen, unabhängigen Intervallen aus [46] liegt das 97,5-%-Quantil von \(g_{\text{S157}}\) nach
numerischer Integration bei 0,833, gerundet 0,83; die 0,837 des Urteils ist Zufallsstreuung einer Simulation. Der
Beispiel-Block `s157_berlin` rechnet das jetzt nach. (4) Seiten der IJERPH-PDF von [70]: Der Abruf mit python3 urllib
endet bei mdpi.com und europepmc.org mit HTTP 403; die Fundstellen bleiben Tabelle, Zeile und Abschnitt.

| Nr | Stelle | Art | Begründung | Vorschlag | Kat. | Prüfausdruck | Status |
|---|---|---|---|---|---|---|---|
| 134 | §5 Hebel Schutzprogramme (Zentralwert \(w_{\text{VG}}\)), Log 43, Kapitel 7 `heat.delta_vg` und `heat.delta_vg_morb`, Zeichentabelle, Register 95-S152-03 | Abweichung der Recherche (Lesart der Quelle; P3) | Der rohe Unterschied von 48,5 Pp. vermischt die Wirkung des Programms mit der Altersstruktur (Anteil ab 90: 9,0 % gegen 10,3 %; Koeffizient 45,5 Pp. je Prozentpunkt, Tabelle 3) und mit der Sterberate vor dem Sommer. Die Quelle bereinigt selbst und kommt auf −24,4 Pp. §5 nennt 0,68 selbst „eher die obere Grenze“. Ein Zentralwert am oberen Rand verdoppelt den Nutzen (Berlin 23,1 statt 11,7 Mio. € je Jahr) und stellt die Lage falsch dar (P3) | \(w_{\text{VG}}\) 0,34 als Abschätzung von KAP3. Das Band bleibt 0–0,68: unten das Intervall aus Tabelle 2, oben die rohe Lesart. Ein Satz dazu, warum das KI 19,7–29,0 aus Tabelle 3 kein Band trägt: Der Standardfehler 2,37 aus 7 nach Einwohnern gewichteten Stadtteilen ist zu eng. \(\delta_{\text{VG}}\) = 1 − 0,20 × 0,34 = 0,931, Band 0,794–1,0 bleibt. Berlin 11,7 Mio. € je Jahr (3,2 % von 362,9 Mio. €), Band 0–34,9 Mio. € bleibt. Über die Reichweite 5–40 % sind es 2,9–23,3 Mio. €; die Kappung wird nicht mehr erreicht. Zusammen mit \(\delta_{\text{HAP}}\): 0,95 × 0,931 = 0,885. \(\delta_{\text{VG,morb}}\): Band 0,931–1,069, Berlin ± 0,02 Mio. €. Nachziehen: Log 43 (11,7 von 79,8 Mio. €, rund 15 %), Zeichentabelle, Blöcke `heat.delta_vg` und `heat.delta_vg_morb`, `schutzprogramme_berlin`, Register 95-S152-03. Die rohe Lesart kommt als verworfene Variante mit einem Satz in Log 43 | A | `grep -qF 'wert: 0.931' docs/methodik/95_hitzebelastung.md && grep -qF 'band: [0.931, 1.069]' docs/methodik/95_hitzebelastung.md` | behoben (T-1333): \(w_{\text{VG}}\) 0,34 (Band 0–0,68) mit Satz zum KI aus Tabelle 3; `heat.delta_vg` 0,931 (0,794–1,0), `heat.delta_vg_morb` 1,0 (0,931–1,069); Berlin 11,7 Mio. € je Jahr (0–34,9 Mio. €; Reichweite 5–40 %: 2,9–23,3 Mio. €), mit \(\delta_{\text{HAP}}\) 0,885; Einweisungen ± 0,02 Mio. €; Log 43 mit der rohen Lesart 0,68 als verworfener Variante; Zeichentabelle, Kommentare der Blöcke, `schutzprogramme_berlin` und Register nachgezogen; Kappung nur noch am oberen Bandende und bei \(\delta_{\text{HAP}}\) 0,85 (Kopf der Runde) |
| 135 | §5 Hebel Schutzprogramme („vorerst die rohe Lesart … dem methodik_manager als Befund 134 vorgelegt“), Log 43 („über den Zentralwert entscheidet der methodik_manager“), Register 95-S152-03 („Entscheidung beim methodik_manager“) | Widerspruch zu P3/E3 | Die Kundenfassung stellt zwei Lesarten mit zwei Beträgen nebeneinander und nennt eine offene Entscheidung. Das ist nicht genau eine Methodik | Mit 134 auflösen. Die Hinweise auf den Arbeitsablauf fallen weg | B | `! grep -qE 'vorerst die rohe\|entscheidet der methodik_manager\|dem methodik_manager als Befund' docs/methodik/95_hitzebelastung.md && ! grep -qF 'Entscheidung beim methodik_manager' docs/evidenz/register.md` | behoben (T-1333): §5, Log 43 und Register nennen eine Lesart mit einem Betrag (11,7 Mio. €); die rohe Lesart steht nur noch als Obergrenze des Bands und in Log 43 als verworfene Variante |
| 128 | §5 Herleitung \(\delta_{\text{VG}}\), Block `heat.delta_vg`, Register 95-S152-03 | Fortschreibung des Prüfausdrucks (Befund 134) | Der Ausdruck aus Runde 25 prüft `wert: 0.864`; nach Befund 134 steht im Block 0.931. Die Fundstellen aus [70] (4.720, 72,8 %, Tabelle 1) bleiben | Ausdruck aus Runde 25 mit `wert: 0.931` statt `wert: 0.864` | B | `grep -qF 'wert: 0.931' docs/methodik/95_hitzebelastung.md && grep -qF '4.720' docs/methodik/95_hitzebelastung.md && grep -qF '72,8 %' docs/evidenz/register.md && grep -qF 'Tabelle 1' docs/evidenz/register.md` | behoben, Prüfausdruck fortgeschrieben in Runde 29 wegen Befund 134 (T-1333): Einschreibeanteil 0,728 aus [70] bleibt, \(\delta_{\text{VG}}\) jetzt 0,931 |
| 131 | §5 Hebel Schutzprogramme (Morbidität), Kapitel 7 `heat.delta_vg_morb`, Zeichentabelle | Fortschreibung des Prüfausdrucks (Befund 134) | Der Ausdruck aus Runde 27 prüft `band: [0.864, 1.136]`; nach Befund 134 ist das Band 0,931–1,069 (unten wie \(\delta_{\text{VG}}\), oben 1 + 0,20 × 0,34) | Ausdruck aus Runde 27 mit `band: [0.931, 1.069]` statt `band: [0.864, 1.136]` | B | `python3 -c "import sys; s=open('docs/methodik/95_hitzebelastung.md',encoding='utf-8').read(); k=s[s.index('## 7 '):s.index('## 8 ')].split('parameter:'); f=[x for x in k if 'id: heat.delta_vg_morb' in x]; sys.exit(not (len(f) == 1 and 'wert: 1.0' in f[0] and 'band: [0.931, 1.069]' in f[0] and 'kennzeichnung: abschaetzung_kap3' in f[0] and 'keine Wirkung angesetzt' not in s and 'VG,morb' in s))"` | behoben, Prüfausdruck fortgeschrieben in Runde 29 wegen Befund 134 (T-1333): Zentralwert 1,0 bleibt, Band 0,931–1,069, Berlin ± 0,02 Mio. € |

## Runde 30 — Gegenprüfung nach Befund 134 und 135 (frische Sitzung, 26.09.2026): Null-Runde

Nachweis: Firmen-Repo, `tickets/T-1333-methodik_manager.md`, Abschnitt „Urteil“, Eintrag „2026-09-26T07:58:46Z ·
Runde 0 · methodik_manager (opus/high)“:

**Urteil:** freigabe

Das Urteil schließt mit den eigenen Zeilen:

VERDIKT: NULL-RUNDE

MANAGER-REVIEW: ABGENOMMEN

Die Gegenprüfung nach §5 in frischer Sitzung ist zugleich die fachliche Abnahme. Geprüft hat sie die Arbeit aus Runde 29
(Befunde 134 und 135, fortgeschriebene Prüfausdrücke 128 und 131) als Re-Review des Diffs 27a98a4f..HEAD nach LF 5, 7
und 11; die volle Runde nach den Leitfragen lief im Urteil zu T-1329 vom 26.09.2026, 07:04:00Z. Maschinell: Lint „ALLE
LINTS GRÜN“ (252 Checks), Ledger-Gate „GRÜN“. „Runde 0“ ist die Zählung im Ticket, im Ledger ist es Runde 30, die Runde
nach Runde 29. Nach A-0046 ist sie die siebte Runde seit der Null-Runde 23 (Runden 24–30); die Zählung endet hier, die
Grenze Runde 33 ist nicht erreicht. Merge des Pakets nach `main`: Commit 6ac0e9c8. Neue Befunde: keine.

Zurückgestellt, jeweils mit Code-Nachzug beim cto, ohne neue Befundzeile:
- Befund 116: Ersatzregel für den geheimgehaltenen Anteil 65+ in `backend/app/services/zensus_loader.py` (Log 41,
  Fassung T-1233); das ist kein A-Befund.
- Registry-Parameter ohne Block, die der Bericht nicht löst: `risks.EXPECTED_ANNUAL_MORTALITY.ref_value` (145 YLL je
  100.000 EW) und `risks.EXPECTED_ANNUAL_MORBIDITY.ref_value` (4,5 Fälle je 100.000 EW). Beide sind Bezugswert der
  Index-Anzeige und Anker der Plausibilitätsprüfung, keine Rechenparameter der Schadensfunktion; am Jahresbetrag ändern
  sie nichts. Der Bericht führt sie nicht, die Registry zeigt sie als „belegt“, obwohl der Anker 18 Todesfälle je
  100.000 EW (etwa 1,7 × das schlimmste beobachtete Jahr) eine Setzung ist. Code-Nachzug: Kennzeichnung als
  Abschätzung von KAP3 mit Herleitung als Datenfeld (P1) in `backend/app/data/catalog.py`.

Die Befunde 99 und 100, in Runde 15 noch zurückgestellt, sind seit Runde 19 geschlossen (99 entschieden vom
methodik_manager, 100 behoben in T-1233). Eingetragen mit T-1334-methodik_manager; am Bericht ändert sich nur die
Statuszeile (ABNAHMEREIF, abgenommen am 26.09.2026, `MANAGER-REVIEW: ABGENOMMEN`).

## Runde 31 — Divergenzen aus der Integration (T-1506, 27.09.2026): neue Befunde 136–153, 9 behoben, 9 zurückgestellt

Anlass: Vorhaben T-1438-cmo (Eltern T-1351-ceo), Nachträge des CEO vom 26.09.2026 um 11:40, 14:20, 14:35 und 19:10 UTC
mit den Divergenzen (i)–(xiv), D1, D2 und den fehlenden Sensitivitäten, dazu Quelle [15]; Ticket T-1506-methodik_manager
(Ersatz für T-1493-methodik_manager), Entscheidungen des methodik_manager dort. Schritt B nach `.claude/methodik-loop.md`:
erst die Befunde, dann die Revision. **Zählung nach A-0046:** ab der Null-Runde 30 ist Runde 31 die erste Runde, die
Grenze ist Runde 40.

| Divergenz | Befund | Lage |
|---|---|---|
| (i) Kennzeichnung `berechnet` | 136 | behoben |
| (ii) `berechnet` bei der Gewissheit | 137 | behoben |
| (iii) Voreinstellung s_gek | 138 | zurückgestellt, T-1534-cmo, Paket 2 |
| (iv) öffentliche Kühlzentren (Log 44) | 139 | zurückgestellt, T-1534-cmo, Paket 2 |
| (v) Toleranz Warmsen | 140 | behoben |
| (vi) ohne Gemeindeschlüssel, 2/7, Zellvergleich | 141 | behoben |
| (vii) HEV-Indikatoren und Rückfallpfad | 142 | behoben (Entscheidung, Umsetzung beim CTO) |
| (viii) Quellenarchiv [47], [70] | 143 | zurückgestellt, Archiv in T-1494-methodik_manager, geschlossen in T-1534-cmo, Paket 3 |
| (ix) Wochenquantile | 144 | behoben |
| (x) Lage der Toleranz Berlin | 145 | behoben |
| (xi) s_gek und h_Heim | 146 | zurückgestellt, T-1534-cmo, Paket 2 |
| (xii) S158 und Band von heat.c_kal | 147 | behoben |
| (xiii) Kühlzentren nach P2 | 148 | zurückgestellt, T-1534-cmo, Paket 2 |
| (xiv) S157 im Anpassungspotenzial | 149 | zurückgestellt, T-1534-cmo, Paket 2 |
| D1 Doppelzählungs-Wächter | 150 | zurückgestellt, T-1534-cmo, Paket 3 |
| D2 Kappung 0,794 | 151 | zurückgestellt, T-1534-cmo, Paket 3 |
| Sensitivitäten f_alter und l_restlebenserwartung | 152 | zurückgestellt, T-1534-cmo, Paket 3 |
| Quelle [15] | 153 | behoben |

**Gemessen am 27.09.2026** mit `docs/methodik/anlagen/95_zellvergleich.py --ersatz` (Berlin `--gemeinde 11000000`,
Warmsen `--gemeinde 03256034`), einmal mit der Tabelle aus §3.2 (Vorgabe) und einmal mit `--wochenquantile produkt`
(`wochenquantile_region.csv`, vier Nachkommastellen):

| Größe | Berlin, Tabelle §3.2 | Berlin, Datei | Warmsen, Tabelle §3.2 | Warmsen, Datei |
|---|---|---|---|---|
| Kette (ein Punkt) | 362,89 Mio. € | 362,80 Mio. € | 177.406 € | 177.209 € |
| Zelllauf mit Gemeindeschlüssel (Stufe 1 und 2) | 342,67 Mio. € | 342,58 Mio. € | 173.099 € | 172.957 € |
| Zelllauf ohne Gemeindeschlüssel (nur Stufe 1) | 338,84 Mio. € | 338,75 Mio. € | 145.025 € | 144.906 € |
| Einwohner ab 65 ohne / mit Gemeindeschlüssel | 696.648 / 707.318 | gleich | 544 / 697 | gleich |
| Faktor ohne gegen mit Gemeindeschlüssel | × 0,989 | × 0,989 | × 0,838 | × 0,838 |
| Spanne des Faktors (60–66 ganz oder gar nicht) | × 0,927–1,000 | gleich | × 0,651–0,947 | gleich |
| Wirkung (c) im Zellvergleich | × 0,984 = 0,9888 × 0,9948 | gleich | | |

Die Spalte „heute“ des Skripts enthält seit T-1364-cto Stufe 1 (Berlin 694.397 + 2.252 (Stufe 1), gerundet 696.648;
Warmsen 508 + 36 = 544 Einwohner ab 65), weil das Skript die Zellen über `zensus_loader.apply_zensus_to_cell_inputs`
ohne Gemeindeschlüssel lädt. Das ist genau die Modellgrenze ohne Gemeindeschlüssel.

**Nacharbeit 1 nach Urteil 2026-09-27T08:07:00Z** (T-1506, Nacharbeitsrunde 2 des Tickets): §3.3 beschreibt die
Modellgrenze jetzt an allen Stellen als „ohne Gemeindeschlüssel (nur Stufe 1)“: Einleitung der Ersatzregel, Satz vor der
Tabelle, Absatz „Was eine einfachere Rechnung verfälschen würde“ (Warmsen 544 und × 0,838 ohne Gemeindeschlüssel; 508
und × 0,800 nur als frühere Produktlogik vor Stufe 1, Messung vom 25.09.2026 in Runde 19; Berlin bei 0/7 × 1,000,
696.649 gegen 696.648 Einwohner ab 65, gemessen am 27.09.2026 mit `--gemeinde 11000000 --ersatz`). Log 41 kennzeichnet
die verworfene Variante als „frühere Produktlogik vor Stufe 1, Historie“, damit die Bindung (c) unten trägt. Der
Toleranzsatz rechnet 362,9 × 0,934 / 0,9888 = 342,8 und nennt 342,9 mit dem ungerundeten Produkt 0,9343 der vier
gerundeten Faktoren (0,948 × 0,981 × 0,984 × 1,021 = 0,93433). Kein Betrag und keine Prüfzahl ändert sich.

**Nacharbeit nach Urteil 2026-09-27T09:22:29Z (T-1534)** (T-1536-methodik_manager, Paket 1 von T-1534-cmo, Ersatz für
T-1506): Die Toleranz in §3.3 und Befund 140 nennt jetzt die ungerundete Quote, „± 0,29 % des Betrags (1 Mio. € /
342,67 Mio. € = 0,2918 %)“; 0,2918 % × 173.099 € = 505 €. Die Termine der neun zurückgestellten Befunde zeigen nicht
mehr auf die abgebrochenen T-1495 und T-1496, sondern auf die Ersatzpakete: „T-1534-cmo, Paket 2“ für 138, 139, 146,
148 und 149, „T-1534-cmo, Paket 3“ für 143 und 150–152. Registry und Tests spiegeln Kapitel 7: `_HEAT_BLOECKE` in
`backend/app/services/engine/impact/params.py` ordnet den bestehenden Parameter
`risks.EXPECTED_ANNUAL_MORTALITY.impact.anteil_60_66_ab65` dem Block `heat.anteil_60_66` zu (kein neuer Parameter),
`_HEAT_KLASSE` führt ihn als `abgeschaetzt` und `heat.beta_iso` als `belegt`; die Tests zählen 24 Blöcke, 10 belegt,
12 abgeschätzt, 2 berechnet. Kein Betrag ändert sich.

**Zahlen, die sich mit Absicht ändern:** §3.0 Wirkung (c) × 0,984 = 0,9888 × 0,9948 statt × 0,982 = 0,9867 × 0,9948,
zusammen × 0,934 statt × 0,932, Zelllauf ohne Gemeindeschlüssel rund 339 statt 338 Mio. €, der Betrag für Berlin ist
der Zelllauf mit Gemeindeschlüssel (342,67 Mio. €), die Kette liegt rund 6 % darüber (statt „rund 7 %“ gegen 338);
§3.3 Tabelle Spalten „ohne Gemeindeschlüssel“ (Berlin 696.648, 338,84 Mio. €, × 0,989, × 0,927–1,000; Warmsen 544,
145.025 €, × 0,838, × 0,651–0,947); Absatz „Was eine einfachere Rechnung verfälschen würde“ und Log 41 entsprechend;
Kapitel 7 bekommt den Block `heat.anteil_60_66` (24 statt 23 Blöcke); `heat.beta_iso` wird `quelle`.
**Unverändert:** die Kette (Berlin 362,9 Mio. €), der Zelllauf mit Gemeindeschlüssel (Berlin 342,67 Mio. €, Warmsen
173.099 €), S157 (25,0 Mio. €), Schutzprogramme (11,7 Mio. €). Weil sich kein Betrag der Methodik ändert, bleibt der
Statuskopf; die Gegenprüfung dieser Runde steht aus.

**Abweichung von der Entscheidung zu (ix), begründet:** Die Entscheidung lautet „Die Kette rechnet mit
`wochenquantile_region.csv`“. Umgesetzt ist: Rechengrundlage des Betrags ist die Datei, und §3.2 und §3.3 nennen die
Beträge mit der Datei (Berlin 342,58 Mio. €, Warmsen 172.957 €). Die Rechenkette §3.0 und die Tabelle in §3.3 rechnen
weiter mit der auf zwei Stellen gerundeten Tabelle als Lesehilfe; beide Fassungen stehen mit Zahl im Bericht. Grund:
Mit vier Stellen änderte sich die Kette um 0,03 % (362,80 statt 362,89 Mio. €), Ebene 4 in der gezeigten Genauigkeit
gar nicht (0,289 · 0,486 · 0,524 · 0,860), Ebene 6 in der letzten Stelle (153,5 statt 153,6; 277,3 statt 277,4),
Ebene 8 um 0,1 Mio. €; S157 (25,0 Mio. €) und Schutzprogramme (11,7 Mio. €) bleiben gleich. Dreizehn Quantile mit vier
Stellen machen Ebene 4 schwerer nachzurechnen, ohne dass sich eine Aussage ändert (Aufgabe §8, E2). Wer die Kette mit
der Datei rechnen will, bekommt die Zahlen aus dem Satz in §3.2. Entscheidet der methodik_manager anders, zieht die
Kette in allen Ebenen und in §5 nach (153,5; 277,3; 361,7; 362,8 Mio. €).

**Bindungstabelle (geänderter Entscheidungslog):**

| Abgeleitete Zahl oder Aussage | Stelle | Bindung |
|---|---|---|
| `berechnet` nur \(c_{\text{kal}}\) und \(\beta_{\text{pfl}}\), \(\beta_{\text{iso}}\) ist `quelle` | Log 40 Spalte Entscheidung; Kapitel 7 Absatz „Kennzeichnung `berechnet`“; Block `heat.beta_iso` | (a) wortgleich |
| Faktor ohne gegen mit Gemeindeschlüssel Berlin × 0,989, Warmsen × 0,838 | Log 41 Spalte Wirkung; §3.3 Tabelle; §3.3 „Was eine einfachere Rechnung verfälschen würde“ | (a) wortgleich |
| Spanne Warmsen × 0,651–0,947, Berlin × 0,927–1,000 | Log 41 Gegenargument (1); §3.3 Tabelle; §3.3 „Was eine einfachere Rechnung verfälschen würde“ | (a) wortgleich |
| 2/7 als Block | Log 41 Gegenargument (1); §3.3 Schritt 1; Block `heat.anteil_60_66` | (b) Verweis auf den Block |
| „65+ = 0 lassen … 508 gegen 602 ab 67“ | Log 41 verworfene Variante, dort gekennzeichnet „frühere Produktlogik vor Stufe 1, Historie“; §3.3 „Was eine einfachere Rechnung verfälschen würde“ (508, × 0,800, „frühere Produktlogik vor Stufe 1“) | (c) Historie: beschreibt die Produktlogik vor T-1364-cto; die Zahl bleibt für diese Variante richtig |
| 305.088 € gegen 138.543 € | §3.3 Absatz zu Befund 117 | (c) Historie: Messung der früheren Fassung, dort schon so gekennzeichnet |

| Nr | Stelle | Art | Begründung | Vorschlag | Kat. | Prüfausdruck | Status |
|---|---|---|---|---|---|---|---|
| 136 | Kapitel 7 Blöcke `heat.c_kal`, `heat.beta_iso`, `heat.beta_pfl`; Log 40 | Kennzeichnung widerspricht der eigenen Definition (P1) | Log 40 definiert `berechnet` als „Wert folgt aus anderen Blöcken“; das Produkt zeigt „berechnet aus amtlichen Daten“. Geprüft je Block: \(c_{\text{kal}}\) ist der Fit des Modells aus fünf Blöcken gegen die RKI-Reihe [50], folgt also aus anderen Blöcken. \(\beta_{\text{pfl}}\) folgt aus der Kette §3.3b mit \(m_{85+}\) und \(\bar q_{\text{pfl}}\) (zwei Blöcke) und den Werten aus Fouillet [60] und WIdO [61]. \(\beta_{\text{iso}}\) ist die Odds Ratio 2,3 aus Semenza 1996 [40], nur umgerechnet mit dem amtlichen Anteil \(\bar q_{\text{1P}}\) [63]; das ist nach Log 40 eine Rechnung aus gemessenen Zahlen ohne Setzung | Entscheidung methodik_manager: `berechnet` nur für \(c_{\text{kal}}\) und \(\beta_{\text{pfl}}\); `heat.beta_iso` wird `quelle` mit Semenza [40] und Mikrozensus [63]; Log 40 nachziehen; Anzeigetext im Produkt „berechnet aus anderen Parametern“, weil bei beiden berechneten Blöcken nicht alle Eingänge amtlich sind | B | `grep -qF 'kennzeichnung: quelle   # (OR-1)/[1+q(OR-1)] mit OR 2,3 aus Semenza 1996' docs/methodik/95_hitzebelastung.md && grep -qF 'berechnet aus anderen Parametern' docs/methodik/95_hitzebelastung.md && ! grep -qF '(\(c_{\text{kal}}\), \(\beta_{\text{iso}}\), \(\beta_{\text{pfl}}\))' docs/methodik/95_hitzebelastung.md` | behoben (T-1506): `heat.beta_iso` `quelle`; Absatz „Kennzeichnung `berechnet`“ vor den Blöcken in Kapitel 7; Log 40 nennt nur noch \(c_{\text{kal}}\) und \(\beta_{\text{pfl}}\); Anzeigetext für den CTO in der Übernahmeliste |
| 137 | Kapitel 7 Absatz „Kennzeichnung `berechnet`“ | Regel fehlt (Gewissheit, Unsicherheits-Zusammenschau) | Das Produkt zählt `berechnet` vorläufig wie „belegt“ (T-1363-cto). Ob ein berechneter Wert belegt oder abgeschätzt ist, hängt an seinen Eingängen | Entscheidung methodik_manager: Für #95 erbt `berechnet` die schwächste Kennzeichnung seiner Eingangsblöcke. \(c_{\text{kal}}\): Eingänge \(\beta_{85+}\) (Süd-Nachschätzung) und \(f_a\) sind `abschaetzung_kap3`, also abgeschätzt. \(\beta_{\text{pfl}}\): \(m_{85+}\) und \(\bar q_{\text{pfl}}\) sind `quelle`, also belegt. Gewissheitsstufe im Produkt, gemessen mit `gewissheit.gewissheitsstufe` am 27.09.2026: Hitzemortalität 16 von 32 Parametern belegt oder berechnet, Stufe „mittel“. Nach der Regel zählen `beta_iso` (jetzt `quelle`) und `beta_pfl` weiter, `calibration` (\(c_{\text{kal}}\)) nicht mehr: 15 von 32, Anteil 0,47, Stufe „gering“. Die Stufe von #95 ändert sich also, sobald die Regel gilt. Die Regel für alle Klimawirkungen gehört in die Querschnittsfrage Gewissheit (T-1117-cmo); bis dahin gilt die vorläufige Regel des Produkts, `berechnet` zählt wie „belegt“, und die Stufe bleibt „mittel“ | B | `grep -qF 'erbt die schwächste Kennzeichnung' docs/methodik/95_hitzebelastung.md && grep -qF 'bis dahin zählt das Produkt' docs/methodik/95_hitzebelastung.md` | behoben (T-1506): Absatz in Kapitel 7 mit beiden Blöcken, ihrer geerbten Kennzeichnung und der vorläufigen Regel; die Wirkung auf die Stufe (mittel, mit der Regel gering) steht hier, die risikoübergreifende Regel liegt bei der Querschnittsfrage |
| 138 | §5 Hebel S157 (\(s_{\text{gek}}\)), Log 44, Kapitel 7 | Nullwirkung ohne Eingabe (P2) | Ohne Eingabe der Kommune bleibt S157 ohne Betrag; das ist eine Nullwirkung gegen P2 (A-0010) | Entscheidung methodik_manager: \(s_{\text{gek}}\) wird Registry-Parameter mit Voreinstellung nach P2 für die ganze Kommune (Block `heat.s_gek`, Zahlenwert, Band, Herleitung, `abschaetzung_kap3`) | B | `grep -qF 'id: heat.s_gek' docs/methodik/95_hitzebelastung.md` | zurückgestellt (Termin: T-1534-cmo, Paket 2): Voreinstellung nach P2 mit Parameter-Block; bis dahin gilt im Produkt die Hausregel (S157 ohne Eingabe ohne Betrag, mit Hinweis) |
| 139 | Log 44, §5 Hebel S157 | Nullwirkung (P2), Zusage ohne Umsetzung | Log 44 verlangt beim Aktivieren von S157 eine eigene Abschätzung nach P2 für öffentliche Kühlzentren; der Bericht enthält sie nicht | Entscheidung methodik_manager: Abschätzung nach P2 für öffentliche Kühlzentren mit Parameter-Block (Zahlenwert, Band, Sensitivität), Personenkreis außerhalb der Heime | B | `grep -qF 'id: heat.delta_kuehlzentren' docs/methodik/95_hitzebelastung.md` | zurückgestellt (Termin: T-1534-cmo, Paket 2): Abschätzung nach P2 mit Block `heat.delta_kuehlzentren`; mit 148 zusammen |
| 140 | §3.3 Tabelle der Beispielkommunen, §3.0 Prüfblock | Toleranz fehlt (§3.3) | Das Produkt überträgt die Toleranz aus §3.0 (< 1 Mio. € für Berlin) relativ auf Warmsen (± 505 €); der Bericht nennt keine Toleranz in §3.3 | Entscheidung methodik_manager: eine Toleranz, relativ, für Berlin und Warmsen, in §3.3 mit Lage und Größe. Gemessen: 1 Mio. € / 342,67 Mio. € = 0,2918 %, gerundet 0,29 %; 0,2918 % × 173.099 € = 505 € (mit der gerundeten Quote 0,29 % wären es 502 €). Bestätigt: ± 505 € um 173.099 € | B | `grep -qF '0,29 % des Betrags' docs/methodik/95_hitzebelastung.md && grep -qF '(1 Mio. € / 342,67 Mio. € = 0,2918 %)' docs/methodik/95_hitzebelastung.md && grep -qF '± 505 €' docs/methodik/95_hitzebelastung.md` | behoben (T-1506): §3.3 nennt die Toleranz ± 0,29 % des Betrags mit Kommazahl, Berlin ± 1 Mio. € um 342,67 Mio. €, Warmsen ± 505 € um 173.099 €; die Datei-Fassung (342,58 Mio. €, 172.957 €) liegt darin; Nacharbeit nach Urteil 2026-09-27T09:22:29Z (T-1534): ungerundete Quote 0,2918 % neben 0,29 %, damit 505 € nachrechenbar ist |
| 141 | §3.0 Wirkung (c), §3.3 Stufe 2, Tabelle und Absatz „Was eine einfachere Rechnung verfälschen würde“, Log 41, Kapitel 7 | Modellgrenze nicht genannt; Zahl ohne Block (P1); Skript und Bericht auseinander | (a) Ohne Gemeindeschlüssel (Kommune kein Gemeindeteil der VG250) rechnet das Produkt nur Stufe 1. (b) 2/7 hat keinen Parameter-Block. (c) Die Spalte „heute“ des Skripts enthält seit T-1364-cto Stufe 1: Berlin 694.397 + 2.252 (Stufe 1), gerundet 696.648 Einwohner ab 65, Warmsen 508 + 36 = 544; der Bericht nannte die alten Werte | Entscheidung methodik_manager: Modellgrenze mit Wirkung auf den Betrag nennen; Block für 2/7; Skript ausführen, die gemessene Seite gilt. Umgesetzt im Bericht (das Skript misst richtig, nur seine Beschriftung „65+ = 0“ ist veraltet, siehe Beobachtung im Ergebnis) | B | `grep -qF 'id: heat.anteil_60_66' docs/methodik/95_hitzebelastung.md && grep -qF '696.648' docs/methodik/95_hitzebelastung.md && grep -qF '145.025 €' docs/methodik/95_hitzebelastung.md && grep -qF 'ohne Gemeindeschlüssel' docs/methodik/95_hitzebelastung.md && ! grep -qF '\| 694.397 \| 707.318 \|' docs/methodik/95_hitzebelastung.md && ! grep -qF '0,9867' docs/methodik/95_hitzebelastung.md && ! grep -qF 'Heute setzt das Produkt 65+ = 0' docs/methodik/95_hitzebelastung.md && ! grep -qF 'Regel über dem heutigen' docs/methodik/95_hitzebelastung.md && grep -qF 'frühere Produktlogik vor Stufe 1, Historie' docs/methodik/95_hitzebelastung.md` | behoben (T-1506): §3.3 Modellgrenze „ohne Gemeindeschlüssel nur Stufe 1“ mit Wirkung Berlin × 0,989 (338,84 statt 342,67 Mio. €), Warmsen × 0,838 (145.025 statt 173.099 €); Tabelle und Log 41 gemessen; §3.0 (c) × 0,984 = 0,9888 × 0,9948, Prüfblock nachgezogen; Block `heat.anteil_60_66` 0,2857 (Band 0–1, `abschaetzung_kap3`); Nacharbeit 1 nach Urteil 2026-09-27T08:07:00Z: die übrigen Stellen in §3.3 und die verworfene Variante in Log 41 auf „ohne Gemeindeschlüssel (nur Stufe 1)“ bzw. „frühere Produktlogik vor Stufe 1, Historie“, Prüfausdruck um diese Stellen erweitert |
| 142 | §3.3 Ersatzregel | Zwei Rechenwege für dieselbe Größe (P3, eine Methodik) | HEV-Indikatoren (`auxiliary.py`, `indicators.py`) und der Rückfallpfad `health._age_bands` lesen den veröffentlichten Anteil ab 65, nicht den Ersatzwert | Entscheidung methodik_manager: ja, Screening und Rückfallpfad nutzen denselben Ersatzwert, weil es eine Methodik ist; Satz in §3.3; Umsetzung beim CTO | B | `grep -qF 'auch die Hitze-Kennzahlen der Übersicht und der Rückfallpfad' docs/methodik/95_hitzebelastung.md` | behoben (T-1506): Satz in §3.3; Umsetzung in der Übernahmeliste an den CTO |
| 143 | Quellen [47] und [70], `docs/quellen/methodik/95/QUELLEN.md` | Quellenarchiv unvollständig (eiserne Regel 3) | Liotta u. a. 2018 ist [70] in #95 und gehört ins Archiv von #95; ebenso [47] | Entscheidung methodik_manager: Archiv in T-1494-methodik_manager, geschlossen mit T-1534-cmo, Paket 3 (Ersatz für das abgebrochene T-1496-methodik_manager) | B | `grep -qF '\| [47] \|' docs/quellen/methodik/95/QUELLEN.md && grep -qF '\| [70] \|' docs/quellen/methodik/95/QUELLEN.md` | zurückgestellt (Termin: T-1534-cmo, Paket 3; Archiv in T-1494-methodik_manager): `docs/quellen/methodik/95/` liegt nicht in diesem Paket; der Ausdruck ist seit T-1494 grün, Paket 3 schließt den Befund |
| 144 | §3.2 Wochenquantile, Zeichentabelle \(q_{w,\text{Region}}\) | Rechengrundlage unklar | Das Produkt rechnet mit `wochenquantile_region.csv` (vier Nachkommastellen), der Bericht mit der Tabelle in §3.2 (zwei). Gemessen: Berlin Kette 362,80 statt 362,89 Mio. €, Zelllauf 342,58 statt 342,67 Mio. €; Warmsen 172.957 statt 173.099 € | Entscheidung methodik_manager: Rechengrundlage ist die Datei, die Tabelle in §3.2 bleibt gerundete Lesehilfe. Für die Rechenkette §3.0 abweichend begründet (Kopf der Runde): sie bleibt Lesehilfe mit der gerundeten Tabelle, die Datei-Fassung steht mit Zahl daneben | B | `grep -qF 'Rechengrundlage ist die Datei' docs/methodik/95_hitzebelastung.md && grep -qF '342,58 Mio. €' docs/methodik/95_hitzebelastung.md && grep -qF '172.957 €' docs/methodik/95_hitzebelastung.md` | behoben (T-1506): §3.2 nennt die Datei als Rechengrundlage und die Tabelle als Lesehilfe mit den gemessenen Beträgen beider Fassungen; Zeichentabelle nachgezogen |
| 145 | §3.0 Prüfblock, §3.3 | Lage der Toleranz unklar | Der Golden-Test legt ± 1 Mio. € um 342,67 Mio. €, der Prüfblock in §3.0 um 343 nach Teilung durch 0,9867 | Entscheidung methodik_manager: ein Satz erklärt 362,9 gegen 342,67 gegen 343. Es ist dieselbe Zahl: 342,67 ist der Zelllauf mit ungerundeten Faktoren, 343 dieselbe Rechnung mit den auf drei Stellen gerundeten Faktoren der Kette (362,9 × 0,934 / 0,9888 = 342,8; mit dem ungerundeten Produkt 0,9343 der gerundeten Faktoren 342,9); 362,9 ist die Kette an einem Punkt | B | `grep -qF 'Teilung durch 0,9888' docs/methodik/95_hitzebelastung.md && grep -qF '/ 0.9888 - 343) < 1' docs/methodik/95_hitzebelastung.md` | behoben (T-1506): Satz in §3.3 unter der Toleranz; Prüfblock §3.0 teilt jetzt durch den gemessenen Faktor 0,9888; Nacharbeit 1 nach Urteil 2026-09-27T08:07:00Z: der Satz rechnet 342,8 mit 0,934 und 342,9 mit dem ungerundeten 0,9343 |
| 146 | §5 Hebel S157 (\(s_{\text{gek}}\), \(h_{\text{Heim}}\)), Zeichentabelle | Bezugsfläche und Parameter ohne Block (P1) | Gilt \(s_{\text{gek}}\) für die ganze Kommune? Rechnet \(h_{\text{Heim}}\) auf Zellebene mit \(q_{\text{pfl}}\) der Zelle statt mit dem Bundeswert 0,344? 0,344 hat keinen eigenen Block | Entscheidung methodik_manager: \(s_{\text{gek}}\) gilt für die ganze Kommune, unabhängig von der gezeichneten Fläche; 0,344 bekommt einen Parameter-Block (`heat.h_heim`); \(h_{\text{Heim}}\) auf Zellebene über \(q_{\text{pfl}}\), sofern \(q_{\text{pfl}}\) je Zelle vorliegt | B | `grep -qF 'id: heat.h_heim' docs/methodik/95_hitzebelastung.md && grep -qF 'id: heat.s_gek' docs/methodik/95_hitzebelastung.md` | zurückgestellt (Termin: T-1534-cmo, Paket 2): mit 138 zusammen |
| 147 | §5 Hebel Hitzeaktionsplan (S155/S158), Block `heat.c_kal` | Knotentyp und Band zwischen Skript und Bericht verschieden | Ist S158 eine Maßnahme oder nur \(\delta_{\text{HAP}}\)? Band von \(c_{\text{kal}}\): Skript 0,55–0,66, Bericht 0,55–0,67 | Entscheidung methodik_manager: In der Arbeitsmappe `KWRA-Schadensbaum_X_UBA-klimawirkungsketten.xlsx`, Blatt „Klimawirkungsketten“, ist S158 „Monitoring von Gesundheitsgefahren und Frühwarnsysteme“ ein Faktor der Sensitivität in der Oberkategorie „Präventationsmaßnahmen“ (so im Original) und hängt an W182 Hitzebelastung. S158 bleibt also eine Maßnahme, ihr Wirkungsparameter ist \(\delta_{\text{HAP}}\); der Knotentyp im Graphen ist Sache des CTO. Band gemessen: Die Kalibrierläufe [50] geben 0,661 ohne Süd-Nachschätzung (`c_kal_rev7_ergebnis.md` Z. 25) und 0,559 bei \(s_{\text{Süd}}\) = 1,85 (Z. 45); außenrundend 0,55–0,67. 0,66 schnitte die gemessene Stütze 0,661 ab; der Bericht gilt | B | `grep -qF 'band: [0.55, 0.67]' docs/methodik/95_hitzebelastung.md && grep -qF 'c_kal = 0.661' backend/data/kalibrierung/c_kal_rev7_ergebnis.md && grep -qF 'c = 0.559' backend/data/kalibrierung/c_kal_rev7_ergebnis.md && grep -qF '(S155/S158)' docs/methodik/95_hitzebelastung.md` | behoben (T-1506): Bericht unverändert richtig; Band 0,55–0,67 und S158 als Maßnahme mit \(\delta_{\text{HAP}}\) gehen in die Übernahmeliste an den CTO |
| 148 | Log 44, §5 | Nullwirkung (P2) | Die Abschätzung nach P2 für öffentliche Kühlzentren liefert der Methodik-Zweig, der CTO baut sie danach ein | Entscheidung methodik_manager: wie 139, Kühlzentren nach P2 | B | `grep -qF 'id: heat.delta_kuehlzentren' docs/methodik/95_hitzebelastung.md` | zurückgestellt (Termin: T-1534-cmo, Paket 2): mit 139 zusammen |
| 149 | §5 Hebel S157, Charakterisierung (Anpassungspotenzial) | Nullwirkung in der Charakterisierung (P2) | S157 zählt im Anpassungspotenzial mit Wirkung 0, weil `default_reduction` `None` ist (T-1367-cto); das Anpassungspotenzial sinkt gegenüber 0,18 | Entscheidung methodik_manager: S157 geht mit seiner Voreinstellung (\(1 - g_{\text{S157}}\) bei \(s_{\text{gek}}\) aus 138) in das Anpassungspotenzial ein; Anzeige und Quelle in der Parameterliste regelt T-1410-ceo | B | `grep -qF 'S157 mit seiner Voreinstellung' docs/methodik/95_hitzebelastung.md` | zurückgestellt (Termin: T-1534-cmo, Paket 2): hängt an der Voreinstellung aus 138 |
| 150 | §5 Hebel Hitzeaktionsplan, Doppelzählungs-Wächter | Eingabe fehlt | \(\delta_{\text{VG}}\) = 1, wenn das Schutzprogramm schon in den Kalibrierjahren bestand; ob die Kommune dafür eine Eingabe braucht und was bis dahin gilt, steht nicht da | Entscheidung methodik_manager: Eingabe der Kommune ja/nein mit begründeter Voreinstellung und Parameter-Block | B | `grep -qF 'id: heat.vg_in_kalibrierjahren' docs/methodik/95_hitzebelastung.md` | zurückgestellt (Termin: T-1534-cmo, Paket 3): Eingabe mit Voreinstellung — ersetzt durch die Zeile in Runde 31 (Befund 150, T-1538) |
| 151 | §5 Hebel Schutzprogramme (Kappung), Block `heat.delta_vg` | Wert begrenzt den Betrag ohne eigenen Block (P1) | Die Kappung 0,794 steht nur im Band von \(\delta_{\text{VG}}\); ein Wert, der den Betrag begrenzt, ist ein Parameter mit Herleitung | Entscheidung methodik_manager: Kappung 0,794 als eigener Parameter-Block nach P1 | B | `grep -qF 'id: heat.kappung_vg' docs/methodik/95_hitzebelastung.md` | zurückgestellt (Termin: T-1534-cmo, Paket 3): eigener Block |
| 152 | §4 Sensitivitäten, Blöcke `heat.f_alter` und `heat.l_restlebenserwartung` | Sensitivität ohne Zahl | Für \(f_a\) und \(\bar L_a\) nennt der Bericht keine Sensitivität als Zahl | Entscheidung methodik_manager: Sensitivitäten als Zahl in Mio. € für Berlin, gemessen wie die übrigen | B | `grep -qF 'Sensitivität von f_alter' docs/methodik/95_hitzebelastung.md && grep -qF 'Sensitivität von l_restlebenserwartung' docs/methodik/95_hitzebelastung.md` | zurückgestellt (Termin: T-1534-cmo, Paket 3): Messung beider Sensitivitäten |
| 153 | §8 Quelle [15] | Quellenangabe falsch (eiserne Regel 3) | [15] nannte „CC 26/2021“, „Kap. 4.2“; das Dokument `docs/quellen/methodik/96/15_UBA2021_KWRA_TB5_Wirtschaft_Gesundheit.md` trägt auf der Titelseite (Z. 14) „CLIMATE CHANGE 24/2021“; im Inhaltsverzeichnis (Z. 193–195) steht 4.2 „Klimawirkungen im Detail“ ab S. 153, 4.2.1 „Hitzebelastung“ S. 153, 4.2.2 ab S. 173 | [15] als Climate Change 24/2021, Kap. 4.2.1 Hitzebelastung, S. 153–172 | B | `! grep -qF '26/2021' docs/methodik/95_hitzebelastung.md && grep -qF 'Climate Change 24/2021), Kap. 4.2.1 Hitzebelastung, S. 153–172' docs/methodik/95_hitzebelastung.md` | behoben (T-1506): [15] berichtigt |
| 105 | §3.0, Liste der Zusammenfassungen | Fortschreibung des Prüfausdrucks (Befund 141) | Der Ausdruck prüft „0,982 … = 0,932“; nach der Messung vom 27.09.2026 ist (c) × 0,984 | Ausdruck mit „0,984 … = 0,934“ | B | `grep -q '0,948 × 0,981 × 0,984 × 1,021 = 0,934' docs/methodik/95_hitzebelastung.md` | behoben, Prüfausdruck fortgeschrieben in Runde 31 wegen Befund 141 (T-1506) |
| 111 | Kapitel 7, alle Blöcke | Fortschreibung des Prüfausdrucks (Befund 141) | Kapitel 7 hat mit `heat.anteil_60_66` 24 statt 23 Blöcke | Ausdruck mit 24 Blöcken | B | `python3 -c "import re,sys; s=open('docs/methodik/95_hitzebelastung.md',encoding='utf-8').read(); b=s[s.index('## 7 '):s.index('## 8 ')].split('parameter:')[1:]; sys.exit(not (len(b) == 24 and all(re.search(r'^ *kennzeichnung: (\S+)', x, re.M).group(1) in ('quelle', 'abschaetzung_kap3', 'berechnet') for x in b) and all(re.search(r'^ *abgeleitet_aus: .heat', x, re.M) for x in b if 'kennzeichnung: berechnet' in x)))"` | behoben, Prüfausdruck fortgeschrieben in Runde 31 wegen Befund 141 (T-1506) |
| 115 | §3.0, Wirkungen (b)–(d) und Beispiel-Block rechenkette_95 | Fortschreibung des Prüfausdrucks (Befund 141) | Der Ausdruck prüft „Produkt: × 0,982“; (c) heißt jetzt „ohne Gemeindeschlüssel: × 0,984“ | Ausdruck mit „Gemeindeschlüssel: × 0,984“ | B | `python3 -c "import sys; s=open('docs/methodik/95_hitzebelastung.md',encoding='utf-8').read(); t=s[s.index('### 3.0'):s.index('### 3.1')]; sys.exit(not ('Einwohnersumme: × 0,981' in t and 'Gemeindeschlüssel: × 0,984' in t and 'unter 1 km: × 1,021' in t and '3_593_357' in t and '3.595.270' not in t and 'python3 docs/methodik/anlagen/95_zellvergleich.py --gemeinde 11000000' in t))"` | behoben, Prüfausdruck fortgeschrieben in Runde 31 wegen Befund 141 (T-1506) |

### Fortsetzung Runde 31, Teil 2

S157-Strang, T-1537-methodik_manager (Paket 2 von T-1534-cmo, Ersatz für T-1495-methodik_manager), 27.09.2026.
Eingelöst werden die Befunde 138, 139, 146, 148 und 149 mit den Entscheidungen des methodik_manager aus der
Tabelle oben; Wortlaut der Divergenzen (iii), (iv), (xi), (xiii) und (xiv) in T-1351-ceo, Nachträge 11:40, 14:20 und
14:35 Uhr. **Zählung nach A-0046:** keine neue Runde, die Arbeit gehört zu Runde 31. Die Befunde 143, 150, 151 und 152
bleiben für Paket 3 zurückgestellt, 116 beim cto.

**Was sich ändert.** Kapitel 7 hat drei neue Blöcke (27 statt 24): `heat.s_gek` 0,11 (Band 0,05–0,15,
`abschaetzung_kap3`), `heat.h_heim` 0,344 (Band 0,275–0,517, `berechnet` aus `heat.qbar_pfl` und `heat.beta_pfl`,
Quelle [61]) und `heat.delta_kuehlzentren` 0,9956 (Band 0,982–0,9994, `abschaetzung_kap3`). §5 hat beim Hebel S157 die
Voreinstellung, \(h_{\text{Heim}}\) je Zelle und die Formelzeile für das Anpassungspotenzial, dazu den neuen Hebel
„Öffentliche Kühlzentren“; Zeichentabelle, Evidenz-Register (neue Zeile 95-S157-02), Knoten-Bilanz S157, Kapitel 1 (b),
Quellen [41] (ergänzt), [71]–[73] (neu) und Entscheidungslog (Nr. 44 fortgeschrieben, Nr. 45 und 46 neu) ziehen mit. Neue
Beispiel-Blöcke `s157_voreinstellung` und `kuehlzentren_berlin`. Die Tests führen die drei neuen Kennungen in
`_AUSSTEHEND_CTO` (kein Registry-Parameter, der CTO legt sie an). Weil der Hebel S157 jetzt ohne Eingabe einen Betrag
rechnet und ein neuer Hebel dazukommt, steht der Statuskopf auf „in Revision“.

**Nachgerechnet:** §3.0 und der Beispiel-Block `rechenkette_95` laufen unverändert grün (Lint); die Kette bleibt
362,9 Mio. €, der Zelllauf Berlin 342,67 Mio. €, Warmsen 173.099 €, weil die Hebel nur wirken, wenn eine Kommune die
Maßnahme wählt. Gemessen am 27.09.2026 mit `docs/methodik/anlagen/95_zellvergleich.py --ersatz` (YLL je Band des
Zelllaufs mit Gemeindeschlüssel, Tabelle §3.2): Berlin 75–84 637,67 YLL, 85+ 556,27 YLL (133,72 Todesfälle 85+);
Warmsen 75–84 0,2905 YLL, 85+ 0,2398 YLL, gesamt 1,0713 YLL.

| Größe (Beträge je Jahr, Preisstand 2024) | Berlin, Kette | Berlin, Zelllauf | Warmsen, Zelllauf |
|---|---|---|---|
| S157, alle Heimplätze gekühlt (\(s_{\text{gek}}\) = 1) | 25,0 Mio. € (unverändert) | 21,8 Mio. € | 9.379 € |
| S157 bei der Voreinstellung \(s_{\text{gek}}\) = 0,11 | 2,7 Mio. € (Band 1,2–3,7 Mio. €) | 2,4 Mio. € | 1.032 € (Band 469–1.407 €) |
| Öffentliche Kühlzentren, \(\delta_{\text{KZ}}\) = 0,9956 | 0,75 Mio. € (Band 0,1–3,0 Mio. €) | 0,72 Mio. € | 320 € |
| Anteil 85+ an den YLL \(a_{85+}\) | 0,284 | 0,262 | 0,224 |
| Anpassungspotenzial Hitzemortalität mit S157 | 0,057 (heute 0,050) | — | 0,056 |

**Bindungstabelle (geänderter Entscheidungslog):**

| Abgeleitete Zahl oder Aussage | Stelle | Bindung |
|---|---|---|
| \(s_{\text{gek}}\) = 0,11 (Band 0,05–0,15), 11 % aus [71], 14,5 % aus [72] | Log 45; §5 Voreinstellung; Zeichentabelle \(s_{\text{gek}}\); Register 95-S157-01; Block `heat.s_gek` | (a) wortgleich |
| S157 Berlin 2,7 Mio. € (1,2–3,7 Mio. €), Warmsen 1.032 € | Log 45 Spalte Auswirkung; §5 Sensitivität; Beispiel-Block `s157_voreinstellung` | (a) wortgleich |
| \(h_{\text{Heim},z}\) mit Rückfallwert 0,344 | Log 45; §5 „\(h_{\text{Heim}}\) je Zelle“; Zeichentabelle | (b) Verweis auf den Block `heat.h_heim` |
| \(r_{\text{S157}}\) = 0,284 × 0,344 × 0,11 × 0,706 = 0,0076; Anpassungspotenzial 0,057, Warmsen 0,056 | Log 45; §5 „S157 mit seiner Voreinstellung im Anpassungspotenzial“ | (a) wortgleich |
| \(\delta_{\text{KZ}}\) = 0,9956 (0,982–0,9994), \(w_{\text{KZ}}\) = 0,71 × 3/24 = 0,089, \(r_{\text{KZ}}\) = 0,05 | Log 46; §5 Kühlzentren; Zeichentabelle; Register 95-S157-02 | (b) Verweis auf den Block `heat.delta_kuehlzentren` |
| Kühlzentren Berlin 0,75 Mio. € (0,1–3,0 Mio. €), Warmsen 320 €, einfachere Rechnung 6,0 Mio. € | Log 46 Spalten Alternative und Auswirkung; §5 Kühlzentren; Beispiel-Block `kuehlzentren_berlin` | (a) wortgleich |
| „Die Maßnahme bleibt im Produkt geparkt … \(s_{\text{gek}}\), den die Kommune eingibt … beim Aktivieren eine eigene Abschätzung nach P2“ | Log 44, gekennzeichnet „Stand 26.09.2026, Historie; fortgeschrieben durch Nr. 45 und 46“; §5 „Stand im Produkt (Befund 130, fortgeschrieben mit Befund 138)“ | (c) Historie: beschreibt den Stand vor T-1367-cto und vor der Voreinstellung |

| Nr | Stelle | Art | Begründung | Vorschlag | Kat. | Prüfausdruck | Status |
|---|---|---|---|---|---|---|---|
| 138 | §5 Hebel S157 (\(s_{\text{gek}}\)), Log 44/45, Kapitel 7 | Nullwirkung ohne Eingabe (P2) | Ohne Eingabe der Kommune blieb S157 ohne Betrag | Entscheidung methodik_manager (Runde 31): Voreinstellung nach P2 für die ganze Kommune, Block `heat.s_gek`. Umgesetzt: \(s_{\text{gek}}\) = 11 % der Pflegeheime mit Klimaanlage [71] × 1 = 0,11, Band 0,05–0,15 (oben 14,5 % der Neubauten des Sozialwesens 2025 [72]), `abschaetzung_kap3`; Sensitivität Berlin (Kette) 2,7 Mio. € je Jahr (1,2–3,7 Mio. €, 0,3–1,0 % des Jahresbetrags), Zelllauf 2,4 Mio. €, Warmsen 1.032 € | B | `python3 -c "import sys; s=open('docs/methodik/95_hitzebelastung.md',encoding='utf-8').read(); k=s[s.index('## 7 '):s.index('## 8 ')]; b=k.split('id: heat.s_gek')[1].split('parameter:')[0]; t=s[s.index('## 5 '):s.index('## 6 ')]; sys.exit(not ('wert: 0.11' in b and 'band: [0.05, 0.15]' in b and 'kennzeichnung: abschaetzung_kap3' in b and '= 0,11 (Abschätzung von KAP3, Block' in t and 'Nullwirkung ist keine Voreinstellung (P2)' in t and '25,0 Mio. € × 0,11 = **2,7 Mio. €' in t and 'python test: s157_voreinstellung' in s and '[72]** Statistisches Bundesamt' in s))"` | behoben (T-1537): Block `heat.s_gek`, Absatz „Voreinstellung“ in §5 mit Band, Sensitivität und Modellgrenze, Log 45, Quellen [71] und [72]; Registry-Parameter beim CTO (`_AUSSTEHEND_CTO`) |
| 139 | Log 44/46, §5 Hebel Kühlzentren, Kapitel 7 | Nullwirkung (P2), Zusage ohne Umsetzung | Log 44 sagte eine eigene Abschätzung für öffentliche Kühlzentren zu; sie fehlte | Entscheidung methodik_manager (Runde 31): Abschätzung nach P2 mit Block, Personenkreis außerhalb der Heime. Umgesetzt: \(\delta_{\text{KZ}}\) = 1 − 0,05 × 0,71 × 3/24 = 0,9956 (Band 0,982–0,9994) auf den Exzess der Bänder 75–84 und 85+ ohne Heimbewohner; Wirkung im gekühlten Raum aus [46], Dauer der Kühlwirkung aus [73], Reichweite Setzung von KAP3, plausibilisiert an [41]; Berlin (Kette) 0,75 Mio. € je Jahr (0,1–3,0 Mio. €), Zelllauf 0,72 Mio. €, Warmsen 320 €; stärkster Treiber die Reichweite | B | `python3 -c "import sys; s=open('docs/methodik/95_hitzebelastung.md',encoding='utf-8').read(); k=s[s.index('## 7 '):s.index('## 8 ')]; b=k.split('id: heat.delta_kuehlzentren')[1].split('parameter:')[0]; t=s[s.index('## 5 '):s.index('## 6 ')]; sys.exit(not ('wert: 0.9956' in b and 'band: [0.982, 0.9994]' in b and 'kennzeichnung: abschaetzung_kap3' in b and 'abgeleitet_aus: [heat.g_s157]' in b and 'Öffentliche Kühlzentren (Knoten S157' in t and '**0,75 Mio. € je Jahr**' in t and 'python test: kuehlzentren_berlin' in s and 'Welche Wirkung haben öffentliche Kühlzentren außerhalb der Heime (Log 44' in s and '[73]** R. D. Meade' in s))"` | behoben (T-1537): Hebel „Öffentliche Kühlzentren“ in §5, Block `heat.delta_kuehlzentren`, Log 46, Register 95-S157-02, Quelle [73]; mit 148 zusammen |
| 146 | §5 Hebel S157 (\(s_{\text{gek}}\), \(h_{\text{Heim}}\)), Zeichentabelle, Kapitel 7 | Bezugsfläche und Parameter ohne Block (P1) | \(s_{\text{gek}}\) ohne Bezugsfläche; \(h_{\text{Heim}}\) nur als Bundeswert 0,344 ohne eigenen Block | Entscheidung methodik_manager (Runde 31): \(s_{\text{gek}}\) für die ganze Kommune; Block für 0,344; Zellebene, sofern \(q_{\text{pfl}}\) je Zelle vorliegt. Umgesetzt: \(q_{\text{pfl}}\) liegt je Zelle vor (Ebene `CARE_HOME_SHARE_85P`, Log 35), deshalb \(h_{\text{Heim},z} = q_{\text{pfl},z}\,[1 + \beta_{\text{pfl}}(1 - \bar q_{\text{pfl}})] / [1 + \beta_{\text{pfl}}(q_{\text{pfl},z} - \bar q_{\text{pfl}})]\), Rückfallwert 0,344 (Zelle mit \(q_{\text{pfl}}\) = 0,5: 0,75); Block `heat.h_heim` 0,344, Band 0,275–0,517, `berechnet` mit Quelle [61]; Modellgrenze „unabhängig von der gezeichneten Fläche“ in §5 | B | `python3 -c "import sys; s=open('docs/methodik/95_hitzebelastung.md',encoding='utf-8').read(); k=s[s.index('## 7 '):s.index('## 8 ')]; b=k.split('id: heat.h_heim')[1].split('parameter:')[0]; t=s[s.index('## 5 '):s.index('## 6 ')]; sys.exit(not ('wert: 0.344' in b and 'band: [0.275, 0.517]' in b and 'kennzeichnung: berechnet' in b and 'abgeleitet_aus: [heat.qbar_pfl, heat.beta_pfl]' in b and 'id: heat.s_gek' in k and 'Kommune, unabhängig von der gezeichneten Fläche' in t and 'CARE_HOME_SHARE_85P' in t and 'Rückfallwert für Zellen ohne eigenen Wert' in t and 'h_zelle(qbar) - h' in s))"` | behoben (T-1537): Absatz „\(h_{\text{Heim}}\) je Zelle“ in §5 mit Formel, Beispiel und Rückfallwert, Block `heat.h_heim`, Zeichentabelle, Log 45; Registry-Parameter und Zellrechnung beim CTO |
| 148 | Log 44/46, §5 | Nullwirkung (P2) | Die Abschätzung für öffentliche Kühlzentren liefert der Methodik-Zweig, der CTO baut sie danach ein | Entscheidung methodik_manager (Runde 31): wie 139. Umgesetzt: Andockpunkt `COOLING_ROOMS_DRINKING_WATER` („Kühle Räume / Kühlzentren“, Kostenmodell je Raum nach dem Konzept „kühle Orte“), Umsetzung beim CTO; der Satz in der Modellgrenze von S157 verweist auf den neuen Hebel | B | `python3 -c "import sys; s=open('docs/methodik/95_hitzebelastung.md',encoding='utf-8').read(); t=s[s.index('## 5 '):s.index('## 6 ')]; sys.exit(not ('95-S157-02' in s and 'Andockpunkt im Produkt:** dieselbe Maßnahme' in t and 'Umsetzung beim CTO (eiserne Regel 5)' in t and 'rechnet der eigene Hebel unten' in t and 'eine eigene Abschätzung nach P2 (Befund 130)' not in t))"` | behoben (T-1537): mit 139 zusammen; Übernahmeliste an den CTO im Ergebnis von T-1537 |
| 149 | §5 Hebel S157, Charakterisierung (Anpassungspotenzial) | Nullwirkung in der Charakterisierung (P2) | S157 zählte im Anpassungspotenzial mit 0; es sank auf 0,050 (früher 0,18) | Entscheidung methodik_manager (Runde 31): S157 mit seiner Voreinstellung. Umgesetzt: \(r_{\text{S157}} = a_{85+} \times h_{\text{Heim}} \times s_{\text{gek}} \times (1 - g_{\text{S157}})\) = 0,284 × 0,344 × 0,11 × 0,706 = 0,0076; mit dem Hitzeaktionsplan 1 − 0,95 × (1 − 0,0076) = 0,057; Warmsen 0,056; Gruppe nach KWRA unverändert (unter 0,1). Verworfen: \(1 - g_{\text{S157}}\) = 0,71 unmittelbar (zählte den Heim-Exzess als ganze Hitzemortalität) | B | `python3 -c "import sys; s=open('docs/methodik/95_hitzebelastung.md',encoding='utf-8').read(); t=s[s.index('## 5 '):s.index('## 6 ')]; sys.exit(not ('S157 mit seiner Voreinstellung' in t and '= 0,284 × 0,344 × 0,11 × 0,706 = 0,0076' in t and '1 − 0,95 × (1 − 0,0076) = 0,057' in t and 'abs(1 - 0.95 * (1 - r) - 0.057)' in s))"` | behoben (T-1537): Formelzeile in §5, Log 45, Beispiel-Block `s157_voreinstellung`; Umsetzung in `charakterisierung.anpassungspotenzial` beim CTO |
| 111 | Kapitel 7, alle Blöcke | Fortschreibung des Prüfausdrucks (Befunde 138, 139, 146) | Kapitel 7 hat mit `heat.s_gek`, `heat.h_heim` und `heat.delta_kuehlzentren` 27 statt 24 Blöcke | Ausdruck mit 27 Blöcken | B | `python3 -c "import re,sys; s=open('docs/methodik/95_hitzebelastung.md',encoding='utf-8').read(); b=s[s.index('## 7 '):s.index('## 8 ')].split('parameter:')[1:]; sys.exit(not (len(b) == 27 and all(re.search(r'^ *kennzeichnung: (\S+)', x, re.M).group(1) in ('quelle', 'abschaetzung_kap3', 'berechnet') for x in b) and all(re.search(r'^ *abgeleitet_aus: .heat', x, re.M) for x in b if 'kennzeichnung: berechnet' in x)))"` | behoben, Prüfausdruck fortgeschrieben in der Fortsetzung der Runde 31, Teil 2, wegen der Befunde 138, 139 und 146 (T-1537) |

### Fortsetzung Runde 31, Teil 3

D1, D2 und Sensitivitäten, T-1538-methodik_manager (Paket 3 von T-1534-cmo, Ersatz für T-1496-methodik_manager),
27.09.2026. Eingelöst werden die Befunde 143, 150, 151 und 152 mit den Entscheidungen des methodik_manager aus der Tabelle
oben; Wortlaut von D1, D2 und den Sensitivitäten in T-1351-ceo, Nachtrag 19:10 Uhr. **Zählung nach A-0046:** keine neue
Runde, die Arbeit gehört zu Runde 31. Nach diesem Teil ist aus 136–153 kein Befund mehr zurückgestellt; 116 bleibt beim
cto.

**Was sich ändert.** Kapitel 7 hat zwei neue Blöcke (29 statt 27): `heat.vg_in_kalibrierjahren` 0 = „nein“ (Band 0–1,
`abschaetzung_kap3`, Quelle [76]) und `heat.kappung_vg` 0,794 (Band 0,743–0,842, `abschaetzung_kap3`, Quelle [47]
Tabelle 1). Die Blöcke `heat.f_alter` und `heat.l_restlebenserwartung` tragen jetzt ein Band je Altersband (bisher
`null` bzw. nur 85+). §5 hat beim Hebel Schutzprogramme den Doppelzählungs-Wächter mit Eingabe, Voreinstellung,
Gegenargument und Wirkung der anderen Voreinstellung für Berlin, den Absatz „Kappung 0,794“ und am Ende den Absatz
„Sensitivitäten des Basiswerts im Vergleich zu den Hebeln“; beim Hebel Kühlzentren gilt derselbe Wächter mit eigener
Frage. §3.3a und §3.5 leiten die Bänder her, Zeichentabelle, Evidenz-Register 95-S152-03, Quellen [74]–[76] (neu) und
Entscheidungslog (Nr. 47–49 neu) ziehen mit; neuer Beispiel-Block `sensitivitaeten_berlin`. Die Tests führen die zwei neuen
Kennungen in `_AUSSTEHEND_CTO`; Kapitel 7 zählt 10 belegt, 16 abgeschätzt, 3 berechnet, die Registry unverändert 10/12/2.
`backend/app/services/engine/impact/params.py` ist nicht angefasst.

**Nachgerechnet:** Kein Betrag ändert sich. Die Voreinstellung „nein“ rechnet wie bisher, die Kappung stand schon in der
Formel, und Bänder ändern keinen Zentralwert. §3.0 und der Beispiel-Block `rechenkette_95` laufen unverändert grün
(Lint 301 Checks). Der Statuskopf bleibt „in Revision“ (seit Teil 2) und nennt Teil 3.

**Gemessen am 27.09.2026:** (1) \(c_{\text{kal}}\) mit ersetztem \(f_a\): `run_evaluation` aus
`backend/scripts/kalibrierung/calibrate_heat_mortality_rev7.py` auf `sommermittel_bundesland_povw.csv`, Fenster
2012–2024, \(s_{\text{Süd}}\) = 1,65; Basis \(f_a\) gibt 0,5808 (Bericht 0,581), \(f_a\) Sommer 2025 0,6512, Sommer 2026
0,5342; Prüfstein in allen drei Fällen 12/16. (2) \(\bar L_a\) sterbefallgewichtet aus den Drucken
`docs/quellen/methodik/95/49_Destatis_Sterbefaelle_2023_12613-02.md` und `48_…12613-b01.md`/`-b02.md` (Rechenweg von
`l85_sterbefallgewichtung.py` auf alle Bänder erweitert): 28,635 · 15,309 · 8,544 · 4,159 J; 85+ trifft den Anlagenwert
4,159. Beide Läufe mit Probeskripten außerhalb des Repos.

| Größe (Beträge je Jahr, Preisstand 2024) | Berlin, Kette | Berlin, Zelllauf (Golden) | Warmsen, Zelllauf |
|---|---|---|---|
| Jahresbetrag nach allen drei Paketen | 362,9 Mio. € (unverändert) | 342,67 Mio. € (unverändert) | 173.099 € (unverändert) |
| Sensitivität von f_alter (Sommer 2025 / 2026, \(c_{\text{kal}}\) neu gefittet) | 310,2 / 402,9 Mio. € | — | — |
| Sensitivität von l_restlebenserwartung (unteres / oberes Bandende) | 357,3 / 381,1 Mio. € | — | — |
| Kappung 0,794, wo sie greift (Band 0,743–0,842; ohne Kappung) | 34,9 Mio. € (26,8–43,6; 46,1) | — | — |
| Schutzprogramme mit Voreinstellung „nein“ / mit „ja“ | 11,7 / 0 Mio. € | — | — |

**Bindungstabelle (geänderter Entscheidungslog):**

| Abgeleitete Zahl oder Aussage | Stelle | Bindung |
|---|---|---|
| Voreinstellung „nein“; 18 Pläne am 10.06.2024; 4 von 53, also 7,5 %; erwarteter Fehler 0,9 gegen 10,8 Mio. € | Log 47; §5 Doppelzählungs-Wächter; Block `heat.vg_in_kalibrierjahren` (Kommentar); Beispiel-Block `sensitivitaeten_berlin` | (a) wortgleich |
| Berlin 0 statt 11,7 Mio. € mit „ja“ | Log 47 Spalte Alternative; §5 Doppelzählungs-Wächter; Tabelle oben | (a) wortgleich |
| Wächter für Kühlzentren: eigene Frage, Voreinstellung „nein“, \(\delta_{\text{KZ}}\) = 1 | Log 47 Spalte Entscheidung; §5 Kühlzentren | (b) Verweis auf den Block `heat.vg_in_kalibrierjahren` |
| Kappung 0,794 (0,743–0,842), ohne Kappung 0,728, bei \(\delta_{\text{HAP}}\) 0,85 0,791 | Log 48; §5 „Kappung 0,794“; Block `heat.kappung_vg`; Register 95-S152-03 | (a) wortgleich |
| 34,9 Mio. € (26,8–43,6 Mio. €), ohne Kappung 46,1 Mio. € | Log 48; §5 „Kappung 0,794“; Block-Kommentar `heat.kappung_vg` | (a) wortgleich |
| 0,794 als Paketwert und Kappung mit \(\delta_{\text{HAP}}\) | Log 43 (unverändert), §5 Hebel Hitzeaktionsplan und Kühlzentren | (b) Verweis auf den Block `heat.kappung_vg` (in §5 Kühlzentren ausdrücklich) |
| Band \(f_a\) 0,156–0,562 / 0,341–0,753 / 0,588–0,659 / 1,0 | Log 49; §3.3a „Band von \(f_a\)“; Zeichentabelle \(f_a\); Block `heat.f_alter` | (a) wortgleich |
| Berlin 310,2–402,9 Mio. € mit \(c_{\text{kal}}\) 0,651 und 0,534; einfachere Rechnung 277,0–438,3 Mio. € | Log 49; §5 „Sensitivität von f_alter“; Block-Kommentar `heat.f_alter` | (a) wortgleich |
| Band \(\bar L_a\) 23,39–28,64 / 15,31–15,59 / 8,54–8,90 / 4,16–4,20 J; Berlin 357,3–381,1 Mio. € | Log 49; §3.5 „Band von \(\bar L_a\)“; Zeichentabelle \(\bar L_a\); Block `heat.l_restlebenserwartung`; §5 „Sensitivität von l_restlebenserwartung“ | (a) wortgleich |
| Wächter „Hat die Kommune ein solches Programm schon in den Kalibrierjahren … dann gilt \(\delta_{\text{VG}}\) = 1“ ohne Eingabe | früher §5, ersetzt; Log 47 Spalte Alternative „Stand bis T-1538“ | (c) Historie |

| Nr | Stelle | Art | Begründung | Vorschlag | Kat. | Prüfausdruck | Status |
|---|---|---|---|---|---|---|---|
| 143 | Quellen [47] und [70], `docs/quellen/methodik/95/QUELLEN.md` | Quellenarchiv unvollständig (eiserne Regel 3) | Liotta u. a. 2018 ist [70] in #95 und gehört ins Archiv von #95; ebenso [47] | Entscheidung methodik_manager: Archiv in T-1494-methodik_manager, geschlossen mit T-1534-cmo, Paket 3. Das Archiv enthält beide Zeilen seit T-1494; `docs/quellen/methodik/95/` ist in diesem Paket nicht geändert | B | `grep -qF '\| [47] \|' docs/quellen/methodik/95/QUELLEN.md && grep -qF '\| [70] \|' docs/quellen/methodik/95/QUELLEN.md` | behoben (T-1538): Prüfausdruck gegen das Archiv aus T-1494 grün, formal geschlossen nach der Antwort des CEO vom 27.09.2026, 09:50 Uhr |
| 150 | §5 Hebel Schutzprogramme und Kühlzentren, Doppelzählungs-Wächter, Kapitel 7 | Eingabe fehlt | \(\delta_{\text{VG}}\) = 1, wenn das Programm schon in den Kalibrierjahren bestand; ob die Kommune dafür eine Eingabe braucht und was bis dahin gilt, stand nicht da | Entscheidung methodik_manager (Runde 31): Eingabe ja/nein mit begründeter Voreinstellung und Block. Umgesetzt: Frage „Lief das Programm schon in den Jahren 2012–2024?“ je Maßnahme (Schutzprogramme, Kühlzentren), Voreinstellung „nein“ als Abschätzung von KAP3 aus [76] (18 Pläne bundesweit am 10.06.2024; 4 von 53 Kreisen und kreisfreien Städten in NRW im Oktober 2023, 7,5 %); mit „ja“ als Voreinstellung Berlin 0 statt 11,7 Mio. € (Unterschätzung, Nullwirkung gegen P2), mit „nein“ bei einer Kommune mit altem Programm 11,7 Mio. € doppelt; erwarteter Fehler 0,9 gegen 10,8 Mio. €; Gegenargument in §5 und Log 47 | B | `python3 -c "import sys; s=open('docs/methodik/95_hitzebelastung.md',encoding='utf-8').read(); k=s[s.index('## 7 '):s.index('## 8 ')]; b=k.split('id: heat.vg_in_kalibrierjahren')[1].split('parameter:')[0]; t=s[s.index('## 5 '):s.index('## 6 ')]; sys.exit(not ('wert: 0 ' in b and 'band: [0, 1]' in b and 'kennzeichnung: abschaetzung_kap3' in b and 'quelle: lzg_nrw2024' in b and 'Voreinstellung „nein“ (Abschätzung von' in t and 'Berlin 0 statt 11,7 Mio. €' in t and 'höchstens 7,5 % × 11,7 = 0,9 Mio. €' in t and 'Voreinstellung „nein“ aus demselben Grund' in t and '**Gegenargument:** Die Zahlen stammen vom Ende des' in t and 'Was gilt beim Doppelzählungs-Wächter der Schutzprogramme' in s and '[76]** K. Müller' in s))"` | behoben (T-1538): Block `heat.vg_in_kalibrierjahren`, Absatz „Doppelzählungs-Wächter“ in §5 (Schutzprogramme) und Satz beim Hebel Kühlzentren, Log 47, Quelle [76]; Registry-Parameter und Eingabe beim CTO (`_AUSSTEHEND_CTO`) |
| 151 | §5 Hebel Schutzprogramme (Kappung), Block `heat.delta_vg`, Kapitel 7 | Wert begrenzt den Betrag ohne eigenen Block (P1) | Die Kappung 0,794 stand nur im Band von \(\delta_{\text{VG}}\) | Entscheidung methodik_manager (Runde 31): eigener Block nach P1. Umgesetzt: `heat.kappung_vg` = 1 − 0,206 = 0,794 aus [47] Tabelle 1, Band 0,743–0,842 aus dem Intervall 15,8–25,7 %, `abschaetzung_kap3` (Paketwert steht für eine andere Größe, Log 40); zugleich unteres Bandende von \(\delta_{\text{VG}}\) (ohne Kappung 0,728); greift bei \(\delta_{\text{HAP}}\) 0,85 (0,791; mit Kühlzentren 0,788) und bei Reichweite und Wirkung am oberen Ende (Befund 126, Runde 29); Sensitivität Berlin dort 34,9 Mio. € (26,8–43,6 Mio. €), ohne Kappung 46,1 Mio. € | B | `python3 -c "import sys; s=open('docs/methodik/95_hitzebelastung.md',encoding='utf-8').read(); k=s[s.index('## 7 '):s.index('## 8 ')]; b=k.split('id: heat.kappung_vg')[1].split('parameter:')[0]; t=s[s.index('## 5 '):s.index('## 6 ')]; sys.exit(not ('wert: 0.794' in b and 'band: [0.743, 0.842]' in b and 'kennzeichnung: abschaetzung_kap3' in b and 'quelle: urban2025' in b and '**Kappung 0,794 (Block' in t and '1 − 0,206 = 0,794, Band 1 − 0,257 = 0,743 bis' in t and '169,5 Mio. € × (1 − 0,794) = 34,9 Mio. €' in t and '1 − 0,40 × 0,68 = 0,728, die Kappung hebt das auf 0,794' in t and 'Kappung aus dem Block' in t and 'python test: sensitivitaeten_berlin' in s))"` | behoben (T-1538): Block `heat.kappung_vg`, Absatz „Kappung 0,794“ in §5, Verweis beim Hebel Kühlzentren, Log 48, Register 95-S152-03; Registry-Parameter beim CTO (`_AUSSTEHEND_CTO`, heute Konstante `VG_PAKET_DE`) |
| 152 | §3.3a, §3.5, §5, Blöcke `heat.f_alter` und `heat.l_restlebenserwartung` | Sensitivität ohne Zahl, Band fehlt | Für \(f_a\) und \(\bar L_a\) nannte der Bericht keine Sensitivität als Zahl; \(f_a\) hatte kein Band, \(\bar L_a\) nur für 85+ | Entscheidung methodik_manager (Runde 31): Sensitivitäten als Zahl in Mio. € für Berlin, gemessen wie die übrigen. Umgesetzt: Bänder als Abschätzung von KAP3 hergeleitet (\(f_a\) aus den Altersanteilen der Sommer 2025 [74] und 2026 [75]; \(\bar L_a\) von der Stützstelle bis zum sterbefallgewichteten Wert aus [48], [49]) und in die Blöcke geschrieben; Berlin (Kette) \(f_a\) 310,2 und 402,9 Mio. € mit neu gefittetem \(c_{\text{kal}}\) 0,651 und 0,534 (einfachere Rechnung mit festem \(c_{\text{kal}}\) 277,0 und 438,3 Mio. €), \(\bar L_a\) 357,3 und 381,1 Mio. € | B | `python3 -c "import sys; s=open('docs/methodik/95_hitzebelastung.md',encoding='utf-8').read(); k=s[s.index('## 7 '):s.index('## 8 ')]; fa=k.split('id: heat.f_alter')[1].split('parameter:')[0]; la=k.split('id: heat.l_restlebenserwartung')[1].split('parameter:')[0]; t=s[s.index('## 5 '):s.index('## 6 ')]; sys.exit(not ('band: {u65: [0.156, 0.562], 65-74: [0.341, 0.753], 75-84: [0.588, 0.659]}' in fa and 'band: {u65: [23.39, 28.64], 65-74: [15.31, 15.59], 75-84: [8.54, 8.90], 85+: [4.16, 4.20]}' in la and 'Sensitivität von f_alter' in t and 'Sensitivität von l_restlebenserwartung' in t and '**310,2 Mio. €**' in t and '**402,9 Mio. €**' in t and '**357,3 Mio. €**' in t and '**381,1 Mio. €**' in t and 'ergäbe 277,0 und 438,3 Mio. €' in t and 'Die Altersanteile der Hitzetoten schwanken von Sommer zu' in s and 'u65 23,39–28,64 J' in s and '[74]** M. an der Heiden' in s and '[75]** M. an der Heiden' in s))"` | behoben (T-1538): Bänder in §3.3a, §3.5, Zeichentabelle und den Blöcken; Absatz „Sensitivitäten des Basiswerts im Vergleich zu den Hebeln“ in §5; Beispiel-Block `sensitivitaeten_berlin`; Log 49; Quellen [74], [75] |
| 111 | Kapitel 7, alle Blöcke | Fortschreibung des Prüfausdrucks (Befunde 150, 151) | Kapitel 7 hat mit `heat.vg_in_kalibrierjahren` und `heat.kappung_vg` 29 statt 27 Blöcke | Ausdruck mit 29 Blöcken | B | `python3 -c "import re,sys; s=open('docs/methodik/95_hitzebelastung.md',encoding='utf-8').read(); b=s[s.index('## 7 '):s.index('## 8 ')].split('parameter:')[1:]; sys.exit(not (len(b) == 29 and all(re.search(r'^ *kennzeichnung: (\S+)', x, re.M).group(1) in ('quelle', 'abschaetzung_kap3', 'berechnet') for x in b) and all(re.search(r'^ *abgeleitet_aus: .heat', x, re.M) for x in b if 'kennzeichnung: berechnet' in x)))"` | behoben, Prüfausdruck fortgeschrieben in der Fortsetzung der Runde 31, Teil 3, wegen der Befunde 150 und 151 (T-1538) |

## Runde 32 des methodik_manager zu T-1583-methodik_manager Abschnitt A (27.09.2026) — neue Befunde ab Nr. 154

Urteil des methodik_manager vom 27.09.2026, 11:43 Uhr (Runde 32, Null-Runde: nein): 1 B-Befund, 2 C-Befunde. Die
Nacharbeit (Nacharbeitsrunde 1 des Tickets) behebt alle drei; das nächste Urteil zu Abschnitt A ist Runde 33.

**Was sich ändert.** Nur Abschnitt A. §3.4 (`#r0-a`): Obergrenze der Summe 4,3 statt 4,4 (1,6775 + 2,6612 = 4,339),
Zusatzterm „1,21…2,66“ in beiden Zeilen, dazu ein Satz, wie der Mittelwert 3,5 entsteht: geometrisches Mittel der
Bandgrenzen √(2,89 × 4,34) = 3,54, auf das die Altersraten normiert sind (Block `beispiel_95_r0_normierung`, Summe 3,54);
die Mitte der Spanne, 3,61, läge 2 % höher. Den Rechenweg nannte bisher keine Stelle des Berichts und auch nicht die
Rev.-5-Fassung (`docs/render/METHODIK_M0_GESUNDHEIT.html`); das geometrische Mittel trifft die normierte Summe 3,54 genau
und ist deshalb als Lesart festgeschrieben. Der Beispiel-Block `beispiel_95_r0_kette` prüft jetzt 2,89 und 4,34 statt
2,9 und 4,4 und zusätzlich das geometrische Mittel. Zeichentabelle §3.6: Summen-Band 2,9–4,3 [×0,83–1,23]; das
kombinierte Band ×0,6–1,6 bleibt als nach außen gerundeter Wert (1,23 × 1,25 = 1,54). \(\delta_{\text{VG}}\) und
\(\delta_{\text{VG,morb}}\) rechnen mit dem ungerundeten \(w_{\text{VG}}\) = 0,3445. §3.2: „die folgende Tabelle“ statt
„die Tabelle oben“.

**Unverändert:** jede `wert:`-Zeile, die Statuszeile, Kapitel 5 bis 8 (Ausdruck (4) des Abnahmekriteriums), alle Beträge.
Die Werte 1,9 / 6,3 / 10,8 / 15,6 und das Band ×0,6–1,6 bleiben; Kapitel 7 (Block `heat.r0_einweisungsrate`) ist nicht
berührt.

**Außerhalb des Dateirahmens, nicht geändert (Eiserne Regel 5):** `backend/app/services/engine/impact/params.py` Z. 1569
nennt im Band-Text von \(r_{0,a}\) weiter „Summenband 2,9–4,4 (×0,83–1,26)“, Z. 328, 339 und 453 sowie
`health.py` Z. 353 „0,20 × 0,34“. Das sind Erläuterungstexte ohne Einfluss auf einen Betrag; Nachzug beim cto zusammen
mit den offenen Kennungen in `_AUSSTEHEND_CTO`.

| Nr | Stelle | Art | Begründung | Vorschlag | Kat. | Prüfausdruck | Status |
|---|---|---|---|---|---|---|---|
| 154 | docs/methodik/95_hitzebelastung.md §3.4, Anker #r0-a Z. 667, und §3.6 Zeichentabelle Z. 799 (r_{0,a}) | falsche Zahl im Fließtext, Herleitung nicht abgeschlossen | Die Zeile nennt '1,68 + 1,21…2,67 ⇒ 3,5 (2,9–4,4)'. Die Zeile davor und der Block beispiel_95_r0_kette ergeben 0,119 × 3,106 × 7,2 = 2,661, also 2,66. Die Obergrenze der Summe ist 1,68 + 2,66 = 4,34, ungerundet 1,6775 + 2,6612 = 4,339, also 4,3 und nicht 4,4. Der Mittelwert 3,5 steht ohne Rechenweg da; die Mitte des Bands wäre 3,6. Die Zeichentabelle übernimmt 'Summen-Band 2,9–4,4 [×0,83–1,26]' | Z. 667 auf '1,68 + 1,21…2,66 ⇒ 3,5 (2,9–4,3)' setzen und in einem Satz sagen, wie 3,5 aus dem Band entsteht, zum Beispiel als geometrisches Mittel √(2,88 × 4,34) = 3,54, falls das die Regel war. Z. 799 auf 'Summen-Band 2,9–4,3 [×0,83–1,23]' setzen. Das kombinierte Band ×0,6–1,6 bleibt als ausdrücklich nach außen gerundeter Wert stehen (1,23 × 1,25 = 1,54). So bleiben Kap. 7 und alle wert:-Zeilen unberührt | B | `grep -qF '1,68 + 1,21…2,66 ⇒' docs/methodik/95_hitzebelastung.md && ! grep -qF '1,21…2,67' docs/methodik/95_hitzebelastung.md && ! grep -qF '(2,9–4,4)' docs/methodik/95_hitzebelastung.md && ! grep -qF 'Summen-Band 2,9–4,4' docs/methodik/95_hitzebelastung.md` | behoben (T-1583): §3.4 Obergrenze 4,3, Satz zum Mittelwert (geometrisches Mittel √(2,89 × 4,34) = 3,54, Normierung der Altersraten), Beispiel-Block `beispiel_95_r0_kette` auf 2,89/4,34 und geometrisches Mittel; Zeichentabelle Summen-Band 2,9–4,3 [×0,83–1,23] |
| 155 | docs/methodik/95_hitzebelastung.md §3.6 Zeichentabelle Z. 817 (δ_VG) und Z. 818 (δ_VG,morb) | Rechenweg rechnet mit gerundeter Zahl nicht auf | '0,931 = 1 − 0,20 × 0,34' ergibt nachgerechnet 0,932, und '1 + 0,20 × 0,34' ergibt 1,068 statt 1,069. Beide Werte stimmen nur mit dem ungerundeten w_VG = 24,4 / 97,3 / 0,728 = 0,3445 | in beiden Zeilen 0,3445 (gerundet 0,34) einsetzen, wie bei der Toleranz 0,2918 % in Befund 140 | C | `! grep -qF '= 1 − 0,20 × 0,34,' docs/methodik/95_hitzebelastung.md && ! grep -qF '= 1 + 0,20 × 0,34 (' docs/methodik/95_hitzebelastung.md` | behoben (T-1583): beide Zeilen rechnen mit 0,3445 (gerundet 0,34) |
| 156 | docs/methodik/95_hitzebelastung.md §3.2 Z. 359 | falscher Verweis | Der Satz lautet 'die Tabelle oben ist die auf zwei Stellen gerundete Lesehilfe'. Die Tabelle der Wochenquantile steht aber darunter, in Z. 364–368 | 'die Tabelle unten' oder 'die folgende Tabelle' | C | `! grep -qF 'die Tabelle oben ist die auf zwei Stellen gerundete Lesehilfe' docs/methodik/95_hitzebelastung.md` | behoben (T-1583): „die folgende Tabelle“ |

## Runde 33 des methodik_manager zu T-1583-methodik_manager Abschnitt A (27.09.2026) — neuer Befund 157

Urteil des methodik_manager vom 27.09.2026, 11:51 Uhr (Runde 33, Null-Runde: nein): 1 B-Befund. Die Befunde 154 bis 156
aus Runde 32 sind dort als behoben bestätigt. Die Nacharbeit (Nacharbeitsrunde 2 des Tickets) behebt Befund 157; das
nächste Urteil zu Abschnitt A ist Runde 34.

**Was sich ändert.** Nur Abschnitt A. §4, „Verbleibender dokumentierter Rest“: σ = 2/√12 = 0,58 K statt „≈ 0,5 K“, dazu
der Satz, dass die Setzung 0,5 K abgerundet ist und den Betrag eher unterschätzt; mit 0,58 K läge Wirkung (d) für Berlin
am Punkt bei × 1,026 statt × 1,019, der Betrag rund 0,7 % höher, mehr als die Toleranz von 0,29 % aus §3.3. §3.0
Wirkung (d): Halbsatz mit denselben Zahlen und Verweis auf §4. Prüfblock `rechenkette_95`: Zeilen für σ = 2/√12
(Ergebnis 1,026 ± 0,003) und für das Verhältnis 1,007 ± 0,001.

**Gemessen am 27.09.2026** mit dem Modell des Prüfblocks (Gauß-Hermite mit fünf Stützstellen, mittelwerttreu, Berlin am
Punkt): σ = 0,5 K ergibt × 1,0192, σ = 0,5774 K ergibt × 1,0260; Verhältnis 1,0067.

**Unverändert:** der gesetzte Wert σ = 0,5 K, die Faktoren × 1,021 (Zelllauf) und × 1,023–1,024 (Modellrechnung Rev. 6)
in §4, jede `wert:`-Zeile, die Statuszeile, Kapitel 5 bis 8, alle Beträge einschließlich Golden 342,67 Mio. €.

| Nr | Stelle | Art | Begründung | Vorschlag | Kat. | Prüfausdruck | Status |
|---|---|---|---|---|---|---|---|
| 157 | docs/methodik/95_hitzebelastung.md §4, Absatz „Verbleibender dokumentierter Rest“, Z. 908–911; mitbetroffen §3.0 Wirkung (d), Z. 237–238 | falsche Zahl im Fließtext, Herleitung geht nicht auf (LF 7, LF 13) | Dort steht „Gleichverteilungsannahme ⇒ σ ≈ 2/√12 ≈ 0,5 K“, aber 2/√12 = 0,577, gerundet 0,58 K. Die genannte Herleitung trägt den gesetzten Wert 0,5 K also nicht. Mit dem Modell des Prüfblocks rechenkette_95 am Punkt nachgerechnet (Gauß-Hermite) gibt σ = 0,5 K den Faktor × 1,019 und σ = 0,577 K den Faktor × 1,026. Der Berlin-Betrag läge damit rund 0,7 % höher, außerhalb der Toleranz von 0,29 % aus §3.3 | Den Wert σ = 0,5 K nicht ändern; er ist keine `wert:`-Zeile, und der Golden-Betrag bleibt. Den Satz so richtigstellen: „2/√12 = 0,58 K; gesetzt ist 0,5 K, abgerundet und damit unterschätzend im Sinn von ‚konservativ‘; mit 0,58 K läge Wirkung (d) für Berlin am Punkt bei × 1,026 statt × 1,019, der Betrag rund 0,7 % höher.“ In §3.0 (d) einen Halbsatz mit Verweis auf §4 ergänzen. Im Prüfblock rechenkette_95 eine Zeile für σ = 2/√12 ergänzen (Ergebnis 1,026 ± 0,003) | B | `! grep -qF '2/√12 ≈ 0,5 K' docs/methodik/95_hitzebelastung.md && grep -qF '2/√12 = 0,58 K' docs/methodik/95_hitzebelastung.md` | behoben (T-1583): §4 σ = 2/√12 = 0,58 K mit Satz zur Setzung 0,5 K (× 1,026 statt × 1,019, rund 0,7 %), §3.0 (d) Halbsatz mit Verweis auf §4, Prüfblock `rechenkette_95` um σ = 2/√12 ergänzt |

## Runde 34 des methodik_manager zu T-1583-methodik_manager Abschnitt A (27.09.2026) — neue Befunde 158 bis 161

Urteil des methodik_manager vom 27.09.2026, 12:04 Uhr UTC (Runde 34, Null-Runde: nein): 2 B-Befunde (158, 159), 1 C-Befund
(160). Befund 157 aus Runde 33 ist dort als behoben bestätigt. T-1583 hatte seine drei Nacharbeitsrunden verbraucht;
nachgezogen wird im Ersatzticket T-1598-methodik_manager (Paket 1 von 3 unter T-1535-cmo). 159 und 160 stehen unverändert
wie im Urteil. 158 (erweitert um die Stellen in §5 und Kap. 7) und 161 sind in der Auflösung von T-1583 durch den
methodik_manager gefasst (T-1535-cmo, Planung vom 27.09.2026). Das nächste Urteil zu Abschnitt A ist Runde 35.

**Was sich ändert.** §3.0 Ebene 9: 34,1 statt 34,2 Fälle (253.528 × 10,8 / 100.000 × 1,2472 = 34,15); die Summanden
ergeben jetzt 152,0. Prüfblock `rechenkette_95`: eine Zeile prüft die vier Fallzahlen einzeln. §3.3: Tausenderpunkt in
3.158, 3.087, 1.897, 1.342, 5.240, 3.893, 2.252 und 1.416 im Fließtext und in der Tabelle (Codeblöcke unverändert).
Außerhalb von A, ausdrücklich verlangt: §5 Hebel Schutzprogramme, Morbidität „34,1 + 21,0 × 0,656 = 47,9 Einweisungen“
(ungerundet 34,15 + 21,00 × 0,6557 = 47,92, aus den gezeigten Zahlen 47,88); §5 \(\delta_{\text{VG}}\) und
\(\delta_{\text{VG,morb}}\) mit \(w_{\text{VG}}\) = 0,3445 wie in der Zeichentabelle (Befund 155); Kap. 7 Block mit
`f_75 = 34.1 + 21.0 * (1 - h_heim)` und Soll 47,9; Entscheidungslog Nr. 24 als Historie gekennzeichnet und durch Nr. 28
fortgeschrieben.

**Unverändert:** jede `wert:`-Zeile, die Statuszeile, alle Beträge (Kette 362,9 Mio. €, Morbidität 1,09 Mio. €,
47,9 × 7.152 € = 0,34 Mio. €, Golden 342,67 Mio. €), die Wahl in Log 24, alle übrigen Stellen in Kapitel 5 bis 8 (sie
gehören T-1584).

| Nr | Stelle | Art | Begründung | Vorschlag | Kat. | Prüfausdruck | Status |
|---|---|---|---|---|---|---|---|
| 158 | docs/methodik/95_hitzebelastung.md §3.0 Rechenkette Ebene 9 (Z. 195), Prüfblock `rechenkette_95`; §5 Hebel Schutzprogramme, Morbidität (Z. 1258–1259); Block in Kap. 7 (Z. 1839–1840) | falsche Zahl, Summe geht nicht auf (LF 11, Kriterium 5) | In §3.0 steht '70,2 + 26,7 + 34,2 + 21,0 = 152,0 Fälle'. Nachgerechnet ergibt 253.528 × 10,8 / 100.000 × 1,2472 = 34,15, also 34,1; die genannten Summanden ergeben 152,1 und nicht 152,0. Dieselbe Zahl steht in B: §5 '34,2 + 21,0 × 0,656 = 48,0 Einweisungen' und Kap. 7 `f_75 = 34.2 + 21.0 * (1 - h_heim)` mit `abs(f_75 - 48.0) < 0.05`. F_85+ = 21,00, h_Heim = 0,34427; ungerundet 34,15 + 21,00 × 0,6557 = 47,92, aus den gezeigten Zahlen 34,1 + 21,0 × 0,656 = 47,88, beides 47,9; mit 47,9 × 7.152 € bleibt es bei 0,34 Mio. € | In Z. 195 '70,2 + 26,7 + 34,1 + 21,0 = 152,0 Fälle'; im Block `rechenkette_95` nach `fall = …` die Zeile `for fi, soll in zip(fall, [70.2, 26.7, 34.1, 21.0]): assert abs(fi - soll) < 0.05`; in §5 '34,1 + 21,0 × 0,656' und '= 47,9 Einweisungen'; in Kap. 7 `f_75 = 34.1 + 21.0 * (1 - h_heim)` und `abs(f_75 - 47.9) < 0.05`. Kein Betrag und keine `wert:`-Zeile ändern sich. In der Auflösung von T-1583 durch den methodik_manager gefasst (T-1535-cmo, Planung vom 27.09.2026) | B | `grep -qF '70,2 + 26,7 + 34,1 + 21,0 = 152,0 Fälle' docs/methodik/95_hitzebelastung.md && ! grep -qF '34,2 + 21,0' docs/methodik/95_hitzebelastung.md && grep -qF '[70.2, 26.7, 34.1, 21.0]' docs/methodik/95_hitzebelastung.md && grep -qF '34,1 + 21,0 × 0,656' docs/methodik/95_hitzebelastung.md && ! grep -qF '48,0 Einweisungen' docs/methodik/95_hitzebelastung.md && grep -qF 'f_75 = 34.1 + 21.0' docs/methodik/95_hitzebelastung.md` | behoben (T-1598-methodik_manager): §3.0 Ebene 9 auf 34,1, Einzelprüfung der vier Fallzahlen im Block `rechenkette_95`, §5 auf 34,1 und 47,9 Einweisungen, Kap. 7 auf 34.1 und 47.9; Beträge unverändert |
| 159 | docs/methodik/95_hitzebelastung.md Entscheidungslog Nr. 24 (Z. 2220, verwiesen aus A in §2 Register 95-S153-04, Z. 155); Stelle außerhalb von A, ausdrücklich verlangt | Widerspruch zum Modell (LF 5 und LF 14) | Entscheidungslog Nr. 24 sagt 'Default 1 (nur β_iso wirkt auf F)'. Nach §3.4 (Z. 642–646), §3.3 (Tabelle Z. 398) und Log 28 wirkt β_iso nicht auf F; im F-Pfad gilt kein Modifikator. Der Eintrag ist nicht als überholt gekennzeichnet und widerspricht damit dem Modell | den Klammersatz ersetzen durch '(Stand Rev. 6, Historie; fortgeschrieben durch Nr. 28: auch β_iso wirkt nicht auf F, im F-Pfad gilt kein Modifikator)'. Wahl und Zahlen bleiben unverändert | B | `! grep -qF 'nur \(\beta_{\text{iso}}\) wirkt auf F' docs/methodik/95_hitzebelastung.md && grep -qF 'fortgeschrieben durch Nr. 28' docs/methodik/95_hitzebelastung.md` | behoben (T-1598-methodik_manager): Klammersatz in Log 24 in der Formelschreibweise des Logs, Wahl und Zahlen unverändert |
| 160 | docs/methodik/95_hitzebelastung.md §3.3, Z. 435–439, 455, 459, 463, 475 (Tabelle), 488, 496, 499 | Stil nach kap3-stil 'Tausenderpunkt ab 1.000' (LF 11) | Im Fließtext von §3.3 fehlt der Tausenderpunkt, und zwar in Z. 435–439 (3158, 3087, 1897), Z. 455 (1342), Z. 459 (5240), Z. 463 (3893), Z. 475 (Tabelle, 3087), Z. 488 (3158), Z. 496 (2252) und Z. 499 (1416). Daneben steht an anderen Stellen richtig '3.593.357' und '10.811'. Codeblöcke bleiben unverändert | 3.158, 3.087, 1.897, 1.342, 5.240, 3.893, 2.252, 1.416 schreiben oder, falls nicht behoben, zurückstellen (terminiert: Paket 3) | C | `python3 -c "import re,sys; s=open('docs/methodik/95_hitzebelastung.md',encoding='utf-8').read(); a=s[:s.index(chr(10)+'## 5 ')]; a=re.sub(chr(96)*3+'.*?'+chr(96)*3,'',a,flags=re.S); sys.exit(bool(re.search(r'(?<![\d.])(3158\|3087\|1897\|1342\|5240\|3893\|2252\|1416)(?!\d)',a)))"` | behoben (T-1598-methodik_manager): 14 Zahlen in elf Zeilen von §3.3 mit Tausenderpunkt, Codeblöcke unverändert; der Lint meldet danach keinen gebundenen Wert (ALLE LINTS GRÜN, 301 Checks) |
| 161 | docs/methodik/95_hitzebelastung.md §5 Hebel Schutzprogramme, Z. 1202 und Z. 1257; Stellen außerhalb von A, ausdrücklich verlangt | Rechenweg rechnet mit gerundeter Zahl nicht auf (LF 11 E5; Folge von Befund 155) | Z. 1202 `1 - 0{,}20 \times 0{,}34 = 0{,}931` und Z. 1257 `1 + 0{,}20 \times 0{,}34 = 1{,}069`: Mit 0,34 ergibt die Rechnung 0,932 und 1,068. Nach Befund 155 rechnet die Zeichentabelle mit 0,3445, §5 noch nicht | an beiden Stellen `0{,}20 \times 0{,}3445` (0,9311 und 1,0689), sonst nichts. In der Auflösung von T-1583 durch den methodik_manager gefasst (T-1535-cmo, Planung vom 27.09.2026) | C | `! grep -qF '0{,}20 \times 0{,}34 = ' docs/methodik/95_hitzebelastung.md && grep -qF '0{,}20 \times 0{,}3445' docs/methodik/95_hitzebelastung.md` | behoben (T-1598-methodik_manager): beide Stellen rechnen mit 0,3445 |

## Runde 36 des methodik_manager zu T-1584-methodik_manager Abschnitt B (27.09.2026) — neue Befunde ab Nr. 163

Urteil des methodik_manager vom 27.09.2026, 12:43 Uhr UTC (Runde 36, Null-Runde: nein): 3 B-Befunde (163, 164, 165), 2
C-Befunde (166, 167). Das letzte Urteil zu Abschnitt A (T-1598-methodik_manager Runde 35) lautet „Null-Runde: ja“; sein
C-Befund 162 steht hier mit, weil das Urteil zu B ihn zur Übernahme ins Ledger weitergibt. 163 bis 167 stehen wie im
Urteil; Stelle, Prüfausdruck und Kategorie sind unverändert. Nachgezogen in der ersten Nacharbeitsrunde von T-1584. Das
nächste Urteil zu Abschnitt B ist Runde 37.

**Was sich ändert (nur Abschnitt B, vor `## 5 ` zeichengleich mit origin/main).** §5 Hebel Hitzeaktionsplan: Absatz
„Herleitung (Abschätzung von KAP3, Befund 164)“ mit 2/3 × 1,00 + 1/3 × 0,85 = 0,95 aus [45] (Abstract, Teil Results;
gelesen am 27.09.2026, 12:45 UTC, über Europe PMC,
https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:10.1016/j.envint.2025.109746&resultType=core&format=json,
SHA-256 5bba9c44…ff84), Grund gegen die Mitte 0,925, Gegenargument und Berliner Betrag 361,8 Mio. € × 0,05 =
18,1 Mio. € je Jahr (Band 0–54,3 Mio. €). Absatz Sensitivitäten: „im Zentralwert um 0,75 bis 18,1 Mio. €“; der Satz
„Beide Bänder sind breiter …“ bezieht sich jetzt ausdrücklich auf den Zentralwert der Hebel und nennt das Band des
Hitzeaktionsplans (0–54,3 Mio. €) zwischen \(\bar L_a\) (23,8 Mio. €) und \(f_a\) (92,7 Mio. €). §5 Hebel S157: Formelzeile
mit \(\max(s_{\text{gek}} - 0{,}06;\ 0)\), Absatz „Bestand der Kalibrierjahre 0,06“ mit Herleitung aus [72] und [71], Band
0,04–0,09, Gegenargumenten, der Verfälschung durch die einfachere Rechnung (2,7 statt 1,2 Mio. €) und der Modellgrenze
(Untergrenze rund 4 %); Voreinstellung wirkt mit 0,05: Berlin 1,2 Mio. € je Jahr (über den Bestand 0,5–1,7 Mio. €, über
\(s_{\text{gek}}\) 0–2,2 Mio. €), Zelllauf 1,1 Mio. €, Warmsen 469 €; \(r_{\text{S157}}\) = 0,00345, Anpassungspotenzial
0,053 (Warmsen 0,0027, ebenfalls 0,053); Berlin je vollen Anteil unverändert 25,0 Mio. €, heute alle Heime gekühlt
23,5 Mio. €; Rechenweg 153,6 × 0,3443 = 52,88 und 52,88 × 0,7064 = 37,35 (Befund 166). Kap. 7: neuer Block
`heat.s_gek_kalib` (einzige neue `wert:`-Zeile, 0.06, gedeckt durch Befund 165), Kommentare in `heat.delta_hap`,
`heat.s_gek`, `heat.delta_vg` und `heat.delta_vg_morb` (0,3445, Befund 167); Beispiel-Blöcke `s157_berlin`,
`s157_voreinstellung` und `sensitivitaeten_berlin` rechnen die neuen Zahlen nach. Kap. 8 [72]: Verwendung um den Block
ergänzt. Entscheidungslog: Nr. 10 um die Herleitung von \(\delta_{\text{HAP}}\) ergänzt; Nr. 45 als Historie gekennzeichnet
und durch den neuen Eintrag Nr. 50 fortgeschrieben; Einleitung ergänzt.

**Unverändert:** Abschnitt A (Befund 162 bleibt deshalb offen, siehe unten), jede bestehende `wert:`-Zeile, die Kette
362,9 Mio. €, die Mortalität 361,8 Mio. €, Golden 342,67 Mio. €, die Hebel Kühlzentren (0,75 Mio. €) und Schutzprogramme
(11,7 Mio. €), die Kappung (34,9 Mio. €, Band 26,8–43,6 Mio. €, ohne Kappung 46,1 Mio. €) und die Sensitivitäten von
\(f_a\) und \(\bar L_a\). Die Kapitel-7-Zählung steigt auf 30 Blöcke (10 quelle, 17 abschaetzung_kap3, 3 berechnet).

| Nr | Stelle | Art | Begründung | Vorschlag | Kat. | Prüfausdruck | Status |
|---|---|---|---|---|---|---|---|
| 162 | docs/methodik/95_hitzebelastung.md §3.3 Absatz „Toleranz“, Z. 490 („mit 2000 bis unter 10.000 Einwohnern“; am 29.09.2026 Z. 492–493, umbrochen nach „2000 bis“) | Stil nach kap3-stil „Tausenderpunkt ab 1.000“ (LF 11 E5) | Befund 160 hat §3.3 nachgezogen, diese Zahl aber nicht. „2000“ ist hier eine Einwohnerzahl, keine Jahreszahl. Der Lint prüft den Tausenderpunkt nicht | „2.000 bis unter 10.000“ schreiben | C | `python3 -c "import re,sys; s=open('docs/methodik/95_hitzebelastung.md',encoding='utf-8').read(); sys.exit(bool(re.search(r'2000\s+bis\s+unter', s)) or not re.search(r'2\.000\s+bis\s+unter', s))"` | behoben (T-1643-methodik_manager): Z. 492–493 lauten jetzt „mit 2.000 bis“ / „unter 10.000 Einwohnern“. Prüfausdruck fortgeschrieben (Runde 39, Anlass C in T-1642-cmo): Der alte Ausdruck (! grep -qF 'mit 2000 bis unter' …) las nur eine Zeile, sah die Zahl über den Umbruch nach „2000 bis“ nicht und war deshalb grün, obwohl die Zahl stand; der neue liest die ganze Datei über Zeilenumbrüche hinweg und verlangt „2.000 bis unter“. Vorher: offen (aus dem Urteil zu T-1598-methodik_manager Runde 35; nachzuziehen mit der nächsten Änderung an A) |
| 163 | docs/methodik/95_hitzebelastung.md §5 Hebel Hitzeaktionsplan Z. 1049–1066; Absatz Sensitivitäten Z. 1306–1307 und Z. 1325 | falsche Aussage, Betrag fehlt (LF 11 E2) | Z. 1307 sagt ‚Die Hebel oben verschieben den Jahresbetrag Berlin … um 0,75 bis 11,7 Mio. €‘. δ_HAP = 0,95 wirkt aber auf den Exzess aller Bänder; mit dem Modell des Blocks sensitivitaeten_berlin senkt es die Mortalität 361,8 Mio. € um 18,1 Mio. € (Band δ_HAP 0,85–1,00: 0–54,3 Mio. €). Der Hebel hat als einziger keinen Berliner Betrag | Beim Hebel Hitzeaktionsplan den Berliner Betrag nennen: 361,8 Mio. € × (1 − 0,95) = 18,1 Mio. € je Jahr (Band 0–54,3 Mio. €), dazu eine Zeile im Beispiel-Block; Z. 1307 auf ‚0,75 bis 18,1 Mio. €‘ setzen; Z. 1325 prüfen, ob ‚Beide Bänder sind breiter als jeder Hebel‘ mit 18,1 Mio. € weiter gilt (L̄_a 23,8 Mio. € breit: ja, bezogen auf den Zentralwert der Hebel) und das so sagen | B | `! grep -qF 'um 0,75 bis 11,7 Mio. €' docs/methodik/95_hitzebelastung.md && grep -qF '18,1 Mio. €' docs/methodik/95_hitzebelastung.md` | behoben (T-1584-methodik_manager, Nacharbeit 1): Berliner Betrag 18,1 Mio. € je Jahr (Band 0–54,3 Mio. €, 5,0 %) im Hebel, im Block `heat.delta_hap` und im Beispiel-Block `sensitivitaeten_berlin` (Mortalität 361,8 Mio. €, Faktor auf den Exzess gleich Faktor auf die Mortalität); Sensitivitäten „im Zentralwert um 0,75 bis 18,1 Mio. €“, Vergleichssatz auf den Zentralwert bezogen, Band des Hebels genannt |
| 164 | docs/methodik/95_hitzebelastung.md §5 Hebel Hitzeaktionsplan Z. 1049–1058; Block heat.delta_hap Z. 1617; Log 10 Z. 2207 | Herleitung fehlt (LF 13, P1, P3) | Der Block ist `abschaetzung_kap3`, der Wert 0,95 steht aber nur als ‚zentral 0,95 zwischen DiD roh 1,00 und adjustiert 0,85 [45]‘. Die Mitte wäre 0,925. Wie 0,95 entsteht, sagt weder §5 noch Log 10, und es gibt keine Zeile ‚Zahl aus Quelle × Faktor = Ergebnis‘ | Im Hebel einen Absatz **Herleitung (Abschätzung von KAP3)** mit der Rechenzeile aus [45] (etwa 1,00 − Anteil × (1,00 − 0,85) = 0,95 mit begründetem Anteil) oder der ausdrücklichen Setzung samt Grund, warum nicht die Mitte 0,925; Band 0,85–1,00 dazu; Log 10 und Blockkommentar nachziehen; `wert:` nur ändern, wenn die Herleitung es verlangt | B | `python3 -c "import sys; s=open('docs/methodik/95_hitzebelastung.md',encoding='utf-8').read(); t=s[s.index('## 5 '):s.index('## 6 ')]; h=t[:t.index('- **Gekühlte Räume')]; sys.exit(not ('Abschätzung von KAP3' in h and 'Herleitung' in h))"` | behoben (T-1584-methodik_manager, Nacharbeit 1): Rechenzeile 2/3 × 1,00 + 1/3 × 0,85 = 1,00 − 1/3 × 0,15 = 0,95 aus [45] (Abstract, Teil Results): das Mittel über 15 Städte doppelt gewichtet, weil der bereinigte Wert an drei im Produkt nicht nachgebildeten Merkmalen der Städte hängt; Grund gegen die Mitte 0,925 (Berlin 27,1 statt 18,1 Mio. €), Gegenargument, Band 0,85–1,00; Log 10 und Blockkommentar nachgezogen; `wert:` unverändert 0.95 |
| 165 | docs/methodik/95_hitzebelastung.md §5 Hebel S157 Voreinstellung s_gek Z. 1096–1109; Block heat.s_gek Z. 1692–1702; Log 45 Z. 2242; gegen Kap. 1 (a) Z. 119–125 | Widerspruch, Doppelzählung gegen die Kalibrierjahre (LF 4, LF 15, Aufgabe §3.5) | Kap. 1 (a): Was 2012–2024 an Anpassung schon wirkte, steckt über c_kal im Basiswert. s_gek = 0,11 ist aber der heutige Bestand an Pflegeheimen mit Klimaanlage [71], und schon 2015 hatten 5,7 % der neuen Gebäude des Sozialwesens eine Kühlung [72]. Die Voreinstellung zieht damit die Wirkung schon vorhandener Klimaanlagen noch einmal vom Basiswert ab (Berlin 2,7 Mio. € je Jahr, dazu r_S157 im Anpassungspotenzial). Für δ_VG und δ_KZ gibt es eine Wächter-Frage, für S157 nicht | s_gek als Anteil der Heimplätze fassen, die zusätzlich zum Stand der Kalibrierjahre gekühlt sind. Eine Wächter-Frage wie bei heat.vg_in_kalibrierjahren stellen oder die Eingabe so benennen. Die Voreinstellung nach P2 neu herleiten, nicht still null: Zahl, Band, Berlin-Betrag, Gegenargument, etwa aus dem Zuwachs zwischen [72] 2015 und 2025. Alternativ mit Quelle belegen, dass der Bestand in c_kal nicht wirkt. §5, Block (die `wert:`-Änderung ist durch diesen Befund gedeckt), Beispiel-Block s157_voreinstellung, r_S157 und Log 45 nachziehen | B | `python3 -c "import sys; s=open('docs/methodik/95_hitzebelastung.md',encoding='utf-8').read(); t=s[s.index('## 5 '):s.index('## 6 ')]; a=t[t.index('- **Gekühlte Räume'):t.index('- **Öffentliche Kühlzentren')]; k=s[s.index('## 7 '):s.index('## 8 ')]; b=k.split('id: heat.s_gek')[1].split('parameter:')[0]; sys.exit(not ('Kalibrierjahr' in a and 'Kalibrierjahr' in b))"` | behoben (T-1584-methodik_manager, Nacharbeit 1): S157 wirkt auf max(s_gek − 0,06; 0); neuer Block `heat.s_gek_kalib` 0,06 (Band 0,04–0,09, Abschätzung von KAP3): Stand 2015 = 11 % [71] × 5,7 / 14,5 [72] = 4,3 %, gleichmäßiges Wachstum 0,67 Prozentpunkte je Jahr, Mittel 2012–2024 = Stand 2018 = 6,3 %. Die Kommune gibt weiter ihren heutigen Anteil ein (Voreinstellung 0,11 und Band 0,05–0,15 unverändert, deshalb bleiben die Stellen in A wahr), den Abzug rechnet das Produkt; eine Wächter-Frage ja oder nein ist verworfen, weil ein Anteil kein Ja oder Nein ist. Berlin bei der Voreinstellung 1,2 statt 2,7 Mio. € je Jahr, r_S157 0,00345, Anpassungspotenzial 0,053; §5, Blöcke `heat.s_gek` und `heat.s_gek_kalib`, Beispiel-Block `s157_voreinstellung`, Log 45 (Historie) und neuer Log 50 nachgezogen. Einzige neue `wert:`-Zeile: `heat.s_gek_kalib` |
| 166 | docs/methodik/95_hitzebelastung.md §5 Hebel S157, Berlin, Z. 1131 | Rechenweg rechnet mit gerundeter Zahl nicht auf (LF 11 E5) | ‚52,9 × 0,71 = 37,4‘ ergibt 37,6; der Block rechnet 52,88 × 0,7064 = 37,35 | ‚52,9 × 0,706 = 37,4‘ oder den ungerundeten Weg nennen | C | `! grep -qF '52,9 × 0,71 = 37,4' docs/methodik/95_hitzebelastung.md` | behoben (T-1584-methodik_manager, Nacharbeit 1): ungerundeter Weg 153,6 × 0,3443 = 52,88 und 52,88 × 0,7064 = 37,35 (52,9 × 0,706 ergäbe 37,3, nicht 37,4); Beispiel-Block `s157_berlin` prüft 52,88 und 37,35 auf zwei Stellen |
| 167 | docs/methodik/95_hitzebelastung.md Kap. 7, Kommentare in heat.delta_vg Z. 1665 und heat.delta_vg_morb Z. 1671 | Rechenweg mit gerundeter Zahl (Folge der Befunde 155 und 161) | ‚1 - 0,20 x 0,34‘ und ‚1 + 0,20 x 0,34‘ ergeben 0,932 und 1,068; §5 und die Zeichentabelle rechnen seit 155/161 mit 0,3445. Der Block schutzprogramme_berlin rechnet w mit 24,372 (0,3441), der Text mit 24,4 (0,3445); beides ergibt auf drei Stellen 0,931 und 1,069 | in beiden Kommentaren 0,3445 schreiben, keine `wert:`-Zeile ändern | C | `! grep -qE '0,20 x 0,34[^0-9]' docs/methodik/95_hitzebelastung.md` | behoben (T-1584-methodik_manager, Nacharbeit 1): beide Kommentare mit 0,3445, keine `wert:`-Zeile geändert |
| 111 | Kapitel 7, alle Blöcke | Fortschreibung des Prüfausdrucks (Befunde 150, 151) | Kapitel 7 hat mit `heat.vg_in_kalibrierjahren` und `heat.kappung_vg` 29 statt 27 Blöcke | Ausdruck mit 29 Blöcken | B | `python3 -c "import re,sys; s=open('docs/methodik/95_hitzebelastung.md',encoding='utf-8').read(); b=s[s.index('## 7 '):s.index('## 8 ')].split('parameter:')[1:]; sys.exit(not (len(b) == 30 and all(re.search(r'^ *kennzeichnung: (\S+)', x, re.M).group(1) in ('quelle', 'abschaetzung_kap3', 'berechnet') for x in b) and all(re.search(r'^ *abgeleitet_aus: .heat', x, re.M) for x in b if 'kennzeichnung: berechnet' in x)))"` | behoben, Prüfausdruck fortgeschrieben in Runde 36 (T-1584-methodik_manager, Nacharbeit 1) wegen des neuen Blocks heat.s_gek_kalib (Befund 165): 30 Blöcke |
| 138 | §5 Hebel S157 (\(s_{\text{gek}}\)), Log 44/45, Kapitel 7 | Nullwirkung ohne Eingabe (P2) | Ohne Eingabe der Kommune blieb S157 ohne Betrag | Entscheidung methodik_manager (Runde 31): Voreinstellung nach P2 für die ganze Kommune, Block `heat.s_gek`. Umgesetzt: \(s_{\text{gek}}\) = 11 % der Pflegeheime mit Klimaanlage [71] × 1 = 0,11, Band 0,05–0,15 (oben 14,5 % der Neubauten des Sozialwesens 2025 [72]), `abschaetzung_kap3`; Sensitivität Berlin (Kette) 2,7 Mio. € je Jahr (1,2–3,7 Mio. €, 0,3–1,0 % des Jahresbetrags), Zelllauf 2,4 Mio. €, Warmsen 1.032 € | B | `python3 -c "import sys; s=open('docs/methodik/95_hitzebelastung.md',encoding='utf-8').read(); k=s[s.index('## 7 '):s.index('## 8 ')]; b=k.split('id: heat.s_gek')[1].split('parameter:')[0]; t=s[s.index('## 5 '):s.index('## 6 ')]; sys.exit(not ('wert: 0.11' in b and 'band: [0.05, 0.15]' in b and 'kennzeichnung: abschaetzung_kap3' in b and '= 0,11 (Abschätzung von KAP3, Block' in t and 'Nullwirkung ist keine Voreinstellung (P2)' in t and '25,0 Mio. € × 0,05 =' in t and 'id: heat.s_gek_kalib' in k and 'python test: s157_voreinstellung' in s and '[72]** Statistisches Bundesamt' in s))"` | behoben, Prüfausdruck fortgeschrieben in Runde 36 (T-1584-methodik_manager, Nacharbeit 1): die Voreinstellung 0,11 bleibt, S157 wirkt nach Befund 165 auf 0,11 − 0,06 = 0,05 (Berlin 1,2 Mio. €) |
| 149 | §5 Hebel S157, Charakterisierung (Anpassungspotenzial) | Nullwirkung in der Charakterisierung (P2) | S157 zählte im Anpassungspotenzial mit 0; es sank auf 0,050 (früher 0,18) | Entscheidung methodik_manager (Runde 31): S157 mit seiner Voreinstellung. Umgesetzt: \(r_{\text{S157}} = a_{85+} \times h_{\text{Heim}} \times s_{\text{gek}} \times (1 - g_{\text{S157}})\) = 0,284 × 0,344 × 0,05 × 0,706 = 0,00345; mit dem Hitzeaktionsplan 1 − 0,95 × (1 − 0,00345) = 0,053; Warmsen 0,056; Gruppe nach KWRA unverändert (unter 0,1). Verworfen: \(1 - g_{\text{S157}}\) = 0,71 unmittelbar (zählte den Heim-Exzess als ganze Hitzemortalität) | B | `python3 -c "import sys; s=open('docs/methodik/95_hitzebelastung.md',encoding='utf-8').read(); t=s[s.index('## 5 '):s.index('## 6 ')]; sys.exit(not ('S157 mit seiner Voreinstellung' in t and '= 0,284 × 0,344 × 0,05 × 0,706 = 0,00345' in t and '1 − 0,95 × (1 − 0,00345) = 0,053' in t and 'abs(1 - 0.95 * (1 - r) - 0.053)' in s))"` | behoben, Prüfausdruck fortgeschrieben in Runde 36 (T-1584-methodik_manager, Nacharbeit 1): r_S157 mit s_gek − 0,06 nach Befund 165, 0,00345 und Anpassungspotenzial 0,053 |

## Runde 37 des methodik_manager zu T-1584-methodik_manager Abschnitt B (27.09.2026) — neue Befunde ab Nr. 168

Urteil des methodik_manager vom 27.09.2026, 12:56 Uhr UTC (Runde 37, Null-Runde: nein): 1 B-Befund (168), 6 C-Befunde
(169–174). Die Befunde 163–167 aus Runde 36 sind dort in der Sache als behoben bestätigt. Nachgezogen in der zweiten
Nacharbeitsrunde von T-1584. Das nächste Urteil zu Abschnitt B ist Runde 38.

**Was sich ändert.** Kap. 7 Block `heat.g_s157`: Der Kommentar rechnet mit max(s_gek - 0,06; 0) (Befund 168). Abschnitt
A, ausdrücklich von Befund 169 verlangt, einzige Stelle in A: Kap. 1, Knotentabelle Zeile S157 (Z. 59), „im gekühlten
Anteil über dem Stand der Kalibrierjahre, \(\max(s_{\text{gek}} - 0{,}06;\ 0)\) (Voreinstellung 0,11, §5)“. §5 Hebel
S157: Die Rückverlängerung des Trends auf 2012–2014 ist als Setzung von KAP3 genannt (Stand 2012 = 2,3 %), die
Alternative „Stand vor 2015 bleibt bei 4,3 %“ steht als Gegenargument (2) mit 6,6 % (0,066, im Band) und Berlin
1,1 Mio. € (Befund 170). Im Block `heat.s_gek_kalib` steht dieselbe Setzung. Berlin „Rechnerisch je vollen Anteil“ mit
dem Hinweis, dass höchstens 0,94 zusätzlich möglich sind (Befund 171). Sensitivität „24,99 Mio. € × 0,05 = 1,249,
gerundet 1,2 Mio. €“ (Befund 172). Der Beispiel-Block `s157_voreinstellung` prüft Stand 2012, das Mittel der 13 Jahre,
6,6 %, 24,99 und 1,249. Entscheidungslog: Eintrag 50 steht hinter Eintrag 49 (Befund 173). Ledger: fortgeschriebene
Zeile zu Befund 149 (Befund 174).

**Unverändert:** jede `wert:`-Zeile (die einzige neue gegenüber origin/main bleibt `heat.s_gek_kalib` aus Befund 165) und
alle Beträge: Kette 362,9 Mio. €, Hitzeaktionsplan 18,1 Mio. €, S157 bei der Voreinstellung 1,2 Mio. €, Kühlzentren
0,75 Mio. €, Schutzprogramme 11,7 Mio. €, Kappung 34,9 Mio. €, Sensitivitäten von \(f_a\) und \(\bar L_a\).

| Nr | Stelle | Art | Begründung | Vorschlag | Kat. | Prüfausdruck | Status |
|---|---|---|---|---|---|---|---|
| 168 | docs/methodik/95_hitzebelastung.md Kap. 7, Block `heat.g_s157`, Kommentar in `kennzeichnung` (Z. 1699) | Widerspruch Kap. 7 ↔ §5 (LF 4, LF 5, LF 10) | Dort steht noch „Wirkt nur auf D_85+ x h_Heim x s_gek, mit heat.delta_hap zusammen auf D_85+ x delta_hap x h_Heim x s_gek“. Das widerspricht der Formelzeile in §5 Z. 1099 und Log 50 (max(s_gek − 0,06; 0)); der cto baut aus Kap. 7 | beide Stellen in „max(s_gek - 0,06; 0)“ ändern, mit Verweis auf heat.s_gek_kalib und Befund 165; keine `wert:`-Zeile ändern | B | `! grep -qF 'x h_Heim x s_gek,' docs/methodik/95_hitzebelastung.md && ! grep -qE 'delta_hap x h_Heim x s_gek *(\(\|;\|$)' docs/methodik/95_hitzebelastung.md` | behoben (T-1584-methodik_manager, Nacharbeit 2): beide Stellen mit max(s_gek - 0,06; 0), Verweis auf heat.s_gek_kalib und Befund 165; `wert:` unverändert |
| 169 | docs/methodik/95_hitzebelastung.md Kap. 1, Knotentabelle Zeile S157 (Z. 59); Stelle in A, von diesem Befund ausdrücklich verlangt | Widerspruch Kap. 1 ↔ §5 (LF 5, LF 15) | Dort steht „… im gekühlten Anteil s_gek (Voreinstellung 0,11, §5)“. Seit Befund 165 wirkt S157 nur auf den Anteil über dem Stand der Kalibrierjahre | „… im gekühlten Anteil über dem Stand der Kalibrierjahre, max(s_gek − 0,06; 0) (Voreinstellung 0,11, §5)“ | C | `grep -qF 'im gekühlten Anteil über dem Stand der Kalibrierjahre' docs/methodik/95_hitzebelastung.md` | behoben (T-1584-methodik_manager, Nacharbeit 2): Z. 59 wie vorgeschlagen; einzige Änderung in Abschnitt A |
| 170 | docs/methodik/95_hitzebelastung.md §5 Hebel S157, Herleitung Bestand der Kalibrierjahre (Z. 1126–1128); Block `heat.s_gek_kalib` | Setzung nicht genannt (LF 13, P1) | Das Mittel der Jahre 2012–2024 ist nur dann gleich dem Stand 2018, wenn der Trend auch 2012–2014 gilt (Stand 2012 = 2,3 %). Bliebe der Stand vor 2015 bei 4,3 %, läge das Mittel bei 6,6 %, gerundet 0,07 | Rückverlängerung als Setzung von KAP3 mit Stand 2012 nennen, Alternative 0,066 als Gegenargument aufnehmen; `wert:` bleibt | C | `grep -qF 'Stand 2012 = 4,3 % − 3 × 0,67 % = 2,3 %' docs/methodik/95_hitzebelastung.md && grep -qF '6,6 % (0,066, im Band 0,04–0,09)' docs/methodik/95_hitzebelastung.md && grep -qF 'derselbe Trend gilt 2012-2014' docs/methodik/95_hitzebelastung.md` | behoben (T-1584-methodik_manager, Nacharbeit 2): Setzung mit Stand 2012 = 2,3 % in §5 und im Block; Gegenargument (2): Mittel 6,6 % (0,066), Wirkung 0,044, Berlin 1,1 statt 1,2 Mio. €; Beispiel-Block prüft Mittel der 13 Jahre und 6,6 %; `wert:` bleibt 0.06 |
| 171 | docs/methodik/95_hitzebelastung.md §5 Hebel S157, Absatz Berlin (Z. 1172) | Zustand, den es nicht geben kann (LF 11 E2) | „Wäre der ganze Bestand zusätzlich zum Stand der Kalibrierjahre gekühlt (Anteil 1)“; höchstens 0,94 ist zusätzlich möglich | „Rechnerisch je vollen Anteil (Anteil 1 über dem Stand der Kalibrierjahre) fielen …“, der Satz mit 0,94 × 25,0 = 23,5 Mio. € bleibt | C | `! grep -qF 'Wäre der ganze Bestand zusätzlich' docs/methodik/95_hitzebelastung.md && grep -qF 'Rechnerisch je vollen Anteil' docs/methodik/95_hitzebelastung.md` | behoben (T-1584-methodik_manager, Nacharbeit 2): wie vorgeschlagen, dazu „Diesen Zustand gibt es nicht, höchstens 0,94 sind zusätzlich möglich“; 0,94 × 25,0 = 23,5 Mio. € bleibt |
| 172 | docs/methodik/95_hitzebelastung.md §5 Hebel S157, Sensitivität (Z. 1138) | Rechenweg rechnet mit gerundeter Zahl nicht auf (LF 11 E5) | „25,0 Mio. € × 0,05 = 1,2 Mio. €“ ergibt 1,25 | ungerundeten Weg nennen, „24,96 Mio. € × 0,05 = 1,248, gerundet 1,2 Mio. €“ | C | `! grep -qF '25,0 Mio. € × 0,05 =' docs/methodik/95_hitzebelastung.md && grep -qF '× 0,05 = 1,249, gerundet' docs/methodik/95_hitzebelastung.md` | behoben (T-1584-methodik_manager, Nacharbeit 2): „je vollen Anteil 24,99 Mio. € × 0,05 = 1,249, gerundet 1,2 Mio. €“. Nachgerechnet ist die Wirkung je Anteil 24,986 Mio. € (153,6 × 0,34427 × 0,70636 × 4,16 × 160.800), nicht 24,96; der Beispiel-Block prüft 24,99 und 1,249 |
| 173 | docs/methodik/95_hitzebelastung.md Entscheidungslog (Z. 2328) | Reihenfolge (LF 14) | Eintrag 50 steht zwischen 45 und 46 | Zeile hinter Eintrag 49 stellen | C | `python3 -c "import sys; s=open('docs/methodik/95_hitzebelastung.md',encoding='utf-8').read(); sys.exit(not (s.index('\| 49 ⚠ \|') < s.index('\| 50 ⚠ \|') and s.index('\| 46 ⚠ \|') < s.index('\| 50 ⚠ \|')))"` | behoben (T-1584-methodik_manager, Nacharbeit 2): Eintrag 50 steht hinter 49; die Verweise in Log 45 und in der Einleitung bleiben |
| 174 | reviews/BEFUNDE_95.md, fortgeschriebene Zeile zu Befund 149 im Abschnitt Runde 36 | Formel und Zahl passen nicht zum Bericht (LF 14) | Die Formel steht dort mit „s_gek“, eingesetzt ist aber 0,05 = s_gek − 0,06, und „Warmsen 0,056“, obwohl der Bericht jetzt 0,053 nennt | die Formel mit (s_gek − 0,06) schreiben und „Warmsen 0,053“ setzen, als fortgeschriebene Zeile | C | `python3 -c "import sys; z=[l for l in open('reviews/BEFUNDE_95.md',encoding='utf-8') if l.startswith('\| 149 \|')][-1]; sys.exit(not ('Warmsen 0,053' in z and '- 0{,}06)' in z and 'Warmsen 0,056' not in z))"` | behoben (T-1584-methodik_manager, Nacharbeit 2): fortgeschriebene Zeile zu 149 unten, Prüfausdruck von 149 unverändert |
| 149 | §5 Hebel S157, Charakterisierung (Anpassungspotenzial) | Nullwirkung in der Charakterisierung (P2) | S157 zählte im Anpassungspotenzial mit 0; es sank auf 0,050 (früher 0,18) | Entscheidung methodik_manager (Runde 31): S157 mit seiner Voreinstellung. Umgesetzt: \(r_{\text{S157}} = a_{85+} \times h_{\text{Heim}} \times (s_{\text{gek}} - 0{,}06) \times (1 - g_{\text{S157}})\) = 0,284 × 0,344 × 0,05 × 0,706 = 0,00345; mit dem Hitzeaktionsplan 1 − 0,95 × (1 − 0,00345) = 0,053; Warmsen 0,053; Gruppe nach KWRA unverändert (unter 0,1). Verworfen: \(1 - g_{\text{S157}}\) = 0,71 unmittelbar (zählte den Heim-Exzess als ganze Hitzemortalität) | B | `python3 -c "import sys; s=open('docs/methodik/95_hitzebelastung.md',encoding='utf-8').read(); t=s[s.index('## 5 '):s.index('## 6 ')]; sys.exit(not ('S157 mit seiner Voreinstellung' in t and '= 0,284 × 0,344 × 0,05 × 0,706 = 0,00345' in t and '1 − 0,95 × (1 − 0,00345) = 0,053' in t and 'abs(1 - 0.95 * (1 - r) - 0.053)' in s))"` | behoben, Zeile fortgeschrieben in Runde 37 (T-1584-methodik_manager, Nacharbeit 2, Befund 174): Formel mit (s_gek − 0,06) wie im Bericht, Warmsen 0,053; Prüfausdruck unverändert |
| 138 | §5 Hebel S157 (\(s_{\text{gek}}\)), Log 44/45, Kapitel 7 | Nullwirkung ohne Eingabe (P2) | Ohne Eingabe der Kommune blieb S157 ohne Betrag | Entscheidung methodik_manager (Runde 31): Voreinstellung nach P2 für die ganze Kommune, Block `heat.s_gek`. Umgesetzt: \(s_{\text{gek}}\) = 11 % der Pflegeheime mit Klimaanlage [71] × 1 = 0,11, Band 0,05–0,15 (oben 14,5 % der Neubauten des Sozialwesens 2025 [72]), `abschaetzung_kap3`; Sensitivität Berlin (Kette) 2,7 Mio. € je Jahr (1,2–3,7 Mio. €, 0,3–1,0 % des Jahresbetrags), Zelllauf 2,4 Mio. €, Warmsen 1.032 € | B | `python3 -c "import sys; s=open('docs/methodik/95_hitzebelastung.md',encoding='utf-8').read(); k=s[s.index('## 7 '):s.index('## 8 ')]; b=k.split('id: heat.s_gek')[1].split('parameter:')[0]; t=s[s.index('## 5 '):s.index('## 6 ')]; sys.exit(not ('wert: 0.11' in b and 'band: [0.05, 0.15]' in b and 'kennzeichnung: abschaetzung_kap3' in b and '= 0,11 (Abschätzung von KAP3, Block' in t and 'Nullwirkung ist keine Voreinstellung (P2)' in t and '× 0,05 = 1,249, gerundet' in t and 'id: heat.s_gek_kalib' in k and 'python test: s157_voreinstellung' in s and '[72]** Statistisches Bundesamt' in s))"` | behoben, Prüfausdruck fortgeschrieben in Runde 37 (T-1584-methodik_manager, Nacharbeit 2): Befund 172 schreibt die Sensitivität ungerundet, 24,99 Mio. € × 0,05 = 1,249, gerundet 1,2 Mio. € |

## Runde 38 — Gegenprüfung nach Runde 31, Abschnitte A und B (frische Sitzung, 27.09.2026): Null-Runde

Die Gegenprüfung nach §5 lief in zwei Paketen unter dem Vorhaben T-1535-cmo, je in frischer Sitzung des
methodik_manager: Abschnitt A (Kopf bis vor `## 5 `) in T-1598-methodik_manager (Ersatz für T-1583-methodik_manager,
dessen Runden 32 bis 34 ohne Null-Runde blieben), Abschnitt B (`## 5 ` bis zum Ende) in T-1584-methodik_manager. Beide
letzten Urteile lauten „Null-Runde: ja“. Die Null-Runde über den ganzen Bericht ist damit Runde 38, das letzte der beiden
Null-Urteile. Eingetragen mit T-1585-methodik_manager (Paket 3); am Bericht ändert sich nur der Kopf vor `## 1 `.

**Nachweis Abschnitt A.** Firmen-Repo, `tickets/T-1598-methodik_manager.md`, Abschnitt „Urteil“, Eintrag
„2026-09-27T12:34:23Z · Runde 0 · methodik_manager (opus/high)“, **Urteil:** freigabe. Verdiktzeile wörtlich:

VERDIKT #95 T-1598-methodik_manager Abschnitt A Runde 35 · Null-Runde: ja. Keine neuen A- oder B-Befunde. Es gibt einen neuen C-Befund (162, siehe unten); er hält die Null-Runde nicht auf.

Merge nach `main`: Commit 95dda1b8. Der C-Befund 162 steht seit Runde 36 im Ledger (offen).

**Nachweis Abschnitt B.** Firmen-Repo, `tickets/T-1584-methodik_manager.md`, Abschnitt „Urteil“, Eintrag
„2026-09-27T13:04:54Z · Runde 2 · methodik_manager (opus/high)“, **Urteil:** freigabe. Verdiktzeile wörtlich:

VERDIKT #95 T-1584-methodik_manager Abschnitt B Runde 38 · Null-Runde: ja

Merge nach `main`: Commit aced8021. „Runde 0“ und „Runde 2“ sind die Zählung im jeweiligen Ticket; im Ledger sind es die
Runden 35 und 38. Das Urteil zu B hat die einzige Änderung an A seit Runde 35 (Kap. 1, Knotentabelle Zeile S157, Z. 59,
Befund 169) mitgelesen, ohne Befund.

**Leitfragen nach §5.** Der Skill `methodik_manager-gegenpruefung` nennt 14 Leitfragen; LF 15 haben beide Urteile von
Hand nach Aufgabe §5 Nr. 15 und §6 Nr. 2 geprüft.

| Leitfrage | Verdikt | Abschnitt |
|---|---|---|
| LF 1 Kette | bestanden: alle elf Knoten in der Knoten-Bilanz, S154 und W123 begründet inaktiv (Log 11, Log 15); Hebel S155, S157, S158, S152 in §5 verarbeitet | beide (A: Knoten-Bilanz; B: Hebel) |
| LF 2 Verteilschlüssel | bestanden: Mortalität ohne Treiber etwa 0, Morbiditätssockel als Grenze in §3.4 und §4 | A (B: „in Abschnitt A“) |
| LF 3 Physische Zwischengröße | bestanden: D_a, YLL und F je Zelle (§3.5); jeder Hebel über Todesfälle zu YLL und € | beide |
| LF 4 Doppelzählung | bestanden: HD_ref zweiseitig, Warnwirkung in c_kal (Wächter), R9 mit #101; δ_HAP gegen c_kal abgegrenzt, δ_VG und δ_KZ über die Wächter-Frage, S157 über den Abzug 0,06, Kappung 0,794, R7-Weiche zu #65 | beide |
| LF 5 Modifikatoren | bestanden: β_iso 0,897 und β_pfl 1,54 zentriert; alle δ multiplikativ auf (RR − 1) | beide |
| LF 6 Struktur | bestanden: Kopplungen f_a↔m_a und L̄_85+; h_Heim je Zelle, Kopplung HAP × VG × KZ gekappt | beide |
| LF 7 Tails/Parameter | bestanden: Wochenquantile empirisch, σ = 0,5 K offengelegt; jeder Hebelparameter mit Band | beide |
| LF 8 Kalibrierung | bestanden: ein Skalar 0,581, 12/16 Länder, Voll-Holdout 12/16, Berlin-Anker −18 % ausgewiesen; der Neufit 0,651 und 0,534 in B aus §5 übernommen | A (B: „in Abschnitt A“) |
| LF 9 Kostensätze | bestanden: VOLY 160.800 €, c_Fall 7.152 €, Preisstand 2024 einheitlich | beide |
| LF 10 Quellen | bestanden: Lint und Register Kap. 2; jeder Verweis in B steht in Kap. 8, [15] ist Climate Change 24/2021 | beide |
| LF 11 Form und Erklärbarkeit (E1–E5) | bestanden, mit den C-Resten 162 (A), 175 und 176 (B); E1 Rechenkette §3.0 mit zehn Ebenen, E2 Rechenbeispiel je Hebel, E3 einfachere Rechnung je beziffert | beide |
| LF 12 Umsetzbarkeit | bestanden: keyless, Datenebenen spezifiziert; 30 Blöcke vollständig, Code-Nachzug beim cto | beide |
| LF 13 Herleitungspflicht | bestanden: jedes Zeichen in §3.6 mit Herleitung oder „Abschätzung von KAP3“; δ_HAP, s_gek_kalib, δ_KZ, δ_VG, Kappung nachgerechnet | beide |
| LF 14 Quellen-Synchronität | bestanden: Monetarisierung Blattzeile 100 und Abgleich-Protokoll stimmen; C-Rest 177 (Log 39) | beide |
| LF 15 Risiko ohne (weitere) Anpassung | bestanden, von Hand geprüft nach Aufgabe §5 Nr. 15 und §6 Nr. 2, weil der Skill 14 Leitfragen nennt: KWRA-Stufe aus `docs/KWAR/KWRA-2021_Klimawirkungen.xlsx`, Zeile 97 (ID 95) deckt sich mit Kap. 1; (a) ordnet den Basiswert dem Zustand ohne (weitere) Anpassung zu, (b) zeigt „mit Anpassung“ nur als Hebel; alle Wächter in §5 passen dazu | beide |

**Leseliste Abschnitt A** (Urteil zu T-1598, zeilenweise gelesen Z. 1 bis Z. 1043, jede Überschrift):
- Kopf: `# Methodik-Bericht #95 — Hitzebelastung`, Statuszeile, Revisionsstand;
- `## 1 Wirkungskette & Knoten-Bilanz (§2.1)` mit `### Knoten-Bilanz`, `### Weitergaben (zweispaltig; Quelle:
  Netzwerkliste + Abgleich-Protokoll)`, `### Konto-Einbettung`, `### Risiko ohne (weitere) Anpassung`;
- `## 2 Evidenz-Register (§2.2)`;
- `## 3 Modell (§2.3) — Ansatz 95-A, Schicht B` mit `### 3.0 Rechenkette` (samt Prüfblock `rechenkette_95`),
  `### 3.1 Zelltemperatur (vorgelagerter Knoten W124; produktseitig implementiert)`, `### 3.2 Wochenverteilung
  (empirische intra-saisonale Quantile; §3.2-Tails)`, `### 3.3 Mortalität (nativer Ausweis YLL)` (Ersatzregel, Tabelle,
  Rechenbeispiel Warmsen, β-Ablesekette, (a) f_a, (b) β_pfl), `### 3.4 Morbidität (altersgeschichtet, §3.2-Struktur)`,
  `### 3.5 Monetarisierung (K1) und Aggregation`, `### 3.6 Zeichentabelle (alphabetisch; §3.2-Form)` mit Datenebenen,
  `### 3.7 Schicht A (getrennt; nie auf €-Pfaden)`;
- `## 4 Kalibrierung & Validierung (§2.4/§3.4)`;
- mitgelesen ab `## 5 `: §5 Hebel Schutzprogramme (Befunde 161 und 158), Kap. 7 Block zu Befund 158, Entscheidungslog
  Nr. 24 gegen Nr. 28.

**Leseliste Abschnitt B** (Urteil zu T-1584 Runde 38, jede Überschrift ab `## 5 `):
- `## 5 Maßnahmen-Hebel (§2.5/§3.5)`, zeilenweise Z. 1044–1378: Hitzeaktionsplan / Frühwarnkette (S155/S158) mit
  Herleitung δ_HAP, Berliner Betrag und Wächter; Gekühlte Räume / Klimaanlagen in Pflegeheimen (S157) mit s_gek,
  s_gek_kalib, h_Heim je Zelle, Anpassungspotenzial, Kombination mit δ_HAP, „Beide Fassungen“ und R7-Weiche; Öffentliche
  Kühlzentren (δ_KZ); Schutzprogramme vulnerable Gruppen (δ_VG, δ_VG,morb, Wächter `heat.vg_in_kalibrierjahren`, Kappung
  0,794); Sensitivität von f_alter; Sensitivität von l_restlebenserwartung;
- `## 6 Szenario-Anwendung & Modellgrenzen (§3.2/§3.6)`, zeilenweise Z. 1380–1437: Szenario-Anwendung 95-A,
  Stationaritätsannahmen, Jahresbeträge ohne Abzinsung, Modellgrenzen 1–5, Infokasten-/UI-Texte, Raten-Darstellung und
  Aggregation;
- `## 7 Parameter-Blöcke (maschinenlesbar, §4)`: 30 Blöcke maschinell über den Lint (Vollständigkeit, Kennzeichnung,
  Beispiel-Blöcke ausgeführt); zeilenweise die seit Runde 37 geänderten Blöcke `heat.g_s157`, `heat.s_gek`,
  `heat.s_gek_kalib`, `s157_voreinstellung` und `schutzprogramme_berlin`;
- `## 8 Quellen (§3.8 — #95-relevanter Auszug; Nummern [11]–[62] = M0-Zählung)`, zeilenweise, alle Quellen [11]–[76];
- `## Entscheidungslog`, zeilenweise, Einleitung und Einträge 1–50;
- außerhalb von B mitgelesen: Kap. 1 Knotentabelle Zeile S157 (Z. 59) und Kap. 1 (a)/(b) für LF 15.

Beide Listen zusammen decken jede Überschrift des Berichts ab; geprüft ist der ganze Bericht, nicht nur ein Diff.

**Maschinell** (ausgeführt am 27.09.2026 auf dem Stand von `main` nach beiden Merges): `python3
backend/scripts/lint_methodik.py 95` meldet „304 Checks grün“ und „ALLE LINTS GRÜN“. `python3 backend/scripts/ledger.py 95
--pruefe` meldet vor diesem Eintrag 158 Befunde, zurückgestellt 1 (116), belegt geschlossen 79, „Prüfausdruck ROT   : 0“
und die Schlusszeile „GRÜN — kein Prüfausdruck eines geschlossenen Befunds schlägt fehl.“ Nach diesem Eintrag: 161
Befunde, zurückgestellt 4 (116, 175, 176, 177; die drei roten Ausdrücke von 175–177 sind der zurückgestellte
Sollzustand), belegt geschlossen 79, „Prüfausdruck ROT   : 0“, Schlusszeile „GRÜN — …“. Der Lint bleibt bei „304
Checks grün“ und „ALLE LINTS GRÜN“.

**Beträge** (je Jahr, Preisstand 2024):
- Berlin, Kette (§3.0, Block `rechenkette_95`, im Lint grün): Mortalität 2.250 YLL × 160.800 € = 361,8 Mio. €, Morbidität
  152,00 Fälle × 7.152 € = 1,09 Mio. €, zusammen 362,9 Mio. €; nachgerechnet im Urteil zu A.
- Berlin, Golden: 342,67 Mio. € (Zelllauf mit Regel, §3.3 Tabelle Z. 475, gemessen 27.09.2026 mit
  `95_zellvergleich.py --gemeinde 11000000 --ersatz`). Wie im Urteil zu A nicht im Zelllauf nachgemessen, Herkunft §3.3:
  `pytest -q backend/tests/test_methodik_95_golden_betraege.py` brach dort beim Import ab (`ImportError: cannot import
  name 'box' from 'shapely.geometry'`); das Urteil zu B meldet `test_methodik_95_golden.py` mit 12 passed, der Test fragt
  342,67 Mio. € aber nicht ausdrücklich ab.
- Warmsen (AGS 03256034): 173.099 € mit Regel, 145.025 € ohne Gemeindeschlüssel (§3.3 Tabelle Z. 476, gemessen
  27.09.2026 mit `--gemeinde 03256034 --ersatz`).

**Zurückgestellt**, jeweils Code-Nachzug beim cto nach eiserner Regel 5, ohne neue Befundzeile:
- Befund 116: Ersatzregel für den geheimgehaltenen Anteil 65+ in `backend/app/services/zensus_loader.py` (Log 41).
- Die Blöcke aus Kapitel 7 ohne Registry-Parameter, geführt in `_AUSSTEHEND_CTO`
  (`backend/tests/test_methodik_95_bloecke.py`): `heat.s_gek`, `heat.h_heim`, `heat.delta_kuehlzentren`,
  `heat.vg_in_kalibrierjahren`, `heat.kappung_vg`; dazu der neue Block `heat.s_gek_kalib` (Befund 165) und der Berliner
  Betrag des Hitzeaktionsplans, die laut Urteil zu B ebenfalls beim cto nachzuziehen sind.

**C-Befunde ohne Sperrwirkung.** 162 (Stelle in A, seit Runde 36 im Ledger) und die drei C-Befunde aus dem Urteil zu
B, Runde 38, die das Urteil zur Übernahme ins Ledger weitergibt. 175 bis 177 stehen unten wie im Urteil, Stelle,
Prüfausdruck und Kategorie unverändert. Nach dem Urteil „gehen sie mit der nächsten Änderung in ein Folgepaket“; dieses
Paket darf den Bericht nur vor `## 1 ` ändern. Sie sind deshalb terminiert zurückgestellt nach Aufgabe §6 (Termin: nächste
Änderung am Bericht), ihr Prüfausdruck ist bis dahin rot und beschreibt den Sollzustand. Eine Null-Runde halten C-Befunde
nicht auf.

| Nr | Stelle | Art | Begründung | Vorschlag | Kat. | Prüfausdruck | Status |
|---|---|---|---|---|---|---|---|
| 175 | docs/methodik/95_hitzebelastung.md Kap. 8 [69] Z. 2205 („Warmsen: 3158 ·“); Entscheidungslog Nr. 41 Z. 2336 („in Warmsen 1416 Einwohner“, „(1342 Gemeinden“) | Stil nach kap3-stil „Tausenderpunkt ab 1.000“ (LF 11 E5) | Befund 160 hat dieselben Zahlen in §3.3 nachgezogen, in B nicht; der Lint prüft den Tausenderpunkt nicht | 3.158, 1.416 und 1.342 schreiben | C | `! grep -qF 'Warmsen: 3158 ·' docs/methodik/95_hitzebelastung.md && ! grep -qF 'Warmsen 1416 Einwohner' docs/methodik/95_hitzebelastung.md && ! grep -qF '(1342 Gemeinden' docs/methodik/95_hitzebelastung.md` | behoben (T-1643-methodik_manager): Kap. 8 [69] „Warmsen: 3.158 ·“, Log 41 „in Warmsen 1.416 Einwohner“ und „(1.342 Gemeinden“; vorher zurückgestellt (Termin: nächste Änderung am Bericht) — Kategorie C |
| 176 | docs/methodik/95_hitzebelastung.md §5 Schutzprogramme Z. 1300 („von 2,9 bis 23,3 Mio. €“); Log 43 Z. 2338 („kommt auf 23,3 Mio. €“); Block schutzprogramme_berlin Z. 1897 | Rechenweg rechnet mit der gezeigten Zahl nicht auf (LF 11 E5; Folge der Befunde 155/167) | Der Text rechnet mit w_VG = 0,3445 (Z. 1251): 169,5 × 0,40 × 0,3445 = 23,36, also 23,4. Der Block rechnet mit 24,372 (0,3441) und kommt auf 23,33 | 23,4 schreiben und im Block für die Reichweite 0,40 mit 0,3445 prüfen, oder beim Wert „w ungerundet 0,3441“ vermerken; keine wert:-Zeile ändern | C | `! grep -qF 'von 2,9 bis 23,3 Mio. €' docs/methodik/95_hitzebelastung.md && ! grep -qF 'kommt auf 23,3 Mio. €' docs/methodik/95_hitzebelastung.md` | behoben (T-1643-methodik_manager): §5 Schutzprogramme und Log 43 nennen 23,4 Mio. €; der Block `schutzprogramme_berlin` prüft die Reichweite 0,40 mit w = 0,3445 auf 23,4 Mio. € und vermerkt w ungerundet 0,3441 (23,33 Mio. €); keine wert:-Zeile geändert; vorher zurückgestellt (Termin: nächste Änderung am Bericht) — Kategorie C |
| 177 | docs/methodik/95_hitzebelastung.md Entscheidungslog Nr. 39 Z. 2334 und Einleitung Z. 2274–2290 | Eintrag durch späteren überholt, ohne Vermerk (LF 14) | Log 39 begründet mit „Der Bericht hat keine Quelle für die Klimaanlagen-Quote … Pflegeheime …“. Seit Log 50 schätzt der Bericht den Bestand der Kalibrierjahre für Pflegeheime aus [71]/[72] ab; das ist die in Log 39 als Alternative genannte Fortschreibung. Die Einleitung nennt außerdem die Einträge 34–36 nicht | In Log 39 den Vermerk „(Stand T-1119, Historie; für Pflegeheime fortgeschrieben durch Nr. 50)“ setzen; die Wahl bleibt. Einleitung um „Einträge 34–36: …“ ergänzen | C | `python3 -c "import sys; z=[l for l in open('docs/methodik/95_hitzebelastung.md',encoding='utf-8') if l.startswith('\| 39 ⚠ \|')]; s=open('docs/methodik/95_hitzebelastung.md',encoding='utf-8').read(); sys.exit(not (z and 'Nr. 50' in z[0] and 'Einträge 34–36' in s))"` | behoben (T-1643-methodik_manager): Log 39 trägt „(Stand T-1119, Historie; für Pflegeheime fortgeschrieben durch Nr. 50)“, die Wahl bleibt; die Einleitung des Logs nennt „Einträge 34–36: …“; vorher zurückgestellt (Termin: nächste Änderung am Bericht) — Kategorie C |

**Zählung nach A-0046.** Seit der Null-Runde 30 liefen die Runden 31 bis 38: 31 (Divergenzen aus der Integration),
32–35 zu Abschnitt A, 36–38 zu Abschnitt B. Runde 38 ist die Null-Runde; die Zählung endet hier, die Grenze Runde 40 ist
nicht erreicht.

Neue Befunde: keine (keine neuen A- oder B-Befunde; 175–177 sind die C-Befunde des Urteils zu B, hier nur übernommen).

## Runde 39 — Anlässe aus T-1642-cmo (Code-Nachzug T-1582-ceo): neue Befunde 178–193, C-Reste 162 und 175–177 behoben (T-1643-methodik_manager, 29.09.2026)

Paket 1 von 7 unter dem Vorhaben T-1642-cmo. Nach dem Code-Nachzug T-1582-ceo hat der CMO die Anlässe A bis E und
„Weiteres“ gestellt; dieser Abschnitt führt sie als Befunde 178 bis 193. Zuordnung: A (Kühlzentren) 178 und 179,
B (δ_HAP auf dem Exzess) 180, D (Setzungen) 181 bis 187, E (Golden-Betrag und S157 im Zelllauf) 188 und 193,
„Weiteres“ 189, 191 und 192, C (Kopfzeile) 190. Die C-Reste 162 und 175 bis 177 sind an ihrer Stelle auf behoben
gesetzt. Am Bericht ändern sich nur diese C-Reste und die Kopfzeile; keine `wert:`-Zeile.

**Zeilenangaben.** Die Stellen in diesem Abschnitt nennen die Zeilen des Berichts auf `main` am 29.09.2026, vor
diesem Ticket. Nach diesem Ticket liegen sie tiefer: ab Z. 15 (Kopfzeile eine Zeile länger) um eine Zeile, ab
Z. 1900 (Block `schutzprogramme_berlin`) um zwei, ab Z. 2280 (Einleitung des Entscheidungslogs) um vier.

**Zurückgestellt.** 178 bis 183 sind terminiert zurückgestellt nach Aufgabe §6, je mit einem Folgepaket unter
T-1642-cmo (Nachtrag des methodik_manager zu T-1643-methodik_manager). Ihr Prüfausdruck beschreibt den Sollzustand und ist heute rot. Die
Folgepakete dürfen ihn mit Vermerk schärfen. Den Termin „Code-Nachzug CTO nach T-1642-cmo“ setzen erst sie, wenn nur
noch der Code nachziehen muss.

| Nr | Stelle | Art | Begründung | Vorschlag | Kat. | Prüfausdruck | Status |
|---|---|---|---|---|---|---|---|
| 178 | docs/methodik/95_hitzebelastung.md §5 Öffentliche Kühlzentren Z. 1229 („Im Zelllauf mit Gemeindeschlüssel 0,72 Mio. €“); Block `heat.delta_kuehlzentren` Z. 1781–1782 (wert 0.9956); Knotentabelle Z. 162, Zeichentabelle Z. 829, Log 46 Z. 2343 (0,05 × 0,71 × 3/24); Anpassungspotenzial S157 Z. 1172 (0,706) | Bericht und Produkt nennen verschiedene Beträge; eine Setzung mit zwei Zahlen (LF 13, P1) | Das Produkt rechnet mit dem Registry-Wert 0,9956 für Berlin 709.059,04 €, der Bericht nennt 0,72 Mio. €. Messung des methodik_manager vom 29.09.2026 (T-1642-cmo): mit 0,9955625 sind es 715.102,16 € (Warmsen 319,27 € gegen 316,57 €). Ursache ist die Rundung von δ_KZ: Der Hebel hängt an 1 − δ_KZ = 0,0044375, die Rundung auf 0,9956 nimmt davon 0,0000375 weg, das sind 0,85 % am Hebelbetrag. Dazu steht 1 − g_S157 in w_KZ als 0,71, im Anpassungspotenzial als 0,706 | δ_KZ in Block und Registry so genau führen, dass die Rundung am Berliner Betrag unter 0,1 % bleibt, oder §5 auf den Betrag des Registry-Werts nachziehen; 1 − g_S157 an allen Stellen mit derselben Zahl; weicht der Code danach ab, Übernahmeliste an den CTO | B | `python3 -c "import re,sys; s=open('docs/methodik/95_hitzebelastung.md',encoding='utf-8').read(); b=s.split('id: heat.delta_kuehlzentren',1)[1][:300]; m=re.search(r'wert:\s*0\.(\d+)', b); sys.exit(not (((m and len(m.group(1))>=5) or 'Gemeindeschlüssel 0,71 Mio. €' in s) and '0,05 × 0,71 × 3/24' not in s))"` | zurückgestellt (Termin: Paket 2, T-1644-methodik_manager; Grund: Entscheidung und Änderung am Bericht im Folgepaket) |
| 179 | docs/methodik/95_hitzebelastung.md §5 Kappung max(δ_HAP × δ_VG × δ_KZ; 0,794) Z. 1238 und Z. 1347; Produkt backend/app/services/measure_service.py Z. 354–356 (laut T-1642-cmo, Anlass A) | Kopplung der Faktoren, Bericht gegen Code (LF 4) | Der Bericht kappt das Produkt aller drei Faktoren bei 0,794. Nach Anlass A in T-1642-cmo kappt der Code beim Pfad der Schutzprogramme nur gegen δ_HAP; ob δ_KZ auf jedem Pfad in der Kappung steht, ist nicht belegt | Jeden Pfad messen (mit und ohne Schutzprogramm, mit und ohne Hitzeaktionsplan); an der Kappung im Bericht die Antwort mit Verweis auf Befund 179; weicht der Code ab, Übernahmeliste an den CTO | B | `grep -qF 'Befund 179' docs/methodik/95_hitzebelastung.md` | zurückgestellt (Termin: Paket 2, T-1644-methodik_manager; Grund: Entscheidung und Änderung am Bericht im Folgepaket) |
| 180 | docs/methodik/95_hitzebelastung.md §5 Hitzeaktionsplan / Frühwarnkette (S155/S158), Herleitung δ_HAP ab Z. 1046, Log 10; Kappung Z. 1238 und Z. 1347 | Lesart der Quelle und Andockpunkt (LF 13, LF 4) | δ_HAP = 0,95 liegt als Faktor auf (RR − 1). Misst [45] die Sterblichkeit in Hitzeperioden insgesamt, heißt 0,95 auf den Exzess etwas anderes als 5 % weniger Todesfälle in der Hitzeperiode; es braucht dann die Übersetzung wie bei Befund 124. Dazu wirkt die Kappung bei Teilabdeckung | Lesart an der Fundstelle von [45] entscheiden; gilt die Gesamtsterblichkeit, δ_Exzess = 1 − (1 − δ_HAP) × RR/(RR − 1) mit dem RR von [45]; beide Fassungen im Beispiel-Block, Berliner Betrag vorher und nachher, Kappung mit Teilabdeckung, Log-Eintrag mit dem verworfenen Ansatz | B | `grep -qF 'Befund 180' docs/methodik/95_hitzebelastung.md` | zurückgestellt (Termin: Paket 3, T-1645-methodik_manager; Grund: Entscheidung und Änderung am Bericht im Folgepaket) |
| 181 | docs/methodik/95_hitzebelastung.md §3.0 Wirkung (d) Z. 239–241 und Prüfblock Z. 322; §4 Z. 917–921 und Z. 1014 | Setzung gegen Herleitung (LF 7) | σ = 0,5 K ist gesetzt, die Herleitung in §4 ergibt 2/√12 = 0,58 K. Mit 0,58 K läge der Berliner Betrag nach §4 Z. 920–921 rund 0,7 % höher, mehr als die Toleranz von 0,29 % aus §3.3 | 0,58 K setzen, außer der Bericht begründet 0,5 K mit einem Grund, den die Herleitung nicht kennt (Leitlinie D in T-1642-cmo); ändert sich der Golden-Betrag, geht er in die Übernahmeliste | B | `python3 -c "import sys; s=open('docs/methodik/95_hitzebelastung.md',encoding='utf-8').read(); sys.exit(not ('σ = 0,5 K' not in s or 'Befund 181' in s))"` | zurückgestellt (Termin: Paket 4, T-1646-methodik_manager; Grund: Entscheidung und Änderung am Bericht im Folgepaket) |
| 182 | docs/methodik/95_hitzebelastung.md §3.0 Z. 239–241 (× 1,021 und × 1,019), §4 Z. 917–921 (×1,023–1,024), Z. 1014 (× 1,021) | drei Zahlen für dieselbe Wirkung (LF 11 E5) | Die Wärmeinsel-Feinstruktur unter 1 km steht mit drei Faktoren im Bericht. Ein Leser kann nicht nachvollziehen, welcher im Betrag steckt | ein Faktor mit einer Fundstelle; die anderen Stellen verweisen darauf | B | `python3 -c "import sys; s=open('docs/methodik/95_hitzebelastung.md',encoding='utf-8').read(); sys.exit(sum(x in s for x in ('× 1,019', '× 1,021', '×1,023–1,024')) > 1)"` | zurückgestellt (Termin: Paket 4, T-1646-methodik_manager; Grund: Entscheidung und Änderung am Bericht im Folgepaket) |
| 183 | docs/methodik/95_hitzebelastung.md §5 S157, Anpassungspotenzial Z. 1172–1174 | Konstante statt Wert je Kommune (LF 6) | a_85+ = 0,284 ist der Berliner Anteil des Bands 85+ an den YLL und steht als Konstante im Anpassungspotenzial; in Warmsen ist er 0,224 (Z. 1174). Eine Berliner Konstante stellt ländliche Kommunen falsch dar | a_85+ je Kommune rechnen, wenn die Quelle den Wert je Gemeinde liefert; sonst die Konstante mit dem Fehler für Warmsen ausweisen (Leitlinie D in T-1642-cmo) | B | `grep -qF 'Befund 183' docs/methodik/95_hitzebelastung.md` | zurückgestellt (Termin: Paket 4, T-1646-methodik_manager; Grund: Entscheidung und Änderung am Bericht im Folgepaket) |
| 184 | docs/methodik/95_hitzebelastung.md Block `heat.s_gek_kalib` Z. 1757–1760, Log 50 Z. 2347 | Setzung ohne Quelle (LF 7, P1), entschieden | Entscheidung des methodik_manager (T-1642-cmo, Leitlinie D): s_gek_kalib = 0,06 aus dem Neubauanteil [72] bleibt Abschätzung von KAP3 mit Band [0,04; 0,09], bis eine Quelle für den Bestand gekühlter Heimplätze vorliegt. Block und Log tragen das schon | keine Änderung; liegt eine Quelle vor, Wert und Band nachziehen | B | `python3 -c "import sys; s=open('docs/methodik/95_hitzebelastung.md',encoding='utf-8').read(); b=s.split('id: heat.s_gek_kalib',1)[1].split('parameter:',1)[0]; sys.exit(not ('wert: 0.06' in b and 'band: [0.04, 0.09]' in b and 'kennzeichnung: abschaetzung_kap3' in b))"` | behoben (T-1643-methodik_manager): entschieden, Bericht unverändert; der Ausdruck belegt Wert, Band und Kennzeichnung |
| 185 | docs/methodik/95_hitzebelastung.md Block `heat.s_gek` Z. 1745–1748, Log 45 Z. 2342 | Voreinstellung, entschieden (LF 7) | Entscheidung des methodik_manager (T-1642-cmo, Leitlinie D): Die Voreinstellung s_gek = 0,11 bleibt (Quelle [71], Band [0,05; 0,15]). 0,145 aus [72] ist der Anteil der Neubauten und überzeichnet den Bestand (Log 45) | keine Änderung | B | `python3 -c "import sys; s=open('docs/methodik/95_hitzebelastung.md',encoding='utf-8').read(); b=s.split('id: heat.s_gek\n',1)[1].split('parameter:',1)[0]; sys.exit(not ('wert: 0.11' in b and 'band: [0.05, 0.15]' in b and 'quelle: carevor9_2026_destatis2026' in b))"` | behoben (T-1643-methodik_manager): entschieden, Bericht unverändert; der Ausdruck belegt Wert, Band und Quelle |
| 186 | docs/methodik/95_hitzebelastung.md §3.4 Z. 678–682 | Mittelwert eines Bands, entschieden (LF 7) | Entscheidung des methodik_manager (T-1642-cmo, Leitlinie D): r_0 bleibt die geometrische Mitte 3,54 je 100.000, weil das Band als Faktor gelesen wird (§3.4 Z. 678) | keine Änderung | B | `grep -qF '√(2,89 × 4,34) = 3,54, weil das Band als Faktor' docs/methodik/95_hitzebelastung.md` | behoben (T-1643-methodik_manager): entschieden, Bericht unverändert |
| 187 | docs/methodik/95_hitzebelastung.md Block `heat.f_alter` Z. 1479–1482; §5 Sensitivität von f_alter Z. 1361 | Sensitivität, entschieden (LF 7) | Entscheidung des methodik_manager (T-1642-cmo, Leitlinie D): f_a bleibt mit Band im Block und mit der Sensitivität in §5 (Z. 1361); kein neuer Wert | keine Änderung | B | `python3 -c "import sys; s=open('docs/methodik/95_hitzebelastung.md',encoding='utf-8').read(); b=s.split('id: heat.f_alter',1)[1].split('parameter:',1)[0]; sys.exit(not ('band: {u65: [0.156, 0.562]' in b and '**Sensitivität von f_alter**' in s))"` | behoben (T-1643-methodik_manager): entschieden, Bericht unverändert |
| 188 | docs/methodik/95_hitzebelastung.md §3.3 Z. 488 („§3.2: mit der Datei 342,58 Mio. € und 172.957 €“); backend/tests/test_methodik_95_golden_betraege.py Z. 22–24 (Docstring) | Golden-Betrag im Zelllauf gemessen (Anlass E) | Messbefehl E (Wortlaut unten), ausgeführt am 29.09.2026 auf dem Branch dieses Tickets, Ausgabe wörtlich: `342581893 172957` (stderr leer, Exit 0). testlauf-Aufruf nach docs/BETRIEB.md Z. 162 mit der Datei als Argument, Schlusszeile wörtlich: `4 passed, 1 warning in 1.46s` (Exit 0). Der Zelllauf des Produkts ergibt für Berlin 342,58 Mio. €, der Bericht nennt 342,67 Mio. € (§3.3). Die 0,03 % kommen aus der Stellenzahl der Tabelle §3.2: Das Produkt liest die Wochenquantile mit vier Nachkommastellen, die Tabelle des Berichts hat zwei (Docstring des Tests Z. 23–24). Der Importfehler aus Runde 38 trat nicht auf | keine Änderung am Bericht; der Wert 342,58 Mio. € steht in §3.3 schon | B | `grep -qF 'mit der Datei 342,58 Mio. € und 172.957 €' docs/methodik/95_hitzebelastung.md` | behoben (T-1643-methodik_manager): gemessen, die Messung gelang; eine Runde am Bericht wird daraus nicht |
| 189 | reviews/BEFUNDE_95.md Z. 1046 und Z. 1164 (Befund 150, beide in Runde 31) | Ledger-Zeile doppelt | Befund 150 steht zweimal: Z. 1046 „zurückgestellt (Termin: T-1534-cmo, Paket 3)“, Z. 1164 „behoben (T-1538)“. Maßgeblich ist nach ledger.py das letzte Vorkommen; an Z. 1046 sieht ein Leser das nicht | Vermerk an Z. 1046 „ersetzt durch die Zeile in Runde 31 (Befund 150, T-1538)“; zusammengeführt wird nichts | C | `python3 -c "import sys; z=[l for l in open('reviews/BEFUNDE_95.md',encoding='utf-8') if l.startswith('\| 150 \| §5 Hebel Hitzeaktionsplan,')]; sys.exit(not (len(z)==1 and 'ersetzt durch die Zeile in Runde 31 (Befund 150, T-1538)' in z[0]))"` | behoben (T-1643-methodik_manager): Vermerk gesetzt, Z. 1164 unverändert |
| 190 | docs/methodik/95_hitzebelastung.md Kopf Z. 10–14 (Revisionsstand) | Kopfzeile überholt (LF 11) | Die Kopfzeile nennt die Kühlzentren und s_gek_kalib nicht, und „im Produkt stehen … noch aus“ ist seit dem Code-Nachzug T-1582-ceo überholt | Kühlzentren und s_gek_kalib ergänzen und den Produktstand nach T-1582-ceo nennen | C | `python3 -c "import sys; s=open('docs/methodik/95_hitzebelastung.md',encoding='utf-8').read().split('## 1 ',1)[0]; k=s.split('Rev. 8 vom',1)[1]; sys.exit(not ('Kühlzentren' in k and 'heat.s_gek_kalib' in k and 'T-1582-ceo' in k and 'noch aus' not in k))"` | behoben (T-1643-methodik_manager): Kopf Z. 10–15 neu gefasst: Ledger-Runden 10–38, Kühlzentren, Block `heat.s_gek_kalib`, Produktstand nach T-1582-ceo, aus steht noch die Ersatzregel (Befund 116) |
| 191 | reviews/BEFUNDE_95.md, Zählung nach A-0046 (Runde 38: „die Grenze Runde 40“) | Rundenzählung, entschieden (CMO) | Entscheidung des CMO (T-1642-cmo, „Weiteres“): Die Rundennummern laufen im Ledger weiter; die Grenze nach A-0046 zählt ab der Null-Runde 38 und liegt bei Runde 48 | Zählung in diesem Abschnitt so führen | C | `python3 -c "import sys; s=open('reviews/BEFUNDE_95.md',encoding='utf-8').read().split('## Runde 39 ',1)[1]; sys.exit(not ('ab der Null-Runde 38' in s and 'bei Runde 48' in s))"` | behoben (T-1643-methodik_manager): Zählung unten fortgeschrieben |
| 192 | .claude/skills/methodik_manager-gegenpruefung/SKILL.md | Skill nennt LF 15 (Nachtrag zu Runde 38) | Runde 38 hat LF 15 von Hand geprüft, weil der Skill 14 Leitfragen nannte. Der Skill nennt LF 15 inzwischen: `grep -c "LF 15\|15 Leitfragen" .claude/skills/methodik_manager-gegenpruefung/SKILL.md` gab am 29.09.2026 `3` aus (auch in diesem Lauf nachgemessen: `3`) | Die Prüfung von Hand entfällt | C | `grep -qE 'LF 15\|15 Leitfragen' .claude/skills/methodik_manager-gegenpruefung/SKILL.md` | behoben (T-1643-methodik_manager): erledigt, gemessen, keine Änderung nötig |
| 193 | docs/methodik/95_hitzebelastung.md §5 S157 Z. 1148 („Im Zelllauf mit Gemeindeschlüssel 1,1 Mio. €; Warmsen (Zelllauf) 469 € je Jahr.“) | Zelllauf-Werte S157 gemessen (Anlass E) | Messbefehl S157 (Wortlaut unten), ausgeführt am 29.09.2026 auf dem Branch dieses Tickets, Ausgabe wörtlich: `1087324.95 468.55` (stderr leer, Exit 0). Das sind 1,09 Mio. € für Berlin und 468,55 € für Warmsen; der Bericht nennt gerundet 1,1 Mio. € und 469 €, beides stimmt | keine Änderung | B | `grep -qF 'Im Zelllauf mit Gemeindeschlüssel 1,1 Mio. €; Warmsen (Zelllauf) 469 € je Jahr.' docs/methodik/95_hitzebelastung.md` | behoben (T-1643-methodik_manager): gemessen, Bericht und Produkt stimmen überein |

**Messungen** (29.09.2026, Branch `ticket/T-1643-methodik_manager`, aus dem Wurzelverzeichnis des Repos).

Messbefehl E:

```
python3 -c "import subprocess,sys,os; py=os.path.expanduser('~/.venvs/kap2/bin/python'); env=dict(os.environ, PYTHONPATH='backend:backend/tests'); code='import test_methodik_95_golden_betraege as t; print(round(t._jahresbetrag(t.BERLIN)), round(t._jahresbetrag(t.WARMSEN)))'; p=subprocess.run([py,'-c',code],capture_output=True,text=True,env=env); print(p.stdout.strip(), p.stderr[-1500:]); sys.exit(p.returncode)"
```

Ausgabe wörtlich (stderr leer, Exit 0):

```
342581893 172957
```

testlauf-Aufruf nach docs/BETRIEB.md Z. 162:

```
python3 -c "import subprocess,sys; p=subprocess.run(['bash','scripts/testlauf.sh','-q','backend/tests/test_methodik_95_golden_betraege.py'],capture_output=True,text=True); print(p.stdout[-1500:], p.stderr[-800:]); sys.exit(p.returncode)"
```

Ausgabe wörtlich (Exit 0):

```
....                                                                     [100%]
=============================== warnings summary ===============================
../../../home/ovl/.venvs/kap2/lib/python3.12/site-packages/pydantic/_internal/_config.py:295
  /home/ovl/.venvs/kap2/lib/python3.12/site-packages/pydantic/_internal/_config.py:295: PydanticDeprecatedSince20: Support for class-based `config` is deprecated, use ConfigDict instead. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.10/migration/
    warnings.warn(DEPRECATION_MESSAGE, DeprecationWarning)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
4 passed, 1 warning in 1.46s
```

Messbefehl S157:

```
python3 -c "import subprocess,sys,os; py=os.path.expanduser('~/.venvs/kap2/bin/python'); env=dict(os.environ, PYTHONPATH='backend:backend/tests'); code='import test_methodik_95_golden_massnahmen as m; print(round(m._s157_eur(m.BERLIN),2), round(m._s157_eur(m.WARMSEN),2))'; p=subprocess.run([py,'-c',code],capture_output=True,text=True,env=env); print(p.stdout.strip(), p.stderr[-1500:]); sys.exit(p.returncode)"
```

Ausgabe wörtlich (stderr leer, Exit 0):

```
1087324.95 468.55
```

**Zählung nach A-0046.** Die Rundennummern laufen im Ledger weiter (Befund 191). Die Grenze nach A-0046 zählt ab der
Null-Runde 38 und liegt bei Runde 48; der Satz „die Grenze Runde 40“ in Runde 38 zählte noch ab der Null-Runde 30.
Runde 39 ist die erste Runde nach der Null-Runde 38.
