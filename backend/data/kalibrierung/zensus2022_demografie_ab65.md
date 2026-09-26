# Zensus 2022, Regionaltabelle „Demografie“ — Einwohner, Gruppe 60–66 und ab 67 je Gemeinde und Kreis

Datei: `zensus2022_demografie_ab65.csv` — Spalten `schluessel, ebene, insgesamt, g60_66, ab67` (Personen).
Gebraucht für Stufe 2 der Ersatzregel für den geheimgehaltenen Anteil 65+ (Bericht #95 §3.3, Entscheidungslog
Nr. 41, Befund 116), gelesen von `backend/app/services/zensus_loader.py` (`demografie_zeile_ab65`).

## Quelle

- **[69]** Statistische Ämter des Bundes und der Länder, Zensus 2022 — Regionaltabelle „Demografie“, Blatt
  „CSV-Demografie“, Stichtag 15.05.2022:
  https://www.destatis.de/static/DE/zensus/gitterdaten/Regionaltabelle_Demografie.xlsx (abgerufen am 26.09.2026).
- Spalten: `0_Insgesamt_` = insgesamt, `Alter_infr__09` = 60–66, `Alter_infr__10` + `Alter_infr__11` = 67–74 und
  75 und älter (= ab 67).

## Verarbeitung

Skript `backend/scripts/zensus_demografie_ab65.py` (dieselbe Lesart wie `docs/methodik/anlagen/95_zellvergleich.py`):

1. Zeilen der Regionalebenen „Gemeinde“ (Schlüssel = AGS, 8 Stellen: ARS Stellen 1–5 und 10–12) und
   „Stadtkreis/kreisfreie Stadt/Landkreis“ (Schlüssel = 5 Stellen). Ergebnis: 10.786 Gemeinden, 400 Kreise.
2. „–“ = genau null (0); „.“ = unbekannt oder geheim → die Zeile bleibt ohne Werte, der Loader nimmt dann die
   Kreiszeile (Befund 119).
3. Kontrollwerte (§3.3): Warmsen 03256034 = 3158 / 388 / 602, Berlin 11000000 = 3.596.999 / 292.354 / 624.505.

## Lizenz

Datenlizenz Deutschland – Namensnennung – Version 2.0 (dl-de/by-2-0), © Statistische Ämter des Bundes und der Länder.
