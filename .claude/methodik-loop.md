# Gemeinsamer Methodik-Loop (L1–L7)

Verbindlich für `/risiko-auto` (Erstdurchlauf) und `/risiko-fortsetzen` (Wiedereinstieg).
Beide Commands unterscheiden sich **nur** im Einstieg; ab L1 laufen sie identisch.
Maßstab bleibt `docs/AUFGABE_METHODIK_SCHADENSRECHNUNG.md`.

## Grundregel — keine Fragen

**Du stellst dem Nutzer während des gesamten Laufs keine einzige Frage und wartest auf keine
Eingabe** — auch nicht bei Weggabelungen, die Modellstruktur, Kalibrierung oder
Datenbeschaffung betreffen. Jede Weggabelung wird nach W1–W6 entschieden, angewendet und im
**Entscheidungslog** des Berichts dokumentiert (Nr · Frage · angewendete Entscheidung ·
Begründung · Alternative · Auswirkung aufs Ergebnis). Der Nutzer überstimmt nachträglich —
das löst einen Delta-Lauf über `/risiko-fortsetzen` aus (§2.8 Gate 1). Fehlende Daten oder
Zugriffe sind kein Haltegrund: nach §3.1/§3.9 als Ebene „geparkt", als Annahme oder als
bezifferte Näherung dokumentieren und weiterarbeiten — nichts stumm überspringen, nichts
blockieren.

## Entscheidungsregeln W1–W6 (statt Rückfragen)

Diese Regeln ersetzen die Weggabelungen, an denen ein Lauf sonst stehenbliebe. Jede
angewendete Regel wird im Entscheidungslog mit ihrer Nummer zitiert.

- **W1 · Saubere Lösung vor Näherung.** Ist die methodisch richtige Lösung mit bereits
  vorhandenen oder offen/keyless beschaffbaren Daten erreichbar, wird sie umgesetzt — §3.9
  erlaubt „Abgeschätzt" nur, wenn keine Quelle existiert. Erst wenn sie nachweislich nicht
  erreichbar ist: bezifferte Näherung mit Richtung, Bandbreite und Ersetzungspfad.
- **W2 · Risikolokal vor Produktumbau.** Reicht die Lösung in Bausteine, die andere Risiken
  mitnutzen (geteilte Bandfunktionen, Loader, Registry-Konventionen), wird die risikolokale
  Variante gewählt: eigene Ableitung/Funktion für dieses Risiko, geteilte Kette unangetastet.
  Der Umbau der geteilten Kette wird als Alternative im Entscheidungslog benannt, nicht
  ausgeführt.
