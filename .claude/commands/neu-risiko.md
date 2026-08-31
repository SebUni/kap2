---
description: Instanziiert das Methodik-Template für eine KWRA-Klimawirkung (§2/§4 der Aufgabe) — Knoten, Kanten und Konto automatisch aus den Arbeitsmappen
argument-hint: <risiko-nr>
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

Risiko-Nummer: $ARGUMENTS

Du legst den Erstaufschlag eines Methodik-Berichts an. Verbindliche Instruktionsquelle ist
@docs/AUFGABE_METHODIK_SCHADENSRECHNUNG.md — lies sie zuerst vollständig, insbesondere §2
(Aufgabe je Klimawirkung), §3 (Anforderungskatalog) und §4 (Berichtsstruktur-Template).

## Schritte

1. **Arbeitsmappen einlesen** (per Python/openpyxl, `read_only=True`):
   - `docs/Schadensbaum/KWRA-Schadensbaum_X_UBA-klimawirkungsketten.xlsx`
     (Sheets „Klimawirkungsketten", „Schadensbaum-Netzwerkliste")
   - `docs/Schadensbaum/KWRA-Monetarisierung.xlsx`
     (Sheets „Risiken-Monetarisierung", „Schadenskonten-System", „Rechenregeln", „Abgleich-Protokoll")
   Falls die Pfade abweichen: per Glob suchen, gefundenen Pfad melden.

2. **Rollen-Check:** Lies in der Netzwerkliste die Zeile der Risiko-Nr. Ist die Rolle
   „Treiber (0 €)", „Rein vorgelagert (0 €)" oder „Zustandsgröße (0 €)": **abbrechen** und
   erklären, dass dieses Risiko per Regel R2/R3 keine eigene Schicht-B-Methodik bekommt —
   nenne stattdessen die Endpunkte (Output-IDs), an denen es wirkt.

3. **Knoten und Kanten extrahieren:** Aus der Wirkungsketten-Zeile des zugehörigen W-Knotens:
   alle E-/S-/R-/W-Eingänge mit IDs und Klartextnamen (bei vorgelagerten W-Knoten auch deren
   Eingänge eine Ebene tief). Aus Netzwerkliste + Abgleich-Protokoll: Input-/Output-Kanten mit
   Protokoll-Punktnummern. Aus der Monetarisierung: Ebene (A/B), Konto, Bewertungsbausteine,
   anzuwendende R-Regeln, „Nicht enthalten"-Abgrenzungen, Handlungserfordernis.

4. **Familie bestimmen:** Prüfe `docs/methodik/` auf bestehende Berichte desselben Kontos /
   Mustertyps (z. B. K1-Gesundheit bottom-up; K3/K4-Ereignisschäden; K6-Ertrag; K8-Vorsorge).
   Das Verzeichnis existiert ggf. noch nicht; der bestehende K1-Gesundheit-Prototyp M0
   (#95/#96/#98) liegt als HTML unter `docs/render/METHODIK_M0_GESUNDHEIT.html`
   (Gegenprüfung: `docs/METHODIK_M0_GESUNDHEIT_Gegenpruefung_Rev5.md`).
   Gibt es einen abgenommenen Familien-Prototyp → dieses Risiko erbt dessen Struktur, der
   Drei-Ansätze-Vergleich entfällt (§2.6). Gibt es keinen → Abschnitt 9 (Ansatz-Vergleich)
   mit anlegen und das im Ergebnis deutlich sagen.

5. **Bericht anlegen:** `docs/methodik/<nr>_<slug>.md` nach dem §4-Template, vorbefüllt:
   - **Kap. 1 Wirkungskette & Knoten-Bilanz:** eine Bilanz-Zeile je Knoten
     (Spalte „rechnet in": vorerst `offen`); Weitergaben **zweispaltig**
     (Output-Kanten laut Abgleich-Protokoll mit Punkt-Nr. | Konto-Ausschlüsse laut
     Konten-Definition) — inklusive Partitionsregel-Zitaten, wo zwei Buchungsobjekte
     dasselbe Konto teilen.
   - **Kap. 2 Evidenz-Register:** Skelett mit einer Zeile je Knoten (Register-ID
     `<nr>-<Knoten>-01`, Entscheidung `offen`). Prüfe `docs/evidenz/register.md` auf
     wiederverwendbare Zeilen (Alter, Pflege, Isolation, Außenberufe …) und referenziere sie;
     existiert die Datei noch nicht, lege sie mit diesem Bericht an.
   - **Kap. 3–8:** leere Abschnitte mit den Pflichtinhalten als Kommentar
     (inkl. Parameter-Block-Beispiel und Beispiel-Test-Block aus §4). Zwei
     Pflichtregeln als Kommentar in Kap. 3 bzw. Kap. 4 vermerken:
     (a) **Datenebenen-Anlagepflicht (§3.1):** jede benötigte Zellgröße, die das
     Produkt nicht führt, wird als Ebene vollständig spezifiziert („neu anzulegen";
     ohne offene Quelle: „geparkt" + Watchlist) — kein dauerhafter, unspezifizierter
     Neutral-Fallback; (b) **Ressourcen-Regel (§3.4):** Kalibrierung/Validierung/
     Abgleiche nie über nationale 100-m-Vollraster-Läufe planen — zulässig sind
     Bundesland-, Gemeindepunkt- und kommunale Stichproben-Ebene;
     (c) **Geschlossene Betrachtungsebene (§3.2):** Zentrierungs-/Referenzmittel
     entweder amtlich publiziert oder aus der Betrachtungsebene selbst (Kommune:
     eigene Zellen, im Baseline-Lauf festgehalten) — nie aus einer Aggregation
     über eine höhere Ebene; ohne zulässige Referenz bleibt der Modifikator neutral.
6. **Ledger anlegen:** `reviews/BEFUNDE_<nr>.md` mit leerer Befund-Tabelle
   (Befund · Kategorie · Status · Umsetzungsnachweis · Begründung bei Abweichung).

## Ergebnis

Kurzer Abschlussbericht: angelegte Dateien, gefundene Knoten/Kanten/Konto (mit Quelle Sheet+Zeile),
gewählte bzw. fehlende Familie — und eine Liste der **offenen menschlichen Entscheidungen**
(Register-Entscheidungen, native Ergebnisgröße, ggf. Familien-Neugründung). Erfinde nichts:
Was die Arbeitsmappen nicht hergeben, bleibt als `offen` markiert.
