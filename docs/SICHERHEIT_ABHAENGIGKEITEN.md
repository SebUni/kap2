# Sicherheit der Frontend-Abhängigkeiten

Bewertung der von `npm audit` im Frontend gemeldeten Schwachstellen (Ticket T-0502).
Die Leitfrage: Haben wir ein Sicherheitsproblem? Das hängt davon ab, ob ein Paket im
ausgelieferten Bündel steckt (läuft im Browser der Nutzer) oder nur beim Bauen mitläuft.
**Mit dieser Unterlage wurde keine Abhängigkeitsversion geändert.** Sie ist Grundlage für die
Entscheidung, was zu tun ist.

## Stand

Ausgeführt am **22.09.2026** in `frontend/` (node v20.20.2, npm 10.8.2, Stand `package-lock.json`
auf `main`) mit `npm audit`. Zusammenfassungszeile, wörtlich:

```
11 vulnerabilities (1 low, 3 moderate, 6 high, 1 critical)
```

Der Schweregrad je Paket stammt aus `npm audit --json` (Feld `vulnerabilities.<paket>.severity`);
die Textausgabe führt `vite` und `react-router-dom` nur eingerückt als abhängige Pakete ohne eigene
Severity-Zeile, die JSON-Ausgabe weist beiden „high" zu. Summe: 1 low, 3 moderate, 6 high,
1 critical = 11 Zeilen.

## Wie „Laufzeit" und „nur Bau" festgestellt wurden

`npm ls --omit=dev` hilft hier **nicht**: `frontend/package.json` führt alle Pakete — auch
`vite` und `typescript` — unter `dependencies`, es gibt keine `devDependencies`. Maßgeblich ist
deshalb, was der Bau tatsächlich ins Bündel schreibt. Dafür zwei Befehle:

1. **Abhängigkeitspfad:** `npm ls <paket>` in `frontend/` zeigt, über welches Paket es hereinkommt.
2. **Modulliste des Bündels (Probebau):** Ein Vite-Bau mit unveränderter `vite.config.ts` und einem
   zusätzlichen Plugin, das in `generateBundle` für jeden Chunk die enthaltenen Module
   (`chunk.modules`) nach Paketname ausgibt. Aufruf aus `frontend/` als Datei `probe.mjs`,
   gestartet mit `node probe.mjs`:

   ```js
   import { build } from 'vite'
   const pakete = new Map()
   await build({ configFile: 'vite.config.ts', logLevel: 'warn', plugins: [{
     name: 'modulliste',
     generateBundle(_o, bundle) {
       for (const [datei, c] of Object.entries(bundle)) {
         if (c.type !== 'chunk') continue
         for (const id of Object.keys(c.modules)) {
           if (!id.includes('node_modules/')) continue
           const rest = id.split('node_modules/').pop(); const t = rest.split('/')
           const name = rest.startsWith('@') ? t[0] + '/' + t[1] : t[0]
           pakete.set(name, datei)
         }
       }
     } }] })
   for (const [n, d] of [...pakete].sort()) console.log(n + '\t' + d)
   ```

   Ergebnis am 22.09.2026 (Exit 0): Von den elf gemeldeten Paketen stehen
   nur **`maplibre-gl`** (Chunk `assets/vendor-maplibre-*.js`), **`react-router`** und
   **`react-router-dom`** (Chunk `assets/vendor-react-*.js`) in der Liste. `@babel/core`,
   `baseline-browser-mapping`, `browserslist`, `esbuild`, `vite`, `postcss`, `nanoid` und
   `protocol-buffers-schema` kommen darin nicht vor; `grep -c protocol-buffers-schema
   dist/assets/*.js` liefert für jede Datei 0.

Zum Betrieb: Die Testumgebung liefert das Frontend als statisches `frontend/dist` über Apache aus
(`deploy/apache-kap2-test.conf`, `DocumentRoot …/frontend/dist`); ein Vite-Entwicklungsserver läuft
dort nicht (`ss -ltn` am 22.09.2026: kein Dienst auf Port 5173). Der Entwicklungsserver
(`start-dev.sh`, `vite --host 0.0.0.0 --port 5173`) läuft nur auf Entwicklerrechnern.

## Tabelle

