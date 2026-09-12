# Methodik-Bericht #47 — Überlastung der Entwässerungseinrichtungen in überflutungsgefährdeten Gebieten

Status: **Erstaufschlag (`/neu-risiko 47`) — noch nicht gegengeprüft** · 12.09.2026 ·
Instruktionsquelle: `docs/AUFGABE_METHODIK_SCHADENSRECHNUNG.md` (v2) · Umsetzungsgrundlage: **offen**
(Ansatz-Vergleich Kap. 9) · Familie: **K8-Vorsorge-Weichen (§2.6)** — Struktur von #50 übernommen,
dort aber noch kein abgenommener Prototyp, deshalb Kap. 9 mit angelegt (Entscheidungslog Nr. 2).
Berichtsaufbau übernommen von #60/#61/#50.

> **Geltungsbereich des Erstaufschlags.** Befüllt sind Kap. 1 (Wirkungskette, Knoten-Bilanz,
> Weitergaben, **Konten-Einbettung mit der Herleitung der Doppelbuchung K8 + K6**) und Kap. 2
> (Evidenz-Register-Skelett) aus den beiden Arbeitsmappen unter `docs/Schadensbaum/`. Kap. 3–9
> tragen die Pflichtinhalte als Kommentar. Einzige bezifferte Größen sind die P2-Abschätzungen zu
> den Maßnahmen Retention und Versickerungsflächen (§5.1, `#s062-wirkung`), ausdrücklich als
> **Abschätzung von KAP3** gekennzeichnet. Alle übrigen Entscheidungen stehen auf `offen`.
> Befund-Ledger: `reviews/BEFUNDE_47.md` (leer).

## Ergebnis

- **Slug:** `47_entwaesserung_kuestenniederungen`. **Registerzeilen:** 11 (`47-<Knoten>-01`), gespiegelt in `docs/evidenz/register.md`.
- **Konto/Baustein wörtlich aus NW Z48:** „K8 Mehr- & Vorsorgekosten; K6 Land-, Forst- & Fischereiproduktion“ · „K8-Maßnahmenkosten; K6-Mengeneffekt Pflanze“. Kein Abbruch (Rolle „Buchungsobjekt — Ebene B“).
- **Doppelbuchung (Kap. 1.3, Kern des Berichts):** Die beiden Konten sind die **zwei Zweige derselben R7-Weiche**, nicht zwei Schäden desselben Ereignisses: Haltefall → K8-Mehrkosten, Versagensfall → K6-Vernässungsschaden, wahrscheinlichkeitsgewichtet mit \(1-p\) und \(p\). Kein Hektar und kein Jahr kann in beiden Zweigen liegen; addiert werden zwei disjunkte Zustände, nicht derselbe Euro (R7 Z9, R9 Z11, Mon. Z52 „Nicht enthalten: Mehrkosten + voll verhinderte Vernässungsschäden gleichzeitig“).
- **Offen:** (1) alle 11 Entscheidungen; (2) Ergebnisgröße und Ansatz (Kap. 9) — bei zwei Konten zusätzlich die Frage, ob K8 oder K6 die native Größe ist; (3) **R9-Partition #47 gegen #25 Ertragsausfälle** (Mon. Z30 führt #25 als „SAMMEL-BUCHUNGSOBJEKT der pflanzlichen Mengenverluste“, die Mappen nennen keine Partitionsregel gegen #47) — im Log Nr. 4 entschieden, bleibt prüfbedürftig; (4) Abgrenzung zu #52 Kanalnetze/Kläranlagen (K4) und zu #45 Küstenschutz, dessen Versagenszweig laut Mon. Z50 „über die Endpunkte 46/47“ läuft, ohne Kante in der Netzwerkliste; (5) Datenebenen Siele/Schöpfwerke, Sperrzeiten, Marschflächen; (6) Namensdivergenz W082 ↔ Id 47 (Log Nr. 1); (7) Volltext-Evidenz zu beiden Maßnahmen.
- **Nacharbeitsrunden:** 0 bis zur Übergabe. Keine Websuche, also keine externe Evidenz.

## 1 Wirkungskette & Knoten-Bilanz (§2.1)

**Rolle (Rollen-Check, Schritt 2):** Sheet „Schadensbaum-Netzwerkliste“ Z48 (Id 47):
**Buchungsobjekt — Ebene B**, Feld Küsten- und Meeresschutz, Handlungserfordernis **sehr dringend**,
Input-Kanten **40 Meeresspiegelhöhe; 43 Sturmfluten** (40 ergänzt aus Abgleich), **keine Output-Kante**,
Konto **K8 Mehr- & Vorsorgekosten; K6 Land-, Forst- & Fischereiproduktion**, Bausteine
**K8-Maßnahmenkosten; K6-Mengeneffekt Pflanze**. Kein Abbruch nach R2/R3. Monetarisierung Z52 führt
die Rolle als „Endpunkt“ mit Schadenskonto „K8 + K6“ und Regel „R7“.

**W-Knoten (Entscheidungslog Nr. 1):** Sheet „Klimawirkungsketten“ Z189, **W082 „Überlastung der
Entwässerungseinrichtungen in niedrig gelegenen Marschgebieten“** (Container „Infrastruktur an der
Küste“, Konfidenz **hoch**). Anmerkung Z189: „Keine direkten klimatischen Einflüsse.“
Wirkungs-Eingänge sind **W074 Meeresspiegelhöhe** (Z181 = Id 40) und **W077 Sturmfluten**
(Z184 = Id 43); beide sind rein vorgelagert (Mon. Z45/Z48, R2). Ihre Eingänge sind eine Ebene tief
mit aufgenommen (E01 über W074; E17, W074, W075 über W077; Sensitivitäten S059/S060 über den
Container „Wasserstand der Meere“, Regel 3/5, Konfidenz **mittel**). Einzige eigene Sensitivität ist
**S062** (Z171), räumliche Eingänge sind **R14/R15/R16** (Z175–Z177). Der Code-Bestand
(`backend/app/data/catalog.py`, Eintrag `kwra_id: 47`) trägt dieselben Namenslisten wie W082,
aber den Namen der Netzwerkliste.

### Knoten-Bilanz

Spalte „rechnet in“ ist im Erstaufschlag durchgängig `offen`. Die Spalte „Vorschlag“ nennt nur, was
die Arbeitsmappen selbst hergeben (Blatt + Zeile); sie ist keine Entscheidung.

