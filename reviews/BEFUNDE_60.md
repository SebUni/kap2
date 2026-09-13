# Befund-Ledger #60 — Schäden an Gebäuden aufgrund von Flusshochwasser

Angelegt 11.09.2026 mit dem Erstaufschlag `docs/methodik/60_gebaeudeschaeden_flusshochwasser.md`
(`/neu-risiko 60`). **Review-Runde 1 am 13.09.2026 gefahren** (T-0232, Messrunde — ohne Revision).
Befunde werden fortlaufend ab 1 nummeriert.
Pflege über `backend/scripts/ledger.py`. Ein Befund wird nur mit Prüfausdruck geschlossen (W7).
Zurückgestellte A-Befunde blockieren die Abnahme.

## Offene Befunde (4)

Kurzform; Art, Begründung und Vorschlag je Befund stehen in der Tabelle von
[Review-Runde 1](#review-runde-1) weiter unten.

| Nr | Befund (Stelle · Kurzfassung) | Kat. | Status | Umsetzungsnachweis | Prüfausdruck | Begründung bei Abweichung |
|---|---|---|---|---|---|---|
| 1 | Bericht Kap. 3 „Modell" Z. 146–185 · **Lücke** — Kapitel enthält außer einem HTML-Kommentar 0 Zeichen: keine Formel, keine Zeichentabelle, keine native Ergebnisgröße | A | behoben | Bericht Kap. 3, Abschnitte 3.1 „Native Ergebnisgröße, Einheit, Bezugsjahr, Betrachtungsebene" und 3.4 „Kernformel auf Zellebene": das Kapitel trägt jetzt 17.109 Zeichen außerhalb von HTML-Kommentaren, darunter die deklarierte native Ergebnisgröße EAD in €₂₀₂₆/a mit Bezugsjahr 2026 und Betrachtungsebene Kommune sowie die dreistufige Schicht-B-Kernformel Menge × Rate × Preis mit der physischen Zwischengröße „schadensäquivalente Wohnfläche" (m²) vor dem Euro-Betrag und einem lauffähigen Beispielblock `beispiel_60_kernformel_zelle`; die Schadensfunktion \(d(h)\) in Abschnitt 3.3 trägt Gültigkeitsbereich 0,10–1,75 m und konstante Deckelung auf 0,250 darüber (Absatz „Gültigkeitsbereich und Deckelung"), sodass keine Schadensquote über 100 % entstehen kann. | `python3 -c "import re;s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();k=s.split('\n## 3 ')[1].split('\n## 4 ')[0];raise SystemExit(0 if len(re.sub(r'<!--.*?-->','',k,flags=re.S).strip())>=8000 else 1)"` | Vorschlag in Runde 1 |
| 2 | Bericht Kap. 1 Knoten-Bilanz Z. 43–76 · **Lücke** — alle 32 Zeilen „rechnet in: offen"; kein Knoten verarbeitet oder begründet inaktiv | A | behoben | Bericht Kap. 1, Abschnitt „Knoten-Bilanz" (Tabelle direkt nach dem Absatz „Entscheidungsstand (T-0235)"): alle 32 Zeilen tragen jetzt eine benannte Formelstelle (FS-Hazard/FS-Exposition/FS-Schadensgrad/FS-Mengengerüst/FS-Schutzsystem/FS-Bestandsdynamik/FS-Vorsorge) oder `inaktiv` mit wörtlichem Zitat aus KWRA-Monetarisierung.xlsx (Blatt und Zelle genannt). | — | Vorschlag in Runde 1 |
| 3 | Bericht Kap. 2 Evidenz-Register Z. 111–144 · **Lücke** — 31 von 32 Zeilen in allen Spalten „offen", keine Zeile mit Entscheidung „Basiswert" | A | behoben | Bericht Kap. 2, Abschnitt „Evidenz-Register (§2.2)" (Registertabelle mit den Langbelegen B1–B6): die sieben tragenden Zeilen 60-W085-01, 60-R24-01, 60-S074-01, 60-R17-01, 60-S093-01, 60-S094-01 und 60-S092-01 tragen jetzt Effektgröße, Studientyp, volltextgeprüfte Quelle, Übertragbarkeit, Datenlage je Zelle und Entscheidung — zwei davon „Basiswert" (Hazard 60-W085-01, Mengengerüst 60-R24-01) —, während die übrigen 25 Zeilen weiterhin auf „offen" stehen. | — | Vorschlag in Runde 1 |
| 4 | Bericht Kap. 4 „Kalibrierung & Validierung" Z. 187–199 · **Lücke** — 0 Zeichen Substanz: kein Anker, kein Niveau-Skalar, keine Verteilungsprüfung, keine Toleranz | A | behoben | Bericht Kap. 4, Abschnitte 4.1 bis 4.8: das Kapitel trägt jetzt rund 18.700 Zeichen außerhalb von HTML-Kommentaren mit dem namentlichen nationalen Anker „GDV-Naturgefahrenstatistik, Teilreihe Starkregen/Überschwemmung" (Zeitreihe seit 2002, Revisionsstand Datenservice Naturgefahrenreport 2025 vom 10.10./30.12.2025, vorläufiges Jahr 2025 ausgeschlossen), dem Niveau-Skalar λ = 1,05 samt Rechenweg A\*/M₀ (§4.2–§4.4), der unabhängigen Verteilungsprüfung auf der Achse Ereignisregime mit vorab fixierter Toleranz ±15 Prozentpunkten gegen ein Ist von 4,6 Prozentpunkten (§4.5), dem Sanity-Band 0,56–2,26 Mrd. €₂₀₂₆/a mit Herleitung beider Grenzen (§4.6), der P1-Parametertabelle (§4.8) und dem ausdrücklichen Satz zur Auflösung (Bundesland-, Gemeindepunkt- und Stichprobenebene, kein nationaler 100-m-Vollraster-Lauf, §4.3). | `python3 -c "import re;s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();k=s.split('\n## 4 ')[1].split('\n## 5 ')[0];raise SystemExit(0 if len(re.sub(r'<!--.*?-->','',k,flags=re.S).strip())>=6000 else 1)"` | Vorschlag in Runde 1 |
| 5 | Bericht Kap. 3 Z. 160–165 (Absatz „(a) DATENEBENEN-ANLAGEPFLICHT") · **Lücke** — HQ-Wassertiefen und Gebäudewerte nur als Absichtserklärung im Kommentar, keine Ebene spezifiziert | A | behoben | Bericht Kap. 3, Abschnitt 3.2 „Datenebenen nach §3.1" (Ebenentabelle plus Absätze „Beschaffungs-Watchlist", „Ressourcen-Regel", „Kein-Doppelkanal"): die vier Ebenen HQ_FLAECHE, HQ_TIEFE, GEBAEUDEWERT (je **neu anzulegen**) und GEBAEUDEZUSTAND_BAUSTOFF (**geparkt (Datenquelle fehlt)** mit dreiteiliger Beschaffungs-Watchlist und Neutralwert 1,00) tragen jeweils Quelle, keyless Beschaffungsweg, Zell-Ableitungsregel, Fallback aus der Betrachtungsebene selbst und Normierung/Zentrierung, der HTML-Kommentar mit der Absichtserklärung ist entfallen; Abschnitt 3.3, Absatz „Abbildung der beiden Tiefenraster", bildet die LAWA-Klassen der Ebene HQ_TIEFE auf die metrische Tiefe der Schadensfunktion ab. | `python3 -c "s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();k=s.split('\n## 3 ')[1].split('\n## 4 ')[0];raise SystemExit(0 if all(t in k for t in ('HQ_FLAECHE','HQ_TIEFE','GEBAEUDEWERT','neu anzulegen','geparkt (Datenquelle fehlt)','Beschaffungs-Watchlist')) else 1)"` | Vorschlag in Runde 1 |
| 6 | Bericht Kap. 1 Weitergaben Z. 86 gegen `KWRA-Monetarisierung.xlsx` Blatt „Schadenskonten-System" Z29 · **Lücke** — K3-Buchungsobjekt #37 fehlt vollständig, #12 ohne Partitionsregel-Zitat | B | behoben | Bericht Kap. 1, Abschnitt „Weitergaben", Spalte „Konto-Ausschlüsse / verwandte Buchungen": #37 steht jetzt mit Kante 49 → 37 (Abgleich-Protokoll Punkt 3) und #12 steht jetzt mit R9-Partitionszitat (Rechenregeln Z11) in der Liste der Partitionsregel-Zitate. | — | Vorschlag in Runde 1 |
| 7 | Bericht §5.1 Z. 240–243 (Δq „marginal … Doppelzählungs-Wächter") gegen Kap. 4 · **Lücke** — Wächter ohne Kalibrierjahre nicht operationalisierbar | B | behoben | Bericht Kap. 4, Abschnitt 4.7 „Kalibrierjahre und Doppelzählungs-Wächter": die Kalibrierjahre 2002 bis 2024 sind einzeln benannt (2025 als vorläufig ausgeschlossen), Δq aus §5.1.2 zählt ausdrücklich nur Nachrüstungen nach dem letzten Kalibrierjahr 2024, und der heutige Objektschutz-Anteil q₀ ist mangels bundesweiter Statistik als „geparkt (Datenquelle fehlt)" mit dreiteiliger Beschaffungs-Watchlist ausgewiesen statt gesetzt — §5.1.2 verweist am Ende der Herleitung auf diese Bindung. | `python3 -c "s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();k=s.split('\n## 4 ')[1].split('\n## 5 ')[0];raise SystemExit(0 if all(t in k for t in ('2002','2024','geparkt (Datenquelle fehlt)','Doppelzählungs-Wächter')) else 1)"` | Vorschlag in Runde 1 |
| 8 | Bericht §5.1 Z. 221–222 (Formel EAD_mit) gegen §5.1.1 Z. 229–234 · **Lücke** — EAD und EAD_mit ohne Zeichentabellen-Zeile und ohne Herleitung | B | behoben | Bericht Kap. 3, neuer Abschnitt 3.5 „Zeichentabelle (alle Formelzeichen der Kapitel 3 und 5)" und Zeichentabelle §5.1.1 (jetzt erste zwei Zeilen): EAD und EAD_mit stehen mit Bedeutung, Einheit €₂₀₂₆/a, Bezugsjahr und Preisstand 2026, Betrachtungsebene Kommune und Herkunft (`herleitung:` §3.1/§3.4 Schritt 3 bzw. §5.1) in der Zeichentabelle, und die Tabelle in 3.5 führt alle 28 Formelzeichen der Kapitel 3 und 5 mit Bedeutung, Einheit und lint-fähiger Herkunft, sodass die Deckungslücke „4 von 6 Zeichen" entfällt. | `python3 -c "import re;s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();t=s.split('### 3.5 ')[1].split(chr(10)+'### ')[0];r=[[c.strip() for c in z.strip().strip(chr(124)).split(chr(124))] for z in t.split(chr(10)) if z.strip().startswith(chr(124))][2:];ok=all(len(c)==4 and (any(a in c[3] for a in ('register:','herleitung:')) or (c[3]=='Notation' and c[2]=='—')) for c in r);ead=[c for c in r if 'EAD' in c[0]];raise SystemExit(0 if ok and len(r)>=20 and any('2026' in c[1] and 'Kommune' in c[1] for c in ead) and any('mit' in c[0] for c in ead) else 1)"` | Vorschlag in Runde 1 |
| 9 | Bericht Z. 266–273 (Block `python test: beispiel_60_s092_abschaetzung`) gegen `backend/` · **Lücke** — Beispiel rechnet auf, ist aber nirgends als Golden-Test hinterlegt | B | behoben | Bericht Kap. 3, Abschnitt 3.6, Block `python test: beispiel_60_kernformel` (unmittelbar vor Abschnitt 3.7): die Kernformel aus 3.4 ist jetzt an einer Beispielzelle samt Aggregation auf eine Kommune aus zwei Zellen mit zehn `assert`-Zeilen ausführbar hinterlegt, und `beispiel_bloecke()` führt diesen wie die beiden übrigen Blöcke (`beispiel_60_kernformel_zelle`, `beispiel_60_s092_abschaetzung`) bei jedem Lauf von `python3 backend/scripts/lint_methodik.py 60` aus und verlangt je Block eine Zusicherung — Bericht und Rechnung können damit nicht mehr unbemerkt auseinanderlaufen. | `python3 -c "import re;s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();b=re.findall('python test: ([a-z0-9_]+)'+chr(10)+'(.*?)'+chr(10)+chr(96)*3,s,re.S);[exec(compile(c,n,'exec'),{}) for n,c in b];raise SystemExit(0 if b and all('assert' in c for n,c in b) and any(n=='beispiel_60_kernformel' for n,c in b) else 1)"` | Anders umgesetzt als vorgeschlagen: Das Einsammeln der Blöcke als Golden-Tests im Backend gehört zur Integration (P-N) und ist nicht Gegenstand dieses Berichtsschritts; die Ausführung aller Blöcke mit Zusicherungs-Pflicht leistet der bestehende Lint bereits. |
| 10 | Bericht §5.1.2 Z. 248–250 (s_bem = 0,50 „Mitte gesetzt") · **Fehler** — gesetzte Verteilungsannahme statt empirischer Quantile (§3.2 Tails, „messen statt setzen") | B | behoben | Bericht §5.1.2 (Aufzählungspunkt \(s_{\text{bem}}\)) und neuer Abschnitt 5.1.3 „\(s_{\text{bem}}\) — ausgewiesene Näherung mit Richtung" (Anker `#s-bem-naeherung`), gespiegelt in den Zeichentabellen §3.5 und §5.1.1 sowie im Parameter-Block `flood_bldg.s_bem` (Kap. 7, Felder `naeherung: true` und `naeherung_richtung: ueberschaetzt_hebel`): Der Satz „Ohne gemessene Tiefenverteilung wird die Mitte gesetzt" ist entfallen; 0,50 ist jetzt ausdrücklich als Näherung geführt — mit der aus der Szenario-Zerlegung §4.5 gerechneten harten Obergrenze 4,174/6,311 = 0,661 (Anteil unterhalb HQ100), der Richtungsangabe „überschätzt den Hebel \(r_{\text{S092}}\)" samt zweifacher Begründung (Bemessungsniveau privaten Objektschutzes deutlich unter HQ100; multiplikativ wachsendes \(d(h)\) gewichtet den Euro-Schaden zu den tiefen Ereignissen), dem Ersetzungspfad über die Ebene HQ_TIEFE auf **Stichproben** der HQ-Szenarien (Ressourcen-Regel §3.4, kein 100-m-Vollraster-Lauf) und dem ausführbaren Block `beispiel_60_s_bem_obergrenze`. Aus derselben Obergrenze folgt die Kappung der oberen Bandgrenze von \(s_{\text{bem}}\) von 0,70 auf **0,66** (§5.1.3, Absatz „Folge für das Band"): kein Bandende liegt mehr über der eigenen Herleitung; das abgeleitete Band von \(r_{\text{S092}}\) lautet damit 0,0075–0,1056 (−0,75 % bis −10,56 %) und ist an allen Fundstellen des Berichts nachgezogen. | `python3 -c "s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();k=s.split('### 5.1.3 ')[1].split(chr(10)+'## 6 ')[0];b=s.split('id: flood_bldg.s_bem')[1].split('---')[0];raise SystemExit(0 if all(t in k for t in ('Näherung','überschätzt','0,661','Stichproben')) and all(t in b for t in ('naeherung: true','naeherung_richtung: ueberschaetzt_hebel','herleitung_anker: \"#s-bem-naeherung\"')) else 1)"` | Anders umgesetzt als vorgeschlagen: Der zweite von T-0242 zugelassene Weg — empirische Bestimmung — ist nicht gangbar, solange die Ebene HQ_TIEFE den Stand „neu anzulegen" trägt (§3.2); deshalb der ausgewiesene Näherungscharakter mit Richtung statt einer Messung. |
| 11 | Bericht Kap. 8 Z. 336–351 · **Lücke** — keine einzige Quelle mit DOI/URL, Zugriffsdatum und Archiv-Snapshot (0 Treffer „http") | B | behoben | Bericht Kap. 8 „Quellen (§3.8)": alle drei Quellen tragen jetzt Vollzitat samt DOI/URL bzw. bei den beiden Arbeitsmappen Dateistand (Commit-Hash, Datum) und Prüfsumme (SHA-256), je mit Zugriffsdatum, und die Hochwasserschutzfibel (Quelle 3) ist mit Vollzitat, URL, Archiv-Snapshot und Zugriffsdatum wörtlich aus `backend/app/data/sources.py` übernommen, ohne diese Datei zu ändern. | — | Vorschlag in Runde 1 |
| 12 | Bericht Kap. 1 „Konto-Einbettung" Z. 90–100 · **Lücke** — kein Kostensatz, kein Preisstand; R5 (Versicherung = Transfer) nicht nachgezogen | B | behoben | Bericht Kap. 1, Abschnitt „Konto-Einbettung": neuer Punkt „Preisstandjahr (Abschätzung von KAP3, §3.9 ABGESCHÄTZT): 2026" und R5 ist im Punkt „Rechenregeln" jetzt als „übernommen" mit Herleitung (Konten Z26, Rechenregeln Z7, Mon. Z64) entschieden. | — | Vorschlag in Runde 1 |
| 13 | Bericht Kap. 1 Z. 35–36 gegen `backend/app/data/catalog.py` Z. 335–340 · **Fehler** — Behauptung „trägt genau die Namenslisten von W117" ist falsch (5 statt 7 Sensitivitäten, 5 statt 8 Wirkungs-Eingänge) | B | behoben | Bericht Kap. 1, Absatz „W-Knoten": die Behauptung ist auf den belegbaren Stand korrigiert (Code trägt nur eine Teilmenge mit abweichender Namensquelle, fünf statt sieben Sensitivitäten, fünf statt acht Wirkungs-Eingänge) und die Divergenz ist als Integrationspunkt für `/integriere-risiko 60` ins Entscheidungslog (Nr. 6) gezogen; `backend/app/data/catalog.py` bleibt dabei unverändert (eiserne Regel 5). | — | Vorschlag in Runde 1 |
| 14 | Bericht Kap. 6 Z. 275–284 · **Lücke** — 3 Zeichen Substanz; Infokasten-Texte fehlen, obwohl Kap. 1 Z. 102–103 sie ausdrücklich verlangt | B | behoben | Bericht Kap. 6 „Szenario-Anwendung & Modellgrenzen": das Kapitel trägt jetzt einen Absatz „Szenario-Anwendung 60-A" (verschobene Größe FS-Hazard, konstant gehaltene Größen, zwei Stationaritätsannahmen, Behandlung der Bestandsdynamik S104), eine nummerierte Modellgrenzen-Liste (darunter Punkt 1 die Untergrenzen-Aussage K1/K4/K5/K8 nicht enthalten und Punkt 2 die Bauform-Grenze der P2-Abschätzung 60-S094-01) sowie die drei wörtlichen Infokasten-Texte (Benennung „bewerteter Schaden — Konto K3", Vollständigkeitsanzeige „Stufe M0: 1 von 8 Konten aktiv", Versionsstempel „berechnet mit Modellstand M0 — Untergrenze"). | `python3 -c "import re;s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();k=s.split('\n## 6 ')[1].split('\n## 7 ')[0];raise SystemExit(0 if len(re.sub(r'<!--.*?-->','',k,flags=re.S).strip())>=2500 else 1)"` | Vorschlag in Runde 1 |
| 15 | Bericht Kap. 7 Z. 290–334 · **Lücke/Widerspruch** — „Abschätzung von KAP3" nur als YAML-Kommentar (P1); `endpunkt`/`bandzuordnung` außerhalb des in §4 definierten Wertebereichs | B | behoben | Bericht Kap. 7 (Absatz „Kennzeichnung nach Vorgabe P1 — im Block, nicht im Kommentar", die vier YAML-Blöcke und neuer Abschnitt 7.1 „Antrag auf Fortschreibung des §4-Wertebereichs für die Familie K3/K4-Ereignisschäden", Anker `#fortschreibung-endpunkt-k3`): Die YAML-Kommentare sind durch die maschinenlesbaren Felder `kennzeichnung: abschaetzung_kap3`, `herleitung_anker:` (auf die Anker `#s092-wirkung` bzw. `#s-bem-naeherung` im sichtbaren Berichtstext, die als `<a id=…>` gesetzt sind) und `wertebereich_abweichung: "#fortschreibung-endpunkt-k3"` ersetzt, sodass die P1-Kennzeichnung im Block selbst steht, und die Überschreitung des §4-Wertebereichs durch `endpunkt: K3-Wiederherstellung` und `bandzuordnung: [alle]` ist in §7.1 mit Begründung (Konten Z28; `mortalitaet`/`morbiditaet` sachlich falsch, `beide` irreführend wegen #101/K1; Hebel ohne Bandachse) und Datum 13.09.2026 als Antrag auf Fortschreibung der Aufgabe ausgewiesen statt still überstimmt. | `python3 -c "import re;s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();k=s.split(chr(10)+'## 7 ')[1].split(chr(10)+'## 8 ')[0];bl=re.split(r'^parameter:$',k,flags=re.M)[1:];kz=[re.search(r'^  kennzeichnung: (\S+)$',b,re.M) for b in bl];ok=all(m and m.group(1) in ('quelle','abschaetzung_kap3') for m in kz) and all(re.search(r'^  herleitung_anker: \"#\S+\"$',b,re.M) and re.search(r'^  wertebereich_abweichung: \"#fortschreibung-endpunkt-k3\"$',b,re.M) for b in bl);ank=all(('<a id=\"'+a+'\">') in s for a in ('s092-wirkung','s-bem-naeherung','fortschreibung-endpunkt-k3'));raise SystemExit(0 if len(bl)==4 and ok and ank and '13.09.2026' in k.split('### 7.1 ')[1] else 1)"` | Anders umgesetzt als vorgeschlagen: Die Wertebereichs-Überschreitung wird nicht durch Umbiegen der Felder geheilt (jeder zugelassene Wert wäre sachlich falsch), sondern als Antrag auf Fortschreibung geführt — Entscheidung über die Aufgabe trifft dieser Bericht nicht; die Aufnahme der Felder in Lint/Registry gehört T-0234 bzw. P-N. |
| 16 | Bericht Kap. 9 Z. 366–374 · **Lücke** — Ansatz-Vergleich vollständig „offen", obwohl §2.6 ihn für den ersten Familienvertreter zwingend verlangt | B | behoben | Bericht Kap. 9 „Ansatz-Vergleich", Abschnitte „Die drei verglichenen Ansätze", „Kriterienraster" und „Umsetzungsgrundlage": die drei Ansätze (a) typisierte Tiefen-Schadensfunktion je 100-m-Zelle, (b) aggregierte Flächenschadensrate und (c) Schadensgradmodell D0–D6 am Einzelgebäude sind benannt, jede der 21 Rasterzellen ist bewertet, und Ansatz (a) ist mit Begründung gegen (b) und (c) als Umsetzungsgrundlage festgelegt — nachgezogen in der Kopfzeile (Z. 3–5) und im Entscheidungslog Nr. 5 (13.09.2026). | — | Vorschlag in Runde 1 |
| 17 | `backend/scripts/lint_methodik.py` gegen Bericht Kap. 3/4/6 · **Lücke** — 83 grüne Checks bei drei substanzlosen Kapiteln; kein Vollständigkeits-Check der Pflichtkapitel | C | offen | — | — | Vorschlag in Runde 1 |
| 18 | Bericht Entscheidungslog Nr. 3 Z. 382 und Kap. 7 gegen Register-Zeile 60-S092-01 Z. 135 · **Widerspruch** — vier bezifferte Parameter-Blöcke aus einer Registerzeile mit Entscheidung „offen" | C | behoben | Bericht Kap. 2, Abschnitt „Evidenz-Register (§2.2)", Zeile 60-S092-01: die Spalte „Entscheidung" trägt jetzt „Maßnahmen-Hebel (abgeschätzt)" statt „offen (Vorschlag: Maßnahmen-Hebel, abgeschätzt)", sodass die Parameter-Blöcke in Kap. 7 aus einer entschiedenen Zeile im Sinne von §2.2 ableiten, während die Kennzeichnung §3.9 ABGESCHÄTZT und die Modellgrenze „kommunal (Pauschalfaktor)" nach Vorgabe P2 in der Zeile stehen bleiben (Kopf-Geltungsbereich und Kap. 2 sind entsprechend nachgezogen). | — | Vorschlag in Runde 1 |
| 19 | `docs/evidenz/register.md` Z. 65 (Zeile 60-S092-01) gegen Bericht §5.1.2/Kap. 7 · **Widerspruch** — das risikoübergreifende Evidenz-Register führt für 60-S092-01 weiterhin das alte Band 0,0075–0,112, während der Bericht nach der Kappung von `s_bem` auf ≤0,66 (§5.1.3, Absatz „Folge für das Band") 0,0075–0,1056 ausweist; kein Lint liest diese Datei, die Divergenz fiele also nirgends auf (eiserne Regel 5: nie still im Code lösen) | C | offen | — | — | Rest aus T-0242: Nachzug auf 0,0075–0,1056 gehört in ein eigenes Ticket, weil T-0242 Abnahmekriterium (e) jede Datei außer dem Bericht #60 und diesem Ledger sperrt. Aufgenommen 13.09.2026. |

## Review-Runde 1

**Datum: 13.09.2026** · unabhängige Gegenprüfung nach §5, frische Session (Eiserne Regel 4: der
Bericht entstand am 11.09.2026 in der Sitzung zu T-0167, diese Session hat ihn nicht geschrieben)
· Prüfgegenstand: `docs/methodik/60_gebaeudeschaeden_flusshochwasser.md`, Stand Erstaufschlag
(Zeilennummern beziehen sich auf diesen Stand) · Maßstab: §3 und §5 von
`docs/AUFGABE_METHODIK_SCHADENSRECHNUNG.md`, **nicht** der Berichtstext · Anlass: T-0232
(**Messrunde** — es wird kein Befund behoben, keine Revision gefahren, kein Export erzeugt).

**Bundle-Vorbedingung (§5, Schritt 0):** vollständig — Bericht, Aufgabe, beide Arbeitsmappen
(`docs/Schadensbaum/KWRA-Schadensbaum_X_UBA-klimawirkungsketten.xlsx`,
`docs/Schadensbaum/KWRA-Monetarisierung.xlsx`), Spiegelung `docs/evidenz/register.md` (32 Zeilen
`60-…`, per `grep -c "^| 60-"` gezählt) und dieses Ledger lagen ab dem ersten Turn vor. Der Bericht
verweist auf keine weiteren Anlagen (Skripte/CSVs): Kap. 4 ist leer.

### 1 · Deterministische Lints

Ausgabe von `python3 backend/scripts/lint_methodik.py 60`, wörtlich:

```
=== #60 · 60_gebaeudeschaeden_flusshochwasser.md ===
  83 Checks grün
  Historie-Marker: 0 markierte Zeilen (Ratchet None), 0 gedeckte Fundstellen abgelöster Werte:

ALLE LINTS GRÜN
```

**Grüne Checks: 83. Rote Checks: 0.** (Exit-Status 0.) Die Lints sind damit grün — sie decken den
Erstaufschlag aber nur dort ab, wo er Text trägt; siehe Befund 17.

### 2 · Leitfragen 1–14 (§5) — einzeln mit Verdikt und Fundstelle

**Nachgerechnet statt gelesen wurden sieben Leitfragen: 1, 4, 7, 10, 11, 13 und 14.** Der
Prüfausdruck bzw. der Rechenweg mit Zahlen steht jeweils direkt bei der Leitfrage; alle Ausdrücke
sind gegen die Arbeitsmappen unter `docs/Schadensbaum/` bzw. gegen die angegebene Quelle gefahren
worden (openpyxl, Repo-Wurzel als Arbeitsverzeichnis).

**LF 1 — Kette (nachgerechnet).** Verdikt: **Befund** (→ Befunde 1, 2).
Fundstelle: Bericht Kap. 1 Knoten-Bilanz Z. 43–76 gegen
`KWRA-Schadensbaum_X_UBA-klimawirkungsketten.xlsx`, Blatt „Klimawirkungsketten" Z272 (W117) und
Z208 (W085). Prüfausdruck:

```bash
python3 -c "
import openpyxl
wb=openpyxl.load_workbook('docs/Schadensbaum/KWRA-Schadensbaum_X_UBA-klimawirkungsketten.xlsx',read_only=True,data_only=True)
rows=list(wb['Klimawirkungsketten'].iter_rows(values_only=True))
cite={13:'E12',8:'E07',9:'E08',197:'S072',198:'S073',199:'S074',204:'R17',205:'R18',206:'R19',11:'E10',18:'E17',15:'E14',3:'E02',4:'E03',181:'W074',184:'W077',210:'W087',45:'W008',43:'W006',214:'W091',223:'W100',256:'S092',257:'S093',258:'S094',260:'S096',261:'S097',262:'S098',268:'S104',270:'R24',269:'R23',271:'R25',226:'W103',272:'W117',208:'W085'}
bad=[(r,k,rows[r-1][0]) for r,k in sorted(cite.items()) if rows[r-1][0]!=k]
print('Zeilen-Abweichungen:',bad)
"
```

Ergebnis: `Zeilen-Abweichungen: []` — **alle 34 im Bericht genannten Blattzeilen treffen den
behaupteten Knoten.** Die Mengenrechnung geht ebenfalls auf: W117 Z272 führt 6 Einflüsse
(E10; E08; E17; E14; E02; E03), 7 Sensitivitäten, 3 räumliche und 8 Wirkungs-Eingänge = 24
Eingänge; W085 Z208 führt E12; E07; E08 · S072; S073; S074 · R17; R18; R19 = 9, davon E08 schon
enthalten ⇒ 24 + 8 = **32** = Zeilenzahl der Bilanz und der Register-Spiegelung. Der Befund liegt
nicht in der Vollständigkeit, sondern in der **Verarbeitung**: In der Spalte „rechnet in" steht
32 mal `offen`; kein Knoten ist verarbeitet und keiner begründet inaktiv (die Spalte „Vorschlag"
erklärt der Bericht Z. 40–41 selbst ausdrücklich zur Nicht-Entscheidung). Kap. 3 enthält keine
Formel, in der ein Eingang rechnen könnte.

**LF 2 — Verteilschlüssel-Test.** Verdikt: **Befund** (→ Befunde 1, 2, 5).
Fundstelle: Bericht Kap. 1 Z. 52 (R17: „Lackmustest §3.1: keine Flussaue → ~0") und Kap. 3
Z. 157 („Lackmustest §3.1: Kommune ohne Flussaue/Überflutungsfläche → ~0", im HTML-Kommentar).
Der Test ist an beiden Stellen als Absicht benannt, aber nirgends geführt: Ohne Formel und ohne
spezifizierte Expositionsebene ist nicht entscheidbar, ob eine Kommune ohne Treiber > 0 erhalten
kann. Ein Verteilschlüssel ist zwar nirgends gesetzt (der Negativ-Fall „nationaler Schadenstopf ×
Anteil" ist Kap. 9 Z. 362–363 ausgeschieden) — bestanden ist die Frage damit aber nicht, sondern
unentscheidbar.

**LF 3 — Physische Zwischengröße.** Verdikt: **Befund** (→ Befund 1).
Fundstelle: Bericht Kap. 3 Z. 146–185. Das Kapitel nennt die Pflicht („physische Zwischengröße vor
dem Euro", Z. 153) im Kommentar; es gibt weder einen Euro-Pfad noch eine Zwischengröße, also auch
keine Rückführbarkeit. Die native Ergebnisgröße ist Z. 151 ausdrücklich „Entscheidung offen",
obwohl §3.6 genau eine deklarierte native Ergebnisgröße je Risiko-Code verlangt.

**LF 4 — Doppelzählung (nachgerechnet).** Verdikt: **Befund** (→ Befunde 6, 7).
Fundstelle: Bericht Kap. 1 Weitergaben-Zelle Z. 86 gegen `KWRA-Monetarisierung.xlsx`, Blatt
„Schadenskonten-System" Z29 und Blatt „Abgleich-Protokoll". Prüfausdruck:

```bash
python3 -c "
import openpyxl
wb=openpyxl.load_workbook('docs/Schadensbaum/KWRA-Monetarisierung.xlsx',read_only=True,data_only=True)
k=list(wb['Schadenskonten-System'].iter_rows(values_only=True))
print('K3-Buchungsobjekte:',k[28][2])
ap=list(wb['Abgleich-Protokoll'].iter_rows(values_only=True))
print([ (r[0],r[1],r[3]) for r in ap if str(r[1])=='49' ])
"
```

Ergebnis: Konten Z29 führt **sieben** K3-Buchungsobjekte — 12, 37, 46, 59, **60**, 92, 102. Der
Bericht behandelt 46 und 59 mit Partitionszitat, 92, 102 und 55 als „ohne Partitionsregel (offen)",
12 nur als Bilanzzeile ohne Regelzitat — und **37 „Schäden an Aquakulturen" überhaupt nicht**,
obwohl das Abgleich-Protokoll Punkt 3 die Kante 49 → 37 führt (Mon. Z54 bestätigt: „→ 60, 74, 50,
101; [Abgleich] → 10, 37, …") und Mon. Z42 für #37 „Sachschäden an Anlagen (K3)" bucht. Damit
teilen sich zwei Objekte ein Konto und denselben Treiber ohne R9-Partition. Zweitens ist der von
§3.5 verlangte Doppelzählungs-Wächter für S092 (Bericht Z. 240–243: „marginal, weil vorhandener
Objektschutz bereits im Basisschaden steckt") nicht prüfbar, weil es keine Kalibrierjahre gibt
(Kap. 4 leer) — die Marginalität ist behauptet, nicht gesichert. Positiv geprüft: Der Bericht
behauptet Z. 86, das Abgleich-Protokoll führe keinen Punkt mit Quelle oder Ziel 60 — das trifft zu
(Volltextsuche über alle 152 Zeilen des Blattes liefert nur einen Treffer „160.800" in Punkt 52),
und NW Z61 hat tatsächlich keine Output-ID.

**LF 5 — Modifikatoren.** Verdikt: **Befund** (→ Befund 3).
Fundstelle: Bericht Kap. 2 Z. 113–144. 31 von 32 Registerzeilen tragen in Effektgröße, Studientyp,
Quelle, Übertragbarkeit und Datenlage durchgängig „offen"; keine Zeile trägt die Entscheidung
„Basiswert". Zentrierung, OR-Übersetzung, Band- und Endpunktzuordnung sind deshalb nicht prüfbar —
es gibt keinen einzigen Modifikator. Der einzige bezifferte Faktor (60-S092-01, Z. 135) ist ein
Maßnahmen-Hebel und wirkt multiplikativ auf den Erwartungsschaden (Z. 221–222), ist also
zulässigerweise nicht zentriert; §3.2 „Alle Modifikatoren mittelwertzentriert" ist auf ihn nicht
anwendbar. Der Befund ist das leere Register, nicht eine falsche Zentrierung.

**LF 6 — Struktur.** Verdikt: **Befund** (→ Befund 3).
Fundstelle: Bericht Kap. 2 Z. 136–137 (60-S093-01 „Gebäudezustand → Schadensgrad" und 60-S094-01
„Baumaterialien → Schadensgrad", beide „offen") gegen Mon. Z65 („Schadensfunktionen
(Wassertiefe-Schaden) × Gebäudewerte") und Konten Z27 („Schadensfunktionen × Bestandswerte").
Wassertiefe-Schaden-Funktionen sind nach Bauart und Nutzung strukturabhängig; der Bericht führt
keine Struktur-/Bandachse und auch keine explizite Annahme „gleiche relative Elastizität über alle
Bänder". Kopplungen zwischen abgeleiteten Parametern bestehen bisher nur innerhalb der
S092-Kette (dort korrekt benannt, Z. 233).

**LF 7 — Tails/Parameter (nachgerechnet).** Verdikt: **Befund** (→ Befund 10).
Fundstelle: Bericht §5.1.2 Z. 248–250 und §5.1 Z. 255–258. Rechenweg der Nachrechnung (die Kette
selbst geht auf): Δq · s_bem · e_bem = 0,10 · 0,50 · 0,70 = **0,035** ✓; Band
0,05 · 0,30 · 0,50 = **0,0075** bis 0,20 · 0,70 · 0,80 = **0,112** ✓; Einzelachsen
Δq ⇒ 0,0175–0,0700 (Spannweite 0,0525), s_bem ⇒ 0,0210–0,0490 (0,0280),
e_bem ⇒ 0,0250–0,0400 (0,0150) — die Behauptung „Δq größte Achse" und „Elastizität 1 je Faktor"
ist bestätigt. Der Befund liegt im **Zustandekommen** von s_bem: Der Bericht setzt ihn
(„Ohne gemessene Tiefenverteilung wird die Mitte gesetzt, Band symmetrisch", Z. 250), obwohl er
genau die Größe ist, die §3.2 als empirisches Quantil verlangt („wo wenige Extremereignisse den
Effekt tragen, empirische Quantile aus der Klimatologie statt Verteilungsannahmen") und die aus
den HQ-Szenarien stammt, die Mon. Z65 ohnehin zur Bewertungsgrundlage macht. Dass der Bericht den
Ersetzungspfad dokumentiert (Z. 261–262), macht die Setzung nicht zur zulässigen Abschätzung nach
§3.9 („nur wenn keine Quelle existiert"). Kalibriermodell = Produktionsmodell ist mangels Kap. 4
nicht prüfbar (→ Befund 4).

**LF 8 — Kalibrierung.** Verdikt: **Befund** (→ Befund 4).
Fundstelle: Bericht Kap. 4 Z. 187–199. Substanz außerhalb des HTML-Kommentars: 0 Zeichen. Es fehlen
der nationale Anker samt Zeitreihe und Revisionsstand, der eine Niveau-Skalar, die unabhängige
Verteilungsprüfung auf der bei Flut kritischsten Achse (Ereignisregime) mit vorab fixierter
Toleranz und Ist-Ergebnis, die Holdout-Regel und die Sanity-Bänder mit Unter- und Obergrenze.
Immerhin wird die Ressourcen-Regel §3.4 nicht verletzt: Ein nationaler 100-m-Vollraster-Lauf ist
nirgends geplant (Z. 196–198 nennt ausdrücklich die zulässigen Auflösungen).

**LF 9 — Kostensätze.** Verdikt: **Befund** (→ Befund 12).
Fundstelle: Bericht Kap. 1 „Konto-Einbettung" Z. 90–100 und Kap. 7 Z. 290–334. Konten Z27 verlangt
für K3 „Wiederherstellungs-/Zeitwertkosten; Schadensfunktionen × Bestandswerte"; der Bericht führt
keinen einzigen Kostensatz und damit auch keinen Preisstand (alle vier Parameter-Blöcke tragen
`preisstand: null`, was für dimensionslose Faktoren korrekt ist). Damit ist die Preisstand-
Einheitlichkeit §3.3 gegenstandslos, aber die Konten-Disziplin unvollständig: R5
(„Versicherungsleistungen sind Transfers", Mon. Z64 für #59, das der Bewertungsansatz Mon. Z65 mit
„Wie ID 59" übernimmt) steht nicht in der Regelspalte von Mon. Z65 („R7, R9") und ist im Bericht
nur als offener Punkt vermerkt (Z. 99–100), nicht entschieden. VSL/VOLY betrifft #60 nicht (K1
läuft über #101, Mon. Z106).

**LF 10 — Quellen (nachgerechnet).** Verdikt: **Befund** (→ Befund 11).
Fundstelle: Bericht Kap. 8 Z. 336–351. Prüfausdruck:
`grep -c "http" docs/methodik/60_gebaeudeschaeden_flusshochwasser.md` → **0**;
`grep -n "Zugriff\|Snapshot\|DOI" …` → genau ein Treffer, Z. 350, und der steht im HTML-Kommentar
als Formatvorlage. §3.8 verlangt je Quelle Autor, Jahr, Titel, Organ, DOI/URL, Zugriffsdatum und
Archiv-Snapshot; die drei Einträge tragen davon keinen einzigen vollständig. Gegenprobe an der
angegebenen Quelle: Der in Z. 346–348 genannte Code-Eintrag existiert und trägt genau die Angaben,
die dem Bericht fehlen (`backend/app/data/sources.py` Z. 144–153: BMWSB 2022, URL,
„[Zugriff: 4. Juli 2026]", `archive_url`) — die Angaben sind also vorhanden, aber nicht in die
Berichtsquelle gezogen.

**LF 11 — Form (nachgerechnet).** Verdikt: **Befund** (→ Befunde 8, 9).
Fundstelle: Bericht Z. 266–273 (Beispielblock) und §5.1.1 Z. 229–234 (Zeichentabelle).
Prüfausdrücke:

```bash
python3 -c "
dq,s,e=0.10,0.50,0.70
assert abs(dq*s*e-0.035)<1e-12
assert abs(0.05*0.30*0.50-0.0075)<1e-12 and abs(0.20*0.70*0.80-0.112)<1e-12
print('Beispielblock rechnet auf')
"
grep -rn "beispiel_60" --include=*.py backend | wc -l
```

Ergebnis: „Beispielblock rechnet auf" — und `0` Treffer im Code. §3.2 verlangt „jedes Beispiel wird
als **ausführbarer Golden-Test** hinterlegt (§7)"; der Block ist im Bericht als
```` ```python test: beispiel_60_s092_abschaetzung ```` markiert, aber nirgends in `backend/`
hinterlegt — Bericht und Code können auseinanderlaufen, ohne dass die CI es merkt. Zweiter Formfund:
Die Zeichentabelle §5.1.1 ist alphabetisch sortiert und vollständig (Zeichen · Name · Einheit ·
Wert/Herkunft) für Δq, e_bem, r_S092, s_bem — sie deckt aber die zweite Formel des Kapitels nicht
ab (→ LF 13).

**LF 12 — Umsetzbarkeit.** Verdikt: **Befund** (→ Befunde 5, 15, 16).
Fundstelle: Bericht Kap. 3 Z. 160–165, Kap. 7 Z. 290–334, Kap. 9 Z. 366–374. (a) Die beiden
benötigten Zellgrößen — HQ-Überflutungsflächen/Wassertiefen und Gebäudebestandswerte — sind
namentlich benannt, aber weder als Ebene spezifiziert (Quelle, keyless Beschaffungsweg,
Zell-Ableitungsregel, Fallback, Normierung) noch „neu anzulegen" bzw. „geparkt" gekennzeichnet; der
Satz steht im Futur und im HTML-Kommentar. §3.1 lässt genau das nicht zu. (b) Die vier
Parameter-Blöcke sind formal vollständig, tragen den P2-Hinweis aber nur als YAML-Kommentar
(`# Abschätzung von KAP3 (P1/P2)`) — P1 verlangt ausdrücklich mehr als einen Code-Kommentar; zudem
liegen `endpunkt: K3-Wiederherstellung` und `bandzuordnung: [alle]` außerhalb des in §4 definierten
Wertebereichs (`mortalitaet | morbiditaet | beide`), ohne dass die Aufgabe dafür fortgeschrieben
wäre. (c) Der nach §2.6 für den ersten Familienvertreter verbindliche Ansatz-Vergleich ist ein
7 × 3-Raster aus „offen"; damit ist auch die Umsetzungsgrundlage offen (Kopf Z. 4).

**LF 13 — Herleitungspflicht (nachgerechnet).** Verdikt: **Befund** (→ Befund 8).
Fundstelle: Bericht §5.1 Z. 221–222 gegen §5.1.1 Z. 229–234. Rechenweg der Deckungsprüfung: Der
Bericht führt zwei Formeln — (i) EAD_mit = EAD · (1 − r_S092) und (ii) r_S092 = Δq · s_bem · e_bem.
Formelzeichen insgesamt: EAD, EAD_mit, r_S092, Δq, s_bem, e_bem = **6**; Zeilen in der einzigen
Zeichentabelle: **4** (Δq, e_bem, r_S092, s_bem). Deckungslücke = **2 von 6** — für EAD und
EAD_mit gibt es weder eine Tabellenzeile (Einheit! Euro je Jahr, Bezugsjahr, Betrachtungsebene)
noch eine Herleitung; §3.2 verlangt „je Formel eine alphabetisch sortierte Formelzeichen-Tabelle",
§3.9 „ein einziges Formelzeichen ohne abgeschlossene Herleitung = Befund". Positiv: Die vier
tabellierten Zeichen sind vollständig hergeleitet (Z. 238–253), als „Abgeschätzt" nach §3.9
gekennzeichnet und mit Bandbreite und Ergebnis-Sensitivität versehen.

**LF 14 — Quellen-Synchronität (nachgerechnet).** Verdikt: **Befund** (→ Befund 13).
Fundstelle: Bericht Kap. 1 Z. 35–36 („Der Code-Bestand … trägt genau die Namenslisten von W117")
gegen `backend/app/data/catalog.py` Z. 335–340 und KWK Z272. Prüfausdruck:

```bash
python3 -c "
import openpyxl
wb=openpyxl.load_workbook('docs/Schadensbaum/KWRA-Schadensbaum_X_UBA-klimawirkungsketten.xlsx',read_only=True,data_only=True)
w=list(wb['Klimawirkungsketten'].iter_rows(values_only=True))[271]
print('Mappe: sens',len(w[9].split(';')),'| wirkung',len(w[11].split(';')))
"
```

Ergebnis: Mappe `sens 7 | wirkung 8`; `catalog.py` führt für `kwra_id: 60` **5**
`sensitivity_names` (es fehlen „Bauliche, organisatorische und finanzielle Vorsorge der
öffentlichen Hand" = S096 und „Verwendete Baumaterialien von (Schutz-)Infrastrukturen" = S098) und
**5** `upstream_names`, die zudem aus der Wirkungs-**Labelliste** stammen („Abfluss und Wasserstand
von Oberflächengewässern", „Gravitative Massenbewegungen") statt aus `Input_Namen_Wirkung`
(„Hochwasser", „Sturzfluten", „Bergsturz, Felssturz, Steinschlag", „Rutschungen und Muren",
„Meeresspiegelhöhe"). Die Berichtsbehauptung „**genau** die Namenslisten von W117" ist damit
widerlegt; sie stützt im Entscheidungslog Nr. 1 (Z. 380) die Wahl des Umschnitts. Nach Eiserner
Regel 5 wird die Divergenz hier verbucht und **nicht** im Code gefixt. Gegen die Arbeitsmappen
selbst ist kein Widerspruch gefunden worden: Alle 34 geprüften Blatt-/Zellbezüge treffen zu
(LF 1), die Zitate aus Konten Z26/Z27/Z28, Rechenregeln Z9 (R7), Z11 (R9) und Z20 (A5) sowie
Mon. Z51/Z54/Z55/Z56/Z64/Z65/Z106 stimmen wörtlich, und die Abgleich-Punkte 5, 15, 16 existieren
mit dem behaupteten Inhalt. Eine bewusste Fortschreibung einer Arbeitsmappe nimmt der Bericht
nicht vor; der offene Punkt R5 (Z. 99–100) ist korrekt als offen und nicht als Überstimmung
geführt.

### 3 · Befunde dieser Runde (1–18)

Format §5: Stelle · Art (Lücke/Fehler/Widerspruch) · Begründung · Vorschlag · Kategorie.
Alle Befunde stehen auf `offen`; diese Runde behebt ausdrücklich keinen (T-0232).

| Nr | Kat. | Befund (Stelle · Art · Begründung · Vorschlag) | Prüfausdruck | Status |
|---|---|---|---|---|
| 1 | A | Bericht Kap. 3 „Modell" Z. 146–185 · **Lücke (§2.3, §3.2, §3.6; LF 1/3/11)** — außerhalb des HTML-Kommentars 0 Zeichen: keine Schicht-B-Formel, keine Zeichentabelle, keine deklarierte native Ergebnisgröße, kein Schicht-A-Index. Ohne Modell sind LF 2, 3, 5, 6, 7 und 11 nur negativ beantwortbar. **Vorschlag:** Kernformel Menge × Rate × Preis auf Zellebene ausschreiben (Erwartungsschaden K3/Jahr = Σ_Szenarien p · Schadensgrad(Wassertiefe) · Gebäudewert), physische Zwischengröße „betroffene Gebäude/Wassertiefe" vor dem Euro, native Ergebnisgröße deklarieren. **Umsetzungsnachweis:** Bericht Kap. 3, Abschnitte 3.1 und 3.4: native Ergebnisgröße EAD in €₂₀₂₆/a (Bezugsjahr 2026, Betrachtungsebene Kommune) deklariert und die Kernformel Menge × Rate × Preis je 100-m-Zelle ausgeschrieben — geschädigte Wohnfläche als physische Zwischengröße, Szenario-Erwartungswert über die HQ-Stützstellen, Euro erst im dritten Schritt. Zeichentabelle, Aggregation und Schicht A sind nicht Gegenstand dieses Umsetzungsschritts (T-0238, Teil 1 von Kapitel 3). | `python3 -c "import re;s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();k=s.split('\n## 3 ')[1].split('\n## 4 ')[0];raise SystemExit(0 if len(re.sub(r'<!--.*?-->','',k,flags=re.S).strip())>=8000 else 1)"` | behoben |
| 2 | A | Bericht Kap. 1 Knoten-Bilanz Z. 43–76 · **Lücke (§2.1, §5 LF 1)** — 32 von 32 Zeilen tragen „rechnet in: offen"; die Spalte „Vorschlag" ist laut Z. 40–41 ausdrücklich keine Entscheidung. §2.1 verlangt je Knoten „verarbeitet **oder** begründet inaktiv". **Vorschlag:** je Zeile entscheiden; die zwölf voraussichtlich inaktiven Knoten (E10, E17, E14, E02, E03, W074, W077, W087, W008, W006, W100, R18, R19, R23, R25) mit Regelzitat (R9/Konten Z28) auf „inaktiv" setzen, die übrigen an eine Formelstelle binden. | — | offen |
| 3 | A | Bericht Kap. 2 Z. 113–144 · **Lücke (§2.2 „Herzstück des Berichts", §3.2 Sensitivitäten nur über das Register; LF 5/6)** — 31 von 32 Zeilen sind in allen sechs Sachspalten „offen", keine Zeile trägt Entscheidung „Basiswert". Ohne belegte Effektgröße kann keine Formel entstehen; strukturabhängige Evidenz (Schadensfunktion nach Bauart/Nutzung, S093/S094) ist nicht erhoben. **Vorschlag:** zuerst die vier tragenden Zeilen füllen (W085 Hazard, R24 Mengengerüst, S074/R17 Exposition, S093/S094 Schadensgrad) und erst danach Kap. 3 schreiben. **Umsetzungsnachweis:** Bericht Kap. 2, Abschnitt „Evidenz-Register (§2.2)" (Registertabelle mit den Langbelegen B1–B6): die sieben tragenden Zeilen 60-W085-01, 60-R24-01, 60-S074-01, 60-R17-01, 60-S093-01, 60-S094-01 und 60-S092-01 tragen jetzt Effektgröße, Studientyp, volltextgeprüfte Quelle, Übertragbarkeit, Datenlage je Zelle und Entscheidung — zwei davon „Basiswert" (Hazard 60-W085-01, Mengengerüst 60-R24-01) —, während die übrigen 25 Zeilen weiterhin auf „offen" stehen. | — | behoben |
| 4 | A | Bericht Kap. 4 Z. 187–199 · **Lücke (§2.4, §3.4; LF 7/8)** — 0 Zeichen Substanz. Kein nationaler Anker, keine Anker-Zeitreihe mit Revisionsstand, kein Niveau-Skalar, keine unabhängige Verteilungsprüfung auf dem Ereignisregime mit vorab fixierter Toleranz und Ist-Ergebnis, keine Sanity-Bänder. **Vorschlag:** Anker-Kandidaten benennen (z. B. amtliche Hochwasser-Schadensbilanzen) und die Prüfachse „Ereignisregime" mit Toleranz vorab fixieren; zulässige Auflösungen nach §3.4 sind bereits korrekt notiert. **Umsetzungsnachweis:** Bericht Kap. 4, Abschnitte 4.1–4.8: benannter nationaler Anker (GDV-Naturgefahrenstatistik, Teilreihe Starkregen/Überschwemmung, Reihe seit 2002, Revisionsstand Datenservice Naturgefahrenreport 2025, vorläufiges Jahr 2025 gesondert ausgewiesen), Niveau-Skalar λ = 1,05 mit Rechenweg A\*/M₀, unabhängige Verteilungsprüfung auf der Achse Ereignisregime mit vorab fixierter Toleranz ±15 Prozentpunkten und Ist-Differenz 4,6 Prozentpunkten, Sanity-Band 0,56–2,26 Mrd. €₂₀₂₆/a mit Herleitung beider Grenzen, P1-Parametertabelle und ausdrücklicher Auflösungssatz (Bundesland-, Gemeindepunkt- und Stichprobenebene, kein nationaler 100-m-Vollraster-Lauf). | `python3 -c "import re;s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();k=s.split('\n## 4 ')[1].split('\n## 5 ')[0];raise SystemExit(0 if len(re.sub(r'<!--.*?-->','',k,flags=re.S).strip())>=6000 else 1)"` | behoben |
| 5 | A | Bericht Kap. 3 Z. 160–165 · **Lücke (§3.1 Datenebenen-Anlagepflicht; LF 12)** — die beiden benötigten Zellgrößen (HQ-Überflutungsflächen/Wassertiefen, Gebäudebestandswerte) werden nur im Futur und im HTML-Kommentar angekündigt; keine Ebene ist mit Quelle, keyless Beschaffungsweg, Zell-Ableitungsregel, Fallback und Normierung spezifiziert, keine ist „neu anzulegen" oder „geparkt (Datenquelle fehlt)" gekennzeichnet. **Vorschlag:** beide Ebenen ausspezifizieren; wo keine offene Quelle existiert, „geparkt" mit Beschaffungs-Watchlist führen. **Umsetzungsnachweis:** Bericht Kap. 3, Abschnitt 3.2 „Datenebenen nach §3.1": HQ_FLAECHE, HQ_TIEFE und GEBAEUDEWERT sind mit Quelle, keyless Beschaffungsweg, Zell-Ableitungsregel, Fallback und Normierung als „neu anzulegen" spezifiziert, GEBAEUDEZUSTAND_BAUSTOFF als „geparkt (Datenquelle fehlt)" mit Beschaffungs-Watchlist und dokumentiertem Neutralwert 1,00; der HTML-Kommentar mit der Futur-Ankündigung ist entfallen. | `python3 -c "s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();k=s.split('\n## 3 ')[1].split('\n## 4 ')[0];raise SystemExit(0 if all(t in k for t in ('HQ_FLAECHE','HQ_TIEFE','GEBAEUDEWERT','neu anzulegen','geparkt (Datenquelle fehlt)','Beschaffungs-Watchlist')) else 1)"` | behoben |
| 6 | B | Bericht Kap. 1 Z. 86 gegen `KWRA-Monetarisierung.xlsx` „Schadenskonten-System" Z29, „Abgleich-Protokoll" Punkt 3, „Risiken-Monetarisierung" Z42 · **Lücke (§3.3 R9-Partition mit Zitat; LF 4)** — K3 hat sieben Buchungsobjekte; #37 (Aquakultur, Sachschäden an Anlagen in K3, Kante 49 → 37) fehlt in Bilanz und Partitionsliste vollständig, #12 steht nur als Bilanzzeile ohne Partitionsregel-Zitat (Mon. Z17 schließt gegenüber #60 nichts aus). **Vorschlag:** #37 und #12 in die Liste „ohne Partitionsregel (offen)" aufnehmen und die Abgrenzung (Gebäude vs. Aquakulturanlagen; Massenbewegung vs. Flusshochwasser) mit R9-Zitat entscheiden. | — | offen |
| 7 | B | Bericht §5.1.2 Z. 240–243 gegen Kap. 4 · **Lücke (§3.5 Doppelzählungs-Wächter gegen die Kalibrierjahre; LF 4)** — die Marginalität von Δq ist behauptet („vorhandener Objektschutz steckt bereits im Basisschaden"), aber ohne Kalibrierjahre und ohne Aussage über den heutigen Ausstattungsgrad nicht prüfbar. **Vorschlag:** den heutigen Objektschutz-Anteil als Referenzzustand beziffern (oder als geparkt kennzeichnen) und den Wächter an die Anker-Zeitreihe binden, sobald Kap. 4 steht. **Umsetzungsnachweis:** Bericht Kap. 4, Abschnitt 4.7: die Kalibrierjahre 2002 bis 2024 sind einzeln benannt (2025 als vorläufiges Jahr ausgeschlossen), Δq zählt ausdrücklich nur Nachrüstungen nach dem letzten Kalibrierjahr 2024, und der heutige Objektschutz-Anteil q₀ ist als „geparkt (Datenquelle fehlt)" mit Beschaffungs-Watchlist ausgewiesen statt gesetzt. | `python3 -c "s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();k=s.split('\n## 4 ')[1].split('\n## 5 ')[0];raise SystemExit(0 if all(t in k for t in ('2002','2024','geparkt (Datenquelle fehlt)','Doppelzählungs-Wächter')) else 1)"` | behoben |
| 8 | B | Bericht §5.1 Z. 221–222 gegen §5.1.1 Z. 229–234 · **Lücke (§3.2 „je Formel eine Zeichentabelle", §3.9 Fertig-Regel; LF 11/13)** — die Formel EAD_mit = EAD · (1 − r_S092) verwendet zwei Zeichen, die in keiner Zeichentabelle stehen und keine Herleitung haben: EAD und EAD_mit. Insbesondere fehlen Einheit, Bezugsjahr und Betrachtungsebene des Erwartungsschadens. Deckung 4 von 6 Zeichen. **Vorschlag:** beide Zeichen in §5.1.1 aufnehmen (Einheit €/a, Ebene Kommune, Herkunft: Kernformel Kap. 3) — der Eintrag zwingt zugleich zur Entscheidung über die native Ergebnisgröße. **Umsetzungsnachweis:** Bericht Abschnitt 3.5 (neue Zeichentabelle über alle 28 Formelzeichen der Kapitel 3 und 5) und §5.1.1, erste zwei Zeilen: EAD und EAD_mit tragen Bedeutung, Einheit €₂₀₂₆/a, Bezugsjahr 2026, Betrachtungsebene Kommune und eine `herleitung:`-Herkunft auf §3.1/§3.4 Schritt 3 bzw. §5.1. | `python3 -c "import re;s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();t=s.split('### 3.5 ')[1].split(chr(10)+'### ')[0];r=[[c.strip() for c in z.strip().strip(chr(124)).split(chr(124))] for z in t.split(chr(10)) if z.strip().startswith(chr(124))][2:];ok=all(len(c)==4 and (any(a in c[3] for a in ('register:','herleitung:')) or (c[3]=='Notation' and c[2]=='—')) for c in r);ead=[c for c in r if 'EAD' in c[0]];raise SystemExit(0 if ok and len(r)>=20 and any('2026' in c[1] and 'Kommune' in c[1] for c in ead) and any('mit' in c[0] for c in ead) else 1)"` | behoben |
| 9 | B | Bericht Z. 266–273 gegen `backend/` · **Lücke (§3.2 „jedes Beispiel als ausführbarer Golden-Test", §7; LF 11)** — der Block `python test: beispiel_60_s092_abschaetzung` rechnet auf (nachgerechnet: 0,035 / 0,0075 / 0,112), ist aber nirgends im Code hinterlegt (`grep -rn "beispiel_60" --include=*.py backend` → 0 Treffer). Bericht und Code können unbemerkt auseinanderlaufen. **Vorschlag:** Beispielblöcke automatisch als Golden-Tests einsammeln (ein Test je Block) und den Lint um „Beispielblock ohne Test = rot" ergänzen. **Umsetzungsnachweis:** Bericht Abschnitt 3.6, Block `python test: beispiel_60_kernformel` (unmittelbar vor Abschnitt 3.7): die Kernformel aus 3.4 rechnet an einer Beispielzelle samt Aggregation auf eine Kommune aus zwei Zellen mit zehn `assert`-Zeilen durch; `beispiel_bloecke()` führt alle drei Blöcke des Berichts bei jedem Lint-Lauf aus und verlangt je Block eine Zusicherung. **Abweichung:** Das Einsammeln als Golden-Test im Backend gehört zur Integration (P-N), nicht zu diesem Berichtsschritt; der Prüfausdruck prüft deshalb die Ausführbarkeit der Blöcke im Bericht. | `python3 -c "import re;s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();b=re.findall('python test: ([a-z0-9_]+)'+chr(10)+'(.*?)'+chr(10)+chr(96)*3,s,re.S);[exec(compile(c,n,'exec'),{}) for n,c in b];raise SystemExit(0 if b and all('assert' in c for n,c in b) and any(n=='beispiel_60_kernformel' for n,c in b) else 1)"` | behoben |
| 10 | B | Bericht §5.1.2 Z. 248–250 · **Fehler (§3.2 Tails/„Parameter messen statt setzen", §3.9 „Abgeschätzt nur wenn keine Quelle existiert"; LF 7)** — s_bem = 0,50 ist der Anteil der Schadenssumme aus Ereignissen unterhalb des Bemessungsniveaus, also genau eine Quantilsgröße der Tiefen-/Schadensverteilung. Der Bericht setzt die Mitte mit symmetrischem Band, obwohl die HQ-Szenarien, aus denen sie folgt, laut Mon. Z65 ohnehin die Bewertungsgrundlage sind; der dokumentierte Ersetzungspfad (Z. 261–262) hebt die Anforderung nicht auf. **Vorschlag:** s_bem aus den HQ-Szenarien empirisch bestimmen, sobald die Ebene nach §3.1 spezifiziert ist; bis dahin die Setzung als Näherung mit Richtungsangabe kennzeichnen (welche Richtung über- bzw. unterschätzt den Hebel). **Umsetzungsnachweis:** Bericht §5.1.2 (Punkt \(s_{\text{bem}}\)) und neuer Abschnitt 5.1.3 (Anker `#s-bem-naeherung`): 0,50 ist ausdrücklich als Näherung geführt — Obergrenze 4,174/6,311 = 0,661 aus der Szenario-Zerlegung §4.5, Richtung „überschätzt den Hebel \(r_{\text{S092}}\)" mit zwei Begründungen, Mess-Ersetzungspfad auf Stichproben der HQ-Szenarien (§3.4), obere Bandgrenze an der Obergrenze auf 0,66 gekappt (Band 0,30–0,66, daraus r_S092 0,0075–0,1056) — und der Parameter-Block `flood_bldg.s_bem` trägt dies maschinenlesbar (`naeherung: true`, `naeherung_richtung: ueberschaetzt_hebel`). **Abweichung:** Der Weg „empirisch bestimmen" ist nicht gangbar, solange die Ebene HQ_TIEFE den Stand „neu anzulegen" trägt. | `python3 -c "s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();k=s.split('### 5.1.3 ')[1].split(chr(10)+'## 6 ')[0];b=s.split('id: flood_bldg.s_bem')[1].split('---')[0];raise SystemExit(0 if all(t in k for t in ('Näherung','überschätzt','0,661','Stichproben')) and all(t in b for t in ('naeherung: true','naeherung_richtung: ueberschaetzt_hebel','herleitung_anker: \"#s-bem-naeherung\"')) else 1)"` | behoben |
| 11 | B | Bericht Kap. 8 Z. 336–351 · **Lücke (§3.8; LF 10)** — keine der drei Quellenangaben trägt DOI/URL, Zugriffsdatum oder Archiv-Snapshot (`grep -c http …` → 0); das Format steht nur als Kommentar Z. 350. Für die Hochwasserschutzfibel liegen die vollständigen Angaben im Code (`sources.py` Z. 144–153), sind aber nicht in den Bericht gezogen. **Vorschlag:** die beiden Arbeitsmappen mit Dateistand/Prüfsumme und Zugriffsdatum führen, die Fibel mit den Angaben aus `sources.py`; §3.8 verlangt zusätzlich Volltextverifikation vor jeder Übernahme. | — | offen |
| 12 | B | Bericht Kap. 1 Z. 90–100 gegen Konten Z27 und Mon. Z64/Z65 · **Lücke (§3.3 Kostensätze mit Preisstand; LF 9)** — für ein K3-Buchungsobjekt führt der Bericht keinen Kostensatz und keinen Preisstand, obwohl Konten Z27 „Wiederherstellungs-/Zeitwertkosten; Schadensfunktionen × Bestandswerte" verlangt; R5 (Versicherungsleistungen sind Transfers) ist über „Wie ID 59" inhaltlich einbezogen, steht aber weder in der Regelspalte Mon. Z65 noch als Entscheidung im Bericht. **Vorschlag:** Kostensatz-Typ und Preisstandjahr festlegen und die R5-Zuordnung entweder als bewusste Fortschreibung im Abgleich-Protokoll nachziehen oder als Nicht-Anwendung begründen. | — | offen |
| 13 | B | Bericht Kap. 1 Z. 35–36 und Entscheidungslog Nr. 1 Z. 380 gegen `backend/app/data/catalog.py` Z. 335–340 und KWK Z272 · **Fehler (§5 LF 14 Quellen-Synchronität; Eiserne Regel 5)** — die Behauptung „der Code-Bestand trägt **genau** die Namenslisten von W117" ist nachgerechnet falsch: 5 statt 7 Sensitivitäten (es fehlen S096 und S098), 5 statt 8 Wirkungs-Eingänge, und diese aus der Labelliste statt aus `Input_Namen_Wirkung`. Die Behauptung stützt die Umschnitt-Entscheidung. **Vorschlag:** Aussage im Bericht auf den belegbaren Stand korrigieren (Teilmenge, abweichende Namensquelle) und die Code-Divergenz als eigenen Integrationspunkt für `/integriere-risiko` führen — **nicht** in dieser Runde im Code fixen. | `python3 -c "import re;s=open('backend/app/data/catalog.py',encoding='utf-8').read();b=s.split('\"kwra_id\": 60')[1].split('kwra_id')[0];raise SystemExit(0 if b.count('\"')//2>=0 else 1)"` | offen |
| 14 | B | Bericht Kap. 6 Z. 275–284 gegen Kap. 1 Z. 102–103 · **Lücke (§3.2 Szenario-Anwendung, §3.6 „Infokasten-Texte sind Teil des Berichts"; LF 12)** — 3 Zeichen Substanz. Es fehlen der Absatz „Szenario-Anwendung" (verschobene Größe, konstante Größen, Stationaritätsannahmen, Bestandsdynamik S104), die nummerierten Modellgrenzen und die drei fest verdrahteten UI-Abgrenzungen (Benennung „bewerteter Schaden — Konto K3", Vollständigkeitsanzeige, Versionsstempel), obwohl Kap. 1 sie ausdrücklich ankündigt. **Vorschlag:** Infokasten-Texte ausschreiben, sobald die native Ergebnisgröße feststeht; die Untergrenzen-Aussage (K1/K4/K5/K8 nicht enthalten) liegt inhaltlich bereits vor. **Umsetzungsnachweis:** Bericht Kap. 6 „Szenario-Anwendung & Modellgrenzen" trägt jetzt den Absatz „Szenario-Anwendung 60-A", die nummerierte Modellgrenzen-Liste (Punkt 1 Untergrenzen-Aussage K1/K4/K5/K8, Punkt 2 Bauform-Grenze der P2-Abschätzung 60-S094-01) und die drei wörtlichen Infokasten-Texte. | `python3 -c "import re;s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();k=s.split('\n## 6 ')[1].split('\n## 7 ')[0];raise SystemExit(0 if len(re.sub(r'<!--.*?-->','',k,flags=re.S).strip())>=2500 else 1)"` | behoben |
| 15 | B | Bericht Kap. 7 Z. 290–334 · **Lücke/Widerspruch (Vorgabe P1; §4 Parameter-Block-Format; LF 12)** — die P2-Kennzeichnung „Abschätzung von KAP3" steht ausschließlich als YAML-Kommentar hinter `herkunft:`; P1 sagt ausdrücklich, eine Herleitung nur als Code-Kommentar erfülle die Vorgabe nicht. Zusätzlich liegen `endpunkt: K3-Wiederherstellung` und `bandzuordnung: [alle]` außerhalb des in §4 definierten Wertebereichs (`mortalitaet \| morbiditaet \| beide`), ohne Fortschreibung der Aufgabe. **Vorschlag:** ein maschinenlesbares Feld für die Abschätzungs-Kennzeichnung samt Herleitungs-Anker einführen und den §4-Wertebereich für K3/K4-Ereignisschäden als Fortschreibung der Aufgabe beantragen statt still zu überschreiben. **Umsetzungsnachweis:** Bericht Kap. 7: jeder der vier Blöcke trägt jetzt die Felder `kennzeichnung: abschaetzung_kap3`, `herleitung_anker:` (auf `#s092-wirkung` bzw. `#s-bem-naeherung`, beide als `<a id=…>` im sichtbaren Text gesetzt) und `wertebereich_abweichung: "#fortschreibung-endpunkt-k3"` statt der YAML-Kommentare, und der neue Abschnitt 7.1 beantragt die Fortschreibung des §4-Wertebereichs für `endpunkt`/`bandzuordnung` für die Familie K3/K4-Ereignisschäden mit Begründung und Datum 13.09.2026. **Abweichung:** Die Felder werden nicht auf einen zugelassenen Wert umgebogen (jeder wäre sachlich falsch), und der Lint erzwingt das neue Feld hier nicht — das gehört T-0234. | `python3 -c "import re;s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();k=s.split(chr(10)+'## 7 ')[1].split(chr(10)+'## 8 ')[0];bl=re.split(r'^parameter:$',k,flags=re.M)[1:];kz=[re.search(r'^  kennzeichnung: (\S+)$',b,re.M) for b in bl];ok=all(m and m.group(1) in ('quelle','abschaetzung_kap3') for m in kz) and all(re.search(r'^  herleitung_anker: \"#\S+\"$',b,re.M) and re.search(r'^  wertebereich_abweichung: \"#fortschreibung-endpunkt-k3\"$',b,re.M) for b in bl);ank=all(('<a id=\"'+a+'\">') in s for a in ('s092-wirkung','s-bem-naeherung','fortschreibung-endpunkt-k3'));raise SystemExit(0 if len(bl)==4 and ok and ank and '13.09.2026' in k.split('### 7.1 ')[1] else 1)"` | behoben |
| 16 | B | Bericht Kap. 9 Z. 353–374 · **Lücke (§2.6, §3.7; LF 12)** — der für den ersten Vertreter einer Familie verbindliche Ansatz-Vergleich besteht aus einem 7 × 3-Raster „offen"; Ansätze (b) und (c) sind nicht einmal benannt. Folge: Die Umsetzungsgrundlage bleibt laut Kopf Z. 4 offen, und die Herleitungspflicht §3.9 hat keinen definierten Geltungsbereich. **Vorschlag:** (b) und (c) benennen (z. B. Schadensfunktion je Gebäudetyp vs. aggregierte Flächenschadensrate) und das Kriterienraster füllen; das Negativ-Beispiel „nationaler Schadenstopf × Anteil" ist bereits ausgeschieden. **Umsetzungsnachweis:** Bericht Kap. 9 „Ansatz-Vergleich", Abschnitte „Die drei verglichenen Ansätze", „Kriterienraster" und „Umsetzungsgrundlage": die drei Ansätze (a) typisierte Tiefen-Schadensfunktion je 100-m-Zelle, (b) aggregierte Flächenschadensrate und (c) Schadensgradmodell D0–D6 am Einzelgebäude sind benannt, jede der 21 Rasterzellen ist bewertet, und Ansatz (a) ist mit Begründung gegen (b) und (c) als Umsetzungsgrundlage festgelegt — nachgezogen in der Kopfzeile (Z. 3–5) und im Entscheidungslog Nr. 5 (13.09.2026). | — | behoben |
| 17 | C | `backend/scripts/lint_methodik.py` gegen Bericht Kap. 3/4/6 · **Lücke (§7 deterministische Lints; LF 11)** — der Lint meldet „83 Checks grün / ALLE LINTS GRÜN" für einen Bericht, dessen Kapitel 3, 4 und 6 zusammen 3 Zeichen Substanz tragen: Er prüft, was dasteht, aber nicht, ob die Pflichtkapitel §4 überhaupt gefüllt sind, und er sieht HTML-Kommentare nicht (die verbotene Zukunftsformulierung „wird … vollständig spezifiziert" steht Z. 161 unbeanstandet im Kommentar). **Vorschlag:** Check „Pflichtkapitel mit < N Zeichen außerhalb von HTML-Kommentaren = rot" und die Negativ-Formulierungen auch in Kommentaren prüfen; Zählung grüner Checks um eine Zählung übersprungener Checks ergänzen. | `python3 -c "import re;s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();k=[len(re.sub(r'<!--.*?-->','',t,flags=re.S).strip()) for t in re.split(r'\n## ',s)];raise SystemExit(0 if min(k)>200 else 1)"` | offen |
| 18 | C | Bericht Entscheidungslog Nr. 3 Z. 382 und Kap. 7 Z. 290–334 gegen Register-Zeile 60-S092-01 Z. 135 · **Widerspruch (§2.2 „In Formeln dürfen später nur Zeilen mit Entscheidung Basiswert stehen"; LF 5/12)** — die Registerzeile trägt Entscheidung „offen (Vorschlag: Maßnahmen-Hebel, abgeschätzt)", während Kap. 7 bereits vier bezifferte, zur Registry-Extraktion vorgesehene Parameter-Blöcke aus ihr ableitet und der Kopf Z. 12 „Alle übrigen Entscheidungen stehen auf offen" sagt. Damit ist unklar, ob der Hebel entschieden ist oder nicht. **Vorschlag:** Entscheidung der Zeile 60-S092-01 explizit auf „Maßnahmen-Hebel (abgeschätzt)" setzen — oder die Parameter-Blöcke bis zur Entscheidung als „nicht extrahieren" kennzeichnen. **Umsetzungsnachweis:** Bericht Kap. 2, Abschnitt „Evidenz-Register (§2.2)", Zeile 60-S092-01: die Spalte „Entscheidung" trägt jetzt „Maßnahmen-Hebel (abgeschätzt)" statt „offen (Vorschlag: Maßnahmen-Hebel, abgeschätzt)", sodass die Parameter-Blöcke in Kap. 7 aus einer entschiedenen Zeile im Sinne von §2.2 ableiten, während die Kennzeichnung §3.9 ABGESCHÄTZT und die Modellgrenze „kommunal (Pauschalfaktor)" nach Vorgabe P2 in der Zeile stehen bleiben (Kopf-Geltungsbereich und Kap. 2 sind entsprechend nachgezogen). | — | behoben |

### 4 · Konvergenz-Verdikt (§5.4)

- **Lints grün: ja.** `python3 backend/scripts/lint_methodik.py 60` meldet 83 grüne und 0 rote
  Checks (Ausgabe wörtlich oben). Reichweite eingeschränkt, siehe Befund 17.
- **Alle 14 Leitfragen mit Verdikt: ja.** LF 1 bis LF 14 sind einzeln beantwortet, jede mit
  Fundstelle (Datei plus Kapitel, Zeilennummer oder Zellbezug); sieben davon (LF 1, 4, 7, 10, 11,
  13, 14) nachgerechnet statt gelesen.
- **Neue A- oder B-Befunde in dieser Runde: ja.** 16 von 18 — fünf A (1–5) und elf B (6–16); dazu
  zwei C (17, 18).
- **Null-Runde: nein.**

Folge nach §5/§6: Der Bericht #60 ist **nicht abnahmereif**; die fünf A-Befunde blockieren die
Abnahme, `/integriere-risiko 60` bleibt gesperrt. Nächster Schritt nach dem Loop wäre eine
Revision (Autor-Session) — sie ist **nicht** Teil von T-0232 und wurde hier bewusst nicht
begonnen.

### 5 · Aufwand dieser Runde (Messzweck von T-0232)

Eine Review-Runde über einen frischen M1-Erstaufschlag: **18 Befunde (A 5 · B 11 · C 2)**,
14 Leitfragen-Verdikte, davon 7 nachgerechnet. Verbrauch dieser Session siehe Ergebnisnotiz zum
Ticket. Die Befunde 1–5 sind Substanz-Lücken des Erstaufschlags (drei leere Pflichtkapitel,
leeres Register, fehlende Datenebenen) — sie sind mit einer Revisionsrunde nicht zu schließen,
sondern entsprechen dem eigentlichen Herleitungsaufwand des Berichts. Die Befunde 6–18 sind
Runden-Material im engeren Sinn.

## Review-Runde 2

**Datum: 13.09.2026** · Re-Review nach §6 („**volle Prüfung erneut**, wenn Kalibrierung oder
Modellstruktur geändert wurde" — beides wurde mit T-0235…T-0243 und T-0256…T-0259 geändert) ·
Maßstab: ausschließlich §3 und §5 von `docs/AUFGABE_METHODIK_SCHADENSRECHNUNG.md`, **nicht** der
Berichtstext · Eiserne Regel 4: frische Sitzung; diese Session hat den geprüften Stand nicht
geschrieben (geschrieben haben die genannten Autoren-Tickets, alle im Endstatus).

Die Runde ist in **sieben Pakete** geschnitten, die nacheinander in diese Datei schreiben und
zusammen die 14 Leitfragen abdecken. **Dieses Paket (T-0270) ist das erste** und trägt
**Leitfrage 1 und Leitfrage 14**; es legt den Abschnitt an, die Geschwisterpakete hängen ihre
Verdikte darunter. Die übrigen Leitfragen (LF 2–13) und die Regression der Befunde 1–19 sind
ausdrücklich **nicht** Gegenstand dieses Pakets und hier weder geprüft noch beantwortet.

### 0 · Vorbedingung nach §5, Schritt 0 — Prüfgrundlagen-Bundle (§1)

Das vollständige Bundle nach §1 lag dieser Session **ab dem ersten Turn** vor (im Repo unter den
genannten Pfaden, keine Nachreichung, kein Extra-Durchgang — Lehre aus der M0-Prüfung):

| Bestandteil des Bundles (§1) | Pfad | Stand zum ersten Turn |
|---|---|---|
| Bericht (Prüfgegenstand) | `docs/methodik/60_gebaeudeschaeden_flusshochwasser.md` | vorhanden, 158.851 Zeichen |
| Aufgabe (einzige Instruktionsquelle, v2) | `docs/AUFGABE_METHODIK_SCHADENSRECHNUNG.md` | vorhanden, §3/§5/§6 gelesen |
| Arbeitsmappe Wirkungsketten | `docs/Schadensbaum/KWRA-Schadensbaum_X_UBA-klimawirkungsketten.xlsx` | vorhanden, Blätter „Klimawirkungsketten", „Schadensbaum-Netzwerkliste" |
| Arbeitsmappe Monetarisierung | `docs/Schadensbaum/KWRA-Monetarisierung.xlsx` | vorhanden, Blätter „Risiken-Monetarisierung", „Schadenskonten-System", „Rechenregeln", „Abgleich-Protokoll" |
| Anlage: Evidenz-Register (risikoübergreifende Spiegelung) | `docs/evidenz/register.md` | vorhanden, unverändert gelesen |
| Anlage: Befund-Ledger (diese Datei) | `reviews/BEFUNDE_60.md` | vorhanden, Befunde 1–19 |
| Anlage: Code-Bezug der Kap.-1-Aussage (eiserne Regel 5) | `backend/app/data/catalog.py` | vorhanden, nur gelesen |
| Anlage: deterministische Lints (§7) | `backend/scripts/lint_methodik.py` | vorhanden, nur **ausgeführt**, nicht geändert |

Weitere Anlagen (Skripte, CSVs) führt der Bericht nicht; die ausführbaren Beispiele liegen als
`python test:`-Blöcke im Bericht selbst und werden vom Lint mitgefahren.

**Prüfumfang dieses Pakets:** Kapitel 1 „Wirkungskette & Knoten-Bilanz" (Z. 37–151) sowie Kopf,
Ergebnis und Entscheidungslog — zusammen rund 22.800 Zeichen. Nachgemessen mit
`python3 -c "s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();k=s.split(chr(10)+'## 1 ')[1].split(chr(10)+'## 2 ')[0];kopf=s.split(chr(10)+'## 1 ')[0];el=s.split(chr(10)+'## Entscheidungslog')[1];print(len(k),len(kopf)+len(el),len(k)+len(kopf)+len(el))"`:
15.669 Zeichen Kapitel 1 (mit Überschriftszeile 15.674), 7.112 Zeichen Kopf + Ergebnis +
Entscheidungslog, Summe 22.781 — die Abweichung von wenigen Zeichen gegenüber den im Ticket
genannten 15.672 / 7.126 / 22.798 rührt allein aus der Schnittkante (Überschriftszeile und
Leerzeilen mitgezählt oder nicht); der geprüfte Textkörper ist derselbe. Ein nationaler
100-m-Vollraster-Lauf nach §3.4 ist nicht verlangt und wurde **nicht** gefahren; alle Nachrechnungen
laufen zellweise gegen die Arbeitsmappen (openpyxl, Repo-Wurzel als Arbeitsverzeichnis).

### 0.1 · Deterministische Lints (§7 — übernommen, nicht manuell nachgeprüft)

Ausgabe von `python3 backend/scripts/lint_methodik.py 60` am 13.09.2026, wörtlich und unverändert
übernommen:

```
=== #60 · 60_gebaeudeschaeden_flusshochwasser.md ===
  115 Checks grün
  Historie-Marker: 0 markierte Zeilen (Ratchet None), 0 gedeckte Fundstellen abgelöster Werte:

ALLE LINTS GRÜN
```

Der Lint wurde nur ausgeführt, nicht geändert (die Datei gehört T-0234). Eine Bewertung der
Reichweite dieser Checks gehört zu Befund 17 und zur Befund-Regression im Geschwisterpaket.

### 0.2 · Leitfragen dieses Pakets (§5) — einzeln mit Verdikt und Beleg

**LF 1 — Kette (nachgerechnet statt gelesen). Verdikt: Befund** (→ neue Befunde **20** und **21**).

Prüfweg: Die Knoten-Bilanz (Kap. 1, Tabelle nach „Entscheidungsstand (T-0235)", 32 Zeilen) wurde
zellweise gegen die Arbeitsmappen abgeglichen — nicht gegen die Behauptungen des Berichts —, und
anschließend wurde geprüft, ob jede als „verarbeitet" ausgewiesene Zeile in Kapitel 3/5/6
tatsächlich eine Rechenstelle hat.

*Bilanzumfang (Sollmenge aus der Mappe).* Blatt „Klimawirkungsketten": **E272/F272/G272/H272**
(W117) tragen 6 Einflüsse (`E10; E08; E17; E14; E02; E03`), 7 Sensitivitäten
(`S092; S093; S094; S096; S097; S098; S104`), 3 räumliche (`R23; R24; R25`) und 8 Wirkungs-Eingänge
(`W074; W077; W085; W087; W008; W006; W091; W100`) = 24; **E208/F208/G208** (W085) tragen
`E12; E07; E08` · `S072; S073; S074` · `R17; R18; R19` = 9, H208 ist leer; E08 ist doppelt, also
24 + 8 = **32**. Die Bilanz führt 32 Zeilen, und die Mengen sind **deckungsgleich**: Prüfausdruck
über Mengengleichheit ergibt `nur Bericht: set() | nur Mappe: set()`. Kein Knoten fehlt, keiner ist
zusätzlich erfunden.

*Zellweise Stichproben (je Stichprobe Blatt und Zelle).*

| # | Zelle in der Arbeitsmappe | Inhalt laut Mappe (wörtlich/gekürzt) | Behauptung im Bericht | Ergebnis |
|---|---|---|---|---|
| 1 | KWK **A272 / B272** | `W117` · „Schäden an Gebäuden und Infrastrukturen" | Kap. 1 „W-Knoten": W117 = Container-Knoten, KWK Z272 | trifft zu |
| 2 | KWK **H272** | `W074; W077; W085; W087; W008; W006; W091; W100` (8 Einträge) | 8 Wirkungs-Eingänge; W085 als Hochwasser-Eingang | trifft zu |
| 3 | KWK **A208 / E208 / F208 / G208 / H208** | `W085` · 3 · 3 · 3 · leer | W085 = Id 49, Eingänge „eine Ebene tief mit aufgenommen" ⇒ 32 Zeilen | trifft zu (24 + 8 = 32) |
| 4 | KWK **B199** | „Topographie (Geländeform, Höhe, **etc.**)" | Bilanzzeile S074: „Topographie (Geländeform, Höhe)" | Name **gekürzt** → Befund 21 |
| 5 | KWK **B223** | „Einschränkungen **der Funktionsfähigkeit von** Kanalnetzen und **Vorflutern**" | Bilanzzeile W100: „Einschränkungen Kanalnetze und Vorfluter" | Name **gekürzt** → Befund 21 |
| 6 | KWK **B256** | „Bauliche, organisatorische und finanzielle Vorsorge der Eigentümer und Nutzer **von Gebäuden und Infrastrukturen**" | Bilanzzeile S092: „… der Eigentümer und Nutzer" | Name **gekürzt** → Befund 21 |
| 7 | NW **A61/C61/E61/F61/G61/H61/I61/J61** | `60` · „Buchungsobjekt — Ebene B" · „sehr dringend" · `49` · „Hochwasser" · leer · „K3 Gebäude & Sachwerte" · „K3-Wiederherstellung" | Kap. 1 „Rolle (Rollen-Check)" und „Weitergaben: **keine** Output-IDs" | trifft zu, wörtlich |
| 8 | Mon. **J65 / K65 / L65 / N65** | „Wie ID 59, ereignisbezogen flussseitig; HQ-Szenarien × Schadensfunktionen (Wassertiefe-Schaden) × Gebäudewerte." · „Sachschäden flussseitiger Überflutung." · „Seeseitige Schäden (ID 46); Verkehrsinfrastruktur (ID 74); Schutzkosten (ID 50, R7)." · „R7, R9" | Kap. 1 Konto-Einbettung und die Inaktiv-Begründungen von E10/E17/E14/E02/E03/W074/W077 | trifft zu, wörtlich |
| 9 | Rechenregeln **A11/C11** | `R9` · „… Innerhalb eines Kontos zählt jede Einheit (Todesfall, kWh, Tonne, Gebäude) genau einmal; verschiedene Konten desselben Ereignisses sind additiv." | R9-Zitat in den Zeilen E08, W008, W006, W091 (Bericht kürzt die Aufzählung sichtbar mit „…") | trifft zu |
| 10 | Konten **C26 / C27 / C28 / C29** | K3-Definition · „Wiederherstellungs-/Zeitwertkosten; Schadensfunktionen × Bestandswerte" · „Betriebsunterbrechung (→K5), Infrastruktur (→K4), Personen (→K1)" · 7 Buchungsobjekte `12 · 37 · 46 · 59 · 60 · 92 · 102` | Kap. 1 Konto-Einbettung, Inaktiv-Zitate R18/R19/R23/R25, Partitionsliste der Weitergaben | trifft zu; alle 7 Buchungsobjekte sind in den Weitergaben adressiert |
| 11 | Abgleich-Protokoll **Z7 (A–F)** und **Z10 (A–F)** | Punkt `3` · `49` „Hochwasser" → `37` „Schäden an Aquakulturen" · „Kante"; Punkt `5` · `55` → `K3` „Direktbuchung Konto K3" · „Direktbuchung" | Weitergaben: Kante 49 → 37 (Punkt 3); Id 55 bucht direkt in K3 (Punkt 5) | trifft zu |
| 12 | Abgleich-Protokoll, Spalten **B und D** über alle 152 Zeilen | keine Zeile mit Quelle-ID 60 oder Ziel 60 | Weitergaben: „das Abgleich-Protokoll hat keinen Punkt mit Quelle oder Ziel 60" | trifft zu |

*Verarbeitungsstand.* Die Spalte „rechnet in" trägt heute **0 mal `offen`**: 16 Zeilen tragen eine
der sieben Formelstellen (FS-Hazard 6, FS-Exposition 2, FS-Schadensgrad 2, FS-Mengengerüst 1,
FS-Schutzsystem 3, FS-Bestandsdynamik 1, FS-Vorsorge 1), 16 Zeilen tragen `inaktiv` mit wörtlichem
Regel- oder Mappenzitat. Befund 2 aus Runde 1 ist insoweit sichtbar abgearbeitet — die Regression
der Befunde 1–19 führt aber das Geschwisterpaket, nicht dieses.

*Der Befund liegt bei der zweiten Hälfte von LF 1 („Eingänge, die nirgends rechnen?").* Drei
Knoten (S096, S097, S098) sind mit **FS-Schutzsystem** als verarbeitet ausgewiesen; die
Zeichenfolge `FS-Schutzsystem` kommt im gesamten Bericht **außerhalb von Kapitel 1 kein einziges
Mal** vor, und die Kernformel §3.4 (Schritte 1–3) enthält keinen R7-Term: Ihre Faktoren sind
\(W_z, a_{z,s}, d(h_{z,s}), f_{S093}, f_{S094}, p_i, k_{\text{BGF}}, \theta_{z,t}, n_t\). Damit
rechnen diese drei Eingänge nirgends → **Befund 20** (Belege dort). Hinzu kommen die drei
gekürzten Knotennamen aus den Stichproben 4–6 → **Befund 21**.

**LF 14 — Quellen-Synchronität. Verdikt: Befund** (→ neuer Befund **22**).

*Gegen die Arbeitsmappen: kein Widerspruch im Prüfumfang dieses Pakets.* Sämtliche in Kapitel 1
zitierten Zellen sind oben zellweise gegengelesen (Stichproben 1–12): Konten Z26/Z27/Z28/Z29,
Rechenregeln Z7 (R5), Z9 (R7), Z11 (R9), Z19 (A4), Z20 (A5), Mon. Z17/Z42/Z51/Z54/Z56/Z57/Z64/Z65/Z106,
NW Z13/Z50/Z61 sowie Abgleich-Protokoll Punkt 3 (Z7), Punkt 5 (Z10), Punkt 15, Punkt 16. Alle
Zitate treffen den Zellinhalt wörtlich; Kürzungen sind durchgehend mit „…" gekennzeichnet
(Ausnahme: die drei **Knotennamen** der Stichproben 4–6, die ohne Kürzungszeichen verkürzt sind —
Befund 21). Eine **bewusste Fortschreibung** einer Arbeitsmappe nimmt der geprüfte Umfang nicht
vor: weder Kapitel 1 noch Kopf/Ergebnis/Entscheidungslog überstimmen eine Mappenzelle; die
Arbeitsmappen wurden in dieser Session ausschließlich gelesen (eiserne Regel 2). Die Divergenz
Bericht ↔ `backend/app/data/catalog.py` ist in Kap. 1 Absatz „W-Knoten" und im Entscheidungslog
Nr. 6 offen als Integrationspunkt geführt und **nicht** still im Code geheilt — eiserne Regel 5
ist hier eingehalten; auch dieses Paket ändert keine Code-Datei.

*Gegen die Aufgabe: Widerspruch in einem verbindlichen Punkt.* Kopf und Ergebnis beschreiben einen
Bearbeitungs- und Prüfstand, den der Bericht nicht mehr hat (Status „noch nicht gegengeprüft",
Datum 11.09.2026, „Kap. 4–8 tragen die Pflichtinhalte als Kommentar", „Offen: … Kap. 4, 6, 8",
„Gegenprüfung … noch nicht gemessen"), obwohl §4 den Kopf als Teil der verbindlichen
Berichtsstruktur führt und §6 den Prozessstand als Abnahmegrundlage nimmt → **Befund 22**.

### 0.3 · Neue Befunde dieses Pakets (ab Nummer 20)

Format §5: Stelle · Art (Lücke/Fehler/Widerspruch) · Begründung · Vorschlag · Kategorie. Das Ledger
trug vor diesem Paket die Nummern 1–19; die erste neue Nummer ist deshalb **20**. **Dieses Paket
behebt keinen Befund** — weder einen neuen noch einen alten; es ändert außer dieser Datei keine
Datei. Die Kurzform-Tabelle „Offene Befunde" am Kopf dieses Ledgers ist bewusst **nicht**
angefasst: sie wird von der Befund-Regression dieser Runde (Geschwisterpaket) fortgeschrieben.

| Nr | Kat. | Befund (Stelle · Art · Begründung · Vorschlag) | Prüfausdruck | Status |
|---|---|---|---|---|
| 20 | A | Bericht Kap. 1 Knoten-Bilanz (Zeilen S096 KWK Z260, S097 Z261, S098 Z262) gegen Kap. 3.4 und Rechenregeln Z20 (A5) · **Widerspruch/Lücke (§2.1 „verarbeitet oder begründet inaktiv", §5 LF 1 „Eingänge, die nirgends rechnen")** — die drei Knoten sind als verarbeitet an der Formelstelle **FS-Schutzsystem** („R7-Erwartungswert-Weiche mit #50") ausgewiesen. Diese Formelstelle existiert in keiner Formel: `FS-Schutzsystem` kommt außerhalb von Kapitel 1 null mal vor, die Kernformel §3.4 trägt keinen Wahrscheinlichkeitsterm für Halte-/Versagensfall, und die Registerzeilen 60-S096-01/-S097-01/-S098-01 stehen in allen Sachspalten auf „offen". Die Mappe verlangt die Weiche ausdrücklich: Mon. **N65** „R7, R9" und Rechenregeln **C20** (A5): „Eintrittswahrscheinlichkeit × Schadensfunktion × Bestand; **Schutzsysteme über die R7-Erwartungswert-Weiche**"; Rechenregeln **C9** (R7) definiert sie als „Erwartungswert über Halte- und Versagensfall, wahrscheinlichkeitsgewichtet". Verschärfend: Kap. 9 („Kriterienraster", Zeile „Maßnahmen-Anschluss") behauptet für den gewählten Ansatz (a), die Schutzsysteme wirkten „über die R7-Weiche mit #50 am Hazard-Term; **beide Angriffspunkte existieren in der Formel bereits**" — das trifft für S092 zu (§5.1), für die R7-Weiche nicht. Damit stützt eine unzutreffende Aussage die Ansatz-Entscheidung (Entscheidungslog Nr. 5). **Vorschlag:** entweder die R7-Weiche in §3.4 als eigenen Term ausschreiben (p(HQ) aufgeteilt in Halte- und Versagensfall des Schutzsystems, Kopplung an #50) oder die drei Zeilen bis zur Bezifferung ausdrücklich auf „inaktiv (geparkt, Datenquelle/Modul fehlt)" mit Regelzitat setzen und die Behauptung in Kap. 9 auf den belegbaren Stand korrigieren; still weiterlaufen lassen ist nach §2.1 keine der beiden zulässigen Optionen. | `python3 -c "s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();k1=s.split(chr(10)+'## 1 ')[1].split(chr(10)+'## 2 ')[0];rest=s.split(chr(10)+'## 2 ')[1];raise SystemExit(0 if rest.count('FS-Schutzsystem')>0 else 1)"` | offen |
| 21 | C | Bericht Kap. 1 Knoten-Bilanz, Spalte „Name", Zeilen S074, W100, S092 gegen `KWRA-Schadensbaum_X_UBA-klimawirkungsketten.xlsx`, Blatt „Klimawirkungsketten", Zellen **B199**, **B223**, **B256** · **Fehler (§5 LF 14 Quellen-Synchronität; §3.8 wörtliche Übernahme)** — drei Knotennamen sind gegenüber der Arbeitsmappe **ohne Kürzungszeichen** verkürzt: B199 „Topographie (Geländeform, Höhe, etc.)" → „Topographie (Geländeform, Höhe)"; B223 „Einschränkungen der Funktionsfähigkeit von Kanalnetzen und Vorflutern" → „Einschränkungen Kanalnetze und Vorfluter"; B256 „… Vorsorge der Eigentümer und Nutzer von Gebäuden und Infrastrukturen" → „… Vorsorge der Eigentümer und Nutzer". Die übrigen 29 Namen sind wörtlich. Das wiegt hier schwerer als eine Formalie, weil derselbe Absatz („W-Knoten") dem Code-Bestand vorwirft, die Einträge seien „teils **umformuliert statt wörtlich** aus der Arbeitsmappe übernommen" (Befund 13) — der Maßstab muss für den Bericht selbst gelten. Bei W100 verschiebt die Kürzung zudem die Bedeutung (die Mappe spricht von der Funktionsfähigkeit, nicht von den Anlagen). **Vorschlag:** die drei Namen wörtlich aus B199/B223/B256 übernehmen oder die Kürzung sichtbar machen („…"). | `python3 -c "import openpyxl,re;s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();t=s.split('| Knoten | Name | Blatt/Zeile | rechnet in |')[1].split(chr(10)+chr(10))[0];rows=[[c.strip() for c in z.strip().strip(chr(124)).split(chr(124))] for z in t.split(chr(10)) if z.strip().startswith(chr(124))][1:];wb=openpyxl.load_workbook('docs/Schadensbaum/KWRA-Schadensbaum_X_UBA-klimawirkungsketten.xlsx',read_only=True,data_only=True);k=list(wb['Klimawirkungsketten'].iter_rows(values_only=True));bad=[r[0] for r in rows if re.sub(r'\s*\((über W085|= Id \d+|direkt[^)]*)\)\s*$','',r[1]).strip()!=k[int(re.search(r'KWK Z(\d+)',r[2]).group(1))-1][1]];raise SystemExit(0 if not bad else 1)"` | offen |
| 22 | B | Bericht Kopf (Z. 3–26) und Abschnitt „Ergebnis" (Z. 28–35) gegen den Ist-Stand des Berichts, dieses Ledger und §4/§6 der Aufgabe · **Widerspruch (§4 Berichtsstruktur „Kopf/Ergebnis", §6 Prozess; LF 14 gegen die Aufgabe)** — der Kopf führt „Status: **Erstaufschlag** (`/neu-risiko 60`) — **noch nicht gegengeprüft** · 11.09.2026", obwohl Review-Runde 1 am 13.09.2026 gefahren wurde (dieses Ledger) und dreizehn Autoren-Tickets den Stand seither geändert haben. Der Geltungsbereich sagt „**Kap. 4–8 tragen die Pflichtinhalte als Kommentar**" und „befüllt ist … Kap. 3 **bis einschließlich der Kernformel**", während Kap. 3 heute bis 3.7 reicht (Zeichentabelle, Aggregation, Schicht-A-Index) und Kap. 4 (8 Abschnitte mit Anker, Niveau-Skalar, Verteilungsprüfung), Kap. 5, 6, 7 und 8 ausgeschrieben sind. Das „Ergebnis" führt dieselben Teile noch als offen („Offen: (1) Zeichentabelle, Aggregation Zelle → Kommune und Schicht A in Kap. 3; (2) Kap. 4, 6, 8") und behauptet „Gegenprüfung ist nicht Teil des Tickets und noch nicht gemessen". Ein Prüfer oder Leser, der nach §4 dem Kopf den Geltungsbereich entnimmt, bekommt damit einen falschen Bearbeitungs- und Prüfstand; nach §6 hängt an diesem Stand die Abnahmefrage. **Vorschlag:** Kopfstatus, Geltungsbereich und „Ergebnis"/„Offen" am Ende jeder Revisionsrunde nachziehen (Status „in Revision, Runde N", Datum des letzten Stands, tatsächlich offene Punkte) und den Abgleich als Lint-Check verankern (gehört in den Vollständigkeits-Check T-0234, nicht in diesen Bericht). | — | offen |

### 0.4 · Abgrenzung und Status dieses Pakets

- **Beantwortet:** LF 1 (Verdikt Befund) und LF 14 (Verdikt Befund), beide mit Beleg; LF 1
  nachgerechnet über zwölf zellweise Stichproben (Blatt und Zelle je Stichprobe genannt) plus
  Mengengleichheit der 32 Bilanzzeilen.
- **Nicht Gegenstand dieses Pakets:** LF 2–13 und die Regression der Befunde 1–19 (Geschwisterpakete
  mit höherer Reihenfolge: Kap. 2 → LF 5/6; Kap. 3 und 5 → LF 2/3/11/13; Kap. 4 → LF 4/7/8;
  Kap. 6–9 → LF 9/10/12). Ein Konvergenz-Verdikt nach §5.4 wird erst gefällt, wenn alle sieben
  Pakete geschrieben haben.
- **Kein Befund behoben**, kein Bericht, kein Register, kein Code, kein Lint geändert:
  `docs/methodik/60_gebaeudeschaeden_flusshochwasser.md` und `docs/evidenz/register.md` sind
  byte-gleich geblieben.

### 1 · Paket T-0271 — Leitfragen 2, 3, 11 und 13 gegen Kapitel 3 und 5

Zweites Paket der Runde 2 (13.09.2026), eigene frische Sitzung: Sie hat den geprüften Stand nicht
geschrieben — Kapitel 3 stammt aus T-0236/T-0256…T-0259, Kapitel 5 aus T-0239, alle im Endstatus
(eiserne Regel 4). Das Bundle nach §1 lag ab dem ersten Turn vor (Tabelle in Abschnitt 0 dieser
Runde, unverändert gültig); die Lint-Ausgabe steht wörtlich in Abschnitt 0.1 und wird hier
**übernommen, nicht neu vorhergesagt** (§5, Schritt „zuerst die deterministischen Lints").

**Prüfumfang dieses Pakets:** Kapitel 3 „Modell" (Z. 451–833, Abschnitte 3.1–3.7) und Kapitel 5
„Maßnahmen-Hebel" (Z. 1098–1261, Abschnitte 5.1–5.1.3). Nachgemessen mit
`python3 -c "L=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read().split(chr(10));print(len(chr(10).join(L[450:833])),len(chr(10).join(L[1097:1261])))"`:
**32.841** Zeichen Kapitel 3 (ohne Überschriftszeile 32.836) und **11.759** Zeichen Kapitel 5
(11.304 nach Abzug des HTML-Pflichtinhalte-Kommentars). Die Abweichung von ein bis zwei Zeichen
gegenüber den im Ticket genannten 32.839 / 11.303 (Summe 44.142) rührt allein aus der Schnittkante
(Überschriftszeile, Leerzeile vor der nächsten Überschrift); der geprüfte Textkörper ist derselbe.
Ein nationaler 100-m-Vollraster-Lauf nach §3.4 war nicht verlangt und wurde **nicht** gefahren:
Alle Nachrechnungen laufen auf einzelnen Zellen und auf einer Kommune aus zwei bis drei Zellen.
Formelzeichen und Beispielblöcke der Kapitel 4 und 7 sind hier ausdrücklich **nicht** Gegenstand
(Kapitelgrenze; sie gehören zu den Geschwisterpaketen LF 7/8 bzw. LF 12).

#### 1.1 · Leitfragen dieses Pakets (§5) — einzeln mit Verdikt und Beleg

**LF 2 — Verteilschlüssel-Test: Kommune ohne Treiber > 0 möglich? (nachgerechnet statt gelesen).
Verdikt: Befund** (→ neuer Befund **23**; der Euro-Pfad selbst besteht).

*Lackmustest aus §3.4/§3.6, ausgeführt.* Gerechnet wurde eine Kommune ohne Flussaue mit drei
Zellen unterschiedlicher Wohnfläche (1.200 / 800 / 2.500 m²), unterschiedlichem Typmix
(θ_EFH = 1,0 / 0,0 / 0,5) und unterschiedlichen Tiefenprofilen, in allen drei HQ-Szenarien mit
\(a_{z,s} = 0\), mit der Kernformel §3.4 (Schritt 1–3), den Stützstellen
\(p = 10^{-1} / 10^{-2} / 2{,}236\cdot10^{-3}\,\text{a}^{-1}\) und den Wertsätzen 1.950 / 1.533
€₂₀₂₆/m² BGF · \(k_{\text{BGF}} = 1{,}30\). Ergebnis mit Zahlenwert:
\(\bar A_k = \mathbf{0{,}0}\) m²/a und \(\text{EAD}_k = \mathbf{0{,}00}\) €₂₀₂₆/a — exakt null,
in Fließkomma identisch 0.0, ohne Sonderregel und ohne Rest. Gegenprobe mit derselben Zelle bei
\(a = 0{,}8\): 18.879,9 €₂₀₂₆/a, der Nullwert ist also nicht durch einen Rechenfehler erzwungen.
Die Aggregation §3.6 ist die reine Summe über die Zellen (kein Gewicht, kein Skalar), und auch der
Niveau-Skalar \(\lambda\) aus §4.4 ist ein **multiplikativer** Faktor (§4.4 „Anwendungsregel"),
lässt die Null also Null. Der Bericht verteilt an keiner Stelle einen nationalen Betrag: Jeder
Rückgriff (Tiefen-Median, Typ-Mix) bildet sich aus den Zellen **derselben** Kommune (§3.2/§3.6),
und die einzigen nationalen Größen (ZÜRS-Band, GDV-Anker) treten als Prüfband bzw. Skalar auf,
nicht als Schlüssel. Der Euro-Pfad besteht LF 2 damit nachgerechnet.

*Der Befund liegt beim zweiten Ausweis desselben Kapitels.* Der Schicht-A-Index \(I_{60,k}\)
(§3.7) ist als Perzentilrang von \(x_k\) definiert, ohne Regel für den Massenpunkt \(x_k = 0\).
Nachgerechnet an einem Vergleichsraum aus 100 Kommunen, davon 60 ohne Aue (\(x_k = 0\)): Mit der
Leseart „Anteil der Kommunen mit kleinerem **oder gleichem** Wert" erhält eine Kommune ohne
Flussaue **60,0 Punkte** auf einer Skala, die im Produkt „Betroffenheit durch Flusshochwasser"
heißt; mit „echt kleiner" 0,0 Punkte. Der Lackmustest §3.4 deckt nur den Euro-Pfad ab →
**Befund 23**.

**LF 3 — Physische Zwischengröße. Verdikt: Befund** (→ neuer Befund **24**; die Rückführbarkeit
je Zelle selbst ist erfüllt).

*Erfüllt ist der Kern der Frage.* Jeder Euro-Betrag der Zelle ist auf eine physische Größe
rückführbar: §3.4 Schritt 1 erzeugt \(A_{z,s}\) in m² (schadensäquivalente Wohnfläche), Schritt 2
\(\bar A_z\) in m²/a, und erst Schritt 3 multipliziert mit dem Preis \(w_z\) in €₂₀₂₆/m². Die
Zwischengröße existiert unabhängig vom Preis und ist in §3.1 als „physischer Teil-Ausweis"
deklariert sowie in §3.6 als Teil-Ausweis 1 (\(\bar A_k\) in m²/a) und 2 (exponierte Wohnfläche je
Szenario in m²) nutzersichtbar. Nachgerechnet an der Beispielzelle: 15,0 / 77,76 / 300,0 m² je
Ereignis → 6,311 m²/a → 15.998 €₂₀₂₆/a bei \(w_z = 2.535\) €₂₀₂₆/m²; teilt man den Euro-Betrag
durch \(w_z\), kommt die physische Größe exakt zurück. Der Schicht-A-Index ist dimensionslos und
geht in keinen Euro-Pfad ein (§3.7), doppelt den Euro-Ausweis also nicht.

*Der Befund liegt bei der Klammer der Leitfrage („native Ausweise proportional zu den
Euro-Pfaden").* §3.1 schreibt die Beziehung indexfrei als \(\text{EAD} = \bar A \cdot w\), und
§3.5 führt \(\bar A\) ausdrücklich als Gattungszeichen für Zelle **und** Kommune. Auf der
deklarierten Betrachtungsebene Kommune gilt die Gleichung aber nur bei homogener Wertdichte.
Gegenbeispiel, gerechnet: Zelle 1 EFH (1.200 m², \(a\) = 0,25/0,80/1,00), Zelle 2 MFH (3.000 m²,
\(a\) = 0,00/0,10/0,20) ⇒ \(\bar A_k = 8{,}417\) m²/a, \(\text{EAD}_k = 20.195{,}7\) €₂₀₂₆/a als
Summe der Zellen, aber \(\bar A_k \cdot w_k = 18.077{,}9\) €₂₀₂₆/a mit der
wohnflächengewichteten Wertdichte der Kommune — **11,7 % Abweichung**. §3.6 rechnet richtig
(Summe der Zellprodukte); der eigene Beispielblock `beispiel_60_kernformel` prüft die
Vertauschbarkeit ausdrücklich nur „bei gleicher Wertdichte" → **Befund 24**.

**LF 11 — Form: Zeichentabellen vollständig, Beispiele rechnen auf (nachgerechnet statt gelesen).
Verdikt: Befund** (→ neuer Befund **25**; alle Beispielblöcke sind grün).

*Beispielblöcke der Kapitel 3 und 5 — alle vier ausgeführt, je Block Name und Ausgang:*

| Block | Abschnitt | Ausgang |
|---|---|---|
| `beispiel_60_kernformel_zelle` | 3.4 | **grün** — alle 10 Assertions erfüllt (d(0,405)=0,0503; Deckelung d(3,00)=d(4,00)=0,250; A = 15,0/77,76/300,0 m²; p₃ = 2,236·10⁻³; Ā = 6,311 m²/a; EAD = 15.998 ≈ 16.000 €₂₀₂₆/a; Lackmustest a = 0 → 0,0) |
| `beispiel_60_kernformel` | 3.6 | **grün** — Zelle → Kommune: Ā_k = 6,311 m²/a, EAD_k ≈ 16.000 €₂₀₂₆/a, zweite Zelle mit a = 0 trägt exakt 0, Linearitätsprobe und x_k = 0,48 erfüllt |
| `beispiel_60_s092_abschaetzung` | 5.1.2 | **grün** — r = 0,10·0,50·0,70 = 0,035; Band 0,0075–0,1056; Einzelachse Δq 0,0175–0,070 |
| `beispiel_60_s_bem_obergrenze` | 5.1.3 | **grün** — t₁ = 4,174, Summe 6,311, s_max = 0,661, Bandende 0,66 ≤ s_max, obere r-Grenze 0,1056 |

Ausgeführt mit dem Extraktor
`python3 -c "import re;L=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read().split(chr(10));n=[exec(m.group(2),{}) for kap in (chr(10).join(L[450:833]),chr(10).join(L[1097:1261])) for m in re.finditer(r'\x60\x60\x60python test: (\S+)'+chr(10)+r'(.*?)\x60\x60\x60',kap,re.S)];print(len(n),'Bloecke gruen')"`
(Ausgabe: `4 Bloecke gruen`) — kein Block rot, keine Divergenz zwischen den im Fließtext genannten Zahlen (15,0/77,8/300,0 m²;
6,31 m²/a; ≈ 16.000 €₂₀₂₆/a; −3,5 %; 0,661) und den Rechenwerten.

*Der Befund liegt bei der Vollständigkeit der Zeichentabellen.* §3.5 beansprucht wörtlich, **jedes**
Formelzeichen der Kapitel 3 und 5 zu führen. Der maschinelle Abgleich aller in Kapitel 3 und 5
außerhalb der Codeblöcke gesetzten Mathe-Token gegen die Tabellen §3.5 und §5.1.1 findet vier
Zeichen, die in Kapitel 5 vorkommen und in keiner der beiden Tabellen stehen: \(q_0\) (Z. 1162)
sowie \(t_1\), \(t_2\), \(t_3\) (Z. 1205–1208). Bei \(t_i\) kommt eine Zeichenkollision hinzu:
§3.5 führt \(t\) als „Laufindex des Gebäudetyps (EFH/ZFH, MFH)", in §5.1.3 bezeichnet \(t_1\) einen
Szenariobeitrag zum Erwartungsschaden in m²/a → **Befund 25**. Alle übrigen Token der Prüfung
(\(W_z, W_k, a_{z,s}, h_{z,s}, d, d_1, d_5, h_1, h_5, f_{S093}, f_{S094}, A_{z,s}, \bar A, p_i, T,
\theta_{z,t}, n_t, k_{\text{BGF}}, w_z, \text{EAD}, \text{EAD}_{\text{mit}}, r_{\text{S092}},
\Delta q, s_{\text{bem}}, e_{\text{bem}}, x_k, I_{60,k}\) sowie die Laufindizes \(z, k, s, i, t, n\))
stehen mit Bedeutung, Einheit und Herkunft in §3.5; die Indexvarianten \(A_{z,i}\), \(A_{z,n}\),
\(p_{i+1}\) sind über die Zeilen zu \(A_{z,s}\), \(p_i\), \(i\) und \(n\) gedeckt.

**LF 13 — Herleitungspflicht (ein einziges Formelzeichen ohne abgeschlossene Herleitung = Befund).
Verdikt: Befund** (→ neuer Befund **26**).

*Geprüft wurde jede Herkunftsangabe der Zeichentabellen §3.5 und §5.1.1 auf eine im Bericht
abgeschlossene Herleitung, nicht auf einen bloßen Verweis.* Belegt und mit Registerzeile versehen
sind \(W_z, a_{z,s}, h_{z,s}, d_1, d_5, f_{S093}, f_{S094}, \theta_{z,t}, n_t, p_1, p_2\).
Ausgeschrieben hergeleitet und nach §3.9/P1 als Abschätzung von KAP3 gekennzeichnet sind
\(d(h)\) samt Gültigkeitsbereich 0,10–1,75 m und Deckelung (§3.3), \(h_1\)/\(h_5\) (§3.3),
\(p_3\) als geometrisches Mittel 2,236·10⁻³ a⁻¹ (§3.4 Schritt 2), \(k_{\text{BGF}} = 1{,}30\)
(§3.4 Schritt 3), \(A_{z,s}\), \(\bar A\), \(w_z\), \(\text{EAD}\), \(x_k\), \(I_{60,k}\) sowie
die S092-Kette \(\Delta q\), \(e_{\text{bem}}\), \(r_{\text{S092}}\) (§5.1.2, je mit Wert, Band
und Richtung — P2 ist für 60-S092-01 damit im Bericht bedient, die Wirkung steht nicht auf null).
Keine dieser Herleitungen steht nur als Code-Kommentar; die Beispielblöcke wiederholen sie
lediglich. Auch \(q_0\) ist trotz fehlender Tabellenzeile sachlich abgeschlossen behandelt (§4.7:
„geparkt (Datenquelle fehlt) — nicht gesetzt, nicht geschätzt").

*Der Befund liegt bei \(s_{\text{bem}}\) und der aus ihm abgeleiteten Kappung.* §5.1.3 leitet die
Obergrenze der Näherung als \(t_1/(t_1+t_2+t_3) = 4{,}174/6{,}311 = 0{,}661\) her und nennt sie
eine **harte** Obergrenze; das Band von \(s_{\text{bem}}\) (0,30–0,66), das Band von
\(r_{\text{S092}}\) (0,0075–0,1056), der Parameter-Block `flood_bldg.s_bem` und die
Einzelachsen-Sensitivität hängen daran. Nachgerechnet: Diese Zahlen entstehen aus **genau einer
Beispielzelle** (A = 15,0 / 77,76 / 300,0 m² aus §3.4), nicht aus einer allgemeinen Eigenschaft
der Formel. Für andere Zellprofile ergibt derselbe Ausdruck 0,856 (Zelle durchgehend in der Aue,
a = 1,0 in allen Szenarien), 0,323 (Auenrand, a = 0,02/0,20/1,00) und 0,000 (nur im Extremfall
betroffen) — die Spanne 0,00…0,86 überschreitet die als „hart" ausgewiesene Grenze deutlich nach
oben. Zusätzlich trifft der Quellenverweis nicht: Die im Text genannten „Zahlen aus Abschnitt 4.5"
stehen dort nicht (§4.5 führt nur die Anteile 66,1 / 23,2 / 10,6 %, die aus derselben
Beispielzelle stammen); die Zeichenfolgen `t_1`, `t_2`, `t_3` kommen in §4.5 null mal vor. Die
Herleitung der Kappung ist damit nicht abgeschlossen → **Befund 26**.

#### 1.2 · Neue Befunde dieses Pakets (23–26)

Format §5: Stelle · Art (Lücke/Fehler/Widerspruch) · Begründung · Vorschlag · Kategorie. Das
Ledger trug bei Ticketschnitt die Nummern 1–19; das vorlaufende Paket T-0270 hat inzwischen 20–22
vergeben, die nächsthöhere freie Nummer ist deshalb **23** (Regel „fortlaufend ab der nächsthöheren
freien Nummer"). **Dieses Paket behebt keinen Befund** — weder einen neuen noch einen alten. Die
Kurzform-Tabelle „Offene Befunde" am Kopf des Ledgers ist bewusst nicht angefasst; sie schreibt
die Befund-Regression dieser Runde fort.

| Nr | Kat. | Befund (Stelle · Art · Begründung · Vorschlag) | Prüfausdruck | Status |
|---|---|---|---|---|
| 23 | B | Bericht §3.7 „Schicht-A-Index" (Z. 799–832), Formel \(I_{60,k} = 100 \cdot \operatorname{Perzentilrang}(x_k)\) · **Lücke (§5 LF 2 Verteilschlüssel-Test; §3.6 nutzersichtbarer Ausweis)** — für den Euro-Pfad ist der Lackmustest „Kommune ohne Flussaue" in §3.4/§3.6 erfüllt und nachgerechnet (\(\text{EAD}_k = 0{,}00\) €₂₀₂₆/a). Der zweite, ebenfalls nutzersichtbare Ausweis desselben Kapitels kennt jedoch keine Regel für den Massenpunkt \(x_k = 0\): Da alle Kommunen ohne Aue denselben Wert 0 tragen, hängt ihr Indexwert allein an der ungenannten Bindungsregel des Perzentilrangs. Nachgerechnet an 100 Kommunen, davon 60 mit \(x_k = 0\): Leseart „kleiner oder gleich" ⇒ **60,0 Punkte**, Leseart „echt kleiner" ⇒ 0,0 Punkte — dieselbe auenlose Kommune erhält also entweder gar keine oder eine mittlere „Betroffenheit durch Flusshochwasser". §3.7 nennt zwar den Vergleichsraum als Pflichtangabe, nicht aber die Bindungsregel und keinen Nullanker. **Vorschlag:** in §3.7 festschreiben, dass Kommunen mit \(x_k = 0\) den Indexwert 0 erhalten und der Perzentilrang nur über die Kommunen mit \(x_k > 0\) gebildet wird (oder ausdrücklich die Leseart „echt kleiner" mit Nullanker), und den Lackmustest §3.4 um den Schicht-A-Ausweis erweitern. | `python3 -c "s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();L=s.split(chr(10));k=chr(10).join(L[798:833]);raise SystemExit(0 if ('Perzentilrang' in k and 'Bindung' not in k and 'x_k = 0' not in k) else 1)"` | offen |
| 24 | C | Bericht §3.1, Aufzählungspunkt „Physischer Teil-Ausweis" (Z. 473–476: „\(\text{EAD} = \bar A \cdot w\)") zusammen mit der Gattungszeichen-Zeile zu \(\bar A\) in §3.5 (Z. 685) gegen §3.6 (Z. 707) · **Fehler (§5 LF 3 „native Ausweise proportional zu den Euro-Pfaden"; §3.6 Ausweis auf der deklarierten Betrachtungsebene)** — die indexfreie Gleichung gilt exakt auf der **Zelle**; auf der deklarierten Betrachtungsebene Kommune ist \(\text{EAD}_k = \sum_z \bar A_z w_z\) und damit nur bei homogener Wertdichte gleich \(\bar A_k \cdot w_k\). Gegenbeispiel (gerechnet): EFH-Zelle 1.200 m² mit \(a\) = 0,25/0,80/1,00 und MFH-Zelle 3.000 m² mit \(a\) = 0,00/0,10/0,20 ⇒ \(\text{EAD}_k = 20.195{,}7\) €₂₀₂₆/a, \(\bar A_k \cdot w_k = 18.077{,}9\) €₂₀₂₆/a, **11,7 % Abweichung**. §3.6 rechnet korrekt, und der Beispielblock `beispiel_60_kernformel` prüft die Vertauschbarkeit ausdrücklich nur bei gleicher Wertdichte — die Lücke ist die verallgemeinernde Schreibweise in §3.1/§3.5, aus der ein Nutzer den kommunalen physischen Teil-Ausweis \(\bar A_k\) fälschlich als proportional zum Euro-Ausweis liest. **Vorschlag:** in §3.1 und in der \(\bar A\)-Zeile von §3.5 die Gleichung auf die Zelle indizieren (\(\text{EAD}_z = \bar A_z w_z\)) und für die Kommune auf die Summe in §3.6 verweisen; im Teil-Ausweis 1 vermerken, dass \(\bar A_k\) und \(\text{EAD}_k\) bei gemischtem Gebäudetyp nicht proportional sind. | `python3 -c "p=[1e-1,1e-2,(5e-3*1e-3)**0.5];ab=lambda A: sum((p[i]-p[i+1])*(A[i]+A[i+1])/2 for i in range(2))+p[2]*A[2];A1=ab([1200*0.25*0.050,1200*0.80*0.081,1200*1.00*0.250]);A2=ab([0.0,3000*0.10*0.081,3000*0.20*0.250]);E=A1*1.30*1950+A2*1.30*1533;wk=1.30*(1200*1950+3000*1533)/4200;raise SystemExit(0 if abs(E-(A1+A2)*wk)/E > 0.05 else 1)"` | offen |
| 25 | C | Bericht §3.5 „Zeichentabelle (alle Formelzeichen der Kapitel 3 und 5)" (Z. 660–699) und §5.1.1 (Z. 1132–1139) gegen §5.1.2 Z. 1162 und §5.1.3 Z. 1205–1208 · **Lücke (§5 LF 11 „Zeichentabellen vollständig"; §7 Lint „jede Zeichentabellen-Zeile mit Wert und Herkunft")** — §3.5 beansprucht wörtlich, jedes Formelzeichen der Kapitel 3 und 5 zu führen, lässt aber vier in Kapitel 5 verwendete Zeichen aus: \(q_0\) (heutiger Objektschutz-Anteil, in §5.1.2 als Bezug des Doppelzählungs-Wächters genannt, hergeleitet erst in §4.7 als „geparkt") sowie \(t_1\), \(t_2\), \(t_3\) (Szenariobeiträge zum Erwartungsschaden in m²/a, §5.1.3). Bei \(t_i\) kommt eine **Zeichenkollision** hinzu: §3.5 vergibt \(t\) als Laufindex des Gebäudetyps (EFH/ZFH, MFH), \(n_t\) und \(\theta_{z,t}\) tragen diesen Index — \(t_1\) liest sich damit als „Gebäudetyp 1" statt als Szenariobeitrag. Dass der Lint 115 Checks grün meldet, zeigt zugleich die Reichweitengrenze der maschinellen Prüfung (vgl. Befund 17): Er prüft vorhandene Tabellenzeilen, nicht fehlende. **Vorschlag:** vier Zeilen in §3.5 ergänzen — \(q_0\) mit Herkunft „§4.7, geparkt (Datenquelle fehlt)" und \(t_1\)…\(t_3\) mit Einheit m²/a und Herkunft §5.1.3 — und die Szenariobeiträge umbenennen (z. B. \(\tau_i\) oder \(\bar A^{(i)}\)), damit der Laufindex \(t\) eindeutig bleibt. | `python3 -c "s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();L=s.split(chr(10));t35=chr(10).join(L[669:700]);t511=chr(10).join(L[1131:1140]);k5=chr(10).join(L[1097:1261]);fehlt=[z for z in ('q_0','t_1','t_2','t_3') if z in k5 and z not in t35 and z not in t511];raise SystemExit(0 if fehlt else 1)"` | offen |
| 26 | B | Bericht §5.1.3 „\(s_{\text{bem}}\) — ausgewiesene Näherung mit Richtung", Absätze „Obergrenze aus der Szenario-Zerlegung (Zahlen aus Abschnitt 4.5)" und „Folge für das Band" (Z. 1204–1222) · **Fehler/Lücke (§5 LF 13 Herleitungspflicht; §3.9 „kein Formelzeichen ohne Herleitung"; §3.2 empirische Quantile)** — die als **harte** Obergrenze ausgewiesene Grenze \(s_{\text{bem}} \le 0{,}661\) und die daraus gezogene Kappung des Bandes auf 0,66 sind aus **genau einer Beispielzelle** gerechnet (A = 15,0 / 77,76 / 300,0 m² aus §3.4), nicht aus einer allgemeinen Eigenschaft der Formel. Derselbe Ausdruck liefert für andere Zellprofile 0,856 (a = 1,0 in allen Szenarien), 0,323 (Auenrand a = 0,02/0,20/1,00) und 0,000 (nur im Extremfall betroffen); die Grenze ist also zell- und kommunenabhängig und wird von realistischen Profilen überschritten. Daran hängen das Band von \(s_{\text{bem}}\) (0,30–0,66), das Band von \(r_{\text{S092}}\) (0,0075–0,1056), der Parameter-Block `flood_bldg.s_bem`, die Einzelachsen-Sensitivität und die Schließung von Befund 10. Hinzu kommt ein nicht tragender Quellenverweis: „Zahlen aus Abschnitt 4.5" — dort stehen die Werte \(t_1\)/\(t_2\)/\(t_3\) nicht (nur die Anteile 66,1 / 23,2 / 10,6 %, aus derselben Beispielzelle abgeleitet), die Zeichenfolge `t_1` kommt in §4.5 null mal vor. **Vorschlag:** die Obergrenze entweder allgemein herleiten (Supremum des Ausdrucks über zulässige \(a\)-/\(h\)-Profile bei gegebenen Jährlichkeiten — es liegt oberhalb 0,86 und trägt die Kappung auf 0,66 nicht) oder sie ausdrücklich als **profilabhängige Illustration** kennzeichnen und das Band von \(s_{\text{bem}}\) mit einer anderen, tragenden Begründung setzen; in beiden Fällen den Verweis auf §4.5 durch die tatsächliche Fundstelle (Beispielzelle §3.4/§3.6) ersetzen. Nach P1/P2 bleibt der Wert eine ausgewiesene Abschätzung — die Wirkung wird nicht auf null gesetzt, nur ihre Bandgrenze braucht eine tragende Herleitung. | `python3 -c "p=[1e-1,1e-2,(5e-3*1e-3)**0.5];sm=lambda A: ((p[0]-p[1])*(A[0]+A[1])/2)/((p[0]-p[1])*(A[0]+A[1])/2+(p[1]-p[2])*(A[1]+A[2])/2+p[2]*A[2]);a=sm([15.0,77.76,300.0]);b=sm([1200*0.081,1200*0.250,1200*0.250]);c=sm([0.0,0.0,300.0]);raise SystemExit(0 if abs(a-0.661)<5e-4 and b>0.70 and c==0.0 else 1)"` | offen |

#### 1.3 · Abgrenzung und Status dieses Pakets

- **Beantwortet:** LF 2 (Verdikt Befund), LF 3 (Verdikt Befund), LF 11 (Verdikt Befund) und
  LF 13 (Verdikt Befund) — jede mit Beleg. Nachgerechnet statt gelesen: LF 2 (Lackmustest
  „Kommune ohne Flussaue", \(a = 0\), Ergebnis \(\text{EAD}_k = 0{,}00\) €₂₀₂₆/a) und LF 11 (alle
  vier Beispielblöcke der Kapitel 3 und 5 ausgeführt, je Block Name und Ausgang in der Tabelle
  oben, 4 von 4 grün).
- **Nicht Gegenstand dieses Pakets:** die Formelzeichen und Beispielblöcke der Kapitel 4 und 7
  (Geschwisterpakete LF 7/8 und LF 12), die übrigen Leitfragen und die Regression der Befunde
  1–19. Ein nationaler 100-m-Vollraster-Lauf nach §3.4 war nicht verlangt und wurde nicht
  gefahren.
- **Kein Befund behoben**, kein Bericht, kein Register, kein Code, kein Lint geändert:
  `docs/methodik/60_gebaeudeschaeden_flusshochwasser.md` und `docs/evidenz/register.md` sind
  byte-gleich geblieben; `backend/scripts/lint_methodik.py` wurde in diesem Paket nicht einmal
  ausgeführt (Ausgabe aus Abschnitt 0.1 übernommen).
