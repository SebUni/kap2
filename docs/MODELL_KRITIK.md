# Modell-Kritik — Rechenmodell KAP2 (HxVxE → absolute Outcomes)

Stand: Juli 2026. Reine Analyse, keine Code-Änderung. Grundlage: verifizierter
Code-Stand in `backend/app/services/engine/risk_engine.py`,
`backend/app/data/catalog.py`, `backend/app/services/engine/override_context.py`.
Gegengelesen: `docs/BERECHNUNGS_HANDBUCH.md`, `docs/REVIEW_WIRKUNGSMECHANISMEN.md`.

Kurzfazit vorab: Der HxVxE-Index ist als **Screening-/Vergleichslogik tragfähig** und
soll bleiben. Die daraufgesetzte **Absolutwert- und Kostenschicht ist methodisch nicht
haltbar** (lineare `ref_value`-Skalierung eines gemittelten Screening-Scores, P90-Index
× Gesamtbevölkerung als „Schadenssumme", EAD-Doppelzählung). Empfehlung: **Option (c)** —
HxVxE fürs Screening behalten, die Outcome-/Kostenschicht durch eine getrennte
Wirkmodell-/Schadensfunktionsschicht ersetzen. Die vollständige Alternativ-Spezifikation
für alle 48 Risiken steht in Abschnitt 6.

---

## 1. Ist-Modell kompakt (mit Code-Fundstellen)

**Zell-Risikoindex** (`risk_engine.cell_risk_indices`, Z. 44–64):

$$\text{Index}_{\text{Risiko}} = 100 \cdot \frac{\sum_p w_p\,\hat H_p\,\hat E_p\,\hat V_p}{\sum_p w_p}$$

Das ist ein **gewichteter Mittelwert** der Pfad-Produkte, kein Summenmodell.
`_WEIGHT_SUM` normiert auf die Gewichtssumme (Z. 27–29).

**Wirkungsketten** (`catalog.build_pathways`, Z. 1043–1088): aus den geordneten
H-/E-/V-Listen eines Risikos werden **deterministisch/kombinatorisch** Pfade erzeugt
(primary, aligned, alternate_hazard/exposure/vulnerability, compound_he/hv/ev).
Gewichte `PATHWAY_WEIGHTS` (Z. 1030–1040): primary 1.0, aligned 0.85, alternate
0.70–0.75, compound 0.55–0.65. `EXPECTED_ANNUAL_MORTALITY` (Z. 508–517) hat je 3
Hazards/Exposures/Vulnerabilities → **12 Pfade**, Gewichtssumme **8,80** (verifiziert:
1·1,0 + 2·0,85 + 2·0,75 + 2·0,70 + 2·0,70 + 0,65 + 0,60 + 0,55).

**Normierung** (`catalog.normalize_value`, Z. 2427–2440; override-fähig in
`override_context.normalize_value`, Z. 47–52): linear min–max auf 0..1 mit Clamp,
Grenzen `norm_min`/`norm_max` je Indikator (z. B. `HEAT_WAVE` 0..40 Tage/Jahr, Z. 98;
`POPULATION_DENSITY` 0..8000 Pers./km², Z. 199).

**Absolutwert / Outcome** (`cell_outcome` Z. 76–81, `estimate_outcome_and_cost`
Z. 112–123):

$$\text{outcome} = \text{ref\_value} \cdot \frac{\text{Index}}{100} \cdot \text{scale\_factor}$$

`scale_factor` = pop/100000 | area_km2/50 | 1.0 (`_scale_factor`, Z. 67–73).
`ref_value` = „Outcome bei Index=100 für eine Referenzkommune mit 100 000 Ew."
(Kommentar Z. 503), z. B. Mortalität `ref_value=18` Todesfälle/Jahr (Z. 515),
Gebäudeschäden `4.5 Mio €` (Z. 572), EAD `10 Mio €` (Z. 614). `ref_value` ist
override-fähig (`effective_ref_value`, Z. 21–23).

**Kommune-Aggregation** (`aggregate`, Z. 126–186; `AGGREGATION_PERCENTILE = 90.0`,
Z. 23): je Risiko das **90. Perzentil** der Zell-Indizes (`_percentile`, Z. 100–109);
Outcome/Kosten werden aus diesem P90-Index **× Gesamtbevölkerung** gerechnet
(`estimate_outcome_and_cost` mit `total_pop`, Z. 149). Gruppen-Index = arithmetisches
**Mittel der Einzelrisiko-P90** je KWRA-Gruppe (Z. 162–171).

**Kosten** (Z. 117–123 und 173–180): `cost_eur = outcome` bei
`cost_dimension="monetary"`; sonst `outcome · cost_per_outcome_eur`, falls gesetzt.
Real tragen zur Summe bei: **17 monetäre Risiken** + **5 Gesundheitsrisiken** mit
`cost_per_outcome_eur` (Mortalität 3,5 Mio; Morbidität 5 000; Verletzte 12 000;
Psyche 4 000; Betroffene/Evakuierte 2 500 — Z. 515–548). **26 der 48 Risiken tragen
0 € bei** (11 operational, 11 environment, 2 Belastungsstunden-Health mit
`cost_per_outcome_eur=0`, 2 Index-Health ohne Kostensatz). `total_eur` = Summe über
**alle** Risiken **inklusive** `EXPECTED_TOTAL_DAMAGE_EAD_EUR` (Z. 608–614) → mutmaßliche
Doppelzählung.

> Anmerkung zur Prompt-Vorgabe: „health, nur 12/48" trifft die Rechnung nicht exakt —
> es sind **5** Gesundheitsrisiken mit echtem Kostensatz (22 kostenwirksame Risiken
> insgesamt). Das verschärft die Kritik in Abschnitt 3.4, nicht umgekehrt.

---

## 2. Stärken (ehrlich, kurz)

1. **KWRA/IPCC-konformes Grundgerüst.** Risiko als Funktion von Hazard × Exposure ×
   Vulnerability ist die etablierte Screening-Logik (IPCC AR6 WGII 2022; KWRA 2021).
   Multiplikativ ist richtig: fehlt eine Komponente (kein Grün, keine Bevölkerung),
   geht das Risiko gegen 0 — sachlogisch korrekt.
2. **Einheitlicher, nachvollziehbarer Rahmen** über alle 48 Risiken. Gleiche Formel,
   dieselbe Normierung, dieselbe Aggregation — leicht auditierbar, gut dokumentiert
   (Tooltips, Handbuch, Provenienz-Felder).
3. **Editierbarkeit / Overrides** (`override_context`) für Normgrenzen, `ref_value`,
   Gewichte, UHI-Koeffizienten. Governance-freundlich (Verantwortung bei der Kommune).
4. **P90 statt Mittel** über Zellen ist die richtige Grundidee, um Belastungsspitzen
   nicht wegzumitteln — die Umsetzung ist aber inkonsistent (Abschnitt 3.3).
5. **Ehrliche Provenienz-Kennzeichnung** vieler Werte als „Modellannahme" statt
   erfundener Quellen — gute Basis für die spätere Belegung.

Diese Stärken betreffen die **Screening-Schicht**. Sie rechtfertigen nicht die
Absolutwert-/Kostenschicht.

---

## 3. Schwachstellen — mit durchgerechnetem Zahlenbeispiel

Durchgehendes Beispiel: `EXPECTED_ANNUAL_MORTALITY`, 12 Pfade, Gewichtssumme 8,80.
Angenommene normierte Werte einer mäßig heißen, dichten Zelle:

| Komponente | Code | absolut | norm |
|---|---|---|---|
| Hazard 0 | HEAT_WAVE | 24 Tage/Jahr (÷40) | 0,60 |
| Hazard 1 | COLD_EXTREME | 8 (÷40) | 0,20 |
| Hazard 2 | COMPOUND_EVENT | — | 0,30 |
| Exposure 0 | POPULATION_DENSITY | 3000 (÷8000) | 0,375 |
| Exposure 1 | VULNERABLE_GROUPS_POPULATION | — | 0,30 |
| Exposure 2 | AGE_STRUCTURE | — | 0,40 |
| Vuln 0 | HEAT_SENSITIVITY | — | 0,60 |
| Vuln 1 | HEALTHCARE_ACCESS | — | 0,40 |
| Vuln 2 | VULNERABLE_GROUPS_SHARE | — | 0,35 |

### 3.1 Der Mittelwert **verdünnt** das dominante Signal (Kettenkombinatorik-Artefakt)

Die 12 Pfade und ihre Beiträge `w · Ĥ·Ê·V̂`:

| # | Pfadtyp | H×E×V | Produkt | w | w·Produkt |
|---|---|---|---|---|---|
| 1 | primary | HEAT×POPD×HEATSENS | 0,135 | 1,00 | 0,1350 |
| 2 | aligned | COLD×VULNPOP×HEALTH | 0,024 | 0,85 | 0,0204 |
| 3 | aligned | COMP×AGE×VULNSHARE | 0,042 | 0,85 | 0,0357 |
| 4 | alt_hazard | COLD×POPD×HEATSENS | 0,045 | 0,75 | 0,0338 |
| 5 | alt_hazard | COMP×POPD×HEATSENS | 0,0675 | 0,75 | 0,0506 |
| 6 | alt_exposure | HEAT×VULNPOP×HEATSENS | 0,108 | 0,70 | 0,0756 |
| 7 | alt_exposure | HEAT×AGE×HEATSENS | 0,144 | 0,70 | 0,1008 |
| 8 | alt_vuln | HEAT×POPD×HEALTH | 0,090 | 0,70 | 0,0630 |
| 9 | alt_vuln | HEAT×POPD×VULNSHARE | 0,0788 | 0,70 | 0,0551 |
| 10 | compound_he | COLD×VULNPOP×HEATSENS | 0,036 | 0,65 | 0,0234 |
| 11 | compound_hv | COLD×POPD×HEALTH | 0,030 | 0,60 | 0,0180 |
| 12 | compound_ev | HEAT×VULNPOP×HEALTH | 0,072 | 0,55 | 0,0396 |

Summe `w·Produkt` = 0,651 → **Index = 100 · 0,651 / 8,80 = 7,40**.

Der **Primärpfad allein** ergäbe 100·0,135 = **13,5**. Der kombinatorische Mittelwert
(7,40) ist **~45 % niedriger** als das dominante Heat-Signal, weil die
Recombinant-Pfade (Cold/Compound in den Nenner gemischt) den Score nach unten ziehen.
Der Primärpfad hat nur **1,0/8,80 = 11,4 %** Gewicht — die eigentliche
Hitze-Todesursache wird von mechanisch erzeugten Mischpfaden überstimmt.

Outcome (100 000 Ew., Index=7,40): `18 · 7,40/100 · 1,0 = 1,33 Todesfälle/Jahr`.

### 3.2 „Mitteln vs. Addieren" — beide Extreme sind falsch, aber aus verschiedenen Gründen

Der Product-Owner-Einwand („aus jeder Kette können Tote resultieren → addieren"): die
12 Pfade sind **keine disjunkten Todesursachen**, sondern **Rekombinationen derselben
3×3×3 Faktoren**. Pfade 1, 6, 7, 8, 9, 12 betreffen alle `HEAT_WAVE` auf **dieselbe
Population**. Würde man die Pfad-Produkte addieren, würden dieselben Hitzetoten 6-fach
gezählt. Naiv-Addition ohne Normierung:
`100 · Σ(w·Produkt) = 100 · 0,651 = 65,1` — bzw. bei ungewichteter Produktsumme
(Σ Produkte = 0,872) → Index ≈ 87 und bei nur wenig höheren Eingaben sofort **Clamp
auf 100**. Addition ist also **nicht haltbar**.

Aber: Der Mittelwert (7,40) ist ebenso wenig eine „reale Größe". Er ist ein
**Screening-Score**, dessen Höhe davon abhängt, **wie viele** Pfade `build_pathways`
zufällig erzeugt (Abschnitt 3.5). Er wird nur über die `ref_value`-Kalibrierung in eine
plausible Totenzahl „zurückgebogen".

### 3.3 Die `ref_value`-Kopplung ist **implizit und bricht unter Editierung**

`ref_value=18` wurde laut Kommentar (Z. 513) so gewählt, dass „typische P90-Indizes
20–40 → 3,6–7,2/100k" ergeben — d. h. der Anker kompensiert genau die Verdünnung aus
3.1. Diese Kopplung ist **nirgends explizit**; sie ist eine stille Kalibrierung eines
Screening-Scores auf eine Statistik.

Sie bricht, sobald jemand die **beworbene Editierbarkeit** nutzt:

- Setzt eine Kommune `HEAT_WAVE.norm_max` von 40 auf 30 (dokumentiertes Override,
  `override_context.effective_norm_bounds`), steigt `Ĥ_HEAT` von 0,60 auf 0,80 (+33 %),
  der Index steigt entsprechend, und da `ref_value` **unverändert** bleibt, steigt die
  ausgewiesene **Totenzahl um ~1/3 — ohne dass ein einziger Mensch mehr gefährdet ist**.
- Ändert jemand ein Pfadgewicht, verschiebt sich `_WEIGHT_SUM`, der Index skaliert
  mit, `ref_value` folgt nicht → Absolutwert falsch.

Der Nutzer editiert eine **Normierungs-Stellschraube fürs Screening** und verändert
unwissentlich die **absolute Schadensbilanz**. Kopplung intransparent und nicht robust.

### 3.4 Linearität `outcome ∝ Index` bildet Dosis-Wirkung nicht ab

`outcome = ref · Index/100 · scale` ist **linear** im Index; der Index ist trilinear in
`Ĥ·Ê·V̂` mit hartem Clamp. Reale Hitzemortalität ist **überproportional** (Exzessmortalität
steigt exponentiell oberhalb einer Schwellentemperatur; an der Heiden u. a. 2020,
Winklmayr u. a. 2022). Konsequenzen:

- **Doppelter Index ≠ doppelte Tote.** Von Index 40 auf 80 verdoppelt das Modell die
  Toten; epidemiologisch kann das ein Faktor 4+ sein. Extremrisiken werden **unterschätzt**.
- **Sättigung durch Clamp:** eine Zelle mit 60 heißen Tagen clamped auf `Ĥ=1,0` —
  identisch zu 40 Tagen. Unter Klimaprojektion (RCP8.5), wo Extreme die Referenzskala
  überschreiten, **saturiert das Modell genau dort, wo es differenzieren müsste**.
- **Schwellenwerteffekte** (Deichüberlauf, Netzausfall ab Belastung X) sind prinzipiell
  nicht darstellbar — ein linearer Index kennt keinen Kipppunkt.

Für **Screening/Ranking** ist Linearität vertretbar. Als Basis **absoluter** Tote/€
ist sie es nicht.

### 3.5 `build_pathways` ist ein **Artefakt**, kein Wirkungsketten-Modell

Die Pfade entstehen mechanisch aus der **Listenreihenfolge**. Beispiele aus Mortalität:

- Pfad 11 (`compound_hv`): `COLD_EXTREME × POPULATION_DENSITY × HEALTHCARE_ACCESS` —
  eine „Kälte"-Kette in einem **Hitze**-Mortalitätsrisiko.
- Pfad 3 (`aligned`): `COMPOUND_EVENT × AGE_STRUCTURE × VULNERABLE_GROUPS_SHARE` —
  gepaart nur, weil sie an Listenposition 2 stehen. Keine kausale Begründung.
- Pfad 10 (`compound_he`): `COLD × VULNERABLE_GROUPS_POPULATION × HEAT_SENSITIVITY` —
  mischt **Kälte-Hazard mit Hitze-Sensitivität**. Fachlich sinnlos.

Die **Anzahl** Pfade (und damit die Verdünnung) hängt allein davon ab, wie viele
H/E/V gelistet sind: 3×3×3 → 12 Pfade; ein Risiko mit 2×1×2 bekommt nur 4. Ein Risiko
wirkt also **niedriger im Index**, nur weil sein Autor mehr Nebenfaktoren aufgezählt
hat. Echte KWRA-Wirkungsketten sind **expertenkuratiert**, nicht kartesische Produkte.

### 3.6 Aggregation: **drei widersprüchliche Wahrheiten** aus denselben Daten

`aggregate` rechnet Kommune-Outcome aus **P90-Index × Gesamtbevölkerung**
(`estimate_outcome_and_cost(risk, p90_idx, total_pop, area)`, Z. 149) — nicht als
Summe der Zell-Outcomes. Zahlenbeispiel, 10 000 Zellen, je 10 Ew. (total 100 000):

- 9 900 Zellen mit Index 5, 100 Zellen mit Index 80.
- **Karte** (`cell_outcome` je Zelle): 100 Zellen leuchten tiefrot (Index 80).
- **Dashboard-P90**: `_percentile` → Rang 0,9·9999 ≈ 8999 → Wert **5**. Ausgewiesene
  Toten: `18 · 5/100 = 0,90/Jahr`.
- **Summe der Zell-Outcomes** (physikalisch korrekt):
  `18/100 · Σ(Index_i·pop_i)/100000 = 18/100 · (9900·5·10 + 100·80·10)/100000
  = 18/100 · 5,75 = 1,035/Jahr`.

Drei Zahlen, ein Datensatz: Karte „tiefrot", Dashboard-P90 „0,9 (unauffällig)",
korrekte Summe „1,035". Das ist **genau der Oschatz-Befund** (TODO Z. 17): Karte rot,
Dashboard grün. Zusätzlich ist die P90-Größe **konzeptionell falsch als
Schadenssumme**: sie multipliziert eine **Intensitäts-Perzentil-Kennzahl** mit der
**Gesamt**bevölkerung — das ist weder das Maximum noch die Summe, sondern eine Größe
ohne physikalische Bedeutung. (Für ein reines Ranking ist P90 dagegen sinnvoll.)

### 3.7 Doppelzählung in der Kostensumme

`total_eur = Σ cost_eur` über **alle** Risiken enthält `EXPECTED_TOTAL_DAMAGE_EAD_EUR`
(`ref_value=10 Mio`, Z. 614), das laut eigener Herleitung (Z. 613) den **nationalen
Gesamtschaden ~8 Mrd/832 ≈ 9,6 Mio** abbildet — also **per Konstruktion die Summe der
Sektorschäden**. Rechnung für eine Referenzkommune (100 000 Ew.) bei Index=100, alle
pop-skalierten monetären Risiken:

Gebäude 4,5 + Verkehr 1,8 + Energie 0,9 + Telekom 0,4 + Wasser/Abwasser 0,7 +
Wiederherstellung 1,5 + indirekt 1,2 + Versorgungsengpässe 0,6 + Migration 0,4 +
Standortnachteile 0,5 + verzögert 0,35 = **12,85 Mio €** Sektorschäden
**+ EAD 10 Mio €** = **22,85 Mio €**.

Die 10 Mio EAD sind **~78 % der 12,85 Mio Sektorschäden noch einmal** — eine fast
vollständige Doppelzählung des Gesamtschadens.

Weitere Überlappungen innerhalb der 12,85 Mio:

- **Wiederherstellungskosten (1,5 Mio)** = Reparaturanteil **derselben** Gebäude-/
  Infrastrukturschäden, die schon in Gebäude/Verkehr/Energie stecken (Z. 620 sagt es
  selbst: „Teilmenge des EAD").
- **Indirekte Verluste / Versorgungsengpässe / Standortnachteile / Migration /
  verzögerte Schäden** sind **Folgeeffekte** der direkten Sektorschäden. Als eigene
  additive Posten sind sie nur zulässig, wenn sie explizit als **Multiplikator auf die
  direkten Schäden** modelliert werden — heute sind es unabhängige HxVxE-Risiken, also
  teilweise Doppelzählung.

---

## 4. Urteil je Kernfrage

| # | Frage | Urteil | Begründung |
|---|-------|--------|------------|
| 1 | Mitteln vs. Addieren über 12 Ketten | **bedingt haltbar** | Mitteln ist **richtiger als Addieren**, weil die Pfade dieselbe Population rekombinieren (Addition würde 6-fach zählen, Abschnitt 3.2). Der Mittelwert ist aber keine reale Größe, sondern ein Screening-Score, der über `ref_value` zurückkalibriert wird. Als Basis absoluter Tote nur bedingt tauglich. |
| 1b | `ref_value`-Kopplung transparent/robust | **nicht haltbar** | Die Kalibrierung `18 → 3,6–7,2/100k` kompensiert die Verdünnung implizit und **nirgends dokumentiert im Code-Fluss**. Editiert ein Nutzer `norm_max` oder Gewichte (beworbenes Feature), ändert sich der Absolutwert ohne reale Ursache (Abschnitt 3.3). |
| 2 | Normierter Index als Basis absoluter Outcomes | **nicht haltbar** | Lineare `ref·Index/100`-Skalierung ignoriert Dosis-Wirkung, Schwellen und Sättigung; Clamp saturiert genau bei Extremen (Abschnitt 3.4). Für Ranking ok, für €/Tote nicht. |
| 3 | P90 + „Mittel der P90s" für absolute Summen | **nicht haltbar** | P90-Index × Gesamtbevölkerung ist keine Schadenssumme; Karte, Dashboard-P90 und Summe der Zell-Outcomes widersprechen sich (Abschnitt 3.6, Oschatz). P90 als **Screening-Kennzahl** haltbar, als **Summenbasis** nicht. |
| 4 | Doppelzählungen (EAD, Sektorüberlappungen) | **nicht haltbar** | EAD verdoppelt die Sektorschadenssumme fast vollständig (Abschnitt 3.7); Wiederherstellung/indirekte/verzögerte Posten überlappen die direkten Schäden. |
| 5 | `build_pathways`-Kombinatorik fachlich begründet | **nicht haltbar (Artefakt)** | Pfade entstehen aus Listenreihenfolge, mischen inkompatible Faktoren (Kälte × Hitze-Sensitivität), und die Pfadzahl bestimmt die Score-Höhe (Abschnitt 3.5). Keine kuratierten Wirkungsketten. |
| 6 | KWRA-Anschluss **und** absolute monetarisierbare Werte | **bedingt haltbar (nur getrennt)** | KWRA/UBA 2021 ist eine **Screening-/Vergleichs**-Methodik, nicht für Absolutschäden gedacht. Beides geht nur mit **getrennten Schichten**: HxVxE fürs Screening + eigene Schadensfunktions-/Wirkmodell-Schicht für Absolutwerte (Abschnitt 5/6). Ein einziger linearer Faktor kann beides nicht leisten. |

---

## 5. Empfehlung

**Klare Ansage: Option (c) — die Outcome-/Kostenschicht ersetzen, den HxVxE-Index
fürs Screening behalten.** Nicht (a) (das Absolutmodell ist irreführend und angreifbar),
und mehr als (b) (punktuelle Reparaturen beheben weder die Linearitäts- noch die
Aggregations-Grundfehler).

Die vom Auftrag favorisierte Architektur ist genau die richtige und wird empfohlen:

> **Zwei-Schichten-Architektur**
>
> - **Schicht A — Screening (HxVxE, bleibt):** normierter Index 0–100 je Risiko je
>   Zelle. Zweck: Karten, Radar, Vergleich zwischen Kommunen/Risiken, Maßnahmenwirkung
>   (multiplikativ). Aggregation Zelle→Kommune per **Perzentil (P90/Max)** — das ist
>   für eine Intensitäts-/Belastungskennzahl korrekt. Änderungsbedarf: gering (optional
>   Pfad-Dilution beheben, siehe unten).
> - **Schicht B — Wirkmodell / Schadensfunktionen (neu, ersetzt `ref·Index/100`):**
>   je Risiko eine **Expected-Annual-Impact-Funktion**, die aus **absoluter** Exposition
>   (Bevölkerung, Assetwert, Fläche), **Hazard-Eintrittswahrscheinlichkeit/-intensität**
>   und einer **Dosis-Wirkungs-/Schadensfunktion** eine absolute Outcome-Größe je Zelle
>   liefert. Aggregation Zelle→Kommune per **Summe**. Monetarisierung über **explizite,
>   editierbare Kostensatz-Parameter** je Risiko. **Gesamtschaden = Summe** der
>   monetarisierten Einzelrisiken (EAD ist kein eigenes Risiko mehr).

Warum diese Trennung KWRA-konform ist: Die KWRA nutzt HxVxE als **relatives**
Risikoklassen-Screening — dort bleibt KAP2 voll anschlussfähig. Absolute Schäden sind
in der KWRA-Praxis (und in Prognos 2023, UBA MK3.1) **eigene Schadensmodelle** (AAL/EAD
über Schadensfunktionen). KAP2 bildet damit beide Welten sauber getrennt ab, statt sie
in einen einzigen linearen Faktor zu pressen.

**Gezielte Stellschrauben, die trotzdem sofort greifen** (falls (c) gestaffelt kommt,
sind das die (b)-Zwischenschritte):

1. **EAD entkoppeln** (`catalog.py` Z. 608–614): aus der additiven Summe nehmen bzw. zu
   reiner Anzeige-Summe umwidmen → beendet die größte Einzel-Doppelzählung sofort.
2. **Kostensätze als Parameter** herauslösen (`cost_per_outcome_eur`,
   `parameter_registry`): jeder nicht-monetäre Outcome bekommt einen sichtbaren,
   belegten €-Parameter (Voraussetzung für „alles monetarisieren").
3. **Aggregations-Konsistenz**: Absolutschäden **immer als Summe der Zell-Outcomes**,
   P90/Max nur als Intensitäts-Kennzahl daneben — nie P90-Index × Gesamt-pop als €.
4. **Pfad-Dilution** entschärfen (Übergangslösung, bis Schicht B steht): entweder nur
   den Primär-/kuratierte Pfade werten oder auf `max`/kuratierte Gewichte umstellen,
   damit die Score-Höhe nicht von der Pfadanzahl abhängt.

---

## 6. Alternativ-Spezifikation (Schicht B) — alle 48 Risiken

Notation: `Zelle c`; `pop_c` Einwohner der Zelle; `A_c` Fläche (0,01 km²);
`assetval_c` exponierter Sachwert; `P_hazard` mittlere jährliche
Eintrittswahrscheinlichkeit/Intensität des Hazards; `f_dose(·)` Dosis-Wirkungs-/
Schadensfunktion (0..1 oder Rate); `V̂_c` normierte Vulnerabilität aus **Schicht A**
(weiterverwendbar!). **Aggregation Kommune = Σ über Zellen**, sofern nicht anders
angegeben. Jeder €-Satz ist ein **editierbarer Registry-Parameter mit Quelle**.

Grundmuster (gilt für alle Gruppen):

$$\text{Outcome}_{\text{Kommune}} = \sum_c \underbrace{\text{Exposition}_c}_{\text{absolut}}\cdot\underbrace{f_{\text{dose}}(\text{Hazard-Intensität}_c)}_{\text{Dosis-Wirkung}}\cdot\underbrace{g(\hat V_c)}_{\text{Vuln.-Modifikator}}$$

$$\text{Schaden}_{\text{Kommune}} = \text{Outcome}_{\text{Kommune}}\cdot \text{Kostensatz}$$

`g(V̂)` z. B. `(0,5 + V̂)` als Vulnerabilitäts-Multiplikator — behält die Rolle der
Schicht-A-Vulnerabilitäten, ohne die Linearitätsfehler des Index selbst zu erben.
Schicht A liefert weiterhin `V̂_c` und die Hazard-Normierung als Screening; Schicht B
nutzt **absolute** Hazard-Intensität aus denselben Rohdaten (DWD/KOSTRA/Terrain).

### 6.1 Gruppe HEALTH (9 Risiken)

Kern: **Betroffene Personen × attributable Rate × Kostensatz**. Bevölkerung
ortsaufgelöst aus Zensus (bereits vorhanden).

| Risiko | Formel (Outcome je Zelle) | Parameter (Einheit) | Quellenlage |
|---|---|---|---|
| EXPECTED_ANNUAL_MORTALITY | `pop_c · baseline_mort · AF(ΔT_c)`, `AF = 1−exp(−β·(T_c−T_thr)_+)` | `baseline_mort` (Tote/100k), `β` (%/°C, ~1–4), `T_thr` (°C), VSL (€/Tod, 3,5 Mio) | RKI JoHM; Winklmayr u. a. 2022; an der Heiden 2020; UBA MK3.1 |
| EXPECTED_ANNUAL_MORBIDITY | `pop_c · morb_rate · AF(ΔT_c, Vektoren)` | `morb_rate` (Fälle/100k), Kostensatz (€/Fall) | RKI JoHM; UBA MK3.1 |
| EXPECTED_ANNUAL_INJURIES | `pop_expo_c · P_flood/storm · inj_rate` | `inj_rate` (Verletzte/betroffene Person·Ereignis), €/Verletzten | GDV; BBK; UBA MK3.1 |
| EXPECTED_ANNUAL_MENTAL_HEALTH | `pop_expo_c · P_ereignis · mental_rate` | `mental_rate`, €/Fall | RKI JoHM; UBA MK3.1 |
| EXPECTED_ANNUAL_AFFECTED_EVACUATED | `pop_c[in Gefahrenzone] · P_flood/surge` | Evakuierungs-Auslöseschwelle, €/Person | HWGK/KOSTRA; BBK |
| EXPECTED_THERMAL_STRESS_HOURS | `pop_outdoor_c · Σ Stunden(T>Schwelle)` | Schwellentemperatur, Stunden aus DWD; optional €/h Produktivitätsverlust | DWD; UBA MK3.1 (Produktivität) |
| EXPECTED_POLLUTANT_EXPOSURE_HOURS | `pop_c · Σ Stunden(Ozon/PM>Schwelle)` | Schwellen, €/h (optional) | UBA Luft; DWD |
| MEDICAL_UNDERSUPPLY_RISK_INDEX | Index bleibt (Screening) ODER `versorgungslücke · pop_vuln` | €/unterversorgtem Fall (optional) | BBSR-Erreichbarkeit; RKI |
| SOCIAL_INEQUALITY_AMPLIFICATION_RISK_INDEX | **Index behalten**, nicht monetarisieren (Modifikator) | — | KWRA 2021 (qualitativ) |

Aggregation: **Summe** über Zellen; für Belastungsstunden Summe der Personen-Stunden.
Index-Risiken (Unterversorgung, Ungleichheit) bleiben Screening und werden **von der
€-Summe ausgenommen** (sonst Doppelzählung mit Mortalität/Morbidität).

### 6.2 Gruppe MONETARY (17 Risiken)

Kern: **Average Annual Loss (AAL)** = Sachwert × Schadensgrad(Intensität) ×
Jahreswahrscheinlichkeit. Das ist die KWRA/versicherungsübliche EAD-Logik.

$$\text{AAL}_c = \text{assetval}_c \cdot \sum_{\text{RP}} \Delta p_{\text{RP}}\cdot d(\text{Intensität}_{\text{RP}})$$

`d(·)` = Depth-/Intensity-Damage-Kurve (0..1), `Δp_RP` = Wahrscheinlichkeitsmasse je
Wiederkehrperiode.

| Risiko | Sachwert / Exposition | Schadenskurve `d` | Quellenlage |
|---|---|---|---|
| EXPECTED_BUILDING_DAMAGE_EUR | Gebäudewert €/m² × Wohn-/BGF (Zensus) | Wassertiefe-/Wind-Schadenskurve | HOWAS21; GDV; JRC depth-damage; KOSTRA/HWGK |
| EXPECTED_TRANSPORT_DAMAGE_EUR | Ersatzwert Verkehrsassets (OSM-Netz) | Überflutungs-/Hitze-Schadensgrad | Prognos 2023; BASt |
| EXPECTED_ENERGY_INFRA_DAMAGE_EUR | Ersatzwert Energieassets (OSM KRITIS) | Sturm-/Flut-Schadensgrad | Prognos 2023; dena |
| EXPECTED_TELECOM_DAMAGE_EUR | Ersatzwert Telekom-Assets | Sturm-/Flut-Schadensgrad | Prognos 2023 |
| EXPECTED_WATER_WASTEWATER_DAMAGE_EUR | Ersatzwert Ver-/Entsorgung | Flut-/Dürre-Schadensgrad | Prognos 2023; DWA |
| EXPECTED_AGRICULTURAL_DAMAGE_EUR | Ertragswert €/ha (Landnutzung) | Ertragsverlust(Dürreindex/SMI) | Prognos 2023; UFZ Dürremonitor; StatBA Agrar |
| EXPECTED_SOIL_LOSS_DEGRADATION_EUR | Bodenwert €/ha × Erosionsfläche | Erosionsrate(Starkregen/Hang) | ESDAC; BGR; Prognos 2023 |
| EXPECTED_RESTORATION_COSTS_EUR | **NICHT eigenständig** — Anteil an Bau/Infra | `restaurierungsquote · Σ Sektorschäden` | — (Doppelzählung; als Teilkennzahl) |
| EXPECTED_ECOSYSTEM_SERVICE_LOSS | Ökosystemleistungswert €/ha/a × Fläche | Degradationsfraktion | TEEB-DE; BfN; Grunewald u. a. |
| EXPECTED_INDIRECT_ECONOMIC_LOSS_EUR | **Multiplikator** `k_indirekt · Σ direkte Sektorschäden` | `k_indirekt` (~0,18–0,5) | Prognos 2023 (I/O-Analyse) |
| EXPECTED_SUPPLY_SHORTAGE_COSTS_EUR | Teil des Indirekt-Multiplikators | in `k_indirekt` aufgehen lassen | Prognos 2023 |
| EXPECTED_CLIMATE_MIGRATION_COSTS_EUR | `migr_kosten · P_verdrängung · pop_expo` | €/verdrängter Person | Prognos 2023 (grob) |
| EXPECTED_LOCATION_DISADVANTAGE_EUR | Teil des Indirekt-Multiplikators | in `k_indirekt` | Prognos 2023 |
| EXPECTED_DELAYED_DAMAGE_COSTS_EUR | **Abgrenzungsproblem** — verzögerter Teil der Sektorschäden | als zeitl. Verteilung, nicht additiv | — |
| EXPECTED_FISHERIES_ECONOMIC_LOSS_EUR | Fischereiwert × Gewässerfläche | Verlust(Wärme/Niedrigwasser) | StatBA/BLE Fischerei; LfU |
| EXPECTED_AQUACULTURE_DAMAGE_EUR | Aquakulturwert × Fläche | Verlust(Wärme/Niedrigwasser) | BLE; Modellannahme |
| EXPECTED_TOTAL_DAMAGE_EAD_EUR | **= Σ aller obigen direkten + indirekten** | keine eigene HxVxE-Kette | Identität |

Zentrale Regel: **direkte Sektorschäden** werden über Schadensfunktionen einzeln
gerechnet; **indirekte/Folgeschäden** (indirekt, Versorgung, Standort, verzögert)
werden als **ein** Multiplikator `k_indirekt` auf die direkten Schäden konsolidiert,
statt als unabhängige additive Risiken (behebt Abschnitt 3.7). **EAD = Summe**,
kein eigenes Risiko.

### 6.3 Gruppe OPERATIONAL (11 Risiken)

Kern: **Erwartete jährliche Ausfallstunden** = Ereignisfrequenz × mittlere
Ausfalldauer / Redundanz. Monetarisierung über **Cost-of-Outage / Value of Lost Load**.

$$\text{Ausfallstd}_c = P_{\text{hazard}}\cdot \text{Basisdauer}\cdot \frac{g(\hat V_{\text{criticality}})}{1+\text{Redundanz}}$$

| Risiko | Exposition/Treiber | Kostensatz | Quellenlage |
|---|---|---|---|
| EXPECTED_CI_OUTAGE_HOURS | KRITIS-Assetdichte × Hazard-P | €/Ausfallstunde (aggregiert) | BBK KRITIS; dena |
| EXPECTED_ENERGY_OUTAGE_HOURS | Last (kW) × Ausfalldauer | VoLL €/kWh (~3–15) | dena; VDE; ENTSO-E |
| EXPECTED_WATER_SUPPLY_OUTAGE_HOURS | versorgte Ew. × Dauer | €/Person·h | DWA; BBK |
| EXPECTED_WASTEWATER_OUTAGE_HOURS | angeschlossene Ew. × Dauer | €/Person·h | DWA |
| EXPECTED_COMMUNICATION_OUTAGE_HOURS | versorgte Ew./Betriebe × Dauer | €/h | BNetzA; BBK |
| EXPECTED_TRANSPORT_DISRUPTION_HOURS | Verkehrsknoten × Dauer | €/h (Zeitkosten) | BASt; BVWP-Zeitkostensätze |
| EXPECTED_SUPPLY_CHAIN_DISRUPTION_HOURS | Industrie-/Logistikknoten × Dauer | €/h Wertschöpfung | Prognos 2023; StatBA |
| EXPECTED_ADMIN_OUTAGE_HOURS | Verwaltungsstellen × Dauer | €/h | BBK; kommunale Kennzahlen |
| EXPECTED_FUNCTIONAL_FAILURE_DURATION | Kaskaden-Kopplung × Dauer | €/h | BBK KRITIS |
| HYDROLOGICAL_STRESS_RISK_INDEX | **Index behalten** (Screening) | — | UFZ; BfG |
| SYSTEMIC_DOMINO_RISK_INDEX | **Index behalten** ODER Kaskaden-Multiplikator auf KRITIS | — | BBK; Netzwerk-Kaskadenmodelle |

Aggregation: Summe der (personen-/last-gewichteten) Ausfallstunden. Index-Risiken
bleiben Screening.

### 6.4 Gruppe ENVIRONMENT (11 Risiken)

Kern: **Physischer Verlust (ha/Arten) = exponierte Naturfläche × Verlustrate**,
Monetarisierung optional über Ökosystemleistungs-/Wiederherstellungswert.

| Risiko | Exposition | Verlustrate | Quellenlage |
|---|---|---|---|
| EXPECTED_BIODIVERSITY_LOSS | Biodiv.-Hotspot-/Waldfläche | Arten/ha·a (Wärme/Dürre/Feuer) | BfN; UBA; Rote Listen |
| EXPECTED_HABITAT_LOSS | Habitat-/Küstenfläche | ha/a (Dürre/Feuer/SLR) | BfN; BSH (SLR) |
| EXPECTED_SOIL_DEGRADATION | Erosionsanfällige Böden | ha/a | BGR; ESDAC |
| EXPECTED_VEGETATION_DAMAGE | Wald-/Agrarfläche | ha/a (Dürre/Feuer) | Waldzustandsbericht; DWD |
| EXPECTED_WATER_AIR_POLLUTION | **Index behalten** (Screening) | — | UBA |
| ECOSYSTEM_DEGRADATION_RISK_INDEX | **Index behalten** | — | BfN |
| ECOSYSTEM_FRAGMENTATION_RISK_INDEX | **Index behalten** | — | BfN |
| RESOURCE_CONFLICT_RISK_INDEX | **Index behalten** | — | KWRA 2021 (qualitativ) |
| ENVIRONMENTAL_FEEDBACK_RISK_INDEX | **Index behalten** | — | IPCC AR6 |
| FISHERIES_STOCK_STRESS_RISK_INDEX | **Index behalten** | — | LfU; ICES |
| LOW_WATER_FISHERIES_IMPACT_INDEX | **Index behalten** | — | BfG; LfU |

Monetarisierung der physischen Verluste (Arten/ha) über **Wiederherstellungs-/
Ökosystemleistungswert** (BfN/TEEB-DE) — als **eigener** €-Posten, der **nicht** mit
`EXPECTED_ECOSYSTEM_SERVICE_LOSS` (6.2) doppelt zählen darf (Abgrenzung: physischer
Flächenverlust vs. laufender Leistungsausfall — im `source_detail` dokumentieren).
Reine Index-Risiken (7 von 11) bleiben Screening und tragen 0 € bei — **bewusst**,
nicht als Lücke.

### 6.5 Aggregationsregeln Zelle → Kommune (Zusammenfassung)

- **Absolute Outcomes / €:** immer **Σ über Zellen** (jede Zelle mit ihrer eigenen
  Exposition, Hazard-Intensität, Vulnerabilität). Das ist die einzige konsistente
  Basis für Karte, Dashboard und Kostensumme (behebt Abschnitt 3.6).
- **Intensitäts-/Screening-Kennzahlen:** P90 und Max des HxVxE-Index je Risiko
  **zusätzlich** ausweisen (Handlungsdruck-Signal), aber **nie** mit Bevölkerung
  multipliziert als „Schaden" verkaufen.
- **Konzentrations-Kennzahl:** Anteil der Schadenssumme aus den Top-5 %-Zellen — macht
  den Oschatz-Fall (wenige heiße Zellen) im Dashboard sichtbar.
- **Gruppen-/Gesamt:** Gesamtschaden = Σ monetarisierte Einzelrisiken (ohne
  ausgenommene Index-Risiken, ohne EAD-Doppel, ohne Restaurierungs-Doppel).

### 6.6 Migrationsskizze & Weiterverwendbares

**Direkt weiterverwendbar (keine Neuentwicklung):**

- **Schicht A komplett**: `cell_risk_indices`, `build_pathways` (optional entdünnt),
  `normalize_value`/Overrides, alle H/E/V-Indikatoren, Karten, Radar, Maßnahmen-Logik.
- **Alle Rohdaten-Pipelines** (Zensus-pop/Alter, OSM-Assets, DWD, Terrain) — sie
  liefern bereits die **absoluten** Expositionen, die Schicht B braucht.
- **`ref_value` + `scale`** werden zu **nationalen Kalibrier-/Sanity-Ankern**
  (Plausibilitätsprüfung der Schadensfunktionen gegen Prognos-Größenordnungen), nicht
  mehr als primärer Rechenweg.
- **`cost_per_outcome_eur`** (VSL etc.) → wird zu explizitem Registry-Parameter
  (Voraussetzung ohnehin für Prompt 3).

**Neu zu bauen:**

- Pro Risiko eine `impact_function` (Modul `engine/impact/*`) nach den Mustern 6.1–6.4.
- Hazard-Wahrscheinlichkeits-/Intensitäts-Inputs: KOSTRA-DWD (Starkregen), HWGK
  (Hochwassergefahrenkarten), Ereignisfrequenzen (Sturm/ERA5), UFZ-SMI (Dürre).
- Sachwert-/Expositions-Layer: Gebäude-/Assetwert €/m² bzw. €/Einheit,
  Ökosystemleistungswert €/ha.
- `k_indirekt`-Multiplikator statt der 4–5 unabhängigen Folgekosten-Risiken.
- Aggregation auf **Summe** umstellen (`aggregate`), P90/Max als Zusatzfelder.

**Aufwand:** L–XL (deckt sich mit Prompt 3 „Monetarisierung" + Prompt 7 „Dashboard
ehrlich"). Schicht B kann **risikogruppen-weise** ausgerollt werden (erst monetary +
health, dann operational + environment), weil jede Gruppe ein eigenes, klar
abgegrenztes Formelwerk hat.

### 6.7 Umsetzungsstand (Prompt 3 „Modell-Umbau", gestufter Rollout)

Stand Juli 2026, in committeten Stufen (Details siehe `git log` / Commit-Messages):

- **Stufe 1 — Schicht A entdünnt (erledigt):** Index = `100·max(w·Ĥ·Ê·V̂)` statt
  gewichtetem Mittel (Pfadzahl-Invarianz, §3.1/3.5); Wirkungsketten **kuratiert** und
  belegt (KWRA 2021 / GIZ Vulnerability Sourcebook), Begründung je Kette im Info-Fenster.
- **Stufe 2 — echte Hazard-Daten, Teil 1 (erledigt):** `heavy_rain_index` aus echten
  DWD-CDC-Starkregenrastern (Tage/Jahr ≥ 20/30 mm) statt des Mitteltemperatur-Proxys;
  Provenienz je Treiber protokolliert (`build_regional_context["provenance"]`).
- **Stufe 3 — Impact-Framework + Σ-Aggregation (erledigt):** Neues Paket
  `engine/impact/` (per-Risk-Dispatch; ab Stufe 4 registrierte Schadensfunktionen, sonst
  `legacy_cell_impact` = bisheriger linearer Weg). Der Runner **materialisiert je Zelle**
  `{index, outcome, cost_eur}`; `aggregate` bildet für pop-/area-Risiken die **Summe der
  Zell-Outcomes** (behebt den Karte↔Dashboard-Widerspruch §3.6), `flat`-Risiken
  (Ausfallstunden, Index-Screening) bleiben P90-basiert. Neue Aggregat-Felder
  `p90_index`, `outcome_sum`, `aggregation`, `top5_share`, `area_km2_affected`,
  `share_above_threshold` (auch für Prompt 7). Behebt zugleich den 0-Spalten-Bug im
  GeoPackage-Export (`outcome`/`cost_eur` je Zelle jetzt gefüllt). Robuster Fallback für
  Alt-Zelldaten ohne materialisierten Outcome (Neuberechnung je Zelle). Die eigentlichen
  Schadensfunktionen (§6.1–6.4) und die `k_indirekt`-Konsolidierung folgen in Stufe 4/5.
- **Stufe 4a — Gesundheits-Schadensfunktionen (erledigt):** Die 7 Gesundheitsrisiken
  (§6.1) rechnen jetzt ``Betroffene · Rate · Dosis-Wirkung · g(V̂)`` je Zelle statt
  ``ref·Index/100``. Hitzegetrieben über die nichtlineare attributable Fraktion
  ``AF(Hitzetage)`` (überproportional durch die Schwelle — behebt §3.4), ereignis-
  getrieben über die normierte Flut-/Sturmintensität. Alle Raten/Koeffizienten sind
  editierbare, quellenbelegte Registry-Parameter (``risks.<CODE>.impact.*``; RKI/
  Winklmayr 2022, UBA MK3.1, BBK, Prognos). ``ref_value`` ist nur noch Kalibrier-/
  Sanity-Anker (``impact/sanity.py`` prüft die Größenordnung). Monetäre + operative +
  Umwelt-Schadensfunktionen und ``k_indirekt`` folgen in Stufe 4b/5.
- **Stufe 4b — Monetäre Schadensfunktionen + k_indirekt (erledigt):** Die 10 direkten
  Sektorschäden (§6.2) rechnen ``Assetwert · Jahresverlustrate · Schadenskurve(Intensität)
  · g(V̂)`` je Zelle; der Assetwert kommt aus realen Zell-Rohgrößen (Gebäudegeschossfläche,
  Infrastruktur-Anzahl, Agrar-/Wald-/Gewässerfläche) × editierbaren €-Parametern statt aus
  ``ref_value``. Die Schadenskurve ist konvex (Exponent > 1). **k_indirekt-Konsolidierung
  (behebt §3.7):** indirekte Verluste = ``k·Σ direkte Sektorschäden``; Versorgungsengpass/
  Standortnachteil/verzögerte Schäden = 0 (darin enthalten); Restaurierung =
  ``quote·Σ direkt`` als **nicht-additive** Teilkennzahl (``NON_ADDITIVE_RISK_CODES``, aus
  ``total_eur`` ausgenommen). Klimamigration eigenständig. 11 globale + 11 per-Risiko-
  Parameter (``impact.*`` / ``risks.<CODE>.impact.max_loss_rate``), editierbar, mit
  Prognos-/TEEB-/GDV-Quellen. Rest offen (Stufe 5): operative (VoLL-Ausfallstunden) und
  Umwelt-Flächen-Schadensfunktionen, ERA5-Sturmintensität. Die exakte JRC-Tiefe-Schaden-
  Kurve (Wassertiefe je Wiederkehrperiode) bleibt spätere Verfeinerung (braucht rasterio +
  DE-Ausschnitt-Download); Stand 4b treibt die real vorhandene normierte Hazard-Intensität
  die Schadenskurve.
- **Nach Schicht B verschoben (Stufe 3+, weil erst dort konsumiert):** die
  intensitäts-/wahrscheinlichkeitsbasierten Hazard-Datensätze
  KOSTRA-DWD (Bemessungsniederschlag), **JRC River Flood Hazard Maps** (EU-weite
  Hochwassertiefe je Wiederkehrperiode — ersetzt 16 Länder-HWGK), **UFZ-Dürremonitor
  SMI** (Bodenfeuchte/Dürre) und **ERA5-Sturmbö-Frequenz** (`storm_days`). Diese speisen
  die Schadensfunktionen (§6.1–6.4) und wären ohne deren Konsumenten ungenutzter,
  untestbarer Code.

  **Korrektur zur Datenlage ERA5/CDS:** ERA5 aus dem Copernicus Climate Data Store ist
  **kostenlos und kommerziell nutzbar** — seit 2. Juli 2025 unter **CC-BY 4.0**
  (Namensnennung), Zugang über ein **kostenloses** CDS-Konto + API-Key. Es ist damit
  **nicht** ausgeschlossen, sondern nur (wie KOSTRA/JRC/SMI) auf die Schicht-B-Stufe
  verschoben; einzige Voraussetzung ist ein vom Betreiber anzulegender (kostenloser)
  CDS-API-Key. `storm_days` bleibt bis dahin eine dokumentierte regionale Konstante.

---

## 7. Entscheidungsvorlage (Product Owner)

Bitte **eine** Option ankreuzen (Empfehlung markiert).

- [ ] **Option A — Status quo behalten.** Aufwand: **—**. Konsequenz: Modell bleibt
      angreifbar (P90×pop als „Schaden", EAD-Doppelzählung, Karte↔Dashboard-Widerspruch,
      Score hängt von Pfadanzahl ab). **Nicht empfohlen** — die Absolutwerte sind nicht
      verteidigbar.

- [ ] **Option B — Minimal-Reparatur ohne Schichtentrennung.** Aufwand: **S–M**.
      Nur: EAD aus Summe nehmen, Kostensätze als Parameter, Aggregation Karte=Dashboard
      angleichen. Konsequenz: behebt Doppelzählung und Inkonsistenz, aber
      **Linearitäts- und Pfad-Artefakt-Fehler bleiben** — Absolutwerte weiterhin nur
      grobe Indikatoren.

- [X] **Option C — Zwei-Schichten-Architektur (EMPFOHLEN).** Aufwand: **L–XL**
      (gruppenweise ausrollbar). HxVxE bleibt Screening; neue Schadensfunktions-Schicht
      für Absolutwerte (Abschnitt 6); Gesamtschaden = Summe. Konsequenz: KWRA-konform
      **und** methodisch belastbare, monetarisierbare Werte je Kommune; Karte, Dashboard
      und Kostensumme aus einer Quelle. Höchster Aufwand, einziger Weg zu verteidigbaren
      Absolutzahlen.

- [ ] **Option D — Nur Screening ausweisen, Absolutwerte streichen.** Aufwand: **S**.
      HxVxE-Index + Ranking behalten, keine Tote/€ mehr ausweisen. Konsequenz:
      voll KWRA-konform und ehrlich, aber die vom PO gewünschte Monetarisierung entfällt.
      Fallback, falls L-/XL-Aufwand nicht tragbar.

- [ ] **Option C-stufig — C als Zielbild, B als Sofortmaßnahme.** Aufwand: **S jetzt,
      L später**. Zuerst B (Doppelzählung/Konsistenz raus), dann Schicht B gruppenweise
      nachziehen. **Pragmatische Empfehlung**, wenn nicht sofort volle Kapazität da ist.

Nachfolgende Prompts (3 „Modell-Umbau/Monetarisierung", 7 „Dashboard ehrlich") setzen
bei **Option C / C-stufig** direkt auf Abschnitt 5–6 auf: Kostensätze als Parameter
(6.1–6.4), EAD als Summe (6.2), Aggregation auf Σ-Zell-Outcomes + P90/Max/Top-5 %
(6.5), Indirekt-Multiplikator statt Einzelrisiken (6.2).
