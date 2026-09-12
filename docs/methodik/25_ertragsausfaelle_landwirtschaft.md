# Methodik-Bericht #25 — Ertragsausfälle (Landwirtschaft)

Status: **Erstaufschlag (`/neu-risiko 25`) — noch nicht gegengeprüft** · 12.09.2026 ·
Instruktionsquelle: `docs/AUFGABE_METHODIK_SCHADENSRECHNUNG.md` (v2) · Umsetzungsgrundlage: **offen**
(Ansatz-Vergleich Kap. 9) · Familie: **K6-Ertrag (Mengeneffekt Pflanze) — noch kein abgenommener
Prototyp, dieser Bericht ist der erste Vertreter** (§2.6; Entscheidungslog Nr. 2)

> **Geltungsbereich des Erstaufschlags.** Befüllt sind Kap. 1 (Wirkungskette, Knoten-Bilanz,
> Weitergaben, Konto) und Kap. 2 (Evidenz-Register-Skelett) aus den beiden Arbeitsmappen unter
> `docs/Schadensbaum/`; Kap. 3–9 tragen die Pflichtinhalte als Kommentar. Einzige bezifferte
> Größe ist die P2-Abschätzung zum Maßnahmen-Hebel S027 (§5.1, `#s027-wirkung`), ausdrücklich als
> **Abschätzung von KAP3** gekennzeichnet. Alle übrigen Entscheidungen stehen auf `offen`.
> Befund-Ledger: `reviews/BEFUNDE_25.md` (leer).

## Ergebnis

- **Slug:** `25_ertragsausfaelle_landwirtschaft`. **Registerzeilen:** 31 (`25-<Knoten>-01`), gespiegelt in `docs/evidenz/register.md`.
- **Offen:** (1) alle 31 Entscheidungen; (2) Ergebnisgröße und Ansatz (Kap. 9); (3) Datenebenen nach §3.1 (Anbaufläche/Fruchtarten, Deckungsbeiträge, Bodenwasser); (4) R9-Partition in K6 gegenüber #26 (Preis), #19 (Bestand, R1), #20 (Tier) und dem K6-Zweig von #47; (5) Ausgangskante 25 → 20 (Abgleich P19): Wirkungsweg und Doppelzählungsschutz sind in den Mappen nicht beziffert; (6) Mon. Z26 (#21) nennt als Ziele „Menge (ID 26) und Qualität (ID 27)“ — gegen NW Z26/Z27 um eins verschoben, wörtlich übernommen, nicht korrigiert (eiserne Regel 2).
- **Meilenstein M1:** Die Knoten-Bilanz (Abschnitt „Zehn Treiber, ein Sammelpunkt“) beantwortet die Ticket-Frage: **alle zehn Eingänge (Rolle „Treiber (0 €)“) erreichen ihren Euro über #25**; für #13, #21 und #23 ist #25 der einzige Mengen-Euro-Weg, #56 hängt über die R7-Weiche daran.
- **Aufwand Erstaufschlag:** 0 Nacharbeitsrunden (eine Session, 11 Werkzeugaufrufe). Keine Websuche, also keine externe Evidenz.
- **Planung:** Gegenprüfung, Revision, Integration und PDF-Export sind nicht Teil des Tickets.

## 1 Wirkungskette & Knoten-Bilanz (§2.1)

**Rolle (Rollen-Check, Schritt 2):** Sheet „Schadensbaum-Netzwerkliste“ Z26 (Id 25):
**Buchungsobjekt — Ebene A**, Feld Landwirtschaft, Handlungserfordernis **sehr dringend**,
Input-Kanten **1; 10; 11; 13; 15; 21; 22; 23; 24; 56**, Output-Kante **20**, Konto
**K6 Land-, Forst- & Fischereiproduktion**, Baustein **K6-Mengeneffekt Pflanze**, Anmerkung
„Sammel-Buchungsobjekt (R9)“. Kein Abbruch nach R2/R3 — Konto und Baustein sind wörtlich aus NW Z26
übernommen, nicht selbst gewählt.

**W-Knoten:** Sheet „Klimawirkungsketten“ Z119, Knoten **W052 „Ertragsausfälle“**, Container
„Ertrag und Qualität der Ernteprodukte“, Konfidenz **mittel** (Sensitivitäts- und Sammelpfeil enden
laut Anmerkung am Container, nicht am Sechseck; nach Regel 3/5 expandiert). **W052 hat keinen
direkten klimatischen Einfluss** — die Anmerkung hält ausdrücklich fest, dass der Einflusspfeil
„CO2-Konzentration“ (E21) allein das Nachbar-Sechseck W051 „Durchschnittlicher Ertrag“ (Z118)
trifft. Das gesamte Klimasignal von #25 kommt also über die vorgelagerten W-Knoten; ein zusätzlicher
direkter Klimaterm wäre ein Doppelkanal (§3.2).

### Knoten-Bilanz

Spalte „rechnet in“ ist im Erstaufschlag durchgängig `offen`. Die Spalte „Vorschlag“ nennt nur, was
die Arbeitsmappen selbst hergeben (Blatt + Zeile); sie ist keine Entscheidung.

