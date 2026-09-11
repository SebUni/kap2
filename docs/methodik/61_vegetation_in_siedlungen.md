# Methodik-Bericht #61 — Vegetation in Siedlungen

Status: **Erstaufschlag (`/neu-risiko 61`) — noch nicht gegengeprüft** · 11.09.2026 ·
Instruktionsquelle: `docs/AUFGABE_METHODIK_SCHADENSRECHNUNG.md` (v2) · Umsetzungsgrundlage: **offen**
(Ansatz-Vergleich Kap. 9) · Familie: **K8-Vorsorge/Mehrkosten — noch kein Prototyp, dieser Bericht ist
der erste Vertreter** (§2.6; Entscheidungslog Nr. 2). Berichtsaufbau übernommen von #60.

> **Geltungsbereich des Erstaufschlags.** Befüllt sind Kap. 1 (Wirkungskette, Knoten-Bilanz,
> Weitergaben, Konten) und Kap. 2 (Evidenz-Register-Skelett) aus den beiden Arbeitsmappen unter
> `docs/Schadensbaum/`. Kap. 3–9 tragen die Pflichtinhalte als Kommentar. Einzige bezifferte Größen
> sind die P2-Abschätzungen zu den Maßnahmen Stadtgrün und begrünte Dächer/Fassaden (§5.1,
> `#s099-wirkung`), ausdrücklich als **Abschätzung von KAP3** gekennzeichnet. Alle übrigen
> Entscheidungen stehen auf `offen`. Befund-Ledger: `reviews/BEFUNDE_61.md` (leer).

## Ergebnis

- **Slug:** `61_vegetation_in_siedlungen`. **Registerzeilen:** 21 (`61-<Knoten>-01`), gespiegelt in `docs/evidenz/register.md`.
- **Struktur von #60:** Berichtsaufbau geerbt (Kopf, Bilanz, zweispaltige Weitergaben, Register-Skelett, P2-Abschnitt, Parameter-Blöcke, Entscheidungslog). Methodik-Familie nicht geerbt: #60 ist K3-Ereignisschaden, #61 bucht K8/K4-Mehrkosten, daher Kap. 9 neu angelegt. Ebene A trägt dieselbe Gliederung wie Ebene B.
- **Wiederverwendete Registerzeilen:** keine. Geprüft wurden die mit #60 gemeinsamen Knoten S096, R23, R24, R25: dort ist das Outcome „Gebäudeschaden/Überflutung“, hier „Grünunterhalt-Mehrkosten“. Das ist ein anderer Zusammenhang (§2.2 c), also eigene Zeilen mit Querverweis und ohne kopierten Inhalt.
- **Offen:** (1) alle 21 Entscheidungen; (2) Ergebnisgröße und Ansatz (Kap. 9); (3) Aufteilung K8/K4 gegen „ein Konto je Endpunkt“ (§3.3), die Mappe nennt keinen K4-Bewertungsansatz; (4) Datenebenen Grünbestand, Straßenbäume, Kostensatz (Kap. 3); (5) R9 mit #65 Kühlenergie (K8) über Id 62; (6) Rollenbezeichnung NW „Ebene A“ ↔ Mon. „Endpunkt“; (7) Volltext-Evidenz zu S099.
- **Nacharbeitsrunden:** 0 bis zur Übergabe an den Prüfer. Keine Websuche, also keine externe Evidenz.

## 1 Wirkungskette & Knoten-Bilanz (§2.1)

**Rolle (Rollen-Check, Schritt 2):** Sheet „Schadensbaum-Netzwerkliste“ Z62 (Id 61):
**Buchungsobjekt — Ebene A**, Feld Bauwesen, Handlungserfordernis **sehr dringend**, Input-Kante
**4 Verschiebung von Arealen und Rückgang der Bestände** (ergänzt aus Abgleich), Output-Kante **100**,
Konten **K8 Mehr- & Vorsorgekosten; K4 Infrastruktur & Ver-/Entsorgung**, Bausteine
**K8-Maßnahmenkosten; K4-Betriebsmehrkosten**. Kein Abbruch nach R2/R3.
Monetarisierung Z66 führt die Rolle als „Endpunkt“ mit Konto „K8 + K4“ (offener Punkt 6).

**W-Knoten (Entscheidungslog Nr. 1):** Die Arbeitsmappe führt einen eigenen W-Knoten: Sheet
„Klimawirkungsketten“ Z282, **W127 „Vegetation in Siedlungen“** (Container „Umweltqualität in Städten“,
Konfidenz **hoch**). W127 hat **keine direkten klimatischen Einflüsse** (Anmerkung Z282). Einziger
Wirkungs-Eingang ist **W030 „Verschiebung von Arealen“** (Z80 = KWRA-Id 4). W030 ist vorgelagert; seine
Eingänge sind eine Ebene tief mit aufgenommen. Sie stammen aus einer Container-Expansion (Regel 3/5,
Konfidenz **mittel**). Der Code-Bestand (`backend/app/data/catalog.py`, Eintrag `kwra_id: 61`) trägt
Namenslisten, die nicht mit W127 übereinstimmen („Grad der Versiegelung“ statt S016/S099-Wortlaut); der
Bericht folgt der Arbeitsmappe.

### Knoten-Bilanz

