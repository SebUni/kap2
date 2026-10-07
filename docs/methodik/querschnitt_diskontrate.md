# Querschnitt: Diskontrate

Querschnittsdatei der Methodik, gültig für alle Klimawirkungen. Einen Wert bekommen zuerst die Gesundheitsschäden von
M0 (#95, #96, #98). Für die übrigen Schadensarten ruht die Anwendung bis zur Abnahme von M0 (A-0048). Schritt 1 (Ticket
T-1242-methodik_manager, Vorhaben T-1116-cmo) hat die Regel und ihre Werte festgelegt. Schritt 2
(T-1243-methodik_manager) hat die Rechenkette vom Jahresbetrag zum Barwert mit Beispiel-Block für #95 gebaut, Schritt 3
(T-1244-methodik_manager) hat #96 nachgerechnet. Dieser Stand ist Schritt 4 (T-1245-methodik_manager): Derselbe Block
rechnet #98 nach, und die Werte für #95 und #96 sind auf den Endstand der Berichte nachgezogen (Entscheidungslog
Nr. 17 und 18). Die Schlussprüfung des Vorhabens (T-1836, 07.10.2026) hat festgelegt, dass Regel D nach dem Jahr des
Schadenseintritts abzinst (Entscheidungslog Nr. 23, Befunde B5 und B6), die Einordnung „Untergrenze“ für #95 und #96 an
Kap. 4 der Berichte geprüft (Befunde B1 und B2) und die Einträge Nr. 12–15 des Entscheidungslogs mit ihren alten Werten
wiederhergestellt; kein Barwert hat sich dabei geändert. Verweise auf die Berichte nennen Abschnitt und Ebene. Eine
Zeilennummer steht nur beim Jahresbetrag von #98, gemessen am 06.10.2026, und in den wiederhergestellten Einträgen
Nr. 12 und 14.

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

„Jahr“ ist dabei das Jahr, in dem der Schaden eintritt, nicht das Jahr der Belastung, die ihn ausgelöst hat; der
Jahresbetrag eines Jahres ist der Schaden, der in diesem Jahr eintritt (Abschnitt „Bezugsjahr und Zeitraum der
Abzinsung“, Punkt „Jahr des Schadenseintritts“).

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
  98, Kap. 3.4, und Kap. 3.0, Ebene 9). In der Beispielkommune Berlin entfallen 7,84 der 11,68 Mio. € je Jahr (67 %) auf
  YLL × VOLY (MM 4,97 Mio. €, C44 2,87 Mio. €). Für diesen immateriellen Schaden legt MK 4.0 die 0,85 fest. Die übrigen
  3,83 Mio. € (33 %) sind Behandlungskosten (MM 173.400 €, C44 3,66 Mio. €).
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
- **Jahr des Schadenseintritts.** Jeder Betrag wird nach dem Jahr abgezinst, in dem der Schaden eintritt: das Jahr des
  Sterbefalls, der Erkrankung, der Behandlung. Das Jahr der Belastung, die den Schaden ausgelöst hat, zählt nicht.
  Begründung: MK 4.0 zinst nach dem Zeitpunkt ab, „zu dem die Kosten und Nutzen heutiger Entscheidungen anfallen“
  (S. 14). Sie nennt als Beispiel gerade verzögerte Gesundheitsschäden: Auswirkungen auf öffentliche Güter „werden oft
  erst in ferner Zukunft sichtbar, beispielsweise die langfristigen gesundheitlichen Auswirkungen der
  Luftverschmutzung“, und eine RZPR von 1 % heißt, dass „nur 74% des Nutzens (Wohlfahrt) der in 30 Jahren auftritt“
  berücksichtigt werden (S. 14). Gezählt wird also ab dem Jahr, in dem der Schaden auftritt. **Folge für eine
  Verzögerung zwischen Belastung und Schaden (Latenz):** Sie geht über den Betrag des Jahres ein, in dem der Schaden
  eintritt, nie über eine Verschiebung des Abzinsungsjahres. Ein Bericht liefert dafür je Jahr die Schäden, die in
  diesem Jahr eintreten. **Folge für #98:** Bericht 98 beziffert mit seinem Jahresbetrag die Fälle, die in einem Jahr
  eintreten (Kap. 3.0, „Lesart des Jahresbetrags“). Die Kette bucht ihn deshalb in seinem Jahr, mit Regel D vereinbar.
  Die Latenz bleibt allein eine Frage des Betrags: Eine Jahres-Attribution kürzt ihn mit dem Transient-Faktor τ, im
  Ausweis des Berichts steht τ = 1. Über 2025–2065 wächst τ und fällt nie, solange die Dosis nicht sinkt, weil jede
  Kohorte, die später erkrankt, einen größeren Teil ihrer Lebenszeitdosis unter der gestiegenen Dosis gesammelt hat
  (Abschnitt „Rechenkette“, Absatz „Wann der Schaden eintritt“). Die Spanne 0,20–0,48 in Bericht 98, Kap. 3.4, gilt für
  die heute Erkrankenden. Ein in allen 41 Jahren gleicher τ ist deshalb der untere Rand des Barwerts unter einer
  Jahres-Attribution, τ = 1 der obere.
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

## Rechenkette

Die Rechenkette führt vom Jahresbetrag eines Berichts zum Barwert nach Regel D. Sie beginnt dort, wo die Rechenkette 3.0
des Berichts endet. **Beispielkommune: Berlin, Klimawirkung #95 Hitzebelastung.** Der Jahresbetrag stammt aus der
letzten Ebene der Rechenkette 3.0 von `docs/methodik/95_hitzebelastung.md`, Kap. 3.0, Ebene 10: „362,9 Mio. € je Jahr
(Preisstand 2024)“. Regel D liefert zwei Barwerte, einen je RZPR; die Kette rechnet beide.

**Wie ein Abzinsfaktor zu lesen ist.** Der Abzinsfaktor eines Jahres sagt, mit welchem Anteil der Betrag dieses Jahres
im Barwert zählt: 0,980 heißt, 1 € Schaden im Jahr 2045 zählt wie 98 Cent im Jahr 2025. Der **Barwertfaktor** ist die
Summe der 41 Abzinsfaktoren. Er sagt, wie vielen vollen Jahresbeträgen der Barwert entspricht. Ohne Abzinsung wären es
genau 41.

