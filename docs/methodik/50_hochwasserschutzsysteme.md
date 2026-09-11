# Methodik-Bericht #50 — Belastung oder Versagen von Hochwasserschutzsystemen

Status: **Erstaufschlag (`/neu-risiko 50`) — noch nicht gegengeprüft** · 11.09.2026 ·
Instruktionsquelle: `docs/AUFGABE_METHODIK_SCHADENSRECHNUNG.md` (v2) · Umsetzungsgrundlage: **offen**
(Ansatz-Vergleich Kap. 9) · Familie: **K8-Vorsorge-Weichen (§2.6) — noch kein Prototyp, dieser Bericht ist
der erste Vertreter** (Entscheidungslog Nr. 2). Berichtsaufbau übernommen von #60/#61.

> **Geltungsbereich des Erstaufschlags.** Befüllt sind Kap. 1 (Wirkungskette, Knoten-Bilanz,
> Weitergaben, Konto) und Kap. 2 (Evidenz-Register-Skelett) aus den beiden Arbeitsmappen unter
> `docs/Schadensbaum/`. Kap. 3–9 tragen die Pflichtinhalte als Kommentar. Einzige bezifferte Größen
> sind die P2-Abschätzungen zu den Maßnahmen Deichverstärkung und Retention/Polder/Rückhaltebecken
> (§5.1, `#s076-wirkung`), ausdrücklich als **Abschätzung von KAP3** gekennzeichnet. Alle übrigen
> Entscheidungen stehen auf `offen`. Befund-Ledger: `reviews/BEFUNDE_50.md` (leer).

## Ergebnis

