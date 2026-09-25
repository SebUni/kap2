---
name: kap3-stil
description: Einheitliche Schreibweise von KAP3 — Zahlen, Beträge, Einheiten, Datum und feste Begriffe; für alles, was eine Rolle schreibt (Methodik-Berichte, Produkttexte, Briefings)
---

# Stil von KAP3

Aufsichtsrat, 24.09.2026: Wiederkehrende Arbeit wird immer gleich ausgeführt — von der Schreibweise („1,2 Mio. €“, nicht
einmal so und einmal „1000000 €“) bis zur Methodik. Dieser Skill gilt für jede Rolle, die schreibt. Was davon maschinell
prüfbar ist, prüft `backend/scripts/lint_methodik.py` (Zahlenformat); der Rest ist Sache der Prüfung.

## Zahlen und Beträge

- Dezimalkomma, Tausenderpunkt ab 1.000 (nicht in Jahreszahlen, Postleitzahlen und Kennungen): `2,5`, `1.250,50 €`, `12.400`.
- Beträge ab einer Million in Millionen oder Milliarden mit einer oder zwei Nachkommastellen: `1,2 Mio. €`,
  `3,45 Mrd. €` — nie `1.200.000 €`, nie `1200000 €`, nie „1,2 Millionen Euro“. Darunter ausgeschrieben: `350.000 €`.
- Euro immer als `€` nach der Zahl mit Leerzeichen (`12 €`), nie `EUR` im Fließtext.
- Rundung: so genau wie die Quelle; im Fließtext und in Übersichten höchstens drei gültige Stellen, in Rechenketten und
  Herleitungen die Stellen der Rechnung.
- Prozent mit Leerzeichen: `12 %`; Prozentpunkte `3 Pp.`; Promille `4 ‰`.
- Spannen mit Halbgeviertstrich ohne Leerzeichen: `0,3–1,4`; mit Einheit einmal am Ende: `12–18 %`.

## Einheiten, Datum, Zeit

- Zahl und Einheit mit Leerzeichen: `5 km`, `28 °C`, `40 m²`, `120 EW/km²`, `100-m-Zelle` (Bindestrich in
  Zusammensetzungen).
- Raten je 1.000 Einwohner: `3,2 je 1.000 EW`.
- Datum im Text `24.09.2026`, in Dateinamen und Daten ISO `2026-09-24`; Uhrzeit `14:30 Uhr`; Zeiträume `2026–2050`.
- Preisstand in Klammern nach dem Betrag: `4.800 € (Preisstand 2024)`.

## Feste Begriffe

| So | Nicht | Anmerkung |
|---|---|---|
| Kommune | Gemeinde (als Betrachtungsebene), Stadt | „Gemeinde“ nur für amtliche Gebietseinheiten und Datensätze |
| Klimawirkung (KWRA-Name, z. B. „Hitzebelastung“) | Risiko als Eigenname | „Risiko #95“ ist die Kurzform |
| Zelle (100-m-Raster) | Kachel, Pixel | |
| bewerteter Schaden (Konto Kx) | Gesamtschaden | Aufgabe §3.6 |
| Rechenkette | Rechenweg, Formelkette | Kapitel 3.0 jedes Methodik-Berichts |
| Beispielkommune | Musterkommune, Testkommune | in Rechenketten und Beispielen |
| Abschätzung von KAP3 | Schätzung, Annahme (für begründete Abschätzungen) | Vorgabe P1/P2 |

## Prüfen

Vor der Abgabe jede Zahl gegen diese Regeln lesen; bei Methodik-Berichten `python3 backend/scripts/lint_methodik.py <nr>`
laufen lassen — der Lint meldet Beträge ab einer Million in voller Länge, ausgeschriebene Währung und fehlende Leerzeichen
vor `%`.