| Knoten | Name | Blatt/Zeile | rechnet in | Vorschlag laut Arbeitsmappe |
|---|---|---|---|---|
| W003 | Wassermangel im Boden (= Id 13) | KWK Z40; NW Z14 | offen | Leitkanal Trockenheit: Id 13 ist „Treiber (0 €)“, Mon. Z18 „Wirkt über Ertragsausfälle (K6) bzw. Produktionsfunktions-Kapitalisierung“ (R1/R3) — Kandidat für die physische Zwischengröße (Bodenwasserdefizit in der Vegetationsperiode) |
| W004 | Vernässung (= Id 15) | KWK Z41; NW Z16 | offen | Id 15 „Treiber (0 €)“, Mon. Z20 „Bewirtschaftungsausfälle über K6; Bauschäden über Gebäude-Endpunkte“ — Partition gegen den K6-Zweig von #47 offen (offener Punkt 4) |
| W044 | Stress durch Schädlinge und Krankheiten (= Id 24) | KWK Z111; NW Z25 | offen | Mon. Z29 „Ertrags-/Qualitätswirkung über K6; Mehraufwand Pflanzenschutz als K8 (Entweder-oder …)“ — R7-Weiche, Ertragsteil hier |
| W045 | Abiotischer Stress (= Id 21) | KWK Z112; NW Z22 | offen | Mon. Z26 „Wirkt über Menge (ID 26) und Qualität (ID 27)“ — die Mappe ist hier um eins verschoben (Menge = Id 25, Qualität = Id 26 laut NW Z26/Z27); wörtlich übernommen, Befund offen (R3) |
| W046 | Agrophänologische Phasen und Wachstumsperiode (= Id 23) | KWK Z113; NW Z24 | offen | Mon. Z28 „Wirkt über Menge/Qualität; Frostrisikoverschiebung ebenfalls“ (R3) — Kandidat für die Szenario-Verschiebung der Anbauperiode (Kap. 6) |
| W047 | Verschiebung von Anbaugebieten (= Id 22) | KWK Z114; NW Z23 | offen | Mon. Z27 „Umstellungs-/Investitionskosten als K8, dauerhafte DB-Differenzen über K6. Kann Chance sein (negativer Schaden)“ — R8-Vorzeichen, R1 gegen Umstellungskosten |
| W048 | Anbau neuer Sorten | KWK Z115 | offen | Knoten der W052-Kette, aber **keine** Input-Kante in NW Z26; Anpassungsreaktion — Kandidat „bewusst inaktiv“ bzw. Maßnahmen-Hebel (Sortenwahl), keine Bewertung in der Mappe |
| W096 | Bewässerungswasser (= Id 56) | KWK Z219; NW Z57 | offen | Mon. Z61: „ENTWEDER Ertragsausfall unbewässerter Flächen (ID 25) ODER Mehrkosten der Ersatzwasserbeschaffung (K8) je Fläche — die Anteile ergänzen sich zu 100 %“ (R7) |
| W017 | Filter-/Pufferfunktionen (Wasser, Schadstoffe) | KWK Z54 | offen | Bodenfunktion, keine Input-Kante in NW Z26; nicht-marktliche Seite → K7 (Konten Z52: „nicht-marktliche Leistungen (→K7)“) — Kandidat „bewusst inaktiv“ |
| W019 | Produktionsfunktionen (Standortstabilität, Bodenfruchtbarkeit) (= Id 19) | KWK Z56; NW Z20 | offen | Mon. Z24: „Dauerhafte Fruchtbarkeitsminderung = kapitalisierter Ertragsverlust (Barwert) — die Bestandsbuchung des Kontos K6“; **R1 erzwingt Entweder-oder gegen #25 (Strom)** |
| W020 | Nährstoffspeicherfunktionen (C, N) | KWK Z57 | offen | wie W017; CO2 aus Böden wird nach R10 nachrichtlich geführt — Kandidat „bewusst inaktiv“ |
| W009 | Bodenerosion durch Wasser (= Id 10) | KWK Z46; NW Z11 | offen | Input-Kante laut NW Z26, **nicht** in der W052-Eingangsliste (Container „Erosion“) — Mon. Z15 „On-site: Ertrags-/Fruchtbarkeitsverlust über K6 (Regel R1). Off-site … (K4), Gewässerbelastung (K7)“; off-site-Anteil nicht hier |
| W010 | Bodenerosion durch Wind (= Id 11) | KWK Z47; NW Z12 | offen | wie W009 — Mon. Z16 „Wie Wassererosion: on-site über K6, off-site Räumungs-/Reinigungskosten als K4-Endpunkt“ |
| W021 | Länge der Vegetationsperiode (= Id 1, Teil 1) | KWK Z71; NW Z2 | offen | Input-Kante laut NW Z26; Mon. Z6 „Wirkt auf Agrarproduktion (K6), Pollensaison (K1) und Ökosystemleistungen (K7)“ (R3) — K1-Teil gehört zu #96 |
| W022 | Phänologie (= Id 1, Teil 2) | KWK Z72 | offen | Eingang von W046/W047 (KWK Z113/Z114); erreicht #25 damit zweifach (direkt über Id 1 und über die Agrophänologie-Knoten) — Kein-Doppelkanal §3.2 zu entscheiden |
| S021 | Bodenart und Bodentyp | KWK Z92 | offen | Vulnerabilität (Container „Bodeneigenschaften“, Regel 3) — Kandidat für die Wasserhaltefähigkeit der Zelle |
| S022 | Bodenfruchtbarkeit | KWK Z93 | offen | Niveau des Ertragspotenzials; Bestandsseite über #19/R1 (Mon. Z24) |
| S023 | Wasserrückhaltekapazität | KWK Z94 | offen | wie S021; Doppelkanal zu W003 prüfen, falls das Bodenwasserdefizit die Kapazität schon enthält |
| S024 | Infiltrationskapazität | KWK Z95 | offen | wie S023; wirkt zugleich auf W004/W009 |
| S025 | Anbaufrucht | KWK Z96 | offen | **Bandzuordnung** der Deckungsbeiträge und der Stresstoleranz (Mon. Z30: „Deckungsbeitrag je ausgefallener Einheit“) |
| S026 | Tierart | KWK Z97 | offen | pauschal über den Container eingetragen (Regel 3); Tierseite bucht #20 (K6-Tierleistung, NW Z21) — Kandidat „bewusst inaktiv“ |
| S027 | Bewässerung | KWK Z98 | offen | Kandidat **Maßnahmen-Hebel** (Wasserspeicher, effiziente Bewässerung); P2-Abschätzung §5.1; R7-Weiche mit #56 (Mon. Z61) |
| S028 | Art der Bewirtschaftung (Dauerkultur, Fruchtfolgen, etc.) | KWK Z99 | offen | Kandidat Vulnerabilität/Hebel; Evidenz und Zellgröße offen |
| S029 | Dünger- und Pestizideinsatz | KWK Z100 | offen | Mehraufwand Pflanzenschutz ist K8 (Mon. Z29, R7) — hier nur die Ertragswirkung |
| S030 | Züchterischer Fortschritt | KWK Z101 | offen | Trendgröße des Referenzertrags (Kalibrierung Kap. 4: Anker-Zeitreihe ohne Züchtungstrend) |
| S031 | Möglichkeiten der Veterinärmedizin | KWK Z102 | offen | pauschal über den Container (Regel 3); Tierseite → #20 — Kandidat „bewusst inaktiv“ |
| S032 | Vorhandensein von Hagelschutz | KWK Z103 | offen | Mon. Z30 nennt Hagel ausdrücklich im Gegenstand („Spätfrost, Hagel, Dürre“); Kandidat Hebel, Bauform-Grenze Dauerkulturen |
| R05 | Vorkommen von landwirtschaftlicher Nutzfläche | KWK Z105 | offen | **Mengengerüst** (ha je Zelle); Lackmustest §3.1: Kommune ohne Nutzfläche → ~0 |
| R06 | Vorkommen von Anbauart | KWK Z106 | offen | Mengengerüst-Aufteilung auf Fruchtarten (Bandzuordnung zu S025) |
| R07 | Vorkommen von Tierhaltung | KWK Z107 | offen | Tierseite → #20 (NW Z21); Futterausfälle sind laut Mon. Z25 „bereits Pflanzenkonto ID 25“ — hier nur als Ausschluss relevant |
| R08 | Vorkommen von landwirtschaftlicher Infrastruktur | KWK Z108 | offen | Bewässerungs- und Speicherinfrastruktur als Träger von S027; Bauschäden → Gebäude-Endpunkte (Mon. Z20) |

