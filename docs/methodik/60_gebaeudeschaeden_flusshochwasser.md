# Methodik-Bericht #60 — Schäden an Gebäuden aufgrund von Flusshochwasser

Status: **Erstaufschlag (`/neu-risiko 60`) — noch nicht gegengeprüft** · 11.09.2026 ·
Instruktionsquelle: `docs/AUFGABE_METHODIK_SCHADENSRECHNUNG.md` (v2) · Umsetzungsgrundlage:
**Ansatz (a) — Szenario-Erwartungswert mit typisierter Tiefen-Schadensfunktion je 100-m-Zelle**
(entschieden im Ansatz-Vergleich Kap. 9; Entscheidungslog Nr. 5) · Familie: **K3/K4-Ereignisschäden — noch kein Prototyp, dieser Bericht ist
der erste Vertreter** (§2.6; Entscheidungslog Nr. 2)

> **Geltungsbereich.** Befüllt sind Kap. 1 (Wirkungskette, Knoten-Bilanz, Weitergaben, Konto) und
> Kap. 2 (Evidenz-Register) aus den beiden Arbeitsmappen unter `docs/Schadensbaum/` und aus
> volltextgeprüfter externer Evidenz (Langbelege B1–B6 unter der Registertabelle); befüllt ist
> zudem Kap. 9 (Ansatz-Vergleich, entschieden mit T-0237) sowie Kap. 3 bis einschließlich der
> Kernformel (native Ergebnisgröße, Datenebenen nach §3.1, Tiefen-Schadensfunktion, Schicht-B-Formel
> auf Zellebene; T-0238). Kap. 4–8 tragen
> die Pflichtinhalte als Kommentar. Die Knoten-Bilanz in Kap. 1 ist entschieden (32/32 Zeilen
> tragen eine Formelstelle oder `inaktiv` mit Zitat). Im Evidenz-Register sind **sieben** der
> 32 Zeilen belegt beziehungsweise entschieden: **60-W085-01** (Basiswert, Hazard),
> **60-R24-01** (Basiswert, Mengengerüst), **60-S074-01** und **60-R17-01**
> (Sensitivitätsbänder der Exposition), **60-S093-01** und **60-S094-01** (Sensitivitätsbänder
> des Schadensgrads, abgeschätzt) sowie **60-S092-01** (Maßnahmen-Hebel, abgeschätzt; Herleitung
> §5.1, `#s092-wirkung`). Die **übrigen 25 Registerzeilen stehen auf `offen`**. Entschieden sind
> der Ansatz (Kap. 9, Ansatz (a)), die native Ergebnisgröße (Kap. 3.1) und die vier Datenebenen
> nach §3.1 (Kap. 3.2). Jeder als
> **Abschätzung von KAP3** geführte Wert ist in seiner Registerzeile als solcher gekennzeichnet
> (§3.9; Vorgaben P1/P2), samt Bandbreite, Sensitivität und Modellgrenze.
> Befund-Ledger: `reviews/BEFUNDE_60.md`.

## Ergebnis

- **Slug:** `60_gebaeudeschaeden_flusshochwasser`. **Registerzeilen:** 32 (`60-<Knoten>-01`), gespiegelt in `docs/evidenz/register.md`. Davon **7 belegt bzw. entschieden** — 60-W085-01, 60-R24-01, 60-S074-01, 60-R17-01, 60-S093-01, 60-S094-01 und 60-S092-01 (Maßnahmen-Hebel, abgeschätzt) —, die **übrigen 25 stehen auf `offen`**.
- **Entschieden (T-0237):** Ansatz-Vergleich Kap. 9 — Umsetzungsgrundlage ist Ansatz **(a)** (Szenario-Erwartungswert mit typisierter Tiefen-Schadensfunktion je 100-m-Zelle); (b) aggregierte Flächenschadensrate bleibt als Ergänzungsmodul, (c) Schadensgradmodell am Einzelgebäude ist ausgeschieden.
- **Entschieden (T-0238):** Kap. 3 bis zur Kernformel — native Ergebnisgröße (EAD in €₂₀₂₆/a, Ebene Kommune), vier Datenebenen nach §3.1 (drei „neu anzulegen", eine „geparkt"), Tiefen-Schadensfunktion und Schicht-B-Kernformel Menge × Rate × Preis je 100-m-Zelle.
- **Offen:** (1) Zeichentabelle, Aggregation Zelle → Kommune und Schicht A in Kap. 3; (2) Kap. 4, 6, 8; (3) R9-Partitionen zum verbliebenen Rest #92/#102/Id 55 (W091) — #37 und #12 sind entschieden, vgl. Kap. 1 Weitergaben; (4) die 25 noch nicht belegten Registerzeilen aus Kap. 2.
- **Aufwand Erstaufschlag:** 2 Nacharbeitsrunden (R1: Planungszahl korrigiert, Beispiel-Code-Zaun im Kommentar entfernt; R2: Lint-Funde behoben, Zeichentabelle S092 als eigener Abschnitt, Verweis korrigiert). Erstaufschlag: eine Session, 26 Werkzeugaufrufe, rund 3,2 USD. Nacharbeit: je rund 0,3 USD. Die Evidenz der sieben belegten Registerzeilen ist in eigenen Runden recherchiert und im Volltext geprüft (Quellen und Langbelege B1–B6 in Kap. 2).
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

