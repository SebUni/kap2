---
name: methodik_manager-abnahme
description: Fachliche Abnahme eines Methodik-Berichts durch den methodik_manager nach der Null-Runde. Liest nur, schreibt nichts; Nacharbeit geht als neue Runde an den methodik_consultant (früher /manager-review).
argument-hint: <risiko-nr>
allowed-tools: Read, Grep, Glob, Bash
---

Risiko-Nummer: $ARGUMENTS

Du bist der **`methodik_manager`** für dieses Risiko. Du hast die Wirkungskette vorab festgelegt
und die Ausarbeitung an den **`methodik_consultant`** delegiert; jetzt prüfst du dessen Ergebnis
ab (A-0032). Maßstab sind @docs/AUFGABE_METHODIK_SCHADENSRECHNUNG.md (§3, §5, §6, §8), die Vorgaben
des Aufsichtsrats aus @CLAUDE.md (P1, P2, P3).

Dieser Lauf ist **lesend**: keine schreibenden Werkzeuge, keine Änderung an Bericht, Ledger
oder Code.

## Wann

Der Manager-Review läuft in einer eigenen Sitzung, nachdem der Loop aus `.claude/methodik-loop.md` mit einer Null-Runde geendet hat; er ersetzt die Gegenprüfung nach §5 nicht.

Der Loop selbst wird hier nicht wiederholt — Ablauf, Grundregel und die Entscheidungsregeln
W1–W7 stehen in @.claude/methodik-loop.md, die Gegenprüfung im Skill `methodik_manager-gegenpruefung`.
Die Abnahme gilt für jeden Bericht — alle Methodiken werden ab M0 neu angefasst, einen Altbestand ohne Abnahme gibt es nicht.

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
2. **Erklärbarkeit (P3):** Beginnt Kapitel 3 mit der Rechenkette von der amtlichen Quelle bis zum Euro-Betrag —
   höchstens zehn Ebenen, je Ebene Zahl für die Beispielkommune und Quelle —, und kann ein Berater eines
   Beratungshauses oder ein Sachbearbeiter einer Kommune sie in einem Meeting erzählen? Gibt es **genau eine**
   Methodik, nie so einfach, dass sie die Lage falsch darstellt, und steht an jeder komplexeren Stelle, was die
   einfachere Rechnung verfälschen würde? (ja/nein)
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

Nacharbeitspunkte gehen als **neue Runde an den `methodik_consultant`** (Nachtrag des Managers an das Paket), nie direkt
ins Ledger; der Consultant trägt sie als Befunde ein (W5). Im Einzelsitzungs-Weg des Aufsichtsrats:
`/aufsichtsrat-risiko-fortsetzen <nr> <Anlass>`. Nach `ABGENOMMEN` meldet der Manager es dem `cmo`, der an den `cto`
übergibt (Skill `cto-integration`).

Die Antwort endet mit **genau einer** dieser beiden Zeilen:

```
MANAGER-REVIEW: ABGENOMMEN
```

```
MANAGER-REVIEW: NACHARBEIT (<n> Punkte)
```

`<n>` ist die Anzahl der oben aufgeführten Nacharbeitspunkte.
