# #95 Hitzebelastung — Regel 6 in einem Durchgang über den ganzen Bericht

Prüfakte zu T-1790-ceo (06.10.2026), getrennt von der Kundenfassung. Gegenstand ist `docs/methodik/95_hitzebelastung.md`. Basis-Stand ist `origin/ticket/T-1742-supervisor`, Commit `6b21dd48`.

## Grenze

Festlegung des CEO in T-1660-ceo vom 06.10.2026 zu Regel 6 (`.claude/methodik-loop.md`): Im Bericht bleibt, was als Vorgabe gilt. Das ist, wie gerechnet wird, welche Datenebene das Produkt führt, welcher Anzeigetext erscheint und welcher Wert an die Stelle eines anderen tritt, im Präsens und ohne Zeitbezug auf die Umsetzung. Umsetzungsstand ist jeder Satz, der sagt, was Code oder Produkt heute tun oder noch nicht tun, und jeder Satz, der auf ein Umsetzungsereignis, eine Rolle oder ein Ticket verweist. Solche Sätze werden gestrichen oder zeitlos gefasst; weicht der Code ab, steht ein Ledger-Befund mit Termin und Zuständigem (Regel 7). Im Entscheidungslog bleiben Zahlen und Entscheidungen einer Zeile, wie sie galten, aber keine Zeile stellt einen heutigen Code-Stand fest. Den Statusblock (von `Status:` bis zur ersten Leerzeile) fasst dieses Paket ohne Ticketkennung und ohne Prüfrunde (Festlegung cto in T-1660-ceo, 06.10.2026, 09:31 UTC).

## Suchmuster M und Zählausdruck

Suchmuster M (Python, `re`), wörtlich:

```
(?i)(im produkt|im code|integration|integriert|nachzug|ratchet|umsetzung|umgesetzt|bis dahin|derzeit|noch nicht|\bcto\b|entwickler|\bT-\d{3,4}\b)
```

Zählausdruck, ausgeführt im Wurzelverzeichnis des Produkt-Repos:

```
python3 -c "import re;M=r'(?i)(im produkt|im code|integration|integriert|nachzug|ratchet|umsetzung|umgesetzt|bis dahin|derzeit|noch nicht|\bcto\b|entwickler|\bT-\d{3,4}\b)';print(sum(1 for l in open('docs/methodik/95_hitzebelastung.md',encoding='utf-8') if re.search(M,l)))"
```

Ausgabe auf dem Basis-Stand: `59`. Ausgabe auf dem Endstand: `44`.

**n = 44.** Genau 44 Zeilen der Liste tragen die Entscheidung `Vorgabe` oder `Log, Stand von damals`; sie treffen M auf dem Endstand weiter. Die übrigen 15 Treffer sind zeitlos gefasst, gestrichen oder einem Befund zugeordnet und treffen M auf dem Endstand nicht mehr. M trifft auch Zeilen, die bleiben (Methodensätze, Quellentitel, Entscheidungslog); deshalb ist die Liste der Nachweis, nicht die Zahl.

## Trefferliste (Basis-Stand)

Satzanfang: der Satz oder die Tabellenzelle, in dem der erste Treffer der Zeile steht, höchstens 80 Zeichen; ein senkrechter Strich ist als `\|` geschrieben. „Zeile Endstand“ nennt die Zeile nach diesem Paket, „—“ heißt: Zeile entfällt.

