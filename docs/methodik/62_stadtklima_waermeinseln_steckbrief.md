# Methodik-Steckbrief #62 — Stadtklima / Wärmeinseln

Screening-Steckbrief zur KWRA-Klimawirkung Id 62 · 18.09.2026 · Gliederung nach Kapitel 3 des
M1-Zuschnitts (Firmen-Repo, `dokumente/produkt/m1-zuschnitt.md`) · Belegbasis:
`docs/evidenz/62_steckbrief_quellen.md`.

> **Was dieser Steckbrief ist — und was nicht.** Er beschreibt die Klimawirkung 62 auf der
> Screening-Ebene: amtliche Einordnung, qualitative Wirkungskette und das, was der Rechenkern von
> KAP2 heute je 100-m-Zelle ausrechnet. Er enthält **keine** Schadensfunktion, **keine**
> Kalibrierung, **keine** Schadenskonten K1 bis K8, **keine** Beträge und **keinen**
> Kosten-Nutzen-Vergleich. Die Trennlinie ist bewusst gezogen: Id 62 ist in der Monetarisierungs-
> Arbeitsmappe als rein vorgelagerte Wirkung geführt, die selbst nichts bucht, sondern über die
> nachgelagerten Wirkungen 95, 65 und 87 wirkt (`docs/evidenz/62_steckbrief_quellen.md`,
> Kanten-Tabelle, Zeile „Risiken-Monetarisierung Z67“). Eine eigene Bepreisung wäre dort
> ausdrücklich eine Doppelzählung.
>
> **Lesbarkeit ist Abnahmegegenstand** (Vorgabe P3, Anweisung A-0034). Dieser Steckbrief benutzt
> keine Verteilungsfunktionen und keine Formeln, die über Multiplikation, Maximum und Perzentil
> hinausgehen. Jede Rechenaussage in Abschnitt 3 ist in einem Satz erklärt und mit der Codestelle
> belegt, an der sie steht.

## 1 Kopf

| Feld | Eintrag | Herkunft |
|---|---|---|
| Amtlicher Name (KWRA 2021) | **Stadtklima / Wärmeinseln** | `KWRA-Schadensbaum_X_UBA-klimawirkungsketten.xlsx`, Blatt „Schadensbaum-Netzwerkliste“, Zeile 63 |
| Nummer | **62** (Netzwerkliste-Id) | ebd., Zeile 63 |
| Kennung im Wirkungsketten-Blatt | **W124** („Stadtklima/Wärmeinseln“) | ebd., Blatt „Klimawirkungsketten“, Zeile 279 |
| Dringlichkeitseinstufung | **SD — sehr dringendes Handlungserfordernis** | KWRA 2021, Teilbericht 6, Tabelle 25; im Repo geführt in `docs/KATALOG_KRITIK.md`, Anhang A, Zeile „62 Stadtklima / Wärmeinseln … SD“ |
| Handlungsfeld (KWRA) | **Bauwesen** | `docs/KATALOG_KRITIK.md`, Anhang A (Spalte HF „Bau“); deckungsgleich mit `kwra_field: "Bauwesen"` in `backend/app/data/catalog.py`, `PLANNED_RISKS`, Zeile 318 |
| Betroffenes Handlungsfeld der Wirkungsseite | **Menschliche Gesundheit** | Klimawirkungsketten, Zeile 279, Spalte `Zu_Handlungsfelder` |
| KAnG-Cluster (Sekundär-Tag) | **Infrastruktur**, Handlungsfeld **Gebäude** | `backend/app/data/catalog.py`, `KANG_CLUSTERS` (Cluster `infrastructure` mit Feld `buildings`); Zuordnung über das KWRA-Handlungsfeld Bauwesen |
| Zweitnennung im KAnG | Wärmeinsel-Effekt ist im **Berücksichtigungsgebot § 8 Abs. 1 KAnG** ausdrücklich benannt | `docs/KATALOG_KRITIK.md`, Abschnitt zu § 8 Abs. 1 Nr. 1–4 |
| Status im Produkt | geplant, **Stufe 1**; im Katalog als gesperrte Klimawirkung sichtbar, nicht als eigenes Risiko gerechnet | `backend/app/data/catalog.py`, `PLANNED_RISKS`, Zeilen 317–322 (`stage: 1`) |

