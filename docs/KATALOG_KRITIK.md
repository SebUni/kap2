# KAP2 — Katalog-Kritik: Struktur des Risiko- und Maßnahmenkatalogs

*Stand: August 2026 · Internes Dokument · Reine Analyse, keine Code-Änderung · Ergänzt [MODELL_KRITIK.md](MODELL_KRITIK.md), [ROADMAP.md](ROADMAP.md), [BERECHNUNGS_HANDBUCH.md](BERECHNUNGS_HANDBUCH.md)*

Geprüfte Code-Stände: `backend/app/data/catalog.py` (`MODEL_VERSION = "2026.08-mortalitaet-erf"`, Zeile 3585), `backend/app/data/pathway_curation.py`, `backend/app/services/engine/impact/`, `frontend/src/components/LayerPanel.tsx`, `frontend/src/components/dashboard/RiskRadarSection.tsx`.
Primärquellen: KWRA 2021 Teilbericht 6 (Tabelle 1, 25, 26), KWRA 2021 Kurzfassung, KAnG §§ 3, 8, 10, 12, DAS 2024.

---

## Kurzfazit vorab

**Der Katalog ist nicht chaotisch aus Nachlässigkeit — er ist chaotisch, weil er vier Taxonomien gleichzeitig halb bedient und keine davon als verbindliche Primärachse festlegt:** die fünf KWRA-Risikofelder (`group`), die vier Kostendimensionen (`cost_dimension`), die sieben KAnG-Cluster (nur bei Maßnahmen) und die KWRA-Handlungsfelder (nur als Freitext-Tooltip). Jede dieser Achsen ist für sich sinnvoll; nebeneinander erzeugen sie genau den Eindruck willkürlicher Einzel-Picks, den der Product Owner beschreibt.

**Zur Grundsatzfrage MECE vs. spezifische Picks lautet das Urteil: Die Frage ist auf einer Ebene nicht entscheidbar.** Vollständigkeit verlangt Zellen, für die es keine belastbaren Daten gibt; Datenehrlichkeit verlangt Lücken, die den Konformitätsanspruch untergraben. Beides gleichzeitig geht nur, wenn man Vollständigkeit und Quantifizierung auf **zwei getrennte Ebenen** legt — dieselbe Trennung, die [MODELL_KRITIK.md](MODELL_KRITIK.md) §5 bereits für Screening und Absolutwerte durchgesetzt hat.

**Der Abgleich mit dem Bund ist der härteste Befund dieses Berichts:** Von den 102 Klimawirkungen der KWRA 2021 sind 15 in KAP2 abgedeckt, 36 teilweise, **36 fehlen vollständig** und 15 sind kommunal nicht relevant. Unter den fehlenden sind **10 der 31 Klimawirkungen, die der Bund als „sehr dringende Handlungserfordernisse" einstuft** — darunter „Vegetation in Siedlungen", „Innenraumklima", „Belastung oder Versagen von Hochwasserschutzsystemen" und „UV-bedingte Gesundheitsschädigungen", also durchweg kommunale Kernthemen. Das Handlungsfeld „Tourismuswirtschaft" fehlt vollständig (0 von 5), das KWRA-Schutzgut „kulturelles Erbe" (23 Klimawirkungen) hat in KAP2 kein einziges Risiko.

**Empfehlung: Variante E-stufig** (Abschnitt 7) — Zwei-Ebenen-Modell mit dem kommunal relevanten KWRA-Universum als MECE-Screening-Ebene und einem nach Gefahr × Schutzgut systematisierten, quantifizierten Kern; KAnG-Handlungsfelder werden als Sekundär-Tag an die Risiken gehängt statt als Primärachse. Sofortmaßnahme ist Variante A (Aufwand S–M), Zielbild ist deckungsgleich mit den ROADMAP-Stufen M1–M4. Vergleich aller Varianten in Abschnitt 6, Entscheidungsvorlage in Abschnitt 8.

---

## 1. Ist-Zustand: der Katalog in Zahlen

### 1.1 Bestand

| Ebene | Anzahl | Fundstelle |
|---|---|---|
| Klimagefahren (Hazards) | 23 | `catalog.py:52` |
| Expositionen | 24 | `catalog.py:206` |
| Vulnerabilitäten | 33 | `catalog.py:356` |
| **Risiken** | **51** | `catalog.py:522` |
| **Maßnahmen** | **47** | `catalog.py:1513` |
| Auxiliary-Layer | 60 | `catalog_auxiliary.py` |

### 1.2 Die vier konkurrierenden Taxonomien

| Achse | Werte | Gilt für | Fundstelle | Problem |
|---|---|---|---|---|
| `group` (KWRA-Risikofeld) | 5: heat 4 · drought 13 · flood 15 · gradual 6 · compound 13 | Risiken | `catalog.py:27` | Primärachse in UI und Radar, aber stark unsymmetrisch besetzt |
| `cost_dimension` | 4: monetary 16 · health 13 · operational 11 · environment 11 | Risiken | Risikodefinitionen | Nur Aggregationshilfe, in der UI nicht als Struktur sichtbar |
| KAnG-Cluster / Handlungsfeld | 7 / 17 | **nur Maßnahmen** | `catalog.py:3392`, `_MEASURE_KANG_MAP:3477` | Risiken haben kein Gegenstück |
| KWRA-Handlungsfeld | 39 Freitext-Varianten | Risiken | `pathway_curation.py` (`"cluster"`) | Freitext, kein Code, nur Tooltip; nicht filterbar, nicht testbar |

Die fünf `group`-Werte sind laut `catalog.py:27` an die Konstanten `KWRA_CHALLENGE_*` gebunden. Sie sind **keine KWRA-Kategorie** — die KWRA 2021 kennt 13 Handlungsfelder und 5 Cluster, aber keine Einteilung in „Hitze / Trockenheit / Hochwasser / Gradueller Wandel / Verbund". Diese fünf Felder sind eine KAP2-Eigenschöpfung entlang von **Gefahrentypen**. Das ist legitim und für Kommunen gut verständlich, aber der Name „KWRA-Risikofelder" (so in [PRODUKTBESCHREIBUNG.md](PRODUKTBESCHREIBUNG.md) und im Radar) suggeriert eine Herkunft, die es nicht gibt.

### 1.3 Befunde B1–B8

Diese acht Befunde sind das Referenzsystem für den Rest des Berichts; jede Variante in Abschnitt 5 wird gegen sie geprüft.

**B1 — Hitze-Schiefstand.** Nur 4 von 51 Risiken liegen in `group = heat`, obwohl Hitze nach [ROADMAP.md](ROADMAP.md) §3 der Kommunen-Pain #1 ist und die KWRA „Hitzebelastung" als einzige Klimawirkung überhaupt schon **in der Gegenwart** mit hohem Klimarisiko bewertet. Die Ursache ist die Achsenwahl: `group` gruppiert nach Gefahr, aber alle Sachschaden-Risiken (`EXPECTED_BUILDING_DAMAGE_EUR`, `EXPECTED_TRANSPORT_DAMAGE_EUR`, `EXPECTED_ENERGY_INFRA_DAMAGE_EUR` …) wurden pauschal `flood` zugewiesen, auch soweit sie von `HEAT_WAVE` getrieben werden. Da der Gruppen-Index als Mittel der Risiko-P90 gebildet wird (`risk_engine.py:307`), verzerrt das direkt die Radar-Darstellung.

**B2 — 18 von 51 Risiken haben keine einzige verknüpfte Maßnahme.** Für den Nutzer entsteht das Kernversprechen „Risiko → Maßnahme → Kosten-Nutzen" bei mehr als einem Drittel des Katalogs gar nicht erst. *(Hinweis: [ROADMAP.md](ROADMAP.md) §2 nennt noch 22 — der Wert ist inzwischen auf 18 gesunken, siehe B8.)*

