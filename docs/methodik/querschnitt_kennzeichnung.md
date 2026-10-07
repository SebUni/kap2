# Querschnitt: Kennzeichnung berechneter Parameter

Querschnittsdatei der Methodik, gültig für alle 102 Klimawirkungen der KWRA 2021. Angewendet wird sie heute nur auf
#95, #96 und #98 (A-0048; Vorhaben T-1808-cmo, Eltern T-1795-ceo). Schritt 1 (Ticket T-1834-methodik_manager, ersetzt
T-1812-methodik_manager) legt die Regel fest und rechnet sie an den 11 Blöcken nach, die heute `kennzeichnung:
berechnet` tragen. Schritt 2 schreibt die Übernahmeliste an den CTO und die Befunde an die Berichte. Anlass ist Befund
224 im Ledger #95: Die Parameterliste zeigt heat.c_kal als „berechnet aus anderen Parametern“, und das Produkt zählt
das wie „belegt“, obwohl in c_kal zwei Abschätzungen von KAP3 stecken (Bericht 95, Kap. 7, Absatz „Kennzeichnung
`berechnet`“).

Begriffe: **Block** = Parameter-Block in Kapitel 7 eines Berichts (Aufgabe §4, „Parameter-Block-Format“).
**Eingang** = ein Eintrag im Feld `abgeleitet_aus` eines Blocks. **Parameter-ID** = Eingang, der selbst ein Block
desselben Berichts ist. **Quellenschlüssel** = Eingang ohne eigenen Block, etwa `zfkd_kid2025`; er steht im Feld
`quelle:` eines Blocks. **Setzung** = eine Zahl oder Wahl von KAP3, die so in keiner Quelle steht. Woran Regel K eine
Setzung erkennt, legt Frage 1 mit den Merkmalen S1 und S2 fest.

## Festlegung

**Regel K (Kennzeichnung eines Parameters).** Für jeden der 11 berechneten Blöcke beantwortet die Parameterliste drei
Fragen in dieser Reihenfolge. Die erste Antwort „ja“ entscheidet. Alle übrigen Blöcke und alle Eingänge übernimmt
Regel K mit der Kennzeichnung ihres Berichts; sie ordnet keinen nicht berechneten Block neu ein.

1. **Steckt im Wert des Blocks selbst eine Setzung von KAP3?** Ja: Kennzeichnung `abschaetzung_kap3`, Anzeigetext
   „Abschätzung von KAP3“. Das gilt auch, wenn der Block zusätzlich andere Blöcke nutzt, und es genügt, dass ein Teil
   des Werts die Setzung trägt, etwa ein Band, eine Region oder der Zellwert. Frage 1 ist ein allgemeines Merkmal für
   alle Klimawirkungen; Grundlage ist der Prüfstein aus #95 Log 40. Eine Setzung liegt vor, wenn eines der beiden
   Merkmale zutrifft:
   - **S1 Zahl von KAP3:** KAP3 setzt oder schätzt eine Zahl, die so in keiner Quelle steht, etwa die
     Süd-Nachschätzung s_Süd = 1,65 in heat.beta_85plus_region (Nord und Mitte sind abgelesen). Erkennbar daran, dass
     der Bericht den Block als `abschaetzung_kap3` führt.
   - **S2 Näherung:** Der Wert stammt aus Zahlen einer Quelle, ein Teil davon steht aber für eine Größe, für die die
     Quelle keine Zahl ausweist: für eine andere Größe (Proxy: heat.c_fall, uv.lambda), für einen anderen Raum, eine
     andere Zeit oder eine andere Gruppe (Extrapolation: heat.beta_pfl, uv.k_uv), als Punkt statt Bandmittel
     (Stützstellen in heat.l_restlebenserwartung, medianes Sterbealter in uv.l_rest) oder in vereinfachter Form
     (lineare Näherung in heat.f_alter, additive Form in pollen.d_saison). **Ein Studienwert zählt als Extrapolation
     nach S2, wenn der Bericht ihn für einen anderen Raum, eine andere Zeit oder eine andere Gruppe nutzt, als die
     Quelle ausweist; ausgenommen ist ein Wert, dessen Geltung die Quelle selbst so ausweist.** Erkennbar ist S2 an
     der Aussage, nicht an einem bestimmten Wort: Der Block, die Stelle, auf die sein `herkunft` verweist, oder §6
     (Modellgrenzen) des Berichts sagt, dass ein Teil des Werts so entsteht.

   **Eine benannte Näherung ist immer eine Setzung**, gleich ob der Bericht sie als Modellgrenze, als gekennzeichnete
   Näherung oder als Abschätzung führt. Keine Setzung ist es, wenn der Wert seine Zielgröße selbst misst, auch wenn
   KAP3 ihn aus Zahlen der Quelle rechnet oder zwischen Quellenwerten wählt. Ein aus einer Abbildung der Quelle
   abgelesener Wert misst die Größe, die die Quelle zeigt; Ablesen allein ist keine Setzung, die Ableseunsicherheit
   gehört ins Band.

   **Angewendet wird das Merkmal hier nur auf die 11 Blöcke** (Entscheidung je Block in „Anwendung auf M0“, Tabelle
   „Frage 1 je Block“). Die übrigen Blöcke werden in den Runden der Berichte daran gemessen; wo ein begründeter Zweifel
   besteht, steht er in der Liste „Zweifel an Kennzeichnungen außerhalb der 11 Blöcke“.
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
Eingangs über alle Stufen bis zum Anzeigetext durch. Für einen Eingang außerhalb der 11 trägt der Bericht die
Kennzeichnung; zweifelt diese Datei daran, steht der Block in der Zweifel-Liste, und die Tabelle der 11 sagt, was sich
an der Anzeige ändert, wenn der Zweifel zutrifft.

### (a) Grenze zwischen `quelle` und `berechnet`

`berechnet` ist ein Block genau dann, wenn er keine Setzung enthält (Frage 1) und `abgeleitet_aus` mindestens eine
Parameter-ID nennt. Eine Rechnung, die nur Zahlen einer Quelle verarbeitet, ist nie `berechnet`, auch wenn KAP3 sie
selbst ausführt: Sie ist `quelle`, wenn sie ihre Zielgröße selbst misst, und `abschaetzung_kap3`, wenn sie eine
Näherung nach S2 trägt. Der Wortlaut von Aufgabe §4 trägt die Grenze zu `berechnet`: „`berechnet`: der Wert folgt
rechnerisch aus anderen Parametern“, und `abgeleitet_aus` nennt „die Parameter-IDs, aus denen der Wert entsteht“.
#95 Log 40 zieht beide Grenzen so: „`berechnet` nur, wo der Wert aus anderen Blöcken folgt“, dazu der Prüfstein für
Setzungen, den Frage 1 übernimmt. #96 Log 25 folgt der Grenze zu `berechnet` (ΔS als ausgewertete amtliche
Messreihe = `quelle`). #98 Log 36 zieht die Grenze zu `berechnet` anders („schwächste Herkunft im Block“, eigene
Auswertung = `berechnet`). Nach Regel K gilt diese Abweichung für die drei betroffenen Blöcke nicht mehr, und #95 Log
40 und #98 Log 36 laufen an ihnen nicht mehr auseinander:

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
  2023 ÷ Bevölkerung ist genau die Sterberate, die das Modell braucht, und der Bericht führt sie als `quelle`.
- **uv.l_rest** (Restlebenserwartung am medianen Sterbealter): ebenfalls keine Parameter-ID. Der Block benennt eine
  „Median-Approximation“, also einen Punkt statt des Mittels über alle Sterbealter (S2). Nach Regel K
  `abschaetzung_kap3`, wie die Stützstellen e(60), e(70) und e(80) in heat.l_restlebenserwartung, die #95 nach Log 40
  als `abschaetzung_kap3` führt.

Was die Grenze für Blöcke außerhalb der 11 bedeuten würde, etwa für heat.beta_iso mit der Parameter-ID heat.qbar_1p,
entscheidet die Runde am Bericht (Zweifel-Liste).

### (b) Eingang ohne eigenen Block (Quellenschlüssel in `abgeleitet_aus`)

Ein Quellenschlüssel zählt als Eingang mit der Kennzeichnung `quelle`. Allein macht er einen Block nicht zu
`berechnet`, denn dafür verlangt §4 eine Parameter-ID. Steht er neben einer Parameter-ID, zählt er bei Frage 3 als
`quelle`. Bedingung: Der Schlüssel steht im Feld `quelle:` eines Blocks desselben Berichts, und hinter ihm stehen nur
Zahlen der Quelle. Eine Zahl, die KAP3 setzt, braucht einen eigenen Block, weil P1 jeden Parameter in der Liste
verlangt; hinter einem Schlüssel darf sie nicht stehen. Ob ein Schlüssel später einen eigenen Block bekommt (#98,
Befund 463), ändert das Ergebnis nicht, solange dieser Block eine reine Auswertung der Quelle ist.

**`abgeleitet_aus` bei einem Block, der nach Regel K nicht `berechnet` ist.** Aufgabe §4 verlangt dort ein leeres
Feld („sonst leer“). Elf Blöcke führen es dennoch. Nur mit Quellenschlüsseln: uv.ssd_delta_region (`quelle`),
uv.lambda und uv.l_rest (`abschaetzung_kap3`). Mit mindestens einer Parameter-ID: uv.k_uv, heat.beta_pfl,
heat.h_heim, pollen.d_saison und pollen.c_tag (nach Frage 1 `abschaetzung_kap3`) sowie heat.g_s157,
heat.delta_vg_morb und heat.delta_kuehlzentren (`abschaetzung_kap3` im Bericht). Regel K wertet das Feld dort nicht
aus: Bei den acht Blöcken unter den 11 hat Frage 1 oder 2 entschieden, bevor Frage 3 es liest, und die drei Blöcke aus
#95 außerhalb der 11 tragen die Kennzeichnung ihres Berichts. Das Feld gilt als Verweis auf die Herleitung und als
benannte Abweichung von §4. Für die vier Blöcke aus #98 hat #98 Log 36 diese Abweichung begründet (Teil 3 der
Gegenprüfung, Befund 460; uv.k_uv nennt Log 36 in seinem Kommentar selbst): Der Quellenschlüssel bleibt, bis die
Eingänge eigene Blöcke haben (Befund 463). Diese Begründung setzt voraus, dass die Blöcke `berechnet` sind; nach
Regel K sind sie es nicht. heat.beta_pfl, heat.h_heim, pollen.d_saison und pollen.c_tag führen das Feld, weil ihr
Bericht sie heute als `berechnet` kennzeichnet. Ob das Feld bei den elf Blöcken geleert oder die Abweichung neu
begründet wird, ist ein Befund an die Berichte (Schritt 2). Bis dahin gilt die Lesart dieses Absatzes. heat.beta_iso
führt das Feld ebenfalls, als `quelle` des Berichts; er zählt nicht zu den elf und steht in der Zweifel-Liste.

### (c) Kalibrierskalar, gefittet gegen eine amtliche Reihe

