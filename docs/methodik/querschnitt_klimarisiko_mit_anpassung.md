# Querschnitt: Klimarisiko mit Anpassung

Querschnittsdatei der Methodik, gültig für alle 102 Klimawirkungen der KWRA 2021. Frage: Wie stark senkt die
Anpassungskapazität einer Kommune die Einstufung einer Klimawirkung, und woher stammen die Reifegrade? Werte bekommen die
drei Klimawirkungen von M0 (A-0048; Vorhaben T-1122-cmo): #95 Hitzebelastung in Schritt 1 (Ticket
T-1895-methodik_manager), #96 Aeroallergene und #98 UV-Schädigungen in Schritt 3 (Ticket T-1897-methodik_manager),
zusammengefasst unter „Ergebnis für M0“. Die
Regel ergibt eine Stufe, keinen Euro-Betrag. Schritt 2 (Ticket T-1896-methodik_manager) legt im Abschnitt
„Anpassungspotenzial und Doppelzählung“ fest, was das Anpassungspotenzial ist und wie Stufe, Anpassungspotenzial und
der Euro-Betrag der Maßnahmen aufeinander wirken.

Abkürzungen: **Broschüre** = Umweltbundesamt (Porst, Voß, Kahlenborn, Schauser): „Klimarisikoanalysen auf kommunaler
Ebene – Handlungsempfehlungen zur Umsetzung der ISO 14091“, Juni 2022 (PDF-Seite = gedruckte Seite); **KWRA** =
Klimawirkungs- und Risikoanalyse 2021 für Deutschland; **TB6** = deren Teilbericht 6 „Integrierte Auswertung“;
**Mappe** = `docs/KWAR/KWRA-2021_Klimawirkungen.xlsx`, Blatt „Klimawirkungen“ (Excel-Zeile 1 Gruppen, Zeile 2 Köpfe,
Zeilen 3–104 die 102 Klimawirkungen; #95 steht in Zeile 97, #96 in Zeile 98, #98 in Zeile 100).

## Festlegung

**Regel A (Klimarisiko mit Anpassung).** Für jede Klimawirkung gilt die Matrix der Broschüre, Tabelle 5 (S. 29):
„Klimarisiko mit Anpassung = Klimarisiko ohne Anpassung – Anpassungskapazität“. Eingang ist die Stufe der KWRA ohne
Anpassung für die Gegenwart (Mappe, Spalte N). Davon geht die Wirksamkeit der Anpassung ab. Sie folgt aus der Summe der
vier Reifegrade, die die Kommune für diese Klimawirkung einstuft, und wird nach unten durch die Wirksamkeit der
beschlossenen Maßnahmen der KWRA (Spalte W, 2020–2030) und nach oben durch die Wirksamkeit der weiterreichenden
Anpassung der KWRA (höherer Wert aus Spalte Z und AA, Mitte des Jahrhunderts 2031–2060) begrenzt. Summentabelle und
Rahmen sind Festlegungen von KAP3; die Werte des Rahmens stammen aus der Mappe. Das Ergebnis ist eine Stufe auf der
Skala von Tabelle 5; Werte unter 1 heißen „gering“.

Grundlage ist Abschnitt 2.2.5 der Broschüre (S. 28–29): „Aus der Kombination der Bewertung der Klimarisiken ohne
weitere Anpassung und der Anpassungskapazität kann die Höhe der Klimarisiken mit Anpassung abgeleitet werden (siehe
Tabelle 5).“ (S. 29). Die Fußnote zu Tabelle 5 legt die Werte fest: Wirksamkeit „0 (gering), 0,5 (gering-mittel), 1
(mittel), 1,5 (mittel-hoch), 2 (hoch)“, Klimarisiko „von 1 (gering) über 2 (mittel) bis 3 (hoch)“ (S. 29). Die Regel
übernimmt den Vorschlag des CEO (T-1071-ceo, Punkt 6: Verknüpfung nach Tabelle 5, qualitativ, ohne Euro-Betrag, mit
Seite) im Kern und ergänzt ihn um die Abbildung der Reifegrade und die beiden Grenzen aus der KWRA.

**Tabelle 5 der Broschüre (S. 29), wiedergegeben.** Zeile = Klimarisiko ohne Anpassung, Spalte = Wirksamkeit.

| ohne Anpassung | Hoch (2) | Mittel-hoch (1,5) | Mittel (1) | Gering-mittel (0,5) | Gering (0) |
|---|---|---|---|---|---|
| Gering (1) | 0 | 0 | 0 | 0,5 | 1 |
| Mittel (2) | 0 | 0,5 | 1 | 1,5 | 2 |
| Hoch (3) | 1 | 1,5 | 2 | 2,5 | 3 |

Jeder Wert ist die Differenz der beiden Kopfwerte, unten bei 0 abgeschnitten (Gering (1) mit Hoch (2) ergibt 0, nicht
−1).

### (a) Eingang: Spalte N, Gegenwart

Als Stufe ohne Anpassung geht die Mappe, Spalte N „Risiko o. Anp. – Gegenwart“, ein. Gründe:

- Die Selbsteinschätzung beschreibt die Fähigkeiten, die eine Kommune heute hat. Die KWRA koppelt ihre Wirksamkeit für
  den Zeitraum 2020–2030 an das Klimarisiko der Gegenwart; für die Mitte des Jahrhunderts hat sie die Wirksamkeit neu
  eingeschätzt, „separat für den Zeitraum 2020 bis 2030 und für die Mitte des Jahrhunderts“ (TB6 Kap. 5.1, S. 112). Für
  #95 trifft die Kopplung Gegenwart mit 2020–2030 das Restrisiko der KWRA genau (Gegenabgleich unter (e)).
- Was die einfachere Rechnung mit einer Zukunftsspalte verfälschen würde: Die heutige Selbsteinschätzung gegen das Risiko
  zur Mitte (Spalte O oder P) zu rechnen, unterstellt, die Kapazität bleibe bis 2060 gleich. Die KWRA sieht das anders:
  Für #95 steigt ihre Wirksamkeit der beschlossenen Maßnahmen von „gering-mittel“ (W97, 2020–2030) auf „mittel“ (X97,
  Mitte, optimistisch). Die Stufen ohne Anpassung zur Mitte und zum Ende bleiben unverändert im Bericht der Klimawirkung
  sichtbar (Abschnitt „Risiko ohne (weitere) Anpassung“); Regel A rechnet sie nicht um.

### (b) Zwischenstufen

- **Eingang.** Spalte N kennt nur „gering“, „mittel“ und „hoch“ (gemessen am 07.10.2026: in den Spalten N–R aller 102
  Zeilen 166-mal „gering“, 244-mal „mittel“, 100-mal „hoch“, keine Zwischenstufe). Sie gehen als 1, 2 und 3 in Tabelle 5
  ein.
- **Wirksamkeit.** Die fünf Wörter der KWRA (Spalten W–AA) sind dieselben fünf Stufen wie in Tabelle 5: gering = 0,
  gering-mittel = 0,5, mittel = 1, mittel-hoch = 1,5, hoch = 2. Die KWRA bestätigt die Bedeutung: „Der Wert ‚gering‘
  würde das angenommene Klimarisiko ohne Anpassung nicht reduzieren, ‚gering-mittel‘ würde eine Reduzierung um eine
  halbe Stufe bedeuten, ‚mittel‘ um eine Stufe und so weiter“ (TB6 Kap. 5.1, S. 112).
- **Ergebnis.** Die Werte 1, 1,5, 2, 2,5 und 3 heißen gering, gering-mittel, mittel, mittel-hoch und hoch. Das sind die
  fünf Stufen der Restrisiko-Spalten AB–AF der Mappe und der Legende von Tabelle 4 der Broschüre (S. 28).

### (c) Vier Komponenten → Wirksamkeit; die Engpassregel wird ersetzt

Die Kommune stuft für jede Klimawirkung die vier Komponenten nach Fußnote 32 (S. 29) je auf 0 bis 3 ein (`REIFEGRADE`).
Die vier Stufen werden zusammengezählt (0 bis 12) und in einer Tabelle nachgeschlagen: je drei Punkte eine halbe Stufe
Wirksamkeit, abgerundet.

| Summe der vier Reifegrade | 0–2 | 3–5 | 6–8 | 9–11 | 12 |
|---|---|---|---|---|---|
| Wirksamkeit der Kommune | gering (0) | gering-mittel (0,5) | mittel (1) | mittel-hoch (1,5) | hoch (2) |

Die Tabelle ist eine Abschätzung von KAP3 (Herleitung unter „Herkunft der Reifegrade“). Ist eine der vier Komponenten
nicht eingestuft, ist die Wirksamkeit und damit die Stufe mit Anpassung „nicht bestimmbar: Selbsteinschätzung
unvollständig“. Eine fehlende Komponente zählt nicht still als 0.

**Körnigkeit: je Klimawirkung.** Eingestuft wird für jede Klimawirkung einzeln, nicht einmal für die ganze Kommune.
Die Frage je Komponente lautet: Wie gut ist diese Fähigkeit ausgeprägt, um diese Klimawirkung zu mindern? Für #95 etwa:
Zuständigkeit und Hitzeaktionsplan (Organisation), Warnkette und Kühlräume (Technik), Mittel dafür (Finanzen),
Grünflächen und Verschattung (Ökosystem). Gründe: Tabelle 5 zieht die Wirksamkeit von der Stufe einer bestimmten
Klimawirkung ab (S. 29), und die Broschüre beschreibt die Einschätzung als „das Ausmaß …, in welchem ausgewählte
Anpassungsmaßnahmen wirksam werden und dadurch Klimarisiken reduzieren“ (S. 28–29). Die KWRA hat die Wirksamkeit ebenso
je Klimawirkung eingeschätzt und die generische Anpassungskapazität dabei berücksichtigt (TB6 S. 112). Eine Einstufung für
die ganze Kommune darf das Produkt als Vorschlag vorbelegen; gerechnet wird mit der Einstufung, die die Kommune für die
Klimawirkung bestätigt. Was eine einzige Einstufung für alle Klimawirkungen verfälschen würde: Eine Fähigkeit, die für
eine Klimawirkung viel und für eine andere wenig beiträgt, ginge überall mit demselben Wert ein; die Stufe mit Anpassung
fiele bei der einen zu ungünstig und bei der anderen zu günstig aus, je höchstens um die Breite des Rahmens aus (e).

**Warum die Summe und nicht die Engpassregel.** Die Summe zählt die vier Komponenten gleich und lässt eine starke
Komponente eine schwache teilweise ausgleichen. Die Engpassregel (`REGEL_GESAMTSTUFE`) nimmt die niedrigste Stufe und
unterstellt das Gegenteil: Keine Komponente kann eine andere ersetzen. Welche Annahme bei welcher Klimawirkung stimmt,
sagt keine gelesene Quelle. Fußnote 32 nennt die vier Komponenten nebeneinander, ohne Gewicht und ohne Rangfolge (S. 29);
TB6 nennt die sechs Anpassungsdimensionen ebenso (S. 113). Die Broschüre nutzt die Einstufung je Komponente, um „grob“
abzuleiten, „welche Art von Anpassung benötigt wird (z. B. mehr Wissen, Geld, Personen)“ (S. 29), nicht als Grenze der
Minderung. Gewählt ist die Summe aus zwei Gründen. Erstens wirkt bei der Engpassregel nur eine der vier Angaben:
Fortschritt in den drei anderen Komponenten ändert die Stufe nie. Zweitens fängt der Rahmen aus (e) die günstige Seite der
Summe an einer Quelle ab, denn mehr als die weiterreichende Anpassung der KWRA lässt Regel A nie zu. Die Engpassregel irrt
dagegen immer dann, wenn die schwächste Komponente für die Klimawirkung nicht allein entscheidet, und zwar stets in die
ungünstige Richtung. Beispiel #95: Eine Kommune mit Organisation 3, Technik 3, Finanzen 3 und Ökosystem 0 (etwa dicht
bebaut, ohne Grünflächen, aber mit Hitzeaktionsplan, Warnkette und Geld) hätte nach der Engpassregel die Wirksamkeit 0,
nach der Untergrenze (e) 0,5 und die Stufe mit Anpassung „mittel-hoch“. Nach der Summe (9 Punkte, 1,5, durch die
Obergrenze 1) ergibt sich „mittel“. Die schwächste Komponente bleibt sichtbar und zeigt, welche Art von Anpassung fehlt.
Als Engpass wirkt sie nicht mehr; in die Stufe geht sie wie die anderen drei mit ihren Punkten ein. Beispiel #95 mit
Organisation 2, Technik 2 und Finanzen 1: Steigt Ökosystem von 0 auf 1, steigt die Summe von 5 auf 6, und die Stufe mit
Anpassung sinkt von „mittel-hoch“ auf „mittel“.

**Richtung und Größe der möglichen Verzerrung.** Die gleich gewichtete Summe verfälscht die Lage, wenn die vier
Komponenten für eine Klimawirkung unterschiedlich wichtig sind:

- Ist eine Komponente für die Klimawirkung unverzichtbar und steht sie niedrig, zählt die Summe die anderen drei zu stark.
  Die Stufe mit Anpassung fällt zu günstig aus.
- Ist eine niedrig stehende Komponente für die Klimawirkung unerheblich, zieht sie die Summe herunter. Die Stufe fällt zu
  ungünstig aus.

Größer als die Breite des Rahmens aus (e) kann die Verzerrung nicht werden, weil die Wirksamkeit nie unter Spalte W fällt
und nie über den höheren Wert aus Z und AA steigt. Gemessen am 08.10.2026 an den 33 analysierten Zeilen: Der Rahmen ist
21-mal eine Stufe breit, 2-mal 1,5 Stufen (ID 21 und 25), 9-mal eine halbe Stufe und einmal null. Sichtbar wird davon
nach (d) weniger, weil Werte unter 1 als „gering“ erscheinen: In 18 Zeilen kann sich die ausgewiesene Stufe um eine Stufe
verschieben, in 6 um eine halbe, in 9 gar nicht. Für #95 ist der Rahmen eine halbe Stufe breit (0,5–1), die Verzerrung
also höchstens eine halbe Stufe. Bei den 69 Zeilen mit Spalte V = „nein“ ist der Rahmen nach (f) eine Stufe breit;
sichtbar wird das nur in den 17 Zeilen mit Spalte N „mittel“, in den 52 mit „gering“ nicht. Die Engpassregel hätte
dieselbe Höchstgrenze, nur stets in die ungünstige Richtung.

**Warum abgerundet wird.** Eine Summe zwischen zwei Schritten zählt die überschießenden ein oder zwei Punkte nicht. Die
Stufe mit Anpassung liegt dadurch höchstens eine halbe Stufe zu hoch, nie zu niedrig. Das ist die vorsichtige Richtung:
Eine Selbsteinschätzung ist kein Nachweis einer Wirkung.

### (d) Die Werte 0 und 0,5

Tabelle 5 kennt unter „gering“ (1) noch die Werte 0,5 und 0, gibt ihnen aber kein Wort; die Skala des Klimarisikos
beginnt bei 1 (Fußnote zu Tabelle 5, S. 29). Festlegung: Ein Wert unter 1 wird als „gering“ ausgewiesen, mit dem Zusatz
„rechnerisch unter der niedrigsten Stufe (Tabelle 5: 0,5)“ beziehungsweise „(Tabelle 5: 0)“. Für die Kommune heißt das:
Ihre Anpassung reicht rechnerisch weiter, als die Skala noch unterscheidet. Es heißt nicht, dass kein Risiko bleibt; ein
Wort wie „kein Risiko“ würde die Lage zu günstig darstellen, weil Tabelle 5 nur Stufen subtrahiert und keine Grenzen der
Anpassung kennt. Die KWRA verfährt ebenso: In 14 Fällen der Mappe ergibt Tabelle 5 den Wert 0 oder 0,5, und die KWRA führt
das Restrisiko als „gering“ (Gegenabgleich unter (e)).

### (e) Verhältnis zur bundesweiten Wirksamkeit und zum Restrisiko der KWRA

