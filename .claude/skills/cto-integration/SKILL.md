---
name: cto-integration
description: Der cto überführt eine abgenommene Methodik in die Plattform — Registry-Parameter, Schicht-B-Funktion, Tests aus Beispielen und Sanity-Ankern, Kartenebenen (früher /integriere-risiko)
argument-hint: <risiko-nr>
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

Risiko-Nummer: $ARGUMENTS

Du integrierst eine **abgenommene** Methodik in die Plattform. Grundlage:
`docs/methodik/<nr>_*.md` + @docs/AUFGABE_METHODIK_SCHADENSRECHNUNG.md (§4, §7).

## Rolle und Auftrag

Ausführende Rolle ist der **`cto`** (Aufsichtsrat, 24.09.2026: die Methodik entsteht beim CMO und seinen Rollen, die
Integration übernimmt der CTO). Den Auftrag gibt der `cmo` nach der Abnahme des Managers weiter. Wer welchen Schritt
verantwortet, steht im Abschnitt „Rollen im Loop“ in `.claude/methodik-loop.md`.

## 0 · Vorbedingung: Abnahme

Lies `reviews/BEFUNDE_<nr>.md`. Sind offene A-Befunde vorhanden, fehlt das dokumentierte
Konvergenz-Verdikt (Null-Runde) oder fehlt die fachliche Abnahme des Managers (Zeile
`MANAGER-REVIEW: ABGENOMMEN`, Skill `methodik_manager-abnahme`): **abbrechen** und die Blocker auflisten —
in der Rollenkette als `blockiert` an den Auftraggeber (`cmo`), im Einzelsitzungs-Weg des Aufsichtsrats über
`/aufsichtsrat-risiko-fortsetzen <nr> <Blocker in einem Satz>`. Keine Integration vor der Abnahme; das gilt für jeden
Bericht, einen Altbestand ohne Abnahme gibt es nicht.

## 1 · Muster der Codebasis lernen (nichts neu erfinden)

Suche die bestehende Implementierung eines bereits integrierten Risikos (z. B. Hitzemortalität)
und die vorhandenen Konventionen: Registry-Format, `sources.py`, Ratchet-Test, Ebenen-Definition,
Testaufbau, Batch-/Kalibrier-Skripte. Folge exakt diesen Mustern; weiche nur ab, wenn der
Bericht es verlangt, und dokumentiere die Abweichung.

## 2 · Registry und Quellen

- Parameter-Blöcke des Berichts (Kap. 7) extrahieren → Registry-Parameter anlegen: editierbar,
  mit Quelle, Band, Bandzuordnung, Endpunkt; Kostensätze mit Preisstand.
- Quellen in die Quellendatenbank übernehmen: Vollzitat, URL/DOI, **Wayback-Permalink erzeugen**
  (Ratchet-Anforderung). Ratchet-Test muss grün sein.

## 3 · Schicht-B-Funktion

Die Formeln aus Kap. 3 implementieren — ausschließlich gegen Registry-Parameter (keine
hartkodierten Zahlen), inklusive Aggregation Zelle → Kommune, nativer Ergebnisgröße und
Teil-Ausweisen. Schicht-A-Index getrennt (nie Screening-Normierung auf €-Pfaden). Als „neu
anzulegen" gekennzeichnete Ebenen (Kartenebenen, Struktur-Ebenen, **Modifikator-Zellgrößen**)
**verpflichtend anlegen** (§3.1-Anlagepflicht) — ein Neutral-Fallback ist nur für Ebenen
zulässig, die der Bericht ausdrücklich als „geparkt (Datenquelle fehlt)" mit
Beschaffungs-Watchlist führt; das Verifikationsergebnis kommt als ein Satz in den Bericht.
Ergebnis-Layer als Raten (je 1.000 EW / je ha) gemäß §3.6. **Ressourcen-Regel (§3.4):**
kein Integrationsschritt darf einen nationalen 100-m-Vollraster-Lauf erfordern oder
einplanen; Abgleiche laufen auf Bundesland-/Gemeindepunkt-/Stichproben-Ebene.
**Geschlossene Betrachtungsebene (§3.2):** Referenz-/Zentrierungsmittel kommen
entweder aus amtlicher Statistik oder werden im Lauf aus der Betrachtungsebene
selbst gebildet (Kommune: über ihre eigenen Zellen, im Baseline-Lauf
festgehalten) — niemals aus einer Aggregation über eine höhere Ebene.

## 4 · Tests aus dem Bericht generieren

- **Golden-Tests:** jeder Beispiel-Block des Berichts wird ein Test (Eingaben → erwartetes
  Ergebnis mit Toleranz). Bericht und Code dürfen nicht divergieren können.
- **Sanity-Band-Test:** Bundessumme des Modells ∈ [Untergrenze, Obergrenze] aus Kap. 4.
- **Validierungs-Test:** Struktur-/Verteilungsprüfung (z. B. Altersanteile) mit der im Bericht
  fixierten Toleranz.
- Kalibrier-Pipeline als reproduzierbares Skript mit gepinnten Daten (kein Einmal-Lauf).

## 5 · Abschluss

Gesamte Testsuite ausführen. **Bei jeder Divergenz Bericht ↔ Code: nicht still im Code fixen** —
Befund ins Ledger (Kategorie A, „Integration blockiert durch …") und melden; die Methodik ist
die Wahrheit, bis ein Review sie ändert. Abschlussbericht: angelegte Parameter, Funktionen,
Ebenen, Tests (grün/rot), offene Punkte.

Bleibt dabei ein methodischer Punkt offen — Divergenz, Unklarheit, Fehler im Bericht —, geht er als Befund an den
`cmo` zurück (neue Runde bei Manager und Consultant; im Einzelsitzungs-Weg `/aufsichtsrat-risiko-fortsetzen <nr>
<Anlass>`). Danach wird erneut integriert.
