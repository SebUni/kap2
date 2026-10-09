# #96 Aeroallergene — Sichtprüfung Stadtbaumwahl und Betrag Berlin

Prüfakte zu T-1962-methodik_manager (09.10.2026), getrennt von der Kundenfassung. Gegenstand ist `docs/methodik/96_aeroallergene.md` §5. Gelesener Stand ist Commit `012afee1` (Runde 1), die Aufnahmen stammen aus Runde 0 (Commit `b8a58364`). Die Zeilenangaben gelten auch auf `39176a2c`, dem Merge von origin/main, auf dem diese Akte entstanden ist: Keine Datei, die hier mit Zeilennummer steht, hat sich seit `012afee1` geändert. Die Akte ist kein Nachweis „sichtbar fertig“ nach A-0066; den Betrag auf https://test.kap3.de misst der CEO nach dem Deploy.

## (1) Seitenleiste der Stadtbaumwahl, Warmsen

Aufgenommen am 09.10.2026 in Runde 0 auf dem Rechner firma-kap3 mit sichtpruefung.py. Das Probeverzeichnis /var/lib/overlord/supervisor/probe/T-1962-methodik_manager-entwicklerlauf-eapm4mot ist nach dem Lauf gelöscht, die Bilder sind nicht erhalten. Der Manager hat sie in Runde 0 gegen den Text geprüft.

Aufgenommen ist die Prüfmaßnahme „T-1962 Sichtprüfung Stadtbaumwahl“ (LOW_ALLERGEN_TREE_SELECTION, id 2) über die größte Fläche der Gemeindegrenze, mit anteil_ersetzt 0,2 und count 16.

Klickweg: Seite /app/massnahmen → „Meine Gebiete“ → „Warmsen“ → „81.6 km²“ → „Maßnahmen-Übersicht“ → „T-1962 Sichtprüfung Stadtbaumwahl“ → [title='Auf Karte zeigen'] in der Zeile T-1962 → Reiter „Karte“ → Zieltext.

### (a) Ersatzfall nicht gewählt

Bild: /var/lib/overlord/supervisor/probe/T-1962-methodik_manager-entwicklerlauf-eapm4mot/sicht4/1.png (ok: true).

Wörtlich auf dem Bild:

- „Ersatzfall“, „bitte wählen“
- „CAPEX (einmalig) –“
- „CAPEX bei Nachpflanzung ohnehin 960 €“ und „CAPEX bei vorgezogenem Ersatz 70.976 €“ (das ist capex_je_fall)
- kosten_vermerk: „Fall wählen: Nachpflanzung ohnehin oder vorgezogener Ersatz“
- „OPEX/Jahr 0 €“
- „Vermiedene Zusatztage/Jahr 0 Tage“, „Vermiedene Schäden / Nutzen 0 €“, „Abschätzung von KAP3“, „Richtung des Fehlers in λ nicht bestimmbar (Modellgrenze 7): …“

Die API-Antwort (POST /api/measures/2/calculate-impact) enthält capex_je_fall {"nachpflanzung": 960.0, "vorgezogen": 70976.0}, ersatzfall null und kosten_nutzen_kennzahl_offen true.

### (b) Ersatzfall Nachpflanzung, s_unbek für Warmsen auf 0,25 überschrieben

Bild: /var/lib/overlord/supervisor/probe/T-1962-methodik_manager-entwicklerlauf-eapm4mot/sicht5/1.png

Wörtlich auf dem Bild:

