# M0-Stand — Ist-Messung der Risiken 95, 96, 98

Reines Feststellen des Ist-Stands (Ticket T-0004), keine Reparatur. Nichts an Methodik-Berichten,
Befund-Ledgern, Produktionscode oder Prüfwerkzeugen wurde verändert. Alle Befehle liefen am
04.09.2026 im Repo-Root `/home/basti/overlord/kap2` (Branch `ticket/T-0004`).

## 1. Golden-Tests

Befehl je Risiko: `pytest backend/tests/test_methodik_<nr>_golden.py`

| Risiko | Letzte Ausgabezeile | Rückgabecode |
|---|---|---|
| 95 | `======================== 12 passed, 1 warning in 1.00s =========================` | 0 |
| 96 | `======================== 16 passed, 1 warning in 0.51s =========================` | 0 |
| 98 | `======================== 15 passed, 1 warning in 0.53s =========================` | 0 |

## 2. Lints

Befehl je Risiko: `python3 backend/scripts/lint_methodik.py <nr>`

| Risiko | Checks (grün) | Fehler (ROT) | Rückgabecode |
|---|---|---|---|
| 95 | 125 | 1 | 1 |
| 96 | 103 | 1 | 1 |
| 98 | 227 | 2 | 1 |

Wortlaut der ROT-Zeilen:

- **95**: `ROT  Zeichentabelle: Abschnitt 3.5 nicht gefunden`
- **96**: `ROT  Zeichentabelle: Abschnitt 3.5 nicht gefunden`
- **98**:
  - `ROT  Abgeloester Wert im Code params.py, Zeile 521: ~ 6,2 % — "8,51 % x 0,7119 ~ 6,2 % ueber den Normalperiodenversatz "`
  - `ROT  Abgeloester Wert im Code params.py, Zeile 522: 2,1 %/Dek — "~ 2,1 %/Dekade. Elastizitaet zeitinvariant angenommen "`

## 3. Ledger-Prüfung

Befehl je Risiko: `python3 backend/scripts/ledger.py <nr> --pruefe`. Kein Lauf hat die 120-Sekunden-Grenze
erreicht (alle liefen unter 5 Sekunden).

| Risiko | Schlusszeile | Rückgabecode |
|---|---|---|
| 95 | `ROT — die Tabellenstruktur trägt die Zusicherung nicht.` | 1 |
| 96 | `ROT — die Tabellenstruktur trägt die Zusicherung nicht.` | 1 |
| 98 | `ROT — mindestens ein Prüfausdruck belegt seinen Befund nicht.` | 1 |

## 4. Offene Befunde in `reviews/BEFUNDE_98.md`

Kriterium: der Status der Befund-Zeile lautet wörtlich `offen` (nicht `zurückgestellt`, nicht
`abweichend gelöst`). Der Runde-23-Kopf über der Tabelle nennt „Befunde 412–420 (A:1 · B:6 · C:2)"
— neun Nummern; Befund **416** trägt darin aber den Status `abweichend gelöst — die Zählung ist
ersatzlos entfallen …`, nicht `offen`. Er ist deshalb nicht in dieser Tabelle. Das ist eine reine
Feststellung anhand des Statuswortlauts, keine Bewertung — die Divergenz zwischen Abschnittskopf
(9) und tatsächlichem Statuswortlaut (8 × `offen`) wird hier nur vermerkt.

Je Zeile: der im Ledger hinterlegte Prüfausdruck (Spalte „Prüfausdruck") wurde einzeln ausgeführt
(`cwd` = Repo-Root); der Rückgabecode dieser Ausführung steht in Spalte „Rückgabecode".

| Nummer | Kategorie | Rückgabecode | Ableitung |
|---|---|---|---|
| 412 | A | 0 | im Code bereits behoben |
| 413 | B | 0 | im Code bereits behoben |
| 414 | B | 0 | im Code bereits behoben |
| 415 | B | 0 | im Code bereits behoben |
| 417 | B | 0 | im Code bereits behoben |
| 418 | B | 0 | im Code bereits behoben |
| 419 | C | 0 | im Code bereits behoben |
| 420 | C | 0 | im Code bereits behoben |
| **Summe** | **A:1 · B:5 · C:2** | **0 (8 × RC 0)** | **8 im Code bereits behoben · 0 noch offen** |

## 5. Integrationsstand

Geprüft gegen `backend/app/data/catalog.py`, Liste `RISKS`, Feld `kwra_id`.

- **95 (Hitzebelastung)**: integriert: ja
  - Beleg: `backend/app/data/catalog.py:168` (`"kwra_id": 95, "kwra_name": "Hitzebelastung", …` — Eintrag `EXPECTED_ANNUAL_MORTALITY`)
  - weiterer Teil-Ausweis: `backend/app/data/catalog.py:200` (`"kwra_id": 95, "kwra_name": "Hitzebelastung", …` — Eintrag `EXPECTED_ANNUAL_MORBIDITY`)
- **96 (Aeroallergene)**: integriert: ja
  - Beleg: `backend/app/data/catalog.py:225` (`"kwra_id": 96,` — Eintrag `EXPECTED_ANNUAL_ALLERGY_DAYS`)
- **98 (UV-Schädigungen)**: integriert: ja
  - Beleg: `backend/app/data/catalog.py:257` (`"kwra_id": 98,` — Eintrag `EXPECTED_ANNUAL_UV_YLL`)
