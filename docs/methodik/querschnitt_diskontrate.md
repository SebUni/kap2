# Querschnitt: Diskontrate

Querschnittsdatei der Methodik, gültig für alle Klimawirkungen. Einen Wert bekommen zuerst die Gesundheitsschäden von
M0 (#95, #96, #98). Für die übrigen Schadensarten ruht die Anwendung bis zur Abnahme von M0 (A-0048). Dieser Stand ist
Schritt 1 (Ticket T-1242-methodik_manager, Vorhaben T-1116-cmo) und enthält die Regel und ihre Werte. Schritt 2 bringt
die Rechenkette vom Jahresbetrag zum Barwert mit Beispiel-Block, Schritt 3 und 4 rechnen #96 und #98 nach.

Abkürzungen: **MK 4.0** = Umweltbundesamt, Handbuch Umweltkosten – Methodenkonvention 4.0
(`docs/UBA/UBA_Handbuch Umweltkosten_Methodenkonvention 4.0.pdf`; PDF-Seite und gedruckte Seite stimmen auf S. 4–22
überein); **RZPR** = Reine Zeitpräferenzrate; **Pp.** = Prozentpunkte; **VOLY** = Wert eines verlorenen Lebensjahres,
im Produkt 160.800 € (Preisstand 2024, Bericht 95, Kap. 3.5); **Barwert** = Summe der abgezinsten Jahresbeträge.
Kürzel in eckigen Klammern verweisen auf den Abschnitt „Quellen“.

## Festlegung

**Regel D (Diskontrate).** Die Diskontrate einer Schadensart ist die Summe aus zwei Teilen: der Reinen
Zeitpräferenzrate (RZPR) und der Veränderung der relativen Preise dieser Schadensart. Mit ihr wird jeder Jahresbetrag
in festen Preisen (Preisstand 2024) auf das Bezugsjahr 2025 abgezinst:

> Barwert = Summe der Jahre 2025 bis 2065 von: Jahresbetrag ÷ (1 + Diskontrate) hoch (Jahr − 2025)

Für die Gesundheitsschäden von M0 gilt:

- **RZPR:** 0 % und 1 %, beide werden immer ausgewiesen.
- **Veränderung der relativen Preise:** 0,1 Pp., Band 0–0,7 Pp. Das ist eine Abschätzung von KAP3, gerechnet aus drei
  Quellenwerten.
- **Diskontrate damit:** 0,1 % zur RZPR 0 % und 1,1 % zur RZPR 1 %.

**Fundstelle.** MK 4.0, Kap. 2.2.3, S. 14: „Diese Diskontrate soll zwei Aspekte abbilden: (1) die individuelle oder
gesellschaftliche Zeitpräferenz und (2) die relative Veränderung zwischen heutigen und künftigen Preisen verschiedener
Güter und Dienstleistungen.“ S. 14–15: Die soziale Diskontrate nach Ramsey „kombiniert“ „i) die Reine
Zeitpräferenzrate (RZPR) und ii) das erwartete Konsumwachstum, gewichtet nach seinen Auswirkungen auf den Grenznutzen
der Verbraucher“. S. 10 stellt klar, „dass sich die RZPR von der Diskontrate unterscheidet“. Welche Richtung der zweite
Teil hat, hängt nach S. 15 vom Gut ab: Sinkende relative Preise von Konsumgütern erhöhen „die Diskontrate für diese
Güter“. Für Umweltauswirkungen besteht dagegen „Konsens darüber, dass die relative Verknappung von Ökosystemleistungen
zu relativen Preissteigerungen führt und darum eine niedrigere Diskontrate anzuwenden ist“.

### Die Regel in Worten

Ein Gesundheitsschaden in 30 Jahren zählt aus zwei Gründen anders als ein Schaden heute.

1. **Zeitpräferenz.** Die Gesellschaft kann Heutiges höher gewichten als Künftiges. Wie stark, ist eine Wertentscheidung.
   MK 4.0 gibt dafür zwei Werte vor, 0 % und 1 %.
2. **Relative Preise.** Hier wirken zwei Effekte gegeneinander:
   - *Wohlstandseffekt, hebt die Rate.* Die Menschen haben künftig mehr Einkommen. Ein zusätzlicher Euro ist ihnen dann
     weniger wert als heute. Diesen Effekt beschreibt MK 4.0 als „Konsumwachstum, gewichtet nach seinen Auswirkungen auf
     den Grenznutzen“ (S. 15).
   - *Preiseffekt des Gesundheitsschadens, senkt die Rate.* Wie viel den Menschen die Vermeidung eines
     Gesundheitsschadens wert ist, steigt mit ihrem Einkommen. MK 4.0 legt dafür eine Elastizität von 0,85 fest (S. 22).
     Ein Lebensjahr, das 2045 verloren geht, ist deshalb, in Preisen von 2024 gerechnet, mehr wert als 160.800 €.

   Zusammen: **Veränderung der relativen Preise = Konsumwachstum je Kopf × (Elastizität des Grenznutzens −
   Einkommenselastizität des Schadenswerts).**

