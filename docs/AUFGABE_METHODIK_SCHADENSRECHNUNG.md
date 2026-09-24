# Aufgabenbeschreibung: Methodik zur Schadensrechnung von Klimarisiken — v2 (konsolidiert)

Stand: 25.08.2026, fortgeschrieben bis 24.09.2026 · **Einzige Instruktionsquelle** für Herleitung, Review und
Integration von Risiko-Methodiken.

> **Fortschreibung 30.08.2026 (Nutzer-Entscheid, aus der #95-Integration):**
> (1) §3.4 **Ressourcen-Regel** — nationale 100-m-Vollraster-Läufe („Zell-Läufe")
> dürfen nie Prüf-, Abnahme- oder Abgleichvoraussetzung einer Methodik sein;
> (2) §3.1 **Datenebenen-Anlagepflicht** — fehlt eine benötigte Zellgröße im
> Produkt, spezifiziert der Bericht die neue Ebene vollständig und
> `/integriere-risiko` legt sie an (oder parkt sie mit Beschaffungs-Watchlist,
> wenn keine offene Quelle existiert).
>
> **Fortschreibung 31.08.2026 (Nutzer-Entscheid, aus der #96-Integration):**
> (3) §3.2 **Geschlossene Betrachtungsebene** — eine Referenz- oder
> Zentrierungsgröße darf **nie** aus einer modellinternen Aggregation über eine
> HÖHERE Ebene als die Betrachtungsebene stammen. Zulässig sind nur
> (a) amtlich/publiziert erhobene Referenzwerte (Mikrozensus, Pflegestatistik …)
> oder (b) Größen, die **innerhalb der Betrachtungsebene selbst** bestimmbar
> sind (bei einer Kommune: aus ihren eigenen Zellen). Liegt keine solche
> Referenz vor, bleibt der Modifikator neutral (Faktor 1) — ein „Bundeslauf"
> als Bezugsgröße ist unzulässig.
>
> **Fortschreibung 06.09.2026 (Aufsichtsrats-Entscheid, Freigabe F-0007; Vorgaben P1/P2 in
> `CLAUDE.md`):** (4) §3.5 — ein Maßnahmen-Hebel ohne publizierte Interventions-Effektgröße
> läuft **nicht mehr als „qualitativ“ mit Wirkung null**, sondern erhält eine **begründete
> Abschätzung** nach §3.9 „Abgeschätzt“ (Zahlenwert mit Begründung, Bandbreite, Sensitivität),
> die im Produkt ausdrücklich als „Abschätzung von KAP3“ mit Herleitung ausgewiesen wird.
> Bauform-Grenzen (z. B. kommunenweiter Pauschalfaktor statt zellscharfer Wirkung) werden als
> Modellgrenze der Abschätzung dokumentiert, nicht als Grund für eine Null. Bestehende Berichte,
> die einen Hebel als „qualitativ“ führen (#96 S158 Pollen-Frühwarnung, Log 15), werden über
> `/risiko-fortsetzen` als bewusste Überstimmung im Ledger fortgeschrieben.
> (5) §3.6 — die nutzersichtbare Parameterliste trägt je Parameter entweder die Quelle oder den
> Vermerk „Abschätzung von KAP3“ samt Herleitung; eine Herleitung, die nur als Code-Kommentar
> existiert, erfüllt die Pflicht nicht.
>
> **Fortschreibung 13.09.2026 (Anweisung des Aufsichtsrats A-0034; Vorgabe P3 in `CLAUDE.md`):**
> (6) neuer **§8 Erklärbarkeit** — die Methodik muss den Spagat zwischen rechnerisch korrekter
> Abschätzung und Nachvollziehbarkeit für Berater und kommunale Sachbearbeiter schaffen. Zu
> komplexe Verteilungsfunktionen und nicht lesbare Formeln sind ein Befund; die Belastbarkeit der
> Ergebnisse darf dabei nicht sinken. Geprüft wird über die Prüfpunkte E1–E4 (§8) im Rahmen von
> Leitfrage 11 (§5).
>
> **Fortschreibung 24.09.2026 (Aufsichtsrat; Vorgabe P3 in `CLAUDE.md` neu gefasst):** (7) **Eine Methodik je
> Risiko.** Am Ende steht genau eine Methodik — kein Nebeneinander einer einfachen und einer komplexen Fassung, kein
> Ansatz-Kapitel; verworfene Ansätze stehen mit je einem Satz im Entscheidungslog (§2.6, §3.7, §4). **So einfach wie
> möglich, so komplex wie nötig:** nie so einfach, dass das Ergebnis die Lage falsch darstellt; wo es nicht einfach geht,
> wird die Methodik komplexer und begründet an der Stelle, was die einfachere Rechnung verfälschen würde (§8 E3). Die
> bisherige Regel „beide Formen ausweisen“ entfällt. **Rechenkette:** Kapitel 3 jedes Berichts beginnt mit der
> durchgehenden Rechenkette von der amtlichen Quelle (etwa Zensus) bis zum Euro-Betrag — „Zahl aus Quelle × Faktor =
> Ergebnis“, möglichst in höchstens zehn Rechenebenen, je Ebene Quelle und Zahl für eine Beispielkommune, nachgerechnet
> von einem Beispiel-Block (§4, §8 E1). **Einheitliche Schreibweise** nach dem Stil-Skill `kap3-stil`, vom Lint geprüft
> (§7, §8 E5). **Rollen:** Die Methodik entsteht in der Rollenkette (CMO, Methodik-Manager plant und prüft,
> Methodik-Consultant arbeitet aus), integriert wird beim CTO; die Befehle heißen nach Rolle und Zweck (§6, §7). Alle
> Methodiken werden ab M0 (#95, #96, #98) neu angefasst; M1 beginnt erst nach der Abnahme von M0 durch den Aufsichtsrat.
>
> v2 konsolidiert die Aufgabenbeschreibung v1 (22.08.2026) und
`docs/METHODIK_GRUNDSAETZE.md` (G1–G14) **inklusive der Review-Fortschreibungen aus der
M0-Gegenprüfung** (Kalibrierfaktor-Regel ex G1/G5, G14-Geltungsbereich, G11-Begründung).
`METHODIK_GRUNDSAETZE.md` entfällt; die Datei bleibt nur als Ein-Zeilen-Verweis hierher bestehen.
Alte G-Referenzen (G1–G14) bleiben zitierfähig — das Mapping steht in §3.0.

---

## 1. Kontext (das Mindeste, was Autor und Prüfer wissen müssen)

**Produkt.** Ein webbasiertes Werkzeug, das für jede deutsche Kommune Klimarisiken auf dem
100-m-Raster (Destatis-INSPIRE-Gitter, EPSG:3035) bewertet und in Euro ausweist. Je Zelle liegen
vor: Zensus-2022-Bevölkerung mit Altersbändern und Haushaltsstruktur, OSM-Rohgrößen, Gelände/SVF,
DWD-Klimaraster (1 km) und eine Zelltemperatur mit mittelwerttreuem Stadtklima-Zuschlag.
Ausschließlich offene, keyless beschaffbare Datenquellen.

**Fachliche Grundlage.** KWRA 2021: 102 Klimawirkungen in 13 Handlungsfeldern (31 „sehr dringend",
23 „dringend"); Risiko = Hazard × Exposition × Vulnerabilität. Jede Klimawirkung läuft 1:1 unter
ihrem KWRA-Namen; Ausbau stufenweise (M0–M4).

**Verbindliche Quellen (Prüfgrundlagen-Bundle).** Ein Methodik-Bericht ist nur zusammen mit diesem
Bundle herleitbar und prüfbar:
1. `KWRA-Schadensbaum_X_UBA-klimawirkungsketten.xlsx` — knotenscharfe Wirkungsketten
   (E01–E25, S001–S161, R01–R36, W001–W198) + Netzwerkliste (Rollen, Kanten, Konten).
   **Diese Knoten sind die einzig zulässigen Eingangsgrößen — nicht mehr, nicht weniger.**
2. `KWRA-Monetarisierung.xlsx` — Schadenskonten K1–K8, Rollen (Treiber 0 € / vorgelagert /
   Zustandsgröße / Buchungsobjekt Ebene A/B), Bewertungsbausteine, Rechenregeln R1–R11,
   Abgleich-Protokoll (ergänzte Kanten).
3. Diese Aufgabenbeschreibung.
4. Die Anlagen des Berichts (Herleitungs-Skripte und Ergebnis-CSVs).

Weicht der Bericht bewusst von 1./2. ab (z. B. Bewertungslogik-Fortschreibung), wird die
**Quelle fortgeschrieben und die Änderung im Abgleich-Protokoll dokumentiert** — nie still
überstimmt (Lehre aus Befund 50 der M0-Prüfung).

**Kernformel je Endpunkt (Beweislastregel):**

> Kommunaler Klimaschaden = Σ über Endpunkte: Mengengerüst (exponierte Einheiten je Zelle)
> × physische Wirkungsfunktion (je Klimaszenario) × Kostensatz des Kontos

Menge × Rate × Preis — zwischen Klimasignal und Euro steht immer eine **physische Größe**
(Fälle, Lebensjahre, Tage, Hektar, kWh), die sich unabhängig gegen amtliche Statistik
plausibilisieren lässt. Das unterscheidet Schicht B von einem Kostentopf.

**Zwei Schichten.** Schicht A = Screening-Index (`100 · max(w·Ĥ·Ê·V̂)`, editierbare Normierung,
**nie** auf Euro-Pfaden — testseitig erzwungen). Schicht B = absolute Schadensfunktion mit fixen
Intensitätsgrenzen; Kommune = Summe der Zellen; genau **eine** native Ergebnisgröße je Risiko-Code
(weitere Ausweise als Teil-Ausweise unter der KWRA-Klammer). Jeder Koeffizient ist ein editierbarer
Registry-Parameter mit Pflicht-Quelle (Ratchet: Parameter ohne Quelle bricht den Build); jede
Quelle mit Zitat, URL, Archiv-Snapshot.

---

## 2. Die Aufgabe je Klimawirkung

Der Methodik-Bericht eines Risikos entsteht in dieser Reihenfolge — sie ist bewusst so gebaut,
dass jeder Schritt den nächsten prüfbar macht:

### 2.1 Wirkungskette und Knoten-Bilanz

Kette strikt aus der Schadensbaum-Arbeitsmappe übernehmen (Hazard, vorgelagerte Wirkungen,
Sensitivitäten, Exposition, KWRA-Indikatoren). Dazu **verpflichtend eine Knoten-Bilanz**:
jeder Knoten der Kette → rechnet in (Schicht A / Schicht B / Maßnahmen-Hebel / **bewusst inaktiv
mit Begründung**). Kein Knoten darf unadressiert bleiben; „bewusst inaktiv" ist zulässig
(z. B. Handlungsfeld-Vererbung der R-Faktoren, fehlende belastbare Effektgröße), aber es muss
dastehen. Konten-Einbettung und R9-Abgrenzung in **zwei getrennten Spalten**:
*Output-Kanten* (laut Netzwerkliste/Abgleich-Protokoll, mit Punkt-Nr. und ggf. Partitionsregel-Zitat)
und *Konto-Ausschlüsse / verwandte Buchungen* (laut Konten-Definition) — die beiden nicht mischen.

### 2.2 Evidenz-Register (Herzstück des Berichts)

**Vor** jeder Modellgleichung wird die Evidenzlage ausgearbeitet: je Zeile ein belegter
Zusammenhang zwischen einem Ketten-Knoten (bzw. dem Hazard) und dem Outcome. Spalten:

| Spalte | Inhalt |
|---|---|
| Register-ID | z. B. `95-S152-01` (Risiko–Knoten–laufend); zeilenweise referenzierbar |
| Knoten → Outcome | z. B. S152 Altersstruktur → Hitzemortalität |
| Effektgröße | Wert + Einheit + Band, exakt aus der Quelle (RR-Steigung, OR, %, €/Fall …) |
| Studientyp | Intervention / quasi-experimentell / Kohorte / Fall-Kontrolle / amtliche Statistik / Modellannahme |
| Quelle | Kurzzitat + Fundstelle (Tabelle/Abbildung/Seite) |
| Übertragbarkeit | DE-Bezug, Zeitraum, Setting; Einschränkungen ehrlich benennen |
| Datenlage je Zelle | welcher offene Datensatz liefert die Zellgröße (oder: nur Kreis/Region/Proxy) |
| **Entscheidung** | **Basiswert** / **Maßnahmen-Hebel** / **Sensitivitätsband** / **bewusst inaktiv** — mit Ein-Satz-Begründung |

Regeln: (a) **In Formeln dürfen nur Register-Zeilen mit Entscheidung „Basiswert" vorkommen** —
damit ist für jede Sensitivität sichtbar, *warum* sie wie eingeht; (b) Fall-Kontroll-Effektgrößen
sind nie Maßnahmen-Effektgrößen (nur Interventions-/quasi-experimentelle Evidenz, §3.5);
(c) das Register ist risikoübergreifend wiederverwendbar — ein Zusammenhang (z. B. Altersstruktur ×
Mortalität, Pflegeheim-Anteil, Außenberufe) wird einmal recherchiert und je Risiko nur ausgewählt;
(d) fehlt Evidenz für einen Ketten-Knoten, ist das eine Register-Zeile mit Entscheidung
„bewusst inaktiv" — keine stillen Lücken.

### 2.3 Modell (Schicht B und Schicht A)

Schicht-B-Formel als Menge × Rate × Preis auf Zellebene, **ausschließlich aus Register-Zeilen
und hergeleiteten Parametern** komponiert; Aggregation Zelle → Kommune; native Ergebnisgröße
deklarieren. Schicht-A-Index aus denselben Knoten. Formregeln in §3.2/§3.7.

### 2.4 Kalibrierung und Validierung

Nationaler Anker als ein Skalar, unabhängige Verteilungsprüfung, Sanity-Bänder — Details §3.4.
**Kalibrierlauf immer mit dem Produktionsmodell** (nicht mit einer Näherung; Lehre aus Befund 1).

### 2.5 Maßnahmen

Hebel nur an Ketten-Sensitivitäten; Effektgrößen aus dem Register (Interventionsevidenz);
Wirkungsort im Modell definieren (auf welche Größe, multiplikativ auf was); Doppelzählungs-Wächter
und R7-Weiche (§3.5).

### 2.6 Methodik-Familien — eine Methodik je Risiko

Risiken werden **Familien** zugeordnet (z. B. „K1-Gesundheit bottom-up" = #95/#96/#98-Muster;
„K3/K4-Ereignisschäden" = Eintrittswahrscheinlichkeit × Schadensfunktion × Bestand;
„K6-Ertragsmodelle"; „K8-Vorsorge-Weichen"). **Am Ende steht je Risiko genau eine Methodik**
(Fortschreibung 7, 24.09.2026). Die Methodenwahl wird im Entscheidungslog begründet — beim ersten
Risiko einer Familie oder bei fachlich strittiger Wahl anhand des Kriterienrasters aus §3.7 —, verworfene
Ansätze stehen dort mit je einem Satz Grund. Ein eigenes Ansatz-Kapitel und ein Nebeneinander mehrerer
Fassungen gibt es nicht. Folge-Risiken derselben Familie übernehmen das Familien-Template.
Verteilschlüssel-Ansätze („nationaler Topf × Anteil") sind per §3.1 generell ausgeschieden und
nur als Negativ-Beispiel zitierfähig. Zur Einordnung des Umfangs: Von den 102 Klimawirkungen sind
laut Netzwerkliste ~50 Treiber (0 €), ~10 rein vorgelagert/Zustandsgrößen — **Schicht-B-Methodiken
braucht es nur für die ~43 Buchungsobjekte**, in Familien gebündelt.

### 2.7 Dokumentationsform

So, dass ein fachlicher Reviewer **ohne Rückfragen** prüfen kann (§3.2 Formregeln, §4 Template).
Quellformat ist **Markdown im Repository** (`docs/methodik/<risiko>.md`); PDF ist nur generierter
Export für Menschen. Herleitungs-Skripte und Ergebnis-CSVs sind Anlagen des Berichts.

### 2.8 Automatische Entscheidungen im Autor-Lauf (Gates)

> **Lücken-Vermerk (26.08.2026):** Dieser Abschnitt existierte nicht und wurde mit Gate 1 und
> der Prüfregel neu angelegt. Die von `/risiko-auto` und dem Subagenten `methodik-reviewer`
> zusätzlich referenzierten Inhalte — ✅/⚠️-Klassifikation, E-Regeln/Standardregeln, ggf.
> weitere Gates — fehlen noch und sind nachzutragen.

**Gate 1 — Entscheidungslog statt blockierender Vorlage:** Ermessensfälle (⚠️) werden mit der
Empfehlung sofort entschieden und angewendet und im Bericht in einem Entscheidungslog
dokumentiert (Frage · angewendete Entscheidung · Alternative · Überstimmungsweg). Der Nutzer
kann jederzeit nachträglich überstimmen; das löst einen Delta-Lauf aus (Neurechnung betroffener
Kopplungen plus Re-Review). Die Pipeline wartet nicht auf Freigabe.

**Prüfregel:** ⚠️-Entscheidungen werden auf Plausibilität der angewendeten Empfehlung geprüft,
nicht gegen eine menschliche Freigabe.

---

## 3. Anforderungskatalog (konsolidiert — enthält die früheren G1–G14)

### 3.0 Mapping alter G-Referenzen

G1 → 3.1/3.2 (Bottom-up, ein Kalibrier-Skalar) · G2 → 3.2 (YLL × VOLY) · G3 → 3.2 (Struktur) ·
G4 → 3.2 + 2.2 (nur belegte Sensitivitäten, via Register) · G5 → 3.2/3.4 (messen statt setzen;
Kalibrierfaktor-Regel) · G6 → 3.6 (Ebenen/Raten) · G7 → 3.2 (Form) · G8 → 3.6 (UI-Abgrenzungen) ·
G9 → 3.2 (Zentrierung/OR) · G10 → 3.5 (Interventionsevidenz) · G11 → 3.2 (Tails) ·
G12 → 3.4 (Verteilungsprüfung) · G13 → 3.2 (Kein-Doppelkanal) · G14 → 3.9 (Herleitungspflicht).

### 3.1 Eingangsgrößen

- Jede Größe trägt: Schadensbaum-Knoten, Datenquelle, Auflösung, Beschaffungsweg (offen, keyless),
  Kennzeichnung „vorhanden / neu anzulegen / geparkt"; Proxies als Proxies (auch: Durchschnitts-
  Kostensätze für spezifische Fallmixe).
- **Datenebenen-Anlagepflicht (Fortschreibung 30.08.2026):** Braucht eine Formel eine
  Zellgröße, die das Produkt nicht führt, spezifiziert der Bericht die neue Datenebene
  **vollständig** (Quelle, Beschaffungsweg keyless, Zell-Ableitungsregel, Fallback,
  Normierung/Zentrierung) und kennzeichnet sie „neu anzulegen" — die Integration (Skill `cto-integration`)
  **legt sie an**; ein dauerhafter Neutral-Fallback ohne spezifizierte Ebene ist
  unzulässig. Existiert nachweislich keine offene Quelle, wird die Ebene als
  „**geparkt** (Datenquelle fehlt)" mit Beschaffungs-Watchlist geführt und der
  Parameter läuft dokumentiert auf dem Zentrierungs-Neutralwert (Bundesmittel ⇒
  Faktor 1) — nie still.
- **Bottom-up-Grundsatz:** Bundes-/Landesstatistik wird **nie** zur räumlichen Verteilung benutzt.
  Lackmustest: *Eine Kommune ohne lokalen Treiber muss ~0 erhalten* (keine Flussaue → keine
  Flutopfer, kein Hitzesignal → keine Hitzetoten).

### 3.2 Verrechnung auf Zellebene

- **Form:** vollständige Formeln (LaTeX); je Formel eine alphabetisch sortierte
  Formelzeichen-Tabelle (Zeichen · Name · Einheit · Wert/Herkunft mit Register-ID oder
  Herleitungs-Anker); Abkürzungen bei Erstnutzung; jede Summe/Verteilung in Klartext, wo hilfreich
  mit Mini-Rechenbeispiel — **jedes Beispiel wird als ausführbarer Golden-Test hinterlegt** (§7).
- Lokale Treiber bestimmen den Zellwert; physische Zwischengröße vor jedem Euro (Kernformel §1).
- Struktur (Alter u. a.) überall, wo die zitierte Evidenz strukturabhängig ist; nicht geschichtete
  Elastizitäten als explizite Annahme („gleiche relative Elastizität über alle Bänder") mit Band.
- **Mortalität als YLL × VOLY** (UBA-MK-4.0-Logik); VSL nur Sensitivität. Konsequenz benennen:
  YLL ist bei altenlastigen Risiken ~Faktor 5–10 konservativer — die Relation zwischen Risiken
  verschiebt sich (Infokasten, §3.6). Konsistenz-Check: VSL ÷ VOLY ≈ plausible Lebensjahre, beide
  aus derselben Quelle mit derselben Anpassung.
- Sensitivitäten **nur über das Evidenz-Register** (§2.2) in den Absolutwert; unbelegte
  Modulatoren Default = 1. Schwache Effekte ehrlich als schwach kennzeichnen. **Bandzuordnung:**
  jeder Modifikator wirkt nur in den Alters-/Strukturbändern und auf die Endpunkte
  (Mortalität/Morbidität getrennt!), für die seine Evidenz gilt.
- **Alle Modifikatoren mittelwertzentriert** (Referenzmittel = 1, `1 + β·(x − x̄)`), sonst wird
  der Kalibrierfaktor uninterpretierbar. Individuelle Odds-Ratios über das Bevölkerungsmittel
  übersetzen: `β = (OR−1) / [1 + q̄·(OR−1)]`. Zentrierungs-Mittelwerte (q̄, d̄) sind
  herleitungspflichtige Parameter (3.9).
- **Geschlossene Betrachtungsebene (Fortschreibung 31.08.2026).** Das Zentrierungsmittel
  ist entweder ein **amtlich publizierter** Wert (z. B. Mikrozensus-Anteil allein lebender
  65-Jähriger, Pflegequote) — dann trägt es die individuelle Evidenz und darf die Kommunen
  gegeneinander verschieben — oder es wird **innerhalb der Betrachtungsebene selbst**
  gebildet (Kommune: gewichtetes Mittel über ihre eigenen Zellen). **Unzulässig ist eine
  modellinterne Aggregation über eine höhere Ebene** (etwa ein bundesweiter Zell-Lauf als
  Bezugswert für eine Zellgröße): Sie verletzt die Ressourcen-Regel (§3.4) und macht das
  Ergebnis einer Kommune von Daten abhängig, die außerhalb ihrer Betrachtungsebene liegen.
  Welcher der beiden Wege gilt, entscheidet die **Reichweite der Evidenz**: intra-urban
  gemessene Effekte (z. B. Vegetations-/Pollengradienten innerhalb einer Stadt) zentrieren
  auf die Kommune; individuell erhobene Risikoverhältnisse (Fall-Kontroll-/Kohorten-ORs)
  zentrieren auf das publizierte Bevölkerungsmittel. Fehlt eine zulässige Referenz, bleibt
  der Modifikator **neutral** (Faktor 1) — keine Ersatzkonstruktion.
  Fortschreibungs-Regel bei innerhalb der Ebene gebildeten Mitteln: Der Referenzzustand
  wird im **Baseline-Lauf** bestimmt und für Maßnahmen-/Szenariorechnungen festgehalten,
  sonst neutralisiert eine mitlaufende Rezentrierung flächige Maßnahmen per Konstruktion.
- **Kein-Doppelkanal:** jede physikalische Wirkung genau einmal (Grünanteil steckt im
  Stadtklima-Zuschlag — nicht zusätzlich als Vulnerabilität); vor Aufnahme jedes Faktors prüfen,
  ob er implizit schon in einem Eingang steckt.
- **Tails:** wo wenige Extremwochen/-ereignisse den Effekt tragen, empirische Quantile aus der
  Klimatologie statt Verteilungsannahmen; **intra-saisonale**, nicht zwischenjährliche Streuung.
  Empirischer Stand (M0, 21 DWD-Stationen): Bei Sommer-Wochenmitteln ist die Anomalieverteilung
  praktisch symmetrisch — der maßgebliche Fehler gesetzter Verteilungen war die zu kleine Streuung,
  nicht die Schiefe; bei Tages-/Ereignisgrößen bleibt Rechtsschiefe relevant. Die Regel
  (empirische Quantile) vermeidet beide Fehler zugleich. Modellgrenze dokumentieren: klimatologische
  Quantile bilden das *mittlere* Jahr ab; Extremjahre mit Hitzewellen bei moderatem Mittel werden
  strukturell unterschätzt.
- Parameter messen statt setzen; **regional variieren dürfen nur physikalische/gemessene
  Modellparameter** (Streuungen, Schwellen, Steigungen, Übersetzungsfaktoren) — Kalibrierfaktoren
  nicht (3.4).
- Zeitbezug sauber: Jahreswerte, Szenariojahre (ein Absatz „Szenario-Anwendung": verschobene Größe,
  konstante Größen, Stationaritätsannahmen), Latenzen explizit.

### 3.3 Konten-Disziplin

- Genau ein Konto je Endpunkt; R9-Partition nach Ursachen mit **Zitat der Partitionsregel** aus
  der Monetarisierungs-Arbeitsmappe, wo zwei Buchungsobjekte dasselbe Konto teilen.
- Vorgelagerte Wirkungen 0 € (R2); Vermeidungs- vs. Schadenskosten nie beide je Einheit (R7 —
  bei Maßnahmen, die Vorsorgeobjekte berühren, die R7-Weiche ausdrücklich referenzieren).
- Kostensätze mit **Preisstand** und Quelle; alle Kostensätze eines Berichts auf einen
  gemeinsamen Preisstand indexiert (Umrechnungsfaktor je Satz in der Zeichentabelle);
  Konservativität („nur Konto Kx aktiv") benennen.

### 3.4 Kalibrierung und Validierung

- **Kalibrierfaktor-Regel (präzisiert):** Der nationale Anker geht als **ein einziger
  Niveau-Skalar** auf die Deutschland-Summe ein (Kleinste Quadrate Anker ÷ Modellsumme über die
  Anker-Zeitreihe; einheitliche Jahres-Auswahlregel, Sensitivitäten je Zeitfenster). Zeigt die
  Verteilungsprüfung regionale Schieflagen, wird die **Wirkungsfunktion regional nachgeschätzt** —
  nicht die Kalibrierung regionalisiert. Regionale Kalibrierfaktoren sind allenfalls eine
  dokumentierte, befristete Übergangslösung mit Fortschreibungsvermerk und Ablaufdatum.
- **Kalibriermodell = Produktionsmodell.** Faktoren aus Näherungsläufen (gröbere Auflösung, ohne
  Teilmodelle) sind unzulässig, sobald das Produktionsmodell konvexe Wirkungsfunktionen oder
  bevölkerungsgewichtete Exposition hat — sonst brennt der Näherungsfehler ins Produkt ein.
- **Ressourcen-Regel (Fortschreibung 30.08.2026):** Kalibrierung, Validierung und jeder
  Abgleich müssen **ohne nationalen 100-m-Vollraster-Lauf** auskommen — ein solcher
  „Zell-Lauf" darf in keiner Methodik als Prüfstein, Abnahmevoraussetzung oder
  „finaler Abgleich" geplant werden (Rechenressourcen; das Produkt rechnet Zellen je
  Kommune on-demand). Zulässige Auflösungen für Kalibrier-/Prüfläufe: Bundesland-,
  Gemeinde-/Gemeindepunkt- und **kommunale Stichproben**-Ebene (ausgewählte Kommunen
  mit dem Produktionsmodell, z. B. dokumentierte Anker-Kommunen). Restfehler unterhalb
  der Kalibrier-Auflösung werden quantifiziert abgeschätzt und als dokumentierte
  Näherung geführt (§3.9), nicht auf einen Vollraster-Lauf vertagt.
- Anker-Zeitreihe mit Revisionsstand; laufende/vorläufige Jahre gesondert (nicht ins
  Kalibrier-Mittel); Sensitivität ohne vorläufige Werte ausweisen.
- **Kalibrierung ist kein Verteilungsnachweis:** mindestens eine unabhängige Prüfung auf der
  kritischsten Achse (Alters-/Strukturverteilung **mit Ist-Ergebnis und vorab fixierter Toleranz**;
  urbane und ländliche Anker bei stadtklima-getriebenen Modellen; Ereignisregime bei Flut).
  Prüfdaten dürfen nicht dieselben sein, auf denen Faktoren gefittet wurden (Holdout/Leave-one-out).
- Sanity-Bänder mit Unter- **und** Obergrenze aus amtlicher Statistik (oder begründete Ausnahme).

### 3.5 Maßnahmen

- Hebel nur an Ketten-Sensitivitäten; Effektgrößen aus Interventions-/quasi-experimentellen
  Studien (Fall-Kontroll-ORs messen nicht die Wirkung einer Einführung — regelmäßig Faktor 5–10
  zu optimistisch); marginal gegenüber dem heutigen Stand; **Doppelzählungs-Wächter** gegen die
  Kalibrierjahre; **Wirkungsort definieren** (z. B. multiplikativ auf den Exzess (RR−1), nicht
  vage „auf β"); R7-Weiche referenzieren, wo einschlägig.
- **Hebel ohne quantifizierte Effektgröße (Vorgabe P2, 06.09.2026):** nicht als „qualitativ" mit
  Wirkung null führen, sondern eine begründete Abschätzung nach §3.9 „Abgeschätzt" erarbeiten
  (Zahlenwert mit Begründung, Bandbreite, Ergebnis-Sensitivität) und im Produkt als „Abschätzung
  von KAP3" mit Herleitung ausweisen. Die Abschätzung ist marginal und an eine Ketten-Sensitivität
  gebunden wie jeder andere Hebel; Bauform-Grenzen werden als Modellgrenze der Abschätzung
  dokumentiert. Wo der Bericht das Fehlen einer Effektgröße feststellt, ist das der Anlass für die
  Abschätzung, nicht ihr Ersatz.

### 3.6 Architektur- und Produktkonformität

- Screening-Normierung nie auf Euro-Pfaden; fixe Intensitätsgrenzen in Schicht B; eine native
  Ergebnisgröße je Risiko-Code (deklariert; weitere als Teil-Ausweise).
- Schlüsselgrößen als Kartenebenen; Ergebnisse als lesbare **Raten (je 1.000 EW / je ha)** plus
  aggregierte Ebene (Quartier/Gemeindeteil) — Rohwerte je 100-m-Zelle sind unlesbar.
- UI-Abgrenzungen fest verdrahtet, nicht disclaimt: (1) Benennung nach Geltungsbereich
  („bewerteter Schaden — Konto Kx", nie „Gesamtschaden"), (2) Vollständigkeitsanzeige
  („Stufe M0: 1 von 8 Konten aktiv" + Roadmap-Aufklappliste), (3) Versionsstempel
  („berechnet mit Modellstand Mx — Untergrenze"). Infokasten-Texte sind Teil des Berichts.
- Jeder Parameter editierbar und bequellt (Ratchet); neue Datenquellen keyless.
- **Nutzersichtbare Parameterliste (Vorgabe P1, 06.09.2026):** je Parameter steht dort entweder
  die Quelle oder der Vermerk „Abschätzung von KAP3" samt Herleitung, wie der Wert zustande kommt.
  Gilt für alle Parameter, auch Defaults, Kostensätze und Wirkungsfaktoren; eine Herleitung nur
  als Code-Kommentar genügt nicht.

### 3.7 Methodenwahl (Entscheidungslog, nach §2.6)

Festes Kriterienraster für die Wahl: kausale Treue · Kalibrierbarkeit · lokale Differenzierung ·
Datenverfügbarkeit · Maßnahmen-Anschluss · Architektur-Konformität · Erklärbarkeit (§8) · Aufwand. Die Wahl
steht mit Begründung im Entscheidungslog; jeder verworfene Ansatz mit einem Satz Grund. Kein Ansatz-Kapitel,
keine zweite Fassung im Bericht.

### 3.8 Quellen

Jede Zahl mit Quelle (Autor, Jahr, Titel, Organ, DOI/URL, Zugriffsdatum, Archiv-Snapshot);
Sekundärfunde **vor** Übernahme im Volltext verifizieren (zitierte Effektzahlen gegenlesen);
Widersprüche zwischen Quellen benennen, nicht glätten; Datenlücken ausdrücklich als Lücken.

### 3.9 Herleitungspflicht für jeden Parameter

Jeder Parameter einer Formel ist im Bericht vollständig hergeleitet:
- **Übernommen:** exakte Fundstelle, Originalwert mit Einheit und Preis-/Bezugsjahr, jede
  Umrechnung als Rechenschritt.
- **Abgeleitet:** komplette Rechenkette mit allen Zwischenwerten (OR → Zellsteigung,
  Altersverteilung → Altersfaktoren, Messreihe → Übersetzungsfaktor) — reproduzierbar. Hängt eine
  Ableitung von anderen Parametern ab (z. B. Altersfaktoren von Basissterberaten), wird die
  **Kopplung benannt** und bei Änderung der Basis neu gerechnet.
- **Gemessen:** Datensatz, Zeitraum, Region, Aggregationsregel, Ergebniswerte, Skript-/CSV-Pfad.
- **Abgeschätzt:** nur wenn keine Quelle existiert — mit Begründung des Zahlenwerts, Bandbreite,
  Ergebnis-Sensitivität, Produkt-Kennzeichnung als Annahme. Keine Kategorienfehler
  (ein Korrelationskoeffizient ist kein Anteil; ein Querschnittsverhältnis keine Kohorten-Rate —
  Approximationen als solche kennzeichnen).
- **Unzulässig:** Platzhalter, „wird bei Implementierung hergeleitet", Werte nur in der
  Zeichentabelle ohne Weg im Text. Gilt auch für Defaults, Bandgrenzen, Referenzwerte,
  Zentrierungs-Mittelwerte und Kostensätze.
- **Geltungsbereich:** vollständig für die eine Methodik des Berichts. Verworfene Ansätze im
  Entscheidungslog brauchen keine Herleitung; wird einer später doch gewählt, gilt die Pflicht vor der
  Implementierung vollständig.

Fertig-Regel: Jede Zeile jeder Zeichentabelle referenziert in „Wert/Herkunft" eine abgeschlossene
Herleitung (Register-ID oder Herleitungs-Anker) — kein Verweis auf später.

---

## 4. Berichtsstruktur je Risiko (Template)

```
docs/methodik/<nn>_<risiko>.md
1  Wirkungskette & Knoten-Bilanz          (§2.1; Weitergaben zweispaltig)
2  Evidenz-Register                        (§2.2; Register-IDs, Entscheidungsspalte)
3  Modell                                  (§2.3; beginnt mit 3.0 Rechenkette, dann Formeln + Zeichentabellen + Beispiele)
4  Kalibrierung & Validierung              (§2.4/§3.4; Skripte/CSVs als Anlage verlinkt)
5  Maßnahmen-Hebel                         (§2.5/§3.5)
6  Szenario-Anwendung & Modellgrenzen      (§3.2; inkl. Infokasten-Texte §3.6)
7  Parameter-Blöcke                        (maschinenlesbar, s. u.)
8  Quellen                                 (§3.8)
Entscheidungslog                           (Methodenwahl §3.7, verworfene Ansätze je ein Satz; kein Kapitel 9)
```

**Rechenkette (Abschnitt 3.0, Pflicht; §8 E1).** Kapitel 3 beginnt mit `### 3.0 Rechenkette` — dem durchgehenden
Rechenweg von der amtlichen Quelle bis zum Euro-Betrag, so, dass ein Sachbearbeiter ihn in einem Meeting erzählen kann:

```
| Ebene | Rechenschritt | Wert (Beispielkommune <Name>) | Quelle |
|---|---|---|---|
| 1 | Einwohner ab 75 Jahren | 12.400 | Zensus 2022, Tabelle … |
| 2 | × zusätzliche Sterbefälle je 1.000 Einwohner und Hitzewoche | × 0,21 | Evidenz-Register 95-S152-01 |
| … | … | … | … |
| n | = bewerteter Schaden (Konto K1) je Jahr | = 1,2 Mio. € | Rechnung |
```

Je Ebene ein Rechenschritt in Worten („Zahl aus Quelle × Faktor = Ergebnis“), die Zahl für die Beispielkommune und die
Quelle (Datensatz, Register-ID oder „Rechnung“ für abgeleitete Ebenen). Höchstens zehn Ebenen; mehr nur mit einer Zeile
`**Mehr als zehn Ebenen:** <Begründung, was eine kürzere Kette an der Lage verfälschen würde>`. Die letzte Ebene ist der
Euro-Betrag. Darunter rechnet ein Beispiel-Block (`python test: rechenkette_<nr>`) die Kette nach. Die Formeln danach sind
die genaue Fassung derselben Kette, keine zweite Methodik.

**Parameter-Block-Format** (wird per Skript in die Produkt-Registry extrahiert; der Ratchet-Test
prüft Herkunft maschinell):

```yaml
parameter:
  id: heat.beta_iso
  wert: 0.86
  einheit: "-"
  band: [0.3, 1.4]
  herkunft: register:95-S152-02        # oder herleitung:#beta-iso
  quelle: semenza1996
  preisstand: null                     # Pflichtfeld bei Kostensätzen
  bandzuordnung: [65-74, 75-84, 85+]
  endpunkt: mortalitaet                # mortalitaet | morbiditaet | beide
  kennzeichnung: quelle                # quelle | abschaetzung_kap3 | berechnet
  abgeleitet_aus: []                   # bei kennzeichnung: berechnet Pflicht — Liste der Parameter-IDs, aus denen der Wert folgt
  rolle: kalibrierung                  # optional: kalibrierung | pruefgroesse | sensitivitaet | waechter
```

Felder `kennzeichnung`, `abgeleitet_aus`, `rolle`:

- `kennzeichnung` (Pflicht) hat genau drei Werte: `quelle | abschaetzung_kap3 | berechnet`. `quelle`: der Wert steht
  in einer benannten Quelle. `abschaetzung_kap3`: begründete Abschätzung von KAP3 mit Herleitung (P1). `berechnet`:
  der Wert folgt rechnerisch aus anderen Parametern.
- `abgeleitet_aus` nennt bei `berechnet` die Parameter-IDs, aus denen der Wert entsteht; sonst leer.
- `rolle` ist optional und sagt, wozu ein Parameter dient: `kalibrierung | pruefgroesse | sensitivitaet | waechter`.
  Fehlt das Feld, ist es ein gewöhnlicher Rechenparameter.

**Beispiel-Blöcke** sind ausführbar markiert (```python test: …```) und werden als Golden-Tests
in die CI übernommen — Bericht und Code können nicht auseinanderlaufen.

---

## 5. Prüfauftrag für die Gegenprüfung

**Vorbedingung:** Das vollständige Prüfgrundlagen-Bundle (§1) liegt der Review-Session ab dem
ersten Turn vor — Bericht, diese Aufgabe, beide Arbeitsmappen, Anlagen. Ein Review ohne
vollständiges Bundle ist ungültig (Lehre aus der M0-Prüfung: nachgereichte Quellen erzeugten
zwei Extra-Durchgänge).

**Ablauf:** Zuerst die deterministischen Lint-Ergebnisse übernehmen (§7 — nicht manuell
nachprüfen, was die Maschine prüft), dann die Leitfragen **einzeln mit Verdikt und Beleg**
beantworten (nicht „nichts weiter gefunden", sondern je Frage: bestanden/Befund + Begründung):

1. **Kette:** Alle Knoten in Knoten-Bilanz und Formeln verarbeitet oder begründet inaktiv?
   Eingänge, die nirgends rechnen? **Direkt gegen die Arbeitsmappe abgleichen, nicht gegen die
   Behauptungen des Berichts.**
2. **Verteilschlüssel-Test:** Kommune ohne Treiber > 0 möglich?
3. **Physische Zwischengröße:** Euro je Zelle auf physische Größe rückführbar (auch native
   Ausweise proportional zu den Euro-Pfaden)?
4. **Doppelzählung:** Zwei Kanäle? Zwei Konten? Maßnahmeneffekt schon im Basiswert?
   Referenzwerte doppeln Baseline-Anteile (HD_ref-Klasse)?
5. **Modifikatoren:** zentriert, OR-Übersetzung korrekt, richtige Studienart, **richtige Band-
   und Endpunkt-Zuordnung**?
6. **Struktur:** überall verwendet, wo die Evidenz strukturabhängig ist; Kopplungen zwischen
   abgeleiteten Parametern neu gerechnet?
7. **Tails/Parameter:** Verteilungsannahmen, wo empirische Quantile verfügbar wären; gesetzte
   Werte, die messbar wären; Kalibriermodell = Produktionsmodell?
8. **Kalibrierung:** ein Skalar; Revisionsstand; unabhängige Verteilungsprüfung mit
   Ist-Ergebnis, out-of-sample?
9. **Kostensätze:** Preisstand einheitlich, Quellen, VSL/VOLY-Konsistenz, Konto-Zuordnung?
10. **Quellen:** fehlend, veraltet, falsch zugeordnet, unverifiziert; Zahlen ≠ Primärquelle?
11. **Form und Erklärbarkeit:** Zeichentabellen vollständig; Beispiele rechnen auf (Golden-Tests
    grün)? **Prüfpunkte E1–E5 aus §8 einzeln mit ja/nein und Fundstelle** — insbesondere E1 (Rechenkette
    vollständig, je Ebene Quelle und Zahl, höchstens zehn Ebenen oder begründet) und E3: eine Vereinfachung,
    die die Lage falsch darstellt, ist ein Befund; ebenso Komplexität ohne Begründung der Fehldarstellung und
    ein Nebeneinander zweier Fassungen.
12. **Umsetzbarkeit:** Daten offen/keyless; Parameter-Blöcke vollständig; Architektur-vereinbar;
    benötigte neue Ebenen als solche gekennzeichnet (inkl. Struktur-Ebenen wie u18)?
13. **Herleitungspflicht:** ein einziges Formelzeichen ohne abgeschlossene Herleitung = Befund.
14. **Quellen-Synchronität:** Widerspricht der Bericht den Arbeitsmappen oder dieser Aufgabe in
    einem verbindlichen Punkt (Bewertungslogik, Kanten, Konten, Rollen)? Jede bewusste
    Fortschreibung in der Quelle nachgezogen und im Abgleich-Protokoll dokumentiert?

**Ergebnisformat:** nummerierte Befunde (Stelle · Art: Lücke/Fehler/Widerspruch · Begründung ·
Vorschlag · Kategorie A/B/C) — fortlaufend in das Befund-Ledger `reviews/BEFUNDE_<risiko>.md`
(eine Tabelle: Befund · Status · Umsetzungsnachweis · Begründung bei Abweichung). „Abweichend
gelöst" nur mit erfüllter Anforderung; Anforderungsänderungen nur per Fortschreibung dieses
Dokuments. Zurückgestellte A-Befunde blockieren die Abnahme.

---

## 6. Prozess: Herleitung → Review → Revision → Abnahme

**Rollen = getrennte Sessions** (dieselbe Session, die schreibt, reviewt nicht — Selbst-Review
ist blind für die eigenen Annahmen):

| Schritt | Werkzeug | Input | Output |
|---|---|---|---|
| **Erstaufschlag** | `methodik_consultant` (Skill `methodik_consultant-erstaufschlag`) | Template §4, Bundle §1, Familien-Template | `docs/methodik/<risiko>.md` + Skripte/CSVs; Lints lokal grün |
| **Review** | `methodik_manager`, Prüflauf in frischer Sitzung (Skill `methodik_manager-gegenpruefung`) | Bundle + Bericht + Ledger | Befunde (Format §5) — im Urteil des Prüflaufs, der Consultant trägt sie ins Ledger ein |
| **Revision** | `methodik_consultant`, eine Runde je Lauf | Ledger | aktualisierter Bericht + Statusspalte je Befund; Rechenläufe neu, wo Kopplungen betroffen |
| **Re-Review** | frische Session | Diff + Ledger | nur: geänderte Abschnitte, Regression geschlossener Befunde, offene Befunde; **volle Prüfung erneut**, wenn Kalibrierung oder Modellstruktur geändert wurde |
| **Abnahme** | `methodik_manager` (Skill `methodik_manager-abnahme`), Übergabe durch den `cmo` | Abnahmekriterien | Freigabe zur Integration beim `cto` (Skill `cto-integration`); die Abnahme einer Stufe (M0, M1 …) legt der `cmo` dem Aufsichtsrat vor |

**Konvergenzkriterium („Review tatsächlich abgeschlossen"):** nicht Gefühl, sondern vier Bedingungen —
1. alle deterministischen Lints grün (§7);
2. alle 14 Leitfragen mit explizitem Verdikt beantwortet;
3. **Null-Runde:** eine frische Review-Session über das vollständige Bundle findet keine neuen
   A-/B-Befunde;
4. Abnahmekriterien erfüllt: alle A-Befunde geschlossen (B geschlossen oder terminiert
   zurückgestellt); Kalibrier-Prüfstein bestanden (Produktionsmodell, Verteilungsprüfung im
   vorab fixierten Band, out-of-sample); Struktur-Validierung im vorab fixierten Toleranzband;
   Sanity-Bänder eingehalten; Quellen-Synchronität (LF 14); Infokasten-/UI-Texte vorhanden.
   Prüfsteine, die scheitern, eskalieren in einen Modellentscheid — Toleranzen werden nicht
   nachträglich geweitet.

**PDF** wird erst nach Abnahme aus dem Markdown generiert (Export, kein Arbeitsformat).

---

## 7. Integration und Automatisierung (One-Person-Setup)

Ziel: Der teure LLM-Review prüft nur, was Urteilskraft braucht; alles Mechanische prüft die CI.

**Deterministische Lints** (Skript, läuft lokal und in CI; deckt erfahrungsgemäß ~⅓ typischer
Befunde ab):
- Jede Zeichentabellen-Zeile hat Wert **und** Herkunft (Register-ID/Anker) — kein „später".
- Jeder Formel-Parameter existiert als Parameter-Block; jeder Block hat Quelle, Kostensätze haben
  Preisstand; Bandzuordnung/Endpunkt gesetzt.
- Jede Quelle hat DOI/URL + Archiv-Snapshot (Ratchet, existiert bereits — erweitern).
- **Knoten-Abgleich gegen die Arbeitsmappe:** Skript liest die xlsx und prüft, dass jeder Knoten
  des Risikos in der Knoten-Bilanz vorkommt und jede behauptete Kante existiert (LF 1/14
  maschinell).
- Beispiel-Blöcke ausführbar und grün (Golden-Tests).
- Preisstand-Einheitlichkeit je Bericht.
- **Rechenkette** (Fortschreibung 7): `### 3.0 Rechenkette` am Anfang von Kapitel 3, Tabelle mit Wert und Quelle je
  Ebene, fortlaufende Ebenen, letzte Ebene in €, höchstens zehn Ebenen oder die Begründungszeile, Beispiel-Block darunter.
- **Zahlenformat** nach `kap3-stil`: Beträge ab einer Million als „Mio. €“/„Mrd. €“, Währung als `€`, Leerzeichen vor `%`.
- **Kein Kapitel 9** (Ansatz-Vergleich): verworfene Ansätze stehen im Entscheidungslog.

**CI-Tests aus dem Bericht:**
- Mini-Rechenbeispiele → pytest (Bericht ⇄ Code können nicht divergieren).
- Sanity-Anker → Test „Bundessumme ∈ [Untergrenze, Obergrenze]".
- Verteilungs-/Struktur-Validierung → Test mit vorab fixierter Toleranz.
- Kalibrier-Pipeline als reproduzierbares Skript (Daten-Pins), nicht als Einmal-Lauf.

**Claude-Code-Bausteine** (Skills unter `.claude/skills/`, benannt nach der Rolle, die sie einsetzt, und dem Zweck):
- `methodik_consultant-erstaufschlag <nn>` (früher `/neu-risiko`): instanziiert Template §4 mit der Rechenkette, zieht
  Knoten + Kanten + Konto automatisch aus den Arbeitsmappen in Abschnitt 1, legt Register-Skelett mit einer Zeile je Knoten
  an (Entscheidung „offen").
- `methodik_manager-gegenpruefung <nn>` (früher `/review-methodik`): führt Lints aus, arbeitet dann §5 ab.
- `methodik_manager-abnahme <nn>` (früher `/manager-review`): fachliche Abnahme nach der Null-Runde.
- `methodik_consultant-export <nn>` (früher `/export-pdf`): PDF, Wirkungsmechanismus-HTML, Übersicht
  `docs/methodik/README.md`.
- `cto-integration <nn>` (früher `/integriere-risiko`): extrahiert Parameter-Blöcke in die Registry, implementiert die
  Schicht-B-Funktion gegen die Registry, generiert die Tests aus Beispielen und Sanity-Ankern, legt Kartenebenen an.
- `kap3-stil`: Schreibweise für alle Rollen.
- Einzelsitzungs-Weg des Aufsichtsrats: `aufsichtsrat-risiko-auto`, `aufsichtsrat-risiko-fortsetzen`.
- Wiederverwendbares **Evidenz-Register-Repository** (`docs/evidenz/register.md` oder CSV):
  risikoübergreifende Zeilen einmal pflegen, je Risiko referenzieren.

**Reihenfolge des Ausbaus:** (1) M0-Bericht auf dieses Format migrieren (er ist der
Familien-Prototyp „K1-Gesundheit bottom-up" — die Migration erzeugt Lints, Registry-Extraktion
und die ersten Golden-Tests als Nebenprodukt), (2) Lints + Commands bauen, (3) erst dann das
nächste Risiko — ab dann kostet ein Familien-Folgerisiko einen Bruchteil des M0-Aufwands.

---

## 8. Erklärbarkeit

**Vorgabe P3 — Erklärbarkeit der Methodik.** Herkunft: **Anweisung des Aufsichtsrats A-0034 vom
13.09.2026** (Firmen-Repo `firma`, `gedaechtnis/aufsichtsrat/regeln.jsonl`). Sie geht den
Methodik-Regeln vor; ein Widerspruch zu einer bestehenden Regel oder einem abgenommenen Bericht
wird als **bewusste Überstimmung im Befund-Ledger** geführt (in der Rollenkette als neue Runde, im Einzelsitzungs-Weg
`/aufsichtsrat-risiko-fortsetzen <nr>`), nie still
im Code gelöst und nie als Grund, die Vorgabe nicht umzusetzen. (Aufgabe §2.7, §3.6, §3.9; Prüfung
über Leitfrage 11 in §5.)

**Adressat.** Ein Berater eines Beratungshauses, das Klimaanpassungskonzepte schreibt, oder ein
Sachbearbeiter einer Kommune: fachkundig in Sache und Verwaltung, aber ohne Statistikausbildung —
er muss den Rechenweg und jede verwendete Formel ohne Statistiklehrbuch nachvollziehen und
gegenüber Dritten vertreten können.

**Prüfpunkte (E1–E5).** Jeder ist mit ja oder nein zu beantworten und benennt seine Fundstelle im
Bericht; ein „nein" ist ein Befund nach §5 (Kategorie B, sofern nicht zugleich ein A-Kriterium
verletzt ist).

- **E1 — Rechenkette.** Beginnt Abschnitt 3 mit der durchgehenden Rechenkette von der amtlichen Quelle bis zum
  Euro-Betrag (Format §4): je Ebene ein Rechenschritt in Worten, die Zahl für die Beispielkommune und die Quelle,
  höchstens zehn Ebenen (mehr nur begründet), vom Beispiel-Block nachgerechnet — so, dass ein Sachbearbeiter sie in
  einem Meeting erzählen kann, ohne dass ein Schritt fehlt? *Fundstelle: Bericht Abschnitt 3.0.*
- **E2 — Rechenbeispiel mit Zahlen.** Trägt jede Hauptformel ein Beispiel mit eingesetzten Zahlen
  und allen Zwischenwerten (ausführbarer Beispiel-Block nach §4)? *Fundstelle: Beispiel-Blöcke in
  Bericht Abschnitt 3.*
- **E3 — So einfach wie möglich, so komplex wie nötig.** Wird eine **Verteilungsfunktion** (z. B.
  Extremwert-, Log-Normal- oder Poisson-Annahme, Faltung, Integral, Quantilfunktion) oder eine **Formel**
  verwendet, die der Adressat nach der Definition oben nicht nachvollziehen kann: steht an derselben Stelle,
  **was die einfachere Rechnung an der Lage verfälschen würde** (Richtung und Größe der Verzerrung, beziffert),
  und ein **Rechenbeispiel mit Zahlen**? Fehlt die Begründung, ist das ein Befund. Umgekehrt ist eine Vereinfachung
  ein Befund, wenn sie die Lage falsch darstellt — die Richtung eines Effekts, die Rangfolge der Kommunen oder die
  Größenordnung des Ergebnisses. Ein Nebeneinander einer einfachen und einer belastbaren Fassung ist ebenfalls ein
  Befund. *Fundstelle: Bericht Abschnitt 3 an der betreffenden Formel, ggf. Abschnitt 6 (Modellgrenzen) und
  Entscheidungslog.*
- **E4 — Zeichen und Begriffe.** Hat jedes Formelzeichen in der Zeichentabelle eine Bedeutung in
  Klartext samt Einheit, und ist jeder statistische Fachbegriff bei erster Verwendung in einem Satz
  erklärt (z. B. Odds Ratio, Zentrierung, out-of-sample)? *Fundstelle: Zeichentabellen in Abschnitt
  3, Parameter-Blöcke in Abschnitt 7.*
- **E5 — Einheitliche Schreibweise.** Folgen Zahlen, Beträge und Einheiten dem Stil-Skill `kap3-stil` (etwa
  „1,2 Mio. €“, Leerzeichen vor `%`)? Maschinell geprüft (§7); im Review nur übernehmen. *Fundstelle: Lint-Ausgabe.*

**Eine Methodik — so einfach wie möglich, so komplex wie nötig** (Fortschreibung 7, 24.09.2026). Am Ende steht je
Risiko genau eine Methodik; ein Nebeneinander einer einfachen und einer belastbaren Fassung gibt es nicht, verworfene
Varianten stehen mit je einem Satz im Entscheidungslog. Die Methodik darf nie so einfach werden, dass das Ergebnis die
Lage falsch darstellt: Eine Verteilungsannahme, ein Modifikator oder eine Kalibrierstufe wird nicht weggelassen, weil sie
schwer zu erklären ist. Wo es wirklich nicht einfach geht, wird die Methodik komplexer — und sagt an der Stelle, was die
einfachere Rechnung verfälschen würde (E3). Die Rechenkette (E1) hält auch eine komplexe Methodik erzählbar. **Still zu
vereinfachen ist unzulässig** und im Review ein Befund, genauso wie eine unerklärt stehengelassene Formel.

## Vorrang zwischen den UBA-Digitalisaten

Widersprechen sich die Arbeitsmappen `KWRA-Schadensbaum_X_UBA-klimawirkungsketten.xlsx` und `KWRA-2021_Klimawirkungen.xlsx`, gilt für jedes Risiko die Schadensbaum-Mappe. Risikostufen ohne Anpassung, Gewissheit, Anpassungsdauer, Wirksamkeit der Anpassung und Restrisiko stehen nur in der KWRA-2021-Mappe und werden von dort übernommen.

**Begründung aus dem Charakter der beiden Dokumente.** Die Knoten der Wirkungskette stammen in
beiden Mappen aus denselben UBA-Zeichnungen von 2016 (Klimawirkungsketten). Die beiden Mappen sind
aber für verschiedene Zwecke gebaut:

- *Schadensbaum-Mappe — die Knotenliste des Bundles.* Sie ist Quelle 1 des
  Prüfgrundlagen-Bundles (diese Aufgabe, §1, Zeilen 66–68: „Diese Knoten sind die einzig
  zulässigen Eingangsgrößen — nicht mehr, nicht weniger."). Jeder Pfeil der Zeichnung ist dort
  eine eigene Kennung: Blatt `Klimawirkungsketten`, Zeile 1, Spalten E bis H tragen die
  Kopfzellen `Input_IDs_Einflüsse`, `Input_IDs_Sensitivitäten`, `Input_IDs_Räumlich` und
  `Input_IDs_Wirkung`; Spalte Q (Kopf `Anmerkung`) hält je Zeile fest, von welchem Pfeil der
  Zeichnung der Eintrag abgelesen ist.
- *KWRA-2021-Mappe — die Bewertungstabelle.* Sie liegt nicht im Bundle, sondern unter
  `docs/KWAR/`, und ist nach eigener Angabe eine Aufbereitung der Teilberichte der KWRA 2021:
  Blatt `Lesehinweise`, Zelle A2:

  `Vollständig aufbereitet aus allen sechs Teilberichten der Klimawirkungs- und Risikoanalyse 2021 (Umweltbundesamt).`

  Belastbar ist sie für die Bewertungen
  im Blatt `Klimawirkungen` (Zeile 2, Kopfzellen der Spalten N bis AF: Risiko ohne Anpassung,
  Gewissheit, Anpassungsdauer, Wirksamkeit, Restrisiko). Ihr Blatt `Wirkungsmechanismen` dagegen
  ist nach seiner Zeile 2 selbst nur eine zweite Abschrift der Zeichnung und nicht Teil der
  KWRA-Bewertung. Zelle A2 dieses Blatts lautet vollständig:

  `Quelle: UBA (2016), Klimawirkungsketten — visuell aus den Diagrammen abgelesen. NICHT Teil der KWRA-2021-Bewertung. Namensstand der Vulnerabilitätsanalyse 2015, auf die KWRA-2021-Klimawirkungen abgebildet. Die Exposition ist in der Quelle nur je Handlungsfeld definiert, nicht je Klimawirkung. Zuordnungsebene „Container" heißt: Der Pfeil zeigt auf das Themenfeld und gilt für alle Klimawirkungen darin.`

Ein Widerspruch entsteht deshalb praktisch nur bei den Knoten der Wirkungskette (Einflüsse,
Sensitivitäten, räumliches Vorkommen, vorgelagerte Wirkungen). Dort ist die Schadensbaum-Mappe die
genauere und die verbindliche Abschrift. Die Bewertungen gibt es nur in der KWRA-2021-Mappe, dort
kann nichts widersprechen. Was außerhalb der Wirkungskette in beiden Mappen steht, stimmt überein
(Abgleich vom 22.09.2026).
Die Namen der 102 Klimawirkungen sind gleich (Schadensbaum-Mappe: Blatt
`Schadensbaum-Netzwerkliste`, Spalte B; KWRA-2021-Mappe: Blatt `Klimawirkungen`, Spalte D). Auch
das Handlungserfordernis ist gleich (Schadensbaum-Mappe: dasselbe Blatt, Spalte E, Kopf
`Handlungserfordernis (KWRA)`; KWRA-2021-Mappe: Blatt `Klimawirkungen`, Spalte AG).

**Vermerkpflicht.** Jede Anwendung dieser Regel wird im Befund-Ledger `reviews/BEFUNDE_<nr>.md` des
betroffenen Risikos mit beiden Fundstellen (Datei, Blatt, Zeile, Spalte) und dem Ergebnis
festgehalten.

**Beispielfall #62 — Stadtklima / Wärmeinseln.** Der Widerspruch betrifft die
Sensitivitätsfaktoren.

| | Fundstelle | Wortlaut der Zelle |
|---|---|---|
| Schadensbaum-Mappe | `docs/Schadensbaum/KWRA-Schadensbaum_X_UBA-klimawirkungsketten.xlsx`, Blatt `Klimawirkungsketten`, Zeile 279 (Knoten `W124`), Spalte J (Kopfzelle J1: `Input_Namen_Sensitivitäten`) | `Verwendete Baumaterialien auf Gebäudeebene; Begrünung von Gebäuden; Bauliche, organisatorische und finanzielle Vorsorge der öffentlichen Hand; Zustand von (Schutz-)Infrastrukturen; Verwendete Baumaterialien von (Schutz-)Infrastrukturen; Begrünung von Städten/Siedlungen; Grad der Versiegelung` |
| KWRA-2021-Mappe | `docs/KWAR/KWRA-2021_Klimawirkungen.xlsx`, Blatt `Wirkungsmechanismen`, Zeile 67 (ID `62`), Spalte G (Kopfzelle G5: `Vulnerabilität – Sensitivitätsfaktoren`) | `Begrünung von Städten / Siedlungen · Grad der Versiegelung` |

Die Schadensbaum-Mappe nennt sieben Faktoren (S094 bis S100, Spalte F derselben Zeile), die
KWRA-2021-Mappe zwei. *Ergebnis der Regel:* Es gelten die sieben Sensitivitäten der
Schadensbaum-Mappe. Die fünf nur dort genannten Faktoren muss der Bericht zu #62 adressieren
(§2.1). So hat Befund 13 in `reviews/BEFUNDE_62.md` schon entschieden.

**Beispielfall #63 — Innenraumklima.** Auch hier betrifft der Widerspruch die
Sensitivitätsfaktoren, und zwar in beide Richtungen.

| | Fundstelle | Wortlaut der Zelle |
|---|---|---|
| Schadensbaum-Mappe | `docs/Schadensbaum/KWRA-Schadensbaum_X_UBA-klimawirkungsketten.xlsx`, Blatt `Klimawirkungsketten`, Zeile 278 (Knoten `W123`), Spalte J (Kopfzelle J1: `Input_Namen_Sensitivitäten`) | `Bauliche, organisatorische und finanzielle Vorsorge der Eigentümer und Nutzer von Gebäuden und Infrastrukturen; Zustand von Gebäuden und Infrastrukturen; Verwendete Baumaterialien auf Gebäudeebene` |
| KWRA-2021-Mappe | `docs/KWAR/KWRA-2021_Klimawirkungen.xlsx`, Blatt `Wirkungsmechanismen`, Zeile 68 (ID `63`), Spalte G (Kopfzelle G5: `Vulnerabilität – Sensitivitätsfaktoren`) | `Verwendete Baumaterialien auf Gebäudeebene · Begrünung von Gebäuden` |

Gemeinsam ist beiden nur der Faktor Verwendete Baumaterialien auf Gebäudeebene (S094). Die Schadensbaum-Mappe führt
zusätzlich die Vorsorge der Eigentümer und Nutzer und den Zustand von Gebäuden (S092, S093,
Spalte F derselben Zeile). Die KWRA-2021-Mappe führt zusätzlich die Begrünung von Gebäuden, die
die Schadensbaum-Mappe bei #63 nicht nennt, sondern nur bei #62 (S095). *Ergebnis der Regel:* Es
gelten die drei Sensitivitäten S092, S093 und S094 der Schadensbaum-Mappe. Die Begrünung von
Gebäuden ist für #63 kein Eingangsknoten. Für #63 gibt es noch keinen Bericht und kein Ledger.
Den Vermerk trägt der erste Erstaufschlag zu #63 (Skill `methodik_consultant-erstaufschlag`) in `reviews/BEFUNDE_63.md` ein.

---

*Dieses Dokument ersetzt: Aufgabenbeschreibung v1 (22.08.2026) und `docs/METHODIK_GRUNDSAETZE.md`.*
