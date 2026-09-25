# Abgleich der benannten Beziehungen und Rückkopplungen mit den Klimawirkungsketten (UBA 2016)

Konformitätszeile 9, Anforderung A2 (Vorhaben T-0870-ceo, Teilpaket T-0942-cto, Stand 25.09.2026).

## Gegenstand

Geprüft wird, ob die Beziehungen, die das Produkt aus der KWRA 2021 übernimmt, schon in den
Klimawirkungsketten des Umweltbundesamts von 2016 dargestellt sind. Abgeglichen werden:

- alle Einträge in `app.data.kwra_querverbindungen.BENANNTE_BEZIEHUNGEN` mit Ebene „Klimawirkung“
  (15 Einträge; die Einträge auf Handlungsfeld- und gemischter Ebene haben kein einzelnes Ende, das
  sich einem Kettenelement zuordnen ließe) und
- die gegenseitigen Beziehungen aus `app.data.kwra_rueckkopplungen.RUECKKOPPLUNGEN` (RK-1, RK-3 und
  das gegenseitige Paar im Kreislauf RK-2). Alle drei stehen auch in `BENANNTE_BEZIEHUNGEN`; sie
  bekommen deshalb keine eigene Zeile, die Spalte „Herkunft“ nennt beide Datenmodule.

Die Tabelle hat damit genau eine Zeile je Beziehung, 15 Zeilen.

## Quelle und Lesart

eurac research und Bosch & Partner: *Klimawirkungsketten*. Umweltbundesamt, Stand November 2016.
Datei `docs/KWAR/klimawirkungsketten_umweltbundesamt_2016.pdf`, 15 Seiten ohne gedruckte
Seitenzahlen. Seitenangaben unten sind **PDF-Seiten**: S. 1 Erläuterungen, S. 3 Biologische Vielfalt,
S. 5 Wald- und Forstwirtschaft, S. 8 Wasserhaushalt, Wasserwirtschaft, S. 9 Verkehr,
Verkehrsinfrastruktur, S. 10 Bauwesen, S. 11 Industrie und Gewerbe, S. 12 Energiewirtschaft,
S. 15 Menschliche Gesundheit.

Gelesen wurden die Erläuterungen (S. 1) vollständig im Text und die Seiten 3, 5, 8, 9, 10, 11, 12 und 15
als Bild. Die Diagramme lassen sich als Text nicht auswerten, weil die Pfeile fehlen.

Nach S. 1 steht neben jedem Pfeilendpunkt der Titel des Ausgangselements. Ein Pfeil, der auf einen
Container führt, betrifft alle Klimawirkungen des Containers; ein Pfeil auf ein Sechseck nur diese
Klimawirkung. Klimawirkungen aus anderen Handlungsfeldern erscheinen als kleinere Container mit
„Von: <Handlungsfeld>“. Das Urteil liest deshalb den Pfeil am Ziel: Steht das Ausgangselement (oder
sein Container) in der Beschriftung des Pfeils auf das Ziel, ist die Beziehung dargestellt.

Urteile:

- **bestätigt**: UBA 2016 zeigt einen Pfeil vom Ausgangselement (oder seinem Container) auf das Ziel
  (oder dessen Container), in jeder genannten Richtung.
- **teilweise**: UBA 2016 zeigt die Wirkung nur mittelbar über ein Zwischenelement, nur für einen Teil
  der gebündelten KWRA-Klimawirkung oder bei einer gegenseitigen Beziehung nur eine Richtung.
- **nicht dargestellt**: kein Pfeil zwischen den beiden Elementen, auch nicht mittelbar.

## Abgleich

