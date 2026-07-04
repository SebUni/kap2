# Quellen-Anreicherung — Übergabe-Prompts (IEEE-Zitation + Wayback-Snapshot)

Ziel: Jeder belegte Parameterwert bekommt eine **zitierfähige** Herkunft, die im
(i)-Hover-Tooltip (Sidebar **und** Konfigurations-Tabelle) sichtbar ist:
IEEE-Zitation + klickbare **Live-URL** + archivierter **Wayback-Snapshot** (falls
die Quelle offline geht) + der bereits vorhandene Herleitungs-Langtext
(`source_details`).

## Was bereits steht (nicht neu bauen)

- **Infrastruktur fertig:** `backend/app/data/sources.py` (`SOURCE_REFERENCES` +
  `resolve()`), `references` fließt durch `measure_service.compute_costs`,
  `parameter_registry` (Maßnahmen-Block), `schemas.SourceReference`,
  Frontend-`InfoTooltip` (rendert „Original"/„Archiv-Snapshot"-Links, bleibt beim
  Hinüberfahren offen) und `ParameterTable`/`MeasureSidebar`.
- **Datenmodell je Katalog-Eintrag:** `sources[feld]` (Kurzlabel),
  `source_details[feld]` (Tooltip-Langtext, für **Kosten** schon vollständig),
  `source_refs[feld] = [bib_key, …]` (Verweis auf die Bibliografie).
- **3 Referenz-Beispiele fertig belegt+archiviert:** `GREEN_ROOFS_FACADES`
  (BuGG + co2online), `DRINKING_FOUNTAINS` (Berliner Wasserbetriebe),
  `DECENTRALIZED_ENERGY_PV_STORAGE` (HTW Stromspeicher-Inspektion). Diese sind die
  Vorlage — Struktur exakt übernehmen.

## Grundlagen (in JEDER Session mitschicken)

```
Kontext: Klimarisiko-Tool, Repo /opt/lampp/htdocs/kap2. Quellen-Bibliografie liegt in
backend/app/data/sources.py (SOURCE_REFERENCES: key -> {ieee, url, archive_url, accessed}),
resolve() hängt sie an CostComponents/Registry-Parameter (Feld "references"). Katalog-
Einträge verweisen per source_refs = {feld: [key, ...]}. Vorlage: die 3 fertigen Einträge
BuGG_Marktreport_2024, co2online_Dachbegruenung, BWB_Trinkbrunnen, HTW_Stromspeicher_2025.

Regeln:
- KEINE Werte/Zahlen ändern, KEINE Methodik anfassen — nur Quellen anreichern.
- NUR belastbare, real existierende Quellen. Reine "Modellannahme (…)"-Felder bleiben
  ohne source_refs (die ehrliche Prosa in source_details genügt) — nichts erfinden.
- IEEE-Zitation deutsch lokalisiert, Schema:
  Autor/Institution, „Titel,“ Ort, Jahr. [Online]. Verfügbar: <url>. [Zugriff: 4. Juli 2026].
  (Bei >3 Autoren: "A. Erstautor u. a.". Ohne Jahr: Jahr weglassen.)
- Jede neue Quelle ZWINGEND archivieren (Wayback), archive_url MUSS ein
  web.archive.org-Permalink sein:
    curl -s -I "https://web.archive.org/save/<url>" | grep -i '^location:'
  Falls leer (PDF/langsam/Ratelimit) den jüngsten vorhandenen Snapshot nehmen:
    curl -s "https://web.archive.org/cdx/search/cdx?url=<url>&output=json&limit=-1&filter=statuscode:200"
    -> https://web.archive.org/web/<timestamp>/<url>
- bib_key: sprechend + stabil (z. B. "DWA_A138_2005", "KTBL_Bewaesserung").
- Verifikation: cd backend && python -m pytest tests/test_measure_pricing.py -q
  (prüft u. a. source_refs -> Bibliografie und Vollständigkeit der Einträge). Danach committen.
```

Einen neuen Bibliografie-Eintrag anlegen (in `sources.py`) und verdrahten (in `catalog.py`):

```python
# sources.py
"DWA_A138_2005": {
    "ieee": "Deutsche Vereinigung für Wasserwirtschaft, Abwasser und Abfall e.V. (DWA), "
            "„Arbeitsblatt DWA-A 138: Planung, Bau und Betrieb von Anlagen zur Versickerung "
            "von Niederschlagswasser,“ Hennef, Deutschland, 2005. [Online]. Verfügbar: "
            "<url>. [Zugriff: 4. Juli 2026].",
    "url": "<live-url>",
    "archive_url": "https://web.archive.org/web/<ts>/<url>",
    "accessed": "2026-07-04",
},
# catalog.py, in der Maßnahme (neben sources/source_details):
"source_refs": {"capex_per_m2": ["DWA_A138_2005"], "opex_per_m2_year": ["DWA_A138_2005"]},
```

---

## Teil 1 — Restliche KOSTEN-Parameter (Infra fertig, nur Daten)

Noch zu belegen: **24 Maßnahmen** mit real belegten (nicht-Modellannahme) Kosten,
gebatcht nach KAnG-Cluster (Anker wie in `MASSNAHMEN_BEPREISUNG_PROMPTS.md §6`).
Je Batch: `source_refs` + Bibliografie-Einträge, für die in `source_details` bereits
genannten Quellen (die Prosa nennt Beleg + Vorgehen — nur URL finden + archivieren).

