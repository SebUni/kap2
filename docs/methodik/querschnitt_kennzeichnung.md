# Querschnitt: Kennzeichnung berechneter Parameter

Querschnittsdatei der Methodik, gültig für alle 102 Klimawirkungen der KWRA 2021. Angewendet wird sie heute nur auf
#95, #96 und #98 (A-0048; Vorhaben T-1808-cmo, Eltern T-1795-ceo). Schritt 1 (Ticket T-1812-methodik_manager) legt
die Regel fest und rechnet sie an den 11 Blöcken nach, die heute `kennzeichnung: berechnet` tragen. Schritt 2 schreibt
die Übernahmeliste an den CTO und die Befunde an die Berichte. Anlass ist Befund 224 im Ledger #95: Die
Parameterliste zeigt heat.c_kal als „berechnet aus anderen Parametern“, und das Produkt zählt das wie „belegt“,
obwohl in c_kal zwei Abschätzungen von KAP3 stecken (Bericht 95, Kap. 7, Absatz „Kennzeichnung `berechnet`“).

Begriffe: **Block** = Parameter-Block in Kapitel 7 eines Berichts (Aufgabe §4, „Parameter-Block-Format“).
**Eingang** = ein Eintrag im Feld `abgeleitet_aus` eines Blocks. **Parameter-ID** = Eingang, der selbst ein Block
desselben Berichts ist. **Quellenschlüssel** = Eingang ohne eigenen Block, etwa `zfkd_kid2025`; er steht im Feld
`quelle:` eines Blocks. **Setzung** = eine Zahl oder Wahl von KAP3, die so in keiner Quelle steht. Woran Regel K eine
Setzung erkennt, legt Frage 1 mit den Merkmalen S1 und S2 fest.

## Festlegung

**Regel K (Kennzeichnung eines Parameters).** Für jeden Block beantwortet die Parameterliste drei Fragen in dieser
Reihenfolge. Die erste Antwort „ja“ entscheidet.

1. **Steckt im Wert des Blocks selbst eine Setzung von KAP3?** Ja: Kennzeichnung `abschaetzung_kap3`, Anzeigetext
   „Abschätzung von KAP3“. Das gilt auch, wenn der Block zusätzlich andere Blöcke nutzt, und es genügt, dass ein Teil
   des Werts die Setzung trägt, etwa ein Band oder eine Region. Eine Setzung liegt vor, wenn eines der beiden Merkmale
   zutrifft:
   - **S1 Zahl von KAP3:** KAP3 setzt oder schätzt eine Zahl, die so in keiner Quelle steht, etwa die
     Süd-Nachschätzung s_Süd = 1,65 in heat.beta_85plus_region (Nord und Mitte sind abgelesen). Erkennbar daran, dass
     der Bericht den Block als `abschaetzung_kap3` führt.
   - **S2 Näherung:** Der Wert stammt aus Zahlen einer Quelle, ein Teil davon steht aber für eine Größe, für die die
     Quelle keine Zahl ausweist: für eine andere Größe (Proxy: heat.c_fall, uv.lambda), für eine Gruppe jenseits der
     Quelle (Extrapolation: pollen.p_ar, die Altersgruppen ab 80 Jahren mit dem Wert der 70- bis 79-Jährigen), als
     Punkt statt Bandmittel (Stützstellen in heat.l_restlebenserwartung, medianes Sterbealter in uv.l_rest) oder in
     vereinfachter Form (lineare Näherung in heat.f_alter). Erkennbar ist S2 an der Aussage, nicht an einem bestimmten
     Wort: Der Block sagt in einem Feld oder Kommentar, dass ein Teil seines Werts so entsteht. In M0 sagen die Blöcke
     das mit „Proxy“, „Approximation“, „Näherung“, „Stützstelle“ und „extrapoliert“.

   **Eine benannte Näherung ist immer eine Setzung**, gleich ob der Bericht sie als Modellgrenze, als gekennzeichnete
   Näherung oder als Abschätzung führt. Keine Setzung ist es, wenn der Wert seine Zielgröße selbst misst, auch wenn
   KAP3 ihn aus Zahlen der Quelle rechnet oder zwischen Quellenwerten wählt. In M0 sehen drei Fälle einer Näherung
   ähnlich und sind keine; der Beispiel-Block prüft an allen 66 Blöcken, dass jeder solche Block hier steht:
   - **Ablesewert:** Ein aus einer Abbildung der Quelle abgelesener Wert misst die Größe, die die Quelle zeigt; die
     Ableseungenauigkeit ist Unsicherheit (heat.t0_region, uv.i_raten_roh, uv.i_mm, uv.i_c44; uv.c_kal nennt die
     Ablesewerte seines Eingangs).
   - **Gemessener Versatz im Band:** pollen.delta_s_region nimmt für die Birke die Blattentfaltung statt der Blüte,
     weil die Blüte 1960–1990 eine Meldelücke hat. Den Versatz misst #96 §3.1 in den Jahren mit beiden Meldungen
     (+3,29 Tage); was davon im Wert bleibt, bis zu 1,3 Tage, führt der Block im Band. Die Quelle selbst sagt also,
     wie weit der Wert von der Zielgröße abweicht.
   - **Annahme über die Geltung eines Werts:** uv.k_uv nennt die Elastizität „zeitinvariant angenommen“ und ihre
     räumliche Streuung Modellgrenze 9. Der Block führt keinen eigenen Wert für eine andere Zeit oder einen Ort; sein
     Wert 0,7119 ist aus dem Stationsquotienten der Quelle und der Rasterauswertung gerechnet. Ob er zu jeder Zeit und
     an jedem Ort gilt, ist eine Annahme des Modells. Anders pollen.p_ar: Dort steht im Wert ein eigener Eintrag für das
     Band ab 85 Jahren, für das die Quelle keine Zahl hat.
2. **Nennt `abgeleitet_aus` keine Parameter-ID?** Ja: Kennzeichnung `quelle`, Anzeigetext „Quelle“. Das umfasst den
   Wert, der so in der Quelle steht, und die Rechnung aus Zahlen einer Quelle, die ihre Zielgröße selbst misst
   (Quotient, Summe, ausgezähltes Quantil, eigene Auswertung amtlicher Rohdaten).
