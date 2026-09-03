#!/usr/bin/env python3
"""Werkzeug für die Befund-Ledger (`reviews/BEFUNDE_<nr>.md`).

Hintergrund (Risiko 98, Runden 12-16): Der Ledger wurde bis Rev. 13 von Hand und per
Regex gepflegt. Dabei sind reproduzierbar zwei Fehlerklassen entstanden:

  * **Spaltenversatz** — Nachweise landeten in der Zeile des Nachbarbefunds
    (Befunde 319/320, 337). Begünstigt durch Nachweiszellen bis 4.612 Zeichen:
    bei solchen Zeilen ist visuell nicht mehr prüfbar, welche Zelle wohin gehört.
  * **Behauptete Umsetzung** — Status „übernommen" ohne tatsächliche Änderung
    (Runde 16: 9 von 17 Befunden). Der Autor benotet seine eigene Hausaufgabe;
    zwischen Befund und Status steht keine Maschine.

Dieses Werkzeug adressiert beides:

  --status    Übersicht je Kategorie und Status (liest, schreibt nicht).
  --kompakt   Einmal-Umbau: Volltext ins Archiv, aktiver Ledger auf eine Zeile je
              Befund gekürzt. Verifiziert danach nummernweise gegen das Original.
  --pruefe    Leitet den Status aus dem hinterlegten Prüfausdruck ab, statt ihn zu
              glauben. Ein Befund ohne Prüfausdruck gilt als offen.

Der Abgleich läuft grundsätzlich **über die Befundnummer, nie über die Zeilenposition** —
genau das macht den Spaltenversatz unmöglich.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
REVIEWS = REPO / "reviews"
ARCHIV = REVIEWS / "archiv"


# ---------------------------------------------------------------- Parsen


@dataclass
class Befund:
    nr: str
    text: str
    kat: str
    status: str
    nachweis: str
    bemerkung: str = ""
    zeile: int = 0
    tabelle: int = 0
    pruefausdruck: str = ""
    roh: str = field(default="", repr=False)

    @property
    def lage(self) -> str:
        """geschlossen · zurückgestellt · offen · unklar.

        Gelesen wird nur der Statusbereich (vor dem ersten Doppelpunkt), nicht die
        Nachweisprosa dahinter: Die enthält regelmäßig Wörter wie „offengelegt",
        die eine Substring-Suche über das ganze Feld falsch auf „offen" ziehen —
        real aufgetreten bei Ledger 95, Befund 76 („geschlossen (Integration …):
        Produktcode offengelegt" wurde als offen gelesen). Die Fälle stehen in
        SELBSTTEST und werden von `--selbsttest` geprüft.
        """
        # Konvention der Ledger: „STATUS: Nachweisprosa" bzw. „STATUS (Detail): …".
        # Nur der Teil vor dem ersten Doppelpunkt ist Status; dahinter steht Prosa,
        # die regelmäßig Wörter wie „offengelegt" und eigene „→" enthält.
        bereich = re.split(r":\s", self.status, maxsplit=1)[0]
        # Ein „→" im Statusbereich markiert einen Verlauf („wieder geöffnet → in
        # Rev. 4 neu geschlossen"); maßgeblich ist dann der Endzustand.
        kopf = re.split(r"[(]|—|–", bereich.split("→")[-1], maxsplit=1)[0].strip().lower()
        # Priorität: geschlossen schlägt offen. „wieder geöffnet → neu geschlossen"
        # ist geschlossen; „offen" allein bleibt offen.
        if re.search(r"geschlossen|gelöst|behoben|übernommen|umgesetzt|erledigt"
                     r"|gegenstandslos|entfällt|akzeptiert|bestätigt", kopf):
            return "geschlossen"
        if re.search(r"geöffnet|\boffen\b", kopf):
            return "offen"
        if re.search(r"zurückgestellt|terminiert|vertagt", kopf):
            return "zurückgestellt"
        return "unklar"

    @property
    def sortkey(self) -> tuple[int, int, str]:
        m = re.match(r"^(GP-)?(\d+)", self.nr)
        return (1 if self.nr.startswith("GP-") else 0, int(m.group(2)) if m else 9999, self.nr)


def _zellen(zeile: str) -> list[str]:
    """Zerlegt eine Markdown-Tabellenzeile in ihre Zellen.

    Splittet NUR an unmaskierten Trennzeichen (Befunde 381/382): Ein `\\|` im
    Zellinhalt — etwa in einem Prüfausdruck wie `grep -c '^\\| 3[12][0-9] …'` —
    gehört zum Text und darf die Zeile nicht zerlegen. Tut es das doch, bekommt
    die Zeile eine Zelle zu viel, der Prüfausdruck wird nicht mehr gefunden und
    die Status-Zelle rutscht: genau der Spaltenversatz, den dieses Werkzeug
    verhindern soll.
    """
    roh = zeile.strip().strip("|")
    zellen, puffer, i = [], [], 0
    while i < len(roh):
        if roh[i] == "\\" and i + 1 < len(roh) and roh[i + 1] == "|":
            puffer.append("|")       # maskiertes Trennzeichen: Text, kein Trenner
            i += 2
            continue
        if roh[i] == "|":
            zellen.append("".join(puffer).strip())
            puffer = []
            i += 1
            continue
        puffer.append(roh[i])
        i += 1
    zellen.append("".join(puffer).strip())
    return zellen


def _entfette(text: str) -> str:
    return re.sub(r"\*\*", "", text).strip()


# Ein Prüfausdruck wird ausgeführt. Der Ledger ist aber ein Textdokument, das
# Reviewer schreiben — deshalb wird nur ausgeführt, was mit einem dieser
# Kommandos beginnt. Ein Dateiname in Backticks (`ssd_povw.csv`) ist damit kein
# Kommando mehr, und ein `rm` im Fließtext wird nie ausgeführt.
ERLAUBTE_KOMMANDOS = ("grep", "rg", "test", "python3", "pytest", "git diff", "git grep")


def _ausdruck(zelle: str) -> str:
    """Holt das Prüfkommando aus der Spalte `Prüfausdruck`.

    Erwartet wird ein Kommando in Backticks, das mit einem Eintrag aus
    ERLAUBTE_KOMMANDOS beginnt. Ein Gedankenstrich, ein leeres Feld, Prosa ohne
    Backticks oder ein nicht freigegebenes Kommando zählen als **kein**
    Prüfausdruck — der Befund gilt dann als unbelegt. Ohne diese Strenge wäre die
    Spalte wieder nur Behauptung.
    """
    for m in re.finditer(r"`([^`]+)`", zelle):
        kandidat = m.group(1).strip()
        # Auf das erste TOKEN pruefen, nicht auf das Praefix: sonst gilt der
        # Testname `test_delta_dosis_uses_change_not_level` als Kommando `test`
        # und wird ausgefuehrt (real aufgetreten, Ledger-Zeile 213).
        # Fuehrende Shell-Negation ist legitim ("! grep -q X" = X kommt nicht vor)
        # und harmlos — sie darf den Kommando-Check nicht blockieren (Befund 350).
        teile = kandidat.split()
        if teile and teile[0] == "!":
            teile = teile[1:]
        kopf = teile[0] if teile else ""
        if kopf in ERLAUBTE_KOMMANDOS or kandidat.startswith(("git diff", "git grep")):
            return kandidat
    return ""


def tabellen(lines: list[str]) -> list[tuple[int, list[str], list[tuple[int, str]]]]:
    """Segmentiert die Datei in Tabellen: (kopfzeile, spaltennamen, [(zeilennr, roh)])."""
    out: list[tuple[int, list[str], list[tuple[int, str]]]] = []
    i = 0
    while i < len(lines):
        if not lines[i].lstrip().startswith("|"):
            i += 1
            continue
        kopf = _zellen(lines[i])
        start = i
        i += 1
        # Trennzeile (---) überspringen, falls vorhanden
        if i < len(lines) and re.match(r"^\|[\s:|-]+\|$", lines[i].strip()):
            i += 1
        body: list[tuple[int, str]] = []
        while i < len(lines) and lines[i].lstrip().startswith("|"):
            body.append((i + 1, lines[i]))
            i += 1
        out.append((start + 1, [_entfette(c) for c in kopf], body))
    return out


def ist_befundtabelle(spalten: list[str]) -> bool:
    """Befundtabellen tragen eine Status-Spalte; Kontrolltabellen ein 'Verdikt'."""
    joined = " ".join(spalten).lower()
    if "verdikt" in joined:
        return False
    return "status" in joined and ("kat" in joined or "befund" in joined)


def parse(pfad: Path, verlauf: bool = False) -> list[Befund]:
    """Liest alle Befundzeilen.

    Eine Befundnummer kommt über 16 Runden mehrfach vor: die Runden-Tabellen
    halten jeweils den **damaligen** Stand fest (Runde 9 führt z. B. Befund 252
    als „offen", die spätere Tabelle als geschlossen). Maßgeblich ist deshalb
    das **letzte** Vorkommen in der Datei — die Runden stehen chronologisch.
    Mit `verlauf=True` werden statt der Endstände alle Vorkommen geliefert.
    """
    lines = pfad.read_text(encoding="utf-8").split("\n")
    roh_liste: list[Befund] = []

    for kopfz, spalten, body in tabellen(lines):
        if not ist_befundtabelle(spalten):
            continue
        low = [s.lower() for s in spalten]

        def idx(*keys: str, default: int | None = None) -> int | None:
            for k in keys:
                for j, s in enumerate(low):
                    if k in s:
                        return j
            return default

        i_nr = idx("nr", "befund") or 0
        i_kat = idx("kat")
        i_st = idx("status")
        i_nw = idx("nachweis")
        i_txt = idx("befund (") if idx("befund (") is not None else (1 if i_nr == 0 else 0)
        i_bem = idx("begründung")
        i_pruef = idx("prüfausdruck")

        for zeilennr, roh in body:
            roh_zellen = _zellen(roh)
            cells = [_entfette(c) for c in roh_zellen]
            if not cells or cells[0].startswith("---"):
                continue
            m = re.match(r"^((?:GP-)?\d{1,3}(?:\s*[/–-]\s*\d{1,3})?(?:\s*\(≡[^)]*\))?)", cells[0])
            if not m:
                continue
            nr = re.sub(r"\s+", " ", m.group(1)).strip()
            key = nr.split(" (")[0]

            def get(j: int | None) -> str:
                return cells[j] if j is not None and j < len(cells) else ""

            kat = get(i_kat)[:1].upper()
            if kat not in ("A", "B", "C"):
                continue  # keine Befundzeile (z. B. Iterationstabelle)
            roh_liste.append(
                Befund(
                    nr=nr,
                    text=get(i_txt),
                    kat=kat,
                    status=get(i_st),
                    nachweis=get(i_nw),
                    bemerkung=get(i_bem),
                    # Rohzelle, NICHT entfettet (Befund 391): `_entfette()`
                    # entfernt Sternchenpaare und veraendert damit das
                    # auszufuehrende Kommando.
                    pruefausdruck=_ausdruck(roh_zellen[i_pruef]
                                            if i_pruef is not None
                                            and i_pruef < len(roh_zellen) else ""),
                    zeile=zeilennr,
                    tabelle=kopfz,
                    roh=roh,
                )
            )
    if verlauf:
        return roh_liste
    # Endstand je Nummer: letztes Vorkommen gewinnt (Status ändert sich über die
    # Runden). Der Befund**text** dagegen ist stabil und steht oft nur im ersten
    # Vorkommen — Zwischenstands-Tabellen führen die Nummer ohne Textspalte. Er
    # wird deshalb aus dem ersten aussagekräftigen Vorkommen übernommen.
    endstand: dict[str, Befund] = {}
    texte: dict[str, str] = {}
    for b in roh_liste:
        key = b.nr.split(" (")[0]
        endstand[key] = b
        if key not in texte and len(b.text) > 8:
            texte[key] = b.text
    for key, b in endstand.items():
        if len(b.text) <= 8 and key in texte:
            b.text = texte[key]
    return sorted(endstand.values(), key=lambda b: b.sortkey)


# ---------------------------------------------------------------- Kommandos


def cmd_status(pfad: Path) -> int:
    befunde = parse(pfad)
    print(f"{pfad.relative_to(REPO)} — {len(befunde)} Befunde, "
          f"{pfad.stat().st_size / 1024:.0f} KB\n")
    lagen = ("offen", "zurückgestellt", "geschlossen", "unklar")
    print(f"{'':4s} " + "".join(f"{l:>16s}" for l in lagen))
    for kat in ("A", "B", "C"):
        zeile = f"{kat:4s} "
        for lage in lagen:
            n = sum(1 for b in befunde if b.kat == kat and b.lage == lage)
            zeile += f"{n if n else '·':>16}"
        print(zeile)
    offen = [b for b in befunde if b.lage in ("offen", "unklar")]
    if offen:
        print(f"\nOffen/unklar ({len(offen)}):")
        for b in offen:
            print(f"  {b.nr:>7s}  {b.kat}  Z{b.zeile:<5d} {b.text[:88]}")
    laengste = max(befunde, key=lambda b: len(b.roh)) if befunde else None
    if laengste:
        print(f"\nLängste Befundzeile: {len(laengste.roh)} Zeichen (Nr {laengste.nr})")
    return 0


def _kurz(nachweis: str, grenze: int = 260) -> str:
    """Kürzt den Prosa-Nachweis auf die nachschlagbaren Referenzen."""
    n = re.sub(r"\s+", " ", nachweis).strip()
    if len(n) <= grenze:
        return n
    schnitt = n[:grenze]
    for trenn in ("; ", " · ", ", "):
        p = schnitt.rfind(trenn)
        if p > grenze * 0.5:
            return schnitt[:p] + " …"
    return schnitt.rstrip() + " …"


def cmd_kompakt(pfad: Path, runde: int) -> int:
    original = pfad.read_text(encoding="utf-8")
    befunde = parse(pfad)
    if not befunde:
        print("FEHLER: keine Befunde erkannt — Umbau abgebrochen.", file=sys.stderr)
        return 1

    nr = re.search(r"BEFUNDE_(\w+)\.md", pfad.name).group(1)
    ARCHIV.mkdir(exist_ok=True)
    archiv = ARCHIV / f"BEFUNDE_{nr}_R01-{runde:02d}_vollstaendig.md"

    # 1) Archiv: Volltext unverändert (Eiserne Regel 2 — nichts still entfernen).
    archiv.write_text(original, encoding="utf-8")
    if archiv.read_text(encoding="utf-8") != original:
        print("FEHLER: Archiv nicht byte-identisch.", file=sys.stderr)
        return 1

    offen = [b for b in befunde if b.lage in ("offen", "unklar")]
    zurueck = [b for b in befunde if b.lage == "zurückgestellt"]
    zu = [b for b in befunde if b.lage == "geschlossen"]

    # Karteileichen: Nummern, deren Lage über die Runden gewechselt hat und deren
    # letzter Eintrag aus einer Zwischenstands-Tabelle stammt. Sie werden
    # konservativ als offen geführt (im Zweifel offen), aber gekennzeichnet.
    verlauf = parse(pfad, verlauf=True)
    lagen: dict[str, list[Befund]] = {}
    for b in verlauf:
        lagen.setdefault(b.nr.split(" (")[0], []).append(b)
    wechsel = {k for k, v in lagen.items() if len({x.lage for x in v}) > 1}

    arel = archiv.relative_to(REVIEWS).as_posix()
    L: list[str] = []
    L.append(f"# Befund-Ledger #{nr} — UV-bedingte Gesundheitsschädigungen (insbesondere Hautkrebs)")
    L.append("")
    L.append(f"Aktiver Stand nach Review-Runde {runde}. Der **vollständige Verlauf der Runden 1–{runde}** "
             f"mit allen Prosa-Nachweisen, Lint-Protokollen und Konvergenz-Verdikten steht unverändert "
             f"im Archiv: [`{arel}`]({arel}).")
    L.append("")
    L.append("**Warum kompakt.** Der Ledger war auf 440 KB und Nachweiszellen bis 4.612 Zeichen "
             "gewachsen. Bei solchen Zeilen ist nicht mehr prüfbar, welche Zelle zu welchem Befund "
             "gehört — daraus sind die Spaltenversätze (Befunde 319/320, 337) entstanden, und die "
             "wachsende Prüffläche hat in jeder Runde neue Formbefunde erzeugt, während der "
             "Modellkern seit Runde 12 fünfmal unverändert bestätigt wurde. Gepflegt wird der Ledger "
             "ab jetzt ausschließlich über `backend/scripts/ledger.py` (Abgleich über die "
             "Befundnummer, nie über die Zeilenposition).")
    L.append("")
    L.append("**Statusregel.** `offen` · `zurückgestellt (Termin)` · `geschlossen`. Ein Befund gilt "
             "erst als geschlossen, wenn die Spalte **Prüfausdruck** einen maschinell auswertbaren "
             "Beleg trägt (`ledger.py --pruefe`). Ohne Prüfausdruck bleibt er offen — die "
             "Selbstauskunft des Autors reicht nicht.")
    L.append("")
    L.append("**Nummern-Konvention (unverändert).** Zeilen ohne Präfix tragen die Nummern der "
             "`Gegenpruefung_Rev5_Befundliste.md` (Fassung 4.0); Zeilen mit **GP-** die Nummern der "
             "Liste in `docs/METHODIK_M0_GESUNDHEIT_Gegenpruefung_Rev5.md`. Neue Befunde laufen ab 201.")
    L.append("")

    def zeilen_offen(rows: list[Befund]) -> None:
        L.append("| Nr | Kat. | Befund (Stelle · Kurzfassung) | Prüfausdruck | Status |")
        L.append("|---|---|---|---|---|")
        for b in rows:
            # Offene Befunde sind die Arbeitsliste der nächsten Runde und werden
            # deshalb ungekürzt übernommen; nur Geschlossenes wird zusammengefasst.
            txt = re.sub(r"\s+", " ", b.text).strip().replace("|", "\\|")
            mark = " ⚠︎" if b.nr.split(" (")[0] in wechsel else ""
            L.append(f"| {b.nr}{mark} | {b.kat} | {txt} | — | offen |")
        L.append("")

    def zeilen_zu(rows: list[Befund]) -> None:
        L.append("| Nr | Kat. | Status | Befund (Stelle · Kurzfassung) | Nachweis (Kurzform) |")
        L.append("|---|---|---|---|---|")
        for b in rows:
            txt = _kurz(b.text, 200).replace("|", "\\|")
            nw = _kurz(b.nachweis, 260).replace("|", "\\|")
            st = "zurückgestellt" if b.lage == "zurückgestellt" else "geschlossen"
            L.append(f"| {b.nr} | {b.kat} | {st} | {txt} | {nw} |")
        L.append("")

    if offen:
        L.append(f"## Offene Befunde ({len(offen)})")
        L.append("")
        if wechsel & {b.nr.split(" (")[0] for b in offen}:
            L.append("Mit **⚠︎** markierte Nummern sind **Karteileichen**: Ihre Lage hat über die "
                     "Runden gewechselt, und der letzte Eintrag stammt aus einer "
                     "Zwischenstands-Tabelle (Runde 9), nicht aus einer Schlusszeile. Die Sachfrage "
                     "wurde vermutlich unter einer späteren Nummer geschlossen, ohne dass der alte "
                     "Eintrag nachgezogen wurde. Sie werden **konservativ als offen geführt** — die "
                     "nächste Runde entscheidet je Nummer: schließen mit Prüfausdruck oder als "
                     "echter Restpunkt bestätigen.")
            L.append("")
        zeilen_offen(offen)

    if zurueck:
        L.append(f"## Zurückgestellte Befunde ({len(zurueck)})")
        L.append("")
        zeilen_zu(zurueck)

    L.append(f"## Geschlossene Befunde ({len(zu)})")
    L.append("")
    L.append(f"Kurzform. Der vollständige Umsetzungsnachweis je Befund steht im Archiv "
             f"[`{arel}`]({arel}) und ist dort über die Befundnummer auffindbar.")
    L.append("")
    zeilen_zu(zu)
    neu = "\n".join(L).rstrip() + "\n"

    pfad.write_text(neu, encoding="utf-8")

    # 2) Verifikation — nummernweise, nie positionsweise.
    nach = parse(pfad)
    vor_map = {b.nr.split(" (")[0]: b for b in befunde}
    nach_map = {b.nr.split(" (")[0]: b for b in nach}
    fehler: list[str] = []
    if set(vor_map) != set(nach_map):
        for k in sorted(set(vor_map) - set(nach_map)):
            fehler.append(f"Befund {k} im neuen Ledger verloren")
        for k in sorted(set(nach_map) - set(vor_map)):
            fehler.append(f"Befund {k} im neuen Ledger erfunden")
    for k, b in vor_map.items():
        n = nach_map.get(k)
        if n is None:
            continue
        if n.kat != b.kat:
            fehler.append(f"Befund {k}: Kategorie {b.kat} -> {n.kat}")
        if n.lage != b.lage:
            fehler.append(f"Befund {k}: Lage {b.lage} -> {n.lage}")

    print(f"Archiv : {archiv.relative_to(REPO)}  ({len(original)/1024:.0f} KB, byte-identisch)")
    print(f"Aktiv  : {pfad.relative_to(REPO)}  ({len(neu)/1024:.0f} KB, "
          f"-{100*(1-len(neu)/len(original)):.0f} %)")
    print(f"Befunde: {len(befunde)} vor · {len(nach)} nach  "
          f"(offen {len(offen)}, zurückgestellt {len(zurueck)}, geschlossen {len(zu)})")
    if fehler:
        print(f"\nVERIFIKATION ROT — {len(fehler)} Abweichung(en):", file=sys.stderr)
        for f in fehler[:40]:
            print(f"  {f}", file=sys.stderr)
        return 1
    print("\nVerifikation GRÜN: jede Befundnummer genau einmal, Kategorie und Lage unverändert.")
    return 0


def _schiefe_zeilen(text: str) -> list[tuple[int, int, int]]:
    """Zeilen, deren Zellenzahl nicht zur Kopfzeile passt (Befunde 391/401).

    Ein unmaskiertes Trennzeichen im Text verschiebt alle folgenden Zellen —
    Status und Pruefausdruck stehen dann nicht mehr dort, wo sie gesucht werden.
    Beide Kommandos muessen das melden: `--schliesse`, damit es nichts falsch
    schliesst, und `--pruefe`, weil dessen Ausgabe die Abnahme belegt. Fehlte die
    Pruefung dort, meldete es „GRUEN" fuer eine Zeile, deren echter Ausdruck rot war.
    """
    schief = []
    for _kopfz, spalten, body in tabellen(text.split("\n")):
        if not ist_befundtabelle(spalten):
            continue
        for zeilennr, roh in body:
            if len(_zellen(roh)) != len(spalten):
                schief.append((zeilennr, len(_zellen(roh)), len(spalten)))
    return schief


def cmd_pruefe(pfad: Path, streng: bool = False) -> int:
    """Leitet den Status aus dem Prüfausdruck ab, statt ihn zu glauben.

    Ein Prüfausdruck ist ein Shell-Kommando in Backticks in der Spalte `Prüfausdruck`.
    Exitcode 0 = Befund belegt geschlossen; alles andere = offen.
    """
    befunde = parse(pfad)
    schief = _schiefe_zeilen(pfad.read_text(encoding="utf-8"))
    rot: list[tuple[Befund, str]] = []
    gruen: list[Befund] = []
    # §6 laesst B-/C-Befunde auch TERMINIERT ZURUECKGESTELLT zu, und §5 kennt
    # „abweichend geloest mit Begruendung". Beides ist keine Behauptung, ein
    # Befund sei umgesetzt — ihr Pruefausdruck DARF rot sein, er beschreibt ja
    # den zurueckgestellten Sollzustand. Sie werden getrennt ausgewiesen, damit
    # der offene Rest sichtbar bleibt, statt als Fehler unterzugehen.
    zurueck = [b for b in befunde
               if b.lage == "zurückgestellt" or "abweichend" in b.status.lower()]
    zurueck_nr = {b.nr for b in zurueck}
    for b in befunde:
        if not b.pruefausdruck or b.nr in zurueck_nr:
            continue
        r = subprocess.run(b.pruefausdruck, shell=True, cwd=REPO,
                           capture_output=True, text=True)
        (gruen.append(b) if r.returncode == 0
         else rot.append((b, (r.stderr or r.stdout).strip()[:120] or f"exit {r.returncode}")))

    # Ein als geschlossen geführter Befund ohne Prüfausdruck ist unbelegt — genau
    # die Lage, aus der in Runde 16 neun nicht umgesetzte „übernommen" entstanden.
    unbelegt = [b for b in befunde if b.lage == "geschlossen" and not b.pruefausdruck]
    print(f"{pfad.relative_to(REPO)}: {len(befunde)} Befunde")
    if zurueck:
        print(f"  zurückgestellt/abw.: {len(zurueck):<4d} ({', '.join(sorted(b.nr for b in zurueck))})")
    print(f"  belegt geschlossen : {len(gruen)}")
    print(f"  Prüfausdruck ROT   : {len(rot)}")
    print(f"  unbelegt geschlossen: {len(unbelegt)}   <- Selbstauskunft, nicht geprüft")
    for b, msg in rot:
        print(f"  ROT  {b.nr:>9s}  {b.text[:64]}  -> {msg}")
    if unbelegt:
        print(f"\n  Ohne Prüfausdruck (Auszug): "
              f"{', '.join(b.nr for b in unbelegt[:12])}"
              f"{' …' if len(unbelegt) > 12 else ''}")
    # GELTUNGSBEREICH von W7: Die Pflicht zum Pruefausdruck gilt fuer Befunde, die
    # ab ihrer Einfuehrung (Runde 16) geschlossen werden — nicht rueckwirkend fuer
    # die 15 Runden davor. Nachtraeglich Ausdruecke zu diesen Altbefunden zu
    # erfinden waere genau die Behauptung, die W7 abschaffen soll; ihre
    # Nachweise stehen im Archiv und wurden im Review mehrfach gegengeprueft.
    # Rot ist deshalb nur ein FEHLSCHLAGENDER Ausdruck. Die Zahl der unbelegten
    # Altbefunde wird trotzdem ausgewiesen, damit der Bestand sichtbar bleibt.
    if schief:
        print(f"\n  STRUKTUR ROT: {len(schief)} Zeile(n) mit falscher Zellenzahl — "
              f"ihre Zellen sind verschoben, Status und Prüfausdruck stehen nicht "
              f"dort, wo sie gesucht werden:")
        for zn, ist, soll in schief[:10]:
            print(f"    Zeile {zn}: {ist} Zellen, Kopf hat {soll}")
    if rot or schief:
        print("\nROT — " + ("mindestens ein Prüfausdruck belegt seinen Befund nicht."
                            if rot else "die Tabellenstruktur trägt die Zusicherung nicht."))
        return 1
    print(f"\nGRÜN — kein Prüfausdruck schlägt fehl. {len(gruen)} Befunde maschinell "
          f"belegt, {len(unbelegt)} Altbefunde aus den Runden vor W7 tragen ihren "
          f"Nachweis nur im Archiv (`--streng` wertet auch diese als rot).")
    return 1 if (streng and unbelegt) else 0


# Statusvokabular, wie es in den Ledgern 95/96/98 tatsächlich vorkommt.
# Jeder Eintrag ist ein real aufgetretener Fall — die Liste wächst, wenn ein
# Reviewer eine neue Formulierung findet. Sie ist die Regressionssicherung
# gegen genau die Substring-Fehler, die den Spaltenversatz begünstigt haben.
SELBSTTEST: tuple[tuple[str, str], ...] = (
    ("offen", "offen"),
    ("offen — Vorschlag: Lint-Ausnahme entfernen", "offen"),
    ("übernommen", "geschlossen"),
    ("übernommen (Alternative des Vorschlags)", "geschlossen"),
    ("umgesetzt (Rev. 2)", "geschlossen"),
    ("abweichend gelöst", "geschlossen"),
    ("abweichend gelöst (Zwischenlösung)", "geschlossen"),
    ("gegenstandslos seit Rev. 2 (31.08.2026)", "geschlossen"),
    ("zurückgestellt (Termin: Rev. 3)", "zurückgestellt"),
    # Nachsatzprosa enthält „offengelegt" — darf nicht auf offen ziehen (Ledger 95/76):
    ("geschlossen (Integration 30.08.2026): Produktcode offengelegt", "geschlossen"),
    # Verlauf mit Pfeil: Endzustand zählt (Ledger 98, Befund 16):
    ("wieder geöffnet (Runde 6, Befund 230) → in Rev. 4 neu geschlossen", "geschlossen"),
    ("wieder geöffnet (Runde 9)", "offen"),
    # Pfeil steckt in der Nachweisprosa hinter dem Doppelpunkt (Ledger 95/78):
    ("behoben (Autor-Revision R4): Kennzeichnung präzisiert (Süd-Fit "
     "out-of-sample) + Vollreihe → 12/16, Länder identisch", "geschlossen"),
)


def cmd_selbsttest() -> int:
    fehler = []
    for text, erwartet in SELBSTTEST:
        got = Befund("x", "", "B", text, "").lage
        if got != erwartet:
            fehler.append((text, erwartet, got))
    for text, erw, got in fehler:
        print(f"  FAIL  {got:<15s} erwartet {erw:<15s} <- {text[:70]}", file=sys.stderr)
    print(f"Selbsttest Statuslogik: {len(SELBSTTEST) - len(fehler)}/{len(SELBSTTEST)} "
          f"{'GRÜN' if not fehler else 'ROT'}")
    return 1 if fehler else 0


def cmd_schliesse(pfad: Path) -> int:
    """Schliesst offene Befunde, deren Pruefausdruck gruen ist (W7).

    Der Status wird nicht gesetzt, sondern ABGELEITET: Nur was sein eigener
    Pruefausdruck belegt, gilt als geschlossen. Ohne Ausdruck oder mit rotem
    Ausdruck bleibt ein Befund offen.

    Gearbeitet wird **positionsunabhaengig**: `parse()` findet die Befundzeile,
    wo immer sie steht (Runden-Abschnitte am Dateiende eingeschlossen), und nur
    ihre Status-Zelle wird ersetzt. Zeilen werden nicht verschoben und Zellen
    nicht umsortiert — genau daraus sind die Spaltenversaetze entstanden.
    """
    text = pfad.read_text(encoding="utf-8")
    # Strukturkontrolle VOR dem Schliessen (Befund 391): Eine Zeile mit falscher
    # Zellenzahl hat ein unmaskiertes Trennzeichen im Text. Ihre Zellen sind
    # verschoben — Status und Pruefausdruck stehen dann nicht mehr dort, wo das
    # Werkzeug sie sucht. Frueher meldete es dafuer „kein Pruefausdruck" und
    # verschluckte den eigentlichen Fehler.
    schief = _schiefe_zeilen(text)
    schiefe_zeilen = {zn for zn, _, _ in schief}
    if schief:
        # Nicht abbrechen: Ein Formfehler in einer Zeile darf die uebrigen nicht
        # blockieren. Die betroffenen Zeilen werden aber NIE geschlossen — ihre
        # Zellen sind verschoben, Status und Pruefausdruck stehen nicht dort, wo
        # das Werkzeug sie sucht.
        print(f"WARNUNG: {len(schief)} Zeile(n) mit falscher Zellenzahl — "
              f"unmaskiertes Trennzeichen im Text; sie bleiben offen:",
              file=sys.stderr)
        for zn, ist, soll in schief[:10]:
            print(f"  Zeile {zn}: {ist} Zellen, Kopf hat {soll}", file=sys.stderr)

    offen = [b for b in parse(pfad) if b.lage in ("offen", "unklar")]
    if not offen:
        print("Keine offenen Befunde.")
        return 0

    geschlossen, bleibt = [], []
    for b in offen:
        if b.zeile in schiefe_zeilen:
            bleibt.append((b.nr, "Zeile strukturell fehlerhaft")); continue
        if not b.pruefausdruck:
            bleibt.append((b.nr, "kein Prüfausdruck")); continue
        r = subprocess.run(b.pruefausdruck, shell=True, cwd=REPO, capture_output=True)
        if r.returncode != 0:
            bleibt.append((b.nr, "Prüfausdruck rot")); continue
        cells = _zellen(b.roh)
        ziel = None
        for i, c in enumerate(cells):
            if _entfette(c).strip().lower() in ("offen", "**offen**"):
                ziel = i
                break
        if ziel is None:
            bleibt.append((b.nr, "keine Status-Zelle 'offen' gefunden")); continue
        cells[ziel] = "geschlossen"
        neu_zeile = "| " + " | ".join(cells) + " |"
        if b.roh not in text:
            bleibt.append((b.nr, "Zeile nicht mehr auffindbar")); continue
        text = text.replace(b.roh, neu_zeile, 1)
        geschlossen.append(b.nr)

    if not geschlossen:
        for nr, grund in bleibt:
            print(f"  offen ({grund}): {nr}")
        print("Nichts zu schliessen.")
        return 0

    pfad.write_text(text, encoding="utf-8")
    for nr, grund in bleibt:
        print(f"  offen ({grund}): {nr}")

    # Ueberschriften-Zahlen nachziehen, damit Kopf und Inhalt nicht auseinanderlaufen.
    nach = parse(pfad)
    n_offen = sum(1 for x in nach if x.lage in ("offen", "unklar"))
    n_zu = sum(1 for x in nach if x.lage == "geschlossen")
    t = pfad.read_text(encoding="utf-8")
    t = re.sub(r"## Offene Befunde \(\d+\)", f"## Offene Befunde ({n_offen})", t)
    t = re.sub(r"## Geschlossene Befunde \(\d+\)", f"## Geschlossene Befunde ({n_zu})", t)
    pfad.write_text(t, encoding="utf-8")

    vor = {x.nr.split(" (")[0] for x in parse_text(text)}
    ist = {x.nr.split(" (")[0] for x in parse(pfad)}
    print(f"\nGeschlossen: {len(geschlossen)} · noch offen: {n_offen}")
    if vor - ist:
        print(f"VERIFIKATION ROT — verlorene Nummern: {sorted(vor - ist)}", file=sys.stderr)
        return 1
    print("Verifikation GRÜN: keine Befundnummer verloren.")
    return 0


def parse_text(text: str) -> list[Befund]:
    """parse() auf einen String — fuer den Vorher/Nachher-Abgleich."""
    import tempfile
    with tempfile.NamedTemporaryFile("w", suffix=".md", encoding="utf-8",
                                     delete=False) as fh:
        fh.write(text)
        tmp = Path(fh.name)
    try:
        return parse(tmp)
    finally:
        tmp.unlink(missing_ok=True)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("nr", nargs="?", default="98", help="Risiko-Nummer, z. B. 98")
    ap.add_argument("--status", action="store_true", help="Übersicht (liest nur)")
    ap.add_argument("--kompakt", action="store_true", help="Volltext archivieren, Ledger kürzen")
    ap.add_argument("--pruefe", action="store_true", help="Status aus Prüfausdrücken ableiten")
    ap.add_argument("--selbsttest", action="store_true", help="Statuslogik gegen bekannte Fälle")
    ap.add_argument("--schliesse", action="store_true",
                    help="offene Befunde mit grünem Prüfausdruck schließen (W7)")
    ap.add_argument("--streng", action="store_true",
                    help="auch Altbefunde ohne Prüfausdruck als rot werten")
    ap.add_argument("--runde", type=int, default=16, help="letzte Review-Runde (für --kompakt)")
    a = ap.parse_args()

    if a.selbsttest:
        return cmd_selbsttest()
    pfad = REVIEWS / f"BEFUNDE_{a.nr}.md"
    if not pfad.exists():
        print(f"FEHLER: {pfad} nicht gefunden.", file=sys.stderr)
        return 1
    if a.kompakt:
        return cmd_kompakt(pfad, a.runde)
    if a.schliesse:
        return cmd_schliesse(pfad)
    if a.pruefe:
        return cmd_pruefe(pfad, a.streng)
    return cmd_status(pfad)


if __name__ == "__main__":
    raise SystemExit(main())
