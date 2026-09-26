# Bestandsaufnahme

## Zweck und Einordnung

Die Bestandsaufnahme ist der Risikoberechnung vorgeschaltet. Sie stellt zusammen, was über eine Kommune bereits bekannt ist: welche Bevölkerungsgruppen besonders verletzlich sind, welche klimasensiblen Einrichtungen und Infrastrukturen es gibt und welche Schadensereignisse durch Wetterextreme bereits eingetreten sind. Damit folgt das Produkt der Bestandsaufnahme als vorgeschalteter Phase der Klimarisikoanalyse nach ISO 14091. Sekundärquelle: Umweltbundesamt, „Klimarisikoanalysen auf kommunaler Ebene – Handlungsempfehlungen zur Umsetzung der ISO 14091“, Abschnitt 2.1.2, S. 12.

Die Bestandsaufnahme rechnet nichts. Sie führt Größen auf und weist je Größe aus, woher der Wert stammt oder dass er fehlt. Sie richtet sich an Beraterinnen und Berater sowie an Sachbearbeiterinnen und Sachbearbeiter in Kommunen.

## Erhobene Größen

Das Produkt führt 22 Größen in fünf Gruppen. Je Größe steht entweder die Datenquelle (Quellschlüssel und Klartext) oder der Hinweis, dass keine Quelle je Kommune vorliegt.

| Code | Größe | Gruppe | Einheit | Quelle oder Lücke |
|---|---|---|---|---|
| aeltere_ab_65 | Ältere Menschen ab 65 Jahren | Vulnerable Personen | % | Zensus_2022 (Zensus 2022, Statistisches Bundesamt) |
| kinder_unter_18 | Kinder und Jugendliche unter 18 Jahren | Vulnerable Personen | % | Zensus_2022 (Zensus 2022, Statistisches Bundesamt) |
| arbeitslosenquote | Arbeitslose (Arbeitslosenquote) | Vulnerable Personen | % | Regionalstatistik_GENESIS (Regionaldatenbank Deutschland, GENESIS-Online) |
| pflegebeduerftige | Pflegebedürftige Menschen | Vulnerable Personen | – | Für die Größe Pflegebedürftige Menschen liegt dem Produkt keine Datenquelle je Kommune vor; sie ist im Rahmen der Konzepterstellung vor Ort zu erheben. |
| alleinlebende_aeltere | Alleinlebende ältere Menschen | Vulnerable Personen | – | Für die Größe Alleinlebende ältere Menschen liegt dem Produkt keine Datenquelle je Kommune vor; sie ist im Rahmen der Konzepterstellung vor Ort zu erheben. |
| vorerkrankte | Menschen mit Vorerkrankungen | Vulnerable Personen | – | Für die Größe Menschen mit Vorerkrankungen liegt dem Produkt keine Datenquelle je Kommune vor; sie ist im Rahmen der Konzepterstellung vor Ort zu erheben. |
| wohnungslose | Wohnungslose Menschen | Vulnerable Personen | – | Für die Größe Wohnungslose Menschen liegt dem Produkt keine Datenquelle je Kommune vor; sie ist im Rahmen der Konzepterstellung vor Ort zu erheben. |
| gewaesser | Gewässer | Natürliche Systeme | – | Für die Größe Gewässer liegt dem Produkt keine Datenquelle je Kommune vor; sie ist im Rahmen der Konzepterstellung vor Ort zu erheben. Hinweis: nicht im Katalog. |
| wald | Wald | Natürliche Systeme | – | Für die Größe Wald liegt dem Produkt keine Datenquelle je Kommune vor; sie ist im Rahmen der Konzepterstellung vor Ort zu erheben. Hinweis: nicht im Katalog. |
| boeden | Böden | Natürliche Systeme | – | Für die Größe Böden liegt dem Produkt keine Datenquelle je Kommune vor; sie ist im Rahmen der Konzepterstellung vor Ort zu erheben. Hinweis: nicht im Katalog. |
| schutzgebiete | Schutzgebiete | Natürliche Systeme | – | Für die Größe Schutzgebiete liegt dem Produkt keine Datenquelle je Kommune vor; sie ist im Rahmen der Konzepterstellung vor Ort zu erheben. Hinweis: nicht im Katalog. |
| energie | Energieinfrastruktur | Klimasensible Strukturen | Vorkommen | OSM_Data (OpenStreetMap-Daten); BBK_KRITIS (Kritische Infrastrukturen, BBK) |
| wasser_abwasser | Wasser- und Abwasserinfrastruktur | Klimasensible Strukturen | Vorkommen | OSM_Data (OpenStreetMap-Daten); BBK_KRITIS (Kritische Infrastrukturen, BBK) |
| verkehrsknoten | Verkehrsknoten | Klimasensible Strukturen | Vorkommen | OSM_Data (OpenStreetMap-Daten); BBK_KRITIS (Kritische Infrastrukturen, BBK) |
| kommunikation | Kommunikationsinfrastruktur | Klimasensible Strukturen | Vorkommen | OSM_Data (OpenStreetMap-Daten); BBK_KRITIS (Kritische Infrastrukturen, BBK) |
| krankenhaeuser | Krankenhäuser | Klimasensible Strukturen | Anzahl | OSM_Data (OpenStreetMap-Daten) |
| pflegeeinrichtungen | Pflegeeinrichtungen | Klimasensible Strukturen | Anzahl | OSM_Data (OpenStreetMap-Daten) |
| kitas_schulen | Kindertagesstätten und Schulen | Klimasensible Strukturen | – | Für die Größe Kindertagesstätten und Schulen liegt dem Produkt keine Datenquelle je Kommune vor; sie ist im Rahmen der Konzepterstellung vor Ort zu erheben. |
| lieferketten | Lieferketten | Klimasensible Strukturen | – | Für die Größe Lieferketten liegt dem Produkt keine Datenquelle je Kommune vor; sie ist im Rahmen der Konzepterstellung vor Ort zu erheben. Hinweis: nicht im Katalog. |
| starkregenereignisse | Vergangene Starkregenereignisse seit 2001 (CatRaRE) | Vergangene Ereignisse | Anzahl | DWD_CatRaRE (CatRaRE T5, Version 2026.01, Deutscher Wetterdienst) |
| schadensereignisse | Vergangene Schadensereignisse durch Wetterextreme | Vergangene Ereignisse | – | Für die Größe Vergangene Schadensereignisse durch Wetterextreme liegt dem Produkt keine Datenquelle je Kommune vor; sie ist im Rahmen der Konzepterstellung vor Ort zu erheben. |
| bevoelkerungsentwicklung | Bevölkerungsentwicklung | Trends | % | Destatis_GVISys_Bevoelkerung (Gemeindeverzeichnis GV-ISys, Destatis, Stichtage 31.12.2017 und 31.12.2023) |