Zwei Begriffe kommen darin vor. Die **Elastizität des Grenznutzens** sagt, wie stark der Nutzen eines zusätzlichen Euros
sinkt, wenn das Einkommen steigt. Beim Wert 1,0 ist einem Menschen mit doppeltem Einkommen ein zusätzlicher Euro halb so
viel wert. Die **Einkommenselastizität des Schadenswerts** sagt, um wie viel Prozent die Zahlungsbereitschaft für die
Vermeidung eines Gesundheitsschadens steigt, wenn das Einkommen um 1 % steigt. Beim Wert 0,85 steigt sie bei 10 % mehr
Einkommen um 8,5 %.

**Warum der Preiseffekt in die Diskontrate gehört.** Für Jahre nach 2025 empfiehlt MK 4.0 eine Preisanpassung der
Kostensätze mit dem Verbraucherpreisindex (S. 9). Eine Anpassung an das Einkommen nennt sie dort nicht. Real bleiben
die Kostensätze also gleich. Genau so rechnet das Produkt: jedes Jahr mit derselben VOLY von 160.800 € (Preisstand
2024), und die Jahresbeträge schreibt es nur mit dem Klimasignal fort
(`backend/app/services/cost_projection_service.py`, `project_costs()`). Der steigende Wert der Gesundheit kommt in der
Rechnung sonst nirgends vor. Er gehört in die Diskontrate, sonst fehlt er ganz. Ließe man stattdessen den Wert im
Jahresbetrag steigen und zinste mit RZPR und Wohlstandseffekt ab, käme praktisch derselbe Barwert heraus. MK 4.0
sieht dafür aber die Diskontrate vor (S. 14–15), und die Jahresbeträge des Produkts bleiben dann unverändert lesbar.

### Erste Komponente: Reine Zeitpräferenzrate

MK 4.0, S. 15: „Die reine Zeitpräferenzrate wird jedoch über die Monte Carlo-Läufe hinweg konstant gehalten, und die
Ergebnisse werden für eine RZPR von 0 % und 1 % dargestellt.“ Nach S. 10 spiegelt eine RZPR von 0 % „eine gleiche
Gewichtung des Wohlergehens künftiger und heutiger Generationen“ wider, eine RZPR von 1 % „eine erheblich geringere
Gewichtung des Wohlergehens künftiger Generationen“. Dazu empfiehlt S. 10 „eine Sensitivitätsanalyse mit dem jeweils
anderen Wert“. S. 14 beziffert, was 1 % bedeutet: Vom Nutzen, der in 30 Jahren auftritt, werden nur 74 % berücksichtigt,
von dem in 60 Jahren nur 55 %.

Die beiden Werte sind keine Bandgrenzen, sondern zwei Wertentscheidungen. Das Produkt zeigt immer beide Barwerte
nebeneinander und wählt keinen aus.

### Zweite Komponente: Veränderung der relativen Preise der Gesundheitsschäden

**Was MK 4.0 sagt und was nicht.** Eine Zahl nennt die Konvention nicht. Im GIVE-Modell ist das Konsumwachstum eine
abhängige Größe, „daher ist es nicht möglich, die genaue Diskontrate anzugeben“ (S. 15). Für Gesundheitsschäden nennt
sie auch keine Richtung, nur für Konsumgüter und für Ökosystemleistungen (S. 15). Nach Vorgabe P2 steht deshalb eine
Abschätzung von KAP3 mit Band, keine Null ohne Begründung.

**Herleitung für die Gesundheitsschäden von M0:**

| Schritt | Rechnung | Wert |
|---|---|---|
| 1 | Konsumwachstum je Kopf, Deutschland 2025–2065 | 0,7 % je Jahr |
| 2 | Wohlstandseffekt: Schritt 1 × Elastizität des Grenznutzens 1,0 | + 0,7 Pp. |
| 3 | Preiseffekt: Schritt 1 × Einkommenselastizität des Schadenswerts 0,85 | − 0,595 Pp. |
| 4 | Veränderung der relativen Preise = Schritt 2 + Schritt 3 | 0,105 Pp., gerundet **0,1 Pp.** |

Gerundet wird auf eine Stelle, weil das Konsumwachstum aus der Quelle nur eine Stelle hat. Im Code steht der Wert als
Dezimalzahl 0,001.

**Tabelle der Komponenten:**