- **W3 · Datenlücke blockiert nie.** Fehlt eine Zellgröße: Ebene nach §3.1 vollständig
  spezifizieren und anlegen („neu anzulegen") oder — wenn keine offene Quelle existiert — als
  „geparkt (Datenquelle fehlt)" mit Beschaffungs-Watchlist führen, Parameter auf dem
  dokumentierten Neutralwert. Nie ein stiller Default, nie ein Halt.
- **W4 · Ressourcen-Regel schlägt Genauigkeitswunsch.** Neurechnungen und Abgleiche laufen auf
  Bundesland-, Gemeinde-/Gemeindepunkt- oder kommunaler Stichprobenebene; ein nationaler
  100-m-Vollraster-Lauf ist auch dann unzulässig, wenn er die schönere Zahl ergäbe (§3.4).
  Wird die Produktionsgewichtung gebraucht (bevölkerungsgewichtete Exposition), über die
  **Produktfunktionen** lesen, damit Kalibrier- und Produktionspfad nicht auseinanderlaufen.
- **W5 · Bericht ist die Quelle.** Eine Divergenz Bericht ↔ Code wird nie im Code stillgefixt:
  erst Befund, dann Berichtsrevision, dann Code-Nachzug — in dieser Reihenfolge, beides im
  Ledger (Eiserne Regel 5).
- **W6 · Eine Runde, eine Neurechnung.** Alle Befunde einer Runde werden gemeinsam abgearbeitet
  und die betroffenen Kopplungen **einmal** konsolidiert neu gerechnet. Keine Teilstände, keine
  zweite Rechnung für denselben Kopplungsbaum in derselben Runde.
- **W7 · Kein Schließen ohne Prüfausdruck.** Ein Befund wird nur dann auf `geschlossen`
  gesetzt, wenn in der Ledger-Spalte **Prüfausdruck** das Kommando steht, mit dem die
  Umsetzung tatsächlich verifiziert wurde (`grep`, `test`, `python3`, `pytest` — die
  Freigabeliste steht in `backend/scripts/ledger.py`). Die Statusspalte ist damit keine
  Selbstauskunft mehr, sondern eine Ableitung. *Anlass:* In Runde 16 von Risiko 98 waren
  9 von 17 als „übernommen" geführten Befunden nicht umgesetzt; das ist über vier Runden
  unbemerkt geblieben, weil zwischen Behauptung und Status keine Maschine stand.

## L1 · Revision (Bericht ist die Quelle)

Alle offenen A- und B-Befunde beheben, C-Befunde gleich mit. Betroffene Kopplungen nach W6
**einmal konsolidiert** neu rechnen (§3.9). Rechenläufe gehören in reproduzierbare
Anlagen-Skripte mit gepinnten Daten (`backend/scripts/kalibrierung/`), nicht in
Einmal-Rechnungen; Ergebnis-CSV/MD als Anlage des Berichts verlinken. Ledger je Befund über
`backend/scripts/ledger.py` pflegen — Statusspalte **und** Prüfausdruck nach W7; der Abgleich
läuft über die Befundnummer, nie über die Zeilenposition. Ändert sich ein Modellwert,
ziehen Zeichentabelle, Parameter-Blöcke (Kap. 7), Beispiel-Blöcke, Kap.-4-Sanity-Bänder und
das Entscheidungslog **in derselben Revision** mit.

*Im Erstdurchlauf ist L1 in der ersten Iteration leer — es gibt noch keine Befunde.*

## L2 · Code-Nachzug (Eiserne Regel 5)

**Nur wenn das Risiko bereits ganz oder teilweise integriert ist** — im Erstdurchlauf vor der
Integration entfällt der Schritt, in jedem Delta-/Wiedereinstiegslauf greift er. Der Bericht
führt, der Code folgt, nie umgekehrt:

- Registry-Parameter auf die neuen Werte (Herleitungswerte, nicht gerundete Anzeigen).
- Schicht-B-Funktion an geänderte Formeln, Wirkungsorte und Bandzuordnungen anpassen.
- Neue oder geänderte Ebenen nach §3.1 anlegen bzw. als „geparkt" mit Neutralwert führen.
- Golden-Tests auf den neuen Stand; jeder Beispiel-Block des Berichts bleibt ein Test.
- Quellen-Ratchet: neue Quellen mit Vollzitat, URL/DOI und Wayback-Permalink.

Der Nachzug wird im Ledger dokumentiert (was geändert wurde, wegen welchem Befund) — nicht
still. W4 gilt auch hier.

## L3 · Lints und Tests

Deterministische Checks laufen lassen (`backend/scripts/lint_methodik.py`, falls vorhanden;
sonst selbst: Zeichentabellen-Herkunft, Parameter-Block-Vollständigkeit, Quellen mit
DOI/URL + Archiv, Knoten-/Kanten-Abgleich per openpyxl gegen beide xlsx, Ausführung der
` ```python test: ` -Blöcke, Preisstand-Einheitlichkeit, Reproduktion der Anlagen-Skripte).
Danach die **gesamte** Testsuite, sofern das Risiko integriert ist. Rot wird sofort behoben,
bevor der Review startet.

**Ledger-Gate (W7):** `python3 backend/scripts/ledger.py <nr> --pruefe` muss grün sein, bevor
L4 startet — jeder als geschlossen geführte Befund trägt dann einen Prüfausdruck, der beim
Lauf tatsächlich durchlief. Ist er rot, ist die Runde nicht fertig: entweder den Prüfausdruck
nachtragen oder den Befund wieder auf `offen` setzen. `--selbsttest` prüft die Statuslogik
selbst mit.

## L4 · Unabhängiger Review

Delegiere an den Subagenten **methodik-reviewer** (frischer Kontext = unabhängige Prüfung).
Übergib: Risikonummer, Berichtspfad, Ledgerpfad, Rundennummer, höchste bereits vergebene
Befundnummer — und ausdrücklich den **Prüfumfang**:

- **volle Prüfung** (alle 14 Leitfragen), wenn in dieser Runde Kalibrierung oder
  Modellstruktur geändert wurden (§6) — im Erstdurchlauf immer, im Wiedereinstieg der Regelfall;
- sonst Diff-Runde: geänderte Abschnitte, Regression der geschlossenen Befunde, offene Befunde.

Für die Umsetzungskontrolle bekommt der Reviewer `ledger.py --pruefe` an die Hand: Er führt es
aus und prüft **stichprobenhaft, ob die Prüfausdrücke das Richtige messen** — ein Ausdruck, der
grün wird, ohne die Umsetzung zu belegen, ist selbst ein Befund. Das ist wirksamer, als
Nachweisprosa zu lesen, und schließt genau die Lücke aus Runde 16.

Warte auf die Verdikt-Zeile.

## L5 · Loop

Zurück zu L1. **Maximal 4 Review-Runden.** Meldet der Reviewer eine Null-Runde (keine neuen
A-/B-Befunde) → L6. Nach 4 Runden ohne Null-Runde → L6 trotzdem ausführen (der Nutzer soll
auch einen unfertigen Stand lesen können), Restpunkte in den Statusbericht.

## L6 · Export (PDF **und** HTML)

`scripts/export_methodik_pdf.sh <nr>` erzeugt beides: das Lese-PDF neben der Markdown-Quelle
**und** die Wirkungsmechanismus-Vorschau `docs/methodik/<slug>_wirkungsmechanismus.html`.
Fehlerbehandlung und Layout-Regeln wie in `.claude/commands/export-pdf.md` — die
Markdown-Quelle bleibt unangetastet, Darstellungs-Fixes nur in `scripts/methodik_report.css`
oder einer Scratchpad-Kopie. **Hat der Lauf das Modell geändert, den Graph-Builder in
`scripts/wirkungsmechanismus_preview.py` mitziehen**, sonst zeigt die Vorschau ein veraltetes
Ziel-Modell. Nach dem Export eine Stichprobe rendern (`pdftoppm -png -r 60`) und auf Überläufe
sichten, bevor Vollzug gemeldet wird. Beide Pfade melden.

## L7 · Statusbericht (das Einzige, was der Nutzer liest — kompakt halten)

1. **Status:** ABNAHMEREIF / NICHT ABNAHMEREIF / INTEGRATION KANN WEITERLAUFEN (ein Satz warum).
2. **Anlass und was daraus wurde** (nur beim Wiedereinstieg): der auslösende Punkt in einer
   Zeile, mit Befundnummer.
3. **📄 PDF** und **🔗 HTML:** die beiden erzeugten Pfade (dort stehen alle Details mit
   Formelsatz bzw. das Wirkungsdiagramm).
4. **Die wichtigsten getroffenen Entscheidungen** (max. 5) aus dem Entscheidungslog — je eine
   Zeile: was entschieden, warum, was die Alternative gewesen wäre.
5. **Kernzahlen:** Bundessumme vs. Sanity-Band, Validierungsergebnis, Testlage (n grün / n rot),
   Review-Runden und Befundzahlen, Code-Nachzug ja/nein.
6. **Nächste Schritte:** „Integrieren bzw. Integration fortsetzen: `/integriere-risiko <nr>`.
   Überstimmen: ‚Entscheidung Nr. X ändern auf …' — dann rechne ich die betroffenen Teile neu,
   lasse erneut reviewen und exportiere PDF und HTML neu (`/risiko-fortsetzen <nr>`)."

Keine Frage am Ende, kein offener Punkt ohne Empfehlung.
