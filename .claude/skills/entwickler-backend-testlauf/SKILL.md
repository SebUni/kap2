---
name: entwickler-backend-testlauf
description: Die Backend-Suite im Produkt-Repo so starten, dass sie in der Projektumgebung wirklich läuft (Ersatzmodul nur bei fehlenden Paketen, gemeinsame conftest.py), und die Ausgabe wörtlich ins Ergebnis übernehmen.
---

# Backend-Testlauf

Wofür: Fast jedes Backend-Abnahmekriterium verlangt einen Testlauf mit wörtlicher Ausgabe. Die Prüfumgebung wird dafür **nicht** neu gebaut — sie steht (T-0481, T-0590) und wird nur benutzt.

## Was schon da ist (nicht neu erfinden)

- `backend/tests/_stub_heavy_deps.py` — `install()` hängt Ersatzmodule (SQLAlchemy, GeoAlchemy, openpyxl u. a.) **nur dann** in `sys.modules`, wenn das echte Paket fehlt. Ist es installiert, läuft der Test gegen die echte Bibliothek.
- `backend/tests/conftest.py` — ruft `install()` genau einmal vor dem Einsammeln auf. Testdateien rufen `install()` **nicht** selbst auf; sonst hängt das Ergebnis von der Reihenfolge ab.
- Es gibt keine Datenbank im Testlauf. Tests, die eine brauchen, laufen hier nicht; das im Ergebnis sagen, nicht umgehen.

## Schritte

1. Im Wurzelverzeichnis des Produkt-Repos bleiben (nicht nach `backend/` wechseln).
2. Zuerst die eigene Datei(en) laufen lassen:
   `python3 -m pytest backend/tests/<datei>.py -q`
3. Dann die ganze Suite:
   `python3 -m pytest backend/tests -q`
4. Schlägt ein Import fehl (`ModuleNotFoundError`): zuerst prüfen, ob das Paket wirklich fehlt und ob `_stub_heavy_deps.py` es abdecken muss. Ersatzmodul **nur** dort ergänzen, nur für Fehlendes, und nur wenn das Ticket es verlangt; ein vorhandenes Paket nie ersetzen. Kein `install()` in einer Testdatei, kein zweites conftest, keine `sys.path`-Tricks.
5. Ein Test, der allein grün und in der Suite rot ist (oder umgekehrt), ist ein Reihenfolgefehler: Ursache benennen, nicht mit `-p no:randomly` o. ä. überdecken.
6. Fehlschläge, die schon vor der Änderung bestanden, vorher feststellen (`git stash` ist verboten, stattdessen die Suite auf dem unveränderten Stand des Branches-Ursprungs lesen) und im Ergebnis getrennt von eigenen Fehlern nennen.

## Ergebnis

Die Ausgabe der Läufe steht **wörtlich** in `beobachtungen` (Befehl, letzte Zeilen mit „N passed, M failed in X s“). Nicht zusammenfassen, nicht runden. Schreibweise nach dem Stil-Skill `kap3-stil` (Zahlen, Einheiten, Begriffe); die Ausgabe selbst bleibt unverändert.

## Beispiel (T-0590 / T-0481)

```
$ python3 -m pytest backend/tests/test_stub_heavy_deps.py -q
..                                                                       [100%]
2 passed in 0.13s
```