| Komponente | Wert | Band | Quelle oder Abschätzung von KAP3 | Größe im Code |
|---|---|---|---|---|
| Reine Zeitpräferenzrate (RZPR) | 0 % und 1 %, beide ausgewiesen | kein Band; zwei Wertentscheidungen, je mit Sensitivität zum anderen Wert (MK 4.0, S. 10) | Quelle: MK 4.0, S. 10 und S. 14–15 | `PURE_TIME_PREFERENCE_RATES` = `(0.0, 0.01)` |
| Veränderung der relativen Preise, Gesundheitsschäden M0 (#95, #96, #98) | 0,1 Pp. | 0–0,7 Pp. | Abschätzung von KAP3: 0,7 % × (1,0 − 0,85), gerechnet aus drei Quellenwerten (Tabelle darunter) | `RELATIVE_PRICE_COMPONENT`, heute `0.0` (Befund C1) |

**Bestandteile der zweiten Komponente:**

| Bestandteil | Wert | Band | Quelle oder Abschätzung von KAP3 | Größe im Code |
|---|---|---|---|---|
| Konsumwachstum je Kopf, Deutschland | 0,7 % je Jahr | 0,4–1,1 % | Abschätzung von KAP3 aus Quellen: Potenzialwachstum 2023–2070 im Mittel 0,7 % je Jahr [SVR, S. 15], Bevölkerung 2022–2070 nahezu gleich [AR, Tabelle 2]; unten 0,4 % [SVR, S. 15], oben 1,1 % [WB] | keine (Befund C2) |
| Elastizität des Grenznutzens | 1,0 | 1,0–1,5 | Quelle: [GB] §2.13 (1,0) und §2.12 (1,3 und 1,5); MK 4.0, S. 16, Rechenbeispiel entspricht 1 | keine (Befund C2) |
| Einkommenselastizität des Schadenswerts | 0,85 | 0,85–1,0 | Quelle: MK 4.0, S. 22 (0,85); 1,0 nach [OECD] Tabelle 0.1, S. 15, und [GB] §2.16 | keine (Befund C2) |

**Konsumwachstum je Kopf, 0,7 % (Band 0,4–1,1 %).** Die Projektion des Sachverständigenrats ergibt für das
Produktionspotenzial von 2023 bis 2070 ein durchschnittliches Wachstum von 0,7 % je Jahr, für die 2020er Jahre 0,4 % und
für die 2030er Jahre 0,5 % („an average annual growth rate […] for potential output from 2023 to 2070“, [SVR, S. 15]). Die Bevölkerung wächst nach EUROPOP2023 von
83,895 Mio. (2022) auf 84,237 Mio. (2070) [AR, Tabelle 2, S. 13], das sind 0,01 % je Jahr. Je Kopf bleiben
1,007 ÷ 1,0001 − 1 = 0,69 %, gerundet 0,7 %. **Setzung von KAP3:** Das Wachstum des Produktionspotenzials je Kopf steht
für das Wachstum des Konsums je Kopf. Langfristig wachsen beide etwa gleich schnell; die Green Book nennt für
Großbritannien Werte beider Größen in derselben Höhe (1,7–2,2 % Konsum, 1,9 % BIP je Kopf, [GB] §2.14). Untergrenze
0,4 %: das Potenzialwachstum der 2020er Jahre [SVR, S. 15]. Obergrenze 1,1 %: das BIP je Kopf von 1991 bis 2024,
31.056,59 US-$ auf 44.027,76 US-$ in Preisen von 2015 [WB], also (44.027,76 ÷ 31.056,59) hoch (1 ÷ 33) − 1 = 1,06 % je
Jahr. Die Vergangenheit ist nur Obergrenze, weil das Arbeitsvolumen in Deutschland ab 2019 wieder schrumpft und nach der
Projektion bis 2070 weiter bremst [SVR, S. 14–15].

**Elastizität des Grenznutzens, 1,0 (Band 1,0–1,5).** „The Green Book assumes a value of 1.0 for the elasticity of the
marginal utility of consumption.“ [GB] §2.13. Als Spanne der Literatur nennt [GB] §2.12 die Werte 1,0, 1,3 und 1,5.
MK 4.0 nennt für die Diskontierung keine Zahl. Ihr Rechenbeispiel zum Equity Weighting lautet: „Wenn das
Pro-Kopf-Einkommen in einem armen Land zehnmal geringer ist, werden die nominalen Schadenskosten zehnmal höher
gewichtet.“ (S. 16). Liest man es mit der üblichen Form solcher Gewichte, Einkommensverhältnis hoch Elastizität, dann
gilt 10 = 10 hoch 1, also Elastizität 1. Das ist eine Ablesung von KAP3, keine Zahl der Konvention. Sie stimmt aber mit
[GB] überein.

**Einkommenselastizität des Schadenswerts, 0,85 (Band 0,85–1,0).** MK 4.0, S. 22: „Wir haben ferner berücksichtigt,
dass die Zahlungsbereitschaft zur Vermeidung immaterieller Gesundheitsbeeinträchtigungen (Schmerzen und Leid) mit dem
Einkommen steigt. Daher erfolgt eine Anpassung der Kostensätze entsprechend der Entwicklung des Bruttoinlandsprodukts
pro Kopf in Deutschland zwischen 2005 und 2025 (unter Verwendung einer Elastizität von 0,85, die auf dem NEEDS-Projekt
basiert […]).“ Bericht 95 schreibt die VOLY genau so von 2005 auf 2024 fort, mit dem Faktor „Einkommensentwicklung
^0,85 ×1,1719“ (Kap. 3.5). Die Obergrenze 1,0 stammt aus zwei Quellen. Die OECD empfiehlt über die Zeit: „Adjust VSL
with the same percentage as the percentage increase in GDP per capita.“ [OECD, Tabelle 0.1, S. 15]. Für den Transfer
zwischen Ländern empfiehlt sie 0,8, aber das ist eine andere Frage. Die Green Book nimmt den Wohlstandseffekt bei
Gesundheit ganz heraus, weil „the welfare or utility from additional years of life will not decline as real incomes
rise“ [GB] §2.16. Das entspricht einer Einkommenselastizität gleich der Elastizität des Grenznutzens, also 1,0.

**Band 0–0,7 Pp.** Die Untergrenze 0 gilt, wenn beide Elastizitäten 1,0 sind. Dann heben sich die Effekte bei jedem
Wachstum auf, und die Diskontrate ist die RZPR allein. Das ist die Lesart von [GB] §2.16 und [OECD]. Die Obergrenze
kombiniert die ungünstigsten Werte: 1,1 % × (1,5 − 0,85) = 0,715 Pp., gerundet 0,7 Pp. **Wirkung auf den Barwert**, bei
gleichbleibendem Jahresbetrag über die 41 Jahre 2025–2065 und zur RZPR 0 %: Die Summe der Abzinsfaktoren ist 41,0 bei
0 Pp., 40,19 beim Wert 0,1 Pp. und 35,78 bei 0,7 Pp. Gegenüber dem Wert liegt der Barwert an der Untergrenze also um
2,0 % höher und an der Obergrenze um 11 % niedriger.

**Eigener Wert, nicht Aufheben.** Die beiden Effekte heben sich zu 85 % auf, aber nicht ganz. Ein volles Aufheben setzte
voraus, dass der Wert der Gesundheit mit dem Einkommen genauso stark steigt wie der Nutzen eines Euros fällt (1,0 gegen
1,0). MK 4.0 setzt für den Wert aber 0,85 (S. 22), und das Produkt schreibt die VOLY damit fort. Dasselbe Gut bekäme
sonst für die Jahre 2005–2024 eine andere Elastizität als für 2025–2065. Das Aufheben bleibt deshalb die Untergrenze
des Bandes und ist nicht der Wert.

### Geltung für die Schadensarten von M0

- **#95 Hitzebelastung.** In der Beispielkommune Berlin entfallen 361,8 der 362,9 Mio. € je Jahr (99,7 %) auf YLL × VOLY
  (Bericht 95, Kap. 3.0, Ebenen 8–10). Das ist ein immaterieller Gesundheitsschaden, für den MK 4.0 die 0,85 festlegt.
  Den Rest von 1,09 Mio. € bilden Krankenhauskosten.
- **#98 UV-Schädigungen.** Bewertet werden Sterbefälle über YLL × VOLY und Erkrankungen über Behandlungskosten (Bericht
  98, Kap. 3.5). Den Anteil beider Teile rechnet Schritt 4 nach dem Endstand des Berichts nach.
