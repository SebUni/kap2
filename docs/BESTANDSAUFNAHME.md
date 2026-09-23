# Bestandsaufnahme

## Zweck und Einordnung

Die Bestandsaufnahme ist der Risikoberechnung vorgeschaltet. Sie stellt zusammen, was über eine Kommune bereits bekannt ist: welche Bevölkerungsgruppen besonders verletzlich sind, welche klimasensiblen Einrichtungen und Infrastrukturen es gibt und welche Schadensereignisse durch Wetterextreme bereits eingetreten sind. Damit folgt das Produkt der Bestandsaufnahme als vorgeschalteter Phase der Klimarisikoanalyse nach ISO 14091. Sekundärquelle: Umweltbundesamt, „Klimarisikoanalysen auf kommunaler Ebene – Handlungsempfehlungen zur Umsetzung der ISO 14091“, Abschnitt 2.1.2, S. 12.

Die Bestandsaufnahme rechnet nichts. Sie führt Größen auf und weist je Größe aus, woher der Wert stammt oder dass er fehlt. Sie richtet sich an Beraterinnen und Berater sowie an Sachbearbeiterinnen und Sachbearbeiter in Kommunen.

## Erhobene Größen

Das Produkt führt 15 Größen in drei Gruppen. Je Größe steht entweder die Datenquelle (Quellschlüssel und Klartext) oder der Hinweis, dass keine Quelle je Kommune vorliegt.

| Code | Größe | Gruppe | Einheit | Quelle oder Lücke |
|---|---|---|---|---|
| aeltere_ab_65 | Ältere Menschen ab 65 Jahren | Vulnerable Personen | % | Zensus_2022 (Zensus 2022, Statistisches Bundesamt) |
| kinder_unter_18 | Kinder und Jugendliche unter 18 Jahren | Vulnerable Personen | % | Zensus_2022 (Zensus 2022, Statistisches Bundesamt) |
| arbeitslosenquote | Arbeitslose (Arbeitslosenquote) | Vulnerable Personen | % | Regionalstatistik_GENESIS (Regionaldatenbank Deutschland, GENESIS-Online) |
| pflegebeduerftige | Pflegebedürftige Menschen | Vulnerable Personen | – | Für die Größe Pflegebedürftige Menschen liegt dem Produkt keine Datenquelle je Kommune vor; sie ist im Rahmen der Konzepterstellung vor Ort zu erheben. |
| alleinlebende_aeltere | Alleinlebende ältere Menschen | Vulnerable Personen | – | Für die Größe Alleinlebende ältere Menschen liegt dem Produkt keine Datenquelle je Kommune vor; sie ist im Rahmen der Konzepterstellung vor Ort zu erheben. |
| vorerkrankte | Menschen mit Vorerkrankungen | Vulnerable Personen | – | Für die Größe Menschen mit Vorerkrankungen liegt dem Produkt keine Datenquelle je Kommune vor; sie ist im Rahmen der Konzepterstellung vor Ort zu erheben. |
| wohnungslose | Wohnungslose Menschen | Vulnerable Personen | – | Für die Größe Wohnungslose Menschen liegt dem Produkt keine Datenquelle je Kommune vor; sie ist im Rahmen der Konzepterstellung vor Ort zu erheben. |
| energie | Energieinfrastruktur | Klimasensible Strukturen | Vorkommen | OSM_Data (OpenStreetMap-Daten); BBK_KRITIS (Kritische Infrastrukturen, BBK) |
| wasser_abwasser | Wasser- und Abwasserinfrastruktur | Klimasensible Strukturen | Vorkommen | OSM_Data (OpenStreetMap-Daten); BBK_KRITIS (Kritische Infrastrukturen, BBK) |
| verkehrsknoten | Verkehrsknoten | Klimasensible Strukturen | Vorkommen | OSM_Data (OpenStreetMap-Daten); BBK_KRITIS (Kritische Infrastrukturen, BBK) |
| kommunikation | Kommunikationsinfrastruktur | Klimasensible Strukturen | Vorkommen | OSM_Data (OpenStreetMap-Daten); BBK_KRITIS (Kritische Infrastrukturen, BBK) |
| krankenhaeuser | Krankenhäuser | Klimasensible Strukturen | Anzahl | OSM_Data (OpenStreetMap-Daten) |
| pflegeeinrichtungen | Pflegeeinrichtungen | Klimasensible Strukturen | Anzahl | OSM_Data (OpenStreetMap-Daten) |
| kitas_schulen | Kindertagesstätten und Schulen | Klimasensible Strukturen | – | Für die Größe Kindertagesstätten und Schulen liegt dem Produkt keine Datenquelle je Kommune vor; sie ist im Rahmen der Konzepterstellung vor Ort zu erheben. |
| schadensereignisse | Vergangene Schadensereignisse durch Wetterextreme | Vergangene Ereignisse | – | Für die Größe Vergangene Schadensereignisse durch Wetterextreme liegt dem Produkt keine Datenquelle je Kommune vor; sie ist im Rahmen der Konzepterstellung vor Ort zu erheben. |

## Lücken und Abgrenzung

Sechs Größen haben keine Datenquelle je Kommune. Für sie zeigt das Produkt den Lückensatz aus der Tabelle, statt einen Wert zu schätzen. Ist eine sonst vorhandene Quelle für eine Kommune nicht abrufbar, weist das Produkt den Wert in der Bestandsaufnahme als fehlend aus.

Workshops und lokale Erhebungen bleiben Arbeitsschritt des Beratungsbüros. Sozioökonomische und geographische Rahmenbedingungen sowie Klimatrends liefert das Kommunenprofil (Route /{kommune_id}/profile); sie sind nicht Teil der Bestandsaufnahme.
