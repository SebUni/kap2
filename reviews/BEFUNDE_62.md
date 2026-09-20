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
grep -nE '0 ?(€|EUR|Euro)|Screening ohne Euro' docs/methodik/62_stadtklima_waermeinseln_steckbrief.md
256:Diese Klimawirkung ist ein Screening ohne Euro-Bezifferung — niemals ein Null-Betrag und niemals
```

Kein „0 €" und kein leeres Feld für diese Klimawirkung; der vorgeschriebene Vermerk steht
wörtlich. Bestanden.

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

## Offene Befunde (11)

Prüfbefehl der Kopfzahl, ausgeführt am 20.09.2026 in der Repo-Wurzel:

```
grep -c '| offen[ ]|' reviews/BEFUNDE_62.md
11
```

Das Muster `[ ]` trifft genau das eine Leerzeichen des Abnahmekriteriums und ist die
selbstzählfreie Schreibweise desselben Ausdrucks: Stünde das Muster wörtlich in dieser Datei,
zählte die Befehlszeile sich selbst mit und verfälschte die Kopfzahl um 1. Auf dieser Datei
liefern beide Formen dieselbe Zahl; die Kopfzahl 11 stimmt mit der Ausgabe überein.

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

Kein Befund der Kategorie A: Die harten Sperren der Klasse B sind eingehalten — sieben
Abschnitte in der vorgeschriebenen Reihenfolge, kein Euro-Betrag außerhalb der Maßnahmenkosten,
kein Null-Betrag und kein leeres Feld, keine Schadensfunktion, keine Kalibrierung, keine
Schadenskonten und keine Hochrechnung einer Größenordnung.