| Ebene | Rechenschritt | Wert (Beispielkommune Berlin, #95) | Quelle |
|---|---|---|---|
| 1 | Jahresbetrag: bewerteter Schaden (Konto K1) je Jahr | 362,9 Mio. € je Jahr (Preisstand 2024) | Bericht 95, Kap. 3.0, Ebene 10 |
| 2 | × 41 Jahre 2025–2065, Jahresbetrag in jedem Jahr gleich = Summe ohne Abzinsung | 362,9 Mio. € × 41 = 14,88 Mrd. € | Zeitraum: Festlegung, „Bezugsjahr und Zeitraum der Abzinsung“; gleichbleibender Verlauf: Bericht 95, Kap. 6, Absätze „Szenario-Anwendung 95-A“ und „Jahresbeträge ohne Abzinsung“ (M0 weist das Ist-Klima aus) |
| 3 | Diskontrate zur RZPR 0 % = RZPR + Veränderung der relativen Preise | 0 % + 0,1 Pp. = 0,1 % | Festlegung, Regel D |
| 4 | Abzinsfaktor je Jahr = 1 ÷ 1,001 hoch (Jahr − 2025) | 2025: 1,000 · 2035: 0,990 · 2045: 0,980 · 2055: 0,970 · 2065: 0,961 | Rechnung |
| 5 | Barwertfaktor = Summe der 41 Abzinsfaktoren, je Jahrzehnt zusammengezählt | 9,955 (2025–2034) + 9,856 (2035–2044) + 9,758 (2045–2054) + 9,661 (2055–2064) + 0,961 (2065) = 40,19 | Rechnung |
| 6 | **Barwert zur RZPR 0 %** = Ebene 1 × Ebene 5 | 362,9 Mio. € × 40,19 = **14,59 Mrd. € (Preisstand 2024)** | Rechnung |
| 7 | Diskontrate zur RZPR 1 % = RZPR + Veränderung der relativen Preise | 1 % + 0,1 Pp. = 1,1 % | Festlegung, Regel D |
| 8 | Abzinsfaktor je Jahr = 1 ÷ 1,011 hoch (Jahr − 2025) | 2025: 1,000 · 2035: 0,896 · 2045: 0,803 · 2055: 0,720 · 2065: 0,646 | Rechnung |
| 9 | Barwertfaktor = Summe der 41 Abzinsfaktoren, je Jahrzehnt zusammengezählt | 9,524 (2025–2034) + 8,537 (2035–2044) + 7,653 (2045–2054) + 6,860 (2055–2064) + 0,646 (2065) = 33,22 | Rechnung |
| 10 | **Barwert zur RZPR 1 %** = Ebene 1 × Ebene 9 | 362,9 Mio. € × 33,22 = **12,06 Mrd. € (Preisstand 2024)** | Rechnung |

**Ergebnis nach Regel D für #95, Beispielkommune Berlin:** Der bewertete Schaden der 41 Jahre 2025–2065 hat einen
Barwert von 14,59 Mrd. € zur RZPR 0 % und von 12,06 Mrd. € zur RZPR 1 % (Preisstand 2024, Bezugsjahr 2025). Das Produkt
zeigt beide Werte nebeneinander (Festlegung, „Erste Komponente“).

**Verlauf der Jahresbeträge.** Die Festlegung schreibt keinen Verlauf vor. Sie sagt nur, dass jeder Jahresbetrag der
Jahre 2025–2065 abgezinst wird, und rechnet ihre eigenen Beispiele mit gleichbleibendem Jahresbetrag. Bericht 95 weist in
M0 das Ist-Klima aus und nennt keinen Betrag für spätere Jahre (Kap. 6, Absatz „Szenario-Anwendung 95-A“). Die Kette setzt deshalb in jedem
Jahr denselben Betrag an. Dass die Festlegung für das Produkt einen Verlauf mit Klimasignal voraussetzt, den Bericht 95 in
M0 nicht liefert, steht als Befund B1 unter „Befunde an Berichte“.

**Kette und Produkt.** Der Betrag des Produkts für Berlin ist der Zelllauf mit Gemeindeschlüssel, nicht die Kette. Er
liegt bei 345,11 Mio. € je Jahr, 5 % unter der Kette (Bericht 95, Kap. 3.0, Punkt „Ebenen 1, 2 und 6, eine Zelle statt
aller Zellen“ unter der Tabelle). Sein Barwert ist 345,11 Mio. € × 40,19 = 13,87 Mrd. € zur RZPR 0 % und
345,11 Mio. € × 33,22 = 11,46 Mrd. € zur RZPR 1 %. Die Abweichungen in Prozent in der Tabelle unten bleiben gleich, weil
derselbe Barwertfaktor auf beide Beträge wirkt.

**Dieselbe Kette für #96 Aeroallergene, Beispielkommune Berlin.** Der Jahresbetrag stammt aus der letzten Ebene der
Rechenkette 3.0 von `docs/methodik/96_aeroallergene.md`, Kap. 3.0, Ebene 10: „2,53 Mio. € je Jahr (Preisstand
2024)“. Das ist der Endstand nach Rev. 4 mit dem Klimaanteil 0,27 (Bericht 96, Statuskopf, Runden 30–32, Befund 258).
Schritt 3 hatte noch mit 4,69 Mio. € gerechnet, dem Stand mit dem Klimaanteil 0,50 (Entscheidungslog Nr. 18). Der
Betrag besteht ganz aus Behandlungskosten (Konto K1, nur Morbidität). Die Ebenen 3–5 und 7–9 hängen nicht vom
Jahresbetrag ab und sind dieselben wie bei #95.

| Ebene | Rechenschritt | Wert (Beispielkommune Berlin, #96) | Quelle |
|---|---|---|---|
| 1 | Jahresbetrag: bewerteter Schaden (Konto K1, nur Morbidität) je Jahr | 2,53 Mio. € je Jahr (Preisstand 2024) | Bericht 96, Kap. 3.0, Ebene 10 |
| 2 | × 41 Jahre 2025–2065, Jahresbetrag in jedem Jahr gleich = Summe ohne Abzinsung | 2,53 Mio. € × 41 = 103,7 Mio. € | Zeitraum: Festlegung, „Bezugsjahr und Zeitraum der Abzinsung“; gleichbleibender Verlauf: Bericht 96, Kap. 6, Absätze „Jahresbeträge ohne Abzinsung“ und „Szenario-Anwendung 96-A“ (M0 weist das Ist-Klima aus) |
| 3 | Diskontrate zur RZPR 0 % | 0,1 %, wie #95 | Festlegung, Regel D |
| 4 | Abzinsfaktor je Jahr = 1 ÷ 1,001 hoch (Jahr − 2025) | wie #95: 2025: 1,000 · 2045: 0,980 · 2065: 0,961 | Rechnung |
| 5 | Barwertfaktor = Summe der 41 Abzinsfaktoren | 40,19, wie #95 | Rechnung |
| 6 | **Barwert zur RZPR 0 %** = Ebene 1 × Ebene 5 | 2,53 Mio. € × 40,19 = **101,7 Mio. € (Preisstand 2024)** | Rechnung |
| 7 | Diskontrate zur RZPR 1 % | 1,1 %, wie #95 | Festlegung, Regel D |
| 8 | Abzinsfaktor je Jahr = 1 ÷ 1,011 hoch (Jahr − 2025) | wie #95: 2025: 1,000 · 2045: 0,803 · 2065: 0,646 | Rechnung |
| 9 | Barwertfaktor = Summe der 41 Abzinsfaktoren | 33,22, wie #95 | Rechnung |
| 10 | **Barwert zur RZPR 1 %** = Ebene 1 × Ebene 9 | 2,53 Mio. € × 33,22 = **84,0 Mio. € (Preisstand 2024)** | Rechnung |

**Ergebnis nach Regel D für #96, Beispielkommune Berlin:** Der bewertete Schaden der 41 Jahre 2025–2065 hat einen
Barwert von 101,7 Mio. € zur RZPR 0 % und von 84,0 Mio. € zur RZPR 1 % (Preisstand 2024, Bezugsjahr 2025). Wie bei #95
setzt die Kette in jedem Jahr denselben Betrag an, weil Bericht 96 in M0 nur das Ist-Klima ausweist (Befund B2).

**Kette und Produkt, #96.** Der Betrag für Berlin ist der Zelllauf des Produkts: 2,47 Mio. € je Jahr, 2,2 % weniger als
die Kette (Bericht 96, Kap. 3.0, Absatz „Kommune statt Zellen“). Sein Barwert ist 2,47 Mio. € × 40,19 = 99,3 Mio. € zur
RZPR 0 % und 2,47 Mio. € × 33,22 = 82,1 Mio. € zur RZPR 1 %. Bis zur Übernahme Ü-13 rechnet das Produkt noch mit dem
Klimaanteil 0,50 und zeigt 4,58 Mio. € je Jahr (Bericht 96, Kap. 3.0, Ebene 10). Maßgeblich für diese Datei ist der
Bericht.

**Behandlungskosten mit demselben Wert: die Wirkung am Endstand von #96.** Die Festlegung gibt Behandlungskosten
dieselbe Komponente von 0,1 Pp. wie den immateriellen Schäden, als Abschätzung von KAP3 (Abschnitt „Geltung für die
Schadensarten von M0“). Bei #96 hängt der ganze Betrag daran. Am Endstand von Bericht 96 wirkt die Wahl so:

| Veränderung der relativen Preise | Barwert zur RZPR 0 % | gegen Regel D | Barwert zur RZPR 1 % | gegen Regel D |
|---|---|---|---|---|
| 0,1 Pp. (Regel D) | 101,7 Mio. € | — | 84,0 Mio. € | — |
| 0 Pp. (Untergrenze des Bandes) | 103,7 Mio. € | +2,0 % | 85,6 Mio. € | +1,9 % |
| 0,7 Pp. (Obergrenze des Bandes) | 90,5 Mio. € | −11 % | 75,5 Mio. € | −10 % |
| −0,5 Pp. (Behandlung je Fall wird aufwendiger, außerhalb des Bandes) | 114,9 Mio. € | +13 % | 94,0 Mio. € | +12 % |

Selbst der Fall außerhalb des Bandes verschiebt den Barwert um weniger als die Wahl der RZPR (17 %) und weit weniger als
das Band des Klimaanteils im Jahresbetrag (Bericht 96, Kap. 3.0, Absatz „Stärkster Treiber“: 1,78–3,84 Mio. € je Jahr,
−30 % bis +52 %, als Barwert nach Regel D 71,5–154,3 Mio. € zur RZPR 0 % und 59,1–127,6 Mio. € zur RZPR 1 %). Die
Abschätzung „derselbe Wert“ ändert deshalb weder die Richtung noch die Größenordnung des Barwerts von #96.

**Dieselbe Kette für #98 UV-Schädigungen, Beispielkommune Berlin.** Der Jahresbetrag stammt aus der letzten Ebene der
Rechenkette 3.0 von `docs/methodik/98_uv_schaedigungen.md`, Kap. 3.0, Ebene 10, Zeile 310 (Rev. 15 vom 05.10.2026):
„zusammen **11,68 Mio. € (Preisstand 2024) je Jahr**“. Er besteht zu 67 % aus YLL × VOLY und zu 33 % aus
Behandlungskosten (Abschnitt „Geltung für die Schadensarten von M0“). Die Ebenen 3–5 und 7–9 sind dieselben wie bei #95.

| Ebene | Rechenschritt | Wert (Beispielkommune Berlin, #98) | Quelle |
|---|---|---|---|
| 1 | Jahresbetrag: bewerteter Schaden (Konto K1, Ursache UV) je Jahr | 11,68 Mio. € je Jahr (Preisstand 2024) | Bericht 98, Kap. 3.0, Ebene 10, Zeile 310 |
| 2 | × 41 Jahre 2025–2065, Jahresbetrag in jedem Jahr gleich = Summe ohne Abzinsung | 11,68 Mio. € × 41 = 478,9 Mio. € | Zeitraum: Festlegung, „Bezugsjahr und Zeitraum der Abzinsung“; gleichbleibender Verlauf: Bericht 98, Kap. 6, Absätze „Szenario-Anwendung 98-A“ und „Jahresbeträge ohne Abzinsung“ (M0 weist das Ist-Klima aus) |
| 3 | Diskontrate zur RZPR 0 % | 0,1 %, wie #95 | Festlegung, Regel D |
| 4 | Abzinsfaktor je Jahr = 1 ÷ 1,001 hoch (Jahr − 2025) | wie #95: 2025: 1,000 · 2045: 0,980 · 2065: 0,961 | Rechnung |
| 5 | Barwertfaktor = Summe der 41 Abzinsfaktoren | 40,19, wie #95 | Rechnung |
| 6 | **Barwert zur RZPR 0 %** = Ebene 1 × Ebene 5 | 11,68 Mio. € × 40,19 = **469,4 Mio. € (Preisstand 2024)** | Rechnung |
| 7 | Diskontrate zur RZPR 1 % | 1,1 %, wie #95 | Festlegung, Regel D |
| 8 | Abzinsfaktor je Jahr = 1 ÷ 1,011 hoch (Jahr − 2025) | wie #95: 2025: 1,000 · 2045: 0,803 · 2065: 0,646 | Rechnung |
| 9 | Barwertfaktor = Summe der 41 Abzinsfaktoren | 33,22, wie #95 | Rechnung |
| 10 | **Barwert zur RZPR 1 %** = Ebene 1 × Ebene 9 | 11,68 Mio. € × 33,22 = **388,0 Mio. € (Preisstand 2024)** | Rechnung |

**Ergebnis nach Regel D für #98, Beispielkommune Berlin:** Der bewertete Schaden der 41 Jahre 2025–2065 hat einen
Barwert von 469,4 Mio. € zur RZPR 0 % und von 388,0 Mio. € zur RZPR 1 % (Preisstand 2024, Bezugsjahr 2025). Wie bei #95
und #96 setzt die Kette in jedem Jahr denselben Betrag an, weil Bericht 98 in M0 nur das Ist-Klima ausweist (Befund B4).

**Kette und Produkt, #98.** Einen Betrag des Produkts für Berlin nennt Bericht 98 nicht. Unter der Kette steht nur, dass
das Produkt Berlin mit 3.586.909 statt 3.662.381 Einwohnern liest, also mit 2,1 % weniger (Kap. 3.0, Punkt „Bevölkerung
im Produkt“). Daraus einen Betrag zu bilden wäre eine Zahl ohne Quelle. Diese Datei weist deshalb für #98 nur den
Barwert der Kette aus.

**Wann der Schaden eintritt: die Latenz bei #98.** Hautkrebs entsteht mit einer Verzögerung von „Jahrzehnten“ (Bericht
98, Kap. 6, Modellgrenze 1). Bericht 98 liest seinen Jahresbetrag deshalb so: Ebene 10 „beziffert die Fälle eines Jahres
unter der heutigen, eingelaufenen Dosislage — die Latenz von Jahrzehnten steckt schon in den Inzidenzraten der Ebene 2,
gemeint sind nicht die späteren Folgen der Belastung dieses Jahres“ (Kap. 3.0, „Lesart des Jahresbetrags“). Der Betrag
ist das „eingelaufene Risiko“ der heutigen Dosislage, „keine Vorhersage der Fälle *dieses* Jahres; die
Jahres-Attribution ist konzeptionell unscharf“ (Kap. 6, Modellgrenze 1). Der Bericht nennt das die Gleichgewichtslesart.
Sein Entscheidungslog Nr. 14 legt sie fest, „kein Latenz-Discounting“, und nennt die Folge: „Ergebnis wird gegenüber
einer Jahres-Attribution überschätzt“. Die Kette übernimmt diese Lesart. Sie bucht jeden Jahresbetrag in seinem Jahr
und zinst ihn nach Regel D ab, ohne Abzug für die Latenz.

Die Latenz könnte den Barwert auf zwei Wegen senken. Beide beschreiben dieselbe Verzögerung, aber an verschiedenen
Stellen der Rechnung. Regel D lässt nur den ersten zu, weil sie nach dem Jahr des Schadenseintritts abzinst
(Festlegung, „Bezugsjahr und Zeitraum der Abzinsung“; Entscheidungslog Nr. 23):

- **Jahres-Attribution: kleinerer Betrag im selben Jahr (Transient-Faktor τ, Bericht 98).** Wer heute erkrankt, hat
  den größten Teil seiner Lebenszeitdosis gesammelt, bevor die Sonnenscheindauer gestiegen ist. Zählt man nur die Fälle,
  die der Anstieg bis heute ausgelöst hat, wird der Jahresbetrag mit τ multipliziert. Bericht 98 rechnet τ = (Dauer des
  Anstiegs ÷ 2) ÷ Erkrankungsalter, etwa 30 ÷ 2 ÷ 75 = 0,20 für C44 oder 60 ÷ 2 ÷ 63 = 0,48 für MM bei doppelt so langem
  Anstieg. Er führt die Spanne 0,20–0,48 als gekennzeichnete Abschätzung (Kap. 3.4, „Abschätzung des
  Transient-Faktors“; Kap. 3.5, Zeichentabelle, Zeile τ). Berlin läge damit um 52–80 % niedriger, bei
  2,34–5,60 Mio. € (Preisstand 2024) je Jahr (Kap. 3.0, Punkt „Lesart τ = 1“), der Bund bei 67 statt 339 Mio. € (Kap. 4,
  Bändertabelle). Das ist die größte Achse des Berichts, und sie ist einseitig: Sie „kann das Ergebnis nur senken“
  (Kap. 4). Im Ausweis steht τ = 1 (Kap. 3.4). Weil der Barwert linear im Jahresbetrag ist, sänke er im selben
  Verhältnis. Mit τ = 0,20–0,48 in allen 41 Jahren läge er bei 93,9–225,3 Mio. € zur RZPR 0 % und bei
  77,6–186,2 Mio. € zur RZPR 1 %.
- **Belastungsjahr: derselbe Betrag, später gebucht (Befund B5; nach Regel D ausgeschlossen).** Läse man den Betrag
  eines Jahres als Folge der Belastung dieses Jahres, träte der Schaden erst Jahrzehnte später ein, und Regel D zinste
  ihn stärker ab. Bis Schritt 4 ließ die Festlegung offen, ob Regel D nach dem Jahr des Schadens oder nach dem Jahr der
  Belastung abzinst (Befund B5). Seit der Schlussprüfung zinst sie nach dem Jahr des Schadenseintritts ab; dieser Weg
  entfällt damit. Die Zahlen bleiben als Prüffall stehen, damit die Größe der verworfenen Wahl sichtbar ist.
  Prüffall, keine Zahl aus einer Quelle: Je zehn Jahre, um die der Schaden später angesetzt würde, sänke der Barwert um
  1,0 % zur RZPR 0 % und um 10 % zur RZPR 1 % (1 ÷ 1,001 hoch 10 = 0,990 und 1 ÷ 1,011 hoch 10 = 0,896).

**Überlagern sich beide Wege? Nein, sie schließen einander aus.** τ bucht den Schaden in dem Jahr, in dem er eintritt,
und kürzt dafür den Betrag. Die Verschiebung lässt den Betrag voll und bucht ihn im späteren Jahr. Beides zugleich
zählte dieselbe Verzögerung zweimal. Bericht 98 schließt das bei der Maßnahme S155 aus demselben Grund aus: τ zusätzlich
zur Rampe anzusetzen ist verworfen, „weil dieselbe Einlaufzeit zweimal zählte“ (Entscheidungslog Nr. 35 des Berichts).
Jeder der beiden Wege für sich senkt den Barwert; die Kette mit vollem Betrag im Jahr des Betrags liegt über beiden.
**Entschieden ist der erste Weg** (Festlegung, Punkt „Jahr des Schadenseintritts“; Entscheidungslog Nr. 23): Regel D
zinst nach dem Jahr des Schadens ab, und offen bleibt allein τ. Das ist eine Frage an den Bericht, und er hat sie mit
τ = 1 im Ausweis entschieden (Entscheidungslog Nr. 14 des Berichts). Der zweite Weg hätte eine Verschiebung mit einer
belegten Latenz in Jahren gebraucht; der Bericht nennt nur „Jahrzehnte“ (Kap. 6, Modellgrenze 1). Zur RZPR 1 % hätten
schon zehn Jahre Verschiebung in der Größenordnung der Wahl der RZPR gelegen: −10 % gegen −17 %. Bei zwei Jahrzehnten
läge die Verschiebung mit −20 % darüber (1 ÷ 1,011 hoch 20 = 0,803). Deshalb war die Frage in der Festlegung zu
entscheiden und nicht still in dieser Kette. An den Barwerten der Kette ändert die Entscheidung nichts, weil die Kette
schon nach dem ersten Weg rechnet.

**Wie weit die Spanne mit τ trägt (Folgerung von KAP3 aus Bericht 98, Kap. 3.4, keine Zahl des Berichts).** Bericht 98
gibt τ für die Menschen an, die heute erkranken. Bleibt die Dosis auf dem heutigen Stand, entsteht von Jahr zu Jahr ein
größerer Teil der Lebenszeitdosis unter ihr, und τ wächst über 2025–2065 Richtung 1. Prüffall mit der Formel des
Berichts, keine Zahl des Berichts: Ist die Dosis über T = 30 Jahre gestiegen und bleibt danach J Jahre auf dem neuen
Stand, ist die Lebenszeitdosis eines Menschen, der mit 75 Jahren erkrankt, so stark gestiegen wie in T ÷ 2 + J Jahren
mit voll erhöhter Dosis; τ ist dieser Wert geteilt durch 75. Für C44 wird aus τ = 15 ÷ 75 = 0,20 im Jahr 2025 dann (15 + 40) ÷ 75 = 0,73 im Jahr 2065. Dieselbe Überlegung trägt die
Rampe der Maßnahme S155 (Kap. 5, Absatz „Latenz: Sprung der Dosis, Rampe der Wirkung“). Die Spanne oben setzt τ in allen
41 Jahren gleich. Ihr unterer Rand ist deshalb die tiefste Lage des Barwerts unter einer Jahres-Attribution: nicht unter
93,9 Mio. € zur RZPR 0 % und 77,6 Mio. € zur RZPR 1 %, also höchstens 80 % unter der Kette. Wo der Barwert zwischen
diesem Rand und der Kette läge, rechnet weder Bericht 98 noch diese Datei. Dafür bräuchte es das Kohorten-Latenzmodell,
das der Bericht für die Stufe M2+ nennt (Entscheidungslog Nr. 14 des Berichts).

**Behandlungskosten mit demselben Wert, #98.** Bei #98 hängt nur ein Drittel des Betrags an der Abschätzung „derselbe
Wert“ (3,83 von 11,68 Mio. €). Bekämen allein die Behandlungskosten eine andere Komponente, änderte sich der Barwert zur
RZPR 0 % bei 0 Pp. um +0,7 %, bei 0,7 Pp. um −3,6 % und im Fall −0,5 Pp. um +4,3 % (zur RZPR 1 %: +0,6 %, −3,3 %,
+3,9 %). Das ist ein Drittel der Wirkung bei #96.

```python test: diskontrate_m0
# Rechenkette Diskontrate, #95 Hitzebelastung, Beispielkommune Berlin: Jahresbetrag -> Barwert nach Regel D
jahresbetrag = 362.9                 # Mio. EUR je Jahr (Preisstand 2024), Bericht 95, Kap. 3.0, Ebene 10
jahre = list(range(2025, 2066))      # Zeitraum 2025-2065, Bezugsjahr 2025
komponente = 0.001                   # Veraenderung der relativen Preise, 0,1 Pp. (Festlegung)
rzpr = (0.0, 0.01)                   # beide Werte werden ausgewiesen (MK 4.0, S. 10)

def faktor(d, jahr):                 # Ebenen 4 und 8
    return 1 / (1 + d) ** (jahr - 2025)

def barwertfaktor(d):                # Ebenen 5 und 9
    return sum(faktor(d, j) for j in jahre)

def barwert(d, betrag=jahresbetrag): # Ebenen 6 und 10, Betrag gleich in jedem Jahr
    return betrag * barwertfaktor(d)

def zehner(d):                       # Summen je Jahrzehnt und das Jahr 2065
    return [sum(faktor(d, j) for j in range(a, a + 10)) for a in (2025, 2035, 2045, 2055)] + [faktor(d, 2065)]

assert len(jahre) == 41
# Ebene 2: Summe ohne Abzinsung
assert abs(jahresbetrag * 41 / 1000 - 14.88) < 0.005
# Ebenen 3 und 7: Diskontrate nach Regel D
regel = [round(r + komponente, 4) for r in rzpr]
assert regel == [0.001, 0.011]
# Ebene 4 und 8: Abzinsfaktoren 2025, 2035, 2045, 2055, 2065
for d, soll in zip(regel, [[1.000, 0.990, 0.980, 0.970, 0.961], [1.000, 0.896, 0.803, 0.720, 0.646]]):
    for j, s in zip((2025, 2035, 2045, 2055, 2065), soll):
        assert abs(faktor(d, j) - s) < 0.0005
# Ebene 5 und 9: Barwertfaktor, je Jahrzehnt
for d, soll, summe in zip(regel, [[9.955, 9.856, 9.758, 9.661, 0.961], [9.524, 8.537, 7.653, 6.860, 0.646]], [40.19, 33.22]):
    for ist, s in zip(zehner(d), soll):
        assert abs(ist - s) < 0.0005
    assert abs(sum(zehner(d)) - barwertfaktor(d)) < 1e-9
    assert abs(barwertfaktor(d) - summe) < 0.005
# Ebene 6 und 10: Barwert nach Regel D in Mrd. EUR
bw_regel = [barwert(d) / 1000 for d in regel]
assert abs(bw_regel[0] - 14.59) < 0.005 and abs(bw_regel[1] - 12.06) < 0.005
# Sensitivitaet: Diskontrate 0 % und 1 % (RZPR allein, Komponente 0)
bw_0, bw_1 = barwert(0.0) / 1000, barwert(0.01) / 1000
assert abs(barwertfaktor(0.01) - 33.83) < 0.005
assert abs(bw_0 - 14.88) < 0.005 and abs(bw_1 - 12.28) < 0.005
abw_0 = bw_0 / bw_regel[0] - 1       # 0 % gegen 0,1 % (gleiche RZPR 0 %)
abw_1 = bw_1 / bw_regel[1] - 1       # 1 % gegen 1,1 % (gleiche RZPR 1 %)
assert abs(abw_0 - 0.020) < 0.0005 and abs(abw_1 - 0.019) < 0.0005
# Spannweite ueber alle vier Varianten und staerkster Treiber (Wahl der RZPR)
assert abs(bw_regel[1] / bw_regel[0] - 1 + 0.173) < 0.0005
assert abs(bw_0 / bw_regel[1] - 1 - 0.234) < 0.0005
# Kette und Produkt: Zelllauf Berlin mit Gemeindeschluessel 345,11 Mio. EUR, 5 % unter der Kette (Bericht 95, Kap. 3.0)
assert abs(345.11 / jahresbetrag - 1 + 0.05) < 0.005
assert abs(barwert(0.001, 345.11) / 1000 - 13.87) < 0.005 and abs(barwert(0.011, 345.11) / 1000 - 11.46) < 0.005
# Pruefall zum Verlauf (keine Projektion): Jahresbetrag steigt gleichmaessig bis 2065 auf das Doppelte
steigend = lambda d: sum(jahresbetrag * (1 + (j - 2025) / 40) * faktor(d, j) for j in jahre) / 1000
assert abs(steigend(0.001) - 21.83) < 0.005 and abs(steigend(0.011) - 17.62) < 0.005
assert abs(steigend(0.001) / bw_regel[0] - 1.50) < 0.005 and abs(steigend(0.011) / bw_regel[1] - 1.46) < 0.005
assert abs(steigend(0.0) / steigend(0.001) - 1 - 0.0225) < 0.0005
assert abs(steigend(0.01) / steigend(0.011) - 1 - 0.0209) < 0.0005

# --- #96 Aeroallergene, Beispielkommune Berlin: dieselben Ebenen, Betrag in Mio. EUR
jahresbetrag_96 = 2.53               # Mio. EUR je Jahr (Preisstand 2024), Bericht 96, Kap. 3.0, Ebene 10 (Rev. 4, a_attr 0,27)
# Ebene 2: Summe ohne Abzinsung
assert abs(jahresbetrag_96 * 41 - 103.7) < 0.05
# Ebenen 3-5 und 7-9 wie #95; Ebene 6 und 10: Barwert nach Regel D
bw96_regel = [barwert(d, jahresbetrag_96) for d in regel]
assert abs(bw96_regel[0] - 101.7) < 0.05 and abs(bw96_regel[1] - 84.0) < 0.05
assert abs(jahresbetrag_96 * 40.19 - 101.7) < 0.05 and abs(jahresbetrag_96 * 33.22 - 84.0) < 0.05
# Sensitivitaet: Diskontrate 0 % und 1 % (RZPR allein, Komponente 0)
bw96_0, bw96_1 = barwert(0.0, jahresbetrag_96), barwert(0.01, jahresbetrag_96)
assert abs(bw96_0 - 103.7) < 0.05 and abs(bw96_1 - 85.6) < 0.05
abw96_0 = bw96_0 / bw96_regel[0] - 1 # 0 % gegen 0,1 % (gleiche RZPR 0 %)
abw96_1 = bw96_1 / bw96_regel[1] - 1 # 1 % gegen 1,1 % (gleiche RZPR 1 %)
assert abs(abw96_0 - 0.020) < 0.0005 and abs(abw96_1 - 0.019) < 0.0005
# Spannweite ueber alle vier Varianten und staerkster Treiber (Wahl der RZPR)
assert abs(bw96_regel[1] / bw96_regel[0] - 1 + 0.173) < 0.0005
assert abs(bw96_0 / bw96_regel[1] - 1 - 0.234) < 0.0005
# Kette und Produkt: Zelllauf Berlin 2,47 Mio. EUR, 2,2 % unter der Kette (Bericht 96, Kap. 3.0, "Kommune statt Zellen")
assert abs(2.47 / jahresbetrag_96 - 1 + 0.022) < 0.005
assert abs(2.47 * barwertfaktor(0.001) - 99.3) < 0.05 and abs(2.47 * barwertfaktor(0.011) - 82.1) < 0.05
# Behandlungskosten mit derselben Komponente: Bandgrenzen 0 und 0,7 Pp., Fall -0,5 Pp.; RZPR 0 % und 1 %
for k, s0, s1, a0, a1 in ((0.0, 103.7, 85.6, 0.020, 0.019), (0.007, 90.5, 75.5, -0.110, -0.101),
                          (-0.005, 114.9, 94.0, 0.130, 0.119)):
    r0, r1 = barwert(k, jahresbetrag_96), barwert(0.01 + k, jahresbetrag_96)
    assert abs(r0 - s0) < 0.05 and abs(r1 - s1) < 0.05
    assert abs(r0 / bw96_regel[0] - 1 - a0) < 0.0005 and abs(r1 / bw96_regel[1] - 1 - a1) < 0.0005
# Band des Klimaanteils im Jahresbetrag, 1,78-3,84 Mio. EUR (Bericht 96, Kap. 3.0, "Staerkster Treiber"), als Barwert
assert abs(1.78 / jahresbetrag_96 - 1 + 0.30) < 0.005 and abs(3.84 / jahresbetrag_96 - 1 - 0.52) < 0.005
assert abs(1.78 * barwertfaktor(0.001) - 71.5) < 0.05 and abs(3.84 * barwertfaktor(0.001) - 154.3) < 0.05
assert abs(1.78 * barwertfaktor(0.011) - 59.1) < 0.05 and abs(3.84 * barwertfaktor(0.011) - 127.6) < 0.05

# --- #98 UV-Schaedigungen, Beispielkommune Berlin: dieselben Ebenen, Betrag in Mio. EUR
jahresbetrag_98 = 11.68              # Mio. EUR je Jahr (Preisstand 2024), Bericht 98, Kap. 3.0, Ebene 10, Zeile 310
mort_98 = 4.97 + 2.87                # YLL x VOLY, MM und C44 (Bericht 98, Kap. 3.0, Ebene 9)
beh_98 = 0.1734 + 3.66               # Behandlung, MM und C44 (Ebene 9)
assert abs(mort_98 + beh_98 - jahresbetrag_98) < 0.01            # Ebene 10 aus Ebene 9, Rundung der Ebene 9
anteil_beh = beh_98 / (mort_98 + beh_98)
assert abs(mort_98 / jahresbetrag_98 - 0.67) < 0.005 and abs(anteil_beh - 0.33) < 0.005
# Ebene 2: Summe ohne Abzinsung
assert abs(jahresbetrag_98 * 41 - 478.9) < 0.05
# Ebenen 3-5 und 7-9 wie #95; Ebene 6 und 10: Barwert nach Regel D
bw98_regel = [barwert(d, jahresbetrag_98) for d in regel]
assert abs(bw98_regel[0] - 469.4) < 0.05 and abs(bw98_regel[1] - 388.0) < 0.05
assert abs(jahresbetrag_98 * 40.19 - 469.4) < 0.05 and abs(jahresbetrag_98 * 33.22 - 388.0) < 0.05
# Sensitivitaet: Diskontrate 0 % und 1 % (RZPR allein, Komponente 0)
bw98_0, bw98_1 = barwert(0.0, jahresbetrag_98), barwert(0.01, jahresbetrag_98)
assert abs(bw98_0 - 478.9) < 0.05 and abs(bw98_1 - 395.2) < 0.05
abw98_0 = bw98_0 / bw98_regel[0] - 1 # 0 % gegen 0,1 % (gleiche RZPR 0 %)
abw98_1 = bw98_1 / bw98_regel[1] - 1 # 1 % gegen 1,1 % (gleiche RZPR 1 %)
assert abs(abw98_0 - 0.020) < 0.0005 and abs(abw98_1 - 0.019) < 0.0005
# Spannweite ueber alle vier Varianten und staerkster Treiber (Wahl der RZPR)
assert abs(bw98_regel[1] / bw98_regel[0] - 1 + 0.173) < 0.0005
assert abs(bw98_0 / bw98_regel[1] - 1 - 0.234) < 0.0005
# Latenz, Pruefall (keine Zahl aus einer Quelle): Schaden je zehn Jahre spaeter angesetzt
assert abs(faktor(0.001, 2035) - 1 + 0.010) < 0.0005 and abs(faktor(0.011, 2035) - 1 + 0.104) < 0.0005
assert abs(faktor(0.001, 2035) - 0.990) < 0.0005 and abs(faktor(0.011, 2035) - 0.896) < 0.0005
# Zur RZPR 1 %: zehn Jahre (-10 %) unter der Wahl der RZPR (-17 %), zwei Jahrzehnte (-20 %, Faktor 0,803) darueber
assert abs(faktor(0.011, 2045) - 0.803) < 0.0005 and abs(1 - faktor(0.011, 2045) - 0.20) < 0.005
assert 1 - faktor(0.011, 2035) < 1 - bw98_regel[1] / bw98_regel[0] < 1 - faktor(0.011, 2045)
# Transient-Faktor tau = (T/2)/a_erk, Spanne 0,20-0,48 (Bericht 98, Kap. 3.4), in allen 41 Jahren gleich angesetzt
assert abs(30 / 2 / 75 - 0.20) < 0.005 and abs(60 / 2 / 63 - 0.48) < 0.005
# Berlin je Jahr mit tau 2,34-5,60 Mio. EUR (Bericht 98, Kap. 3.0, Punkt "Lesart tau = 1")
assert abs(jahresbetrag_98 * 0.20 - 2.34) < 0.01 and abs(jahresbetrag_98 * 0.48 - 5.60) < 0.01
for t, s0, s1 in ((0.20, 93.9, 77.6), (0.48, 225.3, 186.2)):
    assert abs(t * bw98_regel[0] - s0) < 0.05 and abs(t * bw98_regel[1] - s1) < 0.05
# Richtung von tau ueber 2025-2065 (Pruefall mit der Formel des Berichts, Regel D: Jahr des Schadenseintritts):
# Dosis ueber T = 30 Jahre gestiegen, danach J Jahre gleich; C44, Erkrankungsalter 75
tau_c44 = lambda j: (30 / 2 + j) / 75
assert abs(tau_c44(0) - 0.20) < 0.005 and abs(tau_c44(40) - 0.73) < 0.005
assert all(tau_c44(j + 1) > tau_c44(j) for j in range(40)) and tau_c44(40) < 1
# Schwankung von #98 ueber die vier Varianten bei tau = 0,20: 18,2 statt 90,9 Mio. EUR, in Prozent weiter 23 %
assert abs((bw98_0 - bw98_regel[1]) * 0.20 - 18.2) < 0.05
# Behandlungskosten (ein Drittel) mit anderer Komponente, Rest nach Regel D; RZPR 0 % und 1 %
for k, a0, a1 in ((0.0, 0.007, 0.006), (0.007, -0.036, -0.033), (-0.005, 0.043, 0.039)):
    r0 = (1 - anteil_beh) * barwertfaktor(0.001) + anteil_beh * barwertfaktor(k)
    r1 = (1 - anteil_beh) * barwertfaktor(0.011) + anteil_beh * barwertfaktor(0.01 + k)
    assert abs(r0 / barwertfaktor(0.001) - 1 - a0) < 0.0005 and abs(r1 / barwertfaktor(0.011) - 1 - a1) < 0.0005
# Spannweite in Euro je Klimawirkung: am groessten bei #95, weil der Jahresbetrag am groessten ist
spanne = {"95": bw_0 * 1000 - bw_regel[1] * 1000, "96": bw96_0 - bw96_regel[1], "98": bw98_0 - bw98_regel[1]}
assert max(spanne, key=spanne.get) == "95" and abs(spanne["95"] / 1000 - 2.82) < 0.005
assert abs(spanne["96"] - 19.7) < 0.05 and abs(spanne["98"] - 90.9) < 0.05
assert round(jahresbetrag / jahresbetrag_98) == 31 and round(jahresbetrag / jahresbetrag_96) == 143
assert abs(1.09 / jahresbetrag - 0.003) < 0.0005    # Behandlungsanteil #95 (Bericht 95, Kap. 3.0, Ebene 9)

de = lambda x, n=2: f"{x:,.{n}f}".replace(",", "X").replace(".", ",").replace("X", ".")
print(f"Barwert nach Regel D, RZPR 0 % (Rate 0,1 %): {de(bw_regel[0])} Mrd. €, Barwertfaktor {de(barwertfaktor(0.001))}")
print(f"Barwert nach Regel D, RZPR 1 % (Rate 1,1 %): {de(bw_regel[1])} Mrd. €, Barwertfaktor {de(barwertfaktor(0.011))}")
print(f"Barwert zur Diskontrate 0 %: {de(bw_0)} Mrd. €, Abweichung zur Regel (RZPR 0 %) {de(abw_0 * 100, 1)} %")
print(f"Barwert zur Diskontrate 1 %: {de(bw_1)} Mrd. €, Abweichung zur Regel (RZPR 1 %) {de(abw_1 * 100, 1)} %")
print(f"#96: Barwert nach Regel D, RZPR 0 % (Rate 0,1 %): {de(bw96_regel[0], 1)} Mio. €, Barwertfaktor {de(barwertfaktor(0.001))}")
print(f"#96: Barwert nach Regel D, RZPR 1 % (Rate 1,1 %): {de(bw96_regel[1], 1)} Mio. €, Barwertfaktor {de(barwertfaktor(0.011))}")
print(f"#96: Barwert zur Diskontrate 0 %: {de(bw96_0, 1)} Mio. €, Abweichung zur Regel (RZPR 0 %) {de(abw96_0 * 100, 1)} %")
print(f"#96: Barwert zur Diskontrate 1 %: {de(bw96_1, 1)} Mio. €, Abweichung zur Regel (RZPR 1 %) {de(abw96_1 * 100, 1)} %")
print(f"#98: Barwert nach Regel D, RZPR 0 % (Rate 0,1 %): {de(bw98_regel[0], 1)} Mio. €, Barwertfaktor {de(barwertfaktor(0.001))}")
print(f"#98: Barwert nach Regel D, RZPR 1 % (Rate 1,1 %): {de(bw98_regel[1], 1)} Mio. €, Barwertfaktor {de(barwertfaktor(0.011))}")
print(f"#98: Barwert zur Diskontrate 0 %: {de(bw98_0, 1)} Mio. €, Abweichung zur Regel (RZPR 0 %) {de(abw98_0 * 100, 1)} %")
print(f"#98: Barwert zur Diskontrate 1 %: {de(bw98_1, 1)} Mio. €, Abweichung zur Regel (RZPR 1 %) {de(abw98_1 * 100, 1)} %")
```

Ausgabe des Blocks (gelaufen am 07.10.2026; die ersten vier Zeilen gelten für #95, die mit „#96:“ für #96, die mit
„#98:“ für #98):

```text
Barwert nach Regel D, RZPR 0 % (Rate 0,1 %): 14,59 Mrd. €, Barwertfaktor 40,19
Barwert nach Regel D, RZPR 1 % (Rate 1,1 %): 12,06 Mrd. €, Barwertfaktor 33,22
Barwert zur Diskontrate 0 %: 14,88 Mrd. €, Abweichung zur Regel (RZPR 0 %) 2,0 %
Barwert zur Diskontrate 1 %: 12,28 Mrd. €, Abweichung zur Regel (RZPR 1 %) 1,9 %
#96: Barwert nach Regel D, RZPR 0 % (Rate 0,1 %): 101,7 Mio. €, Barwertfaktor 40,19
#96: Barwert nach Regel D, RZPR 1 % (Rate 1,1 %): 84,0 Mio. €, Barwertfaktor 33,22
#96: Barwert zur Diskontrate 0 %: 103,7 Mio. €, Abweichung zur Regel (RZPR 0 %) 2,0 %
#96: Barwert zur Diskontrate 1 %: 85,6 Mio. €, Abweichung zur Regel (RZPR 1 %) 1,9 %
#98: Barwert nach Regel D, RZPR 0 % (Rate 0,1 %): 469,4 Mio. €, Barwertfaktor 40,19
#98: Barwert nach Regel D, RZPR 1 % (Rate 1,1 %): 388,0 Mio. €, Barwertfaktor 33,22
#98: Barwert zur Diskontrate 0 %: 478,9 Mio. €, Abweichung zur Regel (RZPR 0 %) 2,0 %
#98: Barwert zur Diskontrate 1 %: 395,2 Mio. €, Abweichung zur Regel (RZPR 1 %) 1,9 %
```

**Sensitivität gegenüber 0 % und 1 %.** Die Varianten 0 % und 1 % sind die RZPR allein, also der heutige Stand im
Produkt (Befund C1). Jede Variante wird mit dem Barwert nach Regel D zur selben RZPR verglichen: 0 % mit 0,1 %, 1 % mit
1,1 %.

| Klimawirkung | Barwert nach Regel | Barwert 0 % | Barwert 1 % | Abweichung zur Regel in % |
|---|---|---|---|---|
| #95 Hitzebelastung, Beispielkommune Berlin | 14,59 Mrd. € (RZPR 0 %, Rate 0,1 %) · 12,06 Mrd. € (RZPR 1 %, Rate 1,1 %) | 14,88 Mrd. € | 12,28 Mrd. € | 0 % gegen 0,1 %: +2,0 % · 1 % gegen 1,1 %: +1,9 % |
| #96 Aeroallergene, Beispielkommune Berlin | 101,7 Mio. € (RZPR 0 %, Rate 0,1 %) · 84,0 Mio. € (RZPR 1 %, Rate 1,1 %) | 103,7 Mio. € | 85,6 Mio. € | 0 % gegen 0,1 %: +2,0 % · 1 % gegen 1,1 %: +1,9 % |
| #98 UV-Schädigungen, Beispielkommune Berlin | 469,4 Mio. € (RZPR 0 %, Rate 0,1 %) · 388,0 Mio. € (RZPR 1 %, Rate 1,1 %) | 478,9 Mio. € | 395,2 Mio. € | 0 % gegen 0,1 %: +2,0 % · 1 % gegen 1,1 %: +1,9 % |

Zwischen den vier Varianten schwankt der Barwert von #95 von 12,06 bis 14,88 Mrd. €, also um 23 %; davon entfallen
nur 1,9–2,0 % auf die Veränderung der relativen Preise, der **stärkste Treiber** ist die Wahl der RZPR: 1 % statt 0 %
senkt den Barwert nach Regel D um 17 %. Bei #96 (84,0–103,7 Mio. €) und #98 (388,0–478,9 Mio. €) ist es genauso: 23 %
Spannweite, stärkster Treiber die Wahl der RZPR mit 17 %. Das gilt unter den vier Varianten der Diskontrate, nicht für
den Barwert insgesamt. Stärker wirken die stärksten Treiber der Jahresbeträge, die der Barwert im selben Verhältnis
übernimmt: bei #95 die Temperatur (0,5 K kühler oder wärmer: −23 … +27 %, Bericht 95, Kap. 3.0, „Stärkster Treiber“),
bei #96 der Klimaanteil (−30 … +52 %, Bericht 96, Kap. 3.0, „Stärkster Treiber“), bei #98 einseitig der
Transient-Faktor τ (bis −80 %) und zweiseitig die Übersetzung von Sonnenschein in UV-Dosis \(k_{\text{UV}}\) (±49 %;
Bericht 98, Kap. 3.0, „Stärkster Treiber“, und Kap. 4).

**Am stärksten schwankt der Barwert von #95, und zwar in Euro:** um 2,82 Mrd. € gegen 90,9 Mio. € bei #98 und
19,7 Mio. € bei #96, weil sein Jahresbetrag 31-mal so groß ist wie der von #98 und 143-mal so groß wie der von #96. In
Prozent schwanken alle drei gleich stark, um 23 %. Der Grund: Jede Kette multipliziert einen gleichbleibenden
Jahresbetrag mit denselben beiden Barwertfaktoren, und die Klimawirkung bestimmt nur den Jahresbetrag, nicht die Rate.
Unterschiede in Prozent entstünden erst, wenn der Verlauf der Jahresbeträge sich unterschiede (Befunde B1, B2 und B4),
wenn Behandlungskosten eine eigene Komponente bekämen (dann am stärksten #96, ganz Behandlungskosten; #98 zu einem
Drittel; #95 zu 0,3 %) oder wenn bei #98 die Latenz in die Rechnung käme, als Transient-Faktor τ, der über die Jahre
wächst (Absatz „Wann der Schaden eintritt“; eine Verschiebung nach dem Jahr der Belastung schließt Regel D aus,
Entscheidungslog Nr. 23). Ein
in allen Jahren gleicher τ senkte nur den Betrag: Bei τ = 0,20 schwankte der Barwert von #98 um 18,2 statt 90,9 Mio. €,
in Prozent weiter um 23 %.

**Was eine einfachere Rechnung verfälschen würde (§8 E3):**

- **Jahresbetrag × 41 ohne Abzinsung** (Ebene 2) ist der Barwert zur Diskontrate 0 %. Er liegt 2,0 % über dem Barwert
  nach Regel D zur RZPR 0 % und 23 % über dem zur RZPR 1 %. Er zeigt nur eine der beiden Wertentscheidungen, die MK 4.0
  verlangt (S. 10).
- **Gleichbleibender Jahresbetrag.** Steigt der Jahresbetrag mit dem Klimasignal, steigt der Barwert. Die Abweichungen in
  Prozent ändern sich dabei kaum. Prüffall, keine Projektion: Verdoppelt sich der Jahresbetrag gleichmäßig bis 2065,
  liegt der Barwert nach Regel D bei 21,83 Mrd. € (RZPR 0 %) und 17,62 Mrd. € (RZPR 1 %), also 50 % bzw. 46 % höher.
  Die Abweichung der Variante 0 % steigt nur von 2,0 % auf 2,3 %, die der Variante 1 % von 1,9 % auf 2,1 %. Die
  Aussage der Sensitivität hängt also nicht am Verlauf, der Betrag des Barwerts schon. Mit dem Ist-Klima in jedem Jahr
  liegt er bei einem wärmer werdenden Klima zu niedrig (Befunde B1, B2 und B4). Bei #98 auch deshalb, weil der Bericht
  für Szenarien eine weiter steigende UV-B-Belastung nennt und die Inzidenz als stationär ansetzt, obwohl sie real
  steigt (Bericht 98, Kap. 6, Absatz „Szenario-Anwendung 98-A“). **Für #98 ist der Barwert trotzdem keine
  Untergrenze**, weil die Latenz in die andere Richtung wirkt: Eine Jahres-Attribution läge um bis zu 80 % niedriger
  als der Jahresbetrag (Transient-Faktor τ = 0,20); der Ausweis liegt damit bis zum Fünffachen über ihr (Absatz „Wann
  der Schaden eintritt“). Nach dem, was der
  Bericht beziffert, überwiegt diese Richtung: τ ist seine größte Achse (Kap. 4). Den Anstieg der UV-B-Belastung nennt
  er nur als Plausibilisierungsrahmen (UV-B-Projektion +1,3 % je Dekade für 2050–2100), die steigende Inzidenz ohne
  Zahl; wie stark der Verlauf auf den Jahresbetrag wirkt, beziffert er nicht (Kap. 6, Absatz
  „Szenario-Anwendung 98-A“; Kap. 8, Quelle [32]). „Untergrenze“ nennt Bericht 98 seinen Betrag, weil Teile fehlen,
  etwa die Augenschäden und die Produktivität; diese gehört zum Konto K2, und in M0 ist nur K1 aktiv (Kap. 1,
  „Konto-Einbettung“; Kap. 6, Modellgrenze 6). Außerdem folgt innerhalb von K1 die Wahl einzelner Parameter einer
  „Untergrenzen-Zusage“, etwa die der Kostensätze (Kap. 3.4, Punkt \(c_e\); Entscheidungslog Nr. 7 des Berichts).
  Diese Zusage schränkt der Bericht selbst ein, weil die Änderung der Dosis eher überschätzt wird (Kap. 3.2; Kap. 6,
  Modellgrenze 2). Beide Richtungen stellt er in Infokasten 1 nebeneinander (Kap. 6): fünf bewusst überschätzende
  Näherungen, deren größte die Gleichgewichtslesart der Latenz ist,
  „und mehrere *unterschätzende* (nur Konto K1, nur Erstjahreskosten, geparkte Sensitivitäten)“. Unter den Achsen, die
  nur nach oben wirken, beziffert er höchstens +11,3 % je Achse (Verhaltens-Sensitivität, Kap. 4); die fehlenden Teile
  des Kontos und die Folgejahre der Behandlung beziffert er nicht (Kap. 3.4, Punkt \(c_e\); Kap. 4, Schluss der
  „Unsicherheiten“; Kap. 6, Modellgrenze 6).

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

Zur Rechenkette (Schritt 2); Regel D bleibt dabei unverändert:

12. **Ein steigender Jahresbetrag in der Rechenkette von #95** ist verworfen, weil Bericht 95 in M0 nur das Ist-Klima
    ausweist (Kap. 6, Zeile 1008) und jeder angesetzte Anstieg eine Zahl ohne Quelle wäre; der Prüffall mit Verdopplung
    bis 2065 zeigt, dass die Abweichungen in Prozent sich dadurch um höchstens 0,3 Pp. ändern (Abschnitt „Rechenkette“).
    *Fortgeschrieben in Nr. 17:* Der Verweis lautet jetzt Kap. 6, Absatz „Szenario-Anwendung 95-A“.
13. **Der Zelllauf des Produkts (rund 338 Mio. € je Jahr) als Jahresbetrag der Kette** ist verworfen, weil die Kette an
    die letzte Ebene der Rechenkette 3.0 anschließen soll; der Barwert des Zelllaufs steht als Umrechnung mit dem Faktor
    0,932 daneben. *Fortgeschrieben in Nr. 17:* Der Zelllauf steht jetzt mit 345,11 Mio. € je Jahr, ohne Umrechnung.

Zur Rechenkette von #96 (Schritt 3); Regel D und die Werte für #95 bleiben dabei unverändert:

14. **Der ungerundete Betrag 755.753 × 6,20 € = 4,686 Mio. € als Jahresbetrag der Kette für #96** ist verworfen, weil
    die Kette die Zahl der letzten Ebene übernimmt, wie Bericht 96 sie ausweist (4,69 Mio. €, Zeile 304), so wie bei #95;
    der Unterschied im Barwert ist 0,09 %. *Fortgeschrieben in Nr. 18:* Die Begründung gilt weiter, die Werte sind
    408.106 × 6,20 € = 2,530 Mio. € gegen 2,53 Mio. € (Kap. 3.0, Ebene 10), Unterschied 0,01 %.
15. **Der Zelllauf des Produkts (4,59 Mio. € je Jahr) als Jahresbetrag der Kette für #96** ist verworfen, aus demselben
    Grund wie Nr. 13; sein Barwert steht daneben (184,5 und 152,5 Mio. €). *Fortgeschrieben in Nr. 18:* Der Zelllauf
    steht jetzt mit 2,47 Mio. € je Jahr und den Barwerten 99,3 und 82,1 Mio. €.
16. **Ein eigener Wert der Komponente für #96, weil sein Betrag ganz aus Behandlungskosten besteht,** ist verworfen, weil
    Nr. 8 dafür weiter gilt und die Wirkung am Endstand beziffert ist: im Band +2,0 % bis −11 %, im Fall −0,5 Pp. +13 %,
    jeweils weniger als die Wahl der RZPR (Abschnitt „Rechenkette“).

Nachzug auf den Endstand der Berichte 95 und 96 (Schritt 4). Regel D, ihre Werte und die Rechenkette für #95 von
Ebene 1 bis 10 bleiben unverändert; geändert sind die Werte des Zelllaufs von #95 und alle Euro-Werte von #96:

17. **Bericht 95: Verweise und Zelllauf.** Die Verweise auf Bericht 95 nennen jetzt Abschnitt und Ebene statt Zeilen
    (Nachtrag des CEO zu T-1245, 26.09.2026). Der Zelllauf von #95 steht mit 345,11 Mio. € je Jahr und den Barwerten
    13,87 und 11,46 Mrd. €. Bis Schritt 3 stand hier rund 338 Mio. € (Faktor 0,932) mit 13,59 und 11,24 Mrd. €.
    **Begründung:** Bericht 95 weist als Betrag für Berlin den Zelllauf mit Gemeindeschlüssel aus, 345,11 Mio. €, 5 % unter
    der Kette (Kap. 3.0, Punkt „Ebenen 1, 2 und 6, eine Zelle statt aller Zellen“). Die alten Zeilenverweise zeigten auf
    andere Stellen. **Verworfen:** die alten Werte stehen zu lassen, weil die Datei dann einen Betrag des Produkts nennte,
    den der Bericht nicht mehr führt. **Gegenargument:** Der Zelllauf ist Messung am Produkt und kann sich mit jedem
    Datenstand wieder ändern; deshalb verweist die Datei auf den Absatz und nicht auf eine Zeile. **Fortgeschrieben
    sind damit:** Nr. 12 (Verweis Kap. 6, Absatz „Szenario-Anwendung 95-A“ statt Zeile 1008) und Nr. 13 (Zelllauf
    345,11 Mio. € je Jahr statt rund 338 Mio. € mit Faktor 0,932).
18. **Bericht 96: Jahresbetrag 2,53 statt 4,69 Mio. €.** Kette, Zelllauf, Behandlungskosten-Tabelle, Band des
    Klimaanteils und Sensitivitätszeile von #96 sind auf den Endstand von Bericht 96 nachgezogen. Neu sind 101,7 und
    84,0 Mio. € nach Regel D, 103,7 und 85,6 Mio. € zur Diskontrate 0 % und 1 %; vorher waren es 188,5, 155,8, 192,3 und
    158,7 Mio. €. **Fortgeschrieben sind damit:** Nr. 14 (ungerundeter Betrag 408.106 × 6,20 € = 2,530 Mio. € gegen
    2,53 Mio. € in Kap. 3.0, Ebene 10, Unterschied im Barwert 0,01 %; vorher 755.753 × 6,20 € = 4,686 Mio. € gegen
    4,69 Mio. €, 0,09 %) und Nr. 15 (Zelllauf 2,47 Mio. € je Jahr mit den Barwerten 99,3 und 82,1 Mio. €; vorher
    4,59 Mio. € mit 184,5 und 152,5 Mio. €). **Begründung:** Nach Schritt 3 hat Bericht 96 den Klimaanteil von 0,50 auf 0,27 gesenkt (Statuskopf,
    Runden 30–32, Befund 258) und ist am 30.09.2026 abgenommen. Der Jahresbetrag der letzten Ebene ist seither 2,53 Mio. €.
    Die Abweichungen in Prozent bleiben gleich (+2,0 %, +1,9 %, 23 %, 17 %; Behandlungskosten +2,0 % bis −11 %, −0,5 Pp.
    +13 %), weil sich nur der Jahresbetrag geändert hat. **Verworfen:** Schritt 3 unverändert stehen zu lassen und die
    Änderung nur als Befund zu führen, weil die Sensitivitätstabelle dann für #96 einen Barwert zeigte, der 85 % über dem
    Bericht liegt (P3: nie so, dass das Ergebnis die Lage falsch darstellt). **Gegenargument:** Das Paket war für #98
    geschnitten; der Nachzug von #96 vergrößert den Prüfumfang. Das Abnahmekriterium von T-1245 lässt ihn mit Begründung
    an dieser Stelle zu.

Zur Rechenkette von #98 (Schritt 4); Regel D und die Werte für #95 und #96 nach Nr. 17 und 18 bleiben dabei unverändert:

19. **Die Summe der gerundeten Ebene 9 (7,84 + 3,83 = 11,67 Mio. €) als Jahresbetrag der Kette für #98** ist verworfen,
    weil die Kette die Zahl der letzten Ebene übernimmt, wie Bericht 98 sie ausweist (11,68 Mio. €, Kap. 3.0, Ebene 10,
    Zeile 310); die Anteile 67 % und 33 % stammen aus Ebene 9.
20. **Eine Verschiebung nach dem Jahr der Belastung (Abzinsung für die Latenz von Hautkrebs) in der Kette für #98** ist
    verworfen, weil die Festlegung nicht sagt, ob Regel D nach dem Jahr des Schadens oder der Belastung abzinst
    (Befund B5), weil Bericht 98 den Jahresbetrag als „eingelaufenes Risiko“ der heutigen Dosislage liest und „nicht die
    späteren Folgen der Belastung dieses Jahres“ (Kap. 3.0, „Lesart des Jahresbetrags“; Kap. 6, Modellgrenze 1), weil
    er „kein Latenz-Discounting“ festlegt (Entscheidungslog Nr. 14 des Berichts) und weil er die Latenz in Jahren nicht
    beziffert, nur „Jahrzehnte“ (Kap. 6, Modellgrenze 1). Eine angesetzte Verschiebung wäre eine stille Änderung der
    Regel mit einer Zahl ohne Quelle. Die Größenordnung steht als Prüffall im Abschnitt „Rechenkette“: je zehn Jahre
    −1,0 % (RZPR 0 %) und −10 % (RZPR 1 %). **Gegenargument:** Zur RZPR 1 % liegt die Wirkung schon bei zehn Jahren in
    der Größenordnung der Wahl der RZPR (−10 % gegen −17 %) und bei zwei Jahrzehnten darüber (−20 %); bis die
    Festlegung entscheidet, kann der Barwert von #98 zur RZPR 1 % deshalb zu hoch sein. *Fortgeschrieben in Nr. 23:*
    Die Festlegung entscheidet jetzt, Regel D zinst nach dem Jahr des Schadenseintritts ab. Die Verschiebung bleibt
    verworfen, nun durch Regel D selbst; das Gegenargument ist damit erledigt.
21. **Ein Barwert des Produkts für #98** ist verworfen, weil Bericht 98 keinen Betrag des Zelllaufs für Berlin nennt und
    eine Umrechnung allein über die 2,1 % weniger Einwohner andere Unterschiede zwischen Kette und Zellen außer Acht ließe.
22. **Der Transient-Faktor τ (0,20–0,48) auf den Jahresbetrag der Kette für #98** ist verworfen, weil Bericht 98 im
    Ausweis bewusst τ = 1 führt (Kap. 3.4: „Der Ausweis bleibt bewusst die Gleichgewichtslesart“; Entscheidungslog
    Nr. 14 des Berichts) und die Kette an die letzte Ebene der Rechenkette 3.0 anschließt; τ ist eine Frage an den
    Bericht, nicht an Regel D. Auch eine Verschiebung zusätzlich zu τ ist verworfen, weil beide dieselbe Verzögerung
    abbilden und zusammen doppelt zählten (Abschnitt „Rechenkette“, „Überlagern sich beide Wege?“; ebenso
    Entscheidungslog Nr. 35 des Berichts). Die Wirkung steht als Spanne im Abschnitt „Rechenkette“: Barwert
    93,9–225,3 Mio. € zur RZPR 0 % und 77,6–186,2 Mio. € zur RZPR 1 %, wenn τ in allen Jahren gleich bliebe.
    **Gegenargument:** Bericht 98 selbst nennt das Ergebnis gegenüber einer Jahres-Attribution überschätzt, und τ ist
    seine größte Achse. Der Barwert von #98 ist deshalb kein vorsichtiger Wert, sondern der Wert in der
    Gleichgewichtslesart, mit einer Spanne nach unten bis −80 %.

Zur Festlegung (Schlussprüfung T-1836, 07.10.2026; Entscheidung des CEO vom 07.10.2026, Befund B5 hier zu entscheiden).
Werte der Regel D und alle Barwerte bleiben unverändert:

23. **Regel D zinst nach dem Jahr des Schadenseintritts ab** (Festlegung, „Bezugsjahr und Zeitraum der Abzinsung“,
    Punkt „Jahr des Schadenseintritts“). **Begründung:** MK 4.0 zinst nach dem Zeitpunkt ab, „zu dem die Kosten und
    Nutzen heutiger Entscheidungen anfallen“, und rechnet die RZPR an dem Nutzen vor, „der in 30 Jahren auftritt“
    (S. 14); als Beispiel nennt sie verzögerte Gesundheitsschäden der Luftverschmutzung, die „erst in ferner Zukunft
    sichtbar“ werden (S. 14). Die Kette für #98 rechnet schon so, weil Bericht 98 mit dem Jahresbetrag die Fälle eines
    Jahres beziffert (Kap. 3.0, „Lesart des Jahresbetrags“); kein Barwert ändert sich. **Folge für τ:** Die Latenz geht
    nur über den Betrag ein; unter einer Jahres-Attribution wächst τ über 2025–2065 und fällt nie, solange die Dosis
    nicht sinkt, sodass ein in allen Jahren gleicher τ der untere Rand ist (Abschnitt „Rechenkette“, Absatz „Wie weit die
    Spanne mit τ trägt“). **Verworfen:** Das Abzinsen nach dem Jahr der Belastung ist verworfen, weil MK 4.0 nach dem
    Eintreten von Kosten und Nutzen abzinst und nicht nach dem Zeitpunkt ihrer Ursache, und weil es für #98 eine Latenz
    in Jahren bräuchte, die der Bericht nicht beziffert (nur „Jahrzehnte“, Kap. 6, Modellgrenze 1). **Gegenargument:**
    Wer eine Maßnahme gegen die Belastung bewertet, will die Folgen der heute vermiedenen Belastung als Ganzes sehen;
    nach dem Jahr des Schadens muss ein Bericht diese Folgen dafür auf die späteren Jahre verteilen. Bericht 98 tut das
    bei S155 mit der Rampe (Kap. 5, Absatz „Latenz: Sprung der Dosis, Rampe der Wirkung“). Den Barwert unter einer
    Jahres-Attribution beziffern weder der Bericht noch diese Datei; Regel D legt nur fest, dass er zwischen dem unteren
    Rand mit gleichem τ und der Kette liegt. **Keine Entscheidung über den Methodik-Zweig hinaus nötig:** Die Wahl ändert keinen
    Barwert und keinen Code (`_discounted()` zinst schon mit dem Jahr der Projektion ab, Abschnitt „Befunde an Code“,
    „Ohne Abweichung“). Was Bericht 98 daraus braucht, steht als Befund B6 unter „Befunde an Berichte“.

## Befunde an Berichte

Gelesen am 06.10.2026, je am Endstand: Bericht 95, Kap. 3.0 (Tabelle, Punkte unter der Tabelle, Block
`rechenkette_95` bis zum Zelllauf), Kap. 3.5 (VOLY-Kette) und Kap. 6 (Szenario-Anwendung, Jahresbeträge ohne Abzinsung). Bericht 96 in
Rev. 4, abgenommen am 30.09.2026: Statuskopf und Revisionsstand, Kap. 1 (Konto-Einbettung), Kap. 2 (Register
96-K1-01), Kap. 3.0 ganz (Tabelle, Absätze unter der Tabelle, Block `rechenkette_96` bis zum Zelllauf) und Kap. 6
(Jahresbeträge ohne Abzinsung, Szenario-Anwendung). Bericht 98 in Rev. 15 vom 05.10.2026: Statuskopf und
Revisionsstand, Kap. 1 ganz, Kap. 2 ganz, Kap. 3 Kopf mit Preisstand, Kap. 3.0 ganz mit Block `rechenkette_98`, Kap. 3.4
ganz (Gleichgewichtslesart und Transient-Faktor, Monetarisierung mit VOLY, Blöcke `beispiel_98_lambda_l_kosten`,
`beispiel_98_bundessumme`, `beispiel_98_beispielzelle`), Kap. 5 Absatz „Latenz: Sprung der Dosis, Rampe der Wirkung“ und
Kap. 6 ganz bis zu den Infokästen. Gesucht in Bericht 98 nach „Diskont“, „abzins“, „abgezins“, „Barwert“, „T-1116“,
„querschnitt“: Treffer nur in Kap. 3.0 (Lesart), Kap. 5 (Latenz) und Kap. 6 (Jahresbeträge ohne Abzinsung) sowie im
Entscheidungslog Nr. 35 des Berichts.

Nachgelesen am 07.10.2026 (Nacharbeit nach der Prüfung von Schritt 4), Bericht 98 unverändert in Rev. 15: Kap. 1,
Absätze „Konto-Einbettung“ und „Warum die eigene Quellenlage davon abweicht“; Kap. 3.0, Tabelle und alle Punkte darunter
(„Lesart des Jahresbetrags“, „Stärkster Treiber“, „Lesart τ = 1“) mit Block `rechenkette_98`; Kap. 3.4 von der Formel
bis zur Letalität, mit dem Absatz „Kumulative Dosis → jährliche Umgebungsdosis: die Gleichgewichtslesart“ und der
„Abschätzung des Transient-Faktors“; Kap. 3.5, Zeichentabelle, Zeilen \(a_{\text{erk}}\), \(T\) und τ; Kap. 4,
Bändertabelle mit den Absätzen darunter und „Unsicherheiten (nach Größe geordnet)“; Kap. 5, Absatz „Latenz: Sprung der
Dosis, Rampe der Wirkung“ mit dem Beispiel Berlin; Kap. 6 ganz mit Modellgrenzen 1–9 und Infokästen 1–3;
Entscheidungslog des Berichts Nr. 1–15 und Nr. 35. Zusätzlich gesucht nach „Discount“, „Transient“, τ (auch als
`\tau`), „Jahres-Attribution“, „Gleichgewichtslesart“, „Untergrenze“ und „überschätz“. „Discount“ trifft nur den
Entscheidungslog Nr. 14 („kein Latenz-Discounting“); die Suche nach „Diskont“ hatte ihn nicht gefunden. „Transient“, τ,
„Jahres-Attribution“ und „Gleichgewichtslesart“ treffen den Statuskopf (Rev. 14), Kap. 1, Kap. 3.0, 3.4 und 3.5, Kap. 4,
Kap. 5 (S155), Kap. 6 (Modellgrenzen 1 und 2, Infokasten 1) und den Entscheidungslog Nr. 14 und 35. „Untergrenze“ trifft
Kap. 1 (Konto-Einbettung), Kap. 3.2, 3.3 und 3.4, Kap. 4, Kap. 5 (S158), Kap. 6 (Szenario-Anwendung, Modellgrenzen 2, 4
und 6, Infokasten 1, Pflicht-Elemente) und den Entscheidungslog Nr. 7, 11 und 12. Schritt 4 hatte τ in Kap. 3.0 und 3.4
gelesen, aber nicht in diese Datei übernommen; das ist mit B4, B5 und dem Absatz „Wann der Schaden eintritt“ nachgeholt.
Für die zweite Nacharbeit am selben Tag zusätzlich gelesen: Kap. 3.2, Punkt „Stationaritätsannahme der Elastizität“;
Kap. 3.4, Punkte \(c_e\) und VOLY; Kap. 8, Quelle [32]; Entscheidungslog des Berichts Nr. 16–37. Gesucht nach
„Erstjahr“, „Folgejahr“ und „[32]“: Die Folgejahre der Behandlung nennt nur Kap. 3.4, Punkt \(c_e\), ohne Zahl; [32]
steht in Kap. 3.2, Kap. 6 und Kap. 8. Diese Datei ändert keinen Bericht.

Für die Schlussprüfung (T-1836, 07.10.2026) zusätzlich gelesen, je am Endstand: Bericht 95, Kap. 4 ganz (vom Begriff
„konservativ“ bis zu den „Unsicherheiten“), Kap. 3.0, Punkt „Ebenen 1, 2 und 6, eine Zelle statt aller Zellen“, und
Entscheidungslog des Berichts Nr. 18 (Harvesting); Bericht 96, Kap. 4 ganz (Kalibrierfaktor, Sanity-Bänder,
Verteilschlüssel-Test, Verteilungsprüfung, Unsicherheiten), Kap. 3.5, Punkte „Proxy-Kennzeichnung“ des Kostensatzes je
Tag und „Präzisierte Untergrenzen-Aussage“, Kap. 6, Szenario-Anwendung und Modellgrenzen 1–7; Bericht 98, Kap. 3.0,
„Lesart des Jahresbetrags“, Kap. 3.4, Absatz zur Gleichgewichtslesart mit der „Abschätzung des Transient-Faktors“,
Kap. 5, Absatz „Latenz: Sprung der Dosis, Rampe der Wirkung“, und Kap. 6, Absatz „Jahresbeträge ohne Abzinsung“; MK 4.0,
S. 14–15. Gesucht in Bericht 95 nach „überschätz“, „einseitig“, „Harvesting“ und „Untergrenze“, in Bericht 96 nach
„überschätz“, „einseitig“ und „Untergrenze“. In Kap. 4 von Bericht 95 trifft „überschätz“ nur den verworfenen
zeitlichen Holdout der Kalibrierung, in Kap. 4 von Bericht 96 kein Treffer; die übrigen Treffer liegen außerhalb von
Kap. 4 und sind unter B1 und B2 eingeordnet.

| Nr | Bericht, Stelle | Stand im Bericht | Festlegung | Art |
|---|---|---|---|---|
| B1 | Bericht 95, Kap. 6, Absätze „Szenario-Anwendung 95-A“ und „Jahresbeträge ohne Abzinsung“ | „M0 weist das Ist-Klima aus“; die Euro-Beträge „gelten für ein Jahr im heutigen Klima“; Szenariofähigkeit folgt mit Stufe M1+. Einen Jahresbetrag für die Jahre nach dem Ist-Klima nennt der Bericht nicht | Barwert über die 41 Jahre 2025–2065 („Bezugsjahr und Zeitraum der Abzinsung“); das Produkt schreibt die Jahresbeträge mit dem Klimasignal fort („Warum der Preiseffekt in die Diskontrate gehört“) | Verlauf fehlt im Bericht. Die Rechenkette rechnet deshalb mit gleichbleibendem Jahresbetrag; bei wärmer werdendem Klima ist ihr Barwert auf der Achse Verlauf eine Untergrenze. Geprüft an den Unsicherheitsachsen von Kap. 4 (07.10.2026): Keine Achse überschätzt einseitig. Das Profil-Band der Süd-Nachschätzung wirkt gegenläufig bei stabiler Bundessumme; Rest-Bias der Wärmeinsel-Feinstruktur, Schätzgüte der Wochenquantile, Skalentransfer Region → Zelle und Restnäherung der Lebenserwartung ab 95 Jahren in der Restlebenszeit der über 85-Jährigen (Band 4,16–4,20 Jahre) stehen ohne einseitige Richtung; Harvesting nennt Kap. 4 ohne Richtung, und der Entscheidungslog des Berichts (Nr. 18) hält die Mortalität über die RKI-Wochenmethodik für robust. Der Zusatz-Anker Berlin 85+ liegt 17 % unter der RKI-Referenz, und „konservativ“ heißt im Bericht „unterschätzend (Untergrenze)“ (Kap. 4, Kopf). Die Einordnung „Untergrenze“ bleibt deshalb. Die Kette selbst liegt 5 % über dem Zelllauf des Produkts (Kap. 3.0, Punkt „Ebenen 1, 2 und 6, eine Zelle statt aller Zellen“); das ist der Abstand zwischen Kette und Produkt, keine Unsicherheitsachse, und der Barwert des Zelllaufs steht im Abschnitt „Rechenkette“ daneben. Zu klären ist, welchen Verlauf das Produkt für #95 in M0 abzinst: Ist-Klima in jedem Jahr oder Szenario 95-A (Kap. 6, Absatz „Szenario-Anwendung 95-A“) |
| B2 | Bericht 96, Kap. 6, Absätze „Jahresbeträge ohne Abzinsung“ und „Szenario-Anwendung 96-A“ | Die Euro-Beträge „gelten für ein Jahr im Ist-Klima zum Preisstand 2024“; „M0 weist das Ist-Klima aus“; die Szenario-Anwendung verschiebt nur das Klimasignal der Saison-Spreizung und braucht Phänologie-Modelle der Stufe M1+. Einen Jahresbetrag für die Jahre nach dem Ist-Klima nennt der Bericht nicht | wie B1: Barwert über die 41 Jahre 2025–2065, Jahresbeträge mit dem Klimasignal fortgeschrieben | Verlauf fehlt im Bericht, wie B1. Die Rechenkette für #96 rechnet mit gleichbleibendem Jahresbetrag; weil der Blühbeginn der Erle nach der Projektion bis 2100 um etwa zwei Wochen weiter vorrückt (Bericht 96, Kap. 6, Absatz „Szenario-Anwendung 96-A“), ist ihr Barwert auf der Achse Verlauf eine Untergrenze. Geprüft an den Unsicherheitsachsen von Kap. 4 (07.10.2026): Keine Achse überschätzt einseitig. Marker-Näherung der Birke (≤ 1,3 Tage, im Band), Phänologie statt Pollenflug, die Bänder der Anteile Betroffener, Übertrag der Attribution von Nordamerika auf Deutschland, Raumtransfer der Kosten und Pollenlast als Ersatzgröße stehen ohne einseitige Richtung; der monetäre Vergleich mit der früheren M0-Herleitung zeigt das Modell „eher zu niedrig“ (Kap. 4, Sanity-Bänder). Überschätzend wirken zwei Kanäle des Kostensatzes je Tag (Umlage der Jahreskosten auf die Saisontage, Durchschnitts- statt Grenzkosten); ihnen stehen zwei unterschätzende gegenüber, und der Bericht führt den Kostensatz als zweiseitiges Band; die Untergrenze trägt die Mengen-Seite (Kap. 3.5, „Präzisierte Untergrenzen-Aussage“; Kap. 6, Modellgrenze 6). Die Einordnung „Untergrenze“ bleibt deshalb. Zu klären ist, welchen Verlauf das Produkt für #96 in M0 abzinst |
| B3 | Bericht 96, Kap. 6, Absatz „Jahresbeträge ohne Abzinsung“, letzter Satz | „Die Diskontrate für mehrjährige Rechnungen legt T-1116 fest.“ | Die Regel steht in `docs/methodik/querschnitt_diskontrate.md`, Abschnitt „Festlegung“ (Regel D) | Verweis auf ein Ticket des Firmen-Repos statt auf die Festlegung; ein Leser des Berichts kann ihn nicht auflösen. Bericht 95 hat den Satz ohne diesen Verweis (Kap. 6, Absatz „Jahresbeträge ohne Abzinsung“) |
| B4 | Bericht 98, Kap. 6, Absätze „Szenario-Anwendung 98-A“ und „Jahresbeträge ohne Abzinsung“ | „M0 weist das Ist-Klima aus“ (Normalperiodenvergleich); konstant gehalten werden unter anderem Inzidenzraten und Kostensätze; „Inzidenz-Baseline stationär (real steigend — Untergrenze)“. Einen Jahresbetrag für die Jahre nach dem Ist-Klima nennt der Bericht nicht | wie B1: Barwert über die 41 Jahre 2025–2065, Jahresbeträge mit dem Klimasignal fortgeschrieben | Verlauf fehlt im Bericht, wie B1 und B2. Die Rechenkette für #98 rechnet mit gleichbleibendem Jahresbetrag. Weil der Bericht für Szenarien eine weiter steigende UV-B-Belastung nennt und die Inzidenz real steigt, liegt ihr Barwert auf der Achse Verlauf zu niedrig. Eine Untergrenze ist er trotzdem nicht: Auf der Achse Latenz läge eine Jahres-Attribution um bis zu 80 % niedriger (Transient-Faktor τ = 0,20), der Ausweis also bis zum Fünffachen über ihr (Befund B5). Nach dem, was der Bericht beziffert, überwiegt diese Richtung: τ ist seine größte Achse (Kap. 4). Den Anstieg der UV-B-Belastung nennt er nur als Plausibilisierungsrahmen (UV-B-Projektion +1,3 % je Dekade für 2050–2100), die steigende Inzidenz ohne Zahl; wie stark der Verlauf auf den Jahresbetrag wirkt, beziffert er nicht (Kap. 6, Absatz „Szenario-Anwendung 98-A“; Kap. 8, Quelle [32]). Zu klären ist, welchen Verlauf das Produkt für #98 in M0 abzinst |
| B5 | Bericht 98, Kap. 3.0, „Lesart des Jahresbetrags“ und Punkt „Lesart τ = 1“; Kap. 3.4, „Abschätzung des Transient-Faktors“; Kap. 3.5, Zeichentabelle, Zeile τ; Kap. 4, Bändertabelle; Kap. 5, Absatz „Latenz: Sprung der Dosis, Rampe der Wirkung“; Kap. 6, Absatz „Jahresbeträge ohne Abzinsung“ und Modellgrenze 1; Entscheidungslog des Berichts Nr. 14 und Nr. 35 | Der Jahresbetrag beziffert „die Fälle eines Jahres unter der heutigen, eingelaufenen Dosislage — die Latenz von Jahrzehnten steckt schon in den Inzidenzraten der Ebene 2 […], und deshalb wird nicht weiter abgezinst“ (Kap. 3.0); er ist das „eingelaufene Risiko“, „keine Vorhersage der Fälle *dieses* Jahres“ (Modellgrenze 1). Entscheidungslog Nr. 14: „Gleichgewichtslesart“, „kein Latenz-Discounting“, „Ergebnis wird gegenüber einer Jahres-Attribution überschätzt — größte Achse der §4-Bändertabelle (67–339 Mio. €), einseitig“. Den Abstand zur Jahres-Attribution beziffert der Bericht mit dem Transient-Faktor τ = 0,20–0,48 (Kap. 3.4), im Ausweis τ = 1; Berlin läge mit τ um 52–80 % niedriger (Kap. 3.0). Bei der Maßnahme S155 bildet der Bericht die Verzögerung als Rampe im Jahresbetrag ab, „Abgezinst wird nicht“, und setzt τ nicht zusätzlich an, „weil dieselbe Einlaufzeit zweimal zählte“ (Nr. 35) | Regel D zinst jeden Jahresbetrag mit (Jahr − 2025) ab. Stand bis Schritt 4: **Ob „Jahr“ das Jahr des Schadenseintritts oder das Jahr der Belastung ist, legt die Festlegung nicht fest.** Einen verzögerten Schadenseintritt erwähnt sie nicht. Seit der Schlussprüfung (Entscheidungslog Nr. 23): „Jahr“ ist das Jahr des Schadenseintritts; die Latenz geht nur über den Betrag ein (Festlegung, „Bezugsjahr und Zeitraum der Abzinsung“) | Lücke in der Festlegung, keine Abweichung des Berichts; **geschlossen am 07.10.2026** (Nr. 23). Die Rechenkette für #98 rechnet nach der Gleichgewichtslesart des Berichts (voller Betrag im Jahr des Betrags, τ = 1) und ändert Regel D nicht (Entscheidungslog Nr. 20 und 22). Bis zur Entscheidung standen für die Latenz zwei Wege offen, die einander ausschließen: τ auf den Betrag im Jahr des Schadens (Barwert bis −80 %: 93,9–225,3 Mio. € zur RZPR 0 %, 77,6–186,2 Mio. € zur RZPR 1 %, bei τ in allen Jahren gleich) oder eine Verschiebung nach dem Jahr der Belastung (je zehn Jahre −1,0 % zur RZPR 0 %, −10 % zur RZPR 1 %). **Entschieden: Regel D zinst nach dem Jahr des Schadenseintritts ab** (Nr. 23, Quelle MK 4.0, S. 14). Damit sind Basiswert und Rampe von S155 so gebucht, wie Regel D es verlangt, und offen bleibt allein τ, eine Frage an den Bericht, die er mit τ = 1 im Ausweis entschieden hat. Die Verschiebung nach dem Jahr der Belastung entfällt; an den Barwerten der Kette ändert sich nichts. Unter einer Jahres-Attribution wächst τ über 2025–2065, ein in allen Jahren gleicher τ ist der untere Rand. Was Bericht 98 daraus braucht, steht in B6 |
| B6 | Bericht 98, Kap. 3.0, „Lesart des Jahresbetrags“; Kap. 3.4, „Abschätzung des Transient-Faktors“; Kap. 4, Bändertabelle, Zeile „Transient-Faktor τ“; Kap. 5, Absatz „Latenz: Sprung der Dosis, Rampe der Wirkung“, letzter Satz; Kap. 6, Absatz „Jahresbeträge ohne Abzinsung“ | Kap. 3.0: „deshalb wird nicht weiter abgezinst“. Kap. 5: „Abgezinst wird nicht (Satz unter §3.0).“ Kap. 3.4: τ = 0,20–0,48 für die „heute erkrankenden Kohorten“, ohne Aussage, wie sich τ über die Jahre entwickelt. Kap. 6: „Alle Beträge dieses Berichts sind Jahresbeträge ohne Abzinsung“, die „Fälle eines Jahres unter der heutigen, eingelaufenen Dosislage“, ohne Verweis auf die Regel für mehrjährige Rechnungen | Regel D zinst in einer mehrjährigen Rechnung jeden Jahresbetrag nach dem Jahr des Schadenseintritts ab; die Latenz geht nur über den Betrag ein; unter einer Jahres-Attribution wächst τ über 2025–2065 und fällt nie, solange die Dosis nicht sinkt (Festlegung, „Bezugsjahr und Zeitraum der Abzinsung“, Punkt „Jahr des Schadenseintritts“; Entscheidungslog Nr. 23) | Klarstellung im Bericht nötig, keine Abweichung im Betrag. Der Bericht braucht drei Sätze: (1) In Kap. 3.0 und Kap. 5 heißt „nicht abgezinst“: kein Latenzabschlag im Jahresbetrag, wie Entscheidungslog Nr. 14 des Berichts („kein Latenz-Discounting“) eindeutiger sagt. Eine mehrjährige Rechnung zinst jeden Jahresbetrag, auch die Rampe von S155, nach Regel D im Jahr des Schadenseintritts ab. (2) Kap. 6, Absatz „Jahresbeträge ohne Abzinsung“, verweist auf `docs/methodik/querschnitt_diskontrate.md`, Regel D. (3) Kap. 3.4 und Kap. 4 sagen, dass die Spanne 0,20–0,48 für die heute Erkrankenden gilt, dass τ unter einer Jahres-Attribution über die Jahre wächst und dass ein in allen Jahren gleicher τ in einer mehrjährigen Rechnung nur der untere Rand ist. Entscheidungslog Nr. 14 und Nr. 35 des Berichts bleiben gültig. Diese Datei ändert den Bericht nicht |

**Ohne Abweichung:** Jahresbetrag 362,9 Mio. € je Jahr (Preisstand 2024) in Kap. 3.0, Ebene 10; Anteil Mortalität
361,8 Mio. € und Morbidität 1,09 Mio. € (Ebenen 8 und 9) wie unter „Geltung für die Schadensarten von M0“; 225 der
277,4 Todesfälle ab 75 Jahren (Ebene 6: 71,4 + 153,6) wie unter A9; Zelllauf mit Gemeindeschlüssel 345,11 Mio. €
(Kap. 3.0, Punkt „Ebenen 1, 2 und 6, eine Zelle statt aller Zellen“) wie im Abschnitt „Rechenkette“; VOLY 160.800 € mit
dem Faktor „Einkommensentwicklung ^0,85 ×1,1719“ in Kap. 3.5. Den Satz zu Jahresbeträgen ohne Abzinsung hat Bericht 95
bereits (Kap. 6, Absatz „Jahresbeträge ohne Abzinsung“).

**Ohne Abweichung für #96:** Jahresbetrag 2,53 Mio. € je Jahr (Preisstand 2024) in Kap. 3.0, Ebene 10, und Zelllauf
2,47 Mio. € (Kap. 3.0, Absatz „Kommune statt Zellen“), wie im Abschnitt „Rechenkette“; nur Behandlungskosten ohne
Mortalitätskomponente (Kap. 1, Konto-Einbettung; Register 96-K1-01 in Kap. 2), wie unter „Geltung für die Schadensarten
von M0“; alle Kostensätze in festen Preisen, mit dem Verbraucherpreisindex auf den Preisstand 2024 gebracht (Kap. 3,
„Gemeinsamer Preisstand aller Kostensätze“; Kap. 3.5), wie unter „Nur feste Preise werden abgezinst“; in der
Szenario-Anwendung bleiben die Kostensätze konstant (Kap. 6, Absatz „Szenario-Anwendung 96-A“), wie unter „Warum der
Preiseffekt in die Diskontrate gehört“. Den Satz zu Jahresbeträgen ohne Abzinsung hat Bericht 96 (Kap. 6, Absatz
„Jahresbeträge ohne Abzinsung“).

**Ohne Abweichung für #98:** Jahresbetrag 11,68 Mio. € je Jahr (Preisstand 2024) in Kap. 3.0, Ebene 10, Zeile 310, wie
im Abschnitt „Rechenkette“; Mortalität 7,84 Mio. € als YLL × VOLY und Behandlung 3,83 Mio. € (Ebene 9), wie unter
„Geltung für die Schadensarten von M0“; VOLY 160.800 € (Preisstand 2024) aus der Kette in Bericht 95, Kap. 3.5 (Bericht
98, Kap. 3.4), also derselbe Wert, den die Festlegung mit der Elastizität 0,85 fortschreibt; Kostensätze in festen
Preisen, mit dem Verbraucherpreisindex von 2015 auf 2024 gebracht (Kap. 3, Kopf; Kap. 3.4, \(c_e\)), wie unter „Nur feste
Preise werden abgezinst“; in der Szenario-Anwendung bleiben die Kostensätze konstant (Kap. 6, Absatz
„Szenario-Anwendung 98-A“), wie unter „Warum der Preiseffekt in die Diskontrate gehört“; die Sterbefälle sind alt
(medianes Sterbealter 76–88 Jahre, Kap. 3.4, Konsistenz-Check VSL ÷ VOLY), was die Lesart unter A9 („Wessen
Einkommen?“) auch für #98 trägt. Den Satz zu Jahresbeträgen ohne Abzinsung hat Bericht 98 (Kap. 6, Absatz
„Jahresbeträge ohne Abzinsung“), ohne Verweis auf ein Ticket.

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
- **[Bericht 95]** `docs/methodik/95_hitzebelastung.md`, Kap. 3.0 (Ebenen 6–10; Absatz „Stärkster Treiber“, gelesen am
  07.10.2026; Punkt „Ebenen 1, 2 und 6, eine Zelle statt aller Zellen“ mit dem Zelllauf), Kap. 3.5 (VOLY-Kette),
  Kap. 4 (ganz, mit „Unsicherheiten“; gelesen am 07.10.2026), Kap. 6 (Absätze „Szenario-Anwendung 95-A“ und
  „Jahresbeträge ohne Abzinsung“), Entscheidungslog Nr. 18. Gelesen am 06.10.2026, nachgelesen am 07.10.2026.
- **[Bericht 96]** `docs/methodik/96_aeroallergene.md`, Rev. 4, abgenommen am 30.09.2026: Statuskopf (Runden 30–32,
  Befund 258); Kap. 1, Konto-Einbettung; Evidenz-Register 96-K1-01; Kap. 3.0 (Ebene 10; Absätze „Kommune statt Zellen“
  und „Stärkster Treiber“); Kap. 3.5 (mit „Proxy-Kennzeichnung“ des Kostensatzes je Tag und „Präzisierte
  Untergrenzen-Aussage“); Kap. 4 (ganz, gelesen am 07.10.2026); Kap. 6 (Absätze „Jahresbeträge ohne Abzinsung“ und
  „Szenario-Anwendung 96-A“, Modellgrenzen 1–7). Gelesen am 06.10.2026, nachgelesen am 07.10.2026.
- **[Bericht 98]** `docs/methodik/98_uv_schaedigungen.md`, Rev. 15 vom 05.10.2026: Kap. 1 („Konto-Einbettung“), Kap. 3.0
  (Ebenen 9 und 10, Ebene 10 in Zeile 310, gemessen am 06.10.2026 und am 07.10.2026; „Lesart des Jahresbetrags“; Punkte
  „Stärkster Treiber“, „Lesart τ = 1“ und „Bevölkerung im Produkt“), Kap. 3.2 (Punkt „Stationaritätsannahme der
  Elastizität“), Kap. 3.4 (Gleichgewichtslesart und „Abschätzung des Transient-Faktors“, Monetarisierung, Punkt \(c_e\)
  mit der „Untergrenzen-Zusage“, VOLY, Konsistenz-Check VSL ÷ VOLY), Kap. 3.5 (Zeichentabelle, Zeile τ), Kap. 4
  (Bändertabelle, Zeile „Transient-Faktor τ“; „Unsicherheiten (nach Größe geordnet)“), Kap. 5 (Absatz „Latenz: Sprung
  der Dosis, Rampe der Wirkung“), Kap. 6 (Absätze „Szenario-Anwendung 98-A“ und „Jahresbeträge ohne Abzinsung“,
  Modellgrenzen 1, 2 und 6, Infokasten 1), Kap. 8 (Quelle [32]), Entscheidungslog Nr. 7, Nr. 14 und Nr. 35. Gelesen am
  06.10.2026, nachgelesen am 07.10.2026.
- **[Produkt]** `backend/app/data/diskontierung.py`; `backend/app/services/cost_projection_service.py`
  (`_diskontraten()`, `project_costs()`, `_discounted()`); `backend/app/services/climate/dwd_data.py`
  (`get_climate_projection()`); `docs/KONFORMITAET_CHECKLISTE.md`, Zeile 22 und „Gegenprobe Zeile 22“.

Von MK 4.0 zitiert, aber nicht gelesen: Ramsey (1928), Drupp et al. (2024), Baumgärtner et al. (2015) und Anthoff (2025).
Die Festlegung stützt sich auf keine Zahl aus diesen Werken.
