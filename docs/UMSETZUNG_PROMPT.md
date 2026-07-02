# Umsetzung — 6 eigenständige Prompts

Jeder Prompt ist self-contained und einzeln in einer frischen Session submittbar (Token-schonend, ein Block pro Session). Reihenfolge = empfohlene Priorität; Prompts 1–2 sind billig & sofort wirksam, Prompt 5 der größte. Details je Block: siehe `docs/REVIEW_WIRKUNGSMECHANISMEN.md`.

**Gemeinsame Kontextzeile** (steckt in jedem Prompt als `[Kontextzeile]`):

> Kontext: Klimarisiko-Tool, Repo /opt/lampp/htdocs/kap2. Report: docs/REVIEW_WIRKUNGSMECHANISMEN.md. Rahmenmethodik (H·E·V normiert → gewichtetes Mittel → P90 → Outcome=ref·Index/100·scale) NICHT ändern. Neue/geänderte Parameter müssen über PUT /kommune/{id}/parameters editierbar bleiben (custom_source-Pflicht nicht brechen). Nur den unten genannten Block umsetzen, danach committen.

---

## Prompt 1 — Quellen an jeden Parameter (billig, keine Verhaltensänderung)
```
[Kontextzeile]. Umsetzen: In backend/app/data/catalog.py und backend/app/services/
parameter_registry.py jede generische `source` durch einen konkreten Kurz-Key aus §6 des
Reports ersetzen (z.B. "RKI 2022", "UBA MK3.1 2020", "Prognos 2023", "DWD CDC"). Über jeden
ref_value/cost_per_outcome_eur einen Kommentar mit Herleitung setzen.
Akzeptanz: GET /kommune/{id}/parameters liefert für jeden Parameter eine nicht-generische
source; kein bestehender Testwert ändert sich.
```

## Prompt 2 — Info-Fenster = Rechnung (billig, Korrektheit)
```
[Kontextzeile]. Umsetzen (Report §5): (a) lineage_graph.py:574-582 Skalierungs-Tooltip
scale-abhängig aus risk['scale'] (pop→Einw./100.000, area→Fläche/50 km², flat→×1).
(b) indicators.py:135-137 COMPOUND_EVENT auf override_context.normalize_value umstellen.
(c) lineage_graph.py:567 tatsächliches Pfadgewicht einsetzen.
Tests: Skalierungs-Tooltip je scale korrekt; jedes pathway_descriptions-Tupel wird von
catalog.build_pathways erzeugt; Formel-String-Konstanten == indicators.py-Konstanten.
```

## Prompt 3 — INFRA_CRITICALITY & Verkehr auf echte Assets
```
[Kontextzeile]. Umsetzen (Report §B4): indicators.py:185 INFRA_CRITICALITY neu = gewichtete
Dichte aus energy_infra_count, water_wastewater_count, communication_count, Healthcare-
Präsenz, Verkehr; Gewichte als editierbare Parameter (BBK-KRITIS-Sektoren). catalog.py:360
Beschreibung + formulas.py-Formelstring + lineage_operators.py-Schritte angleichen.
indicators.py:152 TRANSPORT_HUBS aus OSM-Knoten (station/halt/public_transport) statt
road_cov·18; osm_data.py-Abfrage erweitern.
Akzeptanz: Kommune mit vielen KRITIS-Assets zeigt höhere INFRA_CRITICALITY als eine ohne.
```

## Prompt 4 — Feste Vulnerabilitäts-Konstanten differenzieren
```
[Kontextzeile]. Umsetzen (Report §B3): FINANCIAL_ADAPTATION_CAPACITY,
PLANNING_IMPLEMENTATION_CAPACITY, income aus BBSR INKAR (Gemeinde-Sozioökonomie) ableiten;
EARLY_WARNING/EMERGENCY aus OSM fire_station/emergency; LEVEE_CONDITION aus OSM
dyke/embankment. Nicht ableitbare bleiben 50, aber editierbar + source="Modellannahme
(mangels lokaler Daten)".
Akzeptanz: zwei unterschiedliche Kommunen liefern unterschiedliche Werte dieser V.
```

## Prompt 5 — Regionale Treiber auf offene Daten (größter Block, ggf. weiter aufteilen)
```
[Kontextzeile]. Umsetzen (Report §B2): inputs.py:279-289 je Treiber echte offene Quelle
anbinden — DWD CDC Raster (heiße/Frosttage), KOSTRA-2020 (Starkregen), UFZ Dürremonitor
(Bodenfeuchte), C3S/DWD-Atlas (Temperaturtrend), DWD/ERA5 (Sturm), BfG/PEGELONLINE
(Niedrigwasser), BSH (Meeresspiegel). Werte am Kommune-/Zell-Zentroid abgreifen und cachen.
Nur wo keine kostenlosen Daten: Proxy behalten UND source/proxy ehrlich als Proxy
kennzeichnen. Bei Token-Knappheit einen Treiber pro Session umsetzen (Report B2.1…B2.9).
Akzeptanz: Kommunen verschiedener Regionen zeigen unterschiedliche Hazard-Treiber.
```

## Prompt 6 — ref_value-Kalibrierung an Statistik
```
[Kontextzeile]. Umsetzen (Report §3): jeden ref_value gegen den Anker in §3 prüfen/justieren
(Punktwert, keine Spanne), Quelle als source + Herleitungskommentar. Struktur (Index=100-
Referenz) beibehalten.
```
