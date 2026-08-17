# KAP2 — Produkt-Roadmap „Vertrauen vor Umfang"

*Stand: 5. August 2026 · Internes Dokument · Ergänzt [PRODUKTBESCHREIBUNG.md](PRODUKTBESCHREIBUNG.md), [BUSINESSPLAN.md](BUSINESSPLAN.md), [WETTBEWERBSANALYSE.md](WETTBEWERBSANALYSE.md), [MODELL_KRITIK.md](MODELL_KRITIK.md)*

---

## 1. Executive Summary

**Kernaussage:** Die technische Basis von KAP2 (Datenbezug, 100-m-Engine, Lineage, Exporte) ist tragfähig — die Methodik hinter den einzelnen Risiken und Maßnahmen ist es noch nicht durchgängig. Statt mit 51 halb-validierten Risiken aufzutreten, wird das Produkt radikal verschlankt und **risikoweise validiert wieder aufgebaut**: Start mit einem offenen, kostenlosen MVP (Risikofeld **Hitze komplett**, 3 Risiken / 3 Maßnahmen), dann schnelle Release-Batches entlang der Kommunen-Pain-Points. Jede Stufe schaltet ein härteres Zugangs-Gate: ab Stage 2 geprüfte Anmeldung + Feedback-Pflicht, ab Stage 3 (35 Risiken) Kommerzialisierung. Endausbau: **45 Risiken / 47 Maßnahmen** (nach Katalog-Bereinigung), erreicht ca. **Mitte Februar 2027**.

**Stufen im Überblick** (Velocity-Annahme: 5 Risiken inkl. Maßnahmen/Woche; alle Termine inkl. 20 % Puffer):

| Stufe | Risiken | Maßnahmen | Zugang / Gate | Fertig (ca.) |
|---|---|---|---|---|
| **M0 — MVP** | 3 (Hitze komplett) | 3 | offen & kostenlos, einfacher Feedback-Kanal; Demo offline | **28.08.2026 (fix)** |
| **M1 — Stage 1** | 16 | 17 | weiterhin offen; Rapid-Release-Batches | ~02.10.2026 |
| **M2 — Stage 2** | 25 | ~25 | **nur geprüfte Anmeldung (KAP3-Freigabe) + Feedback-Pflicht**; Demo wieder online | ~06.11.2026 |
| **M3 — Stage 3** | 35 | ~34 | **Kommerzialisierung** (0,10 €/EW p. a.); Version-Gating für Bestandsnutzer | ~25.12.2026 |
| **M3½ — Studie** *(nur intern)* | — | — | Deutschland-Studie zur öffentlichen Aufmerksamkeit | ~15.01.2027 |
| **M4 — Stage 4** | 45 (Vollausbau) | 47 | Katalog-Bereinigung abgeschlossen | ~12.02.2027 |

**Priorisierung ist trend-validiert:** Hitze ist 2026 Kommunen-Pain #1 (Rekord-Hitzewelle Juni 2026, ~5.100 Hitzetote bis Ende Juni), Hochwasser/Starkregen stellen ~50 % der deutschen Klimaschäden, Sturm/Hagel ~22 %; die Fördernachfrage der Kommunen übersteigt die Bundesmittel um mehr als das Zehnfache (Details und Quellen in Abschnitt 3). Daher die Reihenfolge: **Hitze → Hochwasser → Sturm → Trockenheit → Gradueller Wandel/Verbund.**

**Drei Grundregeln über alle Stufen:**
1. **Kein Risiko ohne mindestens eine verknüpfte Maßnahme** (heute haben 22 von 51 Risiken keine — das wird nicht wiederholt).
2. **Jedes Risiko-Release = validierte Methodik**: geprüfte Parameter, zitierfähige Quellen, dokumentierte Wirkungskette.
3. **Kein Downgrade-Schlupfloch**: Bestandsnutzer behalten alte Analysestände einsehbar, aber ohne Upgrade keine Neuberechnung und keine neuen Risiken; man kann nicht in eine kleinere Version wechseln, um im Free-Tier zu bleiben.

---

## 2. Ausgangslage

