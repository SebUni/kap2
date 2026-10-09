---
name: entwickler-ledger-befund
description: Einen Befund im Prüfprotokoll (reviews/BEFUNDE_*.md) nach festem Muster eintragen, schließen oder wiedereröffnen: Kopftabelle, Kopfzahl, Prüfausdruck und Lauf von ledger.py nachziehen, ohne fremde Ausdrücke zu kippen.
---

# Befund im Prüfprotokoll eintragen, schließen oder wiedereröffnen

Aufsichtsrat, 24.09.2026: Wiederkehrende Arbeit wird immer gleich ausgeführt. Diese Ledger-Arbeit kehrt in vielen Serien
wieder (Kopftabelle Ledger 60, Durchsicht der Prüfausdrücke, Befund schließen in Ledger 62, Befund belegen oder
wiedereröffnen in Ledger 60, Läufe von `ledger.py`). Der Skill beschreibt das Vorgehen; Urteile zu einzelnen Befunden
enthält er nicht. Geschrieben wird nach `kap3-stil`. Das Ticket nennt immer Ledger (`reviews/BEFUNDE_<nr>.md`) und
Befundnummern; was dort vom Skill abweicht, geht vor.

## Grundregeln

- Der Ledger ist die Prüfakte, getrennt von der Kundenfassung. Ein Befund gilt nur mit Prüfausdruck als geschlossen (W7);
  `ledger.py` leitet den Status aus dem Ausdruck ab, es glaubt keine Selbstauskunft.
- Abgeglichen wird immer über die **Befundnummer**, nie über Zeilenposition oder Zeilennummer im Bericht.
- Eine Befundnummer wird nie verschoben und nie neu vergeben. Eine neue Nummer ist die höchste vorhandene plus eins —
  über alle Tabellen der Datei gesucht, nicht nur in der Kopftabelle (T-0020: eine verschobene Nummer kippte Ausdrücke).
- Fremde Zeilen bleiben unberührt: Ändere nur die Zeilen der im Ticket genannten Befunde. Kein „Aufräumen“ daneben.
- Geändert wird nur `reviews/BEFUNDE_<nr>.md` (und, wenn das Ticket es verlangt, der Bericht). Prüfe am Ende mit
  `git diff --numstat origin/main...HEAD`, dass genau die erlaubten Dateien erscheinen.

## Schritt 0: Ausgangslage messen, bevor du änderst