3. **Sonst** (mindestens eine Parameter-ID): Kennzeichnung `berechnet`. Der Anzeigetext richtet sich nach dem
   schwächsten Eingang über alle Rechenstufen:
   - trägt kein Eingang, auch nicht über einen berechneten Eingang hinweg, eine Abschätzung von KAP3:
     „berechnet aus Quellen“;
   - trägt mindestens ein Eingang eine Abschätzung von KAP3, direkt oder weitergereicht: „berechnet, enthält
     Abschätzung von KAP3“.

Die Parameterliste zeigt neben einem berechneten Parameter seine Eingänge mit deren Anzeigetext, damit der Leser
die Herleitung bis zur Quelle oder zur Abschätzung verfolgen kann. **Gezählt** wird so: „Quelle“ und „berechnet aus
Quellen“ zählen als belegt, „Abschätzung von KAP3“ und „berechnet, enthält Abschätzung von KAP3“ als abgeschätzt.
Die drei Werte aus Aufgabe §4 und das Feld `abgeleitet_aus` bleiben, wie sie sind; die Verbindung steht nur im
Anzeigetext. Das Feld `rolle` (etwa `kalibrierung`) ändert an der Kennzeichnung nichts.

**Prüfstein (P1).** Die Parameterliste zeigt eine Setzung von KAP3 nie als Quelle, auch dann nicht, wenn sie über
eine Rechnung weitergereicht wird. Regel K hält das in zwei Schritten ein: Frage 1 hält jede Setzung im Block selbst,
auch eine benannte Näherung, aus `quelle` und aus „berechnet aus Quellen“ heraus. Frage 3 reicht jede Setzung eines
Eingangs über alle Stufen bis zum Anzeigetext durch.

### (a) Grenze zwischen `quelle` und `berechnet`

`berechnet` ist ein Block genau dann, wenn er keine Setzung enthält (Frage 1) und `abgeleitet_aus` mindestens eine
Parameter-ID nennt. Eine Rechnung, die nur Zahlen einer Quelle verarbeitet, ist nie `berechnet`, auch wenn KAP3 sie
selbst ausführt: Sie ist `quelle`, wenn sie ihre Zielgröße selbst misst, und `abschaetzung_kap3`, wenn sie eine
Näherung nach S2 trägt. Der Wortlaut von Aufgabe §4 trägt die Grenze zu `berechnet`: „`berechnet`: der Wert folgt
rechnerisch aus anderen Parametern“, und `abgeleitet_aus` nennt „die Parameter-IDs, aus denen der Wert entsteht“.
#95 Log 40 zieht beide Grenzen so: „`berechnet` nur, wo der Wert aus anderen Blöcken folgt“, dazu der Prüfstein für
Setzungen, den Frage 1 übernimmt. #96 Log 25 folgt der Grenze zu `berechnet` (ΔS als ausgewertete amtliche
Messreihe = `quelle`), nicht aber dem Prüfstein: Es führt pollen.p_ar als `quelle`, weil vier von fünf Bändern einen
Quellwert tragen und die Extrapolation am Band gekennzeichnet ist. #98 Log 36 zieht die Grenze zu `berechnet` anders
(„schwächste Herkunft im Block“, eigene Auswertung = `berechnet`). Nach Regel K gilt keine der beiden Abweichungen
mehr, und alle drei Berichte werden nach derselben Regel gelesen.

- **uv.ssd_delta_region** (eigene Auswertung DWD-Raster × VG250 × Zensus 2022): einziger Eingang ist der
  Quellenschlüssel `dwd_cdc_ssd_raster_x_vg250_x_zensus2022`, keine Parameter-ID. Der Block benennt keine Näherung;
  der Wert misst die Änderung der Sonnenscheindauer selbst. Nach Regel K `quelle`, Anzeigetext „Quelle“ (#98 Log 36:
  `berechnet`).
