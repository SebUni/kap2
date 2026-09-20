# Aufwandsmessung Steckbrief #62 gegen die Schätzung 60–80 Einheiten

Quelle: `/opt/overlord/firma-supervisor/betrieb/delegationen.jsonl` und
`/opt/overlord/firma-supervisor/betrieb/budget.jsonl`, ausschließlich lesend. Erfasst sind alle
nicht abgebrochenen Teilpakete des Vorhabens T-0357 (`eltern: T-0357`), je Läufe von Entwickler und
Prüfer, einschließlich aller Nacharbeitsrunden. Eine Einheit entspricht einem USD-Gegenwert
(`kosten_usd` je Lauf), wie bei der Messung zu #60 in Kapitel 2 von `m1-zuschnitt.md`.

| Ticketnummer | Kurztitel | Modell | Effort | Zahl der Läufe | Gemessene Einheiten |
|---|---|---|---|---|---|
| T-0402 | Befund-Ledger `BEFUNDE_62.md` anlegen | sonnet | low | 4 | 0,67 |
| T-0403 | Methodik-Lint erkennt Steckbriefe | opus | medium | 2 | 1,30 |
| T-0404 | Quellen-/Parameterrecherche aus den Arbeitsmappen | sonnet | medium | 2 | 1,17 |
| T-0405 | Steckbrief anlegen, Abschnitte 1–3 | opus | medium | 2 | 3,57 |
| T-0406 | Abschnitt 4 (Kommunensicht) und 5 (Grenzenkasten) | sonnet | medium | 2 | 0,77 |
| T-0407 | Abschnitt 6 (Maßnahme, CAPEX/OPEX, Euro-Eingrenzung) | opus | medium | 2 | 3,66 |
| T-0408 | Abschnitt 7 (Parameterliste mit Quelle/Abschätzung) | sonnet | medium | 2 | 1,57 |
| T-0409 | Gegenprüfung, Befunde ins Ledger | opus | medium | 4 | 4,38 |
| **Summe** | | | | **20** | **17,10** |

Die gemessene Summe von 17,10 Einheiten liegt damit rund 72 % unter der unteren Schätzgrenze von
60 Einheiten und rund 79 % unter der oberen Schätzgrenze von 80 Einheiten aus Kapitel 2 von
`dokumente/produkt/m1-zuschnitt.md` (Firmen-Repo) — die Schätzung war für den ersten Steckbrief
deutlich zu hoch angesetzt.

Den größten Anteil trug die Gegenprüfung (T-0409) mit 4,38 Einheiten, weil eine Nacharbeitsrunde
dort zwei zusätzliche Läufe (Entwickler und Prüfer, beide auf Opus) nötig machte; ohne
Nacharbeitsrunde war das teuerste Einzelpaket die Maßnahme mit CAPEX/OPEX-Rahmen (T-0407) mit
3,66 Einheiten. Für den Zuschnitt der neun übrigen Steckbriefe folgt daraus, die Opus-Pakete mit
hohem Prüfaufwand (Gegenprüfung, Euro-eingegrenzte Maßnahmenabschnitte) so klein und eindeutig zu
schneiden, dass sie im ersten Anlauf durchlaufen, weil eine einzige Nacharbeitsrunde dort mehr
kostet als ein ganzes Sonnet-Paket.
