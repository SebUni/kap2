---
description: Voller Durchlauf ohne Nutzer-Input — Erstaufschlag inkl. Recherche, automatische Entscheidungen (Entscheidungslog), unabhängiger Review durch frischen Subagenten, Revision, Loop bis Null-Runde. Wartet nirgends auf Eingaben; endet mit einem Statusbericht.
argument-hint: <risiko-nr>
---

Risiko-Nummer: $ARGUMENTS

**Grundregel dieses Commands: Du stellst dem Nutzer während des gesamten Laufs keine einzige
Frage und wartest auf keine Eingabe.** Jede Entscheidung fällt nach den Standardregeln
(§2.8 der Aufgabe); Ermessensfälle entscheidest du mit deiner Empfehlung und protokollierst
sie. Bei fehlenden Daten oder Zugriffen: als Annahme/Lücke nach §3.8/§3.9 dokumentieren und
weiterarbeiten — nichts stumm überspringen, nichts blockieren.

## Schritt 1 — Entwurf

Führe die vollständige Pipeline aus @.claude/commands/neu-risiko.md aus, mit **einer**
Änderung: Phase 6 ist kein Wartepunkt. Jede ⚠️-Entscheidung wird sofort mit deiner Empfehlung
angewendet und im Bericht unter `## Entscheidungslog` dokumentiert
(Nr · Frage · angewendete Entscheidung · Begründung · Alternative · Auswirkung aufs Ergebnis).

## Schritt 2 — Lints

Deterministische Checks laufen lassen (Skript, falls vorhanden; sonst selbst) und Rot sofort
beheben.

## Schritt 3 — Unabhängiger Review

Delegiere den Review an den Subagenten **methodik-reviewer** (eigener, frischer Kontext =
unabhängige Prüfung). Übergib ihm: Risikonummer, Berichtspfad, Ledgerpfad, Rundennummer.
Warte auf sein Verdikt.

## Schritt 4 — Revision

Alle neuen A- und B-Befunde in dieser Hauptsession beheben (C-Befunde gleich mit, wenn
trivial); betroffene Kopplungen neu rechnen (§3.9); Ledger-Status je Befund pflegen.

## Schritt 5 — Loop

Zurück zu Schritt 3. **Maximal 4 Review-Runden.** Meldet der Reviewer eine Null-Runde
(keine neuen A/B-Befunde) → Schritt 6. Nach 4 Runden ohne Null-Runde → Schritt 6 trotzdem
ausführen (der Nutzer soll auch einen unfertigen Stand lesen können), Restpunkte in den
Statusbericht.

## Schritt 6 — PDF-Export

Erzeuge das Lese-PDF aus der Markdown-Quelle: `scripts/export_methodik_pdf.sh $ARGUMENTS`
(Fallback: pandoc direkt mit XeLaTeX und den Optionen aus dem Skript; Fehlerbehandlung wie in
@.claude/commands/export-pdf.md — Darstellungs-Fixes nur in einer /tmp-Kopie, nie in der
Quelle). Das PDF liegt neben der Markdown-Datei. Bei jedem späteren Delta-Lauf
(Überstimmung einer Entscheidung) wird das PDF am Ende automatisch neu erzeugt.

## Schritt 7 — Statusbericht (das Einzige, was der Nutzer liest — kompakt halten)

1. **Status:** ABNAHMEREIF oder NICHT ABNAHMEREIF (ein Satz warum).
2. **📄 PDF:** Pfad zum erzeugten Lese-PDF (dort stehen alle Details mit Formelsatz).
3. **Die 5 wichtigsten getroffenen Entscheidungen** aus dem Entscheidungslog — je eine Zeile:
   was entschieden, warum, was die Alternative gewesen wäre.
4. **Kernzahlen:** Bundessumme vs. Sanity-Band, Validierungsergebnis, Review-Runden und
   Befundzahlen.
5. **Nächste Schritte:** „Nichts weiter nötig. Integrieren: `/integriere-risiko $ARGUMENTS`.
   Überstimmen: ‚Entscheidung Nr. X ändern auf …' — dann rechne ich die betroffenen Teile neu,
   lasse erneut reviewen und erzeuge das PDF neu."

Keine Frage am Ende, kein offener Punkt ohne Empfehlung.