- **#96 Aeroallergene.** Bewertet werden nur Behandlungskosten (Bericht 96, Register 96-K1-01), ohne
  Mortalitätskomponente.

**Behandlungskosten bekommen denselben Wert, als Abschätzung von KAP3.** MK 4.0 bindet die 0,85 an die
Zahlungsbereitschaft für immaterielle Beeinträchtigungen (S. 22). Für Behandlungskosten nennt sie weder eine
Einkommenselastizität noch eine Richtung. Wie sich ihr relativer Preis entwickelt, hängt davon ab, was eine Behandlung
teurer macht:
- Löhne des Personals steigen etwa mit dem Einkommen, das ergibt eine Komponente nahe 0.
- Arzneimittel und Sachmittel steigen etwa mit dem Verbraucherpreisindex, das ergibt eine Komponente bis zum vollen
  Wohlstandseffekt von 0,7 Pp.
- Wird die Behandlung je Fall aufwendiger, liegt die Komponente unter 0.

Für Deutschland trennt keine gefundene Quelle die Preisentwicklung je Fall vom wachsenden Behandlungsumfang. **Was
diese Vereinfachung verfälschen kann (§8 E3):** Jede Abweichung um 0,1 Pp. ändert den Barwert zur RZPR 0 % um rund 2 %
(gleichbleibender Jahresbetrag, 2025–2065). Im Band 0–0,7 Pp. sind das +2,0 % bis −11 %. Läge der wahre Wert bei
−0,5 Pp., läge der richtige Barwert um 13 % über dem nach Regel D. Die Richtung des Ergebnisses, die Rangfolge der Kommunen und die
Größenordnung ändern sich dadurch nicht, weil dieselbe Rate für alle Kommunen gilt. Die Frage betrifft vor allem #96,
wo der ganze Betrag aus Behandlungskosten besteht. Schritt 3 weist die Wirkung dort am Endstand nach.

### Bezugsjahr und Zeitraum der Abzinsung

- **Bezugsjahr 2025.** Abgezinst wird auf das Jahr 2025. Der Betrag des Jahres 2025 zählt voll, jedes spätere Jahr mit
  seinem Abstand zu 2025 in ganzen Jahren. Der Betrag des Jahres 2065 zählt bei 0,1 % mit 1 ÷ 1,001 hoch 40 = 0,961 und
  bei 1,1 % mit 1 ÷ 1,011 hoch 40 = 0,646. Begründung: MK 4.0 zinst „auf den heutigen Tag“ ab (S. 14). Heute im Sinne
  der Rechnung ist der Stand, auf den die Beträge gerechnet sind: Die Kostensätze haben den Preisstand 2024, und die
  Projektion des Produkts beginnt 2025. MK 4.0 versteht „€2025“ ebenso als Preisentwicklung „bis zum Ende von 2024“
  (S. 10, Fußnote 4).
