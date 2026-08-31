"""Registry-Spezifikation der Schicht-B-Impact-Parameter (editierbar, override-fähig).

Reine Datenstruktur: ``parameter_registry`` baut daraus die Registry-Einträge mit den
IDs ``risks.<CODE>.impact.<key>`` (risikospezifisch) bzw. ``impact.<key>`` (global) und
löst ``source_refs`` gegen ``sources.py`` auf. So erscheinen die Parameter automatisch in
der Konfigurations-UI (Gruppe Klimarisiken), im Parameter-Excel und im Info-Tooltip —
ohne dass ``impact/*`` die Registry importieren muss (Zyklus-Vermeidung).

Jeder Eintrag: {risk (Code oder ""), key, value, label, unit, source, source_detail,
source_refs}. Die Defaults sind auf publizierte Größenordnungen kalibrierte, editierbare
Modellparameter (RKI/Winklmayr 2022; UBA MK3.1; GDV/BBK; Prognos 2023).
"""

from __future__ import annotations

_HEAT_AF = ("Nichtlineare attributable Fraktion AF = 1−exp(−β·(Hitzetage−Schwelle)+). "
            "β und Schwelle kalibriert auf die RKI-/Winklmayr-Größenordnung (~20 Hitzetage → "
            "~1 % hitzeattributable Sterblichkeit; ~4.500–8.700 Hitzetote/Jahr in DE).")

_ERF = ("Expositions-Wirkungs-Kurve nach Winklmayr u. a. 2022 (RKI): relatives "
        "Sterberisiko RR = exp(β·(Wochenmitteltemperatur − Schwelle)⁺), geschichtet "
        "nach vier Altersbändern und drei Regionen. Die Kurve wird über die Verteilung "
        "der Sommerwochen integriert, nicht am Mittelwert ausgewertet — das deutsche "
        "Sommermittel (~18,5 °C) liegt UNTER der Wirkschwelle, die Sterbefälle "
        "entstehen in den wenigen heißen Wochen.")

_BETA_FACTOR = (
    "Steigung dieses Altersbands relativ zum Band 85+. Nicht frei gewählt, sondern aus "
    "der publizierten Altersverteilung zurückgerechnet: Für kleine β·Δ gilt "
    "Todesfälle_a ∝ pop_a · m_a · β_a, also β_a ∝ Anteil_a / (pop_a · m_a). Mit den "
    "RKI-Anteilen 2026 (6,5/12,9/25,2/55,5 %) und den Sterbefällen 2023 je Band "
    "(138.024/166.312/302.921/420.949) ergeben sich die Faktoren 0,357/0,588/0,631/1,0 "
    "(Bericht #95 §3.3a, Rev. 6 — Kopplung an die Basissterberaten neu gerechnet). "
    "Kontrolle: Das Modell reproduziert die RKI-Altersverteilung auf <1 Prozentpunkt.")

_POLLEN_DS = (
    "Gemessene Spreizung der Birkengruppen-Saison zwischen den Klimanormalperioden "
    "1961–1990 und 1991–2020: Front-Marker Erle (Blüte Beginn) gegen Kern-Marker Birke "
    "(Blattentfaltung), gepaarte DWD-Phänologie-Stationen mit ≥ 8 Spannen-Jahren in "
    "beiden Perioden. Eine reine Verschiebung der Saison erzeugt KEINE Zusatztage — "
    "nur die Verlängerung tut das (Bericht #96 §3.1). Anlage "
    "backend/data/kalibrierung/pollensaison_region.csv, Skript dwd_pollensaison.py.")

_POLLEN_DS_G = (
    "Gemessene Sukzessions-Spreizung der Gräser-Saison (Wiesen-Fuchsschwanz → "
    "Wiesen-Knäuelgras, jeweils Vollblüte) zwischen 1961–1990 und 1991–2020; gepaarte "
    "DWD-Phänologie-Stationen. Das Saisonende bleibt konstant angesetzt (kein "
    "Phänologie-Marker) — dokumentierte Untergrenze. Anlage pollensaison_region.csv.")

_POLLEN_PAR = (
    "12-Monats-Prävalenz ärztlich diagnostizierter allergischer Rhinitis, "
    "bevölkerungsgewichtet auf die Produktbänder (Gewichte: Bevölkerung 31.12.2023 "
    "nach Altersjahren). Die auf eine Nachkommastelle gerundeten Bandwerte sind die "
    "verbindlichen Produktwerte (Bericht #96 §3.2, Befund 105).")

