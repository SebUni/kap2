# Quellen-Anreicherung — Übergabe-Prompts (IEEE-Zitation + Wayback-Snapshot)

Ziel: Jeder belegte Parameterwert bekommt eine **zitierfähige** Herkunft, die im
(i)-Hover-Tooltip (Sidebar **und** Konfigurations-Tabelle) sichtbar ist:
IEEE-Zitation + klickbare **Live-URL** + archivierter **Wayback-Snapshot** (falls
die Quelle offline geht) + der Herleitungs-Langtext (`source_details`).

## Status (Juli 2026): VOLLSTÄNDIG — Ratchet bei 0

**Alle anwendbaren Parameter der Konfigurations-Registry haben einen Infokasten**
(Herleitung in `source_detail` und/oder IEEE-`references`). Erzwungen durch den
Ratchet-Test `backend/tests/test_parameter_docs_complete.py`:

- `KNOWN_MISSING` ist **leer** — jeder neue Parameter ohne Doku lässt die Suite
  sofort fehlschlagen (`test_docs_ratchet_no_new_undocumented`).
- Offene IDs listet jederzeit:
  `cd backend && python tests/test_parameter_docs_complete.py --list`
- Tote Parameter (9 Pfadgewichte + 18 fest verdrahtete Formel-Konstanten) sind aus
  der Registry entfernt; nur override-fähige Formel-Inputs
  (`formulas._i(..., overridable=True)`) werden emittiert.
- Neu aufgenommen und belegt: `model.*` (Referenzskalierung, Risikozonen-Schwelle,
  Maßnahmen-Sättigung/-Kappung), `regional.*` (Proxy-/Fallback-Klimatreiber),
  `uhi.epsilon`/`uhi.tree_cooling`, `impact.floor_height_m`,
  `risks.EXPECTED_ANNUAL_MENTAL_HEALTH.impact.event_share` — Single Source:
  `backend/app/services/engine/tunables.py`.

### Wo die Herleitungen liegen (nicht neu bauen)

| Parameterart | Ort der Doku |
| --- | --- |
| Maßnahmen-Kostenfelder (Einzelrecherche) | inline `sources`/`source_details`/`source_refs` je Maßnahme in `catalog.py` |
| Maßnahmen-Wirkung/-Nutzen (Cluster-Batches) | zentraler Block `_MEASURE_EFFECT_DOCS` in `catalog.py` |
| Bewusste 0-Werte (`capex_fixed`/`benefit` = 0) | Auto-Anreicherung `_enrich_measure_zero_cost_docs()` in `catalog.py` (maßnahmen­spezifisch generiert; inline-Einträge haben Vorrang) |
| model/regional-Stellschrauben | Spec-Listen in `engine/tunables.py` |
| Impact-Parameter (Schicht B) | `engine/impact/params.py` |
| UHI-Koeffizienten | uhi-Block in `parameter_registry.py` |
| Live-Formel-Parameter (KRITIS-Gewichte, Fallback-Konstanten) | `overridable=True`-Inputs in `engine/formulas.py` |
| H/E/V-Normgrenzen, Risiko-ref_values/Kostensätze | Katalog-Dicts + `_enrich_*`-Funktionen in `catalog.py` |

## Grundlagen (in JEDER Session mitschicken)

```
Kontext: Klimarisiko-Tool, Repo /opt/lampp/htdocs/kap2. Quellen-Bibliografie liegt in
backend/app/data/sources.py (SOURCE_REFERENCES: key -> {ieee, url, archive_url, accessed}),
resolve() hängt sie an CostComponents/Registry-Parameter (Feld "references"). Katalog-
Einträge verweisen per source_refs = {feld: [key, ...]}.

Regeln:
- Dort wo deine Recherchen von den hinterlegten Werten abweichen, ersetze die bestehenden
  Werte um konsistent zu bleiben — dokumentiere im source_detail "angepasst von X auf Y
  gemäß [Quelle]" und plausibilisiere (Größenordnung, Cluster-Konsistenz, pytest).
- NUR belastbare, real existierende Quellen. Reine "Modellannahme (…)"-Felder bleiben
  ohne source_refs (die ehrliche Prosa in source_details genügt) — nichts erfinden.
- JEDER anwendbare Parameter braucht mindestens einen source_details-Text — auch 0-Werte
  ("warum ist das 0?"); der Ratchet-Test erzwingt das.
- IEEE-Zitation deutsch lokalisiert, Schema:
  Autor/Institution, „Titel,“ Ort, Jahr. [Online]. Verfügbar: <url>. [Zugriff: 6. Juli 2026].
  (Bei >3 Autoren: "A. Erstautor u. a.". Ohne Jahr: Jahr weglassen.)
- Jede neue Quelle ZWINGEND archivieren (Wayback), archive_url MUSS ein
  web.archive.org-Permalink sein:
    curl -s -I "https://web.archive.org/save/<url>" | grep -i '^location:'
  Falls leer (PDF/langsam/Ratelimit) den jüngsten vorhandenen Snapshot nehmen:
    curl -s "https://web.archive.org/cdx/search/cdx?url=<url>&output=json&limit=-1&filter=statuscode:200"
    -> https://web.archive.org/web/<timestamp>/<url>
- bib_key: sprechend + stabil (z. B. "DWA_A138", "VDI_2067_Blatt1").
- Verifikation: cd backend && python -m pytest tests/ -q
  (test_measure_pricing prüft source_refs -> Bibliografie und Eintrag-Vollständigkeit;
  test_parameter_docs_complete prüft die Infokasten-Vollständigkeit als Ratchet.)
```

Einen neuen Bibliografie-Eintrag anlegen (in `sources.py`) und verdrahten (in `catalog.py`):