Spalte „rechnet in“ ist im Erstaufschlag durchgängig `offen`. Die Spalte „Vorschlag“ nennt nur, was
die Arbeitsmappen selbst hergeben (Blatt + Zeile); sie ist keine Entscheidung.

| Knoten | Name | Blatt/Zeile | rechnet in | Vorschlag laut Arbeitsmappe |
|---|---|---|---|---|
| W030 | Verschiebung von Arealen (= Id 4) | KWK Z80; NW Z5 | offen | Hazard-Kanal Standort-/Trockenstress der Stadtvegetation (einzige Input-Kante, NW Z62; Abgleich P40). Id 4 selbst „Treiber (0 €)“, R3 (Mon. Z9) |
| E01 | Durchschnittstemperatur (über W030) | KWK Z2 | offen | Kandidat Klimasignal; wirkt nur über W030 (Kein-Doppelkanal §3.2) |
| E06 | Durchschnittlicher Niederschlag (über W030) | KWK Z7 | offen | wie E01 |
| S010 | Habitat- und Biotoptyp (über W030) | KWK Z58 | offen | Container-Expansion (W030-Anmerkung, Regel 3); Bezug zur Stadtvegetation zu prüfen |
| S011 | Habitat- und Biotopzustand (über W030) | KWK Z59 | offen | wie S010 |
| S012 | Tierart (über W030) | KWK Z60 | offen | kein Bezug zu Grünunterhalt-Mehrkosten erkennbar — voraussichtlich bewusst inaktiv |
| S013 | Pflanzenart (über W030) | KWK Z61 | offen | Kandidat Vulnerabilität (Trockenheitstoleranz des Arten-/Baumbestands) |
| S014 | Topographie (Geländeform, Höhe, etc.) (über W030) | KWK Z62 | offen | Container-Expansion; voraussichtlich schwach |
| S015 | Boden-/Vegetationsbedeckung (über W030) | KWK Z63 | offen | Kandidat Mengengerüst-Nähe; Doppelkanal mit S099 prüfen |
| S016 | Flächenversiegelung (über W030) | KWK Z64 | offen | Kandidat Standortstress (Straßenbäume); Doppelkanal mit dem Stadtklima-Zuschlag prüfen |
| S017 | Zerschneidung durch Verkehrswege (über W030) | KWK Z65 | offen | Arealverschiebung freilebender Arten — voraussichtlich bewusst inaktiv |
| S018 | Anthropogene Verbreitung von Arten (über W030) | KWK Z66 | offen | wie S017 |
| S019 | Verfügbarkeit von Ausbreitungskorridoren (über W030) | KWK Z67 | offen | wie S017 |
| S020 | Intensität der landwirtschaftlichen Nutzung (über W030) | KWK Z68 | offen | Agrarfläche, nicht Siedlung — voraussichtlich bewusst inaktiv |
| R03 | Vorkommen von Arealen, Arten und Populationen (über W030) | KWK Z69 | offen | voraussichtlich bewusst inaktiv (Mengengerüst ist das Siedlungsgrün, S099) |
| R04 | Vorkommen von Biotopen, Habitaten und Ökosystemen (über W030) | KWK Z70 | offen | wie R03 |
| S096 | Bauliche, organisatorische und finanzielle Vorsorge der öffentlichen Hand | KWK Z260 | offen | Kandidat Maßnahmen-Hebel (Grünflächenmanagement, Bewässerungsinfrastruktur); R7-Weiche (Mon. Z66) |
| S099 | Begrünung von Städten/Siedlungen | KWK Z263 | offen | Kandidat **Mengengerüst** (Bestand kommunalen Grüns) und **Maßnahmen-Hebel** Stadtgrün / Dach-/Fassadengrün; P2-Abschätzung §5.1 |
| R23 | Vorkommen von Bau- und Immobilienunternehmen | KWK Z269 | offen | laut W127-Anmerkung pauschal nach Regel 4 eingetragen — voraussichtlich bewusst inaktiv (vgl. 60-R23-01) |
| R24 | Vorkommen von Gebäuden | KWK Z270 | offen | Kandidat Mengengerüst Gebäudegrün (Dach-/Fassadenflächen, Mon. Z66 Gegenstand) |
| R25 | Vorkommen von Siedlungsinfrastrukturen | KWK Z271 | offen | Kandidat Straßenbegleitgrün → K4-Betriebsmehrkosten (NW Z62 Baustein) |

KWK = Sheet „Klimawirkungsketten“, NW = „Schadensbaum-Netzwerkliste“, Mon. = „Risiken-Monetarisierung“
(Blattzeile), Konten = „Schadenskonten-System“. **Nicht in der W127-Kette:** S095 „Begrünung von
Gebäuden“ (KWK Z259) speist nur W124 Stadtklima (Z279), nicht W127 (Entscheidungslog Nr. 3).

### Weitergaben (zweispaltig; Quelle: Netzwerkliste + Abgleich-Protokoll)

