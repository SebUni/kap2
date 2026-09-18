# Quellen- und Parameterrecherche kwra_id 62 — Stadtklima / Wärmeinseln

Zuarbeit für die Abschnitte 2 (Wirkungskette) und 7 (Parameterliste/Quellen) des künftigen
Methodik-Steckbriefs zu kwra_id 62 (`backend/app/data/catalog.py`, `PLANNED_RISKS`, Zeile 317–322).
Kein Methodik-Bericht, kein Euro-Betrag — reine Beleg-Zuarbeit nach dem Muster
`docs/evidenz/register.md`.

Quellen-Arbeitsmappen:

- `docs/Schadensbaum/KWRA-Schadensbaum_X_UBA-klimawirkungsketten.xlsx`,
  Blatt „Klimawirkungsketten" (Id `W124`, Name „Stadtklima/Wärmeinseln", Zeile 279 —
  Kopfzeile ist Zeile 1, Zeilenangaben unten sind Excel-Zeilennummern dieses Blatts)
  und Blatt „Schadensbaum-Netzwerkliste" (Id `62`, Name „Stadtklima / Wärmeinseln", Zeile 63).
- `docs/Schadensbaum/KWRA-Monetarisierung.xlsx`, Blatt „Risiken-Monetarisierung", Zeile 67
  (Id 62).

Arbeitsmappe vor Code (Eiserne Regel 5, CLAUDE.md): Wo die Arbeitsmappe von `catalog.py`
abweicht, gilt die Arbeitsmappe; die Abweichung steht unten als eigene Kanten-Zeile, nicht
still im Code gelöst.

## Kanten