- **Zeitraum 2025–2065.** Das sind die 41 Jahre der Klimaprojektion des Produkts (`dwd_data.py`,
  `get_climate_projection()`: 2025 bis 2065 in Jahresschritten). Schäden nach 2065 gehen nicht ein. Der Barwert ist
  deshalb der Wert dieser 41 Jahre und nicht der aller künftigen Schäden. Das Produkt muss es so benennen.
- **Nur feste Preise werden abgezinst.** Die Jahresbeträge stehen in Preisen von 2024. Inflation wird nicht zur
  Diskontrate addiert ([GB] §2.19; MK 4.0, S. 9: Preisanpassung mit dem Verbraucherpreisindex).
- **Eine Rate für den ganzen Zeitraum.** Die Diskontrate ist in allen Jahren gleich. Zur fallenden Rate der Green Book
  siehe A8.

### A8 — Risikoaversion und langfristige staatliche Ziele (MK 4.0, S. 15)

MK 4.0, S. 15: Die bei politischen Entscheidungen anzuwendende Diskontrate muss „auch die höhere gesellschaftliche
Risikoaversion sowie langfristige staatliche Ziele wie Generationengerechtigkeit und langfristige gesellschaftliche
Wohlfahrt berücksichtigen“. **A8 geht ein, und zwar so:** Die langfristigen Ziele stecken in der RZPR von 0 %, die
Risikoaversion bekommt keine eigene Zahl. Generationengerechtigkeit und langfristige Wohlfahrt sind die Gründe, aus
denen MK 4.0 die RZPR von 0 % führt, „die eine gleiche Gewichtung des Wohlergehens künftiger und heutiger Generationen
widerspiegelt“ (S. 10, ebenso S. 14). Das Produkt weist diesen Barwert immer aus, neben dem zu 1 %. Die Risikoaversion
beziffert MK 4.0 weder mit einer Zahl noch mit einem Rechenweg (S. 15). Ihre Richtung ist aber eindeutig: Eine
Gesellschaft, die Risiken scheut, zinst unsichere künftige Schäden eher niedriger ab, nie höher. Eine bezifferte Regel
dafür hat die Green Book: Weil die künftigen Werte der Bestandteile unsicher sind, fällt die Rate nach 30 Jahren
([GB] §3.1), für Gesundheit von 1,5 % auf 1,286 %, also um ein Siebtel ([GB] Tabelle 3.A). Übertragen auf Regel D
fällt die Rate in den Jahren 31–40 (2056–2065) um ein Siebtel. Bei gleichbleibendem Jahresbetrag steigt der Barwert
dadurch um 0,02 % zur RZPR 0 % und um 0,17 % zur RZPR 1 %. Das liegt weit unter der Breite des Bandes. KAP3 lässt diesen
Abschlag deshalb weg und sagt es hier. Keine Wahl dieser Festlegung läuft der Risikoaversion entgegen. Der Wert 0,1 Pp.
liegt im unteren Teil des Bandes 0–0,7 Pp. Ein Wert aus der Mitte des Bandes (0,35 Pp.) hätte den Barwert um 4,8 %
gesenkt, und dafür fehlt eine Quelle.

### A9 — Unvollständiger Zusammenhang zwischen Finanzmärkten und Grenznutzen der Betroffenen (MK 4.0, S. 15)

MK 4.0, S. 15: „Da die Monetarisierung von Umweltauswirkungen auf einem Grenznutzenkonzept basiert, muss die
Diskontrate außerdem berücksichtigen, dass der Zusammenhang zwischen den Finanzmärkten und dem Grenznutzen der
Betroffenen unvollständig ist, z. B. wenn betroffene Gemeinschaften überhaupt keinen Zugang zu den Finanzmärkten
haben.“ Einige Sätze davor steht: „Für politische Entscheidungen ist der Marktzinssatz jedoch kein geeignetes Konzept.“ **A9
geht über die Bauweise der Regel ein, ohne eigene Zahl:**

1. **Kein Bestandteil kommt vom Finanzmarkt.** Die Diskontrate besteht aus der RZPR, dem Konsumwachstum je Kopf und zwei
   Elastizitäten, die beschreiben, was ein Euro und was die Gesundheit den Betroffenen wert sind. Marktzins, Kreditzins
   der Kommune, Kapitalrendite oder Risikoaufschlag kommen nicht vor. Eine Kommune, die den Barwert der
   Gesundheitsschäden mit ihrem Kreditzins bildet, rechnet gegen S. 15.
2. **Das Wachstum ist das der Menschen, nicht das des Kapitals.** In Regel D steht das Wachstum des Konsums je Kopf der
   Bevölkerung, keine Verzinsung von Geldanlagen.