| Zeile Basis | Zeile Endstand | Satzanfang | Entscheidung | Begründung |
|---|---|---|---|---|
| 4 | — | T-1642-cmo: Abschnitt A mit den Urteilen zu T-1653-methodik_manager, Runde 48, u | `zeitlos gefasst` | Statusblock ohne Ticketkennung und Prüfrunde (Nachtrag des CEO, Festlegung cto in T-1660-ceo); Null-Runde und Nachweis nur im Ledger, der Block verweist dorthin |
| 5 | — | Runde 46, Abschnitt B mit dem Urteil zu T-1648-methodik_manager, Runde 47, je „N | `zeitlos gefasst` | wie Z. 4 |
| 14 | 11 | Instruktionsquelle: `docs/AUFGABE_METHODIK_SCHADENSRECHNUNG.md` (v2) · Umsetzung | `Vorgabe` | „Umsetzungsgrundlage“ nennt den gewählten Ansatz 95-A (Methode), keinen Stand von Code oder Produkt |
| 17 | 14 | 8 = Fortschreibung nach der Integration (30.08.2026, | `zeitlos gefasst` | „nach der Integration“ (Umsetzungsereignis) entfällt; Rev. 8 trägt nur ihr Datum |
| 133 | 130 | Im Produkt entsteht daraus der Wert „mit Anpassung" erst, wenn eine Kommune | `Vorgabe` | wie das Produkt den Wert „mit Anpassung“ bildet; Präsens ohne Zeitbezug |
| 142 | 139 | die §2.8-E-Regeln sind in der Aufgabe noch nicht definiert (Lücken-Vermerk §2.8) | `zeitlos gefasst` | „noch nicht definiert“ wird „definiert keine“; betrifft die Aufgabe, keinen Code |
| 183 | 180 | Produktfunktionen wie im Produkt (`dwd_cdc_grid.summer_mean_temp_at`, | `Vorgabe` | mit welchen Funktionen die Werte der Beispielkommune abgegriffen sind (Rechenweg) |
| 230 | 227 | (c) **Altersbänder je Zelle wie im Produkt ohne Gemeindeschlüssel: × 0,984 = 0,9 | `Vorgabe` | Rechenebene der Altersbänder je Zelle ohne Gemeindeschlüssel (Modellgrenze §3.3) |
| 394 | 391 | NW, RP, SL, HE, SN, ST, TH · Süd = BW, BY (identisch im Produktionscode | `zeitlos gefasst` | „identisch im Produktionscode“ (Code-Stand) wird „dieselbe Zuordnung gilt in“ |
| 518 | 515 | Runde 17, T-1199; das Skript rechnet diese Fassung nicht mehr). Der Rest aus der | `zeitlos gefasst` | Ticketkennung und „das Skript rechnet diese Fassung nicht mehr“ (Code-Stand) entfallen; Messung und Ledger-Verweis bleiben |
| 823 | 820 | u.); \(\bar q\) = **0,346** (Mikrozensus 2023 [63]); Zensus-Gitterwert ersetzt b | `zeitlos gefasst` | entschieden in T-1660-ceo; der Ersatz hängt an einer Zellquelle statt an der Integration |
| 830 | 827 | Voreinstellung **0,11** (Band 0,05–0,15), Abschätzung von KAP3 aus [71] und [72] | `Vorgabe` | welcher Wert an die Stelle eines anderen tritt (Eingabe der Kommune statt Voreinstellung) |
| 852 | — | Verifikationsergebnis der Integration 30.08.2026: keine der beiden Zellgrößen wa | `gestrichen` | Verifikationsergebnis der Integration (Umsetzungsereignis, Stand des Produkts) entfällt |
| 1160 | 1154 | Andockpunkt im Produkt: Maßnahme `COOLING_ROOMS_DRINKING_WATER` („Kühle Räume /  | `Vorgabe` | Andockpunkt: an welcher Maßnahme die Methodik ansetzt |
| 1217 | 1211 | S157 mit seiner Voreinstellung im Anpassungspotenzial (Befund 149).** Die Charak | `Vorgabe` | wie die Charakterisierung je Maßnahme rechnet |
| 1306 | 1300 | Andockpunkt im Produkt:** dieselbe Maßnahme `COOLING_ROOMS_DRINKING_WATER` („Küh | `Vorgabe` | Andockpunkt: an welcher Maßnahme die Methodik ansetzt |
| 1414 | — | Im Produkt steht die Maßnahme `VULNERABLE_GROUP_PROGRAMS` mit | `Befund 223` | Satz Z. 1414–1416 gestrichen; die verworfene Variante 0.22 steht in Log 43 |
| 1508 | 1499 | Im Produkt | `Vorgabe` | Anzeigetext der Parameterliste; entschieden in T-1660-ceo |
| 1513 | 1504 | Klimawirkungen gilt, wird risikoübergreifend festgelegt; bis dahin zählt das Pro | `Befund 224` | Halbsatz „bis dahin zählt das Produkt …“ gestrichen; die Abweichung im Code führt Befund 225 |
| 1702 | 1693 | band: null   # Mikrozensus 2023; Zensus-Gitterwert (bevoelkerungsgewichtet) erse | `zeitlos gefasst` | entschieden in T-1660-ceo; Kommentar wie Z. 823 |
| 1907 | 1898 | def p_unter(x, n=2000):                        # Anteil der Werte von g bis x, u | `Vorgabe` | „integriert“ meint das Integral über OR_ohne (Rechenweg im Prüfblock) |
| 2163 | — | `sources.py`-Ratchet-Mechanik der Plattform (automatisierte Wayback-Permalink-Er | `zeitlos gefasst` | „Ratchet-Mechanik der Plattform“ wird `sources.py` |
| 2164 | — | maschinell testbewehrt — kein manueller Später-Schritt); bis zum Integrations-Ra | `zeitlos gefasst` | entschieden in T-1660-ceo; „bis zum Integrations-Ratchet“ wird „fehlt ein Snapshot“ |
| 2287 | 2276 | für Deutschland — Teilbericht 6: Integrierte Auswertung – Klimarisiken, Handlung | `Vorgabe` | Quelle [UBA KWRA Teil 6], Titel „Integrierte Auswertung“; kein Umsetzungsstand |
| 2289 | 2278 | (Publikationsseite https://www.umweltbundesamt.de/publikationen/KWRA-Teil-6-Inte | `Vorgabe` | wie Z. 2287 (Adresse der Publikationsseite) |
| 2290 | 2279 | PDF https://www.umweltbundesamt.de/sites/default/files/medien/479/publikationen/ | `Vorgabe` | wie Z. 2287 (Adresse des PDF) |
| 2291 | 2280 | abgerufen 25.09.2026; im Repo | `Vorgabe` | wie Z. 2287 (Ablage im Repo) |
| 2318 | 2307 | Integrationsschritt wie bei [46]). Verwendet in §5 (Schutzprogramme vulnerable G | `zeitlos gefasst` | „über den Integrationsschritt“ wird „über `sources.py`“ |
| 2325 | 2314 | Snapshot über den Integrationsschritt wie bei [46]. | `zeitlos gefasst` | wie Z. 2318 |
| 2375 | 2364 | Eintrag 41: Ersatzregel für den geheimgehaltenen Anteil 65+ (T-1199, Befunde 104 | `Log, Stand von damals` | Einleitung des Entscheidungslogs: Herkunft der Einträge mit Ticket und Befund, wie sie galten; kein heutiger Code-Stand |
| 2376 | 2365 | Stufe 2 neu gefasst in T-1233, Befunde 99, 117 und 119). Eintrag 42: Stichtag de | `Log, Stand von damals` | Einleitung des Entscheidungslogs: Herkunft der Einträge mit Ticket und Befund, wie sie galten; kein heutiger Code-Stand |
| 2377 | 2366 | Altersband in Ebene 1 (T-1233, Befunde 99 und 120). Eintrag 43: Schutzprogramme  | `Log, Stand von damals` | Einleitung des Entscheidungslogs: Herkunft der Einträge mit Ticket und Befund, wie sie galten; kein heutiger Code-Stand |
| 2378 | 2367 | gegenüber dem Katalogwert im Produkt (T-1295, Befunde 123 und 124; Zentralwert T | `Log, Stand von damals` | Einleitung des Entscheidungslogs: Herkunft der Einträge mit Ticket und Befund, wie sie galten; kein heutiger Code-Stand; „Katalogwert im Produkt“ nennt das Thema von Eintrag 43 |
| 2379 | 2368 | gegenüber der geparkten Maßnahme im Produkt (T-1329, Befund 130). Einträge 45–46 | `Log, Stand von damals` | Einleitung des Entscheidungslogs: Herkunft der Einträge mit Ticket und Befund, wie sie galten; kein heutiger Code-Stand; „geparkte Maßnahme im Produkt“ nennt das Thema von Eintrag 44, wie es damals hieß |
| 2380 | 2369 | \(h_{\text{Heim}}\) je Zelle, S157 im Anpassungspotenzial und öffentliche Kühlze | `Log, Stand von damals` | Einleitung des Entscheidungslogs: Herkunft der Einträge mit Ticket und Befund, wie sie galten; kein heutiger Code-Stand |
| 2382 | 2371 | Voreinstellung, Kappung 0,794 als eigener Parameter, Bänder von \(f_a\) und \(\b | `Log, Stand von damals` | Einleitung des Entscheidungslogs: Herkunft der Einträge mit Ticket und Befund, wie sie galten; kein heutiger Code-Stand |
| 2383 | 2372 | Eintrag 50: Bestand der Kalibrierjahre bei S157 (T-1584, Befund 165; Eintrag 45  | `Log, Stand von damals` | Einleitung des Entscheidungslogs: Herkunft der Einträge mit Ticket und Befund, wie sie galten; kein heutiger Code-Stand |
| 2384 | 2373 | um die Herleitung von \(\delta_{\text{HAP}}\) ergänzt (T-1584, Befund 164). Eint | `Log, Stand von damals` | Einleitung des Entscheidungslogs: Herkunft der Einträge mit Ticket und Befund, wie sie galten; kein heutiger Code-Stand |
| 2385 | 2374 | (T-1642-cmo): Streuung σ = 0,58 K und ein Faktor der Feinstruktur (Nr. 51, T-164 | `Log, Stand von damals` | Einleitung des Entscheidungslogs: Herkunft der Einträge mit Ticket und Befund, wie sie galten; kein heutiger Code-Stand |
| 2386 | 2375 | 52, T-1645, Befunde 180 und 194), \(\delta_{\text{KZ}}\) ungerundet und | `Log, Stand von damals` | Einleitung des Entscheidungslogs: Herkunft der Einträge mit Ticket und Befund, wie sie galten; kein heutiger Code-Stand |
| 2387 | 2376 | 53, T-1644, Befunde 178 und 179), \(a_{85+}\) je Kommune (Nr. 54, T-1646, | `Log, Stand von damals` | Einleitung des Entscheidungslogs: Herkunft der Einträge mit Ticket und Befund, wie sie galten; kein heutiger Code-Stand |
| 2403 | 2392 | (**Stand T-1584, 27.09.2026, Historie; für \(\delta_{\text{HAP}}\) fortgeschrieb | `Log, Stand von damals` | Log 10, Vermerk „Stand T-1584, Historie“ |
| 2413 | 2402 | 0,001/km mit \(\bar d\) aus Ebene bei Integration \| ±1,5 % entfällt; ehrlicher \| | `Log, Stand von damals` | Log 20, Wert der Alternative „bei Integration“, wie er damals galt; kein heutiger Code-Stand |
| 2423 | 2412 | Befund 62-Logik bleibt gültig, Umsetzung nun messungsbasiert \| — \| — \| | `Log, Stand von damals` | Log 30, „Umsetzung nun messungsbasiert“ meint die Methode (Bias gemessen) |
| 2432 | 2421 | gestrichen** (Stand T-1119, Historie; für Pflegeheime fortgeschrieben durch Nr.  | `Log, Stand von damals` | Log 39, Vermerk „Stand T-1119, Historie“ |
| 2433 | 2422 | Die Parameterliste im Produkt (P1) soll eine Setzung nie als Quellenwert zeigen; | `Log, Stand von damals` | Log 40, Anforderung an die Parameterliste (P1), wie entschieden |
| 2434 | 2423 | zweistufige Ersatzregel, Abschätzung von KAP3** (§3.3, festgelegt vom methodik_m | `Log, Stand von damals` | Log 41, festgelegt in T-1199 und T-1233 |
| 2435 | 2424 | 12411-09-01-4-B [48]; festgelegt vom methodik_manager in T-1233, Befund 99) \| Gl | `Log, Stand von damals` | Log 42, festgelegt in T-1233 |
| 2436 | 2425 | (**Stand T-1333, Historie; für das Zusammenwirken mit \(\delta_{\text{HAP}}\) fo | `Log, Stand von damals` | Log 43, Stand T-1333; „Der Katalog im Produkt setzt“ wird „setzte“, damit die Zeile keinen heutigen Code-Stand feststellt; die Meldung an den cto ist die damalige Entscheidung |
| 2437 | 2426 | 45, 46 und 53:** seit T-1367-cto ist die Maßnahme aktiv, \(s_{\text{gek}}\) hat  | `Log, Stand von damals` | Log 44, Kopfvermerk „seit T-1367-cto ist die Maßnahme aktiv“ (heutiger Code-Stand) umformuliert zu „die Maßnahme wirkt über s_gek mit der Voreinstellung 0,11“; die Entscheidung vom 26.09.2026 bleibt, wie sie galt |
| 2438 | 2427 | (**Stand T-1537, Historie; für das Anpassungspotenzial fortgeschrieben durch Nr. | `Log, Stand von damals` | Log 45, Vermerk „Stand T-1537, Historie“ |
| 2439 | 2428 | (**Stand T-1537, Historie; fortgeschrieben durch Nr. 53 und 51:** die Wahl gilt  | `Log, Stand von damals` | Log 46, Vermerk „Stand T-1537, Historie“ |
| 2440 | 2429 | € je Jahr; Unterschätzung für mehr als 90 % der Kommunen und Nullwirkung gegen P | `Log, Stand von damals` | Log 47, verworfene Alternative „Stand bis T-1538“; „das Produkt kann ihn nicht anwenden“ ist ihr Verwerfungsgrund |
| 2441 | 2430 | (**Stand T-1538, Historie; fortgeschrieben durch Nr. 52:** die Wahl gilt weiter; | `Log, Stand von damals` | Log 48, Vermerk „Stand T-1538, Historie“ |
| 2443 | 2432 | (**Stand T-1584, Historie; fortgeschrieben durch Nr. 51, 52 und 54:** die Wahl g | `Log, Stand von damals` | Log 50, Vermerk „Stand T-1584, Historie“ |
| 2444 | 2433 | σ = 0,58 K (Herleitung 2/√12 = 0,577 K, gerundet), ein Faktor: Zelllauf mit gege | `Log, Stand von damals` | Log 51, Entscheidung in T-1646 |
| 2445 | 2434 | \(\delta_{\text{HAP}}\) = 0,939 (Band 0,852–1,00) als Faktor auf den Exzess (RR− | `Log, Stand von damals` | Log 52, Entscheidung in T-1645; Alternative „Stand T-1584“ |
| 2446 | 2435 | \(g_{\text{S157}}\) = (0,93 × 1,11 − 1) / 0,11 = 0,2936, also \(1 - g_{\text{S15 | `Log, Stand von damals` | Log 53, Entscheidung in T-1644; Lesart aus T-1642-cmo als verworfene Alternative |
| 2447 | 2436 | \(a_{85+}\) je Kommune aus ihrem Zelllauf: YLL 85+ / alle YLL aus den Altersbänd | `Log, Stand von damals` | Log 54, Entscheidung in T-1646 |

## Ohne Treffer gefunden

Zeilen ohne Treffer von M, die beim Durchgang als Umsetzungsstand erkannt und ebenso behandelt wurden. Sie zählen nicht zu n.

| Zeile Basis | Satzanfang | Entscheidung | Begründung |
|---|---|---|---|
| 3 | Status: **Rev. 8, Fortschreibung 7 — ABNAHMEREIF** (A-0048; Null-Runde 48 über d | `zeitlos gefasst` | Prüfrunde im Statusblock („Null-Runde 48“); jetzt Verweis auf den Ledger |
| 9–10 | Rev. 8 vom 30.08.2026 (§3.4-Ressourcen-Regel, q_pfl-Ebene angelegt, q_1P geparkt | `zeitlos gefasst` | „q_pfl-Ebene angelegt“ (Stand des Produkts) wird „festgelegt“; „in den Ledger-Runden 10–48“ (Prüfrunde) entfällt |
| 477 | Ihre Zellen der Stufe 2 (3.893 Einwohner) rechnen wie heute mit 65+ = 0. | `zeitlos gefasst` | „wie heute“ (Stand des Codes) entfällt |
| 855–856 | **\(q_{\text{pfl}}\) — Ebene `CARE_HOME_SHARE_85P` („neu anzulegen"; wird von | `zeitlos gefasst` | „wird von /integriere-risiko angelegt“ (Umsetzungsereignis) wird „§3.1“; „neu anzulegen“ ist die Stufe der Datenebenen-Anlagepflicht nach §3.1 der Aufgabe |
| 2161–2162 | Diese Session erreicht web.archive.org nicht (Netz-Sandbox; Save-Versuch dokumen | `gestrichen` | Stand eines Arbeitslaufs, keine Regel |

## Befunde

Befund 223 (§5, Schutzprogramme) und Befund 224 (§7, Kennzeichnung `berechnet`) sind behoben. Befund 225 führt die Abweichung c_kal (Parameterliste zeigt `berechnet`, nicht Abschätzung), zurückgestellt bis 16.10.2026, zuständig cmo (T-1795-ceo) und danach cto. Alle drei in `reviews/BEFUNDE_95.md`.
