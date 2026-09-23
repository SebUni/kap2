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
| 7 | Klimawirkungen mit sehr dringenden Handlungserfordernissen sind anhand von Anpassungspotenzial und Bewertungsgewissheit in Charakterisierungsgruppen (Umsetzung, Entwicklung, Entwicklung unter Unsicherheit, Innovation, Innovation unter Unsicherheit) einzuordnen, um den Handlungstyp zu benennen. | KWRA 2021 | kwra2021_teilbericht_6_integrierte_auswertung_bf_211027_0.pdf, Kap. 6.2 (S. 140–142) | offen | — | Im Produkt gibt es weder eine Kennzeichnung von Maßnahmen oder Klimawirkungen nach diesen fünf KWRA-Kategorien noch eine vergleichbare Systematik, die zwischen "Umsetzung bestehender Planungen", "Entwicklung weiterreichender Maßnahmen" und "Innovation/tiefgreifende Anpassung" unterscheidet; die Maßnahmentabelle (frontend/src/components/MeasuresTableTab.tsx) führt Maßnahmen ohne diese Einordnung. |
| 8 | Die Bewertungsgewissheit ist für jede Klimawirkung auf einer einheitlichen, mehrstufigen Skala (sehr gering bis hoch) auszuweisen und handlungsfeldübergreifend vergleichbar zu machen, damit erkennbar ist, wo hohe Unsicherheiten vorsichtige Interpretation erfordern. | KWRA 2021 | kwra2021_teilbericht_6_integrierte_auswertung_bf_211027_0.pdf, Kap. 3.3 (S. 78–82) | erfüllt | backend/app/services/gewissheit.py, backend/app/api/routes/catalog.py, backend/tests/test_gewissheitsstufe.py | Jede Klimawirkung trägt eine kategoriale Gewissheitsstufe auf der vierstufigen Skala sehr gering/gering/mittel/hoch, abgeleitet nach einer dokumentierten Regel aus den Evidenzklassen ihrer Parameter und damit handlungsfeldübergreifend vergleichbar. |
| 9 | Wechselwirkungen (Querverbindungen) zwischen einzelnen Klimawirkungen sind zu identifizieren und auszuwerten, damit erkennbar ist, welche Klimawirkungen besonders viele andere beeinflussen oder von ihnen beeinflusst werden. | KWRA 2021 | kwra2021_teilbericht_6_integrierte_auswertung_bf_211027_0.pdf, Kap. 3.4 (S. 82–89) | teilweise | backend/app/data/kwra_querverbindungen.py, backend/app/services/querverbindungen.py, docs/QUERVERBINDUNGEN_KLIMAWIRKUNGEN.md, frontend/src/components/dashboard/RiskInteractionSection.tsx | Das Produkt übernimmt Ergebnisse der KWRA-Querverbindungsanalyse (Kennzahlen, 25 Netzrollen, 20 im Fließtext genannte Beziehungen, Systembereichs-Matrix aus Kap. 7), führt die Analyse aber nicht selbst: keine eigene Identifikation der Querbezüge und kein Abgleich mit den Klimawirkungsketten (UBA 2016); keine Darstellung der Querverbindungen zwischen den 13 Handlungsfeldern (Abb. 8); keine gegenseitigen Wechselwirkungen und kein Rückkopplungskreislauf Hitzebelastung – Bedarf an Kühlenergie – Stadtklima/Wärmeinseln (Abb. 9), obwohl Hitzebelastung und Stadtklima im Katalog stehen; keine gesonderte Auswertung der hoch bewerteten Klimawirkungen; die Netzrolle ist einwertig, obwohl eine Klimawirkung Sender und Empfänger zugleich sein kann. Die Dashboard-Tabelle zeigt nur Klimawirkungen des Katalogs, 13 der 25 Netzrollen – darunter Hochwasser, die zentrale Klimawirkung – erscheinen dort nicht. Einzelnachweis: Abschnitt „Gegenprobe Zeile 9“. |

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
| 10 | Die Klimarisiken sind über die fünf übergeordneten Systembereiche (Natürliche Systeme und Ressourcen, Naturnutzende Wirtschaftssysteme, Infrastrukturen und Gebäude, Naturferne Wirtschaftssysteme, Menschen und soziale Systeme) hinweg vergleichbar auszuwerten, um Unterschiede in Risikohöhe und Anpassungsfähigkeit zwischen diesen Bereichen sichtbar zu machen. | KWRA 2021 | kwra2021_teilbericht_6_integrierte_auswertung_bf_211027_0.pdf, Kap. 7 (S. 146–155) | offen | — | Das Produkt gruppiert Risiken nach eigenen, produktspezifischen Kategorien (z. B. den 7 KAnG-Clustern in frontend/src/utils/kangColors.ts, einer rechtlichen Einteilung nach dem Klimaanpassungsgesetz), nicht nach den fünf KWRA-Systembereichen; eine Querbetrachtung, die Klimarisiken und Anpassungsfähigkeit über diese fünf Systembereiche hinweg vergleicht, existiert im Produkt nicht. |
| 11 | Die Bundesregierung erstellt eine Klimarisikoanalyse nach dem aktuellen Stand der Wissenschaft, veröffentlicht sie und aktualisiert sie mindestens alle acht Jahre, um Handlungsfelder, Klimawirkungen und Regionen mit besonders hohen Klimarisiken aufzuzeigen. | KAnG, https://www.gesetze-im-internet.de/kang/__4.html | § 4 Abs. 1 | teilweise | docs/methodik/95_hitzebelastung.md, backend/app/data/catalog.py | Das Produkt liefert eine quantitative Risikobewertung je Kommune und Klimawirkung (Methodik-Berichte, Katalog), das ist aber keine Klimarisikoanalyse der Bundesregierung im Sinne des § 4 KAnG und enthält keinen eingebauten Mechanismus, der eine Aktualisierung im gesetzlich vorgesehenen Achtjahresturnus sicherstellt oder dokumentiert. |
| 12 | Die Bundesregierung legt eine vorsorgende Klimaanpassungsstrategie mit messbaren Zielen vor, setzt sie um und schreibt sie unter Berücksichtigung aktueller wissenschaftlicher Erkenntnisse alle vier Jahre fort. | KAnG, https://www.gesetze-im-internet.de/kang/__3.html | § 3 Abs. 1 | offen | — | Das Produkt ist ein Werkzeug für Kommunen und Berater und bildet weder eine Bundesstrategie noch einen Fortschreibungszyklus ab; die Pflicht richtet sich an die Bundesregierung und wird vom Produkt nicht adressiert. |
| 13 | Die Träger öffentlicher Aufgaben haben bei ihren Planungen und Entscheidungen das Ziel der Klimaanpassung fachübergreifend und integriert zu berücksichtigen. | KAnG, https://www.gesetze-im-internet.de/kang/__8.html | § 8 Abs. 1 | erfüllt | backend/app/data/kang_handlungsfelder.py, backend/app/services/kang_beruecksichtigung.py, backend/app/services/kang_nachweis_markdown.py, docs/NACHWEIS_FACHUEBERGREIFEND_KANG.md | — |
| 14 | Die Länder bestimmen im Rahmen der Grenzen des Art. 28 Abs. 2 Grundgesetz diejenigen öffentlichen Stellen, die für die Gebiete der Gemeinden und Kreise jeweils ein Klimaanpassungskonzept aufzustellen haben, soweit nicht bereits vorhanden. | KAnG, https://www.gesetze-im-internet.de/kang/__12.html | § 12 Abs. 1 | erfüllt | docs/KANG_ZUSTAENDIGKEIT_LAENDER.md, backend/app/data/kang_zustaendigkeit.py, backend/app/api/routes/kommune.py, frontend/src/components/dashboard/KangZustaendigkeit.tsx | — |
| 15 | Klimaanpassungskonzepte sollen auf einer Klimarisikoanalyse im Sinne einer Feststellung von potentiellen prioritären Risiken und sehr dringlichen Handlungserfordernissen (Betroffenheitsanalyse) oder vergleichbaren Entscheidungsgrundlagen beruhen. | KAnG, https://www.gesetze-im-internet.de/kang/__12.html | § 12 Abs. 3 | teilweise | backend/app/data/catalog.py, frontend/src/pages/roadmap/roadmapData.ts | Wie bereits zu Zeile 6 festgehalten, übernimmt das Produkt die Kategorie "sehr dringend" punktuell in der Roadmap, ohne die zugrunde liegende Klimarisikoanalyse systematisch und vollständig nach dieser gesetzlichen Vorgabe herzuleiten; laut docs/KATALOG_KRITIK.md fehlen im heutigen Katalog Klimawirkungen, die bundesweit als sehr dringend eingestuft sind. |
| 16 | Vor der eigentlichen Risikobewertung ist der Kontext festzulegen (Bestandsaufnahme): lokale sozioökonomische und geographische Rahmenbedingungen sowie Trends sind zu erfassen, ebenso bereits vorhandene Informationen zu vergangenen und erwarteten Klimarisiken, einschließlich besonders klimasensibler Strukturen (z. B. kritische Infrastruktur) und vulnerabler Personengruppen. | ISO 14091:2021, Sekundärquelle: Umweltbundesamt, "Klimarisikoanalysen auf kommunaler Ebene – Handlungsempfehlungen zur Umsetzung der ISO 14091", https://www.umweltbundesamt.de/publikationen/klimarisikoanalysen-auf-kommunaler-ebene | Kap. 5 (dort Abschnitt 2.1.2 "Bestandsaufnahme"/"Festlegung des Kontexts", S. 12) | erfüllt | backend/app/data/bestandsaufnahme.py, backend/app/services/bestandsaufnahme_service.py, backend/app/services/bestandsaufnahme_markdown.py, docs/BESTANDSAUFNAHME.md | Keine Lücke im Produkt; Größen ohne Datenquelle je Kommune weist die Bestandsaufnahme ausdrücklich als vor Ort zu erheben aus. |
| 17 | In der Vorbereitungsphase sind interessierte Parteien mit einschlägiger Fachexpertise zu identifizieren und über partizipative Ansätze frühzeitig in die Entscheidungsfindung einzubeziehen, um ein gemeinsames Verständnis und Verantwortungsgefühl unter den Beteiligten zu fördern. | ISO 14091:2021, Sekundärquelle: Umweltbundesamt, "Klimarisikoanalysen auf kommunaler Ebene – Handlungsempfehlungen zur Umsetzung der ISO 14091", https://www.umweltbundesamt.de/publikationen/klimarisikoanalysen-auf-kommunaler-ebene | Kap. 5 (dort Abschnitt 2.1.2 "Interessierte Parteien identifizieren und partizipative Ansätze planen", S. 13) | offen | — | Das Produkt bietet keinen Prozess und keine Funktion, mit der eine Kommune interessierte Parteien identifiziert oder einen partizipativen Beteiligungsprozess plant und begleitet; es ist ein Analysewerkzeug für die inhaltliche Berechnung von Klimarisiken, keine Prozessunterstützung für Beteiligungsverfahren. |
| 18 | Optional kann die Anpassungskapazität eines betroffenen Systems analysiert und bewertet werden, unterschieden nach mehreren Komponenten (u. a. organisationsbezogene Fähigkeit, technisches Vermögen, finanzielle Fähigkeit, Fähigkeit des Ökosystems) und nach unterschiedlichen Reifegraden, um abzuleiten, wie stark sich das Klimarisiko durch Anpassung verringern lässt. | ISO 14091:2021, Sekundärquelle: Umweltbundesamt, "Klimarisikoanalysen auf kommunaler Ebene – Handlungsempfehlungen zur Umsetzung der ISO 14091", https://www.umweltbundesamt.de/publikationen/klimarisikoanalysen-auf-kommunaler-ebene | Kap. 6, Anhang G und H (Abschnitt 2.2.5 "Optional: Anpassungskapazität analysieren und bewerten", S. 28f.) | teilweise | docs/methodik/95_hitzebelastung.md, docs/methodik/61_vegetation_in_siedlungen.md | Die vorliegenden Methodik-Berichte unterscheiden Klimarisiko ohne und mit Anpassung, aber es fehlt eine systematische, nach mehreren Komponenten (organisatorisch, technisch, finanziell, ökosystemisch) untergliederte Bewertung der Anpassungskapazität, wie sie die Norm für diesen optionalen Analyseschritt vorsieht. |
| 19 | Bei der Interpretation der Analyseergebnisse sind bestehende Unsicherheiten in den zugrunde liegenden Informationen und Daten explizit zu berücksichtigen, ebenso handlungsfeld- und regionsübergreifende Abhängigkeiten, bevor daraus Handlungsoptionen formuliert werden. | ISO 14091:2021, Sekundärquelle: Umweltbundesamt, "Klimarisikoanalysen auf kommunaler Ebene – Handlungsempfehlungen zur Umsetzung der ISO 14091", https://www.umweltbundesamt.de/publikationen/klimarisikoanalysen-auf-kommunaler-ebene | Kap. 6 (Abschnitt 2.2.6 "Ergebnisse interpretieren", S. 29f.) | teilweise | docs/evidenz/register.md, docs/methodik/95_hitzebelastung.md | Das Evidenz-Register weist Unsicherheiten je Parameter aus, aber es gibt im Produkt keine zusammenfassende Interpretationsschicht, die diese Unsicherheiten handlungsfeld- und regionsübergreifend bei der Formulierung von Handlungsoptionen einbezieht; die Interpretation bleibt je Klimawirkung isoliert. |
| 20 | Die Ergebnisse der Risikobewertung sind zielgruppenspezifisch zu kommunizieren, etwa durch einen ausführlichen Bericht mit Datengrundlagen und Methodik für die Fachöffentlichkeit sowie durch leicht verständliche, prägnante Kommunikationsprodukte (z. B. Karten, Zusammenfassungen) für politische Entscheidungsträger und die breite Öffentlichkeit. | ISO 14091:2021, Sekundärquelle: Umweltbundesamt, "Klimarisikoanalysen auf kommunaler Ebene – Handlungsempfehlungen zur Umsetzung der ISO 14091", https://www.umweltbundesamt.de/publikationen/klimarisikoanalysen-auf-kommunaler-ebene | Kap. 7 (Abschnitt 2.3.2 "Ergebnisse zielgruppenspezifisch kommunizieren", S. 31) | teilweise | docs/methodik/95_hitzebelastung.md, frontend/src/components/MeasuresTableTab.tsx | Das Produkt liefert ausführliche Methodik-Berichte für die Fachöffentlichkeit und eine Maßnahmentabelle für Nutzer*innen in der Kommune, aber es fehlen eigenständige, stark vereinfachte Kommunikationsprodukte (z. B. Kartendarstellungen oder Kurzzusammenfassungen) speziell für politische Entscheidungsträger oder die breite Öffentlichkeit. |
| 21 | Die Monetarisierung von Umweltauswirkungen soll durchgängig auf dem Schadenskostenansatz beruhen; Vermeidungs- oder Wiederherstellungskosten sollen nicht als Ersatz für Schadenskosten verwendet werden, um Datenlücken zu schließen, da sie vom Minderungsziel abhängen bzw. real oder virtuell sein können und daher kein aussagekräftiger Ersatzwert sind. | UBA Methodenkonvention 4.0 | UBA_Handbuch Umweltkosten_Methodenkonvention 4.0.pdf, Kap. 1 (S. 8f.) und Kap. 2.2.1 (S. 12) | teilweise | docs/methodik/60_gebaeudeschaeden_flusshochwasser.md, backend/app/data/catalog.py | Für Gesundheitswirkungen (z. B. hitzebedingte Mortalität) folgt das Produkt dem Schadenskostenansatz (VSL/VOLY-artige Kostensätze), für Gebäudeschäden bei Flusshochwasser (#60) wird jedoch ausdrücklich mit Wiederherstellungskosten zum Neuwert (NHK, indexiert) bewertet (docs/methodik/60_gebaeudeschaeden_flusshochwasser.md, Konto K3); das Produkt wendet damit je nach Schadenskategorie unterschiedliche, nicht vereinheitlichte Kostenkonzepte an, statt durchgängig den von der Methodenkonvention empfohlenen Schadenskostenansatz zu verwenden, und dokumentiert diesen Methodenwechsel nicht als bewusste Abweichung von der Konvention. |
| 22 | Zukünftige Kosten und Nutzen sind unter Verwendung einer Diskontrate (u. a. der Reinen Zeitpräferenzrate) auf den heutigen Tag abzuzinsen; es werden mindestens zwei Werte (0 % und 1 % RZPR) berichtet, um die Sensitivität der Ergebnisse gegenüber der Zeitpräferenz zu zeigen. | UBA Methodenkonvention 4.0 | UBA_Handbuch Umweltkosten_Methodenkonvention 4.0.pdf, Kap. 2.2.3 (S. 14f.) | erfüllt | backend/app/services/cost_projection_service.py, backend/tests/test_kostenprojektion_diskontierung.py | Die Kostenprojektion 2025–2065 weist die kumulierten Kosten zusätzlich als Barwerte mit 0 % und 1 % Reiner Zeitpräferenzrate aus; die Sensitivität gegenüber der Zeitpräferenz ist damit berichtet. |
| 23 | Kostensätze sind einem eindeutigen Preisbasisjahr zuzuordnen; für die Anwendung auf Aktivitäten oder Emissionen anderer Jahre ist eine Preisanpassung anhand eines Preis- bzw. Verbraucherpreisindexes vorzunehmen. | UBA Methodenkonvention 4.0 | UBA_Handbuch Umweltkosten_Methodenkonvention 4.0.pdf, Kap. 1 (S. 9) | erfüllt | docs/evidenz/register.md, docs/methodik/60_gebaeudeschaeden_flusshochwasser.md | — |
| 24 | Ergebnisse der Monetarisierung sind als Schätzungen mit ausgewiesener Unsicherheit (Bandbreiten, Größenordnung statt Scheingenauigkeit) darzustellen; Modelle mit stochastischen Komponenten sollen die Unsicherheit einzelner Bestandteile und des Gesamtprozesses systematisch abbilden. | UBA Methodenkonvention 4.0 | UBA_Handbuch Umweltkosten_Methodenkonvention 4.0.pdf, Kap. 1 (S. 9) und Kap. 2.2.2 (S. 13) | erfüllt | docs/evidenz/register.md, docs/methodik/60_gebaeudeschaeden_flusshochwasser.md | — |
| 25 | Wirkungskategorien, die im gewählten Bewertungsmodell nicht oder nicht vollständig erfasst werden (z. B. Biodiversität, weitere nicht abgedeckte Klimafolgen), sind zu benennen; die resultierenden Kostensätze sind dann als konservative Schätzung bzw. Untergrenze der tatsächlichen Auswirkungen kenntlich zu machen, statt die fehlende Wirkung stillschweigend weg­zulassen. | UBA Methodenkonvention 4.0 | UBA_Handbuch Umweltkosten_Methodenkonvention 4.0.pdf, Kap. 2.2.2 (S. 13f.) und Kap. 3.1, Fn. 14 (S. 17) | teilweise | backend/app/data/catalog.py, docs/MODELL_KRITIK.md | Der Katalog kennzeichnet Risiken, die aus Doppelzählungsgründen bewusst mit Kostensatz 0 € geführt werden, mit einer erklärenden `cost_source`/`cost_source_detail` (Verweis auf docs/MODELL_KRITIK.md §6); für nicht bewusst ausgeschlossene, sondern methodisch schlicht (noch) nicht abgedeckte Wirkungen greift dagegen das im Code selbst so benannte „Sicherheitsnetz“ (`cost_per_outcome_eur` Default 0,0, Quelle „Modellannahme (Kostensatz, unbelegt)“), ohne dass die daraus resultierende Gesamtsumme im Produkt als konservative Untergrenze ausgewiesen wird. |

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