| # | Paket (installiert) | Schweregrad laut Audit | Laufzeit im Bündel oder nur Bau (Befehl) | Ausnutzbar in unserem Betrieb | Empfohlene Behandlung |
|---|---|---|---|---|---|
| 1 | `maplibre-gl` 5.21.1 (direkt) | critical | **Laufzeit** — Probebau: Chunk `assets/vendor-maplibre-*.js`; `npm ls maplibre-gl` → direkte Abhängigkeit; `grep -c DOMParser dist/assets/vendor-maplibre-*.js` → 1 (der betroffene `DOM.sanitize()` ist enthalten) | **nein** — `DOM.sanitize()` (GHSA-jrc7-96c5-q579) wird nur für die Quellenangabe der Karte aufgerufen (`attribution_control.ts`), und die stammt bei uns ausschließlich aus festen Zeichenketten im Quelltext (`'&copy; OpenStreetMap contributors'` in `MapView.tsx`, `LiteMap.tsx`, `LandingMap.tsx`), nie aus Nutzer- oder Fremddaten. | Eigenes Ticket: Aktualisierung auf ≥ 6.5 (Audit schlägt 6.11.0 vor, **Hauptversionssprung** 5 → 6) mit Kartentest aller drei Kartenansichten. Bis dahin gilt: keine Quellenangaben aus Fremd- oder Nutzerdaten in Kartenquellen übernehmen. |
| 2 | `react-router` 7.13.2 (über `react-router-dom`) | high | **Laufzeit** — Probebau: Chunk `assets/vendor-react-*.js`; `npm ls react-router` → `react-router-dom@7.13.2 └── react-router@7.13.2` | **unklar** — die hohen Meldungen (turbo-stream-RCE, `__manifest`, single-fetch, RSC-CSRF, SSR-Hydration) betreffen Server-/Framework-/RSC-Betrieb, den wir nicht nutzen (reines `BrowserRouter` im Browser, kein Node-Server), die mittlere Meldung „Open redirect via backslash in `<Link>` and `useNavigate`" (GHSA-wrjc-x8rr-h8h6) betrifft aber unseren Modus, und `LoginPage.tsx` übergibt `location.state.from` an `navigate()` — ob sich darüber ein fremdes Ziel einschleusen lässt, ist nicht geprüft. | Aktualisierung innerhalb 7.x auf ≥ 7.18.2 per `npm audit fix` (**kein** Hauptversionssprung), danach `npm run build`, `npm run typecheck` und Klicktest Login-Umleitung. Vorrangig vor allen anderen Zeilen, weil im Bündel und nicht ausgeschlossen. |
| 3 | `react-router-dom` 7.13.2 (direkt) | high | **Laufzeit** — Probebau: Chunk `assets/vendor-react-*.js`; `npm ls react-router-dom` → direkte Abhängigkeit | **unklar** — das Paket hat keine eigene Meldung, sondern erbt sie von `react-router` (Zeile 2), dessen Browser-Teil es neu exportiert; es gilt dieselbe offene Frage zur Login-Umleitung. | Gemeinsam mit Zeile 2: `npm audit fix` hebt beide innerhalb 7.x an. |
| 4 | `vite` 5.4.21 (direkt) | high | **nur Bau** — nicht in der Modulliste des Probebaus; `npm ls vite` → direkte Abhängigkeit (Bauwerkzeug und Entwicklungsserver) | **nein** — alle drei Meldungen betreffen den Entwicklungsserver (`server.fs.deny`-Umgehung und `launch-editor` nur unter Windows, Pfad-Traversal bei `.map` der optimierten Abhängigkeiten), und der läuft im Test-/Kundenbetrieb nicht; ausgeliefert wird statisches `dist` über Apache. | Eigenes Ticket: Aktualisierung auf Vite ≥ 6.4.3 bzw. den vom Audit vorgeschlagenen 8.3.0 (**Hauptversionssprung**, bricht ggf. Konfiguration). Bis dahin: Entwicklungsserver nur in vertrauenswürdigem Netz starten. |
| 5 | `esbuild` 0.21.5 (über `vite`) | moderate | **nur Bau** — nicht in der Modulliste des Probebaus; `npm ls esbuild` → `vite@5.4.21 └── esbuild@0.21.5` | **nein** — GHSA-67mh-4wv8-2f99 betrifft esbuilds eigenen Entwicklungsserver (`esbuild serve`), den Vite 5 nicht startet und der bei uns nirgends läuft. | Erledigt sich mit der Vite-Aktualisierung (Zeile 4); kein eigener Schritt. |
| 6 | `postcss` 8.5.8 (über `vite`) | high | **nur Bau** — nicht in der Modulliste des Probebaus; `npm ls postcss` → `vite@5.4.21 └── postcss@8.5.8` | **nein** — die Meldungen (XSS über `</style>` in der Ausgabe, Dateilesen über `sourceMappingURL`) setzen fremdes CSS als Eingabe voraus; beim Bau verarbeitet PostCSS nur unser eigenes CSS aus dem Repo und `maplibre-gl.css`. | `npm audit fix` (kein Hauptversionssprung), gebündelt mit Zeile 2. |
| 7 | `nanoid` 3.3.11 (über `postcss`) | high | **nur Bau** — nicht in der Modulliste des Probebaus; `npm ls nanoid` → `vite@5.4.21 └── postcss@8.5.8 └── nanoid@3.3.11` | **nein** — Endlosschleife/Überlauf nur bei negativer, null oder übergroßer Längenangabe an eigene Generatoren; PostCSS ruft es beim Bau mit festen Werten auf, keine Eingabe von außen. | `npm audit fix` (kein Hauptversionssprung), gebündelt mit Zeile 2. |
| 8 | `browserslist` 4.28.1 (über `@babel/core`) | high | **nur Bau** — nicht in der Modulliste des Probebaus; `npm ls browserslist` → `@vitejs/plugin-react@4.7.0 └── @babel/core@7.29.0 └── … └── browserslist@4.28.1` | **nein** — Speicherwachstum bei vielen verschiedenen Abfragen und Absturz über eine manipulierte `browserslist-stats.json`; beim Bau gibt es eine feste Abfrage und keine solche Datei von außen. | `npm audit fix` (kein Hauptversionssprung), gebündelt mit Zeile 2. |
| 9 | `baseline-browser-mapping` 2.10.12 (über `browserslist`) | moderate | **nur Bau** — nicht in der Modulliste des Probebaus; `npm ls baseline-browser-mapping` → `… browserslist@4.28.1 └── baseline-browser-mapping@2.10.12` | **nein** — Prozessabbruch bei ungültiger Eingabe trifft höchstens einen Bau, und die Eingabe stammt aus unserer eigenen Konfiguration. | `npm audit fix` (kein Hauptversionssprung), gebündelt mit Zeile 2. |
| 10 | `@babel/core` 7.29.0 (über `@vitejs/plugin-react`) | low | **nur Bau** — nicht in der Modulliste des Probebaus; `npm ls @babel/core` → `@vitejs/plugin-react@4.7.0 └── @babel/core@7.29.0` | **nein** — Dateilesen über einen `sourceMappingURL`-Kommentar setzt fremden Quelltext als Bau-Eingabe voraus; gebaut wird nur unser eigener Code. | `npm audit fix` (kein Hauptversionssprung), gebündelt mit Zeile 2. |
| 11 | `protocol-buffers-schema` 3.6.0 (über `maplibre-gl` → `pbf` → `resolve-protobuf-schema`) | moderate | **nur installiert, nicht im Bündel** — nicht in der Modulliste des Probebaus; `grep -c protocol-buffers-schema dist/assets/*.js` → 0 je Datei; `npm ls protocol-buffers-schema` → `maplibre-gl@5.21.1 └── pbf@4.0.1 └── resolve-protobuf-schema@2.1.0 └── protocol-buffers-schema@3.6.0` | **nein** — maplibre-gl wird als fertig gebautes `dist/maplibre-gl.js` eingebunden; der Schema-Parser gehört zum Werkzeug `pbf` zum Übersetzen von `.proto`-Dateien und wird weder im Browser noch beim Bau aufgerufen. | `npm audit fix` (kein Hauptversionssprung), gebündelt mit Zeile 2. |

## Ergebnis in einem Satz

Im Browser unserer Nutzer laufen drei der elf gemeldeten Pakete; die kritische maplibre-Lücke ist
bei uns nicht erreichbar, bei react-router ist eine mittlere Umleitungs-Lücke im Login-Ablauf nicht
ausgeschlossen („unklar"), die übrigen acht betreffen nur Bau oder Entwicklungsserver.
