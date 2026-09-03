---
description: Wiedereinstieg in den Methodik-Loop ohne Nutzer-Input — wenn bei der Integration, im Betrieb oder durch eine Überstimmung methodische Unklarheiten, offene Punkte oder Fehler auftauchen. Triage, Revision, Code-Nachzug, Review-Loop bis Null-Runde, PDF-/HTML-Export, Statusbericht.
argument-hint: <risiko-nr> [Anlass in einem Satz]
---

Risiko-Nummer und Anlass: $ARGUMENTS

Dieser Command ist der **Wiedereinstieg**: Bericht, Ledger und in der Regel schon Code
existieren. Er unterscheidet sich von `/risiko-auto` nur darin, dass der Einstiegspunkt aus
dem Ist-Stand bestimmt wird statt aus einem Erstaufschlag.

**Grundregel, Entscheidungsregeln W1–W6 und der gesamte Ablauf ab der Revision stehen in
@.claude/methodik-loop.md** — diese Datei ist verbindlich und wird hier nicht wiederholt.
Kern: keine einzige Rückfrage an den Nutzer, auch nicht bei Weggabelungen zu Modellstruktur,
Kalibrierung oder Datenbeschaffung; entschieden wird nach W1–W6, dokumentiert im
Entscheidungslog.

## Schritt A — Triage (nur in diesem Command)

Lies und protokolliere in einem kurzen Arbeitsvermerk:

1. **Bericht** `docs/methodik/<nr>_*.md`: Revisionsstand, Datum, Umsetzungsgrundlage.
2. **Ledger** `reviews/BEFUNDE_<nr>.md`: offene Befunde je Kategorie, letzte Rundennummer,
   höchste vergebene Befundnummer, letztes Konvergenz-Verdikt.
3. **Integrationsstand:** Registry-Parameter, Schicht-B-Funktion, Ebenen, Golden-Tests des
   Risikos — vorhanden? Testsuite grün? (Tests ausführen, nicht vermuten.)
4. **Anlass** aus `$ARGUMENTS` bzw. aus dem, was die Integration gemeldet hat.

Einstiegspunkt:

- **Offene A-/B-/C-Befunde vorhanden** → Schritt C (Loop ab L1).
- **Keine offenen Befunde, aber ein gemeldeter Anlass** → Schritt B, dann Schritt C.
- **Keine offenen Befunde, kein Anlass** → Schritt C, aber Einstieg bei **L3** — der Loop
  bestätigt den Stand oder findet Neues.

## Schritt B — Anlass ins Ledger (nur in diesem Command)

Was Integration, Betrieb oder Nutzer gemeldet hat, wird **zuerst Befund**, nicht sofort Fix:
neue Zeile in `reviews/BEFUNDE_<nr>.md` (fortlaufende Nummer, Stelle · Art · Begründung ·
Vorschlag · Kategorie). Eine Divergenz Bericht ↔ Code ist Kategorie A, solange sie nicht
geklärt ist (W5). Erst danach revidieren.

## Schritt C — Gemeinsamer Loop

Weiter mit **L1–L7** aus @.claude/methodik-loop.md. Für den Wiedereinstieg gilt:

- **L2** (Code-Nachzug) greift, sobald das Risiko integriert ist — beim Wiedereinstieg der
  Regelfall.
- **L4** läuft als volle Prüfung, sobald Kalibrierung oder Modellstruktur berührt wurden;
  das ist beim Wiedereinstieg der Regelfall.
- **L7** Punkt 2 (Anlass und was daraus wurde) ist hier Pflicht.