**Warum die Klimawirkung für eine Kommune zählt.** Die Wärmeinsel ist der einzige Teil der
Hitzebelastung, den eine Kommune mit ihren eigenen Instrumenten unmittelbar beeinflusst: mit
Bebauungsplan, Versiegelungsgrad, Grün- und Baumbestand, Gebäudestellung und Freiflächen. Die
Gefahr selbst — Hitze und Sonnenscheindauer — ist nicht steuerbar; der Aufschlag, den eine Stadt
gegenüber ihrem Umland erzeugt, ist es. Deshalb steht die Klimawirkung im KAnG mit eigenem Namen
und trägt in der KWRA die höchste Dringlichkeitsstufe.

**Zwei Namensräume, ein Gegenstand.** Die Nummer 62 bezeichnet in der Netzwerkliste dieselbe
Klimawirkung wie `W124` im Wirkungsketten-Blatt. Dieser Steckbrief benutzt durchgehend die
Nummer 62; die `W`-Kennungen erscheinen nur dort, wo eine Kante direkt aus dem
Wirkungsketten-Blatt zitiert wird.

## 2 Wirkungskette

Die Kette wird qualitativ geführt: **Gefahr → Exposition → betroffenes Schutzgut**. Jede Kante
trägt eine Quelle aus dem Quellenblatt `docs/evidenz/62_steckbrief_quellen.md`; eine Kante ohne
Beleg steht hier nicht. Die Zeilenangaben sind die Excel-Zeilennummern der jeweiligen
Arbeitsmappenblätter, so wie das Quellenblatt sie führt.

### 2.1 Gefahrenseite (Eingang)

| Kante | Beleg im Quellenblatt |
|---|---|
| Hitze (E02) → Stadtklima / Wärmeinseln | Klimawirkungsketten Z279, Spalte `Input_IDs_Einflüsse` = „E02; E19“ |
| Sonnenscheindauer (E19) → Stadtklima / Wärmeinseln | Klimawirkungsketten Z279, zweiter Einfluss derselben Zelle |
| Vegetation in Siedlungen (W124 ← W127, entspricht Klimawirkung 61) → Stadtklima / Wärmeinseln | Klimawirkungsketten Z279, Spalte `Input_IDs_Wirkung` = „W127“ |

Die dritte Kante ist keine Gefahr im engeren Sinn, sondern eine **vorgelagerte Klimawirkung**: Der
Zustand der Siedlungsvegetation entscheidet mit, wie stark dieselbe Hitze sich im Stadtkörper
aufstaut. Die Arbeitsmappe führt sie als eigene Eingangskante, deshalb steht sie auch hier auf der
Eingangsseite und nicht bei den Einflussgrößen der Sensitivität.

### 2.2 Expositionsseite (worauf die Gefahr trifft)

| Kante | Beleg im Quellenblatt |
|---|---|
| Vorkommen von Bau- und Immobilienunternehmen (R23) → Stadtklima / Wärmeinseln | Klimawirkungsketten Z279, Spalte `Input_IDs_Räumlich` = „R23; R24; R25“ |
| Vorkommen von Gebäuden (R24) → Stadtklima / Wärmeinseln | Klimawirkungsketten Z279, zweite Exposition derselben Zelle |
| Vorkommen von Siedlungsinfrastrukturen (R25) → Stadtklima / Wärmeinseln | Klimawirkungsketten Z279, dritte Exposition derselben Zelle |

Die drei Expositionsgrößen beschreiben denselben Sachverhalt aus drei Blickwinkeln: bebauter,
versiegelter, technisch überprägter Raum. Wo er dicht ist, entsteht die Wärmeinsel; wo er dünn
ist, bleibt der Aufschlag klein.

