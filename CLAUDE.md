# Projekt-Kontext für Claude Code

## Verbindliche Instruktionsquelle

`docs/AUFGABE_METHODIK_SCHADENSRECHNUNG.md` (v2) ist die **einzige** Instruktionsquelle für
Herleitung, Review und Integration von Risiko-Methodiken (enthält die früheren Grundsätze G1–G14).
Bei jedem Methodik-Thema zuerst dort nachschlagen.

## Prüfgrundlagen-Bundle (Pfade)

- Aufgabe: `docs/AUFGABE_METHODIK_SCHADENSRECHNUNG.md`
- Wirkungsketten: `docs/Schadensbaum/KWRA-Schadensbaum_X_UBA-klimawirkungsketten.xlsx`
- Monetarisierung: `docs/Schadensbaum/KWRA-Monetarisierung.xlsx`
- Methodik-Berichte: `docs/methodik/<nr>_<slug>.md` (Markdown ist Quelle; PDF nur Export).
  Verzeichnis existiert noch nicht — es entsteht mit dem ersten `/neu-risiko`.
- Evidenz-Register (risikoübergreifend): `docs/evidenz/register.md` — existiert noch nicht,
  wird mit dem ersten Bericht angelegt.
- Befund-Ledger: `reviews/BEFUNDE_<nr>.md` — Verzeichnis `reviews/` existiert, ist noch leer.

### Sonderfall M0 (Gesundheit — vor dieser Konvention entstanden)

- Quelle ist **HTML, nicht Markdown**: `docs/render/METHODIK_M0_GESUNDHEIT.html`
  (KaTeX; PDF-Export via Playwright-Chromium nach `docs/METHODIK_M0_GESUNDHEIT.pdf`)
- Befund-Ledger/Gegenprüfung: `docs/METHODIK_M0_GESUNDHEIT_Gegenpruefung_Rev5.md`
- Ältere Review-PDFs: `docs/archiv/methodik-reviews/`

## Eiserne Regeln

1. **Markdown ist die Quelle, nie die PDF.** PDFs werden generiert, nicht editiert
   (beim Altbestand M0 ist die HTML-Render-Quelle in `docs/render/` maßgeblich).
2. **Arbeitsmappen nie still ändern oder überstimmen.** Bewusste Fortschreibungen gehören in
   die Quelle + Abgleich-Protokoll (Aufgabe §1/LF 14).
3. **Kein Parameter ohne Quelle** (Ratchet); kein Formelzeichen ohne Herleitung (§3.9).
4. **Review nur in frischer Session** — nie in der Session, die den Bericht geschrieben hat.
5. Divergenz Bericht ↔ Code wird nie still im Code gefixt: Befund ins Ledger.

## Workflow-Commands

- `/neu-risiko <nr>` — Erstaufschlag eines Methodik-Berichts aus den Arbeitsmappen
- `/review-methodik <nr>` — Gegenprüfung nach §5 (Lints + 14 Leitfragen) → Ledger
- `/integriere-risiko <nr>` — abgenommene Methodik → Registry, Schicht-B-Funktion, Tests

Loop: neu-risiko → (Autor füllt Register + Modell) → review-methodik (frische Session) →
Revision (Autor-Session, Ledger abarbeiten) → review-methodik … bis Null-Runde →
integriere-risiko.
