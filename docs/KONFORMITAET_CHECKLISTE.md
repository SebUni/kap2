# Konformitäts-Checkliste: KAP2 gegen KWRA 2021

Interne Arbeitsgrundlage. Kein Konformitätsclaim nach außen ohne Freigabe des Aufsichtsrats.

Diese Checkliste stellt Anforderungen aus der Klimawirkungs- und Risikoanalyse 2021 für
Deutschland (Quelle: KWRA 2021, Fundstelle-Datei
`kwra2021_teilbericht_1_grundlagen_bf_211027_0.pdf`) den entsprechenden Umsetzungen im
Produkt gegenüber. Sie entsteht paketweise (T-0344); dieses Paket trägt die Zeilen 1–5.
Zeilen 6–25 sind eigene, spätere Pakete und werden hier nicht vorweggenommen.

## Tabelle

| Nr | Anforderung | Quelle | Fundstelle | Status | Beleg im Produkt | Lücke |
|---|---|---|---|---|---|---|
| 1 | Das Klimarisiko ist über Klimawirkungsketten herzuleiten, die klimatischen Einfluss, Sensitivität und räumliche Exposition als benannte, unterscheidbare Komponenten abbilden. | KWRA 2021 | kwra2021_teilbericht_1_grundlagen_bf_211027_0.pdf, Kap. 2.1.4.1 | erfüllt | docs/methodik/95_hitzebelastung.md, docs/methodik/61_vegetation_in_siedlungen.md | — |
| 2 | Das Klimarisiko ist ausdrücklich als "Risiko ohne (weitere) Anpassung" auszuweisen und von einem Zustand "mit Anpassung" begrifflich zu unterscheiden. | KWRA 2021 | kwra2021_teilbericht_1_grundlagen_bf_211027_0.pdf, Kap. 2.1.4.1 | teilweise | docs/methodik/61_vegetation_in_siedlungen.md | Nur der Methodik-Bericht zu Vegetation in Siedlungen weist einen Vergleichswert "ohne Anpassung" explizit in KWRA-Terminologie aus. Für die übrigen vorliegenden Methodik-Berichte fehlt ein systematischer, unter diesem Begriff geführter Ausweis; die Aufgabenbeschreibung (docs/AUFGABE_METHODIK_SCHADENSRECHNUNG.md) definiert die Unterscheidung "ohne Anpassung"/"mit Anpassung" bislang nicht als eigenen Pflichtabschnitt. |
| 3 | Für jeden in die Bewertung eingehenden Parameter beziehungsweise Faktor ist die zugrunde gelegte Quelle offenzulegen und zu dokumentieren; ist keine Quelle vorhanden, ist die Abschätzung als solche kenntlich zu machen. | KWRA 2021 | kwra2021_teilbericht_1_grundlagen_bf_211027_0.pdf, Kap. 2.1.3 (S. 42, Tabelle 3) und Kap. 1.3 (S. 34) | erfüllt | docs/evidenz/register.md, docs/methodik/95_hitzebelastung.md | — |
| 4 | Sensitivität (Anfälligkeit eines Systems gegenüber einem klimatischen Einfluss) und räumliche Exposition (Vorhandensein potenziell betroffener Systemelemente) sind begrifflich und methodisch getrennt zu führen, nicht zu vermischen. | KWRA 2021 | kwra2021_teilbericht_1_grundlagen_bf_211027_0.pdf, Kap. 2.1.4.1 (S. 44) | erfüllt | docs/methodik/95_hitzebelastung.md | — |
| 5 | Die Analyse muss ihre methodischen Grenzen und ihren Anwendungsbereich explizit benennen, insbesondere dass sie keine detailliertere lokale oder sektorale Risikoanalyse ersetzt. | KWRA 2021 | kwra2021_teilbericht_1_grundlagen_bf_211027_0.pdf, Kap. 1.4 (S. 35) | erfüllt | docs/methodik/95_hitzebelastung.md, docs/methodik/60_gebaeudeschaeden_flusshochwasser.md | — |
| 6 | Klimawirkungen sind anhand des Klimarisikos (ohne Anpassung, pessimistischer Fall) und der Anpassungsdauer in Prioritätsstufen "sehr dringende" und "dringende" Handlungserfordernisse einzustufen, damit erkennbar ist, wo Anpassung schon jetzt beginnen muss. | KWRA 2021 | kwra2021_teilbericht_6_integrierte_auswertung_bf_211027_0.pdf, Kap. 6.1 (S. 136–140) | teilweise | frontend/src/pages/roadmap/roadmapData.ts, docs/KATALOG_KRITIK.md | Die Produkt-Roadmap übernimmt die KWRA-Kategorie "sehr dringende Klimawirkungen" wörtlich, um die Ausbaureihenfolge zu begründen (zuerst die drei sehr dringenden Gesundheits-Klimawirkungen, danach 15 weitere). Es gibt aber keine im Produkt selbst nachvollziehbare, aus Klimarisiko und Anpassungsdauer hergeleitete Einstufung je Klimawirkung, und laut docs/KATALOG_KRITIK.md sind 10 der bundesweit 31 "sehr dringenden" Klimawirkungen im heutigen Katalog nicht abgebildet, weil sie ausgewählt statt systematisch aus der KWRA-Einstufung hergeleitet wurden. |
| 7 | Klimawirkungen mit sehr dringenden Handlungserfordernissen sind anhand von Anpassungspotenzial und Bewertungsgewissheit in Charakterisierungsgruppen (Umsetzung, Entwicklung, Entwicklung unter Unsicherheit, Innovation, Innovation unter Unsicherheit) einzuordnen, um den Handlungstyp zu benennen. | KWRA 2021 | kwra2021_teilbericht_6_integrierte_auswertung_bf_211027_0.pdf, Kap. 6.2 (S. 140–145) | teilweise | backend/app/services/charakterisierung.py, backend/app/services/gewissheit.py, backend/app/api/routes/catalog.py, backend/tests/test_charakterisierungsgruppen.py | Die fünf Gruppen und eine dokumentierte Entscheidungstabelle sind vorhanden, die Schwellen sind nach P1 als Abschätzung von KAP3 ausgewiesen. Es fehlt aber, was die Einordnung nach Kap. 6.2 trägt: Beschlossene und weiterreichende Maßnahmen werden nicht getrennt, und es gibt keinen optimistischen und pessimistischen Fall. „Innovation“ heißt im Produkt nur, dass der Katalog keinen verknüpften Hebel ab 10 % hat, nicht, dass auch alle Maßnahmen das Ziel verfehlen. Die Gewissheit enthält nicht die Gewissheit der Anpassungskapazität. Die Ausnahme der KWRA für die Allergien (Bewertung auf Basis der beschlossenen Maßnahmen, Fn. 28/29) fehlt, ebenso eine gerechnete Sensitivität der Zuordnung und das Handlungserfordernis je Gruppe. Eingeordnet wird jeder Katalogcode, nicht nur die sehr dringenden. Ergebnis: Nur #95 Hitzebelastung liegt wie in Tabelle 27 in „Entwicklung“. #96 Aeroallergene (KWRA „Umsetzung“) und #98 UV-Schädigungen (KWRA „Entwicklung“) landen mit Anpassungspotenzial 0 in „Innovation“, weil keine Maßnahme im Rechenweg wirkt: Die Pollen-Frühwarnung ist nur qualitativ verknüpft, für UV gibt es keine Maßnahme. Die Modellgrenze der API nennt diese Ursache nicht. Einzelnachweis: Abschnitt „Gegenprobe Zeile 7“. |
| 8 | Die Bewertungsgewissheit ist für jede Klimawirkung auf einer einheitlichen, mehrstufigen Skala (sehr gering bis hoch) auszuweisen und handlungsfeldübergreifend vergleichbar zu machen, damit erkennbar ist, wo hohe Unsicherheiten vorsichtige Interpretation erfordern. | KWRA 2021 | kwra2021_teilbericht_6_integrierte_auswertung_bf_211027_0.pdf, Kap. 3.3 (S. 78–82) | teilweise | backend/app/services/gewissheit.py, backend/app/api/routes/catalog.py, backend/tests/test_gewissheitsstufe.py | Die Skala stimmt: Jede Klimawirkung des Katalogs trägt eine Stufe auf der vierstufigen Skala der KWRA (sehr gering, gering, mittel, hoch), gebildet nach derselben dokumentierten Regel. Die Herleitung passt aber nicht. Die KWRA bewertet die Gewissheit je Zeitscheibe (Mitte und Ende des Jahrhunderts) aus fünf Teilaspekten: Vorhandensein und Zuverlässigkeit der Daten, Kenntnis der Wirkzusammenhänge, Genauigkeit und Plausibilität der Modellannahmen, Eindeutigkeit der Trends. Das Produkt misst nur den Anteil der Rechenparameter mit Evidenzklasse „belegt“, ohne Zeitscheibe. Damit misst es die Quellenlage der Rechnung, nicht die Gewissheit des Klimarisikos, und widerspricht der KWRA bei den eigenen Klimawirkungen: #98 UV-Schädigungen steht im Produkt auf „hoch“, bei der KWRA zum Ende des Jahrhunderts auf „sehr gering“; ein einziger abgeschätzter Parameter senkt #95 Hitzebelastung (Mortalität) auf „mittel“. Es fehlen zudem die Mittelung je Handlungsfeld und Cluster mit Grad (Tabelle 17), die Änderung zwischen den Zeitscheiben, der Bezug zur Höhe des Klimarisikos (Abbildung 7) und ein handlungsfeldübergreifender Vergleich: Der aktive Katalog hat nur das Handlungsfeld „Menschliche Gesundheit“. Einzelnachweis: Abschnitt „Gegenprobe Zeile 8“. |
| 9 | Wechselwirkungen (Querverbindungen) zwischen einzelnen Klimawirkungen sind zu identifizieren und auszuwerten, damit erkennbar ist, welche Klimawirkungen besonders viele andere beeinflussen oder von ihnen beeinflusst werden. | KWRA 2021 | kwra2021_teilbericht_6_integrierte_auswertung_bf_211027_0.pdf, Kap. 3.4 (S. 82–89) | teilweise | backend/app/data/kwra_querverbindungen.py, backend/app/services/querverbindungen.py, docs/QUERVERBINDUNGEN_KLIMAWIRKUNGEN.md, frontend/src/components/dashboard/RiskInteractionSection.tsx | Das Produkt übernimmt Ergebnisse der KWRA-Querverbindungsanalyse (Kennzahlen, 25 Netzrollen, 20 im Fließtext genannte Beziehungen, Systembereichs-Matrix aus Kap. 7), führt die Analyse aber nicht selbst: keine eigene Identifikation der Querbezüge und kein Abgleich mit den Klimawirkungsketten (UBA 2016); keine Darstellung der Querverbindungen zwischen den 13 Handlungsfeldern (Abb. 8); keine gegenseitigen Wechselwirkungen und kein Rückkopplungskreislauf Hitzebelastung – Bedarf an Kühlenergie – Stadtklima/Wärmeinseln (Abb. 9), obwohl Hitzebelastung und Stadtklima im Katalog stehen; keine gesonderte Auswertung der hoch bewerteten Klimawirkungen; die Netzrolle ist einwertig, obwohl eine Klimawirkung Sender und Empfänger zugleich sein kann. Die Dashboard-Tabelle zeigt nur Klimawirkungen des Katalogs, 13 der 25 Netzrollen – darunter Hochwasser, die zentrale Klimawirkung – erscheinen dort nicht. Einzelnachweis: Abschnitt „Gegenprobe Zeile 9“. |
| 10 | Die Klimarisiken sind über die fünf übergeordneten Systembereiche (Natürliche Systeme und Ressourcen, Naturnutzende Wirtschaftssysteme, Infrastrukturen und Gebäude, Naturferne Wirtschaftssysteme, Menschen und soziale Systeme) hinweg vergleichbar auszuwerten, um Unterschiede in Risikohöhe und Anpassungsfähigkeit zwischen diesen Bereichen sichtbar zu machen. | KWRA 2021 | kwra2021_teilbericht_6_integrierte_auswertung_bf_211027_0.pdf, Kap. 7 (S. 146–155) | teilweise | backend/app/data/catalog.py, backend/app/services/systembereiche.py, backend/tests/test_systembereiche.py, backend/app/data/kwra_querverbindungen.py | Die fünf KWRA-Systembereiche und die Querverbindungen zwischen ihnen (Tabelle 28) sind quellenfest vorhanden, der Vergleich selbst nicht: Alle drei gerechneten Klimawirkungen (#95, #96, #98) liegen in „Menschen und soziale Systeme“, die vier übrigen Bereiche bleiben leer, und die 49 Klimawirkungen der Roadmap tragen keinen Systembereich. Die Risikohöhe wird als Mittel des Produkt-Risikoindex verglichen, nicht wie in Kap. 7 als Anteil der hoch bewerteten Klimawirkungen je Zeitscheibe und Fall. Die Anpassungsfähigkeit — Wirksamkeit beschlossener und weiterreichender Anpassung, Klimarisiko mit Anpassung, Anpassungsdauer, Grenzen der Anpassung — wird je Bereich weder ermittelt noch verglichen, ebenso wenig Gewissheit, maßgebliche klimatische Einflüsse und Zahl der sehr dringenden und dringenden Handlungserfordernisse; die Schlüsse für die Anpassungsplanung (S. 153–154) fehlen. `systembereich_auswertung()` wird außer im Test nirgends aufgerufen. Einzelnachweis: Abschnitt „Gegenprobe Zeile 10“. |
| 11 | Die Bundesregierung erstellt eine Klimarisikoanalyse nach dem aktuellen Stand der Wissenschaft, veröffentlicht sie und aktualisiert sie mindestens alle acht Jahre, um Handlungsfelder, Klimawirkungen und Regionen mit besonders hohen Klimarisiken aufzuzeigen. | KAnG, https://www.gesetze-im-internet.de/kang/__4.html | § 4 Abs. 1 | teilweise | docs/methodik/95_hitzebelastung.md, backend/app/data/catalog.py | Das Produkt liefert eine quantitative Risikobewertung je Kommune und Klimawirkung (Methodik-Berichte, Katalog), das ist aber keine Klimarisikoanalyse der Bundesregierung im Sinne des § 4 KAnG und enthält keinen eingebauten Mechanismus, der eine Aktualisierung im gesetzlich vorgesehenen Achtjahresturnus sicherstellt oder dokumentiert. |
| 12 | Die Bundesregierung legt eine vorsorgende Klimaanpassungsstrategie mit messbaren Zielen vor, setzt sie um und schreibt sie unter Berücksichtigung aktueller wissenschaftlicher Erkenntnisse alle vier Jahre fort. | KAnG, https://www.gesetze-im-internet.de/kang/__3.html | § 3 Abs. 1 | offen | — | Das Produkt ist ein Werkzeug für Kommunen und Berater und bildet weder eine Bundesstrategie noch einen Fortschreibungszyklus ab; die Pflicht richtet sich an die Bundesregierung und wird vom Produkt nicht adressiert. |
| 13 | Die Träger öffentlicher Aufgaben haben bei ihren Planungen und Entscheidungen das Ziel der Klimaanpassung fachübergreifend und integriert zu berücksichtigen. | KAnG, https://www.gesetze-im-internet.de/kang/__8.html | § 8 Abs. 1 | teilweise | backend/app/data/kang_handlungsfelder.py, backend/app/services/kang_beruecksichtigung.py, backend/app/services/kang_nachweis_markdown.py, docs/NACHWEIS_FACHUEBERGREIFEND_KANG.md | Fachübergreifend nur dem Raster nach: Alle aktiven Klimawirkungen liegen im Handlungsfeld Gesundheit, die übrigen 16 Felder stehen immer auf „nicht betroffen“; keine Maßnahme des Katalogs wirkt über mehr als ein Handlungsfeld („integriert“ bleibt leer); die in § 8 Abs. 1 Satz 2 Nr. 1–3 genannten Auswirkungen (Überflutung, Grundwasser und Trockenheit, Bodenerosion) sind nur geplant, nicht gerechnet; die Erzeugung oder Verstärkung einer Wärmeinsel durch eine Planung wird nicht verglichen; eingetretene und zu erwartende Auswirkungen trennt der Nachweis nicht; der Erhalt von Versickerungs-, Speicher- und Verdunstungsflächen (Satz 3) wird nicht erfasst. Einzelnachweis: Abschnitt „Gegenprobe Zeile 13“ |
| 14 | Die Länder bestimmen im Rahmen der Grenzen des Art. 28 Abs. 2 Grundgesetz diejenigen öffentlichen Stellen, die für die Gebiete der Gemeinden und Kreise jeweils ein Klimaanpassungskonzept aufzustellen haben, soweit nicht bereits vorhanden. | KAnG, https://www.gesetze-im-internet.de/kang/__12.html | § 12 Abs. 1 | erfüllt | docs/KANG_ZUSTAENDIGKEIT_LAENDER.md, backend/app/data/kang_zustaendigkeit.py, backend/app/api/routes/kommune.py, frontend/src/components/dashboard/KangZustaendigkeit.tsx | — |
| 15 | Klimaanpassungskonzepte sollen auf einer Klimarisikoanalyse im Sinne einer Feststellung von potentiellen prioritären Risiken und sehr dringlichen Handlungserfordernissen (Betroffenheitsanalyse) oder vergleichbaren Entscheidungsgrundlagen beruhen. | KAnG, https://www.gesetze-im-internet.de/kang/__12.html | § 12 Abs. 3 | teilweise | backend/app/data/catalog.py, frontend/src/pages/roadmap/roadmapData.ts | Wie bereits zu Zeile 6 festgehalten, übernimmt das Produkt die Kategorie "sehr dringend" punktuell in der Roadmap, ohne die zugrunde liegende Klimarisikoanalyse systematisch und vollständig nach dieser gesetzlichen Vorgabe herzuleiten; laut docs/KATALOG_KRITIK.md fehlen im heutigen Katalog Klimawirkungen, die bundesweit als sehr dringend eingestuft sind. |
| 16 | Vor der eigentlichen Risikobewertung ist der Kontext festzulegen (Bestandsaufnahme): lokale sozioökonomische und geographische Rahmenbedingungen sowie Trends sind zu erfassen, ebenso bereits vorhandene Informationen zu vergangenen und erwarteten Klimarisiken, einschließlich besonders klimasensibler Strukturen (z. B. kritische Infrastruktur) und vulnerabler Personengruppen. | ISO 14091:2021, Sekundärquelle: Umweltbundesamt, "Klimarisikoanalysen auf kommunaler Ebene – Handlungsempfehlungen zur Umsetzung der ISO 14091", https://www.umweltbundesamt.de/publikationen/klimarisikoanalysen-auf-kommunaler-ebene | Kap. 5 (dort Abschnitt 2.1.2 "Bestandsaufnahme"/"Festlegung des Kontexts", S. 12) | erfüllt | backend/app/data/bestandsaufnahme.py, backend/app/services/bestandsaufnahme_service.py, backend/app/services/bestandsaufnahme_markdown.py, docs/BESTANDSAUFNAHME.md | Keine Lücke im Produkt; Größen ohne Datenquelle je Kommune weist die Bestandsaufnahme ausdrücklich als vor Ort zu erheben aus. |
| 17 | In der Vorbereitungsphase sind interessierte Parteien mit einschlägiger Fachexpertise zu identifizieren und über partizipative Ansätze frühzeitig in die Entscheidungsfindung einzubeziehen, um ein gemeinsames Verständnis und Verantwortungsgefühl unter den Beteiligten zu fördern. | ISO 14091:2021, Sekundärquelle: Umweltbundesamt, "Klimarisikoanalysen auf kommunaler Ebene – Handlungsempfehlungen zur Umsetzung der ISO 14091", https://www.umweltbundesamt.de/publikationen/klimarisikoanalysen-auf-kommunaler-ebene | Kap. 5 (dort Abschnitt 2.1.2 "Interessierte Parteien identifizieren und partizipative Ansätze planen", S. 13) | offen | — | Das Produkt bietet keinen Prozess und keine Funktion, mit der eine Kommune interessierte Parteien identifiziert oder einen partizipativen Beteiligungsprozess plant und begleitet; es ist ein Analysewerkzeug für die inhaltliche Berechnung von Klimarisiken, keine Prozessunterstützung für Beteiligungsverfahren. |
| 18 | Optional kann die Anpassungskapazität eines betroffenen Systems analysiert und bewertet werden, unterschieden nach mehreren Komponenten (u. a. organisationsbezogene Fähigkeit, technisches Vermögen, finanzielle Fähigkeit, Fähigkeit des Ökosystems) und nach unterschiedlichen Reifegraden, um abzuleiten, wie stark sich das Klimarisiko durch Anpassung verringern lässt. | ISO 14091:2021, Sekundärquelle: Umweltbundesamt, "Klimarisikoanalysen auf kommunaler Ebene – Handlungsempfehlungen zur Umsetzung der ISO 14091", https://www.umweltbundesamt.de/publikationen/klimarisikoanalysen-auf-kommunaler-ebene | Kap. 6, Anhang G und H (Abschnitt 2.2.5 "Optional: Anpassungskapazität analysieren und bewerten", S. 28f.) | erfüllt | backend/app/data/anpassungskapazitaet.py, backend/app/services/anpassungskapazitaet.py, backend/app/services/anpassungskapazitaet_markdown.py, backend/app/api/routes/anpassungskapazitaet.py, docs/ANPASSUNGSKAPAZITAET.md | Keine Lücke im Produkt; der nach ISO 14091 optionale Schritt ist als Selbsteinschätzung der Kommune je Komponente und Reifegrad umgesetzt und im Bericht als optionaler Analyseschritt ausgewiesen. |
| 19 | Bei der Interpretation der Analyseergebnisse sind bestehende Unsicherheiten in den zugrunde liegenden Informationen und Daten explizit zu berücksichtigen, ebenso handlungsfeld- und regionsübergreifende Abhängigkeiten, bevor daraus Handlungsoptionen formuliert werden. | ISO 14091:2021, Sekundärquelle: Umweltbundesamt, "Klimarisikoanalysen auf kommunaler Ebene – Handlungsempfehlungen zur Umsetzung der ISO 14091", https://www.umweltbundesamt.de/publikationen/klimarisikoanalysen-auf-kommunaler-ebene | Kap. 6 (Abschnitt 2.2.6 "Ergebnisse interpretieren", S. 29f.) | teilweise | backend/app/services/unsicherheits_zusammenschau.py, backend/app/api/routes/kommune.py, backend/tests/test_unsicherheits_zusammenschau.py, backend/app/services/gewissheit.py, docs/evidenz/register.md | Die Unsicherheit der Daten trägt das Produkt: Die Zusammenschau nennt je Handlungsfeld die niedrigste Gewissheitsstufe und die Zahl der nicht belegten Parameter und verlangt ab „gering“ vorsichtige Interpretation. Es fehlt aber, was Abschnitt 2.2.6 darüber hinaus verlangt. Handlungsfeldübergreifend ist die Zusammenschau nicht: Der aktive Katalog hat nur das Handlungsfeld „Menschliche Gesundheit“, und auch mit mehreren Feldern stellte sie diese nur nebeneinander, statt wechselseitige Abhängigkeiten zu ermitteln. Nur die übernommenen KWRA-Querverbindungen (Zeile 9) zeigen bundesweite Beziehungen. Regionsübergreifende Abhängigkeiten, etwa zu Nachbarkommunen, werden nicht betrachtet. Die Unsicherheit ist nicht mit den einzelnen Handlungsoptionen verbunden. Leitfragen der Kommune, die Einbeziehung von Fachabteilungen, externer Expertise und angrenzenden Kommunen sowie die Trennung der Maßnahmen danach, ob die Kommune sie allein umsetzen kann, fehlen. Gender- und Diversitätsaspekte gehen nur über das Alter ein. Primärtext ISO 14091 nicht gelesen (T-0531-ceo). Einzelnachweis: Abschnitt „Gegenprobe Zeile 19“. |
| 20 | Die Ergebnisse der Risikobewertung sind zielgruppenspezifisch zu kommunizieren, etwa durch einen ausführlichen Bericht mit Datengrundlagen und Methodik für die Fachöffentlichkeit sowie durch leicht verständliche, prägnante Kommunikationsprodukte (z. B. Karten, Zusammenfassungen) für politische Entscheidungsträger und die breite Öffentlichkeit. | ISO 14091:2021, Sekundärquelle: Umweltbundesamt, "Klimarisikoanalysen auf kommunaler Ebene – Handlungsempfehlungen zur Umsetzung der ISO 14091", https://www.umweltbundesamt.de/publikationen/klimarisikoanalysen-auf-kommunaler-ebene | Kap. 7 (Abschnitt 2.3.2 "Ergebnisse zielgruppenspezifisch kommunizieren", S. 31) | teilweise | docs/methodik/95_hitzebelastung.md, backend/app/services/kurzfassung_markdown.py, backend/app/api/routes/kommune.py, backend/tests/test_kurzfassung_export.py, backend/app/services/geodata_export_service.py | Neben dem Methodik-Bericht für die Fachöffentlichkeit erzeugt das Produkt eine prägnante Kurzfassung mit fünf festen Abschnitten für politische Entscheidungsträger, und der GeoPackage-Export bringt die Ergebnisse je Zelle in GIS-Systeme. Es fehlt aber, was Abschnitt 2.3.2 darüber hinaus nennt. Für die breite Öffentlichkeit gibt es kein Produkt: Die öffentliche Deutschland-Karte ist abgeschaltet, die Karte der Anwendung nur nach Anmeldung zugänglich, es gibt weder Broschüre noch Online-Auftritt mit Ergebnissen der Kommune noch Hinweise auf Eigenvorsorge; Karten und Broschüren nennt das UBA dabei nur als Beispiel. Die Kurzfassung weist keine Handlungserfordernisse (Dringlichkeit) aus, nennt als Handlungsmöglichkeiten nur schon geplante Maßnahmen, erklärt ihre Begriffe nicht und enthält keine Karte. Einen Abschlussbericht der Kommune mit Detailergebnissen gibt es nicht; die Methodik-Berichte sind bundesweit gleich und liegen nur im Repo. Ziele der Kommunikation je Akteursgruppe, Beschlussvorlagen, Veranstaltungen und Kampagnen sind Verfahrensschritte ohne Gegenstück im Produkt. Primärtext ISO 14091 nicht gelesen (T-0531-ceo). Einzelnachweis: Abschnitt „Gegenprobe Zeile 20“. |
| 21 | Die Monetarisierung von Umweltauswirkungen soll durchgängig auf dem Schadenskostenansatz beruhen; Vermeidungs- oder Wiederherstellungskosten sollen nicht als Ersatz für Schadenskosten verwendet werden, um Datenlücken zu schließen, da sie vom Minderungsziel abhängen bzw. real oder virtuell sein können und daher kein aussagekräftiger Ersatzwert sind. | UBA Methodenkonvention 4.0 | UBA_Handbuch Umweltkosten_Methodenkonvention 4.0.pdf, Kap. 1 (S. 8f.) und Kap. 2.2.1 (S. 12) | teilweise | docs/methodik/60_gebaeudeschaeden_flusshochwasser.md, backend/app/data/catalog.py | Für Gesundheitswirkungen (z. B. hitzebedingte Mortalität) folgt das Produkt dem Schadenskostenansatz (VSL/VOLY-artige Kostensätze), für Gebäudeschäden bei Flusshochwasser (#60) wird jedoch ausdrücklich mit Wiederherstellungskosten zum Neuwert (NHK, indexiert) bewertet (docs/methodik/60_gebaeudeschaeden_flusshochwasser.md, Konto K3); das Produkt wendet damit je nach Schadenskategorie unterschiedliche, nicht vereinheitlichte Kostenkonzepte an, statt durchgängig den von der Methodenkonvention empfohlenen Schadenskostenansatz zu verwenden, und dokumentiert diesen Methodenwechsel nicht als bewusste Abweichung von der Konvention. |
| 22 | Zukünftige Kosten und Nutzen sind unter Verwendung einer Diskontrate (u. a. der Reinen Zeitpräferenzrate) auf den heutigen Tag abzuzinsen; es werden mindestens zwei Werte (0 % und 1 % RZPR) berichtet, um die Sensitivität der Ergebnisse gegenüber der Zeitpräferenz zu zeigen. | UBA Methodenkonvention 4.0 | UBA_Handbuch Umweltkosten_Methodenkonvention 4.0.pdf, Kap. 2.2.3 (S. 14f.) | teilweise | backend/app/services/cost_projection_service.py, backend/tests/test_kostenprojektion_diskontierung.py | Die Kostenprojektion 2025–2065 weist die kumulierten Kosten zusätzlich als Barwerte mit 0 % und 1 % aus, auf 2025 abgezinst und ohne Marktzinssatz; die beiden Werte entsprechen der Konvention. Abgezinst wird aber mit der Reinen Zeitpräferenzrate allein. Die Konvention verlangt eine Diskontrate aus zwei Teilen: der Zeitpräferenz und der Veränderung der relativen Preise (Ramsey: RZPR plus Konsumwachstum, gewichtet mit dem Grenznutzen). RZPR und Diskontrate trennt sie ausdrücklich (S. 10, S. 14–15). Die zweite Komponente fehlt, ohne Begründung und ohne ausgewiesene Abschätzung von KAP3. Damit fehlt auch die Aussage, ob für die bewerteten Gesundheitsschäden eine höhere Rate gilt (wie für Konsumgüter mit sinkendem relativem Preis) oder eine niedrigere (wie für knapper werdende Umweltgüter). Der „Barwert mit 0 % RZPR“ ist deshalb die unabgezinste Summe und der „Barwert mit 1 % RZPR“ ein Barwert zu 1 % Diskontrate. Risikoaversion geht nicht ein. Einzelnachweis: Abschnitt „Gegenprobe Zeile 22“. |
| 23 | Kostensätze sind einem eindeutigen Preisbasisjahr zuzuordnen; für die Anwendung auf Aktivitäten oder Emissionen anderer Jahre ist eine Preisanpassung anhand eines Preis- bzw. Verbraucherpreisindexes vorzunehmen. | UBA Methodenkonvention 4.0 | UBA_Handbuch Umweltkosten_Methodenkonvention 4.0.pdf, Kap. 1 (S. 9) | erfüllt | docs/evidenz/register.md, docs/methodik/60_gebaeudeschaeden_flusshochwasser.md | — |
| 24 | Ergebnisse der Monetarisierung sind als Schätzungen mit ausgewiesener Unsicherheit (Bandbreiten, Größenordnung statt Scheingenauigkeit) darzustellen; Modelle mit stochastischen Komponenten sollen die Unsicherheit einzelner Bestandteile und des Gesamtprozesses systematisch abbilden. | UBA Methodenkonvention 4.0 | UBA_Handbuch Umweltkosten_Methodenkonvention 4.0.pdf, Kap. 1 (S. 9) und Kap. 2.2.2 (S. 13) | erfüllt | docs/evidenz/register.md, docs/methodik/60_gebaeudeschaeden_flusshochwasser.md | — |
| 25 | Wirkungskategorien, die im gewählten Bewertungsmodell nicht oder nicht vollständig erfasst werden (z. B. Biodiversität, weitere nicht abgedeckte Klimafolgen), sind zu benennen; die resultierenden Kostensätze sind dann als konservative Schätzung bzw. Untergrenze der tatsächlichen Auswirkungen kenntlich zu machen, statt die fehlende Wirkung stillschweigend weg­zulassen. | UBA Methodenkonvention 4.0 | UBA_Handbuch Umweltkosten_Methodenkonvention 4.0.pdf, Kap. 2.2.2 (S. 13f.) und Kap. 3.1, Fn. 14 (S. 17) | teilweise | backend/app/data/catalog.py, docs/MODELL_KRITIK.md | Der Katalog kennzeichnet Risiken, die aus Doppelzählungsgründen bewusst mit Kostensatz 0 € geführt werden, mit einer erklärenden `cost_source`/`cost_source_detail` (Verweis auf docs/MODELL_KRITIK.md §6); für nicht bewusst ausgeschlossene, sondern methodisch schlicht (noch) nicht abgedeckte Wirkungen greift dagegen das im Code selbst so benannte „Sicherheitsnetz“ (`cost_per_outcome_eur` Default 0,0, Quelle „Modellannahme (Kostensatz, unbelegt)“), ohne dass die daraus resultierende Gesamtsumme im Produkt als konservative Untergrenze ausgewiesen wird. |

### Gegenprobe Zeile 9 gegen KWRA 2021, Teilbericht 6, Kap. 3.4

Frage: Tragen die vier in Zeile 9 genannten Belege die Anforderung, die Kap. 3.4 „Analyse der
Querverbindungen“ an eine Querverbindungsanalyse stellt, wirklich — nicht nur dem Namen nach?
Gelesen wurde gegen `docs/KWAR/kwra2021_teilbericht_6_integrierte_auswertung_bf_211027_0.pdf`;
im Kapitel 3.4 stimmen PDF-Seitenzahl und gedruckte Seitenzahl überein. Die vier Belegdateien wurden
vollständig gelesen, der Dienst `querverbindungs_auswertung()` einmal ausgeführt (Ergebnis:
52 Klimawirkungen im Katalog, davon 12 mit Netzrolle und 11 mit benannter Einzelbeziehung; 13 der
25 Netzrollen gehören zu Klimawirkungen außerhalb des Katalogs: #1, #14, #15, #26, #38, #40, #43,
#48, #49, #73, #92, #97, #101).

| Nr | Anforderung (Wortlaut oder enge Wiedergabe) | Seite | tragender Beleg (Datei, Funktion oder Abschnitt) | Urteil |
|---|---|---|---|---|
| A1 | Querbezüge zwischen den einzelnen Klimawirkungen (102 Klimawirkungen, 13 Handlungsfelder) werden identifiziert, „basierend auf den in den Kapiteln der Handlungsfelder dargestellten Zusammenhängen“; eingeschlossen sind die vorgelagerten Klimawirkungen, die in den Wirkungsketten direkt den klimatischen Einflüssen folgen (Fn. 20). | 82 | `backend/app/data/kwra_querverbindungen.py`, `BENANNTE_BEZIEHUNGEN` und `NETZROLLEN`; `backend/app/services/querverbindungen.py`, `querverbindungs_auswertung()` | trägt teilweise |
| A2 | Zusätzlich wird „ein Abgleich mit den dargestellten Querverbindungen und Wirkbeziehungen in den Klimawirkungsketten durchgeführt (UBA 2016)“. | 82 | keiner — `docs/QUERVERBINDUNGEN_KLIMAWIRKUNGEN.md`, Abschnitt „Quellenlage“, nennt als Quelle ausschließlich Teilbericht 6; `docs/KWAR/klimawirkungsketten_umweltbundesamt_2016.pdf` liegt im Repo, wird in keinem der vier Belege herangezogen | trägt nicht |
| A3 | Wirkbeziehungen werden gerichtet erfasst (von einer Klimawirkung zu einer nachgelagerten; aus- und eingehend, „vor- und nachgelagerte Klimawirkungen“); davon werden gegenseitige Wechselwirkungen unterschieden. | 82, 88 | `kwra_querverbindungen.py`, Felder `quelle`/`ziel` in `BENANNTE_BEZIEHUNGEN`; `querverbindungen.py`, Zähler `ausgehende_benannte`/`eingehende_benannte`; `RiskInteractionSection.tsx`, Spalten „wirkt auf (benannt)“ und „beeinflusst von (benannt)“ | trägt teilweise |
| A4 | Die Auswertung „basiert auf der Annahme, dass negative Auswirkungen des Klimawandels auf eine Klimawirkung auch negative Folgen für die ihr nachgelagerten Wirkungen haben“. | 82 | `docs/QUERVERBINDUNGEN_KLIMAWIRKUNGEN.md`, Abschnitt „Anwendung auf den Produktkatalog“ | trägt teilweise |
| A5 | Ausgewertet wird, „welche Klimawirkungen und aggregiert auch Handlungsfelder sich auf besonders viele andere … auswirken oder welche andersherum von besonders vielen beeinflusst werden“ (Ergebnisse S. 84–85: meiste ausgehende Wirkungen „Wasserhaushalt, Wasserwirtschaft“, meiste eingehende „Tourismuswirtschaft“; Kernaussage: „Schäden an touristischen Infrastrukturen und Betriebsunterbrechungen“ wird von den meisten anderen beeinflusst). | 82, 84–85, 88 | `kwra_querverbindungen.py`, `NETZROLLEN` (25 Klimawirkungen) und `KENNZAHLEN` (Handlungsfelder mit den meisten aus-/eingehenden Beziehungen); `querverbindungen.py`, Feld `netzrolle`; `RiskInteractionSection.tsx`, Spalte „Netzrolle“ | trägt teilweise |
| A6 | „Klimawirkungen mit zentraler Bedeutung (also einer hohen Anzahl an ausgehenden Wirkungen)“ werden identifiziert: „Hochwasser“ wirkt sich auf die meisten anderen Klimawirkungen aus; unter den hoch bewerteten Klimawirkungen nimmt „Verschiebung von Arealen und Rückgang der Bestände“ eine zentrale Position ein. | 82, 84, 87, 88 | `kwra_querverbindungen.py`, erster Eintrag in `BENANNTE_BEZIEHUNGEN` („zentrale Klimawirkung“) und `NETZROLLEN` (#49, #4) | trägt teilweise |
| A7 | Kennzahlen des Netzes: 257 Querverbindungen, im Durchschnitt circa 2,5 ein- oder ausgehende Wirkungen je Klimawirkung, 71 Klimawirkungen mit ausgehenden und 62 mit eingehenden Wirkungen. | 83–84, 88 | `kwra_querverbindungen.py`, `KENNZAHLEN`; ausgeliefert über `GET /catalog/querverbindungen`; `RiskInteractionSection.tsx` zeigt 257 und den Durchschnitt | trägt |
| A8 | Eine Klimawirkung kann zugleich ausgehende und eingehende Wirkbeziehungen haben (Fn. 21); „Verschiebung von Arealen und Rückgang der Bestände“ hat „viele ausgehende und eingehende Wirkbeziehungen“. | 84, 87, 88 | `querverbindungen.py` (zählt beide Richtungen getrennt); `NETZROLLEN` (genau eine Rolle je Klimawirkung) | trägt teilweise |
| A9 | Dargestellt werden die Querverbindungen zwischen den 13 Handlungsfeldern: ein- und ausgehende Wirkbeziehungen je Handlungsfeld mit ihrer Anzahl, die Verbindung von Handlungsfeld zu Handlungsfeld in der Stärke der Anzahl ihrer Querbezüge (Abbildung 8 mit Hinweistext). | 83 | keiner — `KENNZAHLEN` nennt nur die Handlungsfelder mit den meisten bzw. nur aus- oder nur eingehenden Beziehungen, die 5 Beziehungen auf Handlungsfeldebene in `BENANNTE_BEZIEHUNGEN` tragen keine Anzahl, das Dashboard hat keine Handlungsfeld-Sicht | trägt nicht |
| A10 | Die Ergebnisse werden nach Clustern und Systembereichen eingeordnet: ausgehende Wirkungen vor allem bei natürlichen Systemen und Ressourcen (Cluster Wasser und Land), eingehende bei naturnutzenden Wirtschaftssystemen, Infrastrukturen und Gebäuden sowie Menschen und sozialen Systemen; mögliche Kaskadeneffekte. | 84–85, 88 | `kwra_querverbindungen.py`, `SYSTEMBEREICH_MATRIX` (Tabelle 28 aus Kap. 7, S. 153); `docs/QUERVERBINDUNGEN_KLIMAWIRKUNGEN.md`, Abschnitt „Querverbindungen zwischen den Systembereichen“ | trägt teilweise |
| A11 | Die Klimawirkungen werden „auf mögliche gegenseitige Wechselwirkungen und damit Rückkopplungsschleifen untersucht“: Gewässertemperatur ↔ Kühlwasser; „Bedarf an Kühlenergie“ ↔ „Stadtklima/Wärmeinseln“; der Kreislauf Hitzebelastung → Bedarf an Kühlenergie ↔ Stadtklima/Wärmeinseln → Hitzebelastung ist der einzige Rückkopplungskreislauf der Gesamtauswertung, mit ausdrücklichem Verweis auf die Verantwortung der Kommunen; schwächer: „Verschiebung von Arealen …“ ↔ „Vegetation in Siedlungen“. | 85–86 (Abb. 9) | nur `BENANNTE_BEZIEHUNGEN`, Eintrag Stadtklima/Wärmeinseln → Hitzebelastung | trägt nicht |
| A12 | In einem weiteren Analyseschritt werden die Querverbindungen der als hoch bewerteten Klimawirkungen (Gegenwart, Mitte und Ende des Jahrhunderts) gesondert betrachtet (Ergebnis: „Biologische Vielfalt“ mit der höchsten Gesamtzahl; viele eingehende Beziehungen bei „Schäden an Küstenökosystemen“, „Schäden an Feuchtgebieten und wassergebundenen Habitaten“, „Schäden an Wäldern“, „Verschiebung von Arealen …“). | 86–87, 88 | keiner — `NETZROLLEN` mischt Befunde der Gesamt- und der Hochrisiko-Auswertung ohne Kennzeichnung (#5 „stark eingehend“ stammt aus S. 87); Feuchtgebiete und Wälder fehlen | trägt nicht |
| A13 | Die Ergebnisse werden mit der Querverbindungsauswertung der Vulnerabilitätsanalyse 2015 verglichen (ähnliche Muster, Kaskade Land/Wasser → Wirtschaft/Gesundheit/Infrastruktur, zentrale Rolle Wasserhaushalt). | 87 | keiner | trägt nicht |

**Begründung je Urteil:**

- A1: das Produkt identifiziert selbst keine Querbezüge, sondern übernimmt einen Auszug von 20 Beziehungen (8 davon zwischen einzelnen Klimawirkungen) aus 257. Selbst im Fließtext von Kap. 3.4 genannte Beziehungen fehlen: „Wassermangel im Boden“ → „Schäden in Wäldern“ → „Holzertrag“/„Erholung“ (S. 82), „Gewässertemperatur …“ ↔ „Mangelndes Kühlwasser für thermische Kraftwerke“ (S. 82, 85), „Bedarf an Kühlenergie“ ↔ „Stadtklima/Wärmeinseln“ (S. 85), „Verschiebung von Arealen …“ ↔ „Vegetation in Siedlungen“ (S. 86). Der Auszug ist als „nicht vollständig“ gekennzeichnet; die Modellgrenze (keine Kantenliste in der Quelle) ist korrekt benannt.
- A3: die Richtung ist abgebildet, gegenseitige Wechselwirkungen gibt es als Beziehungsart nicht.
- A4: sinngemäß als Lesehinweis („Folgewirkungen … mitdenken“), nicht als Annahme der Auswertung benannt; im Dashboard fehlt sie.
- A5: das Ergebnis der KWRA ist quellenfest übernommen, aber nicht ausgewertet (keine Zählung, keine Rangfolge); die Spalten „wirkt auf/beeinflusst von (benannt)“ zählen nur den Auszug aus A1 und sind keine Anzahl im Sinne der KWRA. Das Dashboard zeigt nur Katalog-Klimawirkungen: 13 der 25 Netzrollen fehlen dort, darunter #92 (die am meisten beeinflusste Klimawirkung) und #48 „Niedrigwasser“; die Handlungsfeld-Aussagen aus `KENNZAHLEN` zeigt es nicht an.
- A6: im Datenmodul und in der Doku belegt, aber ohne eigene Kennzeichnung „zentral“; Hochwasser (#49) steht nicht im Katalog und erscheint deshalb weder in der Auswertung je Klimawirkung noch im Dashboard; #4 ist nur als „stark ausgehend“ geführt.
- A7: alle vier Zahlen stimmen mit S. 83–84 überein (71 und 62 nur in API und Datenmodul, nicht im Dashboard).
- A8: die Netzrolle ist einwertig, #4 steht nur als „stark ausgehend“.
- A9: die Anzahlen stehen in der Quelle nur als Skalen der Abbildung 8, nicht als Tabelle; eine Übernahme wäre eine ausgewiesene Ablesung (Vorgabe P1).
- A10: die Systembereichsebene ist quellenfest vorhanden (aus Kap. 7, nicht aus Kap. 3.4), im Dashboard aber nicht angezeigt; die Einordnung nach Clustern und die Aussage zu Kaskadeneffekten fehlen.
- A11: „Bedarf an Kühlenergie“ und „Kühlwasser“ kommen in keinem der vier Belege vor, einen Rückkopplungskreislauf gibt es im Produkt nicht; betroffen sind mit Hitzebelastung (#95), Stadtklima (#62), Vegetation in Siedlungen (#61) und Arealverschiebung (#4) Klimawirkungen des Katalogs.
- A13: Vergleich zweier Ausgaben der Bundesanalyse; für ein kommunales Werkzeug ohne Vorgängerauswertung nicht einschlägig und deshalb nicht in die Lücke der Zeile 9 übernommen.

**Gelesene Seiten und Abschnitte:** Inventar mit `python3 /opt/overlord/overlord/skripte/dokumente.py
inventar` (172 Seiten); Inhaltsverzeichnis S. 6–7 ganz überflogen; Kap. 3.4 „Analyse der
Querverbindungen“ S. 82–88 vollständig im Text gelesen, einschließlich Fußnoten 20 (S. 82) und 21
(S. 84) und des Kastens „Kernaussagen der Analyse der Querverbindungen“ (S. 88), dazu S. 89 bis zum
Beginn von Kap. 4 (Kapitelgrenze geprüft). Als Bild angesehen: S. 83 (Abbildung 8 „Querverbindungen
zwischen den Handlungsfeldern“ mit Hinweistext) und S. 86 (Abbildung 9 „Kreislauf der
Querverbindungen zwischen den Klimawirkungen ‚Hitzebelastung‘, ‚Bedarf an Kühlenergie‘ und
‚Stadtklima/Wärmeinseln‘“). Kap. 3.4 enthält keine Tabelle; Tabelle 28 (Kap. 7, S. 153) stützt nur
den Beleg, nicht das Kapitel, und wurde hier nicht erneut gelesen. Nicht gelesen: Kap. 3.1 (auf das
S. 84 für die klimatischen Einflüsse verweist) und die Handlungsfeldkapitel der Teilberichte 2–5, aus
denen die KWRA ihre Querbezüge gewonnen hat.

**Schluss:** Zeile 9 bleibt nicht `erfüllt`. Von 13 Anforderungen trägt der Bestand eine voll (A7),
sieben teilweise und fünf nicht (A2, A9, A11, A12, A13); der Status der Zeile 9 ist in derselben
Änderung auf `teilweise` gesetzt, die Spalte „Lücke“ nennt, was fehlt. Die Zählungen in den
Abschnitten „Nachtrag: Abschlusszählung“ und „Zusammenfassung“ (6 `erfüllt`, 14 `teilweise`) sind
damit überholt; sie nachzuziehen ist Sache der Gesamtzählung (T-0487), nicht dieser Gegenprobe.

### Gegenprobe Zeile 10 gegen KWRA 2021, Teilbericht 6, Kap. 7

Frage: Tragen die drei in Zeile 10 genannten Belege den Vergleich über die fünf Systembereiche, den
Kap. 7 „Querbetrachtung der Systembereiche“ anstellt — und verlangt Kap. 7 dabei auch einen
Vergleich der Anpassungsfähigkeit? Gelesen wurde gegen
`docs/KWAR/kwra2021_teilbericht_6_integrierte_auswertung_bf_211027_0.pdf`; im Kapitel 7 stimmen
PDF-Seitenzahl und gedruckte Seitenzahl überein. Die drei Belegdateien wurden vollständig gelesen
(`catalog.py` im Abschnitt „KWRA-Systembereiche“, Zeilen 2522–2551 der Datei), dazu
`backend/app/data/kwra_querverbindungen.py` (`SYSTEMBEREICH_MATRIX`) und
`backend/app/services/charakterisierung.py` (`anpassungspotenzial`). Der Katalog wurde einmal
ausgezählt: 4 Risikocodes zu 3 gerechneten Klimawirkungen (#95, #96, #98), alle 4 in
`RISK_SYSTEMBEREICH` dem Bereich „Menschen und soziale Systeme“ zugeordnet; die 49 Klimawirkungen
der Roadmap (`PLANNED_RISKS`) tragen kein Systembereichsfeld. `systembereich_auswertung()` wird außer
in `backend/tests/test_systembereiche.py` an keiner Stelle aufgerufen (kein API-Endpunkt, kein Bericht).

Zum angemeldeten Zweifel: Ja. Kap. 7 führt die fünf Bereiche von Anfang an als Systeme ein, „die
unterschiedlich stark dem Klimawandel ausgesetzt sind und unterschiedlich gut auf ihn reagieren
können“ (S. 146), und vergleicht je Bereich neben dem Klimarisiko ohne Anpassung ausdrücklich die
Wirksamkeit der Anpassung, das Klimarisiko mit Anpassung, die Anpassungsdauer und die Grenzen der
Anpassung (A3–A5). Schadenskosten vergleicht Kap. 7 nicht; der Kostenvergleich des Produkts ist eine
Zugabe, kein Beleg für die Anforderung.

| Nr | Anforderung (Wortlaut oder enge Wiedergabe) | Seite | tragender Beleg (Datei, Funktion oder Abschnitt) | Urteil |
|---|---|---|---|---|
| A1 | Die einzelnen Klimawirkungen werden fünf übergeordneten Systembereichen zugeordnet — „Natürliche Systeme und Ressourcen“ (30 Klimawirkungen), „Naturnutzende Wirtschaftssysteme“ (31), „Infrastrukturen und Gebäude“ (23), „Naturferne Wirtschaftssysteme“ (7), „Menschen und soziale Systeme“ (9) —, „die unterschiedlich stark dem Klimawandel ausgesetzt sind und unterschiedlich gut auf ihn reagieren können“. | 146, 147, 149, 150, 151 | `backend/app/data/catalog.py`, `KWRA_SYSTEMBEREICHE` und `RISK_SYSTEMBEREICH`; `backend/tests/test_systembereiche.py`, Tests (a) und (b) | trägt teilweise |
| A2 | Das Klimarisiko ohne Anpassung wird zwischen den Bereichen verglichen, über alle Zeitscheiben (Gegenwart, Mitte, Ende des Jahrhunderts) und für den optimistischen wie den pessimistischen Fall, gemessen am Anteil der hoch bewerteten Klimawirkungen des Bereichs (z. B. 60 % zur Mitte, 70 % zum Ende bei den natürlichen Systemen; „etwa eine halbe Stufe niedriger“ bei Infrastrukturen und Gebäuden; „mit Abstand … die niedrigsten“ bei den naturfernen Wirtschaftssystemen; die höchsten Risiken der Gegenwart bei Menschen und sozialen Systemen). In Abb. 24 bemisst sich die Größe jedes Bereichs am „Anteil der hoch bewerteten Klimarisiken (Mitte des Jh.) an allen Klimawirkungen des Systembereichs“. | 146–151, 152 (Abb. 24), 153 | `backend/app/services/systembereiche.py`, `systembereich_auswertung()`, Felder `mittlerer_index` und `anzahl_klimawirkungen` | trägt teilweise |
| A3 | Die Wirksamkeit der Anpassung — beschlossene und weiterreichende Maßnahmen, Klimarisiko mit Anpassung, Unterschied zwischen optimistischem und pessimistischem Fall — wird zwischen den Bereichen verglichen (natürliche Systeme: „deutlich niedriger … als bei anderen Systembereichen“; naturnutzende: „deutlich wirksamer“, „erhebliche Diskrepanz“ zwischen den Fällen; Infrastrukturen und Gebäude: „besonders hohe Wirksamkeit“; für naturferne Wirtschaftssysteme und Menschen und soziale Systeme ausdrücklich keine valide Aussage, weil nur eine bzw. drei Klimawirkungen untersucht wurden). Abb. 24 zeigt je Bereich Balken „Klimarisiko mit und ohne Anpassung“ mit „Wirksamkeit der Anpassung“. | 146, 148, 149–150, 150, 151, 152 (Abb. 24), 153 | keiner — `systembereich_auswertung()` führt kein Anpassungsmaß; `charakterisierung.anpassungspotenzial()` liefert eine relative Minderung je Risikocode, wird aber nicht je Bereich zusammengefasst und trennt nicht beschlossene von weiterreichenden Maßnahmen | trägt nicht |
| A4 | Die Anpassungsdauer wird zwischen den Bereichen verglichen (natürliche Systeme „meist über zehn und teils über 50 Jahre“, „deutlich länger“; naturnutzende im Durchschnitt, aber stark streuend; Infrastrukturen und Gebäude „meist mittlere Anpassungsdauer (länger als in anderen Systembereichen)“; naturferne: kein Bereich kürzer, alle unter zehn Jahren; Menschen und soziale Systeme in zwei Dritteln der Fälle unter zehn Jahren). | 147, 148, 150, 151, 153 | keiner — das Produkt führt keine Anpassungsdauer, weder je Klimawirkung noch je Bereich | trägt nicht |
| A5 | Grenzen der Anpassung werden je Bereich ausgewiesen: bei den natürlichen Systemen vier Klimawirkungen ohne grundsätzlich verfügbare Anpassungsmaßnahmen, fünf mit mittel-hohem oder hohem Klimarisiko trotz weiterreichender Anpassung; bei den naturnutzenden Wirtschaftssystemen keine Klimawirkung ohne Reaktionsmöglichkeit, aber sechs von 11 bewerteten mit mittel-hohem Risiko mit Anpassung zur Mitte des Jahrhunderts im pessimistischen Fall; bei Infrastrukturen und Gebäuden lässt sich das Risiko mit weiterreichender Anpassung auf „mittel“ oder „gering-mittel“ eingrenzen. Abb. 24 kennzeichnet „keine Anpassungsmöglichkeiten“ im Dringlichkeitsring. | 147, 148, 150, 152 (Abb. 24) | keiner | trägt nicht |
| A6 | Die Gewissheit der Bewertungen wird zwischen den Bereichen verglichen, getrennt für Klimarisiko ohne Anpassung und Anpassungskapazität (natürliche Systeme „tendenziell geringer“; naturnutzende sinkend auf den Gesamtdurchschnitt; Infrastrukturen und Gebäude bei den Anpassungsmaßnahmen „deutlich über den anderen“; naturferne „relativ gering“; Menschen und soziale Systeme „recht hoch“). | 147, 148, 149, 150, 151 | keiner — `backend/app/services/gewissheit.py` stuft je Klimawirkung ein (Zeile 8), `systembereich_auswertung()` fasst die Stufe nicht je Bereich zusammen | trägt nicht |
| A7 | Die Zahl der sehr dringenden und der dringenden Handlungserfordernisse wird je Bereich ermittelt und verglichen (natürliche Systeme 11 und 5; naturnutzende 10 und 6; Infrastrukturen und Gebäude 7 und 7; naturferne 0 und 2; Menschen und soziale Systeme 3 und 3). Abb. 24 zeigt sie je Bereich als Dringlichkeitsring. | 147, 148–149, 150, 151, 152 (Abb. 24) | keiner — die Dringlichkeit steht nur als Roadmap-Kategorie (Zeile 6), nicht je Bereich | trägt nicht |
| A8 | Die Wirkbeziehungen zwischen den Bereichen werden ausgewertet (Tabelle 28, ohne rein vorgelagerte Klimawirkungen; Diagonale innerhalb des Bereichs, Summe nur zu den vier anderen): etwa 50 % der „knapp 160“ ausgehenden Wirkbeziehungen gehen von den natürlichen Systemen aus, 50 davon zu den naturnutzenden Wirtschaftssystemen; die naturfernen Wirtschaftssysteme haben „relativ gesehen deutlich mehr“ eingehende Beziehungen als jeder andere Bereich. Abb. 24 zeigt die Pfeile mit einer Breite nach der Anzahl der ausgehenden Wirkbeziehungen. | 147, 150, 152 (Abb. 24), 153 | `backend/app/data/kwra_querverbindungen.py`, `SYSTEMBEREICH_MATRIX` (alle 25 Zellen und fünf Summen stimmen mit Tabelle 28 überein; 80 + 35 + 30 + 0 + 12 = 157); ausgeliefert über `GET /catalog/querverbindungen`; `docs/QUERVERBINDUNGEN_KLIMAWIRKUNGEN.md`, Abschnitt „Querverbindungen zwischen den Systembereichen“ | trägt |
| A9 | Je Bereich werden die maßgeblichen klimatischen Einflüsse benannt (natürliche Systeme: gradueller Temperaturanstieg, Hitze, Trockenheit, Starkwind; naturnutzende: Trockenheit, Hitze, gradueller Temperaturanstieg; Infrastrukturen und Gebäude: Starkregen, Überflutung, Starkwind, Meeresspiegelanstieg, Entlastung durch weniger Frost und Schnee; naturferne: gradueller Temperaturanstieg und Extreme; Menschen und soziale Systeme: Hitze, dazu UV-Strahlung und Sturzfluten). Abb. 24 führt sie je Bereich als „Wichtige Klimaänderungen“. | 146, 148, 149, 150, 151, 152 (Abb. 24) | keiner — die Katalogeinträge nennen Einflüsse je Klimawirkung, `systembereich_auswertung()` fasst sie nicht je Bereich zusammen | trägt nicht |
| A10 | Aus dem Vergleich werden Schlüsse für die Anpassungsplanung gezogen: Die natürlichen Systeme sind stärker betroffen, passen sich langsamer und weniger wirksam an und wirken auf alle anderen Bereiche zurück; der Blick ist deshalb auf vorgelagerte Klimawirkungen und diesen Bereich zu richten, Zielkonflikte bei Wasser- und Landnutzung sind vorbeugend einzugrenzen (Raumplanung), und es besteht dort ein „besonderes Handlungserfordernis“ — ausdrücklich für den ganzen Bereich, nicht für einzelne Klimawirkungen aus Kaskadeneffekten. | 153–154 | nur `docs/QUERVERBINDUNGEN_KLIMAWIRKUNGEN.md`, Satz nach der Matrix („Natürliche Systeme und Ressourcen sind mit 80 ausgehenden Beziehungen der stärkste Sender“) | trägt nicht |
| A11 | Methodische Grenze des Vergleichs: Die Bewertung nachgelagerter Klimawirkungen konnte nicht berücksichtigen, ob Anpassung bei den vorgelagerten gelingt (Fn. 30); das Bild kann dadurch verzerrt sein, und nicht alle Wirkbeziehungen sind erfasst. | 153–154 | keiner — `docs/QUERVERBINDUNGEN_KLIMAWIRKUNGEN.md`, Abschnitt „Modellgrenze“, betrifft nur die Unvollständigkeit des Produkt-Auszugs aus den 257 Querverbindungen | trägt nicht |

**Begründung je Urteil:**

- A1: Die fünf Bereichsnamen stimmen wörtlich, und die Zuordnung von #95, #96 und #98 zu „Menschen und
  soziale Systeme“ ist durch S. 151 gedeckt. Zugeordnet sind aber nur die drei gerechneten
  Klimawirkungen; die 49 Klimawirkungen der Roadmap haben keinen Systembereich, und vier der fünf
  Bereiche enthalten im Produkt keine einzige Klimawirkung.
- A2: Die Funktion vergleicht ein arithmetisches Mittel des Produkt-Risikoindex, nicht den Anteil hoch
  bewerteter Klimawirkungen, und kennt weder Zeitscheiben noch Fälle. Solange alle Klimawirkungen in
  einem Bereich liegen, ist kein Unterschied zwischen Bereichen sichtbar; die Auswertung erreicht
  außerhalb des Tests weder API noch Bericht.
- A3: Kern des angemeldeten Zweifels. Der Vergleich der Anpassungsfähigkeit ist in Kap. 7 kein
  Nebenaspekt, sondern trägt die Schlussfolgerung S. 153 („die Wirksamkeit von Anpassungsmaßnahmen
  [ist] vergleichsweise gering“). Das Produkt hat mit `anpassungspotenzial()` einen Baustein je
  Klimawirkung, aber keinen Vergleich je Bereich. Die KWRA selbst trifft für zwei Bereiche keine
  valide Aussage (S. 150, 151); ein Produktvergleich müsste diese Lücke benennen, statt sie zu füllen.
- A4, A5: im Produkt keine Größe vorhanden.
- A6, A7, A9: Die Einzelwerte je Klimawirkung gibt es (Gewissheit Zeile 8, Dringlichkeit Zeile 6,
  Einflüsse im Katalog), die Verdichtung je Bereich nicht.
- A8: quellenfest und vollständig; im Dashboard nicht angezeigt (Sichtbarkeit ist Gegenstand von
  T-0483, nicht dieser Gegenprobe).
- A10: Die Tabelle belegt die Senderrolle, die Schlüsse für die Anpassungsplanung stehen nirgends.
- A11: Die Doku benennt, dass das Produkt nur einen Auszug der KWRA-Querverbindungen führt; dass
  schon die KWRA nicht alle Wirkbeziehungen erfasst hat und ihre Bewertung nachgelagerter
  Klimawirkungen den Anpassungserfolg bei vorgelagerten nicht berücksichtigen konnte (Fn. 30), steht
  nirgends.

**Gelesene Seiten und Abschnitte:** Inventar mit `python3 /opt/overlord/overlord/skripte/dokumente.py
inventar` (172 Seiten); Inhaltsverzeichnis S. 6–7 ganz überflogen; Kap. 7 „Querbetrachtung der
Systembereiche“ S. 146–154 vollständig im Text gelesen — alle fünf Bereichsabschnitte (S. 146–151),
die Schlussfolgerungen S. 153–154 einschließlich Fußnote 30 (S. 153) —, dazu S. 155 mit dem Beginn
von Kap. 8 (Kapitelgrenze geprüft; Kap. 7 endet auf S. 154). Als Bild angesehen: S. 152 (Abbildung 24
„Klimarisiken von betroffenen Systemen, Wirkbeziehungen und Dringlichkeit von Anpassung“ mit
Legende: Balken Klimarisiko mit und ohne Anpassung je Zeitscheibe, Wirksamkeit der Anpassung,
Kreisgröße nach dem Anteil hoch bewerteter Klimarisiken zur Mitte des Jahrhunderts, Pfeilbreite nach
der Zahl ausgehender Wirkbeziehungen, Dringlichkeitsring) und S. 153 (Tabelle 28 „Ausgehende und
eingehende Querverbindungen der fünf Systembereiche“, ganz übernommen und Zelle für Zelle mit
`SYSTEMBEREICH_MATRIX` verglichen). Kap. 7 enthält keine weitere Tabelle oder Abbildung. Nicht
gelesen: Kap. 2.1 (auf das S. 146 für die Gruppenbildung verweist), Kap. 3.2 und 3.4 (auf die
S. 147, 153 und 154 verweisen), Kap. 5 (Anpassungskapazität je Handlungsfeld und Klimawirkung,
Tabellen 21–24) und Teilbericht 1, aus dem die Einzelbewertungen stammen.

**Schluss:** Zeile 10 bleibt nicht `erfüllt`. Von 11 Anforderungen trägt der Bestand eine voll (A8),
zwei teilweise (A1, A2) und acht nicht (A3–A7, A9–A11); der Status der Zeile 10 ist in
derselben Änderung auf `teilweise` gesetzt, die Spalte „Lücke“ nennt, was fehlt. Die Zählungen in den
Abschnitten „Nachtrag: Abschlusszählung“ und „Zusammenfassung“ sind damit weiter überholt; sie
nachzuziehen ist Sache der Gesamtzählung (T-0821-ceo, T-0487), nicht dieser Gegenprobe.

### Gegenprobe Zeile 7 gegen KWRA 2021, Teilbericht 6, Kap. 6.2

Frage: Tragen die vier in Zeile 7 genannten Belege die Einordnung in Charakterisierungsgruppen, die
Kap. 6.2 „Charakterisierung der Handlungserfordernisse“ verlangt — und stimmen die Gruppen, die das
Produkt ausweist, mit denen der KWRA überein? Gelesen wurde gegen
`docs/KWAR/kwra2021_teilbericht_6_integrierte_auswertung_bf_211027_0.pdf`; in Kap. 6.2 stimmen
PDF-Seitenzahl und gedruckte Seitenzahl überein. Kap. 6.2 reicht von S. 140 bis S. 145, nicht nur bis
S. 142, wie die Fundstelle der Zeile 7 angibt. `backend/app/services/charakterisierung.py` und die
Route `GET /catalog/charakterisierungsgruppen` in `backend/app/api/routes/catalog.py` wurden vollständig
gelesen, `backend/app/services/gewissheit.py` und `backend/tests/test_charakterisierungsgruppen.py` im
Aufbau. `charakterisierungen()` wurde einmal ausgeführt, ohne etwas zu ändern:

| Risikocode | Klimawirkung | Anpassungspotenzial p | Gewissheit | Gruppe im Produkt |
|---|---|---|---|---|
| EXPECTED_ANNUAL_MORTALITY | #95 Hitzebelastung | 0,259 | mittel | Entwicklung |
| EXPECTED_ANNUAL_MORBIDITY | #95 Hitzebelastung | 0,259 | hoch | Entwicklung |
| EXPECTED_ANNUAL_ALLERGY_DAYS | #96 Aeroallergene | 0,0 | mittel | Innovation |
| EXPECTED_ANNUAL_UV_YLL | #98 UV-Schädigungen | 0,0 | hoch | Innovation |

Der Katalog führt drei Maßnahmen (`catalog.MEASURES`). Nur `HEAT_ACTION_PLANS` (r = 0,05) und
`VULNERABLE_GROUP_PROGRAMS` (r = 0,22) sind über `linked_risk_codes` mit einer Klimawirkung verknüpft,
beide mit #95. `POLLEN_EARLY_WARNING` (r = 0,03) steht für #96 nur in `qualitative_risk_codes` und zählt
in `anpassungspotenzial()` nicht. Für #98 gibt es keine Maßnahme.

| Nr | Anforderung (Wortlaut oder enge Wiedergabe) | Seite | tragender Beleg (Datei, Funktion oder Abschnitt) | Urteil |
|---|---|---|---|---|
| A1 | Eingeordnet werden die „identifizierten Klimawirkungen mit sehr dringenden Handlungserfordernissen“, also die 31 aus Tabelle 25; Tabelle 27 führt davon 29, weil für die beiden mit Stern markierten („Beschädigung oder Zerstörung von Siedlung und Infrastruktur an der Küste“, „Innenraumklima“) keine Anpassungskapazität bewertet wurde. | 140, 138 (Tab. 25), 142 (Tab. 27) | `charakterisierung.py`, `charakterisierungen()` (läuft über alle Codes aus `catalog.RISKS_BY_CODE`) | trägt teilweise |
| A2 | Erste Frage: „Reichen die beschlossenen Maßnahmen im optimistischen und im pessimistischen Fall aus, um das Restrisiko auf ein bestimmtes, gesetztes Niveau zu reduzieren?“ Gruppe I „Umsetzung“: Die beschlossenen Maßnahmen reichen aus. | 140 | `charakterisierung.py`, `anpassungspotenzial()` und `SCHWELLE_UMSETZUNG` (0,5) | trägt teilweise |
| A3 | Zweite Frage: „Reichen die weiterreichenden Maßnahmen … aus …?“ Gruppe II „Entwicklung“: Die beschlossenen reichen nicht, weiterreichende schon. Gruppe IV „Innovation“: Es ist „relativ sicher, dass das Ziel … selbst bei der Umsetzung aller beschlossenen und weiterreichenden Maßnahmen nicht erreicht wird“. | 140–141, 143 | keiner. `SCHWELLE_ENTWICKLUNG` (0,1) fragt, ob der Katalog einen Hebel ab 10 % enthält, nicht, ob alle beschlossenen und weiterreichenden Maßnahmen das Ziel erreichen. | trägt nicht |
| A4 | Dritte Frage: „Wie sicher sind die getroffenen Aussagen?“ Die Gesamtgewissheit kombiniert die Gewissheit der Bewertung des Klimarisikos ohne Anpassung mit der Gewissheit der Bewertung der Anpassungskapazität (Skalenwerte 0–3); „mittel“ gilt erst ab einem Mittelwert über 1,5. | 140, 141 | `gewissheit.py`, `gewissheitsstufe()` (Evidenzklassen der Parameter der Schadensrechnung); `AUSREICHENDE_GEWISSHEIT` in `charakterisierung.py` | trägt teilweise |
| A5 | Fünf Gruppen: I Umsetzung, II Entwicklung, III Entwicklung unter Unsicherheit, IV Innovation, V Innovation unter Unsicherheit. Die beiden Varianten „unter Unsicherheit“ gibt es nur zu Entwicklung und Innovation. | 140–141 | `charakterisierung.py`, `CHARAKTERISIERUNGSGRUPPEN` und `ENTSCHEIDUNGSTABELLE`; `test_charakterisierungsgruppen.py`, `test_konstanten_fuenf_gruppen` und `test_tabelle_ueberdeckt_alle_eingaben_eindeutig` | trägt |
| A6 | Jede Gruppe benennt ein Handlungserfordernis: die Umsetzung sicherstellen (Finanzierung, Monitoring, Einbindung der Akteure); weiterreichende Maßnahmen entwickeln und in die Planung aufnehmen, auch „high-regret“; Forschung, bevor weiterreichende Maßnahmen aufgegriffen werden; tiefgreifende Anpassung und ein fachlicher und gesellschaftlicher Diskurs; intensive Forschung zu weiterreichender und tiefgreifender Anpassung. | 140–141 | `catalog.py`, `get_charakterisierungsgruppen()`: liefert den Gruppennamen, aber keinen Text zum Handlungserfordernis | trägt teilweise |
| A7 | Normative Vorgabe der beispielhaften Zuordnung: Im optimistischen Fall soll ein gering-mittleres Restrisiko nicht überschritten werden, im pessimistischen Fall wird ein mittleres angestrebt; „eine mittlere Gesamtgewissheit reicht aus“, um nicht in eine Gruppe „unter Unsicherheit“ zu fallen. | 141 | `charakterisierung.py`, `SCHWELLEN` (Wert, „Abschätzung von KAP3“, Herleitung, Band, Sensitivität) und `AUSREICHENDE_GEWISSHEIT` | trägt teilweise |
| A8 | Die Zuordnung „reagiert in hohem Maße sensitiv“ auf das akzeptierte Restrisiko und die gewünschte Gewissheit. Eine Sensitivitätsanalyse weist robuste Zuordnungen aus: Bei einer Gewissheitsschwelle über 1 bleiben vier Klimawirkungen auf Forschung angewiesen, bei über 1,5 kommen neun hinzu. Beim Zielwert „gering-mittel“ auch im pessimistischen Fall reichen die beschlossenen Maßnahmen nur noch für eine Klimawirkung aus, bei „gering“ erreicht nur die Schiffbarkeit das Ziel. | 141, 143–144 | `SCHWELLEN`, Felder `band` und `sensitivitaet` (nur als Text, ohne Rechnung) | trägt teilweise |
| A9 | Ausnahme: Bei „Allergische Reaktionen durch Aeroallergene pflanzlicher Herkunft (z. B. Pollen)“ und „Belastung oder Versagen von Hochwasserschutzsystemen“ erfolgt die Bewertung auf Basis der beschlossenen Maßnahmen (APA III); diese sind ausschlaggebend für die Zuordnung (Fn. 28, Fn. 29). | 141, 143 | keiner | trägt nicht |
| A10 | Tabelle 27 weist die Gruppen beispielhaft zu. Für die Klimawirkungen des Katalogs: Hitzebelastung „Entwicklung“, Allergische Reaktionen durch Aeroallergene „Umsetzung“, UV-bedingte Gesundheitsschädigungen „Entwicklung“ (alle Handlungsfeld „Menschliche Gesundheit“). Im Produkt stimmt nur #95 (Entwicklung, beide Codes). Abweichungen: #96 KWRA „Umsetzung“ (S. 142, Tab. 27; Ausnahme S. 143, Fn. 29), Produkt „Innovation“; #98 KWRA „Entwicklung“ (S. 142, Tab. 27), Produkt „Innovation“. | 142 (Tab. 27), 143 | `charakterisierungen()`, ausgeliefert über `GET /catalog/charakterisierungsgruppen`; `regel()`, Feld `modellgrenze` | trägt teilweise |

**Begründung je Urteil:**

- A1: Das Produkt filtert nicht nach Dringlichkeit, sondern ordnet jeden Katalogcode ein. Im heutigen
  Katalog fällt das nicht auf, weil alle drei gerechneten Klimawirkungen in Tabelle 25 stehen (S. 138).
  Eine vierte Klimawirkung ohne sehr dringende Handlungserfordernisse bekäme trotzdem eine Gruppe. Eine
  Einstufung nach Dringlichkeit führt das Produkt nicht (Zeile 6). Die übrigen 26 Klimawirkungen aus
  Tabelle 27 stehen nicht im Katalog; sie zu zählen, ist Sache von T-0821-ceo und T-0830-ceo.
- A2: Die Schwelle 0,5 ist eine ausgewiesene Übertragung des Restrisikoziels auf eine relative
  Minderung. Das Produkt trennt aber weder beschlossene von weiterreichenden Maßnahmen, noch kennt es
  einen optimistischen und einen pessimistischen Fall. Es misst nur, was der Katalog an verknüpften
  Maßnahmen hinterlegt.
- A3: Kern der Abweichung. In der KWRA sagt „Innovation“, dass selbst alle Maßnahmen nicht reichen. Im
  Produkt heißt „Innovation“ nur, dass der Katalog keinen verknüpften Hebel ab 10 % enthält; bei p = 0
  heißt es, dass gar keine Maßnahme verknüpft ist. Damit benennt das Produkt für #96 und #98 einen
  Handlungstyp (tiefgreifende Anpassung), den die KWRA für diese beiden Klimawirkungen gerade nicht
  benennt.
- A4: Die Skala stimmt, und „mittel“ reicht wie in der KWRA. Die Stufe des Produkts beruht aber nur auf
  den Belegen der Schadensparameter. Eine Gewissheit der Anpassungskapazität geht nicht ein, obwohl sie
  in der KWRA die Hälfte der Gesamtgewissheit ausmacht.
- A5: Namen und Aufbau stimmen wörtlich. „Umsetzung“ hat wie in der KWRA keine Unsicherheitsvariante.
- A6: Der Gruppenname trägt den Handlungstyp nur als Schlagwort. Was die KWRA je Gruppe als
  Handlungserfordernis beschreibt, gibt die API nicht aus. Ob es im Frontend angezeigt wird, ist nicht
  Gegenstand dieser Gegenprobe (Sichtbarkeit, T-0483).
- A7: Die Gewissheitsvorgabe ist wörtlich übernommen. Das Restrisikoziel ist durch eine Abschätzung von
  KAP3 ersetzt, mit Herleitung, Band und Sensitivität; das erfüllt Vorgabe P1. Das Ziel für den
  optimistischen Fall (gering-mittel) hat keine Entsprechung.
- A8: Band und Sensitivität stehen als Text in `SCHWELLEN`. Eine Rechnung, welche Zuordnung an den
  Bandenden stabil bleibt, gibt es nicht. Nachgerechnet mit den Werten oben: Über beide Bänder
  (0,4–0,6 und 0,05–0,2) bleibt #95 bei 0,259 in „Entwicklung“, #96 und #98 bei 0 in „Innovation“.
  Die Gewissheitsschwelle ist im Produkt fest.
- A9: Genau diese Ausnahme betrifft #96. Die KWRA stützt „Umsetzung“ für die Allergien auf die
  beschlossenen Maßnahmen des Bundes (APA III). Das Produkt kennt keine beschlossenen Maßnahmen als
  eigene Größe, daher fehlt die Ausnahme.
- A10: Die Abweichung ist zum Teil ausgewiesen: `regel()["modellgrenze"]` sagt allgemein, die Gruppe
  „kann … abweichen“, und die Schwellen sind nach P1 als Abschätzung gekennzeichnet. Nicht ausgewiesen
  ist die Ursache je Klimawirkung, und die liegt nicht bei den Schwellen. Sie liegt bei fehlenden
  Maßnahmen im Rechenweg:
  - #96: Der Methodik-Bericht `docs/methodik/96_aeroallergene.md` hat zwei Hebel mit Wirkung. Der erste
    ist die Pollen-Frühwarnung S158 mit r = 0,03 (Band 0,005–0,10) als Abschätzung nach Vorgabe P2
    (§5.1). Sie bleibt nach Integrationsauflage aus Befund 124 absichtlich ohne `linked_risk_codes`;
    selbst verknüpft läge sie mit 0,03 unter 0,1. Der zweite ist die allergenarme Stadtbaumwahl mit 14 %
    je Zelle; sie wirkt nur als Umverteilung und ist keine Katalogmaßnahme (§5).
  - #98: `docs/methodik/98_uv_schaedigungen.md` führt beide Hebel nur qualitativ (§5, Entscheidungslog 12).
    Die UV-Schutzprogramme S155 haben keine Effektgröße, die Früherkennung S158 steckt schon im Basiswert
    (Befund 203).

  Zum angemeldeten Zweifel heißt das: Es ist keine reine Modellgrenze der Schwellen. Das Anpassungspotenzial
  0 für #96 und #98 heißt „keine wirkende Maßnahme im Rechenweg“, nicht „Anpassung reicht nicht“. Das
  Produkt liest es aber als Gruppe „Innovation“ und stellt damit die Lage anders dar als die KWRA.
  Bei den Zahlen bemerkt: Der Text auf S. 142 nennt vier Klimawirkungen in „Umsetzung“, Tabelle 27
  (als Bild angesehen) führt drei. „Abiotischer Stress (Pflanzen)“ steht dort in „Entwicklung“.

Nicht als Anforderung an die Einordnung gewertet: der zweite Teil von Kap. 6.2, „Charakterisierung
aufgrund der Anpassungsdimensionen“ (S. 144–145). Er beschreibt eine eigene Auswertung der sechs
Anpassungsdimensionen und ordnet nicht in Gruppen ein.

**Gelesene Seiten und Abschnitte:** Inventar mit `python3 /opt/overlord/overlord/skripte/dokumente.py
inventar` (172 Seiten). Inhaltsverzeichnis S. 6–7 ganz überflogen. Kap. 6.2 „Charakterisierung der
Handlungserfordernisse“ S. 140–145 vollständig im Text gelesen, einschließlich Fußnote 28 (S. 141) und
Fußnote 29 (S. 143). Dazu das Ende von Kap. 6.1 oben auf S. 140 und S. 146 mit dem Beginn von Kap. 7
(Kapitelgrenze geprüft). Tabelle 25 „31 Klimawirkungen mit sehr dringenden Handlungserfordernissen“
(S. 138, Kap. 6.1) im Text gelesen, weil A1 sich auf sie stützt. Als Bild angesehen: S. 142 mit
Tabelle 27 „Kategorien von sehr dringenden Handlungserfordernissen“, ganz übernommen: 3 in Umsetzung,
10 in Entwicklung, 4 in Entwicklung mit Unsicherheit, 3 in Innovation, 9 in Innovation unter
Unsicherheit, zusammen 29. Kap. 6.2 enthält keine weitere Tabelle oder Abbildung. Nicht gelesen:
Kap. 5 (Anpassungskapazität, Tabellen 21–24), auf dem Kap. 6.2 aufbaut; Tabelle 26; Teilbericht 1,
auf den Fn. 28 für die Gesamtgewissheit verweist. Im Produkt gelesen: `docs/methodik/96_aeroallergene.md`
§5 und §5.1 (Kopf) sowie Entscheidungslog 15, 19 und 20; `docs/methodik/98_uv_schaedigungen.md` die
Hebelzeilen S155 und S158, Register 98-S155-01 und 98-S158-01, §5 und Entscheidungslog 12.

**Schluss:** Zeile 7 bleibt nicht `erfüllt`. Von 10 Anforderungen trägt der Bestand eine voll (A5),
sieben teilweise (A1, A2, A4, A6, A7, A8, A10) und zwei nicht (A3, A9). Nur eine der drei Klimawirkungen
des Katalogs (#95) landet in der Gruppe der KWRA. Der Status der Zeile 7 ist in derselben Änderung
auf `teilweise` gesetzt, die Spalte „Lücke“ nennt, was fehlt. Die Zählungen in den Abschnitten
„Nachtrag: Abschlusszählung“ und „Zusammenfassung“ sind damit weiter überholt; sie nachzuziehen ist
Sache der Gesamtzählung (T-0821-ceo, T-0487), nicht dieser Gegenprobe.

### Gegenprobe Zeile 19 gegen UBA-Handlungsempfehlungen zur ISO 14091, Abschnitt 2.2.6

Frage: Tragen die Belege der Zeile 19 das, was Abschnitt 2.2.6 „Ergebnisse interpretieren“ verlangt — und
darf „handlungsfeldübergreifend“ gelten, solange der aktive Katalog nur ein Handlungsfeld hat? Gelesen wurde
gegen die Sekundärquelle Umweltbundesamt (Porst, Voß, Kahlenborn, Schauser), „Klimarisikoanalysen auf
kommunaler Ebene – Handlungsempfehlungen zur Umsetzung der ISO 14091“, Juni 2022, 40 Seiten, abgerufen am
25.09.2026 von
https://www.umweltbundesamt.de/system/files/medien/479/publikationen/2022_uba-fachbroschuere_kra_auf_kommunaler_ebene.pdf
(Verweis von der Publikationsseite in der Spalte „Quelle“). Die Datei liegt nicht im Repo. PDF-Seitenzahl und
gedruckte Seitenzahl stimmen überein. Abschnitt 2.2.6 beginnt auf S. 29 in der rechten Spalte und endet auf
S. 30 in der linken Spalte, rechts beginnt dort 2.3; die Fundstelle „S. 29f.“ stimmt. Fußnote 27 (S. 20) ordnet
Abschnitt 2.2 dem Kapitel 6 der ISO 14091 zu; auch die Angabe „Kap. 6“ stimmt.

**Befund Primärquelle:** Der Normtext ISO 14091:2021 wurde nicht gelesen. Er wird nicht gekauft; das
Menschenticket T-0531-ceo ist offen. Die Tabelle stützt sich allein auf die Wiedergabe durch das UBA. Die
Broschüre spricht in „sollte“ und „empfehlenswert“, nicht in „ist zu“; die Zeile 19 verschärft das zu einer
Pflicht.

Im Produkt wurden `backend/app/services/unsicherheits_zusammenschau.py` und
`backend/tests/test_unsicherheits_zusammenschau.py` vollständig gelesen, die Route
`GET /api/kommune/{kommune_id}/unsicherheits-zusammenschau` in `backend/app/api/routes/kommune.py` im Kopf.
`unsicherheits_zusammenschau(1)` wurde einmal ausgeführt, ohne etwas zu ändern. Ergebnis: genau ein
Handlungsfeld, „Menschliche Gesundheit“, niedrigste Gewissheit „mittel“ (EXPECTED_ANNUAL_MORTALITY,
EXPECTED_ANNUAL_ALLERGY_DAYS), 2 nicht belegte Parameter, Vorsichtsliste leer, `hinweis` = `None`. Alle vier
Codes des Katalogs (#95 zweimal, #96, #98) tragen `kwra_field` „Menschliche Gesundheit“.

| Nr | Anforderung (Wortlaut oder enge Wiedergabe) | Seite | tragender Beleg (Datei, Funktion oder Abschnitt) | Urteil |
|---|---|---|---|---|
| A1 | „Im letzten Schritt der Durchführung einer KRA geht es darum, die identifizierten Risiken zu interpretieren und einzuordnen, um Antworten auf die zu Beginn formulierten Leitfragen zu liefern.“ | 29 | keiner. Das Produkt kennt keine Leitfragen der Kommune (Abschnitt 2.1.1 „Ziele und Ergebnisse definieren“). | trägt nicht |
| A2 | „Bestehende Unsicherheiten in den zugrundeliegenden Informationen und Daten sollten in der Interpretation der Ergebnisse … berücksichtigt werden.“ | 29 | `unsicherheits_zusammenschau.py`, `unsicherheits_zusammenschau()` (niedrigste Gewissheitsstufe und Zahl nicht belegter Parameter je Handlungsfeld, Hinweis ab „gering“); `gewissheit.py`, `gewissheitsstufe()`; `docs/evidenz/register.md` (Evidenzklasse je Parameter) | trägt |
| A3 | Die Unsicherheiten sollten „wie auch in der Formulierung von Handlungsoptionen berücksichtigt werden“. | 29 | `charakterisierung.py`, Gruppen „… unter Unsicherheit“ (Gewissheit geht in den Handlungstyp ein); Hinweistext `HINWEIS_VORSICHT` | trägt teilweise |
| A4 | „Eine handlungsfeld- und regionsübergreifende Betrachtung der Ergebnisse hilft, wechselseitige Abhängigkeiten zu identifizieren und die geeignetsten Maßnahmen zu identifizieren.“ Hier: der handlungsfeldübergreifende Teil. | 30 | `querverbindungen.py`, `querverbindungs_auswertung()` (KWRA-Querverbindungen zwischen Klimawirkungen, Zeile 9); nicht `unsicherheits_zusammenschau()` | trägt teilweise |
| A5 | Derselbe Satz, regionsübergreifender Teil: wechselseitige Abhängigkeiten über die Grenze der Kommune hinweg. | 30 | keiner. Der Kopf von `unsicherheits_zusammenschau.py` schließt einen Vergleich zwischen Kommunen ausdrücklich aus. | trägt nicht |
| A6 | „Da Klimaanpassung auch in Kommunen ein Querschnittsthema darstellt, sollten für die Interpretation der Ergebnisse der KRA verschiedene kommunale Fachabteilungen sowie externe Expertise einbezogen werden.“ | 30 | keiner. `kang_beruecksichtigung.py` zeigt je KAnG-Handlungsfeld Risiken und Maßnahmen einer Planung, bezieht aber niemanden ein. | trägt nicht |
| A7 | „Zudem ist empfehlenswert, Gender- und Diversitätsaspekte zu berücksichtigen.“ | 30 | `backend/app/data/bestandsaufnahme.py` (vulnerable Personen: Ältere ab 65 Jahren, alleinlebende Ältere); `docs/methodik/95_hitzebelastung.md` (Alters- und Geschlechtsschichtung in der Rechnung) | trägt teilweise |
| A8 | „Der priorisierte Handlungsbedarf, als zentrales Ergebnis einer KRA, ist die Grundlage für eine Maßnahmenplanung.“ | 30 | `charakterisierung.py`, `charakterisierungen()` (Zeile 7); `frontend/src/pages/roadmap/roadmapData.ts` (Zeile 6) | trägt teilweise |
| A9 | Es „sollte erörtert werden, welche Handlungsoptionen auf kommunaler Ebene bestehen und ggf. welche Optionen der Zusammenarbeit mit Akteur*innen außerhalb der Kommune bedürfen. Dabei ist auch die Aufteilung der Verwaltungsverantwortung … auf mehrere Ebenen (Stadt/Gemeinde, Landkreis, Bundesland) zu berücksichtigen.“ | 30 | `backend/app/data/kang_zustaendigkeit.py` (zuständige Stelle je Land, Zeile 14); `catalog.MEASURES` (drei Maßnahmen) | trägt teilweise |
| A10 | „Relevante lokale Akteur*innen, ggf. auch von angrenzenden Kommunen oder Ländervertreter*innen, sollten dabei frühzeitig mit einbezogen werden.“ | 30 | keiner (vgl. Zeile 17, `offen`) | trägt nicht |

**Begründung je Urteil:**

- A1: Leitfragen legt die Kommune in der Vorbereitung fest. Das Produkt fragt sie nicht ab und ordnet die
  Ergebnisse keiner Leitfrage zu.
- A2: Das trägt der Kern der Zeile 19. Die Zusammenschau fasst die Unsicherheit der Daten (Evidenzklassen
  der Parameter) über die Klimawirkungen eines Handlungsfelds zusammen und benennt den Fall, der vorsichtige
  Interpretation verlangt. Ob sie im Frontend angezeigt wird, ist nicht Gegenstand dieser Gegenprobe
  (Sichtbarkeit, T-0483); im Frontend ruft heute nichts den Endpunkt auf.
- A3: Die Gewissheit fließt über die Charakterisierungsgruppen in den Handlungstyp ein, und der Hinweistext
  nennt die Handlungsoptionen. Eine Verbindung von Unsicherheit und einzelner Maßnahme gibt es nicht: Die
  Zusammenschau ist ein eigener Endpunkt, nichts stellt sie vor die Maßnahmenwahl. Der Hinweis erscheint
  heute gar nicht, weil die niedrigste Stufe „mittel“ ist.
- A4: Die Zusammenschau stellt Handlungsfelder nur nebeneinander. Wechselseitige Abhängigkeiten ermittelt sie
  nicht, auch nicht bei mehreren Handlungsfeldern. Mit einem einzigen Handlungsfeld gibt es nichts, das
  übergreifend betrachtet werden könnte. Teilweise trägt nur die Übernahme der KWRA-Querverbindungen
  (Zeile 9): Sie zeigt bundesweite Beziehungen zwischen Klimawirkungen verschiedener Handlungsfelder, aber
  keine Abhängigkeiten zwischen den gerechneten Ergebnissen der Kommune.
- A5: Das Produkt rechnet je Kommune. Abhängigkeiten zu Nachbarkommunen oder zur Region (etwa
  Oberlieger und Unterlieger beim Hochwasser) werden weder ermittelt noch angezeigt.
- A6: Einbeziehen ist ein Schritt im Verfahren. Das Produkt bietet dafür nichts, wie schon bei Zeile 17.
  Die Nachweisrechnung nach § 8 KAnG liefert höchstens eine Vorarbeit: welche Felder betroffen sind.
- A7: Diversität steckt über Alter und Alleinleben in der Bestandsaufnahme und in der Rechnung zu #95. In der
  Interpretation, also in der Zusammenschau, spielt sie keine Rolle; Geschlecht geht nur in die
  Lebenserwartung der Rechnung ein, nicht als Aspekt der Betroffenheit.
- A8: Wie zu Zeile 6 und 7: Eine Einordnung in Charakterisierungsgruppen gibt es, eine aus Klimarisiko und
  Anpassungsdauer hergeleitete Priorisierung je Klimawirkung nicht.
- A9: Die Zuständigkeitstabelle klärt, ob Gemeinde oder Landkreis ein Klimaanpassungskonzept aufstellt. Eine
  Unterscheidung der Maßnahmen danach, ob die Kommune sie allein umsetzen kann oder Partner außerhalb braucht,
  gibt es nicht.
- A10: Wie A6, ein Verfahrensschritt ohne Gegenstück im Produkt.

Nicht als eigene Anforderung gewertet: die Hinweisbox „Empfehlung für eher kleine Kommunen und/oder Kommunen
mit begrenzten Ressourcen“ (S. 30, unter den Punkten von 2.2.6). Sie beschreibt eine vereinfachte
Ersatzbewertung (dreistufig gering, mittel, hoch, dazu die Dringlichkeit) und fügt der Interpretation nichts
hinzu. Ebenso nicht: die Bewertung der Dringlichkeit am Ende von 2.2.4 (S. 28), auf die A8 aufbaut; sie ist
Gegenstand von Zeile 6.

**Gelesene Seiten und Abschnitte:** Inventar mit `python3 /opt/overlord/overlord/skripte/dokumente.py
inventar` (40 Seiten). Inhaltsverzeichnis S. 5 ganz. Einführung S. 7–9 ganz, einschließlich des Hinweises auf
S. 8, dass jedem Teilkapitel eine Kurzfassung des ISO-Abschnitts vorangestellt ist, und der Infobox
„Klimarisikoanalysen (KRA)“ mit Abbildung 1 auf S. 9 (im Text). S. 20 mit dem Beginn von 2.2, Fußnote 27
und Abbildung 4 (im Text). S. 28–29 mit dem Ende von 2.2.4, Tabelle 4 und Abschnitt 2.2.5 samt Tabelle 5
(Kapitelgrenze geprüft). Abschnitt 2.2.6 S. 29–30 vollständig im Text gelesen; S. 30 zusätzlich als Bild
angesehen, um die Zuordnung der Hinweisbox und die Grenze zu 2.3 zu klären. S. 31 mit 2.3.2 (Ende der
Nachbarabschnitte). Abschnitt 2.2.6 enthält keine Tabelle und keine Abbildung. Nicht gelesen: 2.1.1 (Leitfragen,
auf die A1 verweist), 2.2.1–2.2.3, Kapitel 3 und 4 der Broschüre; der Primärtext der ISO 14091.

**Schluss:** Zeile 19 bleibt nicht `erfüllt`. Von 10 Anforderungen trägt der Bestand eine voll (A2), fünf
teilweise (A3, A4, A7, A8, A9) und vier nicht (A1, A5, A6, A10). Der Status der Zeile 19 ist in derselben
Änderung auf `teilweise` gesetzt; die Spalte „Lücke“ nennt, was fehlt. Zum angemeldeten Zweifel: Nein, die
Zeile darf nicht als `erfüllt` gelten, solange der aktive Katalog nur ein Handlungsfeld hat. Eine
Zusammenschau über ein Handlungsfeld ist nicht handlungsfeldübergreifend. Auch mit mehreren Handlungsfeldern
reichte sie nicht, denn sie stellt die Felder nur nebeneinander und ermittelt keine wechselseitigen
Abhängigkeiten. Die regionsübergreifende Betrachtung fehlt ganz. Die Zählungen in den Abschnitten „Nachtrag:
Abschlusszählung“ und „Zusammenfassung“ sind damit weiter überholt; sie nachzuziehen ist Sache der
Gesamtzählung (T-0821-ceo, T-0487), nicht dieser Gegenprobe.

### Gegenprobe Zeile 8 gegen KWRA 2021, Teilbericht 6, Kap. 3.3

Frage: Tragen die drei in Zeile 8 genannten Belege, was Kap. 3.3 „Handlungsfeldübergreifende Auswertung der
Gewissheit“ an die Bewertungsgewissheit stellt? Und passen Skala und Herleitung der KWRA zur Ableitung im Produkt aus
den Evidenzklassen der Parameter? Zeile 8 steht seit T-0446 auf `erfüllt`, weil die Belegdateien existieren; der
Normtext war dafür nicht gelesen worden. Gelesen wurde gegen
`docs/KWAR/kwra2021_teilbericht_6_integrierte_auswertung_bf_211027_0.pdf`. Im Kap. 3.3 stimmen PDF-Seitenzahl und
gedruckte Seitenzahl überein. Das Kapitel beginnt auf S. 78 und endet auf S. 82 mit dem letzten Punkt der Kernaussagen;
danach beginnt auf derselben Seite Kap. 3.4. Die Fundstelle „S. 78–82“ stimmt.

Im Produkt wurden `backend/app/services/gewissheit.py` und `backend/tests/test_gewissheitsstufe.py` vollständig
gelesen, in `backend/app/api/routes/catalog.py` die Route `GET /catalog` (Feld `certainty` je Risiko). Dazu die
Stellen, die die Stufe weiterverwenden: `unsicherheits_zusammenschau.py` (`VORSICHT_STUFEN`, `HINWEIS_VORSICHT`) und
`charakterisierung.py` (`AUSREICHENDE_GEWISSHEIT`). `gewissheit.gewissheitsstufen()` wurde einmal ausgeführt, ohne
etwas zu ändern. Ergebnis mit Zahl belegter Parameter je Risiko:

| Risikocode | Klimawirkung | belegt / alle Parameter | Stufe im Produkt |
|---|---|---|---|
| EXPECTED_ANNUAL_MORTALITY | #95 Hitzebelastung | 25 / 26 (abgeschätzt: `beta_dist_km`) | mittel |
| EXPECTED_ANNUAL_MORBIDITY | #95 Hitzebelastung | 8 / 8 | hoch |
| EXPECTED_ANNUAL_ALLERGY_DAYS | #96 Aeroallergene | 20 / 21 (abgeschätzt: `birch_group_share_default`) | mittel |
| EXPECTED_ANNUAL_UV_YLL | #98 UV-Schädigungen | 30 / 30 | hoch |

Alle vier Codes gehören zum Handlungsfeld „Menschliche Gesundheit“. Im Frontend liest heute nichts das Feld
`certainty`. Ob die Stufe angezeigt wird, ist nicht Gegenstand dieser Gegenprobe (Sichtbarkeit, T-0483).

| Nr | Anforderung (Wortlaut oder enge Wiedergabe) | Seite | tragender Beleg (Datei, Funktion oder Abschnitt) | Urteil |
|---|---|---|---|---|
| A1 | „Die Gewissheit wurde für alle Klimawirkungen … bestimmt. Der Wertebereich umfasste eine vierstufige Skala von ‚sehr gering‘, ‚gering‘, ‚mittel‘ und ‚hoch‘.“ | 78 | `gewissheit.py`, `GEWISSHEITSSTUFEN` und `gewissheitsstufen()` (eine Stufe für jeden Code aus `catalog.RISKS_BY_CODE`); `catalog.py`, `get_catalog()`, Feld `certainty`; `test_gewissheitsstufe.py`, `test_jeder_risikocode_hat_eine_stufe_der_skala` | trägt |
| A2 | Die Gewissheit wird je Zeitscheibe bestimmt: „für die beiden Zeitscheiben Mitte des Jahrhunderts (2031 bis 2060) und Ende des Jahrhunderts (2071 bis 2100)“. | 78 | keiner. `gewissheitsstufe()` liefert je Risikocode genau einen Wert ohne Zeitbezug. | trägt nicht |
| A3 | Die Bewertung der Gewissheit stützt sich auf fünf Teilaspekte: „Vorhandensein von Daten, die Zuverlässigkeit der verwendeten Daten, Kenntnisse über Wirkzusammenhänge, Genauigkeit und Plausibilität von Modellannahmen, die Eindeutigkeit von Trends“ (gleichlautend im Glossar, S. 13). | 78 | `gewissheit.py`, `gewissheitsstufe()`: Anteil der Parameter mit `evidence_class == "belegt"`, Schnitt `SCHWELLE_MITTEL` = 0,5 (Abschätzung von KAP3) | trägt teilweise |
| A4 | Die Gewissheiten werden gemittelt, über alle Klimawirkungen und je Handlungsfeld, getrennt nach Zeitscheibe und nach aufsteigender Gewissheit geordnet (Tabelle 17), dazu je Cluster (Wasser, Land und Wirtschaft niedriger als die übrigen). Für die Mittelung wird die Skala als Zahl dargestellt (1 = sehr gering bis 4 = hoch); weil das eine „künstliche Spezifizierung“ ist, wird „der eigentliche Grad der Gewissheit … zusätzlich aufgeführt“ (Fn. 18). | 78, 79, 80 | `unsicherheits_zusammenschau.py`, `unsicherheits_zusammenschau()`: niedrigste Stufe je Handlungsfeld, kein Mittelwert, keine Cluster, keine Zeitscheibe | trägt teilweise |
| A5 | Klimawirkungen und Handlungsfelder „mit besonders hoher oder geringer Gewissheit herausstellen“ (im Text benannt: sehr geringe Gewissheit etwa bei „UV-bedingte Gesundheitsschädigungen“ zum Ende des Jahrhunderts; vergleichsweise hohe, gemittelt 3,5, etwa bei „Hitzebelastung“). | 78, 79 | `catalog.py`, Feld `certainty` je Risiko; `unsicherheits_zusammenschau.py`, Liste der Handlungsfelder ab „gering“ | trägt teilweise |
| A6 | „Änderungen der Gewissheiten zwischen den betrachteten Zeitscheiben hervorheben“ (etwa „Menschliche Gesundheit“: „nimmt … die Sicherheit bei der Bewertung zum Ende des Jahrhunderts … stark ab“, Tabelle 17: 3,4 mittel zu 2,1 gering). | 78, 79, 80 | keiner (ohne Zeitscheibe, A2) | trägt nicht |
| A7 | Aufzeigen, wo „die ermittelten Klimarisiken noch hohen Unsicherheiten unterliegen und daher vorsichtig interpretiert werden sollten“. | 78 | `unsicherheits_zusammenschau.py`, `VORSICHT_STUFEN` und `HINWEIS_VORSICHT` (Hinweis ab Stufe „gering“) | trägt teilweise |
| A8 | Aufzeigen, wo „aufgrund von geringen Gewissheiten noch weiterführender Forschungsbedarf besteht“ (Kernaussage: „Hier besteht insbesondere weiterer Forschungsbedarf“). | 78, 79, 81 | keiner | trägt nicht |
| A9 | „Gleichzeitig können auf diese Weise auch verbesserte Aussagen zu möglichen Handlungserfordernissen getroffen werden (siehe Kapitel 6).“ | 78 | `charakterisierung.py`, `charakterisierungsgruppe()` mit `AUSREICHENDE_GEWISSHEIT` (Gruppen „… unter Unsicherheit“, Zeile 7) | trägt teilweise |
| A10 | Die Gewissheit wird der Höhe des Klimarisikos gegenübergestellt: gemittelte Gewissheit der hoch, mittel und gering bewerteten Klimarisiken je Zeitscheibe und für den optimistischen und pessimistischen Fall, mit der Zahl der Klimawirkungen je Gruppe (Abbildung 7; Fn. 19 zur Stichprobengröße). | 80, 81 | keiner | trägt nicht |
| A11 | Empfehlung für künftige Analysen: „eine detailliertere Aufschlüsselung der Gewissheit, beziehungsweise eine direkte Bewertung der Teilaspekte der Gewissheit“, um „passgenauer Hinweise auf mögliche Wissenslücken geben zu können“. | 81 | `gewissheit.py` über `evidence_class` je Parameter; `docs/evidenz/register.md` (Evidenzklasse je Parameter) | trägt teilweise |

**Begründung je Urteil:**

- A1: Skala und Stufennamen stimmen wörtlich mit S. 78 überein, und jede Klimawirkung des Katalogs trägt genau eine
  Stufe. Der Test sichert das für jeden Code ab.
- A2: Die KWRA kennt keine Gewissheit ohne Zeitscheibe. Das Produkt kennt keine Zeitscheibe der Gewissheit. Welcher
  Zeitscheibe die Stufe des Produkts entsprechen soll, ist nirgends gesagt.
- A3: Das ist der Kern der Frage nach der Herleitung. Die Skala passt, die Herleitung nicht. Die Regel des Produkts
  misst nur, ob ein Rechenparameter eine Quelle hat. Das berührt die ersten beiden Teilaspekte (Vorhandensein und
  Zuverlässigkeit der Daten) und nur für die Parameter, nicht für die Daten des Klimasignals. Kenntnis der
  Wirkzusammenhänge, Plausibilität der Modellannahmen und Eindeutigkeit der Trends gehen nicht ein. Eine Quelle für
  einen Parameter sagt nichts darüber, wie sicher die Zukunftsaussage ist. Das Ergebnis weicht deshalb bei den
  Klimawirkungen des Katalogs von der KWRA ab: #98 UV-Schädigungen hat 30 von 30 Parametern belegt und steht auf
  „hoch“. Die KWRA nennt „UV-bedingte Gesundheitsschädigungen“ zum Ende des Jahrhunderts unter den sieben
  Klimawirkungen mit „sehr gering“ (S. 78). Umgekehrt senkt bei #95 Hitzebelastung (Mortalität) ein einziger
  abgeschätzter Parameter von 26 die Stufe auf „mittel“, während die KWRA „Hitzebelastung“ mit gemittelt 3,5 über
  beide Zeitscheiben zu den Klimawirkungen mit vergleichsweise hoher Gewissheit zählt (S. 78–79). Die Stufe
  „hoch“ verlangt im Produkt, dass alle Parameter belegt sind. Sie ist also ein Randfall der Regel, keine Einstufung
  der Aussagesicherheit. Zudem nennt der Kopf von `gewissheit.py` Tabelle 17 als Ausweis „je Klimawirkung“; Tabelle 17
  zeigt aber Mittelwerte je Handlungsfeld (S. 80).
- A4: Die Zusammenschau fasst je Handlungsfeld zusammen, aber mit dem Minimum statt dem Mittel. Das ist eine
  vertretbare, vorsichtigere Wahl, aber nicht die Auswertung der Tabelle 17. Cluster und Zeitscheiben fehlen. Mit nur
  einem Handlungsfeld im Katalog gibt es nichts handlungsfeldübergreifend zu vergleichen (wie bei Zeile 19, A4).
  Tabelle 17 ordnet die Mittelwerte dem Grad durch Runden zu (2,4 gering, 2,6 mittel); das Produkt rechnet keine
  Mittelwerte und braucht diese Zuordnung heute nicht.
- A5: Die Stufe je Klimawirkung steht in der API. Herausgestellt wird nichts: keine Rangfolge, keine Hervorhebung
  der Klimawirkungen mit besonders hoher oder geringer Gewissheit. Die Zusammenschau hebt nur Handlungsfelder ab
  „gering“ hervor. Wegen A3 würde sie #98 nicht hervorheben, obwohl die KWRA es tut.
- A6: Ohne Zeitscheibe gibt es keine Änderung zwischen Zeitscheiben. Für das einzige Handlungsfeld des Katalogs ist
  genau dieser Wechsel der auffälligste Befund der KWRA (Tabelle 17, Text S. 79).
- A7: Der Hinweis zur vorsichtigen Interpretation ist vorhanden und hängt an der richtigen Grenze („gering“). Er
  greift heute aber nie, weil die niedrigste Stufe im Katalog „mittel“ ist. Nach der KWRA stünde das Handlungsfeld
  „Menschliche Gesundheit“ zum Ende des Jahrhunderts auf „gering“ (Tabelle 17) und verlangte diesen Hinweis.
- A8: Forschungsbedarf leitet die Bundesanalyse für die Forschung ab (Kap. 8). Für ein Werkzeug der Kommune ist das
  nicht einschlägig. Die Anforderung geht deshalb nicht in die Lücke der Zeile 8 ein; A11 deckt den Teil ab, der für
  die Kommune zählt, nämlich die Wissenslücken der eigenen Rechnung.
- A9: Die Stufe geht in die Charakterisierungsgruppe ein. Sie trägt aber die Schwächen aus A2 und A3 mit, und die
  Gewissheit der Anpassungskapazität fehlt (siehe Zeile 7, Abschnitt „Gegenprobe Zeile 7“).
- A10: Einen Bezug zwischen Gewissheit und Höhe des Klimarisikos gibt es im Produkt nicht, auch keinen optimistischen
  und pessimistischen Fall.
- A11: Das Produkt schlüsselt nach Parametern auf: Das Evidenz-Register zeigt, welcher Parameter abgeschätzt ist. Das
  ist eine feinere Aufschlüsselung als die der KWRA, aber nicht nach den fünf Teilaspekten.

Nicht als eigene Anforderung gewertet: die Befunde der Bundesanalyse selbst, also die Mittelwerte 2,718 und 2,2
(S. 78), die Aussagen zu einzelnen Handlungsfeldern (S. 79) und die Kernaussagen (S. 81–82). Sie sind Ergebnisse,
keine Anforderungen, und dienen oben nur als Vergleich (A3, A5, A6, A7).

**Gelesene Seiten und Abschnitte:** Inventar mit `python3 /opt/overlord/overlord/skripte/dokumente.py inventar`
(172 Seiten). Inhaltsverzeichnis S. 6–7 ganz. Glossar S. 13, Eintrag „Gewissheit“ (über die Stichwortsuche auf
S. 12–17 gefunden, dann im Zusammenhang gelesen). S. 77 mit dem Ende von Kap. 3.2 (Kapitelgrenze geprüft). Kap. 3.3
S. 78–82 vollständig im Text gelesen, einschließlich Fußnote 18 (S. 78), Fußnote 19 (S. 80) und des Kastens
„Kernaussagen der handlungsfeldübergreifenden Auswertung der Gewissheit“ (S. 81–82); S. 82 bis zum Beginn von
Kap. 3.4 (Kapitelgrenze geprüft). Als Bild angesehen: S. 80 (Tabelle 17 „Durchschnittliche Gewissheiten und Grad der
Gewissheit der Bewertungen …“, alle 28 Werte samt Grad) und S. 81 (Abbildung 7 „Gemittelte Gewissheiten der
Bewertungen der Klimawirkungen mit hohem, mittleren und geringen Klimarisiko …“ mit den Fallzahlen je Zeitscheibe und
Fall). Kap. 3.3 enthält keine weitere Tabelle und keine weitere Abbildung. Nicht gelesen: die Zusammenfassung
(S. 18–29) und Kap. 1.3 „Methodisches Vorgehen“ dieses Teilberichts, Kap. 6 und 7, auf die Kap. 3.3 verweist, sowie
Teilbericht 1 („Methodik und Konzept“), der das Bewertungsverfahren der Gewissheit festlegt, und die
Handlungsfeldkapitel mit den Einzelwerten je Klimawirkung, darunter die Werte für #96 Aeroallergene.

**Schluss:** Zeile 8 bleibt nicht `erfüllt`. Von 11 Anforderungen trägt der Bestand eine voll (A1), sechs teilweise
(A3, A4, A5, A7, A9, A11) und vier nicht (A2, A6, A8, A10). Zur Frage nach Skala und Herleitung: Die Skala
passt wörtlich, die Herleitung nicht. Die Stufe im Produkt misst die Quellenlage der Rechenparameter, nicht die
Gewissheit des Klimarisikos, und kehrt bei #98 die Einstufung der KWRA um. Der Status der Zeile 8 ist in derselben
Änderung auf `teilweise` gesetzt; die Spalte „Lücke“ nennt, was fehlt. Die Zählungen in den Abschnitten „Nachtrag:
Abschlusszählung“ und „Zusammenfassung“ sind damit weiter überholt; sie nachzuziehen ist Sache der Gesamtzählung
(T-0821-ceo, T-0487), nicht dieser Gegenprobe.

### Gegenprobe Zeile 22 gegen UBA Methodenkonvention 4.0, Kap. 2.2.3

Frage: Tragen die Belege der Zeile 22, was Kap. 2.2.3 „Diskontierung und die Reine Zeitpräferenzrate“ an die
Diskontierung stellt? Verlangt die Konvention neben der Reinen Zeitpräferenzrate (RZPR) weitere Bestandteile der
Diskontrate, und entsprechen die berichteten Werte dem? Zeile 22 steht seit T-0443 auf `erfüllt`, weil die
Kostenprojektion Barwerte mit 0 % und 1 % RZPR ausweist; der Normtext war dafür nicht gelesen worden. Gelesen wurde
gegen `docs/UBA/UBA_Handbuch Umweltkosten_Methodenkonvention 4.0.pdf`. In den gelesenen Seiten stimmen PDF-Seitenzahl
und gedruckte Seitenzahl überein. Kap. 2.2.3 beginnt auf S. 14 und endet auf S. 15; Kap. 2.2.4 beginnt auf S. 16. Die
Fundstelle „S. 14f.“ stimmt.

Im Produkt wurden `backend/app/services/cost_projection_service.py` und
`backend/tests/test_kostenprojektion_diskontierung.py` vollständig gelesen, dazu in
`backend/app/services/climate/dwd_data.py` der Beginn von `_HOT_DAYS_PROJECTION_RCP45` (erstes Jahr 2025). Die
Kostenprojektion rechnet in `project_costs()`, innere Funktion `_discounted()`, für jede Rate aus
`PURE_TIME_PREFERENCE_RATES = (0.0, 0.01)` den Barwert mit dem Faktor 1/(1 + r)^(Jahr − 2025). Die Rate r ist die RZPR
selbst; eine weitere Komponente gibt es nicht. Die Reihe zu 0 % ist deshalb gleich der unabgezinsten Summe
(`test_rate_null_ist_die_undiskontierte_reihe`).

| Nr | Anforderung (Wortlaut oder enge Wiedergabe) | Seite | tragender Beleg (Datei, Funktion oder Abschnitt) | Urteil |
|---|---|---|---|---|
| A1 | „Um gegenwärtige und zukünftige Kosten und Nutzen zu vergleichen, werden zukünftige Kosten und Nutzen unter Verwendung einer Diskontrate auf den heutigen Tag abgezinst.“ | 14 | `cost_projection_service.py`, `project_costs()` → `_discounted()`: kumulierte Kosten je Pfad und Szenario als Barwert, abgezinst auf das Basisjahr `years[0]` = 2025; Feld `discounted` und Eintrag in `assumptions` | trägt |
| A2 | „Diese Diskontrate soll zwei Aspekte abbilden: (1) die individuelle oder gesellschaftliche Zeitpräferenz und (2) die relative Veränderung zwischen heutigen und künftigen Preisen verschiedener Güter und Dienstleistungen.“ | 14 | `cost_projection_service.py`, `PURE_TIME_PREFERENCE_RATES` (nur Aspekt 1) | trägt teilweise |
| A3 | Bedeutung der RZPR: 0 % gewichtet den Nutzen künftiger und heutiger Generationen gleich, eine RZPR > 0 gewichtet heutige höher (Fn. 13: eine RZPR < 0 ist nicht bekannt). „Numerisch bedeutet eine RZPR von 1%, dass … nur 74% des Nutzens (Wohlfahrt) der in 30 Jahren auftritt und nur 55% des Nutzens der in 60 Jahren auftritt, berücksichtigt werden.“ | 14 | `_discounted()`, Faktor 1/(1 + r)^t: bei 1 % nach 30 Jahren 0,742, nach 60 Jahren 0,550 (nachgerechnet); keine Rate unter 0 % | trägt |
| A4 | Die soziale Diskontrate nach Ramsey (1928) „kombiniert“ beide Elemente: „i) die Reine Zeitpräferenzrate (RZPR) und ii) das erwartete Konsumwachstum, gewichtet nach seinen Auswirkungen auf den Grenznutzen der Verbraucher“. Schon S. 10 hält fest, „dass sich die RZPR von der Diskontrate unterscheidet“. | 14, 15 | keiner. `_discounted()` setzt die Diskontrate gleich der RZPR; eine Wachstumskomponente fehlt, ohne Begründung. | trägt nicht |
| A5 | „Die reine Zeitpräferenzrate wird jedoch über die Monte Carlo-Läufe hinweg konstant gehalten, und die Ergebnisse werden für eine RZPR von 0 % und 1 % dargestellt.“ (S. 10 dazu: Kostensatz mit einer der beiden Raten und „eine Sensitivitätsanalyse mit dem jeweils anderen Wert“.) | 15 | `PURE_TIME_PREFERENCE_RATES = (0.0, 0.01)`, über den ganzen Horizont konstant; `test_rate_null_ist_die_undiskontierte_reihe` (beide Schlüssel `0.0` und `0.01` je Pfad und Szenario), `test_rate_ein_prozent_senkt_den_endwert` | trägt |
| A6 | Für die ökonomische Bewertung der meisten Umweltauswirkungen besteht Konsens, „dass die relative Verknappung von Ökosystemleistungen zu relativen Preissteigerungen führt und darum eine niedrigere Diskontrate anzuwenden ist“; bei weiterem Rückgang „eine noch niedrigere Diskontrate“. Dagegen erhöhen sinkende relative Preise von Konsumgütern die Diskontrate für diese Güter. | 15 | keiner. Das Produkt unterscheidet die Diskontrate nicht nach Gütern und begründet nicht, welche Richtung für die bewerteten Gesundheitsschäden gilt. | trägt nicht |
| A7 | „Für politische Entscheidungen ist der Marktzinssatz jedoch kein geeignetes Konzept.“ | 15 | `PURE_TIME_PREFERENCE_RATES`: nur 0 % und 1 %, kein Marktzinssatz | trägt |
| A8 | Die bei politischen Entscheidungen anzuwendende Diskontrate muss „auch die höhere gesellschaftliche Risikoaversion sowie langfristige staatliche Ziele wie Generationengerechtigkeit und langfristige gesellschaftliche Wohlfahrt berücksichtigen“. | 15 | `PURE_TIME_PREFERENCE_RATES`, Wert 0 % (gleiche Gewichtung der Generationen) | trägt teilweise |

**Begründung je Urteil:**

- A1: Abgezinst wird auf 2025, das erste Jahr der DWD-Projektion und das Basisjahr der Schadenskosten. Das ist der
  „heutige Tag“ der Rechnung; der Ausweis nennt das Basisjahr ausdrücklich.
- A2: Das ist der Kern der Frage. Die Konvention verlangt eine Diskontrate aus zwei Teilen. Das Produkt bildet nur die
  Zeitpräferenz ab, die Veränderung der relativen Preise fehlt.
- A3: Die Rechnung des Produkts gibt die Zahlen der Konvention genau wieder. Die Rate 3 %, die der Text zum Vergleich
  nennt (41 % und 17 %), ist keine Empfehlung und wird nicht verlangt.
- A4: Die Konvention nennt die RZPR einen Bestandteil der Diskontrate, nicht die Diskontrate selbst. Das Produkt
  zinst aber mit der RZPR allein ab. Seine Werte sind daher Barwerte zu einer Diskontrate von 0 % und 1 %, nicht zu einer
  RZPR von 0 % und 1 %, wie der Ausweis sagt. Nach Ramsey kommt zur RZPR das Konsumwachstum hinzu, gewichtet mit der
  Elastizität des Grenznutzens. Bei wachsendem Konsum wäre die Diskontrate auch bei 0 % RZPR größer als null. Der
  Barwert „0 % RZPR“ des Produkts ist dagegen die unabgezinste Summe. Eine Zahl für die Diskontrate gibt die Konvention
  nicht vor: Im GIVE-Modell ist das Konsumwachstum eine abhängige Größe, deshalb ist es „nicht möglich, die genaue
  Diskontrate anzugeben“ (S. 15). Das Produkt müsste also selbst entscheiden und begründen, wie es die zweite Komponente
  ansetzt. Heute steht dazu nichts im Code und nichts in den Annahmen.
- A5: Zwei Werte, 0 % und 1 %, konstant über den Horizont, beide ausgewiesen und im Test abgesichert. Die Werte
  stimmen mit der Konvention überein. Was mit ihnen abgezinst wird, ist aber wegen A4 nicht die Diskontrate der Konvention.
- A6: Die Richtung der zweiten Komponente hängt vom Gut ab. Konsumgüter werden relativ billiger, das hebt die
  Diskontrate. Knapper werdende Umweltgüter werden relativ teurer, das senkt sie. Welche Richtung für die bewerteten
  Gesundheitsschäden gilt, ist im Produkt nicht gesagt. Die Wahl „Diskontrate gleich RZPR“ wäre vertretbar, wenn beide
  Effekte sich aufheben. Diese Annahme müsste dann als Abschätzung von KAP3 ausgewiesen und begründet sein (Vorgabe P1);
  das fehlt.
- A7: Das Produkt nutzt keinen Marktzinssatz; beide Raten liegen weit unter einem Kapitalmarktzins.
- A8: Die Rate 0 % bildet Generationengerechtigkeit ab. Risikoaversion geht nirgends ein.

Nicht als eigene Anforderung gewertet: die Begründung, warum private Zeitpräferenz bei öffentlichen Gütern Fragen
aufwirft (S. 14), die Erklärung des Marktzinssatzes für private Entscheidungen und seine Annahmen i) und ii) (S. 15)
sowie der Einkommens- und der Knappheitseffekt als Begründung (S. 15). Sie begründen A3, A6 und A7, stellen aber keine
eigene Anforderung. Die Kostensätze 990 € und 345 € je t CO₂-Äq. (S. 10) betreffen Treibhausgase und sind nicht
Gegenstand der Zeile 22.

**Gelesene Seiten und Abschnitte:** Inventar mit `python3 /opt/overlord/overlord/skripte/dokumente.py inventar`
(82 Seiten). Inhaltsverzeichnis S. 4–5 ganz. Kap. 1 „Einleitung“ S. 8–9 ganz. Kap. 2.1 S. 10–12 ganz, einschließlich
Fußnote 2 (S. 10, Verweis auf Abschnitt 2.2) und Tabelle 1 (S. 11) im Text. Kap. 2.2.1 und 2.2.2 S. 12–14 ganz
(S. 13: Diskontierung im GIVE-Modell). Kap. 2.2.3 S. 14–15 vollständig im Text gelesen, einschließlich Fußnote 13
(S. 14). S. 16 mit Kap. 2.2.4 „Equity Weighting“ samt Kasten (Kapitelgrenze geprüft) und S. 17 mit dem Anfang von
Kap. 3.1. Als Bild angesehen: keine Seite. Kap. 2.2.3 enthält keine Tabelle, keinen Kasten und keine Abbildung: Das
Inventar führt dort keine Tabelle, eingebettete Bilder gibt es nur auf S. 1, und der Text der S. 14–15 ist durchgehend
Fließtext mit Aufzählungen. Tabelle 1 (S. 11) liegt außerhalb von Kap. 2.2.3, enthält keine Anforderungen an die
Diskontierung und wurde nicht als Bild angesehen. Nicht gelesen: der Rest des Handbuchs ab Kap. 3, der Anhang
(S. 68–76) und das Literaturverzeichnis (ab S. 77). Ebenfalls nicht gelesen wurden die zitierten Quellen Ramsey (1928),
Drupp et al. (2024) und Baumgärtner et al. (2015) sowie die Forschungsberichte zur Methodenkonvention (Osterwald et al.
2024, Walther et al. 2024a, Anthoff 2025).

**Schluss:** Zeile 22 bleibt nicht `erfüllt`. Von 8 Anforderungen trägt der Bestand vier voll (A1, A3, A5, A7), zwei
teilweise (A2, A8) und zwei nicht (A4, A6). Zur Frage nach weiteren Bestandteilen: Ja, die Konvention verlangt eine
Diskontrate aus RZPR und einer Komponente für die Veränderung der relativen Preise (Ramsey: Konsumwachstum, gewichtet
mit dem Grenznutzen). Sie trennt RZPR und Diskontrate ausdrücklich. Das Produkt zinst mit der RZPR allein ab. Die Werte
0 % und 1 % entsprechen der Konvention, der als „Barwert mit 1 % RZPR“ ausgewiesene Betrag aber nicht: Er ist ein
Barwert zu 1 % Diskontrate. Der Status der Zeile 22 ist in derselben Änderung auf `teilweise` gesetzt; die Spalte
„Lücke“ nennt, was fehlt. Die Zählungen in den Abschnitten „Nachtrag: Zeilen 21–25“, „Nachtrag: Abschlusszählung“ und
„Zusammenfassung“ sind damit weiter überholt. Sie nachzuziehen ist Sache der Gesamtzählung (T-0821-ceo, T-0487),
nicht dieser Gegenprobe.

### Gegenprobe Zeile 20 gegen UBA-Handlungsempfehlungen zur ISO 14091, Abschnitt 2.3.2

Frage: Tragen die Belege der Zeile 20 das, was Abschnitt 2.3.2 „Ergebnisse zielgruppenspezifisch kommunizieren“
verlangt — und sind Karten und Kommunikationsprodukte für die breite Öffentlichkeit dort verlangt oder nur als Beispiel
genannt? Gelesen wurde gegen die Sekundärquelle Umweltbundesamt (Porst, Voß, Kahlenborn, Schauser),
„Klimarisikoanalysen auf kommunaler Ebene – Handlungsempfehlungen zur Umsetzung der ISO 14091“, Juni 2022, 40 Seiten,
abgerufen am 25.09.2026 von
https://www.umweltbundesamt.de/system/files/medien/479/publikationen/2022_uba-fachbroschuere_kra_auf_kommunaler_ebene.pdf
(Verweis von der Publikationsseite in der Spalte „Quelle“; HTTP 200). Die Datei liegt nicht im Repo. PDF-Seitenzahl und
gedruckte Seitenzahl stimmen überein (S. 31 trägt die gedruckte Zahl 31). Abschnitt 2.3.2 füllt S. 31 in beiden
Spalten; davor endet auf S. 30 Abschnitt 2.3.1, danach beginnt auf S. 32 Kapitel 3 „Praxisbeispiele und Arbeitshilfen“.
Die Fundstelle „S. 31“ stimmt. Fußnote 35 (S. 30) ordnet Abschnitt 2.3 dem Kapitel 7 der ISO 14091 zu; auch die Angabe
„Kap. 7“ stimmt.

**Befund Primärquelle:** Der Normtext ISO 14091:2021 wurde nicht gelesen. Er wird nicht gekauft; das Menschenticket
T-0531-ceo ist offen. Die Tabelle stützt sich allein auf die Wiedergabe durch das UBA. Abschnitt 2.3.2 spricht
durchgehend in „empfiehlt sich“, „bietet sich an“, „kann sinnvoll sein“, „können hilfreiche Medien darstellen“ und
„sollten“; die Zeile 20 verschärft das zu „sind … zu kommunizieren“.

Im Produkt wurden `backend/app/services/kurzfassung_markdown.py` und `backend/tests/test_kurzfassung_export.py`
vollständig gelesen, die Route `GET /api/kommune/{kommune_id}/kurzfassung` in `backend/app/api/routes/kommune.py`
ganz. Dazu, um die Karten und Geodaten zu beurteilen: `frontend/src/App.tsx` (Routen), `frontend/src/config/features.ts`
(Schalter), der Kopf von `frontend/src/pages/lite/LiteMapPage.tsx` und `frontend/src/components/MapView.tsx`,
`backend/app/services/geodata_export_service.py` (Kopf und Aufbau der Layer) und die Routen in
`backend/app/api/routes/export.py`. Im Frontend ruft nichts den Endpunkt `/kurzfassung` auf; ob die Kurzfassung sichtbar
ist, ist nicht Gegenstand dieser Gegenprobe (Sichtbarkeit, T-0483). Ausgeführt wurde nichts.

| Nr | Anforderung (Wortlaut oder enge Wiedergabe) | Seite | tragender Beleg (Datei, Funktion oder Abschnitt) | Urteil |
|---|---|---|---|---|
| A1 | „Für die Kommunikation der Ergebnisse empfiehlt sich die Erarbeitung verschiedener Produkte, die jeweils zielgruppenspezifisch aufbereitet sind (etwa hinsichtlich Tonalität/Sprachstil, Kommunikationsmedium).“ | 31 | `kurzfassung_markdown.py`, `kurzfassung_markdown()` (Kurzfassung für politische Entscheidungsträger); `docs/methodik/95_hitzebelastung.md` mit PDF (Methodik-Bericht für Fachleute) | trägt teilweise |
| A2 | „Aufbauend auf den Vorarbeiten (Kapitel 2.1) sollten die spezifischen Ziele der Ergebniskommunikation gegenüber der jeweiligen Akteursgruppe geklärt werden.“ | 31 | keiner. Das Produkt kennt weder Leitfragen und Ziele der Kommune (Abschnitt 2.1.1) noch Ziele der Kommunikation je Akteursgruppe. | trägt nicht |
| A3 | „Für die Fachöffentlichkeit bietet sich die Veröffentlichung eines Abschlussberichts mit genauer Darstellung der Datengrundlagen, Methodik, Vorgehensweise und Detailergebnissen an.“ | 31 | `docs/methodik/95_hitzebelastung.md` (Kap. 2 Evidenz-Register, Kap. 3 Modell, Kap. 8 Quellen), ebenso #96 und #98; `bestandsaufnahme_markdown.py`; GeoPackage-Export `geodata_export_service.py` (Layer `bewertung_100m`) | trägt teilweise |
| A4 | „Zusätzlich kann eine Zusammenfassung der wesentlichen Ergebnisse, die deutlich und nachvollziehbar auf die Handlungserfordernisse (und -möglichkeiten) für die konkrete praktische Umsetzung von Klimaanpassung hinweist, für politische Entscheidungsträger*innen sinnvoll sein.“ | 31 | `kurzfassung_markdown.py`, `kurzfassung_markdown()` mit den fünf Abschnitten „Gesamtrisiko“, „Die fünf teuersten Klimawirkungen“, „Erwartete Schadenssumme“, „Die fünf wirksamsten Maßnahmen“, „Methode und Grenzen“; `test_kurzfassung_export.py` | trägt teilweise |
| A5 | „Auch Kommunikationsprodukte wie Karten oder Broschüren für die breite Öffentlichkeit können hilfreiche Medien zur Vermittlung der Ergebnisse darstellen.“ | 31 | keiner. Die öffentliche Deutschland-Karte (`LiteMapPage.tsx`, Route `/deutschland`) ist mit `FEATURES.deutschlandKarte: false` abgeschaltet; die Karte in `MapView.tsx` liegt im angemeldeten Bereich `/app/*`; der Kopf von `kurzfassung_markdown.py` schließt Karten aus. | trägt nicht |
| A6 | „Um die Ergebnisse der KRA effektiv gegenüber politischen Mandatsträger*innen zu kommunizieren, kann es sinnvoll sein, diese mitsamt des darauf basierenden kommunalen Anpassungskonzepts (standardmäßig) in Beschlussvorlagen zu integrieren.“ (Fn. 36: Handreichung MONARES) | 31 | keiner. Es gibt keinen Baustein für eine Beschlussvorlage und kein Anpassungskonzept, dem die Kurzfassung beigegeben würde. | trägt nicht |
| A7 | „Bei der Ergebnisdarstellung sind die leichte Erfassbarkeit der Ergebnisse, eine ansprechende Gestaltung der Materialien und eine prägnante Wiedergabe der wichtigen Kernbotschaften der KRA wichtig.“ | 31 | `kurzfassung_markdown.py` (`MAX_ZEILEN = 5`, Gesamtrisiko in einem Satz, „Methode und Grenzen“ in höchstens fünf Sätzen); `test_kurzfassung_export.py`, Tests (a)–(c) | trägt teilweise |
| A8 | „Bei der Kommunikation an Fachfremde sind eindeutige, leicht verständliche Begriffsdefinitionen sowie Erläuterungen von Abbildungen und Karten hilfreich.“ | 31 | keiner. Die Kurzfassung verwendet „Klimawirkung“, „Risikoklasse“ und „nicht abgezinst“ ohne Erklärung; nur das Szenario trägt einen Kurzvermerk („RCP 8.5 (weiter wie bisher)“). | trägt nicht |
| A9 | „Kartendarstellungen können dabei unterstützen, räumlich differenzierte Anpassungsmaßnahmen zu entwickeln und zu planen. Gleichzeitig ermöglichen Kartendarstellungen, Ergebnisse wirksam zu kommunizieren. Dazu ist eventuell auch eine vereinfachte Darstellungsform nützlich.“ | 31 | `frontend/src/components/MapView.tsx` (MapLibre-Karte mit Choroplethen je Zelle und Beschriftung der Maßnahmen, `measureMapLabel()`) | trägt teilweise |
| A10 | „Für die Ergebnispräsentation für lokale oder regionale Akteur*innen und interessierte Bürger*innen empfiehlt sich die Ausrichtung öffentlicher Informationsveranstaltungen wie etwa Bürgerforen oder dialogischer Kommunikationsformate.“ | 31 | keiner (Verfahrensschritt, vgl. Zeile 17, `offen`) | trägt nicht |
| A11 | „Dabei können Risikokarten (z. B. zu Hitze, Hochwasser oder Starkregen), auch als (Web-)GIS-Anwendungen und/oder interaktive Karten, sowie Diagramme und Tabellen genutzt werden oder das Aufzeigen von Beispielen aus der eigenen (oder anderen) Kommune(n).“ | 31 | `MapView.tsx` (interaktive Karte, nur nach Anmeldung); Tabellen der Kurzfassung; `export.py`, `export_measures()` (Maßnahmen als Excel-Datei) | trägt teilweise |
| A12 | „Soweit möglich, sollten Ergebnisse in bestehende teil-/öffentliche GIS-Systeme eingepflegt werden.“ | 31 | `geodata_export_service.py` (GeoPackage mit Grenze, Layer `bewertung_100m` mit Index, Ausprägung und Betrag in € je Klimawirkung und Zelle); `export.py`, `POST /kommune/{kommune_id}/exports/geodaten` und Download | trägt |
| A13 | „Ein zielgruppenspezifischer/-differenzierender Online-Auftritt kann die Ergebniskommunikation flankieren. Darüber können die wesentlichen Inhalte und Ergebnisse der KRA leicht zugänglich und verständlich in komprimierter Form dargestellt werden.“ | 31 | keiner. Der öffentliche Teil (`App.tsx`: Startseite, Anmeldung, Kontakt, Roadmap) zeigt keine Ergebnisse einer Kommune; die Deutschland-Karte ist abgeschaltet (A5). | trägt nicht |
| A14 | „Die Ergebnisse der KRA können ferner über gezielte Informationskampagnen oder Social-Media-Meldungen (kontinuierlich oder anlassbezogen) oder in Form von Themenreihen oder thematischen Spaziergängen zielgruppengerecht kommuniziert werden.“ | 31 | keiner (Verfahrensschritt der Kommune) | trägt nicht |
| A15 | „Speziell in die Kommunikation gegenüber Bürger*innen können auch Hinweise auf die Möglichkeiten der Eigenvorsorge einfließen, um das Anerkennen der gemeinsamen Verantwortung zu stärken.“ | 31 | keiner. „Eigenvorsorge“ steht nur in `backend/app/data/catalog.py` als Wirkmechanismus einer Maßnahme (Förder- und Prämienanreize), nicht als Hinweis an Bürger. | trägt nicht |

**Begründung je Urteil:**

- A1: Es gibt zwei Produkte für zwei Zielgruppen: den Methodik-Bericht für Fachleute und die Kurzfassung für politische
  Entscheidungsträger. Beide sind Text in Markdown (der Bericht zusätzlich als PDF); das Medium unterscheidet sich nicht.
  Für die breite Öffentlichkeit gibt es kein Produkt (A5, A13).
- A2: Ziele der Kommunikation je Akteursgruppe legt die Kommune fest. Das Produkt fragt sie nicht ab, und die Kurzfassung
  ist für alle Kommunen gleich gebaut.
- A3: Datengrundlagen und Methodik trägt der Methodik-Bericht je Klimawirkung, genau und mit Quellen. Er ist aber
  bundesweit gleich und zeigt Ergebnisse nur für eine Beispielzelle, keine Detailergebnisse der Kommune. Einen
  Abschlussbericht der Klimarisikoanalyse einer Kommune, der Datengrundlagen, Vorgehen und Ergebnisse zusammenführt,
  erzeugt das Produkt nicht; die Detailergebnisse liegen nur im GeoPackage und in der Anwendung. Die Methodik-Berichte
  liefert das Produkt selbst nicht aus, sie liegen unter `docs/methodik/`.
- A4: Die Zusammenfassung für politische Entscheidungsträger besteht und nennt Gesamtrisiko, teuerste Klimawirkungen,
  Schadenssumme und Grenzen. Auf Handlungserfordernisse weist sie nicht deutlich hin: Eine Dringlichkeit oder einen
  priorisierten Handlungsbedarf weist sie nicht aus (vgl. Zeile 6). Handlungsmöglichkeiten nennt sie nur als Maßnahmen,
  die die Kommune schon geplant hat; ohne Planung steht dort „Für diese Kommune ist noch keine Maßnahme mit bezifferter
  Wirkung geplant.“
- A5: Zur Frage der Gegenprobe: Karten und Broschüren für die breite Öffentlichkeit nennt der Text nur als Beispiel
  („Auch Kommunikationsprodukte wie Karten oder Broschüren … können hilfreiche Medien … darstellen“), nicht als
  Anforderung. Zeile 20 übernimmt sie als Teil der Anforderung. Gemessen an der Zeile fehlen sie: Die einzige öffentliche
  Karte ist abgeschaltet, eine Broschüre gibt es nicht.
- A6: Eine Kann-Empfehlung an die Kommune. Die Kurzfassung ließe sich einer Vorlage beifügen, sie ist aber nicht dafür
  gebaut, und ein Anpassungskonzept erzeugt das Produkt nicht.
- A7: Prägnanz trägt die Kurzfassung durch feste Grenzen, die die Tests prüfen. Gestaltet ist sie nicht: Sie ist
  unformatiertes Markdown ohne Abbildung, Karte oder Diagramm.
- A8: Die Kurzfassung richtet sich an Fachfremde, erklärt aber ihre Begriffe nicht, und sie enthält keine Abbildungen,
  die zu erläutern wären. Die Zeichentabelle des Methodik-Berichts (Kap. 3.6) richtet sich an Fachleute.
- A9: Die Karte der Anwendung zeigt Ergebnisse je Zelle und die Maßnahmen und unterstützt so die räumliche Planung. Eine
  Karte als Kommunikationsprodukt, etwa vereinfacht oder in einem Export zum Weitergeben, gibt es nicht.
- A10: Veranstaltungen richtet die Kommune aus; das Produkt bietet dafür nichts, wie schon bei Zeile 17.
- A11: Eine interaktive Karte und Tabellen gibt es, aber nur für angemeldete Nutzer der Kommune; für eine öffentliche
  Präsentation fehlt eine freigegebene Karte. Beispiele aus anderen Kommunen zeigt das Produkt nicht.
- A12: Der GeoPackage-Export enthält die Ergebnisse je Zelle in einem Format, das GIS-Systeme der Kommune einlesen
  können. Einpflegen muss die Kommune selbst; „soweit möglich“ ist damit erfüllt.
- A13: Einen Online-Auftritt mit den Ergebnissen einer Kommune gibt es nicht; das Produkt ist im Kern ein angemeldeter
  Arbeitsbereich.
- A14: Kampagnen, Social Media und Spaziergänge sind Aufgaben der Kommune; das Produkt liefert dafür kein Material.
- A15: Hinweise auf Eigenvorsorge für Bürger fehlen in allen Ausgaben.

Nicht als eigene Anforderung gewertet: Abschnitt 2.3.1 „Zentrale Ergebnisse und wichtige Botschaften zusammenstellen“
(S. 30), der den abschließenden Bericht, die Einbettung ins Klimaanpassungskonzept und das Benennen von Schwierigkeiten
behandelt; er gehört nicht zu Zeile 20. Die Begründungssätze in A7 und A15 („um das Anerkennen der gemeinsamen
Verantwortung zu stärken“) sind Zweckangaben, keine eigenen Anforderungen.

**Gelesene Seiten und Abschnitte:** Inventar mit `python3 /opt/overlord/overlord/skripte/dokumente.py inventar`
(40 Seiten). Inhaltsverzeichnis S. 5 ganz. Einführung S. 7–9 ganz, einschließlich des Hinweises auf S. 8, dass jedem
Teilkapitel eine Kurzfassung des ISO-Abschnitts vorangestellt ist, und der Infobox „Klimarisikoanalysen (KRA)“ auf S. 9
mit der Zielgruppe der Empfehlungen (S. 7). S. 30 ganz: Ende von 2.2.6, Hinweisbox für kleine Kommunen, Beginn von 2.3
mit Fußnote 35 und Abschnitt 2.3.1 (Kapitelgrenze geprüft). Abschnitt 2.3.2 auf S. 31 vollständig im Text gelesen,
samt Fußnote 36; S. 31 zusätzlich als Bild angesehen, um die Reihenfolge der Punkte in den beiden Spalten und das Fehlen
eines kursiven ISO-Vorspanns zu prüfen. S. 32–33 mit dem Beginn von Kapitel 3 (Kapitelgrenze geprüft). Abschnitt 2.3.2
enthält keine Tabelle und keine Abbildung. **Nicht gelesen:** die in Fußnote 36 verlinkte Handreichung von MONARES,
Abschnitt 2.1 (Vorarbeiten, auf die A2 verweist), 2.2.1–2.2.5, Kapitel 3 ab S. 34 und Kapitel 4 der Broschüre; der
Primärtext der ISO 14091.

**Schluss:** Zeile 20 bleibt nicht `erfüllt`. Von 15 Anforderungen trägt der Bestand eine voll (A12), sechs teilweise
(A1, A3, A4, A7, A9, A11) und acht nicht (A2, A5, A6, A8, A10, A13, A14, A15). Zur Frage der Gegenprobe: Karten und
Broschüren für die breite Öffentlichkeit sind im Text nur als Beispiel genannt, nicht verlangt; überhaupt ist jeder Punkt
von 2.3.2 eine Empfehlung. Zeile 20 aber fasst die Empfehlung als Pflicht und nennt die breite Öffentlichkeit als
Zielgruppe; an ihr gemessen fehlt ein Produkt für diese Zielgruppe ganz, und die Kurzfassung weist nicht auf
Handlungserfordernisse hin. Der Status der Zeile 20 ist in derselben Änderung auf `teilweise` gesetzt; die Spalte
„Lücke“ nennt, was fehlt. Die Zählungen in den Abschnitten „Nachtrag: Abschlusszählung“ und „Zusammenfassung“ sind damit
weiter überholt. Sie nachzuziehen ist Sache der Gesamtzählung (T-0821-ceo, T-0487), nicht dieser Gegenprobe.

### Gegenprobe Zeile 13 gegen KAnG, § 8 Abs. 1

Frage: Kann ein Werkzeug für Kommunen und Berater die Pflicht „Die Träger öffentlicher Aufgaben haben … fachübergreifend
und integriert zu berücksichtigen“ tragen, und was leistet der Nachweis unter `docs/NACHWEIS_FACHUEBERGREIFEND_KANG.md`
wirklich? Gelesen wurde der Gesetzestext des Bundes-Klimaanpassungsgesetzes (KAnG) in der nichtamtlichen Fassung von
gesetze-im-internet.de, abgerufen am 25.09.2026 (Adressen und Zeitpunkte unten). Der Text liegt nicht im Repo. Die
Webseite hat keine Seitenzahlen; die Spalte „Seite“ nennt Paragraf, Absatz, Satz und Nummer.

Wortlaut von § 8 Abs. 1: „Die Träger öffentlicher Aufgaben haben bei ihren Planungen und Entscheidungen das Ziel der
Klimaanpassung nach § 1 fachübergreifend und integriert zu berücksichtigen. Dabei sind sowohl die bereits eingetretenen
als auch die zukünftig zu erwartenden Auswirkungen des Klimawandels zu berücksichtigen, insbesondere 1. Überflutung oder
Überschwemmung bei Starkregen, Sturzfluten oder Hochwasser, 2. Absinken des Grundwasserspiegels oder Verstärkung von
Trockenheit oder Niedrigwasser, 3. Bodenerosion oder 4. Erzeugung oder Verstärkung eines lokalen Wärmeinsel-Effekts.
Dabei ist zu berücksichtigen, dass Versickerungs-, Speicher- und Verdunstungsflächen im Rahmen einer wassersensiblen
Entwicklung so weit wie möglich erhalten werden.“ § 2 Nr. 3 bestimmt „Träger öffentlicher Aufgaben: alle Stellen, die
öffentliche Aufgaben wahrnehmen, unabhängig davon, ob sie öffentlich-rechtlich oder privatrechtlich organisiert sind.“

Im Produkt wurden `backend/app/data/kang_handlungsfelder.py`, `backend/app/services/kang_beruecksichtigung.py`,
`backend/app/services/kang_nachweis_markdown.py` und `docs/NACHWEIS_FACHUEBERGREIFEND_KANG.md` vollständig gelesen.
Dazu, um die Eingänge des Nachweises zu beurteilen: in `backend/app/data/catalog.py` die Listen `RISKS`,
`PLANNED_RISKS`, `MEASURES` und `KANG_CLUSTERS` (ausgewertet über den Import des Moduls, ohne Schreibzugriff), die
Liste `_PARKED_MEASURES` in `backend/app/data/catalog_parked.py` (Einträge `SPONGE_CITY` und `INFILTRATION_AREAS`) und in
`backend/app/services/engine/inputs.py` die Wärmeinsel-Rechnung (`compute_uhi_delta`, `compute_uhi_components`,
Zellentemperatur `summer_temp_cell`). Der Stand beim Lesen: 4 aktive Klimawirkungen, alle im KWRA-Handlungsfeld
„Menschliche Gesundheit“ (Mortalität und Erkrankungen durch Hitze, Aeroallergene, UV); 49 geplante Klimawirkungen ohne
Rechnung; 3 aktive Maßnahmen, zwei im KAnG-Feld „Gesundheit und Pflege“, eine im Querschnittsfeld; 7 Cluster mit
17 Handlungsfeldern. Außerhalb der vier Belegdateien ruft nichts `nachweis_fachuebergreifend` oder `nachweis_markdown`
auf (Grep über `backend/app` und `frontend/src`); ob der Nachweis im Produkt sichtbar ist, ist nicht Gegenstand dieser
Gegenprobe (Sichtbarkeit, T-0483).

| Nr | Anforderung (Wortlaut oder enge Wiedergabe) | Seite | tragender Beleg (Datei, Funktion oder Abschnitt) | Urteil |
|---|---|---|---|---|
| A1 | „Die Träger öffentlicher Aufgaben haben bei ihren Planungen und Entscheidungen das Ziel der Klimaanpassung nach § 1 fachübergreifend … zu berücksichtigen.“ | § 8 Abs. 1 Satz 1 | `kang_beruecksichtigung.py`, `nachweis_fachuebergreifend()` (Gegenüberstellung je KAnG-Handlungsfeld, 17 Felder); `kang_handlungsfelder.py`, `KWRA_FELD_ZU_KANG` und `handlungsfeld_fuer_risiko()`; `NACHWEIS_FACHUEBERGREIFEND_KANG.md`, Abschnitte „Rechtsgrundlage und Adressat“ und „Was das Produkt prüft“ | trägt teilweise |
| A2 | „… und integriert zu berücksichtigen.“ | § 8 Abs. 1 Satz 1 | keiner, der mit dem Katalog ein Ergebnis liefert. `nachweis_fachuebergreifend()`, Liste `integrierende_massnahmen` (Maßnahmen, deren `linked_risk_codes` auf mehr als ein Handlungsfeld führen); mit dem Katalog ist sie immer leer. | trägt nicht |
| A3 | „Dabei sind sowohl die bereits eingetretenen als auch die zukünftig zu erwartenden Auswirkungen des Klimawandels zu berücksichtigen …“ | § 8 Abs. 1 Satz 2 | `nachweis_fachuebergreifend()`, Eingang `schaeden` (eine jährliche Schadenssumme je Klimawirkung, ohne Zeitbezug) | trägt teilweise |
| A4 | „insbesondere 1. Überflutung oder Überschwemmung bei Starkregen, Sturzfluten oder Hochwasser“ | § 8 Abs. 1 Satz 2 Nr. 1 | keiner. Die zugehörigen Klimawirkungen (#50, #51, #59, #60, #74) stehen nur in `catalog.PLANNED_RISKS`, ohne Rechnung. | trägt nicht |
| A5 | „2. Absinken des Grundwasserspiegels oder Verstärkung von Trockenheit oder Niedrigwasser“ | § 8 Abs. 1 Satz 2 Nr. 2 | keiner. Die zugehörigen Klimawirkungen (#13, #55, #56, #71) stehen nur in `catalog.PLANNED_RISKS`, ohne Rechnung. | trägt nicht |
| A6 | „3. Bodenerosion“ | § 8 Abs. 1 Satz 2 Nr. 3 | keiner. Bodenerosion durch Wasser (#10) und durch Wind (#11) stehen nur in `catalog.PLANNED_RISKS`, ohne Rechnung. | trägt nicht |
| A7 | „4. Erzeugung oder Verstärkung eines lokalen Wärmeinsel-Effekts“ | § 8 Abs. 1 Satz 2 Nr. 4 | `engine/inputs.py`, `compute_uhi_delta()` und `compute_uhi_components()` (Wärmeinsel-ΔT je Zelle aus OSM-Landnutzung), eingerechnet in die Zellentemperatur `summer_temp_cell` und damit in Hitzebelastung (#95) | trägt teilweise |
| A8 | „Dabei ist zu berücksichtigen, dass Versickerungs-, Speicher- und Verdunstungsflächen im Rahmen einer wassersensiblen Entwicklung so weit wie möglich erhalten werden.“ | § 8 Abs. 1 Satz 3 | keiner. Die Maßnahmen „Entsiegelung / Schwammstadt“ (`SPONGE_CITY`) und „Versickerungsflächen“ (`INFILTRATION_AREAS`) sind in `catalog_parked.py` geparkt; kein Nachweisfeld fragt nach dem Erhalt solcher Flächen. | trägt nicht |
| A9 | „Träger öffentlicher Aufgaben sollen darauf hinwirken, dass bereits versiegelte Böden, deren Versiegelung dauerhaft nicht mehr für die Nutzung der Böden notwendig ist, … soweit dies erforderlich und zumutbar ist, wiederhergestellt und entsiegelt werden.“ | § 8 Abs. 3 Satz 1 | keiner. `SPONGE_CITY` ist geparkt (A8). | trägt nicht |

**Begründung je Urteil:**

- A1: Adressat der Pflicht ist nach § 2 Nr. 3 der Träger öffentlicher Aufgaben, nicht das Werkzeug. Ein Werkzeug kann die
  Berücksichtigung nicht leisten, es kann sie nur vorbereiten. Das sagt der Nachweis selbst richtig (`ABGRENZUNG`,
  Abschnitt „Was dem Träger öffentlicher Aufgaben überlassen bleibt“). Das Gerüst dafür ist da: Jede Klimawirkung wird
  einem der 17 KAnG-Handlungsfelder zugeordnet, jede Maßnahme ebenso, und je Feld steht „berücksichtigt“, „offen“ oder
  „nicht betroffen“. Fachübergreifend wird der Blick damit aber nicht: Alle 4 aktiven Klimawirkungen liegen im Feld
  „Gesundheit und Pflege“. Mit dem Katalog kann höchstens dieses eine Feld betroffen sein; die übrigen 16 stehen immer
  auf „nicht betroffen“, auch dort, wo die Kommune in der Sache betroffen ist. Vom Ziel nach § 1 (Schutz von Leben und
  Gesundheit, Gesellschaft, Wirtschaft, Infrastruktur, Natur und Ökosystemen) deckt die Rechnung nur Leben und
  Gesundheit ab.
- A2: Der Nachweis liest „integriert“ als Maßnahme, die über mehr als ein Handlungsfeld wirkt. Keine der 3 aktiven
  Maßnahmen tut das: Zwei verweisen nur auf Klimawirkungen im Feld Gesundheit, die dritte auf keine. Die Ausgabe lautet
  deshalb bei jeder Planung „Keine Maßnahme der Planung setzt an mehr als einem Handlungsfeld an.“ Ob die Lesart des
  Wortes „integriert“ trägt (Einbeziehung in die eigenen Planungs- und Entscheidungsverfahren), prüft der Nachweis nicht.
- A3: Der Nachweis nimmt je Klimawirkung eine Zahl entgegen und trennt nicht zwischen eingetretenen und zu erwartenden
  Auswirkungen. Welche Zahl eingeht (heutiges Klima oder ein Szenario), legt der Aufrufer fest; einen Aufrufer gibt es
  nicht. Der Nachweis kann also einen der beiden Blicke tragen, beide zusammen nicht.
- A4: Keine Rechnung zu Überflutung, Sturzflut oder Hochwasser; die geplanten Einträge lassen sich dem Nachweis zwar
  übergeben, aber ohne Betrag. Das Handlungsfeld Wasserhaushalt bleibt „nicht betroffen“.
- A5: Wie A4: Grundwasser, Trockenheit im Boden, Bewässerungswasser und Niedrigwasser sind geplant, nicht gerechnet.
- A6: Wie A4: Bodenerosion ist geplant, nicht gerechnet; das Feld „Boden“ bleibt „nicht betroffen“.
- A7: Die bestehende Wärmeinsel geht je Zelle in die Temperatur und damit in den Hitzeschaden ein. „Erzeugung oder
  Verstärkung“ durch eine Planung, also ein Vergleich vor und nach einer Bebauung oder Versiegelung, rechnet das Produkt
  nicht. Die eigene Klimawirkung „Stadtklima / Wärmeinseln“ (#62) ist nur geplant; im Nachweis erscheint Hitze allein im
  Feld Gesundheit, nicht im Feld „Gebäude“, dem `KWRA_FELD_ZU_KANG` das Stadtklima zuordnet.
- A8: Das Produkt erfasst weder Versickerungs-, Speicher- und Verdunstungsflächen noch ihren Verlust durch eine Planung.
  Die Maßnahmen, die solche Flächen schaffen, sind geparkt.
- A9: Liegt außerhalb der Fundstelle der Zeile 13 (§ 8 Abs. 1) und geht nicht in ihren Status ein. Auch hier gibt es
  keinen Beleg: Die Entsiegelung ist geparkt.

Nicht als eigene Anforderung gewertet: § 8 Abs. 2 (gilt als erfüllt, soweit nach Fachgesetzen oder anerkannten Regeln der
Technik geplant wird, die der Zielsetzung von Abs. 1 entsprechen; eine Rechtsfolge, keine Pflicht), § 8 Abs. 3 Satz 2
(andere Gesetze „bleiben unberührt“), § 8 Abs. 4 (Kompetenzen der Länder, Gemeinden und Kreise, die Regelungen
auszugestalten) und § 8 Abs. 5 (keine Anwendung auf Verfahren, die vor dem 01.01.2025 beantragt oder angezeigt wurden
oder mit deren Ausführung vorher begonnen wurde). Das Wort „insbesondere“ in Satz 2 macht die Liste Nr. 1–4 nicht
abschließend; die vier Punkte sind trotzdem je eine Anforderung, weil das Gesetz sie ausdrücklich nennt.

**Gelesene Stellen:** alle abgerufen am 25.09.2026 über `urllib` (HTTP 200), Zeitpunkt nach dem `Date`-Kopf des
Servers:

- https://www.gesetze-im-internet.de/kang/index.html (06:12:07 GMT): Inhaltsverzeichnis ganz (Abschnitte 1–5, §§ 1–14;
  § 8 bildet allein Abschnitt 3 „Berücksichtigungsgebot“, damit sind die Grenzen des Abschnitts geprüft).
- https://www.gesetze-im-internet.de/kang/__8.html (06:11:59 GMT): § 8 Abs. 1–5 ganz im Wortlaut.
- https://www.gesetze-im-internet.de/kang/__1.html (06:12:03 GMT): § 1 „Ziel des Gesetzes“ ganz (drei Sätze), auf den
  § 8 Abs. 1 Satz 1 verweist.
- https://www.gesetze-im-internet.de/kang/__2.html (06:12:03 GMT): § 2 „Begriffsbestimmungen“ ganz (Nr. 1–3).

Eine erste Abfrage von § 8 und § 1 über ein zusammenfassendes Abrufwerkzeug gab den Text nur umschrieben wieder; der
Wortlaut oben stammt allein aus dem direkten Abruf. **Nicht gelesen:** §§ 3–7 und 9–14 KAnG, die Gesetzesbegründung
(Bundestags-Drucksache), die amtliche Fassung im Bundesgesetzblatt und Kommentarliteratur zu „fachübergreifend und
integriert“.

**Schluss:** Zeile 13 bleibt nicht `erfüllt`. Von 9 Anforderungen trägt der Bestand keine voll, 3 teilweise (A1, A3, A7)
und 6 nicht (A2, A4, A5, A6, A8, A9); A9 liegt außerhalb der Fundstelle und zählt für den Status nicht. Zur Frage der
Gegenprobe: Ein Werkzeug kann die Pflicht nicht tragen, denn sie trifft den Träger öffentlicher Aufgaben; es kann ihm die
Berücksichtigung vorbereiten, und der Nachweis sagt das richtig. Was er heute leistet, ist ein Raster über 17
Handlungsfelder, in dem mit dem aktiven Katalog nur das Feld Gesundheit betroffen sein kann, keine Maßnahme als
integrierend erscheint und die in Satz 2 Nr. 1–3 und Satz 3 ausdrücklich genannten Auswirkungen fehlen. Der Status der
Zeile 13 ist in derselben Änderung auf `teilweise` gesetzt; die Spalte „Lücke“ nennt, was fehlt. Die Zählungen in den
Abschnitten „Nachtrag: Abschlusszählung“ und „Zusammenfassung“ sind damit weiter überholt. Sie nachzuziehen ist Sache der
Gesamtzählung (T-0821-ceo, T-0487), nicht dieser Gegenprobe.

## Ergebnis

Fünf Anforderungen (Zeilen 1–5) aus Kapitel 1 und 2 des Teilberichts 1 wurden erfasst: vier als
`erfüllt`, eine (Zeile 2, Trennung "Klimarisiko ohne/mit Anpassung") als `teilweise`, weil nur ein
vorliegender Methodik-Bericht diese KWRA-Unterscheidung ausdrücklich verwendet. Keine Lücke
wurde behoben, kein Produktcode wurde angefasst — das war nicht Aufgabe dieses Pakets.

Prüflauf der genannten Belegpfade (`ls -d` je Pfad):

```
$ ls -d docs/methodik/95_hitzebelastung.md
docs/methodik/95_hitzebelastung.md
$ ls -d docs/methodik/61_vegetation_in_siedlungen.md
docs/methodik/61_vegetation_in_siedlungen.md
$ ls -d docs/evidenz/register.md
docs/evidenz/register.md
$ ls -d docs/methodik/60_gebaeudeschaeden_flusshochwasser.md
docs/methodik/60_gebaeudeschaeden_flusshochwasser.md
```

Kein Pfad wurde als `No such file` gemeldet; alle vier zitierten Belegpfade existieren im
Produkt-Repo.

Für das Inhaltsverzeichnis wurden die Seiten 1–10 des PDFs gelesen, für die Kapitelinhalte die
Seiten 33–48 (Kapitel 1 und 2.1). Insgesamt 26 PDF-Seiten, innerhalb des Rahmens von höchstens
40 Seiten.

### Nachtrag: Zeilen 6–10 (Teilpaket 2, Teilbericht 6 — Integrierte Auswertung)

Fünf weitere Anforderungen (Zeilen 6–10) aus Kapitel 3 (Handlungsfeldübergreifende Auswertung),
Kapitel 6 (Identifizierung von Handlungserfordernissen) und Kapitel 7 (Querbetrachtung der
Systembereiche) des Teilberichts 6 wurden erfasst: keine als `erfüllt`, drei (Zeilen 6, 8, 9) als
`teilweise` und zwei (Zeilen 7, 10) als `offen`. Grund ist durchgängig derselbe: Das Produkt
übernimmt einzelne KWRA-Begriffe und -Strukturen punktuell (die Priorisierungskategorie "sehr
dringend" in der Roadmap, Verbundrisiken im Katalog, Sensitivitätsbänder je Parameter), bildet
aber keine der fünf integrierten Auswertungen der KWRA — Priorisierung, Charakterisierung,
Gewissheits-Quervergleich, Querverbindungsanalyse, Systembereichs-Vergleich — systematisch
und vollständig nach. Keine Lücke wurde behoben, kein Produktcode wurde angefasst — das war
nicht Aufgabe dieses Pakets.

Prüflauf der in Zeilen 6–10 genannten Belegpfade (`ls -d` je Pfad):

```
$ ls -d frontend/src/pages/roadmap/roadmapData.ts
frontend/src/pages/roadmap/roadmapData.ts
$ ls -d docs/KATALOG_KRITIK.md
docs/KATALOG_KRITIK.md
$ ls -d frontend/src/components/ParameterTable.tsx
frontend/src/components/ParameterTable.tsx
$ ls -d docs/evidenz/register.md
docs/evidenz/register.md
$ ls -d backend/app/data/catalog.py
backend/app/data/catalog.py
```

Kein Pfad wurde als `No such file` gemeldet; alle fünf zitierten Belegpfade der Zeilen 6–10
existieren im Produkt-Repo.

Für das Inhaltsverzeichnis wurden erneut die Seiten 1–10 gelesen (bereits vorhandener Fund aus
Zeile 1–5, hier nicht erneut gegen das Seitenbudget gezählt). Für die Kapitelinhalte wurden die
Seiten 78–83 (Kapitel 3.3 und 3.4), 136–142 (Kapitel 6.1 und 6.2) sowie 146–149 (Kapitel 7,
Anfang) gelesen. Insgesamt 18 PDF-Seiten für die neuen Zeilen, innerhalb des Rahmens von
höchstens 40 Seiten.

### Nachtrag: Zeilen 11–15 (Teilpaket 3, Bundes-Klimaanpassungsgesetz — KAnG)

Fünf weitere Anforderungen (Zeilen 11–15) wurden direkt aus dem Gesetzestext des
Bundes-Klimaanpassungsgesetzes (KAnG) erfasst, abgerufen per WebFetch ausgehend von
https://www.gesetze-im-internet.de/kang/ (Inhaltsübersicht) und den dort verlinkten
Einzelnormen. Erfasst wurden: keine als `erfüllt`, drei (Zeilen 11, 13, 15) als `teilweise`
und zwei (Zeilen 12, 14) als `offen`. Je Zeile die abgerufene URL, der Paragraf/Absatz und die
Paragrafenüberschrift im Wortlaut der Quelle:

- Zeile 11: https://www.gesetze-im-internet.de/kang/__4.html — § 4 Abs. 1, Paragrafenüberschrift
  „Klimarisikoanalyse; Datenerhebung“. Wortlaut Abs. 1: „Die Bundesregierung erstellt eine
  Klimarisikoanalyse nach dem aktuellen Stand der Wissenschaft und veröffentlicht sie. Die
  Klimarisikoanalyse ist mindestens alle acht Jahre zu aktualisieren.“
- Zeile 12: https://www.gesetze-im-internet.de/kang/__3.html — § 3 Abs. 1, Paragrafenüberschrift
  „Vorsorgende Klimaanpassungsstrategie“. Wortlaut Abs. 1: „Die Bundesregierung legt bis zum
  Ablauf des 30. September 2025 eine vorsorgende Klimaanpassungsstrategie mit messbaren Zielen
  vor. Sie setzt sie im Rahmen ihrer Zuständigkeit um und schreibt sie unter Berücksichtigung
  aktueller wissenschaftlicher Erkenntnisse alle vier Jahre fort.“
- Zeile 13: https://www.gesetze-im-internet.de/kang/__8.html — § 8 Abs. 1, Paragrafenüberschrift
  „Berücksichtigungsgebot“. Wortlaut Abs. 1: „Die Träger öffentlicher Aufgaben haben bei ihren
  Planungen und Entscheidungen das Ziel der Klimaanpassung nach § 1 fachübergreifend und
  integriert zu berücksichtigen.“
- Zeile 14: https://www.gesetze-im-internet.de/kang/__12.html — § 12 Abs. 1, Paragrafenüberschrift
  „Klimaanpassungskonzepte“. Wortlaut Abs. 1: „Die Länder bestimmen im Rahmen der Grenzen des
  Artikels 28 Absatz 2 des Grundgesetzes diejenigen öffentlichen Stellen, die für die Gebiete der
  Gemeinden und Kreise jeweils ein Klimaanpassungskonzept – soweit nicht bereits vorhanden –
  aufstellen.“
- Zeile 15: https://www.gesetze-im-internet.de/kang/__12.html — § 12 Abs. 3, Paragrafenüberschrift
  „Klimaanpassungskonzepte“. Wortlaut Abs. 3: „Klimaanpassungskonzepte sollen auf einer
  Klimarisikoanalyse im Sinne einer Feststellung von potentiellen prioritären Risiken und sehr
  dringlichen Handlungserfordernissen (Betroffenheitsanalyse) oder vergleichbaren
  Entscheidungsgrundlagen beruhen.“

Grund für die Einstufungen: Das Produkt unterstützt Kommunen und Berater bei der inhaltlichen,
risikobasierten Grundlage von Klimaanpassungskonzepten (Zeilen 11, 15 teilweise), prüft aber
nicht, ob eine konkrete Planung das Berücksichtigungsgebot tatsächlich erfüllt (Zeile 13
teilweise), und adressiert weder die Bundesstrategie mit ihrem Fortschreibungszyklus noch die
länderrechtliche Zuständigkeitsbestimmung, wer ein Konzept aufstellen muss (Zeilen 12 und 14
offen) — diese Pflichten richten sich an Bundesregierung beziehungsweise Länder, nicht an ein
Software-Werkzeug. Keine Lücke wurde behoben, kein Produktcode wurde angefasst — das war nicht
Aufgabe dieses Pakets.

Prüflauf der in Zeilen 11–15 genannten Belegpfade (`ls -d` je Pfad):

```
$ ls -d docs/methodik/95_hitzebelastung.md
docs/methodik/95_hitzebelastung.md
$ ls -d backend/app/data/catalog.py
backend/app/data/catalog.py
$ ls -d frontend/src/components/MeasuresTableTab.tsx
frontend/src/components/MeasuresTableTab.tsx
$ ls -d frontend/src/pages/roadmap/roadmapData.ts
frontend/src/pages/roadmap/roadmapData.ts
```

Kein Pfad wurde als `No such file` gemeldet; alle vier zitierten Belegpfade der Zeilen 11–15
existieren im Produkt-Repo (Zeile 11 und 15 verweisen teils auf denselben Pfad wie eine vorherige
Zeile).

### Nachtrag: Zeilen 16–20 (Teilpaket 4, ISO 14091:2021 — Sekundärquelle)

Die ISO 14091:2021 selbst liegt nicht im Repo und wurde nicht beschafft. Als Sekundärquelle wurde
das PDF des Umweltbundesamts "Klimarisikoanalysen auf kommunaler Ebene – Handlungsempfehlungen
zur Umsetzung der ISO 14091" (Autor*innen: Luise Porst, Maike Voß, Walter Kahlenborn, Inke
Schauser; Stand Juni 2022) abgerufen, verlinkt unter
https://www.umweltbundesamt.de/publikationen/klimarisikoanalysen-auf-kommunaler-ebene, direkter
PDF-Pfad https://www.umweltbundesamt.de/system/files/medien/479/publikationen/2022_uba-fachbroschuere_kra_auf_kommunaler_ebene.pdf.
Diese Broschüre fasst die Kapitelstruktur der ISO 14091:2021 zusammen und ordnet ihre eigenen
Abschnitte 2.1–2.3 den Kapiteln der Norm explizit über Fußnoten zu; sie gibt den Norminhalt in
eigenen Worten wieder (keine Wortlautzitate der Norm selbst). Ergänzend wurde eine Websuche zur
groben Orientierung über den Kapitelaufbau (5 Vorbereitung, 6 Durchführung, 7 Berichterstattung
und Kommunikation) durchgeführt; für die in der Tabelle genannten Kapitelnummern wurde jedoch
ausschließlich die tatsächlich abgerufene PDF-Quelle als Beleg verwendet, da nur dort die
Zuordnung Abschnitt → Kapitel explizit und geprüft vorliegt (Fußnote 5: "Kapitel 5 der ISO
14091" zu Abschnitt 2.1; Fußnote 27: "Kapitel 6 der ISO 14091" zu Abschnitt 2.2; Fußnote 35:
"Kapitel 7 der ISO 14091" zu Abschnitt 2.3; Fußnote 33: "Anhang G ... und H ... der ISO 14091"
zur Anpassungskapazität in Abschnitt 2.2.5).

Herkunft der einzelnen Zeilen aus derselben URL (Kapitelnummer und Inhalt jeweils daraus
abgeleitet):

- Zeile 16: https://www.umweltbundesamt.de/publikationen/klimarisikoanalysen-auf-kommunaler-ebene
  — PDF-Abschnitt 2.1.2 "Bestandsaufnahme" (S. 12), Fußnote 7 ("In der ISO 14091 wird dieser
  Abschnitt der KRA als 'Festlegung des Kontexts' bezeichnet") und Fußnote 5 ("Kapitel 5 der ISO
  14091" für den gesamten Abschnitt 2.1).
- Zeile 17: dieselbe URL — PDF-Abschnitt 2.1.2 "Interessierte Parteien identifizieren und
  partizipative Ansätze planen" (S. 13), ebenfalls unter Kapitel 5 (Fußnote 5).
- Zeile 18: dieselbe URL — PDF-Abschnitt 2.2.5 "Optional: Anpassungskapazität analysieren und
  bewerten" (S. 28f.), Fußnote 27 ("Kapitel 6 der ISO 14091" für Abschnitt 2.2) sowie Fußnote 33
  ("Anhang G ... und H ... der ISO 14091") für die vier Komponenten der Anpassungskapazität.
- Zeile 19: dieselbe URL — PDF-Abschnitt 2.2.6 "Ergebnisse interpretieren" (S. 29f.), unter
  Kapitel 6 (Fußnote 27).
- Zeile 20: dieselbe URL — PDF-Abschnitt 2.3.2 "Ergebnisse zielgruppenspezifisch kommunizieren"
  (S. 31), unter Kapitel 7 (Fußnote 35).

Fünf weitere Anforderungen (Zeilen 16–20) wurden erfasst: keine als `erfüllt`, vier (Zeilen 16,
18, 19, 20) als `teilweise` und eine (Zeile 17) als `offen`. Grund: Das Produkt liefert
quantitative Risiko- und Methodik-Inhalte je Klimawirkung, deckt aber die prozessualen
Vorbereitungs- und Kommunikationsschritte der Norm (Bestandsaufnahme vulnerabler Gruppen,
Beteiligungsverfahren, komponentenweise Anpassungskapazität, regionsübergreifende
Unsicherheitsinterpretation, zielgruppendifferenzierte Kommunikationsprodukte) nur ansatzweise
oder gar nicht ab. Keine Lücke wurde behoben, kein Produktcode wurde angefasst — das war nicht
Aufgabe dieses Pakets.

Prüflauf der in Zeilen 16–20 genannten Belegpfade (`ls -d` je Pfad):

```
$ ls -d docs/methodik/95_hitzebelastung.md
docs/methodik/95_hitzebelastung.md
$ ls -d backend/app/data/catalog.py
backend/app/data/catalog.py
$ ls -d docs/methodik/61_vegetation_in_siedlungen.md
docs/methodik/61_vegetation_in_siedlungen.md
$ ls -d docs/evidenz/register.md
docs/evidenz/register.md
$ ls -d frontend/src/components/MeasuresTableTab.tsx
frontend/src/components/MeasuresTableTab.tsx
```

Kein Pfad wurde als `No such file` gemeldet; alle fünf zitierten Belegpfade der Zeilen 16–20
existieren im Produkt-Repo.

### Nachtrag: Zeilen 21–25 (Teilpaket 5, UBA Methodenkonvention 4.0 — Monetarisierung)

Fünf weitere Anforderungen (Zeilen 21–25) wurden aus dem UBA Handbuch Umweltkosten -
Methodenkonvention 4.0 erfasst (`docs/UBA/UBA_Handbuch Umweltkosten_Methodenkonvention 4.0.pdf`,
gelesen mit `scripts/pdf_text.py`, siehe T-0351). Erfasst wurden: eine (Zeile 23, Preisbasisjahr)
und eine (Zeile 24, Ausweis von Unsicherheit) als `erfüllt`, drei (Zeilen 21, 22, 25) als
`teilweise`. Grund: Das Produkt führt für Gesundheitswirkungen den Schadenskostenansatz, weicht
aber für Gebäudeschäden bei Flusshochwasser auf Wiederherstellungskosten aus (Zeile 21); die
mehrjährige Kosten-Projektion diskontiert nicht, benennt das aber offen als Annahme (Zeile 22);
Preisbasisjahr und Bandbreiten sind im Evidenz-Register durchgängig und nachvollziehbar geführt
(Zeilen 23, 24 erfüllt); nicht (vollständig) monetarisierbare Wirkungen werden nur dort explizit
gekennzeichnet, wo sie bewusst zur Vermeidung von Doppelzählung ausgeschlossen sind, nicht aber
dort, wo schlicht noch kein belegter Kostensatz vorliegt (Zeile 25). Keine Lücke wurde behoben,
kein Produktcode wurde angefasst — das war nicht Aufgabe dieses Pakets.

Für das Inhaltsverzeichnis wurden die Seiten 1–7 gelesen, für die Kapitelinhalte die Seiten 8–17
(Kapitel 1, 2.2.1–2.2.4, Anfang Kapitel 3.1). Insgesamt 16 PDF-Seiten, innerhalb des Rahmens von
höchstens 40 Seiten; das Read-Werkzeug mit `pages` wurde nicht benötigt, `scripts/pdf_text.py`
hat auf allen gelesenen Seiten Text geliefert.

Prüflauf der in Zeilen 21–25 genannten Belegpfade (`ls -d` je Pfad):

```
$ ls -d docs/methodik/60_gebaeudeschaeden_flusshochwasser.md
docs/methodik/60_gebaeudeschaeden_flusshochwasser.md
$ ls -d backend/app/data/catalog.py
backend/app/data/catalog.py
$ ls -d backend/app/services/cost_projection_service.py
backend/app/services/cost_projection_service.py
$ ls -d frontend/src/components/dashboard/CostTimelineSection.tsx
frontend/src/components/dashboard/CostTimelineSection.tsx
$ ls -d docs/evidenz/register.md
docs/evidenz/register.md
$ ls -d docs/MODELL_KRITIK.md
docs/MODELL_KRITIK.md
```

Kein Pfad wurde als `No such file` gemeldet; alle sechs zitierten Belegpfade der Zeilen 21–25
existieren im Produkt-Repo.

### Nachtrag: Abschlusszählung aller 25 Zeilen und Gegenprüfung aller Belegpfade (Teilpaket 6)

Zähllauf über die Datei, beschränkt auf Tabellenzeilen (`grep -c` mit Anker auf die Zeilennummer
und die Status-Spalte, damit die Zählmuster nicht versehentlich die eigenen, unten stehenden
Befehlszeilen dieses Transkripts miterfassen; wörtliche Ausgabe):

```
$ grep -c '^| [0-9].*| erfüllt |' docs/KONFORMITAET_CHECKLISTE.md
6
$ grep -c '^| [0-9].*| teilweise |' docs/KONFORMITAET_CHECKLISTE.md
14
$ grep -c '^| [0-9].*| offen |' docs/KONFORMITAET_CHECKLISTE.md
5
$ grep -c '^| [0-9]' docs/KONFORMITAET_CHECKLISTE.md
25
```

6 + 14 + 5 = 25 entspricht der Gesamtzahl der Anforderungszeilen; die Tabelle umfasst damit
alle 25 Zeilen.

Gegenprüflauf sämtlicher Belegpfade aller Zeilen mit Status `erfüllt` oder `teilweise`
(12 verschiedene Pfade insgesamt, aus 20 Zeilen mit teils wiederkehrenden Pfaden; `ls -d`
je Pfad, wörtliche Ausgabe):

```
$ ls -d docs/methodik/95_hitzebelastung.md
docs/methodik/95_hitzebelastung.md
$ ls -d docs/methodik/61_vegetation_in_siedlungen.md
docs/methodik/61_vegetation_in_siedlungen.md
$ ls -d docs/evidenz/register.md
docs/evidenz/register.md
$ ls -d docs/methodik/60_gebaeudeschaeden_flusshochwasser.md
docs/methodik/60_gebaeudeschaeden_flusshochwasser.md
$ ls -d frontend/src/pages/roadmap/roadmapData.ts
frontend/src/pages/roadmap/roadmapData.ts
$ ls -d docs/KATALOG_KRITIK.md
docs/KATALOG_KRITIK.md
$ ls -d frontend/src/components/ParameterTable.tsx
frontend/src/components/ParameterTable.tsx
$ ls -d backend/app/data/catalog.py
backend/app/data/catalog.py
$ ls -d frontend/src/components/MeasuresTableTab.tsx
frontend/src/components/MeasuresTableTab.tsx
$ ls -d backend/app/services/cost_projection_service.py
backend/app/services/cost_projection_service.py
$ ls -d frontend/src/components/dashboard/CostTimelineSection.tsx
frontend/src/components/dashboard/CostTimelineSection.tsx
$ ls -d docs/MODELL_KRITIK.md
docs/MODELL_KRITIK.md
```

Kein Pfad wurde als `No such file` gemeldet; alle Belegpfade aller Zeilen mit Status `erfüllt`
oder `teilweise` existieren im Produkt-Repo. Keine Lücke wurde behoben, kein Produktcode wurde
angefasst — das war nicht Aufgabe dieses Pakets.

## Zusammenfassung

Die Tabelle umfasst alle 25 Anforderungszeilen. Ausgezählt nach Status (Zähllauf und
Gegenprüfung der Belegpfade siehe Abschnitt Ergebnis, Nachtrag "Abschlusszählung"): 6 Zeilen
`erfüllt`, 14 Zeilen `teilweise` und 5 Zeilen `offen`; 6 + 14 + 5 = 25 entspricht der
Gesamtzahl der Anforderungszeilen. Alle 12 im Produkt genannten, unterschiedlichen Belegpfade
der erfüllt/teilweise-Zeilen wurden mit `ls -d` gegengeprüft; kein Pfad wurde als
`No such file` gemeldet. Die Checkliste ist damit für alle 25 Zeilen vollständig erfasst und
die zitierten Belegpfade sind gegengeprüft; keine Lücke wurde behoben, kein Produktcode wurde
angefasst — das war nicht Aufgabe dieses Pakets.

## Nenner der Konformitätsaussage

Entscheid des Aufsichtsrats vom 23.09.2026: Die Zeilen 11 und 12 richten sich ausschließlich an
die Bundesregierung (Klimarisikoanalyse nach § 4 KAnG bzw. Klimaanpassungsstrategie nach § 3
KAnG) und zählen deshalb nicht im Nenner einer Konformitätsaussage dieses Produkts — ein
Werkzeug für Kommunen und Beratungsbüros kann diese Pflichten von vornherein nicht erfüllen.
Zeile 14 richtet sich dagegen an die Länder, die zur Zielgruppe der Konformitätsaussage
gehören; ihre Anforderung zählt im Nenner mit. Der Nenner jeder Konformitätsaussage ist damit
23 von 25 Zeilen (25 Zeilen insgesamt minus die beiden Bundeszeilen 11 und 12).
