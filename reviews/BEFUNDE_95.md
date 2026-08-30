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

| Nr | Stelle | Art | Begründung | Vorschlag | Kat. | Status |
|---|---|---|---|---|---|---|
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

| Nr | Stelle | Art | Begründung | Vorschlag | Kat. | Status |
|---|---|---|---|---|---|---|
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

| Nr | Stelle | Art | Begründung | Vorschlag | Kat. | Status |
|---|---|---|---|---|---|---|
| 75 | §4 Befund-1-Korrektur, Begründungsketten der gekennzeichneten Abschätzungen (a)/(b) | Lücke (§3.8 „jede Zahl mit Quelle"; §2.7 „ohne Rückfragen prüfbar") | Zwei Elemente des seit Runde 2 neuen Textes sind nicht im Bericht verankert: (a) „DE-Bevölkerung lebt zu ≈ 77 % städtisch" ohne Quellenangabe; (b) die σ_UHI-Begründung beruft sich auf „die Feinstruktur-Spanne des §3.1-Beispiels (±1 K)" — §3.1 dieses Berichts enthält kein Beispiel (bei der Migration nicht übernommen; toter Binnenverweis, vgl. Befund-60-Muster). Ergebnisrelevanz gering: beide Größen sind als §3.9-Abschätzungen gekennzeichnet, das Band 0,70–0,79 ist die ausgewiesene Ergebnis-Sensitivität, der σ-Beitrag (×1,03) ist zweiter Ordnung | (a) Quelle ergänzen (Destatis-/Weltbank-Urbanisierungsgrad ≈ 77–78 %, Kap.-8-Eintrag); (b) Spanne direkt beziffern (Stadtmodell-Kennwert) oder das ±1-K-Beispiel aus M0 Rev. 5 in §3.1 übernehmen | C | **übernommen** | §3.1: Mittelwerttreue-Beispiel (±1-K-Spanne) aus M0 wiederhergestellt — Verweis trägt; 77-%-Zahl mit Weltbank-Indikator bequellt | — |
| 76 | Produktcode (Registry/Engine `EXPECTED_ANNUAL_MORTALITY`) ↔ Bericht Rev. 6 — sichtbar geworden in der Wirkungsmechanismus-Vorschau (30.08.2026) | Divergenz Bericht ↔ Code (Eiserne Regel 5; LF 14) | Das Produkt rechnet noch den Vor-Rev.-6-Stand: native Größe **Todesfälle/Jahr** statt YLL (Log 3/P52), Kostensatz-Pfad ohne YLL × VOLY, f_a 0,404/0,577/0,62 (Rev.-5, ersetzt durch 0,357/0,588/0,631 — Befund 32), Basissterberaten 180/1.800/4.600/15.500 statt 213,2/1.737,9/4.812,3/14.800,2, Gauß-σ 2,0 K statt empirischer Wochenquantile (Log 5), Kalibrierfaktor 1,44 statt 0,742 (Log 26/30) | **Kein stiller Code-Fix.** Auflösung ist exakt der Umfang von `/integriere-risiko 95` (Registry-Parameter aus §7, Schicht-B-Funktion, Golden-Tests); bei Integration diesen Befund mit Umsetzungsnachweis schließen und die Wirkungsmechanismus-Vorschau #95 gegen den Bericht abgleichen | A (blockiert nicht den Bericht, sondern markiert den offenen Integrationsschritt) | **offen — wird durch /integriere-risiko 95 geschlossen** |

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