### 2.3 Wirkungsseite (betroffenes Schutzgut und Weitergabe)

| Kante | Beleg im Quellenblatt |
|---|---|
| Stadtklima / Wärmeinseln → Handlungsfeld **Menschliche Gesundheit** | Klimawirkungsketten Z279, Spalte `Zu_Handlungsfelder` = „Menschliche Gesundheit“ |
| Stadtklima / Wärmeinseln → Klimawirkung 95 „Hitzebelastung“ | Netzwerkliste Z63, Spalte `Output_IDs_Wirkung` = „95; 65; 87“ |
| Stadtklima / Wärmeinseln → Klimawirkung 65 „Bedarf an Kühlenergie“ | Netzwerkliste Z63, dieselbe Zelle |
| Stadtklima / Wärmeinseln → Klimawirkung 87 „Leistungseinbußen von Beschäftigten“ | Netzwerkliste Z63, dieselbe Zelle |
| Stadtklima / Wärmeinseln bucht selbst nichts, wirkt nur als Übertragungskanal | Risiken-Monetarisierung Z67, Spalte „Rolle in der Monetarisierung“ = „Rein vorgelagert“; „Wirkt über / bucht in“ = „→ 95, 65, 87“ |

**Lesart der Kette in einem Satz.** Hitze und Sonneneinstrahlung treffen auf dichten, versiegelten
Siedlungsraum mit knapper Vegetation; daraus entsteht ein lokaler Temperaturaufschlag, der nicht
selbst bewertet wird, sondern die Gesundheitsbelastung (95), den Kühlenergiebedarf (65) und die
Leistungsfähigkeit Beschäftigter (87) verstärkt.

### 2.4 Sensitivitäten und ein offener Punkt aus dem Quellenblatt

Die Arbeitsmappe nennt in Zeile 279 sieben Sensitivitäten: S094 Verwendete Baumaterialien auf
Gebäudeebene, S095 Begrünung von Gebäuden, S096 Bauliche, organisatorische und finanzielle
Vorsorge der öffentlichen Hand, S097 Zustand von (Schutz-)Infrastrukturen, S098 Verwendete
Baumaterialien von (Schutz-)Infrastrukturen, S099 Begrünung von Städten und Siedlungen, S100 Grad
der Versiegelung.

`backend/app/data/catalog.py` führt zu Id 62 hingegen nur zwei davon (S099, S100). Nach Eiserner
Regel 5 (`CLAUDE.md`) gilt die Arbeitsmappe, und die Abweichung wird nicht still im Code gelöst:
Sie ist im Quellenblatt als eigene Kanten-Zeile vermerkt und hier als **offener Befund** notiert.
Dieser Steckbrief ändert dazu nichts am Code.

## 3 Screening-Ergebnis

Dieser Abschnitt beschreibt ausschließlich, was der bestehende Rechenkern **heute** liefert —
nachgelesen in `backend/app/services/engine/risk_engine.py`, `…/engine/indicators.py`,
`…/engine/inputs.py`, `backend/app/services/grid_service.py` und
`backend/app/services/projection_service.py`. Was dort nicht steht, steht auch hier nicht.

### 3.1 Die Rechenfläche: 100-Meter-Zellen

Grundlage jeder Bewertung ist das amtliche 100-m-Gitter des Zensus. `grid_service.generate_grid`
erzeugt für eine Kommune alle Zellen, die ihr Gemeindegebiet schneiden: Kantenlänge genau 100
Meter, ausgerichtet im europäischen Bezugssystem EPSG:3035 (deshalb deckungsgleich mit dem
Destatis- und BKG-Zensusgitter), gespeichert zusätzlich in EPSG:4326 für die Kartendarstellung.
Jede Zelle trägt die INSPIRE-Gitterkennung der Form `CRS3035RES100mN<Nordwert>E<Ostwert>`. Eine
andere Kantenlänge lässt der Dienst nicht zu; er bricht mit einem Hinweis ab.