**Ersetzen, nicht addieren.** Die Wirksamkeit der Kommune tritt an die Stelle der bundesweiten Wirksamkeit der KWRA; sie
kommt nicht hinzu. Die weiterreichende Anpassung der KWRA „umfasst Klimaanpassungsmaßnahmen, die die beschlossenen
Maßnahmen einschließen und über diese hinausgehen“, und berücksichtigt „auch andere Akteure als diejenigen auf
Bundesebene“ (TB6 S. 112), also auch Kommunen. Beide Abzüge zusammengezählt, würde dieselbe Anpassung zweimal zählen.

**Rahmen.** Unter- und Obergrenze bilden den Rahmen der Wirksamkeit. Er ist eine Festlegung von KAP3; seine Werte liest
das Produkt je Klimawirkung aus der Mappe (Spalten W, Z und AA), bei Spalte V = „nein“ gilt (f). Die beiden Grenzen
gelten für verschiedene Zeiträume: Spalte W für 2020–2030, die Spalten Z und AA für die Mitte des Jahrhunderts, 2031–2060
(Köpfe W2, Z2 und AA2; TB6 S. 112). Die Obergrenze der Wirksamkeit, mit der die heutige Stufe gerechnet wird, ist also
ein Wert für die Mitte des Jahrhunderts.

**Untergrenze: die beschlossenen Maßnahmen (Spalte W).** Die beschlossenen Maßnahmen des Aktionsplans Anpassung III
„liegen fast nur in der Zuständigkeit des Bundes. Es wird davon ausgegangen, dass diese unter aus heutiger Sicht
plausiblen Bedingungen umgesetzt werden“ (TB6 S. 112). Sie wirken auch in einer Kommune mit schwacher Selbsteinschätzung.
Ohne Untergrenze ergäbe für #95 eine Summe von 0 bis 2 die Stufe „hoch“ und damit eine halbe Stufe über dem bundesweiten
Restrisiko „mittel-hoch“ (AB97): Die Rechnung behauptete, die Bundesmaßnahmen wirkten in dieser Kommune nicht.

**Obergrenze: die weiterreichende Anpassung (höherer Wert aus Spalte Z und AA).** Mehr, als die KWRA mit aller
plausiblen Anpassung bis zur Mitte des Jahrhunderts für erreichbar hält, lässt Regel A heute nicht zu; Anpassung braucht
Zeit (Mappe U97: Anpassungsdauer 10–50 Jahre; Begriff „Anpassungsdauer“, Broschüre S. 19). Ohne Obergrenze ergäbe für #95
die Summe 12 die Wirksamkeit 2 und die Stufe „gering“, eine Stufe unter dem, was die KWRA mit weiterreichender Anpassung
im pessimistischen Fall erwartet (AF97 „mittel“): Die Lage wäre um eine Stufe zu günstig dargestellt. Gemessen am
07.10.2026 liegt die Wirksamkeit der beschlossenen Maßnahmen (W) in keiner der 33 analysierten Zeilen über dem höheren Wert
aus Z und AA; der Rahmen ist also nie leer.

**Gegenabgleich #95.** Tabelle 5 auf die bundesweite Wirksamkeit angewandt, verglichen mit der Restrisiko-Zelle der Mappe:

| Paar | ohne Anpassung | − Wirksamkeit | = Tabelle 5 | Restrisiko der Mappe | trifft |
|---|---|---|---|---|---|
| Gegenwart / 2020–2030, beschlossen | N97 hoch (3) | W97 gering-mittel (0,5) | 2,5 mittel-hoch | AB97 mittel-hoch | ja |
| Mitte optim., beschlossen | O97 mittel (2) | X97 mittel (1) | 1 gering | AC97 gering | ja |
| Mitte pessim., beschlossen | P97 hoch (3) | Y97 gering-mittel (0,5) | 2,5 mittel-hoch | AD97 mittel-hoch | ja |
| Mitte optim., weiterreichend | O97 mittel (2) | Z97 mittel (1) | 1 gering | AE97 gering | ja |
| Mitte pessim., weiterreichend | P97 hoch (3) | AA97 mittel (1) | 2 mittel | AF97 mittel | ja |

Für #95 gibt es keine Abweichung. **Gegenprobe der Regel an der ganzen Mappe** (dieselben fünf Paare für alle 33 Zeilen
mit Spalte V = „ja“, 165 Paare, gemessen am 07.10.2026): 150 treffen ohne weiteres. 14 treffen erst mit (d), weil Tabelle 5
dort 0 oder 0,5 ergibt und die KWRA „gering“ führt (ID 3, 21, 25, 30 dreimal, 35, 47, 50 zweimal, 55, 71 zweimal, 96).
Eine Abweichung bleibt: ID 10 „Bodenerosion durch Wasser“ (Zeile 12), P12 „hoch“ − AA12 „mittel“ = 2 „mittel“, die KWRA
führt in AF12 „mittel-hoch“. Das Restrisiko der KWRA ist eine Bewertung durch Fachleute, keine Rechnung; in diesem einen
Fall haben sie eine halbe Stufe höher bewertet, als die Subtraktion ergibt (dieselbe Stelle ist in
`querschnitt_gewissheit.md`, Abschnitt „Die Regel der KWRA für Entwicklung“, als einziger Fehltreffer vermerkt). Regel A
folgt Tabelle 5 und bildet diese Einzelbewertung nicht nach. Die Kommune sieht das bundesweite Restrisiko (Spalte AB,
2020–2030) zum Vergleich neben ihrer Stufe; es geht nicht in die Rechnung ein.

### (f) Klimawirkungen ohne analysierte Anpassungskapazität

Die KWRA hat die Anpassungskapazität für 33 Klimawirkungen analysiert, ausgewählt nach der Regel „für die Gegenwart
und/oder für die Mitte des Jahrhunderts im pessimistischen Fall als ‚hoch‘ eingeschätzt“ (TB6 S. 112). In der Mappe führen
33 Zeilen in Spalte V „ja“ und 69 „nein“; bei allen 69 sind die Spalten W–AF leer, und Spalte N steht 52-mal auf „gering“,
17-mal auf „mittel“, nie auf „hoch“ (gemessen am 07.10.2026). Für diese 69 gilt Regel A mit zwei **Abschätzungen von
KAP3** an Stelle der fehlenden Grenzen:

- Untergrenze 0 (gering). Begründung: Die KWRA hat für sie keine Wirkung der Bundesmaßnahmen eingeschätzt; „gering“ ist
  auch unter den 33 analysierten der häufigste Wert der Spalte W (23 von 33).
- Obergrenze 1 (mittel). Begründung: Der höhere Wert aus Z und AA ist unter den 33 analysierten 25-mal „mittel“, 3-mal
  „gering-mittel“, 4-mal „mittel-hoch“ und einmal „hoch“.

Empfindlichkeit: Weil Spalte N hier höchstens „mittel“ (2) ist, ändert eine höhere Obergrenze nichts am ausgewiesenen
Wort (2 − 1 = 1 ist schon „gering“). Eine Untergrenze 0,5 statt 0 senkte die Stufe nur bei einer Kommune mit der Summe 0–2
und Spalte N „mittel“, und zwar von „mittel“ auf „gering-mittel“. Das Produkt kennzeichnet die Stufe dieser
Klimawirkungen als „Abschätzung von KAP3; die KWRA hat die Anpassungskapazität nicht analysiert“. Eine stille Null gibt
es nicht.

### (g) Minderungssätze

Die `MINDERUNGSSAETZE` werden neu gefasst. Heute sagen sie je Gesamtstufe, ob sich „das Klimarisiko“ kaum bis weitgehend
verringern lässt, ohne Bezug auf eine Klimawirkung (Gegenprobe Zeile 18, A2 „trägt teilweise“). Neben der Stufe aus
Regel A wären sie eine zweite, möglicherweise widersprüchliche Aussage: Für #95 sagte die Gesamtstufe 0 „kaum“, während
die Untergrenze aus den Bundesmaßnahmen eine halbe Stufe Minderung ergibt. Neu gibt es je Klimawirkung einen Satz, der
die Stufe und ihren Weg zeigt, also auch den Rahmen. Für Klimawirkungen mit Spalte V = „ja“:

> Klimarisiko ohne Anpassung (Gegenwart, KWRA 2021): {Stufe ohne}. Wirksamkeit der Anpassung nach der
> Selbsteinschätzung der Kommune: {Wirksamkeit aus der Summe} ({Summe} von 12 Punkten). Die KWRA hält für diese
> Klimawirkung eine Wirksamkeit von {Spalte W} (beschlossene Maßnahmen, 2020–2030) bis {höherer Wert aus Z und AA}
> (weiterreichende Anpassung, Mitte des Jahrhunderts 2031–2060) für erreichbar; gerechnet wird mit {Wirksamkeit im
> Rahmen}. Klimarisiko mit Anpassung: {Stufe mit} (UBA 2022, Tabelle 5, S. 29; Summentabelle und Rahmen sind
> Festlegungen von KAP3, der Rahmen stammt aus der KWRA-Mappe, Spalten W, Z und AA). Bundesweit nach den beschlossenen
> Maßnahmen (2020–2030): {Spalte AB}.

Für Klimawirkungen mit Spalte V = „nein“, deren Spalten W–AF leer sind:

> Klimarisiko ohne Anpassung (Gegenwart, KWRA 2021): {Stufe ohne}. Wirksamkeit der Anpassung nach der
> Selbsteinschätzung der Kommune: {Wirksamkeit aus der Summe} ({Summe} von 12 Punkten). Die KWRA hat die
> Anpassungskapazität für diese Klimawirkung nicht analysiert; gerechnet wird im Rahmen gering (0) bis mittel (1), einer
> Abschätzung von KAP3, mit {Wirksamkeit im Rahmen}. Klimarisiko mit Anpassung: {Stufe mit} (Abschätzung von KAP3 nach
> UBA 2022, Tabelle 5, S. 29). Ein bundesweites Restrisiko weist die KWRA für diese Klimawirkung nicht aus.

Beispiel #95 mit der Summe 12, vollständig: „Klimarisiko ohne Anpassung (Gegenwart, KWRA 2021): hoch. Wirksamkeit der
Anpassung nach der Selbsteinschätzung der Kommune: hoch (12 von 12 Punkten). Die KWRA hält für diese Klimawirkung eine
Wirksamkeit von gering-mittel (beschlossene Maßnahmen, 2020–2030) bis mittel (weiterreichende Anpassung, Mitte des
Jahrhunderts 2031–2060) für erreichbar; gerechnet wird mit mittel. Klimarisiko mit Anpassung: mittel (UBA 2022,
Tabelle 5, S. 29; Summentabelle und Rahmen sind Festlegungen von KAP3, der Rahmen stammt aus der KWRA-Mappe, Spalten W, Z
und AA). Bundesweit nach den beschlossenen Maßnahmen (2020–2030): mittel-hoch.“ Wer mit Tabelle 5 selbst 3 − 2
nachrechnet, sieht im Satz, warum das Ergebnis nicht „gering“ lautet: Mehr als die Wirksamkeit, die die KWRA der
weiterreichenden Anpassung für die Mitte des Jahrhunderts zuschreibt, rechnet Regel A auch heute nicht an (Begründung
unter (e), „Obergrenze“). Ergibt Tabelle 5 einen Wert unter 1, steht hinter der Stufe der Zusatz aus (d). Der Satz für
eine unvollständige Selbsteinschätzung bleibt in der Sache: „nicht bestimmbar: Selbsteinschätzung unvollständig“.

## Herkunft der Reifegrade

**Gelesen für diese Frage:** Broschüre Abschnitt 2.2.5 (S. 28–29) vollständig mit den Fußnoten 32–34 und Tabelle 5;
S. 18 mit Abbildung 3 (als Bild angesehen); S. 19 mit der Infobox „Zentrale Begriffe“; S. 27 (Ende 2.2.4) und S. 30
(2.2.6) zur Abgrenzung. TB6 Kap. 5.1, S. 112–113. Die Broschüre nennt die vier Komponenten (Fußnote 32) und
„verschiedene Niveaus der Anpassungskapazität“ (S. 29); für die Niveaus verweist sie mit Fußnote 33 auf Anhang G
(„Komponenten der Anpassungskapazität“) und Anhang H („Bewertung der Anpassungskapazität“) der ISO 14091. Die Niveaus
selbst nennt sie nicht. Fußnote 34 verweist für „methodische Details“ auf Kahlenborn et al. 2021a.
Abbildung 3 zeigt die Anpassungskapazität als ein Feld zwischen „Klimarisiko ohne Anpassung“ und „Klimarisiko mit
Anpassung“, ohne Stufen. TB6 S. 112 nennt fünf Stufen der Wirksamkeit und S. 113 sechs „Anpassungsdimensionen“, aber
keine Reifegrade. Den Normtext ISO 14091:2021 hat KAP3 nicht gelesen (Menschenticket T-0531-ceo offen).

| Element | Herkunft | Begründung |
|---|---|---|
| Reifegrad 0 „nicht vorhanden“ | Abschätzung von KAP3 | Unterer Anker: Die Fähigkeit trägt für die Klimawirkung nichts bei und zählt 0 Punkte. Die Wirksamkeit „gering“, die das Risiko „nicht reduzieren“ würde (TB6 S. 112), folgt nach der Summentabelle aus (c) bei 0–2 Punkten, also etwa auch bei 1/1/0/0. |
| Reifegrad 1 „im Aufbau“ | Abschätzung von KAP3 | Unterscheidet erste, nicht verbindliche Ansätze von fehlender Fähigkeit; alle vier auf 1 (Summe 4) ergeben eine halbe Stufe Minderung. |
| Reifegrad 2 „etabliert“ | Abschätzung von KAP3 | Verbindlich verankert und für heute bekannte Risiken ausreichend; alle vier auf 2 (Summe 8) ergeben eine Stufe Minderung, „mittel“ nach Tabelle 5. |
| Reifegrad 3 „vorausschauend“ | Abschätzung von KAP3 | Regelmäßig an künftige Änderungen angepasst, weil Anpassung Zeit braucht (Begriff „Anpassungsdauer“, Broschüre S. 19); nur alle vier auf 3 (Summe 12) erreichen „hoch“ (2). |
| Regel der Gesamtstufe | Abschätzung von KAP3; ersetzt die Engpassregel | Eingestuft je Klimawirkung, weil Tabelle 5 und die KWRA die Wirksamkeit je Klimarisiko führen (Broschüre S. 28–29; TB6 S. 112). Summe statt Minimum, je drei Punkte eine halbe Stufe, abgerundet. Gleiche Gewichte, weil Fußnote 32 die vier Komponenten ohne Gewichtung nebeneinander nennt (S. 29); fünf Stufen 0–2, weil Tabelle 5 fünf Stufen hat (S. 29). Danach der Rahmen aus (e), eine Festlegung von KAP3 mit Werten aus der Mappe (Spalten W, Z und AA). Die Engpassregel hatte keine Fundstelle. |

Vier Stufen statt der fünf von Tabelle 5 je Komponente: Die Einstufung je Komponente ist eine andere Frage als die
Wirksamkeit für ein Risiko; vier Stufen lassen sich ohne Statistikkenntnisse in einem Schritt zuordnen. Die Übersetzung in
die fünf Stufen von Tabelle 5 leistet die Summentabelle unter (c).

**Vorgeschlagener neuer Wortlaut für `HERLEITUNG_REIFEGRADE`:**

> Abschätzung von KAP3: Die vier Stufen 0 bis 3 und ihre Beschreibungen legt KAP3 fest. Die UBA-Handlungsempfehlungen
> zur ISO 14091 (2022) nennen auf S. 29 die vier Komponenten (Fußnote 32) und verweisen für die Niveaus der
> Anpassungskapazität auf Anhang G und H der ISO 14091 (Fußnote 33); die Niveaus selbst nennen sie nicht, und den
> Normtext hat KAP3 nicht gelesen. Die Stufen ordnen nur und sind kein Messwert. Die Kommune stuft die vier Komponenten
> je Klimawirkung ein. Die Summe der vier Stufen (0 bis 12) wird nach einer festen Tabelle in die Wirksamkeit der
> Anpassung nach Tabelle 5 (S. 29) übersetzt: je drei Punkte eine halbe Stufe, abgerundet. Diese Wirksamkeit wird in den
> Rahmen der KWRA 2021 für die Klimawirkung gesetzt: nicht unter die Wirksamkeit der beschlossenen Maßnahmen für
> 2020–2030 und nicht über die der weiterreichenden Anpassung für die Mitte des Jahrhunderts, 2031–2060 (Mappe
> KWRA-2021_Klimawirkungen.xlsx, Spalten W, Z und AA). Hat die KWRA die Anpassungskapazität einer Klimawirkung nicht
> analysiert, gilt als Abschätzung von KAP3 der Rahmen gering (0) bis mittel (1). Summentabelle und Rahmen sind
> Festlegungen von KAP3.