| Knoten | Name | Blatt/Zeile | rechnet in | Vorschlag laut Arbeitsmappe |
|---|---|---|---|---|
| W074 | Meeresspiegelhöhe (= Id 40) | KWK Z181; NW Z41 | offen | Außenwasserstand am Siel: hebt das Sielzugniveau und verlängert die Sperrzeit (Mon. Z52 Gegenstand „bei steigendem Außenwasserstand“). Kante 40 → 47 aus Abgleich **P20** (Blatt Z35; NW Z48 „Ergänzte Kanten aus Abgleich (eingehend)“ = 40). Id 40 selbst „Rein vorgelagert (0 €)“, R2 (Mon. Z45) |
| W077 | Sturmfluten (= Id 43) | KWK Z184; NW Z44 | offen | Ereignisspitze des Außenwasserstands: Sielschluss über mehrere Tiden. Originalkante 43 → 47 (NW Z44; Mon. Z48 „→ 45, 46, **47**, 74, 101“). Id 43 selbst „Rein vorgelagert (0 €)“, R2 |
| W075 | Strömungen und Gezeitendynamik (über W077) | KWK Z182 | offen | wirkt nur über W077 (Kein-Doppelkanal §3.2); Tidehub als Randbedingung der Sielzugdauer, kein eigener Faktor |
| E01 | Durchschnittstemperatur (über W074) | KWK Z2 | offen | einziger klimatischer Eingang von W074; Szenario-Verschiebung des Meeresspiegels, kein eigener Faktor |
| E17 | Starkwind (über W077) | KWK Z18 | offen | einziger klimatischer Eingang von W077; Szenario-Verschiebung der Sturmflutspitze |
| S059 | Meerestopographie (über W074/W077, Container-Vererbung) | KWK Z168 | offen | Container „Eigenschaften des Meeres“ (Regel 5); Kandidat **bewusst inaktiv** — Handlungsfeld-Vererbung ohne kommunale Zellgröße |
| S060 | Wasseraustausch mit anderen Meeren (über W074/W077, Container-Vererbung) | KWK Z169 | offen | wie S059 |
| S062 | Art und Zustand von Bauwerken und Küsteninfrastruktur | KWK Z171 | offen | Kandidat **Vulnerabilität** (Leistungsfähigkeit von Siel und Schöpfwerk, Versagenswahrscheinlichkeit) und **Maßnahmen-Hebel** Retention, Versickerungsflächen; P2-Abschätzung §5.1 |
| R14 | Vorkommen von Küsten, Wattenmeere, Ästuare | KWK Z175 | offen | Kandidat Exposition; Lackmustest §3.1: Kommune ohne Küste/Ästuar → ~0 |
| R15 | Vorkommen von Meeren | KWK Z176 | offen | wie R14; Kandidat **bewusst inaktiv** wegen Redundanz zu R14 |
| R16 | Vorkommen von Bauwerken und Infrastruktur in der Küstenzone | KWK Z177 | offen | **Mengengerüst**: Siele, Schöpfwerke und die von ihnen entwässerte Niederungsfläche (Mon. Z52 Gegenstand) |

KWK = Sheet „Klimawirkungsketten“, NW = „Schadensbaum-Netzwerkliste“, Mon. = „Risiken-Monetarisierung“
(Blattzeile), Konten = „Schadenskonten-System“, RR = „Rechenregeln“. W082 hat keinen Ausgang in der
Kette (kein Blatt nutzt W082 oder S062 als Eingang eines weiteren W-Knotens außer den Küstenknoten,
die eigene Buchungsobjekte sind).

### Weitergaben (zweispaltig; Quelle: Netzwerkliste + Abgleich-Protokoll)

