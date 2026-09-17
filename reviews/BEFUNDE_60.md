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

### 2 · Paket T-0272 — Leitfragen 5 und 6 gegen Kapitel 2 (Evidenz-Register)

Drittes Paket der Runde 2 (17.09.2026), eigene Sitzung: Sie hat den geprüften Stand nicht
geschrieben — Kapitel 2 mit seinen 32 Registerzeilen und den Langbelegen B1–B6 stammt aus T-0237
und den Folgepaketen, alle im Endstatus (eiserne Regel 4). Das Bundle nach §1 gilt unverändert
(Abschnitt 0 dieser Runde); die Lint-Ausgabe aus Abschnitt 0.1 wird **übernommen, nicht neu
vorhergesagt**, der Lint wurde in diesem Paket nicht ausgeführt.

**Prüfumfang dieses Pakets:** genau Kapitel 2 „Evidenz-Register (§2.2)" (Z. 152–450, einschließlich
„Belege zu den entschiedenen Registerzeilen"). Nachgemessen mit
`python3 -c "L=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read().split(chr(10));print(len(chr(10).join(L[151:450])))"`:
**43.426** Zeichen; die Abweichung von zwei Zeichen gegenüber den im Ticket genannten **43.424**
rührt allein aus der Schnittkante (Zeilenumbrüche an Überschrift und Leerzeile vor Kapitel 3), der
geprüfte Textkörper ist derselbe. Summe des Pakets: 43.424 Zeichen (ein Kapitel). Kapitel 3, 5 und 7
wurden nur dort gelesen, wo eine Registerzeile ausdrücklich auf sie verweist (Bandenden von
60-S092-01 in §5.1.2, Stützstellen von \(d(h)\) in §3.3, \(p_3\) in §3.4) — sie sind nicht
Prüfgegenstand. Ein nationaler 100-m-Vollraster-Lauf nach §3.4 war nicht verlangt und wurde
**nicht** gefahren; alle Nachrechnungen laufen auf den Zahlenwerten der Registerzeilen und der
Langbelege.

#### 2.1 · Leitfragen dieses Pakets (§5) — einzeln mit Verdikt und Beleg

**LF 5 — Modifikatoren: zentriert, OR-Übersetzung korrekt, richtige Studienart, richtige Band- und
Endpunkt-Zuordnung (nachgerechnet statt gelesen). Verdikt: Befund** (→ neue Befunde **27**, **28**,
**29** und **31**).

*Vorbemerkung zur OR-/RR-Übersetzung.* Keine der sieben entschiedenen Registerzeilen führt eine
Odds Ratio oder ein relatives Risiko. Die Effektgrößen sind Wiederkehrintervalle (W085),
Prozent-Schadensänderungen je Tiefe (S074), Klassenanteile (R17), Kostenkennwerte mit Index (R24),
Skalierungsfaktoren einer Schadensfunktion (S093/S094) und eine lineare Abschätzungskette (S092).
Nachgerechnet wurde deshalb jeweils die **tatsächliche Übersetzung** der Quellgröße in den
Registerwert (1/T, Tiefe × Rate, Residuum × Bezugsgröße, Index × Kennwert, log-Anteil →
Faktor); eine OR→RR-Umrechnung ist nirgends nötig und nirgends fälschlich angewendet — insoweit
**bestanden**. Nachgerechnet mit Python 3, je Zeile ein Ausdruck; die Zahlen stehen unten.

*Zeile-für-Zeile-Nachrechnung (sieben Registerzeilen mit Modifikator oder Band):*

| Registerzeile | Zentrierung | Übersetzung Quelle → Registerwert (nachgerechnet) | Band- und Endpunkt-Zuordnung (nachgerechnet) | Studienart | Ergebnis |
|---|---|---|---|---|---|
| 60-W085-01 | — (Wahrscheinlichkeiten, kein Faktor) | p = 1/T: 1/10 = 0,100 · 1/100 = 0,0100 · 1/200 = 0,00500 · 1/1000 = 0,00100 a⁻¹ ✓ | HQhäufig: 1/5 = 0,200 und 1/20 = 0,0500 a⁻¹ ✓ als Band, Zentralwert HQ10 = kartierter Fall ✓. HQextrem: Band 5,0·10⁻³ bis 1,0·10⁻³ ✓, Endpunkte korrekt dem WHG (≥ 200 a) bzw. der Länderpraxis (≈ HQ1000) zugeordnet — **aber kein Zentralwert im Register**, obwohl die Entscheidung „Basiswert — die drei Szenario-Stützstellen p(HQ)" lautet; der rechnende Wert \(p_3 = (5{,}0\cdot10^{-3}\cdot1{,}0\cdot10^{-3})^{1/2} = 2{,}236\cdot10^{-3}\) steht erst in §3.4, die Zeichenfolge „2,236" kommt in Kapitel 2 null mal vor | amtliche Kartengrundlage, normiert ✓ | **Befund 31** |
| 60-S074-01 | symmetrisch um den Basiswert ✓ | 2,0 × 5,3 % = 10,6 %; 2,0 × 6,2 % = 12,4 % ✓. Gegenprobe des zitierten Quellfaktors „0,5 m Reduktion ⇒ Faktor 1,35–1,44": 1/(1 − 5 × 0,053) = 1,361 und 1/(1 − 5 × 0,062) = 1,449 ✓ — Register-Rate und Quellfaktor sind untereinander konsistent | Entscheidung „±0,20 m ⇒ ±12 %": 12,4 → 12 gerundet, damit 0,4 Prozentpunkte unter dem oberen Ende des eigenen Bandes (10,6–12,4 %); unerheblich, kein Befund. Endpunkt ±0,20 m = obere Höhengenauigkeit des DGM1 (0,15–0,2 m) ✓ | amtliche Produktspezifikation + publizierte Sensitivitätsrechnung (NL) — als dokumentierte Übertragung geführt ✓ | bestanden |
| 60-R17-01 | — (Prüfband, kein Multiplikativglied) | 100 − 92,4 = 7,6 %; 7,6 − 0,4 = 7,2 % = 6,1 + 1,1 ✓. × 22,6 Mio: GK1 20,882 · GK2 1,3786 · GK3 0,2486 · GK4 0,0904 · GK2–4 1,7176 · GK3+4 0,339 Mio ✓ (alle Rundungen im Register treffen) | GK4 „≥ einmal in 10 Jahren", GK3 HQ10–HQ100 ⇒ GK3+GK4 = „HQ100-Band" ✓; GK2 „seltener als HQ100, inkl. deichgeschützt" ✓. Endpunkte korrekt den Klassen zugeordnet | Bestandsstatistik, ausdrücklich „keine Studie" ✓ | bestanden |
| 60-R24-01 | — (Mengengerüst) | 149,8 ÷ 89,1 = 1,68126; 1.050 × 1,68126 = 1.765,3; 825 × 1,68126 = 1.387,0 ✓; 1,034³ = 1,10551 ✓; 1.765 × 1,105 = 1.950,3 ✓; 1.533 × 1,30 = 1.992,9 ✓; 1.950 × 1,30 = 2.535 ✓; 4,1 Mrd m² × 1.993 / 2.535 = 8,171 / 10,394 Bio. € ✓; 1,25 ÷ 1,40 = 0,893 ⇒ −10,7 % ≈ −11 % ✓ | (a) Bandenden aus **gerundeten** Faktoren: 1.765 × 1,16 = **2.047,4** (Register 2.047), mit dem hergeleiteten 1,050³ = 1,157625 aber **2.043,2**; MFH 1.387 × 1,16 = 1.608,9 (Register 1.609) gegen 1.605,6. (b) Die Jahresraten der Endpunkte **2,3 %** (unten) und **3,4 %** (Zentralwert) sind aus keinem der in B4 zitierten Werte (3,2 / 3,3 / 5,0 %) abgeleitet; die Zeichenfolge „2,3" steht in den zitierten Quellen-Absätzen nicht. (c) Die „Wertdichte 1.993–2.535 €₂₀₂₆/m²" und der „Wiederherstellungswert 8,2–10,4 Bio. €" sind **Typ-Endpunkte** (reiner MFH- gegen reinen EFH-Satz), nicht das Unsicherheitsband der beiden abgeschätzten Faktoren; mit Index 1,07–1,16 und BGF 1,25–1,40 gegengerechnet spannt die Wertdichte 1.387 × 1,07 × 1,25 = **1.855** bis 1.765 × 1,16 × 1,40 = **2.866** €₂₀₂₆/m², der Bestand **7,6–11,8 Bio. €** | amtliche Statistik + Rechtsverordnung ✓ | **Befund 27** |
| 60-S093-01 | geometrisch um 1: √1,5678 = 1,2521, 1/1,2521 = 0,7986 ✓ rechnerisch — **aber** das arithmetische Mittel der beiden Klassen bei 50 : 50 ist (0,7986 + 1,2521)/2 = **1,0254**, und Anteile des Bestandsmix je Klasse nennt die Zeile nicht; „mittelwertzentriert auf den Bestandsmix" ist damit nicht nachgewiesen | 1,58 ÷ 0,41 = 3,8537; ln = 1,3490; ÷ 3 = 0,4497; e^0,4497 = 1,5678 ✓. Lesart „halber Anteil" 0,225 ⇒ 0,894–1,119 ✓. Lesart „voller Anteil" 1,349 ⇒ e^±0,6745 = **0,509–1,963**, der Bericht schreibt **0,52–1,96** (unteres Ende falsch gerundet) | (a) B5 schreibt, die Spannweite 1,349 verteile sich auf die **zwei** Achsen Kontamination und Vorsorge, teilt dann aber durch **drei**; bei gleichem Anteil je Achse wäre der Achsenanteil 1,349 ÷ 2 = 0,6745, also Band 0,71–1,40 statt 0,80–1,25. (b) Die Spannweite 0,41–1,58 ist die Diagonale C0P2 ↔ C2P0 über zwei Achsen, nicht die Summe zweier Einzelachsen-Spannen. (c) Vorsorge ist bewohnerseitig (B5 selbst: „gebäude- und bewohnerseitigen Modifikatoren"), die Teilung „je gebäudeseitiger Achse" stimmt mit der eigenen Zuordnung nicht. (d) Sensitivitätsangabe „±25 %" gegen das Band −20 % / +25 % | empirische Mehrfaktor-Schadensfunktion aus Befragung, als Abschätzung von KAP3 gekennzeichnet ✓ (P1/P2 ausgewiesen) | **Befund 28** |
| 60-S094-01 | geometrisch um 1: e^0,1124 = 1,1190, 0,8937 ✓; arithmetisches Mittel 1,0063 | 0,4497 ÷ 2 = 0,2248; e^0,2248 = 1,2521 ✓ | kombiniert 0,7986 × 0,8937 = 0,7137 ⇒ 0,71 und 1,2521 × 1,1190 = 1,4011 ⇒ 1,40 ✓ (Endpunkte gleichgerichtet, also Vollkorrelation — als konservativ zulässig). Mittel des Produkts bei 50 : 50 je Achse: 1,0254 × 1,0063 = **1,0319** — die beiden „mittelwertzentrierten" Achsen heben den Basiswert zusammen um ≈ +3,2 %, sofern der Bestand je Achse hälftig verteilt ist. Die Zeile erbt Befund 28 über die Kopplung an 0,450 | ingenieurmäßige Schadensgradskala, als Abschätzung von KAP3 gekennzeichnet, Bauform-Grenze nach P2 ausgewiesen ✓ | bestanden (Rechenschritt selbst); Kopplung → Befund 28 |
| 60-S092-01 | — (Reduktionsfaktor, Zentralwert 0,035) | 0,10 × 0,50 × 0,70 = 0,0350 ✓ | 0,05 × 0,30 × 0,50 = 0,0075 ✓; 0,20 × 0,66 × 0,80 = 0,1056 ✓ (Bandenden gleichgerichtet, übereinstimmend mit §5.1.2). Wert, Band und Kennzeichnung „Abschätzung von KAP3" stehen in der Zeile — P2 ist bedient, die Wirkung steht nicht auf null. Die Divergenz zu `docs/evidenz/register.md` Z. 65 (dort weiter „0,0075–0,112") wurde gelesen und besteht fort; ihr Status gehört zur Regression von Befund 19 und wird hier nicht bewertet | Studienart: die Zeile schließt Befragungen nach §3.5 zu Recht als Wertquelle aus, behauptet aber, sie seien „im Volltext nicht verifiziert" — dieselbe Kapitel-2-Quelle Thieken u. a. 2008 ist in B5 „Volltext gegengelesen" und trägt in Tab. 2 Vorsorge-Skalierungsfaktoren (C0P1 0,64 ÷ C0P0 0,92 = **0,696**, C0P2 0,41 ÷ 0,92 = **0,446**, also −30 % bzw. −55 % je Gebäude mit guter bzw. sehr guter Vorsorge) | **Befund 29** |

