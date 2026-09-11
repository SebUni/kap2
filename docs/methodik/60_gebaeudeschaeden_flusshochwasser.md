# Methodik-Bericht #60 — Schäden an Gebäuden aufgrund von Flusshochwasser

Status: **Erstaufschlag (`/neu-risiko 60`) — noch nicht gegengeprüft** · 11.09.2026 ·
Instruktionsquelle: `docs/AUFGABE_METHODIK_SCHADENSRECHNUNG.md` (v2) · Umsetzungsgrundlage: **offen**
(Ansatz-Vergleich Kap. 9) · Familie: **K3/K4-Ereignisschäden — noch kein Prototyp, dieser Bericht ist
der erste Vertreter** (§2.6; Entscheidungslog Nr. 2)

> **Geltungsbereich des Erstaufschlags.** Befüllt sind Kap. 1 (Wirkungskette, Knoten-Bilanz,
> Weitergaben, Konto) und Kap. 2 (Evidenz-Register-Skelett) aus den beiden Arbeitsmappen unter
> `docs/Schadensbaum/`; Kap. 3–9 tragen die Pflichtinhalte als Kommentar. Einzige bezifferte
> Größe ist die P2-Abschätzung zum Maßnahmen-Hebel S092 (§5.1, `#s092-wirkung`), ausdrücklich als
> **Abschätzung von KAP3** gekennzeichnet. Alle übrigen Entscheidungen stehen auf `offen`.
> Befund-Ledger: `reviews/BEFUNDE_60.md` (leer).

## Ergebnis

- **Slug:** `60_gebaeudeschaeden_flusshochwasser`. **Registerzeilen:** 32 (`60-<Knoten>-01`), gespiegelt in `docs/evidenz/register.md`.
- **Offen:** (1) alle 32 Entscheidungen; (2) Ergebnisgröße und Ansatz (Kap. 9); (3) Datenebenen nach §3.1; (4) R9-Partitionen in K3 mit #92/#102/#55 und R5 über „Wie ID 59“; (5) Volltext-Evidenz zu S092.
- **Aufwand Erstaufschlag:** 1 Nacharbeitsrunde (Planungszahl korrigiert, Platzhalter-Code-Zaun entfernt). Erstaufschlag: eine Session, 26 Werkzeugaufrufe, rund 3,2 USD. Nacharbeit: rund 0,3 USD. Keine Websuche, also keine externe Evidenz.
- **Planung:** Gegenprüfung ist nicht Teil des Tickets und noch nicht gemessen. Vergleich laut `reviews/BEFUNDE_98.md`: #98 hatte nach 23 Review-Runden keine Null-Runde und wurde dennoch integriert. #60 gründet eine neue Familie, also ist mit vielen Runden zu rechnen.

## 1 Wirkungskette & Knoten-Bilanz (§2.1)

**Rolle (Rollen-Check, Schritt 2):** Sheet „Schadensbaum-Netzwerkliste“ Z61 (Id 60):
**Buchungsobjekt — Ebene B**, Feld Bauwesen, Handlungserfordernis **sehr dringend**,
Input-Kante **49 Hochwasser**, keine Output-Kante, Konto **K3 Gebäude & Sachwerte**, Baustein
**K3-Wiederherstellung**. Kein Abbruch nach R2/R3.

**W-Knoten (Entscheidungslog Nr. 1):** Die Arbeitsmappe führt keinen eigenen W-Knoten
„Flusshochwasser“. #60 liegt im Bauwesen-Container „Schäden an Gebäuden, Bauwerken und zugehörigen
Infrastrukturen“ = Sheet „Klimawirkungsketten“ Z272, Knoten **W117 „Schäden an Gebäuden und
Infrastrukturen“** (Konfidenz **mittel**: drei Container-Expansionen in der Wirkungs-Labelliste).
Der Hochwasser-Eingang ist dort **W085 „Hochwasser“** (Z208 = KWRA-Id 49). W085 ist ein vorgelagerter
W-Knoten; seine Eingänge sind eine Ebene tief mit aufgenommen (Konfidenz mittel, Sensitivitätspfeil
auf den Container). Der Code-Bestand (`backend/app/data/catalog.py`, Eintrag `kwra_id: 60`) trägt
genau die Namenslisten von W117 — der Umschnitt geht vom selben Knoten aus.

### Knoten-Bilanz

Spalte „rechnet in“ ist im Erstaufschlag durchgängig `offen`. Die Spalte „Vorschlag“ nennt nur, was
die Arbeitsmappen selbst hergeben (Blatt + Zeile); sie ist keine Entscheidung.