| Output-Kanten (Netzwerkliste / Abgleich-Protokoll mit Punkt-Nr.) | Konto-Ausschlüsse / verwandte Buchungen (Konten-Definition, Monetarisierung) |
|---|---|
| **keine** — NW Z48 führt keine Output-IDs; das Abgleich-Protokoll hat keinen Punkt mit Quelle 47. **Eingehend:** 43 → 47 Originalkante (NW Z44; Mon. Z48 „→ 45, 46, 47, 74, 101“); **40 → 47** Abgleich **P20** (Blatt Z35, Art „Kante“; NW Z48 „Ergänzte Kanten aus Abgleich (eingehend)“ = 40; Mon. Z45 „47 (P20)“). **Ohne Kante, aber mit Buchungsweg:** Mon. Z50 (#45 Küstenschutz) „im Versagensfall laufen die Schäden über die Endpunkte **46/47** (K3/K4/K6/K1)“ — #47 nimmt damit den K6-Anteil des #45-Versagenszweigs auf; die Netzwerkliste führt diese Kante nicht (offener Punkt 4). **Der K6-Zweig von #47 selbst bleibt hier** (Baustein „K6-Mengeneffekt Pflanze“, NW Z48) und wird **nicht** an #25 weitergereicht — Begründung und Partition unten sowie Log Nr. 4. | **K8 enthält** (Konten Z66): „Defensive Ausgaben und Vorsorge: … Schutzsystem-Ertüchtigung … R7-Weiche: Mehrkosten schließen den verhinderten Schaden aus.“ **K8 schließt aus** (Z68): „Verhinderte Schäden zusätzlich (R7) · Investitionen mit Eigennutzen“. **K6 enthält** (Konten Z50): „Deckungsbeiträge der Primärproduktion: Pflanze (Menge ID 25 · Preis ID 26) …“ **K6 schließt aus** (Z52): „Preis-Transfers (R5) · nicht-marktliche Leistungen (→K7)“. #47 steht in **beiden** Buchungsobjekt-Listen: K8 (Z69) und K6 (Z53). **#47 schließt aus** (Mon. Z52): „Mehrkosten + voll verhinderte Vernässungsschäden gleichzeitig.“ **Partitionsregel-Zitate:** R7 (RR Z9) „Vorsorge-/Mehrkosten (K8) und der dadurch verhinderte Schaden schließen sich je Einheit aus. Schutzsysteme: Erwartungswert über Halte- und Versagensfall, wahrscheinlichkeitsgewichtet.“ · R9 (RR Z11) „Innerhalb eines Kontos zählt jede Einheit … genau einmal; verschiedene Konten desselben Ereignisses sind additiv.“ · R4 (RR Z6) „Wertschöpfung statt Umsatz“ für den K6-Zweig · R1 (RR Z3) Bestand oder Strom: der Vernässungsschaden ist **Strom** (Ernteausfall des Jahres); dauerhafte Bodenverschlechterung gehört zu #19. **Ohne Partitionsregel in der Mappe (offen):** #25 Ertragsausfälle (K6, Mon. Z30, „SAMMEL-BUCHUNGSOBJEKT der pflanzlichen Mengenverluste“) · #15 Vernässung (Treiber 0 €, Mon. Z20: „Bewirtschaftungsausfälle über K6“) · #52 Kanalnetze/Vorfluter/Kläranlagen (K4, Mon. Z57) · #45 Küstenschutzsysteme (K8, Mon. Z50) · #50 Hochwasserschutzsysteme (K8, Mon. Z55). |

### 1.3 Konten-Einbettung und die Aufteilung auf zwei Konten (Kern dieses Berichts)

#47 ist das erste Buchungsobjekt des Katalogs mit **zwei** Konten. Die Aufteilung wird deshalb
wörtlich aus den Arbeitsmappen hergeleitet und nicht gewählt.

**(a) Was die Mappen vorgeben.** NW Z48: Konto „K8 Mehr- & Vorsorgekosten; K6 Land-, Forst- &
Fischereiproduktion“, Bausteine „K8-Maßnahmenkosten; K6-Mengeneffekt Pflanze“. Mon. Z52:
Schadenskonto „K8 + K6“, Bewertungsansatz „Betriebs- und Ertüchtigungsmehrkosten der
Siel-/Schöpfwerksentwässerung (K8); **bei Versagen** Vernässungsschäden über K6 (**R7-Weiche**)“,
enthalten „Mehrkosten der Dauerentwässerung von Niederungen“, nicht enthalten „Mehrkosten + voll
verhinderte Vernässungsschäden gleichzeitig“, Regeln „R7“. Gegenstand (Mon. Z52): „Funktionsgrenzen
der künstlichen Dauerentwässerung tief liegender Küstenniederungen (Siele, Schöpfwerke in Marschen
und Boddenniederungen) bei steigendem Außenwasserstand und Binnenzufluss.“

**(b) Die Aufteilung ist eine Weiche, keine Summe zweier Schäden.** Das Wort „bei Versagen“ in
Mon. Z52 und die Regel R7 (RR Z9) sagen dasselbe: Für dieselbe Fläche und dieselbe Periode gibt es
genau **zwei sich ausschließende Zustände**.

| Zweig | Zustand der Entwässerung | Physische Größe vor dem Euro | Konto / Baustein | Gewicht |
|---|---|---|---|---|
| Haltefall | Siel und Schöpfwerk halten den Binnenwasserstand, aber nur mit mehr Pumparbeit, längerer Betriebszeit und vorgezogener Ertüchtigung | gepumptes Mehrvolumen (m³/a), Betriebsstunden, Ertüchtigungseinheiten | **K8 — K8-Maßnahmenkosten** (Konten Z67: „Ressourcenkosten der Maßnahmen (Ausgabenansatz)“) | \(1-p\) |
| Versagensfall | Binnenzufluss übersteigt die Leistungsfähigkeit während der Sperrzeit; die Niederung vernässt | vernässte Hektar × Ertragsverlust (t/ha) | **K6 — K6-Mengeneffekt Pflanze** (Konten Z51: „Deckungsbeitrag je Einheit“, R4) | \(p\) |

Erwartungswert je Betrachtungseinheit und Jahr (Form; die Größen selbst sind in Kap. 3 offen):

\[
S_{47} = \underbrace{(1-p)\cdot C_{K8}}_{\text{K8-Zweig}} \;+\; \underbrace{p \cdot D_{K6}}_{\text{K6-Zweig}},
\qquad 0 \le p \le 1
\]

**(c) Warum kein Euro doppelt gezählt wird.** Vier Wächter, jeder mit Regelzitat:

1. **Disjunkte Zustände (R7, RR Z9).** Die Gewichte summieren sich zu 1. Eine Fläche, die im
   Versagensfall vernässt, erzeugt in demselben Zustand keine Haltefall-Mehrkosten mehr; eine
   gehaltene Fläche erzeugt keinen Vernässungsschaden. Die Addition in der Formel addiert
   **Zustände**, nicht Schäden. Ein Modell, das \(C_{K8} + D_{K6}\) ohne Gewichte rechnet, verstößt
   wörtlich gegen Mon. Z52 („Mehrkosten + voll verhinderte Vernässungsschäden gleichzeitig“).
2. **Getrennte Einheiten (R9, RR Z11).** K8 zählt Betriebs- und Ertüchtigungseinheiten der Anlage,
   K6 zählt Hektar und Tonnen der Fläche. Innerhalb jedes Kontos zählt jede Einheit genau einmal;
   zwischen den Konten sind es verschiedene Einheiten — genau der Fall, für den R9 „verschiedene
   Konten desselben Ereignisses sind additiv“ erlaubt.
3. **Keine Verrechnung des verhinderten Schadens (K8-Ausschluss, Konten Z68).** Der Nutzen der
   funktionierenden Entwässerung erscheint ausschließlich als **kleineres \(p\)**, nie als eigene
   Buchung. Das ist der Unterschied zu #50/#45, deren Versagenszweig an **fremden** Endpunkten
   bucht; bei #47 bleibt der Versagenszweig im eigenen Bericht, weil die Mappe ihm mit
   „K6-Mengeneffekt Pflanze“ einen eigenen Baustein gibt (NW Z48).
4. **Bestand oder Strom (R1, RR Z3).** Der K6-Zweig bucht den **Ernteausfall des Jahres**. Eine
   dauerhafte Bodenverschlechterung derselben Fläche gehört zu #19 (Mon. Z30: „dauerhafte
   Bodenverschlechterung (ID 19, R1)“) und darf nicht zusätzlich hier stehen.

**(d) Partition innerhalb von K6 gegen #25 (R9; Entscheidungslog Nr. 4).** Mon. Z30 führt #25
Ertragsausfälle als „SAMMEL-BUCHUNGSOBJEKT der pflanzlichen Mengenverluste — alle Treiber
(Trockenheit, Erosion, Schädlinge, Frost …) wirken hierüber“. Eine Partitionsregel zwischen #25 und
#47 nennen die Mappen **nicht**; #47 steht aber selbst in der K6-Buchungsobjekt-Liste (Konten Z53)
und trägt den Baustein „K6-Mengeneffekt Pflanze“ (NW Z48). Beides zugleich voll zu buchen wäre eine
Doppelzählung derselben Tonne. Angewendete Ursachenpartition (Gate 1, §2.8): **Mengenverluste, deren
physische Ursache die Vernässung nach Versagen der künstlichen Dauerentwässerung ist, buchen an #47;
alle übrigen witterungsbedingten Mengenverluste derselben Fläche buchen an #25.** Die Ursachen sind
disjunkt, die Flächen dürfen sich überschneiden. Der Punkt bleibt als offener Punkt 3 geführt und ist
Prüfstoff der Gegenprüfung, weil die Partition nicht aus der Mappe zitierbar ist.

**(e) Weitere Abgrenzungen.** #52 (K4, Mon. Z57) bucht Instandsetzung und Betriebsmehrkosten der
**Abwasserinfrastruktur** (Kanalnetze, Vorfluter, Kläranlagen); #47 bucht die **Binnenentwässerung
der Niederung** (Siele, Schöpfwerke). Beide Konten sind verschieden (K4 gegen K8/K6), die
Anlagenklassen ebenfalls — die Mappen führen keine gemeinsame Anlage. #15 Vernässung ist Treiber
(0 €, Mon. Z20, R3) und bucht nicht selbst.

**(f) Konservativität.** Ohne die Zweige anderer Konten (Gebäude K3, Infrastruktur K4, Personen K1),
die eine großflächige Vernässung ebenfalls auslöst, ist die #47-Summe eine **Untergrenze**; das
gehört nach §3.6 in den Infokasten (Kap. 6). **Handlungserfordernis:** sehr dringend (NW Z48,
Mon. Z52).

## 2 Evidenz-Register (§2.2)