- **Slug:** `50_hochwasserschutzsysteme`. **Registerzeilen:** 12 (`50-<Knoten>-01`), gespiegelt in `docs/evidenz/register.md`.
- **Konto/Baustein wörtlich aus NW Z51:** „K8 Mehr- & Vorsorgekosten“ · „K8-Erwartungswert-Weiche (R7)“. Kein Abbruch (Rolle „Buchungsobjekt — Ebene B“).
- **Familie:** #61 (K8) ist nicht abgenommen und rechnet mit dem Ausgabenansatz statt mit der R7-Weiche. Deshalb gründet #50 die Familie „K8-Vorsorge-Weichen“, und Kap. 9 ist angelegt.
- **Offen:** (1) alle 12 Entscheidungen; (2) Ergebnisgröße und Ansatz (Kap. 9); (3) Versagenszweig: Die Mappe nennt „Gebäude-/Infrastruktur-/Personen-Endpunkte“ ohne IDs (Zuordnung #59/#60/#74/#101 abgeleitet); (4) Partition K8 mit #45 Küstenschutz und #47, Abgrenzung Entwässerung zu #52 (K4); (5) Doppel-Hebel S096–S098 in #60 gegen S076 hier; (6) Datenebenen Schutzanlagen und Versagenswahrscheinlichkeit; (7) Volltext-Evidenz zu beiden Maßnahmen.
- **Nacharbeitsrunden:** 0 bis zur Übergabe. Keine Websuche, also keine externe Evidenz.

## 1 Wirkungskette & Knoten-Bilanz (§2.1)

**Rolle (Rollen-Check, Schritt 2):** Sheet „Schadensbaum-Netzwerkliste“ Z51 (Id 50):
**Buchungsobjekt — Ebene B**, Feld Wasserhaushalt, Wasserwirtschaft, Handlungserfordernis **sehr
dringend**, Input-Kanten **49 Hochwasser; 51 Sturzfluten** (51 ergänzt aus Abgleich), keine
Output-Kante, Konto **K8 Mehr- & Vorsorgekosten**, Baustein **K8-Erwartungswert-Weiche (R7)**,
Anmerkung „Erwartungswert-Weiche (R7)“. Kein Abbruch nach R2/R3. Monetarisierung Z55 führt die Rolle
als „Endpunkt“ mit Konto „K8 / Erwartungswert-Weiche“.

**W-Knoten (Entscheidungslog Nr. 1):** Die Arbeitsmappe führt einen eigenen W-Knoten: Sheet
„Klimawirkungsketten“ Z226, **W103 „Belastung oder Versagen von Hochwasserschutzsystemen (insb.
Deiche)“** (Container „Infrastruktur an Binnengewässern“, Konfidenz **hoch**). Anmerkung Z226: „Keine
direkten klimatischen Einflüsse.“ Wirkungs-Eingänge sind **W085 Hochwasser** (Z208 = Id 49) und
**W087 Sturzfluten** (Z210 = Id 51). Beide sind vorgelagert. Ihre Eingänge sind eine Ebene tief mit
aufgenommen (Container-Expansion Regel 3/5, Konfidenz **mittel**). Einzige Sensitivität ist **S076**
(Z201), zugleich einziges Mitglied der Oberkategorie „Hochwasserschutzsysteme“. Der Code-Bestand
(`backend/app/data/catalog.py`, Eintrag `kwra_id: 50`) trägt dieselben Namenslisten wie W103.

### Knoten-Bilanz

Spalte „rechnet in“ ist im Erstaufschlag durchgängig `offen`. Die Spalte „Vorschlag“ nennt nur, was
die Arbeitsmappen selbst hergeben (Blatt + Zeile); sie ist keine Entscheidung.

| Knoten | Name | Blatt/Zeile | rechnet in | Vorschlag laut Arbeitsmappe |
|---|---|---|---|---|
| W085 | Hochwasser (= Id 49) | KWK Z208; NW Z50 | offen | Belastung des Schutzsystems (Originalkante 49 → 50, NW Z50, Mon. Z54 „→ 60, 74, 50, 101“). Id 49 selbst „Rein vorgelagert (0 €)“, R2 |
| W087 | Sturzfluten (= Id 51) | KWK Z210; NW Z52 | offen | zweite Belastung (Kante 51 → 50, Abgleich **P20**). Id 51 selbst „Treiber (0 €)“, R3; Entwässerungsversagen gehört zu #52 (Mon. Z56) — R9 |
| E12 | Schneeschmelze (über W085) | KWK Z13 | offen | wirkt nur über W085 (Kein-Doppelkanal §3.2): Szenario-Verschiebung der Belastung, kein eigener Faktor |
| E07 | Nässe (über W085) | KWK Z8 | offen | wie E12; Kandidat Dauerbelastung (Durchfeuchtung des Deichkörpers) — Doppelkanal mit W085 prüfen |
| E08 | Starkregen (über W085 und W087) | KWK Z9 | offen | wie E12 |
| S072 | Boden-/Vegetationsbedeckung (über W085/W087) | KWK Z197 | offen | wirkt auf Abflussbildung; bewusst inaktiv, falls der Hazard-Datensatz den Abfluss schon enthält |
| S073 | Flächenversiegelung (über W085/W087) | KWK Z198 | offen | wie S072 |
| S074 | Topographie (Geländeform, Höhe) (über W085/W087) | KWK Z199 | offen | Kandidat Lage geschützter Flächen hinter der Schutzlinie; Doppelkanal prüfen |
| S076 | Art und Zustand von Hochwasserschutzinfrastruktur | KWK Z201 | offen | Kandidat **Vulnerabilität** (Versagenswahrscheinlichkeit) und **Maßnahmen-Hebel** Deichverstärkung, Retention/Polder/Rückhaltebecken; P2-Abschätzung §5.1 |
| R17 | Vorkommen von Oberflächengewässer und Grundwasser (direkt und über W085/W087) | KWK Z204 | offen | Kandidat Exposition; Lackmustest §3.1: kein Gewässer mit Schutzanlage → ~0 |
| R18 | Vorkommen von Abwasser- und Entwässerungssystemen (direkt und über W085/W087) | KWK Z205 | offen | Entwässerung → #52 (K4, Mon. Z56 „Räumung/Instandsetzung der Entwässerung über ID 52“) — voraussichtlich bewusst inaktiv |
| R19 | Vorkommen von Infrastruktur an Binnengewässern (direkt und über W085/W087) | KWK Z206 | offen | **Mengengerüst** (Deiche, Rückhaltebecken, Talsperren, Polder — Mon. Z55 Gegenstand) |

KWK = Sheet „Klimawirkungsketten“, NW = „Schadensbaum-Netzwerkliste“, Mon. = „Risiken-Monetarisierung“
(Blattzeile), Konten = „Schadenskonten-System“. W103 hat keinen Ausgang in der Kette (kein Blatt nutzt
W103 oder S076 als Eingang).

### Weitergaben (zweispaltig; Quelle: Netzwerkliste + Abgleich-Protokoll)

| Output-Kanten (Netzwerkliste / Abgleich-Protokoll mit Punkt-Nr.) | Konto-Ausschlüsse / verwandte Buchungen (Konten-Definition, Monetarisierung) |
|---|---|
| **keine** — NW Z51 führt keine Output-IDs; das Abgleich-Protokoll hat keinen Punkt mit Quelle 50. **Eingehend:** 49 → 50 Originalkante (NW Z50; Mon. Z54); **51 → 50** Abgleich **P20** (Blatt Z38, Art „Kante“; NW Z51 „Ergänzte Kanten aus Abgleich (eingehend)“ = 51; Mon. Z56 „50 (P20)“). **Versagenszweig der R7-Weiche ohne Kante:** Mon. Z55 „Versagensschäden über die Gebäude-/Infrastruktur-/Personen-Endpunkte, wahrscheinlichkeitsgewichtet“. IDs nennt die Mappe dort nicht. Abgeleitet aus den Ausgängen von 49 (Mon. Z54: 60, 74, 101) und 51 (Mon. Z56: 59, 74, 101): #60/#59 (K3), #74 (K4), #101 (K1) — offener Punkt 3. | **K8 enthält** (Konten Z66): „… Schutzsystem-Ertüchtigung …“; **K8 schließt aus** (Konten Z68): „Verhinderte Schäden zusätzlich (R7) · Investitionen mit Eigennutzen“. **#50 schließt aus** (Mon. Z55): „Schutzkosten + verhinderte Schäden voll addiert.“ **Partitionsregel-Zitate:** R7 (Rechenregeln Z9): „Vorsorge-/Mehrkosten (K8) und der dadurch verhinderte Schaden schließen sich je Einheit aus. Schutzsysteme: Erwartungswert über Halte- und Versagensfall, wahrscheinlichkeitsgewichtet.“ #60 (Mon. Z65): „Nicht enthalten: … Schutzkosten (ID 50, R7)“. R9 (Z11): „Innerhalb eines Kontos zählt jede Einheit … genau einmal“. **Ohne Partitionsregel in der Mappe (offen):** #45 Küstenschutzsysteme (K8, Mon. Z50: „Analog“-Vorbild, gleiche Weiche) — Abgrenzung Fluss-/Küstendeich; #47 Entwässerung Küstenniederungen (K8 + K6, Mon. Z52); #52 Entwässerung (K4) gegen den Sturzflut-Eingang 51. |

### Konto-Einbettung

- **Konto:** K8 Mehr- und Vorsorgekosten — Definition (Konten Z66): „Defensive Ausgaben und Vorsorge:
  Kühlung, Beschneiung, Bewässerungsersatz, Grünunterhalt, Schutzsystem-Ertüchtigung, Bekämpfung,
  Planung, Gesundheitsvorhaltung; … R7-Weiche: Mehrkosten schließen den verhinderten Schaden aus.“
  Kostensatz-Typ (Z67): „Ressourcenkosten der Maßnahmen (Ausgabenansatz)“. #50 steht in der
  Buchungsobjekt-Liste (Z69); Id 49 unter „Wirkt hierauf“ (Z70).
- **Bewertungsbaustein:** K8-Erwartungswert-Weiche (R7) (NW Z51). Bewertungsansatz (Mon. Z55): „Analog
  Küstenschutz (R7): Ertüchtigung/Unterhalt als K8; Versagensschäden über die
  Gebäude-/Infrastruktur-/Personen-Endpunkte, wahrscheinlichkeitsgewichtet.“ Gegenstand: „Beanspruchung
  und Versagensrisiko technischer Hochwasserschutzsysteme (Deiche, Rückhaltebecken, Talsperren, Polder)
  einschließlich des verbleibenden Restrisikos.“ Enthalten: „Schutzkosten des technischen
  Hochwasserschutzes.“ Vorbild #45 (Mon. Z50): „Beide Zweige wahrscheinlichkeitsgewichtet, nie beide voll.“
- **Rechenregeln:** R7 (Mon. Z55, Spalte „Regeln“); dazu Annahme A5 Ereignislogik (Rechenregeln Z20):
  „Schutzsysteme über die R7-Erwartungswert-Weiche“.
- **Handlungserfordernis:** sehr dringend (Mon. Z55, NW Z51).
- **Nur K8 aktiv:** Der Versagenszweig bucht an den Endpunkten (K3/K4/K1), nicht hier — Untergrenze
  des Hochwasser-Gesamtbilds, im Infokasten zu benennen (§3.6).

## 2 Evidenz-Register (§2.2)

Skelett mit einer Zeile je Knoten der Bilanz. Die Zeilen sind in `docs/evidenz/register.md`
gespiegelt. **Wiederverwendung:** Mit #60 gemeinsame Knoten sind W085, W087, E12, E07, E08, S072–S074,
R17–R19. Deren #60-Zeilen haben ein anderes Outcome (Überflutung/Gebäudeschaden), hier ist es Belastung
bzw. Versagen des Schutzsystems. Nach §2.2 c sind sie deshalb **nicht** wiederverwendbar und stehen nur
als Querverweis. In Formeln (§3) dürfen später nur Zeilen mit Entscheidung **Basiswert** stehen.

| Register-ID | Knoten → Outcome | Effektgröße | Studientyp | Quelle | Übertragbarkeit | Datenlage je Zelle | Entscheidung |
|---|---|---|---|---|---|---|---|
| 50-W085-01 | W085 Hochwasser → Belastung des Schutzsystems (Wasserstand/Dauer an der Anlage) | offen | offen | offen | offen | offen — Datenebene nach §3.1 zu spezifizieren | offen |
| 50-W087-01 | W087 Sturzfluten → Belastung des Überflutungsschutzes | offen | offen | offen | offen | offen | offen |
| 50-E12-01 | E12 Schneeschmelze → W085 | offen | offen | offen | offen | offen | offen |
| 50-E07-01 | E07 Nässe → W085 / Durchfeuchtung Deichkörper | offen | offen | offen | offen | offen | offen |
| 50-E08-01 | E08 Starkregen → W085/W087 | offen | offen | offen | offen | offen | offen |
| 50-S072-01 | S072 Boden-/Vegetationsbedeckung → Abfluss (W085/W087) | offen | offen | offen | offen | offen | offen |
| 50-S073-01 | S073 Flächenversiegelung → Abfluss (W085/W087) | offen | offen | offen | offen | offen | offen |
| 50-S074-01 | S074 Topographie → geschützte Fläche hinter der Schutzlinie | offen | offen | offen | offen | offen | offen |
| 50-S076-01 | S076 Art und Zustand der Schutzinfrastruktur → Versagenswahrscheinlichkeit | Basis: offen. Maßnahmen Deichverstärkung / Retention: im Erstaufschlag **keine nach §3.5 zulässige** Effektgröße belegt ⇒ **Abschätzung von KAP3** \(r_{\text{deich}}\) = 0,35 (Band 0,15–0,63), \(r_{\text{ret}}\) = 0,24 (Band 0,08–0,48), §5.1 | — (keine Interventionsstudie belegt) | Herleitung §5.1 (`#s076-wirkung`) | §3.9 ABGESCHÄTZT; Setzung für deutsche Kommunen | kommunal (Pauschalfaktor — Modellgrenze der Abschätzung) | offen (Vorschlag: Vulnerabilität + Maßnahmen-Hebel, abgeschätzt) |
| 50-R17-01 | R17 Oberflächengewässer → Exposition | offen | offen | offen | offen | offen | offen |
| 50-R18-01 | R18 Entwässerungssysteme → Versagen Überflutungsschutz | offen | offen | offen | offen | offen | offen |
| 50-R19-01 | R19 Infrastruktur an Binnengewässern → Mengengerüst (Schutzanlagen) | offen | offen | offen | offen | offen — Datenebene nach §3.1 zu spezifizieren | offen |

## 3 Modell (§2.3)

<!--
Pflichtinhalte (§2.3/§3.1/§3.2/§3.6):
- Native Ergebnisgröße deklarieren (genau eine je Risiko-Code; weitere als Teil-Ausweise).
  Kandidat laut Mon. Z55/R7: Ertüchtigungs- und Unterhaltsmehrkosten K8 je Jahr der Schutzsysteme der
  Kommune; die Versagenswahrscheinlichkeit ist Gewicht der Weiche, der Versagensschaden bucht an den
  Endpunkten — Entscheidung offen.
- Schicht-B-Formel Menge × Rate × Preis auf Zellebene: Menge = Schutzanlagen (km Deich, m³
  Rückhaltevolumen, R19); Rate = klimabedingter Mehraufwand bzw. Versagenswahrscheinlichkeit (S076,
  W085/W087); Preis = Kostensatz mit Preisstand. Physische Zwischengröße vor dem Euro.
- R7-Weiche ausdrücklich: Halte- und Versagensfall wahrscheinlichkeitsgewichtet, nie beide voll.
- Je Formel alphabetische Zeichentabelle; Mini-Rechenbeispiele als Golden-Test-Blöcke.
- Lackmustest §3.1: Kommune ohne Gewässer mit Schutzanlage → ~0.
- Schicht-A-Index aus denselben Knoten, nie auf Euro-Pfaden.

(a) DATENEBENEN-ANLAGEPFLICHT (§3.1): Jede benötigte Zellgröße, die das Produkt nicht führt, wird als
    Ebene vollständig spezifiziert — Quelle, Beschaffungsweg keyless, Zell-Ableitungsregel, Fallback,
    Normierung/Zentrierung — und „neu anzulegen“ gekennzeichnet. Ohne offene Quelle: „geparkt
    (Datenquelle fehlt)“ mit Beschaffungs-Watchlist. Kein dauerhafter, unspezifizierter
    Neutral-Fallback. Kandidaten, Spezifikation offen: Schutzanlagen je Zelle (Deichlinien,
    Rückhaltebecken, Polder); Zustand der Anlagen — der Code-Bestand parkt eine Ebene
    LEVEE_CONDITION (`backend/app/data/catalog_parked.py`).
(c) GESCHLOSSENE BETRACHTUNGSEBENE (§3.2): Zentrierungs-/Referenzmittel entweder amtlich publiziert
    oder aus der Betrachtungsebene selbst (Kommune: eigene Zellen, im Baseline-Lauf festgehalten) —
    nie aus einer Aggregation über eine höhere Ebene; ohne zulässige Referenz bleibt der
    Modifikator neutral.

Parameter-Block-Beispiel (Format §4; Werte erst nach Herleitung eintragen):
  parameter:
    id: flood_protect.<name>
    wert: <Herleitungswert>
    einheit: "<Einheit>"
    band: [<unten>, <oben>]
    herkunft: register:50-<Knoten>-01      # oder herleitung:#<anker>
    quelle: <quellen-id>
    preisstand: <Jahr>                     # Pflichtfeld bei Kostensätzen
    bandzuordnung: [<Anlagentyp>]
    endpunkt: <K8-Erwartungswert-Weiche>

Beispiel-Test-Block (Format §4; im echten Block mit Code-Zaun „python test: beispiel_50_<name>“):
  assert abs(<rechnung> - <erwartet>) < 1e-9
-->

## 4 Kalibrierung & Validierung (§2.4/§3.4)

<!--
Pflichtinhalte: nationaler Anker als EIN Niveau-Skalar (Anker-Zeitreihe mit Revisionsstand;
vorläufige Jahre gesondert); Kalibriermodell = Produktionsmodell; unabhängige Verteilungsprüfung auf
der kritischsten Achse — hier voraussichtlich das Ereignisregime (Jahre mit und ohne Großhochwasser)
und Anlagentyp — mit vorab fixierter Toleranz, out-of-sample; Sanity-Bänder mit Unter- und Obergrenze
aus amtlicher Statistik (Kandidaten: Hochwasserschutz-Ausgaben der Länder). Anker-Kandidaten und
Zahlen: offen (keine Zahl ohne Quelle, P1).

(b) RESSOURCEN-REGEL (§3.4): Kalibrierung, Validierung und Abgleiche nie über nationale
    100-m-Vollraster-Läufe planen — zulässig sind Bundesland-, Gemeinde-/Gemeindepunkt- und
    kommunale Stichproben-Ebene (dokumentierte Anker-Kommunen mit dem Produktionsmodell).
-->

## 5 Maßnahmen-Hebel (§2.5/§3.5)

<!--
Pflichtinhalte: Hebel nur an Ketten-Sensitivitäten; Effektgrößen aus Interventions-/
quasi-experimenteller Evidenz; marginal gegenüber heute; Doppelzählungs-Wächter gegen die
Kalibrierjahre; Wirkungsort definieren; R7-Weiche referenzieren (Maßnahmenkosten K8 hier, verhinderter
Schaden nur als gesenktes Gewicht des Versagenszweigs, nie zusätzlich gebucht). Hebel ohne Effektgröße:
Abschätzung nach P2 (nie Wirkung null).
-->

### 5.1 Wirkungsabschätzung Deichverstärkung und Retention/Polder/Rückhaltebecken an S076 (Anker `#s076-wirkung`) — §3.9 **ABGESCHÄTZT**

**Anlass (Vorgabe P2, §3.5).** Das Produkt führt die Maßnahmen „Deichverstärkung / Barrieren“
(`LEVEE_REINFORCEMENT`) und „Retention / Polder / Rückhaltebecken“ (`RETENTION_POLDER_RESERVOIR`). Beide
greifen an der Ketten-Sensitivität S076 „Art und Zustand von Hochwasserschutzinfrastruktur“ (KWK Z201)
an: die Verstärkung am Zustand, die Retention an der Art des Schutzsystems. Für ihre Wirkung auf die
Versagenswahrscheinlichkeit ist im Erstaufschlag keine Interventions- oder quasi-experimentelle
Effektgröße belegt. Der Code-Bestand setzt 35 % bzw. 30 % Reduktion als Modellannahme ohne Bericht
(`backend/app/data/catalog.py`); diese Werte gehen hier **nicht** ein. Die Wirkung wird deshalb **nicht
null** gesetzt, sondern mit der folgenden **Abschätzung von KAP3** geführt. Im Produkt ist sie als solche
samt dieser Herleitung auszuweisen (P1).

**Wirkungsort (R7).** Multiplikativ auf die jährliche Versagenswahrscheinlichkeit der Schutzsysteme der
Kommune, also auf das Gewicht des Versagenszweigs der Weiche:

\[
p_{\text{mit}} = p_{\text{vers}} \cdot (1 - r_{\text{deich}}) \cdot (1 - r_{\text{ret}}),
\qquad r_{\text{deich}} = a_{\text{def}} \cdot e_{\text{def}},
\qquad r_{\text{ret}} = s_{\text{vol}} \cdot e_{\text{ret}}
\]

Die Kosten der Maßnahmen buchen als K8 an #50. Der verhinderte Schaden erscheint nur als kleineres
Gewicht des Versagenszweigs an den Endpunkten (#59/#60, #74, #101) und wird nie zusätzlich gebucht (R7,
Rechenregeln Z9). Beide Maßnahmen verknüpfen sich multiplikativ, nicht additiv, damit dieselbe
Versagenswahrscheinlichkeit nicht zweimal gemindert wird.

### 5.1.1 Zeichentabelle (Wirkungsort S076)

| Zeichen | Name | Einheit | Wert/Herkunft |
|---|---|---|---|
| \(a_{\text{def}}\) | Anteil der Versagenswahrscheinlichkeit aus Versagen unterhalb des Bemessungswasserstands (Durchsickerung, Erosion, Zustandsmängel) | – | 0,50 (Band 0,30–0,70) · herleitung:#s076-wirkung — Abschätzung von KAP3, keine Primärquelle (§5.1.2) |
| \(e_{\text{def}}\) | Minderung dieses Anteils am verstärkten Deichabschnitt | – | 0,70 (Band 0,50–0,90) · herleitung:#s076-wirkung — Abschätzung von KAP3, keine Primärquelle (§5.1.2) |
| \(e_{\text{ret}}\) | Minderung der Versagenswahrscheinlichkeit in Ereignissen, deren Scheitel die Retention kappen kann | – | 0,40 (Band 0,20–0,60) · herleitung:#s076-wirkung — Abschätzung von KAP3, keine Primärquelle (§5.1.2) |
| \(p_{\text{mit}}\) | Versagenswahrscheinlichkeit mit Maßnahmen | 1/a | berechnet nach der Formel in §5.1 |
| \(p_{\text{vers}}\) | Versagenswahrscheinlichkeit der Schutzsysteme der Kommune ohne Maßnahme (heutiger Bestand) | 1/a | Ergebnis der Schicht-B-Rechnung aus register:50-S076-01; Entscheidung und Datenebene in Kap. 1/2 als offen geführt |
| \(r_{\text{deich}}\) | relative Minderung von \(p_{\text{vers}}\) durch Deichverstärkung | – | 0,35 (Band 0,15–0,63) · berechnet: \(a_{\text{def}} \cdot e_{\text{def}}\) (§5.1.2) |
| \(r_{\text{ret}}\) | relative Minderung von \(p_{\text{vers}}\) durch Retention/Polder/Rückhaltebecken | – | 0,24 (Band 0,08–0,48) · berechnet: \(s_{\text{vol}} \cdot e_{\text{ret}}\) (§5.1.2) |
| \(s_{\text{vol}}\) | Anteil der Belastungsereignisse, deren Scheitel das Rückhaltevolumen kappen kann | – | 0,60 (Band 0,40–0,80) · herleitung:#s076-wirkung — Abschätzung von KAP3, keine Primärquelle (§5.1.2) |

### 5.1.2 Herleitung, Rechnung und Sensitivität

**Herleitung je Faktor** (alle vier Werte sind Abschätzungen von KAP3, keine Primärquelle):

- \(a_{\text{def}}\) = 0,50 (0,30–0,70). Annahme: Flussdeiche versagen teils durch Überströmen oberhalb
  des Bemessungswasserstands, teils vorher durch Durchsickerung, Erosion oder Zustandsmängel. Eine
  Verstärkung auf das bestehende Bemessungsniveau wirkt nur auf den zweiten Anteil. Ohne ausgewertete
  Statistik nach Versagensart wird die Mitte gesetzt, Band symmetrisch.
- \(e_{\text{def}}\) = 0,70 (0,50–0,90). Annahme: Die Ertüchtigung nach Stand der Technik beseitigt die
  Zustandsmängel des Abschnitts weitgehend. Restversagen bleibt durch Untergrund, Wühltiere, Treibgut
  und späteren Unterhaltsrückstand. Obergrenze unter 1, weil kein Deich unterhalb der Bemessung sicher ist.
- \(s_{\text{vol}}\) = 0,60 (0,40–0,80). Annahme: Häufige Hochwasser passen ins Rückhaltevolumen.
  Seltene, lange und volumenreiche Ereignisse füllen es vor dem Scheitel, und Steuerung zu früh oder zu
  spät verschenkt Wirkung. Untere Grenze: kleine Becken im großen Einzugsgebiet. Obere: großer Polder
  nahe am Schutzabschnitt.
- \(e_{\text{ret}}\) = 0,40 (0,20–0,60). Annahme: Eine Scheitelkappung senkt den Wasserstand am
  Schutzsystem nur um einen Teil. Die Versagenswahrscheinlichkeit sinkt unterproportional, weil
  Durchsickerung auch von der Einstaudauer abhängt, die Retention kaum verkürzt.

**Rechnung.** \(r_{\text{deich}}\) = 0,50 · 0,70 = **0,35**; Band (gleichgerichtet) 0,30 · 0,50 =
**0,15** bis 0,70 · 0,90 = **0,63**. \(r_{\text{ret}}\) = 0,60 · 0,40 = **0,24**; Band 0,40 · 0,20 =
**0,08** bis 0,80 · 0,60 = **0,48**. Beide zusammen: \(p_{\text{mit}}/p_{\text{vers}}\) = 0,65 · 0,76 =
**0,494**, also −50,6 % statt −59 % bei (unzulässiger) Addition.

**Ergebnis-Sensitivität.** Das Gewicht des Versagenszweigs und damit der wahrscheinlichkeitsgewichtete
Versagensschaden an den Endpunkten sinkt um 35 % (Band 15–63 %) bei Deichverstärkung und um 24 % (Band
8–48 %) bei Retention. Die K8-Buchung von #50 steigt um die Maßnahmenkosten (Kostensätze aus dem
Maßnahmenkatalog, nicht Gegenstand dieser Abschätzung). Die Ketten sind linear, jeder Faktor hat
Elastizität 1. Einzeln variiert: \(a_{\text{def}}\) 0,30–0,70 ⇒ \(r_{\text{deich}}\) 0,21–0,49 (größte
Achse); \(e_{\text{def}}\) 0,50–0,90 ⇒ 0,25–0,45; \(e_{\text{ret}}\) 0,20–0,60 ⇒ \(r_{\text{ret}}\)
0,12–0,36 (größte Achse); \(s_{\text{vol}}\) 0,40–0,80 ⇒ 0,16–0,32.

