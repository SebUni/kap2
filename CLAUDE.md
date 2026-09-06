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
3. **Kein Parameter ohne Quelle oder ausgewiesene Abschätzung** (Ratchet; Abschätzung nach §3.9
   „Abgeschätzt" und Vorgabe P1); kein Formelzeichen ohne Herleitung (§3.9).
4. **Review nur in frischer Session** — nie in der Session, die den Bericht geschrieben hat.
5. Divergenz Bericht ↔ Code wird nie still im Code gefixt: Befund ins Ledger.

## Vorgaben des Aufsichtsrats für das Produkt

Entscheidungen des Aufsichtsrats (Firmen-Repo `firma`, Freigabe F-0007, Meetings 05./06.09.2026).
Sie gehen den Methodik-Regeln vor; ein Widerspruch zu einer bestehenden Regel oder einem
abgenommenen Bericht wird als **bewusste Überstimmung im Befund-Ledger** geführt
(`/risiko-fortsetzen <nr>`), nie still im Code gelöst und nie als Grund, die Vorgabe nicht umzusetzen.

- **P1 — Parameterliste mit Quelle oder Abschätzung.** Das Produkt führt eine nutzersichtbare
  Parameterliste. Je Parameter steht dort entweder die Quelle oder der Vermerk, dass es eine
  begründete Abschätzung von KAP3 ist, samt Herleitung, wie sie zustande kommt. Gilt für alle
  Parameter (Defaults, Kostensätze, Wirkungsfaktoren). Eine Herleitung nur als Code-Kommentar
  erfüllt die Vorgabe nicht. (Aufgabe §3.6, §3.9)
- **P2 — Abschätzung statt Nullwirkung.** Für Maßnahmen ohne publizierte Effektgröße wird keine
  Wirkung null stehen gelassen, sondern eine begründete Abschätzung erarbeitet (Zahlenwert,
  Bandbreite, Sensitivität) und im Produkt klar als Abschätzung ausgewiesen. Bauform-Grenzen werden
  als Modellgrenze der Abschätzung dokumentiert. (Aufgabe §3.5; betrifft zuerst #96 S158
  Pollen-Frühwarnung.)

Prüfer prüfen Produkt-Tickets auch gegen P1 und P2.

## Workflow-Commands

- `/neu-risiko <nr>` — Erstaufschlag eines Methodik-Berichts aus den Arbeitsmappen
- `/review-methodik <nr>` — Gegenprüfung nach §5 (Lints + 14 Leitfragen) → Ledger
- `/integriere-risiko <nr>` — abgenommene Methodik → Registry, Schicht-B-Funktion, Tests
- `/risiko-auto <nr>` — voller **Erstdurchlauf** ohne Nutzer-Input: Erstaufschlag → Loop
- `/risiko-fortsetzen <nr> [Anlass]` — **Wiedereinstieg** ohne Nutzer-Input, wenn bei der
  Integration, im Betrieb oder durch eine Überstimmung methodische Unklarheiten, offene
  Punkte oder Fehler auftauchen: Triage → Anlass ins Ledger → Loop

Beide teilen sich `.claude/methodik-loop.md` (Grundregel „keine Rückfragen",
Entscheidungsregeln W1–W6, L1 Revision → L2 Code-Nachzug → L3 Lints/Tests → L4 Review →
L5 Loop → L6 PDF-/HTML-Export → L7 Statusbericht). Sie unterscheiden sich **nur** im Einstieg;
Änderungen am Loop gehören in die gemeinsame Datei, nicht in einen der beiden Commands.

Loop: neu-risiko → (Autor füllt Register + Modell) → review-methodik (frische Session) →
Revision (Autor-Session, Ledger abarbeiten) → review-methodik … bis Null-Runde →
integriere-risiko. Bricht die Integration ab oder taucht später ein Befund auf:
`/risiko-fortsetzen` — derselbe Loop, nur ab dem Ist-Stand statt vom Erstaufschlag.
