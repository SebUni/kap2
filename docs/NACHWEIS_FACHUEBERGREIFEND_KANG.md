# Nachweis der fachübergreifenden und integrierten Berücksichtigung (§ 8 Abs. 1 KAnG)

Dieses Dokument beschreibt Methode und Grenzen des Nachweises nach § 8 Abs. 1 KAnG
(Ticket T-0464, Teil 4 des Nachweises, Vorhaben T-0445). Es ergänzt die Berechnung
(`app.services.kang_beruecksichtigung.nachweis_fachuebergreifend`, Teil 2) und die
Markdown-Ausgabe (`app.services.kang_nachweis_markdown`, Teil 3) um die
nutzersichtbare Erklärung, was das Produkt prüft, was es nicht prüft, und wo die
Verantwortung des Trägers öffentlicher Aufgaben beginnt.

## Rechtsgrundlage und Adressat

§ 8 Abs. 1 KAnG (Berücksichtigungsgebot), abrufbar unter
https://www.gesetze-im-internet.de/kang/__8.html, lautet im Wortlaut: „Die Träger
öffentlicher Aufgaben haben bei ihren Planungen und Entscheidungen das Ziel der
Klimaanpassung nach § 1 fachübergreifend und integriert zu berücksichtigen.“
Adressat der Vorschrift ist der Träger öffentlicher Aufgaben, nicht das Produkt:
Das Produkt liefert keine Rechtsauskunft und keinen Bescheid, sondern eine
Arbeitshilfe, mit der ein Träger öffentlicher Aufgaben — etwa eine Kommune oder ein
für sie tätiges Beratungshaus — die eigene Planung gegen das Berücksichtigungsgebot
gegenprüfen kann.

## Was das Produkt prüft

Für jedes der 17 KAnG-Handlungsfelder stellt das Produkt gegenüber:

- welche Risiken der Planung diesem Handlungsfeld zugeordnet sind und dort eine
  jährliche Schadenssumme größer null verursachen,
- welche Maßnahmen der Planung diesem Handlungsfeld zugeordnet sind.

Daraus ergibt sich je Handlungsfeld einer von drei Zuständen: 'nicht betroffen'
(kein zugeordnetes Risiko mit Schaden), 'offen' (betroffen, aber keine zugeordnete
Maßnahme) oder 'berücksichtigt' (betroffen und mindestens eine zugeordnete
Maßnahme). Maßnahmen, deren verknüpfte Risiken auf mehr als ein Handlungsfeld
führen, werden gesondert als integrierend ausgewiesen — das ist der Beitrag des
Nachweises zum 'integriert'-Teil der Vorschrift. Geprüft wird damit die
Vollständigkeit der Planung gegenüber dem im Produkt hinterlegten Risiko- und
Maßnahmenkatalog: Ist jedes betroffene Handlungsfeld durch mindestens eine
Maßnahme der Planung adressiert?

## Was dem Träger öffentlicher Aufgaben überlassen bleibt

Diese Nachweisrechnung stellt den nach § 8 Abs. 1 KAnG geforderten fachübergreifenden und integrierten Blick als Gegenüberstellung dar: je KAnG-Handlungsfeld die zugeordneten Risiken mit ihrer jährlichen Schadenssumme und die dort ansetzenden Maßnahmen der Planung. Sie richtet sich an Träger öffentlicher Aufgaben als Arbeitshilfe für die eigene Abwägung und bescheinigt keine Rechtskonformität: Ob die Belange der Klimaanpassung im Sinne des § 8 Abs. 1 KAnG berücksichtigt worden sind, entscheidet der Träger in eigener Verantwortung. Geprüft wird allein die Vollständigkeit gegenüber dem hinterlegten Risiko- und Maßnahmenkatalog; Risiken, Maßnahmen oder Belange außerhalb dieses Katalogs bleiben unberücksichtigt, und ein Feld ohne Schaden im Modell ('nicht betroffen') kann in der Sache dennoch betroffen sein.

Insbesondere bleibt dem Träger öffentlicher Aufgaben überlassen: die inhaltliche
Angemessenheit einer Maßnahme für das jeweilige Handlungsfeld (das Produkt prüft
nur, ob überhaupt eine Maßnahme zugeordnet ist, nicht ob sie ausreicht), die
Einordnung von Risiken und Maßnahmen, die im Katalog des Produkts nicht enthalten
sind, sowie die abschließende rechtliche Bewertung, ob damit das
Berücksichtigungsgebot des § 8 Abs. 1 KAnG erfüllt ist.

## Felder des Nachweises

Je Feld des Rückgabewertes von `nachweis_fachuebergreifend` steht hier, wofür es
steht und woher es kommt. `handlungsfelder`, `zusammenfassung` und `abgrenzung`
sind die drei Schlüssel der obersten Ebene; `cluster` bis `massnahmen` sind die
Schlüssel eines Eintrags aus `handlungsfelder`; `betroffen_n` bis
`integrierende_massnahmen` sind die Schlüssel von `zusammenfassung`.

| Feld | Bedeutung |
| --- | --- |
| `handlungsfelder` | Liste aller Cluster-/Feld-Paare in Katalogreihenfolge, je Eintrag mit Status, Risiken, Schaden und Maßnahmen. |
| `zusammenfassung` | Verdichtete Kennzahlen über alle betroffenen Handlungsfelder. |
| `abgrenzung` | Wortlaut der Einschränkung, was der Nachweis leistet und was nicht (siehe Modellgrenze). |
| `cluster` | Code des KAnG-Clusters, dem das Handlungsfeld zugeordnet ist. |
| `feld` | Code des KAnG-Handlungsfelds innerhalb des Clusters. |
| `status` | 'berücksichtigt', 'offen' oder 'nicht betroffen'. |
| `risiken` | Risikocodes, die diesem Handlungsfeld zugeordnet sind und einen Schaden größer null verursachen. |
| `schaden_eur` | Summe der jährlichen Schäden der zugeordneten Risiken in Euro. |
| `massnahmen` | Maßnahmencodes der Planung, die diesem Handlungsfeld zugeordnet sind. |
| `betroffen_n` | Anzahl der Handlungsfelder mit Status ungleich 'nicht betroffen'. |
| `beruecksichtigt_n` | Anzahl der betroffenen Handlungsfelder mit Status 'berücksichtigt'. |
| `offen_n` | Anzahl der betroffenen Handlungsfelder mit Status 'offen'. |
| `offene_handlungsfelder` | Cluster-/Feld-Paare der Handlungsfelder mit Status 'offen'. |
| `integrierende_massnahmen` | Maßnahmencodes, deren verknüpfte Risiken auf mehr als ein Handlungsfeld führen. |

## Modellgrenze

Der Nachweis ist eine Vollständigkeitsprüfung gegen den im Produkt hinterlegten
Risiko- und Maßnahmenkatalog, keine Rechtsauskunft und kein Wirksamkeitsnachweis:
Ein 'berücksichtigt' bedeutet nur, dass mindestens eine Maßnahme der Planung dem
betroffenen Handlungsfeld zugeordnet ist — nicht, dass diese Maßnahme ausreicht,
den Schaden abzuwenden oder rechtlich hinreichend ist. Ein 'nicht betroffen' im
Modell schließt eine tatsächliche Betroffenheit außerhalb des Katalogs nicht aus.
Wortlaut siehe Abschnitt „Was dem Träger öffentlicher Aufgaben überlassen bleibt“,
identisch mit `ABGRENZUNG` in `app.services.kang_beruecksichtigung`, damit
Dokument und Code nicht auseinanderlaufen.
