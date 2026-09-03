---
description: Voller Erstdurchlauf ohne Nutzer-Input — Erstaufschlag inkl. Recherche, automatische Entscheidungen (Entscheidungslog), unabhängiger Review durch frischen Subagenten, Revision, Loop bis Null-Runde, PDF-/HTML-Export. Wartet nirgends auf Eingaben; endet mit einem Statusbericht.
argument-hint: <risiko-nr>
---

Risiko-Nummer: $ARGUMENTS

Dieser Command ist der **Erstdurchlauf**: aus den Arbeitsmappen entsteht ein neuer
Methodik-Bericht, der bis zur Null-Runde gebracht wird. Der Wiedereinstieg in einen bereits
bestehenden Bericht läuft über `/risiko-fortsetzen`.

**Grundregel, Entscheidungsregeln W1–W6 und der gesamte Ablauf ab der Revision stehen in
@.claude/methodik-loop.md** — diese Datei ist verbindlich und wird hier nicht wiederholt.
Kern: keine einzige Rückfrage an den Nutzer, Weggabelungen nach W1–W6 entscheiden und im
Entscheidungslog dokumentieren.

## Schritt A — Entwurf (nur in diesem Command)

Führe die vollständige Pipeline aus @.claude/commands/neu-risiko.md aus, mit **einer**
Änderung: Phase 6 ist kein Wartepunkt. Jede ⚠️-Entscheidung wird sofort mit deiner Empfehlung
angewendet und im Bericht unter `## Entscheidungslog` dokumentiert
(Nr · Frage · angewendete Entscheidung · Begründung · Alternative · Auswirkung aufs Ergebnis).

## Schritt B — Gemeinsamer Loop

Weiter mit **L1–L7** aus @.claude/methodik-loop.md. Für den Erstdurchlauf gilt:

- **L1** ist in der ersten Iteration leer (noch keine Befunde) — direkt zu L3.
- **L2** (Code-Nachzug) entfällt, solange das Risiko noch nicht integriert ist; sobald ein
  Delta-Lauf auf ein integriertes Risiko trifft, greift L2 wie beschrieben.
- **L4** läuft im Erstdurchlauf immer als volle Prüfung.
- **L7** Punkt 2 (Anlass) entfällt.
