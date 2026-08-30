# Bevölkerung je Bundesland × Altersband (Kalibrierlauf Gesundheit)

Datei: `bevoelkerung_bundesland_altersband.csv` — Spalten `bundesland, u65, a65_74, a75_84, a85p` (Personen, Insgesamt = Männer + Frauen).

## Quelle

- **Statistik:** 12411 „Fortschreibung des Bevölkerungsstandes" (Basis Zensus 2022), Bevölkerung nach Geschlecht und Altersgruppen (20 Gruppen: unter 5, 5–10, …, 90–95, 95 Jahre und mehr).
- **Stichtag:** 31.12.2023.
- **Tabelle:** regionalstatistik.de (GENESIS der Statistischen Ämter des Bundes und der Länder), Tabelle **12411-09-01-4-B** „Bevölkerung nach Geschlecht und Altersgruppen (20) – Stichtag 31.12. – (ab 2011) regionale Ebenen", abgerufen per GENESIS-WS-2020-REST (`data/tablefile`, ffcsv, Konto RE014779) am **22.08.2026**. Inhaltlich identisch mit Destatis-GENESIS 12411-0013 (dort war der Abruf ohne Login nicht möglich: Katalog/Tabellen liefern als GAST HTTP 401).
- **URL (interaktiv):** https://www.regionalstatistik.de/genesis//online?operation=table&code=12411-09-01-4-B

## Verarbeitung

1. Der Abruf liefert nur die Ebene „Kreise und kreisfreie Städte" (400 Kreise, 5-stelliger Schlüssel) plus 15 Stadtbezirks-Zeilen (8-stellige Schlüssel: Berlin-Bezirke, Hannover, Aachen, Saarbrücken). Die 8-stelligen Zeilen sind Teilmengen ihrer Kreise und wurden **ausgeschlossen**.
2. Bundesland = Summe aller Kreise mit gleichem Landesschlüssel (erste zwei Stellen des AGS).
3. Altersbänder: `u65` = unter 5 … 60–65; `a65_74` = 65–70 + 70–75; `a75_84` = 75–80 + 80–85; `a85p` = 85–90 + 90–95 + 95 und mehr.
4. Kontrolle: Summe aller Bänder und Länder = **83 456 045** = amtliche Bevölkerung Deutschlands am 31.12.2023; Männer + Frauen = Insgesamt in jedem Band.

## Deutschland-Summen (Kontrollwerte)

| Band | Insgesamt | Männer | Frauen |
|---|---:|---:|---:|
| u65 | 64 747 448 | 32 922 306 | 31 825 142 |
| a65_74 | 9 569 640 | 4 525 035 | 5 044 605 |
| a75_84 | 6 294 744 | 2 724 298 | 3 570 446 |
| a85p | 2 844 213 | 990 292 | 1 853 921 |
| davon 85–89 / 90–94 / 95+ | 2 022 499 / 647 607 / 174 107 | 754 258 / 197 380 / 38 654 | 1 268 241 / 450 227 / 135 453 |

## Lizenz

Datenlizenz Deutschland – Namensnennung – Version 2.0 (dl-de/by-2-0), © Statistische Ämter des Bundes und der Länder 2024.