**Modellgrenzen der Abschätzung.** (1) Kommunenweiter Pauschalfaktor statt abschnittsscharfer Wirkung
(Bauform-Grenze); welche Zellen hinter dem verstärkten Abschnitt liegen, bleibt unberücksichtigt.
(2) Eine Deicherhöhung über das Bemessungsniveau hinaus ist nicht abgebildet; sie würde das Überströmen
mindern und braucht eine eigene Abschätzung. (3) Retention wirkt am Unterlieger, oft außerhalb der
Kommune, die sie baut; die Abschätzung gilt nur für Schutzsysteme derselben Betrachtungsebene (§3.2).
(4) \(a_{\text{def}}\) wird messbar, sobald eine Versagensstatistik nach Versagensart vorliegt; dann wird
er gemessen statt gesetzt. Ersetzt wird die Abschätzung, sobald Interventions- oder quasi-experimentelle
Evidenz gefunden ist (§3.8-Recherche offen).

```python test: beispiel_50_s076_abschaetzung
a_def, e_def, s_vol, e_ret = 0.50, 0.70, 0.60, 0.40
r_deich, r_ret = a_def * e_def, s_vol * e_ret
assert abs(r_deich - 0.35) < 1e-12 and abs(r_ret - 0.24) < 1e-12
assert abs(0.30 * 0.50 - 0.15) < 1e-12 and abs(0.70 * 0.90 - 0.63) < 1e-12
assert abs(0.40 * 0.20 - 0.08) < 1e-12 and abs(0.80 * 0.60 - 0.48) < 1e-12
assert abs((1 - r_deich) * (1 - r_ret) - 0.494) < 1e-12
assert abs(0.30 * e_def - 0.21) < 1e-12 and abs(0.70 * e_def - 0.49) < 1e-12
assert abs(a_def * 0.50 - 0.25) < 1e-12 and abs(a_def * 0.90 - 0.45) < 1e-12
assert abs(s_vol * 0.20 - 0.12) < 1e-12 and abs(s_vol * 0.60 - 0.36) < 1e-12
assert abs(0.40 * e_ret - 0.16) < 1e-12 and abs(0.80 * e_ret - 0.32) < 1e-12
```

