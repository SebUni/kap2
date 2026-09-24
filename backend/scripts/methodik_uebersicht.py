#!/usr/bin/env python3
"""Übersicht aller Methodik-Berichte — erzeugt, nicht von Hand gepflegt (Aufsichtsrat, 24.09.2026).

Je Bericht unter `docs/methodik/`: Stufe, Klimawirkung, Stand und Revision (aus der Statuszeile), ob Kapitel 3 mit der
Rechenkette beginnt (Aufgabe §4, §8 E1), offene Befunde je Kategorie und letzte Review-Runde aus der Prüfakte
`reviews/BEFUNDE_<nr>.md`, dazu die Exporte (PDF, Wirkungsmechanismus-HTML). Die Prüfakte bleibt getrennt von der
Kundenfassung; die Übersicht verlinkt nur. Schreibt `docs/methodik/README.md` — nach jedem Export neu
(`scripts/export_methodik_pdf.sh` ruft das Skript am Ende auf).

    python3 backend/scripts/methodik_uebersicht.py            # schreiben
    python3 backend/scripts/methodik_uebersicht.py --pruefe   # nur prüfen, ob die Datei aktuell ist (Rückgabe 1 sonst)
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

HIER = Path(__file__).resolve().parent
REPO = HIER.parent.parent
sys.path.insert(0, str(HIER))

import ledger  # noqa: E402

# M0 = Gesundheit (Hitze, Pollen, UV). Alle Methodiken werden ab M0 neu angefasst; M1 beginnt erst nach der Abnahme von
# M0 durch den Aufsichtsrat.
STUFEN = {"95": "M0", "96": "M0", "98": "M0"}
DATEI = "docs/methodik/README.md"


def _status(text: str) -> str:
    m = re.search(r"^Status:\s*(.+?)(?:\n\s*\n|\n>)", text, re.S | re.M)
    roh = " ".join((m.group(1) if m else "").replace("**", "").split())
    return roh


def _stand(status: str) -> str:
    gross = status.upper()
    teile = []
    rev = re.search(r"\bRev\.\s*(\d+)", status)
    if rev:
        teile.append(f"Rev. {rev.group(1)}")
    if "NICHT ABNAHMEREIF" in gross:
        teile.append("nicht abnahmereif")
    elif "ABNAHMEREIF" in gross:
        teile.append("abnahmereif")
    if "INTEGRIERT" in gross:
        teile.append("integriert")
    return ", ".join(teile) or (status[:60] + ("…" if len(status) > 60 else "")) or "—"


def _titel(text: str, nr: str) -> str:
    m = re.search(r"^# (.+)$", text, re.M)
    t = m.group(1).strip() if m else nr
    return re.sub(r"^Methodik-Bericht\s*#\d+\s*[—–-]\s*", "", t)


def _rechenkette(text: str) -> bool:
    kap3 = re.search(r"^## 3 .*?\n(.*?)(?=^## \d+ |\Z)", text, re.S | re.M)
    return bool(kap3 and re.search(r"^### [^\n]*Rechenkette", kap3.group(1), re.M))


def _pruefakte(pfad: Path) -> tuple[str, str]:
    if not pfad.exists():
        return "—", "—"
    befunde = ledger.parse(pfad)
    offen = {k: sum(1 for b in befunde if b.kat == k and b.lage in ("offen", "unklar")) for k in ("A", "B", "C")}
    runden = [int(x) for x in re.findall(r"^#+ [^\n]*?Runde (\d+)", pfad.read_text(encoding="utf-8"), re.M)]
    return f"{offen['A']}/{offen['B']}/{offen['C']}", (str(max(runden)) if runden else "—")


def erzeugen(repo: Path = REPO) -> str:
    docs = repo / "docs" / "methodik"
    zeilen = []
    for md in sorted(docs.glob("*.md"), key=lambda p: (p.name.split("_")[0].zfill(4), p.name)):
        nr = md.name.split("_")[0]
        if not nr.isdigit() or md.name == "README.md":
            continue
        text = md.read_text(encoding="utf-8")
        steckbrief = md.name.endswith("_steckbrief.md")
        offen, runde = _pruefakte(repo / "reviews" / f"BEFUNDE_{nr}.md")
        pdf, html = md.with_suffix(".pdf"), md.with_name(md.stem + "_wirkungsmechanismus.html")
        zeilen.append("| " + " | ".join([
            STUFEN.get(nr, "M1+"), f"#{nr}", f"[{_titel(text, nr)}]({md.name})" + (" (Steckbrief)" if steckbrief else ""),
            _stand(_status(text)), "—" if steckbrief else ("ja" if _rechenkette(text) else "**fehlt**"), offen, runde,
            f"[PDF]({pdf.name})" if pdf.exists() else "—", f"[HTML]({html.name})" if html.exists() else "—",
            f"[Prüfakte](../../reviews/BEFUNDE_{nr}.md)" if (repo / "reviews" / f"BEFUNDE_{nr}.md").exists() else "—"]) + " |")
    kopf = ["# Methodik-Berichte — Übersicht", "",
            f"Erzeugt von `backend/scripts/methodik_uebersicht.py` aus den Berichten, den Prüfakten (`reviews/`) und den "
            "Exporten — nicht von Hand ändern; `scripts/export_methodik_pdf.sh` erneuert die Datei nach jedem Export.", "",
            "Alle Methodiken werden ab **M0** (Gesundheit: #95, #96, #98) neu angefasst; **M1** beginnt erst nach der "
            "Abnahme von M0 durch den Aufsichtsrat (24.09.2026). Jeder Bericht beginnt Kapitel 3 mit der **Rechenkette** "
            "von der amtlichen Quelle bis zum Euro-Betrag (Aufgabe §4, §8 E1). Kundenfassung sind Bericht, PDF und "
            "Wirkungsmechanismus; die Prüfakte bleibt getrennt.", "",
            "| Stufe | Nr | Klimawirkung | Stand | Rechenkette | offene Befunde A/B/C | letzte Runde | PDF | Wirkungsmechanismus | Prüfakte |",
            "|---|---|---|---|---|---|---|---|---|---|"]
    return "\n".join(kopf + zeilen) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--pruefe", action="store_true", help="nur prüfen, ob docs/methodik/README.md aktuell ist")
    a = ap.parse_args()
    ziel = REPO / DATEI
    neu = erzeugen(REPO)
    if a.pruefe:
        aktuell = ziel.exists() and ziel.read_text(encoding="utf-8") == neu
        print(f"{DATEI}: {'aktuell' if aktuell else 'veraltet — python3 backend/scripts/methodik_uebersicht.py'}")
        return 0 if aktuell else 1
    ziel.write_text(neu, encoding="utf-8")
    print(f"geschrieben: {DATEI}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
