# HTML-Ausgabe ohne Escaping im eigenen Frontend — Bewertung

Anlass: T-0502 (Beobachtung des Entwicklers, Frage des Prüfers
Q-20260922T231221Z-pruefer-c8533a-3). `MapView` und `LandingMap` setzen HTML über
`setHTML`, `LayerInfoModal` über `dangerouslySetInnerHTML`. Diese Tabelle bewertet jede
Stelle, an der das Frontend selbst HTML erzeugt und ohne den React-JSX-Renderweg in den
DOM setzt (`setHTML`, `dangerouslySetInnerHTML`, `innerHTML`) — je Fund einer der
folgenden Aufrufe, mit Datenherkunft und Ausnutzbarkeits-Urteil.

Befehl:

```
grep -rnE "setHTML|dangerouslySetInnerHTML|innerHTML" frontend/src | wc -l
```

Ausgabe: **5**

| Stelle | Eingesetzte Werte | Herkunft | Escaping | Urteil |
|---|---|---|---|---|
| `frontend/src/components/MapView.tsx`, `buildTooltipHtml()` | `buildTooltipHtml()`: Ebenen-Label/-Einheit, Zellwerte (H/E/V, Outcome-Faktoren) sowie — im Debug-Block „OSM-Gewässer-Objekte“ — je Objekt `s.tag`, `s.name`, `s.osm_type` und `s.dist_m`; die OSM-Felder stammen aus `describe_cell_water_sources()` in `backend/app/services/climate/heat/osm_data.py`, unverändert an `props.water_src` durchgereicht | Fremddaten mit Quellname, z. B. OpenStreetMap | ja — `s.name`, `s.tag` und `s.osm_type` laufen durch `escHtml()` aus `frontend/src/utils/escapeHtml.ts`, bevor sie in den Template-String eingesetzt werden | behoben (T-0602-ceo, T-0640-ceo) — `s.name` und `s.osm_type` sind von Dritten frei editierbare bzw. -beeinflussbare OSM-Werte; das Backend liefert sie unverändert, das Frontend escaped sie inzwischen vor dem Einsetzen per `setHTML` (MapLibre-Popup, setzt intern `innerHTML`). Ohne Escaping hätte ein präparierter Wert beim Hover über die betroffene Zelle ausgeführt werden können. |
| `frontend/src/components/LayerInfoModal.tsx`, `FormulaLine` | `FormulaLine`: von `renderFormulaHtml(recipe.formula_index_header)` erzeugtes KaTeX-HTML einer Formelkopfzeile aus dem Recipe-Metadatensatz der Ebene | Katalog im Repo | ja — `katex.renderToString(...)` in `frontend/src/utils/formulaLatex.ts` mit `trust: false` (kein `trust: true` gesetzt); KaTeX escaped Textknoten selbst und lässt bei `trust: false` keine roh eingebetteten HTML-Konstrukte (`\href`, `\includegraphics`, `\url`) zu | nicht ausnutzbar — Eingabe stammt aus im Repo definierten Recipe-Formeltexten (kein Nutzer- oder Fremddateneinfluss), und KaTeX rendert mit `trust: false` grundsätzlich sicher, auch bei beliebigem Formeltext |
| `frontend/src/components/LineageFlowDiagram.tsx`, `tooltip.innerHTML = html` | `tooltip.innerHTML = html`: Knoten-Tooltip aus `buildNodeTooltip()`/`formatLineageTooltip()` — Titel-, Schlüssel/Wert- und Formelzeilen des Lineage-Diagramms | Katalog im Repo | ja — Textteile laufen durch `escHtml()` aus `frontend/src/utils/escapeHtml.ts` (in `lineageTooltip.ts` eingebunden), Formelteile durch `katex.renderToString(...)` mit `trust: false` (wie oben) | nicht ausnutzbar — jeder eingesetzte Text ist entweder per `escHtml()` escaped oder per KaTeX (`trust: false`) sicher gerendert; die Quelle ist zudem Recipe-/Lineage-Metadaten aus dem Repo-Katalog, nicht Nutzer- oder Fremddateneingabe |
| `frontend/src/pages/landing/LandingMap.tsx`, `buildRiskTooltipHtml()` | `buildRiskTooltipHtml()` (aufgerufen über `tooltipForId` aus `HotspotWidget`): Ebenen-Label/-Einheit, Faktor-Namen/-Quellen/-Formeln und Zellwerte des Landing-Demo-Widgets | Katalog im Repo | nein — keine Escaping-Funktion im Aufrufpfad, alle Werte werden als Template-String-Literal direkt eingesetzt | nicht ausnutzbar — sämtliche eingesetzten Werte stammen aus der statisch im Repo gebündelten Demo-Momentaufnahme `frontend/src/pages/landing/data/oschatz-landing.json` und den fest codierten Recipe-Definitionen in `landingData.ts`; kein Feld enthält Nutzer- oder Fremddateneingabe |
| `frontend/src/preview/main.tsx`, Modul-Top-Level (kein Funktionsaufruf) | Fest codierter Hinweistext „Keine Vorschau-Daten (window.__LINEAGE_PREVIEW__ fehlt).“ | Konstante im Code | nein — keine Escaping-Funktion, aber es wird kein dynamischer Wert eingesetzt | nicht ausnutzbar — der HTML-String ist ein Literal ohne jede Variable; es gibt keine Eingabe, die ein Angreifer beeinflussen könnte |

## Abhilfe-Vorschläge (für Zeilen mit „ausnutzbar“ oder „unklar“)

Keine offen — alle bekannten Fundstellen sind behoben (siehe Tabelle oben).