| Nr | Von | Nach | Richtung | Herkunft | Urteil | Beleg in UBA 2016 |
|---|---|---|---|---|---|---|
| 1 | #49 Hochwasser | zahlreiche Klimawirkungen in mehreren Handlungsfeldern | gerichtet | BENANNTE_BEZIEHUNGEN | bestätigt | S. 8: Container „Abfluss und Wasserstand von Oberflächengewässern“ (mit Hochwasser) führt „Zu: Boden; Küsten- und Meeresschutz; Landwirtschaft; Fischerei; Menschliche Gesundheit; Industrie und Gewerbe; Energiewirtschaft; Tourismuswirtschaft; Verkehr, Verkehrsinfrastruktur; Bauwesen“; als „Von: Wasserhaushalt, Wasserwirtschaft“ mit Hochwasser auf S. 3, 9, 10, 11, 12 und 15. |
| 2 | #53 Gewässertemperatur und Eisbedeckung und biologische Wasserqualität | #97 Potenziell schädliche Mikroorganismen und Algen | gerichtet | BENANNTE_BEZIEHUNGEN | teilweise | S. 15: Pfeil „Oberflächengewässer: Biologische Wasserqualität (Eutrophierung, Blaualgen)“ und Pfeile „Badewasser“, „Trinkwasser“ auf den Container „Gesundheitliche Auswirkungen verminderter Bade- und Trinkwasserqualität und Lebensmittelsicherheit“ mit „Potentiell schädliche Mikroorganismen und Algen“. Dargestellt ist nur der Bestandteil biologische Wasserqualität von #53; die Gewässertemperatur ist auf S. 8 ein eigenes Element ohne Pfeil zur Gesundheit, die Förderung der Algen durch Wärme (KWRA S. 84) ist nicht gezeichnet. |
| 3 | #62 Stadtklima / Wärmeinseln | #95 Hitzebelastung | gerichtet | BENANNTE_BEZIEHUNGEN | bestätigt | S. 15: Pfeil „Hitze; Stadtklima / Wärmeinseln“ auf „Hitzebelastung“; ebenso S. 10 („Hitze; Stadtklima / Wärmeinseln“ auf „Hitzebelastung“, Von: Menschliche Gesundheit). |
| 4 | #1 Veränderung der Länge der Vegetationsperiode und Phänologie | #96 Allergische Reaktionen durch Aeroallergene pflanzlicher Herkunft | gerichtet | BENANNTE_BEZIEHUNGEN | teilweise | S. 3: „Länge der Vegetationsperiode“ wirkt auf „Phänologie“ im Container „Vegetation“ (mit „Pollenflug“); S. 15: Pfeil „Vegetation“ auf „Allergische Reaktionen durch Aeroallergene pflanzlicher Herkunft (z. B. Pollen)“. Die Wirkung läuft über den Container Vegetation; einen Pfeil von der Länge der Vegetationsperiode selbst gibt es nicht, „Pollenflug“ erhält auf S. 3 nur Durchschnittstemperatur und Trockenheit. |
| 5 | #49 Hochwasser | #101 Verletzungen und Todesfälle infolge von Extremereignissen | gerichtet | BENANNTE_BEZIEHUNGEN | bestätigt | S. 15: Pfeil „… Abfluss und Wasserstand von Oberflächengewässern …“ auf „Verletzungen und Todesfälle infolge von Extremereignissen“; der Container enthält auf S. 15 „Hochwasser“ und „Sturzfluten“. |
| 6 | #51 Sturzfluten (Versagen von Entwässerungseinrichtungen und Überflutungsschutzsystemen) | #101 Verletzungen und Todesfälle infolge von Extremereignissen | gerichtet | BENANNTE_BEZIEHUNGEN | bestätigt | S. 15: derselbe Pfeil wie in Zeile 5; „Sturzfluten“ steht im Container „Abfluss und Wasserstand von Oberflächengewässern“. |
| 7 | #48 Niedrigwasser | #82 Beeinträchtigung des Warenverkehrs über Wasserstraßen (Inland) | gerichtet | BENANNTE_BEZIEHUNGEN | teilweise | S. 9: Pfeil „Hochwasser; Niedrigwasser; …“ auf „Schiffbarkeit der Wasserstraßen“; S. 11: Pfeil „Schiffbarkeit der Wasserstraßen“ auf „Beeinträchtigung des Warenverkehrs über Wasserstraßen“ (Von: Verkehr, Verkehrsinfrastruktur). Mittelbar über die Schiffbarkeit, kein direkter Pfeil. |
| 8 | #49 Hochwasser | #74 Schäden / Hindernisse bei Straßen und Schienenwegen (Hochwasser) | gerichtet | BENANNTE_BEZIEHUNGEN | bestätigt | S. 9: Pfeil mit „… Hochwasser …“ auf „Schäden an Straßen, Schieneninfrastruktur, Startbahnen“; „Hochwasser“ steht dort im Container „Von: Wasserhaushalt, Wasserwirtschaft“. |
| 9 | #13 Wassermangel im Boden | #8 Schäden an Wäldern | gerichtet | BENANNTE_BEZIEHUNGEN | teilweise | S. 5: „Wassermangel im Boden“ (Container „Bodenwasserhaushalt“, Von: Boden) wirkt über „Bodenwasserhaushalt“ auf „Vitalität / Mortalitätseffekte“ (u. a. „Hitze- und Trockenstress“) und auf „Güter und Dienstleistungen des Waldes“. „Schäden an Wäldern“ erhält auf S. 3 und S. 5 keinen Pfeil vom Bodenwasserhaushalt, sondern von „Trockenheit“ (klimatischer Einfluss) und von der Beeinträchtigung der Vitalität von Pflanzen und Tieren. |
| 10 | #8 Schäden an Wäldern | #31 Nutzfunktion: Holzertrag | gerichtet | BENANNTE_BEZIEHUNGEN | bestätigt | S. 5: Pfeil „… Schäden an Wäldern …“ auf den Container „Güter und Dienstleistungen des Waldes“ mit „Nutzfunktionen (Ertrag)“. |
| 11 | #8 Schäden an Wäldern | #32 Nutzfunktion: Erholung | gerichtet | BENANNTE_BEZIEHUNGEN | bestätigt | S. 5: derselbe Pfeil wie in Zeile 10; der Container enthält „Erholungsfunktionen“. |
| 12 | #53 Gewässertemperatur und Eisbedeckung und biologische Wasserqualität | #68 Mangelndes Kühlwasser für thermische Kraftwerke | gegenseitig | BENANNTE_BEZIEHUNGEN, RUECKKOPPLUNGEN RK-1 | teilweise | Nur eine Richtung. S. 12: Pfeil „Hitze; Gewässertemperatur; Niedrigwasser“ auf „Mangelndes Kühlwasser für thermische Kraftwerke“. Rückrichtung fehlt: „Gewässertemperatur und Eisbedeckung“ erhält auf S. 8 nur Durchschnittstemperatur, Hitze, Kälte / Frost, Schneeschmelze und Sonnenscheindauer; „Abhängigkeit von Kühlwassereinleitungen in Flüsse“ steht auf S. 12 nur als Sensitivität der Energiewirtschaft. |
| 13 | #65 Bedarf an Kühlenergie | #62 Stadtklima/Wärmeinseln | gegenseitig | BENANNTE_BEZIEHUNGEN, RUECKKOPPLUNGEN RK-2 | nicht dargestellt | S. 10: „Stadtklima/Wärmeinseln“ erhält „Hitze; Sonnenscheindauer; Vegetation in Siedlungen“; „Bedarf an Kühlenergie“ erhält „Durchschnittstemperatur; Hitze; Luftfeuchtigkeit; Innenraumklima“. S. 12: „Bedarf an Kühlenergie“ erhält „Durchschnittstemperatur; Hitze; Luftfeuchtigkeit“. Kein Pfeil in einer der beiden Richtungen. |
| 14 | #95 Hitzebelastung | #65 Bedarf an Kühlenergie | gerichtet | BENANNTE_BEZIEHUNGEN | nicht dargestellt | S. 10 und S. 12: wie Zeile 13, „Hitzebelastung“ steht in keiner Pfeilbeschriftung auf „Bedarf an Kühlenergie“. |
| 15 | #4 Verschiebung von Arealen und Rückgang der Bestände | #61 Vegetation in Siedlungen | gegenseitig | BENANNTE_BEZIEHUNGEN, RUECKKOPPLUNGEN RK-3 | teilweise | Nur eine Richtung. S. 10: Pfeil „Verschiebung von Arealen“ (Von: Biologische Vielfalt) auf „Vegetation in Siedlungen“. Rückrichtung fehlt: der Container „Areale, Arten und Populationen“ erhält auf S. 3 keinen Pfeil aus dem Bauwesen. |