## 6 Szenario-Anwendung & Modellgrenzen (§3.2/§3.6)

<!--
Pflichtinhalte: je empfohlenem Ansatz ein Absatz „Szenario-Anwendung“ (verschobene Größe — Belastung
über E12/E07/E08 in W085/W087 —, konstante Größen, Stationaritätsannahmen, Bestand und Zustand der
Schutzanlagen S076/R19); Modellgrenzen nummeriert; Infokasten-Texte: Benennung „bewerteter Schaden —
Konto K8“ (nie „Gesamtschaden“), Vollständigkeitsanzeige, Versionsstempel „Untergrenze“; Hinweis, dass
der Versagensschaden an den Endpunkten #59/#60 (K3), #74 (K4) und #101 (K1) gebucht wird; Ausweis als
Raten (je km Schutzlinie / je 1.000 EW) plus aggregierte Ebene.
-->

## 7 Parameter-Blöcke (maschinenlesbar, §4)

Nur die Faktoren aus §5.1 sind beziffert. Alle weiteren Blöcke entstehen mit der Herleitung in Kap. 3/4.

```yaml
parameter:
  id: flood_protect.a_def_s076
  wert: 0.50
  einheit: "-"
  band: [0.30, 0.70]
  herkunft: herleitung:#s076-wirkung     # Abschätzung von KAP3 (P1/P2)
  quelle: null
  preisstand: null
  bandzuordnung: [Deich]
  endpunkt: K8-Erwartungswert-Weiche
---
parameter:
  id: flood_protect.e_def_s076
  wert: 0.70
  einheit: "-"
  band: [0.50, 0.90]
  herkunft: herleitung:#s076-wirkung     # Abschätzung von KAP3 (P1/P2)
  quelle: null
  preisstand: null
  bandzuordnung: [Deich]
  endpunkt: K8-Erwartungswert-Weiche
---
parameter:
  id: flood_protect.r_deich_s076
  wert: 0.35
  einheit: "-"
  band: [0.15, 0.63]
  herkunft: herleitung:#s076-wirkung     # abgeleitet: a_def_s076 · e_def_s076
  quelle: null
  preisstand: null
  bandzuordnung: [Deich]
  endpunkt: K8-Erwartungswert-Weiche
---
parameter:
  id: flood_protect.s_vol_s076
  wert: 0.60
  einheit: "-"
  band: [0.40, 0.80]
  herkunft: herleitung:#s076-wirkung     # Abschätzung von KAP3 (P1/P2)
  quelle: null
  preisstand: null
  bandzuordnung: [Retention/Polder/Rückhaltebecken]
  endpunkt: K8-Erwartungswert-Weiche
---
parameter:
  id: flood_protect.e_ret_s076
  wert: 0.40
  einheit: "-"
  band: [0.20, 0.60]
  herkunft: herleitung:#s076-wirkung     # Abschätzung von KAP3 (P1/P2)
  quelle: null
  preisstand: null
  bandzuordnung: [Retention/Polder/Rückhaltebecken]
  endpunkt: K8-Erwartungswert-Weiche
---
parameter:
  id: flood_protect.r_ret_s076
  wert: 0.24
  einheit: "-"
  band: [0.08, 0.48]
  herkunft: herleitung:#s076-wirkung     # abgeleitet: s_vol_s076 · e_ret_s076
  quelle: null
  preisstand: null
  bandzuordnung: [Retention/Polder/Rückhaltebecken]
  endpunkt: K8-Erwartungswert-Weiche
```

