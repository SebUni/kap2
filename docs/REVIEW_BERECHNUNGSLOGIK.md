# Review der Berechnungslogik — Wirkungsmechanismen Schicht für Schicht

> **Zweck.** Tiefen-Review der **tatsächlichen Rechen-Mathematik** der Risiko-Engine,
> Schicht für Schicht von den Rohdaten bis zum Risiko, für **beide Ausgabeketten**:
> den dimensionslosen **KWRA-Index (0–100)** und den **monetären Schadenswert (€)**.
> Dies ist die Umsetzungsgrundlage für spätere Verbesserungen — **noch nicht umgesetzt**,
> außer echten Bugs (die sofort gefixt und hier mit Vorher/Nachher dokumentiert werden).
>
> **Abgrenzung.** Ergänzt die bestehende `REVIEW_WIRKUNGSMECHANISMEN.md` (dort:
> Quellen/Provenance/Differenzierung) und `MODELL_KRITIK.md` (Modellannahmen/§-Historie).
> Dieses Dokument prüft die **Formeln selbst**: Koeffizienten, Einheiten, Skalierung,
> Doppelzählungen, tote Terme, Formel↔Code-Divergenzen.
>
> **Format (verbindlich).** Für **jeden einzelnen kartierbaren Layer** (jeden H/E/V/R-
> und Sonstige-Code) ein **eigenes Unterkapitel** mit vier Blöcken:
> **Was** — 2–3 Sätze, fachlich erklärt (was bedeutet die Größe, wozu); **Wie** — die
> vollständige Rechenkette **ab der Quelle, Operator für Operator** (nicht nur „Min–Max"
> o. Ä.); **Review** — ist das fachlich/mathematisch gut so?; **Verbesserung** — konkret,
> nur kostenlose Quellen. Keine Tabellen für die Layer selbst (zu grob).
>
> **Verbesserungen nur mit kostenlosen Quellen.** Bei jeder Schwäche wird zusätzlich
> geprüft, ob (a) bereits geladene, aber **ungenutzte Felder** vorhandener Quellen
> (OSM/DWD/Zensus/INKAR/Terrain/PEGELONLINE/ERA5) den Wert verbessern könnten oder
> (b) aktuelle Elemente fachlich unpassend sind.
>
> **Legende Review:** ✅ tragfähig · 🟡 klein (Kosmetik/Redundanz) · 🟠 wichtig
> (verzerrt/irreführend/kaum differenzierend) · 🔴 kritisch (falsches Ergebnis) ·
> 🐞 Bug (sofort gefixt).

---

## Architektur in einem Bild (beide Ketten)

```
inputs.gather_cell_inputs → ci (Rohgrößen je Zelle) + regional (Kommune-Kontext)
   │
   ├─ auxiliary.build_auxiliary(ci, regional) ─────────────► SONSTIGE (Spiegel, Sackgasse)
   │                                                          (fließt NICHT in Formeln zurück)
   ▼
indicators.compute_cell_hev(ci, regional) → H, E, V  (absolute Einheiten)
   │
   ├─► risk_engine.normalize_hev → Ĥ, Ê, V̂ ∈ [0,1]
   │        └─► cell_risk_indices:  Index = 100·max_p( w_p·Ĥ_p·Ê_p·V̂_p )   ── KETTE 1
   │                └─► aggregate: P90 / Belastungs-P90 je Risiko, Gruppen-Mittel
   │
   └─► CellContext → impact.compute_all_cell_impacts                        ── KETTE 2
            health:   Betroffene·Rate·AF·g(V̂)
            monetary: Assetwert·Verlustrate·Schadenskurve(Intensität)·g(V̂)
            environ.: Naturfläche·Verlustrate·Intensität·g(V̂)
            flat/legacy: ref_value·Index/100·Skalierung
                └─► aggregate: Σ Zell-€ → total_eur (ohne nicht-additive Codes)
```

**Entscheidend:** Der Index nutzt **normierte** H/E/V + Screening-Normgrenzen; die €-Kette
nutzt **absolute** Intensitäten (`impact/base.haz_intensity`, *fixe* Katalog-Grenzen) und
reale Assetgrößen. Beide teilen dieselbe `CellContext`, trennen sich danach vollständig.

---

## Phase 0 — Aufräumen: toter Assessor-Code entfernt ✅

**Befund.** Es existierten zwei parallele Bewertungssysteme. Der produktive Lauf geht
**ausschließlich** über `engine.runner.run_full_assessment` (`tasks/assessment_worker.py`).
Die 8 Gefahren-Assessoren unter `climate/*/assessor.py` waren ein **toter Parallelpfad**:
`registry.get_assessor` / `list_assessors` wurden nirgends aufgerufen, `registry.py`
importierte nichts außerhalb `climate/`, keine API-Route/kein Test/kein CLI nutzte sie.
Nur die OSM-Helfer (`climate/heat/osm_data.py`) und die Datenquellen-Module (`dwd_data`,
`dwd_cdc_grid`, `pegelonline`, `era5_storm`) werden von der Engine wiederverwendet.

**Aktion (umgesetzt).** Entfernt: `climate/{base,registry}.py`, `climate/heat/assessor.py`
und die 7 danach leeren Hazard-Verzeichnisse (`heavy_rain, river_flood, drought,
forest_fire, agriculture, storms, sea_level`). Behalten: `climate/heat/` (wegen
`osm_data.py`), `dwd_data.py`, `dwd_cdc_grid.py`, `pegelonline.py`, `era5_storm.py`.

**Verifikation.** Keine Restreferenz (`grep`), `import app.main` OK, **189/189 Tests grün**.

---

## ✅ Behobene Bugs (Changelog)

Alle beim Review erkannten **echten Bugs** sind umgesetzt & verifiziert (189/189 Tests) und
daher **nicht mehr** als offene Befunde geführt. Kurzprotokoll:

1. **🐞 Gewässerdistanz maß in Grad statt Metern** (`compute_water_distance_m`). `STRtree.
   nearest` wählte bei ~51° N (1° lon ≈ 69,6 km, 1° lat ≈ 111,2 km) das **falsche** Gewässer
   → Distanz zu groß, `WATER_PROXIMITY` zu klein (Nutzerbefund Oschatz: 1 neben 0). Fix:
   metrisches Nachmessen im Umkreis. Gegentest **39/400 → 0/400** Fehler (bis 107 m).
2. **🐞 Gleicher Grad-Fehler in der Infrastruktur-Distanz** (`compute_nearest_distance_m`)
   → betraf `HOSPITAL/DOCTOR/PHARMACY_DISTANCE_M`, `HEALTHCARE_ACCESS_*`, Notfall- und
   Deichnähe. Fix identisch, **0/400** Fehler.