Damit ist die kleinste Aussageeinheit des Screenings ein Hektar Stadtfläche — fein genug, um
Quartiere zu unterscheiden, grob genug, um mit bundesweit einheitlichen Daten befüllbar zu bleiben.

### 3.2 Die Rechnung je Zelle: Gefährdung mal Exposition mal Vulnerabilität

Für jede Zelle werden drei Gruppen von Kennzahlen bestimmt: **Gefährdung** (H), **Exposition** (E)
und **Vulnerabilität** (V). Sie stehen zunächst in ihren natürlichen Einheiten oder als Punktwert
zwischen 0 und 100 (`indicators.py`) und werden anschließend auf die Spanne 0 bis 1 normiert
(`risk_engine.normalize_hev`).

Eine **Wirkungskette** ist ein Tripel aus je einer Gefährdung, einer Exposition und einer
Vulnerabilität — also genau die Struktur aus Abschnitt 2. Für jede Kette wird gerechnet:

```
Kettenwert = Gewicht × Gefährdung × Exposition × Vulnerabilität        (alle drei zwischen 0 und 1)
```

Das **Gewicht** dämpft Nebenketten gegenüber der Hauptkette (`catalog.PATHWAY_WEIGHTS`): Hauptkette
1,00; gleichgerichtete Kette 0,85; alternative Gefahr 0,75; alternative Exposition beziehungsweise
alternative Vulnerabilität 0,70; verbundene Ketten 0,65 bis 0,50.

Der **Index der Zelle** ist der größte Kettenwert, mit 100 multipliziert und bei 100 gedeckelt:

```
Index (0 bis 100) = 100 × größter Kettenwert der Zelle
```

Zwei Eigenschaften dieser Rechnung sind für das Verständnis wichtig und im Code ausdrücklich so
begründet (`risk_engine.py`, Modulkopf):

- **Multiplikation statt Addition.** Fehlt einer der drei Faktoren, ist das Ergebnis null. Wo keine
  Gefahr herrscht, kein Mensch und kein Gebäude exponiert ist oder keine Empfindlichkeit besteht,
  gibt es kein Risiko. Das ist die Regel der DIN-EN-ISO-14091-Systematik, und sie ist bewusst
  streng.
- **Maximum statt Mittelwert über die Ketten.** Der Index ist die stärkste einzelne Wirkungskette.
  Beim Mittelwert hinge die Höhe davon ab, wie viele Nebenketten jemand modelliert hat — mehr
  Ketten hätten das Signal verdünnt. Das Maximum ist gegen die Kettenzahl unempfindlich.

Der Index ist eine **relative Vergleichsgröße** zwischen Zellen, Risiken und Kommunen, keine
physikalische Größe und keine Häufigkeit. Er sagt: hier ist die Belastung höher als dort.

### 3.3 Wo die Wärmeinsel heute in die Rechnung eingeht

Id 62 ist im Produkt als geplante Klimawirkung geführt (`PLANNED_RISKS`, Stufe 1) und hat **heute
kein eigenes Risiko im Rechenkern**: keinen eigenen Index, keine eigene Kette, keinen eigenen
Eintrag in den aktiven Risiken. Sichtbar ist sie im Katalog als gesperrter Eintrag.

Gerechnet wird die Wärmeinsel gleichwohl — als Kennzahl innerhalb der aktiven Hitze-Risiken:

| Kennzahl | Was sie je Zelle misst | Codestelle |
|---|---|---|
| `UHI_INTENSITY` | Wärmeinsel-Aufschlag in Kelvin gegenüber dem Umland, als 24-Stunden-Mittel aus Tag- und Nachtanteil | `indicators.py` (Zuweisung `"UHI_INTENSITY": round(uhi, 2)`), berechnet in `inputs.compute_uhi_components` / `compute_uhi_delta` |
| `SEALING_DEGREE` | Versiegelungsgrad der Zelle, 0 bis 100 | `indicators.py`; Formelzeile in `formulas.py` |
| `GREEN_SPACE_SHARE` | Mangel an Grünfläche (invers: hoch bedeutet wenig Grün), 0 bis 100 | `indicators.py` / `formulas.py` |
| `HEAT_SENSITIVITY` | Hitzeempfindlichkeit der Bevölkerung, erhöht um den Wärmeinsel-Aufschlag und um fehlendes Grün | `indicators.py` |