| Knoten | Name | Blatt/Zeile | rechnet in | Vorschlag laut Arbeitsmappe |
|---|---|---|---|---|
| W085 | Hochwasser (= Id 49) | KWK Z208; NW Z50 | offen | Hazard des Endpunkts (einzige Input-Kante, NW Z61); Id 49 selbst „Rein vorgelagert (0 €)“, R2 — Bewertung „HQ-Szenarien × Schadensfunktionen (Wassertiefe-Schaden) × Gebäudewerte“ (Mon. Z65) |
| E12 | Schneeschmelze (über W085) | KWK Z13 | offen | wirkt nur über W085 (Kein-Doppelkanal §3.2): Szenario-Verschiebung des Hazards, kein eigener Faktor |
| E07 | Nässe (über W085) | KWK Z8 | offen | wie E12 |
| E08 | Starkregen (direkt auf W117 und über W085) | KWK Z9 | offen | über W085 wie E12; direkter Gebäudeschaden durch Starkregen gehört zu #59 (Mon. Z64 „Sachschäden durch Starkregen/Rückstau“) — R9 |
| S072 | Boden-/Vegetationsbedeckung (über W085) | KWK Z197 | offen | wirkt auf Abflussbildung in W085; bewusst inaktiv, falls der Hazard-Datensatz den Abfluss schon enthält (Kein-Doppelkanal) |
| S073 | Flächenversiegelung (über W085) | KWK Z198 | offen | wie S072 |
| S074 | Topographie (Geländeform, Höhe) (über W085) | KWK Z199 | offen | Kandidat für die Zell-Exposition (Geländehöhe → Wassertiefe); Doppelkanal prüfen, falls HQ-Karten Wassertiefen bereits führen |
| R17 | Vorkommen von Oberflächengewässer und Grundwasser (über W085) | KWK Z204 | offen | Kandidat Exposition; Lackmustest §3.1: keine Flussaue → ~0 |
| R18 | Vorkommen von Abwasser- und Entwässerungssystemen (über W085) | KWK Z205 | offen | Rückstau gehört zu #59 (Mon. Z64), Kanalnetz zu #52 (K4) — voraussichtlich bewusst inaktiv |
| R19 | Vorkommen von Infrastruktur an Binnengewässern (über W085) | KWK Z206 | offen | Infrastruktur → K4 (K3-Definition, Konten Z28) — voraussichtlich bewusst inaktiv |
| E10 | Hagel | KWK Z11 | offen | keine Kante auf #60 (NW Z61 Input nur 49); Gegenstand Mon. Z65 „Sachschäden flussseitiger Überflutung“ — voraussichtlich bewusst inaktiv |
| E17 | Starkwind | KWK Z18 | offen | wie E10 |
| E14 | Schnee- und Eisdruck | KWK Z15 | offen | wie E10 |
| E02 | Hitze | KWK Z3 | offen | wie E10 |
| E03 | Kälte / Frost | KWK Z4 | offen | wie E10 |
| W074 | Meeresspiegelhöhe (= Id 40) | KWK Z181 | offen | seeseitig → #46 (Mon. Z65 „Nicht enthalten: Seeseitige Schäden (ID 46)“) — R9 |
| W077 | Sturmfluten (= Id 43) | KWK Z184 | offen | wie W074 |
| W087 | Sturzfluten (= Id 51) | KWK Z210 | offen | Gebäudeschäden über #59 (Mon. Z56: „Schäden laufen über Gebäude-Starkregen (K3)“) — R9 |
| W008 | Bergsturz, Felssturz, Steinschlag | KWK Z45 | offen | Massenbewegungen → #12 (NW Z13, K3) — R9 |
| W006 | Rutschungen und Muren (= Id 12) | KWK Z43 | offen | wie W008 |
| W091 | Grundwasserstand (= Id 55) | KWK Z214 | offen | Id 55 bucht direkt in K3 (Abgleich-Protokoll P5) — Partition gegenüber #60 offen (R9) |
| W100 | Einschränkungen Kanalnetze und Vorfluter (= Id 52) | KWK Z223 | offen | Id 52 bucht K4 (NW Z53) — voraussichtlich bewusst inaktiv |
| S092 | Bauliche, organisatorische und finanzielle Vorsorge der Eigentümer und Nutzer | KWK Z256 | offen | Kandidat **Maßnahmen-Hebel** (Objektschutz); P2-Abschätzung §5.1 |
| S093 | Zustand von Gebäuden und Infrastrukturen | KWK Z257 | offen | Kandidat Vulnerabilität der Schadensfunktion; Evidenz und Zellgröße offen |
| S094 | Verwendete Baumaterialien auf Gebäudeebene | KWK Z258 | offen | wie S093 |
| S096 | Bauliche, organisatorische und finanzielle Vorsorge der öffentlichen Hand | KWK Z260 | offen | Schutzsysteme über R7-Weiche mit #50 (Mon. Z65 „Schutzkosten (ID 50, R7)“; Z55) |
| S097 | Zustand von (Schutz-)Infrastrukturen | KWK Z261 | offen | wie S096 (Versagensfall, Erwartungswert R7) |
| S098 | Verwendete Baumaterialien von (Schutz-)Infrastrukturen | KWK Z262 | offen | wie S096 |
| S104 | Investitionen der Bau- und Immobilienwirtschaft in exponierten Gebieten | KWK Z268 | offen | Kandidat Szenario-Dynamik des Gebäudebestands (Kap. 6) |
| R24 | Vorkommen von Gebäuden | KWK Z270 | offen | **Mengengerüst** (Gebäudewerte, Mon. Z65) |
| R23 | Vorkommen von Bau- und Immobilienunternehmen | KWK Z269 | offen | laut W117-Anmerkung pauschal nach Regel 4 eingetragen; kein Bezug zu Gebäudeschäden — voraussichtlich bewusst inaktiv |
| R25 | Vorkommen von Siedlungsinfrastrukturen | KWK Z271 | offen | Infrastruktur → K4 (Konten Z28) — voraussichtlich bewusst inaktiv |

