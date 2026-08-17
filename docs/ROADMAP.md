# KAP2 — Produkt-Roadmap „Vertrauen vor Umfang, Reihenfolge nach Dringlichkeit"

*Stand: 8. August 2026 · Internes Dokument · Ersetzt die Fassung vom 5. August 2026 (archiviert unter [ablage/ROADMAP.md](ablage/ROADMAP.md)) · Ergänzt [PRODUKTBESCHREIBUNG.md](PRODUKTBESCHREIBUNG.md), [BUSINESSPLAN.md](BUSINESSPLAN.md), [WETTBEWERBSANALYSE.md](WETTBEWERBSANALYSE.md), [MODELL_KRITIK.md](MODELL_KRITIK.md), [KATALOG_KRITIK.md](KATALOG_KRITIK.md)*

---

## 1. Executive Summary

**Kernaussage:** Die technische Basis von KAP2 (Datenbezug, 100-m-Engine, Lineage, Exporte) ist tragfähig — die Methodik hinter den einzelnen Risiken und Maßnahmen ist es noch nicht durchgängig. Statt mit 51 halb-validierten Risiken aufzutreten, wird das Produkt radikal verschlankt und **risikoweise validiert wieder aufgebaut**. Neu gegenüber der Fassung vom 5. August: **Die Reihenfolge und der Zuschnitt der Risiken folgen jetzt strikt dem KWRA-2021-Handlungserfordernis** ([KWRA-2021_Klimawirkungen.xlsx](KWRA-2021_Klimawirkungen.xlsx), Spalte „Handlungserfordernis": 31 sehr dringend → 23 dringend). Jede Klimawirkung wird **1:1 als eigenes Risiko unter ihrem KWRA-Namen** geführt — bisherige Bündel-Risiken (z. B. „Landwirtschaftliche Schäden" für drei Klimawirkungen) werden gestrichen und durch die KWRA-Einzelrisiken ersetzt; Outcome-Größen (Mortalität, Erkrankungen, €) sind Ausweis-Dimensionen innerhalb eines Risikos, keine eigenen Risiken. Endausbau M0–M4: **52 Risiken = 31 „sehr dringend" + 23 „dringend" − 2 kommunal nicht relevante** (#33 marine Nahrungsnetze, #81 internationaler Warentransport — Begründung in §4), erreicht ca. **Mitte Februar 2027**; alles nicht (sehr) Dringende wandert in den neuen, bewusst unterminierten Meilenstein **M5 — Perspektive**.

**Stufen im Überblick** (Velocity-Annahme: 5 Risiken inkl. Maßnahmen/Woche; alle Termine inkl. 20 % Puffer):

| Stufe | Risiken | Maßnahmen | Zugang / Gate | Fertig (ca.) |
|---|---|---|---|---|
| **M0 — MVP** | 3 (Gesundheit: Hitzebelastung, Aeroallergene, UV) | 4 | offen & kostenlos, einfacher Feedback-Kanal; Demo offline | **28.08.2026 (fix)** |
| **M1 — Stage 1** | 18 (nur „sehr dringend") | ~18 | weiterhin offen; Rapid-Release-Batches | ~02.10.2026 |
| **M2 — Stage 2** | 31 (**alle 31 „sehr dringend" komplett**) | ~28 | **nur geprüfte Anmeldung (KAP3-Freigabe) + Feedback-Pflicht**; Demo wieder online | ~06.11.2026 |
| **M3 — Stage 3** | 42 („dringend": Infrastruktur/Wirtschaft/Gesundheit) | ~38 | **Kommerzialisierung** (0,10 €/EW p. a.); Version-Gating für Bestandsnutzer | ~25.12.2026 |
| **M3½ — Studie** *(nur intern)* | — | — | Deutschland-Studie zur öffentlichen Aufmerksamkeit | ~15.01.2027 |
| **M4 — Stage 4** | 52 (Vollausbau „sehr dringend" + „dringend") | ~50 (Ziel, s. §8) | Katalog-Umbau abgeschlossen | ~12.02.2027 |
| **M5 — Perspektive** | nicht (sehr) dringende Klimawirkungen + KAP2-Plus | — | — | **Termin offen** |

**Drei Grundregeln über alle Stufen:**
1. **Kein Risiko ohne mindestens eine verknüpfte Maßnahme** (heute haben 18 von 51 Risiken keine — das wird nicht wiederholt).
2. **Jedes Risiko-Release = validierte Methodik**: geprüfte Parameter, zitierfähige Quellen, dokumentierte Wirkungskette.
3. **Kein Downgrade-Schlupfloch**: Bestandsnutzer behalten alte Analysestände einsehbar, aber ohne Upgrade keine Neuberechnung und keine neuen Risiken; man kann nicht in eine kleinere Version wechseln, um im Free-Tier zu bleiben.

---

## 2. Ausgangslage

- Der Katalog enthält heute **51 Risiken** (nicht 47, wie bisher kommuniziert), 47 Maßnahmen, 23 Klimagefahren, 24 Expositionen, 33 Vulnerabilitätsindikatoren und 70 Auxiliary-Layer (`backend/app/data/catalog.py`, `MODEL_VERSION 2026.08-mortalitaet-erf`).
- **18 der 51 Risiken haben keine einzige verknüpfte Maßnahme** — für Nutzer wirkt das unfertig und widerspricht dem Kernversprechen „Maßnahmen mit Kosten-Nutzen je Risiko".
- **Neue Priorisierungsgrundlage:** [KWRA-2021_Klimawirkungen.xlsx](KWRA-2021_Klimawirkungen.xlsx) (102 Klimawirkungen; 31 „sehr dringend", 23 „dringend", 44 nicht ausgewiesen, 4 ohne Anpassungsoption). Das Mapping Klimawirkung ↔ KAP2-Risiko folgt [KATALOG_KRITIK.md](KATALOG_KRITIK.md) Anhang A — es wird kein neues Mapping erfunden.
- Die [MODELL_KRITIK.md](MODELL_KRITIK.md) stuft den Risiko-Index als belastbares Screening ein, sieht aber bei den monetären Absolutwerten je nach Risiko unterschiedliche Reifegrade. Genau diese Ungleichmäßigkeit ist der Grund für den Neustart in Stufen: lieber wenige Risiken, die einer Prüfung durch Fachöffentlichkeit standhalten, als viele, die Vertrauen kosten.
- Ein Versionierungskonzept für Analysestände existiert nicht (Ergebnisse werden destruktiv überschrieben). Für das Free-Tier-Gating ab Stage 3 ist das eine Neuentwicklung (Abschnitt 7).

## 3. Priorisierung: KWRA-Dringlichkeit zuerst, Nachrichtenlage als Gegenprobe

**Primäres Ordnungskriterium ist ab dieser Fassung das KWRA-Handlungserfordernis** (sehr dringend vor dringend); die Nachrichten- und Studienlage dient als Sekundärvalidierung — und bestätigt den Einstieg:

- **Hitze ist das dominierende Thema 2026:** Der DWD warnte so früh wie nie über einen langen Zeitraum vor Hitze; die Juni-Hitzewelle 2026 brachte regionale Rekorde bis über 40 °C, bis Ende Juni starben in Deutschland rund **5.100 Menschen** an Hitzefolgen. „Hitzebelastung" (#95) ist zugleich die einzige Klimawirkung, die die KWRA **schon in der Gegenwart** mit hohem Klimarisiko bewertet — MVP und KWRA zeigen auf dieselbe Stelle.
- **Hochwasser & Starkregen sind der größte Schadensposten:** ~die Hälfte der seit 1980 verfünffachten Klimaschäden entfällt auf Hochwasser-/Starkregenereignisse; nur gut die Hälfte der ~20 Mio. Wohngebäude ist dagegen versichert. KWRA-seitig: „Gebäudeschäden Flusshochwasser" (#60) und „Versagen von Hochwasserschutzsystemen" (#50) sind sehr dringend → Stage-1-Batch 1.2.
- **Kommunale Zahlungsbereitschaft/Pain ist belegt:** Für die 5. Tranche der Bundesförderung klimaangepasster Städte wurden 326 Projektanträge mit 928 Mio. € Volumen eingereicht — bei nur 80 Mio. € verfügbaren Bundesmitteln.
- Wo Nachrichtenlage und KWRA auseinanderfallen, gewinnt die KWRA: Sturm/Hagel (~22 % der Schäden) hat kein (sehr) dringendes urbanes KWRA-Pendant — der Sturm-Einstieg läuft daher über „Windwurf" (#29, dringend, M4); urbane Sturm-Personenschäden (#101, gering/mittel) liegen in M5.

Quellen: [DWD-Pressemitteilung 25.06.2026](https://www.dwd.de/DE/presse/pressemitteilungen/DE/2026/20260625_dwd-warnt-ueber-langen-zeitraum-vor-hitze_news.html) · [Mitwelt: Hitzesommer 2026](https://www.mitwelt.org/hitze-hitzesommer-klima-wetter-klimawandel-oberrhein-baden-freiburg) · [KfW Research Fokus Nr. 542 (April 2026)](https://www.kfw.de/PDF/Download-Center/Konzernthemen/Research/PDF-Dokumente-Fokus-Volkswirtschaft/Fokus-2026/Fokus-Nr.-542-April-2026-Klimabetroffenheit.pdf) · [ZDFheute: Naturkatastrophen-Bilanz 2025](https://www.zdfheute.de/panorama/naturkatastrophen-deutschland-klimawandel-schaden-100.html) · [BMWSB-Pressemitteilung Juli 2026](https://www.bmwsb.bund.de/SharedDocs/pressemitteilungen/DE/2026/07/klimaangepasste-staedte-gemeinden.html) · [ISOE-Studie Klimaanpassung (Sept. 2025)](https://www.deutschesklimaportal.de/SharedDocs/Kurzmeldungen/DE/Andere/2025/ISOE_Studie_Klimaanpassung_20250916.html)

## 4. Zielbild: 1:1-KWRA-Katalog mit 52 Risiken (M0–M4) + M5-Perspektive

**Risiko-Arithmetik: M0–M4 = 31 „sehr dringend" + 23 „dringend" − 2 kommunal nicht relevante (#33, #81) = 52 KWRA-Risiken · davon 15 NEU (heute ohne KAP2-Pendant) und 37 per 1:1-Umschnitt aus dem Bestand · 16 Bestandsrisiken → M5.**

Grundsätze des Umbaus:

1. **Eine Klimawirkung = ein Risiko, unter ihrem KWRA-Namen.** Bündel-Risiken werden gestrichen und ersetzt. Outcome-Größen (Mortalität, Erkrankungen, Belastungsstunden, €) sind **Ausweis-Dimensionen innerhalb eines Risikos**, keine eigenen Risiken — „Hitzebelastung" (#95) weist z. B. Mortalität, Morbidität und thermische Belastung gemeinsam aus.
2. **Dringlichkeit strikt vor Thema:** Alle „sehr dringend" sind bis Ende M2 vollständig freigeschaltet; „dringend" beginnt exakt mit M3.
3. Risiken tragen künftig das **KWRA-Label + ID**; die bisherigen KAP2-Codes werden im Katalog-Umbau migriert (Folgevorhaben, §8).
4. **Küsten-Risiken** (#39, #44, #45, #46, #47) sind nur für Küstenkommunen aktiv (bestehendes `coastal`-Flag).

**Ausgeschlossen (kommunal nicht relevant, Relevanzregel [KATALOG_KRITIK.md](KATALOG_KRITIK.md) A.0):** #33 „Entkopplung von Nahrungsbeziehungen in der Ostsee" (rein marin-ökologisch, kommunal weder steuerbar noch bezifferbar) · #81 „Beeinträchtigung des internationalen Warentransports" (international verortet). Die 4 Klimawirkungen „ohne Anpassungsoption" (#1, #6, #16, #18) sowie rein vorgelagerte physische Wirkungen (#14, #15, #38, #40–43, #48, #49) bleiben Gefahren-/Screening-Layer, keine Risiken.

### 4.1 Risiken je KWRA-Cluster

| Cluster | M0 | M1 | M2 | M3 | M4 | **Σ M0–M4** | davon SD / D |
|---|---:|---:|---:|---:|---:|---:|---|
| **Land** (Biol. Vielfalt, Boden, Landwirtschaft, Wald) | — | 6 | 7 | — | 7 | **20** | 13 / 7 |
| **Wasser** (Fischerei, Küste, Wasserhaushalt) | — | 5 | 4 | 2 | 2 | **13** | 9 / 4 |
| **Infrastruktur** (Bauwesen, Energie, Verkehr) | — | 4 | 1 | 4 | — | **9** | 5 / 4 |
| **Wirtschaft** (Industrie & Gewerbe, Tourismus) | — | — | 1 | 3 | 1 | **5** | 1 / 4 |
| **Gesundheit** (Menschliche Gesundheit) | 3 | — | — | 2 | — | **5** | 3 / 2 |
| **Σ** | **3** | **15** | **13** | **11** | **10** | **52** | **31 / 21** |

Lesehinweise: (a) **Land ist mit 20 Risiken das größte Cluster** — direkte Folge der KWRA-Bewertung: Boden, Wald und Landwirtschaft stellen 13 der 31 sehr dringenden Klimawirkungen. (b) **Energiewirtschaft steuert kein einziges Risiko zu M0–M4 bei** — alle 6 Energie-Klimawirkungen sind KWRA-seitig „gering" (→ M5); die heutigen Energie-/KI-Ausfall-Risiken wandern entsprechend nach M5. (c) Gesundheit wirkt klein (5), stellt aber das komplette MVP: alle drei sehr dringenden Gesundheits-Klimawirkungen.

### 4.2 Gestrichene Bündel-Risiken und ihr Ersatz

| Bestandsrisiko (entfällt) | Ersetzt durch KWRA-Einzelrisiken |
|---|---|
| Landwirtschaftliche Schäden (€) | #19 Produktionsfunktionen · #21 Abiotischer Stress · #25 Ertragsausfälle (+ #56 in M4, #20 in M5) |
| Bodenverluste/-degradation (€ + ha) | #10 Erosion Wasser · #11 Erosion Wind |
| Forst-/Vegetationsschäden | #8 Schäden an Wäldern · #27 Hitze-/Trockenstress · #30 Waldbrand (+ NEU #28, #31) |
| Hydrologische Belastung (Index) | #13 Wassermangel Boden · #51 Sturzfluten · #55 Grundwasser |
| Erwartete Mortalität (Hitze) · Morbidität (Hitze) · Stunden thermischer Belastung | gehen in **#95 Hitzebelastung** auf (Outcome-Dimensionen Mortalität, Erkrankungen, Belastungsstunden); Hitze-Sachschäden → #62 |
| Gewässer-/Luftbelastung | #53 Gewässertemperatur/biol. Qualität · #54 chemische Wasserqualität |
| Habitatverlust | #7 wassergebundene Habitate · #44 Küstenveränderungen (+ #5 in M4) |
| Biodiversitätsverlust | #3 genetische Vielfalt · #4 Areale/Bestände |
| Fischerei-Indizes (2) | #35 Fischarten in Fließgewässern |
| Gebäudeschäden (€) | #59 Starkregen · #60 Flusshochwasser · #46 Küste (Sturm-Anteil → #29 bzw. M5/#101) |
| Verkehrsschäden + -unterbrechungen | #74 Hochwasser · #75 gravitative Massenbewegungen |
| Abwasser-Ausfallstunden | #47 Entwässerung Küste · #52 Kanalnetze/Kläranlagen |
| Wasserversorgungs-Ausfallstunden | #85 Wasserbedarf (+ #57 in M5) |
| Energieinfrastruktur-Schäden (€) | #76 Verkehrsleitsysteme/Oberleitungen/Stromversorgung |
| Hitzeschäden an Technik & Infrastruktur (€, geplantes Neu-Risiko der Vorfassung) | #62 Stadtklima/Wärmeinseln (€-Outcome; nimmt die Hitze-Anteile der Gebäude-/Verkehrs-/Energie-Schäden auf) |
| Lieferkettenunterbrechungen · Schadstoffexposition · Med. Unterversorgung · Hangrutsch-Verletzte · Ökosystemleistungen | #78 · #100 · #102 · #12 · #9 (Umbenennung auf KWRA-Label) |

### 4.3 Neue Risiken (15 — heute ohne KAP2-Pendant)

Sehr dringend (10): #2 Invasive Arten · #28 Wald-Schädlinge/Krankheiten · #31 Holzertrag · #50 Versagen von Hochwasserschutzsystemen · #61 Vegetation in Siedlungen · #63 Innenraumklima · #71 Binnenschifffahrt (Niedrigwasser) · #82 Warenverkehr Wasserstraßen (Inland) · #96 Aeroallergene · #98 UV-Gesundheitsschädigungen.
Dringend (5): #29 Windwurf · #32 Nutzfunktion Erholung (Wald) · #45 Küstenschutzsysteme · #87 Leistungseinbußen von Beschäftigten · #94 Tourismuswirtschaft (Chancen/Risiken).

**Maßnahmen-Seite:** Die alte Arithmetik „47 + 2 − 2 = 47" hält nicht mehr. Für NEU-Risiken ohne passende Bestandsmaßnahme werden **~10 neue Maßnahmen** budgetiert: Sommerlicher Wärmeschutz im Gebäudebestand (#63) · UV-Schutz im öffentlichen Raum (#98) · Allergenarme Stadtbaumwahl & Pollenmonitoring (#96) · Klimaangepasster Waldumbau/Ertragsmanagement (#31) · Forstschutz-/Kalamitätsmanagement (#28) · Management invasiver Arten (#2) · Niedrigwasser-Logistik- & Verlagerungskonzepte (#71/#82) · Küstenschutz-Ertüchtigung (#45) · Klimafeste Erholungsinfrastruktur/Besucherlenkung (#32) · Klimaangepasste Tourismusstrategie (#94). „Arbeitszeitmodelle bei Hitze" wird von Stage 4 nach Stage 3 vorgezogen (#87). Exakte Maßnahmen-Arithmetik: offener Punkt (§8).

## 5. Meilensteine

**Release-Kriterium für jede Stufe: kein freigeschaltetes Risiko ohne mindestens eine verknüpfte Maßnahme; jedes Risiko-Release mit validierten Parametern, zitierfähigen Quellen und dokumentierter Wirkungskette.**

Legende: **SD** = sehr dringend · **D** = dringend · Status: bestehend / Split (aus Bündel-Risiko) / **NEU**.

### M0 — Verschlankung & MVP „Gesundheit" (3 R / 4 M) — fix bis 28.08.2026

Die drei sehr dringenden Klimawirkungen des Handlungsfelds Menschliche Gesundheit — namentlich aus der KWRA:

| KWRA | Risiko | Dringl. | Status | Maßnahme(n) |
|---|---|---|---|---|
| #95 | Hitzebelastung *(Ausweis: Mortalität, Erkrankungen, €)* | SD | bestehend (fusioniert aus Hitze-Mortalität, -Morbidität, thermischer Belastung) | Hitzeaktionspläne · Schutzprogramme vulnerable Gruppen |
| #96 | Allergische Reaktionen durch Aeroallergene pflanzlicher Herkunft | SD | **NEU** | **NEU:** Allergenarme Stadtbaumwahl & Pollenmonitoring |
| #98 | UV-bedingte Gesundheitsschädigungen (insbesondere Hautkrebs) | SD | **NEU** | **NEU:** UV-Schutz im öffentlichen Raum |

- **Scoping zuerst (3–4 Tage):** Validierung dieser Fassung (Batch-Zuschnitt M1/M2, Velocity-Annahme für 1:1-Risiken, Maßnahmen-Zuordnung). Der Scoping-Block liegt innerhalb des M0-Fensters.
- **Verschlankung:** Landing auf ein Minimum, Produkt-Shell minimal, Auxiliary-/H/E/V-Layer nur soweit die drei aktiven Wirkungsketten sie benötigen. **Demo offline** (kehrt in Stage 2 zurück).
- **Release:** offen und kostenlos, einfacher Feedback-Kanal.

### M1 — Stage 1: +15 → 18 (nur SD), drei Batches à 5 — bis ~02.10.2026

| Batch | KWRA | Risiko | Status | Maßnahme(n) |
|---|---|---|---|---|
| **1.1 Stadt & Gebäude** | #62 | Stadtklima / Wärmeinseln *(Ausweis: thermische Belastung, Hitzeschäden €)* | Umschnitt (nimmt die Hitze-Anteile der Gebäude-/Verkehrs-/Energie-Schäden auf) | Stadtgrün · Hitzeresiliente Beläge · Schatten/Wasser im öffentlichen Raum |
| | #63 | Innenraumklima | **NEU** | **NEU:** Sommerlicher Wärmeschutz im Gebäudebestand |
| | #61 | Vegetation in Siedlungen | **NEU** | Stadtgrün · Begrünte Dächer/Fassaden |
| | #60 | Schäden an Gebäuden aufgrund von Flusshochwasser | Umschnitt | Hochwasserschutz (Gebäude) · Deichverstärkung |
| | #50 | Belastung oder Versagen von Hochwasserschutzsystemen | **NEU** | Deichverstärkung · Retention/Polder/Rückhaltebecken |
| **1.2 Wasser & Entwässerung** | #51 | Sturzfluten (Versagen von Entwässerungseinrichtungen und Überflutungsschutzsystemen) | Umschnitt | Entsiegelung/Schwammstadt · Entwässerung (Mulden/Rigolen) |
| | #47 | Überlastung der Entwässerungseinrichtungen in überflutungsgefährdeten Gebieten | Umschnitt | Retention · Versickerungsflächen |
| | #55 | Grundwasserstand und Grundwasserqualität | Umschnitt | Grundwasseranreicherung |
| | #53 | Gewässertemperatur und Eisbedeckung und biologische Wasserqualität | Umschnitt | Gewässerschutz |
| | #13 | Wassermangel im Boden | Umschnitt | Humusaufbau · Grundwasseranreicherung |
| **1.3 Landwirtschaft & Boden** | #19 | Produktionsfunktionen | Umschnitt | Humusaufbau |
| | #21 | Abiotischer Stress (Pflanzen) | Umschnitt | Trockenresistente Sorten |
| | #25 | Ertragsausfälle | Umschnitt | Wasserspeicher/effiziente Bewässerung |
| | #10 | Bodenerosion durch Wasser | Umschnitt | Erosionsschutz (Hecken, Terrassen) |
| | #11 | Bodenerosion durch Wind | Umschnitt | Erosionsschutz |

### M2 — Stage 2: +13 → 31 — **alle 31 SD komplett** — Zugangs-/Feedback-Gate — bis ~06.11.2026

- **Zugang nur noch mit Anmeldung (KAP3-Prüfung/Freigabe); Feedback-Pflicht; Demo wieder online.**

| Batch | KWRA | Risiko | Status | Maßnahme(n) |
|---|---|---|---|---|
| **2.1 Wald** | #8 | Schäden an Wäldern | Umschnitt | Mischwälder |
| | #27 | Hitze- und Trockenstress | Umschnitt | Mischwälder |
| | #30 | Waldbrandrisiko | Umschnitt | Brandprävention |
| | #28 | Stress durch Schädlinge / Krankheiten (Wald) | **NEU** | **NEU:** Forstschutz-/Kalamitätsmanagement |
| | #31 | Nutzfunktion: Holzertrag | **NEU** | **NEU:** Klimaangepasster Waldumbau/Ertragsmanagement |
| **2.2 Natur & Gewässer** | #7 | Schäden an wassergebundenen Habitaten und Feuchtgebieten | Umschnitt | Auenrenaturierung · Biotopverbund |
| | #35 | Verbreitung von Fischarten in Fließgewässern | Umschnitt | Fischaufstieg/Durchgängigkeit · Laichhabitat-Renaturierung |
| | #2 | Ausbreitung invasiver Arten | **NEU** | **NEU:** Management invasiver Arten |
| **2.3 Küste & Wasserstraßen** *(coastal-Flag außer #71/#82)* | #39 | Wasserqualität und Grundwasserversalzung | Umschnitt | Salzwasserbarrieren |
| | #44 | Naturräumliche Veränderungen an Küsten | Umschnitt | Küstenschutz/Renaturierung |
| | #46 | Beschädigung oder Zerstörung von Siedlung und Infrastruktur an der Küste | Umschnitt | Deichverstärkung · Bauverbote in Risikozonen |
| | #71 | Schiffbarkeit der Binnenschifffahrtsstraßen (Niedrigwasser) | **NEU** | **NEU:** Niedrigwasser-Logistik-/Verlagerungskonzepte |
| | #82 | Beeinträchtigung des Warenverkehrs über Wasserstraßen (Inland) | **NEU** | dito (geteilte Maßnahme) |

### M3 — Stage 3: +11 → 42 (D-Block Infrastruktur, Wirtschaft & Gesundheit) — Kommerzialisierung — bis ~25.12.2026

| KWRA | Risiko | Status | Maßnahme(n) |
|---|---|---|---|
| #74 | Schäden/Hindernisse bei Straßen und Schienenwegen (Hochwasser) | Umschnitt | Schutz kritischer Knoten |
| #75 | Schäden/Hindernisse bei Straßen und Schienenwegen (gravitative Massenbewegungen) | Umschnitt | Schutz kritischer Knoten |
| #76 | Schäden an Verkehrsleitsystemen, Oberleitungen und Stromversorgungsanlagen | Umschnitt | Netzverstärkung/Redundanzen |
| #59 | Schäden an Gebäuden aufgrund von Starkregen | Umschnitt | Präventionsanreize · Hochwasserschutz (Gebäude) |
| #52 | Einschränkungen der Funktionsfähigkeit von Kanalnetzen und Vorflutern und Kläranlagen | Umschnitt | Leckage-Reduktion · Entwässerung |
| #54 | Chemische Wasserqualität | Umschnitt | Gewässerschutz |
| #85 | Wasserbedarf | Umschnitt | Wasserspeicher/effiziente Bewässerung |
| #78 | Beeinträchtigung der Versorgung mit Rohstoffen und Zwischenprodukten (international) | Umschnitt | Lieferketten-Resilienz |
| #87 | Leistungseinbußen von Beschäftigten | **NEU** | Arbeitszeitmodelle bei Hitze (vorgezogen) |
| #100 | Atembeschwerden (aufgrund von Luftverunreinigungen) | Umschnitt | Frischluftschneisen |
| #102 | Auswirkungen auf das Gesundheitssystem | Umschnitt | Kühle Räume/Kühlzentren · Hitzeaktionspläne |

- **Kommerzialisierung** gemäß [BUSINESSPLAN.md](BUSINESSPLAN.md) (0,10 €/EW p. a., Mindestpreis): Voraussetzungen Benutzerverwaltung/Mandantentrennung, Abrechnung, PDF-Ergebnisbericht.
- **Version-Gating:** wie bisher (Snapshot-Konzept, Abschnitt 7).

### M3½ — Studien-Release *(interne Stufenbezeichnung, wird nicht offiziell gezeigt)* — bis ~15.01.2027

- Deutschland-weite Studie über alle Kommunen zur öffentlichen Aufmerksamkeit (Kanal `/studie` existiert).
- Aufwand **≈ 1 Monat**. **Interner Vermerk:** Rechenläufe **parallel zur Stage-3-Entwicklung auf Basis der Stage-2-Ergebnisse (31 Risiken — der komplette SD-Block, inhaltlich stärker als die bisherige 25er-Basis)**. Nach M3 verbleiben Auswertung, Aufbereitung, Redaktion (~2 Wochen).

### M4 — Stage 4: +10 → 52 (D-Rest Natur, Küste, Wald & Tourismus) — bis ~12.02.2027

| KWRA | Risiko | Status | Maßnahme(n) |
|---|---|---|---|
| #3 | Verlust an genetischer Vielfalt | Umschnitt | Biotopverbund |
| #4 | Verschiebung von Arealen und Rückgang der Bestände | Umschnitt | Biotopverbund |
| #5 | Schäden an Küstenökosystemen *(coastal)* | Umschnitt | Küstenschutz/Renaturierung |
| #9 | Ökosystemleistungen | Umbenennung | Auenrenaturierung · Biotopverbund |
| #12 | Rutschungen und Muren | Umbenennung | Frühwarnsysteme |
| #29 | Schäden durch Windwurf | **NEU** (re-verankerter Sturm-Split; urbane Sturmschäden darüber hinaus → M5/#101) | Mischwälder · Risikobasierte Investitionen |
| #32 | Nutzfunktion: Erholung | **NEU** | **NEU:** Klimafeste Erholungsinfrastruktur/Besucherlenkung |
| #45 | Höhere Belastung oder Versagen von Küstenschutzsystemen *(coastal)* | **NEU** | **NEU:** Küstenschutz-Ertüchtigung |
| #56 | Mangel an Bewässerungswasser | Umschnitt | Wasserspeicher/effiziente Bewässerung |
| #94 | Wirtschaftliche Chancen und Risiken für die Tourismuswirtschaft | **NEU** | **NEU:** Klimaangepasste Tourismusstrategie |

### M5 — Perspektive (Termin offen)

Alles nicht (sehr) Dringende — bewusst ohne Termin, gelistet unter den KWRA-Labels:

**Block A — KWRA-Klimawirkungen, nicht als (sehr) dringend ausgewiesen:**

| KWRA | Klimawirkung | Enthält heutige KAP2-Risiken |
|---|---|---|
| #101 | Verletzungen und Todesfälle infolge von Extremereignissen (gering/mittel) | Flut-/Sturm-Mortalität · Flut-/Sturm-Verletzte · Betroffene/Evakuierte; perspektivisch urbane Sturm-Sachschäden |
| #70 | Fehlende Zuverlässigkeit der Energieversorgung (gering) | Ausfallstunden Energieversorgung · Ausfallzeiten kritischer Infrastruktur |
| #57 | Trinkwasser | Ausfallstunden Wasserversorgung (Trinkwasser-Anteil) |
| #37 | Schäden an Aquakulturen | Schäden Aquakultur (€) |
| #20 | Hitzestress bei und Leistung von Nutztieren | — (Erweiterung der Landwirtschafts-Risiken) |
| #65 / #86 / #88 | Kühlenergie-Bedarf · Freisetzung gefährlicher Stoffe · Produktionsprozesse | — |
| #90–#93 | Tourismus-Einzelaspekte (Schneesicherheit, Gesundheitstourismus, touristische Infrastruktur, Nachfrageverlagerung) | — |
| #97 / #99 | Mikroorganismen/Algen · Vektoren | — |

**Block B — KAP2-Plus (kein KWRA-Pendant):** Psychische Belastungsfälle · Kosten klimabedingter Migration · Verstärkung sozialer Ungleichheiten · Systemische Dominoeffekte · Schäden Telekommunikation + Ausfallzeiten Kommunikation · Funktionsausfälle Verwaltung/Dienste (fusioniert aus Admin-Ausfallzeiten + Funktionsausfall-Dauer) · Wirtschaftliche Standortnachteile · Indirekte wirtschaftliche Verluste · Wiederherstellungskosten · Schäden Wasser-/Abwasserinfrastruktur (€) · Wirtschaftliche Verluste Fischerei (€) · Ökosystem-/Ressourcenkonflikt-Indizes.

*Nicht aufgenommen (kommunal nicht relevant):* #33, #81 (Begründung §4).

## 6. Timeline und Annahmen

**Annahmen:** Start 05.08.2026 · Velocity **5 Risiken inkl. zugehöriger Maßnahmen pro Woche** · Zusatzaufwände (Verschlankung, Gates, Kommerzialisierung, Studie) als Schätzung · auf alles **+20 % Puffer** · sequenzielle Abarbeitung (Ausnahme: Studien-Rechenläufe parallel zu Stage 3).

| Meilenstein | Risiko-Arbeit | Zusatzaufwand | inkl. 20 % Puffer | Fertig (ca.) |
|---|---|---|---|---|
| M0 MVP | 3 R → 0,6 Wo | Scoping 3–4 Tage + Verschlankung/Release-Setup + Neumodellierung #96/#98 ≈ 2,5 Wo | ≈ 3,5 Wo (gedeckelt, ambitioniert) | **28.08.2026 (fix)** |
| M1 Stage 1 | +15 R → 3 Wo | Neumodellierung (3 NEU-Risiken, 2 neue Maßnahmen) ≈ 1 Wo | ≈ 5 Wo | **~02.10.2026** |
| M2 Stage 2 | +13 R → 2,6 Wo | Anmelde-/Prüf-Gate (KAP3), Feedback-Gate, Demo ≈ 2 Wo | ≈ 5 Wo (eng) | **~06.11.2026** |
| M3 Stage 3 | +11 R → 2,2 Wo | Auth/Multi-Tenancy, Version-Gating/Snapshots, Billing, PDF-Bericht ≈ 4 Wo | ≈ 7,5 Wo | **~25.12.2026** |
| M3½ Studie | — | ≈ 4 Wo gesamt, davon ~2 Wo Rechenläufe parallel zu Stage 3 (auf Stage-2-Basis) | ≈ 2,5 Wo sequenziell | **~15.01.2027** |
| M4 Stage 4 | +10 R → 2 Wo | Katalog-Migration (Splits/Umbenennungen, Altdaten) ≈ 1 Wo | ≈ 3,5 Wo | **~12.02.2027** |
| M5 Perspektive | — | — | — | **Termin offen** |

**Hinweise:** (a) Alle Termine sind Grobschätzungen inkl. Puffer und **gegenüber der Vorfassung unverändert**. (b) Der Mehrumfang (52 statt 45 Einheiten) wird durch den schmaleren 1:1-Zuschnitt kompensiert — ein umgeschnittenes Risiko umfasst eine Klimawirkung und eine Schadensfunktion statt drei; diese Annahme wird im M0-Scoping validiert (§8). (c) M0 bleibt auf den 28.08.2026 fixiert — enthält jetzt aber zwei Neumodellierungen (#96, #98); das Scoping prüft die Haltbarkeit zuerst. (d) M5 ist bewusst unterminiert und erhält keine Timeline-Zeile mit Datum.

## 7. Querschnitts-Workstreams

- **Methodik-Validierung je Batch:** Review der Parameter, Quellen und Wirkungsketten vor jedem Release (Ratchet-Tests fortführen); Ergebnis dokumentiert im Berechnungshandbuch.
- **Feedback-Infrastruktur:** M0 einfacher Kanal → M2 strukturiertes Pflicht-Feedback als Nutzungsbedingung; Auswertung fließt in die Batch-Priorisierung ein.
- **Versionierung & Free-Tier-Gating (Neuentwicklung):** Analyse-Snapshots je Kommune und Modellstand (heute: destruktives Überschreiben; vorhandene Bausteine: `MODEL_VERSION`, `recalc_recommended`, Lite-`batch_id`). Alte Stände bleiben lesbar, Neuberechnung nur mit aktueller Lizenzstufe; kein Downgrade in kleinere Versionen.
- **Anmelde-Prüfung (ab Stage 2):** Registrierung mit Freigabe-Workflow durch KAP3.
- **Verschlankung & Re-Expansion:** Landing/Produkt/Layer wachsen mit den Stufen kontrolliert wieder mit — nur was aktive Risiken benötigen, wird angezeigt.
- **Kommerzialisierungs-Voraussetzungen (bis M3):** Benutzerverwaltung/Mandantentrennung, Abrechnung, PDF-Ergebnisbericht (siehe [BUSINESSPLAN.md](BUSINESSPLAN.md)).

## 8. Offene Punkte

1. **M0-Scoping** (3–4 Tage) bestätigt oder korrigiert: Batch-Zuschnitt M1/M2, Maßnahmen-Zuordnung je Risiko — und validiert die zentrale Velocity-Annahme, dass 1:1-zugeschnittene Risiken im Schnitt schmaler sind als die bisherigen Bündel-Risiken (sonst verschieben sich M2 ff.).
2. **Modellierungskonzepte für 15 neue Risiken** (statt bisher 2) inkl. Quellenlage je Klimawirkung — insbesondere Innenraumklima (#63), UV (#98), Aeroallergene (#96), Holzertrag (#31), Tourismuswirtschaft (#94).
3. **Maßnahmen-Arithmetik neu aufstellen:** ~10 neue Maßnahmen (Liste §4.3) beziffern und quellenbelegen; welche Bestandsmaßnahmen wandern mit ihren einzigen Zielrisiken nach M5 (z. B. geplante „Psychosoziale Versorgung", „Klimaresiliente Standortentwicklung")?
4. **Katalog-Umbau als Folgevorhaben terminieren:** Splits/Umbenennungen in `catalog.py` (Codes, `CellAssessment`-Migration, Exporte) — die Roadmap beschreibt das Zielbild, nicht die Migration.
5. Ausgestaltung der KAP3-Anmeldeprüfung (Kriterien, SLA der Freigabe).
6. Feedback-Pflicht: Form (Fragebogen, Interview, Datenfreigabe?) und Schwelle, ab der die Nutzung gesperrt wird.
7. Zuschnitt der Studie (M3½): Fragestellung, Kommunen-Auswahl, Reviewer — jetzt auf 33-Risiken-Basis (SD komplett).
8. **PDF-/Public-Fassungen neu erzeugen** (ablage/ROADMAP.pdf und ablage/ROADMAP_PUBLIC.* sind eingefroren und entsprechen der Vorfassung).