## 8 Quellen (§3.8)

1. KWRA-Schadensbaum × UBA-Klimawirkungsketten, Arbeitsmappe
   `docs/Schadensbaum/KWRA-Schadensbaum_X_UBA-klimawirkungsketten.xlsx` — Sheets
   „Klimawirkungsketten“ (Z8, Z9, Z13, Z197–Z199, Z201, Z204–Z206, Z208, Z210, Z226) und
   „Schadensbaum-Netzwerkliste“ (Z50, Z51, Z52).
2. KWRA-Monetarisierung, Arbeitsmappe `docs/Schadensbaum/KWRA-Monetarisierung.xlsx` — Sheets
   „Risiken-Monetarisierung“ (Z50, Z52, Z54–Z56, Z65), „Schadenskonten-System“ (Z65–Z70),
   „Rechenregeln“ (Z4, Z5, Z9, Z11, Z20), „Abgleich-Protokoll“ (P20 = Blatt Z38).
3. Evidenz-Quellen: offen. Für S076 ist keine Primärquelle verwendet (§5.1 ABGESCHÄTZT). Der
   Code-Bestand zitiert für die Maßnahmen den NLWKN-Generalplan Küstenschutz sowie Praxiswerte zu
   Rückhaltebecken (Sieker/agrarheute) (`backend/app/data/catalog.py`). Sie sind hier nicht im Volltext
   geprüft und gehen in keinen Wert ein.

