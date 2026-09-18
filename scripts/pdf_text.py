#!/usr/bin/env python3
"""Extrahiert Text aus PDF-Dateien seitenweise nach stdout.

Arbeitswerkzeug der Methodik- und Konformitätsarbeit (T-0351). Kein
Produktionscode, keine Abhängigkeit in backend/requirements*.txt.

Weg / Installation (Stand 18.09.2026):
    pip install --user --break-system-packages pypdf
Grund fuer --user --break-system-packages: der Container hat ein
"externally-managed" System-Python (PEP 668); ein venv wuerde die
Installation nicht ueber Shell-Grenzen hinweg verfuegbar machen, ein
User-Install unter --break-system-packages bleibt fuer den aktuellen
Nutzer dauerhaft importierbar ("python3 -c 'import pypdf'" laeuft dann
auch in einer frischen Shell durch). Auf einem frischen Container ist
der Schritt einmalig zu wiederholen:
    pip install --user --break-system-packages pypdf

Nutzung:
    python3 scripts/pdf_text.py <pfad-zu.pdf> [--seiten a-b|a]

Ohne --seiten werden alle Seiten ausgegeben. Seitenzahlen sind
1-basiert. Je Seite wird eine Kopfzeile "=== Seite <n> ===" gefolgt
vom extrahierten Text ausgegeben.
"""

import sys


def usage() -> str:
    return (
        "Benutzung: python3 scripts/pdf_text.py <pfad-zu.pdf> [--seiten a-b|a]"
    )


def parse_seiten(spec: str, letzte_seite: int) -> range:
    if "-" in spec:
        a_str, b_str = spec.split("-", 1)
        a, b = int(a_str), int(b_str)
    else:
        a = b = int(spec)
    if a < 1 or b < a:
        raise ValueError(f"ungueltiger Seitenbereich: {spec}")
    if b > letzte_seite:
        b = letzte_seite
    return range(a, b + 1)


def main(argv: list[str]) -> int:
    if not argv:
        print(usage(), file=sys.stderr)
        return 2

    pdf_pfad = None
    seiten_spec = None

    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg == "--seiten":
            if i + 1 >= len(argv):
                print(usage(), file=sys.stderr)
                return 2
            seiten_spec = argv[i + 1]
            i += 2
            continue
        if pdf_pfad is None:
            pdf_pfad = arg
            i += 1
            continue
        print(usage(), file=sys.stderr)
        return 2

    if pdf_pfad is None:
        print(usage(), file=sys.stderr)
        return 2

    try:
        import pypdf
    except ImportError:
        print(
            "Fehler: Modul 'pypdf' fehlt. Installation: "
            "pip install --user --break-system-packages pypdf",
            file=sys.stderr,
        )
        return 1

    try:
        reader = pypdf.PdfReader(pdf_pfad)
    except Exception as exc:  # Datei fehlt, kaputtes PDF etc.
        print(f"Fehler beim Oeffnen von '{pdf_pfad}': {exc}", file=sys.stderr)
        return 1

    anzahl_seiten = len(reader.pages)

    if seiten_spec is None:
        seiten = range(1, anzahl_seiten + 1)
    else:
        try:
            seiten = parse_seiten(seiten_spec, anzahl_seiten)
        except ValueError as exc:
            print(f"Fehler: {exc}", file=sys.stderr)
            return 2

    for n in seiten:
        print(f"=== Seite {n} ===")
        seite = reader.pages[n - 1]
        try:
            text = seite.extract_text() or ""
        except Exception as exc:
            text = f"[Fehler bei der Extraktion: {exc}]"
        print(text)

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