**B3 — Proxy-Verknüpfung bei Maßnahmen.** Weil passende Zielrisiken fehlen, zahlen Maßnahmen auf Ersatzrisiken ein. `HEAT_WORK_SCHEDULES` („Arbeitszeitmodelle bei Hitze") wirkt formal auf `EXPECTED_THERMAL_STRESS_HOURS`, weil das KWRA-Pendant „Leistungseinbußen von Beschäftigten" nicht existiert. `URBAN_GREEN` wirkt auf dasselbe Risiko, weil „Vegetation in Siedlungen" als eigenes Risiko fehlt. Der Effekt: ein einzelnes Risiko sammelt die Wirkung mehrerer inhaltlich verschiedener Maßnahmen ein.

**B4 — 25 von 51 Risiken laufen weiterhin im linearen Legacy-Pfad** (`ref · Index/100 · Skalierung`), weil sie in `IMPACT_FUNCTIONS` keinen Eintrag haben — betroffen sind alle 9 operativen Stunden-Risiken und alle 11 Index-Risiken.

**B5 — 14 Risiken tragen nichts zur Schadenssumme bei.** 11 Index-Risiken sind bewusst nicht monetarisiert (`INDEX_ONLY_RISK_CODES`, `catalog.py:939`), 3 weitere werden auf 0 € gesetzt (`CONSOLIDATED_INTO_INDIRECT_CODES`, `catalog.py:961`). Das ist methodisch richtig (Doppelzählung), aber im Katalog stehen sie gleichrangig neben Risiken mit €-Wert — die Zweiklassigkeit ist eine Eigenschaft der Daten, nicht der Struktur.

**B6 — Semantisch gemischte Benennung.** Der Katalog vermischt drei Namenslogiken ohne Kennzeichnung: **Outcome-basiert** (`EXPECTED_ANNUAL_MORTALITY` — ein zählbarer Schaden), **zustandsbasiert** (`HYDROLOGICAL_STRESS_RISK_INDEX` — ein Systemzustand), **servicebasiert** (`EXPECTED_CI_OUTAGE_HOURS` — eine Leistungsunterbrechung). Es existieren neun verschiedene Outcome-Einheiten (Todesfälle, Fälle, Verletzte, Personen, Stunden, €, ha, Arten, Index). Genau das erzeugt beim Lesen der Liste den Eindruck von Willkür, den der Product Owner beschreibt — und es ist derselbe Eindruck, den seine eigene Beobachtung („Mortalität, Morbidität, finanzielle Schäden, Schäden an Natur und Tieren") bereits als **latent vorhandene Wirkungsdimensions-Logik** benennt.

**B7 — Taxonomie-Asymmetrie zwischen Risiken und Maßnahmen.** Maßnahmen tragen `kang_cluster` und `kang_field` (`catalog.py:3535`), Risiken nicht. Im Maßnahmen-Anlegen-Dialog (`MapView.tsx:876–1005`) muss der Nutzer deshalb zwischen zwei völlig getrennten Einstiegen wählen — „Nach Handlungsfeld" oder „Nach Ziel-Risiko" —, weil die beiden Hälften des Produkts verschiedene Sprachen sprechen.

**B8 — Doku-Drift.** [PRODUKTBESCHREIBUNG.md](PRODUKTBESCHREIBUNG.md) und [BUSINESSPLAN.md](BUSINESSPLAN.md) nennen 47 Risiken, tatsächlich sind es 51. Die ROADMAP nennt 22 maßnahmenlose Risiken, tatsächlich sind es 18. Ein Katalog ohne verbindliche Struktur erzeugt zwangsläufig Zahlen, die niemand nachrechnet.

---

## 2. Normativer Rahmen: was KAnG, DAS und KWRA tatsächlich verlangen

Die drei Begriffe werden im Projekt teils synonym verwendet. Sie sind es nicht, und der Unterschied entscheidet, welche Taxonomie überhaupt bindend ist.

### 2.1 KAnG — das Gesetz

Das Bundes-Klimaanpassungsgesetz verpflichtet, es strukturiert aber nicht die Risiken:

- **§ 12** (Klimaanpassungskonzepte für Gemeinden und Kreise): Die Länder bestimmen die Stellen, die für jedes Gemeinde- und Kreisgebiet ein Klimaanpassungskonzept aufstellen. Die Konzepte **„sollen auf einer Klimarisikoanalyse im Sinne einer Feststellung von potentiellen prioritären Risiken und sehr dringlichen Handlungserfordernissen (Betroffenheitsanalyse) … beruhen"** und münden in einen ortsbezogenen Maßnahmenkatalog. Ausdrücklich zu behandeln sind Maßnahmen bei **extremen Hitzelagen, extremer Dürre und Starkregen**.
- **§ 8 Abs. 1 Nr. 1–4** (Berücksichtigungsgebot): Träger öffentlicher Aufgaben müssen das Ziel der Klimaanpassung fachübergreifend berücksichtigen, namentlich gegenüber Überflutung bei Starkregen/Sturzfluten/Hochwasser, Absinken des Grundwasserspiegels und Trockenheit, Bodenerosion sowie dem Wärmeinsel-Effekt.
- **§ 10**: Länderstrategien inkl. Risikoanalyse und Maßnahmenkatalog bis **31. Januar 2027**, Fortschreibung mindestens alle fünf Jahre.
- **§ 3 Abs. 2**: nennt die **sieben Cluster** — Infrastruktur (Energieinfrastruktur, Gebäude, Verkehr); Land und Landnutzung (biologische Vielfalt, Boden, Landwirtschaft, Wald- und Forstwirtschaft); menschliche Gesundheit und Pflege; Stadtentwicklung, Raumplanung und Bevölkerungsschutz; Wasser (Fischerei, Küsten- und Meeresschutz, Wasserhaushalt/Wasserwirtschaft); Wirtschaft (Finanzwirtschaft, Industrie und Gewerbe); übergreifende Handlungsfelder.

**Zwei Konsequenzen.** Erstens: Die `KANG_CLUSTERS` in `catalog.py:3392` bilden § 3 Abs. 2 korrekt ab — das ist belastbar. Zweitens, und wichtiger: **Die Cluster des § 3 Abs. 2 strukturieren die Bundesstrategie und ihre Maßnahmen, nicht die Risikoanalyse.** Das Gesetz sagt für § 12 nur, dass eine Risikoanalyse zugrunde liegen muss — es schreibt keine Risiko-Taxonomie vor. Wer die KAnG-Cluster zur Primärachse der Risiken macht, tut mehr, als das Gesetz verlangt, und weniger, als eine Risikosystematik leisten muss (Abschnitt 5, Variante C).

Der Formulierung des § 12 kommt allerdings noch eine zweite Bedeutung zu: Sie verlangt wörtlich die Feststellung **„sehr dringlicher Handlungserfordernisse"** — exakt der Terminus, mit dem die KWRA 2021 ihre 31 prioritären Klimawirkungen bezeichnet (Teilbericht 6, Tabelle 25). Das Gesetz zeigt damit implizit auf die KWRA-Systematik als Referenz. Genau deshalb wiegt der Befund aus Abschnitt 4 so schwer.

### 2.2 DAS 2024 — die Strategie

Die Deutsche Anpassungsstrategie 2024 definiert 33 messbare Ziele und über 180 Maßnahmen entlang derselben sieben Cluster. Sie ordnet dem Cluster Wirtschaft zusätzlich die **Tourismuswirtschaft** zu, die in `_MEASURE_KANG_MAP` (`catalog.py:3477`) fehlt — konsistent damit, dass KAP2 auch kein Tourismus-Risiko führt (Abschnitt 4).

### 2.3 KWRA 2021 — das Analysewerk

Die Klimawirkungs- und Risikoanalyse 2021 des Bundes untersucht **102 Klimawirkungen in 13 Handlungsfeldern**, publiziert in sechs Teilberichten. Für diesen Bericht sind vier Strukturmerkmale entscheidend, weil sie zeigen, dass der Bund selbst mehrachsig arbeitet:

1. **13 Handlungsfelder**, gruppiert in **5 Cluster** (Land, Wasser, Infrastruktur, Wirtschaft, Gesundheit — Erbe der Vulnerabilitätsanalyse 2015).
2. **4 Schutzgüter** — Mensch, Volkswirtschaft, Umwelt, kulturelles Erbe — gewählt in Anlehnung an die Risikoanalyse im Bevölkerungsschutz (BBK 2015) und das UVPG. Zuordnung mit Mehrfachnennung: Mensch 74, Volkswirtschaft 93, Umwelt 46, kulturelles Erbe 23 Klimawirkungen.
3. **5 Systembereiche** — Natürliche Systeme und Ressourcen (N), Naturnutzende Wirtschaftssysteme (Nn), Infrastrukturen und Gebäude (I&G), Naturferne Wirtschaftssysteme (Nf), Menschen und soziale Systeme (M). Jede Klimawirkung trägt in Tabelle 1 des Teilberichts 6 genau eine dieser Marken.
4. **Dreistufige Risikobewertung** (gering/mittel/hoch) über Gegenwart, Mitte und Ende des Jahrhunderts, je optimistischer und pessimistischer Fall, plus **Anpassungsdauer** — daraus abgeleitet die Priorisierung in 31 sehr dringende und 23 dringende Handlungserfordernisse.

**Das ist der methodisch wichtigste Fund dieses Berichts:** Die von KAP2 gesuchte MECE-Achse ist keine Erfindung, die man rechtfertigen müsste — der Bund führt sie bereits. Schutzgüter und Systembereiche sind genau die „Wen trifft es?"-Achse, die dem KAP2-Katalog fehlt (Abschnitt 5, Variante D).

---

## 3. Grundsatzabwägung: MECE-Systematik vs. spezifische Einzelrisiken

### 3.1 Was für MECE spricht

- **Verteidigbarkeit.** Ein Katalog, der sich aus einer Systematik ableitet, muss nicht jede einzelne Aufnahme begründen — nur die Systematik. Die Frage „Warum ist X drin und Y nicht?" ist die häufigste Frage in Fachgesprächen und heute nicht beantwortbar.
- **Anschlussfähigkeit an § 12 KAnG.** Eine Betroffenheitsanalyse, die prioritäre Risiken *feststellt*, muss zuvor einen definierten Suchraum abgeschritten haben. Ein Pick-Katalog kann eine Priorität behaupten, aber nicht herleiten.
- **Lückenfindung wird automatisch.** Die Analyse in Abschnitt 4 war nur möglich, weil der Bund eine Systematik hat. Ohne Bezugsmenge ist „vollständig" kein prüfbarer Begriff.
- **Der Katalog wächst kontrolliert.** Neue Risiken füllen Zellen, statt die Liste zu verlängern.

### 3.2 Was gegen MECE spricht

- **Zellen ohne Daten.** Eine Gefahr × Schutzgut-Matrix erzeugt schnell 30–40 Zellen. Für einen erheblichen Teil existiert keine kommunal auflösbare Datengrundlage und keine belastbare Schadensfunktion. [MODELL_KRITIK.md](MODELL_KRITIK.md) §3 hat für genau dieses Muster — Struktur ausfüllen, Zahl erfinden — die schärfste Kritik formuliert.
- **Vollständigkeitsdruck erzeugt Scheinpräzision.** Eine leere Zelle in einer Matrix wirkt wie ein Versäumnis, ein fehlendes Listenelement wie eine bewusste Entscheidung. Die Matrix erzeugt also Druck in genau die falsche Richtung.
- **MECE ist im Risikobereich nie exakt erreichbar.** Kaskaden- und Verbundrisiken (in KAP2 13 Stück in `group = compound`) sind konstitutiv nicht überschneidungsfrei — sie sind die Wechselwirkung zwischen anderen Zellen. Die KWRA löst das nicht, sie beziffert es: 257 Querverbindungen zwischen den 102 Klimawirkungen.

### 3.3 Was für spezifische Picks spricht — und was dagegen

Für die Picks spricht ihre Ehrlichkeit: Jedes der heute 26 mit echter Wirkungsfunktion hinterlegten Risiken (`IMPACT_FUNCTIONS`) ist rechenbar, weil es *ausgewählt* wurde, weil es rechenbar ist. Gegen sie spricht, dass diese Auswahllogik nirgends dokumentiert ist und deshalb von außen nicht von Willkür unterscheidbar bleibt — plus die konkrete, in Abschnitt 4 belegte Konsequenz, dass 10 der 31 bundesseitig sehr dringenden Handlungserfordernisse schlicht durchgefallen sind.

### 3.4 Das Urteil

Die beiden Argumentationslinien widersprechen sich nicht — **sie beziehen sich auf zwei verschiedene Fragen.** „Haben wir an alles gedacht?" ist eine Frage an die Vollständigkeit des Suchraums. „Können wir diese Zahl verteidigen?" ist eine Frage an die Datengrundlage. Ein einziger, flacher Katalog muss beide gleichzeitig beantworten und scheitert an einer von beiden — heute an der ersten.

**Damit ist die Grundsatzfrage entschieden, sobald man sie richtig stellt: nicht „MECE oder Picks?", sondern „auf welcher Ebene MECE, auf welcher Ebene Picks?".** Dieselbe Auflösung hat [MODELL_KRITIK.md](MODELL_KRITIK.md) §5 bereits für die Rechenlogik gewählt: HxVxE bleibt Screening, Absolutwerte bekommen eine eigene Schicht. Der Katalog hat diese Trennung nur noch nicht nachvollzogen. Sie ist die Grundlage von Variante E.

---

## 4. Lückenanalyse: KAP2 gegen die 102 Klimawirkungen der KWRA 2021

Vollständige Matrix in **Anhang A**. Statuslegende dort; Relevanzregel in A.0.

### 4.1 Abdeckung je Handlungsfeld

| KWRA-Handlungsfeld | Klimawirkungen | abgedeckt | teilweise | **fehlt** | kommunal n. r. |
|---|---:|---:|---:|---:|---:|
| Biologische Vielfalt | 9 | 2 | 4 | 1 | 2 |
| Boden | 10 | 1 | 4 | 4 | 1 |
| Landwirtschaft | 7 | 1 | 1 | 5 | 0 |
| Wald- und Forstwirtschaft | 6 | 0 | 2 | 4 | 0 |
| Fischerei | 5 | 2 | 1 | 0 | 2 |
| Küsten- und Meeresschutz | 10 | 0 | 6 | 1 | 3 |
| Wasserhaushalt, Wasserwirtschaft | 11 | 2 | 8 | 1 | 0 |
| Bauwesen | 6 | 3 | 0 | 2 | 1 |
| Energiewirtschaft | 6 | 1 | 1 | 3 | 1 |
| Verkehr, Verkehrsinfrastruktur | 7 | 1 | 2 | 3 | 1 |
| Industrie und Gewerbe | 12 | 0 | 5 | 3 | 4 |
| **Tourismuswirtschaft** | 5 | 0 | 0 | **5** | 0 |
| Menschliche Gesundheit | 8 | 2 | 2 | 4 | 0 |
| **Summe** | **102** | **15** | **36** | **36** | **15** |

Von den 87 kommunal relevanten Klimawirkungen deckt KAP2 51 ganz oder teilweise ab (59 %); **36 fehlen vollständig (41 %)**.

### 4.2 Der kritische Befund: 10 von 31 sehr dringenden Handlungserfordernissen fehlen

Die KWRA priorisiert 31 Klimawirkungen als „sehr dringende Handlungserfordernisse" (Teilbericht 6, Tabelle 25) — jener Terminus, den § 12 KAnG für kommunale Klimaanpassungskonzepte übernimmt. Davon sind in KAP2 7 abgedeckt, 14 teilweise und **10 gar nicht**:

| Fehlende sehr dringende Klimawirkung | Handlungsfeld | Kommunaler Hebel |
|---|---|---|
| **Vegetation in Siedlungen** | Bauwesen | Sehr hoch — Stadtbaum-Vitalität, Ersatzpflanzung; KAP2 hat die Maßnahme (`URBAN_GREEN`), aber nicht das Risiko |
| **Innenraumklima** | Bauwesen | Sehr hoch — Schulen, Kitas, Pflegeheime, Verwaltungsgebäude in kommunaler Trägerschaft |
| **Belastung oder Versagen von Hochwasserschutzsystemen** | Wasserhaushalt | Sehr hoch — Deiche und Rückhaltebecken in kommunaler Unterhaltung; KAP2 hat `LEVEE_REINFORCEMENT` als Maßnahme, aber kein Versagensrisiko |
| **UV-bedingte Gesundheitsschädigungen** | Menschliche Gesundheit | Hoch — Beschattung von Spiel-, Bade- und Schulfreiflächen |
| **Allergische Reaktionen durch Aeroallergene** | Menschliche Gesundheit | Hoch — Baumartenwahl im öffentlichen Grün, Ambrosia-Bekämpfung |
| **Stress durch Schädlinge / Krankheiten (Wald)** | Wald- und Forstwirtschaft | Hoch — Kommunalwald ist in vielen Gemeinden bedeutender Flächen- und Haushaltsposten |
| **Nutzfunktion: Holzertrag** | Wald- und Forstwirtschaft | Hoch — direkter kommunaler Einnahmeausfall |
| Schiffbarkeit der Binnenschifffahrtsstraßen (Niedrigwasser) | Verkehr | Mittel — nur Hafen- und Anrainerkommunen |
| Beeinträchtigung des Warenverkehrs über Wasserstraßen (Inland) | Industrie und Gewerbe | Mittel — dito |
| Ausbreitung invasiver Arten | Biologische Vielfalt | Mittel — kommunale Grünflächen und Gewässerunterhaltung |

Aus den 23 „dringenden Handlungserfordernissen" (Tabelle 26) fehlen zusätzlich u. a. **Leistungseinbußen von Beschäftigten** (Industrie und Gewerbe; KAP2 hat die Maßnahme `HEAT_WORK_SCHEDULES`, aber nicht das Risiko), **Schäden durch Windwurf** (Wald) und **Nutzfunktion: Erholung** (Wald).

### 4.3 Weitere systematische Lücken

- **Handlungsfeld Tourismuswirtschaft: 0 von 5 abgedeckt.** Für Kur-, Küsten-, See- und Wintersportgemeinden ist der Tourismus die zentrale wirtschaftliche Betroffenheit. DAS 2024 führt das Handlungsfeld im Cluster Wirtschaft; `_MEASURE_KANG_MAP` kennt es nicht.
- **Schutzgut „kulturelles Erbe": 0 Risiken in KAP2**, während die KWRA 23 Klimawirkungen darauf bezieht (Kulturlandschaften, Landschaftsgärten, bauliche Kulturgüter). Kommunen sind untere Denkmalschutzbehörde — die Lücke ist inhaltlich wie vertrieblich teuer.
- **Nutztiere.** Die KWRA führt „Hitzestress bei und Leistung von Nutztieren" als eigene Klimawirkung. KAP2 kennt nur `EXPECTED_AGRICULTURAL_DAMAGE_EUR` (pflanzenbaulich parametriert). Das ist exakt die vom Product Owner vermutete Lücke „Schäden an Tieren".
- **Gegenrichtung: KAP2 führt Risiken ohne KWRA-Pendant** — `EXPECTED_ANNUAL_MENTAL_HEALTH`, `EXPECTED_CLIMATE_MIGRATION_COSTS_EUR`, `SOCIAL_INEQUALITY_AMPLIFICATION_RISK_INDEX`, `EXPECTED_ADMIN_OUTAGE_HOURS`. Das ist nicht automatisch falsch (psychische Gesundheit ist eine anerkannte Forschungslücke der KWRA), es muss aber als bewusste Erweiterung deklariert sein statt unmarkiert mitzulaufen.

---

## 5. Sechs Strukturvarianten

Jede Variante folgt derselben Gliederung, damit sie vergleichbar bleiben.

### 5.1 Variante A — Status quo reparieren

**These.** Der Katalog braucht keine neue Systematik, sondern die Behebung seiner offensichtlichen Defekte.

**Mechanik.** `group` bleibt fünfwertig. Hitzegetriebene Sachschadenrisiken wandern von `flood` nach `heat` (oder werden gefahrenanteilig zugeordnet). Kürzung auf 45 Risiken gemäß [ROADMAP.md](ROADMAP.md) §4. Nicht abgedeckte KWRA-Klimawirkungen werden in einer Verzichtsliste dokumentiert, statt unerwähnt zu bleiben. Doku-Zahlen werden korrigiert.

**Pro.** Geringster Aufwand, keine Migration bestehender `CellAssessment.data`-Strukturen, kein Frontend-Umbau (Radar behält seine fünf Achsen), sofort umsetzbar, kollidiert mit keiner anderen Variante.
**Contra.** Behebt Symptome, nicht die Ursache. Die Verzichtsliste ist eine Verteidigungslinie, kein Ordnungsprinzip — und sie wächst nach Abschnitt 4 auf 36 Einträge, was sie als Vertriebsargument unbrauchbar macht.
**Datenlage.** Unverändert; keine neuen Datenanforderungen.
**Konformität.** KAnG: unverändert schwach (keine herleitbare Betroffenheitsanalyse). KWRA: unverändert.
**Aufwand: S–M.** **Frontend/UX:** keiner.
**Befunde:** B1 ✔ · B8 ✔ · B2 teilweise (durch Streichung statt Ergänzung) · B3–B7 ✘.

> **Urteil: Notwendige Sofortmaßnahme, aber als Zielbild eine Absage an die Frage des Product Owners.**

### 5.2 Variante B — KWRA-2021-Systematik übernehmen

**These.** Wenn der Bund 102 Klimawirkungen in 13 Handlungsfeldern führt, ist das der maßgebliche Suchraum; KAP2-Risiken sind dessen quantifizierte Teilmenge.

**Mechanik.** Die 13 KWRA-Handlungsfelder werden Primärachse. Jedes KAP2-Risiko wird einer oder mehreren KWRA-Klimawirkungen zugeordnet (der Freitext in `pathway_curation.py` liefert die Vorarbeit). Die Abdeckungsmatrix aus Anhang A wird Produktbestandteil: jede Klimawirkung mit Status quantifiziert / nur Screening / kommunal nicht relevant.

**Pro.** Maximale Bundes-Konformität; jede Aufnahme und jede Lücke ist gegen eine amtliche Quelle belegbar. Die Lückenanalyse wird vom Problem zum Feature — genau die Aussage, die § 12 KAnG von einer Betroffenheitsanalyse verlangt. Erschließt zudem die KWRA-Dringlichkeitsstufen als fertige, zitierfähige Priorisierung.
**Contra.** 13 Achsen sind für die zentrale Visualisierung unbrauchbar (`RiskRadarSection.tsx` arbeitet mit 5). Mehrere Handlungsfelder sind für die Mehrzahl der Kommunen leer oder fast leer (Fischerei, Küsten- und Meeresschutz, Tourismuswirtschaft) — ein Radar mit strukturell leeren Achsen wirkt wie ein Produktfehler. Vor allem aber: **Handlungsfelder sind Wirkungs-, nicht Schadensraum.** Sie beantworten nicht, wen der Schaden trifft, und heilen B6 daher nicht.
**Datenlage.** Anspruchsvoll, aber ehrlich: Die Matrix darf Lücken ausweisen; sie zwingt nicht zur Bezifferung.
**Konformität.** KWRA: ++. KAnG: gut, aber indirekt (das Gesetz verweist auf Handlungserfordernisse, nicht auf Handlungsfelder).
**Aufwand: L.** **Frontend/UX:** tief — `LayerPanel.tsx`, `RiskRadarSection.tsx`, `RiskDistributionSection.tsx`, `types/index.ts`.
**Befunde:** B1 ✔ · B8 ✔ · B5 teilweise · B2/B3/B6/B7 ✘ · B4 unberührt.

> **Urteil: Das richtige Universum, aber die falsche Präsentationsachse — B liefert den Inhalt für E, nicht die Struktur.**

### 5.3 Variante C — KAnG-Handlungsfeld-Symmetrie

**These.** Risiken und Maßnahmen müssen dieselbe Sprache sprechen; die 7 Cluster / 17 Handlungsfelder existieren bereits im Code.

**Mechanik.** Risiken bekommen `kang_cluster` und `kang_field` analog zu `_MEASURE_KANG_MAP`. Die Layer- und Maßnahmennavigation läuft über eine gemeinsame Achse; der Dual-Einstieg im Anlegen-Dialog entfällt.

**Pro.** Schließt B7 vollständig und B2 strukturell: Eine Maßnahmen-Lücke wird sichtbar als Handlungsfeld mit Risiken, aber ohne Maßnahmen. Die Achse ist bereits implementiert, gesetzesnah (§ 3 Abs. 2 KAnG) und gegenüber Kommunen unmittelbar kommunizierbar, weil sie der Ressortlogik von Verwaltungen entspricht. Farb- und Cluster-Infrastruktur (`kangColors.ts`) ist vorhanden.
**Contra — das Kernargument.** Handlungsfelder beschreiben den **Akteursraum** („wer handelt"), nicht den **Schadensraum** („was wird getroffen"). Hitzemortalität gehört gleichzeitig zu Gesundheit, Stadtentwicklung und Bevölkerungsschutz. Als Primärachse erzwingt das entweder willkürliche Einfachzuordnung oder 1:n-Tagging — und ein 1:n-Tag ist per Definition nicht mutually exclusive. Die Variante löst die Symmetriefrage und verfehlt die MECE-Frage.
**Datenlage.** Unkritisch; reine Zuordnungsarbeit.
**Konformität.** KAnG: ++ (Maßnahmenseite), o (Risikoseite — das Gesetz verlangt es dort nicht). KWRA: o.
**Aufwand: M** als Tagging, **L** als Primärachsen-Umbau. **Frontend/UX:** mittel bis tief.
**Befunde:** B7 ✔ · B2 ✔ · B3 ✔ · B1 teilweise · B6 ✘ · B4/B5/B8 unberührt.

> **Urteil: Als Sekundär-Tag der Risiken unverzichtbar, als Primärachse methodisch nicht tragfähig.**

### 5.4 Variante D — Gefahr × Schutzgut-Matrix

**These.** Ein Risiko ist definiert durch die Kombination *welche Gefahr trifft welches Schutzgut mit welchem Schaden*. Diese Achse ist MECE per Konstruktion — und sie ist keine KAP2-Erfindung: Die KWRA arbeitet mit 4 Schutzgütern und 5 Systembereichen (Abschnitt 2.3), die ISO 14091 mit Rezeptoren.

**Mechanik.** Primärachse: Schutzgüter — **Menschen · Gebäude und Infrastruktur · Wirtschaft · Natur und Umwelt · Gesellschaft, Staat und kulturelles Erbe**. Sekundärachse: die bestehenden Gefahrentypen (heute `group`). Jedes Risiko ist genau eine Zelle und wird konsistent benannt: `<Gefahr>_<Schutzgut>_<Outcome>`. Die fünf Schutzgüter passen exakt auf die fünf vorhandenen Radar-Achsen.

**Pro.** Löst B6 an der Wurzel: Der Name eines Risikos sagt vollständig, was gerechnet wird. Löst B1 automatisch, weil Hitze × Sachwerte eine eigene Zelle ist und nicht mehr unter `flood` verschwinden kann. Deckt die Lücke „kulturelles Erbe" strukturell auf. Anschlussfähig an KWRA (Schutzgüter/Systembereiche), ISO 14091 (Rezeptoren) und BBK-Bevölkerungsschutz. Für die Kommunikation gegenüber Kommunen mindestens so gut wie die Gefahrenachse: „Was passiert mit unseren Menschen, unseren Gebäuden, unserer Wirtschaft, unserer Natur?" ist die Frage, die im Gemeinderat gestellt wird.
**Contra.** 5 Schutzgüter × ~8 Gefahrentypen ergeben bis zu 40 Zellen — Vollständigkeitsdruck ohne Datengrundlage, exakt die in Abschnitt 3.2 und in [MODELL_KRITIK.md](MODELL_KRITIK.md) §3 beschriebene Falle. Die 13 `compound`-Risiken passen in keine Einzelgefahr-Zelle und brauchen eine explizite Sonderbehandlung. Nahezu alle 51 Risikocodes müssten umbenannt werden, mit Migrationsbedarf in `CellAssessment.data`, `RiskZone.layer_code`, gespeicherten `impact_summary`-Blobs und allen Exporten.
**Datenlage.** Kritisch — als Alleinlösung datenblind.
**Konformität.** KWRA: + (Schutzgutachse ist KWRA-eigen, Handlungsfelder gehen verloren). KAnG: o.
**Aufwand: L–XL.** **Frontend/UX:** mittel (Radar-Achsen passen), aber tief in Persistenz und Exporten.
**Befunde:** B1 ✔ · B6 ✔ · B5 ✔ (Kanaltrennung macht Nicht-Monetarisierbarkeit sichtbar) · B2/B3 teilweise · B7 ✘.

> **Urteil: Die beste innere Logik im Feld — und als Alleinlösung die gefährlichste, weil ihre leeren Zellen zum Ausfüllen einladen.**

### 5.5 Variante E — Zwei-Ebenen-Modell (Screening + quantifizierter Kern)

**These.** Vollständigkeit und Quantifizierung sind zwei Anforderungen an zwei Ebenen, nicht an eine Liste.

**Mechanik.**
- **Ebene 1 — Screening (MECE).** Alle kommunal relevanten KWRA-Klimawirkungen (nach Anhang A: 87), qualitativ bzw. index-basiert bewertet, mit KWRA-Dringlichkeitsstufe. Kein €-Wert, kein Outcome. Die 11 heutigen `INDEX_ONLY_RISK_CODES` sind der natürliche Grundstock dieser Ebene und werden dadurch von einer Verlegenheit zu einer Kategorie.
- **Ebene 2 — Quantifizierter Kern.** Nur Risiken mit belastbarer Schadensfunktion und dokumentierten Parametern; € und Outcomes ausschließlich hier. Heutiger Stand: 26 Risiken mit Eintrag in `IMPACT_FUNCTIONS`.
- Jedes Kern-Risiko referenziert die Screening-Klimawirkung(en), die es quantifiziert. Das Dashboard weist beide Ebenen unmissverständlich getrennt aus.

**Pro.** Löst die Grundsatzfrage aus Abschnitt 3, statt sie zu vertagen. Strukturell deckungsgleich mit der bereits getroffenen Entscheidung in [MODELL_KRITIK.md](MODELL_KRITIK.md) §7 (Option C: Screening und Absolutwerte getrennt) — der Katalog vollzieht nach, was die Rechenlogik schon tut. Deckungsgleich auch mit der ROADMAP-Leitlinie „Vertrauen vor Umfang": Der Kern ist exakt das, was risikoweise validiert aufgebaut wird, die Screening-Ebene hält währenddessen den Konformitätsanspruch. **Entschärft B2 grundlegend:** Ein Risiko ohne Maßnahme ist kein Defekt mehr, wenn es als Screening-Befund deklariert ist — heute muss es entweder eine Proxy-Maßnahme bekommen (B3) oder gestrichen werden. Und der Vertriebseffekt ist erheblich: „Wir screenen alle 87 kommunal relevanten Klimawirkungen des Bundes und rechnen 26 davon monetär durch" ist eine stärkere Aussage als „wir haben 51 Risiken".
**Contra.** Zwei Ebenen wollen gepflegt werden, inklusive der Referenzen zwischen ihnen. Die UX muss die Ebenen sauber trennen, sonst wirkt Screening wie zweite Klasse — der schwierigste Teil der Variante liegt im Interface, nicht im Modell. Der Vollausbau des Kerns bleibt **XL**, allerdings ist dieser Aufwand in der ROADMAP ohnehin eingeplant.
**Datenlage.** Der einzige Ansatz, der die Datenlage nicht als Problem behandelt, sondern als Sortierkriterium.
**Konformität.** KWRA: ++. KAnG: ++ (Betroffenheitsanalyse und prioritäre Risiken werden direkt herleitbar).
**Aufwand:** Einstieg **M**, Vollausbau **XL** (bereits eingeplant). **Frontend/UX:** mittel — eine neue Ebenenunterscheidung, kein Achsenwechsel.
**Befunde:** B2 ✔ · B3 ✔ · B5 ✔ · B8 ✔ · B4 über den Kern-Rebuild ✔ · B1/B6/B7 abhängig von der gewählten Kern-Systematik.

> **Urteil: Das Zielbild — die einzige Variante, die die Spannung zwischen Vollständigkeit und Datenehrlichkeit auflöst statt sie zu verschieben.**

### 5.6 Variante F — Wirkungsdimensions-Matrix

**These.** Der Katalog soll nach Schadenskanälen sortiert sein — genau die Struktur, die der Product Owner beim Draufsehen erkannt hat.

**Mechanik.** Primärachse: **Mortalität · Morbidität · Sachschäden (€) · Betriebsunterbrechung (h) · Umwelt- und Naturschäden**. Sekundärachse: Gefahr. Das Feld existiert bereits als `cost_dimension` (health/monetary/operational/environment) und müsste nur um die Trennung Mortalität/Morbidität ergänzt und in der UI sichtbar gemacht werden.

**Pro.** Geringste Datenmigration aller Umbau-Varianten, weil die Achse schon im Katalog steckt. Saubere Aggregation ohne Einheitenmischung: Innerhalb eines Kanals sind Outcomes addierbar, über Kanäle hinweg nie — heute wird das im Radar durch Index-Mittelung verdeckt. Heilt B6 auf der Aggregationsebene und macht B5 sichtbar, weil nicht-monetarisierbare Risiken einen eigenen Kanal bekommen statt in der €-Summe zu fehlen.
**Contra.** Als Erstnavigation stakeholder-untauglich: Kommunen denken in Gefahren („Was macht die Hitze mit uns?") und Ressorts, nicht in Schadenskanälen. Der Umweltkanal bleibt intern heterogen (ha, Arten, Index). Und: MECE über die Kanäle heißt nicht erschöpfend über die Klimawirkungen — F sagt nichts darüber, ob ein Thema fehlt, und lässt damit den Hauptbefund aus Abschnitt 4 unberührt.
**Datenlage.** Unkritisch.
**Konformität.** KWRA/KAnG: o — keine der beiden Systematiken kennt diese Achse.
**Aufwand: M.** **Frontend/UX:** gering als zusätzliche Pivot-Sicht.
**Befunde:** B6 ✔ · B5 ✔ · B1 teilweise · B2/B3/B7 ✘ · B4/B8 unberührt.

> **Urteil: Starke Innenarchitektur des quantifizierten Kerns, keine taugliche Außentaxonomie.**

### 5.7 Die entscheidende Beobachtung: nur B und D konkurrieren

Die sechs Varianten sind keine Alternativen auf gleicher Ebene:

- **B** definiert den **Suchraum** (welche Themen gehören überhaupt hinein).
- **D** definiert die **Ordnung innerhalb des Suchraums** (wie ein Risiko geschnitten und benannt wird).
- **C** und **F** sind **Sekundärachsen** — Tags und Pivot-Sichten, die neben jeder Primärachse existieren können.
- **E** ist eine **Schichtung**, kein Achsenvorschlag: Sie sagt, welche Ebene MECE sein muss und welche quantifiziert.
- **A** ist eine **Zeitachsen-Entscheidung** — was sofort passiert, unabhängig vom Zielbild.

Echte Konkurrenz besteht daher nur zwischen B und D als Primärachse. Und die ist auflösbar: B liefert die Bezugsmenge für Ebene 1, D die Systematik für Ebene 2. **Das ist die Konstruktion, die Abschnitt 7 empfiehlt.**

---

## 6. Vergleich der Varianten

Bewertung `++` sehr gut · `+` gut · `o` neutral · `−` schwach · `−−` sehr schwach.

| Kriterium | A Reparatur | B KWRA | C KAnG | D Schutzgut | **E Zwei-Ebenen** | F Wirkungsdim. |
|---|---|---|---|---|---|---|
| MECE-Grad / Vollständigkeit | `−−` | `++` | `−` | `++` | `++` | `o` |
| KWRA-2021-Konformität | `−` | `++` | `o` | `+` | `++` | `o` |
| KAnG-/DAS-Anschlussfähigkeit | `o` | `+` | `++` | `o` | `++` | `−` |
| Datenlage / ehrliche Quantifizierbarkeit | `+` | `o` | `+` | `−−` | `++` | `+` |
| Löst Hitze-Schiefstand (B1) | `++` | `+` | `o` | `++` | `+` | `+` |
| Schließt Risiko↔Maßnahme-Lücke (B2/B3/B7) | `−` | `−` | `++` | `o` | `++` | `−` |
| Benennungs-/Semantikkonsistenz (B6) | `−−` | `o` | `−` | `++` | `+` | `++` |
| Deckt die 36 fehlenden Klimawirkungen auf | `−` | `++` | `−` | `+` | `++` | `−−` |
| Migrationsaufwand *(niedriger = besser)* | **S–M** | **L** | **M–L** | **L–XL** | **M → XL** | **M** |
| Frontend-/UX-Eingriffstiefe | keine | tief | mittel–tief | mittel | mittel | gering |
| Kompatibel mit ROADMAP + MODELL_KRITIK | `+` | `o` | `+` | `−` | `++` | `+` |
| Kommunizierbarkeit gegenüber Kommunen | `o` | `−` | `++` | `+` | `+` | `−` |

**Lesehilfe.** A gewinnt nur bei Aufwand und Sofortwirkung. B und D haben je eine Spitzenqualität und je eine harte Schwäche (Präsentierbarkeit bzw. Datenblindheit) — sie sind Bausteine, keine Lösungen. C und F sind ergänzend stark und als Primärachse schwach. **E ist die einzige Spalte ohne ein einziges `−`** und die einzige, die bei Datenlage und Vollständigkeit gleichzeitig `++` erreicht — weil sie diese beiden Anforderungen auf verschiedene Ebenen legt, statt sie gegeneinander zu optimieren. Ihre Schwächen liegen im Aufwand des Vollausbaus, und der ist über die ROADMAP bereits beschlossen.

---

## 7. Empfehlung: Variante E-stufig

Analog zur Hauspräzedenz „Option C-stufig" in [MODELL_KRITIK.md](MODELL_KRITIK.md) §7.

### 7.1 Zielbild

**Ebene 1 — Screening (MECE, aus Variante B).** Die 87 kommunal relevanten KWRA-Klimawirkungen als Bezugsmenge, gruppiert nach den 13 KWRA-Handlungsfeldern, angereichert um die KWRA-Dringlichkeitsstufe. Jede trägt einen Status: *quantifiziert* (Verweis auf ein Kern-Risiko) · *nur Screening* · *kommunal nicht relevant* mit Begründung.

**Ebene 2 — Quantifizierter Kern (Systematik aus Variante D).** Risiken werden als Zelle `Gefahr × Schutzgut × Outcome` geschnitten und konsistent benannt. Die fünf Schutzgüter bilden die Radar-Achsen und ersetzen dort die heutige Gefahrenachse — das behebt B1, ohne die Achsenzahl zu ändern. Aufnahme in den Kern nur bei belastbarer Schadensfunktion und dokumentierten Parametern.

**Sekundärachsen.** Jedes Risiko trägt zusätzlich `kang_field` (Variante C) — das schließt B7 und macht die Maßnahmenlücke pro Handlungsfeld messbar. `cost_dimension` bleibt als Pivot- und Aggregationssicht erhalten (Variante F) und wird um die Trennung Mortalität/Morbidität ergänzt.

**Was das für die Ausgangsfrage bedeutet:** MECE gilt strikt auf Ebene 1 (dort ist Vollständigkeit prüfbar und kostet keine erfundenen Zahlen) und als Ordnungsprinzip auf Ebene 2 (dort ist jede Zelle sauber definiert, muss aber nicht besetzt sein). Spezifische Picks bleiben erlaubt — sie heißen jetzt nur „Kern-Risiken" und ihre Auswahl ist begründet statt implizit.

### 7.2 Stufen

| Stufe | Inhalt | Aufwand | Bezug ROADMAP |
|---|---|---|---|
| **1 — sofort** | Variante A vollständig: Hitze-Umgruppierung, Kürzung auf 45, Doku-Zahlen korrigieren (B1, B8) | **S–M** | vor M1 |
| **2 — kurzfristig** | Anhang A als Datenstruktur in den Katalog; Screening-Ebene deklarieren (Index-Risiken dorthin); `kang_field` an alle Risiken (B2, B3, B5, B7) | **M** | M1–M2 |
| **3 — mittelfristig** | Die 10 fehlenden sehr dringenden Klimawirkungen priorisiert ergänzen — beginnend mit „Vegetation in Siedlungen", „Innenraumklima", „Hochwasserschutzsysteme" | **M–L** | M2–M3 |
| **4 — Zielbild** | Kern risikoweise validiert nach D-Systematik aufbauen und benennen (B4, B6) | **XL** | M3–M4 |

Stufe 1 ist unabhängig von der Entscheidung über das Zielbild sinnvoll und sollte nicht auf sie warten. Stufe 3 verschiebt die ROADMAP-Arithmetik: Das dortige Ziel „45 Risiken" entstand aus Fusionen ohne Gegenrechnung der Lücken. Nach Anhang A sind Ergänzungen nötig; die Zielzahl steigt voraussichtlich wieder in Richtung 50 — bei umgekehrtem Vorzeichen, weil sie dann herleitbar ist statt gewachsen.

### 7.3 Was ausdrücklich nicht empfohlen wird

Ein reiner Achsenwechsel — B oder C oder D allein — kostet einen tiefen Frontend- und Migrationseingriff und hinterlässt jeweils mindestens einen der acht Befunde unberührt. Wer nur eine Variante umsetzen kann, sollte A nehmen und die Struktur später angehen; wer die Struktur angeht, sollte nicht bei einer einzelnen Achse stehenbleiben.

---

## 8. Entscheidungsvorlage (Product Owner)

Bitte **eine** Option ankreuzen (Empfehlung markiert).

- [ ] **Option A — Nur reparieren.** Aufwand: **S–M**. Hitze-Umgruppierung, Kürzung auf 45, Doku-Korrektur, Verzichtsliste. Konsequenz: Der Katalog bleibt eine Sammlung spezifischer Picks mit besserer Frisur; die 36 fehlenden Klimawirkungen und 10 fehlenden sehr dringenden Handlungserfordernisse bleiben unadressiert. **Nur als Sofortmaßnahme empfohlen, nicht als Antwort.**

- [ ] **Option B — KWRA-Handlungsfelder als Primärachse.** Aufwand: **L**. 13 Handlungsfelder, 102 Klimawirkungen als Master. Konsequenz: maximale Bundes-Konformität und vollständige Lückentransparenz, aber Radar und Layer-Navigation müssen neu gedacht werden und mehrere Achsen bleiben bei den meisten Kommunen leer.

- [ ] **Option C — KAnG-Symmetrie als Primärachse.** Aufwand: **M–L**. Eine Taxonomie für Risiken und Maßnahmen. Konsequenz: Risiko↔Maßnahme-Lücke geschlossen und beste Kommunizierbarkeit, aber die Primärachse ist nicht überschneidungsfrei — die MECE-Frage bleibt offen.

- [ ] **Option D — Gefahr × Schutzgut-Matrix.** Aufwand: **L–XL**. MECE per Konstruktion, Umbenennung fast aller Risikocodes. Konsequenz: sauberste Systematik, aber ohne Ebenentrennung entsteht Druck, ~40 Zellen mit Zahlen zu füllen, für die die Datengrundlage fehlt — genau der Fehler, den MODELL_KRITIK §3 benennt.

- [X] **Option E-stufig — Zwei-Ebenen-Modell (EMPFOHLEN).** Aufwand: **S–M jetzt, M kurzfristig, XL im Zielbild** (letzteres bereits über die ROADMAP eingeplant). Screening-Ebene = kommunal relevantes KWRA-Universum (aus B); quantifizierter Kern nach Gefahr × Schutzgut (aus D); `kang_field` als Sekundär-Tag (aus C); `cost_dimension` als Pivot (aus F); Stufe 1 = Variante A. Konsequenz: vollständig und datenehrlich zugleich, KAnG-§-12-konform herleitbar, kein Bruch mit ROADMAP oder MODELL_KRITIK — und die Lückenanalyse wird vom Risiko zum Verkaufsargument.

- [ ] **Option F — Wirkungsdimensionen als Primärachse.** Aufwand: **M**. Schadenskanäle statt Gefahren. Konsequenz: sauberste Aggregation bei geringstem Migrationsaufwand, aber für Kommunen kein zugänglicher Einstieg und ohne jede Aussage darüber, ob Themen fehlen.

**Anschlussfrage, unabhängig von der Option:** Sollen die 10 fehlenden sehr dringenden Klimawirkungen aus Abschnitt 4.2 unabhängig von der Strukturentscheidung als eigener Arbeitsstrang priorisiert werden? Empfehlung: **ja** — sie sind der einzige Befund dieses Berichts mit direkter Außenwirkung auf den KAnG-Konformitätsanspruch aus [PRODUKTBESCHREIBUNG.md](PRODUKTBESCHREIBUNG.md) §1.

---

## Anhang A: Abdeckungsmatrix KWRA 2021 → KAP2

### A.0 Legende und Relevanzregel

| Status | Bedeutung |
|---|---|
| **abgedeckt** | Ein KAP2-Risiko bildet die Klimawirkung direkt und mit eigener Wirkungsfunktion ab |
| **teilweise** | Nur als Gefahr/Vulnerabilität vorhanden, nur index-basiert, oder ein KAP2-Risiko deckt nur einen Teilaspekt |
| **fehlt** | Kommunal relevant, im Katalog nicht vorhanden |
| **n. r.** | Kommunal nicht relevant |

**Relevanzregel für „n. r.":** nicht kommunal steuerbar *und* nicht kommunal bezifferbar — betrifft (a) rein vorgelagerte physikalische Klimawirkungen ohne Anpassungsoption (in der KWRA mit `*` markiert, z. B. Seegang, Gezeitendynamik), (b) international verortete Wirkungen (Absatzmärkte, internationaler Warentransport), (c) Chancen des Klimawandels (KWRA Tabelle 2). **Küstenthemen gelten ausdrücklich nicht pauschal als irrelevant** — KAP2 bedient Küstenkommunen; sie sind je nach Steuerbarkeit „teilweise" oder „fehlt".

Dringlichkeit: **SD** = sehr dringendes Handlungserfordernis (KWRA TB6, Tab. 25) · **D** = dringend (Tab. 26).

### A.1 Cluster Land

| # | KWRA-Klimawirkung | HF | Dringl. | KAP2-Risiko | Status |
|---:|---|---|---|---|---|
| 1 | Veränderung der Länge der Vegetationsperiode und Phänologie* | BioV | — | — | n. r. |
| 2 | Ausbreitung invasiver Arten | BioV | SD | — | **fehlt** |
| 3 | Verlust an genetischer Vielfalt | BioV | D | `EXPECTED_BIODIVERSITY_LOSS` | teilweise |
| 4 | Verschiebung von Arealen und Rückgang der Bestände | BioV | D | `EXPECTED_BIODIVERSITY_LOSS` | teilweise |
| 5 | Schäden an Küstenökosystemen | BioV | D | `EXPECTED_HABITAT_LOSS` | teilweise |
| 6 | Schäden an Gebirgsökosystemen | BioV | — | — | n. r. |
| 7 | Schäden an wassergebundenen Habitaten und Feuchtgebieten | BioV | SD | `EXPECTED_HABITAT_LOSS` | teilweise |
| 8 | Schäden an Wäldern | BioV | SD | `EXPECTED_VEGETATION_DAMAGE` | abgedeckt |
| 9 | Ökosystemleistungen | BioV | D | `EXPECTED_ECOSYSTEM_SERVICE_LOSS` | abgedeckt |
| 10 | Bodenerosion durch Wasser | Boden | SD | `EXPECTED_SOIL_DEGRADATION`, `EXPECTED_SOIL_LOSS_DEGRADATION_EUR` | abgedeckt |
| 11 | Bodenerosion durch Wind | Boden | SD | `EXPECTED_SOIL_DEGRADATION` | teilweise |
| 12 | Rutschungen und Muren | Boden | D | `EXPECTED_ANNUAL_INJURIES_LANDSLIDE` | teilweise |
| 13 | Wassermangel im Boden | Boden | SD | `HYDROLOGICAL_STRESS_RISK_INDEX` | teilweise |
| 14 | Sickerwasser* | Boden | — | — | n. r. |
| 15 | Vernässung* | Boden | — | — | **fehlt** |
| 16 | Bodenbiologie | Boden | — | — | **fehlt** |
| 17 | Bodenstoffhaushalt | Boden | — | — | **fehlt** |
| 18 | Bodenfunktionen: Filter- und Pufferfunktionen | Boden | — | — | **fehlt** |
| 19 | Produktionsfunktionen | Boden | SD | `EXPECTED_AGRICULTURAL_DAMAGE_EUR` | teilweise |
| 20 | Hitzestress bei und Leistung von Nutztieren | LaWi | — | — | **fehlt** |
| 21 | Abiotischer Stress (Pflanzen) | LaWi | SD | `EXPECTED_AGRICULTURAL_DAMAGE_EUR` | teilweise |
| 22 | Verschiebung von Anbaugebieten | LaWi | — | — | **fehlt** |
| 23 | Agrophänologische Phasen und Wachstumsperiode | LaWi | — | — | **fehlt** |
| 24 | Stress durch Schädlinge und Krankheiten (Pflanzen) | LaWi | — | — | **fehlt** |
| 25 | Ertragsausfälle | LaWi | SD | `EXPECTED_AGRICULTURAL_DAMAGE_EUR` | abgedeckt |
| 26 | Qualität der Ernteprodukte | LaWi | — | — | **fehlt** |
| 27 | Hitze- und Trockenstress | Wald | SD | `EXPECTED_VEGETATION_DAMAGE` | teilweise |
| 28 | Stress durch Schädlinge / Krankheiten | Wald | SD | — | **fehlt** |
| 29 | Schäden durch Windwurf | Wald | D | — | **fehlt** |
| 30 | Waldbrandrisiko | Wald | SD | `WILDFIRE` (Gefahr) → `EXPECTED_VEGETATION_DAMAGE` | teilweise |
| 31 | Nutzfunktion: Holzertrag | Wald | SD | — | **fehlt** |
| 32 | Nutzfunktion: Erholung | Wald | D | — | **fehlt** |

### A.2 Cluster Wasser

| # | KWRA-Klimawirkung | HF | Dringl. | KAP2-Risiko | Status |
|---:|---|---|---|---|---|
| 33 | Entkopplung von Nahrungsbeziehungen in der Ostsee | Fisch | D | — | n. r. |
| 34 | Verbreitung wärmeliebender Arten in der Nordsee | Fisch | — | — | n. r. |
| 35 | Verbreitung von Fischarten in Fließgewässern | Fisch | SD | `FISHERIES_STOCK_STRESS_RISK_INDEX` | abgedeckt |
| 36 | Stress durch Schädlinge/Krankheiten | Fisch | — | `FISHERIES_STOCK_STRESS_RISK_INDEX` | teilweise |
| 37 | Schäden an Aquakulturen | Fisch | — | `EXPECTED_AQUACULTURE_DAMAGE_EUR` | abgedeckt |
| 38 | Meerestemperatur und Eisbedeckung* | Küste | — | `OCEAN_WARMING` (Gefahr) | n. r. |
| 39 | Wasserqualität und Grundwasserversalzung | Küste | SD | `SALTWATER_INTRUSION` (Gefahr) | teilweise |
| 40 | Meeresspiegelhöhe* | Küste | — | `SEA_LEVEL_RISE` (Gefahr) | teilweise |
| 41 | Strömungen und Gezeitendynamik* | Küste | — | — | n. r. |
| 42 | Seegang* | Küste | — | — | n. r. |
| 43 | Sturmfluten* | Küste | — | `STORM_SURGE` (Gefahr) | teilweise |
| 44 | Naturräumliche Veränderungen an Küsten | Küste | SD | `COASTAL_EROSION` (Gefahr) | teilweise |
| 45 | Höhere Belastung oder Versagen von Küstenschutzsystemen | Küste | D | — | **fehlt** |
| 46 | Beschädigung/Zerstörung von Siedlung und Infrastruktur an der Küste | Küste | SD | `EXPECTED_BUILDING_DAMAGE_EUR` | teilweise |
| 47 | Überlastung der Entwässerungseinrichtungen in überflutungsgefährdeten Gebieten | Küste | SD | `EXPECTED_WASTEWATER_OUTAGE_HOURS` | teilweise |
| 48 | Niedrigwasser* | Wasser | — | `LOW_FLOW_NIEDRIGWASSER` (Gefahr) | teilweise |
| 49 | Hochwasser* | Wasser | — | `HEAVY_RAIN_FLOOD` (Gefahr) | teilweise |
| 50 | Belastung oder Versagen von Hochwasserschutzsystemen | Wasser | SD | — | **fehlt** |
| 51 | Sturzfluten (Versagen von Entwässerungs-/Überflutungsschutzsystemen) | Wasser | SD | `HYDROLOGICAL_STRESS_RISK_INDEX` | teilweise |
| 52 | Einschränkungen der Funktionsfähigkeit von Kanalnetzen, Vorflutern, Kläranlagen | Wasser | D | `EXPECTED_WASTEWATER_OUTAGE_HOURS` | abgedeckt |
| 53 | Gewässertemperatur, Eisbedeckung und biologische Wasserqualität | Wasser | SD | `SURFACE_WATER_HEATING` (Gefahr), `EXPECTED_WATER_AIR_POLLUTION` | teilweise |
| 54 | Chemische Wasserqualität | Wasser | D | `EXPECTED_WATER_AIR_POLLUTION` | teilweise |
| 55 | Grundwasserstand und Grundwasserqualität | Wasser | SD | `HYDROLOGICAL_STRESS_RISK_INDEX` | teilweise |
| 56 | Mangel an Bewässerungswasser | Wasser | D | `EXPECTED_AGRICULTURAL_DAMAGE_EUR` | teilweise |
| 57 | Trinkwasser | Wasser | — | `EXPECTED_WATER_SUPPLY_OUTAGE_HOURS` | abgedeckt |
| 58 | Produktionswasser | Wasser | — | `EXPECTED_SUPPLY_SHORTAGE_COSTS_EUR` (→ 0 €) | teilweise |

### A.3 Cluster Infrastruktur

| # | KWRA-Klimawirkung | HF | Dringl. | KAP2-Risiko | Status |
|---:|---|---|---|---|---|
| 59 | Schäden an Gebäuden aufgrund von Starkregen | Bau | D | `EXPECTED_BUILDING_DAMAGE_EUR` | abgedeckt |
| 60 | Schäden an Gebäuden aufgrund von Flusshochwasser | Bau | SD | `EXPECTED_BUILDING_DAMAGE_EUR` | abgedeckt |
| 61 | **Vegetation in Siedlungen** | Bau | SD | — *(Maßnahme `URBAN_GREEN` ohne Zielrisiko)* | **fehlt** |
| 62 | Stadtklima / Wärmeinseln | Bau | SD | `EXPECTED_THERMAL_STRESS_HOURS` | abgedeckt |
| 63 | **Innenraumklima** | Bau | SD | — | **fehlt** |
| 64 | Zeiten für Bautätigkeit | Bau | — | — | n. r. |
| 65 | Bedarf an Kühlenergie | Energie | — | — | **fehlt** |
| 66 | Bedarf an Heizenergie *(Chance)* | Energie | — | — | n. r. |
| 67 | Unterbrechung der regionalen Lieferketten für Energieträger | Energie | — | `EXPECTED_SUPPLY_CHAIN_DISRUPTION_HOURS` | teilweise |
| 68 | Mangelndes Kühlwasser für thermische Kraftwerke | Energie | — | — | **fehlt** |
| 69 | Ertragsminderung/-zunahme bei PV- und Windenergieanlagen | Energie | — | — | **fehlt** |
| 70 | Fehlende Zuverlässigkeit der Energieversorgung | Energie | — | `EXPECTED_ENERGY_OUTAGE_HOURS` | abgedeckt |
| 71 | Schiffbarkeit der Binnenschifffahrtsstraßen (Niedrigwasser) | Verkehr | SD | — | **fehlt** |
| 72 | Schiffbarkeit der Binnenschifffahrtsstraßen (Hochwasser) | Verkehr | — | — | **fehlt** |
| 73 | Schiffbarkeit der Seeschifffahrtsstraßen | Verkehr | — | — | n. r. |
| 74 | Schäden/Hindernisse bei Straßen und Schienenwegen (Hochwasser) | Verkehr | D | `EXPECTED_TRANSPORT_DAMAGE_EUR`, `EXPECTED_TRANSPORT_DISRUPTION_HOURS` | abgedeckt |
| 75 | Schäden/Hindernisse bei Straßen und Schienenwegen (gravitative Massenbewegungen) | Verkehr | D | `EXPECTED_TRANSPORT_DAMAGE_EUR` | teilweise |
| 76 | Schäden an Verkehrsleitsystemen, Oberleitungen, Stromversorgungsanlagen | Verkehr | D | `EXPECTED_ENERGY_INFRA_DAMAGE_EUR` | teilweise |
| 77 | Schäden an Binnen-/Seeschifffahrtsstraßen, Häfen, maritimen Infrastrukturen | Verkehr | — | — | **fehlt** |

### A.4 Cluster Wirtschaft

| # | KWRA-Klimawirkung | HF | Dringl. | KAP2-Risiko | Status |
|---:|---|---|---|---|---|
| 78 | Beeinträchtigung der Versorgung mit Rohstoffen/Zwischenprodukten (international) | IuG | D | `EXPECTED_SUPPLY_CHAIN_DISRUPTION_HOURS` | teilweise |
| 79 | Bedingungen auf Absatzmärkten (international) | IuG | — | — | n. r. |
| 80 | Wettbewerbsvorteil in innovativen Umwelttechnologien *(Chance)* | IuG | — | — | n. r. |
| 81 | Beeinträchtigung des internationalen Warentransports | IuG | D | — | n. r. |
| 82 | Beeinträchtigung des Warenverkehrs über Wasserstraßen (Inland) | IuG | SD | — | **fehlt** |
| 83 | Beeinträchtigung des landgestützten Warenverkehrs (Inland) | IuG | — | `EXPECTED_TRANSPORT_DISRUPTION_HOURS` | teilweise |
| 84 | Energieverbrauch und Beeinträchtigung bei der Energieversorgung | IuG | — | `EXPECTED_ENERGY_OUTAGE_HOURS` | teilweise |
| 85 | Wasserbedarf | IuG | D | `EXPECTED_WATER_SUPPLY_OUTAGE_HOURS` | teilweise |
| 86 | Freisetzung gefährlicher Stoffe | IuG | — | — | **fehlt** |
| 87 | **Leistungseinbußen von Beschäftigten** | IuG | D | — *(Maßnahme `HEAT_WORK_SCHEDULES` ohne Zielrisiko)* | **fehlt** |
| 88 | Beeinträchtigung von Produktionsprozessen | IuG | — | `EXPECTED_INDIRECT_ECONOMIC_LOSS_EUR` | teilweise |
| 89 | Aufwand für die betriebliche Planung | IuG | — | — | n. r. |
| 90 | Einschränkung touristischer Angebote: fehlende Schneesicherheit (Wintertourismus) | Tour | — | — | **fehlt** |
| 91 | Einschränkung touristischer Angebote: Hitze im Gesundheitstourismus | Tour | — | — | **fehlt** |
| 92 | Schäden an touristischen Infrastrukturen und Betriebsunterbrechungen | Tour | — | — | **fehlt** |
| 93 | Verlagerung der Nachfrage | Tour | — | — | **fehlt** |
| 94 | Wirtschaftliche Chancen und Risiken für die Tourismuswirtschaft | Tour | D | — | **fehlt** |

### A.5 Cluster Gesundheit

| # | KWRA-Klimawirkung | HF | Dringl. | KAP2-Risiko | Status |
|---:|---|---|---|---|---|
| 95 | Hitzebelastung | Gesundheit | SD | `EXPECTED_ANNUAL_MORTALITY`, `EXPECTED_ANNUAL_MORBIDITY`, `EXPECTED_THERMAL_STRESS_HOURS` | abgedeckt |
| 96 | Allergische Reaktionen durch Aeroallergene pflanzlicher Herkunft | Gesundheit | SD | — | **fehlt** |
| 97 | Potenziell schädliche Mikroorganismen und Algen | Gesundheit | — | — | **fehlt** |
| 98 | UV-bedingte Gesundheitsschädigungen (insb. Hautkrebs) | Gesundheit | SD | — | **fehlt** |
| 99 | Verbreitung und Abundanzveränderung von möglichen Vektoren | Gesundheit | — | — | **fehlt** |
| 100 | Atembeschwerden (aufgrund von Luftverunreinigungen) | Gesundheit | D | `EXPECTED_POLLUTANT_EXPOSURE_HOURS` | teilweise |
| 101 | Verletzungen und Todesfälle infolge von Extremereignissen | Gesundheit | — | `EXPECTED_ANNUAL_MORTALITY_FLOOD`, `..._STORM`, `EXPECTED_ANNUAL_INJURIES*` | abgedeckt |
| 102 | Auswirkungen auf das Gesundheitssystem | Gesundheit | D | `MEDICAL_UNDERSUPPLY_RISK_INDEX` | teilweise |

---

## Anhang B: Die 51 KAP2-Risiken im Zielbild

Zielebene: **Kern** = quantifizieren (Ebene 2) · **Screening** = Ebene 1, keine €/Outcome-Ausweisung · **prüfen** = Fusion oder Streichung gemäß ROADMAP §4 zu entscheiden.
Schutzgut (Variante D): **M** Menschen · **G/I** Gebäude und Infrastruktur · **W** Wirtschaft · **N** Natur und Umwelt · **S** Gesellschaft und Staat.

| KAP2-Risiko | heute `group` | Zielebene | Gefahr × Schutzgut | Befunde |
|---|---|---|---|---|
| `EXPECTED_ANNUAL_MORTALITY` | heat | Kern | Hitze × M | — |
| `EXPECTED_ANNUAL_MORBIDITY` | heat | Kern | Hitze × M | — |
| `EXPECTED_THERMAL_STRESS_HOURS` | heat | Kern | Hitze × M | B3 (Sammelbecken) |
| `EXPECTED_POLLUTANT_EXPOSURE_HOURS` | heat | Kern | Hitze × M | B2 |
| `EXPECTED_ANNUAL_MORTALITY_FLOOD` | flood | Kern | Flut × M | — |
| `EXPECTED_ANNUAL_MORTALITY_STORM` | flood | Kern | Sturm × M | — |
| `EXPECTED_ANNUAL_INJURIES` | flood | Kern | Flut × M | — |
| `EXPECTED_ANNUAL_INJURIES_STORM` | flood | Kern | Sturm × M | — |
| `EXPECTED_ANNUAL_INJURIES_LANDSLIDE` | flood | Kern | Hangrutsch × M | — |
| `EXPECTED_ANNUAL_AFFECTED_EVACUATED` | flood | Kern | Flut × M | — |
| `EXPECTED_ANNUAL_MENTAL_HEALTH` | compound | Kern | Verbund × M | B2; kein KWRA-Pendant |
| `EXPECTED_BUILDING_DAMAGE_EUR` | flood | Kern | **aufteilen** Flut/Hitze × G/I | **B1** |
| `EXPECTED_TRANSPORT_DAMAGE_EUR` | flood | Kern | **aufteilen** Flut/Hitze × G/I | **B1** |
| `EXPECTED_ENERGY_INFRA_DAMAGE_EUR` | flood | Kern | **aufteilen** Flut/Hitze × G/I | **B1** |
| `EXPECTED_TELECOM_DAMAGE_EUR` | flood | Kern | Flut × G/I | B2 |
| `EXPECTED_WATER_WASTEWATER_DAMAGE_EUR` | flood | Kern | Flut × G/I | B2 |
| `EXPECTED_AGRICULTURAL_DAMAGE_EUR` | drought | Kern | Trockenheit × W | Nutztiere ergänzen (A#20) |
| `EXPECTED_SOIL_LOSS_DEGRADATION_EUR` | drought | Kern | Trockenheit × N | B2 |
| `EXPECTED_ECOSYSTEM_SERVICE_LOSS` | gradual | Kern | Gradueller Wandel × N | B2 |
| `EXPECTED_FISHERIES_ECONOMIC_LOSS_EUR` | drought | Kern | Trockenheit × W | — |
| `EXPECTED_AQUACULTURE_DAMAGE_EUR` | drought | Kern | Trockenheit × W | — |
| `EXPECTED_CLIMATE_MIGRATION_COSTS_EUR` | compound | prüfen | Verbund × S | B2; kein KWRA-Pendant |
| `EXPECTED_INDIRECT_ECONOMIC_LOSS_EUR` | compound | Kern | Verbund × W | Aggregat, keine Zelle |
| `EXPECTED_RESTORATION_COSTS_EUR` | flood | Kern | Flut × G/I | B4; nicht additiv |
| `EXPECTED_SUPPLY_SHORTAGE_COSTS_EUR` | drought | prüfen | — | **B5** (0 €) |
| `EXPECTED_LOCATION_DISADVANTAGE_EUR` | compound | prüfen | — | **B5** (0 €), B2 |
| `EXPECTED_DELAYED_DAMAGE_COSTS_EUR` | compound | prüfen | — | **B5** (0 €), B2 |
| `EXPECTED_BIODIVERSITY_LOSS` | gradual | Kern | Gradueller Wandel × N | — |
| `EXPECTED_HABITAT_LOSS` | gradual | Kern | Gradueller Wandel × N | — |
| `EXPECTED_SOIL_DEGRADATION` | drought | Kern | Trockenheit × N | — |
| `EXPECTED_VEGETATION_DAMAGE` | drought | Kern | **aufteilen** Trockenheit/Waldbrand × N | A#27/#30 |
| `EXPECTED_CI_OUTAGE_HOURS` | compound | Screening | Verbund × G/I | **B4**, Aggregat |
| `EXPECTED_ENERGY_OUTAGE_HOURS` | compound | Kern | Verbund × G/I | **B4** |
| `EXPECTED_WATER_SUPPLY_OUTAGE_HOURS` | drought | Kern | Trockenheit × G/I | **B4** |
| `EXPECTED_WASTEWATER_OUTAGE_HOURS` | flood | Kern | Flut × G/I | **B4**, B2 |
| `EXPECTED_COMMUNICATION_OUTAGE_HOURS` | flood | Screening | Flut × G/I | **B4**, B2 |
| `EXPECTED_TRANSPORT_DISRUPTION_HOURS` | flood | Kern | Flut × G/I | **B4** |
| `EXPECTED_SUPPLY_CHAIN_DISRUPTION_HOURS` | compound | Screening | Verbund × W | **B4** |
| `EXPECTED_ADMIN_OUTAGE_HOURS` | compound | prüfen | Verbund × S | **B4**, B2; kein KWRA-Pendant |
| `EXPECTED_FUNCTIONAL_FAILURE_DURATION` | compound | prüfen | — | **B4**, B2; Dublette zu CI_OUTAGE |
| `HYDROLOGICAL_STRESS_RISK_INDEX` | drought | Screening | Trockenheit × N | **B4/B5**; deckt A#13/#51/#55 |
| `SYSTEMIC_DOMINO_RISK_INDEX` | compound | Screening | Verbund × S | **B4/B5** |
| `MEDICAL_UNDERSUPPLY_RISK_INDEX` | compound | Screening | Verbund × M | **B4/B5**, B2 |
| `SOCIAL_INEQUALITY_AMPLIFICATION_RISK_INDEX` | compound | Screening | Verbund × S | **B4/B5**; kein KWRA-Pendant |
| `EXPECTED_WATER_AIR_POLLUTION` | drought | Screening | Trockenheit × N | **B4/B5** |
| `ECOSYSTEM_DEGRADATION_RISK_INDEX` | gradual | Screening | Gradueller Wandel × N | **B4/B5**, B2 |
| `ECOSYSTEM_FRAGMENTATION_RISK_INDEX` | gradual | Screening | Gradueller Wandel × N | **B4/B5** |
| `ENVIRONMENTAL_FEEDBACK_RISK_INDEX` | gradual | prüfen | Gradueller Wandel × N | **B4/B5**, B2 |
| `RESOURCE_CONFLICT_RISK_INDEX` | drought | prüfen | Trockenheit × S | **B4/B5**, B2 |
| `FISHERIES_STOCK_STRESS_RISK_INDEX` | drought | Screening | Trockenheit × N | **B4/B5** |
| `LOW_WATER_FISHERIES_IMPACT_INDEX` | drought | Screening | Trockenheit × N | **B4/B5**; Dublette zu FISHERIES_STOCK_STRESS |

**Verteilung im Zielbild:** 31 Kern · 12 Screening · 8 zu prüfen. Die 12 Screening-Risiken sind exakt jene, die heute weder € noch belastbaren Outcome liefern — sie verschwinden nicht, sie bekommen die richtige Ebene.

---

## Quellen

| Schlüssel | Beleg |
|---|---|
| `UBA_KWRA_2021_TB6` | Umweltbundesamt (Hrsg.): *Klimawirkungs- und Risikoanalyse für Deutschland 2021 (Teilbericht 6): Integrierte Auswertung — Klimarisiken, Handlungserfordernisse und Forschungsbedarfe.* Climate Change 26/2021, Dessau-Roßlau, Juni 2021. — Tabelle 1 (102 Klimawirkungen mit Klimarisiken je Handlungsfeld und Systembereich), Tabelle 25 (31 sehr dringende Handlungserfordernisse), Tabelle 26 (23 dringende Handlungserfordernisse), Kap. 3.3 (Schutzgüter). [Publikationsseite](https://www.umweltbundesamt.de/publikationen/KWRA-Teil-6-Integrierte-Auswertung) |
| `UBA_KWRA_2021_KF` | Umweltbundesamt (Hrsg.): *Klimawirkungs- und Risikoanalyse für Deutschland 2021 — Kurzfassung.* Climate Change 26/2021, Dessau-Roßlau, Juni 2021. [Publikationsseite](https://www.umweltbundesamt.de/publikationen/KWRA-Zusammenfassung) |
| `UBA_KWRA_2021_TB1` | Umweltbundesamt (Hrsg.): *Klimawirkungs- und Risikoanalyse für Deutschland 2021 (Teilbericht 1): Grundlagen — Konzept und Methodik.* [Publikationsseite](https://www.umweltbundesamt.de/publikationen/KWRA-Teil-1-Grundlagen) |
| `KANG_2023` | *Bundes-Klimaanpassungsgesetz (KAnG)* vom 20. Dezember 2023, insb. §§ 3 Abs. 2, 5, 8, 10, 12. [gesetze-im-internet.de](https://www.gesetze-im-internet.de/kang/) |
| `DAS_2024` | Bundesregierung: *Deutsche Anpassungsstrategie an den Klimawandel 2024 (DAS 2024)* inkl. Anhang 1 „Ausführliche Clusterpapiere der Ressorts", Dezember 2024. |
| `ISO_14091` | DIN EN ISO 14091:2021 — *Anpassung an den Klimawandel: Leitlinien zu Vulnerabilität, Auswirkungen und Risikobewertung.* |
| `BBK_2015` | Bundesamt für Bevölkerungsschutz und Katastrophenhilfe: *Risikoanalyse im Bevölkerungsschutz*, 2015 — Herkunft der vier KWRA-Schutzgüter. |