## Ergebnis

7 × bestätigt, 6 × teilweise, 2 × nicht dargestellt.

- Die Beziehungen, die in beiden Quellen gleich laufen, betreffen vor allem Hochwasser, Sturzfluten,
  den Wald und die Wirkung des Stadtklimas auf die Hitzebelastung.
- Der **Rückkopplungskreislauf** der KWRA 2021 (Hitzebelastung → Bedarf an Kühlenergie ↔
  Stadtklima/Wärmeinseln → Hitzebelastung, Teilbericht 6, S. 85–86, Abb. 9) steht in UBA 2016 nur mit
  seinem ersten Glied (Stadtklima/Wärmeinseln → Hitzebelastung, Zeile 3). Die beiden anderen Glieder
  (Zeilen 13 und 14) fehlen dort. Der Kreislauf ist damit eine Aussage der KWRA 2021, keine Übernahme
  aus den Wirkungsketten von 2016. Das Produkt stützt ihn auf Teilbericht 6, nicht auf UBA 2016.
- Bei zwei der drei gegenseitigen Beziehungen (Zeilen 12 und 15) zeigt UBA 2016 nur eine Richtung.
  Die Rückrichtung stammt aus dem Fließtext von Teilbericht 6.

## Modellgrenze

UBA 2016 ist eine Darstellung auf Ebene von Elementen und Containern, nicht die Klimawirkungsliste der
KWRA 2021. Die Namen weichen ab (etwa „Schäden an Wäldern“ statt „Schäden in Wäldern“, „Nutzfunktionen
(Ertrag)“ statt „Nutzfunktion: Holzertrag“), und einige KWRA-Klimawirkungen bündeln zwei Elemente von
2016 (#53: Gewässertemperatur und biologische Wasserqualität; #1: Vegetationsperiode und Phänologie).
Die Zuordnung ist eine Lesart dieses Abgleichs, keine Angabe der Quelle. Die Pfeile sind aus den
Abbildungen abgelesen; eine Kantenliste veröffentlicht UBA 2016 nicht. Der Abgleich ändert keine Daten
im Produkt, weder in `BENANNTE_BEZIEHUNGEN` noch in `RUECKKOPPLUNGEN`.
