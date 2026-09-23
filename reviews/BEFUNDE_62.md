# Befund-Ledger #62 — Steckbrief 62

Angelegt 18.09.2026 als Vorbereitung der Gegenprüfung des Steckbriefs 62. Dieser Steckbrief
gehört zur Klasse B nach `dokumente/produkt/m1-zuschnitt.md` Kapitel 3, nicht zu einem
Euro-Bericht. Befunde werden fortlaufend ab 1 nummeriert. Pflege über
`backend/scripts/ledger.py`. Ein Befund wird nur mit Prüfausdruck geschlossen (W7).
Zurückgestellte A-Befunde blockieren die Abnahme.

## Gegenprüfung vom 20.09.2026

Frische Sitzung nach Eiserner Regel 4 (`CLAUDE.md`): Grundlage dieser Prüfung sind
ausschließlich das Ergebnisdokument `docs/methodik/62_stadtklima_waermeinseln_steckbrief.md`,
die Kapitel 3 und 4 von `dokumente/produkt/m1-zuschnitt.md` (Firmen-Repo),
`docs/AUFGABE_METHODIK_SCHADENSRECHNUNG.md` §5 und §8 sowie der Produktcode
(`backend/app/data/catalog.py`, `catalog_parked.py`, `services/measure_service.py`,
`services/parameter_registry.py`, `services/engine/risk_engine.py`) — nicht der Schreibverlauf
der vorangegangenen Pakete. Der Bericht selbst wurde nicht geändert; Korrekturen sind Sache
eines Folgepakets.

### Geltungsbereich der vierzehn Leitfragen (§5)

Ein Steckbrief ohne Euro-Ausweis trägt weder Schadensfunktion noch Kalibrierung noch
Kostensätze eines Schadenskontos. Die folgenden Leitfragen sind deshalb hier **gegenstandslos**
und wurden nicht als Befund gewertet:

| Leitfrage | Warum gegenstandslos |
|---|---|
| 2 Verteilschlüssel-Test | setzt einen Euro-Verteilschlüssel voraus; Klasse B verteilt nichts (Zuschnitt Kap. 3, „Nicht enthalten") |
| 3 Physische Zwischengröße | fragt nach der Rückführung eines Euro-Betrags je Zelle; es gibt keinen Euro-Betrag |
| 5 Modifikatoren | keine epidemiologischen Modifikatoren, keine OR-Übersetzung im Steckbrief |
| 6 Struktur und Kopplungen | keine abgeleiteten Parameter, die neu zu rechnen wären |
| 7 Tails und Parameter | keine Verteilungsannahme, kein Kalibriermodell im Dokument |
| 8 Kalibrierung | Kalibrierung ist für Klasse B ausdrücklich ausgeschlossen |

Angewandt wurden die Leitfragen 1, 4, 9 (nur auf die Maßnahmenkosten), 10, 11, 12, 13 und 14
sowie die Prüfpunkte E1–E4 aus §8 und die Vorgaben P1 und P3 aus `CLAUDE.md`.

### Ausgeführte Prüfausdrücke der Gliederungs- und Euro-Prüfung

Alle Ausdrücke wurden am 20.09.2026 in der Repo-Wurzel ausgeführt; die Ausgaben stehen darunter.

1. Sieben vorgeschriebene Abschnitte (Zuschnitt Kap. 3):

```
grep -c '^## [1-7] ' docs/methodik/62_stadtklima_waermeinseln_steckbrief.md
7
```

Reihenfolge geprüft mit `grep -n '^## ' …`: 1 Kopf · 2 Wirkungskette · 3 Screening-Ergebnis ·
4 Was die Kommune daraus ablesen kann · 5 Warum hier kein Betrag steht · 6 Massnahme ·
7 Parameter und Quellen — deckungsgleich mit der vorgeschriebenen Reihenfolge.

2. Der im Bericht dokumentierte eingegrenzte Euro-Ausdruck (Bericht, Abschnitt 6). `awk` steht in
dieser Prüfumgebung nicht zur Verfügung; der Ausdruck wurde deshalb zweimal wirkungsgleich
ausgeführt — einmal über die Zeilenbereiche außerhalb des Abschnitts 6 (Zeilen 1–270 und
353–Ende) und einmal als Nachbau derselben Abschnittsausgrenzung in Python. Beide liefern 0:

```
sed -n -e '1,270p' -e '353,$p' docs/methodik/62_stadtklima_waermeinseln_steckbrief.md | grep -cE '[0-9][ ]?(€|EUR|Euro)'
0
```

Gegenprobe über alle Euro-Treffer des Dokuments (`grep -nE '[0-9][ ]?(€|EUR|Euro)' …`): fünf
Treffer in den Zeilen 322, 325, 332, 333 und 349 — sämtlich innerhalb des Abschnitts 6
(Zeilen 271–352) und sämtlich Maßnahmenkosten (CAPEX/OPEX), kein Euro-Betrag beziffert einen
Schaden.

3. Verwechslungssperre (Zuschnitt Kap. 4):

```
grep -nE '(^|[^0-9])0 ?(€|EUR|Euro)|Screening ohne Euro' docs/methodik/62_stadtklima_waermeinseln_steckbrief.md
256:Diese Klimawirkung ist ein Screening ohne Euro-Bezifferung — niemals ein Null-Betrag und niemals
```

Die Ziffernsperre `(^|[^0-9])` vor der Null ist nötig, damit das Muster einen Null-Betrag trifft
und nicht jede Zahl, die auf eine Null endet: Ohne sie meldet derselbe Befehl zusätzlich die
Zeilen 322, 325, 332 und 333 („40 €", „0,50 €", „350.000 €", „5.000 €") — sämtlich
Maßnahmenkosten aus Abschnitt 6 und damit für die Verwechslungssperre unschädlich. Ausgeführt
wurden beide Fassungen; die Ausgabe der engen Fassung steht oben, die weite Fassung liefert die
genannten vier Kostenzeilen zusätzlich.

Ergebnis: Kein „0 €" und kein leeres Feld für diese Klimawirkung; der vorgeschriebene Vermerk
steht wörtlich in Zeile 256. Bestanden.

4. Ausschlüsse der Klasse B (Zuschnitt Kap. 3, „Nicht enthalten"):

```
grep -niE 'schadensfunktion|kalibrier|schadenskont|hochrechn|gr(ö|oe)ssenordnung|kosten-nutzen' docs/methodik/62_stadtklima_waermeinseln_steckbrief.md
9:> KAP2 heute je 100-m-Zelle ausrechnet. Er enthält **keine** Schadensfunktion, **keine**
10:> Kalibrierung, **keine** Schadenskonten K1 bis K8, **keine** Beträge und **keinen**
11:> Kosten-Nutzen-Vergleich. Die Trennlinie ist bewusst gezogen: Id 62 ist in der Monetarisierungs-
286:Schadenssumme wird hier ausdrücklich **nicht** ausgewiesen und ein Kosten-Nutzen-Vergleich **nicht**
```

Alle Treffer sind Verneinungen. Bestanden.

5. Erklärbarkeit (A-0034, P3, §8 E3):

```
grep -niE 'verteilungsfunktion|lognormal|gumbel|weibull|poisson|varianz|standardabweichung|konfidenz|quantil|perzentil|monte' docs/methodik/62_stadtklima_waermeinseln_steckbrief.md
18:> keine Verteilungsfunktionen und keine Formeln, die über Multiplikation, Maximum und Perzentil
19:> hinausgehen. Jede Rechenaussage in Abschnitt 3 ist in einem Satz erklärt und mit der Codestelle
192:Die Zellwerte werden je Risiko zum **90. Perzentil** zusammengefasst
197:die für das Risiko einschlägige Exposition gehen nicht in das Perzentil ein, sonst zögen unbewohnte
```

Einzige statistische Größe ist das 90. Perzentil; es ist in Abschnitt 3.4 in einem Satz in
Klartext erklärt („Man sortiert alle Zellwerte … den Wert ab, den nur ein Zehntel der Zellen
übertrifft") und gegenüber dem Mittelwert begründet. E1 ja (Abschnitt 3.2, Rechenweg in Worten),
E2 ja (Beispielrechnung Abschnitt 6.2), E3 ja (keine Verteilungsfunktion; die drei Formeln
bestehen aus Multiplikation, Maximum und Deckelung), E4 ja (die drei Formeln stehen in
Klartextbenennungen statt in Formelzeichen). Abschnitt 4 ist in vier Sätzen Verwaltungssprache
gehalten und ohne Statistikkenntnis verständlich — mit der Einschränkung aus Befund 1.

6. Abschnitt 5 benennt die fehlende Kernformel-Größe und die Datenlage (Zeilen 264–269:
„Fehlende Groesse der Kernformel: Preis" und „Diese Datenlage wuerde sie liefern: …").
Formal erfüllt; siehe Befunde 9 und 11.

7. Abschnitt 7 führt je Parameter eine Spalte Herkunft und eine Spalte Quelle mit drei Fußnoten
für die als Abschätzung geführten Zeilen (A-0010, P1). Formal erfüllt; siehe Befunde 5 und 6.

## Offene Befunde (12)

Prüfbefehl der Kopfzahl, ausgeführt am 20.09.2026 in der Repo-Wurzel:

```
grep -c '| offen[ ]|' reviews/BEFUNDE_62.md
11
```

Das Muster `[ ]` trifft genau das eine Leerzeichen des Abnahmekriteriums und ist die
selbstzählfreie Schreibweise desselben Ausdrucks: Stünde das Muster wörtlich in dieser Datei,
zählte die Befehlszeile sich selbst mit und verfälschte die Kopfzahl um 1. Auf dieser Datei
liefern beide Formen dieselbe Zahl; die Kopfzahl 11 stimmt mit der Ausgabe überein.

Nachgezählt am 23.09.2026 in der Repo-Wurzel nach Aufnahme des offenen Befunds 14 (T-0510),
derselbe Befehl: vorher `11`, nachher

```
grep -c '| offen[ ]|' reviews/BEFUNDE_62.md
12
```

Die Kopfzahl ist entsprechend auf 12 nachgezogen.

| Nr | Befund (Stelle · Kurzfassung) | Kat. | Status | Umsetzungsnachweis | Prüfausdruck | Begründung bei Abweichung |
|---|---|---|---|---|---|---|
| 1 | Abschnitt 4 (Z. 249–250) · Der Bericht stellt der Kommune eine Ortsteil-Aussage in Aussicht („Diese vier Ortsteile tragen die höchste Wärmelast"), während Abschnitt 3.4 (Z. 200–205) feststellt, dass es die Ortsteil-Ebene im Rechenkern nicht gibt — aggregiert wird von der Zelle auf die Kommune. Der Adressat liest in Abschnitt 4 eine Aussage, die das Produkt heute nicht liefert; Widerspruch im Dokument (Leitfrage 14, P3). | B | offen | Abschnitt 4 nennt die tatsächliche Ausgabeebene oder verweist an Ort und Stelle auf die Einschränkung aus 3.4 | `grep -n 'Ortsteile' docs/methodik/62_stadtklima_waermeinseln_steckbrief.md` | — |
| 2 | Abschnitt 2.4 (Z. 97–106) · Die Arbeitsmappe führt zu Id 62 sieben Sensitivitäten (S094–S100), `backend/app/data/catalog.py` (`PLANNED_RISKS`, Z. 317–322) nur zwei (S099, S100). Der Bericht benennt die Lücke, löst sie aber nicht auf; nach §2.1 bleibt kein Knoten unadressiert — fünf Knoten sind weder verarbeitet noch begründet inaktiv (Leitfrage 1). | B | offen | Knoten-Bilanz für S094–S098 im Bericht oder Nachzug im Katalog, jeweils mit Begründung | `grep -n 'sensitivity_names' backend/app/data/catalog.py` | — |
| 3 | Abschnitt 3.4 (Z. 200–205) · Zuschnitt Kap. 3 Punkt 3 schreibt die „Aggregation auf Ortsteile" vor; der Rechenkern kennt diese Ebene nicht. Die Abweichung ist im Bericht vermerkt, war aber bis zu dieser Prüfung in keinem Befund-Ledger geführt, obwohl Kap. 3 jede Abweichung von der Gliederung dort verlangt (Leitfrage 14). | B | offen | Ortsteil-Ebene im Rechenkern angelegt oder Kap. 3 des Zuschnitts fortgeschrieben, Entscheid hier vermerkt | `grep -rn 'district\|ortsteil' backend/app/services/` | — |
| 4 | Abschnitt 6.2 (Z. 311–316) · Der Bericht führt `DESEALING_SURFACE` als einschlägige Maßnahme gegen die Wärmeinsel. Im geparkten Katalog (`catalog_parked.py`, Z. 944–947) trägt der Eintrag als `linked_risk_codes` nur `HYDROLOGICAL_STRESS_RISK_INDEX` und `EXPECTED_BUILDING_DAMAGE_EUR` — keinen Hitze-Pfad; auf `EXPECTED_THERMAL_STRESS_HOURS` wirkt im Katalog `URBAN_GREEN`. Die behauptete Wirkung auf den Wärmeinsel-Pfad ist im Produkt heute nicht hinterlegt (Leitfrage 12). | B | offen | Verknüpfung im Katalog ergänzt oder die Maßnahmenwahl im Bericht an die vorhandene Verknüpfung angepasst | `grep -n 'DESEALING_SURFACE' -A 4 backend/app/data/catalog_parked.py` | — |
| 5 | Abschnitt 7, Zeilen S100 und Kopplung Id 65 (Z. 369, 371) · Die Spalte Herkunft trägt das Wort „Abschaetzung", während Wert und Fußnote ausdrücklich festhalten, dass kein Zahlenwert vorliegt und die Größe offen bleibt. Damit steht weder eine Quelle noch eine ausgewiesene Abschätzung samt Herleitung — P1 und §3.9 verlangen eines von beidem; die Spaltenangabe widerspricht zudem dem Zelleninhalt (Leitfrage 13). | B | offen | Herkunft auf „offen" gestellt oder eine belegte Abschätzung mit Herleitung nachgetragen | `grep -n 'Abschaetzung' docs/methodik/62_stadtklima_waermeinseln_steckbrief.md` | — |
| 6 | Abschnitte 6.2 und 7 · Die Kostenparameter der Maßnahme (35 €/m², 0,50 €/m²/a, nachrichtlich 25 €/m² und 3 €/m²/a) stehen nur in Abschnitt 6, nicht in der Parameterliste des Abschnitts 7. Zuschnitt Kap. 3 Punkt 7 und P1 verlangen die Parameterliste „je Parameter"; verteilt auf zwei Abschnitte ist sie nicht vollzählig an einer Stelle prüfbar. | C | offen | Kostenparameter in die Tabelle des Abschnitts 7 übernommen oder dort ausdrücklich referenziert | `grep -n 'capex_per_m2' docs/methodik/62_stadtklima_waermeinseln_steckbrief.md` | — |
| 7 | Abschnitt 6.1 (Z. 294–307) · Der Bericht beschreibt ein Kostenmodell mit sechs Parametern und schreibt „Mehr Parameter als die sechs oben gibt es nicht"; Zuschnitt Kap. 3 Punkt 6 nennt ein „5-Parameter-Kostenmodell", der Katalogeintrag führt zusätzlich `benefit_per_m2_year`. Die Zählung widerspricht der verbindlichen Fassung (Leitfrage 14). | C | offen | Zählung im Bericht an den Zuschnitt angeglichen oder Zuschnitt Kap. 3 fortgeschrieben | `grep -n 'Parameter-Kostenmodell' dokumente/produkt/m1-zuschnitt.md` | — |
| 8 | Abschnitt 6, Kopf (Z. 273–281) · Der Auslieferungsbericht beginnt seinen Maßnahmenabschnitt mit einer Prüfanweisung samt Shell-Befehlszeile („Eingrenzung der Euro-Pruefung: awk …") und einem Codeblock. Prüfgerüst gehört in das Ledger, nicht in den Steckbrief, den ein Berater oder kommunaler Sachbearbeiter liest (P3, §8). | C | offen | Prüfanweisung aus dem Bericht in das Ledger verschoben | `grep -n 'Eingrenzung der Euro-Pruefung' docs/methodik/62_stadtklima_waermeinseln_steckbrief.md` | — |
| 9 | Abschnitte 5 und 6 (Z. 264–265, 271) · In einem durchgehend typografisch gesetzten Dokument stehen ASCII-Ersatzschreibungen ohne Umlaut: „Fehlende Groesse der Kernformel", „Diese Datenlage wuerde sie liefern", Überschrift „## 6 Massnahme". Formmangel im Kundenblick (P3, Leitfrage 11). | C | offen | Schreibweisen vereinheitlicht | `grep -n 'Groesse\|wuerde\|Massnahme' docs/methodik/62_stadtklima_waermeinseln_steckbrief.md` | — |
| 10 | Abschnitt 3.3 (Z. 183–185) · Der Bericht nennt die UHI-Parameterspanne „`uhi.alpha` bis `uhi.tree_cooling`". `parameter_registry.py` (Z. 294–297) führt elf Schlüssel; `tree_cooling` ist der sechste, die Spanne lässt `zeta`, `delta_night`, `night_weight`, `mean_factor` und `vent_ratio` aus — obwohl derselbe Absatz die Durchlüftungsdämpfung (`vent_ratio`) beschreibt (Leitfrage 10). | C | offen | Spannenangabe im Bericht auf den vollständigen Schlüsselsatz gebracht | `grep -n 'uhi_defaults' -A 4 backend/app/services/parameter_registry.py` | — |
| 11 | Abschnitt 5 (Z. 264) · Als fehlende Kernformel-Größe ist allein der Preis benannt. Nach Abschnitt 2.3 bucht Id 62 überhaupt nichts, es gibt also weder ein Mengengerüst exponierter Einheiten noch eine physische Wirkungsrate für diese Klimawirkung; die Beschränkung auf den Preis ist im Bericht nicht begründet (Zuschnitt Kap. 3 Punkt 5: „Menge, Rate oder Preis"). | C | offen | Abschnitt 5 benennt alle fehlenden Größen oder begründet die Beschränkung auf den Preis | `grep -n 'Fehlende Groesse der Kernformel' docs/methodik/62_stadtklima_waermeinseln_steckbrief.md` | — |
| 12 | Kopplung der Maßnahme Entsiegelung an die Wärmebelastung · Methodischer Entscheid zu `DESEALING_SURFACE` (`catalog_parked.py`, Z. 944–962) gegenüber der Wirkbeschreibung in `catalog.py` (`_MEASURE_EFFECT_DOCS`, Z. 1943–1956). Verdikt, Doppelzählungsprüfung nach G13 und Berichtsfolge im Abschnitt „Befund 12" unter dieser Tabelle. | B | geschlossen (Entscheid, niedergelegt in diesem Ledger): Verdikt „Kopplung wird nicht ergänzt"; die Berichtsformulierung ist im Wortlaut vorgegeben und wird mit Befund 4 eingesetzt | Abschnitt „Befund 12" unten (vier Punkte: Stand, Verdikt, Doppelzählungsprüfung, Berichtsfolge) | `grep -n 'DESEALING_SURFACE' -A 4 backend/app/data/catalog_parked.py` (Sollzustand: `linked_risk_codes` ohne Wärmekennzahl) | — |
| 13 | Sensitivitäten S094 bis S098 im Quellenblatt, aber nicht in `catalog.py` · Methodischer Entscheid zu den fünf Sensitivitäten, die die Arbeitsmappe der Klimawirkung #62 zuordnet (`KWRA-Schadensbaum_X_UBA-klimawirkungsketten.xlsx`, Blatt „Klimawirkungsketten", Zeile 279) und die der Katalogeintrag `PLANNED_RISKS`/`kwra_id: 62` (`catalog.py`, Z. 317–322) nicht führt. Fundstellen, Ergebniswirkung je Kennung und Verdikt im Abschnitt „Befund 13" unter dieser Tabelle. | B | behoben (T-0541, 23.09.2026, Nacharbeitsrunde 1): Nachzug umgesetzt in `backend/app/data/catalog.py` an beiden von Punkt 4 genannten Stellen — Feld `sensitivity_names` des Eintrags `kwra_id: 62`, Z. 327, trägt jetzt sieben Namen (S094–S100) in Reihenfolge des Quellenblatts; der Quellenkommentar über `PLANNED_RISKS`, Z. 318–321, vermerkt den abweichenden Vorrang des Schadensbaum-Quellenblatts für #62. Test `backend/tests/test_katalog_sensitivitaeten_62.py` | Abschnitt „Befund 13" unten (vier Punkte: Fundstellen und Fehlnachweis, Ergebniswirkung, Verdikt, Folgepaket) | `python3 -c "import sys; sys.path.insert(0,'backend'); from app.data import catalog; print([p for p in catalog.PLANNED_RISKS if p['kwra_id']==62][0]['sensitivity_names'])"` (Sollzustand: sieben Namen statt zwei) | — |
| 14 | Derselbe Nutzenwert 5 €/(m²·a) bei URBAN_GREEN und DESEALING_SURFACE · `benefit_per_m2_year: 5.0` aus derselben Quelle TEEB DE steht an zwei Maßnahmen mit zwei einander widersprechenden Herleitungen: bei `URBAN_GREEN` (`catalog_parked.py`, Z. 1371–1375) ausdrücklich ohne Kühlanteil („über die vermiedenen Hitzeschäden hinaus"), bei `DESEALING_SURFACE` (`catalog.py`, `_MEASURE_EFFECT_DOCS`, Z. 1957–1961) ausdrücklich mit Kühlanteil („Versickerung, Kühlung, Grün"). Verdikt: keine Doppelzählung bei URBAN_GREEN, aber ungeklärte Zusammensetzung des Punktwerts (G13, G14/§3.9, P1). Einzelheiten im Abschnitt „Befund 14" unter dieser Tabelle. | B | offen | Beide Herleitungen auf eine belegte Zusammensetzung des Punktwerts gebracht (mit oder ohne Kühlanteil, je Maßnahme begründet), oder abweichende Werte mit eigener Quelle | `grep -n 'Direkter Zusatznutzen über die vermiedenen Hitzeschäden\|Versickerung, Kühlung, Grün' backend/app/data/catalog_parked.py backend/app/data/catalog.py` | — |

Die Befunde 12 und 13 sind mit ihrer Niederschrift geschlossen und zählen deshalb nicht in die
Kopfzahl der elf offenen Befunde; die Ausgabe des Kopf-Prüfbefehls bleibt unverändert 11. Befund 2
bleibt offen: Er wird erst mit dem Nachzug im Katalog geschlossen, den Befund 13 anordnet.
Befund 14 (23.09.2026) ist offen und hebt die Kopfzahl auf 12.

Kein Befund der Kategorie A: Die harten Sperren der Klasse B sind eingehalten — sieben
Abschnitte in der vorgeschriebenen Reihenfolge, kein Euro-Betrag außerhalb der Maßnahmenkosten,
kein Null-Betrag und kein leeres Feld, keine Schadensfunktion, keine Kalibrierung, keine
Schadenskonten und keine Hochrechnung einer Größenordnung.

### Befund 12 — Kopplung der Maßnahme Entsiegelung an die Wärmebelastung

Entschieden am 20.09.2026 aus den offenen Fragen der Läufe zu T-0407 (Entwickler und Prüfer).
Anlass ist Befund 4: Der Steckbrief führt die Entsiegelung als einschlägige Maßnahme gegen die
Wärmeinsel, der Katalog kennt für diese Maßnahme keinen Wärme-Pfad. Dieser Befund entscheidet
die Frage methodisch, bevor ein Feld angefasst wird; der Katalog wird von diesem Paket **nicht**
geändert.

**1. Der heutige Stand.** `DESEALING_SURFACE` steht in `backend/app/data/catalog_parked.py`
(Eintrag Z. 944–962) mit
`linked_risk_codes: ["HYDROLOGICAL_STRESS_RISK_INDEX", "EXPECTED_BUILDING_DAMAGE_EUR"]`
(Z. 947) — also ohne jede Verknüpfung zu einer Wärme- oder Hitzekennzahl; die Wärmekennzahl
`EXPECTED_THERMAL_STRESS_HOURS` (`catalog_parked.py`, Z. 486–493) trägt dort nicht. Die
Wirkbeschreibung derselben Maßnahme in `backend/app/data/catalog.py`
(`_MEASURE_EFFECT_DOCS["DESEALING_SURFACE"]`, Z. 1943–1956) nennt die Kühlwirkung dagegen
ausdrücklich („Zusätzlich kühlt die Fläche und speist Grundwasser", Z. 1948–1949) und führt
„die verknüpften Überflutungs-/Hitzerisiken" als Wirkziel des Reduktionsansatzes von 30 %
(Z. 1949–1950). Katalogfeld und Wirkbeschreibung widersprechen einander: Das Feld kennt keinen
Hitzepfad, der Text unterstellt einen. Im Rechenweg wirkt allein das Feld —
`backend/app/services/measure_service.py` (Z. 578–580) multipliziert den Zellindex jedes in
`linked_risk_codes` genannten Risikos mit dem Reduktionsfaktor, der Text wird nur angezeigt.

**2. Verdikt: Kopplung wird nicht ergänzt.** Der Reduktionswert `default_reduction: 0.30` ist in
`_MEASURE_EFFECT_DOCS` allein aus dem Abflussbeiwert hergeleitet (0,9 → 0,1–0,3 nach DWA-A 138);
für die Wärmebelastung existiert im Produkt keine eigene hergeleitete Reduktionsrate, und der
Katalog führt je Maßnahme nur **einen** Reduktionswert für alle verknüpften Risiken — eine
Kopplung übertrüge also stillschweigend eine hydrologisch hergeleitete Zahl auf einen thermischen
Index und verstieße gegen die Herleitungspflicht (G14, §3.9). Die Roadmap-Grundregel „kein Risiko
ohne mindestens eine Maßnahme" drängt hier nicht: Auf `EXPECTED_THERMAL_STRESS_HOURS` wirken im
geparkten Katalog bereits acht Maßnahmen, darunter `URBAN_GREEN` (Z. 1337–1340) und `COOL_ROOFS` (Z. 963–966), das
Risiko ist also versorgt. Hinzu kommt die Doppelzählung nach Punkt 3, die vor einer Kopplung erst
aufgelöst werden müsste. Der Entscheid ist revidierbar, sobald eine eigene, belegte
Kühlwirkungsrate der Entsiegelung hergeleitet und der Nutzenwert bereinigt ist; er hält den
Zustand nur so lange fest, wie beides fehlt.

**3. Doppelzählungsprüfung nach G13 „Keine Wirkung über zwei Kanäle".** Ja — der Wert
`benefit_per_m2_year: 5.0` enthält bereits einen Hitzenutzen: Seine Herleitung in
`_MEASURE_EFFECT_DOCS` (`catalog.py`, Z. 1951–1955; Quellenlage der `source_details`
Niederschlagswasserentgelt und Ökosystemleistung) setzt sich aus dem entfallenden
Niederschlagswasserentgelt (1,84 €/m²·a, BWB Berlin) und Ökosystemleistungen nach TEEB DE
zusammen, und die dort aufgezählten Leistungen sind wörtlich „Versickerung, **Kühlung**, Grün".
Der Kühlanteil steckt damit heute monetarisiert im direkten Zusatznutzen, den
`measure_service.py` (Z. 486) als `benefit_per_m2_year · Fläche` additiv zum Schadensnutzen
führt. Würde die Maßnahme zusätzlich auf `EXPECTED_THERMAL_STRESS_HOURS` gekoppelt, entstünde der
Hitzenutzen ein zweites Mal als vermiedener Schaden — diese Kennzahl trägt in `catalog.py`
(Z. 957–964) einen Kostensatz von 400 €/Belastungsstunde und wird in
`measure_service.py` zu einem Euro-Nutzen verrechnet: dieselbe physikalische Kühlwirkung über zwei
Kanäle. Eine spätere Kopplung vermeidet die Doppelzählung nur so: Der Nutzenwert wird vorher auf
den nicht-thermischen Anteil zurückgeschnitten (Niederschlagswasserentgelt plus Versickerungs- und
Grünleistung, ohne Kühlanteil), die Kürzung wird in `source_details` mit Zahl und Begründung
ausgewiesen, und der Wärmepfad bekommt eine eigene, aus Kühlwirkungsliteratur hergeleitete
Reduktionsrate statt der hydrologischen 0,30. Solange diese Trennung nicht belegt ist, bleibt die
Kopplung aus.

**Was ein Folgepaket ändern müsste (nicht in diesem Paket).** Zwei Stellen, beide außerhalb des
Dateirahmens dieses Pakets: (a) `backend/app/data/catalog.py`,
`_MEASURE_EFFECT_DOCS["DESEALING_SURFACE"]["default_reduction"]` — die Formulierung „der
verknüpften Überflutungs-/Hitzerisiken" behauptet einen Hitzepfad, den das Katalogfeld nicht
trägt, und ist auf die tatsächlich verknüpften Risiken zurückzuführen; (b) falls der Entscheid
später gedreht wird, `backend/app/data/catalog_parked.py`, Feld `linked_risk_codes` des Eintrags
`DESEALING_SURFACE` (Z. 947) sowie die Felder `default_reduction` und `benefit_per_m2_year`
(Z. 946, 949) nach Punkt 3.

**4. Folge für den Steckbrief #62.** Ja, der Steckbrief muss seinen Verweis anpassen: Abschnitt
6.2 von `docs/methodik/62_stadtklima_waermeinseln_steckbrief.md` nennt die Entsiegelung als „die
einschlägige Maßnahme … für die Wärmeinsel", ohne offenzulegen, dass das Produkt für diese
Maßnahme keine Wirkung auf eine Wärmekennzahl rechnet. Anzupassen ist Abschnitt 6.2 durch einen
zusätzlichen Absatz am Ende des Abschnitts, mit genau dieser Formulierung:

> **Was das Produkt für diese Maßnahme heute nicht rechnet.** Im Katalog ist die Entsiegelung
> allein mit dem hydrologischen Belastungsindex und dem erwarteten Gebäudeschaden verknüpft, nicht
> mit einer Wärme- oder Hitzekennzahl. Dieser Steckbrief nennt die Maßnahme deshalb wegen ihres
> Ansatzpunkts am Versiegelungsgrad und wegen ihres Kostenrahmens; eine im Produkt gerechnete
> Wirkung auf die Wärmebelastung behauptet er nicht.

Damit behauptet der Bericht keine Produktkopplung, die im Katalog nicht besteht. Eingesetzt wird
der Absatz nicht hier, sondern in dem Paket, das Befund 4 abarbeitet: Jede Einfügung in den
Steckbrief verschiebt dessen Zeilennummern, und die Zeilenverweise samt Euro-Prüfausdrücken der
Gegenprüfung oben werden dann in einem Zug nachgezogen statt zweimal. Befund 4 bleibt bis dahin
offen; dieser Befund liefert dafür die Entscheidungsgrundlage, schließt den Zweig „Verknüpfung im
Katalog ergänzt" aus und gibt den Wortlaut des verbleibenden Zweigs vor.

### Befund 13 — Sensitivitäten S094 bis S098 im Quellenblatt, aber nicht in catalog.py

Entschieden am 21.09.2026 aus der offenen Frage
`Q-20260920T110402Z-pruefer-ab99af-2` der Gegenprüfung zu T-0408. Anlass ist Befund 2: Das
Quellenblatt ordnet der Klimawirkung #62 sieben Sensitivitäten zu, der Produktkatalog führt zwei.
Dieser Befund entscheidet die Frage methodisch, bevor ein Feld angefasst wird; der Katalog wird
von diesem Paket **nicht** geändert.

**1. Fundstellen im Quellenblatt und Fehlnachweis in `catalog.py`.** Quellenblatt ist die
Arbeitsmappe `docs/Schadensbaum/KWRA-Schadensbaum_X_UBA-klimawirkungsketten.xlsx`, Blatt
„Klimawirkungsketten". Die Klimawirkung #62 steht dort in Zeile 279 (Id `W124`,
„Stadtklima/Wärmeinseln") und führt in der Spalte `Input_IDs_Sensitivitäten` die Zeichenkette
`S094; S095; S096; S097; S098; S099; S100`; jede der fünf hier strittigen Kennungen hat im selben
Blatt zusätzlich eine eigene Stammzeile vom Typ „Sensitivität". Ausgeführt am 21.09.2026 in der
Repo-Wurzel:

```
python3 -c "
import openpyxl
wb=openpyxl.load_workbook('docs/Schadensbaum/KWRA-Schadensbaum_X_UBA-klimawirkungsketten.xlsx',read_only=True,data_only=True)
for i,r in enumerate(wb['Klimawirkungsketten'].iter_rows(values_only=True),1):
    if r[0] in ('S094','S095','S096','S097','S098'): print(i, r[0], r[1], r[2])
    if i==279: print(i, r[0], r[5])
"
258 S094 Verwendete Baumaterialien auf Gebäudeebene Sensitivität
259 S095 Begrünung von Gebäuden Sensitivität
260 S096 Bauliche, organisatorische und finanzielle Vorsorge der öffentlichen Hand Sensitivität
261 S097 Zustand von (Schutz-)Infrastrukturen Sensitivität
262 S098 Verwendete Baumaterialien von (Schutz-)Infrastrukturen Sensitivität
279 W124 S094; S095; S096; S097; S098; S099; S100
```

Der Fehlnachweis in `backend/app/data/catalog.py` hat zwei Teile, weil der Katalog Sensitivitäten
nicht über die Kennung, sondern über den Klartextnamen führt. Erstens kommt keine der fünf
Kennungen in der Datei überhaupt vor (Ausgabe je Befehlszeile darunter):

```
grep -c 'S094' backend/app/data/catalog.py
0
grep -c 'S095' backend/app/data/catalog.py
0
grep -c 'S096' backend/app/data/catalog.py
0
grep -c 'S097' backend/app/data/catalog.py
0
grep -c 'S098' backend/app/data/catalog.py
0
```

Zweitens führt der Eintrag zu #62 nur die beiden Namen von S099 und S100:

```
grep -n '"kwra_id": 62' -A 5 backend/app/data/catalog.py | grep 'sensitivity_names'
321-     "sensitivity_names": ["Begrünung von Städten / Siedlungen", "Grad der Versiegelung"],
```

```
python3 -c "
import sys; sys.path.insert(0,'backend')
from app.data import catalog
e=[p for p in catalog.PLANNED_RISKS if p['kwra_id']==62][0]
for n in ['Verwendete Baumaterialien auf Gebäudeebene','Begrünung von Gebäuden','Bauliche, organisatorische und finanzielle Vorsorge der öffentlichen Hand','Zustand von (Schutz-)Infrastrukturen','Verwendete Baumaterialien von (Schutz-)Infrastrukturen']:
    print(n in e['sensitivity_names'], n)
"
False Verwendete Baumaterialien auf Gebäudeebene
False Begrünung von Gebäuden
False Bauliche, organisatorische und finanzielle Vorsorge der öffentlichen Hand
False Zustand von (Schutz-)Infrastrukturen
False Verwendete Baumaterialien von (Schutz-)Infrastrukturen
```

Je Kennung zusammengefasst — Datei des Fehlnachweises ist durchgehend
`backend/app/data/catalog.py`, Eintrag `PLANNED_RISKS` mit `kwra_id: 62` (Z. 317–322):

| Kennung | Name im Quellenblatt | Stammzeile (Blatt „Klimawirkungsketten") | Zuordnung zu #62 | Fehlnachweis in `catalog.py` |
|---|---|---|---|---|
| S094 | Verwendete Baumaterialien auf Gebäudeebene | Zeile 258 | Zeile 279, Spalte `Input_IDs_Sensitivitäten`, erstes Listenglied | `grep -c 'S094' …/catalog.py` → `0`; Name nicht in `sensitivity_names` von #62 (Python-Abgleich → `False`). Der Name steht an anderer Stelle der Datei (`grep -c '…auf Gebäudeebene'` → `3`), aber bei den Einträgen #63, #60 und #59, nicht bei #62. |
| S095 | Begrünung von Gebäuden | Zeile 259 | Zeile 279, zweites Listenglied | `grep -c 'S095' …/catalog.py` → `0`; Name nicht in `sensitivity_names` von #62 (→ `False`). Der Name kommt einmal in der Datei vor (→ `1`), dort beim Eintrag #63. |
| S096 | Bauliche, organisatorische und finanzielle Vorsorge der öffentlichen Hand | Zeile 260 | Zeile 279, drittes Listenglied | `grep -c 'S096' …/catalog.py` → `0`; Name nicht in `sensitivity_names` von #62 (→ `False`). Der Name kommt einmal in der Datei vor (→ `1`), dort beim Eintrag #61. |
| S097 | Zustand von (Schutz-)Infrastrukturen | Zeile 261 | Zeile 279, viertes Listenglied | `grep -c 'S097' …/catalog.py` → `0`; Name nicht in `sensitivity_names` von #62 (→ `False`). Der Name kommt zweimal in der Datei vor (→ `2`), an beiden Stellen bei anderen Einträgen. |
| S098 | Verwendete Baumaterialien von (Schutz-)Infrastrukturen | Zeile 262 | Zeile 279, fünftes Listenglied | `grep -c 'S098' …/catalog.py` → `0`; Name nicht in `sensitivity_names` von #62 (→ `False`); der Name kommt in der ganzen Datei nicht vor (`grep -c 'Verwendete Baumaterialien von (Schutz-)Infrastrukturen' …/catalog.py` → `0`). |

**2. Verändert das Fehlen ein ausgewiesenes Ergebnis?** Nein — für keine der fünf Kennungen. Die
betroffene Größe ist in allen fünf Fällen dieselbe: das reine Beschreibungsfeld
`sensitivity_names` des geplanten (gesperrten) Katalogeintrags `kwra_id: 62`, das über
`backend/app/api/routes/catalog.py` (Z. 49–52) als `planned_risks[].sensitivity_names` in die
Antwort von `GET /catalog` geht. Weder der Rechenkern noch die Oberfläche liest es; die Oberfläche
zeigt von einem geplanten Eintrag nur Name und Stufenlabel
(`frontend/src/components/LayerPanel.tsx`, Z. 246–251). Prüfausdruck, ausgeführt am 21.09.2026 in
der Repo-Wurzel — die einzige Fundstelle außerhalb der Katalogdatei ist eine Typdeklaration ohne
Anzeige:

```
grep -rn 'sensitivity_names' backend/app/services backend/app/api frontend/src
frontend/src/types/index.ts:400:  sensitivity_names: string[]
```

Daraus je Kennung derselbe Satz, mit der Größe, die betroffen wäre:

- **S094:** Das Fehlen verändert kein ausgewiesenes Ergebnis; betroffen wäre allein die Länge und
  der Inhalt der Liste `planned_risks[].sensitivity_names` des Eintrags #62 in der Antwort von
  `GET /catalog` — kein Index, kein Euro-Betrag, keine Karte.
- **S095:** wie S094 — kein ausgewiesenes Ergebnis betroffen, nur dasselbe Listenfeld.
- **S096:** wie S094 — kein ausgewiesenes Ergebnis betroffen, nur dasselbe Listenfeld.
- **S097:** wie S094 — kein ausgewiesenes Ergebnis betroffen, nur dasselbe Listenfeld.
- **S098:** wie S094 — kein ausgewiesenes Ergebnis betroffen, nur dasselbe Listenfeld.

Der Grund gilt für alle fünf gemeinsam: #62 ist eine Klimawirkung der Klasse B ohne
Schadensbetrag, steht in `PLANNED_RISKS` (gesperrt) und trägt nach Abschnitt 2.3 des Steckbriefs
ohnehin nichts in ein Schadenskonto. Weil kein Ergebnis betroffen ist, bleibt der Steckbrief
#62 an der zitierenden Stelle (Abschnitt 2.4) unverändert: Seine Aussage, die Arbeitsmappe nenne
sieben und der Katalog führe zwei Sensitivitäten, ist durch Punkt 1 in genau diesem Wortlaut
bestätigt, und sein Satz „Dieser Steckbrief ändert dazu nichts am Code" bleibt richtig.

**3. Verdikt: wird im Katalog ergänzt.** Das Quellenblatt ist nach dem Prüfgrundlagen-Bundle
(`CLAUDE.md`) die verbindliche Arbeitsmappe, und seine Zuordnung ist für #62 nicht pauschal,
sondern eigens gesetzt — die zwölf Bauwesen-Klimawirkungen der Zeilen 272 bis 283 tragen sieben
verschiedene Sensitivitätslisten, #62 als einzige genau diese sieben. Eiserne Regel 2 verbietet,
die Arbeitsmappe still zu überstimmen; §2.1 lässt keinen Knoten unadressiert, und fünf Knoten
sind derzeit weder verarbeitet noch begründet inaktiv (Befund 2). Der Nachzug ist risikolos, weil
er nach Punkt 2 kein ausgewiesenes Ergebnis bewegt und keinen Zahlenwert mit Herleitungspflicht
einführt — anders als die Kopplungsfrage in Befund 12, wo eine hydrologisch hergeleitete
Reduktionsrate auf einen thermischen Pfad übertragen worden wäre. Zu klären hat das Folgepaket
dabei den Ursprung der Abweichung: Der Kommentar über `PLANNED_RISKS` (`catalog.py`, Z. 307–315)
nennt als Herkunft der Namenslisten das Blatt „Wirkungsmechanismen" der Mappe
`docs/KWAR/KWRA-2021_Klimawirkungen.xlsx`, das für #62 in Zeile 67 nur die beiden Namen von S099
und S100 führt — der heutige Katalogstand ist also seiner eigenen Quelle treu, und zwei
Digitalisate derselben UBA-Zeichnung von 2016 widersprechen einander.

**4. Was ein Folgepaket ändern muss (nicht in diesem Paket).** Datei: `backend/app/data/catalog.py`.
Feld: der Schlüssel `sensitivity_names` im Eintrag der Liste `PLANNED_RISKS` mit `kwra_id: 62`
(heute Z. 321) — er wird um die fünf Namen aus der Tabelle in Punkt 1 auf sieben Einträge
erweitert, in der Reihenfolge des Quellenblatts (S094 bis S100). Zweite Stelle in derselben Datei:
der Quellenkommentar über `PLANNED_RISKS` (Z. 307–315), der die Herkunft der Namenslisten
heute allein dem Blatt „Wirkungsmechanismen" zuschreibt; für #62 ist dort der abweichende
Vorrang des Schadensbaum-Quellenblatts samt Zeilenangabe 279 zu vermerken, sonst entstünde eine
neue stille Abweichung von der genannten Quelle. Der Test
`backend/tests/test_planned_risks.py` prüft Anzahl, IDs, Stufen und nichtleere Treiberlisten,
nicht die Länge der Sensitivitätsliste; er bleibt von der Ergänzung unberührt, ist aber nach dem
Nachzug auszuführen. Mit diesem Nachzug wird Befund 2 schließbar; bis dahin bleibt er offen.
Dieses Paket ändert `catalog.py` nicht.

**Nachzug erledigt (T-0541, 23.09.2026, Nacharbeitsrunde 1).** Beide in Punkt 4 genannten Stellen
sind umgesetzt: `backend/app/data/catalog.py`, Feld `sensitivity_names` des Eintrags
`kwra_id: 62` (Z. 327), trägt jetzt die sieben Namen S094 bis S100 in der Reihenfolge des
Quellenblatts; geprüft durch `backend/tests/test_katalog_sensitivitaeten_62.py`. Der
Quellenkommentar über `PLANNED_RISKS` (jetzt Z. 309–321) trägt zusätzlich zur bisherigen
Herkunftsangabe („Wirkungsmechanismen") einen eigenen Absatz (Z. 318–321), der für `kwra_id: 62`
den abweichenden Vorrang des Schadensbaum-Quellenblatts (Blatt „Klimawirkungsketten", Zeile 279)
festhält und auf diesen Befund verweist — die in Punkt 4 befürchtete neue stille Abweichung von
der genannten Quelle entsteht damit nicht. `backend/tests/test_planned_risks.py` wurde nach dem
Nachzug erneut ausgeführt (grün). Damit ist Befund 13 vollständig behoben. Befund 2 ist damit
inhaltlich miterledigt (die Knoten-Bilanz für S094–S098 ist über den Katalog-Nachzug aufgelöst);
seinen eigenen Status auf geschlossen zu setzen und die Kopfzahl der offenen Befunde
nachzuziehen ist nach Punkt „Wahlweise" der Nacharbeit nicht Pflicht dieses Tickets und bleibt
für ein Folgepaket offen.

### Befund 14 — Derselbe Nutzenwert 5 €/(m²·a) bei URBAN_GREEN und DESEALING_SURFACE

Aufgenommen am 23.09.2026 aus den offenen Fragen der Läufe zu T-0480
(`Q-20260920T133924Z-entwickler-1e9861-2`, `Q-20260920T134212Z-pruefer-8c14f9-2`). Anlass ist
Befund 12, Punkt 3: Dort ist für die Entsiegelung festgestellt, dass der Nutzenwert
`benefit_per_m2_year: 5.0` einen Kühlanteil enthält. `URBAN_GREEN` trägt denselben Wert aus
derselben Quelle (TEEB DE) und ist zugleich auf eine Wärmekennzahl gekoppelt. Dieser Befund stellt
nur die Aktenlage fest; Katalog und Dienst werden von diesem Paket **nicht** geändert, und es
entsteht keine neue Zahl. Zeilenangaben nach dem Stand des Branches `ticket/T-0510` am 23.09.2026.

**1. Die beiden Herleitungstexte zu `benefit_per_m2_year`.**

*URBAN_GREEN* — `backend/app/data/catalog_parked.py`, Eintrag Z. 1337–1375; Wert
`"benefit_per_m2_year": 5.0` in Z. 1342, Quellenangabe `"TEEB DE (Ökosystemleistungen Stadtgrün)"`
in Z. 1348, Quellenschlüssel `["TEEB_DE_Naturkapital"]` in Z. 1351, Herleitungstext Z. 1371–1375:

> „Direkter Zusatznutzen über die vermiedenen Hitzeschäden hinaus: Stadtgrün liefert
> quantifizierbare Ökosystemleistungen (Regenwasserrückhalt → geringeres
> Niederschlagswasserentgelt, Luftreinhaltung, Erholungs-/Gesundheitswert; TEEB DE beziffert
> städtische Ökosystemleistungen auf einige €/m²·a). Punktwert 5 €/(m²·a) als konservative Summe
> von Rückhalte- und Erholungsnutzen; editierbar."

Feststellung: Dieser Text rechnet **keinen** Kühl- oder Hitzenutzen in die 5,0 € ein. Er nimmt ihn
dem Wortlaut nach ausdrücklich aus („über die vermiedenen Hitzeschäden hinaus") und benennt als
Bestandteile des Punktwerts allein Rückhalte- und Erholungsnutzen.

*DESEALING_SURFACE* — `backend/app/data/catalog_parked.py`, Eintrag Z. 944–962; Wert
`"benefit_per_m2_year": 5.0` in Z. 949. **In `catalog_parked.py` steht zu diesem Feld kein
Herleitungstext:** `sources` (Z. 952–953) und `source_details` (Z. 955–962) führen nur
`capex_per_m2` und `opex_per_m2_year`, `source_refs` (Z. 954) nur `capex_per_m2`. Die einzige
Herleitung des Werts steht in `backend/app/data/catalog.py`,
`_MEASURE_EFFECT_DOCS["DESEALING_SURFACE"]["benefit_per_m2_year"]`, Z. 1957–1961 (Quellenangabe
„Gesplittete Abwassergebühr + Ökosystemleistung", Schlüssel `BWB_Niederschlagswasserentgelt`,
`TEEB_DE_Naturkapital`):

> „Direkter Zusatznutzen: Entsiegelte Flächen entfallen aus dem Niederschlagswasserentgelt
> (z. B. 1,84 €/m²·a in Berlin, BWB) und erbringen Ökosystemleistungen (Versickerung, Kühlung,
> Grün; TEEB DE einige €/m²·a) → Punktwert 5 €/(m²·a). Kommunal unterschiedlich, editierbar."

Feststellung: Dieser Text rechnet einen **Kühlnutzen** in die 5,0 € ein („Versickerung, Kühlung,
Grün"). Er wird nach `_enrich_measure_effect_docs` (`catalog.py`, Z. 2289–2309) nur an Einträge der
aktiven Liste `MEASURES` gehängt; der geparkte Eintrag bekommt ihn heute nicht, der Text ist dem
Wert also nur über den Code-Schlüssel zugeordnet (Beobachtung, kein eigener Befund hier).

Ergebnis: Derselbe Punktwert 5,0 aus derselben Quelle TEEB DE ist einmal ohne, einmal mit
Kühlanteil hergeleitet. Beide Lesarten können nicht zugleich stimmen: Enthält der TEEB-Wert einen
Kühlanteil, ist die Herleitung bei `URBAN_GREEN` falsch; enthält er keinen, ist die Herleitung bei
`DESEALING_SURFACE` falsch und die Begründung der Doppelzählungsprüfung in Befund 12, Punkt 3,
trägt nur über ihren Wortlaut, nicht über die Quelle. Welche Lesart stimmt, lässt sich aus dem
Katalog nicht entscheiden — keiner der beiden Texte zerlegt den Punktwert in Zahlen je Leistung.

**2. Kopplung an eine Wärme- oder Hitzekennzahl über `linked_risk_codes`.**

- `URBAN_GREEN`: `"linked_risk_codes": ["EXPECTED_THERMAL_STRESS_HOURS"]`,
  `catalog_parked.py` Z. 1340 — gekoppelt an die Wärmekennzahl „Stunden thermischer Belastung"
  (`EXPECTED_THERMAL_STRESS_HOURS`, `catalog_parked.py` Z. 486; Kostensatz 400 € je
  Belastungsstunde in `catalog.py` Z. 963–969).
- `DESEALING_SURFACE`: `"linked_risk_codes": ["HYDROLOGICAL_STRESS_RISK_INDEX",
  "EXPECTED_BUILDING_DAMAGE_EUR"]`, `catalog_parked.py` Z. 947 — an **keine** Wärme- oder
  Hitzekennzahl gekoppelt (Stand nach Befund 12, Verdikt „Kopplung wird nicht ergänzt").

**3. Die Addition in `measure_service.py`.** `backend/app/services/measure_service.py`, Z. 486,
bildet den direkten Zusatznutzen `annual_benefit_direct = benefit_per_m2_year · covered_area_m2`;
Z. 503–504 addiert ihn zum vermiedenen Schaden der gekoppelten Risiken:
`"annual_benefit_eur": round(annual_benefit_direct + annual_benefit_damage + annual_benefit_flat, 2)`.
Der Schadensanteil `annual_benefit_damage` entsteht aus der Minderung der Zellindizes jedes Risikos
in `linked_risk_codes` (Z. 363 und Schleife ab Z. 578), bei `URBAN_GREEN` also allein aus der
Minderung der Stunden thermischer Belastung. Diese Addition zählt bei URBAN_GREEN denselben Effekt
nicht zweimal, solange der Herleitungstext gilt: Der Schadensanteil trägt den Kühleffekt, der
direkte Zusatznutzen nach Z. 1371–1375 nur Rückhalte- und Erholungsnutzen. Sie zählte ihn zweimal,
wenn der Punktwert 5,0 — wie die Entsiegelungs-Herleitung für dieselbe Quelle behauptet — einen
Kühlanteil enthielte. Beide Maßnahmen stehen heute in `_PARKED_MEASURES` und nicht in
`catalog.MEASURES`; die Addition wird für sie derzeit nicht ausgeführt und wird es erst mit ihrer
Rückkehr in den aktiven Katalog.

**4. Verdikt: Doppelzählung besteht bei URBAN_GREEN nicht.** Grundsatz G13 („keine Wirkung über
zwei Kanäle", Aufgabe §3.2 „Kein-Doppelkanal", Z. 256–258) verlangt, dass jede physikalische
Wirkung genau einmal zählt und vor Aufnahme eines Faktors geprüft wird, ob er implizit schon in
einem Eingang steckt. Bei `URBAN_GREEN` läuft die Kühlwirkung nur über einen Kanal, die Kopplung
an `EXPECTED_THERMAL_STRESS_HOURS`, denn der Herleitungstext des Nutzenwerts nimmt Hitzeschäden
ausdrücklich aus und benennt allein Rückhalte- und Erholungsnutzen. Nach der Aktenlage ist G13 damit
eingehalten. Offen bleibt der Befund dennoch, weil dieselbe TEEB-Zahl bei der Entsiegelung mit
Kühlanteil hergeleitet ist und G13 nur so sicher erfüllt ist, wie diese Widersprüchlichkeit
aufgelöst wird. Neue Zahlen, die eine Aufteilung des Punktwerts bräuchten, setzt dieser Befund
nicht (P1).

**5. Folgepaket bei Verdikt „besteht".** Entfällt nach dem Verdikt in Punkt 4.

**Was ein Folgepaket für den offenen Widerspruch klären müsste (nicht in diesem Paket).** Die
Zusammensetzung des TEEB-DE-Werts aus der Quelle selbst belegen und danach genau eine der beiden
Herleitungen richtigstellen: `backend/app/data/catalog_parked.py`, Eintrag `URBAN_GREEN`,
`source_details["benefit_per_m2_year"]` (Z. 1371–1375), oder `backend/app/data/catalog.py`,
`_MEASURE_EFFECT_DOCS["DESEALING_SURFACE"]["benefit_per_m2_year"]` (Z. 1957–1961). Ergäbe die
Quelle einen Kühlanteil im Wert von `URBAN_GREEN`, wäre dessen Feld `benefit_per_m2_year`
(Z. 1342) um diesen Anteil zu kürzen; betroffen wäre dann im Produkt der Jahresnutzen der Maßnahme
(`annual_benefit_eur`), in der Oberfläche „Nutzen/Jahr" (Maßnahmentabelle) und „Vermiedene
Schäden / Nutzen" (Maßnahmen-Seitenleiste).
