# Projekt-Kontext für Claude Code

## Verbindliche Instruktionsquelle

`docs/AUFGABE_METHODIK_SCHADENSRECHNUNG.md` (v2) ist die **einzige** Instruktionsquelle für
Herleitung, Review und Integration von Risiko-Methodiken (enthält die früheren Grundsätze G1–G14).
Bei jedem Methodik-Thema zuerst dort nachschlagen.

## Prüfgrundlagen-Bundle (Pfade)

- Aufgabe: `docs/AUFGABE_METHODIK_SCHADENSRECHNUNG.md`
- Wirkungsketten: `docs/Schadensbaum/KWRA-Schadensbaum_X_UBA-klimawirkungsketten.xlsx`
- Monetarisierung: `docs/Schadensbaum/KWRA-Monetarisierung.xlsx`
- Methodik-Berichte: `docs/methodik/<nr>_<slug>.md` (Markdown ist Quelle; PDF und Wirkungsmechanismus-HTML
  nur Export, daneben abgelegt). Übersicht aller Berichte mit Stand und Links: `docs/methodik/README.md`
  (erzeugt von `backend/scripts/methodik_uebersicht.py`, nicht von Hand ändern).
- Evidenz-Register (risikoübergreifend): `docs/evidenz/register.md`.
- Befund-Ledger (Prüfakte, getrennt von der Kundenfassung): `reviews/BEFUNDE_<nr>.md`.
- M0 (#95, #96, #98) liegt seit der Migration als Markdown in `docs/methodik/`; die frühere HTML-Fassung
  `docs/render/METHODIK_M0_GESUNDHEIT.html` und `docs/METHODIK_M0_GESUNDHEIT_Gegenpruefung_Rev5.md` sind Altbestand,
  ältere Review-PDFs liegen unter `docs/archiv/methodik-reviews/`.

## Eiserne Regeln

1. **Markdown ist die Quelle, nie die PDF.** PDFs werden generiert, nicht editiert.
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
(neue Runde in der Rollenkette, im Einzelsitzungs-Weg `/aufsichtsrat-risiko-fortsetzen <nr>`), nie still im Code
gelöst und nie als Grund, die Vorgabe nicht umzusetzen.

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
- **P3 — Erklärbarkeit: eine Methodik, erzählbar als Rechenkette.** (Anweisung A-0034 vom 13.09.2026, neu gefasst
  vom Aufsichtsrat am 24.09.2026.) Adressat ist ein Berater eines Beratungshauses oder ein Sachbearbeiter einer
  Kommune — fachkundig, aber ohne Statistikausbildung. Jeder Bericht beginnt Kapitel 3 mit der **Rechenkette** von der
  amtlichen Quelle (etwa Zensus) bis zum Euro-Betrag: „Zahl aus Quelle × Faktor = Ergebnis“, höchstens zehn Ebenen,
  je Ebene Quelle und Zahl für eine Beispielkommune, vollständig von Anfang bis Ende und nicht ungenau. Am Ende steht
  **genau eine Methodik** je Risiko — kein Nebeneinander einer einfachen und einer komplexen Fassung. Sie ist **nie so
  einfach, dass das Ergebnis die Lage falsch darstellt**; wo es nicht einfach geht, wird sie komplexer und sagt an der
  Stelle, was die einfachere Rechnung verfälschen würde. Still vereinfacht wird nie. Geschrieben wird nach dem
  Stil-Skill `kap3-stil`. Prüfpunkte E1–E5 und Rechenketten-Format: Aufgabe §8 und §4; geprüft über Leitfrage 11
  (Aufgabe §5) und den Lint.

Prüfer prüfen Produkt-Tickets auch gegen P1, P2 und P3.

## Methodik in der Rollenkette (Aufsichtsrat, 24.09.2026)

Die Methodik entsteht in der Firma KAP3 in einer Rollenkette: Der **CEO** gibt sie an den **`cmo`**, der sie über alle
Berichte führt; je Risiko plant und prüft der **`methodik_manager`**, der **`methodik_consultant`** arbeitet aus;
integriert wird beim **`cto`**. Eine Runde ist ein Lauf des Consultant, geprüft vom Manager in frischer Sitzung, bis eine
Runde ohne Befund durchgeht; dann nimmt der Manager ab, der CMO übergibt an den CTO. Alle Methodiken werden ab M0 (#95,
#96, #98) neu angefasst; M1 beginnt erst nach der Abnahme von M0 durch den Aufsichtsrat.

## Workflow-Skills (`.claude/skills/`, benannt nach Rolle und Zweck)

- `/methodik_consultant-erstaufschlag <nr>` (früher `/neu-risiko`) — Erstaufschlag aus den Arbeitsmappen, mit Rechenkette
- `/methodik_manager-gegenpruefung <nr>` (früher `/review-methodik`) — Gegenprüfung nach §5 in frischer Sitzung
- `/methodik_manager-abnahme <nr>` (früher `/manager-review`) — fachliche Abnahme nach der Null-Runde
- `/methodik_consultant-export <nr>` (früher `/export-pdf`) — PDF, Wirkungsmechanismus-HTML, Übersicht
- `/cto-integration <nr>` (früher `/integriere-risiko`) — abgenommene Methodik → Registry, Schicht-B-Funktion, Tests
- `kap3-stil` — einheitliche Schreibweise (Zahlen, Einheiten, Begriffe) für alle Rollen
- `/entwickler-verify` (früher `/verify`) — KAP2 end-to-end im Browser prüfen

**Einzelsitzungs-Weg des Aufsichtsrats** (ohne Rollenkette, in einer Sitzung):
- `/aufsichtsrat-risiko-auto <nr>` (früher `/risiko-auto`) — voller **Erstdurchlauf** ohne Rückfragen
- `/aufsichtsrat-risiko-fortsetzen <nr> [Anlass]` (früher `/risiko-fortsetzen`) — **Wiedereinstieg**, wenn bei der
  Integration, im Betrieb oder durch eine Überstimmung Unklarheiten, offene Punkte oder Fehler auftauchen

Beide teilen sich mit der Rollenkette `.claude/methodik-loop.md` (Grundregel „keine Rückfragen", Entscheidungsregeln
W1–W7, L1 Revision → L2 Code-Nachzug → L3 Lints/Tests → L4 Review → L5 Loop → L6 PDF-/HTML-Export → L7 Statusbericht;
dort auch „Rollen im Loop"). Sie unterscheiden sich **nur** im Einstieg; Änderungen am Loop gehören in die gemeinsame
Datei.