| Output-Kanten (Netzwerkliste / Abgleich-Protokoll mit Punkt-Nr.) | Konto-Ausschlüsse / verwandte Buchungen (Konten-Definition, Monetarisierung) |
|---|---|
| **61 → 100** Atembeschwerden (aufgrund von Luftverunreinigungen): NW Z62 Output „100“; Abgleich-Protokoll **P10** (Blatt Z13, Art „Buchungsobjekt→Buchungsobjekt“); NW Z101 führt 61 als ergänzte eingehende Kante; Mon. Z66 „→ 100 (P10)“. In der Kette entspricht das W127 → W126 Luftqualität (Smog) (KWK Z281). #100 bucht K1 (Mon. Z105); #61 bucht darauf 0 €. **Eingehend:** 4 → 61, Abgleich **P40** (Blatt Z123, Art „Kante“), NW Z5/Z62. **Kein NW-Ausgang, aber Kette:** W127 → W124 Stadtklima/Wärmeinseln (KWK Z279) = Id 62, „Rein vorgelagert (0 €)“ mit Ausgängen 95; 65; 87 (NW Z63). | **K8 enthält** (Konten Z66): „… Grünunterhalt …“; **K8 schließt aus** (Konten Z68): „Verhinderte Schäden zusätzlich (R7) · Investitionen mit Eigennutzen“. **K4 schließt aus** (Konten Z36): „Energie-VoLL (→ID 86), Gebäude (→K3)“. **#61 schließt aus** (Mon. Z66): „Kühlleistungswert zusätzlich zu gebuchten Hitzeschäden (R7)“; Bewertungsansatz: „Verlust der Kühlleistung NICHT separat bepreisen — er wirkt über die Hitze-Endpunkte (K1/K2)“. **#100 schließt aus** (Mon. Z105): „Gesamte Luftschadstofflast (nur Klimaanteil); hitzeattribuierte Fälle (ID 95)“. **Partitionsregel-Zitate:** R7 (Rechenregeln Z9): „Vorsorge-/Mehrkosten (K8) und der dadurch verhinderte Schaden schließen sich je Einheit aus“; R9 (Z11): „Innerhalb eines Kontos zählt jede Einheit … genau einmal“. **Ohne Partitionsregel in der Mappe (offen):** #65 Kühlenergie (K8, NW Z63 über Id 62) teilt K8 mit #61; #56 Bewässerungswasser (Mon. Z61: „Mehrkosten der Ersatzwasserbeschaffung (K8) je Fläche“) betrifft Feldberegnung, Überschneidung mit Stadtgrün-Bewässerung zu prüfen; K4-Anteil gegen #74–#77 (K4, Konten Z37). |

### Konto-Einbettung

- **Konten:** K8 Mehr- und Vorsorgekosten — Definition (Konten Z66): „Defensive Ausgaben und Vorsorge:
  Kühlung, Beschneiung, Bewässerungsersatz, Grünunterhalt, Schutzsystem-Ertüchtigung, Bekämpfung,
  Planung, Gesundheitsvorhaltung; … R7-Weiche: Mehrkosten schließen den verhinderten Schaden aus.“
  Kostensatz-Typ (Z67): „Ressourcenkosten der Maßnahmen (Ausgabenansatz)“. K4 Infrastruktur und
  Ver-/Entsorgung — Definition (Z34): „Instandsetzung und Betriebsmehrkosten öffentlicher und
  netzgebundener Infrastruktur …“; Kostensatz-Typ (Z35): „Instandsetzungskosten · Betriebsmehrkosten ·
  Umwegekostensätze“. #61 steht in beiden Buchungsobjekt-Listen (Z37, Z69).
- **Bewertungsbausteine:** K8-Maßnahmenkosten; K4-Betriebsmehrkosten (NW Z62). Bewertungsansatz
  (Mon. Z66): „Mehrkosten Grünunterhalt (Bewässerung, Ersatzpflanzung, Baumkontrolle) als K8“.
  Gegenstand: „Alle grünen Freiräume und begrünten Gebäude in Siedlungen (Parks, Straßenbäume, Gärten,
  Dach-/Fassadengrün): ihre Vitalität unter Trockenstress und ihre stadtklimatischen Funktionen.“
  Enthalten: „Kommunale Grünflächen-Mehrkosten.“ Für K4 nennt die Mappe **keinen** Bewertungsansatz
  (offener Punkt 3).
- **Rechenregeln:** R3, R7 (Mon. Z66, Spalte „Regeln“). Genau ein Konto je Endpunkt (§3.3) steht gegen
  „K8 + K4“: Die Aufteilung braucht eine Partitionsregel, die die Mappe nicht enthält (offener Punkt 3).
