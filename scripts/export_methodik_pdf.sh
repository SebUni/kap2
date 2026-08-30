#!/usr/bin/env bash
# Exportiert einen Methodik-Bericht (Markdown-Quelle) als Lese-PDF.
# Pipeline: pandoc (Markdown → HTML, KaTeX-Formelsatz) → Playwright-Chromium (HTML → PDF),
# Optik angelehnt an docs/render/METHODIK_M0_GESUNDHEIT.html (scripts/methodik_report.css).
# Aufruf: scripts/export_methodik_pdf.sh <risiko-nr | pfad/zur/datei.md>
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ARG="${1:?Aufruf: export_methodik_pdf.sh <risiko-nr|md-pfad>}"

if [[ -f "$ARG" ]]; then
  MD="$(realpath "$ARG")"
else
  MD="$(ls "$ROOT"/docs/methodik/"$ARG"_*.md 2>/dev/null | head -1 || true)"
  [[ -n "$MD" ]] || { echo "FEHLER: Kein Bericht für '$ARG' unter docs/methodik/ gefunden." >&2; exit 1; }
fi

command -v pandoc >/dev/null || { echo "FEHLER: pandoc fehlt. Installieren: sudo apt install pandoc" >&2; exit 1; }

KATEX="$ROOT/frontend/node_modules/katex/dist"
[[ -f "$KATEX/katex.min.js" ]] || { echo "FEHLER: KaTeX fehlt unter $KATEX — im Ordner frontend/ 'npm install' ausführen." >&2; exit 1; }

# Python-Interpreter mit Playwright finden (Projekt-venvs, PATH, Playwright-CLI-Umgebung).
PY=""
for c in "$ROOT/.venv/bin/python" "$ROOT/backend/.venv/bin/python" python3 \
         "$(command -v playwright >/dev/null && dirname "$(command -v playwright)")/python"; do
  [[ -x "$c" || "$c" == python3 ]] || continue
  if "$c" -c 'import playwright' 2>/dev/null; then PY="$c"; break; fi
done
[[ -n "$PY" ]] || { echo "FEHLER: Kein Python mit Playwright gefunden. Installieren: pip install playwright && playwright install chromium" >&2; exit 1; }

OUT="${MD%.md}.pdf"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

{ echo '<style>'; cat "$ROOT/scripts/methodik_report.css"; echo '</style>'; } > "$TMP/head.html"

# H1 der Quelle wird per --shift-heading-level-by=-1 zum Dokumenttitel (Hero);
# keine Auto-Nummerierung, da die Berichte manuell nummerierte Abschnitte tragen.
pandoc "$MD" -o "$TMP/report.html" \
  --standalone --to html5 \
  --from markdown+pipe_tables+tex_math_dollars+tex_math_single_backslash \
  --shift-heading-level-by=-1 \
  --toc --toc-depth=2 \
  --katex="file://$KATEX/" \
  --include-in-header="$TMP/head.html" \
  -M document-css=false \
  -V lang=de-DE \
  --metadata date="$(date +%d.%m.%Y)"

"$PY" "$ROOT/scripts/html_to_pdf.py" "$TMP/report.html" "$OUT"

echo "PDF erzeugt: $OUT"