- „Ersatzfall“ „Nachpflanzung ohnehin“
- „CAPEX (einmalig) 960 €“
- „Der Nutzen je Jahr gilt erst mit voller Krone der sonst gepflanzten Bäume; Amortisation am Punktwert nach rund 24 Jahren (Bericht #96 §5)“
- „OPEX/Jahr 0 €“
- Hinweis zu s_unbek: „Die Überschreibung von s_unbek (0,12) gilt erst mit einem neuen Zelllauf; die Senkung rechnet mit s_unbek = 0,12 des Ausgangslaufs.“

Der direkte API-Aufruf im selben Zustand nennt dagegen „(0,25)“.

Ergänzend aus dem Ergebnis Runde 0, Punkt (1) (b), wörtlich:

- Vorher per API gesetzt: config ersatzfall=nachpflanzung, dazu Parameter risks.EXPECTED_ANNUAL_ALLERGY_DAYS.impact.birch_group_share_default=0,25 für Warmsen, mit custom_source.
- Im selben Zustand gibt der direkte API-Aufruf an denselben Endpunkt zweimal wörtlich aus: „Die Überschreibung von s_unbek (0,25) gilt erst mit einem neuen Zelllauf; die Senkung rechnet mit s_unbek = 0,12 des Ausgangslaufs.“

## (2) Wo der Jahresbetrag #96 steht

Der Sichtstart hat keine Daten für Berlin. Die Stelle der Oberfläche ist deshalb ausdrücklich an Warmsen gezeigt.

- Seite /app, Reiter „Dashboard“, Karte „Größte Schadenstreiber“, Zeile „Allergische Reaktionen durch Aeroallergene pflanzlicher Herkunft (#96)“, Betrag „2.300 €/a“.
- Bild: /var/lib/overlord/supervisor/probe/T-1962-methodik_manager-entwicklerlauf-eapm4mot/sicht7/1.png (Runde 0).

API-Endpunkt: GET /api/kommune/{kommune_id}/risk-summary (backend/app/api/routes/assessment.py Z. 268). Er liefert das Ergebnis von get_risk_aggregate(apply_measures=False), also von risk_engine.aggregate.

JSON-Pfad des angezeigten Betrags:

- `cost.klimawirkungen[]`, Eintrag mit `kwra_id` = 96 und `codes` = ["EXPECTED_ANNUAL_ALLERGY_DAYS"], Feld `cost_eur`.
- Im Frontend: RiskRadarSection.tsx Z. 259 und 267 (Auswahl), Z. 291 `fmtEurCompact(k.cost_eur)`/a.

Gleich groß sind:

- `cost.by_risk[]`, Eintrag mit `code` = EXPECTED_ANNUAL_ALLERGY_DAYS, Feld `cost_eur` (Anzeigewert `cost_display`; risk_engine.py Z. 389/395; Frontend Z. 257 als byRiskCode).
- `risks.EXPECTED_ANNUAL_ALLERGY_DAYS.cost_eur` (risk_engine.py Z. 340).

Wert für Berlin aus dem Zelllauf an den gepinnten Zelldaten (backend/data/kalibrierung/golden96_zellen_11000000.csv.gz) über risk_engine.aggregate: in allen drei Pfaden 2.474.857,71 € je Jahr (Preisstand 2024).

## (3) Beleg Berlin

Ausgeführt im Repo-Wurzelverzeichnis, ein Aufruf, ohne Hilfsdatei:

```
python3 -B -c "import os,sys; os.chdir('backend'); sys.path[:0]=['.','tests']; import test_methodik_96_golden_betraege as g; from app.services.engine import impact, risk_engine; gids,cis=g._zellen(g.BERLIN); bew=[ci for ci in cis if sum(float(ci['pop_age_bands'][k]) for k in g.BANDS)>0]; zellen=[{'risks':{g.CODE:impact.compute_all_cell_impacts(g._ctx({k:float(ci['pop_age_bands'][k]) for k in g.BANDS}))[g.CODE]},'inputs':{'pop':float(ci['pop'])}} for ci in bew]; agg=risk_engine.aggregate(zellen, sum(float(ci['pop']) for ci in cis), len(gids)*risk_engine.CELL_AREA_KM2); a=agg['risks'][g.CODE]['cost_eur']; b=[e['cost_eur'] for e in agg['cost']['by_risk'] if e['code']==g.CODE][0]; kw=[e for e in agg['cost']['klimawirkungen'] if g.CODE in e.get('codes',[])][0]; s=sum(z['risks'][g.CODE]['cost_eur'] for z in zellen); print('Zellen:',len(gids),'/ davon mit Einwohnern:',len(bew)); print('risks.%s.cost_eur: %.4f EUR' % (g.CODE,a)); print('cost.by_risk[code=%s].cost_eur: %.4f EUR' % (g.CODE,b)); print('cost.klimawirkungen[kwra_id=%s, codes=%s].cost_eur: %.4f EUR' % (kw.get('kwra_id'),kw.get('codes'),kw['cost_eur'])); print('Summe der Zell-cost_eur: %.4f EUR' % s); print('Differenz Betrag - Summe: %.6f EUR / innerhalb +-0,01 EUR: %s' % (a-s, abs(a-s)<=0.01))"
```

Ausgabe wörtlich, Runde 1 (09.10.2026, Rechner x360-1040-LX, System-python3, Stand `012afee1`):

```
Zellen: 40669 / davon mit Einwohnern: 40669
risks.EXPECTED_ANNUAL_ALLERGY_DAYS.cost_eur: 2474857.7100 EUR
cost.by_risk[code=EXPECTED_ANNUAL_ALLERGY_DAYS].cost_eur: 2474857.7100 EUR
cost.klimawirkungen[kwra_id=96, codes=['EXPECTED_ANNUAL_ALLERGY_DAYS']].cost_eur: 2474857.7100 EUR
Summe der Zell-cost_eur: 2474857.7133 EUR
Differenz Betrag - Summe: -0.003279 EUR / innerhalb +-0,01 EUR: True
```

Beide Zahlen:

- Betrag der Kommune: 2.474.857,71 €
- Summe der Zell-Euro: 2.474.857,7133 €
- Differenz: −0,0033 €, also innerhalb von ± 0,01 €. Sie kommt aus der Rundung des Betrags auf Cent in risk_engine.py Z. 312.

Die Zelleingaben baut der Golden-Test (_zellen, _ctx). Die Zellwerte rechnet das Produkt (impact.compute_all_cell_impacts), den Betrag bildet risk_engine.aggregate. Der Filter `bew` lässt keine Zelle weg: 40.669 von 40.669 Zellen haben Einwohner.

Wiederholung in Runde 2 (09.10.2026, Rechner firma-kap3, System-python3, Stand `39176a2c`): Derselbe Einzeiler bricht im Wurzelverzeichnis des Repos mit Exit-Code 1 ab. Ausgabe wörtlich:

```
Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File "/opt/overlord/kap2-supervisor/backend/tests/test_methodik_96_golden_betraege.py", line 40, in <module>
    from app.services import zensus_loader as zl  # noqa: E402
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/overlord/kap2-supervisor/backend/tests/../app/services/zensus_loader.py", line 18, in <module>
    from shapely.geometry import box
ModuleNotFoundError: No module named 'shapely'
```

Grund: Dem System-python3 auf firma-kap3 fehlt das Paket shapely, das backend/app/services/zensus_loader.py Z. 18 lädt. Der Abbruch liegt an der Umgebung, nicht an der Rechnung. Nach dem Nachtrag des Managers zu Runde 2 gilt deshalb die Ausgabe aus Runde 1. Seit `012afee1` hat kein Commit auf origin/main backend/app/services/engine, backend/tests/test_methodik_96_golden_betraege.py oder backend/data/kalibrierung berührt: `git log --oneline 012afee1..origin/main -- backend/app/services/engine backend/tests/test_methodik_96_golden_betraege.py backend/data/kalibrierung` gibt nichts aus (gemessen 09.10.2026 auf firma-kap3).

## (4) Abweichungen zwischen Produkt und Bericht §5

| Stelle im Bericht | Stelle im Produkt | Falsche Seite |
|---|---|---|
| docs/methodik/96_*.md §5, „Vorgabe für das Produkt (Befund 230)“, Z. 1551–1553 (Ü-10, Befund 252): Überschreibt die Kommune s_unbek nach dem Ausgangslauf, sagt ein Hinweis neben dem Betrag, dass der neue Wert erst mit einem neuen Zelllauf gilt. | Seitenleiste Stadtbaumwahl, Karte „Nutzen (jährlich)“, Feld stadtbaum_s_unbek_hinweis (frontend/src/components/MeasureSidebar.tsx Z. 409–413; Text aus backend/app/services/measure_service.py _stadtbaum_s_unbek_hinweis / _s_unbek_heute). Die Oberfläche nennt die Überschreibung „(0,12)“, gesetzt war 0,25; der direkte API-Aufruf nennt „(0,25)“. Ursache nicht geklärt. | Produkt (Oberfläche bzw. der Aufruf, den sie auslöst) |

Nur festgehalten, nichts behoben (eiserne Regel 5). Ins Ledger trägt es T-1926-cmo ein.

Ohne Abweichung geprüft:

- Abfrage des Falls, Z. 1425–1430
- 16 × 60 € = 960 € und 16 × 4.436 € = 70.976 €
- ohne gewählten Fall beide Beträge und keine Kosten-Nutzen-Kennzahl
- Hinweis zu voller Krone und 24 Jahren
- „Abschätzung von KAP3“ mit der Richtung des Fehlers in λ, Z. 1535–1537
- Summe der ungerundeten Zellwerte = Betrag der Kommune, Z. 1543–1545 (Beleg 3)

## Weitere Funde (nicht §5)

(a) `backend/data/kalibrierung/golden96_zellen.md`, Z. 5–6, nennt „Berlin 4,58 Mio. € je Jahr“; Golden-Test und Produkt rechnen 2.474.857,71 €.

(b) Der Sichtstart schreibt `finance_osm_*.json` über `finance_loader._write_cache` (`backend/app/services/finance_loader.py`, Z. 172 und 193–196) in das getrackte Verzeichnis `backend/data/inkar`.

Beide Funde sind nur festgehalten (eiserne Regel 5). Ins Ledger trägt sie T-1926-cmo ein, auf der Seite des Codes, mit Zuständigkeit cto und Termin 20.10.2026. Dasselbe gilt für die Abweichung zu s_unbek.
