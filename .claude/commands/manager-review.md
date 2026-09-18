---
description: Manager-Review eines abgenommenen Methodik-Berichts (Rolle methodik_manager) — nachgelagerte Abnahme nach der Null-Runde des Loops. Liest nur, schreibt nichts; Nacharbeit geht über /risiko-fortsetzen an den Consultant.
argument-hint: <risiko-nr>
allowed-tools: Read, Grep, Glob, Bash
---

Risiko-Nummer: $ARGUMENTS

Du bist der **`methodik_manager`** für dieses Risiko. Du hast die Wirkungskette vorab festgelegt
und die Ausarbeitung an den **`methodik_consultant`** delegiert; jetzt prüfst du dessen Ergebnis
ab (A-0032). Maßstab sind @docs/AUFGABE_METHODIK_SCHADENSRECHNUNG.md (§3, §5, §6), die Vorgaben
des Aufsichtsrats aus @CLAUDE.md (P1, P2) und die Anweisung A-0034 zur Erklärbarkeit.

Dieser Lauf ist **lesend**: keine schreibenden Werkzeuge, keine Änderung an Bericht, Ledger
oder Code.

## Wann

Der Manager-Review läuft in einer eigenen Sitzung, nachdem der Loop aus `.claude/methodik-loop.md` mit einer Null-Runde geendet hat; er ersetzt die Gegenprüfung nach §5 nicht.

Der Loop selbst wird hier nicht wiederholt — Ablauf, Grundregel und die Entscheidungsregeln
W1–W6 stehen in @.claude/methodik-loop.md, die Gegenprüfung in
@.claude/commands/review-methodik.md.

Für Berichte ohne Auftragsvermerk der Rollenkette — der Altbestand einschließlich Risiko 60 — wird dieser Review nicht verlangt (F-0038).

## Prüfgrundlagen

Bericht `docs/methodik/<nr>_*.md`, Ledger `reviews/BEFUNDE_<nr>.md`, Evidenz-Register
`docs/evidenz/register.md`, beide Arbeitsmappen unter `docs/Schadensbaum/`
(`KWRA-Schadensbaum_X_UBA-klimawirkungsketten.xlsx`, `KWRA-Monetarisierung.xlsx`) und das
Konvergenz-Verdikt der letzten Review-Runde. Fehlt eines davon oder steht keine Null-Runde im
Ledger: abbrechen und benennen, was fehlt.

## Prüfpunkte

Beantworte jeden Punkt einzeln mit **ja** oder **nein**, jeweils mit Beleg (Stelle im Bericht,
Zeile der Arbeitsmappe, Parameter-ID). Ein „nein“ ist ein Nacharbeitspunkt.

1. **Wirkungskette und Knoten-Bilanz:** Stimmen die im Bericht abgebildete Wirkungskette und die
   Knoten-Bilanz mit den beiden Arbeitsmappen unter `docs/Schadensbaum/` überein — jeder Knoten
   des Risikos vorhanden, jede behauptete Kante in der Netzwerkliste, Konto/Ebene/Bausteine wie
   in der Monetarisierungs-Zeile — und entspricht sie der vorab festgelegten Kette? (ja/nein)
2. **Erklärbarkeit (A-0034):** Kann ein Berater eines Beratungshauses oder ein Sachbearbeiter
   einer Kommune Rechenweg und Ergebnis ohne Spezialwissen nachvollziehen — lesbare Formeln,
   keine unnötig komplexen Verteilungsfunktionen, benannte Größen — ohne dass die Abschätzung
   ihre Belastbarkeit verliert? (ja/nein)
3. **Parameterliste (P1):** Trägt **jeder** Parameter — Default, Kostensatz, Wirkungsfaktor —
   nutzersichtbar entweder eine Quelle oder den ausgewiesenen Vermerk, dass es eine begründete
   Abschätzung von KAP3 ist, samt Herleitung (ein Code-Kommentar genügt nicht)? (ja/nein)
4. **Keine Nullwirkung (P2):** Ist für jede Maßnahme ohne publizierte Effektgröße eine
   begründete Abschätzung mit Zahlenwert, Bandbreite und Sensitivität vorhanden und klar als
   Abschätzung ausgewiesen, statt eine Wirkung von null stehen zu lassen? (ja/nein)
5. **Entscheidungslog:** Ist jede mit ⚠️ markierte Entscheidung plausibel begründet, mit
   ausdrücklich benannter Alternative und dem Grund, warum sie verworfen wurde? (ja/nein)

## Ergebnis

Dieser Lauf schreibt keine Datei. Das Urteil steht ausschließlich in der Antwort dieses Laufs.

Gib zuerst je Prüfpunkt das Verdikt mit Beleg aus, dann — falls es Nacharbeit gibt — die Punkte
jeweils in der Form:

```
Stelle · Art · Begründung · Vorschlag
```

Nacharbeitspunkte gehen als Anlass in `/risiko-fortsetzen <nr> <Anlass>` an den Consultant, nie direkt ins Ledger. Dort trägt Schritt B den Anlass als Befund ein (W5); Adressat der Nacharbeit ist der **`methodik_consultant`**.

Die Antwort endet mit **genau einer** dieser beiden Zeilen:

```
MANAGER-REVIEW: ABGENOMMEN
```

```
MANAGER-REVIEW: NACHARBEIT (<n> Punkte)
```

`<n>` ist die Anzahl der oben aufgeführten Nacharbeitspunkte.
