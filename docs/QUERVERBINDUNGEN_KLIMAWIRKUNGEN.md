# Querverbindungen zwischen Klimawirkungen (KWRA 2021, Teilbericht 6, Kap. 3.4 und Kap. 7)

Analysedokument zu Quellenlage, Netzrollen und Modellgrenze der im Backend-Datenmodul
`backend/app/data/kwra_querverbindungen.py` geführten Querverbindungen. Ergänzt die dortigen
Docstrings um eine für Berater und Kommunen lesbare Fassung (Teil 3 der Reihe; Teil 1 = Datenmodul,
Teil 2 = Auswertung je Produkt-Klimawirkung und Katalog-Endpunkt).

## Quellenlage

Quelle ist ausschließlich UBA/BMU, „Klimawirkungs- und Risikoanalyse 2021 für Deutschland"
(KWRA 2021), Teilbericht 6 (Integrierte Auswertung), Kapitel 3.4 „Analyse der Querverbindungen"
(S. 82–88) sowie Kapitel 7 „Querbetrachtung der Systembereiche" (S. 146–154), Dessau-Roßlau 2021
— abgelegt unter `docs/KWAR/kwra2021_teilbericht_6_integrierte_auswertung_bf_211027_0.pdf`.

Teilbericht 6 benennt für das KWRA-Wirkungsnetz in Kapitel 3.4 (Kernaussagen S. 88) **257
Querverbindungen** zwischen den 102 Klimawirkungen insgesamt (im Durchschnitt rund 2,5 ein- oder
ausgehende Beziehungen je Klimawirkung). Eine vollständige Liste aller 257 Einzelkanten
veröffentlicht der Teilbericht jedoch in keinem der sechs Teilberichte: Abbildung 8 (S. 83) zeigt
das Netz nur als Chord-Diagramm auf Handlungsfeldebene, aus dem sich keine exakten Kanten ablesen
lassen. Aus Kapitel 3.4 belegt sind deshalb nur zwei Ausschnitte, die dieses Dokument und das
zugrunde liegende Datenmodul wörtlich übernehmen:

1. die **Netzrollen** — 25 Klimawirkungen, die Kap. 3.4 (S. 82–88) ausdrücklich als starke Sender
   oder starke Empfänger im Wirkungsnetz benennt (Abschnitt „Netzrollen");
2. die im Fließtext von Kap. 3.4 (S. 82–88) **wörtlich genannten Einzelbeziehungen** (Auszug,
   20 Einträge, Abschnitt „Benannte Einzelbeziehungen").

Zusätzlich belegt **Tabelle 28** in **Kapitel 7** „Querbetrachtung der Systembereiche" (S. 153) die
Querverbindungen auf der Ebene der fünf Systembereiche (Abschnitt „Querverbindungen zwischen den
Systembereichen") — diese Tabelle steht damit außerhalb von Kap. 3.4, in einem eigenen späteren
Kapitel des Teilberichts. Übertragen wurde die kuratierte Arbeitsmappe
`docs/KWAR/KWRA-2021_Klimawirkungen.xlsx`, Blätter „Klimawirkungen"
(Spalte „Netzrolle (TB 6 Kap. 3.4)") und „Wirkbeziehungen".

## Netzrollen

Die 25 Klimawirkungen, die Teilbericht 6 Kap. 3.4 „Analyse der Querverbindungen" (S. 82–88)
ausdrücklich als starke Sender („stark ausgehend") oder starke Empfänger („stark eingehend") im
Wirkungsnetz benennt (`app.data.kwra_querverbindungen.NETZROLLEN`).

| KWRA-ID | Klimawirkung | Handlungsfeld | Rolle |
|---|---|---|---|
| 1 | Veränderung der Länge der Vegetationsperiode und Phänologie | Biologische Vielfalt | stark ausgehend |
| 4 | Verschiebung von Arealen und Rückgang der Bestände | Biologische Vielfalt | stark ausgehend |
| 5 | Schäden an Küstenökosystemen | Biologische Vielfalt | stark eingehend |
| 12 | Rutschungen und Muren | Boden | stark ausgehend |
| 13 | Wassermangel im Boden | Boden | stark ausgehend |
| 14 | Sickerwasser | Boden | stark ausgehend |
| 15 | Vernässung | Boden | stark ausgehend |
| 25 | Ertragsausfälle | Landwirtschaft | stark eingehend |
| 26 | Qualität der Ernteprodukte | Landwirtschaft | stark eingehend |
| 31 | Nutzfunktion: Holzertrag | Wald- und Forstwirtschaft | stark eingehend |
| 38 | Meerestemperatur und Eisbedeckung | Küsten- und Meeresschutz | stark ausgehend |
| 39 | Wasserqualität und Grundwasserversalzung | Küsten- und Meeresschutz | stark ausgehend |
| 40 | Meeresspiegelhöhe | Küsten- und Meeresschutz | stark ausgehend |
| 43 | Sturmfluten | Küsten- und Meeresschutz | stark ausgehend |
| 48 | Niedrigwasser | Wasserhaushalt, Wasserwirtschaft | stark ausgehend |
| 49 | Hochwasser | Wasserhaushalt, Wasserwirtschaft | stark ausgehend |
| 53 | Gewässertemperatur und Eisbedeckung und biologische Wasserqualität | Wasserhaushalt, Wasserwirtschaft | stark ausgehend |
| 55 | Grundwasserstand und Grundwasserqualität | Wasserhaushalt, Wasserwirtschaft | stark eingehend |
| 73 | Schiffbarkeit der Seeschifffahrtsstraßen | Verkehr, Verkehrsinfrastruktur | stark eingehend |
| 82 | Beeinträchtigung des Warenverkehrs über Wasserstraßen (Inland) | Industrie und Gewerbe | stark eingehend |
| 92 | Schäden an touristischen Infrastrukturen und Betriebsunterbrechungen | Tourismuswirtschaft | stark eingehend |
| 95 | Hitzebelastung | Menschliche Gesundheit | stark eingehend |
| 96 | Allergische Reaktionen durch Aeroallergene pflanzlicher Herkunft | Menschliche Gesundheit | stark eingehend |
| 97 | Potenziell schädliche Mikroorganismen und Algen | Menschliche Gesundheit | stark eingehend |
| 101 | Verletzungen und Todesfälle infolge von Extremereignissen | Menschliche Gesundheit | stark eingehend |

13 Klimawirkungen sind stark ausgehend (Sender), 12 stark eingehend (Empfänger). Küsten- und
Meeresschutz hat ausschließlich ausgehende Netzrollen, Tourismuswirtschaft (über die benannten
Einzelbeziehungen, siehe unten) ausschließlich eingehende.

## Benannte Einzelbeziehungen

Im Fließtext von Teilbericht 6 Kap. 3.4 „Analyse der Querverbindungen" (S. 82–88) wörtlich genannte
Einzelbeziehungen (Auszug, nicht vollständig — `app.data.kwra_querverbindungen.BENANNTE_BEZIEHUNGEN`). Acht Beziehungen liegen auf
Ebene einzelner Klimawirkungen, sieben auf gemischter Ebene (ein oder beide Enden ein
Handlungsfeld mit mehreren Klimawirkungen) und fünf zwischen ganzen Handlungsfeldern.

| Quelle | Ziel | Ebene | Beleg |
|---|---|---|---|
| Hochwasser | zahlreiche Klimawirkungen in mehreren Handlungsfeldern | Klimawirkung | TB6 Kap. 3.4: zentrale Klimawirkung, wirkt sich auf die meisten anderen aus |
| Gewässertemperatur und Eisbedeckung und biologische Wasserqualität | Potenziell schädliche Mikroorganismen und Algen | Klimawirkung | TB6 Kap. 3.4: fördert deren Entwicklung |
| Stadtklima / Wärmeinseln | Hitzebelastung | Klimawirkung | TB6 Kap. 3.4: zunehmender urbaner Wärmeinseleffekt erhöht die Hitzebelastung |
| Veränderung der Länge der Vegetationsperiode und Phänologie | Allergische Reaktionen durch Aeroallergene pflanzlicher Herkunft | Klimawirkung | TB6 Kap. 3.4: verlängerte Vegetationsperiode verstärkt Pollenreaktionen |
| Hochwasser | Verletzungen und Todesfälle infolge von Extremereignissen | Klimawirkung | TB6 Kap. 3.4 |
| Sturzfluten (Versagen von Entwässerungseinrichtungen und Überflutungsschutzsystemen) | Verletzungen und Todesfälle infolge von Extremereignissen | Klimawirkung | TB6 Kap. 3.4 |
| Niedrigwasser | Beeinträchtigung des Warenverkehrs über Wasserstraßen (Inland) | Klimawirkung | TB6 Kap. 3.4: niedrigwasserbedingte Einschränkungen im Warentransport |
| Hochwasser | Schäden / Hindernisse bei Straßen und Schienenwegen (Hochwasser) | Klimawirkung | TB6 Kap. 3.4: Beeinträchtigung der Verkehrswege |
| Boden (Handlungsfeld) | Grundwasserstand und Grundwasserqualität | gemischt | TB6 Kap. 3.4: viele Klimawirkungen des Bodens wirken hierauf ein |
| Boden und Biologische Vielfalt (Handlungsfelder) | Ertragsausfälle | gemischt | TB6 Kap. 3.4: landwirtschaftliche Ertragsausfälle werden von vielen Klimawirkungen dieser Handlungsfelder beeinflusst |
| Boden und Biologische Vielfalt (Handlungsfelder) | Qualität der Ernteprodukte | gemischt | TB6 Kap. 3.4 |
| Boden und Biologische Vielfalt (Handlungsfelder) | Nutzfunktion: Holzertrag | gemischt | TB6 Kap. 3.4: weitere Auswirkungen auf Holzerträge in der Forstwirtschaft |
| Küsten- und Meeresschutz (Handlungsfeld) | Schiffbarkeit der Seeschifffahrtsstraßen | gemischt | TB6 Kap. 3.4 |
| Küsten- und Meeresschutz (Handlungsfeld) | Schäden an touristischen Infrastrukturen und Betriebsunterbrechungen | gemischt | TB6 Kap. 3.4 |
| Küsten- und Meeresschutz (Handlungsfeld) | Schäden an Küstenökosystemen | gemischt | TB6 Kap. 3.4 |
| Wasserhaushalt, Wasserwirtschaft (Handlungsfeld) | Industrie und Gewerbe (Handlungsfeld) | Handlungsfeld | TB6 Kap. 3.4: Einschränkungen der Wasserversorgung treffen die Produktion |
| Energiewirtschaft (Handlungsfeld) | Industrie und Gewerbe (Handlungsfeld) | Handlungsfeld | TB6 Kap. 3.4: Einschränkungen der Energieversorgung treffen die Produktion |
| Küsten- und Meeresschutz (Handlungsfeld) | Tourismuswirtschaft (Handlungsfeld) | Handlungsfeld | TB6 Kap. 3.4: viele eingehende Wirkungen beim Tourismus |
| Biologische Vielfalt (Handlungsfeld) | Tourismuswirtschaft (Handlungsfeld) | Handlungsfeld | TB6 Kap. 3.4 |
| Wasserhaushalt, Wasserwirtschaft (Handlungsfeld) | Tourismuswirtschaft (Handlungsfeld) | Handlungsfeld | TB6 Kap. 3.4 |

## Querverbindungen zwischen den Systembereichen

Tabelle 28 aus Teilbericht 6, Kapitel 7 „Querbetrachtung der Systembereiche" (S. 153) — und damit
außerhalb von Kap. 3.4, in einem eigenen späteren Kapitel des Teilberichts — fasst die
Querverbindungen auf Ebene der fünf Systembereiche zusammen
(`app.data.kwra_querverbindungen.SYSTEMBEREICH_MATRIX`). Rein vorgelagerte Klimawirkungen sind
darin nicht enthalten; die Diagonale zählt Wirkbeziehungen innerhalb desselben Systembereichs,
„Summe ausgehend" nur die Beziehungen zu den vier anderen Systembereichen.

| Systembereich (Quelle) | Natürliche Systeme und Ressourcen | Naturnutzende Wirtschaftssysteme | Infrastrukturen und Gebäude | Naturferne Wirtschaftssysteme | Menschen und soziale Systeme | Summe ausgehend |
|---|---|---|---|---|---|---|
| Natürliche Systeme und Ressourcen | 24 | 50 | 13 | 9 | 8 | 80 |
| Naturnutzende Wirtschaftssysteme | 6 | 44 | 13 | 8 | 8 | 35 |
| Infrastrukturen und Gebäude | 3 | 3 | 26 | 13 | 11 | 30 |
| Naturferne Wirtschaftssysteme | 0 | 0 | 0 | 5 | 0 | 0 |
| Menschen und soziale Systeme | 0 | 4 | 1 | 7 | 6 | 12 |

Naturferne Wirtschaftssysteme haben nach dieser Tabelle keine ausgehenden Wirkungen auf einen
anderen Systembereich; Natürliche Systeme und Ressourcen sind mit 80 ausgehenden Beziehungen der
stärkste Sender.

## Anwendung auf den Produktkatalog

Die Netzrollen und benannten Einzelbeziehungen zeigen, welche Klimawirkungen im Produktkatalog
(Steckbriefe je Klimawirkung, siehe `docs/methodik/`) besonders viele Folgewirkungen auf andere
Steckbriefe haben (starke Sender, z. B. Hochwasser, Wassermangel im Boden) oder besonders viele
Ursachen aus anderen Steckbriefen bündeln (starke Empfänger, z. B. Hitzebelastung, Ertragsausfälle).
Das ist ein Lesehinweis für Berater und Kommunen: Wer an einem Steckbrief mit starker Netzrolle
etwas ändert (z. B. eine Maßnahme gegen Hochwasser), sollte die benannten Folgewirkungen auf andere
Steckbriefe mitdenken, auch wenn der Katalog jeden Steckbrief einzeln rechnet. Teil 2 dieser Reihe
(Auswertung je Produkt-Klimawirkung, Katalog-Endpunkt) macht diese Zuordnung im Produkt
nachschlagbar; dieses Dokument liefert dazu die Quellenlage und die Begründung, warum die Liste
kein vollständiges Kantenverzeichnis ist.

## Modellgrenze

- Die 257 Querverbindungen aus Teilbericht 6 sind eine **Gesamtzahl**, keine Kantenliste. Nur 25
  Netzrollen und 20 im Fließtext benannte Einzelbeziehungen sind wörtlich belegt; die übrigen
  Kanten des Netzes sind aus dem Teilbericht nicht rekonstruierbar (Chord-Diagramm ohne
  Achsenbeschriftung auf Klimawirkungsebene).
- Eine vollständige Kantenliste aller 257 Querverbindungen wäre keine KWRA-Angabe, sondern eine
  eigenständige Modellierung, die als solche ausgewiesen werden müsste (Vorgabe P1/P2) — sie ist
  nicht Gegenstand dieses Dokuments und des zugrunde liegenden Datenmoduls.
- Von den 20 benannten Einzelbeziehungen sind 7 auf gemischter Ebene und 5 auf Handlungsfeldebene
  formuliert; sie lassen sich nicht auf eine einzelne Klimawirkung als Quelle oder Ziel verengen,
  ohne den Wortlaut der KWRA zu überstimmen (`quelle_kwra_id`/`ziel_kwra_id` sind dort bewusst auf
  `None` gesetzt).
- Die Systembereichs-Matrix (Tabelle 28, Kap. 7, S. 153) zählt Beziehungen zwischen Systembereichen,
  nicht zwischen einzelnen Klimawirkungen; ein Rückschluss von der Matrix auf einzelne
  Steckbrief-Paare ist nicht möglich. Sie stammt aus einem eigenen, späteren Kapitel des
  Teilberichts (Kap. 7 „Querbetrachtung der Systembereiche") und nicht aus Kap. 3.4 — beide
  Kapitel werden hier bewusst getrennt referenziert, damit die Herkunft jeder Tabelle eindeutig
  bleibt.
- Alle Angaben stammen ausschließlich aus Teilbericht 6 der KWRA 2021 (Bezugsjahr 2021):
  Netzrollen und benannte Einzelbeziehungen aus Kapitel 3.4 „Analyse der Querverbindungen"
  (S. 82–88, Abbildung 8 auf S. 83, Kernaussagen S. 88), die Systembereichs-Matrix aus Kapitel 7
  „Querbetrachtung der Systembereiche" (Tabelle 28, S. 153); eine Aktualisierung des
  Wirkungsnetzes durch neuere KWRA-Ausgaben ist nicht Teil dieses Dokuments.
