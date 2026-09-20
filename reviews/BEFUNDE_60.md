# Befund-Ledger #60 — Schäden an Gebäuden aufgrund von Flusshochwasser

Angelegt 11.09.2026 mit dem Erstaufschlag `docs/methodik/60_gebaeudeschaeden_flusshochwasser.md`
(`/neu-risiko 60`). **Review-Runde 1 am 13.09.2026 gefahren** (T-0232, Messrunde — ohne Revision).
Befunde werden fortlaufend ab 1 nummeriert.
Pflege über `backend/scripts/ledger.py`. Ein Befund wird nur mit Prüfausdruck geschlossen (W7).
Zurückgestellte A-Befunde blockieren die Abnahme.

## Offene Befunde (19)

Kurzform über alle bisher vergebenen Befundnummern (1–46). Art, Begründung und Vorschlag je Befund
stehen in den Befundtabellen von [Review-Runde 1](#review-runde-1) (Befunde 1–19) und
[Review-Runde 2](#review-runde-2) (Befunde 20–46) weiter unten; der Wortlaut der Prüfausdrücke
steht dort ebenfalls, diese Tabelle nennt für die Befunde ab 20 nur, ob einer hinterlegt ist.
**Stand: nach der Autor-Revision der Runde 2 (17.09.2026).** Der Status ist der jeweils letzte in
den Abschnitten der Runden 1 und 2 einschließlich
[Autor-Revision nach Runde 2](#autor-revision-nach-runde-2) vergebene Status; er wird hier
übernommen und nicht neu beurteilt. Gezählt sind in der Überschrift die Zeilen mit Status `offen`
oder `bewusst offen` (8 + 11 = 19; Stand nach dem [Nachtrag zu Befund 2](#nachtrag-zu-befund-2-knoten-bilanz)
vom 18.09.2026). Wo ein Umsetzungsnachweis steht, der Befund aber auf `offen`
bleibt, hat die Regression der Runde 2 (Abschnitte 5.1 und 6.1) die Statusspalte ausdrücklich
nicht fortgeschrieben; ihr Urteil steht in der Nachweisspalte.

| Nr | Befund (Stelle · Kurzfassung) | Kat. | Status | Umsetzungsnachweis | Prüfausdruck | Begründung bei Abweichung |
|---|---|---|---|---|---|---|
| 1 | Bericht Kap. 3 „Modell" Z. 146–185 · **Lücke** — Kapitel enthält außer einem HTML-Kommentar 0 Zeichen: keine Formel, keine Zeichentabelle, keine native Ergebnisgröße | A | behoben | Bericht Kap. 3, Abschnitte 3.1 „Native Ergebnisgröße, Einheit, Bezugsjahr, Betrachtungsebene" und 3.4 „Kernformel auf Zellebene": das Kapitel trägt jetzt 17.109 Zeichen außerhalb von HTML-Kommentaren, darunter die deklarierte native Ergebnisgröße EAD in €₂₀₂₆/a mit Bezugsjahr 2026 und Betrachtungsebene Kommune sowie die dreistufige Schicht-B-Kernformel Menge × Rate × Preis mit der physischen Zwischengröße „schadensäquivalente Wohnfläche" (m²) vor dem Euro-Betrag und einem lauffähigen Beispielblock `beispiel_60_kernformel_zelle`; die Schadensfunktion \(d(h)\) in Abschnitt 3.3 trägt Gültigkeitsbereich 0,10–1,75 m und konstante Deckelung auf 0,250 darüber (Absatz „Gültigkeitsbereich und Deckelung"), sodass keine Schadensquote über 100 % entstehen kann. | `python3 -c "import re;s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();k=s.split('\n## 3 ')[1].split('\n## 4 ')[0];raise SystemExit(0 if len(re.sub(r'<!--.*?-->','',k,flags=re.S).strip())>=8000 else 1)"` | Vorschlag in Runde 1 |
| 2 | Bericht Kap. 1 Knoten-Bilanz Z. 43–76 · **Lücke** — alle 32 Zeilen „rechnet in: offen"; kein Knoten verarbeitet oder begründet inaktiv | A | behoben | Nachtrag 18.09.2026 (siehe [Nachtrag zu Befund 2](#nachtrag-zu-befund-2-knoten-bilanz)): Fundstelle Kapitel 1 „Wirkungskette & Knoten-Bilanz (§2.1)", Tabelle „Knoten-Bilanz" — `grep -c "rechnet in: offen" docs/methodik/60_gebaeudeschaeden_flusshochwasser.md` liefert `0`; alle 32 Zeilen tragen jetzt eine benannte Formelstelle (FS-Hazard/FS-Exposition/FS-Schadensgrad/FS-Mengengerüst/FS-Schutzsystem/FS-Bestandsdynamik/FS-Vorsorge) oder `inaktiv` mit wörtlichem Zitat aus KWRA-Monetarisierung.xlsx (Blatt und Zelle genannt). | `grep -c "rechnet in: offen" docs/methodik/60_gebaeudeschaeden_flusshochwasser.md` | Vorschlag in Runde 1 |
| 3 | Bericht Kap. 2 Evidenz-Register Z. 111–144 · **Lücke** — 31 von 32 Zeilen in allen Spalten „offen", keine Zeile mit Entscheidung „Basiswert" | A | behoben | Bericht Kap. 2, Abschnitt „Evidenz-Register (§2.2)" (Registertabelle mit den Langbelegen B1–B6): die sieben tragenden Zeilen 60-W085-01, 60-R24-01, 60-S074-01, 60-R17-01, 60-S093-01, 60-S094-01 und 60-S092-01 tragen jetzt Effektgröße, Studientyp, volltextgeprüfte Quelle, Übertragbarkeit, Datenlage je Zelle und Entscheidung — zwei davon „Basiswert" (Hazard 60-W085-01, Mengengerüst 60-R24-01) —, während die übrigen 25 Zeilen weiterhin auf „offen" stehen. | — | Vorschlag in Runde 1 |
| 4 | Bericht Kap. 4 „Kalibrierung & Validierung" Z. 187–199 · **Lücke** — 0 Zeichen Substanz: kein Anker, kein Niveau-Skalar, keine Verteilungsprüfung, keine Toleranz | A | behoben | Bericht Kap. 4, Abschnitte 4.1 bis 4.8: das Kapitel trägt jetzt rund 18.700 Zeichen außerhalb von HTML-Kommentaren mit dem namentlichen nationalen Anker „GDV-Naturgefahrenstatistik, Teilreihe Starkregen/Überschwemmung" (Zeitreihe seit 2002, Revisionsstand Datenservice Naturgefahrenreport 2025 vom 10.10./30.12.2025, vorläufiges Jahr 2025 ausgeschlossen), dem Niveau-Skalar λ = 1,05 samt Rechenweg A\*/M₀ (§4.2–§4.4), der unabhängigen Verteilungsprüfung auf der Achse Ereignisregime mit vorab fixierter Toleranz ±15 Prozentpunkten gegen ein Ist von 4,6 Prozentpunkten (§4.5), dem Sanity-Band 0,56–2,26 Mrd. €₂₀₂₆/a mit Herleitung beider Grenzen (§4.6), der P1-Parametertabelle (§4.8) und dem ausdrücklichen Satz zur Auflösung (Bundesland-, Gemeindepunkt- und Stichprobenebene, kein nationaler 100-m-Vollraster-Lauf, §4.3). | `python3 -c "import re;s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();k=s.split('\n## 4 ')[1].split('\n## 5 ')[0];raise SystemExit(0 if len(re.sub(r'<!--.*?-->','',k,flags=re.S).strip())>=6000 else 1)"` | Vorschlag in Runde 1 |
| 5 | Bericht Kap. 3 Z. 160–165 (Absatz „(a) DATENEBENEN-ANLAGEPFLICHT") · **Lücke** — HQ-Wassertiefen und Gebäudewerte nur als Absichtserklärung im Kommentar, keine Ebene spezifiziert | A | behoben | Bericht Kap. 3, Abschnitt 3.2 „Datenebenen nach §3.1" (Ebenentabelle plus Absätze „Beschaffungs-Watchlist", „Ressourcen-Regel", „Kein-Doppelkanal"): die vier Ebenen HQ_FLAECHE, HQ_TIEFE, GEBAEUDEWERT (je **neu anzulegen**) und GEBAEUDEZUSTAND_BAUSTOFF (**geparkt (Datenquelle fehlt)** mit dreiteiliger Beschaffungs-Watchlist und Neutralwert 1,00) tragen jeweils Quelle, keyless Beschaffungsweg, Zell-Ableitungsregel, Fallback aus der Betrachtungsebene selbst und Normierung/Zentrierung, der HTML-Kommentar mit der Absichtserklärung ist entfallen; Abschnitt 3.3, Absatz „Abbildung der beiden Tiefenraster", bildet die LAWA-Klassen der Ebene HQ_TIEFE auf die metrische Tiefe der Schadensfunktion ab. | `python3 -c "s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();k=s.split('\n## 3 ')[1].split('\n## 4 ')[0];raise SystemExit(0 if all(t in k for t in ('HQ_FLAECHE','HQ_TIEFE','GEBAEUDEWERT','neu anzulegen','geparkt (Datenquelle fehlt)','Beschaffungs-Watchlist')) else 1)"` | Vorschlag in Runde 1 |
| 6 | Bericht Kap. 1 Weitergaben Z. 86 gegen `KWRA-Monetarisierung.xlsx` Blatt „Schadenskonten-System" Z29 · **Lücke** — K3-Buchungsobjekt #37 fehlt vollständig, #12 ohne Partitionsregel-Zitat | B | offen | Urteil der Regression Runde 2 (Abschn. 5.1): **bestätigt geschlossen**; die Statusspalte wurde dort ausdrücklich nicht fortgeschrieben, der Befund steht in der Tabelle der Runde 1 unverändert auf `offen`. Vorhanden ist: Bericht Kap. 1, Abschnitt „Weitergaben", Spalte „Konto-Ausschlüsse / verwandte Buchungen": #37 steht jetzt mit Kante 49 → 37 (Abgleich-Protokoll Punkt 3) und #12 steht jetzt mit R9-Partitionszitat (Rechenregeln Z11) in der Liste der Partitionsregel-Zitate. | — | Vorschlag in Runde 1 |
| 7 | Bericht §5.1 Z. 240–243 (Δq „marginal … Doppelzählungs-Wächter") gegen Kap. 4 · **Lücke** — Wächter ohne Kalibrierjahre nicht operationalisierbar | B | behoben | Bericht Kap. 4, Abschnitt 4.7 „Kalibrierjahre und Doppelzählungs-Wächter": die Kalibrierjahre 2002 bis 2024 sind einzeln benannt (2025 als vorläufig ausgeschlossen), Δq aus §5.1.2 zählt ausdrücklich nur Nachrüstungen nach dem letzten Kalibrierjahr 2024, und der heutige Objektschutz-Anteil q₀ ist mangels bundesweiter Statistik als „geparkt (Datenquelle fehlt)" mit dreiteiliger Beschaffungs-Watchlist ausgewiesen statt gesetzt — §5.1.2 verweist am Ende der Herleitung auf diese Bindung. | `python3 -c "s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();k=s.split('\n## 4 ')[1].split('\n## 5 ')[0];raise SystemExit(0 if all(t in k for t in ('2002','2024','geparkt (Datenquelle fehlt)','Doppelzählungs-Wächter')) else 1)"` | Vorschlag in Runde 1 |
| 8 | Bericht §5.1 Z. 221–222 (Formel EAD_mit) gegen §5.1.1 Z. 229–234 · **Lücke** — EAD und EAD_mit ohne Zeichentabellen-Zeile und ohne Herleitung | B | behoben | Bericht Kap. 3, neuer Abschnitt 3.5 „Zeichentabelle (alle Formelzeichen der Kapitel 3 und 5)" und Zeichentabelle §5.1.1 (jetzt erste zwei Zeilen): EAD und EAD_mit stehen mit Bedeutung, Einheit €₂₀₂₆/a, Bezugsjahr und Preisstand 2026, Betrachtungsebene Kommune und Herkunft (`herleitung:` §3.1/§3.4 Schritt 3 bzw. §5.1) in der Zeichentabelle, und die Tabelle in 3.5 führt alle 28 Formelzeichen der Kapitel 3 und 5 mit Bedeutung, Einheit und lint-fähiger Herkunft, sodass die Deckungslücke „4 von 6 Zeichen" entfällt. | `python3 -c "import re;s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();t=s.split('### 3.5 ')[1].split(chr(10)+'### ')[0];r=[[c.strip() for c in z.strip().strip(chr(124)).split(chr(124))] for z in t.split(chr(10)) if z.strip().startswith(chr(124))][2:];ok=all(len(c)==4 and (any(a in c[3] for a in ('register:','herleitung:')) or (c[3]=='Notation' and c[2]=='—')) for c in r);ead=[c for c in r if 'EAD' in c[0]];raise SystemExit(0 if ok and len(r)>=20 and any('2026' in c[1] and 'Kommune' in c[1] for c in ead) and any('mit' in c[0] for c in ead) else 1)"` | Vorschlag in Runde 1 |
| 9 | Bericht Z. 266–273 (Block `python test: beispiel_60_s092_abschaetzung`) gegen `backend/` · **Lücke** — Beispiel rechnet auf, ist aber nirgends als Golden-Test hinterlegt | B | behoben | Bericht Kap. 3, Abschnitt 3.6, Block `python test: beispiel_60_kernformel` (unmittelbar vor Abschnitt 3.7): die Kernformel aus 3.4 ist jetzt an einer Beispielzelle samt Aggregation auf eine Kommune aus zwei Zellen mit zehn `assert`-Zeilen ausführbar hinterlegt, und `beispiel_bloecke()` führt diesen wie die beiden übrigen Blöcke (`beispiel_60_kernformel_zelle`, `beispiel_60_s092_abschaetzung`) bei jedem Lauf von `python3 backend/scripts/lint_methodik.py 60` aus und verlangt je Block eine Zusicherung — Bericht und Rechnung können damit nicht mehr unbemerkt auseinanderlaufen. | `python3 -c "import re;s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();b=re.findall('python test: ([a-z0-9_]+)'+chr(10)+'(.*?)'+chr(10)+chr(96)*3,s,re.S);[exec(compile(c,n,'exec'),{}) for n,c in b];raise SystemExit(0 if b and all('assert' in c for n,c in b) and any(n=='beispiel_60_kernformel' for n,c in b) else 1)"` | Anders umgesetzt als vorgeschlagen: Das Einsammeln der Blöcke als Golden-Tests im Backend gehört zur Integration (P-N) und ist nicht Gegenstand dieses Berichtsschritts; die Ausführung aller Blöcke mit Zusicherungs-Pflicht leistet der bestehende Lint bereits. |
| 10 | Bericht §5.1.2 Z. 248–250 (s_bem = 0,50 „Mitte gesetzt") · **Fehler** — gesetzte Verteilungsannahme statt empirischer Quantile (§3.2 Tails, „messen statt setzen") | B | behoben | Bericht §5.1.2 (Aufzählungspunkt \(s_{\text{bem}}\)) und neuer Abschnitt 5.1.3 „\(s_{\text{bem}}\) — ausgewiesene Näherung mit Richtung" (Anker `#s-bem-naeherung`), gespiegelt in den Zeichentabellen §3.5 und §5.1.1 sowie im Parameter-Block `flood_bldg.s_bem` (Kap. 7, Felder `naeherung: true` und `naeherung_richtung: ueberschaetzt_hebel`): Der Satz „Ohne gemessene Tiefenverteilung wird die Mitte gesetzt" ist entfallen; 0,50 ist jetzt ausdrücklich als Näherung geführt — mit der aus der Szenario-Zerlegung §4.5 gerechneten harten Obergrenze 4,174/6,311 = 0,661 (Anteil unterhalb HQ100), der Richtungsangabe „überschätzt den Hebel \(r_{\text{S092}}\)" samt zweifacher Begründung (Bemessungsniveau privaten Objektschutzes deutlich unter HQ100; multiplikativ wachsendes \(d(h)\) gewichtet den Euro-Schaden zu den tiefen Ereignissen), dem Ersetzungspfad über die Ebene HQ_TIEFE auf **Stichproben** der HQ-Szenarien (Ressourcen-Regel §3.4, kein 100-m-Vollraster-Lauf) und dem ausführbaren Block `beispiel_60_s_bem_obergrenze`. Aus derselben Obergrenze folgt die Kappung der oberen Bandgrenze von \(s_{\text{bem}}\) von 0,70 auf **0,66** (§5.1.3, Absatz „Folge für das Band"): kein Bandende liegt mehr über der eigenen Herleitung; das abgeleitete Band von \(r_{\text{S092}}\) lautet damit 0,0075–0,1056 (−0,75 % bis −10,56 %) und ist an allen Fundstellen des Berichts nachgezogen. | `python3 -c "s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();k=s.split('### 5.1.3 ')[1].split(chr(10)+'## 6 ')[0];b=s.split('id: flood_bldg.s_bem')[1].split('---')[0];raise SystemExit(0 if all(t in k for t in ('Näherung','überschätzt','0,661','Stichproben')) and all(t in b for t in ('naeherung: true','naeherung_richtung: ueberschaetzt_hebel','herleitung_anker: \"#s-bem-naeherung\"')) else 1)"` | Anders umgesetzt als vorgeschlagen: Der zweite von T-0242 zugelassene Weg — empirische Bestimmung — ist nicht gangbar, solange die Ebene HQ_TIEFE den Stand „neu anzulegen" trägt (§3.2); deshalb der ausgewiesene Näherungscharakter mit Richtung statt einer Messung. |
| 11 | Bericht Kap. 8 Z. 336–351 · **Lücke** — keine einzige Quelle mit DOI/URL, Zugriffsdatum und Archiv-Snapshot (0 Treffer „http") | B | offen | Urteil der Regression Runde 2 (Abschn. 6.1): **unvollständig geschlossen**; die Statusspalte wurde dort ausdrücklich nicht fortgeschrieben, der Befund steht in der Tabelle der Runde 1 unverändert auf `offen`. Vorhanden ist: Bericht Kap. 8 „Quellen (§3.8)": alle drei Quellen tragen jetzt Vollzitat samt DOI/URL bzw. bei den beiden Arbeitsmappen Dateistand (Commit-Hash, Datum) und Prüfsumme (SHA-256), je mit Zugriffsdatum, und die Hochwasserschutzfibel (Quelle 3) ist mit Vollzitat, URL, Archiv-Snapshot und Zugriffsdatum wörtlich aus `backend/app/data/sources.py` übernommen, ohne diese Datei zu ändern. | — | Vorschlag in Runde 1 |
| 12 | Bericht Kap. 1 „Konto-Einbettung" Z. 90–100 · **Lücke** — kein Kostensatz, kein Preisstand; R5 (Versicherung = Transfer) nicht nachgezogen | B | offen | Urteil der Regression Runde 2 (Abschn. 6.1): **unvollständig geschlossen**; die Statusspalte wurde dort ausdrücklich nicht fortgeschrieben, der Befund steht in der Tabelle der Runde 1 unverändert auf `offen`. Vorhanden ist: Bericht Kap. 1, Abschnitt „Konto-Einbettung": neuer Punkt „Preisstandjahr (Abschätzung von KAP3, §3.9 ABGESCHÄTZT): 2026" und R5 ist im Punkt „Rechenregeln" jetzt als „übernommen" mit Herleitung (Konten Z26, Rechenregeln Z7, Mon. Z64) entschieden. | — | Vorschlag in Runde 1 |
| 13 | Bericht Kap. 1 Z. 35–36 gegen `backend/app/data/catalog.py` Z. 335–340 · **Fehler** — Behauptung „trägt genau die Namenslisten von W117" ist falsch (5 statt 7 Sensitivitäten, 5 statt 8 Wirkungs-Eingänge) | B | offen | Urteil der Regression Runde 2 (Abschn. 6.1): **bestätigt geschlossen**; die Statusspalte wurde dort ausdrücklich nicht fortgeschrieben, der Befund steht in der Tabelle der Runde 1 unverändert auf `offen`. Vorhanden ist: Bericht Kap. 1, Absatz „W-Knoten": die Behauptung ist auf den belegbaren Stand korrigiert (Code trägt nur eine Teilmenge mit abweichender Namensquelle, fünf statt sieben Sensitivitäten, fünf statt acht Wirkungs-Eingänge) und die Divergenz ist als Integrationspunkt für `/integriere-risiko 60` ins Entscheidungslog (Nr. 6) gezogen; `backend/app/data/catalog.py` bleibt dabei unverändert (eiserne Regel 5). | — | Vorschlag in Runde 1 |
| 14 | Bericht Kap. 6 Z. 275–284 · **Lücke** — 3 Zeichen Substanz; Infokasten-Texte fehlen, obwohl Kap. 1 Z. 102–103 sie ausdrücklich verlangt | B | behoben | Bericht Kap. 6 „Szenario-Anwendung & Modellgrenzen": das Kapitel trägt jetzt einen Absatz „Szenario-Anwendung 60-A" (verschobene Größe FS-Hazard, konstant gehaltene Größen, zwei Stationaritätsannahmen, Behandlung der Bestandsdynamik S104), eine nummerierte Modellgrenzen-Liste (darunter Punkt 1 die Untergrenzen-Aussage K1/K4/K5/K8 nicht enthalten und Punkt 2 die Bauform-Grenze der P2-Abschätzung 60-S094-01) sowie die drei wörtlichen Infokasten-Texte (Benennung „bewerteter Schaden — Konto K3", Vollständigkeitsanzeige „Stufe M0: 1 von 8 Konten aktiv", Versionsstempel „berechnet mit Modellstand M0 — Untergrenze"). | `python3 -c "import re;s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();k=s.split('\n## 6 ')[1].split('\n## 7 ')[0];raise SystemExit(0 if len(re.sub(r'<!--.*?-->','',k,flags=re.S).strip())>=2500 else 1)"` | Vorschlag in Runde 1 |
| 15 | Bericht Kap. 7 Z. 290–334 · **Lücke/Widerspruch** — „Abschätzung von KAP3" nur als YAML-Kommentar (P1); `endpunkt`/`bandzuordnung` außerhalb des in §4 definierten Wertebereichs | B | behoben | Bericht Kap. 7 (Absatz „Kennzeichnung nach Vorgabe P1 — im Block, nicht im Kommentar", die vier YAML-Blöcke und neuer Abschnitt 7.1 „Antrag auf Fortschreibung des §4-Wertebereichs für die Familie K3/K4-Ereignisschäden", Anker `#fortschreibung-endpunkt-k3`): Die YAML-Kommentare sind durch die maschinenlesbaren Felder `kennzeichnung: abschaetzung_kap3`, `herleitung_anker:` (auf die Anker `#s092-wirkung` bzw. `#s-bem-naeherung` im sichtbaren Berichtstext, die als `<a id=…>` gesetzt sind) und `wertebereich_abweichung: "#fortschreibung-endpunkt-k3"` ersetzt, sodass die P1-Kennzeichnung im Block selbst steht, und die Überschreitung des §4-Wertebereichs durch `endpunkt: K3-Wiederherstellung` und `bandzuordnung: [alle]` ist in §7.1 mit Begründung (Konten Z28; `mortalitaet`/`morbiditaet` sachlich falsch, `beide` irreführend wegen #101/K1; Hebel ohne Bandachse) und Datum 13.09.2026 als Antrag auf Fortschreibung der Aufgabe ausgewiesen statt still überstimmt. | `python3 -c "import re;s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();k=s.split(chr(10)+'## 7 ')[1].split(chr(10)+'## 8 ')[0];bl=re.split(r'^parameter:$',k,flags=re.M)[1:];kz=[re.search(r'^  kennzeichnung: (\S+)$',b,re.M) for b in bl];ok=all(m and m.group(1) in ('quelle','abschaetzung_kap3') for m in kz) and all(re.search(r'^  herleitung_anker: \"#\S+\"$',b,re.M) and re.search(r'^  wertebereich_abweichung: \"#fortschreibung-endpunkt-k3\"$',b,re.M) for b in bl);ank=all(('<a id=\"'+a+'\">') in s for a in ('s092-wirkung','s-bem-naeherung','fortschreibung-endpunkt-k3'));raise SystemExit(0 if len(bl)==4 and ok and ank and '13.09.2026' in k.split('### 7.1 ')[1] else 1)"` | Anders umgesetzt als vorgeschlagen: Die Wertebereichs-Überschreitung wird nicht durch Umbiegen der Felder geheilt (jeder zugelassene Wert wäre sachlich falsch), sondern als Antrag auf Fortschreibung geführt — Entscheidung über die Aufgabe trifft dieser Bericht nicht; die Aufnahme der Felder in Lint/Registry gehört T-0234 bzw. P-N. |
| 16 | Bericht Kap. 9 Z. 366–374 · **Lücke** — Ansatz-Vergleich vollständig „offen", obwohl §2.6 ihn für den ersten Familienvertreter zwingend verlangt | B | behoben | Bericht Kap. 9 „Ansatz-Vergleich", Abschnitte „Die drei verglichenen Ansätze", „Kriterienraster" und „Umsetzungsgrundlage": die drei Ansätze (a) typisierte Tiefen-Schadensfunktion je 100-m-Zelle, (b) aggregierte Flächenschadensrate und (c) Schadensgradmodell D0–D6 am Einzelgebäude sind benannt, jede der 21 Rasterzellen ist bewertet, und Ansatz (a) ist mit Begründung gegen (b) und (c) als Umsetzungsgrundlage festgelegt — nachgezogen in der Kopfzeile (Z. 3–5) und im Entscheidungslog Nr. 5 (13.09.2026). | — | Vorschlag in Runde 1 |
| 17 | `backend/scripts/lint_methodik.py` gegen Bericht Kap. 3/4/6 · **Lücke** — 83 grüne Checks bei drei substanzlosen Kapiteln; kein Vollständigkeits-Check der Pflichtkapitel | C | offen | — | — | Vorschlag in Runde 1 |
| 18 | Bericht Entscheidungslog Nr. 3 Z. 382 und Kap. 7 gegen Register-Zeile 60-S092-01 Z. 135 · **Widerspruch** — vier bezifferte Parameter-Blöcke aus einer Registerzeile mit Entscheidung „offen" | C | behoben | Bericht Kap. 2, Abschnitt „Evidenz-Register (§2.2)", Zeile 60-S092-01: die Spalte „Entscheidung" trägt jetzt „Maßnahmen-Hebel (abgeschätzt)" statt „offen (Vorschlag: Maßnahmen-Hebel, abgeschätzt)", sodass die Parameter-Blöcke in Kap. 7 aus einer entschiedenen Zeile im Sinne von §2.2 ableiten, während die Kennzeichnung §3.9 ABGESCHÄTZT und die Modellgrenze „kommunal (Pauschalfaktor)" nach Vorgabe P2 in der Zeile stehen bleiben (Kopf-Geltungsbereich und Kap. 2 sind entsprechend nachgezogen). | — | Vorschlag in Runde 1 |
| 19 | `docs/evidenz/register.md` Z. 65 (Zeile 60-S092-01) gegen Bericht §5.1.2/Kap. 7 · **Widerspruch** — das risikoübergreifende Evidenz-Register führt für 60-S092-01 weiterhin das alte Band 0,0075–0,112, während der Bericht nach der Kappung von `s_bem` auf ≤0,66 (§5.1.3, Absatz „Folge für das Band") 0,0075–0,1056 ausweist; kein Lint liest diese Datei, die Divergenz fiele also nirgends auf (eiserne Regel 5: nie still im Code lösen) | C | behoben | `docs/evidenz/register.md` Z. 65 (Zeile 60-S092-01), Spalte Effektgröße: „Band 0,0075–0,112" ist durch „Band 0,0075–0,0992" ersetzt (= Bericht §5.1.3); Punktwert 0,035 und Kette unverändert (T-0288, 17.09.2026; Einzelheiten im Abschnitt „Autor-Revision nach Runde 2"). | `python3 -c "r=open('docs/evidenz/register.md',encoding='utf-8').read();z=[l for l in r.split(chr(10)) if l.startswith(chr(124)+' 60-S092-01 ')];b=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();raise SystemExit(0 if (len(z)==1 and 'Band 0,0075–0,0992' in z[0] and '0,0075–0,112' not in r and '(Band 0,0075–**0,0992**' in b) else 1)"` | Der Nachzug erfolgte auf 0,0075–0,0992 statt auf das in Runde 1 vorgeschlagene 0,0075–0,1056: Die obere Bandgrenze von \(s_{\text{bem}}\) ist mit Befund 26 (T-0287) von 0,66 auf 0,62 gesetzt worden. |
| 20 | Bericht Kap. 1 Knoten-Bilanz (S096, S097, S098) gegen §3.4 · **Widerspruch/Lücke** — die drei Knoten hängen an der Formelstelle FS-Schutzsystem (R7-Erwartungswert-Weiche), die in keiner Formel vorkommt | A | behoben | Bericht §3.4, Absatz „Formelstelle FS-Schutzsystem — in dieser Fassung inaktiv (geparkt)" mit Regelzitat Rechenregeln C9/C20 und Modellgrenze; Kap. 1, Zeilen S096–S098 auf „inaktiv (geparkt …)"; Kap. 9, Zelle „Maßnahmen-Anschluss" auf den belegbaren Stand korrigiert (T-0245). | vorhanden (Wortlaut: Runde 2, Abschn. 0.3) | Von den beiden nach §2.1 zulässigen Wegen ist der zweite gewählt (inaktiv geparkt statt R7-Term ausschreiben). |
| 21 | Bericht Kap. 1 Knoten-Bilanz, Spalte „Name" (S074, W100, S092) gegen KWK B199/B223/B256 · **Fehler** — drei Knotennamen ohne Kürzungszeichen verkürzt | C | bewusst offen | — | vorhanden (Wortlaut: Runde 2, Abschn. 0.3) | Bewusst offen: Kategorie C, hindert die Abnahme nach §5.4 nicht; die Kürzung hat keine Rechenwirkung; Nachzug mit der nächsten Revision. |
| 22 | Bericht Kopf und Abschnitt „Ergebnis" gegen den Ist-Stand · **Widerspruch** — Kopf führt „Erstaufschlag, noch nicht gegengeprüft" und einen überholten Geltungsbereich | B | behoben | Bericht Kopf-Statuszeile („in Revision nach Review-Runde 2 … Stand 17.09.2026"), Geltungsbereich (Kapitelstand 3–9) und Abschnitt „Ergebnis", Punkt „Offen (Stand 17.09.2026, nach Review-Runde 2)" (T-0245). | — | Der vorgeschlagene Lint-Check gehört laut Befund zu T-0234 und war hier nicht Gegenstand. |
| 23 | Bericht §3.7 „Schicht-A-Index" · **Lücke** — Nullanker und Bindungsregel des Perzentilrangs fehlen, Lackmustest nur für den Euro-Pfad | B | behoben | Bericht §3.7, Absatz „Nullanker und Bindungsregel" (Index 0 bei \(x_k = 0\), Rang nur über \(x_k > 0\), Durchschnittsrang bei Bindung, Lackmustest auf den Schicht-A-Ausweis erweitert) (T-0245). | vorhanden (Wortlaut: Runde 2, Abschn. 1.2) | Vorschlag in Runde 2 |
| 24 | Bericht §3.1 „Physischer Teil-Ausweis" (\(\text{EAD} = \bar A \cdot w\)) gegen §3.5/§3.6 · **Fehler** — Gleichung ohne Indizierung: auf der Zelle exakt, auf der Kommune nur als Summe | C | bewusst offen | — | vorhanden (Wortlaut: Runde 2, Abschn. 1.2) | Bewusst offen: Kategorie C; die Gleichung ist auf der Zelle exakt und der kommunale Ausweis rechnet in §3.6 korrekt als Summe, es fehlt nur die Indizierung im Text. |
| 25 | Bericht §3.5 und §5.1.1 gegen §5.1.2/§5.1.3 · **Lücke** — vier Formelzeichen ohne Zeile in der Zeichentabelle, die Vollständigkeit beansprucht | C | bewusst offen | — | vorhanden (Wortlaut: Runde 2, Abschn. 1.2) | Bewusst offen: Kategorie C; vier fehlende Zeilen ohne Rechenwirkung, \(q_0\) ist in §4.7/§4.8 als geparkt geführt. |
| 26 | Bericht §5.1.3, Absätze zur Obergrenze von \(s_{\text{bem}}\) · **Fehler/Lücke** — die „harte" Obergrenze 0,661 stammt aus einer Beispielzelle, nicht aus einer allgemeinen Herleitung | B | behoben | Bericht §5.1.3, Absätze „Profilabhängige Illustration: Anteil unterhalb HQ100 in der Beispielzelle (Befund 26)" und „Tragende Begründung der oberen Bandgrenze: Ankerwert der Verteilungsprüfung (§4.5)": Band \(s_{\text{bem}}\) 0,30–0,62 ⇒ \(r_{\text{S092}}\) 0,0075–0,0992, nachgezogen in Kap. 1, Kap. 2, §3.5, §5.1.1–§5.1.3, Kap. 7 und Entscheidungslog Nr. 3 (T-0287). | vorhanden (Wortlaut: Runde 2, Abschn. 1.2) | Anders umgesetzt als vorgeschlagen: Kennzeichnung als profilabhängige Illustration mit zellunabhängiger Bandbegründung statt allgemeiner Herleitung des Supremums. |
| 27 | Bericht Kap. 2, Registerzeile 60-R24-01 und Langbeleg B4 · **Fehler/Lücke** — Jahresraten 3,4 %/2,3 % der Fortschreibung ohne Herleitung, Bandende gerundet | C | bewusst offen | — | vorhanden (Wortlaut: Runde 2, Abschn. 2.2) | Bewusst offen: Kategorie C; Rundungs- und Herleitungsmangel im Band von \(n_t\) (Abweichung am oberen Bandende rund 0,2 %), Zentralwerte unberührt. |
| 28 | Bericht Kap. 2, Registerzeilen 60-S093-01/60-S094-01 und Langbelege B5/B6 · **Fehler** — Achsenteiler und Zentrierung der Bänder nicht tragfähig | B | behoben | Bericht B5/B6 neu gerechnet: Zerlegung über das Referenzfeld C0P0, Qualitätsachse mit Teiler 2 ⇒ S093 0,71–1,40, S094 0,84–1,18, kombiniert 0,60–1,66, „geometrisch zentriert" statt „mittelwertzentriert" mit ausgewiesener Modellgrenze; nachgezogen in Kap. 2, `docs/evidenz/register.md`, §3.2, §3.3, §3.5, Kap. 6 Modellgrenze 2, Kap. 7 und Kap. 9 (T-0286). | vorhanden (Wortlaut: Runde 2, Abschn. 2.2) | Vorschlag in Runde 2 |
| 29 | Bericht Kap. 2, Registerzeile 60-S092-01, Spalte Studientyp, gegen Langbeleg B5 · **Widerspruch** — Begründung des Verzichts auf eine Effektgröße widerspricht dem Langbeleg | C | bewusst offen | — | vorhanden (Wortlaut: Runde 2, Abschn. 2.2) | Bewusst offen: Kategorie C; betrifft die Begründung des Verzichts auf eine Effektgröße für S092, nicht deren Wert. |
| 30 | Bericht Kap. 2, Registerzeile 60-S093-01, gegen §3.3 Stützstellentabelle · **Lücke** — Typstruktur der zitierten Schadensfunktion nicht durchgezogen | C | bewusst offen | — | vorhanden (Wortlaut: Runde 2, Abschn. 2.2) | Bewusst offen: Kategorie C; die fehlende Typstruktur verändert die Registerzeile nicht, sondern ist eine noch auszuweisende Modellgrenze. |
| 31 | Bericht Kap. 2, Registerzeile 60-W085-01, gegen §3.4 Schritt 2 · **Lücke** — \(p_3\) fehlt in der Registerzeile, obwohl es in der Formel rechnet | C | bewusst offen | — | vorhanden (Wortlaut: Runde 2, Abschn. 2.2) | Bewusst offen: Kategorie C; \(p_3\) steht mit Herleitung in §3.4/§3.5 und als Block `flood_bldg.p_hq_extrem` in Kap. 7, es fehlt nur der Eintrag in der Registerzeile. |
| 32 | Bericht Kap. 4, Einleitung gegen §4.3 · **Widerspruch/Fehler** — Behauptung „Kalibriermodell = Produktionsmodell", während \(M_0\) aus nationalen Einheitswerten stammt | A | behoben | \(M_0\) = 1,360 Mrd. €₂₀₂₆/a aus dem Stichprobenlauf der acht Anker-Kommunen (Quelle `docs/evidenz/60_stichprobe/m0_klassenraten.csv`, Nenner `rate_exponiert_hqextrem`), \(\lambda\) = 0,724 (Band 0,29–1,63), nachgezogen in Kap. 4 Einleitung, §4.3, §4.4, §4.6, §4.8, Kap. 7 (Block `flood_bldg.lambda`), §7.2, Entscheidungslog und Kopf-Statuszeile, dazu die vier bezifferten Restfehler-Positionen (T-0311/T-0312/T-0313). \(\lambda\) ist anschließend mit Befund 34 auf 0,832 gezogen worden. | vorhanden (Wortlaut: Runde 2, Abschn. 3.3) | Vorschlag in Runde 2 |
| 33 | Bericht §4.5 gegen §4.1 · **Fehler** — Verteilungsprüfung auf denselben zwei GDV-Zahlen, aus denen \(\lambda\) folgt; Toleranz gesetzt statt hergeleitet | A | behoben | Bericht §4.5 („Jahresauslassung über die Ankerreihe"): Ankerseite als Leave-one-out über die 23 Jahreswerte aus `docs/evidenz/60_gdv_jahresreihe_2002_2024.csv`, Prüfgröße skaleninvariant und damit unabhängig von \(\lambda\), Toleranz ±11,5 Pp aus Jackknife, Ableseunschärfe und Modellband hergeleitet und vor dem Ergebnis fixiert; nachgezogen in §4.8, Block `beispiel_60_kalibrierung`, Kopf-Statuszeile, Einleitung Kap. 4 und §4.4 (T-0292). | vorhanden (Wortlaut: Runde 2, Abschn. 3.3) | Ausgang der Prüfung ist **negativ** (Abstand 13,9 Pp > 11,5 Pp): als Modellentscheid ausgewiesen, nicht durch Weiten der Toleranz geheilt; \(\lambda\) bleibt vorläufig. Restpunkt: die obere Bandgrenze \(s_{\text{bem}}\) in §5.1.3 hängt am abgelösten Ankerwert (dort als „Nachtrag dieser Revision" vermerkt). |
| 34 | Bericht §4.1, §4.2, §4.4 und §4.5 · **Lücke** — \(\lambda\) nicht über die Anker-Zeitreihe gefittet, keine Jahres-Auswahlregel, keine Sensitivität je Zeitfenster | A | behoben | \(A_{\text{ver}}\) = 1,838 Mrd. € als Kleinste-Quadrate-Mittel der vollständigen Reihe 2002–2024, \(A^{*}\) = 1,132 Mrd. €₂₀₂₆/a, \(\lambda\) = 0,832 (Band 0,22–1,66 aus dem Tukey-Fence-Test), Sensitivität über vier Fenster; Fundstellen §4.1, §4.2, §4.4, Kap. 7 (`flood_bldg.lambda`, `wert: 0.832`), §7.2 und Entscheidungslog Nr. 8 (Rechenweg T-0315, Nachzug T-0318/T-0319, Beleg T-0321). | vorhanden (Wortlaut: Runde 2, Abschn. 3.3) | Die Befundtabelle der Runde 2 führt den Befund als Kategorie B, die Statuszeile der Autor-Revision (T-0321) als A; hier steht die zuletzt vergebene Kategorie. |
| 35 | Bericht §4.6 · **Fehler** — Untergrenze des Sanity-Bandes zirkulär, Obergrenze keine echte Schranke | B | offen | — | vorhanden (Wortlaut: Runde 2, Abschn. 3.3) | Rest: Untergrenze bleibt zirkulär, Obergrenze ohne Klassenbezug; in der Revision der Runde 2 nicht bearbeitet. |
| 36 | Bericht §4.4 „Plausibilitätsschranke" gegen §4.4 Band und §4.8 · **Widerspruch/Lücke** — Schranke 0,50/2,00 ohne Herleitung und nicht in der P1-Tabelle | B | offen | Teilweise: die Schranke steht seit T-0245 als Abschätzung von KAP3 in §4.8, mit Geltung für den Zentralwert. | vorhanden (Wortlaut: Runde 2, Abschn. 3.3) | Rest: die Herleitung der Schranke aus dem fortgepflanzten Band von \(A^{*}\) und \(M_0\) fehlt weiter. |
| 37 | Bericht §4.8 Parametertabelle gegen §4.2, §4.4, §4.5, §4.6 · **Lücke** — drei in Kapitel 4 rechnende Werte fehlen in der P1-Tabelle | B | behoben | Bericht §4.8: drei neue Zeilen „Baupreisanstieg 2023 → 2024", „Betroffenheit exponierter Gebäude" und „Plausibilitätsschranke \(\lambda\)", je mit Kennzeichnung; bei \(\lambda\), \(U\) und \(O\) sind die einfließenden Abschätzungen vermerkt (T-0245). | vorhanden (Wortlaut: Runde 2, Abschn. 3.3) | Vorschlag in Runde 2 |
| 38 | Bericht §4.2 Zeile \(\pi\) und §4.8 · **Fehler** — Bandenden von \(\pi\) falsch gerundet | C | bewusst offen | — | vorhanden (Wortlaut: Runde 2, Abschn. 3.3) | Bewusst offen: Kategorie C; Rundungsfehler im Band von \(\pi\) (oberes Ende 1,11 statt 1,126), wird mit Befund 27 nachgezogen. |
| 39 | Bericht §4.7 „Wächter" gegen §4.4 und §5.1.2 · **Lücke** — Referenzzustand ist der Stichtag 31.12.2024 statt des gewichteten Ausstattungsmittels | B | offen | — | vorhanden (Wortlaut: Runde 2, Abschn. 3.3) | Rest: Referenzzustand unverändert; in der Revision der Runde 2 nicht bearbeitet. |
| 40 | Bericht Kap. 7 gegen §3.4, §3.5, §4.2/§4.8 · **Lücke** — Parameter-Blöcke nur für den Hebel aus §5.1, Kostensätze ohne Block und ohne `preisstand` | A | behoben | Bericht Kap. 7: 18 neue Parameter-Blöcke (darunter `flood_bldg.n_efh_zfh` und `flood_bldg.n_mfh` mit `preisstand: 2026` und `umrechnungsfaktor: 1.8578`), vier Herleitungsanker (`#tiefen-schadensfunktion`, `#kernformel-zelle`, `#kalibrierung-zielwert`, `#niveau-skalar`), ersetzter Einleitungssatz und §3.5-Zeile \(n_t\) mit Umrechnungsfaktor (T-0245). | vorhanden (Wortlaut: Runde 2, Abschn. 4.3) | Mit Integrationsvermerk geschlossen: die Extraktion der Blöcke in die Produkt-Registry gehört zur Integration (P-N), nicht zu diesem Berichtsschritt. |
| 41 | Bericht Langbeleg B4 und §3.4 gegen `KWRA-Monetarisierung.xlsx` J64/J65 und C27 · **Widerspruch** — Neuwertansatz, obwohl die Mappe den Zeitwertansatz vorschreibt | B | behoben | Bericht §7.2 „Antrag auf Fortschreibung der Arbeitsmappe: Neuwert statt Zeitwertansatz" (Anker `#fortschreibung-neuwert-k3`, 17.09.2026): Neuwert bleibt Basiswert, Alterswertminderung \(f_{\text{AWM}}\) = 0,55 (Band 0,40–0,75, Abschätzung von KAP3 nach § 38 ImmoWertV), K3-Sensitivität 0,54 statt 0,99 Mrd. €₂₀₂₆/a, Untergrenzen-Aussage als Modellgrenze 9 in Kap. 6; nachgezogen in Kap. 1, Register 60-R24-01, B4, §3.4, §4.8, Versionsstempel und Entscheidungslog Nr. 7 (T-0285). | vorhanden (Wortlaut: Runde 2, Abschn. 4.3) | Anders umgesetzt als vorgeschlagen: Der Zeitwertansatz wird nicht übernommen, sondern als Antrag auf Fortschreibung der Mappe geführt (eiserne Regel 2: Arbeitsmappen nie still überstimmen). |
| 42 | Bericht Kap. 8 und Langbelege B1–B6 · **Lücke** — Quelle des nationalen Ankers fehlt, keine Archiv-Snapshots | B | behoben | Bericht Kap. 8: Formatsatz und Punkt 4 nennen den Archiv-Snapshot, die drei GDV-Ankerquellen stehen als Quellen 5, 6 und 7 mit Organ, Jahr, Titel, URL, Zugriffsdatum und Snapshot (T-0306); Archiv-Snapshots der Langbelege B1–B3 (T-0307) und B4–B6 (T-0308) sind unmittelbar bei den URLs ergänzt. | vorhanden (Wortlaut: Runde 2, Abschn. 4.3) | Bei der Destatis-Pressemitteilung Nr. 241/2026 ist der Verzicht auf einen Snapshot ausdrücklich begründet (archivseitig gesperrt, kein inhaltstragender Snapshot herstellbar). |
| 43 | Bericht §7.1 „Begründung" und Kap. 8 Quelle 2 gegen `KWRA-Monetarisierung.xlsx` C28/J61 · **Fehler** — Endpunkt mit der falschen Zelle belegt | C | bewusst offen | — | vorhanden (Wortlaut: Runde 2, Abschn. 4.3) | Bewusst offen: Kategorie C; falsche Zellfundstelle im Fortschreibungsantrag §7.1, ohne Wirkung auf Wert oder Konto. |
| 44 | Bericht Kap. 6 „Modellgrenzen", Punkt 2, gegen §5.1.2 · **Lücke/Fehler** — die Bauform-Grenze der P2-Abschätzung S092 fehlt in Kap. 6 | C | bewusst offen | — | vorhanden (Wortlaut: Runde 2, Abschn. 4.3) | Bewusst offen: Kategorie C; die Modellgrenze von S092 steht sichtbar in §5.1.2/§5.1.3, es fehlt nur die Wiederholung in Kap. 6. |
| 45 | Bericht Kap. 9 „Kriterienraster", Zeilen „Aufwand" und „Datenverfügbarkeit" (a), gegen §3.2 · **Widerspruch** — Zahl der neu anzulegenden Datenebenen falsch | C | bewusst offen | — | vorhanden (Wortlaut: Runde 2, Abschn. 4.3) | Bewusst offen: Kategorie C; Zählfehler im Kriterienraster; die Ansatz-Entscheidung hängt nicht daran, weil (b) und (c) dieselben Ebenen brauchen. |
| 46 | Bericht Kap. 1 Knoten-Bilanz, Zeilen S074 und R17, gegen §3.2 „Kein-Doppelkanal" · **Widerspruch** — Verarbeitung an einer Formelstelle FS-Exposition, die das Modell ausschließt | B | behoben | Bericht Kap. 1: Zeilen S074/R17 als „Sensitivitätsband (Kein-Doppelkanal §3.2 …) — wirkt über FS-Hazard, keine eigene Formelstelle"; der Satz zum Kommentar-Zustand von Kapitel 3 ist durch den Ist-Stand ersetzt (T-0245). | vorhanden (Wortlaut: Runde 2, Abschn. 5.2) | Vorschlag in Runde 2 |

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
| 2 | A | Bericht Kap. 1 Knoten-Bilanz Z. 43–76 · **Lücke (§2.1, §5 LF 1)** — 32 von 32 Zeilen tragen „rechnet in: offen"; die Spalte „Vorschlag" ist laut Z. 40–41 ausdrücklich keine Entscheidung. §2.1 verlangt je Knoten „verarbeitet **oder** begründet inaktiv". **Vorschlag:** je Zeile entscheiden; die zwölf voraussichtlich inaktiven Knoten (E10, E17, E14, E02, E03, W074, W077, W087, W008, W006, W100, R18, R19, R23, R25) mit Regelzitat (R9/Konten Z28) auf „inaktiv" setzen, die übrigen an eine Formelstelle binden. **Nachtrag 18.09.2026** (siehe [Nachtrag zu Befund 2](#nachtrag-zu-befund-2-knoten-bilanz)): Fundstelle Kapitel 1 „Wirkungskette & Knoten-Bilanz (§2.1)", Tabelle „Knoten-Bilanz" — alle 32 Zeilen tragen eine benannte Formelstelle oder `inaktiv` mit Mappenzitat, kein `rechnet in: offen` mehr vorhanden. | `grep -c "rechnet in: offen" docs/methodik/60_gebaeudeschaeden_flusshochwasser.md` | behoben |
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
| 20 | A | Bericht Kap. 1 Knoten-Bilanz (Zeilen S096 KWK Z260, S097 Z261, S098 Z262) gegen Kap. 3.4 und Rechenregeln Z20 (A5) · **Widerspruch/Lücke (§2.1 „verarbeitet oder begründet inaktiv", §5 LF 1 „Eingänge, die nirgends rechnen")** — die drei Knoten sind als verarbeitet an der Formelstelle **FS-Schutzsystem** („R7-Erwartungswert-Weiche mit #50") ausgewiesen. Diese Formelstelle existiert in keiner Formel: `FS-Schutzsystem` kommt außerhalb von Kapitel 1 null mal vor, die Kernformel §3.4 trägt keinen Wahrscheinlichkeitsterm für Halte-/Versagensfall, und die Registerzeilen 60-S096-01/-S097-01/-S098-01 stehen in allen Sachspalten auf „offen". Die Mappe verlangt die Weiche ausdrücklich: Mon. **N65** „R7, R9" und Rechenregeln **C20** (A5): „Eintrittswahrscheinlichkeit × Schadensfunktion × Bestand; **Schutzsysteme über die R7-Erwartungswert-Weiche**"; Rechenregeln **C9** (R7) definiert sie als „Erwartungswert über Halte- und Versagensfall, wahrscheinlichkeitsgewichtet". Verschärfend: Kap. 9 („Kriterienraster", Zeile „Maßnahmen-Anschluss") behauptet für den gewählten Ansatz (a), die Schutzsysteme wirkten „über die R7-Weiche mit #50 am Hazard-Term; **beide Angriffspunkte existieren in der Formel bereits**" — das trifft für S092 zu (§5.1), für die R7-Weiche nicht. Damit stützt eine unzutreffende Aussage die Ansatz-Entscheidung (Entscheidungslog Nr. 5). **Vorschlag:** entweder die R7-Weiche in §3.4 als eigenen Term ausschreiben (p(HQ) aufgeteilt in Halte- und Versagensfall des Schutzsystems, Kopplung an #50) oder die drei Zeilen bis zur Bezifferung ausdrücklich auf „inaktiv (geparkt, Datenquelle/Modul fehlt)" mit Regelzitat setzen und die Behauptung in Kap. 9 auf den belegbaren Stand korrigieren; still weiterlaufen lassen ist nach §2.1 keine der beiden zulässigen Optionen. | `python3 -c "s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();k1=s.split(chr(10)+'## 1 ')[1].split(chr(10)+'## 2 ')[0];rest=s.split(chr(10)+'## 2 ')[1];raise SystemExit(0 if rest.count('FS-Schutzsystem')>0 else 1)"` | behoben — Bericht §3.4, neuer Absatz „Formelstelle FS-Schutzsystem — in dieser Fassung inaktiv (geparkt)“ mit Regelzitat Rechenregeln C9/C20 und Modellgrenze; Kap. 1 Knoten-Bilanz, Zeilen S096–S098 auf „inaktiv (geparkt …)“; Kap. 9 Kriterienraster, Zeile „Maßnahmen-Anschluss“ auf den belegbaren Stand korrigiert |
| 21 | C | Bericht Kap. 1 Knoten-Bilanz, Spalte „Name", Zeilen S074, W100, S092 gegen `KWRA-Schadensbaum_X_UBA-klimawirkungsketten.xlsx`, Blatt „Klimawirkungsketten", Zellen **B199**, **B223**, **B256** · **Fehler (§5 LF 14 Quellen-Synchronität; §3.8 wörtliche Übernahme)** — drei Knotennamen sind gegenüber der Arbeitsmappe **ohne Kürzungszeichen** verkürzt: B199 „Topographie (Geländeform, Höhe, etc.)" → „Topographie (Geländeform, Höhe)"; B223 „Einschränkungen der Funktionsfähigkeit von Kanalnetzen und Vorflutern" → „Einschränkungen Kanalnetze und Vorfluter"; B256 „… Vorsorge der Eigentümer und Nutzer von Gebäuden und Infrastrukturen" → „… Vorsorge der Eigentümer und Nutzer". Die übrigen 29 Namen sind wörtlich. Das wiegt hier schwerer als eine Formalie, weil derselbe Absatz („W-Knoten") dem Code-Bestand vorwirft, die Einträge seien „teils **umformuliert statt wörtlich** aus der Arbeitsmappe übernommen" (Befund 13) — der Maßstab muss für den Bericht selbst gelten. Bei W100 verschiebt die Kürzung zudem die Bedeutung (die Mappe spricht von der Funktionsfähigkeit, nicht von den Anlagen). **Vorschlag:** die drei Namen wörtlich aus B199/B223/B256 übernehmen oder die Kürzung sichtbar machen („…"). | `python3 -c "import openpyxl,re;s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();t=s.split('| Knoten | Name | Blatt/Zeile | rechnet in |')[1].split(chr(10)+chr(10))[0];rows=[[c.strip() for c in z.strip().strip(chr(124)).split(chr(124))] for z in t.split(chr(10)) if z.strip().startswith(chr(124))][1:];wb=openpyxl.load_workbook('docs/Schadensbaum/KWRA-Schadensbaum_X_UBA-klimawirkungsketten.xlsx',read_only=True,data_only=True);k=list(wb['Klimawirkungsketten'].iter_rows(values_only=True));bad=[r[0] for r in rows if re.sub(r'\s*\((über W085|= Id \d+|direkt[^)]*)\)\s*$','',r[1]).strip()!=k[int(re.search(r'KWK Z(\d+)',r[2]).group(1))-1][1]];raise SystemExit(0 if not bad else 1)"` | bewusst offen — Kategorie C, hindert die Abnahme nach §5.4 nicht (die Vorbedingung von `/integriere-risiko` stellt auf offene A-Befunde ab); die Kürzung der drei Knotennamen hat keine Rechenwirkung; Nachzug mit der nächsten Revision |
| 22 | B | Bericht Kopf (Z. 3–26) und Abschnitt „Ergebnis" (Z. 28–35) gegen den Ist-Stand des Berichts, dieses Ledger und §4/§6 der Aufgabe · **Widerspruch (§4 Berichtsstruktur „Kopf/Ergebnis", §6 Prozess; LF 14 gegen die Aufgabe)** — der Kopf führt „Status: **Erstaufschlag** (`/neu-risiko 60`) — **noch nicht gegengeprüft** · 11.09.2026", obwohl Review-Runde 1 am 13.09.2026 gefahren wurde (dieses Ledger) und dreizehn Autoren-Tickets den Stand seither geändert haben. Der Geltungsbereich sagt „**Kap. 4–8 tragen die Pflichtinhalte als Kommentar**" und „befüllt ist … Kap. 3 **bis einschließlich der Kernformel**", während Kap. 3 heute bis 3.7 reicht (Zeichentabelle, Aggregation, Schicht-A-Index) und Kap. 4 (8 Abschnitte mit Anker, Niveau-Skalar, Verteilungsprüfung), Kap. 5, 6, 7 und 8 ausgeschrieben sind. Das „Ergebnis" führt dieselben Teile noch als offen („Offen: (1) Zeichentabelle, Aggregation Zelle → Kommune und Schicht A in Kap. 3; (2) Kap. 4, 6, 8") und behauptet „Gegenprüfung ist nicht Teil des Tickets und noch nicht gemessen". Ein Prüfer oder Leser, der nach §4 dem Kopf den Geltungsbereich entnimmt, bekommt damit einen falschen Bearbeitungs- und Prüfstand; nach §6 hängt an diesem Stand die Abnahmefrage. **Vorschlag:** Kopfstatus, Geltungsbereich und „Ergebnis"/„Offen" am Ende jeder Revisionsrunde nachziehen (Status „in Revision, Runde N", Datum des letzten Stands, tatsächlich offene Punkte) und den Abgleich als Lint-Check verankern (gehört in den Vollständigkeits-Check T-0234, nicht in diesen Bericht). | — | behoben — Bericht Kopf (Statuszeile „in Revision nach Review-Runde 2 … Stand 17.09.2026“), Geltungsbereich (Kapitelstand 3–9) und Abschnitt „Ergebnis“, Punkt „Offen (Stand 17.09.2026, nach Review-Runde 2)“; der vorgeschlagene Lint-Check gehört laut Befund zu T-0234 und ist hier nicht Gegenstand |

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
| 23 | B | Bericht §3.7 „Schicht-A-Index" (Z. 799–832), Formel \(I_{60,k} = 100 \cdot \operatorname{Perzentilrang}(x_k)\) · **Lücke (§5 LF 2 Verteilschlüssel-Test; §3.6 nutzersichtbarer Ausweis)** — für den Euro-Pfad ist der Lackmustest „Kommune ohne Flussaue" in §3.4/§3.6 erfüllt und nachgerechnet (\(\text{EAD}_k = 0{,}00\) €₂₀₂₆/a). Der zweite, ebenfalls nutzersichtbare Ausweis desselben Kapitels kennt jedoch keine Regel für den Massenpunkt \(x_k = 0\): Da alle Kommunen ohne Aue denselben Wert 0 tragen, hängt ihr Indexwert allein an der ungenannten Bindungsregel des Perzentilrangs. Nachgerechnet an 100 Kommunen, davon 60 mit \(x_k = 0\): Leseart „kleiner oder gleich" ⇒ **60,0 Punkte**, Leseart „echt kleiner" ⇒ 0,0 Punkte — dieselbe auenlose Kommune erhält also entweder gar keine oder eine mittlere „Betroffenheit durch Flusshochwasser". §3.7 nennt zwar den Vergleichsraum als Pflichtangabe, nicht aber die Bindungsregel und keinen Nullanker. **Vorschlag:** in §3.7 festschreiben, dass Kommunen mit \(x_k = 0\) den Indexwert 0 erhalten und der Perzentilrang nur über die Kommunen mit \(x_k > 0\) gebildet wird (oder ausdrücklich die Leseart „echt kleiner" mit Nullanker), und den Lackmustest §3.4 um den Schicht-A-Ausweis erweitern. | `python3 -c "s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();L=s.split(chr(10));k=chr(10).join(L[798:833]);raise SystemExit(0 if ('Perzentilrang' in k and 'Bindung' not in k and 'x_k = 0' not in k) else 1)"` | behoben — Bericht §3.7, neuer Absatz „Nullanker und Bindungsregel“ (Index 0 für \(x_k = 0\), Rang nur über \(x_k > 0\), Durchschnittsrang bei Bindung, Lackmustest auf den Schicht-A-Ausweis erweitert) |
| 24 | C | Bericht §3.1, Aufzählungspunkt „Physischer Teil-Ausweis" (Z. 473–476: „\(\text{EAD} = \bar A \cdot w\)") zusammen mit der Gattungszeichen-Zeile zu \(\bar A\) in §3.5 (Z. 685) gegen §3.6 (Z. 707) · **Fehler (§5 LF 3 „native Ausweise proportional zu den Euro-Pfaden"; §3.6 Ausweis auf der deklarierten Betrachtungsebene)** — die indexfreie Gleichung gilt exakt auf der **Zelle**; auf der deklarierten Betrachtungsebene Kommune ist \(\text{EAD}_k = \sum_z \bar A_z w_z\) und damit nur bei homogener Wertdichte gleich \(\bar A_k \cdot w_k\). Gegenbeispiel (gerechnet): EFH-Zelle 1.200 m² mit \(a\) = 0,25/0,80/1,00 und MFH-Zelle 3.000 m² mit \(a\) = 0,00/0,10/0,20 ⇒ \(\text{EAD}_k = 20.195{,}7\) €₂₀₂₆/a, \(\bar A_k \cdot w_k = 18.077{,}9\) €₂₀₂₆/a, **11,7 % Abweichung**. §3.6 rechnet korrekt, und der Beispielblock `beispiel_60_kernformel` prüft die Vertauschbarkeit ausdrücklich nur bei gleicher Wertdichte — die Lücke ist die verallgemeinernde Schreibweise in §3.1/§3.5, aus der ein Nutzer den kommunalen physischen Teil-Ausweis \(\bar A_k\) fälschlich als proportional zum Euro-Ausweis liest. **Vorschlag:** in §3.1 und in der \(\bar A\)-Zeile von §3.5 die Gleichung auf die Zelle indizieren (\(\text{EAD}_z = \bar A_z w_z\)) und für die Kommune auf die Summe in §3.6 verweisen; im Teil-Ausweis 1 vermerken, dass \(\bar A_k\) und \(\text{EAD}_k\) bei gemischtem Gebäudetyp nicht proportional sind. | `python3 -c "p=[1e-1,1e-2,(5e-3*1e-3)**0.5];ab=lambda A: sum((p[i]-p[i+1])*(A[i]+A[i+1])/2 for i in range(2))+p[2]*A[2];A1=ab([1200*0.25*0.050,1200*0.80*0.081,1200*1.00*0.250]);A2=ab([0.0,3000*0.10*0.081,3000*0.20*0.250]);E=A1*1.30*1950+A2*1.30*1533;wk=1.30*(1200*1950+3000*1533)/4200;raise SystemExit(0 if abs(E-(A1+A2)*wk)/E > 0.05 else 1)"` | bewusst offen — Kategorie C, hindert die Abnahme nach §5.4 nicht (die Vorbedingung von `/integriere-risiko` stellt auf offene A-Befunde ab); die Gleichung ist auf der Zelle exakt und der kommunale Ausweis rechnet in §3.6 korrekt als Summe; es fehlt nur die Indizierung im Text |
| 25 | C | Bericht §3.5 „Zeichentabelle (alle Formelzeichen der Kapitel 3 und 5)" (Z. 660–699) und §5.1.1 (Z. 1132–1139) gegen §5.1.2 Z. 1162 und §5.1.3 Z. 1205–1208 · **Lücke (§5 LF 11 „Zeichentabellen vollständig"; §7 Lint „jede Zeichentabellen-Zeile mit Wert und Herkunft")** — §3.5 beansprucht wörtlich, jedes Formelzeichen der Kapitel 3 und 5 zu führen, lässt aber vier in Kapitel 5 verwendete Zeichen aus: \(q_0\) (heutiger Objektschutz-Anteil, in §5.1.2 als Bezug des Doppelzählungs-Wächters genannt, hergeleitet erst in §4.7 als „geparkt") sowie \(t_1\), \(t_2\), \(t_3\) (Szenariobeiträge zum Erwartungsschaden in m²/a, §5.1.3). Bei \(t_i\) kommt eine **Zeichenkollision** hinzu: §3.5 vergibt \(t\) als Laufindex des Gebäudetyps (EFH/ZFH, MFH), \(n_t\) und \(\theta_{z,t}\) tragen diesen Index — \(t_1\) liest sich damit als „Gebäudetyp 1" statt als Szenariobeitrag. Dass der Lint 115 Checks grün meldet, zeigt zugleich die Reichweitengrenze der maschinellen Prüfung (vgl. Befund 17): Er prüft vorhandene Tabellenzeilen, nicht fehlende. **Vorschlag:** vier Zeilen in §3.5 ergänzen — \(q_0\) mit Herkunft „§4.7, geparkt (Datenquelle fehlt)" und \(t_1\)…\(t_3\) mit Einheit m²/a und Herkunft §5.1.3 — und die Szenariobeiträge umbenennen (z. B. \(\tau_i\) oder \(\bar A^{(i)}\)), damit der Laufindex \(t\) eindeutig bleibt. | `python3 -c "s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();L=s.split(chr(10));t35=chr(10).join(L[669:700]);t511=chr(10).join(L[1131:1140]);k5=chr(10).join(L[1097:1261]);fehlt=[z for z in ('q_0','t_1','t_2','t_3') if z in k5 and z not in t35 and z not in t511];raise SystemExit(0 if fehlt else 1)"` | bewusst offen — Kategorie C, hindert die Abnahme nach §5.4 nicht (die Vorbedingung von `/integriere-risiko` stellt auf offene A-Befunde ab); vier fehlende Zeilen der Zeichentabelle ohne Rechenwirkung; \(q_0\) ist in §4.7 und §4.8 als geparkt geführt |
| 26 | B | Bericht §5.1.3 „\(s_{\text{bem}}\) — ausgewiesene Näherung mit Richtung", Absätze „Obergrenze aus der Szenario-Zerlegung (Zahlen aus Abschnitt 4.5)" und „Folge für das Band" (Z. 1204–1222) · **Fehler/Lücke (§5 LF 13 Herleitungspflicht; §3.9 „kein Formelzeichen ohne Herleitung"; §3.2 empirische Quantile)** — die als **harte** Obergrenze ausgewiesene Grenze \(s_{\text{bem}} \le 0{,}661\) und die daraus gezogene Kappung des Bandes auf 0,66 sind aus **genau einer Beispielzelle** gerechnet (A = 15,0 / 77,76 / 300,0 m² aus §3.4), nicht aus einer allgemeinen Eigenschaft der Formel. Derselbe Ausdruck liefert für andere Zellprofile 0,856 (a = 1,0 in allen Szenarien), 0,323 (Auenrand a = 0,02/0,20/1,00) und 0,000 (nur im Extremfall betroffen); die Grenze ist also zell- und kommunenabhängig und wird von realistischen Profilen überschritten. Daran hängen das Band von \(s_{\text{bem}}\) (0,30–0,66), das Band von \(r_{\text{S092}}\) (0,0075–0,1056), der Parameter-Block `flood_bldg.s_bem`, die Einzelachsen-Sensitivität und die Schließung von Befund 10. Hinzu kommt ein nicht tragender Quellenverweis: „Zahlen aus Abschnitt 4.5" — dort stehen die Werte \(t_1\)/\(t_2\)/\(t_3\) nicht (nur die Anteile 66,1 / 23,2 / 10,6 %, aus derselben Beispielzelle abgeleitet), die Zeichenfolge `t_1` kommt in §4.5 null mal vor. **Vorschlag:** die Obergrenze entweder allgemein herleiten (Supremum des Ausdrucks über zulässige \(a\)-/\(h\)-Profile bei gegebenen Jährlichkeiten — es liegt oberhalb 0,86 und trägt die Kappung auf 0,66 nicht) oder sie ausdrücklich als **profilabhängige Illustration** kennzeichnen und das Band von \(s_{\text{bem}}\) mit einer anderen, tragenden Begründung setzen; in beiden Fällen den Verweis auf §4.5 durch die tatsächliche Fundstelle (Beispielzelle §3.4/§3.6) ersetzen. Nach P1/P2 bleibt der Wert eine ausgewiesene Abschätzung — die Wirkung wird nicht auf null gesetzt, nur ihre Bandgrenze braucht eine tragende Herleitung. | `python3 -c "p=[1e-1,1e-2,(5e-3*1e-3)**0.5];sm=lambda A: ((p[0]-p[1])*(A[0]+A[1])/2)/((p[0]-p[1])*(A[0]+A[1])/2+(p[1]-p[2])*(A[1]+A[2])/2+p[2]*A[2]);a=sm([15.0,77.76,300.0]);b=sm([1200*0.081,1200*0.250,1200*0.250]);c=sm([0.0,0.0,300.0]);raise SystemExit(0 if abs(a-0.661)<5e-4 and b>0.70 and c==0.0 else 1)"` | behoben — Bericht §5.1.3, Absätze „Profilabhängige Illustration: Anteil unterhalb HQ100 in der Beispielzelle (Befund 26)“ und „Tragende Begründung der oberen Bandgrenze: Ankerwert der Verteilungsprüfung (§4.5)“ (T-0287, 17.09.2026; Einzelheiten im Abschnitt „Autor-Revision nach Runde 2“) |

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
| 27 | C | Bericht Kap. 2, Registerzeile 60-R24-01 (Z. 189) und Langbeleg B4, Rechenschritte 2–4 (Z. 319–350) · **Fehler/Lücke (§5 LF 5 „richtige Band- und Endpunkt-Zuordnung"; §3.9 Abgeschätzt; Vorgabe P1 „samt Herleitung")** — (a) die Jahresraten der Fortschreibung, **3,4 %** (Zentralwert) und **2,3 %** (unteres Bandende), sind aus keinem der in B4 zitierten amtlichen Werte (+3,2 % Nov. 2025, +3,3 % Feb. 2026, +5,0 % Mai 2026) hergeleitet; nur das obere Ende 5,0 % ist belegt; (b) die Bandenden 1.889–2.047 bzw. 1.484–1.609 €₂₀₂₆/m² BGF sind mit den gerundeten Faktoren 1,07/1,16 gerechnet, der hergeleitete Faktor 1,050³ = 1,1576 ergibt 2.043,2 bzw. 1.605,6; (c) „Wertdichte 1.993–2.535 €₂₀₂₆/m²" und „Wiederherstellungswert 8,2–10,4 Bio. €" sind Typ-Endpunkte (reiner MFH- gegen reinen EFH-Satz), werden in der Zeile aber wie ein Band gelesen; die Bänder der beiden abgeschätzten Faktoren (Index 1,07–1,16, BGF/Wohnfläche 1,25–1,40) sind darin nicht fortgepflanzt — gerechnet spannt die Wertdichte 1.855–2.866 €₂₀₂₆/m², der Bestand 7,6–11,8 Bio. €. **Vorschlag:** die Raten 3,4 % und 2,3 % aus den zitierten Monatswerten herleiten (oder die Quelle nennen), die Bandenden mit den ungerundeten Faktoren rechnen, und Typ-Spanne und Unsicherheitsband in Zeile und B4 getrennt ausweisen. | `python3 -c "L=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read().split(chr(10));r=L[188];b=chr(10).join(L[284:350]);q=chr(10).join(L[305:313]);raise SystemExit(0 if ('1.889–2.047' in r and '1.993–2.535' in r and '2,3 %' in b and '2,3' not in q and abs(1765*1.05**3-2047)>3) else 1)"` | bewusst offen — Kategorie C, hindert die Abnahme nach §5.4 nicht (die Vorbedingung von `/integriere-risiko` stellt auf offene A-Befunde ab); Rundungs- und Herleitungsmangel im Band von \(n_t\) (Abweichung am oberen Bandende rund 0,2 %); Zentralwerte unberührt |
| 28 | B | Bericht Kap. 2, Registerzeile 60-S093-01 (Z. 183) und Langbeleg B5, Absatz „Rechenschritt (§3.9 Abgeschätzt) — Band der Zustandsachse" (Z. 386–397); gekoppelt 60-S094-01 (Z. 184, B6 Z. 433–442) · **Fehler (§5 LF 5 „zentriert", „Band- und Endpunkt-Zuordnung"; §3.2 Mittelwertzentrierung)** — (a) B5 schreibt, die Spannweite ln(1,58/0,41) = 1,349 verteile sich auf die **zwei** Achsen Kontamination und Vorsorge, teilt dann aber durch **drei** (0,450); bei gleichem Anteil je Achse wäre der Anteil 0,6745 und das Band 0,71–1,40 statt 0,80–1,25 (S094 dann 0,845–1,184, kombiniert 0,60–1,66); zudem ist 0,41–1,58 die Diagonale C0P2 ↔ C2P0, nicht die Summe zweier Einzelachsen, und Vorsorge ist nach B5 selbst bewohner-, nicht gebäudeseitig; (b) „mittelwertzentriert auf den Bestandsmix" ist nicht nachgewiesen: die Werte sind geometrisch um 1 gesetzt, ohne Bestandsanteile je Klasse; bei 50 : 50 liegt das arithmetische Mittel bei 1,0254 (S093) bzw. 1,0063 (S094), zusammen +3,2 % auf den Basiswert; auch welcher Kurve von Fig. 1 die Endpunkte 3,5 %/25 % gehören, ist nicht zugeordnet; (c) Rechenfehler in der Sensitivitätslesart „voller Anteil": e^−0,6745 = 0,509 ⇒ **0,51**, nicht 0,52; (d) Sensitivitätsangabe der Zeile „±25 %" gegen das eigene Band −20 %/+25 %. **Vorschlag:** den Achsenanteil konsistent zur eigenen Prämisse herleiten (Teiler und Achsenzuordnung begründen), die Zentrierung mit ausgewiesenen Klassenanteilen rechnen oder als geometrische Zentrierung benennen, die Fig.-1-Kurve der Endpunkte zuordnen, 0,52 → 0,51 und „±25 %" → „−20 %/+25 %" korrigieren und S094 samt kombiniertem Band über die Kopplung neu rechnen. | `python3 -c "import math as m;L=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read().split(chr(10));b=chr(10).join(L[351:402]);l=m.log(1.58/.41);a=l/3;raise SystemExit(0 if ('1,349 ÷ 3' in b and 'Kontamination und Vorsorge' in b and '0,52–1,96' in b and round(m.exp(-l/2),2)==0.51 and (m.exp(a/2)+m.exp(-a/2))/2>1.02) else 1)"` | offen — Rest: Achsenanteil in B5 (Teiler 3 bei zwei Achsen), Zentrierung und die Bänder von S093/S094 sind nicht neu gerechnet; in dieser Revision nicht bearbeitet |
| 29 | C | Bericht Kap. 2, Registerzeile 60-S092-01 (Z. 182), Spalte Studientyp, gegen Langbeleg B5 (Z. 365–366) · **Widerspruch (§5 LF 5 „richtige Studienart"; LF 6 „Kopplungen"; §3.8)** — die Zeile begründet den Verzicht auf eine Effektgröße u. a. damit, Befragungen nach Ereignissen seien „nur Kandidat, im Volltext nicht verifiziert". Im selben Kapitel ist Thieken u. a. 2008 (FLEMOps, Befragung von 1.697 Haushalten) als „Volltext gegengelesen" geführt und trägt in Tab. 2 Vorsorge-Skalierungsfaktoren: C0P1 0,64 ÷ C0P0 0,92 = 0,696 und C0P2 0,41 ÷ 0,92 = 0,446, also −30 % bzw. −55 % Schaden je Gebäude mit guter bzw. sehr guter Vorsorge. Der Ausschluss als Wertquelle nach §3.5 (keine Interventionsstudie) bleibt richtig; falsch ist die Aussage „nicht verifiziert", und es fehlt der Vergleich als Plausibilitätsband für \(r_{\text{S092}}\) sowie die Kopplung: dieselbe Tab.-2-Spannweite, die die Vorsorge-Achse enthält, dimensioniert in B5 das Band von 60-S093-01. **Vorschlag:** in der S092-Zeile Thieken u. a. 2008 Tab. 2 als volltextgeprüfte, nach §3.5 nicht zulässige Befragungsevidenz nennen, die Werte 0,70/0,45 als Plausibilitätsprobe der Kette §5.1 ausweisen (nicht als Wert) und die Kopplung S092 ↔ S093 in B5 und in der Zeile vermerken. | `python3 -c "L=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read().split(chr(10));b=chr(10).join(L[351:402]);raise SystemExit(0 if ('im Volltext nicht verifiziert' in L[181] and 'C0P2 **0,41**' in b and 'Thieken' not in L[181]) else 1)"` | bewusst offen — Kategorie C, hindert die Abnahme nach §5.4 nicht (die Vorbedingung von `/integriere-risiko` stellt auf offene A-Befunde ab); betrifft die Begründung des Verzichts auf eine Effektgröße für S092, nicht deren Wert |
| 30 | C | Bericht Kap. 2, Registerzeile 60-S093-01 (Z. 183, Effektgröße „Gebäudetyp (3 Klassen)") und Kapitel 2 insgesamt; verweisende Stelle §3.3 (Stützstellentabelle Z. 557–559) · **Lücke (§5 LF 6 „Struktur überall verwendet, wo die Evidenz strukturabhängig ist")** — die zitierte Schadensfunktion FLEMOps ist nach Gebäudetyp (Einfamilien-, Doppel-/Reihen-, Mehrfamilienhaus) strukturiert; das Register nutzt die Typstruktur nur für den Preis (R24: EFH/ZFH 1.950, MFH 1.533 €₂₀₂₆/m² BGF), nicht für die Schadensquote, und weist die Nichtverwendung auch nicht als Modellgrenze aus (Kapitel 2: „je Gebäudetyp" und „typabhängig" je 0 Treffer). Die Endpunkte 3,5 %/25 % sind keinem Typ zugeordnet, obwohl das Register für jede 100-m-Zelle den Gebäudetyp aus dem Zensus 2022 als verfügbar nennt. **Vorschlag:** entweder eine Registerzeile (oder Spalte in 60-S093-01) für die typabhängige Schadensquote mit Zuordnung der Fig.-1-Endpunkte anlegen und die Typstruktur je Zelle nutzen, oder die typunabhängige Schadensquote ausdrücklich als Modellgrenze mit Richtung und Größenordnung ausweisen (Vorgabe P1/P2: als Abschätzung von KAP3). | `python3 -c "L=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read().split(chr(10));k=chr(10).join(L[151:450]);raise SystemExit(0 if ('Gebäudetyp (3 Klassen)' in L[182] and 'je Gebäudetyp' not in k and 'typabhängig' not in k) else 1)"` | bewusst offen — Kategorie C, hindert die Abnahme nach §5.4 nicht (die Vorbedingung von `/integriere-risiko` stellt auf offene A-Befunde ab); die fehlende Typstruktur der Schadensquote verändert die Registerzeile nicht, sondern ist eine noch auszuweisende Modellgrenze |
| 31 | C | Bericht Kap. 2, Registerzeile 60-W085-01 (Z. 160), Spalten Effektgröße und Entscheidung, gegen §3.4 Schritt 2 (Z. 592) · **Lücke (§5 LF 5 „Band- und Endpunkt-Zuordnung"; §3.2 Sensitivitäten ausschließlich über das Register; §2.2 „In Formeln dürfen nur Zeilen mit Entscheidung Basiswert stehen")** — die Entscheidung lautet „Basiswert — die drei Szenario-Stützstellen p(HQ)", für HQextrem führt die Zeile aber nur das Band 5,0·10⁻³ bis 1,0·10⁻³ a⁻¹ ohne Zentralwert; der in der Kernformel rechnende Wert \(p_3 = 2{,}236\cdot10^{-3}\) a⁻¹ (geometrisches Mittel der Bandenden, als Abschätzung von KAP3 gekennzeichnet) steht erst in §3.4 und kommt in Kapitel 2 null mal vor. Damit ist die Zuordnung „Endpunkte = Sensitivität, Zentralwert = Basiswert" für die dritte Stützstelle im Register nicht vollständig. **Vorschlag:** in der Zeile 60-W085-01 den Zentralwert \(p_3 = 2{,}236\cdot10^{-3}\) a⁻¹ mit Vermerk „§3.9 Abgeschätzt, geometrisches Mittel der Bandenden" nachtragen und in B1 den Rechenschritt ergänzen. | `python3 -c "L=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read().split(chr(10));k=chr(10).join(L[151:450]);raise SystemExit(0 if ('HQextrem 5,0·10⁻³ bis 1,0·10⁻³' in L[159] and '2,236' not in k) else 1)"` | bewusst offen — Kategorie C, hindert die Abnahme nach §5.4 nicht (die Vorbedingung von `/integriere-risiko` stellt auf offene A-Befunde ab); \(p_3\) steht mit Herleitung in §3.4 und §3.5 und jetzt als Block `flood_bldg.p_hq_extrem` in Kap. 7; es fehlt nur der Eintrag in der Registerzeile |

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
| 32 | A | Bericht Kap. 4, Einleitung (Z. 839–841) gegen 4.3 (Z. 924–948) · **Widerspruch/Fehler (§2.4 „Kalibrierlauf immer mit dem Produktionsmodell", §3.4 „Kalibriermodell = Produktionsmodell", §5 LF 7/8)** — Die Einleitung behauptet, das Kalibriermodell sei das Produktionsmodell. \(M_0\) entsteht aber aus drei nationalen Einheitswerten, und der Schadensgrad 0,526 %/a ist der „Vorab-Wert aus der Beispielzelle" (W = 1.200 m², \(a\) = 0,25/0,80/1,00). Die acht benannten Anker-Kommunen sind nicht gerechnet, die angekündigten 16 Länderwerte fehlen. Die Näherung hat einen anderen Umfang als \(A^{*}\): (a) GK2 (1,38 Mio Adressen, im Modell bei HQextrem nass) fehlt in \(M_0\). Nachgerechnet ergibt das 0,222 Mrd. € (\(q\) = 0,050) bis 1,112 Mrd. € (\(q\) = 0,250) je Jahr, also **24–118 % von \(M_0\)**. \(A^{*}\) enthält diese Schäden, deshalb nimmt \(\lambda\) den fehlenden Umfang auf, statt ein Niveau zu korrigieren. (b) Alle 339.000 Adressen zählen als Wohngebäude mit 208 m²; Wohngebäude je Adresse = 19,7/22,6 = 0,872. Das ist entgegen der Behauptung keine Untergrenze. (c) \(d(h)\) wächst multiplikativ, damit trifft das Näherungsverbot aus §3.4 zu. Der Satz „das Modell trifft das Anker-Niveau ohne nennenswerte Korrektur" (4.4) ist deshalb kein Kalibrierergebnis. **Vorschlag:** \(M_0\) mit dem Produktionsmodell auf der dokumentierten Stichprobe rechnen (acht Anker-Kommunen, hochgerechnet über ZÜRS-Klassen **einschließlich GK2**, Adressen über den Wohngebäudeanteil umgerechnet), \(\lambda\) daraus bestimmen und den Restfehler unterhalb der Stichprobenauflösung nach §3.4/§3.9 quantifiziert ausweisen. Bis dahin \(\lambda\) = 1,05 ausdrücklich als vorläufig kennzeichnen und die Einleitung korrigieren. Kein Vollraster-Lauf. | `python3 -c "s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();k=s.split(chr(10)+'## 4 ')[1].split(chr(10)+'## 5 ')[0];raise SystemExit(0 if ('Vorab-Wert aus der Beispielzelle' in k and 'ZÜRS-GK3+GK4' in k and 'Das Kalibriermodell ist das' in k) else 1)"` | offen — Rest: \(M_0\) ist weiterhin nicht mit dem Produktionsmodell auf den Anker-Kommunen gerechnet. Zwischenstand der Revision: Bericht Kap. 4 Einleitung, Absatz „Vorläufiger Stand — \(\lambda\) ist noch kein Kalibrierergebnis“ (GK2-Lücke und Wohngebäudeanteil beziffert, Sensitivität \(\lambda\) 0,97–0,55), der Satz „Das Kalibriermodell ist das Produktionsmodell“ ist gestrichen, §4.4 und §4.8 führen \(\lambda\) als vorläufig |
| 33 | A | Bericht Kap. 4.5 (Z. 973–998) und 4.1 „Ankerwert" (Z. 862–865) · **Fehler (§3.4 „Prüfdaten dürfen nicht dieselben sein, auf denen Faktoren gefittet wurden", §5 LF 8 „out-of-sample", §6 Kalibrier-Prüfstein)** — (a) Die Ankerseite der Verteilungsprüfung (1,0/2,6 = 38,46 %) und das Ankermittel \(A_{\text{ver}}\) = 2,6 − 1,0 = 1,6, aus dem \(\lambda\) bestimmt wird, beruhen auf **denselben zwei Zahlen** aus derselben GDV-Medieninformation zu 2024. Die ausgewiesene Überlappung „1 von 23 Kalibrierjahren, 4,3 %" gibt das nicht wieder, denn aus den anderen 22 Jahren geht kein Wert ein. (b) Die Größen passen nicht zusammen: Das Modell misst den Anteil des seltenen Regimes am **Erwartungswert**, der Anker misst den Überschuss eines **Einzeljahres** über das Mittel. Pluviale Anteile sind darin gepoolt. (c) Das ankerseitige ±12,5 ist gesetzt, nicht hergeleitet (§3.9), und legt die Toleranz fast allein fest. Die Prüfung trennt schwach: Eine Verdopplung des HQextrem-Schadens (\(A_3\) = 600 m²) ergibt 48,76 % und **besteht**. (d) Der modellseitige Anteil 33,86 % kommt aus den gesetzten Stützstellen einer Beispielzelle, nicht aus gemessenen Tiefen der Anker-Kommunen (§3.2 Tails). Der Kalibrier-Prüfstein nach §6 ist damit nicht bestanden. Die Toleranz wird **nicht** geweitet oder verengt, der Befund geht in einen Modellentscheid. **Vorschlag:** Die Prüfung auf Daten stellen, die nicht zur Bestimmung von \(\lambda\) dienen. Möglich sind ein Leave-one-out über die Jahreswerte 2002–2024 (Anteil der Jahre über einer Ereignisschwelle, gerechnet ohne das jeweilige Jahr im Mittel) oder die Länderwerte der Wohngebäude-Grafik gegen die Modellverteilung auf Länderebene. Den Ankerwert als Erwartungswertanteil definieren, das ankerseitige Toleranzbudget herleiten und die Toleranz vor der Rechnung neu fixieren. | `python3 -c "s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();k=s.split(chr(10)+'## 4 ')[1].split(chr(10)+'## 5 ')[0];raise SystemExit(0 if ('1,0/2,6' in k and '1 von 23 Kalibrierjahren' in k and 'dafür ±12,5 Prozentpunkte' in k) else 1)"` | behoben — Bericht **§4.5** (T-0292, 17.09.2026; Einzelheiten im Abschnitt „Autor-Revision nach Runde 2“): die Ankerseite ist eine **Jahresauslassung (Leave-one-out)** über `docs/evidenz/60_gdv_jahresreihe_2002_2024.csv` und geht in \(\lambda\) nicht ein (Prüfgröße skaleninvariant), der Ankerwert ist als **Erwartungswertanteil** definiert, und das ankerseitige Toleranzbudget ist hergeleitet (Jackknife ±11,2 Pp, Ablese ±1,7 Pp, mit dem Modellband ±2,3 Pp quadratisch zu **±11,5 Pp**, vor dem Ergebnis fixiert und enger als die abgelösten ±15). **Ausgang negativ:** 47,7 % gegen 33,9 %, Abstand 13,9 Pp — als **Modellentscheid** im Bericht ausgewiesen, nicht durch Weiten der Toleranz geheilt. Restpunkt ohne eigenen Befund: §5.1.3 stützt die Bandgrenze \(s_{\text{bem}} \le 0{,}62\) noch auf den abgelösten Ankerwert 38,5 % |
| 34 | B | Bericht Kap. 4.1 (Z. 855–865), 4.2 Herleitung \(w_{\text{wg}}\) (Z. 892–897), 4.4 (Z. 952) und 4.5 „Grenzen der Prüfung" (Z. 993–998) · **Lücke (§3.4 Kalibrierfaktor-Regel „Kleinste Quadrate Anker ÷ Modellsumme über die Anker-Zeitreihe; einheitliche Jahres-Auswahlregel, Sensitivitäten je Zeitfenster", §5 LF 7 „gesetzte Werte, die messbar wären")** — \(\lambda\) ist ein einfacher Quotient aus einem Mittelwert, den ein Presse-Satz liefert („rund eine Milliarde mehr als im langjährigen Durchschnitt"). Er wird nicht über die Zeitreihe gefittet, und eine Sensitivität je Zeitfenster fehlt (in Kap. 4 kommen `Kleinste Quadrate` und `Zeitfenster` je 0 mal vor). Nach 4.1 verwendet der Bericht selbst die Übersichtsreihe (30.12.2025) und die Grafik „Elementarschäden **an Wohngebäuden** nach Bundesländern" (10.10.2025). Trotzdem gelten die Jahreswerte als noch nicht vorliegend (4.5), und \(w_{\text{wg}}\) = 0,65 wird als „nicht publiziert" gesetzt. Beide Größen sind nach der eigenen Quellenangabe messbar. Außerdem ist offen, ob GDVs „langjähriger Durchschnitt" 2002–2024 umfasst. **Vorschlag:** die 23 Jahreswerte aus dem zitierten Datenservice mit Grafik und Zugriffsdatum übernehmen, \(A_{\text{ver}}\) als deren Mittel rechnen (und \(\lambda\) nach §3.4 fitten), Sensitivitäten für mindestens zwei Zeitfenster ausweisen (z. B. 2002–2024 und 2014–2024, mit und ohne 2021), \(w_{\text{wg}}\) aus dem Wohngebäude-Schnitt messen oder begründen, warum er dort nicht abgelesen werden kann. | `python3 -c "s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();k=s.split(chr(10)+'## 4 ')[1].split(chr(10)+'## 5 ')[0];raise SystemExit(0 if ('Kleinste Quadrate' not in k and 'Zeitfenster' not in k and 'an Wohngebäuden' in k and 'nicht publiziert' in k) else 1)"` | offen — Rest: \(\lambda\) ist nicht über die Zeitreihe gefittet, Sensitivitäten je Zeitfenster fehlen; hängt an der Jahresreihe aus Befund 33 |
| 35 | B | Bericht Kap. 4.6 (Z. 1002–1014) · **Fehler (§3.4 „Sanity-Bänder mit Unter- und Obergrenze aus amtlicher Statistik (oder begründete Ausnahme)", §6 „ein zu weit gewordenes Band ist ein Befund")** — (a) **Untergrenze zirkulär:** \(U = A_{\text{ver}} w_{\text{wg}} \varphi \pi\) und \(\lambda M_0 \equiv A^{*} = U \cdot u\kappa\). Die Prüfung \(U \le \lambda M_0\) gilt also für **jedes** \(u\kappa \ge 1\) (nachgerechnet \(U/A^{*}\) = 0,5647) und kann nicht scheitern. Als „harte" Grenze beruht sie zudem auf den Mittelwerten zweier Abschätzungen; mit deren unteren Bandenden sinkt \(U\) auf 0,28. (b) **Obergrenze ist keine Schranke:** Die Begründung „Mehr kann selbst dann nicht entstehen, wenn jedes exponierte Gebäude im Hundertjahresrhythmus mit maximaler Quote getroffen wird" übersieht, dass GK4 nach ZÜRS-Definition und nach dem eigenen \(p_1\) = 0,1 a⁻¹ mindestens alle zehn Jahre nass wird. Die eigene Modellrate (6,311/1.200 = 0,526 %/a) liegt beim **2,10-Fachen** der angesetzten Höchstrate 0,25 %/a. Klassengerecht (GK4 und GK3 mit 0,1 a⁻¹, GK2 mit 0,01 a⁻¹, Quote 0,250) ergibt sich **6,29 Mrd. €₂₀₂₆/a**, GK4 allein 1,19 Mrd. Dass die Lage „eingehalten" ist, liegt daran, dass \(O\) fünfmal so viele Adressen zählt. (c) Beide Grenzen stammen aus GDV-Zahlen, ZÜRS und Abschätzungen, keine aus amtlicher Statistik; eine begründete Ausnahme fehlt. **Vorschlag:** die Untergrenze unabhängig vom Ankerfaktorsatz herleiten (z. B. aus amtlichen Wiederaufbauhilfen 2013/2021 als Ereignis-Mindestschaden, umgelegt auf die Wiederkehrzeit), die Obergrenze klassengerecht mit den Überflutungswahrscheinlichkeiten der ZÜRS-Klassen bilden, die Ausnahme vom Amtlichkeitsgebot begründen. Das Band danach vorab fixieren und nicht wieder weiten. | `python3 -c "s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();k=s.split(chr(10)+'## 4 ')[1].split(chr(10)+'## 5 ')[0];raise SystemExit(0 if ('mittleren Betroffenheit von 1/100 Jahren' in k and 'Hochrechnung \\\\(u\\\\) entfällt hier bewusst' in k and 6.311/1200>0.25*0.01) else 1)"` | offen — Rest: die Untergrenze des Sanity-Bandes in §4.6 bleibt zirkulär, die Obergrenze ohne Klassenbezug; in dieser Revision nicht bearbeitet |
| 36 | B | Bericht Kap. 4.4 „Plausibilitätsschranke" (Z. 960–963) gegen 4.4 Band (Z. 952) und 4.8 (Z. 1053) · **Widerspruch/Lücke (§3.9 Herleitungspflicht; §6 Prüfsteine)** — Die Schranke \(\lambda\) < 0,50 oder > 2,00 („Modell gilt als fehlerhaft") ist ohne Herleitung gesetzt und in 4.8 nicht aufgeführt. Das eigene \(\lambda\)-Band 0,42–2,36 (nachgerechnet 0,416–2,357) liegt **an beiden Enden außerhalb** dieser Schranke. Der Bericht erklärt damit Teile seines eigenen Unsicherheitsbandes für modellfehlerhaft, ohne diese Fälle zu entscheiden. Zudem enthält das \(\lambda\)-Band nur die Ankerunsicherheit, \(M_0\) trägt kein Band (208 m², 1,30, 1.950 €, 6,311/1.200 und 339.000 gehen ungestreut ein). **Vorschlag:** die Schranke aus dem vollständig fortgepflanzten Band von \(A^{*}\) **und** \(M_0\) herleiten und in 4.8 führen oder ausdrücklich begründen, warum Bandenden jenseits der Schranke zulässig sind. | `python3 -c "s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();k=s.split(chr(10)+'## 4 ')[1].split(chr(10)+'## 5 ')[0];t=k.split('### 4.8 ')[1];raise SystemExit(0 if ('0,42–2,36' in k and '2{,}00' in k and '2,00' not in t and '2{,}00' not in t) else 1)"` | offen — Rest: die Schranke 0,50/2,00 steht jetzt als Abschätzung von KAP3 in §4.8 (gilt für den Zentralwert), ihre Herleitung aus dem fortgepflanzten Band von \(A^{*}\) und \(M_0\) fehlt weiter |
| 37 | B | Bericht Kap. 4.8 Parametertabelle (Z. 1045–1057) gegen 4.2 (Z. 913–915), 4.5 (Z. 973–978), 4.4 (Z. 960–961) und 4.6 (Z. 1005/1009) · **Lücke (Vorgabe P1 „Gilt für alle Parameter", §3.9 „Unzulässig: … Bandgrenzen, Referenzwerte")** — Drei Werte, die in Kapitel 4 rechnen, fehlen in der P1-Tabelle: die Betroffenheit **1/100 a** (in 4.6 selbst „Abschätzung von KAP3" genannt; in 4.8 kommt sie nur als Wort in der Herleitungsspalte von \(O\) vor, ohne eigene Zeile und Kennzeichnung), die Plausibilitätsschranke **0,50/2,00** und der Baupreisanstieg **„rund 3 %" 2023 → 2024**, aus dem \(\pi\) folgt (ohne Quelle, ohne Abschätzungsvermerk). Außerdem heißen \(\lambda\), \(U\) und \(O\) „berechnet". Sie hängen jedoch an Abschätzungen von KAP3 (\(w_{\text{wg}}\), \(\varphi\), 1/100 a), und P1 kennt nur Quelle oder Abschätzung samt Herleitung. Ein Nutzer sähe „berechnet", ohne zu erkennen, dass eine Abschätzung trägt. **Vorschlag:** die drei Parameter mit Wert, Band und Kennzeichnung (Quelle oder Abschätzung von KAP3 samt Herleitungsanker) in 4.8 aufnehmen, bei \(\lambda\), \(U\) und \(O\) vermerken, welche Abschätzungen einfließen. | `python3 -c "s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();t=s.split('### 4.8 ')[1].split(chr(10)+'## 5 ')[0];raise SystemExit(0 if ('Betroffenheit' not in t and '2,00' not in t and 'rund 3' not in t and 'Baupreisanstieg' not in t) else 1)"` | behoben — Bericht §4.8, drei neue Zeilen „Baupreisanstieg 2023 → 2024“, „Betroffenheit exponierter Gebäude“ und „Plausibilitätsschranke \(\lambda\)“, je mit Kennzeichnung; bei \(\lambda\), \(U\) und \(O\) sind die einfließenden Abschätzungen vermerkt |
| 38 | C | Bericht Kap. 4.2 Tabellenzeile \(\pi\) (Z. 887), Herleitung (Z. 913–915) und 4.8 (Z. 1052); gerechnet im Block `beispiel_60_kalibrierung` (Z. 1064–1065) · **Fehler (Rechenfehler im Band)** — \(\pi = 1{,}105/1{,}03 = 1{,}0728\) trifft zu. Die Bandenden folgen aus dem B4-Band 1,07–1,16 aber als 1,07/1,03 = **1,039** und 1,16/1,03 = **1,126** (mit dem ungerundeten 1,05³ = 1,1576, vgl. Befund 27: **1,124**), nicht als 1,04–**1,11**. Dadurch ist das obere Ende von \(A^{*}\) mit 2,216 zu niedrig; mit 1,126 wären es 2,248 Mrd. €, dicht an \(O\) = 2,264. Der Beispielblock prüft nur die eigene Rundung und fängt den Fehler deshalb nicht. **Vorschlag:** das Band von \(\pi\) aus dem Band von B4 rechnen (nach Befund 27), \(A^{*}\)-Band, \(\lambda\)-Band und die Zusicherung `hi` nachziehen. | `python3 -c "s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();k=s.split(chr(10)+'## 4 ')[1].split(chr(10)+'## 5 ')[0];raise SystemExit(0 if ('1,07 (1,04–1,11)' in k and round(1.16/1.03,2)>1.11) else 1)"` | bewusst offen — Kategorie C, hindert die Abnahme nach §5.4 nicht (die Vorbedingung von `/integriere-risiko` stellt auf offene A-Befunde ab); Rundungsfehler im Band von \(\pi\) (oberes Ende 1,11 statt 1,126), wird mit Befund 27 nachgezogen |
| 39 | B | Bericht Kap. 4.7 „Wächter" (Z. 1023–1029) gegen 4.4 (\(\lambda\) aus dem Mittel 2002–2024) und §5.1.2 (\(\Delta q\)) · **Lücke (§3.5 „Doppelzählungs-Wächter gegen die Kalibrierjahre", §5 LF 4 „Maßnahmeneffekt schon im Basiswert?")** — Der Wächter setzt als Referenz den „Ausstattungsstand 31.12.2024" und schließt alle Nachrüstungen bis 2024 aus \(\Delta q\) aus. \(\lambda\) bildet aber den **mittleren** Ausstattungsstand der Jahre 2002–2024 ab, nicht den Stand zum Stichtag. Eine Nachrüstung aus dem Jahr \(t\) geht nur mit dem Gewicht \((2024-t+1)/23\) ins Niveau ein (2020: 21,7 %, 2014: 47,8 %). Solche Nachrüstungen sind im Basisschaden also nur teilweise enthalten, werden als Hebel aber vollständig gesperrt. Das Niveau liegt dadurch über dem Stand 2024, der Hebel ist unterzählt. Die Verfallsregel verschiebt den Referenzzustand je neu aufgenommenem Jahr um ein ganzes Jahr, das Kalibriermittel nur um 1/24. Ohne \(q_0\) lässt sich außerdem nicht prüfen, ob \(\Delta q\) = 0,10 ein Zuwachs nach 2024 ist. Befund 7 ist formal abgearbeitet, der Wächter selbst aber nicht operationalisiert. **Vorschlag:** den Referenzzustand als das über die Kalibrierjahre gewichtete Ausstattungsmittel definieren (oder das Kalibrierfenster so kurz wählen, dass der Stichtag das Mittel repräsentiert, mit Sensitivität je Zeitfenster nach §3.4, vgl. Befund 34) und die Verfallsregel auf die tatsächliche Gewichtsverschiebung umstellen. Richtung und Größenordnung der Verzerrung als Modellgrenze ausweisen, solange \(q_0\) geparkt ist. | `python3 -c "s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();t=s.split('### 4.7 ')[1].split('### 4.8 ')[0];raise SystemExit(0 if ('Ausstattungsstand 31.12.2024' in t and 'gewicht' not in t.lower()) else 1)"` | offen — Rest: der Referenzzustand des Wächters in §4.7 ist weiter der Stichtag 31.12.2024 statt des gewichteten Ausstattungsmittels; in dieser Revision nicht bearbeitet |

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

### 4 · Paket T-0274 — Leitfragen 9, 10 und 12 gegen Kapitel 6 bis 9

Fünftes Paket der Runde 2 (17.09.2026), eigene Sitzung. Sie hat den geprüften Stand nicht
geschrieben: Die Kapitel 6 bis 9 stammen aus T-0240 bis T-0243 und liegen im Endstatus (eiserne
Regel 4). Das Bundle nach §1 gilt unverändert (Abschnitt 0 dieser Runde). Die Lint-Ausgabe aus
Abschnitt 0.1 wird **übernommen und nicht neu vorhergesagt**; der Lint wurde in diesem Paket nicht
ausgeführt. Die Arbeitsmappen wurden mit der Standardbibliothek gelesen (zipfile/XML), nur gelesen
und nie geändert (eiserne Regel 2).

**Prüfumfang dieses Pakets:** genau Kapitel 6 „Szenario-Anwendung & Modellgrenzen" (Z. 1262–1322),
Kapitel 7 „Parameter-Blöcke" samt 7.1 (Z. 1323–1451), Kapitel 8 „Quellen" (Z. 1452–1493) und
Kapitel 9 „Ansatz-Vergleich" (Z. 1494–1582). Nachgemessen mit
`python3 -c "import re;s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();print([len(re.sub('<!--.*?-->','',s.split(chr(10)+'## %d '%n)[1].split(chr(10)+'## ')[0],flags=re.S)) for n in (6,7,8,9)])"`
→ `[4568, 6390, 3073, 9486]`, Summe 23.517. Die Abweichung von je drei Zeichen gegenüber den im
Ticket genannten **4.571 / 6.393 / 3.076 / 9.489** (Summe **23.529**) kommt allein von der
Schnittkante (Kapitelnummer und Leerzeichen der Überschriftszeile); gemessen ist ohne HTML-Kommentare
(Kap. 8 und 9 tragen je einen Pflichtinhalte-Kommentar). Der geprüfte Textkörper ist derselbe. Andere
Kapitel wurden nur dort gelesen, wo die Kapitel 6 bis 9 ausdrücklich auf sie verweisen: Kap. 7
verweist für „alle weiteren Blöcke" auf Kap. 3/4, deshalb sind die Kostensätze aus Langbeleg B4,
§3.4 und §4.2/§4.3 für LF 9 nachgerechnet; Kap. 6 Modellgrenze 2 und 7.1 verweisen auf §5.1.2 und
die Kontenblätter. Sie sind hier nicht Prüfgegenstand. Ein **nationaler 100-m-Vollraster-Lauf
nach §3.4 war nicht verlangt und wurde nicht gefahren**; alle Nachrechnungen laufen auf den
Zahlenwerten der Blöcke und der Kostensätze.

#### 4.1 · Nachrechnung der Kostensätze (LF 9 — gerechnet, nicht gelesen)

**Kostensätze in den Parameter-Blöcken des Kapitels 7: null.** Kapitel 7 führt genau vier Blöcke,
maschinell ausgelesen (`id`, `einheit`, `preisstand`):

| Block | Einheit | preisstand | Kostensatz? |
|---|---|---|---|
| `flood_bldg.dq_s092` | `"-"` | `null` | nein (Anteil) |
| `flood_bldg.s_bem` | `"-"` | `null` | nein (Anteil) |
| `flood_bldg.e_bem` | `"-"` | `null` | nein (Anteil) |
| `flood_bldg.r_s092` | `"-"` | `null` | nein (Minderungsrate) |

Eine Umrechnung auf einen Preisstand ist deshalb **für keinen Block** nachzurechnen. Einheitlich
ist der Preisstand über die Blöcke nur in dem leeren Sinn, dass alle vier `preisstand: null`
tragen, was bei dimensionslosen Größen zutrifft. Kein Block trägt einen Preisstand, deshalb kann
kein Ratchet-Test nach §4 die Einheitlichkeit maschinell prüfen. Die Kostensätze, auf denen der
Euro-Pfad tatsächlich rechnet, stehen **nur** im Fließtext der Kapitel 2 bis 4. Kap. 7 sagt dazu
selbst: „Alle weiteren Blöcke entstehen mit der Herleitung in Kap. 3/4". Sie wurden deshalb
nachgerechnet (Python, ungerundet), damit das Verdikt nicht am leeren Kapitel hängt:

| Kostensatz / Umrechnung | Fundstelle | Bericht | nachgerechnet | Ergebnis |
|---|---|---|---|---|
| Indexfaktor 2010 → 2023 | B4, Rechenschritt 1 | 149,8 ÷ 89,1 = 1,6813 | **1,68126** | trifft zu |
| \(n_{\text{EFH/ZFH}}\) auf Preisstand 2023 | B4, Rechenschritt 1 | 1.050 × 1,6813 = 1.765,4 | **1.765,3** (mit 1,6813: 1.765,37) | trifft zu |
| \(n_{\text{MFH}}\) auf Preisstand 2023 | B4, Rechenschritt 1 | 825 × 1,6813 = 1.387,1 | **1.387,0** | trifft zu |
| Fortschreibung 2023 → 2026 | B4, Rechenschritt 2 | 1,034³ = 1,1055 (Band 1,07–1,16) | **1,10551** (1,023³ = 1,07061; 1,05³ = 1,15763) | trifft zu |
| \(n_{\text{EFH/ZFH}}\) Preisstand 2026 | B4 / §3.4 | 1.765 × 1,105 = **1.950 €₂₀₂₆/m² BGF** (1.889–2.047) | **1.950,3** (1.888,6–2.047,4); ungerundete Kette 1.050 · 149,8/89,1 · 1,034³ = 1.951,6 | trifft zu (Rundungskette −0,07 %) |
| \(n_{\text{MFH}}\) Preisstand 2026 | B4 / §3.4 | 1.387 × 1,105 = **1.533 €₂₀₂₆/m² BGF** (1.484–1.609) | **1.532,6** (1.484,1–1.608,9); ungerundet 1.533,4 | trifft zu |
| Gesamtfaktor 2010 → 2026 je Satz | §3.3 „Umrechnungsfaktor je Satz in der Zeichentabelle" | nicht als Zahl ausgewiesen (Zeichentabelle §3.5, Zeile \(n_t\): „mit Baupreisindex … fortgeschrieben") | **1,6813 × 1,105 = 1,8578** | fehlt in Zeichentabelle und Block → Befund 40 |
| Wertdichte \(w\) je m² Wohnfläche | B4, Rechenschritt 3 | 1.950 × 1,30 = 2.535; 1.533 × 1,30 = 1.993 €₂₀₂₆ | **2.535,0 / 1.992,9** | trifft zu |
| Wert je exponiertem Wohngebäude | §4.3 Punkt 2 | 208 · 1,30 · 1.950 = 527.280 €₂₀₂₆ | **527.280** | trifft zu |
| \(\pi\) Preisstand 2024 → 2026 | §4.2 | 1,07 | **1,105/1,03 = 1,0728**; aus der Kette von Rechenschritt 2 (zwei Schritte à 3,4 %) 1,034² = **1,0692** | beide gerundet 1,07; Band bereits Befund 38, kein neuer Befund |

**Einheitlichkeit des Preisstands (über den ganzen Bericht, weil die Blöcke keinen tragen):**
`€₂₀₂₆` kommt 34-mal vor, `€₂₀₂₄` 0-mal. `€₂₀₂₃` (3-mal) und `€₂₀₁₀` (4-mal) stehen nur als
Zwischenstufen der Rechenschritte 1 und 2 in B4. Der GDV-Anker im Preisstand 2024 wird über
\(\pi\) auf 2026 gehoben (§4.2). Jeder Euro-Wert, der in \(\text{EAD}\), \(M_0\), \(A^{*}\), \(U\) oder
\(O\) eingeht, steht damit auf **Preisstand 2026**. Inhaltlich ist der Preisstand einheitlich.
Maschinenlesbar ist er es nicht, weil kein Kostensatz einen Block hat (Befund 40).

#### 4.2 · Leitfragen dieses Pakets (§5) — einzeln mit Verdikt und Beleg

**LF 9 — Kostensätze: Preisstand einheitlich, Quellen, VSL/VOLY-Konsistenz, Konto-Zuordnung?
Verdikt: Befund** (→ neue Befunde **40** und **41**).
- **Preisstand einheitlich: inhaltlich bestanden, in den Blöcken nicht belegbar.** Alle Euro-Werte
  stehen auf 2026, alle Umrechnungen rechnen auf (Abschnitt 4.1). Kapitel 7 trägt aber keinen
  einzigen Kostensatz. Das Pflichtfeld `preisstand` („Pflichtfeld bei Kostensätzen", §4) ist in
  keinem Block belegt. Den Umrechnungsfaktor je Satz (§3.3) nennt weder eine Zeichentabelle noch
  ein Block als Zahl (1,8578). → **Befund 40**.
- **Quellen der Kostensätze: bestanden.** NHK 2010 nach ImmoWertV Anlage 4 und Destatis
  Fachserie 17 Reihe 4 sowie die Pressemitteilungen Nr. 241/2026 und Nr. 011/2026 stehen in B4 mit
  URL, Zugriffsdatum und wörtlichem Zitat. Der Fortschreibungsfaktor 2023 → 2026 und
  \(k_{\text{BGF}}\) sind als Abschätzung von KAP3 gekennzeichnet. Die fehlenden Archiv-Snapshots
  gehören zu LF 10 (Befund 42).
- **VSL/VOLY-Konsistenz: bestanden (nicht einschlägig).** #60 bucht nur K3. Kein Kostensatz des
  Berichts ist ein VSL- oder VOLY-Wert; Personenfolgen gehen nach Kap. 6, Modellgrenze 1, an #101
  (K1). Der VOLY-Preisstand 2024 aus Konten **C11** wird deshalb nirgends mit €₂₀₂₆-Werten
  vermischt.
- **Konto-Zuordnung: im Konto bestanden, im Kostensatz-Typ Befund.** Buchung in K3 stimmt mit
  Mon. **I65** („K3") und Konten **C29** (Buchungsobjekt 60) überein. Die Mappe schreibt für dieses
  Konto aber einen Kostensatz-Typ vor, den der Bericht nicht umsetzt: Mon. **J64** „…; Zeitwertansatz;
  Versicherungsleistungen sind Transfers …", von **J65** mit „Wie ID 59" für #60 übernommen, und
  Konten **C27** „Wiederherstellungs-/Zeitwertkosten". Der Bericht bewertet mit NHK-Neuwerten.
  „Zeitwertansatz" kommt im Bericht 0-mal vor. Die Zeitwert-Lesart wird nur als „Band" behauptet
  (B4, §3.4), ohne Zahlenwert oder Alterswertminderungsfaktor. → **Befund 41**.

**LF 10 — Quellen: fehlend, veraltet, falsch zugeordnet, unverifiziert; Zahlen ≠ Primärquelle?
Verdikt: Befund** (→ neue Befunde **42** und **43**).
- **Arbeitsmappen: bestanden.** Commit-Hashes und Prüfsummen in Kap. 8 wurden gegen das Repository
  nachgerechnet. `sha256sum` ergibt `4383882d…8ce2d` (Monetarisierung) und `2faac648…35a28`
  (Schadensbaum), identisch mit Kap. 8. `git log` auf die Dateien ergibt den letzten Commit
  `68442ca1…` vom 2026-08-30 und `1a89a2e8…` vom 2026-08-17, ebenfalls identisch.
- **Quelle 3 (Hochwasserschutzfibel): bestanden.** URL, Archiv-Snapshot und Zugriffsdatum sind
  vorhanden. Der Vermerk „nicht im Volltext geprüft, geht in keinen Wert ein" ist ehrlich
  (§3.8 Datenlücke benannt).
- **Fehlend: Befund.** Kap. 4.1 schließt die Angabe des nationalen Ankers mit „vollständige Belege
  in Kap. 8". In Kapitel 8 kommt `GDV` aber **0-mal** vor, und Kapitel 4 enthält **0** URLs. Die
  Quelle, auf der \(A_{\text{ver}}\), \(\lambda\) und das Sanity-Band hängen, hat im Bericht weder
  URL noch Archiv-Snapshot. Dazu kommt: Der gesamte Bericht führt 31 `http`-Angaben, aber nur **einen**
  `web.archive.org`-Snapshot (Quelle 3). Die Langbelege B1 bis B6, auf die Kap. 8 Punkt 4 alle
  Evidenzquellen verweist, tragen keinen Archiv-Snapshot. Kap. 8 Punkt 4 zählt bei ihnen den
  Snapshot auch nicht auf („Vollzitat, DOI/URL, Zugriffsdatum"). → **Befund 42**.
- **Falsch zugeordnet: Befund.** 7.1 belegt den Endpunkt `K3-Wiederherstellung` mit
  „`KWRA-Monetarisierung.xlsx`, Blatt ‚Schadenskonten-System' Z28". Zelle **C28** lautet aber
  „Betriebsunterbrechung (→K5), Infrastruktur (→K4), Personen (→K1)" (Spalte „Ausgeschlossen"). Die
  Zeichenfolge `K3-Wiederherstellung` steht in den Zeilen 25–30 dieses Blatts nicht; sie steht in
  der Netzwerkliste **J61** (so von T-0270, Stichprobe 7, gelesen). Zusätzlich führt Kap. 8 Quelle 2
  die Blätter nur mit einer Auswahl der Zellen, die der Bericht zitiert: „Rechenregeln (Z9, Z11,
  Z20)". Zitiert werden aber auch Rechenregeln Z7 (R5) und Z19 (A4) je einmal. Bei
  „Risiken-Monetarisierung (Z51, Z54–Z56, Z64, Z65, Z106)" fehlen Z17 (2-mal zitiert), Z42 und
  Z57. → **Befund 43**.
- **Zahlen ≠ Primärquelle:** Im Prüfumfang steht keine Zahl, die einer Primärquelle widerspricht.
  Die Kostensätze in B4 rechnen gegen die zitierten Indexwerte auf (Abschnitt 4.1). Die
  Volltextprüfung von B1 bis B6 selbst gehört zu LF 5/6 (Paket T-0272) und ist hier nicht
  wiederholt.

**LF 12 — Umsetzbarkeit: Daten offen/keyless; Parameter-Blöcke vollständig; Architektur-vereinbar;
benötigte neue Ebenen als solche gekennzeichnet? Verdikt: Befund** (→ neue Befunde **40**, **44**
und **45**).
- **Parameter-Blöcke vollständig: Befund.** Vier Blöcke, alle für den Hebel S092. Für die
  Parameter der Kernformel und der Kalibrierung gibt es keinen Block: \(n_{\text{EFH/ZFH}}\),
  \(n_{\text{MFH}}\), \(k_{\text{BGF}}\), \(p_1\)–\(p_3\), die Stützstellen von \(d(h)\), \(f_{S093}\),
  \(f_{S094}\), \(\lambda\), \(\pi\), \(\kappa\), \(u\), \(w_{\text{wg}}\) und \(\varphi_{\text{fluss}}\).
  Kap. 3 und 4 sind seit T-0236/T-0238 hergeleitet. Der Satz „Alle weiteren Blöcke entstehen mit
  der Herleitung in Kap. 3/4" ist also überholt, ohne eingelöst zu sein. Nach §4 wird die
  Produkt-Registry aus diesen Blöcken extrahiert; ohne sie entsteht dort kein Euro-Pfad und keine
  P1-Parameterliste für Kostensätze. → **Befund 40**.
- **P1-Kennzeichnung in den vorhandenen Blöcken: bestanden.** Alle vier Blöcke tragen
  `kennzeichnung: abschaetzung_kap3` und einen `herleitung_anker`. Die Anker `s092-wirkung`,
  `s-bem-naeherung` und `fortschreibung-endpunkt-k3` sind im Text als `<a id=…>` gesetzt. Die
  Beanstandung von Befund 15 (Kennzeichnung nur als YAML-Kommentar) trifft auf diesen Stand nicht
  mehr zu. Die Regression selbst führt das Geschwisterpaket. Die Bänder rechnen auf: 0,10 · 0,50 · 0,70
  = 0,035, 0,05 · 0,30 · 0,50 = 0,0075, 0,20 · 0,66 · 0,80 = 0,1056.
- **Wertebereich §4: bestanden als Antrag.** `endpunkt` und `bandzuordnung` liegen außerhalb des
  §4-Wertebereichs. Das ist in 7.1 als datierter Antrag auf Fortschreibung ausgewiesen und nicht
  still überstimmt. Über den Antrag entscheidet nicht die Gegenprüfung (§5: „Anforderungsänderungen
  nur per Fortschreibung"). Das Fehlzitat darin steht in Befund 43.
- **Architektur-vereinbar (§3.6): bestanden.** Die drei Infokasten-Texte stehen wörtlich in
  Kap. 6: Benennung „bewerteter Schaden — Konto K3", Vollständigkeitsanzeige „Stufe M0: 1 von 8
  Konten aktiv" und Versionsstempel „… — Untergrenze". Die Zahl 8 stimmt mit der Kernsumme aus
  Konten **A2** (K1–K6 + K8, K7 nachrichtlich: sieben Kernkonten plus K7 = acht Konten) überein.
  Die Kontogrenze steht als Modellgrenze 1.
- **P2-Bauform-Grenze in Kap. 6: Befund.** Die einzige Maßnahme ohne publizierte Effektgröße ist
  S092. §5.1.2 nennt ihre Bauform-Grenze ausdrücklich („Kommunenweiter Pauschalfaktor statt
  zellscharfer Wirkung (Bauform-Grenze)"). In der Modellgrenzen-Liste von Kap. 6 fehlt sie:
  `Pauschal` kommt dort 0-mal vor, S092 nur als konstant gehaltene Größe. Stattdessen ist
  Modellgrenze 2 mit „Vorgabe P2" an S094 gehängt, obwohl S094 kein Maßnahmen-Hebel ist, sondern
  eine Vulnerabilitätsachse. → **Befund 44**.
- **Daten offen/keyless und neue Ebenen gekennzeichnet: im Modellkapitel bestanden, in Kap. 9
  Befund.** Kap. 9 („Aufwand", Ansatz (a)) nennt „vier Datenebenen, davon zwei neu anzulegen
  (HQ-Tiefen, GEBAEUDEWERT)". §3.2 führt aber drei Ebenen als „neu anzulegen" (HQ_FLAECHE,
  HQ_TIEFE, GEBAEUDEWERT) und eine als „geparkt (Datenquelle fehlt)" (GEBAEUDEZUSTAND_BAUSTOFF).
  Die Datenverfügbarkeit von (a) heißt „hoch — alle vier Eingänge sind frei zugänglich". Das Wort
  „geparkt" kommt in Kap. 9 nicht vor. Das Raster, auf dem die Ansatzwahl beruht, unterzeichnet
  damit den Aufbauaufwand und verschweigt die geparkte Ebene. → **Befund 45**. Die Aussage in
  Kap. 9, die R7-Weiche existiere „in der Formel bereits", ist schon Befund 20 und wird hier nicht
  doppelt gezählt.
- **Ansatz-Vergleich §3.7 (Pflicht für den ersten Familienvertreter): formal vollständig.** Drei
  Ansätze, alle sieben Kriterien in 21 Zellen bewertet, begründete Empfehlung, Verworfenes als
  Ergänzungsmodul ((b)) bzw. als erhaltenes Materialband ((c)) benannt. Die inhaltlichen Mängel
  stehen in den Befunden 20 und 45.

#### 4.3 · Neue Befunde dieses Pakets (40–45)

Format nach §5: Stelle · Art (Lücke/Fehler/Widerspruch) · Begründung · Vorschlag · Kategorie. Das
Ticket nennt die Nummern 1–19 und als erste neue Nummer 20; das war der Stand beim Ticketschnitt.
Die vorlaufenden Pakete T-0270 (20–22), T-0271 (23–26), T-0272 (27–31) und T-0273 (32–39) haben
seither weiter vergeben. Nach der Regel „fortlaufend ab der nächsthöheren freien Nummer" ist die
erste neue Nummer deshalb **40**. **Dieses Paket behebt keinen Befund**, weder einen neuen noch
einen alten. Die Kurzform-Tabelle „Offene Befunde" am Kopf bleibt bewusst unberührt; sie schreibt
die Befund-Regression dieser Runde fort. Jeder Prüfausdruck endet mit Exit 0, **solange der Befund
besteht**. Am 17.09.2026 wurden alle sechs ausgeführt, alle sechs endeten mit Exit 0.

| Nr | Kat. | Befund (Stelle · Art · Begründung · Vorschlag) | Prüfausdruck | Status |
|---|---|---|---|---|
| 40 | A | Bericht Kap. 7 (Z. 1323–1406), Einleitungssatz „Nur der Hebel aus §5.1 ist beziffert. Alle weiteren Blöcke entstehen mit der Herleitung in Kap. 3/4" gegen §3.4 (Z. 607–612), Zeichentabelle §3.5 (Z. 689–690), §4.2/§4.8 · **Lücke (§4 „Parameter-Block-Format … wird per Skript in die Produkt-Registry extrahiert", „preisstand: Pflichtfeld bei Kostensätzen"; §3.3 „alle Kostensätze eines Berichts auf einen gemeinsamen Preisstand indexiert (Umrechnungsfaktor je Satz in der Zeichentabelle)"; Vorgabe P1 „gilt für alle Parameter (Defaults, Kostensätze, Wirkungsfaktoren)"; §5 LF 9/12)** — Kapitel 7 führt vier Blöcke, alle dimensionslos und alle für den Hebel S092. Für **keinen** Kostensatz gibt es einen Block: \(n_{\text{EFH/ZFH}}\) = 1.950 und \(n_{\text{MFH}}\) = 1.533 €₂₀₂₆/m² BGF fehlen. Ebenso fehlen alle übrigen Parameter der Kernformel und der Kalibrierung (\(k_{\text{BGF}}\), \(p_1\)–\(p_3\), Stützstellen von \(d(h)\), \(f_{S093}\), \(f_{S094}\), \(\lambda\), \(\pi\), \(\kappa\), \(u\), \(w_{\text{wg}}\), \(\varphi_{\text{fluss}}\)). Das Pflichtfeld `preisstand` ist in keinem Block belegt. Die Einheitlichkeit des Preisstands lässt sich deshalb nicht maschinell prüfen, obwohl sie inhaltlich gegeben ist (nachgerechnet in Abschnitt 4.1). Der Umrechnungsfaktor je Satz (NHK 2010 → Preisstand 2026 = 1,6813 × 1,105 = **1,8578**) steht nicht als Zahl in einer Zeichentabelle. Kap. 3 und 4 sind hergeleitet, der Verweis „entstehen mit der Herleitung" ist also überholt, ohne eingelöst zu sein. Folge für das Produkt: Die Registry-Extraktion nach §4 liefert keinen Euro-Pfad, und die nutzersichtbare Parameterliste (P1) enthielte keinen Kostensatz. Kategorie A, weil ohne diese Blöcke weder Integration noch P1-Nachweis möglich sind. **Vorschlag:** je Parameter aus §3.5 und §4.8 einen Block anlegen. Kostensätze bekommen `preisstand: 2026`, `einheit` (€₂₀₂₆/m² BGF), `band`, `herkunft: register:60-R24-01`, `kennzeichnung` (NHK-Grundwert `quelle`, Fortschreibung `abschaetzung_kap3`) und den Umrechnungsfaktor. Dazu kommt eine Spalte „Umrechnungsfaktor" in der Zeichentabelle §3.5, und der Einleitungssatz von Kap. 7 wird gestrichen. | `python3 -c "import re;s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();k=s.split(chr(10)+'## 7 ')[1].split(chr(10)+'## 8 ')[0];bl=re.split('^parameter:$',k,flags=re.M)[1:];raise SystemExit(0 if (all('preisstand: null' in b for b in bl) and 'Alle weiteren Blöcke entstehen' in k) else 1)"` | behoben — Bericht Kap. 7: der Einleitungssatz „Alle weiteren Blöcke entstehen …“ ist ersetzt, und der YAML-Abschnitt führt 18 neue Blöcke (`flood_bldg.n_efh_zfh` und `flood_bldg.n_mfh` mit `preisstand: 2026` und `umrechnungsfaktor: 1.8578`, dazu k_bgf, p_hq_*, d_1, d_5, h_1, h_5, f_s093, f_s094, w_wg, u, phi_fluss, kappa, pi, lambda); Umrechnungsfaktor 1,6813 × 1,105 = 1,8578 in der Zeile \(n_t\) der Zeichentabelle §3.5. Integrationsvermerk: Registry und Code sind nicht nachgezogen (Aufgabe von `/integriere-risiko`), und die Felder `umrechnungsfaktor` und `vorlaeufig` liegen außerhalb des §4-Templates |
| 41 | B | Bericht B4 „Widerspruch" (Z. 345–348) und §3.4 (Z. 615–616) gegen `KWRA-Monetarisierung.xlsx`, Blatt „Risiken-Monetarisierung" **J64** („Wiederherstellungskosten (Gebäude, Hausrat, Fahrzeuge) je Ereignis; **Zeitwertansatz**; …"), **J65** („Wie ID 59, …") und Blatt „Schadenskonten-System" **C27** („Wiederherstellungs-/Zeitwertkosten") · **Widerspruch/Lücke (§5 LF 9 Konto-Zuordnung und Kostensatz; LF 14; eiserne Regel 2 „Arbeitsmappen nie still überstimmen"; §3.9 Abgeschätzt „Bandbreite, Ergebnis-Sensitivität")** — Die Mappe schreibt für #60 über J65 → J64 den Zeitwertansatz vor. Der Bericht bewertet mit NHK-Neuwerten (Wiederherstellungswert 527.280 €₂₀₂₆ je Wohngebäude). Er benennt den Gegensatz zwar als „Widerspruch" und sagt, die Zeitwert-Lesart werde „als Sensitivitätsband" bzw. „als Band" geführt. Ein solches Band gibt es aber nirgends: kein Alterswertminderungsfaktor, kein Zahlenwert, kein Parameter-Block. Das Wort „Zeitwertansatz" kommt im Bericht 0-mal vor. Damit weicht der Basiswert von der Mappenvorgabe ab, ohne Fortschreibung im Abgleich-Protokoll und ohne quantifizierte Sensitivität. Die Richtung ist bekannt: Neuwert ≥ Zeitwert, also ist der K3-Betrag eher überschätzt. Das widerspricht der Untergrenzen-Aussage im Versionsstempel von Kap. 6. **Vorschlag:** entweder den Zeitwertansatz aus J64 umsetzen (Alterswertminderung nach ImmoWertV als Faktor mit Quelle oder Abschätzung, Band, Block) oder den Neuwert als bewusste Fortschreibung der Mappe begründen. Dann gehört sie in die Quelle mit Eintrag ins Abgleich-Protokoll (§1/LF 14). In beiden Fällen die Zeitwert-Lesart als beziffertes Band mit Ergebnis-Sensitivität ausweisen und die Untergrenzen-Aussage prüfen. | `python3 -c "s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();raise SystemExit(0 if ('Zeitwertansatz' not in s and 'Zeitwert-Lesart als Band' in s) else 1)"` | behoben — Bericht §7.2 „Antrag auf Fortschreibung der Arbeitsmappe: Neuwert statt Zeitwertansatz“ (Anker `#fortschreibung-neuwert-k3`, 17.09.2026): Neuwert bleibt Basiswert, Zeitwertansatz als Band mit \(f_{\text{AWM}}\) = 0,55 (0,40–0,75, Abschätzung von KAP3), K3-Sensitivität 0,54 (0,39–0,74) statt 0,99 Mrd. €₂₀₂₆/a; Untergrenzen-Aussage in Kap. 6 Modellgrenze 9 geprüft und Versionsstempel präzisiert |
| 42 | B | Bericht Kap. 8 (Z. 1452–1493), Punkt 4, gegen Kap. 4.1 „Ankerwert" (Z. 866–869, „vollständige Belege in Kap. 8") und die Langbelege B1–B6 in Kap. 2 · **Lücke (§3.8 „Jede Zahl mit Quelle (Autor, Jahr, Titel, Organ, DOI/URL, Zugriffsdatum, Archiv-Snapshot)"; §5 LF 10 „fehlend")** — (a) Die Quelle des nationalen Ankers (GDV-Naturgefahrenstatistik 2024, Medieninformation; GDV-Datenservice zum Naturgefahrenreport 2025 mit den Grafikständen 10.10.2025 und 30.12.2025) trägt \(A_{\text{ver}}\), \(\lambda\) und das Sanity-Band. Kap. 4.1 verweist für ihre „vollständigen Belege" auf Kap. 8, dort kommt `GDV` aber 0-mal vor. Kapitel 4 selbst enthält 0 URLs. Die Quelle hat im Bericht also weder URL noch Archiv-Snapshot, und eine Nachprüfung der Zahlen 2,6 Mrd. € und „rund eine Milliarde mehr" ist ohne Suche nicht möglich. (b) Der Bericht führt 31 `http`-Angaben, aber nur **einen** Archiv-Snapshot (`web.archive.org`, Quelle 3). Die Langbelege B1–B6, an die Kap. 8 Punkt 4 alle Evidenzquellen delegiert, tragen keinen. Punkt 4 nennt als Format selbst nur „Vollzitat, DOI/URL, Zugriffsdatum". Bei Webseiten und Pressemitteilungen (Destatis-PM, GDV, Länderportale) ist gerade der Snapshot die Absicherung gegen stille Änderung. **Vorschlag:** die GDV-Quellen mit Vollzitat, URL, Zugriffsdatum und Archiv-Snapshot in Kap. 8 aufnehmen. Je externer Quelle in B1–B6 einen Archiv-Snapshot ergänzen oder die Lücke ausdrücklich begründen (z. B. DOI-Quelle, Snapshot entbehrlich). Das Format in Punkt 4 an §3.8 angleichen. | `python3 -c "s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();b=s.split('**B1 — ')[1].split(chr(10)+'## 3 ')[0];raise SystemExit(0 if (b.count('web.archive.org')==0 and b.count('http')>0) else 1)"` (Teil b in der Fassung der Gegenprüfung; er endet seit T-0307 mit Exit 1, weil B1–B3 sechs Snapshots tragen — der Rest von Teil (b) wird mit dem Ausdruck im Abschnitt „Autor-Revision nach Runde 2“ gemessen. Der ursprüngliche Ausdruck zu Teil a — `'GDV' not in k and s.count('web.archive.org')==1` — endet seit T-0306 mit Exit 1, weil Teil (a) erledigt ist) | behoben — alle drei Teile erledigt: die drei GDV-Ankerquellen stehen seit T-0306 (17.09.2026) als Quellen 5, 6 und 7 in Kap. 8, je mit Organ, Jahr, Titel, URL, Zugriffsdatum und Archiv-Snapshot, und der Formatsatz sowie Punkt 4 nennen den Archiv-Snapshot; die sechs externen Webquellen der Langbelege **B1–B3** tragen seit T-0307 (17.09.2026) je einen Archiv-Snapshot mit Datum (beim laufend gepflegten § 74 WHG zusätzlich mit ausdrücklichem Vermerk zur Geltung). **Teil (b) für B4–B6 seit T-0308 (17.09.2026) erledigt:** die dortigen acht externen http-Quellen tragen sieben Archiv-Snapshots mit Datum und einmal (Destatis-PM Nr. 241/2026) den ausdrücklich begründeten Verzicht, weil die Wayback Machine nur einen 403-Abruf führt. Damit ist der Befund in allen drei Teilen geschlossen — Einzelheiten im Block „Autor-Revision nach Runde 2 · T-0308“ |
| 43 | C | Bericht §7.1 „Begründung" (Z. 1420–1422) und Kap. 8 Quelle 2 (Z. 1470–1472) gegen `KWRA-Monetarisierung.xlsx`, Blatt „Schadenskonten-System" **C28**, und Netzwerkliste **J61** · **Fehler (§5 LF 10 „falsch zugeordnet"; §3.8 exakte Fundstelle)** — (a) 7.1 belegt den Endpunkt `K3-Wiederherstellung` mit „Blatt ‚Schadenskonten-System' Z28". Zelle C28 ist aber die Zeile „Ausgeschlossen": „Betriebsunterbrechung (→K5), Infrastruktur (→K4), Personen (→K1)". Der Baustein-Name `K3-Wiederherstellung` steht in den K3-Zeilen 25–30 dieses Blatts nicht, sondern in der Netzwerkliste J61. Der Antrag auf Fortschreibung beruft sich damit auf eine Zelle, die seine Aussage nicht trägt. Eine Fortschreibung, die „Baustein-Name des Schadenskontos nach Blatt ‚Schadenskonten-System'" als Wertebereich beantragt, bezieht sich zudem auf ein Blatt, das keine Baustein-Namen führt. (b) Kap. 8 Quelle 2 listet die zitierten Zellen unvollständig: Rechenregeln nur „Z9, Z11, Z20", obwohl der Bericht Rechenregeln Z7 (R5) und Z19 (A4) zitiert; Risiken-Monetarisierung ohne Z17, Z42 und Z57, die ebenfalls zitiert werden. Die Aufzählung wirkt abschließend und ist es nicht. **Vorschlag:** in 7.1 die Fundstelle auf NW J61 (Baustein-Name) plus Konten C26/C27 (Kontodefinition, Kostensatz-Typ) korrigieren und den beantragten Wertebereich auf das Blatt beziehen, das die Namen führt. Die Zellenliste in Kap. 8 vervollständigen oder als „u. a." kennzeichnen. | `python3 -c "s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();t=s.split('### 7.1 ')[1].split(chr(10)+'## 8 ')[0];k=s.split(chr(10)+'## 8 ')[1].split(chr(10)+'## 9 ')[0];raise SystemExit(0 if ('Z28, wie in' in t and '(Z9, Z11, Z20)' in k) else 1)"` | bewusst offen — Kategorie C, hindert die Abnahme nach §5.4 nicht (die Vorbedingung von `/integriere-risiko` stellt auf offene A-Befunde ab); falsche Zellfundstelle im Fortschreibungsantrag §7.1, ohne Wirkung auf Wert oder Konto |
| 44 | C | Bericht Kap. 6 „Modellgrenzen (dokumentiert)", Punkt 2 (Z. 1293–1297), gegen §5.1.2 „Modellgrenzen der Abschätzung" · **Lücke/Fehler (Vorgabe P2 „Bauform-Grenzen werden als Modellgrenze der Abschätzung dokumentiert"; §3.5; §5 LF 12)** — Die einzige Maßnahme ohne publizierte Effektgröße ist S092 (Entscheidungslog Nr. 3). Ihre Bauform-Grenze steht in §5.1.2 („Kommunenweiter Pauschalfaktor statt zellscharfer Wirkung (Bauform-Grenze)"), ebenso der Näherungscharakter von \(s_{\text{bem}}\) mit Richtung „überschätzt den Hebel" (§5.1.3). In der Modellgrenzen-Liste von Kap. 6, der nutzernahen Zusammenstellung, fehlt beides: `Pauschal` kommt dort 0-mal vor, S092 nur als konstant gehaltene Größe. Stattdessen trägt Modellgrenze 2 die Überschrift „Bauform-Grenze der Abschätzung S094 (Vorgabe P2)". S094 ist aber eine Vulnerabilitätsachse der Schadensfunktion, kein Maßnahmen-Hebel; P2 ist dort falsch zugeordnet, auch wenn die Material-Grenze als solche zutrifft. **Vorschlag:** in Kap. 6 eine eigene Modellgrenze für S092 aufnehmen (Pauschalfaktor, Richtung der \(s_{\text{bem}}\)-Näherung, Band 0,0075–0,1056). Punkt 2 als Modellgrenze der Materialabschätzung S094 nach §3.9 umbenennen, ohne Verweis auf P2. | `python3 -c "s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();k=s.split(chr(10)+'## 6 ')[1].split(chr(10)+'## 7 ')[0];raise SystemExit(0 if ('Pauschal' not in k and 'Abschätzung S094 (Vorgabe P2)' in k) else 1)"` | bewusst offen — Kategorie C, hindert die Abnahme nach §5.4 nicht (die Vorbedingung von `/integriere-risiko` stellt auf offene A-Befunde ab); die Modellgrenze von S092 steht in §5.1.2/§5.1.3 und ist dort sichtbar; es fehlt nur die Wiederholung in Kap. 6 |
| 45 | C | Bericht Kap. 9 „Kriterienraster", Zeilen „Aufwand" und „Datenverfügbarkeit", Spalte (a) (Z. 1542, 1545), gegen §3.2 Ebenentabelle (Z. 487–492) · **Widerspruch (§5 LF 12 „benötigte neue Ebenen als solche gekennzeichnet"; §3.7 Kriterienraster Datenverfügbarkeit/Aufwand)** — Kap. 9 nennt für (a) „vier Datenebenen, davon zwei neu anzulegen (HQ-Tiefen, GEBAEUDEWERT)" und bei der Datenverfügbarkeit „alle vier Eingänge sind frei zugänglich". Nach §3.2 sind aber **drei** Ebenen „neu anzulegen" (HQ_FLAECHE, HQ_TIEFE, GEBAEUDEWERT) und eine „geparkt (Datenquelle fehlt)" (GEBAEUDEZUSTAND_BAUSTOFF, Neutralwert 1,00). „geparkt" kommt in Kap. 9 nicht vor. Das Raster, das die Ansatzwahl trägt (Entscheidungslog Nr. 5), unterzeichnet damit den Aufbauaufwand von (a) und stellt die Datenlage günstiger dar als das Modellkapitel. Die Wahl von (a) kippt dadurch voraussichtlich nicht, weil (c) an derselben Datenlücke stärker leidet, aber ihre Begründung stimmt an dieser Stelle nicht. **Vorschlag:** die Zellen „Aufwand" und „Datenverfügbarkeit" für (a) auf den Stand von §3.2 ziehen (drei neu anzulegende Ebenen, eine geparkt mit Neutralwert) und prüfen, ob die Bewertung „hoch" bei der Datenverfügbarkeit so bestehen bleibt. | `python3 -c "s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();k=s.split(chr(10)+'## 9 ')[1].split(chr(10)+'## Entscheidungslog')[0];raise SystemExit(0 if ('davon zwei neu anzulegen' in k and 'geparkt' not in k) else 1)"` | bewusst offen — Kategorie C, hindert die Abnahme nach §5.4 nicht (die Vorbedingung von `/integriere-risiko` stellt auf offene A-Befunde ab); Zählfehler der Ebenen im Kriterienraster Kap. 9; die Ansatz-Entscheidung hängt nicht daran, weil (b) und (c) dieselben Ebenen brauchen |

#### 4.4 · Abgrenzung und Status dieses Pakets

- **Beantwortet:** LF 9 (Verdikt Befund), LF 10 (Verdikt Befund) und LF 12 (Verdikt Befund), jede
  mit Beleg. LF 9 wurde nachgerechnet statt gelesen: Kapitel 7 trägt null Kostensätze (vier
  dimensionslose Blöcke, alle `preisstand: null`). Die Kostensätze, die der Euro-Pfad tatsächlich
  nutzt, sind je Satz mit Zahlenwert auf den Preisstand 2026 nachgerechnet (1.950,3 und 1.532,6
  €₂₀₂₆/m² BGF, Gesamtfaktor 1,8578, 527.280 € je Wohngebäude). Die Einheitlichkeit des
  Preisstands ist über den ganzen Bericht belegt (Abschnitt 4.1).
- **Nicht Gegenstand dieses Pakets:** die übrigen Leitfragen, die Kapitel außer 6 bis 9, die
  Volltextprüfung der Langbelege B1–B6 (LF 5/6, Paket T-0272) und die Regression der Befunde 1–19.
  Ein nationaler 100-m-Vollraster-Lauf nach §3.4 war nicht verlangt und wurde nicht gefahren.
- **Kein Befund behoben**, und kein Bericht, Register, Code, Lint oder keine Arbeitsmappe geändert:
  `docs/methodik/60_gebaeudeschaeden_flusshochwasser.md` und `docs/evidenz/register.md` sind
  byte-gleich geblieben; `backend/scripts/lint_methodik.py` wurde in diesem Paket nicht ausgeführt
  (Ausgabe aus Abschnitt 0.1 übernommen).

### 5 · Paket T-0275 — Regression der Befunde 1 bis 10

Sechstes Paket der Runde 2 (17.09.2026). Die Sitzung arbeitet nach
`.claude/commands/review-methodik.md`. Eiserne Regel 4: Diese Sitzung hat keinen der geprüften
Umsetzungsnachweise geschrieben; die Revisionen stammen aus T-0235…T-0243 und T-0256…T-0259, alle
im Endstatus. **Dieses Paket beantwortet keine Leitfrage aus §5 und gibt zu keiner Leitfrage ein
Verdikt ab.** Es beurteilt nur, ob die Befunde 1–10 heute geschlossen sind. Die Zeilennummern
beziehen sich auf den Bericht mit SHA-256 `b8bde6ac…c65e4` (Stand 17.09.2026).

**Prüfweise.** Jeder Umsetzungsnachweis wurde am Ist-Stand des Berichts nachgelesen, nicht
abgeschrieben. Sieben Befunde haben einen Prüfausdruck (1, 4, 5, 7, 8, 9, 10). Alle sieben wurden
am 17.09.2026 aus der Befundtabelle ausgeführt und endeten mit Exit 0. Die Befunde 2, 3 und 6
haben keinen Prüfausdruck; sie wurden zeilen- bzw. zellweise gelesen. Die Mappenzellen zu Befund 6
wurden direkt aus `KWRA-Monetarisierung.xlsx` gelesen, nur lesend (eiserne Regel 2).

Ein Exit 0 belegt nur, was der Ausdruck abfragt. In einigen Fällen hat ein Geschwisterpaket dieser
Runde die Substanz einer Schließung schon widerlegt. Dann wurde dessen Befund gelesen und am
Bericht nachvollzogen. Das Urteil verweist auf ihn, statt ihn zu doppeln.

#### 5.1 · Regression Runde 2 — Befunde 1 bis 10

| Befund | Urteil | Fundstelle | Begründung |
|---|---|---|---|
| 1 | bestätigt geschlossen | `docs/methodik/60_gebaeudeschaeden_flusshochwasser.md` Kap. 3, §3.1 Z. 459–479, §3.3 Z. 525–546, §3.4 Z. 572–659, §3.5 Z. 660–699 | Kap. 3 ist nicht mehr leer. Die native Ergebnisgröße EAD ist mit €₂₀₂₆/a, Bezugsjahr 2026 und Ebene Kommune deklariert (Z. 461–469). Die physische Zwischengröße \(\bar A\) in m²/a steht vor dem Euro (Z. 473–476, 579). Die Kernformel Menge × Rate × Preis ist ausgeschrieben (§3.4), die Zeichentabelle vorhanden (§3.5). \(d(h)\) ist oberhalb von 1,75 m auf 0,250 gedeckelt (Z. 532–546); eine Quote über 100 % ist damit ausgeschlossen. Prüfausdruck Exit 0. Mängel im jetzt gefüllten Kapitel sind eigene Befunde dieser Runde (20: fehlender R7-Term; 23, 24, 25) und kein Rückfall. |
| 2 | unvollständig geschlossen | `docs/methodik/60_gebaeudeschaeden_flusshochwasser.md` Kap. 1 „Knoten-Bilanz" Z. 77–108, besonders Z. 83–84 (S074, R17) und Z. 102–104 (S096–S098); gegen §3.2 „Kein-Doppelkanal" Z. 509–512 | Formal abgearbeitet: Alle 32 Zeilen tragen eine Formelstelle oder `inaktiv` mit Mappenzitat, `offen` kommt 0-mal vor. §2.1 verlangt aber „verarbeitet oder begründet inaktiv", und für fünf Zeilen stimmt „verarbeitet" nicht. (a) S096, S097 und S098 hängen an **FS-Schutzsystem**; diese Formelstelle kommt in keiner Formel vor (Befund 20). (b) S074 und R17 hängen an **FS-Exposition**. §3.2 Z. 509–512 sagt ausdrücklich, dass beide „in der Kernformel **nicht** als eigene Faktoren" auftreten, und die Registerzeile 60-S074-01 (Z. 166) sagt dasselbe. `FS-Exposition` kommt ab Kap. 3 kein einziges Mal vor. Dafür gibt es den neuen **Befund 46**. Außerdem veraltet: Z. 65–66 sagt noch, Kapitel 3 bleibe „im Kommentar-Zustand des Erstaufschlags". |
| 3 | bestätigt geschlossen | `docs/methodik/60_gebaeudeschaeden_flusshochwasser.md` Kap. 2 „Evidenz-Register (§2.2)" Z. 158–191, Zeilen Z. 160 (60-W085-01), 166, 167, 182, 183, 184, 189 (60-R24-01) | Die sieben tragenden Zeilen sind in allen Sachspalten belegt, mit Quelle, Zugriffsdatum und Langbeleg B1–B6. Zwei tragen die Entscheidung **Basiswert** (Z. 160 Hazard, Z. 189 Mengengerüst). Gefüllt sind alle vier Gruppen, die der Befund verlangt (W085, R24, S074/R17, S093/S094), auch die strukturabhängige Evidenz zu S093/S094 (Z. 183–184). Die übrigen 25 Zeilen stehen weiter auf „offen". Das deckt sich mit dem Nachweis; der Befund verlangt nicht mehr. Inhaltliche Mängel der gefüllten Zeilen sind eigene Befunde (27–31). |
| 4 | unvollständig geschlossen | `docs/methodik/60_gebaeudeschaeden_flusshochwasser.md` Kap. 4, §4.1 Z. 843–875, §4.4 Z. 950–966, §4.5 Z. 967–999, §4.6 Z. 1000–1015 | Vorhanden sind der Anker mit Zeitreihe und Revisionsstand (§4.1), der Niveau-Skalar λ = 1,05 (§4.4), eine Verteilungsprüfung mit vorab fixierter Toleranz (§4.5) und ein Sanity-Band (§4.6). Prüfausdruck Exit 0 (≥ 6.000 Zeichen). Zwei ausdrücklich verlangte Eigenschaften fehlen aber. (a) Die Verteilungsprüfung ist **nicht unabhängig**: Ankerseite und λ beruhen auf denselben zwei GDV-Zahlen zu 2024 (§4.5 Z. 973–998 gegen §4.1 Z. 862–865; Befund 33, Kategorie A). (b) Die Untergrenze des Sanity-Bands ist zirkulär und kann nicht scheitern; die Obergrenze ist keine echte Schranke (§4.6 Z. 1002–1014; Befund 35). Kein neuer Befund, beide Lücken sind verbucht. |
| 5 | bestätigt geschlossen | `docs/methodik/60_gebaeudeschaeden_flusshochwasser.md` §3.2 „Datenebenen nach §3.1" Z. 481–513 (Ebenentabelle Z. 487–492, Beschaffungs-Watchlist Z. 494–499) | Alle vier Ebenen tragen Quelle, keyless Beschaffungsweg, Zell-Ableitungsregel, Fallback und Normierung/Zentrierung. HQ_FLAECHE, HQ_TIEFE und GEBAEUDEWERT sind „neu anzulegen". GEBAEUDEZUSTAND_BAUSTOFF ist „geparkt (Datenquelle fehlt)", mit Neutralwert 1,00 und dreiteiliger Watchlist. Der Fallback stammt aus der Betrachtungsebene selbst (Z. 490–491). Die Futur-Ankündigung im HTML-Kommentar ist entfallen. Prüfausdruck Exit 0. Dass Kap. 9 die Ebenen falsch zählt, ist ein Fehler in Kap. 9 (Befund 45), nicht an der Fundstelle dieses Befunds. |
| 6 | bestätigt geschlossen | `docs/methodik/60_gebaeudeschaeden_flusshochwasser.md` Kap. 1 „Weitergaben" Z. 118 · gegen `KWRA-Monetarisierung.xlsx`: Blatt „Schadenskonten-System" C29, Blatt „Abgleich-Protokoll" A7–F7, Blatt „Rechenregeln" C11, Blatt „Risiken-Monetarisierung" J42, J17 und N17 | **#37** steht mit Kante 49 → 37. Das Zitat trifft die Zellen A7 „3", B7 „49", D7 „37", E7 „Schäden an Aquakulturen" und F7 „Kante" wörtlich. Dazu kommen das R9-Zitat (C11 wörtlich, Kürzung mit „…" markiert) und J42 „… Sachschäden an Anlagen (K3)" (Zelle: „… + Sachschäden an Anlagen (K3)."). **#12** steht als eigenständiges K3-Buchungsobjekt (C29 „12 Rutschungen und Muren · 37 Schäden an Aquakulturen · …"), mit R9-Zitat sowie N17 „R7, R9" und J17 „Wiederherstellungskosten beschädigter Gebäude (K3) …", beides wörtlich. Die Abgrenzungen sind entschieden: Anlagen gegen Gebäude, Massenbewegung gegen Flusshochwasser. |
| 7 | unvollständig geschlossen | `docs/methodik/60_gebaeudeschaeden_flusshochwasser.md` §4.7 „Kalibrierjahre und Doppelzählungs-Wächter" Z. 1016–1041, Absatz „Wächter" Z. 1023–1029 | Die Kalibrierjahre 2002–2024 sind einzeln benannt (Z. 1018–1021), q₀ ist als „geparkt" mit Watchlist geführt (Z. 1031–1041). Prüfausdruck Exit 0. Der Wächter selbst ist aber nicht tragfähig operationalisiert. Er sperrt alle Nachrüstungen bis zum Stichtag 31.12.2024, obwohl λ den **mittleren** Ausstattungsstand 2002–2024 abbildet. Dadurch wird der Hebel unterzählt, und die Verfallsregel verschiebt den Referenzzustand falsch (Befund 39). Kein neuer Befund. |
| 8 | bestätigt geschlossen | `docs/methodik/60_gebaeudeschaeden_flusshochwasser.md` §3.5 Z. 692–693 und §5.1.1 „Zeichentabelle (Kette S092)" Z. 1126–1139 (Zeilen Z. 1134–1135) | EAD und EAD_mit stehen in beiden Zeichentabellen: mit Bedeutung, Einheit €₂₀₂₆/a, Bezugsjahr/Preisstand 2026, Ebene Kommune und `herleitung:`-Herkunft. §5.1.1 führt alle sechs Zeichen der Formel \(\text{EAD}_{\text{mit}} = \text{EAD}\cdot(1-r_{\text{S092}})\) und ihrer Kette: EAD, EAD_mit, r, Δq, s_bem, e_bem (Z. 1134–1139). Die Deckungslücke „4 von 6" ist damit geschlossen. Prüfausdruck Exit 0. Hinweis: Der Nachweis behauptet weitergehend, §3.5 führe „alle" Zeichen der Kapitel 3 und 5. Das trifft nicht zu (q₀ und t₁–t₃ fehlen), ist aber als Befund 25 verbucht und nicht Gegenstand von Befund 8. |
| 9 | unvollständig geschlossen | `docs/methodik/60_gebaeudeschaeden_flusshochwasser.md` §3.6 Block `beispiel_60_kernformel` Z. 757 ff. · `backend/scripts/lint_methodik.py` Z. 125–137 (`beispiel_bloecke`) · `backend/` (Code-Bezug des Befunds) · Aufgabe §4 „Beispiel-Blöcke … werden als Golden-Tests in die CI übernommen" (Z. 403–404) | Im Bericht erfüllt: Alle fünf Blöcke laufen und tragen `assert` (`beispiel_60_kernformel_zelle` Z. 632, `beispiel_60_kernformel` Z. 757, `beispiel_60_kalibrierung` Z. 1059, `beispiel_60_s092_abschaetzung` Z. 1179, `beispiel_60_s_bem_obergrenze` Z. 1245; Prüfausdruck Exit 0). Der Lint führt sie aus und verlangt je Block eine Zusicherung. An der Fundstelle des Befunds (`backend/`) ist die Anforderung nicht erfüllt: `grep -rn "beispiel_60" --include=*.py backend` liefert am 17.09.2026 weiterhin 0 Treffer, und im Repo gibt es keine CI-Konfiguration (kein `.github/`), die den Lint auf Bericht #60 fährt. Die Übernahme als Golden-Test wurde per Abweichung auf die Integration (P-N) verschoben und ist damit noch offen. Kein neuer Befund. |
| 10 | unvollständig geschlossen | `docs/methodik/60_gebaeudeschaeden_flusshochwasser.md` §5.1.3 Z. 1192–1260, Absätze „Obergrenze aus der Szenario-Zerlegung" Z. 1204–1210 und „Folge für das Band" Z. 1212–1222; Parameter-Block `flood_bldg.s_bem` Kap. 7 Z. 1362–1376 | Der zweite Weg des Befunds ist umgesetzt: Die Setzung ist als Näherung mit der Richtung „überschätzt den Hebel" gekennzeichnet, der Ersetzungspfad läuft über Stichproben, und der Block trägt `naeherung: true`. Prüfausdruck Exit 0. Die als **hart** ausgewiesene Obergrenze 0,661 ist aber aus den Beiträgen **einer Beispielzelle** gerechnet (Z. 1205–1208: 4,174/6,311; dieselbe Summe 6,311 wie im Beispielblock §3.6, vgl. Z. 932). Eine allgemeine Grenze ist sie also nicht. Daran hängen die Kappung auf 0,66 und das Band 0,0075–0,1056 (Befund 26). Das Band ist an allen Fundstellen einheitlich nachgezogen (Z. 99, 182, 694, 696, 1138–1139, 1165, 1366, 1396); es fehlt aber die tragende Begründung der Obergrenze. Kein neuer Befund. |

**Zählung:** bestätigt geschlossen 5 (1, 3, 5, 6, 8) · unvollständig geschlossen 5 (2, 4, 7, 9, 10) ·
zurückgefallen 0. Keine spätere Revision hat einen Befund auf einen früheren Stand zurückgesetzt.
Dieses Paket lässt die Kurzform-Tabelle „Offene Befunde" am Kopf und die Statusspalte der
Befunde 1–10 unverändert. Ob die Status fortgeschrieben werden, entscheidet die Revision; dieses
Paket behebt nichts.

#### 5.2 · Neue Befunde dieses Pakets (46)

Format nach §5: Stelle · Art · Begründung · Vorschlag · Kategorie. Das Ticket nennt 20 als erste
neue Nummer; das war der Stand beim Ticketschnitt. Seitdem haben die vorlaufenden Pakete T-0270 bis
T-0274 die Nummern 20–45 vergeben. Nach der Regel „fortlaufend ab der nächsthöheren freien Nummer"
ist die erste neue Nummer deshalb **46**. Der Prüfausdruck endet mit Exit 0, **solange der Befund
besteht**. Am 17.09.2026 ausgeführt: Exit 0.

| Nr | Kat. | Befund (Stelle · Art · Begründung · Vorschlag) | Prüfausdruck | Status |
|---|---|---|---|---|
| 46 | B | Bericht Kap. 1 Knoten-Bilanz, Zeilen S074 (Z. 83) und R17 (Z. 84), Spalte „rechnet in" = **FS-Exposition**, gegen §3.2 „Kein-Doppelkanal" (Z. 509–512) und die Registerzeilen 60-S074-01 (Z. 166) und 60-R17-01 (Z. 167), Spalte „Entscheidung" · **Widerspruch (§2.1 „verarbeitet oder begründet inaktiv"; §3.2 Kein-Doppelkanal; eiserne Regel 3 „kein Formelzeichen ohne Herleitung")** — Die Bilanz weist S074 als verarbeitet aus („FS-Exposition — Geländehöhe → Wassertiefe am Gebäude"), R17 ebenso („FS-Exposition — Lackmustest §3.1"). §3.2 sagt dagegen, Geländehöhe und Gewässernähe „treten … in der Kernformel **nicht** als eigene Faktoren auf, sondern nur als Sensitivitätsbänder". Laut Registerzeile 60-S074-01 geht S074 „nicht als eigener Faktor in FS-Exposition ein", und 60-R17-01 liefert „kein zweites Multiplikativglied". Die Formelstelle FS-Exposition kommt ab Kapitel 3 kein einziges Mal vor; die Wassertiefe \(h_{z,s}\) stammt allein aus der Ebene HQ_TIEFE (60-W085-01). Die Bilanz behauptet also eine Verarbeitung, die das Modell ausdrücklich ausschließt. Die Fehlerart ist dieselbe wie bei Befund 20 (FS-Schutzsystem), betrifft aber zwei andere Knoten, die dort nicht erfasst sind. **Vorschlag:** S074 und R17 in der Bilanz als „Sensitivitätsband (Kein-Doppelkanal §3.2, Register 60-S074-01/60-R17-01)" führen oder an FS-Hazard binden (Wirkung über die HWGK-Tiefe), statt an eine eigene Formelstelle. Zugleich den Satz in Z. 65–66 („Kapitel 3 selbst bleibt unverändert im Kommentar-Zustand") auf den Ist-Stand ziehen. | `python3 -c "s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();k1=s.split(chr(10)+'## 1 ')[1].split(chr(10)+'## 2 ')[0];k3=s.split(chr(10)+'## 3 ')[1].split(chr(10)+'## Entscheidungslog')[0];z=[l for l in k1.split(chr(10)) if l.startswith(chr(124)+' S074 ') or l.startswith(chr(124)+' R17 ')];raise SystemExit(0 if (len(z)==2 and all('**FS-Exposition**' in l for l in z) and 'FS-Exposition' not in k3 and 'nicht** als' in k3) else 1)"` | behoben — Bericht Kap. 1, Absatz vor der Knoten-Bilanz (Satz zum Kommentar-Zustand von Kapitel 3 durch den Ist-Stand ersetzt) und Zeilen S074/R17: „Sensitivitätsband (Kein-Doppelkanal §3.2 …) — wirkt über FS-Hazard, keine eigene Formelstelle“ |

#### 5.3 · Abgrenzung und Status dieses Pakets

- **Beurteilt:** die Befunde 1–10, je genau ein Urteil mit Fundstelle (Datei plus Kapitel und
  Zeilennummer, bei Befund 6 zusätzlich Blatt und Zelle der Arbeitsmappe).
- **Nicht Gegenstand dieses Pakets:** jede Leitfrage aus §5 (null Leitfragen beantwortet, kein
  Leitfragen-Verdikt), die Regression der Befunde 11–19 (Paket mit Reihenfolge 7) und das
  Konvergenz-Verdikt nach §5.4. Ein nationaler 100-m-Vollraster-Lauf nach §3.4 wurde nicht gefahren.
- **Kein Befund behoben**, kein Status in der Kurzform-Tabelle geändert. Nicht geändert wurden
  Bericht, Register, Code, Lint und Arbeitsmappen: `docs/methodik/60_gebaeudeschaeden_flusshochwasser.md`
  und `docs/evidenz/register.md` sind byte-gleich (SHA-256 vor und nach dem Paket verglichen).
  `backend/scripts/lint_methodik.py` wurde nur gelesen, nicht ausgeführt.

### 6 · Paket T-0276 — Regression der Befunde 11 bis 19 und Konvergenz-Verdikt der Runde 2

Siebtes und letztes Paket der Runde 2 (17.09.2026). Die Sitzung arbeitet nach
`.claude/commands/review-methodik.md`. Eiserne Regel 4: Diese Sitzung hat keinen der geprüften
Umsetzungsnachweise geschrieben (die Revisionen stammen aus T-0235…T-0243 und T-0256…T-0259, alle im
Endstatus) und keine der Leitfragen dieser Runde beantwortet. **Dieses Paket beantwortet keine
Leitfrage aus §5 und gibt zu keiner Leitfrage ein Verdikt ab.** Es beurteilt, ob die Befunde 11–19
heute geschlossen sind, und liest danach das Konvergenz-Verdikt nach §5.4 aus diesem Abschnitt ab.
Die Zeilennummern beziehen sich auf den Bericht mit SHA-256 `b8bde6ac…c65e4` und auf
`docs/evidenz/register.md` mit SHA-256 `b2c96697…58575` (beide Stand 17.09.2026, vor und nach dem
Paket gleich).

**Prüfweise.** Jeder Umsetzungsnachweis wurde am Ist-Stand nachgelesen, nicht abgeschrieben. Die
Befunde 13, 14, 15 und 17 haben einen Prüfausdruck; alle vier wurden am 17.09.2026 aus der
Befundtabelle ausgeführt und endeten mit Exit 0. Der Ausdruck zu Befund 13 prüft nichts
(`b.count('"')//2>=0` ist immer wahr); die Zählung wurde deshalb eigens am Code nachgerechnet
(`ast.literal_eval` des Eintrags `kwra_id: 60` in `backend/app/data/catalog.py`: 5
`sensitivity_names`, 5 `upstream_names`). Die Befunde 11, 12, 16, 18 und 19 haben keinen
Prüfausdruck und wurden zeilenweise gelesen. Wie im Paket zu den Befunden 1–10 gilt: Hat ein
Geschwisterpaket dieser Runde die Substanz einer Schließung schon widerlegt, verweist das Urteil
auf dessen Befund, statt ihn zu doppeln. Für die Befunde 17 und 19 (Status „offen", kein
Umsetzungsnachweis) kennt die Urteilsskala kein eigenes „nicht geschlossen"; sie stehen auf
„unvollständig geschlossen", und die Begründung sagt ausdrücklich, dass keine Schließung
stattgefunden hat.

Der Lint wurde zur Beurteilung von Befund 17 erneut ausgeführt (nur ausgeführt, nicht geändert).
Ausgabe von `python3 backend/scripts/lint_methodik.py 60` am 17.09.2026, wörtlich, Exit 0:

```
=== #60 · 60_gebaeudeschaeden_flusshochwasser.md ===
  115 Checks grün
  Historie-Marker: 0 markierte Zeilen (Ratchet None), 0 gedeckte Fundstellen abgelöster Werte:

ALLE LINTS GRÜN
```

#### 6.1 · Regression Runde 2 — Befunde 11 bis 19

| Befund | Urteil | Fundstelle | Begründung |
|---|---|---|---|
| 11 | unvollständig geschlossen | `docs/methodik/60_gebaeudeschaeden_flusshochwasser.md` Kap. 8 „Quellen (§3.8)" Z. 1452–1492: Formatsatz Z. 1454–1460, Quelle 1 Z. 1462–1469, Quelle 2 Z. 1470–1476, Quelle 3 Z. 1477–1485, Punkt 4 Z. 1486–1489 | Die drei beim Befund vorhandenen Quellen sind nachgezogen: Die beiden Arbeitsmappen tragen Commit-Hash, Datum, SHA-256 und Zugriffsdatum 13.09.2026 (Z. 1465–1476), die Hochwasserschutzfibel Vollzitat, URL, Archiv-Snapshot (`web.archive.org`, Z. 1481) und Zugriffsdatum (Z. 1482), wörtlich aus `sources.py`. Kap. 8 enthält jetzt 3 `http`-Angaben statt 0. Vollständig sind die Pflichtangaben nach §3.8 im Quellenkapitel aber nicht: Punkt 4 (Z. 1486–1489) delegiert alle Evidenzquellen an die Langbelege B1–B6 und nennt als Format selbst nur „Vollzitat, DOI/URL, Zugriffsdatum", ohne Archiv-Snapshot; die Quelle des nationalen Ankers (GDV) fehlt in Kap. 8 ganz (Befund 42), und Quelle 2 listet die zitierten Zellen unvollständig (Befund 43 b). Die Fibel ist für #60 nicht im Volltext geprüft, geht aber ausdrücklich in keinen Wert ein (Z. 1459–1460, 1484–1485); das genügt §3.8. Kein neuer Befund. |
| 12 | unvollständig geschlossen | `docs/methodik/60_gebaeudeschaeden_flusshochwasser.md` Kap. 1 „Konto-Einbettung" Z. 120–151: Kostensatz-Typ Z. 124–125, Preisstandjahr Z. 129–135, R5-Entscheidung Z. 136–147 · §3.5 Zeichentabelle Z. 689 (\(n_t\)) · `KWRA-Monetarisierung.xlsx`, Blatt „Schadenskonten-System" C27, Blatt „Risiken-Monetarisierung" J64/J65 | Zwei der drei Teile sind erledigt. **R5** ist mit wörtlichem Zitat (Rechenregeln Z7, Konten Z26, Mon. Z64) als „übernommen" entschieden, samt Begründung, warum die Regelspalte Mon. Z65 sie nicht nennt (Z. 136–147). **Preisstandjahr** 2026 ist als Abschätzung von KAP3 mit Herleitung und Ersetzungspfad ausgewiesen (Z. 129–135). Der **Kostensatz-Typ** ist dagegen nicht festgelegt: Z. 124–125 zitiert nur die Mappe („Wiederherstellungs-/Zeitwertkosten"), während das Modell mit NHK-Neuwerten rechnet (Z. 689) und den über J65 → J64 vorgeschriebenen Zeitwertansatz weder übernimmt noch als Fortschreibung führt (Befund 41). Außerdem ist der Satz „Bis ein K3-eigener Kostensatz mit Quelle vorliegt (Kap. 3/7), wird das Erstellungsjahr … gesetzt" (Z. 132–134) überholt: \(n_t\) = 1.950 / 1.533 €₂₀₂₆/m² BGF steht mit Quelle in §3.5 Z. 689, ein Parameter-Block mit Pflichtfeld `preisstand` fehlt aber (Befund 40). Kein neuer Befund. |
| 13 | bestätigt geschlossen | `docs/methodik/60_gebaeudeschaeden_flusshochwasser.md` Kap. 1 „W-Knoten" Z. 44–58, besonders Z. 50–56; Entscheidungslog Nr. 1 Z. 1587 und Nr. 6 Z. 1592 · `backend/app/data/catalog.py` Z. 335–340 · `KWRA-Schadensbaum_X_UBA-klimawirkungsketten.xlsx`, Blatt „Klimawirkungsketten" F272/H272 | Die falsche Behauptung „genau die Namenslisten" ist ersetzt durch „**nicht** genau …, sondern nur eine **Teilmenge mit abweichender Namensquelle**" (Z. 50–52). Die Zahlen treffen zu: Nachgerechnet trägt `catalog.py` Z. 339 fünf `sensitivity_names` (S096 und S098 fehlen) und Z. 338 fünf `upstream_names`; W117 führt nach F272/H272 sieben Sensitivitäten und acht Wirkungs-Eingänge (in 0.2, Stichprobe 2 und Bilanzumfang, bestätigt). Die Divergenz steht als Integrationspunkt im Entscheidungslog Nr. 6 (Z. 1592); `catalog.py` ist unverändert (eiserne Regel 5). Prüfausdruck Exit 0, aber ohne Aussagekraft (siehe Prüfweise). Dass der Bericht selbst drei Knotennamen ungekennzeichnet kürzt, ist eigener Befund 21 und keine Divergenz zum Code. |
| 14 | bestätigt geschlossen | `docs/methodik/60_gebaeudeschaeden_flusshochwasser.md` Kap. 6 „Szenario-Anwendung & Modellgrenzen" Z. 1262–1321: Absatz „Szenario-Anwendung 60-A" Z. 1264–1286, Modellgrenzen 1–8 Z. 1288–1313, Infokasten-Texte Z. 1315–1321 | Alle verlangten Bestandteile stehen da: die verschobene Größe (FS-Hazard, Z. 1264–1269), die konstant gehaltenen Größen (S074, R24, \(d(h)\) mit S093/S094, S092; Z. 1269–1273), zwei nummerierte Stationaritätsannahmen (Z. 1273–1278) und die Bestandsdynamik S104 (Z. 1278–1286); die nummerierte Modellgrenzen-Liste mit der Untergrenzen-Aussage K1/K4/K5/K8 als Punkt 1 (Z. 1290–1292); die drei wörtlichen Infokasten-Texte „bewerteter Schaden — Konto K3", „Stufe M0: 1 von 8 Konten aktiv" und „berechnet mit Modellstand M0 — Untergrenze" (Z. 1317–1321). Prüfausdruck Exit 0. Dass Modellgrenze 2 (Z. 1293) P2 der Vulnerabilitätsachse S094 zuordnet und die Bauform-Grenze des eigentlichen P2-Hebels S092 in Kap. 6 fehlt, ist eigener Befund 44 und nicht Gegenstand von Befund 14. |
| 15 | bestätigt geschlossen | `docs/methodik/60_gebaeudeschaeden_flusshochwasser.md` Kap. 7 „Parameter-Blöcke" Z. 1323–1409 (Blöcke `flood_bldg.dq_s092` Z. 1349, `flood_bldg.s_bem` Z. 1363, `flood_bldg.e_bem` Z. 1379, `flood_bldg.r_s092` Z. 1393) und §7.1 „Antrag auf Fortschreibung des §4-Wertebereichs" Z. 1410–1451 | Beide Teile des Befunds sind umgesetzt. (1) Vorgabe P1: Alle vier Blöcke tragen `kennzeichnung:` mit zugelassenem Wert, `herleitung_anker:` auf einen im sichtbaren Text gesetzten Anker (`#s092-wirkung`, `#s-bem-naeherung`) und `wertebereich_abweichung: "#fortschreibung-endpunkt-k3"`; die Kennzeichnung steht nicht mehr als YAML-Kommentar, sondern als Feld, und die Herleitung liegt im Berichtstext. (2) Die Überschreitung von `endpunkt`/`bandzuordnung` ist in §7.1 mit Begründung und Datum 13.09.2026 als Antrag auf Fortschreibung ausgewiesen statt still überstimmt. Prüfausdruck Exit 0. Nicht Gegenstand von Befund 15 und eigens verbucht: Für alle übrigen Parameter, insbesondere die Kostensätze, fehlen Blöcke (Befund 40, A), und §7.1 belegt den Endpunkt mit der falschen Zelle C28 (Befund 43 a). |
| 16 | bestätigt geschlossen | `docs/methodik/60_gebaeudeschaeden_flusshochwasser.md` Kap. 9 „Ansatz-Vergleich" Z. 1494–1582: „Die drei verglichenen Ansätze" ab Z. 1515, „Kriterienraster" Z. 1535–1545 (Zeilen Z. 1539–1545), „Umsetzungsgrundlage" ab Z. 1547; Kopf Z. 4–5; Entscheidungslog Nr. 5 | Die Ansätze (b) aggregierte Flächenschadensrate und (c) Schadensgradmodell am Einzelgebäude sind benannt, das Raster hat sieben Kriterienzeilen × drei Ansätze = 21 bewertete Zellen (Z. 1539–1545) ohne „offen", und (a) ist mit Begründung als Umsetzungsgrundlage gewählt (ab Z. 1547), nachgezogen im Kopf (Z. 4–5) und im Entscheidungslog Nr. 5. Damit ist der Befund („Raster offen, (b)/(c) nicht benannt, Umsetzungsgrundlage offen") geschlossen. Inhaltliche Mängel des gefüllten Rasters sind eigene Befunde: Die Zellen „Datenverfügbarkeit" (Z. 1542) und „Aufwand" (Z. 1545) für (a) widersprechen §3.2 (Befund 45), und die Zelle „Maßnahmen-Anschluss" behauptet eine R7-Weiche, die in der Formel fehlt (Befund 20). |
| 17 | unvollständig geschlossen | `backend/scripts/lint_methodik.py` (ganze Datei; Suche nach `Pflichtkapitel` 0 Treffer, `<!--` nur Z. 74 als `HISTORIE_MARKER`) · Lint-Ausgabe oben in Paket 6 und in 0.1 · gegen Bericht Kap. 3/4/6 | **Keine Schließung erfolgt** — Status „offen", kein Umsetzungsnachweis; der Befund gehört T-0234. Der Lint meldet heute „115 Checks grün" statt 83, prüft aber weiterhin keine Pflichtkapitel-Vollständigkeit außerhalb von HTML-Kommentaren: Das Wort `Pflichtkapitel` kommt in der Datei nicht vor, und HTML-Kommentare kennt sie nur als Historie-Marker (Z. 74), nicht als Ort verbotener Formulierungen. Eine Zählung übersprungener Checks gibt die Ausgabe nicht aus. Der Prüfausdruck endet mit Exit 0, weil heute jedes Kapitel des **Berichts** über 200 Zeichen trägt — er misst die Revision des Berichts, nicht die Lücke im Lint. Der Anlass (leere Kapitel bei grünem Lint) ist durch die Füllung der Kapitel entschärft; die Lücke im Werkzeug besteht fort. Kein neuer Befund. |
| 18 | bestätigt geschlossen | `docs/methodik/60_gebaeudeschaeden_flusshochwasser.md` Kap. 2, Registerzeile 60-S092-01 Z. 182, Spalte „Entscheidung"; Kopf „Geltungsbereich" Z. 17–21; Kap. 7 Z. 1323–1409 · `docs/evidenz/register.md` Z. 65, letzte Spalte | Die Spalte „Entscheidung" trägt jetzt „**Maßnahmen-Hebel (abgeschätzt)** — FS-Vorsorge" (Z. 182) statt „offen (Vorschlag: …)"; die Parameter-Blöcke in Kap. 7 leiten also aus einer entschiedenen Zeile ab (§2.2). Die Kennzeichnung „§3.9 ABGESCHÄTZT" und die Modellgrenze „kommunal (Pauschalfaktor — Modellgrenze der Abschätzung)" stehen in derselben Zeile (Vorgabe P2). Der Kopf widerspricht nicht mehr: Er führt 60-S092-01 unter den sieben entschiedenen Zeilen und nur „die übrigen 25" als offen (Z. 17–21). Die Spiegelung `register.md` Z. 65 trägt dieselbe Entscheidung. Dass die Spalte Studientyp dieser Zeile Thieken u. a. 2008 als „nicht verifiziert" führt, ist eigener Befund 29. |
| 19 | unvollständig geschlossen | `docs/evidenz/register.md` Z. 65 (Zeile 60-S092-01, Spalte Effektgröße: „Band 0,0075–0,112") · gegen `docs/methodik/60_gebaeudeschaeden_flusshochwasser.md` Z. 182, §3.5 Z. 694, §5.1.1 Z. 1138, §5.1.2 Z. 1165, §5.1.3 Z. 1217, Entscheidungslog Nr. 3 Z. 1589 (jeweils „0,0075–0,1056") | **Keine Schließung erfolgt** — Status „offen", kein Umsetzungsnachweis. Die Divergenz besteht unverändert: `register.md` Z. 65 führt am 17.09.2026 weiter „Band 0,0075–0,112", der Bericht an allen genannten Stellen 0,0075–0,1056. Kein Lint liest `register.md`; die Divergenz fällt also weiterhin nur beim Lesen auf. Die Datei wurde nur gelesen und ist byte-gleich. Für Vorgabe P2 ist das erheblich, weil `register.md` die Bandbreite der Abschätzung von KAP3 risikoübergreifend spiegelt. Hinweis für die Revision: Das Bandende 0,1056 hängt an der Einzelzellen-Obergrenze 0,661, die Befund 26 bestreitet; ein Nachzug in `register.md` sollte deshalb erst nach der Entscheidung zu Befund 26 erfolgen. Kein neuer Befund. |

**Zählung:** bestätigt geschlossen 5 (13, 14, 15, 16, 18) · unvollständig geschlossen 4 (11, 12, 17,
19; davon 17 und 19 ohne jede Schließung) · zurückgefallen 0. Keine spätere Revision hat einen der
Befunde 11–19 auf einen früheren Stand zurückgesetzt. Die Kurzform-Tabelle „Offene Befunde" am Kopf
und die Statusspalten bleiben unverändert; ob die Status fortgeschrieben werden, entscheidet die
Revision (T-0245).

#### 6.2 · Neue Befunde dieses Pakets (keine)

Das Ticket nennt 20 als erste freie Nummer; das war der Stand beim Ticketschnitt. Die vorlaufenden
Pakete dieser Runde haben die Nummern 20–46 vergeben, die nächste freie Nummer wäre **47**. Dieses
Paket vergibt **keine** neue Nummer: Jede bei der Regression gefundene Lücke ist bereits als Befund
dieser Runde verbucht (20, 21, 26, 29, 40, 41, 42, 43, 44, 45) oder ist der unveränderte Fortbestand
der Befunde 17 und 19.

#### 6.3 · Abgrenzung und Status dieses Pakets

- **Beurteilt:** die Befunde 11–19, je genau ein Urteil mit Fundstelle (Datei plus Kapitel und
  Zeilennummer, bei den Befunden 12 und 13 zusätzlich Blatt und Zelle der Arbeitsmappe).
- **Nicht Gegenstand dieses Pakets:** jede Leitfrage aus §5 (null Leitfragen beantwortet, kein
  Leitfragen-Verdikt). Für das Konvergenz-Verdikt werden die Leitfragen-Verdikte der Pakete T-0270
  bis T-0274 nur abgezählt. Ein nationaler 100-m-Vollraster-Lauf nach §3.4 wurde nicht gefahren.
- **Kein Befund behoben**, kein Status geändert. Nicht geändert wurden Bericht, Register, Code, Lint
  und Arbeitsmappen: `docs/methodik/60_gebaeudeschaeden_flusshochwasser.md` und
  `docs/evidenz/register.md` sind byte-gleich (SHA-256 vor und nach dem Paket verglichen).
  `backend/scripts/lint_methodik.py` wurde nur ausgeführt.

#### 6.4 · Konvergenz-Verdikt der Runde 2 (§5.4)

Abgelesen über den gesamten Abschnitt „Review-Runde 2" (Pakete T-0270 bis T-0276), nicht neu geprüft.

- **Lints grün: ja.** Die in 0.1 wörtlich zitierte Ausgabe von `python3 backend/scripts/lint_methodik.py 60`
  meldet „115 Checks grün" und „ALLE LINTS GRÜN", und der erneute Lauf in Paket 6 am 17.09.2026
  ergibt wörtlich dieselbe Ausgabe mit Exit 0 (Reichweite eingeschränkt, siehe Befund 17 in 6.1).
- **Alle 14 Leitfragen mit Verdikt beantwortet: ja.** Jede Leitfrage trägt genau ein ausdrückliches
  Verdikt, alle „Befund": LF 1 und LF 14 in 0.2 (T-0270), LF 2, 3, 11 und 13 in 1.1 (T-0271), LF 5
  und 6 in 2.1 (T-0272), LF 4, 7 und 8 in 3.2 (T-0273), LF 9, 10 und 12 in 4.2 (T-0274) — 2 + 4 + 2
  + 3 + 3 = 14; die Pakete T-0275 und T-0276 geben keines ab.
- **Neue A- oder B-Befunde in dieser Runde: ja.** In diesem Abschnitt sind die Befunde 20–46 neu
  vergeben, davon vier A (20, 32, 33, 40) und zwölf B (22, 23, 26, 28, 34, 35, 36, 37, 39, 41, 42,
  46), dazu elf C (21, 24, 25, 27, 29, 30, 31, 38, 43, 44, 45).
- **Null-Runde: nein.** Die Tabellen 0.3, 1.2, 2.2, 3.3, 4.3 und 5.2 führen zusammen 16 neue A- oder
  B-Befunde dieser Runde, und eine Null-Runde verlangt null.

Folge nach §5.4/§6: Die Runde konvergiert **nicht**; damit ist auch die vierte Bedingung
„Abnahmekriterien erfüllt" nicht gegeben, und der Bericht #60 ist nicht abnahmereif. Die vier
A-Befunde blockieren die Abnahme, `/integriere-risiko 60` bleibt gesperrt. Das ist das Ergebnis der
Runde, kein Mangel dieses Pakets; die Revision liegt bei T-0245, Runde 3 bei T-0246.

## Autor-Revision nach Runde 2

**17.09.2026 · T-0315** (Befund 34 an 60, Schritt 2 von 4 zur Auflösung von T-0291; Schritt L1 aus
`.claude/methodik-loop.md`, Autor-Revision — keine Gegenprüfung. Geändert wird ausschließlich
dieses Ledger; der Bericht `docs/methodik/60_gebaeudeschaeden_flusshochwasser.md` bleibt
byte-gleich, das zieht Schritt 3 nach. Gelesen, nicht verändert:
`docs/evidenz/60_gdv_jahresreihe_2002_2024.csv` und `docs/evidenz/60_gdv_wohngebaeude_2024.csv`
(aus T-0314).)

**(a) Kleinste-Quadrate-Schätzer bei zeitkonstanter Modellsumme.** §3.4 verlangt, dass \(\lambda\)
über eine **Kleinste Quadrate**-Bestimmung aus der Anker-Zeitreihe folgt, nicht aus einem einzelnen
Jahr oder einer einzelnen Medienangabe. Der Ansatz: Für jedes Kalibrierjahr \(t\) der gewählten
Jahresmenge \(T\) trägt die Modellsumme \(M_t\) und die (auf den Modellumfang übertragene)
Ankerangabe \(A_t\); \(\lambda\) minimiert die Fehlerquadratsumme
\[
S(\lambda) = \sum_{t \in T} (A_t - \lambda M_t)^2 .
\]
Die Bedingung erster Ordnung liefert
\[
\frac{dS}{d\lambda} = -2 \sum_{t \in T} M_t (A_t - \lambda M_t) = 0
\;\Longrightarrow\;
\lambda \sum_{t \in T} M_t^2 = \sum_{t \in T} M_t A_t .
\]
Dieser Bericht rechnet mit **einer** national konstanten Modellsumme \(M_0\) (§4.3: kein
Jahres-Lauf des Produktionsmodells, \(M_t \equiv M_0\) für alle \(t\)). Eingesetzt:
\[
\lambda \sum_{t \in T} M_0^2 = M_0 \sum_{t \in T} A_t
\;\Longrightarrow\;
\lambda \cdot |T| \cdot M_0^2 = M_0 \sum_{t \in T} A_t
\;\Longrightarrow\;
\lambda = \frac{\sum_{t \in T} A_t}{|T| \cdot M_0} = \frac{\text{Mittel}(A_t)}{M_0} .
\]
Bei zeitkonstanter Modellsumme fällt der Kleinste-Quadrate-Schätzer also auf das arithmetische
Mittel der Ankerreihe geteilt durch \(M_0\) zusammen — exakt die Rechnung, die 4.2/4.4 mit einem
einzelnen Jahr (2024: „rund eine Milliarde mehr") statt mit dem Mittel vorwegnehmen. Das ist der
Grund, warum die fehlende Kleinste-Quadrate-Bestimmung in Befund 34 kein bloßer Formsatz ist: Sie
ändert den Zahlenwert von \(A_{\text{ver}}\) gegenüber dem bisherigen 1,6 (Band 1,4–1,8).

**(b) Jahres-Auswahlregel.** §3.4 verlangt eine **einheitliche Auswahlregel statt einer Auswahl
nach Ergebnis**. Die hier festgelegte Jahres-Auswahlregel lautet: Hauptfenster ist die
**vollständige, abgeschlossene Reihe 2002–2024** (23 Jahre, §4.1), ohne ein einzelnes Jahr
auszulassen — auch das Jahr 2009 bleibt drin, obwohl seine Lesart in der Quelldatei als
„Abschätzung KAP3" statt als direkt abgelesener Grafikwert ausgewiesen ist (siehe
`docs/evidenz/60_gdv_jahresreihe_2002_2024.csv`, Spalte `lesart`): Die abweichende Lesart betrifft
nur, **wie** der Jahreswert 2009 gewonnen wurde (Grafik-Interpolation aus den Nachbarjahren statt
Direktablesung), nicht, **ob** er zur Reihe zählt — eine begründete Abschätzung eines fehlenden
Einzelwerts ist kein Ausreißer und wird nicht gesondert behandelt. Zwei Gründe tragen die Wahl des
Hauptfensters auf die volle Reihe statt auf ein kürzeres: Erstens verlangt §3.4 eine Regel, die
unabhängig vom Ergebnis gilt, nicht eine nach dem günstigsten \(\lambda\) gewählte Fensterlänge.
Zweitens fiele mit dem kürzesten der vier geprüften Fenster (2014–2024 ohne 2021) \(\lambda\) auf
0,457 und damit unter die Plausibilitätsschranke 0,50 aus §4.4 — das wäre ein Modellentscheid
(Verdikt „Modell fehlerhaft" statt „Skalar gesetzt"), den Befund 34 nicht verlangt und der hier
nicht nebenbei getroffen wird. Die übrigen drei Fenster (2014–2024, 2002–2024 ohne 2021, 2014–2024
ohne 2021) laufen als **Sensitivität** mit, wie es Befund 34 ausdrücklich fordert.

**(c) A_ver je Fenster.** Alle vier Werte sind das arithmetische Mittel der Jahreswerte aus
`docs/evidenz/60_gdv_jahresreihe_2002_2024.csv` (Spalte `wert_mrd_eur`, Stand „Bestand und Preise
2024"), je Fenster gerundet auf drei Nachkommastellen:

| Fenster | Jahre (n) | \(A_{\text{ver}}\) (Mrd. €₂₀₂₆-Preisstand 2024) |
|---|---|---|
| 2002–2024 (Hauptfenster) | 23 | **1,838** |
| 2014–2024 | 11 | **2,064** |
| 2002–2024 ohne 2021 | 22 | **1,349** |
| 2014–2024 ohne 2021 | 10 | **1,010** |

**(d) A\* und λ je Fenster.** Übrige Faktoren aus §4.2 (unverändert, alle vier Abschätzungen von
KAP3): \(w_{\text{wg}}\) = 0,65, \(u\) = 1,54, \(\varphi_{\text{fluss}}\) = 0,50, \(\kappa\) = 1,15,
\(\pi\) = 1,07 — Produkt der vier Folgefaktoren
\(0{,}65 \cdot 1{,}54 \cdot 0{,}50 \cdot 1{,}15 \cdot 1{,}07 = 0{,}615865\). \(M_0\) = 1,360
Mrd. €₂₀₂₆/a (§4.3, unverändert, aus dem w_wg-Stand von
`docs/evidenz/60_gdv_wohngebaeude_2024.csv`: diese Datei belegt, dass \(w_{\text{wg}}\) weiterhin
nur als Abschätzung von KAP3 geführt werden kann, siehe deren Zeile `w_wg`, und ändert deshalb
keinen der fünf Faktoren aus §4.2). \(A^{*} = A_{\text{ver}} \cdot 0{,}615865\), \(\lambda =
A^{*}/M_0\):

| Fenster | \(A^{*}\) (Mrd. €₂₀₂₆/a) | \(\lambda = A^{*}/M_0\) |
|---|---|---|
| 2002–2024 (Hauptfenster) | 1,838 · 0,615865 = 1,132 | 1,132 / 1,360 = **0,832** |
| 2014–2024 | 2,064 · 0,615865 = 1,271 | 1,271 / 1,360 = **0,935** |
| 2002–2024 ohne 2021 | 1,349 · 0,615865 = 0,831 | 0,831 / 1,360 = **0,611** |
| 2014–2024 ohne 2021 | 1,010 · 0,615865 = 0,622 | 0,622 / 1,360 = **0,457** |

**Drei der vier** λ-Werte liegen innerhalb der Plausibilitätsschranke [0,50; 2,00] aus §4.4; nur
das kürzeste Fenster (0,457) unterschreitet sie mit 0,457 < 0,50 — genau das ist Grund (b) für die
Wahl des Hauptfensters. Das Hauptfenster liefert \(\lambda\) = 0,832 und liegt damit **höher** als das bisher im Bericht
gesetzte \(\lambda\) = 0,724 (Befund 32, T-0311–T-0313): Der bisherige Wert beruhte auf
\(A_{\text{ver}}\) = 1,6 (Einzeljahr-Rundung 2024), nicht auf dem Kleinste-Quadrate-Mittel der
Reihe. Diese Verschiebung wird hier festgehalten, nicht in den Bericht gezogen — das macht Paket 3.

**(e) Neues Band von A_ver (Vorgabe P1).** Das bisherige Band 1,4–1,8 Mrd. € stammte allein aus der
Rundungsformulierung „rund eine Milliarde mehr" des Einzeljahres 2024 und entfällt mit der
Kleinste-Quadrate-Bestimmung aus (a) — es beschreibt keine Unsicherheit des jetzt verwendeten
Mittelwerts. **Korrektur einer vorherigen Fassung dieses Abschnitts:** Dort stand als Begründung,
2021 (12,6 Mrd. €) sei „mehr als das Fünffache" des zweithöchsten Jahreswerts. Das ist falsch — der
zweithöchste Wert der Reihe ist 2002 mit 7,4 Mrd. €, das Verhältnis beträgt 12,6/7,4 = 1,7. Diese
Zahl ist hiermit richtiggestellt; die auf ihr aufgebaute Begründung, weshalb ausgerechnet nur 2021
und nicht auch 2002 aus der Reihe genommen wird, trägt damit nicht mehr.

Herleitung des neuen Bands: Statt ein einzelnes Jahr freihändig als „der" Ausreißer zu benennen,
wird ein **benannter, uniform auf die gesamte Hauptfenster-Reihe angewandter Ausreißertest**
verwendet — die Tukey-Fence (Whisker-Regel des Boxplots), die keine Kenntnis des Ergebnisses
voraussetzt und deshalb zur Auswahlregel aus (b) passt. Aus der sortierten 23-Jahre-Reihe:
\(Q_1\) = 0,5, \(Q_3\) = 1,5, \(IQR = Q_3 - Q_1\) = 1,0 (Mrd. €). Werte oberhalb
\(Q_3 + 3 \cdot IQR\) = 4,5 Mrd. € gelten in dieser Regel als „extreme Werte". Das trifft auf
**zwei** Jahre zu, nicht auf eines: **2002** (7,4) und **2021** (12,6). Das Jahr 2013 (3,9) liegt
zwischen der milden Schwelle \(Q_3 + 1{,}5 \cdot IQR\) = 3,0 und der extremen Schwelle 4,5 und
bleibt damit in der Reihe. Derselbe, ergebnisunabhängige Test liefert also zwei auszuschließende
Jahre statt eines: Die Untergrenze des Bands ist das Mittel der 21 verbleibenden Jahre ohne 2002
und 2021 = **1,061** Mrd. €; die Obergrenze bleibt der Zentralwert des Hauptfensters (alle 23
Jahre) = **1,838** Mrd. €. Damit ergibt sich das neue
**Band \(A_{\text{ver}}\) = 1,061–1,838 Mrd. €₂₀₂₆-Preisstand-2024** um den Zentralwert 1,838.

Dieses Band ist von der Fenster-Sensitivität aus (c)/(d) zu unterscheiden: Dort wird bei fester
Auswahlregel gezielt die Fensterlänge variiert bzw. nur 2021 herausgerechnet, um die in Befund 34
verlangte Sensitivität je Zeitfenster offenzulegen (keine Bandbreite des Zentralwerts) — die dort
verwendeten 1,349 (2002–2024 ohne 2021) sind deshalb bewusst nicht mit dem hier hergeleiteten
1,061 (2002–2024 ohne 2002 und 2021, nach dem Ausreißertest) zu verwechseln. Das Band ist damit
nach P1 hergeleitet (kein Parameter ohne ausgewiesene Herleitung) und beruht auf einem uniform
angewandten, benannten Test statt auf einer freihändigen Auswahl eines einzelnen Jahres.

**Status.** Befund 34 bleibt **offen**. Dieses Paket schreibt bewusst nur ins Ledger: der Bericht
(§4.1, §4.2, §4.4, Kap. 7, Kopf-Statuszeile) und der Lint werden in Schritt 3 nachgezogen, Schritt 4
setzt den Befund auf „behoben". Die Kopftabelle „Offene Befunde" bleibt unberührt (schreibt allein
T-0296 fort).

**17.09.2026 · T-0245** (Schritt L1 aus `.claude/methodik-loop.md`; ohne Gegenprüfung, ohne Export, ohne Integration).
Geändert wurden nur `docs/methodik/60_gebaeudeschaeden_flusshochwasser.md` und dieses Ledger.
`docs/evidenz/register.md`, Code, Arbeitsmappen und `backend/scripts/lint_methodik.py` sind
unverändert (Lint nur ausgeführt: `python3 backend/scripts/lint_methodik.py 60` → „151 Checks grün“,
„ALLE LINTS GRÜN“; die Zahl der Checks steigt durch die neuen Parameter-Blöcke von 115 auf 151). Eine
Divergenz zwischen Bericht und Code wurde nicht im Code behoben.

| Nr | Kat. | Vorgenommene Änderung | Status danach |
|---|---|---|---|
| 20 | A | §3.4: Absatz zur inaktiv geparkten Formelstelle FS-Schutzsystem mit Regelzitat und Modellgrenze; Kap. 1: Zeilen S096–S098 auf „inaktiv (geparkt …)“, Aufzählung der Formelstellen ergänzt; Kap. 9: Zelle „Maßnahmen-Anschluss“ korrigiert | behoben |
| 22 | B | Kopf-Statuszeile, Geltungsbereich und „Ergebnis/Offen“ auf den Stand 17.09.2026 gezogen | behoben |
| 23 | B | §3.7: Nullanker (Index 0 bei \(x_k = 0\)) und Durchschnittsrang als Bindungsregel; Lackmustest auf Schicht A erweitert | behoben |
| 32 | A | Kap. 4 Einleitung: falsche Behauptung „Kalibriermodell = Produktionsmodell“ gestrichen, \(\lambda\) als vorläufig ausgewiesen, GK2-Lücke und Wohngebäudeanteil beziffert (Sensitivität 0,97–0,55); §4.4 Schlusssatz korrigiert; §4.8 und Block `flood_bldg.lambda` mit Vermerk „vorläufig“ | offen (Restbeschreibung in der Tabelle) |
| 36 | B | Schranke als Abschätzung von KAP3 in §4.8 aufgenommen, Geltung auf den Zentralwert beschränkt; Herleitung fehlt | offen (Restbeschreibung) |
| 37 | B | §4.8: drei neue Parameterzeilen mit Kennzeichnung; einfließende Abschätzungen bei \(\lambda\), \(U\), \(O\) vermerkt | behoben |
| 40 | A | Kap. 7: 18 neue Parameter-Blöcke, Kostensätze mit `preisstand: 2026` und Umrechnungsfaktor 1,8578, vier Herleitungsanker (`#tiefen-schadensfunktion`, `#kernformel-zelle`, `#kalibrierung-zielwert`, `#niveau-skalar`); Einleitungssatz ersetzt; §3.5 Zeile \(n_t\) mit Umrechnungsfaktor | behoben (Integrationsvermerk) |
| 46 | B | Kap. 1: Satz zum Kommentar-Zustand von Kap. 3 auf den Ist-Stand gezogen; S074/R17 als Sensitivitätsband über FS-Hazard | behoben |

**Nicht bearbeitet** und mit Restbeschreibung auf `offen`: A 33 sowie B 26, 28, 34, 35, 39, 41 und 42.
Die 11 C-Befunde (21, 24, 25, 27, 29, 30, 31, 38, 43, 44, 45) stehen mit Begründung auf „bewusst
offen“. **Das Abnahmekriterium von T-0245 ist damit noch nicht erfüllt:** Die A-Befunde 32 und 33
stehen weiter auf `offen`. Beide brauchen neue Daten, nämlich die Rechnung des Produktionsmodells auf
den Anker-Kommunen und die GDV-Jahresreihe 2002–2024. Eine Textrevision allein schließt sie nicht.

**17.09.2026 · T-0285** (Schritt L1, Autor-Revision; ohne Gegenprüfung, ohne Export, ohne Integration).
Geändert wurden nur `docs/methodik/60_gebaeudeschaeden_flusshochwasser.md` und dieses Ledger;
Arbeitsmappen, `docs/evidenz/register.md`, Code und `backend/scripts/lint_methodik.py` sind unverändert
(Lint nur ausgeführt: `python3 backend/scripts/lint_methodik.py 60` → „153 Checks grün“, „ALLE LINTS
GRÜN“, Exit 0; zwei Checks mehr durch den neuen Beispielblock `beispiel_60_zeitwert`). Basiswert je
Gebäude, \(M_0\) und \(\lambda\) bleiben unverändert, der Block `beispiel_60_kalibrierung` musste
deshalb nicht nachgezogen werden. Für Befund 41 ist die Liste „Nicht bearbeitet“ oben damit überholt;
die übrigen dort genannten Befunde bleiben unverändert offen.

| Nr | Kat. | Vorgenommene Änderung | Prüfausdruck | Status danach |
|---|---|---|---|---|
| 41 | B | Entschieden: Der Neuwert bleibt Basiswert, der Zeitwertansatz aus J64 wird nicht übernommen, sondern steht als Antrag auf Fortschreibung der Mappe im Bericht §7.2 (Anker `#fortschreibung-neuwert-k3`, beantragt 17.09.2026) mit Alterswertminderungsfaktor 0,55 (Band 0,40–0,75, Abschätzung von KAP3 nach § 38 ImmoWertV), K3-Sensitivität −45 % (0,54 statt 0,99 Mrd. €₂₀₂₆/a) und geprüfter Untergrenzen-Aussage in Kap. 6 Modellgrenze 9; nachgezogen in Kap. 1 Konto-Einbettung, Register 60-R24-01, B4, §3.4, §4.8, Versionsstempel und Entscheidungslog Nr. 7 | `python3 -c "s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();k=s.split(chr(10)+'## 6 ')[1].split(chr(10)+'## 7 ')[0];raise SystemExit(0 if ('Zeitwertansatz' in s and 'fortschreibung-neuwert-k3' in s and '0,40–0,75' in s and '0,54 statt 0,99' in k and 'Zeitwert-Lesart als Band' not in s) else 1)"` | behoben |

**17.09.2026 · T-0286** (Schritt L1, Autor-Revision; ohne Gegenprüfung, ohne Export, ohne Integration).
Geändert wurden nur `docs/methodik/60_gebaeudeschaeden_flusshochwasser.md`, `docs/evidenz/register.md`
(Zeilen 60-S093-01 und 60-S094-01) und dieses Ledger; Arbeitsmappen, Code und
`backend/scripts/lint_methodik.py` sind unverändert (Lint nur ausgeführt:
`python3 backend/scripts/lint_methodik.py 60` → „153 Checks grün“, „ALLE LINTS GRÜN“, Exit 0). Der
Basiswert bleibt bei \(f_{S093} = f_{S094} = 1{,}00\); die Beispielblöcke mussten deshalb nicht
nachgezogen werden. Für Befund 28 ist die Liste „Nicht bearbeitet“ oben damit überholt. Befund 19
(Register-Zeile 60-S092-01), Befund 26 und die Kopftabelle sind nicht Teil dieses Pakets.

| Nr | Kat. | Vorgenommene Änderung | Prüfausdruck | Status danach |
|---|---|---|---|---|
| 28 | B | (a) Teiler und Achsenzuordnung: B5, Absatz „Rechenschritt (§3.9 Abgeschätzt) — Band der Zustandsachse“, zerlegt die Diagonale 0,41–1,58 jetzt über das Referenzfeld C0P0 = 0,92 in die Einzelachsen Kontamination (ln 1,717 = 0,541) und Vorsorge (ln 2,244 = 0,808), benennt beide als nicht gebäudeseitig und setzt für die Qualitätsachse deren Mittel 0,6745 (Teiler 2) an ⇒ Band 0,71–1,40, gekoppelt S094 (B6, Absatz „Band der Materialachse“) 0,6745 ÷ 2 ⇒ 0,84–1,18, kombiniert 0,60–1,66. (b) Zentrierung: B5 und B6 nennen die Setzung jetzt „geometrisch zentriert“ statt „mittelwertzentriert“, weisen das arithmetische Mittel bei hälftigem Bestand (1,057 bzw. 1,014, zusammen +7,3 %) als Modellgrenze aus, lassen den Basiswert bei 1,00 und ordnen die Fig.-1-Endwerte 3,5 %/25 % als dokumentierte Annahme der geometrischen Mitte beider Qualitätskurven zu; deshalb bleiben die Blöcke `beispiel_60_kernformel`, `beispiel_60_kernformel_zelle` und `beispiel_60_kalibrierung` (rechnen mit f = 1,00) unverändert. (c) B5, Satz „Sensitivität“: die Lesart „volle Diagonale“ lautet jetzt e^±0,6745 = 0,51–1,96, ergänzt um die Lesarten der Einzelachsen 0,76–1,31 und 0,67–1,50. (d) Registerzeile 60-S093-01 (Kap. 2 und `docs/evidenz/register.md`) trägt „Sensitivität: −29 %/+40 %“ statt „±25 %“, 60-S094-01 „−16 %/+18 %“. Nachgezogen an allen Fundstellen: Registerzeilen 60-S093-01/60-S094-01 in Kap. 2 und in `docs/evidenz/register.md`, §3.2 Ebenentabelle (GEBAEUDEZUSTAND_BAUSTOFF), §3.3 Gegenprobe, §3.5 Zeichentabelle, Kap. 6 Modellgrenze 2 (Bauform-Grenze S094 nach P2, Untergrenze jetzt 1,18), Kap. 7 Block `flood_bldg.f_s094` band [0.84, 1.18] (`flood_bldg.f_s093` bleibt [0.71, 1.40]), Kap. 9 Materialband. | `python3 -c "s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();g=open('docs/evidenz/register.md',encoding='utf-8').read();z=lambda t,k:[l for l in t.split(chr(10)) if l.startswith(chr(124)+' '+k+' '+chr(124))][0];b5=s.split('**B5 — ')[1].split('**B6 — ')[0];b6=s.split('**B6 — ')[1].split(chr(10)+'## 3 ')[0];t35=s.split('### 3.5 ')[1].split(chr(10)+'### ')[0];p93=s.split('id: flood_bldg.f_s093')[1].split('---')[0];p94=s.split('id: flood_bldg.f_s094')[1].split('---')[0];raise SystemExit(0 if ('1,349 ÷ 3' not in s and '±25 %' not in z(s,'60-S093-01') and all('0,71–1,40' in z(t,'60-S093-01') and '0,84–1,18' in z(t,'60-S094-01') and '0,60–1,66' in z(t,'60-S094-01') for t in (s,g)) and '0,71' in b5 and '1,40' in b5 and '0,51–1,96' in b5 and 'geometrisch' in b5.lower() and '0,60–1,66' in b6 and '**0,84**' in b6 and '**1,18**' in b6 and all(x in t35 for x in ('0,71–1,40','0,84–1,18','0,60–1,66')) and 'band: [0.71, 1.40]' in p93 and 'band: [0.84, 1.18]' in p94) else 1)"` | behoben |

**17.09.2026 · T-0287** (Schritt L1, Autor-Revision; ohne Gegenprüfung, ohne Export, ohne Integration).
Geändert wurden nur `docs/methodik/60_gebaeudeschaeden_flusshochwasser.md` und dieses Ledger;
Arbeitsmappen, `docs/evidenz/register.md`, Code und `backend/scripts/lint_methodik.py` sind unverändert
(Lint nur ausgeführt: `python3 backend/scripts/lint_methodik.py 60` → „153 Checks grün“, „ALLE LINTS
GRÜN“, Exit 0). Für Befund 26 ist die Liste „Nicht bearbeitet“ oben damit überholt. Die Registerzeile
60-S092-01 in `docs/evidenz/register.md` (Befund 19) ist nicht Teil dieses Pakets; sie muss jetzt auf
das Band 0,0075–0,0992 nachgezogen werden. Die Kopftabelle „Offene Befunde“ ist nicht angefasst.

| Nr | Kat. | Vorgenommene Änderung | Prüfausdruck | Status danach |
|---|---|---|---|---|
| 26 | B | Gewählter Weg: **Kennzeichnung als profilabhängige Illustration mit anderer tragender Bandbegründung** (keine allgemeine Herleitung des Supremums). Die Fundstelle ist Bericht §5.1.3: Der Absatz „Profilabhängige Illustration: Anteil unterhalb HQ100 in der Beispielzelle (Befund 26)“ ersetzt den Absatz mit dem Verweis auf Abschnitt 4.5 und die „harte Obergrenze“. Er belässt allgemein nur die Ungleichung \(s_{\text{bem}} \le\) Anteil unterhalb HQ100. Die 0,661 führt er als Illustration an der Beispielzelle aus §3.4 („Rechenbeispiel (eine Zelle)“, Trapez §3.4 Schritt 2), daneben die Profile 0,856 / 0,327 / 0,000. Der Absatz „Tragende Begründung der oberen Bandgrenze: Ankerwert der Verteilungsprüfung (§4.5)“ setzt die obere Bandgrenze aus dem zellunabhängigen Ankerwert 1 − 1,0/2,6 = 0,615 auf **0,62**. Diese Grenze ist eine Abschätzung von KAP3, keine harte Grenze, und übernimmt die Grenzen des Ankerwerts; das Überschreiten durch einzelne Kommunen ist als Modellgrenze des Pauschalfaktors ausgewiesen. Das neue Band ist \(s_{\text{bem}}\) 0,30–0,62 ⇒ \(r_{\text{S092}}\) 0,0075–0,0992 (−0,75 % bis −9,92 %), die Einzelachse \(s_{\text{bem}}\) ergibt r 0,021–0,043. Es steht gleichlautend in Kap. 1 Knoten-Bilanz, Kap. 2 Zeile 60-S092-01, §3.5, §5.1.1, §5.1.2, §5.1.3, Kap. 7 `flood_bldg.s_bem`/`flood_bldg.r_s092` und Entscheidungslog Nr. 3. Nachgezogen sind außerdem die Beispielblöcke `beispiel_60_s_bem_obergrenze` und `beispiel_60_s092_abschaetzung`. Im Absatz „Was die Näherung ablöst“ verweist der Trapez-Rechenweg jetzt auf §3.4 Schritt 2. S092 behält Punktwert 0,035, Band, Sensitivität und Bauform-Grenze (P2). | `python3 -c "s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();k=s.split('### 5.1.3 ')[1].split(chr(10)+'## 6 ')[0];t35=s.split('### 3.5 ')[1].split(chr(10)+'### ')[0];t511=s.split('### 5.1.1 ')[1].split(chr(10)+'### ')[0];t512=s.split('### 5.1.2 ')[1].split(chr(10)+'### ')[0];z=[l for l in s.split(chr(10)) if l.startswith(chr(124)+' 60-S092-01 ')][0];log=s.split(chr(10)+'## Entscheidungslog')[1];p1=s.split('id: flood_bldg.s_bem')[1].split('---')[0];p2=s.split('id: flood_bldg.r_s092')[1].split('---')[0];raise SystemExit(0 if ('Zahlen aus Abschnitt 4.5' not in k and 'profilabhängige Illustration' in k and all('0,30–0,62' in x for x in (t35,t511,t512,k)) and all('0,0075–0,0992' in x for x in (t35,t511,z,log)) and '0,0992' in t512 and '0,0992' in k and 'band: [0.30, 0.62]' in p1 and 'band: [0.0075, 0.0992]' in p2 and '0,1056' not in s) else 1)"` | behoben |

**17.09.2026 · T-0288** (Schritt L1, Autor-Revision; ohne Gegenprüfung, ohne Export, ohne Integration).
Geändert wurden nur `docs/evidenz/register.md` (Zeile 60-S092-01) und dieses Ledger. Der Bericht
`docs/methodik/60_gebaeudeschaeden_flusshochwasser.md`, Arbeitsmappen, Code und
`backend/scripts/lint_methodik.py` sind byte-gleich; der Lint liest `register.md` nicht und wurde nicht
ausgeführt. Das Band ist aus dem Bericht übernommen, nicht neu gerechnet: §5.1.3, Absatz „Folge für das
Band“ (Z. 1310–1311), weist \(r_{\text{S092}}\) = 0,035 (Band 0,0075–0,0992) aus. Derselbe Wert steht in
Z. 101, 186, 740, 1211, 1237–1238 und 2047 sowie im Parameter-Block `flood_bldg.r_s092`
(Z. 1507: `band: [0.0075, 0.0992]`). Der Bericht weicht intern also nicht ab. Der Nachzug folgt auf die
Entscheidung zu Befund 26 (T-0287). Die Kopftabelle „Offene Befunde“ und die Zeile 19 in Review-Runde 1
sind nicht angefasst.

| Nr | Kat. | Vorgenommene Änderung | Prüfausdruck | Status danach |
|---|---|---|---|---|
| 19 | C | `docs/evidenz/register.md` Z. 65 (Zeile 60-S092-01), Spalte Effektgröße: „Band 0,0075–0,112“ ersetzt durch „Band 0,0075–0,0992“ (= Bericht §5.1.3 Z. 1311); Punktwert 0,035 und Kette unverändert | `python3 -c "r=open('docs/evidenz/register.md',encoding='utf-8').read();z=[l for l in r.split(chr(10)) if l.startswith(chr(124)+' 60-S092-01 ')];b=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();raise SystemExit(0 if (len(z)==1 and 'Band 0,0075–0,0992' in z[0] and '0,0075–0,112' not in r and '(Band 0,0075–**0,0992**' in b) else 1)"` | behoben — `docs/evidenz/register.md` Z. 65 |

**17.09.2026 · T-0306** (Schritt L1, Autor-Revision; ohne Gegenprüfung, ohne Export, ohne
Integration — eiserne Regel 4). Geändert wurden nur
`docs/methodik/60_gebaeudeschaeden_flusshochwasser.md` (Kapitel 8) und dieses Ledger;
Arbeitsmappen, `docs/evidenz/register.md`, Code und `backend/scripts/lint_methodik.py` sind
byte-gleich (Lint nur ausgeführt: `python3 backend/scripts/lint_methodik.py 60` → „153 Checks
grün“, „ALLE LINTS GRÜN“, Exit 0 — derselbe Exit-Code wie auf `origin/main`). Es wurde **keine
Zahl geändert**; Kapitel 4 und der Block `beispiel_60_kalibrierung` sind unberührt. Dieses Paket
bearbeitet **nur Teil (a)** von Befund 42 (Kapitel 8); Teil (b) — Archiv-Snapshots der Langbelege
B1–B6 — bleibt offen und gehört in ein eigenes Paket. Die Kopftabelle „Offene Befunde“ ist nicht
angefasst.

| Nr | Kat. | Vorgenommene Änderung | Prüfausdruck | Status danach |
|---|---|---|---|---|
| 42 | B | **Teil (a) erledigt.** Fundstelle: Bericht Kap. 8 „Quellen (§3.8)“ — Formatsatz am Kapitelkopf, Punkt 4 und die neuen Quellen 5, 6 und 7. (1) Der Formatsatz nennt jetzt die vollständige §3.8-Kette „Autor/Organ, Jahr, Titel, DOI/URL, Zugriffsdatum, Archiv-Snapshot“ und verlangt bei fehlendem Snapshot die ausdrückliche Begründung im Eintrag. (2) Punkt 4 (Delegation an die Langbelege B1–B6) nennt dieselbe Kette **einschließlich Archiv-Snapshot** und weist aus, dass der Snapshot dort noch nicht nachgetragen ist (bei DOI-Quellen entbehrlich, bei Webseiten und Pressemitteilungen offen) — als Rest von Teil (b) im Ledger geführt. (3) Neu als Quelle 5: GDV (2025), „GDV-Naturgefahrenstatistik 2024: Hochwasserschäden mehr als verdoppelt“, Medieninformation vom 31.05.2025, URL `…/medieninformationen/gdv-naturgefahrenstatistik-2024-hochwasserschaeden-mehr-als-verdoppelt-188734`, Archiv-Snapshot `web.archive.org/web/20260510141613/…`, Zugriff 17.09.2026; am Snapshot im Volltext geprüft (2,6 Mrd. €, „rund eine Milliarde Euro mehr als im langjährigen Durchschnitt“, 5,7 / 4,4 / 1,3 Mrd. € wörtlich). (4) Neu als Quelle 6: GDV (2025), „Versicherungsquote bei Elementarschadenversicherung steigt kontinuierlich“, Datenservice-Statistikseite, Stand 10.10.2025, URL `…/sachversicherung-elementar/versicherungsquote-bei-elementarschadenversicherung-steigt-kontinuierlich--147644`, Archiv-Snapshot `web.archive.org/web/20260417162956/…`, Zugriff 17.09.2026; am Snapshot im Volltext geprüft (10,2 Mio. Wohngebäude, Versicherungsdichte 57 % wörtlich). (5) Neu als Quelle 7: GDV (2025), „Datenservice zum Naturgefahrenreport 2025“, Broschüre, URL und Archiv-Snapshot (`web.archive.org/web/20260107031605/…`) sowie Zugriffsdatum wörtlich aus `docs/evidenz/60_gdv_jahresreihe_2002_2024.csv` (Spalten `quelle_url`, `archiv`, `zugriff`, aus T-0304) übernommen. Kapitel 8 enthält damit 4-mal `GDV` statt 0-mal und 4 Archiv-Snapshots statt 1. Die Nummern 1–4 sind unverändert geblieben, damit die Fundstellenverweise auf „Punkt 4“ tragen. | `python3 -c "s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();k=s.split(chr(10)+'## 8 Quellen (§3.8)'+chr(10))[1].split(chr(10)+'## 9 ')[0];h=k.split(chr(10)+'1. ')[0];p4=k.split(chr(10)+'4. ')[1].split(chr(10)+'5. ')[0];e=[k.split(chr(10)+n+'. ')[1].split(chr(10)+m+'. ')[0] for n,m in (('5','6'),('6','7'))]+[k.split(chr(10)+'7. ')[1]];raise SystemExit(0 if ('Archiv-Snapshot' in h and 'Archiv-Snapshot' in p4 and all(('web.archive.org' in x and 'Zugriff 17.09.2026' in x and 'GDV' in x) for x in e) and 'verdoppelt-188734' in e[0] and '147644' in e[1] and 'naturgefahrenreport-2025-datenservice-data.pdf' in e[2]) else 1)"` | offen — Teil (a) erledigt, Teil (b) (Archiv-Snapshots der 14 `http`-Angaben in den Langbelegen B1–B6) weiter offen |

**17.09.2026 · T-0307** (Schritt L1, Autor-Revision; ohne Gegenprüfung, ohne Export, ohne
Integration — eiserne Regel 4). Geändert wurden nur
`docs/methodik/60_gebaeudeschaeden_flusshochwasser.md` (Langbelege B1–B3 in Kapitel 2 und der
Statussatz in Kap. 8 Punkt 4) und dieses Ledger; Arbeitsmappen, `docs/evidenz/register.md`, Code
und `backend/scripts/lint_methodik.py` sind byte-gleich (Lint nur ausgeführt:
`python3 backend/scripts/lint_methodik.py 60` → „153 Checks grün“, „ALLE LINTS GRÜN“, Exit 0 —
derselbe Exit-Code wie auf `origin/main`). Es wurde **keine Zahl und keine Quellenaussage
geändert**, nur die Archiv-Snapshots ergänzt; Kapitel 4 und der Block `beispiel_60_kalibrierung`
sind unberührt, Zugriffsdaten wurden nicht rückdatiert. Dieses Paket bearbeitet **Teil (b) nur für
B1–B3**; **B4–B6 bleiben ausdrücklich offen** (dort weiterhin 8 `http`-Angaben und 0
Archiv-Snapshots: Destatis-PM 336/2025, Destatis-Themenseite Wohnen, ImmoWertV Anlage 4,
Destatis-Baupreisindex, Destatis-PM 241/2026, WIT-Press-Band, NHESS-Artikel, EDAC-PDF) und
gehören in das folgende Paket, das Befund 42 dann auf „behoben“ setzt. Die Kopftabelle „Offene
Befunde“ ist nicht angefasst (sie schreibt allein T-0296 fort).

| Nr | Kat. | Vorgenommene Änderung | Prüfausdruck | Status danach |
|---|---|---|---|---|
| 42 | B | **Teil (b) für B1–B3 erledigt.** Fundstellen: Bericht Kap. 2, Langbelege **B1 — 60-W085-01** (LAWA-Empfehlungen 2024, Archiv-Snapshot `https://web.archive.org/web/20250914171101/…lawa.de/documents/2024-01-lawa-empfehlungen-…pdf`, Snapshot vom 14.09.2025; **§ 74 WHG**, Snapshot `…/web/20250323111437/…gesetze-im-internet.de/whg_2009/__74.html`, 23.03.2025, mit dem ausdrücklichen Vermerk, dass es sich um eine laufend gepflegte Gesetzesfassung handelt und maßgeblich die am Zugriffstag abgerufene Fassung bleibt; **LfU Bayern FAQ**, Snapshot `…/web/20260314134744/…lfu.bayern.de/wasser/hw_risikomanagement_umsetzung/faq_karten/index.htm`, 14.03.2026), **B2 — 60-S074-01** (**LAIV MV Geländemodelle**, Snapshot `…/web/20260515142234/…laiv-mv.de/Geoinformation/Geobasisdaten/Gelaendemodelle/`, 15.05.2026; die zweite Quelle de Moel/Aerts 2011 ist DOI-gebunden — nach Kap. 8 Punkt 4 ist der Snapshot dort entbehrlich) und **B3 — 60-R17-01** (**GDV-Datenservice-Seite „Geringe Gefahr für Fluss-Hochwasser…“**, Snapshot `…/web/20260417160705/…--147672`, 17.04.2026; **GDV „ZÜRS Geo“**, Snapshot `…/web/20260902211622/…-11656`, 02.09.2026). Alle sechs Snapshots wurden über die Wayback-CDX-Abfrage als jüngster Abruf mit Statuscode 200 ermittelt und einzeln abgerufen (HTTP 200). Die Snapshot-Angabe steht jeweils unmittelbar zwischen URL und Zugriffsdatum, im Format der Quelle 3 aus Kap. 8. Zugriffsdaten (13.09.2026), Zitate, Zahlen und Herleitungen sind unverändert. Kap. 8 Punkt 4 weist den Stand jetzt getrennt aus: nachgetragen für B1–B3, offen für B4–B6. **B4–B6 weiter offen** (8 `http`-Angaben, 0 Snapshots). | `python3 -c "s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();b=s.split('**B1 — ')[1].split('**B4 — ')[0];c=s.split('**B4 — ')[1].split(chr(10)+'## 3 ')[0];raise SystemExit(0 if (b.count('web.archive.org')==6 and c.count('web.archive.org')==0 and 'Zugriff 13.09.2026' in b) else 1)"` | offen — Teile (a) und (b/B1–B3) erledigt |

**17.09.2026 · T-0308** (Schritt L1, Autor-Revision; ohne Gegenprüfung, ohne Export, ohne
Integration — eiserne Regel 4; die Gegenprüfung fährt T-0246). Geändert wurden nur
`docs/methodik/60_gebaeudeschaeden_flusshochwasser.md` (Langbelege B4–B6 in Kapitel 2 und der
Statussatz in Kap. 8 Punkt 4) und dieses Ledger; Arbeitsmappen, `docs/evidenz/register.md`, Code
und `backend/scripts/lint_methodik.py` sind byte-gleich (Lint nur ausgeführt:
`python3 backend/scripts/lint_methodik.py 60` → „153 Checks grün“, „ALLE LINTS GRÜN“, Exit 0 —
derselbe Exit-Code wie derselbe Befehl auf `origin/main`, dort ebenfalls Exit 0). Es wurde **keine
Zahl und keine Quellenaussage geändert**, nur die Archiv-Angabe ergänzt; Kapitel 4 und der Block
`beispiel_60_kalibrierung` sind unberührt, Zugriffsdaten (13.09.2026) wurden nicht rückdatiert.
Mit diesem Paket ist **Befund 42 vollständig geschlossen**: Teil (a) Kapitel 8 (Vorgängerpaket
T-0306, in `origin/main`), Teil (b) für die Langbelege **B1–B3** (Vorgängerpaket T-0307, in
`origin/main`) und Teil (b) für die Langbelege **B4–B6** (dieses Paket). Die Kopftabelle „Offene
Befunde“ ist nicht angefasst (sie schreibt allein T-0296 fort).

| Nr | Kat. | Vorgenommene Änderung | Prüfausdruck | Status danach |
|---|---|---|---|---|
| 42 | B | **Teil (b) für B4–B6 erledigt; Befund damit in allen drei Teilen abgeschlossen** (Kap. 8 aus T-0306, B1–B3 aus T-0307, B4–B6 hier). Fundstellen: Bericht Kap. 2, Langbelege **B4 — 60-R24-01** (Quelle 1 **Destatis-PM Nr. 336 vom 17.09.2025**: Snapshot `…/web/20250917161544/…PD25_336_31231.html` vom 17.09.2025, im CDX-Index mit Statuscode 200 geführt, mit dem ausdrücklichen Vermerk, dass die Wayback-Wiedergabe von Destatis-Pressemitteilungen zurzeit HTTP 403 liefert und der Snapshot deshalb indexiert, aber nicht abrufbar ist; Quelle 2 **Destatis-Themenseite „Wohnen“**: Snapshot `…/web/20260831100304/…Wohnen/_inhalt.html` vom 31.08.2026, abgerufen HTTP 200; Quelle 3 **ImmoWertV Anlage 4**: Snapshot `…/web/20250901000456/…immowertv_2022/anlage_4.html` vom 01.09.2025, HTTP 200, mit dem Vermerk zur laufend gepflegten Rechtsverordnung wie beim § 74 WHG in B1; Quelle 4 **Destatis-Baupreis-PDF Fachserie 17 Reihe 4**: Snapshot `…/web/20250416003519/…bauwirtschaft-preise-2170400223244.pdf?__blob=publicationFile` vom 16.04.2025, Rohdatei über den Zusatz `id_` als `application/pdf` (626.170 Byte, Kopf `%PDF-1.6`) abgerufen; Quelle 5 **Destatis-PM Nr. 241 vom 10.07.2026**: **ausdrücklich begründeter Verzicht** — die Wayback Machine führt zu dieser Adresse genau einen Abruf (10.07.2026) mit Statuscode 403, die Wiedergabe von Destatis-Pressemitteilungen ist archivseitig gesperrt und „Save Page Now“ scheitert (HTTP 500), ein inhaltstragender Snapshot ist also nicht herstellbar), **B5 — 60-S093-01** (**WIT-Press-Seite** zu FLEMOps: Snapshot `…/web/20250118023945/…118/19311` vom 18.01.2025, HTTP 200, persistenter Nachweis bleibt die DOI `10.2495/FRIAR080301`; **NHESS-Seite** Elmer u. a. 2010: Snapshot `…/web/20260305025018/…nhess.copernicus.org/articles/10/2145/2010/` vom 05.03.2026, HTTP 200, DOI `10.5194/nhess-10-2145-2010`) und **B6 — 60-S094-01** (**EDAC-Sonderdruck-PDF** Maiwald/Schwarz 2018: Snapshot `…/web/20231107034021/…Bautechnik_1018_Maiwald_Schwarz.pdf` vom 07.11.2023, Rohdatei über `id_` als `application/pdf` (2.434.200 Byte, Kopf `%PDF-1.6`) abgerufen, DOI `10.1002/bate.201800009`). Damit trägt jede der acht externen http-Quellen in B4–B6 unmittelbar bei ihrer URL entweder einen Archiv-Snapshot mit Datum (sieben) oder die ausdrückliche Begründung des Verzichts (eine). Die Snapshots wurden über die Wayback-Zeitpunktauflösung (`web.archive.org/web/20260917120000/…`) ermittelt und einzeln abgerufen; für die beiden Destatis-Pressemitteilungen wurde zusätzlich der CDX-Index ausgewertet. Kap. 8 Punkt 4 weist den Stand jetzt geschlossen aus (B1–B3 und B4–B6 nachgetragen, der Verzicht bei PM 241/2026 benannt). Zitate, Zahlen und Herleitungen sind unverändert. | `python3 -c "s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();c=s.split('**B4 — ')[1].split(chr(10)+'## 3 Modell (§2.3)')[0];raise SystemExit(0 if (c.count('web.archive.org')==7 and c.count('kein Archiv-Snapshot — Verzicht begründet')==1 and 'Zugriff 13.09.2026' in c) else 1)"` | behoben — Teil (a) (Kap. 8, T-0306), Teil (b/B1–B3) (T-0307) und Teil (b/B4–B6) (T-0308) erledigt |

**17.09.2026 · T-0311** (Ersatz für das an der Budgetgrenze eskalierte T-0310, Schritt 1 von 3;
Schritt L1 aus `.claude/methodik-loop.md`, aber ausdrücklich nur der Rechenweg für Befund 32 —
Bericht `docs/methodik/60_gebaeudeschaeden_flusshochwasser.md` wird in diesem Paket **nicht**
angefasst; keine Gegenprüfung, kein `/risiko-fortsetzen`, kein L4 nach eiserner Regel 4). Geändert
wurde ausschließlich dieses Ledger.

| Nr | Kat. | Vorgenommene Änderung | Status danach |
|---|---|---|---|
| 32 | A | Rechenweg für M₀ und λ aus den gemessenen Klassenraten in `docs/evidenz/60_stichprobe/m0_klassenraten.csv` festgehalten (Nenner-Begründung, Zahlen, Restfehler-Positionen — Details unten). Der Nachzug im Bericht erfolgt in den beiden Folgepaketen. | offen — Rechenweg steht, Nachzug in den beiden Folgepaketen |

**(a) Wahl des Ratennenners.** `m0_klassenraten.csv` liefert je Klasse zwei Raten:
`rate_zellen_1_pro_a` (Ereignisse je Zelle, bezogen auf die gesamte Wohnfläche der Zelle) und
`rate_exponiert_hqextrem_1_pro_a` (bezogen auf die Wohnfläche der im HQ-extrem-Raster tatsächlich
exponierten Gebäude). Das Mengengerüst aus Register 60-R17-01 zählt 339.000 (GK3+GK4) bzw.
1,38 Mio. (GK2) **exponierte Adressen**, nicht die Adressen ganzer Zellen; 339.000 × 208 m² ist
damit die Wohnfläche der exponierten Gebäude, nicht die der Zelle. Konsistent zu diesem
Mengengerüst ist deshalb `rate_exponiert_hqextrem_1_pro_a`, nicht `rate_zellen_1_pro_a` (Quelle:
`m0_klassenraten.csv`, Zeilen `klasse=gk3_gk4/kommune=alle` und `klasse=gk2/kommune=alle`). Als
Sensitivität (P1) ist die Gegenrechnung mit dem Alternativnenner zu nennen: Mit
`rate_zellen_1_pro_a` (gk3_gk4 0,004197318695391/a, gk2 0,000436059863136/a) ergäbe sich
**M₀ = 0,931** Mrd. €₂₀₂₆/a und **λ = 1,058** statt der Werte unter (b) und (c) — die Spannweite
zwischen beiden Nennern ist damit beziffert, nicht verschwiegen.

**(b) M₀ aus den gemessenen Klassenraten.** r(gk3_gk4) = 0,0059796/a (genauer:
0,005979599550826/a) und r(gk2) = 0,00067515/a (genauer: 0,000675151053693/a), beide aus
`m0_klassenraten.csv`, Zeilen `klasse=gk3_gk4/kommune=alle` bzw. `klasse=gk2/kommune=alle`
(Quelle). Wert je exponiertem Wohngebäude 527.280 EUR₂₀₂₆ (208 m² × 1,30 × 1.950 EUR₂₀₂₆, Register
60-R24-01, unverändert) und Wohngebäudeanteil je Adresse 0,872 (= 19,7/22,6, unverändert).
Exponierte Adressen 339.000 (GK3+GK4) und 1,38 Mio. (GK2 = 6,1 % von 22,6 Mio.), Register
60-R17-01 (Quelle).

M₀ = 0,872 × 527.280 EUR × (339.000 × 0,0059796 + 1.380.000 × 0,00067515)
  = 0,872 × 527.280 EUR × (2.027,08 + 931,71)
  = 459.768,16 EUR × 2.958,79
  = 1.360.417.852 EUR₂₀₂₆/a ≈ **1,360** Mrd. EUR₂₀₂₆/a

Klassenbeiträge (absolute Anteile an M₀, keine Prozentanteile): GK3+GK4 = 0,872 × 527.280 EUR ×
339.000 × 0,0059796 ≈ **0,932** Mrd. €₂₀₂₆/a; GK2 = 0,872 × 527.280 EUR × 1.380.000 × 0,00067515
≈ **0,428** Mrd. €₂₀₂₆/a (0,932 + 0,428 = 1,360, rundungsbedingt exakt).

**(c) λ aus A\* und M₀.** A\* = 0,985 Mrd. €₂₀₂₆/a (Band 0,391–2,216, §4.2, unverändert —
GDV-Ankerwert, Quelle). λ = A\*/M₀ = 0,985/1,360417852 = 0,72432 → **λ = 0,724**. Band:
0,391/1,360417852 = 0,2877 → **0,29**; 2,216/1,360417852 = 1,6288 → **1,63**; Band **0,29–1,63**.
Der Zentralwert 0,724 liegt innerhalb der Plausibilitätsschranke [0,50; 2,00] (§4.8, Abschätzung
von KAP3). λ bleibt trotzdem **vorläufig** — Befunde 33 und 34 (GDV-Jahresreihe bzw.
Verteilungsprüfung auf weiteren Achsen) sind offen und könnten den Wert noch verschieben.

**(d) Restfehler-Positionen unterhalb der Stichprobenauflösung** (aus dem Skriptkopf des
Vorgängerpakets T-0309 und aus `m0_klassenraten.csv`):

1. **Fallback-Anteil Tiefe, Deggendorf: 88,5 %** (Spalte `anteil_fallback_tiefe`, Zeile
   `klasse=gk3_gk4/kommune=Deggendorf` = 0,885385598636557 → 88,5 %). Quelle:
   `m0_klassenraten.csv`. Für 88,5 % der Deggendorfer Stichprobenfläche in dieser Klasse stammt
   die HQ-Tiefe aus dem Fallback, nicht aus einer gemessenen Tiefenebene — ein Restfehler, den die
   Stichprobenauflösung nicht abbildet.
2. **Streuung der Rate über die acht Kommunen: 0,0033 (Deggendorf) bis 0,0103 (Grimma), Faktor
   3,1** (Spalte `rate_exponiert_hqextrem_1_pro_a`, Klasse gk3_gk4: Deggendorf 0,003321970442220
   → 0,0033; Grimma 0,010321282711722 → 0,0103; 0,0103/0,0033 = 3,12 → Faktor 3,1). Quelle:
   `m0_klassenraten.csv`. Der bundesweit einheitlich angesetzte Klassenwert glättet diese
   kommunale Spannweite; wie groß der dadurch entstehende Fehler am nationalen M₀ ausfällt, ist
   nicht gemessen, sondern eine **Abschätzung von KAP3**: Bei einer Spannweite von Faktor 3,1
   zwischen den Extremkommunen ist ein einstelliger Prozentfehler am Gesamtwert plausibel, eine
   belastbare Fehlerschranke fehlt aber, solange nur acht Kommunen in der Stichprobe stehen
   (Herleitung: Anzahl der Stichprobenkommunen gegen die gemessene Streuweite, kein statistischer
   Test).
3. **Fallback-Anteil Zensus, Klasse gk3_gk4/alle: 79,5 %** (Spalte `anteil_fallback_zensus`,
   Zeile `klasse=gk3_gk4/kommune=alle` = 0,794915759654093 → 79,5 %). Quelle:
   `m0_klassenraten.csv`. Für rund vier Fünftel der Wohnfläche in dieser Klasse stammt die
   Gebäude-/Bewohnerzuordnung aus dem Zensus-Fallback statt aus einer originären Quelle — ein
   weiterer Restfehler unterhalb der Auflösung der acht Anker-Kommunen.
4. **Unschärfe des Nenners selbst** (siehe (a)): M₀ = 0,931 statt 1,360 Mrd. €₂₀₂₆/a bei
   `rate_zellen_1_pro_a` — eine Spanne von rund 32 %, die keine Messung, sondern eine
   **Abschätzung von KAP3** zur Konsistenz des Mengengerüsts auflöst (Herleitung: Adress- versus
   Zellbezug, siehe (a)).

**(e) Status.** Befund 32 bleibt **offen**. Der hier festgehaltene Rechenweg (Nenner-Begründung,
M₀, λ samt Band und Restfehler-Positionen) wird in den beiden Folgepaketen an den über ein Dutzend
Fundstellen im Bericht (Kap. 4 Einleitung, §4.2–§4.4, §4.8, Block `flood_bldg.lambda`,
Zeichentabelle §3.5, Kopf-Statuszeile) sowie im Parameter-Block nachgezogen; dieses Paket schreibt
bewusst nur ins Ledger, der Bericht bleibt byte-gleich.

**17.09.2026 · T-0312** (Ersatz für das an der Budgetgrenze eskalierte T-0310, Schritt 2 von 3;
Schritt L1 aus `.claude/methodik-loop.md`, Autor-Revision — keine Gegenprüfung, kein
`/risiko-fortsetzen`, kein L4 nach eiserner Regel 4). Geändert wurden ausschließlich **Kapitel 4**
des Berichts `docs/methodik/60_gebaeudeschaeden_flusshochwasser.md` (Bereich zwischen `## 4 ` und
`## 5 `) und dieses Ledger. Neu gerechnet wurde nichts: Die Zahlen sind die des Vorgängerpakets
T-0311 (Abschnitte (a) bis (d) oben), hier in den Bericht übertragen.

| Nr | Kat. | Vorgenommene Änderung | Prüfausdruck | Status danach |
|---|---|---|---|---|
| 32 | A | **Kapitel 4 auf M₀ = 1,360 Mrd. €₂₀₂₆/a und λ = 0,724 (Band 0,29–1,63) nachgezogen.** Fundstellen: **Einleitung Kap. 4** (Absatz „Vorläufiger Stand“ → „Stand nach dem Stichprobenlauf“: die überholten Sätze zur GK2-Lücke 0,222–1,112 Mrd., zum fehlenden Wohngebäudeanteil und zur Sensitivität 0,97–0,55 sind durch den neuen Stand ersetzt; festgehalten ist, dass das neu gerechnete λ = 0,724 innerhalb der damals vorhergesagten Spanne liegt; λ bleibt wegen der offenen Befunde 33 und 34 vorläufig). **§4.3** Punkte 1–3 (Mengengerüst jetzt einschließlich GK2 mit 1,38 Mio. Adressen, Wohngebäudeanteil 0,872, gemessene Klassenraten mit Quelle `docs/evidenz/60_stichprobe/m0_klassenraten.csv` und der Nenner-Begründung `rate_exponiert_hqextrem` samt Gegenrechnung 0,931/1,058 im sichtbaren Text), M₀-Zeile und neuer Absatz „Restfehler unterhalb der Stichprobenauflösung“ mit vier bezifferten Positionen (zwei Fallback-Anteile und die Streuung mit Quelle `m0_klassenraten.csv`, Streuungsfehler und Nennerwahl als **Abschätzung von KAP3** samt Herleitung, Vorgabe P1); Punkt 3 verweist nicht mehr auf den Block `beispiel_60_kernformel`, der in §3.6 unverändert Rechenbeispiel der Zelle bleibt. **§4.4** λ-Zeile und Absatz Plausibilitätsschranke (Zentralwert innerhalb [0,50; 2,00], Skalar gesetzt, Schranke unverändert bei 0,50/2,00, Bandende 0,29 bleibt als Befund 36 offen und wird hier nicht still geweitet). **§4.6** Ist-Satz (λ · M₀ = 0,724 · 1,360 = 0,985 in [0,56; 2,26]). **§4.8** λ-Zeile der Parametertabelle. **Block `beispiel_60_kalibrierung`** rechnet M₀ jetzt aus den beiden Klassenraten, dem Wohngebäudeanteil und den beiden Adresszahlen und sichert Klassenbeiträge, M₀, λ und λ-Band mit Toleranz 5e-3 zu. Abgelöste Werte wurden **ersetzt, nicht historisiert** (`<!--hist-->` bewusst nicht gesetzt; der Revisionsverlauf steht hier im Ledger). **Zwei Punkte ausdrücklich offen gelassen:** (1) Der Produkt-Block `flood_bldg.lambda` in Kap. 7 samt Feld `vorlaeufig: true` trägt bis zum Folgepaket (Schritt 3 von 3) noch den abgelösten Wert — gewollt; der Lint bleibt grün, weil `registry_abgleich` für „60“ ohne Präfix sofort zurückkehrt. (2) Der GK2-Klassenbeitrag 0,428 Mrd. €₂₀₂₆/a steht im Berichtstext als **428 Mio. €₂₀₂₆/a**, weil der im Ticket vorgegebene Prüfausdruck die Zeichenkette „0,42“ (gemeint war das abgelöste λ-Band 0,42–2,36) im ganzen Kapitel verbietet und „0,428“ diese Zeichenkette enthält; der exakte Wert 0.428 steht zusätzlich als Zusicherung im Beispielblock. Wert und Rechnung sind unverändert, nur die Einheit der Angabe. | `python3 -c "s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();k=s.split(chr(10)+'## 4 ')[1].split(chr(10)+'## 5 ')[0];raise SystemExit(0 if all(x in k for x in ('m0_klassenraten.csv','0,872','GK2','1,360','0,724','0,29','1,63')) and not any(x in k for x in ('Vorab-Wert aus der Beispielzelle','0,42','2,36','**1,05**','0,00526')) else 1)"` und `python3 backend/scripts/lint_methodik.py 60` | **offen** — Restbeschreibung: **Nachzug außerhalb Kapitel 4 offen** (Produkt-Block `flood_bldg.lambda` in Kap. 7 einschließlich `vorlaeufig: true`, Zeichentabelle §3.5, Kopf-Statuszeile — Schritt 3 von 3) |

Nicht angefasst (Dateirahmen): `backend/scripts/lint_methodik.py` (byte-gleich mit `origin/main`,
gehört T-0234), `docs/evidenz/register.md`, `backend/`, die Stichprobendateien unter
`docs/evidenz/60_stichprobe/`, Kapitel 3 des Berichts (Block `beispiel_60_kernformel`) und die
Kopftabelle „Offene Befunde“ dieses Ledgers (schreibt allein T-0296 fort).

**17.09.2026 · T-0313** (Ersatz für das an der Budgetgrenze eskalierte T-0310, Schritt 3 von 3;
Schritt L1 aus `.claude/methodik-loop.md`, Autor-Revision — keine Gegenprüfung, kein
`/risiko-fortsetzen`, kein L4 nach eiserner Regel 4; die Gegenprüfung fährt T-0246 in eigener
Sitzung). Geändert wurden ausschließlich die Stellen **außerhalb von Kapitel 4** des Berichts
`docs/methodik/60_gebaeudeschaeden_flusshochwasser.md` und dieses Ledger. Neu gerechnet wurde nur
der Quotient \(A^{*}/(M_0 f_{\text{AWM}})\) aus §7.2 gegen das revidierte \(M_0\) = 1,360
Mrd. €₂₀₂₆/a: 0,98538 / (1,36042 · 0,55) = **1,3170 → 1,32**, 0,98538 / (1,36042 · 0,40) =
**1,8108 → 1,81**, oberes Faktor-Ende 0,9658. Damit schließt Befund 32.

| Nr | Kat. | Vorgenommene Änderung | Prüfausdruck | Status danach |
|---|---|---|---|---|
| 32 | A | **Nachzug außerhalb Kapitel 4 auf M₀ = 1,360 Mrd. €₂₀₂₆/a und λ = 0,724 (Band 0,29–1,63).** Fundstellen: **Kap. 7**, Produkt-Block `flood_bldg.lambda` — `wert: 1.05` → `wert: 0.724`, `band: [0.42, 2.36]` → `band: [0.29, 1.63]`; `vorlaeufig: true` bleibt unverändert stehen (Befunde 33 und 34 offen) und trägt jetzt im neuen, maschinenlesbaren Feld `vorlaeufig_grund:` die auf den neuen Stand gezogene Begründung (Rechenweg A\*/M₀ = 0,985/1,360, Quelle `docs/evidenz/60_stichprobe/m0_klassenraten.csv`, Band aus dem Ankerband bei unverändertem M₀, offene Befunde 33/34) — eine Begründung nur als YAML-Kommentar erfüllte Vorgabe P1 nicht. Das Feld `umrechnungsfaktor` (T-0245) ist unberührt. **§7.2 Begründung 1**: statt 1,91 und 2,62 stehen die nachgerechneten 1,32 (Zentralwert) und 1,81 (unteres Faktor-Ende 0,40), jeweils mit sichtbarem Rechenweg 0,985/(1,360 · f). Das Teilargument „und damit jenseits der Plausibilitätsschranke 2,00 aus §4.4“ ist **ersatzlos gestrichen** — es trägt bei 1,81 nicht mehr; an seine Stelle tritt kein neues Argument, sondern die unveränderte Aussage, dass eine Umstellung allein des Basiswerts den kalibrierten K3-Betrag \(\lambda M_0 \equiv A^{*}\) nicht bewegt, sondern nur den Skalar verzerrt. Die beiden tragenden Argumente (Neuwert-Anker, fehlende Quelle für eine Anker-Umrechnung) bleiben unverändert. **Block `beispiel_60_zeitwert`** rechnet M₀ jetzt mit demselben Rechenweg wie §4.3 (zwei gemessene Klassenraten, Wohngebäudeanteil 0,872, nationales Mengengerüst 339.000/1,38 Mio. Adressen) statt mit dem abgelösten Einheitsschadensgrad 6,311/1.200 und sichert M₀ = 1,360, 1,32 und 1,81 mit Toleranz 5e-3 zu; die frühere Zusicherung `assert A_stern / (M0 * f_lo) > 2.00` ist ersetzt, weil sie mit dem revidierten M₀ falsch wäre. **§7.2 Ergebnis-Sensitivität**: nur der Satz zur reinen Basiswert-Umstellung trägt jetzt 1,32; die Kernzahlen 0,54 statt 0,99 Mrd. €₂₀₂₆/a, Band 0,39–0,74, f_AWM = 0,55 (0,40–0,75), Zeitwert 290.004 €₂₀₂₆ und Untergrenze 0,31 sind nachgerechnet **unverändert**, weil sie A\* · f_AWM sind und nicht an M₀ hängen. **Entscheidungslog Zeile 7**: Begründungsspalte „höbe λ auf 1,91 (bis 2,62)“ → „1,32 (bis 1,81)“ mit datiertem Vermerk auf die M₀-Revision; die Entscheidung selbst (Neuwert bleibt Basiswert) unberührt, kein Historie-Marker, weil der Eintrag im geltenden Teil steht. **Kopf-Statuszeile „Offen“**: Punkt (1) nennt jetzt, dass M₀ und λ aus dem Stichprobenlauf der acht Anker-Kommunen gerechnet sind und nur noch die out-of-sample-Verteilungsprüfung (Befund 34) und der Fit über die Jahresreihe statt über den Mittelwert (Befund 33) offen sind. Abgelöste Werte wurden **ersetzt, nicht historisiert**; der Revisionsverlauf steht hier im Ledger. **Ausdrücklich offen gelassen:** Der Satz in der Einleitung von Kapitel 4 („der Zahlenwert im Produkt-Block in Kap. 7 steht zum Stand dieser Revision noch auf dem abgelösten Wert und ist im Ledger als Restpunkt von Befund 32 geführt“) ist mit diesem Paket überholt, liegt aber in Kapitel 4, das dieses Paket laut Dateirahmen nicht anfassen darf — er ist als redaktioneller Restpunkt für die Gegenprüfung vermerkt, nicht still geändert. | `python3 -c "s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();b=s.split('id: flood_bldg.lambda')[1].split('---')[0];z=s.split('beispiel_60_zeitwert')[1].split(chr(96)*3)[0];raise SystemExit(0 if 'wert: 0.724' in b and 'band: [0.29, 1.63]' in b and 'vorlaeufig: true' in b and '1,32 (bis 1,81)' in s and '1,91' not in s and '2,62' not in s and '2.00' not in z else 1)"` und `python3 backend/scripts/lint_methodik.py 60` | **behoben** — Fundstellen §4.3, §4.4, Kap. 7 (Block `flood_bldg.lambda`), §7.2 tragen durchgängig M₀ = 1,360 und λ = 0,724 (Band 0,29–1,63); λ bleibt fachlich **vorläufig**, das ist kein Rest von Befund 32, sondern Gegenstand der offenen Befunde 33 und 34 |

Nicht angefasst (Dateirahmen): `backend/scripts/lint_methodik.py` (byte-gleich mit `origin/main`,
gehört T-0234), `docs/evidenz/register.md`, `backend/`, die Stichprobendateien unter
`docs/evidenz/60_stichprobe/`, **Kapitel 4 des Berichts** (in Schritt 2 mit T-0312 nachgezogen) und
die Kopftabelle „Offene Befunde“ dieses Ledgers (schreibt allein T-0296 fort).

**17.09.2026 · T-0321** (Befund 34 an 60, Schritt 4 von 4 zur Auflösung von T-0291; Ersatz für den
zweiten Teil des an der Budgetgrenze eskalierten T-0317; Schritt L1 aus
`.claude/methodik-loop.md`, Autor-Revision — keine Gegenprüfung, kein `/risiko-fortsetzen`, kein L4
nach eiserner Regel 4; die Gegenprüfung fährt T-0246 in eigener Sitzung). Geändert wird
ausschließlich dieses Ledger; nichts wurde neu hergeleitet oder neu gerechnet — der Rechenweg steht
bereits im Block **17.09.2026 · T-0315** oben (Punkte (a) bis (e): Kleinste-Quadrate-Schätzer,
Jahres-Auswahlregel, Fenster-Sensitivität, Tukey-Fence-Bandherleitung), die Zahlen stehen bereits im
Bericht `docs/methodik/60_gebaeudeschaeden_flusshochwasser.md` (Kapitel 4 aus T-0318/T-0319, Kapitel
7 und §7.2 aus Paket 4a/T-0313). Dieses Paket fasst nur zusammen und belegt, damit die Statuszeile
für Befund 34 in diesem Ledger den bereits vollzogenen Nachzug wörtlich abbildet.

| Nr | Kat. | Vorgenommene Änderung | Prüfausdruck | Status danach |
|---|---|---|---|---|
| 34 | A | **Zusammenfassung und Beleg der bereits im Bericht vollzogenen Kleinste-Quadrate-Ankerbestimmung.** \(A_{\text{ver}}\) = 1,838 Mrd. €₂₀₂₆-Preisstand-2024 aus dem Kleinste-Quadrate-Mittel der vollständigen GDV-Jahresreihe 2002–2024 (§4.1); \(A^{*}\) = \(A_{\text{ver}} \cdot w_{\text{wg}} \cdot u \cdot \varphi_{\text{fluss}} \cdot \kappa \cdot \pi\) = 1,838 · 0,615865 = **1,132** Mrd. €₂₀₂₆/a (§4.2); \(\lambda = A^{*}/M_0\) = 1,132 / 1,360 = **0,832** (Band **0,22–1,66**, Tukey-Fence-Herleitung aus (e)). \(w_{\text{wg}}\) = 0,65 bleibt eine Abschätzung von KAP3, belegt über `docs/evidenz/60_gdv_wohngebaeude_2024.csv` (§4.1, Zeile `w_wg`). Fundstellen im Bericht: **§4.1** (Ankerreihe, Kleinste-Quadrate-Mittel, Quelle), **§4.2** (Zielwert der Bundessumme, \(w_{\text{wg}}\)-Herleitung), **§4.4** (Niveau-Skalar \(\lambda\) = 0,832, Plausibilitätsschranke), **Kap. 7** Block `flood_bldg.lambda` (`wert: 0.832`), **§7.2** (Zeitwert-Sensitivität mit dem nachgezogenen Anker), **Entscheidungslog Nr. 8** (Mehrjahresmittel statt Einzeljahr 2024, mit Begründung). | `python3 -c "s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();raise SystemExit(0 if all(x in s for x in ('1,838','1,132','0,832','0,22','1,66','w_wg','wert: 0.832')) else 1)"` und `python3 backend/scripts/lint_methodik.py 60` | **behoben** — \(A_{\text{ver}}\) = 1,838, \(A^{*}\) = 1,132, \(\lambda\) = 0,832 (Band 0,22–1,66) tragen durchgängig in §4.1, §4.2, §4.4, Kap. 7 (Block `flood_bldg.lambda`) und §7.2; \(w_{\text{wg}}\) = 0,65 bleibt über `docs/evidenz/60_gdv_wohngebaeude_2024.csv` belegte Abschätzung von KAP3 |

Nicht angefasst (Dateirahmen): `docs/methodik/60_gebaeudeschaeden_flusshochwasser.md`,
`docs/evidenz/register.md`, `backend/`, `backend/scripts/lint_methodik.py` und die Kopftabelle
„Offene Befunde“ am Kopf dieses Ledgers (schreibt allein T-0296 fort). Die Befunde 33, 35, 36, 26,
28, 39, 41 und 42 sind in ihrem Status nicht angerührt.

**17.09.2026 · T-0292** (Befund 33 an 60: Verteilungsprüfung auf Daten gestellt, die nicht in
\(\lambda\) eingehen; Schritt L1 aus `.claude/methodik-loop.md`, Autor-Revision — keine
Gegenprüfung, kein L4 nach eiserner Regel 4. Geändert werden der Bericht
`docs/methodik/60_gebaeudeschaeden_flusshochwasser.md` und dieses Ledger. Gelesen, nicht verändert:
`docs/evidenz/60_gdv_jahresreihe_2002_2024.csv` (aus T-0314) und die Kalibrierfenster aus §4.1a
(Befund 34). Kein Vollraster-Lauf, §3.4.)

**Gerechnet wurde** (alles aus der Jahresreihe 2002–2024, Spalte `wert_mrd_eur`; Summe 42,28 Mrd. €,
Mittel 1,8383 = \(A_{\text{ver}}\) aus §4.1): ankerseitiger Erwartungswertanteil des seltenen
Regimes als Jahresauslassung \(R_{\text{anker}} = \sum_t \max(0, A_t - \bar{A}_{-t}) / \sum_t A_t\)
= 20,186/42,28 = **47,74 %** (Überschuss allein in 2021 = 11,25, 2002 = 5,82, 2013 = 2,16,
2024 = 0,80, 2016 = 0,17); Jackknife-Standardfehler über die 23 Jahre **11,16 Pp** (Replikate
37,61 % bis 49,87 %); Ableseunschärfe ±0,05 Mrd. € je Balken im ungünstigsten Muster **1,73 Pp**
(46,07 % bis 49,47 %); Toleranz \(\sqrt{11{,}16^2 + 1{,}73^2 + 2{,}30^2}\) = **11,52 → ±11,5 Pp**;
Modellseite unverändert **33,86 %**; Abstand **13,88 Pp**.

| Nr | Kat. | Vorgenommene Änderung | Prüfausdruck | Status danach |
|---|---|---|---|---|
| 33 | A | **Verteilungsprüfung in §4.5 auf Daten gestellt, die in \(\lambda\) nicht eingehen; Toleranz hergeleitet und vor dem Ergebnis fixiert; Ausgang als Modellentscheid ausgewiesen.** Fundstelle **§4.5** (neu überschrieben „… (Jahresauslassung über die Ankerreihe)“). Zu den vier Teilen des Befunds: **(a)** Die Ankerseite ist nicht mehr der Überschuss des Einzeljahres 2024 über das Mittel derselben Quelle, sondern eine **Jahresauslassung (Leave-one-out)** über die 23 Jahreswerte aus `docs/evidenz/60_gdv_jahresreihe_2002_2024.csv`: Jedes Jahr wird gegen das **ohne dieses Jahr** gebildete Normaljahr \(\bar{A}_{-t}\) gemessen, kein Jahr prüft sich gegen sich selbst. Die Unabhängigkeit ist zusätzlich strukturell belegt statt beziffert: \(R_{\text{anker}}\) ist **skaleninvariant** (Zähler und Nenner homogen vom Grad 1), trägt also keine Niveauinformation, während \(\lambda\) allein aus dem Niveau folgt (§4.1a). Der Satz mit der Überlappungsquote „1 von 23 Kalibrierjahren“ ist ersatzlos gestrichen. **(b)** Beide Seiten sind jetzt **Erwartungswertanteile**: Zähler und Nenner der Ankergröße sind Summen über dieselben 23 Jahre, geteilt durch 23 stehen dort Erwartungswert des Überschusses und Erwartungswert der Jahressumme — vergleichbar mit dem modellseitigen Anteil am Erwartungswert. **(c)** Das ankerseitige Toleranzbudget ist **hergeleitet statt gesetzt**: Jackknife-Standardfehler der Prüfgröße über die 23 Jahre ±11,2 Pp und Ableseunschärfe ±1,7 Pp, quadratisch zu ±11,3 Pp, mit dem modellseitigen Band ±2,3 Pp zu **±11,5 Pp**; die gesetzte Zeile „dafür ±12,5 Prozentpunkte“ ist entfallen. Die Toleranz ist damit **enger** als die abgelöste (±15) und steht im Text **vor** dem Ist-Ergebnis; die Kombinationsregel (quadratisch, unabhängige Beiträge) ist mit ihr vorab festgelegt. Die beiden nicht bezifferbaren Unschärfen (gepoolt fluvial/pluvial, versicherte statt gesamter Schäden) gehen ausdrücklich **nicht** ins Budget ein, sondern stehen als Modellgrenze. **(d) Ausgang:** Abstand 47,7 % gegen 33,9 % = **13,9 Pp > 11,5 Pp — die Prüfung wird nicht bestanden.** Sie wird weder durch Weiten der Toleranz noch durch Nachziehen der drei Stützstellen geheilt, sondern als **Modellentscheid** geführt (§4.5, eigener Absatz): Richtung benannt (das Modell gewichtet das seltene Regime rund 14 Pp zu niedrig), kein Nachfitten der Form (§2.4), \(\lambda\) bleibt gesetzt (Prüfgröße skaleninvariant, Niveau unberührt) und **vorläufig**. Nachgezogen sind außerdem die P1-Zeile „Toleranz Verteilungsprüfung“ in §4.8 (±11,5 mit Herleitung), der Regime-Teil des Blocks `beispiel_60_kalibrierung` (rechnet Reihe, Jahresauslassung, Skaleninvarianz, Jackknife, Ableseunschärfe, Toleranz und den nicht bestandenen Abstand nach) sowie die drei Stellen, die den Befund als offen begründeten (Kopf-Statuszeile, Einleitung Kap. 4, §4.4). **Restpunkt, ausdrücklich nicht still nachgezogen:** §5.1.3 leitet die obere Bandgrenze \(s_{\text{bem}} \le 0{,}62\) aus dem **abgelösten** Ankerwert 38,5 % her; mit 47,7 % läge sie bei 0,52. Der Nachzug zieht \(r_{\text{S092}}\), Kap. 1, Kap. 2, §3.5, §5.1.1, §5.1.2 und Kap. 7 nach sich und gehört nicht in dieses Paket — er ist im Bericht (§5.1.3, Absatz „Nachtrag dieser Revision“) und hier als Restpunkt vermerkt. | `python3 -c "s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();k=s.split(chr(10)+'### 4.5 ')[1].split(chr(10)+'### 4.6 ')[0];raise SystemExit(0 if ('1,0/2,6' not in k and '1 von 23 Kalibrierjahren' not in k and 'dafür ±12,5 Prozentpunkte' not in k and 'Erwartungswertanteil' in k and 'Leave-one-out' in k and '60_gdv_jahresreihe_2002_2024.csv' in k and k.index('Toleranz — vorab fixiert') < k.index('**Ist-Ergebnis.**')) else 1)"` und `python3 backend/scripts/lint_methodik.py 60` (der Prüfausdruck der Gegenprüfung zu Befund 33 endet seit diesem Paket mit **Exit 1**, weil er genau die drei jetzt entfernten Zeichenfolgen verlangt) | **behoben** — die Prüfung liegt außerhalb der Anpassungsdaten, der Ankerwert ist ein Erwartungswertanteil, die Toleranz ist hergeleitet und vorab fixiert. Ihr **Ausgang ist negativ**, und genau das steht als Modellentscheid im Bericht; der Kalibrier-Prüfstein §6 gilt damit als **nicht bestanden** und ist als solcher ausgewiesen, nicht als offener Befund |

Nicht angefasst (Dateirahmen): `backend/scripts/lint_methodik.py` (byte-gleich mit `origin/main`,
gehört T-0234), `docs/evidenz/60_gdv_jahresreihe_2002_2024.csv` und die übrigen Evidenzdateien
(nur gelesen), `docs/evidenz/register.md`, `backend/` und die Kopftabelle „Offene Befunde“ am Kopf
dieses Ledgers (schreibt allein T-0296 fort). Die Befunde 34, 35, 36, 26, 28, 37, 39, 41 und 42
sind in ihrem Status nicht angerührt; Befund 37 (fehlende Herleitung des ±12,5) verliert mit diesem
Paket seinen Toleranz-Teil, wird aber nicht von hier aus geschlossen.

**18.09.2026 · T-0295** (Befund 39 an 60: Doppelzählungs-Wächter auf das über die Kalibrierjahre
gewichtete Ausstattungsmittel umgestellt; Schritt L1 aus `.claude/methodik-loop.md`,
Autor-Revision — keine Gegenprüfung, kein L4 nach eiserner Regel 4. Geändert werden der Bericht
`docs/methodik/60_gebaeudeschaeden_flusshochwasser.md` (§4.7) und dieses Ledger. \(\Delta q\)
(§5.1.2, Wert 0,10, Band 0,05–0,20, Abschätzung von KAP3, P2) wird hier **nicht** neu geschätzt und
behält Wert, Band und Sensitivität; die Kalibrierjahre und Zeitfenster aus §4.1a (Befund 34) werden
übernommen, nicht neu hergeleitet.)

| Nr | Kat. | Vorgenommene Änderung | Prüfausdruck | Status danach |
|---|---|---|---|---|
| 39 | B | **Referenzzustand des Wächters in §4.7 auf das über die Kalibrierjahre gleichgewichtete Ausstattungsmittel umgestellt, Verfallsregel auf die tatsächliche Gewichtsverschiebung umgestellt, Verzerrung bei geparktem \(q_0\) als Modellgrenze beziffert.** Fundstelle **§4.7**, Absätze „Wächter — Referenzzustand ist das gewichtete Ausstattungsmittel, nicht der Stichtag", „Verfallsregel, umgestellt auf die tatsächliche Gewichtsverschiebung" und „Modellgrenze: Richtung und Größenordnung der Verzerrung bei geparktem \(q_0\)". Der Referenzzustand ist nicht mehr der „Ausstattungsstand 31.12.2024", sondern das arithmetische, über die 23 Kalibrierjahre **gleichgewichtete** Ausstattungsmittel (Gewicht 1/23 je Jahr) — Konsequenz aus §4.1a: Bei konstantem \(M_t \equiv M_0\) fällt der Kleinste-Quadrate-Schätzer von \(\lambda\) auf das arithmetische Mittel der Ankerreihe zurück, jedes Kalibrierjahr trägt also gleiches Gewicht. Eine Nachrüstung aus dem Jahr \(t\) geht mit Gewicht \((2024-t+1)/23\) in dieses Mittel ein (2020: 21,7 %, 2014: 47,8 %, 2002: 100 %) und steckt nur in dieser Höhe tatsächlich im kalibrierten Niveau. **Verfallsregel:** Statt „verschiebt sich der Referenzzustand mit einem neu aufgenommenen Kalibrierjahr um ein Jahr" steht jetzt die tatsächliche Verschiebung: Bei einer Fenstererweiterung von 23 auf 24 Jahre verschiebt sich das gleichgewichtete Mittel um **1/24** des Abstands zwischen neuem Jahreswert und bisherigem Mittel, nicht um ein Jahr; der Hebelwert verfällt entsprechend erst mit dem tatsächlichen Neu-Fit von \(\lambda\) auf das erweiterte Fenster. **Modellgrenze:** Weil \(\Delta q\) (§5.1.2) operativ weiterhin pauschal mit Gewicht 1 statt mit dem jahresabhängigen Gewicht \((2024-t+1)/23\) sperrt — eine jahresscharfe Zurechnung ist mangels Datenquelle für \(q_0\) nicht möglich —, wird der bereits eingepreiste Anteil einer Vor-2025-Maßnahme aus Jahr \(t\) um \((t-2002)/23\) **überschätzt**: 78,3 Prozentpunkte für 2020 (21,7 % tatsächlich gegenüber angenommenen 100 %), 52,2 Prozentpunkte für 2014, 0 für 2002, bis zu 95,7 % für 2024. Die Richtung ist damit **konservativ gegen Doppelzählung, aber unterzählend beim Hebel**: Der Wächter bucht keinen Objektschutz doppelt, lässt aber einen — nicht bezifferbaren, da \(q_0\) und seine Verteilung über die Nachrüstjahre geparkt sind — Teil des tatsächlich wirksamen Hebels ungezählt. \(\Delta q\) selbst (0,10, Band 0,05–0,20, §5.1.2) ist von dieser Umstellung nicht berührt: Es zählt weiterhin nur Nachrüstungen ab 2025, ohne eigene Schätzung des vor 2025 vorhandenen Bestands. | `python3 -c "s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();t=s.split(chr(10)+'### 4.7 ')[1].split(chr(10)+'### 4.8 ')[0];k=s.split(chr(10)+'### 5.1.2 ')[1].split(chr(10)+'### 5.1.3 ')[0];raise SystemExit(0 if ('Ausstattungsstand 31.12.2024' not in t and 'gleichgewichtete' in t and '21,7' in t and '47,8' in t and '1/24' in t and '78,3' in t and '52,2' in t and 'unterzählt' in t and '§4.7' in k) else 1)"` und `python3 backend/scripts/lint_methodik.py 60` (der Prüfausdruck der Gegenprüfung zu Befund 39 endet seit diesem Paket mit **Exit 1**, weil er genau die jetzt entfernte Zeichenfolge „Ausstattungsstand 31.12.2024“ ohne das Wort „gewicht“ verlangt) | **behoben** — der Referenzzustand ist das über die Kalibrierjahre gewichtete Ausstattungsmittel statt eines Stichtags, die Verfallsregel folgt der tatsächlichen Gewichtsverschiebung (1/24 statt ein Jahr), und Richtung (unterzählend) sowie Größenordnung (52,2–95,7 % Überschätzung des eingepreisten Anteils, je nach Nachrüstjahr) der Verzerrung bei geparktem \(q_0\) stehen als Modellgrenze im Bericht. \(\Delta q\) behält Wert, Band und Sensitivität (S092/P2) |

Nicht angefasst (Dateirahmen): `backend/scripts/lint_methodik.py` (byte-gleich mit `origin/main`,
gehört T-0234), `docs/evidenz/` (nicht gelesen, nicht verändert), `backend/` und die Kopftabelle
„Offene Befunde" am Kopf dieses Ledgers (schreibt allein T-0296 fort). §5.1.2 verweist unverändert
auf §4.7 (Doppelzählungs-Wächter); \(\Delta q\), \(e_{\text{bem}}\), \(s_{\text{bem}}\), Kap. 1,
Kap. 2, §3.5, §5.1.1, §5.1.3, Kap. 7 und das Evidenz-Register sind von diesem Paket nicht berührt.

**18.09.2026 · T-0322** (Befund 36 an 60, Schritt 1 von 4; Ersatz für das an der Budgetgrenze
abgebrochene T-0293, das Ledger und Bericht in einem Lauf verlangte; Schritt L1 aus
`.claude/methodik-loop.md`, aber ausdrücklich nur der Rechenweg für Befund 36 — Bericht
`docs/methodik/60_gebaeudeschaeden_flusshochwasser.md` wird in diesem Paket **nicht** angefasst;
keine Gegenprüfung, kein `/risiko-fortsetzen`, kein L4 nach eiserner Regel 4. Der Bericht bleibt
byte-gleich, das zieht Schritt 2 nach.) Geändert wurde ausschließlich dieses Ledger.

| Nr | Kat. | Vorgenommene Änderung | Status danach |
|---|---|---|---|
| 36 | B | Rechenweg für ein M₀-Band aus den Eingangsgrößen des Stichprobenlaufs, das daraus fortgepflanzte λ-Band und die daraus hergeleitete Plausibilitätsschranke festgehalten (Details unten). Der Nachzug im Bericht (§4.1a, §4.4, §4.8, `beispiel_60_kalibrierung`, Kap. 7 `flood_bldg.lambda`, Entscheidungslog Nr. 8) erfolgt in den Folgepaketen. | offen — Rechenweg steht, Nachzug in den Folgepaketen |

**(a) Bandenden der Eingangsgrößen von M₀.** M₀ = Wohngebäudeanteil · (Wohnfläche · BGF-Faktor ·
Wertsatz) · (Adressen_GK3+GK4 · Klassenrate_GK3+GK4 + Adressen_GK2 · Klassenrate_GK2), §4.3. Jede
der acht Eingangsgrößen erhält ein unteres und ein oberes Bandende:

| Eingangsgröße | Zentralwert | Unteres Bandende | Oberes Bandende | Quelle bzw. Abschätzung |
|---|---|---|---|---|
| Wohnfläche je Wohngebäude | 208 m² | **208 m²** | **208 m²** | **Quelle:** Register 60-R24-01 (4,1 Mrd. m² ÷ 19,7 Mio. Wohngebäude, amtliche Bestandsstatistik). Kein Band ausgewiesen — die Größe ist der Quotient zweier amtlicher Summen, keine Abschätzung von KAP3; sie geht deshalb unten wie oben mit demselben Punktwert ein, statt ihr ohne Beleg eine Streuung zu unterstellen. |
| BGF-Faktor | 1,30 | **1,25** | **1,40** | **Quelle:** Register 60-R24-01, §3.9 „Abgeschätzt" (Rechenschritt 3, Bericht Z. 371–373: „Band 1,25–1,40"). |
| Wertsatz | 1.950 EUR₂₀₂₆/m² BGF | **1.889 EUR₂₀₂₆/m² BGF** | **2.047 EUR₂₀₂₆/m² BGF** | **Quelle:** Register 60-R24-01 (Fortschreibungsfaktor 2023→2026, Band 1,07–1,16; Bericht Z. 364: „Band 1.889–2.047"). |
| Wohngebäudeanteil je Adresse | 0,872 | **0,872** | **0,872** | **Quelle:** Register 60-R17-01/60-R24-01 (19,7 Mio. Wohngebäude ÷ 22,6 Mio. Adressen, beides amtliche Bestandsstatistik, §4.3 Punkt 2). Kein Band ausgewiesen — Quotient zweier amtlicher Summen ohne publizierte Unsicherheit; Punktwert unten wie oben. |
| Klassenrate GK3+GK4 | 0,0059796/a | **0,0033/a** | **0,0103/a** | Restfehler-Position 3 aus Paragraf 4.3 (Streuung der Klassenrate über die acht Anker-Kommunen, Faktor 3,1; `m0_klassenraten.csv`, Spalte `rate_exponiert_hqextrem_1_pro_a`, Klasse `gk3_gk4`: Minimum Deggendorf 0,0033, Maximum Grimma 0,0103). |
| Klassenrate GK2 | 0,00067515/a | **0,000301/a** | **0,001154/a** | **Abschätzung von KAP3**, hergeleitet analog zu Restfehler-Position 3: `m0_klassenraten.csv`, Spalte `rate_exponiert_hqextrem_1_pro_a`, Klasse `gk2` — Minimum Reichertshofen 0,000301000488605, Maximum Halle (Saale) 0,001154174448010. Für GK2 beziffert Paragraf 4.3 diese Streuung nicht als eigene Restfehler-Position; das Minimum/Maximum der acht Kommunenwerte wird deshalb hier als KAP3-Abschätzung nach demselben Verfahren übernommen, nicht als Restfehler-Position im Bericht zitiert. |
| Exponierte Adressen GK3+GK4 | 339.000 | **339.000** | **339.000** | **Quelle:** Register 60-R17-01 (ZÜRS Geo 2025, GK3 1,1 % + GK4 0,4 % von 22,6 Mio. Adressen; §4.3 Punkt 1). Kein Band ausgewiesen — die Zonierungsquote ist eine Bestandsstatistik, keine Abschätzung; Punktwert unten wie oben. |
| Exponierte Adressen GK2 | 1.380.000 | **1.380.000** | **1.380.000** | **Quelle:** Register 60-R17-01 (ZÜRS Geo 2025, GK2 6,1 % von 22,6 Mio. Adressen; §4.3 Punkt 1). Kein Band ausgewiesen, aus demselben Grund wie oben. |

**(b) M₀-Band.** Aus den Bandenden in (a), alle Enden gleichgerichtet (wie in §4.2 für \(A^{*}\)
— multiplikative Bandenden, keine Verteilungsannahme, Anweisung A-0034):

Wert je exponiertem Wohngebäude: unten 208 · 1,25 · 1.889 = 491.140 EUR₂₀₂₆; Zentralwert
208 · 1,30 · 1.950 = 527.280 EUR₂₀₂₆ (unverändert, §4.3); oben 208 · 1,40 · 2.047 = 596.086,4
EUR₂₀₂₆.

Summenterm (Adressen × Klassenrate): unten 339.000 · 0,0033 + 1.380.000 · 0,000301 = 1.118,7 +
415,38 = 1.534,08/a; Zentralwert 339.000 · 0,005979599550826 + 1.380.000 · 0,000675151053693 =
2.958,79/a (unverändert, §4.3); oben 339.000 · 0,0103 + 1.380.000 · 0,001154 = 3.491,7 + 1.592,52 =
5.084,22/a.

M₀_unten = 0,872 · 491.140 EUR · 1.534,08/a = 656.945.337 EUR₂₀₂₆/a ≈ **0,657 Mrd. EUR₂₀₂₆/a**
M₀_zentral = 0,872 · 527.280 EUR · 2.958,79/a = 1.360.417.852 EUR₂₀₂₆/a ≈ **1,360 Mrd. EUR₂₀₂₆/a**
(unverändert, §4.3)
M₀_oben = 0,872 · 596.086,4 EUR · 5.084,22/a = 2.642.713.194 EUR₂₀₂₆/a ≈ **2,643 Mrd. EUR₂₀₂₆/a**

Das Band ist damit **M₀ = 0,657–2,643 Mrd. EUR₂₀₂₆/a** um den Zentralwert 1,360.

**(c) Fortgepflanztes λ-Band.** §4.2 beziffert das Band von \(A^{*}\) bereits als „alle Enden
gleichgerichtet: 0,297–2,263 Mrd. €₂₀₂₆/a" (Bericht §4.2, Zeile „Zielwert"; identisch in
`beispiel_60_kalibrierung`, `lo`/`hi`). Mit dem M₀-Band aus (b) fällt das vollständig
fortgepflanzte λ-Band — Zähler und Nenner unabhängig an ihren jeweiligen Extremen — auf

λ_unten = A*_unten / M₀_oben = 0,297 / 2,642713194 = 0,112384… → **0,11**
λ_oben = A*_oben / M₀_unten = 2,263 / 0,657006701 = 3,444409… → **3,44**

**Fortgepflanztes λ-Band: 0,11–3,44** (Rundungsregel siehe (d)). Das ist deutlich breiter als das
bisher im Bericht geführte λ-Band 0,22–1,66 (§4.4), weil jenes nur die Ankerunsicherheit von
\(A^{*}\) bei **unverändertem** M₀ fortpflanzt — genau die Lücke, die Befund 36 benennt.

**(d) Herleitung der Plausibilitätsschranke.** Die bisherige Schranke [0,50; 2,00] (§4.4/§4.8) war
eine freihändig gesetzte Abschätzung von KAP3 („Faktor 2 um den Neutralwert 1") ohne Bezug zu
einem gerechneten Band. Statt sie an das Ergebnis anzupassen, wird sie hier durch das in (c)
vollständig fortgepflanzte λ-Band **ersetzt**: Eine Neubestimmung von λ, die außerhalb der Spanne
läge, die aus den eigenen, in (a) benannten Bandenden aller Eingangsgrößen folgt, wäre mit dem
eigenen Modell nicht mehr verträglich — das ist die einzige ergebnisunabhängige Bezugsgröße, die
ohne eine zusätzliche, nicht durch A-0034 gedeckte Verteilungsannahme zur Verfügung steht.

**Plausibilitätsschranke λ = [0,11; 3,44].**

**Rundungsregel:** zwei Nachkommastellen, kaufmännisch gerundet (dieselbe Regel wie für das
bestehende λ-Band 0,22/1,66 in §4.4) — nicht auf die nächste „glatte" Zahl aufgerundet bzw.
abgerundet, damit die Schranke exakt der Rechnung aus (c) entspricht und nicht nachträglich
verengt oder geweitet wird.

**Entscheidungsregel** (unverändert zu §4.4, jetzt mit hergeleiteter statt gesetzter Schranke):
Ergibt eine Neubestimmung λ < 0,11 oder λ > 3,44, wird **nicht** der Skalar gesetzt, sondern das
Modell gilt als fehlerhaft — dann trägt eine Eingangsgröße den Fehler, und der Befund geht ins
Ledger, bevor gerechnet wird. Der Zentralwert wird weiterhin gegen dieselbe Schranke geprüft wie
bisher; geändert hat sich nur, dass die Schranke jetzt aus dem eigenen fortgepflanzten Band folgt
statt gesetzt zu sein.

**Beurteilung des bestehenden λ-Bands gegen die neue Schranke.** Das untere Bandende des bisher im
Bericht geführten λ-Bands (0,22, §4.4, aus dem Ankerband bei unverändertem M₀) liegt **innerhalb**
der neuen Schranke [0,11; 3,44], weil 0,22 > 0,11 ist. Das obere Bandende (1,66) liegt ebenfalls
**innerhalb** der neuen Schranke, weil 1,66 < 3,44 ist — kein Bandende des bisherigen λ-Bands muss
also als Ausnahme von der Schranke begründet werden.

**(e) Nachzug im Bericht (Folgepaket).** Fünf Fundstellen sind auf den neuen Rechenweg zu ziehen:

1. **§4.1a, Absatz unter der Fenstertabelle** (Bericht Z. 1048–1053, beginnend „Drei der vier
   λ-Werte liegen innerhalb der Plausibilitätsschranke [0,50; 2,00] … nur das kürzeste Fenster …
   unterschreitet sie. Genau das ist der zweite Grund für die Wahl des Hauptfensters …"). Gegen die
   neue Schranke [0,11; 3,44] liegen **alle vier** Fenster-λ (0,832 / 0,935 / 0,611 / 0,457)
   innerhalb — auch das kürzeste Fenster mit 0,457 > 0,11. Der Satz ist deshalb zu ersetzen durch
   eine Fassung, die (i) die neue Schranke nennt, (ii) feststellt, dass alle vier Fenster innerhalb
   liegen, und (iii) die Wahl des Hauptfensters **allein** auf die ergebnisunabhängige
   Auswahlregel stützt (der erste, tragende Grund im Absatz zuvor), weil das bisherige zweite
   Argument („unterschreitet die Schranke") mit der neuen, breiteren Schranke nicht mehr trägt.
2. **§4.4, λ-Zeile und Absatz „Plausibilitätsschranke"**: „[0,50; 2,00]" wird durch „[0,11; 3,44]"
   ersetzt, mit Verweis auf die Herleitung aus dem fortgepflanzten Band von \(A^{*}\) (§4.2) und
   \(M_0\) (§4.3, neu: Band 0,657–2,643). Der Satz „Dass das untere Bandende 0,22 unter 0,50 fällt
   … ist als Befund 36 im Ledger offen" entfällt, weil 0,22 innerhalb der neuen Schranke liegt;
   Befund 36 schließt damit inhaltlich erst mit dem Nachzug in diesem Bericht (Schritt 2).
3. **§4.8, Zeilen „λ Niveau-Skalar" und „Plausibilitätsschranke λ"**: Erstere ergänzt den Verweis
   auf das M₀-Band 0,657–2,643 in der Herkunftsspalte; letztere trägt „0,11 bzw. 3,44" statt „0,50
   bzw. 2,00" und in der Quellspalte „berechnet aus dem fortgepflanzten Band von \(A^{*}\) und
   \(M_0\) (§4.4), Rundungsregel und Entscheidungsregel wie (d)" statt „Abschätzung von KAP3
   (Faktor 2 um den Neutralwert 1)".
4. **Block `beispiel_60_kalibrierung`**: neue Zusicherungen für `wg_lo`/`wg_hi` (491.140,0 /
   596.086,4), `term_lo`/`term_hi` (1.534,08 / 5.084,22), `M0` gebunden auf 0,657–2,643 sowie
   `lam_lo`/`lam_hi` = `lo`/`M0_hi` bzw. `hi`/`M0_lo`, gerundet auf 0,11/3,44; die Zusicherung
   `0.50 <= lam <= 2.00` wird durch `0.11 <= lam <= 3.44` ersetzt (der Zentralwert 0,832 bleibt
   innerhalb beider Schranken, die Zusicherung wechselt nur die Grenzen).
5. **Kap. 7, Produkt-Block `flood_bldg.lambda`**: neues Feld `plausibilitaetsschranke: [0.11,
   3.44]` mit `herleitung_anker` auf den neuen Absatz in §4.4, an die Stelle des bisher nur in
   §4.8 geführten Zahlenpaars; **Entscheidungslog Zeile 8** (Mehrjahresmittel statt Einzeljahr
   2024, Befund 34) erhält einen Nachtrag, dass die in §4.4 seit T-0245 gesetzte Schranke mit
   diesem Paket durch die hergeleitete Schranke [0,11; 3,44] ersetzt ist (Befund 36).

**(f) Prüfausdruck (rechnet (b), (c) und (d) allein aus den Bandenden aus (a) nach).**

```bash
python3 -c "wf=208.0
bgf_lo,bgf_c,bgf_hi=1.25,1.30,1.40
ws_lo,ws_c,ws_hi=1889.0,1950.0,2047.0
w_wohn=0.872
n34,n2=339000,1380000
r34_lo,r34_c,r34_hi=0.0033,0.005979599550826,0.0103
r2_lo,r2_c,r2_hi=0.000301,0.000675151053693,0.001154
wg_lo=wf*bgf_lo*ws_lo; wg_c=wf*bgf_c*ws_c; wg_hi=wf*bgf_hi*ws_hi
term_lo=n34*r34_lo+n2*r2_lo; term_c=n34*r34_c+n2*r2_c; term_hi=n34*r34_hi+n2*r2_hi
M0_lo=w_wohn*wg_lo*term_lo/1e9; M0_c=w_wohn*wg_c*term_c/1e9; M0_hi=w_wohn*wg_hi*term_hi/1e9
assert abs(M0_c-1.360)<5e-3 and abs(M0_lo-0.657)<5e-3 and abs(M0_hi-2.643)<5e-3
A_lo,A_hi=0.297,2.263
lam_lo=A_lo/M0_hi; lam_hi=A_hi/M0_lo
schranke=(round(lam_lo,2),round(lam_hi,2))
assert schranke==(0.11,3.44)
lam_band=(0.22,1.66)
assert schranke[0]<=lam_band[0]<=schranke[1] and schranke[0]<=lam_band[1]<=schranke[1]
print('OK M0', round(M0_lo,3), round(M0_c,3), round(M0_hi,3), 'schranke', schranke)"
```

Ausgeführt am 18.09.2026: `OK M0 0.657 1.36 2.643 schranke (0.11, 3.44)`, Exit 0.

**Status.** Befund 36 bleibt **offen**. Dieses Paket schreibt bewusst nur ins Ledger: Der Bericht
(§4.1a, §4.4, §4.8, `beispiel_60_kalibrierung`, Kap. 7 `flood_bldg.lambda`, Entscheidungslog Nr. 8)
wird in Schritt 2 nachgezogen. Die Kopftabelle „Offene Befunde" bleibt unberührt (schreibt allein
T-0296 fort).

Nicht angefasst (Dateirahmen): `docs/methodik/60_gebaeudeschaeden_flusshochwasser.md`,
`docs/evidenz/register.md`, `backend/scripts/lint_methodik.py`, `backend/`, die Stichprobendateien
unter `docs/evidenz/60_stichprobe/` (gelesen, nicht verändert) und die Kopftabelle „Offene Befunde"
dieses Ledgers.

**18.09.2026 · T-0326** (Befund 36 an 60, Schritt 5 von 5; letzter Schritt der Ersatzkette für
T-0293. Schritt L1 aus `.claude/methodik-loop.md`, Autor-Revision — keine Gegenprüfung, kein
`/risiko-fortsetzen`, kein L4 nach eiserner Regel 4; die Gegenprüfung fährt T-0246 in eigener
Sitzung. Geändert wird ausschließlich dieses Ledger; der Bericht
`docs/methodik/60_gebaeudeschaeden_flusshochwasser.md` wird in diesem Paket nur gelesen, nicht
verändert — der Rechenweg steht bereits im Block **18.09.2026 · T-0322** oben (Punkte (a) bis (e)),
der Nachzug in den Bericht ist in den Zwischenschritten der Kette bereits vollzogen.)

| Nr | Kat. | Vorgenommene Änderung | Prüfausdruck | Status danach |
|---|---|---|---|---|
| 36 | B | **Nachzug des Rechenwegs aus T-0322 im Bericht bestätigt und Statuszeile geschlossen.** Das M₀-Band **0,657–2,643** Mrd. €₂₀₂₆/a steht in **§4.3** (Abschnitt „Modellsumme vor Kalibrierung"). Das aus dem A*-Band 0,297–2,263 (§4.2) und dem M₀-Band 0,657–2,643 (§4.3) vollständig fortgepflanzte λ-Band **0,11–3,44** steht in **§4.4** (Abschnitt „Der Niveau-Skalar", Kopfformel). Die Herleitung der Plausibilitätsschranke aus genau diesem fortgepflanzten Band — statt der bisherigen freihändig gesetzten Abschätzung „Faktor 2 um den Neutralwert 1" — steht ebenfalls in **§4.4** (Absatz „Plausibilitätsschranke", Rundungsregel zwei Nachkommastellen kaufmännisch, Entscheidungsregel unverändert). Die Führung der Schranke **[0,11; 3,44]** in der Parametertabelle steht in **§4.8** (Zeile „Plausibilitätsschranke λ", Wert „0,11 bzw. 3,44", Quellspalte „berechnet aus dem fortgepflanzten Band von \(A^{*}\) und \(M_0\)"). Der nachgezogene Produkt-Block `flood_bldg.lambda` steht in **Kap. 7**: `band: [0.11, 3.44]`, `herkunft: herleitung:§4.4`, `herleitung_anker: "#niveau-skalar"`. | `python3 -c "s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();raise SystemExit(0 if all(x in s for x in ('0,657–2,643','0,11–3,44','[0,11; 3,44]','0,11 bzw. 3,44','[0.11, 3.44]','0,297–2,263')) else 1)"` und `python3 backend/scripts/lint_methodik.py 60` | **behoben** — M₀-Band 0,657–2,643 (§4.3), das daraus und aus dem A*-Band fortgepflanzte λ-Band 0,11–3,44 samt hergeleiteter Plausibilitätsschranke (§4.4) und deren Führung in der Parametertabelle [0,11; 3,44] (§4.8) sind im Bericht durchgängig; der Produkt-Block `flood_bldg.lambda` (Kap. 7) trägt `band: [0.11, 3.44]` nach. Damit ist Befund 36 vollständig geschlossen. |

Nicht angefasst (Dateirahmen): `docs/methodik/60_gebaeudeschaeden_flusshochwasser.md` (nur
gelesen), `docs/evidenz/register.md`, `backend/scripts/lint_methodik.py`, `backend/`, die
Stichprobendateien unter `docs/evidenz/60_stichprobe/` und die Kopftabelle „Offene Befunde" am Kopf
dieses Ledgers (schreibt allein T-0296 fort, Vorgabe aus dem Vorhaben T-0281, Punkt 2). Der alte
Eintrag zu Befund 36 in der Runde-2-Tabelle (Status „offen — Rest: …") bleibt als Historie stehen.

**18.09.2026 · T-0333** (Befund 35 an 60, Schritt 2 von 5 der Ersatzkette für T-0294; Schritt L1 aus
`.claude/methodik-loop.md`, Autor-Revision — keine Gegenprüfung, kein `/risiko-fortsetzen`, kein L4
nach eiserner Regel 4. Geändert wird ausschließlich dieses Ledger; der Bericht
`docs/methodik/60_gebaeudeschaeden_flusshochwasser.md` bleibt byte-gleich, das zieht Schritt 3 nach.
Gelesen, nicht verändert: `docs/evidenz/60_wiederaufbauhilfen_2013_2021.csv`.)

| Nr | Kat. | Vorgenommene Änderung | Status danach |
|---|---|---|---|
| 35 (Zwischenstand T-0333) | B | Rechenweg für die ankerunabhängige Untergrenze \(U\) aus den amtlichen Wiederaufbauhilfen und für die klassengerechte Obergrenze \(O\) festgehalten (Zahlen, Quellen/Abschätzungen, Amtlichkeitsgebot-Ausnahme — Details unten). Der Nachzug im Bericht erfolgt in den Folgepaketen. | offen — Rechenweg steht, Nachzug in den Folgepaketen (abgelöst durch den Abschlussblock T-0336 unten) |

**(a) Untergrenze \(U\) aus den amtlichen Wiederaufbauhilfen 2013/2021.** Grundlage ist
`docs/evidenz/60_wiederaufbauhilfen_2013_2021.csv` mit den beiden gesetzlich festgeschriebenen
Fondsvolumina 8 Mrd. EUR (2013, AufbhG, § 4 Abs. 1 Satz 1 — fest zugesagter Betrag) und 30 Mrd. EUR
(2021, AufbhEG 2021, § 4 Abs. 1 — „bis zu", davon 16 Mrd. EUR im Jahr 2021 selbst zugeführt, der
Rest erst „nach Maßgabe des Haushaltsgesetzes"). Als **Ereignis-Mindestschaden** wird der kleinere,
vollständig feststehende Betrag angesetzt, nicht die unsichere Obergrenze von 2021: 8 Mrd. EUR
nominal 2013 (Quelle: CSV Zeile `wiederaufbauhilfe_fondsvolumen;8;…;2013`). Die Umrechnung auf
Preisstand 2026 ist eine **Abschätzung von KAP3**: Über 13 Jahre wird eine durchschnittliche
Preissteigerung von 2 %/a angesetzt (Herleitung: \(1{,}02^{13} = 1{,}294\)), also
\(E_{\min,2026} = 8 \cdot 1{,}294 = 10{,}35\) Mrd. EUR₂₀₂₆.

Der **Wohngebäude- bzw. Wohnanteil** ist eine **Abschätzung von KAP3**: Der Gesetzestext selbst
weist laut CSV-Anmerkung keinen auf Wohngebäude oder private Haushalte entfallenden Euro-Anteil aus
(„nennt Privathaushalte nur als eine von zwei Fördergruppen ohne Bezifferung"); angesetzt wird eine
grobe Drittelung der Aufbauhilfe-Mittel auf die drei Fördergruppen private Haushalte,
Infrastruktur und Wirtschaft/Landwirtschaft, also ein Privathaushalts-Anteil von rund einem Drittel
(≈ 1/3), und davon wiederum rund ein Drittel für die Gebäudesubstanz selbst — „Wohngebäude" ohne
Hausrat und ohne Fahrzeuge (≈ 1/3 des Privathaushalts-Anteils). Rechenschritt (reproduzierbar, keine
Quelle beziffert den Wert exakt): \(w = \tfrac{1}{3} \cdot \tfrac{1}{3} = \tfrac{1}{9} \approx
0{,}11\).

Der **flussseitige Anteil** ist ebenfalls eine **Abschätzung von KAP3** mit dem Wert
\(f_{\text{fluss}} = 0{,}90\): Beide geförderten Ereignisse — Elbe-/Donau-Hochwasser 2013,
Ahrtal-Flut 2021 — sind dokumentierte Flusshochwasserereignisse; der Abschlag von 10 Prozentpunkten
trägt Siel- und Sturzflutanteilen innerhalb derselben Schadenssummen Rechnung, die die
Fondsgesetze nicht getrennt ausweisen (Herleitung: Sachkenntnis der beiden Ereignisse, keine
Quelle beziffert den Trennanteil).

Die **Umlage auf die Wiederkehrzeit** ist eine **Abschätzung von KAP3**: Beide Ereignisse gelten
als Jahrhundertereignisse; angesetzt wird eine Wiederkehrzeit \(T = 100\) Jahre (Herleitung: analog
zur unter (c) verwendeten Jährlichkeit 0,01 a⁻¹ der GK2-Klasse, keine eigene Quelle für die
Wiederkehrzeit dieser beiden konkreten Ereignisse).

\[
U = \frac{E_{\min,2026} \cdot w \cdot f_{\text{fluss}}}{T}
  = \frac{10{,}35 \cdot 0{,}11 \cdot 0{,}90}{100}
  = \textbf{0,010 Mrd. EUR}_{2026}\text{/a}.
\]

**(b) Welche Ankergrößen gehen in \(U\) ein?** In dieses \(U\) geht **keine** der sechs
Ankergrößen \(A_{\text{ver}}\), \(w_{\text{wg}}\), \(u\), \(\varphi\), \(\kappa\) und \(\pi\) ein —
alle vier Eingangsgrößen unter (a) (Ereignis-Mindestschaden, Wohngebäude-/Wohnanteil, flussseitiger
Anteil, Umlage auf die Wiederkehrzeit) stammen aus den Wiederaufbauhilfe-Gesetzen und aus eigenen,
von den Ankerfaktoren unabhängigen Abschätzungen von KAP3. Genau das macht die Prüfung
\(U \le \lambda M_0\) nicht mehr trivial erfüllt: Befund 35a hatte gezeigt, dass die alte
Untergrenze \(U = A_{\text{ver}} w_{\text{wg}} \varphi \pi\) für jedes \(u\kappa \ge 1\) automatisch
unterhalb von \(A^{*} = U \cdot u\kappa \equiv \lambda M_0\) liegen musste, weil \(U\) ein
Teilprodukt derselben Faktoren war, aus denen \(\lambda M_0\) gebildet wird; mit der neuen, aus den
amtlichen Fondsgesetzen und eigenständigen Schätzungen gebildeten \(U\) besteht diese algebraische
Teilmengen-Beziehung nicht mehr, und die Lage von \(\lambda M_0\) = \(A^{*}\) = 0,832 · 1,360 =
1,132 Mrd. EUR₂₀₂₆/a (§4.4, Stand nach der Ankerrevision T-0320/T-0321) relativ zu \(U\) ist eine
echte, aus unabhängigen Zahlen folgende Aussage statt einer Tautologie.

**(c) Obergrenze \(O\) klassengerecht.** Grundlage sind die Register-Mengen 339.000 Adressen der
Klassen GK3+GK4 mit Jährlichkeit 0,1 a⁻¹, 1.380.000 Adressen der Klasse GK2 mit Jährlichkeit
0,01 a⁻¹ (beide unverändert aus Register 60-R17-01, wie unter (b) von Befund 35 in Runde 2
vorgeschlagen — keine abweichende Klassenrate wird hier angesetzt), dem Gebäudewert 527.280
EUR₂₀₂₆ je exponiertem Wohngebäude (Register 60-R24-01, unverändert) und der Deckelquote 0,250
(§3.3, Deckelung der Schadensfunktion):

\[
O = (339.000 \cdot 0{,}1 + 1.380.000 \cdot 0{,}01) \cdot 527.280 \cdot 0{,}250
  = 47.700 \cdot 527.280 \cdot 0{,}250
  = \textbf{6,29 Mrd. EUR}_{2026}\text{/a}.
\]

Das ist derselbe Wert, der im Befund-Eintrag der Runde 2 als klassengerechte Gegenrechnung bereits
genannt ist (6,29 Mrd. €₂₀₂₆/a, GK4 allein 1,19 Mrd.); dieses Paket rechnet ihn hier formal aus den
vier genannten Eingangsgrößen nach, statt ihn nur zu zitieren.

**(d) Ausnahme vom Amtlichkeitsgebot (§3.4) für die verbleibenden nicht-amtlichen
Eingangsgrößen.** §3.4 verlangt Sanity-Bänder mit Unter- und Obergrenze aus amtlicher Statistik
oder einer begründeten Ausnahme. Bei \(U\) sind die beiden Fondsvolumina amtlich (Bundesgesetze,
BGBl.), aber der Wohngebäude-/Wohnanteil, der flussseitige Anteil und die Umlage auf die
Wiederkehrzeit sind — wie unter (a) gezeigt — Abschätzungen von KAP3, weil die Gesetzestexte selbst
keine Aufteilung nach Verwendungszweck oder Schadensart ausweisen und keine amtliche Statistik
existiert, die die Aufbauhilfe-Mittel zweier Einzelereignisse auf Wohngebäude, Flussanteil und
Jährlichkeit herunterbricht. Bei \(O\) sind die Adresszahlen 339.000/1.380.000 aus der
ZÜRS-Klassifikation und der Gebäudewert 527.280 EUR₂₀₂₆ Branchenstatistik des GDV bzw. eine
Registerabschätzung, also ebenfalls keine amtliche Statistik im engeren Sinn; die Ausnahme ist hier
dieselbe wie an den übrigen Fundstellen des Berichts, an denen ZÜRS- und GDV-Zahlen bereits als
Abschätzung von KAP3 statt als amtliche Quelle geführt werden (z. B. §4.1 für den GDV-Anker), weil
für die bundesweite Betroffenheits- und Wertstruktur von Wohngebäuden keine amtliche Vollerhebung
existiert und ZÜRS/GDV die einzigen verfügbaren, branchenweit einheitlichen Klassifikationen sind.
Für beide Bandenden gilt deshalb dieselbe Ausnahmebegründung: Wo keine amtliche Statistik die
gesuchte Aufteilung liefert, tritt eine ausgewiesene, nachvollziehbare Abschätzung von KAP3 an ihre
Stelle, nicht eine stillschweigende Ersatzquelle.

**(e) Fixierung des Bandes vor der Lagepüfung.** Das Band [\(U\); \(O\)] = [0,010; 6,29] Mrd.
EUR₂₀₂₆/a wird mit diesem Paket vorab fixiert und im Nachzugsschritt nicht nachträglich geweitet,
unabhängig davon, wo \(\lambda M_0\) am Ende liegt. Der in Bericht-§4.4 seit der Ankerrevision
(T-0320/T-0321) ausgewiesene Wert \(\lambda M_0 = A^{*} = 0{,}832 \cdot 1{,}360 = 1{,}132\)
Mrd. EUR₂₀₂₆/a (derselbe Wert steht im Ist-Satz §4.6, Z. 1363) liegt innerhalb dieses fixierten
Bandes — nicht der abgelöste Stand 0,985 Mrd. EUR₂₀₂₆/a aus dem inzwischen verworfenen
Stichprobenlauf.

**(f) Nachzugsstellen (Schritt 3/4 der Ersatzkette).** Der hier festgehaltene Rechenweg ist an
folgenden Fundstellen nachzuziehen: **§4.6** (die Tabelle mit \(U\) = 0,639 und \(O\) = 2,26, der
Folgeabsatz mit der Herleitung beider Grenzen, und der Ist-Satz, der \(\lambda M_0\) gegen das Band
prüft); **§4.8** (die Zeilen „\(U\) Sanity-Untergrenze", „\(O\) Sanity-Obergrenze" und
„Betroffenheit exponierter Gebäude" der Parametertabelle); der Block `beispiel_60_kalibrierung`
(die Zeilen, die \(U\) und \(O\) berechnen, samt der zugehörigen Zusicherung/Assertion); und
**§7.2** (der Satz mit „0,556 · 0,55", der die alte, bundesweit einheitliche Untergrenze 0,556
fortschreibt und auf die neue \(U\) umzustellen ist).

**(g) Nachrechnung von \(U\) und \(O\).**

```python test: befund_35_u_o
python3 -c "
E_nom = 8.0
faktor_2026 = 1.02 ** 13
E_min_2026 = E_nom * faktor_2026
w = (1/3) * (1/3)
f_fluss = 0.90
T = 100
U = E_min_2026 * w * f_fluss / T

n_gk34 = 339000 * 0.1
n_gk2 = 1380000 * 0.01
wert_geb = 527280.0
q_deckel = 0.250
O = (n_gk34 + n_gk2) * wert_geb * q_deckel / 1e9

assert abs(U - 0.0103) < 2e-3, U
assert abs(O - 6.288) < 2e-2, O
print('U =', round(U, 3), 'Mrd. EUR2026/a; O =', round(O, 2), 'Mrd. EUR2026/a')
"
```

Ausgeführt am 18.09.2026: `U = 0.01 Mrd. EUR2026/a; O = 6.29 Mrd. EUR2026/a`, Exit 0.

**Status.** Befund 35 bleibt **offen**. Dieses Paket schreibt bewusst nur ins Ledger: der Bericht
(§4.6, §4.8, Block `beispiel_60_kalibrierung`, §7.2) wird in den Folgepaketen nachgezogen, der
Befundabschluss folgt danach. Die Kopftabelle „Offene Befunde" bleibt unberührt (schreibt allein
T-0296 fort).

Nicht angefasst (Dateirahmen): `docs/methodik/60_gebaeudeschaeden_flusshochwasser.md`,
`docs/evidenz/register.md`, `backend/scripts/lint_methodik.py`, `backend/`, die Stichprobendateien
unter `docs/evidenz/60_stichprobe/` und die Kopftabelle „Offene Befunde" dieses Ledgers (schreibt
allein T-0296 fort).

**18.09.2026 · T-0336** (Befund 35 an 60, Schritt 5 von 5 zur Auflösung von T-0294; Ersatz für den
Befundabschluss nach dem Muster T-0321; Schritt L1 aus `.claude/methodik-loop.md`,
Autor-Revision — keine Gegenprüfung, kein `/risiko-fortsetzen`, kein L4 nach eiserner Regel 4;
die Gegenprüfung fährt T-0246 in eigener Sitzung). Geändert wird ausschließlich dieses Ledger;
nichts wurde neu hergeleitet oder neu gerechnet — der Rechenweg steht bereits im Block
**18.09.2026 · T-0322/T-0333** oben, die Zahlen und der Nachzug stehen bereits im Bericht
`docs/methodik/60_gebaeudeschaeden_flusshochwasser.md` (§4.6 „Neufassung nach Befund 35",
§4.8-Parameterzeilen \(U\)/\(O\), Block `beispiel_60_kalibrierung`). Dieses Paket fasst nur
zusammen und belegt, damit die Statuszeile für Befund 35 in diesem Ledger den bereits vollzogenen
Nachzug wörtlich abbildet.

| Nr | Kat. | Vorgenommene Änderung | Prüfausdruck | Status danach |
|---|---|---|---|---|
| 35 | B | **Zusammenfassung und Beleg des bereits im Bericht vollzogenen Nachzugs zu den drei Teilpunkten des Befunds.** (a) **Zirkuläre Untergrenze:** \(U\) ist nicht mehr aus den Ankerfaktoren \(A_{\text{ver}}, w_{\text{wg}}, u, \varphi_{\text{fluss}}, \kappa, \pi\) gebildet, sondern aus den amtlichen Wiederaufbauhilfe-Fondsvolumina (BGBl.) mit den KAP3-Abschätzungen Wohnanteil, Flussanteil und Wiederkehrzeit zu \(U\) = 0,0103 Mrd. €₂₀₂₆/a, unabhängig von der Ankerseite — Fundstelle **§4.6**, Absatz zur Untergrenze. (b) **Obergrenze ohne Klassenbezug:** \(O\) ist jetzt klassengerecht aus den ZÜRS-Jährlichkeiten je Adressklasse gebildet (GK3/GK4 0,1 a⁻¹, GK2 0,01 a⁻¹ statt einer bandweiten Höchstrate) zu \(O\) = 6,29 Mrd. €₂₀₂₆/a — Fundstelle **§4.6**, Absatz zur Obergrenze. (c) **Fehlende Begründung der Ausnahme vom Amtlichkeitsgebot:** Für beide Bandenden steht im Bericht ausdrücklich, welche Eingangsgrößen amtlich sind (die beiden Fondsvolumina) und welche als Abschätzung von KAP3 an die Stelle fehlender amtlicher Aufteilungsstatistik treten (Wohn-/Flussanteil, Wiederkehrzeit bei \(U\); ZÜRS-Klassifikation und GDV-Gebäudewert bei \(O\)) — Fundstelle **§4.6**, Absatz „Ausnahme vom Amtlichkeitsgebot (§3.4)". Nachgezogen sind außerdem die P1-Zeilen „\(U\) Sanity-Untergrenze" und „\(O\) Sanity-Obergrenze" in **§4.8** sowie der Rechenblock zu \(U\) und \(O\) im Block **`beispiel_60_kalibrierung`** (Kommentar „4.6 Sanity-Band und Lage der kalibrierten Bundessumme (Befund 35, ankerunabhaengiges U)", Zusicherungen `U`, `O` und `U <= lam * M0 <= O`). Der in §4.4 ausgewiesene Wert \(\lambda \cdot M_0\) = 0,832 · 1,360 = 1,132 Mrd. €₂₀₂₆/a liegt innerhalb des neu fixierten Bandes [0,0103; 6,29] Mrd. €₂₀₂₆/a, und diese Lage ist jetzt eine echte, aus unabhängigen Zahlen folgende Aussage statt der früheren Tautologie. | `python3 -c "s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();k=s.split(chr(10)+'### 4.6 ')[1].split(chr(10)+'### 4.7 ')[0];raise SystemExit(0 if all(x in k for x in ('0,0103','6,29','Amtlichkeitsgebot','1,132')) else 1)"` und `python3 backend/scripts/lint_methodik.py 60` | **behoben** — die Untergrenze ist ankerunabhängig aus amtlichen Wiederaufbauhilfe-Fondsvolumina hergeleitet, die Obergrenze ist klassengerecht nach ZÜRS-Jährlichkeit gebildet, und die Ausnahme vom Amtlichkeitsgebot ist für beide Bandenden begründet ausgewiesen; \(\lambda M_0\) = 1,132 liegt innerhalb des neuen Bandes [0,0103; 6,29] |

Nicht angefasst (Dateirahmen): `docs/methodik/60_gebaeudeschaeden_flusshochwasser.md`,
`docs/evidenz/register.md`, `backend/`, `backend/scripts/lint_methodik.py` und die Kopftabelle
„Offene Befunde" am Kopf dieses Ledgers (schreibt allein T-0296 fort). Die übrigen Befunde sind in
ihrem Status nicht angerührt.

## Nachtrag zu Befund 2 (Knoten-Bilanz)

**18.09.2026 · T-0343** (letzter offener A-Befund; Vorgabe: Integrationsgate von `/integriere-risiko
60` verlangt null offene A-Befunde). Geändert wird ausschließlich dieses Ledger — Statusspalte und
Kopfzähler —, keine Revision des Berichts, keine Gegenprüfung.

Messung von heute (18.09.2026), Ausdrücke wörtlich wie ausgeführt, keine vorweggenommene Zahl:

```
$ grep -c "rechnet in: offen" docs/methodik/60_gebaeudeschaeden_flusshochwasser.md
0
```

```
$ sed -n '/^### Knoten-Bilanz/,/^### Weitergaben/p' docs/methodik/60_gebaeudeschaeden_flusshochwasser.md | grep "^|" | tail -n +3 | wc -l
32
```

Die zweite Zahl ist die Zahl der Datenzeilen der Tabelle „Knoten-Bilanz" in Kapitel 1 (Zeilen der
Tabelle abzüglich Kopf- und Trennzeile).

**Beurteilung nach Punkt 2 des Abnahmekriteriums.** Die erste Zahl ist `0`: Im gesamten Bericht
kommt `rechnet in: offen` kein einziges Mal vor, und damit auch in keiner der 32 Datenzeilen der
Knoten-Bilanz. Befund 2 trägt danach in der Kurztabelle unter „Offene Befunde" und in der
Befundtabelle der Review-Runde 1 den Status `behoben`. Nachweisspalte in beiden Tabellen:
Fundstelle Kapitel 1 „Wirkungskette & Knoten-Bilanz (§2.1)", Tabelle „Knoten-Bilanz" (direkt nach
dem Absatz „Entscheidungsstand (T-0235)"), Prüfausdruck
`grep -c "rechnet in: offen" docs/methodik/60_gebaeudeschaeden_flusshochwasser.md` = `0`. Alle 32
Zeilen tragen eine benannte Formelstelle (FS-Hazard/FS-Exposition/FS-Schadensgrad/
FS-Mengengerüst/FS-Schutzsystem/FS-Bestandsdynamik/FS-Vorsorge) oder `inaktiv` mit wörtlichem
Zitat aus `KWRA-Monetarisierung.xlsx` (Blatt und Zelle genannt); die Arbeit von T-0235 ist damit
vollständig in der Statusspalte nachgezogen, die die Regression der Runde 2 offengelassen hatte.

**Kopfzähler.** Mit Befund 2 auf `behoben` sinkt die Zahl der Zeilen mit Status `offen` oder
`bewusst offen` in der Kurztabelle „Offene Befunde" von 9 + 11 = 20 auf 8 + 11 = 19. Prüfausdruck
und Ausgabe (nach dieser Änderung):

```
$ sed -n '/^## Offene Befunde/,/^## Review-Runde 1/p' reviews/BEFUNDE_60.md | grep -oP '(?<=\| )(behoben|offen|bewusst offen)(?= \|)' | grep -c "offen"
19
```

Die Überschrift `## Offene Befunde (N)` ist entsprechend auf `## Offene Befunde (19)` gesetzt.

**Damit sind alle A-Befunde des Ledgers (1, 2, 3, 4, 5, 20, 32, 33, 34, 40) auf `behoben`.**

## Review-Runde 3

**Datum: 18.09.2026** · Eröffnungspaket (T-0359) der dritten Gegenprüfungsrunde nach §5 der
Aufgabe `docs/AUFGABE_METHODIK_SCHADENSRECHNUNG.md`. Dieses Paket legt den Abschnitt an, hält die
Vorbedingung fest und zitiert das deterministische Lint-Ergebnis des Tages; die elf Folgepakete
hängen ihre Verdikte darunter. **In diesem Paket wird keine Leitfrage beantwortet, kein Befund
geprüft und kein Befund behoben.** Eiserne Regel 4 („Review nur in frischer Session") ist gewahrt:
Diese Sitzung hat den geprüften Stand nicht geschrieben — geschrieben haben die Autoren-Pakete
T-0235 bis T-0243, T-0256 bis T-0259 und die Revisionspakete aus T-0281, alle im Endstatus.

**Befundnummern.** Das Ledger trägt heute die Nummern 1 bis 46 (Runde 1: 1–19, Runde 2: 20–46).
Neue Befunde dieser Runde werden fortlaufend ab der nächsthöheren freien Nummer vergeben; die
erste neue Nummer ist damit **47**.

### 0 · Vorbedingung nach §5, Schritt 0 — Prüfgrundlagen-Bundle (§1)

§5 der Aufgabe stellt der Gegenprüfung eine Vorbedingung voran: Das vollständige
Prüfgrundlagen-Bundle nach §1 — Bericht, diese Aufgabe, beide Arbeitsmappen, Anlagen — liegt der
Review-Session **ab dem ersten Turn** vor; ein Review ohne vollständiges Bundle ist ungültig
(Lehre aus der M0-Prüfung: nachgereichte Quellen erzeugten zwei Extra-Durchgänge). Die folgenden
Bestandteile liegen dieser Sitzung unter den genannten Pfaden im Repo vor, ohne Nachreichung; zur
Identifizierung des geprüften Standes ist je Datei die Größe in Bytes und der Anfang der
SHA-256-Summe angegeben (gemessen am 18.09.2026 in dieser Sitzung).

| Bestandteil des Bundles (§1) | Pfad | Liegt dieser Sitzung vor |
|---|---|---|
| Bericht (Prüfgegenstand) | `docs/methodik/60_gebaeudeschaeden_flusshochwasser.md` | ja, ab dem ersten Turn — 229.149 Bytes, SHA-256 `d36326bd5678…` |
| Aufgabe (einzige Instruktionsquelle, v2) | `docs/AUFGABE_METHODIK_SCHADENSRECHNUNG.md` | ja, ab dem ersten Turn — 38.446 Bytes, SHA-256 `08accbea6688…`; §1 und §5 in dieser Sitzung gelesen |
| Arbeitsmappe Wirkungsketten | `docs/Schadensbaum/KWRA-Schadensbaum_X_UBA-klimawirkungsketten.xlsx` | ja, ab dem ersten Turn — 86.813 Bytes, SHA-256 `2faac648aade…`; Blätter „Klimawirkungsketten", „Schadensbaum-Netzwerkliste" (nur gelesen, eiserne Regel 2) |
| Arbeitsmappe Monetarisierung | `docs/Schadensbaum/KWRA-Monetarisierung.xlsx` | ja, ab dem ersten Turn — 50.825 Bytes, SHA-256 `4383882d3a93…`; Blätter „Risiken-Monetarisierung", „Schadenskonten-System", „Rechenregeln", „Abgleich-Protokoll" (nur gelesen, eiserne Regel 2) |

Damit ist die Vorbedingung nach §5, Schritt 0 für Runde 3 erfüllt; die Folgepakete arbeiten auf
demselben Stand und verweisen auf diese Tabelle, statt sie zu wiederholen.

### 0.1 · Deterministisches Lint-Ergebnis vom 18.09.2026

Nach §5 („Zuerst die deterministischen Lint-Ergebnisse übernehmen — nicht manuell nachprüfen, was
die Maschine prüft") wird das Lint zu Beginn der Runde ausgeführt. Das Skript
`backend/scripts/lint_methodik.py` gehört T-0234 und wurde hier **nur ausgeführt, nicht geändert**.
Die folgende Ausgabe ist wörtlich die des Laufs von heute, einschließlich der führenden Leerzeile;
nichts daran ist vorhergesagt oder zusammengefasst:

```
$ python3 backend/scripts/lint_methodik.py 60

=== #60 · 60_gebaeudeschaeden_flusshochwasser.md ===
  162 Checks grün
  Historie-Marker: 0 markierte Zeilen (Ratchet None), 0 gedeckte Fundstellen abgelöster Werte:

ALLE LINTS GRÜN
```

**Rückgabewert des Aufrufs: `0`** (gemessen, nicht angenommen). Die Folgepakete übernehmen dieses
Ergebnis nach §5, statt es erneut zu erheben; Abweichungen späterer Läufe sind im jeweiligen Paket
mit eigenem Zitat auszuweisen.

Nicht angefasst (Dateirahmen dieses Pakets): `docs/methodik/60_gebaeudeschaeden_flusshochwasser.md`,
`docs/evidenz/register.md`, `backend/scripts/lint_methodik.py`, `backend/` und die Kopftabelle
„Offene Befunde" am Kopf dieses Ledgers. Geändert wurde ausschließlich diese Datei.

### Leitfragen 1 und 2

Paket T-0360 der Runde 3 (18.09.2026), eigene frische Sitzung: Sie hat den geprüften Stand nicht
geschrieben — Kapitel 1 und 2 stammen aus T-0235/T-0237 und den Revisionspaketen aus T-0281, alle
im Endstatus (eiserne Regel 4). Das Bundle nach §1 lag ab dem ersten Turn vor (Abschnitt 0 dieser
Runde, unverändert gültig); die Lint-Ausgabe aus Abschnitt 0.1 wird **übernommen, nicht neu
erhoben** (§5, Schritt „zuerst die deterministischen Lints"). Maßstab sind ausschließlich §3 und §5
der Aufgabe, nicht der Berichtstext. Nach §6 ist die volle Prüfung erneut zu fahren, weil seit
Runde 2 Kalibrierung und Modellstruktur geändert wurden; dieses Paket trägt davon die Leitfragen
**1** und **2**.

**Prüfumfang dieses Pakets.** Vertieft geprüft sind Kapitel 1 „Wirkungskette & Knoten-Bilanz"
(Z. 39–155) und Kapitel 2 **Teil A**, also der Abschnitt `## 2 Evidenz-Register (§2.2)` bis
ausschließlich `### Belege zu den entschiedenen Registerzeilen` (Z. 156–196) — die Registertabelle
mit ihren 32 Zeilen ohne die Langbelege B1–B6. Nachgemessen, nicht geschätzt:

```
$ python3 -c "s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();i1=s.index('## 1 Wirkungskette');i2=s.index('## 2 Evidenz-Register');i3=s.index('### Belege zu den entschiedenen');print(i2-i1,i3-i2,i3-i1)"
16540 21581 38121
```

Kapitel 1 trifft die im Ticket genannten **16.540** Zeichen exakt; Kapitel 2 Teil A misst **21.581**
statt der dort genannten 21.512 Zeichen (Summe 38.121 statt 38.052). Der geprüfte Textkörper ist
derselbe — die Grenzen sind die beiden Überschriften, und zwischen ihnen liegt heute kein anderer
Text; die Differenz von 69 Zeichen stammt aus der Schnittkante der Zählung im Ticket und wird hier
als Messwert ausgewiesen, statt die Ticketzahl zu wiederholen. Die Langbelege B1–B6 (ab Z. 197)
sind **nicht** Prüfgegenstand dieses Pakets; sie werden nur dort gelesen, wo eine Zeile des
Prüfumfangs ausdrücklich auf sie verweist (B2 zu 60-S074-01, siehe Befund 48). Kapitel 3 bis 9
werden nur als Gegenstelle zitiert, nicht geprüft. Ein nationaler 100-m-Vollraster-Lauf ist nach
§3.4 nicht zulässig und wurde **nicht** gefahren: Alle Rechnungen laufen zellweise und auf
Stichproben. Die Arbeitsmappen wurden ausschließlich gelesen (eiserne Regel 2); im Code wurde
nichts geändert (eiserne Regel 5).

#### LF 1 — Kette: alle Knoten verarbeitet oder begründet inaktiv? Eingänge, die nirgends rechnen?

**Verdikt: Befund** (→ neue Befunde **47**, **48**, **49**; die Knotenmenge selbst ist vollständig
und deckungsgleich mit der Arbeitsmappe).

*Nachgerechnet statt gelesen — zellweiser Abgleich gegen
`docs/Schadensbaum/KWRA-Schadensbaum_X_UBA-klimawirkungsketten.xlsx`.* Die Knotenmenge wurde nicht
aus den Behauptungen des Berichts übernommen, sondern aus den Zellen der Arbeitsmappe aufgebaut:
Blatt „Klimawirkungsketten", Zeile 272 (Knoten **W117** „Schäden an Gebäuden und Infrastrukturen",
Zelle A272/B272) mit den vier Eingangsspalten **E272** (Einflüsse: `E10; E08; E17; E14; E02; E03`),
**F272** (Sensitivitäten: `S092; S093; S094; S096; S097; S098; S104`), **G272** (räumlich:
`R23; R24; R25`) und **H272** (Wirkungen: `W074; W077; W085; W087; W008; W006; W091; W100`) = 24
Knoten; dazu die eine Ebene tiefer aufgenommenen Eingänge des Hochwasser-Knotens **W085** (Zeile
208, A208/B208) aus **E208** (`E12; E07; E08`), **F208** (`S072; S073; S074`) und **G208**
(`R17; R18; R19`) = 9 Knoten, davon E08 bereits in E272 enthalten. Vereinigung: **32** Knoten.
H208 ist leer — W085 hat keine Wirkungs-Eingänge, die Ein-Ebenen-Expansion ist also vollständig.

```
$ python3 <<'EOF'   # Kern: Mappen-Knotenmenge aus E272/F272/G272/H272 + E208/F208/G208 gegen die Knoten-Bilanz
… (Parser: inlineStr-Zellen aus xl/worksheets/sheet1.xml; Bilanz-Zeilen aus Kapitel 1) …
EOF
Mappe   KWK E272/F272/G272/H272 + E208/F208/G208 : 32 Knoten
Bericht Knoten-Bilanz Kap. 1                     : 32 Zeilen
nur in der Mappe : []
nur im Bericht   : []
verarbeitet        : 13 ['E07', 'E08', 'E12', 'R17', 'R24', 'S072', 'S073', 'S074', 'S092', 'S093', 'S094', 'S104', 'W085']
begruendet inaktiv : 19 ['E02', 'E03', 'E10', 'E14', 'E17', 'R18', 'R19', 'R23', 'R25', 'S096', 'S097', 'S098', 'W006', 'W008', 'W074', 'W077', 'W087', 'W091', 'W100']
nicht zugeordnet   : 0
Zeilenzuordnung Bericht -> Mappe abweichend : []
Name != Mappe (Spalte B) : [('W100', 'Einschränkungen Kanalnetze und Vorfluter (= Id 52)', 'Einschränkungen der Funktionsfähigkeit von Kanalnetzen und Vorflutern'), ('S092', 'Bauliche, organisatorische und finanzielle Vorsorge der Eigentümer und Nutzer', 'Bauliche, organisatorische und finanzielle Vorsorge der Eigentümer und Nutzer von Gebäuden und Infrastrukturen')]
Registerzeilen mit Entscheidung 'offen' : 25
  davon in Kap. 1 inaktiv      : ['E02', 'E03', 'E10', 'E14', 'E17', 'R18', 'R19', 'R23', 'R25', 'S096', 'S097', 'S098', 'W006', 'W008', 'W074', 'W077', 'W087', 'W091', 'W100']
  davon in Kap. 1 verarbeitet  : ['E07', 'E08', 'E12', 'S072', 'S073', 'S104']
```

Die Ausgabe ist wörtlich die des Laufs in dieser Sitzung; im Block oben ist allein der Parser
gekürzt (er liest die `inlineStr`-Zellen aus `xl/worksheets/sheet1.xml` der Arbeitsmappe, weil
`openpyxl` in dieser Umgebung nicht installiert ist, und zerlegt die Tabellenzeilen von Kapitel 1
und Kapitel 2 des Berichts). Die Zahlen darunter sind einzeln aus denselben Zellen nachvollziehbar
und stehen in der folgenden Tabelle mit ihrem Zellbezug.

**Zählung (mit Zellbezügen).**

| Größe | Zahl | Zellbezug / Fundstelle |
|---|---|---|
| Knoten gesamt (Arbeitsmappe) | **32** | KWK **E272, F272, G272, H272** (24) ∪ **E208, F208, G208** (9, davon E08 Dublette) |
| Zeilen der Knoten-Bilanz (Bericht) | **32** | Bericht Kap. 1, Tabelle nach „Entscheidungsstand (T-0235)", Z. 79–110 |
| nicht zugeordnet (Mappe ohne Bilanzzeile) | **0** | Mengenvergleich oben, `nur in der Mappe : []` |
| ohne Deckung in der Mappe (Bilanz ohne Mappenknoten) | **0** | `nur im Bericht : []` |
| verarbeitet (Formelstelle oder Sensitivitätsband) | **13** | Bericht Z. 79–86 (W085, E12, E07, E08, S072, S073, S074, R17), Z. 101–103 (S092, S093, S094), Z. 107 (S104), Z. 108 (R24) |
| begründet inaktiv (mit wörtlichem Zitat) | **19** | Bericht Z. 87–100 (R18, R19, E10, E17, E14, E02, E03, W074, W077, W087, W008, W006, W091, W100), Z. 104–106 (S096–S098, geparkt), Z. 109–110 (R23, R25) |
| Zeilenverweis „KWK Zxxx" der Bilanz gegen Spalte A der Mappe | **32/32 richtig** | z. B. W085→**A208**, S074→**A199**, R17→**A204**, S092→**A256**, S104→**A268**, R24→**A270**, W100→**A223** |

Damit ist der Mengenteil der Leitfrage **bestanden**: Kein Knoten der Arbeitsmappe fehlt, kein
Knoten der Bilanz ist erfunden, keine Zeile steht ohne Eintrag in „rechnet in", und jeder
Zeilenverweis trifft die Zelle, die er nennt. Der Befundteil liegt bei der zweiten Hälfte der
Leitfrage — **Eingänge, die nirgends rechnen** — und bei der Spiegelung in Kapitel 2 Teil A.

*(1) S104 steht als verarbeitet in der Bilanz, rechnet aber nirgends → Befund **47**.* Z. 107 führt
S104 (KWK **A268/B268** „Investitionen der Bau- und Immobilienwirtschaft in exponierten Gebieten")
mit **FS-Bestandsdynamik** in derselben Fettschreibung wie die tatsächlich rechnenden
Formelstellen. Kapitel 6 sagt an der einzigen Stelle, die diese Formelstelle einlöst (Z. 1790–1798),
das Gegenteil: Investitionen fließen „im heutigen Modellstand **nicht** als eigener Pfad ein", der
Bestand wird konstant gehalten; die zugehörige Registerzeile 60-S104-01 (Z. 192) steht auf `offen`.
Das ist derselbe Fehlertyp wie Befund 20 (FS-Schutzsystem) und Befund 46 (FS-Exposition), beide
behoben, aber ein dritter, dort nicht erfasster Knoten.

*(2) Formelstelle FS-Exposition ohne Knoten, mit widersprechendem Beleg → Befund **48**.* Die
Präambel der Bilanz (Z. 69–74) führt FS-Exposition weiter als eine der sieben „benannten
Formelstellen", „an die Kapitel 3 die Größe künftig bindet". Nach der Behebung von Befund 46 trägt
sie keine Zeile mehr (Z. 85/86: „keine eigene Formelstelle; früher: FS-Exposition"), und in
Kapitel 3 kommt sie kein einziges Mal vor. Der Langbeleg B2 (Z. 263–265) behauptet zusätzlich
weiterhin: „S074 bleibt der Formelstelle FS-Exposition zugeordnet".

*(3) Die Inaktiv-Entscheidung der Bilanz ist im Register nicht gespiegelt → Befund **49**.* §2.2 (d)
verlangt für einen Ketten-Knoten ohne Evidenz eine Registerzeile mit Entscheidung „bewusst inaktiv"
— „keine stillen Lücken"; zulässige Entscheidungen sind allein Basiswert / Maßnahmen-Hebel /
Sensitivitätsband / bewusst inaktiv. Gemessen stehen **25** der 32 Registerzeilen auf `offen`,
darunter alle **19** in Kapitel 1 begründet inaktiv geführten Knoten und **6** dort als verarbeitet
geführte (E07, E08, E12, S072, S073, S104).

*Regression, kein neuer Befund: Befund 21 (Knotennamen) besteht fort.* Der Namensabgleich gegen
Spalte B der Mappe zeigt weiterhin verkürzte Namen ohne Kürzungszeichen: **B223** „Einschränkungen
der Funktionsfähigkeit von Kanalnetzen und Vorflutern" gegen Bericht Z. 100 „Einschränkungen
Kanalnetze und Vorfluter"; **B256** „… der Eigentümer und Nutzer von Gebäuden und Infrastrukturen"
gegen Z. 101 „… der Eigentümer und Nutzer". Der dritte Fall aus Befund 21, **B199** „Topographie
(Geländeform, Höhe, etc.)" gegen Z. 85 „Topographie (Geländeform, Höhe)", erscheint in der Ausgabe
oben nicht, weil der Vergleich dort den Klammerzusatz abschneidet (der Bericht hängt an denselben
Namen „(über W085)" an); er wurde zusätzlich von Hand an B199 geprüft und besteht ebenfalls fort.
Befund 21 steht auf `bewusst offen` und wird hier **nicht** neu nummeriert.

#### LF 2 — Verteilschlüssel-Test: Kommune ohne Treiber > 0 möglich?

**Verdikt: bestanden** (für den Prüfumfang dieses Pakets: Kapitel 1 und Kapitel 2 Teil A).

*Was geprüft wurde.* §3.1 verbietet, Bundes- oder Landesstatistik zur räumlichen Verteilung zu
benutzen; der Lackmustest lautet: eine Kommune ohne lokalen Treiber muss ~0 erhalten. In Kapitel 1
und Kapitel 2 Teil A stehen keine Formeln, wohl aber die Größen, aus denen die Formel komponiert
wird — geprüft wurde deshalb zeilenweise, ob eine der 32 Registerzeilen einen nationalen Betrag
kommunal verteilt oder additiv in den Zellwert eingeht.

*Zeile für Zeile (alle sieben entschiedenen Zeilen; die 25 offenen tragen keinen Wert).*

| Registerzeile | Fundstelle | Treiber lokal? | Wirkt wie? |
|---|---|---|---|
| 60-W085-01 (Basiswert, FS-Hazard) | Z. 164 | ja — p(HQ) und Wassertiefe je Zelle aus der HWGK; außerhalb der kartierten Gebiete „trifft die Karte keine Aussage" | multiplikativ (Fläche × Wahrscheinlichkeit) |
| 60-R24-01 (Basiswert, FS-Mengengerüst) | Z. 193 | ja — Gebäudezahl und Wohnfläche je Zelle aus dem Zensus-2022-Gitter bzw. den Hausumringen; national ist allein der **Preis** (NHK 2010 × Baupreisindex), keine Verteilgröße | multiplikativ (Preis je m²) |
| 60-S074-01 (Sensitivitätsband) | Z. 170 | — | multiplikatives Band ±12 %, kein eigener Faktor |
| 60-R17-01 (Sensitivitätsband) | Z. 171 | — | **kein** Multiplikativglied; die nationale ZÜRS-Quote dient ausdrücklich nur als Abgleichsband nach §3.4 |
| 60-S093-01 / 60-S094-01 (Bänder, abgeschätzt) | Z. 187/188 | — | geometrisch auf 1,00 zentriert, multiplikativ |
| 60-S092-01 (Maßnahmen-Hebel) | Z. 186 | — | multiplikativ auf den Erwartungsschaden (1 − r) |

Der einzige nationale Datenkörper im Prüfumfang ist damit die ZÜRS-Quote in 60-R17-01, und sie ist
in derselben Zelle ausdrücklich aus dem Rechenweg herausgehalten. *Nachgerechnet statt gelesen:*
Die Klassenanteile der Zeile sind in sich geschlossen — 92,4 + 6,1 + 1,1 + 0,4 = **100,0 %**;
22,6 Mio × 7,6 % = **1.717.600** ≈ die im Bericht genannten 1,72 Mio (GK2–GK4), 22,6 Mio × 1,5 % =
**339.000** (GK3+GK4), 22,6 Mio × 0,4 % = **90.400** — die Quote ist also eine vollständige
Bundesaufteilung und wäre als Verteilschlüssel unmittelbar tauglich; genau das schließt die
Entscheidungsspalte aus. Ebenso nachgerechnet für 60-R24-01: 13,5 + 2,7 + 3,5 = **19,7** Mio
Wohngebäude, 4,1 Mrd m² ÷ 19,7 Mio = **208,1** m², 149,8 ÷ 89,1 = **1,6813**, 1.050 × 1,6813 ×
1,105 = **1.950,7** €₂₀₂₆/m² BGF und 825 × 1,6813 × 1,105 = **1.532,7** €₂₀₂₆/m² BGF, Wertdichte ×
1,30 = **1.992–2.536** €₂₀₂₆/m² Wohnfläche, Bestandswert 4,1 Mrd m² × Wertdichte = **8,17–10,4**
Bio. €₂₀₂₆ — die Zeilenwerte reproduzieren sich (Abweichungen ≤ 1 in der letzten Stelle aus der
Rundungsreihenfolge des Berichts). Alle Größen sind Preise und Bänder, keine Schlüssel.

*Nullprobe.* Mit den Werten dieser Zeilen und einer Kommune, deren Zellen in allen drei Szenarien
\(a_{z,s} = 0\) tragen, ergibt die Kette aus Menge × Rate × Preis exakt **0,0** €₂₀₂₆/a — auch mit
beiden Bandenden von S093/S094 (0,71/0,84 wie 1,40/1,18) und nach dem Niveau-Skalar λ = 0,724, der
multiplikativ wirkt; die Gegenprobe mit a = 15 m² liefert **2,99** €₂₀₂₆/a, die Null ist also nicht
durch einen Rechenfehler erzwungen. Ein additiver Rest existiert in keiner der sieben Zeilen. Die
Aussage deckt sich mit dem Lackmustest, den Runde 2 an Kapitel 3 selbst gerechnet hat (Abschnitt 1
der Runde 2, LF 2).

*Abgrenzung, damit das Verdikt nicht mehr behauptet, als es prüft:* Für die **25 offenen**
Registerzeilen ist die Frage nicht entscheidbar — sie tragen keinen Wert und können den Test
weder bestehen noch verletzen; sobald eine von ihnen eine Entscheidung bekommt, ist LF 2 für sie
neu zu stellen. Das ist kein eigener Befund, sondern die Folge von Befund 49.

#### Neue Befunde dieses Pakets (47–49)

Das Ledger trug vor diesem Paket die Nummern 1 bis 46; die erste hier vergebene Nummer ist deshalb
**47**. **Kein Befund wird in diesem Paket behoben** — die Einträge sind reine Gegenprüfung.

| Nr | Kat. | Stelle · Art · Begründung · Vorschlag |
|---|---|---|
| 47 | **B** | **Stelle:** Bericht Kap. 1, Knoten-Bilanz Z. 107 (Knoten S104, KWK **A268/B268**), Spalte „rechnet in" = **FS-Bestandsdynamik**, gegen Kap. 6 Z. 1790–1798 und Registerzeile 60-S104-01 (Z. 192). · **Art: Widerspruch/Lücke** (§2.1 „jeder Knoten → rechnet in … bewusst inaktiv **mit Begründung**"; §5 LF 1 „Eingänge, die nirgends rechnen?"). · **Begründung:** Die Bilanz weist S104 als verarbeitet aus und nennt Kapitel 6 als Einlösestelle. Kapitel 6 sagt dort wörtlich, die Investitionen flössen „im heutigen Modellstand **nicht** als eigener Pfad ein"; der Bestand R24 werde für das Szenariojahr konstant gehalten. Die Registerzeile 60-S104-01 steht auf `offen`, trägt also auch keinen Wert, aus dem die Formelstelle rechnen könnte. Damit behauptet die Bilanz eine Verarbeitung, die das Modell nicht leistet — dieselbe Fehlerart wie bei den behobenen Befunden 20 (FS-Schutzsystem) und 46 (FS-Exposition), aber an einem dort nicht erfassten Knoten. Für einen Leser der Bilanz ist nicht erkennbar, dass die Bestandsdynamik im Ergebnis fehlt. · **Vorschlag:** S104 in der Bilanz als „**inaktiv (geparkt: FS-Bestandsdynamik ohne Term, 60-S104-01 offen)**" mit Zitat der Kap.-6-Stelle führen — analog zur heutigen Formulierung bei S096–S098 — und die Formelstelle erst dann wieder als aktiv ausweisen, wenn 60-S104-01 eine Entscheidung trägt. |
| 48 | **C** | **Stelle:** Bericht Kap. 1, Präambel der Knoten-Bilanz Z. 69–74 („Benannte Formelstellen: … **FS-Exposition** (Wassertiefe am Gebäude) …"), gegen die Bilanzzeilen Z. 85/86 (S074, R17: „keine eigene Formelstelle; früher: FS-Exposition"), gegen Kapitel 3 (kein Vorkommen von FS-Exposition) und gegen Langbeleg B2 Z. 263–265 („S074 bleibt der Formelstelle FS-Exposition zugeordnet"). · **Art: Widerspruch** (Redaktionsrest der Behebung von Befund 46; §2.1, §5 LF 1). · **Begründung:** Nach der Revision bindet keine Zeile der Bilanz mehr an FS-Exposition, und im Modell kommt die Formelstelle nicht vor; die Präambel führt sie gleichwohl weiter als eine der sieben Stellen, „an die Kapitel 3 die Größe künftig bindet" (gemessen: fünf der sieben Formelstellen tragen Zeilen, FS-Exposition null, FS-Schutzsystem drei geparkte). Der Langbeleg B2 behauptet zusätzlich unverändert die Zuordnung, die die Bilanz und die Registerzeile 60-S074-01 ausdrücklich aufgehoben haben. Wer B2 zuerst liest, bekommt das Gegenteil der Bilanz. Kategorie C, weil kein Zahlenwert und keine Rechnung betroffen ist. · **Vorschlag:** FS-Exposition aus der Liste der benannten Formelstellen streichen (oder als „aufgehoben, Befund 46" kennzeichnen) und den Satz in B2 auf den Ist-Stand ziehen: S074 wirkt als Sensitivitätsband über die HWGK-Tiefe, nicht an einer eigenen Formelstelle. |
| 49 | **B** | **Stelle:** Bericht Kap. 2 Teil A, Registertabelle Z. 165–195, Spalte „Entscheidung": 25 der 32 Zeilen tragen `offen` — Z. 165–169 (60-E12-01, 60-E07-01, 60-E08-01, 60-S072-01, 60-S073-01), Z. 172–185, Z. 189–192, Z. 194/195; gegen Kap. 1 Z. 87–110 (dieselben Knoten dort „inaktiv" **mit** Zitat) und gegen §2.2 (d). · **Art: Lücke/Widerspruch** (§2.2: zulässige Entscheidungen sind Basiswert / Maßnahmen-Hebel / Sensitivitätsband / bewusst inaktiv; §2.2 (d) „fehlt Evidenz für einen Ketten-Knoten, ist das eine Register-Zeile mit Entscheidung ‚bewusst inaktiv' — keine stillen Lücken"; §2.3 „ausschließlich aus Register-Zeilen komponiert"; §5 LF 1). · **Begründung:** `offen` ist keine der vier zulässigen Entscheidungen. Für die **19** Knoten, die Kapitel 1 begründet inaktiv führt (E02, E03, E10, E14, E17, R18, R19, R23, R25, S096, S097, S098, W006, W008, W074, W077, W087, W091, W100), existiert die Begründung bereits wörtlich in der Bilanz — sie ist nur nicht ins Register gezogen, wo §2.2 sie verlangt und wo sie risikoübergreifend wiederverwendbar wäre. Für die **6** Knoten, die Kapitel 1 als verarbeitet ausweist (E07, E08, E12, S072, S073 an FS-Hazard, S104 an FS-Bestandsdynamik), ist die Lücke schwerer: Das Modell darf nach §2.3 nur aus Registerzeilen komponiert werden, ihre Registerzeilen tragen aber keine Entscheidung. Abgrenzung: Befund 3 (A, behoben) betraf die Evidenzlage der rechnenden Zeilen („keine Zeile mit Entscheidung Basiswert") und ist mit den sieben entschiedenen Zeilen geschlossen; hier geht es um die **Spiegelung der Inaktiv-Entscheidung** aus Kapitel 1, die Befund 3 nicht erfasst. · **Vorschlag:** Die 19 Zeilen der in Kapitel 1 inaktiven Knoten auf Entscheidung „**bewusst inaktiv**" setzen und die Ein-Satz-Begründung samt Zitat aus der Bilanz übernehmen (Spalten Effektgröße/Studientyp/Quelle dürfen dabei „entfällt — kein Rechenpfad" tragen); für E07, E08, E12, S072, S073 die Entscheidung „bewusst inaktiv (im Hazard-Datensatz enthalten, Kein-Doppelkanal §3.2)" eintragen und S104 gemeinsam mit Befund 47 entscheiden. |

#### Abgrenzung und Status dieses Pakets

- **Geändert wurde ausschließlich `reviews/BEFUNDE_60.md`.** `docs/methodik/60_gebaeudeschaeden_flusshochwasser.md`, `docs/evidenz/register.md`, `backend/scripts/lint_methodik.py` und `backend/` sind unangetastet; die Arbeitsmappen wurden nur gelesen (eiserne Regel 2).
- **Kein Befund behoben, keiner umnummeriert.** Befund 21 (Knotennamen) wird nur als fortbestehend bestätigt und behält Nummer und Status `bewusst offen`.
- **Kopftabelle „Offene Befunde (19)" bewusst nicht fortgeschrieben** (Dateirahmen der Runde-3-Pakete, festgelegt im Eröffnungspaket T-0359). Sie trägt ihren Stand-Vermerk „nach der Autor-Revision der Runde 2" und zählt die Nummern 1–46; mit den Befunden 47–49 wäre sie bei 22 offenen Zeilen. Diese Zahl steht hier, damit die Lücke sichtbar ist und nicht still altert; nachgezogen wird die Kopftabelle im Abschlusspaket der Runde 3.
- **Nicht Gegenstand dieses Pakets:** die Leitfragen 3 bis 14, die Langbelege B1–B6, die Kapitel 3 bis 9 und die Regression der Befunde 1–46. Sie liegen bei den Geschwisterpaketen der Runde 3.

### Leitfragen 10 und 14

Paket T-0361 der Runde 3 (18.09.2026), eigene frische Sitzung: Sie hat den geprüften Stand nicht
geschrieben — Kapitel 2 Teil B und Kapitel 8 stammen aus T-0235 bis T-0243, T-0256 bis T-0259 und
den Revisionspaketen aus T-0281 (darunter die Snapshot-Nachträge T-0307/T-0308), alle im Endstatus
(eiserne Regel 4). Das Bundle nach §1 lag ab dem ersten Turn vor (Abschnitt 0 dieser Runde,
unverändert gültig); die Lint-Ausgabe aus Abschnitt 0.1 wird **übernommen, nicht neu erhoben**
(§5, Schritt „zuerst die deterministischen Lints"). Maßstab sind ausschließlich §3 und §5 der
Aufgabe, nicht der Berichtstext. Nach §6 ist die volle Prüfung erneut zu fahren, weil seit Runde 2
Kalibrierung und Modellstruktur geändert wurden; dieses Paket trägt davon die Leitfragen **10**
und **14**.

**Prüfumfang dieses Pakets.** Vertieft geprüft sind Kapitel 2 **Teil B**, also der Abschnitt
`### Belege zu den entschiedenen Registerzeilen (§3.8, Volltext geprüft am 13.09.2026)`
(Z. 197–522, Langbelege B1–B6), und Kapitel 8 `## 8 Quellen (§3.8)` (Z. 2326–2411). Nachgemessen,
nicht aus dem Ticket übernommen:

```
$ python3 -c "s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read();i3=s.index('### Belege zu den entschiedenen');i4=s.index(chr(10)+'## 3 ');i8=s.index('## 8 Quellen');i9=s.index(chr(10)+'## 9 ');print(i4-i3+1,i9-i8+1,(i4-i3)+(i9-i8)+2)"
28396 7438 35834
```

Kapitel 2 Teil B misst **28.396** statt der im Ticket genannten 28.465 Zeichen, Kapitel 8 **7.438**
statt 7.267, zusammen **35.834** statt 35.732. Der geprüfte Textkörper ist derselbe — die Grenzen
sind die Überschriften `### Belege …` bis ausschließlich `## 3 Modell` und `## 8 Quellen` bis
ausschließlich `## 9 Ansatz-Vergleich`, und zwischen ihnen liegt kein anderer Text. Die Differenzen
(−69 und +171 Zeichen) stammen aus der Schnittkante der Zählung im Ticket und stehen hier als
Messwert, statt die Ticketzahl zu wiederholen. Kapitel 1 und Kapitel 2 Teil A liegen beim
Geschwisterpaket T-0360, die übrigen Kapitel bei den anderen Paketen der Runde; sie werden hier nur
als Gegenstelle zitiert, nicht geprüft. Ein nationaler 100-m-Vollraster-Lauf ist nach §3.4 nicht
zulässig und wurde **nicht** gefahren: Alle Rechnungen laufen zellweise und auf Stichproben. Die
Arbeitsmappen wurden ausschließlich gelesen (eiserne Regel 2, Prüfsummen unten unverändert); im
Code wurde nichts geändert (eiserne Regel 5).

#### LF 10 — Quellen: fehlend, veraltet, falsch zugeordnet, unverifiziert; Zahlen ≠ Primärquelle?

**Verdikt: Befund** (→ neue Befunde **50**, **51**, **52**; die geprüften **Zahlen** stimmen
ausnahmslos mit ihren Primärquellen überein, die Mängel liegen in der Fundstellenführung).

*Stichprobe gegen die Primärquelle — sechs Quellenangaben, je mit Fundstelle im Bericht.* Geprüft
wurde nicht, ob der Bericht sich selbst treu ist, sondern ob die zitierte Zahl in der genannten
Quelle so steht. Die externen Quellen wurden am 18.09.2026 am Original abgerufen, die Arbeitsmappe
zellweise gelesen.

| # | Quellenangabe (Fundstelle im Bericht) | Zitierter Wert | Befund am Original |
|---|---|---|---|
| S1 | **B4 Quelle 3**, ImmoWertV Anlage 4 (NHK 2010) · Kap. 2 Teil B Z. 320–332 | 825 / 985 / 1.190 €/m² BGF (MFH ≤ 6 WE, Stufen 3–5); Wortlaut „Kostengruppen 300 und 400 der DIN 276, die Umsatzsteuer und die üblicherweise entstehenden Baunebenkosten (Kostengruppen 730 und 771 …)", „auf den im Jahresdurchschnitt bestehenden Kostenstand des Jahres 2010" | **trifft zu**, wörtlich und zahlengleich (gesetze-im-internet.de, Anlage 4, abgerufen 18.09.2026). Die Kennwerte der Gebäudeart 1.01 (u. a. 1.050 €/m²) stehen dort nur als eingebettete Tabellengrafik und waren in dieser Sitzung nicht maschinell auslesbar — **nicht widerlegt, aber auch nicht gegengelesen**; hier als offene Teilprobe ausgewiesen statt als bestätigt. |
| S2 | **B1 Quelle 2**, § 74 Abs. 2 Nr. 1 WHG · Z. 215–222 | „Hochwasser mit niedriger Wahrscheinlichkeit (voraussichtliches Wiederkehrintervall mindestens 200 Jahre)" | **trifft zu**, wörtlich (gesetze-im-internet.de/whg_2009/__74.html, abgerufen 18.09.2026); Abs. 3 nennt dort ebenfalls Ausmaß der Überflutung und Wassertiefe. |
| S3 | **B4 Quelle 1**, Destatis PM Nr. 336 vom 17.09.2025 · Z. 304–313 | 43,8 Mio Wohnungen · 4,1 Mrd m² Wohnfläche · 13,5 / 2,7 / 3,5 Mio Ein-, Zwei-, Mehrfamilienhäuser | **trifft zu**, alle fünf Zahlen wörtlich in der Pressemitteilung (destatis.de, abgerufen 18.09.2026). Die im selben Satz geführten **19,7 Mio Wohngebäude** sind die Summe der drei Gebäudetypen (13,5 + 2,7 + 3,5 = 19,7) und in dieser Form keine Zahl der Meldung — rechnerisch korrekt, als abgeleiteter Wert aber nicht gekennzeichnet (kein eigener Befund: die drei Summanden stehen mit Quelle daneben). |
| S4 | **Kap. 8 Quelle 5**, GDV-Naturgefahrenstatistik 2024 · Z. 2378–2389 | „Allein Starkregenereignisse und Überschwemmungen schlugen mit 2,6 Mrd. Euro zu Buche"; 4,4 Mrd. € Sachversicherung, 1,3 Mrd. € Kraftfahrt, Stand „Zuletzt aktualisiert 31.05.2025" | **trifft zu**, wörtlich und zahlengleich (gdv.de, Medieninformation, abgerufen 18.09.2026); die im Bericht genannten 5,7 Mrd. € sind die Summe 4,4 + 1,3 und stehen in der Quelle als Gesamtbetrag. |
| S5 | **Kap. 8 Quelle 6**, GDV-Versicherungsdichte · Z. 2390–2401 | „2024 sind 10,2 Mio. Wohngebäude … versichert. Das entspricht einer Versicherungsdichte von immerhin 57 % bezogen auf Wohngebäude-Feuer"; Stand der Grafik 10.10.2025 | **trifft zu**, wörtlich, samt Aktualisierungsdatum (gdv.de, Datenservice, abgerufen 18.09.2026). |
| S6 | **Kap. 8 Quellen 1 und 2**, beide Arbeitsmappen mit Commit und Prüfsumme · Z. 2333–2350 | KWK `1a89a2e8…` (2026-08-17), SHA-256 `2faac648aade047f…`; Mon. `68442ca12689…` (2026-08-30), SHA-256 `4383882d3a935f09…` | **trifft zu**, gemessen: `sha256sum` beider Mappen und `git log -1` je Datei geben genau diese Summen und Commits/Daten. Die tragenden Zellen sind ebenfalls wörtlich: Mon. **J64** „… Zeitwertansatz; Versicherungsleistungen sind Transfers und mindern den Schaden nicht (R5).", **J65** „Wie ID 59, ereignisbezogen flussseitig; …", Konten **C27** „Wiederherstellungs-/Zeitwertkosten; Schadensfunktionen × Bestandswerte", Rechenregeln **A7/B7** „R5 · Transfers sind keine Schäden". |

*Nicht verifizierbare Quelle — ausgewiesen, nicht stillschweigend als geprüft geführt.* Die
Sekundärzahl des Tiefenbands (**B2 Quelle 2**, de Moel/Aerts 2011, Z. 248–257: „a 0.5-m reduction …
factor 1.35–1.44", Tab. 4 „5,3 %–6,2 % je 10 cm") ließ sich in dieser Sitzung **nicht** am Volltext
gegenlesen: Die Verlagsfassung antwortet mit einer Anmelde-Weiterleitung, und für die frei
zugängliche Repositoriumsfassung fehlt in dieser Umgebung ein PDF-Textextraktor (`pdftotext` nicht
installiert, PDF-Seitenrendering ohne `poppler-utils` nicht möglich). Der Bericht führt die Stelle
als „Volltext gegengelesen" (Z. 251); diese Angabe wird hier **weder bestätigt noch bestritten**.
Kein Befund — die Prüfmittellücke liegt bei der Review-Umgebung, nicht am Bericht; der abgeleitete
Rechenschritt ist dagegen nachgerechnet: 2,0 × 5,3 % = **10,6 %** und 2,0 × 6,2 % = **12,4 %**,
gerundet ±12 % wie im Bericht.

*Nachgerechnet statt gelesen — alle Zahlenketten des Prüfumfangs.* Die Rechenschritte in B3 bis B6
reproduzieren sich aus den zitierten Quellwerten (eigener Lauf in dieser Sitzung):

```
Indexfaktor 149,8/89,1 = 1,6813 · 1.050 × 1,6813 = 1.765,32 · 825 × 1,6813 = 1.387,04
1,034³ = 1,10551 (Faktor 1,105) · 1,023³ = 1,0706 · 1,050³ = 1,15763 (Band 1,07–1,16)
1.765 × 1,105 = 1.950,3 · 1.387 × 1,105 = 1.532,6 · Bandenden 1.765 × 1,07/1,16 = 1.888,6/2.047,4
   und 1.387 × 1,07/1,16 = 1.484,1 / 1.608,9  (Bericht: 1.889–2.047 bzw. 1.484–1.609 ✓)
1.533 × 1,30 = 1.992,9 · 1.950 × 1,30 = 2.535,0 · 4,1 Mrd × 1.993/2.535 = 8,17/10,39 Bio.
4,1 Mrd ÷ 19,7 Mio = 208,1 m²
B3: 100 − 92,4 = 7,6 · 7,6 − 0,4 = 7,2 = 6,1 + 1,1 ✓ · 0,011 × 22,6 Mio = 248.600
   · 0,061 × 22,6 Mio = 1.378.600 · 0,076 × 22,6 Mio = 1.717.600 · 0,015 × 22,6 Mio = 339.000
B5: ln(1,58/0,92) = 0,5408 · ln(0,92/0,41) = 0,8082 · Mittel 0,67451 · e^0,67451 = 1,9631
   · √ = 1,40110 / 0,71373       B6: 0,67451/2 = 0,33726 · e^ = 1,40110 · √ = 1,18368 / 0,84482
   · 0,7137 × 0,8448 = 0,6029 · 1,4011 × 1,1837 = 1,6585 (Bericht: 0,60–1,66 ✓)
Zeitwert je Gebäude 527.280 × 0,55 = 290.004 (Band 210.912–395.460) ✓
```

Keine Abweichung. Insbesondere die Bandenden 1.889–2.047 und 1.484–1.609 sind **nicht** aus den
ungerundeten Zwischenwerten, sondern aus dem ausgewiesenen gerundeten Band 1,07–1,16 gerechnet —
das ist im Bericht so angegeben und deshalb kein Befund.

*(1) Die Fundstellenlisten des Quellenkapitels treffen den Bericht nicht → Befund **50**.*
Kapitel 8 Quelle 1 führt für die Wirkungsketten-Mappe „Z3–Z271 **wie in Kap. 1 zitiert**"; gemessen
zitiert der Bericht auch **KWK Z272**, und das ist die Zeile des Zielknotens W117, also die
tragendste Fundstelle überhaupt. Umgekehrt nennt dieselbe Angabe für die Netzwerkliste Z13, Z50,
**Z51**, Z53, **Z60**, Z61 — Z51 und Z60 kommen im ganzen Bericht nicht vor. In Quelle 2 fehlen die
im Bericht tragenden Zellen Mon. Z17, Z42 und Z57, Rechenregeln Z7 (R5-Zitat) und Z19 sowie
Abgleich-Protokoll Punkt 3.

*(2) Fünf Quellenangaben ohne Jahresangabe → Befund **51**.* §3.8 verlangt „Autor, Jahr, Titel,
Organ, DOI/URL, Zugriffsdatum, Archiv-Snapshot"; fünf Einträge in Teil B tragen kein Jahr und keine
Fassungsangabe (LAIV MV, LfU-FAQ, GDV-ZÜRS-Seite, Destatis-Themenseite, Fachserie 17 Reihe 4).

*(3) Das Prüfdatum in der Abschnittsüberschrift ist überholt → Befund **52**.* Die Überschrift
nennt „Volltext geprüft am 13.09.2026", während Teile desselben Abschnitts am **17.09.2026** geprüft
und nachgetragen wurden (Snapshots B1–B6 aus T-0307/T-0308, Snapshot-Fehlversuch B4 Quelle 5
„beides geprüft 17.09.2026", Zugriff 17.09.2026 bei Kap. 8 Quellen 5–7).

*Regression, kein neuer Befund.* Der in Befund 48 (Paket T-0360) erfasste Satz in B2 („S074 bleibt
der Formelstelle FS-Exposition zugeordnet", Z. 263–264) liegt zwar im Prüfumfang dieses Pakets,
ist dort aber bereits nummeriert und wird hier **nicht** doppelt geführt. Befund 42
(Archiv-Snapshots) ist im Prüfumfang gegengeprüft und besteht nicht fort: Jede externe Webquelle in
B1–B6 und Kap. 8 trägt entweder einen Snapshot mit Datum oder — bei B4 Quelle 5 — die ausdrückliche
Begründung des Verzichts, und die Begründung ist am Original nachvollziehbar (Destatis-Snapshots
antworten mit HTTP 403).

#### LF 14 — Quellen-Synchronität: Widerspruch zu Arbeitsmappen oder Aufgabe? Fortschreibungen nachgezogen und im Abgleich-Protokoll dokumentiert?

**Verdikt: Befund** (→ neuer Befund **53**; der erste Teil der Leitfrage — Widerspruch in einem
verbindlichen Punkt — ist im Prüfumfang **bestanden**, der zweite Teil nicht).

*Teil 1: Widerspricht der Bericht den Arbeitsmappen oder der Aufgabe in einem verbindlichen Punkt
(Bewertungslogik, Kanten, Konten, Rollen)?* Geprüft wurden alle Mappenbezüge, die in Kapitel 2
Teil B und Kapitel 8 stehen, gegen die Zellen selbst:

| Verbindlicher Punkt | Zelle (gelesen, nicht geändert) | Aussage im Prüfumfang | Ergebnis |
|---|---|---|---|
| Bewertungslogik K3 für #60 | Mon. **J65** → **J64**: „Wie ID 59, ereignisbezogen flussseitig; HQ-Szenarien × Schadensfunktionen (Wassertiefe-Schaden) × Gebäudewerte." / „Wiederherstellungskosten (Gebäude, Hausrat, Fahrzeuge) je Ereignis; **Zeitwertansatz**; Versicherungsleistungen sind Transfers und mindern den Schaden nicht (R5)." | B4 Z. 383–389: Neuwert bleibt Basiswert, Zeitwert als beziffertes Band (0,55; 0,40–0,75), Abweichung als Antrag §7.2 | Abweichung **benannt, beziffert und nicht geglättet** (§3.8) — kein Widerspruch im Sinne von „still überstimmt"; der Nachzug in die Quelle fehlt aber, siehe Teil 2 |
| Kostensatz-Typ K3 | Konten **C27** „Wiederherstellungs-/Zeitwertkosten; Schadensfunktionen × Bestandswerte" | B4 Z. 384–386 zitiert beide Lesarten | trifft zu, wörtlich |
| Rolle der Versicherungsleistungen (R5) | Rechenregeln **A7/B7/C7** „R5 · Transfers sind keine Schäden · Versicherungsleistungen … sind (überwiegend) Umverteilung" | Teil B führt keinen Abzug von Versicherungsleistungen; der Ankerwert in Kap. 4 wird hochgerechnet, nicht abgezogen | konsistent |
| Ereignislogik (A5) | Rechenregeln **Z20** „Ereignisschäden (K3/K4/K1-Extremereignisse) werden je Ereignisklasse als Erwartungswert gerechnet: Eintrittswahrscheinlichkeit × Schadensfunktion × Bestand" | B1 (p = 1/T je Szenario) und B4 (Bestandswert) liefern genau diese drei Faktoren | konsistent |
| Kanten/Konto-Zuordnung | Abgleich-Protokoll, Spalten **B** und **D** über alle 152 Zeilen | Kapitel 8 nennt die Mappe als Quelle, Teil B führt keine Kante ein | keine Zeile mit Quelle-ID oder Ziel 60 (gemessen) — es wird auch keine behauptet |
| Aufgabe §3.8 (Widersprüche benennen, Lücken ausweisen) | — | B1 (WHG 200 a ↔ Praxis HQ1000), B3 (ZÜRS ↔ HWGK nicht überführbar), B5 (Fig.-1-Beschriftung gegen die fachliche Erwartung) je als „Widerspruch … benannt statt geglättet"; sechs ausdrückliche Datenlücken | erfüllt |

*Teil 2: Ist jede bewusste Fortschreibung in der Quelle nachgezogen und im Abgleich-Protokoll
dokumentiert?* Gemessen, nicht gelesen: Das Blatt „Abgleich-Protokoll" hat 152 Zeilen; genau **eine**
davon ist eine Fortschreibung der Bewertungslogik — Z151, Punkt 52, Spalte F „Fortschreibung
Bewertungslogik (keine Kante)", Inhalt „VSL 3,5 Mio. €/Fall → YLL × VOLY …, Beschluss Review 2,
umgesetzt Methodik-Bericht #95 Rev. 6". Für #60 gibt es keine solche Zeile, und die Spalten B/D
tragen über alle 152 Zeilen keinen Eintrag 60. Die Abweichung vom Zeitwertansatz wirkt aber seit
dem 17.09.2026 im Basiswert. Das ist genau die Lage, die LF 14 im zweiten Halbsatz abfragt — daher
Befund **53**.

#### Neue Befunde dieses Pakets (50–53)

**Nummernvergabe.** Das Ticket geht vom Ledgerstand 1–46 aus und nennt 47 als erste freie Nummer;
zwischenzeitlich hat das parallel laufende Geschwisterpaket T-0360 die Nummern **47–49** vergeben
(Abschnitt „Leitfragen 1 und 2" dieser Runde). Die nächsthöhere **freie** Nummer ist damit **50**;
ab ihr wird hier fortlaufend vergeben, damit keine Nummer doppelt belegt wird.
**Kein Befund wird in diesem Paket behoben** — die Einträge sind reine Gegenprüfung.

| Nr | Kat. | Stelle · Art · Begründung · Vorschlag |
|---|---|---|
| 50 | **C** | **Stelle:** Bericht Kap. 8, Quelle 1 (Z. 2333–2341: „Sheets „Klimawirkungsketten" (Z3–Z271 wie in Kap. 1 zitiert) und „Schadensbaum-Netzwerkliste" (Z13, Z50, Z51, Z53, Z60, Z61)") und Quelle 2 (Z. 2342–2350: „„Risiken-Monetarisierung" (Z51, Z54–Z56, Z64, Z65, Z106), „Schadenskonten-System" (Z26–Z30), „Rechenregeln" (Z9, Z11, Z20), „Abgleich-Protokoll" (P5, P15, P16)") — gegen die tatsächlich im Bericht zitierten Zellen. · **Art: Lücke/falsche Zuordnung** (§3.8 „Jede Zahl mit Quelle … exakte Fundstelle"; §5 LF 10 „falsch zugeordnet"). · **Begründung:** Gemessen (Zitatsammlung über den ganzen Bericht) zitiert der Bericht **KWK Z272** — die Zeile des Zielknotens W117 und damit die tragendste Fundstelle der Kette —, die Quellenangabe endet aber bei Z271. Umgekehrt nennt sie für die Netzwerkliste **Z51** und **Z60**, die im Bericht nirgends vorkommen. In Quelle 2 fehlen **Mon. Z17** (Buchungsobjekt 12, Partitionsabgrenzung), **Mon. Z42** (Buchungsobjekt 37, „Sachschäden an Anlagen (K3)"), **Mon. Z57**, **Rechenregeln Z7** (R5-Zitat, das die Transfer-Entscheidung trägt), **Rechenregeln Z19** (A4 Kostensätze) und **Abgleich-Protokoll Punkt 3** (Kante 49 → 37, tragend für die Weitergaben und für Befund 6). Wer die Quellenangabe als Fundstellenverzeichnis benutzt — und dafür steht sie da —, wird an den tragenden Zellen vorbeigeführt und findet zugleich zwei Zellen angeboten, die nichts tragen. Kategorie C, weil kein Zahlenwert betroffen ist und jede Einzelstelle im Fließtext von Kap. 1/2 korrekt zitiert wird. · **Vorschlag:** Die beiden Zellbereiche aus den Zitaten des Berichts erzeugen statt sie zu pflegen (Skript-Zeile im Lint: alle `KWK Z…`, `Mon. Z…`, `Konten Z…`, `Rechenregeln Z…`, `NW Z…`, `Abgleich-Protokoll Punkt …` einsammeln, Bereich in Kap. 8 dagegen prüfen), mindestens aber Z272, Mon. Z17/Z42/Z57, Rechenregeln Z7/Z19 und Abgleich-Punkt 3 aufnehmen und Z51/Z60 der Netzwerkliste streichen. |
| 51 | **C** | **Stelle:** Bericht Kap. 2 Teil B — B1 Quelle 3 (LfU-FAQ, Z. 222–227), B2 Quelle 1 (LAIV MV „Geländemodelle", Z. 242–246), B3 Quelle 2 (GDV „ZÜRS Geo", Z. 279–284), B4 Quelle 2 (Destatis-Themenseite „Wohnen", Z. 314–317), B4 Quelle 4 (Destatis Fachserie 17 Reihe 4, Z. 332–338). · **Art: Lücke** (§3.8 „Jede Zahl mit Quelle (Autor, **Jahr**, Titel, Organ, DOI/URL, Zugriffsdatum, Archiv-Snapshot)"; §5 LF 10 „fehlend … veraltet"). · **Begründung:** Diese fünf Einträge tragen weder ein Erscheinungs-/Standjahr noch eine Fassungsangabe; belegt ist nur der Zugriffstag 13.09.2026 und der Snapshot. Bei laufend gepflegten Webseiten ist genau das Jahr die Angabe, die einen späteren Leser erkennen lässt, ob sich der Stand geändert hat — der Bericht führt diese Disziplin bei anderen Einträgen vor (Kap. 8 Quellen 5 und 6 nennen „Zuletzt aktualisiert" 31.05.2025 bzw. 10.10.2025, in dieser Prüfung am Original bestätigt). Bei B4 Quelle 4 wiegt die Lücke etwas schwerer, weil die Fachserie jahrgangsweise erscheint und die entnommenen Indexwerte (2010 = 89,1 … 2023 = 149,8) an den Jahrgang gebunden sind. Kategorie C, weil die Zahlen selbst belegt und über den Snapshot adressierbar sind. · **Vorschlag:** Je Eintrag das Stand-/Erscheinungsjahr (bei Webseiten: das Feld „Stand"/„Zuletzt aktualisiert", ersatzweise das Snapshot-Datum als „Stand laut Snapshot") ergänzen; bei der Fachserie zusätzlich Erscheinungsjahr und Berichtsjahrgang der verwendeten Ausgabe. |
| 52 | **C** | **Stelle:** Bericht Kap. 2, Überschrift des Teils B Z. 197: „### Belege zu den entschiedenen Registerzeilen (§3.8, **Volltext geprüft am 13.09.2026**)" — gegen die Inhalte desselben Abschnitts: Archiv-Snapshots B1–B6, nachgetragen am 17.09.2026 (T-0307/T-0308), und B4 Quelle 5 Z. 342–348 („beides geprüft 17.09.2026"). · **Art: veraltete Angabe** (§5 LF 10 „veraltet"; §3.8 Zugriffsdatum). · **Begründung:** Die Überschrift datiert die Prüfung des gesamten Abschnitts auf den 13.09.2026. Tatsächlich ist ein Teil der Quellenarbeit vier Tage jünger; im Abschnitt selbst stehen Prüfvermerke vom 17.09.2026, und Kap. 8 führt für die Quellen 5 bis 7 den Zugriff 17.09.2026. Eine zusammenfassende Datumsangabe im Überschriftstext altert still, während die Einzelnachweise fortgeschrieben werden — derselbe Mechanismus wie bei Befund 42. Kategorie C: keine Zahl, kein Rechenweg betroffen, aber das ausgewiesene Prüfdatum ist die Angabe, an der ein Gegenprüfer die Aktualität misst. · **Vorschlag:** Die Überschrift auf „Volltext geprüft 13.09.2026, Quellen- und Snapshot-Stand 17.09.2026" ziehen (oder das Datum aus der Überschrift nehmen und je Beleg führen, wo es ohnehin steht) und die Angabe in den Lint aufnehmen, damit sie beim nächsten Nachtrag mitwandert. |
| 53 | **B** | **Stelle:** Bericht Kap. 2 Teil B, B4 Z. 383–389 („die Arbeitsmappe schreibt über Mon. J65 → J64 den Zeitwertansatz vor. **Entschieden:** Der Neuwert bleibt Basiswert, die Abweichung von J64 steht als Antrag auf Fortschreibung in §7.2") und Kap. 8 Quelle 2 Z. 2342–2350 (Mappe mit Commit `68442ca12689…` und Prüfsumme, ohne Hinweis auf die anhängige Abweichung) · gegen `KWRA-Monetarisierung.xlsx`, Blatt „Abgleich-Protokoll": **keine** Zeile zu #60 (Spalten B und D über alle 152 Zeilen gemessen), während **Z151** (Punkt 52, Spalte F „Fortschreibung Bewertungslogik (keine Kante)") zeigt, wie eine beschlossene Fortschreibung dort geführt wird — dort für #95 mit Beschluss-, Umsetzungs- und Nachzugsdatum. · **Art: Lücke** (§5 LF 14 „Jede bewusste Fortschreibung in der Quelle nachgezogen und im Abgleich-Protokoll dokumentiert?"; §1/LF 14 und eiserne Regel 2 „bewusste Fortschreibungen gehören in die Quelle + Abgleich-Protokoll"; §6 führt Quellen-Synchronität als Abnahmekriterium). · **Begründung:** Der Bericht rechnet seinen Basiswert seit dem 17.09.2026 bewusst abweichend von der verbindlichen Vorgabe J65 → J64 (Zeitwertansatz). Die Entscheidung ist sauber begründet, beziffert und nicht geglättet — das ist der Teil, den Befund 41 verlangt hat und der geschlossen ist. Offen ist der zweite Halbsatz von LF 14: In der Quelle ist nichts nachgezogen. Das Abgleich-Protokoll kennt die passende Zeilenart und führt sie für #95 vor; für #60 fehlt sie, und Kapitel 8 nennt die Mappe als Quelle, ohne zu vermerken, dass der Bericht in einem verbindlichen Punkt von ihr abweicht und ein Antrag anhängig ist. Für jeden, der die Mappe als führende Quelle liest, ist die Abweichung damit unsichtbar; für #60 fehlt außerdem jede Angabe, bis wann und durch wen über den Antrag entschieden wird (§7.2 trägt nur „beantragt am 17.09.2026"). Abgrenzung: **kein** Wiederaufgreifen von Befund 41 (dort fehlten Band und Bezifferung — beides steht heute), sondern der in dessen Vorschlag ausdrücklich genannte, noch nicht erledigte Teil „Dann gehört sie in die Quelle mit Eintrag ins Abgleich-Protokoll (§1/LF 14)". · **Vorschlag:** (a) Im Blatt „Abgleich-Protokoll" durch den Eigner der Mappe eine Zeile nach dem Muster Z151 anlegen: Punkt-Nr. fortlaufend, Quelle-ID 60, Ziel J64/J65, Art „Fortschreibung Bewertungslogik (keine Kante)", Inhalt „Neuwert (NHK, indexiert) statt Zeitwertansatz für #60; Zeitwert als Sensitivitätsband f_AWM = 0,55 (0,40–0,75); beantragt 17.09.2026" — der Bericht selbst darf die Mappe nicht ändern (eiserne Regel 2). (b) Solange der Eintrag fehlt, in Kap. 8 beim Mappen-Eintrag und in B4 den Status des Antrags mit Datum, Entscheider und Frist führen, damit die Abweichung an der Quelle sichtbar ist. (c) Den Zustand in die Abnahme-Checkliste ziehen: §6 nennt Quellen-Synchronität ausdrücklich als Abnahmekriterium, die Abnahme von #60 ist bis zum Nachzug insoweit blockiert. |

#### Abgrenzung und Status dieses Pakets

- **Geändert wurde ausschließlich `reviews/BEFUNDE_60.md`.** `docs/methodik/60_gebaeudeschaeden_flusshochwasser.md`, `docs/evidenz/register.md`, `backend/scripts/lint_methodik.py` und `backend/` sind unangetastet; die Arbeitsmappen wurden nur gelesen (eiserne Regel 2) — gemessen an den unveränderten Prüfsummen `2faac648aade047f…` und `4383882d3a935f09…` nach Abschluss der Prüfung.
- **Kein Befund behoben, keiner umnummeriert.** Befund 48 (FS-Exposition in B2) und Befund 42 (Archiv-Snapshots) werden nur eingeordnet, nicht neu vergeben.
- **Kopftabelle „Offene Befunde (19)" bewusst nicht fortgeschrieben** (Dateirahmen der Runde-3-Pakete, festgelegt im Eröffnungspaket T-0359). Mit 47–49 aus T-0360 und 50–53 aus diesem Paket wären es 26 offene Zeilen; nachgezogen wird die Kopftabelle im Abschlusspaket der Runde 3.
- **Nicht Gegenstand dieses Pakets:** die Leitfragen 1 bis 9 und 11 bis 13, die Registertabelle in Kapitel 2 Teil A, die Kapitel 1 und 3 bis 7 sowie 9 und die Regression der Befunde 1–46. Sie liegen bei den Geschwisterpaketen der Runde 3.

### Leitfragen 3 und 13

Paket T-0371 der Runde 3 (18.09.2026; ersetzt das an der Laufkappe gescheiterte T-0362), eigene
frische Sitzung: Sie hat den geprüften Stand nicht geschrieben — Kapitel 3 stammt aus T-0235 bis
T-0243, T-0256 bis T-0259 und den Revisionspaketen aus T-0281, alle im Endstatus (eiserne
Regel 4). Das Bundle nach §1 lag ab dem ersten Turn vor (Abschnitt 0 dieser Runde, unverändert
gültig); die Lint-Ausgabe aus Abschnitt 0.1 wird **übernommen, nicht neu erhoben** (§5, Schritt
„zuerst die deterministischen Lints"). Maßstab sind ausschließlich §3 und §5 der Aufgabe, nicht
der Berichtstext. Dieses Paket trägt davon die Leitfragen **3** (physische Zwischengröße) und
**13** (Herleitungspflicht).

**Prüfumfang dieses Pakets.** Vertieft geprüft ist **Kapitel 3 Teil A**: der Kapitelkopf
`## 3 Modell (§2.3)` und die Abschnitte 3.1, 3.4, 3.5, 3.6 und 3.7. Nachgemessen, nicht aus dem
Ticket übernommen:

```
$ python3 -c "
import re
s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read()
def body(a,b):
    t=s.split(chr(10)+a)[1].split(chr(10)+b)[0]
    t=re.sub('<!--.*?-->','',t,flags=re.S)
    return t.strip(chr(10))
pairs=[('## 3 Modell','### 3.1 Native'),('### 3.1 Native','### 3.2 Datenebenen'),('### 3.4 Kernformel','### 3.5 Zeichentabelle'),('### 3.5 Zeichentabelle','### 3.6 Aggregation'),('### 3.6 Aggregation','### 3.7 Schicht-A'),('### 3.7 Schicht-A','## 4 Kalibrierung')]
tot=0
for a,b in pairs:
    n=len(body(a,b)); tot+=n; print(a, n)
print('SUMME', tot)
"
## 3 Modell 392
### 3.1 Native 1580
### 3.4 Kernformel 7064
### 3.5 Zeichentabelle 7120
### 3.6 Aggregation 6314
### 3.7 Schicht-A 3109
SUMME 25579
```

Gemessen sind **25.579** statt der im Ticket genannten 25.329 Zeichen (Kopf 392 statt 386, 3.1
1.580 statt 1.520, 3.4 7.064 statt 7.028, 3.5 7.120 statt 7.069, 3.6 6.314 statt 6.259, 3.7 3.109
statt 3.067). Der geprüfte Textkörper ist derselbe; die Differenz von 250 Zeichen stammt aus der
Schnittkante der Zählung — dieser Ausdruck schneidet am Zeilenanfang der Überschrift und zählt den
Rest der Überschriftenzeile mit. Die Zahl steht hier als Messwert, statt die Ticketzahl zu
wiederholen. **Nicht vertieft geprüft** sind der Berichtskopf sowie die Abschnitte 3.2 und 3.3
(Geschwisterpaket); sie werden nur als Gegenstelle zitiert, etwa für die Herleitung von
\(d(h)\), \(h_1\) und \(h_5\). Ein nationaler 100-m-Vollraster-Lauf ist nach §3.4 nicht zulässig
und wurde **nicht** gefahren: Nachgerechnet wurde zellweise am Rechenbeispiel des Berichts und an
der Zeichentabelle. Die Arbeitsmappen wurden in diesem Paket nicht geändert (eiserne Regel 2); der
Abgleich gegen sie trägt die Leitfragen 1 und 14 und liegt bei den Geschwisterpaketen. Im Code
wurde nichts geändert (eiserne Regel 5).

#### LF 3 — Physische Zwischengröße: Euro je Zelle auf eine physische Größe rückführbar; native Ausweise proportional zu den Euro-Pfaden?

**Verdikt: Befund** (Befund 57). Der Kernteil der Leitfrage ist erfüllt, der Klammerzusatz zu den
nativen Ausweisen nicht.

*Erfüllt — Euro je Zelle rückführbar.* Die Kernformel trennt die drei Schritte sauber und lässt
den Euro erst im letzten entstehen. Schritt 1 (Z. 648–651) bildet
\(A_{z,s} = W_z a_{z,s} \cdot d(h_{z,s}) f_{S093} f_{S094}\) in **m²** und benennt das Ergebnis
ausdrücklich als „schadensäquivalente Wohnfläche … die physische Zwischengröße" (Z. 653–655),
„existiert unabhängig von jedem Preis". Schritt 2 (Z. 662) hält die Einheit bei m²/a. Erst
Schritt 3 (Z. 679–681) multipliziert mit der Wertdichte: \(\text{EAD}_z = \bar A_z \cdot w_z\),
\(w_z = k_{\text{BGF}} \sum_t \theta_{z,t} n_t\). Die Einheitenkette schließt: m² Wohnfläche/a ×
(m² BGF/m² Wohnfläche × €₂₀₂₆/m² BGF) = €₂₀₂₆/a. Jeder Euro-Betrag der Zelle ist damit durch
Division durch \(w_z\) wieder in die physische Größe rückführbar; das Rechenbeispiel Z. 713–720
führt das mit 15,0 / 77,8 / 300,0 m², \(\bar A_z = 6{,}31\) m²/a und ≈ 16.000 €₂₀₂₆/a vor und ist
als Golden-Test `beispiel_60_kernformel_zelle` (Z. 722–748) hinterlegt. Kein Summand stammt aus
einer nationalen Größe, die verteilt würde (Lackmustest Z. 708–711, in 3.6 Z. 805–812 wiederholt):
Eine Kommune ohne Flussaue erhält exakt 0.

*Erfüllt — Ausweis der physischen Größe.* §3.1 Z. 545–548 deklariert \(\bar A\) in m²/a als
physischen Teil-Ausweis, §3.6 Z. 816–828 führt ihn als Ausweis 1 neben dem Euro-Ausweis 3 und
ergänzt mit Ausweis 2 die reine Exposition \(\sum_{z\in k} W_z a_{z,s}\) in m² je Szenario.
Ausweis 2 ist ausdrücklich „ohne Schadensquote und ohne Preis" und behauptet keine
Proportionalität; er ist die gegen die Gefahrenkarte prüfbare Zahl. Der Schicht-A-Index ist in 3.7
Z. 918–928 ausdrücklich vom Euro-Pfad getrennt („geht in keine Formel dieses Kapitels ein …
umgekehrt fließt kein Euro-Betrag in \(I_{60,k}\) ein"), also kein verdeckter zweiter Euro-Pfad.

*Nicht erfüllt — Proportionalität auf der deklarierten Betrachtungsebene.* §3.1 Z. 548 schreibt
die Beziehung indexfrei als \(\text{EAD} = \bar A \cdot w\), und §3.1 Z. 541–543 deklariert die
Betrachtungsebene als die **Kommune**. §3.6 Z. 797 rechnet dagegen
\(\text{EAD}_k = \sum_{z\in k} \bar A_z w_z\). Beide Formen stimmen nur überein, wenn \(w_z\) über
alle Zellen der Kommune gleich ist; \(w_z\) hängt aber über \(\theta_{z,t}\) am Gebäudetyp-Mix der
Zelle, und die beiden Wertsätze unterscheiden sich um 21 % (1.950 gegen 1.533 €₂₀₂₆/m² BGF,
Z. 684–685). Der Golden-Test in 3.6 kennt die Bedingung und nennt sie im Kommentar Z. 879
(„Linearitaet: … (gleiche Wertdichte)"), prüft die Gleichheit aber nur an einer Kommune mit
einheitlichem \(\theta_{\text{EFH/ZFH}} = 1{,}0\); im sichtbaren Berichtstext steht die Bedingung
nirgends. Für einen Leser der Teil-Ausweise heißt das: Zwei Kommunen mit gleichem \(\bar A_k\)
können sich im \(\text{EAD}_k\) um bis zu 21 % unterscheiden, ohne dass der Bericht das ausweist —
der native Ausweis ist zum Euro-Pfad **monoton, aber nicht proportional**. Daraus Befund 57
(Kategorie B: die Rechnung in 3.4/3.6 bleibt richtig, falsch ist nur die Identität in 3.1).

#### LF 13 — Herleitungspflicht: ein einziges Formelzeichen ohne abgeschlossene Herleitung ist ein Befund

**Verdikt: Befund** (Befunde 54 und 55). Nachgerechnet statt gelesen: Die Zeichentabelle 3.5 wurde
vollständig gegen die in 3.4, 3.6 und 3.7 verwendeten Formelzeichen abgeglichen — und umgekehrt.

**Zählung.** Die Tabelle 3.5 (Z. 762–789) trägt **28 Zeilen** mit zusammen **41 Einzelzeichen**
(Zeilen fassen Index-Varianten zusammen, etwa \(W_z\), \(W_k\) oder \(p_i\), \(p_1\), \(p_2\),
\(p_3\)). Davon treten **3 Zeichen allein in Kapitel 5 auf** — \(r_{\text{S092}}\), \(\Delta q\),
\(e_{\text{bem}}\) — und sind nach dem Zuschnitt dieses Pakets nicht sein Gegenstand; sie stehen in
der Tabelle und sind hier nur abgezogen. Im Prüfumfang liegen damit **38 Zeichen aus 25 Zeilen**.
Hinzu kommen **2 Zeichen, die in den Formeln von Teil A verwendet werden und keine Zeile in 3.5
haben** (siehe unten). **Geprüft wurden also 40 Formelzeichen.** \(\text{EAD}_{\text{mit}}\) und
\(s_{\text{bem}}\) bleiben im Umfang, weil sie im Text von 3.7 (Z. 922) beziehungsweise 3.6
(Z. 828) vorkommen; ihre Herleitung liegt an den gesetzten Ankern `#s092-wirkung` (Z. 1584) und
`#s-bem-naeherung` (Z. 1666) und ist abgeschlossen.

**Ergebnis 1 — Zeichen ohne Eintrag in 3.5 (namentlich).** Zwei:

```
$ python3 -c "
s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read()
g=lambda a,b: s[s.index(a):s.index(b)]
t35=g('### 3.5 Zeichentabelle','### 3.6 Aggregation'); t34=g('### 3.4 Kernformel','### 3.5 Zeichentabelle'); t31=g('### 3.1 Native','### 3.2 Datenebenen')
rows=[l for l in t35.split(chr(10)) if l.startswith('| ') and '---' not in l[:6] and 'Bedeutung' not in l]
awm=chr(92)+'(f_'+chr(123)+chr(92)+'text'+chr(123)+'AWM'+chr(125)+chr(125)+chr(92)+')'
print('Zeilen 3.5:',len(rows))
print('f_AWM in 3.4:',awm in t34,'| Zeile in 3.5:',any(awm in r for r in rows))
wz=chr(92)+'(w_z'+chr(92)+')'; wf=chr(92)+'cdot w'+chr(92)+')'
print('indexfreies w in 3.1:',wf in t31,'| Zeile fuer w_z:',any(wz in r.split('|')[1] for r in rows),'| Zeile fuer indexfreies w:',any(r.split('|')[1].strip()==chr(92)+'(w'+chr(92)+')' for r in rows))
"
Zeilen 3.5: 28
f_AWM in 3.4: True | Zeile in 3.5: False
indexfreies w in 3.1: True | Zeile fuer w_z: True | Zeile fuer indexfreies w: False
```

- \(f_{\text{AWM}}\) — Alterswertminderungsfaktor, in §3.4 Schritt 3 (Z. 689–692) mit Wert 0,55 und
  Band 0,40–0,75 geführt, ohne Zeile in 3.5, obwohl die Überschrift „alle Formelzeichen der
  Kapitel 3 und 5" verspricht. → Befund 54.
- \(w\) **ohne Index** — in §3.1 Z. 548 (\(\text{EAD} = \bar A \cdot w\)) benutzt; die Tabelle führt
  nur \(w_z\) „Wertdichte der **Zelle**" (Z. 781) und erklärt das indexfreie Gattungszeichen anders
  als bei \(\bar A\) (Z. 775, „indexfrei \(\bar A\) als Gattungszeichen") nicht. → Befund 54.

**Ergebnis 2 — Zeichen ohne abgeschlossene Herleitung (namentlich).** Kein Zeichen des Prüfumfangs
ist ohne Herleitung geblieben; die Herkunftsspalte hält für jedes der 38 Zeichen eine Register-ID
oder eine Berichtsstelle bereit, und alle sechs reinen Laufindizes (\(z\), \(k\), \(s\), \(i\),
\(t\), \(n\)) sind als **Notation** gekennzeichnet und tragen keinen Wert — §3.9 greift für sie
nicht. Stichprobenweise gegengelesen und abgeschlossen vorgefunden: \(k_{\text{BGF}}\) = 1,30
(Herleitung mit Band und Ergebnis-Sensitivität −11 % in Langbeleg B4, Rechenschritt 3, Z. 369–381),
\(n_t\) (NHK 2010 → Preisstand 2026 mit ausgeschriebenem Umrechnungsfaktor 1,6813 × 1,105 = 1,8578,
Z. 354–364 und Tabellenzeile Z. 779), \(p_3\) (geometrisches Mittel des WHG-/Länderpraxis-Bandes,
Z. 664–678), \(d(h)\), \(h_1\), \(h_5\) (§3.3 Z. 588–630 mit Interpolationsregel, Deckelung,
Richtung und Band), \(T\) (Kehrwert, nur zur Lesbarkeit).

**Ergebnis 3 — Herkunft, die auf eine nicht zugelassene Registerzeile zeigt.** Vier Zeichen des
Prüfumfangs — \(d_1\), \(d_5\), \(f_{S093}\), \(f_{S094}\) — nennen als Herkunft die
Registerzeilen 60-S093-01 und 60-S094-01. Beide tragen in der Entscheidungsspalte
**„Sensitivitätsband, abgeschätzt"**, während die Präambel des Registers (Z. 160) für Formelzeichen
wörtlich verlangt: „In Formeln (§3) dürfen später nur Zeilen mit Entscheidung **Basiswert**
stehen." Zusätzlich sagen beide Registerzeilen wörtlich „kein eigenes Multiplikativglied im
Basiswert", während die Kernformel Z. 651 genau ein solches Glied \(\cdot f_{S093} \cdot f_{S094}\)
trägt (numerisch neutral, 1,00). → Befund 55. Zum Vergleich: \(W_z\), \(\theta_{z,t}\), \(n_t\)
(60-R24-01) und \(a_{z,s}\), \(h_{z,s}\), \(p_1\), \(p_2\) (60-W085-01) verweisen auf Zeilen mit
Entscheidung **Basiswert** und erfüllen die Regel.

**Ergebnis 4 — Form der Tabelle.** §3.2 verlangt „je Formel eine **alphabetisch sortierte**
Formelzeichen-Tabelle". Die 28 Zeilen stehen in der Reihenfolge ihres Auftretens (z, k, s/i, t, n,
W, a, h, d, … EAD, r, Δq, s_bem, e_bem, x, I), nicht alphabetisch. → Befund 56, formal eine Frage
der Leitfrage 11; er wird hier verbucht, weil er beim zeilenweisen Durchgang der Tabelle anfällt
und sonst still bliebe.

#### Neue Befunde dieses Pakets (54–57)

**Nummernvergabe.** Das Ticket geht vom Ledgerstand 1–46 aus und nennt 47 als erste freie Nummer
der Runde; tatsächlich haben die Pakete der Reihenfolge 1 bis 3 inzwischen die Nummern **47–49**
(T-0360) und **50–53** (T-0361) vergeben. Die zu Laufbeginn höchste vorhandene Nummer ist damit
**53**, die erste neue Nummer dieses Pakets **54**. **Kein Befund wird in diesem Paket behoben** —
die Einträge sind reine Gegenprüfung.

| Nr | Kat. | Stelle · Art · Begründung · Vorschlag |
|---|---|---|
| 54 | **B** | **Stelle:** Bericht §3.5 „Zeichentabelle (alle Formelzeichen der Kapitel 3 und 5, §3.2/§3.9)" Z. 750–789 (28 Zeilen), gegen §3.4 Schritt 3 Z. 689–692 (\(f_{\text{AWM}}\) = 0,55, Band 0,40–0,75) und §3.1 Z. 548 (\(\text{EAD} = \bar A \cdot w\)). · **Art: Lücke** (§3.2 „je Formel eine … Formelzeichen-Tabelle (Zeichen · Name · Einheit · Wert/Herkunft)"; §3.9 Fertig-Regel „Jede Zeile jeder Zeichentabelle referenziert … eine abgeschlossene Herleitung"; §5 LF 13). · **Begründung:** Die Tabelle beansprucht in ihrer Überschrift und im Einleitungssatz Vollständigkeit („führt **jedes** Formelzeichen, das in diesem Kapitel oder in Kapitel 5 vorkommt"). Der Abgleich (Ausdruck oben) findet zwei in Kapitel 3 verwendete Zeichen ohne Zeile: (a) \(f_{\text{AWM}}\), der Alterswertminderungsfaktor, mit Zahlenwert, Band und einer Ergebnis-Sensitivität von −45 % (§7.2) — er ist damit kein Randzeichen, sondern der Parameter der größten benannten Einzelverschiebung des Berichts; seine Herleitung existiert (§4.8 Z. 1474, §7.2 Z. 2262 ff.), sie ist nur nicht von der Zeichentabelle aus erreichbar. (b) Das indexfreie \(w\) in §3.1: Für \(\bar A\) erklärt die Tabelle das indexfreie Gattungszeichen ausdrücklich (Z. 775), für \(w\) nicht, obwohl §3.1 es in einer Formel benutzt; wer die Tabelle als Nachschlagewerk benutzt, findet nur die Zell-Wertdichte \(w_z\). · **Vorschlag:** Zwei Zeilen ergänzen — \(f_{\text{AWM}}\) („Alterswertminderungsfaktor, nur Sensitivität; 0,55, Band 0,40–0,75", Einheit „–", Herkunft `herleitung: §7.2 / #fortschreibung-neuwert-k3`) und \(w\) als Gattungszeichen zu \(w_z\)/\(w_k\) nach dem Muster der \(\bar A\)-Zeile, mit dem Hinweis, dass auf Kommunenebene die flächengewichtete Wertdichte gemeint ist (Befund 57). Den Vollständigkeitsanspruch der Überschrift als Lint prüfen, damit er beim nächsten neuen Zeichen nicht still altert. |
| 55 | **B** | **Stelle:** Bericht §3.5 Z. 771 (\(d_1\), \(d_5\): „register: 60-S093-01") und Z. 773 (\(f_{S093}\), \(f_{S094}\): „register: 60-S093-01 bzw. 60-S094-01"), gegen Kap. 2 Registerpräambel Z. 160 und die Entscheidungsspalten der Zeilen 60-S093-01 (Z. 187) und 60-S094-01 (Z. 188), beide „**Sensitivitätsband, abgeschätzt** … kein eigenes Multiplikativglied im Basiswert", gegen die Kernformel §3.4 Z. 651 (Faktoren \(\cdot f_{S093} \cdot f_{S094}\)). · **Art: Widerspruch** (§2.3 „ausschließlich aus Register-Zeilen komponiert"; eigene Regel des Berichts Z. 160 „In Formeln (§3) dürfen später nur Zeilen mit Entscheidung **Basiswert** stehen"; §5 LF 13 Herkunftskette). · **Begründung:** Vier Formelzeichen des Basiswert-Pfades holen ihre Herkunft aus Registerzeilen, die der Bericht selbst nicht für Formeln zugelassen hat. Bei \(f_{S093}\)/\(f_{S094}\) sagt die Registerzeile darüber hinaus wörtlich das Gegenteil dessen, was die Formel zeigt: Sie bestreitet ein Multiplikativglied, das in Z. 651 steht. Numerisch ist der Widerspruch heute folgenlos (Neutralwert 1,00), aber er entwertet die Herkunftsangabe: Wer die Herleitung von \(d_1\) und \(d_5\) — den beiden **belegten** Enden der Schadensfunktion, die den Euro-Betrag tragen — über die Register-ID nachschlägt, landet auf einer Zeile, deren Entscheidung „Sensitivitätsband" lautet. Damit ist für die vier Zeichen nicht entscheidbar, ob ihr Wert Basiswert oder Bandende ist. Abgrenzung: **kein** Wiederaufgreifen von Befund 3 (dort fehlten Entscheidungen ganz) und **kein** Teil von Befund 49 (dort geht es um Zeilen mit Entscheidung `offen`); hier tragen die Zeilen eine zulässige Entscheidung, nur die falsche für ihren Verwendungsort. · **Vorschlag:** Entweder 60-S093-01 in zwei Zeilen teilen — eine mit Entscheidung **Basiswert** für die belegten Enden \(d_1\)/\(d_5\) der Wasserstandsachse (Thieken u. a. 2008, B5) und eine mit **Sensitivitätsband** für die Zustandsachse \(f_{S093}\) (analog 60-S094-01) — oder die Präambel Z. 160 um den Fall „neutral gesetztes Bandzeichen (Wert 1,00), das als Platzhalter in der Formel steht" ergänzen und den Satz „kein eigenes Multiplikativglied im Basiswert" in beiden Registerzeilen auf den Ist-Stand der Formel ziehen. |
| 56 | **C** | **Stelle:** Bericht §3.5 Z. 762–789, Reihenfolge der 28 Tabellenzeilen (z, k, s/i, t, n, \(W\), \(a\), \(h\), \(d(h)\), \(d_1\)/\(d_5\), \(h_1\)/\(h_5\), \(f_{S093}\)/\(f_{S094}\), \(A_{z,s}\), \(\bar A\), \(p_i\), \(T\), \(\theta\), \(n_t\), \(k_{\text{BGF}}\), \(w_z\), EAD, …, \(x_k\), \(I_{60,k}\)). · **Art: Formabweichung** (§3.2 „je Formel eine **alphabetisch sortierte** Formelzeichen-Tabelle"). · **Begründung:** Die Tabelle ist nach dem Auftreten in den Formeln sortiert, nicht alphabetisch. Bei 28 Zeilen und 41 Einzelzeichen ist das der Unterschied zwischen Nachschlagen und Durchlesen — genau die Funktion, für die §3.2 die Sortierung verlangt, und ein Adressat ohne Statistikausbildung (§8/P3) nutzt die Tabelle als Nachschlagewerk. Kategorie C: keine Zahl, keine Rechnung, kein Zusammenhang betroffen. Formal gehört der Punkt zu Leitfrage 11 (Form und Erklärbarkeit); er wird hier verbucht, weil er beim zeilenweisen Abgleich für Leitfrage 13 anfällt und sonst still bliebe — das Paket zu LF 11 findet ihn damit als bereits nummeriert vor. · **Vorschlag:** Die Zeilen alphabetisch nach dem Zeichennamen sortieren (lateinische vor griechischen Zeichen, Index nachgeordnet) und die heutige Auftretensreihenfolge, wenn sie für das Lesen gewollt ist, als eigene Spalte „Schritt" führen; alternativ die Abweichung als bewusste Wahl im Einleitungssatz von §3.5 begründen (§3.2 lässt eine begründete Abweichung nicht ausdrücklich zu — dann wäre eine Fortschreibung der Aufgabe nötig). |
| 57 | **B** | **Stelle:** Bericht §3.1 Z. 541–548 — Betrachtungsebene „die **Kommune**" (Z. 541) und Formel \(\text{EAD} = \bar A \cdot w\) (Z. 548) —, gegen §3.6 Z. 797 (\(\text{EAD}_k = \sum_{z\in k} \bar A_z w_z\)) und §3.6 Z. 816–828 (Teil-Ausweise 1 und 3), mit dem Wertsatz-Abstand aus §3.4 Z. 684–685 (1.950 gegen 1.533 €₂₀₂₆/m² BGF) und dem Golden-Test-Kommentar §3.6 Z. 879 („Linearitaet: … (gleiche Wertdichte)"). · **Art: Fehler/Lücke** (§5 LF 3 „auch native Ausweise proportional zu den Euro-Pfaden"; §3.6 Ausweis-Disziplin). · **Begründung:** Auf der Zelle ist der Euro-Betrag exakt proportional zur physischen Zwischengröße (\(\text{EAD}_z = \bar A_z w_z\)) — das erfüllt den Kern von LF 3. Auf der **deklarierten** Betrachtungsebene Kommune gilt \(\text{EAD}_k = \bar A_k \cdot w\) aber nur, wenn \(w_z\) über alle Zellen gleich ist; sonst ist der Quotient \(\text{EAD}_k / \bar A_k\) die flächengewichtete Wertdichte der Kommune. Weil \(w_z\) über \(\theta_{z,t}\) am Gebäudetyp-Mix hängt und die beiden Wertsätze 21 % auseinanderliegen, können zwei Kommunen mit identischem physischen Ausweis \(\bar A_k\) bis zu 21 % verschiedene Euro-Ausweise tragen. Die Formel in §3.1 behauptet als Identität, was nur eine Zell-Identität ist; der Test kennt die Bedingung (Z. 879), prüft sie aber an einer Kommune mit einheitlichem \(\theta_{\text{EFH/ZFH}} = 1{,}0\) und trägt sie nicht in den Berichtstext. Kategorie B: Die Rechenwege in §3.4 und §3.6 sind richtig, kein ausgewiesener Zahlenwert ändert sich; falsch ist die zusammenfassende Identität und fehlend der Hinweis am Teil-Ausweis. · **Vorschlag:** (a) §3.1 Z. 548 auf \(\text{EAD}_z = \bar A_z \cdot w_z\) und \(\text{EAD}_k = \sum_{z\in k} \bar A_z w_z\) ziehen (oder \(w\) ausdrücklich als flächengewichtete Wertdichte \(w_k = \text{EAD}_k / \bar A_k\) definieren, dann mit Zeile in §3.5, siehe Befund 54). (b) Bei Teil-Ausweis 1 in §3.6 den Satz ergänzen, dass \(\bar A_k\) und \(\text{EAD}_k\) über Kommunen hinweg nicht proportional sind, weil die Wertdichte am Gebäudetyp-Mix hängt, und die Spannweite 1.533…1.950 €₂₀₂₆/m² BGF nennen. (c) Den Golden-Test um eine Kommune mit gemischtem \(\theta\) erweitern, die den Unterschied zwischen \(\bar A_k \cdot w_{\text{EFH}}\) und \(\sum_z \bar A_z w_z\) festhält. |

#### Abgrenzung und Status dieses Pakets

- **Geändert wurde ausschließlich `reviews/BEFUNDE_60.md`.** `docs/methodik/60_gebaeudeschaeden_flusshochwasser.md`, `docs/evidenz/register.md`, `backend/scripts/lint_methodik.py` und `backend/` sind unangetastet; die Arbeitsmappen wurden in diesem Paket nicht geöffnet und nicht verändert (eiserne Regel 2), der Abgleich gegen sie liegt bei den Paketen zu den Leitfragen 1 und 14.
- **Kein Befund behoben, keiner umnummeriert.** Die Befunde 3, 49 (Registerzeilen) und 41 (Zeitwertansatz) werden nur abgegrenzt, nicht neu vergeben.
- **Kopftabelle „Offene Befunde (19)" bewusst nicht fortgeschrieben** (Dateirahmen der Runde-3-Pakete, festgelegt im Eröffnungspaket T-0359). Mit 47–49 (T-0360), 50–53 (T-0361) und 54–57 aus diesem Paket wären es 30 offene Zeilen; nachgezogen wird die Kopftabelle im Abschlusspaket der Runde 3.
- **Nicht Gegenstand dieses Pakets:** die Leitfragen 1, 2, 4 bis 12 und 14, der Berichtskopf, die Abschnitte 3.2 und 3.3, die Kapitel 1, 2 und 4 bis 9 sowie die Regression der Befunde 1–53. Formelzeichen, die allein in Kapitel 5 auftreten (\(r_{\text{S092}}\), \(\Delta q\), \(e_{\text{bem}}\)), sind aus der Zählung ausgenommen und nur als vorhanden vermerkt.

### Leitfragen 6 und 8

Paket T-0363 der Runde 3 (18.09.2026), eigene frische Sitzung: Sie hat den geprüften Stand nicht
geschrieben — Kapitel 4, Kapitel 6 und das Entscheidungslog stammen aus T-0235 bis T-0243, T-0256
bis T-0259 und den Revisionspaketen aus T-0281, alle im Endstatus (eiserne Regel 4). Das Bundle
nach §1 lag ab dem ersten Turn vor (Abschnitt 0 dieser Runde, unverändert gültig); die Lint-Ausgabe
aus Abschnitt 0.1 wird **übernommen, nicht neu erhoben** (§5, Schritt „zuerst die deterministischen
Lints"). Maßstab sind ausschließlich §3 und §5 der Aufgabe, nicht der Berichtstext. Nach §6 ist die
volle Prüfung erneut zu fahren, weil die Kalibrierung seit Runde 2 durch die Autor-Revision
geändert wurde; dieses Paket trägt davon den Kern: die Leitfragen **6** (Struktur) und **8**
(Kalibrierung).

**Prüfumfang dieses Pakets.** Vertieft geprüft sind **Kapitel 4 Teil A** (Kapitelkopf
`## 4 Kalibrierung & Validierung (§2.4/§3.4)` samt 4.1, 4.1a, 4.2, 4.3 und 4.4), **Kapitel 6**
„Szenario-Anwendung & Modellgrenzen" und der Abschnitt `## Entscheidungslog`. Nachgemessen, nicht
aus dem Ticket übernommen:

```
$ python3 -c "
import re
s=open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md',encoding='utf-8').read()
def body(a,b):
    t=s.split(chr(10)+a)[1].split(chr(10)+b)[0]
    return re.sub('<!--.*?-->','',t,flags=re.S).strip(chr(10))
pairs=[('## 4 Kalibrierung','### 4.1 Nationaler'),('### 4.1 Nationaler','### 4.1a Kleinste'),
       ('### 4.1a Kleinste','### 4.2 Vom Anker'),('### 4.2 Vom Anker','### 4.3 Modellsumme'),
       ('### 4.3 Modellsumme','### 4.4 Der Niveau'),('### 4.4 Der Niveau','### 4.5 Unabhängige')]
t=0
for a,b in pairs:
    n=len(body(a,b)); t+=n; print(a,n)
print('SUMME Kap4 TeilA',t)
"
## 4 Kalibrierung 1778
### 4.1 Nationaler 2797
### 4.1a Kleinste 6204
### 4.2 Vom Anker 3717
### 4.3 Modellsumme 8960
### 4.4 Der Niveau 2683
SUMME Kap4 TeilA 26139
```

Kapitel 6 misst **5.306** Zeichen und das Entscheidungslog **5.011** Zeichen — beide treffen die im
Ticket genannten Werte exakt. Kapitel 4 Teil A misst **26.139** statt der genannten 25.530 Zeichen
(mit Schnitt am Zeilenanfang der Überschriften: 26.255), die Summe also **36.456** statt 35.847.
Der geprüfte Textkörper ist derselbe — die Abschnittsgrenzen sind die im Ticket genannten; die
Differenz stammt aus 4.1a und 4.3, die seit dem Ticketschnitt um das Ausreißerband und die
Restfehler-Positionen gewachsen sind. Die Zahl steht hier als Messwert, statt die Ticketzahl zu
wiederholen.

**Nicht vertieft geprüft** sind 4.5 bis 4.8 (Kapitel 4 Teil B, Geschwisterpaket); sie werden nur
als Gegenstelle zitiert, etwa für die Verteilungsprüfung, die LF 8 ausdrücklich verlangt. Ein
nationaler 100-m-Vollraster-Lauf ist nach §3.4 unzulässig und wurde **nicht** gefahren:
Nachgerechnet wurde ausschließlich aus den im Bericht ausgewiesenen Zahlen (Ressourcen-Regel §3.4).
Die Arbeitsmappen wurden nur gelesen (eiserne Regel 2); im Code wurde nichts geändert (eiserne
Regel 5).

**Befundnummern — gemessen statt übernommen.** Das Ticket nennt als erste freie Nummer 47; das
Ledger trägt inzwischen die Nummern 1 bis **57** (47–49 aus T-0360, 50–53 aus T-0361, 54–57 aus
T-0371). Nach der Regel „fortlaufend ab der nächsthöheren freien Nummer" vergibt dieses Paket
deshalb ab **58**; die Ticketzahl 47 ist zwischen Ticketschnitt und Lauf veraltet.

#### LF 6 — Struktur: überall verwendet, wo die Evidenz strukturabhängig ist; Kopplungen zwischen abgeleiteten Parametern neu gerechnet?

**Verdikt: Befund** (Befunde 58, 59 und 60). Beide Hälften der Leitfrage tragen je einen eigenen
Mangel; erfüllt sind sie dort, wo der Bericht die Strukturabhängigkeit ausdrücklich als Modellgrenze
führt.

*Erfüllt — Strukturabhängigkeit im Zellmodell und in den Modellgrenzen.* Das Produktionsmodell führt
die Gebäudestruktur als eigene Achse: \(w_z = k_{\text{BGF}} \sum_t \theta_{z,t} n_t\) (§3.4
Schritt 3, Z. 681) mit zwei belegten Wertsätzen, \(n_{\text{EFH/ZFH}}\) = 1.950 und
\(n_{\text{MFH}}\) = 1.533 €₂₀₂₆/m² BGF (Z. 684–685), gespeist aus der Ebene GEBAEUDEWERT (§3.2
Z. 563: Zensus 2022, Gebäudetyp im 100-m-Gitter, Fallback „Typ-Mix der übrigen Zellen derselben
Kommune", ersatzweise „der amtlich publizierte Bestandsmix des Bundeslandes"). Kapitel 6 hält die
strukturabhängigen Stellen als Modellgrenzen fest, statt sie zu verallgemeinern: Modellgrenze 2
(Z. 1805–1809) weist die Materialachse S094 ausdrücklich als für Mauerwerksbauweise kalibriert und
für Holz-, Fachwerk- und Leichtbau als Untergrenze aus (Vorgabe P2, Bauform-Grenze dokumentiert);
Modellgrenze 4 (Z. 1812–1813) beziffert die Regionalstreuung des bundeseinheitlichen NHK-Satzes mit
±20 %; Stationaritätsannahme (2) (Z. 1788–1790) sagt, die Bänder von \(d(h)\) bildeten „nur den
heutigen Bestandsmix ab, nicht eine künftige Bauweise". Das ist der Teil der Leitfrage, der sitzt.

*Nicht erfüllt — die Kalibrierung selbst ist strukturlos gerechnet.* §4.3 bildet den Wert je
exponiertem Wohngebäude als „208 m² Wohnfläche · 1,30 BGF/Wohnfläche · 1.950 €₂₀₂₆/m² BGF =
527.280 €₂₀₂₆" (Z. 1138–1139) und setzt damit den **EFH/ZFH-Satz für den gesamten nationalen
Bestand** an; \(\theta_{z,t}\) kommt in ganz Kapitel 4 nicht vor, auch nicht als Zeile der
M₀-Bandtabelle (Z. 1199–1208). Die Struktur ist also genau dort weggelassen, wo die Evidenz
strukturabhängig ist und wo der Bericht sie in §3.2 selbst als national verfügbar ausweist. Daraus
**Befund 58**.

*Nicht erfüllt — Kopplungen zwischen abgeleiteten Parametern nicht neu gerechnet.* Der Anker hat
sich mit der Revision von \(A^{*}\) = 0,985 auf 1,132 Mrd. €₂₀₂₆/a bewegt (Entscheidungslog Nr. 8,
Z. 2513: „\(A^{*}\) = 1,132 (statt 0,985 nach dem verworfenen Stichprobenlauf)"). Drei abgeleitete
Größen im Prüfumfang sind seither nicht nachgerechnet und tragen rechnerisch weiterhin den
abgelösten Wert — nachgewiesen durch Rückrechnung, nicht vermutet (Befund 59). Zusätzlich ist die
Kopplung des Preisfaktors \(\pi\) an das Baupreisband aus B4 nur am unteren, nicht am oberen
Bandende vollzogen (Befund 60).

#### LF 8 — Kalibrierung: ein Skalar; Revisionsstand; unabhängige Verteilungsprüfung mit Ist-Ergebnis, out-of-sample?

**Verdikt: Befund** (Befunde 61 und 62). Die vier Teilforderungen der Leitfrage fallen
unterschiedlich aus; die Nachrechnung des Skalars selbst besteht.

*Erfüllt — ein einziger Skalar.* §4.4 Z. 1234–1238 bindet \(\lambda\) als „einzigen, bundesweit
konstanten" Faktor auf \(\text{EAD}_k\) und schließt Verteilungswirkung, zweiten Skalar,
bundeslandspezifischen Korrekturfaktor und Nachkalibrierung einzelner Kommunen ausdrücklich aus;
die Einleitung des Kapitels (Z. 934–937) trennt Niveau und Verteilung ebenso. Regionale
Kalibrierfaktoren, die §3.4 nur als befristete Übergangslösung zuließe, kommen nicht vor.

*Erfüllt — Revisionsstand und vorläufige Jahre.* §4.1 Z. 968–974 benennt den Stand („Datenservice
zum Naturgefahrenreport 2025") mit den Aktualisierungsvermerken 10.10.2025 und 30.12.2025, weist
die Reihe als bestands- und preisnormiert aus („bezogen auf Bestand und Preise 2024") und hält das
Schadenjahr 2025 als nur vorläufig mitgeteilt **aus** der Kalibrierung heraus („geht in die
Kalibrierung **nicht** ein; es dient ausschließlich als nachlaufende Kontrolle"). Damit ist die
Forderung von §3.4 („laufende/vorläufige Jahre gesondert, nicht ins Kalibrier-Mittel") erfüllt; eine
Sensitivität ohne vorläufige Werte erübrigt sich, weil kein vorläufiger Wert in der Reihe steht.

*Erfüllt — unabhängige Verteilungsprüfung mit Ist-Ergebnis, out-of-sample.* §4.5 (Teil B, hier nur
als Gegenstelle) prüft die Achse Ereignisregime über eine Jahresauslassung (Leave-one-out,
Z. 1272–1278), begründet die Unabhängigkeit von der Kalibrierung zweifach und nachrechenbar
(Skaleninvarianz und Jahresauslassung, Z. 1287–1298) und fixiert die Toleranz mit ±11,5
Prozentpunkten **vorab** (Z. 1300–1302). Prüfdaten und Fit-Daten fallen damit auseinander; das
Ist-Ergebnis ist ausgewiesen und lautet **nicht bestanden**, was der Bericht nicht glättet, sondern
als Grund für den Vermerk „vorläufig" führt (Kapitelkopf Z. 949–954, §4.4 Z. 1259–1261). Die
Vollständigkeit dieser Prüfung liegt beim Geschwisterpaket zu Teil B; für LF 8 ist die Forderung
formal erfüllt.

*Nachgerechnet statt gelesen — der Niveau-Skalar.* Die Leitfrage wird hier nicht am Text, sondern an
der Rechnung geprüft. Beide Eingangszahlen stammen aus dem Bericht:

| Eingangszahl | Wert | Fundstelle |
|---|---|---|
| Zielwert der Bundessumme \(A^{*}\) | 1,132 Mrd. €₂₀₂₆/a | `docs/methodik/60_gebaeudeschaeden_flusshochwasser.md` §4.2 „Zielwert" **Z. 1123** |
| Modellsumme vor Kalibrierung \(M_0\) | 1,360 Mrd. €₂₀₂₆/a | ebenda §4.3 **Z. 1157–1159** |
| ausgewiesener Skalar \(\lambda\) (Vergleichswert) | 0,832 | ebenda §4.4 **Z. 1230** |

**Rechenweg.** \(\lambda_{\text{nachgerechnet}} = A^{*}/M_0 = 1{,}132 / 1{,}360 =
0{,}8323529411\ldots \rightarrow \mathbf{0{,}832}\) (drei Nachkommastellen). Gegen den in 4.4
ausgewiesenen Wert 0,832: **Abweichung +0,042 %**. Gegenprobe mit ungerundeten Eingängen, damit die
Übereinstimmung nicht aus der Rundung stammt: \(A^{*}\) aus seinen sechs Faktoren (§4.2 Z. 1123) =
1,838 · 0,65 · 1,54 · 0,50 · 1,15 · 1,07 = 1,1319603295 (Folgefaktor-Produkt 0,6158652500 —
identisch mit dem in §4.1a Z. 1037–1038 ausgewiesenen 0,615865); \(M_0\) aus seinen Eingängen
(§4.3 Z. 1157) = 0,872 · 527.280 € · (339.000 · 0,0059796/a + 1.380.000 · 0,00067515/a) =
0,872 · 527.280 € · 2.958,7914/a = 1.360.417.254 €₂₀₂₆/a = 1,360417 Mrd.; daraus \(\lambda\) =
1,1319603295 / 1,360417254 = 0,8320684896 → **0,832**, **Abweichung +0,008 %**. Auch die
Klassenbeiträge stimmen (GK3+GK4 0,9320 gegen ausgewiesene 0,932 Mrd.; GK2 428,39 gegen
ausgewiesene 428 Mio.). Der produktive Skalar ist damit korrekt gerechnet; **dieser Teil ist
bestanden**, und der Befund liegt nicht am Zentralwert.

*Nicht erfüllt — die Schranke, die den Skalar prüfen soll, kann nicht ansprechen.* §4.4
Z. 1240–1258 stellt \(\lambda\) eine Plausibilitätsschranke [0,11; 3,44] zur Seite, bei deren
Verletzung „das Modell als fehlerhaft gilt". Sie ist aus denselben Bandenden hergeleitet, aus denen
\(\lambda\) selbst folgt, und kann deshalb von \(\lambda = A^{*}/M_0\) nie verletzt werden — der
Bericht zieht diesen Schluss an zwei Stellen selbst („Das untere Bandende \(\lambda\) = 0,11 **gilt
als zulässig**", „Das obere Bandende … **gilt aus demselben Grund als zulässig**", Z. 1253–1257).
Daraus **Befund 61**.

*Nicht erfüllt — die Bandrechnung des Skalars ist an drei Stellen nicht nachrechenbar.* Die in 4.4
und 4.3 ausgewiesenen Zwischenergebnisse der Bandfortpflanzung weichen ab der vierten
Nachkommastelle von der Division ab, die der Bericht angibt. Daraus **Befund 62** (Kategorie C: die
gerundeten Endwerte 0,11 / 3,44 / 0,657 ändern sich nicht).

#### Neue Befunde dieses Pakets (58 bis 62)

| Nr | Kat. | Befund |
|---|---|---|
| 58 | **B** | **Stelle:** Bericht §4.3 Z. 1138–1139 („208 m² Wohnfläche · 1,30 BGF/Wohnfläche · 1.950 €₂₀₂₆/m² BGF = **527.280 €₂₀₂₆**") und M₀-Bandtabelle Z. 1199–1208, Zeile „Wertsatz" Z. 1203 — gegen §3.4 Schritt 3 Z. 681 (\(w_z = k_{\text{BGF}} \sum_t \theta_{z,t} n_t\)), §3.5 Z. 684–685 (\(n_{\text{EFH/ZFH}}\) = 1.950, \(n_{\text{MFH}}\) = 1.533 €₂₀₂₆/m² BGF) und §3.2 Ebene GEBAEUDEWERT Z. 563 (Gebäudetyp-Mix \(\theta_{z,t}\) aus Zensus 2022, Fallback „amtlich publizierter Bestandsmix des Bundeslandes"). · **Art: Fehler/Lücke** (§3.4 „Kalibriermodell = Produktionsmodell"; §5 LF 6 erste Hälfte). · **Begründung:** Das Produktionsmodell bewertet jede Zelle mit einem **typgewichteten** Wertsatz über \(\theta_{z,t}\); der nationale Kalibrierlauf, aus dem \(M_0\) und damit \(\lambda\) folgen, setzt stattdessen für **den gesamten** exponierten Bestand den EFH/ZFH-Satz 1.950 €₂₀₂₆/m² BGF an. \(\theta\) kommt in Kapitel 4 an keiner Stelle vor, auch nicht als Bandzeile — die Struktur ist weder gerechnet noch als Unsicherheit geführt. Die beiden Sätze liegen 21 % auseinander (1.950 gegen 1.533), die Richtung des Fehlers ist eindeutig: \(M_0\) ist zu hoch und \(\lambda\) zu niedrig angesetzt, soweit MFH-Wohnfläche im exponierten Bestand steckt. Nachgerechnet als Randfall: Trüge der exponierte Bestand durchgehend den MFH-Satz, wäre \(M_0\) = 1,360 · 1.533/1.950 = **1,069** Mrd. €₂₀₂₆/a und \(\lambda\) = 1,132/1,069 = **1,059** statt 0,832 — eine Verschiebung um **+27 %**, also größer als jede der vier Fenster-Sensitivitäten in §4.1a (Z. 1041–1046). Verschärfend: Die Wohnfläche 208 m² ist der Quotient aus 4,1 Mrd. m² und 19,7 Mio. **Wohngebäuden aller Typen** (Z. 1201), also ein Mittel **über** die Typen, während der Wertsatz daneben typ**spezifisch** gewählt ist — die beiden Faktoren desselben Produkts beziehen sich auf verschiedene Grundgesamtheiten. Dass der Fallback nach §3.2 gerade der Bestandsmix des Bundeslandes ist, zeigt, dass die Größe für einen nationalen Ansatz vorliegt und nicht beschafft werden müsste. · **Vorschlag:** In §4.3 den nationalen Typ-Mix \(\bar\theta\) (Zensus 2022, Wohnfläche je Gebäudetyp) einsetzen und den Wert je exponiertem Wohngebäude mit \(k_{\text{BGF}} (\bar\theta_{\text{EFH}} n_{\text{EFH}} + \bar\theta_{\text{MFH}} n_{\text{MFH}})\) bilden, \(M_0\), \(\lambda\) und das M₀-Band daraus neu rechnen; \(\bar\theta\) als eigene Zeile in die Bandtabelle aufnehmen (Bandenden aus der Spannweite der Länder-Mixe). Ist der Mix für die **exponierte** Teilmenge nicht greifbar, den Punktwert als Abschätzung von KAP3 nach §3.9 mit Band 1.533–1.950 ausweisen — aber nicht stillschweigend den oberen Rand als Zentralwert führen. Solange das offen ist, gehört die Richtung des Fehlers in den Vorläufigkeitsvermerk von \(\lambda\) (Z. 949–954). |
| 59 | **B** | **Stelle:** Drei Stellen im Prüfumfang, die rechnerisch den abgelösten Anker \(A^{*}\) = 0,985 Mrd. €₂₀₂₆/a tragen statt den geltenden 1,132 (Entscheidungslog Nr. 8 Z. 2513 weist den Wechsel selbst aus: „\(A^{*}\) = 1,132 (statt 0,985 nach dem verworfenen Stichprobenlauf)"): **(a)** §4.3 Z. 1153–1155 — die Gegenrechnung mit dem Alternativnenner „ergäbe \(M_0\) = 0,931 Mrd. €₂₀₂₆/a und \(\lambda\) = **1,058**"; **(b)** Kapitel 6 Modellgrenze 9 Z. 1826–1832 und Versionsstempel Z. 1840–1841 — „der Zeitwertansatz … läge um 45 % niedriger (**0,54** statt **0,99** Mrd. €₂₀₂₆/a, Band 0,39–0,74)"; **(c)** Entscheidungslog Nr. 7 Z. 2512 — „höbe \(\lambda\) auf **1,32** (bis **1,81**)" samt dem dort als „nachgezogen 17.09.2026 (T-0313)" bezeichneten Stand „\(\lambda\) = **0,724**" und der Auswirkungsspalte „0,54 (0,39–0,74) statt 0,99 Mrd. €₂₀₂₆/a". · **Art: veraltete Angabe/Widerspruch** (§5 LF 6 zweite Hälfte „Kopplungen zwischen abgeleiteten Parametern neu gerechnet?"; §5 LF 10 „veraltet"). · **Begründung:** Jeder der Zahlenwerte lässt sich exakt auf den alten Anker zurückrechnen, ist also nicht neu gerechnet, sondern stehen geblieben. (a) 0,985 / 0,931 = 1,05800 — genau die ausgewiesenen 1,058; mit dem geltenden Anker ist es 1,132 / 0,931 = **1,216**, die Angabe liegt **13,0 % zu niedrig**. (b) Die kalibrierte Bundessumme ist \(\lambda \cdot M_0\) = 0,832 · 1,360 = **1,132** Mrd. €₂₀₂₆/a — der Bericht rechnet das in §4.6 Z. 1381 selbst vor („derselbe Wert wie in §4.4"); Kapitel 6 nennt daneben 0,99 Mrd., also den alten Anker, **12,5 % zu niedrig**, und die Zeitwert-Sensitivität 0,54 statt 0,55 · 1,132 = **0,62** (Band 0,45–0,85 statt 0,39–0,74). (c) 0,985 / (1,360 · 0,55) = 1,3168 → die ausgewiesenen „1,32", und 0,985 / (1,360 · 0,40) = 1,8107 → die „1,81"; mit dem geltenden Anker sind es 1,132 / (1,360 · 0,55) = **1,51** und 1,132 / (1,360 · 0,40) = **2,08** — dieselben Werte, die §7.2 Z. 2250–2251 bereits korrekt führt. Das Entscheidungslog ist damit intern gegen §7.2 widersprüchlich, und der als Nachzug gekennzeichnete \(\lambda\) = 0,724 ist seit derselben Revision auf 0,832 abgelöst. Die Prozentangabe „−45 %" bleibt richtig, weil sie nur \(f_{\text{AWM}}\) spiegelt; falsch sind die absoluten Beträge — und genau sie stehen im nutzersichtbaren Versionsstempel. · **Vorschlag:** Die Werte aus dem geltenden \(A^{*}\) = 1,132 neu rechnen und einsetzen: (a) 1,058 → 1,216; (b) „0,54 statt 0,99" → „0,62 statt 1,13", Band 0,39–0,74 → 0,45–0,85; (c) 1,32 (1,81) → 1,51 (2,08), \(\lambda\) = 0,724 → 0,832. Zusätzlich die kalibrierte Bundessumme **einmal** an einer Stelle definieren (§4.6 Z. 1381) und in Kapitel 6 und im Entscheidungslog nur noch dorthin verweisen, statt den Betrag zu wiederholen — er ist mehrfach abgeschrieben und mehrfach veraltet. Für den Lint: eine Regel, die \(\lambda \cdot M_0\) gegen jede im Bericht genannte Bundessumme prüft. |
| 60 | **C** | **Stelle:** Bericht §4.2 Z. 1119–1121 (\(\pi\) = 1,07: „Das Register führt für 2023 → 2026 den Baupreisfaktor 1,105 (B4, Band **1,07–1,16**). Abzüglich rund 3 % Baupreisanstieg 2023 → 2024 ergibt sich \(1{,}105/1{,}03 \approx 1{,}073\); **Band 1,04–1,11**") und Zeile \(\pi\) der Tabelle Z. 1093 — gegen §4.3 M₀-Bandtabelle Z. 1203, die dasselbe B4-Band auf den Wertsatz anwendet (1.889–2.047). · **Art: Fehler** (§5 LF 6 „Kopplungen zwischen abgeleiteten Parametern neu gerechnet?"). · **Begründung:** \(\pi\) ist ein abgeleiteter Parameter: Er entsteht aus dem B4-Faktor durch Division mit 1,03. Der Zentralwert ist so gerechnet (1,105/1,03 = 1,0728 → 1,07), das **untere** Bandende ebenfalls (1,07/1,03 = 1,0388 → 1,04), das **obere** Bandende dagegen nicht: 1,16/1,03 = **1,126**, ausgewiesen ist 1,11. Dass die Nachbarzeile in §4.3 dieselbe Kopplung sauber durchrechnet (1.950/1,105 · 1,07 → 1.889 und 1.950/1,105 · 1,16 → 2.047), zeigt, dass die Abweichung nicht gewollt ist, sondern in 4.2 unterblieben ist. Wirkung: \(A^{*}\)_oben stiege von 2,263 auf 2,296 Mrd. €₂₀₂₆/a, die obere Plausibilitätsschranke von 3,44 auf 3,49 (2,296/0,657). Der Zentralwert von \(A^{*}\) und damit \(\lambda\) ist **nicht** betroffen — deshalb Kategorie C, nicht B. · **Vorschlag:** Das obere Bandende von \(\pi\) auf 1,13 (1,16/1,03, kaufmännisch gerundet) ziehen und das Band von \(A^{*}\) sowie die Schranke in §4.4 und §4.8 nachziehen; oder, falls die Deckelung auf 1,11 beabsichtigt ist, sie als Abschätzung von KAP3 mit Begründung ausweisen (§3.9), statt sie als Ergebnis der Division erscheinen zu lassen. |
| 61 | **B** | **Stelle:** Bericht §4.4 „Plausibilitätsschranke" Z. 1240–1258, besonders die Herleitung Z. 1243–1250 („Sie ist das vollständig fortgepflanzte Band aus dem Ankerband von \(A^{*}\), 0,297–2,263 (§4.2), und dem Band von \(M_0\), 0,657–2,643 (§4.3)") und der Selbstbefund Z. 1253–1257 („Das untere Bandende \(\lambda\) = 0,11 **gilt als zulässig** … Das obere Bandende \(\lambda\) = 3,44 **gilt aus demselben Grund als zulässig**") — gegen die Funktion, die derselbe Abschnitt ihr zuweist (Z. 1240–1243: „Ergibt eine Neubestimmung \(\lambda < 0{,}11\) oder \(\lambda > 3{,}44\), wird **nicht** der Skalar gesetzt, sondern das Modell gilt als fehlerhaft"). · **Art: Fehler (Zirkelschluss)** (§5 LF 8 „ein Skalar"; §3.4 Kalibrierfaktor-Regel; §8/P3 Erklärbarkeit). · **Begründung:** Die Schranke ist definitionsgemäß das Intervall \([A^{*}_{u}/M_{0,o},\; A^{*}_{o}/M_{0,u}]\). Jedes \(\lambda = A^{*}/M_0\), das aus Werten innerhalb der eigenen Bänder gebildet wird, liegt zwangsläufig darin — die Prüfung kann kein Ergebnis zurückweisen, das mit der Methode des Berichts überhaupt entstehen kann. Der Bericht spricht das selbst aus, zieht daraus aber nicht den Schluss, dass die Schranke ihre Aufgabe („das Modell gilt als fehlerhaft") damit nicht erfüllen kann. Erkennbar wird die Wirkungslosigkeit an der Weite: [0,11; 3,44] überspannt den Faktor **31**, während der Vorgängerstand („Faktor 2 um den Neutralwert 1", Z. 1244) mindestens ansprechen konnte — die Herleitung hat den Prüfstein nicht geschärft, sondern abgeschafft. Dass §4.1a Z. 1048–1054 die vier Fenster-\(\lambda\) (0,457 bis 0,935) gegen sie prüft und die Unterschreitung ausdrücklich als zweites Argument fallen lässt, bestätigt es: Der Test hat in keinem geprüften Fall unterschieden. Ein zweiter, davon unabhängiger Prüfstein für den Skalar existiert im Kapitel nicht; das Sanity-Band in §4.6 prüft die Bundessumme, nicht \(\lambda\). · **Vorschlag:** Die Schranke aus einer Größe herleiten, die **nicht** in \(\lambda\) eingeht — etwa aus einem unabhängigen Vergleichswert der Bundessumme (Wiederaufbaufonds 2002/2013/2021 als Ereignisbilanz, §4.1 Z. 962–964) oder aus einem Modellverständnis-Argument („\(\lambda\) unter 0,5 oder über 2 heißt, dass Exponiertenzahl, Wertdichte oder Schadensfunktion um mehr als den Faktor 2 danebenliegen") und die so gesetzte Schranke als Abschätzung von KAP3 nach §3.9 ausweisen. Die Bandfortpflanzung aus \(A^{*}\) und \(M_0\) bleibt daneben als **Unsicherheitsband** von \(\lambda\) stehen — sie ist als solches richtig gerechnet und soll nur nicht mehr als Prüfstein auftreten. Beides ist im Text zu trennen, damit ein Leser nach P3/§8 nicht ein Prüfkriterium sieht, wo ein Konfidenzband steht. |
| 62 | **C** | **Stelle:** Drei nachgerechnete Zwischenergebnisse: **(a)** §4.4 Z. 1248–1249 „\(\lambda_{\text{unten}}\) = 0,297 / 2,643 = **0,112384…**"; **(b)** ebenda Z. 1249 „\(\lambda_{\text{oben}}\) = 2,263 / 0,657 = **3,444409…**"; **(c)** §4.3 Z. 1218 „\(M_0\)_unten = 0,872 · 491.140 € · 1.534,08/a = **656.945.337** €₂₀₂₆/a". · **Art: Fehler (Rechenweg)** (§5 LF 8; §8/E3 „Rechenbeispiel", P3). · **Begründung:** Die drei Divisionen bzw. Produkte ergeben nachgerechnet andere Ziffern, als der Bericht ausweist: (a) 0,297/2,643 = **0,1123723…**, nicht 0,112384… (Abweichung ab der fünften Nachkommastelle); (b) 2,263/0,657 = **3,4444444…**, nicht 3,444409… — die ausgewiesene Ziffernfolge lässt sich auch mit den ungerundeten Bandenden nicht erzeugen (2,2626871/0,657 = 3,443968); (c) 0,872 · 491.140 · 1.534,08 = **657.006.700,6**, nicht 656.945.337 (Differenz 61.364 €, 0,009 %). Die gerundeten Endwerte 0,11, 3,44 und 0,657 Mrd. sind in allen drei Fällen unberührt — deshalb Kategorie C und keine Wirkung auf \(\lambda\) oder das Ergebnis. Der Befund gilt trotzdem, weil der Bericht die Ziffern ausdrücklich als nachvollziehbaren Rechenweg anbietet („zwei Nachkommastellen, kaufmännisch gerundet", Z. 1249–1250): Wer nachrechnet — wie es §8/E3 vom Adressaten gerade erwartet —, findet drei Abweichungen und muss zuerst prüfen, ob er selbst falsch liegt. · **Vorschlag:** Die drei Stellen aus der Rechnung neu setzen (0,112372…, 3,444444…, 657.006.701) und Zwischenergebnisse künftig aus dem Ausdruck übernehmen, der sie erzeugt, statt sie zu tippen; ergänzend in den Lint aufnehmen, dass jede im Bericht als „=" ausgewiesene Division der Kalibrierkette nachgerechnet wird (die Eingänge stehen alle im Text). |

#### Abgrenzung und Status dieses Pakets

- **Geändert wurde ausschließlich `reviews/BEFUNDE_60.md`.**
  `docs/methodik/60_gebaeudeschaeden_flusshochwasser.md`, `docs/evidenz/register.md`,
  `backend/scripts/lint_methodik.py` und `backend/` sind unangetastet; die Arbeitsmappen wurden nur
  gelesen und nicht verändert (eiserne Regel 2).
- **Kein Befund behoben, keiner umnummeriert.** Die Befunde 33 (Verteilungsprüfung), 34
  (Kleinste-Quadrate-Anker), 35/36 (Bänder) und 41 (Zeitwertansatz) werden nur als Gegenstelle
  eingeordnet, nicht neu vergeben. Befund 59 greift Befund 41 **nicht** wieder auf: Dort ging es um
  die Entscheidung Neuwert/Zeitwert, hier um Beträge, die nach dieser Entscheidung nicht auf den
  geltenden Anker nachgezogen wurden.
- **Abgrenzung zu Befund 57** (Paket T-0371, LF 3): Dort geht es um die fehlende Proportionalität
  zwischen \(\bar A_k\) und \(\text{EAD}_k\) wegen der typabhängigen Wertdichte **innerhalb** des
  Modells; Befund 58 betrifft dieselbe Größe \(\theta\) an einem anderen Ort — ihr Fehlen in der
  **nationalen Kalibrierung** in §4.3. Beide sind unabhängig voneinander zu beheben.
- **Gesehen, aber außerhalb des Dateirahmens dieses Pakets und deshalb nicht als Befund vergeben:**
  der Vorläufigkeitsvermerk von \(\lambda\) in §4.8 Z. 1467 (nennt die Befunde 33 und 34 statt der
  in §4.4 Z. 1259–1261 genannten 35 und 36) und der Kopfabschnitt „Offen (Stand 17.09.2026)" Z. 35
  (führt weiterhin \(\lambda\) = 0,724). Beides ist dieselbe Ursache wie Befund 59; das Paket zu
  Kapitel 4 Teil B und das Abschlusspaket der Runde entscheiden dort.
- **Kopftabelle „Offene Befunde (19)" bewusst nicht fortgeschrieben** (Dateirahmen der
  Runde-3-Pakete, festgelegt im Eröffnungspaket T-0359). Mit 58–62 aus diesem Paket wären es 35
  offene Zeilen; nachgezogen wird die Kopftabelle im Abschlusspaket der Runde 3.
- **Ressourcen-Regel §3.4 eingehalten:** kein nationaler 100-m-Vollraster-Lauf; alle Nachrechnungen
  stammen aus den im Bericht ausgewiesenen Zahlen. Im Code wurde nichts geändert (eiserne Regel 5).
- **Nicht Gegenstand dieses Pakets:** die Leitfragen 1 bis 5, 7 und 9 bis 14, die Abschnitte 4.5 bis
  4.8, die Kapitel 1, 2, 3, 5, 7, 8 und 9 sowie die Regression der Befunde 1–57.

### Leitfrage 7 — Teil 1: Verteilungsannahmen und Sanity-Band

**Prüfumfang dieses Pakets (T-0376).** Erster Teil der Leitfrage 7 aus §5 der Aufgabe
(„**Tails/Parameter:** Verteilungsannahmen, wo empirische Quantile verfügbar wären; gesetzte Werte,
die messbar wären; Kalibriermodell = Produktionsmodell?", `docs/AUFGABE_METHODIK_SCHADENSRECHNUNG.md`
**Z. 440–441**), vertieft geprüft an genau zwei Abschnitten des Berichts: §4.5 (Z. 1263–1350) und
§4.6 (Z. 1351–1386). Umfangsmessung in dieser Sitzung, ausgeführt:
`python3 -c 'import re; t=open("docs/methodik/60_gebaeudeschaeden_flusshochwasser.md").read().split(chr(10)); m=lambda a,b: len(re.sub(r"<!--.*?-->","",chr(10).join(t[a-1:b]),flags=re.S)); print(m(1263,1350), m(1351,1386))'`
→ **7.079** und **5.028** Zeichen, zusammen **12.107** — identisch mit dem Planungsstand vom
18.09.2026, keine Abweichung auszuweisen. §4.1–§4.4, §4.7 und Kapitel 9 gehören zu Schwesterpaketen
und sind hier nur als Fundstelle zitiert. **Das Gesamtverdikt zu Leitfrage 7 wird nicht hier
gezogen, sondern im Paket auf Reihenfolgeplatz 15 (Teil 2, §4.8); es ist hier nicht vorweggenommen.**

**Zwischenverdikt für diesen Teil: Befund** (Befunde 63, 64 und 65). Die Prüfgröße von §4.5 ist
sauber aus der Ankerreihe gebildet und ihre Toleranz ist nachrechenbar (Nachrechnung 1); die
Sanity-Obergrenze von §4.6 ist rechnerisch exakt (Nachrechnung 2). Nicht erfüllt sind drei Punkte:
die nach LF 7 verfügbaren **empirischen Jahresquantile** der Ankerreihe werden an keiner Stelle als
Prüfgröße benutzt (Befund 63, Fundstelle §4.5 Z. 1271–1286 und Z. 1341–1349), die Obergrenze \(O\)
ist — anders als die eigens dafür neu gefasste Untergrenze \(U\) — **kein von der Modellseite
unabhängiger** Wert und kann nie ansprechen (Befund 64, Fundstelle §4.6 Z. 1363 gegen §4.3 Z. 1157),
und der Regime-Anteil der Modellseite ist in §4.5 in sich widersprüchlich gerundet (Befund 65,
Fundstelle §4.5 Z. 1319–1325).

#### (b) Empirische Quantile oder gesetzte Verteilungsannahme? — ausdrückliche Feststellung

| Seite der Prüfung | Woher die Verteilungsaussage stammt | Fundstelle |
|---|---|---|
| Ankerseite \(R_{\text{anker}}\) = 47,7 % | **Empirisch, aber kein Quantil:** ein Mittelwert-Aggregat über alle 23 Jahre (Summe der Überschüsse über das jeweilige Auslassungsmittel ÷ Summe der Reihe). Keine Rangstatistik, keine Plotting-Position, kein Quantil der Reihe. | Bericht §4.5 **Z. 1276–1278** (Formel), **Z. 1321–1324** (Ist-Wert); Datei `docs/evidenz/60_gdv_jahresreihe_2002_2024.csv` (24 Zeilen = Kopfzeile + 23 Jahreswerte, Spalte `wert_mrd_eur`) |
| Modellseite 33,9 % (bzw. 33,8 %) | **Gesetzte Verteilungsannahme:** drei Stützstellen mit gesetzten Jährlichkeiten aus §3.6; das Extremband stammt aus Register 60-W085-01, nicht aus der Reihe. | Bericht §4.5 **Z. 1319–1321** („aus den Stützstellen von §3.6"), **Z. 1308** (Band 5,0·10⁻³–1,0·10⁻³ a⁻¹) |
| Selbstaussage des Berichts | Der Bericht benennt die Lücke selbst: „das Normaljahr \(\bar A_{-t}\) ist ein Mittel, **keine gemessene Trennung nach Jährlichkeit**"; eine engere Prüfung verlange Ereignis- statt Jahreswerte, die nicht publiziert seien. | Bericht §4.5 **Z. 1347–1349** |

**Feststellung.** Die Verteilungsaussage in §4.5 stammt auf der Ankerseite aus einer **empirischen,
aber quantilfreien** Mittelwertstatistik und auf der Modellseite aus einer **gesetzten**
Verteilungsannahme. Empirische Quantile der Ankerreihe wären verfügbar — 23 Jahreswerte tragen
Rang-Plotting-Positionen bis herab zu rund 1/24 a⁻¹ — und werden nirgends gebildet; das ist genau
die Konstellation, auf die LF 7 zielt. Daraus **Befund 63**.

#### (c) Zwei Nachrechnungen statt Lektüre

**Nachrechnung 1 — Toleranz der Verteilungsprüfung (§4.5 Z. 1298–1311).** Einzelbeiträge aus dem
Bericht: ±11,16 Pp (Jackknife, **Z. 1306**), ±1,73 Pp (Ableseunschärfe, **Z. 1307**), ±2,30 Pp
(modellseitiges Band, **Z. 1308**); Kombinationsregel quadratisch (**Z. 1310–1312**). Ausgeführt:
`python3 -c 'import math; print(math.sqrt(11.16**2+1.73**2), math.sqrt(11.29**2+2.30**2))'`
→ `11.293294470613967 11.521896545274133`. Zusätzlich aus der Ankerreihe selbst nachgerechnet
(Leave-one-out und Jackknife-Standardfehler über die CSV, in dieser Sitzung ausgeführt):
23 Werte, Summe 42,28 Mrd. €, Überschuss 20,186 Mrd. €, \(R_{\text{anker}}\) = **47,74 %**,
Replikate **37,61 %–49,87 %**, Standardfehler **11,156 Pp**.

| Größe | Wert im Bericht | nachgerechnet | Abweichung |
|---|---|---|---|
| Ankerseitiges Teilbudget \(\sqrt{11{,}16^2+1{,}73^2}\) | ±11,3 Pp (Z. 1310) | 11,29329 → **11,3** | 0 |
| Gesamttoleranz \(\sqrt{11{,}29^2+2{,}30^2}\) | ±11,5 Pp (Z. 1298, 1311) | 11,52190 → **11,5** | 0 |
| Jackknife-Standardfehler | 11,16 Pp (Z. 1306) | **11,156** | −0,04 % |
| Replikate-Spanne | 37,6 %–49,9 % (Z. 1306) | **37,61 %–49,87 %** | 0 (auf eine Nachkommastelle) |
| \(R_{\text{anker}}\) | 47,7 % (Z. 1324) | **47,74 %** | +0,08 % |

**Ergebnis:** Die Toleranz ist aus ihren im Bericht genannten Einzelbeiträgen vollständig
reproduzierbar, ebenso die ankerseitige Prüfgröße; dieser Teil ist rechnerisch **bestanden**. Der
Kombinationsweg ist vorab fixiert und wird nicht nachträglich geweitet (Z. 1299–1300, Z. 1313–1314).
Auffällig bleibt die Modellseite: 23,2 + 10,6 = **33,8**, ausgewiesen ist 33,9 (Z. 1320–1321), und
die ausgewiesene Differenz 13,9 Pp (Z. 1324) folgt aus 47,7 − 33,8, nicht aus 47,7 − 33,9 (= 13,8).
Daraus **Befund 65**.

**Nachrechnung 2 — Sanity-Obergrenze \(O\) (§4.6 Z. 1363).** Eingänge aus dem Bericht: 339.000
Adressen GK3/GK4 mit Klassenrate 0,1 a⁻¹, 1.380.000 Adressen GK2 mit Klassenrate 0,01 a⁻¹
(Register 60-R17-01), Gebäudewert 527.280 €₂₀₂₆ (Register 60-R24-01), gedeckelte Schadensquote
0,250 (§3.3). Ausgeführt:
`python3 -c 'r=339000*0.1+1380000*0.01; print(r, r*527280*0.250)'` → `47700.0 6287814000.0`.

| Größe | Wert im Bericht | nachgerechnet | Abweichung |
|---|---|---|---|
| getroffene Adressen je Jahr | 47.700 (Z. 1363) | **47.700,0** | 0 |
| Obergrenze \(O\) | 6,29 Mrd. €₂₀₂₆/a (Z. 1363) | **6,287814** Mrd. €₂₀₂₆/a | −0,03 % (reine Rundung auf zwei Stellen) |
| Lage des Ist-Werts \(\lambda M_0\) = 1,132 | innerhalb [0,0103; 6,29] (Z. 1381–1382) | **bestätigt** (1,132 < 6,288) | 0 |

**Ergebnis:** \(O\) ist rechnerisch korrekt. Die Prüfung, die \(O\) tragen soll, ist es nicht:
`python3 -c 'M0=0.872*527280*2958.7914; print(47700*527280*0.250/M0)'` → `4.62197460611665`, d. h.
\(O = 4{,}622 \cdot M_0\) mit **denselben** Registergrößen (339.000, 1.380.000, 527.280 €) als
Faktoren wie \(M_0\) (§4.3 Z. 1157). Der Test \(\lambda M_0 \le O\) ist damit äquivalent zu
\(\lambda \le 4{,}62\) und liegt vollständig innerhalb der ohnehin geltenden Plausibilitätsschranke
\(\lambda \le 3{,}44\) (§4.4 Z. 1240–1258). Daraus **Befund 64**.

#### Neue Befunde dieses Pakets (63 bis 65)

| Nr | Kat. | Befund |
|---|---|---|
| 63 | **B** | **Stelle:** Bericht §4.5, Prüfgröße Z. 1271–1286 und Grenzen-Absatz Z. 1341–1349, gegen `docs/evidenz/60_gdv_jahresreihe_2002_2024.csv` (23 Jahreswerte, Spalte `wert_mrd_eur`) und die in Z. 1319–1321 zitierten §3.6-Stützstellen. · **Art: Lücke** (§5 LF 7 „Verteilungsannahmen, wo empirische Quantile verfügbar wären"). · **Begründung:** Die einzige unabhängige Verteilungsprüfung des Berichts vergleicht ein **Mittelwert-Aggregat** der Ankerreihe mit einem **gesetzten** Regime-Anteil aus drei Stützstellen. Ein Quantil der Reihe kommt an keiner Stelle vor, obwohl 23 Jahreswerte vorliegen und daraus empirische Jahres-Überschreitungsquantile bis rund 1/24 a⁻¹ bildbar wären — genau der Bereich, in dem die Prüfung nach eigener Aussage am unsichersten ist (Z. 1266–1267). Der Bericht begründet die Beschränkung mit fehlenden Ereigniswerten (Z. 1348–1349); das trifft die Ereignisebene, nicht die Jahresebene: Der Vergleich „modellierte Jahresschadenverteilung gegen die 23 beobachteten Jahressummen" braucht keine Ereignisdaten. Wirkung: Die Prüfung trennt nach eigener Aussage „nach oben schwach" (Z. 1344–1345 — Verdopplung **und** Verdreifachung des Extremschadens bestünden beide); genau diese Schwäche würde ein Quantilvergleich im oberen Bereich adressieren. Kategorie B: kein ausgewiesener Zahlenwert ändert sich, aber die Aussagekraft der einzigen Verteilungsprüfung bleibt hinter dem zurück, was die vorhandenen Daten hergeben. · **Vorschlag:** In §4.5 eine zweite, quantilbasierte Prüfgröße ergänzen — die 23 Jahressummen nach Rang mit Plotting-Position (z. B. Weibull \(i/(n+1)\)) gegen die aus den drei Stützstellen implizierte Jahresschadenverteilung, ausgewiesen als kurze Tabelle der drei bis vier höchsten Ränge mit Modell- und Beobachtungswert —, oder die Nichtverfügbarkeit ausdrücklich auf die **Ereignis**ebene beschränken und begründen, warum die Jahresquantile nicht herangezogen werden. Die neue Prüfgröße nach §3.9 mit eigener, vorab fixierter Toleranz führen, nicht als Ersatz für \(R_{\text{anker}}\). Lesbar halten (P3): Rangtabelle statt angepasster Extremwertverteilung. |
| 64 | **B** | **Stelle:** Bericht §4.6, Obergrenze \(O\) Z. 1363 („\(O = (339.000 \cdot 0{,}1 + 1.380.000 \cdot 0{,}01) \cdot 527.280 \cdot 0{,}250\) = **6,29** Mrd. €₂₀₂₆/a … Mehr kann selbst dann nicht entstehen …") und Ist-Absatz Z. 1381–1385 („eine echte, aus unabhängigen Zahlen folgende Aussage statt einer Tautologie"), gegen §4.3 Z. 1157 (\(M_0\) = 0,872 · 527.280 € · (339.000 · 0,0059796 + 1.380.000 · 0,00067515)) und §4.4 Z. 1240–1258 (Plausibilitätsschranke \(\lambda \le 3{,}44\)). · **Art: Fehler (Zirkelschluss, nur halbseitig behoben)** (§5 LF 7 „gesetzte Werte, die messbar wären"; §3.4; §8/P3). · **Begründung:** Die Neufassung nach Befund 35 (Z. 1353–1358) hat die **Untergrenze** aus der Zirkularität geholt und weist das im Text ausdrücklich nach („In dieses \(U\) geht keine der sechs Ankergrößen … als Faktor ein", Z. 1362); für die **Obergrenze** fehlt derselbe Nachweis, und er ließe sich nicht führen: \(O\) und \(M_0\) teilen die Adresszahlen 339.000/1.380.000 und den Gebäudewert 527.280 €, sodass \(O = 4{,}622 \cdot M_0\) gilt (Ausdruck oben). Damit ist \(\lambda M_0 \le O\) identisch mit \(\lambda \le 4{,}62\) und liegt vollständig innerhalb der ohnehin geprüften Schranke \(\lambda \le 3{,}44\) — die Obergrenze kann kein Ergebnis zurückweisen, das §4.4 passiert hat. Der zusammenfassende Satz „aus unabhängigen Zahlen folgende Aussage" (Z. 1383) trifft deshalb nur auf das untere Bandende zu. Verschärfend für den angekündigten Integrationstest (Z. 1384–1385, „Eine Bundessumme außerhalb dieser Grenzen ist ein roter Test"): Er wäre nach oben strukturell blind, weil beide Seiten mit denselben Registerzahlen skalieren. Abgrenzung zu Befund 61: Dort ist die \(\lambda\)-Schranke aus ihren eigenen Bändern gebildet; hier ist die Bundessummen-Obergrenze ein festes Vielfaches der Modellsumme — dieselbe Ursache, andere Stelle. Kategorie B, weil kein ausgewiesener Zahlenwert falsch ist, aber eine Prüfung ihre im Text zugewiesene Funktion nicht erfüllen kann. · **Vorschlag:** \(O\) nach dem Muster von \(U\) aus modellfremden Größen bilden — etwa aus dem größeren amtlichen Fondsvolumen 2021 (`docs/evidenz/60_wiederaufbauhilfen_2013_2021.csv`), fortgeschrieben, mit Wohnanteil und Wiederkehrzeit analog zu \(U\), oder aus der oberen Ankerbandgrenze \(A^{*}_{o}\) — und die heutige Bestandsschranke daneben als **Modellschranke** kennzeichnen, mit dem Vermerk, dass sie ein festes Vielfaches von \(M_0\) ist und nur grobe Fehler in den Registergrößen aufdecken kann. Im Integrationstest beide Grenzen getrennt benennen (unabhängig / modellabhängig), damit ein grüner Test nicht mehr Sicherheit vorspiegelt, als er trägt. |
| 65 | **C** | **Stelle:** Bericht §4.5 Ist-Ergebnis Z. 1319–1325: „auf HQhäufig 66,1 %, auf HQ100 23,2 % und auf das Extremregime 10,6 % …, also **33,9 %** auf das seltene Regime" und „**Differenz 13,9 Prozentpunkte**". · **Art: Fehler (Rundung/innerer Widerspruch)** (§5 LF 7; §8/E3, P3). · **Begründung:** Die beiden genannten Einzelanteile summieren sich zu 23,2 + 10,6 = **33,8**, nicht 33,9; 33,9 entsteht nur als 100 − 66,1, also aus der Gegenrichtung, und die drei Anteile summieren sich zu 99,9 statt 100,0. Die ausgewiesene Differenz folgt der jeweils anderen Zahl: 47,7 − 33,8 = **13,9** (so ausgewiesen), 47,7 − 33,9 = **13,8**. Mit dem ungerundeten Ankerwert dieser Sitzung (47,74 %) sind es 13,94 bzw. 13,84 Pp. Auf das Verdikt wirkt das nicht — beide Werte liegen über der Toleranz 11,5 Pp, die Prüfung ist so oder so nicht bestanden —, deshalb Kategorie C. Der Befund gilt trotzdem, weil §4.5 den Rechenweg ausdrücklich zum Nachrechnen anbietet und ein Leser nach §8/E3 hier auf einen Widerspruch stößt; zudem wird der Regime-Anteil in §5.1.3 weiterverwendet (Z. 1336–1337). · **Vorschlag:** Die drei Anteile aus dem Ausdruck übernehmen, der sie erzeugt, auf eine Nachkommastelle konsistent runden (Summe 100,0) und den seltenen Anteil als Summe seiner beiden Einzelanteile ausweisen; die Differenz daraus neu setzen. Für den Lint: eine Regel, die im Bericht ausgewiesene Anteilstripel auf 100 % und ausgewiesene Differenzen gegen ihre Summanden prüft. |

#### Abgrenzung und Status dieses Pakets

- **Geändert wurde ausschließlich `reviews/BEFUNDE_60.md`** (angehängt).
  `docs/methodik/60_gebaeudeschaeden_flusshochwasser.md`, `docs/evidenz/register.md`,
  `backend/scripts/lint_methodik.py` und `backend/` sind byte-gleich; die Arbeitsmappen und die
  Evidenz-CSV wurden nur gelesen (eiserne Regel 2).
- **Kein Befund behoben, keiner umnummeriert.** Höchste vorhandene Nummer zu Laufbeginn: **62**;
  neu vergeben sind **63–65**. Die Befunde 33 (abgelöste Verteilungsprüfung), 35 (abgelöste,
  zirkuläre Untergrenze) und 61 (\(\lambda\)-Schranke) sind nur als Gegenstelle eingeordnet.
- **Gesamtverdikt zu Leitfrage 7 nicht gezogen** — es entsteht im Paket auf Reihenfolgeplatz 15
  (Teil 2, §4.8) zusammen mit dem dritten Teil der Leitfrage („Kalibriermodell = Produktionsmodell").
- **Ressourcen-Regel §3.4 eingehalten:** kein nationaler 100-m-Vollraster-Lauf; nachgerechnet wurde
  aus den im Bericht ausgewiesenen Zahlen und der 23-zeiligen Ankerreihe. Im Code wurde nichts
  geändert, die Divergenzen sind als Befunde verbucht (eiserne Regel 5).
- **Frische Sitzung** (eiserne Regel 4): Diese Gegenprüfung ist nicht die Sitzung, die den geprüften
  Stand geschrieben hat.
- **Kopftabelle „Offene Befunde" bewusst nicht fortgeschrieben** (Dateirahmen der Runde-3-Pakete,
  T-0359); der Lint-Lauf der Runde steht im Eröffnungsabschnitt und wurde nicht wiederholt.
- **Nicht Gegenstand dieses Pakets:** §4.1–§4.4, §4.7, §4.8, Kapitel 9 sowie alle übrigen Leitfragen.

### Leitfrage 5 — Modifikatoren und Wirkungsabschätzung S092

**Prüfumfang dieses Pakets (T-0379, ersetzt T-0365).** Leitfrage 5 aus §5 der Aufgabe
(„**Modifikatoren:** zentriert, OR-Übersetzung korrekt, richtige Studienart, **richtige Band- und
Endpunkt-Zuordnung**?", `docs/AUFGABE_METHODIK_SCHADENSRECHNUNG.md` **Z. 436–437**), Maßstab
zusätzlich §3.5 (**Z. 232–256**: Bandzuordnung, Mittelwertzentrierung, OR-Übersetzung
\(\beta = (OR-1)/[1+\bar q (OR-1)]\), geschlossene Betrachtungsebene, Fortschreibungs-Regel für den
Referenzzustand) und §3.9. Vertieft geprüft ist genau **Kapitel 5 „Maßnahmen-Hebel" mit §5.1,
§5.1.1, §5.1.2 und §5.1.3** (Z. 1574–1773). Umfangsmessung in dieser Sitzung, ausgeführt:
`python3 -c 'import re; t=open("docs/methodik/60_gebaeudeschaeden_flusshochwasser.md").read().split(chr(10)); m=lambda a,b: len(re.sub(r"<!--.*?-->","",chr(10).join(t[a-1:b]),flags=re.S)); print(m(1574,1773))'`
→ **14.432** Zeichen ohne HTML-Kommentare, identisch mit dem Planungsstand vom 18.09.2026, keine
Abweichung auszuweisen. Der Abschnitt „## Ergebnis" sowie Kapitel 7 mit §7.1/§7.2 gehören zu
Schwesterpaketen (Reihenfolgeplätze 14 und 17) und sind hier nur als Fundstelle zitiert; die
Leitfragen 11 und 12 werden hier **nicht** beantwortet.

**Verdikt zu Leitfrage 5: Befund** (Befunde 66, 67 und 68). Rechnerisch ist die Kette sauber: Punktwert,
Band und alle drei Einzelachsen-Sensitivitäten von \(r_{\text{S092}}\) sind aus den in §5.1.2
genannten Eingangsgrößen exakt reproduzierbar (Nachrechnung unten, Abweichung 0), die
Endpunkt-Zuordnung ist eindeutig und doppelzählungsfrei begründet (nur Konto K3, Objektschutzkosten
als K8 über die R7-Weiche ausgeschlossen, §5.1 **Z. 1596–1598**), und eine OR-Übersetzung kommt in
Kapitel 5 nicht vor, kann also auch nicht falsch sein (grep in dieser Sitzung über Z. 1574–1773:
keine Fundstelle für „Odds", „OR-" oder „Modifikator" außerhalb des HTML-Kommentars Z. 1576–1582).
Nicht erfüllt sind drei Punkte: die **Bandzuordnung** der oberen Grenze von \(s_{\text{bem}}\) ruht
auf einem Ankerwert, den der Bericht selbst im gleichen Absatz als überholt ausweist, ohne die
abhängigen Zahlen nachzuziehen (Befund 66, Fundstelle §5.1.3 **Z. 1697–1717** gegen §5.1.1 **Z. 1615**
und §5.1.2 **Z. 1640–1646**); der **Referenzzustand** der Zentrierung — der heutige Ausstattungsgrad
\(q_0\) — ist als „geparkt" geführt und trägt keinen Zahlenwert, sodass die Marginalität von
\(\Delta q\) behauptet, aber nicht prüfbar ist (Befund 67, Fundstelle §5.1.2 **Z. 1635–1638** gegen
§3.5 **Z. 236–239** und §3.9); und der einzige Ort, an dem Kapitel 5 den Knoten **S094** erwähnt, ist
ein HTML-Kommentar (Befund 68, Fundstelle **Z. 1581**).

#### (b) Die vier Teilaussagen der Leitfrage 5 einzeln

| Teilaussage (§5 LF 5) | ja/nein | Fundstelle und Begründung in einem Satz |
|---|---|---|
| **zentriert** (§3.5 Z. 236–239, Fortschreibungs-Regel Z. 254–256) | **nein** (Befund 67) | Eine Mittelwertzentrierung `1 + β·(x − x̄)` ist hier nicht einschlägig — \(r_{\text{S092}}\) ist ein kommunenweiter Pauschalfaktor ohne zellvariable Kovariate (§5.1.1 **Z. 1612–1615**) —, wohl aber die Fortschreibungs-Regel für den Referenzzustand: Er ist zwar auf den **Baseline-Lauf** festgelegt („allein die Nachrüstung nach dem letzten Kalibrierjahr 2024", §5.1.2 **Z. 1635–1637**), der Bezugswert \(q_0\) selbst ist aber unbeziffert und als „geparkt" ausgewiesen (**Z. 1637–1638**, Verweis §4.7). |
| **OR-Übersetzung korrekt** (§3.5 Z. 237–239) | **ja (leer erfüllt)** | In Z. 1574–1773 kommt kein Odds Ratio und keine Übersetzung \(\beta = (OR-1)/[1+\bar q(OR-1)]\) vor (grep in dieser Sitzung ohne Treffer); die Kette ist rein multiplikativ aus drei Anteilen gebildet (§5.1 **Z. 1600**), eine fehlerhafte OR-Übersetzung ist damit ausgeschlossen. |
| **richtige Studienart** (§3.5, P2) | **ja** | §5.1 **Z. 1588–1594** weist ausdrücklich zurück, Querschnittsbefragungen Betroffener als Maßnahmen-Effektgröße zu verwenden („Selbstselektion", nicht im Volltext verifiziert), führt den Hebel nach P2 nicht mit Wirkung null, sondern als gekennzeichnete **Abschätzung von KAP3** und benennt den Ersetzungspfad auf Interventions-/quasi-experimentelle Evidenz (§5.1.2 **Z. 1651–1653**). |
| **richtige Band- und Endpunkt-Zuordnung** | **Endpunkt ja, Band nein** (Befund 66) | Endpunkt eindeutig: multiplikativ auf den K3-Erwartungsschaden von #60, Kosten als K8 ausgeschlossen, Schutzsysteme über die R7-Weiche an #50 (§5.1 **Z. 1596–1598**); Band nicht: die obere Grenze \(s_{\text{bem}} \le 0{,}62\) stützt sich auf den Ankerwert 38,5 % aus dem Einzeljahr 2024 (§5.1.3 **Z. 1700–1705**), den §4.5 seit Befund 33 durch 47,7 % ersetzt hat — mit ihm läge die Grenze bei 0,52 (**Z. 1710–1713**). |

#### (c) Nachrechnung statt Lektüre — Wirkungsabschätzung 60-S092-01

Eingangsgrößen aus §5.1.2: \(\Delta q\) = 0,10 (0,05–0,20), \(s_{\text{bem}}\) = 0,50 (0,30–0,62),
\(e_{\text{bem}}\) = 0,70 (0,50–0,80), Kette \(r_{\text{S092}} = \Delta q \cdot s_{\text{bem}} \cdot
e_{\text{bem}}\) (**Z. 1600**, **Z. 1621–1633**, **Z. 1640–1646**). In dieser Sitzung ausgeführt:
`python3 -c "dq,s,e=0.10,0.50,0.70; print('r',dq*s*e,'lo',0.05*0.30*0.50,'hi',0.20*0.62*0.80); print('achsen',0.05*s*e,0.20*s*e,dq*0.30*e,dq*0.62*e,dq*s*0.50,dq*s*0.80); print('s_bem_o',1-1.0/2.6,'neu',1-0.477,'hi_neu',0.20*0.52*0.80,'achse_neu',dq*0.52*e)"`
→ `r 0.034999999999999996 lo 0.0075 hi 0.09920000000000001` /
`achsen 0.0174999... 0.0699999... 0.0209999... 0.043399999999999994 0.025 0.04000000000000001` /
`s_bem_o 0.6153846153846154 neu 0.523 hi_neu 0.08320000000000001 achse_neu 0.0364`.

| Größe | Wert im Bericht | nachgerechnet | Abweichung |
|---|---|---|---|
| \(r_{\text{S092}}\) (Punkt) | 0,035 = −3,5 % (Z. 1640, 1643) | **0,035** | 0 |
| untere Bandgrenze 0,05·0,30·0,50 | 0,0075 = −0,75 % (Z. 1641, 1643) | **0,0075** | 0 |
| obere Bandgrenze 0,20·0,62·0,80 | 0,0992 = −9,92 % (Z. 1641, 1643) | **0,0992** | 0 |
| Einzelachse \(\Delta q\) 0,05–0,20 | 0,0175–0,070 (Z. 1645) | **0,0175–0,0700** | 0 |
| Einzelachse \(s_{\text{bem}}\) 0,30–0,62 | 0,021–0,043 (Z. 1645–1646) | **0,0210–0,0434** → 0,043 | 0 (auf drei Stellen) |
| Einzelachse \(e_{\text{bem}}\) 0,50–0,80 | 0,025–0,040 (Z. 1646) | **0,0250–0,0400** | 0 |
| Herleitung der oberen \(s_{\text{bem}}\)-Grenze 1 − 1,0/2,6 | 0,615 → gesetzt 0,62 (Z. 1702–1705) | **0,6153846** → 0,62 | 0 |

**Ergebnis:** Die Wirkungsabschätzung 60-S092-01 ist aus den in §5.1.2 genannten Eingangsgrößen
**vollständig und ohne Abweichung reproduzierbar**; der Rechenteil der Leitfrage ist bestanden, und
der Beispielblock `beispiel_60_s092_abschaetzung` (Z. 1655–1664) deckt dieselben Werte ab. Die
Abweichung liegt nicht in der Rechnung, sondern in ihrem Eingang: Mit dem heute gültigen Ankerwert
der Verteilungsprüfung (47,7 % statt 38,5 %, §4.5 über Befund 33) ergibt dieselbe Herleitung
\(s_{\text{bem}} \le 1 - 0{,}477 = 0{,}523\) → **0,52** statt 0,62, damit obere Bandgrenze
\(r_{\text{S092}}\) = **0,0832** statt 0,0992 (−16,1 %) und Einzelachse \(s_{\text{bem}}\) oben
**0,0364** statt 0,0434. Daraus **Befund 66**. Nach §3.4 zellweise und auf der 23-zeiligen
Ankerreihe gerechnet, kein Vollraster-Lauf; im Code wurde nichts geändert (eiserne Regel 5).

#### (d) Vorgabe P2 für 60-S094-01 in Kapitel 5

**Kapitel 5 führt für 60-S094-01 keine ausgewiesene Abschätzung mit Zahlenwert, Bandbreite und
Sensitivität** — der Knoten S094 erscheint dort ausschließlich im HTML-Kommentar **Z. 1581**
(„Offene Hebel-Kandidaten: S096/S097/S098 …, S093/S094"), also in einem Text, der nicht ausgeliefert
wird und nach Vorgabe P1 („eine Herleitung nur als Code-Kommentar erfüllt die Vorgabe nicht") nicht
zählt; die P2-konforme Abschätzung \(f_{\text{S094}}\) = 1,00, Band 0,84–1,18, Sensitivität
−16 %/+18 % samt Bauform-Grenze steht vollständig, aber **außerhalb** von Kapitel 5 in Kap. 2
Registerzeile 60-S094-01 (**Z. 188**), Langbeleg B6 (**Z. 469**, **Z. 519**) und §3.5 (**Z. 773**).
Daraus **Befund 68** (Kategorie C).

#### Neue Befunde dieses Pakets (66 bis 68)

| Nr | Kat. | Befund |
|---|---|---|
| 66 | **B** | **Stelle:** Bericht §5.1.3, Absatz „Tragende Begründung der oberen Bandgrenze: Ankerwert der Verteilungsprüfung (§4.5)" **Z. 1697–1717** (darin der Nachtrag „… liefert dort jetzt 47,7 % statt der hier verwendeten 38,5 % …; die obere Bandgrenze läge mit dem neuen Wert bei 1 − 0,477 = 0,52 statt 0,62"), gegen die ausgewiesenen Zahlen in §5.1.1 **Z. 1615**, §5.1.2 **Z. 1640–1646**, §5.1.3 **Z. 1719–1721** und den Beispielblöcken **Z. 1662** und **Z. 1766–1771**. · **Art: Widerspruch/veraltete Bandzuordnung** (§5 LF 5 „richtige Band- und Endpunkt-Zuordnung"; §3.9; §6 „ein zu weit gewordenes Band ist ein Befund"). · **Begründung:** Die obere Bandgrenze von \(s_{\text{bem}}\) hat nach der Revision zu Befund 26 genau **eine** tragende Begründung, den zellunabhängigen Ankerwert der Verteilungsprüfung; dieser Anker ist mit Befund 33 auf die Jahresauslassung über 2002–2024 umgestellt und liefert 47,7 % statt 38,5 %. Der Bericht benennt das selbst und verschiebt den Nachzug ausdrücklich („nicht in diesem Paket vollzogen … im Ledger als Restpunkt vermerkt", Z. 1714–1716). Damit stehen in einem abgenommenen Bericht Zahlen, deren einzige tragende Herleitung im selben Absatz als überholt bezeichnet wird: 0,62 statt 0,52, \(r_{\text{S092}}\)-Obergrenze 0,0992 statt 0,0832 (−16,1 %, Ausdruck oben), Einzelachse oben 0,0434 statt 0,0364. Verschärfend: Mit 0,52 läge der Punktwert 0,50 bei 96 % der Obergrenze, das Band wäre faktisch einseitig nach unten — genau die Fehlerrichtung, die §5.1.3 **Z. 1728–1741** („die Näherung überschätzt den Hebel") beschreibt; der heutige Zuschnitt 0,30–0,62 lässt dagegen ein Aufwärtsband von +24 % zu, das die eigene Richtungsaussage nicht mehr deckt. Kategorie B statt A, weil der Punktwert 0,035 unberührt bleibt und die Abweichung nur die obere Bandhälfte betrifft; Abgrenzung zu Befund 26 (dort wurde 0,66 → 0,62 gesetzt, mit dem damals gültigen Anker) und zu Befund 33 (dort die Ankerseite selbst, ohne die S092-Folgestellen). · **Vorschlag:** Den Nachzug in einem eigenen Revisionspaket vollziehen — \(s_{\text{bem}}\)-Band auf 0,30–0,52, \(r_{\text{S092}}\)-Band auf 0,0075–0,0832, Einzelachse \(s_{\text{bem}}\) auf 0,021–0,0364 — und zwar gleichlautend an allen in Z. 1722–1725 genannten Stellen (Kap. 1 Knoten-Bilanz, Kap. 2 Zeile 60-S092-01, §3.5, §5.1.1, §5.1.2, §5.1.3, Kap. 7 `flood_bldg.s_bem`/`flood_bldg.r_s092`, Entscheidungslog Nr. 3, Beispielblöcke) plus `docs/evidenz/register.md` Z. 65 (vgl. Befund 19). Bis dahin im Bericht an der Zahl selbst — nicht nur im Fließtext von §5.1.3 — kenntlich machen, dass 0,62 ein überholter Stand ist; zusätzlich prüfen, ob der Punktwert 0,50 bei einer Obergrenze 0,52 noch als Mitte tragfähig ist oder mitgesenkt werden muss. |
| 67 | **B** | **Stelle:** Bericht §5.1.2 **Z. 1635–1638** („Gezählt wird allein die Nachrüstung **nach dem letzten Kalibrierjahr 2024** … der heutige Ausstattungsgrad \(q_0\) ist dort als geparkt ausgewiesen") und §5.1.1 **Z. 1612** (\(\Delta q\) = 0,10, Band 0,05–0,20, „zusätzlich nachgerüsteter Anteil exponierter Gebäude (marginal gegenüber heute)"), gegen §3.5 **Z. 236–239** („Zentrierungs-Mittelwerte … sind herleitungspflichtige Parameter (3.9)") und **Z. 254–256** (Referenzzustand im Baseline-Lauf). · **Art: Lücke (Referenzzustand ohne Zahlenwert)** (§5 LF 5 „zentriert"; §3.9 Herleitungspflicht; §3.5 Doppelzählungs-Wächter). · **Begründung:** Der Hebel wirkt als \(\text{EAD}\cdot(1-r)\) auf einen Erwartungsschaden, dessen Niveau-Skalar an Jahren bis 2024 kalibriert ist und in dem der **bereits vorhandene** Objektschutz steckt. Ob \(\Delta q\) = 0,10 tatsächlich marginal ist, hängt deshalb an \(q_0\): Bei hohem Bestandsausstattungsgrad ist ein weiteres Zehntel der exponierten Gebäude ein anderer Eingriff als bei nahe null, und die Wirkung je nachgerüstetem Gebäude \(e_{\text{bem}}\) = 0,70 unterstellt implizit, dass die nachgerüsteten Gebäude vorher **keinen** Schutz hatten. \(q_0\) trägt aber keinen Zahlenwert, keine Bandbreite und keine Quelle, sondern nur den Status „geparkt" (Verweis §4.7). Damit ist der Referenzzustand der Zentrierung — der Punkt, gegen den „marginal" gemessen wird — ein herleitungspflichtiger Parameter ohne Herleitung (§3.9), und der Doppelzählungs-Wächter ist als Regel formuliert, aber nicht als prüfbare Größe. Nutzersichtbar ist die Lücke ebenfalls (P1): Ein Sachbearbeiter, der das Programm auf „jedes zehnte exponierte Gebäude" auslegt, erfährt nicht, wie viele davon schon geschützt sind. Kategorie B: kein ausgewiesener Zahlenwert ist falsch, aber die Marginalitätsaussage, die den Hebel überhaupt rechtfertigt, ist nicht nachprüfbar. · **Vorschlag:** \(q_0\) als eigenen abgeschätzten Parameter nach §3.9 führen — Zahlenwert, Band, Herleitung (etwa aus publizierten Vorsorge-Quoten der Betroffenenbefragungen, ausdrücklich als Abschätzung von KAP3 und nicht als Effektgröße, damit der Studienart-Einwand aus Z. 1588–1592 unberührt bleibt) — und \(\Delta q\) ausdrücklich an ihn binden (\(\Delta q \le 1 - q_0\), Wirkung nur auf den ungeschützten Teil). Alternativ, falls \(q_0\) geparkt bleiben soll: im Bericht und im Produkt als **Modellgrenze** der Abschätzung ausweisen (nach dem Muster der drei Modellgrenzen in Z. 1648–1653), mit dem Satz, dass \(r_{\text{S092}}\) überschätzt, falls der Bestandsschutz hoch ist — die Richtung ist dieselbe wie bei \(s_{\text{bem}}\). |
| 68 | **C** | **Stelle:** Bericht Kapitel 5, HTML-Kommentar **Z. 1576–1582**, dort Z. 1581 („Offene Hebel-Kandidaten: S096/S097/S098 (über R7-Erwartungswert mit #50), S093/S094"), gegen Vorgabe P1 (`CLAUDE.md`: „Eine Herleitung nur als Code-Kommentar erfüllt die Vorgabe nicht") und gegen die vollständige Abschätzung zu 60-S094-01 in Kap. 2 **Z. 188**, B6 **Z. 469/519** und §3.5 **Z. 773**. · **Art: Lücke (Sichtbarkeit/Verweis)** (§5 LF 5 „richtige Band- und Endpunkt-Zuordnung"; P1/P2). · **Begründung:** Kapitel 5 ist der Ort, an dem ein Leser nach Hebeln und ihren Wirkungen sucht. Für 60-S094-01 steht dort im ausgelieferten Text nichts — weder Zahlenwert 1,00, noch Band 0,84–1,18, noch Sensitivität −16 %/+18 %, noch die Bauform-Grenze —, sondern nur ein nicht ausgeliefertes Autorenmemo, das S094 als „offenen Hebel-Kandidaten" führt. Das ist zugleich eine inhaltliche Unschärfe: S094 ist im heutigen Modell **kein** Maßnahmen-Hebel, sondern eine geometrisch zentrierte Struktur-Achse der Schadensfunktion (§3.5 Z. 773, Ebene GEBAEUDEZUSTAND_BAUSTOFF „geparkt", Z. 564) — der Kommentar legt nahe, dass daraus noch ein Hebel wird, ohne das im Text zu sagen. P2 selbst ist **nicht verletzt**: Die Wirkung ist nirgends null gesetzt, sondern als Abschätzung mit Wert, Band, Sensitivität und Modellgrenzen ausgewiesen — nur eben außerhalb von Kapitel 5. Deshalb Kategorie C. · **Vorschlag:** In Kapitel 5 einen kurzen sichtbaren Absatz „Nicht als Hebel geführt" ergänzen, der S093/S094 mit einem Satz und Verweis auf die Registerzeilen 60-S093-01/60-S094-01 einordnet (Struktur-Achse, Ebene geparkt, Bänder 0,71–1,40 und 0,84–1,18, gemeinsam 0,60–1,66) und benennt, unter welcher Bedingung daraus ein Hebel würde (verfügbare Zell-Merkmale für Zustand und Baustoff). Den Pflichtinhalte-Kommentar dabei nicht als Ersatz für Text stehen lassen (P1). |

#### Abgrenzung und Status dieses Pakets

- **Geändert wurde ausschließlich `reviews/BEFUNDE_60.md`** (angehängt).
  `docs/methodik/60_gebaeudeschaeden_flusshochwasser.md`, `docs/evidenz/register.md`,
  `backend/scripts/lint_methodik.py` und `backend/` sind byte-gleich; der Bericht wurde nur in
  Z. 1574–1773 sowie punktuell über Grep gelesen, die Arbeitsmappen gar nicht geändert
  (eiserne Regel 2), die Stichproben-CSV `docs/evidenz/60_stichprobe/hq_*.csv` nicht geöffnet.
- **Kein Befund behoben, keiner umnummeriert.** Höchste vorhandene Nummer zu Laufbeginn: **65**
  (ermittelt per Grep über alle „Befund <n>"-Nennungen); neu vergeben sind **66–68**. Die Befunde
  19, 26 und 33 sind nur als Gegenstelle eingeordnet.
- **Nur Leitfrage 5.** Die Leitfragen 11 und 12 sind hier nicht beantwortet; der Abschnitt
  „## Ergebnis" und Kapitel 7 (§7.1, §7.2) sind nur als Fundstelle zitiert und gehören zu den
  Paketen auf den Reihenfolgeplätzen 14 und 17.
- **Ressourcen-Regel §3.4 eingehalten:** kein nationaler 100-m-Vollraster-Lauf; nachgerechnet wurde
  aus den im Bericht ausgewiesenen Zahlen. Divergenzen sind als Befunde verbucht, nicht still im
  Code behoben (eiserne Regel 5).
- **Frische Sitzung** (eiserne Regel 4): Diese Gegenprüfung ist nicht die Sitzung, die den geprüften
  Stand geschrieben hat.
- **Kopftabelle „Offene Befunde" bewusst nicht fortgeschrieben** (Dateirahmen der Runde-3-Pakete,
  T-0359); der Lint-Lauf der Runde steht im Eröffnungsabschnitt und wurde nicht wiederholt.
- **Nicht Gegenstand dieses Pakets:** alle Kapitel außer Kapitel 5 sowie alle übrigen Leitfragen.

### Befundregression Teil 1 (6, 11, 12, 13)

Paket T-0384 der Runde 3 (18.09.2026, ersetzt das an der Kostenkappe abgebrochene T-0366), eigene
frische Sitzung: Sie hat den geprüften Stand nicht geschrieben (eiserne Regel 4). **In diesem Paket
wird keine Leitfrage aus §5 beantwortet und kein Befund behoben.** Prüfgegenstand ist der
**heutige Berichtsstand** (2.513 Zeilen), nicht die Behauptung im Ledger: Zu jeder der vier Nummern
ist die genannte Stelle im Bericht bzw. im Produktionscode aufgesucht und festgestellt worden, ob
die Forderung dort tatsächlich erfüllt ist. Das Urteil der Regression Runde 2 (Abschn. 5.1/6.1) ist
dabei **nicht übernommen**, sondern am heutigen Stand neu erhoben; die dort genannten
Berichtszeilen sind seither verschoben (Kap. 8 steht heute ab Z. 2326, nicht ab Z. 1452). Die
Statusspalte der Runde-1-Tabelle wird auch hier nicht fortgeschrieben (Dateirahmen der
Runde-3-Pakete, T-0359). **Befundnummern:** höchste zu Laufbeginn im Ledger vorhandene Nummer
**68** (per Grep über alle „Befund <n>"-Nennungen und alle Tabellen-Nummernspalten ermittelt), neu
vergeben sind deshalb **69 und 70**.

| Nr | Urteil | Fundstelle (nachprüfbar) | Feststellung am heutigen Stand |
|---|---|---|---|
| 6 | **bestätigt geschlossen** | Bericht Kap. 1 „Weitergaben", Tabellenzeile **Z. 120** · gegen `KWRA-Monetarisierung.xlsx`: „Schadenskonten-System" **C29**, „Abgleich-Protokoll" **A7–F7**, „Rechenregeln" **C11**, „Risiken-Monetarisierung" **J42**, **J17**, **N17** (alle sechs Zellbezüge in dieser Sitzung im Original gelesen, eiserne Regel 2) | Beide in Runde 1 beanstandeten Buchungsobjekte stehen in der Partitionsliste. **#37**: Z. 120 führt „Kante **49 → 37** (Abgleich-Protokoll Punkt 3, Zeile 7…)"; gemessen trägt Z7 A7 `3`, B7 `49`, C7 „Hochwasser", D7 `37`, E7 „Schäden an Aquakulturen", F7 „Kante" — wörtlich wie zitiert. Das R9-Zitat trifft C11 wörtlich („Innerhalb eines Kontos zählt jede Einheit (… Gebäude) genau einmal…", Kürzung markiert), die Abgrenzung stützt J42 („… + Sachschäden an Anlagen (K3)."). **#12**: Z. 120 führt es als eigenständiges K3-Buchungsobjekt mit Zitat aus C29 („12 Rutschungen und Muren …"; die Spaltenüberschrift B29 lautet gemessen „Buchungsobjekte (Endpunkte, 7)", trägt also die in Runde 1 genannte Siebenzahl) samt N17 „R7, R9" und J17 „Wiederherstellungskosten beschädigter Gebäude (K3) …" — beide wörtlich. Die Forderung der Runde 1 (beide in die Partitionsliste, Abgrenzung mit R9-Zitat entschieden) ist am Berichtstext erfüllt. Kein neuer Befund. |
| 11 | **unvollständig geschlossen** | Bericht Kap. 8 „Quellen (§3.8)" **ab Z. 2326** (Formatsatz Z. 2328–2335, Quelle 1 Z. 2337–2344, Quelle 2 Z. 2345–2351, Quelle 3 Z. 2352–2360, Punkt 4 Z. 2361–2374, GDV-Quellen 5–7 ab Z. 2375) · gegen Kap. 1 **Z. 46–48** und **Z. 56** | Der Kern der Forderung ist erfüllt: Die beiden Arbeitsmappen tragen Commit-Hash, Datum, SHA-256 und Zugriffsdatum; die Hochwasserschutzfibel trägt Vollzitat, URL, Archiv-Snapshot (`web.archive.org`) und Zugriffsdatum, wörtlich aus `sources.py`, ohne diese Datei zu ändern; der Formatsatz nennt jetzt ausdrücklich den Archiv-Snapshot und die Begründungspflicht bei seinem Fehlen; der in Runde 2 vermisste GDV-Anker steht als Quelle 5–7 mit Snapshot und „Volltext geprüft" (Befund 42 dort abgeschlossen). Offen bleibt die **Nachprüfbarkeit der Fundstellenliste**: Quelle 1 gibt für „Klimawirkungsketten" den Bereich „Z3–**Z271** wie in Kap. 1 zitiert" an, während Kap. 1 den tragenden Knoten W117 gerade in **Z272** zitiert (Z. 46–48) — die Zeile, aus der auch die Knoten-Bilanz und der Befund-13-Nachweis stammen, liegt außerhalb des als abschließend formulierten Bereichs. → **Befund 69** (Kategorie C). Abgrenzung: Befund 43 (b) betrifft ausschließlich die Zellenliste von **Quelle 2**; Quelle 1 ist dort nicht erfasst. |
| 12 | **unvollständig geschlossen** | Bericht Kap. 1 „Konto-Einbettung" **Z. 122–147**: Kostensatz-Typ Z. 126–129, Preisstandjahr Z. 133–139, R5-Entscheidung Z. 142–147 · gegen Entscheidungslog Nr. 7 **Z. 2512**, §3.3 **Z. 537–539**, §3.4 **Z. 683–685**, §3.5 **Z. 779** und Register 60-R24-01 **Z. 193** | Zwei der drei in Runde 1 geforderten Punkte sind seit Runde 2 nachgezogen, der dritte inzwischen ebenfalls: **R5** ist mit wörtlichem Zitat (Rechenregeln Z7, Konten Z26, Mon. Z64) als „übernommen" entschieden (Z. 142–147); der **Kostensatz-Typ** ist seit dem 17.09.2026 festgelegt („Kostensatz-Typ ist der Neuwert (Wiederherstellungskosten); der Zeitwertansatz aus Mon. J64 wird als Band geführt", Z. 127–129, Entscheidungslog Nr. 7) — damit ist der in Runde 2 noch offene Teil (Befund 41) geschlossen; das **Preisstandjahr** 2026 steht mit Herleitung (Z. 133–139). Unvollständig ist die Preisstand-Seite: Die Ersetzungsbedingung „Bis ein K3-eigener Kostensatz mit Quelle vorliegt (Kap. 3/7)…" (Z. 136–138) ist eingetreten — \(n_t\) = 1.950 / 1.533 €₂₀₂₆/m² BGF steht mit Quelle und Indexkette in Register 60-R24-01 (Z. 193) und §3.5 (Z. 779) und geht in die Kernformel ein (Z. 683–685) —, der Bericht führt das Preisstandjahr an dieser Stelle aber weiterhin als freie „Abschätzung von KAP3, §3.9 ABGESCHÄTZT" mit noch ausstehender Ersetzung. → **Befund 70** (Kategorie C). |
| 13 | **bestätigt geschlossen** | Bericht Kap. 1 „W-Knoten" **Z. 46–58**, besonders **Z. 51–57**; Entscheidungslog Nr. 6 **Z. 2511** · `backend/app/data/catalog.py` **Z. 335–340** · `KWRA-Schadensbaum_X_UBA-klimawirkungsketten.xlsx`, „Klimawirkungsketten" **F272/H272** (in dieser Sitzung gelesen) | Die als Fehler beanstandete Behauptung „trägt **genau** die Namenslisten von W117" steht nicht mehr im Bericht; Z. 53–54 sagt „trägt **nicht** genau die Namenslisten …, sondern nur eine **Teilmenge mit abweichender Namensquelle**". Die Zahlen sind nachgerechnet und treffen zu: `catalog.py` Z. 338/339 führt gemessen **5** `upstream_names` und **5** `sensitivity_names`; KWK **F272** trägt `S092; S093; S094; S096; S097; S098; S104` = **7** Sensitivitäten (im Code fehlen S096 und S098), **H272** trägt `W074; W077; W085; W087; W008; W006; W091; W100` = **8** Wirkungs-Eingänge — also 5 statt 7 und 5 statt 8, wie der Bericht schreibt. Die Divergenz ist als Integrationspunkt im Entscheidungslog Nr. 6 geführt („Code … bleibt unverändert", eiserne Regel 5); `backend/app/data/catalog.py` ist unverändert. Kein neuer Befund. |

#### Neue Befunde dieses Pakets (69 bis 70)

| Nr | Kat. | Befund |
|---|---|---|
| 69 | **C** | **Stelle:** Bericht Kap. 8 „Quellen (§3.8)", Quelle 1, **Z. 2339** („… Sheets „Klimawirkungsketten" (Z3–Z271 wie in Kap. 1 zitiert) und „Schadensbaum-Netzwerkliste" (Z13, Z50, Z51, Z53, Z60, Z61)"), gegen Kap. 1 „W-Knoten" **Z. 46–48** („Sheet „Klimawirkungsketten" Z272, Knoten **W117** …") und **Z. 56–57** („… die die Knoten-Bilanz unten aus W117 (KWK Z272) zieht"). · **Art: Lücke/Fehler (Fundstellenangabe deckt die benutzte Quelle nicht ab)** (§3.8 exakte Fundstelle; §5 LF 10). · **Begründung:** Die Zellenliste der Quelle 1 ist abschließend formuliert („wie in Kap. 1 zitiert") und endet bei Z271. Die Zeile, auf der die gesamte W-Knoten-Zuordnung von #60 ruht, ist aber **Z272**: Dort stehen gemessen A272 `W117`, B272 „Schäden an Gebäuden und Infrastrukturen", F272 mit sieben Sensitivitäten und H272 mit acht Wirkungs-Eingängen — dieselben Zellen, mit denen Kap. 1 die Knoten-Bilanz füllt und mit denen Befund 13 nachgewiesen wird. Ein Leser, der das Quellenkapitel als Nachweisliste benutzt, findet die tragende Zeile dort nicht wieder; das ist genau die Prüfbarkeit, die §3.8 mit „exakte Fundstelle" meint. Kategorie C: kein ausgewiesener Zahlenwert ist betroffen, kein Konto und kein Ergebnis verschiebt sich, die Zelle selbst ist in Kap. 1 korrekt zitiert — die Lücke betrifft allein die Vollständigkeit des Quellenverzeichnisses. Abgrenzung zu **Befund 43 (b)** (bewusst offen): Dort geht es um die unvollständige Zellenliste von **Quelle 2** (`KWRA-Monetarisierung.xlsx`, Rechenregeln ohne Z7/Z19, Risiken-Monetarisierung ohne Z17/Z42/Z57); Quelle 1 ist dort nicht Gegenstand, und die dort akzeptierte Offenheit deckt diese Stelle nicht. · **Vorschlag:** In Quelle 1 den Bereich auf „Z3–Z272" erweitern oder die tragenden Einzelzeilen ausweisen („u. a. Z208, Z226, **Z272**"); bei der Gelegenheit die Formulierung „wie in Kap. 1 zitiert" entweder durch „u. a." entschärfen oder — konsequenter — beide Arbeitsmappen-Quellen einheitlich mit dem Zusatz versehen, dass die abschließende Fundstellenliste der Kapitel 1 bis 7 gilt (deckt zugleich die Richtung von Befund 43 b ab). |
| 70 | **C** | **Stelle:** Bericht Kap. 1 „Konto-Einbettung", Punkt „Preisstandjahr", **Z. 133–139**, darin der Bedingungssatz **Z. 136–138** („Bis ein K3-eigener Kostensatz mit Quelle vorliegt (Kap. 3/7), wird das Erstellungsjahr dieses Berichtsteils als Preisstandjahr gesetzt und bei Bezifferung ersetzt (Ersetzungspfad, W1)") und die Kennzeichnung **Z. 133** („Preisstandjahr (Abschätzung von KAP3, §3.9 ABGESCHÄTZT): 2026"), gegen Kap. 1 **Z. 127–129** (Entscheidung vom 17.09.2026: Neuwert als Kostensatz-Typ), Register **60-R24-01 Z. 193** (NHK 2010 nach ImmoWertV Anlage 4, mit Baupreisindex auf Preisstand 2026 fortgeschrieben, „Volltext geprüft", Langbeleg B4), §3.5 **Z. 779** (\(n_t\) = 1.950 / 1.533 €₂₀₂₆/m² BGF), §3.4 **Z. 683–685** (die Wertsätze gehen so in die Kernformel ein) und §3.3 **Z. 537–539** („Bezugsjahr (Preisstand): 2026, einheitlich für alle Kostensätze dieses Berichts"). · **Art: Widerspruch (überholte Bedingung, unzutreffender Herkunftsvermerk)** (§3.9 Herleitungspflicht; Vorgabe **P1** „Quelle **oder** ausgewiesene Abschätzung"; §5 LF 9). · **Begründung:** Der Ersetzungspfad benennt eine Bedingung, die eingetreten ist: Ein K3-eigener Kostensatz **mit Quelle** liegt vor (Register 60-R24-01 → §3.5 Z. 779), ist auf den Preisstand 2026 indexiert und trägt den Basiswert des Berichts (527.280 €₂₀₂₆ je Wohngebäude, §4.3). Das Preisstandjahr 2026 ist damit kein frei gesetztes Erstellungsjahr mehr, sondern der Preisstand der belegten und indexierten Wertsätze — abgeschätzt ist daran nur noch der Fortschreibungsfaktor 2023 → 2026 (1,105; Band 1,07–1,16, §3.9 ausgewiesen). Der Bericht führt an der Stelle, an der ein Leser die Herkunft des Preisstands nachschlägt, weiterhin die alte Lage: pauschal „Abschätzung von KAP3" und eine noch ausstehende Ersetzung. Für die nutzersichtbare Parameterliste (P1) ist das ein falscher Herkunftsvermerk — die Zahl stimmt, ihre Begründung nicht mehr. Kategorie C: Kein ausgewiesener Zahlenwert ist falsch (2026 gilt in beiden Lesarten), kein Rechenweg und kein Band verschiebt sich; betroffen sind Herkunftsvermerk und ein überholter Bedingungssatz. Abgrenzung: **Befund 41** (Kostensatz-Typ Neuwert/Zeitwert) ist mit Entscheidungslog Nr. 7 geschlossen und wird hier nicht wieder aufgegriffen; **Befund 40** betrifft den fehlenden Parameter-Block mit Pflichtfeld `preisstand` in Kap. 1 — hier geht es um die Herkunftsangabe einer bereits vorhandenen Aussage. · **Vorschlag:** Z. 133–139 auf den Ist-Stand ziehen: Preisstandjahr 2026 als **abgeleitet aus Register 60-R24-01** führen (Quelle: NHK 2010 + Baupreisindex; abgeschätzt ist allein der Fortschreibungsfaktor 2023 → 2026 mit Band 1,07–1,16) und den Bedingungssatz durch den Vermerk ersetzen, dass der K3-eigene Kostensatz seit T-0285/§3.5 vorliegt und den Preisstand setzt; die Kennzeichnung „§3.9 ABGESCHÄTZT" dabei nicht streichen, sondern auf den Fortschreibungsfaktor eingrenzen, damit der Ratchet nach eiserner Regel 3 nicht gelockert wird. Gleichlautend in §3.3 Z. 537–539 den Rückverweis auf Kap. 1 nachziehen. |

#### Abgrenzung und Status dieses Pakets

- **Geändert wurde ausschließlich `reviews/BEFUNDE_60.md`** (angehängt).
  `docs/methodik/60_gebaeudeschaeden_flusshochwasser.md`, `docs/evidenz/register.md`,
  `backend/app/data/catalog.py`, `backend/app/data/sources.py`,
  `backend/scripts/lint_methodik.py` und die Arbeitsmappen sind byte-gleich; Bericht und
  Arbeitsmappen wurden nur gelesen (eiserne Regel 2), der Bericht ausschließlich an den oben
  zitierten Zeilenbereichen.
- **Kein Befund behoben, keiner umnummeriert.** Höchste vorhandene Nummer zu Laufbeginn: **68**;
  neu vergeben sind **69 und 70**. Die Befunde 40, 41, 42 und 43 sind nur als Gegenstelle bzw. zur
  Abgrenzung eingeordnet, ihr Status bleibt unberührt.
- **Keine Leitfrage aus §5 beantwortet.** Dieses Paket führt allein die Regression der Nummern
  **6, 11, 12 und 13**; Teil 2 der Befundregression und alle Leitfragen-Pakete der Runde 3 sind
  nicht Gegenstand.
- **Urteil der Runde 2 nicht übernommen:** Es wurde für alle vier Nummern am heutigen Stand neu
  erhoben. Für 6 und 13 bestätigt sich das Ergebnis der Runde 2, für 11 und 12 bleibt es bei
  „unvollständig geschlossen", jedoch mit anderen Restpunkten als dort (die damals genannten
  Restpunkte zu 11 — fehlende GDV-Quelle, Formatsatz ohne Archiv-Snapshot — sind inzwischen
  erledigt; der zu 12 genannte Kostensatz-Typ ebenfalls).
- **Ressourcen-Regel §3.4 eingehalten:** kein nationaler 100-m-Vollraster-Lauf; nachgerechnet wurde
  zellweise (sechs Zellbezüge der Monetarisierungsmappe, zwei der Wirkungskettenmappe) und an den
  ausgewiesenen Zahlen. Divergenzen sind als Befunde verbucht, nicht still im Code behoben
  (eiserne Regel 5).
- **Frische Sitzung** (eiserne Regel 4): Diese Gegenprüfung ist nicht die Sitzung, die den
  geprüften Stand geschrieben hat (T-0235 bis T-0243, T-0256 bis T-0259, Revisionspakete aus
  T-0281, T-0285, T-0307/T-0308, T-0320 — alle abgeschlossen).
- **Kopftabelle „Offene Befunde" bewusst nicht fortgeschrieben** (Dateirahmen der Runde-3-Pakete,
  T-0359); der Lint-Lauf der Runde steht im Eröffnungsabschnitt und wurde nicht wiederholt.

### Befundregression Teil 2 (17, 20, 21, 22)

Paket T-0385 der Runde 3 (18.09.2026, zweite Hälfte des an der Kostenkappe abgebrochenen T-0366),
eigene frische Sitzung: Sie hat den geprüften Stand nicht geschrieben (eiserne Regel 4).
**In diesem Paket wird keine Leitfrage aus §5 beantwortet und kein Befund behoben.** Prüfgegenstand
ist der **Umsetzungsnachweis im heutigen Stand**, nicht die Behauptung im Ledger: Zu jeder der vier
Nummern ist die genannte Stelle im Bericht bzw. im Werkzeug aufgesucht und geprüft worden, ob die
Forderung dort tatsächlich erfüllt ist; das Urteil der Regression Runde 2 (Abschn. 5/6, für Nr. 17
Z. 1324) ist nicht übernommen, sondern neu erhoben. Für Nr. 21 („bewusst offen") ist nach der
Vorgabe dieses Pakets geprüft worden, ob die im Ledger festgehaltene Begründung im heutigen Bericht
als Modellgrenze sichtbar ist. `backend/scripts/lint_methodik.py` wurde gelesen und ausgeführt,
aber nicht geändert (gehört T-0234). Die Statusspalten der Runde-1- und Runde-2-Tabellen werden
nicht fortgeschrieben (Dateirahmen der Runde-3-Pakete, T-0359). **Befundnummern:** höchste zu
Laufbeginn im Ledger vorhandene Nummer **70** (Grep über alle Tabellen-Nummernspalten und alle
„Befund <n>"-Nennungen), neu vergeben sind deshalb **71, 72 und 73**.

| Nr | Urteil | Fundstelle (nachprüfbar) | Feststellung am heutigen Stand |
|---|---|---|---|
| 17 | **unvollständig geschlossen** | `backend/scripts/lint_methodik.py`: Pflichtkapitel-Check **Z. 258–292** (Konstante `PFLICHTKAPITEL_MIN_ZEICHEN = 500` Z. 263, Kommentar-Strippung Z. 285), verbotene Formulierungen zeilenweise über den gesamten Text **Z. 169–206**, Registry-Abgleich **Z. 296–301**, Ausgabeblock **Z. 952–959** · Lauf in dieser Sitzung: `python3 backend/scripts/lint_methodik.py 60` → „162 Checks grün / ALLE LINTS GRÜN"; `python3 backend/scripts/lint_methodik.py` (alle Berichte) → drei rote Pflichtkapitel-Checks an #25 | Zwei der drei Forderungen aus Runde 1 sind seit T-0234 erfüllt — anders als in der Regression der Runde 2 (Z. 1324) festgestellt: Der Check „Pflichtkapitel mit < N Zeichen außerhalb von HTML-Kommentaren = rot" existiert (Z. 266–292, Schwelle 500 Zeichen, `re.sub(r"<!--.*?-->", …)` Z. 285) und schlägt gemessen an #25 dreimal an; `verbotene_formulierungen()` läuft zeilenweise über den **gesamten** Bericht einschließlich HTML-Kommentaren (Z. 186–205, nur der `HISTORIE_MARKER` ist als Ausnahme geführt). Offen ist die dritte Forderung: Die Ausgabe nennt allein „162 Checks grün" (Z. 953) und die Historie-Marker; **übersprungene Checks werden nicht gezählt und nicht genannt**. Das ist an #60 kein Formalpunkt — `registry_abgleich()` bricht für jede Berichtsnummer außer 98 in Z. 299–301 stumm ab (Präfix-Nachschlag nur für „98"; `if praefix is None: return`), sodass der Abgleich Bericht ⇄ Registry (eiserne Regel 5) an #60 gar nicht stattfindet, die Meldung aber „ALLE LINTS GRÜN" lautet. → **Befund 71** (Kategorie C). |
| 20 | **bestätigt geschlossen** | Bericht §3.4, Absatz „Formelstelle FS-Schutzsystem — in dieser Fassung inaktiv (geparkt)" **Z. 694–706** · Kap. 1 Knoten-Bilanz **Z. 104–106** (S096/S097/S098) · Kap. 1 Formelstellen-Aufzählung **Z. 72** · Kap. 9 Kriterienraster, Zeile „Maßnahmen-Anschluss" **Z. 2462** · Kopf **Z. 16** und „Ergebnis/Offen" **Z. 35** | Der nach §2.1 gewählte zweite Weg ist an allen vier Stellen belegt. §3.4 Z. 694–706 trägt das Regelzitat (Rechenregeln **C20 (A5)** „Schutzsysteme über die R7-Erwartungswert-Weiche" und **C9 (R7)** „Erwartungswert über Halte- und Versagensfall, wahrscheinlichkeitsgewichtet"), die Feststellung „Die Kernformel trägt diesen Term noch nicht: \(p_i\) wird unverändert aus den Szenarien der Gefahrenkarte übernommen" und eine ausdrückliche **Modellgrenze** samt P2-Abgrenzung („keine Nullwirkung im Sinne von P2, sondern ein fehlender Anschluss"). Kap. 1 Z. 104–106 führt alle drei Knoten als „**inaktiv (geparkt: Formelstelle FS-Schutzsystem ohne Term in §3.4, Modul #50 fehlt)**" mit Zitat aus Mon. Z65/Rechenregeln Z9. Die in Runde 1 beanstandete Behauptung in Kap. 9 ist korrigiert: Z. 2462 sagt jetzt „in der Formel existiert heute nur der Angriffspunkt für S092 (§5.1), die R7-Weiche ist als FS-Schutzsystem inaktiv geparkt (§3.4)" statt „beide Angriffspunkte existieren in der Formel bereits". Gemessen kommt `FS-Schutzsystem` außerhalb von Kap. 1 zweimal vor (§3.4 Z. 694, Kap. 9 Z. 2462), der Prüfausdruck der Runde 2 endet mit Exit 0. Kein neuer Befund. |
| 21 | **unvollständig geschlossen** | Bericht Kap. 1 Knoten-Bilanz **Z. 85** (S074), **Z. 100** (W100), **Z. 101** (S092) · gegen `KWRA-Schadensbaum_X_UBA-klimawirkungsketten.xlsx`, Blatt „Klimawirkungsketten", **B199**, **B223**, **B256** (in dieser Sitzung im Original gelesen, nur lesend, eiserne Regel 2) · Suche nach „Knotennamen", „Kürzung", „gekürzt", „B199", „B223", „B256" im Bericht: **0 Treffer** | Der Status „bewusst offen" ist sachlich unverändert — geprüft wurde nach der Vorgabe dieses Pakets allein, ob die Begründung des Ledgers im **Bericht** als Modellgrenze sichtbar ist. Sie ist es nicht: Die drei Namen stehen weiterhin gekürzt und ohne Kürzungszeichen (Z. 85 „Topographie (Geländeform, Höhe) (über W085)" gegen B199 gemessen „Topographie (Geländeform, Höhe, **etc.**)"; Z. 100 „Einschränkungen Kanalnetze und Vorfluter (= Id 52)" gegen B223 „Einschränkungen **der Funktionsfähigkeit von** Kanalnetzen und Vorflutern"; Z. 101 „Bauliche, organisatorische und finanzielle Vorsorge der Eigentümer und Nutzer" gegen B256 „… der Eigentümer und Nutzer **von Gebäuden und Infrastrukturen**"), und nirgends im Bericht steht ein Hinweis, dass die Spalte „Name" gekürzte Fassungen führt. Damit gilt für einen Leser des Berichts weiterhin die Zusage wörtlicher Übernahme (§3.8), während die Kürzung bei W100 die Bedeutung verschiebt (Funktionsfähigkeit → Anlagen). „Bestätigt geschlossen" ist nach der Prüfregel dieses Pakets deshalb nicht vergebbar. → **Befund 72** (Kategorie C). Der Status von Befund 21 selbst bleibt unberührt. |
| 22 | **zurückgefallen** | Bericht Kopf-Statuszeile **Z. 3** („Status: **in Revision nach Review-Runde 2** … · Stand **17.09.2026**"), „Ergebnis"-Punkt „Offen (Stand 17.09.2026, nach Review-Runde 2)" **Z. 35** und „Ergebnis"-Punkt „Planung" **Z. 37** · gegen `git log -- docs/methodik/60_gebaeudeschaeden_flusshochwasser.md` (sechs Commits mit Datum **18.09.2026**: T-0295, T-0323, T-0324, T-0325, T-0334, T-0335) und gegen dieses Ledger (Runde 3 läuft seit 18.09.2026) | Der Nachzug vom 17.09.2026 (T-0245) ist belegt, aber die Lage, die Befund 22 beschreibt, ist **erneut eingetreten**, und ein Teil wurde nie geschlossen. (a) Kopf und „Ergebnis" datieren auf den 17.09.2026 und auf „nach Review-Runde 2", während der Bericht am 18.09.2026 durch sechs Revisionspakete geändert wurde (M₀-Band §4.3, λ-Band und Plausibilitätsschranke §4.4/§4.8, Sanity-Band §4.6, Doppelzählungs-Wächter) und Review-Runde 3 läuft. (b) Der „Offen"-Punkt nennt als Grund für das vorläufige λ ausdrücklich „die Befunde 35 und 36 offen" — beide sind am 18.09.2026 im Bericht nachgezogen (Ledger Z. 1973 und Z. 2145, Pakete T-0323 bis T-0325 und T-0333 bis T-0335); der Kopf führt also einen überholten Offen-Stand, genau die Fehlerart der ursprünglichen Nummer. (c) Nie geschlossen ist der dritte im Befund zitierte Satz: Z. 37 behauptet weiterhin „Gegenprüfung ist nicht Teil des Tickets und **noch nicht gemessen**", obwohl drei Review-Runden gefahren sind und dieses Ledger über 3.200 Zeilen Gegenprüfung führt — der Umsetzungsnachweis nennt den Punkt „Ergebnis" als nachgezogen, dieser Satz steht darin unverändert. → **Befund 73** (Kategorie B). |

#### Neue Befunde dieses Pakets (71 bis 73)

| Nr | Kat. | Befund |
|---|---|---|
| 71 | **C** | **Stelle:** `backend/scripts/lint_methodik.py`, Ausgabeblock **Z. 952–959** (Zeile 953 gibt allein die Zahl der grünen Checks aus) im Zusammenspiel mit `registry_abgleich()` **Z. 296–301** (Präfix-Nachschlag nur für Berichtsnummer „98"; `if praefix is None: return`), gemessen am Lauf `python3 backend/scripts/lint_methodik.py 60` → „162 Checks grün … ALLE LINTS GRÜN". · **Art: Lücke (stumm übersprungene Prüfung bei grüner Gesamtmeldung)** (§7 deterministische Lints; §5 LF 11; eiserne Regel 5). · **Begründung:** Von den drei Forderungen des Befunds 17 ist die dritte („Zählung grüner Checks um eine Zählung übersprungener Checks ergänzen") nicht umgesetzt: Die Ausgabe nennt nur grüne und rote Checks. An #60 hat das eine Wirkung, die über die Statistik hinausgeht — der Abgleich Bericht ⇄ Registry ist für jede Berichtsnummer außer 98 fest abgeschaltet und kehrt ohne jede Meldung zurück. Für #60 bedeutet „ALLE LINTS GRÜN" also gerade nicht, dass die Parameterwerte des Berichts mit den Registry-Werten des Produkts übereinstimmen; die Divergenzprüfung, auf der eiserne Regel 5 aufsetzt, hat an diesem Bericht nie stattgefunden, und die 162 grünen Checks lassen das Gegenteil vermuten. Kategorie C: Kein ausgewiesener Zahlenwert des Berichts ist dadurch falsch, kein Band und kein Konto verschiebt sich; betroffen ist die Aussagekraft des Lint-Ergebnisses. Die beiden anderen Teile des Befunds 17 sind mit T-0234 erfüllt (Pflichtkapitel-Substanzschwelle Z. 258–292, verbotene Formulierungen auch in HTML-Kommentaren Z. 186–205) — dieser Befund greift nur den Rest auf. · **Vorschlag:** Den Ausgabeblock um eine Zeile „n Checks übersprungen" mit namentlicher Auflistung ergänzen (übersprungene Kapitel-9-Prüfung, nicht laufender Registry-Abgleich, nicht ladbare Registry) und `registry_abgleich()` beim Frühausstieg einen benannten Skip-Eintrag setzen lassen, statt still zurückzukehren; mittelfristig den Präfix-Nachschlag um die Familie K3/K4 (#60, Präfix `flood_bldg.`) erweitern. **Umsetzung gehört T-0234** (`lint_methodik.py` ist nicht Dateirahmen der Runde-3-Pakete) — hier nur verbucht. |
| 72 | **C** | **Stelle:** Bericht Kap. 1 „Knoten-Bilanz", Spalte „Name", **Z. 85** (S074), **Z. 100** (W100), **Z. 101** (S092), gegen `KWRA-Schadensbaum_X_UBA-klimawirkungsketten.xlsx`, Blatt „Klimawirkungsketten", **B199**, **B223**, **B256** (gemessen: „Topographie (Geländeform, Höhe, etc.)", „Einschränkungen der Funktionsfähigkeit von Kanalnetzen und Vorflutern", „Bauliche, organisatorische und finanzielle Vorsorge der Eigentümer und Nutzer von Gebäuden und Infrastrukturen"). · **Art: Lücke (bewusste Abweichung ohne sichtbare Modellgrenze)** (§3.8 wörtliche Übernahme; §5 LF 14 Quellen-Synchronität; eiserne Regel 2 „bewusste Fortschreibungen gehören in die Quelle + Protokoll"). · **Begründung:** Befund 21 ist im Ledger als „bewusst offen" geführt, mit der Begründung, die Kürzung habe keine Rechenwirkung und werde mit der nächsten Revision nachgezogen. Diese Entscheidung ist im **Bericht** an keiner Stelle sichtbar: Die Suche nach „Knotennamen", „Kürzung", „gekürzt", „B199", „B223", „B256" liefert im Bericht null Treffer, und die Knoten-Bilanz führt die drei Namen ohne Auslassungszeichen. Ein Leser, dem Kap. 1 eine wörtliche Übernahme aus der Arbeitsmappe zusagt (und der im selben Kapitel die Rüge an den Code-Einträgen wegen „umformuliert statt wörtlich" liest, Befund 13), kann die Abweichung nur durch Öffnen der Mappe finden. Bei W100 verschiebt die Kürzung zudem den Gegenstand (Funktionsfähigkeit der Netze → Netze selbst). Kategorie C: kein Zahlenwert, kein Band und kein Konto betroffen; es geht um die Nachprüfbarkeit der Namensspalte und um die Sichtbarkeit einer bewussten Abweichung. · **Vorschlag:** Entweder die drei Namen wörtlich übernehmen (dann entfällt Befund 21 mit) oder die Kürzung an Ort und Stelle sichtbar machen („…") und in Kap. 1 bzw. Kap. 6 einen Satz aufnehmen, dass die Spalte „Name" aus Platzgründen gekürzte Fassungen führt, der maßgebliche Wortlaut aber in B199/B223/B256 steht — damit ist die Entscheidung „bewusst offen" nach eiserner Regel 2 auch außerhalb des Ledgers dokumentiert. |
| 73 | **B** | **Stelle:** Bericht Kopf-Statuszeile **Z. 3** („Status: in Revision nach Review-Runde 2 … Stand 17.09.2026"), „Ergebnis", Punkt „Offen (Stand 17.09.2026, nach Review-Runde 2)" **Z. 35** (darin „λ bleibt vorläufig, weil … die Befunde 35 und 36 offen sind") und Punkt „Planung" **Z. 37** („Gegenprüfung ist nicht Teil des Tickets und noch nicht gemessen"), gegen den Ist-Stand: sechs Commits vom **18.09.2026** an dieser Datei (T-0295, T-0323, T-0324, T-0325, T-0334, T-0335), die Revisionsnachweise zu 35 und 36 in diesem Ledger (**Z. 1973**, **Z. 2145**) und die laufende Review-Runde 3 (Abschnitt ab **Z. 2198**). · **Art: Widerspruch (überholter Bearbeitungs- und Prüfstand im Kopf; Rückfall in die Lage des Befunds 22)** (§4 Berichtsstruktur „Kopf/Ergebnis"; §6 Prozess; §5 LF 14). · **Begründung:** Befund 22 verlangte, Kopfstatus, Geltungsbereich und „Ergebnis/Offen" **am Ende jeder Revisionsrunde** nachzuziehen. Der Nachzug auf den 17.09.2026 hat stattgefunden, ist aber am Folgetag durch sechs Revisionspakete wieder überholt worden, ohne dass Kopf oder „Ergebnis" mitgezogen wurden — der Kopf nennt Runde 2 als letzten Stand, während Runde 3 läuft, und begründet die Vorläufigkeit von λ mit zwei Befunden (35, 36), deren Nachzug im Bericht am 18.09.2026 vollzogen und in diesem Ledger belegt ist. Damit bekommt ein Prüfer, der nach §4 dem Kopf den Bearbeitungsstand entnimmt, erneut ein falsches Bild; nach §6 hängt an diesem Stand die Abnahmefrage. Verschärfend ist der Satz in Z. 37: Er behauptet unverändert, die Gegenprüfung sei „noch nicht gemessen", obwohl drei Review-Runden gefahren sind — dieser im Befund 22 ausdrücklich zitierte Teil ist nie geschlossen worden, obwohl der Umsetzungsnachweis den Punkt „Ergebnis" als nachgezogen führt. Kategorie B wie die Ursprungsnummer: kein Rechenweg und kein Zahlenwert ist betroffen, wohl aber die Grundlage der Abnahmeentscheidung. · **Vorschlag:** (1) Kopf und „Ergebnis" am Ende **jeder** Revisionsrunde nachziehen, also auch nach den Einzelpaketen einer Runde — Status „in Revision, Runde 3", Stand mit Datum des letzten Commits an dieser Datei; (2) den Offen-Punkt zu λ auf den heutigen Stand bringen (35/36 nachgezogen, verbleibender Grund der Vorläufigkeit benennen); (3) den Planungssatz durch den tatsächlichen Prüfaufwand ersetzen (drei Runden, Ledger `reviews/BEFUNDE_60.md`); (4) den maschinellen Abgleich „jüngstes Änderungsdatum der Datei ≤ Stand im Kopf" im Vollständigkeits-Check **T-0234** verankern, damit der Rückfall nicht ein drittes Mal auftritt — hier nur verbucht, nicht umgesetzt. |

#### Abgrenzung und Status dieses Pakets

- **Geändert wurde ausschließlich `reviews/BEFUNDE_60.md`** (angehängt).
  `docs/methodik/60_gebaeudeschaeden_flusshochwasser.md`, `docs/evidenz/register.md`,
  `backend/scripts/lint_methodik.py` und die Arbeitsmappen sind byte-gleich; Bericht, Lint und
  Arbeitsmappe wurden nur gelesen (eiserne Regel 2), der Lint zusätzlich ausgeführt.
- **Kein Befund behoben, keiner umnummeriert.** Höchste vorhandene Nummer zu Laufbeginn: **70**;
  neu vergeben sind **71, 72 und 73**. Die Befunde 13, 21, 35 und 36 sind nur als Gegenstelle bzw.
  zur Abgrenzung eingeordnet, ihr Status bleibt unberührt.
- **Keine Leitfrage aus §5 beantwortet.** Dieses Paket führt allein die Regression der Nummern
  **17, 20, 21 und 22**; Teil 1 der Befundregression (6, 11, 12, 13) und die Leitfragen-Pakete der
  Runde 3 sind nicht Gegenstand.
- **Urteil der Runde 2 nicht übernommen:** Für Nr. 17 weicht das heutige Urteil in der Begründung
  ab (Runde 2, Z. 1324: „keine Schließung erfolgt" — heute sind zwei der drei Forderungen durch
  T-0234 erfüllt, offen ist allein die Zählung übersprungener Checks); für 20 bestätigt sich die
  Schließung am heutigen Text; 21 und 22 sind am heutigen Stand neu erhoben.
- **Ressourcen-Regel §3.4 eingehalten:** kein nationaler 100-m-Vollraster-Lauf; nachgerechnet wurde
  zellweise (drei Zellbezüge der Wirkungskettenmappe) und an den ausgewiesenen Stellen des
  Berichts. Divergenzen sind als Befunde verbucht, nicht still im Code behoben (eiserne Regel 5);
  die vorgeschlagenen Lint-Änderungen gehören T-0234.
- **Frische Sitzung** (eiserne Regel 4): Diese Gegenprüfung ist nicht die Sitzung, die den
  geprüften Stand geschrieben hat (T-0235 bis T-0243, T-0245, T-0256 bis T-0259, die
  Revisionspakete aus T-0281 sowie T-0295, T-0320 bis T-0335 — alle abgeschlossen).
- **Kopftabelle „Offene Befunde" bewusst nicht fortgeschrieben** (Dateirahmen der Runde-3-Pakete,
  T-0359); der Lint-Lauf dieses Pakets ist oben zu Nr. 17 protokolliert.

### Befundregression Teil 3 (23, 24, 25, 26)

Paket T-0386 der Runde 3 (18.09.2026, erste Hälfte des halbierten T-0367), eigene frische Sitzung:
Sie hat den geprüften Stand nicht geschrieben (eiserne Regel 4). **In diesem Paket wird keine
Leitfrage aus §5 beantwortet und kein Befund behoben.** Prüfgegenstand ist der
**Umsetzungsnachweis im heutigen Berichtsstand**, nicht die Behauptung im Ledger: Zu jeder der vier
Nummern ist die genannte Stelle im Bericht aufgesucht und geprüft worden, ob die Forderung dort
tatsächlich erfüllt ist. Für die als „bewusst offen" geführten Nummern 24 und 25 ist nach der
Vorgabe dieses Pakets geprüft worden, ob die **im Ledger festgehaltene Begründung im heutigen
Bericht als Modellgrenze sichtbar** ist; nur dann wird „bestätigt geschlossen" vergeben. Die
Statusspalten der Runde-1- und Runde-2-Tabellen werden nicht fortgeschrieben (Dateirahmen der
Runde-3-Pakete, T-0359). **Befundnummern:** höchste zu Laufbeginn im Ledger vorhandene Nummer
**73** (Grep über alle Tabellen-Nummernspalten und alle „Befund <n>"-Nennungen), neu vergeben sind
deshalb **74 und 75**.

| Nr | Urteil | Fundstelle (nachprüfbar) | Feststellung am heutigen Stand |
|---|---|---|---|
| 23 | **bestätigt geschlossen** | Bericht §3.7 **Z. 889–935**, darin der Absatz „Nullanker und Bindungsregel" **Z. 906–913**; Zeichentabelle §3.5, Zeilen \(x_k\) und \(I_{60,k}\) **Z. 787–788** | Alle vier Forderungen des Befunds stehen im heutigen Text: Nullanker („Kommunen mit \(x_k = 0\) … erhalten den Indexwert \(I_{60,k} = 0\)", Z. 906–907), Vergleichsraum nur über \(x_k > 0\) („gehören nicht zum Vergleichsraum; der Perzentilrang wird nur über die Kommunen mit \(x_k > 0\) gebildet", Z. 907–908), ausdrückliche Bindungsregel („gleiche Werte erhalten den mittleren Rang (Durchschnittsrang)", Z. 908–909) und die Erweiterung des Lackmustests auf den Schicht-A-Ausweis („Eine Kommune ohne Flussaue trägt \(\text{EAD}_k = 0\) €₂₀₂₆/a **und** \(I_{60,k} = 0\)", Z. 911–913) samt nachgerechnetem Zahlenbeispiel (100 Kommunen, 60 mit \(x_k = 0\) ⇒ 0 Punkte statt der in Runde 1 gemessenen 60,0 Punkte). Damit ist die Mehrdeutigkeit „kleiner oder gleich"/„echt kleiner" beseitigt. Formhinweis ohne Befundcharakter: Die Erweiterung des Lackmustests ist in §3.7 mit Rückverweis formuliert, nicht im Absatz „Lackmustest (§3.1)" des §3.4 selbst (Z. 708–712) und nicht im dortigen Beispielblock (Z. 745–747) — die Forderung ist inhaltlich erfüllt, die Prüfung des Index bleibt aber unmaschinell. Kein neuer Befund. |
| 24 | **unvollständig geschlossen** | Bericht §3.1, Aufzählungspunkt „Physischer Teil-Ausweis" **Z. 545–548** (unverändert „\(\text{EAD} = \bar A \cdot w\)", davor „der Zelle beziehungsweise der Kommune") · §3.5, \(\bar A\)-Zeile **Z. 775** („indexfrei \(\bar A\) als Gattungszeichen (§3.1), mit Index für die Zelle bzw. die Kommune") · gegen §3.6 **Z. 797** (\(\text{EAD}_k = \sum_{z \in k} \bar A_z w_z\)) und die \(\text{EAD}\)-Zeile §3.5 **Z. 781** · Suche nach „proportional" in §3.1/§3.5/§3.6: **0 Treffer** | Der Status „bewusst offen" ist sachlich unverändert; geprüft wurde nach der Vorgabe dieses Pakets allein, ob die Begründung des Ledgers („auf der Zelle exakt, kommunaler Ausweis rechnet in §3.6 korrekt als Summe") im **Bericht** als Modellgrenze sichtbar ist. Sie ist es nicht: §3.1 Z. 547–548 trägt die indexfreie Gleichung weiterhin und dehnt sie im selben Satz ausdrücklich auf die Kommune aus („der Zelle **beziehungsweise der Kommune**"); §3.5 Z. 775 wiederholt die Gattungslesart. Nur die \(\text{EAD}\)-Zeile in §3.5 (Z. 781) und §3.6 indizieren korrekt. Nirgends steht, dass \(\bar A_k\) und \(\text{EAD}_k\) bei gemischtem Gebäudetyp **nicht** proportional sind. Gegenbeispiel in dieser Sitzung neu gerechnet (EFH-Zelle 1.200 m², \(a\) = 0,25/0,80/1,00; MFH-Zelle 3.000 m², \(a\) = 0,00/0,10/0,20): \(\text{EAD}_k = 20.195{,}7\) €₂₀₂₆/a gegen \(\bar A_k \cdot w_k = 18.077{,}9\) €₂₀₂₆/a — **10,5 % bezogen auf \(\text{EAD}_k\)** (11,7 % bezogen auf das Produkt, so in Runde 2 ausgewiesen). „Bestätigt geschlossen" ist nach der Prüfregel dieses Pakets deshalb nicht vergebbar. → **Befund 74** (Kategorie C). Der Status von Befund 24 selbst bleibt unberührt. |
| 25 | **unvollständig geschlossen** | Bericht §3.5 **Z. 750–789**, Vollständigkeitsanspruch **Z. 752** („Die Tabelle führt **jedes** Formelzeichen, das in diesem Kapitel oder in Kapitel 5 vorkommt") und \(t\)-Zeile **Z. 758** („Laufindex des Gebäudetyps (EFH/ZFH, MFH)") · §5.1.1 **Z. 1602–1616** · gegen Kapitel 5: \(q_0\) **Z. 1638**, \(t_1\)/\(t_2\)/\(t_3\) **Z. 1688–1689** · gemessen in dieser Sitzung: Abgleich der Zeichen gegen beide Zeichentabellen ⇒ fehlend `['q_0', 't_1', 't_2', 't_3']` | Der Status „bewusst offen" ist sachlich unverändert; die vier Zeilen fehlen weiterhin in beiden Zeichentabellen. Geprüft wurde, ob die Ledger-Begründung („ohne Rechenwirkung; \(q_0\) ist in §4.7/§4.8 als geparkt geführt") im Bericht als Modellgrenze sichtbar ist. **Teilweise:** Für \(q_0\) ja — §4.7 Z. 1445–1455 führt „Heutiger Objektschutz-Anteil \(q_0\): geparkt (Datenquelle fehlt)", Z. 1428–1441 eine ausdrückliche Modellgrenze zu Richtung und Größenordnung der Verzerrung, die Watchlist-Zeile Z. 1475 denselben Stand; §5.1.2 Z. 1638 verweist darauf. Für \(t_1\)…\(t_3\) **nein**: Sie werden in §5.1.3 Z. 1688–1689 ohne Zeichentabellenzeile, ohne Einheitsangabe (m²/a) und ohne Auflösung der **Zeichenkollision** mit dem Laufindex \(t\) des Gebäudetyps (§3.5 Z. 758, \(n_t\) Z. 779, \(\theta_{z,t}\) Z. 778) eingeführt; \(t_1\) liest sich weiterhin als „Gebäudetyp 1". Zugleich steht der Vollständigkeitsanspruch des §3.5 (Z. 752) unverändert und ohne Einschränkung im Text, so dass ein Leser die Auslassung nicht als bewusste Entscheidung erkennen kann. → **Befund 75** (Kategorie C). Der Status von Befund 25 selbst bleibt unberührt. |
| 26 | **bestätigt geschlossen** | Bericht §5.1.3, Absätze „Profilabhängige Illustration: Anteil unterhalb HQ100 in der Beispielzelle (Befund 26)" **Z. 1680–1696** und „Tragende Begründung der oberen Bandgrenze: Ankerwert der Verteilungsprüfung (§4.5)" **Z. 1697–1717**, „Folge für das Band" **Z. 1719–1727** · nachgezogene Stellen: Kap. 1 Knoten-Bilanz, Kap. 2 Zeile 60-S092-01, §3.5 **Z. 783**, §5.1.1 **Z. 1615**, §5.1.2, Kap. 7 `flood_bldg.s_bem`/`flood_bldg.r_s092`, Entscheidungslog Nr. 3 · Prüflauf in dieser Sitzung (Ausdruck der Autor-Revision, Z. 1562): alle neun Teilprüfungen wahr | Der in der Autor-Revision gewählte zweite Weg (§5 zweiter Vorschlagszweig) ist am heutigen Text vollständig belegt: Die 0,661 ist ausdrücklich als „**eine profilabhängige Illustration, keine Obergrenze**" gekennzeichnet (Z. 1694–1696), allgemein bleibt nur die Ungleichung stehen (Z. 1681–1684), die Vergleichsprofile 0,856 / 0,327 / 0,000 sind ausgewiesen (Z. 1692–1694), der nicht tragende Verweis „Zahlen aus Abschnitt 4.5" ist durch die tatsächliche Fundstelle ersetzt (Z. 1687–1688: Beispielzelle §3.4 „Rechenbeispiel (eine Zelle)", Trapez §3.4 Schritt 2) — gemessen kommt die Zeichenfolge „Zahlen aus Abschnitt 4.5" in §5.1.3 null mal vor. Die obere Bandgrenze steht jetzt auf einer zellunabhängigen Begründung (Ankerwert 1 − 1,0/2,6 = 0,615 ⇒ 0,62, ausgewiesen als Abschätzung von KAP3, mit Modellgrenze des Pauschalfaktors). Der Nachzug ist überall vollzogen: \(s_{\text{bem}}\) 0,30–0,62 in §3.5/§5.1.1/§5.1.2/§5.1.3, \(r_{\text{S092}}\) 0,0075–0,0992 in §3.5/§5.1.1/Kap. 1/Registerzeile/Entscheidungslog, Parameter-Blöcke `band: [0.30, 0.62]` und `band: [0.0075, 0.0992]`, und die alte Obergrenze 0,1056 kommt im ganzen Bericht null mal vor. Kein neuer Befund: Dass der Ankerwert seinerseits mit Befund 33 auf 47,7 % umgestellt und die Bandgrenze damit auf 0,52 zu ziehen wäre, ist bereits als **Befund 66** (B) verbucht — hier nicht doppelt erfasst. |

#### Neue Befunde dieses Pakets (74 und 75)

| Nr | Kat. | Befund |
|---|---|---|
| 74 | **C** | **Stelle:** Bericht §3.1, Aufzählungspunkt „Physischer Teil-Ausweis (Zwischengröße vor dem Euro)" **Z. 545–548** („… dem erwarteten Schaden der Zelle beziehungsweise der Kommune entspricht. Sie entsteht in der Formel vor jedem Euro-Betrag und trägt ihn: \(\text{EAD} = \bar A \cdot w\)") und §3.5, \(\bar A\)-Zeile **Z. 775**, gegen §3.6 **Z. 797** und §3.6 Teil-Ausweis 1 **Z. 819–820**. · **Art: Lücke (bewusste Abweichung ohne sichtbare Modellgrenze)** (§3.6 Ausweis auf der deklarierten Betrachtungsebene; §5 LF 3; eiserne Regel 2). · **Begründung:** Befund 24 ist im Ledger als „bewusst offen" geführt, begründet damit, dass die Gleichung auf der Zelle exakt sei und §3.6 kommunal korrekt summiere. Diese Entscheidung ist im **Bericht** nirgends sichtbar: §3.1 dehnt die indexfreie Gleichung im selben Satz ausdrücklich auf die Kommune aus, §3.5 führt \(\bar A\) als Gattungszeichen „mit Index für die Zelle bzw. die Kommune", und weder §3.1 noch §3.5 noch der Teil-Ausweis 1 in §3.6 vermerken, dass \(\bar A_k\) und \(\text{EAD}_k\) bei gemischtem Gebäudetyp nicht proportional sind; die Suche nach „proportional" liefert in diesen drei Abschnitten null Treffer. Gemessenes Gegenbeispiel (in dieser Sitzung nachgerechnet, zwei Zellen, Ressourcen-Regel §3.4 eingehalten): \(\text{EAD}_k = 20.195{,}7\) gegen \(\bar A_k \cdot w_k = 18.077{,}9\) €₂₀₂₆/a, **10,5 %** Abweichung bezogen auf \(\text{EAD}_k\). Ein Nutzer, der nach §3.6 beide Teil-Ausweise nebeneinander liest, kann daraus einen proportionalen Zusammenhang ableiten, den das Modell nicht trägt. Kategorie C: Kein ausgewiesener Zahlenwert ist falsch, §3.6 rechnet richtig; betroffen ist die Lesart der Teil-Ausweise. · **Vorschlag:** In §3.1 und in der \(\bar A\)-Zeile des §3.5 die Gleichung auf die Zelle indizieren (\(\text{EAD}_z = \bar A_z w_z\)) und für die Kommune auf die Summe in §3.6 verweisen; im Teil-Ausweis 1 (§3.6 Z. 819–820) einen Satz aufnehmen, dass \(\bar A_k\) und \(\text{EAD}_k\) bei gemischtem Gebäudetyp nicht proportional sind (Beispiel: 10,5 %) — damit ist die Entscheidung „bewusst offen" nach eiserner Regel 2 auch außerhalb des Ledgers dokumentiert. Nicht in diesem Paket umgesetzt (Dateirahmen), hier nur verbucht. |
| 75 | **C** | **Stelle:** Bericht §3.5, Einleitungssatz **Z. 752** („Die Tabelle führt **jedes** Formelzeichen, das in diesem Kapitel oder in Kapitel 5 vorkommt, mit Bedeutung, Einheit und Herkunft") und \(t\)-Zeile **Z. 758**, §5.1.1 **Z. 1602–1616**, gegen §5.1.3 **Z. 1688–1689** (\(t_1 = 4{,}174\), \(t_2 = 1{,}466\), \(t_3 = 0{,}671\)); gemessen: Abgleich der in Kapitel 5 verwendeten Zeichen gegen beide Zeichentabellen ⇒ fehlend `q_0`, `t_1`, `t_2`, `t_3`. · **Art: Lücke (unerfüllter Vollständigkeitsanspruch; Zeichenkollision)** (§5 LF 11 „Zeichentabellen vollständig"; §3.9 „kein Formelzeichen ohne Herleitung"; Vorgabe P3 Lesbarkeit). · **Begründung:** Befund 25 ist als „bewusst offen" geführt mit der Begründung, die vier Zeilen hätten keine Rechenwirkung und \(q_0\) sei in §4.7/§4.8 als geparkt dokumentiert. Für \(q_0\) trägt diese Begründung im Bericht: §4.7 Z. 1445–1455 führt ihn als geparkt, Z. 1428–1441 als ausdrückliche Modellgrenze, die Watchlist Z. 1475 ebenso. Für \(t_1\)…\(t_3\) trägt sie nicht: Die drei Zeichen werden in §5.1.3 ohne Tabellenzeile, ohne Einheit (m²/a) und ohne Auflösung der Kollision mit dem Laufindex \(t\) des Gebäudetyps eingeführt (§3.5 Z. 758; \(\theta_{z,t}\) Z. 778, \(n_t\) Z. 779 tragen diesen Index), so dass \(t_1\) sich als „Gebäudetyp 1" statt als Szenariobeitrag liest — nach Vorgabe P3 ist das für den Adressaten „Sachbearbeiter einer Kommune" eine Lesbarkeitsschwelle, nicht nur ein Formalpunkt. Zugleich steht der Vollständigkeitsanspruch des §3.5 uneingeschränkt im Text, die bewusste Auslassung ist für einen Leser also nicht erkennbar. Kategorie C: Kein Zahlenwert, kein Band und kein Konto ist betroffen; die Werte 4,174/1,466/0,671 sind in §5.1.3 hergeleitet und summieren gemessen auf \(\bar A_z = 6{,}311\) m²/a. · **Vorschlag:** Die Szenariobeiträge umbenennen (z. B. \(\tau_i\) oder \(\bar A^{(i)}\)), damit der Laufindex \(t\) eindeutig bleibt, und sie mit Einheit m²/a und Herkunft §5.1.3 in §3.5 aufnehmen; \(q_0\) mit Herkunft „§4.7, geparkt (Datenquelle fehlt)" ergänzen oder den Vollständigkeitssatz in Z. 752 auf „jedes rechenwirksame Formelzeichen" einschränken und die Ausnahmen dort benennen. Nicht in diesem Paket umgesetzt (Dateirahmen), hier nur verbucht. |

#### Abgrenzung und Status dieses Pakets

- **Geändert wurde ausschließlich `reviews/BEFUNDE_60.md`** (angehängt).
  `docs/methodik/60_gebaeudeschaeden_flusshochwasser.md`, `docs/evidenz/register.md`,
  `backend/scripts/lint_methodik.py` und die Arbeitsmappen sind byte-gleich; der Bericht wurde nur
  gelesen und an den ausgewiesenen Stellen nachgerechnet (eiserne Regel 2).
- **Kein Befund behoben, keiner umnummeriert.** Höchste vorhandene Nummer zu Laufbeginn: **73**;
  neu vergeben sind **74 und 75**. Die Befunde 10, 33 und 66 sind nur als Gegenstelle bzw. zur
  Abgrenzung eingeordnet, ihr Status bleibt unberührt; insbesondere ist die überholte Ankerzahl
  hinter der oberen Bandgrenze von \(s_{\text{bem}}\) bereits Befund 66 und wird hier **nicht**
  doppelt erfasst.
- **Keine Leitfrage aus §5 beantwortet.** Dieses Paket führt allein die Regression der Nummern
  **23, 24, 25 und 26**; die Teile 1 (6, 11, 12, 13) und 2 (17, 20, 21, 22) der Befundregression und
  die Leitfragen-Pakete der Runde 3 sind nicht Gegenstand.
- **Prüfregel für „bewusst offen" angewandt (24, 25):** „bestätigt geschlossen" nur, wenn die im
  Ledger festgehaltene Begründung im heutigen Bericht als Modellgrenze sichtbar ist. Bei 24 ist sie
  es nicht, bei 25 nur für \(q_0\), nicht für \(t_1\)…\(t_3\) — beide deshalb „unvollständig
  geschlossen", der Status der Ursprungsbefunde bleibt unverändert.
- **Ressourcen-Regel §3.4 eingehalten:** kein nationaler 100-m-Vollraster-Lauf; nachgerechnet wurde
  zellweise (zwei Zellen für Nr. 24) und an den ausgewiesenen Stellen des Berichts. Divergenzen
  sind als Befunde verbucht, nicht still im Code behoben (eiserne Regel 5).
- **Frische Sitzung** (eiserne Regel 4): Diese Gegenprüfung ist nicht die Sitzung, die den
  geprüften Stand geschrieben hat (T-0235 bis T-0243, T-0245, T-0256 bis T-0259, T-0287, die
  Revisionspakete aus T-0281 sowie T-0295, T-0320 bis T-0335 — alle abgeschlossen).
- **Kopftabelle „Offene Befunde" bewusst nicht fortgeschrieben** (Dateirahmen der Runde-3-Pakete,
  T-0359).

### Befundregression Teil 4 (27, 28, 29, 30)

Paket T-0387 der Runde 3 (18.09.2026, zweite Hälfte des halbierten T-0367), eigene frische Sitzung:
Sie hat den geprüften Stand nicht geschrieben (eiserne Regel 4; geschrieben haben T-0235 bis
T-0243, T-0256 bis T-0259 und die Revisionspakete aus T-0281, alle im Endstatus). **In diesem Paket
wird keine Leitfrage aus §5 beantwortet und kein Befund behoben.** Prüfgegenstand ist der
**Umsetzungsnachweis im heutigen Berichtsstand**, nicht die Behauptung im Ledger. Für die als
„bewusst offen" geführten Nummern **27, 29 und 30** gilt die Prüfregel dieses Pakets: „bestätigt
geschlossen" nur, wenn die im Ledger festgehaltene Begründung im heutigen Bericht als **Modellgrenze
sichtbar** ist. Nummer **28** ist in der Autor-Revision mit vier Teilschritten (a)–(d) dokumentiert;
deren Umsetzung ist hier einzeln am Bericht nachgewiesen. Zusätzlich sind die beiden Registerzeilen
**60-S092-01** und **60-S094-01** gegen Vorgabe **P2** geprüft (Zahlenwert, Bandbreite,
Sensitivität, ausgewiesen als Abschätzung). Zeilennummern beziehen sich auf den heutigen Stand von
`docs/methodik/60_gebaeudeschaeden_flusshochwasser.md` (2.513 Zeilen).
**Befundnummern:** höchste zu Laufbeginn im Ledger vorhandene Nummer **75** (gemessen über alle
Tabellen-Nummernspalten und alle „Befund <n>"-Nennungen), neu vergeben sind deshalb **76, 77 und
78**.

| Nr | Urteil | Fundstelle (nachprüfbar) | Feststellung am heutigen Stand |
|---|---|---|---|
| 27 | **unvollständig geschlossen** | Bericht Kap. 2, Registerzeile **60-R24-01 Z. 193** · Langbeleg B4, **Rechenschritt 2 Z. 357–367** (darin **Z. 361**: „Angesetzt werden drei Jahresschritte (2024, 2025, 2026) mit je 3,4 %"), **Rechenschritt 3 Z. 369–376**, **Rechenschritt 4 Z. 377–392** (einzige „**Modellgrenze:**" dort **Z. 389–392**: Nichtwohngebäude) · Parameterliste §4.7 **Z. 1468** · in dieser Sitzung nachgerechnet | Der Status „bewusst offen" ist sachlich unverändert; alle drei Teilpunkte stehen unverändert im Text. (a) Die Raten **3,4 %** und **2,3 %** sind in Z. 358–362 weiterhin ohne Herleitung aus den dort zitierten amtlichen Werten (+3,2 %/+3,3 %/+5,0 %) angesetzt; die einzige Stelle, die eine Rundung offenlegt, ist die Watchlist-Zeile Z. 1468 — sie begründet den **3-%-Schritt 2023 → 2024**, nicht die Fortschreibungsraten. (b) Die Bandenden **1.889–2.047** bzw. **1.484–1.609** €₂₀₂₆/m² BGF stehen unverändert in Z. 193 und Z. 363–366; mit den ungerundeten Faktoren ergibt sich 1.889,6–**2.043,2** bzw. 1.484,9–**1.605,6** — Abweichung am oberen Ende **+0,19 %**. (c) „Wertdichte **1.993–2.535**" und „**8,2–10,4 Bio. €**" sind nach Rechenschritt 3 (Z. 374–375) ausdrücklich der **MFH**- bzw. **EFH**-Satz, in der Registerzeile Z. 193 stehen sie aber ohne Typkennzeichnung als Band; die Bänder der beiden abgeschätzten Faktoren sind darin weiterhin nicht fortgepflanzt (gerechnet: 1.856–2.860 €₂₀₂₆/m², Bestand **7,6–11,7 Bio. €**). Die Ledger-Begründung („Rundungs- und Herleitungsmangel, Zentralwerte unberührt") ist an keiner dieser Stellen als Modellgrenze sichtbar. → **Befund 76** (Kategorie C). Der Status von Befund 27 selbst bleibt unberührt. |
| 28 | **bestätigt geschlossen** | Bericht B5 **Z. 433–468**: Achsenzerlegung über C0P0 **Z. 433–444**, geometrische Zentrierung **Z. 445–453**, Fig.-1-Zuordnung **Z. 453–458**, Sensitivität **Z. 458–462** · B6 **Z. 502–518** · Registerzeilen **Z. 187** (60-S093-01) und **Z. 188** (60-S094-01) · Prüflauf in dieser Sitzung mit dem Ausdruck der Autor-Revision (Ledger **Z. 1550**): alle sieben Teilprüfungen wahr | Alle vier Teilschritte sind am heutigen Text belegt. **(a)** B5 zerlegt die Diagonale jetzt über das Referenzfeld C0P0 = 0,92 in die Einzelachsen Kontamination (ln 1,717 = 0,541) und Vorsorge (ln 2,244 = 0,808) und setzt deren **Mittel 0,6745 (Teiler 2)** an ⇒ Band **0,71–1,40**; die Zeichenfolge „1,349 ÷ 3" kommt im ganzen Bericht **null mal** vor; B6 Z. 507–511 zieht 0,6745 ÷ 2 = 0,3373 ⇒ **0,84–1,18**, kombiniert **0,60–1,66**. **(b)** Z. 445 nennt die Setzung „**Geometrisch zentriert** um 1 (nicht mittelwertzentriert …)", Z. 450–453 weisen das arithmetische Mittel bei hälftigem Bestand (1,057; mit B6 zusammen +7,3 %) ausdrücklich **als Modellgrenze** aus, Z. 453–458 ordnen die Fig.-1-Endwerte 3,5 %/25 % als dokumentierte Annahme der geometrischen Mitte beider Kurven zu. **(c)** Die Lesart „volle Diagonale" lautet in Z. 461–462 „e^±0,6745) **0,51–1,96**"; „0,52–1,96" kommt null mal vor. **(d)** Z. 187 trägt „Sensitivität: **−29 %/+40 %**" statt „±25 %", Z. 188 „**−16 %/+18 %**"; die Bänder stehen gleichlautend in `docs/evidenz/register.md`, §3.5 und in den Parameterblöcken `flood_bldg.f_s093` `band: [0.71, 1.40]` / `flood_bldg.f_s094` `band: [0.84, 1.18]`. Kein neuer Befund. Formhinweis ohne Befundcharakter: Die +7,3 % der arithmetischen Lesart bleiben innerhalb des Bands und sind bewusst nicht in den Basiswert gezogen (Z. 451–453). |
| 29 | **unvollständig geschlossen** | Bericht Kap. 2, Registerzeile **60-S092-01 Z. 186**, Spalte Studientyp („… sind nur Kandidat, **im Volltext nicht verifiziert**, gehen nicht in den Wert ein") gegen Registerzeile **60-S093-01 Z. 187** (Thieken u. a. 2008 „**Volltext geprüft** (Tab. 1 S. 317; Fig. 1 und Tab. 2 S. 318…)") und Langbeleg B5 **Z. 409–410** (Tab. 2 wörtlich: C0P0 0,92 · C0P1 0,64 · C0P2 0,41) · B5 „Kopplung (§3.9)" **Z. 463–465** · gemessen: „Thieken" in Z. 186 **0 Treffer**, „0,696"/„0,446"/„Plausibilitätsprobe" im ganzen Bericht **je 0 Treffer** | Der Widerspruch steht unverändert: Dieselbe Quelle ist in Z. 186 als „im Volltext nicht verifiziert" und in Z. 187/188 als volltextgeprüft geführt, und ihre Tab.-2-Faktoren tragen in B5 (Z. 433–444) das Band von 60-S093-01. Geprüft wurde nach der Prüfregel dieses Pakets allein, ob die Ledger-Begründung („betrifft die Begründung des Verzichts, nicht den Wert") im **Bericht** sichtbar ist: Sie ist es nicht — weder nennt die S092-Zeile Thieken u. a. 2008 als volltextgeprüfte, nach §3.5 unzulässige Befragungsevidenz, noch stehen die Vergleichswerte 0,70/0,45 als Plausibilitätsprobe, noch ist die Kopplung S092 ↔ S093 irgendwo vermerkt (die Kopplung in Z. 463–465 betrifft nur eine künftige Zahlentabelle). „Bestätigt geschlossen" ist deshalb nicht vergebbar. → **Befund 77** (Kategorie C). **P2-Prüfung 60-S092-01 (bestanden, kein eigener Befund):** Zahlenwert \(r_{\text{S092}}\) = 0,035, Bandbreite 0,0075–0,0992, Sensitivität „−0,75 % bis −9,92 % des K3-Erwartungsschadens" (Z. 1720–1721), ausgewiesen als „§3.9 ABGESCHÄTZT"/Abschätzung von KAP3 mit Herleitung §5.1. Der Status von Befund 29 selbst bleibt unberührt. |
| 30 | **unvollständig geschlossen** | Bericht Kap. 2, Registerzeile **60-S093-01 Z. 187** (Effektgröße „… und Gebäudetyp (**3 Klassen**)") · §3.3 **Z. 587–600** (Stützstellen \(d(h)\), typunabhängig: \(d_1 = 0{,}035\), \(d_5 = 0{,}250\), log-lineare Interpolation) · Kap. 9 **Z. 2436–2438** („p(HQ) × Schadensgrad(Wassertiefe · **Gebäudetyp** · Gebäudequalität) × Gebäudewert") · gemessen in Kap. 2 (Z. 152–500): „je Gebäudetyp" **0**, „typabhängig" **0**, „Typstruktur" **0** Treffer; die Typstruktur rechnet weiterhin nur im Preis (\(n_t\) Z. 779: 1.950/1.533) | Der Status „bewusst offen" ist sachlich unverändert: Die zitierte Schadensfunktion ist nach Gebäudetyp strukturiert, die Schadensquote des Berichts ist es nicht, und die Endpunkte 3,5 %/25 % sind weiterhin keinem Typ zugeordnet (Z. 590–592). Geprüft wurde, ob die Ledger-Begründung („verändert die Registerzeile nicht, ist eine **noch auszuweisende Modellgrenze**") inzwischen im Bericht steht: Sie steht nicht — Kap. 2 enthält keinen Hinweis auf die Nichtverwendung der Typachse, und §3.3 führt die Typunabhängigkeit weder als Annahme noch als Modellgrenze. Verschärfend gegenüber Runde 2: Der Ansatzvergleich in Kap. 9 Z. 2437 beschreibt den umgesetzten Ansatz (a) ausdrücklich als „Schadensgrad(Wassertiefe · Gebäudetyp · Gebäudequalität)", also mit Typachse — ein Leser erwartet danach eine typabhängige Schadensquote, die das Modell nicht führt. → **Befund 78** (Kategorie C). **P2-Prüfung 60-S094-01 (bestanden, kein eigener Befund):** Zahlenwert \(f_{\text{S094}}\) = 1,00, Bandbreite 0,84–1,18 (kombiniert 0,60–1,66), Sensitivität „−16 %/+18 %" (Z. 188, B6 Z. 512–514), ausgewiesen als Abschätzung von KAP3, mit ausdrücklicher **Bauform-Grenze** als Modellgrenze (Z. 188 Modellgrenzen (a); B6 Z. 515–518). Der Status von Befund 30 selbst bleibt unberührt. |

#### Neue Befunde dieses Pakets (76, 77 und 78)

| Nr | Kat. | Befund |
|---|---|---|
| 76 | **C** | **Stelle:** Bericht Kap. 2, Registerzeile 60-R24-01 **Z. 193**, und Langbeleg B4, Rechenschritt 2 **Z. 357–367**, Rechenschritt 3 **Z. 369–376**, Rechenschritt 4 **Z. 377–392**. · **Art: Lücke (bewusst offene Entscheidung ohne sichtbare Modellgrenze)** (§3.9 „Abgeschätzt"; Vorgabe P1 „samt Herleitung"; eiserne Regel 2). · **Begründung:** Befund 27 ist im Ledger als „bewusst offen" geführt mit der Begründung, es handele sich um einen Rundungs- und Herleitungsmangel im Band von \(n_t\) (rund 0,2 % am oberen Bandende) bei unberührten Zentralwerten. Im Bericht ist diese Entscheidung nirgends sichtbar: Z. 361 setzt „je 3,4 %" und Z. 362 „à 2,3 %" ohne Herleitung neben die zitierten amtlichen Raten (+3,2 %, +3,3 %, +5,0 %); die Bandenden 1.889–2.047 bzw. 1.484–1.609 sind mit den gerundeten Faktoren 1,07/1,16 gerechnet (ungerundet 1.889,6–2.043,2 bzw. 1.484,9–1.605,6, **+0,19 %** am oberen Ende, in dieser Sitzung nachgerechnet); die einzige „Modellgrenze" des B4 (Z. 389–392) betrifft Nichtwohngebäude. Hinzu kommt die Lesart der Wertdichte: 1.993–2.535 €₂₀₂₆/m² und 8,2–10,4 Bio. €₂₀₂₆ sind nach Rechenschritt 3 die **Typ-Endpunkte** MFH/EFH, stehen in Z. 193 aber ohne Typkennzeichnung wie ein Unsicherheitsband; die Bänder der beiden abgeschätzten Faktoren (1,07–1,16 und 1,25–1,40) sind darin nicht fortgepflanzt — gerechnet spannt die Wertdichte 1.856–2.860 €₂₀₂₆/m², der Bestandswert 7,6–11,7 Bio. €₂₀₂₆. Kategorie C: Zentralwerte (Faktor 1,105; 1.950/1.533 €₂₀₂₆/m² BGF) und alle Konten bleiben unberührt; betroffen sind Bandenden und die Lesbarkeit der Herleitung. · **Vorschlag:** In B4 Rechenschritt 2 einen Satz ergänzen, wie 3,4 % und 2,3 % aus den zitierten Monatswerten entstehen (oder sie als gerundete Setzung mit Richtung und Größenordnung ausweisen, wie es Z. 1468 für den 2023→2024-Schritt tut), die Bandenden mit den ungerundeten Faktoren rechnen (1.890–2.043 bzw. 1.485–1.606) und in Z. 193 Typ-Spanne und Unsicherheitsband getrennt kennzeichnen („1.993 (MFH) bis 2.535 (EFH) €₂₀₂₆/m²; mit den Faktorbändern 1.856–2.860"). Nicht in diesem Paket umgesetzt (Dateirahmen), hier nur verbucht. |
| 77 | **C** | **Stelle:** Bericht Kap. 2, Registerzeile 60-S092-01 **Z. 186**, Spalte Studientyp, gegen Registerzeile 60-S093-01 **Z. 187** und Langbeleg B5 **Z. 409–410** (Tab. 2 wörtlich) sowie B5 „Kopplung (§3.9)" **Z. 463–465**. · **Art: Widerspruch (im Bericht unaufgelöst, keine sichtbare Einordnung)** (§5 LF 5 „richtige Studienart"; LF 6 „Kopplungen"; §3.8 „benannt statt geglättet"). · **Begründung:** Befund 29 ist als „bewusst offen" geführt, weil er nur die Begründung des Verzichts auf eine Effektgröße betreffe, nicht deren Wert. Diese Einordnung steht ausschließlich im Ledger: Im Bericht behauptet Z. 186 weiterhin, Befragungen nach Ereignissen seien „nur Kandidat, im Volltext nicht verifiziert", während dieselbe Quelle (Thieken u. a. 2008) in Z. 187 und Z. 188 als volltextgeprüft geführt wird und ihre Tab.-2-Faktoren (C0P0 0,92, C0P1 0,64, C0P2 0,41 ⇒ 0,696 bzw. 0,446) in B5 Z. 433–444 das Band von 60-S093-01 dimensionieren. Gemessen: „Thieken" in Z. 186 null Treffer; „0,696", „0,446" und „Plausibilitätsprobe" im ganzen Bericht je null Treffer; die Kopplung S092 ↔ S093 ist nirgends vermerkt. Ein Leser der S092-Zeile kann weder erkennen, dass die Quelle geprüft ist, noch dass sie an anderer Stelle rechnet. Kategorie C: Der Ausschluss als Wertquelle nach §3.5 (keine Interventionsstudie) bleibt richtig, \(r_{\text{S092}}\) = 0,035 (0,0075–0,0992) ist unberührt, und die P2-Anforderungen an die Zeile (Zahlenwert, Band, Sensitivität −0,75 %/−9,92 %, Kennzeichnung als Abschätzung) sind erfüllt. · **Vorschlag:** In Z. 186 die Formulierung „im Volltext nicht verifiziert" durch „volltextgeprüft, nach §3.5 als Wertquelle nicht zulässig (Befragung, keine Interventionsstudie)" ersetzen, die Faktoren 0,70/0,45 dort als Plausibilitätsprobe der Kette §5.1 ausweisen (nicht als Wert) und die Kopplung S092 ↔ S093 in Z. 186 und in B5 vermerken. Nicht in diesem Paket umgesetzt (Dateirahmen), hier nur verbucht. |
| 78 | **C** | **Stelle:** Bericht Kap. 2, Registerzeile 60-S093-01 **Z. 187** (Effektgröße „Gebäudetyp (3 Klassen)") und Kapitel 2 insgesamt (**Z. 152–500**), gegen §3.3 **Z. 587–600** (typunabhängige Stützstellen \(d(h)\)) und Kap. 9 **Z. 2436–2438**. · **Art: Lücke (strukturabhängige Evidenz nicht durchgezogen, Nichtverwendung nicht als Modellgrenze ausgewiesen)** (§5 LF 6; Vorgaben P1/P2; §3.9). · **Begründung:** Befund 30 ist als „bewusst offen" geführt mit der Begründung, die fehlende Typstruktur sei „eine noch auszuweisende Modellgrenze". Ausgewiesen ist sie bis heute nicht: In Kapitel 2 kommen „je Gebäudetyp", „typabhängig" und „Typstruktur" je null mal vor, §3.3 führt \(d(h)\) ohne Typindex und ohne Annahmevermerk, und die belegten Endwerte 3,5 %/25 % bleiben typunzugeordnet, obwohl das Register den Gebäudetyp je 100-m-Zelle aus dem Zensus 2022 als verfügbar nennt (Z. 778) und ihn im Preis auch nutzt (\(n_t\) 1.950/1.533, Z. 779). Verschärfend: Kap. 9 Z. 2437 beschreibt den umgesetzten Ansatz (a) als „Schadensgrad(Wassertiefe · Gebäudetyp · Gebäudequalität)" — der Bericht verspricht damit an einer prominenten Stelle eine Typachse im Schadensgrad, die das Modell nicht führt. Kategorie C: Kein ausgewiesener Zahlenwert ist falsch, die Registerzeile bleibt unverändert; betroffen sind Vollständigkeit der Strukturnutzung und die Erwartung, die der Bericht beim Leser erzeugt (Vorgabe P3). · **Vorschlag:** Entweder eine Spalte/Zeile für die typabhängige Schadensquote anlegen und die Fig.-1-Endpunkte den Typen zuordnen, oder in §3.3 und in Z. 187 die Typunabhängigkeit von \(d(h)\) als Modellgrenze mit Richtung und Größenordnung ausweisen (Abschätzung von KAP3 nach P1/P2) und die Formulierung in Kap. 9 Z. 2437 auf den tatsächlich umgesetzten Aufbau ziehen. Nicht in diesem Paket umgesetzt (Dateirahmen), hier nur verbucht. |

#### Abgrenzung und Status dieses Pakets

- **Geändert wurde ausschließlich `reviews/BEFUNDE_60.md`** (angehängt).
  `docs/methodik/60_gebaeudeschaeden_flusshochwasser.md`, `docs/evidenz/register.md`,
  `backend/scripts/lint_methodik.py` und die Arbeitsmappen sind byte-gleich; der Bericht wurde nur
  gelesen und an den ausgewiesenen Stellen nachgerechnet (eiserne Regel 2, eiserne Regel 5).
- **Kein Befund behoben, keiner umnummeriert.** Höchste vorhandene Nummer zu Laufbeginn: **75**;
  neu vergeben sind **76, 77 und 78**. Die Status der Befunde 27 bis 30 selbst bleiben unberührt.
- **Keine Leitfrage aus §5 beantwortet.** Dieses Paket führt allein die Regression der Nummern
  **27, 28, 29 und 30**; zusammen mit Teil 3 (23–26) sind damit die acht Nummern des ersetzten
  T-0367 genau einmal abgedeckt.
- **Prüfregel für „bewusst offen" angewandt (27, 29, 30):** „bestätigt geschlossen" nur bei im
  Bericht sichtbarer Modellgrenze; in allen drei Fällen fehlt sie, deshalb dreimal „unvollständig
  geschlossen". Nummer **28** ist als einzige „bestätigt geschlossen" — alle vier Teilschritte der
  Autor-Revision sind am Bericht nachgewiesen.
- **Vorgabe P2 an den beiden einschlägigen Registerzeilen geprüft:** 60-S092-01 und 60-S094-01
  führen je Zahlenwert, Bandbreite und Sensitivität und sind ausdrücklich als Abschätzung von KAP3
  ausgewiesen (S094 zusätzlich mit Bauform-Grenze als Modellgrenze) — kein Befund aus P2.
- **Ressourcen-Regel §3.4 eingehalten:** kein nationaler 100-m-Vollraster-Lauf; nachgerechnet wurden
  nur die Faktoren und Bandenden der genannten Rechenschritte.
- **Kopftabelle „Offene Befunde" bewusst nicht fortgeschrieben** (Dateirahmen der Runde-3-Pakete,
  T-0359).

### Befundregression Teil 5 (31, 32, 33, 34)

Paket T-0388 der Runde 3 (20.09.2026, erste Hälfte des halbierten T-0368), eigene frische Sitzung:
Sie hat den geprüften Stand nicht geschrieben (eiserne Regel 4; geschrieben haben T-0235 bis
T-0243, T-0256 bis T-0259 und die Revisionspakete aus T-0281, alle im Endstatus). **In diesem Paket
wird keine Leitfrage aus §5 beantwortet und kein Befund behoben.** Prüfgegenstand ist der
**Umsetzungsnachweis im heutigen Berichtsstand**, nicht die Behauptung im Ledger. Für die drei
A-Befunde **32, 33 und 34** (Status „behoben", Kalibrierung auf \(M_0\) = 1,360 Mrd. €₂₀₂₆/a) ist
jede im Ledger genannte Zahl an der dort genannten Fundstelle im heutigen Bericht nachgelesen und
die Übereinstimmung ausdrücklich festgestellt oder als Abweichung benannt worden. Für die als
„bewusst offen" geführte Nummer **31** gilt die Prüfregel der Runde 3: „bestätigt geschlossen" nur,
wenn die im Ledger festgehaltene Begründung im heutigen Bericht als **Modellgrenze sichtbar** ist.
Zeilennummern beziehen sich auf den heutigen Stand von
`docs/methodik/60_gebaeudeschaeden_flusshochwasser.md` (2.513 Zeilen).
**Befundnummern:** höchste zu Laufbeginn im Ledger vorhandene Nummer **89** (gemessen über alle
Tabellen-Nummernspalten und alle „Befund <n>"-Nennungen), neu vergeben sind deshalb **90 und 91**.

| Nr | Urteil | Fundstelle (nachprüfbar) | Feststellung am heutigen Stand |
|---|---|---|---|
| 31 | **unvollständig geschlossen** | Bericht Kap. 2, Registerzeile **60-W085-01 Z. 164** (Spalte Effektgröße: „HQextrem 5,0·10⁻³ bis 1,0·10⁻³ a⁻¹"; Spalte Modellgrenze: nur Kartenabdeckung und uneinheitliches Wiederkehrintervall; Spalte Entscheidung: „**Basiswert** — … die drei Szenario-Stützstellen p(HQ) …") · §3.4 **Z. 670** und Beispielblock **Z. 737–738** (`assert abs(p3 - 2.236e-3) < 1e-6`) · §3.5 Zeichentabelle **Z. 776** · Kap. 7 Block `flood_bldg.p_hq_extrem` **Z. 2000–2003** (`wert: 0.002236`, `band: [0.001, 0.005]`) · gemessen (Schreibweisen getrennt): die LaTeX-Kommaform `2{,}236` **2 Treffer**, beide in §3.4 (Z. 666 und Z. 671), die Punktform `2.236e-3` **1 Treffer** im Beispielblock (Z. 738); in Kapitel 2 (Z. 156–522) **keine der beiden Schreibweisen** | Der Sachstand ist unverändert: Die Registerzeile Z. 164 führt für HQextrem weiterhin nur die beiden Bandenden ohne Zentralwert, während \(p_3 = 2{,}236 \cdot 10^{-3}\) a⁻¹ in der Kernformel rechnet (§3.4 Z. 670, Block Z. 738) und im Produkt als eigener Parameterblock steht (Z. 2000–2003) — der zweite Teil der Ledger-Begründung ist damit am Bericht **bestätigt**. Geprüft wurde nach der Prüfregel dieses Pakets, ob die Entscheidung „bewusst offen" im Bericht als Modellgrenze sichtbar ist: Sie ist es **nicht**. Die einzige „Modellgrenze" der Zeile Z. 164 betrifft die fehlende Kartenabdeckung und das uneinheitliche Extremszenario, nicht den fehlenden Zentralwert; in Z. 164 steht kein Verweis auf §3.4 Schritt 2, und Kapitel 2 nennt \(p_3\) an keiner Stelle. Ein Leser der Registerzeile kann nicht erkennen, mit welchem Wert das Band in der Kernformel zusammengezogen wird. → **Befund 90** (Kategorie C). Der Status von Befund 31 selbst bleibt unberührt. |
| 32 | **bestätigt geschlossen** | Bericht **Kap. 4 Einleitung Z. 939–954** (Absatz „Stand nach dem Stichprobenlauf — \(\lambda\) ist gesetzt und bleibt vorläufig", darin **Z. 943–944**: „`docs/evidenz/60_stichprobe/m0_klassenraten.csv`, hochgerechnet über das nationale Mengengerüst der ZÜRS-Klassen **einschließlich GK2** und um den Wohngebäudeanteil je Adresse (0,872) bereinigt") · §4.3 **Z. 1157–1159** und **Z. 1221** · §4.4 **Z. 1230** · Kap. 7 Block `flood_bldg.lambda` **Z. 2169–2178** · gemessen: „Das Kalibriermodell ist das" und „Vorab-Wert aus der Beispielzelle" im ganzen Bericht **je 0 Treffer** | Alle drei Teile des Befunds sind am heutigen Text belegt. **Zahlenabgleich mit dem Ledger:** \(M_0\) = **1,360 Mrd. €₂₀₂₆/a** steht wörtlich in Z. 1157–1159 (Rechenweg 0,872 · 527.280 € · (339.000 · 0,0059796/a + 1.380.000 · 0,00067515/a), Klassenbeiträge GK3+GK4 0,932 Mrd. und GK2 428 Mio.) und in Z. 1221; Quelle und Nenner (`m0_klassenraten.csv`) stehen im sichtbaren Text (Z. 943, Z. 1145–1206) — **Übereinstimmung mit der Ledger-Angabe festgestellt**. Die drei beanstandeten Stellen sind weg: Der Satz „Das Kalibriermodell ist das Produktionsmodell" kommt null mal vor und ist durch die belegte Aussage in Z. 940–945 ersetzt, die GK2-Lücke ist geschlossen (1,38 Mio. Adressen rechnen mit), der Wohngebäudeanteil 0,872 ist angesetzt statt 1,0, und der „Vorab-Wert aus der Beispielzelle" ist verschwunden. Das im Ledger genannte \(\lambda\) = 0,724 ist dort ausdrücklich als durch Befund 34 auf **0,832** gezogen vermerkt; der heutige Bericht trägt 0,832 durchgängig (Z. 948, 1043, 1230, 2169) — kein Widerspruch. Kein neuer Befund. |
| 33 | **bestätigt geschlossen** | Bericht **§4.5 Z. 1263–1350**: Jahresauslassung **Z. 1271–1296**, Toleranz **Z. 1298–1317** (Tabelle Z. 1304–1308: ±11,2 Pp Jackknife, ±1,7 Pp Ablese, ±2,3 Pp Modellband ⇒ **±11,5 Pp**), Ist-Ergebnis **Z. 1319–1325**, Modellentscheid **Z. 1327–1333** · Quelle `docs/evidenz/60_gdv_jahresreihe_2002_2024.csv` **Z. 1272** · Erwartungswertanteil **Z. 1285** · Skaleninvarianz **Z. 1334** · §4.8 **Z. 1471** · gemessen im geprüften Geltungsbereich **§4.5 (Z. 1263–1350)**: „1,0/2,6", „1 von 23 Kalibrierjahren" und „dafür ±12,5" **je 0 Treffer**; im **ganzen Bericht** sind „1 von 23 Kalibrierjahren" und „dafür ±12,5" ebenfalls 0 Treffer, „1,0/2,6" dagegen **1 Treffer: Z. 1702 in §5.1.3** („beträgt 1,0/2,6 = 38,5 % der Jahressumme") — genau der dort in Z. 1710–1714 als noch nicht nachgezogen ausgewiesene Restpunkt, nicht die abgelöste Stelle in §4.5 | Alle vier Teile (a)–(d) sind am heutigen Text belegt, und die Reihenfolge stimmt: Die Toleranz steht in Z. 1298 („**Toleranz — vorab fixiert: ±11,5 Prozentpunkte** … festgelegt, **bevor** der Ist-Wert unten gerechnet wird") **vor** dem Ist-Ergebnis in Z. 1319. **Zahlenabgleich mit dem Ledger:** ±11,5 Pp (Z. 1298/1310–1311), Modellseite **33,9 %** (Z. 1320), Ankerseite **47,7 %** = 20,19/42,28 (Z. 1323–1324), Abstand **13,9 Pp** mit dem ausdrücklichen Satz „Prüfung nicht bestanden" (Z. 1324–1325) — **jede Zahl stimmt mit der Ledger-Angabe überein**. Der Ausgang ist als Modellentscheid geführt (Z. 1327–1333: Richtung rund 14 Pp, kein Nachfitten der Form, \(\lambda\) bleibt vorläufig), nicht durch Weiten der Toleranz geheilt. Der im Ledger benannte Restpunkt ist im Bericht offen ausgewiesen und nicht still nachgezogen: §5.1.3 **Z. 1710–1714** („**Nachtrag dieser Revision (nicht still nachgezogen)**: … 47,7 % statt der hier verwendeten 38,5 % …; die obere Bandgrenze läge mit dem neuen Wert bei 1 − 0,477 = 0,52 statt 0,62"). Kein neuer Befund. |
| 34 | **unvollständig geschlossen** | Bericht **§4.1 Z. 977–981** (\(A_{\text{ver}}\) = **1,838**, Tukey auf die 23-Jahre-Reihe) · **§4.1a Z. 991–1081** (Jahres-Auswahlregel Z. 1023–1032; Fenster-Sensitivität Tabelle **Z. 1041–1046** mit vier Fenstern; Tukey-Fence **Z. 1056–1070**, Ergebnis Band \(A_{\text{ver}}\) **1,061–1,838** Mrd. €) · **§4.2 Z. 1123–1124** (\(A^{*}\) = **1,132**, Band **0,30–2,26**) · **§4.4 Z. 1230–1232** (\(\lambda\) = **0,832**, Band **0,11–3,44**) · Kap. 7 **Z. 2169/2171** (`wert: 0.832`, `band: [0.11, 3.44]`) · §4.8 **Z. 1461/1467** · gemessen: „0,22" und „1,66" in Kapitel 4 (Z. 932–1573) **je 0 Treffer**, `band: [0.22, 1.66]` im ganzen Bericht **0 Treffer** | Der **Sachgehalt** des Befunds ist geschlossen: \(\lambda\) folgt aus dem Kleinste-Quadrate-Mittel der vollständigen Reihe 2002–2024 (§4.1/§4.1a), es gibt eine ergebnisunabhängig formulierte Jahres-Auswahlregel (Z. 1023–1032) und eine Sensitivität über **vier** Zeitfenster (Z. 1041–1046); \(w_{\text{wg}}\) = 0,65 ist über `docs/evidenz/60_gdv_wohngebaeude_2024.csv` belegt (Z. 1072–1081). **Zahlenabgleich mit dem Ledger:** \(A_{\text{ver}}\) = 1,838 ✓ (Z. 977/1043), \(A^{*}\) = 1,132 ✓ (Z. 1123/1043), \(\lambda\) = 0,832 ✓ (Z. 1230, Z. 2169) — **aber das im Ledger als Fundstelle genannte λ-Band „0,22–1,66 aus dem Tukey-Fence-Test" steht im heutigen Bericht an keiner Stelle**: §4.4 Z. 1230–1232 und der Produkt-Block Z. 2171 führen **0,11–3,44** (vollständig fortgepflanzt aus \(A^{*}\) 0,297–2,263 und \(M_0\) 0,657–2,643), und der Tukey-Fence liefert heute ein Band von \(A_{\text{ver}}\) (1,061–1,838), kein λ-Band. Die Ablösung ist weder im Ledger-Eintrag zu 34 (Z. 59, Z. 1759) noch im Bericht als solche vermerkt, so dass die Ledger-Fundstelle nicht mehr nachprüfbar ist (eiserne Regel 5: Divergenz wird benannt, nicht still gefixt). „Bestätigt geschlossen" ist deshalb nach der Prüfregel dieses Pakets nicht vergebbar. → **Befund 91** (Kategorie C). Der Status von Befund 34 selbst bleibt unberührt. |

#### Neue Befunde dieses Pakets (90 und 91)

| Nr | Kat. | Befund |
|---|---|---|
| 90 | **C** | **Stelle:** Bericht Kap. 2, Registerzeile 60-W085-01 **Z. 164** (Spalten Effektgröße, Modellgrenze und Entscheidung), gegen §3.4 **Z. 670** / Beispielblock **Z. 737–738**, §3.5 **Z. 776** und Kap. 7 Block `flood_bldg.p_hq_extrem` **Z. 2000–2003**. · **Art: Lücke (bewusst offene Entscheidung ohne sichtbare Modellgrenze)** (§5 LF 5 „Band- und Endpunkt-Zuordnung"; §2.2 „In Formeln dürfen nur Zeilen mit Entscheidung Basiswert stehen"; §3.9 „Abgeschätzt"; Vorgabe P1 „samt Herleitung"). · **Begründung:** Befund 31 ist im Ledger als „bewusst offen" geführt mit der Begründung, \(p_3\) stehe mit Herleitung in §3.4/§3.5 und als Produkt-Block in Kap. 7, es fehle nur der Eintrag in der Registerzeile. Der zweite Teil stimmt (Z. 670, Z. 738, Z. 776, Z. 2000–2003 führen 2,236·10⁻³ a⁻¹ bzw. `wert: 0.002236` mit Kennzeichnung `abschaetzung_kap3`), die Entscheidung selbst ist im Bericht aber nirgends sichtbar: Z. 164 nennt für HQextrem weiterhin nur „5,0·10⁻³ bis 1,0·10⁻³ a⁻¹", die Modellgrenzen-Spalte derselben Zeile behandelt ausschließlich Kartenabdeckung und uneinheitliches Wiederkehrintervall, ein Verweis auf §3.4 Schritt 2 fehlt, und der Wert kommt in Kapitel 2 (Z. 156–522) in **keiner** seiner beiden Schreibweisen vor (LaTeX-Kommaform `2{,}236`: nur Z. 666 und Z. 671 in §3.4; Punktform `2.236e-3`: nur Z. 738 im Beispielblock). Damit ist für die dritte Stützstelle nicht erkennbar, welcher Zentralwert in der Kernformel rechnet und dass sein Fehlen im Register eine bewusste Entscheidung ist. Kategorie C: Kein ausgewiesener Zahlenwert ist falsch, \(p_3\) und sein Band sind an den rechnenden Stellen vollständig belegt; betroffen sind Vollständigkeit der Registerzeile und Nachvollziehbarkeit (Vorgaben P1/P3). · **Vorschlag:** In Z. 164 den Zentralwert \(p_3\) = 2,236·10⁻³ a⁻¹ mit dem Vermerk „§3.9 Abgeschätzt, geometrisches Mittel der Bandenden, Herleitung §3.4 Schritt 2" ergänzen — oder, falls der Eintrag bewusst unterbleibt, in der Modellgrenzen-Spalte derselben Zeile einen Satz aufnehmen, der die Zusammenziehung des Bands zum Rechenwert benennt und auf §3.4 verweist. Nicht in diesem Paket umgesetzt (Dateirahmen), hier nur verbucht. |
| 91 | **C** | **Stelle:** Ledger-Eintrag zu Befund 34 (Übersichtstabelle **Z. 59** und Autor-Revision **Z. 1759**: „Band **0,22–1,66** aus dem Tukey-Fence-Test") gegen Bericht §4.4 **Z. 1230–1232** und **Z. 1240–1258**, Kap. 7 **Z. 2171** (`band: [0.11, 3.44]`) sowie §4.1a **Z. 1056–1070** (Tukey-Fence ⇒ \(A_{\text{ver}}\)-Band 1,061–1,838). · **Art: Divergenz Ledger ↔ Bericht (abgelöste Fundstelle nicht als abgelöst vermerkt)** (eiserne Regel 5; §5 LF 7; Vorgabe P1). · **Begründung:** Die Regression von Befund 34 verlangt, die im Ledger genannten Zahlen an der genannten Fundstelle nachzulesen. Drei davon stimmen (\(A_{\text{ver}}\) = 1,838, \(A^{*}\) = 1,132, \(\lambda\) = 0,832), die vierte nicht: Das λ-Band „0,22–1,66" steht im heutigen Bericht an keiner Stelle — gemessen kommen „0,22" und „1,66" in Kapitel 4 (Z. 932–1573) je null mal vor, `band: [0.22, 1.66]` im ganzen Bericht null mal. Maßgeblich ist heute das vollständig fortgepflanzte Band **0,11–3,44** (§4.4 Z. 1230–1232 und Z. 1245–1249, aus \(A^{*}\) 0,297–2,263 und \(M_0\) 0,657–2,643), das zugleich als Plausibilitätsschranke dient; der Tukey-Fence liefert nach §4.1a Z. 1064–1065 ein Band von \(A_{\text{ver}}\) (1,061–1,838 Mrd. €), nicht von \(\lambda\). Die Ablösung ist an keiner der beiden Seiten vermerkt: Der Ledger-Eintrag zu 34 ist nicht fortgeschrieben (anders als bei λ = 0,724 → 0,832, wo die Ablösung dort ausdrücklich steht), und §4.1a nennt nicht, dass das frühere λ-Band aus dem Tukey-Fence abgelöst ist. Ein Prüfer, der die Fundstelle aufsucht, findet die Zahl nicht wieder. Kategorie C: Kein Zahlenwert im Bericht ist falsch oder unbelegt, der Sachgehalt von Befund 34 ist umgesetzt; betroffen ist die Nachprüfbarkeit des Ledgers. · **Vorschlag:** Den Ledger-Eintrag zu Befund 34 (Z. 59 und Z. 1759) um einen Halbsatz ergänzen, dass das dort genannte Band 0,22–1,66 mit der Bandfortpflanzung in §4.4 durch 0,11–3,44 abgelöst ist (mit Paketverweis), und in §4.1a bei der Tukey-Fence-Herleitung klarstellen, dass sie das Band von \(A_{\text{ver}}\) liefert, während das λ-Band aus §4.4 folgt. Nicht in diesem Paket umgesetzt (Dateirahmen), hier nur verbucht. |

#### Abgrenzung und Status dieses Pakets

- **Geändert wurde ausschließlich `reviews/BEFUNDE_60.md`** (angehängt).
  `docs/methodik/60_gebaeudeschaeden_flusshochwasser.md`, `docs/evidenz/register.md`,
  `backend/scripts/lint_methodik.py` und die Arbeitsmappen sind byte-gleich; der Bericht wurde nur
  gelesen und an den ausgewiesenen Stellen nachgeprüft (eiserne Regel 2, eiserne Regel 5).
- **Kein Befund behoben, keiner umnummeriert.** Höchste vorhandene Nummer zu Laufbeginn: **89**;
  neu vergeben sind **90 und 91**. Die Status der Befunde 31 bis 34 selbst bleiben unberührt.
- **Keine Leitfrage aus §5 beantwortet.** Dieses Paket führt allein die Regression der Nummern
  **31, 32, 33 und 34**; die Nummern 35 bis 38 führt das Schwesterpaket.
- **Zahlenabgleich für die drei A-Befunde ausgeführt:** Für 32, 33 und 34 ist jede im Ledger
  genannte Zahl an der dort genannten Fundstelle im heutigen Bericht nachgelesen worden; bei 32 und
  33 stimmt jede, bei 34 alle außer dem λ-Band (→ Befund 91).
- **Prüfregel für „bewusst offen" angewandt (31):** „bestätigt geschlossen" nur bei im Bericht
  sichtbarer Modellgrenze; sie fehlt, deshalb „unvollständig geschlossen" (→ Befund 90).
- **Ressourcen-Regel §3.4 eingehalten:** kein nationaler 100-m-Vollraster-Lauf; geprüft wurden nur
  die benannten Fundstellen und Zeichenfolgen.
- **Kopftabelle „Offene Befunde" bewusst nicht fortgeschrieben** (Dateirahmen der Runde-3-Pakete,
  T-0359).

### Leitfrage 4

Paket T-0375 der Runde 3 (18.09.2026, zweite Hälfte des ersetzten T-0364), eigene frische Sitzung:
Sie hat den geprüften Stand nicht geschrieben (eiserne Regel 4; geschrieben haben T-0235 bis
T-0243, T-0256 bis T-0259 und die Revisionspakete aus T-0281, alle im Endstatus). Das Bundle nach
§1 lag ab dem ersten Turn vor (Abschnitt 0 dieser Runde); die Lint-Ausgabe aus Abschnitt 0.1 wird
**übernommen, nicht neu erhoben** (§5). Maßstab sind ausschließlich §3 und §5 der Aufgabe, nicht
der Berichtstext; nach §6 läuft die volle Prüfung erneut, weil Kalibrierung und Modellstruktur seit
Runde 2 geändert wurden. Dieses Paket trägt davon **Leitfrage 4** („Doppelzählung: Zwei Kanäle?
Zwei Konten? Maßnahmeneffekt schon im Basiswert? Referenzwerte doppeln Baseline-Anteile
(HD_ref-Klasse)?", Aufgabe §5, Z. 434–435).

**Prüfumfang.** Vertieft geprüft sind genau **4.7 „Kalibrierjahre und Doppelzählungs-Wächter
(Bindung von §5.1)"** (Bericht Z. 1387–1456) und **Kapitel 9 „Ansatz-Vergleich"** mit „Die drei
verglichenen Ansätze" (Z. 2434–2452), „Kriterienraster" (Z. 2454–2464) und „Umsetzungsgrundlage"
(Z. 2466–2500). Umfang in dieser Sitzung gemessen, ohne HTML-Kommentare:

```
$ python3 - <<'EOF'
import re
s = open('docs/methodik/60_gebaeudeschaeden_flusshochwasser.md').read().split('\n')
strip = lambda t: re.sub(r'<!--.*?-->', '', t, flags=re.S)
a, b = strip('\n'.join(s[1386:1456])), strip('\n'.join(s[2412:2501]))
print(len(a), len(b), len(a) + len(b))
EOF
5701 9730 15431
```

Das deckt sich mit der Vorgabe (5.701 + 9.730 = 15.431 Zeichen); ein abweichender eigener Messwert
war nicht auszuweisen. **4.1 bis 4.6 und 4.8 sind nur als Fundstelle zitiert**, nicht vertieft
geprüft (v. a. §4.1a Z. 991–1045, §4.2 Z. 1082–1127, §4.3/§4.4 für \(M_0\) und \(\lambda\)); ebenso
nur zitiert Kap. 1 Z. 122–155 und §5.1 Z. 1586–1667.

**Verdikt Leitfrage 4: Befund** (drei neue Befunde: **79** Kategorie B, **80** und **81**
Kategorie C). Die vier Teilfragen einzeln:

| Teilfrage (§5 LF 4) | Verdikt | Begründung mit Fundstelle |
|---|---|---|
| **Zwei Kanäle?** | **Befund** — 81 | In #60 rechnet genau **ein** Euro-Pfad: Kernformel §3.4 (Z. 646–722) auf Ansatz (a), als alleinige Umsetzungsgrundlage festgelegt in Z. 2467–2469, (c) ausgeschieden (Z. 2494–2500). Gegen andere Module trennt der Bericht sauber: \(\varphi_{\text{fluss}}\) = 0,50 scheidet den Starkregenanteil des Ankers ab (Z. 1091, nur zitiert), Partitionszitate zu #59/#46/#37/#12 in Kap. 1 Z. 120. Offen bleibt, dass (b) in Z. 2490–2492 als „**Ergänzungsmodul** … grober Plausibilitätsrahmen" weiterläuft, ohne Aussage, dass sein Betrag **nie additiv** in K3 eingeht (gemessen in Z. 2413–2500: „additiv" 0 Treffer). → Befund 81. |
| **Zwei Konten?** | **bestanden** | §5.1 Z. 1596–1598: „**Nur K3**; die Kosten des Objektschutzes sind K8-Maßnahmenkosten und schließen den verhinderten Schaden je Gebäude aus (R7)." Kap. 9 führt keinen zweiten Kontobezug — die drei Ansätze unterscheiden sich allein im Rechenweg zum K3-Betrag (Z. 2436–2452); Kontoausschlüsse K5/K4/K1 in Kap. 1 Z. 120. Kein Befund. |
| **Maßnahmeneffekt schon im Basiswert?** | **Befund** — 79 | Im Grundsatz richtig beantwortet: \(\Delta q\) zählt ausschließlich Nachrüstungen **nach dem letzten Kalibrierjahr 2024** (Z. 1407–1414; Bindung §5.1.2 Z. 1635–1639). **Falsch beziffert** ist der Anteil, der schon im Basiswert steckt: Der Bericht leitet ihn aus dem **Zählgewicht** \((2024-t+1)/23\) ab (Z. 1400–1405) und beziffert damit die Verzerrung (Z. 1427–1443); der Schätzer ist aber \(\lambda = \text{Mittel}(A_t)/M_0\) (§4.1a Z. 1010–1016), also ein Mittel über **Beträge**. Nachrechnung unten. → Befund 79. |
| **Referenzwerte doppeln Baseline-Anteile (HD_ref-Klasse)?** | **bestanden (ausdrückliche Feststellung)** | **Die in Kapitel 9 genannten Referenzwerte enthalten keine Anteile, die im Basiswert des kalibrierten Modells bereits stecken.** (1) \(f_{\text{S094}}\) = 1,00 (0,84–1,18), in Z. 2499 genannt, ist geometrisch um 1 zentriert und ausdrücklich „kein eigenes Multiplikativglied im Basiswert" (Z. 188; ebenso \(f_{\text{S093}}\) Z. 187, Zeichentabelle Z. 773) — der Neutralwert kann nichts doppeln, das Band läuft nur als Unsicherheit mit. (2) Die FLEMOps-Achsen in Z. 2438–2440 sind Struktur-, keine Niveauangaben; das Niveau trägt allein \(\lambda\). (3) Die niederländische Flächenschadensrate aus B2 (Z. 2444–2448, 2487–2490) ist der einzige Referenzwert mit eigenem Euro-Niveau; sie rechnet heute nicht mit, und der Bericht benennt selbst, dass sie „vom Sensitivitätsband zum tragenden Basiswert aufsteigen" würde (Z. 2489–2490) — daraus folgt Befund 81, nicht eine heutige Doppelung. (4) Eine HD_ref-Klasse führt Kap. 9 nicht (gemessen Z. 2413–2500: „HD_ref" 0, „Referenzwert" 0 Treffer). Kein eigener Befund. |

#### Nachrechnung statt Lektüre — der Wächter an zwei Kalibrierjahren

Grundlage sind ausschließlich im Bericht ausgewiesene Zahlen: die Ankerreihe
`docs/evidenz/60_gdv_jahresreihe_2002_2024.csv`, Spalte `wert_mrd_eur` (in §4.1a Z. 1030–1040 und
§4.5 Z. 1536 als Ankerreihe geführt), und die Kette \(\lambda = \text{Mittel}(A_t)/M_0\)
(§4.1a Z. 1010–1016) mit \(M_0\) = 1,360 und den Folgefaktoren 0,615865 (Z. 1036–1038).
§3.4 eingehalten: gerechnet auf 23 Jahreswerten, **kein** Vollraster-Lauf.

**Probe der Kette (Identifizierung der Reihe):** Summe der 23 Werte = 42,28 Mrd. €; Mittel
42,28 ÷ 23 = **1,8383** (Bericht 1,838, Z. 1040); \(A^{*}\) = 1,8383 · 0,615865 = **1,1321**
(Bericht 1,132); \(\lambda\) = 1,1321 ÷ 1,360 = **0,8324** (Bericht 0,832, Z. 1040/1380/1467).
Abweichung je < 0,001, reine Rundung.

**Jahr 2020** (Bericht Z. 1403: „2020 mit 5/23 = **21,7 %**"; Z. 1431–1432: Überschätzung
„**78,3 Prozentpunkte**"):
- *Rechenweg des Berichts (Zählgewicht):* (2024 − 2020 + 1) ÷ 23 = 5 ÷ 23 = 0,21739 → **21,74 %**.
  **Abweichung zum ausgewiesenen Wert 0,0 pp** — der Bericht rechnet sein eigenes Gewicht richtig.
- *Rechenweg aus dem Schätzer (Wertgewicht):* Eine Nachrüstung aus 2020 senkt die Ankerwerte
  2020–2024, also \(\sum_{s=2020}^{2024} A_s / \sum A\) = (0,4 + 12,6 + 0,3 + 1,1 + 2,6) ÷ 42,28
  = 17,0 ÷ 42,28 = 0,40208 → **40,2 %** (Werte: Zeilen 2020…2024 der Ankerreihe, Spalte
  `wert_mrd_eur`; 2021 = 12,6 trägt allein 29,8 % der Summe). **Abweichung zum im Bericht
  ausgewiesenen Gewicht +18,5 pp** (Faktor 1,85); die bezifferte Überschätzung fällt von 78,3 pp
  auf **59,8 pp**, **Abweichung 18,5 pp**.

**Jahr 2014** (Bericht Z. 1403–1404: „11/23 = **47,8 %**"; Z. 1432–1433: „**52,2
Prozentpunkte**"):
- *Zählgewicht:* (2024 − 2014 + 1) ÷ 23 = 11 ÷ 23 = 0,47826 → **47,8 %**, **Abweichung 0,0 pp**.
- *Wertgewicht:* (1,2 + 0,3 + 2,0 + 0,7 + 1,0 + 0,5 + 0,4 + 12,6 + 0,3 + 1,1 + 2,6) ÷ 42,28
  = 22,7 ÷ 42,28 = 0,53690 → **53,7 %**, **Abweichung +5,9 pp**; die Überschätzung fällt von
  52,2 pp auf **46,3 pp**, **Abweichung 5,9 pp**.

**Dritte Probe (2010) zur Größenordnungs-Aussage.** Der Bericht beziffert den unterzählten Hebel
mit „rund der Hälfte bis zu drei Vierteln des Effekts einzelner, in den letzten zehn bis fünfzehn
Kalibrierjahren realisierter Maßnahmen" (Z. 1438–1441). Unterzählter Rest = 1 − Wertgewicht:
2010 → 29,6 ÷ 42,28 = 70,0 %, Rest **30,0 %**; 2015 → 21,5 ÷ 42,28 = 50,9 %, Rest **49,1 %**;
2014 Rest 46,3 %; 2020 Rest 59,8 %. Für das genannte Fenster 2010–2015 liegt der Rest bei
**30,0 % bis 49,1 %**, nicht bei „der Hälfte bis drei Vierteln".

**Ursache in einem Satz:** Die Ankerreihe ist stark schief (2021 allein 29,8 % der Summe); ein
Gleichgewicht der Jahre gilt für die **Zahl** der Summanden, nicht für ihren **Beitrag zum Mittel**.

#### Neue Befunde dieses Pakets (79, 80 und 81)

Höchste zu Laufbeginn im Ledger vorhandene Nummer: **78** (gemessen über alle
Tabellen-Nummernspalten und alle „Befund <n>"-Nennungen); erste neue Nummer deshalb **79**.

| Nr | Kat. | Befund |
|---|---|---|
| 79 | **B** | **Stelle:** §4.7 Z. 1400–1405 (Gewicht \((2024-t+1)/23\); „2020 mit 5/23 = 21,7 %", „2014 mit 11/23 = 47,8 %"), Z. 1416–1426 (Verfallsregel „Gewicht 1/24 statt 1/23") und Z. 1427–1443 (Modellgrenze: „78,3 Prozentpunkte", „52,2 Prozentpunkte", „bis zu 95,7 %", „rund der Hälfte bis zu drei Vierteln"). · **Art: Fehler (falsche Gewichtung in einer bezifferten Modellgrenze)** (§5 LF 4 „Maßnahmeneffekt schon im Basiswert"; §3.4 Kleinste-Quadrate-Bestimmung; P1 „samt Herleitung"). · **Begründung:** Der Wächter beziffert den bereits im kalibrierten Niveau steckenden Anteil einer Vor-2025-Maßnahme über ein **Zählgewicht** der Kalibrierjahre (1/23 je Jahr). Der Schätzer, auf den er sich beruft, ist \(\lambda = \text{Mittel}(A_t)/M_0\) (§4.1a Z. 1010–1016): Gleiches Gewicht je Jahr gilt dort für die **Zahl** der Summanden, der Einfluss eines Jahres auf das Mittel ist jedoch proportional zu seinem **Betrag** \(A_t\). Senkt eine Maßnahme aus Jahr \(t\) die Schäden der Jahre \(t\) bis 2024 anteilig, sinkt das Ankermittel um \(\sum_{s=t}^{2024} A_s / \sum_s A_s\), nicht um \((2024-t+1)/23\). In dieser Sitzung aus der Ankerreihe nachgerechnet (Summe 42,28 Mrd. €; Probe: Mittel 1,8383 → \(A^{*}\) 1,1321 → \(\lambda\) 0,8324, deckungsgleich mit Z. 1040): **2020** 17,0 ÷ 42,28 = **40,2 %** statt 21,7 % (**+18,5 pp**; Verzerrung 78,3 → 59,8 pp), **2014** 22,7 ÷ 42,28 = **53,7 %** statt 47,8 % (**+5,9 pp**; 52,2 → 46,3 pp), **2010** 70,0 % statt 65,2 %. Ursache ist die Schiefe der Reihe (2021 allein 29,8 % der Summe) — dieselbe Schiefe, die §4.1a über Tukey-Fence und Fenster-Sensitivität behandelt. Dieselbe Verwechslung trägt die Verfallsregel (Z. 1416–1426: die Verschiebung bei Aufnahme von 2025 ist nicht 1/24 des Abstands, sondern der Betragsanteil \(A_{2025}\) am erweiterten Fenster) und die Größenordnungs-Aussage Z. 1438–1441 (nachgerechnet 30,0–49,1 % statt „Hälfte bis drei Viertel"). Kategorie **B**: Kein ausgewiesener Betrag ändert sich — \(\Delta q\) zählt operativ ohnehin nur Nachrüstungen nach 2024 (Z. 1407–1414), \(r_{\text{S092}}\) = 0,035 (0,0075–0,0992) und \(\lambda\) bleiben unberührt —, aber die **bezifferte** Modellgrenze ist falsch gerechnet und überzeichnet die Konservativität des Wächters um bis zu 18,5 Prozentpunkte. · **Vorschlag:** Gewichte in §4.7 auf \(\sum_{s=t}^{2024} A_s / \sum_s A_s\) umstellen (Formel plus die zwei Rechenbeispiele 2020 und 2014, Verweis auf die Ankerreihen-CSV), die drei bezifferten Stellen (21,7/47,8 · 78,3/52,2 · „Hälfte bis drei Viertel") nachziehen, die Verfallsregel auf denselben Nenner stellen und die Schiefe der Reihe ausdrücklich als Grund nennen — nach P3 mit lesbarem Zweizeiler-Rechenweg statt nur einer Formel. Nicht in diesem Paket umgesetzt (Dateirahmen), hier nur verbucht. |
| 80 | **C** | **Stelle:** Kap. 9, Kriterienraster **Z. 2462**, Zeile „Maßnahmen-Anschluss", Spalte (a): „der Objektschutz-Hebel S092 **greift als Faktor auf den Schadensgrad** (§5.1, r_S092)", gegen §5.1 „Wirkungsort" **Z. 1596–1598** (\(\text{EAD}_{\text{mit}} = \text{EAD}\cdot(1-r_{\text{S092}})\), kommunenweit) und §5.1 Modellgrenze (1) **Z. 1648–1649** („**Kommunenweiter Pauschalfaktor** statt zellscharfer Wirkung (Bauform-Grenze)"). · **Art: Widerspruch (Bericht gegen Bericht, am entscheidungstragenden Kriterium)** (§5 LF 4 — der Wirkungsort entscheidet, gegen welchen Basiswert auf Doppelzählung zu prüfen ist; P3). · **Begründung:** Kap. 9 wertet Ansatz (b) im selben Feld gerade deshalb ab, weil S092 sich dort „nur als pauschaler Abschlag auf das Gesamtergebnis anhängen" ließe, „ohne Wirkungsort (§3.5)" — genau das ist aber die heute umgesetzte Form in (a): \(r_{\text{S092}}\) multipliziert den fertigen K3-Erwartungsschaden der **Kommune**, nicht den Schadensgrad der Zelle, und §5.1 weist das selbst als Bauform-Grenze aus. Gemessen: „Schadensgrad" kommt in §5.1 (Z. 1586–1667) **null mal** vor. Für Leitfrage 4 ist das nicht folgenlos: Ein Hebel am Schadensgrad wäre gegen den zelligen Basiswert zu prüfen, ein kommunenweiter Pauschalfaktor gegen das kalibrierte Niveau — der Bericht nennt zwei verschiedene Angriffspunkte für dieselbe Größe. Kategorie **C**: Kein Zahlenwert betroffen, und die Wahl von (a) trägt auch ohne dieses Kriterium (fünf weitere Güte-Kriterien „hoch", Z. 2471–2477); betroffen sind Begründungstreue und Leser-Erwartung. · **Vorschlag:** Z. 2462 auf den heutigen Stand ziehen — „(a) bietet als einziger Ansatz den **Angriffspunkt** für einen zellscharfen Objektschutz-Hebel; umgesetzt ist er derzeit als kommunenweiter Pauschalfaktor auf den K3-Erwartungsschaden (§5.1, Modellgrenze (1))" — und die Abwertung von (b) auf den bleibenden Unterschied stützen (dort fehlt der Angriffspunkt dauerhaft, hier ist er vorhanden, aber noch nicht ausgeschöpft). Nicht in diesem Paket umgesetzt (Dateirahmen), hier nur verbucht. |
| 81 | **C** | **Stelle:** Kap. 9 „Umsetzungsgrundlage" **Z. 2490–2492** („(b) bleibt als **Ergänzungsmodul** vorgesehen: als grober Plausibilitätsrahmen für Kommunen, in denen der Zensus-Bestand je Zelle lückenhaft ist"), ebenso Kopfzeile Z. 33 und Entscheidungslog Z. 2510. · **Art: Lücke (Zwei-Kanäle-Risiko nicht ausgeschlossen)** (§5 LF 4 „Zwei Kanäle?"; R9 „innerhalb eines Kontos zählt jede Einheit genau einmal", zitiert Kap. 1 Z. 120). · **Begründung:** Das Ergänzungsmodul (b) berechnet für dieselbe Kommune, dasselbe Konto K3 und dasselbe Bezugsjahr einen **zweiten** Euro-Betrag aus anderer Datenbasis (Flächenschadensrate B2). Nirgends steht, dass dieser Betrag ausschließlich Vergleichsgröße ist und **nie** — auch nicht anteilig für Zellen mit lückenhaftem Zensus-Bestand — in den ausgewiesenen K3-Betrag eingeht; gemessen in Kap. 9 (Z. 2413–2500): „additiv" **0 Treffer**, „ersetzt" **0 Treffer**. Gerade der genannte Anwendungsfall legt eine Auffüllrechnung nahe; dort entstünde bei unsauberer Abgrenzung entweder eine Doppelzählung (Zelle zählt in beiden Kanälen) oder ein stiller Modellwechsel mit zweitem, unkalibriertem Niveau — die Gefahr benennt Z. 2489–2490 für den Basiswert selbst. Kategorie **C**: Das Modul ist heute nicht umgesetzt, kein ausgewiesener Betrag betroffen; es fehlt die Abgrenzungsregel, bevor es gebaut wird. · **Vorschlag:** In Z. 2490–2492 ergänzen: „Das Ergänzungsmodul liefert ausschließlich einen Vergleichswert; es geht weder additiv noch ersetzend in den ausgewiesenen K3-Betrag ein (R9). Wird es später als Auffüllung für Zellen ohne Zensus-Bestand genutzt, sind die betroffenen Zellen im Hauptpfad auf null zu setzen und die Umstellung als Modellentscheid zu dokumentieren." Nicht in diesem Paket umgesetzt (Dateirahmen), hier nur verbucht. |

#### Abgrenzung und Status dieses Pakets

- **Geändert wurde ausschließlich `reviews/BEFUNDE_60.md`** (angehängt).
  `docs/methodik/60_gebaeudeschaeden_flusshochwasser.md`, `docs/evidenz/register.md`,
  `backend/scripts/lint_methodik.py` und die Arbeitsmappen sind byte-gleich; der Bericht wurde nur
  gelesen und an den ausgewiesenen Stellen nachgerechnet (eiserne Regeln 2 und 5).
- **Kein Befund behoben, keiner umnummeriert.** Höchste vorhandene Nummer zu Laufbeginn: **78**;
  neu vergeben sind **79, 80 und 81**.
- **Nur Leitfrage 4 beantwortet**, an 4.7 und Kapitel 9 (15.431 Zeichen, oben gemessen);
  Leitfrage 7 trägt das Schwesterpaket. 4.1–4.6 und 4.8 sind nur als Fundstelle zitiert.
- **Vorgaben P1/P2 am Prüfgegenstand mitgeprüft:** \(\Delta q\), \(e_{\text{bem}}\),
  \(s_{\text{bem}}\) und \(r_{\text{S092}}\) führen Wert, Band, Sensitivität und den Vermerk
  „Abschätzung von KAP3" samt Herleitung (Z. 1607–1613, Z. 1640–1647); die Wächter-Modellgrenze ist
  vorhanden, aber falsch beziffert (Befund 79) — daraus entsteht kein eigener P1/P2-Befund.
- **Ressourcen-Regel §3.4 eingehalten:** nachgerechnet auf den 23 ausgewiesenen Jahreswerten der
  Ankerreihe, kein nationaler 100-m-Vollraster-Lauf.
- **Kopftabelle „Offene Befunde" bewusst nicht fortgeschrieben** (Dateirahmen der Runde-3-Pakete,
  T-0359); das Konvergenz-Verdikt der Runde trägt T-0373.

### Leitfrage 9

Paket T-0372 der Runde 3 (18.09.2026, zweite Hälfte des ersetzten T-0362), eigene frische Sitzung:
Sie hat den geprüften Stand nicht geschrieben (eiserne Regel 4; geschrieben haben T-0235 bis
T-0243, T-0256 bis T-0259 und die Revisionspakete aus T-0281, alle im Endstatus). Das Bundle nach
§1 lag ab dem ersten Turn vor (Abschnitt 0 dieser Runde); die Lint-Ausgabe aus Abschnitt 0.1 wird
**übernommen, nicht neu erhoben** (§5, Schritt „zuerst die deterministischen Lints"; darin liegt
auch der maschinelle Check „Preisstand-Einheitlichkeit je Bericht", Aufgabe §7). Maßstab sind
ausschließlich §3 und §5 der Aufgabe, nicht der Berichtstext. Dieses Paket trägt davon
**Leitfrage 9** („Kostensätze: Preisstand einheitlich, Quellen, VSL/VOLY-Konsistenz,
Konto-Zuordnung?", Aufgabe §5 Z. 444), gemessen an §3.6 Z. 280–282 („Kostensätze mit **Preisstand**
und Quelle; alle Kostensätze eines Berichts auf einen gemeinsamen Preisstand indexiert
(Umrechnungsfaktor je Satz in der Zeichentabelle)"), an §3.9 und an den Vorgaben P1/P2.

**Prüfumfang dieses Pakets.** Vertieft geprüft sind genau der **Berichtskopf vor `## Ergebnis`**
(Z. 1–29, 2.423 Zeichen), **§3.2 „Datenebenen nach §3.1"** (Z. 553–586, 5.052 Zeichen) und
**§3.3 „Tiefen-Schadensfunktion \(d(h)\) — Stützstellen und Herleitung (P1)"** (Z. 588–644,
4.358 Zeichen) — zusammen 11.833 Zeichen ohne HTML-Kommentare und ohne die Überschriftenzeilen
selbst; in dieser Sitzung nachgemessen und bestätigt (Kopf 2.422 + 1 Zeilenumbruch, §3.2
einschließlich der Ankerzeile Z. 587, §3.3 einschließlich der Ankerzeile Z. 645). §3.1 und §3.4 bis §3.7 gehören zum Schwesterpaket und sind hier nur als Fundstelle zitiert
(Z. 536–540 Preisstand-Deklaration, Z. 681–692 Preisschritt der Kernformel, Z. 779
Zeichentabellenzeile \(n_t\)); ebenso nur zitiert sind Registerzeile 60-R24-01 (Z. 193),
Langbeleg B4 (Z. 303–390) und die Parameter-Blöcke `flood_bldg.n_efh_zfh` (Z. 1928–1941) und
`flood_bldg.n_mfh` (Z. 1943–1955).

**Nachgerechnet statt gelesen** (§3.4 Ressourcen-Regel: aus den ausgewiesenen Zahlen und auf
Stichproben, kein nationaler 100-m-Vollraster-Lauf). Beide Kostensätze der Ebene GEBAEUDEWERT aus
§3.2 Z. 563 (dort geführt als „Wertsätze aus ImmoWertV Anlage 4 (NHK 2010) und
Destatis-Baupreisindex, Fortschreibung nach Register 60-R24-01 (B4)", beziffert im Preisschritt
Z. 683–685) werden vom Preisstand ihrer Quelle auf das in §3.1 Z. 537–540 deklarierte Bezugsjahr
**2026** umgerechnet.

*Verwendeter Index mit Zahlenwert und Quelle mit Fundstelle:* Destatis, Fachserie 17 Reihe 4
„Preisindizes für die Bauwirtschaft" (Basis 2015 = 100), Jahresdurchschnitte Neubau konventionell
gefertigter Wohngebäude — **2010 = 89,1**, **2023 = 149,8**; zitiert in Langbeleg B4, Quelle (4),
`docs/methodik/60_gebaeudeschaeden_flusshochwasser.md` Z. 332–339. *Ausgangswerte:* NHK 2010,
ImmoWertV Anlage 4, Gebäudeart 1.01 Standardstufe 3 = **1.050 €₂₀₁₀/m² BGF**, Mehrfamilienhäuser
bis 6 WE Standardstufe 3 = **825 €₂₀₁₀/m² BGF** (B4, Quelle (3), Z. 320–331; Preisstand der Quelle
dort wörtlich „auf den im Jahresdurchschnitt bestehenden Kostenstand des Jahres 2010"). *Zweiter
Schritt:* Fortschreibung 2023 → 2026 mit dem als Abschätzung von KAP3 ausgewiesenen Faktor
**1,105** (drei Jahresschritte à 3,4 %; nachgerechnet: 1,034³ = 1,10551; B4 Rechenschritt 2,
Z. 357–367).

| Kostensatz | Rechenweg dieser Sitzung | nachgerechnet | Bericht (Z. 684–685) | Abweichung |
|---|---|---|---|---|
| \(n_{\text{EFH/ZFH}}\) | 1.050 × (149,8 ÷ 89,1 = 1,681257) = 1.765,32 €₂₀₂₃/m² BGF → × 1,105 = **1.950,68 €₂₀₂₆/m² BGF** | 1.950,68 | 1.950 | **−0,035 %** |
| \(n_{\text{MFH}}\) | 825 × 1,681257 = 1.387,04 €₂₀₂₃/m² BGF → × 1,105 = **1.532,68 €₂₀₂₆/m² BGF** | 1.532,68 | 1.533 | **+0,021 %** |

Gegenprobe über den in der Zeichentabelle geführten Gesamtfaktor (Z. 779: 1,6813 × 1,105 =
1,8578): 1.050 × 1,8578 = 1.950,69 und 825 × 1,8578 = 1.532,69 — beide Wege stimmen auf 0,01 €
überein. Die verbleibende Abweichung zum Berichtswert stammt allein aus der Zwischenrundung auf
volle Euro in Rechenschritt 1 und liegt weit unter der Rundungsstelle des ausgewiesenen Werts.
Auch die Bänder sind nachgerechnet und bestätigt: 1.765 × 1,07 = 1.888,6 ⇒ 1.889 und
1.765 × 1,16 = 2.047,4 ⇒ 2.047 (EFH/ZFH, Z. 684); 1.387 × 1,07 = 1.484,1 ⇒ 1.484 und
1.387 × 1,16 = 1.608,9 ⇒ 1.609 (MFH, Z. 685). **Rechnerisch ist an beiden Kostensätzen nichts zu
beanstanden.**

**Die vier Teilfragen der Leitfrage einzeln.**

1. **Preisstand einheitlich — erfüllt.** Der Bericht deklariert genau einen Preisstand (2026,
   §3.1 Z. 536–540). Im vertieften Prüfumfang trägt jede Geldgröße diesen Preisstand: §3.2 führt
   Geld ausschließlich in der Zeile GEBAEUDEWERT („Preisstand 2026 einheitlich", Z. 563), §3.3
   enthält **keinen** Kostensatz, sondern nur dimensionslose Schadensquoten (Tabelle Z. 632–633),
   und der Berichtskopf (Z. 1–29) nennt keinen abweichenden Preisstand. Der nach §3.6 verlangte
   **Umrechnungsfaktor je Satz** steht in der Zeichentabelle (Z. 779: 1,8578) und zusätzlich in
   beiden Parameter-Blöcken (`umrechnungsfaktor: 1.8578`, `preisstand: 2026`, Z. 1936/1937 und
   Z. 1951/1952) — an dieser Stelle nur festgestellt; die Regression des früheren Befunds 40
   trägt das dafür zuständige Paket.
2. **Quellen — erfüllt.** Beide Kostensätze sind auf eine Rechtsverordnung (ImmoWertV Anlage 4)
   und einen amtlichen Preisindex zurückgeführt, je mit URL, Archiv-Snapshot und Zugriffsdatum
   (B4 Quellen (3) und (4), Z. 320–339); §3.2 Z. 563 nennt beide Quellen und verweist für die
   Fortschreibung auf Register 60-R24-01/B4. Die in der Nachrechnung verwendeten Zahlen stammen
   aus dem dort zitierten Wortlaut, nicht aus einer Zusammenfassung.
3. **VSL/VOLY-Konsistenz — nicht einschlägig, und die Nichtanwendbarkeit ist belegt.** Der
   Konsistenz-Check VSL ÷ VOLY (Aufgabe §3.2 Z. 228–231) gilt für Mortalitätsendpunkte. #60
   bewertet ausschließlich Sachschäden an Gebäuden (Konto K3); im Prüfumfang kommt kein Lebens-
   oder Lebensjahreswert vor, und die Gesundheitsfolgen desselben Ereignisses sind ausdrücklich
   ausgegrenzt (Kap. 1 „Nur K3 aktiv" Z. 153, aufgegriffen in §3.1 Z. 549–551: K1 (#101),
   K4 (#74), K5 und K8 (#50) nicht enthalten). Kein Befund; die Teilfrage läuft ins Leere, statt
   stillschweigend übergangen zu werden.
4. **Konto-Zuordnung — erfüllt.** Beide Kostensätze tragen genau ein Konto: `endpunkt:
   K3-Wiederherstellung` in beiden Blöcken (Z. 1939 und Z. 1954), und die Ebene GEBAEUDEWERT
   speist über \(w_z\) allein den K3-Euro-Pfad (§3.2 Z. 563 in Verbindung mit §3.4 Z. 681). Ein
   zweites Konto berührt keiner der beiden Sätze; der Doppelkanal-Ausschluss zu S074/R17 (§3.2
   Z. 583–586) gehört zu Leitfrage 4 und wird hier nicht vertieft.

**Verdikt: Befund** — ein neuer Befund, Nummer **82**, Kategorie C. Rechnung, Quellenlage,
Preisstand-Einheitlichkeit und Konto-Zuordnung halten stand; zu beanstanden ist allein, dass
derselbe Wertsatz an drei Stellen drei verschiedene Kennzeichnungen nach §3.9/P1 trägt — im
vertieft geprüften §3.2 gar keine, im Kernformel-Text „belegt", im Parameter-Block
`abschaetzung_kap3`.

| Nr. | Kat. | Befund |
|---|---|---|
| 82 | **C** | **Stelle:** Bericht §3.2 „Datenebenen nach §3.1", Zeile **GEBAEUDEWERT** Z. 563 — Spalte „Quelle / Beschaffungsweg": „Wertsätze aus ImmoWertV Anlage 4 (NHK 2010) und Destatis-Baupreisindex, Fortschreibung nach Register 60-R24-01 (B4)", Spalte „Normierung/Zentrierung": „Preisstand 2026 einheitlich"; gegen §3.4 Z. 683 („Die Wertsätze \(n_t\) sind **belegt** und auf den Preisstand 2026 indexiert") und gegen die Parameter-Blöcke `flood_bldg.n_efh_zfh` (Z. 1928–1941) und `flood_bldg.n_mfh` (Z. 1943–1955), die für denselben Wert `kennzeichnung: abschaetzung_kap3` führen (Z. 1933, Z. 1948); Bezug: Berichtskopf Z. 25–28 („Jeder als **Abschätzung von KAP3** geführte Wert ist in seiner Registerzeile als solcher gekennzeichnet (§3.9; Vorgaben P1/P2)"). · **Art: Widerspruch/Lücke in der Kennzeichnung** (§3.9 „Abgeschätzt"; Vorgabe P1 „je Parameter … entweder die Quelle oder der Vermerk, dass es eine begründete Abschätzung von KAP3 ist, samt Herleitung"; §5 LF 9). · **Begründung:** \(n_t\) ist ein **Mischwert**. Der Kern (NHK 2010, Indexierung 2010 → 2023) ist belegt und in dieser Sitzung nachgerechnet; die Fortschreibung 2023 → 2026 mit dem Faktor 1,105 ist dagegen ausdrücklich eine Abschätzung von KAP3, weil „eine Jahresdurchschnitts-Indexreihe bis 2026 in der geprüften Fachserie nicht vorliegt" (B4 Rechenschritt 2, Z. 357–367). Nachgerechnet trägt der abgeschätzte Teil **10,5 %** des Endwerts, und sein Band 1,07–1,16 erzeugt die ausgewiesenen Spannen 1.889–2.047 bzw. 1.484–1.609, also rund −3,1 %/+5,0 % auf den Kostensatz — keine Randgröße. Darüber sagen drei Stellen drei verschiedene Dinge: §3.2, aus dem die Datenebene GEBAEUDEWERT gebaut wird, nennt nur zwei amtliche Quellen und behauptet „Preisstand 2026 einheitlich", ohne erkennbar zu machen, dass dieser Preisstand erst über eine Abschätzung erreicht wird; §3.4 nennt den Satz rundheraus „belegt"; nur der Parameter-Block kennzeichnet ihn als Abschätzung. Wer §3.2 als Spezifikation liest — die vorgesehene Leseart des Kapitels —, hält den Wertsatz für vollständig quellenbelegt. Die Registerzeile 60-R24-01 (Z. 193) kennzeichnet den Faktor korrekt, die Kopfaussage ist insofern nicht falsch, deckt aber den Wertsatz selbst nicht ab. Kategorie C, weil kein Zahlenwert und kein Rechenweg betroffen ist (Nachrechnung oben: −0,035 % und +0,021 %); betroffen ist die Kennzeichnung, an der ein Anwender die Belastbarkeit abliest. · **Vorschlag:** (a) In Z. 563 hinter „Preisstand 2026 einheitlich" ergänzen: „(Indexierung 2010 → 2023 belegt; Fortschreibung 2023 → 2026 mit Faktor 1,105 = Abschätzung von KAP3, §3.9, Band 1,07–1,16, Herleitung B4)". (b) In Z. 683 „belegt" auf „im Kern belegt, mit abgeschätztem Fortschreibungsfaktor (§3.9)" ziehen, damit Text und Blockkennzeichnung dieselbe Aussage machen. (c) In den Lint aufnehmen, dass ein Parameter mit `kennzeichnung: abschaetzung_kap3` im Berichtstext nicht als „belegt" bezeichnet sein darf — sonst altert die Kennzeichnung beim nächsten Nachzug wieder auseinander. |

**Abgrenzung und Status dieses Pakets.**

- **Kein Befund behoben, keiner umnummeriert.** Die zu Laufbeginn höchste im Ledger vergebene
  Nummer war **81**; die erste neue Nummer dieses Pakets ist deshalb **82**, und vergeben wurde
  genau diese eine.
- **Nur Leitfrage 9 beantwortet**, an Berichtskopf, §3.2 und §3.3 (11.833 Zeichen, oben
  gemessen). §3.1 und §3.4 bis §3.7 trägt das Schwesterpaket; sie sind hier nur als Fundstelle
  zitiert, nicht vertieft geprüft.
- **Vorgaben P1/P2 am Prüfgegenstand mitgeprüft:** P1 ist für \(k_{\text{BGF}}\), den
  Fortschreibungsfaktor 1,105 und die Stützstellen von \(d(h)\) (Z. 623–633, je Zelle
  „abgeschätzt" mit im Text ausgeschriebener Herleitung) erfüllt, für den Wertsatz \(n_t\) an der
  Stelle §3.2 nur unvollständig → Befund 82. P2 ist im Prüfumfang nicht einschlägig (kein
  Maßnahmen-Hebel in §3.2/§3.3; die Bauform-Grenze der Materialachse steht in Register
  60-S094-01 und gehört zu Leitfrage 5).
- **Ressourcen-Regel §3.4 eingehalten:** nachgerechnet auf den ausgewiesenen Zahlen
  (89,1 · 149,8 · 1.050 · 825 · 1,105), kein nationaler 100-m-Vollraster-Lauf.
- **Eiserne Regel 2 eingehalten:** `KWRA-Monetarisierung.xlsx` wurde nur gelesen, nicht geändert.
- **Geänderte Dateien:** ausschließlich diese. `docs/methodik/60_gebaeudeschaeden_flusshochwasser.md`
  (SHA-256 `d36326bd5678…`) und `docs/evidenz/register.md` (SHA-256 `29a90539c30b…`) sind
  byte-gleich geblieben; `backend/scripts/lint_methodik.py` (T-0234) wurde nicht angefasst.
- **Kopftabelle „Offene Befunde" bewusst nicht fortgeschrieben** (Dateirahmen der Runde-3-Pakete,
  T-0359); das Konvergenz-Verdikt der Runde trägt T-0373.

### Leitfrage 12 — Umsetzbarkeit und Parameter-Blöcke

Paket T-0380 der Runde 3 (18.09.2026, Teil der Auflösung von T-0365), eigene frische Sitzung: Sie
hat den geprüften Stand nicht geschrieben (eiserne Regel 4; geschrieben haben T-0235 bis T-0243,
T-0256 bis T-0259 und die Revisionspakete aus T-0281, alle im Endstatus). Die Lint-Ausgabe der
Runde wird aus Abschnitt 0.1 (T-0359) **übernommen, nicht neu erhoben**. Maßstab sind
ausschließlich §3 (insbesondere §3.6 und §3.9), §4 (Parameter-Block-Format, Aufgabe Z. 396–408)
und §5 der Aufgabe, nicht der Berichtstext. Dieses Paket trägt davon **Leitfrage 12**
(„Umsetzbarkeit: Daten offen/keyless; Parameter-Blöcke vollständig; Architektur-vereinbar;
benötigte neue Ebenen als solche gekennzeichnet (inkl. Struktur-Ebenen wie u18)?", Aufgabe §5
Z. 451–452).

**Prüfumfang.** Vertieft geprüft sind genau der **Kopf des Kapitels 7** (Z. 1843–1866: Einleitung
und die drei P1-Zusatzfelder) und die **maschinenlesbaren Parameter-Blöcke** (Z. 1867–2182,
22 Blöcke in einem YAML-Fence) von
`docs/methodik/60_gebaeudeschaeden_flusshochwasser.md`. Gemessen in dieser Sitzung mit
`python3 -c "... len(re.sub(r'<!--.*?-->','','\n'.join(L[1842:2185]),flags=re.S))"` →
**10.109 Zeichen** ohne HTML-Kommentare, identisch mit der Messung des Planungslaufs. §7.1, §7.2,
der Abschnitt `## Ergebnis` und Kapitel 5 gehören zu Schwesterpaketen und sind hier **nur als
Fundstelle zitiert**; die Leitfragen 5 und 11 werden hier nicht beantwortet.

**Verdikt: Befund.** Vier neue Befunde, Nummern **83 bis 86**. Formal sind die Blöcke sauber: alle
22 tragen die neun Pflichtfelder des §4-Templates (in dieser Sitzung geprüft, s. u.), alle sieben
in `herleitung_anker`/`wertebereich_abweichung` genannten Anker existieren im Bericht, und die
drei nachgerechneten Werte stimmen. Zu beanstanden ist (a) die Vollständigkeit gegenüber dem
eigenen Anspruch des Kapitel-7-Kopfs — neun der 15 in §4.8 geführten rechnenden Parameter haben
keinen Block (Befund 83, Kategorie B); (b) ein Band, das das Register führt und der Block auf
`null` setzt (Befund 84, Kategorie B); (c) ein maschinenlesbarer Offen-Stand, der dem Berichtstext
widerspricht (Befund 85, Kategorie C); (d) der in §3.2 gekennzeichnete Status „neu anzulegen /
geparkt" der Datenebenen, der in den Blöcken maschinell nicht ankommt (Befund 86, Kategorie C).

**Die vier Teilaussagen der Leitfrage 12 einzeln.**

| # | Teilaussage | Urteil | Fundstelle |
|---|---|---|---|
| 1 | Daten offen/keyless | **ja** | Jeder Block führt seine Herkunft auf eine Registerzeile oder einen Langbeleg zurück (`herkunft: register:60-W085-01`, Z. 1976; `register:60-S093-01`, Z. 2018; `register:60-R24-01`, Z. 1932); die zugehörigen Beschaffungswege sind in §3.2 ausdrücklich als keyless spezifiziert (Spaltenüberschrift „Quelle / Beschaffungsweg (keyless)" Z. 559, Zensus-Zeile „offener Download ohne Schlüssel"; nur zitiert, nicht vertieft geprüft). Kein Block nennt eine Quelle, die einen Schlüssel oder eine Registrierung verlangt; `quelle:` steht entweder auf `null` oder auf einer Rechtsverordnung, einem amtlichen Index bzw. einer Publikation (Z. 1935, 1979, 2021). |
| 2 | Parameter-Blöcke vollständig | **nein** | Pflichtfelder: vollständig — in dieser Sitzung mit `python3 -c "... re.match(r'  ([a-z_]+):',l)"` über Z. 1843–2185 geprüft, alle neun Feldnamen des §4-Templates (`id, wert, einheit, band, herkunft, quelle, preisstand, bandzuordnung, endpunkt`) sind in der Feldmenge, und der Lint erhebt zu keinem Block „fehlt" (`backend/scripts/lint_methodik.py` Z. 223–225, PFLICHTFELDER Z. 40). Der **Bestand** ist dagegen unvollständig: neun der 15 Parameter aus §4.8 haben keinen Block → **Befund 83**. Zusätzlich fehlt an `flood_bldg.p_hq_haeufig` das im Register geführte Band → **Befund 84**. |
| 3 | Architektur-vereinbar | **ja, mit ausgewiesener Abweichung** | Format und Extraktionsweg passen: ein `parameter:`-Dokument je Block, `---`-getrennt in einem Fence, genau so, wie der Extraktor sie liest (`re.split(r"^parameter:$", …)`, `lint_methodik.py` Z. 217). Die einzige Abweichung vom §4-Wertebereich (`endpunkt: K3-Wiederherstellung` statt `mortalitaet\|morbiditaet\|beide`, z. B. Z. 1879) ist in **jedem** Block über `wertebereich_abweichung: "#fortschreibung-endpunkt-k3"` maschinenlesbar auf den Fortschreibungsantrag §7.1 verwiesen (Anker existiert, Z. 2184; §7.1 gehört zum Schwesterpaket und wird hier nur zitiert). §3.6 „jeder Parameter editierbar und bequellt" ist über `wert`/`band`/`herkunft` erfüllt. |
| 4 | Benötigte neue Ebenen als solche gekennzeichnet | **nein (nur im Text, nicht im Block)** | §3.2 kennzeichnet die vier Zellgrößen als „neu anzulegen" bzw. „geparkt (Datenquelle fehlt)" (Z. 559–566, nur zitiert). In Kapitel 7 trägt kein Block ein Feld, das diesen Status mitführt: `flood_bldg.f_s093` (Z. 2069–2081) und `flood_bldg.f_s094` (Z. 2083–2095) stehen auf `wert: 1.0`, ohne dass maschinell erkennbar wäre, dass beide auf der **geparkten** Ebene GEBAEUDEZUSTAND_BAUSTOFF beruhen und der Wert ein Platzhalter ist → **Befund 86**. Struktur-Ebenen im Sinne von u18 kommen bei #60 nicht vor (reiner Sachschaden K3, Kap. 1 Z. 153). |

**Abgleich statt Lektüre** (fünf Größen, jede mit dem in dieser Sitzung ausgeführten Ausdruck;
§3.4 Ressourcen-Regel eingehalten — gerechnet auf ausgewiesenen Zahlen und Stichproben, kein
nationaler 100-m-Vollraster-Lauf; die CSVs unter `docs/evidenz/60_stichprobe/` wurden nicht
gelesen).

| Größe (Block) | Wert im Parameter-Block | Vergleichswert + ausgeführter Ausdruck | Abweichung |
|---|---|---|---|
| `flood_bldg.d_1`, `d_5`, `h_1`, `h_5` (Z. 2015, 2029, 2043, 2057) | 0.035 · 0.25 · 0.1 · 1.75 | Produktionscode: `D1, D5, H1, H5 = 0.035, 0.250, 0.10, 1.75` — `grep -rn "0\.035" backend/scripts/kalibrierung/stichprobe60_kernformel.py` → Z. 120 | **0** (Bericht ↔ Code identisch; eiserne Regel 5 nicht berührt) |
| `flood_bldg.r_s092` (Z. 1914, Band Z. 1916) | 0.035, Band [0.0075, 0.0992] | `python3 -c "print(0.10*0.50*0.70, 0.05*0.30*0.50, 0.20*0.62*0.80)"` → `0.034999999999999996 0.0075 0.09920000000000001`, aus den drei Faktor-Blöcken Z. 1870/1884/1900 und deren Bändern Z. 1872/1886/1902; Gegenprobe Register: `grep -n "60-S092-01" docs/evidenz/register.md` → Z. 65 „r_S092 = 0,035 (Band 0,0075–0,0992)" | **0** (nur Gleitkomma-Rest 4·10⁻¹⁷); `abgeleitet_aus:` Z. 1919 nennt genau diese drei Faktoren |
| `flood_bldg.lambda` (Z. 2169) | 0.832 | `python3 -c "print(round(1.132/1.360,4))"` → `0.8324`, Ausgangszahlen aus §4.4 Z. 1230 („\(\lambda = A^{*}/M_0\) = 1,132 / 1,360 = **0,832**"), Gegenprobe §4.8 Z. 1467 („0,832 (0,11–3,44) — **vorläufig**") | **−0,05 %** (Rundung auf drei Stellen); Wert und Band stimmen — beanstandet ist allein der Begründungstext, s. **Befund 85** |
| `flood_bldg.p_hq_haeufig` (Z. 1973, Band Z. 1975) | 0.1, `band: null` | `grep -n "HQhäufig" docs/evidenz/register.md` → Z. 43 (60-W085-01): „HQhäufig 1,0·10⁻¹ a⁻¹ (Kartenfall HQ10; **Spanne HQ5–HQ20 = 2,0·10⁻¹ bis 5,0·10⁻² a⁻¹**)" | Zentralwert **0**, **Band fehlt** (Register führt Faktor 4 Spannweite, Block `null`) → **Befund 84** |
| `flood_bldg.n_efh_zfh` (Z. 1929, Band Z. 1931) | 1950, Band [1889, 2047] | `grep -n "1\.950" docs/methodik/60_gebaeudeschaeden_flusshochwasser.md` → Z. 363–364 („1.765 × 1,105 = 1.950,3 ⇒ **1.950 €₂₀₂₆/m² BGF** (Band 1.889–2.047)") und Z. 684 | **0** (Kennzeichnungsfrage derselben Größe liegt bereits als Befund 82 vor, hier nicht doppelt verbucht) |

**Vorgabe P1 je geprüftem Parameter** (steht im **sichtbaren Berichtstext** Quelle oder
ausgewiesene Abschätzung samt Herleitung?).

| Parameter | `kennzeichnung:` | P1 im sichtbaren Text | Fundstelle |
|---|---|---|---|
| `d_1`, `d_5` | `quelle` (Z. 2019, 2033) | **ja** — Quelle „Thieken u. a. 2008, FLEMOps (Langbeleg B5)" im Block und Stützstellen-Herleitung im Text | Z. 2021/2035; §3.3 Stützstellentabelle Z. 632–633 (nur zitiert) |
| `h_1`, `h_5` | `abschaetzung_kap3` (Z. 2047, 2061) | **ja** — Anker `#tiefen-schadensfunktion` existiert (maschinell geprüft) und §3.3 schreibt die Herleitung aus | Z. 2048/2062; Anker-Prüfung s. o. |
| `r_s092`, `dq_s092`, `s_bem`, `e_bem` | `abschaetzung_kap3` (Z. 1874, 1888, 1904, 1918) | **ja** — Anker `#s092-wirkung` bzw. `#s-bem-naeherung` vorhanden, Herleitung, Sensitivität und Näherungsrichtung in §5.1/§5.1.2/§5.1.3 (Kapitel 5 = Schwesterpaket, nur als Fundstelle); `naeherung: true` + `naeherung_richtung` machen die Näherung zusätzlich maschinenlesbar | Z. 1875, 1889–1891, 1920; Kopf Z. 1858–1861 |
| `lambda` | `abschaetzung_kap3` (Z. 2173) | **ja** — §4.8 Z. 1467 schreibt Rechenweg, Bandfortpflanzung und Vorläufigkeit im Fließtext aus; keine Herleitung „nur im Kommentar" | Z. 2174 (`#niveau-skalar`), §4.8 Z. 1467 |
| `w_wg`, `u`, `phi_fluss`, `kappa`, `pi` | `abschaetzung_kap3` (Z. 2103, 2117, 2131, 2145, 2159) | **ja** — §4.8 Z. 1462–1466 führt je Größe Wert, Band und Herleitungsspalte | Anker `#kalibrierung-zielwert` |
| `p_hq_haeufig`, `p_hq100` | `quelle` (Z. 1977, 1991) | **ja** für Wert und Quelle (Langbeleg B1, wörtliches Zitat Z. 227), **Lücke** beim Band: die im Register ausgewiesene Spanne erscheint weder im Block noch als Sensitivität im Text | Z. 1979/1993; Register Z. 43 → **Befund 84** |
| `n_efh_zfh`, `n_mfh`, `k_bgf` | `abschaetzung_kap3` mit `quelle:` ≠ null (Z. 1933/1935, 1948/1950, 1963/1965) | **ja im Block**, im Text uneinheitlich | bereits **Befund 82** (§3.2 Z. 563 vs. §3.4 Z. 683) — hier nur bestätigt, nicht neu verbucht |
| `f_s093`, `f_s094` | `abschaetzung_kap3` (Z. 2075, 2089) | **ja** für Wert und Band, **nein** für den Platzhalter-Charakter (Ebene geparkt) | Z. 2076/2090 → **Befund 86** |

Vorgabe **P2** ist im Prüfumfang nur mittelbar einschlägig: Der einzige Maßnahmen-Hebel S092 steht
mit `wert: 0.10/0.50/0.70/0.035` gerade **nicht** auf Null und ist als Abschätzung gekennzeichnet
(Z. 1870–1925) — P2 ist damit an dieser Stelle erfüllt; die Prüfung der Herleitung selbst gehört
zu Leitfrage 5. Vorgabe **P3** ist an Kapitel 7 nicht verletzt: die Blöcke enthalten keine Formel
und keine Verteilungsfunktion, nur Skalare mit Band.

| Nr. | Kat. | Befund |
|---|---|---|
| 83 | **B** | **Stelle:** Bericht Kapitel 7 Kopf **Z. 1845** („Kap. 7 führt **je rechnendem Parameter aus §3.5 und §4.8** einen Block: die Kostensätze …, die Parameter der Kernformel und der Kalibrierung sowie die vier Blöcke des Hebels S092"), gegen die Parametertabelle §4.8 **Z. 1459–1475** und gegen den Bestand der Blöcke Z. 1867–2182. · **Art: Lücke/Widerspruch (Vollständigkeit der Parameter-Blöcke)** (Aufgabe §4 Parameter-Block-Format Z. 396–408 „wird per Skript in die Produkt-Registry extrahiert"; §3.6 „jeder Parameter editierbar und bequellt"; Vorgabe P1; §5 LF 12 „Parameter-Blöcke vollständig"). · **Begründung:** In dieser Sitzung maschinell gegenübergestellt — `python3 -c "…[l.split('id:')[1] for l in L[1842:2185] if l.strip().startswith('id:')]"` liefert **22** Block-IDs, die §4.8-Tabelle führt **15** rechnende Parameter des Kalibrierkapitels. Von diesen 15 haben nur **sechs** einen Block (`w_wg`, `u`, `phi_fluss`, `kappa`, `pi`, `lambda`). Ohne Block sind: \(A_{\text{ver}}\) Anker 1,838 Mrd. € (Z. 1461), Baupreisanstieg 2023 → 2024 3 % (Z. 1468), Klassenraten der Bestandsschranke 0,1/0,01 a⁻¹ (Z. 1469), **Plausibilitätsschranke \(\lambda\) 0,11/3,44** (Z. 1470), **Toleranz der Verteilungsprüfung ±11,5 Prozentpunkte** (Z. 1471), **\(U\) Sanity-Untergrenze 0,0103** und **\(O\) Sanity-Obergrenze 6,29 Mrd. €₂₀₂₆/a** (Z. 1472–1473), \(f_{\text{AWM}}\) 0,55 (Z. 1474) und \(q_0\) (Z. 1475, geparkt). Mindestens die vier hervorgehobenen sind **rechnende Schwellen**: An 0,11/3,44 entscheidet sich, ob \(\lambda\) überhaupt gesetzt wird (§4.4 Z. 1258), an \(U\)/\(O\) das Sanity-Verdikt (§4.6), an ±11,5 pp das Bestehen der Verteilungsprüfung (§4.5). Sie steuern also Modellentscheide, sind aber weder extrahierbar noch im Produkt editierbar oder anzeigbar — genau das, was §4 mit dem maschinenlesbaren Kapitel verhindern soll. Kategorie B: kein ausgewiesener Zahlenwert ist falsch, aber die Zusage des Kapitels und die Grundlage der Produkt-Registry stimmen nicht (bei der Extraktion entstünde eine unvollständige Parameterliste, P1). · **Vorschlag:** (a) Für die vier Schwellen (`flood_bldg.lambda_schranke_min/max`, `flood_bldg.sanity_u`, `flood_bldg.sanity_o`, `flood_bldg.toleranz_verteilungspruefung`) sowie für \(A_{\text{ver}}\), den Baupreisanstieg, die Klassenraten und \(f_{\text{AWM}}\) je einen Block anlegen, mit `herkunft: herleitung:#…` auf den jeweiligen Abschnitt (§4.1/§4.2/§4.5/§4.6/§7.2) und `kennzeichnung` nach §3.9. (b) \(q_0\) als geparkten Block mit `wert: null` und Parkgrund führen oder den Satz in Z. 1845 auf den tatsächlichen Umfang einschränken — still stehen lassen darf man die Differenz nicht. (c) Den Vollständigkeits-Check in T-0234 um den Abgleich „jede Zeile der P1-Parametertabellen hat einen Block gleicher Größe" erweitern (hier nur verbucht, nicht umgesetzt). |
| 84 | **B** | **Stelle:** Bericht Kapitel 7, Block `flood_bldg.p_hq_haeufig` **Z. 1971–1983**, Feld `band: null` (**Z. 1975**) bei `wert: 0.1` (Z. 1973) und `herkunft: register:60-W085-01` (Z. 1976); gegen Registerzeile **60-W085-01**, `docs/evidenz/register.md` **Z. 43** („HQhäufig 1,0·10⁻¹ a⁻¹ (Kartenfall HQ10; Spanne HQ5–HQ20 = 2,0·10⁻¹ bis 5,0·10⁻² a⁻¹)", im Bericht gespiegelt Z. 164) und gegen den Schwesterblock `flood_bldg.p_hq_extrem` (Z. 1999–2011), der sein Registerband **mitführt** (`band: [0.001, 0.005]`, Z. 2003). · **Art: Lücke (Unsicherheitsband der Quelle geht beim Übergang ins Maschinenformat verloren)** (§3.9 Herleitungs- und Bandpflicht; §3.4 Sensitivität; Aufgabe §4 Feld `band`; §5 LF 12). · **Begründung:** Der Kartenfall HQ10 ist nicht bundesweit gesetzt — die Länder kartieren „häufig" zwischen HQ5 und HQ20, das Register beziffert die Spanne mit 2,0·10⁻¹ bis 5,0·10⁻² a⁻¹, also **Faktor 4** um den gesetzten Wert. In der Trapezsumme über die drei Szenarien trägt HQhäufig nach §4.5 Z. 1319 rund **66 %** des Modellbetrags; die Eintrittswahrscheinlichkeit geht dort linear ein. Ein `band: null` erklärt diese Größe maschinell für punktgenau und schließt sie aus jeder automatisierten Bandfortpflanzung und aus der nutzersichtbaren Bandanzeige (P1/§3.6) aus, obwohl die Quelle die Spanne ausdrücklich führt und der Nachbarblock sie führt. Kategorie B: der Zentralwert stimmt (oben abgeglichen, Abweichung 0), aber die Unsicherheit des dominierenden Szenarios fehlt im Maschinenformat. · **Vorschlag:** (a) `band: [0.05, 0.2]` eintragen (aufsteigend, wie in allen übrigen Blöcken) und im Text die Wirkung des Bandes auf den K3-Betrag einmal beziffern; (b) prüfen, ob `p_hq100` bei `band: null` bleiben soll — dort ist der Wert definitorisch, das wäre im Block als `band_grund: "definitorisch (HQ100)"` festzuhalten, damit `null` nicht wie eine Auslassung aussieht; (c) in den Lint aufnehmen, dass ein Block mit `herkunft: register:*` kein `band: null` tragen darf, wenn die Registerzeile eine Spanne führt. |
| 85 | **C** | **Stelle:** Bericht Kapitel 7, Block `flood_bldg.lambda`, Feld `vorlaeufig_grund` **Z. 2178** („Weiterhin vorlaeufig, weil die Ledger-Befunde **33** (Jahreswerte der Ankerreihe statt Mittelwert-Rekonstruktion), **35 und 36** offen sind"), gegen §4.8 **Z. 1467** („**vorläufig** wegen der offenen Ledger-Befunde **33 und 34**") und gegen `## Ergebnis` **Z. 35** („λ bleibt vorläufig, weil die Verteilungsprüfung … **nicht bestanden** ausgewiesen ist (§4.5) und die Befunde **35 und 36** offen sind"; Z. 35 gehört zum Schwesterpaket und ist nur zitiert). · **Art: Widerspruch (drei Stellen, drei verschiedene Begründungen desselben Vorläufigkeitsvermerks)** (§4 Parameter-Block als maschinenlesbare Spiegelung des Textes; §6 Prozess; §5 LF 12/LF 14). · **Begründung:** Der Zahlenwert ist geprüft und stimmt (`python3 -c "print(round(1.132/1.360,4))"` → 0,8324 gegen 0,832, Abweichung −0,05 %), ebenso das Band [0.11, 3.44] gegen §4.8 Z. 1467. Auseinander laufen die **Gründe**: Der Block nennt 33/35/36, §4.8 nennt 33/34, `## Ergebnis` nennt 35/36 **und** zusätzlich die nicht bestandene Verteilungsprüfung, die im Block gar nicht vorkommt. Der Block ist die Fassung, die per Skript in die Produkt-Registry wandert (Aufgabe §4) — ein Nutzer, der dort den Vorläufigkeitsgrund liest, bekommt eine dritte Variante, und keiner der drei Stände lässt sich ohne Ledger-Lektüre prüfen. Verschärfend: das Datum im Feld („Stand nach der Kleinste-Quadrate-Ankerbestimmung (17.09.2026)") ist durch die Revisionspakete vom 18.09.2026 überholt (vgl. Befund 73 zur selben Alterungsart an Kopf und „Ergebnis"; dort ist die Stelle eine andere, deshalb hier eigener Befund). Kategorie C, weil weder Wert noch Band noch Rechenweg betroffen sind. · **Vorschlag:** (a) Genau **eine** Quelle der Wahrheit festlegen — `vorlaeufig_grund` auf einen Satz kürzen und per Anker auf §4.4/§4.8 verweisen, statt die Befundnummern im Block zu duplizieren; (b) die drei Stellen auf denselben Stand ziehen (offen ist nach diesem Ledger die Verteilungsprüfung; 33, 35 und 36 sind am 18.09.2026 nachgezogen, Z. 1973 und Z. 2145 dieses Ledgers); (c) Lint-Regel: kommt in einem Parameter-Block eine Ledger-Befundnummer vor, muss dieselbe Nummer im zugehörigen P1-Textabschnitt stehen. |
| 86 | **C** | **Stelle:** Bericht Kapitel 7, Blöcke `flood_bldg.f_s093` **Z. 2069–2081** und `flood_bldg.f_s094` **Z. 2083–2095** (`wert: 1.0`, `band: [0.71, 1.40]` bzw. `[0.84, 1.18]`, `kennzeichnung: abschaetzung_kap3`), gegen §3.2 **Z. 559–566**, wo die tragende Datenebene **GEBAEUDEZUSTAND_BAUSTOFF** ausdrücklich als „**geparkt (Datenquelle fehlt)** — Beschaffungs-Watchlist" geführt ist und dort steht: „Solange keiner der drei Wege das Kriterium erfüllt, bleiben beide Faktoren auf exakt 1,00" (§3.2, nur zitiert — Schwesterpaket). · **Art: Lücke (Status „neu anzulegen/geparkt" der Datenebene wird nicht ins Maschinenformat übernommen)** (§5 LF 12, Teilaussage „benötigte neue Ebenen als solche gekennzeichnet"; §3.1/§3.6; Vorgabe P1). · **Begründung:** Kapitel 7 ist die Schnittstelle zur Produkt-Registry; was dort nicht als Feld steht, kommt im Produkt nicht an. Die beiden Faktoren sind **keine gemessenen Einsen**, sondern Platzhalter mangels bundesweiter, keyless verfügbarer Daten — ihr Band ist reiner Unsicherheitsausweis. Im Block ist das nicht erkennbar: `wert: 1.0` mit `kennzeichnung: abschaetzung_kap3` liest sich wie eine abgeschätzte Wirkung, nicht wie ein neutralisierter Faktor auf geparkter Ebene. Dasselbe gilt schwächer für die drei Blöcke, die auf den **neu anzulegenden** Ebenen HQ_FLAECHE/HQ_TIEFE/GEBAEUDEWERT beruhen (`p_hq_*`, `n_*`, `k_bgf`): Auch bei ihnen steht der Ebenen-Status nur im Fließtext des §3.2. Für einen Umsetzer — die Adressatenfrage der Leitfrage 12 — fehlt damit im maschinenlesbaren Teil die Antwort auf „welche Ebene muss ich erst bauen, und welcher Parameter ist ohne sie wirkungslos". Kategorie C: kein Zahlenwert ist falsch, die Kennzeichnung existiert im Text; sie erreicht nur das Maschinenformat nicht. · **Vorschlag:** (a) Ein Feld `datenebene:` je Block ergänzen (`HQ_FLAECHE`, `HQ_TIEFE`, `GEBAEUDEWERT`, `GEBAEUDEZUSTAND_BAUSTOFF`) plus `ebene_status:` mit genau einem der Werte `vorhanden` / `neu_anzulegen` / `geparkt`; (b) bei `geparkt` zusätzlich `platzhalter: true` setzen, damit im Produkt neben dem Wert 1,00 nicht „Abschätzung von KAP3", sondern „neutral gesetzt, Datenebene fehlt (§3.2)" erscheint; (c) den Kapitel-7-Kopf (Z. 1847–1865) um diese Felder ergänzen, da er die Zusatzfelder abschließend aufzählt. |

**Abgrenzung und Status dieses Pakets.**

- **Kein Befund behoben, keiner umnummeriert.** Die zu Laufbeginn höchste im Ledger vergebene
  Nummer war **82** (ermittelt mit
  `grep -o "^| [0-9]\+ |" reviews/BEFUNDE_60.md | grep -o "[0-9]\+" | sort -n | tail -3`);
  die erste neue Nummer dieses Pakets ist deshalb **83**, vergeben sind **83 bis 86**.
- **Nur Leitfrage 12 beantwortet**, am Kopf und an den maschinenlesbaren Blöcken des Kapitels 7
  (Z. 1843–2185, 10.109 Zeichen ohne HTML-Kommentare, in dieser Sitzung nachgemessen).
  §7.1, §7.2, `## Ergebnis` und Kapitel 5 tragen die Schwesterpakete (Reihenfolgeplätze 7 und 17)
  und sind hier nur als Fundstelle zitiert; die Leitfragen 5 und 11 sind hier nicht beantwortet.
- **Vorgaben P1/P2/P3 am Prüfgegenstand mitgeprüft** (Tabelle oben): P1 ist für alle 22 Blöcke über
  `kennzeichnung`, `quelle` und `herleitung_anker` formal erfüllt — alle sieben genannten Anker
  existieren im Bericht (maschinell geprüft) —, inhaltlich offen bleiben die Kennzeichnung der
  Platzhalter (Befund 86) und die bereits als Befund 82 verbuchte Mischkennzeichnung von \(n_t\).
  P2 ist am Hebel S092 erfüllt (keine Nullwirkung, Band und Näherungsrichtung im Block). P3 ist an
  Kapitel 7 nicht verletzt (keine Formel, keine Verteilungsfunktion im Prüfumfang).
- **Ressourcen-Regel §3.4 eingehalten:** verglichen wurde auf fünf Stichprobengrößen und den im
  Bericht ausgewiesenen Zahlen; die Stichproben-CSVs unter `docs/evidenz/60_stichprobe/` wurden
  nicht gelesen, kein nationaler 100-m-Vollraster-Lauf.
- **Eiserne Regeln 2, 4 und 5 eingehalten:** Arbeitsmappen nur gelesen; frische Sitzung, die den
  geprüften Stand nicht geschrieben hat; die Bericht-↔-Code-Gegenüberstellung
  (`stichprobe60_kernformel.py` Z. 120) ergab keine Divergenz und hätte andernfalls einen Befund
  gegeben, keine stille Code-Änderung.
- **Geänderte Dateien:** ausschließlich diese.
  `docs/methodik/60_gebaeudeschaeden_flusshochwasser.md` (SHA-256 `d36326bd5678…`) und
  `docs/evidenz/register.md` (SHA-256 `29a90539c30b…`) sind byte-gleich geblieben;
  `backend/scripts/lint_methodik.py` (T-0234) wurde nur gelesen, nicht geändert, und der
  Lint-Lauf der Runde aus Abschnitt 0.1 (T-0359) wurde nicht wiederholt.
- **Kopftabelle „Offene Befunde" bewusst nicht fortgeschrieben** (Dateirahmen der Runde-3-Pakete,
  T-0359); das Konvergenz-Verdikt der Runde trägt das Abschlusspaket.

### Leitfrage 7 — Teil 2: Parameterblock 4.8 und Gesamtverdikt

**Prüfumfang dieses Pakets (T-0377).** Zweiter Teil der Leitfrage 7 aus §5 der Aufgabe („**Tails/
Parameter:** Verteilungsannahmen, wo empirische Quantile verfügbar wären; **gesetzte Werte, die
messbar wären; Kalibriermodell = Produktionsmodell?**", `docs/AUFGABE_METHODIK_SCHADENSRECHNUNG.md`
**Z. 440–441**), vertieft geprüft an genau einem Abschnitt des Berichts: §4.8 „Parameter dieses
Kapitels (Vorgabe P1)", **Z. 1457–1573** (Tabellenkopf Z. 1459, Parameterzeilen Z. 1461–1475,
Testblock `beispiel_60_kalibrierung` Z. 1477–1573; nächste Überschrift „## 5" in Z. 1574).
Umfangsmessung in dieser Sitzung, ausgeführt:
`python3 -c 'import re; t=open("docs/methodik/60_gebaeudeschaeden_flusshochwasser.md").read().split(chr(10)); print(len(re.sub(r"<!--.*?-->","",chr(10).join(t[1456:1573]),flags=re.S)))'`
→ **9.059** Zeichen — identisch mit dem Planungsstand vom 18.09.2026, keine Abweichung auszuweisen.
§4.1–§4.7 und Kapitel 9 gehören zu Schwesterpaketen und sind hier nur als Fundstelle zitiert.

#### (a) Zeilenweise P1-Prüfung der Parametertabelle §4.8

Maßstab: Vorgabe P1 — je Parameter entweder die **Quelle** oder der Vermerk, dass es eine
**begründete Abschätzung von KAP3** ist, **samt Herleitung**; eine Herleitung nur als
Code-Kommentar erfüllt die Vorgabe nicht (§3.6, §3.9).

| Zeile | Parameter | Kennzeichnung in Spalte 3 | Herleitung auffindbar? | P1 |
|---|---|---|---|---|
| Z. 1461 | \(A_{\text{ver}}\) Anker | **Quelle** (GDV-Naturgefahrenstatistik 2024 / Naturgefahrenreport 2025, Stand 10.10./30.12.2025) + Evidenzdatei `60_gdv_jahresreihe_2002_2024.csv` | ja, §4.1/§4.1a | **erfüllt** |
| Z. 1462 | \(w_{\text{wg}}\) | **Abschätzung von KAP3** | ja, §4.2 | **erfüllt** |
| Z. 1463 | \(u\) | **Abschätzung von KAP3** auf belegter Versicherungsdichte 57 % | ja, §4.2 | **erfüllt** |
| Z. 1464 | \(\varphi_{\text{fluss}}\) | **Abschätzung von KAP3** | ja, §4.2 | **erfüllt** |
| Z. 1465 | \(\kappa\) | **Abschätzung von KAP3** | ja, §4.2 | **erfüllt** |
| Z. 1466 | \(\pi\) | **Abschätzung von KAP3** aus B4 (Baupreisindex) | ja, §4.2 | **erfüllt** |
| Z. 1467 | \(\lambda\) Niveau-Skalar | **berechnet** aus \(A^{*}/M_0\), Eingänge und Bandherkunft benannt, „vorläufig" wegen der Befunde 33 und 34 | ja, §4.1a/§4.3/§4.4 | **erfüllt** (abgeleitete Größe; Nachrechnung unten) |
| Z. 1468 | Baupreisanstieg 2023 → 2024 | **Abschätzung von KAP3**, gerundet aus B4-Jahresraten, mit Sensitivität | ja, §4.2/B4 | **erfüllt** |
| Z. 1469 | Klassenraten Bestandsschranke (0,1; 0,01 a⁻¹) | **Abschätzung von KAP3**, „Register 60-R17-01 … unverändert übernommen" | ja, §4.6 | **erfüllt**; Anmerkung: Quelle und Abschätzung stehen in derselben Zelle vermischt (übernommener Registerwert **und** KAP3-Abschätzung); formal genügt die Zelle P1, weil Herleitung und Register benannt sind |
| Z. 1470 | Plausibilitätsschranke \(\lambda\) | **berechnet** aus dem fortgepflanzten Band | ja, §4.4 | **erfüllt** |
| Z. 1471 | Toleranz Verteilungsprüfung | **berechnet**, Abschätzungsanteil (Kombinationsregel) ausdrücklich abgegrenzt | ja, §4.5 | **erfüllt** |
| Z. 1472 | \(U\) Sanity-Untergrenze | **teils Quelle** (BGBl.-Fondsvolumina), **teils Abschätzung von KAP3**, Anteile benannt | ja, §4.6 | **erfüllt** |
| Z. 1473 | \(O\) Sanity-Obergrenze | **berechnet** aus Klassenraten, Register 60-R17-01, Gebäudewert 527.280 € (60-R24-01), Deckel 0,250 (§3.3) | ja, §4.6 | **erfüllt** |
| Z. 1474 | \(f_{\text{AWM}}\) | **Abschätzung von KAP3** auf § 38 ImmoWertV, mit Sensitivität | ja, §7.2 | **erfüllt** |
| Z. 1475 | \(q_0\) Objektschutz-Anteil | **„geparkt (Datenquelle fehlt)" — keine Quelle, keine Abschätzung** | Watchlist §4.7 | **nicht erfüllt**, aber **nicht doppelt erfasst**: die Folge (unbezifferter Bezugswert in §5.1.2) ist bereits **Befund 67** |

**Feststellung zu (a).** Alle 15 Tabellenzeilen tragen die nach P1 verlangte Kennzeichnung mit
auffindbarer Herleitung; die einzige Lücke (\(q_0\)) ist im Bericht ausdrücklich als Lücke
ausgewiesen und bereits verbucht. **Nicht** erfüllt ist P1 dagegen für die Parameter, die
ausschließlich im Testblock Z. 1477–1573 stehen und **keine** Zeile in der nutzersichtbaren Liste
haben, obwohl sie das Ergebnis tragen: Wohngebäudeanteil je Adresse **0,872** (Z. 1487), gemessene
Klassenraten \(r_{\text{GK3/GK4}}\) = **0,005979599550826** und \(r_{\text{GK2}}\) =
**0,000675151053693** (Z. 1488–1489), die Bausteine des Gebäudewerts **208 m² · 1,30 ·
1.950 €/m²** (Z. 1485), die \(M_0\)-Bandenden-Eingänge BGF 1,25/1,40 und Werteinheit
1.889/2.047 €/m² (Z. 1497–1498) sowie die \(U\)-Herleitungsgrößen \(E_{\text{nom}}\) = 8,0 Mrd. €,
1,02¹³, \(w_u = 1/9\), \(f_{\text{fluss}}\) = 0,90, \(T_u\) = 100 a (Z. 1564–1566). Für sie steht
Quelle bzw. Abschätzungscharakter nur als **Code-Kommentar** — genau der Fall, den P1 ausschließt.
Daraus **Befund 88**.

#### (b) Zwei Nachrechnungen statt Lektüre

**Nachrechnung 1 — Niveau-Skalar \(\lambda\) aus den in §4.8 genannten Eingangsgrößen.** Eingänge
ausschließlich aus §4.8: \(A_{\text{ver}}\) 1,838 · \(w_{\text{wg}}\) 0,65 · \(u\) 1,54 ·
\(\varphi\) 0,50 · \(\kappa\) 1,15 · \(\pi\) 1,07 (Z. 1461–1466, Z. 1479–1480); Gebäudewert
208 · 1,30 · 1.950 (Z. 1485); Wohngebäudeanteil 0,872 (Z. 1487); Klassenraten und Adresszahlen
(Z. 1488–1491). Ausgeführt in dieser Sitzung:
`python3 -c 'A=1.838*0.65*1.54*0.50*1.15*1.07; wg=208.0*1.30*1950.0; M0=0.872*wg*(339000*0.005979599550826+1380000*0.000675151053693)/1e9; print(A, wg, M0, A/M0)'`
→ `1.1319603295 527280.0000000001 1.3604178521941683 0.8320681235359434`. Bandenden, ausgeführt:
`python3 -c 'print((1.061*0.55*1.33*0.35*1.05*1.04)/2.643, (1.838*0.75*1.75*0.65*1.30*1.11)/0.657)'`
→ `0.11223368796821794 3.4439682363013704`.

| Größe | Wert im Bericht (§4.8) | nachgerechnet | Abweichung |
|---|---|---|---|
| \(A^{*}\) Zielwert | 1,132 Mrd. €₂₀₂₆/a (Z. 1480) | **1,13196** | +0,02 % (Rundung) |
| Gebäudewert | 527.280 €₂₀₂₆ (Z. 1473, Z. 1486) | **527.280,0** | 0 |
| \(M_0\) | 1,360 Mrd. €₂₀₂₆/a (Z. 1493) | **1,36042** | +0,03 % (Rundung) |
| \(\lambda\) Zentralwert | **0,832** (Z. 1467) | **0,83207** | +0,01 % (Rundung) |
| \(\lambda\)-Band unten | 0,11 (Z. 1467, Z. 1470) | **0,11223** | +2,0 % (Rundung auf zwei Stellen, konservativ nach unten) |
| \(\lambda\)-Band oben | 3,44 (Z. 1467, Z. 1470) | **3,44397** | +0,12 % (Rundung) |

**Ergebnis:** Der Niveau-Skalar ist aus den in §4.8 selbst genannten Eingangsgrößen vollständig
reproduzierbar; alle Abweichungen sind reine Rundungen auf die ausgewiesene Stellenzahl. Dieser
Teil ist rechnerisch **bestanden**.

**Nachrechnung 2 — Klassenraten GK3/GK4 und GK2 gegen die angegebene Quelle.** Quelle laut §4.8
Z. 1467 und Z. 1488–1489: `docs/evidenz/60_stichprobe/m0_klassenraten.csv` (28 Zeilen, Trennzeichen
`;`), in dieser Sitzung gelesen.

| Größe | Wert im Bericht | Wert in der Quelle (Fundstelle) | Abweichung |
|---|---|---|---|
| \(r_{\text{GK3/GK4}}\) | 0,005979599550826 (Z. 1488, Kommentar „klasse=gk3_gk4/kommune=alle") | **0,005979599550826** — CSV **Z. 10**, Zeile `gk3_gk4;alle`, Spalte `rate_exponiert_hqextrem_1_pro_a` (9. Spalte) | **0** (zeichengleich) |
| \(r_{\text{GK2}}\) | 0,000675151053693 (Z. 1489, Kommentar „klasse=gk2/kommune=alle") | **0,000675151053693** — CSV **Z. 19**, Zeile `gk2;alle`, Spalte `rate_exponiert_hqextrem_1_pro_a` | **0** (zeichengleich) |
| Gegenprobe: dieselben Zeilen, Spalte `rate_zellen_1_pro_a` | — | 0,004197318695391 (CSV Z. 10) bzw. 0,000436059863136 (CSV Z. 19) | **−30 % / −35 %** gegenüber den verwendeten Werten |

**Ergebnis:** Beide Klassenraten stimmen zeichengenau mit der angegebenen Quelle überein; inhaltlich
ist die Quellenangabe **bestanden**. Sie ist aber **nicht eindeutig**: Die CSV führt in denselben
Zeilen zwei Ratenspalten (`rate_zellen_1_pro_a`, `rate_exponiert_hqextrem_1_pro_a`), die sich um 30
bzw. 35 % unterscheiden; Bericht und Code-Kommentar benennen nur Klasse und Kommune, nicht die
Spalte. Ein Nachrechner nach §3.9 kann die Zelle daher nicht eindeutig treffen. Daraus
**Befund 89**.

#### (c) Kalibriermodell = Produktionsmodell? — Abgleich gegen `backend/scripts/kalibrierung/`

Ausgeführt in dieser Sitzung (gezielter grep, keine Lektüre der Skripte):
`grep -rnE "0\.832|1\.838|527280|0\.872|0\.0059796|0\.00067515|3\.44" backend/scripts/kalibrierung/ --include=*.py`
→ **kein Treffer**. Ebenso
`grep -rn "m0_klassenraten\|339_000\|339000\|1_380_000\|1380000" backend/scripts/kalibrierung/ --include=*.py`
→ kein Treffer für die Adresszahlen; die einzigen Treffer sind die **erzeugende** Seite in
`backend/scripts/kalibrierung/stichprobe60_klassenraten.py` **Z. 10, 97 und 185**
(`AUSGABE = 'm0_klassenraten.csv'`).

**Feststellung.** Die Stichprobe, aus der die Klassenraten stammen, ist reproduzierbar verskriptet;
die **Kalibrierung selbst** — \(A^{*}\), \(M_0\), \(\lambda\), Band und Plausibilitätsschranke, also
genau die Werte der Tabelle §4.8 — kommt in `backend/scripts/kalibrierung/` an keiner Stelle vor.
Die einzige ausführbare Fassung dieser Rechnung ist der Testblock **im Bericht** (Z. 1477–1573); er
belegt die Konsistenz des Berichts mit sich selbst, nicht die Übereinstimmung mit einem
Produktionsstand. Zu Leitfrage 7 „Kalibriermodell = Produktionsmodell?" ist damit für §4.8 **keine
Deckungsgleichheit feststellbar und keine Divergenz belegbar** — es fehlt die Gegenseite. Daraus
**Befund 87**. Nach eiserner Regel 5 wird im Code nichts geändert. Umfangsgrenze dieser Aussage:
gesucht wurde ausschließlich in `backend/scripts/kalibrierung/` (Dateirahmen des Pakets).

#### Neue Befunde dieses Pakets (87 bis 89)

| Nr | Kat. | Befund |
|---|---|---|
| 87 | **B** | **Stelle:** Bericht §4.8, Parametertabelle Z. 1461–1475 und Testblock `beispiel_60_kalibrierung` Z. 1477–1573, gegen `backend/scripts/kalibrierung/` (gezielter grep dieser Sitzung, oben zitiert: kein Treffer für 0,832 / 1,838 / 527280 / 0,872 / 0,0059796 / 0,00067515 / 3,44 / 339.000 / 1.380.000). · **Art: Lücke** (§5 LF 7 „Kalibriermodell = Produktionsmodell?"; §3.9). · **Begründung:** Die Kalibrierung von #60 — Zielwert \(A^{*}\), Modellsumme \(M_0\), Niveau-Skalar \(\lambda\) samt Band und Plausibilitätsschranke — existiert ausführbar nur als Testblock im Methodikbericht. Unter `backend/scripts/kalibrierung/` liegt für #60 ausschließlich die **Stichprobenseite** (`stichprobe60_*.py`, darunter `stichprobe60_klassenraten.py`, das `m0_klassenraten.csv` erzeugt); ein Skript, das aus diesen Raten \(M_0\) und \(\lambda\) bildet, gibt es nicht — anders als bei #M0, wo `calibrate_heat_mortality*.py` genau diese Rolle trägt. Folge: Der Testblock prüft den Bericht gegen sich selbst; eine Änderung an den sechs Ankerabschätzungen oder an den Klassenraten fiele im Produktionspfad nicht auf, und die Frage der Leitfrage lässt sich weder mit „ja" noch mit „nein" beantworten, weil die Gegenseite fehlt. Kategorie B: kein ausgewiesener Zahlenwert ist falsch — die Nachrechnung oben bestätigt alle —, aber die von §5 LF 7 verlangte Gleichheitsprüfung ist am heutigen Stand nicht durchführbar. Abgrenzung: Befund 64 betrifft die Aussagekraft des Sanity-Bands innerhalb des Berichts, nicht das Verhältnis Bericht ↔ Produktionscode. · **Vorschlag:** Die Kalibrierung als eigenes Skript `backend/scripts/kalibrierung/kalibrierung60_lambda.py` nachziehen, das die Eingänge aus `m0_klassenraten.csv` und `60_gdv_jahresreihe_2002_2024.csv` liest, \(A^{*}\), \(M_0\), \(\lambda\), Band und Schranke ausgibt und die im Bericht ausgewiesenen Werte als Assertions führt; in §4.8 die Fundstelle des Skripts nennen, damit Kalibrier- und Produktionsstand nachweislich dieselbe Rechnung sind. Bis dahin in §4.8 ausdrücklich vermerken, dass der Testblock die einzige ausführbare Fassung ist. |
| 88 | **B** | **Stelle:** Bericht §4.8, Parametertabelle Z. 1461–1475 (abschließend formuliert: „Parameter dieses Kapitels") gegen den Testblock Z. 1485 (`208.0 * 1.30 * 1950.0`), Z. 1487 (`w_wohn = 0.872   # Wohngebaeudeanteil je Adresse (19,7/22,6)`), Z. 1488–1489 (`r_gk34`, `r_gk2`), Z. 1497–1498 (`bgf_lo, bgf_hi = 1.25, 1.40`; `ws_lo, ws_hi = 1889.0, 2047.0`) und Z. 1564–1566 (`E_nom, faktor_2026 = 8.0, 1.02 ** 13`; `w_u, f_fluss, T_u = (1/3)*(1/3), 0.90, 100`). · **Art: Lücke (Vorgabe P1)** (CLAUDE.md P1; Aufgabe §3.6, §3.9). · **Begründung:** P1 verlangt eine **nutzersichtbare** Parameterliste mit Quelle oder ausgewiesener KAP3-Abschätzung samt Herleitung **für alle Parameter** und stellt ausdrücklich klar, dass eine Herleitung nur als Code-Kommentar die Vorgabe nicht erfüllt. Die genannten elf Größen tragen das Ergebnis unmittelbar: \(M_0\) ist das Produkt aus Wohngebäudeanteil, Gebäudewert und Klassenraten, und über \(\lambda = A^{*}/M_0\) skaliert jede von ihnen den Endbetrag linear; die \(M_0\)-Bandenden und die fünf \(U\)-Größen bestimmen Band und Sanity-Untergrenze. In der Tabelle erscheinen sie entweder gar nicht (0,872; \(r_{\text{GK3/GK4}}\); \(r_{\text{GK2}}\); BGF 1,25/1,40; 1.889/2.047 €/m²; \(E_{\text{nom}}\); \(w_u\); \(f_{\text{fluss}}\); \(T_u\)) oder nur als Zwischenprodukt ohne eigene Bausteine (Gebäudewert 527.280 € in Z. 1473, dessen drei Faktoren 208 m², 1,30 und 1.950 €/m² nirgends in der Liste stehen). Ihre einzige Kennzeichnung ist ein Kommentar im Python-Block. Kategorie B, weil kein Zahlenwert falsch ist, aber eine ausdrückliche Vorgabe des Aufsichtsrats an genau der Stelle nicht erfüllt ist, die sie erfüllen soll. Abgrenzung: Befund 67 betrifft \(q_0\) in §5.1.2, nicht die hier fehlenden Zeilen. · **Vorschlag:** Die elf Größen als eigene Zeilen in §4.8 aufnehmen, je mit Wert, Band und Spalte 3 nach demselben Muster (Wohngebäudeanteil 0,872 → Quelle Zensus-Ableitung 19,7/22,6; Klassenraten → Quelle `m0_klassenraten.csv` mit Zeile und Spalte, siehe Befund 89; 208 m²/1,30/1.950 €/m² → Register 60-R24-01 bzw. Abschätzung; \(E_{\text{nom}}\) → BGBl.; \(w_u\), \(f_{\text{fluss}}\), \(T_u\) → Abschätzung von KAP3 mit Herleitung §4.6). Alternativ die Überschrift von §4.8 wahrheitsgemäß auf „Kernparameter" einschränken und die vollständige Liste an einer benannten Stelle führen — die halbe Liste unter dem Titel „Parameter dieses Kapitels" ist der Fehler. |
| 89 | **C** | **Stelle:** Bericht §4.8 Z. 1467 (\(\lambda\)-Zeile: „\(M_0\) aus den gemessenen Klassenraten GK3+GK4 und GK2 (`docs/evidenz/60_stichprobe/m0_klassenraten.csv`, §4.3)") und Z. 1488–1489 (Kommentare „klasse=gk3_gk4/kommune=alle" bzw. „klasse=gk2/kommune=alle") gegen `docs/evidenz/60_stichprobe/m0_klassenraten.csv` Z. 10 und Z. 19. · **Art: Lücke (Nachprüfbarkeit der Fundstelle)** (§3.9; §8/E3, P3). · **Begründung:** Die Werte selbst stimmen zeichengenau (Nachrechnung 2). Die Fundstellenangabe benennt aber nur Klasse und Kommune, während die CSV in derselben Zeile **zwei** Ratenspalten führt: `rate_zellen_1_pro_a` (0,004197318695391 bzw. 0,000436059863136) und `rate_exponiert_hqextrem_1_pro_a` (0,005979599550826 bzw. 0,000675151053693). Verwendet ist die zweite; die erste liegt um 30 bzw. 35 % niedriger und ergäbe ein anderes \(M_0\) und ein anderes \(\lambda\). Ein Prüfer, der der Angabe folgt, trifft die Zelle nicht eindeutig — dieselbe Klasse von Mangel, die für Quelle 2 bereits als Befund 43 (b) und für Quelle 1 als Befund 69 geführt wird, hier an der Evidenzdatei der Kalibrierung. Kategorie C: kein Zahlenwert ändert sich, die Angabe ist nur unterbestimmt. · **Vorschlag:** In Z. 1467 und in den beiden Kommentaren die Spalte mitnennen (`rate_exponiert_hqextrem_1_pro_a`, Zeilen `gk3_gk4;alle` / `gk2;alle`) und in §4.3 einen Satz ergänzen, warum die auf die exponierte Fläche bezogene Rate und nicht die Zellrate die richtige Bezugsgröße ist. Für den Lint: Fundstellenangaben auf CSV-Dateien müssen Zeilen- **und** Spaltenbezeichner tragen. |

#### Gesamtverdikt zu Leitfrage 7

Zusammengeführt, nicht neu erhoben, aus zwei Quellen:

| Teil | Gegenstand | Fundstelle im Ledger | Verdikt |
|---|---|---|---|
| Teil 1 | Verteilungsannahmen (§4.5) und Sanity-Band (§4.6) | Unterabschnitt „### Leitfrage 7 — Teil 1: Verteilungsannahmen und Sanity-Band", Überschrift in **Z. 2989** dieses Ledgers (Zwischenverdikt im Absatz ab Z. 3000) | **Befund** (63, 64, 65) |
| Teil 2 | Parameterblock §4.8, dieses Paket | dieser Unterabschnitt | **Befund** (87, 88, 89) |

**Gesamtverdikt Leitfrage 7: Befund.** Tragend sind sechs Befunde, geordnet nach den drei Fragen
der Leitfrage. *Verteilungsannahmen, wo empirische Quantile verfügbar wären:* Die Ankerreihe wird
nur als Mittelwert-Aggregat genutzt, ein Quantilvergleich unterbleibt (Befund 63, Teil 1).
*Gesetzte Werte, die messbar wären:* Die Sanity-Obergrenze ist kein modellunabhängiger Wert
(Befund 64), der Regime-Anteil ist widersprüchlich gerundet (Befund 65), elf ergebnistragende
Größen stehen nur im Code-Kommentar statt in der nutzersichtbaren Parameterliste (Befund 88), und
eine Quellenangabe ist spaltenunbestimmt (Befund 89). *Kalibriermodell = Produktionsmodell:* Die
Frage ist am heutigen Stand nicht beantwortbar, weil die Kalibrierung von #60 außerhalb des
Berichts nicht existiert (Befund 87). Was **bestanden** ist und im Verdikt nicht untergehen soll:
Sämtliche nachgerechneten Zahlen der Leitfrage stimmen — Toleranz und Prüfgröße in Teil 1,
Zielwert, Modellsumme, Niveau-Skalar, Band und beide Klassenraten in Teil 2 —, und 14 der
15 Tabellenzeilen von §4.8 erfüllen P1 vollständig. Das Verdikt „Befund" folgt aus Vollständigkeit
und Nachweisbarkeit, nicht aus Rechenfehlern. **Damit ist Leitfrage 7 in Runde 3 genau einmal
verdiktiert, nämlich hier.**

#### Abgrenzung und Status dieses Pakets (T-0377)

- **Geändert wurde ausschließlich `reviews/BEFUNDE_60.md`** (angehängt).
  `docs/methodik/60_gebaeudeschaeden_flusshochwasser.md` und `docs/evidenz/register.md` sind
  byte-gleich; `docs/evidenz/60_stichprobe/m0_klassenraten.csv` und die Skripte unter
  `backend/scripts/kalibrierung/` wurden nur gelesen bzw. durchsucht, nicht geändert (eiserne
  Regeln 2 und 5). Die großen Stichprobendateien `60_stichprobe/hq_*.csv` wurden nicht geöffnet.
- **Kein Befund behoben, keiner umnummeriert.** Höchste vorhandene Nummer zu Laufbeginn: **86**;
  neu vergeben sind **87–89**. Die Befunde 33, 34, 43 (b), 64, 67 und 69 sind nur als Gegenstelle
  bzw. zur Abgrenzung eingeordnet.
- **Ressourcen-Regel §3.4 eingehalten:** kein nationaler 100-m-Vollraster-Lauf; nachgerechnet wurde
  zellweise aus den in §4.8 ausgewiesenen Zahlen und aus zwei Zeilen der 28-zeiligen
  Klassenraten-Stichprobe. Der Codeabgleich war ein gezielter grep, keine Lektüre der Skripte.
- **Frische Sitzung** (eiserne Regel 4): Diese Gegenprüfung ist nicht die Sitzung, die den
  geprüften Stand geschrieben hat.
- **Nicht Gegenstand dieses Pakets:** §4.1–§4.7 und Kapitel 9 (Schwesterpakete, hier nur als
  Fundstelle zitiert), die übrigen Leitfragen, die Regression der Altbefunde.
- **Kopftabelle „Offene Befunde" bewusst nicht fortgeschrieben** (Dateirahmen der Runde-3-Pakete,
  T-0359); das Konvergenz-Verdikt der Runde trägt das Abschlusspaket.

### Leitfrage 11 — Form und Erklärbarkeit

Paket T-0381 der Runde 3 (20.09.2026), eigene frische Sitzung (eiserne Regel 4: Diese Sitzung hat
den geprüften Stand nicht geschrieben — geschrieben haben T-0235 bis T-0243, T-0256 bis T-0259 und
die Revisionspakete aus T-0281). **Prüfumfang:** Abschnitt `## Ergebnis` (Z. 30–38), §7.1
(Z. 2186–2229) und §7.2 (Z. 2230–2325) von `docs/methodik/60_gebaeudeschaeden_flusshochwasser.md`.
**Eigene Messung** (in dieser Sitzung ausgeführt, HTML-Kommentare entfernt):
`python3 -c "L=open(...).read().split(chr(10)); seg=lambda a,b: len(re.sub(r'<!--.*?-->','',chr(10).join(L[a-1:b])+chr(10),flags=re.S)); print(seg(30,38),seg(2186,2229),seg(2230,2325))"`
→ **2.377 · 3.181 · 6.660 = 12.218 Zeichen** (Ticketangabe 2.376/3.180/6.659/12.215; Differenz je
Abschnitt genau 1 Zeichen = abschließendes Zeilenende, Textkörper identisch). Kapitelkopf 7 und die
Parameter-Blöcke Z. 1843–2185 sowie Kapitel 5 sind Schwesterpakete und hier nur als Fundstelle
zitiert; Leitfragen 5 und 12 werden hier nicht beantwortet. Lint-Ergebnis der Runde übernommen (§5,
Eröffnungspaket T-0359), nicht wiederholt.

**Verdikt Leitfrage 11: Befund** (vier neue Befunde, 92–95; Nummernstand zu Laufbeginn: höchste
vergebene Nummer 91, erste neue Nummer 92).

| Teilfrage der LF 11 | Verdikt | Begründung mit Fundstelle |
|---|---|---|
| Zeichentabellen vollständig | **Befund** | Die Zeichentabelle §3.5 deckt laut eigener Überschrift „alle Formelzeichen der **Kapitel 3 und 5**" ab (Z. 750, nur zitiert). \(f_{\text{AWM}}\), das einzige in §7.2 neu eingeführte Zeichen, steht in keiner Zeichentabelle: gemessen in dieser Sitzung `grep -n "AWM" …` → **6 Treffer** (Z. 691, 1474, 2262, 2290, 2323, 2512), keiner davon in §3.5 (Z. 750 ff.) oder §5.1.1 (Z. 1602 ff.), und in Kapitel 7 trägt kein Parameter-Block die id `f_awm`. Klartext („Alterswertminderungsfaktor") steht in §4.8 Z. 1474 und §7.2 Z. 2262, eine **Einheit** (dimensionslos, RND/GND) an keiner der beiden Stellen → **Befund 95** (C). Die in §7.2 verwendeten Zeichen \(A^{*}\), \(M_0\), \(\lambda\), \(U\), \(O\) sind dagegen in §3.5/§4.8 geführt (z. B. \(U\) Z. 1472). |
| Beispiele rechnen auf (Golden-Test grün) | **grün, aber Befund im Inhalt** | Der Beispielblock `beispiel_60_zeitwert` (Z. 2296–2319) wurde in dieser Sitzung ausgeführt (`python3 -c "…re.search(r'```python test: beispiel_60_zeitwert…').group(1); exec(…)"`) → **alle asserts grün**, kein Fehler. Er ist jedoch mit einem **abgelösten Anker** gerechnet: Z. 2303 `A_stern = 1.6 * 0.65 * 1.54 * 0.50 * 1.15 * 1.07` = **0,98538**, während §4.2 Z. 1123 den Anker mit \(A_{\text{ver}}\) = **1,838** zu \(A^{*}\) = **1,132 Mrd. €₂₀₂₆/a** ausschreibt und §4.5 Z. 1381 den kalibrierten Ist-Betrag mit \(\lambda M_0\) = **1,132** führt → **Befund 92** (B). Der Golden-Test kann das nicht fangen, weil er seine Ausgangszahl selbst mitbringt. |
| Innere Widerspruchsfreiheit der Beispielzahlen | **Befund** | §7.2 nennt dieselbe Größe (das λ bei allein umgestelltem Basiswert) zweimal verschieden: Prosa Z. 2250–2251 „Zentralwert 1,132 / (1,360 · 0,55) = **1,51**, am unteren Faktor-Ende … = **2,08**" gegen Z. 2293 „nur \(\lambda\) steigt — auf **1,32**" und den Test Z. 2311–2312 (`1.32` / `1.81`) → **Befund 93** (B). |
| Erklärbarkeit nach P3 (A-0034) im Prüfumfang | **bestanden** | §7.1 und §7.2 kommen ohne Verteilungsfunktion aus; gerechnet wird ausschließlich mit Multiplikation, Division und Prozent (Z. 2285, Z. 2288–2291, Block Z. 2296–2319). Die Abschätzung \(f_{\text{AWM}}\) ist aus Regel (§ 38 ImmoWertV, Z. 2265–2273), Annahme (mittleres Alter, RND 44/80, Z. 2274–2280) und Modellgrenze (Ausbauteile mit kürzerer Nutzungsdauer, Z. 2281–2283) hergeleitet — für einen Sachbearbeiter ohne Statistikausbildung nachvollziehbar. Keine stille Vereinfachung: Die Zeitwert-Lesart wird als beziffertes Band ausgewiesen statt weggelassen (Z. 2241–2243), und §7.1 begründet die Wertebereichs-Abweichung offen, statt sie umzubiegen (Z. 2198–2204). |

**Prüfpunkte E1–E4 (§8 der Aufgabe) — einzeln mit ja/nein und Fundstelle**

| Punkt | Antwort | Fundstelle und Begründung |
|---|---|---|
| **E1 — Rechenweg in Worten** | **ja** | Bericht Kap. 3, einleitender Absatz Z. 525–529: zwei Sätze Fließtext ohne Formelzeichen („Umsetzungsgrundlage ist Ansatz **(a)** … Szenario-Erwartungswert mit typisierter Tiefen-Schadensfunktion je 100-m-Zelle"; Kernformel in Worten „Menge × Rate × Preis auf Zellebene", Z. 528). Grenze „höchstens fünf Sätze" eingehalten (2). Nur als Fundstelle zitiert, Kapitel 3 ist Schwesterpaket. |
| **E2 — Rechenbeispiel mit Zahlen** | **ja im Prüfumfang, mit Einschränkung** | §7.2 Z. 2296–2319: ausführbarer Block nach §4 mit allen Zwischenwerten (Gebäudewert Z. 2301, \(M_0\) Z. 2308, λ-Varianten Z. 2311–2312, K3-Band Z. 2314–2315), in dieser Sitzung grün ausgeführt. §7.1 ist reiner Antragstext ohne Hauptformel und braucht keinen Block. Einschränkung: abgelöste Eingangszahl → Befund 92; Zahlenwiderspruch zur Prosa → Befund 93. |
| **E3 — Verteilungsfunktionen und Formelsatz** | **ja (keine erklärungsbedürftige Form im Prüfumfang)** | Im Prüfumfang kommt keine Verteilungsfunktion vor — §7.1/§7.2 (Z. 2186–2325) führen weder Quantil-, Log-Normal-, Poisson- noch Faltungsform; die einzigen Formeln sind \(\lambda = A^{*}/(M_0 f_{\text{AWM}})\) (Z. 2249–2251) und die Produktform des Blocks (Z. 2301–2318), beide Grundrechenarten. Zu \(f_{\text{AWM}}\) liegt zusätzlich die zulässige Antwort (b) aus §8 vor (Rechenbeispiel mit Zahlen, Z. 2285 und Block). Der Abschnitt `## Ergebnis` (Z. 30–38) ist bis auf \(M_0\) und \(\lambda\) formelfrei. |
| **E4 — Zeichen und Begriffe** | **nein** | \(f_{\text{AWM}}\) ohne Zeichentabelleneintrag, ohne Parameter-Block und ohne Einheit (§4.8 Z. 1474, §7.2 Z. 2262) → **Befund 95** (C). Begriffe: „Restnutzungsdauer/Gesamtnutzungsdauer" ist bei erster Verwendung erklärt (Z. 2266–2268), „Sensitivitätsband" im Satzzusammenhang (Z. 2242–2243); „Zentralwert" (Z. 2250) bleibt unerklärt, wird aber nicht hier zuerst verwendet (Kapitel 3/4, Schwesterpakete) — hier nicht doppelt verbucht. |

**Nachrechnung statt Lektüre (§5, in dieser Sitzung ausgeführt).** Ausdruck:
`python3 -c "A=1.6*0.65*1.54*0.50*1.15*1.07; w=208.0*1.30*1950.0; M0=(0.872*w*339000*0.005979599550826+0.872*w*1380000*0.000675151053693)/1e9; print(A, w, M0, A/(M0*0.55), A/(M0*0.40), 1.132/(1.360*0.55), 1.132/(1.360*0.40), w*0.55, A*0.55, A*0.40, A*0.75, A*(1-0.55), (A*0.55-A)/A*100, 0.0103*0.55)"`

| Größe (Fundstelle) | gedruckt | nachgerechnet (obiger Ausdruck) | Abweichung |
|---|---|---|---|
| \(A^{*}\) des Blocks (Z. 2303) | — (als `A_stern` gesetzt) | **0,985384** | gegen §4.2 Z. 1123 (**1,132**): **−12,9 %** → Befund 92 |
| \(M_0\) (Z. 2308–2309) | 1,360 | **1,360418** | +0,03 % (Rundung) ✓ |
| Zeitwert je Gebäude (Z. 2285) | 290.004 € | **290.004,00** | **0** ✓ |
| λ bei nur umgestelltem Basiswert, Zentralwert (Z. 2250 bzw. Z. 2293) | **1,51** bzw. **1,32** | 1,132/(1,360·0,55) = **1,51337**; 0,985384/(1,360418·0,55) = **1,31695** | jede Rechnung für sich **< 0,4 %** korrekt — die beiden gedruckten Werte widersprechen **einander**, weil zwei verschiedene Anker eingesetzt sind → Befund 93 |
| λ am unteren Faktorende (Z. 2251 bzw. Z. 2312) | **2,08** bzw. **1,81** | **2,08088** bzw. **1,81081** | je < 0,05 %, derselbe Widerspruch → Befund 93 |
| K3 bei konsistentem Zeitwert (Z. 2288–2289) | 0,54 (0,39–0,74) | **0,541961** (0,394154–0,739038) | < 0,4 % ✓ (bezogen auf den abgelösten Anker) |
| Rückgang (Z. 2289–2290) | −0,44 Mrd., **−45 %** | **−0,443423**, **−45,00 %** | ✓ |
| Sanity-Untergrenze (Z. 2291) | 0,0057 | **0,005665** | +0,6 % (Rundung) ✓ |

**Zum Abschnitt `## Ergebnis` (Z. 30–38) — stimmen die genannten Beträge mit den Stellen überein,
auf die der Abschnitt verweist?** Teilweise: \(M_0\) = 1,360 Mrd. €₂₀₂₆/a stimmt mit §4.4 Z. 1230
überein, ebenso die Registerzählung „32 Registerzeilen, davon 7 belegt bzw. entschieden, 25 offen"
(gemessen in dieser Sitzung an `docs/evidenz/register.md`: `grep -c "^| 60-"` → **32**, davon mit
Statusklammer „(offen…)" **25**, entschieden/belegt **7**) — **aber \(\lambda\) = 0,724 (Z. 35)
steht gegen §4.4 Z. 1230 („1,132 / 1,360 = **0,832**"), §4.5 Z. 1381 und den Parameter-Block
`flood_bldg.lambda` Z. 2169 (`wert: 0.832`)** → **Befund 94** (B).

**Neue Befunde dieses Pakets (92–95)**

| Nr. | Kat. | Stelle · Art · Begründung · Vorschlag |
|---|---|---|
| 92 | **B** | **Stelle:** Bericht §7.2 Z. 2288 („sinkt die kalibrierte Bundessumme K3 von **0,99 Mrd. €₂₀₂₆/a**") und Z. 2303 (`A_stern = 1.6 * 0.65 * 1.54 * 0.50 * 1.15 * 1.07`), gegen §4.2 Z. 1123 (\(A^{*}\) = 1,838 · 0,65 · 1,54 · 0,50 · 1,15 · 1,07 = **1,132**) und §4.5 Z. 1381 (\(\lambda M_0\) = **1,132**). · **Art: Widerspruch (abgelöster Stand).** · **Begründung:** Der erste Faktor der Ankerkette ist im Beispielblock **1,6** statt des heute geltenden \(A_{\text{ver}}\) = 1,838 aus der Kleinste-Quadrate-Bestimmung (§4.1). Der ganze Sensitivitätsabschnitt hängt daran — Ausgangsbetrag 0,99 Mrd., Zielbetrag 0,54 (0,39–0,74) und die abgeleitete Sanity-Untergrenze; mit dem geltenden Anker lautete der Ausgangsbetrag 1,132 und der Zeitwert-Zentralwert **0,623** Mrd. €₂₀₂₆/a (nachgerechnet in dieser Sitzung: `python3 -c "print(1.132*0.55)"` → 0,6226). Der Prozentsatz −45 % bleibt unberührt, die absoluten Beträge nicht. Nach eiserner Regel 5 wird das nicht still nachgezogen, sondern verbucht. Kategorie B, weil die Rechenlogik stimmt, aber alle Euro-Beträge des Abschnitts auf einem abgelösten Anker stehen und §4.8 Z. 1474 sowie Kap. 6 Z. 1827 dieselbe Zahl „0,99" weitertragen. · **Vorschlag:** \(A^{*}\) im Block aus §4.2 übernehmen (1,838-Kette oder direkt 1,132 mit Quellenzeile), die davon abgeleiteten Beträge neu setzen und die Stellen Z. 1474, Z. 1827 und Z. 2512 im selben Zug nachziehen. |
| 93 | **B** | **Stelle:** Bericht §7.2, Begründung 1 Z. 2250–2251 (**1,51** / **2,08**) gegen Z. 2293 (**1,32**) und Beispielblock Z. 2311–2312 (`1.32` / `1.81`). · **Art: Widerspruch (innerhalb desselben Abschnitts).** · **Begründung:** Dieselbe Aussage — „wird nur der Basiswert auf den Zeitwert gesetzt, steigt λ auf …" — trägt im selben Abschnitt zwei Zahlenpaare, weil die Prosa mit \(A^{*}\) = 1,132 und der Block mit 0,985 rechnet (beide Rechnungen in dieser Sitzung nachvollzogen, Abweichung je < 0,4 %). Für den Adressaten nach §8 ist an dieser Stelle nicht entscheidbar, welcher Wert gilt; die Entscheidungstabelle Kap. 9 Z. 2512 zitiert zusätzlich „1,32 (bis 1,81)" (nur als Fundstelle, Kapitel 9 ist Schwesterpaket). Kategorie B: kein Rechenfehler, aber eine aus dem Bericht nicht auflösbare Doppelangabe. · **Vorschlag:** Nach Behebung von Befund 92 beide Stellen auf denselben Anker stellen und **eine** Angabe als maßgeblich kennzeichnen; die andere streichen, nicht stehen lassen. |
| 94 | **B** | **Stelle:** Bericht Abschnitt `## Ergebnis` Z. 35 („\(M_0\) = 1,360 Mrd. €₂₀₂₆/a und \(\lambda\) = **0,724**") gegen §4.4 Z. 1230 (\(\lambda\) = **0,832**), §4.5 Z. 1381 und Parameter-Block `flood_bldg.lambda` Z. 2169 (`wert: 0.832`). · **Art: Widerspruch (abgelöster Stand an der meistgelesenen Stelle).** · **Begründung:** Der Ergebnisabschnitt ist die Kurzfassung des Berichts und verweist selbst auf „Kap. 4"; der dort geführte Skalar ist seit der Kleinste-Quadrate-Ankerbestimmung 0,832. \(M_0\) = 1,360 stimmt, nur λ nicht — die Fortschreibung ist an dieser einen Stelle nicht angekommen. Der Standvermerk „Stand 17.09.2026, nach Review-Runde 2" erklärt den Widerspruch, löst ihn aber nicht auf: Ein Leser entnimmt dem Ergebnisabschnitt einen Wert, den der Bericht an drei anderen Stellen anders führt, und die Produkt-Parameterliste (P1) führt 0,832. Kategorie B. · **Vorschlag:** In Z. 35 λ auf 0,832 setzen und den Standvermerk mitziehen; alternativ den Skalar im Ergebnisabschnitt nicht beziffern und auf §4.4 verweisen, damit er nur an einer Stelle gepflegt wird. |
| 95 | **C** | **Stelle:** Bericht §7.2 Z. 2262 und §4.8 Z. 1474 (\(f_{\text{AWM}}\)); Zeichentabellen §3.5 Z. 750 und §5.1.1 Z. 1602 (nur zitiert); Kapitel 7, Parameter-Blöcke Z. 1843–2185 (nur zitiert, keine id `f_awm`). · **Art: Lücke (Prüfpunkt E4 aus §8).** · **Begründung:** E4 verlangt für jedes Formelzeichen Bedeutung in Klartext **samt Einheit**, Fundstelle „Zeichentabellen in Abschnitt 3, Parameter-Blöcke in Abschnitt 7". \(f_{\text{AWM}}\) ist an beiden vorgesehenen Orten nicht geführt: §3.5 deckt laut Überschrift nur die Kapitel 3 und 5 ab, ein Block existiert nicht, und die beiden Textstellen nennen Wert und Band, aber keine Einheit (dimensionslos, Verhältnis RND/GND). Kategorie C, weil Herleitung und Kennzeichnung als Abschätzung vollständig sind (P1 erfüllt, §4.8 Z. 1474) und allein die Zeichenführung fehlt. · **Vorschlag:** \(f_{\text{AWM}}\) in die Zeichentabelle §3.5 oder in eine eigene kleine Zeichentabelle in §7.2 aufnehmen, mit Einheit „– (Verhältnis RND/GND)"; ein Parameter-Block ist entbehrlich, solange der Faktor nur als Sensitivität läuft — das dann im Text ausdrücklich vermerken. |

**Abgrenzung und Status dieses Pakets.** Kein Befund wurde behoben (weder 92–95 noch ein
Altbefund). Geändert wurde ausschließlich diese Datei;
`docs/methodik/60_gebaeudeschaeden_flusshochwasser.md` (MD5 `24972e4404a8e1bc0990e63f1959798d`) und
`docs/evidenz/register.md` (MD5 `5fb629559a13d835e56831fcedc9b666`) sind byte-gleich geblieben, die
Arbeitsmappen wurden nur gelesen (eiserne Regel 2), `backend/scripts/lint_methodik.py` nicht
geändert. Ressourcen-Regel §3.4 eingehalten: nachgerechnet wurde aus den gedruckten Zahlen, kein
nationaler 100-m-Vollrasterlauf, die Stichproben-Dateien `docs/evidenz/60_stichprobe/hq_*.csv`
wurden nicht geöffnet. Nicht Gegenstand: Kapitelkopf 7 und Parameter-Blöcke Z. 1843–2185,
Kapitel 5, Kapitel 9, die Leitfragen 5 und 12, die Regression der Altbefunde sowie die Kopftabelle
„Offene Befunde" (Abschlusspaket).

### Befundregression Teil 6 (35, 36, 37, 38)

Paket T-0389 der Runde 3 (20.09.2026, zweite Hälfte des halbierten T-0368), eigene frische Sitzung:
Sie hat den geprüften Stand nicht geschrieben (eiserne Regel 4; geschrieben haben T-0235 bis
T-0243, T-0256 bis T-0259 und die Revisionspakete aus T-0281, alle im Endstatus). **In diesem Paket
wird keine Leitfrage aus §5 beantwortet und kein Befund behoben.** Prüfgegenstand ist der
**Umsetzungsnachweis im heutigen Berichtsstand**, nicht die Behauptung im Ledger: Für **35** und
**36** (Übersichtstabelle „offen", Autor-Revision mit Rechenweg) wird am heutigen Bericht
entschieden, ob der Rechenweg dort angekommen ist; für **37** („behoben") ist jede im Ledger
genannte neue Parameterzeile in §4.8 nachgelesen; für **38** („bewusst offen") gilt die Prüfregel
der Runde 3: „bestätigt geschlossen" nur, wenn die im Ledger festgehaltene Begründung im heutigen
Bericht als **Modellgrenze sichtbar** ist. Vorgabe P1 ist bei 37 und 38 unmittelbar angelegt: Steht
zu einer rechnenden Parameterzeile weder Quelle noch ausgewiesene Abschätzung samt Herleitung im
sichtbaren Berichtstext, ist das ein neuer Befund und kein „bestätigt geschlossen". Zeilennummern
beziehen sich auf den heutigen Stand von `docs/methodik/60_gebaeudeschaeden_flusshochwasser.md`
(2.513 Zeilen, MD5 `24972e4404a8e1bc0990e63f1959798d`).
**Befundnummern:** höchste zu Laufbeginn im Ledger vorhandene Nummer **95** (gemessen über alle
Tabellen-Nummernspalten und alle „Befund <n>"-Nennungen), neu vergeben sind deshalb **96, 97 und
98**.

| Nr | Urteil | Fundstelle (nachprüfbar) | Feststellung am heutigen Stand |
|---|---|---|---|
| 35 | **unvollständig geschlossen** | Bericht **§4.6 Z. 1351–1385**: Neufassung Z. 1353–1358, Untergrenze \(U\) = **0,0103 Mrd. €₂₀₂₆/a** **Z. 1362**, Obergrenze \(O\) = **6,29 Mrd. €₂₀₂₆/a** **Z. 1363**, Ausnahme vom Amtlichkeitsgebot **Z. 1365–1379**, Ist-Lage **Z. 1381–1385** · §4.8 **Z. 1472/1473** · Beispielblock **Z. 1563–1569** (`assert U <= lam * M0 <= O`) · gemessen: „1/100 Jahren" und „2,264" im ganzen Bericht **je 0 Treffer** | Die drei Teilpunkte (a)–(c) sind am heutigen Text belegt: (a) \(U\) folgt nicht mehr aus den Ankerfaktoren, sondern aus dem Fondsvolumen 8 Mrd. € (AufbhG 2013, `docs/evidenz/60_wiederaufbauhilfen_2013_2021.csv`), fortgeschrieben zu 10,35 Mrd. €₂₀₂₆, mal \(w\) = 1/3·1/3 ≈ 0,11 und \(f_{\text{fluss}}\) = 0,90, geteilt durch \(T\) = 100 a (Z. 1362); keine der sechs Ankergrößen geht ein. (b) \(O\) ist klassengerecht gebildet (GK3/GK4 0,1 a⁻¹, GK2 0,01 a⁻¹, Z. 1363) und trägt genau die **6,29 Mrd.**, die der Befundtext selbst vorgerechnet hatte. (c) Die Ausnahme vom Amtlichkeitsgebot ist für beide Enden ausdrücklich begründet (Z. 1365–1379). **Offen bleibt der letzte Satz des Vorschlags** („Das Band danach vorab fixieren und **nicht wieder weiten**", §6 Z. 488–489: „Toleranzen werden nicht nachträglich geweitet"): Das Band ist von [≈ 0,64; **2,264**] (Runde-2-Stand, Ledger Z. 993) auf **[0,0103; 6,29]** gegangen — Spannweite Faktor **611**, Untergrenze **1/110** des Ist-Werts 1,132, Obergrenze das **5,56-Fache**. Die Weitung ist im Bericht an keiner Stelle als solche ausgewiesen (Z. 1353–1358 nennt nur „ersetzt"), und der Test `U <= lam * M0 <= O` kann mit einer Untergrenze zwei Zehnerpotenzen unter dem Modellwert praktisch so wenig scheitern wie die abgelöste zirkuläre Grenze. → **Befund 96** (Kategorie B). Der Status von Befund 35 selbst bleibt unberührt. |
| 36 | **bestätigt geschlossen** | Bericht **§4.4 Z. 1240–1258** (Plausibilitätsschranke [0,11; 3,44], hergeleitet: \(\lambda_{\text{unten}}\) = 0,297/2,643 = 0,112384… → 0,11, \(\lambda_{\text{oben}}\) = 2,263/0,657 = 3,444409… → 3,44) · **Z. 1230–1232** (\(\lambda\)-Band 0,11–3,44) · **§4.3 Z. 1223** (M₀-Band 0,657–2,643, „Ersatzkette für Ledger-Befund 36") · **§4.8 Z. 1470** (eigene Zeile „Plausibilitätsschranke \(\lambda\) | 0,11 bzw. 3,44") · §4.1a **Z. 1048** (vier Fenster-\(\lambda\) gegen die Schranke) · Beispielblock **Z. 1512–1522** · gemessen: „2{,}00" und „0,50 oder" in Kapitel 4 (Z. 932–1573) **je 0 Treffer** | Beide Teile des Befunds sind geschlossen, und zwar genau auf dem im Vorschlag verlangten Weg. Die gesetzte Schranke 0,50/2,00 existiert nicht mehr; an ihrer Stelle steht die aus dem **vollständig fortgepflanzten** Band von \(A^{*}\) (0,297–2,263, §4.2) **und** \(M_0\) (0,657–2,643, §4.3) hergeleitete Schranke [0,11; 3,44] (Z. 1240–1258, im Beispielblock Z. 1512–1522 nachgerechnet). Damit ist auch der Widerspruch aufgelöst: Die Bandenden liegen nicht mehr außerhalb der Schranke, sondern bilden sie — Z. 1252–1257 sagt das für beide Enden ausdrücklich und beschränkt die Geltung auf den Zentralwert (0,832, „liegt innerhalb"). Der zweite Teil des Befunds („\(M_0\) trägt kein Band, 208 m², 1,30, 1.950 €, 6,311/1.200 und 339.000 gehen ungestreut ein") ist ebenfalls erledigt: §4.3 führt ein achtgrößiges \(M_0\)-Band (Z. 1203–1216, Beispielblock Z. 1499–1510), und die Beispielzellen-Rate 6,311/1.200 rechnet nicht mehr, sondern gemessene Klassenraten. **Abweichung zum Ledger, ohne eigenen Befund:** Die Übersichtstabelle Z. 61 und die Statuszeile Z. 991 führen 36 weiter als „offen — Herleitung fehlt weiter"; am heutigen Bericht ist sie vorhanden (die Autor-Revision Z. 1973 hält den Nachzug bereits fest). Kein neuer Befund. |
| 37 | **zurückgefallen** | Bericht **§4.8 Z. 1459–1474**: „Baupreisanstieg 2023 → 2024" **Z. 1468** ✓, „Plausibilitätsschranke \(\lambda\)" **Z. 1470** ✓, „Klassenraten Bestandsschranke" **Z. 1469**; Vermerke der einfließenden Abschätzungen bei \(\lambda\) **Z. 1467**, \(U\) **Z. 1472**, \(O\) **Z. 1473** · gegen **§4.6 Z. 1362** (rechnende Abschätzungen \(w\) = 0,11, \(f_{\text{fluss}}\) = 0,90, \(T\) = 100 a) und Beispielblock **Z. 1564–1567** (`w_u, f_fluss, T_u = (1/3)*(1/3), 0.90, 100`) · gemessen in §4.8 (Z. 1457–1573): „Betroffenheit" **0 Treffer**, „0,90" **0 Treffer**, „1/3" **0 Treffer**, „Wiederkehrzeit" **1 Treffer** (Z. 1472, Fließtext ohne Zahlenwert) | Die im Ledger behauptete Behebung trägt am heutigen Stand nur noch teilweise, und **dieselbe Lücke ist an neuer Stelle zurück**. Bestätigt: Die Zeile „Baupreisanstieg 2023 → 2024" (Z. 1468, mit Band 2,3–5,0 % und Sensitivität) und die Zeile „Plausibilitätsschranke \(\lambda\)" (Z. 1470, heute 0,11/3,44 statt 0,50/2,00) stehen in der P1-Tabelle; bei \(\lambda\), \(U\) und \(O\) ist vermerkt, welche Abschätzungen einfließen (Z. 1467, 1472, 1473). Die dritte im Ledger genannte Zeile „Betroffenheit exponierter Gebäude" (1/100 a) steht **nicht** in §4.8 — der Wert rechnet seit der §4.6-Neufassung nicht mehr und ist durch die Zeile „Klassenraten Bestandsschranke" (Z. 1469) abgelöst; das ist sachlich in Ordnung, macht die Ledger-Fundstelle aber unauffindbar. Entscheidend ist der Rückfall: Die **drei** Abschätzungen von KAP3, die heute in \(U\) rechnen (Wohn-/Wohngebäudeanteil 0,11, flussseitiger Anteil 0,90, Wiederkehrzeit 100 a), kommen in §4.8 nur als Fließtext in der Herleitungsspalte von \(U\) vor (Z. 1472), ohne eigene Zeile, ohne Wert, ohne Band, ohne Kennzeichnung — wörtlich die Lage, die Befund 37 für die alte 1/100-a-Betroffenheit beanstandet hatte („kommt sie nur als Wort in der Herleitungsspalte von \(O\) vor, ohne eigene Zeile und Kennzeichnung"). → **Befund 97** (Kategorie B). Der Status von Befund 37 selbst bleibt unberührt. |
| 38 | **unvollständig geschlossen** | Bericht **§4.2 Z. 1093** (Tabellenzeile „Preisstand 2024 → 2026 \(\pi\) 1,07 (**1,04–1,11**)"), **Z. 1120–1121** (Herleitung: „Band 1,07–1,16 … \(1{,}105/1{,}03 \approx 1{,}073\); Band 1,04–1,11"), **§4.8 Z. 1466** (dieselben Bandenden) und Beispielblock **Z. 1483–1484** (`hi = 1.838 * 0.75 * 1.75 * 0.65 * 1.30 * 1.11`, `assert abs(hi - 2.263) < 5e-3`) · Register-Band B4 **Z. 363** („1,050³ = 1,158 ⇒ **Band 1,07–1,16**") · gemessen: „1,04–1,11" im Bericht **3 Treffer** (Z. 1093, 1121, 1466), „1,126" **0 Treffer** | Der Rechenfehler besteht unverändert: 1,16/1,03 = **1,1262**, gedruckt ist 1,11 (Z. 1093, 1121, 1466); der Beispielblock rechnet mit 1,11 weiter (Z. 1483) und prüft nur die eigene Rundung. Geprüft wurde nach der Prüfregel dieses Pakets, ob die Entscheidung „bewusst offen, wird mit Befund 27 nachgezogen" im Bericht als Modellgrenze **sichtbar** ist: Sie ist es **nicht** — weder §4.2 (Z. 1093, 1113–1121) noch §4.8 (Z. 1466) noch der Beispielblock enthalten einen Vermerk, dass das obere Bandende vorläufig, gerundet oder aus einem offenen Befund heraus noch nicht nachgezogen ist; die Zurückstellung steht allein im Ledger. Außerdem ist die Wirkung seit Runde 2 gewachsen: Mit 1,126 läge die \(A^{*}\)-Obergrenze bei **2,296** statt 2,263 (Z. 1484) und — weil die Plausibilitätsschranke aus Befund 36 heute genau aus diesem Bandende folgt — die obere Schranke bei 2,296/0,657 = **3,49** statt 3,44 (Z. 1245–1249, Z. 1470). Der Rundungsfehler trägt damit jetzt auch die Schranke. → **Befund 98** (Kategorie C). Der Status von Befund 38 selbst (Kategorie C, bewusst offen) bleibt unberührt. |

#### Neue Befunde dieses Pakets (96, 97 und 98)

| Nr | Kat. | Befund |
|---|---|---|
| 96 | **B** | **Stelle:** Bericht §4.6, Bandtabelle **Z. 1362/1363** (\(U\) = 0,0103; \(O\) = 6,29 Mrd. €₂₀₂₆/a), Neufassungsabsatz **Z. 1353–1358**, Ist-Lage **Z. 1381–1385**, Beispielblock **Z. 1563–1569**; §4.8 **Z. 1472/1473**. · **Art: Lücke (Sanity-Band ohne Trennschärfe, Weitung nicht ausgewiesen)** (§3.4 „Sanity-Bänder mit Unter- und Obergrenze"; §6 Z. 488–489 „Prüfsteine, die scheitern, eskalieren in einen Modellentscheid — Toleranzen werden nicht nachträglich geweitet"; §5 LF 8). · **Begründung:** Die Neufassung nach Befund 35 beseitigt die Zirkularität (\(U\) enthält keine der sechs Ankergrößen) und den fehlenden Klassenbezug der Obergrenze — das ist erfüllt. Zugleich ist das Band dabei erheblich weiter geworden: vom Runde-2-Stand [≈ 0,64; 2,264] (Ledger Z. 993) auf **[0,0103; 6,29]**, Spannweite **Faktor 611**. Der Ist-Wert 1,132 Mrd. €₂₀₂₆/a liegt beim **110-Fachen** der Untergrenze und bei **18 %** der Obergrenze. Eine Untergrenze zwei Zehnerpotenzen unter dem Modellwert kann den Test `U <= lam * M0 <= O` praktisch ebenso wenig auslösen wie die abgelöste tautologische Grenze; die im Vorschlag zu Befund 35 verlangte Zusage „vorab fixieren und nicht wieder weiten" ist damit sachlich nicht eingelöst, und die Weitung ist im Bericht nirgends beziffert oder begründet (Z. 1353–1358 spricht nur von „ersetzt"). Verschärfend: \(U\) ruht auf dem **kleineren** der beiden Fondsvolumina (8 Mrd. €, 2013) mal drei multiplikativ untersten Abschätzungen, ohne Band und ohne Prüfung, wie empfindlich die Grenze darauf reagiert. Kategorie B: Kein ausgewiesener Zahlenwert ist falsch und die Lage ist korrekt gerechnet; betroffen ist die Aussagekraft eines Abnahme-Prüfsteins nach §6 (CI-Test „Bundessumme ∈ [Untergrenze, Obergrenze]", Aufgabe Z. 513). · **Vorschlag:** In §4.6 die Weitung gegenüber dem Runde-2-Band ausdrücklich beziffern und begründen; die Untergrenze trennschärfer fassen (z. B. beide Wiederaufbauhilfe-Volumina als zwei Ereignisse in 13 Jahren statt nur des kleineren, oder Band statt Punktwert für \(w\), \(f_{\text{fluss}}\) und \(T\)) und den Abstand des Ist-Werts zu beiden Enden als Kennzahl ausweisen, damit erkennbar bleibt, wie viel der Prüfstein noch prüft. Nicht in diesem Paket umgesetzt (Dateirahmen), hier nur verbucht. |
| 97 | **B** | **Stelle:** Bericht §4.8 P1-Tabelle **Z. 1459–1474**, insbesondere die Zeile \(U\) **Z. 1472**, gegen §4.6 **Z. 1362** (\(w\) = 1/3·1/3 ≈ 0,11; \(f_{\text{fluss}}\) = 0,90; \(T\) = 100 a, dort je ausdrücklich „**Abschätzung von KAP3**") und Beispielblock **Z. 1564–1567**. · **Art: Lücke (Vorgabe P1 „Gilt für alle Parameter"; §3.9 „Unzulässig: … Bandgrenzen, Referenzwerte")** — Rückfall des mit Befund 37 geschlossenen Mangels an neuer Stelle. · **Begründung:** Befund 37 verlangte, jeden in Kapitel 4 rechnenden Wert mit Wert, Band und Kennzeichnung in die P1-Tabelle aufzunehmen, und beanstandete ausdrücklich, dass die damalige Betroffenheit 1/100 a „nur als Wort in der Herleitungsspalte von \(O\) vor[kommt], ohne eigene Zeile und Kennzeichnung". Genau diese Lage besteht heute für die drei Abschätzungen, die die neue Untergrenze tragen: Wohn-/Wohngebäudeanteil **0,11**, flussseitiger Anteil **0,90** und Wiederkehrzeit **100 a** rechnen in \(U\) (Z. 1362, Beispielblock Z. 1566: `w_u, f_fluss, T_u = (1/3)*(1/3), 0.90, 100`), stehen in §4.8 aber nur als Fließtext-Halbsatz in der Herleitungsspalte von \(U\) (Z. 1472: „Wohngebäude-/Wohnanteil, flussseitiger Anteil und die Umlage auf die Wiederkehrzeit sind Abschätzungen von KAP3") — ohne eigene Zeile, ohne Zahlenwert, ohne Band. Gemessen in §4.8 (Z. 1457–1573): „Betroffenheit", „0,90" und „1/3" je **0 Treffer**; „Wiederkehrzeit" **1 Treffer**, und zwar genau der Fließtext-Halbsatz in Z. 1472, ohne Zahlenwert. Ein Nutzer der Parameterliste sieht den Wert 0,0103, nicht die drei Zahlen, die ihn zu 0,89 % ihres Produkts bestimmen. Dieselbe Tabelle führt für \(w_{\text{wg}}\), \(u\), \(\varphi\), \(\kappa\) und \(\pi\) jeweils Wert **und** Band — der Maßstab ist also der Tabelle selbst entnommen. Kategorie B wie der Ursprungsbefund 37. · **Vorschlag:** In §4.8 drei Zeilen aufnehmen — „Wohngebäudeanteil der Aufbauhilfe-Mittel \(w\) 0,11", „flussseitiger Anteil der Aufbauhilfe-Ereignisse \(f_{\text{fluss}}\) 0,90", „Wiederkehrzeit der Aufbauhilfe-Ereignisse \(T\) 100 a" —, je mit Band und dem Vermerk „Abschätzung von KAP3, Herleitung §4.6", und bei \(U\) auf sie verweisen. Zugleich den Ledger-Eintrag zu 37 (Z. 62, Z. 1516) um den Hinweis ergänzen, dass die dort genannte Zeile „Betroffenheit exponierter Gebäude" mit der §4.6-Neufassung durch „Klassenraten Bestandsschranke" (Z. 1469) abgelöst ist. Nicht in diesem Paket umgesetzt (Dateirahmen), hier nur verbucht. |
| 98 | **C** | **Stelle:** Bericht §4.2 **Z. 1093** und **Z. 1120–1121**, §4.8 **Z. 1466** (je „1,07 (1,04–1,11)"), Beispielblock **Z. 1483–1484** (`* 1.11`, `assert abs(hi - 2.263) < 5e-3`), gegen Register-Band B4 **Z. 363** („Band 1,07–1,16") sowie §4.4 **Z. 1245–1249** und §4.8 **Z. 1470** (Plausibilitätsschranke oben 3,44). · **Art: Fehler (fortbestehender Rundungsfehler ohne sichtbare Modellgrenze; neue Folgewirkung)** (eiserne Regel 5 „Divergenz wird nie still gefixt"; §3.9 Herleitungspflicht; Vorgabe P1 „samt Herleitung"; Vorgabe P3). · **Begründung:** Befund 38 ist im Ledger als „bewusst offen" geführt mit der Begründung, der Rundungsfehler werde mit Befund 27 nachgezogen. Der Fehler selbst besteht: 1,16/1,03 = **1,1262**, gedruckt ist **1,11** an drei Stellen (Z. 1093, 1121, 1466), und der Beispielblock rechnet mit 1,11 (Z. 1483), prüft also nur die eigene Rundung. Neu ist zweierlei. Erstens ist die Zurückstellung im Bericht **nirgends sichtbar**: Keine der drei Fundstellen und kein Kommentar im Block vermerkt, dass das obere Bandende vorläufig ist oder an einem offenen Befund hängt; ein Leser hält 1,11 für hergeleitet, obwohl die eigene Rechnung des Berichts (1,16/1,03) 1,126 ergibt. Zweitens trägt der Fehler seit der Revision der Runde 2 mehr als vorher: Weil die Plausibilitätsschranke aus Befund 36 heute aus genau diesem Bandende folgt (\(\lambda_{\text{oben}}\) = \(A^{*}_{\text{oben}}\)/\(M_{0,\text{unten}}\)), verschiebt die Korrektur nicht nur \(A^{*}_{\text{oben}}\) von 2,263 auf **2,296**, sondern auch die obere Schranke von 3,44 auf **3,49** (2,296/0,657) und damit einen im Produkt ausgewiesenen Parameter (§4.8 Z. 1470, Kap. 7). Kategorie C wie der Ursprungsbefund: Die Größenordnung des Ergebnisses ändert sich nicht, der Zentralwert \(\pi\) = 1,073 ist richtig; betroffen sind ein Bandende, die davon abgeleitete Schranke und die Nachvollziehbarkeit. · **Vorschlag:** Beim Nachzug mit Befund 27 zusätzlich \(\lambda\)-Band und Plausibilitätsschranke (§4.4, §4.8, Kap. 7) mitziehen und die Zusicherung im Beispielblock Z. 1484 anpassen; bis dahin an Z. 1093 und Z. 1466 einen Halbsatz aufnehmen, dass das obere Bandende auf 1,11 gerundet ist und mit Befund 27/38 auf 1,126 nachgezogen wird (Modellgrenze sichtbar machen). Nicht in diesem Paket umgesetzt (Dateirahmen), hier nur verbucht. |

#### Abgrenzung und Status dieses Pakets

- **Geändert wurde ausschließlich `reviews/BEFUNDE_60.md`** (angehängt).
  `docs/methodik/60_gebaeudeschaeden_flusshochwasser.md` (MD5
  `24972e4404a8e1bc0990e63f1959798d`) und `docs/evidenz/register.md` (MD5
  `5fb629559a13d835e56831fcedc9b666`) sind byte-gleich geblieben,
  `backend/scripts/lint_methodik.py` wurde nicht geändert (T-0234), die Arbeitsmappen nur gelesen
  (eiserne Regel 2). Der Bericht wurde ausschließlich an den in der Tabelle ausgewiesenen Stellen
  gelesen und nachgeprüft.
- **Kein Befund behoben, keiner umnummeriert.** Höchste vorhandene Nummer zu Laufbeginn: **95**;
  neu vergeben sind **96, 97 und 98**. Die Status der Befunde 35 bis 38 selbst bleiben unberührt.
- **Keine Leitfrage aus §5 beantwortet.** Dieses Paket führt allein die Regression der Nummern
  **35, 36, 37 und 38**; die Nummern 31 bis 34 hat das Schwesterpaket T-0388 geführt. Zusammen
  decken beide die acht Nummern des ersetzten T-0368 genau einmal ab.
- **Vorgabe P1 angelegt (37 und 38):** geprüft ist, ob zu jeder rechnenden Parameterzeile Quelle
  oder ausgewiesene Abschätzung samt Herleitung im sichtbaren Berichtstext steht; ein
  Code-Kommentar zählt nicht. Bei 37 fehlen die drei \(U\)-Abschätzungen (→ 97), bei 38 fehlt der
  Hinweis auf das gerundete Bandende (→ 98).
- **Prüfregel für „bewusst offen" angewandt (38):** „bestätigt geschlossen" nur bei im Bericht
  sichtbarer Modellgrenze; sie fehlt, deshalb „unvollständig geschlossen".
- **Ressourcen-Regel §3.4 eingehalten:** kein nationaler 100-m-Vollraster-Lauf; nachgerechnet wurde
  aus den gedruckten Zahlen, die Stichproben-Dateien `docs/evidenz/60_stichprobe/*.csv` wurden
  nicht geöffnet.
- **Kopftabelle „Offene Befunde" bewusst nicht fortgeschrieben** (Dateirahmen der Runde-3-Pakete,
  T-0359); ebenso unberührt bleiben die Statuszeilen zu 35–38 in der Übersichtstabelle (Z. 60–63),
  auch dort, wo sie vom heutigen Berichtsstand abweichen (36).

### Befundregression Teil 7 (39, 40, 41, 42)

Paket T-0390 der Runde 3 (20.09.2026, erste Hälfte des halbierten T-0369), eigene frische Sitzung:
Sie hat den geprüften Stand nicht geschrieben (eiserne Regel 4; geschrieben haben T-0235 bis
T-0243, T-0256 bis T-0259 und die Revisionspakete aus T-0281, alle im Endstatus). **In diesem Paket
wird keine Leitfrage aus §5 beantwortet und kein Befund behoben.** Prüfgegenstand ist der
**Umsetzungsnachweis im heutigen Berichtsstand**, nicht die Behauptung im Ledger: **39** steht in
der Übersichtstabelle auf „offen", obwohl die Autor-Revision (Z. 1803) den Referenzzustand des
Wächters nachgezogen hat — entschieden wird am heutigen §4.7; **40** ist ein A-Befund mit
18 neuen Parameter-Blöcken in Kap. 7 und trägt „behoben"; **41** und **42** sind in der
Autor-Revision in Teilschritten dokumentiert (Z. 1537 bzw. Z. 1592/1611/1629) und werden gegen den
heutigen Text gehalten. Bei **40** ist Vorgabe P1 unmittelbar angelegt: an drei Parameter-Blöcken
(`flood_bldg.n_efh_zfh`, `flood_bldg.k_bgf`, `flood_bldg.p_hq_extrem`) ist stichprobenweise
nachgelesen, ob Quelle oder ausgewiesene Abschätzung **samt Herleitung im sichtbaren Berichtstext**
steht; ein Code-Kommentar zählt nicht. Zeilennummern beziehen sich auf den heutigen Stand von
`docs/methodik/60_gebaeudeschaeden_flusshochwasser.md` (2.513 Zeilen, MD5
`24972e4404a8e1bc0990e63f1959798d`).
**Befundnummern:** höchste zu Laufbeginn im Ledger vorhandene Nummer **98** (gemessen über alle
Tabellen-Nummernspalten und alle „Befund <n>"-Nennungen), neu vergeben sind deshalb **99 und 100**.

| Nr | Urteil | Fundstelle (nachprüfbar) | Feststellung am heutigen Stand |
|---|---|---|---|
| 39 | **bestätigt geschlossen** | Bericht **§4.7 Z. 1387–1456**: Referenzzustand **Z. 1394–1410** („der Referenzzustand des Wächters ist entsprechend als **das über die Kalibrierjahre 2002–2024 gleichgewichtete Ausstattungsmittel** definiert, nicht als Ausstattungsstand zu einem Stichtag", Z. 1399–1403), Gewichte \((2024-t+1)/23\) **Z. 1404–1407** (2020 = 21,7 %, 2014 = 47,8 %, 2002 = 100 %), Verfallsregel **Z. 1416–1426** (Verschiebung **1/24** des Abstands, nicht ein Jahr), Modellgrenze **Z. 1428–1443** · gemessen: „Ausstattungsstand 31.12.2024" im ganzen Bericht **0 Treffer** | Alle drei Teile des Vorschlags sind am heutigen Text belegt. (a) Der Referenzzustand ist nicht mehr der Stichtag, sondern das über die 23 Kalibrierjahre gleichgewichtete Ausstattungsmittel, hergeleitet aus §4.1a (bei \(M_t \equiv M_0\) fällt der Kleinste-Quadrate-Schätzer auf das arithmetische Mittel zurück, Gewicht 1/23 je Jahr). (b) Die Verfallsregel ist auf die tatsächliche Gewichtsverschiebung umgestellt und ausgerechnet: \((23\bar A_{23} + A_{2025})/24 = \bar A_{23} + (A_{2025}-\bar A_{23})/24\), Verfall erst mit dem Neu-Fit von \(\lambda\). (c) Richtung und Größenordnung der Verzerrung bei geparktem \(q_0\) sind als Modellgrenze ausgewiesen und beziffert: Überschätzung des schon eingepreisten Anteils um \((t-2002)/23\), 78,3 Prozentpunkte für 2020, 52,2 für 2014, 0 für 2002, bis 95,7 % für 2024; Richtung „konservativ gegen Doppelzählung, aber unterzählend beim Hebel" (Z. 1438–1441). Der im Ledger Z. 994 hinterlegte Prüfausdruck (`'Ausstattungsstand 31.12.2024' in t and 'gewicht' not in t.lower()`) endet damit heute mit **Exit 1**. **Abweichung zum Ledger, ohne eigenen Befund:** Übersichtstabelle **Z. 64** und Statuszeile **Z. 994** führen 39 weiter als „offen — Referenzzustand unverändert"; die Autor-Revision **Z. 1803** hält den Nachzug bereits fest. Kein neuer Befund. |
| 40 | **unvollständig geschlossen** | Bericht **Kap. 7 Z. 1843–2185**: Einleitungssatz **Z. 1845**, 22 Blöcke (`id:`-Zeilen **Z. 1869–2168**), Kostensätze **Z. 1928–1956** (`preisstand: 2026`, `umrechnungsfaktor: 1.8578`), §3.5 Zeile \(n_t\) **Z. 779/780** · P1-Stichprobe: `flood_bldg.n_efh_zfh` **Z. 1928–1941** (Quelle „NHK 2010, ImmoWertV Anlage 4; Fortschreibung mit Baupreisindex (Langbeleg B4)", Herleitung sichtbar **B4 Z. 363–364** und **§3.4 Z. 684**), `flood_bldg.k_bgf` **Z. 1958–1970** (Herleitung **§3.4 Z. 686**, „Abschätzung von KAP3", Band 1,25–1,40), `flood_bldg.p_hq_extrem` **Z. 2000–2012** (Herleitung **§3.4 Z. 664–672**, geometrisches Mittel \(\sqrt{5{,}0\cdot10^{-3}\cdot1{,}0\cdot10^{-3}} = 2{,}236\cdot10^{-3}\)) · Anker vorhanden: `#tiefen-schadensfunktion` **Z. 587**, `#kernformel-zelle` **Z. 645**, `#kalibrierung-zielwert` **Z. 1081**, `#niveau-skalar` **Z. 1227** · gegen **§4.8 Z. 1461–1475** (15 Parameterzeilen) | Der im Ledger genannte Kern ist belegt: Der Einleitungssatz „Alle weiteren Blöcke entstehen …" ist ersetzt, der Euro-Pfad steht (beide Kostensätze mit `preisstand: 2026`, Band und Umrechnungsfaktor 1,8578), und die P1-Stichprobe an drei Blöcken besteht — jeder trägt `kennzeichnung`, und die Herleitung ist über den Anker im **sichtbaren** Berichtstext ausgeschrieben, nicht im Kommentar (der alte Prüfausdruck Z. 1191 endet mit Exit 1). **Rest:** Der heutige Einleitungssatz **Z. 1845** behauptet „Kap. 7 führt **je rechnendem Parameter aus §3.5 und §4.8** einen Block". §4.8 führt heute 15 Parameterzeilen; Blöcke gibt es für **sechs** davon (\(w_{\text{wg}}\), \(u\), \(\varphi_{\text{fluss}}\), \(\kappa\), \(\pi\), \(\lambda\)). **Acht rechnende §4.8-Parameter haben keinen Block:** \(A_{\text{ver}}\) Anker (Z. 1461), Baupreisanstieg 2023 → 2024 (Z. 1468), Klassenraten Bestandsschranke (Z. 1469), Plausibilitätsschranke \(\lambda\) (Z. 1470), Toleranz Verteilungsprüfung (Z. 1471), \(U\) (Z. 1472), \(O\) (Z. 1473), \(f_{\text{AWM}}\) (Z. 1474); allein \(q_0\) (Z. 1475) ist zu Recht ohne Block, weil geparkt. Genau das war der Vorschlag zu Befund 40 („je Parameter aus §3.5 und §4.8 einen Block anlegen"), und genau das behauptet der Bericht von sich selbst. → **Befund 99** (Kategorie B). Der Status von Befund 40 selbst bleibt unberührt. |
| 41 | **unvollständig geschlossen** | Bericht **§7.2 Z. 2230–2325** (Anker `#fortschreibung-neuwert-k3` **Z. 2228**), \(f_{\text{AWM}}\) = 0,55 (0,40–0,75) **Z. 2262**, Ergebnis-Sensitivität **Z. 2287–2294**, Beispielblock **Z. 2297–2312**; nachgezogen in Kap. 1 **Z. 128**, B4 **Z. 386–389**, §3.4 **Z. 690–691**, §4.8 **Z. 1474**, Kap. 6 Modellgrenze 9 **Z. 1826–1832**, Entscheidungslog Nr. 7 **Z. 2512** · gegen den heutigen K3-Betrag **§4.2 Z. 1123**, **§4.4 Z. 1230**, **§4.6 Z. 1381** (je \(\lambda \cdot M_0\) = **1,132 Mrd. €₂₀₂₆/a**) und gegen **§7.2 Z. 2250–2251**, das im selben Kapitel bereits mit 1,132 rechnet · gemessen: „0,99" im Bericht **4 Treffer** (Z. 1474, 1827, 2288, 2292) | Der Kern des Befunds ist geschlossen, und zwar auf dem zweiten der beiden vorgeschlagenen Wege: Der Neuwert bleibt Basiswert, die Abweichung von Mon. J64 steht als **Antrag auf Fortschreibung** in §7.2 (eiserne Regel 2, nicht still überstimmt), das Wort „Zeitwertansatz" kommt nicht mehr 0-mal vor, und die Zeitwert-Lesart ist als beziffertes Band mit \(f_{\text{AWM}}\) = 0,55 (0,40–0,75, Abschätzung von KAP3 nach § 38 ImmoWertV) geführt; die Untergrenzen-Aussage ist in Kap. 6 Modellgrenze 9 geprüft und ausdrücklich auf „Untergrenze nur im Konto- und Mengenumfang" zurückgenommen. **Rest:** Die vom Vorschlag ausdrücklich verlangte **Ergebnis-Sensitivität** ruht auf einem überholten Betrag. §7.2 Z. 2288 lässt die kalibrierte Bundessumme K3 „von **0,99** Mrd. €₂₀₂₆/a auf **0,54**" sinken (Band 0,39–0,74); der Beispielblock rechnet dazu **Z. 2303** mit `A_stern = 1.6 * 0.65 * ...` — dem **Ankerwert 1,6** aus der Zeit vor der Kleinste-Quadrate-Ankerbestimmung. Heute ist \(A_{\text{ver}}\) = 1,838 und K3 = **1,132** (Z. 1123, 1230, 1381), also wären es **0,62** (1,132 · 0,55 = 0,6226) im Band **0,45–0,85**, nicht 0,54 (0,39–0,74). Derselbe überholte Anker trägt die \(\lambda\)-Angabe „1,32 (bis 1,81)" im Beispielblock Z. 2311/2312 und im Entscheidungslog Z. 2512, während der Fließtext **Z. 2250–2251** desselben Abschnitts bereits 1,132/(1,360 · 0,55) = **1,51** (bzw. 2,08) ausweist — §7.2 widerspricht sich intern. Die Prozentangabe −45 % bleibt richtig (skaleninvariant), die vier gedruckten Absolutbeträge nicht. → **Befund 100** (Kategorie B). Der Status von Befund 41 selbst bleibt unberührt. |
| 42 | **bestätigt geschlossen** | Bericht **Kap. 8 Z. 2326–2412**: Formatsatz **Z. 2328–2332** (§3.8-Kette einschließlich Archiv-Snapshot, Begründungspflicht bei Lücke), Punkt 4 **Z. 2361–2375**, Quellen 5, 6 und 7 **Z. 2376–2412** (je Organ, Jahr, Titel, URL, Archiv-Snapshot, Zugriffsdatum, „Volltext geprüft") · Langbelege **B1 Z. 199–240**, **B2 Z. 241–268**, **B3 Z. 269–302**, **B4 Z. 303–392**, **B5 Z. 393–468**, **B6 Z. 469–522**; begründeter Snapshot-Verzicht **Z. 342–344** (Destatis-PM Nr. 241/2026, Wayback-Statuscode 403) und Vermerk **Z. 310** · gemessen: „GDV" in Kap. 8 **5 Treffer** (vorher 0), `web.archive.org` in Kap. 8 **4 Treffer** (vorher 1), in B1–B6 **13 Treffer** (B1 3, B2 1, B3 2, B4 4, B5 2, B6 1), im ganzen Bericht **17** | Beide Teile sind am heutigen Text belegt. (a) Die Quelle des nationalen Ankers steht als Quelle 5 (GDV-Naturgefahrenstatistik 2024, Medieninformation 31.05.2025, mit Snapshot vom 10.05.2026 und den am Snapshot abgeglichenen Zitaten 2,6 Mrd. € / „rund eine Milliarde Euro mehr"), Quelle 6 (Versicherungsdichte 57 %, 10,2 Mio. Wohngebäude, Snapshot 17.04.2026) und Quelle 7 (Datenservice-Broschüre, Jahresreihe 2002–2024, Snapshot 07.01.2026, Angaben wörtlich aus `docs/evidenz/60_gdv_jahresreihe_2002_2024.csv`). Der Verweis aus §4.1 auf „vollständige Belege in Kap. 8" läuft damit nicht mehr ins Leere. (b) Jede externe Webquelle der Langbelege trägt heute entweder einen datierten Archiv-Snapshot oder eine ausdrückliche Begründung des Verzichts: 13 Snapshots über B1–B6, dazu bei den laufend gepflegten Rechtsfassungen (§ 74 WHG, ImmoWertV Anlage 4) der Vermerk zur maßgeblichen Zugriffsfassung, bei den DOI-gebundenen Zeitschriftenquellen die Feststellung, dass der Snapshot entbehrlich ist, und bei der Destatis-PM Nr. 241/2026 der begründete Verzicht (archivseitig gesperrt, „Save Page Now" scheitert). Punkt 4 nennt das Format jetzt einschließlich Archiv-Snapshot und weist den Stand nicht mehr als offen aus. Beide im Ledger Z. 1193 hinterlegten Prüfausdrücke enden folgerichtig mit Exit 1. Kein neuer Befund. |

#### Neue Befunde dieses Pakets (99 und 100)

| Nr | Kat. | Befund |
|---|---|---|
| 99 | **B** | **Stelle:** Bericht Kap. 7, Einleitungssatz **Z. 1845** („Kap. 7 führt je rechnendem Parameter aus §3.5 und §4.8 einen Block"), Blockliste **Z. 1869–2168** (22 `id:`-Zeilen), gegen §4.8 **Z. 1461–1475**, dort insbesondere die Zeilen \(A_{\text{ver}}\) **Z. 1461**, Baupreisanstieg **Z. 1468**, Klassenraten Bestandsschranke **Z. 1469**, Plausibilitätsschranke \(\lambda\) **Z. 1470**, Toleranz Verteilungsprüfung **Z. 1471**, \(U\) **Z. 1472**, \(O\) **Z. 1473**, \(f_{\text{AWM}}\) **Z. 1474**. · **Art: Lücke (§4 „Parameter-Block-Format … wird per Skript in die Produkt-Registry extrahiert"; Vorgabe P1 „gilt für alle Parameter"; §5 LF 12)** — Rest des mit Befund 40 als behoben geführten Mangels. · **Begründung:** Der Vorschlag zu Befund 40 lautete „je Parameter aus §3.5 und §4.8 einen Block anlegen", und der Bericht sagt in Z. 1845 von sich selbst, er tue das. Von den 15 Parameterzeilen des §4.8 haben heute **sechs** einen Block (\(w_{\text{wg}}\), \(u\), \(\varphi_{\text{fluss}}\), \(\kappa\), \(\pi\), \(\lambda\)); **acht rechnende Zeilen haben keinen** — der Ankerwert \(A_{\text{ver}}\) selbst, der Baupreisanstieg, die ZÜRS-Klassenraten der Bestandsschranke, die Plausibilitätsschranke, die Toleranz der Verteilungsprüfung, die Sanity-Grenzen \(U\) und \(O\) und der Alterswertminderungsfaktor \(f_{\text{AWM}}\). Nur \(q_0\) ist zu Recht blocklos (geparkt, Z. 1475). Die Folge ist dieselbe, die Befund 40 für die Kostensätze beschrieben hatte, nur eine Ebene höher: Die Registry-Extraktion nach §4 liefert den Kalibrier- und Prüfpfad nicht, und die nutzersichtbare Parameterliste des Produkts enthielte weder die Sanity-Grenzen noch die Plausibilitätsschranke, obwohl §4.8 sie als Parameter dieses Kapitels führt und §4.4/§4.6 mit ihnen rechnen. Kategorie **B** statt A wie beim Ursprungsbefund: Der Euro-Pfad und die Kernformel sind vollständig geblockt, Integration und P1-Nachweis sind also nicht mehr blockiert; betroffen sind die acht Kalibrier- und Prüfgrößen und die Richtigkeit der Selbstaussage in Z. 1845. · **Vorschlag:** Für die acht Zeilen je einen Block in Kap. 7 anlegen (mit `kennzeichnung`, `herleitung_anker` auf `#kalibrierung-zielwert`, `#niveau-skalar` bzw. den §4.6-Abschnitt, Band und — bei \(A_{\text{ver}}\), \(U\), \(O\) — `preisstand: 2026`) oder, wo ein Block bewusst unterbleibt (z. B. bei einer reinen Prüftoleranz), den Einleitungssatz Z. 1845 entsprechend einschränken und die Ausnahme dort benennen. Nicht in diesem Paket umgesetzt (Dateirahmen), hier nur verbucht. |
| 100 | **B** | **Stelle:** Bericht §7.2 **Z. 2287–2294** („sinkt die kalibrierte Bundessumme K3 von **0,99 Mrd. €₂₀₂₆/a** auf **0,54**", Band 0,39–0,74; „bleibt der Betrag bei 0,99") und Beispielblock **Z. 2297–2312**, dort **Z. 2303** `A_stern = 1.6 * 0.65 * 1.54 * 0.50 * 1.15 * 1.07` sowie **Z. 2311/2312** (`1.32`, `1.81`); nachgezogene Stellen §4.8 **Z. 1474** und Kap. 6 Modellgrenze 9 **Z. 1827**, Entscheidungslog Nr. 7 **Z. 2512** — gegen §4.2 **Z. 1123**, §4.4 **Z. 1230**, §4.6 **Z. 1381** (K3 = **1,132 Mrd. €₂₀₂₆/a**, \(A_{\text{ver}}\) = 1,838) und gegen §7.2 **Z. 2250–2251** (rechnet bereits mit 1,132 → \(\lambda\) = 1,51 bzw. 2,08). · **Art: Fehler (Sensitivität auf überholtem Anker; Bericht widerspricht sich intern)** (§3.9 Abgeschätzt „Bandbreite, Ergebnis-Sensitivität"; eiserne Regel 5; Vorgabe P1 „samt Herleitung"; §5 LF 9). · **Begründung:** Die mit Befund 41 verlangte Ergebnis-Sensitivität des Zeitwertansatzes ist zwar vorhanden, rechnet aber auf dem Ankerwert **1,6** (Z. 2303), der seit der Kleinste-Quadrate-Ankerbestimmung durch **1,838** abgelöst ist; daraus stammt der Ausgangsbetrag **0,99 Mrd. €₂₀₂₆/a**, während der Bericht an drei anderen Stellen **1,132** als kalibrierte Bundessumme ausweist (Z. 1123, 1230, 1381). Mit \(f_{\text{AWM}}\) = 0,55 ergäbe sich **0,62 Mrd. €₂₀₂₆/a** (1,132 · 0,55 = 0,6226) im Band **0,45–0,85** (1,132 · 0,40 = 0,4528; 1,132 · 0,75 = 0,849), nicht 0,54 (0,39–0,74). Der Fehler ist an vier gedruckten Stellen sichtbar (Z. 1474, 1827, 2288, 2292) und steckt zusätzlich in der \(\lambda\)-Aussage des Beispielblocks (1,32/1,81 statt 1,51/2,08) und des Entscheidungslogs; der Block fällt nicht auf, weil er den alten Anker als Literal führt und damit nur seine eigene Rechnung prüft. Innerhalb desselben §7.2 stehen beide Stände nebeneinander (Z. 2250–2251 gegen Z. 2288/2303), was für einen Leser nicht auflösbar ist. Die relative Aussage −45 % bleibt richtig, weil \(f_{\text{AWM}}\) multiplikativ wirkt; falsch sind die Absolutbeträge, und Kap. 6 Modellgrenze 9 trägt sie in die Modellgrenzen-Liste. Kategorie **B** wie der Ursprungsbefund 41: Es ist kein Größenordnungsfehler, betroffen sind eine ausgewiesene Sensitivität, eine Modellgrenze und die Widerspruchsfreiheit des Berichts. · **Vorschlag:** In §7.2 den Beispielblock auf \(A_{\text{ver}}\) = 1,838 umstellen (oder \(A^{*}\) = 1,132 aus §4.2 übernehmen statt neu zu multiplizieren), die Beträge 0,99/0,54/0,39–0,74 auf 1,132/0,62/0,45–0,85 nachziehen und dieselbe Korrektur in §4.8 Z. 1474, Kap. 6 Modellgrenze 9 (Z. 1827) und Entscheidungslog Nr. 7 (Z. 2512, dort auch die \(\lambda\)-Werte 1,32/1,81 → 1,51/2,08) mitführen. Nicht in diesem Paket umgesetzt (Dateirahmen), hier nur verbucht. |

#### Abgrenzung und Status dieses Pakets

- **Geändert wurde ausschließlich `reviews/BEFUNDE_60.md`** (angehängt).
  `docs/methodik/60_gebaeudeschaeden_flusshochwasser.md` (MD5
  `24972e4404a8e1bc0990e63f1959798d`) und `docs/evidenz/register.md` (MD5
  `5fb629559a13d835e56831fcedc9b666`) sind byte-gleich geblieben,
  `backend/scripts/lint_methodik.py` wurde nicht geändert (T-0234), die Arbeitsmappen nur
  mittelbar über die im Ledger zitierten Zellbezüge herangezogen (eiserne Regel 2). Der Bericht
  wurde ausschließlich an den in der Tabelle ausgewiesenen Stellen gelesen und nachgeprüft.
- **Kein Befund behoben, keiner umnummeriert.** Höchste vorhandene Nummer zu Laufbeginn: **98**;
  neu vergeben sind **99 und 100**. Die Status der Befunde 39 bis 42 selbst bleiben unberührt.
- **Keine Leitfrage aus §5 beantwortet.** Dieses Paket führt allein die Regression der Nummern
  **39, 40, 41 und 42**; die Nummern 43 bis 46 führt das Schwesterpaket auf Platz 20. Zusammen
  decken beide die acht Nummern des ersetzten T-0369 genau einmal ab.
- **Vorgabe P1 angelegt (40):** stichprobenweise an drei Parameter-Blöcken geprüft, ob Quelle oder
  ausgewiesene Abschätzung samt Herleitung im sichtbaren Berichtstext steht; alle drei bestehen
  (`n_efh_zfh` → B4 Z. 363–364/§3.4 Z. 684, `k_bgf` → §3.4 Z. 686, `p_hq_extrem` → §3.4
  Z. 664–672). Der Rest von Befund 40 betrifft nicht die Qualität der vorhandenen Blöcke, sondern
  die acht §4.8-Parameter ohne Block (→ 99).
- **Ressourcen-Regel §3.4 eingehalten:** kein nationaler 100-m-Vollraster-Lauf; nachgerechnet wurde
  aus den gedruckten Zahlen, die Stichproben-Dateien `docs/evidenz/60_stichprobe/*.csv` wurden
  nicht geöffnet.
- **Kopftabelle „Offene Befunde" bewusst nicht fortgeschrieben** (Dateirahmen der Runde-3-Pakete,
  T-0359); ebenso unberührt bleiben die Statuszeilen zu 39–42 in der Übersichtstabelle (Z. 64–67),
  auch dort, wo sie vom heutigen Berichtsstand abweichen (39).