## Anpassungspotenzial und Doppelzählung

Drei Größen des Produkts setzen auf denselben Maßnahmen auf: die Wirkung der Maßnahmen in Euro (Kapitel 5 der Berichte,
`backend/app/services/measure_service.py`), das Anpassungspotenzial (`anpassungspotenzial()` in
`backend/app/services/charakterisierung.py`) und die Anpassungskapazität mit der Stufe aus Regel A. Dieser Abschnitt
legt genau eine Definition des Anpassungspotenzials fest (Definition P) und eine Regel, wie die drei Größen aufeinander
wirken (Regel D). Regel A bleibt unverändert.

### Definition P: Anpassungspotenzial

**Das Anpassungspotenzial einer Klimawirkung in einer Kommune ist der Anteil ihres bewerteten Schadens, den alle
Maßnahmen des Katalogs für diese Klimawirkung zusammen wegnehmen, wenn jede die ganze Kommune abdeckt:**
\(p = 1 - S_{\text{alle}} / S_{\text{ohne}}\).

| Zeichen | Bedeutung | Einheit | Herleitung |
|---|---|---|---|
| \(p\) | Anpassungspotenzial der Klimawirkung in der Kommune | Anteil, 0–1 | abgeleitet aus den beiden Zeilen darunter |
| \(S_{\text{ohne}}\) | bewerteter Schaden der Klimawirkung ohne weitere Anpassung, Summe über ihre Risiko-Codes; der heutige Anpassungsstand steckt darin (#95: über die Kalibrierung, Bericht 95 Kapitel 1 (a)) | Mio. € je Jahr | übernommen aus der Rechenkette des Berichts; #95 Berlin 362,9 Mio. € (Preisstand 2024), Bericht 95 §3.0 Ebene 10; im Produkt `damages_base_eur` in `build_cost_summary` |
| \(S_{\text{alle}}\) | bewerteter Schaden derselben Klimawirkung, wenn jede Maßnahme, die der Katalog ihr im Euro-Pfad zuordnet (`linked_risk_codes`), die ganze Kommune abdeckt (Abdeckung 1, Stückzahl am Richtwert); Eingaben wie der Anteil gekühlter Heimplätze mit dem Wert der Kommune, sonst mit der Voreinstellung aus Kapitel 7 des Berichts | Mio. € je Jahr | abgeleitet mit den Hebeln aus Kapitel 5 des Berichts samt ihren Regeln für das Zusammenwirken, Kappungen und Doppelzählungs-Wächtern; im Produkt derselbe Rechenweg wie `damages_with_measures_eur` in `build_cost_summary` |

Gründe:

- **Je Klimawirkung, nicht je Risiko-Code.** Die KWRA ordnet Klimawirkungen den Gruppen zu: „Welche Klimawirkung auf
  Basis der Betrachtung der Anpassungskapazität welcher Gruppe von Handlungserfordernissen zugeordnet wird, hängt davon
  ab, welches Restrisiko … akzeptiert werden soll“ (TB6 Kap. 6.2, S. 141). Regel A rechnet ebenso je Klimawirkung. In
  Euro lassen sich die Risiko-Codes einer Klimawirkung zusammenzählen (#95: Mortalität und Morbidität).
- **Ein Anteil, kein Betrag.** Die Frage der KWRA ist, ob die Maßnahmen das Risiko auf ein gesetztes Niveau senken
  (TB6 S. 140); die Einordnungsschwellen 0,5 und 0,1 in `querschnitt_gewissheit.md` sind Anteile und bleiben dort.
- **Aus dem Euro-Pfad abgelesen, nicht nachgebaut.** \(p\) nutzt dieselben Hebel, Faktoren und Grenzen wie der
  Euro-Betrag mit Maßnahmen. So steht jeder Wert an einer Stelle (Abgleich-Regel 5 in `.claude/methodik-loop.md`), und
  jede Maßnahme, die den Betrag senkt, zählt auch in \(p\). Keine zählt still mit null (P2).
- **Kein Euro-Betrag, keine Zahl.** Hat eine Klimawirkung im Produkt keinen bewerteten Schaden, ist \(p\) „nicht
  bestimmbar: kein Euro-Betrag“, nie still 0.

**Ohne Kommune (Katalog): \(p_0\).** Die Katalogroute rechnet ohne Kommune, und dabei bleibt es (Befund 214 in
`reviews/BEFUNDE_95.md`, Entscheidung des CEO vom 06.10.2026). Ohne Kommune gibt es keine Beträge \(S\). Dann gilt
dieselbe Definition mit Anteilen statt Beträgen, und es zählen nur die Hebel, die mit einem festen Faktor auf den ganzen
Schaden eines Risiko-Codes wirken (#95: der Hitzeaktionsplan auf die ganze Mortalität):
\(p_0 = \sum_c a_c \times p_{c,0}\), in Worten: je Risiko-Code sein Anteil am Schaden mal der Anteil, den diese Hebel
von ihm wegnehmen, und das für alle Codes der Klimawirkung zusammengezählt.

| Zeichen | Bedeutung | Einheit | Herleitung |
|---|---|---|---|
| \(p_0\) | Anpassungspotenzial der Klimawirkung ohne Kommune; Untergrenze, mit Vermerk | Anteil, 0–1 | abgeleitet aus den beiden Zeilen darunter |
| \(c\) | ein Risiko-Code der Klimawirkung (#95: Mortalität, Morbidität) | — | Katalog, `catalog.RISKS_BY_CODE` |
| \(a_c\) | Anteil des Risiko-Codes \(c\) am bewerteten Schaden der Klimawirkung | Anteil, 0–1 | übernommen aus der Rechenkette des Berichts; #95: Mortalität 361,8 von 362,9 Mio. € = 0,997, Morbidität 0,003 (Bericht 95 §3.0 Ebenen 8–10) |
| \(p_{c,0}\) | Anteil des Schadens von Code \(c\), den die Hebel mit festem Faktor auf den ganzen Code zusammen wegnehmen, nach den Regeln aus Kapitel 5 | Anteil, 0–1 | abgeleitet; #95: Mortalität 1 − 0,939 = 0,061 (Kapitel 5, Hebel Hitzeaktionsplan), Morbidität 0 (ebenda: „Die Morbidität bleibt unberührt“) |

Für #95: \(p_0\) = 0,997 × 0,061 + 0,003 × 0 = 0,0608, auf drei Stellen 0,061. Ein sichtbarer Vermerk nennt die
fehlenden Hebel: S157, Kühlzentren und Schutzprogramme wirken nur auf einzelne Altersbänder oder auf die Heimbewohner,
und wie viel des Schadens das ist, hängt am Altersaufbau und an den Zellen der Kommune. Ohne Kommune zählen sie nicht, und
einen Ersatzwert für sie gibt es nicht (Bericht 95 Kapitel 5, Hebel S157, Absatz „Ohne Kommune (Befund 214)“). Mit
Kommune kommen sie hinzu, deshalb ist \(p_0\) eine Untergrenze (Berlin 0,096, unten). Die Gewichte \(a_c\) stammen aus
der Beispielkommune des Berichts, hängen aber kaum an ihr: In Warmsen trägt die Mortalität 0,995 des Betrags (Kette
177.406 € je Jahr, davon Morbidität 0,1213 Fälle × 7.152 € = 868 €; Bericht 95 §3.5), \(p_0\) ist dort 0,0607, auf drei
Stellen ebenfalls 0,061. Anders als \(a_{85+}\) bei S157, mit dem Berliner Wert in Warmsen 27 % zu hoch (Befund 183), ist
\(a_c\) deshalb keine Berliner Konstante, die andere Kommunen falsch darstellt.

**Was die einfachere Rechnung ohne Kommune verfälschen würde.** Den Berliner Wert 0,096 in den Katalog zu setzen, rechnete
die Hebel an den Altersbändern für jede Kommune mit dem Altersaufbau Berlins; schon bei S157 läge Warmsen damit 27 % zu
hoch. Die 0,061 ohne Vermerk als Anpassungspotenzial zu zeigen, unterschlüge in Berlin 3,5 Pp. (0,061 statt 0,096) und
gäbe den Abstand zur Schwelle 0,1 mit 3,9 Pp. statt 0,4 Pp. an. Deshalb steht \(p_0\) als Untergrenze mit Vermerk.

**Gegen den Code.** `anpassungspotenzial()` in `backend/app/services/charakterisierung.py` rechnet heute so (gemessen am
08.10.2026, ohne Kommune: 0,061 für `EXPECTED_ANNUAL_MORTALITY` und 0,061 für `EXPECTED_ANNUAL_MORBIDITY`):

| Punkt | Definition P | `anpassungspotenzial()` heute | Folge für #95 |
|---|---|---|---|
| Bezug | je Klimawirkung, Euro-Summe ihrer Risiko-Codes | je Risiko-Code; `charakterisierungen()` gibt jedem Code aus `catalog.RISKS_BY_CODE` einen Wert | #95 hat zwei Werte und damit zwei mögliche Gruppen |
| Rechenweg | derselbe wie der Euro-Betrag mit Maßnahmen | eigene Formel \(1 - \prod (1 - r)^n\), die `_reduction_factor` in `measure_service.py` bei voller Abdeckung nachbildet; S157 über `_s157_faktor` | zwei Stellen für denselben Wert |
| Hebel mit eigenem Zweig | zählen mit ihrer Euro-Wirkung | Schutzprogramme (`effect_model` „vg“) haben keine `default_reduction` und zählen mit \(r = 0\); die Kühlzentren im Zweig „s157“ zählen nicht, nur \(r_{\text{S157}}\) | es fehlen 11,7 Mio. € (Schutzprogramme) und 0,75 Mio. € je Jahr (Kühlzentren), Kapitel 5 |
| Morbidität | Hitzeaktionsplan nur auf die Mortalität (Kapitel 5, Hebel Hitzeaktionsplan: „Die Morbidität bleibt unberührt“) | 0,061 auch für die Morbidität, weil der Katalog den Plan mit ihr verknüpft | dieselbe Ursache wie Befund 230 in `reviews/BEFUNDE_95.md` |
| ohne Kommune (Katalogroute) | \(p_0\) = 0,0608, auf drei Stellen 0,061, mit Vermerk für S157, Kühlzentren und Schutzprogramme | S157 zählt nicht (Befund 214), Schutzprogramme und Kühlzentren zählen nie; Mortalität und Morbidität je 0,061; kein Vermerk | auf drei Stellen gleich; es fehlt der Vermerk |
| Interpretationsbericht einer Kommune | mit der Kommune gerechnet | `interpretationsbericht_fuer_kommune` in `backend/app/services/ergebnis_interpretation_markdown.py` hat die Kommune, ruft `charakterisierungen()` aber ohne sie auf | der Bericht für Berlin zeigt 0,061 statt 0,096 |

In der Formel des Codes ist \(r\) die `default_reduction` einer Maßnahme, auf 0–1 begrenzt, und \(n\) die Zahl ihrer
`effect_target`-Komponenten, mindestens 1; das Produkt \(\prod\) läuft über alle Maßnahmen des Katalogs, deren
`linked_risk_codes` den Code enthalten. \(r_{\text{S157}}\) ist der Anteil der ganzen Hitzemortalität, den S157 bei der
Voreinstellung wegnimmt (Bericht 95 Kapitel 5, Hebel S157, Absatz „S157 mit seiner Voreinstellung im
Anpassungspotenzial (Befund 149)“).

**Was die heutige Formel an der Lage verfälscht.** Für Berlin nennt Bericht 95 nach der heutigen Formel \(p\) = 0,064
(Kapitel 5, Hebel S157, Absatz „S157 mit seiner Voreinstellung im Anpassungspotenzial (Befund 149)“). Nach Definition P
zählen Schutzprogramme und Kühlzentren mit. \(S_{\text{alle}}\) folgt aus den Regeln für das Zusammenwirken in Kapitel 5,
je Teil des Schadens (Block `doppelzaehlung_95`):

| Teil des Schadens, Berlin (Kette) | Betrag | Hebel und Regel (Bericht 95 Kapitel 5) | weniger |
|---|---|---|---|
| Mortalität, Bänder 75–84 und 85+ außerhalb der Heime | 169,5 Mio. € (Hebel Schutzprogramme, Absatz „Berlin“) | Hitzeaktionsplan, Schutzprogramme und Kühlzentren multipliziert: 0,939 × 0,931 × 0,995585 = 0,8703; die Kappung 0,794 greift nicht (Absatz „Kappung 0,794“) | 169,5 × (1 − 0,8703) = 21,98 Mio. € |
| Mortalität, Heimbewohner ab 85 | 638,8 YLL × 0,344 × 160.800 € = 35,34 Mio. € (YLL 85+ und Heimanteil wie bei den Schutzprogrammen, Wert je YLL §3.0 Ebene 8) | Hitzeaktionsplan 1 − 0,939 = 0,061 | 35,34 × 0,061 = 2,16 Mio. € |
| dazu S157 bei der Voreinstellung | 1,249 Mio. € (Hebel S157, Absatz „Sensitivität“) | mit dem Plan gedämpft, × 0,939 (Absatz „Zusammen mit dem Hitzeaktionsplan (Befund 129)“) | 1,249 × 0,939 = 1,17 Mio. € |
| Mortalität, Bänder unter 75 | Rest: 361,8 − 169,5 − 35,34 = 156,96 Mio. € (§3.0 Ebene 8) | Hitzeaktionsplan 0,061 | 156,96 × 0,061 = 9,57 Mio. € |
| Morbidität | 1,09 Mio. € (§3.0 Ebene 9) | keiner wirkt (Hitzeaktionsplan: „Die Morbidität bleibt unberührt“; Schutzprogramme \(\delta_{\text{VG,morb}}\) = 1,0) | 0 |
| zusammen | 362,9 Mio. € | | **34,9 Mio. €** |

\(S_{\text{alle}}\) = 362,9 − 34,9 = 328,0 Mio. € je Jahr, \(p\) = 1 − 328,0 / 362,9 = 34,9 / 362,9 = **0,096**.
Gegenprobe: Die Summe der Einzelbeträge aus Kapitel 5 ist eine Obergrenze, weil die Hebel auf denselben Exzess
multipliziert und gekappt werden und zusammen nie mehr wegnehmen als einzeln addiert:
(22,1 + 1,2 + 0,75 + 11,7) / 362,9 = 35,75 / 362,9 = 0,0985; 0,096 liegt darunter. Die Gruppe (unter 0,1) bleibt, der
Abstand zur Schwelle schrumpft aber von 3,6 Pp. auf 0,4 Pp. Am oberen Bandende der Schutzprogramme (34,9 Mio. €, Kapitel 5,
Absatz „Kappung 0,794“) liegt \(p\) bei mindestens (34,9 + 192,3 × 0,061) / 362,9 = 0,128 und damit über 0,1;
192,3 Mio. € = 361,8 − 169,5 Mio. € ist die Mortalität außerhalb der Bänder ab 75 ohne Heim, auf die der
Hitzeaktionsplan wirkt; S157 käme hinzu und ist hier nicht mitgezählt. Die Gruppe hängt dann an einem Hebel, den die heutige Formel nicht sieht. Die Abweichung steht
als Befund 1 unter „Befunde an Berichte“; der Code bleibt hier unverändert.

### Regel D: wie die drei Größen aufeinander wirken

**Regel D.**

1. Den Euro-Betrag senken nur die Maßnahmen, die die Kommune wählt, über die Hebel aus Kapitel 5 ihres Berichts, jeder
   einmal und nach den Regeln dort für das Zusammenwirken. Der Euro-Betrag hat zwei Zustände: ohne weitere Anpassung
   (\(S_{\text{ohne}}\)) und mit den gewählten Maßnahmen.
2. Die Anpassungskapazität wirkt nur auf die Stufe (Regel A), nie auf den Euro-Betrag.
3. Das Anpassungspotenzial wird aus dem Euro-Pfad abgelesen (Definition P) und wirkt nur auf die
   Charakterisierungsgruppe, zusammen mit der Gewissheit. Es wird weder vom Euro-Betrag noch von der Stufe abgezogen.
4. Stufe und Euro-Betrag werden nie ineinander umgerechnet.

| Größe | auf den Euro-Betrag | auf die Stufe mit Anpassung | auf die Charakterisierungsgruppe |
|---|---|---|---|
| Wirkung der gewählten Maßnahmen (Kapitel 5, `measure_service.py`) | senkt ihn, jeder Hebel einmal | keine | keine |
| Anpassungspotenzial \(p\) (Definition P, `charakterisierung.py`) | keine; wird aus ihm abgelesen | keine | wirkt, mit der Gewissheit |
| Anpassungskapazität: Summe der Reifegrade → Wirksamkeit (Regel A) | keine | senkt sie | keine |

**Warum die Kapazität nur auf die Stufe wirkt:**

1. **Keine Effektgröße (Grund 1).** Die Reifegrade sind eine Selbsteinschätzung und kein Nachweis einer Wirkung ((c),
   „Warum abgerundet wird“). Ein Euro-Hebel braucht eine Effektgröße aus Interventionsstudien oder eine hergeleitete
   Abschätzung, marginal gegenüber dem heutigen Stand (Aufgabe §3.5). Tabelle 5 rechnet in Stufen von 1 bis 3 und kennt
   keinen Euro (Broschüre S. 29).
2. **Dieselben Maßnahmen (Grund 2).** Für #95 fragt die Einstufung nach Hitzeaktionsplan, Warnkette, Kühlräumen und
   Grünflächen ((c), „Körnigkeit“). Den Hitzeaktionsplan, die Kühlräume und die Schutzprogramme rechnet Kapitel 5 schon
   als Hebel in Euro. Eine Minderung aus der Kapazität käme hinzu und zöge denselben Plan ein zweites Mal ab.
3. **Der Bestand im Mittel Deutschlands steckt im Basiswert (Grund 3).** Was in den Kalibrierjahren 2012–2024 schon
   wirkte, ist im Euro-Betrag ohne weitere Anpassung enthalten, und zwar im Mittel Deutschlands, nicht im Stand der
   Kommune: Der Kalibrierfaktor ist an die Hitzetoten Deutschlands angepasst (Bericht 95 Kapitel 1 (a)), und „Der Abzug
   rechnet mit dem Mittel Deutschlands, nicht mit dem Stand der Kommune“ (Bericht 95 Kapitel 5, Hebel S157,
   Gegenargument (3)). Kapitel 5 zählt ein Programm, das schon in diesen Jahren lief, deshalb nicht noch einmal als
   Hebel (Doppelzählungs-Wächter `heat.vg_in_kalibrierjahren`); bei den gekühlten Heimplätzen zählt nur der Anteil über
   dem Mittel der Kalibrierjahre (`heat.s_gek_kalib`). Die Selbsteinschätzung beschreibt den Stand der Kommune. Soweit
   er dem Mittel entspricht, zählte sie ihn als Euro-Minderung ein zweites Mal. Für einen Stand über dem Mittel gilt das
   nicht; die Entscheidung tragen dort die Gründe 1 und 2 (Modellgrenze unten).

**Warum nichts doppelt zählt.** Jede Maßnahme wirkt auf jeder Skala genau einmal. Im Euro-Betrag wirkt sie als Hebel aus
Kapitel 5. In der Stufe wirkt sie über die Selbsteinschätzung der Kommune, die an die Stelle der bundesweiten Wirksamkeit
tritt ((e), „Ersetzen, nicht addieren“). Die gewählten Maßnahmen senken die Stufe nicht noch einmal, und die Stufe senkt
den Euro-Betrag nicht. Stufe und Betrag stehen nebeneinander und werden nie addiert, multipliziert oder ineinander
umgerechnet. Das Anpassungspotenzial ist ein Verhältnis zweier Beträge desselben Pfads und zieht nichts ab.

**Was die einfachere Rechnung verfälschen würde.** Läse man die Minderung der Stufe als Minderung des Betrags, im
Beispiel der Rechenkette von 3 auf 2 also als ein Drittel weniger, fielen in Berlin nach dem Hitzeaktionsplan weitere
340,8 Mio. € × (1 − 2/3) = 113,6 Mio. € je Jahr weg (Block `doppelzaehlung_95`). Das ist gut das Fünffache des Plans
selbst (22,1 Mio. €), ohne Effektgröße, und den Plan zählte die Rechnung zweimal, wenn die Kommune ihre Organisation
wegen dieses Plans hoch einstuft.

**Modellgrenzen.**

- Wählt eine Kommune Maßnahmen, ohne ihre Selbsteinschätzung nachzuführen, sinkt der Betrag, die Stufe aber nicht. Das
  ist keine Doppelzählung, sondern ein fehlender Abgleich; das Produkt zeigt beides mit seiner Grundlage nebeneinander.
- Der Basiswert rechnet jede Kommune mit dem Anpassungsstand im Mittel Deutschlands. Was darüber hinausgeht, senkt den
  Euro-Betrag nur auf zwei Wegen: über den Anteil gekühlter Heimplätze, soweit er über dem Mittel der Kalibrierjahre
  liegt (\(s_{\text{gek}}\) − 0,06, `heat.s_gek_kalib`), und über neu gewählte Maßnahmen, bei Schutzprogrammen und
  Kühlzentren mit der Wächter-Antwort „nein“. Ein älteres Programm, das schon 2012–2024 lief, bekommt die Antwort „ja“,
  und dann gilt \(\delta_{\text{VG}}\) = \(\delta_{\text{VG,morb}}\) = 1 und \(\delta_{\text{KZ}}\) = 1 (Bericht 95
  Kapitel 5, Hebel Schutzprogramme, Absatz „Doppelzählungs-Wächter (Befund 150)“, und Hebel Kühlzentren; Block
  `heat.vg_in_kalibrierjahren`). Ein solches Programm steckt im Betrag also nur mit dem Mittel Deutschlands; seinen
  Vorsprung vor dem Mittel zeigt allein die Stufe über die Selbsteinschätzung. Für eine Kommune mit einem älteren
  Programm fällt der Betrag deshalb zu hoch aus, nach den Abschätzungen aus Kapitel 5 höchstens um die Wirkung, die das
  Programm als neue Maßnahme hätte: in Berlin 11,7 Mio. € (Schutzprogramme) und 0,75 Mio. € je Jahr (Kühlzentren). In
  den Betrag holt die Selbsteinschätzung diesen Vorsprung nicht, weil sie keine Effektgröße hat (Grund 1).

## Rechenkette

Format nach Aufgabe §4, hier „Feld der Mappe → Stufe“ und Nachschlagen in Tabellen statt „Zahl × Faktor“. Kein
Euro-Betrag am Ende: Ergebnisgröße ist die Stufe auf der Skala von Tabelle 5.

| Ebene | Rechenschritt | Wert (#95 Hitzebelastung, Beispielkommune) | Quelle |
|---|---|---|---|
| 1 | Klimawirkung → Zeile der Mappe (Spalte A = 95) | Zeile 97; D97 „Hitzebelastung“; V97 „ja“ | Mappe A97, D97, V97 |
| 2 | Stufe ohne Anpassung, Gegenwart (Kopf N2 „Risiko o. Anp. – Gegenwart“) → Zeile von Tabelle 5 | hoch = 3 | Mappe N97; Broschüre Tabelle 5, S. 29 |
| 3 | Selbsteinschätzung der vier Komponenten für #95 (je Klimawirkung, Festlegung (c)), **Beispiel, keine Messung** | Organisation 3, Technik 2, Finanzen 1, Ökosystem 3 | Komponenten nach Fußnote 32, S. 29; Stufen `REIFEGRADE` |
| 4 | Summe der vier Reifegrade | 3 + 2 + 1 + 3 = 9 | Rechnung |
| 5 | Summe → Wirksamkeit der Kommune (Summentabelle) | 9 → mittel-hoch = 1,5 | Festlegung (c), Abschätzung von KAP3 |
| 6 | Untergrenze: Wirksamkeit der beschlossenen Maßnahmen 2020–2030 (Kopf W2) | gering-mittel = 0,5 | Mappe W97; TB6 S. 112 |
| 7 | Obergrenze: höherer Wert aus weiterreichender Anpassung, Mitte des Jahrhunderts 2031–2060, optim. und pessim. (Köpfe Z2, AA2) | mittel = 1 und mittel = 1 → 1 | Mappe Z97, AA97; TB6 S. 112 |
| 8 | Wirksamkeit im Rahmen: nicht unter Ebene 6, nicht über Ebene 7 | 1,5 → 1 (mittel) | Festlegung (e) |
| 9 | Tabelle 5: Zeile „Hoch (3)“, Spalte „Mittel (1)“ | 3 − 1 = 2 | Broschüre Tabelle 5, S. 29 |
| 10 | Wert → Stufe mit Anpassung | 2 = **mittel** | Festlegung (b) und (d) |

Neben der Stufe, nicht in der Rechnung: schwächste Komponente Finanzen (1), also fehlt vor allem Geld (Broschüre S. 29);
bundesweit nach den beschlossenen Maßnahmen (2020–2030) „mittel-hoch“ (AB97). Stärkster Treiber ist die Stufe ohne
Anpassung („hoch“). Die beiden Grenzen aus der KWRA lassen der Selbsteinschätzung für #95 eine halbe Stufe Spielraum:
Die Stufe mit Anpassung hängt nur daran, ob die Summe unter 6 liegt.

| Summe für #95 | 0–2 | 3–5 | 6–8 | 9–11 | 12 |
|---|---|---|---|---|---|
| Wirksamkeit nach Summentabelle | 0 | 0,5 | 1 | 1,5 | 2 |
| im Rahmen 0,5–1 | 0,5 | 0,5 | 1 | 1 | 1 |
| Stufe mit Anpassung | mittel-hoch | mittel-hoch | mittel | mittel | mittel |

**Euro-Betrag ohne und mit Maßnahmen nach Regel D (#95, Berlin).** Ohne weitere Anpassung trägt #95 in Berlin
362,9 Mio. € je Jahr (Preisstand 2024; Bericht 95 §3.0 Ebene 10, Zustand nach Kapitel 1 (a)). Mit dem Hitzeaktionsplan
sind es 362,9 − 22,1 = 340,8 Mio. € je Jahr; die 22,1 Mio. € = 361,8 Mio. € × (1 − 0,939) stehen in Bericht 95
Kapitel 5, Hebel „Hitzeaktionsplan / Frühwarnkette (S155/S158)“, Absatz „Berlin“. Die Selbsteinschätzung aus Ebene 3
(Summe 9) ändert keinen der beiden Beträge (Regel D, Punkt 2); sie senkt allein die Stufe von „hoch“ auf „mittel“
(Ebenen 2 und 10). Der Plan ändert die Stufe nur, wenn die Kommune ihn in ihrer Selbsteinschätzung führt. Das
Anpassungspotenzial nach Definition P ist für Berlin 34,9 / 362,9 = 0,096, 0,4 Pp. unter der Schwelle 0,1; ohne
Kommune, im Katalog, ist es 0,061 mit Vermerk.

Beispiel-Block `rechenkette_klimarisiko_mit_anpassung_95`, aus dem Stamm des Produkt-Repos ausführbar (am 07.10.2026
gelaufen, Ausgabe darunter):

```python
# rechenkette_klimarisiko_mit_anpassung_95 — Regel A an #95 nachgerechnet
import openpyxl

RISIKO = {"gering": 1.0, "mittel": 2.0, "hoch": 3.0}  # Broschüre Tabelle 5, S. 29
WIRKSAMKEIT = {"gering": 0.0, "gering-mittel": 0.5, "mittel": 1.0, "mittel-hoch": 1.5, "hoch": 2.0}  # ebenda
STUFE = {1.0: "gering", 1.5: "gering-mittel", 2.0: "mittel", 2.5: "mittel-hoch", 3.0: "hoch"}  # TB6 S. 112


def wirksamkeit_aus_summe(summe):
    """Ebene 5: je drei Punkte eine halbe Stufe, abgerundet (Abschätzung von KAP3)."""
    assert 0 <= summe <= 12
    return (summe // 3) * 0.5


def tabelle_5(ohne, wirksamkeit):
    """Ebene 9: ohne Anpassung minus Wirksamkeit, unten bei 0 abgeschnitten."""
    return max(0.0, ohne - wirksamkeit)


def stufe(wert):
    """Ebene 10: Werte unter 1 heißen „gering“ (Festlegung d)."""
    return STUFE[max(1.0, wert)]


# Tabelle 5 selbst, alle 15 Felder (Spalten Hoch … Gering)
TAB5 = {1: (0, 0, 0, 0.5, 1), 2: (0, 0.5, 1, 1.5, 2), 3: (1, 1.5, 2, 2.5, 3)}
for r, soll in TAB5.items():
    assert tuple(tabelle_5(r, w) for w in (2, 1.5, 1, 0.5, 0)) == soll

ws = openpyxl.load_workbook("docs/KWAR/KWRA-2021_Klimawirkungen.xlsx", data_only=True)["Klimawirkungen"]
assert (ws["N2"].value, ws["W2"].value) == ("Risiko o. Anp. – Gegenwart", "Wirksamkeit APA III – 2020–2030")
assert (ws["Z2"].value, ws["AA2"].value) == ("Wirksamkeit weiterr. – Mitte optim.", "Wirksamkeit weiterr. – Mitte pessim.")

# Ebenen 1 und 2
zeile = next(r for r in range(3, ws.max_row + 1) if ws.cell(r, 1).value == 95)
assert zeile == 97 and ws["D97"].value == "Hitzebelastung" and ws["V97"].value == "ja"
ohne = RISIKO[ws["N97"].value]

# Ebenen 3 bis 5 (Selbsteinschätzung als Beispiel)
beispiel = {"organisation": 3, "technik": 2, "finanzen": 1, "oekosystem": 3}
summe = sum(beispiel.values())
eigen = wirksamkeit_aus_summe(summe)

# Ebenen 6 bis 8
unten = WIRKSAMKEIT[ws["W97"].value]
oben = max(WIRKSAMKEIT[ws["Z97"].value], WIRKSAMKEIT[ws["AA97"].value])
wirk = min(max(eigen, unten), oben)

# Ebenen 9 und 10
wert = tabelle_5(ohne, wirk)
print("ohne:", ws["N97"].value, ohne, "| Summe:", summe, "| eigen:", eigen, "| Rahmen:", unten, oben,
      "| Wirksamkeit:", wirk, "| Tabelle 5:", wert, "| mit Anpassung:", stufe(wert),
      "| Engpass:", min(beispiel, key=beispiel.get), "| bundesweit AB97:", ws["AB97"].value)
assert (ohne, summe, eigen, unten, oben, wirk, wert, stufe(wert)) == (3.0, 9, 1.5, 0.5, 1.0, 1.0, 2.0, "mittel")

# Stufe mit Anpassung für #95 je Summe 0 bis 12
je_summe = {s: stufe(tabelle_5(ohne, min(max(wirksamkeit_aus_summe(s), unten), oben))) for s in range(13)}
print("je Summe:", je_summe)
assert all(je_summe[s] == ("mittel-hoch" if s < 6 else "mittel") for s in range(13))

# Gegenabgleich (e): Tabelle 5 auf die bundesweite Wirksamkeit, alle Zeilen mit V = „ja“
PAARE = (("N", "W", "AB"), ("O", "X", "AC"), ("P", "Y", "AD"), ("O", "Z", "AE"), ("P", "AA", "AF"))
ja = [r for r in range(3, ws.max_row + 1) if ws[f"V{r}"].value == "ja"]
ohne_d, mit_d, abw = 0, 0, []
for r in ja:
    for o, w, rr in PAARE:
        roh = tabelle_5(RISIKO[ws[f"{o}{r}"].value], WIRKSAMKEIT[ws[f"{w}{r}"].value])
        ohne_d += roh in STUFE and STUFE[roh] == ws[f"{rr}{r}"].value
        if stufe(roh) == ws[f"{rr}{r}"].value:
            mit_d += 1
        else:
            abw.append((ws[f"A{r}"].value, f"{o}{r}", f"{w}{r}", f"{rr}{r}", roh, ws[f"{rr}{r}"].value))
treffer_95 = [stufe(tabelle_5(RISIKO[ws[f"{o}97"].value], WIRKSAMKEIT[ws[f"{w}97"].value])) == ws[f"{rr}97"].value
              for o, w, rr in PAARE]
print("Zeilen V = ja:", len(ja), "| Paare:", 5 * len(ja), "| treffen ohne (d):", ohne_d, "| mit (d):", mit_d,
      "| Abweichung:", abw, "| #95:", treffer_95)
assert (len(ja), ohne_d, mit_d, abw[0][0], all(treffer_95)) == (33, 150, 164, 10, True)
```

Ausgabe:

```
ohne: hoch 3.0 | Summe: 9 | eigen: 1.5 | Rahmen: 0.5 1.0 | Wirksamkeit: 1.0 | Tabelle 5: 2.0 | mit Anpassung: mittel | Engpass: finanzen | bundesweit AB97: mittel-hoch
je Summe: {0: 'mittel-hoch', 1: 'mittel-hoch', 2: 'mittel-hoch', 3: 'mittel-hoch', 4: 'mittel-hoch', 5: 'mittel-hoch', 6: 'mittel', 7: 'mittel', 8: 'mittel', 9: 'mittel', 10: 'mittel', 11: 'mittel', 12: 'mittel'}
Zeilen V = ja: 33 | Paare: 165 | treffen ohne (d): 150 | mit (d): 164 | Abweichung: [(10, 'P12', 'AA12', 'AF12', 2.0, 'mittel-hoch')] | #95: [True, True, True, True, True]
```

Beispiel-Block `doppelzaehlung_95`, Regel D und Definition P an #95, Berlin; alle Beträge aus Bericht 95 (am 08.10.2026
gelaufen, Ausgabe darunter):

```python
# doppelzaehlung_95 — Regel D und Definition P an #95, Berlin (Beträge aus Bericht 95)
S_OHNE = 362.9   # Mio. € je Jahr (Preisstand 2024), Bericht 95 §3.0 Ebene 10
MORT = 361.8     # Mio. € je Jahr, Mortalität, Bericht 95 §3.0 Ebene 8
D_HAP = 0.939    # Kapitel 5, Hebel Hitzeaktionsplan
EINZELN = {"Hitzeaktionsplan": 22.1, "S157": 1.2, "Kuehlzentren": 0.75, "Schutzprogramme": 11.7}  # Kapitel 5, Berlin
R_S157 = 0.00345  # Kapitel 5, Hebel S157, Absatz „S157 mit seiner Voreinstellung im Anpassungspotenzial“
VG_BAENDER = 169.5  # Mio. € je Jahr, Bänder 75–84 und 85+ außerhalb der Heime, Kapitel 5, Schutzprogramme
VG_OBEN = 34.9   # Mio. € je Jahr, Schutzprogramme am oberen Bandende, Kappung 0,794, Kapitel 5

# Regel D, Punkte 1 und 2: Euro ohne und mit Hitzeaktionsplan; die Kapazität wirkt auf keinen Betrag
hap = round(MORT * (1 - D_HAP), 1)
s_mit = round(S_OHNE - hap, 1)
# Definition P: Grenzen für Berlin
p_heute = 1 - D_HAP * (1 - R_S157)
p_oben = sum(EINZELN.values()) / S_OHNE
p_vg_oben = (VG_OBEN + (MORT - VG_BAENDER) * (1 - D_HAP)) / S_OHNE
# verworfene Rechnung: Stufe 3 → 2 als ein Drittel weniger Euro
verworfen = s_mit * (1 - 2 / 3)
print("ohne:", S_OHNE, "| Hitzeaktionsplan:", hap, "| mit:", s_mit, "| p heute:", round(p_heute, 3),
      "| p höchstens:", round(p_oben, 4), "| p am oberen Band der Schutzprogramme mindestens:", round(p_vg_oben, 3),
      "| verworfen, Stufe als Euro:", round(verworfen, 1))
assert (hap, s_mit, round(p_heute, 3), round(p_oben, 4), round(p_vg_oben, 3), round(verworfen, 1)) == \
    (22.1, 340.8, 0.064, 0.0985, 0.128, 113.6)
assert round(p_heute, 3) < 0.1 and p_oben < 0.1 < p_vg_oben  # Schwelle 0,1 aus querschnitt_gewissheit.md

# Definition P, genauer Wert für Berlin: S_alle nach den Regeln für das Zusammenwirken aus Kapitel 5
YLL_85 = 638.8      # YLL Band 85+, Kapitel 5 (S157, Schutzprogramme)
H_HEIM = 0.344      # Anteil der Heimbewohner, Kapitel 5, Schutzprogramme
VOLY = 0.1608       # Mio. € je YLL, §3.0 Ebene 8
D_VG = 0.931        # Kapitel 5, Schutzprogramme
D_KZ = 0.995585     # Kapitel 5, Kühlzentren
KAPPUNG = 0.794     # Kapitel 5, Absatz „Kappung 0,794“
S157_EINZELN = 1.249  # Mio. € je Jahr, Kapitel 5, Hebel S157, Absatz „Sensitivität“
e_heim = YLL_85 * H_HEIM * VOLY
e_unter75 = MORT - VG_BAENDER - e_heim
faktor_75 = max(D_HAP * D_VG * D_KZ, KAPPUNG)
weniger = {"75+ ohne Heim": VG_BAENDER * (1 - faktor_75), "Heim, Plan": e_heim * (1 - D_HAP),
           "Heim, S157": S157_EINZELN * D_HAP, "unter 75": e_unter75 * (1 - D_HAP), "Morbiditaet": 0.0}
p_berlin = sum(weniger.values()) / S_OHNE
print({k: round(v, 2) for k, v in weniger.items()}, "| zusammen:", round(sum(weniger.values()), 2),
      "| S_alle:", round(S_OHNE - sum(weniger.values()), 1), "| p:", round(p_berlin, 4),
      "| Abstand zu 0,1 in Pp.:", round((0.1 - p_berlin) * 100, 1))
assert (round(e_heim, 2), round(e_unter75, 2), round(faktor_75, 4)) == (35.34, 156.96, 0.8703)
assert [round(v, 2) for v in weniger.values()] == [21.98, 2.16, 1.17, 9.57, 0.0]
# Tabelle „Teil des Schadens“ mit den angezeigten Stellen nachgerechnet
assert [round(x, 2) for x in (169.5 * (1 - 0.8703), 35.34 * 0.061, 1.249 * 0.939, 156.96 * 0.061)] == \
    [21.98, 2.16, 1.17, 9.57]
assert (round(sum(weniger.values()), 1), round(p_berlin, 3), round((0.1 - p_berlin) * 100, 1)) == (34.9, 0.096, 0.4)
assert p_heute < p_berlin < p_oben

# ohne Kommune: p_0 = Summe über die Codes von a_c × p_c,0; ohne Kommune wirkt nur der Hitzeaktionsplan
p0_berlin = (MORT / S_OHNE) * (1 - D_HAP)                 # a_Mortalität aus §3.0, Morbidität × 0
S_WARMSEN = 177406                                         # € je Jahr, Kette Warmsen, Bericht 95 §3.5
MORB_WARMSEN = 0.1213 * 7152                               # € je Jahr, ebenda
p0_warmsen = (1 - MORB_WARMSEN / S_WARMSEN) * (1 - D_HAP)
print("a Mortalität Berlin:", round(MORT / S_OHNE, 3), "| Warmsen:", round(1 - MORB_WARMSEN / S_WARMSEN, 3),
      "| p_0 Berlin:", round(p0_berlin, 4), "| Warmsen:", round(p0_warmsen, 4),
      "| Abstand p - p_0 Berlin in Pp.:", round((p_berlin - p0_berlin) * 100, 1))
assert (round(p0_berlin, 4), round(p0_warmsen, 4)) == (0.0608, 0.0607)
assert round(p0_berlin, 3) == round(p0_warmsen, 3) == 0.061
assert round((p_berlin - p0_berlin) * 100, 1) == 3.5 and round((0.1 - p0_berlin) * 100, 1) == 3.9
```

Ausgabe:

```
ohne: 362.9 | Hitzeaktionsplan: 22.1 | mit: 340.8 | p heute: 0.064 | p höchstens: 0.0985 | p am oberen Band der Schutzprogramme mindestens: 0.128 | verworfen, Stufe als Euro: 113.6
{'75+ ohne Heim': 21.98, 'Heim, Plan': 2.16, 'Heim, S157': 1.17, 'unter 75': 9.57, 'Morbiditaet': 0.0} | zusammen: 34.88 | S_alle: 328.0 | p: 0.0961 | Abstand zu 0,1 in Pp.: 0.4
a Mortalität Berlin: 0.997 | Warmsen: 0.995 | p_0 Berlin: 0.0608 | Warmsen: 0.0607 | Abstand p - p_0 Berlin in Pp.: 3.5
```

**#96 Allergische Reaktionen durch Aeroallergene pflanzlicher Herkunft (Schritt 3).** Dieselbe Regel und dieselben zehn
Ebenen wie für #95, Werte aus Zeile 98 der Mappe. Die Kommune stuft die vier Komponenten für diese Klimawirkung ein, etwa:
Zuständigkeit und Weitergabe der Pollenflug-Warnung an Kitas, Schulen und Heime (Organisation), Warnkette (Technik),
Mittel dafür (Finanzen), allergenarme Stadtbäume (Ökosystem). Die Beispielwerte sind andere als bei #95, weil die
Kommune je Klimawirkung einstuft ((c), „Körnigkeit“).

| Ebene | Rechenschritt | Wert (#96, Beispielkommune) | Quelle |
|---|---|---|---|
| 1 | Klimawirkung → Zeile der Mappe (Spalte A = 96) | Zeile 98; D98 „Allergische Reaktionen durch Aeroallergene pflanzlicher Herkunft“; V98 „ja“ | Mappe A98, D98, V98 |
| 2 | Stufe ohne Anpassung, Gegenwart (Kopf N2 „Risiko o. Anp. – Gegenwart“) → Zeile von Tabelle 5 | gering = 1 | Mappe N98; Broschüre Tabelle 5, S. 29 |
| 3 | Selbsteinschätzung der vier Komponenten für #96, **Beispiel, keine Messung** | Organisation 2, Technik 2, Finanzen 1, Ökosystem 2 | Komponenten nach Fußnote 32, S. 29; Stufen `REIFEGRADE` |
| 4 | Summe der vier Reifegrade | 2 + 2 + 1 + 2 = 7 | Rechnung |
| 5 | Summe → Wirksamkeit der Kommune (Summentabelle) | 7 → mittel = 1 | Festlegung (c), Abschätzung von KAP3 |
| 6 | Untergrenze: Wirksamkeit der beschlossenen Maßnahmen 2020–2030 (Kopf W2) | gering-mittel = 0,5 | Mappe W98; TB6 S. 112 |
| 7 | Obergrenze: höherer Wert aus weiterreichender Anpassung, Mitte des Jahrhunderts 2031–2060 (Köpfe Z2, AA2) | mittel = 1 und mittel = 1 → 1 | Mappe Z98, AA98; TB6 S. 112 |
| 8 | Wirksamkeit im Rahmen: nicht unter Ebene 6, nicht über Ebene 7 | 1 bleibt 1 (mittel) | Festlegung (e) |
| 9 | Tabelle 5: Zeile „Gering (1)“, Spalte „Mittel (1)“ | 1 − 1 = 0 | Broschüre Tabelle 5, S. 29 |
| 10 | Wert → Stufe mit Anpassung | 0 = **gering**, rechnerisch unter der niedrigsten Stufe (Tabelle 5: 0) | Festlegung (b) und (d) |

Neben der Stufe, nicht in der Rechnung: schwächste Komponente Finanzen (1); bundesweit nach den beschlossenen Maßnahmen
(2020–2030) „gering“ (AB98). Stärkster Treiber ist die Stufe ohne Anpassung: „gering“ ist schon die niedrigste Stufe der
Skala. Tabelle 5 ergibt aus der Zeile „Gering (1)“ für jede Wirksamkeit von 0 bis 2 einen Wert von 1 oder darunter, also
„gering“. Keine vollständige Selbsteinschätzung ändert deshalb das Wort; die Summe entscheidet nur über den Zusatz aus (d).

| Summe für #96 | 0–2 | 3–5 | 6–8 | 9–11 | 12 |
|---|---|---|---|---|---|
| Wirksamkeit nach Summentabelle | 0 | 0,5 | 1 | 1,5 | 2 |
| im Rahmen 0,5–1 | 0,5 | 0,5 | 1 | 1 | 1 |
| Tabelle 5 | 0,5 | 0,5 | 0 | 0 | 0 |
| Stufe mit Anpassung | gering (Tabelle 5: 0,5) | gering (Tabelle 5: 0,5) | gering (Tabelle 5: 0) | gering (Tabelle 5: 0) | gering (Tabelle 5: 0) |

Was das für die Kommune heißt: Ihre Anpassung reicht für die Gegenwart rechnerisch unter die niedrigste Stufe, schon mit
den Bundesmaßnahmen allein (Untergrenze 0,5). Das ist keine Aussage über die Zukunft. Ohne Anpassung steigt #96 zur Mitte
des Jahrhunderts auf „mittel“ (O98) und „hoch“ (P98); diese Stufen bleiben im Bericht sichtbar (Bericht 96, Abschnitt
„Risiko ohne (weitere) Anpassung“ (c)), und Regel A rechnet sie nicht um ((a)).

**Gegenabgleich #96.** Tabelle 5 auf die bundesweite Wirksamkeit angewandt, verglichen mit der Restrisiko-Zelle der Mappe
(dieselben fünf Paare wie für #95 unter (e)):

| Paar | ohne Anpassung | − Wirksamkeit | = Tabelle 5 | Restrisiko der Mappe | trifft |
|---|---|---|---|---|---|
| Gegenwart / 2020–2030, beschlossen | N98 gering (1) | W98 gering-mittel (0,5) | 0,5, ohne Wort | AB98 gering | erst mit (d) |
| Mitte optim., beschlossen | O98 mittel (2) | X98 mittel (1) | 1 gering | AC98 gering | ja |
| Mitte pessim., beschlossen | P98 hoch (3) | Y98 mittel (1) | 2 mittel | AD98 mittel | ja |
| Mitte optim., weiterreichend | O98 mittel (2) | Z98 mittel (1) | 1 gering | AE98 gering | ja |
| Mitte pessim., weiterreichend | P98 hoch (3) | AA98 mittel (1) | 2 mittel | AF98 mittel | ja |

**Erklärung der Abweichung im ersten Paar.** Gemessen ist 1 − 0,5 = 0,5, die KWRA führt in AB98 „gering“. Das ist eine
Grenze der Skala, keine andere Bewertung. Die Skala des Klimarisikos beginnt bei 1 (gering); für 0,5 hat Tabelle 5 kein
Wort (Fußnote zu Tabelle 5, S. 29). Die KWRA rechnet den Bundesmaßnahmen die halbe Stufe zu (W98 „gering-mittel“;
„‚gering-mittel‘ würde eine Reduzierung um eine halbe Stufe bedeuten“, TB6 S. 112), kann das Ergebnis aber nicht tiefer
als „gering“ führen. Festlegung (d) liest den Wert ebenso: „gering“ mit dem Zusatz „rechnerisch unter der niedrigsten
Stufe (Tabelle 5: 0,5)“. Das Paar ist eines der 14, die erst mit (d) treffen (ID 96 in der Liste unter (e)). Die übrigen
vier Paare treffen ohne weiteres. Regel A muss deshalb für #96 nicht geändert werden.

**Euro-Betrag ohne und mit Maßnahmen nach Regel D (#96, Berlin).** Ohne weitere Anpassung trägt #96 in Berlin
408.106 Tage × 6,20 € = 2,53 Mio. € je Jahr (Preisstand 2024; Bericht 96 §3.0 Ebene 10, Zustand nach Kapitel 1,
Abschnitt „Risiko ohne (weitere) Anpassung“ (a)). Mit der Pollen-Frühwarnung S158, ganze Stadt im Geltungsbereich, fallen
9.182 Tage × 6,20 € ≈ 56.900 € je Jahr weg, 2,25 % des Betrags; das ist eine Abschätzung von KAP3 nach Vorgabe P2
(Bericht 96 §5.1, Tabelle „Beispielkommune Berlin“, Schritte 4 und 5). Es bleiben 2,53 Mio. € − 56.900 € = 2,47 Mio. €
je Jahr. Dass der Zelllauf des Produkts ohne Maßnahme ebenfalls 2,47 Mio. € ergibt (§3.0), ist ein Zufall der Rundung;
die beiden Zahlen hängen nicht zusammen. Die allergenarme Stadtbaumwahl hat in Kapitel 5 keinen Berliner Betrag, weil sie
an der Änderung des Kronenanteils je Zelle hängt; das Rechenbeispiel dort (vier Zellen, 8.000 Betroffene) ergibt 637 Tage
und ≈ 3.950 € weniger je Jahr (Kapitel 5, Hebel „Allergenarme Stadtbaumwahl“, Schritt 9). Die Selbsteinschätzung aus
Ebene 3 ändert keinen der Beträge (Regel D, Punkt 2), und die gewählten Maßnahmen ändern die Stufe nicht. Führt die
Kommune ihre Warnkette in der Selbsteinschätzung, wirkt dieselbe Warnung auf jeder Skala einmal: im Euro-Betrag als
Hebel S158, in der Stufe über die Summe (Regel D, „Warum nichts doppelt zählt“).

Beispiel-Block `rechenkette_klimarisiko_mit_anpassung_96`, aus dem Stamm des Produkt-Repos ausführbar (am 09.10.2026
gelaufen, Ausgabe darunter):

```python
# rechenkette_klimarisiko_mit_anpassung_96 — Regel A und Regel D an #96 nachgerechnet
import openpyxl

RISIKO = {"gering": 1.0, "mittel": 2.0, "hoch": 3.0}  # Broschüre Tabelle 5, S. 29
WIRKSAMKEIT = {"gering": 0.0, "gering-mittel": 0.5, "mittel": 1.0, "mittel-hoch": 1.5, "hoch": 2.0}  # ebenda
STUFE = {1.0: "gering", 1.5: "gering-mittel", 2.0: "mittel", 2.5: "mittel-hoch", 3.0: "hoch"}  # TB6 S. 112


def wirksamkeit_aus_summe(summe):
    """Ebene 5: je drei Punkte eine halbe Stufe, abgerundet (Abschätzung von KAP3)."""
    assert 0 <= summe <= 12
    return (summe // 3) * 0.5


def tabelle_5(ohne, wirksamkeit):
    """Ebene 9: ohne Anpassung minus Wirksamkeit, unten bei 0 abgeschnitten."""
    return max(0.0, ohne - wirksamkeit)


def stufe(wert):
    """Ebene 10: Werte unter 1 heißen „gering“, mit Zusatz (Festlegung d)."""
    if wert < 1:
        return f"gering (Tabelle 5: {wert:g})"
    return STUFE[wert]


ws = openpyxl.load_workbook("docs/KWAR/KWRA-2021_Klimawirkungen.xlsx", data_only=True)["Klimawirkungen"]
assert (ws["N2"].value, ws["W2"].value) == ("Risiko o. Anp. – Gegenwart", "Wirksamkeit APA III – 2020–2030")
assert (ws["Z2"].value, ws["AA2"].value) == ("Wirksamkeit weiterr. – Mitte optim.", "Wirksamkeit weiterr. – Mitte pessim.")

# Ebenen 1 und 2
zeile = next(r for r in range(3, ws.max_row + 1) if ws.cell(r, 1).value == 96)
assert zeile == 98 and ws["V98"].value == "ja"
assert ws["D98"].value == "Allergische Reaktionen durch Aeroallergene pflanzlicher Herkunft"
ohne = RISIKO[ws["N98"].value]

# Ebenen 3 bis 5 (Selbsteinschätzung als Beispiel)
beispiel = {"organisation": 2, "technik": 2, "finanzen": 1, "oekosystem": 2}
summe = sum(beispiel.values())
eigen = wirksamkeit_aus_summe(summe)

# Ebenen 6 bis 8
unten = WIRKSAMKEIT[ws["W98"].value]
oben = max(WIRKSAMKEIT[ws["Z98"].value], WIRKSAMKEIT[ws["AA98"].value])
wirk = min(max(eigen, unten), oben)

# Ebenen 9 und 10
wert = tabelle_5(ohne, wirk)
print("ohne:", ws["N98"].value, ohne, "| Summe:", summe, "| eigen:", eigen, "| Rahmen:", unten, oben,
      "| Wirksamkeit:", wirk, "| Tabelle 5:", wert, "| mit Anpassung:", stufe(wert),
      "| Engpass:", min(beispiel, key=beispiel.get), "| bundesweit AB98:", ws["AB98"].value)
assert (ohne, summe, eigen, unten, oben, wirk, wert) == (1.0, 7, 1.0, 0.5, 1.0, 1.0, 0.0)
assert stufe(wert) == "gering (Tabelle 5: 0)"

# Stufe mit Anpassung für #96 je Summe 0 bis 12: das Wort bleibt „gering“, nur der Zusatz wechselt
je_summe = {s: stufe(tabelle_5(ohne, min(max(wirksamkeit_aus_summe(s), unten), oben))) for s in range(13)}
print("je Summe:", je_summe)
assert all(je_summe[s] == ("gering (Tabelle 5: 0.5)" if s < 6 else "gering (Tabelle 5: 0)") for s in range(13))

# Gegenabgleich: Tabelle 5 auf die bundesweite Wirksamkeit, Zeile 98
PAARE = (("N", "W", "AB"), ("O", "X", "AC"), ("P", "Y", "AD"), ("O", "Z", "AE"), ("P", "AA", "AF"))
abgleich = []
for o, w, rr in PAARE:
    roh = tabelle_5(RISIKO[ws[f"{o}98"].value], WIRKSAMKEIT[ws[f"{w}98"].value])
    wort = STUFE[max(1.0, roh)]
    abgleich.append((f"{o}98", f"{w}98", roh, f"{rr}98", ws[f"{rr}98"].value, roh in STUFE, wort == ws[f"{rr}98"].value))
print("Gegenabgleich (ohne, Wirksamkeit, Tabelle 5, Restrisiko, Zelle, Wort ohne (d), trifft mit (d)):", abgleich)
assert [a[2] for a in abgleich] == [0.5, 1.0, 2.0, 1.0, 2.0]
assert [a[5] for a in abgleich] == [False, True, True, True, True] and all(a[6] for a in abgleich)

# Regel D: Euro-Betrag Berlin ohne und mit S158 (Bericht 96 §3.0 Ebene 10, §5.1); die Kapazität wirkt auf keinen Betrag
TAGE, C_TAG = 408106, 6.20           # §3.0 Ebenen 8 bis 10
VERMIEDEN = 9182                      # §5.1, Tabelle „Beispielkommune Berlin“, Schritt 4
s_ohne = TAGE * C_TAG
s158 = VERMIEDEN * C_TAG
print("ohne:", round(s_ohne), "| S158:", round(s158), "| mit S158:", round(s_ohne - s158),
      "| Anteil S158:", round(s158 / s_ohne, 4))
assert (round(s_ohne / 1e6, 2), round(s158, -2), round((s_ohne - s158) / 1e6, 2)) == (2.53, 56900, 2.47)
```

Ausgabe:

```
ohne: gering 1.0 | Summe: 7 | eigen: 1.0 | Rahmen: 0.5 1.0 | Wirksamkeit: 1.0 | Tabelle 5: 0.0 | mit Anpassung: gering (Tabelle 5: 0) | Engpass: finanzen | bundesweit AB98: gering
je Summe: {0: 'gering (Tabelle 5: 0.5)', 1: 'gering (Tabelle 5: 0.5)', 2: 'gering (Tabelle 5: 0.5)', 3: 'gering (Tabelle 5: 0.5)', 4: 'gering (Tabelle 5: 0.5)', 5: 'gering (Tabelle 5: 0.5)', 6: 'gering (Tabelle 5: 0)', 7: 'gering (Tabelle 5: 0)', 8: 'gering (Tabelle 5: 0)', 9: 'gering (Tabelle 5: 0)', 10: 'gering (Tabelle 5: 0)', 11: 'gering (Tabelle 5: 0)', 12: 'gering (Tabelle 5: 0)'}
Gegenabgleich (ohne, Wirksamkeit, Tabelle 5, Restrisiko, Zelle, Wort ohne (d), trifft mit (d)): [('N98', 'W98', 0.5, 'AB98', 'gering', False, True), ('O98', 'X98', 1.0, 'AC98', 'gering', True, True), ('P98', 'Y98', 2.0, 'AD98', 'mittel', True, True), ('O98', 'Z98', 1.0, 'AE98', 'gering', True, True), ('P98', 'AA98', 2.0, 'AF98', 'mittel', True, True)]
ohne: 2530257 | S158: 56928 | mit S158: 2473329 | Anteil S158: 0.0225
```

**#98 UV-bedingte Gesundheitsschädigungen (insbesondere Hautkrebs) (Schritt 3).** Dieselbe Regel, Werte aus Zeile 100
der Mappe. Die Kommune stuft die vier Komponenten für diese Klimawirkung ein, etwa: Zuständigkeit und UV-Schutz in Kitas,
Schulen und Freibädern (Organisation), UV-Index-Hinweise (Technik), Mittel dafür (Finanzen), Schatten durch Bäume und
Sonnensegel (Ökosystem). Das Beispiel liegt unter der Summe 6, damit beide Fälle des Rahmens einmal vorkommen (#96 darüber).

| Ebene | Rechenschritt | Wert (#98, Beispielkommune) | Quelle |
|---|---|---|---|
| 1 | Klimawirkung → Zeile der Mappe (Spalte A = 98) | Zeile 100; D100 „UV-bedingte Gesundheitsschädigungen (insbesondere Hautkrebs)“; V100 „ja“ | Mappe A100, D100, V100 |
| 2 | Stufe ohne Anpassung, Gegenwart (Kopf N2 „Risiko o. Anp. – Gegenwart“) → Zeile von Tabelle 5 | mittel = 2 | Mappe N100; Broschüre Tabelle 5, S. 29 |
| 3 | Selbsteinschätzung der vier Komponenten für #98, **Beispiel, keine Messung** | Organisation 2, Technik 1, Finanzen 1, Ökosystem 1 | Komponenten nach Fußnote 32, S. 29; Stufen `REIFEGRADE` |
| 4 | Summe der vier Reifegrade | 2 + 1 + 1 + 1 = 5 | Rechnung |
| 5 | Summe → Wirksamkeit der Kommune (Summentabelle) | 5 → gering-mittel = 0,5 | Festlegung (c), Abschätzung von KAP3 |
| 6 | Untergrenze: Wirksamkeit der beschlossenen Maßnahmen 2020–2030 (Kopf W2) | gering-mittel = 0,5 | Mappe W100; TB6 S. 112 |
| 7 | Obergrenze: höherer Wert aus weiterreichender Anpassung, Mitte des Jahrhunderts 2031–2060 (Köpfe Z2, AA2) | mittel = 1 und mittel = 1 → 1 | Mappe Z100, AA100; TB6 S. 112 |
| 8 | Wirksamkeit im Rahmen: nicht unter Ebene 6, nicht über Ebene 7 | 0,5 bleibt 0,5 (gering-mittel) | Festlegung (e) |
| 9 | Tabelle 5: Zeile „Mittel (2)“, Spalte „Gering-mittel (0,5)“ | 2 − 0,5 = 1,5 | Broschüre Tabelle 5, S. 29 |
| 10 | Wert → Stufe mit Anpassung | 1,5 = **gering-mittel** | Festlegung (b) |

Neben der Stufe, nicht in der Rechnung: Technik, Finanzen und Ökosystem stehen je auf 1, es fehlt also mehr als eine Art
von Anpassung (Broschüre S. 29); bundesweit nach den beschlossenen Maßnahmen (2020–2030) „gering-mittel“ (AB100), gleich
der Stufe der Beispielkommune, weil ihre Summe nicht über die Untergrenze hinausreicht. Stärkster Treiber ist die Stufe
ohne Anpassung („mittel“). Der Rahmen lässt der Selbsteinschätzung eine halbe Stufe Spielraum: Ein Punkt mehr in einer
beliebigen Komponente (Summe 6) senkt die Stufe auf „gering“.

| Summe für #98 | 0–2 | 3–5 | 6–8 | 9–11 | 12 |
|---|---|---|---|---|---|
| Wirksamkeit nach Summentabelle | 0 | 0,5 | 1 | 1,5 | 2 |
| im Rahmen 0,5–1 | 0,5 | 0,5 | 1 | 1 | 1 |
| Stufe mit Anpassung | gering-mittel | gering-mittel | gering | gering | gering |

**Gegenabgleich #98.** Alle fünf Paare treffen ohne (d):

| Paar | ohne Anpassung | − Wirksamkeit | = Tabelle 5 | Restrisiko der Mappe | trifft |
|---|---|---|---|---|---|
| Gegenwart / 2020–2030, beschlossen | N100 mittel (2) | W100 gering-mittel (0,5) | 1,5 gering-mittel | AB100 gering-mittel | ja |
| Mitte optim., beschlossen | O100 mittel (2) | X100 gering-mittel (0,5) | 1,5 gering-mittel | AC100 gering-mittel | ja |
| Mitte pessim., beschlossen | P100 hoch (3) | Y100 gering-mittel (0,5) | 2,5 mittel-hoch | AD100 mittel-hoch | ja |
| Mitte optim., weiterreichend | O100 mittel (2) | Z100 mittel (1) | 1 gering | AE100 gering | ja |
| Mitte pessim., weiterreichend | P100 hoch (3) | AA100 mittel (1) | 2 mittel | AF100 mittel | ja |

**Euro-Betrag ohne und mit Maßnahmen nach Regel D (#98, Berlin).** Ohne weitere Anpassung trägt #98 in Berlin
11,68 Mio. € je Jahr (Preisstand 2024; Bericht 98 §3.0 Ebene 10, Zustand nach Kapitel 1, Abschnitt „Risiko ohne
(weitere) Anpassung“ (a)). Mit UV-Schutz im öffentlichen Raum und Kommunikation (S155) sind es nach vollem Einlauf
11,68 Mio. € − 252.500 € = 11,43 Mio. € je Jahr; die 252.500 € (2,2 %, Band 70.100–631.200 €) sind eine Abschätzung von
KAP3 (Bericht 98 Kapitel 5, Hebel „UV-Schutz im öffentlichen Raum und Kommunikation (S155)“, Tabelle „Beispiel Berlin“).
Die Wirkung läuft über Jahrzehnte ein: Nach 10 Jahren werden 34.700 € angerechnet, es bleiben 11,65 Mio. € je Jahr
(ebenda, Tabelle „angerechnet nach“). Die Förderung der Früherkennung (S158) hat keinen eigenen Betrag, sondern den Vermerk
„Kostenwirkung im Basiswert voll angerechnet“ (Kapitel 5, Hebel „Förderung der Früherkennung (S158)“). Die
Selbsteinschätzung aus Ebene 3 ändert keinen der Beträge (Regel D, Punkt 2); sie senkt allein die Stufe von „mittel“ auf
„gering-mittel“ (Ebenen 2 und 10). Schatten und UV-Index-Hinweise, nach denen die Selbsteinschätzung fragt, sind dieselben
Maßnahmen, die S155 in Euro rechnet; eine Minderung des Betrags aus der Kapazität zöge sie ein zweites Mal ab (Regel D,
Grund 2).

Beispiel-Block `rechenkette_klimarisiko_mit_anpassung_98`, aus dem Stamm des Produkt-Repos ausführbar (am 09.10.2026
gelaufen, Ausgabe darunter):

```python
# rechenkette_klimarisiko_mit_anpassung_98 — Regel A und Regel D an #98 nachgerechnet
import openpyxl

RISIKO = {"gering": 1.0, "mittel": 2.0, "hoch": 3.0}  # Broschüre Tabelle 5, S. 29
WIRKSAMKEIT = {"gering": 0.0, "gering-mittel": 0.5, "mittel": 1.0, "mittel-hoch": 1.5, "hoch": 2.0}  # ebenda
STUFE = {1.0: "gering", 1.5: "gering-mittel", 2.0: "mittel", 2.5: "mittel-hoch", 3.0: "hoch"}  # TB6 S. 112


def wirksamkeit_aus_summe(summe):
    """Ebene 5: je drei Punkte eine halbe Stufe, abgerundet (Abschätzung von KAP3)."""
    assert 0 <= summe <= 12
    return (summe // 3) * 0.5


def tabelle_5(ohne, wirksamkeit):
    """Ebene 9: ohne Anpassung minus Wirksamkeit, unten bei 0 abgeschnitten."""
    return max(0.0, ohne - wirksamkeit)


def stufe(wert):
    """Ebene 10: Werte unter 1 heißen „gering“, mit Zusatz (Festlegung d)."""
    if wert < 1:
        return f"gering (Tabelle 5: {wert:g})"
    return STUFE[wert]


ws = openpyxl.load_workbook("docs/KWAR/KWRA-2021_Klimawirkungen.xlsx", data_only=True)["Klimawirkungen"]
assert (ws["N2"].value, ws["W2"].value) == ("Risiko o. Anp. – Gegenwart", "Wirksamkeit APA III – 2020–2030")
assert (ws["Z2"].value, ws["AA2"].value) == ("Wirksamkeit weiterr. – Mitte optim.", "Wirksamkeit weiterr. – Mitte pessim.")

# Ebenen 1 und 2
zeile = next(r for r in range(3, ws.max_row + 1) if ws.cell(r, 1).value == 98)
assert zeile == 100 and ws["V100"].value == "ja"
assert ws["D100"].value == "UV-bedingte Gesundheitsschädigungen (insbesondere Hautkrebs)"
ohne = RISIKO[ws["N100"].value]

# Ebenen 3 bis 5 (Selbsteinschätzung als Beispiel)
beispiel = {"organisation": 2, "technik": 1, "finanzen": 1, "oekosystem": 1}
summe = sum(beispiel.values())
eigen = wirksamkeit_aus_summe(summe)

# Ebenen 6 bis 8
unten = WIRKSAMKEIT[ws["W100"].value]
oben = max(WIRKSAMKEIT[ws["Z100"].value], WIRKSAMKEIT[ws["AA100"].value])
wirk = min(max(eigen, unten), oben)

# Ebenen 9 und 10
wert = tabelle_5(ohne, wirk)
print("ohne:", ws["N100"].value, ohne, "| Summe:", summe, "| eigen:", eigen, "| Rahmen:", unten, oben,
      "| Wirksamkeit:", wirk, "| Tabelle 5:", wert, "| mit Anpassung:", stufe(wert),
      "| bundesweit AB100:", ws["AB100"].value)
assert (ohne, summe, eigen, unten, oben, wirk, wert, stufe(wert)) == (2.0, 5, 0.5, 0.5, 1.0, 0.5, 1.5, "gering-mittel")

# Stufe mit Anpassung für #98 je Summe 0 bis 12
je_summe = {s: stufe(tabelle_5(ohne, min(max(wirksamkeit_aus_summe(s), unten), oben))) for s in range(13)}
print("je Summe:", je_summe)
assert all(je_summe[s] == ("gering-mittel" if s < 6 else "gering") for s in range(13))

# Gegenabgleich: Tabelle 5 auf die bundesweite Wirksamkeit, Zeile 100
PAARE = (("N", "W", "AB"), ("O", "X", "AC"), ("P", "Y", "AD"), ("O", "Z", "AE"), ("P", "AA", "AF"))
abgleich = []
for o, w, rr in PAARE:
    roh = tabelle_5(RISIKO[ws[f"{o}100"].value], WIRKSAMKEIT[ws[f"{w}100"].value])
    abgleich.append((f"{o}100", f"{w}100", roh, f"{rr}100", ws[f"{rr}100"].value, STUFE.get(roh) == ws[f"{rr}100"].value))
print("Gegenabgleich (ohne, Wirksamkeit, Tabelle 5, Restrisiko, Zelle, trifft ohne (d)):", abgleich)
assert [a[2] for a in abgleich] == [1.5, 1.5, 2.5, 1.0, 2.0] and all(a[5] for a in abgleich)

# Regel D: Euro-Betrag Berlin ohne und mit S155 (Bericht 98 §3.0 Ebene 10, Kapitel 5); die Kapazität wirkt auf keinen Betrag
S_OHNE = 11.68e6                      # € je Jahr (Preisstand 2024), §3.0 Ebene 10
S155_VOLL, S155_10J = 252_500, 34_700  # Kapitel 5, Hebel S155, Beispiel Berlin
print("ohne:", S_OHNE, "| S155 voll:", S155_VOLL, "| mit S155 voll:", S_OHNE - S155_VOLL,
      "| nach 10 Jahren:", S_OHNE - S155_10J, "| Anteil S155:", round(S155_VOLL / S_OHNE, 4))
assert (round((S_OHNE - S155_VOLL) / 1e6, 2), round((S_OHNE - S155_10J) / 1e6, 2)) == (11.43, 11.65)
```

Ausgabe:

```
ohne: mittel 2.0 | Summe: 5 | eigen: 0.5 | Rahmen: 0.5 1.0 | Wirksamkeit: 0.5 | Tabelle 5: 1.5 | mit Anpassung: gering-mittel | bundesweit AB100: gering-mittel
je Summe: {0: 'gering-mittel', 1: 'gering-mittel', 2: 'gering-mittel', 3: 'gering-mittel', 4: 'gering-mittel', 5: 'gering-mittel', 6: 'gering', 7: 'gering', 8: 'gering', 9: 'gering', 10: 'gering', 11: 'gering', 12: 'gering'}
Gegenabgleich (ohne, Wirksamkeit, Tabelle 5, Restrisiko, Zelle, trifft ohne (d)): [('N100', 'W100', 1.5, 'AB100', 'gering-mittel', True), ('O100', 'X100', 1.5, 'AC100', 'gering-mittel', True), ('P100', 'Y100', 2.5, 'AD100', 'mittel-hoch', True), ('O100', 'Z100', 1.0, 'AE100', 'gering', True), ('P100', 'AA100', 2.0, 'AF100', 'mittel', True)]
ohne: 11680000.0 | S155 voll: 252500 | mit S155 voll: 11427500.0 | nach 10 Jahren: 11645300.0 | Anteil S155: 0.0216
```

## Ergebnis für M0

Regel A auf die drei Klimawirkungen von M0 angewandt. Die Stufe gilt für die Beispiel-Selbsteinschätzung des jeweiligen
Blocks; für eine echte Kommune rechnet das Produkt mit ihrer eigenen. Was jede vollständige Selbsteinschätzung ergibt,
steht in der Stufe „je Summe“. Der Rahmen der Wirksamkeit ist bei allen drei derselbe, 0,5–1 (W, Z und AA der Mappe).

| Klimawirkung (Beispiel-Block) | Eingangsstufe | Wirksamkeit | Stufe mit Anpassung | Kennzeichnung |
|---|---|---|---|---|
| #95 Hitzebelastung (`rechenkette_klimarisiko_mit_anpassung_95`) | hoch (3), N97 (Ebene 2) | Beispiel 9 Punkte → 1,5, im Rahmen 0,5–1 → mittel (1) (Ebenen 5–8) | **mittel** (Ebene 10); je Summe: 0–5 mittel-hoch, 6–12 mittel | Eingangsstufe: Quelle (Mappe N97). Wirksamkeit und Stufe: Abschätzung von KAP3 (Summentabelle und Rahmen), Werte des Rahmens aus der Quelle (W97, Z97, AA97), Tabelle 5 aus der Quelle (UBA 2022, S. 29). Nicht bestimmbar, solange eine Komponente fehlt. |
| #96 Aeroallergene (`rechenkette_klimarisiko_mit_anpassung_96`) | gering (1), N98 (Ebene 2) | Beispiel 7 Punkte → 1, im Rahmen 0,5–1 → mittel (1) (Ebenen 5–8) | **gering** (Tabelle 5: 0) (Ebene 10); je Summe: 0–5 gering (Tabelle 5: 0,5), 6–12 gering (Tabelle 5: 0) | Eingangsstufe: Quelle (Mappe N98). Wirksamkeit und Zusatz: Abschätzung von KAP3 (Summentabelle und Rahmen), Werte des Rahmens aus der Quelle (W98, Z98, AA98). Das Wort „gering“ hängt an keiner Abschätzung: Es folgt für jede Wirksamkeit von 0 bis 2 aus N98 und Tabelle 5 (UBA 2022, S. 29). Nicht bestimmbar, solange eine Komponente fehlt. |
| #98 UV-Schädigungen (`rechenkette_klimarisiko_mit_anpassung_98`) | mittel (2), N100 (Ebene 2) | Beispiel 5 Punkte → 0,5, im Rahmen 0,5–1 → gering-mittel (0,5) (Ebenen 5–8) | **gering-mittel** (Ebene 10); je Summe: 0–5 gering-mittel, 6–12 gering | Eingangsstufe: Quelle (Mappe N100). Wirksamkeit und Stufe: Abschätzung von KAP3 (Summentabelle und Rahmen), Werte des Rahmens aus der Quelle (W100, Z100, AA100), Tabelle 5 aus der Quelle (UBA 2022, S. 29). Nicht bestimmbar, solange eine Komponente fehlt. |

Kein Euro-Betrag in dieser Tabelle: Nach Regel D wirkt die Selbsteinschätzung auf keinen Betrag. Die Beträge ohne und
mit Maßnahmen stehen unter dem jeweiligen Beispiel-Block, alle für Berlin, Preisstand 2024: #95 362,9 und 340,8 Mio. €,
#96 2,53 und 2,47 Mio. €, #98 11,68 und nach vollem Einlauf 11,43 Mio. € je Jahr. Alle drei Klimawirkungen gehören zu
den 9 Zeilen mit einem Rahmen von einer halben Stufe; sichtbar wird er bei #95 und #98, bei #96 nicht ((c), „Richtung und
Größe der möglichen Verzerrung“).

## Entscheidungslog

Gewählt ist Regel A. Der Vorschlag des CEO (qualitativ, ohne Euro-Betrag, mit Seite) ist darin im Kern gewählt und
steht deshalb nicht unter den verworfenen Ansätzen.

Verworfen, je mit einem Satz:

1. **Engpassregel (`REGEL_GESAMTSTUFE`) als Wirksamkeit:** verworfen, weil nur die schwächste der vier Angaben wirkt und
   eine einzige Komponente auf 0 die ganze Wirksamkeit auf 0 setzt, im Beispiel aus (c) (3/3/3/0) für #95 mit der Stufe
   „mittel-hoch“ statt „mittel“.
2. **Minderungssätze ohne Bezug auf ein Klimarisiko:** in der heutigen Form verworfen, weil sie neben der Stufe aus
   Regel A eine zweite, möglicherweise widersprüchliche Aussage über „das Klimarisiko“ machen; sie werden nach (g) neu
   gefasst.
3. **Tabelle 5 allein mit der Selbsteinschätzung, ohne Grenzen:** verworfen, weil sie für #95 bei der Summe 12 eine Stufe
   zu günstig („gering“ statt höchstens „mittel“) und bei der Summe 0–2 eine halbe Stufe ungünstiger als das bundesweite
   Restrisiko einstuft.
4. **Bundesweite und kommunale Wirksamkeit addieren:** verworfen, weil die weiterreichende Anpassung der KWRA andere
   Akteure als den Bund einschließt (TB6 S. 112) und dieselbe Anpassung dann zweimal zählte.
5. **Restrisiko der KWRA (Spalte AB) unverändert übernehmen:** verworfen, weil dann die Selbsteinschätzung der Kommune
   auf die Stufe nicht wirkte und Abschnitt 2.2.5 die Kombination mit der Anpassungskapazität verlangt (S. 29).
6. **Zeitscheibe Mitte (Spalte O oder P) als Eingang:** verworfen, weil die heutige Selbsteinschätzung dann gegen ein
   Risiko von 2031–2060 liefe, für das die KWRA die Wirksamkeit eigens neu eingeschätzt hat (TB6 S. 112).
7. **Kaufmännisch runden statt abrunden:** verworfen, weil eine Summe von 5 Punkten dann eine volle Stufe Minderung
   ergäbe und die Stufe mit Anpassung zu günstig ausfiele.
8. **Mittelwert mit Deckel „höchstens Engpass plus eine Stufe“:** verworfen, weil er eine zweite Regel ohne Fundstelle
   einführt, die der Sachbearbeiter zusätzlich nachschlagen müsste.
9. **Werte 0 und 0,5 als eigene Stufe („sehr gering“ oder „kein Risiko“):** verworfen, weil Tabelle 5 dafür kein Wort
   hat, die KWRA „gering“ führt und „kein Risiko“ die Lage zu günstig darstellte.
10. **„Nicht bestimmbar“ für alle Klimawirkungen ohne analysierte Anpassungskapazität:** verworfen, weil Vorgabe P2
    eine begründete Abschätzung verlangt und die Grenzen aus den 33 analysierten Zeilen abschätzbar sind.
11. **Einstufung einmal je Kommune für alle Klimawirkungen:** verworfen, weil Tabelle 5 und die KWRA die Wirksamkeit je
    Klimawirkung führen und eine Fähigkeit, die für eine Klimawirkung viel und für eine andere wenig beiträgt, sonst
    überall mit demselben Wert einginge.

**Schritt 2 (T-1896-methodik_manager).** Gewählt sind Definition P und Regel D: Die Anpassungskapazität wirkt nur auf
die Stufe, nicht auf den Euro-Betrag. Regel A bleibt unverändert; kein Befund dieses Schritts erzwingt eine Änderung.
Verworfen, je mit einem Satz:

12. **Die Kapazität mindert den Euro-Betrag zusätzlich zu den Maßnahmen:** verworfen, weil die Selbsteinschätzung keine
    Effektgröße hat (Grund 1) und ihre Fähigkeiten dieselben Maßnahmen sind, die Kapitel 5 schon als Hebel abzieht
    (Grund 2; in Berlin fielen so weitere 113,6 Mio. € je Jahr weg); das Gegenargument, dass der Basiswert nur den
    Bestand im Mittel Deutschlands enthält und der Vorsprung eines älteren Programms deshalb im Betrag fehlt, trifft zu,
    ändert die Entscheidung aber nicht, weil die Selbsteinschätzung auch diesen Vorsprung nicht in Euro messen kann
    (Grund 1) und eine Minderung aus ihr zugleich jede neu gewählte Maßnahme ein zweites Mal träfe (Grund 2).
13. **Die Kapazität ersetzt die Maßnahmenwahl im Euro-Betrag (Betrag mit Anpassung aus der Stufe):** verworfen, weil
    Tabelle 5 keine Euro-Skala hat und jeder Umrechnungsfaktor von Stufe in Euro ohne Quelle wäre.
14. **Das Anpassungspotenzial als eigene Faktorformel neben dem Euro-Pfad (heutiger Stand):** verworfen, weil derselbe
    Wert dann an zwei Stellen steht und Hebel mit eigenem Zweig still mit null zählen, in Berlin 12,45 Mio. € je Jahr.
15. **Das Anpassungspotenzial je Risiko-Code statt je Klimawirkung:** verworfen, weil die KWRA Klimawirkungen den
    Gruppen zuordnet (TB6 S. 141) und #95 sonst zwei Gruppen haben könnte.
16. **Das Anpassungspotenzial aus der bundesweiten Wirksamkeit der KWRA (Spalten W, Z und AA):** verworfen, weil es dann
    für alle Kommunen gleich wäre, die Maßnahmen des Katalogs nicht sähe und die Schwellen in `querschnitt_gewissheit.md`
    auf die Minderung durch die Katalogmaßnahmen bezogen sind.
17. **Das Anpassungspotenzial aus der Stufe der Kommune (Wirksamkeit geteilt durch Stufe ohne Anpassung):** verworfen,
    weil es dann die Kapazität ein zweites Mal ausdrückte und die Charakterisierung Regel A wiederholte.
18. **Das Anpassungspotenzial zusätzlich vom Euro-Betrag abziehen:** verworfen, weil es aus denselben Hebeln besteht,
    die den Betrag mit Maßnahmen schon senken.
19. **Ohne Kommune den Wert der Beispielkommune zeigen (Berlin 0,096):** verworfen, weil die Hebel an den Altersbändern
    dann für jede Kommune mit dem Altersaufbau Berlins gälten, was Bericht 95 für S157 schon verwirft (Befunde 183 und
    214).
20. **Ohne Kommune „nicht bestimmbar“:** verworfen, weil der Hitzeaktionsplan auch ohne Kommune einen festen Anteil der
    Mortalität wegnimmt und eine Untergrenze mit Vermerk mehr sagt als keine Zahl (P2).
21. **Ohne Kommune den Wert des Risiko-Codes mit dem Hebel ungewichtet nehmen (0,061 je Code wie heute):** verworfen,
    weil der Plan dann auch auf den Anteil der Morbidität zählte, den er nach Kapitel 5 nicht senkt; bei #95 ist das
    unsichtbar (0,0608 statt 0,061), bei einer Klimawirkung, deren Hebel nur einen kleinen Teil des Schadens treffen,
    wäre es ein Vielfaches.

**Schritt 3 (T-1897-methodik_manager).** Regel A, Definition P und Regel D werden auf #96 und #98 angewandt, nicht neu
gefasst. Kein Wert zwingt zu einer Änderung der Regel: #98 trifft den Gegenabgleich in allen fünf Paaren ohne (d), #96 in
vier ohne und im ersten Paar (1 − 0,5 = 0,5, KWRA „gering“) mit (d). Der Beispiel-Block für #95 bleibt deshalb
unverändert. Verworfen, je mit einem Satz:

22. **Für #96 die Selbsteinschätzung weglassen, weil keine vollständige Summe das Wort „gering“ ändert:** verworfen, weil
    (c) eine fehlende Komponente nicht still ersetzt und der Zusatz aus (d) (Tabelle 5: 0,5 oder 0) an der Summe hängt.
23. **Für #96 die Mitte (P98 „hoch“) als Eingang, damit die Selbsteinschätzung sichtbar wirkt:** verworfen aus demselben
    Grund wie Nummer 6; die Stufen zur Mitte bleiben im Bericht sichtbar ((a)).

**Bewusst offen (Gegenprobe Zeile 18, `docs/KONFORMITAET_CHECKLISTE.md`):**

- **A3** „welche Anpassungsmöglichkeiten grundsätzlich bestehen“ (S. 28): Regel A nennt keine Maßnahme. Zuständig: CTO
  (Produktseite Zeile 18, T-1071-ceo).
- **A4** „Bedarf nach zusätzlicher, möglicherweise transformativer Anpassung“ (S. 28): Regel A sagt, wo die Kommune
  steht, nicht, wie viel Anpassung fehlt. Zuständig: CMO (Vorhaben T-1122-cmo).
- **A11** Wechselwirkungen, Synergien und Zielkonflikte zwischen Maßnahmen (S. 29): Regel A betrachtet keine Maßnahme
  einzeln. Zuständig: CMO (Vorhaben T-1122-cmo).
- **A12** „die Grenzen der Klimaanpassung beleuchten“ (S. 29): Die Obergrenze aus (e) ist eine Grenze der Rechnung, keine
  Aussage über Grenzen der Anpassung; die Mappe führt dafür Spalte AI „Grenzen der Anpassung“, für #95 leer (AI97,
  gemessen am 07.10.2026). Zuständig: CMO (Vorhaben T-1122-cmo).

## Befunde an Berichte

**Schritt 3.** Keine Befunde; Bericht 96 und Bericht 98 ändert dieser Schritt nicht. Verglichen am 09.10.2026 mit der
Mappe (SHA-256 unter „Quellen“), Köpfe in Zeile 2:

- **#96, `docs/methodik/96_aeroallergene.md`: keine.** Abschnitt „Risiko ohne (weitere) Anpassung“ (ab Zeile 163),
  Unterabschnitt (c): Gegenwart „gering“ = N98, Mitte optimistisch „mittel“ = O98, Mitte pessimistisch „hoch“ = P98, Ende
  optimistisch „mittel“ = Q98, Ende pessimistisch „hoch“ = R98, Gewissheit Mitte „mittel“ = S98, Ende „mittel“ = T98;
  Fundstelle Zeile 98 = Mappe. Unterabschnitt (b): AB98 „gering“, AC98 „gering“, AD98 „mittel“, AE98 „gering“, AF98
  „mittel“ = Mappe; „Für das Ende des Jahrhunderts führt die Mappe kein Restrisiko“ trifft zu (Köpfe AB2–AF2 nennen nur
  2020–2030 und die Mitte). Kapitel 5 (ab Zeile 1070, mit §5.1) nennt keine Zelle der Mappe; seine Beträge (9.182 Tage
  und ≈ 56.900 €; 637 Tage und ≈ 3.950 € je Jahr) stimmen mit Unterabschnitt (b) überein.
- **#98, `docs/methodik/98_uv_schaedigungen.md`: keine.** Abschnitt „Risiko ohne (weitere) Anpassung“ (ab Zeile 199),
  Unterabschnitt (c): Gegenwart „mittel“ = N100, Mitte „mittel“ und „hoch“ = O100 und P100, Ende „mittel“ und „hoch“ =
  Q100 und R100; Fundstelle Zeile 100, Kopfnamen N2 und R2 wörtlich = Mappe. Unterabschnitt (d): Gewissheit Mitte
  „mittel“ = S100, Ende „sehr gering“ = T100, Kopfnamen S2 und T2 wörtlich = Mappe. Kapitel 5 (ab Zeile 1304) nennt keine
  Zelle der Mappe; S155 mit 252.500 € (Band 70.100–631.200 €; nach 10, 20 und 30 Jahren 34.700, 69.400 und 104.000 €)
  stimmt mit Unterabschnitt (b) überein. Hinweis ohne Befund: Unterabschnitt (b) sagt, der Bericht weise kein Restrisiko
  aus, und nennt die Zellen AB100–AF100 nicht, anders als Bericht 96. Ein Widerspruch zur Mappe ist das nicht; diese
  Datei zeigt die Zellen im Gegenabgleich #98.

**Schritt 2.** Beide Befunde gehen über den CMO weiter (eiserne Regel 5); Code und Bericht 95 ändert dieser Schritt nicht.

- **Befund 1, an den CTO.** `backend/app/services/charakterisierung.py`, `anpassungspotenzial()` (mit `_s157_faktor` und
  `charakterisierungen()`), gegen Definition P. Richtung: Der Code weicht ab. Er rechnet je Risiko-Code mit einer
  eigenen Faktorformel und zählt die Schutzprogramme (r = 0, weil `default_reduction` leer ist) und die Kühlzentren
  nicht mit. Wirkung für #95 in Berlin: \(p\) = 0,064 statt 0,096; die Gruppe (unter 0,1) bleibt, der Abstand zur
  Schwelle ist aber 0,4 Pp. statt 3,6 Pp., und am oberen Bandende der Schutzprogramme läge \(p\) bei mindestens 0,128. Für
  die Morbidität gibt der Code 0,061 statt 0, aus derselben Ursache wie Befund 230 in `reviews/BEFUNDE_95.md`
  (zurückgestellt, CTO, Termin 16.10.2026). Aufrufer: Die Katalogroute (`backend/app/api/routes/catalog.py`, Aufrufe von
  `charakterisierung.charakterisierungen()` in Z. 39 und 83) bleibt ohne Kommune und zeigt \(p_0\) = 0,061 mit einem
  Vermerk für S157, Kühlzentren und Schutzprogramme; heute fehlt jeder Vermerk. Der Interpretationsbericht
  (`interpretationsbericht_fuer_kommune` in `backend/app/services/ergebnis_interpretation_markdown.py`, Z. 281) hat die
  Kommune, reicht sie aber nicht durch und zeigt deshalb auch für Berlin 0,061 statt 0,096. Den Weg „Kommune
  durchreichen, ohne Kommune Vermerk ohne Ersatzwert“ hat der CEO am 06.10.2026 zu Befund 214 entschieden (Folgepaket
  T-1740-ceo); Definition P dehnt den Vermerk auf Kühlzentren und Schutzprogramme aus. Gemessen am 08.10.2026 mit
  `python3 -c "import sys; sys.path.insert(0,'backend'); from app.services import charakterisierung as ch; print(round(ch.anpassungspotenzial('EXPECTED_ANNUAL_MORTALITY'),4), round(ch.anpassungspotenzial('EXPECTED_ANNUAL_MORBIDITY'),4))"`:
  `0.061 0.061`.
- **Befund 2, an das Vorhaben von Bericht 95.** `docs/methodik/95_hitzebelastung.md`, Kapitel 5, Hebel S157, Absätze
  „S157 mit seiner Voreinstellung im Anpassungspotenzial (Befund 149)“ und „\(a_{85+}\) je Kommune (Befund 183)“: Der Bericht
  nennt als Anpassungspotenzial 0,064 aus Hitzeaktionsplan und S157. Nach Definition P zählen Schutzprogramme und
  Kühlzentren mit: Berlin 0,096. Ohne Kommune bleibt es bei 0,061 (Definition P: 0,0608), der Vermerk nennt dann auch
  Kühlzentren und Schutzprogramme. Richtung: Der Bericht beschreibt den heutigen Code. Wirkung: kein Euro-Betrag des
  Berichts ändert sich, nur die Zahl 0,064 und ihr Satz.

**Schritt 1.** Keine. Verglichen wurde `docs/methodik/95_hitzebelastung.md`, Abschnitt „Risiko ohne (weitere) Anpassung“ (ab Zeile 94),
mit der Mappe am 07.10.2026: Gegenwart „hoch“ = N97, Mitte optimistisch „mittel“ = O97, Mitte pessimistisch „hoch“ = P97,
Ende optimistisch „mittel“ = Q97, Ende pessimistisch „hoch“ = R97; Fundstelle Zeile 97, Spalten N–R mit Kopfzellen N2 bis
R2 = Mappe; Gewissheit Mitte „hoch“ = S97, Ende „mittel“ = T97.

## Quellen

- **[Broschüre]** Umweltbundesamt (Hrsg.); Porst, L.; Voß, M.; Kahlenborn, W.; Schauser, I.: Klimarisikoanalysen auf
  kommunaler Ebene – Handlungsempfehlungen zur Umsetzung der ISO 14091. Dessau-Roßlau, Juni 2022.
  https://www.umweltbundesamt.de/system/files/medien/479/publikationen/2022_uba-fachbroschuere_kra_auf_kommunaler_ebene.pdf.
  Lokale Kopie `docs/quellen/normtexte/UBA2022_Klimarisikoanalysen_kommunal_ISO14091.pdf`, SHA-256
  `6c457bc42f467f6258e13c6794dc85f05c3d235886acf693549941564f378745`. Verwendet: S. 18 (Abbildung 3), S. 19 (Zentrale
  Begriffe), S. 28 (Tabelle 4, Abschnitt 2.2.5), S. 29 (Abschnitt 2.2.5, Fußnoten 32–34, Tabelle 5).
- **[TB6]** Umweltbundesamt (Hrsg.): Klimawirkungs- und Risikoanalyse 2021 für Deutschland, Teilbericht 6: Integrierte
  Auswertung – Klimarisiken, Handlungserfordernisse und Forschungsbedarfe. Reihe Climate Change, Dessau-Roßlau, Oktober
  2021. Lokale Kopie `docs/KWAR/kwra2021_teilbericht_6_integrierte_auswertung_bf_211027_0.pdf`, SHA-256
  `e21823b021f3f774331ccd7b3efa086446084ae4781993d6f86fb671d678bc8f`. Verwendet: Kap. 5.1, S. 112–113 (Autoren Porst,
  Kahlenborn); Kap. 6.2 „Charakterisierung der Handlungserfordernisse“, S. 140–141 (Schritt 2).
- **[Bericht 95]** `docs/methodik/95_hitzebelastung.md` (abgenommen), Schritt 2: Kapitel 1, Abschnitt „Risiko ohne
  (weitere) Anpassung“, Absatz (a); §3.0 Rechenkette, Ebenen 8, 9 und 10; §3.5 (Kette Warmsen, 177.406 € je Jahr,
  0,1213 Fälle); Kapitel 5, Hebel „Hitzeaktionsplan / Frühwarnkette (S155/S158)“ (Absätze „Berlin“ und
  „Doppelzählungs-Wächter“), „Gekühlte Räume / Klimaanlagen in Pflegeheimen (S157)“ (Gegenargument (3), Absätze
  „Sensitivität“, „Zusammen mit dem Hitzeaktionsplan (Befund 129)“ und die Absätze zum Anpassungspotenzial, Befunde
  149, 183 und 214), „Öffentliche Kühlzentren“ und „Schutzprogramme vulnerable Gruppen“ (Absätze „Berlin“,
  „Morbidität (Befund 131)“, „Doppelzählungs-Wächter (Befund 150)“, „Kappung 0,794“).
- **[Bericht 96]** `docs/methodik/96_aeroallergene.md`, Schritt 3: Kapitel 1, Abschnitt „Risiko ohne (weitere)
  Anpassung“ (ab Zeile 163), Unterabschnitte (a), (b) und (c); §3.0 Rechenkette, Ebene 10 (408.106 Tage × 6,20 € =
  2,53 Mio. € je Jahr) und Zelllauf (2,47 Mio. €); Kapitel 5 (ab Zeile 1070), Hebel „Allergenarme Stadtbaumwahl“,
  Rechenbeispiel Schritt 9; §5.1 „Wirkungsabschätzung S158 Pollen-Frühwarnung“, Tabelle „Beispielkommune Berlin“,
  Schritte 4 und 5.
- **[Bericht 98]** `docs/methodik/98_uv_schaedigungen.md`, Schritt 3: Kapitel 1, Abschnitt „Risiko ohne (weitere)
  Anpassung“ (ab Zeile 199), Unterabschnitte (a) bis (d); §3.0 Rechenkette, Ebene 10 (11,68 Mio. € je Jahr); Kapitel 5
  (ab Zeile 1304), Hebel „UV-Schutz im öffentlichen Raum und Kommunikation (S155)“ (Tabellen „Beispiel Berlin“ und
  „angerechnet nach“) und „Förderung der Früherkennung (S158)“.
- **[Ledger 95]** `reviews/BEFUNDE_95.md`, Befund 214 (Entscheidung des CEO vom 06.10.2026, Folgepaket T-1740-ceo) und
  Befund 230.
- **[Code]** `backend/app/services/charakterisierung.py` (`anpassungspotenzial`, `_s157_faktor`, `charakterisierungen`),
  `backend/app/services/measure_service.py` (`_reduction_factor`, `_measure_cell_factor`, `build_cost_summary`),
  `backend/app/api/routes/catalog.py` (Z. 39 und 83) und `backend/app/services/ergebnis_interpretation_markdown.py`
  (`interpretationsbericht_fuer_kommune`, Z. 281), gelesen am 08.10.2026 auf dem Stand von `main`.
- **[Mappe]** `docs/KWAR/KWRA-2021_Klimawirkungen.xlsx`, SHA-256
  `70cf6d0090e24b15098f61e5004bf709e91c41cc2b397510499a4cedb8223611`, Blatt „Klimawirkungen“: Kopfzeile 2; Zeile 97
  (#95), Spalten A, D, N–T, U, V, W–AF, AI, AJ (AJ97: „TB 6 Tab. 1 | TB 6 Tab. 22 | …“); für den Gegenabgleich und (f)
  die Spalten N–AF und V aller 102 Zeilen; Schritt 3: Zeilen 98 (#96) und 100 (#98), Spalten A, D, N–T, V und W–AF,
  gelesen am 09.10.2026 mit derselben SHA-256.
