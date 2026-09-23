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
| `frontend/src/components/MapView.tsx:558` | `buildTooltipHtml()`: Ebenen-Label/-Einheit, Zellwerte (H/E/V, Outcome-Faktoren) sowie — im Debug-Block „OSM-Gewässer-Objekte“ — je Objekt `s.tag`, `s.name` und `s.dist_m`; `s.name` ist der rohe OSM-Tag `name` (Backend: `describe_cell_water_sources()` in `backend/app/services/climate/heat/osm_data.py:759-775`, unverändert an `props.water_src` durchgereicht) | Fremddaten mit Quellname, z. B. OpenStreetMap | nein — `s.name` wird als Template-String-Literal (`` `${s.name}` ``) direkt in den HTML-String eingesetzt, keine Escaping-Funktion im Aufrufpfad | ausnutzbar — `s.name` ist ein von Dritten frei editierbarer OSM-Tag; das Backend liefert ihn unverändert, das Frontend fügt ihn unescaped per `setHTML` (MapLibre-Popup, setzt intern `innerHTML`) in die Seite ein. Ein präparierter Tag-Wert (z. B. `<img src=x onerror=…>`) würde beim Hover über die betroffene Zelle ausgeführt. |
| `frontend/src/components/LayerInfoModal.tsx:176` | `FormulaLine`: von `renderFormulaHtml(recipe.formula_index_header)` erzeugtes KaTeX-HTML einer Formelkopfzeile aus dem Recipe-Metadatensatz der Ebene | Katalog im Repo | ja — `katex.renderToString(...)` in `frontend/src/utils/formulaLatex.ts:131` mit `trust: false` (kein `trust: true` gesetzt); KaTeX escaped Textknoten selbst und lässt bei `trust: false` keine roh eingebetteten HTML-Konstrukte (`\href`, `\includegraphics`, `\url`) zu | nicht ausnutzbar — Eingabe stammt aus im Repo definierten Recipe-Formeltexten (kein Nutzer- oder Fremddateneinfluss), und KaTeX rendert mit `trust: false` grundsätzlich sicher, auch bei beliebigem Formeltext |
| `frontend/src/components/LineageFlowDiagram.tsx:282` | `tooltip.innerHTML = html`: Knoten-Tooltip aus `buildNodeTooltip()`/`formatLineageTooltip()` — Titel-, Schlüssel/Wert- und Formelzeilen des Lineage-Diagramms | Katalog im Repo | ja — Textteile laufen durch `esc()` (manuelles HTML-Escaping, `frontend/src/utils/lineageTooltip.ts:4-9`), Formelteile durch `katex.renderToString(...)` mit `trust: false` (wie oben) | nicht ausnutzbar — jeder eingesetzte Text ist entweder per `esc()` escaped oder per KaTeX (`trust: false`) sicher gerendert; die Quelle ist zudem Recipe-/Lineage-Metadaten aus dem Repo-Katalog, nicht Nutzer- oder Fremddateneingabe |
| `frontend/src/pages/landing/LandingMap.tsx:185` | `buildRiskTooltipHtml()` (aufgerufen über `tooltipForId` aus `HotspotWidget`): Ebenen-Label/-Einheit, Faktor-Namen/-Quellen/-Formeln und Zellwerte des Landing-Demo-Widgets | Katalog im Repo | nein — keine Escaping-Funktion im Aufrufpfad, alle Werte werden als Template-String-Literal direkt eingesetzt | nicht ausnutzbar — sämtliche eingesetzten Werte stammen aus der statisch im Repo gebündelten Demo-Momentaufnahme `frontend/src/pages/landing/data/oschatz-landing.json` und den fest codierten Recipe-Definitionen in `landingData.ts`; kein Feld enthält Nutzer- oder Fremddateneingabe |
| `frontend/src/preview/main.tsx:132` | Fest codierter Hinweistext „Keine Vorschau-Daten (window.__LINEAGE_PREVIEW__ fehlt).“ | Konstante im Code | nein — keine Escaping-Funktion, aber es wird kein dynamischer Wert eingesetzt | nicht ausnutzbar — der HTML-String ist ein Literal ohne jede Variable; es gibt keine Eingabe, die ein Angreifer beeinflussen könnte |

## Abhilfe-Vorschläge (für Zeilen mit „ausnutzbar“ oder „unklar“)

- `frontend/src/components/MapView.tsx:558`: `s.name` (und vorsorglich `s.tag`) vor dem
  Einsetzen in den Template-String HTML-escapen (z. B. dieselbe `esc()`-Funktion wie in
  `lineageTooltip.ts` verwenden) oder den Debug-Block auf textContent-basierte
  DOM-Erzeugung statt String-Konkatenation umstellen.