Skelett mit einer Zeile je Knoten der Bilanz (11 Zeilen). Die Zeilen sind in
`docs/evidenz/register.md` gespiegelt. **Wiederverwendung:** Mit #60 gemeinsame Knoten sind W074 und
W077; dort ist das Outcome der Gebäudeschaden, hier die Überlastung der Entwässerung. Nach §2.2 c
sind sie deshalb **nicht** wiederverwendbar und stehen nur als Querverweis. Die K6-Kostensatz-Zeile
(Deckungsbeitrag je Tonne) ist mit #25 potenziell teilbar, sobald eine der beiden Methodiken sie
recherchiert hat — heute existiert sie in keinem Bericht. In Formeln (§3) dürfen später nur Zeilen
mit Entscheidung **Basiswert** stehen.

| Register-ID | Knoten → Outcome | Effektgröße | Studientyp | Quelle | Übertragbarkeit | Datenlage je Zelle | Entscheidung |
|---|---|---|---|---|---|---|---|
| 47-W074-01 | W074 Meeresspiegelhöhe → Sielzugdauer / Sperrzeit am Siel | offen | offen | offen | offen | offen — Datenebene nach §3.1 zu spezifizieren | offen |
| 47-W077-01 | W077 Sturmfluten → Dauer des Sielschlusses (Ereignisspitze) | offen | offen | offen | offen | offen — Datenebene nach §3.1 zu spezifizieren | offen |
| 47-W075-01 | W075 Strömungen und Gezeitendynamik → W077 / Tidehub | offen | offen | offen | offen | offen | offen |
| 47-E01-01 | E01 Durchschnittstemperatur → W074 | offen | offen | offen | offen | offen | offen |
| 47-E17-01 | E17 Starkwind → W077 | offen | offen | offen | offen | offen | offen |
| 47-S059-01 | S059 Meerestopographie → Außenwasserstand (über W074/W077) | offen | offen | offen | offen | offen | offen (Kandidat bewusst inaktiv) |
| 47-S060-01 | S060 Wasseraustausch mit anderen Meeren → Außenwasserstand | offen | offen | offen | offen | offen | offen (Kandidat bewusst inaktiv) |
| 47-S062-01 | S062 Art und Zustand von Bauwerken und Küsteninfrastruktur → Leistungsfähigkeit der Siel-/Schöpfwerksentwässerung (Gewicht \(p\) der R7-Weiche) | Basis: offen. Maßnahmen Retention / Versickerungsflächen: im Erstaufschlag **keine nach §3.5 zulässige** Effektgröße belegt ⇒ **Abschätzung von KAP3** \(r_{\text{ret}}\) = 0,175 (Band 0,06–0,385), \(r_{\text{vers}}\) = 0,08 (Band 0,016–0,21), §5.1 | — (keine Interventionsstudie belegt) | Herleitung §5.1 (`#s062-wirkung`) | §3.9 ABGESCHÄTZT; Setzung für deutsche Küstenkommunen | kommunal (Pauschalfaktor — Modellgrenze der Abschätzung) | offen (Vorschlag: Vulnerabilität + Maßnahmen-Hebel, abgeschätzt) |
| 47-R14-01 | R14 Küsten, Wattenmeere, Ästuare → Exposition (Lackmustest §3.1) | offen | offen | offen | offen | offen | offen |
| 47-R15-01 | R15 Vorkommen von Meeren → Exposition | offen | offen | offen | offen | offen | offen (Kandidat bewusst inaktiv, redundant zu R14) |
| 47-R16-01 | R16 Bauwerke und Infrastruktur in der Küstenzone → Mengengerüst (Siele, Schöpfwerke, entwässerte Niederungsfläche) | offen | offen | offen | offen | offen — Datenebene nach §3.1 zu spezifizieren | offen |

## 3 Modell (§2.3)

<!--
Pflichtinhalte (§2.3/§3.1/§3.2/§3.6):
- Native Ergebnisgröße deklarieren (genau eine je Risiko-Code; weitere als Teil-Ausweise). Bei zwei
  Konten ist zusätzlich zu entscheiden, welcher Zweig die native Größe trägt und welcher Teil-Ausweis
  ist — Kandidat: erwartete Jahreskosten der Niederungsentwässerung (K8) nativ, erwarteter
  Vernässungs-Deckungsbeitragsverlust (K6) als zweiter Ausweis; beide getrennt sichtbar, nie nur als
  Summe. Entscheidung offen (Kap. 9).
- Schicht-B-Formel Menge × Rate × Preis je Zweig, auf Zellebene, physische Zwischengröße vor dem Euro:
  K8: Menge = entwässerte Niederungsfläche / Schöpfwerkskapazität (R16); Rate = klimabedingtes
      Mehrvolumen je ha und Jahr (W074/W077 über Sperrzeit); Preis = Pump-/Unterhaltskostensatz mit
      Preisstand (RR Z19, Annahme A4: Kostensätze vor Produktivsetzung belegen).
  K6: Menge = vernässungsgefährdete landwirtschaftliche Fläche (ha); Rate = Ertragsverlust je ha im
      Versagensfall; Preis = Deckungsbeitrag je t (R4 — nie Umsatz).
  Gewicht: p = Versagenswahrscheinlichkeit je Jahr (S062 + W074/W077).
- R7-Weiche ausdrücklich als Erwartungswert S_47 = (1-p)·C_K8 + p·D_K6 rechnen; die Wächter 1-4 aus
  Kap. 1.3 als Testfälle abbilden (u. a.: bei p=0 ist die K6-Buchung exakt 0; bei p=1 ist die
  K8-Mehrkostenbuchung exakt 0; Summe der Gewichte = 1).
- Doppelzählungs-Wächter gegen #25 nach der Partition in Kap. 1.3 (d) — als Test, nicht als Prosa.
- Je Formel alphabetische Zeichentabelle; Mini-Rechenbeispiele als Golden-Test-Blöcke.
- Lackmustest §3.1: Kommune ohne Küste/Ästuar (R14) → ~0.
- Schicht-A-Index aus denselben Knoten, nie auf Euro-Pfaden.

(a) DATENEBENEN-ANLAGEPFLICHT (§3.1): Jede benötigte Zellgröße, die das Produkt nicht führt, wird als
    Ebene vollständig spezifiziert — Quelle, Beschaffungsweg keyless, Zell-Ableitungsregel, Fallback,
    Normierung/Zentrierung — und „neu anzulegen" gekennzeichnet. Ohne offene Quelle: „geparkt
    (Datenquelle fehlt)" mit Beschaffungs-Watchlist. Kein dauerhafter, unspezifizierter
    Neutral-Fallback. Kandidaten, Spezifikation offen: Siele und Schöpfwerke je Zelle; entwässerte
    Niederungsfläche unter Tidehochwasser (Geländehöhe); Sperrzeiten/Sielzugfenster; landwirtschaftliche
    Nutzfläche der Niederung.