**Entscheidungsstand (T-0235).** Spalte „rechnet in” trägt ab dieser Fassung je Zeile entweder eine
der sieben benannten **Formelstellen**, an die Kapitel 3 die Größe künftig bindet, oder den Wert
`inaktiv` mit einem wörtlichen Zitat aus `KWRA-Monetarisierung.xlsx` (Blatt und Zelle). Die
Formelstellen sind **Namen, keine Formeln**: Kapitel 3 selbst bleibt unverändert im
Kommentar-Zustand des Erstaufschlags und wird in einem eigenen Ticket nachgezogen — diese
Zeile ist die Vorbedingung dafür, nicht der Formelbau selbst. Benannte Formelstellen: **FS-Hazard**
(Eintrittswahrscheinlichkeit p(HQ) inkl. der Kein-Doppelkanal-Zuflüsse), **FS-Exposition**
(Wassertiefe am Gebäude), **FS-Schadensgrad** (Wassertiefe-Schadensfunktion nach Bauart/Zustand),
**FS-Mengengerüst** (Gebäudewerte/Bestand), **FS-Schutzsystem** (R7-Erwartungswert-Weiche mit #50),
**FS-Bestandsdynamik** (Kap. 6, Szenario-Dynamik des Bestands) und **FS-Vorsorge** (Maßnahmen-Hebel
S092, bereits in §5.1 beziffert). Die Spalte „Vorschlag” bleibt unverändert als Beleg aus der
Arbeitsmappe stehen; sie ist weiterhin keine eigene Entscheidung.

| Knoten | Name | Blatt/Zeile | rechnet in | Vorschlag laut Arbeitsmappe |
|---|---|---|---|---|
| W085 | Hochwasser (= Id 49) | KWK Z208; NW Z50 | **FS-Hazard** — Hazard-Term p(HQ); alleiniger Input der Bilanz (NW Z61) | Hazard des Endpunkts (einzige Input-Kante, NW Z61); Id 49 selbst „Rein vorgelagert (0 €)”, R2 — Bewertung „HQ-Szenarien × Schadensfunktionen (Wassertiefe-Schaden) × Gebäudewerte” (Mon. Z65) |
| E12 | Schneeschmelze (über W085) | KWK Z13 | **FS-Hazard** (enthalten, kein eigener Faktor — Kein-Doppelkanal §3.2) | wirkt nur über W085 (Kein-Doppelkanal §3.2): Szenario-Verschiebung des Hazards, kein eigener Faktor |
| E07 | Nässe (über W085) | KWK Z8 | **FS-Hazard** (enthalten, kein eigener Faktor — Kein-Doppelkanal §3.2) | wie E12 |
| E08 | Starkregen (direkt auf W117 und über W085) | KWK Z9 | **FS-Hazard** (Anteil über W085, kein eigener Faktor); direkter Kanal **inaktiv** — R9 (Rechenregeln Z11): „Innerhalb eines Kontos zählt jede Einheit (…Gebäude) genau einmal; verschiedene Konten desselben Ereignisses sind additiv.” i. V. m. Mon. Z64 (Nicht enthalten): „Flusshochwasserschäden (ID 60)” (#59 bucht den direkten Starkregen-Gebäudeschaden) | über W085 wie E12; direkter Gebäudeschaden durch Starkregen gehört zu #59 (Mon. Z64 „Sachschäden durch Starkregen/Rückstau”) — R9 |
| S072 | Boden-/Vegetationsbedeckung (über W085) | KWK Z197 | **FS-Hazard** (enthalten im Hazard-Datensatz, kein eigener Faktor — Kein-Doppelkanal §3.2) | wirkt auf Abflussbildung in W085; bewusst inaktiv, falls der Hazard-Datensatz den Abfluss schon enthält (Kein-Doppelkanal) |
| S073 | Flächenversiegelung (über W085) | KWK Z198 | **FS-Hazard** (enthalten im Hazard-Datensatz, kein eigener Faktor — Kein-Doppelkanal §3.2) | wie S072 |
| S074 | Topographie (Geländeform, Höhe) (über W085) | KWK Z199 | **FS-Exposition** — Geländehöhe → Wassertiefe am Gebäude | Kandidat für die Zell-Exposition (Geländehöhe → Wassertiefe); Doppelkanal prüfen, falls HQ-Karten Wassertiefen bereits führen |
| R17 | Vorkommen von Oberflächengewässer und Grundwasser (über W085) | KWK Z204 | **FS-Exposition** — Lackmustest §3.1: keine Flussaue → ~0 | Kandidat Exposition; Lackmustest §3.1: keine Flussaue → ~0 |
| R18 | Vorkommen von Abwasser- und Entwässerungssystemen (über W085) | KWK Z205 | **inaktiv** — Schadenskonten-System Z28 (Spalte „Ausgeschlossen”): „Betriebsunterbrechung (→K5), Infrastruktur (→K4), Personen (→K1)”; Mon. Z57 (Id 52, Spalte „Nicht enthalten”): „Gebäudeschäden durch Rückstau (ID 59).” | Rückstau gehört zu #59 (Mon. Z64), Kanalnetz zu #52 (K4) — voraussichtlich bewusst inaktiv |
| R19 | Vorkommen von Infrastruktur an Binnengewässern (über W085) | KWK Z206 | **inaktiv** — Schadenskonten-System Z28 (Spalte „Ausgeschlossen”): „Betriebsunterbrechung (→K5), Infrastruktur (→K4), Personen (→K1)” | Infrastruktur → K4 (K3-Definition, Konten Z28) — voraussichtlich bewusst inaktiv |
| E10 | Hagel | KWK Z11 | **inaktiv** — keine Kante auf #60 (NW Z61 Input nur 49); Mon. Z65 (Spalte „Wird hier bepreist (enthalten)”): „Sachschäden flussseitiger Überflutung.” | keine Kante auf #60 (NW Z61 Input nur 49); Gegenstand Mon. Z65 „Sachschäden flussseitiger Überflutung” — voraussichtlich bewusst inaktiv |
| E17 | Starkwind | KWK Z18 | **inaktiv** — wie E10; Mon. Z65: „Sachschäden flussseitiger Überflutung.” | wie E10 |
| E14 | Schnee- und Eisdruck | KWK Z15 | **inaktiv** — wie E10; Mon. Z65: „Sachschäden flussseitiger Überflutung.” | wie E10 |
| E02 | Hitze | KWK Z3 | **inaktiv** — wie E10; Mon. Z65: „Sachschäden flussseitiger Überflutung.” | wie E10 |
| E03 | Kälte / Frost | KWK Z4 | **inaktiv** — wie E10; Mon. Z65: „Sachschäden flussseitiger Überflutung.” | wie E10 |
| W074 | Meeresspiegelhöhe (= Id 40) | KWK Z181 | **inaktiv** — Mon. Z65 (Spalte „Nicht enthalten”): „Seeseitige Schäden (ID 46); Verkehrsinfrastruktur (ID 74); Schutzkosten (ID 50, R7).” | seeseitig → #46 (Mon. Z65 „Nicht enthalten: Seeseitige Schäden (ID 46)”) — R9 |
| W077 | Sturmfluten (= Id 43) | KWK Z184 | **inaktiv** — wie W074; Mon. Z65 (Spalte „Nicht enthalten”): „Seeseitige Schäden (ID 46); Verkehrsinfrastruktur (ID 74); Schutzkosten (ID 50, R7).” | wie W074 |
| W087 | Sturzfluten (= Id 51) | KWK Z210 | **inaktiv** — Mon. Z56 (Spalte „Wird hier bepreist (enthalten)”): „Schäden laufen über Gebäude-Starkregen (K3), Verkehr (K4), Personen (K1); Räumung/Instandsetzung der Entwässerung über ID 52 (K4).” | Gebäudeschäden über #59 (Mon. Z56: „Schäden laufen über Gebäude-Starkregen (K3)”) — R9 |
| W008 | Bergsturz, Felssturz, Steinschlag | KWK Z45 | **inaktiv** — R9 (Rechenregeln Z11): „Innerhalb eines Kontos zählt jede Einheit (…Gebäude) genau einmal”; Schadenskonten-System Z29 führt „12 Rutschungen und Muren” als eigenständiges K3-Buchungsobjekt | Massenbewegungen → #12 (NW Z13, K3) — R9 |
| W006 | Rutschungen und Muren (= Id 12) | KWK Z43 | **inaktiv** — wie W008; zusätzlich Mon. Z17 (Id 12, Spalte „Regeln”): „R7, R9” und Spalte „Bewertungsansatz”: „Wiederherstellungskosten beschädigter Gebäude (K3) …” (eigener Bewertungsansatz von #12, nicht #60) | wie W008 |
| W091 | Grundwasserstand (= Id 55) | KWK Z214 | **inaktiv** — Abgleich-Protokoll Punkt 5 (Zeile 10): Ziel-Name/Konto „Direktbuchung Konto K3” — Id 55 bucht eigenständig direkt in K3, außerhalb der #60-Formel (R9, Rechenregeln Z11) | Id 55 bucht direkt in K3 (Abgleich-Protokoll P5) — Partition gegenüber #60 offen (R9) |
| W100 | Einschränkungen Kanalnetze und Vorfluter (= Id 52) | KWK Z223 | **inaktiv** — Mon. Z57 (Id 52, Spalte „Schadenskonto”): „K4”; Spalte „Nicht enthalten”: „Gebäudeschäden durch Rückstau (ID 59).” | Id 52 bucht K4 (NW Z53) — voraussichtlich bewusst inaktiv |
| S092 | Bauliche, organisatorische und finanzielle Vorsorge der Eigentümer und Nutzer | KWK Z256 | **FS-Vorsorge** — Maßnahmen-Hebel, bereits beziffert (§5.1: r_S092 = 0,035, Band 0,0075–0,112, §3.9 Abgeschätzt) | Kandidat **Maßnahmen-Hebel** (Objektschutz); P2-Abschätzung §5.1 |
| S093 | Zustand von Gebäuden und Infrastrukturen | KWK Z257 | **FS-Schadensgrad** — Vulnerabilität der Wassertiefe-Schadensfunktion (Mon. Z65) | Kandidat Vulnerabilität der Schadensfunktion; Evidenz und Zellgröße offen |
| S094 | Verwendete Baumaterialien auf Gebäudeebene | KWK Z258 | **FS-Schadensgrad** — wie S093 | wie S093 |
| S096 | Bauliche, organisatorische und finanzielle Vorsorge der öffentlichen Hand | KWK Z260 | **FS-Schutzsystem** — R7-Erwartungswert-Weiche mit #50 (Mon. Z65 Spalte „Regeln”: „R7, R9”; Rechenregeln Z9 R7) | Schutzsysteme über R7-Weiche mit #50 (Mon. Z65 „Schutzkosten (ID 50, R7)”; Z55) |
| S097 | Zustand von (Schutz-)Infrastrukturen | KWK Z261 | **FS-Schutzsystem** — wie S096 (Versagensfall, Erwartungswert R7) | wie S096 (Versagensfall, Erwartungswert R7) |
| S098 | Verwendete Baumaterialien von (Schutz-)Infrastrukturen | KWK Z262 | **FS-Schutzsystem** — wie S096 | wie S096 |
| S104 | Investitionen der Bau- und Immobilienwirtschaft in exponierten Gebieten | KWK Z268 | **FS-Bestandsdynamik** — Szenario-Dynamik des Gebäudebestands (Kap. 6) | Kandidat Szenario-Dynamik des Gebäudebestands (Kap. 6) |
| R24 | Vorkommen von Gebäuden | KWK Z270 | **FS-Mengengerüst** — Gebäudewerte (Mon. Z65: „HQ-Szenarien × Schadensfunktionen × Gebäudewerte”) | **Mengengerüst** (Gebäudewerte, Mon. Z65) |
| R23 | Vorkommen von Bau- und Immobilienunternehmen | KWK Z269 | **inaktiv** — Schadenskonten-System Z28 (Spalte „Ausgeschlossen”): „Betriebsunterbrechung (→K5), Infrastruktur (→K4), Personen (→K1)” — Unternehmensschäden (Betriebsausfall der Bauwirtschaft) sind kein K3-Gebäudeschaden | laut W117-Anmerkung pauschal nach Regel 4 eingetragen; kein Bezug zu Gebäudeschäden — voraussichtlich bewusst inaktiv |
| R25 | Vorkommen von Siedlungsinfrastrukturen | KWK Z271 | **inaktiv** — Schadenskonten-System Z28 (Spalte „Ausgeschlossen”): „Betriebsunterbrechung (→K5), Infrastruktur (→K4), Personen (→K1)” | Infrastruktur → K4 (Konten Z28) — voraussichtlich bewusst inaktiv |

KWK = Sheet „Klimawirkungsketten“, NW = „Schadensbaum-Netzwerkliste“, Mon. = „Risiken-Monetarisierung“
(Blattzeile), Konten = „Schadenskonten-System“. Zusätzlich, kein Knoten der W117-Kette: W103
„Belastung oder Versagen von Hochwasserschutzsystemen“ (KWK Z226 = Id 50), nur als R7-Partner genannt.

### Weitergaben (zweispaltig; Quelle: Netzwerkliste + Abgleich-Protokoll)

| Output-Kanten (Netzwerkliste / Abgleich-Protokoll mit Punkt-Nr.) | Konto-Ausschlüsse / verwandte Buchungen (Konten-Definition, Monetarisierung) |
|---|---|
| **keine** — NW Z61 führt keine Output-IDs; das Abgleich-Protokoll hat keinen Punkt mit Quelle oder Ziel 60. Eingehend: **49 → 60** ist eine Originalkante (NW Z50, Mon. Z54 „→ 60, 74, 50, 101”), kein Abgleich-Punkt. | **K3 schließt aus** (Konten Z28): „Betriebsunterbrechung (→K5), Infrastruktur (→K4), Personen (→K1)”. **#60 schließt aus** (Mon. Z65): „Seeseitige Schäden (ID 46); Verkehrsinfrastruktur (ID 74); Schutzkosten (ID 50, R7)”. **Partitionsregel-Zitate, K3 geteilt:** #59 (Mon. Z64) „Nicht enthalten: Flusshochwasserschäden (ID 60)”; #46 (Mon. Z51) „Nicht enthalten: … flussseitige/Starkregenschäden (ID 59/60)”; **#37** Schäden an Aquakulturen — Kante **49 → 37** (Abgleich-Protokoll Punkt 3, Zeile 7: Quelle-ID 49 „Hochwasser” → Ziel 37 „Schäden an Aquakulturen”, Art „Kante”) mit R9-Zitat (Rechenregeln Z11): „Innerhalb eines Kontos zählt jede Einheit (… Gebäude) genau einmal; verschiedene Konten desselben Ereignisses sind additiv” i. V. m. Mon. Z42 (Spalte „Bewertungsansatz”): „… Sachschäden an Anlagen (K3)” — Teichwirtschafts-Anlagenschäden zählen unter #37, flussseitige Gebäudeschäden unter #60; **#12** Rutschungen und Muren — eigenständiges K3-Buchungsobjekt (Schadenskonten-System Z29: „12 Rutschungen und Muren”), R9-Zitat wie vor i. V. m. Mon. Z17 (Id 12, Spalte „Regeln”: „R7, R9”; Spalte „Bewertungsansatz”: „Wiederherstellungskosten beschädigter Gebäude (K3) …”) — Massenbewegungsschäden zählen unter #12, flussseitige Gebäudeschäden unter #60. **Ohne Partitionsregel in der Mappe (offen):** #92 touristische Infrastruktur (K3; Kante 49→92, P15), #102 Gesundheitsinfrastruktur (K3; 49→102, P16), Id 55 Direktbuchung K3 (P5). Personen-Folgen desselben Ereignisses: #101 (K1, andere Konten zulässig, Mon. Z106). |

### Konto-Einbettung

- **Konto:** K3 Gebäude und Sachwerte — Definition (Konten Z26): „Wiederherstellungskosten an
  Gebäuden, Hausrat, Fahrzeugen, Anlagen und Grundstücken (inkl. Landverlust), ereignisbezogen;
  Versicherungsleistungen sind Transfers.“ Kostensatz-Typ (Z27): „Wiederherstellungs-/Zeitwertkosten;
  Schadensfunktionen × Bestandswerte“.
- **Bewertungsbaustein:** K3-Wiederherstellung (NW Z61). Bewertungsansatz (Mon. Z65): „Wie ID 59,
  ereignisbezogen flussseitig; HQ-Szenarien × Schadensfunktionen (Wassertiefe-Schaden) ×
  Gebäudewerte.” Gegenstand: „Sachschäden flussseitiger Überflutung.”
- **Preisstandjahr (Abschätzung von KAP3, §3.9 ABGESCHÄTZT):** 2026. Herleitung: Keine der beiden
  Arbeitsmappen beziffert für K3-Wiederherstellungskosten ein Preisstandjahr (anders als K1/VOLY,
  Konten Z11: „Preisstand 2024”); Rechenregeln Z19 (A4) verlangt: „Konkrete Zahlen sind vor
  Produktivsetzung zu belegen.” Bis ein K3-eigener Kostensatz mit Quelle vorliegt (Kap. 3/7), wird
  das Erstellungsjahr dieses Berichtsteils als Preisstandjahr gesetzt und bei Bezifferung ersetzt
  (Ersetzungspfad, W1) — kein dauerhafter unspezifizierter Wert ohne Kennzeichnung als Abschätzung
  (Eiserne Regel 3, P1).
- **Rechenregeln:** R5 (übernommen), R7, R9 (Mon. Z65, Spalte „Regeln”: „R7, R9”); dazu Annahme A5
  Ereignislogik (Rechenregeln Z20): „Eintrittswahrscheinlichkeit × Schadensfunktion × Bestand;
  Schutzsysteme über die R7-Erwartungswert-Weiche”. **R5-Entscheidung (schließt offenen Punkt 4 des
  Erstaufschlags):** R5 (Rechenregeln Z7): „Versicherungsleistungen, Preisänderungen und
  Nachfrageverlagerungen zwischen Regionen sind (überwiegend) Umverteilung. Kommunal zählt die
  lokale reale Änderung; national wäre vieles davon Transfer.” wird **übernommen**. Die
  K3-Kontodefinition selbst trägt den Satz „Versicherungsleistungen sind Transfers” (Konten Z26);
  der Bewertungsansatz von #60 verweist mit „Wie ID 59” (Mon. Z65) auf #59, dessen eigener
  Bewertungsansatz R5 ausdrücklich anwendet (Mon. Z64: „… Versicherungsleistungen sind Transfers und
  mindern den Schaden nicht (R5).”). Dass die Regelspalte von Mon. Z65 nur „R7, R9” nennt, schließt
  R5 nicht aus — es ist bereits Bestandteil der Kontodefinition (Konten Z26) und wird deshalb dort
  nicht wiederholt.
- **Handlungserfordernis:** sehr dringend (Mon. Z65, NW Z61).
- **Nur K3 aktiv:** Folgen desselben Ereignisses in K1 (#101), K4 (#74), K5 und K8 (#50) sind nicht
  enthalten — Untergrenze, im Infokasten zu benennen (§3.6).

## 2 Evidenz-Register (§2.2)

Skelett mit einer Zeile je Knoten der Bilanz. Die Zeilen sind in `docs/evidenz/register.md`
gespiegelt. Wiederverwendbare Zeilen fanden sich dort nicht (Register führt bisher nur K1-Zeilen
aus #95/#96/#98). In Formeln (§3) dürfen später nur Zeilen mit Entscheidung **Basiswert** stehen.

| Register-ID | Knoten → Outcome | Effektgröße | Studientyp | Quelle | Übertragbarkeit | Datenlage je Zelle | Entscheidung |
|---|---|---|---|---|---|---|---|
| 60-W085-01 | W085 Hochwasser → Überflutungswahrscheinlichkeit/-tiefe am Gebäude | p(HQ) je Pflicht-Szenario der Hochwassergefahrenkarte: HQhäufig 1,0·10⁻¹ a⁻¹ (Kartenfall HQ10; Spanne HQ5–HQ20 = 2,0·10⁻¹ bis 5,0·10⁻² a⁻¹), HQ100 1,0·10⁻² a⁻¹, HQextrem 5,0·10⁻³ bis 1,0·10⁻³ a⁻¹ (WHG-Mindestvorgabe 200 a gegen Länderpraxis ≈ HQ1000); je Szenario liefert die Karte flächendeckend die Wassertiefe in den Klassen 0–0,5 / >0,5–1 / >1–2 / >2–4 / >4 m | amtliche Kartengrundlage nach HWRM-RL (Pegel- bzw. Regionalisierungsstatistik plus hydrodynamische Berechnung) auf rechtlich normierter Szenariendefinition | LAWA 2024, „Empfehlungen zur Aufstellung von Hochwassergefahrenkarten und Hochwasserrisikokarten“, S. 4 und 16, https://www.lawa.de/documents/2024-01-lawa-empfehlungen-aufstellung-hochwassergefahrenkarten-barrierefrei_1739980622.pdf, Zugriff 13.09.2026; § 74 Abs. 2/3 WHG, https://www.gesetze-im-internet.de/whg_2009/__74.html, Zugriff 13.09.2026; LfU Bayern, „FAQ: Hochwassergefahren- und -risikokarten“, https://www.lfu.bayern.de/wasser/hw_risikomanagement_umsetzung/faq_karten/index.htm, Zugriff 13.09.2026 — Volltext geprüft; Langbeleg **B1** unter der Tabelle | DE-weit für die Risikogebiete nach § 73 WHG, da die Szenarien bundeseinheitlich normiert sind; **Modellgrenze:** außerhalb der kartierten Risikogebiete trifft die Karte keine Aussage, und das Wiederkehrintervall des Extremszenarios ist bundesweit uneinheitlich (mindestens 200 a nach WHG gegen ≈ 1000 a in der Länderpraxis) — als Band geführt, nicht geglättet | HWGK-Raster der Länder über den BfG-Kartendienst WasserBLIcK; Abgleich nach §3.4 auf Bundesland- und Gemeindepunkt-Stichproben, kein Vollraster-Lauf | **Basiswert** — FS-Hazard: die drei Szenario-Stützstellen p(HQ) samt zugehöriger Wassertiefe; die Spannen von HQhäufig und HQextrem laufen als Sensitivitätsband mit |
| 60-E12-01 | E12 Schneeschmelze → W085 | offen | offen | offen | offen | offen | offen |
| 60-E07-01 | E07 Nässe → W085 | offen | offen | offen | offen | offen | offen |
| 60-E08-01 | E08 Starkregen → W085 / Gebäudeschaden | offen | offen | offen | offen | offen | offen |
| 60-S072-01 | S072 Boden-/Vegetationsbedeckung → Abfluss (W085) | offen | offen | offen | offen | offen | offen |
| 60-S073-01 | S073 Flächenversiegelung → Abfluss (W085) | offen | offen | offen | offen | offen | offen |
| 60-S074-01 | S074 Topographie → Wassertiefe am Gebäude | h(Gebäude) = max(0; Wasserspiegellage − Geländehöhe DGM1); der Höhenfehler des DGM1 (σ_z = 0,15–0,20 m) schlägt 1:1 auf die Wassertiefe durch; Schadenswirkung der Wassertiefe: 5,3–6,2 % Schadensänderung je 10 cm (Mittel ≈ 6 %/10 cm) ⇒ σ_z = 0,20 m entspricht ±10,6 bis ±12,4 % Schaden; ±0,5 m ⇒ Faktor 1,35–1,44; ein Faktor 2 erfordert 0,95–1,1 m | amtliche Produktspezifikation eines Geobasisdatensatzes (Airborne Laserscanning) plus publizierte Unsicherheits- und Sensitivitätsrechnung eines Hochwasserschadensmodells (systematische Variation der Überflutungstiefe) | LAIV MV (Landesamt für innere Verwaltung Mecklenburg-Vorpommern), „Geländemodelle“ (Höhengenauigkeit DGM1 0,15–0,2 m), https://www.laiv-mv.de/Geoinformation/Geobasisdaten/Gelaendemodelle/, Zugriff 13.09.2026; de Moel, H. & Aerts, J. C. J. H. 2011, „Effect of uncertainty in land use, damage models and inundation depth on flood damage estimates“, Natural Hazards 58(1), 407–425, DOI 10.1007/s11069-010-9675-6, Zugriff 13.09.2026 — Volltext geprüft (Tab. 4, S. 421; Abschn. 4.3, S. 420); Langbeleg **B2** unter der Tabelle | DGM1 flächendeckend in DE verfügbar; die Tiefen-Sensitivität stammt aus einer niederländischen Fallstudie (Rheindelta, flaches Relief, Landnutzungs-Schadensmodelle). **Modellgrenze:** der Wert gilt für aggregierte Landnutzungsklassen, nicht für das Einzelgebäude, und ist in Mittelgebirgs- und Steillagen eine Untergrenze, weil dort derselbe Höhenfehler größere Tiefenfehler erzeugt | DGM1 (1 m Rasterweite) der Landesvermessungen; Prüfung nach §3.4 auf Gemeindepunkt-Stichproben, kein Vollraster-Lauf | **Sensitivitätsband** — Kein-Doppelkanal §3.2: die Geländehöhe wirkt bereits über die HWGK-Wassertiefe der Zeile 60-W085-01 und geht deshalb nicht als eigener Faktor in FS-Exposition ein; ihr eigener Beitrag ist das Tiefen-Unsicherheitsband ±0,20 m ⇒ ±12 % um den Basiswert |
| 60-R17-01 | R17 Oberflächengewässer → Exposition | Exponiertenquote der Adressen am Gewässernetz (ZÜRS Geo, Stand 2025; Bezugsgröße 22,6 Mio bundesweit bewertete Adressen): GK1 92,4 % (≈ 20,88 Mio) „statistisch nach gegenwärtiger Datenlage nicht von Hochwasser größerer Gewässer betroffen“, GK2 6,1 % (≈ 1,38 Mio; seltener als HQ100, einschließlich deichgeschützter Objekte), GK3 1,1 % (≈ 249.000; HQ10–HQ100), GK4 0,4 % (≈ 90.400; „Hochwasser statistisch mindestens einmal in 10 Jahren“) ⇒ exponiert GK2–GK4 = 7,6 % ≈ 1,72 Mio Adressen, flussnah im HQ100-Band GK3+GK4 = 1,5 % ≈ 339.000 Adressen | Bestandsstatistik (adressscharfe Vollzonierung des versicherten Bestands auf Basis der wasserwirtschaftlichen Länderdaten) — keine Studie | GDV (Gesamtverband der Deutschen Versicherer) 2025, „Geringe Gefahr für Fluss-Hochwasser bei den meisten Wohngebäuden“, Datenservice zum Naturgefahrenreport, Stand ZÜRS Geo 2025, https://www.gdv.de/gdv/statistik/datenservice-zum-naturgefahrenreport/sachversicherung-elementar/geringe-gefahr-fuer-fluss-hochwasser-bei-den-meisten-wohngebaeuden--147672, Zugriff 13.09.2026; GDV, „ZÜRS Geo — Zonierungssystem für Überschwemmungsrisiko und Einschätzung von Umweltrisiken“, https://www.gdv.de/gdv/themen/klima/-zuers-geo-zonierungssystem-fuer-ueberschwemmungsrisiko-und-einschaetzung-von-umweltrisiken-11656, Zugriff 13.09.2026 — Volltext geprüft (GK1 92,4 %, GK4 0,4 %, 22,6 Mio Adressen wörtlich; GK2/GK3-Aufteilung aus der GDV-Klassengrafik, Residualprobe unten); Langbeleg **B3** unter der Tabelle | DE-weit adressscharf, Stand 2025. **Modellgrenzen:** (a) ZÜRS zählt versicherbare **Adressen**, nicht Gebäude — je Adresse können mehrere Gebäude stehen, die Quote ist deshalb keine Gebäudequote; (b) die ZÜRS-Klassen und die Risikogebiete nach § 73 WHG sind **nicht deckungsgleich** (ZÜRS zoniert bundesweit alle bewerteten Adressen, die HWGK nur Gewässer mit signifikantem Risiko) — der Widerspruch wird benannt, nicht geglättet (§3.8); (c) GK2 enthält ausdrücklich deichgeschützte Objekte, ist also keine Restrisiko-freie Klasse | ZÜRS Geo ist nicht offen (Zugang nur für Versicherer) ⇒ die Zellgröße bildet das Produkt aus der HWGK-Überflutungsfläche (60-W085-01) × Gebäudebestand (60-R24-01); die ZÜRS-Quote dient als bundes- und bundeslandweites Abgleichsband nach §3.4 (Stichprobe, kein Vollraster-Lauf) | **Sensitivitätsband** — Kein-Doppelkanal §3.2: die zellgenaue Exposition entsteht bereits aus 60-W085-01 × 60-R24-01; R17 liefert kein zweites Multiplikativglied, sondern das nationale Prüfband (7,6 % aller Adressen in GK2–GK4, davon 1,5 % im HQ100-nahen Band) für den Abgleich nach §3.4 |
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
| 60-S092-01 | S092 Vorsorge der Eigentümer (Objektschutz) → Gebäudeschaden | im Erstaufschlag **keine nach §3.5 zulässige** (Interventions-/quasi-experimentelle) Effektgröße belegt ⇒ **Abschätzung von KAP3** \(r_{\text{S092}}\) = 0,035 (Band 0,0075–0,112), Kette §5.1 | — (keine Interventionsstudie belegt; Befragungen nach Ereignissen sind nur Kandidat, im Volltext nicht verifiziert, gehen nicht in den Wert ein) | Herleitung §5.1 (`#s092-wirkung`) | §3.9 ABGESCHÄTZT; Setzung für deutsche Kommunen | kommunal (Pauschalfaktor — Modellgrenze der Abschätzung) | **Maßnahmen-Hebel (abgeschätzt)** — FS-Vorsorge; wirkt multiplikativ auf den Erwartungsschaden (§5.1), Wert und Band sind die Abschätzung von KAP3 nach §3.9/Vorgabe P2, Herleitung §5.1 (`#s092-wirkung`) |
| 60-S093-01 | S093 Gebäudezustand → Schadensgrad | Zustands-/Qualitätsachse der Wassertiefe-Schadensfunktion: FLEMOps führt die Gebäudequalität als eigene Eingangsachse mit **zwei Klassen** („Low/medium quality“ / „high quality“) neben Wasserstand (5 Klassen: <21 / 21–60 / 61–100 / 101–150 / >150 cm) und Gebäudetyp (3 Klassen); die Schadensquote des Gebäudes steigt über diese Wasserstandsklassen von ≈ 3,5 % auf ≈ 25 %, die Qualitätsachse ist jedoch **nur grafisch** (Fig. 1) und ohne Zahlentabelle je Qualitätsklasse publiziert ⇒ **Abschätzung von KAP3** \(f_{\text{S093}}\) = 1,00 (mittelwertzentriert auf den Bestandsmix), **Band 0,80–1,25** (Spannweitenfaktor 1,57 zwischen den beiden Zustandsklassen), Kette in B5; Sensitivität: ±25 % auf den Schadensgrad je Zelle (gegen ±12 % Tiefenband aus 60-S074-01) | empirische Mehrfaktor-Schadensfunktion aus Betroffenenbefragung (1.697 im August 2002 betroffene Haushalte), validiert an Instandsetzungskosten von 1.274 Einzelgebäuden in drei sächsischen Kommunen; die Zustandsachse selbst ist in der Quelle nur als Grafik ausgewiesen, der Bandwert ist deshalb eine Abschätzung von KAP3 (§3.9) | Thieken, A. H.; Olschewski, A.; Kreibich, H.; Kobsch, S.; Merz, B. 2008, „Development and evaluation of FLEMOps – a new Flood Loss Estimation MOdel for the private sector“, WIT Transactions on Ecology and the Environment 118, 315–324, WIT Press, DOI 10.2495/FRIAR080301, https://www.witpress.com/elibrary/wit-transactions-on-ecology-and-the-environment/118/19311, Zugriff 13.09.2026 — Volltext geprüft (Tab. 1 S. 317; Fig. 1 und Tab. 2 S. 318; S. 319 und S. 323); Elmer, F.; Thieken, A. H.; Pech, I.; Kreibich, H. 2010, „Influence of flood frequency on residential building losses“, Natural Hazards and Earth System Sciences 10, 2145–2159, DOI 10.5194/nhess-10-2145-2010, https://nhess.copernicus.org/articles/10/2145/2010/, Zugriff 13.09.2026 — Volltext geprüft (S. 2151) — Langbeleg **B5** unter der Tabelle | DE (Elbe- und Donaueinzugsgebiet, Ereignisse 2002 sowie 2005/2006). **Modellgrenzen:** (a) die Qualitätsklassen stammen aus den INFAS-Ausstattungsklassen („value of the equipment, windows, doors etc.“, sechs Klassen), nicht aus einer bautechnischen Zustandserhebung — die Lesart „Gebäudezustand“ ist eine dokumentierte Annahme; (b) die **Richtung** der Achse ist aus der Quelle nicht auflösbar: die Beschriftung von Fig. 1 ordnet die höheren Schadensquoten der Klasse „high building quality“ zu, was der erwarteten Richtung widerspricht, und eine Zahlentabelle zur Auflösung fehlt — der Widerspruch wird benannt, nicht geglättet (§3.8); das Band läuft deshalb symmetrisch um 1; (c) die Quelle stellt selbst infrage, ob ein an einem Extremereignis abgeleitetes Schadensmodell auf häufigere Hochwasser anwendbar ist — für HQhäufig ist das Band eine Untergrenze | keine bundesweite offene Zustandserhebung des Gebäudebestands (Datenlücke §3.8); als schwacher Proxy je 100-m-Zelle stehen Baujahrsklasse und Gebäudetyp der Zensus-2022-Gebäude- und Wohnungszählung zur Verfügung (der Bauzustand selbst wird dort nicht erhoben); die Achse läuft deshalb als bundesweit einheitliches Band auf der Ebene GEBAEUDEWERT (60-R24-01) mit; Abgleich nach §3.4 auf Bundesland- und Gemeindepunkt-Stichproben, kein Vollraster-Lauf | **Sensitivitätsband, abgeschätzt** — mittelwertzentriert \(f_{\text{S093}}\) = 1,00 für den Bestandsmix (§3.2), also kein eigenes Multiplikativglied im Basiswert; das Band 0,80–1,25 läuft als Struktur-Unsicherheit der Schadensfunktion mit und wird im Produkt nach Vorgabe P1/P2 als „Abschätzung von KAP3“ samt Herleitung (B5) ausgewiesen |
| 60-S094-01 | S094 Baumaterialien → Schadensgrad | Materialachse der Wassertiefe-Schadensfunktion: die empirischen deutschen Wohngebäude-Schadensmodelle führen **keine** Baustoffachse (FLEMOps-Eingangsgrößen: Wasserstand, Gebäudetyp, Gebäudequalität, Kontamination, private Vorsorge), und die ingenieurmäßige Schadensgradskala D1–D6 gilt laut Quelle „zunächst für die allgemeine Bebauung vornehmlich in Mauerwerksbauweise“; jedes von der Einwirkung betroffene Bauwerk ist dort mindestens D1 (reiner Durchfeuchtungsschaden) ⇒ **Abschätzung von KAP3** \(f_{\text{S094}}\) = 1,00 (mittelwertzentriert), **Band 0,89–1,12** (halber logarithmischer Anteil der Zustandsachse S093), Kette in B6; Sensitivität: ±12 % auf den Schadensgrad, gemeinsam mit 60-S093-01 multiplikativ **0,71–1,40** | ingenieurmäßige Klassifikation real beobachteter Schadensbilder aus Feldeinsätzen (Hochwasser Sachsen 2002/2006/2010/2013, Sturzflut Braunsbach 2015) mit sechs- bzw. siebenstufiger Schadensgradskala D0–D6; der Zahlenwert selbst ist keine publizierte Effektgröße, sondern eine Abschätzung von KAP3 (§3.9) | Maiwald, H.; Schwarz, J. 2018, „Vereinheitlichte Schadensbeschreibung und Risikobewertung von Bauwerken unter extremen Naturgefahren“, Bautechnik 95(10), 743–753, Ernst & Sohn, DOI 10.1002/bate.201800009, https://edac.biz/fileadmin/Dokumente/06_Publikationen/Bautechnik_1018_Maiwald_Schwarz.pdf, Zugriff 13.09.2026 — Volltext geprüft (Tab. 1 und Abschn. 3.1 S. 744–745, Tab. 2 S. 745, Tab. 3 S. 746, Tab. 4 S. 747); Thieken u. a. 2008 (Fundstelle wie 60-S093-01, Tab. 1 S. 317), DOI 10.2495/FRIAR080301, Zugriff 13.09.2026 — Volltext geprüft — Langbeleg **B6** unter der Tabelle | DE (Sachsen, Baden-Württemberg). **Modellgrenzen — Bauform-Grenze der Abschätzung (Vorgabe P2):** (a) die Schadensgradbeschreibungen sind mauerwerksbasiert, materialspezifische Schadensbilder für Holz-, Fachwerk- und Leichtbaukonstruktionen sind nach eigener Aussage der Quelle „in weiterführenden Arbeiten im Detail noch herauszuarbeiten“ — für diese Bauformen ist das Band eine Untergrenze und wird nicht stillschweigend verallgemeinert; (b) die Skala ist an Extremereignissen einschließlich einer Sturzflut kalibriert (dort Dislokation ganzer Bauwerke, Schadensgrad D6), das Produkt rechnet Flusshochwasser mit deutlich geringerer Fließgeschwindigkeit; (c) die Skala beschreibt Schadensgrade, nicht Schadensquoten in Euro — die Umrechnung ist nicht Bestandteil der Quelle und bleibt Teil der Abschätzung | Baumaterial ist in der amtlichen Statistik (Zensus 2022, Hausumringe, ALKIS) bundesweit nicht als Merkmal geführt — ausdrückliche Datenlücke (§3.8); nutzbar sind je 100-m-Zelle nur Baujahrsklasse und Gebäudetyp als schwacher Materialproxy; die Achse läuft deshalb als bundesweit einheitliches Band auf der Ebene GEBAEUDEWERT (60-R24-01) mit; Abgleich nach §3.4 auf Bundesland- und Gemeindepunkt-Stichproben, kein Vollraster-Lauf | **Sensitivitätsband, abgeschätzt** — mittelwertzentriert \(f_{\text{S094}}\) = 1,00 für den Bestandsmix (§3.2), kein eigenes Multiplikativglied im Basiswert; das Band 0,89–1,12 läuft als Struktur-Unsicherheit mit und wird im Produkt nach Vorgabe P1/P2 als „Abschätzung von KAP3“ samt Herleitung (B6) ausgewiesen |
| 60-S096-01 | S096 Vorsorge der öffentlichen Hand → Überflutungswahrscheinlichkeit | offen | offen | offen | offen | offen | offen (Vorschlag: R7-Weiche mit #50) |
| 60-S097-01 | S097 Zustand Schutzinfrastruktur → Versagenswahrscheinlichkeit | offen | offen | offen | offen | offen | offen (Vorschlag: R7-Weiche mit #50) |
| 60-S098-01 | S098 Baumaterialien Schutzinfrastruktur → Versagenswahrscheinlichkeit | offen | offen | offen | offen | offen | offen (Vorschlag: R7-Weiche mit #50) |
| 60-S104-01 | S104 Investitionen in exponierten Gebieten → Bestandsentwicklung | offen | offen | offen | offen | offen | offen |
| 60-R24-01 | R24 Gebäude → Mengengerüst (Gebäudewerte) | **Menge:** 19,7 Mio Wohngebäude (13,5 Mio Einfamilien-, 2,7 Mio Zweifamilien-, 3,5 Mio Mehrfamilienhäuser), 43,8 Mio Wohnungen, 4,1 Mrd m² Wohnfläche (31.12.2024) ⇒ 208 m² Wohnfläche je Wohngebäude; Fortschreibung 31.12.2025: 44,0 Mio Wohnungen, 4,1 Mrd m². **Wertsatz (Wiederherstellung/Neubauwert):** NHK 2010 Standardstufe 3 (mittlerer Standard) = 1.050 €₂₀₁₀/m² BGF (freistehende Ein-/Zweifamilienhäuser, Geb.-Art 1.01) bzw. 825 €₂₀₁₀/m² BGF (Mehrfamilienhäuser ≤ 6 WE), je inkl. Umsatzsteuer und Baunebenkosten; Indexierung mit dem Baupreisindex Wohngebäude (2015 = 100: 2010 = 89,1 → 2023 = 149,8, Faktor 1,681) ⇒ 1.765 bzw. 1.387 €₂₀₂₃/m² BGF; Fortschreibung 2023 → Preisstand 2026 mit Faktor 1,105 (Band 1,07–1,16; §3.9 **abgeschätzt**, Kette in B4) ⇒ **1.950 €₂₀₂₆/m² BGF (Band 1.889–2.047)** bzw. **1.533 €₂₀₂₆/m² BGF (Band 1.484–1.609)**; BGF je m² Wohnfläche = 1,30 (Band 1,25–1,40; §3.9 **abgeschätzt**) ⇒ Wertdichte 1.993–2.535 €₂₀₂₆/m² Wohnfläche ⇒ Wiederherstellungswert des Wohngebäudebestands 8,2–10,4 Bio. €₂₀₂₆ (Sensitivität: ±10 % auf den Indexfaktor verschieben den Bestandswert um ±0,8–1,0 Bio. €) | amtliche Statistik (Fortschreibung des Wohngebäude- und Wohnungsbestands auf Zensus-2022-Basis) + normierter Kostenkennwert aus Rechtsverordnung (ImmoWertV Anlage 4), fortgeschrieben mit amtlichem Preisindex | Destatis 2025, Pressemitteilung Nr. 336 vom 17.09.2025, „43,8 Millionen Wohnungen in Deutschland zum Jahresende 2024“, https://www.destatis.de/DE/Presse/Pressemitteilungen/2025/09/PD25_336_31231.html, Zugriff 13.09.2026; Destatis, Themenseite „Wohnen“ (Fortschreibung zum 31.12.2025: 44,0 Mio Wohnungen, 4,1 Mrd m²), https://www.destatis.de/DE/Themen/Gesellschaft-Umwelt/Wohnen/_inhalt.html, Zugriff 13.09.2026; ImmoWertV, Anlage 4 (zu § 36 Abs. 1) „Normalherstellungskosten 2010 (NHK 2010)“, https://www.gesetze-im-internet.de/immowertv_2022/anlage_4.html, Zugriff 13.09.2026; Destatis, Fachserie 17 Reihe 4 „Preisindizes für die Bauwirtschaft“ (Basis 2015 = 100), https://www.destatis.de/DE/Themen/Wirtschaft/Preise/Baupreise-Immobilienpreisindex/Publikationen/Downloads-Bau-und-Immobilienpreisindex/bauwirtschaft-preise-2170400223244.pdf?__blob=publicationFile, Zugriff 13.09.2026; Destatis 2026, PM Nr. 241 vom 10.07.2026 (Baupreise Wohngebäude Mai 2026: +5,0 % gg. Vj.), https://www.destatis.de/DE/Presse/Pressemitteilungen/2026/07/PD26_241_61261.html, Zugriff 13.09.2026 — Volltext geprüft; Langbeleg **B4** unter der Tabelle (Mon. Z65: „Gebäudewerte“) | DE-weit. **Modellgrenzen:** (a) NHK-Standardstufe 3 als bundesweiter Einheitssatz — ohne Regionalfaktor der Gutachterausschüsse streut der Wertsatz zwischen Hoch- und Niedrigpreisregionen um schätzungsweise ±20 %; (b) **Nichtwohngebäude** (Gewerbe, öffentliche Gebäude) sind im Mengengerüst nicht enthalten — die Mengenbasis ist insoweit eine Untergrenze (§3.6); (c) NHK sind **Neubau-/Wiederherstellungswerte**; die Zeitwert-Lesart (Alterswertminderung nach ImmoWertV) liegt je nach Restnutzungsdauer deutlich darunter — der Unterschied wird als Band geführt, nicht geglättet (§3.8) | Gebäudezahl und Wohnfläche je Zelle aus dem Zensus-2022-Gitter (100 m) bzw. den amtlichen Hausumringen; Datenebene GEBAEUDEWERT **neu anzulegen** (§3.1, Spezifikation in Kap. 3), Fortschreibung über die Destatis-Bestandsfortschreibung; Abgleich nach §3.4 auf Bundesland- und Gemeindepunkt-Stichproben, kein Vollraster-Lauf | **Basiswert** — FS-Mengengerüst: Wohnfläche je Zelle × Wertdichte €₂₀₂₆/m²; die Zeitwert-Lesart sowie die abgeschätzten Faktoren (Indexierung 2023→2026, BGF/Wohnfläche) laufen als Sensitivitätsband mit und werden im Produkt nach Vorgabe P1/P2 als Abschätzung von KAP3 ausgewiesen |
| 60-R23-01 | R23 Bau- und Immobilienunternehmen → Gebäudeschaden | offen | offen | offen | offen | offen | offen |
| 60-R25-01 | R25 Siedlungsinfrastrukturen → Gebäudeschaden | offen | offen | offen | offen | offen | offen |

### Belege zu den entschiedenen Registerzeilen (§3.8, Volltext geprüft am 13.09.2026)

**B1 — 60-W085-01 (Hazard-Szenarien und Überflutungstiefe).**
Quellen: (1) **LAWA — Bund/Länder-Arbeitsgemeinschaft Wasser (2024):** „Empfehlungen zur
Aufstellung von Hochwassergefahrenkarten und Hochwasserrisikokarten“, Stand Januar 2024,
beschlossen durch die 167. LAWA-Vollversammlung am 21./22.03.2024 in Potsdam, Herausgeber LAWA,
Potsdam; URL
`https://www.lawa.de/documents/2024-01-lawa-empfehlungen-aufstellung-hochwassergefahrenkarten-barrierefrei_1739980622.pdf`,
Zugriff 13.09.2026. S. 4 wörtlich: „Hochwasser mit niedriger Wahrscheinlichkeit oder Szenarien für
Extremereignisse“ · „Hochwasser mit mittlerer Wahrscheinlichkeit (Ereignisse, die im statistischen
Mittel einmal in 100 Jahren auftreten)“ · „gegebenenfalls Hochwasser mit hoher Wahrscheinlichkeit“;
anzugeben sind „Ausmaß der Überflutung (Fläche)“ und „Wassertiefe bzw. gegebenenfalls
Wasserstand“. S. 16 wörtlich: „Für jedes Hochwasserszenario sind sowohl das Ausmaß der Überflutung
(Überflutungsgebiet) als auch die Wassertiefen in den Karten darzustellen.“ und zu den Klassen:
„0–0,5 m, >0,5–1 m, >1–2 m, >2–4 m und >4 m“. S. 10 wörtlich zum Klimabezug: „Der bisher wirksam
gewordene Einfluss von Klimaveränderungen ist in den Daten der hydrologischen Statistiken
enthalten.“ (2) **§ 74 Abs. 2/3 WHG**, Fassung abgerufen unter
`https://www.gesetze-im-internet.de/whg_2009/__74.html`, Zugriff 13.09.2026; Abs. 2 Nr. 1 wörtlich:
„Hochwasser mit niedriger Wahrscheinlichkeit (voraussichtliches Wiederkehrintervall mindestens 200
Jahre) oder bei Extremereignissen“. (3) **Bayerisches Landesamt für Umwelt (LfU), „FAQ:
Hochwassergefahren- und -risikokarten“**, URL
`https://www.lfu.bayern.de/wasser/hw_risikomanagement_umsetzung/faq_karten/index.htm`,
Zugriff 13.09.2026; wörtlich: HQhäufig ist „ein Abfluss (Q) verstanden, der statistisch gesehen im
Mittel alle 5 bis 20 Jahre auftritt“ (die Karten zeigen ein HQ10), HQ100 ist „ein Abfluss (Q), der
im Mittel alle hundert Jahre erreicht oder überschritten wird“, HQextrem entspricht ungefähr einem
HQ1000. **Rechenschritt (§3.9 Übernommen):** p = 1/T mit T aus den zitierten Wiederkehrintervallen
— für das häufige Szenario gilt der kartierte Fall HQ10, also T = 10 a ⇒ p = 1,0·10⁻¹ a⁻¹;
die von LfU genannte Bandbreite der Praxis (T = 5 a bis T = 20 a ⇒ 2,0·10⁻¹ a⁻¹ bis
5,0·10⁻² a⁻¹) läuft als Sensitivitätsband mit. Für das mittlere Szenario gilt T = 100 a ⇒
p = 1,0·10⁻² a⁻¹. Für das Extremszenario
**benennt der Bericht den Widerspruch der Quellen, statt ihn zu glätten** (§3.8): das WHG verlangt
mindestens 200 a (⇒ 5,0·10⁻³ a⁻¹), die Länderpraxis kartiert ≈ HQ1000 (⇒ 1,0·10⁻³ a⁻¹); beide
Enden bilden das Band. **Datenlücke (§3.8):** eine bundesweit einheitliche Angabe des tatsächlich
kartierten Extrem-Wiederkehrintervalls je Land liegt nicht vor; sie ist bei der Datenanbindung je
Land zu erheben.

**B2 — 60-S074-01 (Geländehöhe → Wassertiefe am Gebäude).**
Quellen: (1) **LAIV MV — Landesamt für innere Verwaltung Mecklenburg-Vorpommern, „Geländemodelle“**,
URL `https://www.laiv-mv.de/Geoinformation/Geobasisdaten/Gelaendemodelle/`, Zugriff 13.09.2026;
wörtlich zur Höhengenauigkeit des DGM1: „0,15 – 0,2 m“, zur Erfassung: „Dominierende
Erfassungsmethoden für die Erhebung der Messdaten sind das Airborne Laserscanning und die
Bildkorrelation auf Basis orientierter Luftbildpaare.“ (2) **de Moel, H.; Aerts, J. C. J. H.
(2011):** „Effect of uncertainty in land use, damage models and inundation depth on flood damage
estimates“, *Natural Hazards* 58(1), 407–425, Springer, DOI `10.1007/s11069-010-9675-6`
(Verlagsfassung, Open Access), Zugriff 13.09.2026. Volltext gegengelesen, Abschn. 4.3 (S. 420)
wörtlich: „a 0.5-m reduction in inundation depth corresponds to a factor 1.35–1.44 difference in
the resulting damage estimate“ · „A variation in inundation depth of more than 1 m (0.95 m using
DM1 to 1.1 m using DM3) is necessary to cause a factor 2 difference“; Tab. 4 (S. 421):
proportionale Schadensänderung je 10 cm Überflutungstiefe 5,3 %–6,2 % (Streuung zwischen den drei
Schadensmodellen Faktor 1,14, zwischen den Landnutzungskarten Faktor 1,04), im Fließtext (S. 421)
„almost 6 % … per 10 cm inundation depth change“. **Rechenschritt (§3.9 Abgeleitet):** der
DGM1-Höhenfehler geht als Tiefenfehler ein (h = Wasserspiegellage − Geländehöhe), also
σ_z = 0,20 m = 2,0 × 10 cm; mit 5,3 %/10 cm bzw. 6,2 %/10 cm folgt 2,0 × 5,3 % = 10,6 % bzw.
2,0 × 6,2 % = 12,4 % Schadensänderung, gerundet ±12 % als Bandmitte-nahe Obergrenze. Die Linearität
ist nur im geprüften Bereich der Quelle (−0,5 m bis 0 m) belegt und wird nicht extrapoliert.
**Kopplung (§3.9):** das Band hängt an der Wassertiefe aus 60-W085-01; ändert sich dort die
Tiefenquelle, wird es neu gerechnet. **Abgrenzung zur Knoten-Bilanz:** S074 bleibt der
Formelstelle FS-Exposition zugeordnet, wirkt dort aber über die bereits topographiebasierte
HWGK-Wassertiefe; ein zweiter Topographie-Faktor wäre ein Doppelkanal (§3.2). **Datenlücke
(§3.8):** eine deutsche Sensitivitätsrechnung derselben Bauart (Schaden je 10 cm Tiefe) wurde nicht
gefunden; die niederländische Fallstudie wird als dokumentierte Übertragung geführt.

**B3 — 60-R17-01 (Exposition am Gewässernetz).**
Quellen: (1) **GDV — Gesamtverband der Deutschen Versicherer (2025):** „Geringe Gefahr für
Fluss-Hochwasser bei den meisten Wohngebäuden“, Datenservice zum Naturgefahrenreport,
Stand ZÜRS Geo 2025; URL
`https://www.gdv.de/gdv/statistik/datenservice-zum-naturgefahrenreport/sachversicherung-elementar/geringe-gefahr-fuer-fluss-hochwasser-bei-den-meisten-wohngebaeuden--147672`,
Zugriff 13.09.2026. Wörtlich zur Gefährdungsklasse 1 (92,4 %): „statistisch nach gegenwärtiger
Datenlage nicht von Hochwasser größerer Gewässer betroffen“; wörtlich zur Gefährdungsklasse 4
(0,4 %): „Hochwasser statistisch mindestens einmal in 10 Jahren“; Bezugsgröße: 22,6 Mio erfasste
Adressen. (2) **GDV, „ZÜRS Geo — Zonierungssystem für Überschwemmungsrisiko und Einschätzung von
Umweltrisiken“**, URL
`https://www.gdv.de/gdv/themen/klima/-zuers-geo-zonierungssystem-fuer-ueberschwemmungsrisiko-und-einschaetzung-von-umweltrisiken-11656`,
Zugriff 13.09.2026; wörtlich zur Klasse 2: in ihr sind „auch Objekte enthalten, die durch einen
Deich geschützt sind“, sofern dieser mindestens einem hundertjährlichen Hochwasser standhält;
Objekte im Umkreis von 100 m zu einem Bach tragen zusätzlich den Vermerk „Bachzone“.
**Rechenschritt (§3.9 Abgeleitet):** aus den beiden wörtlich belegten Anteilen folgt die
Exponiertenquote als Residuum 100 % − 92,4 % = **7,6 %** (GK2–GK4) und daraus GK2 + GK3 =
7,6 % − 0,4 % = **7,2 %**. Die Aufteilung dieses Residuums auf GK2 = 6,1 % und GK3 = 1,1 % stammt
aus der GDV-Klassengrafik („Gefährdung durch Hochwasser“, Anteile 92,4 / 6,1 / 1,1 / 0,4 %);
sie ist mit dem Residuum konsistent (6,1 + 1,1 = 7,2 ✓). Absolutzahlen aus 22,6 Mio Adressen:
GK4 0,004 × 22,6 Mio = 90.400; GK3 0,011 × 22,6 Mio = 248.600 ≈ 249.000; GK2 0,061 × 22,6 Mio =
1.378.600 ≈ 1,38 Mio; GK2–GK4 0,076 × 22,6 Mio = 1.717.600 ≈ 1,72 Mio; GK3 + GK4 = 1,5 % =
339.000. **Widerspruch (§3.8, benannt statt geglättet):** ZÜRS zoniert alle bundesweit bewerteten
Adressen, die Hochwassergefahrenkarten (60-W085-01) nur die Risikogebiete nach § 73 WHG; die
Exponiertenzahlen beider Quellen sind deshalb **nicht** ineinander überführbar und werden
nebeneinander geführt. **Datenlücke (§3.8):** der GDV veröffentlicht keine Absolutzahlen je Klasse
und keine maschinenlesbare Fassung der Klassengrafik; die Prozentanteile der Klassen 2 und 3 sind
nur grafisch belegt, die Residualprobe ist die einzige verfügbare Gegenrechnung. Eine offene,
adressscharfe Exponiertenstatistik der amtlichen Statistik existiert nicht — die Zellgröße des
Produkts wird deshalb aus HWGK × Gebäudebestand gebildet, ZÜRS bleibt Abgleichsband.

**B4 — 60-R24-01 (Mengengerüst der Gebäudewerte).**
Quellen: (1) **Statistisches Bundesamt (2025):** Pressemitteilung Nr. 336 vom 17.09.2025,
„43,8 Millionen Wohnungen in Deutschland zum Jahresende 2024“, URL
`https://www.destatis.de/DE/Presse/Pressemitteilungen/2025/09/PD25_336_31231.html`,
Zugriff 13.09.2026; Stichtag 31.12.2024: 43,8 Mio Wohnungen, 4,1 Mrd m² Wohnfläche,
19,7 Mio Wohngebäude (13,5 Mio Einfamilien-, 2,7 Mio Zweifamilien-, 3,5 Mio Mehrfamilienhäuser).
(2) **Statistisches Bundesamt, Themenseite „Wohnen“**, URL
`https://www.destatis.de/DE/Themen/Gesellschaft-Umwelt/Wohnen/_inhalt.html`, Zugriff 13.09.2026;
wörtlich: „44,0 Millionen Wohnungen in Deutschland zum Jahresende 2025“, Gesamtwohnfläche
4,1 Mrd m² (Fortschreibung des Wohngebäude- und Wohnungsbestandes auf Zensus-2022-Basis).
(3) **ImmoWertV, Anlage 4 (zu § 36 Abs. 1) „Normalherstellungskosten 2010“**, URL
`https://www.gesetze-im-internet.de/immowertv_2022/anlage_4.html`, Zugriff 13.09.2026; wörtlich:
die NHK erfassen „die Kostengruppen 300 und 400 der DIN 276, die Umsatzsteuer und die
üblicherweise entstehenden Baunebenkosten (Kostengruppen 730 und 771 der DIN 276)“ und beziehen
sich „auf den im Jahresdurchschnitt bestehenden Kostenstand des Jahres 2010“, angegeben „in Euro
pro Quadratmeter Grundfläche“ (Brutto-Grundfläche). Kostenkennwerte Gebäudeart 1.01 (freistehende
Ein- und Zweifamilienhäuser), Standardstufen 1–5: 600 / 800 / **1.050** / 1.300 / 1.600 €/m² BGF;
Mehrfamilienhäuser bis 6 WE, Standardstufen 3–5: **825** / 985 / 1.190 €/m² BGF. Verwendet wird
Standardstufe 3 (mittlerer Standard) als bundesweiter Bestandsmittelwert. (4) **Statistisches
Bundesamt, Fachserie 17 Reihe 4 „Preisindizes für die Bauwirtschaft“ (Basis 2015 = 100)**, URL
`https://www.destatis.de/DE/Themen/Wirtschaft/Preise/Baupreise-Immobilienpreisindex/Publikationen/Downloads-Bau-und-Immobilienpreisindex/bauwirtschaft-preise-2170400223244.pdf?__blob=publicationFile`,
Zugriff 13.09.2026; Jahresdurchschnitte Neubau konventionell gefertigter Wohngebäude:
2010 = 89,1 · 2015 = 100,0 · 2020 = 114,0 · 2021 = 121,9 · 2022 = 139,4 · 2023 = 149,8.
(5) **Statistisches Bundesamt (2026):** Pressemitteilung Nr. 241 vom 10.07.2026, URL
`https://www.destatis.de/DE/Presse/Pressemitteilungen/2026/07/PD26_241_61261.html`,
Zugriff 13.09.2026; wörtlich: „Die Preise für den Neubau konventionell gefertigter Wohngebäude in
Deutschland sind im Mai 2026 gegenüber Mai 2025 um 5,0 % gestiegen.“; Februar 2026 gegenüber dem
Vorjahresmonat +3,3 %; ferner PM Nr. 011 vom 15.01.2026 für November 2025: +3,2 % gegenüber
November 2024.

**Rechenschritt 1 (§3.9 Abgeleitet) — Indexierung 2010 → 2023:** Faktor = 149,8 ÷ 89,1 = 1,6813.
Ein-/Zweifamilienhaus: 1.050 €₂₀₁₀/m² × 1,6813 = 1.765,4 ⇒ **1.765 €₂₀₂₃/m² BGF**;
Mehrfamilienhaus: 825 €₂₀₁₀/m² × 1,6813 = 1.387,1 ⇒ **1.387 €₂₀₂₃/m² BGF**.

**Rechenschritt 2 (§3.9 Abgeschätzt) — Fortschreibung 2023 → Preisstand 2026 (Befund 12).**
Eine Jahresdurchschnitts-Indexreihe bis 2026 liegt in der geprüften Fachserie nicht vor; die
amtlichen Veränderungsraten sind punktuell veröffentlicht (November 2025 +3,2 %, Februar 2026
+3,3 %, Mai 2026 +5,0 % gegenüber dem jeweiligen Vorjahresmonat). Angesetzt werden drei
Jahresschritte (2024, 2025, 2026) mit je 3,4 % ⇒ 1,034³ = 1,1055 ⇒ **Faktor 1,105**. Bandbreite:
unteres Ende drei Schritte à 2,3 % (1,023³ = 1,071), oberes Ende drei Schritte à 5,0 %
(1,050³ = 1,158) ⇒ **Band 1,07–1,16**. Ergebnis: 1.765 × 1,105 = 1.950,3 ⇒
**1.950 €₂₀₂₆/m² BGF** (Band 1.889–2.047); 1.387 × 1,105 = 1.532,6 ⇒ **1.533 €₂₀₂₆/m² BGF**
(Band 1.484–1.609). **Produkt-Kennzeichnung (Vorgabe P1/P2):** der Fortschreibungsfaktor ist eine
begründete Abschätzung von KAP3, keine Quellenangabe, und wird in der nutzersichtbaren
Parameterliste als solche geführt.

**Rechenschritt 3 (§3.9 Abgeschätzt) — BGF je m² Wohnfläche.** Die amtliche Bestandsstatistik
führt Wohnfläche, die NHK je m² Brutto-Grundfläche; eine bundesweite amtliche BGF-Statistik des
Bestands existiert nicht (**Datenlücke §3.8**). Angesetzt wird BGF/Wohnfläche = **1,30**
(Band 1,25–1,40) — begründet damit, dass Wohnfläche weder Konstruktionsflächen (Außen- und
Innenwände) noch Erschließungs-, Keller- und Nebenflächen enthält, die in der BGF mitzählen.
Ergebnis: 1.533 × 1,30 = 1.992,9 ⇒ **1.993 €₂₀₂₆/m² Wohnfläche** (Mehrfamilienhaus) und
1.950 × 1,30 = 2.535 ⇒ **2.535 €₂₀₂₆/m² Wohnfläche** (Ein-/Zweifamilienhaus).

**Rechenschritt 4 (§3.9 Abgeleitet) — Bestandsprobe und Sensitivität.** 4,1 Mrd m² Wohnfläche ×
1.993 bis 2.535 €₂₀₂₆/m² = 8,17 bis 10,39 ⇒ **8,2 bis 10,4 Bio. €₂₀₂₆** Wiederherstellungswert des
Wohngebäudebestands; je Wohngebäude 4,1 Mrd m² ÷ 19,7 Mio = **208 m² Wohnfläche**. Sensitivität:
±10 % auf den Fortschreibungsfaktor verschieben den Bestandswert um ±0,8 bis 1,0 Bio. €; der
BGF-Faktor 1,25 statt 1,40 verschiebt ihn um −11 %. **Kopplung (§3.9):** die Wertdichte hängt am
Baupreisindex; erscheint die Jahresdurchschnittsreihe bis 2026, wird Rechenschritt 2 durch den
gemessenen Indexstand ersetzt und der Wertsatz neu gerechnet. **Widerspruch (§3.8, benannt statt
geglättet):** die NHK sind Neubau-/Wiederherstellungswerte, die Schadensrechnung K3 kann je nach
Regulierungspraxis auch Zeitwerte ansetzen (Alterswertminderung nach ImmoWertV); beide Lesarten
werden nebeneinander geführt, die Zeitwert-Lesart als Sensitivitätsband. **Modellgrenze:**
Nichtwohngebäude sind im Mengengerüst nicht enthalten — die Mengenbasis ist insoweit eine
Untergrenze (§3.6).

**B5 — 60-S093-01 (Gebäudezustand → Schadensgrad).**
Quellen: (1) **Thieken, A. H.; Olschewski, A.; Kreibich, H.; Kobsch, S.; Merz, B. (2008):**
„Development and evaluation of FLEMOps – a new *F*lood *L*oss *E*stimation *MO*del for the
*p*rivate *s*ector“, in: *Flood Recovery, Innovation and Response I*, WIT Transactions on Ecology
and the Environment, Vol. 118, S. 315–324, WIT Press, Southampton, DOI `10.2495/FRIAR080301`,
URL `https://www.witpress.com/elibrary/wit-transactions-on-ecology-and-the-environment/118/19311`,
Zugriff 13.09.2026 (Volltext gegengelesen). Tab. 1 (S. 317) wörtlich zu den Eingangsgrößen:
Water level „<21 cm, 21-60 cm, 61-100 cm, 101-150 cm, >150 cm“ · Building type „One-family homes,
(semi-)detached houses, multifamily houses“ · Building quality „Low/medium quality, high quality“ ·
Contamination „None, medium, heavy (i.e. oil or multiple) contamination“ · Private precaution
„None, good, very good precaution“. Fig. 1 (S. 318) trägt die Achse „Loss ratio of a building [%]“
über den fünf Wasserstandsklassen und ist mit „poor/average building quality“ und „high building
quality“ beschriftet; abgelesen steigt die Schadensquote von ≈ 3,5 % (< 21 cm) auf ≈ 25 %
(> 150 cm). Tab. 2 (S. 318) wörtlich, Skalierungsfaktoren „Loss at residential buildings“:
C0P0 0,92 · C0P1 0,64 · C0P2 **0,41** · C1P0 1,20 · C1P1 0,86 · C1P2 0,71 · C2P0 **1,58**.
S. 319 wörtlich zur Herkunft der Qualitätsklassen: „the information about the building quality in
INFAS Geodaten (i.e. value of the equipment, windows, doors etc.), which is distinguished in six
classes (from 1 ‚exclusive building quality‘ to 6 ‚very poor quality‘)“. S. 323 wörtlich zur
Übertragbarkeit: „it has to be questioned whether loss models that were derived from data of an
extreme flood such as the 2002 event can be applied to more frequent floods“. Datenbasis:
1697 befragte Haushalte (Fig. 1); Validierung an 379 + 550 + 345 = 1.274 Schadensfällen in Döbeln,
Eilenburg und Grimma (Tab. 4, S. 321). (2) **Elmer, F.; Thieken, A. H.; Pech, I.; Kreibich, H.
(2010):** „Influence of flood frequency on residential building losses“, *Natural Hazards and Earth
System Sciences* 10, S. 2145–2159, DOI `10.5194/nhess-10-2145-2010`,
URL `https://nhess.copernicus.org/articles/10/2145/2010/`, Zugriff 13.09.2026 (Volltext
gegengelesen); S. 2151 wörtlich: „In the basic FLEMOps model, five water level classes, three
building types and two building quality classes are used as input.“
**Datenlücke (§3.8):** eine Zahlentabelle der Schadensquoten je Qualitätsklasse ist in beiden
Quellen nicht publiziert; die Qualitätsachse ist ausschließlich grafisch ausgewiesen. Eine
bautechnische, bundesweite Zustandserhebung des Wohngebäudebestands existiert ebenfalls nicht.
**Widerspruch (§3.8, benannt statt geglättet):** die Beschriftung von Fig. 1 ordnet die **höheren**
Schadensquoten der Klasse „high building quality“ zu; fachlich erwartet würde die umgekehrte
Richtung. Ohne Zahlentabelle ist der Widerspruch aus der Quelle nicht auflösbar; das abgeschätzte
Band wird deshalb **symmetrisch** um 1 geführt und die Richtung nicht gesetzt.
**Rechenschritt (§3.9 Abgeschätzt) — Band der Zustandsachse.** Belegt ist die Spannweite der
gebäude- und bewohnerseitigen Modifikatoren derselben Datenbasis: 0,41 bis 1,58 (Tab. 2, S. 318),
Verhältnis 1,58 ÷ 0,41 = 3,854 ⇒ ln 3,854 = 1,349. Diese Spannweite verteilt sich auf die beiden
dort abgebildeten Achsen Kontamination und Vorsorge; die Gebäudequalität ist in Tab. 1 als dritte,
gleichrangige gebäudeseitige Achse geführt, ohne eigenen Zahlenwert. KAP3 setzt deshalb **gleichen
logarithmischen Anteil je gebäudeseitiger Achse** an: 1,349 ÷ 3 = 0,450 ⇒ Spannweitenfaktor
e^0,450 = 1,568 ≈ **1,57** zwischen den beiden Zustandsklassen. Mittelwertzentriert (§3.2) auf den
Bestandsmix: √1,568 = 1,252 ⇒ **1,25** für die schlechtere, 1 ÷ 1,252 = 0,799 ⇒ **0,80** für die
bessere Klasse, Zentralwert **1,00**. **Sensitivität:** das Band verschiebt den Erwartungsschaden
je Zelle um −20 % bis +25 % und ist damit größer als das Tiefenband aus 60-S074-01 (±12 %);
ein Wechsel der Anteilsannahme auf „halber Anteil“ (0,225) ergäbe 0,89–1,12, auf „voller Anteil“
(1,349) ergäbe 0,52–1,96 — die Gleichverteilungsannahme ist damit die mittlere der drei Lesarten.
**Kopplung (§3.9):** erscheint eine Zahlentabelle der FLEMOps-Qualitätsachse oder eine deutsche
Zustandsstatistik, wird dieser Schritt durch die gemessenen Werte ersetzt und das Band neu
gerechnet. **Produkt-Kennzeichnung (Vorgabe P1/P2):** \(f_{\text{S093}}\) ist eine begründete
Abschätzung von KAP3, keine Quellenangabe, und steht mit dieser Herleitung in der nutzersichtbaren
Parameterliste.

**B6 — 60-S094-01 (Baumaterialien → Schadensgrad).**
Quellen: (1) **Maiwald, H.; Schwarz, J. (2018):** „Vereinheitlichte Schadensbeschreibung und
Risikobewertung von Bauwerken unter extremen Naturgefahren“, *Bautechnik* 95(10), S. 743–753,
Ernst & Sohn, Berlin, DOI `10.1002/bate.201800009`, Sonderdruck-URL
`https://edac.biz/fileadmin/Dokumente/06_Publikationen/Bautechnik_1018_Maiwald_Schwarz.pdf`,
Zugriff 13.09.2026 (Volltext gegengelesen). Tab. 1 (S. 744): ausgewertete Schadensdokumentationen
Hochwasser — Sachsen 2002 (Mulde), 2006 (Elbe), 2010 (Neiße, Spree), 2013 (Mulde) sowie Braunsbach
2015 (Baden-Württemberg), je EDAC-Feldeinsatz mit Schadensdokumentation. Tab. 2 (S. 745)
definiert die Schadensgrade D0–D6; für Hochwasser sind D1–D6 belegt, D0 ist ausdrücklich nicht
belegt. S. 745 wörtlich: „Ein Bauwerk unterliegt also entweder der Einwirkung in unterschiedlicher
Intensität (und weist hier zumindest Durchfeuchtungsschäden im Sinne nicht struktureller Schäden
auf) oder ist nicht von der Einwirkung betroffen. Der Schadensgrad D0 muss hier nicht
berücksichtigt werden, da alle betroffenen Bauwerke mind. dem Schadensgrad D1 zuzuordnen sind.“
S. 745 wörtlich zur Bauform: „Es ist anzumerken, dass die Beschreibungen der Schadensgrade zunächst
für die allgemeine Bebauung vornehmlich in Mauerwerksbauweise gelten. Sie sind aber auch auf andere
Bauweisen anwendbar, wobei spezifische Schadensbilder analog zu EMS-98 in weiterführenden Arbeiten
im Detail noch herauszuarbeiten wären.“ Tab. 4 (S. 747) ordnet den Graden die Schadensbilder zu:
D1 „reiner Durchfeuchtungsschaden“, D2 „leichte Risse in tragenden Wänden“ / „Unterspülung von
Fundamenten“, D3 „Einsturz nicht tragender Wände“, D4 „Einsturz von tragenden Wänden, Decken“,
D5 „Kollaps bzw. Einsturz von größeren Gebäudeteilen“, D6 „Dislokation: Bauwerk vollständig
weggeschwemmt, umgestürzt oder vom Fundament verschoben“. (2) **Thieken u. a. (2008)**, Fundstelle
und Zugriff wie B5: Tab. 1 (S. 317) führt als Eingangsgrößen Wasserstand, Gebäudetyp,
Gebäudequalität, Kontamination und Vorsorge — **kein Baustoffmerkmal**.
**Datenlücke (§3.8):** eine publizierte, nach Baumaterial differenzierte Wassertiefe-Schadensfunktion
für deutsche Wohngebäude wurde nicht gefunden; die materialspezifischen Schadensbilder sind in der
geprüften Quelle ausdrücklich noch nicht ausgearbeitet, und die amtliche Statistik führt kein
bundesweites Baustoffmerkmal des Bestands. Die in `backend/app/data/sources.py` geführte
Hochwasserschutzfibel (BMWSB 2022) ist Kandidat für die bauliche Vorsorge (60-S092-01); sie wurde
für diese Zeile nicht im Volltext geprüft und geht nach §3.8 deshalb nicht in den Wert ein.
**Rechenschritt (§3.9 Abgeschätzt) — Band der Materialachse.** Ausgangspunkt ist der in B5
hergeleitete logarithmische Achsenanteil 0,450. Das Baumaterial ist in **keinem** der beiden
empirischen Modelle eine eigene Achse, obwohl sie auf 1.697 (Thieken u. a. 2008) bzw. 2.158
Schadensfällen (Elmer u. a. 2010) beruhen; hätte es eine mit Zustand, Kontamination oder Vorsorge
vergleichbare Wirkung, wäre es dort als Achse aufgetaucht. KAP3 setzt den Materialbeitrag deshalb
auf den **halben logarithmischen Anteil** der Zustandsachse: 0,450 ÷ 2 = 0,225 ⇒ Spannweitenfaktor
e^0,225 = 1,252; mittelwertzentriert √1,252 = 1,119 ⇒ **1,12** (schadensanfälligere Bauweise) bzw.
1 ÷ 1,119 = 0,894 ⇒ **0,89** (unempfindlichere Bauweise), Zentralwert **1,00**.
**Sensitivität:** allein ±12 % auf den Schadensgrad; multiplikativ mit dem Zustandsband aus B5
(0,80 × 0,89 = 0,712 bis 1,25 × 1,12 = 1,40) spannt die Strukturachse insgesamt **0,71–1,40**.
**Bauform-Grenze als Modellgrenze der Abschätzung (Vorgabe P2):** der Wert ist an
Mauerwerksbauweise kalibriert; für Holz-, Fachwerk- und Leichtbaukonstruktionen sowie für
Lehmmörtel-Mauerwerk ist 1,12 eine Untergrenze, und die Übertragung wird nicht stillschweigend
verallgemeinert. **Kopplung (§3.9):** das Band hängt an B5; ändert sich dort der Achsenanteil,
wird es neu gerechnet. **Produkt-Kennzeichnung (Vorgabe P1/P2):** \(f_{\text{S094}}\) ist eine
begründete Abschätzung von KAP3 und steht mit dieser Herleitung in der nutzersichtbaren
Parameterliste.

## 3 Modell (§2.3)

Umsetzungsgrundlage ist Ansatz **(a)** aus Kap. 9: Szenario-Erwartungswert mit typisierter
Tiefen-Schadensfunktion je 100-m-Zelle. Dieses Kapitel deklariert die native Ergebnisgröße (§3.6),
spezifiziert die dafür benötigten Datenebenen (§3.1) und schreibt die Schicht-B-Kernformel
Menge × Rate × Preis auf Zellebene aus (§3.2), mit einer physischen Zwischengröße vor dem
Euro-Betrag.

### 3.1 Native Ergebnisgröße, Einheit, Bezugsjahr, Betrachtungsebene (§3.6)

**Native Ergebnisgröße (deklariert, genau eine je Risiko-Code):** der **jährliche
Erwartungsschaden des Kontos K3 aus flussseitiger Überflutung**, Zeichen \(\text{EAD}\).

- **Einheit:** Euro je Jahr, im Preisstand des Berichts — **€₂₀₂₆/a**.
- **Bezugsjahr (Preisstand):** **2026**, einheitlich für alle Kostensätze dieses Berichts
  (Kap. 1, „Konto-Einbettung“: Preisstandjahr 2026, §3.9 abgeschätzt, mit Ersetzungspfad). Die
  Wertsätze der Ebene GEBAEUDEWERT sind auf genau diesen Preisstand indexiert (Register
  60-R24-01, Langbeleg B4).
- **Betrachtungsebene:** die **Kommune**; gerechnet wird auf 100-m-Zellen innerhalb der Kommune,
  der deklarierte Ausweis ist die Kommune. Referenz- und Zentrierungsmittel dieses Kapitels stammen
  nach §3.2 entweder aus amtlicher Statistik oder aus der Betrachtungsebene selbst (die Zellen
  derselben Kommune), nie aus einer Aggregation über eine höhere Ebene.
- **Physischer Teil-Ausweis (Zwischengröße vor dem Euro):** die **schadensäquivalente Wohnfläche**
  \(\bar A\) in **m²/a** — diejenige Wohnfläche, deren vollständige Wiederherstellung dem
  erwarteten Schaden der Zelle beziehungsweise der Kommune entspricht. Sie entsteht in der Formel
  vor jedem Euro-Betrag und trägt ihn: \(\text{EAD} = \bar A \cdot w\).
- **Begrenzung des Ausweises (§3.6):** \(\text{EAD}\) ist der bewertete Schaden des Kontos K3 und
  damit eine Untergrenze des Gesamtschadens desselben Ereignisses; K1 (#101), K4 (#74), K5 und K8
  (#50) sind nicht enthalten (Kap. 1, „Nur K3 aktiv“).

### 3.2 Datenebenen nach §3.1

Vier Zellgrößen trägt das Produkt heute nicht. Jede ist hier vollständig spezifiziert — Quelle,
keyless Beschaffungsweg, Zell-Ableitungsregel, Fallback, Normierung/Zentrierung — und entweder
„neu anzulegen“ oder „geparkt (Datenquelle fehlt)“ gekennzeichnet.

| Ebene | §3.1-Status | Quelle / Beschaffungsweg (keyless) | Zell-Ableitungsregel | Fallback | Normierung/Zentrierung |
|---|---|---|---|---|---|
| **HQ_FLAECHE** — überfluteter Flächenanteil \(a_{z,s}\) je Zelle und Szenario | **neu anzulegen** | Hochwassergefahrenkarten der Länder nach § 74 WHG / HWRM-RL; Kartendienste und Downloads der Landesämter sowie der Bund/Länder-Zusammenführung WasserBLIcK (BfG), ohne Schlüssel oder Nutzerkonto abrufbar; Szenariendefinition LAWA 2024 (Register 60-W085-01, Langbeleg B1) | Verschnitt der Überflutungsfläche des Szenarios \(s\) mit der 100-m-Zelle; \(a_{z,s}\) = überflutete Teilfläche / Zellfläche, Werte in [0, 1] | Zelle ohne Kartenabdeckung (Gewässer ohne signifikantes Risiko nach § 73 WHG): \(a_{z,s} = 0\), nachrichtlich als „nicht kartiert“ geführt — kein Neutralwert, sondern der Lackmustest-Fall (§3.1) | keine Zentrierung: \(a_{z,s}\) ist ein Anteil mit physischer Bedeutung, kein Modifikator |
| **HQ_TIEFE** — Wassertiefe \(h_{z,s}\) je Zelle und Szenario | **neu anzulegen** | dieselbe Quelle; die Tiefenklassen 0–0,5 / >0,5–1 / >1–2 / >2–4 / >4 m sind nach LAWA 2024, S. 16 Pflichtbestandteil jeder Karte (B1) | flächengewichtetes Mittel der Tiefenklassen-Mittelwerte über den überfluteten Teil der Zelle; offene oberste Klasse mit ihrer Untergrenze angesetzt (Untergrenze, §3.6) | Zelle mit \(a_{z,s} > 0\), aber ohne Tiefenangabe: Median der Tiefenklasse **derselben Kommune im selben Szenario** (Betrachtungsebene selbst, §3.2); fehlt auch der, die amtlich publizierte Klassenverteilung des Bundeslandes | keine Zentrierung; die Tiefe geht über die Schadensfunktion §3.3 ein |
| **GEBAEUDEWERT** — Wohnfläche \(W_z\), Gebäudetyp-Mix \(\theta_{z,t}\), Wertdichte \(w_z\) | **neu anzulegen** | Zensus 2022, Gebäude- und Wohnungszählung, 100-m-Gitter (offener Download ohne Schlüssel) für Wohnfläche und Gebäudetyp; Wertsätze aus ImmoWertV Anlage 4 (NHK 2010) und Destatis-Baupreisindex, Fortschreibung nach Register 60-R24-01 (B4) | \(W_z\) = Summe der Wohnfläche der Gitterzelle; \(\theta_{z,t}\) = Anteil der Wohnfläche je Gebäudetyp \(t\) (Ein-/Zweifamilien- gegen Mehrfamilienhaus); \(w_z = k_{\text{BGF}} \sum_t \theta_{z,t} n_t\) | Zelle mit Gebäudebestand, aber ohne Typaufteilung: Typ-Mix **der übrigen Zellen derselben Kommune** (§3.2); fehlt auch der, der amtlich publizierte Bestandsmix des Bundeslandes | \(w_z\) ist ein Preis, kein Modifikator — keine Zentrierung; Preisstand 2026 einheitlich |
| **GEBAEUDEZUSTAND_BAUSTOFF** — Zustands- und Materialachse \(f_{S093}\), \(f_{S094}\) | **geparkt (Datenquelle fehlt)** — Beschaffungs-Watchlist | keine bundesweite offene Erhebung von Bauzustand oder Baumaterial je Zelle; Zensus 2022 führt Baujahrsklasse und Gebäudetyp, nicht den Bauzustand und nicht den Baustoff (Register 60-S093-01, 60-S094-01) | entfällt, solange die Ebene geparkt ist | \(f_{S093} = f_{S094} = 1{,}00\) — der Zentrierungs-Neutralwert, dokumentiert und nicht still (§3.1) | mittelwertzentriert auf den Bestandsmix (§3.2); die Bänder 0,80–1,25 und 0,89–1,12 laufen als Struktur-Unsicherheit mit (multiplikativ 0,71–1,40) |

**Beschaffungs-Watchlist zu GEBAEUDEZUSTAND_BAUSTOFF (§3.1).** Beobachtet werden drei Wege, jeder
mit dem Kriterium „zellscharf, bundesweit, keyless“: (1) eine Fortschreibung der Zensus-Gebäude-
und Wohnungszählung um ein Zustands- oder Baustoffmerkmal; (2) die Gebäudemodelle LoD2 der
Landesvermessungen, sofern sie ein Konstruktionsmerkmal führen; (3) Energieausweis- oder
Sanierungsstandsregister mit Gitterausweis. Solange keiner der drei Wege das Kriterium erfüllt,
bleiben beide Faktoren auf exakt 1,00, und ihr Band bleibt der ausgewiesene Unsicherheitsbeitrag.

**Ressourcen-Regel (§3.4).** Keine der vier Ebenen verlangt einen nationalen
100-m-Vollraster-Lauf, und keiner der beschriebenen Schritte plant einen ein: Der Verschnitt nach
HQ_FLAECHE und HQ_TIEFE läuft auf dem Zuschnitt der jeweils berechneten Kommune, der
GEBAEUDEWERT-Aufbau ebenso. Jeder Abgleich dieses Kapitels — insbesondere die Prüfung der
Exponiertenquote gegen das ZÜRS-Band aus Register 60-R17-01 (7,6 % der Adressen in GK2–GK4,
1,5 % im HQ100-nahen Band) — läuft auf **Bundesland-, Gemeindepunkt- oder Stichprobenebene**,
nicht auf dem Vollraster.

**Kein-Doppelkanal (§3.2).** Die Geländehöhe (S074) und die Gewässernähe (R17) stecken bereits in
den Karten der Ebenen HQ_FLAECHE und HQ_TIEFE; sie treten deshalb in der Kernformel **nicht** als
eigene Faktoren auf, sondern nur als Sensitivitätsbänder (±12 % aus dem DGM1-Höhenfehler,
Register 60-S074-01; nationales Prüfband, Register 60-R17-01). Ebenso wirken Bodenbedeckung
(S072) und Versiegelung (S073) ausschließlich über den Hazard-Datensatz.

### 3.3 Tiefen-Schadensfunktion \(d(h)\) — Stützstellen und Herleitung (P1)

Die Schadensfunktion gibt die Schadensquote eines Gebäudes bei der Wassertiefe \(h\) an, also den
Anteil des Wiederherstellungswerts. Belegt sind die beiden **Enden** der FLEMOps-Wasserstandsachse
(Register 60-S093-01, Langbeleg B5, Thieken u. a. 2008): ≈ 3,5 % in der untersten Klasse (< 21 cm)
und ≈ 25 % in der obersten (> 150 cm). Die Werte **zwischen** den Enden und die repräsentativen
Tiefen der Klassen sind in der Quelle nicht als Zahlentabelle publiziert; sie sind deshalb eine
**begründete Abschätzung von KAP3** (§3.9, Vorgabe P1) mit der folgenden, im Berichtstext
ausgeschriebenen Herleitung.

*Herleitung.* Zwischen den beiden belegten Enden wird **log-linear** interpoliert, weil die
publizierte Achse über die Klassen hinweg multiplikativ und nicht additiv wächst:
\(d(h) = d_1 \cdot (d_5/d_1)^{(h - h_1)/(h_5 - h_1)}\) mit \(d_1 = 0{,}035\) bei
\(h_1 = 0{,}10\) m und \(d_5 = 0{,}250\) bei \(h_5 = 1{,}75\) m. Die repräsentativen Tiefen sind
die Klassenmitten; für die oben offene Klasse ist 1,75 m gesetzt (Abschätzung von KAP3, Richtung:
unterschätzt tiefe Überflutungen, damit Untergrenze).

| Klasse (FLEMOps) | < 21 cm | 21–60 cm | 61–100 cm | 101–150 cm | > 150 cm |
|---|---|---|---|---|---|
| repräsentative Tiefe \(h\) [m] | 0,10 | 0,405 | 0,805 | 1,255 | 1,75 |
| Schadensquote \(d(h)\) | **0,035** (belegt, B5) | 0,050 (abgeschätzt) | 0,081 (abgeschätzt) | 0,139 (abgeschätzt) | **0,250** (belegt, B5) |

*Gegenprobe und benannter Widerspruch (§3.8).* Die Interpolation entspricht einem Zuwachs von
**12,7 % je 10 cm** Wassertiefe. Die unabhängige Sensitivitätsrechnung aus Register 60-S074-01
(de Moel & Aerts 2011, Langbeleg B2) misst 5,3–6,2 % je 10 cm. Der Unterschied wird benannt und
nicht geglättet: Die niederländische Zahl gilt für **aggregierte Landnutzungsklassen** über ein
ganzes Untersuchungsgebiet, die deutsche Achse für das **einzelne Wohngebäude** in fünf Klassen.
Als Sensitivitätsband der Schadensfunktion läuft deshalb der flachere Verlauf mit
(untere Bandgrenze: Zuwachs 6 % je 10 cm ab demselben belegten Startwert 0,035, obere Bandgrenze:
die Stützstellen oben), zusätzlich zu den mittelwertzentrierten Achsen \(f_{S093}\) und
\(f_{S094}\) mit ihrem gemeinsamen Band 0,71–1,40.

### 3.4 Kernformel auf Zellebene (Menge × Rate × Preis)

**Schritt 1 — Menge × Rate: geschädigte Wohnfläche je Ereignis (physische Zwischengröße).**
Für die Zelle \(z\) und das Szenario \(s\)

$$ A_{z,s} \;=\; \underbrace{W_z \cdot a_{z,s}}_{\text{Menge: überflutete Wohnfläche } [\text{m}^2]} \;\cdot\; \underbrace{d(h_{z,s}) \cdot f_{S093} \cdot f_{S094}}_{\text{Rate: Schadensquote } [-]} \qquad [\text{m}^2] $$

\(A_{z,s}\) ist die **schadensäquivalente Wohnfläche** der Zelle im Ereignis \(s\): die Wohnfläche,
deren vollständige Wiederherstellung dem Schaden entspricht. Sie ist die physische Zwischengröße
und existiert unabhängig von jedem Preis.

**Schritt 2 — Erwartungswert über die Szenarien (Rate der Zeit).** Die drei Stützstellen der
Hochwassergefahrenkarte (Register 60-W085-01) spannen eine Schaden-Wahrscheinlichkeits-Kurve auf;
der Jahreserwartungswert ist ihre Fläche, trapezförmig integriert, mit konstanter Fortsetzung
oberhalb des Extremszenarios:

$$ \bar A_z \;=\; \sum_{i=1}^{n-1} \bigl(p_i - p_{i+1}\bigr)\cdot\frac{A_{z,i} + A_{z,i+1}}{2} \;+\; p_n \cdot A_{z,n} \qquad [\text{m}^2/\text{a}] $$

mit \(n = 3\) und \(p_1 > p_2 > p_3\): \(p_1 = 1{,}0\cdot10^{-1}\,\text{a}^{-1}\) (HQhäufig,
Kartenfall HQ10), \(p_2 = 1{,}0\cdot10^{-2}\,\text{a}^{-1}\) (HQ100), beide belegt (B1);
\(p_3 = 2{,}236\cdot10^{-3}\,\text{a}^{-1}\) (HQextrem) als **Abschätzung von KAP3** (§3.9).
*Herleitung \(p_3\):* Die Quellen geben für das Extremszenario keine einheitliche Jährlichkeit,
sondern zwei Enden — mindestens 200 a nach § 74 Abs. 2 WHG (\(5{,}0\cdot10^{-3}\)) gegen ≈ 1000 a
in der Länderpraxis (\(1{,}0\cdot10^{-3}\), LfU Bayern). Da beide Enden Größenordnungsenden sind,
ist der Basiswert ihr **geometrisches Mittel**
\(\sqrt{5{,}0\cdot10^{-3}\cdot1{,}0\cdot10^{-3}} = 2{,}236\cdot10^{-3}\,\text{a}^{-1}\)
(\(T \approx 447\) a); das volle Band \(5{,}0\cdot10^{-3}\)…\(1{,}0\cdot10^{-3}\) läuft als
Sensitivität mit und ist je Land durch die tatsächlich kartierte Jährlichkeit ersetzbar
(Ersetzungspfad, W1; Datenlücke in B1). Ereignisse häufiger als \(p_1\) sind nicht kartiert und
tragen deshalb 0 — eine ausgewiesene Untergrenze (§3.6). Der letzte Summand \(p_n A_{z,n}\) setzt
den Schaden oberhalb des Extremszenarios konstant fort; das ist ebenfalls eine Abschätzung von
KAP3, Richtung: unterschätzt den Tail, weil dort die Schadensquote noch steigt.

**Schritt 3 — Preis: Euro-Betrag.** Erst hier entsteht der Euro:

$$ \text{EAD}_z \;=\; \bar A_z \cdot w_z, \qquad w_z \;=\; k_{\text{BGF}} \cdot \sum_t \theta_{z,t}\, n_t \qquad [\text{€}_{2026}/\text{a}] $$

Die Wertsätze \(n_t\) sind belegt und auf den Preisstand 2026 indexiert (Register 60-R24-01, B4):
\(n_{\text{EFH/ZFH}} = 1.950\) €₂₀₂₆/m² BGF (Band 1.889–2.047),
\(n_{\text{MFH}} = 1.533\) €₂₀₂₆/m² BGF (Band 1.484–1.609). Der Umrechnungsfaktor
\(k_{\text{BGF}} = 1{,}30\) m² BGF je m² Wohnfläche (Band 1,25–1,40) ist eine **Abschätzung von
KAP3** (§3.9, Herleitung in Register 60-R24-01: Verhältnis von Brutto-Grundfläche zu Wohnfläche
im Wohnungsbau, Band aus der Spannweite zwischen kompakten Mehrfamilien- und gegliederten
Einfamilienbauten). Der Preis trägt die Zeitwert-Lesart als Band (Alterswertminderung nach
ImmoWertV, B4), nicht als Glättung.

**Lackmustest (§3.1).** Eine Kommune ohne Flussaue erhält in jedem Szenario \(a_{z,s} = 0\) für
alle ihre Zellen, damit \(A_{z,s} = 0\), \(\bar A_z = 0\) und \(\text{EAD}_z = 0\) — ohne
Sonderregel und ohne Rest aus einer höheren Ebene. Kein Summand der Formel stammt aus einer
nationalen Größe, die räumlich verteilt würde.

**Rechenbeispiel (eine Zelle).** Reines Einfamilienhausgebiet in der Aue,
\(W_z = 1.200\) m² Wohnfläche, \(\theta_{\text{EFH/ZFH}} = 1{,}0\) ⇒
\(w_z = 1{,}30 \cdot 1.950 = 2.535\) €₂₀₂₆/m² Wohnfläche. Szenarien: HQhäufig
\(a = 0{,}25\), \(h = 0{,}30\) m ⇒ \(d = 0{,}050\); HQ100 \(a = 0{,}80\), \(h = 0{,}80\) m ⇒
\(d = 0{,}081\); HQextrem \(a = 1{,}00\), \(h = 1{,}60\) m ⇒ \(d = 0{,}250\). Physische
Zwischengrößen: 15,0 / 77,8 / 300,0 m² je Ereignis, daraus \(\bar A_z = 6{,}31\) m²/a und
\(\text{EAD}_z \approx 16.000\) €₂₀₂₆/a.

```python test: beispiel_60_kernformel_zelle
# Schadensfunktion: log-lineare Interpolation zwischen den belegten Enden (B5)
d1, d5, h1, h5 = 0.035, 0.250, 0.10, 1.75
d = lambda h: d1 * (d5 / d1) ** ((h - h1) / (h5 - h1))
assert abs(d(0.405) - 0.0503) < 5e-4 and abs(d(0.805) - 0.0811) < 5e-4
assert abs(d(1.255) - 0.1386) < 5e-4 and abs(d(1.75) - 0.250) < 1e-9
# Zelle: Menge x Rate -> physische Zwischengroesse (m2), erst danach der Preis
W, f093, f094 = 1200.0, 1.00, 1.00
A = [W * a * d_s * f093 * f094 for a, d_s in ((0.25, 0.050), (0.80, 0.081), (1.00, 0.250))]
assert abs(A[0] - 15.0) < 1e-9 and abs(A[2] - 300.0) < 1e-9
# Szenario-Erwartungswert: Trapeze + konstante Fortsetzung oberhalb HQextrem
p3 = (5.0e-3 * 1.0e-3) ** 0.5          # geometrisches Mittel des WHG/Laenderpraxis-Bandes
assert abs(p3 - 2.236e-3) < 1e-6
p = [1.0e-1, 1.0e-2, p3]
A_bar = sum((p[i] - p[i + 1]) * (A[i] + A[i + 1]) / 2 for i in range(2)) + p[2] * A[2]
assert abs(A_bar - 6.311) < 1e-3
# Preis: erst hier entsteht der Euro
w = 1.30 * 1950.0
assert abs(A_bar * w - 16000.0) < 1.0
# Lackmustest: Kommune ohne Flussaue -> exakt 0
A0 = [0.0, 0.0, 0.0]
assert sum((p[i] - p[i + 1]) * (A0[i] + A0[i + 1]) / 2 for i in range(2)) + p[2] * A0[2] == 0.0
```

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

### 5.1.1 Zeichentabelle (Kette S092)

| Zeichen | Name | Einheit | Wert/Herkunft |
|---|---|---|---|
| \(\Delta q\) | zusätzlich nachgerüsteter Anteil exponierter Gebäude (marginal gegenüber heute) | – | 0,10 (Band 0,05–0,20) · herleitung:#s092-wirkung — Abschätzung von KAP3, keine Primärquelle (§5.1.2) |
| \(e_{\text{bem}}\) | Schadensminderung am nachgerüsteten Gebäude, solange der Wasserstand das Bemessungsniveau nicht übersteigt | – | 0,70 (Band 0,50–0,80) · herleitung:#s092-wirkung — Abschätzung von KAP3, keine Primärquelle (§5.1.2) |
| \(r_{\text{S092}}\) | relative Minderung des K3-Erwartungsschadens von #60 durch S092 | – | 0,035 (Band 0,0075–0,112) · berechnet: \(\Delta q \cdot s_{\text{bem}} \cdot e_{\text{bem}}\) (§5.1.2) |
| \(s_{\text{bem}}\) | Anteil der Schadenssumme aus Ereignissen unterhalb des Bemessungsniveaus | – | 0,50 (Band 0,30–0,70) · herleitung:#s092-wirkung — Abschätzung von KAP3, keine Primärquelle (§5.1.2) |

### 5.1.2 Herleitung, Rechnung und Sensitivität

**Herleitung je Faktor** (alle drei Werte sind Abschätzungen von KAP3, keine Primärquelle):

- \(\Delta q\) = 0,10 (0,05–0,20). Annahme: Ein kommunales Förder- und Beratungsprogramm erreicht in
  einem Planungszeitraum jedes zehnte exponierte Gebäude. Untere Bandgrenze: halbe Reichweite.
  Obere: doppelte. Marginal, weil vorhandener Objektschutz bereits im Basisschaden steckt
  (Doppelzählungs-Wächter).
- \(e_{\text{bem}}\) = 0,70 (0,50–0,80). Annahme: Objektschutz (Abdichtung, Rückstausicherung,
  angepasste Nutzung) hält Wasser bis zur Schutzhöhe weitgehend fern. Restschaden durch Feuchte,
  Ausführungsmängel und nicht verschlossene Öffnungen. Obergrenze unter 1, weil kein Objektschutz
  vollständig dicht ist.
- \(s_{\text{bem}}\) = 0,50 (0,30–0,70). Annahme: Schadenssummen verteilen sich auf häufige flache
  und seltene tiefe Überflutungen. Oberhalb der Schutzhöhe wird Objektschutz überströmt und wirkt
  praktisch nicht. Ohne gemessene Tiefenverteilung wird die Mitte gesetzt, Band symmetrisch.

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
Negativ-Beispiel (§2.6/§3.1): Verteilschlüssel
„nationaler Schadenstopf × Anteil“ — ausgeschieden.
-->

**Entscheidungsstand (T-0237).** Die drei verglichenen Ansätze sind benannt, das Raster ist in
jeder Zelle bewertet, und der Ansatz der Umsetzungsgrundlage ist am Ende dieses Kapitels
festgelegt. Die Bewertung ist nach §3.4 **argumentativ und anhand von Stichproben** geführt:
kein Kriterium verlangt als Nachweis einen nationalen 100-m-Vollraster-Lauf; die
Ressourcenverträglichkeit auf Bundesland-, Gemeindepunkt- und Stichprobenebene ist selbst
Kriterium („Aufwand“). Das Ausschreiben des gewählten Ansatzes (Kernformel, Zeichentabelle,
native Ergebnisgröße) ist **nicht** Gegenstand dieses Kapitels, sondern von Kapitel 3.

### Die drei verglichenen Ansätze

- **(a) Szenario-Erwartungswert mit typisierter Tiefen-Schadensfunktion je 100-m-Zelle.**
  EAD = Σ über die drei HQ-Szenarien: p(HQ) × Schadensgrad(Wassertiefe · Gebäudetyp ·
  Gebäudequalität) × Gebäudewert der Zelle. Achsen und Klassen nach FLEMOps-Bauart
  (Register 60-S093-01/60-S094-01), Tiefe und Eintrittswahrscheinlichkeit aus der
  Hochwassergefahrenkarte (60-W085-01), Wertdichte aus Bestand × Normalherstellungskosten
  (60-R24-01). Dies ist der aus der Arbeitsmappe vorgegebene Kandidat (A5, Mon. Z65:
  „HQ-Szenarien × Schadensfunktionen (Wassertiefe-Schaden) × Gebäudewerte“).
- **(b) Szenario-Erwartungswert mit aggregierter Flächenschadensrate je Landnutzungsklasse.**
  EAD = Σ über die drei HQ-Szenarien: p(HQ) × überflutete Siedlungsfläche der Zelle ×
  Schadensrate in €/m² je Landnutzungsklasse, tiefengestuft nach den fünf Tiefenklassen der
  Hochwassergefahrenkarte. Der Gebäudebestand geht nur über die Landnutzungsklasse ein, nicht
  über Typ und Zustand des einzelnen Gebäudes; Bauart der Schadensmodelle in de Moel & Aerts 2011
  (Langbeleg B2).
- **(c) Ingenieurmäßiges Schadensgradmodell am Einzelgebäude.** Je Hausumring wird aus Wassertiefe,
  Fließgeschwindigkeit und Bauweise ein Schadensgrad D0–D6 nach Maiwald & Schwarz 2018
  (Langbeleg B6) bestimmt und anschließend in Wiederherstellungskosten des jeweiligen Gebäudes
  umgerechnet; Aggregation Gebäude → Zelle → Kommune.

### Kriterienraster

| Kriterium | (a) Szenario-Erwartungswert, typisierte Tiefen-Schadensfunktion je Zelle | (b) Szenario-Erwartungswert, aggregierte Flächenschadensrate | (c) Schadensgradmodell D0–D6 am Einzelgebäude |
|---|---|---|---|
| kausale Treue | **hoch** — bildet die drei Wirkungsglieder der Kette einzeln ab (Hazard W085, Exposition S074/R17, Vulnerabilität S093/S094 auf Mengengerüst R24) und entspricht der Ereignislogik A5 (Rechenregeln Z20) | **mittel** — Hazard und Exposition bleiben getrennt, die Vulnerabilität ist jedoch in der Flächenrate mit dem Mengengerüst verschmolzen; S093/S094 haben keinen eigenen Angriffspunkt | **sehr hoch** — modelliert das Schadensbild physisch am Bauwerk; erfasst zusätzlich die Fließgeschwindigkeit, die #60 laut B6 nur in Sturzflut-Lagen braucht (Modellgrenze der Quelle) |
| Kalibrierbarkeit | **hoch** — ein einziger Niveau-Skalar auf den nationalen Anker (§3.4) wirkt multiplikativ auf alle Zellen; die Tiefenachse bleibt als unabhängige Prüfachse „Ereignisregime“ frei | **hoch** — dieselbe Skalar-Kalibrierung möglich, aber die Flächenrate ist selbst schon ein Kalibrierergebnis: Anker und Parameter sind schwer trennbar (Gefahr der Selbstbestätigung, §3.4) | **gering** — Schadensgrade sind Klassen, keine Euro-Größen; die Umrechnung Grad → Kosten ist laut B6 nicht Bestandteil der Quelle und müsste vollständig selbst kalibriert werden |
| lokale Differenzierung | **hoch** — unterscheidet Zellen nach Tiefe, Gebäudetyp-Mix und Wertdichte; der Lackmustest §3.1 (Kommune ohne Flussaue → ~0) ist über die Überflutungsfläche unmittelbar erfüllt | **mittel** — unterscheidet nur nach Tiefe und Landnutzungsklasse; zwei Kommunen mit gleicher Siedlungsfläche im selben Tiefenband erhalten denselben Schaden, unabhängig vom Bestand | **sehr hoch** — Auflösung bis zum einzelnen Bauwerk, allerdings auf einer Merkmalsbasis, die bundesweit nicht vorliegt (siehe Datenverfügbarkeit) |
| Datenverfügbarkeit | **hoch** — alle vier Eingänge sind frei zugänglich und im Register belegt: HWGK-Raster der Länder (60-W085-01), DGM1 (60-S074-01), Zensus-2022-Gitter mit Gebäudetyp und Wohnfläche (60-R24-01), NHK 2010 aus ImmoWertV Anlage 4; die Zustands- und Materialachsen sind als Bänder geführt, nicht als Zelldaten (60-S093-01/60-S094-01) | **hoch** — Landnutzung aus ATKIS/CORINE plus HWGK; die Schadensraten selbst stammen jedoch aus der niederländischen Fallstudie B2 und sind für Deutschland nicht belegt (§3.8 Datenlücke) | **gering** — Bauweise, Fließgeschwindigkeit und Bauzustand je Gebäude sind bundesweit **nicht** erhoben (ausdrückliche Datenlücken in 60-S093-01 und 60-S094-01); es bliebe ein Modell mit gesetzten Merkmalen, das Vorgabe P1 nur über eine Kette von Abschätzungen erfüllte |
| Maßnahmen-Anschluss | **hoch** — der Objektschutz-Hebel S092 greift als Faktor auf den Schadensgrad (§5.1, r_S092), die Schutzsysteme S096–S098 über die R7-Weiche mit #50 am Hazard-Term; beide Angriffspunkte existieren in der Formel bereits | **gering** — Objektschutz wirkt am Gebäude, die Flächenrate kennt kein Gebäude: S092 ließe sich nur als pauschaler Abschlag auf das Gesamtergebnis anhängen, ohne Wirkungsort (§3.5) | **hoch** — feinster Angriffspunkt für Objektschutz denkbar, aber nur nutzbar, wenn die Gebäudemerkmale vorlägen; ohne sie fällt der Hebel auf dieselbe Pauschale zurück wie bei (b) |
| Architektur-Konformität | **hoch** — Schicht-B-Form Menge × Rate × Preis auf Zellebene mit physischer Zwischengröße (überflutete Gebäude, Wassertiefe, Schadensgrad) vor dem Euro; Schicht-A-Index aus denselben Knoten ableitbar | **mittel** — formal Menge × Rate × Preis, aber die physische Zwischengröße vor dem Euro fehlt: die Flächenrate springt von Quadratmetern direkt in Euro | **gering** — Aggregationsebene Einzelgebäude liegt unterhalb der Zellebene des Produkts; es entstünde eine zusätzliche Objektebene samt eigener Fortschreibung |
| Aufwand (Ressourcenverträglichkeit §3.4) — *umgekehrte Skala: gering = günstig, hoch = teuer* | **mittel** — vier Datenebenen, davon zwei neu anzulegen (HQ-Tiefen, GEBAEUDEWERT); Kalibrierung und Abgleich laufen auf Bundesland- und Gemeindepunkt-Stichproben, ein nationaler 100-m-Vollraster-Lauf ist zu keinem Zeitpunkt nötig | **gering** — zwei Datenebenen, Stichprobenprüfung ebenso auf Gemeindepunktebene möglich; der günstigste Ansatz, aber der Aufwandsvorteil beruht auf der weggelassenen Bestandsachse | **hoch** — Objektebene für rund 19,7 Mio Wohngebäude mit Merkmalen, die erst erhoben werden müssten; eine Stichprobenprüfung genügte für die Kalibrierung nicht, weil die Merkmalsverteilung selbst das Ergebnis trägt |

### Umsetzungsgrundlage

**Gewählt ist Ansatz (a)** — Szenario-Erwartungswert mit typisierter Tiefen-Schadensfunktion je
100-m-Zelle. Er ist damit die Umsetzungsgrundlage für Kapitel 3 und zugleich der Prototyp der
Familie **K3/K4-Ereignisschäden** (§2.6), an dem sich #50 und #47 künftig messen.
Das Raster ist dabei in zwei Skalenrichtungen zu lesen: Die sechs Güte-Kriterien (kausale Treue,
Kalibrierbarkeit, lokale Differenzierung, Datenverfügbarkeit, Maßnahmen-Anschluss,
Architektur-Konformität) laufen von „gering“ bis „sehr hoch“, wobei mehr besser ist; das siebte
Kriterium „Aufwand“ läuft umgekehrt — „gering“ ist dort **günstig**, „hoch“ ist teuer. Ein
geringer Aufwand zählt also nicht als Schwäche.

Ausschlaggebend ist, dass (a) als einziger Ansatz in den sechs Güte-Kriterien durchgehend „hoch“
trägt und in keinem von ihnen unter „mittel“ liegt, ohne an einer Stelle auf nicht vorhandene
Daten oder auf einen Vollraster-Lauf angewiesen zu sein. Beim Aufwand ist (a) mit „mittel“ nicht
der günstigste Ansatz — (b) ist billiger —, bleibt aber deutlich unter dem Objektaufwand von (c)
und ist auf Bundesland-, Gemeindepunkt- und Stichprobenebene ressourcenverträglich (§3.4). Der
Aufwandsvorteil von (b) wird damit gesehen und ausdrücklich in Kauf genommen; er wiegt die beiden
folgenden Gründe nicht auf.

Gegen **(b)** sprechen zwei Gründe, die schwerer wiegen als sein Aufwandsvorteil: Erstens hat der
Maßnahmen-Hebel S092 dort keinen Wirkungsort — der bereits nach Vorgabe P2 bezifferte
Objektschutz (§5.1) ließe sich nur als pauschaler Abschlag anhängen, was §3.5 ausdrücklich
verlangt zu vermeiden. Zweitens fehlt die physische Zwischengröße vor dem Euro, und die einzige
belegte Flächenschadensrate stammt aus einer niederländischen Fallstudie (B2), deren
Übertragbarkeit der Bericht bereits als Modellgrenze führt; sie würde hier vom Sensitivitätsband
zum tragenden Basiswert aufsteigen. (b) bleibt als **Ergänzungsmodul** vorgesehen: als grober
Plausibilitätsrahmen für Kommunen, in denen der Zensus-Bestand je Zelle lückenhaft ist.

Gegen **(c)** spricht die Datenlage, nicht die Modellidee: Bauweise und Bauzustand je Gebäude sind
bundesweit nicht erhoben (Datenlücken in 60-S093-01 und 60-S094-01), die Skala ist laut B6
mauerwerksbasiert und an Extremereignissen einschließlich einer Sturzflut kalibriert, und die
Umrechnung Schadensgrad → Euro ist nicht Bestandteil der Quelle. Der Ansatz wäre in der Fläche nur
mit gesetzten Merkmalen zu betreiben und damit eine Scheingenauigkeit unterhalb der Zellebene des
Produkts. Seine Stärke bleibt im Modell erhalten: die Schadensgradskala trägt weiterhin das
Materialband \(f_{\text{S094}}\) = 1,00 (0,89–1,12) in Ansatz (a).

## Entscheidungslog

| Nr | Frage | angewendete Entscheidung | Begründung | Alternative | Auswirkung |
|---|---|---|---|---|---|
| 1 | Welcher W-Knoten trägt #60? | W117 (KWK Z272), mit W085 eine Ebene tief | einziger Bauwesen-Knoten für Gebäudeschäden mit Hochwasser-Eingang; NW Z61 Input 49 = W085; Code-Bestand nutzt dieselben Namenslisten | nur W085 als Kette (dann fehlten S092–S104 und R24, also Vulnerabilität und Mengengerüst) | 32 Knoten in Bilanz und Register |
| 2 | Familie? | neue Familie K3/K4-Ereignisschäden, Kap. 9 angelegt | kein K3-Bericht in `docs/methodik/` | Übernahme der K1-Struktur (#95) — passt nicht zu Ereignislogik A5 | Drei-Ansätze-Vergleich Pflicht |
| 3 | S092 ohne zulässige Effektgröße | P2-Abschätzung r = 0,035 (0,0075–0,112) | Vorgabe P2, §3.5; Querschnittsbefragungen sind keine Maßnahmen-Effektgröße | Wirkung null (unzulässig nach P2) | Maßnahmen-Modul, kein Basiswert |
| 4 | Slug | `gebaeudeschaeden_flusshochwasser` | kurz, eindeutig gegen #59 (Starkregen) und #46 (Küste) | `flusshochwasser` (verwechselbar mit Id 49) | Dateinamen Bericht/Ledger |
| 5 | Welcher Ansatz wird umgesetzt? (Ansatz-Vergleich §2.6/§3.7) | **13.09.2026 (T-0237):** Ansatz **(a)** Szenario-Erwartungswert mit typisierter Tiefen-Schadensfunktion je 100-m-Zelle — p(HQ) × Schadensgrad(Wassertiefe · Gebäudetyp · Gebäudequalität) × Gebäudewert | einziger Ansatz, der in den sechs Güte-Kriterien durchgehend „hoch“ trägt (das siebte Kriterium Aufwand läuft umgekehrt: dort ist „gering“ günstig, (a) liegt mit „mittel“ über (b) und weit unter (c) und ist nach §3.4 ressourcenverträglich): vollständig aus frei zugänglichen, im Register belegten Datenebenen speisbar, Wirkungsort für S092 und die R7-Weiche vorhanden, Schicht-B-Form mit physischer Zwischengröße vor dem Euro, Kalibrierung und Abgleich auf Stichprobenebene ohne nationalen Vollraster-Lauf (§3.4) | (b) aggregierte Flächenschadensrate — kein Wirkungsort für den Maßnahmen-Hebel, tragender Wert nur aus niederländischer Fallstudie (B2); als Ergänzungsmodul vorgesehen. (c) Schadensgradmodell D0–D6 am Einzelgebäude — Bauweise/Bauzustand bundesweit nicht erhoben, Umrechnung Grad → Euro nicht belegt | Umsetzungsgrundlage für Kap. 3 und Prototyp der Familie K3/K4-Ereignisschäden (bindet später #50 und #47); Kopfzeile und Kap. 9 nachgezogen |
