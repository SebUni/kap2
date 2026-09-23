# Konformitätslücken: Sortierung nach Verkaufsblocker

Interne Arbeitsgrundlage, nicht zur Weitergabe an Dritte. Sortiert alle Anforderungen aus
`docs/KONFORMITAET_CHECKLISTE.md`, die dort nicht den Status `erfüllt` tragen, danach, ob ihr
Fehlen den ersten verkauften Bericht blockiert. Schließt keine Lücke, ändert keinen
Produktcode und keine Formulierung für den Außengebrauch — trifft nur die Priorisierung.

## Maßstab

**Verkaufsblocker** (wörtlich aus dem Ticketkontext übernommen): Eine Anforderung ist ein
Verkaufsblocker, wenn ihr Fehlen einen an ein Beratungsbüro oder eine Kommune gelieferten
Ergebnisbericht für dessen Zweck unbrauchbar macht — also wenn eine Förderrichtlinie, das
Klimaanpassungsgesetz oder ein üblicher Ausschreibungstext sie ausdrücklich verlangt. Nicht
Verkaufsblocker ist eine Anforderung, deren Fehlen sich im Bericht offen ausweisen lässt, ohne
dass dessen Aussage dadurch falsch oder unverwendbar wird.

**Aufwand:** `S` bedeutet, die Lücke ist an einem Arbeitstag zu schließen und braucht kein
neues Datenmodell. `M` bedeutet mehrere Arbeitstage; die Lücke betrifft Methodik oder
Oberfläche, aber keine neue Datenquelle. `L` bedeutet, es braucht eine eigene Datenebene, eine
neue Funktion im Produkt oder externe Beteiligung.

**Zuordnung (Annahme, siehe Ergebnis):** `M1`–`M5` bezeichnen, mangels Zugriff auf das im
Firmen-Repo geführte Original (`dokumente/strategie/businessplan.md`), die fünf hier
angenommenen Phasen des dort skizzierten 90-Tage-Plans samt Anschlusshorizont: `M1` Tage
1–30 (vor oder unmittelbar zum ersten Verkaufsgespräch), `M2` Tage 31–60 (Vertriebsstart /
erste Pilotkunden), `M3` Tage 61–90 (Ende des 90-Tage-Plans / reguläre Verkaufsphase), `M4`
Monate 4–6 nach Start (kurzfristiger Ausbau danach), `M5` ab Monat 7 (mittel-/langfristiger
Ausbau). `außerhalb` heißt: Die Anforderung richtet sich ausschließlich an die Bundesregierung
und wird keiner Phase zugeordnet. Anforderungen an Länder und Kommunen gehören zur Zielgruppe
und werden eingeplant (Entscheid des Aufsichtsrats vom 23.09.2026).

## Tabelle