3. **Wessen Einkommen?** Hitzetote sind überwiegend alt: 225 der 277,4 Todesfälle je Jahr in Berlin sind 75 Jahre und
   älter (Bericht 95, Kap. 3.0, Ebene 6). Ihr Einkommen ist meist Rente und wächst womöglich langsamer als der
   Durchschnitt. In Regel D wird dasselbe Wachstum mit beiden Elastizitäten multipliziert. Wächst das Einkommen der
   Betroffenen langsamer, werden deshalb Wohlstandseffekt und Preiseffekt beide kleiner. Die Komponente sinkt dann
   Richtung 0, das Vorzeichen bleibt aber. Die Untergrenze 0 des Bandes deckt diesen Fall. Als Wert gilt der
   Durchschnitt, weil MK 4.0 Einkommensunterschiede innerhalb Deutschlands nicht berücksichtigt (S. 16) und die VOLY
   für alle gleich ist.

### Was eine einfachere Rechnung verfälschen würde (§8 E3)

- **Die RZPR allein**, heute im Produkt, gleichbedeutend mit Komponente 0: Der Barwert zur RZPR 0 % ist dann die
  unabgezinste Summe. Bei gleichbleibendem Jahresbetrag liegt er 2,0 % über dem Barwert nach Regel D, zur RZPR 1 % sind
  es 1,9 %. Der Fehler ist klein. Die Null ist aber nicht hergeleitet (P2), und sie widerspricht der Elastizität 0,85,
  mit der das Produkt die VOLY selbst fortschreibt.
- **Der Wohlstandseffekt ohne Preiseffekt** (0,7 Pp.): Der Barwert läge 11 % zu niedrig. Künftige Gesundheitsschäden
  zählten dann so, als stiege ihr Wert nicht mit dem Einkommen. Das widerspricht MK 4.0, S. 22.
- **Ein Kapitalmarktzins** ist nach S. 15 unzulässig und würde künftige Schäden stark abwerten. Wie stark, zeigt das
  Rechenbeispiel der Konvention: Bei einer Rate von 3 % zählt ein Schaden in 30 Jahren nur noch mit 41 % (S. 14).

## Entscheidungslog

Gewählt ist Regel D. Die zweite Komponente für die Gesundheitsschäden von M0 ist ein eigener Wert von 0,1 Pp. mit Band
0–0,7 Pp. Verworfen, je mit einem Satz:

1. **Die RZPR allein als Diskontrate** (heutiger Stand im Produkt) ist verworfen, weil MK 4.0 RZPR und Diskontrate
   ausdrücklich trennt (S. 10, S. 14–15) und die zweite Komponente sonst ohne Herleitung auf null stünde (Vorgabe P2).
2. **Das Aufheben der Effekte** (Komponente 0 als Wert) ist verworfen, weil es eine Einkommenselastizität des
   Gesundheitswerts von 1,0 voraussetzt, MK 4.0 aber 0,85 festlegt (S. 22) und das Produkt die VOLY damit fortschreibt;
   das Aufheben bleibt Untergrenze des Bandes.
3. **Der Wohlstandseffekt ohne Preiseffekt** (0,7 Pp.) ist verworfen, weil er unterstellt, dass der Wert der
   Gesundheit nicht mit dem Einkommen steigt, entgegen MK 4.0, S. 22.
4. **Ein Marktzins oder der Kreditzins der Kommune** ist verworfen, weil MK 4.0 den Marktzinssatz für politische
   Entscheidungen ausschließt und der Zusammenhang zwischen Finanzmärkten und dem Grenznutzen der Betroffenen
   unvollständig ist (S. 15).
5. **Die Einkommenselastizität 1,0 als Wert** ([OECD] über die Zeit, [GB]) ist verworfen, weil das Produkt dieselbe
   VOLY für 2005–2024 mit 0,85 fortschreibt und dasselbe Gut nicht in Vergangenheit und Zukunft zwei Elastizitäten
   tragen soll; 1,0 bleibt Bandgrenze.
6. **Eine Elastizität des Grenznutzens von 1,3 oder 1,5 als Wert** ist verworfen, weil [GB] sie nur als Spanne der
   Literatur nennt (§2.12), selbst 1,0 setzt (§2.13) und das Rechenbeispiel von MK 4.0 (S. 16) der 1 entspricht.
7. **Das Wachstum 1991–2024 von 1,06 % als Wert** ist verworfen, weil es mit einem wachsenden Arbeitsvolumen entstand,
   das die Projektion für 2023–2070 nicht mehr sieht ([SVR] S. 14–15); es bleibt Obergrenze.
8. **Ein eigener Wert für Behandlungskosten** neben dem für immaterielle Gesundheitsschäden ist verworfen, weil keine
   gefundene Quelle für Deutschland die Preisentwicklung je Fall vom wachsenden Behandlungsumfang trennt und die
   Abweichung unter „Geltung für die Schadensarten von M0“ beziffert ist.
9. **Eine nach 30 Jahren fallende Diskontrate** ([GB] Tabelle 3.A) ist verworfen, weil sie den Barwert über 2025–2065
   um höchstens 0,17 % ändert und eine zweite Zeitstufe die Rechnung schwerer lesbar macht.
