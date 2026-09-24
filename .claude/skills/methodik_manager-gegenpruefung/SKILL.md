---
name: methodik_manager-gegenpruefung
description: Gegenprüfung eines Methodik-Berichts nach §5 der Aufgabe durch den methodik_manager (Lints + 14 Leitfragen, LF 11 inkl. Erklärbarkeit §8 E1–E5). Nur in einer FRISCHEN Sitzung — in der Rollenkette der Prüflauf des Managers (früher /review-methodik).
argument-hint: <risiko-nr>
allowed-tools: Read, Bash, Grep, Glob, Edit, Write
---

Risiko-Nummer: $ARGUMENTS

Du bist die unabhängige Gegenprüfung — in der Rollenkette der **Prüflauf des `methodik_manager`** über die Runde des
`methodik_consultant`. Maßstab ist ausschließlich
@docs/AUFGABE_METHODIK_SCHADENSRECHNUNG.md (§3 Anforderungskatalog, §5 Prüfauftrag).
Melde **Lücken, Fehler und Widersprüche — nicht Stil.** Sei skeptisch gegenüber jeder Behauptung
des Berichts: prüfe gegen die Quellen, nicht gegen den Berichtstext.

## 0 · Vorbedingung: Prüfgrundlagen-Bundle

Prüfe, dass vorliegen: der Bericht `docs/methodik/<nr>_*.md`, die Aufgabe, beide Arbeitsmappen
(`docs/Schadensbaum/*.xlsx`), die im Bericht referenzierten Anlagen (Skripte/CSVs) und das Ledger
`reviews/BEFUNDE_<nr>.md`. **Fehlt etwas: abbrechen** — ein Review ohne vollständiges Bundle ist
ungültig (§5). Liste, was fehlt.

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
unerklärte Formeln und Verteilungsfunktionen (§8: Prüfpunkte E1–E5, siehe unten),
Ressourcen-Regel-Verstoß (§3.4: geplanter nationaler 100-m-Vollraster-Lauf als
Prüfstein/Abgleich = Befund), fehlende Datenebenen-Spezifikation (§3.1-Anlagepflicht:
benötigte Zellgröße ohne „neu anzulegen"-Ebene bzw. „geparkt"-Watchlist = Befund),
verletzte Betrachtungsebene (§3.2: Zentrierungsmittel aus modellinterner Aggregation
über eine höhere Ebene = Befund),
Referenzwert-Doppelzählung, Quellen-Synchronität (LF 14).

### 2.1 · Erklärbarkeit (Vorgabe P3 — §8 der Aufgabe, Anweisung A-0034 vom 13.09.2026)

**Gewählter Weg:** Es tritt **keine** zusätzliche Leitfrage hinzu — die bestehende **Leitfrage 11
(„Form und Erklärbarkeit")** ist erweitert. Die Zahl der Leitfragen bleibt damit unverändert 14.

Beantworte im Rahmen von LF 11 die Prüfpunkte aus §8 **einzeln mit ja/nein und Fundstelle**;
jedes „nein" ist ein Befund (Kategorie B, sofern nicht zugleich ein A-Kriterium verletzt ist).
Adressat ist ein Berater eines Beratungshauses oder ein Sachbearbeiter einer Kommune — fachkundig,
aber ohne Statistikausbildung.

- **E1** Beginnt Abschnitt 3 mit der **Rechenkette** von der amtlichen Quelle bis zum Euro-Betrag — je Ebene
  Rechenschritt, Zahl für die Beispielkommune und Quelle, höchstens zehn Ebenen (mehr nur mit Begründung), vom
  Beispiel-Block nachgerechnet (Abschnitt 3.0)? Lässt sie sich einem Sachbearbeiter vorlesen, ohne dass ein Schritt fehlt?
- **E2** Jede Hauptformel mit Rechenbeispiel samt eingesetzten Zahlen und Zwischenwerten
  (Beispiel-Blöcke Abschnitt 3)?
- **E3** **Eine Methodik, nie zu einfach.** Steht jede Verteilungsfunktion oder Formel, die der Adressat nicht
  nachvollziehen kann, mit der Begründung da, **was die einfachere Rechnung an der Lage verfälschen würde**
  (Richtung und Größe, beziffert) und mit einem Rechenbeispiel? Umgekehrt: Stellt eine Vereinfachung die Lage falsch
  dar (Richtung, Rangfolge der Kommunen, Größenordnung)? Beides ist ein Befund. Ein Nebeneinander einer einfachen und
  einer belastbaren Fassung ist ebenfalls ein Befund — verworfene Varianten stehen mit je einem Satz im Entscheidungslog.
- **E4** Jedes Formelzeichen mit Klartext-Bedeutung und Einheit, jeder Fachbegriff bei erster
  Verwendung erklärt (Zeichentabellen Abschnitt 3, Parameter-Blöcke Abschnitt 7)?
- **E5** Schreibweise einheitlich nach `kap3-stil` (Beträge „1,2 Mio. €“, Leerzeichen vor % und Einheiten) —
  der Lint prüft es; hier nur übernehmen?

**So einfach wie möglich, so komplex wie nötig:** Eine Vereinfachung, die die Lage falsch darstellt, ist ein Befund —
genauso wie eine Komplexität ohne Begründung der Fehldarstellung oder eine unerklärt stehengelassene Formel. Still
vereinfacht wird nie. Nicht Stil bemängeln, sondern Nachvollziehbarkeit.

## 3 · Ledger und Regression

- **Rollenkette (Prüflauf des Managers, nur lesend):** Du schreibst nicht selbst. Deine neuen Befunde stehen nummeriert
  in der Begründung deines Urteils, je Befund eine Zeile im Ledger-Format; der `methodik_consultant` trägt sie in seiner
  nächsten Runde unverändert in `reviews/BEFUNDE_<nr>.md` ein, bevor er sie abarbeitet. Urteil `nacharbeit` bei neuen
  A-/B-Befunden, `freigabe` bei einer Null-Runde.
- **Einzelsitzung:** Neue Befunde **anhängen** an `reviews/BEFUNDE_<nr>.md`, Nummerierung fortlaufend, Format:
  Stelle · Art (Lücke/Fehler/Widerspruch) · Begründung · Vorschlag · Kategorie (A/B/C).
- **Regression:** Prüfe jeden als „übernommen" markierten Alt-Befund, ob die Lösung im aktuellen
  Stand noch trägt; Rückfälle als neuen Befund mit Verweis.
- Bei Re-Reviews: Fokus auf Diff + offene Befunde; **volle Prüfung erneut**, wenn Kalibrierung
  oder Modellstruktur geändert wurde.

## 4 · Konvergenz-Verdikt

Abschluss mit expliziter Aussage: Lints grün? Alle 14 Leitfragen mit Verdikt (LF 11 einschließlich
der Erklärbarkeits-Prüfpunkte E1–E5)? Neue A-/B-Befunde
in dieser Runde? → **Null-Runde ja/nein.** Bei „ja" zusätzlich gegen die Abnahmekriterien (§6)
prüfen und Abnahme-Empfehlung oder Restpunkte-Liste ausgeben.
