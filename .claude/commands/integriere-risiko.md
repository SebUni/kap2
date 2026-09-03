---
description: Überführt eine abgenommene Methodik in die Plattform — Registry-Parameter, Schicht-B-Funktion, Tests aus Beispielen und Sanity-Ankern, Kartenebenen
argument-hint: <risiko-nr>
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

Risiko-Nummer: $ARGUMENTS

Du integrierst eine **abgenommene** Methodik in die Plattform. Grundlage:
`docs/methodik/<nr>_*.md` + @docs/AUFGABE_METHODIK_SCHADENSRECHNUNG.md (§4, §7).
Sonderfall M0 (Altbestand): Bericht ist `docs/render/METHODIK_M0_GESUNDHEIT.html`.

## 0 · Vorbedingung: Abnahme

Lies `reviews/BEFUNDE_<nr>.md` (für M0: `docs/METHODIK_M0_GESUNDHEIT_Gegenpruefung_Rev5.md`).
Sind offene A-Befunde vorhanden oder fehlt das dokumentierte
Konvergenz-Verdikt (Null-Runde): **abbrechen** und die Blocker auflisten. Keine Integration
vor der Abnahme. Wiedereinstieg in den Loop: `/risiko-fortsetzen <nr> <Blocker in einem Satz>`
— arbeitet die Blocker ohne Rückfragen ab und exportiert PDF und HTML neu.

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

Bleibt dabei ein methodischer Punkt offen — Divergenz, Unklarheit, Fehler im Bericht —, ist der
nächste Schritt `/risiko-fortsetzen <nr> <Anlass in einem Satz>`: derselbe Review-/Revisions-Loop
ab dem Ist-Stand, ohne Nutzer-Input, mit Code-Nachzug und neuem PDF-/HTML-Export. Danach
`/integriere-risiko <nr>` erneut.