3. **🐞 Zensus-Gedankenstrich „–" fälschlich als fehlend** (`zensus_loader`). „–"/„-"
   bedeutet in der Destatis-Notation **genau Null** — wurde aber wie „geheim/fehlend" auf
   `None` gesetzt (Zelle teils verworfen). Fix: bei **Zähl-/Anteilsgrößen** (Bevölkerung,
   Anteile %, Gebäudezahlen) `–` → **0**; bei **Durchschnittswerten** (Nettokaltmiete,
   Wohnfläche/Person) bleibt `–` = **`None`** (mangels Fällen „kein Wert", nicht 0 €/m² —
   sonst würde der Resilienz-Index verzerrt). Echt fehlende Werte („…"/leer) bleiben `None`.
   Damit ist auch die frühere NULL-Inkonsistenz bei `POPULATION_OVER_65/UNDER_18` **korrekt**
   (dash = 0).
4. **🐞 Hartcodiertes Jahr 2024** in `BUILDING_STABILITY` (`_building_stability`) → durch
   `date.today().year` ersetzt (Baualter-Term altert nicht mehr ein).
5. **🐞 Veraltete Provenance-Texte** für `HEAVY_RAIN_INDEX` und `STORM_DAYS`
   (`catalog_auxiliary`) behaupteten „noch nicht angebunden", obwohl DWD-CDC-Starkregen bzw.
   ERA5 real genutzt werden → `source`-Strings auf die tatsächliche Herkunft korrigiert.
6. **🐞 `type=waterway`-Relation als Riesenpolygon** (`fetch_water_features` /
   `_relation_to_multipolygon`). Eine lineare Fluss-/Bach-Relation (Segmente ohne Rolle, z. B.
   „Döllnitz" `rel/15077092` bei Oschatz) wurde wie eine Multipolygon-Fläche behandelt und zu
   einem Polygon über den **ganzen Bachlauf** gestitcht → `WATER_DISTANCE` 0, `WATER_PROXIMITY`
   flächig **1** über ganze Felder, obwohl kein Gewässer sichtbar ist (zweiter Oschatz-Befund).
   Fix: nur echte Flächen-Relationen (`type=multipolygon` bzw. `natural=water`/`water=*`, nicht
   `type=waterway`) polygonisieren; lineare Gewässer-Relationen als **Linien** (Member-Ways)
   führen. Zur Diagnose zeigt der Inspektor (Modus *Details*) auf den Gewässer-Layern jetzt die
   auslösenden **OSM-Objekte inkl. ID/Tag/Distanz** (`water_src`, `describe_cell_water_sources`).

> Die Fixes 1–3 und 6 ändern Per-Zell-Rohgrößen → bei Bedarf Neuberechnung der Assessments
> (`MODEL_VERSION`-Bump), damit Karte/Dashboard die korrigierten Werte zeigen.
> **Offene Punkte** (Verbesserungen, keine Bugs) stehen weiter je Layer und im Gesamtfazit.

---

## Schicht „Sonstige" (AUXILIARY) — 59 Rohdaten-Layer

**Rolle in den Ketten: keine (bewusst).** Reiner **Nachvollziehbarkeits-Spiegel**:
`auxiliary.build_auxiliary(ci, regional)` (`engine/auxiliary.py:25`) mappt die Zell-
Rohgrößen `ci` und den Kommune-Kontext `regional` 1:1 auf 59 Codes, persistiert sie in
`CellAssessment.data["auxiliary"]` und exportiert `sonstige_100m`. **Fließt nicht in
H/E/V/R zurück** — Indikatoren lesen direkt aus `ci`/`regional`. Ein Fehler in der reinen
*Spiegelung* verfälscht daher nur Anzeige/Export; ein Fehler in der *Quellrechnung* (z. B.
die beiden Distanz-Bugs oben) verfälscht dagegen auch H/E/V/R, weil dieselbe `ci`-Rohgröße
dort einfließt. Das Katalog-Feld `feeds_layers` dokumentiert je Rohgröße, welche H/E/V sie
speist (Basis des Wirkungsdiagramms).

---

### Kategorie `zensus` (10 Layer)

Quelle durchweg **Zensus 2022, 100-m-INSPIRE-Gitter (Destatis)**, je Zelle über die
`gitter_id` gejoint (`zensus_loader.apply_zensus_to_cell_inputs`). Pflichtdaten, kein
OSM-Proxy. Destatis-Kennzeichen: **`–` = genau Null → `0`** bei Zähl-/Anteilsgrößen
(behoben); bei Durchschnittswerten (Miete/Wohnfläche) bleibt `–` = `None` (kein Wert).
Echt fehlende/geheime Werte (`…`/leer) → `None`, Klammerwerte mit Unsicherheits-Flag.

#### `POPULATION_COUNT` — Einwohner je Zelle [Pers.]
- **Was.** Zahl der gemeldeten Personen in der 100×100-m-Zelle. Grundgröße für alle
  bevölkerungsskalierten Expositionen und Risiken (Mortalität, Betroffene, Evakuierte).
- **Wie.** Direktübernahme des Zensus-Bevölkerungswerts der Gitterzelle (`pop`); im
  Auxiliary gerundet auf 2 Nachkommastellen (`auxiliary.py:33`). Kein Operator dazwischen.
- **Review.** ✅ Echte, ortsaufgelöste Pflichtdaten — der stärkste Differenzierer der
  ganzen Kette.
- **Verbesserung.** —

#### `SHARE_OVER_65` — Anteil ≥65 Jahre [%]
- **Was.** Prozentualer Anteil der ≥65-Jährigen an der Zellbevölkerung — Kernindikator für
  Hitze-Vulnerabilität (ältere Menschen sterben überproportional in Hitzewellen).
- **Wie.** Direkt aus dem Zensus-Thema `share_over_65` (`AnteilUeber65`), keine Rechnung.
- **Review.** ✅ echt, ortsaufgelöst.
- **Verbesserung.** —

#### `SHARE_UNDER_18` — Anteil <18 Jahre [%]
- **Was.** Anteil der Minderjährigen — zweite vulnerable Altersgruppe (Kinder reagieren
  empfindlich auf Hitze/Luftschadstoffe).
- **Wie.** Direkt aus Zensus-Thema `share_under_18`.
- **Review.** ✅.
- **Verbesserung.** —

#### `POPULATION_OVER_65` — Einwohner ≥65 [Pers.]
- **Was.** Absolute Zahl älterer Menschen in der Zelle (nicht der Anteil) — die eigentliche
  Betroffenenzahl für Hitze-Gesundheitsrisiken.
- **Wie.** `pop_over_65 = pop · share_o / 100` mit `share_o = share_over_65 or 0.0`
  (`zensus_loader.py:416,420`).
- **Review.** ✅ **Konsistent (behoben).** Da der Zensus-Gedankenstrich `–` jetzt als
  **genau Null** interpretiert wird, sind `SHARE_OVER_65 = 0` und `POPULATION_OVER_65 = 0`
  stimmig; echt fehlende/geheime Zellen bleiben `None`.
- **Verbesserung.** —

#### `POPULATION_UNDER_18` — Einwohner <18 [Pers.]
- **Was.** Absolute Zahl Minderjähriger in der Zelle.
- **Wie.** `pop_under_18 = pop · share_u / 100` (`zensus_loader.py:421`).
- **Review.** ✅ konsistent (behoben — `–` = genau Null).
- **Verbesserung.** —

#### `LIVING_AREA_PER_PERSON` — Wohnfläche je Bewohner [m²]
- **Was.** Durchschnittliche Wohnfläche pro Kopf — Proxy für Wohlstand/Enge; geht in den
  Sozioökonomie-/Resilienz-Index ein.
- **Wie.** Direkt aus Zensus-Thema (`durchschnWohnflaeche`/analog).
- **Review.** ✅.
- **Verbesserung.** —

#### `NET_COLD_RENT` — Nettokaltmiete [€/m²]
- **Was.** Ortsübliche Kaltmiete je m² — Proxy für Kaufkraft/Standortwert.
- **Wie.** Direkt aus Zensus-Thema `durchschnMieteQM`.
- **Review.** ✅.
- **Verbesserung.** —

#### `OWNER_SHARE` — Eigentümerquote [%]
- **Was.** Anteil selbstnutzender Eigentümer — Proxy für finanzielle Anpassungskapazität
  (Eigentümer investieren eher in Gebäudeschutz).
- **Wie.** Direkt aus Zensus-Thema `Eigentuemerquote`.
- **Review.** ✅.
- **Verbesserung.** —

#### `BUILDING_COUNT_ZENSUS` — Gebäudeanzahl (Zensus) [Anzahl]
- **Was.** Zahl der Gebäude in der Zelle laut Gebäude-/Wohnungszählung.
- **Wie.** Direkt aus Zensus-Thema `Insgesamt_Gebaeude`.
- **Review.** 🟡 **Doppelung (P1-5):** existiert parallel zu `BUILDING_COUNT` (OSM) ohne
  Kennzeichnung, welche Quelle maßgeblich ist.
- **Verbesserung.** Eine als „maßgeblich" markieren (Zensus für Bestand, OSM für Geometrie).

#### `BUILDING_AGE_MEAN` — Mittleres Baujahr [Jahr]
- **Was.** Mittleres Baujahr der Gebäude — Proxy für Bausubstanz/Ertüchtigungsgrad; geht in
  `BUILDING_STABILITY` ein.
- **Wie.** Direkt aus Zensus-Thema `building_age_mean` (vorab aus Baualtersklassen
  gemittelt).
- **Review.** 🟡 Kartennormierung `norm_max=2025` (`catalog_auxiliary.py:52`) staucht die
  reale Spanne (~1900–2020) an den oberen Rand → farblich kaum unterscheidbar.
- **Verbesserung.** `norm_min≈1950` setzen (reine Anzeige, keine Quelle nötig).

---

### Kategorie `osm` (17 Layer)

Gemeinsame Quelle: **OpenStreetMap** (Overpass), einmal je Kommune geladen. Zwei
Kernrechnungen je Zelle: **Flächenkomposition** (`compute_cell_composition`, Schichtmodell
mit 100 %-Budget) und **Gebäude/Straßen/Bäume** (`compute_cell_buildings`, für UHI-Canyon,
Baumkronen, Gebäudehöhe). Grundprinzip: Für jedes OSM-Objekt wird die **Schnittfläche mit
der Zellgeometrie** gebildet und durch die **Zellfläche** geteilt → Flächenanteil `[0..1]`.

> **~~O-1 🟠 „Coverage-Asymmetrie"~~ → ✅ behoben (Schichtmodell).** Früher normierte
> `compute_cell_landuse` `impervious_fraction`/`albedo` auf die kartierte Fläche
> (`total_covered`), Grün/Wasser/Wald/Acker aber nicht — teil-erfasste (ländliche) Zellen
> unterschätzten dadurch systematisch Vegetation. Die Ablösung durch
> `compute_cell_composition` bildet ein geschlossenes 100 %-Budget (V/G/W/A/Wa/O): unkartierte
> Restfläche fällt an die Fallback-Zeile (`5 V / 95 O`), alle Anteile teilen sich konsistent
> dieselbe Zellfläche. Details siehe §`IMPERVIOUS_FRACTION`.

> **Gemeinsame Schwäche (O-2 🟡 „Grad-Flächen"):** Flächen werden in **Grad²** gerechnet
> (`cell_geom.area`). Da eine 100-m-Zelle bei 51° N in Grad höher als breit ist, sind
> reine Anteile (Fläche/Zellfläche) näherungsweise korrekt (Grad² kürzt sich), aber
> **absolute** Breiten (Straßen-Puffer, Baumkronen) nutzen `1/111 320 °/m` (Breitengrad-
> Faktor) → in Ost-West-Richtung ~1,6× verzerrt. Nur Proxy-relevant, klein.

#### `IMPERVIOUS_FRACTION` — Versiegelungsgrad [0..1]
- **Was.** Anteil wasserundurchlässiger Oberfläche (Dächer, Asphalt, Pflaster, Beton) an der
  Zelle. Treiber für Aufheizung (UHI), Oberflächenabfluss (Starkregen) und Trockenstress.
- **Wie.** **Flächenkompositions-Schichtmodell** (`compute_cell_composition`,
  `osm_data.py`): Die Zelle wird vollständig auf sechs Kategorien aufgeteilt — **V**ersiegelt,
  **G**rün, **W**ald, **A**cker, **Wa**sser, **O**ffen — deren Summe konstruktionsbedingt
  exakt 100 % ergibt. Jede OSM-Tag-Zeile ist selbst eine Komposition mit Summe 100 (per
  Unit-Test `test_cell_composition.py` erzwungen). `imp = clamp(V; 0,02..0,98)`
  (`inputs.py`, `_clamp_impervious`).
  - **Vier Regeln.** (1) *surface sticht Tag:* der `surface`-Wert eines Features ersetzt
    dessen V-Default über `SURFACE_SEALING` (Abflussbeiwert-Spannen DWA-A 138 / DIN 1986,
    z. B. `paving_stones`=75 %, `sett`=65 %, `gravel`=35 %, `grass_paver`=25 %) — ein
    gepflasterter Marktplatz ist eben weder 0 % noch 100 % versiegelt. (2) *100 %-Budget:*
    Zellwerte = flächengewichtete Summe der Zeilen. (3) *Fallback:* unkartierte Restfläche
    bekommt `5 V / 95 O` (= alter Default). (4) *Überlagerung:* feste Schichtreihenfolge mit
    geometrischem Abzug (`difference`) — **Gebäude → Verkehr/Plätze → Wasser → spezifische
    Nutzung → großflächige Landnutzung → Fallback**; jedes Stück Zellfläche zählt genau
    einmal, das konkretere Objekt „oben" sticht.
  - **Residual-Zeilen.** Urbane Landnutzung (`residential` 30 V / 55 G, `industrial` 65 V …)
    beschreibt die Fläche **nach** Abzug gemappter Gebäude/Straßen (Einfahrten, Höfe, Gärten).
    Anker: residential-Rest 30 % + typ. Gebäudedeckung ~25 % + Straßen ~7 % ≈ 55 % —
    deckungsgleich mit der früheren Pauschale. Ungemappte Privatflächen sind so systematisch
    erfasst (frühere harte `imp_detail`-Umschaltung entfällt).
  - **Neue Objekte im Detail-Weg.** gepflasterte Plätze (`highway=pedestrian`+`area=yes`) als
    Fläche statt 3-m-Linie, `amenity=parking`, `aeroway`; Straßen surface-/tracktype-abhängig
    (Feldweg `track/grade4` ≈ 15 % statt pauschal 95 %) statt der alten Konstante `0,95`.
- **Review.** ✅ Echtes 100 %-Budget (behebt die frühere Coverage-Asymmetrie O-1) und
  klare Überlagerungssemantik. surface-Gewichtung ersetzt die frühere Straßen-Pauschale 0,95.
- **Verbesserung.** Optional gegen **Copernicus HRL Imperviousness Density** (kostenlos,
  10–20 m) plausibilisieren.

#### `GREEN_FRACTION` — Grünanteil [0..1]
- **Was.** Anteil vegetationsbedeckter Fläche (Wald, Wiese, Park, Grasland). Kühlwirkung
  gegen Hitze, Versickerung, Erholungsfunktion.
- **Wie.** Aus derselben Flächenkomposition: `green_fraction = G + W` (Wald zählt zum
  Grünanteil). Da die Komposition ein geschlossenes 100 %-Budget bildet, ist der Grünanteil
  konsistent mit Versiegelung/Wasser/Acker/Offen — keine unabhängige Summe mehr.
- **Review.** ✅ nicht mehr von der Coverage-Asymmetrie (O-1) betroffen: die unkartierte
  Restfläche fällt an die Fallback-Zeile (`95 O`), nicht stumm aus der Normierung.
- **Verbesserung.** Kostenlos: Copernicus HRL Grassland/Tree-Cover als Referenz.

#### `WATER_FRACTION` — Wasseranteil (Fläche) [0..1]
- **Was.** Soll den Anteil offener Wasserfläche (Seen, Flüsse) in der Zelle abbilden —
  kühlend, aber auch Expositionsträger für Gewässer-/Fischereirisiken.
- **Wie.** **Nicht** der reine Landnutzungs-Wasseranteil, sondern
  `max(lu.water_fraction, water_adj·0,5, water_prox·0,3)` (`inputs.py:205`): der größere aus
  echter Wasserfläche, halbem Nachbar-Wasseranteil und 0,3× Gewässer-Nähe-Score.
- **Review.** 🟠 **Semantik-Bruch:** Eine Zelle **ohne** Wasser, aber nahe einem Gewässer,
  bekommt bis zu `0,3` „Wasseranteil" — für einen Layer namens „Wasseranteil (Fläche)"
  irreführend (mischt Fläche und Nähe).
- **Verbesserung.** Den reinen `lu.water_fraction` als `WATER_FRACTION` spiegeln; die
  Nähe-Anreicherung nur intern für H/E behalten (dort ggf. gewollt), nicht als „Fläche"
  ausweisen.

#### `FOREST_FRACTION` — Waldanteil [0..1]
- **Was.** Anteil Wald in der Zelle — Expositionsträger für Waldbrand und Basis für
  Ökosystemleistungen/CO₂.
- **Wie.** Summe der Schnittflächen-Anteile der Objekte mit Label `forest/wood/forestry`
  (`osm_data.py:747-748`), geklemmt auf 1.
- **Review.** 🟠 Coverage-Asymmetrie (O-1); zudem keine Trennung Nadel-/Laubwald, obwohl
  Nadelwald deutlich brandgefährdeter ist.
- **Verbesserung.** OSM `leaf_type=needleleaved/broadleaved` (bereits im Fetch verfügbar)
  auswerten → Nadelwaldanteil für den Waldbrand-Layer (statt der pauschalen 0,6 im späteren
  H-Review).

#### `FARMLAND_FRACTION` — Ackeranteil [0..1]
- **Was.** Anteil landwirtschaftlicher Nutzfläche — Expositionsträger für Dürre-/Ernteschäden.
- **Wie.** Summe der Schnittflächen-Anteile der Objekte mit Label `farmland/orchard/vineyard`
  (`osm_data.py:749-750`), geklemmt auf 1.
- **Review.** 🟠 Coverage-Asymmetrie (O-1). Keine Kulturart-Differenzierung.
- **Verbesserung.** Optional gegen **Copernicus CLC+ / Invekos** (kostenlos) prüfen.

#### `BUILDING_COVERAGE` — Gebäudeanteil [0..1]
- **Was.** Von Gebäudegrundrissen bedeckter Flächenanteil der Zelle — Kern für
  Gebäudebestand, Aufheizung und Sturmangriffsfläche.
- **Wie.** `bldg_coverage = Σ (Zelle ∩ Gebäudepolygon).area / Zellfläche`, geklemmt auf 1
  (`osm_data.py:900-911`).
- **Review.** ✅ direkte Geometrie, robust.
- **Verbesserung.** —

#### `BUILDING_COUNT` — Gebäudeanzahl (OSM) [Anzahl]
- **Was.** Zahl der OSM-Gebäudepolygone, die die Zelle berühren.
- **Wie.** Zähler `bldg_count += 1` je Gebäude mit `Zelle ∩ Gebäude > 0` (`osm_data.py:907`).
- **Review.** 🟡 Doppelung mit `BUILDING_COUNT_ZENSUS` (P1-5); zählt an Zellgrenzen ein
  Gebäude in beiden Nachbarzellen (leichte Überzählung).
- **Verbesserung.** Zuordnung über Gebäude-Zentroid statt Berührung (verhindert
  Doppelzählung).

#### `ENERGY_INFRA_COUNT` — Energieinfrastruktur (OSM) [Anzahl]
- **Was.** Zahl energiewirtschaftlicher Anlagen (Umspannwerke, Kraftwerke, größere Trafos)
  in/berührend die Zelle — KRITIS-Assetdichte für Energie-Schadensrisiken.
- **Wie.** Zählung der OSM-Objekte der KRITIS-Kategorie Energie (`power=*`-Tags) je Zelle
  aus dem Infrastruktur-Fetch.
- **Review.** ✅ echte Assetzählung (viel besser als reiner Gebäudeproxy). Genauigkeit hängt
  an der OSM-Erfassung (Umspannwerke gut, Ortsnetzstationen lückenhaft).
- **Verbesserung.** Gewichtung nach Anlagentyp (Kraftwerk ≫ Trafo) im späteren
  €-/Kritikalitäts-Review.

#### `WATER_WASTEWATER_COUNT` — Wasser/Abwasseranlagen (OSM) [Anzahl]
- **Was.** Zahl der Wasserwerke/Kläranlagen/Pumpwerke in der Zelle — KRITIS-Assetdichte
  Wasser.
- **Wie.** Zählung der OSM-Objekte der Kategorie Wasser/Abwasser (`man_made=water_works/
  wastewater_plant`, `landuse=reservoir` u. ä.) je Zelle.
- **Review.** ✅ echte Assetzählung.
- **Verbesserung.** —

#### `COMMUNICATION_INFRA_COUNT` — Kommunikationsmasten (OSM) [Anzahl]
- **Was.** Zahl der Kommunikations-/Mobilfunkmasten in der Zelle — KRITIS-Assetdichte TK.
- **Wie.** Zählung der OSM-Objekte der Kategorie Kommunikation (`man_made=mast/tower` mit
  Kommunikationsnutzung, `communication=*`) je Zelle.
- **Review.** ✅ Assetzählung; OSM-Erfassung von Masten uneinheitlich.
- **Verbesserung.** —

#### `AVG_BUILDING_HEIGHT` — Ø Gebäudehöhe [m]
- **Was.** Mittlere Höhe der Gebäude in der Zelle — bestimmt thermische Masse, Straßen-
  schlucht-Effekt (Canyon) und Nacht-UHI.
- **Wie.** **Flächengewichtetes** Mittel `avg_height = Σ(height·Grundriss∩Zelle) /
  Σ(Grundriss∩Zelle)` (`osm_data.py:compute_cell_buildings`). Höhen aus den
  **amtlichen LoD2-Modellen** der Länder (`bldg:measuredHeight`,
  `services/geodata/lod2/`), wo angebunden (NRW, BY, BB, HH; weitere folgen);
  sonst OSM-Heuristik (`height`-Tag / `building:levels·3 m` / 6-m-Default).
  Quelle je Lauf in `provenance.building_height`.
- **Review.** ✅ Amtliche, gebäudescharfe Höhen; Flächengewichtung verhindert, dass
  Kleinstgebäude Hochhäuser verwässern. OSM-Fallback bleibt als Qualitätsflag
  sichtbar. Nebeneffekt: LoD2-Footprints (ALKIS-vollständig) verbessern auch
  `BUILDING_COVERAGE`/Versiegelung.
- **Verbesserung.** Phase-2-Länder (Atom-Feeds/Portale) anbinden; Landesgrenzen-
  Kommunen erhalten jenseits der Grenze weiterhin OSM-Höhen.

#### `ROAD_COVERAGE` — Straßenanteil [0..1]
- **Was.** Von Straßenflächen bedeckter Zellanteil — Versiegelungs- und
  Verkehrsexpositions-Proxy.
- **Wie.** Je Straßenlinie Puffer um die halbe Fahrbahnbreite (`width_m/2`, in Grad über
  `1/111 320`), Schnitt mit der Zelle, Flächen summiert / Zellfläche, geklemmt auf 1
  (`osm_data.py:920-931`).
- **Review.** 🟡 Puffer in Grad (O-2) → Ost-West etwas verzerrt; `width_m` oft aus
  Straßenklasse geschätzt.
- **Verbesserung.** Puffer in UTM legen (wie bei den Distanz-Fixes).

#### `TREE_CANOPY` — Baumkronendeckung [0..1]
- **Was.** Von Baumkronen beschatteter Zellanteil — lokale Kühlung/Verschattung.
- **Wie.** Je OSM-Baum (Punkt in Zelle) Kreisfläche `π·(Kronendurchmesser/2)²` (Radius in
  Grad), summiert / Zellfläche, geklemmt auf 1 (`osm_data.py:936-943`).
- **Review.** 🟠 nur **einzeln gemappte** OSM-Bäume (`natural=tree`) → in DE stark
  lückenhaft, Waldkronen fehlen; Kronenradius meist Default.
- **Verbesserung.** **Copernicus HRL Tree Cover Density** (kostenlos, 10 m) als Rasterquelle.

#### `SKY_VIEW_FACTOR` — Sky-View-Faktor [0..1]
- **Was.** Anteil des von einer Fläche „sichtbaren" Himmels (1 = frei, 0 = tiefe
  Straßenschlucht). Bestimmt die nächtliche Ausstrahlung und damit Nacht-UHI/Tropennächte.
- **Wie.** **Echtes geometrisches SVF** per Horizontwinkel-Verfahren
  (`services/geodata/lod2/svf.py`): `SVF = 1 − (1/N)·Σ sin²γᵢ` mit N=16
  Richtungen, 100-m-Suchradius auf einem 5-m-Gebäudehöhenraster (LoD2- bzw.
  OSM-Höhen), gemittelt über die nicht überbauten Pixel der Zelle
  (Oke 1981; Zakšek et al. 2011). Der frühere Proxy
  `max(0,1; 1 − coverage·min(h/20;1))` ist entfernt.
- **Review.** ✅ methodisch sauber; Nachbargebäude außerhalb der Zelle gehen ein
  (Rasterverfahren über die gesamte bbox). Erbt die verbleibende Höhen-
  Unsicherheit nur noch in OSM-Fallback-Ländern (siehe `provenance.svf`).
- **Verbesserung.** Optional Gelände-Horizont (DEM) für Tallagen ergänzen.

#### `SURFACE_ALBEDO` — Albedo [0..1]
- **Was.** Rückstrahlvermögen der Oberfläche — hohe Albedo (helle Dächer/Flächen) reflektiert
  Sonne und mindert Aufheizung.
- **Wie.** Flächengewichtetes Mittel der Albedo-Koeffizienten je Landnutzung
  (`LANDUSE_ALBEDO`/`NATURAL_ALBEDO`, Default 0,20), normiert auf die abgedeckte Fläche
  (`osm_data.py:734`).
- **Review.** ✅ als Proxy dokumentiert; Koeffizienten sind Literaturmittel.
- **Verbesserung.** Optional Sentinel-2-Albedo (kostenlos) — aufwändig, als Proxy belassen.

#### `INDUSTRIAL_FRACTION` — Industrie-/Gewerbeanteil [0..1]
- **Was.** Soll den Anteil von Industrie-/Gewerbeflächen abbilden (Expositionsträger für
  Standort-/Betriebsrisiken).
- **Wie.** **Residuum** `max(0; imp_frac − building_coverage − road_coverage)`
  (`auxiliary.py:11`) — „versiegelt, aber weder Gebäude noch Straße".
- **Review.** 🟠 (P1-3) misst tatsächlich **Parkplätze/Plätze/Höfe**, nicht Industrie; kann
  bei geklemmtem `imp_frac` auch 0 werden, obwohl Gewerbe vorhanden ist.
- **Verbesserung.** OSM `landuse=industrial/commercial/retail` (im selben Fetch vorhanden)
  direkt als Flächenanteil verschneiden.

#### `VENTILATION_SCORE` — Frischluft-Anteil [0..1]
- **Was.** Anteil „offener" Nachbarzellen — Proxy für Durchlüftung/Kaltluftzufuhr, mindert
  Hitzestau und ist Sturmexpositions-Faktor.
- **Wie.** Über die 8 Nachbarzellen: `offen` wenn Nachbar fehlt (Rand) **oder**
  `building_coverage < 0,05` **und** `green+water+farmland > 0,3`; `vent_score =
  offen/gesamt` (`inputs.py:150-163`).
- **Review.** ✅ einfacher, nachvollziehbarer Proxy. Randzellen zählen als „offen" (leichte
  Aufwertung am Kommunerand).
- **Verbesserung.** Kaltluft aus dem **DEM-Hangabtrieb** (Kaltluftschneisen) ergänzen —
  Terraindaten liegen bereits vor.

---

### Kategorie `health` (9 Layer)

Basis: OSM-Gesundheitsinfrastruktur (Krankenhaus/Arzt/Apotheke), je Zelle die **Distanz zum
nächsten** Objekt via `compute_nearest_distance_m` (nach 🐞 B-Fix 2 metrisch korrekt),
inkl. Umwegfaktor `×HEALTHCARE_ROAD_FACTOR = 1,3` und Deckelung bei 20 km.

#### `HOSPITAL_DISTANCE_M` — Distanz Krankenhaus [m]
- **Was.** Luftlinien-Distanz (×1,3 Umwegfaktor) zum nächsten Krankenhaus — Erreichbarkeit
  akutmedizinischer Versorgung bei Hitze/Katastrophen.
- **Wie.** `min(20000; nächste_Distanz_UTM · 1,3)` (`osm_data.py:578-611`); Klassifikation
  KH/Arzt/Apo über `_healthcare_category` (`amenity=hospital`, `building=hospital`, …).
- **Review.** ✅ nach dem Bugfix korrekt; 1,3 als Umwegfaktor ist Modellkonstante.
- **Verbesserung.** Optional echte Netzdistanz (OSRM/Valhalla auf OSM, self-hosted
  kostenlos) statt Luftlinie×1,3.

#### `DOCTOR_DISTANCE_M` — Distanz Arzt/Klinik [m]
- **Was.** Distanz zur nächsten (haus-)ärztlichen Einrichtung.
- **Wie.** wie `HOSPITAL_DISTANCE_M`, Kategorie `doctor` (`amenity=doctors/clinic`, …).
- **Review.** ✅.
- **Verbesserung.** wie oben.

#### `PHARMACY_DISTANCE_M` — Distanz Apotheke [m]
- **Was.** Distanz zur nächsten Apotheke (Medikamentenversorgung).
- **Wie.** wie oben, Kategorie `pharmacy` (`amenity=pharmacy`, …).
- **Review.** ✅.
- **Verbesserung.** wie oben.

#### `HEALTHCARE_ACCESS_SCORE` — Erreichbarkeit gesamt [0..1]
- **Was.** Zusammengesetzter Erreichbarkeits-Score (1 = alles direkt vor Ort, 0 = alles
  ≥20 km weg) — die **kanonische** Gesundheits-Erreichbarkeitsgröße.
- **Wie.** Je Typ Nähescore `prox = max(0; 1 − d/20000)`, dann gewichtete Summe
  `score = 0,50·prox_KH + 0,35·prox_Arzt + 0,15·prox_Apo` (`osm_data.py:604-620`).
- **Review.** ✅ plausibel gewichtet; linearer Abfall über 20 km ist eine (vertretbare)
  Modellwahl.
- **Verbesserung.** Gewichte/Reichweiten als editierbare Parameter (z. B. BBSR-Erreichbar-
  keitsschwellen).

#### `HEALTHCARE_ACCESS_GRID` — Erreichbarkeit [Index 0..100]
- **Was.** Derselbe Score als 0–100-Zahl für die Kartendarstellung.
- **Wie.** `HEALTHCARE_ACCESS_SCORE · 100` (`auxiliary.py:57`).
- **Review.** 🟡 redundant zu SCORE (P1-4).
- **Verbesserung.** aus dem Export nehmen (Tooltip genügt).

#### `HEALTHCARE_ACCESS_INDEX` — Erreichbarkeits**defizit** [0..100]
- **Was.** Kartenkonformes „hoch = schlecht": 100 = keine Versorgung erreichbar.
- **Wie.** `100 · (1 − HEALTHCARE_ACCESS_SCORE)` (`auxiliary.py:62-63`).
- **Review.** 🟡 exakt invers zu `GRID` (P1-4) — beide gleichzeitig ist verwirrend.
- **Verbesserung.** Als **einzige** Erreichbarkeits-Leitgröße behalten (weil „hoch = Risiko"
  zur restlichen Kartenlogik passt).

#### `HEALTHCARE_INDEX_HOSPITAL` — Beitrag Krankenhaus [0..0,5]
- **Was.** Zerlegungsanteil des KH-Terms am Gesamtscore (zeigt, woher die Erreichbarkeit
  kommt).
- **Wie.** `0,50 · prox_KH` (`osm_data.py:617`).
- **Review.** 🟡 Detailgröße; als eigener Kartenlayer wenig sinnvoll.
- **Verbesserung.** in den Tooltip von `HEALTHCARE_ACCESS_INDEX` verschieben.

#### `HEALTHCARE_INDEX_DOCTOR` — Beitrag Arzt [0..0,35]
- **Was.** Zerlegungsanteil des Arzt-Terms.
- **Wie.** `0,35 · prox_Arzt`.
- **Review.** 🟡 wie oben.
- **Verbesserung.** wie oben.

#### `HEALTHCARE_INDEX_PHARMACY` — Beitrag Apotheke [0..0,15]
- **Was.** Zerlegungsanteil des Apotheken-Terms.
- **Wie.** `0,15 · prox_Apo`.
- **Review.** 🟡 wie oben.
- **Verbesserung.** wie oben.

---

### Kategorie `terrain` (8 Layer) — AWS Terrarium DEM

Gemeinsame Quelle: **AWS Terrarium DEM** (Copernicus-basiert, kostenlos). Pipeline
(`terrain_service.compute_terrain_for_cells`): DEM-Kacheln laden → je Zelle Höhe mitteln →
Hangneigung (Horn), Senkentiefe, D8-Abflussakkumulation, TWI berechnen → einige Größen
**pro Kommune min–max-normieren**.

> **Gemeinsame Schwäche (T-1 🟠 „relative Normierung"):** `slope_norm`, `sink_norm`,
> `twi_norm` und damit `depression_factor`/`slope_factor` werden mit `_normalize` **über die
> Zellen der jeweiligen Kommune** min–max-skaliert (`terrain_service.py:354-363`). Der Wert
> 1,0 bedeutet daher „am extremsten **in dieser Kommune**", nicht absolut. Folge: Auch eine
> topografisch flache Kommune erhält eine volle 0..1-Spreizung, und die Werte sind **nicht
> zwischen Kommunen vergleichbar** — relevant, weil `depression_factor`/`twi_norm` später in
> `HEAVY_RAIN_FLOOD` einfließen.

#### `MEAN_ELEVATION` — Mittlere Höhe [m ü. NN]
- **Was.** Durchschnittliche Geländehöhe der Zelle — Basisgröße für Hangneigung, Kaltluft
  und (an Küsten) Überflutungshöhe.
- **Wie.** Mittel mehrerer DEM-Stichproben je Zelle (`_sample_cell_elevation`, n≈5), NaN-
  Lücken per Nearest gefüllt.
- **Review.** ✅ echte, absolute Größe (nicht relativ normiert).
- **Verbesserung.** —

#### `SLOPE_DEGREES` — Hangneigung [°]
- **Was.** Geländeneigung der Zelle — steuert Abfluss vs. Versickerung, Erosion,
  Rutschungsneigung.
- **Wie.** Horn-Operator über die 4 Nachbarn: `dz/dx=(z_O−z_W)/2Δ`, `dz/dy=(z_S−z_N)/2Δ`,
  `slope = atan(√(dz/dx²+dz/dy²))`, umgerechnet in Grad (`terrain_service.py:289-303`).
- **Review.** ✅ Standardverfahren, absolut.
- **Verbesserung.** —

#### `SINK_DEPTH` — Senkentiefe [m]
- **Was.** Wie tief eine Zelle unter dem Mittel ihrer 8 Nachbarn liegt — Proxy für
  Muldenlagen, in denen sich Starkregen sammelt.
- **Wie.** `sink = max(0; Mittel(8 Nachbarhöhen) − eigene Höhe)` (`terrain_service.py:306-322`).
- **Review.** ✅ einfacher, korrekter Muldenindikator (absolut).
- **Verbesserung.** —

#### `TWI` — Topographic Wetness Index [–]
- **Was.** Maß für die potenzielle Bodennässe: kombiniert Einzugsgebietsgröße und Neigung —
  hoher TWI = viel Zufluss bei geringem Gefälle → staunass/überflutungsanfällig.
- **Wie.** `TWI = ln(A / tan β)` mit `A = max(Abflussakkumulation, 1)·Zellfläche` und
  `tan β = max(tan(slope), 0,001)` (`terrain_service.py:347-351`).
- **Review.** ✅ Lehrbuchformel korrekt umgesetzt. `TWI` selbst ist absolut; erst `twi_norm`
  ist relativ (T-1).
- **Verbesserung.** —

#### `TWI_NORMALIZED` — TWI normiert [0..1]
- **Was.** Auf 0..1 skalierter TWI für Karten/Verrechnung; geht in `HEAVY_RAIN_FLOOD` und
  `FLOODPLAINS` ein.
- **Wie.** `(TWI − min) / (max − min)` über die **Kommune-Zellen** (`_normalize`).
- **Review.** 🟠 relative Normierung (T-1) → nicht kommunenübergreifend vergleichbar.
- **Verbesserung.** Feste phys-basierte Referenzgrenzen (z. B. TWI 3..15) statt
  Kommune-Min–Max.

#### `DEPRESSION_FACTOR` — Senkenfaktor [0..1]
- **Was.** Kombiniertes Muldenmaß aus Nässe und Tiefe — „wie stark sammelt sich hier Wasser".
- **Wie.** `min(1; 0,55·twi_norm + 0,45·sink_norm)` (`terrain_service.py:460`).
- **Review.** 🟠 erbt die relative Normierung (T-1); Gewichte 0,55/0,45 sind Modellwahl.
- **Verbesserung.** absolute Referenzgrenzen wie bei `TWI_NORMALIZED`.

#### `SLOPE_FACTOR` — Hangfaktor [0..1]
- **Was.** Normierte Hangneigung — Treiber für Rutschung/Erosion.
- **Wie.** `slope_factor = slope_norm` = min–max des Hangs über die Kommune.
- **Review.** 🟠 relative Normierung (T-1).
- **Verbesserung.** feste Grenzen (z. B. 0°..30°).

#### `FLOW_ACCUMULATION` — Flussakkumulation [Zellen]
- **Was.** Zahl der oberhalb liegenden Zellen, die (D8) in diese Zelle entwässern — markiert
  Abflussbahnen/Gerinne.
- **Wie.** D8: Zellen absteigend nach Höhe abarbeiten, jeweils den gesamten akkumulierten
  Fluss an den steilsten tieferen Nachbarn weitergeben (`terrain_service.py:325-344`).
- **Review.** ✅ Standard-D8. `norm_max=1000` (Katalog) ist nur Kartenfärbung, willkürlich.
- **Verbesserung.** Perzentil-basierte Kartenskala je Kommune (Anzeige).

---

### Kategorie `water` (3 Layer) — OSM-Gewässer

Basis: OSM-Wasserflächen/-läufe (`fetch_water_features`), Distanz je Zelle nach 🐞 B-Fix 1
metrisch korrekt; lineare Gewässer-Relationen nach 🐞 Fix 6 als Linien statt Riesenpolygon.

#### `WATER_DISTANCE` — Gewässerdistanz [m]
- **Was.** Luftlinien-Distanz der Zelle zum nächsten Gewässer (See/Fluss/Bach) — Grundgröße
  für Nähe-Scores und Auen.
- **Wie.** `compute_water_distance_m`: nächstes Feature via STRtree, exakte Distanz in UTM;
  ohne Gewässer im Gebiet Fallback `20·Zellgröße` (`osm_data.py:433-467`, nach Fix).
- **Review.** 🐞→✅ Nach B-Fix 1 (Metrik) **und** Fix 6: eine `type=waterway`-Relation
  (z. B. „Döllnitz" `rel/15077092`) wurde zuvor zu einem Polygon über den ganzen Bachlauf
  gestitcht → Distanz 0 flächig. Jetzt werden nur echte Flächen-Relationen polygonisiert,
  lineare als Member-Linien geführt.
- **Diagnose.** Inspektor-Modus *Details* listet auf diesem Layer die auslösenden OSM-Objekte
  (`osm_type/osm_id`, Tag, Distanz) via `describe_cell_water_sources` → `water_src`.
- **Verbesserung.** — (Größen-/Typ-Differenzierung folgt bei `WATER_PROXIMITY`).

#### `WATER_PROXIMITY` — Gewässernähe (Score) [0..1]
- **Was.** Nähe-Score (1 = am/ im Gewässer, 0 = ≥500 m entfernt) — Expositionsproxy für
  Hochwasser/Auen und (invers) Wasserverfügbarkeit.
- **Wie.** `water_prox = max(echte_nähe, graben_score)`. Echte Nähe =
  `max(0; 1 − WATER_DISTANCE/500)` gegen **echte** Gewässer (See/Fluss/Bach/Kanal).
  Kleinstgräben (`waterway=ditch`/`drain`) zählen **nicht** als echtes Gewässer, sondern
  liefern nur `graben_score = min(DITCH_PROX_CAP; grabendichte · DITCH_DENSITY_WEIGHT)`
  mit `grabendichte = Grabenlänge innerhalb der Zelle / Zellkantenlänge`
  (`osm_data.py:compute_ditch_density_score`, Trennung echt/Graben in `inputs.py`).
- **Review.** 🐞→✅ Drei aufeinanderfolgende Ursachen für falsche Nähe-1-Felder, alle behoben:
  (1) **Distanz-Bug** (B-Fix 1, Grad statt Meter); (2) **Kleinstgräben** pinnten flächig auf 1
  — jetzt sehr schwach & dichteskaliert (ein querender Graben ≈`DITCH_DENSITY_WEIGHT` 0,05,
  dichtes Netz max `DITCH_PROX_CAP` 0,2, gestreifte Ecke ≈0); (3) **`type=waterway`-Relation**
  (Fix 6) wurde zum Riesenpolygon über den ganzen Bachlauf — das war die eigentliche Ursache
  des Oschatz-Feldes (`rel/15077092` „Döllnitz"); jetzt linienbasiert. Die auslösenden Objekte
  sind im Inspektor (*Details*) samt OSM-ID nachvollziehbar (`water_src`).
- **Justierbare Parameter** (`osm_data.py`, oben im Modul definiert):
  - `DITCH_DENSITY_WEIGHT` **= 0,05** — Gewicht je Einheit Grabendichte; ein die Zelle voll
    querender Graben (Dichte ≈ 1) ergibt genau diesen Score. Höher ⇒ Gräben zählen mehr.
  - `DITCH_PROX_CAP` **= 0,2** — Obergrenze, ab der ein dichtes Grabennetz sättigt; verhindert,
    dass viele Gräben zusammen einen echten Gewässer-Score (→1) erreichen.
  - `_MINOR_WATERWAYS` **= {ditch, drain}** — welche `waterway`-Typen als Kleinstgräben
    schwach gewichtet statt als echtes Gewässer behandelt werden (z. B. `stream`/`canal`
    hier ergänzen, um auch sie herabzustufen).
  - Die echte Reichweite ist weiterhin `max_dist = 500 m` (Default in `water_proximity_score`).
- **Offen 🟠 (Nutzeranregung, kostenlos aus vorhandenem OSM):** echte Gewässer zusätzlich nach
  **Größe/Typ** skalieren — Flächengewässer über die Polygonfläche, Fließgewässer über
  `waterway`-Rang (`river` ≫ `stream`), z. B. `max_dist` typabhängig. Alle nötigen Tags liegen
  im `fetch_water_features`-Ergebnis bereits vor.

#### `WATER_ADJACENCY` — Gewässernähe kombiniert [0..1]
- **Was.** Kombiniertes Nähemaß aus eigener Wasserfläche, Nachbar-Wasser und Nähe-Score —
  „liegt die Zelle an/bei Wasser".
- **Wie.** `max(water_adj, water_prox, lu.water_fraction)` mit `water_adj = max` des
  Wasseranteils über die 8 Nachbarzellen (`inputs.py:162,176,206`).
- **Review.** ✅ sinnvolle Kombination; `WATER_ADJACENCY` feeds `COASTAL_RIPARIAN_ZONES`.
- **Verbesserung.** von der Größen-/Typ-Skalierung bei `WATER_PROXIMITY` profitiert dieser
  Layer automatisch mit.

---

### Kategorie `regional` (12 Layer) — je Kommune ein Wert (`spatial=false`)

Alle aus `build_regional_context` (`inputs.py:304-416`); ein Wert je Kommune, in jede Zelle
gespiegelt. Zwei Klassen: **real am Zentroid** und **linearer Proxy**. Der Lauf protokolliert
die echte Herkunft in `regional["provenance"]`.

> **Gemeinsame Schwäche (R-1 🟠 „Proxy-Kollinearität"):** `DROUGHT_DAYS`, `DRYNESS_INDEX`,
> `SOIL_MOISTURE_DECLINE` sind monotone Funktionen von `hot_days`; `TEMPERATURE_RISE`,
> `SURFACE_WATER_HEATING` monotone Funktionen des **Bundesland**-`mean_temp`. Dadurch können
> Dürre-/Temperatur-Layer nie unabhängig von Hitze variieren, und `mean_temp`-basierte Layer
> haben bundesweit nur 16 verschiedene Werte. Wichtigster inhaltlicher Hebel dieser Schicht.

#### `HOT_DAYS` — Heiße Tage/Jahr [Tage ≥30 °C]
- **Was.** Jahresmittel der Tage mit Tmax ≥30 °C — der zentrale, real ortsaufgelöste
  Hitzetreiber (speist `HEAT_WAVE` und die Hitze-Gesundheitsfunktionen).
- **Wie.** DWD-CDC-`hot_days`-Raster (1 km) am Kommune-Zentroid (`dwd_cdc_grid.hot_days_at`);
  Fallback DWD-Bundesland-Mittel (`inputs.py:335-339`).
- **Review.** ✅ bester Treiber der Kette (echte Rasterdaten).
- **Verbesserung.** — (innerkommunal konstant; feinere Auflösung wäre nur mit Modellrastern
  möglich).

#### `FROST_DAYS` — Frosttage [Tage]
- **Was.** Jahresmittel der Tage mit Tmin <0 °C — Treiber für Kälteextreme/`COLD_EXTREME`.
- **Wie.** DWD-CDC-`frost_days`-Raster am Zentroid; Fallback Proxy `90 − mean_temp·6`
  (`inputs.py:341-346`).
- **Review.** ✅ real, Fallback-Proxy dokumentiert.
- **Verbesserung.** —

#### `MEAN_ANNUAL_TEMP` — Jahresmitteltemperatur [°C]
- **Was.** Mittlere Lufttemperatur — Basis mehrerer Proxys und Treiber für
  Vektor-/Krankheitsrisiken.
- **Wie.** DWD-Gebietsmittel **je Bundesland** (`get_regional_climate`).
- **Review.** 🟠 nur 16 Werte bundesweit → keine kommunale Differenzierung; als Basis für
  weitere Proxys (R-1) verstärkt sich das.
- **Verbesserung.** DWD-CDC-Jahresmittel**raster** am Zentroid (kostenlos, analog `hot_days`).

#### `DROUGHT_DAYS` — Trockentage [Tage]
- **Was.** Geschätzte Zahl der Trockentage/Jahr — Treiber für den Dürre-Hazard.
- **Wie.** Proxy `8 + hot_days·1,2` (`inputs.py:397-399`).
- **Review.** 🟠 reine Funktion von `hot_days` (R-1) → Dürre kann nie von Hitze abweichen;
  Koeffizienten 8/1,2 unbelegt.
- **Verbesserung.** **UFZ-Dürremonitor (SMI)** oder DWD-Bodenfeuchte (beide kostenlos) am
  Zentroid.

#### `DRYNESS_INDEX` — Trockenheitsindex [0..1]
- **Was.** Normierter Trockenheitsgrad — Treiber für Waldbrand und Wasserstress.
- **Wie.** Proxy `min(1; hot_days/25)` (`inputs.py:400-401`).
- **Review.** 🟠 wieder nur `hot_days` (R-1); Divisor 25 unbelegt.
- **Verbesserung.** UFZ-SMI / DWD-Bodenfeuchte.

#### `STORM_DAYS` — Sturmtage [Anzahl/Jahr]
- **Was.** Zahl der Tage mit Sturmböen (≥25 m/s) — Treiber für `EXTRATROPICAL_STORM`.
- **Wie.** ERA5-Böenklimatologie-Raster am Zentroid, **falls** der Betreiber es erzeugt hat;
  sonst regionaler Konstantwert `tunables.regional_fallback("storm_days", 6,0)`
  (`inputs.py:355-360`).
- **Review.** 🟠 in der Praxis meist konstant 6,0 → **null Differenzierung** (ERA5-Raster
  optional). Provenance-Text korrigiert (behoben).
- **Verbesserung.** ERA5-Sturmklimatologie ausrollen (kostenlos, CDS-Key; Skript
  `fetch_era5_storm.py` vorhanden).

#### `HEAVY_RAIN_INDEX` — Starkregenindex [0..100]
- **Was.** Maß der Starkregen-Häufigkeit/-Intensität — Treiber für `HEAVY_RAIN_FLOOD` und
  `LANDSLIDE`.
- **Wie.** Real aus DWD-CDC: `p20·4 + p30·6` (Tage/Jahr ≥20 mm bzw. ≥30 mm) am Zentroid,
  geklemmt auf 100; Fallback Proxy `40 + (mean_temp−9,5)·4` (`inputs.py:375-387`).
- **Review.** ✅ echter Realdatenpfad (deutlicher Fortschritt); Provenance-Text korrigiert
  (behoben — nennt jetzt die DWD-CDC-Herkunft).
- **Verbesserung.** optional KOSTRA-2020 für die Bemessungsregen-Kalibrierung.

#### `TEMPERATURE_RISE` — Temperaturanstieg [°C]
- **Was.** Projizierter mittlerer Temperaturanstieg — Treiber für `MEAN_TEMPERATURE_RISE`.
- **Wie.** Proxy `1,6 + (mean_temp−9,5)·0,1` (`inputs.py:405-406`).
- **Review.** 🟠 aus Bundesland-`mean_temp` (R-1) → 16 Werte bundesweit; Koeffizienten
  unbelegt.
- **Verbesserung.** **DWD-Klimaatlas / Copernicus C3S-CORDEX** Delta ggü. Referenzperiode
  (kostenlos, CDS).

#### `SOIL_MOISTURE_DECLINE` — Bodenfeuchte-Rückgang [mm]
- **Was.** Geschätzter Rückgang der Bodenfeuchte — Treiber für den gleichnamigen
  Boden-/Landwirtschafts-Hazard.
- **Wie.** Proxy `20 + hot_days` (`inputs.py:407`).
- **Review.** 🟠 reine `hot_days`-Funktion (R-1); Einheit „mm" nicht hergeleitet.
- **Verbesserung.** UFZ-Dürremonitor-SMI (kostenlos).

#### `LOW_FLOW_DAYS` — Niedrigwasser-Tage [Tage]
- **Was.** Tage/Jahr, an denen der nächste Pegel unter dem mittleren Niedrigwasser (MNW)
  liegt — Treiber für `LOW_FLOW_NIEDRIGWASSER` (Schifffahrt, Kühlwasser, Ökologie).
- **Wie.** **PEGELONLINE (WSV)**: Tage < MNW am nächsten Pegel (`pegelonline.
  low_flow_days_at`); Fallback Proxy `10 + hot_days` (`inputs.py:348-353`).
- **Review.** ✅ echte Messdaten, wo ein Pegel in Reichweite ist.
- **Verbesserung.** Für pegelferne Binnen-Kommunen den nächsten **Fluss** statt des
  hot_days-Proxys nutzen (WSV-Pegelnetz + OSM-Gewässer bereits vorhanden).

#### `SURFACE_WATER_HEATING_REGIONAL` — Gewässererwärmung (regional) [°C]
- **Was.** Erwärmung offener Gewässer — Treiber für Fischerei-/Aquakultur- und Gewässer-
  ökologie-Risiken.
- **Wie.** Proxy `1,5 + (mean_temp−9,5)·0,2` (`inputs.py:409`).
- **Review.** 🟠 aus Bundesland-`mean_temp` (R-1) → kaum Differenzierung.
- **Verbesserung.** Sentinel/Landsat-LST über Wasserflächen (kostenlos, aufwändig) — sonst
  als Proxy kennzeichnen.

#### `SEA_LEVEL_RISE` — Meeresspiegelanstieg [mm/Jahr]
- **Was.** Jährlicher Meeresspiegelanstieg — Treiber für Küstenrisiken (nur Küstenkommunen).
- **Wie.** Konstante `tunables.regional_fallback("sea_level_rise", 4,5)` für Küstenkommunen,
  sonst 0 (`inputs.py:410`).
- **Review.** 🟡 ein nationaler Wert für alle Küsten.
- **Verbesserung.** **BSH**-Regionalpegel + IPCC-AR6-Sea-Level-Tool (kostenlos) je Küstenort.

---

### Sammelbefunde Sonstige (Kurzliste)

- **O-1 🟠** — Coverage-Asymmetrie: Grün/Wald/Wasser/Acker nicht auf abgedeckte Fläche
  normiert → in teil-erfassten Zellen unterschätzt.
- **T-1 🟠** — Terrain-Normierungen (`*_norm`, `depression_factor`, `slope_factor`) sind
  **kommunerelativ** min–max → nicht vergleichbar; feste physikalische Grenzen setzen.
- **R-1 🟠** — Regionale Proxy-Kollinearität (Dürre/Temp aus `hot_days`/Bundesland-
  `mean_temp`) → UFZ-SMI + DWD-Rasterjahresmittel anbinden.
- **P1-3 🟠** — `INDUSTRIAL_FRACTION` Residuum statt OSM-`landuse=industrial`.
- **`WATER_PROXIMITY` 🟠** — nach Bugfix noch ohne Größen-/Typ-Skalierung (Nutzeranregung).
- **P1-4/P1-5, O-2 🟡** — Healthcare-Redundanz, doppelte Gebäudezahl,
  Grad-Flächen-Anisotropie.

---

## Schicht „Sensitivitäten" (Vulnerabilities V) — 33 Layer

Berechnet in `indicators.compute_cell_hev` (`engine/indicators.py:232-266`) aus den
`ci`-Rohgrößen. Meist Index 0..100 (hoch = **verwundbarer**). „Kapazitäts"-Indikatoren
(Resilienz, Geld, Governance) sind **invers** kodiert und im Katalog-`name` mit „(invers)"
markiert — ein hoher Wert heißt dort *wenig* Kapazität.

**Wie V in beide Ketten eingeht (einmal zentral):**
- **Index (Kette 1):** `V̂ = clamp((V − norm_min)/(norm_max − norm_min), 0, 1)`
  (`risk_engine.normalize_hev`), dann als **Faktor** im Pfadprodukt `w·Ĥ·Ê·V̂` (Maximum über
  die Pfade). Höheres V̂ ⇒ höherer Index. Ein konstantes `V̂` (z. B. 0,5) **halbiert** hier
  den Pfadterm — ist also nicht neutral.
- **€ (Kette 2):** ausschließlich über den Vulnerabilitäts-Modifikator
  `g(V̂) = 0,5 + Mittel(V̂ über die V-Liste des Risikos) ∈ [0,5; 1,5]`
  (`impact/base.py:70-74`), der jeden Zell-Schaden multipliziert. V verschiebt den €-Schaden
  also um max. ±50 %. Ein konstantes `V=50` (V̂=0,5) ist hier **neutral** (Beitrag 0,5 zum
  Mittel) — im Index dagegen dämpfend. Wichtige Asymmetrie.
- Fast alle V haben `norm=[0,100]` ⇒ `V̂ = V/100`. Ausnahmen: `VULNERABLE_GROUPS_SHARE`
  `[0,50]`, `UHI_INTENSITY` `[0,8]`.

**Schicht-übergreifende Befunde (gelten für viele V):**
- **V-A 🟠 — 7 konstante V ohne Ortsauflösung.** `CRITICAL_INFRA_CONDITION=50` (in **8**
  Risiken!), `SUPPLY_CHAIN_DEPENDENCY=50`, `REDUNDANCY_BACKUP=50`, `INFRA_DEPENDENCY_CHAIN=50`,
  `AQUACULTURE_TECHNICAL_VULNERABILITY=50`, `FISHERIES_MANAGEMENT_CAPACITY=45`,
  `SALTWATER_INTRUSION_RISK=40/10`. Sie differenzieren Kommunen nicht (im Index sogar
  dämpfend). Editierbar, aber nicht datengetrieben.
- **V-B 🟠 — 2 tote V.** `LEVEE_CONDITION` und `SALTWATER_INTRUSION_RISK` werden von **0
  Risiken** referenziert → fließen in **keine** Kette. `LEVEE_CONDITION` wird dennoch
  aufwändig aus `dyke_prox`/Exposition berechnet (inkl. OSM-Deich-Fetch). Entweder in
  Hochwasser-/Küstenrisiken verdrahten oder entfernen.
- **V-C 🟡 — Doppelformeln.** `MATERIAL_HEAT_SENSITIVITY` und `SEALING_DEGREE` sind
  **identisch** (`clamp(imp·100)`); `UHI_INTENSITY` (=`uhi`) überlappt mit dem `uhi`-Term in
  `HEAT_SENSITIVITY`.
- **V-D 🟠 — T-1-Erbe.** `SOIL_SENSITIVITY`, `EROSION_SUSCEPTIBILITY` (und indirekt weitere)
  nutzen `slope_factor`/`twi_norm`, die **kommunerelativ** min–max-normiert sind (siehe
  Terrain T-1) → nicht kommunenübergreifend vergleichbar.
- **V-E 🟡 — Doppelzählung vulnerabler Gruppen.** `EXPECTED_ANNUAL_MORTALITY` führt sowohl
  `VULNERABLE_GROUPS_SHARE` als auch `HEAT_SENSITIVITY` (das `share_vuln` bereits enthält) in
  seiner g(V̂)-Liste → der vulnerable Anteil wirkt doppelt.

---

### Gruppe A — Bevölkerung & Gesundheit

#### `VULNERABLE_GROUPS_SHARE` — Anteil vulnerabler Gruppen [%, norm 0..50]
- **Was.** Anteil sozial/gesundheitlich besonders verwundbarer Personen (Alte + Kinder) an
  der Zellbevölkerung. Kernsensitivität für Hitze-Gesundheit und soziale Ungleichheit.
- **Wie.** `share_vuln = min(100; share_over_65 + share_under_18)` je Zelle (Zensus), sonst
  regionaler Fallback (`indicators.py:87-88,236`). `V̂ = share_vuln/50` (norm_max=50).
- **Ketten.** Index: in Pfaden von `EXPECTED_ANNUAL_MORTALITY`,
  `SOCIAL_INEQUALITY_AMPLIFICATION_RISK_INDEX`. €: über g(V̂) derselben Risiken.
- **Review.** ✅ echte Zensus-Basis, sinnvoll. 🟡 `norm_max=50` ⇒ ab 50 % Vulnerable ist V̂
  gesättigt; in sehr alten Gemeinden früh am Anschlag.
- **Verbesserung.** —

#### `HEAT_SENSITIVITY` — Hitzesensitivität [Index]
- **Was.** Zusammengesetzte gesundheitliche Hitze-Empfindlichkeit einer Zelle aus
  Demografie, lokaler Überwärmung und Grünmangel. Treiber für Hitzemortalität/-morbidität.
- **Wie.** `clamp(share_vuln + uhi·6 + (1 − green_frac)·20; 0; 100)` (`indicators.py:248`):
  additive Kombination aus vulnerablem Anteil [%], UHI-ΔT [K] ×6 und Grünmangel ×20.
- **Ketten.** Index+€ von Mortalität, Morbidität, `EXPECTED_THERMAL_STRESS_HOURS`,
  `EXPECTED_POLLUTANT_EXPOSURE_HOURS`.
- **Review.** 🟠 Die Gewichte 6/20 sind unbelegte Modellwahl, und der `share_vuln`-Term
  **doppelt** mit `VULNERABLE_GROUPS_SHARE` in der Mortalitäts-g(V̂) (V-E). Dimensionsmix
  (%+K+Anteil) ist als Indexkonstruktion vertretbar, aber intransparent.
- **Verbesserung.** Gewichte an epidemiologische Evidenz koppeln (RKI-Hitzemortalität nach
  Alter/UHI) und die Demografie-Doppelung mit `VULNERABLE_GROUPS_SHARE` auflösen.

#### `INCOME_SOCIAL_RESILIENCE` — Soziale Resilienz (invers) [Index]
- **Was.** Sozioökonomische Widerstandsfähigkeit der Bewohner; hoher Wert = *geringe*
  Resilienz (wenig Mittel, um sich anzupassen/erholen).
- **Wie.** Mittel der verfügbaren Teilindizes (`_income_resilience`, `indicators.py:29-43`):
  `Miete/18·100`, `100 − Eigentümerquote`, `100 − min(Wohnfläche/60·100; 100)` (alle Zensus,
  0..100 geklemmt); fehlt alles → 45.
- **Ketten.** Index+€ von Mental-Health, Migrationskosten, Ressourcenkonflikt, sozialer
  Ungleichheit.
- **Review.** 🟡 Der Miet-Term wertet **hohe Miete als geringe Resilienz** — diskutabel
  (hohe Miete kann auch Wohlstand/hohe Lagequalität anzeigen). Referenz 18 €/m², 60 m² sind
  gesetzte Anker.
- **Verbesserung.** INKAR-Kaufkraft/Arbeitslosenquote (bereits geladen für die
  Kapazitäts-V!) direkt einbeziehen statt nur Miete/Eigentum/Fläche.

#### `HEALTHCARE_ACCESS` — Zugang Gesundheitsdienste (invers) [Index]
- **Was.** Verwundbarkeit durch **schlechte** Erreichbarkeit medizinischer Versorgung; hoch
  = weit entfernt/unterversorgt.
- **Wie.** `clamp(100·(1 − healthcare_access_score); 0; 100)` (`indicators.py:46-49`) —
  Inversion des Sonstige-Scores (der nach 🐞 B-Fix 2 metrisch korrekt ist).
- **Ketten.** Index+€ von Mortalität, Morbidität, Mental-Health, `MEDICAL_UNDERSUPPLY_…`.
- **Review.** ✅ nach Bugfix solide; profitiert direkt von der korrigierten Distanz.
- **Verbesserung.** —

#### `DISEASE_VECTOR_SUSCEPTIBILITY` — Krankheitsanfälligkeit Vektoren [Index]
- **Was.** Anfälligkeit für vektorübertragene Krankheiten (z. B. Stechmücken) — steigt mit
  stehendem Wasser und Wärme.
- **Wie.** `clamp(water_frac·100·(mean_temp/12); 0; 100)` (`indicators.py:250`).
- **Ketten.** Index+€ von `EXPECTED_ANNUAL_MORBIDITY`.
- **Review.** 🟠 `mean_temp` ist **Bundesland-konstant** (R-1) und `water_frac` ist der
  proximity-angereicherte Wert (`WATER_FRACTION`-Semantikbruch aus Phase 1) → Größe hängt an
  zwei schwachen Eingaben.
- **Verbesserung.** Reine Stillgewässerfläche (See/Teich statt Fluss) + DWD-Rastertemperatur
  am Zentroid.

#### `AIR_QUALITY_RISK` — Luftqualitätsrisiko [Index]
- **Was.** Verwundbarkeit durch verkehrs-/hitzebedingte Luftschadstoffe (oft hitzekoppelt).
- **Wie.** `clamp(imp_frac·60 + road_coverage·200; 0; 100)` (`indicators.py:249`).
- **Ketten.** Index+€ von `EXPECTED_POLLUTANT_EXPOSURE_HOURS`, `EXPECTED_WATER_AIR_POLLUTION`.
- **Review.** 🟠 dominiert vom `road_coverage·200` (bei road_cov≈0,3 schon 60) — ein grober,
  breitengrad-verzerrter Proxy (O-2); keine echte Emissions-/Immissionsgröße.
- **Verbesserung.** Umweltbundesamt-Luftdaten / Copernicus CAMS (kostenlos) als
  Plausibilisierung; Verkehrsmenge aus OSM-Straßenklasse statt reiner Fläche.

---

### Gruppe B — Gebäude, Material & Stadtklima

#### `BUILDING_STABILITY` — Gebäudestabilität (invers) [Index]
- **Was.** Physische Verwundbarkeit der Bausubstanz; hoher Wert = geringe Stabilität
  (älter/ungünstiger). Sensitivität für Gebäudeschäden.
- **Wie.** `clamp(50 + bldg_cov·20 + (10 wenn avg_height>18) + min(30; max(0; (aktuelles
  Jahr − Baujahr)/100·30)); 0; 100)` (`indicators.py:19-26`).
- **Ketten.** Index+€ nur von `EXPECTED_BUILDING_DAMAGE_EUR`.
- **Review.** 🟠 fragwürdige Terme: `avg_height>18 ⇒ +10` (höhere Gebäude sind oft
  *neuer/stabiler*, nicht verwundbarer); `bldg_cov·20` koppelt Verwundbarkeit an
  Bebauungsdichte (eher Exposition). *(Das früher hartcodierte `2024` ist behoben →
  `date.today().year`.)*
- **Verbesserung.** Auf Zensus-Baualter + Bautyp fokussieren; Höhen-/Dichteterm streichen
  oder begründen.

#### `MATERIAL_HEAT_SENSITIVITY` — Materialanfälligkeit Hitze [Index]
- **Was.** Hitzeempfindlichkeit versiegelter Materialien (Asphalt-Verformung,
  Schienenverzug) — Sensitivität für Verkehrsschäden bei Hitze.
- **Wie.** `clamp(imp_frac·100; 0; 100)` (`indicators.py:235`).
- **Ketten.** Index+€ von `EXPECTED_TRANSPORT_DAMAGE_EUR`, `EXPECTED_TRANSPORT_DISRUPTION_HOURS`.
- **Review.** 🟡 **identisch** zu `SEALING_DEGREE` (V-C) — dieselbe Zahl unter zwei Codes.
- **Verbesserung.** Differenzieren (z. B. Asphalt-/Schienenanteil aus OSM `surface=asphalt`)
  oder einen der beiden Codes als Alias kennzeichnen.

#### `SEALING_DEGREE` — Versiegelungsgrad [%]
- **Was.** Grad der Bodenversiegelung — Sensitivität für Kanalüberlastung (Abwasser).
- **Wie.** `clamp(imp_frac·100; 0; 100)` (`indicators.py:257`).
- **Ketten.** Index+€ von `EXPECTED_WASTEWATER_OUTAGE_HOURS`.
- **Review.** 🟡 identisch zu `MATERIAL_HEAT_SENSITIVITY` (V-C).
- **Verbesserung.** wie oben.

#### `UHI_INTENSITY` — Wärmeinselintensität [K, norm 0..8]
- **Was.** Städtische Überwärmung ΔT gegenüber dem Umland — verstärkt Hitzebelastung nachts.
- **Wie.** Direkt `round(uhi_delta; 2)` (`indicators.py:258`); `V̂ = uhi/8`. Die ΔT-Rechnung
  selbst (Aufheizung − Kühlung + Canyon) wird in Phase 4 (H) reviewt.
- **Ketten.** Index+€ nur von `EXPECTED_THERMAL_STRESS_HOURS`.
- **Review.** 🟡 überlappt mit dem `uhi`-Term in `HEAT_SENSITIVITY` (V-C).
- **Verbesserung.** —

#### `GREEN_SPACE_SHARE` — Grünflächenmangel (invers) [%]
- **Was.** **Mangel** an Grünflächen (trotz Code-Name „…SHARE"); hoch = wenig Grün =
  verwundbarer. Kühlungs-/Rückzugsdefizit.
- **Wie.** `clamp(100 − green_frac·100; 0; 100)` (`indicators.py:259`).
- **Ketten.** Index+€ von `EXPECTED_THERMAL_STRESS_HOURS`, `ECOSYSTEM_FRAGMENTATION_…`,
  `EXPECTED_ECOSYSTEM_SERVICE_LOSS`.
- **Review.** 🟡 Code-Name irreführend (Wert ist der Mangel, nicht der Anteil; der
  Anzeige-`name` „Grünflächenmangel (invers)" ist korrekt). Erbt die Coverage-Asymmetrie
  (O-1) über `green_frac`.
- **Verbesserung.** Code umbenennen (`GREEN_SPACE_DEFICIT`) für Klarheit.

---

### Gruppe C — Infrastruktur & System

#### `INFRA_CRITICALITY` — Kritikalität von Infrastrukturen [Index]
- **Was.** Systemkritikalität durch Dichte echter KRITIS-Assets in der Zelle (Energie,
  Wasser, TK, Gesundheit, Verkehr).
- **Wie.** `clamp(8·energy + 8·water + 6·comm + 10·health_score + 6·transport; 0; 100)`
  mit editierbaren Gewichten (`indicators.py:178-185`).
- **Ketten.** Index+€ von `EXPECTED_CI_OUTAGE_HOURS`, `EXPECTED_FUNCTIONAL_FAILURE_DURATION`.
- **Review.** ✅ echte Assetdichte (gut). 🟡 mischt Zählungen (energy/…·Gewicht) mit einem
  0..1-Score (`health_score·10`); Zelle ohne Assets → 0 (nicht neutral 50).
- **Verbesserung.** Einheitlich auf „gewichtete Assetzahl" bringen (Gesundheit als Anzahl
  statt Score).

#### `CRITICAL_INFRA_CONDITION` — Zustand kritischer Infrastruktur [Index]
- **Was.** Technischer Zustand/Alter kritischer Infrastruktur (schlecht = verwundbar).
- **Wie.** **Konstante 50,0** (`indicators.py:234`).
- **Ketten.** Index+€ von **8** Risiken (Transport-/Energie-/Telecom-/Wasser-Schäden +
  Ausfallstunden).
- **Review.** 🟠 (V-A) konstant → in 8 Risiken derselbe Beitrag, keine Differenzierung; im
  Index dämpfend (V̂=0,5).
- **Verbesserung.** Proxy aus **Zensus-Gebäudealter** + Assetdichte ableiten (beide
  vorhanden), sonst neutral halten und als „Modellannahme" kennzeichnen.

#### `REDUNDANCY_BACKUP` — Redundanzen/Backup (invers) [Index]
- **Was.** Fehlende Ausfallreserven (hoch = wenig Redundanz = verwundbar).
- **Wie.** **Konstante 50,0** (`indicators.py:246`).
- **Ketten.** Index+€ von 6 Risiken (Energie/Telecom-Schäden, diverse Ausfallstunden, Domino).
- **Review.** 🟠 (V-A) konstant.
- **Verbesserung.** Mangels Daten neutral + editierbar; ggf. Netzredundanz aus OSM-Topologie
  (Umspannwerksdichte) grob ableiten.

#### `INFRA_DEPENDENCY_CHAIN` — Infrastruktur-Abhängigkeiten [Index]
- **Was.** Funktionale Kopplung zwischen Infrastruktursystemen (Strom→Wasser→TK).
- **Wie.** **Konstante 50,0** (`indicators.py:247`).
- **Ketten.** Index+€ von 5 Risiken (CI-/Wasser-Ausfall, Funktionsausfall, Domino,
  Med-Unterversorgung).
- **Review.** 🟠 (V-A) konstant — konzeptionell schwer ortsaufzulösen.
- **Verbesserung.** Als bewusste Modellkonstante kennzeichnen; nicht vortäuschen, dass sie
  differenziert.

#### `SINGLE_SITE_DEPENDENCY` — Abhängigkeit von Einzelstandorten [Index]
- **Was.** Wirtschaftliche Klumpenbildung auf wenige (Industrie-)Standorte → hohe
  Ausfallwirkung.
- **Wie.** `clamp(industrial·200; 0; 100)` mit `industrial = max(0; imp − bldg_cov −
  road_cov)` (`indicators.py:242`).
- **Ketten.** Index+€ von `EXPECTED_SUPPLY_CHAIN_DISRUPTION_HOURS`,
  `EXPECTED_LOCATION_DISADVANTAGE_EUR`.
- **Review.** 🟠 erbt das schwache Industrie-**Residuum** (P1-3); Faktor 200 sättigt schon
  bei 50 % „Industrie".
- **Verbesserung.** OSM `landuse=industrial` direkt (P1-3-Fix) und echte Betriebskonzentration.

#### `SUPPLY_CHAIN_DEPENDENCY` — Abhängigkeit von Lieferketten [Index]
- **Was.** Abhängigkeit von externen Lieferketten (Vorprodukte, Logistik).
- **Wie.** **Konstante 50,0** (`indicators.py:243`).
- **Ketten.** Index+€ von 3 Risiken (Lieferketten-Ausfall, indirekte Verluste,
  Versorgungsengpass-Kosten).
- **Review.** 🟠 (V-A) konstant.
- **Verbesserung.** Kommunal kaum auflösbar; als Modellkonstante kennzeichnen.

#### `LEVEE_CONDITION` — Deichzustand (invers) [Index] — **tot (V-B)**
- **Was.** Baulicher Zustand/Vorhandensein von Deichen entlang hochwasserexponierter Lagen.
- **Wie.** Ableitung aus Deichnähe und Exposition: falls küstennah/gewässernah/muldig
  `clamp(baseline + 40·exposure·(1 − dyke_prox) − 25·dyke_prox; 0; 100)`, sonst `baseline`
  (30 Binnen / 50 Küste), mit `exposure = clamp(max(water_prox; twi_norm|1_Küste;
  depression))` (`indicators.py:210-220`).
- **Ketten.** **keine** — von 0 Risiken referenziert.
- **Review.** 🟠 (V-B) **toter Rechenaufwand**: nutzt `dyke_prox` (OSM-Deich-Fetch, nach
  🐞 B-Fix 2 metrisch korrekt) und Exposition, wird aber nirgends verwendet.
- **Verbesserung.** In `HEAVY_RAIN_FLOOD`-/Küstenrisiken als V aufnehmen (fachlich naheliegend)
  **oder** Indikator + zugehörigen Deich-Fetch entfernen.

---

### Gruppe D — Wasser & Boden

#### `WATER_STRESS_INDEX` — Wasserstressindex [Index]
- **Was.** Wasserstress aus hoher Nachfrage (Versiegelung, Bevölkerung) und geringer
  Verfügbarkeit (Trockenheit).
- **Wie.** `clamp(imp·40 + min(pop_density/4000; 1)·40 + dry_index·20; 0; 100)`
  (`indicators.py:252`).
- **Ketten.** Index+€ von **8** Risiken (Agrarschaden, Wasserausfall, Vegetationsschaden,
  hydrologischer Stress, …).
- **Review.** 🟠 `dry_index` ist der `hot_days`-Proxy (R-1); `pop_density/4000` sättigt bei
  4000 E/km² (großstädtisch) — für Kleinstädte kaum wirksam.
- **Verbesserung.** UFZ-SMI statt `dry_index`; Entnahme-/Dargebotsdaten (LAWA) falls verfügbar.

#### `GROUNDWATER_DEPENDENCY` — Grundwasserabhängigkeit [Index]
- **Was.** Abhängigkeit von Grundwasser (Land-/Forstwirtschaft, Ökosysteme) → Verwundbarkeit
  bei sinkenden Grundwasserständen.
- **Wie.** `clamp((farmland_frac + green_frac)·50; 0; 100)` (`indicators.py:251`).
- **Ketten.** Index+€ von Wasser-Schäden/-Ausfall, hydrologischem Stress, Niedrigwasser-
  Fischerei.
- **Review.** 🟡 reiner Landnutzungs-Proxy (Coverage-Asymmetrie O-1); keine echte
  Grundwasserflurabstand-Info.
- **Verbesserung.** BGR/Landes-Grundwasserflurabstände (teils offen) ergänzen.

#### `IRRIGATION_DEPENDENCY` — Bewässerungsabhängigkeit [Index]
- **Was.** Wie stark die lokale Landwirtschaft auf Bewässerung angewiesen ist (steigt mit
  Ackeranteil und Trockenheit).
- **Wie.** `clamp(farmland·100·(0,5 + dry_index/2); 0; 100)` (`indicators.py:253`).
- **Ketten.** Index+€ von Agrarschaden, Bodenverlust, Bodendegradation.
- **Review.** 🟠 `dry_index` = `hot_days`-Proxy (R-1); Kulturart (bewässerungsintensiv?)
  unberücksichtigt.
- **Verbesserung.** Invekos/CLC+-Kulturarten + UFZ-SMI.

#### `SOIL_SENSITIVITY` — Bodenempfindlichkeit [Index]
- **Was.** Empfindlichkeit der Böden gegen Erosion/Versalzung (Hang + Ackeranteil).
- **Wie.** `clamp(slope_factor·60 + farmland·40; 0; 100)` (`indicators.py:241`).
- **Ketten.** Index+€ von Agrarschaden, Bodenverlust, Bodendegradation, Ökosystem-Degradation.
- **Review.** 🟠 `slope_factor` ist **kommunerelativ** normiert (T-1/V-D) → nicht vergleichbar;
  keine Bodenart (BÜK).
- **Verbesserung.** BGR **BÜK200** (Bodenart/Erodierbarkeit, offen) + absolute Hangklassen.

#### `EROSION_SUSCEPTIBILITY` — Erosionsanfälligkeit [Index]
- **Was.** Anfälligkeit von Hängen/Böden für Abtrag (steil + wenig Vegetation).
- **Wie.** `clamp(slope_factor·100·(1 − green_frac); 0; 100)` (`indicators.py:254`).
- **Ketten.** Index+€ nur von `EXPECTED_HABITAT_LOSS`.
- **Review.** 🟠 `slope_factor` kommunerelativ (T-1/V-D); Coverage-Asymmetrie über `green`.
- **Verbesserung.** Absolute Hangklassen + BÜK-Erodierbarkeit; ggf. USLE-K-Faktor.

#### `SALTWATER_INTRUSION_RISK` — Salzwasserintrusionsrisiko [Index] — **tot (V-B)**
- **Was.** Risiko salzwasserbeeinflussten Grundwassers/Bodens in Küstennähe.
- **Wie.** **Konstante** 40 (Küste) / 10 (Binnen) (`indicators.py:256`).
- **Ketten.** **keine** — von 0 Risiken referenziert.
- **Review.** 🟠 (V-A + V-B) konstant **und** ungenutzt.
- **Verbesserung.** In Küsten-/Grundwasserrisiken verdrahten und aus Küstendistanz + Höhe
  ableiten, oder entfernen.

---

### Gruppe E — Ökologie & Fischerei

#### `BIODIVERSITY_RESILIENCE` — Biodiversitätsresilienz (invers) [Index]
- **Was.** Widerstandsfähigkeit der lokalen Biodiversität; hoch = geringe Resilienz (wenig
  naturnahe Fläche).
- **Wie.** `clamp(100 − (forest_frac + green_frac)·100·0,6; 0; 100)` (`indicators.py:240`).
- **Ketten.** Index+€ von 7 Risiken (Biodiversitäts-/Habitatverlust, Ökosystem-Degradation/
  -Fragmentierung, Ökosystemleistungen, Umwelt-Feedback).
- **Review.** 🟡 grober Naturnähe-Proxy (Coverage-Asymmetrie O-1); Faktor 0,6 gesetzt.
- **Verbesserung.** Schutzgebietsanteil (OSM `boundary=protected_area`, bereits erfassbar) +
  Habitatvielfalt.

#### `WILDFIRE_SUSCEPTIBILITY` — Waldbrandanfälligkeit [Index]
- **Was.** Ökologische Brandanfälligkeit (Waldanteil × Trockenheit).
- **Wie.** `clamp(forest_frac·100·(0,5 + dry_index/2); 0; 100)` (`indicators.py:239`).
- **Ketten.** Index+€ von Biodiversitätsverlust, Vegetationsschaden, Umwelt-Feedback.
- **Review.** 🟠 `dry_index` = `hot_days`-Proxy (R-1); keine Nadelwald-Differenzierung (obwohl
  brandrelevanter).
- **Verbesserung.** OSM `leaf_type=needleleaved` (P1/Forest-Vorschlag) + UFZ-SMI.

#### `FISHERIES_TEMPERATURE_SENSITIVITY` — Temp.-Empfindlichkeit Fischbestände [Index]
- **Was.** Empfindlichkeit von Fischbeständen gegen Gewässererwärmung/Niedrigwasser.
- **Wie.** `clamp(water_frac·100·(surface_water_heating/3); 0; 100)` (`indicators.py:263`).
- **Ketten.** Index+€ von Fischerei-Verlust, Fischbestandsstress, Niedrigwasser-Fischerei.
- **Review.** 🟠 `surface_water_heating` = Bundesland-`mean_temp`-Proxy (R-1); `water_frac`
  proximity-verunreinigt.
- **Verbesserung.** Stillgewässerfläche + LST-Wassertemperatur.

#### `AQUACULTURE_TECHNICAL_VULNERABILITY` — Anfälligkeit Aquakultur [Index]
- **Was.** Technische Verwundbarkeit von Aquakulturanlagen (Teiche, Becken).
- **Wie.** **Konstante 50,0** (`indicators.py:264`).
- **Ketten.** Index+€ nur von `EXPECTED_AQUACULTURE_DAMAGE_EUR`.
- **Review.** 🟠 (V-A) konstant.
- **Verbesserung.** Falls Aquakultur-Standorte in OSM (`landuse=aquaculture`) vorhanden, an
  deren Präsenz koppeln; sonst als Annahme kennzeichnen.

#### `FISHERIES_MANAGEMENT_CAPACITY` — Fischerei-Anpassungsfähigkeit (invers) [Index]
- **Was.** Kapazität für monitoringbasierte Bestandsbewirtschaftung; hoch = geringe Kapazität.
- **Wie.** **Konstante 45,0** (`indicators.py:265`).
- **Ketten.** Index+€ nur von `EXPECTED_FISHERIES_ECONOMIC_LOSS_EUR`.
- **Review.** 🟠 (V-A) konstant.
- **Verbesserung.** Als Modellkonstante kennzeichnen.

---

### Gruppe F — Governance & Kapazität (INKAR/OSM, invers)

#### `FINANCIAL_ADAPTATION_CAPACITY` — Finanzielle Anpassungskapazität (invers) [Index]
- **Was.** Finanzielle Mittel der Kommune für Anpassung; hoch = geringe Kapazität.
- **Wie.** `_derived_or`: User-Override › INKAR `financial_adaptation` (aus Steuerkraft/
  Arbeitslosigkeit je AGS) › Fallback 50 (`indicators.py:224-226`).
- **Ketten.** Index+€ von 6 €-Risiken (Gebäude-/Restaurierungs-/Migrations-/Standort-/
  verzögerte Kosten, indirekte Verluste).
- **Review.** ✅ echte INKAR-Sozioökonomie (kommunenscharf, invers korrekt). Kommune-weit
  konstant (kein Zellbezug — sachgerecht).
- **Verbesserung.** —

#### `PLANNING_IMPLEMENTATION_CAPACITY` — Planungs-/Umsetzungskapazität (invers) [Index]
- **Was.** Governance-/Verwaltungskapazität zur Umsetzung von Anpassung; hoch = gering.
- **Wie.** `_derived_or`: Override › INKAR `planning_capacity` › 50 (`indicators.py:227-229`).
- **Ketten.** Index+€ von Restaurierungskosten, Admin-Ausfall, verzögerten Kosten.
- **Review.** ✅ INKAR-basiert, kommunenscharf.
- **Verbesserung.** —

#### `EARLY_WARNING_SYSTEMS` — Frühwarnsysteme (invers) [Index]
- **Was.** Vorhandensein/Qualität von Frühwarnung; hoch = fehlend.
- **Wie.** aus dem gedämpften Notfall-Proxy `clamp(50 + (emergency_mgmt_derived − 50)·0,6)`,
  sonst 40 (`indicators.py:202-208`); `emergency_mgmt_derived = 100·(1 − emergency_access)`
  aus OSM-Feuerwehr/Rettungsnähe (nach 🐞 B-Fix 2 korrekt).
- **Ketten.** Index+€ von `EXPECTED_ANNUAL_INJURIES`, `EXPECTED_ANNUAL_AFFECTED_EVACUATED`.
- **Review.** 🟡 Frühwarnung wird nur als **gedämpfte Kopie** der Feuerwehrnähe modelliert
  (fachlich schwacher Zusammenhang), aber ehrlich als Proxy geführt.
- **Verbesserung.** Vorhandensein von Sirenen/`emergency=siren` (OSM) direkt zählen.

#### `EMERGENCY_MANAGEMENT` — Notfallmanagement (invers) [Index]
- **Was.** Kapazität des Katastrophen-/Rettungsmanagements; hoch = gering (weit von
  Feuerwehr/Rettung).
- **Wie.** `_derived_or`: Override › `100·(1 − emergency_access)` › 40 (`indicators.py:195-201`).
- **Ketten.** Index+€ von Verletzten, Betroffenen/Evakuierten, Admin-Ausfall.
- **Review.** ✅ echter OSM-Näheproxy (nach Bugfix korrekt); `None`→40 nur wenn im Gebiet
  keine Rettungsinfra gemappt.
- **Verbesserung.** Zusätzlich Feuerwehr-Typ/Größe gewichten.

---

### Sammelbefunde Sensitivitäten (Kurzliste)

- **V-A 🟠** — 7 konstante V (u. a. `CRITICAL_INFRA_CONDITION=50` in 8 Risiken) ⇒ keine
  Differenzierung, im Index dämpfend.
- **V-B 🟠** — 2 tote V (`LEVEE_CONDITION`, `SALTWATER_INTRUSION_RISK`) in keiner Kette;
  `LEVEE_CONDITION` samt Deich-Fetch verdrahten oder entfernen.
- **V-C 🟡** — Doppelformeln (`MATERIAL_HEAT_SENSITIVITY` ≡ `SEALING_DEGREE`; `UHI_INTENSITY`
  ⊂ `HEAT_SENSITIVITY`).
- **V-D 🟠** — mehrere V erben die kommunerelative Terrain-Normierung (T-1): `SOIL_SENSITIVITY`,
  `EROSION_SUSCEPTIBILITY`.
- **V-E 🟡** — Demografie-Doppelzählung in `EXPECTED_ANNUAL_MORTALITY`
  (`VULNERABLE_GROUPS_SHARE` + `HEAT_SENSITIVITY`).
- **R-1-Erbe 🟠** — `dry_index`/`mean_temp`-Proxys treiben `WATER_STRESS_INDEX`,
  `IRRIGATION_DEPENDENCY`, `WILDFIRE_SUSCEPTIBILITY`, `DISEASE_VECTOR_SUSCEPTIBILITY`,
  `FISHERIES_TEMPERATURE_SENSITIVITY` ⇒ UFZ-SMI/DWD-Raster wären der größte Hebel.
- **Positiv ✅** — INKAR-Kapazitäten (`FINANCIAL_/PLANNING_…`), OSM-Notfallnähe
  (`EMERGENCY_MANAGEMENT`), KRITIS-Dichte (`INFRA_CRITICALITY`) und die nach Bugfix korrekte
  `HEALTHCARE_ACCESS` sind echte, differenzierende Datenpfade.
- **🐞 kein offener Bug** in der V-Rechnung (das früher hartcodierte Jahr in
  `BUILDING_STABILITY` ist behoben).

---

## Schicht „Exposition" (Exposures E) — 24 Layer

Berechnet in `indicators.compute_cell_hev` (`engine/indicators.py:145-172`). E beschreibt
**was** an einem Ort dem Klimareiz ausgesetzt ist (Menschen, Gebäude, Assets, Flächen), in
**absoluten Einheiten** (Pers., m², Anzahl, ha).

**Wie E in beide Ketten eingeht (einmal zentral):**
- **Index (Kette 1):** `Ê = clamp((E − norm_min)/(norm_max − norm_min), 0, 1)`, dann Faktor
  im Pfadprodukt `w·Ĥ·Ê·V̂`. Die `norm_max`-Anker bestimmen, ab wann eine Exposition „voll"
  zählt (z. B. `POPULATION_DENSITY` bei 8000 E/km², `BUILDING_STOCK` bei 6000 m²).
- **€ (Kette 2):** Die Schadensfunktionen (`impact/monetary.py`, `health.py`, `environment.py`)
  lesen **NICHT die E-Indikatorwerte**, sondern **direkt die `ci`-Rohgrößen** als
  Assetmenge/Betroffenenzahl: Gebäude `bldg_cov·Fläche·€/m²`, KRITIS `*_count·€/Stück`,
  Flächen `frac·ha·€/ha`, Gesundheit `pop·Rate` (`ctx.pop`). E ist damit die **Index-Sicht**
  der Exposition; die **€-Sicht** ist eine parallele, aus derselben `ci` gespeiste Rechnung.
  Folge: Ein Override an einem E-Indikator (Norm/Formel) verändert den **Index**, nicht den
  **€-Schaden** — und E-Wert und €-Assetmenge können semantisch auseinanderlaufen (z. B.
  `POPULATION_DENSITY` [E, Dichte] vs. `pop` [€, absolute Zahl]).

**Schicht-übergreifende Befunde:**
- **E-A 🟠 — 2 tote E.** `BUILDING_USE_TYPES` (=`bldg_count`) und `HEALTHCARE_INFRASTRUCTURE`
  (=`healthcare_score·100`) werden von **0 Risiken** genutzt → keine Kette. `HEALTHCARE_
  INFRASTRUCTURE` ist zudem eine als *Exposition* fehlplatzierte Kopie der V `HEALTHCARE_
  ACCESS` und des Sonstige-`HEALTHCARE_ACCESS_GRID` (dreifach).
- **E-B 🟠 — Hazard-in-Exposition-Vermischung.** `LOCATION_HAZARD_ZONES` (×`max(depression,
  uhi/6)`), `FLOODPLAINS` (×`depression`), `EROSION_PRONE_SOILS` (×`slope`) mischen einen
  **Gefahren**-Term in die Exposition. Da im Index ohnehin `Ĥ·Ê·V̂` multipliziert wird,
  wandert die Gefahr so **doppelt** in den Term (einmal als Ĥ, einmal in Ê). Konzeptionell
  soll E nur „was ist exponiert" abbilden.
- **E-C 🟡 — `area_ha`-Faktor ist Identität.** Viele Flächen-E rechnen `area_ha·frac`; beim
  festen 100-m-Gitter ist `area_ha=1`, der Faktor also wirkungslos (latent nur bei anderer
  Zellgröße). Harmlos, aber irreführend beim Lesen.
- **E-D 🟡 — Dreifache Alters-/Vulnerabilitätssicht.** `AGE_STRUCTURE` (E), `VULNERABLE_
  GROUPS_POPULATION` (E) und `VULNERABLE_GROUPS_SHARE` (V) speisen sich alle aus
  `share_old/share_young`.

---

### Gruppe A — Bevölkerung

#### `POPULATION_DENSITY` — Bevölkerungsdichte [Pers./km², norm 0..8000]
- **Was.** Einwohner je km² in der Zelle — die wichtigste Exposition (in **13** Risiken),
  Grundgröße für alle personenbezogenen Schäden.
- **Wie.** `pop / area_km2` (`indicators.py:146`), mit `area_km2 = area_m2/1e6`. Für 100-m-
  Zellen: `pop/0,01 = pop·100`. `Ê = min(pop_density/8000; 1)`.
- **Ketten.** Index: 13 Risiken. €: die zugehörigen Gesundheits-/Migrationsfunktionen nutzen
  `ctx.pop` (absolute Zahl), nicht die Dichte.
- **Review.** ✅ echte Zensus-Basis. 🟡 `norm_max=8000` ist großstädtisch — ländliche/klein-
  städtische Zellen bleiben im Index niedrig, was fachlich korrekt, aber wenig spreizend ist.
- **Verbesserung.** —

#### `AGE_STRUCTURE` — Altersstruktur [%, norm 0..50]
- **Was.** Summe der Anteile Ältere + Kinder — demografische Exposition gegenüber Hitze.
- **Wie.** `share_over_65 + share_under_18` (`indicators.py:147`).
- **Ketten.** Index: nur 1 Risiko. €: —.
- **Review.** 🟡 überlappt inhaltlich mit `VULNERABLE_GROUPS_SHARE` (V) und `VULNERABLE_
  GROUPS_POPULATION` (E) (E-D); nur ein Nutzer.
- **Verbesserung.** Konsolidieren (eine Alters-Exposition genügt).

#### `VULNERABLE_GROUPS_POPULATION` — Vulnerable Gruppen [Pers., norm 0..2000]
- **Was.** Absolute Zahl vulnerabler Personen (Alte+Kinder) in der Zelle — Betroffenenbasis
  für Gesundheits-/Sozialrisiken.
- **Wie.** `pop · share_vuln / 100` (`indicators.py:149`).
- **Ketten.** Index: 5 Risiken. €: die Gesundheitsfunktionen nutzen `ctx.pop`·Rate (nicht
  diesen Wert direkt).
- **Review.** ✅ sinnvoll; erbt die share-Basis.
- **Verbesserung.** —

#### `OUTDOOR_THERMAL_EXPOSURE` — Aufenthalt im Freien [h/Tag, norm 0..8]
- **Was.** Geschätzte Stunden im Freien pro Tag — Näherung, wie lange Menschen der
  Außenhitze ausgesetzt sind.
- **Wie.** `2,0 + 3,0·green_frac` (`indicators.py:148`): 2 h Basis + bis 3 h mehr bei viel Grün.
- **Ketten.** Index: 2 Risiken (thermischer Stress, Schadstoffexposition). €: —.
- **Review.** 🟠 fragwürdige Richtung: **mehr Grün ⇒ mehr Außen-Exposition** — Grün ist aber
  auch kühlend/schützend; die Kopplung an `green_frac` ist ein schwacher Proxy für
  „Verweildauer draußen".
- **Verbesserung.** An Park-/Erholungsflächen (OSM `leisure`) + Bevölkerung koppeln statt an
  den Grünanteil generell; oder als grobe Konstante führen.

---

### Gruppe B — Gebäude & Wirtschaft

#### `BUILDING_STOCK` — Gebäudebestand [m², norm 0..6000]
- **Was.** Von Gebäuden bedeckte Fläche der Zelle (m²) — physische Substanz, die z. B.
  Starkregen/Sturm ausgesetzt ist.
- **Wie.** `bldg_cov · area_m2` (`indicators.py:150`); für 100-m-Zellen `bldg_cov·10000`.
  `Ê` sättigt bei `bldg_cov≈0,6` (norm_max 6000).
- **Ketten.** Index: 3 Risiken. €: `EXPECTED_BUILDING_DAMAGE_EUR` nutzt `bldg_cov·Fläche·
  Geschosse·€/m²` (dieselbe `bldg_cov`).
- **Review.** ✅ konsistent zwischen Index und €.
- **Verbesserung.** —

#### `BUILDING_USE_TYPES` — Nutzungstypen [Anzahl, norm 0..200] — **tot (E-A)**
- **Was.** Sollte Nutzungsvielfalt (Wohnen/Gewerbe/kritisch) abbilden.
- **Wie.** `float(bldg_count)` (`indicators.py:151`) — schlicht die Gebäudezahl, keine
  Nutzungstypen.
- **Ketten.** **keine** (0 Risiken).
- **Review.** 🟠 (E-A) tot **und** Formel↔Name-Divergenz (zählt Gebäude, nicht Typen).
- **Verbesserung.** Entweder echte Nutzungsmischung aus OSM `building=*` ableiten und
  verdrahten, oder entfernen.

#### `LOCATION_HAZARD_ZONES` — Lage in Gefahrenzonen [ha, norm 0..1]
- **Was.** Bebaute Fläche, die zusätzlich in einer Gefahrenlage (Mulde/Hitzeinsel) liegt.
- **Wie.** `area_ha · bldg_cov · max(depression_factor; min(uhi/6; 1))` (`indicators.py:152`).
- **Ketten.** Index: 5 Risiken. €: —.
- **Review.** 🟠 (E-B) mischt Gefahr (`depression`/`uhi`) in die Exposition → im Index
  doppelte Gefahrengewichtung; erbt zudem T-1 über `depression`.
- **Verbesserung.** Reine bebaute Fläche als E; die Gefahrenlage über den H-Faktor im Pfad
  wirken lassen.

#### `INDUSTRIAL_COMMERCIAL_AREAS` — Industrie-/Gewerbeflächen [ha, norm 0..1]
- **Was.** Fläche mit Industrie/Gewerbe — Exposition wirtschaftlicher Aktivität.
- **Wie.** `area_ha · industrial`, `industrial = max(0; imp − bldg_cov − road_cov)`
  (`indicators.py:160`).
- **Ketten.** Index: 3 Risiken. €: —.
- **Review.** 🟠 erbt das schwache Industrie-Residuum (P1-3).
- **Verbesserung.** OSM `landuse=industrial/commercial` direkt.

#### `SUPPLY_CHAIN_NODES` — Lieferkettenknoten [Anzahl, norm 0..10]
- **Was.** Näherung für logistische Knoten (Betriebe/Lager) in der Zelle.
- **Wie.** `industrial·6 + bldg_count·0,004` (`indicators.py:162`) — willkürliche Linearkombi.
- **Ketten.** Index: 3 Risiken. €: —.
- **Review.** 🟠 unbelegte Koeffizienten (6; 0,004); mischt Residuum-Industrie und Gebäudezahl.
- **Verbesserung.** OSM `landuse=industrial` + `building=warehouse`/Logistik-Tags echt zählen.

---

### Gruppe C — Kritische Infrastruktur (KRITIS)

Alle vier aktiven zählen OSM-Assets in der Zelle (nach demselben Muster wie die Sonstige-
Counts); die zugehörigen €-Schäden nutzen genau diese `*_count`.

#### `ENERGY_INFRASTRUCTURE` — Energieanlagen [Anzahl, norm 0..20]
- **Was.** Zahl energiewirtschaftlicher Anlagen in der Zelle.
- **Wie.** `float(energy_infra_count)` (`indicators.py:153`).
- **Ketten.** Index: 7 Risiken. €: `EXPECTED_ENERGY_INFRA_DAMAGE_EUR` = `energy_infra_count·
  800 000 €·Verlustrate·Kurve·g(V̂)`.
- **Review.** ✅ echte Assetzählung, Index↔€ konsistent.
- **Verbesserung.** Typgewichtung (Kraftwerk≫Trafo) im €-Review (Phase 5).

#### `WATER_WASTEWATER_INFRA` — Wasser/Abwasseranlagen [Anzahl, norm 0..20]
- **Was.** Zahl der Wasser-/Abwasseranlagen.
- **Wie.** `float(water_wastewater_count)` (`indicators.py:154`).
- **Ketten.** Index: 7 Risiken. €: `…WATER_WASTEWATER_DAMAGE_EUR` = `count·600 000 €·…`.
- **Review.** ✅.
- **Verbesserung.** —

#### `TRANSPORT_HUBS` — Verkehrsknotenpunkte [Anzahl, norm 0..20]
- **Was.** Zahl der Verkehrsknoten (Bahnhöfe/ÖPNV-Stationen) in der Zelle.
- **Wie.** `float(transport_hub_count)`; `transport_hub_count` = Zahl der OSM-`transport_
  points`, deren Punkt in der Zelle liegt (`osm_data.py:1234-1242`).
- **Ketten.** Index: 2 Risiken. €: `EXPECTED_TRANSPORT_DAMAGE_EUR` = `count·500 000 €·…`.
- **Review.** ✅ echte Knotenzählung (der frühere `road_cov·18`-Proxy lag im entfernten
  Assessor). 🟡 Punkt-in-Zelle verliert linienhafte Verkehrsinfrastruktur (Gleise, Brücken).
- **Verbesserung.** Zusätzlich `railway=*`/Brücken-Linienlänge je Zelle.

#### `COMMUNICATION_INFRA` — Kommunikationsinfrastruktur [Anzahl, norm 0..10]
- **Was.** Zahl der TK-Masten/-Knoten in der Zelle.
- **Wie.** `float(communication_count)` (`indicators.py:156`).
- **Ketten.** Index: 3 Risiken. €: `EXPECTED_TELECOM_DAMAGE_EUR` = `count·400 000 €·…`.
- **Review.** ✅.
- **Verbesserung.** —

#### `HEALTHCARE_INFRASTRUCTURE` — Gesundheitsversorgung [Index, norm 0..100] — **tot (E-A)**
- **Was.** Erreichbarkeit der Gesundheitsversorgung, als Exposition geführt.
- **Wie.** `healthcare_access_score·100` (`indicators.py:157-159`).
- **Ketten.** **keine** (0 Risiken).
- **Review.** 🟠 (E-A) tot; zudem **konzeptionell falsch** als Exposition (ist eine
  Kapazität/Vulnerabilität — existiert bereits als V `HEALTHCARE_ACCESS`).
- **Verbesserung.** Entfernen (V deckt es ab).

---

### Gruppe D — Natur- und Bodenflächen

#### `AGRICULTURAL_LAND` — Landwirtschaftliche Nutzfläche [ha, norm 0..1]
- **Was.** Ackerfläche der Zelle — Exposition für Dürre-/Ernteschäden.
- **Wie.** `area_ha · farmland_frac` (`indicators.py:161`); 100-m-Zelle ⇒ = `farmland_frac`.
- **Ketten.** Index: 6 Risiken. €: `EXPECTED_AGRICULTURAL_DAMAGE_EUR` = `farmland_frac·1 ha·
  12 000 €·…`.
- **Review.** ✅ Index↔€ konsistent; erbt Coverage-Asymmetrie (O-1).
- **Verbesserung.** wie Phase 1 (CLC+/Invekos-Kulturarten).

#### `FOREST_AREA` — Waldflächen [ha, norm 0..1]
- **Was.** Waldfläche der Zelle — Exposition für Waldbrand/Ökosystemleistungen (8 Risiken).
- **Wie.** `area_ha · forest_frac` (`indicators.py:163`).
- **Ketten.** Index: 8 Risiken. €: Ökosystem-/Vegetationsfunktionen nutzen `(forest+green)`.
- **Review.** ✅; Coverage-Asymmetrie (O-1); keine Nadel-/Laub-Trennung.
- **Verbesserung.** `leaf_type` (OSM) für Brandrisiko.

#### `BIODIVERSITY_HOTSPOTS` — Biodiversitäts-Hotspots [ha, norm 0..1]
- **Was.** Näherung für artenreiche Flächen (Wald + Wasser).
- **Wie.** `area_ha · (forest_frac + water_frac)·0,5` (`indicators.py:164`).
- **Ketten.** Index: 4 Risiken. €: Umweltfunktionen über Naturfläche.
- **Review.** 🟡 grober Proxy (Wald+Wasser ≠ Hotspot); Faktor 0,5 gesetzt.
- **Verbesserung.** OSM `boundary=protected_area`/Natura-2000 (offen) statt Wald+Wasser.

#### `EROSION_PRONE_SOILS` — Erosionsgefährdete Flächen [ha, norm 0..1]
- **Was.** Ackerfläche in Hanglage — erosionsexponiert.
- **Wie.** `area_ha · farmland_frac · slope_factor` (`indicators.py:165`).
- **Ketten.** Index: 2 Risiken. €: —.
- **Review.** 🟠 (E-B) mischt `slope` (Gefahr/T-1) in die Exposition; kommunerelativ (T-1).
- **Verbesserung.** BÜK-Erodierbarkeit + absolute Hangklassen.

#### `GROUNDWATER_DEPENDENT_ECOSYSTEMS` — GW-abhängige Ökosysteme [ha, norm 0..1]
- **Was.** Feuchte-/grundwassernahe Naturflächen, die bei sinkendem Grundwasser leiden.
- **Wie.** `area_ha · (forest_frac + green_frac)·(0,3 + water_adj)` (`indicators.py:169`).
- **Ketten.** Index: 3 Risiken. €: Umweltfunktion.
- **Review.** 🟡 Proxy; `water_adj` proximity-basiert.
- **Verbesserung.** Feuchtgebiets-Tags (OSM `natural=wetland`) direkt.

---

### Gruppe E — Wasser, Küste & Fischerei

#### `FLOODPLAINS` — Überschwemmungsflächen [ha, norm 0..1]
- **Was.** Überflutungsgefährdete Zellfläche (muldig/gewässernah).
- **Wie.** `area_ha · depression_factor · max(water_prox; 0,3 wenn water_adj>0 sonst 0,1)`
  (`indicators.py:167`).
- **Ketten.** Index: 3 Risiken. €: —.
- **Review.** 🟠 (E-B) `depression` (Gefahr, T-1) in der Exposition; ansonsten plausibel.
- **Verbesserung.** Amtliche HW-Gefahrenflächen (Länder-WMS, teils offen) statt DEM-Proxy.

#### `COASTAL_RIPARIAN_ZONES` — Küsten-/Uferzonen [ha, norm 0..1]
- **Was.** Ufernahe Zellfläche — Exposition für Ufer-/Küstenprozesse.
- **Wie.** `area_ha · max(water_adj; water_prox) · (0,5 + 0,5·twi_norm)` (`indicators.py:166`).
- **Ketten.** Index: 1 Risiko. €: —.
- **Review.** 🟡 `twi_norm` kommunerelativ (T-1).
- **Verbesserung.** absolute Ufer-Puffer (Distanzband) statt TWI-Gewicht.

#### `COASTAL_STORM_SURGE_EXPOSURE` — Küstennähe/Sturmflut [ha, norm 0..1] (`spatial=false`)
- **Was.** Bebaute Fläche in Küstenkommunen als Sturmflut-Exposition.
- **Wie.** `area_ha · bldg_cov` wenn Küste, sonst 0 (`indicators.py:168`).
- **Ketten.** Index: 2 Risiken. €: —.
- **Review.** 🟡 keine echte Höhen-/Distanz-Differenzierung an der Küste (nur „Küste ja/nein"
  × Bebauung).
- **Verbesserung.** DEM-Höhe + Küstendistanz (beide vorhanden) für echtes Sturmflut-Niveau.

#### `FISHERIES_AQUACULTURE_AREAS` — Fischerei-/Aquakulturbetriebe [Anzahl, norm 0..5]
- **Was.** Näherung für fischereiwirtschaftliche Nutzung der Zelle.
- **Wie.** `water_frac · 5,0` (`indicators.py:170`) — reine Skalierung des Wasseranteils.
- **Ketten.** Index: 4 Risiken. €: Fischerei-/Aquakulturschäden nutzen `water_frac`·€/ha.
- **Review.** 🟠 Einheit „Anzahl", aber Formel liefert einen Wasseranteil×5 (kein
  Betriebszähler); `water_frac` proximity-verunreinigt (Phase 1).
- **Verbesserung.** OSM `landuse=aquaculture`/Fischerei-Tags echt zählen; sonst reine
  Wasserfläche.

#### `FISH_SPAWNING_HABITATS` — Laich-/Aufwuchsgebiete [ha, norm 0..1]
- **Was.** Gewässernahe Flächen mit Laichfunktion.
- **Wie.** `area_ha · max(water_frac; water_prox·0,5)` (`indicators.py:171`).
- **Ketten.** Index: 2 Risiken. €: —.
- **Review.** 🟡 Proxy; keine Habitatqualität.
- **Verbesserung.** Fließgewässer-Renaturierungs-/Schutzstatus (falls offen verfügbar).

---

### Sammelbefunde Exposition (Kurzliste)

- **E-A 🟠** — 2 tote E (`BUILDING_USE_TYPES`, `HEALTHCARE_INFRASTRUCTURE`); letzteres zudem
  als Exposition fehlplatziert (ist V).
- **E-B 🟠** — Hazard-in-Exposition: `LOCATION_HAZARD_ZONES`, `FLOODPLAINS`,
  `EROSION_PRONE_SOILS` mischen `depression`/`uhi`/`slope` ein → im Index doppelte
  Gefahrengewichtung; teils T-1-Erbe.
- **E-C/E-D 🟡** — `area_ha`-Faktor wirkungslos beim 100-m-Gitter; Alters-/Vulnerabilitäts-
  Sicht dreifach (`AGE_STRUCTURE`/`VULNERABLE_GROUPS_POPULATION`/V `…SHARE`).
- **Formel↔Name/Einheit-Divergenzen 🟠** — `BUILDING_USE_TYPES` (zählt Gebäude, nicht Typen),
  `FISHERIES_AQUACULTURE_AREAS` (Wasseranteil statt „Anzahl").
- **Positiv ✅** — KRITIS-Zählungen (`ENERGY_/WATER_/TRANSPORT_/COMMUNICATION_…`) und
  `BUILDING_STOCK`/`AGRICULTURAL_LAND`/`FOREST_AREA` sind echte, Index↔€-konsistente
  Asset-/Flächenexpositionen aus realen OSM/Zensus-Daten.
- **🐞 kein neuer Bug** in der E-Rechnung.

---

## Schicht „Einflüsse" (Hazards H) — 23 Layer

Berechnet in `indicators.compute_cell_hev` (`engine/indicators.py:93-142`) aus dem
`regional`-Kontext (Klimatreiber) × lokalen `ci`-Modulatoren. H ist die **Reizstärke** in
absoluter Einheit (°C, Tage/Jahr, mm, Index).

**Wie H in beide Ketten eingeht (einmal zentral):**
- **Index (Kette 1):** `Ĥ = clamp((H − norm_min)/(norm_max − norm_min), 0, 1)` mit den
  **editierbaren** Screening-Normgrenzen, dann Faktor im Pfad `w·Ĥ·Ê·V̂`.
- **€ (Kette 2):** über `impact/base.haz_intensity(code)` = Normierung mit **FIXEN Katalog-
  Grenzen** (entkoppelt von Screening-Overrides, §3.3-Fix). Daraus:
  - **monetär:** konvexe Schadenskurve `damage_fraction = haz_intensity^exponent`
    (Exponent 1,5) — die €-Funktion nimmt das **Maximum** über ihre Hazard-Liste.
  - **Gesundheit:** nichtlineare attributable Fraktion `AF = 1 − exp(−β·(Intensität −
    Schwelle)₊)` (Hitze: β≈0,0008, Schwelle 8 Hitzetage) — Nichtlinearität aus der Schwelle.
  Ein Screening-Norm-Override verschiebt damit den **Index**, nicht die absoluten **€**.

**Der zentrale Treiber: UHI-ΔT (`compute_uhi_delta`, `inputs.py:87-119`).** Speist
`HEAT_WAVE`, `COLD_EXTREME`, `MEAN_TEMPERATURE_RISE` (H) sowie `HEAT_SENSITIVITY`,
`UHI_INTENSITY` (V). Formel (K), Operator für Operator:
```
imp        = clamp(bldg_cov + road_cov·0,95 ; 0,02..0,98)   (sonst Landnutzungs-Versiegelung)
height_f   = min(avg_height/15 ; 2)
bldg_f     = bldg_cov · height_f
meadow     = max(0 ; green − forest)
uhi_base   = α·(1−albedo)·imp + β·bldg_f
green_cool = γ·forest·1,8 + γ·meadow + γ·farmland·0,5
water_cool = δ·water
tree_cool  = tree_coef·canopy·10
canyon     = ε·(1−svf)·height_f
ΔT = max(0 ; uhi_base − green_cool − water_cool − tree_cool + canyon)
```
Koeffizienten editierbar (`uhi_coefficients`): α=6, β=2, γ=3,5, δ=2, ε=1,5, tree=0,3.
**Review UHI 🟠:** heuristisches Additivmodell (K entsteht nur aus den Koeffizienten, keine
Energiebilanz); erbt die Lücken von `avg_height` (oft 0 → `bldg_f`/`canyon`≈0) und
`tree_canopy` (spärlich). Als kalibrierbares Screening vertretbar, aber nicht als absolute
Temperatur. **Verbesserung:** Koeffizienten gegen Messkampagnen/LST plausibilisieren;
`avg_height`-Fallback aus Zensus-Geschossen.

**Schicht-übergreifende Befunde:**
- **H-A 🟠 — 6 tote H.** `OCEAN_ACIDIFICATION`, `GLACIER_SNOW_LOSS`, `PERMAFROST_THAW`,
  `TROPICAL_CYCLONE`, `SALTWATER_INTRUSION`, `COASTAL_EROSION` werden von **0 Risiken**
  genutzt. `GLACIER_SNOW_LOSS` wird sogar berechnet, `PERMAFROST_THAW` ist konstant 0.
- **H-B 🟠 — `CASCADE_EVENT` = 0,3 konstant in 11 Risiken.** Ein fixer Ĥ=0,3-Beitrag (im
  Index) ohne jede Ortsauflösung; `COMPOUND_EVENT` ist dagegen sauber berechnet
  (`max` der normierten Bestandteile).
- **H-C 🟠 — T-1 erreicht die meistgenutzten Hazards.** `HEAVY_RAIN_FLOOD` (**26** Risiken)
  nutzt `twi_norm`+`depression`, `LANDSLIDE` `slope_factor` — alle **kommunerelativ**
  min–max-normiert (Terrain T-1) → nicht kommunenübergreifend vergleichbar.
- **H-D 🟠 — R-1 erreicht Dürre/Hitze-Hazards.** `DROUGHT` (**26**), `SOIL_MOISTURE_DECLINE`,
  `WILDFIRE`, `SURFACE_WATER_HEATING`, `MEAN_TEMPERATURE_RISE` hängen an den `hot_days`/
  `mean_temp`-Proxys → Dürre kann nie von Hitze abweichen (größter inhaltlicher Hebel).

---

### Gruppe A — Temperatur & Hitze

#### `HEAT_WAVE` — Hitzewellen [Tage/Jahr ≥30 °C, norm 0..40]
- **Was.** Zahl der Hitzetage inkl. städtischer Verstärkung — der wichtigste Gesundheits-
  treiber (in **20** Risiken).
- **Wie.** `clamp(hot_days + uhi·1,5 ; 0 ; 40)` (`indicators.py:107`): reale DWD-Hitzetage +
  1,5×UHI-ΔT.
- **Ketten.** Index: 20 Risiken. €: Gesundheit über `AF(hot_days)` (absolute Hitzetage,
  Schwelle 8); monetär (Gebäude/Hitze) über die Schadenskurve.
- **Review.** ✅ bester Hazard (echte Daten + lokale UHI). 🟡 `uhi·1,5` addiert K-basierte
  UHI zu Tagen (Dimensionsmix), aber als Verstärkungsterm vertretbar.
- **Verbesserung.** —

#### `COLD_EXTREME` — Kälteextreme [Tage/Jahr, norm 0..40]
- **Was.** Frosttage, leicht gemindert durch städtische Wärme.
- **Wie.** `frost_days · (1 − 0,3·min(uhi/5 ; 1))` (`indicators.py:108`).
- **Ketten.** Index: 1 Risiko. €: gering.
- **Review.** ✅ plausibel (Stadt wärmer → weniger Frost); reale `frost_days`.
- **Verbesserung.** —

#### `MEAN_TEMPERATURE_RISE` — Mittlerer Temperaturanstieg [°C, norm 0..3]
- **Was.** Langfristiger Temperaturtrend als schleichender Einfluss.
- **Wie.** `mean_temp_rise + uhi·0,08` (`indicators.py:94`).
- **Ketten.** Index: 5 Risiken. €: gering.
- **Review.** 🟠 `mean_temp_rise` ist Bundesland-`mean_temp`-Proxy (R-1); der `uhi·0,08`-
  Zuschlag ist marginal.
- **Verbesserung.** DWD-Klimaatlas/C3S-Delta am Zentroid.

---

### Gruppe B — Wasser & Niederschlag

#### `HEAVY_RAIN_FLOOD` — Starkregen/Sturzflut [Index 0..100]
- **Was.** Sturzflut-/Überflutungsneigung aus Starkregen, Versiegelung und Geländeform —
  der meistgenutzte Hazard (**26** Risiken).
- **Wie.** `clamp(heavy_rain_index · (0,4 + imp) · (0,5 + 0,5·twi_norm) · (0,6 + depression) ;
  0 ; 100)` (`indicators.py:109-111`).
- **Ketten.** Index: 26 Risiken. €: Gebäude-/Infrastruktur-/Transport-Schäden über die
  Schadenskurve auf `haz_intensity(HEAVY_RAIN_FLOOD)`.
- **Review.** 🟠 (H-C) `twi_norm`+`depression` sind kommunerelativ (T-1) → der wichtigste
  Flut-Hazard ist nicht kommunenübergreifend vergleichbar; `heavy_rain_index` selbst ist
  aber real (DWD-CDC).
- **Verbesserung.** `twi`/`depression` mit **absoluten** Referenzgrenzen normieren (T-1-Fix);
  optional amtliche HW-Gefahrenflächen.

#### `DROUGHT` — Dürre [Tage/Jahr, norm 0..60]
- **Was.** Trockenperioden-Belastung, verstärkt durch Vegetations-/Ackeranteil (Wasserbedarf).
- **Wie.** `clamp(drought_days · (0,6 + 0,7·(farmland + green)) ; 0 ; 60)` (`indicators.py:112`).
- **Ketten.** Index: **26** Risiken. €: Agrar-/Boden-/Ökosystemschäden.
- **Review.** 🟠 (H-D) `drought_days = 8 + hot_days·1,2` → reine Hitzefunktion; Dürre und
  Hitze bewegen sich immer gleich.
- **Verbesserung.** UFZ-Dürremonitor-SMI (kostenlos) — der wirksamste Einzelfix der Kette.

#### `SOIL_MOISTURE_DECLINE` — Bodenfeuchte-Rückgang [mm, norm 0..80]
- **Was.** Rückgang der Bodenfeuchte als Boden-/Landwirtschaftstreiber.
- **Wie.** `soil_moisture_decline · (0,5 + 0,6·(farmland + green))` (`indicators.py:106`).
- **Ketten.** Index: 2 Risiken. €: Bodenschäden.
- **Review.** 🟠 (H-D) `soil_moisture_decline = 20 + hot_days` (Proxy); Coverage-Asymmetrie
  über `green`.
- **Verbesserung.** UFZ-SMI.

#### `LOW_FLOW_NIEDRIGWASSER` — Niedrigwasser [Tage/Jahr, norm 0..60]
- **Was.** Niedrigwasserdauer (Schifffahrt, Kühlwasser, Ökologie).
- **Wie.** `clamp(low_flow_days · (0,6 + 0,4·dry) · (1 + 0,3·water_prox) ; 0 ; 60)`
  (`indicators.py:131-133`).
- **Ketten.** Index: 4 Risiken. €: Fischerei/Wasser.
- **Review.** ✅ `low_flow_days` real (PEGELONLINE); `dry` (Proxy) nur als Modulator.
- **Verbesserung.** Pegelferne Kommunen (Phase 1 P-Verbesserung).

#### `SURFACE_WATER_HEATING` — Gewässererwärmung [°C, norm 0..5]
- **Was.** Erwärmung offener Gewässer (Fischerei/Ökologie).
- **Wie.** `surface_water_heating · (0,5 + water_frac)` (`indicators.py:130`).
- **Ketten.** Index: 3 Risiken. €: Fischerei/Aquakultur.
- **Review.** 🟠 (H-D) `surface_water_heating` = `mean_temp`-Proxy; `water_frac` proximity-
  verunreinigt.
- **Verbesserung.** LST-Wassertemperatur.

---

### Gruppe C — Sturm

#### `EXTRATROPICAL_STORM` — Winterstürme [Anzahl/Jahr, norm 0..12]
- **Was.** Häufigkeit außertropischer Stürme, lokal durch Exponiertheit moduliert.
- **Wie.** `storm_days · (0,8 + 0,5·vent_score)` (`indicators.py:114`).
- **Ketten.** Index: 9 Risiken. €: Gebäude-/Energie-/Telecom-Schäden.
- **Review.** 🟠 `storm_days` meist Konstante 6 (ERA5 optional) → Differenzierung nur über
  `vent_score`.
- **Verbesserung.** ERA5-Sturmklimatologie ausrollen.

#### `TROPICAL_CYCLONE` — Tropische Wirbelstürme [Anzahl/Jahr] — **tot (H-A)**
- **Was.** In DE praktisch irrelevant (Restläufer).
- **Wie.** **Konstante 0,05** (`indicators.py:113`).
- **Ketten.** **keine** (0 Risiken).
- **Review.** 🟠 (H-A) tot.
- **Verbesserung.** Entfernen (für DE nicht sinnvoll).

#### `STORM_SURGE` — Sturmflut [Anzahl/Jahr, norm 0..6]
- **Was.** Sturmflutereignisse an der Küste.
- **Wie.** **Konstante 2,0** wenn Küste, sonst 0 (`indicators.py:115`).
- **Ketten.** Index: 1 Risiko. €: —.
- **Review.** 🟠 konstant (keine Höhen-/Pegel-Differenzierung).
- **Verbesserung.** BSH-Sturmflutstatistik je Küstenabschnitt.

---

### Gruppe D — Feuer, Hang & Boden

#### `WILDFIRE` — Waldbrand [Index 0..100]
- **Was.** Waldbrandgefahr aus Waldanteil × Trockenheit.
- **Wie.** `clamp(forest_frac·100 · (0,4 + dry_index) ; 0 ; 100)` (`indicators.py:116`).
- **Ketten.** Index: 7 Risiken. €: Vegetations-/Biodiversitätsschäden.
- **Review.** 🟠 (H-D) `dry_index` = `hot_days`-Proxy; keine Nadelwald-/Windkopplung.
- **Verbesserung.** UFZ-SMI + `leaf_type`; ggf. Waldbrandindex (DWD WBI, offen).

#### `LANDSLIDE` — Hangrutschung [Index 0..100]
- **Was.** Rutschungsneigung aus Hang × Starkregen.
- **Wie.** `clamp(slope_factor·100 · (heavy_rain_index/100) ; 0 ; 100)` (`indicators.py:117`).
- **Ketten.** Index: 1 Risiko. €: —.
- **Review.** 🟠 (H-C) `slope_factor` kommunerelativ (T-1).
- **Verbesserung.** Absolute Hangklassen + Bodenart (BÜK).

#### `SOIL_SALINIZATION` — Bodenversalzung [Index 0..1]
- **Was.** Versalzungsneigung (küstennah durch Salzwasser, binnen durch Verdunstung in
  Mulden/Trockenheit).
- **Wie.** Produkt aus Küsten-/Binnen-Basiswert × `(0,35+0,65·depression)` ×
  `(0,45+0,55·farmland)` × `(0,55+0,45·dry)` × Küsten-/Höhenterm (`indicators.py:120-129`).
- **Ketten.** Index: 2 Risiken. €: Bodenschaden.
- **Review.** 🟠 viele multiplikative Proxys (depression T-1, dry R-1); schwer validierbar.
- **Verbesserung.** Nur wo relevant (Küste/Marschen); sonst niedrig halten.

---

### Gruppe E — Küste & Meer (überwiegend konstant)

#### `SEA_LEVEL_RISE` — Meeresspiegelanstieg [mm/Jahr, norm 0..10]
- **Was.** Anstiegsrate an der Küste (schleichender Einfluss).
- **Wie.** `regional.sea_level_rise` (Konstante 4,5) wenn Küste, sonst 0 (`indicators.py:95`).
- **Ketten.** Index: 3 Risiken. €: Migrations-/Küstenkosten.
- **Review.** 🟡 ein nationaler Wert (Phase 1 SEA_LEVEL_RISE).
- **Verbesserung.** BSH-Regionalpegel.

#### `OCEAN_WARMING` — Meereserwärmung [°C, norm 0..3]
- **Was.** Erwärmung der Küstengewässer.
- **Wie.** **Konstante 1,2** wenn Küste, sonst 0 (`indicators.py:96`).
- **Ketten.** Index: 1 Risiko. €: —.
- **Review.** 🟠 konstant.
- **Verbesserung.** Copernicus Marine SST (offen) für Nord-/Ostsee.

#### `OCEAN_ACIDIFICATION` — Ozeanversauerung [ΔpH] — **tot (H-A)**
- **Wie.** **Konstante 0,1** wenn Küste (`indicators.py:97`). **Ketten: keine.**
- **Review.** 🟠 (H-A) tot. **Verbesserung.** Entfernen oder in ein Meeresökologie-Risiko
  verdrahten.

#### `SALTWATER_INTRUSION` — Salzwasserintrusion [Index] — **tot (H-A)**
- **Wie.** **Konstante 0,3** wenn Küste (`indicators.py:118`). **Ketten: keine.**
- **Review.** 🟠 (H-A) tot (analog zur ebenfalls toten V `SALTWATER_INTRUSION_RISK`).
- **Verbesserung.** Entfernen oder als Küsten-Grundwasserrisiko verdrahten.

#### `COASTAL_EROSION` — Küstenerosion [m/Jahr] — **tot (H-A)**
- **Wie.** **Konstante 1,0** wenn Küste (`indicators.py:119`). **Ketten: keine.**
- **Review.** 🟠 (H-A) tot. **Verbesserung.** Entfernen oder in Küstenrisiko verdrahten.

---

### Gruppe F — Kryosphäre (tot/marginal)

#### `GLACIER_SNOW_LOSS` — Gletscher-/Schneeverlust [%/Jahr] — **tot (H-A)**
- **Was.** Rückgang von Gletschern/Schneedecke (nur alpine Lagen relevant).
- **Wie.** `glacier_loss_rate·glacier_frac + snow_decline·(0,25+0,75·snow_elev)·min(1;
  snow_days/45)` (`indicators.py:98-104`) — wird berechnet.
- **Ketten.** **keine** (0 Risiken).
- **Review.** 🟠 (H-A) **berechneter, aber toter** Hazard.
- **Verbesserung.** In ein alpines Wasserhaushalts-/Tourismusrisiko verdrahten oder (für die
  meisten Kommunen irrelevant) entfernen.

#### `PERMAFROST_THAW` — Permafrostauftauen [Index] — **tot (H-A)**
- **Wie.** **Konstante 0,0** (`indicators.py:105`) — immer null.
- **Ketten.** **keine**.
- **Review.** 🟠 (H-A) tot und null. **Verbesserung.** Entfernen (für DE irrelevant).

---

### Gruppe G — Verbund & Kaskade

#### `COMPOUND_EVENT` — Compound-Ereignis [Index 0..1]
- **Was.** Gleichzeitiges Zusammentreffen mehrerer Reize (Hitze+Dürre+Starkregen).
- **Wie.** `max(norm(HEAT_WAVE); norm(DROUGHT); norm(HEAVY_RAIN_FLOOD))` (`indicators.py:137-142`).
- **Ketten.** Index: 9 Risiken. €: Compound-Risiken.
- **Review.** ✅ methodisch sauber (Maximum normierter Bestandteile). 🟡 nutzt
  `override_context.normalize_value` — konsistent mit der Pipeline (der frühere Divergenz-
  Befund B6.2 der Provenance-Review ist hier nicht mehr zutreffend, da einheitlich).
- **Verbesserung.** Optional echte Ko-Inzidenz (Tage mit gleichzeitig Hitze+Trockenheit).

#### `CASCADE_EVENT` — Kaskaden-Ereignis [Index 0..1]
- **Was.** Domino-/Folgeereignisse (Ausfall löst Ausfall aus).
- **Wie.** **Konstante 0,3** (`indicators.py:134`).
- **Ketten.** Index: **11** Risiken. €: —.
- **Review.** 🟠 (H-B) konstant in 11 Risiken → fixer Ĥ=0,3-Beitrag ohne Ortsauflösung.
- **Verbesserung.** Aus der lokalen Infrastruktur-Kopplung (`INFRA_CRITICALITY`/-Dichte)
  ableiten statt Konstante.

---

### Sammelbefunde Einflüsse (Kurzliste)

- **H-A 🟠** — 6 tote H (`OCEAN_ACIDIFICATION`, `GLACIER_SNOW_LOSS`, `PERMAFROST_THAW`,
  `TROPICAL_CYCLONE`, `SALTWATER_INTRUSION`, `COASTAL_EROSION`); `GLACIER_SNOW_LOSS`
  berechnet, `PERMAFROST_THAW` konstant 0. Entfernen oder verdrahten.
- **H-B 🟠** — `CASCADE_EVENT`=0,3 konstant in 11 Risiken; aus Infrastruktur-Kopplung ableiten.
- **H-C 🟠** — T-1 erreicht `HEAVY_RAIN_FLOOD` (26×) und `LANDSLIDE`: absolute Terrain-Grenzen
  setzen.
- **H-D 🟠** — R-1 erreicht `DROUGHT` (26×), `SOIL_MOISTURE_DECLINE`, `WILDFIRE`,
  `SURFACE_WATER_HEATING`, `MEAN_TEMPERATURE_RISE`: UFZ-SMI + DWD-Rasterjahresmittel = größter
  Hebel.
- **UHI 🟠** — heuristisches Additivmodell, erbt `avg_height`/`canopy`-Lücken; kalibrieren.
- **Positiv ✅** — `HEAT_WAVE`, `COLD_EXTREME`, `LOW_FLOW_NIEDRIGWASSER`, `HEAVY_RAIN_FLOOD`
  (Regenteil), `COMPOUND_EVENT` beruhen auf echten DWD/PEGELONLINE-Daten bzw. sauberer Logik.
- **🐞 kein neuer Bug** in der H-Rechnung.

---

## Schicht „Risiken" (R) — 47 Layer, beide Ketten

Hier laufen H, E, V zusammen. Jedes Risiko liefert **zwei** Ergebnisse je Zelle: einen
**KWRA-Index** (Screening) und einen **Outcome/€-Wert** (Schadensbilanz). 47 Risiken (das
frühere Gesamtschaden-EAD wurde als Doppelzählung entfernt), davon 22 mit echter
Schadensfunktion, 11 reine Index-Risiken (0 €), 9 operative Ausfallrisiken.

### Kette 1 — Index (für **alle** 47 gleich)
`cell_risk_indices` (`risk_engine.py:55-77`): `Index = 100 · max_p( w_p · Ĥ_p · Ê_p · V̂_p )`
über die **kuratierten** Wirkungspfade des Risikos (`pathway_curation`), Gewichte degressiv
(`primary`=1,0 … `compound_multi`=0,5). **Nur der stärkste Pfad** bestimmt den Wert (Maximum,
nicht Summe → pfadanzahl-invariant). Aggregation je Kommune: **P90** der Zell-Indizes bzw.
**Belastungs-P90** über die expositionsrelevanten Zellen; Klassifikation gering/mittel/hoch
aus `tunables.risk_class_bounds`.

### Kette 2 — Outcome/€ (fünf Rechenfamilien)
Je Zelle `{outcome, cost_eur}`, Kommune-Aggregat = **Σ über Zellen** (pop/area) bzw.
**P90** (flat); `total_eur = Σ cost_eur` ohne `NON_ADDITIVE`-Codes. Monetarisierung
`cost_from_outcome`: monetär 1:1, sonst `outcome · cost_per_outcome`.
1. **Gesundheit (7, pop):** `pop · Rate · Treiber · g(V̂)`; Treiber = nichtlineare
   `AF(Hitzetage)` (hitzegetrieben) oder `haz_intensity` (ereignisgetrieben). × `cost_per_
   outcome` (z. B. VSL 3,5 Mio €).
2. **Monetäre Sektorschäden (10, DIRECT):** `Assetwert · Jahresverlustrate ·
   Schadenskurve(haz_intensity)^1,5 · g(V̂)`; € = Outcome.
3. **Monetär indirekt/konsolidiert (6):** über `consolidate_indirect` —
   `INDIRECT = k·Σdirekt` (k=0,25); `RESTORATION = 0,15·Σdirekt` (**nicht-additiv**);
   `SUPPLY_SHORTAGE/LOCATION/DELAYED = 0` (in k enthalten); `MIGRATION` = pop-Funktion.
4. **Umwelt (4, area):** `exponierte Naturfläche · Verlustrate(Hazard) · g(V̂)` × Kostensatz.
5. **Operativ (9, flat) + Index-only (11):** Legacy `outcome = ref_value · Index/100`;
   operativ × `cost_per_outcome` (VoLL) und **pop-skaliert** (`pop/100 000`, da VoLL je
   ~100 000-Ew.-Kommune kalibriert); Index-only tragen **0 €** (Doppelzählungsschutz).

`g(V̂) = 0,5 + Mittel(V̂ der Risiko-V-Liste) ∈ [0,5;1,5]`. **Wichtig:** die €-Kette nutzt
`haz_intensity` mit **fixen** Katalog-Grenzen ⇒ Screening-Norm-Overrides verschieben den
Index, **nicht** die €. Plausibilisierung über `impact/sanity.py` (Faktor >5 gg. `ref·pop/
Ref-pop` wird geloggt).

### Übergreifende Befunde Risiken
- **R-A 🟠 — Vererbte H/E/V-Schwächen dominieren.** Da `HEAVY_RAIN_FLOOD` und `DROUGHT` in je
  26 Risiken stecken, tragen **T-1** (kommunerelative Terrain-Normierung) und **R-1**
  (`hot_days`/`mean_temp`-Proxys) in fast jeden Risiko-Index. Der größte Hebel für die
  Risikoqualität liegt also in H/E/V, nicht in der Risiko-Komposition.
- **R-B 🟡 — Nur der stärkste Pfad zählt.** Das `max_p` macht sekundäre/kuratierte Pfade für
  den **Wert** irrelevant (sie erscheinen nur im Wirkungsdiagramm). Bewusst gewählt
  (pfadanzahl-invariant), aber die Pfadkuratierung wirkt weniger als sie suggeriert.
- **R-C 🟠 — Legacy-/Flat-Risiken hängen am `ref_value` × Index.** Operative (9) und
  Index-only (11) sowie einige monetäre Legacy-Risiken skalieren linear mit dem Index und
  einem gesetzten `ref_value`; deren Kalibrierung ist teils überzeichnet (MODELL_KRITIK §8/D2:
  Sanity-Faktoren Gebäude ~25×, indirekt ~35× — bewusst nur sichtbar gemacht, nicht kalibriert).
- **R-D 🟡 — Konstante V verwässern `g(V̂)`.** Die 7 konstanten V (V-A) ziehen `g(V̂)` gegen
  1,0 (in € neutral) und dämpfen den Index — informationslos, aber breit wirksam.
- **Positiv ✅ (R-E) — Saubere €-Architektur.** Schicht-B-Entkopplung (fixe `haz_intensity`),
  Doppelzählungsschutz (k-Konsolidierung, nicht-additive Restaurierung, Index-only=0 €, EAD
  entfernt) und die Live-Monetarisierung aus Per-Zell-Outcomes sind methodisch stark.

---

### Familie 1 — Gesundheit (7 Risiken, `scale=pop`, echte Funktion)
Muster: `Outcome = pop · (Rate/100 000) · Treiber · g(V̂)`, € = `Outcome · cost_per_outcome`.

#### `EXPECTED_ANNUAL_MORTALITY` — Hitzemortalität [Tote/Jahr]
- **Was.** Erwartete hitzebedingte Zusatzsterbefälle. Leitrisiko der Hitzekette.
- **Wie.** `pop·(1130/100k)·AF·g(V̂)`, `AF = 1 − exp(−0,0008·(Hitzetage − 8)₊)`
  (`health.py:34-40`); € = Outcome·**3,5 Mio € (VSL)**.
- **Review.** ✅ nichtlineare AF ist state-of-the-art (RKI/Winklmayr). 🟡 **V-E-Doppelzählung**:
  `VULNERABLE_GROUPS_SHARE` **und** `HEAT_SENSITIVITY` (enthält `share_vuln`) in g(V̂).
- **Verbesserung.** Demografie-Doppelzählung auflösen; AF-β je Altersgruppe.

#### `EXPECTED_ANNUAL_MORBIDITY` — Hitzemorbidität [Fälle/Jahr]
- **Was.** Hitzebedingte Erkrankungen/Klinikfälle.
- **Wie.** `pop·(8000/100k)·AF·g`, `AF`-β=0,0016 (`health.py:46-51`); € = ·5 000 €.
- **Review.** ✅ analog Mortalität; g(V̂) nutzt u. a. `DISEASE_VECTOR_SUSCEPTIBILITY` (R-1-Erbe).
- **Verbesserung.** wie Mortalität.

#### `EXPECTED_ANNUAL_INJURIES` — Verletzte [Verletzte/Jahr]
- **Was.** Verletzte durch Flut/Sturm/Hangrutsch.
- **Wie.** `pop·(150/100k)·driver·g`, `driver = max(haz_intensity(HEAVY_RAIN_FLOOD,
  EXTRATROPICAL_STORM, LANDSLIDE))` (`health.py:56-64`); € = ·12 000 €.
- **Review.** 🟠 ereignisgetrieben über T-1-behaftete Hazards (`HEAVY_RAIN_FLOOD`/`LANDSLIDE`);
  g(V̂) nutzt `EARLY_WARNING`/`EMERGENCY` (nach Bugfix echte OSM-Nähe).
- **Verbesserung.** T-1-Fix in den Hazards.

#### `EXPECTED_ANNUAL_MENTAL_HEALTH` — Psychische Gesundheit [Fälle/Jahr]
- **Was.** Psychische Belastungsfälle nach Hitze/Extremereignissen.
- **Wie.** `pop·(1500/100k)·min(1; AF + 0,3·event)·g`, `event = max(haz_intensity(COMPOUND,
  CASCADE, DROUGHT))` (`health.py:70-79`); € = ·4 000 €.
- **Review.** 🟠 nutzt `CASCADE_EVENT` (Konstante 0,3, H-B) und `DROUGHT` (R-1) als Ereignisteil.
- **Verbesserung.** `CASCADE`-Konstante ersetzen (H-B-Fix).

#### `EXPECTED_ANNUAL_AFFECTED_EVACUATED` — Betroffene/Evakuierte [Pers./Jahr]
- **Was.** Von Flut/Sturmflut/Feuer betroffene bzw. evakuierte Personen.
- **Wie.** `pop·(2500/100k)·max(haz_intensity(HEAVY_RAIN_FLOOD, STORM_SURGE, WILDFIRE))·g`
  (`health.py:85-92`); € = ·2 500 €.
- **Review.** 🟠 `STORM_SURGE` konstant, `HEAVY_RAIN_FLOOD` T-1.
- **Verbesserung.** wie oben.

#### `EXPECTED_THERMAL_STRESS_HOURS` — Wärmebelastungsstunden [h/Jahr]
- **Was.** Personenstunden unter Hitzestress.
- **Wie.** `(pop/100k)·400·(Hitzetage/20)·g` (`health.py:98-105`); € = ·400 €.
- **Review.** 🟡 linearer `driver = hd/20` **unclamped** (bei 40 Hitzetagen ×2); g(V̂) nutzt
  `UHI_INTENSITY`/`GREEN_SPACE_SHARE`.
- **Verbesserung.** Sättigung des Treibers erwägen.

#### `EXPECTED_POLLUTANT_EXPOSURE_HOURS` — Schadstoff-Belastungsstunden [h/Jahr]
- **Was.** Personenstunden unter erhöhter (hitzegekoppelter) Luftschadstoffbelastung.
- **Wie.** `(pop/100k)·250·(Hitzetage/20)·g` (`health.py:111-118`); € = ·300 €.
- **Review.** 🟠 Ozon/Feinstaub nur über Hitzetage proxyiert (kein echter Schadstoff);
  g(V̂) nutzt `AIR_QUALITY_RISK` (road_cov-Proxy).
- **Verbesserung.** UBA/CAMS-Luftdaten (kostenlos) einkoppeln.

---

### Familie 2 — Monetäre Sektorschäden (10, DIRECT)
Muster: `€ = Assetwert · Jahresverlustrate · haz_intensity^1,5 · g(V̂)` (`impact/monetary.py`).

#### `EXPECTED_BUILDING_DAMAGE_EUR` — Gebäudeschäden [€/Jahr]
- **Was.** Jahresschaden an Gebäuden durch Flut/Sturm/Hitze.
- **Wie.** Asset `bldg_cov·10 000 m²·Geschosse·2 000 €/m²` × Verlustrate 0,008 ×
  Kurve(max(HEAVY_RAIN_FLOOD, STORM, HEAT)) × g(V̂).
- **Review.** 🟠 Sanity-Flag ~25× (D2) deutet auf **Überkalibrierung** (Asset×Rate zu hoch);
  T-1 über den Flut-Treiber.
- **Verbesserung.** Verlustrate/Assetwert an GDV-Schadensquoten nachkalibrieren.

#### `EXPECTED_TRANSPORT_DAMAGE_EUR` — Verkehrsschäden [€/Jahr]
- **Was.** Schäden an Verkehrsinfrastruktur.
- **Wie.** `transport_hub_count·500 000 €·0,02·Kurve(HEAVY_RAIN_FLOOD, HEAT, DROUGHT)·g`.
- **Review.** ✅ echte Knotenzählung; 🟡 Punkt-Assets erfassen keine Linien (Gleise/Brücken).
- **Verbesserung.** Linien-Assets ergänzen (Phase 3 `TRANSPORT_HUBS`).

#### `EXPECTED_ENERGY_INFRA_DAMAGE_EUR` — Energieinfrastrukturschäden [€/Jahr]
- **Wie.** `energy_infra_count·800 000 €·0,02·Kurve(STORM, FLOOD, HEAT)·g`.
- **Review.** ✅ echte Assets. 🟡 keine Typgewichtung (Kraftwerk = Trafo).
- **Verbesserung.** Anlagentyp gewichten.

#### `EXPECTED_TELECOM_DAMAGE_EUR` — Telekom-Schäden [€/Jahr]
- **Wie.** `communication_count·400 000 €·0,02·Kurve(STORM, FLOOD)·g`.
- **Review.** ✅. **Verbesserung.** —

#### `EXPECTED_WATER_WASTEWATER_DAMAGE_EUR` — Wasser/Abwasser-Schäden [€/Jahr]
- **Wie.** `water_wastewater_count·600 000 €·0,015·Kurve(FLOOD, DROUGHT, HEAT)·g`.
- **Review.** ✅. **Verbesserung.** —

#### `EXPECTED_AGRICULTURAL_DAMAGE_EUR` — Agrarschäden [€/Jahr, `scale=area`]
- **Wie.** `farmland_frac·1 ha·12 000 €·0,15·Kurve(DROUGHT, HEAT, FLOOD)·g`.
- **Review.** 🟠 `DROUGHT`-Treiber R-1-kollinear; Coverage-Asymmetrie über `farmland`.
- **Verbesserung.** UFZ-SMI + Kulturarten.

#### `EXPECTED_SOIL_LOSS_DEGRADATION_EUR` — Bodenverlust [€/Jahr, area]
- **Wie.** `farmland_frac·1 ha·30 000 €·0,01·Kurve(DROUGHT, FLOOD, SOIL_SALINIZATION)·g`.
- **Review.** 🟠 gegen ökologischen Bodenwert abgegrenzt (kein Doppelzähler, §8/B5); Treiber R-1.
- **Verbesserung.** BÜK-Erodierbarkeit.

#### `EXPECTED_ECOSYSTEM_SERVICE_LOSS` — Verlust Ökosystemleistungen [€/Jahr, area]
- **Wie.** `(forest+green)·1 ha·3 000 €/ha·a·0,08·Kurve(DROUGHT, FLOOD, SEA_LEVEL_RISE)·g`.
- **Review.** 🟡 TEEB-basiert; gegen physische Habitat-/Biodiversitätsverluste abgegrenzt.
- **Verbesserung.** —

#### `EXPECTED_FISHERIES_ECONOMIC_LOSS_EUR` — Fischerei-Verlust [€/Jahr, area]
- **Wie.** `water_frac·1 ha·5 000 €·0,20·Kurve(SURFACE_WATER_HEATING, LOW_FLOW, DROUGHT, HEAT)·g`.
- **Review.** 🟠 `water_frac` proximity-verunreinigt; `SURFACE_WATER_HEATING` R-1.
- **Verbesserung.** reine Wasserfläche + LST.

#### `EXPECTED_AQUACULTURE_DAMAGE_EUR` — Aquakulturschäden [€/Jahr, area]
- **Wie.** `water_frac·1 ha·5 000 €·0,25·Kurve(SURFACE_WATER_HEATING, LOW_FLOW, FLOOD)·g`.
- **Review.** 🟠 g(V̂) nutzt die **konstante** `AQUACULTURE_TECHNICAL_VULNERABILITY` (V-A).
- **Verbesserung.** Aquakultur-Standorte aus OSM.

---

### Familie 3 — Monetär indirekt/konsolidiert (6)
Werden von `consolidate_indirect` (`monetary.py:242-254`) gesetzt, **nicht** vom nominellen
Legacy-Weg — Doppelzählungsschutz.

#### `EXPECTED_INDIRECT_ECONOMIC_LOSS_EUR` — Indirekte Wirtschaftsverluste [€/Jahr]
- **Wie.** `k · Σ direkte Sektorschäden`, k = 0,25 (Prognos-I/O-Band 0,18–0,5).
- **Review.** ✅ saubere Konsolidierung (ersetzt frühere Doppelzählung).
- **Verbesserung.** k regional differenzieren (Wirtschaftsstruktur).

#### `EXPECTED_RESTORATION_COSTS_EUR` — Wiederherstellungskosten [€/Jahr] — **nicht-additiv**
- **Wie.** `0,15 · Σ direkte Sektorschäden`; ausgewiesen, aber **nicht** in `total_eur`.
- **Review.** ✅ korrekt als Teilmenge behandelt (kein Doppelzähler).
- **Verbesserung.** —

#### `EXPECTED_SUPPLY_SHORTAGE_COSTS_EUR` · `EXPECTED_LOCATION_DISADVANTAGE_EUR` · `EXPECTED_DELAYED_DAMAGE_COSTS_EUR` — **je 0 € (CONSOL)**
- **Wie.** Auf **0** gesetzt (in `k_indirekt` enthalten); tragen weiter zum **Index** bei.
- **Review.** ✅ Doppelzählungsschutz. 🟡 Als eigene Layer mit 0 € potenziell verwirrend.
- **Verbesserung.** In der UI als „in indirekten Verlusten enthalten" kennzeichnen.

#### `EXPECTED_CLIMATE_MIGRATION_COSTS_EUR` — Klimamigrationskosten [€/Jahr]
- **Wie.** `(pop/100 000)·400 000 €·max(haz_intensity(SEA_LEVEL_RISE, FLOOD, DROUGHT))·g`
  (eigenständige Impact-Funktion, nicht in k enthalten).
- **Review.** 🟡 pop-getrieben, plausibel; `SEA_LEVEL_RISE` konstant.
- **Verbesserung.** —

---

### Familie 4 — Umwelt (4, `scale=area`, echte Funktion)
Muster: `Outcome = exponierte Naturfläche · Verlustrate(Hazard) · g(V̂)`, × Kostensatz.

#### `EXPECTED_BIODIVERSITY_LOSS` — Biodiversitätsverlust [Arten/Jahr]
- **Wie.** Naturfläche × Verlustrate(WILDFIRE/DROUGHT/…) × g(V̂); € = ·500 000 €/Art.
- **Review.** 🟠 g(V̂) nutzt `BIODIVERSITY_RESILIENCE`+`WILDFIRE_SUSCEPTIBILITY` (R-1);
  „Arten/Jahr" ist eine grobe Kennzahl.
- **Verbesserung.** Schutzgebiets-/Rote-Liste-Bezug.

#### `EXPECTED_HABITAT_LOSS` — Habitatverlust [ha/Jahr]
- **Wie.** exponierte Habitatfläche × Verlustrate × g(V̂); € = ·80 000 €/ha.
- **Review.** 🟡 nutzt `EROSION_SUSCEPTIBILITY` (T-1-Erbe).
- **Verbesserung.** absolute Hang-/Bodendaten.

#### `EXPECTED_SOIL_DEGRADATION` — Bodendegradation [ha/Jahr]
- **Wie.** Ack/Bodenfläche × Verlustrate(DROUGHT/…) × g(V̂); € = ·10 000 €/ha.
- **Review.** 🟠 R-1-Treiber. **Verbesserung.** UFZ-SMI.

#### `EXPECTED_VEGETATION_DAMAGE` — Vegetationsschäden [ha/Jahr]
- **Wie.** Vegetationsfläche × Verlustrate(DROUGHT/WILDFIRE) × g(V̂); € = ·20 000 €/ha.
- **Review.** 🟠 R-1-Treiber. **Verbesserung.** UFZ-SMI + `leaf_type`.

---

### Familie 5 — Operative Ausfallrisiken (9, `scale=flat`, Legacy + VoLL)
Muster: `outcome = ref_value · Index/100` [Stunden]; `€ = outcome · VoLL · (pop/100 000)`;
Aggregat **P90** (nicht zell-additiv). Alle erben die H/E/V-Schwächen über den Index (R-A/R-C).

#### `EXPECTED_CI_OUTAGE_HOURS` — Ausfall kritischer Infrastruktur [h/Jahr]
- **Wie.** `120·Index/100` h × 40 000 €/h × pop-Skalierung. g(V̂): `INFRA_CRITICALITY`,
  `REDUNDANCY_BACKUP`(konst), `INFRA_DEPENDENCY_CHAIN`(konst).
- **Review.** 🟠 zwei der drei V konstant (V-A) → Index kaum V-differenziert.
- **Verbesserung.** V-A-Fixe.

#### `EXPECTED_ENERGY_OUTAGE_HOURS` [h/Jahr]
- **Wie.** `40·Index/100` × 120 000 €/h × pop. **Review.** 🟠 `REDUNDANCY_BACKUP` konst.
- **Verbesserung.** —

#### `EXPECTED_WATER_SUPPLY_OUTAGE_HOURS` [h/Jahr]
- **Wie.** `30·Index/100` × 60 000 €/h × pop; V: `WATER_STRESS_INDEX`,
  `GROUNDWATER_DEPENDENCY`, `INFRA_DEPENDENCY_CHAIN`(konst).
- **Review.** 🟠 R-1 über `WATER_STRESS_INDEX`. **Verbesserung.** UFZ-SMI.

#### `EXPECTED_WASTEWATER_OUTAGE_HOURS` [h/Jahr]
- **Wie.** `25·Index/100` × 25 000 €/h × pop; V: `SEALING_DEGREE`, `CRITICAL_INFRA_CONDITION`(konst).
- **Review.** 🟡 **Verbesserung.** —

#### `EXPECTED_COMMUNICATION_OUTAGE_HOURS` [h/Jahr]
- **Wie.** `20·Index/100` × 50 000 €/h × pop. **Review.** 🟠 `REDUNDANCY_BACKUP` konst.

#### `EXPECTED_TRANSPORT_DISRUPTION_HOURS` [h/Jahr]
- **Wie.** `60·Index/100` × 30 000 €/h × pop; H: Hitze/Flut; V: `MATERIAL_HEAT_SENSITIVITY`.
- **Review.** ✅ echte V. **Verbesserung.** —

#### `EXPECTED_SUPPLY_CHAIN_DISRUPTION_HOURS` [h/Jahr]
- **Wie.** `50·Index/100` × 40 000 €/h × pop; V: `SUPPLY_CHAIN_DEPENDENCY`(konst),
  `SINGLE_SITE_DEPENDENCY`.
- **Review.** 🟠 eine V konst, andere Residuum-Proxy (P1-3).

#### `EXPECTED_ADMIN_OUTAGE_HOURS` [h/Jahr]
- **Wie.** `15·Index/100` × 15 000 €/h × pop; V: `EMERGENCY_MANAGEMENT`,
  `PLANNING_IMPLEMENTATION_CAPACITY`.
- **Review.** ✅ echte INKAR/OSM-V. **Verbesserung.** —

#### `EXPECTED_FUNCTIONAL_FAILURE_DURATION` — Funktionsausfalldauer [h/Jahr]
- **Wie.** `35·Index/100` × 30 000 €/h × pop; V: `INFRA_CRITICALITY`, `INFRA_DEPENDENCY_CHAIN`(konst).
- **Review.** 🟠 `CASCADE_EVENT`(konst, H-B) als Hazard.

---

### Familie 6 — Reine Index-Risiken (11, `scale=flat`, 0 €)
`outcome = Index` (ref=100), **cost = 0** (Doppelzählungsschutz — Schaden ist über die
monetären Risiken erfasst). Sie sind reine **Screening-/Systemkennzahlen**; ihr ganzer Wert
= der Index und erbt damit dessen H/E/V-Schwächen (R-A). Kurzcharakteristik:

- `MEDICAL_UNDERSUPPLY_RISK_INDEX` — Med. Unterversorgung (V: `HEALTHCARE_ACCESS`✅,
  `INFRA_DEPENDENCY_CHAIN`konst). 🟡
- `HYDROLOGICAL_STRESS_RISK_INDEX` — Hydrolog. Stress (H: DROUGHT/LOW_FLOW; V: `WATER_STRESS`).
  🟠 R-1.
- `EXPECTED_WATER_AIR_POLLUTION` — Wasser-/Luftverschmutzung (V: `WATER_STRESS`,
  `AIR_QUALITY_RISK`). 🟠 Proxys.
- `ECOSYSTEM_DEGRADATION_RISK_INDEX` · `ECOSYSTEM_FRAGMENTATION_RISK_INDEX` —
  Ökosystem-Degradation/-Fragmentierung (V: `BIODIVERSITY_RESILIENCE`, `GREEN_SPACE_SHARE`). 🟡
- `SYSTEMIC_DOMINO_RISK_INDEX` — Domino/Systemik (V: `REDUNDANCY_BACKUP`konst,
  `INFRA_DEPENDENCY_CHAIN`konst; H: `CASCADE`konst). 🟠 fast nur Konstanten.
- `RESOURCE_CONFLICT_RISK_INDEX` — Ressourcenkonflikt (V: `INCOME_SOCIAL_RESILIENCE`,
  `WATER_STRESS`). 🟡
- `SOCIAL_INEQUALITY_AMPLIFICATION_RISK_INDEX` — Soziale Ungleichheit (V:
  `VULNERABLE_GROUPS_SHARE`, `INCOME_SOCIAL_RESILIENCE`). ✅ echte V.
- `ENVIRONMENTAL_FEEDBACK_RISK_INDEX` — Umwelt-Rückkopplung (V: `BIODIVERSITY_RESILIENCE`,
  `WILDFIRE_SUSCEPTIBILITY`). 🟠 R-1.
- `FISHERIES_STOCK_STRESS_RISK_INDEX` · `LOW_WATER_FISHERIES_IMPACT_INDEX` — Fischbestand/
  Niedrigwasser-Fischerei (V: `FISHERIES_TEMPERATURE_SENSITIVITY`, `GROUNDWATER_DEPENDENCY`). 🟠 R-1.

**Review Familie 6:** ✅ das 0-€-Prinzip verhindert Doppelzählung sauber. 🟠 `SYSTEMIC_DOMINO`
ist fast vollständig aus Konstanten gebaut (`CASCADE`+2 konstante V) → kaum differenzierend.
**Verbesserung:** V-A/H-B-Fixe schlagen hier am stärksten durch.

---

### Sammelbefunde Risiken (Kurzliste)
- **R-A 🟠** — Risiko-Qualität steht/fällt mit H/E/V: T-1 (`HEAVY_RAIN_FLOOD`) und R-1
  (`DROUGHT`) sind in je 26 Risiken. Größter Hebel: UFZ-SMI + absolute Terrain-Normen.
- **R-B 🟡** — `max_p` macht sekundäre Pfade wertirrelevant.
- **R-C 🟠** — Legacy/Flat + Index-only skalieren mit `ref_value×Index`; Sanity-Flags
  (Gebäude ~25×, indirekt ~35×) signalisieren Überkalibrierung — nachkalibrieren.
- **R-D 🟡** — konstante V (V-A) verwässern `g(V̂)` und dämpfen Index in vielen Risiken.
- **Positiv ✅ (R-E)** — Schicht-B-Entkopplung, k-Konsolidierung, nicht-additive Restaurierung,
  Index-only=0 €, Live-Monetarisierung: methodisch stark und doppelzählungsfrei.
- **🐞 kein neuer Bug** in der Risiko-Komposition; die zwei Bugfixes dieser Sitzung
  (`WATER_PROXIMITY`, Infrastruktur-Distanzen) wirken über H/E/V in die Risiken hinein.

---

## Gesamtfazit & Priorisierung (Umsetzungs-Roadmap)

**Grundurteil:** Das H·E·V·R-Gerüst und die Schicht-B-€-Architektur sind **methodisch
tragfähig** und in der €-Kette (Entkopplung, Doppelzählungsschutz) sogar stark. Die
Schwächen sitzen fast alle in den **Eingaben** (Proxys, relative Normierung, tote/konstante
Indikatoren), nicht in der Komposition. Der Hebel für Qualität liegt daher unten in der
Kette (Sonstige/H/E/V), nicht in den Risiken.

**Sofort erledigt (diese Sitzung):**
- 🐞 5 Bugs gefixt & verifiziert (siehe Changelog oben): Gewässer- + Infrastruktur-Distanz
  (Grad→Meter), Zensus `–`→0, dynamisches Jahr in `BUILDING_STABILITY`, veraltete
  Provenance-Texte.
- 🧹 Toten Assessor-Parallelpfad entfernt (189/189 Tests grün).

**Priorisierte Verbesserungen (alle mit kostenlosen Quellen):**

| Prio | Maßnahme | Wirkt auf | Aufwand |
|---|---|---|---|
| **1** | **R-1 auflösen:** UFZ-Dürremonitor-SMI + DWD-CDC-Jahresmittelraster am Zentroid statt `hot_days`/Bundesland-`mean_temp`-Proxys | `DROUGHT` (26 Risiken), `WATER_STRESS`, `WILDFIRE`, `SOIL_MOISTURE`, `SURFACE_WATER_HEATING`, `TEMPERATURE_RISE` | mittel |
| **2** | **T-1 auflösen:** Terrain-Normierungen (`twi_norm`, `depression_factor`, `slope_factor`) auf **absolute** physikalische Grenzen statt kommunerelativ min–max | `HEAVY_RAIN_FLOOD` (26), `LANDSLIDE`, `SOIL_/EROSION_SUSCEPTIBILITY`, `FLOODPLAINS` | klein |
| **3** | **Toten Code bereinigen/verdrahten:** 6 tote H, 2 tote V, 2 tote E; `LEVEE_CONDITION` + Deich-Fetch verdrahten oder entfernen; `CONSOL`-0-€-Layer in UI kennzeichnen | Klarheit, Wartbarkeit | klein |
| **4** | **Konstanten datengetrieben machen:** 7 konstante V (`CRITICAL_INFRA_CONDITION` in 8 Risiken!) + `CASCADE_EVENT`=0,3 (11 Risiken) aus Zensus-Baualter/KRITIS-Dichte/INKAR ableiten oder ehrlich als Modellannahme labeln | breit (Index-Differenzierung) | mittel |
| **5** | **€-Kalibrierung:** Sektor-Verlustraten/Assetwerte gegen GDV-Schadensquoten nachziehen (Sanity-Flags Gebäude ~25×, indirekt ~35×) | monetäre Schäden, `total_eur` | mittel |
| **6** | **Coverage-Asymmetrie (O-1):** Grün/Wald/Wasser/Acker auf abgedeckte Fläche normieren; `WATER_FRACTION`-Semantik entmischen; `INDUSTRIAL_FRACTION` aus OSM `landuse` (P1-3) | Vegetation/Dürre/Wald in ländl. Zellen | klein |
| **7** | **Kosmetik/Redundanz:** Doppelformeln/Redundanzen (V-C, Healthcare) aufräumen; `GREEN_SPACE_SHARE`→`_DEFICIT` umbenennen; `WATER_FRACTION`-Semantik entmischen | Nachvollziehbarkeit | klein |

**Nicht-Ziele (bewusst so lassen):** die Schicht-B-Entkopplung (fixe `haz_intensity`), die
k-Indirekt-Konsolidierung, nicht-additive Restaurierung und Index-only=0 € — methodisch
korrekt, nicht anfassen.

> **Status:** Reine Analyse (kein Code außer den zwei Bugfixes + Assessor-Cleanup geändert).
> Reihenfolge oben = empfohlene Implementierungsreihenfolge; jede Zeile ist unabhängig
> umsetzbar und einzeln testbar.