KWK = Sheet „Klimawirkungsketten“, NW = „Schadensbaum-Netzwerkliste“, Mon. = „Risiken-Monetarisierung“
(Blattzeile), Konten = „Schadenskonten-System“, RR = „Rechenregeln“. Zusätzlich, kein Knoten der
W052-Kette: W051 „Durchschnittlicher Ertrag“ (KWK Z118, derselbe Container, trägt den Einfluss E21
CO2-Konzentration) und W091 „Grundwasserstand“ (KWK Z214 = Id 55, Eingang von W003/W004).

### Zehn Treiber, ein Sammelpunkt (Ticket-Frage zum Meilenstein M1)

Die zehn Input-Kanten aus NW Z26 sind in der Bilanz vollständig abgebildet; jede trägt in der
Netzwerkliste die Rolle **„Treiber (0 €)“** und in der Monetarisierung die Rolle „Treiber (0 €)“ mit
Konto „keine eigene Buchung“. Ihr Euro entsteht ausschließlich an Endpunkten (R3, RR Z5):

| Treiber (NW/Mon.) | Euro-Weg laut Mappe | erreicht #25? | weitere Endpunkte |
|---|---|---|---|
| 1 Länge der Vegetationsperiode/Phänologie (Z2/Z6) | Mon. Z6 | ja (K6) | #96 (K1), K7 |
| 10 Bodenerosion durch Wasser (Z11/Z15) | Mon. Z15 | ja (on-site K6) | K4 off-site (Direktbuchung „K4-Betriebsmehrkosten“, NW Z11), K7 |
| 11 Bodenerosion durch Wind (Z12/Z16) | Mon. Z16 | ja (on-site K6) | K4 off-site (NW Z12) |
| 13 Wassermangel im Boden (Z14/Z18) | Mon. Z18 | **ja — einziger Euro-Weg neben #19/R1** | — |
| 15 Vernässung (Z16/Z20) | Mon. Z20 | ja | Gebäude-Endpunkte |
| 21 Abiotischer Stress (Z22/Z26) | Mon. Z26 | **ja — einziger Euro-Weg** (Menge) | #26 (Qualität) |
| 22 Verschiebung von Anbaugebieten (Z23/Z27) | Mon. Z27 | ja (DB-Differenz) | K8 Umstellungskosten (NW Z23) |
| 23 Agrophänologische Phasen (Z24/Z28) | Mon. Z28 | **ja — einziger Euro-Weg** (Menge) | #26 (Qualität) |
| 24 Schädlinge/Krankheiten Pflanzen (Z25/Z29) | Mon. Z29 | ja | K8 Pflanzenschutz (R7), #26, #20 |
| 56 Mangel an Bewässerungswasser (Z57/Z61) | Mon. Z61 | **ja — R7-Komplement** | K8 Ersatzwasser |

