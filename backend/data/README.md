# Lokale Daten

## Zensus 2022 (100-m-Gitter)

Für Bevölkerungs- und Wohnindikatoren werden CSV-Extracts und Index-Dateien unter
`zensus/` erwartet. Sie sind nicht im Repository (zu groß).

Nach dem Klonen im Backend-Verzeichnis:

```bash
python -m app.cli zensus-download
```

Optional nur bestimmte Datensätze:

```bash
python -m app.cli zensus-download --keys population share_over_65
```

Die Dateien landen in `backend/data/zensus/extract/` und `backend/data/zensus/index/`.