10. **Das Jahr der Berechnung als Bezugsjahr** ist verworfen, weil der Barwert dann mit dem Kalender wandern und bereits
    vergangene Projektionsjahre aufzinsen würde, was [GB] §2.20 ausschließt.
11. **Eine nominale Diskontrate** (Diskontrate plus Inflation) ist verworfen, weil die Jahresbeträge in festen Preisen
    stehen und Inflation nicht zur Rate addiert wird ([GB] §2.19; MK 4.0, S. 9).

## Befunde an Code

Gelesen am 25.09.2026: `backend/app/data/diskontierung.py` vollständig; in
`backend/app/services/cost_projection_service.py` die Funktionen `_diskontraten()` und `_discounted()` (innere Funktion
von `project_costs()`) sowie ihr Aufruf in `_scenario_block()`. Den Nachzug macht der CTO (T-1060-ceo, T-1147-cto,
T-1151-cto), diese Datei ändert keinen Code.

| Nr | Stelle | Stand im Code | Regel D | Art |
|---|---|---|---|---|
| C1 | `diskontierung.py`, `RELATIVE_PRICE_COMPONENT` | `0.0` | `0.001` (0,1 Pp.) für die Gesundheitsschäden von M0 | Wert weicht ab |
| C2 | `diskontierung.py` | keine Größen für Konsumwachstum je Kopf (0,7 %), Elastizität des Grenznutzens (1,0) und Einkommenselastizität des Schadenswerts (0,85) | die Komponente ist aus diesen drei Werten gerechnet; die Parameterliste muss nach P1 zeigen, wie sie zustande kommt, mit Band je Bestandteil | Herleitung fehlt im Produkt |
| C3 | `diskontierung.py`, `RELATIVE_PRICE_COMPONENT_SPEC` | `source` nennt nur S. 14–15; `evidence_derivation.wert`: „vorläufig“, „unterstellt, dass sich beide Effekte aufheben“; `band`: „Keine Bandbreite in Zahlen“, Vorzeichen für Gesundheitsschäden „offen“; `sensitivitaet` beschreibt den Fall 0 | Wert 0,1 Pp. mit Herleitung und Quellen (MK 4.0, S. 14–16 und S. 22; [GB]; [OECD]; [SVR]; [AR]; [WB]); Band 0–0,7 Pp.; Vorzeichen positiv; Barwert zur RZPR 0 % liegt unter der unabgezinsten Summe | Text weicht ab |
| C4 | `diskontierung.py`, `MODELLGRENZEN` | Satz 1: Richtung für Gesundheitsschäden „offen“; Satz 2: Risikoaversion „geht nicht ein“, ohne Begründung; Satz 3: der unvollständige Zusammenhang zwischen Finanzmärkten und Grenznutzen „ist nicht berücksichtigt“ | Satz 1: Richtung positiv, Wert 0,1 Pp.; Satz 2: A8 geht über die RZPR 0 % ein, Risikoaversion ohne eigene Zahl mit Begründung (Abschnitt A8); Satz 3: A9 ist über die Bauweise berücksichtigt (Abschnitt A9); es fehlen die Grenzen „Behandlungskosten mit demselben Wert“ und „Barwert nur über 2025–2065“ | Text weicht ab |
| C5 | `cost_projection_service.py`, `_discounted()` über `_diskontraten()` | eine Komponente für die ganze Reihe: alle Risikogruppen, auch Schadensarten außerhalb der Gesundheit, und auf dem Maßnahmenpfad auch OPEX und CAPEX | die Komponente gilt je Schadensart; einen Wert hat nur die Gesundheit von M0; für andere Schadensarten und für Maßnahmenkosten setzt diese Datei keinen Wert (A-0048) | Geltungsbereich weicht ab; mit C1 bekämen alle Schadensarten den Gesundheitswert |

**Ohne Abweichung:** `PURE_TIME_PREFERENCE_RATES = (0.0, 0.01)`. Die Summe RZPR + Komponente in `_diskontraten()`. Der
Faktor 1 ÷ (1 + d) hoch (Jahr − `years[0]`) in `_discounted()`, mit Bezugsjahr `years[0]` = 2025 und Zeitraum 2025–2065,
solange die Klimaprojektion 2025 beginnt. Die über den Zeitraum gleiche Rate. Die Schlüssel des Feldes `discounted`
nach der RZPR.

**Betroffen beim Nachzug, nicht Gegenstand dieser Befunde:** In derselben Datei nennen der Modulkopf (Z. 10–11: „vorläufig
0 Pp.“) und der Eintrag in `assumptions` (Richtung „offen“, „bis die Methodik sie festlegt“) den alten Stand. Die Tests
`test_rate_null_ist_die_undiskontierte_reihe` und `test_spec_und_modellgrenzen` in
`backend/tests/test_kostenprojektion_diskontierung.py` setzen die Komponente 0 voraus.

## Quellen

Abgerufen am 25.09.2026. Ein Archiv-Schnappschuss ließ sich in diesem Lauf nicht anlegen, weil web.archive.org für den
Abruf gesperrt ist. Er ist in der Quellenpflege nachzutragen (Aufgabe §3.8).

