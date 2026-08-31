# Aufgabenbeschreibung: Methodik zur Schadensrechnung von Klimarisiken — v2 (konsolidiert)

Stand: 25.08.2026 · **Einzige Instruktionsquelle** für Herleitung, Review und Integration von
Risiko-Methodiken.

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
> als Bezugsgröße ist unzulässig. v2 konsolidiert die Aufgabenbeschreibung v1 (22.08.2026) und
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

### 2.6 Methodik-Familien statt Drei-Ansätze-Ritual

Risiken werden **Familien** zugeordnet (z. B. „K1-Gesundheit bottom-up" = #95/#96/#98-Muster;
„K3/K4-Ereignisschäden" = Eintrittswahrscheinlichkeit × Schadensfunktion × Bestand;
„K6-Ertragsmodelle"; „K8-Vorsorge-Weichen"). Der vollständige **Drei-Ansätze-Vergleich (a–d,
Kriterienraster, Empfehlung) ist nur Pflicht beim ersten Risiko einer Familie** oder wenn die
Methodenwahl fachlich strittig ist. Folge-Risiken derselben Familie übernehmen das
Familien-Template und dokumentieren Alternativen als kurze Verworfen-Liste (je ein Satz Grund).
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
  Normierung/Zentrierung) und kennzeichnet sie „neu anzulegen" — `/integriere-risiko`
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
- Zeitbezug sauber: Jahreswerte, Szenariojahre (je empfohlenem Ansatz ein Absatz
  „Szenario-Anwendung": verschobene Größe, konstante Größen, Stationaritätsannahmen), Latenzen
  explizit.

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
  vage „auf β"); R7-Weiche referenzieren, wo einschlägig. Hebel ohne quantifizierte Effektgröße
  laufen ehrlich als „qualitativ".

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

### 3.7 Ansatz-Vergleich (nur wo nach §2.6 gefordert)

Festes Kriterienraster: kausale Treue · Kalibrierbarkeit · lokale Differenzierung ·
Datenverfügbarkeit · Maßnahmen-Anschluss · Architektur-Konformität · Aufwand. Empfehlung begründet;
Verworfenes ggf. als Ergänzungsmodul benannt.

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
- **Geltungsbereich:** vollständig für jeden Ansatz, der **Umsetzungsgrundlage** ist; dokumentierte
  Alternativen/Negativ-Beispiele bis zur Quelle. Wird eine Alternative später Umsetzungsgrundlage,
  gilt die Pflicht vor der Implementierung vollständig.

Fertig-Regel: Jede Zeile jeder Zeichentabelle referenziert in „Wert/Herkunft" eine abgeschlossene
Herleitung (Register-ID oder Herleitungs-Anker) — kein Verweis auf später.

---

## 4. Berichtsstruktur je Risiko (Template)

```
docs/methodik/<nn>_<risiko>.md
1  Wirkungskette & Knoten-Bilanz          (§2.1; Weitergaben zweispaltig)
2  Evidenz-Register                        (§2.2; Register-IDs, Entscheidungsspalte)
3  Modell                                  (§2.3; Formeln + Zeichentabellen + Beispiele)
4  Kalibrierung & Validierung              (§2.4/§3.4; Skripte/CSVs als Anlage verlinkt)
5  Maßnahmen-Hebel                         (§2.5/§3.5)
6  Szenario-Anwendung & Modellgrenzen      (§3.2; inkl. Infokasten-Texte §3.6)
7  Parameter-Blöcke                        (maschinenlesbar, s. u.)
8  Quellen                                 (§3.8)
[nur erster Familien-Vertreter: 9 Ansatz-Vergleich (§3.7)]
```

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
```

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
11. **Form:** Zeichentabellen vollständig; Beispiele rechnen auf (Golden-Tests grün)?
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
| **Erstaufschlag** | Claude Code (Repo) | Template §4, Bundle §1, Familien-Template | `docs/methodik/<risiko>.md` + Skripte/CSVs; Lints lokal grün |
| **Review** | frische Session: Claude Code `/review-methodik` (bevorzugt — Bundle liegt im Repo) oder claude.ai mit komplettem Bundle | Bundle + Bericht + Ledger | Befunde ins Ledger (Format §5) |
| **Revision** | Claude Code | Ledger | aktualisierter Bericht + Statusspalte je Befund; Rechenläufe neu, wo Kopplungen betroffen |
| **Re-Review** | frische Session | Diff + Ledger | nur: geänderte Abschnitte, Regression geschlossener Befunde, offene Befunde; **volle Prüfung erneut**, wenn Kalibrierung oder Modellstruktur geändert wurde |
| **Abnahme** | — | Abnahmekriterien | Freigabe zur Integration |

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

**CI-Tests aus dem Bericht:**
- Mini-Rechenbeispiele → pytest (Bericht ⇄ Code können nicht divergieren).
- Sanity-Anker → Test „Bundessumme ∈ [Untergrenze, Obergrenze]".
- Verteilungs-/Struktur-Validierung → Test mit vorab fixierter Toleranz.
- Kalibrier-Pipeline als reproduzierbares Skript (Daten-Pins), nicht als Einmal-Lauf.

**Claude-Code-Bausteine** (einmal bauen, dann je Risiko wiederverwenden):
- `/neu-risiko <nn>`: instanziiert Template §4, zieht Knoten + Kanten + Konto automatisch aus den
  Arbeitsmappen in Abschnitt 1, legt Register-Skelett mit einer Zeile je Knoten an
  (Entscheidung „offen").
- `/review-methodik <nn>`: führt Lints aus, arbeitet dann §5 ab, schreibt Befunde ins Ledger.
- `/integriere-risiko <nn>`: extrahiert Parameter-Blöcke in die Registry, implementiert die
  Schicht-B-Funktion gegen die Registry, generiert die Tests aus Beispielen und Sanity-Ankern,
  legt Kartenebenen an.
- Wiederverwendbares **Evidenz-Register-Repository** (`docs/evidenz/register.md` oder CSV):
  risikoübergreifende Zeilen einmal pflegen, je Risiko referenzieren.

**Reihenfolge des Ausbaus:** (1) M0-Bericht auf dieses Format migrieren (er ist der
Familien-Prototyp „K1-Gesundheit bottom-up" — die Migration erzeugt Lints, Registry-Extraktion
und die ersten Golden-Tests als Nebenprodukt), (2) Lints + Commands bauen, (3) erst dann das
nächste Risiko — ab dann kostet ein Familien-Folgerisiko einen Bruchteil des M0-Aufwands.

---

*Dieses Dokument ersetzt: Aufgabenbeschreibung v1 (22.08.2026) und `docs/METHODIK_GRUNDSAETZE.md`.*