(c) GESCHLOSSENE BETRACHTUNGSEBENE (§3.2): Zentrierungs-/Referenzmittel entweder amtlich publiziert
    oder aus der Betrachtungsebene selbst (Kommune: eigene Zellen, im Baseline-Lauf festgehalten) —
    nie aus einer Aggregation über eine höhere Ebene; ohne zulässige Referenz bleibt der
    Modifikator neutral.

Parameter-Block-Beispiel (Format §4; Werte erst nach Herleitung eintragen):
  parameter:
    id: coastal_drainage.<name>
    wert: <Herleitungswert>
    einheit: "<Einheit>"
    band: [<unten>, <oben>]
    herkunft: register:47-<Knoten>-01      # oder herleitung:#<anker>
    quelle: <quellen-id>
    preisstand: <Jahr>                     # Pflichtfeld bei Kostensätzen
    bandzuordnung: [<Anlagentyp>]
    endpunkt: <K8-Maßnahmenkosten | K6-Mengeneffekt Pflanze>

Beispiel-Test-Block (Format §4; im echten Block mit Code-Zaun „python test: beispiel_47_<name>"):
  assert abs(<rechnung> - <erwartet>) < 1e-9
-->

## 4 Kalibrierung & Validierung (§2.4/§3.4)

<!--
Pflichtinhalte: nationaler Anker als EIN Niveau-Skalar (Anker-Zeitreihe mit Revisionsstand;
vorläufige Jahre gesondert); Kalibriermodell = Produktionsmodell; unabhängige Verteilungsprüfung auf
der kritischsten Achse — hier voraussichtlich Küstenabschnitt (Nordsee-Marsch gegen
Ostsee-Boddenniederung) und Ereignisregime (Jahre mit und ohne schwere Sturmflut) — mit vorab
fixierter Toleranz, out-of-sample; Sanity-Bänder mit Unter- und Obergrenze aus amtlicher Statistik.
Anker-Kandidaten (zu prüfen, keine Zahl ohne Quelle, P1): Ausgaben der Deich- und
Entwässerungsverbände, Länder-Generalpläne Küstenschutz. Zwei Konten heißt: ZWEI Anker, einer je
Zweig — der K8-Anker darf nicht über den K6-Zweig kalibriert werden und umgekehrt.

(b) RESSOURCEN-REGEL (§3.4): Kalibrierung, Validierung und Abgleiche nie über nationale
    100-m-Vollraster-Läufe planen — zulässig sind Bundesland-, Gemeinde-/Gemeindepunkt- und
    kommunale Stichproben-Ebene (dokumentierte Anker-Kommunen mit dem Produktionsmodell).
-->

## 5 Maßnahmen-Hebel (§2.5/§3.5)

<!--
Pflichtinhalte: Hebel nur an Ketten-Sensitivitäten; Effektgrößen aus Interventions-/
quasi-experimenteller Evidenz; marginal gegenüber heute; Doppelzählungs-Wächter gegen die
Kalibrierjahre; Wirkungsort definieren; R7-Weiche referenzieren (Maßnahmenkosten K8 hier, verhinderter
Vernässungsschaden nur als kleineres Gewicht p des K6-Zweigs, nie zusätzlich gebucht). Hebel ohne
Effektgröße: Abschätzung nach P2 (nie Wirkung null).
-->

### 5.1 Wirkungsabschätzung Retention und Versickerungsflächen an S062 (Anker `#s062-wirkung`) — §3.9 **ABGESCHÄTZT**

**Anlass (Vorgabe P2, §3.5).** Die Roadmap führt für #47 die Maßnahmen **Retention** und
**Versickerungsflächen**; im Produkt entsprechen ihnen `RETENTION_STORAGE` und `INFILTRATION_AREAS`
(`backend/app/data/catalog_parked.py`). Beide greifen an der Ketten-Sensitivität S062 „Art und
Zustand von Bauwerken und Küsteninfrastruktur“ (KWK Z171) an: Sie verändern, wie viel Binnenzufluss
die Entwässerungsbauwerke in der Sperrzeit bewältigen müssen. Für ihre Wirkung auf die Überlastung
einer **Siel-/Schöpfwerksentwässerung in der Marsch** ist im Erstaufschlag keine Interventions- oder
quasi-experimentelle Effektgröße belegt. Der Code-Bestand setzt 28 % bzw. 25 % Reduktion als
Modellannahme ohne Bericht und bezogen auf andere Risiken (`HYDROLOGICAL_STRESS_RISK_INDEX`); diese
Werte gehen hier **nicht** ein. Die Wirkung wird deshalb **nicht null** gesetzt, sondern mit der
folgenden **Abschätzung von KAP3** geführt. Im Produkt ist sie als solche samt dieser Herleitung
auszuweisen (P1).

**Wirkungsort (R7, beide Konten).** Multiplikativ auf das **klimabedingte Zusatzvolumen** \(\Delta V\)
des Binnenzuflusses, das während der Sperrzeit zurückgehalten oder gepumpt werden muss (marginal
gegenüber dem heutigen Stand, §3.5):

\[
\Delta V_{\text{mit}} = \Delta V \cdot (1 - r_{\text{ret}}) \cdot (1 - r_{\text{vers}}),
\qquad r_{\text{ret}} = s_{\text{ret}} \cdot e_{\text{ret}},
\qquad r_{\text{vers}} = s_{\text{vers}} \cdot e_{\text{vers}}
\]

\(\Delta V\) ist die gemeinsame Wurzel beider Zweige der Weiche: Es treibt die Pumparbeit des
Haltefalls (K8) **und** das Gewicht \(p\) des Versagenszweigs (K6). Die Abschätzung wirkt deshalb an
**einer** Stelle und pflanzt sich in beide Konten fort — sie wird nicht zweimal angesetzt. Die Kosten
der Maßnahmen selbst buchen als K8 an #47 (Baustein K8-Maßnahmenkosten, NW Z48); der verhinderte
Vernässungsschaden erscheint ausschließlich als kleineres \(p\) und wird nie zusätzlich gebucht
(R7, RR Z9; Mon. Z52). Beide Maßnahmen verknüpfen sich multiplikativ, nicht additiv, damit dasselbe
Zuflussvolumen nicht zweimal gemindert wird.

### 5.1.1 Zeichentabelle (Wirkungsort S062)

| Zeichen | Name | Einheit | Wert/Herkunft |
|---|---|---|---|
| \(\Delta V\) | klimabedingtes Zusatzvolumen des Binnenzuflusses in der Sperrzeit, ohne Maßnahme | m³/a | Ergebnis der Schicht-B-Rechnung aus register:47-W074-01/47-W077-01; Entscheidung und Datenebene in Kap. 1/2 als offen geführt |
| \(\Delta V_{\text{mit}}\) | dasselbe Volumen mit Maßnahmen | m³/a | berechnet nach der Formel in §5.1 |
| \(e_{\text{ret}}\) | Minderung des angeschlossenen Zusatzvolumens durch die Retention | – | 0,50 (Band 0,30–0,70) · herleitung:#s062-wirkung — Abschätzung von KAP3, keine Primärquelle (§5.1.2) |
| \(e_{\text{vers}}\) | Minderung des angeschlossenen Zusatzvolumens durch Versickerung | – | 0,40 (Band 0,20–0,60) · herleitung:#s062-wirkung — Abschätzung von KAP3, keine Primärquelle (§5.1.2) |
| \(r_{\text{ret}}\) | relative Minderung von \(\Delta V\) durch Retention | – | 0,175 (Band 0,06–0,385) · berechnet: \(s_{\text{ret}} \cdot e_{\text{ret}}\) (§5.1.2) |
| \(r_{\text{vers}}\) | relative Minderung von \(\Delta V\) durch Versickerungsflächen | – | 0,08 (Band 0,016–0,21) · berechnet: \(s_{\text{vers}} \cdot e_{\text{vers}}\) (§5.1.2) |
| \(s_{\text{ret}}\) | Anteil des Zusatzvolumens, der einer Retentionsfläche oberhalb des Siels/Schöpfwerks zugeführt werden kann | – | 0,35 (Band 0,20–0,55) · herleitung:#s062-wirkung — Abschätzung von KAP3, keine Primärquelle (§5.1.2) |
| \(s_{\text{vers}}\) | Anteil des Zusatzvolumens auf Flächen, auf denen Versickerung in der Marsch überhaupt möglich ist | – | 0,20 (Band 0,08–0,35) · herleitung:#s062-wirkung — Abschätzung von KAP3, keine Primärquelle (§5.1.2) |

### 5.1.2 Herleitung, Rechnung und Sensitivität

**Herleitung je Faktor** (alle vier Werte sind Abschätzungen von KAP3, keine Primärquelle):

- \(s_{\text{ret}}\) = 0,35 (0,20–0,55). Annahme: Die Marsch entwässert über ein Grabensystem auf
  wenige Siele und Schöpfwerke. Rückhalt ist dort möglich, wo Grabenstau, Speicherbecken oder
  Polderflächen oberhalb des Bauwerks liegen. Das Gelände ist flach, das freie Gefälle gering und ein
  Teil des Zuflusses stammt aus der oberhalb liegenden Geest, die an der Niederungsgrenze ankommt —
  dieser Teil ist erreichbar, der ortsnah anfallende Niederschlag der Niederung selbst kaum. Mitte
  gesetzt, Band asymmetrisch nach unten, weil die geringe Höhendifferenz eher gegen als für Rückhalt
  spricht.
- \(e_{\text{ret}}\) = 0,50 (0,30–0,70). Annahme: Rückhalt ist auf ein Bemessungsereignis
  dimensioniert und kappt die Spitze. Die kritischen Lagen für #47 sind aber **lange** Sperrzeiten
  (Sturmflut plus Dauerregen über mehrere Tiden); dabei füllt sich der Speicher vor dem Ende der
  Sperrzeit. Deshalb deutlich unter 1, aber nicht klein, weil schon eine Verzögerung des Zuflusses
  bis zum nächsten Sielzug wirkt.
- \(s_{\text{vers}}\) = 0,20 (0,08–0,35). Annahme: In Marschen steht das Grundwasser hoch und die
  Böden sind tonreich; eine Versickerung nach DWA-Bemessungslogik funktioniert dort nur auf sandigen
  Geesträndern und auf abgekoppelten Siedlungsflächen. Das ist die engste Größe der Kette und die
  eigentliche **Bauform-Grenze** dieser Maßnahme im Marschkontext.
- \(e_{\text{vers}}\) = 0,40 (0,20–0,60). Annahme: Wo Versickerung möglich ist, nimmt sie den Abfluss
  der angeschlossenen Fläche auf, gibt ihn aber bei anhaltender Nässe nur verzögert an den
  Grundwasserkörper ab; bei hohem Binnenwasserstand versagt die Aufnahme teilweise ganz.

**Rechnung.** \(r_{\text{ret}}\) = 0,35 · 0,50 = **0,175**; Band (gleichgerichtet) 0,20 · 0,30 =
**0,06** bis 0,55 · 0,70 = **0,385**. \(r_{\text{vers}}\) = 0,20 · 0,40 = **0,08**; Band
0,08 · 0,20 = **0,016** bis 0,35 · 0,60 = **0,21**. Beide zusammen:
\(\Delta V_{\text{mit}}/\Delta V\) = 0,825 · 0,92 = **0,759**, also **−24,1 %** statt −25,5 % bei
(unzulässiger) Addition. Band der Gesamtwirkung: −7,5 % (0,94 · 0,984 = 0,92496) bis −51,4 %
(0,615 · 0,79 = 0,48585).

**Ergebnis-Sensitivität (beide Konten).** Das klimabedingte Zusatzvolumen sinkt um 24,1 %
(Band 7,5–51,4 %). Im **K8-Zweig** sinkt die Pumparbeit des Haltefalls proportional zu \(\Delta V\),
also ebenfalls um 24,1 %, während die Maßnahmenkosten selbst (capex/opex aus dem Maßnahmenkatalog,
nicht Gegenstand dieser Abschätzung) die K8-Buchung erhöhen. Im **K6-Zweig** sinkt das Gewicht \(p\)
des Versagenszweigs und damit der erwartete Vernässungsschaden; wie stark, hängt von der in Kap. 3
noch offenen Übersetzung \(\Delta V \to p\) ab — bei einer angenommenen Elastizität 1 wäre es
dieselbe Größenordnung, bei einem Schwellenverhalten mehr. Diese Übersetzung ist Teil des Modells,
nicht dieser Abschätzung, und bleibt offen. Die Ketten sind linear, jeder Faktor hat Elastizität 1.
Einzeln variiert: \(s_{\text{ret}}\) 0,20–0,55 ⇒ \(r_{\text{ret}}\) 0,10–0,275 (größte Achse);
\(e_{\text{ret}}\) 0,30–0,70 ⇒ 0,105–0,245; \(s_{\text{vers}}\) 0,08–0,35 ⇒ \(r_{\text{vers}}\)
0,032–0,14 (größte Achse); \(e_{\text{vers}}\) 0,20–0,60 ⇒ 0,04–0,12.

**Modellgrenzen der Abschätzung.** (1) Kommunenweiter Pauschalfaktor statt einzugsgebietsscharfer
Wirkung (Bauform-Grenze); welche Zellen oberhalb welchen Siels liegen, bleibt unberücksichtigt.
(2) Versickerung ist in der Marsch bauform-begrenzt (\(s_{\text{vers}}\)); die Abschätzung darf nicht
auf Binnenstandorte übertragen werden, wo derselbe Maßnahmencode deutlich stärker wirkt.
(3) Eine Kapazitätserhöhung des Schöpfwerks selbst ist **nicht** abgebildet — sie wirkt auf die
Leistungsfähigkeit statt auf \(\Delta V\) und braucht eine eigene Abschätzung. (4) Die Wirkung auf
\(p\) und damit auf den K6-Zweig setzt die in Kap. 3 offene Übersetzung \(\Delta V \to p\) voraus.
(5) \(s_{\text{ret}}\) und \(s_{\text{vers}}\) werden messbar, sobald Einzugsgebiete der Siele und
Bodenkarten der Niederung als Ebene vorliegen; dann werden sie gemessen statt gesetzt. Ersetzt wird
die Abschätzung, sobald Interventions- oder quasi-experimentelle Evidenz gefunden ist
(§3.8-Recherche offen).

```python test: beispiel_47_s062_abschaetzung
s_ret, e_ret, s_vers, e_vers = 0.35, 0.50, 0.20, 0.40
r_ret, r_vers = s_ret * e_ret, s_vers * e_vers
assert abs(r_ret - 0.175) < 1e-12 and abs(r_vers - 0.08) < 1e-12
assert abs(0.20 * 0.30 - 0.06) < 1e-12 and abs(0.55 * 0.70 - 0.385) < 1e-12
assert abs(0.08 * 0.20 - 0.016) < 1e-12 and abs(0.35 * 0.60 - 0.21) < 1e-12
assert abs((1 - r_ret) * (1 - r_vers) - 0.759) < 1e-12
assert abs((1 - 0.06) * (1 - 0.016) - 0.92496) < 1e-12
assert abs((1 - 0.385) * (1 - 0.21) - 0.48585) < 1e-12
assert abs(0.20 * e_ret - 0.10) < 1e-12 and abs(0.55 * e_ret - 0.275) < 1e-12
assert abs(s_ret * 0.30 - 0.105) < 1e-12 and abs(s_ret * 0.70 - 0.245) < 1e-12
assert abs(0.08 * e_vers - 0.032) < 1e-12 and abs(0.35 * e_vers - 0.14) < 1e-12
assert abs(s_vers * 0.20 - 0.04) < 1e-12 and abs(s_vers * 0.60 - 0.12) < 1e-12
# R7-Wächter: die Gewichte der Weiche summieren sich zu 1, nie beide Zweige voll
p = 0.03
assert abs((1 - p) + p - 1.0) < 1e-12
```

## 6 Szenario-Anwendung & Modellgrenzen (§3.2/§3.6)

<!--
Pflichtinhalte: je empfohlenem Ansatz ein Absatz „Szenario-Anwendung" (verschobene Größe —
Außenwasserstand über E01 in W074 und über E17 in W077, daraus Sperrzeit und Binnenzufluss —,
konstante Größen, Stationaritätsannahmen, Bestand und Zustand der Entwässerungsbauwerke S062/R16);
Modellgrenzen nummeriert; Infokasten-Texte: Benennung „bewerteter Schaden — Konten K8 und K6" (nie
„Gesamtschaden"), und zwar mit BEIDEN Zweigen getrennt sichtbar (Haltefall-Mehrkosten K8;
erwarteter Vernässungsschaden K6) samt dem Satz, dass sie sich nach R7 ausschließen und nicht addiert
gelesen werden dürfen wie zwei Schäden; Vollständigkeitsanzeige; Versionsstempel „Untergrenze";
Hinweis, dass Gebäude-, Infrastruktur- und Personenschäden einer großflächigen Vernässung an anderen
Endpunkten (K3/K4/K1) gebucht werden und hier fehlen; Ausweis als Raten (je ha Niederung /
je 1.000 EW) plus aggregierte Ebene.
-->

