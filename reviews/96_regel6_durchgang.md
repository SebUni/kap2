# #96 Aeroallergene — Regel 6 in einem Durchgang über den ganzen Bericht

Prüfakte zu T-1932-methodik_manager (09.10.2026), getrennt von der Kundenfassung. Gegenstand ist `docs/methodik/96_aeroallergene.md`. Basis-Stand ist Commit `ed0ae1db`; Bericht und Ledger sind von dort mit `git show` geholt. Alle Änderungen erhalten die Zeilenzahl, deshalb ist die Zeilennummer auf Basis- und Endstand dieselbe.

## Grenze

Festlegung des CEO in T-1660-ceo vom 06.10.2026 zu Regel 6 (`.claude/methodik-loop.md`), angewandt wie in T-1790-ceo für #95: Im Bericht bleibt, was als Vorgabe gilt. Das ist, wie gerechnet wird, welche Datenebene das Produkt führt, welcher Anzeigetext erscheint und welcher Wert an die Stelle eines anderen tritt, im Präsens und ohne Zeitbezug auf die Umsetzung. Umsetzungsstand ist jeder Satz, der sagt, was Code oder Produkt heute tun oder noch nicht tun, und jeder Satz, der auf ein Umsetzungsereignis, eine Rolle oder ein Ticket verweist. Solche Sätze werden gestrichen oder zeitlos gefasst; weicht der Code ab, steht ein Ledger-Befund mit Termin und Zuständigem (Regel 7). Im Entscheidungslog und im Block „Revisionsstand“ bleiben Zahlen und Entscheidungen, wie sie galten. Den Statusblock (von `Status:` bis zur ersten Leerzeile) fasst dieses Paket ohne Ticketkennung und ohne Prüfrunde (Festlegung cto in T-1660-ceo, 06.10.2026, 09:31 UTC).

## Suchmuster M und Zählausdruck

Suchmuster M (Python, `re`), wörtlich aus T-1790-ceo:

```
(?i)(im produkt|im code|integration|integriert|nachzug|ratchet|umsetzung|umgesetzt|bis dahin|derzeit|noch nicht|\bcto\b|entwickler|\bT-\d{3,4}\b)
```

Zählausdruck aus T-1790-ceo mit dem Dateinamen von #96, ausgeführt im Wurzelverzeichnis des Produkt-Repos:

```
python3 -c "import re;M=r'(?i)(im produkt|im code|integration|integriert|nachzug|ratchet|umsetzung|umgesetzt|bis dahin|derzeit|noch nicht|\bcto\b|entwickler|\bT-\d{3,4}\b)';print(sum(1 for l in open('docs/methodik/96_aeroallergene.md',encoding='utf-8') if re.search(M,l)))"
```

Ausgabe auf dem Basis-Stand `ed0ae1db`: `89`. Ausgabe auf dem Endstand: `54`.

**n = 54.** Genau 54 Zeilen der Liste tragen die Entscheidung `Vorgabe` oder `Log, Stand von damals`; sie treffen M auf dem Endstand weiter. Die übrigen 35 Treffer sind zeitlos gefasst und treffen M auf dem Endstand nicht mehr. M trifft auch Zeilen, die bleiben (Methodensätze, Quellentitel, Entscheidungslog); deshalb ist die Liste der Nachweis, nicht die Zahl.

## Trefferliste (Basis-Stand ed0ae1db)

Satzanfang: der Satz oder die Tabellenzelle, in dem der erste Treffer der Zeile steht, höchstens 80 Zeichen; ein senkrechter Strich ist als `\|` geschrieben.