| Batch | Maßnahmen (Auszug) | Quellen-Anker |
|---|---|---|
| Gebäude/Begrünung | COOL_ROOFS, HEAT_RESILIENT_PAVEMENT, FLOOD_PROTECTION_BUILDING | BuGG (vorhanden), co2online (vorhanden), kostencheck, BBK-Hochwasserschutzfibel |
| Wasser/Starkregen | DESEALING_SURFACE, DRAINAGE_SWALES, INFILTRATION_AREAS, RETENTION_STORAGE, RETENTION_POLDER_RESERVOIR, LEAKAGE_REDUCTION | DWA-A 138, Sieker, Hamburg RISA, LANUV NRW, DVGW |
| Küste/Fluss | LEVEE_REINFORCEMENT, FLOODPLAIN_RENATURATION, EROSION_PROTECTION | NLWKN/MELUND, IKSR, BfN |
| Land-/Forst | MIXED_FORESTS, HUMUS_BUILDUP, DROUGHT_RESISTANT_VARIETIES, WATER_STORAGE_EFFICIENT_IRRIGATION | KTBL, LfL Bayern, Landesforsten |
| Energie/Wirtschaft | GRID_REINFORCEMENT_REDUNDANCY | BNetzA/dena, Verteilnetz-Praxiswerte |
| Bevölkerungsschutz/Fischerei | EARLY_WARNING_MEASURE (opex_fixed_year: kommunal.de/Hydrotec), FISH_PASSAGE_RESTORATION, FISHERIES_SPAWNING_HABITAT_RESTORATION | BBK, kommunal.de, LAWA |
| Stadt/Hitze (Rest) | HEAT_ACTION_PLANS, URBAN_GREEN | klimastadtraum.de, GALK, difu |

Session-Prompt je Batch: Grundlagen (oben) + „Batch <Name>: finde für die unten
gelisteten Maßnahmen die in `source_details` genannten Quellen als stabile URL,
archiviere sie (Wayback), lege je Quelle einen `SOURCE_REFERENCES`-Eintrag an und
verdrahte `source_refs` je belegtem Kostenfeld. `capex_fixed: 0.0`-Felder
(planungsrechtlich/kostenlos) brauchen keine Quelle."

---

## Teil 2 — NICHT-Kosten-Parameter (Hazards, Risiken, Expositionen, Sensitivitäten, Formeln)

Diese Parameter haben heute nur ein `source`-Kurzlabel (kein `source_detail`, keine
`references`). Zwei Schritte:

### 2a. Kleiner Infra-Ausbau in `parameter_registry.py` (einmalig)

`_base_param` kann `source_detail`/`references` bereits — sie werden für Nicht-
Maßnahmen nur noch nicht befüllt. In `catalog_parameters()` je Emissions-Block
ergänzen (analog zum Maßnahmen-Block):

- **RISKS** (`ref_value`, ~Z. 98): `source_detail=r.get("source_detail","")`,
  `references=sources.resolve(r.get("source_refs"))`.
- **HAZARDS/EXPOSURES/VULNERABILITIES** (`norm_min`/`norm_max`, ~Z. 116):
  `source_detail=m.get("source_detail","")`, `references=sources.resolve(m.get("source_refs"))`.
- **Formel-Parameter** (`formulas.DETAILED`-Inputs, ~Z. 146): `source_detail=inp.get("source_detail","")`,
  `references=sources.resolve(inp.get("source_refs"))`.
- **pathway_weights / UHI**: analog, falls belegbar (meist dokumentierte Modellwahl → nur `source_detail`).

Frontend braucht KEINE Änderung (ModelParameter.references/-source_detail + Tooltip
sind generisch). Test: bestehende `python -m pytest backend/tests/` bleibt grün.

### 2b. Daten je Cluster (Research + Wayback), gebatcht

Katalog-Einträge in `catalog.py` um `source_detail` (Langtext) + `source_refs`
ergänzen; Bibliografie-Einträge in `sources.py` anlegen + archivieren. Cluster:

- **Hazards** (Klimaprojektionen, Kennwerte): DWD, Copernicus/C3S, IPCC AR6, Umweltbundesamt.
- **Risiken** (`ref_value` Schadens-/Outcome-Kennwerte): KWRA 2021 (UBA), GDV-Schadenstatistik,
  RKI (Hitzemortalität), Destatis.
- **Expositionen/Sensitivitäten** (Normierungsskalen): Zensus 2022, CORINE/Copernicus Land,
  einschlägige Fachliteratur je Indikator.
- **Formel-Parameter** (UHI-Koeffizienten etc.): VDI 3787, Oke 1982, Stewart & Oke 2012
  (bereits als `source` vorhanden → nur `source_detail` + ggf. `source_refs` nachziehen).

Session-Prompt je Cluster: Grundlagen (oben) + 2a als Voraussetzung + „Cluster
<Name>: belege die aufgeführten Parameter mit source_detail + archivierter IEEE-
Quelle; unbelegbare bleiben ehrlich Modellannahme."

Akzeptanz gesamt: `python -m pytest backend/tests/` grün; im Browser zeigt der
(i)-Tooltip an einem angereicherten Nicht-Kosten-Parameter IEEE-Zitat + Original-
und Archiv-Link.