## 7 Parameter-Blöcke (maschinenlesbar, §4)

Nur die Faktoren aus §5.1 sind beziffert. Alle weiteren Blöcke entstehen mit der Herleitung in Kap. 3/4.

```yaml
parameter:
  id: coastal_drainage.s_ret_s062
  wert: 0.35
  einheit: "-"
  band: [0.20, 0.55]
  herkunft: herleitung:#s062-wirkung     # Abschätzung von KAP3 (P1/P2)
  quelle: null
  preisstand: null
  bandzuordnung: [Retention]
  endpunkt: K8-Maßnahmenkosten + K6-Mengeneffekt Pflanze (über Delta V)
---
parameter:
  id: coastal_drainage.e_ret_s062
  wert: 0.50
  einheit: "-"
  band: [0.30, 0.70]
  herkunft: herleitung:#s062-wirkung     # Abschätzung von KAP3 (P1/P2)
  quelle: null
  preisstand: null
  bandzuordnung: [Retention]
  endpunkt: K8-Maßnahmenkosten + K6-Mengeneffekt Pflanze (über Delta V)
---
parameter:
  id: coastal_drainage.r_ret_s062
  wert: 0.175
  einheit: "-"
  band: [0.06, 0.385]
  herkunft: herleitung:#s062-wirkung     # abgeleitet: s_ret_s062 · e_ret_s062
  quelle: null
  preisstand: null
  bandzuordnung: [Retention]
  endpunkt: K8-Maßnahmenkosten + K6-Mengeneffekt Pflanze (über Delta V)
---
parameter:
  id: coastal_drainage.s_vers_s062
  wert: 0.20
  einheit: "-"
  band: [0.08, 0.35]
  herkunft: herleitung:#s062-wirkung     # Abschätzung von KAP3 (P1/P2)
  quelle: null
  preisstand: null
  bandzuordnung: [Versickerungsflächen]
  endpunkt: K8-Maßnahmenkosten + K6-Mengeneffekt Pflanze (über Delta V)
---
parameter:
  id: coastal_drainage.e_vers_s062
  wert: 0.40
  einheit: "-"
  band: [0.20, 0.60]
  herkunft: herleitung:#s062-wirkung     # Abschätzung von KAP3 (P1/P2)
  quelle: null
  preisstand: null
  bandzuordnung: [Versickerungsflächen]
  endpunkt: K8-Maßnahmenkosten + K6-Mengeneffekt Pflanze (über Delta V)
---
parameter:
  id: coastal_drainage.r_vers_s062
  wert: 0.08
  einheit: "-"
  band: [0.016, 0.21]
  herkunft: herleitung:#s062-wirkung     # abgeleitet: s_vers_s062 · e_vers_s062
  quelle: null
  preisstand: null
  bandzuordnung: [Versickerungsflächen]
  endpunkt: K8-Maßnahmenkosten + K6-Mengeneffekt Pflanze (über Delta V)
```