- **[MK 4.0]** Eser, N.; Matthey, A.; Bünger, B.: Handbuch Umweltkosten – Methodenkonvention 4.0. Umweltbundesamt,
  Dessau-Roßlau, Dezember 2025, ISSN 2363-832X. Lokale Kopie
  `docs/UBA/UBA_Handbuch Umweltkosten_Methodenkonvention 4.0.pdf`. Vollständig gelesen: Inhaltsverzeichnis S. 4–5,
  Kap. 1 S. 8–9, Kap. 2 S. 10–16 (Kap. 2.1 mit Fußnoten 2 und 4, Tabelle 1 im Text; Kap. 2.2.1–2.2.2; Kap. 2.2.3
  „Diskontierung und die Reine Zeitpräferenzrate“ S. 14–15 mit Fußnote 13; Kap. 2.2.4 „Equity Weighting“ mit Kasten
  S. 16), Kap. 3.4 S. 21–22 mit Fußnoten 17–19. Verwendet: S. 9, 10, 14, 15, 16, 22.
- **[GB]** HM Treasury: Discounting – Green Book supplementary guidance. London, Februar 2026, ISBN 978-1-918417-18-0.
  https://assets.publishing.service.gov.uk/media/698f30a4492ea446ea7f43d3/Green_Book_supplementary_guidance_-_discounting.pdf.
  Vollständig gelesen: Kap. 1–3, S. 6–13. Verwendet: §2.12–2.16, §2.19–2.20, §3.1–3.2, Tabelle 3.A (S. 9–12).
- **[OECD]** OECD: Mortality Risk Valuation in Environment, Health and Transport Policies. OECD Publishing, Paris, 2012,
  doi:10.1787/9789264130807-en.
  https://www.oecd.org/content/dam/oecd/en/publications/reports/2012/02/mortality-risk-valuation-in-environment-health-and-transport-policies_g1g1690a/9789264130807-en.pdf.
  Gelesen: Executive Summary, S. 13–15 (PDF-Seiten 15–17), mit Tabelle 0.1 „Recommendations for adjusting VSL base
  values“, S. 15. Nicht gelesen: Kap. 1–5 und die Anhänge.
- **[SVR]** Ochsner, C.; Other, L.; Thiel, E.; Zuber, C.: Demographic Aging and Long-Run Economic Growth in Germany.
  Working Paper 02/2024, Sachverständigenrat zur Begutachtung der gesamtwirtschaftlichen Entwicklung, Wiesbaden,
  15.02.2024. https://www.sachverstaendigenrat-wirtschaft.de/fileadmin/dateiablage/Arbeitspapiere/Arbeitspapier_02_2024.pdf.
  Gelesen: Abstract, Kap. 1, Kap. 4 und Anfang Kap. 5, gedruckte S. 1–2 und 11–15 (PDF-Seiten 3–5 und 14–18). Verwendet:
  S. 14–15, gedruckte Seite 15 = PDF-Seite 18.
- **[AR]** European Commission, Economic Policy Committee: 2024 Ageing Report – Country fiche for Germany. Brüssel, 2024.
  https://economy-finance.ec.europa.eu/document/download/e8f41d38-6d27-45b4-8919-c9348720fcfc_en?filename=2024-ageing-report-country-fiche-Germany.pdf.
  Gelesen: Inhaltsverzeichnis S. 2–3, Kap. 2 S. 13–15. Verwendet: Tabelle 2 „Main demographic variables“, S. 13. Das
  Länderblatt führt kein BIP je Kopf.
- **[WB]** World Bank: World Development Indicators, GDP per capita (constant 2015 US$), Kennung NY.GDP.PCAP.KD,
  Deutschland, 1991–2024.
  https://api.worldbank.org/v2/country/DEU/indicator/NY.GDP.PCAP.KD?format=json&per_page=100&date=1991:2024. Verwendet:
  1991 = 31.056,59 US-$, 2024 = 44.027,76 US-$; Rechnung von KAP3: 1,06 % je Jahr.
- **[Bericht 95]** `docs/methodik/95_hitzebelastung.md`, Kap. 3.0 (Ebenen 6–10), Kap. 3.5 (VOLY-Kette).
- **[Bericht 96]** `docs/methodik/96_aeroallergene.md`, Evidenz-Register 96-K1-01.
- **[Bericht 98]** `docs/methodik/98_uv_schaedigungen.md`, Kap. 3.5.
- **[Produkt]** `backend/app/data/diskontierung.py`; `backend/app/services/cost_projection_service.py`
  (`_diskontraten()`, `project_costs()`, `_discounted()`); `backend/app/services/climate/dwd_data.py`
  (`get_climate_projection()`); `docs/KONFORMITAET_CHECKLISTE.md`, Zeile 22 und „Gegenprobe Zeile 22“.

Von MK 4.0 zitiert, aber nicht gelesen: Ramsey (1928), Drupp et al. (2024), Baumgärtner et al. (2015) und Anthoff (2025).
Die Festlegung stützt sich auf keine Zahl aus diesen Werken.