1. Die Kopfzahl der Datei: `grep -n '^## Offene Befunde' reviews/BEFUNDE_<nr>.md` (steht als „## Offene Befunde (N)“).
2. Den Lauf **vorher**: `python3 backend/scripts/ledger.py <nr> --pruefe`. Schlusszeilen und die ROT-Liste wörtlich
   notieren (Zähler „belegt geschlossen“, „Prüfausdruck ROT“, „unbelegt geschlossen“). Sie sind der Vergleichsstand.
3. Übersicht der offenen Befunde: `python3 backend/scripts/ledger.py <nr> --status`.
4. Die Zeile des Befunds in der Kopftabelle lesen (Spalten siehe unten) und, falls vorhanden, seine Zeile in der
   Befundtabelle der Review-Runde.

## Aufbau der Kopftabelle

Spalten: `| Nr | Befund (Stelle · Kurzfassung) | Kat. | Status | Umsetzungsnachweis | Prüfausdruck | Begründung bei Abweichung |`
(sieben Zellen, Kopftabelle direkt unter `## Offene Befunde (N)`). Die Tabellen der Review-Runden haben andere Spalten
(`Nr | Kat. | Befund | Prüfausdruck | Status`); `ledger.py` findet beide.

- Status: `offen`, `behoben`, `bewusst offen`, `zurückgestellt`. Wer `behoben` setzt, trägt in derselben Zeile
  Umsetzungsnachweis (Abschnitt „Autor-Revision T-xxxx“ mit Anker) und Prüfausdruck ein.
- Jede Zeile hat genau sieben Zellen. Ein ungeschütztes `|` im Text verschiebt die Zellen (Spaltenversatz, Befund 391);
  `ledger.py --schliesse` und `--pruefe` melden schiefe Zeilen.

## Prüfausdruck schreiben

- In Backticks, einzeilig, beginnt mit `grep`, `rg`, `test`, `python3`, `pytest`, `git diff` oder `git grep`
  (`ERLAUBTE_KOMMANDOS` in `ledger.py`); eine führende Negation `! grep …` ist erlaubt. Alles andere zählt als „kein
  Prüfausdruck“.
- Kein Zeichen `|` im Ausdruck: Wo eines nötig wäre, in Python `chr(124)`, ein Backtick als `chr(96)`. Kein `echo`,
  keine Heredocs, keine Umleitung.
- Er liest nur den Bericht oder den Code, den der Befund nennt, **nie** den Ledger selbst und keine feste Zeilennummer
  (Zeilen verschieben sich, Selbstbeleg-Fehlertyp).
- Er prüft den Sachverhalt, nicht das Vorkommen eines Stichworts: Er muss auf dem Stand vor der Behebung mit Wert
  ungleich 0 enden und danach mit 0. Beides wird gemessen, nicht angenommen:
  - Nachher: Ausdruck auf dem Branch ausführen, Exit-Code notieren.
  - Vorher: Die betroffenen Dateien per `git show origin/main:<pfad>` in das Probeverzeichnis kopieren (mit
    `python3 -c` und `subprocess.run`/`pathlib.Path.write_bytes`), den Ausdruck dort (Pfade angepasst) laufen lassen.
- Ausdrücke anderer Befunde werden nicht angefasst. Ändert deine Arbeit den Bericht, lässt du den Lauf
  `ledger.py <nr> --pruefe` zeigen, ob ein bisher grüner Ausdruck rot wird; ein solcher wird nur mit Begründung im
  Revisionsabschnitt fortgeschrieben (altes und neues Kommando wörtlich), sonst ist deine Änderung falsch.

## Befund eintragen (neuer Befund)

1. Neue Nummer bestimmen (höchste plus eins, siehe oben) und in der Kopftabelle in der Reihenfolge der Nummern einfügen.
2. Zeile mit sieben Zellen: Stelle · Kurzfassung (Art in Fettdruck, z. B. **Lücke**), Kategorie A/B/C, Status `offen`,
   Umsetzungsnachweis `—` oder Vermerk, Prüfausdruck (falls bekannt), Begründung.
3. Gleiche Zeile mit Langtext in die Befundtabelle des Review-Abschnitts.
4. Kopfzahl um eins erhöhen (siehe „Kopfzahl“) und den Satz „vergebene Befundnummern (1–N)“ im Kopftext anpassen,
   falls das Ticket die höchste Nummer hebt. Prüfe danach, ob Ausdrücke anderer Befunde die höchste Nummer lesen (T-0020).

## Befund schließen

1. Ursache beheben (im Bericht oder Code, wie das Ticket es vorgibt) und den Prüfausdruck wie oben bauen und messen.
2. In der Kopftabelle: Status `behoben`, Umsetzungsnachweis mit Verweis auf den Abschnitt „Autor-Revision T-xxxx“,
   Prüfausdruck eintragen. Wo derselbe Befund in einer Review-Runden-Tabelle steht, den Status dort gleichziehen.
3. Abschnitt `## Autor-Revision T-xxxx (Befunde …)` am Dateiende anhängen (vor einem vorhandenen Messabschnitt nur, wenn
   das Ticket es sagt): was geändert wurde, Begründungen, was bewusst nicht umgesetzt wurde.
4. Nachtragssatz im Kopftext ergänzen: „**Nachtrag T-xxxx (Datum):** … stehen auf `behoben` (siehe [Autor-Revision …]);
   die Überschrift zählt deshalb A − k = B.“
5. Kopfzahl senken (siehe unten).
6. Läuft das Ticket in einer Serie, bleibt die Form des vorigen Nachtrags maßgeblich; kopiere sie, erfinde keine neue.

## Befund wiedereröffnen

1. Nur auf Anordnung des Tickets oder wenn der Prüfausdruck des Befunds auf dem Branch rot ist und die Ursache nicht im
   Ticket behoben wird.
2. Status auf `offen` setzen, Prüfausdruck stehen lassen (er ist der Beleg des Mangels), in der Begründungsspalte den
   Grund und das Datum nennen. Nichts löschen.
3. Kopfzahl um eins erhöhen, Nachtragssatz ergänzen („… wiedereröffnet, weil …; die Überschrift zählt deshalb A + 1 = B“).

## Kopfzahl

- Die Zahl in `## Offene Befunde (N)` ist die Anzahl der Befunde, die weder `behoben` noch geschlossen sind. Sie wird
  gezählt, nicht fortgeschrieben: Zähle die offenen Befunde aus `ledger.py <nr> --status` (Spalte „offen“ plus
  zurückgestellt, wie es der Kopf der Datei bisher gezählt hat) und vergleiche mit N. Weicht der Bestand schon vor
  deiner Änderung ab (Beispiel BEFUNDE_60: Überschrift 3, `--status` meldet 5 offen), ändere das nicht still, sondern
  notiere es als Beobachtung — außer das Ticket verlangt die Korrektur.
- `ledger.py <nr> --schliesse` schließt offene **und** zurückgestellte Befunde (Status „zurückgestellt (Termin …)“), sobald ihr Prüfausdruck grün ist; ein zurückgestellter Befund muss vorher nicht von Hand auf `offen` gesetzt werden.
- Prüfe jede weitere Stelle, die die Zahl wiederholt (Schlussabsatz, Zähler im Kopftext), mit
  `grep -n '<alte Zahl>' reviews/BEFUNDE_<nr>.md` vorher und nachher.

## Durchsicht von Prüfausdrücken (Serie)

Wenn das Ticket Ausdrücke „beurteilt“ statt Befunde zu ändern: je Ausdruck eine Tabellenzeile mit Zeilenbereich im
Bezugscommit M, den gelesenen Dateien, den vom Ticket geänderten Dateien (`git show --stat`) und einem Urteil aus der
Urteilsliste des Ticketabschnitts. Ein untauglicher Ausdruck bekommt einen Ersatzblock mit altem und neuem Befehl
wörtlich, beiden Läufen am heutigen Stand und einer Probe am Vergabestand (Commit nennen). Bestehende Urteile werden
nicht geändert. Gelöscht wird nichts: `git diff -U0 origin/main...HEAD` zeigt nur hinzugefügte Zeilen, außer das Ticket
nennt einen Bereich.

## Abschluss

1. `python3 backend/scripts/ledger.py <nr> --pruefe` **nachher**: wörtlich festhalten und mit dem Lauf von Schritt 0
   vergleichen. Jeder Befund, der vorher grün war, bleibt grün; neu rot ist ein Fehler deiner Änderung. Für Berichte
   zusätzlich `python3 backend/scripts/lint_methodik.py <nr>` laufen lassen.
2. Betrifft das Ticket den Code von `ledger.py` selbst: `python3 backend/scripts/ledger.py --selbsttest` und die Tests
   `backend/tests/test_ledger*.py` über `bash scripts/testlauf.sh <datei> -q` (siehe `docs/BETRIEB.md`).
3. `git diff --numstat origin/main...HEAD` nennt nur die erlaubten Dateien.
4. Alle Ausgaben stehen **wörtlich** im Ergebnis, jeweils vorher und nachher (ein Prüfer lehnt Zusammenfassungen in Worten
   ab, T-0604: Nacharbeit nur wegen fehlender Ausgaben). Was die Ausgabe kürzt, sagt das Ergebnis.

## Beispiel (T-0568-cto, Ledger 60)

Auftrag: Befunde 25, 54, 55, 56, 75, 95 in `reviews/BEFUNDE_60.md` schließen.

- Prüfausdruck zu 25 (einzeilig, ohne `|`, `chr(124)` als Trenner): liest §3.5 des Berichts, verlangt eine Zeile
  `\(q_0`, in deren Herkunft „geparkt“ steht, eine Zeile mit `tau_` und kein `t_1`, `t_2`, `t_3` in Kapitel 5; endet
  mit `raise SystemExit(0 if … else 1)`.
- Gemessen: auf dem Branch Exit 0, auf main vor dem Paket (Bericht und Ledger per `git show main:<pfad>` kopiert) Exit 1
  für alle sechs.
- Kopftabelle: sechs Zeilen auf `behoben` mit Verweis auf `Autor-Revision T-0568`; Kopfzahl 71 − 6 = 65;
  Nachtragssatz „**Nachtrag T-0568 (23.09.2026):** 25, 54, 55, 56, 75 und 95 stehen auf `behoben` …“; neuer Abschnitt
  `## Autor-Revision T-0568 (Befunde 25, 54, 55, 56, 75, 95)` am Dateiende.
- Danach `ledger.py 60 --pruefe` und `lint_methodik.py 60`: keine Prüfung, die vorher grün war, ist rot.
