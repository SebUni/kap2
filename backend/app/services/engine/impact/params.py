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
    "RKI-Anteilen 2026 (6,5/12,9/25,2/55,5 %), der Zensus-Altersstruktur und den "
    "altersspezifischen Basissterberaten ergeben sich die hinterlegten Faktoren. "
    "Kontrolle: Das Modell reproduziert die RKI-Altersverteilung auf <1 Prozentpunkt.")

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
    {"risk": "EXPECTED_ANNUAL_MORTALITY", "key": "beta_85p_sued", "value": 0.0531,
     "label": "Kurvensteigung 85+ (Süd)", "unit": "1/K",
     "source": "Winklmayr u. a. 2022, Abb. 3/4",
     "source_detail": "Aus der publizierten Kurve: RR ≈ 1,25 bei 25 °C über der "
                      "Süd-Schwelle 20,8 °C — die flachste der drei Regionen. " + _ERF,
     "source_refs": ["Winklmayr_2022"]},

    # ── Hitzemortalität: Altersband-Steigungsfaktoren ──────────────────────────
    {"risk": "EXPECTED_ANNUAL_MORTALITY", "key": "beta_factor_u65", "value": 0.404,
     "label": "Steigungsfaktor Band <65", "unit": "Faktor",
     "source": "Hergeleitet aus RKI-Altersverteilung", "source_detail": _BETA_FACTOR,
     "source_refs": ["RKI_Wochenbericht_Hitzemortalitaet", "Winklmayr_2022"]},
    {"risk": "EXPECTED_ANNUAL_MORTALITY", "key": "beta_factor_a65_74", "value": 0.577,
     "label": "Steigungsfaktor Band 65–74", "unit": "Faktor",
     "source": "Hergeleitet aus RKI-Altersverteilung", "source_detail": _BETA_FACTOR,
     "source_refs": ["RKI_Wochenbericht_Hitzemortalitaet", "Winklmayr_2022"]},
    {"risk": "EXPECTED_ANNUAL_MORTALITY", "key": "beta_factor_a75_84", "value": 0.620,
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
    {"risk": "EXPECTED_ANNUAL_MORTALITY", "key": "baseline_mort_u65", "value": 180.0,
     "label": "Basissterblichkeit <65", "unit": "Tote/100k·a",
     "source": "Destatis Todesursachenstatistik",
     "source_detail": "Altersspezifische rohe Sterberate. Ersetzt die frühere pauschale "
                      "Rate von 1.130/100k: Ohne Altersdifferenzierung ist die "
                      "Altersverteilung der Hitzetoten nicht darstellbar — die 85+-Gruppe "
                      "hat die ~86-fache Basissterblichkeit der unter 65-Jährigen. "
                      "Kontrolle: Die vier Bänder summieren sich mit der Zensus-"
                      "Altersstruktur auf ~977.000 Sterbefälle/Jahr (DE-Ist ~1,02 Mio).",
     "source_refs": ["Destatis_Sterbefaelle_Altersgruppen"]},
    {"risk": "EXPECTED_ANNUAL_MORTALITY", "key": "baseline_mort_a65_74", "value": 1800.0,
     "label": "Basissterblichkeit 65–74", "unit": "Tote/100k·a",
     "source": "Destatis Todesursachenstatistik",
     "source_detail": "Altersspezifische rohe Sterberate des Bands 65–74.",
     "source_refs": ["Destatis_Sterbefaelle_Altersgruppen"]},
    {"risk": "EXPECTED_ANNUAL_MORTALITY", "key": "baseline_mort_a75_84", "value": 4600.0,
     "label": "Basissterblichkeit 75–84", "unit": "Tote/100k·a",
     "source": "Destatis Todesursachenstatistik",
     "source_detail": "Altersspezifische rohe Sterberate des Bands 75–84.",
     "source_refs": ["Destatis_Sterbefaelle_Altersgruppen"]},
    {"risk": "EXPECTED_ANNUAL_MORTALITY", "key": "baseline_mort_a85p", "value": 15500.0,
     "label": "Basissterblichkeit 85+", "unit": "Tote/100k·a",
     "source": "Destatis Todesursachenstatistik",
     "source_detail": "Altersspezifische rohe Sterberate des Bands 85+ — der mit Abstand "
                      "größte Treiber der absoluten Hitzemortalität.",
     "source_refs": ["Destatis_Sterbefaelle_Altersgruppen"]},

    # ── Hitzemortalität: Verteilungs- und Kalibrierparameter ───────────────────
    {"risk": "EXPECTED_ANNUAL_MORTALITY", "key": "weekly_temp_sd", "value": 2.0,
     "label": "Streuung der Sommer-Wochenmittel", "unit": "K",
     "source": "DWD-CDC-Monatsraster (abgeleitet)",
     "source_detail": "Standardabweichung der Wochenmitteltemperaturen im Sommer. Aus den "
                      "DWD-Monatsrastern abgeleitet: Streuung der Monatsmittel über "
                      "Monate und Jahre = 1,03 K (davon 0,40 K zwischen den Monaten, "
                      "1,01 K zwischen den Jahren), zuzüglich der synoptischen "
                      "Wochenstreuung innerhalb eines Monats (~1,7 K) ergibt ~2,0 K. "
                      "Der Parameter ist wirkungsstark, weil die Kurve konvex ist — "
                      "deshalb datengestützt hergeleitet und nicht auf den Zielwert "
                      "getrimmt.",
     "source_refs": ["DWD_CDC_Monatsraster_Temperatur"]},
    {"risk": "EXPECTED_ANNUAL_MORTALITY", "key": "summer_weeks", "value": 13.0,
     "label": "Zahl der Sommerwochen", "unit": "Wochen",
     "source": "Modellabgrenzung (Juni–August)",
     "source_detail": "Die Expositionsrechnung läuft über die 13 Wochen der Monate Juni "
                      "bis August — konsistent zur Sommermitteltemperatur aus den "
                      "DWD-Monatsrastern (Jun/Jul/Aug). Das RKI rechnet über das längere "
                      "Sommerhalbjahr (KW 15–40); der Beitrag der kühleren Randwochen "
                      "steckt im Kalibrierfaktor.",
     "source_refs": ["Winklmayr_2022"]},
    {"risk": "EXPECTED_ANNUAL_MORTALITY", "key": "calibration", "value": 1.44,
     "label": "Nationaler Kalibrierfaktor", "unit": "Faktor",
     "source": "Kalibrierung gegen die RKI-Jahresreihe",
     "source_detail": "EINZIGER freier Parameter der Hitzemortalität — alle übrigen "
                      "Koeffizienten stammen aus der Literatur. Bestimmt aus einer "
                      "bundesweiten Rechnung über 208.622 besiedelte 1-km-Zellen "
                      "(bevölkerungsgewichtete Sommertemperatur 19,01 °C gegenüber "
                      "18,55 °C im Flächenmittel): Das Modell liefert ~4.625 Sterbefälle, "
                      "das Mittel der signifikanten RKI-Hitzejahre liegt bei ~6.656. "
                      "Der Rest von 1,44 deckt die im 1-km-Raster nicht aufgelöste "
                      "Wärmeinsel-Konvexität, die Randwochen des Sommerhalbjahrs und die "
                      "Nachlaufwochen der RKI-Methodik ab — alle drei wirken in dieselbe "
                      "Richtung.",
     "source_refs": ["Winklmayr_2022", "RKI_Wochenbericht_Hitzemortalitaet"]},
    {"risk": "EXPECTED_ANNUAL_MORTALITY", "key": "healthcare_modifier_span", "value": 0.5,
     "label": "Spannweite Versorgungs-Modifikator", "unit": "Faktor",
     "source": "Modellannahme (dokumentiert)",
     "source_detail": "Der Zellmodifikator läuft von 1 − Spanne/2 bis 1 + Spanne/2 über "
                      "den normierten Gesundheitszugang. Er ersetzt bewusst g(V̂): Mit "
                      "expliziten Altersbändern zählte g die Demografie ein zweites und "
                      "drittes Mal (HEAT_SENSITIVITY und VULNERABLE_GROUPS_SHARE enthalten "
                      "beide den Verwundbaren-Anteil — REVIEW_BERECHNUNGSLOGIK V-E). "
                      "Jetzt steckt die Demografie genau einmal in der Altersschichtung.",
     "source_refs": ["RKI_Hitzemortalitaet"]},

    # ── Hitzemorbidität ─────────────────────────────────────────────────────────
    {"risk": "EXPECTED_ANNUAL_MORBIDITY", "key": "rate_per_100k", "value": 8000.0,
     "label": "Basis-Morbiditätsrate", "unit": "Fälle/100k·a",
     "source": "UBA MK3.1 / RKI (Modellannahme)",
     "source_detail": "Basisrate hitzeassoziierter Behandlungsfälle je 100k; die attributable "
                      "Fraktion (Hitzetage) reduziert sie auf die klimabedingten Fälle. "
                      "Dokumentierte, editierbare Modellannahme.",
     "source_refs": ["RKI_Hitzemortalitaet"]},
    {"risk": "EXPECTED_ANNUAL_MORBIDITY", "key": "beta_per_hotday", "value": 0.0016,
     "label": "AF-Steigung je Hitzetag", "unit": "1/Hitzetag", "source": "RKI/Winklmayr",
     "source_detail": _HEAT_AF, "source_refs": ["RKI_Hitzemortalitaet"]},
    {"risk": "EXPECTED_ANNUAL_MORBIDITY", "key": "hotday_threshold", "value": 8.0,
     "label": "Hitzetage-Schwelle", "unit": "Hitzetage/Jahr", "source": "RKI/Winklmayr",
     "source_detail": "Akklimatisierungsschwelle für hitzeassoziierte Morbidität.",
     "source_refs": ["RKI_Hitzemortalitaet"]},

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
                      "Zelle vom Bundesmittel (22 %).",
     "source_refs": ["CEDIM_Hochwasser_2021"]},
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
     "label": "Referenz-Hitzetage", "unit": "Hitzetage/Jahr", "source": "DWD/Modellannahme",
     "source_detail": "Bezugsniveau der Hitzetage, bei dem die Referenz-Belastungsstunden gelten.",
     "source_refs": ["DWD_CDC_Starkregen"]},

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
