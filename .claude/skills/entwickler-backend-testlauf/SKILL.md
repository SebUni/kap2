---
name: entwickler-backend-testlauf
description: Die Backend-Suite im Produkt-Repo so starten, dass sie in der Projektumgebung wirklich läuft (Ersatzmodul nur bei fehlenden Paketen, gemeinsame conftest.py), und die Ausgabe wörtlich ins Ergebnis übernehmen.
---

# Backend-Testlauf

Wofür: Fast jedes Backend-Abnahmekriterium verlangt einen Testlauf mit wörtlicher Ausgabe. Die Prüfumgebung wird dafür **nicht** neu gebaut — sie steht (T-0500) und wird nur benutzt.

## Der einzige Startweg: `scripts/testlauf.sh`

Nie `python3 -m pytest …` direkt: Das System-Python hat Pakete wie `bcrypt` nicht, und die ganze Suite bricht beim Einsammeln ab („9 errors during collection“). `scripts/testlauf.sh` (T-0500) macht, was nötig ist:

- legt beim ersten Lauf die Umgebung `~/.venvs/kap2` an (oder `$KAP2_VENV`) und installiert `backend/requirements.txt` plus pytest nach, wenn sich die Anforderungen geändert haben;
- stellt Playwright-Chromium bereit (T-1423);
- setzt `PYTHONPATH` auf `backend/`, hält Bytecode- und pytest-Cache außerhalb des Repos (`git status` bleibt sauber);
- ohne Argumente läuft alles unter `backend/tests`; alle Argumente gehen an pytest.

## Was im Bestand schon da ist (nicht neu erfinden)

- `backend/tests/_stub_heavy_deps.py` — `install()` legt Ersatzmodule (SQLAlchemy, GeoAlchemy, openpyxl u. a.) **nur dann** in `sys.modules`, wenn das echte Paket fehlt. Ist es installiert, läuft der Test gegen die echte Bibliothek.
- `backend/tests/conftest.py` — ruft `install()` genau einmal vor dem Einsammeln auf. Testdateien rufen `install()` **nicht** selbst auf; sonst hängt das Ergebnis von der Reihenfolge ab.
- Es gibt keine Datenbank im Testlauf. Tests, die eine brauchen, laufen hier nicht; das im Ergebnis sagen, nicht umgehen.

## Schritte

1. Im Wurzelverzeichnis des Produkt-Repos bleiben.
2. Zuerst die eigene(n) Datei(en):
   `bash scripts/testlauf.sh backend/tests/<datei>.py -q`
3. Dann die ganze Suite:
   `bash scripts/testlauf.sh -q`
4. Schlägt ein Import fehl (`ModuleNotFoundError`): zuerst prüfen, ob das Paket in `backend/requirements.txt` steht (dann liegt es an der Umgebung, nicht am Code). Ein Ersatzmodul in `_stub_heavy_deps.py` ergänzt man nur, wenn das Ticket es verlangt, nur für Fehlendes, nie für ein vorhandenes Paket. Kein `install()` in einer Testdatei, kein zweites conftest, keine `sys.path`-Tricks.
5. Ein Test, der allein grün und in der Suite rot ist (oder umgekehrt), ist ein Reihenfolgefehler: Ursache benennen, nicht überdecken.
6. Rote Tests von vorher feststellen — fester Ablauf, ohne `git stash`: Die rot gemeldeten Dateien auf dem Ursprungsstand laufen lassen, in einem Wegwerf-Arbeitsbaum im Probeverzeichnis:
   `git worktree add <Probeverzeichnis>/ursprung origin/main`
   `bash <Probeverzeichnis>/ursprung/scripts/testlauf.sh backend/tests/<rote_datei>.py -q`
   `git worktree remove --force <Probeverzeichnis>/ursprung`
   (`testlauf.sh` leitet das Repo aus seinem eigenen Ort ab, läuft also im Wegwerf-Stand; die Umgebung wird geteilt.) Fehler, die dort ebenfalls rot sind, gelten als vorher bestehend und werden im Ergebnis getrennt von eigenen Fehlern genannt, mit Dateiname und Testname. Ist `origin/main` nicht erreichbar, wird das so gesagt, nicht geraten.

## Ergebnis

- In `beobachtungen` steht die pytest-Ausgabe **wörtlich**: Befehl, die Fehlschläge, die Schlusszeile („N passed, M failed in X s“). Nicht zusammenfassen, nicht runden.
- Zeilen mit dem Präfix `[testlauf]` (Anlegen der Umgebung, Installieren) stammen vom Skript, nicht von pytest. Sie gehören nicht in die wörtliche pytest-Ausgabe; man erwähnt sie in einem Satz („Umgebung beim ersten Lauf angelegt“), falls sie auftraten.
- Schreibweise der eigenen Sätze nach dem Stil-Skill `kap3-stil`; die Ausgabe selbst bleibt unverändert.

## Beispiel (zu T-1599-cto: Ersatzmodul greift nur bei fehlenden Paketen, gemeinsame conftest.py)

```
$ bash scripts/testlauf.sh backend/tests/test_stub_heavy_deps.py -q
..                                                                       [100%]
2 passed in 0.11s
```
