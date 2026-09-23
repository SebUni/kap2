# Methodik-Bericht #60 — Schäden an Gebäuden aufgrund von Flusshochwasser

Status: **in Revision nach Review-Runde 2** (Erstaufschlag 11.09.2026; Review-Runde 1 13.09.2026, Review-Runde 2 17.09.2026; Autor-Revision nach Runde 2 am 17.09.2026, Ledger `reviews/BEFUNDE_60.md`) · Stand 17.09.2026 ·
Instruktionsquelle: `docs/AUFGABE_METHODIK_SCHADENSRECHNUNG.md` (v2) · Umsetzungsgrundlage:
**Ansatz (a) — Szenario-Erwartungswert mit typisierter Tiefen-Schadensfunktion je 100-m-Zelle**
(entschieden im Ansatz-Vergleich Kap. 9; Entscheidungslog Nr. 5) · Familie: **K3/K4-Ereignisschäden — noch kein Prototyp, dieser Bericht ist
der erste Vertreter** (§2.6; Entscheidungslog Nr. 2)

> **Geltungsbereich.** Befüllt sind Kap. 1 (Wirkungskette, Knoten-Bilanz, Weitergaben, Konto) und
> Kap. 2 (Evidenz-Register) aus den beiden Arbeitsmappen unter `docs/Schadensbaum/` und aus
> volltextgeprüfter externer Evidenz (Langbelege B1–B6 unter der Registertabelle); befüllt ist
> zudem Kap. 9 (Ansatz-Vergleich, entschieden mit T-0237), Kap. 3 vollständig (3.1–3.7: native
> Ergebnisgröße, Datenebenen, Tiefen-Schadensfunktion, Kernformel, Zeichentabelle, Aggregation,
> Schicht-A-Index), Kap. 4 (Kalibrierung; der Niveau-Skalar \(\lambda\) ist **vorläufig**, siehe
> Einleitung Kap. 4), Kap. 5 (Hebel S092), Kap. 6 (Modellgrenzen), Kap. 7 (Parameter-Blöcke aller
> rechnenden Parameter) und Kap. 8 (Quellen). Die Formelstelle FS-Schutzsystem (R7-Weiche mit #50)
> ist inaktiv geparkt (§3.4). Die Knoten-Bilanz in Kap. 1 ist entschieden (32/32 Zeilen
> tragen eine Formelstelle oder `inaktiv` mit Zitat). Im Evidenz-Register sind **sieben** der
> 32 Zeilen belegt beziehungsweise entschieden: **60-W085-01** (Basiswert, Hazard),
> **60-R24-01** (Basiswert, Mengengerüst), **60-S074-01** und **60-R17-01**
> (Sensitivitätsbänder der Exposition), **60-S093-01** und **60-S094-01** (Sensitivitätsbänder
> des Schadensgrads, abgeschätzt) sowie **60-S092-01** (Maßnahmen-Hebel, abgeschätzt; Herleitung
> §5.1, `#s092-wirkung`). Die **übrigen 25 Registerzeilen sind entschieden „bewusst inaktiv“** (Befund 49, T-0580) — mit derselben Begründung samt Zitat wie in der Knoten-Bilanz; S096–S098 und S104 davon als geparkt. Entschieden sind
> der Ansatz (Kap. 9, Ansatz (a)), die native Ergebnisgröße (Kap. 3.1) und die vier Datenebenen
> nach §3.1 (Kap. 3.2). Jeder als
> **Abschätzung von KAP3** geführte Wert ist in seiner Registerzeile als solcher gekennzeichnet
> (§3.9; Vorgaben P1/P2), samt Bandbreite, Sensitivität und Modellgrenze.
> Befund-Ledger: `reviews/BEFUNDE_60.md`.

## Ergebnis

- **Slug:** `60_gebaeudeschaeden_flusshochwasser`. **Registerzeilen:** 32 (`60-<Knoten>-01`), gespiegelt in `docs/evidenz/register.md`. Davon **7 belegt bzw. entschieden** — 60-W085-01, 60-R24-01, 60-S074-01, 60-R17-01, 60-S093-01, 60-S094-01 und 60-S092-01 (Maßnahmen-Hebel, abgeschätzt) —, die **übrigen 25 sind „bewusst inaktiv“** mit Begründung und Zitat aus der Knoten-Bilanz (Befund 49, T-0580; S096–S098 und S104 geparkt).
- **Entschieden (T-0237):** Ansatz-Vergleich Kap. 9 — Umsetzungsgrundlage ist Ansatz **(a)** (Szenario-Erwartungswert mit typisierter Tiefen-Schadensfunktion je 100-m-Zelle); (b) aggregierte Flächenschadensrate bleibt als Ergänzungsmodul, (c) Schadensgradmodell am Einzelgebäude ist ausgeschieden.
- **Entschieden (T-0238):** Kap. 3 bis zur Kernformel — native Ergebnisgröße (EAD in €₂₀₂₆/a, Ebene Kommune), vier Datenebenen nach §3.1 (drei „neu anzulegen", eine „geparkt"), Tiefen-Schadensfunktion und Schicht-B-Kernformel Menge × Rate × Preis je 100-m-Zelle.
- **Offen (Stand 17.09.2026, nach Review-Runde 2):** (1) \(M_0\) = 1,243 Mrd. €₂₀₂₆/a und \(\lambda\) = 0,911 (Werte nachgezogen 23.09.2026 auf §4.3/§4.4, die dort allein gepflegt werden) sind aus dem Stichprobenlauf des Produktionsmodells auf den acht Anker-Kommunen gerechnet (Kap. 4); die out-of-sample-Verteilungsprüfung (Jahresauslassung, §4.5) und der Fit über die Jahresreihe (§4.1a) sind seither nachgezogen (Ledger-Befunde 33 und 34); \(\lambda\) bleibt vorläufig, weil die Verteilungsprüfung als Modellentscheid **nicht bestanden** ausgewiesen ist (§4.5) und die Befunde 35 und 36 offen sind; (2) R7-Weiche mit #50 (FS-Schutzsystem, geparkt); (3) R9-Partitionen zum verbliebenen Rest #92/#102/Id 55 (W091) — #37 und #12 sind entschieden, vgl. Kap. 1 Weitergaben; (4) die 25 noch nicht belegten Registerzeilen aus Kap. 2.
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
auf den Container). **Divergenz Bericht ↔ Code (Befund 13, eiserne Regel 5).** Der Code-Bestand
(`backend/app/data/catalog.py`, Eintrag `kwra_id: 60`) trägt **nicht** genau die Namenslisten von
W117, sondern nur eine **Teilmenge mit abweichender Namensquelle**: nachgerechnet führt der Eintrag
fünf statt sieben Sensitivitäten (`sensitivity_names`) und fünf statt acht Wirkungs-Eingänge
(`upstream_names`) gegenüber den 7 Sensitivitäten bzw. 8 Wirkungs-Eingängen, die die Knoten-Bilanz
unten aus W117 (KWK Z272) zieht; die vorhandenen Einträge sind zudem teils umformuliert statt
wörtlich aus der Arbeitsmappe übernommen. Der Umschnitt geht vom selben Knoten aus, die Namenslisten
selbst sind aber nicht deckungsgleich. Diese Divergenz wird hier **nicht** im Code gefixt, sondern
als Integrationspunkt für `/integriere-risiko 60` geführt (Entscheidungslog Nr. 6).

### Knoten-Bilanz

**Entscheidungsstand (T-0235).** Spalte „rechnet in” trägt ab dieser Fassung je Zeile entweder eine
der sechs benannten **Formelstellen**, an die Kapitel 3 die Größe künftig bindet, oder den Wert
`inaktiv` mit einem wörtlichen Zitat aus `KWRA-Monetarisierung.xlsx` (Blatt und Zelle). Die
Formelstellen sind **Namen, keine Formeln**: Kapitel 3 ist inzwischen ausgeschrieben (§3.1–§3.7);
jede Zeile unten rechnet dort an einer Formelstelle, wirkt als Sensitivitätsband über eine andere
Formelstelle oder ist ausdrücklich inaktiv geführt. Benannte Formelstellen: **FS-Hazard**
(Eintrittswahrscheinlichkeit p(HQ) inkl. der Kein-Doppelkanal-Zuflüsse; die Wassertiefe am Gebäude
kommt allein aus der HWGK-Tiefe, 60-W085-01), **FS-Schadensgrad** (Wassertiefe-Schadensfunktion nach
Bauart/Zustand), **FS-Mengengerüst** (Gebäudewerte/Bestand), **FS-Schutzsystem** (R7-Erwartungswert-Weiche mit #50 — **in dieser Fassung inaktiv, geparkt**: die Kernformel trägt den Term noch nicht, §3.4),
**FS-Bestandsdynamik** (Kap. 6, Szenario-Dynamik des Bestands — **in dieser Fassung inaktiv,
geparkt**: Registerzeile 60-S104-01 ist bewusst inaktiv (geparkt), der Bestand R24 wird für das Szenariojahr konstant
gehalten, Kap. 6 Modellgrenzen) und **FS-Vorsorge** (Maßnahmen-Hebel S092, bereits in §5.1
beziffert). Die frühere siebte Formelstelle FS-Exposition (Wassertiefe am Gebäude) ist
**aufgehoben**: Kapitel 3 kennt sie nicht, und Geländehöhe (S074) und Gewässernähe (R17) wirken nach
dem Kein-Doppelkanal-Grundsatz (§3.2) nur als Sensitivitätsband über FS-Hazard, nicht als eigener
Faktor; keine Zeile der Bilanz bindet mehr an sie. Die Spalte „Name” führt den Wortlaut der
Arbeitsmappe (Blatt „Klimawirkungsketten”, Spalte B der genannten Zeile) **ungekürzt**; nur der
Klammerzusatz am Ende („über W085”, „= Id …”, „direkt …”) ist ein Zusatz dieses Berichts. Die
Spalte „Vorschlag” bleibt unverändert als Beleg aus der Arbeitsmappe stehen; sie ist weiterhin keine
eigene Entscheidung.

| Knoten | Name | Blatt/Zeile | rechnet in | Vorschlag laut Arbeitsmappe |
|---|---|---|---|---|
| W085 | Hochwasser (= Id 49) | KWK Z208; NW Z50 | **FS-Hazard** — Hazard-Term p(HQ); alleiniger Input der Bilanz (NW Z61) | Hazard des Endpunkts (einzige Input-Kante, NW Z61); Id 49 selbst „Rein vorgelagert (0 €)”, R2 — Bewertung „HQ-Szenarien × Schadensfunktionen (Wassertiefe-Schaden) × Gebäudewerte” (Mon. Z65) |
| E12 | Schneeschmelze (über W085) | KWK Z13 | **FS-Hazard** (enthalten, kein eigener Faktor — Kein-Doppelkanal §3.2) | wirkt nur über W085 (Kein-Doppelkanal §3.2): Szenario-Verschiebung des Hazards, kein eigener Faktor |
| E07 | Nässe (über W085) | KWK Z8 | **FS-Hazard** (enthalten, kein eigener Faktor — Kein-Doppelkanal §3.2) | wie E12 |
| E08 | Starkregen (direkt auf W117 und über W085) | KWK Z9 | **FS-Hazard** (Anteil über W085, kein eigener Faktor); direkter Kanal **inaktiv** — R9 (Rechenregeln Z11): „Innerhalb eines Kontos zählt jede Einheit (…Gebäude) genau einmal; verschiedene Konten desselben Ereignisses sind additiv.” i. V. m. Mon. Z64 (Nicht enthalten): „Flusshochwasserschäden (ID 60)” (#59 bucht den direkten Starkregen-Gebäudeschaden) | über W085 wie E12; direkter Gebäudeschaden durch Starkregen gehört zu #59 (Mon. Z64 „Sachschäden durch Starkregen/Rückstau”) — R9 |
| S072 | Boden-/Vegetationsbedeckung (über W085) | KWK Z197 | **FS-Hazard** (enthalten im Hazard-Datensatz, kein eigener Faktor — Kein-Doppelkanal §3.2) | wirkt auf Abflussbildung in W085; bewusst inaktiv, falls der Hazard-Datensatz den Abfluss schon enthält (Kein-Doppelkanal) |
| S073 | Flächenversiegelung (über W085) | KWK Z198 | **FS-Hazard** (enthalten im Hazard-Datensatz, kein eigener Faktor — Kein-Doppelkanal §3.2) | wie S072 |
| S074 | Topographie (Geländeform, Höhe, etc.) (über W085) | KWK Z199 | **Sensitivitätsband** (Kein-Doppelkanal §3.2; Register 60-S074-01/60-R17-01) — wirkt über FS-Hazard (Wassertiefe der Gefahrenkarte), keine eigene Formelstelle; früher: FS-Exposition — Geländehöhe → Wassertiefe am Gebäude | Kandidat für die Zell-Exposition (Geländehöhe → Wassertiefe); Doppelkanal prüfen, falls HQ-Karten Wassertiefen bereits führen |
| R17 | Vorkommen von Oberflächengewässer und Grundwasser (über W085) | KWK Z204 | **Sensitivitätsband** (Kein-Doppelkanal §3.2; Register 60-S074-01/60-R17-01) — wirkt über FS-Hazard (Wassertiefe der Gefahrenkarte), keine eigene Formelstelle; früher: FS-Exposition — Lackmustest §3.1: keine Flussaue → ~0 | Kandidat Exposition; Lackmustest §3.1: keine Flussaue → ~0 |
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
| W100 | Einschränkungen der Funktionsfähigkeit von Kanalnetzen und Vorflutern (= Id 52) | KWK Z223 | **inaktiv** — Mon. Z57 (Id 52, Spalte „Schadenskonto”): „K4”; Spalte „Nicht enthalten”: „Gebäudeschäden durch Rückstau (ID 59).” | Id 52 bucht K4 (NW Z53) — voraussichtlich bewusst inaktiv |
| S092 | Bauliche, organisatorische und finanzielle Vorsorge der Eigentümer und Nutzer von Gebäuden und Infrastrukturen | KWK Z256 | **FS-Vorsorge** — Maßnahmen-Hebel, bereits beziffert (§5.1: r_S092 = 0,035, Band 0,0075–0,0832, §3.9 Abgeschätzt) | Kandidat **Maßnahmen-Hebel** (Objektschutz); P2-Abschätzung §5.1 |
| S093 | Zustand von Gebäuden und Infrastrukturen | KWK Z257 | **FS-Schadensgrad** — Vulnerabilität der Wassertiefe-Schadensfunktion (Mon. Z65) | Kandidat Vulnerabilität der Schadensfunktion; Evidenz und Zellgröße offen |
| S094 | Verwendete Baumaterialien auf Gebäudeebene | KWK Z258 | **FS-Schadensgrad** — wie S093 | wie S093 |
| S096 | Bauliche, organisatorische und finanzielle Vorsorge der öffentlichen Hand | KWK Z260 | **inaktiv (geparkt: Formelstelle FS-Schutzsystem ohne Term in §3.4, Modul #50 fehlt)** — Ziel: R7-Erwartungswert-Weiche mit #50 (Mon. Z65 Spalte „Regeln”: „R7, R9”; Rechenregeln Z9 R7) | Schutzsysteme über R7-Weiche mit #50 (Mon. Z65 „Schutzkosten (ID 50, R7)”; Z55) |
| S097 | Zustand von (Schutz-)Infrastrukturen | KWK Z261 | **inaktiv (geparkt: Formelstelle FS-Schutzsystem ohne Term in §3.4, Modul #50 fehlt)** — Ziel: wie S096 (Versagensfall, Erwartungswert R7) | wie S096 (Versagensfall, Erwartungswert R7) |
| S098 | Verwendete Baumaterialien von (Schutz-)Infrastrukturen | KWK Z262 | **inaktiv (geparkt: Formelstelle FS-Schutzsystem ohne Term in §3.4, Modul #50 fehlt)** — Ziel: wie S096 | wie S096 |
| S104 | Investitionen der Bau- und Immobilienwirtschaft in exponierten Gebieten | KWK Z268 | **inaktiv (geparkt: Formelstelle FS-Bestandsdynamik ohne Term, Registerzeile 60-S104-01 bewusst inaktiv)** — Kap. 6 (Modellgrenzen, „Bestandsdynamik S104”): Investitionen in exponierten Gebieten fließen „im heutigen Modellstand **nicht** als eigener Pfad ein”, der Gebäudebestand R24 wird für das Szenariojahr konstant gehalten; Ziel: Szenario-Dynamik des Gebäudebestands, sobald 60-S104-01 eine rechnende Entscheidung trägt | Kandidat Szenario-Dynamik des Gebäudebestands (Kap. 6) |
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
  Schadensfunktionen × Bestandswerte“. **Entschieden (17.09.2026):** Kostensatz-Typ ist der Neuwert
  (Wiederherstellungskosten); der Zeitwertansatz aus Mon. J64 wird als Band geführt und die
  Abweichung als Antrag auf Fortschreibung in §7.2 ausgewiesen.
- **Bewertungsbaustein:** K3-Wiederherstellung (NW Z61). Bewertungsansatz (Mon. Z65): „Wie ID 59,
  ereignisbezogen flussseitig; HQ-Szenarien × Schadensfunktionen (Wassertiefe-Schaden) ×
  Gebäudewerte.” Gegenstand: „Sachschäden flussseitiger Überflutung.”
- **Preisstandjahr (abgeleitet aus Register 60-R24-01):** 2026. Herleitung: Keine der beiden
  Arbeitsmappen beziffert für K3-Wiederherstellungskosten ein Preisstandjahr (anders als K1/VOLY,
  Konten Z11: „Preisstand 2024”); Rechenregeln Z19 (A4) verlangt: „Konkrete Zahlen sind vor
  Produktivsetzung zu belegen.” Der K3-eigene Kostensatz mit Quelle liegt vor: Register 60-R24-01
  (NHK 2010 nach ImmoWertV Anlage 4, mit dem amtlichen Baupreisindex fortgeschrieben, Langbeleg B4)
  trägt die Wertsätze \(n_t\) = 1.950 / 1.533 €₂₀₂₆/m² BGF (§3.5) und damit den Basiswert
  527.280 €₂₀₂₆ je Wohngebäude (§4.3). Das Preisstandjahr 2026 ist deshalb der Preisstand dieser
  belegten und indexierten Wertsätze, kein frei gesetztes Erstellungsjahr mehr; der frühere
  Ersetzungspfad (W1) ist mit dem Register eingelöst. **Abschätzung von KAP3 (§3.9 ABGESCHÄTZT)**
  ist daran allein der Fortschreibungsfaktor 2023 → 2026 (1,105; Band 1,07–1,16; Langbeleg B4,
  Rechenschritt 2) — nur er wird im Produkt als Abschätzung ausgewiesen (Eiserne Regel 3, P1).
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
gespiegelt. Die 25 Zeilen ohne Rechenpfad tragen die Entscheidung **bewusst inaktiv** (§2.2 (d)) mit derselben Begründung und demselben Zitat wie ihr Knoten in der Knoten-Bilanz (Kap. 1); ihre Evidenzspalten stehen auf „entfällt — kein Rechenpfad“ (Befund 49). Wiederverwendbare Zeilen fanden sich dort nicht (Register führt bisher nur K1-Zeilen
aus #95/#96/#98). In Formeln (§3) dürfen später nur Zeilen mit Entscheidung **Basiswert** stehen.
Zwei Fälle sind davon ausdrücklich erfasst (Befund 55): (1) Ein Zeichen einer Zeile mit Entscheidung
**Sensitivitätsband** darf als **neutral gesetztes Glied** (Wert 1,00) in der Formel stehen;
es verschiebt den Basiswert nicht und trägt nur das Band — so \(f_{\text{S093}}\) und
\(f_{\text{S094}}\) in der Kernformel §3.4. (2) Die belegten Enden \(d_1\), \(d_5\) der
Wasserstandsachse von FLEMOps (Langbeleg B5) sind Basiswert und in §3.3 hergeleitet; die Zeile
60-S093-01 nennt dieselbe Quelle, ihre Entscheidung „Sensitivitätsband“ gilt nur der Zustandsachse.

| Register-ID | Knoten → Outcome | Effektgröße | Studientyp | Quelle | Übertragbarkeit | Datenlage je Zelle | Entscheidung |
|---|---|---|---|---|---|---|---|
| 60-W085-01 | W085 Hochwasser → Überflutungswahrscheinlichkeit/-tiefe am Gebäude | p(HQ) je Pflicht-Szenario der Hochwassergefahrenkarte: HQhäufig 1,0·10⁻¹ a⁻¹ (Kartenfall HQ10; Spanne HQ5–HQ20 = 2,0·10⁻¹ bis 5,0·10⁻² a⁻¹), HQ100 1,0·10⁻² a⁻¹, HQextrem 5,0·10⁻³ bis 1,0·10⁻³ a⁻¹ (WHG-Mindestvorgabe 200 a gegen Länderpraxis ≈ HQ1000); **Zentralwert HQextrem \(p_3\) = 2,236·10⁻³ a⁻¹** (T ≈ 447 a; §3.9 Abgeschätzt, geometrisches Mittel der Bandenden, Herleitung §3.4 Schritt 2 und B1) — mit ihm rechnet die Kernformel, die beiden Bandenden laufen als Sensitivität mit; je Szenario liefert die Karte flächendeckend die Wassertiefe in den Klassen 0–0,5 / >0,5–1 / >1–2 / >2–4 / >4 m | amtliche Kartengrundlage nach HWRM-RL (Pegel- bzw. Regionalisierungsstatistik plus hydrodynamische Berechnung) auf rechtlich normierter Szenariendefinition | LAWA 2024, „Empfehlungen zur Aufstellung von Hochwassergefahrenkarten und Hochwasserrisikokarten“, S. 4 und 16, https://www.lawa.de/documents/2024-01-lawa-empfehlungen-aufstellung-hochwassergefahrenkarten-barrierefrei_1739980622.pdf, Zugriff 13.09.2026; § 74 Abs. 2/3 WHG, https://www.gesetze-im-internet.de/whg_2009/__74.html, Zugriff 13.09.2026; LfU Bayern, „FAQ: Hochwassergefahren- und -risikokarten“, https://www.lfu.bayern.de/wasser/hw_risikomanagement_umsetzung/faq_karten/index.htm, Zugriff 13.09.2026 — Volltext geprüft; Langbeleg **B1** unter der Tabelle | DE-weit für die Risikogebiete nach § 73 WHG, da die Szenarien bundeseinheitlich normiert sind; **Modellgrenze:** außerhalb der kartierten Risikogebiete trifft die Karte keine Aussage, und das Wiederkehrintervall des Extremszenarios ist bundesweit uneinheitlich (mindestens 200 a nach WHG gegen ≈ 1000 a in der Länderpraxis) — als Band geführt, nicht geglättet; für die Kernformel wird das Band des Extremszenarios bewusst zum Zentralwert \(p_3\) = 2,236·10⁻³ a⁻¹ zusammengezogen (geometrisches Mittel, Abschätzung von KAP3, §3.4 Schritt 2), weil eine einheitliche Jährlichkeit je Land fehlt; je Land ist \(p_3\) durch die tatsächlich kartierte Jährlichkeit ersetzbar | HWGK-Raster der Länder über den BfG-Kartendienst WasserBLIcK; Abgleich nach §3.4 auf Bundesland- und Gemeindepunkt-Stichproben, kein Vollraster-Lauf | **Basiswert** — FS-Hazard: die drei Szenario-Stützstellen p(HQ) samt zugehöriger Wassertiefe, für HQextrem mit dem Zentralwert \(p_3\) = 2,236·10⁻³ a⁻¹ (Abschätzung von KAP3, §3.4 Schritt 2); die Spannen von HQhäufig und HQextrem laufen als Sensitivitätsband mit |
| 60-E12-01 | E12 Schneeschmelze → W085 | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | **bewusst inaktiv (im Hazard-Datensatz enthalten, Kein-Doppelkanal §3.2)** — wirkt allein über W085 an FS-Hazard (HWGK-Szenarien p(HQ) samt Wassertiefe, Registerzeile 60-W085-01) und erhält keinen eigenen Faktor; Kap. 1 Knoten-Bilanz: „FS-Hazard (enthalten, kein eigener Faktor — Kein-Doppelkanal §3.2)” |
| 60-E07-01 | E07 Nässe → W085 | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | **bewusst inaktiv (im Hazard-Datensatz enthalten, Kein-Doppelkanal §3.2)** — wirkt allein über W085 an FS-Hazard (HWGK-Szenarien p(HQ) samt Wassertiefe, Registerzeile 60-W085-01) und erhält keinen eigenen Faktor; Kap. 1 Knoten-Bilanz: „FS-Hazard (enthalten, kein eigener Faktor — Kein-Doppelkanal §3.2)” |
| 60-E08-01 | E08 Starkregen → W085 / Gebäudeschaden | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | **bewusst inaktiv** — Anteil über W085 im Hazard-Datensatz enthalten (FS-Hazard, Kein-Doppelkanal §3.2); direkter Kanal auf den Gebäudeschaden: R9 (Rechenregeln Z11): „Innerhalb eines Kontos zählt jede Einheit (…Gebäude) genau einmal”; „verschiedene Konten desselben Ereignisses sind additiv.” i. V. m. Mon. Z64 (Nicht enthalten): „Flusshochwasserschäden (ID 60)” — der direkte Starkregen-Gebäudeschaden wird unter #59 gebucht |
| 60-S072-01 | S072 Boden-/Vegetationsbedeckung → Abfluss (W085) | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | **bewusst inaktiv (im Hazard-Datensatz enthalten, Kein-Doppelkanal §3.2)** — wirkt auf die Abflussbildung, die die HWGK-Wassertiefe bereits enthält, also allein über W085 an FS-Hazard (HWGK-Szenarien p(HQ) samt Wassertiefe, Registerzeile 60-W085-01) und erhält keinen eigenen Faktor; Kap. 1 Knoten-Bilanz: „FS-Hazard (enthalten, kein eigener Faktor — Kein-Doppelkanal §3.2)” |
| 60-S073-01 | S073 Flächenversiegelung → Abfluss (W085) | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | **bewusst inaktiv (im Hazard-Datensatz enthalten, Kein-Doppelkanal §3.2)** — wirkt auf die Abflussbildung, die die HWGK-Wassertiefe bereits enthält, also allein über W085 an FS-Hazard (HWGK-Szenarien p(HQ) samt Wassertiefe, Registerzeile 60-W085-01) und erhält keinen eigenen Faktor; Kap. 1 Knoten-Bilanz: „FS-Hazard (enthalten, kein eigener Faktor — Kein-Doppelkanal §3.2)” |
| 60-S074-01 | S074 Topographie → Wassertiefe am Gebäude | h(Gebäude) = max(0; Wasserspiegellage − Geländehöhe DGM1); der Höhenfehler des DGM1 (σ_z = 0,15–0,20 m) schlägt 1:1 auf die Wassertiefe durch; Schadenswirkung der Wassertiefe: 5,3–6,2 % Schadensänderung je 10 cm (Mittel ≈ 6 %/10 cm) ⇒ σ_z = 0,20 m entspricht ±10,6 bis ±12,4 % Schaden; ±0,5 m ⇒ Faktor 1,35–1,44; ein Faktor 2 erfordert 0,95–1,1 m | amtliche Produktspezifikation eines Geobasisdatensatzes (Airborne Laserscanning) plus publizierte Unsicherheits- und Sensitivitätsrechnung eines Hochwasserschadensmodells (systematische Variation der Überflutungstiefe) | LAIV MV (Landesamt für innere Verwaltung Mecklenburg-Vorpommern), „Geländemodelle“ (Höhengenauigkeit DGM1 0,15–0,2 m), https://www.laiv-mv.de/Geoinformation/Geobasisdaten/Gelaendemodelle/, Zugriff 13.09.2026; de Moel, H. & Aerts, J. C. J. H. 2011, „Effect of uncertainty in land use, damage models and inundation depth on flood damage estimates“, Natural Hazards 58(1), 407–425, DOI 10.1007/s11069-010-9675-6, Zugriff 13.09.2026 — Volltext geprüft (Tab. 4, S. 421; Abschn. 4.3, S. 420); Langbeleg **B2** unter der Tabelle | DGM1 flächendeckend in DE verfügbar; die Tiefen-Sensitivität stammt aus einer niederländischen Fallstudie (Rheindelta, flaches Relief, Landnutzungs-Schadensmodelle). **Modellgrenze:** der Wert gilt für aggregierte Landnutzungsklassen, nicht für das Einzelgebäude, und ist in Mittelgebirgs- und Steillagen eine Untergrenze, weil dort derselbe Höhenfehler größere Tiefenfehler erzeugt | DGM1 (1 m Rasterweite) der Landesvermessungen; Prüfung nach §3.4 auf Gemeindepunkt-Stichproben, kein Vollraster-Lauf | **Sensitivitätsband** — Kein-Doppelkanal §3.2: die Geländehöhe wirkt bereits über die HWGK-Wassertiefe der Zeile 60-W085-01 und geht deshalb nicht als eigener Faktor in FS-Exposition ein; ihr eigener Beitrag ist das Tiefen-Unsicherheitsband ±0,20 m ⇒ ±12 % um den Basiswert |
| 60-R17-01 | R17 Oberflächengewässer → Exposition | Exponiertenquote der Adressen am Gewässernetz (ZÜRS Geo, Stand 2025; Bezugsgröße 22,6 Mio bundesweit bewertete Adressen): GK1 92,4 % (≈ 20,88 Mio) „statistisch nach gegenwärtiger Datenlage nicht von Hochwasser größerer Gewässer betroffen“, GK2 6,1 % (≈ 1,38 Mio; seltener als HQ100, einschließlich deichgeschützter Objekte), GK3 1,1 % (≈ 249.000; HQ10–HQ100), GK4 0,4 % (≈ 90.400; „Hochwasser statistisch mindestens einmal in 10 Jahren“) ⇒ exponiert GK2–GK4 = 7,6 % ≈ 1,72 Mio Adressen, flussnah im HQ100-Band GK3+GK4 = 1,5 % ≈ 339.000 Adressen | Bestandsstatistik (adressscharfe Vollzonierung des versicherten Bestands auf Basis der wasserwirtschaftlichen Länderdaten) — keine Studie | GDV (Gesamtverband der Deutschen Versicherer) 2025, „Geringe Gefahr für Fluss-Hochwasser bei den meisten Wohngebäuden“, Datenservice zum Naturgefahrenreport, Stand ZÜRS Geo 2025, https://www.gdv.de/gdv/statistik/datenservice-zum-naturgefahrenreport/sachversicherung-elementar/geringe-gefahr-fuer-fluss-hochwasser-bei-den-meisten-wohngebaeuden--147672, Zugriff 13.09.2026; GDV, „ZÜRS Geo — Zonierungssystem für Überschwemmungsrisiko und Einschätzung von Umweltrisiken“, https://www.gdv.de/gdv/themen/klima/-zuers-geo-zonierungssystem-fuer-ueberschwemmungsrisiko-und-einschaetzung-von-umweltrisiken-11656, Zugriff 13.09.2026 — Volltext geprüft (GK1 92,4 %, GK4 0,4 %, 22,6 Mio Adressen wörtlich; GK2/GK3-Aufteilung aus der GDV-Klassengrafik, Residualprobe unten); Langbeleg **B3** unter der Tabelle | DE-weit adressscharf, Stand 2025. **Modellgrenzen:** (a) ZÜRS zählt versicherbare **Adressen**, nicht Gebäude — je Adresse können mehrere Gebäude stehen, die Quote ist deshalb keine Gebäudequote; (b) die ZÜRS-Klassen und die Risikogebiete nach § 73 WHG sind **nicht deckungsgleich** (ZÜRS zoniert bundesweit alle bewerteten Adressen, die HWGK nur Gewässer mit signifikantem Risiko) — der Widerspruch wird benannt, nicht geglättet (§3.8); (c) GK2 enthält ausdrücklich deichgeschützte Objekte, ist also keine Restrisiko-freie Klasse | ZÜRS Geo ist nicht offen (Zugang nur für Versicherer) ⇒ die Zellgröße bildet das Produkt aus der HWGK-Überflutungsfläche (60-W085-01) × Gebäudebestand (60-R24-01); die ZÜRS-Quote dient als bundes- und bundeslandweites Abgleichsband nach §3.4 (Stichprobe, kein Vollraster-Lauf) | **Sensitivitätsband** — Kein-Doppelkanal §3.2: die zellgenaue Exposition entsteht bereits aus 60-W085-01 × 60-R24-01; R17 liefert kein zweites Multiplikativglied, sondern das nationale Prüfband (7,6 % aller Adressen in GK2–GK4, davon 1,5 % im HQ100-nahen Band) für den Abgleich nach §3.4 |
| 60-R18-01 | R18 Entwässerungssysteme → Gebäudeschaden (flussseitig) | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | **bewusst inaktiv** — Schadenskonten-System Z28 (Spalte „Ausgeschlossen”): „Betriebsunterbrechung (→K5), Infrastruktur (→K4), Personen (→K1)”; Mon. Z57 (Id 52, Spalte „Nicht enthalten”): „Gebäudeschäden durch Rückstau (ID 59).” — Rückstau bucht #59, das Kanalnetz #52 (K4) |
| 60-R19-01 | R19 Infrastruktur an Binnengewässern → Gebäudeschaden | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | **bewusst inaktiv** — Schadenskonten-System Z28 (Spalte „Ausgeschlossen”): „Betriebsunterbrechung (→K5), Infrastruktur (→K4), Personen (→K1)” — Infrastruktur an Binnengewässern bucht K4 |
| 60-E10-01 | E10 Hagel → Gebäudeschaden (flussseitig) | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | **bewusst inaktiv** — keine Kante auf #60 (NW Z61 Input nur 49); Mon. Z65 (Spalte „Wird hier bepreist (enthalten)”): „Sachschäden flussseitiger Überflutung.” |
| 60-E17-01 | E17 Starkwind → Gebäudeschaden (flussseitig) | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | **bewusst inaktiv** — keine Kante auf #60 (NW Z61 Input nur 49); Mon. Z65 (Spalte „Wird hier bepreist (enthalten)”): „Sachschäden flussseitiger Überflutung.” |
| 60-E14-01 | E14 Schnee- und Eisdruck → Gebäudeschaden (flussseitig) | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | **bewusst inaktiv** — keine Kante auf #60 (NW Z61 Input nur 49); Mon. Z65 (Spalte „Wird hier bepreist (enthalten)”): „Sachschäden flussseitiger Überflutung.” |
| 60-E02-01 | E02 Hitze → Gebäudeschaden (flussseitig) | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | **bewusst inaktiv** — keine Kante auf #60 (NW Z61 Input nur 49); Mon. Z65 (Spalte „Wird hier bepreist (enthalten)”): „Sachschäden flussseitiger Überflutung.” |
| 60-E03-01 | E03 Kälte / Frost → Gebäudeschaden (flussseitig) | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | **bewusst inaktiv** — keine Kante auf #60 (NW Z61 Input nur 49); Mon. Z65 (Spalte „Wird hier bepreist (enthalten)”): „Sachschäden flussseitiger Überflutung.” |
| 60-W074-01 | W074 Meeresspiegelhöhe → Gebäudeschaden (flussseitig) | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | **bewusst inaktiv** — Mon. Z65 (Spalte „Nicht enthalten”): „Seeseitige Schäden (ID 46); Verkehrsinfrastruktur (ID 74); Schutzkosten (ID 50, R7).” — seeseitige Schäden bucht #46 |
| 60-W077-01 | W077 Sturmfluten → Gebäudeschaden (flussseitig) | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | **bewusst inaktiv** — Mon. Z65 (Spalte „Nicht enthalten”): „Seeseitige Schäden (ID 46); Verkehrsinfrastruktur (ID 74); Schutzkosten (ID 50, R7).” — seeseitige Schäden bucht #46 |
| 60-W087-01 | W087 Sturzfluten → Gebäudeschaden (flussseitig) | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | **bewusst inaktiv** — Mon. Z56 (Spalte „Wird hier bepreist (enthalten)”): „Schäden laufen über Gebäude-Starkregen (K3), Verkehr (K4), Personen (K1); Räumung/Instandsetzung der Entwässerung über ID 52 (K4).” — Gebäudeschäden bucht #59 |
| 60-W008-01 | W008 Bergsturz, Felssturz, Steinschlag → Gebäudeschaden (flussseitig) | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | **bewusst inaktiv** — R9 (Rechenregeln Z11): „Innerhalb eines Kontos zählt jede Einheit (…Gebäude) genau einmal”; Schadenskonten-System Z29 führt „12 Rutschungen und Muren” als eigenständiges K3-Buchungsobjekt — Massenbewegungen bucht #12 |
| 60-W006-01 | W006 Rutschungen und Muren → Gebäudeschaden (flussseitig) | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | **bewusst inaktiv** — wie 60-W008-01; zusätzlich Mon. Z17 (Id 12, Spalte „Regeln”): „R7, R9” und Spalte „Bewertungsansatz”: „Wiederherstellungskosten beschädigter Gebäude (K3) …” (eigener Bewertungsansatz von #12, nicht #60) |
| 60-W091-01 | W091 Grundwasserstand → Gebäudeschaden (flussseitig) | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | **bewusst inaktiv** — Abgleich-Protokoll Punkt 5 (Zeile 10): Ziel-Name/Konto „Direktbuchung Konto K3” — Id 55 bucht eigenständig direkt in K3, außerhalb der #60-Formel (R9, Rechenregeln Z11) |
| 60-W100-01 | W100 Kanalnetze/Vorfluter → Gebäudeschaden (flussseitig) | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | **bewusst inaktiv** — Mon. Z57 (Id 52, Spalte „Schadenskonto”): „K4”; Spalte „Nicht enthalten”: „Gebäudeschäden durch Rückstau (ID 59).” |
| 60-S092-01 | S092 Vorsorge der Eigentümer (Objektschutz) → Gebäudeschaden | im Erstaufschlag **keine nach §3.5 zulässige** (Interventions-/quasi-experimentelle) Effektgröße belegt ⇒ **Abschätzung von KAP3** \(r_{\text{S092}}\) = 0,035 (Band 0,0075–0,0832), Kette §5.1 | — (keine Interventionsstudie belegt). **Befragungsevidenz:** Thieken u. a. 2008 (FLEMOps, Befragung von 1.697 Haushalten nach dem Hochwasser 2002) ist **volltextgeprüft** (Langbeleg B5, Tab. 2 S. 318), nach §3.5 als Wertquelle aber **nicht zulässig** (Befragung im Querschnitt, keine Interventionsstudie; Selbstselektion) und geht nicht in den Wert ein. **Plausibilitätsprobe der Kette §5.1 (nicht als Wert):** Tab. 2 skaliert den Gebäudeschaden bei guter Vorsorge mit C0P1 0,64 ÷ C0P0 0,92 = 0,696, bei sehr guter mit C0P2 0,41 ÷ 0,92 = 0,446, also −30 % bzw. −55 % je vorsorgendem Gebäude; die Kette §5.1 setzt je nachgerüstetem Gebäude \(s_{\text{bem}} \cdot e_{\text{bem}}\) = 0,50 · 0,70 = 0,35, also −35 % (Band 0,30 · 0,50 = 0,15 bis 0,52 · 0,80 = 0,416), und liegt damit zwischen den beiden Befragungswerten. **Kopplung S092 ↔ S093 (§3.9):** dieselbe Tab. 2 dimensioniert über die Vorsorge-Einzelachse (ln(0,92 ÷ 0,41) = 0,808) das Band von 60-S093-01 (B5); ändert sich die Lesart von Tab. 2, sind beide Zeilen neu zu prüfen | Herleitung §5.1 (`#s092-wirkung`) | §3.9 ABGESCHÄTZT; Setzung für deutsche Kommunen | kommunal (Pauschalfaktor — Modellgrenze der Abschätzung) | **Maßnahmen-Hebel (abgeschätzt)** — FS-Vorsorge; wirkt multiplikativ auf den Erwartungsschaden (§5.1), Wert und Band sind die Abschätzung von KAP3 nach §3.9/Vorgabe P2, Herleitung §5.1 (`#s092-wirkung`) |
| 60-S093-01 | S093 Gebäudezustand → Schadensgrad | Zustands-/Qualitätsachse der Wassertiefe-Schadensfunktion: FLEMOps führt die Gebäudequalität als eigene Eingangsachse mit **zwei Klassen** („Low/medium quality“ / „high quality“) neben Wasserstand (5 Klassen: <21 / 21–60 / 61–100 / 101–150 / >150 cm) und Gebäudetyp (3 Klassen); die Schadensquote des Gebäudes steigt über diese Wasserstandsklassen von ≈ 3,5 % auf ≈ 25 %, die Qualitätsachse ist jedoch **nur grafisch** (Fig. 1) und ohne Zahlentabelle je Qualitätsklasse publiziert ⇒ **Abschätzung von KAP3** \(f_{\text{S093}}\) = 1,00 (geometrisch zentriert, Klassenanteile des Bestands nicht belegt), **Band 0,71–1,40** (Spannweitenfaktor 1,96 zwischen den beiden Zustandsklassen = mittlere Einzelachsen-Spannweite von Kontamination und Vorsorge aus FLEMOps Tab. 2), Kette in B5; Sensitivität: −29 %/+40 % auf den Schadensgrad je Zelle (gegen ±12 % Tiefenband aus 60-S074-01) | empirische Mehrfaktor-Schadensfunktion aus Betroffenenbefragung (1.697 im August 2002 betroffene Haushalte), validiert an Instandsetzungskosten von 1.274 Einzelgebäuden in drei sächsischen Kommunen; die Zustandsachse selbst ist in der Quelle nur als Grafik ausgewiesen, der Bandwert ist deshalb eine Abschätzung von KAP3 (§3.9) | Thieken, A. H.; Olschewski, A.; Kreibich, H.; Kobsch, S.; Merz, B. 2008, „Development and evaluation of FLEMOps – a new Flood Loss Estimation MOdel for the private sector“, WIT Transactions on Ecology and the Environment 118, 315–324, WIT Press, DOI 10.2495/FRIAR080301, https://www.witpress.com/elibrary/wit-transactions-on-ecology-and-the-environment/118/19311, Zugriff 13.09.2026 — Volltext geprüft (Tab. 1 S. 317; Fig. 1 und Tab. 2 S. 318; S. 319 und S. 323); Elmer, F.; Thieken, A. H.; Pech, I.; Kreibich, H. 2010, „Influence of flood frequency on residential building losses“, Natural Hazards and Earth System Sciences 10, 2145–2159, DOI 10.5194/nhess-10-2145-2010, https://nhess.copernicus.org/articles/10/2145/2010/, Zugriff 13.09.2026 — Volltext geprüft (S. 2151) — Langbeleg **B5** unter der Tabelle | DE (Elbe- und Donaueinzugsgebiet, Ereignisse 2002 sowie 2005/2006). **Modellgrenzen:** (a) die Qualitätsklassen stammen aus den INFAS-Ausstattungsklassen („value of the equipment, windows, doors etc.“, sechs Klassen), nicht aus einer bautechnischen Zustandserhebung — die Lesart „Gebäudezustand“ ist eine dokumentierte Annahme; (b) die **Richtung** der Achse ist aus der Quelle nicht auflösbar: die Beschriftung von Fig. 1 ordnet die höheren Schadensquoten der Klasse „high building quality“ zu, was der erwarteten Richtung widerspricht, und eine Zahlentabelle zur Auflösung fehlt — der Widerspruch wird benannt, nicht geglättet (§3.8); das Band läuft deshalb symmetrisch um 1; (c) die Quelle stellt selbst infrage, ob ein an einem Extremereignis abgeleitetes Schadensmodell auf häufigere Hochwasser anwendbar ist — für HQhäufig ist das Band eine Untergrenze; (d) **Typstruktur:** die Gebäudetyp-Achse von FLEMOps (3 Klassen) wird für die Schadensquote **nicht** genutzt — \(d(h)\) ist typunabhängig, der Gebäudetyp rechnet nur im Preis (\(n_t\), 60-R24-01); Modellgrenze mit Richtung (unterschätzt Einfamilienhaus-, überschätzt Mehrfamilienhaus-Zellen) und Größenordnung (Faktor 1,15–1,25 bzw. 0,63–0,77 je Gebäudetyp) in §3.3, Abschnitt „Typstruktur“ (Abschätzung von KAP3) | keine bundesweite offene Zustandserhebung des Gebäudebestands (Datenlücke §3.8); als schwacher Proxy je 100-m-Zelle stehen Baujahrsklasse und Gebäudetyp der Zensus-2022-Gebäude- und Wohnungszählung zur Verfügung (der Bauzustand selbst wird dort nicht erhoben); die Achse läuft deshalb als bundesweit einheitliches Band auf der Ebene GEBAEUDEWERT (60-R24-01) mit; Abgleich nach §3.4 auf Bundesland- und Gemeindepunkt-Stichproben, kein Vollraster-Lauf | **Sensitivitätsband, abgeschätzt** — geometrisch zentriert \(f_{\text{S093}}\) = 1,00 (§3.2; Klassenanteile nicht belegt, bei hälftigem Bestand läge das arithmetische Mittel bei 1,057); in der Kernformel §3.4 steht es als neutral gesetztes Glied (1,00), das den Basiswert nicht verschiebt (Präambel Kap. 2); das Band 0,71–1,40 läuft als Struktur-Unsicherheit der Schadensfunktion mit und wird im Produkt nach Vorgabe P1/P2 als „Abschätzung von KAP3“ samt Herleitung (B5) ausgewiesen |
| 60-S094-01 | S094 Baumaterialien → Schadensgrad | Materialachse der Wassertiefe-Schadensfunktion: die empirischen deutschen Wohngebäude-Schadensmodelle führen **keine** Baustoffachse (FLEMOps-Eingangsgrößen: Wasserstand, Gebäudetyp, Gebäudequalität, Kontamination, private Vorsorge), und die ingenieurmäßige Schadensgradskala D1–D6 gilt laut Quelle „zunächst für die allgemeine Bebauung vornehmlich in Mauerwerksbauweise“; jedes von der Einwirkung betroffene Bauwerk ist dort mindestens D1 (reiner Durchfeuchtungsschaden) ⇒ **Abschätzung von KAP3** \(f_{\text{S094}}\) = 1,00 (geometrisch zentriert), **Band 0,84–1,18** (halber logarithmischer Anteil der Zustandsachse S093), Kette in B6; Sensitivität: −16 %/+18 % auf den Schadensgrad, gemeinsam mit 60-S093-01 multiplikativ **0,60–1,66** | ingenieurmäßige Klassifikation real beobachteter Schadensbilder aus Feldeinsätzen (Hochwasser Sachsen 2002/2006/2010/2013, Sturzflut Braunsbach 2015) mit sechs- bzw. siebenstufiger Schadensgradskala D0–D6; der Zahlenwert selbst ist keine publizierte Effektgröße, sondern eine Abschätzung von KAP3 (§3.9) | Maiwald, H.; Schwarz, J. 2018, „Vereinheitlichte Schadensbeschreibung und Risikobewertung von Bauwerken unter extremen Naturgefahren“, Bautechnik 95(10), 743–753, Ernst & Sohn, DOI 10.1002/bate.201800009, https://edac.biz/fileadmin/Dokumente/06_Publikationen/Bautechnik_1018_Maiwald_Schwarz.pdf, Zugriff 13.09.2026 — Volltext geprüft (Tab. 1 und Abschn. 3.1 S. 744–745, Tab. 2 S. 745, Tab. 3 S. 746, Tab. 4 S. 747); Thieken u. a. 2008 (Fundstelle wie 60-S093-01, Tab. 1 S. 317), DOI 10.2495/FRIAR080301, Zugriff 13.09.2026 — Volltext geprüft — Langbeleg **B6** unter der Tabelle | DE (Sachsen, Baden-Württemberg). **Modellgrenzen — Bauform-Grenze der Abschätzung (§3.9):** (a) die Schadensgradbeschreibungen sind mauerwerksbasiert, materialspezifische Schadensbilder für Holz-, Fachwerk- und Leichtbaukonstruktionen sind nach eigener Aussage der Quelle „in weiterführenden Arbeiten im Detail noch herauszuarbeiten“ — für diese Bauformen ist das Band eine Untergrenze und wird nicht stillschweigend verallgemeinert; (b) die Skala ist an Extremereignissen einschließlich einer Sturzflut kalibriert (dort Dislokation ganzer Bauwerke, Schadensgrad D6), das Produkt rechnet Flusshochwasser mit deutlich geringerer Fließgeschwindigkeit; (c) die Skala beschreibt Schadensgrade, nicht Schadensquoten in Euro — die Umrechnung ist nicht Bestandteil der Quelle und bleibt Teil der Abschätzung | Baumaterial ist in der amtlichen Statistik (Zensus 2022, Hausumringe, ALKIS) bundesweit nicht als Merkmal geführt — ausdrückliche Datenlücke (§3.8); nutzbar sind je 100-m-Zelle nur Baujahrsklasse und Gebäudetyp als schwacher Materialproxy; die Achse läuft deshalb als bundesweit einheitliches Band auf der Ebene GEBAEUDEWERT (60-R24-01) mit; Abgleich nach §3.4 auf Bundesland- und Gemeindepunkt-Stichproben, kein Vollraster-Lauf | **Sensitivitätsband, abgeschätzt** — geometrisch zentriert \(f_{\text{S094}}\) = 1,00 (§3.2; Anteile der Bauweisen nicht belegt); in der Kernformel §3.4 steht es als neutral gesetztes Glied (1,00), das den Basiswert nicht verschiebt (Präambel Kap. 2); das Band 0,84–1,18 läuft als Struktur-Unsicherheit mit und wird im Produkt nach Vorgabe P1/P2 als „Abschätzung von KAP3“ samt Herleitung (B6) ausgewiesen |
| 60-S096-01 | S096 Vorsorge der öffentlichen Hand → Überflutungswahrscheinlichkeit | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | **bewusst inaktiv (geparkt: Formelstelle FS-Schutzsystem ohne Term in §3.4, Modul #50 fehlt)** — Ziel: R7-Erwartungswert-Weiche mit #50 (Mon. Z65 Spalte „Regeln”: „R7, R9”; Rechenregeln Z9 R7); bis dahin rechnet das Modell ohne Schutzsystem-Term (§3.4) |
| 60-S097-01 | S097 Zustand Schutzinfrastruktur → Versagenswahrscheinlichkeit | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | **bewusst inaktiv (geparkt: Formelstelle FS-Schutzsystem ohne Term in §3.4, Modul #50 fehlt)** — Ziel: R7-Erwartungswert-Weiche mit #50, Versagensfall (Mon. Z65 Spalte „Regeln”: „R7, R9”; Rechenregeln Z9 R7); bis dahin rechnet das Modell ohne Schutzsystem-Term (§3.4) |
| 60-S098-01 | S098 Baumaterialien Schutzinfrastruktur → Versagenswahrscheinlichkeit | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | **bewusst inaktiv (geparkt: Formelstelle FS-Schutzsystem ohne Term in §3.4, Modul #50 fehlt)** — Ziel: R7-Erwartungswert-Weiche mit #50 (Mon. Z65 Spalte „Regeln”: „R7, R9”; Rechenregeln Z9 R7); bis dahin rechnet das Modell ohne Schutzsystem-Term (§3.4) |
| 60-S104-01 | S104 Investitionen in exponierten Gebieten → Bestandsentwicklung | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | **bewusst inaktiv (geparkt: Formelstelle FS-Bestandsdynamik ohne Term)** — Kap. 6 (Modellgrenzen, „Bestandsdynamik S104”): Investitionen in exponierten Gebieten fließen im heutigen Modellstand **nicht** als eigener Pfad ein, der Gebäudebestand R24 wird für das Szenariojahr konstant gehalten; weder eine belegte noch eine abgeschätzte Wachstums- oder Rückbaurate liegt vor (Befund 47) |
| 60-R24-01 | R24 Gebäude → Mengengerüst (Gebäudewerte) | **Menge:** 19,7 Mio Wohngebäude (13,5 Mio Einfamilien-, 2,7 Mio Zweifamilien-, 3,5 Mio Mehrfamilienhäuser), 43,8 Mio Wohnungen, 4,1 Mrd m² Wohnfläche (31.12.2024) ⇒ 208 m² Wohnfläche je Wohngebäude; Fortschreibung 31.12.2025: 44,0 Mio Wohnungen, 4,1 Mrd m². **Wertsatz (Wiederherstellung/Neubauwert):** NHK 2010 Standardstufe 3 (mittlerer Standard) = 1.050 €₂₀₁₀/m² BGF (freistehende Ein-/Zweifamilienhäuser, Geb.-Art 1.01) bzw. 825 €₂₀₁₀/m² BGF (Mehrfamilienhäuser ≤ 6 WE), je inkl. Umsatzsteuer und Baunebenkosten; Indexierung mit dem Baupreisindex Wohngebäude (2015 = 100: 2010 = 89,1 → 2023 = 149,8, Faktor 1,681) ⇒ 1.765 bzw. 1.387 €₂₀₂₃/m² BGF; Fortschreibung 2023 → Preisstand 2026 mit Faktor 1,105 (Band 1,07–1,16; §3.9 **abgeschätzt**, Kette in B4) ⇒ **1.950 €₂₀₂₆/m² BGF (Band 1.890–2.043)** bzw. **1.533 €₂₀₂₆/m² BGF (Band 1.485–1.606)** (Bandenden mit den ungerundeten Faktoren 1,023³ = 1,0706 und 1,050³ = 1,1576 gerechnet, B4 Rechenschritt 2); BGF je m² Wohnfläche = 1,30 (Band 1,25–1,40; §3.9 **abgeschätzt**) ⇒ Wertdichte als **Typ-Spanne** 1.993 (MFH) bis 2.535 (EFH/ZFH) €₂₀₂₆/m² Wohnfläche, als **Unsicherheitsband** mit beiden Faktorbändern 1.856–2.860 €₂₀₂₆/m² Wohnfläche ⇒ Wiederherstellungswert des Wohngebäudebestands als Typ-Spanne 8,2 (MFH) bis 10,4 (EFH/ZFH) Bio. €₂₀₂₆, als Unsicherheitsband 7,6–11,7 Bio. €₂₀₂₆ (B4 Rechenschritte 3 und 4; Sensitivität: ±10 % auf den Indexfaktor verschieben den Bestandswert um ±0,8–1,0 Bio. €) | amtliche Statistik (Fortschreibung des Wohngebäude- und Wohnungsbestands auf Zensus-2022-Basis) + normierter Kostenkennwert aus Rechtsverordnung (ImmoWertV Anlage 4), fortgeschrieben mit amtlichem Preisindex | Destatis 2025, Pressemitteilung Nr. 336 vom 17.09.2025, „43,8 Millionen Wohnungen in Deutschland zum Jahresende 2024“, https://www.destatis.de/DE/Presse/Pressemitteilungen/2025/09/PD25_336_31231.html, Zugriff 13.09.2026; Destatis, Themenseite „Wohnen“ (Fortschreibung zum 31.12.2025: 44,0 Mio Wohnungen, 4,1 Mrd m²), https://www.destatis.de/DE/Themen/Gesellschaft-Umwelt/Wohnen/_inhalt.html, Zugriff 13.09.2026; ImmoWertV, Anlage 4 (zu § 36 Abs. 1) „Normalherstellungskosten 2010 (NHK 2010)“, https://www.gesetze-im-internet.de/immowertv_2022/anlage_4.html, Zugriff 13.09.2026; Destatis, Fachserie 17 Reihe 4 „Preisindizes für die Bauwirtschaft“ (Basis 2015 = 100), https://www.destatis.de/DE/Themen/Wirtschaft/Preise/Baupreise-Immobilienpreisindex/Publikationen/Downloads-Bau-und-Immobilienpreisindex/bauwirtschaft-preise-2170400223244.pdf?__blob=publicationFile, Zugriff 13.09.2026; Destatis 2026, PM Nr. 241 vom 10.07.2026 (Baupreise Wohngebäude Mai 2026: +5,0 % gg. Vj.), https://www.destatis.de/DE/Presse/Pressemitteilungen/2026/07/PD26_241_61261.html, Zugriff 13.09.2026 — Volltext geprüft; Langbeleg **B4** unter der Tabelle (Mon. Z65: „Gebäudewerte“) | DE-weit. **Modellgrenzen:** (a) NHK-Standardstufe 3 als bundesweiter Einheitssatz — ohne Regionalfaktor der Gutachterausschüsse streut der Wertsatz zwischen Hoch- und Niedrigpreisregionen um schätzungsweise ±20 %; (b) **Nichtwohngebäude** (Gewerbe, öffentliche Gebäude) sind im Mengengerüst nicht enthalten — die Mengenbasis ist insoweit eine Untergrenze (§3.6); (c) NHK sind **Neubau-/Wiederherstellungswerte**; der Zeitwertansatz der Arbeitsmappe (Mon. J64; Alterswertminderung nach § 38 ImmoWertV) liegt darunter — entschieden: Neuwert bleibt Basiswert, Antrag auf Fortschreibung in §7.2, Zeitwertansatz als Band mit Alterswertminderungsfaktor 0,55 (0,40–0,75; Abschätzung von KAP3), nicht geglättet (§3.8) | Gebäudezahl und Wohnfläche je Zelle aus dem Zensus-2022-Gitter (100 m) bzw. den amtlichen Hausumringen; Datenebene GEBAEUDEWERT **neu anzulegen** (§3.1, Spezifikation in Kap. 3), Fortschreibung über die Destatis-Bestandsfortschreibung; Abgleich nach §3.4 auf Bundesland- und Gemeindepunkt-Stichproben, kein Vollraster-Lauf | **Basiswert** — FS-Mengengerüst: Wohnfläche je Zelle × Wertdichte €₂₀₂₆/m²; der Zeitwertansatz (§7.2) sowie die abgeschätzten Faktoren (Indexierung 2023→2026, BGF/Wohnfläche) laufen als Sensitivitätsband mit und werden im Produkt nach Vorgabe P1/P2 als Abschätzung von KAP3 ausgewiesen |
| 60-R23-01 | R23 Bau- und Immobilienunternehmen → Gebäudeschaden | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | **bewusst inaktiv** — Schadenskonten-System Z28 (Spalte „Ausgeschlossen”): „Betriebsunterbrechung (→K5), Infrastruktur (→K4), Personen (→K1)” — Unternehmensschäden (Betriebsausfall der Bauwirtschaft) sind kein K3-Gebäudeschaden |
| 60-R25-01 | R25 Siedlungsinfrastrukturen → Gebäudeschaden | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | entfällt — kein Rechenpfad | **bewusst inaktiv** — Schadenskonten-System Z28 (Spalte „Ausgeschlossen”): „Betriebsunterbrechung (→K5), Infrastruktur (→K4), Personen (→K1)” — Siedlungsinfrastruktur bucht K4 |

### Belege zu den entschiedenen Registerzeilen (§3.8, Volltext geprüft am 13.09.2026)

**B1 — 60-W085-01 (Hazard-Szenarien und Überflutungstiefe).**
Quellen: (1) **LAWA — Bund/Länder-Arbeitsgemeinschaft Wasser (2024):** „Empfehlungen zur
Aufstellung von Hochwassergefahrenkarten und Hochwasserrisikokarten“, Stand Januar 2024,
beschlossen durch die 167. LAWA-Vollversammlung am 21./22.03.2024 in Potsdam, Herausgeber LAWA,
Potsdam; URL
`https://www.lawa.de/documents/2024-01-lawa-empfehlungen-aufstellung-hochwassergefahrenkarten-barrierefrei_1739980622.pdf`,
Archiv-Snapshot
`https://web.archive.org/web/20250914171101/https://www.lawa.de/documents/2024-01-lawa-empfehlungen-aufstellung-hochwassergefahrenkarten-barrierefrei_1739980622.pdf`
(Snapshot vom 14.09.2025), Zugriff 13.09.2026. S. 4 wörtlich: „Hochwasser mit niedriger Wahrscheinlichkeit oder Szenarien für
Extremereignisse“ · „Hochwasser mit mittlerer Wahrscheinlichkeit (Ereignisse, die im statistischen
Mittel einmal in 100 Jahren auftreten)“ · „gegebenenfalls Hochwasser mit hoher Wahrscheinlichkeit“;
anzugeben sind „Ausmaß der Überflutung (Fläche)“ und „Wassertiefe bzw. gegebenenfalls
Wasserstand“. S. 16 wörtlich: „Für jedes Hochwasserszenario sind sowohl das Ausmaß der Überflutung
(Überflutungsgebiet) als auch die Wassertiefen in den Karten darzustellen.“ und zu den Klassen:
„0–0,5 m, >0,5–1 m, >1–2 m, >2–4 m und >4 m“. S. 10 wörtlich zum Klimabezug: „Der bisher wirksam
gewordene Einfluss von Klimaveränderungen ist in den Daten der hydrologischen Statistiken
enthalten.“ (2) **§ 74 Abs. 2/3 WHG**, Fassung abgerufen unter
`https://www.gesetze-im-internet.de/whg_2009/__74.html`, Archiv-Snapshot
`https://web.archive.org/web/20250323111437/https://www.gesetze-im-internet.de/whg_2009/__74.html`
(Snapshot vom 23.03.2025; laufend gepflegte Gesetzesfassung — der Snapshot belegt den Wortlaut zum
Snapshot-Zeitpunkt, maßgeblich bleibt die am Zugriffstag abgerufene Fassung),
Zugriff 13.09.2026; Abs. 2 Nr. 1 wörtlich:
„Hochwasser mit niedriger Wahrscheinlichkeit (voraussichtliches Wiederkehrintervall mindestens 200
Jahre) oder bei Extremereignissen“. (3) **Bayerisches Landesamt für Umwelt (LfU), „FAQ:
Hochwassergefahren- und -risikokarten“**, URL
`https://www.lfu.bayern.de/wasser/hw_risikomanagement_umsetzung/faq_karten/index.htm`,
Archiv-Snapshot
`https://web.archive.org/web/20260314134744/https://www.lfu.bayern.de/wasser/hw_risikomanagement_umsetzung/faq_karten/index.htm`
(Snapshot vom 14.03.2026), Zugriff 13.09.2026; wörtlich: HQhäufig ist „ein Abfluss (Q) verstanden, der statistisch gesehen im
Mittel alle 5 bis 20 Jahre auftritt“ (die Karten zeigen ein HQ10), HQ100 ist „ein Abfluss (Q), der
im Mittel alle hundert Jahre erreicht oder überschritten wird“, HQextrem entspricht ungefähr einem
HQ1000. **Rechenschritt (§3.9 Übernommen):** p = 1/T mit T aus den zitierten Wiederkehrintervallen
— für das häufige Szenario gilt der kartierte Fall HQ10, also T = 10 a ⇒ p = 1,0·10⁻¹ a⁻¹;
die von LfU genannte Bandbreite der Praxis (T = 5 a bis T = 20 a ⇒ 2,0·10⁻¹ a⁻¹ bis
5,0·10⁻² a⁻¹) läuft als Sensitivitätsband mit. Für das mittlere Szenario gilt T = 100 a ⇒
p = 1,0·10⁻² a⁻¹. Für das Extremszenario
**benennt der Bericht den Widerspruch der Quellen, statt ihn zu glätten** (§3.8): das WHG verlangt
mindestens 200 a (⇒ 5,0·10⁻³ a⁻¹), die Länderpraxis kartiert ≈ HQ1000 (⇒ 1,0·10⁻³ a⁻¹); beide
Enden bilden das Band. **Rechenschritt (§3.9 Abgeschätzt) — Zentralwert \(p_3\):** Da beide
Enden Größenordnungsenden sind, rechnet die Kernformel mit ihrem geometrischen Mittel
√(5,0·10⁻³ · 1,0·10⁻³) = 2,236·10⁻³ a⁻¹ (T ≈ 447 a); Herleitung in §3.4 Schritt 2, im Register
als Zentralwert der Zeile 60-W085-01 geführt. **Datenlücke (§3.8):** eine bundesweit einheitliche Angabe des tatsächlich
kartierten Extrem-Wiederkehrintervalls je Land liegt nicht vor; sie ist bei der Datenanbindung je
Land zu erheben.

**B2 — 60-S074-01 (Geländehöhe → Wassertiefe am Gebäude).**
Quellen: (1) **LAIV MV — Landesamt für innere Verwaltung Mecklenburg-Vorpommern, „Geländemodelle“**,
URL `https://www.laiv-mv.de/Geoinformation/Geobasisdaten/Gelaendemodelle/`, Archiv-Snapshot
`https://web.archive.org/web/20260515142234/https://www.laiv-mv.de/Geoinformation/Geobasisdaten/Gelaendemodelle/`
(Snapshot vom 15.05.2026), Zugriff 13.09.2026;
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
Tiefenquelle, wird es neu gerechnet. **Abgrenzung zur Knoten-Bilanz:** S074 ist
**keiner eigenen Formelstelle** zugeordnet (Kap. 1, Knoten-Bilanz), sondern wirkt als
Sensitivitätsband über FS-Hazard, also über die bereits topographiebasierte HWGK-Wassertiefe
(60-W085-01); ein zweiter Topographie-Faktor wäre ein Doppelkanal (§3.2). **Datenlücke
(§3.8):** eine deutsche Sensitivitätsrechnung derselben Bauart (Schaden je 10 cm Tiefe) wurde nicht
gefunden; die niederländische Fallstudie wird als dokumentierte Übertragung geführt.

**B3 — 60-R17-01 (Exposition am Gewässernetz).**
Quellen: (1) **GDV — Gesamtverband der Deutschen Versicherer (2025):** „Geringe Gefahr für
Fluss-Hochwasser bei den meisten Wohngebäuden“, Datenservice zum Naturgefahrenreport,
Stand ZÜRS Geo 2025; URL
`https://www.gdv.de/gdv/statistik/datenservice-zum-naturgefahrenreport/sachversicherung-elementar/geringe-gefahr-fuer-fluss-hochwasser-bei-den-meisten-wohngebaeuden--147672`,
Archiv-Snapshot
`https://web.archive.org/web/20260417160705/https://www.gdv.de/gdv/statistik/datenservice-zum-naturgefahrenreport/sachversicherung-elementar/geringe-gefahr-fuer-fluss-hochwasser-bei-den-meisten-wohngebaeuden--147672`
(Snapshot vom 17.04.2026), Zugriff 13.09.2026. Wörtlich zur Gefährdungsklasse 1 (92,4 %): „statistisch nach gegenwärtiger
Datenlage nicht von Hochwasser größerer Gewässer betroffen“; wörtlich zur Gefährdungsklasse 4
(0,4 %): „Hochwasser statistisch mindestens einmal in 10 Jahren“; Bezugsgröße: 22,6 Mio erfasste
Adressen. (2) **GDV, „ZÜRS Geo — Zonierungssystem für Überschwemmungsrisiko und Einschätzung von
Umweltrisiken“**, URL
`https://www.gdv.de/gdv/themen/klima/-zuers-geo-zonierungssystem-fuer-ueberschwemmungsrisiko-und-einschaetzung-von-umweltrisiken-11656`,
Archiv-Snapshot
`https://web.archive.org/web/20260902211622/https://www.gdv.de/gdv/themen/klima/-zuers-geo-zonierungssystem-fuer-ueberschwemmungsrisiko-und-einschaetzung-von-umweltrisiken-11656`
(Snapshot vom 02.09.2026), Zugriff 13.09.2026; wörtlich zur Klasse 2: in ihr sind „auch Objekte enthalten, die durch einen
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
Archiv-Snapshot
`https://web.archive.org/web/20250917161544/https://www.destatis.de/DE/Presse/Pressemitteilungen/2025/09/PD25_336_31231.html`
(Snapshot vom 17.09.2025, im Wayback-Index mit Statuscode 200 geführt; die Wiedergabe von
Destatis-Pressemitteilungen beantwortet die Wayback Machine zurzeit mit HTTP 403 — geprüft
17.09.2026 —, der Snapshot ist deshalb indexiert, aber nicht abrufbar), Zugriff 13.09.2026;
Stichtag 31.12.2024: 43,8 Mio Wohnungen, 4,1 Mrd m² Wohnfläche,
19,7 Mio Wohngebäude (13,5 Mio Einfamilien-, 2,7 Mio Zweifamilien-, 3,5 Mio Mehrfamilienhäuser).
(2) **Statistisches Bundesamt, Themenseite „Wohnen“**, URL
`https://www.destatis.de/DE/Themen/Gesellschaft-Umwelt/Wohnen/_inhalt.html`, Archiv-Snapshot
`https://web.archive.org/web/20260831100304/https://www.destatis.de/DE/Themen/Gesellschaft-Umwelt/Wohnen/_inhalt.html`
(Snapshot vom 31.08.2026), Zugriff 13.09.2026;
wörtlich: „44,0 Millionen Wohnungen in Deutschland zum Jahresende 2025“, Gesamtwohnfläche
4,1 Mrd m² (Fortschreibung des Wohngebäude- und Wohnungsbestandes auf Zensus-2022-Basis).
(3) **ImmoWertV, Anlage 4 (zu § 36 Abs. 1) „Normalherstellungskosten 2010“**, URL
`https://www.gesetze-im-internet.de/immowertv_2022/anlage_4.html`, Archiv-Snapshot
`https://web.archive.org/web/20250901000456/https://www.gesetze-im-internet.de/immowertv_2022/anlage_4.html`
(Snapshot vom 01.09.2025; laufend gepflegte Rechtsverordnung — der Snapshot belegt den Wortlaut
zum Snapshot-Zeitpunkt, maßgeblich bleibt die am Zugriffstag abgerufene Fassung),
Zugriff 13.09.2026; wörtlich:
die NHK erfassen „die Kostengruppen 300 und 400 der DIN 276, die Umsatzsteuer und die
üblicherweise entstehenden Baunebenkosten (Kostengruppen 730 und 771 der DIN 276)“ und beziehen
sich „auf den im Jahresdurchschnitt bestehenden Kostenstand des Jahres 2010“, angegeben „in Euro
pro Quadratmeter Grundfläche“ (Brutto-Grundfläche). Kostenkennwerte Gebäudeart 1.01 (freistehende
Ein- und Zweifamilienhäuser), Standardstufen 1–5: 600 / 800 / **1.050** / 1.300 / 1.600 €/m² BGF;
Mehrfamilienhäuser bis 6 WE, Standardstufen 3–5: **825** / 985 / 1.190 €/m² BGF. Verwendet wird
Standardstufe 3 (mittlerer Standard) als bundesweiter Bestandsmittelwert. (4) **Statistisches
Bundesamt, Fachserie 17 Reihe 4 „Preisindizes für die Bauwirtschaft“ (Basis 2015 = 100)**, URL
`https://www.destatis.de/DE/Themen/Wirtschaft/Preise/Baupreise-Immobilienpreisindex/Publikationen/Downloads-Bau-und-Immobilienpreisindex/bauwirtschaft-preise-2170400223244.pdf?__blob=publicationFile`,
Archiv-Snapshot
`https://web.archive.org/web/20250416003519/https://www.destatis.de/DE/Themen/Wirtschaft/Preise/Baupreise-Immobilienpreisindex/Publikationen/Downloads-Bau-und-Immobilienpreisindex/bauwirtschaft-preise-2170400223244.pdf?__blob=publicationFile`
(Snapshot vom 16.04.2025; die PDF-Datei selbst liegt unter derselben Adresse mit dem Zusatz `id_`
hinter dem Zeitstempel), Zugriff 13.09.2026; Jahresdurchschnitte Neubau konventionell gefertigter Wohngebäude:
2010 = 89,1 · 2015 = 100,0 · 2020 = 114,0 · 2021 = 121,9 · 2022 = 139,4 · 2023 = 149,8.
(5) **Statistisches Bundesamt (2026):** Pressemitteilung Nr. 241 vom 10.07.2026, URL
`https://www.destatis.de/DE/Presse/Pressemitteilungen/2026/07/PD26_241_61261.html`,
**kein Archiv-Snapshot — Verzicht begründet:** die Wayback Machine führt zu dieser Adresse genau
einen Abruf (10.07.2026), und der ist mit Statuscode 403 gespeichert; die Wiedergabe von
Destatis-Pressemitteilungen ist archivseitig gesperrt, ein Neuabruf über „Save Page Now“ scheitert
ebenfalls (beides geprüft 17.09.2026). Ein inhaltstragender Snapshot ist damit nicht herstellbar;
die Meldung bleibt über Pressemitteilungsnummer und Datum im Destatis-Pressearchiv adressierbar,
und die hier zitierten Veränderungsraten sind mit den Vorjahresmonatswerten der Fachserie
gegenprüfbar. Zugriff 13.09.2026; wörtlich: „Die Preise für den Neubau konventionell gefertigter Wohngebäude in
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
unteres Ende drei Schritte à 2,3 % (1,023³ = 1,0706), oberes Ende drei Schritte à 5,0 %
(1,050³ = 1,1576) ⇒ **Band 1,07–1,16** (gerundete Anzeige; gerechnet wird mit 1,0706 und 1,1576).
**Woher die Jahresraten kommen (§3.9 Abgeschätzt, Vorgabe P1).** Nur das obere Bandende ist
belegt: 5,0 % ist der höchste der drei zitierten amtlichen Werte (Mai 2026). Die beiden anderen
Raten sind **gerundete Setzungen von KAP3**, nicht aus den Monatswerten errechnet: Der Zentralwert
3,4 % liegt zwischen dem Median (3,3 %) und dem arithmetischen Mittel (3,83 %) der drei zitierten
Werte, näher am Median, weil der Mai-Wert ein einzelner Monat am aktuellen Rand ist und die beiden
älteren Werte (3,2 %/3,3 %) zwei der drei Fortschreibungsjahre abbilden. Richtung und Größe der
Setzung: mit dem Median ergäbe sich 1,033³ = 1,102 (−0,2 % gegenüber 1,105), mit dem Mittel
1,0383³ = 1,119 (+1,3 %) — beide innerhalb des Bandes. Das untere Bandende 2,3 % liegt rund einen
Prozentpunkt unter dem niedrigsten zitierten Wert (3,2 %), weil für das Jahr 2024 keine Rate
zitiert ist und ein Jahresdurchschnitt unter den Monatswerten vom Jahresende 2025 liegen kann.
Ergebnis: 1.765 × 1,105 = 1.950,3 ⇒ **1.950 €₂₀₂₆/m² BGF** (Band 1.765 × 1,0706 = 1.889,6 bis
1.765 × 1,1576 = 2.043,2 ⇒ **1.890–2.043**); 1.387 × 1,105 = 1.532,6 ⇒ **1.533 €₂₀₂₆/m² BGF**
(Band 1.387 × 1,0706 = 1.484,9 bis 1.387 × 1,1576 = 1.605,6 ⇒ **1.485–1.606**). **Modellgrenze:**
Die Jahresraten sind gesetzt, nicht aus einer amtlichen Jahresdurchschnittsreihe gemessen; der
Zentralwert 1.950 / 1.533 hängt an der Setzung 3,4 % (Wirkung der Alternativen Median/Mittel:
−0,2 % bzw. +1,3 % auf \(n_t\)); erscheint die Jahresdurchschnittsreihe bis 2026, wird der Schritt
durch den gemessenen Indexstand ersetzt (Rechenschritt 4, „Kopplung“). **Produkt-Kennzeichnung
(Vorgabe P1/P2):** der Fortschreibungsfaktor ist eine begründete Abschätzung von KAP3, keine
Quellenangabe, und wird in der nutzersichtbaren Parameterliste als solche geführt.

**Rechenschritt 3 (§3.9 Abgeschätzt) — BGF je m² Wohnfläche.** Die amtliche Bestandsstatistik
führt Wohnfläche, die NHK je m² Brutto-Grundfläche; eine bundesweite amtliche BGF-Statistik des
Bestands existiert nicht (**Datenlücke §3.8**). Angesetzt wird BGF/Wohnfläche = **1,30**
(Band 1,25–1,40) — begründet damit, dass Wohnfläche weder Konstruktionsflächen (Außen- und
Innenwände) noch Erschließungs-, Keller- und Nebenflächen enthält, die in der BGF mitzählen.
Ergebnis: 1.533 × 1,30 = 1.992,9 ⇒ **1.993 €₂₀₂₆/m² Wohnfläche** (Mehrfamilienhaus) und
1.950 × 1,30 = 2.535 ⇒ **2.535 €₂₀₂₆/m² Wohnfläche** (Ein-/Zweifamilienhaus). Die Spanne
1.993–2.535 ist eine **Typ-Spanne** (reiner MFH- gegen reinen EFH/ZFH-Satz), kein
Unsicherheitsband. Das **Unsicherheitsband** entsteht erst, wenn die Bänder der beiden
abgeschätzten Faktoren fortgepflanzt werden (alle Enden gleichgerichtet): unten 1.484,9 × 1,25 =
1.856 (MFH), oben 2.043,2 × 1,40 = 2.860 (EFH/ZFH) ⇒ **1.856–2.860 €₂₀₂₆/m² Wohnfläche**.

**Rechenschritt 4 (§3.9 Abgeleitet) — Bestandsprobe und Sensitivität.** 4,1 Mrd m² Wohnfläche ×
1.993 bis 2.535 €₂₀₂₆/m² = 8,17 bis 10,39 ⇒ **8,2 (MFH) bis 10,4 (EFH/ZFH) Bio. €₂₀₂₆**
Wiederherstellungswert des Wohngebäudebestands als Typ-Spanne; mit dem Unsicherheitsband der
Wertdichte 4,1 Mrd m² × 1.856 bis 2.860 €₂₀₂₆/m² = 7,61 bis 11,73 ⇒ **7,6–11,7 Bio. €₂₀₂₆**; je Wohngebäude 4,1 Mrd m² ÷ 19,7 Mio = **208 m² Wohnfläche**. Sensitivität:
±10 % auf den Fortschreibungsfaktor verschieben den Bestandswert um ±0,8 bis 1,0 Bio. €; der
BGF-Faktor 1,25 statt 1,40 verschiebt ihn um −11 %. **Kopplung (§3.9):** die Wertdichte hängt am
Baupreisindex; erscheint die Jahresdurchschnittsreihe bis 2026, wird Rechenschritt 2 durch den
gemessenen Indexstand ersetzt und der Wertsatz neu gerechnet. **Widerspruch (§3.8, benannt statt
geglättet):** die NHK sind Neubau-/Wiederherstellungswerte, die Schadensrechnung K3 kann je nach
Regulierungspraxis auch Zeitwerte ansetzen (Alterswertminderung nach ImmoWertV); die Arbeitsmappe
schreibt über Mon. J65 → J64 den Zeitwertansatz vor. **Entschieden:** Der Neuwert bleibt Basiswert,
die Abweichung von J64 steht als Antrag auf Fortschreibung in §7.2 (Anker `#fortschreibung-neuwert-k3`);
der Zeitwertansatz läuft dort als beziffertes Band mit (Alterswertminderungsfaktor 0,55, Band
0,40–0,75, Abschätzung von KAP3; K3-Betrag −45 %). **Status des Antrags:** beantragt 17.09.2026,
noch nicht entschieden, im Abgleich-Protokoll der Mappe noch ohne Zeile; Entscheider, Frist und die
Folge für die Abnahme (Quellen-Synchronität, LF 14) stehen in §7.2 unter „Status". **Modellgrenze:**
Nichtwohngebäude sind im Mengengerüst nicht enthalten — die Mengenbasis ist insoweit eine
Untergrenze (§3.6).

**B5 — 60-S093-01 (Gebäudezustand → Schadensgrad).**
Quellen: (1) **Thieken, A. H.; Olschewski, A.; Kreibich, H.; Kobsch, S.; Merz, B. (2008):**
„Development and evaluation of FLEMOps – a new *F*lood *L*oss *E*stimation *MO*del for the
*p*rivate *s*ector“, in: *Flood Recovery, Innovation and Response I*, WIT Transactions on Ecology
and the Environment, Vol. 118, S. 315–324, WIT Press, Southampton, DOI `10.2495/FRIAR080301`,
URL `https://www.witpress.com/elibrary/wit-transactions-on-ecology-and-the-environment/118/19311`,
Archiv-Snapshot
`https://web.archive.org/web/20250118023945/https://www.witpress.com/elibrary/wit-transactions-on-ecology-and-the-environment/118/19311`
(Snapshot vom 18.01.2025; der Snapshot sichert die Verlagsseite, der persistente Nachweis des
Beitrags ist die DOI), Zugriff 13.09.2026 (Volltext gegengelesen). Tab. 1 (S. 317) wörtlich zu den Eingangsgrößen:
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
URL `https://nhess.copernicus.org/articles/10/2145/2010/`, Archiv-Snapshot
`https://web.archive.org/web/20260305025018/https://nhess.copernicus.org/articles/10/2145/2010/`
(Snapshot vom 05.03.2026; der persistente Nachweis ist auch hier die DOI),
Zugriff 13.09.2026 (Volltext
gegengelesen); S. 2151 wörtlich: „In the basic FLEMOps model, five water level classes, three
building types and two building quality classes are used as input.“
**Datenlücke (§3.8):** eine Zahlentabelle der Schadensquoten je Qualitätsklasse ist in beiden
Quellen nicht publiziert; die Qualitätsachse ist ausschließlich grafisch ausgewiesen. Eine
bautechnische, bundesweite Zustandserhebung des Wohngebäudebestands existiert ebenfalls nicht.
**Widerspruch (§3.8, benannt statt geglättet):** die Beschriftung von Fig. 1 ordnet die **höheren**
Schadensquoten der Klasse „high building quality“ zu; fachlich erwartet würde die umgekehrte
Richtung. Ohne Zahlentabelle ist der Widerspruch aus der Quelle nicht auflösbar; das abgeschätzte
Band wird deshalb **symmetrisch** um 1 geführt und die Richtung nicht gesetzt.
**Rechenschritt (§3.9 Abgeschätzt) — Band der Zustandsachse.** Belegt sind in Tab. 2 (S. 318)
die Skalierungsfaktoren zweier weiterer Modifikatoren derselben Datenbasis, Kontamination und
private Vorsorge (Vorsorge ist bewohnerseitig, Kontamination ereignisseitig — keine der beiden ist
eine gebäudeseitige Achse). Die Spannweite 0,41–1,58 ist die **Diagonale** C0P2 ↔ C2P0 über beide
Achsen zugleich; sie wird deshalb nicht selbst geteilt, sondern in ihre **Einzelachsen** zerlegt,
jeweils vom gemeinsamen Referenzfeld C0P0 = 0,92 aus: Kontamination C0P0 → C2P0 =
ln(1,58 ÷ 0,92) = ln 1,717 = **0,541**; Vorsorge C0P2 → C0P0 = ln(0,92 ÷ 0,41) = ln 2,244 =
**0,808**. (Die beiden Einzelspannen summieren sich über C0P0 zur Diagonale 1,349; gerechnet wird
aber mit den Einzelachsen.) Die Gebäudequalität ist in Tab. 1 als gleichrangige Eingangsgröße
neben diesen beiden Modifikatoren geführt, ohne eigenen Zahlenwert. KAP3 setzt deshalb für die
Qualitätsachse die **mittlere logarithmische Einzelachsen-Spannweite** der **zwei** belegten
Achsen an: (0,541 + 0,808) ÷ 2 = **0,6745** ⇒ Spannweitenfaktor e^0,6745 = 1,963 zwischen den
beiden Zustandsklassen. **Geometrisch zentriert** um 1 (nicht mittelwertzentriert — Anteile der
beiden Qualitätsklassen am Bestand sind weder in der Quelle noch in der amtlichen Statistik
ausgewiesen): √1,963 = 1,401 ⇒ **1,40** für die schadensanfälligere, 1 ÷ 1,401 = 0,7137 ⇒
**0,71** für die unempfindlichere Klasse, Zentralwert **1,00**. **Folge der geometrischen
Zentrierung für den Basiswert:** der Basiswert rechnet mit dem Zentralwert 1,00 und bleibt
unverändert. Wären die beiden Klassen hälftig im Bestand vertreten, läge das arithmetische Mittel
bei (0,7137 + 1,4011) ÷ 2 = 1,057, also +5,7 % (zusammen mit der Materialachse aus B6 +7,3 %);
diese Abweichung liegt innerhalb des Bands und wird als Modellgrenze der Abschätzung geführt, nicht
in den Basiswert gezogen, solange die Klassenanteile nicht belegt sind. **Zuordnung der Endwerte
von Fig. 1:** die abgelesenen Endwerte ≈ 3,5 % und ≈ 25 % sind keiner der beiden Qualitätskurven
zahlenmäßig zuordenbar (keine Zahlentabelle, widersprüchliche Beschriftung, siehe oben); KAP3 liest
sie als Werte der geometrischen Mitte beider Kurven, also bei \(f_{\text{S093}}\) = 1,00 — eine
dokumentierte Annahme; gehörten sie einer der beiden Kurven, läge die Mitte um den Faktor 0,71
bzw. 1,40 verschoben, also am Bandrand. **Sensitivität:** das Band verschiebt den Erwartungsschaden
je Zelle um −29 % bis +40 % und ist damit größer als das Tiefenband aus 60-S074-01 (±12 %); ein
Wechsel der Anteilsannahme auf die kleinere Einzelachse Kontamination (0,541) ergäbe 0,76–1,31, auf
die größere Einzelachse Vorsorge (0,808) 0,67–1,50, auf die volle Diagonale (1,349,
e^±0,6745) 0,51–1,96 — die Annahme der mittleren Einzelachse liegt damit zwischen den beiden belegten Achsen.
**Kopplung (§3.9):** erscheint eine Zahlentabelle der FLEMOps-Qualitätsachse oder eine deutsche
Zustandsstatistik, wird dieser Schritt durch die gemessenen Werte ersetzt und das Band neu
gerechnet. **Kopplung S092 ↔ S093 (§3.9):** die Vorsorge-Faktoren derselben Tab. 2 (C0P1 0,64 und
C0P2 0,41 gegen C0P0 0,92) tragen die Vorsorge-Einzelachse dieses Bands und dienen zugleich in der
Registerzeile 60-S092-01 als Plausibilitätsprobe der Kette §5.1 (nicht als Wert); ändert sich die
Lesart von Tab. 2, sind beide Zeilen neu zu prüfen. **Produkt-Kennzeichnung (Vorgabe P1/P2):** \(f_{\text{S093}}\) ist eine begründete
Abschätzung von KAP3, keine Quellenangabe, und steht mit dieser Herleitung in der nutzersichtbaren
Parameterliste.

**B6 — 60-S094-01 (Baumaterialien → Schadensgrad).**
Quellen: (1) **Maiwald, H.; Schwarz, J. (2018):** „Vereinheitlichte Schadensbeschreibung und
Risikobewertung von Bauwerken unter extremen Naturgefahren“, *Bautechnik* 95(10), S. 743–753,
Ernst & Sohn, Berlin, DOI `10.1002/bate.201800009`, Sonderdruck-URL
`https://edac.biz/fileadmin/Dokumente/06_Publikationen/Bautechnik_1018_Maiwald_Schwarz.pdf`,
Archiv-Snapshot
`https://web.archive.org/web/20231107034021/https://edac.biz/fileadmin/Dokumente/06_Publikationen/Bautechnik_1018_Maiwald_Schwarz.pdf`
(Snapshot vom 07.11.2023; die PDF-Datei selbst liegt unter derselben Adresse mit dem Zusatz `id_`
hinter dem Zeitstempel; der persistente Nachweis des Aufsatzes ist die DOI),
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
hergeleitete logarithmische Achsenanteil 0,6745. Das Baumaterial ist in **keinem** der beiden
empirischen Modelle eine eigene Achse, obwohl sie auf 1.697 (Thieken u. a. 2008) bzw. 2.158
Schadensfällen (Elmer u. a. 2010) beruhen; hätte es eine mit Zustand, Kontamination oder Vorsorge
vergleichbare Wirkung, wäre es dort als Achse aufgetaucht. KAP3 setzt den Materialbeitrag deshalb
auf den **halben logarithmischen Anteil** der Zustandsachse: 0,6745 ÷ 2 = 0,3373 ⇒ Spannweitenfaktor
e^0,3373 = 1,401; geometrisch zentriert um 1 (Anteile der Bauweisen am Bestand nicht belegt, wie B5)
√1,401 = 1,184 ⇒ **1,18** (schadensanfälligere Bauweise) bzw. 1 ÷ 1,184 = 0,845 ⇒ **0,84**
(unempfindlichere Bauweise), Zentralwert **1,00**; arithmetisches Mittel bei hälftigem Bestand
(0,845 + 1,184) ÷ 2 = 1,014, also +1,4 % (Modellgrenze wie B5, nicht im Basiswert).
**Sensitivität:** allein −16 % bis +18 % auf den Schadensgrad; multiplikativ mit dem Zustandsband aus B5
(0,7137 × 0,8448 = 0,603 bis 1,4011 × 1,1837 = 1,658; gleichgerichtete Endpunkte, also
Vollkorrelation beider Achsen als konservative Annahme) spannt die Strukturachse insgesamt **0,60–1,66**.
**Bauform-Grenze als Modellgrenze der Abschätzung (§3.9):** der Wert ist an
Mauerwerksbauweise kalibriert; für Holz-, Fachwerk- und Leichtbaukonstruktionen sowie für
Lehmmörtel-Mauerwerk ist 1,18 eine Untergrenze, und die Übertragung wird nicht stillschweigend
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
  (Kap. 1, „Konto-Einbettung“: Preisstandjahr 2026, abgeleitet aus Register 60-R24-01; §3.9
  abgeschätzt ist allein der Fortschreibungsfaktor 2023 → 2026). Die
  Wertsätze der Ebene GEBAEUDEWERT sind auf genau diesen Preisstand indexiert (Register
  60-R24-01, Langbeleg B4).
- **Betrachtungsebene:** die **Kommune**; gerechnet wird auf 100-m-Zellen innerhalb der Kommune,
  der deklarierte Ausweis ist die Kommune. Referenz- und Zentrierungsmittel dieses Kapitels stammen
  nach §3.2 entweder aus amtlicher Statistik oder aus der Betrachtungsebene selbst (die Zellen
  derselben Kommune), nie aus einer Aggregation über eine höhere Ebene.
- **Physischer Teil-Ausweis (Zwischengröße vor dem Euro):** die **schadensäquivalente Wohnfläche**
  \(\bar A\) in **m²/a** — diejenige Wohnfläche, deren vollständige Wiederherstellung dem
  erwarteten Schaden der Zelle beziehungsweise der Kommune entspricht. Sie entsteht in der Formel
  vor jedem Euro-Betrag und trägt ihn auf der **Zelle**: \(\text{EAD}_z = \bar A_z \cdot w_z\).
  Auf der deklarierten Betrachtungsebene **Kommune** ist der Euro-Ausweis die Summe über die Zellen,
  \(\text{EAD}_k = \sum_{z \in k} \bar A_z \cdot w_z\) (§3.6), und keine Multiplikation von
  \(\bar A_k\) mit einer einzigen Wertdichte. **Modellgrenze:** \(\bar A_k\) und
  \(\text{EAD}_k\) sind über Kommunen hinweg **nicht proportional**, sobald der Gebäudetyp-Mix
  \(\theta_{z,t}\) zwischen den Zellen wechselt, weil die Wertdichte \(w_z\) zwischen
  \(1{,}30 \cdot 1.533\) und \(1{,}30 \cdot 1.950\) €₂₀₂₆/m² Wohnfläche liegt; der Quotient
  \(\text{EAD}_k / \bar A_k\) ist die mit \(\bar A_z\) gewichtete Wertdichte der Kommune.
  Gerechnetes Beispiel (Golden-Test in §3.6): eine Ein-/Zweifamilienhaus-Zelle und eine
  Mehrfamilienhaus-Zelle ergeben \(\text{EAD}_k = 20.195{,}7\) €₂₀₂₆/a gegen
  \(\bar A_k \cdot w_{\text{Kommune}} = 18.077{,}9\) €₂₀₂₆/a mit der wohnflächengewichteten
  Wertdichte der Kommune — 10,5 % Abweichung bezogen auf \(\text{EAD}_k\).
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
| **HQ_TIEFE** — Wassertiefe \(h_{z,s}\) je Zelle und Szenario | **neu anzulegen** | dieselbe Quelle; die Tiefenklassen 0–0,5 / >0,5–1 / >1–2 / >2–4 / >4 m sind nach LAWA 2024, S. 16 Pflichtbestandteil jeder Karte (B1) | flächengewichtetes Mittel der Tiefenklassen-Mittelwerte über den überfluteten Teil der Zelle; offene oberste Klasse mit ihrer Untergrenze angesetzt (Untergrenze, §3.6) | Zelle mit \(a_{z,s} > 0\), aber ohne Tiefenangabe: Median der Tiefenklasse **derselben Kommune im selben Szenario** (Betrachtungsebene selbst, §3.2); fehlt auch der, die amtlich publizierte Klassenverteilung des Bundeslandes | keine Zentrierung; die Tiefe geht über die Schadensfunktion aus Abschnitt 3.3 dieses Berichts ein |
| **GEBAEUDEWERT** — Wohnfläche \(W_z\), Gebäudetyp-Mix \(\theta_{z,t}\), Wertdichte \(w_z\) | **neu anzulegen** | Zensus 2022, Gebäude- und Wohnungszählung, 100-m-Gitter (offener Download ohne Schlüssel) für Wohnfläche und Gebäudetyp; Wertsätze aus ImmoWertV Anlage 4 (NHK 2010) und Destatis-Baupreisindex, Fortschreibung nach Register 60-R24-01 (B4) | \(W_z\) = Summe der Wohnfläche der Gitterzelle; \(\theta_{z,t}\) = Anteil der Wohnfläche je Gebäudetyp \(t\) (Ein-/Zweifamilien- gegen Mehrfamilienhaus); \(w_z = k_{\text{BGF}} \sum_t \theta_{z,t} n_t\) | Zelle mit Gebäudebestand, aber ohne Typaufteilung: Typ-Mix **der übrigen Zellen derselben Kommune** (§3.2); fehlt auch der, der amtlich publizierte Bestandsmix des Bundeslandes | \(w_z\) ist ein Preis, kein Modifikator — keine Zentrierung; Preisstand 2026 einheitlich (Indexierung 2010 → 2023 belegt; Fortschreibung 2023 → 2026 mit Faktor 1,105 = Abschätzung von KAP3, §3.9, Band 1,07–1,16, Herleitung B4) |
| **GEBAEUDEZUSTAND_BAUSTOFF** — Zustands- und Materialachse \(f_{S093}\), \(f_{S094}\) | **geparkt (Datenquelle fehlt)** — Beschaffungs-Watchlist | keine bundesweite offene Erhebung von Bauzustand oder Baumaterial je Zelle; Zensus 2022 führt Baujahrsklasse und Gebäudetyp, nicht den Bauzustand und nicht den Baustoff (Register 60-S093-01, 60-S094-01) | entfällt, solange die Ebene geparkt ist | \(f_{S093} = f_{S094} = 1{,}00\) — der Zentrierungs-Neutralwert, dokumentiert und nicht still (§3.1) | geometrisch zentriert um 1 (§3.2; Klassenanteile nicht belegt, B5/B6); die Bänder 0,71–1,40 und 0,84–1,18 laufen als Struktur-Unsicherheit mit (multiplikativ 0,60–1,66) |

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

<a id="tiefen-schadensfunktion"></a>
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

*Gültigkeitsbereich und Deckelung (P1).* Die log-lineare Form gilt **ausschließlich** im belegten
Intervall \(h_1 = 0{,}10\) m … \(h_5 = 1{,}75\) m; unterhalb \(h_1\) wird sie auf \(d = 0{,}035\)
und oberhalb \(h_5\) auf \(d = 0{,}250\) **konstant fortgesetzt**, formal
\(d(h) = 0{,}035\) für \(h < 0{,}10\) m, \(d(h) = 0{,}250\) für \(h > 1{,}75\) m. Ohne diese
Deckelung liefe die Formel über das belegte obere Ende hinaus und ergäbe für tiefe Zellen
Schadensquoten über 100 % des Wiederherstellungswerts (\(d(3{,}0) = 1{,}109\),
\(d(4{,}0) = 3{,}65\)), also einen Euro-Betrag oberhalb des Gebäudewerts — sachlich ausgeschlossen.
Die Deckelung ist keine Extrapolation, sondern die Weigerung zu extrapolieren: Sie setzt jenseits
des Belegs genau den obersten belegten Wert an und ist damit dieselbe Konstruktion wie die
konstante Tail-Fortsetzung in Schritt 2 von Abschnitt 3.4 dieses Berichts. Sie ist eine **Abschätzung von KAP3** (§3.9,
Vorgabe P1); Richtung: **unterschätzt** den Schaden sehr tiefer Überflutungen, weil die
FLEMOps-Achse oberhalb 150 cm nicht endet, sondern nur nicht mehr differenziert wird — damit eine
Untergrenze im Sinne §3.6. Als obere Sensitivitätsgrenze läuft die ungedeckelte Interpolation bis
zur physischen Schranke \(d \le 1{,}00\) mit; das Band der Zellen mit \(h > 1{,}75\) m ist damit
0,250 … 1,000 und wird in Kap. 7 als eigener Unsicherheitsbeitrag geführt.

*Abbildung der beiden Tiefenraster (§3.1).* Die Ebene HQ_TIEFE liefert nach LAWA 2024 die Klassen
0–0,5 / >0,5–1 / >1–2 / >2–4 / >4 m, die Schadensfunktion ist auf der feineren FLEMOps-Achse
(<21 / 21–60 / 61–100 / 101–150 / >150 cm) belegt; in \(d(h)\) geht deshalb **nicht** eine
Klassennummer ein, sondern die in Abschnitt 3.2 dieses Berichts abgeleitete metrische Tiefe \(h_{z,s}\) in Metern
(flächengewichtetes Mittel der LAWA-Klassenmitten 0,25 / 0,75 / 1,50 / 3,00 m, offene Klasse >4 m
mit ihrer Untergrenze 4,00 m), die dann in \(d(h)\) mit Deckelung eingesetzt wird — die beiden
obersten LAWA-Klassen (3,00 m und 4,00 m) fallen dadurch beide auf den gedeckelten Wert
\(d = 0{,}250\).

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
die Stützstellen oben), zusätzlich zu den geometrisch zentrierten Achsen \(f_{S093}\) und
\(f_{S094}\) mit ihrem gemeinsamen Band 0,60–1,66.

*Typstruktur — Modellgrenze (§3.9 Abgeschätzt, Vorgabe P1/P2).* FLEMOps ist nach drei Gebäudetypen
strukturiert (Einfamilien-, Doppel-/Reihen-, Mehrfamilienhaus; Langbeleg B5, Tab. 1), publiziert
die Schadensquote je Typ aber nicht als Zahlentabelle. \(d(h)\) wird deshalb **typunabhängig** für
alle Gebäude der Zelle angesetzt; der Gebäudetyp rechnet im Modell nur im Preis (Wertsatz \(n_t\),
60-R24-01, §3.4), nicht in der Schadensquote. Die Endwerte 3,5 %/25 % liest KAP3 als Wert des
nationalen Typ-Mixes (Wohnflächenanteil EFH/ZFH \(\bar\theta\) = 0,596, §4.3). **Richtung:** Ein
überflutetes Erdgeschoss ist beim Einfamilien-/Zweifamilienhaus rund die Hälfte des Gebäudewerts,
beim Mehrfamilienhaus mit drei bis fünf Geschossen rund ein Viertel bis ein Drittel; das Verhältnis
der Schadensquoten MFH ÷ EFH liegt damit bei \(\rho\) ≈ 0,50–0,67 (Abschätzung von KAP3, keine
Quelle). Typunabhängig gerechnet wird der Schaden **EFH-geprägter Zellen unterschätzt** und der
**MFH-geprägter Zellen überschätzt**. **Größenordnung:** Mit \(\bar\theta\) = 0,596 folgt
\(d_{\text{EFH}} = d \div (0{,}596 + 0{,}404\,\rho)\) und \(d_{\text{MFH}} = \rho \cdot d_{\text{EFH}}\): bei
\(\rho\) = 0,50 Faktor 1,25 (EFH) bzw. 0,63 (MFH), bei \(\rho\) = 0,67 Faktor 1,15 bzw. 0,77. Eine reine
EFH-Zelle läge also um +15 % bis +25 % höher, eine reine MFH-Zelle um −23 % bis −37 % niedriger. Beide
Faktoren liegen im gemeinsamen Band 0,60–1,66 der Achsen \(f_{S093}\), \(f_{S094}\); die Bundessumme
ist über den Niveau-Skalar (§4.4) kalibriert und bleibt in erster Näherung unberührt, betroffen ist
die Verteilung zwischen ländlichen und städtischen Kommunen. Liegt eine Zahlentabelle je Typ vor, wird
\(d(h)\) je Typ geführt und mit \(\theta_{z,t}\) gewichtet; bis dahin ist die Typunabhängigkeit eine
ausgewiesene Modellgrenze, keine stille Vereinfachung.

<a id="kernformel-zelle"></a>
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

Die Wertsätze \(n_t\) sind im Kern belegt, mit abgeschätztem Fortschreibungsfaktor (§3.9), und auf den Preisstand 2026 indexiert (Register 60-R24-01, B4):
\(n_{\text{EFH/ZFH}} = 1.950\) €₂₀₂₆/m² BGF (Band 1.890–2.043),
\(n_{\text{MFH}} = 1.533\) €₂₀₂₆/m² BGF (Band 1.485–1.606). Der Umrechnungsfaktor
\(k_{\text{BGF}} = 1{,}30\) m² BGF je m² Wohnfläche (Band 1,25–1,40) ist eine **Abschätzung von
KAP3** (§3.9, Herleitung in Register 60-R24-01: Verhältnis von Brutto-Grundfläche zu Wohnfläche
im Wohnungsbau, Band aus der Spannweite zwischen kompakten Mehrfamilien- und gegliederten
Einfamilienbauten). Die Wertsätze sind Neuwerte. Der von der Arbeitsmappe (Mon. J64) vorgesehene
Zeitwertansatz wird nicht übernommen, sondern mit dem Alterswertminderungsfaktor
\(f_{\text{AWM}}\) = 0,55 (Band 0,40–0,75, Abschätzung von KAP3) als Sensitivitätsband geführt;
Entscheidung, Herleitung und Ergebnis-Sensitivität in §7.2 (Antrag auf Fortschreibung).

**Formelstelle FS-Schutzsystem — in dieser Fassung inaktiv (geparkt).** Die Arbeitsmappe verlangt
für #60 die Einbindung öffentlicher Schutzsysteme über die R7-Erwartungswert-Weiche
(`KWRA-Monetarisierung.xlsx`, Blatt „Rechenregeln", C20 (A5): „Schutzsysteme über die
R7-Erwartungswert-Weiche"; C9 (R7): „Erwartungswert über Halte- und Versagensfall,
wahrscheinlichkeitsgewichtet"). Die Kernformel trägt diesen Term noch nicht: \(p_i\) wird unverändert
aus den Szenarien der Gefahrenkarte übernommen, ohne Aufteilung in Halte- und Versagensfall. Die
Knoten S096, S097 und S098 sind deshalb in Kap. 1 als inaktiv (geparkt) geführt; beziffert wird
die Weiche erst mit dem Schutzsystem-Modul #50, das Halte- und Versagenswahrscheinlichkeiten
liefert. **Modellgrenze:** Bis dahin rechnet \(\text{EAD}\) mit dem Schutzstand, den die
Gefahrenkarte im jeweiligen Szenario abbildet; eine Änderung am Schutzsystem verändert das Ergebnis
nicht, und Maßnahmen an öffentlichen Schutzanlagen haben in #60 keinen Hebel. Das ist keine
Nullwirkung im Sinne von P2, sondern ein fehlender Anschluss: Die Wirkung wird im Modul #50
abgeschätzt und nicht hier auf null gesetzt.

**Lackmustest (§3.1).** Eine Kommune ohne Flussaue erhält in jedem Szenario \(a_{z,s} = 0\) für
alle ihre Zellen, damit \(A_{z,s} = 0\), \(\bar A_z = 0\) und \(\text{EAD}_z = 0\) — ohne
Sonderregel und ohne Rest aus einer höheren Ebene. Kein Summand der Formel stammt aus einer
nationalen Größe, die räumlich verteilt würde.

**Rechenbeispiel (eine Zelle).** Reines Einfamilienhausgebiet in der Aue,
\(W_z = 1.200\) m² Wohnfläche, \(\theta_{\text{EFH/ZFH}} = 1{,}0\) ⇒
\(w_z = 1{,}30 \cdot 1.950 = 2.535\) €₂₀₂₆/m² Wohnfläche. Szenarien: HQhäufig
\(a = 0{,}25\), \(h = 0{,}405\) m ⇒ \(d = 0{,}050\); HQ100 \(a = 0{,}80\), \(h = 0{,}805\) m ⇒
\(d = 0{,}081\); HQextrem \(a = 1{,}00\), \(h = 1{,}80\) m ⇒ \(d = 0{,}250\) (gedeckelt, da
\(h > h_5\)). Physische
Zwischengrößen: 15,0 / 77,8 / 300,0 m² je Ereignis, daraus \(\bar A_z = 6{,}31\) m²/a und
\(\text{EAD}_z \approx 16.000\) €₂₀₂₆/a.

```python test: beispiel_60_kernformel_zelle
# Schadensfunktion: log-lineare Interpolation zwischen den belegten Enden (B5),
# ausserhalb des belegten Intervalls [h1, h5] konstant fortgesetzt (Deckelung)
d1, d5, h1, h5 = 0.035, 0.250, 0.10, 1.75
d = lambda h: d1 * (d5 / d1) ** ((min(max(h, h1), h5) - h1) / (h5 - h1))
assert abs(d(0.405) - 0.0503) < 5e-4 and abs(d(0.805) - 0.0811) < 5e-4
assert abs(d(1.255) - 0.1386) < 5e-4 and abs(d(1.75) - 0.250) < 1e-9
# Deckelung: oberhalb 1,75 m bleibt die Quote auf dem obersten belegten Wert,
# insbesondere fuer die LAWA-Klassen >2-4 m (3,00 m) und >4 m (Untergrenze 4,00 m)
assert d(3.00) == 0.250 and d(4.00) == 0.250 and d(0.05) == 0.035
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

### 3.5 Zeichentabelle (alle Formelzeichen der Kapitel 3 und 5, §3.2/§3.9)

Die Tabelle führt **jedes** Formelzeichen, das in diesem Kapitel oder in Kapitel 5 vorkommt, mit
Bedeutung, Einheit und Herkunft — auch Zeichen ohne Rechenwirkung im Basiswert: den nur als
Sensitivität geführten Alterswertminderungsfaktor \(f_{\text{AWM}}\) (§3.4, Herleitung §7.2), den
abgeschätzten Objektschutz-Anteil \(q_0\) (§4.7) und die Szenariobeiträge \(\tau_1\)…\(\tau_3\) der
Beispielrechnung in §5.1.3. Diese heißen \(\tau\) und nicht \(t\), weil \(t\) in diesem Bericht
allein den Gebäudetyp bezeichnet. Die Herkunftsspalte nennt je Zeichen entweder die Registerzeile
des Evidenz-Registers (Kap. 2) oder die Berichtsstelle, an der das Zeichen hergeleitet wird — nach
Vorgabe P1 genügt ein Code-Kommentar als Herleitung nicht. Reine Laufindizes tragen keine Einheit
und keine Datenquelle; sie sind als **Notation** gekennzeichnet. Zahlenwerte und Bänder stehen bei
den Zeichen der S092-Kette zusätzlich in der Zeichentabelle §5.1.1, die Parameter-Blöcke in Kap. 7
tragen sie maschinenlesbar.

Die Tabelle ist ein Nachschlagewerk und deshalb **alphabetisch** sortiert (§3.2): nach dem
Grundbuchstaben, lateinische vor griechischen Buchstaben, bei gleichem Buchstaben der kleine vor
dem großen, Indizes und Zusätze nachgeordnet (\(\bar A\) steht unter A, \(\Delta q\) unter Delta).
In welchem Rechenschritt ein Zeichen auftritt, nennt die Herkunftsspalte.

| Zeichen | Bedeutung | Einheit | Herkunft |
|---|---|---|---|
| \(a_{z,s}\) | überfluteter Flächenanteil der Zelle im Szenario \(s\), Wertebereich [0, 1] | – | register: 60-W085-01 — Ebene HQ_FLAECHE, Verschnitt der Gefahrenkarte mit der Zelle (§3.2, Langbeleg B1) |
| \(\bar A\) (\(\bar A_z\), \(\bar A_k\)) | jährlich erwartete schadensäquivalente Wohnfläche — indexfrei \(\bar A\) als Gattungszeichen (§3.1), mit Index für die Zelle bzw. die Kommune — physischer Teil-Ausweis; \(\text{EAD}_z = \bar A_z w_z\) gilt auf der Zelle, auf der Kommune ist \(\text{EAD}_k = \sum_{z \in k} \bar A_z w_z\) (§3.6), \(\bar A_k\) und \(\text{EAD}_k\) sind bei gemischtem Gebäudetyp nicht proportional (§3.1) | m²/a | herleitung: §3.4 Schritt 2 (Trapezsumme über die Szenarien) und §3.6 (Summe über die Zellen der Kommune) |
| \(A_{z,s}\) | schadensäquivalente Wohnfläche der Zelle im Ereignis \(s\) — die physische Zwischengröße vor jedem Euro-Betrag | m² | herleitung: §3.4 Schritt 1 — Menge \(W_z a_{z,s}\) × Rate \(d(h_{z,s}) f_{S093} f_{S094}\) |
| \(d(h)\) | Schadensquote: Anteil des Wiederherstellungswerts, der bei der Tiefe \(h\) verloren geht | – | herleitung: §3.3 — Enden belegt (Wasserstandsachse von FLEMOps, Langbeleg B5), Zwischenwerte und Deckelung sind Abschätzung von KAP3 (§3.9) |
| \(d_1\), \(d_5\) | belegte Endwerte der Schadensfunktion: \(d_1 = 0{,}035\) bei \(h_1\), \(d_5 = 0{,}250\) bei \(h_5\) | – | herleitung: §3.3 — belegte Enden der Wasserstandsachse von FLEMOps, Langbeleg B5 (Thieken u. a. 2008, Tab. 1 und Fig. 1); Basiswert. Die Registerzeile 60-S093-01 trägt dieselbe Quelle, ihre Entscheidung „Sensitivitätsband“ gilt nur der Zustandsachse \(f_{S093}\) (Präambel Kap. 2) |
| \(e_{\text{bem}}\) | Schadensminderung am nachgerüsteten Gebäude unterhalb des Bemessungsniveaus | – | herleitung:#s092-wirkung — Abschätzung von KAP3 (§3.9), Wert 0,70 (Band 0,50–0,80) in §5.1.1/§5.1.2 |
| \(\text{EAD}\), \(\text{EAD}_z\), \(\text{EAD}_k\) | native Ergebnisgröße: jährlicher Erwartungsschaden des Kontos K3 aus flussseitiger Überflutung. Bezugsjahr und Preisstand **2026**; deklarierte Betrachtungsebene ist die **Kommune**, also \(\text{EAD} = \text{EAD}_k\); \(\text{EAD}_z\) ist das Zell-Zwischenergebnis und kein eigener Ausweis (§3.6) | €₂₀₂₆/a | herleitung: §3.1 (Deklaration) und §3.4 Schritt 3 — \(\text{EAD}_z = \bar A_z \cdot w_z\), Kommune als Summe über ihre Zellen (§3.6) |
| \(\text{EAD}_{\text{mit}}\) | Erwartungsschaden derselben Kommune, desselben Kontos K3 und desselben Bezugsjahres 2026 **nach** Umsetzung des Hebels S092; Betrachtungsebene Kommune | €₂₀₂₆/a | herleitung: §5.1 — \(\text{EAD}_{\text{mit}} = \text{EAD}\cdot(1 - r_{\text{S092}})\), Wirkungsort und Ausschluss der K8-Kosten dort begründet |
| \(f_{\text{AWM}}\) | Alterswertminderungsfaktor des Zeitwertansatzes: Verhältnis Restnutzungsdauer zu Gesamtnutzungsdauer; 0,55 (Band 0,40–0,75). Läuft nur als Sensitivitätsband (Ergebnis −45 %, §7.2) und geht nicht in den Basiswert ein; deshalb trägt er keinen eigenen Parameter-Block in Kap. 7 | – (Verhältnis RND/GND) | herleitung:#fortschreibung-neuwert-k3 — §7.2, Regel § 38 ImmoWertV mit GND 80 a (Anlage 1); Wert und Band sind Abschätzung von KAP3 (§3.9); Parameterzeile §4.8 |
| \(f_{S093}\), \(f_{S094}\) | geometrisch zentrierte Zustands- und Baustoffachse des Gebäudebestands | – | register: 60-S093-01 bzw. 60-S094-01 — Entscheidung Sensitivitätsband; in der Kernformel §3.4 stehen die Zeichen als neutral gesetztes Glied (Wert 1,00), das den Basiswert nicht verschiebt (Präambel Kap. 2); Ebene geparkt, Bänder 0,71–1,40 bzw. 0,84–1,18, gemeinsam 0,60–1,66 als Unsicherheitsbeitrag (§3.2) |
| \(h_1\), \(h_5\) | Grenzen des belegten Tiefenintervalls: 0,10 m und 1,75 m | m | herleitung: §3.3 — \(h_1\) Klassenmitte der untersten, \(h_5\) gesetzte Repräsentanz der offenen obersten FLEMOps-Klasse (Abschätzung von KAP3, §3.9) |
| \(h_{z,s}\), \(h\) | Wassertiefe der Zelle im Szenario \(s\); \(h\) ist dasselbe Zeichen als Argument der Schadensfunktion | m | register: 60-W085-01 — Ebene HQ_TIEFE, flächengewichtetes Mittel der LAWA-Klassenmitten (§3.2) |
| \(I_{60,k}\) | Schicht-A-Index „Betroffenheit durch Flusshochwasser" der Kommune, Skala 0–100 | Punkte (0–100) | herleitung: §3.7 — Perzentilrang von \(x_k\) im ausgewiesenen Vergleichsraum; kein Euro-Pfad |
| \(k\) | Laufindex der Kommune — die deklarierte Betrachtungsebene (§3.1) | — | Notation |
| \(k_{\text{BGF}}\) | Brutto-Grundfläche je m² Wohnfläche: 1,30 (Band 1,25–1,40) | m²/m² | herleitung: §3.4 Schritt 3 mit register: 60-R24-01 — Abschätzung von KAP3 (§3.9), Band aus der Spannweite kompakter bis gegliederter Bauformen |
| \(n\) | Zahl der kartierten Szenario-Stützstellen; hier \(n = 3\), \(p_n\) ist die kleinste davon (HQextrem) | — | Notation |
| \(n_t\) | Wertsatz je Gebäudetyp: 1.950 (EFH/ZFH), 1.533 (MFH) | €₂₀₂₆/m² BGF | register: 60-R24-01 — NHK 2010 nach ImmoWertV Anlage 4, mit Baupreisindex auf den Preisstand 2026 fortgeschrieben (Langbeleg B4); Umrechnungsfaktor NHK 2010 → Preisstand 2026: 1,6813 × 1,105 = **1,8578** (Blöcke `flood_bldg.n_efh_zfh` und `flood_bldg.n_mfh`, Kap. 7) |
| \(p_i\) (\(p_1\), \(p_2\), \(p_3\)) | jährliche Überschreitungswahrscheinlichkeit des Szenarios \(i\) | a⁻¹ | register: 60-W085-01 — \(p_1\), \(p_2\) belegt (Langbeleg B1); \(p_3\) herleitung: §3.4 Schritt 2, geometrisches Mittel der beiden Enden (Abschätzung von KAP3, §3.9) |
| \(q_0\) | heutiger Anteil exponierter Gebäude mit privatem Objektschutz (Ende 2024) — Referenzzustand des Doppelzählungs-Wächters (§5.1.2); bindet \(\Delta q \le 1 - q_0\), geht nicht in \(r_{\text{S092}}\) ein | – | herleitung:#q0-abschaetzung — Abschätzung von KAP3 (§3.9), 0,15 (Band 0,05–0,30); Datenebene geparkt (Datenquelle fehlt), Beschaffungs-Watchlist §4.7, Parameterzeile §4.8 |
| \(r_{\text{S092}}\) | relative Minderung des K3-Erwartungsschadens durch den Hebel S092 | – | herleitung:#s092-wirkung — Kette \(\Delta q \cdot s_{\text{bem}} \cdot e_{\text{bem}}\), Wert 0,035 (Band 0,0075–0,0832) in §5.1.1/§5.1.2 |
| \(s\), \(i\) | Laufindex des HQ-Szenarios (HQhäufig, HQ100, HQextrem); \(i\) ist derselbe Index in der Trapezsumme, absteigend nach \(p\) sortiert | — | Notation |
| \(s_{\text{bem}}\) | Anteil der Schadenssumme aus Ereignissen unterhalb des Bemessungsniveaus | – | herleitung:#s-bem-naeherung — Abschätzung von KAP3 (§3.9), ausgewiesene Näherung (Richtung: überschätzt den Hebel, §5.1.3), Wert 0,50 (Band 0,30–0,52, obere Bandgrenze aus dem Ankerwert der Verteilungsprüfung §4.5 mit 47,74 %, keine harte Grenze, §5.1.3) in §5.1.1/§5.1.2 |
| \(t\) | Laufindex des Gebäudetyps (EFH/ZFH, MFH) | — | Notation |
| \(T\) | Wiederkehrintervall eines Szenarios, \(T = 1/p\); für \(p_3\) rund 447 a | a | herleitung: §3.4 Schritt 2 — Kehrwert der Jährlichkeit, nur zur Lesbarkeit ausgewiesen |
| \(w\) (\(w_z\), \(w_{\text{Kommune}}\)) | Wertdichte — indexfrei \(w\) als Gattungszeichen, mit Index für die Zelle bzw. die Kommune. \(w_z\) ist der Preis, mit dem die physische Zwischengröße der Zelle bewertet wird; \(w_{\text{Kommune}}\) ist die wohnflächengewichtete Wertdichte der Kommune und erscheint nur im Vergleich in §3.1/§3.6. Der Euro-Ausweis der Kommune entsteht nicht aus \(\bar A_k \cdot w_{\text{Kommune}}\), sondern als Summe \(\sum_{z \in k} \bar A_z w_z\); der Quotient \(\text{EAD}_k / \bar A_k\) ist die mit \(\bar A_z\) gewichtete Wertdichte (§3.1) | €₂₀₂₆/m² Wohnfläche | herleitung: §3.4 Schritt 3 — \(w_z = k_{\text{BGF}} \sum_t \theta_{z,t} n_t\); \(w_{\text{Kommune}}\) als Mittel der \(w_z\), gewichtet mit der Wohnfläche \(W_z\) (§3.1, Golden-Test §3.6) |
| \(W_z\), \(W_k\) | Wohnfläche der Zelle \(z\) bzw. ihre Summe über alle Zellen der Kommune \(k\) | m² | register: 60-R24-01 — Ebene GEBAEUDEWERT aus dem Zensus-2022-100-m-Gitter (§3.2) |
| \(x_k\) | exponierter Wohnflächenanteil der Kommune im HQ100 — die einzige Eingangsgröße des Schicht-A-Index | – | herleitung: §3.7 — \(x_k = \sum_z W_z a_{z,\text{HQ100}} / W_k\) aus den Ebenen HQ_FLAECHE und GEBAEUDEWERT |
| \(z\) | Laufindex der 100-m-Zelle innerhalb der Kommune | — | Notation |
| \(\Delta q\) | zusätzlich nachgerüsteter Anteil exponierter Gebäude, marginal gegenüber heute | – | herleitung:#s092-wirkung — Abschätzung von KAP3 (§3.9), Wert 0,10 (Band 0,05–0,20) in §5.1.1/§5.1.2 |
| \(\theta_{z,t}\) | Anteil der Wohnfläche der Zelle, der auf den Gebäudetyp \(t\) entfällt; \(\sum_t \theta_{z,t} = 1\) | – | register: 60-R24-01 — Gebäudetyp des Zensus 2022 im 100-m-Gitter (§3.2) |
| \(\tau_i\) (\(\tau_1\), \(\tau_2\), \(\tau_3\)) | Beitrag eines Summanden der Trapezsumme (§3.4 Schritt 2) zur jährlich erwarteten schadensäquivalenten Wohnfläche der Beispielzelle: \(\tau_1\) zwischen HQhäufig und HQ100, \(\tau_2\) zwischen HQ100 und HQextrem, \(\tau_3\) jenseits HQextrem; \(\tau_1 + \tau_2 + \tau_3 = \bar A_z\). Nur in der Illustration zu \(s_{\text{bem}}\) verwendet | m²/a | herleitung:#s-bem-naeherung — §5.1.3, Werte 4,174 / 1,466 / 0,671 aus der Beispielzelle §3.4 |

### 3.6 Aggregation von der Zelle zur Kommune und Teil-Ausweise (§3.2/§3.6)

Gerechnet wird auf 100-m-Zellen, ausgewiesen wird die Kommune. Die Aggregation ist die
**einfache Summe über die Zellen der Kommune**, ohne Gewicht, ohne Skalar und ohne Rest aus einer
höheren Ebene:

$$ \bar A_k \;=\; \sum_{z \in k} \bar A_z \quad [\text{m}^2/\text{a}], \qquad \text{EAD}_k \;=\; \sum_{z \in k} \text{EAD}_z \;=\; \sum_{z \in k} \bar A_z \cdot w_z \quad [\text{€}_{2026}/\text{a}] $$

**Reihenfolge der Operationen.** Erwartungswertbildung (Schritt 2) und Aggregation sind beide
linear und deshalb vertauschbar: \(\sum_z \bar A_z\) ist identisch mit der Trapezsumme über die
zellsummierten Ereignisflächen \(\sum_z A_{z,s}\). Nichtlinear ist ausschließlich die
Schadensfunktion \(d(h)\) samt Deckelung — sie wird deshalb **immer auf der Zelle** ausgewertet und
**nie** auf einem Kommunenmittel der Wassertiefe. Ein kommunal gemitteltes \(h\) würde die
Krümmung von \(d\) glätten und in Kommunen mit wenigen tiefen und vielen flachen Zellen den
Schaden verzerren; die Formel sieht diesen Weg nicht vor.

**Geschlossene Betrachtungsebene (§3.2).** Jeder Zentrierungs-, Median- oder Mix-Rückgriff dieses
Kapitels bildet sich aus den **eigenen Zellen derselben Kommune**: der Tiefen-Median bei fehlender
Tiefenangabe (Ebene HQ_TIEFE) und der Gebäudetyp-Mix bei fehlender Typaufteilung (Ebene
GEBAEUDEWERT). Erst wenn die Kommune selbst keine Deckung hat, greift als zweiter Fallback eine
amtlich publizierte Verteilung des Bundeslandes — und dann als ausgewiesener Fallback, nicht als
stiller Standardwert. Ein Mittel über eine höhere Ebene wird an keiner Stelle gebildet und kein
nationaler Betrag wird auf Kommunen verteilt; der Lackmustest aus Abschnitt 3.4 bleibt dadurch
exakt erfüllt: Eine Kommune ohne Flussaue erhält 0, nicht einen kleinen Rest.

**Teil-Ausweise je Kommune.** Ausgewiesen werden vier Größen, jede mit ihrer eigenen Einheit, damit
der physische Teil nicht im Euro-Betrag verschwindet (§3.6):

1. **Physischer Teil-Ausweis:** \(\bar A_k\) in m²/a — die jährlich erwartete
   schadensäquivalente Wohnfläche der Kommune. \(\bar A_k\) und \(\text{EAD}_k\) sind über
   Kommunen hinweg **nicht proportional**, weil die Wertdichte am Gebäudetyp-Mix hängt: Die
   Wertsätze spannen 1.533…1.950 €₂₀₂₆/m² BGF, zwei Kommunen mit gleichem \(\bar A_k\) können
   deshalb bis zu rund 21 % verschiedene Euro-Ausweise tragen (Beispiel mit gemischtem Typ-Mix im
   Golden-Test unten: 10,5 % bezogen auf \(\text{EAD}_k\); §3.1, Modellgrenze).
2. **Exponierte Wohnfläche je Szenario:** \(\sum_{z \in k} W_z\,a_{z,s}\) in m², getrennt für
   HQhäufig, HQ100 und HQextrem. Diese Größe ist reine Exposition, ohne Schadensquote und ohne
   Preis, und damit die Zahl, die sich unmittelbar gegen die Hochwassergefahrenkarte prüfen lässt.
3. **Monetärer Ausweis:** \(\text{EAD}_k\) in €₂₀₂₆/a, benannt als „bewerteter Schaden — Konto K3",
   mit dem Vermerk, dass K1, K4, K5 und K8 nicht enthalten sind (Untergrenze, §3.6).
4. **Szenario-Beiträge:** der Anteil jedes Szenarios an \(\bar A_k\) beziehungsweise
   \(\text{EAD}_k\). Er zeigt, ob eine Kommune ihren Erwartungsschaden aus häufigen flachen oder
   aus seltenen tiefen Ereignissen bezieht — dieselbe Information, die Abschnitt 5.1.2 für
   \(s_{\text{bem}}\) heute abschätzen muss und später messen kann.

**Vollständigkeitsanzeige.** Zu jedem Ausweis gehört der Anteil der Wohnfläche der Kommune in
Zellen **ohne Kartenabdeckung** (\(a_{z,s}\) nachrichtlich „nicht kartiert", §3.2). Er ist kein
Schaden und wird nicht hochgerechnet, sondern als Deckungsgrad des Ausweises angezeigt: Ein
niedriger Deckungsgrad bedeutet, dass die ausgewiesene Untergrenze weiter unten liegt als in einer
vollständig kartierten Kommune.

**Kein Ausweis unterhalb der Kommune.** \(\text{EAD}_z\) und \(A_{z,s}\) sind Zwischenergebnisse.
Sie werden nicht je Zelle publiziert, weil die Genauigkeit der Gefahrenkarten und der
Zensus-Gitterwerte auf der einzelnen 100-m-Zelle deutlich geringer ist als im kommunalen Summenwert
(Zufallsrundung im Gitter, Kartenkanten). Aggregate **oberhalb** der Kommune (Kreis, Land) entstehen
ausschließlich als Summe der \(\text{EAD}_k\), nie als Mittel von Indexwerten.

**Ressourcen-Regel (§3.4).** Die Summe läuft über die Zellen genau der Kommune, die berechnet wird;
kein Schritt dieses Abschnitts verlangt einen nationalen 100-m-Vollraster-Lauf. Das folgende
Beispiel rechnet dementsprechend eine einzelne Zelle und eine Kommune aus zwei Zellen durch.

```python test: beispiel_60_kernformel
# Kernformel aus 3.4 an einer Beispielzelle, danach Aggregation auf die Kommune (3.6).
d1, d5, h1, h5 = 0.035, 0.250, 0.10, 1.75
d = lambda h: d1 * (d5 / d1) ** ((min(max(h, h1), h5) - h1) / (h5 - h1))
p = [1.0e-1, 1.0e-2, (5.0e-3 * 1.0e-3) ** 0.5]   # HQhaeufig, HQ100, HQextrem
k_bgf, n_efh = 1.30, 1950.0                      # Preisstand 2026 (Register 60-R24-01)

def zelle(W, theta_efh, szenarien, f093=1.00, f094=1.00):
    """Schritt 1 Menge x Rate [m2] -> Schritt 2 Erwartungswert [m2/a] -> Schritt 3 Preis [EUR/a]."""
    A = [W * a * q * f093 * f094 for a, q in szenarien]
    A_bar = (sum((p[i] - p[i + 1]) * (A[i] + A[i + 1]) / 2 for i in range(len(p) - 1))
             + p[-1] * A[-1])
    w = k_bgf * theta_efh * n_efh                # reines EFH/ZFH-Gebiet: theta_EFH = 1,0
    return A, A_bar, A_bar * w

# Die gerundeten Quoten der Stuetzstellentabelle 3.3 stimmen mit d(h) ueberein,
# die oberste Zelle liegt oberhalb h5 und ist deshalb gedeckelt.
assert abs(d(0.405) - 0.050) < 5e-4 and abs(d(0.805) - 0.081) < 5e-4
assert d(1.80) == 0.250
A1, A1_bar, ead_z1 = zelle(1200.0, 1.0, ((0.25, 0.050), (0.80, 0.081), (1.00, 0.250)))
assert [round(x, 2) for x in A1] == [15.0, 77.76, 300.0]   # physische Zwischengroesse [m2]
assert abs(A1_bar - 6.311) < 1e-3                          # [m2/a]
assert abs(ead_z1 - 16000.0) < 1.0                         # [EUR2026/a]

# Zweite Zelle der Kommune liegt ausserhalb der Aue: a = 0 in jedem Szenario -> exakt 0
A2, A2_bar, ead_z2 = zelle(800.0, 1.0, ((0.0, 0.050), (0.0, 0.081), (0.0, 0.250)))
assert A2_bar == 0.0 and ead_z2 == 0.0

# Aggregation Zelle -> Kommune: einfache Summe, kein Rest aus einer hoeheren Ebene
A_bar_k = A1_bar + A2_bar
ead_k = ead_z1 + ead_z2
assert abs(ead_k - 16000.0) < 1.0
# Linearitaet: Erwartungswert und Aggregation sind vertauschbar (gleiche Wertdichte)
assert abs(ead_k - A_bar_k * k_bgf * n_efh) < 1e-9

# Schicht-A-Index (3.7): dimensionsloser Anteil, der in keinen Euro-Wert eingeht
W_k = 1200.0 + 800.0
x_k = (1200.0 * 0.80 + 800.0 * 0.0) / W_k
assert abs(x_k - 0.48) < 1e-12 and 0.0 <= x_k <= 1.0
assert abs(ead_k - A_bar_k * k_bgf * n_efh) < 1e-9         # unveraendert ohne x_k

# Gemischter Gebaeudetyp (3.1 Modellgrenze): EFH-Zelle und MFH-Zelle in einer Kommune.
# Auf der Zelle gilt EAD_z = A_bar_z * w_z, auf der Kommune nur die Summe -> nicht proportional.
n_mfh = 1533.0
B1, B1_bar, _ = zelle(1200.0, 1.0, ((0.25, 0.050), (0.80, 0.081), (1.00, 0.250)))
B2, B2_bar, _ = zelle(3000.0, 1.0, ((0.00, 0.050), (0.10, 0.081), (0.20, 0.250)))
ead_mix = B1_bar * k_bgf * n_efh + B2_bar * k_bgf * n_mfh    # Summe ueber die Zellen
w_mix = k_bgf * (1200.0 * n_efh + 3000.0 * n_mfh) / 4200.0   # wohnflaechengewichtete Wertdichte
assert abs(ead_mix - 20195.7) < 0.1
assert abs((B1_bar + B2_bar) * w_mix - 18077.9) < 0.1
assert abs(ead_mix - (B1_bar + B2_bar) * w_mix) / ead_mix > 0.10   # 10,5 % bezogen auf EAD_k
```

### 3.7 Schicht-A-Index — getrennt vom Euro-Pfad (§3.2/§3.6)

Neben dem bewerteten Schaden führt das Produkt für dieses Risiko einen **Schicht-A-Index**
\(I_{60,k}\): eine Betroffenheitskennzahl auf der Skala 0–100, die Kommunen **vergleichbar** macht,
ohne einen Geldbetrag zu behaupten. Er ist hier bewusst in einem eigenen Abschnitt beschrieben,
weil er eine andere Konstruktion, eine andere Einheit und eine andere Lesart hat als
\(\text{EAD}_k\).

**Konstruktion.** Eingangsgröße ist genau eine Größe, der exponierte Wohnflächenanteil im HQ100:

$$ x_k \;=\; \frac{\sum_{z \in k} W_z\,a_{z,\text{HQ100}}}{W_k} \quad [-], \qquad I_{60,k} \;=\; 100 \cdot \operatorname{Perzentilrang}\bigl(x_k\bigr) \quad [\text{Punkte}] $$

Der Perzentilrang wird über einen **ausgewiesenen Vergleichsraum** gebildet — alle Kommunen, für
die dieselbe Kartengrundlage vorliegt —, und der Vergleichsraum steht am Indexwert. Ohne diese
Angabe ist ein Rang bedeutungslos: Dieselbe Kommune erhält im Bundesvergleich einen anderen Rang
als im Landesvergleich.

**Nullanker und Bindungsregel.** Kommunen mit \(x_k = 0\) (keine exponierte Wohnfläche im HQ100)
erhalten den Indexwert \(I_{60,k} = 0\) und gehören nicht zum Vergleichsraum; der Perzentilrang
wird nur über die Kommunen mit \(x_k > 0\) gebildet, gleiche Werte erhalten den mittleren Rang
(Durchschnittsrang). Damit hängt der Indexwert einer Kommune ohne Aue an keiner Rangkonvention, und
der Lackmustest aus §3.4 gilt auch für diesen Ausweis: Eine Kommune ohne Flussaue trägt
\(\text{EAD}_k = 0\) €₂₀₂₆/a **und** \(I_{60,k} = 0\). Bei 100 Kommunen, davon 60 mit
\(x_k = 0\), erhalten die 60 Kommunen 0 Punkte und die übrigen 40 ihren Rang unter sich.

**Warum getrennt vom Euro-Pfad.** \(I_{60,k}\) ist eine **Ordnungsgröße**. Sie enthält keine
Schadensquote, keinen Preis und keine Jährlichkeit; ein doppelt so hoher Indexwert bedeutet
keinen doppelt so hohen Schaden, und Indexwerte lassen sich nicht addieren. Der Perzentilrang
bezieht sich zudem notwendig auf eine Menge **anderer** Kommunen und verlässt damit die
geschlossene Betrachtungsebene, die für die Euro-Rechnung nach §3.2 gilt. **Der Schicht-A-Index
wird nie auf Euro-Pfaden verwendet.** Konkret heißt das: \(I_{60,k}\) geht in keine Formel dieses
Kapitels ein, wird nicht mit \(\text{EAD}\) oder \(\text{EAD}_{\text{mit}}\) multipliziert, nicht
zur Verteilung nationaler Beträge auf Kommunen benutzt und nicht als Gewicht in der Aggregation
nach Abschnitt 3.6 verwendet; umgekehrt fließt kein Euro-Betrag in \(I_{60,k}\) ein. Die beiden
Pfade teilen sich ausschließlich die Datenebenen HQ_FLAECHE und GEBAEUDEWERT.

**Anzeige und Grenzen.** Der Index wird getrennt vom Euro-Ausweis angezeigt, mit dem
Vergleichsraum, dem Kartenstand und derselben Vollständigkeitsanzeige wie in Abschnitt 3.6. Seine
Grenzen: Er bildet nur die Exposition im HQ100 ab, nicht die Tiefe und nicht den Gebäudewert; zwei
Kommunen mit gleichem \(x_k\), aber sehr verschiedenen Wassertiefen erhalten denselben Indexwert
und deutlich verschiedene \(\text{EAD}_k\). Genau deshalb ersetzt er den bewerteten Schaden nicht,
sondern steht neben ihm.

## 4 Kalibrierung & Validierung (§2.4/§3.4)

Kalibriert wird das Niveau, geprüft wird die Verteilung. Beides ist getrennt: Das Niveau wird über
**genau einen** nationalen Skalar \(\lambda\) an einen benannten Anker gebunden (§2.4: ein
Niveau-Skalar, nicht mehrere), und die Verteilung über die Ereignisse wird gegen eine Größe
geprüft, die in die Bestimmung von \(\lambda\) **nicht** eingeht.

**Stand nach dem Stichprobenlauf — \(\lambda\) ist gesetzt und bleibt vorläufig.** §2.4 verlangt,
dass der Kalibrierlauf mit dem Produktionsmodell gerechnet wird. Diese Fassung erfüllt das: Die
Modellsumme \(M_0\) in 4.3 entsteht aus den Jahresschadensraten, die das Produktionsmodell auf den
acht Anker-Kommunen je ZÜRS-Klasse gemessen hat
(`docs/evidenz/60_stichprobe/m0_klassenraten.csv`), hochgerechnet über das nationale Mengengerüst
der ZÜRS-Klassen **einschließlich GK2** und um den Wohngebäudeanteil je Adresse (0,872) bereinigt —
kein Vollraster-Lauf nach §3.4. Die beiden Umfangsunterschiede zu \(A^{*}\), die die vorige Fassung
nur beziffert hatte (fehlende Klasse GK2, alle Adressen als Wohngebäude gezählt), sind damit
geschlossen. Bemerkenswert und hier festgehalten: Die damals angegebene Umfangs-Sensitivität sagte
einen Wert zwischen 0,97 und 0,55 voraus — das jetzt gerechnete \(\lambda\) = 0,911 liegt
innerhalb dieser Spanne. **Wertsatz typgewichtet (Ledger-Befund 58).** Seit dieser Revision
bewertet auch der Kalibrierlauf jedes exponierte Wohngebäude mit dem typgewichteten Wertsatz des
Produktionsmodells (\(\bar\theta\) = 0,596 EFH/ZFH, §4.3) statt mit dem reinen EFH/ZFH-Satz; das
senkt \(M_0\) von 1,360 auf 1,243 Mrd. €₂₀₂₆/a und hebt \(\lambda\) von 0,832 auf 0,911.
**Richtung des verbleibenden Fehlers (Vorläufigkeitsvermerk):** Der Typ-Mix ist der bundesweite
Bestandsmix, nicht der Mix der **exponierten** Teilmenge, der nicht gemessen ist. Liegt in den
Flussauen mehr MFH-Wohnfläche als im Bundesmittel, ist \(M_0\) weiter zu hoch und \(\lambda\) zu
niedrig — im Randfall eines reinen MFH-Bestands \(\lambda\) = 1,132/1,069 ≈ 1,06; liegt dort mehr EFH/ZFH-Fläche,
gilt das Umgekehrte bis zum Randfall \(\lambda\) = 0,832 (reiner EFH/ZFH-Satz). \(\lambda\) bleibt dennoch **vorläufig** und trägt im Produkt diesen
Vermerk (Block `flood_bldg.lambda`, Feld `vorlaeufig: true`), weil die Verteilungsprüfung in 4.5
seit dieser Revision außerhalb der Anpassungsdaten liegt und dort **nicht bestanden** wird
(Modellentscheid, Ledger-Befund 33); der Produkt-Block in Kap. 7 trägt zum Stand dieser Revision denselben
Wert.

<a id="anker-gdv"></a>

### 4.1 Nationaler Anker: GDV-Naturgefahrenstatistik, Teilreihe Überschwemmung/Starkregen

**Anker \(A_{\text{ver}}\) (namentlich).** Die jährlich veröffentlichte
**GDV-Naturgefahrenstatistik** (Gesamtverband der Deutschen Versicherer), Teilreihe **„Starkregen
und Überschwemmung" in der Sachversicherung**, ausgewiesen im *Datenservice zum
Naturgefahrenreport*. Sie ist der einzige bundesweit durchgehend geführte Schadensdatensatz zu
Überflutungsschäden an Gebäuden; eine amtliche Hochwasser-Schadensbilanz des Bundes mit
Jahreswerten existiert nicht (die Wiederaufbaufonds nach 2002, 2013 und 2021 sind Ereignis-, keine
Zeitreihenwerte und werden deshalb nicht als Anker verwendet).

- **Zeitreihe.** Elementargefahren in der Sachversicherung werden **seit 2002** erhoben (Sturm und
  Hagel seit 1973). Die Reihe ist damit 23 abgeschlossene Schadenjahre lang (2002–2024).
- **Revisionsstand.** Verwendet wird der Stand *Datenservice zum Naturgefahrenreport 2025*;
  Aktualisierungsvermerke der genutzten Grafiken: **10.10.2025** (Elementarschäden an Wohngebäuden
  nach Bundesländern) und **30.12.2025** (Übersichtsreihe, „bezogen auf Bestand und Preise 2024"
  — die Reihe ist also bestands- und preisnormiert, nicht nominal).
- **Vorläufige Jahre gesondert.** Das Schadenjahr **2025** liegt nur als vorläufige Mitteilung vor
  (Sachversicherung 1,4 Mrd. € Naturgefahren) und geht in die Kalibrierung **nicht** ein; es dient
  ausschließlich als nachlaufende Kontrolle.
- **Ankerwert.** Für 2024 nennt der GDV **2,6 Mrd. €** versicherte Schäden durch Starkregen und
  Überschwemmung, „rund eine Milliarde Euro mehr als im langjährigen Durchschnitt". Daraus folgt
  der hier verwendete Mittelwert der Reihe: \(A_{\text{ver}}\) = **1,838 Mrd. €** je Jahr
  (Bestands-/Preisstand 2024, arithmetisches Mittel der 23 Jahreswerte 2002–2024,
  `docs/evidenz/60_gdv_jahresreihe_2002_2024.csv`), **Band 1,061–1,838 Mrd. €** — uniform
  angewandter Ausreißer-Test nach Tukey auf die 23-Jahre-Reihe, extrem sind 2002 und 2021; die
  ausführliche Herleitung des Mittelwerts, der Jahres-Auswahlregel und des Tukey-Tests steht in 4.1a. Quelle: GDV, „GDV-Naturgefahrenstatistik 2024: Hochwasserschäden mehr als
  verdoppelt" (Medieninformation), sowie GDV, „Versicherungsquote bei Elementarschadenversicherung
  steigt kontinuierlich" (Datenservice, Versicherungsdichte 2024: 57 %, 10,2 Mio. versicherte
  Wohngebäude) — Zugriff 13.09.2026; vollständige Belege in Kap. 8.

**Was der Anker nicht ist.** Er misst *gezahlte Versicherungsleistungen* für *alle*
Überschwemmungen (fluvial **und** pluvial) in *allen* Sachsparten. Der Berichtsgegenstand von #60
ist enger (Wohngebäude, flussseitig) und zugleich weiter (auch nicht versicherte Schäden). Die
Lücke wird nicht weggerundet, sondern in 4.2 Schritt für Schritt überbrückt.

### 4.1a Kleinste-Quadrate-Herleitung, Jahres-Auswahlregel und Fenster-Sensitivität (Ledger-Befund 34)

**Warum eine Kleinste-Quadrate-Bestimmung.** §3.4 verlangt, dass \(\lambda\) über eine
**Kleinste Quadrate**-Bestimmung aus der Anker-Zeitreihe folgt, nicht aus einem einzelnen Jahr
oder einer einzelnen Medienangabe. Für jedes Kalibrierjahr \(t\) der gewählten Jahresmenge \(T\)
trägt die Modellsumme \(M_t\) und die (auf den Modellumfang übertragene) Ankerangabe \(A_t\);
\(\lambda\) minimiert die Fehlerquadratsumme
\[
S(\lambda) = \sum_{t \in T} (A_t - \lambda M_t)^2 .
\]
Die Bedingung erster Ordnung liefert
\[
\frac{dS}{d\lambda} = -2 \sum_{t \in T} M_t (A_t - \lambda M_t) = 0
\;\Longrightarrow\;
\lambda \sum_{t \in T} M_t^2 = \sum_{t \in T} M_t A_t .
\]
Dieser Bericht rechnet mit **einer** national konstanten Modellsumme \(M_0\) (§4.3: kein
Jahres-Lauf des Produktionsmodells, \(M_t \equiv M_0\) für alle \(t\)). Eingesetzt:
\[
\lambda \sum_{t \in T} M_0^2 = M_0 \sum_{t \in T} A_t
\;\Longrightarrow\;
\lambda \cdot |T| \cdot M_0^2 = M_0 \sum_{t \in T} A_t
\;\Longrightarrow\;
\lambda = \frac{\sum_{t \in T} A_t}{|T| \cdot M_0} = \frac{\text{Mittel}(A_t)}{M_0} .
\]
Bei zeitkonstanter Modellsumme fällt der Kleinste-Quadrate-Schätzer also auf das arithmetische
Mittel der Ankerreihe geteilt durch \(M_0\) zusammen. Das ist der Grund, warum der in 4.1
verwendete Ankerwert \(A_{\text{ver}}\) nicht mehr aus dem Einzeljahr 2024 kommt, sondern aus dem
Mittel der Jahresreihe: Die einfache Formel ist keine Abkürzung, sondern das Ergebnis der
Kleinste-Quadrate-Bestimmung unter der (in 4.3 begründeten) Annahme einer zeitkonstanten
Modellsumme.

**Jahres-Auswahlregel.** §3.4 verlangt eine **einheitliche Auswahlregel** statt einer Auswahl nach
Ergebnis. Die hier festgelegte Regel: Hauptfenster ist die **vollständige, abgeschlossene Reihe
2002–2024** (23 Jahre, §4.1), ohne ein einzelnes Jahr auszulassen — auch das Jahr 2009 bleibt drin,
obwohl seine Lesart in `docs/evidenz/60_gdv_jahresreihe_2002_2024.csv` (Spalte `lesart`) als
„Abschätzung KAP3" statt als direkt abgelesener Grafikwert ausgewiesen ist: Die abweichende Lesart
betrifft nur, **wie** der Jahreswert 2009 gewonnen wurde (Grafik-Interpolation aus den
Nachbarjahren statt Direktablesung), nicht, **ob** er zur Reihe zählt — eine begründete Abschätzung
eines fehlenden Einzelwerts ist kein Ausreißer und wird nicht gesondert behandelt. Die Regel gilt
**ergebnisunabhängig**: Sie ist unabhängig davon festgelegt, welches Zeitfenster das für den
Bericht günstigste \(\lambda\) liefert.

**Sensitivität je Zeitfenster.** Neben dem Hauptfenster laufen drei weitere Zeitfenster als
Sensitivität mit (Mittelwert \(A_{\text{ver}}\) je Fenster aus
`docs/evidenz/60_gdv_jahresreihe_2002_2024.csv`, Spalte `wert_mrd_eur`; Folgefaktoren wie 4.2:
\(w_{\text{wg}} \cdot u \cdot \varphi_{\text{fluss}} \cdot \kappa \cdot \pi = 0{,}65 \cdot 1{,}54
\cdot 0{,}50 \cdot 1{,}15 \cdot 1{,}07 = 0{,}615865\); \(M_0\) = 1,243 Mrd. €₂₀₂₆/a unverändert,
§4.3):

| Zeitfenster | Jahre (n) | \(A_{\text{ver}}\) (Mrd. €) | \(A^{*}\) (Mrd. €₂₀₂₆/a) | \(\lambda = A^{*}/M_0\) |
|---|---|---|---|---|
| 2002–2024 (Hauptfenster) | 23 | **1,838** | 1,132 | **0,911** |
| 2014–2024 | 11 | **2,064** | 1,271 | **1,023** |
| 2002–2024 ohne 2021 | 22 | **1,349** | 0,831 | **0,669** |
| 2014–2024 ohne 2021 | 10 | **1,010** | 0,622 | **0,500** |

Gegen die Plausibilitätsschranke [0,5; 2,0] aus §4.4 (Abschätzung von KAP3, seit T-0574 getrennt
vom Unsicherheitsband [0,12; 3,93]) liegen **alle vier** \(\lambda\)-Werte innerhalb — das kürzeste
Fenster (2014–2024 ohne 2021, \(\lambda\) = 0,500) nur knapp am unteren Rand. Die Schranke trägt die
Wahl des Hauptfensters damit nicht als zweiten Grund; sie stützt sich
**allein** auf die ergebnisunabhängige Auswahlregel oben, die unabhängig davon feststeht, welches
der vier geprüften Fenster das für den Bericht günstigste \(\lambda\) liefert.

**Herleitung des Ausreißerbands (Tukey-Fence).** Statt ein einzelnes Jahr freihändig als „den"
Ausreißer zu benennen, wird ein benannter, uniform auf die gesamte Hauptfenster-Reihe angewandter
Ausreißertest verwendet: die Tukey-Fence (Whisker-Regel des Boxplots). Aus der sortierten
23-Jahre-Reihe (`docs/evidenz/60_gdv_jahresreihe_2002_2024.csv`): \(Q_1\) = 0,5, \(Q_3\) = 1,5,
\(IQR = Q_3 - Q_1\) = 1,0 (Mrd. €). Werte oberhalb der extremen Schwelle \(Q_3 + 3 \cdot IQR\) =
4,5 Mrd. € gelten als extrem. Das trifft auf zwei Jahre zu: **2002** (7,4 Mrd. €) und **2021**
(12,6 Mrd. €). Das Jahr 2013 (3,9 Mrd. €) liegt zwischen der milden Schwelle \(Q_3 + 1{,}5 \cdot
IQR\) = 3,0 und der extremen Schwelle 4,5 und bleibt damit in der Reihe. Die Untergrenze des
in 4.1 genannten Bands ist das Mittel der 21 verbleibenden Jahre ohne 2002 und 2021 = **1,061**
Mrd. €; die Obergrenze bleibt der Zentralwert des Hauptfensters (alle 23 Jahre) = **1,838** Mrd. €.
Der Tukey-Fence-Test liefert damit das Band von \(A_{\text{ver}}\) (1,061–1,838 Mrd. €), **nicht**
das Band von \(\lambda\): Dieses folgt aus der vollständigen Bandfortpflanzung von \(A^{*}\) und
\(M_0\) in §4.4 (0,12–3,93); ein früher an diese Herleitung geknüpftes \(\lambda\)-Band ist damit
abgelöst (Ledger-Befunde 34 und 91). Das \(A_{\text{ver}}\)-Band ist von der Fenster-Sensitivität oben zu unterscheiden: Dort wird bei fester
Auswahlregel gezielt die Fensterlänge variiert bzw. nur 2021 herausgerechnet, um die Sensitivität
je Zeitfenster offenzulegen (keine Bandbreite des Zentralwerts) — der dort verwendete Wert 1,349
(2002–2024 ohne 2021) ist deshalb bewusst nicht mit dem hier hergeleiteten Wert 1,061 (2002–2024
ohne 2002 **und** 2021, nach dem Ausreißertest) zu verwechseln.

**Stand von \(w_{\text{wg}}\).** `docs/evidenz/60_gdv_wohngebaeude_2024.csv` dokumentiert, dass die
GDV-Bundesländer-Grafik zu Elementarschäden an Wohngebäuden nur Verhältniszahlen (Schadensatz,
Schadenhäufigkeit, Schadendurchschnitt je Bundesland) führt, aber weder den Zähler
(Wohngebäude-Elementarschaden in Euro) noch einen jahresgleichen Nenner (Sach-Elementarschaden
gesamt) liefert, aus denen sich ein Anteil errechnen ließe (Zeile `w_wg`, Spalte `lesart`: „nicht
ablesbar"). \(w_{\text{wg}}\) = 0,65 (Band 0,55–0,75) bleibt deshalb weiterhin eine **Abschätzung
von KAP3** (Herleitung 4.2); die Datei belegt nur, dass die genannte Grafik diese Abschätzung nicht
durch eine Messung ersetzen kann, und ändert keinen der fünf Faktoren aus 4.2.

<a id="kalibrierung-zielwert"></a>
### 4.2 Vom Anker zum Modellumfang — Zielwert der Bundessumme

\(A^{*} = A_{\text{ver}} \cdot w_{\text{wg}} \cdot u \cdot \varphi_{\text{fluss}} \cdot \kappa \cdot \pi\)

| Schritt | Zeichen | Wert (Band) | Herkunft |
|---|---|---|---|
| Anker, Mittel 2002–2024 | \(A_{\text{ver}}\) | 1,838 Mrd. € (1,061–1,838) | **Quelle:** GDV-Naturgefahrenstatistik 2024 (§4.1) |
| Anteil Wohngebäude an der Sach-Schadensumme | \(w_{\text{wg}}\) | 0,65 (0,55–0,75) | **Abschätzung von KAP3** (§3.9), Herleitung unten |
| Hochrechnung auf den unversicherten Bestand | \(u\) | 1,54 (1,33–1,75) | **Abschätzung von KAP3** aus der belegten Versicherungsdichte 57 % |
| Anteil flussseitig an Starkregen + Überschwemmung | \(\varphi_{\text{fluss}}\) | 0,50 (0,35–0,65) | **Abschätzung von KAP3** (§3.9), Herleitung unten |
| Leistung → Wiederherstellungskosten | \(\kappa\) | 1,15 (1,05–1,30) | **Abschätzung von KAP3** (§3.9), Herleitung unten |
| Preisstand 2024 → 2026 | \(\pi\) | 1,07 (1,039–1,124) | **Abschätzung von KAP3**, abgeleitet aus B4 (Register 60-R24-01) |

**Herleitung der vier abgeschätzten Faktoren** (alle vier sind Abschätzungen von KAP3, keine
Primärquelle; sie werden im Produkt nach Vorgabe P1 mit genau dieser Herleitung ausgewiesen):

- \(w_{\text{wg}}\) = 0,65. 2024 entfielen von 5,7 Mrd. € versicherten Naturgefahrenschäden
  4,4 Mrd. € auf die Sachversicherung und 1,3 Mrd. € auf Kraftfahrt (GDV, §4.1). Innerhalb der
  Sachversicherung trägt die Wohngebäudeversicherung den größten Teil, weil die Gebäudesubstanz
  die teuerste betroffene Position ist; Hausrat sowie Gewerbe/Industrie teilen sich den Rest.
  Untergrenze 0,55 (Gewerbeanteil hoch), Obergrenze 0,75 (Gewerbeanteil niedrig). Eine
  spartenscharfe Aufteilung der Teilreihe ist nicht publiziert — deshalb abgeschätzt.
- \(u\) = 1,54 = \(1/0{,}65\). Belegt ist eine Versicherungsdichte Elementar von **57 %**
  (10,2 Mio. von 19,7 Mio. Wohngebäuden, Stand 2024; 2017: 41 %). Der Deckungsgrad **exponierter**
  Gebäude liegt darüber, weil betroffene Regionen deutlich höhere Quoten erreichen (Baden-
  Württemberg historisch 94 %, Rheinland-Pfalz nach 2021 von 37 % auf 59 %). Deshalb wird nicht
  mit 0,57, sondern mit einem effektiven Deckungsgrad 0,65 gerechnet; Band 0,57 (keine
  Selbstselektion, \(u\) = 1,75) bis 0,75 (starke Selbstselektion, \(u\) = 1,33).
- \(\varphi_{\text{fluss}}\) = 0,50. Der GDV führt Starkregen und Überschwemmung in **einer**
  Position. #60 rechnet nur flussseitige Überflutung; Sturzfluten und Kanalrückstau sind W087 bzw.
  W100 und gehören nicht hierher. Für eine hälftige Teilung spricht, dass die Spitzenjahre beide
  Regime abbilden: 2024 dominierte das Juni-Hochwasser in Bayern und Baden-Württemberg (je
  ≈ 1,6 Mrd. € Landesschaden, flussseitig), 2021 die Sturzflut „Bernd" (pluvial). Band 0,35–0,65.
- \(\kappa\) = 1,15. Gezahlte Leistungen liegen unter den Wiederherstellungskosten
  (Selbstbehalte, Unterversicherung, nicht gedeckte Positionen), aber nicht weit darunter, weil
  Wohngebäudeverträge zum gleitenden Neuwert decken. Band 1,05–1,30. Gegenrichtung ausdrücklich
  benannt: Regulierungskosten und Kulanz wirken umgekehrt, deshalb kein höherer Zentralwert.
- \(\pi\) = 1,07. Das Register führt für 2023 → 2026 den Baupreisfaktor 1,105 (B4, Band
  1,07–1,16). Abzüglich rund 3 % Baupreisanstieg 2023 → 2024 ergibt sich \(1{,}105/1{,}03 \approx
  1{,}073\). Das Band ist aus dem ungerundeten B4-Band (1,023³ = 1,0706 bis 1,050³ = 1,1576,
  Langbeleg B4, Rechenschritt 2) mit derselben Division gerechnet: \(1{,}0706/1{,}03 = 1{,}039\)
  bis \(1{,}1576/1{,}03 = 1{,}124\) ⇒ **Band 1,039–1,124**. \(\pi\) ist damit ein abgeleiteter
  Parameter: Zentralwert und beide Bandenden folgen aus B4, abgeschätzt sind allein die
  B4-Jahresraten und der 3-%-Schritt 2023 → 2024 (Parameterliste §4.8).

**Zielwert.** \(A^{*}\) = 1,838 · 0,65 · 1,54 · 0,50 · 1,15 · 1,07 = **1,132 Mrd. €₂₀₂₆/a**
(Band, alle Enden gleichgerichtet: **0,30–2,29 Mrd. €₂₀₂₆/a**). Das ist der bundesweite
Erwartungsschaden des Kontos K3 an Wohngebäuden aus flussseitiger Überflutung, den der Anker nahe
legt — die Größe, gegen die die Modellsumme gestellt wird.

<a id="modellsumme-m0"></a>

### 4.3 Modellsumme vor Kalibrierung — und die verwendete Auflösung (§3.4)

Die unkalibrierte Bundessumme \(M_0\) entsteht aus drei Größen: dem Mengengerüst der ZÜRS-Klassen,
dem Wert je exponiertem Wohngebäude und den **gemessenen** Jahresschadensraten je Klasse aus dem
Stichprobenlauf auf den acht Anker-Kommunen.

1. **Exponierte Wohngebäude-Adressen je ZÜRS-Klasse:** 339.000 Adressen in **GK3+GK4** und
   1,38 Mio. Adressen in **GK2** (6,1 % von 22,6 Mio. Adressen; Register 60-R17-01, **Quelle**).
   GK2 wird mitgerechnet, weil die Klasse im Modell bei HQextrem nass ist. Modellgrenze: Adressen
   sind keine Gebäude, ein Gebäude je Adresse ist eine Untergrenze.
2. **Wert je exponiertem Wohngebäude und Wohngebäudeanteil:** Wie im Produktionsmodell
   (§3.4, \(w_z = k_{\text{BGF}} \sum_t \theta_{z,t} n_t\)) wird der Wertsatz nach dem
   Gebäudetyp gewichtet, hier mit dem **nationalen Typ-Mix** \(\bar\theta\) als Wohnflächenanteil:
   \(\bar\theta_{\text{EFH/ZFH}}\) = **0,596** und \(\bar\theta_{\text{MFH}}\) = 1 − 0,596 = **0,404**
   (**Quelle:** Destatis, Bestand und Bauabgang von Wohnungen und Wohngebäuden 2021, Tabelle 2.1.3,
   Stichtag 31.12.2021, Deutschland: Wohnfläche in Wohngebäuden mit 1 Wohnung 1.676.403 und mit
   2 Wohnungen 612.785 von zusammen 3.841.438 Tsd. m² ⇒ 2.289.188/3.841.438 = 0,5959 → 0,596;
   Wohngebäude mit 3 oder mehr Wohnungen und Wohnheime bilden den MFH-Anteil;
   `docs/evidenz/60_destatis_wohnflaeche_gebaeudetyp_2021.csv`). Typgewichteter Wertsatz:
   \(\bar n = \bar\theta_{\text{EFH/ZFH}}\, n_{\text{EFH/ZFH}} + \bar\theta_{\text{MFH}}\, n_{\text{MFH}}\)
   = 0,596 · 1.950 + 0,404 · 1.533 = **1.781,532 €₂₀₂₆/m² BGF**; Wert je exponiertem Wohngebäude
   208 m² Wohnfläche · 1,30 BGF/Wohnfläche · 1.781,532 €₂₀₂₆/m² BGF = **481.726,25 €₂₀₂₆**
   (Wertsätze und BGF-Faktor: Register 60-R24-01). Wohnfläche 208 m² und Typ-Mix beziehen sich
   damit auf **dieselbe** Grundgesamtheit (alle Wohngebäude): \(\sum_t W_t n_t = W \sum_t
   \bar\theta_t n_t\). **Modellgrenze:** \(\bar\theta\) ist der Bestandsmix des Bundes, nicht der
   der exponierten Teilmenge (nicht gemessen). Die Quelle ist die Bestandsfortschreibung auf Basis
   der GWZ 2011; ob der Zensus 2022 eine Bundessumme der Wohnfläche je Gebäudetyp veröffentlicht,
   ist **nicht geprüft**. Randfälle reiner MFH- bzw. EFH/ZFH-Satz: \(M_0\) = 1,069
   bzw. 1,360 Mrd. €₂₀₂₆/a. Der Wert wird
   multipliziert mit dem **Wohngebäudeanteil je Adresse 0,872** (= 19,7 Mio. Wohngebäude /
   22,6 Mio. Adressen, Register 60-R17-01, **Quelle**) — nicht jede exponierte Adresse trägt ein
   Wohngebäude, und #60 rechnet nur Wohngebäude.
3. **Gemessene Jahresschadensrate je Klasse** aus dem Lauf des Produktionsmodells über die acht
   Anker-Kommunen: \(r_{\text{GK3+GK4}}\) = **0,0059796/a** und \(r_{\text{GK2}}\) =
   **0,00067515/a**. **Quelle:** `docs/evidenz/60_stichprobe/m0_klassenraten.csv`, Zeilen
   `klasse=gk3_gk4/kommune=alle` bzw. `klasse=gk2/kommune=alle`, Spalte
   `rate_exponiert_hqextrem_1_pro_a`. **Wahl des Nenners** (gehört sichtbar in den Bericht, nicht
   in einen Code-Kommentar): Die Datei führt je Klasse zwei Raten — bezogen auf die gesamte
   Wohnfläche der Rasterzelle (`rate_zellen_1_pro_a`) oder auf die Wohnfläche der im
   HQextrem-Raster tatsächlich exponierten Gebäude (`rate_exponiert_hqextrem_1_pro_a`). Das
   Mengengerüst aus Punkt 1 zählt **exponierte Adressen**, nicht die Adressen ganzer Zellen;
   339.000 · 208 m² ist also exponierte Wohnfläche. Konsistent dazu ist die zweite Rate. Die
   Gegenrechnung mit dem Alternativnenner (0,0041973/a bzw. 0,00043606/a) ergäbe
   \(M_0\) = 0,850 Mrd. €₂₀₂₆/a und \(\lambda\) = 1,33; die Spannweite zwischen beiden Nennern ist
   damit beziffert statt verschwiegen.

\(M_0\) = 0,872 · 481.726,25 € · (339.000 · 0,0059796/a + 1.380.000 · 0,00067515/a) =
**1,243 Mrd. €₂₀₂₆/a** — Klassenbeiträge: GK3+GK4 **0,852 Mrd. €₂₀₂₆/a**, GK2 **391 Mio. €₂₀₂₆/a**
(zusammen 1,243 Mrd. €₂₀₂₆/a; vor der Typgewichtung, mit dem reinen EFH/ZFH-Satz 527.280 €:
1,360 Mrd. €₂₀₂₆/a, Ledger-Befund 58).

**Restfehler unterhalb der Stichprobenauflösung (§3.8, Vorgabe P1).** Die acht Anker-Kommunen
lösen nicht alles auf, was in die Klassenraten eingeht. Die vier bekannten Positionen werden
beziffert, nicht geglättet:

1. **Fallback-Anteil Tiefe, Deggendorf: 88,5 %** (**Quelle:** `m0_klassenraten.csv`, Spalte
   `anteil_fallback_tiefe`, Zeile `klasse=gk3_gk4/kommune=Deggendorf`). Für diesen Flächenanteil
   stammt die Überflutungstiefe aus dem Fallback statt aus einer gemessenen Tiefenebene.
2. **Fallback-Anteil Zensus, Klasse GK3+GK4: 79,5 %** (**Quelle:** `m0_klassenraten.csv`, Spalte
   `anteil_fallback_zensus`, Zeile `klasse=gk3_gk4/kommune=alle`). Für rund vier Fünftel der
   Wohnfläche dieser Klasse kommt die Gebäude-/Wohnflächenzuordnung aus dem Zensus-Fallback.
3. **Streuung der Klassenrate über die acht Kommunen: 0,0033/a (Deggendorf) bis 0,0103/a (Grimma),
   Faktor 3,1** (**Quelle:** `m0_klassenraten.csv`, Spalte `rate_exponiert_hqextrem_1_pro_a`,
   Klasse `gk3_gk4`). Der bundesweit einheitlich angesetzte Klassenwert glättet diese Spannweite.
   Wie groß der daraus entstehende Fehler am nationalen \(M_0\) ist, ist **nicht gemessen**,
   sondern eine **Abschätzung von KAP3** (§3.9): bei Faktor 3,1 zwischen den Extremkommunen ein
   einstelliger Prozentfehler am Gesamtwert; eine belastbare Fehlerschranke fehlt, solange nur acht
   Kommunen in der Stichprobe stehen (Herleitung: Zahl der Stichprobenkommunen gegen die gemessene
   Streuweite, kein statistischer Test).
4. **Unschärfe des Nenners selbst: 0,850 gegenüber 1,243 Mrd. €₂₀₂₆/a**, also rund 32 % Spanne
   (Wahl des Nenners, Punkt 3 der Größen-Aufzählung oben). Welcher Nenner richtig ist, entscheidet keine Messung, sondern eine
   **Abschätzung von KAP3** zur Konsistenz mit dem Mengengerüst (Herleitung: Adress- statt
   Zellbezug der 339.000 bzw. 1,38 Mio. Adressen).

**Auflösung (Ressourcen-Regel §3.4).** Alle Schritte dieses Kapitels laufen auf **Bundesland-Ebene
(16 Werte), auf Gemeindepunkt-Ebene und auf einer dokumentierten Stichprobe von Anker-Kommunen**;
**kein Schritt dieses Kapitels erfordert einen nationalen 100-m-Vollraster-Lauf** — weder die
Bestimmung von \(\lambda\) (zwei gemessene Klassenraten und das nationale Mengengerüst, siehe
oben) noch die Verteilungsprüfung
(Länderwerte) noch das Sanity-Band (Bestandsstatistik). Die Anker-Stichprobe umfasst je
Ereignisjahr die am stärksten betroffenen Kommunen der betroffenen Länder; für den Erstlauf sind
das **Grimma, Dresden, Deggendorf, Passau, Halle (Saale), Hitzacker, Rosenheim und Reichertshofen**
— acht Kommunen mit Hochwassergefahrenkarten-Deckung, auf denen das Produktionsmodell vollständig
gerechnet wird. Die Auswahlregel steht damit im Bericht und ist nachvollziehbar erweiterbar.

**M₀-Band (Vorgabe P1, Ledger-Befunde 36 und 58).** Jede der zehn Eingangsgrößen aus den Punkten 1–3 oben
erhält ein unteres und ein oberes Bandende, alle Enden gleichgerichtet (multiplikative Bandenden,
keine Verteilungsannahme, wie in §4.2 für \(A^{*}\), Anweisung A-0034):

| Eingangsgröße | Zentralwert | Unteres Bandende | Oberes Bandende | Quelle bzw. Abschätzung |
|---|---|---|---|---|
| Wohnfläche je Wohngebäude | 208 m² | **208 m²** | **208 m²** | **Quelle:** Register 60-R24-01 (4,1 Mrd. m² ÷ 19,7 Mio. Wohngebäude, amtliche Bestandsstatistik). Kein Band ausgewiesen — die Größe ist der Quotient zweier amtlicher Summen, keine Abschätzung von KAP3; sie geht deshalb unten wie oben mit demselben Punktwert ein, statt ihr ohne Beleg eine Streuung zu unterstellen. |
| BGF-Faktor | 1,30 | **1,25** | **1,40** | **Quelle:** Register 60-R24-01, §3.9 „Abgeschätzt" (Rechenschritt 3, Band 1,25–1,40). |
| Wertsatz \(n_{\text{EFH/ZFH}}\) | 1.950 €₂₀₂₆/m² BGF | **1.890 €₂₀₂₆/m² BGF** | **2.043 €₂₀₂₆/m² BGF** | **Quelle:** Register 60-R24-01 (Fortschreibungsfaktor 2023→2026, Band 1,0706–1,1576, gerundet 1,07–1,16; Band 1.890–2.043, B4 Rechenschritt 2). |
| Wertsatz \(n_{\text{MFH}}\) | 1.533 €₂₀₂₆/m² BGF | **1.485 €₂₀₂₆/m² BGF** | **1.606 €₂₀₂₆/m² BGF** | **Quelle:** Register 60-R24-01 (derselbe Fortschreibungsfaktor; Band 1.485–1.606, B4 Rechenschritt 2). |
| Typ-Mix \(\bar\theta_{\text{EFH/ZFH}}\) (Wohnflächenanteil; \(\bar\theta_{\text{MFH}} = 1 - \bar\theta_{\text{EFH/ZFH}}\)) | 0,596 | **0,471** | **0,624** | **Quelle:** Destatis, Bestand und Bauabgang von Wohnungen und Wohngebäuden 2021, Tabelle 2.1.3, 31.12.2021 (`docs/evidenz/60_destatis_wohnflaeche_gebaeudetyp_2021.csv`): Deutschland 2.289.188/3.841.438 = 0,596. Bandenden aus den beiden Gebietsteilen, die Tabelle 2.1.3 ausweist: Neue Länder und Berlin (259.344 + 72.212)/703.982 = 0,471, Früheres Bundesgebiet (1.417.059 + 540.574)/3.137.456 = 0,624. In dieser Publikation ist die Wohnfläche nach Gebäudetyp nur in Tabelle 2.1 (Deutschland und die zwei Gebietsteile) aufgegliedert; die Länder-Tabellen 1.3 (Wohnfläche, PDF-S. 11–13) und 2.2 (Wohngebäude, PDF-S. 17–19) führen keinen Gebäudetyp (gelesen: Tabellenverzeichnis PDF-S. 4, Tabellen 1.3.3, 2.1.3 und 2.2.3 vollständig). Ob Länderwerte aus einer anderen amtlichen Quelle (etwa GENESIS-Tabelle 31231) das Band weiten würden, ist **nicht geprüft**; die Wahl der Gebietsteile als Bandenden ist deshalb eine **Abschätzung von KAP3** (§3.9). Ebenso ist es eine Abschätzung von KAP3, dass der Mix der **exponierten** Teilmenge in diesem Band liegt (Herleitung: die Anker-Kommunen liegen in beiden Gebietsteilen). Die Randfälle 0 und 1 stehen als Modellgrenze in Punkt 2 oben. |
| Wohngebäudeanteil je Adresse | 0,872 | **0,872** | **0,872** | **Quelle:** Register 60-R17-01/60-R24-01 (19,7 Mio. Wohngebäude ÷ 22,6 Mio. Adressen, beides amtliche Bestandsstatistik, Punkt 2 oben). Kein Band ausgewiesen — Quotient zweier amtlicher Summen ohne publizierte Unsicherheit; Punktwert unten wie oben. |
| Klassenrate GK3+GK4 | 0,0059796/a | **0,0033/a** | **0,0103/a** | **Abschätzung von KAP3**, Herleitung: Streuung der Klassenrate über die acht Anker-Kommunen (Faktor 3,1; `m0_klassenraten.csv`, Spalte `rate_exponiert_hqextrem_1_pro_a`, Klasse `gk3_gk4`: Minimum Deggendorf 0,0033, Maximum Grimma 0,0103), siehe Restfehler-Position 3 oben. |
| Klassenrate GK2 | 0,00067515/a | **0,000301/a** | **0,001154/a** | **Abschätzung von KAP3**, hergeleitet analog zur Restfehler-Position 3: `m0_klassenraten.csv`, Spalte `rate_exponiert_hqextrem_1_pro_a`, Klasse `gk2` — Minimum Reichertshofen 0,000301, Maximum Halle (Saale) 0,001154. Für GK2 beziffert dieses Kapitel die Streuung nicht als eigene Restfehler-Position; das Minimum/Maximum der acht Kommunenwerte wird deshalb hier nach demselben Verfahren als KAP3-Abschätzung übernommen. |
| Exponierte Adressen GK3+GK4 | 339.000 | **339.000** | **339.000** | **Quelle:** Register 60-R17-01 (ZÜRS Geo 2025, GK3 1,1 % + GK4 0,4 % von 22,6 Mio. Adressen; Punkt 1 oben). Kein Band ausgewiesen — die Zonierungsquote ist eine Bestandsstatistik, keine Abschätzung; Punktwert unten wie oben. |
| Exponierte Adressen GK2 | 1.380.000 | **1.380.000** | **1.380.000** | **Quelle:** Register 60-R17-01 (ZÜRS Geo 2025, GK2 6,1 % von 22,6 Mio. Adressen; Punkt 1 oben). Kein Band ausgewiesen, aus demselben Grund wie oben. |

Typgewichteter Wertsatz (alle Enden gleichgerichtet, der niedrige Typ-Mix mit den unteren
Wertsätzen): unten 0,471 · 1.890 + 0,529 · 1.485 = 1.675,755 €₂₀₂₆/m² BGF; Zentralwert
1.781,532 €₂₀₂₆/m² BGF (Punkt 2); oben 0,624 · 2.043 + 0,376 · 1.606 = 1.878,688 €₂₀₂₆/m² BGF.

Wert je exponiertem Wohngebäude: unten 208 · 1,25 · 1.675,755 = 435.696,30 €₂₀₂₆; Zentralwert
208 · 1,30 · 1.781,532 = 481.726,25 €₂₀₂₆ (Punkt 2); oben 208 · 1,40 · 1.878,688 = 547.073,95
€₂₀₂₆.

Summenterm (Adressen × Klassenrate): unten 339.000 · 0,0033 + 1.380.000 · 0,000301 = 1.534,08/a;
Zentralwert 339.000 · 0,0059796 + 1.380.000 · 0,00067515 = 2.958,79/a (unverändert, Punkt 3); oben
339.000 · 0,0103 + 1.380.000 · 0,001154 = 5.084,22/a.

\(M_0\)_unten = 0,872 · 435.696,30 € · 1.534,08/a = 582.838.678 €₂₀₂₆/a ≈ **0,583 Mrd. €₂₀₂₆/a**
\(M_0\)_oben = 0,872 · 547.073,95 € · 5.084,22/a = 2.425.419.445 €₂₀₂₆/a ≈ **2,425 Mrd. €₂₀₂₆/a**

Damit ist \(M_0\) = **1,243 Mrd. €₂₀₂₆/a**, mit einem Band von **0,583–2,425 Mrd. €₂₀₂₆/a** um
diesen Zentralwert. Dieses Band ist in §4.4 und §4.8 in das Unsicherheitsband von λ fortgepflanzt (Ersatzkette
für Ledger-Befund 36; die Plausibilitätsschranke ist seit T-0574 davon getrennt, §4.4) und ebenso in den
Produkt-Block `flood_bldg.lambda` (Kap. 7) und die Entscheidungslog-Zeile 8 nachgezogen.

<a id="niveau-skalar"></a>
### 4.4 Der Niveau-Skalar

\(\lambda = A^{*}/M_0\) = 1,132 / 1,243 = **0,911** (vollständig fortgepflanztes Band, Zähler und
Nenner unabhängig an ihren jeweiligen Extremen, aus dem Ankerband von \(A^{*}\), 0,296–2,291
(§4.2), und dem Band von \(M_0\), 0,583–2,425 (§4.3): **0,12–3,93**). Vor der Typgewichtung des
Wertsatzes (Ledger-Befund 58) stand hier 1,132 / 1,360 = 0,832 mit Band 0,11–3,49.

**Anwendungsregel.** \(\lambda\) ist ein **einziger, bundesweit konstanter** Faktor auf
\(\text{EAD}_k\) jeder Kommune. Er ist kein Verteilungsschlüssel: Die relative Verteilung zwischen
Kommunen bleibt unverändert, eine Kommune ohne Flussaue bleibt bei 0 (Lackmustest §3.4). Es gibt
keinen zweiten Skalar, keinen bundeslandspezifischen Korrekturfaktor und keine Nachkalibrierung
einzelner Kommunen.

**Unsicherheitsband von \(\lambda\) — kein Prüfstein.** Das Band **0,12–3,93** ist das vollständig
fortgepflanzte Band aus dem Ankerband von \(A^{*}\), 0,296–2,291 (§4.2), und dem Band von \(M_0\),
0,583–2,425 (§4.3) — Zähler und Nenner unabhängig an ihren jeweiligen Extremen, alle Enden
gleichgerichtet (multiplikative Bandenden, keine Verteilungsannahme, Anweisung A-0034):
\(\lambda_{\text{unten}}\) = 0,296 / 2,425 = 0,122061… → **0,12**, \(\lambda_{\text{oben}}\) =
2,291 / 0,583 = 3,929674… → **3,93** (zwei Nachkommastellen, kaufmännisch gerundet). Es sagt, wie
weit \(\lambda\) schwankt, wenn Anker und Modellsumme innerhalb ihrer eigenen Bänder liegen, und
wird so im Produkt als Band des Skalars geführt. **Als Prüfstein taugt es nicht** (Ledger-Befund 61):
Jedes \(\lambda = A^{*}/M_0\), das aus Werten innerhalb der eigenen Bänder gebildet wird, liegt
zwangsläufig in [0,12; 3,93]; eine Prüfung gegen dieses Intervall kann kein Ergebnis zurückweisen,
das mit der Methode dieses Berichts entstehen kann. Bis zum Stand vor T-0574 stand genau dieses
Intervall hier als „Plausibilitätsschranke"; das ist aufgegeben.

**Plausibilitätsschranke [0,5; 2,0] (Abschätzung von KAP3).** Ergibt eine Neubestimmung
\(\lambda < 0{,}5\) oder \(\lambda > 2{,}0\), wird **nicht** der Skalar gesetzt, sondern das
Modell gilt als fehlerhaft: Dann trägt eine Eingangsgröße den Fehler (Exponiertenzahl, Wertdichte,
Schadensfunktion), und der Befund geht ins Ledger, bevor gerechnet wird. Die Schranke ist bewusst
**nicht** aus den Bändern von \(A^{*}\) oder \(M_0\) gebildet, sondern aus einem
Modellverständnis-Argument, das keine Größe enthält, die in \(\lambda\) eingeht: \(\lambda\)
gleicht nur den gemeinsamen Niveaufehler von \(M_0\) aus. Jede der tragenden Eingangsgrößen von
\(M_0\) — exponierte Adressen je Klasse, Wertsatz je Gebäude, Schadensquote aus der
Schadensfunktion — ist aus einer eigenen Quelle belegt (§4.3, Register 60-R17-01, 60-R24-01, §3.3).
Muss der Skalar das Modellniveau um mehr als den **Faktor 2** nach oben oder unten verschieben,
liegen diese Eingangsgrößen **zusammen** um mehr als den Faktor 2 daneben — weil sie sich
multiplizieren, genügt dafür schon, dass jede der drei um rund 26 % in dieselbe Richtung abweicht
(\(2^{1/3}\) = 1,26). Warum das als Modellfehler gilt und nicht als Kalibrierrest: Ein
Kalibrierrest ist die Niveauabweichung, die sich aus der belegten Unsicherheit der Eingangsgrößen
erklären lässt. Selbst wenn alle Eingangsgrößen von \(M_0\) gleichzeitig an ihren ungünstigen
Bandenden liegen, verschiebt sich \(M_0\) nur auf das 0,47- bzw. 1,95-Fache seines Zentralwerts
(0,583 / 1,243 bzw. 2,425 / 1,243, §4.3), also knapp innerhalb des Faktors 2. Ein darüber hinaus
nötiger Ausgleich lässt sich mit den belegten Bändern nicht mehr erklären und deutet auf eine
Eingangsgröße außerhalb ihres Bandes (falsche Quelle, falsche Einheit, fehlende Klasse). Das
\(M_0\)-Band dient dabei nur als Stütze der Plausibilität, nicht als Herleitung: Die Schranke
bewegt sich nicht mit ihm. Der Faktor 2 ist eine **Abschätzung von KAP3**
(§3.9), keine Messung; er ist der frühere, vor der Herleitung aus den Bändern (Ledger-Befund 36) geltende Stand
(„Faktor 2 um den Neutralwert 1"), jetzt mit dieser Begründung und getrennt vom Unsicherheitsband ausgewiesen. **Sensitivität der Wahl:**
Mit Faktor 2 liegt das kürzeste Fenster aus §4.1a (\(\lambda\) = 0,500, genau 0,5004) knapp
innerhalb, mit Faktor 1,5 ([0,67; 1,5]) fiele es heraus, mit Faktor 3 ([0,33; 3,0]) keines der vier; der Zentralwert 0,911 liegt bei allen drei Wahlen
innerhalb. **Trennschärfe:** Das Unsicherheitsband [0,12; 3,93] ragt an beiden Enden über die
Schranke hinaus — die Schranke kann also Werte zurückweisen, die mit der Methode entstehen können;
genau das unterscheidet sie vom Unsicherheitsband.

Der Zentralwert \(\lambda\) = 0,911 **liegt innerhalb** der Schranke [0,5; 2,0] (Abstand zur
Untergrenze Faktor 1,82, zur Obergrenze Faktor 2,20); der Skalar wird deshalb gesetzt. Gesetzt heißt
nicht endgültig: \(\lambda\) ist **weiterhin vorläufig**, weil die Verteilungsprüfung in 4.5 nicht
bestanden wird (Modellentscheid, Einleitung Kap. 4).

<a id="verteilungspruefung"></a>

### 4.5 Unabhängige Verteilungsprüfung: Achse Ereignisregime (Jahresauslassung über die Ankerreihe)

**Prüfgröße.** Anteil des **Erwartungswerts** der Jahresschadensumme, der aus dem **seltenen
Regime** (Ereignisse ab HQ100 einschließlich HQextrem) stammt — die kritischste Achse dieses
Risikos, weil die Schadensfunktion dort gedeckelt und die Jährlichkeit dort am unsichersten ist.
Beide Seiten der Prüfung sind damit **dieselbe Größe**: ein Anteil am Erwartungswert, nicht der
Überschuss eines Einzeljahres über ein Mittel (abgelöste Fassung, Ledger-Befund 33).

**Ankerseitige Prüfgröße (Jahresauslassung, Leave-one-out).** Aus der Jahresreihe
\(A_t\), \(t \in T\) = 2002–2024 (`docs/evidenz/60_gdv_jahresreihe_2002_2024.csv`, Spalte
`wert_mrd_eur`, 23 Werte, Bestands- und Preisstand 2024):

\[
R_{\text{anker}} = \frac{\sum_{t \in T} \max\!\left(0,\; A_t - \bar{A}_{-t}\right)}{\sum_{t \in T} A_t},
\qquad
\bar{A}_{-t} = \frac{1}{|T|-1} \sum_{s \in T,\, s \neq t} A_s .
\]

Gelesen wird das so: \(\bar{A}_{-t}\) ist das **ohne das Jahr \(t\) selbst** gebildete Normaljahr;
\(\max(0, A_t - \bar{A}_{-t})\) ist der Teil des Jahres \(t\), den ein Normaljahr nicht erklärt,
also der Beitrag seltener Ereignisse. Zähler und Nenner sind Summen über dieselben 23 Jahre; geteilt
durch 23 stehen dort Erwartungswert des Überschusses und Erwartungswert der Jahressumme.
\(R_{\text{anker}}\) ist deshalb ein **Erwartungswertanteil** und direkt mit dem modellseitigen
Regime-Anteil vergleichbar.

**Unabhängigkeit von der Kalibrierung (§3.4).** Zwei Eigenschaften, beide nachrechenbar statt
behauptet. (1) **Skaleninvarianz:** Zähler und Nenner sind homogen vom Grad 1 in den \(A_t\), also
gilt \(R_{\text{anker}}(c \cdot A) = R_{\text{anker}}(A)\) für jedes \(c > 0\). Die Prüfgröße trägt
damit **keine** Niveauinformation; \(\lambda\) folgt allein aus dem Niveau (Mittel der Reihe,
§4.1a) und könnte sich beliebig ändern, ohne \(R_{\text{anker}}\) zu bewegen. (2)
**Jahresauslassung:** Der Bezugswert eines Jahres enthält dieses Jahr nicht, kein Jahr prüft sich
gegen sich selbst. Die frühere Überlappung — das Prüfjahr war zugleich die einzige Quelle des
Ankermittels — ist damit aufgehoben; geprüft wird die **Form** der Reihe, angepasst wurde ihr
**Niveau**.

**Toleranz — vorab fixiert: ±11,5 Prozentpunkte** (absolut, auf den Regime-Anteil). Sie ist
festgelegt, **bevor** der Ist-Wert unten gerechnet wird, und sie wird bei einer Nichterfüllung
nicht geweitet; gegenüber der abgelösten Fassung (±15, ankerseitig gesetzt statt hergeleitet) ist
sie **enger**. Herleitung aus drei voneinander unabhängigen Beiträgen, quadratisch
zusammengesetzt (Abschätzung von KAP3, §3.9, mit gerechneten Bestandteilen):

| Beitrag | Wert | Herkunft |
|---|---|---|
| Ankerseitige Stichprobenstreuung | **±11,2 Pp** | **berechnet:** Jackknife über die 23 Jahre — für jedes Jahr wird \(R_{\text{anker}}\) auf den übrigen 22 Jahren neu gerechnet (Replikate 37,6 % bis 49,9 %), Standardfehler \(\sqrt{\tfrac{n-1}{n}\sum_i (R_{(i)} - \bar{R})^2}\) = 11,16 Pp. Er ist groß, weil wenige Jahre den Überschuss tragen — das ist die reale Unsicherheit einer 23-Jahre-Reihe, nicht ein Zuschlag. |
| Ankerseitige Ableseunschärfe | **±1,7 Pp** | **berechnet:** je Balken ±0,05 Mrd. € (Ablesegenauigkeit der Grafik, CSV-Spalte `anmerkung`), im ungünstigsten Muster angesetzt (alle Jahre über ihrem Auslassungsmittel nach oben und alle übrigen nach unten, und umgekehrt): \(R_{\text{anker}}\) zwischen 46,1 % und 49,5 %. |
| Modellseitiges Band | **±2,3 Pp** | **berechnet:** belegtes HQextrem-Band 5,0·10⁻³ bis 1,0·10⁻³ a⁻¹ (Register 60-W085-01) ergibt einen Regime-Anteil von 32,4 % bis 36,9 %. |

Ankerseitiges Toleranzbudget: \(\sqrt{11{,}16^2 + 1{,}73^2}\) = **±11,3 Pp**; mit dem
modellseitigen Band \(\sqrt{11{,}29^2 + 2{,}30^2}\) = **±11,5 Pp**. Quadratisch und nicht linear,
weil die drei Beiträge unabhängige Fehlerquellen sind (Standardfehler bzw. Bänder, keine
systematisch gleichgerichteten Zuschläge); die Kombinationsregel ist zusammen mit der Toleranz
vorab gewählt und wird nicht nach dem Ergebnis gewechselt. Zwei Unschärfen gehen **nicht** ins
Budget ein, weil sie nicht als Streuung beziffert werden können: die gepoolten fluvialen und
pluvialen Ereignisse der GDV-Position und der Unterschied zwischen versicherten und gesamten
Schäden. Beide stehen unten als Modellgrenze.

**Ist-Ergebnis.** Modellseite: aus den Stützstellen von §3.6 entfallen auf HQhäufig 66,14 %, auf
HQ100 23,23 % und auf das Extremregime 10,63 % des Erwartungswerts (die drei Summanden
4,174 / 1,466 / 0,671 m²/a der Trapezsumme aus §3.4 Schritt 2, geteilt durch ihre Summe
6,311 m²/a; die drei Anteile summieren sich zu 100,00 %), also
23,23 + 10,63 = **33,86 %** auf das seltene Regime ab HQ100. Ankerseite: Von der Summe
42,28 Mrd. € der 23 Jahre liegen 20,186 Mrd. € über dem jeweils ohne das Jahr gebildeten
Normaljahr; dieser Überschuss verteilt sich auf fünf Jahre — 2021 (11,25), 2002 (5,82), 2013
(2,16), 2024 (0,80) und 2016 (0,17). Daraus \(R_{\text{anker}}\) = 20,186/42,28 = **47,74 %**.
**Differenz 47,74 − 33,86 = 13,88 Prozentpunkte > 11,5 Prozentpunkte — Prüfung nicht bestanden.**
Alle Anteile stehen mit zwei Nachkommastellen, damit sich die Einzelanteile zu 100 und die beiden
seltenen Anteile zu ihrer Summe addieren; auf eine Stelle gerundet ergäben 66,1 + 23,2 + 10,6 nur
99,9 und 23,2 + 10,6 = 33,8 statt 33,9 (Ledger-Befund 65). Gerundet auf eine Stelle bleibt es bei
rund 13,9 Prozentpunkten Abstand.

**Modellentscheid (§3.8, nicht geglättet).** Das Ergebnis wird weder durch Weiten der Toleranz noch
durch Nachziehen des Modells an den Anker geheilt. Es wird als Entscheid ausgewiesen und im Ledger
geführt: (1) **Richtung.** Das Modell legt rund 14 Prozentpunkte **zu wenig** Gewicht auf das
seltene Regime; seine Tiefen-Schadensfunktion ist im Extrem gedeckelt (§3.3) und die HQextrem-Rate
niedrig angesetzt. (2) **Kein Nachfitten der Form.** Die drei Stützstellen bleiben unverändert; ein
Anpassen der Jährlichkeiten oder der Deckelquote an den Ankerbefund wäre ein zweiter, verdeckter
Kalibrierschritt und ist nach §2.4 unzulässig. (3) **\(\lambda\) bleibt gesetzt, aber vorläufig.**
Die Prüfgröße ist skaleninvariant und berührt das Niveau nicht; die Bundessumme bleibt an den Anker
gebunden. Betroffen ist die **Aufteilung** des Erwartungsschadens auf die Szenarien — und damit
jede Größe, die auf dem Regime-Anteil steht, zuerst \(s_{\text{bem}}\) in §5.1.3 (der Hebel S092
wird eher überschätzt, wenn das Modell dem seltenen Regime zu wenig Gewicht gibt). (4) **Was die
Prüfung bestehen ließe**, ist benannt, nicht gesetzt: eine höhere HQextrem-Jährlichkeit oder eine
weniger stark gedeckelte Schadensfunktion. Beides braucht Evidenz, nicht die Prüfung als Begründung.

**Trennschärfe und Grenzen der Prüfung** (nicht geglättet, §3.8): Gegen den Ankerwert 47,7 %
bestünde eine Verdopplung des HQextrem-Schadens (\(A_3\) = 600 m², Regime-Anteil 48,8 %, Abstand
1,0 Pp) und ebenso eine Verdreifachung (58,2 %, Abstand 10,4 Pp); eine Halbierung (22,6 %, Abstand
25,1 Pp) bestünde nicht. Die Prüfung trennt also **nach unten** scharf und nach oben schwach — eine
Folge des großen ankerseitigen Stichprobenfehlers, nicht der Toleranzwahl. Weiter offen bleiben:
die GDV-Position poolt fluviale und pluviale Ereignisse (2021 ist pluvial dominiert und trägt
allein 56 % des Überschusses), sie misst versicherte statt gesamter Schäden, und das Normaljahr
\(\bar{A}_{-t}\) ist ein Mittel, keine gemessene Trennung nach Jährlichkeit. Was fehlt, sind
**Ereignis**werte; sie sind nicht publiziert (§4.1). Die **Jahres**werte selbst sind dagegen
vorhanden, und ihre Quantile gehen in die zweite Prüfgröße unten ein (Ledger-Befund 63).

**Zweite Prüfgröße: Quantilvergleich der höchsten Jahre (Ledger-Befund 63).**
\(R_{\text{anker}}\) vergleicht Mittelwerte. Daneben steht ein Vergleich der **Jahresquantile**, der
keine Ereignisdaten braucht: Die 23 Jahreswerte werden der Größe nach geordnet; das Jahr auf Rang
\(i\) (\(i = 1\) ist das schadensreichste) erhält die Überschreitungswahrscheinlichkeit nach Weibull
\(p_i = i/(n+1) = i/24\) a⁻¹ — Rang 1 steht also für ein „rund 24-jährliches Jahr". Verglichen wird
auf beiden Seiten, das Wievielfache eines Normaljahrs dieses Jahr ist:

\[
Q_i^{\text{anker}} = \frac{A_{(i)}}{\bar{A}_{-(i)}},
\qquad
Q_i^{\text{modell}} = \frac{D(p_i)}{\bar A_z} .
\]

Dabei ist \(A_{(i)}\) der Jahreswert auf Rang \(i\), \(\bar{A}_{-(i)}\) das ohne dieses Jahr gebildete
Normaljahr (wie oben), und \(D(p)\) die Schaden-Wahrscheinlichkeits-Kurve aus §3.4 Schritt 2 —
dieselbe Kurve, deren Fläche \(\bar A_z\) ist: zwischen den drei Stützstellen (15,0 / 77,76 /
300,0 m² bei \(p\) = 0,1 / 0,01 / 0,002236 a⁻¹) geradlinig in \(p\), seltener als HQextrem konstant,
häufiger als HQhäufig null. Beide Seiten sind Verhältnisse und damit **skaleninvariant**; sie
tragen wie \(R_{\text{anker}}\) keine Niveauinformation und sind von \(\lambda\) unabhängig. Die
Modellseite unterstellt, dass die Kurve der Beispielzelle die **Form** der Bundesjahressumme
wiedergibt, also alle betroffenen Flussabschnitte eines Jahres dasselbe Ereignisregime erleben —
eine Modellgrenze; eine räumlich weniger gleichläufige Bundessumme hätte flachere obere Quantile.
Gelesen wird eine Rangtabelle, keine angepasste Extremwertverteilung (P3).

**Toleranz — vorab fixiert: 90-%-Rangband** (Abschätzung von KAP3 beim Niveau 90 %, §3.9; die
Bandgrenzen selbst sind gerechnet). Wie selten das Jahr auf Rang \(i\) in Wahrheit ist, ist bei
23 Jahren selbst unsicher. Die Grenzen \(p_{i,u}\) und \(p_{i,o}\) sind die
Überschreitungswahrscheinlichkeiten, bei denen in 23 unabhängigen Jahren mit 5 % bzw. 95 %
Wahrscheinlichkeit mindestens \(i\) Jahre darüber lägen (Binomialverteilung; über die Form der
Schäden wird dabei nichts angenommen). Die Prüfung gilt je Rang als bestanden, wenn
\(Q_i^{\text{anker}}\) zwischen \(D(p_{i,o})/\bar A_z\) und \(D(p_{i,u})/\bar A_z\) liegt. Geprüft
werden die vier höchsten Ränge. Die Ableseunschärfe (±0,05 Mrd. € je Balken, ungünstigstes Muster)
verschiebt \(Q_1^{\text{anker}}\) nur zwischen 8,97 und 9,74 und geht deshalb nicht eigens ins Band
ein. Sensitivität des Niveaus: Mit 80 % statt 90 % wird das Band enger (Rang 1: 2,90 bis 36,9),
das Ergebnis unten ändert sich nicht.

| Rang \(i\) | Jahr | \(A_{(i)}\) (Mrd. €) | \(\bar{A}_{-(i)}\) | \(Q_i^{\text{anker}}\) | \(p_i\) (a⁻¹) | \(Q_i^{\text{modell}}\) bei \(p_i\) | Rangband \(p_{i,u}\)–\(p_{i,o}\) (a⁻¹) | Band für \(Q_i^{\text{anker}}\) | Ergebnis |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 2021 | 12,6 | 1,349 | **9,34** | 0,042 | 8,82 | 0,0022–0,122 | 0 bis 47,5 | im Band |
| 2 | 2002 | 7,4 | 1,585 | **4,67** | 0,083 | 4,22 | 0,016–0,190 | 0 bis 11,7 | im Band |
| 3 | 2013 | 3,9 | 1,745 | **2,24** | 0,125 | 0 (häufiger als HQhäufig) | 0,037–0,249 | 0 bis 9,39 | im Band |
| 4 | 2024 | 2,6 | 1,804 | **1,44** | 0,167 | 0 (häufiger als HQhäufig) | 0,062–0,304 | 0 bis 6,61 | im Band |

**Ist-Ergebnis des Quantilvergleichs: bestanden auf allen vier Rängen.** Im Punktvergleich bei
\(p_i\) liegen die beiden höchsten Jahre um 6 % (9,34 gegen 8,82) und 11 % (4,67 gegen 4,22) über
dem Modell — dieselbe Richtung wie bei \(R_{\text{anker}}\) (seltene Jahre im Anker schwerer als im
Modell), aber klein. Auf den Rängen 3 und 4 liegt \(p_i\) über der HQhäufig-Rate von 0,1 a⁻¹: Dort
rechnet das Modell nicht (ausgewiesene Untergrenze, §3.4 Schritt 2), und die GDV-Werte enthalten
zudem pluviale Schäden; die Modellseite 0 ist dort keine Aussage über die Form.

**Trennschärfe des Quantilvergleichs** (gemessen, nicht geglättet, §3.8): Er kann bei 23 Jahren
praktisch nicht scheitern. Das untere Bandende ist auf allen vier Rängen 0, weil das Rangband über
die HQhäufig-Rate hinausreicht; das obere liegt beim 6,6- bis 47,5-Fachen des Normaljahrs. Eine
Verdopplung (\(A_3\) = 600 m²), eine Verdreifachung (900 m²) und eine Halbierung (150 m²) des
HQextrem-Schadens bestehen ebenso. Die erhoffte Schärfung nach oben tritt damit **nicht** ein: Die
Schwäche von \(R_{\text{anker}}\) nach oben kommt aus der Kürze der Reihe, und ein Quantilvergleich
über dieselben 23 Jahre erbt sie. Informativ, aber ohne Toleranz und deshalb **kein Prüfurteil**,
ist der Punktvergleich unter den Varianten: Bei doppeltem HQextrem-Schaden sänke
\(Q_1^{\text{modell}}\) auf 6,83 und \(Q_2^{\text{modell}}\) auf 3,27, bei dreifachem auf 5,58 und
2,67 — weiter weg von 9,34 und 4,67, weil \(D(p)\) zwischen HQhäufig und HQ100 nicht von \(A_3\)
abhängt, das Normaljahr \(\bar A_z\) aber steigt. Die im Modellentscheid oben benannte Richtung
„mehr Gewicht auf HQextrem" wird von den oberen Jahresquantilen also nicht gestützt; das spricht
eher für mehr Gewicht zwischen HQhäufig und HQ100. Entschieden wird daraus nichts — die Stützstellen
bleiben unverändert (§2.4), der Befund steht als Hinweis für die nächste Revision der
Schadensfunktion.

<a id="sanity-band"></a>

### 4.6 Sanity-Band der Bundessumme

**Neufassung nach Befund 35 (Ledger-Schritt T-0333, 18.09.2026), geschärft nach den Befunden 64, 96
und 97 (T-0574, 23.09.2026).** Die frühere Untergrenze
\(U = A_{\text{ver}} \cdot w_{\text{wg}} \cdot \varphi_{\text{fluss}} \cdot \pi\) war ein
Teilprodukt derselben Faktoren, aus denen \(\lambda M_0 \equiv A^{*} = U \cdot u\kappa\) gebildet
wird; die Prüfung \(U \le \lambda M_0\) war damit für jedes \(u\kappa \ge 1\) trivial erfüllt und
konnte nicht scheitern. T-0333 hat sie durch einen ankerunabhängigen Rechenweg ersetzt (nur das
kleinere Fondsvolumen 2013, umgelegt auf eine geschätzte Wiederkehrzeit von 100 Jahren: 0,0103 Mrd.
€₂₀₂₆/a) und die Obergrenze klassengerecht aus den Registerzahlen gebildet (6,29 Mrd. €₂₀₂₆/a). Das
war unabhängig, aber ohne Trennschärfe (Befund 96), und die Obergrenze teilte Adresszahlen und
Gebäudewert mit \(M_0\) (Befund 64). Die Fassung unten trennt deshalb **unabhängige Grenzen**, die
den Prüfstein bilden, von der **Modellschranke**, die nur mitgeführt wird.

| Grenze | Wert | Herleitung |
|---|---|---|
| Untergrenze \(U\) (unabhängig) | **0,189 Mrd. €₂₀₂₆/a** | amtliche Ereignisbilanz der beiden Wiederaufbauhilfe-Gesetze (`docs/evidenz/60_wiederaufbauhilfen_2013_2021.csv`), beide im Ankerfenster 2002–2024: Fondsvolumen 8 Mrd. € (2013, AufbhG § 4 Abs. 1 Satz 1), fortgeschrieben mit 2 %/a über 13 Jahre (\(1{,}02^{13} = 1{,}294\)) zu 10,35 Mrd. €₂₀₂₆, und 30 Mrd. € (2021), fortgeschrieben über 5 Jahre (\(1{,}02^{5} = 1{,}104\)) zu 33,12 Mrd. €₂₀₂₆; zusammen \(E_{\text{fonds}}\) = **43,47 Mrd. €₂₀₂₆**. Davon der Wohngebäudeanteil \(w\) = 1/3 · 1/3 ≈ 0,11 (**Abschätzung von KAP3**, Band 0,06–0,17: ein Drittel der Mittel für private Haushalte neben Infrastruktur und Wirtschaft/Landwirtschaft, davon ein Drittel für die Gebäudesubstanz ohne Hausrat und Fahrzeuge; Band aus einem Haushaltsanteil von 1/4 bis 1/2 und einem Gebäudeanteil von 1/4 bis 1/3) und der flussseitige Anteil \(f_{\text{fluss}}\) = 0,90 (**Abschätzung von KAP3**, Band 0,80–1,00: beide Ereignisse sind dokumentierte Flusshochwasser; der Abschlag trägt nicht getrennt ausgewiesenen Siel- und Sturzflutanteilen Rechnung), verteilt auf die Länge des Ankerfensters \(N\) = 23 Jahre (2002–2024, dieselben Kalibrierjahre wie §4.1 und §4.7; gezählt, keine Abschätzung): \(U = \dfrac{E_{\text{fonds}} \cdot w \cdot f_{\text{fluss}}}{N} = \dfrac{43{,}47 \cdot (1/9) \cdot 0{,}90}{23}\) = **0,189 Mrd. €₂₀₂₆/a**. Es ist ein Mindestwert, weil alle übrigen Hochwasserschäden des Fensters (2002 und alle Jahre ohne Aufbauhilfegesetz) hinzukommen. Keine der sechs Ankergrößen \(A_{\text{ver}}\), \(w_{\text{wg}}\), \(u\), \(\varphi_{\text{fluss}}\), \(\kappa\) und \(\pi\) und keine Registergröße von \(M_0\) geht als Faktor ein. Die frühere Wiederkehrzeit \(T\) = 100 a entfällt; an ihre Stelle tritt die gezählte Fensterlänge. |
| Obergrenze \(O_u\) (unabhängig) | **11,04 Mrd. €₂₀₂₆/a** | aus derselben amtlichen Quelle: das größere Fondsvolumen 2021, fortgeschrieben 33,12 Mrd. €₂₀₂₆, mit den **oberen** Enden der beiden Anteile — der volle Drittelanteil der privaten Haushalte (1/3, einschließlich Hausrat, als Ersatz für den nicht im Fonds enthaltenen versicherten Teil) und \(f_{\text{fluss}}\) = 1,00 — **in jedem Jahr**: \(O_u = 33{,}12 \cdot 1/3 \cdot 1{,}00\) = **11,04 Mrd. €₂₀₂₆/a**. Begründung (**Abschätzung von KAP3**): Das langjährige Jahresmittel kann den Schaden des schwersten Jahres im Ankerfenster nicht übersteigen. Weder Registerzahlen noch Gebäudewert von \(M_0\) noch Ankergrößen gehen ein. |
| Modellschranke \(O_M\) (modellabhängig, kein Prüfstein) | 6,29 Mrd. €₂₀₂₆/a | klassengerechte Bestandsschranke aus Register 60-R17-01: 339.000 exponierte Adressen GK3/GK4 mit Jährlichkeit 0,1 a⁻¹ und 1.380.000 Adressen GK2 mit 0,01 a⁻¹, Gebäudewert 527.280 €₂₀₂₆ (Register 60-R24-01), gedeckelte Schadensquote 0,250 (§3.3): \(O_M = (339.000 \cdot 0{,}1 + 1.380.000 \cdot 0{,}01) \cdot 527.280 \cdot 0{,}250\) = 6,29 Mrd. €₂₀₂₆/a — das physikalische Maximum der Registerstruktur. Weil \(O_M\) dieselben Adresszahlen und fast denselben Wertsatz wie \(M_0\) trägt, ist sie ein festes Vielfaches der Modellsumme (\(O_M / M_0\) = 6,29 / 1,243 = 5,06). \(\lambda M_0 \le O_M\) ist deshalb gleichbedeutend mit \(\lambda \le 5{,}06\) und kann nach bestandener Plausibilitätsschranke \(\lambda \le 2{,}0\) (§4.4) nicht mehr auslösen (\(2{,}0 \cdot 1{,}243\) = 2,49 < 6,29). Sie wird nur mitgeführt, damit ein Leser sieht, wie weit das Ergebnis vom Maximum der eigenen Registerstruktur entfernt ist. |

**Weitung ausgewiesen und fixiert (Befund 96).** Der Stand der Runde 2 war [≈ 0,64; 2,264] Mrd.
€₂₀₂₆/a (Spannweite Faktor 3,5), aber an der Untergrenze tautologisch und an der Obergrenze unter der
klassengerechten Rate. T-0333 ging auf [0,0103; 6,29] (Spannweite Faktor 611), ohne das als Weitung
zu benennen. Das unabhängige Band **[0,189; 11,04]** hat die Spannweite **Faktor 58** — gegenüber
T-0333 um den Faktor 10,5 enger, gegenüber Runde 2 um den Faktor 16,5 weiter. Die Weitung gegenüber
Runde 2 ist der Preis dafür, dass keine Grenze mehr aus den Größen des Modells selbst stammt: Ein
unabhängiges Band kann nicht so eng sein wie eines, das aus dem Ergebnis abgeleitet ist. Das Band
[0,189; 11,04] ist hiermit vorab fixiert; eine spätere Weitung ist ein Befund (§6), kein
Nachführen.

**Empfindlichkeit von \(U\).** Mit den Bandenden von \(w\) und \(f_{\text{fluss}}\) liegt \(U\)
zwischen 43,47 · (1/16) · 0,80 / 23 = 0,095 und 43,47 · (1/6) · 1,00 / 23 = 0,315 Mrd. €₂₀₂₆/a. Die
kalibrierte Bundessumme 1,132 liegt auch über dem oberen Ende (Faktor 3,6) und beim unteren Ende beim
Faktor 12. Fixiert ist der Zentralwert 0,189.

**Ausnahme vom Amtlichkeitsgebot (§3.4).** Bei \(U\) und \(O_u\) sind die beiden Fondsvolumina
amtlich (Bundesgesetze, BGBl.) und die Fensterlänge gezählt; nicht amtlich sind der
Wohngebäudeanteil und der flussseitige Anteil — für sie existiert keine amtliche Statistik, die die
Aufbauhilfe-Mittel zweier Einzelereignisse auf Wohngebäude und Flussanteil herunterbricht, deshalb
tritt an ihre Stelle eine ausgewiesene Abschätzung von KAP3 mit Band (§4.8). Bei der Modellschranke
\(O_M\) sind die Adresszahlen 339.000/1.380.000 aus der ZÜRS-Klassifikation und der Gebäudewert
527.280 €₂₀₂₆ Branchenstatistik des GDV bzw. eine Registerabschätzung, ebenfalls keine amtliche
Statistik im engeren Sinn; die Ausnahme ist dieselbe wie an den übrigen Fundstellen des Berichts,
an denen ZÜRS- und GDV-Zahlen als Abschätzung von KAP3 geführt werden (z. B. §4.1 für den
GDV-Anker), weil für die bundesweite Betroffenheits- und Wertstruktur von Wohngebäuden keine
amtliche Vollerhebung existiert. Für alle Grenzen gilt: Wo keine amtliche Statistik die gesuchte
Aufteilung liefert, tritt eine ausgewiesene, nachvollziehbare Abschätzung von KAP3 an ihre Stelle,
nicht eine stillschweigende Ersatzquelle.

**Ist und Abstand als Kennzahl:** \(\lambda \cdot M_0\) = 0,911 · 1,243 = **1,132 Mrd. €₂₀₂₆/a**
(derselbe Wert wie in §4.4) liegt innerhalb von [0,189; 11,04] Mrd. €₂₀₂₆/a — beim **6,0-Fachen** der
Untergrenze und bei **10 %** der unabhängigen Obergrenze (Abstand Faktor 9,8); zur Modellschranke
\(O_M\) hält es den Faktor 5,6. Diese Abstände zeigen, wie viel der Prüfstein noch prüft: Unten
würde er auslösen, wenn das Modell ein Sechstel seines heutigen Niveaus unterschritte; oben erst beim
Zehnfachen. Das Band ist zugleich die Vorlage für den Sanity-Band-Test der Integration, der beide
Grenzarten getrennt benennt: Eine Bundessumme außerhalb von **[\(U\); \(O_u\)]** ist ein roter
Test (unabhängiger Prüfstein); eine Überschreitung von \(O_M\) ist ein roter Test mit dem Vermerk
„modellabhängig — nur Registerstruktur geprüft", damit ein grüner Test nicht mehr Sicherheit
vorspiegelt, als er trägt.

### 4.7 Kalibrierjahre und Doppelzählungs-Wächter (Bindung von §5.1)

**Kalibrierjahre, namentlich:** **2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011,
2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023 und 2024** — 23
abgeschlossene Schadenjahre. **2025 ist ausgeschlossen** (vorläufig, §4.1). Das **letzte
Kalibrierjahr ist 2024**; auf dieses Jahr sind Bestands- und Preisnormierung des Ankers bezogen.

**Wächter — Referenzzustand ist das betragsgewichtete Ausstattungsmittel, nicht der Stichtag.** Weil die
Modellsumme im Kalibrierfenster konstant gesetzt ist (\(M_t \equiv M_0\), §4.3), fällt der
Kleinste-Quadrate-Schätzer von \(\lambda\) auf das arithmetische Mittel der Ankerreihe über die
23 Kalibrierjahre zurück (\(\lambda = \text{Mittel}(A_t)/M_0\), §4.1a). \(\lambda\) bildet damit
nicht den Ausstattungsstand eines Stichtags ab, sondern den Ausstattungsstand, der in diesem Mittel
steckt. **Jedes Jahr zählt im Mittel einmal, sein Einfluss auf das Mittel ist aber so groß wie sein
Schadenbetrag \(A_s\)** — ein Jahr mit 12,6 Mrd. € (2021) bewegt das Mittel gut dreißigmal so stark wie
ein Jahr mit 0,4 Mrd. €. Senkt eine Nachrüstung aus dem Jahr \(t\) die Schäden der Jahre \(t\) bis
2024 anteilig, steckt sie deshalb mit dem **Betragsanteil** dieser Jahre an der Summe im kalibrierten
Niveau, nicht mit ihrem Zählanteil \((2024-t+1)/23\) (so die Fassung bis T-0577, Ledger-Befund 79):

\[
g_t = \frac{\sum_{s=t}^{2024} A_s}{\sum_{s=2002}^{2024} A_s}
\]

In Worten: Schadensumme der Jahre ab dem Nachrüstjahr geteilt durch die Schadensumme aller 23
Kalibrierjahre (42,28 Mrd. €, Ankerreihe `docs/evidenz/60_gdv_jahresreihe_2002_2024.csv`, Spalte
`wert_mrd_eur`). Zwei Rechenbeispiele:

- Nachrüstung **2020**: Jahre 2020–2024 zusammen 0,4 + 12,6 + 0,3 + 1,1 + 2,6 = 17,0 Mrd. €;
  17,0 ÷ 42,28 = **40,2 %** (Zählgewicht wäre 5/23 = 21,7 %).
- Nachrüstung **2014**: Jahre 2014–2024 zusammen 22,7 Mrd. €; 22,7 ÷ 42,28 = **53,7 %**
  (Zählgewicht wäre 11/23 = 47,8 %).

Das früheste Kalibrierjahr 2002 hat \(g_{2002}\) = 100 %, das letzte 2024 nur 2,6 ÷ 42,28 = 6,1 %.
Grund für den Abstand zum Zählgewicht ist die **Schiefe der Reihe**: 2021 trägt allein 29,8 % der
Summe, 2002 weitere 17,5 % — dieselbe Schiefe, die §4.1a über den Ausreißer-Test und die
Fenster-Sensitivität behandelt. Jede Nachrüstung bis einschließlich 2021 erbt deshalb das volle Gewicht des
Jahres 2021. Nur mit diesem Gewicht \(g_t\) steckt eine vor 2025 realisierte Maßnahme im
kalibrierten Niveau, nicht vollständig.

\(\Delta q\) aus §5.1.2 zählt operativ trotzdem **ausschließlich Nachrüstungen nach dem letzten
Kalibrierjahr 2024**: Um die jahresabhängigen Gewichte \(g_t\) je Maßnahme anzuwenden, müsste der
heutige Ausstattungsstand jahresscharf auf die Nachrüstjahre verteilt sein. Diese Verteilung gibt es
nicht; \(q_0\) ist unten nur als Gesamtanteil abgeschätzt. Der Wächter sperrt Vor-2025-Maßnahmen
deshalb **pauschal mit Gewicht 1** statt mit \(g_t\) — bewusst konservativ gegen Doppelzählung,
aber mit einer bezifferbaren Verzerrung (siehe Modellgrenze unten).

**Verfallsregel, auf denselben Betragsanteil gestellt.** Bisher verfiel der Hebelwert „sobald ein
Kalibrierjahr nach 2024 in den Anker aufgenommen wird"; das unterstellte, dass sich der
Referenzzustand mit jedem neuen Jahr um ein volles Jahr verschiebt. Tatsächlich geht ein neu
aufgenommenes Jahr 2025 mit seinem **Betragsanteil am erweiterten Fenster** ein,
\(A_{2025} / (\sum_{s=2002}^{2024} A_s + A_{2025})\), und eine Nachrüstung aus dem Jahr \(t\) steckt danach
mit \((\sum_{s=t}^{2024} A_s + A_{2025}) / (\sum_{s=2002}^{2024} A_s + A_{2025})\) im Niveau. Rechenbeispiel:
Wäre 2025 ein mittleres Jahr (1,84 Mrd. €), trüge es 1,84 ÷ 44,12 = 4,2 % des erweiterten Fensters;
ein Jahr wie 2021 trüge 12,6 ÷ 54,88 = 23,0 %. Der Hebelwert verfällt deshalb erst mit dem
tatsächlichen Neu-Fit von \(\lambda\) auf das erweiterte Fenster, nicht bereits mit der bloßen
Aufnahme des Jahres in die Ankerreihe; wie stark sich der Referenzzustand dann verschiebt, hängt am
Schadenbetrag des neuen Jahres, nicht an der Zahl der Jahre.

**Modellgrenze: Richtung und Größenordnung der Verzerrung.** Weil der Wächter Vor-2025-Maßnahmen
pauschal mit Gewicht 1 statt mit \(g_t\) sperrt, wird der Anteil einer Maßnahme aus Jahr \(t\), der
bereits im kalibrierten Niveau steckt, **überschätzt** — um \(1 - g_t\). Für 2020 sind das
59,8 Prozentpunkte (40,2 % tatsächlich gegenüber 100 % angenommen), für 2014 sind es
46,3 Prozentpunkte (53,7 % gegenüber 100 %); die Überschätzung fällt für das früheste
Kalibrierjahr 2002 auf 0 und wächst zum letzten Kalibrierjahr 2024 hin auf bis zu 93,9 % (Gewicht
dort nur 6,1 %). In dieser Richtung ist der Wächter also **konservativ**: Er bucht keinen vor 2025
realisierten Objektschutz doppelt, verzichtet dafür aber darauf, den in \(\Delta q\) zählbaren
Hebel um den nicht schon eingepreisten Rest jüngerer Vor-2025-Maßnahmen zu erhöhen — der
tatsächlich wirksame Hebel wird dadurch **unterzählt**, für Maßnahmen aus den Jahren 2010 bis 2015
(zehn bis fünfzehn Jahre vor dem Fensterende) um 30,0 bis 49,1 % ihres Effekts. Auf das
tatsächliche Portfolio ist diese Verzerrung nicht bezifferbar, solange die Verteilung von \(q_0\)
über die Nachrüstjahre fehlt; sie ist hier als Modellgrenze der Wächter-Vereinfachung ausgewiesen,
nicht als Fehler behoben.

<a id="q0-abschaetzung"></a>

**Heutiger Objektschutz-Anteil \(q_0\): Abschätzung von KAP3 (§3.9), Datenebene geparkt (Datenquelle
fehlt).** \(q_0\) ist der Anteil der exponierten Wohngebäude, die Ende 2024 bereits bauliche
Objektvorsorge haben (Abdichtung, Rückstausicherung, angepasste Nutzung). Er ist der
Referenzzustand, gegen den \(\Delta q\) in §5.1.2 „marginal" ist. Eine bundesweite Statistik des
Ausstattungsgrads existiert nicht; eine Datenebene dafür bleibt **geparkt (Datenquelle fehlt)**, mit
Beschaffungs-Watchlist: (1) Zusatzmodul einer künftigen Zensus-Gebäudeerhebung, (2) Auswertung
kommunaler Förderprogramme zur Objektvorsorge, (3) Schadenstatistik der Wohngebäudeversicherung nach
Vorsorgemerkmal, (4) Volltextprüfung der Betroffenenbefragungen nach den Hochwassern 2002–2013
(Kandidat: Kienzler u. a. 2015, NHESS 15, 505–526; §3.8, nicht volltextgeprüft). Der Zahlenwert
wird deshalb **nicht gemessen, sondern abgeschätzt**:

- \(q_0\) = **0,15** (Band **0,05–0,30**), Abschätzung von KAP3, keine Quelle.
- Herleitung: Befragungen nach Ereignissen erfassen nur Haushalte in gerade betroffenen Gebieten,
  überwiegend nach wiederholter Überflutung; dort ist Vorsorge am häufigsten. Der Wächter bezieht
  sich aber auf **alle** exponierten Wohngebäude, und davon liegen vier Fünftel in der seltenen
  Gefährdungsklasse GK2 (1.380.000 von 1.719.000 Adressen, §4.8), wo Überflutungserfahrung und
  Vorsorge seltener sind. KAP3 setzt deshalb eine niedrige Mitte: jedes siebte exponierte Gebäude
  hat heute baulichen Objektschutz. Untere Bandgrenze 0,05: Vorsorge fast nur in den wiederholt
  betroffenen Lagen GK3/GK4 (339.000 Adressen, knapp ein Fünftel) und dort bei einem Viertel der
  Gebäude. Obere Bandgrenze 0,30: auch in GK2 verbreitete Nachrüstung nach 2002, 2013 und 2021.
  Die Befragungen gehen nicht als Effektgröße ein; der Studienart-Einwand aus §5.1 bleibt unberührt.
- **Bindung von \(\Delta q\):** Nachgerüstet werden kann nur ein bisher ungeschütztes Gebäude,
  also gilt \(\Delta q \le 1 - q_0\). Mit den Bandenden: 0,20 ≤ 1 − 0,30 = 0,70 — erfüllt, auch im
  ungünstigsten Fall. \(\Delta q\) = 0,10 ist damit rund ein Achtel des ungeschützten Bestands
  (0,10 ÷ 0,85 = 11,8 %), also tatsächlich ein zusätzlicher, marginaler Schritt.
- **Wirkung nur auf den ungeschützten Teil — bezifferte Modellgrenze.** Die geschützten Gebäude
  tragen schon heute weniger Schaden; ein ungeschütztes Gebäude trägt deshalb mehr als seinen
  Kopfanteil am Erwartungsschaden. Genau gerechnet wäre
  \(r_{\text{S092}} = \Delta q \cdot s_{\text{bem}} \cdot e_{\text{bem}} / (1 - q_0 \cdot s_{\text{bem}} \cdot e_{\text{bem}})\).
  Mit \(q_0\) = 0,15 ist der Nenner 1 − 0,15 · 0,50 · 0,70 = 0,9475, der Hebel also um
  1 ÷ 0,9475 = **+5,5 %** größer (0,035 → 0,0369); am oberen Bandende \(q_0\) = 0,30 um **+11,7 %**
  (0,0391), am unteren 0,05 um +1,8 %. Der Bericht rechnet \(r_{\text{S092}}\) **ohne** diesen
  Faktor und weist ihn hier aus: Er liegt innerhalb des Bands von \(r_{\text{S092}}\) und zeigt in
  die Gegenrichtung der \(s_{\text{bem}}\)-Näherung (§5.1.3, überschätzt den Hebel); beide sind
  Abschätzungen ähnlicher Größe, und die einfache Kette bleibt lesbar (P3). Ist \(q_0\) gemessen,
  wird der Faktor eingerechnet.

### 4.8 Parameter dieses Kapitels (Vorgabe P1)

| Parameter | Wert (Band) | Quelle **oder** Abschätzung von KAP3 |
|---|---|---|
| \(A_{\text{ver}}\) Anker | 1,838 Mrd. € (1,061–1,838) | **Quelle:** GDV-Naturgefahrenstatistik 2024, Datenservice Naturgefahrenreport 2025 (Stand 10.10./30.12.2025); Kleinste-Quadrate-Mittelwert der Jahres-Auswahlregel-Reihe und Tukey-Ausreißertest der 23-Jahre-Reihe (`docs/evidenz/60_gdv_jahresreihe_2002_2024.csv`), §4.1/§4.1a |
| \(w_{\text{wg}}\) | 0,65 (0,55–0,75) | **Abschätzung von KAP3**, Herleitung §4.2 |
| \(u\) | 1,54 (1,33–1,75) | **Abschätzung von KAP3** auf belegter Versicherungsdichte 57 %, Herleitung §4.2 |
| \(\varphi_{\text{fluss}}\) | 0,50 (0,35–0,65) | **Abschätzung von KAP3**, Herleitung §4.2 |
| \(\kappa\) | 1,15 (1,05–1,30) | **Abschätzung von KAP3**, Herleitung §4.2 |
| \(\pi\) | 1,07 (1,039–1,124) | **Abschätzung von KAP3** aus B4 (Baupreisindex), Herleitung §4.2 |
| \(\lambda\) Niveau-Skalar | 0,911 (0,12–3,93) — **vorläufig** | **berechnet** aus \(A^{*}/M_0\) als Kleinste-Quadrate-Schätzer der Jahres-Auswahlregel-Reihe (§4.1a), §4.4, Stand nach dem Stichprobenlauf: \(M_0\) aus den gemessenen Klassenraten GK3+GK4 und GK2 (`docs/evidenz/60_stichprobe/m0_klassenraten.csv`, Spalte `rate_exponiert_hqextrem_1_pro_a`, Zeilen `gk3_gk4;alle` bzw. `gk2;alle`; Wahl dieser Spalte statt `rate_zellen_1_pro_a` begründet in §4.3 Punkt 3) mit Wohngebäudeanteil 0,872 und typgewichtetem Wertsatz (\(\bar\theta_{\text{EFH/ZFH}}\) = 0,596, §4.3 Punkt 2); es fließen die Abschätzungen von KAP3 \(w_{\text{wg}}\), \(u\), \(\varphi_{\text{fluss}}\), \(\kappa\), \(\pi\) sowie die Restfehler der Stichprobe (§4.3) ein, über \(M_0\) zusätzlich der BGF-Faktor \(k_{\text{BGF}}\) und der Fortschreibungsfaktor der Wertsätze (eigene Zeilen); Band vollständig fortgepflanzt aus dem \(A^{*}\)-Band (§4.2) und dem \(M_0\)-Band 0,583–2,425 (§4.3); Zentralwert innerhalb der Plausibilitätsschranke, Sensitivität je Zeitfenster in §4.1a, **vorläufig**, weil die unabhängige Verteilungsprüfung in §4.5 nicht bestanden ist (Abstand 13,9 Pp gegen Toleranz ±11,5 Pp, Modellentscheid §4.5; derselbe Grund in §4.4 und im Block `flood_bldg.lambda`) |
| Baupreisanstieg 2023 → 2024 | 3 % (2,3–5,0 %) | **Abschätzung von KAP3**: gerundet aus den in B4 zitierten Jahresraten des Baupreisindex (3,2 %/3,3 %), Band wie B4; geht in \(\pi = 1{,}105/1{,}03\) ein (§4.2); Sensitivität: \(\pi\) = 1,080 bei 2,3 %, 1,052 bei 5,0 % |
| Klassenraten Bestandsschranke (GK3/GK4; GK2) | 0,1 a⁻¹; 0,01 a⁻¹ | **Abschätzung von KAP3**, Herleitung §4.6 (Register 60-R17-01: Jährlichkeit je ZÜRS-Adressklasse, unverändert übernommen); geht linear in \(O\) ein |
| \(\bar\theta_{\text{EFH/ZFH}}\) nationaler Typ-Mix (Wohnflächenanteil EFH/ZFH; MFH = 1 − \(\bar\theta_{\text{EFH/ZFH}}\)) | 0,596 (0,471–0,624) | **Quelle:** Destatis, Bestand und Bauabgang von Wohnungen und Wohngebäuden 2021, Tabelle 2.1.3, 31.12.2021 (`docs/evidenz/60_destatis_wohnflaeche_gebaeudetyp_2021.csv`); Band aus den Gebietsteilen derselben Tabelle; dass die exponierte Teilmenge im Band liegt, ist eine **Abschätzung von KAP3**, Herleitung §4.3 (Punkt 2 und Bandtabelle) |
| \(M_0\) Modellsumme vor Kalibrierung | 1,243 Mrd. €₂₀₂₆/a (0,583–2,425) | **berechnet**, Herleitung §4.3: \(M_0\) = Wohngebäudeanteil je Adresse · Wert je exponiertem Wohngebäude · (Adressen GK3+GK4 · \(r_{\text{GK3+GK4}}\) + Adressen GK2 · \(r_{\text{GK2}}\)) aus den Zeilen darunter; Band aus den Bandenden dieser Zeilen, alle gleichgerichtet (§4.3 „M₀-Band"); es fließen die Abschätzungen von KAP3 BGF-Faktor, Fortschreibungsfaktor der Wertsätze, Bandenden des Typ-Mix und Bandenden der Klassenraten ein |
| Wohnfläche je Wohngebäude | 208 m² (kein Band) | **Quelle:** Register 60-R24-01 (4,1 Mrd. m² Wohnfläche ÷ 19,7 Mio. Wohngebäude, amtliche Bestandsstatistik 31.12.2024), Herleitung §4.3 Punkt 2; kein Band, weil Quotient zweier amtlicher Summen (§4.3 Bandtabelle) |
| \(k_{\text{BGF}}\) BGF-Faktor (m² Brutto-Grundfläche je m² Wohnfläche) | 1,30 (1,25–1,40) | **Abschätzung von KAP3**, Herleitung §3.4 Schritt 3 und Register 60-R24-01 (Langbeleg B4, Rechenschritt 3: Verhältnis BGF zu Wohnfläche, Band aus kompakten bis gegliederten Bauformen); Sensitivität: 1,25 statt 1,40 verschiebt den Wert je Wohngebäude um −11 % |
| \(n_{\text{EFH/ZFH}}\) Wertsatz Ein-/Zweifamilienhaus | 1.950 €₂₀₂₆/m² BGF (1.890–2.043) | **Quelle:** Register 60-R24-01, NHK 2010 nach ImmoWertV Anlage 4 (Langbeleg B4, Rechenschritt 2); der Fortschreibungsfaktor auf den Preisstand 2026 (1,105, Band 1,0706–1,1576) ist eine **Abschätzung von KAP3** aus dem Baupreisindex, Herleitung B4 |
| \(n_{\text{MFH}}\) Wertsatz Mehrfamilienhaus | 1.533 €₂₀₂₆/m² BGF (1.485–1.606) | **Quelle:** Register 60-R24-01, NHK 2010 nach ImmoWertV Anlage 4 (Langbeleg B4, Rechenschritt 2); derselbe Fortschreibungsfaktor wie in der Zeile darüber (**Abschätzung von KAP3**) |
| Wert je exponiertem Wohngebäude | 481.726,25 €₂₀₂₆ (435.696,30–547.073,95) | **berechnet**, Herleitung §4.3 Punkt 2: 208 m² · 1,30 · (0,596 · 1.950 + 0,404 · 1.533) €₂₀₂₆/m² BGF aus den Zeilen darüber; Band aus deren Bandenden (§4.3 „M₀-Band") |
| Wohngebäudeanteil je Adresse | 0,872 (kein Band) | **Quelle:** Register 60-R17-01/60-R24-01 (19,7 Mio. Wohngebäude ÷ 22,6 Mio. bewertete Adressen), Herleitung §4.3 Punkt 2; kein Band, weil Quotient zweier amtlicher Summen ohne publizierte Unsicherheit |
| Exponierte Adressen GK3+GK4 bzw. GK2 | 339.000 bzw. 1.380.000 (kein Band) | **Quelle:** Register 60-R17-01 (ZÜRS Geo 2025: GK3 1,1 % + GK4 0,4 % bzw. GK2 6,1 % von 22,6 Mio. Adressen), Herleitung §4.3 Punkt 1; gehen auch in \(O_M\) ein |
| \(r_{\text{GK3+GK4}}\) gemessene Klassenrate | 0,0059796 a⁻¹ (0,0033–0,0103) | **Quelle** des Zentralwerts: `docs/evidenz/60_stichprobe/m0_klassenraten.csv`, Zeile `gk3_gk4;alle`, Spalte `rate_exponiert_hqextrem_1_pro_a` (Stichprobenlauf auf den acht Anker-Kommunen, Wahl der Spalte §4.3 Punkt 3); Band **Abschätzung von KAP3**: kleinster und größter Kommunenwert derselben Spalte (Deggendorf, Grimma), Herleitung §4.3 Bandtabelle |
| \(r_{\text{GK2}}\) gemessene Klassenrate | 0,00067515 a⁻¹ (0,000301–0,001154) | **Quelle** des Zentralwerts: `docs/evidenz/60_stichprobe/m0_klassenraten.csv`, Zeile `gk2;alle`, Spalte `rate_exponiert_hqextrem_1_pro_a`, Herleitung §4.3 Punkt 3; Band **Abschätzung von KAP3**: kleinster und größter Kommunenwert derselben Spalte (Reichertshofen, Halle (Saale)), Herleitung §4.3 Bandtabelle |
| Unsicherheitsband \(\lambda\) | 0,12 bzw. 3,93 | **berechnet** aus dem fortgepflanzten Band von \(A^{*}\) und \(M_0\) (§4.4), Rundungsregel wie dort; Band des Skalars, **kein Prüfstein** (bis T-0574 als Plausibilitätsschranke geführt, Ledger-Befund 61) |
| Plausibilitätsschranke \(\lambda\) | 0,5 bzw. 2,0 | **Abschätzung von KAP3**, Herleitung §4.4: Faktor 2 um den Neutralwert 1 aus dem Modellverständnis-Argument (die Eingangsgrößen von \(M_0\) zusammen um mehr als den Faktor 2 daneben, mehr als ihre belegten Bänder gemeinsam erklären), ohne eine Größe, die in \(\lambda\) eingeht; Sensitivität Faktor 1,5 / 3 dort; gilt für den Zentralwert einer Neubestimmung, die Fenster-Sensitivität in §4.1a prüft sie an vier \(\lambda\)-Werten, alle vier innerhalb (0,500 knapp) |
| Toleranz Verteilungsprüfung | ±11,5 Prozentpunkte | **berechnet**, Herleitung §4.5: quadratische Zusammensetzung aus Jackknife-Standardfehler der Ankerreihe ±11,2 (gerechnet aus `docs/evidenz/60_gdv_jahresreihe_2002_2024.csv`), Ableseunschärfe ±1,7 und modellseitigem HQextrem-Band ±2,3; **Abschätzung von KAP3** ist daran nur die Wahl der Kombinationsregel (unabhängige Beiträge, quadratisch), vorab festgelegt. Ist-Ergebnis: Abstand 13,9 Pp, **Prüfung nicht bestanden** (Modellentscheid §4.5) |
| Toleranz Quantilvergleich | 90-%-Rangband je Rang (Rang 1: \(p\) = 0,0022–0,122 a⁻¹) | **Abschätzung von KAP3** beim Niveau 90 %, Bandgrenzen **berechnet** aus der Binomialverteilung der Rangplätze in 23 Jahren (Reihe `docs/evidenz/60_gdv_jahresreihe_2002_2024.csv`), Herleitung §4.5 „Zweite Prüfgröße"; Sensitivität: mit 80 % bleibt das Ergebnis (alle vier Ränge im Band) unverändert |
| \(U\) Sanity-Untergrenze (unabhängig) | 0,189 Mrd. €₂₀₂₆/a (0,095–0,315) | **berechnet**, Herleitung §4.6: \(E_{\text{fonds}} \cdot w \cdot f_{\text{fluss}} / N\) aus den drei Zeilen darunter; Band aus den Bandenden von \(w\) und \(f_{\text{fluss}}\), fixiert ist der Zentralwert; es fließen die Abschätzungen von KAP3 \(w\), \(f_{\text{fluss}}\) und die Fortschreibungsrate der Fondsvolumina ein |
| \(E_{\text{fonds}}\) Fondsvolumina der Wiederaufbauhilfe 2013 und 2021 | 8 und 30 Mrd. €, fortgeschrieben 10,35 + 33,12 = 43,47 Mrd. €₂₀₂₆ | **Quelle:** AufbhG 2013 § 4 Abs. 1 Satz 1 und Aufbauhilfegesetz 2021 (BGBl.), `docs/evidenz/60_wiederaufbauhilfen_2013_2021.csv`; Fortschreibung 2 %/a wie im Bericht, Herleitung §4.6 |
| Fortschreibungsrate der Fondsvolumina auf den Preisstand 2026 | 2 %/a (\(1{,}02^{13}\) = 1,294 für 2013, \(1{,}02^{5}\) = 1,104 für 2021; kein Band) | **Abschätzung von KAP3**: Setzung in §4.6, dort ohne eigenen Beleg; Sensitivität: ohne Fortschreibung (0 %/a) \(U\) = 0,165 und \(O_u\) = 10,0 Mrd. €₂₀₂₆/a, mit 3 %/a \(U\) = 0,202 und \(O_u\) = 11,59 Mrd. €₂₀₂₆/a — Lage des Ist-Werts 1,132 im Band unverändert |
| \(w\) Wohngebäudeanteil der Aufbauhilfe-Mittel | 0,11 (0,06–0,17) | **Abschätzung von KAP3, Herleitung §4.6**: 1/3 private Haushalte · 1/3 Gebäudesubstanz; Band aus Haushaltsanteil 1/4–1/2 und Gebäudeanteil 1/4–1/3 |
| \(f_{\text{fluss}}\) flussseitiger Anteil der Aufbauhilfe-Ereignisse | 0,90 (0,80–1,00) | **Abschätzung von KAP3, Herleitung §4.6**: beide Ereignisse dokumentierte Flusshochwasser, Abschlag für nicht getrennt ausgewiesene Siel- und Sturzflutanteile |
| \(N\) Länge des Ankerfensters für \(U\) | 23 a (2002–2024) | **gezählt**, dieselben Kalibrierjahre wie §4.1/§4.7; ersetzt die frühere Wiederkehrzeit \(T\) = 100 a (Abschätzung von KAP3, bis T-0574) |
| \(O_u\) Sanity-Obergrenze (unabhängig) | 11,04 Mrd. €₂₀₂₆/a | **berechnet** aus dem Fondsvolumen 2021 (33,12 Mrd. €₂₀₂₆, Quelle wie \(E_{\text{fonds}}\)) mit den oberen Enden Haushaltsanteil 1/3 und \(f_{\text{fluss}}\) 1,00, in jedem Jahr; Begründung „Mittel ≤ schwerstes Jahr des Fensters" ist eine **Abschätzung von KAP3**, Herleitung §4.6 |
| \(O_M\) Modellschranke (modellabhängig, kein Prüfstein) | 6,29 Mrd. €₂₀₂₆/a | **berechnet** aus den ZÜRS-Klassenraten (GK3/GK4 0,1 a⁻¹, GK2 0,01 a⁻¹), den Adresszahlen (Register 60-R17-01) und dem Gebäudewert 527.280 €₂₀₂₆ (Register 60-R24-01), gedeckelt mit der Schadensquote 0,250 (§3.3), Herleitung §4.6; es fließen die Abschätzungen von KAP3 der ZÜRS-/GDV-Registerabschätzungen ein; festes Vielfaches der Modellsumme (\(O_M/M_0\) = 5,06), kann nach bestandener Plausibilitätsschranke nicht auslösen |
| Gebäudewert je Wohngebäude, reiner EFH/ZFH-Satz (nur \(O_M\)) | 527.280 €₂₀₂₆ | **berechnet**: 208 m² · 1,30 · 1.950 €₂₀₂₆/m² BGF aus den Zeilen Wohnfläche je Wohngebäude, \(k_{\text{BGF}}\) und \(n_{\text{EFH/ZFH}}\), Herleitung §4.6; es fließt die Abschätzung von KAP3 \(k_{\text{BGF}}\) ein |
| Gedeckelte Schadensquote (nur \(O_M\)) | 0,250 | **Quelle:** Langbeleg B5 (Thieken u. a. 2008, Tab. 1 und Fig. 1), belegtes oberes Ende \(d_5\) der Tiefen-Schadensfunktion \(d(h)\), §3.3; geht nur in die Modellschranke \(O_M\) ein |
| \(f_{\text{AWM}}\) Alterswertminderungsfaktor (Zeitwertansatz, nur Sensitivität) | 0,55 (0,40–0,75) | **Abschätzung von KAP3** auf der Regel § 38 ImmoWertV (RND/GND, GND 80 a nach Anlage 1), Herleitung §7.2; geht nicht in den Basiswert ein; Sensitivität: K3-Betrag 0,62 (0,45–0,85) statt 1,13 Mrd. €₂₀₂₆/a (kalibrierte Bundessumme §4.6) |
| \(q_0\) Objektschutz-Anteil heute (Ende 2024) | 0,15 (0,05–0,30) | **Abschätzung von KAP3**, Herleitung §4.7 (`#q0-abschaetzung`); Datenebene geparkt (Datenquelle fehlt), Watchlist §4.7; bindet \(\Delta q \le 1 - q_0\); geht nicht in \(r_{\text{S092}}\) ein, Faktor \(1/(1 - q_0 s_{\text{bem}} e_{\text{bem}})\) = +5,5 % (+1,8 bis +11,7 %) als Modellgrenze ausgewiesen |

```python test: beispiel_60_kalibrierung
# 4.2 Zielwert aus dem Anker (Mrd. EUR2026/a)
A_ver, w_wg, u, phi, kappa, pi = 1.838, 0.65, 1.54, 0.50, 1.15, 1.07
A_stern = A_ver * w_wg * u * phi * kappa * pi
assert abs(A_stern - 1.132) < 5e-3
lo = 1.061 * 0.55 * 1.33 * 0.35 * 1.05 * 1.039
hi = 1.838 * 0.75 * 1.75 * 0.65 * 1.30 * 1.124   # pi-Band 1.0706/1.03 bis 1.1576/1.03 (B4 ungerundet)
assert abs(lo - 0.296) < 5e-3 and abs(hi - 2.291) < 5e-3

# 4.3 Modellsumme aus den gemessenen Klassenraten (docs/evidenz/60_stichprobe/m0_klassenraten.csv)
theta = 2_289_188 / 3_841_438                     # Typ-Mix EFH/ZFH, Destatis Tab. 2.1.3, 31.12.2021
assert round(theta, 3) == 0.596
theta = 0.596
n_mix = theta * 1950.0 + (1 - theta) * 1533.0    # typgewichteter Wertsatz EUR2026/m2 BGF (Befund 58)
assert abs(n_mix - 1781.532) < 1e-6
wert_geb = 208.0 * 1.30 * n_mix                  # EUR2026 je exponiertem Wohngebaeude
assert abs(wert_geb - 481726.25) < 1.0
w_wohn = 0.872                                   # Wohngebaeudeanteil je Adresse (19,7/22,6)
r_gk34 = 0.005979599550826                       # m0_klassenraten.csv, Zeile gk3_gk4;alle, Spalte rate_exponiert_hqextrem_1_pro_a
r_gk2 = 0.000675151053693                        # m0_klassenraten.csv, Zeile gk2;alle, Spalte rate_exponiert_hqextrem_1_pro_a
beitrag_gk34 = w_wohn * wert_geb * 339_000 * r_gk34 / 1e9
beitrag_gk2 = w_wohn * wert_geb * 1_380_000 * r_gk2 / 1e9
assert abs(beitrag_gk34 - 0.852) < 5e-3 and abs(beitrag_gk2 - 0.391) < 5e-3
M0 = beitrag_gk34 + beitrag_gk2
assert abs(M0 - 1.243) < 5e-3

# 4.3 M0-Band (Vorgabe P1): Bandenden der zehn Eingangsgroessen, alle gleichgerichtet
bgf_lo, bgf_hi = 1.25, 1.40
theta_lo, theta_hi = 0.471, 0.624
n_lo = theta_lo * 1890.0 + (1 - theta_lo) * 1485.0
n_hi = theta_hi * 2043.0 + (1 - theta_hi) * 1606.0
assert abs(n_lo - 1675.755) < 1e-6 and abs(n_hi - 1878.688) < 1e-6
r_gk34_lo, r_gk34_hi = 0.0033, 0.0103
r_gk2_lo, r_gk2_hi = 0.000301, 0.001154
wert_geb_lo = 208.0 * bgf_lo * n_lo
wert_geb_hi = 208.0 * bgf_hi * n_hi
term_lo = 339_000 * r_gk34_lo + 1_380_000 * r_gk2_lo
term_hi = 339_000 * r_gk34_hi + 1_380_000 * r_gk2_hi
M0_unten = w_wohn * wert_geb_lo * term_lo / 1e9
M0_oben = w_wohn * wert_geb_hi * term_hi / 1e9
assert abs(M0_unten - 0.583) < 5e-3
assert abs(M0_oben - 2.425) < 5e-3

# 4.4 Niveau-Skalar: vollstaendig fortgepflanztes Lambda-Band (Unsicherheitsband) und Plausibilitaetsschranke
lam = A_stern / M0
assert abs(lam - 0.911) < 5e-3
lam_lo = lo / M0_oben                       # unteres Lambda-Bandende (Zaehler/Nenner an den Extremen)
lam_hi = hi / M0_unten                      # oberes Lambda-Bandende
assert abs(lam_lo - 0.12) < 5e-3
assert abs(lam_hi - 3.93) < 5e-3
# Unsicherheitsband von Lambda (bis T-0574 als Schranke gefuehrt; Namen fuer die Prueffolge beibehalten)
schranke_lo, schranke_hi = round(lam_lo, 2), round(lam_hi, 2)
assert abs(schranke_lo - 0.12) < 5e-3       # Unsicherheitsband unten, kein Pruefstein (Befund 61)
assert abs(schranke_hi - 3.93) < 5e-3       # Unsicherheitsband oben, kein Pruefstein (Befund 61)
# Rechenweg-Ziffern aus dem Text (Befund 62): aus den gerundeten Bandenden gerechnet
assert abs(0.296 / 2.425 - 0.122061) < 1e-6 and abs(2.291 / 0.583 - 3.929674) < 1e-6
assert schranke_lo <= lam <= schranke_hi    # Zentralwert liegt im Unsicherheitsband
pl_lo, pl_hi = 0.5, 2.0                     # Plausibilitaetsschranke: Faktor 2 um 1, Abschaetzung von KAP3 (4.4)
assert pl_lo <= lam <= pl_hi                # Zentralwert liegt innerhalb der Schranke
assert schranke_lo < pl_lo and pl_hi < schranke_hi   # Schranke trennschaerfer als das Band

# 4.5 Verteilungspruefung Ereignisregime: Anteil ab HQ100 gegen Ankerbefund
A = [15.0, 77.76, 300.0]
def regime(p_extrem):
    p = [1.0e-1, 1.0e-2, p_extrem]
    t1 = (p[0] - p[1]) * (A[0] + A[1]) / 2
    t2 = (p[1] - p[2]) * (A[1] + A[2]) / 2
    t3 = p[2] * A[2]
    return (t2 + t3) / (t1 + t2 + t3)
anteil = regime((5.0e-3 * 1.0e-3) ** 0.5)
assert abs(anteil - 0.339) < 5e-4
assert abs(regime(1.0e-3) - 0.324) < 5e-4 and abs(regime(5.0e-3) - 0.369) < 5e-4
# Ankerseite: Jahresauslassung (Leave-one-out) ueber die 23 Jahreswerte
# docs/evidenz/60_gdv_jahresreihe_2002_2024.csv, Spalte wert_mrd_eur (2002 ... 2024)
reihe = [7.4, 0.5, 0.4, 0.9, 0.9, 1.0, 0.9, 0.68, 1.5, 1.1, 0.4, 3.9,
         1.2, 0.3, 2.0, 0.7, 1.0, 0.5, 0.4, 12.6, 0.3, 1.1, 2.6]
assert len(reihe) == 23 and abs(sum(reihe) / 23 - A_ver) < 5e-4   # Mittel = Anker aus 4.1
def loo_anteil(werte):                                   # Erwartungswertanteil ueber dem Normaljahr
    s, m = sum(werte), len(werte)
    return sum(max(0.0, x - (s - x) / (m - 1)) for x in werte) / s
anker = loo_anteil(reihe)
assert abs(anker - 0.4774) < 5e-4
assert abs(loo_anteil([3.0 * x for x in reihe]) - anker) < 1e-12   # skaleninvariant: kein Niveau
# Toleranz vorab: Jackknife-Streuung + Ableseunschaerfe + Modellband, quadratisch (4.5)
repl = [loo_anteil(reihe[:i] + reihe[i + 1:]) for i in range(23)]
mittel = sum(repl) / 23
se = (22 / 23 * sum((x - mittel) ** 2 for x in repl)) ** 0.5 * 100
assert abs(se - 11.16) < 5e-2
def versetzt(vz):                                        # +-0,05 Mrd. EUR je Balken, unguenstigstes Muster
    s = sum(reihe)
    return [max(0.0, x + vz * 0.05) if x > (s - x) / 22 else max(0.0, x - vz * 0.05)
            for x in reihe]
ablese = max(abs(loo_anteil(versetzt(1)) - anker), abs(loo_anteil(versetzt(-1)) - anker)) * 100
assert abs(ablese - 1.73) < 5e-2
toleranz = (se ** 2 + ablese ** 2 + 2.3 ** 2) ** 0.5
assert abs(toleranz - 11.5) < 5e-2
# Ergebnis: Abstand groesser als die Toleranz -> Pruefung nicht bestanden (Modellentscheid 4.5)
abstand = abs(anker - anteil) * 100
assert abs(abstand - 13.88) < 5e-2 and abstand > toleranz
# Ausgewiesene Anteile auf zwei Stellen: Summe 100, seltenes Regime = Summe seiner Teile (Befund 65)
p3 = (5.0e-3 * 1.0e-3) ** 0.5
tau = [(1.0e-1 - 1.0e-2) * (A[0] + A[1]) / 2, (1.0e-2 - p3) * (A[1] + A[2]) / 2, p3 * A[2]]
proz = [round(100 * x / sum(tau), 2) for x in tau]
assert proz == [66.14, 23.23, 10.63] and abs(sum(proz) - 100.0) < 1e-9
assert round(proz[1] + proz[2], 2) == round(100 * anteil, 2) == 33.86
assert round(100 * anker, 2) == 47.74 and round(47.74 - 33.86, 2) == 13.88
assert abs(sum(max(0.0, x - (sum(reihe) - x) / 22) for x in reihe) - 20.186) < 5e-4

# 4.5 zweite Pruefgroesse: Quantilvergleich der hoechsten Jahre (Befund 63)
def kurve(q, a3=300.0):                                  # D(p) aus 3.4 Schritt 2
    s = [15.0, 77.76, a3]
    if q > 1.0e-1:
        return 0.0                                       # haeufiger als HQhaeufig: nicht kartiert
    if q >= 1.0e-2:
        return s[0] + (1.0e-1 - q) / (1.0e-1 - 1.0e-2) * (s[1] - s[0])
    if q >= p3:
        return s[1] + (1.0e-2 - q) / (1.0e-2 - p3) * (s[2] - s[1])
    return s[2]
def flaeche(a3=300.0):
    return ((1.0e-1 - 1.0e-2) * (15.0 + 77.76) / 2 + (1.0e-2 - p3) * (77.76 + a3) / 2 + p3 * a3)
assert abs(flaeche() - sum(tau)) < 1e-12
def rangband(i, n=23, niveau=0.90):                     # Binomialverteilung der Rangplaetze
    from math import comb
    def ueber(x):
        return sum(comb(n, k) * x ** k * (1 - x) ** (n - k) for k in range(i, n + 1))
    grenzen = []
    for ziel in ((1 - niveau) / 2, (1 + niveau) / 2):
        lo_, hi_ = 0.0, 1.0
        for _ in range(200):
            mid = (lo_ + hi_) / 2
            lo_, hi_ = (mid, hi_) if ueber(mid) < ziel else (lo_, mid)
        grenzen.append((lo_ + hi_) / 2)
    return grenzen
sortiert = sorted(reihe, reverse=True)
def quantilvergleich(a3=300.0, niveau=0.90):
    zeilen = []
    for i in range(1, 5):
        x = sortiert[i - 1]
        q_anker = x / ((sum(reihe) - x) / 22)
        p_u, p_o = rangband(i, niveau=niveau)
        band = (kurve(p_o, a3) / flaeche(a3), kurve(p_u, a3) / flaeche(a3))
        zeilen.append((q_anker, kurve(i / 24, a3) / flaeche(a3), p_u, p_o, band))
    return zeilen
qv = quantilvergleich()
soll = [(9.34, 8.82, 0.0022, 0.122, 47.5), (4.67, 4.22, 0.016, 0.190, 11.7),
        (2.24, 0.0, 0.037, 0.249, 9.39), (1.44, 0.0, 0.062, 0.304, 6.61)]
for (q_a, q_m, p_u, p_o, band), (s_a, s_m, s_u, s_o, s_hi) in zip(qv, soll):
    assert abs(q_a - s_a) < 5e-3 and abs(q_m - s_m) < 5e-3
    assert abs(p_u - s_u) < 5e-4 and abs(p_o - s_o) < 5e-3
    assert band[0] == 0.0 and abs(band[1] - s_hi) < 5e-2 * max(1.0, s_hi / 10)
    assert band[0] <= q_a <= band[1]                     # bestanden auf allen vier Raengen
# Trennschaerfe: Verdopplung, Verdreifachung, Halbierung von A_3 und Niveau 80 % bestehen ebenso
for a3 in (600.0, 900.0, 150.0):
    assert all(b[0] <= q <= b[1] for q, _, _, _, b in quantilvergleich(a3))
# Ableseunschaerfe Rang 1 (+-0,05 je Balken, unguenstigstes Muster): 8,97 bis 9,74
rest1 = sum(reihe) - sortiert[0]
assert abs((sortiert[0] - 0.05) / ((rest1 + 22 * 0.05) / 22) - 8.97) < 5e-3
assert abs((sortiert[0] + 0.05) / ((rest1 - 22 * 0.05) / 22) - 9.74) < 5e-3
assert all(b[0] <= q <= b[1] for q, _, _, _, b in quantilvergleich(niveau=0.80))
assert abs(quantilvergleich(niveau=0.80)[0][4][0] - 2.90) < 5e-3
assert abs(quantilvergleich(niveau=0.80)[0][4][1] - 36.9) < 5e-2
assert [round(z[1], 2) for z in quantilvergleich(600.0)[:2]] == [6.83, 3.27]
assert [round(z[1], 2) for z in quantilvergleich(900.0)[:2]] == [5.58, 2.67]

# 4.6 Sanity-Band und Lage der kalibrierten Bundessumme (Befunde 35, 64, 96, 97)
E_2013 = 8.0 * 1.02 ** 13                    # Fondsvolumen 2013, fortgeschrieben
E_2021 = 30.0 * 1.02 ** 5                    # Fondsvolumen 2021, fortgeschrieben
E_fonds = E_2013 + E_2021
assert abs(E_2013 - 10.35) < 5e-3 and abs(E_2021 - 33.12) < 5e-3 and abs(E_fonds - 43.47) < 5e-3
w_u, f_fluss, N_fenster = (1 / 3) * (1 / 3), 0.90, 2024 - 2002 + 1
U = E_fonds * w_u * f_fluss / N_fenster      # unabhaengige Untergrenze
U_lo = E_fonds * (1 / 4) * (1 / 4) * 0.80 / N_fenster
U_hi = E_fonds * (1 / 2) * (1 / 3) * 1.00 / N_fenster
assert abs(U - 0.189) < 5e-4 and abs(U_lo - 0.095) < 5e-4 and abs(U_hi - 0.315) < 5e-4
O_u = E_2021 * (1 / 3) * 1.00                # unabhaengige Obergrenze (Mittel <= schwerstes Jahr)
assert abs(O_u - 11.04) < 5e-3
n_gk34, n_gk2 = 339_000 * 0.1, 1_380_000 * 0.01
O_M = (n_gk34 + n_gk2) * (208.0 * 1.30 * 1950.0) * 0.250 / 1e9   # Modellschranke, reiner EFH/ZFH-Satz
assert abs(O_M - 6.29) < 5e-2 and abs(O_M / M0 - 5.06) < 5e-3
assert 2.0 * M0 < O_M                        # O_M kann nach bestandener Schranke nicht ausloesen
assert U <= lam * M0 <= O_u and lam * M0 <= O_M
assert abs(lam * M0 / U - 6.0) < 5e-2 and abs(O_u / (lam * M0) - 9.8) < 5e-2
assert abs(O_u / U - 58.4) < 5e-2 and abs(6.29 / 0.0103 - 610.7) < 5e-2 and abs(2.264 / 0.64 - 3.54) < 5e-3

# 4.8 P1-Zeilen (Befunde 37, 88): Zwischenwerte und Sensitivitaet der Fortschreibungsrate
assert abs(208.0 * 1.30 * 1950.0 - 527280.0) < 1e-6          # Gebaeudewert reiner EFH/ZFH-Satz (O_M)
assert abs(wert_geb_lo - 435696.30) < 1e-2 and abs(wert_geb_hi - 547073.95) < 1e-2
def U_rate(r):                                                # Fondsvolumina mit Fortschreibungsrate r
    return (8.0 * (1 + r) ** 13 + 30.0 * (1 + r) ** 5) * w_u * f_fluss / N_fenster
assert abs(U_rate(0.02) - U) < 1e-12
assert abs(U_rate(0.0) - 0.165) < 5e-4 and abs(U_rate(0.03) - 0.202) < 5e-4
assert abs(30.0 / 3 - 10.0) < 1e-12 and abs(30.0 * 1.03 ** 5 / 3 - 11.59) < 5e-3
assert U_rate(0.03) <= lam * M0 <= 30.0 / 3                   # Lage des Ist-Werts im Band unveraendert
```

## 5 Maßnahmen-Hebel (§2.5/§3.5)

<!--
Pflichtinhalte: Hebel nur an Ketten-Sensitivitäten; Effektgrößen aus Interventions-/
quasi-experimenteller Evidenz; marginal gegenüber heute; Doppelzählungs-Wächter gegen die
Kalibrierjahre; Wirkungsort definieren; R7-Weiche referenzieren (Schutzsysteme #50; Objektschutz
als K8-Maßnahmenkosten). Hebel ohne Effektgröße: Abschätzung nach P2 (nie Wirkung null).
Offene Hebel-Kandidaten: S096/S097/S098 (über R7-Erwartungswert mit #50). S093/S094 sind keine
Hebel-Kandidaten, sondern Struktur-Achsen (sichtbarer Absatz „Nicht als Hebel geführt" unten).
-->

**Nicht als Hebel geführt: S093 Gebäudezustand und S094 Baumaterial.** Beide Knoten wirken im
heutigen Modell **nicht als Maßnahme**, sondern als Struktur-Achsen der Schadensfunktion: Sie
beschreiben, wie stark ein Gebäude bei gleicher Wassertiefe beschädigt wird, und sind um 1,00
zentriert, verschieben den Basiswert also nicht (§3.2, §3.5). Ihre Wirkung ist nicht null gesetzt,
sondern als Abschätzung von KAP3 mit Wert, Band und Sensitivität ausgewiesen — Registerzeilen
**60-S093-01** (Zustand, \(f_{\text{S093}}\) = 1,00, Band **0,71–1,40**, Sensitivität −29 %/+40 % auf den Schadensgrad) und **60-S094-01**
(Material, \(f_{\text{S094}}\) = 1,00, Band **0,84–1,18**, Sensitivität −16 %/+18 % auf den
Schadensgrad), gemeinsam multiplikativ **0,60–1,66** (Kap. 2, Langbelege B5/B6, §3.5). Die
Datenebene GEBAEUDEZUSTAND_BAUSTOFF ist **geparkt** (§3.2): Es gibt keine bundesweite offene
Erhebung von Bauzustand und Baumaterial je Zelle. **Ein Hebel würde daraus erst**, wenn diese
Zell-Merkmale verfügbar sind — dann ließe sich eine Maßnahme (etwa Sanierung oder
wasserbeständige Baustoffe beim Umbau) als Verschiebung der Klassenanteile rechnen. Bis dahin bleiben
beide Knoten Unsicherheit der Schadensfunktion, kein Maßnahmen-Hebel. Die Schutzsysteme S096–S098
sind ebenfalls kein Hebel dieses Berichts; sie sollen über die R7-Weiche mit #50 anschließen
(Kap. 1).

<a id="s092-wirkung"></a>

### 5.1 Wirkungsabschätzung S092 Objektschutz der Eigentümer (Anker `#s092-wirkung`) — §3.9 **ABGESCHÄTZT**

**Anlass (Vorgabe P2, §3.5).** Für den Hebel „bauliche Vorsorge der Eigentümer“ (S092) ist im
Erstaufschlag keine Interventions- oder quasi-experimentelle Effektgröße belegt. Befragungen
Betroffener nach Hochwasserereignissen vergleichen vorsorgende und nicht vorsorgende Haushalte im
Querschnitt. Das ist nach §3.5 keine Maßnahmen-Effektgröße (Selbstselektion); die im Bericht
volltextgeprüfte Befragung Thieken u. a. 2008 (Tab. 2, Langbeleg B5) dient deshalb nur als
Plausibilitätsprobe der Kette (Kap. 2, Zeile 60-S092-01), nicht als Wert. Der Hebel wird deshalb **nicht mit Wirkung null**
geführt, sondern mit der folgenden **Abschätzung von KAP3**. Im Produkt ist sie als solche samt
dieser Herleitung auszuweisen (P1).

**Wirkungsort.** Multiplikativ auf den K3-Erwartungsschaden von #60 der Kommune:
\(\text{EAD}_{\text{mit}} = \text{EAD} \cdot (1 - r_{\text{S092}})\). Nur K3; die Kosten des
Objektschutzes sind K8-Maßnahmenkosten und schließen den verhinderten Schaden je Gebäude aus (R7).

**Kette.** \(r_{\text{S092}} = \Delta q \cdot s_{\text{bem}} \cdot e_{\text{bem}}\)

### 5.1.1 Zeichentabelle (Kette S092)

Die vollständige Zeichentabelle beider Kapitel steht in Abschnitt 3.5; hier stehen dieselben
Zeichen der S092-Kette noch einmal mit ihren Werten und Bändern, ergänzt um die beiden Zeichen der
Wirkungsformel \(\text{EAD}_{\text{mit}} = \text{EAD}\cdot(1 - r_{\text{S092}})\).

| Zeichen | Name | Einheit | Wert/Herkunft |
|---|---|---|---|
| \(\text{EAD}\) | jährlicher Erwartungsschaden des Kontos K3 aus flussseitiger Überflutung **ohne** den Hebel — native Ergebnisgröße, Bezugsjahr und Preisstand 2026, Betrachtungsebene Kommune | €₂₀₂₆/a | herleitung: §3.1 und §3.4 Schritt 3 — \(\text{EAD} = \text{EAD}_k = \sum_{z \in k} \bar A_z w_z\) (Aggregation §3.6); Zeichentabelle §3.5 |
| \(\text{EAD}_{\text{mit}}\) | Erwartungsschaden derselben Kommune, desselben Kontos K3 und desselben Bezugsjahres 2026 **nach** Umsetzung von S092 | €₂₀₂₆/a | herleitung: §5.1 — \(\text{EAD}\cdot(1 - r_{\text{S092}})\), Wirkungsort nur K3 (K8-Kosten ausgeschlossen, R7); Zeichentabelle §3.5 |
| \(\Delta q\) | zusätzlich nachgerüsteter Anteil exponierter Gebäude (marginal gegenüber heute) | – | 0,10 (Band 0,05–0,20) · herleitung:#s092-wirkung — Abschätzung von KAP3, keine Primärquelle (§5.1.2) |
| \(e_{\text{bem}}\) | Schadensminderung am nachgerüsteten Gebäude, solange der Wasserstand das Bemessungsniveau nicht übersteigt | – | 0,70 (Band 0,50–0,80) · herleitung:#s092-wirkung — Abschätzung von KAP3, keine Primärquelle (§5.1.2) |
| \(r_{\text{S092}}\) | relative Minderung des K3-Erwartungsschadens von #60 durch S092 | – | 0,035 (Band 0,0075–0,0832) · herleitung:#s092-wirkung — berechnet aus \(\Delta q \cdot s_{\text{bem}} \cdot e_{\text{bem}}\) (§5.1.2) |
| \(s_{\text{bem}}\) | Anteil der Schadenssumme aus Ereignissen unterhalb des Bemessungsniveaus | – | 0,50 (Band 0,30–0,52) · herleitung:#s-bem-naeherung — Abschätzung von KAP3, keine Primärquelle; ausdrücklich **Näherung**, Richtung: **überschätzt** den Hebel (§5.1.3) |

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
- \(s_{\text{bem}}\) = 0,50 (0,30–0,52). Annahme: Schadenssummen verteilen sich auf häufige flache
  und seltene tiefe Überflutungen. Oberhalb der Schutzhöhe wird Objektschutz überströmt und wirkt
  praktisch nicht. Der Wert ist **nicht empirisch bestimmt, sondern ausdrücklich eine Näherung**;
  ihr Status, die Begründung ihrer oberen Bandgrenze und die **Richtung** ihres Fehlers stehen in
  Abschnitt 5.1.3 (`#s-bem-naeherung`).

Die Marginalität von \(\Delta q\) ist an die Kalibrierjahre gebunden: Gezählt wird allein die
Nachrüstung **nach dem letzten Kalibrierjahr 2024**, weil der bis dahin vorhandene Objektschutz im
Anker und damit im Niveau-Skalar steckt (Doppelzählungs-Wächter, §4.7). Der Referenzzustand, gegen
den „marginal" gemessen wird, ist der heutige Ausstattungsgrad \(q_0\) = 0,15 (Band 0,05–0,30;
Abschätzung von KAP3, Herleitung §4.7 `#q0-abschaetzung`): Nachrüsten lässt sich nur ein bisher
ungeschütztes Gebäude, also gilt \(\Delta q \le 1 - q_0\) (am ungünstigsten Bandende
0,20 ≤ 0,70), und \(\Delta q\) = 0,10 ist rund ein Achtel des ungeschützten Bestands. Dass die
ungeschützten Gebäude mehr als ihren Kopfanteil am Erwartungsschaden tragen, rechnet die Kette nicht
ein; der Hebel wäre damit um 5,5 % größer (Band +1,8 bis +11,7 %, Modellgrenze 4 unten).

Rechnung: \(r_{\text{S092}}\) = 0,10 · 0,50 · 0,70 = **0,035**. Band (alle Enden gleichgerichtet):
0,05 · 0,30 · 0,50 = **0,0075** bis 0,20 · 0,52 · 0,80 = **0,0832**.

**Ergebnis-Sensitivität.** Der ausgewiesene Maßnahmeneffekt ist −3,5 % des K3-Erwartungsschadens
von #60 (Band −0,75 % bis −8,32 %). Die Kette ist linear, jeder Faktor hat Elastizität 1. Einzeln
variiert: \(\Delta q\) 0,05–0,20 ⇒ r 0,0175–0,070 (größte Achse); \(s_{\text{bem}}\) 0,30–0,52 ⇒ r
0,021–0,0364; \(e_{\text{bem}}\) 0,50–0,80 ⇒ r 0,025–0,040.

**Modellgrenzen der Abschätzung.** (1) Kommunenweiter Pauschalfaktor statt zellscharfer Wirkung
(Bauform-Grenze). (2) \(s_{\text{bem}}\) ist messbar, sobald Wassertiefen je HQ-Szenario als Ebene
vorliegen (§3.1). Dann wird er gemessen statt genähert (Ersetzungspfad, W1; der Näherungscharakter
und seine Fehlerrichtung stehen bis dahin in §5.1.3). (3) Ersetzt wird die
ganze Abschätzung, sobald eine Interventions- oder quasi-experimentelle Effektgröße gefunden ist
(§3.8-Recherche offen). (4) Wirkung nur auf den ungeschützten Teil: Die Kette rechnet mit dem
Kopfanteil der nachgerüsteten Gebäude am Erwartungsschaden, nicht mit ihrem höheren Anteil als
bisher ungeschützte Gebäude. Mit \(q_0\) = 0,15 unterschätzt sie den Hebel um den Faktor
1 ÷ (1 − 0,15 · 0,50 · 0,70) = 1,055 (+5,5 %; Band von \(q_0\): +1,8 bis +11,7 %) — Gegenrichtung zu
\(s_{\text{bem}}\), Herleitung §4.7 `#q0-abschaetzung`.

```python test: beispiel_60_s092_abschaetzung
dq, s_bem, e_bem = 0.10, 0.50, 0.70
r = dq * s_bem * e_bem
assert abs(r - 0.035) < 1e-12
lo, hi = 0.05 * 0.30 * 0.50, 0.20 * 0.52 * 0.80
assert abs(lo - 0.0075) < 1e-12 and abs(hi - 0.0832) < 1e-12
# obere Bandgrenze von s_bem aus dem Ankerwert der Verteilungspruefung 4.5 (5.1.3)
assert abs(0.10 * 0.52 * 0.70 - 0.0364) < 1e-12
assert abs(0.05 * s_bem * e_bem - 0.0175) < 1e-12 and abs(0.20 * s_bem * e_bem - 0.070) < 1e-12
# q0 (Abschaetzung 4.7): Bindung dq <= 1 - q0 und Modellgrenze 4 (ungeschuetzter Teil)
q0, q0_lo, q0_hi = 0.15, 0.05, 0.30
assert 0.20 <= 1 - q0_hi and abs(dq / (1 - q0) - 0.118) < 5e-4
f = lambda q: 1 / (1 - q * s_bem * e_bem)
assert abs(f(q0) - 1.055) < 5e-4 and abs(f(q0_lo) - 1.018) < 5e-4 and abs(f(q0_hi) - 1.117) < 5e-4
assert abs(r * f(q0) - 0.0369) < 5e-5 and abs(r * f(q0_hi) - 0.0391) < 5e-5
assert r * f(q0_hi) < hi                     # liegt im Band von r_S092
```

<a id="s-bem-naeherung"></a>

### 5.1.3 \(s_{\text{bem}}\) — ausgewiesene Näherung mit Richtung (Anker `#s-bem-naeherung`)

**Status: Näherung, nicht Messwert** (Befund 10 im Ledger). \(s_{\text{bem}}\) ist eine
Quantilsgröße der Tiefen- und Schadensverteilung; §3.2 verlangt für solche Größen „empirische
Quantile … statt Verteilungsannahmen". Empirisch bestimmbar ist sie erst, wenn die Wassertiefen je
HQ-Szenario zellscharf vorliegen — Ebene **HQ_TIEFE**, Stand „neu anzulegen" (Abschnitt 3.2). Diese
Ebene existiert im heutigen Modellstand nicht, es gibt für \(s_{\text{bem}}\) also keine Quelle und
kein Messergebnis (§3.9). Der Wert 0,50 wird deshalb **nicht länger als „gesetzte Mitte" geführt,
sondern ausdrücklich als Näherung** — mit Obergrenze und Fehlerrichtung. Wird er später bestimmt,
geschieht das auf **Stichproben** der HQ-Szenarien, nie in einem nationalen 100-m-Vollraster-Lauf
(Ressourcen-Regel §3.4; vgl. Abschnitt 4.3).

**Profilabhängige Illustration: Anteil unterhalb HQ100 in der Beispielzelle (Befund 26).** Allgemein
gilt nur die Ungleichung, nicht ihr Zahlenwert: Solange das Bemessungsniveau privaten
Objektschutzes nicht über dem HQ100-Wasserstand liegt (Absatz „Richtung des Fehlers“), kann
\(s_{\text{bem}}\) den Anteil der Schadenssumme **unterhalb HQ100** nicht übersteigen. Wie groß
dieser Anteil ist, hängt aber vom Betroffenheits- und Tiefenprofil der Zelle ab und ist **keine
Eigenschaft der Formel**. Zur Veranschaulichung dient die Beispielzelle aus Abschnitt 3.4
(„Rechenbeispiel (eine Zelle)“, physische Zwischengrößen 15,0 / 77,76 / 300,0 m² je Ereignis;
Trapez-Erwartungswert über die drei HQ-Stützstellen wie in §3.4 Schritt 2): Sie liefert die
Beiträge zum Erwartungsschaden \(\tau_1 = 4{,}174\) (zwischen HQhäufig und HQ100), \(\tau_2 = 1{,}466\)
und \(\tau_3 = 0{,}671\) (jeweils jenseits HQ100; Zeichen in §3.5), Summe \(6{,}311\) (= \(\bar A_z\) = 6,31 m²/a aus
§3.4), und damit einen Anteil unterhalb HQ100 von \(4{,}174 / 6{,}311 = 0{,}661\). Derselbe Ausdruck
ergibt für andere Profile mit denselben Jährlichkeiten und derselben Schadensfunktion 0,856 (Zelle
durchgehend in der Aue, \(a = 1{,}0\) in allen drei Szenarien), 0,327 (Auenrand,
\(a\) = 0,02 / 0,20 / 1,00) und 0,000 (nur im Extremfall betroffen). Der Wert 0,661 ist deshalb
**eine profilabhängige Illustration, keine Obergrenze** von \(s_{\text{bem}}\); er trägt kein
Bandende.

**Tragende Begründung der oberen Bandgrenze: Ankerwert der Verteilungsprüfung (§4.5).**
\(s_{\text{bem}}\) wird als **kommunenweiter Pauschalfaktor** geführt (Modellgrenze 1 in §5.1.2),
seine Bandgrenze muss also für den Durchschnitt der Schadenssumme gelten, nicht für eine Zelle. Den
einzigen zellunabhängigen Messwert für den Anteil des seltenen Regimes liefert die **Ankerseite**
der Verteilungsprüfung (§4.5): In der Jahresauslassung über die Reihe 2002–2024 entfallen auf den
Überschuss der Großereignis-Jahre über das jeweilige Normaljahr **47,74 %** der Schadenssumme
(20,186 ÷ 42,28, GDV-Naturgefahrenstatistik, §4.1; Ledger-Befunde 33 und 65). Auf die Ereignisse
unterhalb des seltenen Regimes entfallen damit 1 − 0,4774 = 0,5226 der Schadenssumme. Weil
\(s_{\text{bem}}\) nach der Ungleichung oben nicht über diesem Anteil liegen kann, setzt KAP3 die
**obere Bandgrenze auf 0,52** (0,5226 auf zwei Stellen gerundet). Diese Grenze ist eine
**Abschätzung von KAP3 (§3.9)**, keine harte Grenze: Sie stützt sich auf gepoolte fluviale und
pluviale Schäden und auf die Gleichsetzung „Überschuss über dem Normaljahr“ ≈ „Beitrag des seltenen
Regimes“, und einzelne Kommunen mit tiefem Auenprofil können darüber liegen (Illustration oben:
0,856). Das ist eine Modellgrenze des Pauschalfaktors, nicht der Kette.
**Nachzug (T-0577, Ledger-Befund 66).** Bis T-0577 stand hier 0,62 aus dem Überschuss des
Einzeljahres 2024 (1,0 ÷ 2,6 = 38,5 %, also 1 − 0,385 = 0,615). Dieser Anker ist mit Befund 33
abgelöst; die Grenze ist jetzt an allen Stellen auf 0,52 gesenkt. Die untere Bandgrenze 0,30 bildet
die Fehlerrichtung ab (Absatz „Richtung des Fehlers“).

**Punktwert 0,50 bleibt — begründet, nicht still.** Mit der Obergrenze 0,52 liegt 0,50 bei 96 % des
oberen Bandendes; das Band ist damit fast nur noch nach unten offen. Das ist gewollt: Die Näherung
überschätzt den Hebel (Absatz „Richtung des Fehlers“), der wahre Wert liegt eher unter 0,50, und
genau diese Richtung bildet ein nach unten gestrecktes Band ab. Ein gesenkter Punktwert (etwa die
Bandmitte 0,41) würde eine Messung vortäuschen, die es nicht gibt, und den ausgewiesenen Hebel
0,035 ändern, ohne dass eine neue Information vorliegt. Der Punktwert 0,50 ist deshalb als
**oberer Näherungswert** zu lesen, nicht als Mitte.

**Folge für das Band.** \(s_{\text{bem}}\) = 0,50 (Band **0,30–0,52**) und daraus
\(r_{\text{S092}}\) = 0,035 (Band 0,0075–**0,0832**, also −0,75 % bis −8,32 % des
K3-Erwartungsschadens), Einzelachsen-Sensitivität \(s_{\text{bem}}\) 0,30–0,52 ⇒ r 0,021–0,0364.
Gegenüber der Fassung bis T-0577 (0,30–0,62, 0,0075–0,0992, 0,021–0,043) sinkt die Obergrenze von
\(r_{\text{S092}}\) um 16,1 %. Diese Werte stehen gleichlautend in Kap. 1 (Knoten-Bilanz), Kap. 2
(Registerzeile 60-S092-01, auch in `docs/evidenz/register.md`), den Zeichentabellen §3.5/§5.1.1,
§5.1.2 samt Beispielblock `beispiel_60_s092_abschaetzung`, den Parameter-Blöcken
`flood_bldg.s_bem` und `flood_bldg.r_s092` in Kap. 7 und im Entscheidungslog Nr. 3. Die Wirkung von
S092 bleibt eine ausgewiesene Abschätzung mit Zahlenwert, Band und Sensitivität (Vorgabe P2).

**Richtung des Fehlers: die Näherung überschätzt den Hebel.** Das Bemessungsniveau privaten
Objektschutzes (Abdichtung, Rückstausicherung, angepasste Nutzung) liegt bei wenigen Dezimetern
Wassertiefe und damit deutlich unterhalb des HQ100-Wasserstands; der Anteil der Schadenssumme
unterhalb dieses Niveaus ist zwangsläufig **kleiner** als der Anteil unterhalb HQ100 desselben Profils. Hinzu kommt,
dass die Schadensfunktion \(d(h)\) über die Tiefenachse multiplikativ wächst (Abschnitt 3.3: 0,035
bei 0,10 m auf 0,250 bei 1,75 m, +12,7 % je 10 cm) und das flächengewichtete Tiefenmittel der
LAWA-Klassen schon in der zweiten Klasse über 0,5 m liegt — der Euro-Schaden ist also zu den tiefen,
vom Objektschutz **nicht** gedeckten Ereignissen hin gewichtet. Beides zeigt in dieselbe Richtung:
Der wahre Anteil liegt eher unter als über der Näherung 0,50. Folge für das Ergebnis: Die Näherung
**überschätzt** \(r_{\text{S092}}\) und damit die Wirkung des Hebels; der ausgewiesene Punktwert
−3,5 % ist nach oben gerichtet zu lesen, die untere Bandgrenze \(s_{\text{bem}} = 0{,}30\)
(⇒ \(r_{\text{S092}} = 0{,}021\)) bildet diese Richtung ab. Eine **Unter**schätzung wäre nur
möglich, wenn Objektschutz regelmäßig über das HQ100-Niveau hinaus bemessen würde; das ist für
private Einzelmaßnahmen ausgeschlossen (dafür stehen die Schutzsysteme #50, R7-Weiche).

**Was die Näherung ablöst.** Sobald HQ_TIEFE vorliegt, wird \(s_{\text{bem}}\) aus den
szenariogewichteten Schadenssummen unterhalb des unterstellten Bemessungsniveaus **gemessen**
(Rechenweg: derselbe Trapez-Aufbau wie in Abschnitt 3.4 Schritt 2, nur mit dem Bemessungsniveau als
Schnittgrenze statt HQ100) und ersetzt Wert **und** Band; der Ersetzungspfad ist in den
Modellgrenzen dieses Abschnitts (Punkt 2) und als W1-Fall geführt.

```python test: beispiel_60_s_bem_obergrenze
# Anteil unterhalb HQ100 ist profilabhaengig (Illustration, Beispielzelle 3.4) -> traegt kein Bandende
p = [1.0e-1, 1.0e-2, (5.0e-3 * 1.0e-3) ** 0.5]
def anteil_unter_hq100(A):
    t1 = (p[0] - p[1]) * (A[0] + A[1]) / 2
    t2 = (p[1] - p[2]) * (A[1] + A[2]) / 2
    t3 = p[2] * A[2]
    return t1 / (t1 + t2 + t3), t1, t1 + t2 + t3
s_zelle, t1, summe = anteil_unter_hq100([15.0, 77.76, 300.0])      # Beispielzelle 3.4
assert abs(t1 - 4.174) < 5e-4 and abs(summe - 6.311) < 5e-4 and abs(s_zelle - 0.661) < 5e-4
s_aue = anteil_unter_hq100([1200 * 1.00 * 0.081, 1200 * 1.00 * 0.250, 1200 * 1.00 * 0.250])[0]
s_rand = anteil_unter_hq100([1200 * 0.02 * 0.050, 1200 * 0.20 * 0.081, 1200 * 1.00 * 0.250])[0]
s_extrem = anteil_unter_hq100([0.0, 0.0, 300.0])[0]
assert abs(s_aue - 0.856) < 5e-4 and abs(s_rand - 0.327) < 5e-4 and s_extrem == 0.0
# tragende obere Bandgrenze: Ankerwert der Verteilungspruefung 4.5 (Jahresauslassung 2002-2024)
anteil_unter_selten = 1 - 20.186 / 42.28
assert abs(anteil_unter_selten - 0.5226) < 5e-5
s_bem_band = (0.30, round(anteil_unter_selten, 2))   # Band aus 5.1.1 / Parameter-Block flood_bldg.s_bem
assert s_bem_band == (0.30, 0.52)
assert s_bem_band[0] < 0.50 < s_bem_band[1]      # Naeherung liegt im Band
assert abs(0.50 / s_bem_band[1] - 0.96) < 5e-3   # Punktwert bei 96 % der Obergrenze
assert abs(0.10 * 0.30 * 0.70 - 0.021) < 1e-12   # untere Bandgrenze bildet die Richtung ab
assert abs(0.20 * s_bem_band[1] * 0.80 - 0.0832) < 1e-12   # obere Grenze von r_S092
assert abs(0.10 * s_bem_band[1] * 0.70 - 0.0364) < 1e-12   # Einzelachse s_bem, obere Grenze
assert abs(1 - 0.0832 / 0.0992 - 0.161) < 5e-4   # Senkung der Obergrenze gegen die Fassung bis T-0577
```

## 6 Szenario-Anwendung & Modellgrenzen (§3.2/§3.6)

**Szenario-Anwendung 60-A.** Verschoben wird ausschließlich die Hazard-Achse **FS-Hazard**: die
drei Szenario-Stützstellen \(p(\text{HQ})\) und die zugehörige Wassertiefe je Zelle (Register
60-W085-01), fortgeschrieben auf die im Szenariojahr projizierten Jährlichkeiten der
HQ-Kartierung — der Kanal, über den E12 (Schneeschmelze), E07 (Nässe) und E08 (Starkregen, Anteil
über W085) laut Knoten-Bilanz in Kapitel 1 ausschließlich wirken (Kein-Doppelkanal §3.2). **Konstant
gehalten** werden: die Geländehöhe/Topographie S074 (die Wassertiefe entsteht nach Abschnitt 3.3
zellweise aus Wasserspiegellage minus DGM1; das DGM1 selbst schreibt sich nicht mit dem Szenario
fort), der Gebäudebestand R24 in seiner heutigen Menge und Wertdichte (Mengengerüst 60-R24-01), die
Wassertiefe-Schadensfunktion \(d(h)\) samt ihrer Zustands- und Materialbänder S093/S094 und der
Maßnahmen-Hebel S092 (§5.1). **Stationaritätsannahmen:** (1) die HWGK-Wassertiefenklassen und das
DGM1 werden für das Szenariojahr unverändert aus der heutigen Kartierung übernommen (Kap. 2,
60-W085-01/60-S074-01) — ein Wandel der Gewässermorphologie oder der Deichlinien liegt außerhalb
des Modells und wird nicht unterstellt; (2) die Schadensfunktion \(d(h)\) gilt als zeitinvariant,
ihre Zustands- und Materialbänder bilden nur den heutigen Bestandsmix ab, nicht eine künftige
Bauweise. **Bestandsdynamik S104** (Formelstelle FS-Bestandsdynamik, Registerzeile 60-S104-01,
Stand „bewusst inaktiv (geparkt)“): Investitionen der Bau- und Immobilienwirtschaft in exponierten Gebieten fließen im
heutigen Modellstand **nicht** als eigener Pfad ein — der Gebäudebestand R24 wird für das
Szenariojahr auf dem zuletzt fortgeschriebenen Stand konstant gehalten, nicht mit einer eigenen
Wachstums- oder Rückbaurate versehen. Das ist eine bewusste Vereinfachung mangels belegter oder
abgeschätzter Größe, keine Aussage, dass Investitionstätigkeit die Exposition nicht verändert:
Sobald 60-S104-01 eine rechnende Entscheidung trägt, bindet sie an FS-Bestandsdynamik und geht als eigener
Faktor in die Aggregation nach Abschnitt 3.6 ein, ohne die Kernformel aus Abschnitt 3.4 selbst zu
ändern.

**Modellgrenzen (dokumentiert):**

1. **Untergrenze (Konto):** Nur K3 ist aktiv. Folgen desselben Hochwasser-Ereignisses in K1
   (Personenschäden, #101), K4 (Infrastruktur, #74), K5 (Betriebsunterbrechung) und K8
   (Schutzkosten, #50) sind **nicht enthalten** (Kap. 1, Abschnitt „Konto-Einbettung"; §3.6).
2. **Bauform-Grenze der Materialabschätzung S094 (§3.9):** Die Materialachse der Schadensfunktion ist
   eine Abschätzung von KAP3 (Register 60-S094-01, Band 0,84–1,18), weil die zugrunde liegende
   Schadensgradskala „zunächst für die allgemeine Bebauung vornehmlich in Mauerwerksbauweise" gilt
   (Maiwald & Schwarz 2018); für Holz-, Fachwerk- und Leichtbaukonstruktionen ist das Band deshalb
   eine Untergrenze und wird nicht stillschweigend verallgemeinert (Modellgrenze der Abschätzung).
   **Bauform-Grenze der Abschätzung des Maßnahmen-Hebels S092 (Vorgabe P2):** Vorgabe P2 gilt
   Maßnahmen ohne publizierte Effektgröße, und das ist in diesem Bericht allein der Hebel S092
   (Register 60-S092-01, Band 0,0075–0,0832). Er wirkt als **kommunenweiter Pauschalfaktor** statt
   als zellscharfe Wirkung: Ein Objektschutz-Anteil gilt für die ganze Kommune, nicht für die
   einzelne Zelle. Die Näherung von \(s_{\text{bem}}\) **überschätzt den Hebel** (Fehlerrichtung
   und Begründung §5.1.3); der Hebel ist deshalb als Abschätzung gekennzeichnet und keine
   Zellprognose. Herleitung und Band: §5.1.2 und §5.1.3.
3. Nichtwohngebäude (Gewerbe, öffentliche Gebäude) sind im Mengengerüst nicht enthalten (60-R24-01)
   — die Mengenbasis ist insoweit eine weitere Untergrenze.
4. Der bundeseinheitliche NHK-Wertsatz streut ohne Regionalfaktor der Gutachterausschüsse
   schätzungsweise ±20 % zwischen Hoch- und Niedrigpreisregionen (60-R24-01).
5. Der DGM1-Höhenfehler (σ_z = 0,15–0,20 m) schlägt auf die Wassertiefe durch; die zugehörige
   Sensitivitätskette 60-S074-01 stammt aus einer Fallstudie im flachen Relief, in Mittelgebirgs-
   und Steillagen erzeugt derselbe Höhenfehler größere Tiefenfehler — dort ist das Band ebenfalls
   eine Untergrenze.
6. Die ZÜRS-Zonierung (60-R17-01) und die amtlichen Risikogebiete nach § 73 WHG sind nicht
   deckungsgleich; der Widerspruch dient nur als bundesweites Abgleichband (§3.4), nicht als eigenes
   Multiplikativglied der Zellrechnung.
7. Die Zustandsfunktion FLEMOps (60-S093-01) ist an einem Extremereignis kalibriert und validiert;
   für HQhäufig ist ihre Anwendbarkeit von der Quelle selbst infrage gestellt — auch hier ist das
   Band eine Untergrenze (§3.8).
8. Die Bestandsdynamik S104 wird konstant gehalten (s. o.): Zu- oder Abnahme der exponierten
   Bausubstanz zwischen Bezugsjahr und Szenariojahr wird im heutigen Modellstand nicht abgebildet.
9. **Bewertung zum Neuwert — Untergrenzen-Aussage geprüft.** Der Betrag rechnet mit Neuwerten; der
   Zeitwertansatz der Arbeitsmappe (Mon. J64) läge um 45 % niedriger (0,62 statt 1,13 Mrd. €₂₀₂₆/a,
   Band 0,45–0,85; §7.2; der Neuwert-Betrag ist die kalibrierte Bundessumme \(\lambda M_0\) aus §4.6). Ergebnis der Prüfung: Der Betrag ist eine **Untergrenze nur im
   Konto- und Mengenumfang** (Modellgrenzen 1 und 3: K1, K4, K5, K8 und Nichtwohngebäude fehlen).
   Auf der Bewertungsachse ist er **keine Untergrenze**, sondern gegenüber dem Zeitwertansatz die
   obere Lesart. Eine Untergrenze des K3-Betrags nach Mappenvorgabe ist er damit nicht; der
   Versionsstempel unten nennt deshalb beide Richtungen.

**Infokasten-Texte (§3.6 — Teil des Berichts):**

> **Benennung nach Geltungsbereich:** „bewerteter Schaden — Konto K3" (nie „Gesamtschaden").
>
> **Vollständigkeitsanzeige:** „Stufe M0: 1 von 8 Konten aktiv" mit Roadmap-Aufklappliste.
>
> **Versionsstempel:** „berechnet mit Modellstand M0 — Untergrenze im Kontoumfang (nur K3, nur
> Wohngebäude); bewertet zum Neuwert, zum Zeitwert rund 45 % niedriger".

## 7 Parameter-Blöcke (maschinenlesbar, §4)

Kap. 7 führt je rechnendem Parameter aus §3.5 und §4.8 einen Block: die Kostensätze mit Pflichtfeld `preisstand: 2026` und Umrechnungsfaktor, die Parameter der Kernformel und der Kalibrierung sowie die vier Blöcke des Hebels S092.

**Zuordnung der Zeilen aus §4.8 (Befunde 83, 99).** Jede Zeile der Tabelle §4.8 hat einen eigenen
Block, mit zwei Ausnahmen, die auf einen vorhandenen Block zeigen statt ihn zu doppeln: die Zeile
„Unsicherheitsband \(\lambda\)" ist das Feld `band` des Blocks `flood_bldg.lambda`, die Zeile
„Gedeckelte Schadensquote (nur \(O_M\))" ist der Block `flood_bldg.d_5`. Die Blöcke der Kalibrier-
und Prüfgrößen (Anker \(A_{\text{ver}}\), Baupreisanstieg, Klassenraten der Bestandsschranke,
Typ-Mix, \(M_0\) und seine Eingänge, Plausibilitätsschranke, beide Prüftoleranzen, Sanity-Grenzen
\(U\), \(O_u\), \(O_M\) mit ihren Eingängen, \(f_{\text{AWM}}\), \(q_0\)) stehen hinter den Blöcken der
Kernformel. Jeder dieser Blöcke sagt im Feld `rolle:`, wie er rechnet: `kalibrierung` — geht
über \(\lambda\) in den Betrag ein; `pruefgroesse` — entscheidet eine Prüfung (Plausibilitätsschranke,
Verteilungsprüfung, Sanity-Band), geht aber nicht in den Betrag ein; `sensitivitaet` — läuft nur
als Sensitivität; `waechter` — bindet den Doppelzählungs-Wächter (§4.7). Blöcke ohne `rolle:`
gehen unmittelbar in die Kernformel oder den Hebel ein. Der Anker \(A_{\text{ver}}\) ist kein Kostensatz, sondern die Kalibriergröße im
Bestands- und Preisstand 2024 der GDV-Reihe (§4.1); er trägt deshalb `preisstand: null` und das
Feld `preisstand_hinweis`, auf den Preisstand 2026 hebt ihn \(\pi\) (Block `flood_bldg.pi`).

**Datenebene und Ebenen-Status (Befund 86).** Jeder Block trägt `datenebene:` — die Ebene aus §3.2,
auf der der Parameter im Produkt wirkt (`HQ_FLAECHE`, `HQ_TIEFE`, `GEBAEUDEWERT`,
`GEBAEUDEZUSTAND_BAUSTOFF`), oder `null`, wenn er an keiner Zellebene hängt (Kalibrier- und
Prüfgrößen, Hebel). Wo eine Ebene genannt ist, steht `ebene_status:` mit genau einem der Werte
`vorhanden`, `neu_anzulegen` oder `geparkt` nach §3.2. Bei `geparkt` setzt der Block zusätzlich
`platzhalter: true` und `platzhalter_text:`: Der Wert 1,00 der Faktoren \(f_{S093}\), \(f_{S094}\) ist
keine abgeschätzte Wirkung, sondern der Neutralwert einer fehlenden Datenebene; im Produkt steht
neben ihm deshalb „neutral gesetzt, Datenebene fehlt (§3.2)", nicht „Abschätzung von KAP3".
\(q_0\) hängt an keiner Zellebene aus §3.2, seine Datenquelle ist aber ebenfalls geparkt (§4.7);
sein Block führt `ebene_status: geparkt` ohne das Feld `platzhalter`, weil 0,15 eine Abschätzung und kein
Neutralwert ist.

**Band der Szenario-Wahrscheinlichkeit HQhäufig (Befund 84).** Der Block `flood_bldg.p_hq_haeufig`
führt das Band der Registerzeile 60-W085-01 mit: Die Länder kartieren „häufig" zwischen HQ20 und
HQ5, also 0,05 bis 0,2 a⁻¹ um den Kartenfall HQ10. Wirkung auf den K3-Betrag, einmal beziffert:
Die Trapezsumme je Zelle vor dem Niveau-Skalar (§3.4, Stützstellen 15,0 / 77,76 / 300,0 m² je Ereignis bei
p = 0,1 / 0,01 / 0,002236 a⁻¹) sinkt am unteren Bandende auf das 0,63-Fache und steigt am oberen auf das 1,73-Fache; der
Anteil des häufigen Szenarios liegt dabei bei 46 % bzw. 80 % statt 66 %. Die kalibrierte
Bundessumme bleibt davon unberührt, weil \(\lambda\) sie auf \(A^{*}\) setzt; das Band verschiebt die
Verteilung zwischen Kommunen mit viel und wenig häufig überfluteter Fläche. `flood_bldg.p_hq100`
bleibt ohne Band, weil HQ100 definitorisch ist (§ 74 WHG); das steht als `band_grund` im Block,
damit `band: null` nicht wie eine Auslassung aussieht.

**Kennzeichnung nach Vorgabe P1 — im Block, nicht im Kommentar.** Jeder Block dieses Kapitels trägt
drei zusätzliche, maschinenlesbare Felder. Eine Kennzeichnung als YAML-Kommentar hinter `herkunft`
erfüllt P1 ausdrücklich nicht („eine Herleitung nur als Code-Kommentar erfüllt die Vorgabe nicht"),
deshalb sind die früheren Kommentare durch echte Felder ersetzt:

- **`kennzeichnung:`** — genau einer von zwei Werten: `quelle` (der Wert stammt aus einer belegten
  Quelle; das Feld `quelle:` nennt sie) oder `abschaetzung_kap3` (begründete Abschätzung von KAP3
  nach §3.9, Vorgaben P1/P2). Die vier Blöcke des Hebels S092 stehen auf `abschaetzung_kap3`;
  `flood_bldg.r_s092` ist aus den drei übrigen berechnet, und weil alle drei Faktoren Abschätzungen
  sind, ist das Produkt als Ganzes ebenfalls eine Abschätzung (Feld `abgeleitet_aus:` nennt die
  Faktoren).
- **`herleitung_anker:`** — bei jedem als `abschaetzung_kap3` gekennzeichneten Block der benannte
  Anker des Abschnitts, der die Herleitung im **sichtbaren Berichtstext** ausschreibt:
  `#s092-wirkung` → §5.1 mit §5.1.2 (Kette, Herleitung je Faktor, Sensitivität, Modellgrenzen),
  `#s-bem-naeherung` → §5.1.3 (Näherungscharakter und Richtung von \(s_{\text{bem}}\)).
- **`wertebereich_abweichung:`** — Anker des Abschnitts, der die Abweichung der Felder `endpunkt`
  und `bandzuordnung` vom Wertebereich des §4-Templates ausweist und die Fortschreibung beantragt:
  `#fortschreibung-endpunkt-k3` → §7.1. Die Abweichung ist damit weder im Text noch maschinell
  still.

```yaml
parameter:
  id: flood_bldg.dq_s092
  wert: 0.10
  einheit: "-"
  band: [0.05, 0.20]
  herkunft: herleitung:#s092-wirkung
  kennzeichnung: abschaetzung_kap3
  herleitung_anker: "#s092-wirkung"
  quelle: null
  preisstand: null
  datenebene: null
  bandzuordnung: [alle]
  endpunkt: K3-Wiederherstellung
  wertebereich_abweichung: "#fortschreibung-endpunkt-k3"
---
parameter:
  id: flood_bldg.s_bem
  wert: 0.50
  einheit: "-"
  band: [0.30, 0.52]
  herkunft: herleitung:#s-bem-naeherung
  kennzeichnung: abschaetzung_kap3
  herleitung_anker: "#s-bem-naeherung"
  naeherung: true
  naeherung_richtung: ueberschaetzt_hebel
  quelle: null
  preisstand: null
  datenebene: null
  bandzuordnung: [alle]
  endpunkt: K3-Wiederherstellung
  wertebereich_abweichung: "#fortschreibung-endpunkt-k3"
---
parameter:
  id: flood_bldg.e_bem
  wert: 0.70
  einheit: "-"
  band: [0.50, 0.80]
  herkunft: herleitung:#s092-wirkung
  kennzeichnung: abschaetzung_kap3
  herleitung_anker: "#s092-wirkung"
  quelle: null
  preisstand: null
  datenebene: null
  bandzuordnung: [alle]
  endpunkt: K3-Wiederherstellung
  wertebereich_abweichung: "#fortschreibung-endpunkt-k3"
---
parameter:
  id: flood_bldg.r_s092
  wert: 0.035
  einheit: "-"
  band: [0.0075, 0.0832]
  herkunft: herleitung:#s092-wirkung
  kennzeichnung: abschaetzung_kap3
  abgeleitet_aus: [flood_bldg.dq_s092, flood_bldg.s_bem, flood_bldg.e_bem]
  herleitung_anker: "#s092-wirkung"
  quelle: null
  preisstand: null
  datenebene: null
  bandzuordnung: [alle]
  endpunkt: K3-Wiederherstellung
  wertebereich_abweichung: "#fortschreibung-endpunkt-k3"
---
parameter:
  id: flood_bldg.n_efh_zfh
  wert: 1950
  einheit: "EUR2026/m2 BGF"
  band: [1890, 2043]
  herkunft: register:60-R24-01
  kennzeichnung: abschaetzung_kap3
  herleitung_anker: "#kernformel-zelle"
  quelle: "NHK 2010, ImmoWertV Anlage 4; Fortschreibung mit Baupreisindex (Langbeleg B4)"
  preisstand: 2026
  umrechnungsfaktor: 1.8578
  datenebene: GEBAEUDEWERT
  ebene_status: neu_anzulegen
  bandzuordnung: [alle]
  endpunkt: K3-Wiederherstellung
  wertebereich_abweichung: "#fortschreibung-endpunkt-k3"
---
parameter:
  id: flood_bldg.n_mfh
  wert: 1533
  einheit: "EUR2026/m2 BGF"
  band: [1485, 1606]
  herkunft: register:60-R24-01
  kennzeichnung: abschaetzung_kap3
  herleitung_anker: "#kernformel-zelle"
  quelle: "NHK 2010, ImmoWertV Anlage 4; Fortschreibung mit Baupreisindex (Langbeleg B4)"
  preisstand: 2026
  umrechnungsfaktor: 1.8578
  datenebene: GEBAEUDEWERT
  ebene_status: neu_anzulegen
  bandzuordnung: [alle]
  endpunkt: K3-Wiederherstellung
  wertebereich_abweichung: "#fortschreibung-endpunkt-k3"
---
parameter:
  id: flood_bldg.k_bgf
  wert: 1.3
  einheit: "m2/m2"
  band: [1.25, 1.40]
  herkunft: register:60-R24-01
  kennzeichnung: abschaetzung_kap3
  herleitung_anker: "#kernformel-zelle"
  quelle: null
  preisstand: null
  datenebene: GEBAEUDEWERT
  ebene_status: neu_anzulegen
  bandzuordnung: [alle]
  endpunkt: K3-Wiederherstellung
  wertebereich_abweichung: "#fortschreibung-endpunkt-k3"
---
parameter:
  id: flood_bldg.p_hq_haeufig
  wert: 0.1
  einheit: "1/a"
  band: [0.05, 0.2]
  herkunft: register:60-W085-01
  kennzeichnung: quelle
  herleitung_anker: null
  quelle: "Langbeleg B1; Spanne HQ20 bis HQ5 nach Register 60-W085-01"
  preisstand: null
  datenebene: HQ_FLAECHE
  ebene_status: neu_anzulegen
  bandzuordnung: [alle]
  endpunkt: K3-Wiederherstellung
  wertebereich_abweichung: "#fortschreibung-endpunkt-k3"
---
parameter:
  id: flood_bldg.p_hq100
  wert: 0.01
  einheit: "1/a"
  band: null
  band_grund: "definitorisch (HQ100, § 74 WHG)"
  herkunft: register:60-W085-01
  kennzeichnung: quelle
  herleitung_anker: null
  quelle: "Langbeleg B1"
  preisstand: null
  datenebene: HQ_FLAECHE
  ebene_status: neu_anzulegen
  bandzuordnung: [alle]
  endpunkt: K3-Wiederherstellung
  wertebereich_abweichung: "#fortschreibung-endpunkt-k3"
---
parameter:
  id: flood_bldg.p_hq_extrem
  wert: 0.002236
  einheit: "1/a"
  band: [0.001, 0.005]
  herkunft: register:60-W085-01
  kennzeichnung: abschaetzung_kap3
  herleitung_anker: "#kernformel-zelle"
  quelle: null
  preisstand: null
  datenebene: HQ_FLAECHE
  ebene_status: neu_anzulegen
  bandzuordnung: [alle]
  endpunkt: K3-Wiederherstellung
  wertebereich_abweichung: "#fortschreibung-endpunkt-k3"
---
parameter:
  id: flood_bldg.d_1
  wert: 0.035
  einheit: "-"
  band: null
  herkunft: register:60-S093-01
  kennzeichnung: quelle
  herleitung_anker: null
  quelle: "Thieken u. a. 2008, FLEMOps (Langbeleg B5)"
  preisstand: null
  datenebene: HQ_TIEFE
  ebene_status: neu_anzulegen
  bandzuordnung: [alle]
  endpunkt: K3-Wiederherstellung
  wertebereich_abweichung: "#fortschreibung-endpunkt-k3"
---
parameter:
  id: flood_bldg.d_5
  wert: 0.25
  einheit: "-"
  band: null
  herkunft: register:60-S093-01
  kennzeichnung: quelle
  herleitung_anker: null
  quelle: "Thieken u. a. 2008, FLEMOps (Langbeleg B5)"
  preisstand: null
  datenebene: HQ_TIEFE
  ebene_status: neu_anzulegen
  bandzuordnung: [alle]
  endpunkt: K3-Wiederherstellung
  wertebereich_abweichung: "#fortschreibung-endpunkt-k3"
---
parameter:
  id: flood_bldg.h_1
  wert: 0.1
  einheit: "m"
  band: null
  herkunft: herleitung:§3.3
  kennzeichnung: abschaetzung_kap3
  herleitung_anker: "#tiefen-schadensfunktion"
  quelle: null
  preisstand: null
  datenebene: HQ_TIEFE
  ebene_status: neu_anzulegen
  bandzuordnung: [alle]
  endpunkt: K3-Wiederherstellung
  wertebereich_abweichung: "#fortschreibung-endpunkt-k3"
---
parameter:
  id: flood_bldg.h_5
  wert: 1.75
  einheit: "m"
  band: null
  herkunft: herleitung:§3.3
  kennzeichnung: abschaetzung_kap3
  herleitung_anker: "#tiefen-schadensfunktion"
  quelle: null
  preisstand: null
  datenebene: HQ_TIEFE
  ebene_status: neu_anzulegen
  bandzuordnung: [alle]
  endpunkt: K3-Wiederherstellung
  wertebereich_abweichung: "#fortschreibung-endpunkt-k3"
---
parameter:
  id: flood_bldg.f_s093
  wert: 1.0
  einheit: "-"
  band: [0.71, 1.40]
  herkunft: register:60-S093-01
  kennzeichnung: abschaetzung_kap3
  herleitung_anker: "#tiefen-schadensfunktion"
  quelle: null
  preisstand: null
  datenebene: GEBAEUDEZUSTAND_BAUSTOFF
  ebene_status: geparkt
  platzhalter: true
  platzhalter_text: "neutral gesetzt, Datenebene fehlt (§3.2)"
  bandzuordnung: [alle]
  endpunkt: K3-Wiederherstellung
  wertebereich_abweichung: "#fortschreibung-endpunkt-k3"
---
parameter:
  id: flood_bldg.f_s094
  wert: 1.0
  einheit: "-"
  band: [0.84, 1.18]
  herkunft: register:60-S094-01
  kennzeichnung: abschaetzung_kap3
  herleitung_anker: "#tiefen-schadensfunktion"
  quelle: null
  preisstand: null
  datenebene: GEBAEUDEZUSTAND_BAUSTOFF
  ebene_status: geparkt
  platzhalter: true
  platzhalter_text: "neutral gesetzt, Datenebene fehlt (§3.2)"
  bandzuordnung: [alle]
  endpunkt: K3-Wiederherstellung
  wertebereich_abweichung: "#fortschreibung-endpunkt-k3"
---
parameter:
  id: flood_bldg.w_wg
  wert: 0.65
  einheit: "-"
  band: [0.55, 0.75]
  herkunft: herleitung:§4.2
  kennzeichnung: abschaetzung_kap3
  herleitung_anker: "#kalibrierung-zielwert"
  quelle: null
  preisstand: null
  datenebene: null
  bandzuordnung: [alle]
  endpunkt: K3-Wiederherstellung
  wertebereich_abweichung: "#fortschreibung-endpunkt-k3"
---
parameter:
  id: flood_bldg.u
  wert: 1.54
  einheit: "-"
  band: [1.33, 1.75]
  herkunft: herleitung:§4.2
  kennzeichnung: abschaetzung_kap3
  herleitung_anker: "#kalibrierung-zielwert"
  quelle: null
  preisstand: null
  datenebene: null
  bandzuordnung: [alle]
  endpunkt: K3-Wiederherstellung
  wertebereich_abweichung: "#fortschreibung-endpunkt-k3"
---
parameter:
  id: flood_bldg.phi_fluss
  wert: 0.5
  einheit: "-"
  band: [0.35, 0.65]
  herkunft: herleitung:§4.2
  kennzeichnung: abschaetzung_kap3
  herleitung_anker: "#kalibrierung-zielwert"
  quelle: null
  preisstand: null
  datenebene: null
  bandzuordnung: [alle]
  endpunkt: K3-Wiederherstellung
  wertebereich_abweichung: "#fortschreibung-endpunkt-k3"
---
parameter:
  id: flood_bldg.kappa
  wert: 1.15
  einheit: "-"
  band: [1.05, 1.30]
  herkunft: herleitung:§4.2
  kennzeichnung: abschaetzung_kap3
  herleitung_anker: "#kalibrierung-zielwert"
  quelle: null
  preisstand: null
  datenebene: null
  bandzuordnung: [alle]
  endpunkt: K3-Wiederherstellung
  wertebereich_abweichung: "#fortschreibung-endpunkt-k3"
---
parameter:
  id: flood_bldg.pi
  wert: 1.07
  einheit: "-"
  band: [1.039, 1.124]
  herkunft: herleitung:§4.2
  kennzeichnung: abschaetzung_kap3
  herleitung_anker: "#kalibrierung-zielwert"
  quelle: null
  preisstand: null
  datenebene: null
  bandzuordnung: [alle]
  endpunkt: K3-Wiederherstellung
  wertebereich_abweichung: "#fortschreibung-endpunkt-k3"
---
parameter:
  id: flood_bldg.lambda
  wert: 0.911
  einheit: "-"
  band: [0.12, 3.93]
  herkunft: herleitung:§4.4
  kennzeichnung: abschaetzung_kap3
  herleitung_anker: "#niveau-skalar"
  quelle: null
  preisstand: null
  vorlaeufig: true
  vorlaeufig_grund: "Vorlaeufig, weil die unabhaengige Verteilungspruefung (§4.5) nicht bestanden ist: Abstand 13,9 Prozentpunkte gegen die vorab fixierte Toleranz von 11,5 Prozentpunkten (Modellentscheid §4.5). Massgeblich ist der Text in §4.4 (#niveau-skalar); Stand 23.09.2026."
  datenebene: null
  bandzuordnung: [alle]
  endpunkt: K3-Wiederherstellung
  wertebereich_abweichung: "#fortschreibung-endpunkt-k3"
---
parameter:
  id: flood_bldg.a_ver
  wert: 1.838
  einheit: "Mrd. €2024/a"
  band: [1.061, 1.838]
  herkunft: herleitung:§4.1
  kennzeichnung: quelle
  herleitung_anker: "#anker-gdv"
  preisstand_hinweis: "Bestands- und Preisstand 2024 der GDV-Reihe (§4.1); auf 2026 ueber flood_bldg.pi"
  rolle: kalibrierung
  quelle: "GDV-Naturgefahrenstatistik 2024, Datenservice Naturgefahrenreport 2025; docs/evidenz/60_gdv_jahresreihe_2002_2024.csv"
  preisstand: null
  datenebene: null
  bandzuordnung: [alle]
  endpunkt: K3-Wiederherstellung
  wertebereich_abweichung: "#fortschreibung-endpunkt-k3"
---
parameter:
  id: flood_bldg.baupreisanstieg_2023_2024
  wert: 0.03
  einheit: "1/a"
  band: [0.023, 0.050]
  herkunft: herleitung:§4.2
  kennzeichnung: abschaetzung_kap3
  herleitung_anker: "#kalibrierung-zielwert"
  sensitivitaet: "pi = 1,080 bei 2,3 %, 1,052 bei 5,0 %"
  rolle: kalibrierung
  quelle: null
  preisstand: null
  datenebene: null
  bandzuordnung: [alle]
  endpunkt: K3-Wiederherstellung
  wertebereich_abweichung: "#fortschreibung-endpunkt-k3"
---
parameter:
  id: flood_bldg.rate_bestand_gk3_gk4
  wert: 0.1
  einheit: "1/a"
  band: null
  herkunft: register:60-R17-01
  kennzeichnung: abschaetzung_kap3
  herleitung_anker: "#sanity-band"
  band_grund: "Jaehrlichkeit der ZUeRS-Adressklasse, unveraendert uebernommen (§4.6)"
  rolle: pruefgroesse
  quelle: null
  preisstand: null
  datenebene: null
  bandzuordnung: [alle]
  endpunkt: K3-Wiederherstellung
  wertebereich_abweichung: "#fortschreibung-endpunkt-k3"
---
parameter:
  id: flood_bldg.rate_bestand_gk2
  wert: 0.01
  einheit: "1/a"
  band: null
  herkunft: register:60-R17-01
  kennzeichnung: abschaetzung_kap3
  herleitung_anker: "#sanity-band"
  band_grund: "Jaehrlichkeit der ZUeRS-Adressklasse, unveraendert uebernommen (§4.6)"
  rolle: pruefgroesse
  quelle: null
  preisstand: null
  datenebene: null
  bandzuordnung: [alle]
  endpunkt: K3-Wiederherstellung
  wertebereich_abweichung: "#fortschreibung-endpunkt-k3"
---
parameter:
  id: flood_bldg.theta_efh_zfh
  wert: 0.596
  einheit: "-"
  band: [0.471, 0.624]
  herkunft: herleitung:§4.3
  kennzeichnung: quelle
  herleitung_anker: "#modellsumme-m0"
  band_kennzeichnung: abschaetzung_kap3
  rolle: kalibrierung
  quelle: "Destatis, Bestand und Bauabgang von Wohnungen und Wohngebaeuden 2021, Tabelle 2.1.3; docs/evidenz/60_destatis_wohnflaeche_gebaeudetyp_2021.csv"
  preisstand: null
  datenebene: null
  bandzuordnung: [alle]
  endpunkt: K3-Wiederherstellung
  wertebereich_abweichung: "#fortschreibung-endpunkt-k3"
---
parameter:
  id: flood_bldg.m0
  wert: 1.243
  einheit: "Mrd. EUR2026/a"
  band: [0.583, 2.425]
  herkunft: herleitung:§4.3
  kennzeichnung: abschaetzung_kap3
  herleitung_anker: "#modellsumme-m0"
  abgeleitet_aus: [flood_bldg.w_wohn, flood_bldg.wert_je_wohngebaeude, flood_bldg.adressen_gk3_gk4, flood_bldg.adressen_gk2, flood_bldg.r_gk3_gk4, flood_bldg.r_gk2]
  rolle: kalibrierung
  quelle: null
  preisstand: 2026
  datenebene: null
  bandzuordnung: [alle]
  endpunkt: K3-Wiederherstellung
  wertebereich_abweichung: "#fortschreibung-endpunkt-k3"
---
parameter:
  id: flood_bldg.wohnflaeche_je_wohngebaeude
  wert: 208
  einheit: "m2"
  band: null
  herkunft: register:60-R24-01
  kennzeichnung: quelle
  herleitung_anker: null
  band_grund: "Quotient zweier amtlicher Summen (§4.3 Bandtabelle)"
  rolle: kalibrierung
  quelle: "amtliche Bestandsstatistik 31.12.2024 (4,1 Mrd. m2 / 19,7 Mio. Wohngebaeude)"
  preisstand: null
  datenebene: null
  bandzuordnung: [alle]
  endpunkt: K3-Wiederherstellung
  wertebereich_abweichung: "#fortschreibung-endpunkt-k3"
---
parameter:
  id: flood_bldg.wert_je_wohngebaeude
  wert: 481726.25
  einheit: "EUR2026"
  band: [435696.30, 547073.95]
  herkunft: herleitung:§4.3
  kennzeichnung: abschaetzung_kap3
  herleitung_anker: "#modellsumme-m0"
  abgeleitet_aus: [flood_bldg.wohnflaeche_je_wohngebaeude, flood_bldg.k_bgf, flood_bldg.theta_efh_zfh, flood_bldg.n_efh_zfh, flood_bldg.n_mfh]
  rolle: kalibrierung
  quelle: null
  preisstand: 2026
  datenebene: null
  bandzuordnung: [alle]
  endpunkt: K3-Wiederherstellung
  wertebereich_abweichung: "#fortschreibung-endpunkt-k3"
---
parameter:
  id: flood_bldg.w_wohn
  wert: 0.872
  einheit: "-"
  band: null
  herkunft: register:60-R17-01
  kennzeichnung: quelle
  herleitung_anker: null
  band_grund: "Quotient zweier amtlicher Summen ohne publizierte Unsicherheit (§4.3)"
  rolle: kalibrierung
  quelle: "Register 60-R17-01/60-R24-01 (19,7 Mio. Wohngebaeude / 22,6 Mio. bewertete Adressen)"
  preisstand: null
  datenebene: null
  bandzuordnung: [alle]
  endpunkt: K3-Wiederherstellung
  wertebereich_abweichung: "#fortschreibung-endpunkt-k3"
---
parameter:
  id: flood_bldg.adressen_gk3_gk4
  wert: 339000
  einheit: "Adressen"
  band: null
  herkunft: register:60-R17-01
  kennzeichnung: quelle
  herleitung_anker: null
  rolle: kalibrierung
  quelle: "ZUeRS Geo 2025: GK3 1,1 % + GK4 0,4 % von 22,6 Mio. Adressen"
  preisstand: null
  datenebene: null
  bandzuordnung: [alle]
  endpunkt: K3-Wiederherstellung
  wertebereich_abweichung: "#fortschreibung-endpunkt-k3"
---
parameter:
  id: flood_bldg.adressen_gk2
  wert: 1380000
  einheit: "Adressen"
  band: null
  herkunft: register:60-R17-01
  kennzeichnung: quelle
  herleitung_anker: null
  rolle: kalibrierung
  quelle: "ZUeRS Geo 2025: GK2 6,1 % von 22,6 Mio. Adressen"
  preisstand: null
  datenebene: null
  bandzuordnung: [alle]
  endpunkt: K3-Wiederherstellung
  wertebereich_abweichung: "#fortschreibung-endpunkt-k3"
---
parameter:
  id: flood_bldg.r_gk3_gk4
  wert: 0.0059796
  einheit: "1/a"
  band: [0.0033, 0.0103]
  herkunft: herleitung:§4.3
  kennzeichnung: quelle
  herleitung_anker: "#modellsumme-m0"
  band_kennzeichnung: abschaetzung_kap3
  rolle: kalibrierung
  quelle: "docs/evidenz/60_stichprobe/m0_klassenraten.csv, Zeile gk3_gk4;alle, Spalte rate_exponiert_hqextrem_1_pro_a"
  preisstand: null
  datenebene: null
  bandzuordnung: [alle]
  endpunkt: K3-Wiederherstellung
  wertebereich_abweichung: "#fortschreibung-endpunkt-k3"
---
parameter:
  id: flood_bldg.r_gk2
  wert: 0.00067515
  einheit: "1/a"
  band: [0.000301, 0.001154]
  herkunft: herleitung:§4.3
  kennzeichnung: quelle
  herleitung_anker: "#modellsumme-m0"
  band_kennzeichnung: abschaetzung_kap3
  rolle: kalibrierung
  quelle: "docs/evidenz/60_stichprobe/m0_klassenraten.csv, Zeile gk2;alle, Spalte rate_exponiert_hqextrem_1_pro_a"
  preisstand: null
  datenebene: null
  bandzuordnung: [alle]
  endpunkt: K3-Wiederherstellung
  wertebereich_abweichung: "#fortschreibung-endpunkt-k3"
---
parameter:
  id: flood_bldg.lambda_schranke_min
  wert: 0.5
  einheit: "-"
  band: null
  herkunft: herleitung:§4.4
  kennzeichnung: abschaetzung_kap3
  herleitung_anker: "#niveau-skalar"
  sensitivitaet: "Faktor 1,5 bzw. 3 um 1 (§4.4)"
  rolle: pruefgroesse
  quelle: null
  preisstand: null
  datenebene: null
  bandzuordnung: [alle]
  endpunkt: K3-Wiederherstellung
  wertebereich_abweichung: "#fortschreibung-endpunkt-k3"
---
parameter:
  id: flood_bldg.lambda_schranke_max
  wert: 2.0
  einheit: "-"
  band: null
  herkunft: herleitung:§4.4
  kennzeichnung: abschaetzung_kap3
  herleitung_anker: "#niveau-skalar"
  sensitivitaet: "Faktor 1,5 bzw. 3 um 1 (§4.4)"
  rolle: pruefgroesse
  quelle: null
  preisstand: null
  datenebene: null
  bandzuordnung: [alle]
  endpunkt: K3-Wiederherstellung
  wertebereich_abweichung: "#fortschreibung-endpunkt-k3"
---
parameter:
  id: flood_bldg.toleranz_verteilungspruefung
  wert: 11.5
  einheit: "Prozentpunkte"
  band: null
  herkunft: herleitung:§4.5
  kennzeichnung: abschaetzung_kap3
  herleitung_anker: "#verteilungspruefung"
  band_grund: "Toleranz selbst; berechnet aus Jackknife 11,2, Ablese 1,7, Modellband 2,3 (quadratisch); abgeschaetzt ist die Kombinationsregel"
  rolle: pruefgroesse
  quelle: null
  preisstand: null
  datenebene: null
  bandzuordnung: [alle]
  endpunkt: K3-Wiederherstellung
  wertebereich_abweichung: "#fortschreibung-endpunkt-k3"
---
parameter:
  id: flood_bldg.niveau_quantilvergleich
  wert: 0.90
  einheit: "-"
  band: null
  herkunft: herleitung:§4.5
  kennzeichnung: abschaetzung_kap3
  herleitung_anker: "#verteilungspruefung"
  sensitivitaet: "Niveau 0,80: Ergebnis unveraendert (§4.5)"
  rolle: pruefgroesse
  quelle: null
  preisstand: null
  datenebene: null
  bandzuordnung: [alle]
  endpunkt: K3-Wiederherstellung
  wertebereich_abweichung: "#fortschreibung-endpunkt-k3"
---
parameter:
  id: flood_bldg.sanity_u
  wert: 0.189
  einheit: "Mrd. EUR2026/a"
  band: [0.095, 0.315]
  herkunft: herleitung:§4.6
  kennzeichnung: abschaetzung_kap3
  herleitung_anker: "#sanity-band"
  abgeleitet_aus: [flood_bldg.e_fonds, flood_bldg.w_aufbauhilfe, flood_bldg.f_fluss, flood_bldg.n_ankerfenster]
  rolle: pruefgroesse
  quelle: null
  preisstand: 2026
  datenebene: null
  bandzuordnung: [alle]
  endpunkt: K3-Wiederherstellung
  wertebereich_abweichung: "#fortschreibung-endpunkt-k3"
---
parameter:
  id: flood_bldg.e_fonds
  wert: 43.47
  einheit: "Mrd. EUR2026"
  band: null
  herkunft: herleitung:§4.6
  kennzeichnung: quelle
  herleitung_anker: "#sanity-band"
  abgeleitet_aus: [flood_bldg.fondsrate]
  band_grund: "Fondsvolumina gesetzlich fixiert; Fortschreibung als eigener Block"
  rolle: pruefgroesse
  quelle: "AufbhG 2013 § 4 Abs. 1 Satz 1; Aufbauhilfegesetz 2021; docs/evidenz/60_wiederaufbauhilfen_2013_2021.csv"
  preisstand: 2026
  datenebene: null
  bandzuordnung: [alle]
  endpunkt: K3-Wiederherstellung
  wertebereich_abweichung: "#fortschreibung-endpunkt-k3"
---
parameter:
  id: flood_bldg.fondsrate
  wert: 0.02
  einheit: "1/a"
  band: null
  herkunft: herleitung:§4.6
  kennzeichnung: abschaetzung_kap3
  herleitung_anker: "#sanity-band"
  sensitivitaet: "0 %/a: U 0,165, O_u 10,0; 3 %/a: U 0,202, O_u 11,59 Mrd. EUR2026/a"
  rolle: pruefgroesse
  quelle: null
  preisstand: null
  datenebene: null
  bandzuordnung: [alle]
  endpunkt: K3-Wiederherstellung
  wertebereich_abweichung: "#fortschreibung-endpunkt-k3"
---
parameter:
  id: flood_bldg.w_aufbauhilfe
  wert: 0.11
  einheit: "-"
  band: [0.06, 0.17]
  herkunft: herleitung:§4.6
  kennzeichnung: abschaetzung_kap3
  herleitung_anker: "#sanity-band"
  rolle: pruefgroesse
  quelle: null
  preisstand: null
  datenebene: null
  bandzuordnung: [alle]
  endpunkt: K3-Wiederherstellung
  wertebereich_abweichung: "#fortschreibung-endpunkt-k3"
---
parameter:
  id: flood_bldg.f_fluss
  wert: 0.90
  einheit: "-"
  band: [0.80, 1.00]
  herkunft: herleitung:§4.6
  kennzeichnung: abschaetzung_kap3
  herleitung_anker: "#sanity-band"
  rolle: pruefgroesse
  quelle: null
  preisstand: null
  datenebene: null
  bandzuordnung: [alle]
  endpunkt: K3-Wiederherstellung
  wertebereich_abweichung: "#fortschreibung-endpunkt-k3"
---
parameter:
  id: flood_bldg.n_ankerfenster
  wert: 23
  einheit: "a"
  band: null
  herkunft: herleitung:§4.6
  kennzeichnung: quelle
  herleitung_anker: "#sanity-band"
  rolle: pruefgroesse
  quelle: "gezaehlt: Kalibrierjahre 2002-2024 (§4.1/§4.7)"
  preisstand: null
  datenebene: null
  bandzuordnung: [alle]
  endpunkt: K3-Wiederherstellung
  wertebereich_abweichung: "#fortschreibung-endpunkt-k3"
---
parameter:
  id: flood_bldg.sanity_o_u
  wert: 11.04
  einheit: "Mrd. EUR2026/a"
  band: null
  herkunft: herleitung:§4.6
  kennzeichnung: abschaetzung_kap3
  herleitung_anker: "#sanity-band"
  abgeleitet_aus: [flood_bldg.e_fonds, flood_bldg.f_fluss]
  rolle: pruefgroesse
  quelle: null
  preisstand: 2026
  datenebene: null
  bandzuordnung: [alle]
  endpunkt: K3-Wiederherstellung
  wertebereich_abweichung: "#fortschreibung-endpunkt-k3"
---
parameter:
  id: flood_bldg.sanity_o_m
  wert: 6.29
  einheit: "Mrd. EUR2026/a"
  band: null
  herkunft: herleitung:§4.6
  kennzeichnung: abschaetzung_kap3
  herleitung_anker: "#sanity-band"
  abgeleitet_aus: [flood_bldg.rate_bestand_gk3_gk4, flood_bldg.rate_bestand_gk2, flood_bldg.adressen_gk3_gk4, flood_bldg.adressen_gk2, flood_bldg.gebaeudewert_efh_om, flood_bldg.d_5]
  pruefstein: false
  rolle: pruefgroesse
  quelle: null
  preisstand: 2026
  datenebene: null
  bandzuordnung: [alle]
  endpunkt: K3-Wiederherstellung
  wertebereich_abweichung: "#fortschreibung-endpunkt-k3"
---
parameter:
  id: flood_bldg.gebaeudewert_efh_om
  wert: 527280
  einheit: "EUR2026"
  band: null
  herkunft: herleitung:§4.6
  kennzeichnung: abschaetzung_kap3
  herleitung_anker: "#sanity-band"
  abgeleitet_aus: [flood_bldg.wohnflaeche_je_wohngebaeude, flood_bldg.k_bgf, flood_bldg.n_efh_zfh]
  rolle: pruefgroesse
  quelle: null
  preisstand: 2026
  datenebene: null
  bandzuordnung: [alle]
  endpunkt: K3-Wiederherstellung
  wertebereich_abweichung: "#fortschreibung-endpunkt-k3"
---
parameter:
  id: flood_bldg.f_awm
  wert: 0.55
  einheit: "-"
  band: [0.40, 0.75]
  herkunft: herleitung:§7.2
  kennzeichnung: abschaetzung_kap3
  herleitung_anker: "#fortschreibung-neuwert-k3"
  sensitivitaet: "K3-Betrag 0,62 (0,45-0,85) statt 1,13 Mrd. EUR2026/a"
  rolle: sensitivitaet
  quelle: null
  preisstand: null
  datenebene: null
  bandzuordnung: [alle]
  endpunkt: K3-Wiederherstellung
  wertebereich_abweichung: "#fortschreibung-endpunkt-k3"
---
parameter:
  id: flood_bldg.q0
  wert: 0.15
  einheit: "-"
  band: [0.05, 0.30]
  herkunft: herleitung:§4.7
  kennzeichnung: abschaetzung_kap3
  herleitung_anker: "#q0-abschaetzung"
  ebene_status: geparkt
  ebene_hinweis: "Ausstattungsgrad Objektvorsorge, Datenquelle fehlt, Watchlist §4.7"
  rolle: waechter
  quelle: null
  preisstand: null
  datenebene: null
  bandzuordnung: [alle]
  endpunkt: K3-Wiederherstellung
  wertebereich_abweichung: "#fortschreibung-endpunkt-k3"
```

<a id="fortschreibung-endpunkt-k3"></a>

### 7.1 Antrag auf Fortschreibung des §4-Wertebereichs für die Familie K3/K4-Ereignisschäden (Anker `#fortschreibung-endpunkt-k3`) — beantragt am 13.09.2026

**Sachverhalt.** Das Parameter-Block-Format in §4 der Aufgabe gibt für `endpunkt` den Wertebereich
`mortalitaet | morbiditaet | beide` und für `bandzuordnung` als Beispiel Altersbänder
(`[65-74, 75-84, 85+]`) vor. Beides stammt aus der Gesundheitsfamilie (M0, #95, #96), für die die
Aufgabe geschrieben wurde. Die vier Blöcke dieses Kapitels tragen `endpunkt: K3-Wiederherstellung`
und `bandzuordnung: [alle]` und liegen damit **außerhalb** dieses Wertebereichs
(Befund 15 in `reviews/BEFUNDE_60.md`).

**Begründung.** #60 ist der erste Vertreter der Familie **K3/K4-Ereignisschäden** (§2.6). Sein
Endpunkt ist kein Gesundheitsendpunkt, sondern der Baustein eines Schadenskontos —
`K3-Wiederherstellung` aus `KWRA-Monetarisierung.xlsx`, Blatt „Schadenskonten-System" Z28, wie in
Kap. 1 („Konto-Einbettung") gebucht. Keiner der drei zugelassenen Werte träfe zu: `mortalitaet` und
`morbiditaet` sind für einen Sachschaden sachlich falsch, `beide` wäre irreführend, weil die
Personenfolgen desselben Ereignisses ausdrücklich **nicht** in #60, sondern in #101 (K1) gebucht
werden (Kap. 6, Modellgrenze 1). Ebenso hat der Hebel S092 keine Bandachse: Er wirkt als
kommunaler Pauschalfaktor gleichmäßig auf alle exponierten Gebäude (Modellgrenze der Abschätzung,
§5.1.2), weshalb `[alle]` und nicht eine Teilmenge von Bändern zugeordnet ist. Ein Umbiegen auf
einen der zugelassenen Werte wäre eine falsche Angabe, keine Einhaltung des Wertebereichs.

**Beantragt wird** (Entscheidung nicht in diesem Bericht — die Aufgabe wird nur durch
Fortschreibung geändert, §1/§5.4; dieser Abschnitt ist der Antrag, nicht die Änderung):

1. `endpunkt` erhält für Berichte der Familie K3/K4-Ereignisschäden zusätzlich den Wertebereich
   „Baustein-Name des Schadenskontos nach Blatt „Schadenskonten-System"" (hier
   `K3-Wiederherstellung`).
2. `bandzuordnung` erhält zusätzlich den Wert `[alle]` für Parameter ohne differenzierende
   Bandachse.
3. Das Block-Format wird um die fünf Felder erweitert, mit denen dieses Kapitel die Vorgabe P1
   maschinenlesbar erfüllt: `kennzeichnung:` (`quelle | abschaetzung_kap3`), `herleitung_anker:`
   (Pflicht bei `abschaetzung_kap3`), `wertebereich_abweichung:`, `abgeleitet_aus:` (bei berechneten
   Parametern) sowie `naeherung:`/`naeherung_richtung:` (bei ausgewiesenen Näherungen, hier
   \(s_{\text{bem}}\), §5.1.3). Auch diese Felder gehen über das §4-Template hinaus; sie sind
   deshalb Teil desselben Antrags und nicht still eingeführt. Ob der Lint sie erzwingt, entscheidet
   T-0234, nicht dieser Bericht.

**Status.** Beantragt am **13.09.2026**, noch nicht entschieden. Bis zur Entscheidung bleibt die
Abweichung an beiden Stellen ausgewiesen: hier im Berichtstext und maschinenlesbar im Feld
`wertebereich_abweichung:` jedes Blocks. Wird die Fortschreibung abgelehnt, ist der Umbau der
beiden Felder (und nicht ihre stille Beibehaltung) die Folge; nach der Regel „Divergenz wird nie
still im Code gefixt" wird das über den Befund-Ledger geführt.

<a id="fortschreibung-neuwert-k3"></a>

### 7.2 Antrag auf Fortschreibung der Arbeitsmappe: Neuwert statt Zeitwertansatz (Mon. J64/J65) (Anker `#fortschreibung-neuwert-k3`) — beantragt am 17.09.2026

**Sachverhalt.** `KWRA-Monetarisierung.xlsx`, Blatt „Risiken-Monetarisierung", schreibt für #60 über
J65 („Wie ID 59, …") → J64 („Wiederherstellungskosten (Gebäude, Hausrat, Fahrzeuge) je Ereignis;
**Zeitwertansatz**; …") den **Zeitwertansatz** vor. Das Blatt „Schadenskonten-System" C27 lässt für K3
beide Lesarten zu („Wiederherstellungs-/Zeitwertkosten"), die Kontodefinition Z26 spricht von
„Wiederherstellungskosten". Dieser Bericht bewertet mit **NHK-Neuwerten**: Wiederherstellungswert
**481.726,25 €₂₀₂₆** je exponiertem Wohngebäude (typgewichteter Wertsatz 1.781,532 €₂₀₂₆/m² BGF,
§4.3 Punkt 2; Mengengerüst Register 60-R24-01). Die Arbeitsmappe wird nicht
verändert (eiserne Regel 2); dieser Abschnitt ist der Antrag, nicht die Änderung (Befund 41 in
`reviews/BEFUNDE_60.md`).

**Entscheidung (W1, W6).** Der **Neuwert bleibt Basiswert** von #60; der Zeitwertansatz aus J64 wird
**nicht** übernommen, sondern als beziffertes Sensitivitätsband geführt. Beantragt wird, J64/J65 für
#60 auf „Wiederherstellungskosten zum Neuwert (NHK, indexiert); Zeitwertansatz als Sensitivitätsband"
fortzuschreiben. Begründung:

1. **Der Anker ist ein Neuwert-Anker.** \(\lambda = A^{*}/M_0\) (§4.4) stellt die Modellsumme gegen
   gezahlte Wohngebäude-Leistungen, und Wohngebäudeverträge decken zum gleitenden Neuwert (§4.2,
   Herleitung von \(\kappa\)). Würde nur der Basiswert je Gebäude auf den Zeitwert gesetzt, bliebe der
   kalibrierte K3-Betrag \(\lambda M_0 \equiv A^{*}\) **unverändert** — \(\lambda\) nähme allein die
   Alterswertminderung auf (Zentralwert \(A^{*}/(M_0 f_{\text{AWM}})\) = 1,132 / (1,243 · 0,55) =
   **1,66**, am unteren Faktor-Ende 1,132 / (1,243 · 0,40) = **2,28**; \(A^{*}\) aus §4.2,
   \(M_0\) aus §4.3). Diese beiden Werte sind die maßgebliche \(\lambda\)-Angabe dieses Abschnitts;
   der Beispielblock unten rechnet sie nach. Die Umstellung hätte dann keine Wirkung auf das Ergebnis,
   sondern verzerrte nur den Skalar: Derselbe Anker würde durch einen kleineren Nenner geteilt, ohne
   dass sich an der bewerteten Sache etwas ändert.
2. **Ein konsistenter Zeitwertansatz braucht eine Anker-Umrechnung ohne Quelle.** Erst wenn auch
   \(A^{*}\) und die Sanity-Grenzen (§4.6) mit demselben Faktor auf den Zeitwert umgerechnet werden,
   sinkt der Betrag. Für diese Umrechnung gibt es keine Quelle, nur die Abschätzung unten; nach W1 wird
   eine Abschätzung nicht an die Stelle des belegten Werts gesetzt, wenn sie den Basiswert trägt.
3. **Die Mappe ist selbst nicht eindeutig.** C27 nennt „Wiederherstellungs-/Zeitwertkosten", Z26
   „Wiederherstellungskosten"; der Antrag beseitigt den Widerspruch für #60 in Richtung der Lesart,
   die mit dem Anker übereinstimmt.

**Alterswertminderungsfaktor \(f_{\text{AWM}}\) = 0,55, Band 0,40–0,75 — Abschätzung von KAP3
(§3.9 Abgeschätzt).** Herleitung:

- **Regel (Quelle):** § 38 ImmoWertV: „Der Alterswertminderungsfaktor entspricht dem Verhältnis der
  Restnutzungsdauer zur Gesamtnutzungsdauer." Die Gesamtnutzungsdauer (GND) für Ein- und
  Zweifamilienhäuser, Doppel-, Reihen- und Mehrfamilienhäuser beträgt nach ImmoWertV Anlage 1
  **80 Jahre**. Die Restnutzungsdauer (RND) ist ohne Modernisierung GND − Alter und verlängert sich
  nach ImmoWertV Anlage 2 („Modell zur Ermittlung der Restnutzungsdauer von Wohngebäuden bei
  Modernisierungen") mit der Modernisierungspunktzahl. ImmoWertV § 38 und Anlagen 1/2,
  https://www.gesetze-im-internet.de/immowertv_2022/__38.html,
  https://www.gesetze-im-internet.de/immowertv_2022/anlage_1.html,
  https://www.gesetze-im-internet.de/immowertv_2022/anlage_2.html, Zugriff 17.09.2026.
- **Abgeschätzt (keine Quelle):** Eine bundesweite Statistik der Restnutzungsdauer exponierter
  Wohngebäude existiert nicht (Datenlücke §3.8). Angesetzt wird ein mittleres Gebäudealter des
  flussnahen Bestands von rund 50 Jahren (überwiegend Nachkriegsbestand; flussnahe Lagen sind eher
  früh bebaut) und eine durch Teilmodernisierung verlängerte mittlere RND von **44 Jahren** ⇒
  44 / 80 = **0,55**. **Unteres Bandende 0,40:** weitgehend unmodernisierter Altbestand, RND 32 Jahre
  (32 / 80). **Oberes Bandende 0,75:** jüngerer oder umfassend modernisierter Bestand, RND 60 Jahre
  (60 / 80).
- **Modellgrenze der Abschätzung:** Der Faktor gilt für das Gebäude als Ganzes. Hochwasser trifft vor
  allem Ausbauteile mit kürzerer Nutzungsdauer (Estrich, Putz, Bodenbeläge, Haustechnik); auf sie
  bezogen läge der Faktor eher am unteren Bandende.

**Zeitwert je Gebäude:** 481.726,25 € · 0,55 = **264.949 €₂₀₂₆** (Band 192.691–361.295 €₂₀₂₆).

**Ergebnis-Sensitivität auf den K3-Betrag.** Ausgangspunkt ist die kalibrierte Bundessumme
\(\lambda M_0 = A^{*}\) = **1,132 Mrd. €₂₀₂₆/a** (§4.2, §4.6). Bei konsistentem Zeitwertansatz
(Basiswert, Anker und Sanity-Grenzen mit demselben Faktor) sinkt sie auf 1,132 · 0,55 =
**0,62 Mrd. €₂₀₂₆/a** (Band 1,132 · 0,40 bis 1,132 · 0,75 = **0,45–0,85 Mrd. €₂₀₂₆/a**), also um
**−0,51 Mrd. €₂₀₂₆/a bzw. −45 %** (Band −25 % bis −60 %). Dieselbe Verschiebung gilt je Kommune, weil
\(f_{\text{AWM}}\) bundesweit einheitlich wirkt. Die unabhängige Sanity-Untergrenze fiele mit auf 0,189 · 0,55 =
**0,104 Mrd. €₂₀₂₆/a** (§4.6). Werden nur die Gebäudewerte umgestellt, der Anker aber nicht, bleibt der
Betrag bei 1,132 Mrd. €₂₀₂₆/a und nur \(\lambda\) steigt (Werte in Begründung 1). Im Produkt wird der
Faktor nach Vorgabe P1 als „Abschätzung von KAP3" mit dieser Herleitung in der Parameterliste geführt
(§4.8).

```python test: beispiel_60_zeitwert
# 7.2 Zeitwertansatz als Sensitivitaetsband (Abschaetzung von KAP3)
GND = 80.0
f_mid, f_lo, f_hi = 44.0 / GND, 32.0 / GND, 60.0 / GND
assert (f_mid, f_lo, f_hi) == (0.55, 0.40, 0.75)
theta = 0.596                                    # Typ-Mix EFH/ZFH wie in 4.3 Punkt 2
n_mix = theta * 1950.0 + (1 - theta) * 1533.0    # typgewichteter Wertsatz EUR2026/m2 BGF
wert_geb = 208.0 * 1.30 * n_mix                  # Neuwert je exponiertem Wohngebaeude (4.3)
assert abs(wert_geb - 481726.25) < 1.0
assert abs(wert_geb * f_mid - 264949.0) < 1.0
assert abs(wert_geb * f_lo - 192691.0) < 1.0 and abs(wert_geb * f_hi - 361295.0) < 1.0
A_stern = 1.838 * 0.65 * 1.54 * 0.50 * 1.15 * 1.07   # Anker wie in 4.2 (A_ver = 1,838)
assert abs(A_stern - 1.132) < 5e-3
# M0 wie in 4.3: gemessene Klassenraten, Wohngebaeudeanteil, nationales Mengengeruest
w_wohn = 0.872
r_gk34 = 0.005979599550826
r_gk2 = 0.000675151053693
M0 = (w_wohn * wert_geb * 339_000 * r_gk34 + w_wohn * wert_geb * 1_380_000 * r_gk2) / 1e9
assert abs(M0 - 1.243) < 5e-3
# nur Basiswert umgestellt: Betrag unveraendert, lambda steigt (Begruendung 1)
assert abs(A_stern / (M0 * f_mid) - 1.66) < 5e-3
assert abs(A_stern / (M0 * f_lo) - 2.28) < 5e-3
# konsistent umgestellt: K3-Betrag und Band
assert abs(A_stern * f_mid - 0.62) < 5e-3
assert abs(A_stern * f_lo - 0.45) < 5e-3 and abs(A_stern * f_hi - 0.85) < 5e-3
assert abs(A_stern * (1 - f_mid) - 0.51) < 5e-3
U = 0.189                                        # unabhaengige Sanity-Untergrenze aus 4.6, Mrd. EUR2026/a
assert abs(U * f_mid - 0.104) < 5e-4
```

**Status.** Beantragt am **17.09.2026**, noch nicht entschieden. Bis zur Entscheidung rechnet #60 mit
dem Neuwert und weist den Zeitwertansatz als Band aus (hier, §3.4, §4.8, Kap. 6 Modellgrenze 9).
**Stand an der Quelle (Befund 53):** Das Blatt „Abgleich-Protokoll" der Arbeitsmappe führt zu #60
**noch keine Zeile**; vorgesehen ist eine Zeile nach dem Muster Z151 (Quelle-ID 60, Ziel J64/J65, Art
„Fortschreibung Bewertungslogik (keine Kante)", Inhalt „Neuwert (NHK, indexiert) statt
Zeitwertansatz für #60; Zeitwert als Sensitivitätsband \(f_{\text{AWM}}\) = 0,55 (0,40–0,75);
beantragt 17.09.2026"). **Entscheider:** der Eigner der Arbeitsmappe (Nutzer bzw. Aufsichtsrat, wie
bei den bisherigen Fortschreibungen der Aufgabe); dieser Bericht ändert die Mappe nicht (eiserne
Regel 2). **Frist:** vor der Abnahme und Integration von #60 (`/integriere-risiko 60`). Bis die
Zeile im Abgleich-Protokoll steht oder der Antrag abgelehnt ist, ist die Abnahme von #60 im Punkt
Quellen-Synchronität (Aufgabe §5 LF 14, §6) blockiert; Kap. 8 (Quelle 2) und B4 verweisen auf diesen
Status.
Wird der Antrag abgelehnt, sind Basiswert, \(A^{*}\), \(U\), \(O_u\) und \(O_M\) mit \(f_{\text{AWM}}\)
umzurechnen; das läuft über den Befund-Ledger, nicht still im Code.

## 8 Quellen (§3.8)

Format je Quelle nach §3.8: Autor/Organ, Jahr, Titel, DOI/URL, Zugriffsdatum, Archiv-Snapshot —
fehlt ein Archiv-Snapshot, wird die Lücke im Eintrag ausdrücklich begründet; bei den beiden Arbeitsmappen
statt DOI/URL/Archiv-Snapshot Dateistand (Commit-Hash, Datum) und Prüfsumme (SHA-256) mit
Zugriffsdatum. Die Angaben zu Quelle 3 sind wörtlich aus `backend/app/data/sources.py`
(`BBK_Hochwasserschutzfibel`) übernommen, ohne dass diese Datei geändert wurde; Volltextverifikation
vor Übernahme (§3.8) hat für diese Quelle bereits bei ihrer Aufnahme in `sources.py` stattgefunden,
für #60 ist sie hier weiterhin **nicht erneut** im Volltext geprüft (sie geht nicht in einen Wert
dieses Berichts ein — vgl. B6, „Hochwasserschutzfibel … hier nicht im Volltext geprüft“).

1. **KWRA-Schadensbaum × UBA-Klimawirkungsketten**, Arbeitsmappe
   `docs/Schadensbaum/KWRA-Schadensbaum_X_UBA-klimawirkungsketten.xlsx` — Sheets
   „Klimawirkungsketten“ (Z3–Z272, u. a. wie in Kap. 1 zitiert) und „Schadensbaum-Netzwerkliste“
   (Z13, Z50, Z53, Z61). **Dateistand:** Git-Commit `1a89a2e8a69539eb15aa48aec214a44a05567137`
   (2026-08-17). **Prüfsumme (SHA-256):**
   `2faac648aade047f274f6b305a73c44ef3727f16a379124bf35eb590c0735a28`. **Zugriffsdatum:**
   13.09.2026 (Repository-Arbeitskopie, Volltext im Original geprüft — Sheet-/Zeilenbezüge oben
   und in Kap. 1/2 einzeln verifiziert).
2. **KWRA-Monetarisierung**, Arbeitsmappe `docs/Schadensbaum/KWRA-Monetarisierung.xlsx` — Sheets
   „Risiken-Monetarisierung“ (Z51, Z54–Z56, Z64, Z65, Z106), „Schadenskonten-System“ (Z26–Z30),
   „Rechenregeln“ (Z9, Z11, Z20), „Abgleich-Protokoll“ (P5, P15, P16). **Dateistand:** Git-Commit
   `68442ca12689045730c349c4160abe963096f733` (2026-08-30). **Prüfsumme (SHA-256):**
   `4383882d3a935f09abe891b6f60ec6f8843e28da627813eaaed31fe15308ce2d`. **Zugriffsdatum:**
   13.09.2026 (Repository-Arbeitskopie, Volltext im Original geprüft — Sheet-/Zeilenbezüge oben
   und in Kap. 1/2 einzeln verifiziert). **Anhängige Abweichung:** In einem verbindlichen Punkt
   weicht dieser Bericht von der Mappe ab — Neuwert statt des in Mon. J65 → J64 vorgeschriebenen
   Zeitwertansatzes. Antrag auf Fortschreibung vom 17.09.2026, noch nicht entschieden, im
   Abgleich-Protokoll noch ohne Zeile; Entscheider, Frist und Folge für die Abnahme in §7.2
   („Status", Anker `#fortschreibung-neuwert-k3`).
3. **Bundesministerium für Wohnen, Stadtentwicklung und Bauwesen (BMWSB) (2022):**
   „Hochwasserschutzfibel – Objektschutz und bauliche Vorsorge“, Berlin, Deutschland. URL
   `https://www.bmwsb.bund.de/SharedDocs/downloads/DE/publikationen/raumordnung/hochwasserschutzfibel.html`,
   Archiv-Snapshot
   `https://web.archive.org/web/20251121213733/https://www.bmwsb.bund.de/SharedDocs/downloads/DE/publikationen/raumordnung/hochwasserschutzfibel.html`,
   Zugriff 4. Juli 2026 (Angaben wörtlich übernommen aus `backend/app/data/sources.py`,
   Eintrag `BBK_Hochwasserschutzfibel`, ohne diese Datei zu ändern). Kandidat für die bauliche
   Vorsorge (60-S092-01, Register-Zeile Kap. 2; B6, Kap. 1 „Konto-Einbettung“); **für #60 nicht im
   Volltext geprüft** und geht deshalb nach §3.8 in keinen Wert dieses Berichts ein.
4. Evidenz-Quellen der belegten Registerzeilen: siehe die Langbelege B1–B6 unter der Tabelle in
   Kap. 2, dort jeweils mit Vollzitat, DOI/URL, Zugriffsdatum 13.09.2026 und dem Vermerk
   „Volltext geprüft“ bzw. „Volltext gegengelesen“. Für S092 ist keine Primärquelle verwendet
   (§5.1 ABGESCHÄTZT, Quelle 3 oben ist nur Kandidat, nicht Basis der Zahl). **Format der
   Langbelege (§3.8):** Autor/Organ, Jahr, Titel, DOI/URL, Zugriffsdatum **und Archiv-Snapshot**;
   der Archiv-Snapshot ist für die externen Webquellen in **B1–B3** (T-0307, 17.09.2026) und in
   **B4–B6** (T-0308, 17.09.2026) nachgetragen; damit trägt jede externe Webquelle der Langbelege
   entweder einen Snapshot mit Datum oder eine ausdrückliche Begründung des Verzichts. Bei
   DOI-gebundenen Zeitschriftenquellen ist der Snapshot entbehrlich (die DOI ist der persistente
   Nachweis) und dort, wo er vorliegt, nur zusätzliche Absicherung der Verlagsseite. Verzichtet
   wird auf einen Snapshot bei der Destatis-Pressemitteilung Nr. 241/2026 (B4 Quelle 5): die
   Wayback Machine führt dort nur einen Abruf mit Statuscode 403, und die Wiedergabe von
   Destatis-Pressemitteilungen ist archivseitig gesperrt — der bei Quelle 1 genannte Snapshot ist
   aus demselben Grund indexiert, aber nicht abrufbar. Befund 42 ist damit abgeschlossen.
5. **Gesamtverband der Deutschen Versicherungswirtschaft e. V. (GDV) (2025):**
   „GDV-Naturgefahrenstatistik 2024: Hochwasserschäden mehr als verdoppelt“, Medieninformation
   vom 31.05.2025 (Feld „Zuletzt aktualisiert“), Berlin. URL
   `https://www.gdv.de/gdv/medien/medieninformationen/gdv-naturgefahrenstatistik-2024-hochwasserschaeden-mehr-als-verdoppelt-188734`,
   Archiv-Snapshot
   `https://web.archive.org/web/20260510141613/https://www.gdv.de/gdv/medien/medieninformationen/gdv-naturgefahrenstatistik-2024-hochwasserschaeden-mehr-als-verdoppelt-188734`,
   Zugriff 17.09.2026 (über den genannten Snapshot). Trägt in §4.1 den Ankerwert: „Allein
   Starkregenereignisse und Überschwemmungen schlugen mit 2,6 Mrd. Euro zu Buche – rund eine
   Milliarde Euro mehr als im langjährigen Durchschnitt“, dazu 5,7 Mrd. € Gesamtschaden 2024,
   4,4 Mrd. € Sachversicherung und 1,3 Mrd. € Kraftfahrt. **Volltext geprüft** (Zitate am
   Snapshot wörtlich abgeglichen, 17.09.2026).
6. **Gesamtverband der Deutschen Versicherungswirtschaft e. V. (GDV) (2025):**
   „Versicherungsquote bei Elementarschadenversicherung steigt kontinuierlich“, Statistikseite des
   *Datenservice zum Naturgefahrenreport*, Rubrik „Sachversicherung Elementar“, Stand der Grafik
   10.10.2025 (Feld „Zuletzt aktualisiert“), Berlin. URL
   `https://www.gdv.de/gdv/statistik/datenservice-zum-naturgefahrenreport/sachversicherung-elementar/versicherungsquote-bei-elementarschadenversicherung-steigt-kontinuierlich--147644`,
   Archiv-Snapshot
   `https://web.archive.org/web/20260417162956/https://www.gdv.de/gdv/statistik/datenservice-zum-naturgefahrenreport/sachversicherung-elementar/versicherungsquote-bei-elementarschadenversicherung-steigt-kontinuierlich--147644`,
   Zugriff 17.09.2026 (über den genannten Snapshot). Trägt in §4.1 die Versicherungsdichte 2024:
   „2024 sind 10,2 Mio. Wohngebäude gegen Überschwemmung durch Starkregen und Hochwasser sowie
   andere Naturgefahren versichert. Das entspricht einer Versicherungsdichte von immerhin 57 %
   bezogen auf Wohngebäude-Feuer“. **Volltext geprüft** (Zitate am Snapshot wörtlich abgeglichen,
   17.09.2026).
7. **Gesamtverband der Deutschen Versicherungswirtschaft e. V. (GDV) (2025):** „Datenservice zum
   Naturgefahrenreport 2025 — Tabellen · Grafiken · Karten“, Broschüre, Berlin. URL
   `https://www.gdv.de/resource/blob/193410/e09858f310a1f7b4d3c2135df59369ce/naturgefahrenreport-2025-datenservice-data.pdf`,
   Archiv-Snapshot
   `http://web.archive.org/web/20260107031605/https://www.gdv.de/resource/blob/193410/e09858f310a1f7b4d3c2135df59369ce/naturgefahrenreport-2025-datenservice-data.pdf`,
   Zugriff 17.09.2026. Quelle der Jahresreihe 2002–2024 (S. 17, Grafik „Zeitreihe
   Naturgefahrenschäden – Hochrechnung auf Bestand und Preise 2024“, Balken Elementar) und damit
   des Revisionsstands in §4.1 (Aktualisierungsvermerke 10.10.2025 und 30.12.2025). URL,
   Snapshot und Zugriffsdatum sind wörtlich aus `docs/evidenz/60_gdv_jahresreihe_2002_2024.csv`
   (Spalten `quelle_url`, `archiv`, `zugriff`) übernommen, wo die abgelesenen Jahreswerte
   einzeln mit Fundstelle stehen.

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
  EAD = Σ über die drei HQ-Szenarien: p(HQ) × Schadensgrad(Wassertiefe; Gebäudequalität und
  Baustoff als Band) × Gebäudewert der Zelle (Gebäudetyp im Wertsatz). Die Typachse von FLEMOps
  geht in der Umsetzung nicht in den Schadensgrad ein — ausgewiesene Modellgrenze, §3.3
  „Typstruktur“. Achsen und Klassen nach FLEMOps-Bauart
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
| Datenverfügbarkeit | **hoch** — die Eingänge der drei rechnenden Ebenen sind frei zugänglich und im Register belegt: HWGK-Raster der Länder (60-W085-01), DGM1 (60-S074-01), Zensus-2022-Gitter mit Gebäudetyp und Wohnfläche (60-R24-01), NHK 2010 aus ImmoWertV Anlage 4. Die vierte Ebene GEBAEUDEZUSTAND_BAUSTOFF ist geparkt (Datenquelle fehlt, keine bundesweite offene Erhebung, §3.2); sie fährt mit dem Neutralwert 1,00 und steht auf der Beschaffungs-Watchlist, die Zustands- und Materialachsen sind als Bänder geführt, nicht als Zelldaten (60-S093-01/60-S094-01). „hoch“ bleibt bestehen, weil der Neutralwert die Rechnung nicht blockiert und die Lücke als Modellgrenze ausgewiesen ist; bei (b) und (c) wiegt dieselbe Bestandslücke schwerer | **hoch** — Landnutzung aus ATKIS/CORINE plus HWGK; die Schadensraten selbst stammen jedoch aus der niederländischen Fallstudie B2 und sind für Deutschland nicht belegt (§3.8 Datenlücke) | **gering** — Bauweise, Fließgeschwindigkeit und Bauzustand je Gebäude sind bundesweit **nicht** erhoben (ausdrückliche Datenlücken in 60-S093-01 und 60-S094-01); es bliebe ein Modell mit gesetzten Merkmalen, das Vorgabe P1 nur über eine Kette von Abschätzungen erfüllte |
| Maßnahmen-Anschluss | **hoch** — (a) bietet als einziger Ansatz den Angriffspunkt für einen zellscharfen Objektschutz-Hebel S092; umgesetzt ist er derzeit als kommunenweiter Pauschalfaktor r_S092 auf den K3-Erwartungsschaden (§5.1, Modellgrenze (1)); die Schutzsysteme S096–S098 sollen über die R7-Weiche mit #50 am Hazard-Term anschließen; in der Formel existiert heute nur der Angriffspunkt für S092 (§5.1), die R7-Weiche ist als FS-Schutzsystem inaktiv geparkt (§3.4) — die Bewertung stützt sich für die Schutzsysteme auf den vorgesehenen, noch nicht gerechneten Anschluss, den (b) und (c) nicht besser bedienen | **gering** — Objektschutz wirkt am Gebäude, die Flächenrate kennt kein Gebäude: S092 ließe sich nur als pauschaler Abschlag auf das Gesamtergebnis anhängen, ohne Wirkungsort (§3.5); der bleibende Unterschied zu (a) ist der fehlende Angriffspunkt — bei (a) ist er vorhanden und nur noch nicht ausgeschöpft, bei (b) fehlt er dauerhaft | **hoch** — feinster Angriffspunkt für Objektschutz denkbar, aber nur nutzbar, wenn die Gebäudemerkmale vorlägen; ohne sie fällt der Hebel auf dieselbe Pauschale zurück wie bei (b) |
| Architektur-Konformität | **hoch** — Schicht-B-Form Menge × Rate × Preis auf Zellebene mit physischer Zwischengröße (überflutete Gebäude, Wassertiefe, Schadensgrad) vor dem Euro; Schicht-A-Index aus denselben Knoten ableitbar | **mittel** — formal Menge × Rate × Preis, aber die physische Zwischengröße vor dem Euro fehlt: die Flächenrate springt von Quadratmetern direkt in Euro | **gering** — Aggregationsebene Einzelgebäude liegt unterhalb der Zellebene des Produkts; es entstünde eine zusätzliche Objektebene samt eigener Fortschreibung |
| Aufwand (Ressourcenverträglichkeit §3.4) — *umgekehrte Skala: gering = günstig, hoch = teuer* | **mittel** — vier Datenebenen nach §3.2, davon drei neu anzulegen (HQ_FLAECHE, HQ_TIEFE, GEBAEUDEWERT) und eine geparkt (GEBAEUDEZUSTAND_BAUSTOFF, Neutralwert 1,00, Beschaffungs-Watchlist); Kalibrierung und Abgleich laufen auf Bundesland- und Gemeindepunkt-Stichproben, ein nationaler 100-m-Vollraster-Lauf ist zu keinem Zeitpunkt nötig | **gering** — zwei Datenebenen, Stichprobenprüfung ebenso auf Gemeindepunktebene möglich; der günstigste Ansatz, aber der Aufwandsvorteil beruht auf der weggelassenen Bestandsachse | **hoch** — Objektebene für rund 19,7 Mio Wohngebäude mit Merkmalen, die erst erhoben werden müssten; eine Stichprobenprüfung genügte für die Kalibrierung nicht, weil die Merkmalsverteilung selbst das Ergebnis trägt |

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
Materialband \(f_{\text{S094}}\) = 1,00 (0,84–1,18) in Ansatz (a).

## Entscheidungslog

| Nr | Frage | angewendete Entscheidung | Begründung | Alternative | Auswirkung |
|---|---|---|---|---|---|
| 1 | Welcher W-Knoten trägt #60? | W117 (KWK Z272), mit W085 eine Ebene tief | einziger Bauwesen-Knoten für Gebäudeschäden mit Hochwasser-Eingang; NW Z61 Input 49 = W085; Code-Bestand geht vom selben Knoten aus, trägt aber nur eine Teilmenge mit abweichender Namensquelle (Befund 13, → Log Nr. 6) | nur W085 als Kette (dann fehlten S092–S104 und R24, also Vulnerabilität und Mengengerüst) | 32 Knoten in Bilanz und Register |
| 2 | Familie? | neue Familie K3/K4-Ereignisschäden, Kap. 9 angelegt | kein K3-Bericht in `docs/methodik/` | Übernahme der K1-Struktur (#95) — passt nicht zu Ereignislogik A5 | Drei-Ansätze-Vergleich Pflicht |
| 3 | S092 ohne zulässige Effektgröße | P2-Abschätzung r = 0,035 (0,0075–0,0832) | Vorgabe P2, §3.5; Querschnittsbefragungen sind keine Maßnahmen-Effektgröße | Wirkung null (unzulässig nach P2) | Maßnahmen-Modul, kein Basiswert |
| 4 | Slug | `gebaeudeschaeden_flusshochwasser` | kurz, eindeutig gegen #59 (Starkregen) und #46 (Küste) | `flusshochwasser` (verwechselbar mit Id 49) | Dateinamen Bericht/Ledger |
| 5 | Welcher Ansatz wird umgesetzt? (Ansatz-Vergleich §2.6/§3.7) | **13.09.2026 (T-0237):** Ansatz **(a)** Szenario-Erwartungswert mit typisierter Tiefen-Schadensfunktion je 100-m-Zelle — p(HQ) × Schadensgrad(Wassertiefe · Gebäudetyp · Gebäudequalität) × Gebäudewert | einziger Ansatz, der in den sechs Güte-Kriterien durchgehend „hoch“ trägt (das siebte Kriterium Aufwand läuft umgekehrt: dort ist „gering“ günstig, (a) liegt mit „mittel“ über (b) und weit unter (c) und ist nach §3.4 ressourcenverträglich): vollständig aus frei zugänglichen, im Register belegten Datenebenen speisbar, Wirkungsort für S092 und die R7-Weiche vorhanden, Schicht-B-Form mit physischer Zwischengröße vor dem Euro, Kalibrierung und Abgleich auf Stichprobenebene ohne nationalen Vollraster-Lauf (§3.4) | (b) aggregierte Flächenschadensrate — kein Wirkungsort für den Maßnahmen-Hebel, tragender Wert nur aus niederländischer Fallstudie (B2); als Ergänzungsmodul vorgesehen. (c) Schadensgradmodell D0–D6 am Einzelgebäude — Bauweise/Bauzustand bundesweit nicht erhoben, Umrechnung Grad → Euro nicht belegt | Umsetzungsgrundlage für Kap. 3 und Prototyp der Familie K3/K4-Ereignisschäden (bindet später #50 und #47); Kopfzeile und Kap. 9 nachgezogen |
| 6 | Divergenz Bericht ↔ Code bei den Namenslisten von #60 (Befund 13) | **13.09.2026 (T-0243):** Bericht auf den belegbaren Stand korrigiert (Kap. 1: Teilmenge mit abweichender Namensquelle statt „genau"); Code (`backend/app/data/catalog.py`, `kwra_id: 60`) bleibt unverändert | eiserne Regel 5 — Divergenz Bericht ↔ Code wird nie still im Code gefixt; Angleichen des Codes ist Aufgabe der Integration, nicht dieses Berichtsschritts | Code stillschweigend an W117 nachziehen (verstieße gegen eiserne Regel 4/5, kein Prüfmittel im Rahmen dieses Pakets) | Divergenz als Integrationspunkt für `/integriere-risiko 60` geführt: `sensitivity_names` und `upstream_names` in `catalog.py` müssen dort gegen die 7 Sensitivitäten und 8 Wirkungs-Eingänge von W117 abgeglichen werden |
| 7 | Neuwert oder Zeitwertansatz der Arbeitsmappe (Mon. J65 → J64) als Basiswert K3? (Befund 41) | **17.09.2026 (T-0285):** Neuwert (NHK, indexiert, 527.280 €₂₀₂₆ je Wohngebäude) bleibt Basiswert; Zeitwertansatz als Sensitivitätsband mit \(f_{\text{AWM}}\) = 0,55 (0,40–0,75, Abschätzung von KAP3); Abweichung von J64 als Antrag auf Fortschreibung in §7.2 | W1/W6: der Anker \(A^{*}\) ist neuwertbasiert (gleitender Neuwert, §4.2); eine Umstellung nur des Basiswerts ließe den kalibrierten Betrag unverändert und höbe \(\lambda\) auf 1,66 (bis 2,28) (**nachgezogen 23.09.2026 (T-0571)** auf den geltenden Stand \(A^{*}\) = 1,132 (§4.2), \(M_0\) = 1,243 Mrd. €₂₀₂₆/a und \(\lambda\) = 0,911 (§4.3/§4.4): 1,132 / (1,243 · 0,55) = 1,66, am unteren Faktor-Ende 1,132 / (1,243 · 0,40) = 2,28; frühere Nachzüge T-0313 und T-0320; die Entscheidung selbst bleibt unberührt); ein konsistenter Zeitwertansatz braucht eine quellenlose Anker-Umrechnung | Zeitwertansatz übernehmen und \(A^{*}\), \(U\), \(O\) mit \(f_{\text{AWM}}\) umrechnen | Basiswert, \(M_0\) und \(\lambda\) unverändert; Sensitivität K3-Betrag 0,62 (0,45–0,85) statt der kalibrierten Bundessumme aus §4.6 (−45 %); Kap. 6 Modellgrenze 9 und Versionsstempel präzisiert |
| 8 | Anker \(A^{*}\) aus dem Einzeljahr 2024 oder aus dem Mehrjahresmittel 2002–2024 der GDV-Reihe? (Befund 34) | **17.09.2026 (T-0320):** Mehrjahresmittel per Kleinste-Quadrate-Ankerbestimmung (§4.1/§4.4): \(A^{*}\) = 1,132 Mrd. €₂₀₂₆/a | ein Einzeljahr trägt die volle Jahreswitterung (Hochwasserereignisse streuen stark zwischen den Jahren) und wäre kein robuster Anker für einen langfristigen Skalar; die Kleinste-Quadrate-Bestimmung über die gesamte Reihe 2002–2024 glättet diese Streuung und ist reproduzierbar aus den veröffentlichten Jahreswerten | Anker aus dem letzten verfügbaren Einzeljahr (2024) | \(A^{*}\) = 1,132 (statt 0,985 nach dem verworfenen Stichprobenlauf), \(\lambda\) = 0,832, Band 0,11–3,49; §7.2 Zeitwert-Sensitivität 1,51 (2,08). **Nachtrag 23.09.2026 (T-0570, Ledger-Befund 58):** mit typgewichtetem Wertsatz in \(M_0\) (1,243 statt 1,360) \(\lambda\) = 0,911, Band 0,12–3,93 (§4.3/§4.4) |