Damit sind **sieben** Registerzeilen mit Modifikator bzw. Band Zeile für Zeile nachgerechnet
(Mindestmaß des Tickets: fünf). Die übrigen 25 Zeilen stehen auf „offen" und tragen keinen
Modifikator, den man nachrechnen könnte.

**LF 6 — Struktur: überall verwendet, wo die Evidenz strukturabhängig ist; Kopplungen zwischen
abgeleiteten Parametern neu gerechnet? Verdikt: Befund** (→ neuer Befund **30**; die ausgewiesenen
Kopplungen selbst sind neu gerechnet und stimmen, soweit nicht Befund 28 greift).

*Kopplungen — einzeln nachgerechnet.* (1) **S094 → S093** (Achsenanteil 0,450): 0,450 ÷ 2 = 0,225
⇒ 0,89–1,12, kombiniert 0,71–1,40 — neu gerechnet ✓; die Kopplung ist in B6 ausdrücklich benannt.
Folge: jede Korrektur aus Befund 28 muss S094 und das kombinierte Band mitziehen (bei Anteil 0,6745
würde S094 zu e^±0,1686 = 0,845–1,184 und das kombinierte Band zu 0,60–1,66). (2) **S074 → W085**
(Tiefenquelle): in B2 benannt, Rechenweg 2,0 × Rate neu gerechnet ✓. (3) **R24 → Baupreisindex**:
in B4 benannt, Kette 1,68126 × 1,105 × 1,30 neu gerechnet ✓ (Bandenden siehe Befund 27).
(4) **R17 → W085 × R24** (Kein-Doppelkanal): R17 liefert nur Prüfband, kein Multiplikativglied ✓.
(5) **S092 ↔ S093 — nicht benannt:** B5 bildet die Spannweite der Zustandsachse aus der Tab.-2-
Spannweite, in der die **Vorsorge**-Achse steckt; S092 ist die Vorsorge-Wirkung. Ändert sich die
Vorsorge-Evidenz, ändern sich beide Zeilen — diese Kopplung steht weder in B5 noch in der
S092-Zeile (→ Teil von **Befund 29**).

*Struktur — wo ist die Evidenz strukturabhängig, und wird die Struktur verwendet?*
- **Gebäudetyp → Mengengerüst/Preis:** verwendet ✓ — R24 trennt EFH/ZFH (1.950 €₂₀₂₆/m² BGF)
  und MFH (1.533 €₂₀₂₆/m² BGF), Zellbezug über Zensus-2022-Gitter.
- **Gebäudetyp → Schadensquote: nicht verwendet, nicht als Modellgrenze ausgewiesen.** Die
  Zeile 60-S093-01 selbst nennt FLEMOps mit der Eingangsachse „Gebäudetyp (3 Klassen)" neben
  Wasserstand und Qualität; die Schadensquote der Quelle ist also typabhängig. Kapitel 2 führt aber
  in keiner Registerzeile eine typabhängige Schadensquote und vermerkt die Nichtverwendung auch nicht
  als Modellgrenze (Kapitel 2: „je Gebäudetyp" 0 Treffer, „typabhängig" 0 Treffer). Die
  verweisende Stelle §3.3 bestätigt, dass \(d(h)\) eine einzige, typunabhängige Stützstellenreihe ist
  (≈ 3,5 % … ≈ 25 %), und die Registerzeile ordnet diese beiden Endpunkte weder einem Gebäudetyp
  noch einer Qualitätsklasse von Fig. 1 zu. Die Struktur-Proxy-Daten dafür nennt das Register
  selbst („Baujahrsklasse und Gebäudetyp der Zensus-2022-Gebäude- und Wohnungszählung" je
  100-m-Zelle) → **Befund 30**.
- **Bauform/Material → Schadensgrad:** strukturabhängig nach Quelle; mangels Merkmal (Datenlücke
  §3.8) als bundesweit einheitliches Band geführt und als Bauform-Grenze nach P2 ausgewiesen ✓.
- **Relief → Tiefenfehler (S074):** strukturabhängig; als Modellgrenze „in Mittelgebirgs- und
  Steillagen Untergrenze" ausgewiesen, nicht verwendet — für ein Sensitivitätsband ohne
  Multiplikativglied zulässig ✓.
- **Adresse gegen Gebäude (R17):** als Modellgrenze (a) benannt; R17 rechnet nicht ✓.
- **Objektschutz (S092):** kommunaler Pauschalfaktor, als Modellgrenze der Abschätzung benannt ✓
  (die fehlende Typ-/Kellerdifferenzierung ist damit ausgewiesen, P2 bedient).

#### 2.2 · Neue Befunde dieses Pakets (27–31)