Die Größe `starkregenereignisse` zählt die Ereignisse des DWD-Katalogs CatRaRE seit 2001, deren Mittelpunkt (Ort des Niederschlagsmaximums) in der Fläche der Kommune liegt; die Markdown-Fassung nennt zusätzlich das Datum des jüngsten Ereignisses. Als Fläche dient die Grenze der Kommune, ersatzweise die Hülle ihrer gespeicherten Zellen; liegt keine Fläche vor, steht der Laufzeitsatz statt eines Werts. Unter der Gruppe „Vergangene Klimarisiken“ steht die Modellgrenze des Katalogs wörtlich. Schäden trägt der Katalog nicht: `schadensereignisse` behält den Lückensatz.

## Lücken und Abgrenzung

Elf Größen haben keine Datenquelle je Kommune. Für sie zeigt das Produkt den Lückensatz aus der Tabelle, statt einen Wert zu schätzen. Ist eine sonst vorhandene Quelle für eine Kommune nicht abrufbar, weist das Produkt den Wert in der Bestandsaufnahme als fehlend aus.

Workshops und lokale Erhebungen bleiben Arbeitsschritt des Beratungsbüros. Sozioökonomische und geographische Rahmenbedingungen sowie Klimatrends liefert das Kommunenprofil (Route /{kommune_id}/profile); sie sind nicht Teil der Bestandsaufnahme.

## Vorhandene Untersuchungen

Die Markdown-Fassung der Bestandsaufnahme enthält nach den fünf Gruppen den Abschnitt „Vorhandene Untersuchungen“. Er nennt je Eintrag aus `app.data.vorhandene_untersuchungen.UNTERSUCHUNGEN` die Bezeichnung und wo die Untersuchung erhältlich ist. Für das Bundesland der Kommune stehen zusätzlich die beiden Fundorte aus `LANDESPORTALE` (Hochwassergefahren- und Hochwasserrisikokarten, Klimarisikoanalyse des Landes); darunter steht der Nachbarsatz wörtlich. Ist kein Bundesland bekannt oder ist es dem Produkt unbekannt, bleibt der Abschnitt bestehen und sagt in einem Satz, dass die Fundorte des Landes fehlen. Dafür gibt `bestandsaufnahme_fuer_kommune` zusätzlich den Schlüssel `bundesland` aus. Die Größenliste bleibt bei 22 Größen.

## Handlungsfelder

Die Markdown-Fassung der Bestandsaufnahme enthält vor den Datenlücken den Abschnitt „Handlungsfelder“. Er nennt alle 17 KAnG-Handlungsfelder aus `catalog.KANG_CLUSTERS` und weist je Feld aus, ob der Katalog dazu ein Risiko führt (`im Katalog`) oder nicht (`nicht im Katalog`); die Zuordnung der Risiken folgt `handlungsfeld_fuer_risiko`. Am Katalogstand vom 25.09.2026 führt der Katalog vier Risiken, alle im Feld Gesundheit und Pflege; die übrigen 16 Felder stehen als „nicht im Katalog“. Für die Felder im Katalog rechnet das Produkt Schäden, der KAnG-Nachweis zeigt den Stand. Ob ein Feld „nicht im Katalog“ die Kommune betrifft, schätzt sie selbst ein; das Produkt legt das nicht fest. Umgesetzt in `app.services.bestandsaufnahme_handlungsfelder.handlungsfelder_im_katalog`.