- **uv.lambda** = Sterbefälle ÷ Neuerkrankungen im Fenster 2021–2023 aus ZfKD [27], beim Melanom 3.081,0 ÷ 26.870 =
  0,11466: einziger Eingang ist `zfkd_kid2025`, keine Parameter-ID, also nicht `berechnet`. Der Block benennt aber
  eine „Perioden-Approximation“: Der Quotient eines Zeitfensters steht für den Anteil der Erkrankten, die an der
  Krankheit sterben, und diesen Anteil weist die Quelle nicht aus (#98 §3.4: „bei steigender Inzidenz keine
  Kohorten-Letalität; Richtung: Überschätzung des Mortalitätsanteils“). Das ist S2. Nach Regel K `abschaetzung_kap3`,
  Anzeigetext „Abschätzung von KAP3“ (#98 Log 36: `berechnet`). Anders heat.m_basissterberate in #95: Sterbefälle
  2023 ÷ Bevölkerung ist genau die Sterberate, die das Modell braucht, also `quelle`.
- **uv.l_rest** (Restlebenserwartung am medianen Sterbealter): ebenfalls keine Parameter-ID. Der Block benennt eine
  „Median-Approximation“, also einen Punkt statt des Mittels über alle Sterbealter (S2). Nach Regel K
  `abschaetzung_kap3`, wie die Stützstellen e(60), e(70) und e(80) in heat.l_restlebenserwartung, die #95 nach Log 40
  als `abschaetzung_kap3` führt.
- **Folgen außerhalb der 11 Blöcke:** heat.beta_iso steht in #95 als `quelle`, nennt in `abgeleitet_aus` aber den
  Block heat.qbar_1p. Nach Regel K ist er `berechnet`, Anzeigetext „berechnet aus Quellen“; er zählt weiter als belegt.
  pollen.p_ar steht in #96 als `quelle`, führt für die Bänder 75–84 und ab 85 Jahren aber den DEGS1-Wert der 70- bis
  79-Jährigen (#96 §3.2: „Extrapolation über das DEGS1-Ende 79 hinaus“). Nach Regel K (Frage 1, S2) ist er
  `abschaetzung_kap3`, Anzeigetext „Abschätzung von KAP3“; er zählt nicht mehr als belegt.

### (b) Eingang ohne eigenen Block (Quellenschlüssel in `abgeleitet_aus`)

Ein Quellenschlüssel zählt als Eingang mit der Kennzeichnung `quelle`. Allein macht er einen Block nicht zu
`berechnet`, denn dafür verlangt §4 eine Parameter-ID. Steht er neben einer Parameter-ID, zählt er bei Frage 3 als
`quelle`. Bedingung: Der Schlüssel steht im Feld `quelle:` eines Blocks desselben Berichts, und hinter ihm stehen nur
Zahlen der Quelle. Eine Zahl, die KAP3 setzt, braucht einen eigenen Block, weil P1 jeden Parameter in der Liste
verlangt; hinter einem Schlüssel darf sie nicht stehen. Ob ein Schlüssel später einen eigenen Block bekommt (#98,
Befund 463), ändert das Ergebnis nicht, solange dieser Block eine reine Auswertung der Quelle ist.

**`abgeleitet_aus` bei einem Block, der nach Regel K nicht `berechnet` ist.** Aufgabe §4 verlangt dort ein leeres
Feld („sonst leer“). Sechs Blöcke führen es dennoch: uv.ssd_delta_region (`quelle`), uv.lambda und uv.l_rest
(`abschaetzung_kap3`) mit einem Quellenschlüssel, heat.g_s157, heat.delta_vg_morb und heat.delta_kuehlzentren
(`abschaetzung_kap3`) mit einer Parameter-ID. Regel K wertet das Feld dort nicht aus, weil Frage 1 oder 2 entschieden
hat, bevor Frage 3 es liest. Es gilt als Verweis auf die Herleitung und als benannte Abweichung von §4. Für die drei
Blöcke aus #98 hat #98 Log 36 diese Abweichung begründet (Teil 3 der Gegenprüfung, Befund 460): Der Quellenschlüssel
bleibt, bis die Eingänge eigene Blöcke haben (Befund 463). Diese Begründung setzt voraus, dass die drei Blöcke
`berechnet` sind; nach Regel K sind sie es nicht. Ob das Feld bei den sechs Blöcken geleert oder die Abweichung neu
begründet wird, ist ein Befund an die Berichte (Schritt 2). Bis dahin gilt die Lesart dieses Absatzes.

### (c) Kalibrierskalar, gefittet gegen eine amtliche Reihe

Ein Kalibrierskalar ist ein berechneter Block wie jeder andere. Seine Eingänge sind die Blöcke des Modells, das er an
die Reihe anpasst, und die Reihe selbst. Die Reihe zählt als `quelle`, gleich ob sie in `abgeleitet_aus` oder nur im
Feld `quelle:` steht; sie kann den schwächsten Eingang nicht anheben. Grund: Der Fit gleicht genau das aus, was die
Setzungen im Modell verschieben. Ändert sich eine Setzung, ändert sich der Skalar. Belegt ist nach dem Fit die Summe
aus Modell und Skalar, die an die Reihe angepasst ist, nicht der Skalar.

- **heat.c_kal** = 0,581, Fit gegen die RKI-Reihe 2012–2024 (`rki_eb19_2025`). Eingänge: heat.t0_region,
  heat.m_basissterberate und heat.q_wochenquantile (`quelle`), heat.beta_85plus_region (Süd-Nachschätzung) und
  heat.f_alter (lineare Näherung), beide `abschaetzung_kap3`. Nach Regel K `berechnet`, Anzeigetext „berechnet,
  enthält Abschätzung von KAP3“. Dass die Setzung im Wert steckt, zeigt das Band des Blocks: Mit s_Süd = 1,85 statt
  1,65 ergibt der Fit 0,559, ohne die Region Süd 0,661.
- **uv.c_kal** = ZfKD-Anker ÷ Modellsumme der Rohraten. Eingänge: uv.i_raten_roh (`quelle`) und `zfkd_kid2025`
  (Quellenschlüssel). Nach Regel K `berechnet`, Anzeigetext „berechnet aus Quellen“.

Regel K wertet `abgeleitet_aus` so aus, wie der Bericht es führt. Ob die Liste vollständig ist, prüft der Bericht
(Aufgabe §4: Pflichtfeld bei `berechnet`).

### (d) Zählung als belegt in Gewissheitsstufe und Unsicherheits-Zusammenschau

**Ja, Regel K ändert, was als belegt zählt.** Ein berechneter Block zählt nur dann als belegt, wenn kein Eingang über
alle Stufen eine Abschätzung von KAP3 trägt, und ein Block mit benannter Näherung zählt nie als belegt. Heute zählt das
Produkt jeden berechneten Parameter als belegt: `BELEGTE_KLASSEN = frozenset({"belegt", "berechnet"})`
(`backend/app/services/parameter_registry.py`, Z. 102), genutzt in `gewissheit.py` (Z. 86) und
`unsicherheits_zusammenschau.py` (Z. 99), festgeschrieben in `backend/tests/test_evidence_class_berechnet.py`, Teil (c).
**Begründung:** Die Zählung „x von y Parametern mit Quelle“ ist dieselbe Aussage wie die Parameterliste, nur
verdichtet. Zählte heat.c_kal dort als belegt, zeigte die Zählung eine Setzung als Quelle, gegen den Prüfstein. Wie
viel sich verschiebt, zeigt die Zählung über die Blöcke in Kapitel 7 (nachgerechnet im Beispiel-Block):

| Bericht | Blöcke | belegt bisher | belegt nach Regel K |
|---|---|---|---|
| 95 | 30 | 13 | 12 |
| 96 | 14 | 5 | 2 |
| 98 | 22 | 11 | 9 |

Bei #95 fällt heat.c_kal heraus, bei #96 fallen pollen.d_saison, pollen.c_tag und pollen.p_ar heraus, bei #98
uv.lambda und uv.l_rest. pollen.p_ar, uv.lambda und uv.l_rest entscheidet Frage 1 (benannte Näherung).
uv.ssd_delta_region wechselt von `berechnet` nach `quelle` und bleibt belegt.
**Die Gewissheit nach Regel G ändert sich nicht:** Sie übernimmt die Stufe der KWRA (TB6 Tabelle 1) und nimmt die
Quellenlage nicht auf ([querschnitt_gewissheit.md](querschnitt_gewissheit.md), „Festlegung“). Solange der Code die
Stufe noch aus dem Anteil der belegten Parameter bildet (`gewissheit.py`, `gewissheitsstufe`), verschiebt Regel K auch
diese Stufe, und die Unsicherheits-Zusammenschau führt die sechs Werte als nicht belegt. Wie der Code das umsetzt,
legt Schritt 2 fest.

### Begründung und Fundstelle

- **P1** (`CLAUDE.md` des Produkts, Abschnitt „Vorgaben des Aufsichtsrats für das Produkt“, Spiegelstrich P1): „Je
  Parameter steht dort entweder die Quelle oder der Vermerk, dass es eine begründete Abschätzung von KAP3 ist, samt
  Herleitung, wie sie zustande kommt.“ P1 kennt zwei Aussagen, Quelle oder Abschätzung, und verlangt die Herleitung.
  Regel K gibt jedem berechneten Parameter eine der beiden Aussagen („aus Quellen“ oder „enthält Abschätzung von
  KAP3“) und behält mit „berechnet“ die Herleitung. „Quelle“ sagt dem Leser, dass die Quelle den Wert für die Größe
  im Modell nennt; bei einer Näherung nennt sie ihn nicht, deshalb Frage 1.
- **Aufgabe §4** (`docs/AUFGABE_METHODIK_SCHADENSRECHNUNG.md`, „Felder `kennzeichnung`, `abgeleitet_aus`, `rolle`“):
  „`kennzeichnung` (Pflicht) hat genau drei Werte: `quelle | abschaetzung_kap3 | berechnet`. `quelle`: der Wert steht
  in einer benannten Quelle. `abschaetzung_kap3`: begründete Abschätzung von KAP3 mit Herleitung (P1). `berechnet`:
  der Wert folgt rechnerisch aus anderen Parametern.“ und „`abgeleitet_aus` nennt bei `berechnet` die Parameter-IDs,
  aus denen der Wert entsteht; sonst leer.“ Regel K behält die drei Werte und zieht die Grenze zu `berechnet` dort, wo
  §4 sie zieht: an den anderen Parametern. Füllt ein Bericht `abgeleitet_aus` bei einem Block, der nach Regel K nicht
  `berechnet` ist, weicht er von §4 ab; Regel K liest das Feld dort nach Festlegung (b).
- **#95 Log 40** (Prüfstein für Setzungen, Grundlage von Frage 1): „Misst der Wert die Zielgröße selbst, ist die bloße
  Wahl zwischen Quellenwerten keine Setzung (…) — steht er für eine andere Größe (Proxy) oder nähert er ein Bandmittel
  durch einen Punkt an, ist es eine“. Regel K schreibt diesen Prüfstein als S2 für alle Berichte fest, also auch für
  #96 und #98.

**Was Regel K dem Bericht überlässt.** Regel K entscheidet jede der drei Fragen selbst. Aus dem Bericht übernimmt sie
nur Tatsachen: welche Zahl KAP3 setzt (S1, `abschaetzung_kap3`), welche Näherung der Block benennt (S2) und welche
Eingänge `abgeleitet_aus` nennt. Ob ein Bericht jede Setzung und jede Näherung benennt, prüft seine Gegenprüfung
(Aufgabe §3.9, §5). Einen Block, den der Bericht als `abschaetzung_kap3` führt, stuft Regel K nie herauf.

## Anwendung auf M0: die 11 berechneten Blöcke

Alle 11 Blöcke tragen im Bericht heute `kennzeichnung: berechnet`. Eingänge in der Reihenfolge von `abgeleitet_aus`,
ihre Kennzeichnung nach Regel K in derselben Reihenfolge; „kein Block“ heißt Quellenschlüssel (Festlegung, b).

| Bericht | Block-ID | Eingänge | deren Kennzeichnung | Kennzeichnung nach der Regel | Anzeigetext |
|---|---|---|---|---|---|
| 95 | `heat.c_kal` | `heat.t0_region` · `heat.beta_85plus_region` · `heat.f_alter` · `heat.m_basissterberate` · `heat.q_wochenquantile` | `quelle` · `abschaetzung_kap3` · `abschaetzung_kap3` · `quelle` · `quelle` | `berechnet` | „berechnet, enthält Abschätzung von KAP3“ |
| 95 | `heat.beta_pfl` | `heat.m_basissterberate` · `heat.qbar_pfl` | `quelle` · `quelle` | `berechnet` | „berechnet aus Quellen“ |
| 95 | `heat.h_heim` | `heat.qbar_pfl` · `heat.beta_pfl` | `quelle` · `berechnet` (aus Quellen) | `berechnet` | „berechnet aus Quellen“ |
| 96 | `pollen.d_saison` | `pollen.f_symptomtage` · `pollen.p_sens_gruppen` · `pollen.l_saison` | `abschaetzung_kap3` · `abschaetzung_kap3` · `abschaetzung_kap3` | `berechnet` | „berechnet, enthält Abschätzung von KAP3“ |
| 96 | `pollen.c_tag` | `pollen.c_jahr_direkt` · `pollen.d_saison` | `quelle` · `berechnet` (enthält Abschätzung von KAP3) | `berechnet` | „berechnet, enthält Abschätzung von KAP3“ |
| 98 | `uv.ssd_delta_region` | `dwd_cdc_ssd_raster_x_vg250_x_zensus2022` | `quelle` (kein Block) | `quelle` | „Quelle“ |
| 98 | `uv.k_uv` | `lorenz2024_dwd_ssd_trend` · `dwd_cdc_ssd_raster_x_vg250_x_zensus2022` · `uv.ssd_delta_region` | `quelle` (kein Block) · `quelle` (kein Block) · `quelle` | `berechnet` | „berechnet aus Quellen“ |
| 98 | `uv.baf` | `uv.w_scc` · `slaper1996_rivm2023_madronich2021` | `quelle` · `quelle` (kein Block) | `berechnet` | „berechnet aus Quellen“ |
| 98 | `uv.lambda` | `zfkd_kid2025` | `quelle` (kein Block) | `abschaetzung_kap3` | „Abschätzung von KAP3“ |
| 98 | `uv.l_rest` | `zfkd_kid2025_sterbetafel2224` | `quelle` (kein Block) | `abschaetzung_kap3` | „Abschätzung von KAP3“ |
| 98 | `uv.c_kal` | `uv.i_raten_roh` · `zfkd_kid2025` | `quelle` · `quelle` (kein Block) | `berechnet` | „berechnet aus Quellen“ |

uv.lambda und uv.l_rest entscheidet Frage 1 (S2, benannte Näherung), uv.ssd_delta_region Frage 2. Bei diesen drei
Blöcken wertet Regel K die Eingänge nicht aus (Festlegung, b); die Spalten nennen sie, weil der Bericht sie führt. Zur
Zielreihe von heat.c_kal: `rki_eb19_2025` steht im Feld `quelle:`, nicht in `abgeleitet_aus`. Sie zählt nach
Festlegung (c) als `quelle` und ändert das Ergebnis nicht.

### Beispiel-Block

`regel_k`, aus dem Stamm des Produkt-Repos ausführbar (am 06.10.2026 gelaufen, Ausgabe darunter). Er liest die Blöcke
aus Kapitel 7 der drei Berichte und die Tabellen dieser Datei; abgeschrieben wird nichts.

```python
# regel_k — Regel K an allen Kapitel-7-Blöcken von #95, #96 und #98, gegen die Tabellen dieser Datei
import re

BERICHTE = {"95": "95_hitzebelastung", "96": "96_aeroallergene", "98": "98_uv_schaedigungen"}
ANZEIGE = {"quelle": "Quelle", "abschaetzung_kap3": "Abschätzung von KAP3",
           "aus_quellen": "berechnet aus Quellen", "mit_abschaetzung": "berechnet, enthält Abschätzung von KAP3"}
ZUSATZ = {"aus_quellen": "aus Quellen", "mit_abschaetzung": "enthält Abschätzung von KAP3"}
# S2: Näherung, die der Block selbst benennt (die Blöcke schreiben Umlaute teils als ae und ue)
NAEHERUNG = re.compile(r"(?i)proxy|approximation|n(ä|ae)herung|st(ü|ue)tzstelle|extrapol")


def feld(block, name):
    """Wert eines Feldes ohne Kommentar, etwa 'kennzeichnung' → 'berechnet'."""
    m = re.search(r"^\s+" + name + r": ([^#\n]*)", block, re.M)
    return m.group(1).strip() if m else ""


def bloecke(datei):
    """Kapitel-7-Blöcke eines Berichts, geschnitten wie im Prüfausdruck: id → Blocktext."""
    text = open(f"docs/methodik/{datei}.md", encoding="utf-8").read()
    teile = [b.split(chr(96) * 3)[0] for b in re.split(r"\nparameter:", text)[1:]]
    return {re.search(r"id: (\S+)", b).group(1): b for b in teile}


B = {nr: bloecke(d) for nr, d in BERICHTE.items()}
KZ = {nr: {i: feld(b, "kennzeichnung") for i, b in B[nr].items()} for nr in B}
AUS = {nr: {i: [e.strip() for e in feld(b, "abgeleitet_aus").strip("[]").split(",") if e.strip()]
            for i, b in B[nr].items()} for nr in B}
QUELLEN = {nr: {feld(b, "quelle").split()[0] for b in B[nr].values() if feld(b, "quelle")} for nr in B}

# (b) Jeder Eingang ohne Block ist ein Quellenschlüssel aus einem Feld quelle: desselben Berichts
for nr in B:
    for i in B[nr]:
        for e in AUS[nr][i]:
            assert e in B[nr] or ("." not in e and e in QUELLEN[nr]), (nr, i, e)


def setzung(nr, i):
    """Frage 1: S1 erkennbar an abschaetzung_kap3 im Bericht, S2 an der im Block benannten Näherung."""
    return KZ[nr][i] == "abschaetzung_kap3" or bool(NAEHERUNG.search(B[nr][i]))


def regel_k(nr, i):
    """Regel K für Block i in Bericht nr → (Kennzeichnung nach der Regel, Anzeigeklasse)."""
    if setzung(nr, i):                              # Frage 1: Setzung im Block selbst
        return "abschaetzung_kap3", "abschaetzung_kap3"
    ids = [e for e in AUS[nr][i] if e in B[nr]]     # Parameter-IDs
    if not ids:                                     # Frage 2: keine Parameter-ID → quelle
        return "quelle", "quelle"
    schwach = any(regel_k(nr, e)[1] in ("abschaetzung_kap3", "mit_abschaetzung") for e in ids)  # Frage 3
    return "berechnet", "mit_abschaetzung" if schwach else "aus_quellen"


def eingang_text(nr, e):
    """Kennzeichnung eines Eingangs, wie die Spalte „deren Kennzeichnung“ sie schreibt."""
    if e not in B[nr]:
        return "quelle (kein Block)"
    kz, kl = regel_k(nr, e)
    return f"berechnet ({ZUSATZ[kl]})" if kz == "berechnet" else kz


# Die 11 Blöcke, die heute berechnet tragen (dieselbe Auswahl wie der Prüfausdruck)
ELF = [(nr, i) for nr in B for i in B[nr] if re.search(r"^\s+kennzeichnung: berechnet", B[nr][i], re.M)]
assert len(ELF) == 11

# Tabellen dieser Datei lesen, erkannt an ihrer Kopfzeile
q = open("docs/methodik/querschnitt_kennzeichnung.md", encoding="utf-8").read()


def tabelle(kopf):
    """Datenzeilen der Tabelle, deren Kopfzeile mit kopf beginnt, als Listen von Zellen ohne Backticks."""
    zeilen = q.split("\n" + kopf, 1)[1].split("\n\n")[0].splitlines()[2:]
    return [[c.strip().replace(chr(96), "") for c in z.strip().strip("|").split("|")] for z in zeilen]


tab = {(z[0], z[1]): z for z in tabelle("| Bericht | Block-ID | Eingänge |")}
tab_z = {z[0]: tuple(int(x) for x in z[1:]) for z in tabelle("| Bericht | Blöcke | belegt bisher |")}
assert set(tab) == set(ELF), set(tab) ^ set(ELF)

for nr, i in ELF:
    kz, kl = regel_k(nr, i)
    _, _, ein, ein_kz, soll_kz, soll_text = tab[(nr, i)]
    assert ein.split(" · ") == AUS[nr][i], (i, ein)
    assert ein_kz.split(" · ") == [eingang_text(nr, e) for e in AUS[nr][i]], (i, ein_kz)
    assert (soll_kz, soll_text.strip("„“")) == (kz, ANZEIGE[kl]), (i, soll_kz, soll_text)
    print(f"#{nr} {i:<22} {kz:<18} „{ANZEIGE[kl]}“")

# heat.c_kal ausdrücklich: keine eigene Setzung, zwei abgeschätzte Eingänge, die Setzung bewegt den Fit (Feld band)
c = B["95"]["heat.c_kal"]
assert not setzung("95", "heat.c_kal")
assert regel_k("95", "heat.c_kal") == ("berechnet", "mit_abschaetzung")
assert ANZEIGE[regel_k("95", "heat.c_kal")[1]] == tab[("95", "heat.c_kal")][5].strip("„“")
assert [e for e in AUS["95"]["heat.c_kal"] if KZ["95"][e] == "abschaetzung_kap3"] == \
    ["heat.beta_85plus_region", "heat.f_alter"]
assert feld(c, "wert") == "0.581" and "0,559 (s_Sued=1,85)" in c and "0,661 (ohne Sued)" in c
assert "s_Sued 1,65" in B["95"]["heat.beta_85plus_region"]
assert (feld(c, "rolle"), feld(c, "quelle")) == ("kalibrierung", "rki_eb19_2025")
assert regel_k("98", "uv.c_kal") == ("berechnet", "aus_quellen")      # (c) gleiche Regel, anderes Ergebnis

# (a) Grenze, benannt an uv.ssd_delta_region und uv.lambda: ohne Parameter-ID nie berechnet;
#     ssd_delta_region misst seine Zielgröße selbst (quelle), lambda benennt eine Näherung (S2)
for i in ("uv.ssd_delta_region", "uv.lambda", "uv.l_rest"):
    assert KZ["98"][i] == "berechnet" and not [e for e in AUS["98"][i] if e in B["98"]], i
assert regel_k("98", "uv.ssd_delta_region") == ("quelle", "quelle")
assert regel_k("98", "uv.lambda") == regel_k("98", "uv.l_rest") == ("abschaetzung_kap3", "abschaetzung_kap3")
assert "Perioden-Approximation" in B["98"]["uv.lambda"] and "Median-Approximation" in B["98"]["uv.l_rest"]
lam = float(re.search(r"mm: ([\d.]+)", feld(B["98"]["uv.lambda"], "wert")).group(1))
assert abs(3081.0 / 26870 - lam) < 5e-6, lam                          # Zahlenbeispiel in Festlegung (a)
# Gleiche Bauart in #95, gleiche Antwort: Stützstellen, Proxy und lineare Näherung führt #95 als abschaetzung_kap3;
# Quotienten, die ihre Zielgröße selbst messen, bleiben quelle (heat.m_basissterberate, ΔS in #96 Log 25)
for i in ("heat.l_restlebenserwartung", "heat.c_fall", "heat.f_alter"):
    assert KZ["95"][i] == "abschaetzung_kap3" and NAEHERUNG.search(B["95"][i]), i
assert regel_k("95", "heat.m_basissterberate") == regel_k("96", "pollen.delta_s_region") == ("quelle", "quelle")
naeh = sorted(i for nr in B for i in B[nr] if NAEHERUNG.search(B[nr][i]) and KZ[nr][i] != "abschaetzung_kap3")
assert naeh == ["pollen.p_ar", "uv.l_rest", "uv.lambda"], naeh
print("Setzung nach S2, im Bericht nicht abschaetzung_kap3:", naeh)

# Frage 1, Abgrenzung: jeder Block ohne S1 und S2, dessen Text einer Näherung ähnlich sieht, steht in der Festlegung
AEHNLICH = re.compile(r"(?i)ablese|offset|marker|angenommen|annahme|modellgrenze|statt|transfer|(ü|ue)bertr|gesch(ä|ae)tzt")
festlegung = q.split("\n## Festlegung")[1].split("\n### (a)")[0]
aehnlich = sorted(i for nr in B for i in B[nr] if AEHNLICH.search(B[nr][i]) and not setzung(nr, i))
assert aehnlich == ["heat.t0_region", "pollen.delta_s_region", "uv.c_kal", "uv.i_c44", "uv.i_mm", "uv.i_raten_roh",
                    "uv.k_uv"], aehnlich
assert all(i in festlegung for i in aehnlich), [i for i in aehnlich if i not in festlegung]
print("Einer Näherung ähnlich, nach Frage 1 keine Setzung:", aehnlich)

# Wo Regel K von der Kennzeichnung im Bericht abweicht (alle Blöcke, nicht nur die 11)
wechsel = sorted((i, KZ[nr][i], regel_k(nr, i)[0]) for nr in B for i in B[nr] if regel_k(nr, i)[0] != KZ[nr][i])
assert wechsel == [("heat.beta_iso", "quelle", "berechnet"), ("pollen.p_ar", "quelle", "abschaetzung_kap3"),
                   ("uv.l_rest", "berechnet", "abschaetzung_kap3"), ("uv.lambda", "berechnet", "abschaetzung_kap3"),
                   ("uv.ssd_delta_region", "berechnet", "quelle")], wechsel
print("Kennzeichnung weicht vom Bericht ab:", "; ".join(f"{i} {a} → {n}" for i, a, n in wechsel))

# (b) abgeleitet_aus gefüllt, obwohl der Block nach Regel K nicht berechnet ist: alle in Festlegung (b) genannt
gefuellt = sorted(i for nr in B for i in B[nr] if AUS[nr][i] and regel_k(nr, i)[0] != "berechnet")
assert gefuellt == ["heat.delta_kuehlzentren", "heat.delta_vg_morb", "heat.g_s157",
                    "uv.l_rest", "uv.lambda", "uv.ssd_delta_region"], gefuellt
abschnitt_b = q.split("\n### (b)")[1].split("\n### (c)")[0]
assert all(i in abschnitt_b for i in gefuellt), [i for i in gefuellt if i not in abschnitt_b]
print("abgeleitet_aus gefüllt, nach Regel K nicht berechnet:", gefuellt)

# (d) Zählung belegt: bisher quelle + berechnet, nach Regel K „Quelle“ + „berechnet aus Quellen“
zaehl = {nr: (len(B[nr]), sum(KZ[nr][i] in ("quelle", "berechnet") for i in B[nr]),
              sum(regel_k(nr, i)[1] in ("quelle", "aus_quellen") for i in B[nr])) for nr in B}
assert zaehl == tab_z, (zaehl, tab_z)
print("Blöcke, belegt bisher, belegt nach Regel K:", zaehl)
```

Ausgabe:

```
#95 heat.c_kal             berechnet          „berechnet, enthält Abschätzung von KAP3“
#95 heat.beta_pfl          berechnet          „berechnet aus Quellen“
#95 heat.h_heim            berechnet          „berechnet aus Quellen“
#96 pollen.d_saison        berechnet          „berechnet, enthält Abschätzung von KAP3“
#96 pollen.c_tag           berechnet          „berechnet, enthält Abschätzung von KAP3“
#98 uv.ssd_delta_region    quelle             „Quelle“
#98 uv.k_uv                berechnet          „berechnet aus Quellen“
#98 uv.baf                 berechnet          „berechnet aus Quellen“
#98 uv.lambda              abschaetzung_kap3  „Abschätzung von KAP3“
#98 uv.l_rest              abschaetzung_kap3  „Abschätzung von KAP3“
#98 uv.c_kal               berechnet          „berechnet aus Quellen“
Setzung nach S2, im Bericht nicht abschaetzung_kap3: ['pollen.p_ar', 'uv.l_rest', 'uv.lambda']
Einer Näherung ähnlich, nach Frage 1 keine Setzung: ['heat.t0_region', 'pollen.delta_s_region', 'uv.c_kal', 'uv.i_c44', 'uv.i_mm', 'uv.i_raten_roh', 'uv.k_uv']
Kennzeichnung weicht vom Bericht ab: heat.beta_iso quelle → berechnet; pollen.p_ar quelle → abschaetzung_kap3; uv.l_rest berechnet → abschaetzung_kap3; uv.lambda berechnet → abschaetzung_kap3; uv.ssd_delta_region berechnet → quelle
abgeleitet_aus gefüllt, nach Regel K nicht berechnet: ['heat.delta_kuehlzentren', 'heat.delta_vg_morb', 'heat.g_s157', 'uv.l_rest', 'uv.lambda', 'uv.ssd_delta_region']
Blöcke, belegt bisher, belegt nach Regel K: {'95': (30, 13, 12), '96': (14, 5, 2), '98': (22, 11, 9)}
```

## Rechenkette

Format nach Aufgabe §4, hier „Eingänge → Kennzeichnung“ statt „Zahl × Faktor“, weil Regel K einordnet und nicht
rechnet. Am Ende steht kein Euro-Betrag, sondern der Anzeigetext in der Parameterliste. Beispiel: heat.c_kal aus
Bericht 95, der Kalibrierskalar der Sterbefälle durch Hitze. Jede Ebene ist ein Block; die letzte Spalte ist genau
der Text, den die Parameterliste zeigt.

| Ebene | Block | Eingänge | Kennzeichnung der Eingänge | Kennzeichnung nach der Regel | Anzeigetext |
|---|---|---|---|---|---|
| 1 | heat.t0_region: Temperatur, ab der die Sterblichkeit steigt, je Region | keine; Ablesewerte Winklmayr 2022, Abb. 3 | – | `quelle` (Frage 2) | „Quelle“ |
| 2 | heat.beta_85plus_region: Anstieg der Sterblichkeit je Grad, ab 85 Jahren | keine; Nord und Mitte abgelesen, Süd von KAP3 nachgeschätzt (s_Süd = 1,65) | – | `abschaetzung_kap3` (Frage 1, S1) | „Abschätzung von KAP3“ |
| 3 | heat.f_alter: Faktor je Altersband | keine; aus RKI-Anteilen zurückgerechnet, mit linearer Näherung | – | `abschaetzung_kap3` (Frage 1, S1 und S2) | „Abschätzung von KAP3“ |
| 4 | heat.m_basissterberate: Sterbefälle 2023 ÷ Bevölkerung, je Altersband | keine; Quotient amtlicher Summen, misst die Sterberate selbst | – | `quelle` (Frage 2) | „Quelle“ |
| 5 | heat.q_wochenquantile: Temperaturquantile je Woche | keine; aus DWD-Tageswerten ausgezählt | – | `quelle` (Frage 2) | „Quelle“ |
| 6 | heat.c_kal = 0,581: Fit des Modells aus Ebene 1–5 an die hitzebedingten Sterbefälle des RKI 2012–2024 | Ebene 1–5 (Parameter-IDs); dazu die Zielreihe `rki_eb19_2025` im Feld `quelle:`, kein Block | `quelle` · `abschaetzung_kap3` · `abschaetzung_kap3` · `quelle` · `quelle`; Zielreihe zählt als `quelle` (Festlegung, c) | `berechnet` (Frage 1: keine eigene Setzung; Frage 2: fünf Parameter-IDs; Frage 3: schwächster Eingang Ebene 2 und 3) | „berechnet, enthält Abschätzung von KAP3“ |

**Gegenprobe (kein Eintrag der Parameterliste).** Dass die Setzung aus Ebene 2 im Wert von heat.c_kal steckt, zeigt
das Band des Blocks: Mit s_Süd = 1,85 statt 1,65 ergibt der Fit 0,559 statt 0,581, ohne die Region Süd 0,661.

**Zählung (kein Eintrag der Parameterliste).** In der Quellenlage von #95 zählt heat.c_kal nach Regel K als
abgeschätzt. Belegt sind damit 12 statt 13 der 30 Blöcke in Kapitel 7 (Festlegung, d).

**Nacherzählt.** c_kal ist die Zahl, mit der KAP3 das Hitzemodell so einstellt, dass es die Sterbefälle des RKI der
Jahre 2012–2024 trifft. Das Modell besteht aus fünf Bausteinen. Drei stammen aus Quellen. Zwei hat KAP3 selbst
abgeschätzt: den Anstieg der Sterblichkeit im Süden und den Faktor je Altersband. Weil c_kal genau das ausgleicht, was
diese beiden Bausteine verschieben, steckt ihre Abschätzung in c_kal. Ändert man die Abschätzung im Süden, wird aus
0,581 eine 0,559. Deshalb zeigt die Parameterliste „berechnet, enthält Abschätzung von KAP3“ und zählt c_kal nicht als
belegt. Den Ausschlag geben Ebene 2 und 3; ein einziger abgeschätzter Eingang hätte genügt.

**Über zwei Rechenstufen: pollen.c_tag (Bericht 96).** pollen.d_saison = 0,70 × (0,55 × 30 + 0,75 × 60) = 43,05 Tage
folgt aus drei Abschätzungen von KAP3 und zeigt „berechnet, enthält Abschätzung von KAP3“. pollen.c_tag = 266,90 €
÷ 43,05 Tage = 6,20 € je Tag (Preisstand 2024) folgt aus c_jahr (`quelle`) und d_saison. c_tag selbst hat keinen
abgeschätzten Eingang, erbt die Abschätzung aber über d_saison und zeigt ebenfalls „berechnet, enthält Abschätzung von
KAP3“. So wird eine Setzung auch über eine Rechnung weitergereicht nie als Quelle gezeigt.

**Frage 1 an einem Block ohne Parameter-ID: uv.lambda (Bericht 98).** Beim Melanom ergibt 3.081,0 Sterbefälle ÷
26.870 Neuerkrankungen (ZfKD, Mittel 2021–2023) den Wert 0,11466. Beide Zahlen stehen in der Quelle. Das Modell
braucht aber den Anteil der Erkrankten, die am Melanom sterben, und den trifft der Quotient eines Zeitfensters nur
näherungsweise; der Bericht nennt die Richtung selbst: „Überschätzung des Mortalitätsanteils“. Dass diese Näherung
gelten soll, entscheidet KAP3. Deshalb zeigt die Parameterliste „Abschätzung von KAP3“, mit der Herleitung aus den
beiden ZfKD-Zahlen. Zum Vergleich heat.m_basissterberate: Sterbefälle 2023 ÷ Bevölkerung ist genau die Sterberate,
die das Hitzemodell braucht, und die Liste zeigt „Quelle“.

**Was die einfachere Regel verfälschen würde (§8 E3).** Liest man `berechnet` wie heute als belegt und übernimmt die
Kennzeichnung der Berichte, zählen heat.c_kal, pollen.d_saison, pollen.c_tag, pollen.p_ar, uv.lambda und uv.l_rest als
belegt: #95 käme auf 13 statt 12 belegte Blöcke von 30, #96 auf 5 statt 2 von 14, #98 auf 11 statt 9 von 22, und die
Liste zeigte sechs Werte mit Setzung als belegt. Schreibt man stattdessen schlicht „Abschätzung von KAP3“, verliert die Anzeige,
dass c_kal ein Fit an die RKI-Reihe ist und drei seiner fünf Eingänge aus Quellen stammen.

## Entscheidungslog

**Gewählt:** Ansatz B, die Vererbung der schwächsten Kennzeichnung über alle Stufen, angezeigt als Verbindung, mit
der Grenze zwischen `quelle` und `berechnet` aus Aufgabe §4 und dem Prüfstein aus #95 Log 40 als Frage 1 für alle
Berichte. Verworfen, je in einem Satz:

- **Ansatz A** (`berechnet` als neutrale Klasse wie heute, gelesen wie belegt): Er zeigt heat.c_kal, pollen.d_saison
  und pollen.c_tag als belegt, obwohl in ihnen Setzungen von KAP3 stecken, und verletzt damit den Prüfstein aus P1.
- **Ansatz C** (ein berechneter Wert mit abgeschätztem Eingang heißt schlicht `abschaetzung_kap3`): Er hält den
  Prüfstein ein, verliert in der Anzeige aber, dass der Wert aus anderen Parametern folgt und welche davon belegt
  sind, also die Herleitung, die P1 verlangt.
- **Ansatz D** (Urteil je Block ohne feste Regel): Er ließ die Berichte bei gleicher Bauart auseinanderlaufen (eine
  benannte Näherung in #95 `abschaetzung_kap3`, in #96 `quelle`, in #98 `berechnet`) und ließe sich weder im
  Beispiel-Block noch im Code nachrechnen, während Regel K auch Frage 1 nach festen Merkmalen beantwortet.
- **Erkennung von S2 an einer festen Wortliste** (wie in der zweiten Fassung dieser Datei): Sie übersah die
  Extrapolation in pollen.p_ar, die der Block mit einem anderen Wort benennt, deshalb entscheidet die Aussage des
  Blocks und nicht das Wort.
- **Teil-Näherung nur am Band kennzeichnen** (pollen.p_ar bleibt `quelle`, weil vier von fünf Bändern einen Quellwert
  tragen, #96 Log 25): Sie zeigte die Altersgruppen ab 80 Jahren, für die DEGS1 keine Zahl hat, als Quelle und
  behandelte p_ar anders als heat.beta_85plus_region, bei dem der Süd-Wert allein die Kennzeichnung bestimmt.
- **Benannte Näherung als Modellgrenze statt als Setzung** (uv.lambda und uv.l_rest wären `quelle`, wie in der ersten
  Fassung dieser Datei): Sie zeigte in #98 als Quelle, was #95 bei gleicher Bauart (Stützstellen in
  heat.l_restlebenserwartung, Proxy heat.c_fall) als Abschätzung führt, und verletzte damit den Prüfstein aus P1.
- **Grenze nach #98 Log 36** (jede eigene Auswertung amtlicher Daten ist `berechnet`): Sie widerspricht Aufgabe §4,
  wonach `berechnet` aus anderen Parametern folgt, und machte jede Sterberate und jedes ausgezählte Quantil zu
  `berechnet`, ohne dass der Leser etwas über Setzungen erfährt.
- **Ausnahme für umgerechnete Studienzahlen** (heat.beta_iso bleibt `quelle`, obwohl er den Block heat.qbar_1p nutzt,
  #95 Log 40): Sie verlangt ein Urteil je Block, und heat.beta_iso zählt als „berechnet aus Quellen“ ebenso als
  belegt.
- **Kalibrierskalar als `quelle`, weil gegen eine amtliche Reihe gefittet**: Das verwechselt die an die Reihe
  angepasste Summe mit dem Skalar, der die Setzungen des Modells ausgleicht und sich mit ihnen ändert (heat.c_kal
  0,559 statt 0,581 bei s_Süd = 1,85).
- **Quellenschlüssel ohne Block wie eine Abschätzung zählen**: Das stellte Zahlen einer Quelle schlechter als einen
  Block mit denselben Zahlen und überzeichnete die Unsicherheit amtlicher Quotienten.
- **Fünfter Anzeigetext „Quelle, ausgewertet von KAP3“**: Die Auswertung steht schon in der Herleitung, die P1 je
  Parameter verlangt, und der Text zeigte gleich gerechnete Blöcke verschieden, weil etwa heat.m_basissterberate kein
  `abgeleitet_aus` führt.

**Abgrenzung zur Gewissheit.** Regel K sagt, woher der Wert eines Parameters stammt. Die Gewissheit einer
Klimawirkung legt Regel G in [querschnitt_gewissheit.md](querschnitt_gewissheit.md) fest: Sie übernimmt die Gewissheit
der Bewertung aus KWRA TB6 Tabelle 1 und rechnet sie nicht aus Parametern. Die Quellenlage der Parameter erscheint
dort nur als Zählung zum Vergleich und geht in die Gewissheit nicht ein. Regel K ändert diese Zählung (Festlegung, d),
aber keine Stufe nach Regel G. querschnitt_gewissheit.md bleibt unverändert.