- **Handlungserfordernis:** sehr dringend (Mon. Z66, NW Z62).
- **Nur K8/K4 aktiv:** Kühl- und Luftwirkungen der Vegetation (K1 #95/#100, K2 #87, K8 #65) sind nicht
  enthalten — Untergrenze, im Infokasten zu benennen (§3.6).

## 2 Evidenz-Register (§2.2)

Skelett mit einer Zeile je Knoten der Bilanz. Die Zeilen sind in `docs/evidenz/register.md`
gespiegelt. **Wiederverwendung:** Das Register führt Zeilen aus #95/#96/#98 (K1) und #60 (K3). Mit #60
gemeinsame Knoten sind S096, R23, R24, R25. Deren #60-Zeilen beschreiben andere Zusammenhänge
(Überflutung, Gebäudeschaden) und sind deshalb **nicht** wiederverwendbar (§2.2 c: gleicher Knoten
**und** gleiches Outcome). Sie stehen nur als Querverweis in der Bilanz. 96-W024-01 (OSM-Vegetation,
Ebene POLLEN_LOAD) betrifft Symptomlast, nicht Grünunterhalt, und ist nur ein Datenhinweis für Kap. 3.
In Formeln (§3) dürfen später nur Zeilen mit Entscheidung **Basiswert** stehen.

| Register-ID | Knoten → Outcome | Effektgröße | Studientyp | Quelle | Übertragbarkeit | Datenlage je Zelle | Entscheidung |
|---|---|---|---|---|---|---|---|
| 61-W030-01 | W030 Arealverschiebung / Standortstress → Vitalitätsverlust Stadtvegetation | offen | offen | offen | offen | offen — Datenebene nach §3.1 zu spezifizieren | offen |
| 61-E01-01 | E01 Durchschnittstemperatur → W030 | offen | offen | offen | offen | offen (DWD-Raster 1 km im Produkt) | offen |
| 61-E06-01 | E06 Durchschnittlicher Niederschlag → W030 | offen | offen | offen | offen | offen (DWD-Raster 1 km im Produkt) | offen |
| 61-S010-01 | S010 Habitat-/Biotoptyp → Grünunterhalt-Mehrkosten | offen | offen | offen | offen | offen | offen |
| 61-S011-01 | S011 Habitat-/Biotopzustand → Grünunterhalt-Mehrkosten | offen | offen | offen | offen | offen | offen |
| 61-S012-01 | S012 Tierart → Grünunterhalt-Mehrkosten | offen | offen | offen | offen | offen | offen |
| 61-S013-01 | S013 Pflanzenart → Ausfall-/Ersatzpflanzungsrate | offen | offen | offen | offen | offen | offen |
| 61-S014-01 | S014 Topographie → Grünunterhalt-Mehrkosten | offen | offen | offen | offen | offen | offen |
| 61-S015-01 | S015 Boden-/Vegetationsbedeckung → Grünunterhalt-Mehrkosten | offen | offen | offen | offen | offen | offen |
| 61-S016-01 | S016 Flächenversiegelung → Standortstress Straßenbäume | offen | offen | offen | offen | offen | offen |
| 61-S017-01 | S017 Zerschneidung durch Verkehrswege → Grünunterhalt-Mehrkosten | offen | offen | offen | offen | offen | offen |
| 61-S018-01 | S018 Anthropogene Verbreitung von Arten → Grünunterhalt-Mehrkosten | offen | offen | offen | offen | offen | offen |
| 61-S019-01 | S019 Ausbreitungskorridore → Grünunterhalt-Mehrkosten | offen | offen | offen | offen | offen | offen |
| 61-S020-01 | S020 Landwirtschaftliche Nutzung → Grünunterhalt-Mehrkosten | offen | offen | offen | offen | offen | offen |
| 61-R03-01 | R03 Areale, Arten, Populationen → Mengengerüst | offen | offen | offen | offen | offen | offen |
| 61-R04-01 | R04 Biotope, Habitate, Ökosysteme → Mengengerüst | offen | offen | offen | offen | offen | offen |
| 61-S096-01 | S096 Vorsorge der öffentlichen Hand → Grünunterhalt-Mehrkosten | offen | offen | offen | offen | offen | offen (Vorschlag: Maßnahmen-Hebel, R7) |
| 61-S099-01 | S099 Begrünung von Städten/Siedlungen → Mengengerüst und Mehrkosten neuer Flächen | Mengengerüst: offen. Maßnahmen Stadtgrün / Dach-/Fassadengrün: im Erstaufschlag **keine** Effektgröße belegt ⇒ **Abschätzung von KAP3** \(v_{\text{neu}}\) = 0,60 (Band 0,40–0,90), \(v_{\text{geb}}\) = 0,30 (Band 0,10–0,60), §5.1 | — (keine Studie belegt) | Herleitung §5.1 (`#s099-wirkung`) | §3.9 ABGESCHÄTZT; Setzung für deutsche Kommunen | kommunal (Pauschalfaktor — Modellgrenze der Abschätzung) | offen (Vorschlag: Mengengerüst + Maßnahmen-Hebel, abgeschätzt) |
| 61-R23-01 | R23 Bau- und Immobilienunternehmen → Grünunterhalt-Mehrkosten | offen | offen | offen | offen | offen | offen |
| 61-R24-01 | R24 Gebäude → Mengengerüst Gebäudegrün | offen | offen | offen | offen | offen — Datenebene nach §3.1 zu spezifizieren | offen |
| 61-R25-01 | R25 Siedlungsinfrastrukturen → Mengengerüst Straßenbegleitgrün (K4) | offen | offen | offen | offen | offen — Datenebene nach §3.1 zu spezifizieren | offen |

## 3 Modell (§2.3)

<!--
Pflichtinhalte (§2.3/§3.1/§3.2/§3.6):
- Native Ergebnisgröße deklarieren (genau eine je Risiko-Code; weitere als Teil-Ausweise).
  Kandidat laut Mon. Z66: klimabedingte Grünunterhalt-Mehrkosten K8 je Jahr (Bewässerung,
  Ersatzpflanzung, Baumkontrolle) der Kommune — Entscheidung offen; K4-Teil offen (offener Punkt 3).
- Schicht-B-Formel Menge × Rate × Preis auf Zellebene: Menge = Bestand kommunalen Grüns (m², Bäume);
  Rate = klimabedingter Mehraufwand je Einheit (z. B. Bewässerungsgänge, Ausfallrate); Preis =
  Kostensatz mit Preisstand. Physische Zwischengröße vor dem Euro (Bewässerungsmenge, ersetzte Bäume).
- Je Formel alphabetische Zeichentabelle; Mini-Rechenbeispiele als Golden-Test-Blöcke.
- Lackmustest §3.1: Kommune ohne Trockenstress-Signal oder ohne kommunalen Grünbestand → ~0.
- Schicht-A-Index aus denselben Knoten, nie auf Euro-Pfaden.
- Kein-Doppelkanal: Kühlleistung nie hier (Mon. Z66), Grünanteil steckt im Stadtklima-Zuschlag.

(a) DATENEBENEN-ANLAGEPFLICHT (§3.1): Jede benötigte Zellgröße, die das Produkt nicht führt, wird als
    Ebene vollständig spezifiziert — Quelle, Beschaffungsweg keyless, Zell-Ableitungsregel, Fallback,
    Normierung/Zentrierung — und „neu anzulegen“ gekennzeichnet. Ohne offene Quelle: „geparkt
    (Datenquelle fehlt)“ mit Beschaffungs-Watchlist. Kein dauerhafter, unspezifizierter
    Neutral-Fallback. Kandidaten, Spezifikation offen:
    · Grünflächen-Bestand je Zelle (m²): OSM-Landnutzungsklassen liegen im Produkt als Vorstufe vor
      (`backend/app/services/climate/heat/osm_data.py`); öffentlich/privat ist in OSM nicht
      verlässlich trennbar — Proxy-Kennzeichnung nötig.
    · Straßenbäume je Zelle: OSM-Baumpunkte (vgl. Ebene POLLEN_LOAD) unvollständig; kommunale
      Baumkataster ohne bundesweite offene Quelle — Kandidat „geparkt“ mit Watchlist.
    · Gebäudegrün-Fläche (Dach/Fassade): offene Quelle nicht bekannt — Kandidat „geparkt“.
(c) GESCHLOSSENE BETRACHTUNGSEBENE (§3.2): Zentrierungs-/Referenzmittel entweder amtlich publiziert
    oder aus der Betrachtungsebene selbst (Kommune: eigene Zellen, im Baseline-Lauf festgehalten) —
    nie aus einer Aggregation über eine höhere Ebene; ohne zulässige Referenz bleibt der
    Modifikator neutral.

Parameter-Block-Beispiel (Format §4; Werte erst nach Herleitung eintragen):
  parameter:
    id: settlement_veg.<name>
    wert: <Herleitungswert>
    einheit: "<Einheit>"
    band: [<unten>, <oben>]
    herkunft: register:61-<Knoten>-01      # oder herleitung:#<anker>
    quelle: <quellen-id>
    preisstand: <Jahr>                     # Pflichtfeld bei Kostensätzen
    bandzuordnung: [<Grünflächentyp>]
    endpunkt: <K8-Maßnahmenkosten | K4-Betriebsmehrkosten>

Beispiel-Test-Block (Format §4; im echten Block mit Code-Zaun „python test: beispiel_61_<name>“):
  assert abs(<rechnung> - <erwartet>) < 1e-9
-->

## 4 Kalibrierung & Validierung (§2.4/§3.4)

<!--
Pflichtinhalte: nationaler Anker als EIN Niveau-Skalar (Anker-Zeitreihe mit Revisionsstand;
vorläufige Jahre gesondert); Kalibriermodell = Produktionsmodell; unabhängige Verteilungsprüfung auf
der kritischsten Achse — hier voraussichtlich Trockenjahr vs. Normaljahr und Großstadt vs. Kleinstadt —
mit vorab fixierter Toleranz, out-of-sample; Sanity-Bänder mit Unter- und Obergrenze aus amtlicher
Statistik (z. B. kommunale Haushaltsstatistik Grünflächenunterhalt). Anker-Kandidaten und Zahlen: offen
(keine Zahl ohne Quelle, P1).

(b) RESSOURCEN-REGEL (§3.4): Kalibrierung, Validierung und Abgleiche nie über nationale
    100-m-Vollraster-Läufe planen — zulässig sind Bundesland-, Gemeinde-/Gemeindepunkt- und
    kommunale Stichproben-Ebene (dokumentierte Anker-Kommunen mit dem Produktionsmodell).
-->

## 5 Maßnahmen-Hebel (§2.5/§3.5)

<!--
Pflichtinhalte: Hebel nur an Ketten-Sensitivitäten; Effektgrößen aus Interventions-/
quasi-experimenteller Evidenz; marginal gegenüber heute; Doppelzählungs-Wächter gegen die
Kalibrierjahre; Wirkungsort definieren; R7-Weiche referenzieren (Mehrkosten K8 schließen den
verhinderten Schaden aus). Hebel ohne Effektgröße: Abschätzung nach P2 (nie Wirkung null).
Offener Hebel-Kandidat: S096 (Grünflächenmanagement, Bewässerungsinfrastruktur).
-->

### 5.1 Wirkungsabschätzung Stadtgrün und begrünte Dächer/Fassaden auf #61 (Anker `#s099-wirkung`) — §3.9 **ABGESCHÄTZT**

**Anlass (Vorgabe P2, §3.5).** Das Produkt führt die Maßnahmen „Stadtgrün“ (Ausbau städtischer
Grünflächen) und „Begrünte Dächer/Fassaden“. Beide greifen an der Ketten-Sensitivität S099 „Begrünung
von Städten/Siedlungen“ (KWK Z263) an. Für ihre Wirkung auf die klimabedingten Grünunterhalt-Mehrkosten
von #61 ist im Erstaufschlag keine Effektgröße belegt. Die Wirkung wird deshalb **nicht null**
gesetzt, sondern mit der folgenden **Abschätzung von KAP3** geführt. Im Produkt ist sie als solche samt
dieser Herleitung auszuweisen (P1).

**Wirkungsrichtung.** Nach Mon. Z66 bucht #61 nur Mehrkosten des Grünunterhalts. Die Kühlleistung wirkt
über die Hitze-Endpunkte und wird hier nicht bepreist. Neue Grünflächen vergrößern also den Bestand, an
dem klimabedingte Mehrkosten entstehen: Die Maßnahme **erhöht** die K8-Buchung von #61. Klimaangepasste
Anlage macht diese Erhöhung kleiner als proportional. Ihre entlastende Wirkung erscheint an #95/#87
(über Id 62) und #100 (P10), nicht hier (Kein-Doppelkanal §3.2).

**Wirkungsort.** Multiplikativ auf die klimabedingten Grünunterhalt-Mehrkosten \(M_0\) (K8) der Kommune:

\[
M_{\text{mit}} = M_0 \cdot \Bigl(1 + \frac{\Delta B_{\text{grün}}}{B}\, v_{\text{neu}} + \frac{\Delta B_{\text{geb}}}{B}\, v_{\text{geb}}\Bigr)
\]

Ohne Anpassung wäre der Faktor je neuer Fläche 1, weil die Mehrkosten nach der Kernformel
(Menge × Rate × Preis, §1) proportional zur Menge sind. Nur kommunale Flächen zählen
(Mon. Z66 „Kommunale Grünflächen-Mehrkosten“). Private Dach-/Fassadenflächen gehören nicht zum
Konto-Geltungsbereich von #61. Das ist eine Konto-Abgrenzung, keine Nullwirkung aus fehlender
Effektgröße (Entscheidungslog Nr. 5).

### 5.1.1 Zeichentabelle (Wirkungsort S099)

| Zeichen | Name | Einheit | Wert/Herkunft |
|---|---|---|---|
| \(B\) | Bestand kommunalen Grüns der Kommune vor der Maßnahme | m² | Mengengerüst aus register:61-S099-01 (Entscheidung und Datenebene in Kap. 1/2 als offen geführt) |
| \(\Delta B_{\text{geb}}\) | neu begrünte kommunale Dach- und Fassadenfläche | m² | Nutzereingabe der Maßnahme „Begrünte Dächer/Fassaden“, kein Parameter · herleitung:#s099-wirkung (Wirkungsort) |
| \(\Delta B_{\text{grün}}\) | neu angelegte kommunale Grünfläche | m² | Nutzereingabe der Maßnahme „Stadtgrün“, kein Parameter · herleitung:#s099-wirkung (Wirkungsort) |
| \(M_0\) | klimabedingte Grünunterhalt-Mehrkosten der Kommune ohne Maßnahme (K8) | €/a | Ergebnis der Schicht-B-Rechnung, Kandidat native Größe (Mon. Z66); Entscheidung in Kap. 1 als offen geführt |
| \(M_{\text{mit}}\) | dieselben Mehrkosten mit Maßnahme | €/a | berechnet nach der Formel in §5.1 |
| \(v_{\text{geb}}\) | relative klimabedingte Mehrkosten-Intensität je m² kommunalen Dach-/Fassadengrüns gegenüber dem Bestandsmittel | – | 0,30 (Band 0,10–0,60) · herleitung:#s099-wirkung — Abschätzung von KAP3, keine Primärquelle (§5.1.2) |
| \(v_{\text{neu}}\) | relative klimabedingte Mehrkosten-Intensität je m² neu und klimaangepasst angelegten Stadtgrüns gegenüber dem Bestandsmittel | – | 0,60 (Band 0,40–0,90) · herleitung:#s099-wirkung — Abschätzung von KAP3, keine Primärquelle (§5.1.2) |

### 5.1.2 Herleitung, Rechnung und Sensitivität

**Herleitung je Faktor** (beide Werte sind Abschätzungen von KAP3, keine Primärquelle):

- \(v_{\text{neu}}\) = 0,60 (0,40–0,90). Annahme: Neue Flächen werden heute klimaangepasst geplant
  (trockenheitsverträgliche, standortgerechte Arten; Baumstandorte mit mehr Wurzelraum und
  Wasserspeicher). Das senkt Ausfälle und damit Ersatzpflanzungen sowie den dauerhaften
  Bewässerungsbedarf gegenüber dem Bestandsmittel. Dagegen steht die Anwuchsbewässerung junger
  Pflanzungen in Trockenjahren. Mitte: 40 % unter dem Bestandsmittel. Untere Bandgrenze 0,40: Anpassung
  wirkt stark. Obere 0,90: Die Anwuchspflege zehrt den Vorteil fast auf. Unter 1, weil die Größe über die
  Standzeit gemittelt ist und die Anwuchsjahre nur einen kleinen Teil davon ausmachen.
- \(v_{\text{geb}}\) = 0,30 (0,10–0,60). Annahme: Extensive Dachbegrünung trägt trockenheitsverträgliche
  Vegetation und wird meist nicht bewässert. Klimabedingte Mehrkosten beschränken sich auf Nachsaat nach
  Dürreausfällen; Baumkontrolle entfällt. Bodengebundene Fassadenbegrünung braucht in Trockenperioden
  Bewässerung und bestimmt die obere Bandgrenze 0,60. Untere Grenze 0,10: fast nur Extensivdächer.

**Rechnung und Ergebnis-Sensitivität.** Die Formel ist linear, jeder Faktor hat Elastizität 1. Je 1 %
Flächenzuwachs (\(\Delta B / B\) = 0,01):

- Stadtgrün: \(M_{\text{mit}}/M_0 - 1\) = 0,01 · 0,60 = **+0,60 %** (Band +0,40 % bis +0,90 %).
- Dach-/Fassadengrün: 0,01 · 0,30 = **+0,30 %** (Band +0,10 % bis +0,60 %).
- Vergleich ohne Anpassung (Faktor 1): +1,00 %. Die ausgewiesene Maßnahmenwirkung auf #61 gegenüber
  unangepasster Anlage ist also −0,40 Prozentpunkte (Stadtgrün) bzw. −0,70 Prozentpunkte (Gebäudegrün)
  je 1 % Flächenzuwachs.
- Größte Achse: \(v_{\text{geb}}\), Band umfasst Faktor 6 (0,10–0,60); \(v_{\text{neu}}\) Faktor 2,25.

**Modellgrenzen der Abschätzung.** (1) Kommunenweiter Pauschalfaktor statt zellscharfer Wirkung
(Bauform-Grenze); Standortunterschiede (Versiegelung S016, Pflanzenart S013) bleiben unberücksichtigt.
(2) Die Anwuchsjahre sind über die Standzeit gemittelt; der zeitliche Verlauf der Mehrkosten wird nicht
abgebildet. (3) Doppelzählungs-Wächter offen: Die laufenden Unterhaltskosten der Maßnahme selbst dürfen
nur die Grundpflege enthalten, sonst stehen Trockenstress-Mehrkosten zweimal in K8 (R7). (4) Ersetzt
wird die Abschätzung, sobald Kostenstatistiken zu Pflege klimaangepasster gegenüber konventioneller
Pflanzungen gefunden sind (§3.8-Recherche offen).

```python test: beispiel_61_s099_abschaetzung
v_neu, v_geb, anteil = 0.60, 0.30, 0.01
assert abs(anteil * v_neu - 0.0060) < 1e-12
assert abs(anteil * 0.40 - 0.0040) < 1e-12 and abs(anteil * 0.90 - 0.0090) < 1e-12
assert abs(anteil * v_geb - 0.0030) < 1e-12
assert abs(anteil * 0.10 - 0.0010) < 1e-12 and abs(anteil * 0.60 - 0.0060) < 1e-12
assert abs((anteil * 1.0 - anteil * v_neu) - 0.0040) < 1e-12
assert abs((anteil * 1.0 - anteil * v_geb) - 0.0070) < 1e-12
assert abs(0.60 / 0.10 - 6.0) < 1e-12 and abs(0.90 / 0.40 - 2.25) < 1e-12
```

## 6 Szenario-Anwendung & Modellgrenzen (§3.2/§3.6)

<!--
Pflichtinhalte: je empfohlenem Ansatz ein Absatz „Szenario-Anwendung“ (verschobene Größe — über E01/E06
in W030 —, konstante Größen, Stationaritätsannahmen, Bestandsdynamik S099); Modellgrenzen nummeriert;
Infokasten-Texte: Benennung „bewerteter Schaden — Konto K8“ (bzw. K4-Teil), nie „Gesamtschaden“,
Vollständigkeitsanzeige, Versionsstempel „Untergrenze“; Hinweis, dass Kühlleistung (#95, #87, #65) und
Luftwirkung (#100) nicht enthalten sind; Ausweis als Raten (je ha Grünfläche / je 1.000 EW) plus
aggregierte Ebene.
-->

## 7 Parameter-Blöcke (maschinenlesbar, §4)

Nur die Faktoren aus §5.1 sind beziffert. Alle weiteren Blöcke entstehen mit der Herleitung in Kap. 3/4.

```yaml
parameter:
  id: settlement_veg.v_neu_s099
  wert: 0.60
  einheit: "-"
  band: [0.40, 0.90]
  herkunft: herleitung:#s099-wirkung     # Abschätzung von KAP3 (P1/P2)
  quelle: null
  preisstand: null
  bandzuordnung: [kommunales Stadtgrün]
  endpunkt: K8-Maßnahmenkosten
---
parameter:
  id: settlement_veg.v_geb_s099
  wert: 0.30
  einheit: "-"
  band: [0.10, 0.60]
  herkunft: herleitung:#s099-wirkung     # Abschätzung von KAP3 (P1/P2)
  quelle: null
  preisstand: null
  bandzuordnung: [kommunales Dach-/Fassadengrün]
  endpunkt: K8-Maßnahmenkosten
```

## 8 Quellen (§3.8)

1. KWRA-Schadensbaum × UBA-Klimawirkungsketten, Arbeitsmappe
   `docs/Schadensbaum/KWRA-Schadensbaum_X_UBA-klimawirkungsketten.xlsx` — Sheets
   „Klimawirkungsketten“ (Z2, Z7, Z58–Z70, Z80, Z259, Z260, Z263, Z269–Z271, Z279, Z281, Z282) und
   „Schadensbaum-Netzwerkliste“ (Z5, Z62, Z63, Z101).
2. KWRA-Monetarisierung, Arbeitsmappe `docs/Schadensbaum/KWRA-Monetarisierung.xlsx` — Sheets
   „Risiken-Monetarisierung“ (Z9, Z61, Z66, Z105), „Schadenskonten-System“ (Z33–Z37, Z65–Z69),
   „Rechenregeln“ (Z5, Z9, Z11), „Abgleich-Protokoll“ (P10 = Blatt Z13; P40 = Blatt Z123).
3. Evidenz-Quellen: offen. Für S099 ist keine Primärquelle verwendet (§5.1 ABGESCHÄTZT). Der
   Code-Bestand zitiert für Unterhaltskosten Semmler (2013, `Semmler_Stadtgruen_2013`) und für
   Gebäudegrün den BuGG-Marktreport 2024 (`backend/app/data/sources.py`). Beide sind hier nicht im
   Volltext geprüft und gehen in keinen Wert ein.

<!-- Format je Quelle: Autor, Jahr, Titel, Organ, DOI/URL, Zugriffsdatum, Archiv-Snapshot;
Sekundärfunde vor Übernahme im Volltext verifizieren; Widersprüche benennen. -->

## 9 Ansatz-Vergleich (§3.7 — erster Vertreter der Familie K8-Vorsorge/Mehrkosten)

<!--
Pflicht nach §2.6, weil kein abgenommener Familien-Prototyp existiert (docs/methodik/ führt K1-Berichte
#95/#96/#98 und den K3-Erstaufschlag #60). Mindestens drei Ansätze a–c, festes Kriterienraster: kausale
Treue · Kalibrierbarkeit · lokale Differenzierung · Datenverfügbarkeit · Maßnahmen-Anschluss ·
Architektur-Konformität · Aufwand; Empfehlung begründet; Verworfenes ggf. als Ergänzungsmodul.
Aus der Arbeitsmappe vorgegebener Kandidat (a): Mehrkosten Grünunterhalt je Einheit — Bestand ×
klimabedingter Mehraufwand (Bewässerung, Ersatzpflanzung, Baumkontrolle) × Kostensatz (Mon. Z66).
Weitere Kandidaten (b), (c): offen. Negativ-Beispiel (§2.6/§3.1): Verteilschlüssel
„nationaler Grünflächen-Mehrkostentopf × Flächenanteil“ — ausgeschieden.
-->

| Kriterium | (a) Bestand × Mehraufwand × Kostensatz | (b) offen | (c) offen |
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
| 1 | Welcher W-Knoten trägt #61? | W127 (KWK Z282), mit W030 eine Ebene tief | eigener, namensgleicher Knoten mit Konfidenz hoch; NW Z62 Input 4 = W030 | Code-Bestand-Namensliste (weicht von W127 ab) | 21 Knoten in Bilanz und Register |
| 2 | Familie? | neue Familie K8-Vorsorge/Mehrkosten, Kap. 9 angelegt; Berichtsaufbau von #60 übernommen | kein K8-Bericht in `docs/methodik/`; #60 ist K3-Ereignislogik (A5), #61 Ausgabenansatz (Konten Z67) | Übernahme der K3/K4-Ereignislogik von #60 — kein Ereignis, sondern laufende Mehrkosten | Drei-Ansätze-Vergleich Pflicht |
| 3 | Woran hängt Dach-/Fassadengrün? | an S099 (Z263) | Mon. Z66 zählt Dach-/Fassadengrün zum Gegenstand von #61; S095 „Begrünung von Gebäuden“ speist nur W124, nicht W127 | S095 als Hebel (unzulässig: kein Knoten der W127-Kette, §1) | beide Maßnahmen an einem Knoten, getrennte Faktoren |
| 4 | Maßnahmen ohne Effektgröße | P2-Abschätzung \(v_{\text{neu}}\) = 0,60 (0,40–0,90), \(v_{\text{geb}}\) = 0,30 (0,10–0,60) | Vorgabe P2, §3.5 | Wirkung null (unzulässig nach P2); Wirkung als Minderung (widerspräche Mon. Z66: Kühlleistung nicht hier) | Maßnahmen-Modul, kein Basiswert; Vorzeichen Mehrkosten |
| 5 | Private Gebäude-/Grünflächen | nicht im Konto-Geltungsbereich von #61 | Mon. Z66 „Kommunale Grünflächen-Mehrkosten“ | privates Grün mitbuchen (Fortschreibung der Mappe nötig, §1) | kleineres Mengengerüst; Wirkung privater Flächen über Hitze-Endpunkte |
| 6 | Slug | `vegetation_in_siedlungen` | KWRA-Name 1:1 (§1), eindeutig | `stadtgruen` (verengt auf Maßnahme) | Dateinamen Bericht/Ledger |