<!-- Format je Quelle: Autor, Jahr, Titel, Organ, DOI/URL, Zugriffsdatum, Archiv-Snapshot;
Sekundärfunde vor Übernahme im Volltext verifizieren; Widersprüche benennen. -->

## 9 Ansatz-Vergleich (§3.7 — erster Vertreter der Familie K8-Vorsorge-Weichen)

<!--
Pflicht nach §2.6, weil kein abgenommener Familien-Prototyp existiert (docs/methodik/ führt K1-Berichte
#95/#96/#98 und die nicht gegengeprüften Erstaufschläge #60 (K3) und #61 (K8, Ausgabenansatz ohne
Weiche)). Mindestens drei Ansätze a–c, festes Kriterienraster: kausale Treue · Kalibrierbarkeit · lokale
Differenzierung · Datenverfügbarkeit · Maßnahmen-Anschluss · Architektur-Konformität · Aufwand;
Empfehlung begründet; Verworfenes ggf. als Ergänzungsmodul. Aus der Arbeitsmappe vorgegebener Kandidat
(a): R7-Erwartungswert-Weiche — Ertüchtigung/Unterhalt der Schutzanlagen als K8, Versagenszweig
wahrscheinlichkeitsgewichtet an den Endpunkten (Mon. Z55, Vorbild #45 Z50). Weitere Kandidaten (b), (c):
offen. Negativ-Beispiel (§2.6/§3.1): Verteilschlüssel „nationale Hochwasserschutz-Ausgaben × Anteil“ —
ausgeschieden.
-->

| Kriterium | (a) R7-Erwartungswert-Weiche | (b) offen | (c) offen |
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
| 1 | Welcher W-Knoten trägt #50? | W103 (KWK Z226), mit W085/W087 eine Ebene tief | eigener, namensgleicher Knoten mit Konfidenz hoch; NW Z51 Inputs 49/51 = W085/W087 | nur W103 ohne Vorstufen (dann fehlten die Belastungstreiber E12/E07/E08, S072–S074) | 12 Knoten in Bilanz und Register |
| 2 | Familie? | neue Familie K8-Vorsorge-Weichen, Kap. 9 angelegt; Berichtsaufbau von #60/#61 übernommen | kein abgenommener K8-Bericht; #61 rechnet Ausgabenansatz ohne Weiche, #50 die R7-Weiche (NW Z51); §2.6 nennt „K8-Vorsorge-Weichen“ als eigene Familie | Einordnung unter #61 (K8-Vorsorge/Mehrkosten) — andere Bewertungslogik | Drei-Ansätze-Vergleich Pflicht; Vorlage für #45/#47 |
| 3 | Maßnahmen ohne Effektgröße | P2-Abschätzung \(r_{\text{deich}}\) = 0,35 (0,15–0,63), \(r_{\text{ret}}\) = 0,24 (0,08–0,48) an S076 | Vorgabe P2, §3.5; Code-Werte 35 %/30 % ohne Bericht erfüllen P1 nicht | Wirkung null (unzulässig nach P2); Code-Werte übernehmen (ohne Herleitung) | Maßnahmen-Modul, kein Basiswert |
| 4 | Wirkungsort | Gewicht des Versagenszweigs \(p_{\text{vers}}\), multiplikativ für beide Maßnahmen | R7 (Rechenregeln Z9): verhinderter Schaden nie zusätzlich; Multiplikation verhindert doppelte Minderung | Minderung der K8-Buchung (Vorzeichenfehler: Maßnahmen erhöhen K8) | Euro-Wirkung an #59/#60/#74/#101, Kosten an #50 |
| 5 | Slug | `hochwasserschutzsysteme` | kurz, eindeutig gegen #45 (Küstenschutzsysteme) und #49 (Hochwasser) | `versagen_hochwasserschutz` (verengt auf den Versagensfall) | Dateinamen Bericht/Ledger |