```python
# sources.py
"DWA_A138": {
    "ieee": "Deutsche Vereinigung für Wasserwirtschaft, Abwasser und Abfall e.V. (DWA), "
            "„Arbeitsblatt DWA-A 138: Planung, Bau und Betrieb von Anlagen zur Versickerung "
            "von Niederschlagswasser,“ Hennef, Deutschland, 2005. [Online]. Verfügbar: "
            "<url>. [Zugriff: 6. Juli 2026].",
    "url": "<live-url>",
    "archive_url": "https://web.archive.org/web/<ts>/<url>",
    "accessed": "2026-07-06",
},
# catalog.py, in der Maßnahme (neben sources/source_details):
"source_refs": {"capex_per_m2": ["DWA_A138"], "opex_per_m2_year": ["DWA_A138"]},
```

---

## Fortsetzungs-Prompt (Pflege / neue Parameter)

Der folgende Prompt hält den Zustand „kein genutzter Parameter ohne Erklärung“
dauerhaft aufrecht — für neue Parameter, Vertiefung bestehender Herleitungen oder
das Nachziehen besserer Quellen:

```
Kontext: Klimarisiko-Tool, Repo /opt/lampp/htdocs/kap2 (+ Grundlagen-Block aus
docs/QUELLEN_ANREICHERUNG_PROMPTS.md).

Aufgabe:
1. cd backend && python tests/test_parameter_docs_complete.py --list
   → listet alle anwendbaren Parameter ohne Infokasten (Soll: 0).
2. Für jede gelistete ID: Herleitung (source_detail) schreiben — Wirkmechanismus,
   Wertherleitung inkl. Bandbreite, ehrliche Kennzeichnung als Modellannahme wo
   keine belastbare Quelle existiert; belastbare Quellen als IEEE-Eintrag in
   sources.py anlegen (inkl. Wayback-archive_url) und per source_refs verdrahten.
   Ablageorte je Parameterart: siehe Tabelle "Wo die Herleitungen liegen".
3. Weicht ein recherchierter Wert vom hinterlegten ab: Wert ersetzen und im
   source_detail "angepasst von X auf Y gemäß [Quelle]" dokumentieren;
   plausibilisieren (Größenordnung je Einheit prüfen — €/m² vs. €/ha!,
   Cluster-Konsistenz, Kappungsgrenzen 0,05-0,50 bei default_reduction).
4. KNOWN_MISSING in tests/test_parameter_docs_complete.py auf den neuen Stand
   schrumpfen (Soll: leer lassen) und die volle Suite laufen lassen:
   python -m pytest tests/ -q → alles grün, dann committen.
5. Prüfe bei neuen/geänderten Maßnahmen die Feld-Plausibilität (B-Audit):
   Hat jede bauliche/technische Maßnahme realistische OPEX (VDI-2067-Größenordnung,
   Kühlung/Pumpen auch Energie)? Ist benefit_per_m2_year frei von Doppelzählung
   mit den vermiedenen Schäden und in €/m² plausibel (ha-Maßstab für Agrar/Forst)?
```

## Abgeschlossene Batches (Referenz)

| Batch | Inhalt | Anker-Quellen |
| --- | --- | --- |
| Phase A (Struktur) | tote Parameter raus, 20 neue Stellschrauben verdrahtet+belegt, Ratchet-Test | — |
| B0 | systematische 0-Wert-Herleitungen (capex_fixed=0, benefit=0) | Modellentscheidungs-Texte |
| B1 Energie/Wirtschaft | Netzverstärkung (0,30), Kühlung (+OPEX!), PV+Speicher, kritische Knoten, Lieferketten, Leckage | BNetzA_SAIDI_2023, VDI_2067_Blatt1, HTW, DVGW, RONT |
| B2 Hitze/Gesundheit | HAP (0,20→**0,25** gemäß Studie), kühle Räume (+OPEX), Frühwarnung, Evakuierung, Stadtgrün, Schneisen, helle Dächer/Beläge, Trinkbrunnen, vulnerable Gruppen, Arbeitszeit | **Urban_HHAP_Wirksamkeit_2025** (−25,2 % Hitzemortalität), WMO_EarlyWarnings, VDI 3787 |
| B3 Wasser/Starkregen | Entsiegelung, Schwammstadt, Retention/Polder, Versickerung, Abflusslenkung, GW-Anreicherung | DWA_A138, BWB_Niederschlagswasserentgelt (1,84 €/m²·a), Agrarheute, UBA |
| B4 Gebäude | Gründach/Fassade, Objektschutz | BuGG, co2online, BBK_Hochwasserschutzfibel |
| B5 Küste/Land/Forst | Deich (+OPEX 10 T€/km·a), Sperrwerke (+OPEX), Erosion, Auen, Mischwald, Humus, Sorten, Bewässerung, Waldbrand, Biotopverbund — **9 Agrar-/Forst-Nutzenwerte auf ha-Maßstab plausibilisiert** | NLWKN, LfL, KTBL, AGDW, TEEB DE, UBA |
| B6 Fischerei/Anreize | adaptives Management, Aquakultur (+OPEX), Laichhabitate, Gewässergüte, Fischaufstieg (+OPEX), Anreiz-/Investitionsprogramme | LfU_Bayern_Fischaufstieg, UBA_Gewaesserrenaturierung |

Methodik-Ergänzung (B1): Flat-skalierte verknüpfte Risiken (z. B. Ausfallstunden bei
Netzverstärkung) liefern jetzt einen Einzelmaßnahmen-Nutzen als Delta der kommunen-
weiten P90-Outcome-Kosten (`measure_service.compute_impact`, Feld
`annual_benefit_flat_eur`) — vorher stand dort 0 € trotz CAPEX.