KWK = Sheet „Klimawirkungsketten“, NW = „Schadensbaum-Netzwerkliste“, Mon. = „Risiken-Monetarisierung“
(Blattzeile), Konten = „Schadenskonten-System“. Zusätzlich, kein Knoten der W117-Kette: W103
„Belastung oder Versagen von Hochwasserschutzsystemen“ (KWK Z226 = Id 50), nur als R7-Partner genannt.

### Weitergaben (zweispaltig; Quelle: Netzwerkliste + Abgleich-Protokoll)

| Output-Kanten (Netzwerkliste / Abgleich-Protokoll mit Punkt-Nr.) | Konto-Ausschlüsse / verwandte Buchungen (Konten-Definition, Monetarisierung) |
|---|---|
| **keine** — NW Z61 führt keine Output-IDs; das Abgleich-Protokoll hat keinen Punkt mit Quelle oder Ziel 60. Eingehend: **49 → 60** ist eine Originalkante (NW Z50, Mon. Z54 „→ 60, 74, 50, 101“), kein Abgleich-Punkt. | **K3 schließt aus** (Konten Z28): „Betriebsunterbrechung (→K5), Infrastruktur (→K4), Personen (→K1)“. **#60 schließt aus** (Mon. Z65): „Seeseitige Schäden (ID 46); Verkehrsinfrastruktur (ID 74); Schutzkosten (ID 50, R7)“. **Partitionsregel-Zitate, K3 geteilt:** #59 (Mon. Z64) „Nicht enthalten: Flusshochwasserschäden (ID 60)“; #46 (Mon. Z51) „Nicht enthalten: … flussseitige/Starkregenschäden (ID 59/60)“; R9 (Rechenregeln Z11): „Innerhalb eines Kontos zählt jede Einheit (… Gebäude) genau einmal“. **Ohne Partitionsregel in der Mappe (offen):** #92 touristische Infrastruktur (K3; Kante 49→92, P15), #102 Gesundheitsinfrastruktur (K3; 49→102, P16), Id 55 Direktbuchung K3 (P5). Personen-Folgen desselben Ereignisses: #101 (K1, andere Konten zulässig, Mon. Z106). |

### Konto-Einbettung

- **Konto:** K3 Gebäude und Sachwerte — Definition (Konten Z26): „Wiederherstellungskosten an
  Gebäuden, Hausrat, Fahrzeugen, Anlagen und Grundstücken (inkl. Landverlust), ereignisbezogen;
  Versicherungsleistungen sind Transfers.“ Kostensatz-Typ (Z27): „Wiederherstellungs-/Zeitwertkosten;
  Schadensfunktionen × Bestandswerte“.
- **Bewertungsbaustein:** K3-Wiederherstellung (NW Z61). Bewertungsansatz (Mon. Z65): „Wie ID 59,
  ereignisbezogen flussseitig; HQ-Szenarien × Schadensfunktionen (Wassertiefe-Schaden) ×
  Gebäudewerte.“ Gegenstand: „Sachschäden flussseitiger Überflutung.“
- **Rechenregeln:** R7, R9 (Mon. Z65, Spalte „Regeln“); dazu Annahme A5 Ereignislogik (Rechenregeln
  Z20): „Eintrittswahrscheinlichkeit × Schadensfunktion × Bestand; Schutzsysteme über die
  R7-Erwartungswert-Weiche“. R5 ist über „Wie ID 59“ inhaltlich einbezogen, steht aber nicht in der
  Regelspalte (offener Punkt 5).
