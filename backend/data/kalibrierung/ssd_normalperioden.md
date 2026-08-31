# SSD-Normalperioden-Mittelraster (#98 §3.2, Zellebene)

Quelle: DWD-CDC Jahresraster sunshine_duration (1 km, GK3), 30 Jahre 1961–1990 und 30 Jahre 1991–2020.

- Rastergeometrie: 654×866 Zellen, 1000 m
- Flächenmittel SSD 1961–1990: **1544.0 h/Jahr**
- Flächenmittel SSD 1991–2020: **1664.7 h/Jahr**
- Flächenmittel der relativen Änderung: **+7.90 %** (Median +7.91 %, Spanne -4.86 … +20.91 %)

Abgleich mit der Gebietsmittel-Anlage `ssd_trend_region.csv` (DE +7,82 %): Die Rasterzahlen sind das FLÄCHEN-Mittel der Zellwerte, die CSV nutzt die DWD-Gebietsmittel-Zeitreihe — kleine Abweichungen sind erwartbar (unterschiedliche Aggregationswege), die Größenordnung muss übereinstimmen.

Verwendung: `app/services/climate/ssd_normalperioden.py` liest die Anlage und liefert `ssd_at(lon, lat)` → (SSD_ref, SSD_neu) je Zellstandort; Fallback bei fehlender Anlage/Position: Bundesland-Gebietsmittel aus `ssd_trend_region.csv` (Bericht §3.6).
