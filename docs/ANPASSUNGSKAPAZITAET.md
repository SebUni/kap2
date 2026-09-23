# Anpassungskapazität nach Komponenten und Reifegraden

Dieses Dokument beschreibt Methode und Grenzen der optionalen Analyse der
Anpassungskapazität (Konformitätszeile 18, Vorhaben T-0448, Teil D). Es ergänzt die
Berechnung (`app.services.anpassungskapazitaet.bewerte_anpassungskapazitaet`) und die
Markdown-Ausgabe (`app.services.anpassungskapazitaet_markdown.anpassungskapazitaet_als_markdown`)
um die nutzersichtbare Erklärung. Es richtet sich an Berater und Sachbearbeiter einer
Kommune, fachkundig, aber ohne Statistikausbildung.

## Zweck

Die Analyse der Anpassungskapazität ist nach ISO 14091 ein optionaler Analyseschritt; sie ergänzt die Bewertung des Klimarisikos ohne (weitere) Anpassung und ersetzt sie nicht.

Das Produkt kann die Anpassungskapazität einer Kommune nicht messen. Die Kommune oder
das Beratungshaus stuft deshalb jede der vier Komponenten selbst ein. Das Produkt fasst
die Einstufung mit einer lesbaren Regel zusammen und leitet daraus in Worten ab, wie
stark sich das Klimarisiko verringern lässt.

## Komponenten

Die Reihenfolge ist verbindlich.

| Code | Bezeichnung | Beschreibung |
|---|---|---|
| organisation | Organisationsbezogene Fähigkeit | Zuständigkeiten, Personal, Fachwissen und Abstimmungswege, mit denen die Kommune Anpassung planen und umsetzen kann. |
| technik | Technisches Vermögen | Technische Infrastruktur, Daten sowie Warn- und Informationssysteme, die für Anpassung zur Verfügung stehen. |
| finanzen | Finanzielle Fähigkeit | Haushaltsmittel und Zugang zu Fördermitteln, mit denen Anpassungsmaßnahmen finanziert werden können. |
| oekosystem | Fähigkeit des Ökosystems | Natürliche Puffer- und Regulationsleistungen (z. B. Grünflächen, Gewässer, Böden), die Klimawirkungen abmildern. |

## Reifegradskala

| Stufe | Bezeichnung | Beschreibung |
|---|---|---|
| 0 | nicht vorhanden | Die Fähigkeit fehlt oder wird für Klimaanpassung nicht genutzt. |
| 1 | im Aufbau | Erste Ansätze sind vorhanden, aber nicht verbindlich verankert oder für die bekannten Klimarisiken nicht ausreichend. |
| 2 | etabliert | Die Fähigkeit ist verbindlich verankert und reicht für die heute bekannten Klimarisiken aus. |
| 3 | vorausschauend | Die Fähigkeit wird regelmäßig überprüft und an die künftig erwarteten Klimaänderungen angepasst. |

## Gesamtstufe und Ableitung der Risikominderung

Engpassregel: Die Gesamtstufe ist die niedrigste Stufe der vier Komponenten, weil die schwächste Fähigkeit begrenzt, wie viel Anpassung tatsächlich umgesetzt werden kann.

Aus der Gesamtstufe folgt in Worten, wie stark sich das Klimarisiko verringern lässt:

| Gesamtstufe | Aussage |
|---|---|
| 0 | Mit der vorhandenen Anpassungskapazität lässt sich das Klimarisiko voraussichtlich kaum verringern. |
| 1 | Mit der vorhandenen Anpassungskapazität lässt sich das Klimarisiko voraussichtlich nur in geringem Umfang verringern. |
| 2 | Mit der vorhandenen Anpassungskapazität lässt sich das Klimarisiko voraussichtlich teilweise verringern. |
| 3 | Mit der vorhandenen Anpassungskapazität lässt sich das Klimarisiko voraussichtlich weitgehend verringern. |
| nicht bewertet | Die Anpassungskapazität ist nicht für alle vier Komponenten bewertet; eine Aussage, wie stark sich das Klimarisiko durch Anpassung verringern lässt, unterbleibt. |

Rechenbeispiel: organisation 2, technik 3, finanzen 1, oekosystem 2 → Gesamtstufe 1 (im Aufbau), Engpass finanzen.
Mit der vorhandenen Anpassungskapazität lässt sich das Klimarisiko voraussichtlich nur in geringem Umfang verringern.

Die Stärke der Technik hilft hier nicht weiter: Solange die finanzielle Fähigkeit im
Aufbau ist, lässt sich nicht mehr umsetzen, als das Geld erlaubt.

## Quellen und Abschätzung

Quelle der Komponenten: Umweltbundesamt (2022): Klimarisikoanalysen auf kommunaler Ebene – Handlungsempfehlungen zur Umsetzung der ISO 14091, Abschnitt 2.2.5, S. 28f.; ISO 14091:2021, Anhang G und H.

Herleitung der Skala: Abschätzung von KAP3: Die vierstufige Skala ist eine Festlegung von KAP3, angelehnt an die in der Quelle genannten Reifegrade; sie ordnet nur und ist kein Messwert. Vier Stufen erlauben einer Kommune, jede Komponente ohne Statistikkenntnisse in einem Schritt einzuordnen.

Die Engpassregel und die Aussagen zur Risikominderung sind ebenfalls Festlegungen von KAP3
und keine publizierten Werte.

## Grenzen

- Es ist eine Selbsteinschätzung und keine Messung: Das Ergebnis ist nur so belastbar wie die Einstufung, die die Kommune oder das Beratungshaus vornimmt.
- Es gibt bewusst keinen Prozentsatz der Minderung. Eine solche Zahl wäre ein unbelegter Parameter (P1), eine Verteilungsfunktion wäre überkomplex (A-0034).
- Der Schritt ersetzt die Bewertung des Klimarisikos ohne (weitere) Anpassung nicht; er ergänzt sie nur.
- Ist nicht jede der vier Komponenten bewertet, unterbleibt jede Aussage zur Risikominderung.
