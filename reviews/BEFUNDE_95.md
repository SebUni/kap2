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
| 111 | Kapitel 7, alle 19 Blöcke | Formverstoß (Aufgabe §4, Felder `kennzeichnung`, `abgeleitet_aus`, `rolle`) | Feld `kennzeichnung` fehlte in allen Blöcken | Feld je Block; `abgeleitet_aus` bei `berechnet`; `rolle` für c_kal und Distanzterm | B | `python3 -c "import re,sys; s=open('docs/methodik/95_hitzebelastung.md',encoding='utf-8').read(); b=s[s.index('## 7 '):s.index('## 8 ')].split('parameter:')[1:]; sys.exit(not (len(b) == 22 and all(re.search(r'^ *kennzeichnung: (\S+)', x, re.M).group(1) in ('quelle', 'abschaetzung_kap3', 'berechnet') for x in b) and all(re.search(r'^ *abgeleitet_aus: .heat', x, re.M) for x in b if 'kennzeichnung: berechnet' in x)))"` | behoben (T-1119): 10 × quelle, 6 × abschaetzung_kap3, 3 × berechnet (c_kal, beta_iso, beta_pfl); rolle kalibrierung (c_kal), sensitivitaet (Distanzterm); Lesart der Grenzfälle im Entscheidungslog Nr. 40; keine `wert:`-Zeile geändert; Prüfausdruck in Runde 24 (T-1295) von 19 auf 22 Blöcke fortgeschrieben, weil drei Maßnahmen-Blöcke dazukamen (Befunde 122 und 123) |

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