IMPACT_PARAM_SPECS: list[dict] = [
    # ── Hitzemortalität: Wirkschwellen je Region ───────────────────────────────
    {"risk": "EXPECTED_ANNUAL_MORTALITY", "key": "threshold_nord", "value": 19.7,
     "label": "Wirkschwelle Region Nord", "unit": "°C Wochenmittel",
     "source": "Winklmayr u. a. 2022, Abb. 3",
     "source_detail": "Wochenmitteltemperatur, ab der die Sterblichkeit in der Region Nord "
                      "(HB, HH, MV, NI, SH) messbar steigt. " + _ERF,
     "source_refs": ["Winklmayr_2022", "RKI_Hitzemortalitaet"]},
    {"risk": "EXPECTED_ANNUAL_MORTALITY", "key": "threshold_mitte", "value": 20.2,
     "label": "Wirkschwelle Region Mitte", "unit": "°C Wochenmittel",
     "source": "Winklmayr u. a. 2022, Abb. 3",
     "source_detail": "Wochenmitteltemperatur-Schwelle der Region Mitte (BE, BB, NW, RP, "
                      "SL, HE, SN, ST, TH). " + _ERF,
     "source_refs": ["Winklmayr_2022", "RKI_Hitzemortalitaet"]},
    {"risk": "EXPECTED_ANNUAL_MORTALITY", "key": "threshold_sued", "value": 20.8,
     "label": "Wirkschwelle Region Süd", "unit": "°C Wochenmittel",
     "source": "Winklmayr u. a. 2022, Abb. 3",
     "source_detail": "Wochenmitteltemperatur-Schwelle der Region Süd (BW, BY). Die "
                      "Schwelle steigt von Nord nach Süd — Ausdruck der Akklimatisierung. "
                      + _ERF,
     "source_refs": ["Winklmayr_2022", "RKI_Hitzemortalitaet"]},

    # ── Hitzemortalität: Kurvensteigung 85+ je Region ──────────────────────────
    {"risk": "EXPECTED_ANNUAL_MORTALITY", "key": "beta_85p_nord", "value": 0.0634,
     "label": "Kurvensteigung 85+ (Nord)", "unit": "1/K",
     "source": "Winklmayr u. a. 2022, Abb. 3/4",
     "source_detail": "Aus der publizierten Kurve für 2012–2021: RR ≈ 1,4 bei 25 °C, "
                      "bezogen auf die Nord-Schwelle 19,7 °C. Im Norden ist die Kurve am "
                      "steilsten. " + _ERF,
     "source_refs": ["Winklmayr_2022"]},
    {"risk": "EXPECTED_ANNUAL_MORTALITY", "key": "beta_85p_mitte", "value": 0.0625,
     "label": "Kurvensteigung 85+ (Mitte)", "unit": "1/K",
     "source": "Winklmayr u. a. 2022, Abb. 3/4",
     "source_detail": "Aus der publizierten Kurve: RR ≈ 1,35 bei 25 °C über der "
                      "Mitte-Schwelle 20,2 °C. " + _ERF,
     "source_refs": ["Winklmayr_2022"]},
    {"risk": "EXPECTED_ANNUAL_MORTALITY", "key": "beta_85p_sued", "value": 0.0876,
     "label": "Kurvensteigung 85+ (Süd)", "unit": "1/K",
     "source": "Winklmayr 2022 × Rev.-7-Nachschätzung (Bericht #95 §4)",
     "source_detail": "Ablesewert der publizierten Kurve 0,0531 (RR ≈ 1,25 bei 25 °C über "
                      "der Süd-Schwelle 20,8 °C) × Nachschätzungs-Skalar 1,65 aus dem "
                      "Holdout-Fit der Rev.-7-Kalibrierung (Fit ohne die Prüfjahre "
                      "2018/19/22; Profil-Band 1,45–1,85 ⇒ β-Band 0,0770–0,0982). "
                      "Modellinterner Kompensationsparameter — kehrt die publizierte "
                      "Regionen-Rangfolge um (§3.8-Widerspruch im Bericht benannt); der "
                      "Zell-Lauf prüft den Topographie-Anteil. " + _ERF,
     "source_refs": ["Winklmayr_2022", "RKI_EpidBull_19_2025"]},

    # ── Hitzemortalität: Altersband-Steigungsfaktoren ──────────────────────────
    {"risk": "EXPECTED_ANNUAL_MORTALITY", "key": "beta_factor_u65", "value": 0.357,
     "label": "Steigungsfaktor Band <65", "unit": "Faktor",
     "source": "Hergeleitet aus RKI-Altersverteilung", "source_detail": _BETA_FACTOR,
     "source_refs": ["RKI_Wochenbericht_Hitzemortalitaet", "Winklmayr_2022"]},
    {"risk": "EXPECTED_ANNUAL_MORTALITY", "key": "beta_factor_a65_74", "value": 0.588,
     "label": "Steigungsfaktor Band 65–74", "unit": "Faktor",
     "source": "Hergeleitet aus RKI-Altersverteilung", "source_detail": _BETA_FACTOR,
     "source_refs": ["RKI_Wochenbericht_Hitzemortalitaet", "Winklmayr_2022"]},
    {"risk": "EXPECTED_ANNUAL_MORTALITY", "key": "beta_factor_a75_84", "value": 0.631,
     "label": "Steigungsfaktor Band 75–84", "unit": "Faktor",
     "source": "Hergeleitet aus RKI-Altersverteilung", "source_detail": _BETA_FACTOR,
     "source_refs": ["RKI_Wochenbericht_Hitzemortalitaet", "Winklmayr_2022"]},
    {"risk": "EXPECTED_ANNUAL_MORTALITY", "key": "beta_factor_a85p", "value": 1.0,
     "label": "Steigungsfaktor Band 85+", "unit": "Faktor",
     "source": "Referenzband (Winklmayr u. a. 2022)",
     "source_detail": "Bezugsband der Kurvensteigung; die übrigen Bänder werden relativ "
                      "dazu skaliert. 85+ ist laut RKI die mit Abstand am stärksten "
                      "betroffene Gruppe (~55 % der hitzebedingten Sterbefälle bei ~3 % "
                      "Bevölkerungsanteil).",
     "source_refs": ["Winklmayr_2022"]},

    # ── Hitzemortalität: altersspezifische Basissterblichkeit ──────────────────
    {"risk": "EXPECTED_ANNUAL_MORTALITY", "key": "baseline_mort_u65", "value": 213.2,
     "label": "Basissterblichkeit <65", "unit": "Tote/100k·a",
     "source": "Destatis, Sterbefälle 2023 (Tab. 12613-03) ÷ Bevölkerung 31.12.2023",
     "source_detail": "Altersspezifische rohe Sterberate: 138.024 Sterbefälle u65 ÷ "
                      "64.747.448 EW = 213,2/100.000·a (Bericht #95 §3.5, Golden-Test "
                      "beispiel_95_basisraten). Ohne Altersdifferenzierung ist die "
                      "Altersverteilung der Hitzetoten nicht darstellbar — die 85+-Gruppe "
                      "hat die ~69-fache Basissterblichkeit der unter 65-Jährigen.",
     "source_refs": ["Destatis_Sterbefaelle_Altersgruppen"]},
    {"risk": "EXPECTED_ANNUAL_MORTALITY", "key": "baseline_mort_a65_74", "value": 1737.9,
     "label": "Basissterblichkeit 65–74", "unit": "Tote/100k·a",
     "source": "Destatis Todesursachenstatistik",
     "source_detail": "Altersspezifische rohe Sterberate des Bands 65–74.",
     "source_refs": ["Destatis_Sterbefaelle_Altersgruppen"]},
    {"risk": "EXPECTED_ANNUAL_MORTALITY", "key": "baseline_mort_a75_84", "value": 4812.3,
     "label": "Basissterblichkeit 75–84", "unit": "Tote/100k·a",
     "source": "Destatis Todesursachenstatistik",
     "source_detail": "Altersspezifische rohe Sterberate des Bands 75–84.",
     "source_refs": ["Destatis_Sterbefaelle_Altersgruppen"]},
    {"risk": "EXPECTED_ANNUAL_MORTALITY", "key": "baseline_mort_a85p", "value": 14800.2,
     "label": "Basissterblichkeit 85+", "unit": "Tote/100k·a",
     "source": "Destatis Todesursachenstatistik",
     "source_detail": "Altersspezifische rohe Sterberate des Bands 85+ — der mit Abstand "
                      "größte Treiber der absoluten Hitzemortalität.",
     "source_refs": ["Destatis_Sterbefaelle_Altersgruppen"]},

    # ── Hitzemortalität: Verteilungs- und Kalibrierparameter ───────────────────
    # weekly_temp_sd ENTFERNT (Rev. 7): Die Wochenverteilung kommt jetzt aus den
    # empirischen intra-saisonalen Anomalie-Quantilen je Region (Bericht #95 §3.2,
    # Anlage backend/data/kalibrierung/wochenquantile_region.csv; Konstanten in
    # impact/health.py REGION_WEEK_ANOMALIES) — gemessen statt Gauß-Annahme.
    # summer_weeks ENTFERNT (Rev. 7): Die 13 Sommerwochen (Juni–August) stecken
    # strukturell in den 13 empirischen Wochenquantilen (§3.2) — kein freier Parameter.
    {"risk": "EXPECTED_ANNUAL_MORTALITY", "key": "calibration", "value": 0.581,
     "label": "Nationaler Kalibrierfaktor", "unit": "Faktor",
     "source": "Rev.-7-Kalibrierung gegen die RKI-Jahresreihe (Bericht #95 §4)",
     "source_detail": "EINZIGER freier Niveau-Parameter der Hitzemortalität (§3.4: genau "
                      "ein nationaler Skalar; keine Pauschalkorrektur, keine "
                      "Regionalfaktoren). Kleinste Quadrate durch den Ursprung auf "
                      "bevölkerungsgewichteten Sommermittel-Reihen (DWD-JJA-Raster × "
                      "Gemeindepunkt × Zensus-Bevölkerung), Fenster 2012–2024, gegen die "
                      "revidierte RKI-Reihe (EB 19/2025). Band [0,55, 0,67] (Stützen: "
                      "ohne Süd-Nachschätzung 0,661; Vollreihe 0,660; Voll-Holdout 0,567; "
                      "s_Süd-Profilband 0,559–0,604). Kalibrier-Prüfstein: 12/16 Länder "
                      "im Band 0,75–1,35, auch in der Voll-Holdout-Variante. "
                      "Reproduzierbar: backend/scripts/kalibrierung/"
                      "calibrate_heat_mortality_rev7.py.",
     "source_refs": ["RKI_EpidBull_19_2025", "Winklmayr_2022"]},
    # healthcare_modifier_span ENTFERNT (Rev. 7): Der pauschale Versorgungszugangs-
    # Modifikator ist durch die evidenzbasierten, mittelwertzentrierten und bandweisen
    # v_vers-Faktoren ersetzt (β_iso 65+/β_pfl 85+; Bericht #95 §3.3); der Distanz-
    # Effekt ist Sensitivitätsband mit Basiswert 0 (beta_dist_km).

    # ── Hitzemortalität: v_vers-Modifikatoren (mittelwertzentriert, nur D-Pfad) ─
    {"risk": "EXPECTED_ANNUAL_MORTALITY", "key": "beta_iso", "value": 0.90,
     "label": "Isolations-Effekt β_iso (Bänder 65+)", "unit": "Faktor",
     "source": "Semenza 1996 (OR ≈ 2,3) / Mikrozensus 2023 (q̄ = 0,346)",
     "source_detail": "OR-Übersetzung über das Bevölkerungsmittel: β = (OR−1)/[1+q̄·(OR−1)] "
                      "= 1,3/1,4498 = 0,90 (Band 0,3–1,4). Wirkt mittelwertzentriert "
                      "1+β·(q_1P − q̄) nur in den Bändern 65+ und nur auf die Mortalität "
                      "(für Einweisungen keine Evidenz — Bericht #95 §3.3, Log 28). "
                      "Zellwert q_1P: Ebene SINGLE_HH_SHARE_65P ist GEPARKT (keine "
                      "offene Zellquelle, §3.1-Watchlist) → Zelle rechnet mit q̄ "
                      "(Faktor 1, kalibrierneutral).",
     "source_refs": ["Semenza_1996_Chicago",
                     "Destatis_Mikrozensus_2023_Einpersonenhaushalte"]},
    {"risk": "EXPECTED_ANNUAL_MORTALITY", "key": "beta_pfl", "value": 1.54,
     "label": "Pflegeheim-Effekt β_pfl (nur 85+)", "unit": "Faktor",
     "source": "Fouillet 2006 / Pflegestatistik 2023 (Kette Bericht #95 §3.3b)",
     "source_detail": "OR Heim vs. Nicht-Heim ≈ 3,0 aus Exzess-Verhältnis 1,0 (Fouillet "
                      "Tab. 2: O/E Heime 1,9 = Wohnung ≥75) × Basissterblichkeits-"
                      "Verhältnis 2,97 (Heim 0,34/a vs. Nicht-Heim-85+ 0,1144/a); "
                      "Übersetzung β = (3,0−1)/[1+0,149·2,0] = 1,54 (Band 1,0–2,9; "
                      "Stützen Bouchama 2007, Klenk 2010). Wirkt mittelwertzentriert "
                      "1+β·(q_pfl − q̄) nur im Band 85+ und nur auf die Mortalität "
                      "(Gegenevidenz für Einweisungen). Zellwert q_pfl: Ebene "
                      "CARE_HOME_SHARE_85P (OSM-Pflegeeinrichtungen, kommunen-"
                      "erwartungstreu auf q̄ normiert — Rev. 8 §3.6); Kommunen ohne "
                      "OSM-Heim rechnen mit q̄ (Faktor 1, kalibrierneutral).",
     "source_refs": ["Fouillet_2006_Frankreich", "Destatis_Pflegestatistik_2023",
                     "Bouchama_2007_Meta", "Klenk_2010_Heime"]},
    {"risk": "EXPECTED_ANNUAL_MORTALITY", "key": "qbar_1p", "value": 0.346,
     "label": "Bundesmittel Allein-Lebende 65+ (q̄_1P)", "unit": "Anteil",
     "source": "Mikrozensus 2023 (Indikator 132088)",
     "source_detail": "Anteil der ab 65-Jährigen in Einpersonenhaushalten: 34,6 % "
                      "(Mikrozensus 2023, Erstergebnisse). Zentrierungsmittel des "
                      "β_iso-Terms — Bundesmittel ⇒ Faktor exakt 1 (kalibrierneutral, "
                      "§3.2-Zentrierungsregel des Berichts).",
     "source_refs": ["Destatis_Mikrozensus_2023_Einpersonenhaushalte"]},
    {"risk": "EXPECTED_ANNUAL_MORTALITY", "key": "qbar_pfl", "value": 0.149,
     "label": "Bundesmittel Heimbewohner-Anteil 85+ (q̄_pfl)", "unit": "Anteil",
     "source": "Pflegestatistik 2023 / Bevölkerung 31.12.2023 (424.300 ÷ 2.844.213)",
     "source_detail": "Vollstationär versorgte 85+ (218,7+142,6+63,0 Tsd. = 424.300) ÷ "
                      "Bevölkerung 85+ (2.844.213) = 0,149. Zentrierungsmittel des "
                      "β_pfl-Terms (Golden-Test beispiel_95_or_uebersetzungen).",
     "source_refs": ["Destatis_Pflegestatistik_2023"]},
    {"risk": "EXPECTED_ANNUAL_MORTALITY", "key": "beta_dist_km", "value": 0.0,
     "label": "Distanz-Effekt (Sensitivität)", "unit": "1/km",
     "source": "Nicholl u. a. 2007 (Sensitivitätsband, Basiswert 0)",
     "source_detail": "≈ +1 % Mortalität je +10 km Krankenhausdistanz (Nicholl u. a., "
                      "Emerg Med J 24:665–668, 2007, doi:10.1136/emj.2007.047654 — "
                      "transportierte Notfälle, UK). Hitzetote versterben überwiegend zu "
                      "Hause; Übertragbarkeit zu schwach für den Basiswert → "
                      "Sensitivitätsband 0–0,002, Basiswert 0 (Bericht #95, Log 20). "
                      "Kein Archiv-Snapshot möglich (Verlag blockt Wayback-Save; "
                      "dokumentiert).",
     "source_refs": []},

    # ── Hitzemortalität: Restlebenserwartung je Band (YLL-Bewertung, §3.5) ─────
    {"risk": "EXPECTED_ANNUAL_MORTALITY", "key": "life_years_u65", "value": 23.39,
     "label": "Restlebenserwartung <65", "unit": "Jahre",
     "source": "Destatis Sterbetafeln 2022/2024, Stützstelle e(60)",
     "source_detail": "Verlorene Lebensjahre je Sterbefall im Band u65: Stützstelle "
                      "e(60) — 86 % der u65-Sterbefälle entfallen auf 50–64; "
                      "Geschlechter-Kombination mit der Bevölkerung 31.12.2023 "
                      "(Bericht #95 §3.5, Anker #l-a).",
     "source_refs": ["Destatis_Sterbetafeln_2022_2024"]},
    {"risk": "EXPECTED_ANNUAL_MORTALITY", "key": "life_years_a65_74", "value": 15.59,
     "label": "Restlebenserwartung 65–74", "unit": "Jahre",
     "source": "Destatis Sterbetafeln 2022/2024, Stützstelle e(70)",
     "source_detail": "Verlorene Lebensjahre je Sterbefall im Band 65–74 (Stützstelle "
                      "e(70), m/w bevölkerungsgewichtet; Bericht #95 §3.5).",
     "source_refs": ["Destatis_Sterbetafeln_2022_2024"]},
    {"risk": "EXPECTED_ANNUAL_MORTALITY", "key": "life_years_a75_84", "value": 8.90,
     "label": "Restlebenserwartung 75–84", "unit": "Jahre",
     "source": "Destatis Sterbetafeln 2022/2024, Stützstelle e(80)",
     "source_detail": "Verlorene Lebensjahre je Sterbefall im Band 75–84 (Stützstelle "
                      "e(80), m/w bevölkerungsgewichtet; Bericht #95 §3.5).",
     "source_refs": ["Destatis_Sterbetafeln_2022_2024"]},
    {"risk": "EXPECTED_ANNUAL_MORTALITY", "key": "life_years_a85p", "value": 4.16,
     "label": "Restlebenserwartung 85+", "unit": "Jahre",
     "source": "Sterbetafeln 2022/2024 × Sterbefälle 2023 (exakt; Bericht #95 Rev. 8)",
     "source_detail": "EXAKT sterbefallgewichtet (Rev. 8, löst Befund 22): reale "
                      "Sterbefälle 2023 nach Einzelaltersjahren 85–94 × e(x); 95+-Rest "
                      "mit tafelintern gewichtetem ē(95+); m/w mit Sterbefällen "
                      "kombiniert (161.178 M / 259.771 F) = 4,16 (Band [4,16, 4,20]: "
                      "Obergrenze mit e(95)-Stützstelle). Ersetzt den Rev.-7-Wert 5,44 "
                      "(Bevölkerungsgewichte + Untergrenzen-Stützstellen — beide Fehler "
                      "wirkten aufwärts). Reproduzierbar: backend/scripts/kalibrierung/"
                      "l85_sterbefallgewichtung.py; Golden-Test beispiel_95_basisraten.",
     "source_refs": ["Destatis_Sterbetafeln_2022_2024",
                     "Destatis_Sterbefaelle_Altersgruppen"]},

    # ── Hitzemorbidität (Rev. 7: F = Σ_a pop_a · r_0,a/100k · max(0, 1+e_HD·(HD−HD_ref))) ─
    {"risk": "EXPECTED_ANNUAL_MORBIDITY", "key": "r0_u65", "value": 1.9,
     "label": "Baseline-Einweisungsrate <65", "unit": "Fälle/100k·a",
     "source": "Destatis T67 + Karlsson & Ziebarth (Herleitung Bericht #95 §3.4)",
     "source_detail": "Gesamtrate 3,54/100k·a = T67-Kern 1,68 (Ø ≈ 1.400/a ÷ 83,456 Mio.) "
                      "+ Kreislauf-Kern 1,21–2,66 (11,9 % des Einweisungs-Exzesses je "
                      "Hitzetag × 7,2 Tage). Altersaufteilung 1,9/6,3/10,8/15,6 "
                      "(= 1:3,3:5,7:8,2) — gekennzeichnete Abschätzung am Steilheits"
                      "muster der Kreislauf-Morbidität; Band ×0,6–1,6 (Golden-Tests "
                      "beispiel_95_r0_kette/_normierung).",
     "source_refs": ["Destatis_T67_Hitzeeinweisungen", "Karlsson_Ziebarth_2018",
                     "Karlsson_Ziebarth_IZA_DP7875"]},
    {"risk": "EXPECTED_ANNUAL_MORBIDITY", "key": "r0_a65_74", "value": 6.3,
     "label": "Baseline-Einweisungsrate 65–74", "unit": "Fälle/100k·a",
     "source": "Destatis T67 + Karlsson & Ziebarth (Herleitung Bericht #95 §3.4)",
     "source_detail": "Band 65–74 der altersgeschichteten Baseline (Herleitung s. r0_u65; "
                      "bevölkerungsgewichtete Summe = 3,54/100k·a).",
     "source_refs": ["Destatis_T67_Hitzeeinweisungen", "Karlsson_Ziebarth_2018"]},
    {"risk": "EXPECTED_ANNUAL_MORBIDITY", "key": "r0_a75_84", "value": 10.8,
     "label": "Baseline-Einweisungsrate 75–84", "unit": "Fälle/100k·a",
     "source": "Destatis T67 + Karlsson & Ziebarth (Herleitung Bericht #95 §3.4)",
     "source_detail": "Band 75–84 der altersgeschichteten Baseline (Herleitung s. r0_u65).",
     "source_refs": ["Destatis_T67_Hitzeeinweisungen", "Karlsson_Ziebarth_2018"]},
    {"risk": "EXPECTED_ANNUAL_MORBIDITY", "key": "r0_a85p", "value": 15.6,
     "label": "Baseline-Einweisungsrate 85+", "unit": "Fälle/100k·a",
     "source": "Destatis T67 + Karlsson & Ziebarth (Herleitung Bericht #95 §3.4)",
     "source_detail": "Band 85+ der altersgeschichteten Baseline (Herleitung s. r0_u65).",
     "source_refs": ["Destatis_T67_Hitzeeinweisungen", "Karlsson_Ziebarth_2018"]},
    {"risk": "EXPECTED_ANNUAL_MORBIDITY", "key": "excess_per_hotday", "value": 0.024,
     "label": "Mehr-Einweisungen je Hitzetag (e_HD)", "unit": "1/Hitzetag",
     "source": "Karlsson & Ziebarth 2018, Tab. 1 (konditional)",
     "source_detail": "Relativer Einweisungs-Exzess je zusätzlichem Hitzetag (> 30 °C): "
                      "konditional +2,4 % (Basiswert; misst den marginalen Effekt), "
                      "Band 0,024–0,061 (unkonditional 0,054, Hitzewellentag 0,061). "
                      "HD-Term zweiseitig linear, bei 0 gedeckelt (HD = 0 → Faktor "
                      "0,83) — bevölkerungsgewichtet erwartungstreu um die Referenz, "
                      "keine Doppelzählung des in r_0 enthaltenen Durchschnittseffekts "
                      "(Bericht #95 §3.4, Befund 59). Harvesting steckt bereits in den "
                      "K&Z-Jahresaggregaten. Keine Modifikatoren im F-Pfad (Gegen-/"
                      "fehlende Evidenz, Log 28).",
     "source_refs": ["Karlsson_Ziebarth_2018", "Karlsson_Ziebarth_IZA_DP7875"]},
    {"risk": "EXPECTED_ANNUAL_MORBIDITY", "key": "hotday_ref_days", "value": 7.2,
     "label": "Referenz-Hitzetage HD_ref", "unit": "Tage/Jahr",
     "source": "Karlsson & Ziebarth 2018 (Panel-Basisperiode 1999–2008)",
     "source_detail": "Bundesmittel der Hitzetage (Tmax > 30 °C) der K&Z-Beobachtungs"
                      "periode — die Hitzetag-Last, unter der die Baseline r_0 gemessen "
                      "wurde; verhindert Doppelzählung des Durchschnittseffekts "
                      "(Bericht #95 §3.4, Anker #hd-ref). Räumlich konstanter Parameter; "
                      "HD der Zelle: DWD-CDC hot_days (1 km), ohne UHI-Verschiebung "
                      "(dokumentierte Unterschätzung in UHI-Lagen).",
     "source_refs": ["Karlsson_Ziebarth_2018", "Karlsson_Ziebarth_IZA_DP7875"]},

    # ── #96 Aeroallergene: klimaattribuierte Symptomtage (Bericht Rev. 1) ──────
    # δ_R = f · (p_B·ΔS_B,R + p_G·ΔS_G,R) · a_attr;  ΔTage = B · δ_R · P̂
    {"risk": "EXPECTED_ANNUAL_ALLERGY_DAYS", "key": "delta_s_birke_nord", "value": 3.96,
     "label": "Saison-Spreizung Birkengruppe (Nord)", "unit": "Tage",
     "source": "DWD-Phänologie, gepaarte Stationen (Bericht #96 §3.1)",
     "source_detail": _POLLEN_DS + " Nord: 257 Stationenpaare.",
     "source_refs": ["DWD_CDC_Phaenologie", "Bergmann_2023_RKI_Allergie_Klima"]},
    {"risk": "EXPECTED_ANNUAL_ALLERGY_DAYS", "key": "delta_s_birke_mitte", "value": 4.20,
     "label": "Saison-Spreizung Birkengruppe (Mitte)", "unit": "Tage",
     "source": "DWD-Phänologie, gepaarte Stationen (Bericht #96 §3.1)",
     "source_detail": _POLLEN_DS + " Mitte: 421 Stationenpaare.",
     "source_refs": ["DWD_CDC_Phaenologie", "Bergmann_2023_RKI_Allergie_Klima"]},
    {"risk": "EXPECTED_ANNUAL_ALLERGY_DAYS", "key": "delta_s_birke_sued", "value": 5.94,
     "label": "Saison-Spreizung Birkengruppe (Süd)", "unit": "Tage",
     "source": "DWD-Phänologie, gepaarte Stationen (Bericht #96 §3.1)",
     "source_detail": _POLLEN_DS + " Süd: 405 Stationenpaare.",
     "source_refs": ["DWD_CDC_Phaenologie", "Bergmann_2023_RKI_Allergie_Klima"]},
    {"risk": "EXPECTED_ANNUAL_ALLERGY_DAYS", "key": "delta_s_graeser_nord", "value": 4.78,
     "label": "Saison-Spreizung Gräser (Nord)", "unit": "Tage",
     "source": "DWD-Phänologie, gepaarte Stationen (Bericht #96 §3.1)",
     "source_detail": _POLLEN_DS_G + " Nord: 200 Stationenpaare.",
     "source_refs": ["DWD_CDC_Phaenologie"]},
    {"risk": "EXPECTED_ANNUAL_ALLERGY_DAYS", "key": "delta_s_graeser_mitte", "value": 4.08,
     "label": "Saison-Spreizung Gräser (Mitte)", "unit": "Tage",
     "source": "DWD-Phänologie, gepaarte Stationen (Bericht #96 §3.1)",
     "source_detail": _POLLEN_DS_G + " Mitte: 465 Stationenpaare.",
     "source_refs": ["DWD_CDC_Phaenologie"]},
    {"risk": "EXPECTED_ANNUAL_ALLERGY_DAYS", "key": "delta_s_graeser_sued", "value": 3.70,
     "label": "Saison-Spreizung Gräser (Süd)", "unit": "Tage",
     "source": "DWD-Phänologie, gepaarte Stationen (Bericht #96 §3.1)",
     "source_detail": _POLLEN_DS_G + " Süd: 420 Stationenpaare.",
     "source_refs": ["DWD_CDC_Phaenologie"]},
    {"risk": "EXPECTED_ANNUAL_ALLERGY_DAYS", "key": "a_attr", "value": 0.50,
     "label": "Klima-Attribution des Saisontrends", "unit": "Anteil",
     "source": "Anderegg u. a. 2021 (PNAS)",
     "source_detail": "Anteil des beobachteten Pollensaison-Trends, der dem "
                      "anthropogenen Klimawandel zurechenbar ist: ≈ 50 % "
                      "(IQR 19–84 %, Nordamerika — Übertrag auf DE als dokumentierte "
                      "Annahme, Band = Sensitivitätsspanne des Berichts §4). "
                      "Multiplikativ auf die gemessene Saison-Spreizung.",
     "source_refs": ["Anderegg_2021_Pollensaison"]},
    {"risk": "EXPECTED_ANNUAL_ALLERGY_DAYS", "key": "p_ar_u20", "value": 0.088,
     "label": "AR-Prävalenz Band u20", "unit": "Anteil",
     "source": "KiGGS Welle 2 (RKI)", "source_detail": _POLLEN_PAR +
     " u20 = 8,8 % (KiGGS 0–17; die 18/19-Jährigen erhalten den Kinderwert statt des "
     "höheren DEGS1-Werts 14,6 % — dokumentiert unterschätzend, Log 10).",
     "source_refs": ["Thamm_2018_KiGGS_W2"]},
    {"risk": "EXPECTED_ANNUAL_ALLERGY_DAYS", "key": "p_ar_a20_64", "value": 0.132,
     "label": "AR-Prävalenz Band 20–64", "unit": "Anteil",
     "source": "DEGS1 (RKI), bevölkerungsgewichtet", "source_detail": _POLLEN_PAR +
     " 20–64 = 13,2 %: (9.301.783·14,6 + 10.947.845·17,2 + 10.275.235·14,3 + "
     "12.293.757·10,1 + 6.345.372·8,2)/49.163.992 = 13,16 %.",
     "source_refs": ["Langen_2013_DEGS1", "Destatis_Sterbetafeln_2022_2024"]},
    {"risk": "EXPECTED_ANNUAL_ALLERGY_DAYS", "key": "p_ar_a65_74", "value": 0.067,
     "label": "AR-Prävalenz Band 65–74", "unit": "Anteil",
     "source": "DEGS1 (RKI), bevölkerungsgewichtet", "source_detail": _POLLEN_PAR +
     " 65–74 = 6,7 %: (5.180.675·8,2 + 4.388.965·5,0)/9.569.640 = 6,73 %.",
     "source_refs": ["Langen_2013_DEGS1", "Destatis_Sterbetafeln_2022_2024"]},
    {"risk": "EXPECTED_ANNUAL_ALLERGY_DAYS", "key": "p_ar_a75_84", "value": 0.050,
     "label": "AR-Prävalenz Band 75–84", "unit": "Anteil",
     "source": "DEGS1 (RKI), Extrapolation ab 80", "source_detail": _POLLEN_PAR +
     " 75–84 = 5,0 % (DEGS1-Wert 70–79; 80–84 extrapoliert — gekennzeichnet).",
     "source_refs": ["Langen_2013_DEGS1"]},
    {"risk": "EXPECTED_ANNUAL_ALLERGY_DAYS", "key": "p_ar_a85p", "value": 0.050,
     "label": "AR-Prävalenz Band 85+", "unit": "Anteil",
     "source": "DEGS1 (RKI), Extrapolation", "source_detail": _POLLEN_PAR +
     " 85+ = 5,0 % (Extrapolation über das DEGS1-Ende 79 hinaus — gekennzeichnete "
     "Abschätzung; Richtung unklar: Prävalenz fällt mit Alter, Untererfassung bei "
     "Hochaltrigen möglich).",
     "source_refs": ["Langen_2013_DEGS1"]},
    {"risk": "EXPECTED_ANNUAL_ALLERGY_DAYS", "key": "p_sens_birke", "value": 0.55,
     "label": "Anteil Patienten mit Birkengruppen-Saison", "unit": "Anteil",
     "source": "Haftenberger u. a. 2013 (DEGS1-Sensibilisierung)",
     "source_detail": "Anteil der AR-Patienten, deren Symptomfenster die "
                      "Birkengruppe (Hasel/Erle/Birke, Bet-v-1-Kreuzreaktivität) "
                      "umfasst: 0,55 (Band 0,4–0,7) — gekennzeichnete Abschätzung aus "
                      "den DEGS1-Sensibilisierungsprävalenzen (Birke 17,4 %, Gräser "
                      "19,4 % in der Gesamtbevölkerung; Bericht #96 §3.4).",
     "source_refs": ["Haftenberger_2013_Sensibilisierung"]},
    {"risk": "EXPECTED_ANNUAL_ALLERGY_DAYS", "key": "p_sens_graeser", "value": 0.75,
     "label": "Anteil Patienten mit Gräser-Saison", "unit": "Anteil",
     "source": "Haftenberger u. a. 2013 (DEGS1-Sensibilisierung)",
     "source_detail": "Anteil der AR-Patienten mit Gräser-Saison: 0,75 (Band "
                      "0,6–0,85) — gekennzeichnete Abschätzung (Gräser sind das "
                      "häufigste Inhalationsallergen; Bericht #96 §3.4). Summe > 1 ist "
                      "korrekt: Mehrfachsensibilisierung ist die Regel.",
     "source_refs": ["Haftenberger_2013_Sensibilisierung"]},
    {"risk": "EXPECTED_ANNUAL_ALLERGY_DAYS", "key": "f_symptomtage", "value": 0.70,
     "label": "Anteil symptomatischer Saisontage", "unit": "Anteil",
     "source": "Modellannahme (Bericht #96 §3.4; Pfaar 2020 qualitativ)",
     "source_detail": "Anteil der Saisontage mit tatsächlicher Symptomlast: 0,70 "
                      "(Band 0,50–0,85) — Modellannahme; Pfaar 2020 stützt qualitativ "
                      "(Pollenflug treibt Symptomlast), liefert aber keinen Zahlenwert. "
                      "WICHTIG: f kürzt sich im €-Pfad vollständig heraus (c_Tag = "
                      "c_Jahr/d_Saison enthält f im Nenner) — der weichste Parameter "
                      "beeinflusst den Euro-Ausweis nicht (Golden-Test "
                      "beispiel_96_f_kuerzung).",
     "source_refs": ["Pfaar_2020_Symptomlast"]},
    {"risk": "EXPECTED_ANNUAL_ALLERGY_DAYS", "key": "l_saison_birke", "value": 30.0,
     "label": "Saisonlänge Birkengruppe L_B", "unit": "Tage",
     "source": "EAACI-Saisonkriterium (Pfaar 2017) — gekennzeichnete Abschätzung",
     "source_detail": "Typische Länge der Birkengruppen-Saison nach dem "
                      "EAACI-Kriterium: 30 Tage (Band 20–45). Die Quelle definiert das "
                      "Kriterium (Pollenschwellen), publiziert aber KEINE festen "
                      "Längenwerte — daher gekennzeichnete Abschätzung (§3.9). Geht in "
                      "d_Saison = f·(p_B·L_B + p_G·L_G) = 43,05 Tage ein und damit in "
                      "den Kostensatz c_Tag = c_Jahr/d_Saison: Eine Änderung von L_B "
                      "verschiebt c_Tag mit (Kopplung §3.9, Bericht §3.5).",
     "source_refs": ["Pfaar_2017_EAACI_Pollensaison"]},
    {"risk": "EXPECTED_ANNUAL_ALLERGY_DAYS", "key": "l_saison_graeser", "value": 60.0,
     "label": "Saisonlänge Gräser L_G", "unit": "Tage",
     "source": "EAACI-Saisonkriterium (Pfaar 2017) — gekennzeichnete Abschätzung",
     "source_detail": "Typische Länge der Gräser-Saison nach dem EAACI-Kriterium: "
                      "60 Tage (Band 45–80); gekennzeichnete Abschätzung wie L_B. "
                      "Geht über d_Saison in den Kostensatz c_Tag ein (Bericht §3.5).",
     "source_refs": ["Pfaar_2017_EAACI_Pollensaison"]},
    {"risk": "EXPECTED_ANNUAL_ALLERGY_DAYS", "key": "lambda_veg", "value": 0.70,
     "label": "Gewicht der Vegetations-Modulation λ", "unit": "Faktor",
     "source": "Werchan 2017/2018, Bogawski 2019 (Kette Bericht #96 §3.4)",
     "source_detail": "λ = 2(R−1)/(R+1) × a_veg mit R = Extremstandort-Verhältnis "
                      "der Berliner Pollenfallen (Birke 3,45 / Gräser 4,06 in der "
                      "Zuwachs-Lesart) und a_veg = 0,6 (Anteil der räumlichen Varianz, "
                      "den lokale Vegetation erklärt): 0,66–0,73 ⇒ Basiswert 0,70 "
                      "(Band 0,3–1,0). Gekennzeichnete Abschätzung; wirkt "
                      "mittelwertzentriert über P̂ = 1 + λ(Ĝ/Ḡ − 1) auf ΔTage UND €.",
     "source_refs": ["Werchan_2017_Pollen_Berlin", "Werchan_2018_Symptome_Berlin",
                     "Bogawski_2019_Baumkronen_Pollen"]},
    # ── #96: Integrationsparameter der Ebene POLLEN_LOAD (§3.3-Spezifikation) ──
    # g_bar_ref ENTFERNT (31.08.2026, Aufgabe §3.2 „geschlossene Betrachtungsebene"):
    # Das Referenzmittel Ḡ des P̂-Terms wird NICHT mehr als bundesweiter Parameter
    # geführt, sondern im Lauf aus den Zellen der jeweiligen Kommune gebildet
    # (inputs.kommunale_pollen_referenz → regional["pollen_g_bar"]). Ohne Referenz
    # bleibt P̂ neutral. Die Stichprobe pollen_g_bar.py dokumentiert nur noch die
    # Größenordnung/Streuung von Ĝ zur Plausibilisierung der Ebene.
    # veg_weight_birke ENTFERNT (31.08.2026, Ledger #96 Befund 138): w_B ist eine
    # ABGELEITETE Größe (p_B·ΔS_B,DE / Σ) und kein frei setzbarer Parameter — als
    # editierbarer Registry-Wert wäre die Kopplung an p_B/p_G tot gewesen; eine
    # Laufzeit-Ableitung hätte den Schicht-A-Hazard bewegt (Befund 142). w_B ist
    # daher eine Definitionskonstante der Ebene (indicators.POLLEN_G_WEIGHT_BIRKE)
    # mit TESTGEBUNDENER Kopplung an p_B/p_G/ΔS_DE (Bericht #96 §3.3, #p-hat).
    {"risk": "EXPECTED_ANNUAL_ALLERGY_DAYS", "key": "birch_group_share_default",
     "value": 0.12,
     "label": "Birkengruppen-Anteil ungetaggter Bäume", "unit": "Anteil",
     "source": "ABGESCHÄTZT ohne Primärquelle (§3.9) — Bericht #96 §3.3",
     "source_detail": "OSM-Bäume tragen nur teilweise genus/species. Für Kronen ohne "
                      "Gattungs-Tag wird der Birkengruppen-Anteil (Betula/Alnus/Corylus) "
                      "mit 0,12 angesetzt. Wirkung: s_unbek verschiebt die Gewichtung "
                      "von Kronen gegen Grün INNERHALB der Kommune — die Kommunensumme "
                      "bleibt unberührt (die Zentrierung über Ḡ macht sie invariant), "
                      "die Zellverteilung reagiert unterschiedlich stark "
                      "(gehölzgeprägt zweistellig, vegetationsarm kaum — Zahlen s. u.). "
                      "§3.9-Kategorie "
                      "ABGESCHÄTZT: Für den Gattungsmix ungetaggter OSM-Bäume "
                      "existiert keine belastbare Primärquelle (Straßenbaumkataster "
                      "sind kommunal, uneinheitlich und nicht keyless aggregierbar) — "
                      "der Wert ist eine dokumentierte Annahme, kein Messwert. "
                      "Begründung OHNE Fundstelle (§3.8-Datenlücke, es wird bewusst "
                      "keine Literaturzahl zitiert): Setzung zwischen zwei Ankern — "
                      "Straßenbaumbestände führen Birke/Erle als Nebenbaumarten "
                      "(unteres Bandende 0,05), Park-/Gehölzstrukturen mit Hasel und "
                      "Hainbuche liegen höher (oberes Bandende 0,25); Basiswert 0,12 "
                      "als Mitte der Spanne. "
                      "Ergebnis-Sensitivität über den dokumentierten Zelltypen-Satz "
                      "(s_unbek 0,05 → 0,25): Ĝ/Ḡ Allee/Park 0,665 → 0,752 "
                      "(+13,0 %), Wohnblock 0,255 → 0,258 (+0,9 %), Grünanlage "
                      "2,014 → 1,918 (−4,7 %), Mischlage 1,066 → 1,072 (+0,6 %); "
                      "reproduzierbar im Golden-Test "
                      "test_s_unbekannt_sensitivity_band. Die KOMMUNENSUMME bleibt "
                      "unverändert (Zentrierung). Produkt-Kennzeichnung als Annahme; "
                      "ersetzbar durch ein kommunales Baumkataster.",
     "source_refs": []},

    # ── #98 UV-Schädigungen: klimaattribuierte Hautkrebsfälle (Bericht Rev. 1) ─
    # ΔF_e = F_e · BAF_e · ΔDosis;  YLL = Σ_e ΔF_e · λ_e · L̄_e
    {"risk": "EXPECTED_ANNUAL_UV_YLL", "key": "k_uv", "value": 0.84,
     "label": "Übersetzung SSD-Trend → UV-Dosis", "unit": "Faktor",
     "source": "Lorenz 2024 (Dosistrend) ÷ eigene SSD-Trendmessung (§3.2)",
     "source_detail": "Der erythemwirksame Dosistrend steigt langsamer als die "
                      "Sonnenscheindauer: +4,9 %/Dekade (BfS-Messreihe Dortmund "
                      "1997–2022, signifikant) ÷ +5,81 %/Dekade (SSD-Trend NRW im "
                      "SELBEN Fenster und derselben Datenfamilie, die das Produkt "
                      "nutzt — DWD-Gebietsmittel, Anlage ssd_trend_region.csv) = "
                      "0,84. Band 0,4–1,0: untere Stütze die frühere Stations-"
                      "Paarung 0,43, obere Stütze 1,0 (Globalstrahlung ≈ parallel "
                      "zur Dosis). Plausibilisierung: implizite Dosisänderung DE "
                      "7,82 % × 0,84 ≈ 6,6 % über den Normalperiodenversatz "
                      "≈ 2,2 %/Dekade — im Satellitenband 1,2–3,6 %/Dekade.",
     "source_refs": ["Lorenz_2024_UV_Dortmund", "DWD_CDC_SSD_Raster"]},
    {"risk": "EXPECTED_ANNUAL_UV_YLL", "key": "a_attr", "value": 0.75,
     "label": "Klima-Attribution des Dosistrends", "unit": "Anteil",
     "source": "Gekennzeichnete Abschätzung (§3.9; Bericht #98 §3.2)",
     "source_detail": "Anteil des SSD-/Dosistrends, der dem Klimawandel "
                      "zuzurechnen ist: 0,75 (Band 0,5–1,0). Für UV existiert "
                      "KEINE Attributionsstudie (anders als bei #96, dort 0,50 "
                      "gemessen) — Begründung: Lorenz nennt als Trendursache "
                      "v. a. die Bewölkungsabnahme (klimasystemisch → hoher Wert), "
                      "das Aerosol-Brightening seit den 1980ern ist anthropogen, "
                      "aber keine Klimawirkung im KWRA-Sinn (→ < 1,0). "
                      "Ersetzungspfad: Wolken-/Aerosol-Zerlegung aus Reanalysen.",
     "source_refs": ["Lorenz_2024_UV_Dortmund"]},
    {"risk": "EXPECTED_ANNUAL_UV_YLL", "key": "baf_mm", "value": 0.60,
     "label": "Biologischer Verstärkungsfaktor Melanom", "unit": "Faktor",
     "source": "Slaper 1996 / Madronich 2021",
     "source_detail": "%-Änderung der Melanom-Inzidenz je +1 % erythemwirksamer "
                      "Dosis: 0,6 (± 0,4). Zwei unabhängige Quellen nennen "
                      "denselben Wert (Slaper 1996 Nature; Madronich 2021 "
                      "ACS Earth Space Chem).",
     "source_refs": ["Slaper_1996_BAF", "Madronich_2021_BAF"]},
    {"risk": "EXPECTED_ANNUAL_UV_YLL", "key": "baf_c44", "value": 1.675,
     "label": "Biologischer Verstärkungsfaktor C44", "unit": "Faktor",
     "source": "Slaper 1996 × KID-2025-Entitätensplit (§3.1)",
     "source_detail": "Gewichtetes Mittel der BAF von Basaliom (1,4) und "
                      "Plattenepithelkarzinom (2,5) mit dem SCC-Anteil w_SCC: "
                      "0,75·1,4 + 0,25·2,5 = 1,675 (Band 1,675–1,95 über "
                      "w_SCC = 0,25–0,50). Der Split wird altersinvariant "
                      "angewendet — dokumentierte Annahme; Richtung: Der "
                      "SCC-Anteil steigt real mit dem Alter ⇒ Unterschätzung des "
                      "Zusatzes in alten Kommunen. KOPPLUNG (§3.9): Ändert sich "
                      "w_SCC, ist BAF_C44 neu zu rechnen (Golden-Test bindet die "
                      "Kette).",
     "source_refs": ["Slaper_1996_BAF", "ZfKD_KID_2025"]},
    {"risk": "EXPECTED_ANNUAL_UV_YLL", "key": "w_scc", "value": 0.25,
     "label": "SCC-Anteil an C44", "unit": "Anteil",
     "source": "ZfKD KID 2025, Kap. 3.14 (Quellen-Widerspruch benannt)",
     "source_detail": "Anteil der Plattenepithelkarzinome am nicht-melanotischen "
                      "Hautkrebs: 0,25 („knapp drei Viertel Basaliome, etwa ein "
                      "Viertel Plattenepithelkarzinome“, KID 2025 für 2021–2023). "
                      "WIDERSPRUCH benannt (§3.8): Die 2015er-BfS-Fallzahlen "
                      "(BCC 158.840 / SCC 98.950) ergäben 0,384 — Band 0,25–0,50 "
                      "deckt beide ab; Basiswert = aktuelle Registerdaten der "
                      "Primärquelle. Mögliche Ursache: Untererfassung von "
                      "SCC-Mehrfachtumoren.",
     "source_refs": ["ZfKD_KID_2025"]},
    {"risk": "EXPECTED_ANNUAL_UV_YLL", "key": "c_kal_mm", "value": 1.022,
     "label": "Normierungsskalar Melanom", "unit": "Faktor",
     "source": "ZfKD 2023 ÷ Ablesekette (§3.3/§3.4)",
     "source_detail": "EIN Skalar je Entität (§3.4): 27.430 amtliche "
                      "Neuerkrankungen 2023 ÷ 26.837 aus der Ablesekette = 1,022. "
                      "Damit reproduziert die Bundes-Baseline die ZfKD-Fallzahlen "
                      "exakt. Die Ablese-Toleranz (±15 %, vorab fixiert) ist mit "
                      "−2,2 % eingehalten.",
     "source_refs": ["ZfKD_KID_2025"]},
    {"risk": "EXPECTED_ANNUAL_UV_YLL", "key": "c_kal_c44", "value": 0.999,
     "label": "Normierungsskalar C44", "unit": "Faktor",
     "source": "ZfKD 2023 ÷ Ablesekette (§3.3/§3.4)",
     "source_detail": "EIN Skalar je Entität (§3.4): 242.820 ÷ 243.158 = 0,999; "
                      "Ablese-Abweichung vor Normierung +0,1 % (Toleranz ±15 %).",
     "source_refs": ["ZfKD_KID_2025"]},
    {"risk": "EXPECTED_ANNUAL_UV_YLL", "key": "lambda_mm", "value": 0.1155,
     "label": "Letalitätsanteil Melanom", "unit": "Anteil",
     "source": "ZfKD 2023: 3.169 Sterbefälle / 27.430 Neuerkrankungen",
     "source_detail": "Perioden-Approximation, GEKENNZEICHNET (§3.9): Bei "
                      "steigender Inzidenz ist das Verhältnis Sterbefälle/"
                      "Neuerkrankungen desselben Jahres keine Kohorten-Letalität; "
                      "Richtung: Überschätzung des Mortalitätsanteils.",
     "source_refs": ["ZfKD_KID_2025"]},
    {"risk": "EXPECTED_ANNUAL_UV_YLL", "key": "lambda_c44", "value": 0.00549,
     "label": "Letalitätsanteil C44", "unit": "Anteil",
     "source": "ZfKD 2023: 1.332 / 242.820",
     "source_detail": "Perioden-Approximation wie lambda_mm (gekennzeichnet).",
     "source_refs": ["ZfKD_KID_2025"]},
    {"risk": "EXPECTED_ANNUAL_UV_YLL", "key": "l_rest_mm", "value": 10.58,
     "label": "Restlebenserwartung je Melanom-Sterbefall", "unit": "Jahre",
     "source": "Sterbetafel 2022/2024 am medianen Sterbealter",
     "source_detail": "Sterbefallgewichtet über die Geschlechter: "
                      "(1.318·10,92 + 1.851·10,33)/3.169 = 10,58 Jahre "
                      "(e(78) Frauen, e(76) Männer). MEDIAN-Approximation, "
                      "gekennzeichnet: Bei rechtsschiefer Sterbealter-Verteilung "
                      "leicht überschätzend.",
     "source_refs": ["ZfKD_KID_2025", "Destatis_Sterbetafeln_2022_2024"]},
    {"risk": "EXPECTED_ANNUAL_UV_YLL", "key": "l_rest_c44", "value": 5.30,
     "label": "Restlebenserwartung je C44-Sterbefall", "unit": "Jahre",
     "source": "Sterbetafel 2022/2024 am medianen Sterbealter",
     "source_detail": "(541·5,04 + 791·5,47)/1.332 = 5,30 Jahre (e(88) Frauen, "
                      "e(85) Männer); Median-Approximation wie l_rest_mm.",
     "source_refs": ["ZfKD_KID_2025", "Destatis_Sterbetafeln_2022_2024"]},
    {"risk": "EXPECTED_ANNUAL_UV_YLL", "key": "c_fall_mm", "value": 6724.0,
     "label": "Behandlungskosten je Melanom-Fall", "unit": "EUR/Fall",
     "source": "Speckemeier 2022 (Erstjahr, indexiert €2024)",
     "source_detail": "5.326 €₂₀₁₅ × VPI 119,3/94,5 = 6.724 €₂₀₂₄ (Band bis "
                      "11.410 € = nicht-SCS-detektierte Fälle). PROXY (§3.1): "
                      "überschätzend, weil Gesamt- statt Inkrementalkosten "
                      "(Grundversorgung überwiegend alter Patienten enthalten); "
                      "unterschätzend, weil nur das Erstjahr (Folgejahre und "
                      "Metastasentherapien fehlen). Basiswahl folgt der "
                      "Untergrenzen-Zusage.",
     "source_refs": ["Speckemeier_2022_Hautkrebskosten",
                     "Destatis_VPI_lange_Reihen"]},
    {"risk": "EXPECTED_ANNUAL_UV_YLL", "key": "c_fall_c44", "value": 5883.0,
     "label": "Behandlungskosten je C44-Fall", "unit": "EUR/Fall",
     "source": "Speckemeier 2022 (Erstjahr, indexiert €2024)",
     "source_detail": "4.660 €₂₀₁₅ × 119,3/94,5 = 5.883 €₂₀₂₄ (Band bis "
                      "7.436 €); Proxy-Kennzeichnung wie c_fall_mm.",
     "source_refs": ["Speckemeier_2022_Hautkrebskosten",
                     "Destatis_VPI_lange_Reihen"]},
    {"risk": "EXPECTED_ANNUAL_UV_YLL", "key": "or_out", "value": 1.77,
     "label": "Außenberufs-OR (SCC)", "unit": "Odds Ratio",
     "source": "Schmitt u. a. 2011 (Meta-Analyse)",
     "source_detail": "OR 1,77 [1,37–2,30] für Plattenepithelkarzinom bei "
                      "beruflicher UV-Exposition. Wirkt NUR im Sensitivitätsband "
                      "(r_out, Default 1 — siehe r_out_enabled): mittelwert"
                      "zentriert auf den Außenberufs-Bundesanteil q̄ = 0,070 und "
                      "nur auf den SCC-Anteil am C44-Zusatz (w^Z = 0,373).",
     "source_refs": ["Schmitt_2011_Aussenberufe"]},
    {"risk": "EXPECTED_ANNUAL_UV_YLL", "key": "qbar_out", "value": 0.070,
     "label": "Bundesmittel Außenberufs-Anteil", "unit": "Anteil",
     "source": "Destatis VGR 2023 (Erwerbstätige nach Wirtschaftsbereichen)",
     "source_detail": "(572 Tsd. Land-/Forstwirtschaft/Fischerei + 2.643 Tsd. "
                      "Baugewerbe) / 45.909 Tsd. Erwerbstätige = 0,070. PROXY "
                      "(beide Richtungen): Nicht alle Beschäftigten dieser "
                      "Branchen arbeiten im Freien; Außenberufe anderer Branchen "
                      "fehlen. Amtlich publiziertes Zentrierungsmittel — nach "
                      "Aufgabe §3.2 zulässig, weil die Evidenz (Fall-Kontroll-OR) "
                      "individuell erhoben ist.",
     "source_refs": ["Destatis_Erwerbstaetige_Wirtschaftsbereiche"]},
    {"risk": "EXPECTED_ANNUAL_UV_YLL", "key": "r_out_enabled", "value": 0.0,
     "label": "Außenberufs-Modifikator aktiv (0/1)", "unit": "Schalter",
     "source": "Bericht #98 §3.4: Sensitivitätsband, nicht im Basiswert",
     "source_detail": "0 = aus (Basiswert des Berichts), 1 = an. Der "
                      "Außenberufs-Modifikator ist ausdrücklich ein "
                      "Sensitivitätsband und geht NICHT in den Basiswert ein "
                      "(Log 10); der Schalter macht die Sensitivitätsrechnung "
                      "reproduzierbar, ohne den Basiswert zu verändern. Die "
                      "Zellgröße (Außenbeschäftigten-Anteil) ist als Ebene "
                      "GEPARKT — INKAR/SVB-Branchenanteile sind nicht keyless je "
                      "100-m-Zelle verfügbar (§3.1-Watchlist).",
     "source_refs": ["Schmitt_2011_Aussenberufe"]},
    {"risk": "EXPECTED_ANNUAL_UV_YLL", "key": "v_verh", "value": 1.0,
     "label": "Verhaltens-Sensitivität (Default 1)", "unit": "Faktor",
     "source": "Bericht #98 §3.4: Sensitivitätsband, nicht im Basiswert",
     "source_detail": "Tages-Multiplikator der persönlichen Dosis an "
                      "Komforttagen (Band 1,25–1,60 als TAGESWERT): +1,2 min "
                      "Außenzeit je °C (ATUS) ⇒ +27 % an einem Komforttag; Zeit "
                      "im Freien erklärt die persönliche Dosis nahezu "
                      "proportional (R² 0,75–0,79); Kleidungskomponente +15 % ⇒ "
                      "s ≈ +45 %. Die JAHRESwirkung hängt vom Komforttag-Anteil "
                      "ab (Szenario-Stellgröße, keine Zellgröße in M0) — deshalb "
                      "Default 1. Doppelzählungsschutz: Der Ambient-Anteil steckt "
                      "bereits in ΔDosis.",
     "source_refs": ["GraffZivin_2014_Zeitallokation", "Schmalwieser_2021_Dosis"]},

    {"risk": "EXPECTED_ANNUAL_UV_YLL", "key": "i_mm_u20", "value": 0.5,
     "label": "Inzidenz Melanom (C43) Band u20", "unit": "1/100.000·a",
     "source": "ZfKD KID 2025 Abb. 3.13.2 (Ablesekette, roh)",
     "source_detail": "Roh-Neuerkrankungsrate vor Normierung: Die "
                      "altersspezifischen Raten sind in KID 2025 nur als "
                      "Abbildungen publiziert (ZfKD-Datenbankwerte nicht keyless "
                      "abrufbar — dokumentierte Datenlücke). Ablesung je "
                      "5-Jahres-Gruppe und Geschlecht (Toleranz ±15 %, "
                      "gitterlinien-gestützt; Anlage kid2025_ablesewerte.csv), "
                      "Aggregation auf die Produktbänder mit "
                      "geschlechtsspezifischen Bevölkerungsgewichten "
                      "(31.12.2023). Der Normierungsskalar c_kal_mm zieht die "
                      "Bundessumme exakt auf die amtliche Fallzahl. UNTER der Ablesegrenze der Abbildung (< ≈ 15 je 100.000 bei Achse 0–2.500) — angesetzt mit Band 0–5, gekennzeichnete Abschätzung mit < 0,3 % Wirkung auf die Bundes-Baseline.",
     "source_refs": ["ZfKD_KID_2025", "Destatis_Sterbetafeln_2022_2024"]},
    {"risk": "EXPECTED_ANNUAL_UV_YLL", "key": "i_mm_a20_64", "value": 24.7,
     "label": "Inzidenz Melanom (C43) Band 20–64", "unit": "1/100.000·a",
     "source": "ZfKD KID 2025 Abb. 3.13.2 (Ablesekette, roh)",
     "source_detail": "Roh-Neuerkrankungsrate vor Normierung: Die "
                      "altersspezifischen Raten sind in KID 2025 nur als "
                      "Abbildungen publiziert (ZfKD-Datenbankwerte nicht keyless "
                      "abrufbar — dokumentierte Datenlücke). Ablesung je "
                      "5-Jahres-Gruppe und Geschlecht (Toleranz ±15 %, "
                      "gitterlinien-gestützt; Anlage kid2025_ablesewerte.csv), "
                      "Aggregation auf die Produktbänder mit "
                      "geschlechtsspezifischen Bevölkerungsgewichten "
                      "(31.12.2023). Der Normierungsskalar c_kal_mm zieht die "
                      "Bundessumme exakt auf die amtliche Fallzahl.",
     "source_refs": ["ZfKD_KID_2025", "Destatis_Sterbetafeln_2022_2024"]},
    {"risk": "EXPECTED_ANNUAL_UV_YLL", "key": "i_mm_a65_74", "value": 64.0,
     "label": "Inzidenz Melanom (C43) Band 65–74", "unit": "1/100.000·a",
     "source": "ZfKD KID 2025 Abb. 3.13.2 (Ablesekette, roh)",
     "source_detail": "Roh-Neuerkrankungsrate vor Normierung: Die "
                      "altersspezifischen Raten sind in KID 2025 nur als "
                      "Abbildungen publiziert (ZfKD-Datenbankwerte nicht keyless "
                      "abrufbar — dokumentierte Datenlücke). Ablesung je "
                      "5-Jahres-Gruppe und Geschlecht (Toleranz ±15 %, "
                      "gitterlinien-gestützt; Anlage kid2025_ablesewerte.csv), "
                      "Aggregation auf die Produktbänder mit "
                      "geschlechtsspezifischen Bevölkerungsgewichten "
                      "(31.12.2023). Der Normierungsskalar c_kal_mm zieht die "
                      "Bundessumme exakt auf die amtliche Fallzahl.",
     "source_refs": ["ZfKD_KID_2025", "Destatis_Sterbetafeln_2022_2024"]},
    {"risk": "EXPECTED_ANNUAL_UV_YLL", "key": "i_mm_a75_84", "value": 94.9,
     "label": "Inzidenz Melanom (C43) Band 75–84", "unit": "1/100.000·a",
     "source": "ZfKD KID 2025 Abb. 3.13.2 (Ablesekette, roh)",
     "source_detail": "Roh-Neuerkrankungsrate vor Normierung: Die "
                      "altersspezifischen Raten sind in KID 2025 nur als "
                      "Abbildungen publiziert (ZfKD-Datenbankwerte nicht keyless "
                      "abrufbar — dokumentierte Datenlücke). Ablesung je "
                      "5-Jahres-Gruppe und Geschlecht (Toleranz ±15 %, "
                      "gitterlinien-gestützt; Anlage kid2025_ablesewerte.csv), "
                      "Aggregation auf die Produktbänder mit "
                      "geschlechtsspezifischen Bevölkerungsgewichten "
                      "(31.12.2023). Der Normierungsskalar c_kal_mm zieht die "
                      "Bundessumme exakt auf die amtliche Fallzahl.",
     "source_refs": ["ZfKD_KID_2025", "Destatis_Sterbetafeln_2022_2024"]},
    {"risk": "EXPECTED_ANNUAL_UV_YLL", "key": "i_mm_a85p", "value": 88.5,
     "label": "Inzidenz Melanom (C43) Band 85+", "unit": "1/100.000·a",
     "source": "ZfKD KID 2025 Abb. 3.13.2 (Ablesekette, roh)",
     "source_detail": "Roh-Neuerkrankungsrate vor Normierung: Die "
                      "altersspezifischen Raten sind in KID 2025 nur als "
                      "Abbildungen publiziert (ZfKD-Datenbankwerte nicht keyless "
                      "abrufbar — dokumentierte Datenlücke). Ablesung je "
                      "5-Jahres-Gruppe und Geschlecht (Toleranz ±15 %, "
                      "gitterlinien-gestützt; Anlage kid2025_ablesewerte.csv), "
                      "Aggregation auf die Produktbänder mit "
                      "geschlechtsspezifischen Bevölkerungsgewichten "
                      "(31.12.2023). Der Normierungsskalar c_kal_mm zieht die "
                      "Bundessumme exakt auf die amtliche Fallzahl.",
     "source_refs": ["ZfKD_KID_2025", "Destatis_Sterbetafeln_2022_2024"]},
    {"risk": "EXPECTED_ANNUAL_UV_YLL", "key": "i_c44_u20", "value": 2.0,
     "label": "Inzidenz C44 Band u20", "unit": "1/100.000·a",
     "source": "ZfKD KID 2025 Abb. 3.14.3 (Ablesekette, roh)",
     "source_detail": "Roh-Neuerkrankungsrate vor Normierung: Die "
                      "altersspezifischen Raten sind in KID 2025 nur als "
                      "Abbildungen publiziert (ZfKD-Datenbankwerte nicht keyless "
                      "abrufbar — dokumentierte Datenlücke). Ablesung je "
                      "5-Jahres-Gruppe und Geschlecht (Toleranz ±15 %, "
                      "gitterlinien-gestützt; Anlage kid2025_ablesewerte.csv), "
                      "Aggregation auf die Produktbänder mit "
                      "geschlechtsspezifischen Bevölkerungsgewichten "
                      "(31.12.2023). Der Normierungsskalar c_kal_c44 zieht die "
                      "Bundessumme exakt auf die amtliche Fallzahl. UNTER der Ablesegrenze der Abbildung (< ≈ 15 je 100.000 bei Achse 0–2.500) — angesetzt mit Band 0–5, gekennzeichnete Abschätzung mit < 0,3 % Wirkung auf die Bundes-Baseline.",
     "source_refs": ["ZfKD_KID_2025", "Destatis_Sterbetafeln_2022_2024"]},
    {"risk": "EXPECTED_ANNUAL_UV_YLL", "key": "i_c44_a20_64", "value": 125.9,
     "label": "Inzidenz C44 Band 20–64", "unit": "1/100.000·a",
     "source": "ZfKD KID 2025 Abb. 3.14.3 (Ablesekette, roh)",
     "source_detail": "Roh-Neuerkrankungsrate vor Normierung: Die "
                      "altersspezifischen Raten sind in KID 2025 nur als "
                      "Abbildungen publiziert (ZfKD-Datenbankwerte nicht keyless "
                      "abrufbar — dokumentierte Datenlücke). Ablesung je "
                      "5-Jahres-Gruppe und Geschlecht (Toleranz ±15 %, "
                      "gitterlinien-gestützt; Anlage kid2025_ablesewerte.csv), "
                      "Aggregation auf die Produktbänder mit "
                      "geschlechtsspezifischen Bevölkerungsgewichten "
                      "(31.12.2023). Der Normierungsskalar c_kal_c44 zieht die "
                      "Bundessumme exakt auf die amtliche Fallzahl.",
     "source_refs": ["ZfKD_KID_2025", "Destatis_Sterbetafeln_2022_2024"]},
    {"risk": "EXPECTED_ANNUAL_UV_YLL", "key": "i_c44_a65_74", "value": 617.6,
     "label": "Inzidenz C44 Band 65–74", "unit": "1/100.000·a",
     "source": "ZfKD KID 2025 Abb. 3.14.3 (Ablesekette, roh)",
     "source_detail": "Roh-Neuerkrankungsrate vor Normierung: Die "
                      "altersspezifischen Raten sind in KID 2025 nur als "
                      "Abbildungen publiziert (ZfKD-Datenbankwerte nicht keyless "
                      "abrufbar — dokumentierte Datenlücke). Ablesung je "
                      "5-Jahres-Gruppe und Geschlecht (Toleranz ±15 %, "
                      "gitterlinien-gestützt; Anlage kid2025_ablesewerte.csv), "
                      "Aggregation auf die Produktbänder mit "
                      "geschlechtsspezifischen Bevölkerungsgewichten "
                      "(31.12.2023). Der Normierungsskalar c_kal_c44 zieht die "
                      "Bundessumme exakt auf die amtliche Fallzahl.",
     "source_refs": ["ZfKD_KID_2025", "Destatis_Sterbetafeln_2022_2024"]},
    {"risk": "EXPECTED_ANNUAL_UV_YLL", "key": "i_c44_a75_84", "value": 1267.2,
     "label": "Inzidenz C44 Band 75–84", "unit": "1/100.000·a",
     "source": "ZfKD KID 2025 Abb. 3.14.3 (Ablesekette, roh)",
     "source_detail": "Roh-Neuerkrankungsrate vor Normierung: Die "
                      "altersspezifischen Raten sind in KID 2025 nur als "
                      "Abbildungen publiziert (ZfKD-Datenbankwerte nicht keyless "
                      "abrufbar — dokumentierte Datenlücke). Ablesung je "
                      "5-Jahres-Gruppe und Geschlecht (Toleranz ±15 %, "
                      "gitterlinien-gestützt; Anlage kid2025_ablesewerte.csv), "
                      "Aggregation auf die Produktbänder mit "
                      "geschlechtsspezifischen Bevölkerungsgewichten "
                      "(31.12.2023). Der Normierungsskalar c_kal_c44 zieht die "
                      "Bundessumme exakt auf die amtliche Fallzahl.",
     "source_refs": ["ZfKD_KID_2025", "Destatis_Sterbetafeln_2022_2024"]},
    {"risk": "EXPECTED_ANNUAL_UV_YLL", "key": "i_c44_a85p", "value": 1479.5,
     "label": "Inzidenz C44 Band 85+", "unit": "1/100.000·a",
     "source": "ZfKD KID 2025 Abb. 3.14.3 (Ablesekette, roh)",
     "source_detail": "Roh-Neuerkrankungsrate vor Normierung: Die "
                      "altersspezifischen Raten sind in KID 2025 nur als "
                      "Abbildungen publiziert (ZfKD-Datenbankwerte nicht keyless "
                      "abrufbar — dokumentierte Datenlücke). Ablesung je "
                      "5-Jahres-Gruppe und Geschlecht (Toleranz ±15 %, "
                      "gitterlinien-gestützt; Anlage kid2025_ablesewerte.csv), "
                      "Aggregation auf die Produktbänder mit "
                      "geschlechtsspezifischen Bevölkerungsgewichten "
                      "(31.12.2023). Der Normierungsskalar c_kal_c44 zieht die "
                      "Bundessumme exakt auf die amtliche Fallzahl.",
     "source_refs": ["ZfKD_KID_2025", "Destatis_Sterbetafeln_2022_2024"]},

    # ── Todesfälle durch Hochwasser/Sturzfluten ────────────────────────────────
    {"risk": "EXPECTED_ANNUAL_MORTALITY_FLOOD", "key": "fatality_rate_flash_per_100k",
     "value": 9.0, "label": "Letalität Sturzflut-Regime", "unit": "Tote/100k je Intensität",
     "source": "Jonkman 2008 / CEDIM (Ahr 2021)",
     "source_detail": "Todesfälle je 100.000 Exponierter bei voller Ereignisintensität im "
                      "Sturzflut-Regime (enges Steiltal, schneller Anstieg). Getrennt vom "
                      "Langsam-Regime geführt, weil sich die Letalität je exponierter "
                      "Person zwischen beiden um Größenordnungen unterscheidet: Die Ahr "
                      "2021 forderte über 180 Todesopfer, die Elbe 2002 bei weit größerer "
                      "überfluteter Fläche und vergleichbarem Sachschaden rund 21. Ein "
                      "gemittelter Wert würde genau diesen Unterschied verwischen.",
     "source_refs": ["Jonkman_2008_LossOfLife", "CEDIM_Hochwasser_2021"]},
    {"risk": "EXPECTED_ANNUAL_MORTALITY_FLOOD", "key": "fatality_rate_slow_per_100k",
     "value": 0.15, "label": "Letalität Langsam-Anstiegs-Regime",
     "unit": "Tote/100k je Intensität",
     "source": "Jonkman 2008 (Restzone) / Elbe 2002",
     "source_detail": "Todesfälle je 100.000 Exponierter im flachen Auen-Regime mit "
                      "langsamem Wasseranstieg — Menschen können sich in aller Regel in "
                      "Sicherheit bringen. Entspricht Jonkmans „Restzone“.",
     "source_refs": ["Jonkman_2008_LossOfLife"]},
    {"risk": "EXPECTED_ANNUAL_MORTALITY_FLOOD", "key": "warning_modifier_span", "value": 0.6,
     "label": "Spannweite Warnzeit-Modifikator", "unit": "Faktor",
     "source": "Modellannahme (dokumentiert)",
     "source_detail": "Frühwarnung und Notfallmanagement skalieren den Outcome von "
                      "1 − Spanne/2 bis 1 + Spanne/2. Bewusst explizit modelliert statt in "
                      "eine Konstante gefaltet: Das Warnversagen war an der Ahr "
                      "ausschlaggebend, und es ist der Hebel, den eine Kommune tatsächlich "
                      "bedienen kann.",
     "source_refs": ["CEDIM_Hochwasser_2021", "BBK_Hochwasserschutzfibel"]},
    {"risk": "EXPECTED_ANNUAL_MORTALITY_FLOOD", "key": "elderly_weight", "value": 1.5,
     "label": "Altersgewichtung Flutopfer", "unit": "Faktor",
     "source": "Ereignisauswertungen (Modellannahme)",
     "source_detail": "Flutopfer sind überproportional alt und mobilitätseingeschränkt. "
                      "Der Modifikator skaliert mit der Abweichung des 65+-Anteils der "
                      "Zelle vom Zentrierungsmittel **0,22** = amtlicher 65+-Anteil "
                      "Deutschlands (Zensus 2022/Destatis-Fortschreibung; identisch "
                      "zum Regional-Fallback in engine/tunables.py). Zentrierung auf "
                      "ein PUBLIZIERTES Bevölkerungsmittel ist hier der richtige "
                      "Bezug (Aufgabe §3.2): Die Evidenz (Altersverteilung der "
                      "Flutopfer, CEDIM-Ereignisauswertung) ist individuell erhoben, "
                      "nicht intra-kommunal — deshalb darf der Term Kommunen "
                      "gegeneinander verschieben. Das Mittel ist in "
                      "impact/health.py hartkodiert (0.22); Registry-Parameter erst "
                      "bei einer Methodik-Ausarbeitung des Flut-Kanals.",
     "source_refs": ["CEDIM_Hochwasser_2021", "Destatis_Sterbetafeln_2022_2024"]},
    {"risk": "EXPECTED_ANNUAL_MORTALITY_FLOOD", "key": "calibration", "value": 1.0,
     "label": "Kalibrierfaktor Flut-Mortalität", "unit": "Faktor",
     "source": "Kuratierte Ereignisliste",
     "source_detail": "Skaliert die nationale Summe auf das annualisierte Mittel der "
                      "kuratierten Hochwasser-Ereignisliste (~6 Todesfälle/Jahr über "
                      "1990–2024). ACHTUNG: extrem tail-lastig — allein 2021 trägt rund "
                      "80 % der Todesfälle des Zeitraums; der Erwartungswert beschreibt "
                      "keine typische Jahreslage.",
     "source_refs": ["CEDIM_Hochwasser_2021", "Destatis_Todesursachen_23211"]},

    # ── Todesfälle durch Stürme ────────────────────────────────────────────────
    {"risk": "EXPECTED_ANNUAL_MORTALITY_STORM", "key": "fatality_rate_per_100k",
     "value": 0.35, "label": "Sturm-Letalität", "unit": "Tote/100k je Intensität",
     "source": "Kuratierte Ereignisliste (DWD)",
     "source_detail": "Todesfälle je 100.000 Einwohner bei voller Sturmintensität. "
                      "Kalibriert an Kyrill 2007 (13 Todesopfer in Deutschland, europaweit "
                      "47) und Friederike 2018 (8–10) — Größenordnung 5–15 in einem "
                      "schweren Sturmjahr.",
     "source_refs": ["DWD_Sturmereignisse", "Destatis_Todesursachen_23211"]},
    {"risk": "EXPECTED_ANNUAL_MORTALITY_STORM", "key": "tree_road_scale", "value": 8.0,
     "label": "Skalierung Baum-Straßen-Exposition", "unit": "Faktor",
     "source": "Modellannahme (dokumentiert)",
     "source_detail": "Skaliert das Produkt aus Kronen-/Waldanteil und Straßendeckung auf "
                      "0…1. Bewusst als Interaktion und nicht als zwei additive Terme: "
                      "Umstürzende Bäume an Straßen sind der dominierende Tötungsmechanismus, "
                      "und weder Baumbestand noch Straßendichte allein bilden ihn ab.",
     "source_refs": ["DWD_Sturmereignisse"]},
    {"risk": "EXPECTED_ANNUAL_MORTALITY_STORM", "key": "base_share", "value": 0.4,
     "label": "Grundanteil Sturmexposition", "unit": "Anteil",
     "source": "Modellannahme (dokumentiert)",
     "source_detail": "Anteil der Sturmtoten ohne Bezug zu Bäumen oder Bausubstanz "
                      "(fliegende Trümmer, Verkehrsunfälle bei Sturmböen).",
     "source_refs": ["DWD_Sturmereignisse"]},
    {"risk": "EXPECTED_ANNUAL_MORTALITY_STORM", "key": "tree_share", "value": 0.4,
     "label": "Anteil Baumsturz", "unit": "Anteil",
     "source": "Modellannahme (dokumentiert)",
     "source_detail": "Gewicht des Baum-Straßen-Mechanismus an der Sturmexposition.",
     "source_refs": ["DWD_Sturmereignisse"]},
    {"risk": "EXPECTED_ANNUAL_MORTALITY_STORM", "key": "building_share", "value": 0.2,
     "label": "Anteil Bauteilversagen", "unit": "Anteil",
     "source": "Modellannahme (dokumentiert)",
     "source_detail": "Gewicht des Gebäude-/Dachversagens (skaliert mit BUILDING_STABILITY).",
     "source_refs": ["DWD_Sturmereignisse"]},
    {"risk": "EXPECTED_ANNUAL_MORTALITY_STORM", "key": "calibration", "value": 1.0,
     "label": "Kalibrierfaktor Sturm-Mortalität", "unit": "Faktor",
     "source": "Kuratierte Ereignisliste",
     "source_detail": "Skaliert die nationale Summe auf das annualisierte Mittel der "
                      "kuratierten Sturm-Ereignisliste (~1 Todesfall/Jahr im Mittel, "
                      "5–15 in einem schweren Sturmjahr).",
     "source_refs": ["DWD_Sturmereignisse"]},

    # ── Verletzte: je Gefahr getrennt (nicht-tödlich) ──────────────────────────
    # Vorher EIN Risiko mit max() über drei Gefahren. Das war nicht nur unsauber,
    # sondern falsch: Verletzte aus Flut und Sturm sind additiv, nicht alternativ.
    {"risk": "EXPECTED_ANNUAL_INJURIES", "key": "rate_per_100k", "value": 90.0,
     "label": "Verletztenrate Hochwasser", "unit": "Verletzte/100k je Intensität",
     "source": "ICD-10 X38 (Destatis) / BBK",
     "source_detail": "NICHT-TÖDLICH Verletzte je 100.000 Einwohner bei voller "
                      "Hochwasserintensität; die Todesfälle stehen im eigenen Kanal, damit "
                      "nichts doppelt bewertet wird. Amtliche Bezugsgröße sind die "
                      "ICD-10-Außenursachen X38 (Opfer einer Überschwemmung) in der "
                      "Krankenhausstatistik — dort als Nebendiagnose kodiert. Ein "
                      "erheblicher Teil der Verletzungen entsteht erst bei den "
                      "Aufräumarbeiten nach dem Ereignis.",
     "source_refs": ["Destatis_Krankenhausdiagnosen_23131", "BBK_Hochwasserschutzfibel"]},
    {"risk": "EXPECTED_ANNUAL_INJURIES_STORM", "key": "rate_per_100k", "value": 55.0,
     "label": "Verletztenrate Sturm", "unit": "Verletzte/100k je Intensität",
     "source": "ICD-10 X37/X33 (Destatis) / DWD",
     "source_detail": "Nicht-tödlich Verletzte je 100.000 Einwohner bei voller "
                      "Sturmintensität. Amtliche Bezugsgröße: ICD-10 X37 (Opfer eines "
                      "Sturms) und X33 (Blitzschlag). Das Verhältnis Verletzte je Todesfall "
                      "ist bei Sturm hoch — viele Verletzte, wenige Tote — und schließt "
                      "Verletzungen bei Dachreparaturen nach dem Ereignis ein.",
     "source_refs": ["Destatis_Krankenhausdiagnosen_23131", "DWD_Sturmereignisse"]},
    {"risk": "EXPECTED_ANNUAL_INJURIES_LANDSLIDE", "key": "rate_per_100k", "value": 5.0,
     "label": "Verletztenrate Hangrutsch", "unit": "Verletzte/100k je Intensität",
     "source": "ICD-10 X36 (Destatis)",
     "source_detail": "Nicht-tödlich Verletzte je 100.000 Einwohner bei voller "
                      "Hangrutsch-Intensität (ICD-10 X36). Außerhalb steilen Geländes "
                      "liegt der Kanal nahe null — das ist ehrlich und informativ, kein "
                      "Mangel.",
     "source_refs": ["Destatis_Krankenhausdiagnosen_23131"]},

    # ── Psychische Gesundheit ───────────────────────────────────────────────────
    {"risk": "EXPECTED_ANNUAL_MENTAL_HEALTH", "key": "rate_per_100k", "value": 1500.0,
     "label": "Basisrate psychischer Fälle", "unit": "Fälle/100k·a",
     "source": "RKI / UBA (Modellannahme)",
     "source_detail": "Basisrate klimaassoziierter psychischer Belastungsfälle je 100k; "
                      "Treiber = Hitze-AF plus Extremereignis-/Kaskadenanteil. Editierbar.",
     "source_refs": ["RKI_Hitzemortalitaet"]},
    {"risk": "EXPECTED_ANNUAL_MENTAL_HEALTH", "key": "beta_per_hotday", "value": 0.0012,
     "label": "AF-Steigung je Hitzetag", "unit": "1/Hitzetag", "source": "RKI/Winklmayr",
     "source_detail": _HEAT_AF, "source_refs": ["RKI_Hitzemortalitaet"]},
    {"risk": "EXPECTED_ANNUAL_MENTAL_HEALTH", "key": "hotday_threshold", "value": 10.0,
     "label": "Hitzetage-Schwelle", "unit": "Hitzetage/Jahr", "source": "Modellannahme",
     "source_detail": "Schwelle für den hitzegetriebenen Anteil psychischer Belastung.",
     "source_refs": ["RKI_Hitzemortalitaet"]},
    {"risk": "EXPECTED_ANNUAL_MENTAL_HEALTH", "key": "event_share", "value": 0.3,
     "label": "Ereignis-Anteil (Extremereignisse)", "unit": "Anteil",
     "source": "Post-Desaster-Prävalenzstudien (Größenordnung, Modellannahme)",
     "source_detail": "Zusatztreiber neben der Hitze-AF: Treiber = min(1; AF + Anteil · "
                      "Ereignisintensität). Bei voller Extremereignis-Intensität (Compound/"
                      "Kaskade/Dürre) kommen bis zu 30 % der Basisrate als ereignisbedingte "
                      "Belastungsfälle hinzu — Größenordnung aus Prävalenzstudien nach "
                      "Flutkatastrophen (PTBS/Depression/Angst bei ~20-30 % der Betroffenen, "
                      "z. B. Ahrtal-Kohorten). Dokumentierte, editierbare Modellannahme.",
     "source_refs": []},

    # ── Betroffene / Evakuierte ─────────────────────────────────────────────────
    {"risk": "EXPECTED_ANNUAL_AFFECTED_EVACUATED", "key": "rate_per_100k", "value": 2500.0,
     "label": "Betroffenenrate je Ereignisintensität", "unit": "Personen/100k",
     "source": "BBK / Prognos (Modellannahme)",
     "source_detail": "Betroffene/evakuierte Personen je 100k bei voller (normierter) Flut-/"
                      "Sturmflut-/Feuerintensität der Zelle. Editierbar.",
     "source_refs": ["BBK_Hochwasserschutzfibel", "Prognos_Klimaschaeden_2023"]},

    # ── Wärmebelastungsstunden ──────────────────────────────────────────────────
    {"risk": "EXPECTED_THERMAL_STRESS_HOURS", "key": "hours_ref_per_100k", "value": 400.0,
     "label": "Belastungsstunden bei Referenz-Hitze", "unit": "Stunden/Jahr je 100k",
     "source": "UBA MK3.1 (Modellannahme)",
     "source_detail": "Wärmebelastungsstunden je 100k Einwohner bei den Referenz-Hitzetagen; "
                      "skaliert linear mit den Zell-Hitzetagen.",
     "source_refs": ["RKI_Hitzemortalitaet"]},
    {"risk": "EXPECTED_THERMAL_STRESS_HOURS", "key": "reference_hotdays", "value": 20.0,
     "label": "Referenz-Hitzetage", "unit": "Hitzetage/Jahr",
     "source": "Gesetztes Bezugsniveau (Modellannahme, dokumentiert)",
     "source_detail": "Bezugsniveau der Hitzetage, bei dem die Referenz-Belastungs"
                      "stunden gelten; der Treiber ist das Verhältnis HD_Zelle / 20. "
                      "GESETZTE Größe (§3.9, Kategorie Abgeschätzt), KEIN "
                      "Modellaggregat über "
                      "Deutschland — Größenordnung an der DWD-Rasterklimatologie "
                      "heißer Tage orientiert (Bundesmittel ~10–20 Tage/Jahr, "
                      "Ballungsräume darüber). Als reiner Skalierungsnenner wirkt sie "
                      "linear auf den Belastungsstunden-Ausweis; eine Herleitung folgt "
                      "mit der Methodik-Ausarbeitung dieses Screening-nahen Kanals. "
                      "Quellenzuordnung korrigiert (vorher fälschlich Starkregen-Raster).",
     "source_refs": ["DWD_CDC_Rasterklimatologie"]},

    # ── Schadstoff-Belastungsstunden ────────────────────────────────────────────
    {"risk": "EXPECTED_POLLUTANT_EXPOSURE_HOURS", "key": "hours_ref_per_100k", "value": 250.0,
     "label": "Schadstoffstunden bei Referenz-Hitze", "unit": "Stunden/Jahr je 100k",
     "source": "UBA (Modellannahme)",
     "source_detail": "Schadstoff-Belastungsstunden (bodennahes Ozon/Feinstaub) je 100k bei "
                      "Referenz-Hitzetagen; Ozonbildung korreliert mit Hitze.",
     "source_refs": ["RKI_Hitzemortalitaet"]},
    {"risk": "EXPECTED_POLLUTANT_EXPOSURE_HOURS", "key": "reference_hotdays", "value": 20.0,
     "label": "Referenz-Hitzetage", "unit": "Hitzetage/Jahr", "source": "DWD/Modellannahme",
     "source_detail": "Bezugsniveau der Hitzetage für die Referenz-Schadstoffstunden.",
     "source_refs": ["DWD_CDC_Starkregen"]},

    # ── Monetäre Sektorschäden: max. Jahresverlustrate je Risiko (Schicht B §6.2) ──
    {"risk": "EXPECTED_BUILDING_DAMAGE_EUR", "key": "max_loss_rate", "value": 0.008,
     "label": "Max. Jahresverlustrate", "unit": "Anteil/a", "source": "GDV/Prognos (Modellannahme)",
     "source_detail": "Anteil des Gebäude-Assetwerts, der bei voller Hazard-Intensität "
                      "jährlich als Schaden anfällt; über die konvexe Schadenskurve mit der "
                      "Intensität skaliert.", "source_refs": ["Prognos_Klimaschaeden_2023"]},
    {"risk": "EXPECTED_TRANSPORT_DAMAGE_EUR", "key": "max_loss_rate", "value": 0.02,
     "label": "Max. Jahresverlustrate", "unit": "Anteil/a", "source": "Prognos (Modellannahme)",
     "source_detail": "Verlustrate des Verkehrsasset-Ersatzwerts bei voller Intensität.",
     "source_refs": ["Prognos_Klimaschaeden_2023"]},
    {"risk": "EXPECTED_ENERGY_INFRA_DAMAGE_EUR", "key": "max_loss_rate", "value": 0.02,
     "label": "Max. Jahresverlustrate", "unit": "Anteil/a", "source": "Prognos/dena (Modellannahme)",
     "source_detail": "Verlustrate des Energieasset-Ersatzwerts bei voller Intensität.",
     "source_refs": ["Prognos_Klimaschaeden_2023"]},
    {"risk": "EXPECTED_TELECOM_DAMAGE_EUR", "key": "max_loss_rate", "value": 0.02,
     "label": "Max. Jahresverlustrate", "unit": "Anteil/a", "source": "Prognos (Modellannahme)",
     "source_detail": "Verlustrate des Telekom-Asset-Ersatzwerts bei voller Intensität.",
     "source_refs": ["Prognos_Klimaschaeden_2023"]},
    {"risk": "EXPECTED_WATER_WASTEWATER_DAMAGE_EUR", "key": "max_loss_rate", "value": 0.015,
     "label": "Max. Jahresverlustrate", "unit": "Anteil/a", "source": "Prognos/DWA (Modellannahme)",
     "source_detail": "Verlustrate des Ver-/Entsorgungsasset-Ersatzwerts bei voller Intensität.",
     "source_refs": ["Prognos_Klimaschaeden_2023"]},
    {"risk": "EXPECTED_AGRICULTURAL_DAMAGE_EUR", "key": "max_loss_rate", "value": 0.15,
     "label": "Max. Ertragsverlustrate", "unit": "Anteil/a", "source": "Prognos/StatBA (Modellannahme)",
     "source_detail": "Anteil des Ertragswerts je ha, der bei voller Dürre-/Hitzeintensität "
                      "verloren geht.", "source_refs": ["Prognos_Klimaschaeden_2023"]},
    {"risk": "EXPECTED_SOIL_LOSS_DEGRADATION_EUR", "key": "max_loss_rate", "value": 0.01,
     "label": "Max. Jahresverlustrate", "unit": "Anteil/a", "source": "Prognos (Modellannahme)",
     "source_detail": "Anteil des Bodenwerts je ha, der bei voller Erosionsintensität jährlich "
                      "degradiert.", "source_refs": ["Prognos_Klimaschaeden_2023"]},
    {"risk": "EXPECTED_ECOSYSTEM_SERVICE_LOSS", "key": "max_loss_rate", "value": 0.08,
     "label": "Max. Leistungsverlustrate", "unit": "Anteil/a", "source": "TEEB-DE (Modellannahme)",
     "source_detail": "Anteil der jährlichen Ökosystemleistung je ha, der bei voller "
                      "Degradationsintensität verloren geht.", "source_refs": ["TEEB_DE_Naturkapital"]},
    {"risk": "EXPECTED_FISHERIES_ECONOMIC_LOSS_EUR", "key": "max_loss_rate", "value": 0.20,
     "label": "Max. Ertragsverlustrate", "unit": "Anteil/a", "source": "Modellannahme",
     "source_detail": "Anteil des Fischereiwerts je Gewässer-ha bei voller Wärme-/"
                      "Niedrigwasserintensität.", "source_refs": ["Prognos_Klimaschaeden_2023"]},
    {"risk": "EXPECTED_AQUACULTURE_DAMAGE_EUR", "key": "max_loss_rate", "value": 0.25,
     "label": "Max. Ertragsverlustrate", "unit": "Anteil/a", "source": "Modellannahme",
     "source_detail": "Anteil des Aquakulturwerts je Gewässer-ha bei voller Wärme-/"
                      "Niedrigwasserintensität.", "source_refs": ["Prognos_Klimaschaeden_2023"]},
    {"risk": "EXPECTED_CLIMATE_MIGRATION_COSTS_EUR", "key": "cost_ref_per_100k", "value": 400_000.0,
     "label": "Referenz-Migrationskosten je 100k", "unit": "€/Jahr je 100k",
     "source": "Prognos (Modellannahme)",
     "source_detail": "Klimabedingte Umsiedlungs-/Verdrängungskosten je 100k Einwohner bei "
                      "voller (normierter) Küsten-/Flut-/Dürreintensität. In DE geringe, aber "
                      "ausgewiesene Größenordnung.", "source_refs": ["Prognos_Klimaschaeden_2023"]},

    # ── Umwelt-Flächen-/Artenverlust (Schicht B §6.4) ───────────────────────────
    {"risk": "EXPECTED_BIODIVERSITY_LOSS", "key": "species_loss_per_ha", "value": 0.0006,
     "label": "Artenverlustrate je ha", "unit": "Arten/ha·a", "source": "BfN/UBA (Modellannahme)",
     "source_detail": "Lokal verlorene Arten je ha Naturfläche bei voller Intensität "
                      "(Wärme/Dürre/Feuer); über den Kostensatz (€/Art) monetarisiert.",
     "source_refs": ["TEEB_DE_Naturkapital"]},
    {"risk": "EXPECTED_HABITAT_LOSS", "key": "loss_rate", "value": 0.02,
     "label": "Habitatverlustrate", "unit": "ha/ha·a", "source": "BfN (Modellannahme)",
     "source_detail": "Anteil der exponierten Naturfläche, der bei voller Intensität "
                      "(Dürre/Feuer/Meeresspiegel) jährlich als Habitat verloren geht.",
     "source_refs": ["TEEB_DE_Naturkapital"]},
    {"risk": "EXPECTED_SOIL_DEGRADATION", "key": "loss_rate", "value": 0.03,
     "label": "Bodendegradationsrate", "unit": "ha/ha·a", "source": "BGR/UBA (Modellannahme)",
     "source_detail": "Anteil der Ackerfläche, der bei voller Intensität (Dürre/Erosion/"
                      "Versalzung) jährlich degradiert.", "source_refs": ["TEEB_DE_Naturkapital"]},
    {"risk": "EXPECTED_VEGETATION_DAMAGE", "key": "loss_rate", "value": 0.05,
     "label": "Vegetationsschadensrate", "unit": "ha/ha·a", "source": "Waldzustandsbericht (Modellannahme)",
     "source_detail": "Anteil der Wald-/Agrarfläche mit Vegetationsschaden bei voller "
                      "Intensität (Dürre/Hitze/Feuer).", "source_refs": ["TEEB_DE_Naturkapital"]},
]

