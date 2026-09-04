# KAP2

KAP2 ist eine Software für die vollständige Klimawirkungs- und Risikoanalyse deutscher Kommunen — von der automatischen Datenerhebung über die räumliche Risikobewertung auf dem 100-Meter-Raster bis zur priorisierten Anpassungsplanung mit Kosten und Nutzen in Euro. Die Analyse erfüllt die methodischen Anforderungen der DIN EN ISO 14091, der Klimawirkungs- und Risikoanalyse des Bundes (KWRA 2021, UBA) und der UBA-Empfehlungen für kommunale Klimarisikoanalysen und liefert damit die fachliche Grundlage, die das Bundes-Klimaanpassungsgesetz (KAnG) von Ländern und Kommunen verlangt. Die Risikoanalyse folgt der KWRA-Systematik des Bundes — relative Risikobewertung über Wirkungsketten —, die KAP2 um eine eigene Schadensfunktionsschicht ergänzt: Sie schätzt die Risiken zusätzlich als absolute Größen ab, als erwartete Jahresschäden in Euro, je Risiko, je Ortsteil, mit und ohne Anpassungsmaßnahmen. Jeder Modellparameter ist dabei einsehbar, mit zitierfähiger Quelle hinterlegt und kommunenspezifisch anpassbar, sodass die Analyse durch Gemeinderat, Fördermittelgeber und Fachöffentlichkeit prüfbar ist.

## Backend starten

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt

# DATABASE_URL setzen (Default: postgresql://kap2:kap2dev@localhost:5432/kap2)
export DATABASE_URL="postgresql://kap2:kap2dev@localhost:5432/kap2"

cd backend
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Alternativ: `./start-dev.sh` im Repo-Root startet Backend und Frontend zusammen
(erwartet eine virtuelle Umgebung unter `.venv/`).

## Frontend starten

```bash
cd frontend
npm install
npm run dev
```

Der Dev-Server läuft auf Port 5173 und proxyt Anfragen an `/api` auf das
Backend unter `http://localhost:8000`.

## Tests ausführen

```bash
cd backend
python -m pytest tests/ -q
```

## Weitere Dokumentation

- [`docs/BERECHNUNGS_HANDBUCH.md`](docs/BERECHNUNGS_HANDBUCH.md) — Berechnungslogik der Risiko- und Schadensmodelle
- [`docs/BETRIEB.md`](docs/BETRIEB.md) — RAM-Budget, Hintergrund-Prozesse, Caches, Migration/Upgrade
- [`docs/ROADMAP.md`](docs/ROADMAP.md) — geplante Weiterentwicklung
- [`CLAUDE.md`](CLAUDE.md) — Projekt-Kontext und Methodik-Workflow für Claude Code
