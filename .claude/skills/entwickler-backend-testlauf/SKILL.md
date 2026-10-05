---
name: entwickler-backend-testlauf
description: Die Backend-Suite im Produkt-Repo so starten, dass sie in der Projektumgebung wirklich läuft (Ersatzmodul nur bei fehlenden Paketen, gemeinsame conftest.py), und die Ausgabe wörtlich ins Ergebnis übernehmen.
---

# Backend-Testlauf

Wofür: Fast jedes Backend-Abnahmekriterium verlangt einen Testlauf mit wörtlicher Ausgabe. Die Prüfumgebung wird dafür **nicht** neu gebaut. Sie steht seit T-0500 und wird nur benutzt.

## Der einzige Startweg: `scripts/testlauf.sh`

Nie `python3 -m pytest …` direkt aufrufen. Dem System-Python fehlen Pakete wie `bcrypt`, und die ganze Suite bricht beim Einsammeln ab („Interrupted: 9 errors during collection“). `scripts/testlauf.sh` (T-0500) erledigt, was nötig ist:

- legt beim ersten Lauf die Umgebung `~/.venvs/kap2` an (oder `$KAP2_VENV`);
- installiert `backend/requirements.txt` und pytest nach, wenn sich die Anforderungen geändert haben;
- stellt Playwright-Chromium bereit (T-1423);
- setzt `PYTHONPATH` auf `backend/`;
- hält Bytecode- und pytest-Cache außerhalb des Repos, sodass `git status` sauber bleibt;
- lässt ohne Argumente alles unter `backend/tests` laufen; alle Argumente gehen an pytest.

## Was im Bestand schon da ist (nicht neu erfinden)

- `backend/tests/_stub_heavy_deps.py`: `install()` legt Ersatzmodule (SQLAlchemy, GeoAlchemy, openpyxl u. a.) **nur dann** in `sys.modules`, wenn das echte Paket fehlt. Ist es installiert, läuft der Test gegen die echte Bibliothek.
- `backend/tests/conftest.py` ruft `install()` genau einmal vor dem Einsammeln auf. Testdateien rufen `install()` **nicht** selbst auf, sonst hängt das Ergebnis von der Reihenfolge ab.
- Im Testlauf gibt es keine Datenbank. Tests, die eine brauchen, laufen hier nicht. Das wird im Ergebnis gesagt, nicht umgangen.

## Schritte

1. Im Wurzelverzeichnis des Produkt-Repos bleiben.
2. Verlangt das Abnahmekriterium einen bestimmten Befehl, wird **genau dieser Befehl** ausgeführt, Zeichen für Zeichen (meist `python3 -c "import subprocess,sys; p=subprocess.run(['bash','scripts/testlauf.sh', …],capture_output=True,text=True); print(p.stdout[-3000:], p.stderr[-2000:]); sys.exit(p.returncode)"`).
3. Sonst laufen zuerst die eigenen Dateien:
   `bash scripts/testlauf.sh backend/tests/<datei>.py -q`
4. Danach die ganze Suite:
   `bash scripts/testlauf.sh -q`
5. Schlägt ein Import fehl (`ModuleNotFoundError`), zuerst prüfen, ob das Paket in `backend/requirements.txt` steht. Steht es dort, liegt der Fehler an der Umgebung, nicht am Code. Ein Ersatzmodul in `_stub_heavy_deps.py` wird nur ergänzt, wenn das Ticket es verlangt, nur für fehlende Pakete und nie für ein vorhandenes. Verboten sind ein `install()` in einer Testdatei, eine zweite conftest.py und Eingriffe in `sys.path`.
6. Ein Test, der allein grün und in der Suite rot ist (oder umgekehrt), hat einen Reihenfolgefehler. Die Ursache wird benannt, nicht überdeckt.
7. Fehlschläge, die schon vorher bestanden, werden so festgestellt (fester Ablauf, ohne `git stash`): Die rot gemeldeten Dateien laufen auf dem Ursprungsstand, in einem Wegwerf-Arbeitsbaum im Probeverzeichnis:
   `git worktree add <Probeverzeichnis>/ursprung origin/main`
   `bash <Probeverzeichnis>/ursprung/scripts/testlauf.sh backend/tests/<rote_datei>.py -q`
   `git worktree remove --force <Probeverzeichnis>/ursprung`
   `testlauf.sh` leitet den Repo-Pfad aus seinem eigenen Ort ab und läuft deshalb im Wegwerf-Stand; die Umgebung teilen sich beide Arbeitsbäume. Sind die Fehler dort ebenfalls rot, bestanden sie schon vorher. Im Ergebnis stehen sie getrennt von den eigenen Fehlern, mit Datei- und Testname. Ist `origin/main` nicht erreichbar, steht das so im Ergebnis; geraten wird nicht.

## Ergebnis

- In `beobachtungen` stehen wörtlich: der Befehl, die Fehlschläge, die **Schlusszeile** („N passed, M failed … in X s“) und der **Exit-Code**. Nichts zusammenfassen, nichts runden. „Läuft grün, Exit-Code 0“ allein genügt nicht.
- Der Exit-Code wird nicht mit `echo $?` abgefragt. Fehlt die Zeile `Exit code <n>` in der Werkzeugausgabe, war er 0.
- Zeilen mit dem Präfix `[testlauf]` (Anlegen der Umgebung, Installieren) kommen vom Skript, nicht von pytest. Sie gehören nicht zur wörtlichen pytest-Ausgabe; falls sie auftraten, genügt ein Satz („Umgebung beim ersten Lauf angelegt“).
- Die eigenen Sätze folgen dem Stil-Skill `kap3-stil`; die Ausgabe selbst bleibt unverändert.

## Beispiel aus T-1599-cto (Stadtbaum-Zellfunktion zu #96)

Befehl aus dem Abnahmekriterium von T-1599-cto, unverändert ausgeführt:

```
$ python3 -c "import subprocess,sys; p=subprocess.run(['bash','scripts/testlauf.sh','backend/tests/test_stadtbaum_zellfunktion.py','backend/tests/test_methodik_96_golden.py','backend/tests/test_massnahme_s158.py','backend/tests/test_methodik_96_s158_golden.py','-q'],capture_output=True,text=True); print(p.stdout[-3000:], p.stderr[-2000:]); sys.exit(p.returncode)"
....................................                                     [100%]
=============================== warnings summary ===============================
../../../../.venvs/kap2/lib/python3.12/site-packages/pydantic/_internal/_config.py:295
  /home/basti/.venvs/kap2/lib/python3.12/site-packages/pydantic/_internal/_config.py:295: PydanticDeprecatedSince20: Support for class-based `config` is deprecated, use ConfigDict instead. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.10/migration/
    warnings.warn(DEPRECATION_MESSAGE, DeprecationWarning)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
36 passed, 1 warning in 3.04s
```

Exit-Code 0, denn die Werkzeugausgabe enthält keine Zeile `Exit code`. Die Schlusszeile enthält „passed“ und weder „failed“ noch „error“. Gemessen am 05.10.2026; damals hieß die Schlusszeile in T-1599-cto „35 passed, 1 warning in 1.98s“, inzwischen kam ein Test hinzu.

Daraus gelernt: In T-1599-cto lief der Test in Runde 0 grün, trotzdem ging das Ticket in die Nacharbeit, weil das Ergebnis nur „laufen grün, Exit-Code 0“ nannte und die wörtliche Schlusszeile fehlte. Erst Runde 1 mit der Schlusszeile wörtlich bekam die Freigabe.