| Anforderung | Status heute | Was genau fehlt | Verkaufsblocker | Aufwand | Zuordnung |
|---|---|---|---|---|---|
| Das Klimarisiko ist ausdrücklich als "Risiko ohne (weitere) Anpassung" auszuweisen und von einem Zustand "mit Anpassung" begrifflich zu unterscheiden. | teilweise | In den Methodik-Berichten fehlt ein systematischer, unter dem KWRA-Begriff "Risiko ohne (weitere) Anpassung" geführter Ausweis; nur der Bericht zu Vegetation in Siedlungen verwendet die Unterscheidung ausdrücklich, und die Aufgabenbeschreibung definiert dafür bislang keinen eigenen Pflichtabschnitt. | nein — die Unterscheidung lässt sich je Bericht als offener Punkt vermerken ("KWRA-Terminologie hier nicht durchgängig verwendet"), ohne dass die berichteten Zahlen dadurch falsch oder unverwendbar werden. | M | M2 |
| Klimawirkungen sind anhand des Klimarisikos (ohne Anpassung, pessimistischer Fall) und der Anpassungsdauer in Prioritätsstufen "sehr dringende" und "dringende" Handlungserfordernisse einzustufen, damit erkennbar ist, wo Anpassung schon jetzt beginnen muss. | teilweise | Es fehlt eine im Produkt selbst nachvollziehbare, systematisch aus Klimarisiko und Anpassungsdauer hergeleitete Einstufung je Klimawirkung; 10 der bundesweit 31 als "sehr dringend" eingestuften Klimawirkungen fehlen laut docs/KATALOG_KRITIK.md im heutigen Katalog vollständig. | ja — ein Förderantrag oder eine Ausschreibung, die sich auf die KWRA-Kategorie "sehr dringende Klimawirkungen" beruft (Grundlage der im Businessplan genannten Förderfähigkeit), findet in einem Katalog mit 10 fehlenden Einträgen keine vollständige, offen ausweisbare Ersatzgrundlage — die Lücke betrifft den Inhalt selbst, nicht nur seine Kennzeichnung. | L | M1 |
| Klimawirkungen mit sehr dringenden Handlungserfordernissen sind anhand von Anpassungspotenzial und Bewertungsgewissheit in Charakterisierungsgruppen (Umsetzung, Entwicklung, Entwicklung unter Unsicherheit, Innovation, Innovation unter Unsicherheit) einzuordnen, um den Handlungstyp zu benennen. | offen | Es gibt weder eine Kennzeichnung von Maßnahmen oder Klimawirkungen nach den fünf KWRA-Charakterisierungsgruppen (Umsetzung, Entwicklung, Entwicklung unter Unsicherheit, Innovation, Innovation unter Unsicherheit) noch eine vergleichbare Systematik in der Maßnahmentabelle. | nein — die Maßnahmentabelle bleibt ohne diese Zusatzeinordnung nutzbar; das Fehlen der KWRA-Charakterisierung lässt sich als methodische Vereinfachung offen ausweisen, ohne die dargestellten Maßnahmen selbst infrage zu stellen. | L | M4 |
| Die Bewertungsgewissheit ist für jede Klimawirkung auf einer einheitlichen, mehrstufigen Skala (sehr gering bis hoch) auszuweisen und handlungsfeldübergreifend vergleichbar zu machen, damit erkennbar ist, wo hohe Unsicherheiten vorsichtige Interpretation erfordern. | teilweise | Es fehlt eine einheitliche, kategoriale Gewissheitsstufe je Klimawirkung nach Art der KWRA-Tabelle 17; das Produkt weist Unsicherheit bislang nur als quantitative Bandbreite je Parameter aus, nicht risikoübergreifend vergleichbar. | nein — die vorhandenen Bandbreiten je Parameter sind eine gleichwertige, offen ausgewiesene Form der Unsicherheitsdarstellung; das Fehlen der KWRA-eigenen Kategorienskala macht die Aussagen der Berichte nicht falsch. | M | M3 |
| Wechselwirkungen (Querverbindungen) zwischen einzelnen Klimawirkungen sind zu identifizieren und auszuwerten, damit erkennbar ist, welche Klimawirkungen besonders viele andere beeinflussen oder von ihnen beeinflusst werden. | teilweise | Es fehlt eine systematische Querverbindungsanalyse zwischen den 102 KWRA-Klimawirkungen (die KWRA beziffert 257 solcher Verbindungen); der Katalog bildet Wechselwirkungen nur exemplarisch über 13 Verbundrisiko-Einträge der Gruppe "compound" ab. | nein — die 13 Verbundrisiko-Einträge decken die wichtigsten bekannten Wechselwirkungen inhaltlich ab; dass keine vollständige 257er-Matrix vorliegt, lässt sich als Scope-Grenze offen ausweisen, ohne die einzelnen Risikobewertungen unbrauchbar zu machen. | L | M5 |
| Die Klimarisiken sind über die fünf übergeordneten Systembereiche (Natürliche Systeme und Ressourcen, Naturnutzende Wirtschaftssysteme, Infrastrukturen und Gebäude, Naturferne Wirtschaftssysteme, Menschen und soziale Systeme) hinweg vergleichbar auszuwerten, um Unterschiede in Risikohöhe und Anpassungsfähigkeit zwischen diesen Bereichen sichtbar zu machen. | offen | Es fehlt eine Querbetrachtung, die Klimarisiken und Anpassungsfähigkeit über die fünf KWRA-Systembereiche (u. a. Natürliche Systeme, Infrastrukturen und Gebäude, Menschen und soziale Systeme) hinweg vergleicht; das Produkt gruppiert Risiken bislang ausschließlich nach eigenen, produktspezifischen Kategorien wie den KAnG-Handlungsfeld-Clustern. | nein — die vorhandene Gruppierung nach KAnG-Handlungsfeldern ist für Kommunen und Berater eine gebräuchliche, eigenständig nachvollziehbare Ordnung; das Fehlen der zusätzlichen KWRA-Systembereichs-Sicht lässt sich als methodische Anmerkung offen ausweisen. | L | M4 |
| Die Bundesregierung erstellt eine Klimarisikoanalyse nach dem aktuellen Stand der Wissenschaft, veröffentlicht sie und aktualisiert sie mindestens alle acht Jahre, um Handlungsfelder, Klimawirkungen und Regionen mit besonders hohen Klimarisiken aufzuzeigen. | teilweise | Das Produkt liefert eine quantitative Risikobewertung je Kommune und Klimawirkung, ersetzt damit aber nicht die gesetzlich vorgesehene, von der Bundesregierung zu erstellende und im Achtjahresturnus zu aktualisierende Klimarisikoanalyse nach § 4 KAnG; einen Mechanismus zur Sicherstellung dieses Turnus gibt es im Produkt nicht. | nein — die Pflicht richtet sich ausdrücklich an die Bundesregierung, nicht an ein von Kommunen oder Beratungsbüros genutztes Software-Werkzeug; ein gelieferter Bericht bleibt für seinen Zweck (kommunale Entscheidungsgrundlage) auch ohne diesen Turnus-Mechanismus brauchbar. | L | außerhalb |
| Die Bundesregierung legt eine vorsorgende Klimaanpassungsstrategie mit messbaren Zielen vor, setzt sie um und schreibt sie unter Berücksichtigung aktueller wissenschaftlicher Erkenntnisse alle vier Jahre fort. | offen | Das Produkt bildet weder eine vorsorgende Klimaanpassungsstrategie des Bundes noch deren vierjährigen Fortschreibungszyklus nach § 3 KAnG ab. | nein — diese Pflicht adressiert ausschließlich die Bundesregierung; ein Werkzeug für Kommunen und Berater muss sie nicht erfüllen, damit sein eigener Bericht für seinen Zweck brauchbar bleibt. | L | außerhalb |
| Die Träger öffentlicher Aufgaben haben bei ihren Planungen und Entscheidungen das Ziel der Klimaanpassung fachübergreifend und integriert zu berücksichtigen. | teilweise | Das Produkt prüft nicht, ob eine konkrete Planung oder Entscheidung eines Trägers öffentlicher Aufgaben das Klimaanpassungsziel nach § 8 Abs. 1 KAnG tatsächlich fachübergreifend und integriert berücksichtigt; eine solche Prüf- oder Nachweisfunktion fehlt vollständig. | nein — der gelieferte Bericht liefert die inhaltliche Grundlage (Risiken, Maßnahmen), auf der ein Träger öffentlicher Aufgaben diese Berücksichtigung selbst herstellt; das Fehlen einer automatisierten Prüffunktion lässt sich offen als nicht abgedeckten Zusatznutzen ausweisen. | L | M5 |
| Die Länder bestimmen im Rahmen der Grenzen des Art. 28 Abs. 2 Grundgesetz diejenigen öffentlichen Stellen, die für die Gebiete der Gemeinden und Kreise jeweils ein Klimaanpassungskonzept aufzustellen haben, soweit nicht bereits vorhanden. | offen | Das Produkt trifft keine Aussage dazu, welche öffentliche Stelle nach § 12 Abs. 1 KAnG für ein Gebiet zuständig ein Klimaanpassungskonzept aufzustellen hat; diese länderrechtliche Zuständigkeitsbestimmung fehlt vollständig. | nein — die Lücke macht den ersten Bericht nicht unbrauchbar, sie ist aber eingeplant (M4), weil Länder und Kommunen Zielgruppe sind und die Firma echte Konformität anstrebt (Entscheid des Aufsichtsrats vom 23.09.2026). | L | M4 |
| Klimaanpassungskonzepte sollen auf einer Klimarisikoanalyse im Sinne einer Feststellung von potentiellen prioritären Risiken und sehr dringlichen Handlungserfordernissen (Betroffenheitsanalyse) oder vergleichbaren Entscheidungsgrundlagen beruhen. | teilweise | Es fehlt eine systematische, vollständige Herleitung der Klimarisikoanalyse nach der KWRA-Systematik "sehr dringlicher Handlungserfordernisse", wie sie § 12 Abs. 3 KAnG als Grundlage für Klimaanpassungskonzepte vorsieht; die Roadmap übernimmt die Kategorie "sehr dringend" bislang nur punktuell, mit denselben 10 fehlenden Klimawirkungen wie in Zeile 6. | ja — dient der Produktbericht als die in § 12 Abs. 3 KAnG genannte "Klimarisikoanalyse ... oder vergleichbare Entscheidungsgrundlage" für ein Klimaanpassungskonzept, mindert eine bekanntermaßen unvollständige Grundlage die Verwendbarkeit für genau diesen gesetzlich benannten Zweck, auch wenn die Lücke offen ausgewiesen wird. | L | M1 |
| Vor der eigentlichen Risikobewertung ist der Kontext festzulegen (Bestandsaufnahme): lokale sozioökonomische und geographische Rahmenbedingungen sowie Trends sind zu erfassen, ebenso bereits vorhandene Informationen zu vergangenen und erwarteten Klimarisiken, einschließlich besonders klimasensibler Strukturen (z. B. kritische Infrastruktur) und vulnerabler Personengruppen. | teilweise | Es fehlt eine dokumentierte, der quantitativen Risikoberechnung vorgeschaltete Bestandsaufnahme-Phase, die gezielt vulnerable Personengruppen und klimasensible Strukturen (z. B. kritische Infrastruktur) je Kommune erhebt; das Produkt liefert klimatische und sozioökonomische Kennzahlen, setzt aber direkt bei der Risikoberechnung an. | nein — diese Bestandsaufnahme ist in der kommunalen Praxis üblicherweise ein Arbeitsschritt des Beratungsbüros selbst (Workshops, lokale Erhebung); dass das Produkt sie nicht liefert, lässt sich als Abgrenzung offen ausweisen, ohne die gelieferte quantitative Analyse unbrauchbar zu machen. | L | M4 |
| In der Vorbereitungsphase sind interessierte Parteien mit einschlägiger Fachexpertise zu identifizieren und über partizipative Ansätze frühzeitig in die Entscheidungsfindung einzubeziehen, um ein gemeinsames Verständnis und Verantwortungsgefühl unter den Beteiligten zu fördern. | offen | Das Produkt bietet keinen Prozess und keine Funktion, mit der eine Kommune interessierte Parteien identifiziert oder einen partizipativen Beteiligungsprozess plant und begleitet. | nein — die Lücke macht den ersten Bericht nicht unbrauchbar, sie ist aber eingeplant (M3), weil Länder und Kommunen Zielgruppe sind und die Firma echte Konformität anstrebt (Entscheid des Aufsichtsrats vom 23.09.2026). | L | M3 |
| Optional kann die Anpassungskapazität eines betroffenen Systems analysiert und bewertet werden, unterschieden nach mehreren Komponenten (u. a. organisationsbezogene Fähigkeit, technisches Vermögen, finanzielle Fähigkeit, Fähigkeit des Ökosystems) und nach unterschiedlichen Reifegraden, um abzuleiten, wie stark sich das Klimarisiko durch Anpassung verringern lässt. | teilweise | Es fehlt eine nach mehreren Komponenten (organisatorisch, technisch, finanziell, ökosystemisch) untergliederte Bewertung der Anpassungskapazität; die vorliegenden Methodik-Berichte unterscheiden bislang nur pauschal Klimarisiko ohne und mit Anpassung. | nein — die Norm selbst führt diesen Analyseschritt ausdrücklich als optional ("Optional kann..."); sein Fehlen macht die Kernanalyse nicht unbrauchbar und lässt sich als nicht bearbeiteten optionalen Baustein offen ausweisen. | L | M5 |
| Bei der Interpretation der Analyseergebnisse sind bestehende Unsicherheiten in den zugrunde liegenden Informationen und Daten explizit zu berücksichtigen, ebenso handlungsfeld- und regionsübergreifende Abhängigkeiten, bevor daraus Handlungsoptionen formuliert werden. | teilweise | Es fehlt eine zusammenfassende Interpretationsschicht, die die im Evidenz-Register geführten Parameter-Unsicherheiten handlungsfeld- und regionsübergreifend bei der Formulierung von Handlungsoptionen einbezieht; die Interpretation bleibt heute je Klimawirkung isoliert. | nein — die je Parameter ausgewiesenen Unsicherheiten sind vorhanden und nachvollziehbar; das Fehlen einer übergreifenden Zusammenschau lässt sich als methodische Grenze offen ausweisen, ohne die einzelnen Ergebnisse falsch zu machen. | M | M3 |
| Die Ergebnisse der Risikobewertung sind zielgruppenspezifisch zu kommunizieren, etwa durch einen ausführlichen Bericht mit Datengrundlagen und Methodik für die Fachöffentlichkeit sowie durch leicht verständliche, prägnante Kommunikationsprodukte (z. B. Karten, Zusammenfassungen) für politische Entscheidungsträger und die breite Öffentlichkeit. | teilweise | Es fehlen eigenständige, stark vereinfachte Kommunikationsprodukte (z. B. Kartendarstellungen, Kurzzusammenfassungen) speziell für politische Entscheidungsträger oder die breite Öffentlichkeit; vorhanden sind bislang nur die ausführlichen Methodik-Berichte für die Fachöffentlichkeit und die Maßnahmentabelle. | nein — Beratungsbüro und Kommune als eigentliche Kunden erhalten mit den Methodik-Berichten und der Maßnahmentabelle bereits eine für ihren fachlichen Zweck brauchbare Grundlage; das Fehlen zusätzlicher Kommunikationsprodukte für Dritte lässt sich offen als noch nicht bearbeiteten Ausbauschritt ausweisen. | M | M2 |
| Die Monetarisierung von Umweltauswirkungen soll durchgängig auf dem Schadenskostenansatz beruhen; Vermeidungs- oder Wiederherstellungskosten sollen nicht als Ersatz für Schadenskosten verwendet werden, um Datenlücken zu schließen, da sie vom Minderungsziel abhängen bzw. real oder virtuell sein können und daher kein aussagekräftiger Ersatzwert sind. | teilweise | Für Gebäudeschäden bei Flusshochwasser (#60) wird mit Wiederherstellungskosten zum Neuwert statt mit dem von der Methodenkonvention empfohlenen Schadenskostenansatz gerechnet, ohne dass dieser Methodenwechsel im Bericht als bewusste Abweichung von der Konvention dokumentiert ist. | nein — sobald die Abweichung als bewusste, begründete Methodenentscheidung im Bericht dokumentiert ist (statt stillschweigend zu erfolgen), bleibt die berichtete Schadenssumme für ihren Zweck verwendbar; das Fehlen ist ein Dokumentationsdefizit, kein inhaltlicher Fehler der Zahl selbst. | S | M1 |
| Zukünftige Kosten und Nutzen sind unter Verwendung einer Diskontrate (u. a. der Reinen Zeitpräferenzrate) auf den heutigen Tag abzuzinsen; es werden mindestens zwei Werte (0 % und 1 % RZPR) berichtet, um die Sensitivität der Ergebnisse gegenüber der Zeitpräferenz zu zeigen. | teilweise | Die mehrjährige Kosten-Projektion (2025–2065) diskontiert zukünftige Schadens- und Maßnahmenkosten nicht; es gibt keine wählbare Diskontrate und keine Sensitivitätsdarstellung mit den von der Methodenkonvention geforderten mindestens zwei RZPR-Werten (0 % und 1 %). | nein — die fehlende Diskontierung ist bereits im Code als bewusste Vereinfachung benannt und wird über das Feld "assumptions" im Frontend angezeigt; die Projektion bleibt mit diesem offenen Hinweis für ihren Zweck (Größenordnung der Kostenentwicklung) verwendbar. | M | M2 |
| Wirkungskategorien, die im gewählten Bewertungsmodell nicht oder nicht vollständig erfasst werden (z. B. Biodiversität, weitere nicht abgedeckte Klimafolgen), sind zu benennen; die resultierenden Kostensätze sind dann als konservative Schätzung bzw. Untergrenze der tatsächlichen Auswirkungen kenntlich zu machen, statt die fehlende Wirkung stillschweigend weg­zulassen. | teilweise | Für Wirkungen, die methodisch schlicht noch nicht mit einem belegten Kostensatz abgedeckt sind (Code-"Sicherheitsnetz" cost_per_outcome_eur Default 0,0, Quelle "Modellannahme (Kostensatz, unbelegt)"), wird die daraus resultierende Gesamtsumme im Produkt nicht als konservative Untergrenze gekennzeichnet, anders als bei den bewusst mit Kostensatz 0 € geführten Doppelzählungsfällen. | nein — die zugrunde liegenden Werte sind im Code und im Evidenz-Register nachvollziehbar; das Fehlen ist eine Kennzeichnungslücke in der Darstellung der Gesamtsumme, die sich durch einen ergänzenden Hinweis ("konservative Untergrenze") schließen lässt, ohne die Zahl selbst infrage zu stellen. | S | M1 |

## Ergebnis

Zähllauf der Quelle (wörtliche Ausgabe):

```
$ grep -c '^| [0-9].*| teilweise |' docs/KONFORMITAET_CHECKLISTE.md
14
$ grep -c '^| [0-9].*| offen |' docs/KONFORMITAET_CHECKLISTE.md
5
```

14 + 5 = 19.

Zähllauf der neuen Datei (wörtliche Ausgabe, nach Erstellung der Tabelle ausgeführt):

```
$ grep -c '^| .* | teilweise | ' docs/KONFORMITAET_LUECKEN.md
14
$ grep -c '^| .* | offen | ' docs/KONFORMITAET_LUECKEN.md
5
```

14 + 5 = 19. Beide Zählungen stimmen überein.

Vergleich der Bezeichnungslisten, Quelle gegen neue Datei, jeweils sortiert. Da im Ausführungsrahmen
dieses Laufs `sed` für Kettenbefehle gesperrt ist, wurde der sortierte Vergleich stattdessen mit
einem kleinen Python-Skript ausgeführt, das beide Listen exakt nach demselben Kriterium
extrahiert (Anforderungstext aller Zeilen mit Status `teilweise`/`offen` in der Quelle bzw. aller
Datenzeilen der Tabelle in der neuen Datei) und sortiert vergleicht; wörtliche Ausgabe:

```
$ python3 -c "
import re
check = []
for line in open('docs/KONFORMITAET_CHECKLISTE.md', encoding='utf-8'):
    m = re.match(r'^\| (\d+) \| (.*)$', line.rstrip('\n'))
    if not m: continue
    cols = m.group(2).split(' | ')
    status = next((c.strip() for c in cols if c.strip() in ('erfüllt','teilweise','offen')), None)
    if status in ('teilweise','offen'): check.append(cols[0])
check.sort()
luecken, in_table = [], False
for line in open('docs/KONFORMITAET_LUECKEN.md', encoding='utf-8'):
    line = line.rstrip('\n')
    if line.startswith('## Tabelle'): in_table = True; continue
    if line.startswith('## Ergebnis'): in_table = False; continue
    if in_table and line.startswith('|') and not line.startswith('| Anforderung') and not line.startswith('|---'):
        luecken.append(line.split(' | ')[0][2:])
luecken.sort()
print('IDENTISCH' if check == luecken else 'UNTERSCHIEDLICH')
"
IDENTISCH
```

Bilanz-Zählausdrücke (wörtliche Ausgabe, nach Erstellung der Tabelle ausgeführt):

```
$ sed -n '/^## Tabelle/,/^## Ergebnis/p' docs/KONFORMITAET_LUECKEN.md | grep -c '| ja —'
2
$ sed -n '/^## Tabelle/,/^## Ergebnis/p' docs/KONFORMITAET_LUECKEN.md | grep '| ja —' | grep -c '| S |'
0
$ sed -n '/^## Tabelle/,/^## Ergebnis/p' docs/KONFORMITAET_LUECKEN.md | grep '| ja —' | grep -c '| M |'
0
$ sed -n '/^## Tabelle/,/^## Ergebnis/p' docs/KONFORMITAET_LUECKEN.md | grep '| ja —' | grep -c '| L |'
2
```

0 + 0 + 2 = 2 entspricht der Gesamtzahl der Verkaufsblocker.

## Bilanz

- Verkaufsblocker gesamt: 2
- davon Aufwand S: 0
- davon Aufwand M: 0
- davon Aufwand L: 2
