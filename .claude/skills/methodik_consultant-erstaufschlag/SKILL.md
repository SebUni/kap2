---
name: methodik_consultant-erstaufschlag
description: Erstaufschlag eines Methodik-Berichts durch den methodik_consultant — instanziiert das Template (§2/§4 der Aufgabe) mit Rechenkette, Knoten, Kanten und Konto automatisch aus den Arbeitsmappen (früher /neu-risiko)
argument-hint: <risiko-nr>
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

Risiko-Nummer: $ARGUMENTS

Du legst den Erstaufschlag eines Methodik-Berichts an. Verbindliche Instruktionsquelle ist
@docs/AUFGABE_METHODIK_SCHADENSRECHNUNG.md — lies sie zuerst vollständig, insbesondere §2
(Aufgabe je Klimawirkung), §3 (Anforderungskatalog) und §4 (Berichtsstruktur-Template).

## Rolle und Auftrag

Ausführende Rolle ist der `methodik_consultant` (der Name dieses Skills sagt es: Rolle und Zweck); Auftraggeber ist der
`methodik_manager`, der das Risiko zugeteilt hat. Die Liste der offenen Entscheidungen aus dem Ergebnis geht an den
`methodik_manager`, nicht an einen Nutzer. Geschrieben wird nach dem Stil-Skill `kap3-stil` (Zahlen, Einheiten, Begriffe).
Wer welchen Schritt verantwortet, steht im Abschnitt „Rollen im Loop“ in
`.claude/methodik-loop.md`.

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
   Der K1-Gesundheit-Prototyp M0 liegt als Markdown unter `docs/methodik/95_…`, `96_…`, `98_…`.
   Gibt es einen abgenommenen Familien-Prototyp → dieses Risiko erbt dessen Struktur. Ein
   Ansatz-Kapitel gibt es nicht (Aufgabe §2.6, Fortschreibung 7): Am Ende steht **eine** Methodik;
   die Methodenwahl steht im Entscheidungslog, verworfene Ansätze mit je einem Satz Grund.
   Gibt es keinen Prototyp, sagt das Ergebnis es deutlich — die Wahl wird dann ausführlicher
   im Entscheidungslog begründet, nicht in einem eigenen Kapitel.

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
   - **Kap. 3 beginnt mit `### 3.0 Rechenkette`** (Aufgabe §4, §8 E1): Tabelle
     `| Ebene | Rechenschritt | Wert (Beispielkommune <Name>) | Quelle |` von der amtlichen Quelle
     (etwa Zensus-Einwohner) bis zum Euro-Betrag, je Ebene „Zahl aus Quelle × Faktor = Ergebnis“,
     höchstens zehn Ebenen (mehr nur mit `**Mehr als zehn Ebenen:** <Begründung>`), letzte Ebene der
     Euro-Betrag; darunter ein Beispiel-Block ```` ```python test: rechenkette_<nr> ```` , der die Kette
     nachrechnet. Solange Werte fehlen, steht die Kette mit `offen` in der Wertspalte da.
   - **Kap. 3–8:** leere Abschnitte mit den Pflichtinhalten als Kommentar
     (inkl. Parameter-Block-Beispiel und Beispiel-Test-Block aus §4). Ein Kapitel 9 gibt es nicht. Zwei
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
gewählte bzw. fehlende Familie — und eine Liste der **offenen Entscheidungen** für den `methodik_manager`
(Register-Entscheidungen, native Ergebnisgröße, Beispielkommune der Rechenkette, ggf. Familien-Neugründung).
Erfinde nichts: Was die Arbeitsmappen nicht hergeben, bleibt als `offen` markiert.