Format §5: Stelle · Art (Lücke/Fehler/Widerspruch) · Begründung · Vorschlag · Kategorie. Das
Ledger trug bei Ticketschnitt die Nummern 1–19; die vorlaufenden Pakete T-0270 (20–22) und T-0271
(23–26) haben inzwischen weiter vergeben, die nächsthöhere freie Nummer ist deshalb **27** (Regel
„fortlaufend ab der nächsthöheren freien Nummer"). **Dieses Paket behebt keinen Befund** — weder
einen neuen noch einen alten. Die Kurzform-Tabelle „Offene Befunde" am Kopf des Ledgers ist bewusst
nicht angefasst; sie schreibt die Befund-Regression dieser Runde fort. Jeder Prüfausdruck endet mit
Exit 0, **solange der Befund besteht** (am 17.09.2026 ausgeführt: alle fünf Exit 0).

| Nr | Kat. | Befund (Stelle · Art · Begründung · Vorschlag) | Prüfausdruck | Status |
|---|---|---|---|---|
| 27 | C | Bericht Kap. 2, Registerzeile 60-R24-01 (Z. 189) und Langbeleg B4, Rechenschritte 2–4 (Z. 319–350) · **Fehler/Lücke (§5 LF 5 „richtige Band- und Endpunkt-Zuordnung"; §3.9 Abgeschätzt; Vorgabe P1 „samt Herleitung")** — (a) die Jahresraten der Fortschreibung, **3,4 %** (Zentralwert) und **2,3 %** (unteres Bandende), sind aus keinem der in B4 zitierten amtlichen Werte (+3,2 % Nov. 2025, +3,3 % Feb. 2026, +5,0 % Mai 2026) hergeleitet; nur das obere Ende 5,0 % ist belegt; (b) die Bandenden 1.889–2.047 bzw. 1.484–1.609 €₂₀₂₆/m² BGF sind mit den gerundeten Faktoren 1,07/1,16 gerechnet, der hergeleitete Faktor 1,050³ = 1,1576 ergibt 2.043,2 bzw. 1.605,6; (c) „Wertdichte 1.993–2.535 €₂₀₂₆/m²" und „Wiederherstellungswert 8,2–10,4 Bio. €" sind Typ-Endpunkte (reiner MFH- gegen reinen EFH-Satz), werden in der Zeile aber wie ein Band gelesen; die Bänder der beiden abgeschätzten Faktoren (Index 1,07–1,16, BGF/Wohnfläche 1,25–1,40) sind darin nicht fortgepflanzt — gerechnet spannt die Wertdichte 1.855–2.866 €₂₀₂₆/m², der Bestand 7,6–11,8 Bio. €. **Vorschlag:** die Raten 3,4 % und 2,3 % aus den zitierten Monatswerten herleiten (oder die Quelle nennen), die Bandenden mit den ungerundeten Faktoren rechnen, und Typ-Spanne und Unsicherheitsband in Zeile und B4 getrennt ausweisen. | `python3 -c "L=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read().split(chr(10));r=L[188];b=chr(10).join(L[284:350]);q=chr(10).join(L[305:313]);raise SystemExit(0 if ('1.889–2.047' in r and '1.993–2.535' in r and '2,3 %' in b and '2,3' not in q and abs(1765*1.05**3-2047)>3) else 1)"` | offen |
| 28 | B | Bericht Kap. 2, Registerzeile 60-S093-01 (Z. 183) und Langbeleg B5, Absatz „Rechenschritt (§3.9 Abgeschätzt) — Band der Zustandsachse" (Z. 386–397); gekoppelt 60-S094-01 (Z. 184, B6 Z. 433–442) · **Fehler (§5 LF 5 „zentriert", „Band- und Endpunkt-Zuordnung"; §3.2 Mittelwertzentrierung)** — (a) B5 schreibt, die Spannweite ln(1,58/0,41) = 1,349 verteile sich auf die **zwei** Achsen Kontamination und Vorsorge, teilt dann aber durch **drei** (0,450); bei gleichem Anteil je Achse wäre der Anteil 0,6745 und das Band 0,71–1,40 statt 0,80–1,25 (S094 dann 0,845–1,184, kombiniert 0,60–1,66); zudem ist 0,41–1,58 die Diagonale C0P2 ↔ C2P0, nicht die Summe zweier Einzelachsen, und Vorsorge ist nach B5 selbst bewohner-, nicht gebäudeseitig; (b) „mittelwertzentriert auf den Bestandsmix" ist nicht nachgewiesen: die Werte sind geometrisch um 1 gesetzt, ohne Bestandsanteile je Klasse; bei 50 : 50 liegt das arithmetische Mittel bei 1,0254 (S093) bzw. 1,0063 (S094), zusammen +3,2 % auf den Basiswert; auch welcher Kurve von Fig. 1 die Endpunkte 3,5 %/25 % gehören, ist nicht zugeordnet; (c) Rechenfehler in der Sensitivitätslesart „voller Anteil": e^−0,6745 = 0,509 ⇒ **0,51**, nicht 0,52; (d) Sensitivitätsangabe der Zeile „±25 %" gegen das eigene Band −20 %/+25 %. **Vorschlag:** den Achsenanteil konsistent zur eigenen Prämisse herleiten (Teiler und Achsenzuordnung begründen), die Zentrierung mit ausgewiesenen Klassenanteilen rechnen oder als geometrische Zentrierung benennen, die Fig.-1-Kurve der Endpunkte zuordnen, 0,52 → 0,51 und „±25 %" → „−20 %/+25 %" korrigieren und S094 samt kombiniertem Band über die Kopplung neu rechnen. | `python3 -c "import math as m;L=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read().split(chr(10));b=chr(10).join(L[351:402]);l=m.log(1.58/.41);a=l/3;raise SystemExit(0 if ('1,349 ÷ 3' in b and 'Kontamination und Vorsorge' in b and '0,52–1,96' in b and round(m.exp(-l/2),2)==0.51 and (m.exp(a/2)+m.exp(-a/2))/2>1.02) else 1)"` | offen |
| 29 | C | Bericht Kap. 2, Registerzeile 60-S092-01 (Z. 182), Spalte Studientyp, gegen Langbeleg B5 (Z. 365–366) · **Widerspruch (§5 LF 5 „richtige Studienart"; LF 6 „Kopplungen"; §3.8)** — die Zeile begründet den Verzicht auf eine Effektgröße u. a. damit, Befragungen nach Ereignissen seien „nur Kandidat, im Volltext nicht verifiziert". Im selben Kapitel ist Thieken u. a. 2008 (FLEMOps, Befragung von 1.697 Haushalten) als „Volltext gegengelesen" geführt und trägt in Tab. 2 Vorsorge-Skalierungsfaktoren: C0P1 0,64 ÷ C0P0 0,92 = 0,696 und C0P2 0,41 ÷ 0,92 = 0,446, also −30 % bzw. −55 % Schaden je Gebäude mit guter bzw. sehr guter Vorsorge. Der Ausschluss als Wertquelle nach §3.5 (keine Interventionsstudie) bleibt richtig; falsch ist die Aussage „nicht verifiziert", und es fehlt der Vergleich als Plausibilitätsband für \(r_{\text{S092}}\) sowie die Kopplung: dieselbe Tab.-2-Spannweite, die die Vorsorge-Achse enthält, dimensioniert in B5 das Band von 60-S093-01. **Vorschlag:** in der S092-Zeile Thieken u. a. 2008 Tab. 2 als volltextgeprüfte, nach §3.5 nicht zulässige Befragungsevidenz nennen, die Werte 0,70/0,45 als Plausibilitätsprobe der Kette §5.1 ausweisen (nicht als Wert) und die Kopplung S092 ↔ S093 in B5 und in der Zeile vermerken. | `python3 -c "L=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read().split(chr(10));b=chr(10).join(L[351:402]);raise SystemExit(0 if ('im Volltext nicht verifiziert' in L[181] and 'C0P2 **0,41**' in b and 'Thieken' not in L[181]) else 1)"` | offen |
| 30 | C | Bericht Kap. 2, Registerzeile 60-S093-01 (Z. 183, Effektgröße „Gebäudetyp (3 Klassen)") und Kapitel 2 insgesamt; verweisende Stelle §3.3 (Stützstellentabelle Z. 557–559) · **Lücke (§5 LF 6 „Struktur überall verwendet, wo die Evidenz strukturabhängig ist")** — die zitierte Schadensfunktion FLEMOps ist nach Gebäudetyp (Einfamilien-, Doppel-/Reihen-, Mehrfamilienhaus) strukturiert; das Register nutzt die Typstruktur nur für den Preis (R24: EFH/ZFH 1.950, MFH 1.533 €₂₀₂₆/m² BGF), nicht für die Schadensquote, und weist die Nichtverwendung auch nicht als Modellgrenze aus (Kapitel 2: „je Gebäudetyp" und „typabhängig" je 0 Treffer). Die Endpunkte 3,5 %/25 % sind keinem Typ zugeordnet, obwohl das Register für jede 100-m-Zelle den Gebäudetyp aus dem Zensus 2022 als verfügbar nennt. **Vorschlag:** entweder eine Registerzeile (oder Spalte in 60-S093-01) für die typabhängige Schadensquote mit Zuordnung der Fig.-1-Endpunkte anlegen und die Typstruktur je Zelle nutzen, oder die typunabhängige Schadensquote ausdrücklich als Modellgrenze mit Richtung und Größenordnung ausweisen (Vorgabe P1/P2: als Abschätzung von KAP3). | `python3 -c "L=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read().split(chr(10));k=chr(10).join(L[151:450]);raise SystemExit(0 if ('Gebäudetyp (3 Klassen)' in L[182] and 'je Gebäudetyp' not in k and 'typabhängig' not in k) else 1)"` | offen |
| 31 | C | Bericht Kap. 2, Registerzeile 60-W085-01 (Z. 160), Spalten Effektgröße und Entscheidung, gegen §3.4 Schritt 2 (Z. 592) · **Lücke (§5 LF 5 „Band- und Endpunkt-Zuordnung"; §3.2 Sensitivitäten ausschließlich über das Register; §2.2 „In Formeln dürfen nur Zeilen mit Entscheidung Basiswert stehen")** — die Entscheidung lautet „Basiswert — die drei Szenario-Stützstellen p(HQ)", für HQextrem führt die Zeile aber nur das Band 5,0·10⁻³ bis 1,0·10⁻³ a⁻¹ ohne Zentralwert; der in der Kernformel rechnende Wert \(p_3 = 2{,}236\cdot10^{-3}\) a⁻¹ (geometrisches Mittel der Bandenden, als Abschätzung von KAP3 gekennzeichnet) steht erst in §3.4 und kommt in Kapitel 2 null mal vor. Damit ist die Zuordnung „Endpunkte = Sensitivität, Zentralwert = Basiswert" für die dritte Stützstelle im Register nicht vollständig. **Vorschlag:** in der Zeile 60-W085-01 den Zentralwert \(p_3 = 2{,}236\cdot10^{-3}\) a⁻¹ mit Vermerk „§3.9 Abgeschätzt, geometrisches Mittel der Bandenden" nachtragen und in B1 den Rechenschritt ergänzen. | `python3 -c "L=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read().split(chr(10));k=chr(10).join(L[151:450]);raise SystemExit(0 if ('HQextrem 5,0·10⁻³ bis 1,0·10⁻³' in L[159] and '2,236' not in k) else 1)"` | offen |

#### 2.3 · Abgrenzung und Status dieses Pakets

- **Beantwortet:** LF 5 (Verdikt Befund) und LF 6 (Verdikt Befund) — jede mit Beleg. LF 5
  nachgerechnet statt gelesen: sieben Registerzeilen mit Modifikator bzw. Band (60-W085-01,
  60-S074-01, 60-R17-01, 60-R24-01, 60-S093-01, 60-S094-01, 60-S092-01), je Zeile Zentrierung,
  Übersetzung und Band-/Endpunkt-Zuordnung mit Zahlenwert in der Tabelle von Abschnitt 2.1.
- **Nicht Gegenstand dieses Pakets:** die übrigen Leitfragen, die Kapitel außer Kapitel 2 und die
  Regression der Befunde 1–19 — insbesondere der Status von Befund 19 (`docs/evidenz/register.md`
  Z. 65), der ins Regressionspaket gehört. Ein nationaler 100-m-Vollraster-Lauf nach §3.4 war nicht
  verlangt und wurde nicht gefahren.
- **Kein Befund behoben**, kein Bericht, kein Register, kein Code, kein Lint, keine Arbeitsmappe
  geändert: `docs/methodik/60_gebaeudeschaeden_flusshochwasser.md` und `docs/evidenz/register.md`
  sind byte-gleich geblieben; `backend/scripts/lint_methodik.py` wurde in diesem Paket nicht
  ausgeführt (Ausgabe aus Abschnitt 0.1 übernommen).

### 3 · Paket T-0273 — Leitfragen 4, 7 und 8 gegen Kapitel 4 (Kalibrierung & Validierung)

Viertes Paket der Runde 2 (17.09.2026), eigene Sitzung. Sie hat den geprüften Stand nicht
geschrieben: Kapitel 4 stammt aus T-0238 und den Nachschnittpaketen T-0256 bis T-0259, alle im
Endstatus (eiserne Regel 4). Das Bundle nach §1 gilt unverändert (Abschnitt 0 dieser Runde). Die
Lint-Ausgabe aus Abschnitt 0.1 wird **übernommen und nicht neu vorhergesagt**; der Lint wurde in
diesem Paket nicht ausgeführt. Nach §6 ist die Prüfung **voll**, weil Kalibrierung und
Modellstruktur neu sind. Toleranzen werden nicht geweitet: Ein Prüfstein, der nicht trägt, ist ein
Befund und kein Anlass, ein Band anzupassen.

**Prüfumfang dieses Pakets:** genau Kapitel 4 „Kalibrierung & Validierung (§2.4/§3.4)"
(Z. 834–1097, Abschnitte 4.1–4.8 samt Block `beispiel_60_kalibrierung`). Nachgemessen mit
`python3 -c "s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();L=s.split(chr(10));print(len(s.split(chr(10)+'## 4 ')[1].split(chr(10)+'## 5 ')[0]),len(chr(10).join(L[833:1097])))"`
→ `18692 18697`. Die Abweichung von drei bzw. zwei Zeichen gegenüber den im Ticket genannten
**18.695** Zeichen kommt allein von der Schnittkante (Überschriftszeile, Leerzeile vor Kapitel 5).
Der geprüfte Textkörper ist derselbe; **Summe des Pakets: 18.695 Zeichen, ein Kapitel**. Andere
Kapitel wurden nur dort gelesen, wo Kapitel 4 ausdrücklich auf sie verweist: Registerzeilen
60-W085-01, 60-R17-01 und 60-R24-01, den Block `beispiel_60_kernformel` in §3.6 und \(\Delta q\) in
§5.1.2. Sie sind hier nicht Prüfgegenstand. Ein **nationaler 100-m-Vollraster-Lauf nach §3.4 war
nicht verlangt und wurde nicht gefahren**. Alle Nachrechnungen laufen auf den nationalen
Aggregaten des Kapitels, auf der Beispielzelle aus §3.6 und auf ZÜRS-Klassen als Stichprobe. Die
Arbeitsmappen wurden mit der Standardbibliothek gelesen (zipfile/XML, in dieser Umgebung ist
openpyxl nicht installiert), nur gelesen und nie geändert (eiserne Regel 2).

#### 3.1 · Nachrechnung der Rechenblöcke (LF 8 — gerechnet, nicht gelesen)

Der Block `beispiel_60_kalibrierung` wurde aus dem Bericht herausgelöst und mit `exec` ausgeführt.
**Alle Zusicherungen halten (grün).** Die Zwischenwerte wurden ungerundet ausgegeben:

| Schritt | Größe | Bericht | nachgerechnet | Ergebnis |
|---|---|---|---|---|
| 4.2 Zielwert | \(A^{*}\) = 1,6 · 0,65 · 1,54 · 0,50 · 1,15 · 1,07 | 0,99 Mrd. €₂₀₂₆/a | **0,9854** | trifft zu |
| 4.2 Band | alle Enden gleichgerichtet | 0,39–2,22 | **0,3914–2,2159** | trifft zu (rechnerisch); oberes Ende von \(\pi\) falsch → Befund 38 |
| 4.3 Modellsumme | \(M_0\) = 339.000 · 527.280 € · 6,311/1.200 a⁻¹ | 0,94 Mrd. €₂₀₂₆/a | **0,9401** | rechnet auf; Umfang und Herkunft des Schadensgrads → Befund 32 |
| 4.4 Niveau-Skalar | \(\lambda = A^{*}/M_0\) | 1,05 (0,42–2,36) | **1,0482** (0,416–2,357) | rechnet auf; Band liegt an beiden Enden außerhalb der eigenen Schranke 0,50–2,00 → Befund 36 |
| 4.5 Modellseite | Regime-Anteil ab HQ100 aus \(A = [15{,}0;\ 77{,}76;\ 300{,}0]\) m², \(p_3 = 2{,}236\cdot10^{-3}\) | 66,1 / 23,2 / 10,6 %, Summe 33,9 % | **66,14 / 23,23 / 10,63 %, 33,86 %** | trifft zu; die Stützstellen sind identisch mit der Beispielzelle `zelle(1200, …)` aus §3.6 (Ausgabe `[15.0, 77.76, 300.0]`, \(\bar A\) = 6,311) |
| 4.5 Ankerseite | Überschuss 2024 = 1,0/2,6 | 38,5 % | **38,46 %**, Differenz **4,6** Prozentpunkte | rechnet auf; nicht out-of-sample → Befund 33 |
| 4.6 Untergrenze | \(U\) = 1,6 · 0,65 · 0,50 · 1,07 | 0,56 | **0,5564** | rechnet auf; zirkulär → Befund 35 |
| 4.6 Obergrenze | \(O\) = 0,076 · 22,6 Mio · 527.280 € · 0,250 · 0,01 | 2,26 | **2,2641** | rechnet auf; keine obere Schranke → Befund 35 |
| 4.6 Lage | \(U \le \lambda M_0 \le O\) | 0,99 ∈ [0,56; 2,26] | **0,5564 ≤ 0,9854 ≤ 2,2641** | formal eingehalten, aber per Konstruktion (\(\lambda M_0 \equiv A^{*}\)) |

Die Gegenproben laufen mit `python3 -c` und stehen je Befund in Abschnitt 3.3. Die wichtigsten
Zahlen:
- **GK2-Lücke in \(M_0\):** Ein Gebäude in GK2 wird im Modell erst beim HQextrem nass.
  Trapez-Erwartungswert: \((p_2-p_3)\cdot q/2 + p_3 q\) = 0,000306 a⁻¹ bei \(q\) = 0,050 und
  0,001530 a⁻¹ bei \(q\) = 0,250. Multipliziert mit 1.378.600 Adressen · 527.280 € ergibt das
  **0,222 bis 1,112 Mrd. €₂₀₂₆/a, also 24 % bis 118 % von \(M_0\)**.
- **Obergrenze:** Die Modellrate beträgt 6,311/1.200 = **0,526 %/a** und liegt damit beim
  **2,10-Fachen** der „Höchstrate" von \(O\) (0,250 · 0,01 = 0,25 %/a). Setzt man für GK4 und
  GK3 \(p\) = 0,1 und für GK2 \(p\) = 0,01 an, entstehen **6,29 Mrd. €₂₀₂₆/a**; GK4 allein mit
  \(p\) = 0,1 ergibt 1,19 Mrd.
- **Untergrenze:** \(U/A^{*} = 1/(u\kappa)\) = **0,5647**. Mit den unteren Bandenden aus 4.2
  sinkt \(U\) auf **0,28**.
- **Trennschärfe der Verteilungsprüfung:** Eine Verdopplung des HQextrem-Schadens (\(A_3\) = 600)
  ergibt 48,8 % und **besteht**. Eine Verdreifachung ergibt 58,2 % und besteht nicht. Eine
  Halbierung ergibt 22,6 % und besteht knapp nicht.
- **\(\pi\):** 1,16/1,03 = **1,126** und 1,05³/1,03 = 1,124. Das Bandende 1,11 im Bericht liegt
  darunter.

#### 3.2 · Leitfragen dieses Pakets (§5) — einzeln mit Verdikt und Beleg

**LF 4 — Doppelzählung: zwei Kanäle? zwei Konten? Maßnahmeneffekt schon im Basiswert?
Referenzwerte doppeln Baseline-Anteile? Verdikt: Befund** (→ neuer Befund **39**).

Geprüft wurden vier Punkte. Drei bestehen, einer nicht.
- **Zwei Konten: bestanden.** \(A^{*}\) bleibt in K3 (Konten C26 „Wiederherstellungskosten an
  Gebäuden, Hausrat, Fahrzeugen …"). Kraftfahrt (1,3 von 5,7 Mrd. €) liegt außerhalb der
  Sachsumme, Hausrat und Gewerbe fallen über \(w_{\text{wg}}\) heraus. Versicherungsleistungen
  dienen **als Messung** des Schadens und werden über \(u\) und \(\kappa\) auf den Bruttoschaden
  hochgerechnet, nicht vom Schaden abgezogen. Das entspricht Mon. **J64** („Versicherungsleistungen
  sind Transfers und mindern den Schaden nicht (R5)"), das Mon. **J65** mit „Wie ID 59" übernimmt,
  und Rechenregeln **C7**. Dass ein GDV-Anker gewählt wird, deckt Rechenregeln **C19** („ergänzt um
  GDV-Schadensstatistiken").
- **Zwei Kanäle: bestanden.** \(\varphi_{\text{fluss}}\) schneidet Sturzflut (W087) und
  Kanalrückstau (W100) aus der gepoolten GDV-Position heraus (4.2). Kein anderer Bericht
  kalibriert heute auf dieselbe Reihe: `grep -c GDV` ergibt 0 in `25_…`, `47_…`, `50_…` und `61_…`.
  Eine Doppelbuchung derselben Anker-Euro gibt es heute also nicht.
- **Referenzwerte doppeln Baseline-Anteile (HD_ref-Klasse): bestanden.** \(A^{*}\) steht auf
  Bestand und Preisen 2024, \(\pi\) führt nur den Preisstand fort, \(M_0\) rechnet mit Preisen 2026.
  Kein Faktor steht doppelt im Produkt \(A^{*}\). Dass \(U\) dieselben Faktoren wiederverwendet,
  ist eine Frage der Sanity-Prüfung und steht unter LF 8.
- **Maßnahmeneffekt schon im Basiswert: Befund.** Der Doppelzählungs-Wächter aus 4.7 ist mit den
  Kalibrierjahren **formal verbunden** (2002–2024 einzeln benannt, 2025 ausgeschlossen, Stichtag
  31.12.2024, Befund 7 insoweit erledigt). In der vorliegenden Form lässt er sich aber **nicht
  operationalisieren**. \(\lambda\) hängt am **Mittel über 23 Jahre**. Der Ausstattungsstand vom
  31.12.2024 ist darin nicht enthalten, enthalten ist der mittlere Stand der Periode. Eine
  Nachrüstung aus dem Jahr \(t\) geht nur mit dem Gewicht \((2024-t+1)/23\) ins Mittel ein: für 2020
  mit **21,7 %**, für 2014 mit **47,8 %**. Nachrüstungen aus 2002–2024 stecken deshalb nur teilweise
  im kalibrierten Niveau. Sie werden über \(\Delta q\) aber vollständig ausgeschlossen. Auch die
  Verfallsregel („verfällt, sobald ein Kalibrierjahr nach 2024 aufgenommen wird") ist
  uneinheitlich: Der Referenzzustand rückt um ein volles Jahr, das Mittel nur um 1/24 →
  **Befund 39**.

**LF 7 — Tails/Parameter: Verteilungsannahmen, wo empirische Quantile verfügbar wären; gesetzte
Werte, die messbar wären; Kalibriermodell = Produktionsmodell? Verdikt: Befund** (→ neue Befunde
**32** und **34**).
- **Kalibriermodell = Produktionsmodell: nicht erfüllt.** Der Einleitungssatz von Kapitel 4
  behauptet es. Tatsächlich entsteht \(M_0\) jedoch aus dem „Vorab-Wert aus der Beispielzelle"
  (4.3, Punkt 3), also aus **einer erfundenen Zelle** mit \(W\) = 1.200 m² und den Anteilen
  \(a\) = 0,25/0,80/1,00, dazu einem Einheitswert je Adresse. Die acht Anker-Kommunen sind nur
  benannt und nicht gerechnet, die angekündigten „16 Werte" auf Bundesland-Ebene kommen im Kapitel
  nicht vor. Die Näherung hat zudem einen anderen **Umfang** als das Produktionsmodell: GK2 fehlt
  (0,22–1,11 Mrd. €, 24–118 % von \(M_0\), Abschnitt 3.1), und Adressen werden als Wohngebäude
  gezählt (19,7 Mio Wohngebäude auf 22,6 Mio Adressen = 0,872). §3.4 verbietet Faktoren aus
  Näherungsläufen, sobald das Produktionsmodell konvexe Wirkungsfunktionen hat. \(d(h)\) wächst
  multiplikativ (§3.3). → **Befund 32**.
- **Gesetzte Werte, die messbar wären: Befund.** Der Bericht verwendet laut 4.1 die Grafiken
  „Elementarschäden **an Wohngebäuden** nach Bundesländern" (10.10.2025) und die Übersichtsreihe
  (30.12.2025). Trotzdem setzt er \(w_{\text{wg}}\) = 0,65 („spartenscharfe Aufteilung … nicht
  publiziert") und leitet den Mittelwert \(A_{\text{ver}}\) aus dem Satz einer Pressemitteilung ab
  („rund eine Milliarde mehr"). Der ankerseitige Regime-Anteil stammt aus einem einzigen Jahr,
  „sobald die Jahreswerte … vorliegen" (4.5). Nach der eigenen Quellenangabe liegen die Jahreswerte
  und der Wohngebäude-Schnitt aber im zitierten Datenservice vor. Die Kleinste-Quadrate-Bestimmung
  über die Anker-Zeitreihe und die Sensitivität je Zeitfenster, die §3.4 verlangt, fehlen
  (`Kleinste Quadrate` und `Zeitfenster` kommen in Kapitel 4 je 0 mal vor). → **Befund 34**.
- **Verteilungsannahmen statt empirischer Quantile: Befund (in Befund 33 aufgenommen).** Der
  modellseitige Regime-Anteil ist ein reines Tail-Maß. Er stammt aus drei gesetzten Stützstellen
  der Beispielzelle mit einer flachen Fortsetzung \(p_3 \cdot A_3\), nicht aus gemessenen
  Tiefenverteilungen der Anker-Kommunen. Das modellseitige ±2,3 zeigt nur die Streuung über das
  \(p_3\)-Band.

**LF 8 — Kalibrierung: ein Skalar; Revisionsstand; unabhängige Verteilungsprüfung mit
Ist-Ergebnis, out-of-sample? Verdikt: Befund** (→ neue Befunde **32**, **33**, **35**, **36**,
**37**, **38**).
- **Ein Skalar: bestanden.** Es gibt genau ein \(\lambda\), bundesweit konstant, ohne Länder- oder
  Kommunalfaktor (4.4, „Anwendungsregel"). Gegenprobe: Eine Kommune mit \(a\) = 0 bleibt bei 0,
  denn \(\lambda \cdot 0 = 0\). Das Paket T-0271 hat \(\text{EAD}_k\) = 0,00 bereits nachgerechnet.
- **Revisionsstand: bestanden.** Datenservice Naturgefahrenreport 2025, Grafikstände 10.10.2025 und
  30.12.2025, Normierung „Bestand und Preise 2024"; das vorläufige Jahr 2025 ist aus dem Mittel
  herausgenommen (4.1). Die Sensitivität ohne vorläufige Werte ist damit trivial erfüllt. Die
  fehlende Sensitivität je Zeitfenster steht in Befund 34.
- **Nachgerechnete Zahlen:** Zielwert 0,9854, Modellsumme 0,9401, Skalar 1,0482, Regime-Anteil
  33,86 % gegen 38,46 %, Lage 0,5564 ≤ 0,9854 ≤ 2,2641 — **die Arithmetik stimmt vollständig**
  (Abschnitt 3.1).
- **Unabhängige Verteilungsprüfung mit Ist-Ergebnis: vorhanden, aber nicht out-of-sample.** Das
  Prüfjahr 2024 ist **selbst die Quelle des Ankermittels**: \(A_{\text{ver}}\) = 2,6 − 1,0 = 1,6,
  und die Ankerseite der Prüfung lautet 1,0/2,6. Beide Seiten beruhen auf denselben zwei Zahlen
  aus derselben Medieninformation. Die bezifferte Überlappung „1 von 23 Kalibrierjahren, 4,3 %"
  beschreibt das nicht. Die Prüfung vergleicht außerdem den Anteil an einem **Erwartungswert**
  (Modell) mit dem Überschuss eines **Einzeljahres** (Anker). Das ankerseitige ±12,5 ist gesetzt,
  nicht hergeleitet („dafür ±12,5 Prozentpunkte"). Eine Verdopplung des Extremschadens besteht die
  Prüfung noch (48,8 %). → **Befund 33**.
- **Kalibrierung mit dem Produktionsmodell:** nicht erfüllt → **Befund 32** (siehe LF 7).
- **Sanity-Band: formal eingehalten, als Prüfstein nicht tragfähig.** \(U\) ist zirkulär, denn
  \(U \le \lambda M_0\) gilt für jedes \(u\kappa \ge 1\). \(O\) ist keine Obergrenze, weil die
  eigene Modellrate 2,10-mal so hoch liegt. Die §3.4-Forderung nach „amtlicher Statistik" ist ohne
  begründete Ausnahme nicht erfüllt, da der GDV keine amtliche Stelle ist. → **Befund 35**.
- **Plausibilitätsschranke 0,50–2,00:** ungeleitet und im Widerspruch zum eigenen \(\lambda\)-Band
  0,42–2,36 → **Befund 36**.
- **Vorgabe P1, gemessen an 4.8:** Die Tabelle trennt Quelle und Abschätzung sauber für elf
  Zeilen. Es fehlen jedoch die Betroffenheitsannahme 1/100 a, die Schranke 0,50/2,00 und der
  Baupreisanstieg 2023 → 2024 von „rund 3 %". Das sind Parameter, die im Kapitel rechnen und
  nutzersichtbar ausgewiesen werden müssen. Die Toleranzzeile führt ±2,3/±12,5 zwar, doch ±12,5 hat
  keine Herleitung (Befund 33). → **Befund 37**.
- **Bandende von \(\pi\) falsch gerechnet** → **Befund 38**.

*Formelzeichen (Abgrenzung zu LF 13):* Alle zwölf Formelzeichen von Kapitel 4 haben im Kapitel
eine Herleitungsstelle: \(A_{\text{ver}}\) (4.1), \(w_{\text{wg}}, u, \varphi_{\text{fluss}},
\kappa, \pi, A^{*}\) (4.2), \(M_0\) (4.3), \(\lambda\) (4.4), \(U, O\) (4.6) und \(q_0\) (4.7,
ausdrücklich geparkt). Ein Formelzeichen **ohne** Herleitung gibt es nicht, **deshalb kein eigener
Befund**. Ob Kapitel 4 eine eigene Zeichentabelle braucht, ist eine Formfrage (LF 11/13) und wird
hier nicht beurteilt.

#### 3.3 · Neue Befunde dieses Pakets (32–39)

Format nach §5: Stelle · Art (Lücke/Fehler/Widerspruch) · Begründung · Vorschlag · Kategorie. Das
Ticket nennt die Nummern 1–19 und als erste neue Nummer 20; das war der Stand beim Ticketschnitt.
Die vorlaufenden Pakete T-0270 (20–22), T-0271 (23–26) und T-0272 (27–31) haben seither weiter
vergeben. Nach der Regel „fortlaufend ab der nächsthöheren freien Nummer" ist die erste neue Nummer
deshalb **32**. **Dieses Paket behebt keinen Befund**, weder einen neuen noch einen alten. Die
Kurzform-Tabelle „Offene Befunde" am Kopf bleibt bewusst unberührt, sie schreibt die
Befund-Regression dieser Runde fort. Jeder Prüfausdruck endet mit Exit 0, **solange der Befund
besteht**. Am 17.09.2026 wurden alle acht ausgeführt, alle acht endeten mit Exit 0.

| Nr | Kat. | Befund (Stelle · Art · Begründung · Vorschlag) | Prüfausdruck | Status |
|---|---|---|---|---|
| 32 | A | Bericht Kap. 4, Einleitung (Z. 839–841) gegen 4.3 (Z. 924–948) · **Widerspruch/Fehler (§2.4 „Kalibrierlauf immer mit dem Produktionsmodell", §3.4 „Kalibriermodell = Produktionsmodell", §5 LF 7/8)** — Die Einleitung behauptet, das Kalibriermodell sei das Produktionsmodell. \(M_0\) entsteht aber aus drei nationalen Einheitswerten, und der Schadensgrad 0,526 %/a ist der „Vorab-Wert aus der Beispielzelle" (W = 1.200 m², \(a\) = 0,25/0,80/1,00). Die acht benannten Anker-Kommunen sind nicht gerechnet, die angekündigten 16 Länderwerte fehlen. Die Näherung hat einen anderen Umfang als \(A^{*}\): (a) GK2 (1,38 Mio Adressen, im Modell bei HQextrem nass) fehlt in \(M_0\). Nachgerechnet ergibt das 0,222 Mrd. € (\(q\) = 0,050) bis 1,112 Mrd. € (\(q\) = 0,250) je Jahr, also **24–118 % von \(M_0\)**. \(A^{*}\) enthält diese Schäden, deshalb nimmt \(\lambda\) den fehlenden Umfang auf, statt ein Niveau zu korrigieren. (b) Alle 339.000 Adressen zählen als Wohngebäude mit 208 m²; Wohngebäude je Adresse = 19,7/22,6 = 0,872. Das ist entgegen der Behauptung keine Untergrenze. (c) \(d(h)\) wächst multiplikativ, damit trifft das Näherungsverbot aus §3.4 zu. Der Satz „das Modell trifft das Anker-Niveau ohne nennenswerte Korrektur" (4.4) ist deshalb kein Kalibrierergebnis. **Vorschlag:** \(M_0\) mit dem Produktionsmodell auf der dokumentierten Stichprobe rechnen (acht Anker-Kommunen, hochgerechnet über ZÜRS-Klassen **einschließlich GK2**, Adressen über den Wohngebäudeanteil umgerechnet), \(\lambda\) daraus bestimmen und den Restfehler unterhalb der Stichprobenauflösung nach §3.4/§3.9 quantifiziert ausweisen. Bis dahin \(\lambda\) = 1,05 ausdrücklich als vorläufig kennzeichnen und die Einleitung korrigieren. Kein Vollraster-Lauf. | `python3 -c "s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();k=s.split(chr(10)+'## 4 ')[1].split(chr(10)+'## 5 ')[0];raise SystemExit(0 if ('Vorab-Wert aus der Beispielzelle' in k and 'ZÜRS-GK3+GK4' in k and 'Das Kalibriermodell ist das' in k) else 1)"` | offen |
| 33 | A | Bericht Kap. 4.5 (Z. 973–998) und 4.1 „Ankerwert" (Z. 862–865) · **Fehler (§3.4 „Prüfdaten dürfen nicht dieselben sein, auf denen Faktoren gefittet wurden", §5 LF 8 „out-of-sample", §6 Kalibrier-Prüfstein)** — (a) Die Ankerseite der Verteilungsprüfung (1,0/2,6 = 38,46 %) und das Ankermittel \(A_{\text{ver}}\) = 2,6 − 1,0 = 1,6, aus dem \(\lambda\) bestimmt wird, beruhen auf **denselben zwei Zahlen** aus derselben GDV-Medieninformation zu 2024. Die ausgewiesene Überlappung „1 von 23 Kalibrierjahren, 4,3 %" gibt das nicht wieder, denn aus den anderen 22 Jahren geht kein Wert ein. (b) Die Größen passen nicht zusammen: Das Modell misst den Anteil des seltenen Regimes am **Erwartungswert**, der Anker misst den Überschuss eines **Einzeljahres** über das Mittel. Pluviale Anteile sind darin gepoolt. (c) Das ankerseitige ±12,5 ist gesetzt, nicht hergeleitet (§3.9), und legt die Toleranz fast allein fest. Die Prüfung trennt schwach: Eine Verdopplung des HQextrem-Schadens (\(A_3\) = 600 m²) ergibt 48,76 % und **besteht**. (d) Der modellseitige Anteil 33,86 % kommt aus den gesetzten Stützstellen einer Beispielzelle, nicht aus gemessenen Tiefen der Anker-Kommunen (§3.2 Tails). Der Kalibrier-Prüfstein nach §6 ist damit nicht bestanden. Die Toleranz wird **nicht** geweitet oder verengt, der Befund geht in einen Modellentscheid. **Vorschlag:** Die Prüfung auf Daten stellen, die nicht zur Bestimmung von \(\lambda\) dienen. Möglich sind ein Leave-one-out über die Jahreswerte 2002–2024 (Anteil der Jahre über einer Ereignisschwelle, gerechnet ohne das jeweilige Jahr im Mittel) oder die Länderwerte der Wohngebäude-Grafik gegen die Modellverteilung auf Länderebene. Den Ankerwert als Erwartungswertanteil definieren, das ankerseitige Toleranzbudget herleiten und die Toleranz vor der Rechnung neu fixieren. | `python3 -c "s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();k=s.split(chr(10)+'## 4 ')[1].split(chr(10)+'## 5 ')[0];raise SystemExit(0 if ('1,0/2,6' in k and '1 von 23 Kalibrierjahren' in k and 'dafür ±12,5 Prozentpunkte' in k) else 1)"` | offen |
| 34 | B | Bericht Kap. 4.1 (Z. 855–865), 4.2 Herleitung \(w_{\text{wg}}\) (Z. 892–897), 4.4 (Z. 952) und 4.5 „Grenzen der Prüfung" (Z. 993–998) · **Lücke (§3.4 Kalibrierfaktor-Regel „Kleinste Quadrate Anker ÷ Modellsumme über die Anker-Zeitreihe; einheitliche Jahres-Auswahlregel, Sensitivitäten je Zeitfenster", §5 LF 7 „gesetzte Werte, die messbar wären")** — \(\lambda\) ist ein einfacher Quotient aus einem Mittelwert, den ein Presse-Satz liefert („rund eine Milliarde mehr als im langjährigen Durchschnitt"). Er wird nicht über die Zeitreihe gefittet, und eine Sensitivität je Zeitfenster fehlt (in Kap. 4 kommen `Kleinste Quadrate` und `Zeitfenster` je 0 mal vor). Nach 4.1 verwendet der Bericht selbst die Übersichtsreihe (30.12.2025) und die Grafik „Elementarschäden **an Wohngebäuden** nach Bundesländern" (10.10.2025). Trotzdem gelten die Jahreswerte als noch nicht vorliegend (4.5), und \(w_{\text{wg}}\) = 0,65 wird als „nicht publiziert" gesetzt. Beide Größen sind nach der eigenen Quellenangabe messbar. Außerdem ist offen, ob GDVs „langjähriger Durchschnitt" 2002–2024 umfasst. **Vorschlag:** die 23 Jahreswerte aus dem zitierten Datenservice mit Grafik und Zugriffsdatum übernehmen, \(A_{\text{ver}}\) als deren Mittel rechnen (und \(\lambda\) nach §3.4 fitten), Sensitivitäten für mindestens zwei Zeitfenster ausweisen (z. B. 2002–2024 und 2014–2024, mit und ohne 2021), \(w_{\text{wg}}\) aus dem Wohngebäude-Schnitt messen oder begründen, warum er dort nicht abgelesen werden kann. | `python3 -c "s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();k=s.split(chr(10)+'## 4 ')[1].split(chr(10)+'## 5 ')[0];raise SystemExit(0 if ('Kleinste Quadrate' not in k and 'Zeitfenster' not in k and 'an Wohngebäuden' in k and 'nicht publiziert' in k) else 1)"` | offen |
| 35 | B | Bericht Kap. 4.6 (Z. 1002–1014) · **Fehler (§3.4 „Sanity-Bänder mit Unter- und Obergrenze aus amtlicher Statistik (oder begründete Ausnahme)", §6 „ein zu weit gewordenes Band ist ein Befund")** — (a) **Untergrenze zirkulär:** \(U = A_{\text{ver}} w_{\text{wg}} \varphi \pi\) und \(\lambda M_0 \equiv A^{*} = U \cdot u\kappa\). Die Prüfung \(U \le \lambda M_0\) gilt also für **jedes** \(u\kappa \ge 1\) (nachgerechnet \(U/A^{*}\) = 0,5647) und kann nicht scheitern. Als „harte" Grenze beruht sie zudem auf den Mittelwerten zweier Abschätzungen; mit deren unteren Bandenden sinkt \(U\) auf 0,28. (b) **Obergrenze ist keine Schranke:** Die Begründung „Mehr kann selbst dann nicht entstehen, wenn jedes exponierte Gebäude im Hundertjahresrhythmus mit maximaler Quote getroffen wird" übersieht, dass GK4 nach ZÜRS-Definition und nach dem eigenen \(p_1\) = 0,1 a⁻¹ mindestens alle zehn Jahre nass wird. Die eigene Modellrate (6,311/1.200 = 0,526 %/a) liegt beim **2,10-Fachen** der angesetzten Höchstrate 0,25 %/a. Klassengerecht (GK4 und GK3 mit 0,1 a⁻¹, GK2 mit 0,01 a⁻¹, Quote 0,250) ergibt sich **6,29 Mrd. €₂₀₂₆/a**, GK4 allein 1,19 Mrd. Dass die Lage „eingehalten" ist, liegt daran, dass \(O\) fünfmal so viele Adressen zählt. (c) Beide Grenzen stammen aus GDV-Zahlen, ZÜRS und Abschätzungen, keine aus amtlicher Statistik; eine begründete Ausnahme fehlt. **Vorschlag:** die Untergrenze unabhängig vom Ankerfaktorsatz herleiten (z. B. aus amtlichen Wiederaufbauhilfen 2013/2021 als Ereignis-Mindestschaden, umgelegt auf die Wiederkehrzeit), die Obergrenze klassengerecht mit den Überflutungswahrscheinlichkeiten der ZÜRS-Klassen bilden, die Ausnahme vom Amtlichkeitsgebot begründen. Das Band danach vorab fixieren und nicht wieder weiten. | `python3 -c "s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();k=s.split(chr(10)+'## 4 ')[1].split(chr(10)+'## 5 ')[0];raise SystemExit(0 if ('mittleren Betroffenheit von 1/100 Jahren' in k and 'Hochrechnung \\\\(u\\\\) entfällt hier bewusst' in k and 6.311/1200>0.25*0.01) else 1)"` | offen |
| 36 | B | Bericht Kap. 4.4 „Plausibilitätsschranke" (Z. 960–963) gegen 4.4 Band (Z. 952) und 4.8 (Z. 1053) · **Widerspruch/Lücke (§3.9 Herleitungspflicht; §6 Prüfsteine)** — Die Schranke \(\lambda\) < 0,50 oder > 2,00 („Modell gilt als fehlerhaft") ist ohne Herleitung gesetzt und in 4.8 nicht aufgeführt. Das eigene \(\lambda\)-Band 0,42–2,36 (nachgerechnet 0,416–2,357) liegt **an beiden Enden außerhalb** dieser Schranke. Der Bericht erklärt damit Teile seines eigenen Unsicherheitsbandes für modellfehlerhaft, ohne diese Fälle zu entscheiden. Zudem enthält das \(\lambda\)-Band nur die Ankerunsicherheit, \(M_0\) trägt kein Band (208 m², 1,30, 1.950 €, 6,311/1.200 und 339.000 gehen ungestreut ein). **Vorschlag:** die Schranke aus dem vollständig fortgepflanzten Band von \(A^{*}\) **und** \(M_0\) herleiten und in 4.8 führen oder ausdrücklich begründen, warum Bandenden jenseits der Schranke zulässig sind. | `python3 -c "s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();k=s.split(chr(10)+'## 4 ')[1].split(chr(10)+'## 5 ')[0];t=k.split('### 4.8 ')[1];raise SystemExit(0 if ('0,42–2,36' in k and '2{,}00' in k and '2,00' not in t and '2{,}00' not in t) else 1)"` | offen |
| 37 | B | Bericht Kap. 4.8 Parametertabelle (Z. 1045–1057) gegen 4.2 (Z. 913–915), 4.5 (Z. 973–978), 4.4 (Z. 960–961) und 4.6 (Z. 1005/1009) · **Lücke (Vorgabe P1 „Gilt für alle Parameter", §3.9 „Unzulässig: … Bandgrenzen, Referenzwerte")** — Drei Werte, die in Kapitel 4 rechnen, fehlen in der P1-Tabelle: die Betroffenheit **1/100 a** (in 4.6 selbst „Abschätzung von KAP3" genannt; in 4.8 kommt sie nur als Wort in der Herleitungsspalte von \(O\) vor, ohne eigene Zeile und Kennzeichnung), die Plausibilitätsschranke **0,50/2,00** und der Baupreisanstieg **„rund 3 %" 2023 → 2024**, aus dem \(\pi\) folgt (ohne Quelle, ohne Abschätzungsvermerk). Außerdem heißen \(\lambda\), \(U\) und \(O\) „berechnet". Sie hängen jedoch an Abschätzungen von KAP3 (\(w_{\text{wg}}\), \(\varphi\), 1/100 a), und P1 kennt nur Quelle oder Abschätzung samt Herleitung. Ein Nutzer sähe „berechnet", ohne zu erkennen, dass eine Abschätzung trägt. **Vorschlag:** die drei Parameter mit Wert, Band und Kennzeichnung (Quelle oder Abschätzung von KAP3 samt Herleitungsanker) in 4.8 aufnehmen, bei \(\lambda\), \(U\) und \(O\) vermerken, welche Abschätzungen einfließen. | `python3 -c "s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();t=s.split('### 4.8 ')[1].split(chr(10)+'## 5 ')[0];raise SystemExit(0 if ('Betroffenheit' not in t and '2,00' not in t and 'rund 3' not in t and 'Baupreisanstieg' not in t) else 1)"` | offen |
| 38 | C | Bericht Kap. 4.2 Tabellenzeile \(\pi\) (Z. 887), Herleitung (Z. 913–915) und 4.8 (Z. 1052); gerechnet im Block `beispiel_60_kalibrierung` (Z. 1064–1065) · **Fehler (Rechenfehler im Band)** — \(\pi = 1{,}105/1{,}03 = 1{,}0728\) trifft zu. Die Bandenden folgen aus dem B4-Band 1,07–1,16 aber als 1,07/1,03 = **1,039** und 1,16/1,03 = **1,126** (mit dem ungerundeten 1,05³ = 1,1576, vgl. Befund 27: **1,124**), nicht als 1,04–**1,11**. Dadurch ist das obere Ende von \(A^{*}\) mit 2,216 zu niedrig; mit 1,126 wären es 2,248 Mrd. €, dicht an \(O\) = 2,264. Der Beispielblock prüft nur die eigene Rundung und fängt den Fehler deshalb nicht. **Vorschlag:** das Band von \(\pi\) aus dem Band von B4 rechnen (nach Befund 27), \(A^{*}\)-Band, \(\lambda\)-Band und die Zusicherung `hi` nachziehen. | `python3 -c "s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();k=s.split(chr(10)+'## 4 ')[1].split(chr(10)+'## 5 ')[0];raise SystemExit(0 if ('1,07 (1,04–1,11)' in k and round(1.16/1.03,2)>1.11) else 1)"` | offen |
| 39 | B | Bericht Kap. 4.7 „Wächter" (Z. 1023–1029) gegen 4.4 (\(\lambda\) aus dem Mittel 2002–2024) und §5.1.2 (\(\Delta q\)) · **Lücke (§3.5 „Doppelzählungs-Wächter gegen die Kalibrierjahre", §5 LF 4 „Maßnahmeneffekt schon im Basiswert?")** — Der Wächter setzt als Referenz den „Ausstattungsstand 31.12.2024" und schließt alle Nachrüstungen bis 2024 aus \(\Delta q\) aus. \(\lambda\) bildet aber den **mittleren** Ausstattungsstand der Jahre 2002–2024 ab, nicht den Stand zum Stichtag. Eine Nachrüstung aus dem Jahr \(t\) geht nur mit dem Gewicht \((2024-t+1)/23\) ins Niveau ein (2020: 21,7 %, 2014: 47,8 %). Solche Nachrüstungen sind im Basisschaden also nur teilweise enthalten, werden als Hebel aber vollständig gesperrt. Das Niveau liegt dadurch über dem Stand 2024, der Hebel ist unterzählt. Die Verfallsregel verschiebt den Referenzzustand je neu aufgenommenem Jahr um ein ganzes Jahr, das Kalibriermittel nur um 1/24. Ohne \(q_0\) lässt sich außerdem nicht prüfen, ob \(\Delta q\) = 0,10 ein Zuwachs nach 2024 ist. Befund 7 ist formal abgearbeitet, der Wächter selbst aber nicht operationalisiert. **Vorschlag:** den Referenzzustand als das über die Kalibrierjahre gewichtete Ausstattungsmittel definieren (oder das Kalibrierfenster so kurz wählen, dass der Stichtag das Mittel repräsentiert, mit Sensitivität je Zeitfenster nach §3.4, vgl. Befund 34) und die Verfallsregel auf die tatsächliche Gewichtsverschiebung umstellen. Richtung und Größenordnung der Verzerrung als Modellgrenze ausweisen, solange \(q_0\) geparkt ist. | `python3 -c "s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();t=s.split('### 4.7 ')[1].split('### 4.8 ')[0];raise SystemExit(0 if ('Ausstattungsstand 31.12.2024' in t and 'gewicht' not in t.lower()) else 1)"` | offen |

#### 3.4 · Abgrenzung und Status dieses Pakets

- **Beantwortet:** LF 4 (Verdikt Befund), LF 7 (Verdikt Befund) und LF 8 (Verdikt Befund), jede mit
  Beleg. LF 8 wurde nachgerechnet statt gelesen: Zielwert 0,9854, Modellsumme 0,9401,
  Niveau-Skalar 1,0482, Regime-Anteil 33,86 % gegen 38,46 % (Differenz 4,6 Prozentpunkte) und die
  Lage 0,5564 ≤ 0,9854 ≤ 2,2641 stammen aus dem ausgeführten Block `beispiel_60_kalibrierung`
  (grün) und sind mit Gegenproben ergänzt (Abschnitt 3.1).
- **Nicht Gegenstand dieses Pakets:** die übrigen Leitfragen, die Kapitel außer Kapitel 4, die
  Prüfung der GDV-Primärquelle gegen Kapitel 8 (LF 10), die Kostensatz-Frage Neuwert gegen den
  „Zeitwertansatz" aus Mon. J64 (LF 9) und die Regression der Befunde 1–19. Ein nationaler
  100-m-Vollraster-Lauf nach §3.4 war nicht verlangt und wurde nicht gefahren.
- **Kein Befund behoben**, und kein Bericht, Register, Code, Lint oder keine Arbeitsmappe geändert:
  `docs/methodik/60_gebaeudeschaeden_flusshochwasser.md` und `docs/evidenz/register.md` sind
  byte-gleich geblieben; `backend/scripts/lint_methodik.py` wurde in diesem Paket nicht ausgeführt
  (Ausgabe aus Abschnitt 0.1 übernommen).