Ein Kalibrierskalar ist ein berechneter Block wie jeder andere. Seine Eingänge sind die Blöcke des Modells, das er an
die Reihe anpasst, und die Reihe selbst. Die Reihe zählt als `quelle`, gleich ob sie in `abgeleitet_aus` oder nur im
Feld `quelle:` steht; sie kann den schwächsten Eingang nicht anheben. Grund: Der Fit gleicht genau das aus, was die
Setzungen im Modell verschieben. Ändert sich eine Setzung, ändert sich der Skalar. Belegt ist nach dem Fit die Summe
aus Modell und Skalar, die an die Reihe angepasst ist, nicht der Skalar.

- **heat.c_kal** = 0,581, Fit gegen die RKI-Reihe 2012–2024 (`rki_eb19_2025`). Frage 1: nein; der Fit ist eine
  Wahl zwischen Quellenwerten (#95 Log 40). Eingänge mit der Kennzeichnung des Berichts: heat.t0_region,
  heat.m_basissterberate und heat.q_wochenquantile (`quelle`), heat.beta_85plus_region (Süd-Nachschätzung) und
  heat.f_alter (lineare Näherung), beide `abschaetzung_kap3`. Nach Regel K `berechnet`, Anzeigetext „berechnet,
  enthält Abschätzung von KAP3“. Dass die Setzung im Wert steckt, zeigt das Band des Blocks: Mit s_Süd = 1,85 statt
  1,65 ergibt der Fit 0,559, ohne die Region Süd 0,661. heat.t0_region und heat.q_wochenquantile stehen in der
  Zweifel-Liste; die Anzeige von c_kal ändert sich dadurch nicht.
- **uv.c_kal** = ZfKD-Anker ÷ Modellsumme der Rohraten. Frage 1: nein; der Block nennt die Ablesewerte seines
  Eingangs, und Ablesen allein ist keine Setzung. Eingänge: uv.i_raten_roh (`quelle`) und `zfkd_kid2025`
  (Quellenschlüssel). Nach Regel K `berechnet`, Anzeigetext „berechnet aus Quellen“. Trifft der Zweifel an
  uv.i_raten_roh zu, zeigt uv.c_kal „berechnet, enthält Abschätzung von KAP3“.

Regel K wertet `abgeleitet_aus` so aus, wie der Bericht es führt. Ob die Liste vollständig ist, prüft der Bericht
(Aufgabe §4: Pflichtfeld bei `berechnet`).

### (d) Zählung als belegt in Gewissheitsstufe und Unsicherheits-Zusammenschau

**Ja, Regel K ändert, was als belegt zählt.** Ein berechneter Block zählt nur dann als belegt, wenn kein Eingang über
alle Stufen eine Abschätzung von KAP3 trägt, und ein Block mit benannter Näherung zählt nie als belegt. Heute zählt das
Produkt jeden berechneten Parameter als belegt: `BELEGTE_KLASSEN = frozenset({"belegt", "berechnet"})`
(`backend/app/services/parameter_registry.py`, Z. 102), genutzt in `gewissheit.py` (Z. 86) und
`unsicherheits_zusammenschau.py` (Z. 99), festgeschrieben in `backend/tests/test_evidence_class_berechnet.py`, Teil (a) und (c).
**Begründung:** Die Zählung „x von y Parametern mit Quelle“ ist dieselbe Aussage wie die Parameterliste, nur
verdichtet. Zählte heat.c_kal dort als belegt, zeigte die Zählung eine Setzung als Quelle, gegen den Prüfstein. Wie
viel sich verschiebt, zeigt die Zählung über die Blöcke in Kapitel 7 (nachgerechnet im Beispiel-Block; außerhalb der
11 mit der Kennzeichnung des Berichts):

| Bericht | Blöcke | belegt bisher | belegt nach der Regel |
|---|---|---|---|
| 95 | 31 | 13 | 10 |
| 96 | 14 | 5 | 3 |
| 98 | 22 | 11 | 8 |

Acht der 11 Blöcke zählen danach nicht mehr als belegt: bei #95 heat.c_kal, heat.beta_pfl und heat.h_heim, bei #96
pollen.d_saison und pollen.c_tag, bei #98 uv.k_uv, uv.lambda und uv.l_rest. uv.ssd_delta_region wechselt von
`berechnet` nach `quelle` und bleibt belegt. Blöcke aus der Zweifel-Liste ändern die Zählung erst, wenn die Runde am
Bericht ihre Kennzeichnung ändert.
**Die Gewissheit nach Regel G ändert sich nicht:** Sie übernimmt die Stufe der KWRA (TB6 Tabelle 1) und nimmt die
Quellenlage nicht auf ([querschnitt_gewissheit.md](querschnitt_gewissheit.md), „Festlegung“). Solange der Code die
Stufe noch aus dem Anteil der belegten Parameter bildet (`gewissheit.py`, `gewissheitsstufe`), verschiebt Regel K auch
diese Stufe, und die Unsicherheits-Zusammenschau führt die acht Werte als nicht belegt. Wie der Code das umsetzt,
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
  #96 und #98. Mit der Extrapolation nennt S2 eine Form, die Log 40 nicht ausdrücklich nennt; sie folgt aus demselben
  Gedanken (der Wert steht für eine Größe, für die die Quelle keine Zahl ausweist).

**Was Regel K dem Bericht überlässt.** Regel K entscheidet jede der drei Fragen für die 11 Blöcke selbst. Aus dem
Bericht übernimmt sie nur Tatsachen: welche Zahl KAP3 setzt (S1, `abschaetzung_kap3`), welche Näherung der Bericht
benennt (S2) und welche Eingänge `abgeleitet_aus` nennt. Die Kennzeichnung eines nicht berechneten Blocks gehört dem
Bericht. Ob ein Bericht jede Setzung und jede Näherung benennt, prüft seine Gegenprüfung (Aufgabe §3.9, §5). Einen
Block, den der Bericht als `abschaetzung_kap3` führt, stuft Regel K nie herauf.

## Anwendung auf M0: die 11 berechneten Blöcke

Alle 11 Blöcke tragen im Bericht heute `kennzeichnung: berechnet`. Eingänge in der Reihenfolge von `abgeleitet_aus`,
ihre Kennzeichnung in derselben Reihenfolge: außerhalb der 11 die des Berichts, innerhalb der 11 die nach Regel K;
„kein Block“ heißt Quellenschlüssel (Festlegung, b). Die letzte Spalte nennt jeden Eingang aus der Zweifel-Liste, der
über `abgeleitet_aus` in den Block eingeht, über alle Stufen, und die Anzeige, falls sein Zweifel zutrifft.

| Bericht | Block-ID | Eingänge | deren Kennzeichnung | Kennzeichnung nach der Regel | Anzeigetext | Änderung, falls ein Zweifel zutrifft |
|---|---|---|---|---|---|---|
| 95 | `heat.c_kal` | `heat.t0_region` · `heat.beta_85plus_region` · `heat.f_alter` · `heat.m_basissterberate` · `heat.q_wochenquantile` | `quelle` · `abschaetzung_kap3` · `abschaetzung_kap3` · `quelle` · `quelle` | `berechnet` | „berechnet, enthält Abschätzung von KAP3“ | `heat.q_wochenquantile` · `heat.t0_region`: keine Änderung, weil c_kal über heat.beta_85plus_region und heat.f_alter ohnehin eine Abschätzung von KAP3 enthält |
| 95 | `heat.beta_pfl` | `heat.m_basissterberate` · `heat.qbar_pfl` | `quelle` · `quelle` | `abschaetzung_kap3` | „Abschätzung von KAP3“ | `heat.qbar_pfl`: keine Änderung, weil beta_pfl nach Frage 1 selbst eine Setzung trägt |
| 95 | `heat.h_heim` | `heat.qbar_pfl` · `heat.beta_pfl` | `quelle` · `abschaetzung_kap3` | `abschaetzung_kap3` | „Abschätzung von KAP3“ | `heat.qbar_pfl`: keine Änderung, weil h_heim nach Frage 1 selbst eine Setzung trägt |
| 96 | `pollen.d_saison` | `pollen.f_symptomtage` · `pollen.p_sens_gruppen` · `pollen.l_saison` | `abschaetzung_kap3` · `abschaetzung_kap3` · `abschaetzung_kap3` | `abschaetzung_kap3` | „Abschätzung von KAP3“ | kein Eingang aus der Zweifel-Liste: keine Änderung |
| 96 | `pollen.c_tag` | `pollen.c_jahr_direkt` · `pollen.d_saison` | `quelle` · `abschaetzung_kap3` | `abschaetzung_kap3` | „Abschätzung von KAP3“ | `pollen.c_jahr_direkt`: keine Änderung, weil c_tag über pollen.d_saison ohnehin eine Abschätzung von KAP3 enthält und nach Frage 1 selbst eine Setzung trägt |
| 98 | `uv.ssd_delta_region` | `dwd_cdc_ssd_raster_x_vg250_x_zensus2022` | `quelle (kein Block)` | `quelle` | „Quelle“ | kein Eingang aus der Zweifel-Liste: keine Änderung |
| 98 | `uv.k_uv` | `lorenz2024_dwd_ssd_trend` · `dwd_cdc_ssd_raster_x_vg250_x_zensus2022` · `uv.ssd_delta_region` | `quelle (kein Block)` · `quelle (kein Block)` · `quelle` | `abschaetzung_kap3` | „Abschätzung von KAP3“ | kein Eingang aus der Zweifel-Liste: keine Änderung |
| 98 | `uv.baf` | `uv.w_scc` · `slaper1996_rivm2023_madronich2021` | `quelle` · `quelle (kein Block)` | `berechnet` | „berechnet aus Quellen“ | `uv.w_scc`: Anzeige wird „berechnet, enthält Abschätzung von KAP3“ |
| 98 | `uv.lambda` | `zfkd_kid2025` | `quelle (kein Block)` | `abschaetzung_kap3` | „Abschätzung von KAP3“ | kein Eingang aus der Zweifel-Liste: keine Änderung |
| 98 | `uv.l_rest` | `zfkd_kid2025_sterbetafel2224` | `quelle (kein Block)` | `abschaetzung_kap3` | „Abschätzung von KAP3“ | kein Eingang aus der Zweifel-Liste: keine Änderung |
| 98 | `uv.c_kal` | `uv.i_raten_roh` · `zfkd_kid2025` | `quelle` · `quelle (kein Block)` | `berechnet` | „berechnet aus Quellen“ | `uv.i_raten_roh`: Anzeige wird „berechnet, enthält Abschätzung von KAP3“ |

Frage 1 entscheidet bei sieben Blöcken (Antwort „ja“), Frage 2 bei uv.ssd_delta_region und Frage 3 bei heat.c_kal,
uv.baf und uv.c_kal. Bei einem Block mit
„ja“ und bei uv.ssd_delta_region wertet Regel K die Eingänge nicht aus (Festlegung, b); die Spalten nennen sie, weil
der Bericht sie führt. Zur Zielreihe von heat.c_kal: `rki_eb19_2025` steht im Feld `quelle:`, nicht in
`abgeleitet_aus`. Sie zählt nach Festlegung (c) als `quelle` und ändert das Ergebnis nicht.

**Frage 1 je Block.** Geprüft ist jeder Block an drei Stellen: im Block, an der Stelle, auf die sein `herkunft`
verweist, und in §6 (Modellgrenzen) des Berichts. Der Beleg steht wörtlich im Bericht; Zeilen nach dem Stand vom
07.10.2026.

| Bericht | Block-ID | Frage 1 | Form | Beleg | Fundstellen (Block · herkunft · §6) |
|---|---|---|---|---|---|
| 95 | `heat.c_kal` | nein | Fit, Wahl zwischen Quellenwerten (#95 Log 40) | Kleinste-Quadrate-Fit des Modells gegen die RKI-Reihe 2012-2024 | Block, Feld `kennzeichnung` · §4 #c-kal · Modellgrenzen 1–4 (Z. 1461–1472) betreffen die Eingänge oder den Fit, keine Setzung im Skalar |
| 95 | `heat.beta_pfl` | ja | S2, Extrapolation: Exzess-Verhältnis aus Frankreich 2003 für Deutschland | F 2003 / DE | Block, Feld `kennzeichnung` („Kette §3.3b (Fouillet …)“) · Register 95-S153-01 (Z. 156), Spalte „Übertragbarkeit“ · §6: keine Stelle einschlägig |
| 95 | `heat.h_heim` | ja | S2, Proxy: Zellwert aus OSM-Pflegeeinrichtungen statt Heimquote der Zelle | OSM-Pflegeeinrichtungen × Pflegestatistik (Proxy, Fallback §3.6) | Block, Feld `wert` („je Zelle q_pfl,z …“) · Register 95-S153-01 (Z. 156), Spalte „Datenlage je Zelle“ · §6: keine Stelle einschlägig |
| 96 | `pollen.d_saison` | ja | S2, vereinfachte Form: Doppelt-Sensibilisierte doppelt gezählt | additive Form EUR-konservativ | Block, Feld `band` (Z. 2258) · §3.5 #d-saison · §6: keine Stelle einschlägig |
| 96 | `pollen.c_tag` | ja | S2, Proxy: Durchschnitts-Kostensatz eines Fallmix für jeden Symptomtag, wie heat.c_fall nach #95 Log 40 | Durchschnitts-Kostensatz für einen | Block, Feld `kennzeichnung` · §3.5 #c-tag, „Proxy-Kennzeichnung“ (Z. 863) · Modellgrenze 6 „Kostensatz: Proxy“ (Z. 2025) |
| 98 | `uv.ssd_delta_region` | nein | misst die Zielgröße selbst (eigene Auswertung einer amtlichen Messreihe) | amtliche Messreihe, eigene Auswertung | Block, Feld `kennzeichnung` · Register 98-E20-01 (Z. 271) · §6: keine Stelle einschlägig |
| 98 | `uv.k_uv` | ja | S2, Extrapolation: Elastizität aus einem Messpunkt für alle Gemeinden und als zeitinvariant angenommen | Gekennzeichnete Annahme (Befund 292) | Block, Feld `band` („zeitinvariant angenommen“, Z. 1651) · Register 98-E20-02 · Modellgrenze 2 (Z. 1468–1489, Annahme Z. 1476, Zeitinvarianz Z. 1482) und 9 (Z. 1516) |
| 98 | `uv.baf` | nein | Studienwert, dessen Geltung die Quelle selbst ausweist | international etabliert (Montreal-Protokoll-Folgenabschätzung) | Block, Feld `kennzeichnung` · Register 98-E20-04 (Z. 274) · §6: keine Stelle einschlägig |
| 98 | `uv.lambda` | ja | S2, Proxy: Periodenquotient für den Letalitätsanteil | Perioden-Approximation | Block, Feld `band` · Register 98-K1-02 (Z. 277) · §6: keine Stelle einschlägig |
| 98 | `uv.l_rest` | ja | S2, Punkt statt Bandmittel: medianes Sterbealter | Median-Approximation | Block, Feld `band` · Register 98-K1-02 (Z. 277) · §6: keine Stelle einschlägig |
| 98 | `uv.c_kal` | nein | Quotient aus Anker und Modellsumme; Ablesewerte des Eingangs | = ZfKD-Anker (Mittel 2021-2023) / Modellsumme der Rohraten | Block, Feld `kennzeichnung` · §3.3 #i-raten · Modellgrenze 5 (Z. 1497) betrifft den Eingang uv.i_raten_roh, Modellgrenze 8 (Z. 1515) die Einwohnerbasis der Produktion |

**Zu uv.baf und heat.beta_pfl.** Beide nutzen einen Studienwert in Deutschland. Fouillet misst das Exzess-Verhältnis
für Frankreich 2003, und das Register führt die Übertragung „F 2003 / DE“ selbst; die Verstärkungsfaktoren der BAF
dagegen weist die Quelle als biologisch-epidemiologisches Standardmodell ohne räumliche Grenze aus („international
etabliert“, „unabhängig bestätigt“). Trüge diese Abgrenzung nicht, wäre uv.baf eine Setzung, und #98 hätte nach der
Regel 7 statt 8 belegte Blöcke.

**Zu uv.k_uv (Runde 2 an T-1812, Mangel 1 Nr. 3).** Der Block führt einen Wert für alle Gemeindepunkte und alle
Zeiten. #98 benennt beide Übertragungen selbst: die Skaleninvarianz aus einem Messpunkt als „Gekennzeichnete Annahme“
(Modellgrenze 2), die Zeitinvarianz (Modellgrenze 2 und Block) und die räumliche Streuung (Modellgrenze 9). Ein Wert
für alle zählt damit wie ein eigener Eintrag für eine andere Zeit oder einen anderen Ort: S2, Extrapolation.

**Zu pollen.c_tag.** #96 §3.5 führt den Wert als „Proxy-Kennzeichnung“ und als „Durchschnitts-Kostensatz für einen
spezifischen Fallmix“, Modellgrenze 6 als „Kostensatz: Proxy“. Das ist dieselbe Bauart wie heat.c_fall, der
Durchschnitt aller Krankenhausfälle, den #95 nach Log 40 als `abschaetzung_kap3` führt.

### Zweifel an Kennzeichnungen außerhalb der 11 Blöcke

Durchgesehen sind die 18 Blöcke, die außerhalb der 11 `kennzeichnung: quelle` tragen (gemessen am 07.10.2026); nur
bei ihnen kann die Parameterliste eine Setzung als Quelle zeigen. Blöcke mit `abschaetzung_kap3` sind nicht
durchzusehen. Die Liste ordnet nichts neu ein: **Die Runde am jeweiligen Bericht entscheidet**, auch über die
Fundstelle. Bis dahin gilt die Kennzeichnung des Berichts. Je Block steht die Fundstelle, die Form nach dem Merkmal und
genau ein Sollzustand nach dem Merkmal.

| Bericht | Block-ID | Fundstelle | Form | Sollzustand |
|---|---|---|---|---|
| 95 | `heat.t0_region` | Register 95-E02-01 (Z. 150): „Skalentransfer Region→Zelle als Modellgrenze (§6)“; Modellgrenze 3 (Z. 1470) | S2, Proxy: Schwelle der Region für jede Zelle; das Ablesen aus Winklmayr 2022, Abb. 3 ist keine Setzung | `abschaetzung_kap3` |
| 95 | `heat.q_wochenquantile` | Modellgrenze 1 (Z. 1461): Quantile bilden das „mittlere“ Jahr ab | S2, Punkt statt Bandmittel: das klimatologisch mittlere Jahr für jedes Jahr | `abschaetzung_kap3` |
| 95 | `heat.e_hd` | Register 95-E02-02 (Z. 151): „Alterstabelle nicht publiziert (top-kodiert > 75)“; §3.4 (Z. 684–686): e_HD „als gleiche relative Elastizität über alle Bänder (dokumentierte Annahme …)“ | S2, Extrapolation: ein Wert der Gesamtstudie für alle Altersbänder, wie bei uv.w_scc | `abschaetzung_kap3` |
| 95 | `heat.beta_iso` | Register 95-S152-02 (Z. 155): „Chicago 1995 (Todesfälle)“; Zeichentabelle (Z. 842): Band als „KI-Approximation“ | S2, Extrapolation: OR aus Chicago 1995 für Deutschland; das Merkmal geht hier über #95 Log 40 hinaus, das eine nur umgerechnete Studienzahl als `quelle` führt (Befund 136), und nach der Grenze (a) wäre der Block wegen heat.qbar_1p in `abgeleitet_aus` sonst `berechnet` | `abschaetzung_kap3` |
| 95 | `heat.qbar_pfl` | Register 95-S153-01 (Z. 156), Spalte „Datenlage je Zelle“: „Proxy, Fallback §3.6“ | S2, Proxy: Zellwert aus OSM-Pflegeeinrichtungen; der Kommunenwert 0,149 ist ein Quotient amtlicher Summen | `abschaetzung_kap3` |
| 95 | `heat.gamma_hoehe` | Block: `quelle: icao_standardatmosphaere` (Z. 1741), `herkunft` verweist auf Register 95-W124-01 (Z. 152), den Stadtklima-Zuschlag | S2, Proxy: Gradient der Standardatmosphäre für den bodennahen Gradienten | `abschaetzung_kap3` |
| 95 | `heat.ror_s157` | Register 95-S157-01 (Z. 163): „Ontario 2010–2023; Deutschland 2025/2026“ | S2, Extrapolation: Odds-Verhältnis aus Ontario für deutsche Heime | `abschaetzung_kap3` |
| 96 | `pollen.delta_s_region` | Block, Feld `band`: „Birke-Marker-Offset bis −1,3 Tage“; Modellgrenze 4 (Z. 2019) | S2, Proxy: Blattentfaltung statt Blüte bei der Birke; den Versatz misst #96 §3.1 selbst | `abschaetzung_kap3` |
| 96 | `pollen.p_ar` | Block, Feld `band`: „80–84 und 85+ extrapoliert ueber das DEGS1-Ende 79“; §3.2 (Z. 578) | S2, Extrapolation: Wert der 70- bis 79-Jährigen für die Bänder ab 80 Jahren | `abschaetzung_kap3` |
| 96 | `pollen.c_jahr_direkt` | Register 96-K1-01 (Z. 293): „Raumtransfer Schweden → Deutschland 1:1 dokumentiert“ | S2, Extrapolation: Kosten aus Schweden 18–65 für Deutschland | `abschaetzung_kap3` |
| 98 | `uv.w_scc` | Zeichentabelle (Z. 1082): „altersinvariant, dokumentierte Annahme“; §3.1 (Z. 392) | S2, Extrapolation: ein Anteil für alle Altersbänder | `abschaetzung_kap3` |
| 98 | `uv.i_raten_roh` | Register 98-R35-01 (Z. 275); Modellgrenze 5 (Z. 1497): „Ablesekette der Altersraten (±15 % vor Normierung)“ | S2, Proxy: gepoolte Rohraten 2021–2023 aus der Ablesekette für die Bänder des Modells | `abschaetzung_kap3` |
| 98 | `uv.i_mm` | Block, Feld `quelle`: „Abb. 3.13.2, altersspezifische Rohraten Melanom“ | Ablesewert; nach dem Merkmal keine Setzung, der Zweifel trägt nicht, die Runde an #98 bestätigt den Fall | `quelle` |
| 98 | `uv.i_c44` | Block, Feld `quelle`: „Abb. 3.14.3, altersspezifische Rohraten heller Hautkrebs“ | Ablesewert; nach dem Merkmal keine Setzung, der Zweifel trägt nicht, die Runde an #98 bestätigt den Fall | `quelle` |
| 98 | `uv.or_out` | Block, Feld `kennzeichnung`: „Meta-Analyse Schmitt 2011“ | S2, Extrapolation geprüft: Meta-Analyse mehrerer Länder, deren Geltung die Quelle selbst ausweist; der Zweifel trägt nicht, die Runde an #98 bestätigt den Fall | `quelle` |

Ohne begründeten Zweifel: heat.m_basissterberate (Quotient amtlicher Summen, misst die Sterberate selbst),
heat.hd_ref (Panelbeschreibung bei Karlsson und Ziebarth 2018, misst die Referenzgröße des Studienpanels selbst) und
heat.qbar_1p (Mikrozensus 2023, misst den Anteil Alleinlebender selbst).

### Beispiel-Block

`regel_k`, aus dem Stamm des Produkt-Repos ausführbar (am 07.10.2026 gelaufen, Ausgabe darunter). Er liest die Blöcke
aus Kapitel 7 der drei Berichte und die Tabellen dieser Datei; abgeschrieben wird nichts. Außerhalb der 11 rechnet er
mit der Kennzeichnung des Berichts und liest dort nur das Feld `abgeleitet_aus`.

```python
# regel_k — Regel K an den 11 berechneten Blöcken von #95, #96 und #98, gegen die Tabellen dieser Datei
import re

BERICHTE = {"95": "95_hitzebelastung", "96": "96_aeroallergene", "98": "98_uv_schaedigungen"}
ANZEIGE = {"quelle": "Quelle", "abschaetzung_kap3": "Abschätzung von KAP3",
           "aus_quellen": "berechnet aus Quellen", "mit_abschaetzung": "berechnet, enthält Abschätzung von KAP3"}
BELEGT = ("quelle", "aus_quellen")
TEXT = {nr: open(f"docs/methodik/{d}.md", encoding="utf-8").read() for nr, d in BERICHTE.items()}


def feld(block, name):
    """Wert eines Feldes ohne Kommentar, etwa 'kennzeichnung' → 'berechnet'."""
    m = re.search(r"^\s+" + name + r": ([^#\n]*)", block, re.M)
    return m.group(1).strip() if m else ""


def bloecke(text):
    """Kapitel-7-Blöcke eines Berichts, geschnitten wie im Prüfausdruck: id → Blocktext."""
    teile = [b.split(chr(96) * 3)[0] for b in re.split(r"\nparameter:", text)[1:]]
    return {re.search(r"id: (\S+)", b).group(1): b for b in teile}


B = {nr: bloecke(TEXT[nr]) for nr in BERICHTE}
KZ = {nr: {i: feld(b, "kennzeichnung") for i, b in B[nr].items()} for nr in B}
AUS = {nr: {i: [e.strip() for e in feld(b, "abgeleitet_aus").strip("[]").split(",") if e.strip()]
            for i, b in B[nr].items()} for nr in B}
ELF = [(nr, i) for nr in B for i in B[nr] if KZ[nr][i] == "berechnet"]
assert len(ELF) == 11, ELF

# Tabellen dieser Datei, erkannt an ihrer Kopfzeile
q = open("docs/methodik/querschnitt_kennzeichnung.md", encoding="utf-8").read()


def tabelle(kopf):
    """Datenzeilen der Tabelle, deren Kopfzeile mit kopf beginnt, als Listen von Zellen ohne Backticks."""
    zeilen = q.split("\n" + kopf, 1)[1].split("\n\n")[0].splitlines()[2:]
    return [[c.strip().replace(chr(96), "") for c in z.strip().strip("|").split("|")] for z in zeilen]


TAB = {(z[0], z[1]): z for z in tabelle("| Bericht | Block-ID | Eingänge |")}
F1 = {(z[0], z[1]): z for z in tabelle("| Bericht | Block-ID | Frage 1 |")}
ZW = {z[1]: z for z in tabelle("| Bericht | Block-ID | Fundstelle |")}
ZAEHL = {z[0]: tuple(int(x) for x in z[1:]) for z in tabelle("| Bericht | Blöcke | belegt bisher |")}
assert set(TAB) == set(F1) == set(ELF), set(TAB) ^ set(ELF)

# Frage 1 je Block: Antwort ja oder nein, Beleg wörtlich im Bericht
for (nr, i), z in F1.items():
    assert z[2] in ("ja", "nein") and z[4] in TEXT[nr], (i, z[4])


def klasse(nr, e, soll=None):
    """Anzeigeklasse eines Eingangs: Quellenschlüssel → quelle, einer der 11 → Regel K, sonst Bericht (oder soll)."""
    if e not in B[nr]:
        return "quelle"
    if (nr, e) in F1:
        return regel_k(nr, e, soll)[1]
    return (soll or {}).get(e, KZ[nr][e])


def regel_k(nr, i, soll=None, frage1=None):
    """Regel K für einen der 11 Blöcke → (Kennzeichnung nach der Regel, Anzeigeklasse)."""
    if (frage1 or {}).get(i, F1[(nr, i)][2]) == "ja":      # Frage 1: Setzung im Block selbst
        return "abschaetzung_kap3", "abschaetzung_kap3"
    ids = [e for e in AUS[nr][i] if e in B[nr]]              # Parameter-IDs
    if not ids:                                              # Frage 2: keine Parameter-ID → quelle
        return "quelle", "quelle"
    schwach = any(klasse(nr, e, soll) not in BELEGT for e in ids)   # Frage 3: über alle Stufen
    return "berechnet", "mit_abschaetzung" if schwach else "aus_quellen"


def eingang_text(nr, e):
    """Kennzeichnung eines Eingangs, wie die Spalte „deren Kennzeichnung“ sie schreibt."""
    if e not in B[nr]:
        return "quelle (kein Block)"
    return regel_k(nr, e)[0] if (nr, e) in F1 else KZ[nr][e]


def eingaenge(nr, i):
    """Alle Blöcke, die über abgeleitet_aus in i eingehen, über alle Stufen."""
    s = set()
    for e in AUS[nr][i]:
        if e in B[nr]:
            s |= {e} | eingaenge(nr, e)
    return s


# Zweifel-Liste: deckt mit dem Absatz „Ohne begründeten Zweifel“ genau die 18 quelle-Blöcke außerhalb der 11 ab
QUELLE = sorted(i for nr in B for i in B[nr] if KZ[nr][i] == "quelle")
ohne = q.split("\nOhne begründeten Zweifel:", 1)[1].split("\n\n")[0]
OHNE = {i for i in QUELLE if i in ohne}
assert len(QUELLE) == 18 and not set(ZW) & OHNE and sorted(set(ZW) | OHNE) == QUELLE, sorted(set(QUELLE) ^ set(ZW))
SOLL = {i: z[4] for i, z in ZW.items()}
assert set(SOLL.values()) <= {"quelle", "abschaetzung_kap3"}

# Die 11 Blöcke gegen die Tabelle: Eingänge, deren Kennzeichnung, Regel K, Anzeigetext, letzte Spalte
for nr, i in ELF:
    _, _, ein, ein_kz, soll_kz, soll_text, zweifel = TAB[(nr, i)]
    kz, kl = regel_k(nr, i)
    assert ein.split(" · ") == AUS[nr][i], (i, ein)
    assert ein_kz.split(" · ") == [eingang_text(nr, e) for e in AUS[nr][i]], (i, ein_kz)
    assert (soll_kz, soll_text.strip("„“")) == (kz, ANZEIGE[kl]), (i, soll_kz, soll_text)
    genannt = sorted(re.findall(r"(?:heat|pollen|uv)\.[a-z0-9_]+", zweifel.split(":")[0]))
    assert genannt == sorted(e for e in eingaenge(nr, i) if e in ZW), (i, genannt)
    neu = regel_k(nr, i, soll=SOLL)[1]                       # Anzeige, falls jeder Zweifel zutrifft
    assert ("keine Änderung" if neu == kl else "„" + ANZEIGE[neu] + "“") in zweifel, (i, neu)
    print(f"#{nr} {i:<20} {kz:<18} „{ANZEIGE[kl]}“")

# heat.c_kal ausdrücklich: keine eigene Setzung, zwei abgeschätzte Eingänge, die Setzung bewegt den Fit (Feld band)
c = B["95"]["heat.c_kal"]
assert F1[("95", "heat.c_kal")][2] == "nein"
assert regel_k("95", "heat.c_kal") == ("berechnet", "mit_abschaetzung")
assert TAB[("95", "heat.c_kal")][5].strip("„“") == ANZEIGE["mit_abschaetzung"]
assert [e for e in AUS["95"]["heat.c_kal"] if KZ["95"][e] == "abschaetzung_kap3"] == \
    ["heat.beta_85plus_region", "heat.f_alter"]
assert feld(c, "wert") == "0.581" and "0,559 (s_Sued=1,85)" in c and "0,661 (ohne Sued)" in c
assert (feld(c, "rolle"), feld(c, "quelle")) == ("kalibrierung", "rki_eb19_2025")
assert regel_k("95", "heat.c_kal", soll=SOLL) == regel_k("95", "heat.c_kal")    # Zweifel an t0 und q_w: gleich

# (a) Grenze, benannt an uv.ssd_delta_region und uv.lambda: ohne Parameter-ID nie berechnet
for i in ("uv.ssd_delta_region", "uv.lambda"):
    assert not [e for e in AUS["98"][i] if e in B["98"]], i
assert regel_k("98", "uv.ssd_delta_region") == ("quelle", "quelle")
assert regel_k("98", "uv.lambda") == ("abschaetzung_kap3", "abschaetzung_kap3")
lam = float(re.search(r"mm: ([\d.]+)", feld(B["98"]["uv.lambda"], "wert")).group(1))
assert abs(3081.0 / 26870 - lam) < 5e-6, lam                        # Zahlenbeispiel in Festlegung (a)

# Über zwei Rechenstufen (Rechenkette): heat.beta_pfl → heat.h_heim mit den Zahlen der Blöcke
assert abs(2 / (1 + 0.149 * 2) - float(feld(B["95"]["heat.beta_pfl"], "wert"))) < 5e-3
assert abs(0.149 * (1 + 1.54 * (1 - 0.149)) - float(feld(B["95"]["heat.h_heim"], "wert"))) < 5e-4
assert regel_k("95", "heat.h_heim", frage1={"heat.h_heim": "nein"}) == ("berechnet", "mit_abschaetzung")

# (b) abgeleitet_aus gefüllt, obwohl der Block nicht berechnet ist: alle in Festlegung (b) genannt
gefuellt = sorted(i for nr in B for i in B[nr] if AUS[nr][i]
                  and (regel_k(nr, i)[0] if (nr, i) in F1 else KZ[nr][i]) != "berechnet")
abschnitt_b = q.split("\n### (b)")[1].split("\n### (c)")[0]
assert len(gefuellt) == 12 and all(i in abschnitt_b for i in gefuellt), [i for i in gefuellt if i not in abschnitt_b]
print("abgeleitet_aus gefüllt, nicht berechnet:", gefuellt)

# (d) Zählung belegt: bisher quelle + berechnet; nach der Regel „Quelle“ + „berechnet aus Quellen“,
#     außerhalb der 11 mit der Kennzeichnung des Berichts
zaehl = {nr: (len(B[nr]), sum(KZ[nr][i] in ("quelle", "berechnet") for i in B[nr]),
              sum(klasse(nr, i) in BELEGT for i in B[nr])) for nr in B}
assert zaehl == ZAEHL, (zaehl, ZAEHL)
for nr, (n, a, b) in zaehl.items():
    print(f"#{nr}: {n} Blöcke, belegt bisher {a} / belegt nach der Regel {b}")
print("Zweifel-Liste:", len(ZW), "Blöcke; ohne begründeten Zweifel:", sorted(OHNE))
```

Ausgabe:

```
#95 heat.c_kal           berechnet          „berechnet, enthält Abschätzung von KAP3“
#95 heat.beta_pfl        abschaetzung_kap3  „Abschätzung von KAP3“
#95 heat.h_heim          abschaetzung_kap3  „Abschätzung von KAP3“
#96 pollen.d_saison      abschaetzung_kap3  „Abschätzung von KAP3“
#96 pollen.c_tag         abschaetzung_kap3  „Abschätzung von KAP3“
#98 uv.ssd_delta_region  quelle             „Quelle“
#98 uv.k_uv              abschaetzung_kap3  „Abschätzung von KAP3“
#98 uv.baf               berechnet          „berechnet aus Quellen“
#98 uv.lambda            abschaetzung_kap3  „Abschätzung von KAP3“
#98 uv.l_rest            abschaetzung_kap3  „Abschätzung von KAP3“
#98 uv.c_kal             berechnet          „berechnet aus Quellen“
abgeleitet_aus gefüllt, nicht berechnet: ['heat.beta_iso', 'heat.beta_pfl', 'heat.delta_kuehlzentren', 'heat.delta_vg_morb', 'heat.g_s157', 'heat.h_heim', 'pollen.c_tag', 'pollen.d_saison', 'uv.k_uv', 'uv.l_rest', 'uv.lambda', 'uv.ssd_delta_region']
#95: 31 Blöcke, belegt bisher 13 / belegt nach der Regel 10
#96: 14 Blöcke, belegt bisher 5 / belegt nach der Regel 3
#98: 22 Blöcke, belegt bisher 11 / belegt nach der Regel 8
Zweifel-Liste: 15 Blöcke; ohne begründeten Zweifel: ['heat.hd_ref', 'heat.m_basissterberate', 'heat.qbar_1p']
```

## Rechenkette

Format nach Aufgabe §4, hier „Eingänge → Kennzeichnung“ statt „Zahl × Faktor“, weil Regel K einordnet und nicht
rechnet. Am Ende steht kein Euro-Betrag, sondern der Anzeigetext in der Parameterliste. Beispiel: heat.c_kal aus
Bericht 95, der Kalibrierskalar der Sterbefälle durch Hitze. Jede Ebene ist ein Block; die letzte Spalte ist genau
der Text, den die Parameterliste zeigt. Die Ebenen 1 bis 5 liegen außerhalb der 11; ihre Kennzeichnung ist die des
Berichts.

| Ebene | Block | Eingänge | Kennzeichnung der Eingänge | Kennzeichnung nach der Regel | Anzeigetext |
|---|---|---|---|---|---|
| 1 | heat.t0_region: Temperatur, ab der die Sterblichkeit steigt, je Region | keine; Ablesewerte Winklmayr 2022, Abb. 3 | – | `quelle` (Kennzeichnung des Berichts; steht in der Zweifel-Liste) | „Quelle“ |
| 2 | heat.beta_85plus_region: Anstieg der Sterblichkeit je Grad, ab 85 Jahren | keine; Nord und Mitte abgelesen, Süd von KAP3 nachgeschätzt (s_Süd = 1,65) | – | `abschaetzung_kap3` (Kennzeichnung des Berichts) | „Abschätzung von KAP3“ |
| 3 | heat.f_alter: Faktor je Altersband | keine; aus RKI-Anteilen zurückgerechnet, mit linearer Näherung | – | `abschaetzung_kap3` (Kennzeichnung des Berichts) | „Abschätzung von KAP3“ |
| 4 | heat.m_basissterberate: Sterbefälle 2023 ÷ Bevölkerung, je Altersband | keine; Quotient amtlicher Summen, misst die Sterberate selbst | – | `quelle` (Kennzeichnung des Berichts) | „Quelle“ |
| 5 | heat.q_wochenquantile: Temperaturquantile je Woche | keine; aus DWD-Tageswerten ausgezählt | – | `quelle` (Kennzeichnung des Berichts; steht in der Zweifel-Liste) | „Quelle“ |
| 6 | heat.c_kal = 0,581: Fit des Modells aus Ebene 1–5 an die hitzebedingten Sterbefälle des RKI 2012–2024 | Ebene 1–5 (Parameter-IDs); dazu die Zielreihe `rki_eb19_2025` im Feld `quelle:`, kein Block | `quelle` · `abschaetzung_kap3` · `abschaetzung_kap3` · `quelle` · `quelle`; Zielreihe zählt als `quelle` (Festlegung, c) | `berechnet` (Frage 1: keine eigene Setzung; Frage 2: fünf Parameter-IDs; Frage 3: schwächster Eingang Ebene 2 und 3) | „berechnet, enthält Abschätzung von KAP3“ |

**Zweifel an Ebene 1 und 5 (kein Eintrag der Parameterliste).** heat.t0_region und heat.q_wochenquantile stehen in
der Zweifel-Liste. Die Anzeige von c_kal ändert sich dadurch nicht, weil c_kal über Ebene 2 (β85+) und Ebene 3 (f_a)
ohnehin eine Abschätzung von KAP3 enthält.

**Gegenprobe (kein Eintrag der Parameterliste).** Dass die Setzung aus Ebene 2 im Wert von heat.c_kal steckt, zeigt
das Band des Blocks: Mit s_Süd = 1,85 statt 1,65 ergibt der Fit 0,559 statt 0,581, ohne die Region Süd 0,661.

**Zählung (kein Eintrag der Parameterliste).** In der Quellenlage von #95 zählt heat.c_kal nach Regel K als
abgeschätzt, ebenso heat.beta_pfl und heat.h_heim. Belegt sind damit 10 statt 13 der 31 Blöcke in Kapitel 7
(Festlegung, d).

**Nacherzählt.** c_kal ist die Zahl, mit der KAP3 das Hitzemodell so einstellt, dass es die Sterbefälle des RKI der
Jahre 2012–2024 trifft. Das Modell besteht aus fünf Bausteinen. Drei stammen laut Bericht aus Quellen. Zwei hat KAP3
selbst abgeschätzt: den Anstieg der Sterblichkeit im Süden und den Faktor je Altersband. Weil c_kal genau das
ausgleicht, was diese beiden Bausteine verschieben, steckt ihre Abschätzung in c_kal. Ändert man die Abschätzung im
Süden, wird aus 0,581 eine 0,559. Deshalb zeigt die Parameterliste „berechnet, enthält Abschätzung von KAP3“ und zählt
c_kal nicht als belegt. Den Ausschlag geben Ebene 2 und 3; ein einziger abgeschätzter Eingang hätte genügt.

**Über zwei Rechenstufen: heat.beta_pfl → heat.h_heim (Bericht 95).** Stufe 1: β_pfl = (3,0 − 1) ÷ [1 + 0,149 ×
(3,0 − 1)] = 2 ÷ 1,298 = 1,54, mit der Heimquote 0,149 aus der Pflegestatistik und dem
Odds-Verhältnis 3,0, das KAP3 nach #95 §3.3b selbst bildet: Exzess-Verhältnis 1,0 aus Frankreich 2003 (Fouillet) ×
Basissterblichkeits-Verhältnis 2,97 (WIdO, m_85+ und Heimquote) ≈ 3,0. Stufe 2: h_heim = 0,149 × [1 + 1,54 × (1 − 0,149)] = 0,149 × 2,31 = 0,344. β_pfl überträgt
einen Wert aus Frankreich nach Deutschland und zeigt nach Frage 1 „Abschätzung von KAP3“. Hätte h_heim selbst keine
Setzung, zeigte die Liste trotzdem „berechnet, enthält Abschätzung von KAP3“, weil Frage 3 die Setzung aus Stufe 1
über Stufe 2 weiterreicht; tatsächlich trägt h_heim mit dem Zellwert einen eigenen Proxy und zeigt „Abschätzung von
KAP3“. So wird eine Setzung auch über eine Rechnung weitergereicht nie als Quelle gezeigt. In M0 hat nach den
Entscheidungen zu Frage 1 kein berechneter Block mehr einen berechneten Eingang; die zweite Stufe wirkt deshalb hier
nur als Gegenprobe (Beispiel-Block).

**Frage 1 an einem Block ohne Parameter-ID: uv.lambda (Bericht 98).** Beim Melanom ergibt 3.081,0 Sterbefälle ÷
26.870 Neuerkrankungen (ZfKD, Mittel 2021–2023) den Wert 0,11466. Beide Zahlen stehen in der Quelle. Das Modell
braucht aber den Anteil der Erkrankten, die am Melanom sterben, und den trifft der Quotient eines Zeitfensters nur
näherungsweise; der Bericht nennt die Richtung selbst: „Überschätzung des Mortalitätsanteils“. Dass diese Näherung
gelten soll, entscheidet KAP3. Deshalb zeigt die Parameterliste „Abschätzung von KAP3“, mit der Herleitung aus den
beiden ZfKD-Zahlen. Zum Vergleich heat.m_basissterberate: Sterbefälle 2023 ÷ Bevölkerung ist genau die Sterberate,
die das Hitzemodell braucht, und die Liste zeigt „Quelle“.

**Was die einfachere Regel verfälschen würde (§8 E3).** Liest man `berechnet` wie heute als belegt und übernimmt die
Kennzeichnung der Berichte, zählen heat.c_kal, heat.beta_pfl, heat.h_heim, pollen.d_saison, pollen.c_tag, uv.k_uv,
uv.lambda und uv.l_rest als belegt: #95 käme auf 13 statt 10 belegte Blöcke von 31, #96 auf 5 statt 3 von 14, #98 auf
11 statt 8 von 22, und die Liste zeigte acht Werte mit Setzung als belegt. Schreibt man stattdessen schlicht
„Abschätzung von KAP3“, verliert die Anzeige, dass c_kal ein Fit an die RKI-Reihe ist und drei seiner fünf Eingänge
aus Quellen stammen.

## Übernahmeliste an den CTO

Schritt 2 (Ticket T-1835-methodik_manager). Termin für die Umsetzung im Produkt: **23.10.2026**. Jede Zeile nennt
den Sollzustand nach Regel K (Abschnitt „Festlegung“); der heutige Stand steht nur zur Orientierung in der Spalte
„heute“ und ist nie Vorgabe. Die Umsetzung vergibt der CEO an den CTO; dieses Paket ändert keinen Code. Zeilen nach dem
Stand vom 07.10.2026.

**Durchgehendes Beispiel: heat.c_kal = 0,581 (Bericht 95).** Eingänge heat.t0_region, heat.m_basissterberate,
heat.q_wochenquantile (`quelle`), heat.beta_85plus_region und heat.f_alter (`abschaetzung_kap3`). Sollzustand: Klasse
`berechnet`, Anzeigetext „berechnet, enthält Abschätzung von KAP3“, darunter die fünf Eingänge mit ihrem Anzeigetext
(dreimal „Quelle“, zweimal „Abschätzung von KAP3“); in der Zählung abgeschätzt. Gegenbeispiel uv.c_kal (Bericht 98):
einziger Parameter-Eingang uv.i_raten_roh (`quelle`), Anzeigetext „berechnet aus Quellen“, in der Zählung belegt.

| Stelle im Produkt | heute | Sollzustand nach Regel K | Beispiel |
|---|---|---|---|
| Kennzeichnung der 11 Parameter in der Registry: `backend/app/services/parameter_registry.py` übernimmt die Klasse aus `_HEAT_KLASSE` und `_UV_KLASSE` in `backend/app/services/engine/impact/params.py` (Z. 1702 ff., 1941 ff.), `_POLLEN_KLASSE` (ebenda) und `cost_evidence_class` in `backend/app/data/catalog.py` (Z. 281) | alle 11 `berechnet` (uv.ssd_delta_region ohne eigene Stelle, Ebene UV_RADIATION) | Klasse je Block nach der Spalte „Kennzeichnung nach der Regel“ der Tabelle der 11, übersetzt wie bisher (`quelle` → `belegt`, `abschaetzung_kap3` → `abgeschaetzt`, `berechnet` → `berechnet`): `abgeschaetzt` für heat.beta_pfl, heat.h_heim, pollen.d_saison, pollen.c_tag, uv.k_uv, uv.lambda, uv.l_rest, je mit Herleitung als Datenfeld `evidence_derivation`, die die Setzung nach Frage 1 nennt (P1); `berechnet` für heat.c_kal, uv.baf, uv.c_kal; uv.ssd_delta_region `belegt`, sobald er eine Stelle in der Registry bekommt, bis dahin ändert sich an der Parameterliste nichts, weil er dort nicht erscheint. Jeder `berechnet`-Parameter führt zusätzlich seine Parameter-Eingänge (`abgeleitet_aus` des Blocks, nur Parameter-IDs) und ein daraus über alle Stufen gerechnetes Merkmal `enthaelt_abschaetzung` (wahr, sobald ein Eingang `abgeschaetzt` ist oder selbst `enthaelt_abschaetzung` trägt). `EVIDENCE_CLASSES` bleibt bei drei Werten (Festlegung: die drei Werte aus §4 bleiben). | heat.beta_pfl: `abgeschaetzt`, Herleitung „Exzess-Verhältnis aus Frankreich 2003 für Deutschland übertragen (S2, Extrapolation)“; heat.c_kal: `berechnet`, `enthaelt_abschaetzung` wahr; uv.baf: `berechnet`, `enthaelt_abschaetzung` falsch |
| `BELEGTE_KLASSEN` (`parameter_registry.py`, Z. 102) | `frozenset({"belegt", "berechnet"})`: jeder berechnete Parameter zählt als belegt | Eine Menge von Klassen kann Regel K nicht ausdrücken, weil `berechnet` je nach Eingängen belegt oder abgeschätzt zählt. Soll: eine Prüfung je Parameter, „zählt als belegt“ = Klasse `belegt`, oder Klasse `berechnet` und `enthaelt_abschaetzung` falsch. Alle Aufrufer (`gewissheit.py`, `unsicherheits_zusammenschau.py`) nutzen diese Prüfung statt der Menge. | heat.c_kal zählt abgeschätzt, uv.c_kal belegt |
| Gewissheitsstufe (`backend/app/services/gewissheit.py`, Z. 86, `gewissheitsstufe`) | Stufe aus dem Anteil der Parameter in `BELEGTE_KLASSEN` | Die Stufe selbst folgt Regel G ([querschnitt_gewissheit.md](querschnitt_gewissheit.md)): Stufe der KWRA, nicht aus Parametern; daran ändert Regel K nichts. Die Zählung „x von y Parametern mit Quelle“ (Quellenlage, nur zum Vergleich) zählt nach der Prüfung „zählt als belegt“. Solange der Code die Stufe noch aus dem Anteil bildet, nutzt auch dieser Anteil die neue Prüfung, damit keine Setzung als belegt eingeht. | Kapitel 7 von #95: 10 statt 13 von 31 Blöcken belegt (Festlegung, d) |
| Unsicherheits-Zusammenschau (`backend/app/services/unsicherheits_zusammenschau.py`, Z. 99) | führt einen Parameter als nicht belegt, wenn seine Klasse weder `belegt` noch `berechnet` ist | Nicht belegt ist jeder Parameter, der die Prüfung „zählt als belegt“ nicht besteht. Damit erscheinen die acht Werte heat.c_kal, heat.beta_pfl, heat.h_heim, pollen.d_saison, pollen.c_tag, uv.k_uv, uv.lambda, uv.l_rest als nicht belegt; uv.baf und uv.c_kal bleiben belegt. | heat.c_kal steht unter den nicht belegten Werten |
| Anzeigetext in der Oberfläche: `frontend/src/utils/evidenceLabel.ts` (Z. 6), `frontend/src/components/ParameterTable.tsx` (Z. 47–62), dazu Excel (`backend/app/services/export_service.py`, Z. 110) und PDF (`backend/app/services/ergebnisbericht/teile.py`, Z. 67) | drei Texte je Klasse: „belegt“, „abgeschätzt (KAP3)“, „berechnet aus anderen Parametern“ (ein Text für alle berechneten Parameter); Überschrift der Herleitung „Berechnet aus anderen Parametern — Herleitung“ | vier Anzeigetexte nach Regel K: „Quelle“ (Klasse `belegt`), „Abschätzung von KAP3“ (Klasse `abgeschaetzt`), „berechnet aus Quellen“ (`berechnet`, `enthaelt_abschaetzung` falsch), „berechnet, enthält Abschätzung von KAP3“ (`berechnet`, `enthaelt_abschaetzung` wahr). Damit ändern sich auch die beiden heutigen Texte „belegt“ und „abgeschätzt (KAP3)“, und zwar für alle Parameter, nicht nur für die 11. Neben einem berechneten Parameter stehen seine Eingänge mit deren Anzeigetext. Die Überschrift der Herleitung nennt den Anzeigetext des Parameters. Oberfläche und Excel zeigen denselben Text. Das PDF ebenso; die bisherige Ausnahme der Gliederung (Teil 7: „ausgewiesene Abschätzung von KAP3“) enthält den Text der Regel und kann bleiben. Der Typ `EvidenceClass` (`frontend/src/types/index.ts`) bleibt bei drei Werten; das Merkmal `enthaelt_abschaetzung` und die Eingänge kommen als eigene Felder dazu. | heat.c_kal: „berechnet, enthält Abschätzung von KAP3“, darunter heat.beta_85plus_region „Abschätzung von KAP3“ … heat.m_basissterberate „Quelle“ |
| `backend/tests/test_evidence_class_berechnet.py`, Teil (a) (Z. 42–49) | `test_evidence_classes_fuehrt_drei_klassen` (Z. 44) prüft die drei Klassen; `test_belegte_klassen_sind_belegt_und_berechnet` (Z. 48) schreibt `BELEGTE_KLASSEN == {"belegt", "berechnet"}` fest | Z. 44 bleibt: Die drei Klassen ändern sich nicht (Festlegung). Z. 48 entfällt mit der Menge `BELEGTE_KLASSEN`. An seine Stelle tritt ein Test der Prüfung „zählt als belegt“: `belegt` ja, `abgeschaetzt` nein, `berechnet` nur mit `enthaelt_abschaetzung` falsch. | `berechnet` mit `enthaelt_abschaetzung` wahr (wie heat.c_kal): zählt nicht als belegt |
| `backend/tests/test_evidence_class_berechnet.py`, Teil (c) (Z. 76–134) | schreibt fest, dass `berechnet` wie `belegt` zählt (`test_gewissheit_zaehlt_berechnet_wie_belegt`, Z. 99; `test_alle_berechnet_ergibt_hoch`, Z. 106; `test_zusammenschau_zaehlt_berechnet_nicht_als_unbelegt`, Z. 111); `test_katalog_heute_unveraendert` (Z. 127) sagt im Docstring, kein Registry-Parameter trage `berechnet` | Teil (c) prüft Regel K: Ein berechneter Parameter ohne abgeschätzten Eingang zählt wie belegt; einer mit abgeschätztem Eingang zählt wie abgeschätzt, auch über zwei Stufen, in der Quellenlage zur Gewissheit und in der Zusammenschau. `test_alle_berechnet_ergibt_hoch` gilt nur noch für berechnete Parameter ohne abgeschätzten Eingang, solange die Stufe noch aus dem Anteil gebildet wird. In `test_katalog_heute_unveraendert` bleibt die Prüfung (jede Klasse gültig); der Docstring wird berichtigt, weil heute elf Blöcke `berechnet` tragen. | Fall „`berechnet` mit Eingang `abgeschaetzt`, dazu `belegt`“ zählt wie `["abgeschaetzt", "belegt"]`; Zweistufen-Fall wie heat.beta_pfl → heat.h_heim |
| `backend/tests/test_evidence_class_berechnet.py`, Teile (b), (d), (e) und (f) | (b) Registry übernimmt `berechnet`; (d) Maßnahmen-Gewissheit gibt `berechnet` durch; (e) Typ und Anzeige im Frontend (Z. 146–159); (f) gleicher Text in Oberfläche, Excel und PDF (Z. 164–189) | (b) und (d) ändern sich nicht: Die Klasse `berechnet` bleibt, und keine Maßnahme im Katalog trägt sie als Wirkungsklasse. Einzige Fundstelle in `catalog.py` ist Z. 281, der Kostensatz pollen.c_tag am Risiko, und der steht schon in der Zeile zur Registry. (e) prüft die vier Anzeigetexte und die neue Überschrift statt „berechnet aus anderen Parametern“. (f) vergleicht die Texte je Anzeige statt je Klasse, weil `berechnet` zwei Texte hat, mit derselben Ausnahme im PDF. | (e): `evidenceLabel.ts` liefert für heat.c_kal „berechnet, enthält Abschätzung von KAP3“ |
| `backend/tests/test_methodik_95_kennzeichnung.py` | erwartet in Kapitel 7 und Registry 10 × belegt, 18 × abgeschätzt, 3 × berechnet und je Parameter die Klasse seines Blocks | Erwartet für die drei Blöcke unter den 11 die Klasse nach Regel K, gelesen aus der Tabelle der 11 dieser Datei: 10 × belegt, 20 × abgeschätzt, 1 × berechnet (heat.c_kal, `enthaelt_abschaetzung` wahr). Ändert die Runde an #95 Kapitel 7 entsprechend, liest der Test wieder nur den Bericht. | heat.h_heim: `abgeschaetzt` |
| `backend/tests/test_methodik_96_kennzeichnung.py` | erwartet 3 × belegt, 9 × abgeschätzt, 2 × berechnet; `c_tag["evidence_class"] == "berechnet"` (Z. 123), `d["evidence_class"] == "berechnet"` (Z. 166) | Erwartet 3 × belegt, 11 × abgeschätzt, 0 × berechnet; pollen.c_tag und pollen.d_saison `abgeschaetzt` mit Herleitung (Z. 123 und 166 entsprechend). Werte bleiben (43,05 und 266,90 ÷ 43,05). | pollen.d_saison: `abgeschaetzt`, Wert 43,05 |
| `backend/tests/test_methodik_98_kennzeichnung.py` | **Vermerk:** Am 06.10.2026, als das Paket geschnitten wurde, fehlte die Datei; es gab nur die Tests für #95 und #96. Seit 07.10.2026 ist sie angelegt (Commit ee83c67b, T-1820-cto) und prüft die Klasse je Block gegen Kapitel 7 (`test_klasse_in_der_parameterliste_folgt_der_kennzeichnung`, Z. 134). | Erwartet für die sechs Blöcke unter den 11 die Klasse nach Regel K: `abgeschaetzt` für uv.k_uv, uv.lambda, uv.l_rest (mit Herleitung, `test_abgeschaetzte_bloecke_tragen_herleitung`), `berechnet` mit `enthaelt_abschaetzung` falsch für uv.baf und uv.c_kal; uv.ssd_delta_region bleibt ohne eigene Stelle (`test_bloecke_ohne_eigene_stelle_bleiben_abweichung`), Soll-Kennzeichnung `quelle`. | uv.lambda: `abgeschaetzt`, Herleitung „Periodenquotient 3.081,0 ÷ 26.870 = 0,11466 für den Letalitätsanteil (S2, Proxy)“ |

**Was sich nicht ändert.** Werte, Bänder und Rechenwege der 11 Parameter bleiben; Regel K ändert nur Kennzeichnung,
Anzeigetext und Zählung. Die Blöcke außerhalb der 11 behalten im Produkt die Klasse ihres Berichts, auch die der
Zweifel-Liste, bis die Runde am Bericht entscheidet. Die Gewissheitsstufe nach Regel G bleibt.

**Reihenfolge.** Der Code kann vor den Berichten umgestellt werden, weil die Tests für die 11 Blöcke aus dieser Datei
lesen. Ändert eine Runde Kapitel 7 eines Berichts nach den Befunden unten, laufen Bericht und Code wieder gleich; eine
Abweichung dazwischen ist ein Befund im Ledger, kein stiller Fix (CLAUDE.md, eiserne Regel 5).

## Befunde an Berichte

Je Bericht (a) jede `kennzeichnung:`-Zeile der 11 Blöcke und jede Textstelle, die Regel K widerspricht, mit Fundstelle
und Sollzustand, und (b) die Blöcke dieses Berichts aus der Zweifel-Liste. Die Berichte ändert dieses Paket nicht; jede
Änderung ist eine eigene Runde am Bericht, mit Eintrag im Ledger `reviews/BEFUNDE_<nr>.md`. Zeilen nach dem Stand vom
07.10.2026.

### #95 Hitzebelastung

**(a) Widersprüche zu Regel K**

| Fundstelle | Block-ID | heute | Sollzustand |
|---|---|---|---|
| Kap. 7, Z. 1611, `kennzeichnung:` | heat.c_kal | `berechnet` | bleibt `berechnet`; kein Widerspruch (Anzeigetext „berechnet, enthält Abschätzung von KAP3“) |
| Kap. 7, Z. 1684, `kennzeichnung:` | heat.beta_pfl | `berechnet` | `abschaetzung_kap3` (Frage 1, S2 Extrapolation: Exzess-Verhältnis Frankreich 2003 für Deutschland); `abgeleitet_aus` leeren oder die Abweichung von §4 begründen (Festlegung, b) |
| Kap. 7, Z. 1841, `kennzeichnung:` | heat.h_heim | `berechnet` | `abschaetzung_kap3` (Frage 1, S2 Proxy: Zellwert aus OSM-Pflegeeinrichtungen); `abgeleitet_aus` leeren oder begründen |
| Zeichentabelle §3.6, Zeile \(h_{\text{Heim}}\) (Z. 819) | heat.h_heim | „berechnet, Block `heat.h_heim` [61]“ | „Abschätzung von KAP3, Block `heat.h_heim` [61]“ (Frage 1, S2 Proxy: Zellwert). In dieser Zeile ist „berechnet“ eine Kennzeichnung, weil es neben dem Block steht. Die übrigen „berechnet“ in der Zeichentabelle §3.6 (Z. 814, 834, 836, 848–850) und in der Tabelle von §3.1 (Z. 362) gehören zu Größen ohne eigenen Block und heißen dort nur „im Modell gerechnet“; sie sind kein Befund |
| Kap. 7, Absatz „Kennzeichnung `berechnet`“, Z. 1506–1514 | heat.beta_pfl | „Das gilt für \(c_{\text{kal}}\) (…) und für \(\beta_{\text{pfl}}\) (Kette §3.3b aus \(m_{85+}\) und \(\bar q_{\text{pfl}}\))“ (Z. 1507–1508) und „\(\beta_{\text{pfl}}\) stützt sich auf \(m_{85+}\) und \(\bar q_{\text{pfl}}\), beide `quelle`, und zählt wie belegt“ (Z. 1512–1513) | β_pfl ist `abschaetzung_kap3` und zählt als abgeschätzt, weil er selbst eine Setzung trägt; „berechnet“ gilt in #95 nur für c_kal |
| Entscheidungslog, Log 40 (Z. 2444), Spalte Entscheidung | heat.beta_pfl | „**`berechnet`** nur, wo der Wert aus anderen Blöcken folgt (\(c_{\text{kal}}\), \(\beta_{\text{pfl}}\))“ | Beispiel für `berechnet` nur c_kal; β_pfl als `abschaetzung_kap3` (Frage 1, S2 Extrapolation). Der Log-Eintrag wird in der Runde fortgeschrieben, mit Verweis auf diese Datei |
| ebenda | alle berechneten | „Im Produkt lautet der Anzeigetext ‚berechnet aus anderen Parametern‘“; „Ob diese Regel für alle Klimawirkungen gilt, wird risikoübergreifend festgelegt.“ | Anzeigetext nach Regel K („berechnet aus Quellen“ oder „berechnet, enthält Abschätzung von KAP3“); Verweis auf diese Datei als die risikoübergreifende Festlegung |
| ebenda, zum Satz aus dem Ticket „bis dahin zählt das Produkt `berechnet` wie ‚belegt‘“ | alle berechneten | Der Satz steht in der Fassung vom 07.10.2026 nicht mehr wörtlich in §7 (gesucht nach „bis dahin zählt“ und „wie ‚belegt‘“, Absatz Z. 1506–1514 ganz gelesen). Seinen Inhalt trägt dort der Halbsatz „zählt wie belegt“ zu β_pfl. | Beurteilt: Die Aussage widerspricht Regel K. Soll: Ein berechneter Wert zählt nur dann als belegt, wenn kein Eingang über alle Stufen eine Abschätzung von KAP3 trägt (Festlegung, d); steht der Satz in einer anderen Fassung, wird er so ersetzt |
| Kap. 7, `abgeleitet_aus` bei heat.g_s157, heat.delta_vg_morb, heat.delta_kuehlzentren (`abschaetzung_kap3`) | heat.g_s157 · heat.delta_vg_morb · heat.delta_kuehlzentren | Feld gefüllt, obwohl der Block nicht `berechnet` ist | Feld leeren oder die Abweichung von §4 im Bericht begründen (Festlegung, b) |

Übereinstimmend und ohne Befund sind nur zwei Aussagen: in Log 40 der Prüfstein selbst („Misst der Wert die Zielgröße
selbst, ist die bloße Wahl zwischen Quellenwerten keine Setzung (…)“, Grundlage von Frage 1) und im Absatz Z. 1506–1514
die Aussage, dass c_kal über β85+ und f_a wie eine Abschätzung zählt. Das Beispiel β_pfl in Log 40 ist ein Befund
(Tabelle oben), ebenso β_iso als `quelle` in Log 40 (Zweifel, Teil b).

**(b) Zweifel aus der Liste.** Die nächste Runde an #95 entscheidet je Block; bis dahin gilt die Kennzeichnung des
Berichts.

| Block-ID | Fundstelle | Form nach dem Merkmal | Sollzustand nach dem Merkmal |
|---|---|---|---|
| heat.t0_region | Register 95-E02-01 (Z. 150); Modellgrenze 3 (Z. 1470) | S2, Proxy: Schwelle der Region für jede Zelle | `abschaetzung_kap3` |
| heat.q_wochenquantile | Modellgrenze 1 (Z. 1461) | S2, Punkt statt Bandmittel | `abschaetzung_kap3` |
| heat.e_hd | Register 95-E02-02 (Z. 151); §3.4 (Z. 684–686) | S2, Extrapolation über Altersbänder | `abschaetzung_kap3` |
| heat.beta_iso | Register 95-S152-02 (Z. 155); Zeichentabelle (Z. 842); §7 Z. 1508–1509 („ist deshalb `quelle`“); Log 40 (Z. 2444, „eine nur umgerechnete Studienzahl ist `quelle`“) | S2, Extrapolation Chicago 1995 → Deutschland | `abschaetzung_kap3`, `abgeleitet_aus` dann nach Festlegung (b) |
| heat.qbar_pfl | Register 95-S153-01 (Z. 156) | S2, Proxy: Zellwert aus OSM | `abschaetzung_kap3` |
| heat.gamma_hoehe | Kap. 7 (Z. 1741); Register 95-W124-01 (Z. 152) | S2, Proxy: Gradient der Standardatmosphäre | `abschaetzung_kap3` |
| heat.ror_s157 | Register 95-S157-01 (Z. 163) | S2, Extrapolation Ontario → deutsche Heime | `abschaetzung_kap3` |

### #96 Aeroallergene

**(a) Widersprüche zu Regel K**

| Fundstelle | Block-ID | heute | Sollzustand |
|---|---|---|---|
| Kap. 7, Z. 2264, `kennzeichnung:` | pollen.d_saison | `berechnet` | `abschaetzung_kap3` (Frage 1, S2 vereinfachte Form: additive Form zählt Doppelt-Sensibilisierte doppelt); `abgeleitet_aus` leeren oder begründen (Festlegung, b) |
| Kap. 7, Z. 2276, `kennzeichnung:` | pollen.c_tag | `berechnet` | `abschaetzung_kap3` (Frage 1, S2 Proxy: Durchschnitts-Kostensatz, §3.5 „Proxy-Kennzeichnung“, Modellgrenze 6); `abgeleitet_aus` leeren oder begründen |
| Log 25 (Z. 2637), Spalte Entscheidung | pollen.d_saison · pollen.c_tag | „`berechnet` für \(d_{\text{Saison}}\) (aus f, p_sens, L) und \(c_{\text{Tag}}\) (aus c_jahr, d_Saison)“ | beide `abschaetzung_kap3`; der Log-Eintrag wird in der Runde fortgeschrieben, mit Verweis auf diese Datei |

Ohne Befund: Die Zeichentabelle führt pollen.d_saison und pollen.c_tag ohne Kennzeichnung (Z. 927–928). Die „berechnet“
in Z. 925, 929 und 944 gehören zu Größen ohne eigenen Block.

**(b) Zweifel aus der Liste.** Die nächste Runde an #96 entscheidet je Block; bis dahin gilt die Kennzeichnung des
Berichts.

| Block-ID | Fundstelle | Form nach dem Merkmal | Sollzustand nach dem Merkmal |
|---|---|---|---|
| pollen.delta_s_region | Kap. 7, Feld `band`; Modellgrenze 4 (Z. 2019) | S2, Proxy: Blattentfaltung statt Blüte bei der Birke | `abschaetzung_kap3` |
| pollen.p_ar | Kap. 7, Feld `band`; §3.2 (Z. 578); Log 25 (Z. 2637, „die Extrapolation ist am Band gekennzeichnet“) | S2, Extrapolation auf die Bänder ab 80 Jahren | `abschaetzung_kap3` |
| pollen.c_jahr_direkt | Register 96-K1-01 (Z. 293) | S2, Extrapolation Schweden → Deutschland | `abschaetzung_kap3` |

### #98 UV-Schädigungen

**(a) Widersprüche zu Regel K**

| Fundstelle | Block-ID | heute | Sollzustand |
|---|---|---|---|
| Kap. 7, Z. 1626, `kennzeichnung:` | uv.ssd_delta_region | `berechnet` | `quelle` (Frage 2: keine Parameter-ID; misst die Zielgröße selbst); `abgeleitet_aus` leeren oder begründen (Festlegung, b) |
| Kap. 7, Z. 1657, `kennzeichnung:` | uv.k_uv | `berechnet` | `abschaetzung_kap3` (Frage 1, S2 Extrapolation, Modellgrenze 2 und 9); `abgeleitet_aus` leeren oder begründen |
| Kap. 7, Z. 1681, `kennzeichnung:` | uv.baf | `berechnet` | bleibt `berechnet`; kein Widerspruch (Anzeigetext „berechnet aus Quellen“) |
| Kap. 7, Z. 1722, `kennzeichnung:` | uv.lambda | `berechnet` | `abschaetzung_kap3` (Frage 1, S2 Proxy: Periodenquotient für den Letalitätsanteil); `abgeleitet_aus` leeren oder begründen |
| Kap. 7, Z. 1738, `kennzeichnung:` | uv.l_rest | `berechnet` | `abschaetzung_kap3` (Frage 1, S2 Punkt statt Bandmittel: medianes Sterbealter); `abgeleitet_aus` leeren oder begründen |
| Kap. 7, Z. 1777, `kennzeichnung:` | uv.c_kal | `berechnet` | bleibt `berechnet`; kein Widerspruch (Anzeigetext „berechnet aus Quellen“) |
| Log 36 (Z. 2212), Spalte Entscheidung | uv.ssd_delta_region · uv.k_uv · uv.lambda · uv.l_rest | „schwächste Herkunft im Block“, `berechnet` für ΔSSD als eigene Auswertung amtlicher Daten, für \(k_{\text{UV}}\), λ und \(\bar L\) | Beurteilt: widerspricht Regel K in der Grenze zu `berechnet` (Festlegung, a). Soll: `berechnet` nur mit Parameter-ID; eigene Auswertung ohne Näherung = `quelle` (ΔSSD), mit benannter Näherung = `abschaetzung_kap3` (k_UV, λ, \(\bar L\)) |
| Log 36 (Z. 2212), Begründung der „Abweichung von Aufgabe §4“ für sechs Blöcke | uv.ssd_delta_region · uv.k_uv · uv.lambda · uv.l_rest | Quellenschlüssel in `abgeleitet_aus`, weil die Blöcke `berechnet` seien | Für diese vier trägt die Begründung nicht mehr: Feld leeren oder die Abweichung neu begründen. Für uv.baf und uv.c_kal bleibt sie tragfähig, der Quellenschlüssel zählt als `quelle` (Festlegung, b) |

Ohne Befund: Die Zeichentabelle führt die Größen der 11 Blöcke ohne Kennzeichnung (Z. 1057, 1059, 1067–1069). Die
„berechnet“ in Z. 1060, 1061, 1063, 1075, 1083 und 1086 gehören zu Größen ohne eigenen Block. Im Register steht „berechnet“
bei 98-E20-02 (Z. 272) in der Spalte „Datenlage je Zelle“; dort heißt es „je Gemeindepunkt gerechnet“ und ist keine
Kennzeichnung.

**(b) Zweifel aus der Liste.** Die nächste Runde an #98 entscheidet je Block; bis dahin gilt die Kennzeichnung des
Berichts.

| Block-ID | Fundstelle | Form nach dem Merkmal | Sollzustand nach dem Merkmal |
|---|---|---|---|
| uv.w_scc | Zeichentabelle (Z. 1082); §3.1 (Z. 392) | S2, Extrapolation über Altersbänder | `abschaetzung_kap3`; dann zeigt uv.baf „berechnet, enthält Abschätzung von KAP3“ |
| uv.i_raten_roh | Register 98-R35-01 (Z. 275); Modellgrenze 5 (Z. 1497) | S2, Proxy: gepoolte Rohraten aus der Ablesekette | `abschaetzung_kap3`; dann zeigt uv.c_kal „berechnet, enthält Abschätzung von KAP3“ |
| uv.i_mm | Kap. 7, Feld `quelle` (Abb. 3.13.2) | Ablesewert, keine Setzung | `quelle`; die Runde bestätigt den Fall |
| uv.i_c44 | Kap. 7, Feld `quelle` (Abb. 3.14.3) | Ablesewert, keine Setzung | `quelle`; die Runde bestätigt den Fall |
| uv.or_out | Kap. 7, Feld `kennzeichnung` (Meta-Analyse Schmitt 2011) | Geltung weist die Quelle selbst aus | `quelle`; die Runde bestätigt den Fall |

## Entscheidungslog

**Gewählt:** Ansatz B, die Vererbung der schwächsten Kennzeichnung über alle Stufen, angezeigt als Verbindung, mit
der Grenze zwischen `quelle` und `berechnet` aus Aufgabe §4 und dem Prüfstein aus #95 Log 40 als Frage 1, angewendet
auf die 11 berechneten Blöcke. Verworfen, je in einem Satz:

- **Ansatz A** (`berechnet` als neutrale Klasse wie heute, gelesen wie belegt): Er zeigt heat.c_kal, pollen.d_saison
  und pollen.c_tag als belegt, obwohl in ihnen Setzungen von KAP3 stecken, und verletzt damit den Prüfstein aus P1.
- **Ansatz C** (ein berechneter Wert mit abgeschätztem Eingang heißt schlicht `abschaetzung_kap3`): Er hält den
  Prüfstein ein, verliert in der Anzeige aber, dass der Wert aus anderen Parametern folgt und welche davon belegt
  sind, also die Herleitung, die P1 verlangt.
- **Ansatz D** (Urteil je Block ohne feste Regel): Er ließ die Berichte bei gleicher Bauart auseinanderlaufen (eine
  benannte Näherung in #95 `abschaetzung_kap3`, in #96 `quelle`, in #98 `berechnet`) und ließe sich weder im
  Beispiel-Block noch im Code nachrechnen, während Regel K auch Frage 1 nach festen Merkmalen beantwortet.
- **Erkennung von S2 an einer festen Wortliste** (wie in der zweiten Fassung dieser Datei): Sie übersähe die
  vereinfachte Form in pollen.d_saison und die Übertragung in heat.beta_pfl, die der Bericht mit anderen Worten
  benennt, deshalb entscheidet die Aussage und nicht das Wort.
- **Teil-Näherung nur am Band kennzeichnen** (#96 Log 25): Sie ließe den eigenen Zell-Proxy von heat.h_heim aus der
  Kennzeichnung verschwinden, weil nur ein Teil des Werts ihn trägt, und behandelte h_heim anders als
  heat.beta_85plus_region, bei dem der Süd-Wert allein die Kennzeichnung bestimmt.
- **Benannte Näherung als Modellgrenze statt als Setzung** (uv.lambda und uv.l_rest wären `quelle`, wie in der ersten
  Fassung dieser Datei): Sie zeigte in #98 als Quelle, was #95 bei gleicher Bauart (Stützstellen in
  heat.l_restlebenserwartung, Proxy heat.c_fall) als Abschätzung führt, und verletzte damit den Prüfstein aus P1.
- **Grenze nach #98 Log 36** (jede eigene Auswertung amtlicher Daten ist `berechnet`): Sie widerspricht Aufgabe §4,
  wonach `berechnet` aus anderen Parametern folgt, und machte jede Sterberate und jedes ausgezählte Quantil zu
  `berechnet`, ohne dass der Leser etwas über Setzungen erfährt.
- **Kalibrierskalar als `quelle`, weil gegen eine amtliche Reihe gefittet**: Das verwechselt die an die Reihe
  angepasste Summe mit dem Skalar, der die Setzungen des Modells ausgleicht und sich mit ihnen ändert (heat.c_kal
  0,559 statt 0,581 bei s_Süd = 1,85).
- **Quellenschlüssel ohne Block wie eine Abschätzung zählen**: Das stellte Zahlen einer Quelle schlechter als einen
  Block mit denselben Zahlen und überzeichnete die Unsicherheit amtlicher Quotienten.
- **Fünfter Anzeigetext „Quelle, ausgewertet von KAP3“**: Die Auswertung steht schon in der Herleitung, die P1 je
  Parameter verlangt, und der Text zeigte gleich gerechnete Blöcke verschieden, weil etwa heat.m_basissterberate kein
  `abgeleitet_aus` führt.
- **Einordnung aller Kapitel-7-Blöcke in der Querschnittsdatei**: verworfen, weil die Kennzeichnung eines nicht
  berechneten Blocks dem Bericht gehört und die Prüfung so nicht konvergiert (T-1812, Runden 0–2).

**Abgrenzung zur Gewissheit.** Regel K sagt, woher der Wert eines Parameters stammt. Die Gewissheit einer
Klimawirkung legt Regel G in [querschnitt_gewissheit.md](querschnitt_gewissheit.md) fest: Sie übernimmt die Gewissheit
der Bewertung aus KWRA TB6 Tabelle 1 und rechnet sie nicht aus Parametern. Die Quellenlage der Parameter erscheint
dort nur als Zählung zum Vergleich und geht in die Gewissheit nicht ein. Regel K ändert diese Zählung (Festlegung, d),
aber keine Stufe nach Regel G. querschnitt_gewissheit.md bleibt unverändert.