**Antwort:** Ja, der Befund „zehn Treiber, fünf Buchungsobjekte“ trägt für das
Landwirtschafts-Cluster. Alle zehn Eingänge bekommen ihren Euro über #25; für #13, #21 und #23 ist
#25 der Mengen-Euro überhaupt (bei #21/#23 daneben nur der Preis-Euro in #26, bei #13 daneben nur
die Bestandsseite #19 unter R1), und #56 ist über die R7-Weiche komplementär an #25 gebunden. Kein
Treiber braucht einen eigenen Bericht; was jeder braucht, ist **eine Kante auf #25** samt Attribution
(R3: „Attribution auf Treiber ist zulässig (Anteile), Addition nicht“). Nicht über #25 laufen nur
die ausdrücklich anderen Konten: die Off-site-Erosion (#10/#11 → K4), die Umstellungskosten (#22 →
K8), der Pflanzenschutz-Mehraufwand (#24 → K8), das Ersatzwasser (#56 → K8) und die Pollenseite
(#1 → K1/#96). Der Vollständigkeitsanspruch von M1 ist damit erfüllt, ohne zehn weitere Berichte.

### Weitergaben (zweispaltig; Quelle: Netzwerkliste + Abgleich-Protokoll)

| Output-Kanten (Netzwerkliste / Abgleich-Protokoll mit Punkt-Nr.) | Konto-Ausschlüsse / verwandte Buchungen (Konten-Definition, Monetarisierung) |
|---|---|
| **25 → 20** — NW Z26 Output-ID 20; Abgleich-Protokoll **P19** (Blatt Z33), Art **„Buchungsobjekt→Buchungsobjekt“**; Mon. Z30 Spalten „[Abgleich] → 20“ und „→ 20 (P19)“. Ziel: #20 „Hitzestress bei und Leistung von Nutztieren“ (NW Z21, Buchungsobjekt Ebene B, K6, Baustein K6-Tierleistung). **Gegenrichtung ausgeschlossen:** Mon. Z25 (#20) „Nicht enthalten: … Futterausfälle (bereits Pflanzenkonto ID 25)“ — der Futter-Mengenverlust bleibt in #25 und wird in #20 **nicht** erneut gebucht. **Kein Euro-Transport:** Die Kante ist im gleichen Konto (K6) gezogen; unter R9 („Innerhalb eines Kontos zählt jede Einheit … genau einmal“) darf sie nur als physische Kopplung (weniger/teureres Futter → Leistung der Tiere) wirken, nicht als Summand. Beziffert ist sie in keiner Mappe — **offener Punkt 5**. Parallelkante desselben Punkts: 26 → 20 (Z34), dazu 24 → 20 (Z32, Art „Kante“). **Eingehend:** die zehn Kanten aus NW Z26 (Originalkanten); „Ergänzte Kanten aus Abgleich (eingehend)“ ist leer. | **K6 enthält** (Konten Z50): „Deckungsbeiträge der Primärproduktion: Pflanze (**Menge ID 25** · Preis ID 26), Tier (ID 20), Holz (ID 31), Fang …; Bestandsseite über R1 (Produktionsfunktionen, kapitalisiert). — Enthält die gesamte Outputlücke des Primärbetriebs einschließlich arbeitsbedingter Anteile, wenn die Natur der bindende Engpass ist (R11).“ **K6 schließt aus** (Z52): „Preis-Transfers (R5) · nicht-marktliche Leistungen (→K7)“. **#25 schließt aus** (Mon. Z30): „Qualitätsabschläge (ID 26); dauerhafte Bodenverschlechterung (ID 19, R1); Preisänderungen als Transfers (R5).“ **Partitionsregel-Zitate, K6 geteilt (sechs Buchungsobjekte, Konten Z53: 20 · 25 · 26 · 31 · 37 · 47):** #26 (Mon. Z31) „Nicht geerntete Mengen (ID 25) — Menge und Preisabschlag sind disjunkt“ · #19 (Mon. Z24) „KERNREGEL R1: Für dieselbe Ursache und Fläche ENTWEDER Jahres-Ertragsausfall (ID 25, Strom) …“ · #20 (Mon. Z25) „Futterausfälle (bereits Pflanzenkonto ID 25)“ · R9 (RR Z11) „Sammel-Buchungsobjekte bündeln Mehrfach-Treiber (Ertragsausfälle, …); innerhalb eines Kontos zählt jede Einheit (… Tonne …) genau einmal“ · R11 (RR Z13) Engpassregel gegen K2/K5 desselben Betriebs · Lesebeispiel Konten Z31: „Bodenerosion, Wassermangel, Schädlinge und Frost sind Treiber — sie erhalten 0 € und wirken auf die zwei Buchungsobjekte Ertragsausfälle (ID 25, Menge) und Qualität (ID 26, Preisabschlag).“ **Ohne Partitionsregel in der Mappe (offen):** der K6-Zweig von **#47** (NW Z48, Baustein „K6-Mengeneffekt Pflanze“, Mon. Z52 — vernässte Niederungsfläche; `docs/methodik/47_entwaesserung_kuestenniederungen.md` Kap. 1 hält die Partition gegen #25 ausdrücklich offen) und **#31** Holzertrag (K6, Waldfläche statt Nutzfläche). |

### Konto-Einbettung

- **Konto:** K6 Land-, Forst- & Fischereiproduktion — wörtlich aus NW Z26; Definition (Konten Z50)
  siehe oben. Kostensatz-Typ (Z51): „Deckungsbeitrag je Einheit · Bestandswert-/Barwertansatz“.
- **Bewertungsbaustein:** **K6-Mengeneffekt Pflanze** (wörtlich NW Z26). Bewertungsansatz (Mon. Z30):
  „Deckungsbeitrag je ausgefallener Einheit (nicht Umsatz!): Menge × (Erlös − variable Kosten).
  SAMMEL-BUCHUNGSOBJEKT der pflanzlichen Mengenverluste — alle Treiber (Trockenheit, Erosion,
  Schädlinge, Frost …) wirken hierüber.“ Gegenstand (Mon. Z30): „Witterungsbedingte Mengenverluste
  der pflanzlichen Erzeugung im Jahr.“ Beschreibung (Mappenspalte E): „… (Spätfrost, Hagel, Dürre)
  einschließlich der ökonomischen Folgen bis zur Existenzgefährdung von Betrieben.“
- **Rechenregeln:** **R1, R4, R5, R9** (Mon. Z30, Spalte „Regeln“) — R1 Bestand oder Strom (RR Z3,
  Gegenstück #19), R4 Wertschöpfung statt Umsatz (RR Z6, Deckungsbeitrag statt Erlös), R5 Transfers
  (RR Z7, Preisänderungen), R9 ein Schaden/ein Konto/eine Buchung (RR Z11, Sammel-Buchungsobjekt).
  Zusätzlich einschlägig, aber nicht in der Regelspalte: **R11** Engpassregel (RR Z13, K6 vorrangig
  vor K2/K5) und **R8** Chancen mit Vorzeichen (RR Z10; Mon. Z27 zu #22: „Kann Chance sein“) —
  offener Punkt 4.
- **Handlungserfordernis:** sehr dringend (Mon. Z30, NW Z26).
- **Nur K6-Menge aktiv:** Preisabschläge (#26), Bestandsverlust des Bodens (#19), Tierleistung (#20),
  Off-site-Erosion (K4), Umstellungs-, Pflanzenschutz- und Ersatzwasserkosten (K8) sowie
  nicht-marktliche Bodenfunktionen (K7) sind nicht enthalten — Untergrenze, im Infokasten zu
  benennen (§3.6).

## 2 Evidenz-Register (§2.2)

Skelett mit einer Zeile je Knoten der Bilanz. Die Zeilen sind in `docs/evidenz/register.md`
gespiegelt. **Wiederverwendbare Zeilen fanden sich dort nicht:** Das Register führt bisher K1-Zeilen
(#95/#96/#98) und die Skelette von #60/#61/#50/#47 — keine Zeile mit einem agrarischen
Ertrags-Outcome; der gemeinsame Knoten-Typ mit #47 (K6-Mengeneffekt) hat dort das Outcome
„vernässte Niederungsfläche“, nicht „Mengenverlust je Fruchtart“. In Formeln (§3) dürfen später nur
Zeilen mit Entscheidung **Basiswert** stehen.

| Register-ID | Knoten → Outcome | Effektgröße | Studientyp | Quelle | Übertragbarkeit | Datenlage je Zelle | Entscheidung |
|---|---|---|---|---|---|---|---|
| 25-W003-01 | W003 Wassermangel im Boden → Mengenverlust je Fruchtart | offen | offen | offen (Mon. Z18) | offen | offen — Datenebene nach §3.1 zu spezifizieren | offen |
| 25-W004-01 | W004 Vernässung → Mengenverlust / Bewirtschaftungsausfall | offen | offen | offen (Mon. Z20) | offen | offen — Datenebene nach §3.1 | offen |
| 25-W044-01 | W044 Schädlinge und Krankheiten → Mengenverlust | offen | offen | offen | offen | offen | offen |
| 25-W045-01 | W045 Abiotischer Stress (Hitze, Spätfrost, Hagel) → Mengenverlust | offen | offen | offen | offen | offen | offen |
| 25-W046-01 | W046 Agrophänologische Phasen → Mengenverlust | offen | offen | offen | offen | offen | offen |
| 25-W047-01 | W047 Verschiebung von Anbaugebieten → Deckungsbeitrags-Differenz | offen | offen | offen | offen | offen | offen (Vorschlag: R8-Vorzeichen) |
| 25-W048-01 | W048 Anbau neuer Sorten → Mengenverlust | offen | offen | offen | offen | offen | offen (Vorschlag: bewusst inaktiv / Hebel) |
| 25-W096-01 | W096 Bewässerungswasser → Mengenverlust unbewässerter Flächen | offen | offen | offen (Mon. Z61) | offen | offen | offen (Vorschlag: R7-Weiche mit #56) |
| 25-W017-01 | W017 Filter-/Pufferfunktionen → Mengenverlust | offen | offen | offen | offen | offen | offen (Vorschlag: bewusst inaktiv, → K7) |
| 25-W019-01 | W019 Produktionsfunktionen → Mengenverlust (Strom) | offen | offen | offen (Mon. Z24) | offen | offen | offen (Vorschlag: R1-Weiche mit #19) |
| 25-W020-01 | W020 Nährstoffspeicherfunktionen → Mengenverlust | offen | offen | offen | offen | offen | offen (Vorschlag: bewusst inaktiv, R10) |
| 25-W009-01 | W009 Bodenerosion durch Wasser → Mengenverlust on-site | offen | offen | offen (Mon. Z15) | offen | offen | offen |
| 25-W010-01 | W010 Bodenerosion durch Wind → Mengenverlust on-site | offen | offen | offen (Mon. Z16) | offen | offen | offen |
| 25-W021-01 | W021 Länge der Vegetationsperiode → Mengenverlust | offen | offen | offen (Mon. Z6) | offen | offen | offen |
| 25-W022-01 | W022 Phänologie → W046/W047 | offen | offen | offen | offen | offen | offen (Doppelkanal §3.2 zu klären) |
| 25-S021-01 | S021 Bodenart und Bodentyp → Stressempfindlichkeit des Ertrags | offen | offen | offen | offen | offen | offen |
| 25-S022-01 | S022 Bodenfruchtbarkeit → Ertragsniveau | offen | offen | offen | offen | offen | offen |
| 25-S023-01 | S023 Wasserrückhaltekapazität → Trockenstress-Ertragsverlust | offen | offen | offen | offen | offen | offen |
| 25-S024-01 | S024 Infiltrationskapazität → Vernässungs-/Erosions-Ertragsverlust | offen | offen | offen | offen | offen | offen |
| 25-S025-01 | S025 Anbaufrucht → Deckungsbeitrag und Stresstoleranz (Bandzuordnung) | offen | offen | offen (Mon. Z30: Deckungsbeitrag je Einheit) | offen | offen — Datenebene nach §3.1 | offen |
| 25-S026-01 | S026 Tierart → Mengenverlust Pflanze | offen | offen | offen | offen | offen | offen (Vorschlag: bewusst inaktiv, → #20) |
| 25-S027-01 | S027 Bewässerung → Mengenverlust (Hebel Wasserspeicher, effiziente Bewässerung) | im Erstaufschlag **keine nach §3.5 zulässige** (Interventions-/quasi-experimentelle) Effektgröße belegt ⇒ **Abschätzung von KAP3** \(r_{\text{S027}}\) = 0,0264 (Band 0,0056–0,09), Kette §5.1 | — (keine Interventionsstudie belegt; Feldversuche zu Bewässerungsgaben sind nur Kandidat, im Volltext nicht verifiziert, gehen nicht in den Wert ein) | Herleitung §5.1 (`#s027-wirkung`) | §3.9 ABGESCHÄTZT; Setzung für deutsche Kommunen | kommunal (Pauschalfaktor — Modellgrenze der Abschätzung) | offen (Vorschlag: Maßnahmen-Hebel, abgeschätzt) |
| 25-S028-01 | S028 Art der Bewirtschaftung → Mengenverlust | offen | offen | offen | offen | offen | offen |
| 25-S029-01 | S029 Dünger- und Pestizideinsatz → Mengenverlust | offen | offen | offen | offen | offen | offen (Vorschlag: R7 mit K8) |
| 25-S030-01 | S030 Züchterischer Fortschritt → Referenzertrags-Trend | offen | offen | offen | offen | offen | offen (Kalibrierung Kap. 4) |
| 25-S031-01 | S031 Möglichkeiten der Veterinärmedizin → Mengenverlust Pflanze | offen | offen | offen | offen | offen | offen (Vorschlag: bewusst inaktiv, → #20) |
| 25-S032-01 | S032 Vorhandensein von Hagelschutz → Mengenverlust (Hagel) | offen | offen | offen | offen | offen | offen (Vorschlag: Hebel, Bauform-Grenze Dauerkulturen) |
| 25-R05-01 | R05 Landwirtschaftliche Nutzfläche → Mengengerüst (ha) | offen | offen | offen | offen | offen — Datenebene nach §3.1 | offen |
| 25-R06-01 | R06 Anbauart → Mengengerüst je Fruchtart | offen | offen | offen | offen | offen — Datenebene nach §3.1 | offen |
| 25-R07-01 | R07 Tierhaltung → Mengenverlust Pflanze | offen | offen | offen | offen | offen | offen (Vorschlag: bewusst inaktiv, → #20) |
| 25-R08-01 | R08 Landwirtschaftliche Infrastruktur → Bewässerungs-/Speicherkapazität | offen | offen | offen | offen | offen | offen |

## 3 Modell (§2.3)

<!--
Pflichtinhalte (§2.3/§3.1/§3.2/§3.6):
- Native Ergebnisgröße deklarieren (genau eine je Risiko-Code; weitere als Teil-Ausweise).
  Kandidat laut Mon. Z30: Deckungsbeitragsverlust der pflanzlichen Erzeugung je Jahr (K6-Menge)
  — Entscheidung offen.
- Schicht-B-Formel Menge × Rate × Preis auf Zellebene, nur aus Register-Zeilen „Basiswert“ und
  hergeleiteten Parametern; physische Zwischengröße vor dem Euro (hier: Ertragsverlust in t/ha je
  Fruchtart, vor der Bewertung mit dem Deckungsbeitrag); Aggregation Zelle → Kommune.
- Je Formel alphabetische Zeichentabelle (Zeichen · Name · Einheit · Wert/Herkunft mit Register-ID
  oder Herleitungs-Anker); Mini-Rechenbeispiele als Golden-Test-Blöcke.
- Treiber-Attribution nach R3 (Anteile, keine Addition): die zehn Eingänge verteilen denselben
  Mengenverlust zu 100 %, sie summieren sich nicht (siehe Kap. 1, „Zehn Treiber, ein Sammelpunkt“).
- Lackmustest §3.1: Kommune ohne landwirtschaftliche Nutzfläche (R05) → ~0.
- Schicht-A-Index aus denselben Knoten, nie auf Euro-Pfaden.

(a) DATENEBENEN-ANLAGEPFLICHT (§3.1): Jede benötigte Zellgröße, die das Produkt nicht führt
    (voraussichtlich Anbaufläche je Fruchtart, Deckungsbeiträge je Fruchtart, nutzbare
    Feldkapazität/Bodenwasser, Bewässerungsanteil), wird als Ebene vollständig spezifiziert —
    Quelle, Beschaffungsweg keyless, Zell-Ableitungsregel, Fallback, Normierung/Zentrierung — und
    „neu anzulegen“ gekennzeichnet. Ohne offene Quelle: „geparkt (Datenquelle fehlt)“ mit
    Beschaffungs-Watchlist. Kein dauerhafter, unspezifizierter Neutral-Fallback.
(c) GESCHLOSSENE BETRACHTUNGSEBENE (§3.2): Zentrierungs-/Referenzmittel (hier insbesondere der
    Referenzertrag je Fruchtart) entweder amtlich publiziert oder aus der Betrachtungsebene selbst
    (Kommune: eigene Zellen, im Baseline-Lauf festgehalten) — nie aus einer Aggregation über eine
    höhere Ebene; ohne zulässige Referenz bleibt der Modifikator neutral.

Parameter-Block-Beispiel (Format §4; Werte erst nach Herleitung eintragen):
  parameter:
    id: crop_yield.<name>
    wert: <Herleitungswert>
    einheit: "<Einheit>"
    band: [<unten>, <oben>]
    herkunft: register:25-<Knoten>-01      # oder herleitung:#<anker>
    quelle: <quellen-id>
    preisstand: <Jahr>                     # Pflichtfeld bei Kostensätzen (Deckungsbeiträge!)
    bandzuordnung: [<Fruchtart>]
    endpunkt: <K6-Mengeneffekt Pflanze>

Beispiel-Test-Block (Format §4; im echten Block mit Code-Zaun „python test: beispiel_25_<name>“):
  assert abs(<rechnung> - <erwartet>) < 1e-9
-->

## 4 Kalibrierung & Validierung (§2.4/§3.4)

<!--
Pflichtinhalte: nationaler Anker als EIN Niveau-Skalar (Anker-Zeitreihe mit Revisionsstand;
vorläufige Jahre gesondert — bei Ernteerträgen sind die jüngsten Jahre regelmäßig vorläufig);
Kalibriermodell = Produktionsmodell; unabhängige Verteilungsprüfung auf der kritischsten Achse —
hier die TROCKENJAHRE (Dürrejahre gegen Normaljahre, nicht der Mittelwert) — mit vorab fixierter
Toleranz, out-of-sample; Sanity-Bänder mit Unter- und Obergrenze aus amtlicher Statistik;
Skripte/CSVs als Anlage verlinkt. Anker-Kandidaten und Zahlen: offen (keine Zahl ohne Quelle, P1).
Zu trennen ist der Züchtungs-/Managementtrend (S030, Register 25-S030-01) vom Klimasignal, sonst
wird der Trend als Schaden oder Chance fehlgebucht.

(b) RESSOURCEN-REGEL (§3.4): Kalibrierung, Validierung und Abgleiche nie über nationale
    100-m-Vollraster-Läufe planen — zulässig sind Bundesland-, Gemeinde-/Gemeindepunkt- und
    kommunale Stichproben-Ebene (dokumentierte Anker-Kommunen mit dem Produktionsmodell).
-->

## 5 Maßnahmen-Hebel (§2.5/§3.5)

<!--
Pflichtinhalte: Hebel nur an Ketten-Sensitivitäten; Effektgrößen aus Interventions-/
quasi-experimenteller Evidenz; marginal gegenüber heute; Doppelzählungs-Wächter gegen die
Kalibrierjahre; Wirkungsort definieren; R7-Weiche referenzieren (Ersatzwasser #56 und
Pflanzenschutz-Mehraufwand #24 sind K8-Maßnahmenkosten und schließen den verhinderten Ausfall je
Fläche aus). Hebel ohne Effektgröße: Abschätzung nach P2 (nie Wirkung null).
Offene Hebel-Kandidaten: S028 Bewirtschaftung/Fruchtfolge, S032 Hagelschutz, W048 Sortenwahl,
S029 Pflanzenschutz (über R7).
-->

### 5.1 Wirkungsabschätzung S027 Wasserspeicher und effiziente Bewässerung (Anker `#s027-wirkung`) — §3.9 **ABGESCHÄTZT**

**Anlass (Vorgabe P2, §3.5).** Die Roadmap nennt für #25 die Maßnahmen „Wasserspeicher“ und
„effiziente Bewässerung“; beide hängen am Ketten-Knoten S027 „Bewässerung“ (KWK Z98). Im
Erstaufschlag ist dafür **keine** Interventions- oder quasi-experimentelle Effektgröße belegt:
Bewässerungs-Feldversuche vergleichen Gaben unter Versuchsbedingungen, nicht den marginalen Ausbau
eines kommunalen Bestands, und sind hier nicht im Volltext verifiziert. Der Hebel wird deshalb
**nicht mit Wirkung null** geführt, sondern mit der folgenden **Abschätzung von KAP3**. Im Produkt
ist sie als solche samt dieser Herleitung auszuweisen (P1).

**Wirkungsort.** Multiplikativ auf den K6-Mengeneffekt von #25 der Kommune:
\(\text{DB-Verlust}_{\text{mit}} = \text{DB-Verlust} \cdot (1 - r_{\text{S027}})\). Nur K6-Menge; die
Kosten des Speicher- und Bewässerungsausbaus sind K8-Maßnahmenkosten und schließen den verhinderten
Ausfall je Fläche aus (R7, RR Z9; Mon. Z61 zu #56: „ENTWEDER Ertragsausfall unbewässerter Flächen
(ID 25) ODER Mehrkosten der Ersatzwasserbeschaffung (K8) je Fläche“).

**Kette.** \(r_{\text{S027}} = \Delta a \cdot s_{\text{tr}} \cdot e_{\text{bew}}\)

### 5.1.1 Zeichentabelle (Kette S027)

| Zeichen | Name | Einheit | Wert/Herkunft |
|---|---|---|---|
| \(\Delta a\) | zusätzlich gesichert bewässerter Anteil der Ackerfläche der Kommune (marginal gegenüber heute) | – | 0,08 (Band 0,04–0,15) · herleitung:#s027-wirkung — Abschätzung von KAP3, keine Primärquelle (§5.1.2) |
| \(e_{\text{bew}}\) | Anteil des Wassermangel-Verlusts, der auf der neu gesicherten Fläche vermieden wird | – | 0,60 (Band 0,40–0,80) · herleitung:#s027-wirkung — Abschätzung von KAP3, keine Primärquelle (§5.1.2) |
| \(r_{\text{S027}}\) | relative Minderung des K6-Mengeneffekts von #25 durch S027 | – | 0,0264 (Band 0,0056–0,09) · berechnet: \(\Delta a \cdot s_{\text{tr}} \cdot e_{\text{bew}}\) (§5.1.2) |
| \(s_{\text{tr}}\) | Anteil des Mengenverlusts, der auf Wassermangel im Boden zurückgeht (W003/W096) | – | 0,55 (Band 0,35–0,75) · herleitung:#s027-wirkung — Abschätzung von KAP3, keine Primärquelle (§5.1.2) |

### 5.1.2 Herleitung, Rechnung und Sensitivität

**Herleitung je Faktor** (alle drei Werte sind Abschätzungen von KAP3, keine Primärquelle):

- \(\Delta a\) = 0,08 (0,04–0,15). Annahme: Ein kommunales Speicher- und Bewässerungsprogramm sichert
  in einem Planungszeitraum jede zwölfte Ackerfläche zusätzlich ab. Untere Bandgrenze: halbe
  Reichweite. Obere: knapp doppelte, begrenzt durch Wasserrechte und Speicherbau. Marginal, weil
  bereits bewässerte Flächen im Basisverlust stecken (Doppelzählungs-Wächter gegen die
  Kalibrierjahre).
- \(s_{\text{tr}}\) = 0,55 (0,35–0,75). Annahme: Der Mengenverlust verteilt sich auf die zehn Treiber
  (Kap. 1); Wassermangel im Boden (#13) und fehlendes Bewässerungswasser (#56) sind der größte, aber
  nicht der einzige Block — Spätfrost, Hagel, Vernässung, Erosion und Schädlinge bleiben außerhalb.
  Ohne Attributionsrechnung wird knapp über der Mitte gesetzt, Band symmetrisch ±0,20.
- \(e_{\text{bew}}\) = 0,60 (0,40–0,80). Annahme: Zusatzbewässerung aus gefülltem Speicher deckt den
  Wasserbedarf in der kritischen Phase weitgehend. Restverlust, weil (i) der Speicher gerade im
  Dürrejahr nicht voll ist, (ii) Hitzestress auch bei ausreichendem Wasser Ertrag kostet und
  (iii) Gaben- und Technikverluste bleiben. Obergrenze unter 1, weil Bewässerung den Dürreschaden
  nie vollständig aufhebt.

Rechnung: \(r_{\text{S027}}\) = 0,08 · 0,55 · 0,60 = **0,0264**. Band (alle Enden gleichgerichtet):
0,04 · 0,35 · 0,40 = **0,0056** bis 0,15 · 0,75 · 0,80 = **0,09**.

**Ergebnis-Sensitivität.** Der ausgewiesene Maßnahmeneffekt ist −2,64 % des K6-Mengeneffekts von #25
(Band −0,56 % bis −9,0 %). Die Kette ist linear, jeder Faktor hat Elastizität 1. Einzeln variiert:
\(\Delta a\) 0,04–0,15 ⇒ r 0,0132–0,0495 (größte Achse); \(s_{\text{tr}}\) 0,35–0,75 ⇒ r
0,0168–0,036; \(e_{\text{bew}}\) 0,40–0,80 ⇒ r 0,0176–0,0352.

**Modellgrenzen der Abschätzung.** (1) Kommunenweiter Pauschalfaktor statt zellscharfer Wirkung je
Fruchtart (Bauform-Grenze: Dauerkulturen und Sonderkulturen sind anders bewässerbar als Ackerbau,
der Faktor unterscheidet das nicht). (2) Speicher und Bewässerungstechnik sind zu **einem** Faktor
\(e_{\text{bew}}\) zusammengefasst; getrennt wären sie erst trennbar, wenn Speichervolumen und
Wasserverfügbarkeit in Dürrejahren als Ebene vorliegen (§3.1, Knoten R08/W096). (3)
\(s_{\text{tr}}\) ist messbar, sobald die Treiber-Attribution nach R3 gerechnet ist — dann wird er
gemessen statt gesetzt (Ersetzungspfad, W1). (4) Ersetzt wird die ganze Abschätzung, sobald eine
Interventions- oder quasi-experimentelle Effektgröße gefunden ist (§3.8-Recherche offen).
(5) Die R7-Weiche gegen #56/K8 ist in dieser Abschätzung **nicht** beziffert: wer den Speicher baut,
bucht dessen Kosten, nicht den vermiedenen Ausfall — die 100-%-Aufteilung je Fläche steht offen.

```python test: beispiel_25_s027_abschaetzung
da, s_tr, e_bew = 0.08, 0.55, 0.60
r = da * s_tr * e_bew
assert abs(r - 0.0264) < 1e-12
lo, hi = 0.04 * 0.35 * 0.40, 0.15 * 0.75 * 0.80
assert abs(lo - 0.0056) < 1e-12 and abs(hi - 0.09) < 1e-12
assert abs(0.04 * s_tr * e_bew - 0.0132) < 1e-12 and abs(0.15 * s_tr * e_bew - 0.0495) < 1e-12
assert abs(da * 0.35 * e_bew - 0.0168) < 1e-12 and abs(da * 0.75 * e_bew - 0.036) < 1e-12
assert abs(da * s_tr * 0.40 - 0.0176) < 1e-12 and abs(da * s_tr * 0.80 - 0.0352) < 1e-12
```

## 6 Szenario-Anwendung & Modellgrenzen (§3.2/§3.6)

<!--
Pflichtinhalte: je empfohlenem Ansatz ein Absatz „Szenario-Anwendung“ (verschobene Größe — hier
Trockenheit/Hitze über W003/W045 und die Vegetationsperiode über W021/W046 —, konstante Größen:
Fruchtartenmuster R06, Deckungsbeiträge, Züchtungstrend S030; Stationaritätsannahmen);
Modellgrenzen nummeriert; Infokasten-Texte: Benennung „bewerteter Schaden — Konto K6 (Mengeneffekt
Pflanze)“ (nie „Gesamtschaden“), Vollständigkeitsanzeige, Versionsstempel „Untergrenze“; Hinweis,
dass Qualität (#26), Bodenbestand (#19, R1), Tierleistung (#20), K4-Off-site-Erosion und
K8-Mehrkosten (#22/#24/#56) nicht enthalten sind; Ausweis als Raten (je ha / je 1.000 EW) plus
aggregierte Ebene. Chancen nach R8 (z. B. längere Vegetationsperiode, #22) negativ und getrennt
ausweisen, nicht saldieren.
-->

## 7 Parameter-Blöcke (maschinenlesbar, §4)

Nur der Hebel aus §5.1 ist beziffert. Alle weiteren Blöcke entstehen mit der Herleitung in Kap. 3/4.

```yaml
parameter:
  id: crop_yield.da_s027
  wert: 0.08
  einheit: "-"
  band: [0.04, 0.15]
  herkunft: herleitung:#s027-wirkung     # Abschätzung von KAP3 (P1/P2)
  quelle: null
  preisstand: null
  bandzuordnung: [alle]
  endpunkt: K6-Mengeneffekt Pflanze
---
parameter:
  id: crop_yield.s_tr
  wert: 0.55
  einheit: "-"
  band: [0.35, 0.75]
  herkunft: herleitung:#s027-wirkung     # Abschätzung von KAP3 (P1/P2)
  quelle: null
  preisstand: null
  bandzuordnung: [alle]
  endpunkt: K6-Mengeneffekt Pflanze
---
parameter:
  id: crop_yield.e_bew
  wert: 0.60
  einheit: "-"
  band: [0.40, 0.80]
  herkunft: herleitung:#s027-wirkung     # Abschätzung von KAP3 (P1/P2)
  quelle: null
  preisstand: null
  bandzuordnung: [alle]
  endpunkt: K6-Mengeneffekt Pflanze
---
parameter:
  id: crop_yield.r_s027
  wert: 0.0264
  einheit: "-"
  band: [0.0056, 0.09]
  herkunft: herleitung:#s027-wirkung     # abgeleitet: da_s027 · s_tr · e_bew
  quelle: null
  preisstand: null
  bandzuordnung: [alle]
  endpunkt: K6-Mengeneffekt Pflanze
```

## 8 Quellen (§3.8)

1. KWRA-Schadensbaum × UBA-Klimawirkungsketten, Arbeitsmappe
   `docs/Schadensbaum/KWRA-Schadensbaum_X_UBA-klimawirkungsketten.xlsx` — Sheets
   „Klimawirkungsketten“ (Z40, Z41, Z46, Z47, Z54, Z56, Z57, Z71, Z72, Z92–Z103, Z105–Z108, Z111–Z115,
   Z118, Z119, Z214, Z219) und „Schadensbaum-Netzwerkliste“ (Z2, Z11, Z12, Z14, Z16, Z20, Z21, Z22–Z27,
   Z48, Z57).
2. KWRA-Monetarisierung, Arbeitsmappe `docs/Schadensbaum/KWRA-Monetarisierung.xlsx` — Sheets
   „Risiken-Monetarisierung“ (Z6, Z15, Z16, Z18, Z20, Z24–Z31, Z52, Z61), „Schadenskonten-System“
   (Z31, Z49–Z54), „Rechenregeln“ (Z3, Z5, Z6, Z7, Z9, Z10, Z11, Z13), „Abgleich-Protokoll“
   (P19, Blattzeilen Z32–Z34).
3. Evidenz-Quellen: offen. Für S027 ist **keine** Primärquelle verwendet (§5.1 ABGESCHÄTZT);
   Bewässerungs-Feldversuche sind genannt, aber nicht im Volltext geprüft und gehen in keinen Wert
   ein.

<!-- Format je Quelle: Autor, Jahr, Titel, Organ, DOI/URL, Zugriffsdatum, Archiv-Snapshot;
Sekundärfunde vor Übernahme im Volltext verifizieren; Widersprüche benennen. -->

## 9 Ansatz-Vergleich (§3.7 — erster Vertreter der Familie K6-Ertrag (Mengeneffekt Pflanze))

<!--
Pflicht nach §2.6, weil kein ABGENOMMENER Familien-Prototyp existiert: docs/methodik/ führt
K1-Berichte (#95/#96/#98) sowie die Erstaufschläge #60 (K3-Ereignisschaden), #61 und #50 (K8) und
#47 (K8 + ein K6-Zweig). #47 trägt denselben Baustein „K6-Mengeneffekt Pflanze“, ist aber nicht
gegengeprüft und rechnet die R7-Weiche eines Entwässerungssystems, nicht den Ertrag der Fläche.
Mindestens drei Ansätze a–c, festes Kriterienraster: kausale Treue · Kalibrierbarkeit · lokale
Differenzierung · Datenverfügbarkeit · Maßnahmen-Anschluss · Architektur-Konformität · Aufwand;
Empfehlung begründet; Verworfenes ggf. als Ergänzungsmodul.
Aus der Arbeitsmappe vorgegebener Kandidat (a): Mengenverlust je Fruchtart × Deckungsbeitrag je
Einheit (Mon. Z30, R4). Weitere Kandidaten (b), (c): offen. Negativ-Beispiel (§2.6/§3.1):
Verteilschlüssel „nationale Dürreschadensbilanz × Flächenanteil“ — ausgeschieden.
-->

| Kriterium | (a) Mengenverlust je Fruchtart × Deckungsbeitrag | (b) offen | (c) offen |
|---|---|---|---|
| kausale Treue | offen | offen | offen |
| Kalibrierbarkeit | offen | offen | offen |
| lokale Differenzierung | offen | offen | offen |
| Datenverfügbarkeit | offen | offen | offen |
| Maßnahmen-Anschluss | offen | offen | offen |
| Architektur-Konformität | offen | offen | offen |
| Aufwand | offen | offen | offen |

## Entscheidungslog

| Nr | Frage | angewendete Entscheidung | Begründung | Alternative | Auswirkung |
|---|---|---|---|---|---|
| 1 | Welcher W-Knoten trägt #25? | W052 (KWK Z119), ohne W051 | gleichnamiger Knoten im Container „Ertrag und Qualität der Ernteprodukte“; W051 „Durchschnittlicher Ertrag“ ist ein eigenes Sechseck und trägt allein den Einfluss E21 CO2 (KWK-Anmerkung) | W051 mitnehmen (brächte einen direkten Klimaterm E21 und damit einen Doppelkanal zu den Treibern) | 31 Knoten in Bilanz und Register; kein direkter Klimaeinfluss auf #25 |
| 2 | Familie? | neue Familie „K6-Ertrag (Mengeneffekt Pflanze)“, Kap. 9 angelegt; Berichtsaufbau von #60 übernommen | §2.6 verlangt einen **abgenommenen** Prototyp; #47 nutzt denselben Baustein, ist aber Erstaufschlag und rechnet eine K8-Weiche | #47 als Prototyp behandeln und Kap. 9 weglassen | Drei-Ansätze-Vergleich bleibt Pflicht |
| 3 | Die drei NW-Eingänge ohne W052-Kante (Id 1, 10, 11) | als Knoten W021/W022, W009, W010 in Bilanz und Register aufgenommen | NW Z26 führt sie als Input-Kanten; ohne sie fehlten Erosion und Vegetationsperiode, die Mon. Z15/Z16/Z6 ausdrücklich über K6 buchen | nur die W052-Eingangsliste (dann fiele der Nachweis „alle zehn Treiber erreichen #25“ aus) | vier zusätzliche Registerzeilen; Kein-Doppelkanal W022 zu klären |
| 4 | S027 ohne zulässige Effektgröße | P2-Abschätzung r = 0,0264 (0,0056–0,09) | Vorgabe P2, §3.5; Feldversuche sind keine Effektgröße für einen marginalen Bestandsausbau | Wirkung null (unzulässig nach P2) | Maßnahmen-Modul, kein Basiswert |
| 5 | Ausgangskante 25 → 20 (P19) | als physische Kopplung im selben Konto geführt, **kein** Euro-Transport; beziffert offen | R9 (RR Z11) lässt je Einheit nur eine Buchung zu; Mon. Z25 schließt Futterausfälle in #20 ausdrücklich aus | Betrag an #20 weiterreichen (wäre Doppelzählung in K6) | offener Punkt 5 statt stiller Annahme |
| 6 | Mon. Z26 (#21) nennt „Menge (ID 26)/Qualität (ID 27)“ | wörtlich übernommen, nicht korrigiert; als Befund in Ergebnis und Bilanz ausgewiesen | eiserne Regel 2: Arbeitsmappen nie still ändern oder überstimmen | im Bericht auf 25/26 „richtigstellen“ | Ledger-Befund für die Gegenprüfung |
| 7 | Slug | `ertragsausfaelle_landwirtschaft` | kurz, eindeutig gegen #26 (Qualität) und #31 (Holzertrag) | `ertragsausfaelle` (verwechselbar mit Forst/Fang-Ausfällen) | Dateinamen Bericht/Ledger |
