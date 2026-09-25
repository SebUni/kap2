---
name: entwickler-gegenprobe-konformitaet
description: Gegenprobe einer Zeile der Konformitätsliste (docs/KONFORMITAET_CHECKLISTE.md) am Normtext — Quelle finden, Kapitel vollständig lesen, Anforderungen in einer Tabelle gegen den Bestand urteilen, Status der Zeile setzen, Testlauf.
---

# Gegenprobe einer Konformitätszeile am Normtext

Aufsichtsrat, 24.09.2026: Wiederkehrende Arbeit wird immer gleich ausgeführt. Die Gegenproben laufen seit dem 23.09.2026
nach diesem Muster (Zeilen 9, 10, 7, 19, 8). Vorlage für die Form sind die vorhandenen Abschnitte
`### Gegenprobe Zeile …` in `docs/KONFORMITAET_CHECKLISTE.md`. Dieser Skill beschreibt das Vorgehen; Urteile zu einzelnen
Zeilen enthält er nicht. Geschrieben wird nach `kap3-stil`.

## Quelle finden

- Die Quellen liegen unter `docs/KWAR/` (KWRA 2021, auch Teilbericht 6) und `docs/UBA/`. Welche Datei und welches
  Kapitel gemeint ist, steht in den Spalten „Quelle“ und „Fundstelle“ der Zeile.
- Gesucht wird mit den Werkzeugen Glob und Grep, nicht mit `find /` (im gesteuerten Lauf gesperrt).
- Das Inventar (Gliederung, Zusammenfassung, Abbildungen und Tabellen je Seite) liefert, falls erreichbar:
  `python3 /opt/overlord/overlord/skripte/dokumente.py inventar "<datei.pdf>"`. Ist das Skript nicht erreichbar, steht
  das im Abschnitt „Gelesene Seiten“, und das Inhaltsverzeichnis wird über den Text der ersten Seiten gelesen.
- Prüfe, ob PDF-Seitenzahl und gedruckte Seitenzahl übereinstimmen, und nenne im Ergebnis, welche du verwendest.

## Lesen

Du liest, du suchst nicht. Stichwortsuche ergänzt das Lesen, sie ersetzt es nie.

- Das Inhaltsverzeichnis ganz.
- Die Zusammenfassung oder Einleitung des Kapitels ganz.
- Das genannte Kapitel vollständig, samt Fußnoten; dazu die Seite davor und danach, um die Kapitelgrenzen zu prüfen.
  Text: `python3 /opt/overlord/overlord/skripte/dokumente.py text "<datei.pdf>" --seiten a-b`.
- Tabellen und Abbildungen, die Anforderungen enthalten, als Bild ansehen:
  `python3 /opt/overlord/overlord/skripte/dokumente.py seite "<datei.pdf>" n`. Nur die nötigen Seiten, Bildseiten
  kosten.
- Jede Aussage über den Normtext steht mit Seite. Jede Zahl mit Seite und Abschnitt.
- „Nicht enthalten“ sagst du nur mit der Liste der gelesenen Seiten, nie, weil ein Stichwort nicht vorkommt.
- Im Produkt liest du die in der Spalte „Beleg im Produkt“ genannten Dateien und Funktionen vollständig, dazu die
  Stellen, die sie weiterverwenden. Was du ausführst, ändert nichts.

## Tabelle der Anforderungen

Zerlege das Kapitel in einzelne Anforderungen und stelle sie dem Bestand gegenüber. Der Kopf ist wörtlich:

| Nr | Anforderung (Wortlaut oder enge Wiedergabe) | Seite | tragender Beleg (Datei, Funktion oder Abschnitt) | Urteil |
|---|---|---|---|---|

- Nummern `A1`, `A2` …, in der Reihenfolge des Normtexts.
- Das Urteil heißt genau `trägt`, `trägt teilweise` oder `trägt nicht`. Ohne Beleg steht in der Spalte „keiner“ mit dem
  Grund.
- Unter der Tabelle steht **Begründung je Urteil** als Liste, eine Begründung je Anforderung (A1: …, A2: …).
- Befunde der Quelle selbst (Ergebnisse, Mittelwerte, Kernaussagen) sind keine Anforderungen. Sie werden in einem Satz
  „Nicht als eigene Anforderung gewertet“ genannt.
- Der Abschnitt beginnt mit der Frage der Gegenprobe (ein bis zwei Sätze) und der gelesenen Datei.

## Gelesene Seiten

Am Ende des Abschnitts steht **Gelesene Seiten und Abschnitte:** — Inventar (mit Seitenzahl des Dokuments),
Inhaltsverzeichnis, Zusammenfassung oder Einleitung, Kapitel mit Seiten samt Fußnoten, als Bild angesehene Seiten mit
Tabellen- oder Abbildungsnummer, geprüfte Kapitelgrenzen. Danach ausdrücklich: **Nicht gelesen:** … Ein erzeugtes
`.lesbar/`-Verzeichnis wird nach dem Lesen wieder gelöscht.

## Schlusssatz und Status

- Der Abschnitt heißt `### Gegenprobe Zeile <n> gegen <Quelle>, <Kapitel>`. Er steht in `docs/KONFORMITAET_CHECKLISTE.md`
  nach dem letzten vorhandenen Abschnitt `### Gegenprobe …` und vor `## Ergebnis`.
- Er schließt mit **Schluss:** Zählung der Urteile (voll, teilweise, nicht) und Antwort auf die Frage der Gegenprobe.
- Die Zeile in der Tabelle bleibt `erfüllt`, wenn alle Anforderungen tragen. Andernfalls steht ihr Status in derselben
  Änderung auf `teilweise`, und die Spalte „Lücke“ nennt, was fehlt, mit Verweis „Einzelnachweis: Abschnitt „Gegenprobe
  Zeile <n>““.
- Zählungen in „Nachtrag: Abschlusszählung“ und „Zusammenfassung“ zieht diese Gegenprobe nicht nach, wenn das Ticket es
  nicht verlangt; der Schluss vermerkt, dass sie überholt sind.

## Testlauf

Vor dem Ergebnis läuft `scripts/testlauf.sh` über den `python3`-Subprozess aus `docs/BETRIEB.md` (Abschnitt „Wenn der
Aufruf verweigert wird“), aus dem Wurzelverzeichnis des Repos:

```bash
python3 -c "import subprocess,sys; p=subprocess.run(['bash','scripts/testlauf.sh','-q'],capture_output=True,text=True); print(p.stdout[-3000:], p.stderr[-2000:]); sys.exit(p.returncode)"
```

Im Ergebnis stehen die Schlusszeile von `pytest` und der Exit-Code wörtlich. Es dürfen keine Tracebacks erscheinen.

## Grenzen

- Geändert wird nur `docs/KONFORMITAET_CHECKLISTE.md`. Kein Code, keine Tests, keine anderen Dokumente.
- Probedateien liegen unter `$TMPDIR`, nie unter `/tmp`.
- Kein `git cherry-pick`. Commit und Push übernimmt der Supervisor.
- Ein erzeugtes `.lesbar/`-Verzeichnis wird wieder gelöscht.
- Die Schreibweise folgt `kap3-stil` (Dezimalkomma, `€`, Datum `24.09.2026`, feste Begriffe).
- Läuft eine andere Gegenprobe parallel, ändert jede nur ihren eigenen Abschnitt und ihre eigene Zeile der Tabelle.