## 8 Quellen (§3.8)

1. KWRA-Schadensbaum × UBA-Klimawirkungsketten, Arbeitsmappe
   `docs/Schadensbaum/KWRA-Schadensbaum_X_UBA-klimawirkungsketten.xlsx` — Sheets
   „Klimawirkungsketten“ (Z2, Z18, Z168, Z169, Z171, Z175–Z177, Z181, Z182, Z184, Z189) und
   „Schadensbaum-Netzwerkliste“ (Z26, Z41, Z44, Z46, Z48, Z51, Z53).
2. KWRA-Monetarisierung, Arbeitsmappe `docs/Schadensbaum/KWRA-Monetarisierung.xlsx` — Sheets
   „Risiken-Monetarisierung“ (Z20, Z30, Z45, Z48, Z50, Z52, Z55, Z57), „Schadenskonten-System“
   (Z49–Z54 für K6, Z65–Z70 für K8), „Rechenregeln“ (Z3, Z4, Z5, Z6, Z9, Z11, Z13, Z19, Z20),
   „Abgleich-Protokoll“ (P20 = Blatt Z35).
3. Evidenz-Quellen: offen. Für S062 ist keine Primärquelle verwendet (§5.1 ABGESCHÄTZT). Der
   Code-Bestand zitiert für die beiden Maßnahmen DWA-A 138 sowie Praxiswerte zu Rückhaltebecken
   (Sieker/agrarheute) (`backend/app/data/catalog_parked.py`, `backend/app/data/catalog.py`). Sie
   sind hier nicht im Volltext geprüft, beziehen sich auf Binnenstandorte und gehen in keinen Wert ein.