- Der Katalog enthält heute **51 Risiken** (nicht 47, wie bisher kommuniziert), 47 Maßnahmen, 23 Klimagefahren, 24 Expositionen, 33 Vulnerabilitätsindikatoren und 70 Auxiliary-Layer (`backend/app/data/catalog.py`, `MODEL_VERSION 2026.08-mortalitaet-erf`).
- **22 der 51 Risiken haben keine einzige verknüpfte Maßnahme** — für Nutzer wirkt das unfertig und widerspricht dem Kernversprechen „Maßnahmen mit Kosten-Nutzen je Risiko".
- Die [MODELL_KRITIK.md](MODELL_KRITIK.md) stuft den Risiko-Index als belastbares Screening ein, sieht aber bei den monetären Absolutwerten je nach Risiko unterschiedliche Reifegrade. Genau diese Ungleichmäßigkeit ist der Grund für den Neustart in Stufen: lieber wenige Risiken, die einer Prüfung durch Fachöffentlichkeit standhalten, als viele, die Vertrauen kosten.
- Ein Versionierungskonzept für Analysestände existiert nicht (Ergebnisse werden destruktiv überschrieben). Für das Free-Tier-Gating ab Stage 3 ist das eine Neuentwicklung (Abschnitt 7).

## 3. Priorisierung: Abgleich mit Nachrichtenlage und Kommunen-Pain

Die Stage-0/1-Auswahl wurde gegen die aktuelle Nachrichten- und Studienlage geprüft (Websuche, Stand August 2026):

- **Hitze ist das dominierende Thema 2026:** Der DWD warnte so früh wie nie über einen langen Zeitraum vor Hitze; die Juni-Hitzewelle 2026 brachte regionale Rekorde bis über 40 °C, bis Ende Juni starben in Deutschland rund **5.100 Menschen** an Hitzefolgen. Das MVP „Hitze komplett" trifft den Nerv exakt.
- **Hochwasser & Starkregen sind der größte Schadensposten:** ~die Hälfte der seit 1980 verfünffachten Klimaschäden entfällt auf Hochwasser-/Starkregenereignisse; nur gut die Hälfte der ~20 Mio. Wohngebäude ist dagegen versichert. → Stage-1-Batch 1 (direkt nach dem MVP).
- **Sturm/Hagel** stellen ~22 % der Schäden → Stage-1-Batch 2.
- **Hitze + Dürre** zusammen ~29 % (Landwirtschaft, Forst, Niedrigwasser) → Stage-1-Batch 3.
- **Kommunale Zahlungsbereitschaft/Pain ist belegt:** Für die 5. Tranche der Bundesförderung klimaangepasster Städte wurden 326 Projektanträge mit 928 Mio. € Volumen eingereicht — bei nur 80 Mio. € verfügbaren Bundesmitteln.
- Biodiversitäts-/Habitatverlust und psychische Folgen/Standortnachteile sind mediale Nebenthemen, komplettieren aber die fünf KWRA-Risikofelder — wichtig für den Konformitätsanspruch, daher bewusst am Ende von Stage 1 statt später.

