---
description: Gegenprüfung eines Methodik-Berichts nach §5 der Aufgabe (Lints + 14 Leitfragen). Nur in einer FRISCHEN Session ausführen — nie in der Session, die den Bericht geschrieben hat.
argument-hint: <risiko-nr>
allowed-tools: Read, Bash, Grep, Glob, Edit, Write
---

Risiko-Nummer: $ARGUMENTS

Du bist die unabhängige Gegenprüfung. Maßstab ist ausschließlich
@docs/AUFGABE_METHODIK_SCHADENSRECHNUNG.md (§3 Anforderungskatalog, §5 Prüfauftrag).
Melde **Lücken, Fehler und Widersprüche — nicht Stil.** Sei skeptisch gegenüber jeder Behauptung
des Berichts: prüfe gegen die Quellen, nicht gegen den Berichtstext.

## 0 · Vorbedingung: Prüfgrundlagen-Bundle

Prüfe, dass vorliegen: der Bericht `docs/methodik/<nr>_*.md`, die Aufgabe, beide Arbeitsmappen
(`docs/Schadensbaum/*.xlsx`), die im Bericht referenzierten Anlagen (Skripte/CSVs) und das Ledger
`reviews/BEFUNDE_<nr>.md`. **Fehlt etwas: abbrechen** — ein Review ohne vollständiges Bundle ist
ungültig (§5). Liste, was fehlt.
Sonderfall M0 (Altbestand): Bericht ist `docs/render/METHODIK_M0_GESUNDHEIT.html`
(PDF-Export im docs-Root), Ledger ist `docs/METHODIK_M0_GESUNDHEIT_Gegenpruefung_Rev5.md`.

## 1 · Deterministische Lints (zuerst — nicht manuell prüfen, was die Maschine prüft)

Existiert `backend/scripts/lint_methodik.py`: ausführen und Ergebnis übernehmen. Sonst führe die Checks
selbst per Python/Grep aus und schlage am Ende vor, sie als Skript zu persistieren:

- Jede Zeichentabellen-Zeile hat Wert **und** Herkunft (Register-ID oder Herleitungs-Anker);
  verbotene Formulierungen: „Platzhalter", „wird … hergeleitet/ergänzt/nachgezogen", „später".
- Jeder Parameter-Block vollständig (id, wert, einheit, band, herkunft, quelle; `preisstand`
  bei Kostensätzen; bandzuordnung/endpunkt gesetzt); jedes Formelzeichen hat einen Block.
- Jede Quelle mit DOI/URL + Archiv-Snapshot.
- **Knoten-Abgleich gegen die Arbeitsmappe** (openpyxl): jeder Knoten des Risikos kommt in der
  Knoten-Bilanz vor; jede im Bericht behauptete Kante/Weitergabe existiert in Netzwerkliste
  bzw. Abgleich-Protokoll; Konto/Ebene/Bausteine stimmen mit der Monetarisierungs-Zeile überein.
- Beispiel-Test-Blöcke ausführen — jedes Mini-Rechenbeispiel muss aufgehen.
- Preisstand-Einheitlichkeit aller Kostensätze des Berichts.

## 2 · Leitfragen 1–14 (§5) — einzeln, mit Verdikt

Beantworte **jede** Leitfrage einzeln mit `bestanden` oder `Befund` **plus Beleg** — niemals
pauschal „nichts gefunden". Rechne Herleitungen stichprobenhaft nach (Python): OR-Übersetzungen,
Kalibrierketten, Umrechnungen, Bandobergrenzen. Prüfe besonders die bekannten Fehlerklassen:
Kalibriermodell ≠ Produktionsmodell, Band-/Endpunkt-Zuordnung von Modifikatoren, unzentrierte
Faktoren, Fall-Kontroll-OR als Maßnahmeneffekt, Kategorienfehler (Korrelation als Anteil),
Referenzwert-Doppelzählung, Quellen-Synchronität (LF 14).

## 3 · Ledger und Regression

- Neue Befunde **anhängen** an `reviews/BEFUNDE_<nr>.md`, Nummerierung fortlaufend, Format:
  Stelle · Art (Lücke/Fehler/Widerspruch) · Begründung · Vorschlag · Kategorie (A/B/C).
- **Regression:** Prüfe jeden als „übernommen" markierten Alt-Befund, ob die Lösung im aktuellen
  Stand noch trägt; Rückfälle als neuen Befund mit Verweis.
- Bei Re-Reviews: Fokus auf Diff + offene Befunde; **volle Prüfung erneut**, wenn Kalibrierung
  oder Modellstruktur geändert wurde.

## 4 · Konvergenz-Verdikt

Abschluss mit expliziter Aussage: Lints grün? Alle 14 Leitfragen mit Verdikt? Neue A-/B-Befunde
in dieser Runde? → **Null-Runde ja/nein.** Bei „ja" zusätzlich gegen die Abnahmekriterien (§6)
prüfen und Abnahme-Empfehlung oder Restpunkte-Liste ausgeben.