- **Handlungserfordernis:** sehr dringend (Mon. Z65, NW Z61).
- **Nur K3 aktiv:** Folgen desselben Ereignisses in K1 (#101), K4 (#74), K5 und K8 (#50) sind nicht
  enthalten — Untergrenze, im Infokasten zu benennen (§3.6).

## 2 Evidenz-Register (§2.2)

Skelett mit einer Zeile je Knoten der Bilanz. Die Zeilen sind in `docs/evidenz/register.md`
gespiegelt. Wiederverwendbare Zeilen fanden sich dort nicht (Register führt bisher nur K1-Zeilen
aus #95/#96/#98). In Formeln (§3) dürfen später nur Zeilen mit Entscheidung **Basiswert** stehen.

| Register-ID | Knoten → Outcome | Effektgröße | Studientyp | Quelle | Übertragbarkeit | Datenlage je Zelle | Entscheidung |
|---|---|---|---|---|---|---|---|
| 60-W085-01 | W085 Hochwasser → Überflutungswahrscheinlichkeit/-tiefe am Gebäude | offen | offen | offen (Mon. Z65: HQ-Szenarien) | offen | offen — Datenebene nach §3.1 zu spezifizieren | offen |
| 60-E12-01 | E12 Schneeschmelze → W085 | offen | offen | offen | offen | offen | offen |
| 60-E07-01 | E07 Nässe → W085 | offen | offen | offen | offen | offen | offen |
| 60-E08-01 | E08 Starkregen → W085 / Gebäudeschaden | offen | offen | offen | offen | offen | offen |
| 60-S072-01 | S072 Boden-/Vegetationsbedeckung → Abfluss (W085) | offen | offen | offen | offen | offen | offen |
| 60-S073-01 | S073 Flächenversiegelung → Abfluss (W085) | offen | offen | offen | offen | offen | offen |
| 60-S074-01 | S074 Topographie → Wassertiefe am Gebäude | offen | offen | offen | offen | offen | offen |
| 60-R17-01 | R17 Oberflächengewässer → Exposition | offen | offen | offen | offen | offen | offen |
| 60-R18-01 | R18 Entwässerungssysteme → Gebäudeschaden (flussseitig) | offen | offen | offen | offen | offen | offen |
| 60-R19-01 | R19 Infrastruktur an Binnengewässern → Gebäudeschaden | offen | offen | offen | offen | offen | offen |
| 60-E10-01 | E10 Hagel → Gebäudeschaden (flussseitig) | offen | offen | offen | offen | offen | offen |
| 60-E17-01 | E17 Starkwind → Gebäudeschaden (flussseitig) | offen | offen | offen | offen | offen | offen |
| 60-E14-01 | E14 Schnee- und Eisdruck → Gebäudeschaden (flussseitig) | offen | offen | offen | offen | offen | offen |
| 60-E02-01 | E02 Hitze → Gebäudeschaden (flussseitig) | offen | offen | offen | offen | offen | offen |
| 60-E03-01 | E03 Kälte / Frost → Gebäudeschaden (flussseitig) | offen | offen | offen | offen | offen | offen |
| 60-W074-01 | W074 Meeresspiegelhöhe → Gebäudeschaden (flussseitig) | offen | offen | offen | offen | offen | offen |
| 60-W077-01 | W077 Sturmfluten → Gebäudeschaden (flussseitig) | offen | offen | offen | offen | offen | offen |
| 60-W087-01 | W087 Sturzfluten → Gebäudeschaden (flussseitig) | offen | offen | offen | offen | offen | offen |
| 60-W008-01 | W008 Bergsturz, Felssturz, Steinschlag → Gebäudeschaden (flussseitig) | offen | offen | offen | offen | offen | offen |
| 60-W006-01 | W006 Rutschungen und Muren → Gebäudeschaden (flussseitig) | offen | offen | offen | offen | offen | offen |
| 60-W091-01 | W091 Grundwasserstand → Gebäudeschaden (flussseitig) | offen | offen | offen | offen | offen | offen |
| 60-W100-01 | W100 Kanalnetze/Vorfluter → Gebäudeschaden (flussseitig) | offen | offen | offen | offen | offen | offen |
| 60-S092-01 | S092 Vorsorge der Eigentümer (Objektschutz) → Gebäudeschaden | im Erstaufschlag **keine nach §3.5 zulässige** (Interventions-/quasi-experimentelle) Effektgröße belegt ⇒ **Abschätzung von KAP3** \(r_{\text{S092}}\) = 0,035 (Band 0,0075–0,112), Kette §5.1 | — (keine Interventionsstudie belegt; Befragungen nach Ereignissen sind nur Kandidat, im Volltext nicht verifiziert, gehen nicht in den Wert ein) | Herleitung §5.1 (`#s092-wirkung`) | §3.9 ABGESCHÄTZT; Setzung für deutsche Kommunen | kommunal (Pauschalfaktor — Modellgrenze der Abschätzung) | offen (Vorschlag: Maßnahmen-Hebel, abgeschätzt) |
| 60-S093-01 | S093 Gebäudezustand → Schadensgrad | offen | offen | offen | offen | offen | offen |
| 60-S094-01 | S094 Baumaterialien → Schadensgrad | offen | offen | offen | offen | offen | offen |
| 60-S096-01 | S096 Vorsorge der öffentlichen Hand → Überflutungswahrscheinlichkeit | offen | offen | offen | offen | offen | offen (Vorschlag: R7-Weiche mit #50) |
| 60-S097-01 | S097 Zustand Schutzinfrastruktur → Versagenswahrscheinlichkeit | offen | offen | offen | offen | offen | offen (Vorschlag: R7-Weiche mit #50) |
| 60-S098-01 | S098 Baumaterialien Schutzinfrastruktur → Versagenswahrscheinlichkeit | offen | offen | offen | offen | offen | offen (Vorschlag: R7-Weiche mit #50) |
| 60-S104-01 | S104 Investitionen in exponierten Gebieten → Bestandsentwicklung | offen | offen | offen | offen | offen | offen |
| 60-R24-01 | R24 Gebäude → Mengengerüst (Gebäudewerte) | offen | offen | offen (Mon. Z65: Gebäudewerte) | offen | offen — Datenebene nach §3.1 zu spezifizieren | offen |
| 60-R23-01 | R23 Bau- und Immobilienunternehmen → Gebäudeschaden | offen | offen | offen | offen | offen | offen |
| 60-R25-01 | R25 Siedlungsinfrastrukturen → Gebäudeschaden | offen | offen | offen | offen | offen | offen |

## 3 Modell (§2.3)

<!--
Pflichtinhalte (§2.3/§3.1/§3.2/§3.6):
- Native Ergebnisgröße deklarieren (genau eine je Risiko-Code; weitere als Teil-Ausweise).
  Kandidat laut A5/Mon. Z65: Erwartungsschaden K3 je Jahr über HQ-Szenarien — Entscheidung offen.
- Schicht-B-Formel Menge × Rate × Preis auf Zellebene, nur aus Register-Zeilen „Basiswert“ und
  hergeleiteten Parametern; physische Zwischengröße vor dem Euro (z. B. betroffene Gebäude,
  Wassertiefe, Schadensgrad); Aggregation Zelle → Kommune.
- Je Formel alphabetische Zeichentabelle (Zeichen · Name · Einheit · Wert/Herkunft mit Register-ID
  oder Herleitungs-Anker); Mini-Rechenbeispiele als Golden-Test-Blöcke.
- Lackmustest §3.1: Kommune ohne Flussaue/Überflutungsfläche → ~0.
- Schicht-A-Index aus denselben Knoten, nie auf Euro-Pfaden.

(a) DATENEBENEN-ANLAGEPFLICHT (§3.1): Jede benötigte Zellgröße, die das Produkt nicht führt
    (voraussichtlich HQ-Überflutungsflächen/Wassertiefen und Gebäudebestandswerte), wird als Ebene
    vollständig spezifiziert — Quelle, Beschaffungsweg keyless, Zell-Ableitungsregel, Fallback,
    Normierung/Zentrierung — und „neu anzulegen“ gekennzeichnet. Ohne offene Quelle: „geparkt
    (Datenquelle fehlt)“ mit Beschaffungs-Watchlist. Kein dauerhafter, unspezifizierter
    Neutral-Fallback.
(c) GESCHLOSSENE BETRACHTUNGSEBENE (§3.2): Zentrierungs-/Referenzmittel entweder amtlich publiziert
    oder aus der Betrachtungsebene selbst (Kommune: eigene Zellen, im Baseline-Lauf festgehalten) —
    nie aus einer Aggregation über eine höhere Ebene; ohne zulässige Referenz bleibt der
    Modifikator neutral.

Parameter-Block-Beispiel (Format §4; Werte erst nach Herleitung eintragen):
  parameter:
    id: flood_bldg.<name>
    wert: <Herleitungswert>
    einheit: "<Einheit>"
    band: [<unten>, <oben>]
    herkunft: register:60-<Knoten>-01      # oder herleitung:#<anker>
    quelle: <quellen-id>
    preisstand: <Jahr>                     # Pflichtfeld bei Kostensätzen
    bandzuordnung: [<Gebäudetyp/Band>]
    endpunkt: <K3-Wiederherstellung>

Beispiel-Test-Block (Format §4; im echten Block mit Code-Zaun „python test: beispiel_60_<name>“):
  assert abs(<rechnung> - <erwartet>) < 1e-9
-->

## 4 Kalibrierung & Validierung (§2.4/§3.4)

<!--
Pflichtinhalte: nationaler Anker als EIN Niveau-Skalar (Anker-Zeitreihe mit Revisionsstand;
vorläufige Jahre gesondert); Kalibriermodell = Produktionsmodell; unabhängige Verteilungsprüfung
auf der kritischsten Achse — bei Flut das EREIGNISREGIME — mit vorab fixierter Toleranz,
out-of-sample; Sanity-Bänder mit Unter- und Obergrenze aus amtlicher Statistik; Skripte/CSVs als
Anlage verlinkt. Anker-Kandidaten und Zahlen: offen (keine Zahl ohne Quelle, P1).

(b) RESSOURCEN-REGEL (§3.4): Kalibrierung, Validierung und Abgleiche nie über nationale
    100-m-Vollraster-Läufe planen — zulässig sind Bundesland-, Gemeinde-/Gemeindepunkt- und
    kommunale Stichproben-Ebene (dokumentierte Anker-Kommunen mit dem Produktionsmodell).
-->

## 5 Maßnahmen-Hebel (§2.5/§3.5)

<!--
Pflichtinhalte: Hebel nur an Ketten-Sensitivitäten; Effektgrößen aus Interventions-/
quasi-experimenteller Evidenz; marginal gegenüber heute; Doppelzählungs-Wächter gegen die
Kalibrierjahre; Wirkungsort definieren; R7-Weiche referenzieren (Schutzsysteme #50; Objektschutz
als K8-Maßnahmenkosten). Hebel ohne Effektgröße: Abschätzung nach P2 (nie Wirkung null).
Offene Hebel-Kandidaten: S096/S097/S098 (über R7-Erwartungswert mit #50), S093/S094.
-->

### 5.1 Wirkungsabschätzung S092 Objektschutz der Eigentümer (Anker `#s092-wirkung`) — §3.9 **ABGESCHÄTZT**

**Anlass (Vorgabe P2, §3.5).** Für den Hebel „bauliche Vorsorge der Eigentümer“ (S092) ist im
Erstaufschlag keine Interventions- oder quasi-experimentelle Effektgröße belegt. Befragungen
Betroffener nach Hochwasserereignissen vergleichen vorsorgende und nicht vorsorgende Haushalte im
Querschnitt. Das ist nach §3.5 keine Maßnahmen-Effektgröße (Selbstselektion); zudem sind diese
Studien hier nicht im Volltext verifiziert. Der Hebel wird deshalb **nicht mit Wirkung null**
geführt, sondern mit der folgenden **Abschätzung von KAP3**. Im Produkt ist sie als solche samt
dieser Herleitung auszuweisen (P1).

**Wirkungsort.** Multiplikativ auf den K3-Erwartungsschaden von #60 der Kommune:
\(\text{EAD}_{\text{mit}} = \text{EAD} \cdot (1 - r_{\text{S092}})\). Nur K3; die Kosten des
Objektschutzes sind K8-Maßnahmenkosten und schließen den verhinderten Schaden je Gebäude aus (R7).

**Kette.** \(r_{\text{S092}} = \Delta q \cdot s_{\text{bem}} \cdot e_{\text{bem}}\)

| Zeichen | Name | Einheit | Wert (Band) | Herleitung — alle drei Werte sind Abschätzungen von KAP3, keine Primärquelle |
|---|---|---|---|---|
| \(\Delta q\) | zusätzlich nachgerüsteter Anteil exponierter Gebäude (marginal gegenüber heute) | – | 0,10 (0,05–0,20) | Annahme: Ein kommunales Förder- und Beratungsprogramm erreicht in einem Planungszeitraum jedes zehnte exponierte Gebäude. Untere Bandgrenze: halbe Reichweite. Obere: doppelte. Marginal, weil vorhandener Objektschutz bereits im Basisschaden steckt (Doppelzählungs-Wächter). |
| \(e_{\text{bem}}\) | Schadensminderung am nachgerüsteten Gebäude, solange der Wasserstand das Bemessungsniveau nicht übersteigt | – | 0,70 (0,50–0,80) | Annahme: Objektschutz (Abdichtung, Rückstausicherung, angepasste Nutzung) hält Wasser bis zur Schutzhöhe weitgehend fern. Restschaden durch Feuchte, Ausführungsmängel und nicht verschlossene Öffnungen. Obergrenze unter 1, weil kein Objektschutz vollständig dicht ist. |
| \(s_{\text{bem}}\) | Anteil der Schadenssumme aus Ereignissen unterhalb des Bemessungsniveaus | – | 0,50 (0,30–0,70) | Annahme: Schadenssummen verteilen sich auf häufige flache und seltene tiefe Überflutungen. Oberhalb der Schutzhöhe wird Objektschutz überströmt und wirkt praktisch nicht. Ohne gemessene Tiefenverteilung wird die Mitte gesetzt, Band symmetrisch. |

Rechnung: \(r_{\text{S092}}\) = 0,10 · 0,50 · 0,70 = **0,035**. Band (alle Enden gleichgerichtet):
0,05 · 0,30 · 0,50 = **0,0075** bis 0,20 · 0,70 · 0,80 = **0,112**.

**Ergebnis-Sensitivität.** Der ausgewiesene Maßnahmeneffekt ist −3,5 % des K3-Erwartungsschadens
von #60 (Band −0,75 % bis −11,2 %). Die Kette ist linear, jeder Faktor hat Elastizität 1. Einzeln
variiert: \(\Delta q\) 0,05–0,20 ⇒ r 0,0175–0,070 (größte Achse); \(s_{\text{bem}}\) 0,30–0,70 ⇒ r
0,021–0,049; \(e_{\text{bem}}\) 0,50–0,80 ⇒ r 0,025–0,040.

**Modellgrenzen der Abschätzung.** (1) Kommunenweiter Pauschalfaktor statt zellscharfer Wirkung
(Bauform-Grenze). (2) \(s_{\text{bem}}\) ist messbar, sobald Wassertiefen je HQ-Szenario als Ebene
vorliegen (§3.1). Dann wird er gemessen statt gesetzt (Ersetzungspfad, W1). (3) Ersetzt wird die
ganze Abschätzung, sobald eine Interventions- oder quasi-experimentelle Effektgröße gefunden ist
(§3.8-Recherche offen).

```python test: beispiel_60_s092_abschaetzung
dq, s_bem, e_bem = 0.10, 0.50, 0.70
r = dq * s_bem * e_bem
assert abs(r - 0.035) < 1e-12
lo, hi = 0.05 * 0.30 * 0.50, 0.20 * 0.70 * 0.80
assert abs(lo - 0.0075) < 1e-12 and abs(hi - 0.112) < 1e-12
assert abs(0.05 * s_bem * e_bem - 0.0175) < 1e-12 and abs(0.20 * s_bem * e_bem - 0.070) < 1e-12
```

## 6 Szenario-Anwendung & Modellgrenzen (§3.2/§3.6)

<!--
Pflichtinhalte: je empfohlenem Ansatz ein Absatz „Szenario-Anwendung“ (verschobene Größe — z. B.
HQ-Jährlichkeiten über E12/E07/E08 in W085 —, konstante Größen, Stationaritätsannahmen,
Bestandsdynamik S104); Modellgrenzen nummeriert; Infokasten-Texte: Benennung „bewerteter Schaden
— Konto K3“ (nie „Gesamtschaden“), Vollständigkeitsanzeige, Versionsstempel „Untergrenze“;
Hinweis, dass K1 (#101), K4 (#74), K5 und K8 (#50) desselben Ereignisses nicht enthalten sind;
Ausweis als Raten (je 1.000 EW / je ha) plus aggregierte Ebene.
-->

## 7 Parameter-Blöcke (maschinenlesbar, §4)

Nur der Hebel aus §5.1 ist beziffert. Alle weiteren Blöcke entstehen mit der Herleitung in Kap. 3/4.

```yaml
parameter:
  id: flood_bldg.dq_s092
  wert: 0.10
  einheit: "-"
  band: [0.05, 0.20]
  herkunft: herleitung:#s092-wirkung     # Abschätzung von KAP3 (P1/P2)
  quelle: null
  preisstand: null
  bandzuordnung: [alle]
  endpunkt: K3-Wiederherstellung
---
parameter:
  id: flood_bldg.s_bem
  wert: 0.50
  einheit: "-"
  band: [0.30, 0.70]
  herkunft: herleitung:#s092-wirkung     # Abschätzung von KAP3 (P1/P2)
  quelle: null
  preisstand: null
  bandzuordnung: [alle]
  endpunkt: K3-Wiederherstellung
---
parameter:
  id: flood_bldg.e_bem
  wert: 0.70
  einheit: "-"
  band: [0.50, 0.80]
  herkunft: herleitung:#s092-wirkung     # Abschätzung von KAP3 (P1/P2)
  quelle: null
  preisstand: null
  bandzuordnung: [alle]
  endpunkt: K3-Wiederherstellung
---
parameter:
  id: flood_bldg.r_s092
  wert: 0.035
  einheit: "-"
  band: [0.0075, 0.112]
  herkunft: herleitung:#s092-wirkung     # abgeleitet: dq_s092 · s_bem · e_bem
  quelle: null
  preisstand: null
  bandzuordnung: [alle]
  endpunkt: K3-Wiederherstellung
```

## 8 Quellen (§3.8)

1. KWRA-Schadensbaum × UBA-Klimawirkungsketten, Arbeitsmappe
   `docs/Schadensbaum/KWRA-Schadensbaum_X_UBA-klimawirkungsketten.xlsx` — Sheets
   „Klimawirkungsketten“ (Z3–Z271 wie in Kap. 1 zitiert) und „Schadensbaum-Netzwerkliste“ (Z13, Z50,
   Z51, Z53, Z60, Z61).
2. KWRA-Monetarisierung, Arbeitsmappe `docs/Schadensbaum/KWRA-Monetarisierung.xlsx` — Sheets
   „Risiken-Monetarisierung“ (Z51, Z54–Z56, Z64, Z65, Z106), „Schadenskonten-System“ (Z26–Z30),
   „Rechenregeln“ (Z9, Z11, Z20), „Abgleich-Protokoll“ (P5, P15, P16).
3. Evidenz-Quellen: offen. Für S092 ist keine Primärquelle verwendet (§5.1 ABGESCHÄTZT). Der
   Code-Bestand zitiert für Objektschutz die „Hochwasserschutzfibel“ des BMWSB (2022;
   `backend/app/data/sources.py`, `BBK_Hochwasserschutzfibel`). Sie ist hier nicht im Volltext
   geprüft und geht in keinen Wert ein.

<!-- Format je Quelle: Autor, Jahr, Titel, Organ, DOI/URL, Zugriffsdatum, Archiv-Snapshot;
Sekundärfunde vor Übernahme im Volltext verifizieren; Widersprüche benennen. -->

## 9 Ansatz-Vergleich (§3.7 — erster Vertreter der Familie K3/K4-Ereignisschäden)

<!--
Pflicht nach §2.6, weil kein abgenommener Familien-Prototyp existiert (docs/methodik/ führt nur
K1-Berichte #95/#96/#98). Mindestens drei Ansätze a–c, festes Kriterienraster: kausale Treue ·
Kalibrierbarkeit · lokale Differenzierung · Datenverfügbarkeit · Maßnahmen-Anschluss ·
Architektur-Konformität · Aufwand; Empfehlung begründet; Verworfenes ggf. als Ergänzungsmodul.
Aus der Arbeitsmappe vorgegebener Kandidat (a): Erwartungswert über HQ-Szenarien —
Eintrittswahrscheinlichkeit × Wassertiefe-Schadensfunktion × Gebäudewert (A5, Mon. Z65).
Weitere Kandidaten (b), (c): offen. Negativ-Beispiel (§2.6/§3.1): Verteilschlüssel
„nationaler Schadenstopf × Anteil“ — ausgeschieden.
-->

| Kriterium | (a) HQ-Szenarien × Schadensfunktion × Bestand | (b) offen | (c) offen |
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
| 1 | Welcher W-Knoten trägt #60? | W117 (KWK Z272), mit W085 eine Ebene tief | einziger Bauwesen-Knoten für Gebäudeschäden mit Hochwasser-Eingang; NW Z61 Input 49 = W085; Code-Bestand nutzt dieselben Namenslisten | nur W085 als Kette (dann fehlten S092–S104 und R24, also Vulnerabilität und Mengengerüst) | 32 Knoten in Bilanz und Register |
| 2 | Familie? | neue Familie K3/K4-Ereignisschäden, Kap. 9 angelegt | kein K3-Bericht in `docs/methodik/` | Übernahme der K1-Struktur (#95) — passt nicht zu Ereignislogik A5 | Drei-Ansätze-Vergleich Pflicht |
| 3 | S092 ohne zulässige Effektgröße | P2-Abschätzung r = 0,035 (0,0075–0,112) | Vorgabe P2, §3.5; Querschnittsbefragungen sind keine Maßnahmen-Effektgröße | Wirkung null (unzulässig nach P2) | Maßnahmen-Modul, kein Basiswert |
| 4 | Slug | `gebaeudeschaeden_flusshochwasser` | kurz, eindeutig gegen #59 (Starkregen) und #46 (Küste) | `flusshochwasser` (verwechselbar mit Id 49) | Dateinamen Bericht/Ledger |