Wirkungskette Gefahr → Exposition → betroffenes Schutzgut für Id 62 (kwra_id 62 =
Netzwerkliste-Id 62 = Klimawirkungsketten-Id `W124`, „Stadtklima/Wärmeinseln").

| Kante | Blatt | Zeile | Beleg |
|---|---|---|---|
| Gefahr Hitze (E02) → Wirkung Stadtklima/Wärmeinseln (W124) | Klimawirkungsketten | 279 | Spalte `Input_IDs_Einflüsse` = "E02; E19", `Input_Namen_Einflüsse` = "Hitze; Sonnenscheindauer" |
| Gefahr Sonnenscheindauer (E19) → Wirkung Stadtklima/Wärmeinseln (W124) | Klimawirkungsketten | 279 | dieselbe Zelle wie oben, zweiter Einfluss derselben Zeile |
| Vorgelagerte Wirkung Vegetation in Siedlungen (W127, = kwra_id 61) → Stadtklima/Wärmeinseln (W124) | Klimawirkungsketten | 279 | Spalte `Input_IDs_Wirkung` = "W127", `Input_Namen_Wirkung` = "Vegetation in Siedlungen" |
| Exposition Vorkommen von Bau- und Immobilienunternehmen (R23) → Stadtklima/Wärmeinseln (W124) | Klimawirkungsketten | 279 | Spalte `Input_IDs_Räumlich` = "R23; R24; R25", `Input_Namen_Räumlich` nennt "Vorkommen von Bau- und Immobilienunternehmen" |
| Exposition Vorkommen von Gebäuden (R24) → Stadtklima/Wärmeinseln (W124) | Klimawirkungsketten | 279 | dieselbe Zelle, zweite Exposition |
| Exposition Vorkommen von Siedlungsinfrastrukturen (R25) → Stadtklima/Wärmeinseln (W124) | Klimawirkungsketten | 279 | dieselbe Zelle, dritte Exposition |
| Stadtklima/Wärmeinseln (W124) → betroffenes Schutzgut/Handlungsfeld Menschliche Gesundheit | Klimawirkungsketten | 279 | Spalte `Zu_Handlungsfelder` = "Menschliche Gesundheit" |
| Stadtklima/Wärmeinseln (Id 62) → nachgelagerte Wirkung 95 „Hitzebelastung" | Schadensbaum-Netzwerkliste | 63 | Spalte `Output_IDs_Wirkung` = "95; 65; 87" |
| Stadtklima/Wärmeinseln (Id 62) → nachgelagerte Wirkung 65 „Bedarf an Kühlenergie" | Schadensbaum-Netzwerkliste | 63 | dieselbe Zelle wie oben |
| Stadtklima/Wärmeinseln (Id 62) → nachgelagerte Wirkung 87 „Leistungseinbußen von Beschäftigten" | Schadensbaum-Netzwerkliste | 63 | dieselbe Zelle wie oben |
| Stadtklima/Wärmeinseln (Id 62) → keine eigene Buchung, wirkt nur als Übertragungskanal (0 €) | Risiken-Monetarisierung (KWRA-Monetarisierung.xlsx) | 67 | Spalte „Rolle in der Monetarisierung" = "Rein vorgelagert (0 €)"; „Wirkt über / bucht in" = "→ 95, 65, 87"; Regel R2 |
| **Abweichung Arbeitsmappe ↔ Code:** Zeile 279 führt 7 Sensitivitäten (S094 Verwendete Baumaterialien auf Gebäudeebene, S095 Begrünung von Gebäuden, S096 Bauliche/organisatorische/finanzielle Vorsorge der öffentlichen Hand, S097 Zustand von (Schutz-)Infrastrukturen, S098 Verwendete Baumaterialien von (Schutz-)Infrastrukturen, S099 Begrünung von Städten/Siedlungen, S100 Grad der Versiegelung); `catalog.py` führt nur zwei (S099, S100) | Klimawirkungsketten Zeile 279 (Arbeitsmappe) vs. `backend/app/data/catalog.py` Zeile 321 (Code) | Spalte `Input_IDs_Sensitivitäten` = "S094; S095; S096; S097; S098; S099; S100" | Arbeitsmappe gilt (Eiserne Regel 5): fünf Sensitivitäten (S094–S098) fehlen in `sensitivity_names`; nicht hier still im Code ergänzt, sondern als Befund für den künftigen Methodik-Bericht #62 vermerkt |

## Parameter

Parameterrecherche für die künftige Methodik zu Id 62. Jede Zeile trägt in der Spalte
„Herkunft" entweder eine zitierfähige Quelle oder — wo noch keine belegte Zahl vorliegt —
wörtlich das Wort „Abschaetzung" (Vorgabe P1, CLAUDE.md).

| Parameter | Wert/Bandbreite | Herkunft | Anmerkung |
|---|---|---|---|
| Gefahr Hitze (E02) als Eingangsgröße der Wirkungskette | qualitativ, kein Schwellenwert in der Arbeitsmappe | Quelle: Klimawirkungsketten, Zeile 3 (Id E02, Name „Hitze", Typ „Einfluss") | deckungsgleich mit `hazard_names[0]` in `catalog.py` Zeile 319 |
| Gefahr Sonnenscheindauer (E19) als Eingangsgröße der Wirkungskette | qualitativ, kein Schwellenwert in der Arbeitsmappe | Quelle: Klimawirkungsketten, Zeile 20 (Id E19, Name „Sonnenscheindauer", Typ „Einfluss") | deckungsgleich mit `hazard_names[1]` in `catalog.py` Zeile 319 |
| Sensitivität Grad der Versiegelung (S100) — Wirkstärke auf die Wärmeinsel-Intensität | kein Zahlenwert in der Arbeitsmappe hinterlegt | Abschaetzung noch zu erarbeiten — im Evidenz-Register (`docs/evidenz/register.md`) bislang kein Basiswert zu S100 für Id 62 vorhanden | für den künftigen Bericht #62 zu recherchieren, bevor eine Formel entsteht (§3.9) |
| Sensitivität Begrünung von Städten/Siedlungen (S099) — Mengengerüst/Kühlwirkung | v_neu = 0,60 (Band 0,40–0,90, Stadtgrün); v_geb = 0,30 (Band 0,10–0,60, Dach-/Fassadengrün) | Quelle: `docs/evidenz/register.md`, Register-ID 61-S099-01 (dort für Risiko #61 als Abschaetzung von KAP3 ausgewiesen, §3.9/Vorgabe P2) | S099 wird laut Netzwerkliste (Zeilen 62–63) von den Risiken 61 und 62 gemeinsam genutzt; der für #61 hergeleitete Wert ist ein Ausgangspunkt für #62, nicht unbesehen zu übernehmen — im Bericht #62 gesondert zu prüfen |
| Kopplung an nachgelagerten Kühlenergiebedarf (Id 65, „Bedarf an Kühlenergie") | kein Zahlenwert recherchiert | Abschaetzung noch zu erarbeiten — bislang keine Quelle zu dieser Kopplung recherchiert | Voraussetzung für eine spätere Wirkungsfunktion Stadtklima → Kühlenergiebedarf |
| Bewertungsansatz / Kostensatz für Id 62 | „—" (kein Kostensatz, da 0 €, rein vorgelagert) | Quelle: `KWRA-Monetarisierung.xlsx`, Blatt „Risiken-Monetarisierung", Zeile 67, Spalte „Bewertungsansatz / Kostensatz" | bestätigt die reine Durchleitungsfunktion; jede eigene Bepreisung wäre laut Zeile 67 eine Doppelzählung der Endpunktschäden (Regel R2) |