Der Wärmeinsel-Aufschlag selbst entsteht aus OSM-Landnutzung und Gebäudedaten der Zelle:
Versiegelung und Rückstrahlvermögen der Oberfläche, Gebäudeanteil und Gebäudehöhe, Enge der
Straßenräume, kühlende Wirkung von Wald, Wiese, Ackerfläche, Gewässern und Baumkronen, gedämpft
durch die Durchlüftungslage. Alle Koeffizienten dieser Rechnung sind übersteuerbare
Registry-Parameter (`uhi.alpha` bis `uhi.tree_cooling`, `parameter_registry.py`) und keine im
Code versteckten Zahlen — jede trägt dort Herkunft und Begründung.

Das Screening-Ergebnis zu 62 ist damit heute die Zellkarte des Wärmeinsel-Aufschlags und der
Index der Hitze-Risiken, in die er eingeht — nicht ein eigener Index „62“.

### 3.4 Aggregation: von der Zelle zur Gesamtaussage

Die Zellwerte werden je Risiko zum **90. Perzentil** zusammengefasst
(`risk_engine.AGGREGATION_PERCENTILE = 90.0`, ausgewiesen als `"aggregation": "P90"`). Gemeint ist:
Man sortiert alle Zellwerte der Rolle nach und liest den Wert ab, den nur ein Zehntel der Zellen
übertrifft. Der Mittelwert wäre hier irreführend — eine Stadt mit zwei überhitzten Quartieren und
viel Flur käme rechnerisch harmlos heraus. Zusätzlich gilt ein **Expositions-Gate**: Zellen ohne
die für das Risiko einschlägige Exposition gehen nicht in das Perzentil ein, sonst zögen unbewohnte
Flächen das Ergebnis gegen null.

**Abweichung, ausdrücklich benannt (Eiserne Regel 5).** Die Produktbeschreibung in `README.md`
nennt als räumliche Ausgabeebene den **Ortsteil**. Im Rechenkern gibt es diese Ebene heute nicht:
Aggregiert wird von der 100-m-Zelle auf die **Kommune**; unterhalb der Kommune ist die Zelle selbst
die Ausgabeebene (Kartenlayer je Zelle, `cell_outcome`). Eine Ortsteil- oder Stadtteilgeometrie
kommt in `backend/app/services/` nicht vor. Diese Divergenz zwischen Beschreibung und Code wird
hier als Befund festgehalten und **nicht** still im Code aufgelöst.

### 3.5 Projektion: RCP 4.5 und RCP 8.5

`projection_service.project_group_risks` schreibt die heutigen Risikoindizes je Gefahrengruppe über
die Jahresreihe der Klimaprojektion fort, für die beiden Szenarien **RCP 4.5** (mittlerer
Emissionspfad) und **RCP 8.5** (hoher Emissionspfad). Die Rechnung ist bewusst einfach gehalten:

```
Index im Jahr X  =  heutiger Index  ×  Klimasignal-Faktor des Jahres X   (gedeckelt bei 100)
```

Der Faktor ist auf das Startjahr normiert, beginnt also bei 1,0. Er wird auf zwei Wegen bestimmt:

- **Gefahrengruppe Hitze** — über die Expositions-Wirkungs-Kurve: Die projizierte Erwärmung wird auf
  die bevölkerungsgewichtete Sommertemperatur aufgeschlagen und die Wirkungskurve neu ausgewertet;
  der Faktor ist das Verhältnis des neuen zum heutigen Kurvenwert. Grund: Die Kurve steigt oberhalb
  der Wirkschwelle überproportional an, eine lineare Fortschreibung mit der Zahl der Hitzetage
  unterschätzt die Zukunft systematisch.