# Globale Schicht-B-Parameter (ID ``impact.<key>``): Assetwerte, Konsolidierungsfaktoren,
# Kurvenexponent. Editier- und override-fähig, in der Registry unter Kategorie "impact".
IMPACT_GLOBAL_SPECS: list[dict] = [
    {"key": "building_value_eur_m2", "value": 2000.0, "label": "Gebäudewert je m² BGF",
     "unit": "€/m²", "source": "Destatis Baupreise / GDV (Größenordnung)",
     "source_detail": "Wiederherstellungswert je m² Bruttogeschossfläche; multipliziert mit "
                      "der geschätzten Geschossfläche der Zelle (Bebauungsgrad × Fläche × Geschosse).",
     "source_refs": ["Prognos_Klimaschaeden_2023"]},
    {"key": "agri_value_eur_ha", "value": 12_000.0, "label": "Agrar-Ertragswert je ha",
     "unit": "€/ha", "source": "StatBA Agrar (Größenordnung)",
     "source_detail": "Ertrags-/Bodenwert je ha landwirtschaftlicher Fläche.",
     "source_refs": ["Prognos_Klimaschaeden_2023"]},
    {"key": "soil_value_eur_ha", "value": 30_000.0, "label": "Bodenwert je ha",
     "unit": "€/ha", "source": "BGR/Modellannahme",
     "source_detail": "ÖKONOMISCHER Bodenwert je ha (Ertrags-/Wiederherstellungswert der "
                      "Nutzfläche) für das monetäre Erosions-/Degradationsrisiko. Abgrenzung "
                      "(§8/B5): Der ökologische Bodenfunktionswert (Naturhaushalt) derselben "
                      "Fläche ist getrennt über das Umweltrisiko „Bodendegradation“ bewertet "
                      "(dortiger Kostensatz €/ha) — keine Doppelzählung.",
     "source_refs": ["Prognos_Klimaschaeden_2023"]},
    {"key": "esl_value_eur_ha", "value": 3000.0, "label": "Ökosystemleistungswert je ha·a",
     "unit": "€/ha·a", "source": "TEEB-DE / Grunewald",
     "source_detail": "Jährlicher Wert der Ökosystemleistungen je ha Wald-/Grünfläche.",
     "source_refs": ["TEEB_DE_Naturkapital"]},
    {"key": "fisheries_value_eur_ha", "value": 5000.0, "label": "Fischerei-/Aquakulturwert je ha·a",
     "unit": "€/ha·a", "source": "Modellannahme",
     "source_detail": "Jährlicher Ertragswert je ha Gewässer-/Aquakulturfläche.",
     "source_refs": ["Prognos_Klimaschaeden_2023"]},
    {"key": "k_indirect", "value": 0.25, "label": "k_indirekt (Folgekosten-Multiplikator)",
     "unit": "Anteil", "source": "Prognos 2023 (I/O-Analyse)",
     "source_detail": "Indirekte Verluste (Betriebs-/Lieferkettenunterbrechung, Standort, "
                      "verzögerte Schäden) als Anteil der DIREKTEN Sektorschäden — konsolidiert "
                      "die früher einzeln (doppelt) gezählten Folgekosten-Risiken. Band ~0,18–0,5.",
     "source_refs": ["Prognos_Klimaschaeden_2023"]},
    {"key": "restoration_share", "value": 0.15, "label": "Restaurierungsquote",
     "unit": "Anteil", "source": "Modellannahme",
     "source_detail": "Wiederherstellungskosten als Anteil der direkten Sektorschäden. "
                      "Teilkennzahl (Teilmenge) — NICHT additiv in die Gesamtsumme.",
     "source_refs": ["Prognos_Klimaschaeden_2023"]},
    {"key": "damage_exponent", "value": 1.5, "label": "Schadenskurven-Exponent",
     "unit": "–", "source": "HOWAS21/JRC (Größenordnung)",
     "source_detail": "Konvexität der Schadenskurve (Schaden ∝ Intensität^Exponent). >1 = "
                      "überproportionaler Schaden bei hoher Intensität (Tiefe-Schaden-Kurven).",
     "source_refs": ["Prognos_Klimaschaeden_2023"]},
    {"key": "floor_height_m", "value": 3.5, "label": "Mittlere Geschosshöhe",
     "unit": "m", "source": "Bau-Größenordnung DE (Modellannahme)",
     "source_detail": "Schätzt die Geschosszahl aus der OSM-Gebäudehöhe: Geschosse = "
                      "max(1; mittlere Gebäudehöhe / Geschosshöhe); Bruttogeschossfläche = "
                      "Bebauungsgrad × Zellfläche × Geschosse — Basis des Gebäude-Assetwerts "
                      "(× €/m²). Wohngebäude haben ~2,6-3,0 m lichte Geschosshöhe (zzgl. "
                      "Decken), Gewerbe-/Altbauten 3,5-4,5 m; 3,5 m als Mittel über den "
                      "gemischten Bestand. Kleinere Werte erhöhen die geschätzte "
                      "Geschossfläche und damit die Gebäudeschäden.",
     "source_refs": []},
]


def _infra_value_specs() -> list[dict]:
    """Klassenspezifische Ersatzwerte der vier KRITIS-Infrastruktur-Sektoren.

    Generiert aus der zentralen Taxonomie (app/data/infra_assets.py), Keys
    ``<sektor>_value_<klasse>_eur``. Ersetzt die früheren Pauschalen
    ``energy/water/transport/telecom_asset_value_eur`` (ein Mittelwert je
    Sektor kann Umspannwerk und Ortsnetztrafo nicht zugleich abbilden).
    """
    from app.data import infra_assets

    return [
        {"key": infra_assets.value_param_key(sector, cls),
         "value": spec["value_eur"],
         "label": f"Ersatzwert {spec['label']}",
         "unit": "€/Stück",
         "source": "Prognos/BBK (Modellannahme je Anlagenklasse)",
         "source_detail": spec["source_detail"],
         "source_refs": list(infra_assets.VALUE_SOURCE_REFS)}
        for sector, classes in infra_assets.ASSET_CLASSES.items()
        for cls, spec in classes.items()
    ]


IMPACT_GLOBAL_SPECS += _infra_value_specs()