Quellen: [DWD-Pressemitteilung 25.06.2026](https://www.dwd.de/DE/presse/pressemitteilungen/DE/2026/20260625_dwd-warnt-ueber-langen-zeitraum-vor-hitze_news.html) · [Mitwelt: Hitzesommer 2026](https://www.mitwelt.org/hitze-hitzesommer-klima-wetter-klimawandel-oberrhein-baden-freiburg) · [KfW Research Fokus Nr. 542 (April 2026)](https://www.kfw.de/PDF/Download-Center/Konzernthemen/Research/PDF-Dokumente-Fokus-Volkswirtschaft/Fokus-2026/Fokus-Nr.-542-April-2026-Klimabetroffenheit.pdf) · [ZDFheute: Naturkatastrophen-Bilanz 2025](https://www.zdfheute.de/panorama/naturkatastrophen-deutschland-klimawandel-schaden-100.html) · [BMWSB-Pressemitteilung Juli 2026](https://www.bmwsb.bund.de/SharedDocs/pressemitteilungen/DE/2026/07/klimaangepasste-staedte-gemeinden.html) · [ISOE-Studie Klimaanpassung (Sept. 2025)](https://www.deutschesklimaportal.de/SharedDocs/Kurzmeldungen/DE/Andere/2025/ISOE_Studie_Klimaanpassung_20250916.html)

## 4. Zielbild: Katalog-Bereinigung auf 45 Risiken / 47 Maßnahmen

Orientierung ist durchgängig die KWRA-Systematik (fünf Risikofelder, Wirkungsketten H×E×V). Die Bereinigung erfolgt schrittweise bis Stage 4; alle Fusionen sind Empfehlungen und werden je Batch methodisch geprüft.

**Risiko-Arithmetik: 51 Bestand + 2 neu − 8 Fusionen = 45**

Neue Risiken (Modellierungsaufwand eingeplant):

| Neu | Begründung |
|---|---|
| **Hitzeschäden an Technik & Infrastruktur (€)** | Bisher fehlt ein Hitze-Sachschadensrisiko komplett. Beispiel Leipzig 2026: Tram-Ausfall durch hitzebedingte Gleisschäden. Erfasst Schäden an Gleisen, Straßen, Technik, Anlagen. |
| **Sturmschäden (€)** | Gebäude-/Sachschäden sind heute ein Sammelrisiko unter „Hochwasser & Starkregen". Split in Flut- und Sturm-Anteil für saubere Attribution je Risikofeld. |

Fusionen (KWRA-orientiert, gegen Doppelzählung und Index-Wildwuchs):

| Fusion | Ergebnis |
|---|---|
| Schäden Aquakultur → Wirtschaftliche Verluste Fischerei | ein Fischerei-Schadensrisiko (€) |
| Bodenverluste/-degradation (€) + Bodenverschlechterung (ha) | ein Boden-Risiko |
| Ökosystemdegradation + Ökosystemfragmentierung + Umwelt-Rückkopplungen (3 Indizes) | ein Ökosystem-Index |
| Fischereiliche Bestandsbelastung + Niedrigwasser-Fischerei-Index | ein Fischerei-Index |
| Verzögerte Schadenswirkungen + Kosten Versorgungsengpässe | endgültig in „Indirekte wirtschaftliche Verluste" (sind dort heute schon konsolidiert) |
| Administrative Ausfallzeiten + Dauer von Funktionsausfällen | ein Risiko „Funktionsausfälle Verwaltung/Dienste" |

*Hinweis:* „Wirtschaftliche Standortnachteile" ist heute ebenfalls in „Indirekte Verluste" konsolidiert, soll aber (Stage 1) eigenständig erscheinen — beim Hinzukommen der Indirekten Verluste in Stage 3 wird die Doppelzählungsregel neu gezogen.

**Maßnahmen-Arithmetik: 47 Bestand + 2 neu − 2 Fusionen = 47**

Neue Maßnahmen (Stage 1, damit kein Risiko ohne Maßnahme bleibt): **Psychosoziale Versorgung & Nachsorge nach Extremereignissen** (→ Psychische Belastungsfälle) und **Klimaresiliente Standortentwicklung/Wirtschaftsförderung** (→ Standortnachteile). Fusionen: „Entsiegelung/Schwammstadt" in „Entsiegelung", „Retentionsflächen/Speicher" in „Retention/Polder/Rückhaltebecken" (jeweils nahezu deckungsgleich).

## 5. Meilensteine

**Release-Kriterium für jede Stufe: kein freigeschaltetes Risiko ohne mindestens eine verknüpfte Maßnahme; jedes Risiko-Release mit validierten Parametern, zitierfähigen Quellen und dokumentierter Wirkungskette.**

### M0 — Verschlankung & MVP „Hitze komplett" (3 R / 3 M) — fix bis 28.08.2026

- **Scoping zuerst (3–4 Tage):** endgültige Festlegung, welche Risiken und Maßnahmen ins MVP und in die Stage-1-Batches gehen und in welcher Reihenfolge sie implementiert werden. Die Auswahl ist **noch nicht final** — die folgenden Listen sind der begründete Vorschlag als Scoping-Grundlage. Der Scoping-Block liegt innerhalb des M0-Fensters; der Puffer für M0 ist entsprechend reduziert (ambitioniertes Ziel).
- **Risiken (Vorschlag):** Erwartete Mortalität (Hitze) · Erwartete Morbidität (Hitze) · **NEU: Hitzeschäden an Technik & Infrastruktur (€)**. Damit ist das Risikofeld Hitze vollständig abgedeckt.
- **Maßnahmen (Vorschlag):** Hitzeaktionspläne (`HEAT_ACTION_PLANS`) · Schutzprogramme vulnerable Gruppen (`VULNERABLE_GROUP_PROGRAMS`) · Hitzeresiliente Beläge (`HEAT_RESILIENT_PAVEMENT`, adressiert das neue Hitze-Infra-Risiko).
- **Verschlankung:** Landing auf ein Minimum reduziert (Scrollytelling-Widgets ausdünnen), Produkt-Shell minimal, Auxiliary-/H/E/V-Layer nur soweit die drei aktiven Wirkungsketten sie benötigen. **Demo offline** (kehrt in Stage 2 zurück).
- **Release:** offen und kostenlos, einfacher Feedback-Kanal (niedrigschwellig, z. B. Formular je Ansicht).

### M1 — Stage 1: Rapid Releases auf 16 R / 17 M — bis ~02.10.2026

Vier Batches in Prioritätsreihenfolge (jeder Batch einzeln releast):

| Batch | Risiken (+13 → 16) | Maßnahmen (+14 → 17) |
|---|---|---|
| **1.1 Hochwasser** | Flut-Mortalität · Flut-Verletzte · Gebäudeschäden Flut (**NEU: Split Flut/Sturm**) | Frühwarnsysteme · Deichverstärkung · Entsiegelung |
| **1.2 Sturm** | Sturm-Mortalität · Sturm-Verletzte · **NEU: Sturmschäden (€)** | Risikobasierte Investitionen (vorgezogen, → Sturmschäden) |
| **1.3 Trockenheit** | Landwirtschaftliche Schäden · Forstschäden (Vegetationsschäden) · Fischerei-Verluste (inkl. Aquakultur-Fusion) | Trockenresistente Sorten · Humusaufbau · Mischwälder · Adaptive Fischereibewirtschaftung · Aquakultur-Resilienz |
| **1.4 Graduell + Verbund** | Biodiversitätsverlust · Habitatverlust · Psychische Belastungsfälle · Wirtschaftliche Standortnachteile | Biotopverbund · **NEU: Psychosoziale Versorgung/Nachsorge** · **NEU: Klimaresiliente Standortentwicklung** |
| **Hitze-Ergänzung** | — | Dachgrün/Fassadengrün · Stadtgrün |

Damit sind alle fünf KWRA-Risikofelder vertreten (Konformitätsanspruch), und jedes Risiko hat mindestens eine Maßnahme.

### M2 — Stage 2: 25 R / ~25 M — Zugangs- und Feedback-Gate — bis ~06.11.2026

- **Zugang nur noch mit Anmeldung, die durch KAP3 geprüft und freigegeben wird.**
- **Feedback-Pflicht:** Freinutzung nur gegen strukturiertes Feedback (Gate im Produkt, z. B. Pflicht-Review nach N Analysen).
- **Demo wieder online** (`/demo`).
- **+9 Risiken** (Prio-1-lastig): Stunden thermischer Belastung · Betroffene/Evakuierte · Ausfallstunden Wasserversorgung · Hydrologische Belastung · Schäden Energieinfrastruktur · Schäden Wasser-/Abwasserinfrastruktur · Ausfallzeiten kritischer Infrastruktur · Ausfallstunden Energieversorgung · Systemische Dominoeffekte.
- **+8 Maßnahmen:** Kühle Räume/Trinkwasser · Evakuierungs- & Notfallpläne · Grundwasseranreicherung · Leckage-Reduktion · Retention/Polder/Rückhaltebecken · Netzverstärkung/Redundanzen · Hitzefeste Anlagen/Kühlung · Dezentrale Energie (PV, Speicher). Für „Schäden Wasser-/Abwasser" wird die Zuordnung von „Risikobasierte Investitionen" erweitert (Regel 1).

### M3 — Stage 3: 35 R / ~34 M — Kommerzialisierung — bis ~25.12.2026

- **+10 Risiken:** Medizinische Unterversorgung · Schäden Verkehrswege · Verkehrsunterbrechungen · Wiederherstellungskosten · Indirekte wirtschaftliche Verluste · Lieferkettenunterbrechungen · Bodenverluste/-degradation (fusioniert) · Gewässer-/Luftbelastung · Verstärkung sozialer Ungleichheiten · Schadstoffexpositionsstunden.
- **+9 Maßnahmen:** Schutz kritischer Knoten · Präventionsanreize · Lieferketten-Resilienz · Brandprävention · Erosionsschutz · Wasserspeicher/effiziente Bewässerung · Entwässerung (Mulden/Rigolen) · Kühlkonzepte Industrie/Gewerbe · Gewässerschutz für Fischerei.
- **Kommerzialisierung** gemäß [BUSINESSPLAN.md](BUSINESSPLAN.md) (0,10 €/EW p. a., Mindestpreis): Voraussetzungen sind Benutzerverwaltung/Mandantentrennung, Abrechnung und PDF-Ergebnisbericht.
- **Version-Gating:** Bestandsnutzer behalten ihre alten Analysestände (einsehbar), können aber ohne Upgrade **nicht neu rechnen** und erhalten keine neuen Risiken. Ein Wechsel auf ältere/kleinere Versionen, um im Free-Tier zu bleiben, ist ausgeschlossen. Technische Basis: neues Snapshot-Konzept (Abschnitt 7).

### M3½ — Studien-Release *(interne Stufenbezeichnung, wird nicht offiziell gezeigt)* — bis ~15.01.2027

- Deutschland-weite Studie über alle Kommunen zur öffentlichen Aufmerksamkeit (Kanal `/studie` existiert).
- Aufwand **≈ 1 Monat**. **Interner Vermerk:** Die Rechenläufe müssen **parallel zur Stage-3-Entwicklung auf Basis der Stage-2-Ergebnisse (25 Risiken)** erfolgen — sonst ist der Zeitplan nicht haltbar. Nach M3 verbleiben nur Auswertung, Aufbereitung und Redaktion (~2 Wochen).

### M4 — Stage 4: Vollausbau 45 R / 47 M — bis ~12.02.2027

- **+10 Risiken** (Rest inkl. Fusionen): Schäden Telekommunikation · Ausfallzeiten Kommunikation · Ausfallstunden Abwasserentsorgung · Verlust von Ökosystemleistungen · Ökosystem-Index (fusioniert aus 3) · Fischerei-Bestands-Index (fusioniert aus 2) · Ressourcenkonflikte · Kosten klimabedingter Migration · Hangrutsch-Verletzte · Funktionsausfälle Verwaltung/Dienste (fusioniert).
- **+13 Maßnahmen** (Rest): Hochwasserschutz Gebäude · Helle Dächer · Frischluftschneisen · Schatten/Wasser im öffentlichen Raum · Trinkbrunnen · Bauverbote in Risikozonen · Auenrenaturierung · Versickerungsflächen · Abflusslenkung (DGM) · Salzwasserbarrieren · Fischaufstieg · Laichhabitat-Renaturierung · Arbeitszeitmodelle bei Hitze.
- Damit ist die heutige Lücke „22 Risiken ohne Maßnahme" vollständig geschlossen.

## 6. Timeline und Annahmen

**Annahmen:** Start 05.08.2026 · Velocity **5 Risiken inkl. zugehöriger Maßnahmen pro Woche** · Zusatzaufwände (Verschlankung, Gates, Kommerzialisierung, Studie) als Schätzung · auf alles **+20 % Puffer** · sequenzielle Abarbeitung (Ausnahme: Studien-Rechenläufe parallel zu Stage 3).

| Meilenstein | Risiko-Arbeit | Zusatzaufwand | inkl. 20 % Puffer | Fertig (ca.) |
|---|---|---|---|---|
| M0 MVP | 3 R → 0,6 Wo | Scoping 3–4 Tage + Verschlankung/Release-Setup ≈ 2 Wo | ≈ 3,5 Wo (gedeckelt) | **28.08.2026 (fix)** |
| M1 Stage 1 | +13 R → 2,6 Wo | Neumodellierung (Hitze-Infra €, Flut/Sturm-Split, 2 neue Maßnahmen) ≈ 1 Wo | ≈ 4,5 Wo | **~02.10.2026** |
| M2 Stage 2 | +9 R → 1,8 Wo | Anmelde-/Prüf-Gate (KAP3), Feedback-Gate, Demo ≈ 2 Wo | ≈ 4,5 Wo | **~06.11.2026** |
| M3 Stage 3 | +10 R → 2 Wo | Auth/Multi-Tenancy, Version-Gating/Snapshots, Billing, PDF-Bericht ≈ 4 Wo | ≈ 7 Wo | **~25.12.2026** |
| M3½ Studie | — | ≈ 4 Wo gesamt, davon ~2 Wo Rechenläufe parallel zu Stage 3 (auf Stage-2-Basis) | ≈ 2,5 Wo sequenziell | **~15.01.2027** |
| M4 Stage 4 | +10 R → 2 Wo | Fusionen/Migration Altdaten ≈ 1 Wo | ≈ 3,5 Wo | **~12.02.2027** |

Gesamt ≈ 25 Wochen. **Hinweise:** (a) Alle Termine sind Grobschätzungen auf Basis der Velocity-Annahme; der Puffer ist bereits enthalten. (b) M0 ist auf den 28.08.2026 fixiert — das Scoping liegt innerhalb dieses Fensters, der M0-Puffer ist dadurch reduziert. (c) Die Risiko-/Maßnahmenzuordnung für M0/M1 wird im Scoping final festgezurrt.

## 7. Querschnitts-Workstreams

- **Methodik-Validierung je Batch:** Review der Parameter, Quellen und Wirkungsketten vor jedem Release (Ratchet-Tests fortführen); Ergebnis dokumentiert im Berechnungshandbuch.
- **Feedback-Infrastruktur:** M0 einfacher Kanal → M2 strukturiertes Pflicht-Feedback als Nutzungsbedingung; Auswertung fließt in die Batch-Priorisierung ein.
- **Versionierung & Free-Tier-Gating (Neuentwicklung):** Analyse-Snapshots je Kommune und Modellstand (heute: destruktives Überschreiben; vorhandene Bausteine: `MODEL_VERSION`, `recalc_recommended`, Lite-`batch_id`). Alte Stände bleiben lesbar, Neuberechnung nur mit aktueller Lizenzstufe; kein Downgrade in kleinere Versionen.
- **Anmelde-Prüfung (ab Stage 2):** Registrierung mit Freigabe-Workflow durch KAP3.
- **Verschlankung & Re-Expansion:** Landing/Produkt/Layer wachsen mit den Stufen kontrolliert wieder mit — nur was aktive Risiken benötigen, wird angezeigt.
- **Kommerzialisierungs-Voraussetzungen (bis M3):** Benutzerverwaltung/Mandantentrennung, Abrechnung, PDF-Ergebnisbericht (siehe [BUSINESSPLAN.md](BUSINESSPLAN.md)).

## 8. Offene Punkte

1. **M0-Scoping** (3–4 Tage) bestätigt oder korrigiert die hier vorgeschlagene Risiko-/Maßnahmenauswahl und die Batch-Reihenfolge.
2. Modellierungskonzept für die zwei neuen Risiken (Hitze-Infra €, Sturmschäden-Split) und die zwei neuen Maßnahmen — inkl. Quellenlage.
3. Ausgestaltung der KAP3-Anmeldeprüfung (Kriterien, SLA der Freigabe).
4. Feedback-Pflicht: Form (Fragebogen, Interview, Datenfreigabe?) und Schwelle, ab der die Nutzung gesperrt wird.
5. Zuschnitt der Studie (M3½): Fragestellung, Kommunen-Auswahl, Reviewer.