<!-- Format je Quelle: Autor, Jahr, Titel, Organ, DOI/URL, Zugriffsdatum, Archiv-Snapshot;
Sekundärfunde vor Übernahme im Volltext verifizieren; Widersprüche benennen. -->

## 9 Ansatz-Vergleich (§3.7 — kein abgenommener Familien-Prototyp)

<!--
Pflicht nach §2.6, weil kein ABGENOMMENER Familien-Prototyp existiert: #50 hat die Familie
„K8-Vorsorge-Weichen" gegründet, ist aber selbst nur Erstaufschlag ohne Gegenprüfung. #47 übernimmt
die Struktur von #50 und ergänzt den zweiten Zweig (K6). Mindestens drei Ansätze a–c, festes
Kriterienraster: kausale Treue · Kalibrierbarkeit · lokale Differenzierung · Datenverfügbarkeit ·
Maßnahmen-Anschluss · Architektur-Konformität · Aufwand; Empfehlung begründet; Verworfenes ggf. als
Ergänzungsmodul. Aus der Arbeitsmappe vorgegebener Kandidat (a): R7-Erwartungswert-Weiche mit zwei
Konten — Betriebs-/Ertüchtigungsmehrkosten der Siel-/Schöpfwerksentwässerung als K8, Vernässungsschaden
im Versagensfall als K6-Mengeneffekt Pflanze, wahrscheinlichkeitsgewichtet (Mon. Z52). Weitere
Kandidaten (b), (c): offen; zu prüfen ist insbesondere, ob der K6-Zweig stattdessen an #25 gebucht
und #47 auf K8 verengt wird (widerspräche NW Z48) — als Variante (b) zu führen. Negativ-Beispiel
(§2.6/§3.1): Verteilschlüssel „nationale Ausgaben der Entwässerungsverbände × Anteil" — ausgeschieden.
-->

| Kriterium | (a) R7-Weiche mit zwei Konten (K8 + K6) | (b) offen | (c) offen |
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
| 1 | Welcher W-Knoten trägt #47, trotz abweichendem Namen? | W082 (KWK Z189) „… in niedrig gelegenen Marschgebieten“, mit W074/W077 eine Ebene tief | einziger Knoten mit dieser Wirkung, Konfidenz hoch; NW Z48 Inputs 40/43 = W074/W077; Container „Infrastruktur an der Küste“ | anderen Knoten suchen (es gibt keinen) | 11 Knoten in Bilanz und Register; Namensdivergenz NW ↔ KWK bleibt als offener Punkt 6 stehen, nicht still angeglichen (eiserne Regel 2) |
| 2 | Familie? | Struktur von #50 (K8-Vorsorge-Weichen) übernommen, Kap. 9 trotzdem angelegt | §2.6 verlangt einen **abgenommenen** Prototyp; #50 ist Erstaufschlag ohne Gegenprüfung, und #47 ergänzt einen zweiten Zweig | Kap. 9 weglassen und #50 als Prototyp behandeln | Drei-Ansätze-Vergleich bleibt Pflicht; Doppelkonto-Herleitung wird Vorlage für weitere Mehrkonten-Risiken |
| 3 | Wie wird auf zwei Konten aufgeteilt? | Zwei Zweige **einer** R7-Weiche, wahrscheinlichkeitsgewichtet: \((1-p)\cdot C_{K8} + p\cdot D_{K6}\); vier Wächter in Kap. 1.3 (c) | Mon. Z52 „bei Versagen … (R7-Weiche)“ und „Nicht enthalten: Mehrkosten + voll verhinderte Vernässungsschäden gleichzeitig“; R7 (RR Z9), R9 (RR Z11), R1 (RR Z3) | ungewichtete Addition beider Konten (verstößt wörtlich gegen Mon. Z52); nur K8 buchen (verstößt gegen NW Z48) | Modell in Kap. 3 muss die Gewichte führen; Infokasten weist beide Zweige getrennt aus |
| 4 | K6-Anteil an #47 oder an #25 (Sammel-Buchungsobjekt)? | Ursachenpartition: vernässungsbedingte Mengenverluste nach Versagen der Dauerentwässerung → #47; alle übrigen witterungsbedingten Mengenverluste → #25 | R9 (RR Z11) verlangt eine Partition, die Mappen liefern dafür kein Zitat; NW Z48 gibt #47 aber ausdrücklich den Baustein „K6-Mengeneffekt Pflanze“ | alles an #25 (dann wäre der zweite Baustein aus NW Z48 unbelegt) | Doppelzählungs-Wächter gegen #25 als Test in Kap. 3; bleibt offener Punkt 3 für die Gegenprüfung |
| 5 | Maßnahmen ohne Effektgröße | P2-Abschätzung \(r_{\text{ret}}\) = 0,175 (0,06–0,385), \(r_{\text{vers}}\) = 0,08 (0,016–0,21) an S062 | Vorgabe P2, §3.5; die Code-Werte 28 %/25 % stammen aus einem anderen Risikokontext (Binnen-Hydrologie) und erfüllen P1 nicht | Wirkung null (unzulässig nach P2); Code-Werte übernehmen (ohne Herleitung, anderer Kontext) | Maßnahmen-Modul, kein Basiswert |
| 6 | Wirkungsort der Maßnahmen | klimabedingtes Zusatzvolumen \(\Delta V\) des Binnenzuflusses, multiplikativ für beide Maßnahmen | \(\Delta V\) ist die gemeinsame Wurzel beider Zweige — ein Ansatzpunkt statt zwei, damit die Wirkung nicht je Konto erneut angesetzt wird; Multiplikation verhindert doppelte Minderung desselben Volumens | direkt auf \(p\) (unterschlägt die K8-Wirkung); je Konto getrennt ansetzen (doppelte Wirkung) | Wirkung pflanzt sich über Kap. 3 in beide Konten fort; Übersetzung \(\Delta V \to p\) bleibt offen |
| 7 | Slug | `entwaesserung_kuestenniederungen` | kurz, eindeutig gegen #52 (Kanalnetze/Kläranlagen) und #51 (Sturzfluten/Versagen von Entwässerungseinrichtungen) | `ueberlastung_entwaesserung` (verwechselbar mit #51/#52) | Dateinamen Bericht/Ledger |