- **Alle übrigen Gruppen** — über den Trend der Hitzetage als übergreifendes Klimasignal, weil für
  Starkregen und Sturm keine belastbare regionalisierte Projektionsreihe vorliegt. Diese
  Vereinfachung ist im Code als solche dokumentiert und wird hier nicht schöner dargestellt, als
  sie ist.

Datengrundlage ist das DWD-Angebot KlimaFolgenOnline, regionalisiert auf das Bundesland; die
Kurvenparameter stammen aus der RKI-/Winklmayr-Auswertung. Die Projektion wirkt auf die
Gruppenebene, nicht auf einzelne Zellen: Die räumliche Verteilung von heute wird als konstant
angenommen — eine Modellgrenze, die für die Wärmeinsel besonders zu beachten ist, weil bauliche
Veränderungen das Muster verschieben können.

### 3.6 Was ein Screening-Ergebnis zu 62 aussagen kann

Zusammengefasst liefert der Rechenkern heute für die Klimawirkung 62 drei prüfbare Aussagen:
erstens den Wärmeinsel-Aufschlag je Hektar als Karte, zweitens dessen Beitrag zum Hitze-Risikoindex
der Kommune auf der Skala 0 bis 100, drittens die Fortschreibung dieses Index unter den Szenarien
RCP 4.5 und RCP 8.5. Was der Rechenkern hierzu **nicht** liefert, ist eine eigene Schadensgröße:
Die Klimawirkung 62 ist nach der Monetarisierungs-Arbeitsmappe rein vorgelagert und gibt ihre
Wirkung an 95, 65 und 87 weiter (Abschnitt 2.3).

## 4 Was die Kommune daraus ablesen kann

Die Zellkarte zeigt, in welchen Quartieren sich die Stadt gegenüber ihrem Umland am stärksten
aufheizt und wie stark dieser Aufschlag zum Hitze-Risikoindex der Kommune beiträgt. Eine Kommune
liest daraus ab, wo Verschattung, Entsiegelung und Begrünung zuerst wirken, weil dort die
Ausgangsbelastung am höchsten ist — etwa in dem Sinn: „Diese vier Ortsteile tragen die höchste
Wärmelast; Verschattung und Entsiegelung wirken dort am stärksten.“ Die Karte liefert eine
Rangfolge der Flächen für die Maßnahmenplanung, keinen Schadensbetrag und keine Zahl betroffener
Personen.

## 5 Warum hier kein Betrag steht

Diese Klimawirkung ist ein Screening ohne Euro-Bezifferung — niemals 0 Euro und niemals leer. Der
Rechenkern zeigt, wo die Wärmeinsel am stärksten wirkt, bucht dafür aber bewusst keinen eigenen
Betrag: Nach der Monetarisierungs-Arbeitsmappe ist die Klimawirkung 62 rein vorgelagert und gibt
ihre Wirkung ausschließlich an die nachgelagerten Klimawirkungen Hitzebelastung (95),
Kühlenergiebedarf (65) und Leistungseinbußen von Beschäftigten (87) weiter; eine eigene Bepreisung
wäre dort ausdrücklich eine Doppelzählung (Abschnitt 2.3, Quellenblatt Zeile 67, Regel R2).

Fehlende Groesse der Kernformel: Preis
Diese Datenlage wuerde sie liefern: ein eigener, doppelzählungsfreier Kostensatz für Id 62 in der
Monetarisierungs-Arbeitsmappe „Risiken-Monetarisierung“ — dort steht dazu heute ausdrücklich „—“
(kein Kostensatz, da rein vorgelagert ohne eigene Buchung; `docs/evidenz/62_steckbrief_quellen.md`,
Abschnitt Parameter). Aus dem Screening wird kein Euro-Wert per Analogie zu anderen Klimawirkungen
hochgerechnet, auch nicht als Spanne.

## 6 Massnahme

<!-- Inhalt aus dem Folge-Teilpaket zu T-0405 dieses Vorhabens (T-0357). -->

## 7 Parameter und Quellen

<!-- Inhalt aus dem Folge-Teilpaket zu T-0405 dieses Vorhabens (T-0357). -->