| Zeile | Satzanfang | Entscheidung | Begründung |
|---|---|---|---|
| 4 | (T-1238, Ledger-Befunde 152–155), Schritt 2 S158 nach Tagen und Belastung und St | zeitlos gefasst | Statusblock ohne Ticketkennung und Prüfrunde, verweist auf das Ledger (Festlegung cto, T-1660-ceo) |
| 6 | Kennzeichnung der Parameter-Blöcke, Jahresbeträge ohne Abzinsung (T-1240, Log 25 | zeitlos gefasst | Statusblock ohne Ticketkennung und Prüfrunde, verweist auf das Ledger (Festlegung cto, T-1660-ceo) |
| 7 | Schritt 4 Bezugswert Ḡ₀ der Stadtbaumwahl (T-1323, T-1362, Log 26, Befund 182),  | zeitlos gefasst | Statusblock ohne Ticketkennung und Prüfrunde, verweist auf das Ledger (Festlegung cto, T-1660-ceo) |
| 8 | Null-Runde über den ganzen Bericht: A Runde 21 (T-1442-methodik_manager), B Rund | zeitlos gefasst | Statusblock ohne Ticketkennung und Prüfrunde, verweist auf das Ledger (Festlegung cto, T-1660-ceo) |
| 10 | Instruktionsquelle: `docs/AUFGABE_METHODIK_SCHADENSRECHNUNG.md` (v2) · Umsetzung | Vorgabe | „Umsetzungsgrundlage“ benennt den Rechenansatz 96-A, keinen Code-Stand |
| 19 | die Ebenen POLLEN_LOAD (OSM-Vegetation, §3.3), POPULATION_U20 (§3.2) und CANOPY_ | zeitlos gefasst | Datenebenen, die das Produkt führt, ohne Datum der Integration |
| 22 | **Schritt 1 (T-1238):** Rechenkette §3.0 | Log, Stand von damals | Block „Revisionsstand“: datierte Änderungen einer Revision, wie sie galten |
| 24 | **Schritt 2 (T-1239):** S158 wirkt nur an gewarnten Tagen (DWD-Index mindestens  | Log, Stand von damals | Block „Revisionsstand“: datierte Änderungen einer Revision, wie sie galten |
| 27 | **Schritt 3 (T-1240):** Kap. 1 Unterabschnitt | Log, Stand von damals | Block „Revisionsstand“: datierte Änderungen einer Revision, wie sie galten |
| 31 | **Schritt 4 (T-1323, T-1362):** Bezugswert Ḡ₀ der Zentrierung im Ausgangsstand | Log, Stand von damals | Block „Revisionsstand“: datierte Änderungen einer Revision, wie sie galten |
| 34 | **Nachzug (T-1330):** Befunde 183–185 aus Runde 13 — Untergrenze 4,38 Mio. € in  | Log, Stand von damals | Block „Revisionsstand“: datierte Änderungen einer Revision, wie sie galten |
| 36 | **Runde 14 (T-1330):** Befunde 186–194 — Stadtbaumwahl über den Kronenanteil ger | Log, Stand von damals | Block „Revisionsstand“: datierte Änderungen einer Revision, wie sie galten |
| 39 | **Runde 15 (T-1330):** Befunde 195–197 — Stadtbaumwahl mit der vollen Ebenendefi | Log, Stand von damals | Block „Revisionsstand“: datierte Änderungen einer Revision, wie sie galten |
| 41 | Ĝ′ ≥ 0,536 × Grünanteil (§5, Integrationsauflage, Kap. 1 (b), Log 24/26); Berlin | Log, Stand von damals | Block „Revisionsstand“: datierte Änderungen einer Revision, wie sie galten |
| 43 | **Runde 16 (T-1427):** Befunde 199–200 — Abgrenzung in §5.1 auf die Regel nach L | Log, Stand von damals | Block „Revisionsstand“: datierte Änderungen einer Revision, wie sie galten |
| 46 | **Runde 17 (T-1427):** Befunde 201–204 — Sensitivität von p_B/p_G in §3.4 nachge | Log, Stand von damals | Block „Revisionsstand“: datierte Änderungen einer Revision, wie sie galten |
| 49 | **Runde 25 (T-1633):** Befunde 241–245 — Zelllauf §3.0 mit der Ersatzregel des P | Log, Stand von damals | Block „Revisionsstand“: datierte Änderungen einer Revision, wie sie galten |
| 53 | **Runde 26 (T-1634):** Befunde 246–252 — Stadtbaumwahl: s_unbek kommunenweit und | Log, Stand von damals | Block „Revisionsstand“: datierte Änderungen einer Revision, wie sie galten |
| 56 | **Runde 27 (T-1635):** Befund 253 — Kosten der Stadtbaumwahl je Baum als Abschät | Log, Stand von damals | Block „Revisionsstand“: datierte Änderungen einer Revision, wie sie galten |
| 60 | Abfrage des Falls im Produkt (Log 27). Kein Basiswert und kein bestehender Wert  | Log, Stand von damals | Block „Revisionsstand“: datierte Änderungen einer Revision, wie sie galten |
| 62 | **Runde 29 (T-1638):** Befunde 254–257 aus Runde 28 — jeder statistische Fachbeg | Log, Stand von damals | Block „Revisionsstand“: datierte Änderungen einer Revision, wie sie galten |
| 66 | **Runden 30–32 (T-1650, T-1651):** Befunde 258–264 — Klimaanteil \(a_{\text{attr | Log, Stand von damals | Block „Revisionsstand“: datierte Änderungen einer Revision, wie sie galten |
| 72 | Ü-13 beim CTO. | Log, Stand von damals | Block „Revisionsstand“: datierte Änderungen einer Revision, wie sie galten |
| 80 | abnahmereif und ist integriert (Null-Runde: Review Runde 10; Befunde 116–150 beh | Log, Stand von damals | Block „Revisionsstand“: datierte Änderungen einer Revision, wie sie galten |
| 81 | (Null-Runde Runde 3) und ist integriert. | Log, Stand von damals | Block „Revisionsstand“: datierte Änderungen einer Revision, wie sie galten |
| 88 | `default_reduction` bleibt in dieser Revision 0,0 (Code-Nachzug L2 als eigener S | Log, Stand von damals | Block „Revisionsstand“: datierte Änderungen einer Revision, wie sie galten |
| 169 | Der umgesetzte Anpassungsstand steckt über die | Vorgabe | umgesetzte Anpassung als Größe der Methode bzw. Zitat der KWRA [73] |
| 184 | nur bestehende und umgesetzte Anpassungsmaßnahmen als Teil der Sensitivität berü | Vorgabe | umgesetzte Anpassung als Größe der Methode bzw. Zitat der KWRA [73] |
| 219 | Im Produkt rechnen beide Hebel seit der Integration am 27.09.2026 im Zelllauf, a | zeitlos gefasst | beide Hebel rechnen im Zelllauf, ohne Datum der Integration |
| 280 | die §2.8-E-Regeln sind in der Aufgabe noch nicht definiert (Lücken-Vermerk §2.8) | zeitlos gefasst | Lücke der Aufgabe ohne „noch“ |
| 295 | **§3.9 ABGESCHÄTZT**, im Produkt als „Abschätzung von KAP3" gekennzeichnet \| ge | Vorgabe | Register: Ausweis „Abschätzung“ im Produkt (P1, P2) |
| 561 | **Ergebnis der Integration (31.08.2026):** Ebene `POPULATION_U20` **angelegt** — | zeitlos gefasst | Datenebene POPULATION_U20, ohne Integrationsergebnis |
| 562 | der Zensus-Gitterdatensatz „Alter in 5er-Jahresgruppen" liegt bereits im Produkt | zeitlos gefasst | Datenebene POPULATION_U20, ohne Integrationsergebnis |
| 681 | nur die Arten-/OSM-Detailspezifikation ist Integrationsumfang. **Referenzzustand | zeitlos gefasst | Detailspezifikation steht im Bericht, kein Integrationsumfang |
| 693 | Stand nach der Integration, Befund 231): | zeitlos gefasst | Verweis ohne „Stand nach der Integration“ |
| 697 | **Integrationsauflage**: Mit #96 ist **keine** pauschal wirkende Maßnahme verknü | Vorgabe | Integrationsauflage: Regel, wie verknüpft wird (keine pauschale Maßnahme) |
| 699 | Seit der Integration am 27.09.2026 sind zwei Maßnahmen so verknüpft: Die | zeitlos gefasst | zwei verknüpfte Maßnahmen, ohne Datum |
| 706 | die Ebene ist Teil des Integrationsumfangs (Kartenebenen-Pflicht §3.6). | zeitlos gefasst | Ebene im Produkt statt „Teil des Integrationsumfangs“ |
| 707 | **Ergebnis der Integration (31.08.2026; §3.1-Anlagepflicht):** Ebene | zeitlos gefasst | Ebene POLLEN_LOAD, ohne Integrationsergebnis |
| 709 | Integration überlassen): \(\hat G_z = w_B\,[k_{\text{Birke},z} + | zeitlos gefasst | Ebene POLLEN_LOAD, ohne Integrationsergebnis |
| 853 | **Produktverankerung** (Integration 31.08.2026): Maßgeblicher Produktwert ist | zeitlos gefasst | Produktverankerung von c_Tag ohne Datum der Integration |
| 948 | noch nicht ausgewertet; Quelle DWD-Pollenflugstatistik [71]; wird über \(m_{g,V} | zeitlos gefasst | „im Bericht nicht ausgewertet“ statt „noch nicht“ (Datenlage) |
| 1010 | Registry-Vermerk vor Integration). | zeitlos gefasst | Registry-Vermerk ohne „vor Integration“ |
| 1159 | a = dk / k                                   # Eingabe anteil_ersetzt im Produkt | Vorgabe | Eingabefeld anteil_ersetzt (Andockpunkt) |
| 1261 | über \(\hat G'\), nie als pauschaler Faktor (Integrationsauflage unten). | Vorgabe | Verweis auf die Integrationsauflage (Regel) |
| 1425 | **Im Produkt** führt die Katalogmaßnahme heute keine Kosten (Befund 253). Nach d | zeitlos gefasst | „Vorgabe für das Produkt“: Abfrage des Falls und Kosten je Baum; Abweichung im Code führt Befund 253 |
| 1510 | **Produktstand, ehrlich benannt (seit der Integration am 27.09.2026, Befund 230) | zeitlos gefasst | Mangel 15: „Produktstand, ehrlich benannt“ als „Vorgabe für das Produkt (Befund 230)“; Folgezeile 230 |
| 1512 | Kommune zeichnet die Zellen als Geometrie der Maßnahme und gibt einen Anteil \(a | Vorgabe | Eingabefeld anteil_ersetzt (Andockpunkt) |
| 1552 | trägt ein älterer Ausgangslauf den Wert noch nicht, rechnet | Vorgabe | Anzeigeregel bei älterem Ausgangslauf (Hinweis neben dem Betrag) |
| 1558 | **Integrationsauflage (Stadtbaumwahl)**, im | Vorgabe | Integrationsauflage Stadtbaumwahl: Regel, was die Rechnung braucht |
| 1560 | Faktor): Der CTO braucht (1) die vom Nutzer gewählten Zellen, (2) als Eingabe di | zeitlos gefasst | „Die Rechnung braucht“ statt „Der CTO braucht“ |
| 1601 | Ergebnis-Sensitivität), die im Produkt als „Abschätzung von KAP3" mit Herleitung | Vorgabe | Anzeigetext „Abschätzung von KAP3“ (P1) |
| 1632 | **An welchen Tagen und ab welcher Belastung die Warnung wirkt (Festlegung, T-123 | zeitlos gefasst | Verweis auf Log 23/24 statt Ticketkennung |
| 1711 | im Produkt ist \(A_{\text{Zelle}}\) der Deckungsgrad | Vorgabe | A_Zelle ist der Deckungsgrad (Andockpunkt) |
| 1782 | Basiswert bei flächendeckender Umsetzung **≈ 1,3 Mio. € je Jahr** vermiedener Be | Vorgabe | flächendeckende Umsetzung der Maßnahme (Annahme der Rechnung) |
| 1789 | # S158 nach Tagen und Belastung (T-1239), Beispielkommune Berlin wie Rechenkette | zeitlos gefasst | Kommentar der Anlage mit Log 23 statt Ticketkennung |
| 1864 | - **Kommune mit 100.000 Einwohnern im Bundes-Altersmix** (Beispielgröße im Produ | Vorgabe | Beispielgröße im Produkttext (Anzeigetext) |
| 1884 | Satz im Produkt (Katalog, Feld `sensitivitaet` der Frühwarnung), die Maßnahme tr | zeitlos gefasst | Katalogtext gibt den Absatz wieder, ohne „das Produkt übernimmt“ |
| 1932 | **Integrationsauflage (S158).** Der CTO verknüpft die Maßnahme nach der Abnahme  | Vorgabe | Überschrift Integrationsauflage bleibt als Regel; Satz ohne „der CTO verknüpft“ gefasst |
| 1948 | **Produktstand (seit 27.09.2026, Befund 231).** Der CTO hat die Rechnung im Zell | zeitlos gefasst | „Verknüpfung im Zelllauf (Befund 231)“ statt Produktstand mit Datum; Folgezeile 231 |
| 1958 | vollständig umgesetzt: Den Ersetzungspfad aus Punkt 2 hat das Produkt nur als Fo | zeitlos gefasst | Ersetzungspfad als Vorgabe mit Modellgrenze 8 (Befund 233), Euro je Zelle (Befund 237) |
| 1980 | bis dahin ist die Kette oben der vollständige Nachweis des Werts. | zeitlos gefasst | „ohne diese Daten“ statt „bis dahin“ (Datenlage) |
| 1992 | (Befunde 151 und 156, nach der Integration die Befunde ab 230), nicht still (Eis | zeitlos gefasst | Befundverweis ohne „nach der Integration“ |
| 2003 | Die Diskontrate für mehrjährige Rechnungen legt T-1116 fest. | zeitlos gefasst | Diskontrate ohne Ticketkennung |
| 2052 | neu gefasst mit T-1239): Seit der Festlegung wirkt die Warnung nur an gewarnten  | zeitlos gefasst | Modellgrenze 8 mit Log 23/24 statt Ticketkennung |
| 2074 | der Integrationsauflage (S158) in §5.1. | Vorgabe | Verweis auf die Integrationsauflage S158 (Regel) |
| 2191 | # Baustein der Ebene POLLEN_LOAD (Detailspezifikation der Integration, §3.3). | zeitlos gefasst | Kommentar in Kapitel 7: Detailspezifikation in §3.3 |
| 2214 | # (Integrationsauflage S158 in §5.1; Ledger-Befunde 151, 178, 215, 231). | Vorgabe | Kommentar in Kapitel 7: Verweis auf die Integrationsauflage (Regel) |
| 2229 | # Anteil gewarnter Zusatztage fuer S158 (T-1239): Tage mit DWD-Pollenflug- | zeitlos gefasst | Kommentar in Kapitel 7 mit Log 23 statt Ticketkennung |
| 2320 | 8) — deterministisch über die `sources.py`-Ratchet- | zeitlos gefasst | Archiv-Snapshots ohne Ratchet-Mechanik und „bis dahin“ |
| 2321 | Mechanik bei Integration; bis dahin sind DOI-/amtliche Links die persistenten Re | zeitlos gefasst | Archiv-Snapshots ohne Ratchet-Mechanik und „bis dahin“ |
| 2483 | im Bericht noch nicht | zeitlos gefasst | Quelle [71]: „der Bericht wertet sie nicht aus“ statt „noch nicht“ |
| 2499 | bestehende und umgesetzte Anpassung im Zustand ohne Anpassung; optimistischer un | Vorgabe | bestehende und umgesetzte Anpassung als Größe der Methode |
| 2527 | Infrastrukturpolitik in Hamburg – Sachstände, Kosten und konkrete Umsetzung“, An | Vorgabe | Quellentitel, Adresse oder wörtliches Zitat einer Quelle |
| 2530 | https://www.buergerschaft-hh.de/parldok/dokument/105068/23_05166_umwelt_klima_un | Vorgabe | Quellentitel, Adresse oder wörtliches Zitat einer Quelle |
| 2531 | Permalink https://web.archive.org/web/20260929162705/https://www.buergerschaft-h | Vorgabe | Quellentitel, Adresse oder wörtliches Zitat einer Quelle |
| 2543 | 6 (PDF-Seite 7): „Im Rahmen der Stadtbaumkampagne kostet derzeit eine | Vorgabe | Quellentitel, Adresse oder wörtliches Zitat einer Quelle |
| 2601 | **Einträge 21–22: Fortschreibung 7 (25.09.2026, T-1238)** — Kapitel 9 entfällt ( | Log, Stand von damals | Präambel des Entscheidungslogs: datierte Einträge, wie sie galten |
| 2603 | **Einträge 23–24: Fortschreibung 7, Schritt 2 (26.09.2026, T-1239)** — S158 nach | Log, Stand von damals | Präambel des Entscheidungslogs: datierte Einträge, wie sie galten |
| 2605 | **Eintrag 25: Fortschreibung 7, Schritt 3 (26.09.2026, T-1240)** — Kennzeichnung | Log, Stand von damals | Präambel des Entscheidungslogs: datierte Einträge, wie sie galten |
| 2607 | 4 (26.09.2026, T-1362)** — Bezugswert Ḡ₀ im Ausgangsstand festgehalten; | Log, Stand von damals | Präambel des Entscheidungslogs: datierte Einträge, wie sie galten |
| 2609 | **Eintrag 27: Runde 27 (29.09.2026, T-1635)** — Kosten der Stadtbaumwahl nach Vo | Log, Stand von damals | Präambel des Entscheidungslogs: datierte Einträge, wie sie galten |
| 2621 | J30-KKR-Anker bei Integration interaktiv ziehen (Registry-Vermerk) \| kein Fit-S | Log, Stand von damals | Zeile des Entscheidungslogs, Entscheidung wie sie galt |
| 2634 | die Produktmechanik (measure_service skaliert gespeicherte Outcomes) ist KEIN Be | Log, Stand von damals | Zeile des Entscheidungslogs, Entscheidung wie sie galt |
| 2635 | 3 zunächst 0,0 (Code-Nachzug L2 nach der P1-Kennzeichnung; überholt, heutiger Co | Log, Stand von damals | Zeile des Entscheidungslogs, Entscheidung wie sie galt |
| 2639 | Im Produkt rechnet sie seit dem 27.09.2026 als Katalogmaßnahme im Zelllauf nach  | Log, Stand von damals | Zeile des Entscheidungslogs, Entscheidung wie sie galt |
| 2641 | **Festhalten (Weg (a), Festlegung CMO in T-1323):** Ḡ₀ = betroffenengewichtetes  | Log, Stand von damals | Zeile des Entscheidungslogs, Entscheidung wie sie galt |
| 2642 | im Produkt Abfrage des Falls ohne stille Vorgabe (Ü-11); Amortisation der Nachpf | Log, Stand von damals | Zeile des Entscheidungslogs, Entscheidung wie sie galt |
| 2643 | **Beide Vergleiche beim selben \(a_{\text{attr}}\)** (Festlegung des methodik_ma | Log, Stand von damals | Zeile des Entscheidungslogs, Entscheidung wie sie galt |

## Ohne Treffer gefunden

Zeilen ohne Treffer von M, die Umsetzungsstand trugen und im selben Zug zeitlos gefasst sind:

| Zeile | Änderung |
|---|---|
| 3 | Statusblock: Aufzählung der Schritte durch Verweis auf den Block „Revisionsstand“ ersetzt |
| 5 | Statusblock: wie Z. 3 |
| 220 | Verweis „Produktstand in §5.1 und §5, Befunde 230 und 231“ entfällt |
| 705 | „Bis zur Anlage der Ebene“ entfällt |
| 708 | „angelegt“ und „vom Bericht der Integration überlassen“ entfallen |
| 1426 | „Nach der Übernahme Ü-11“ entfällt |
| 1511 | „sichtbar“ als Produktstand entfällt |
| 1556 | „Vor Ü-10 mischte das Produkt …“ als Bedingung gefasst |
| 1885 | „das Produkt übernimmt diesen Absatz“ entfällt |
| 1933 | „Er braucht dafür“ als „Die Rechnung braucht dafür“ |
| 1936 | „heute führt die Schicht-B-Funktion nur ihre Summe“ als Vorgabe „nicht nur ihre Summe“ |
| 1957 | „Zwei Punkte sind nicht vollständig umgesetzt“ entfällt |
| 1960 | „gibt es nicht aus (Befund 237)“ und „mit den heutigen Werten“ entfallen |

## Selbstprüfung

Erzeugt per Skript. Geprüft: Jede Zeile mit Treffer auf dem Basis-Stand hat genau eine Entscheidung; jede Zeile mit `Vorgabe` oder `Log, Stand von damals` trifft M auf dem Endstand; keine andere Zeile trifft M auf dem Endstand; ihre Zahl ist gleich der Ausgabe des Zählausdrucks (54).
