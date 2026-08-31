"""Zentrale Quellen-Bibliographie: zitierfähige Herkunft je Kostenkennwert.

Jede belegte (nicht als reine Modellannahme gekennzeichnete) Quelle wird hier GENAU
EINMAL definiert und über einen Kurz-Key referenziert. Im Katalog verweist eine
Maßnahme per ``source_refs`` (``{feld: [key, ...]}``) auf die Keys, sodass eine
mehrfach genutzte Quelle nur an einer Stelle gepflegt wird und jeder Kostenparameter
im Hover-Tooltip seine vollständige, nachprüfbare Herkunft zeigen kann.

Jeder Eintrag trägt:
  ieee         vollständige Zitation im IEEE-Stil (deutsch lokalisiert)
  url          Live-Adresse der Quelle
  archive_url  Wayback-Machine-Permalink (Snapshot, falls die Live-Quelle offline geht)
  accessed     Zugriffsdatum (ISO)

Snapshot-Konvention (Internet Archive / Wayback Machine):
  # frisch archivieren und Permalink aus dem Location-Header lesen:
  curl -s -I "https://web.archive.org/save/<url>" | grep -i '^location:'
  # bereits vorhandenen jüngsten Snapshot finden:
  curl -s "https://web.archive.org/cdx/search/cdx?url=<url>&output=json&limit=-1"
  -> https://web.archive.org/web/<timestamp>/<url>
"""

from __future__ import annotations

# Kurz-Key -> Bibliografie-Eintrag. Keys sind stabil (werden aus catalog.source_refs
# referenziert); Umbenennen erfordert Anpassung der referenzierenden Maßnahmen.
SOURCE_REFERENCES: dict[str, dict[str, str]] = {
    "Regionalstatistik_GENESIS": {
        "ieee": "Statistische Ämter des Bundes und der Länder, „Regionaldatenbank "
                "Deutschland (GENESIS-Online),“ Düsseldorf, Deutschland. [Online]. "
                "Verfügbar: https://www.regionalstatistik.de. [Zugriff: 6. Juli 2026].",
        "url": "https://www.regionalstatistik.de",
        "archive_url": "https://web.archive.org/web/2026/https://www.regionalstatistik.de/",
        "accessed": "2026-07-06",
    },
    "BuGG_Marktreport_2024": {
        "ieee": "Bundesverband GebäudeGrün e.V. (BuGG), „BuGG-Marktreport Gebäudegrün "
                "2024,“ Berlin, Deutschland, 2024. [Online]. Verfügbar: "
                "https://www.gebaeudegruen.info/fileadmin/website/downloads/"
                "bugg-fachinfos/Marktreport/BuGG_Marktreport_2024.pdf. "
                "[Zugriff: 4. Juli 2026].",
        "url": "https://www.gebaeudegruen.info/fileadmin/website/downloads/"
               "bugg-fachinfos/Marktreport/BuGG_Marktreport_2024.pdf",
        "archive_url": "https://web.archive.org/web/20250210042547/"
                       "https://www.gebaeudegruen.info/fileadmin/website/downloads/"
                       "bugg-fachinfos/Marktreport/BuGG_Marktreport_2024.pdf",
        "accessed": "2026-07-04",
    },
    "co2online_Dachbegruenung": {
        "ieee": "co2online gemeinnützige GmbH, „Dachbegrünung: Pflanzen, Kosten, "
                "Vorteile,“ Berlin, Deutschland. [Online]. Verfügbar: "
                "https://www.co2online.de/modernisieren-und-bauen/"
                "anpassung-an-den-klimawandel/dachbegruenung/. "
                "[Zugriff: 4. Juli 2026].",
        "url": "https://www.co2online.de/modernisieren-und-bauen/"
               "anpassung-an-den-klimawandel/dachbegruenung/",
        "archive_url": "https://web.archive.org/web/20260704082516/"
                       "https://www.co2online.de/modernisieren-und-bauen/"
                       "anpassung-an-den-klimawandel/dachbegruenung/",
        "accessed": "2026-07-04",
    },
    "BWB_Trinkbrunnen": {
        "ieee": "Berliner Wasserbetriebe, „Trinkbrunnen in Berlin,“ Berlin, "
                "Deutschland. [Online]. Verfügbar: https://www.bwb.de/de/"
                "trinkbrunnen.php. [Zugriff: 4. Juli 2026].",
        "url": "https://www.bwb.de/de/trinkbrunnen.php",
        "archive_url": "https://web.archive.org/web/20260704083542/"
                       "https://www.bwb.de/de/trinkbrunnen.php",
        "accessed": "2026-07-04",
    },
    "HTW_Stromspeicher_2025": {
        "ieee": "J. Weniger, N. Orth und N. Böhme, „Stromspeicher-Inspektion 2025,“ "
                "Hochschule für Technik und Wirtschaft (HTW) Berlin, Berlin, "
                "Deutschland, 2025. [Online]. Verfügbar: https://solar.htw-berlin.de/"
                "studien/stromspeicher-inspektion-2025/. [Zugriff: 4. Juli 2026].",
        "url": "https://solar.htw-berlin.de/studien/stromspeicher-inspektion-2025/",
        "archive_url": "https://web.archive.org/web/20260704083611/"
                       "https://solar.htw-berlin.de/studien/stromspeicher-inspektion-2025/",
        "accessed": "2026-07-04",
    },
    # ── Wasser / Starkregen / Versickerung ──────────────────────────────────
    "DWA_A138": {
        "ieee": "Deutsche Vereinigung für Wasserwirtschaft, Abwasser und Abfall e.V. (DWA), "
                "„Arbeitsblatt DWA-A 138-1: Anlagen zur Versickerung von Niederschlagswasser "
                "– Teil 1: Planung, Bau, Betrieb,“ Hennef, Deutschland, 2024. [Online]. "
                "Verfügbar: https://de.dwa.de/de/regelwerk-news-volltext/"
                "arbeitsblatt-dwa-a-138-1-anlagen-zur-versickerung-von-niederschlagswasser-"
                "teil-1-planung-bau-betrieb.html. [Zugriff: 4. Juli 2026].",
        "url": "https://de.dwa.de/de/regelwerk-news-volltext/arbeitsblatt-dwa-a-138-1-anlagen-"
               "zur-versickerung-von-niederschlagswasser-teil-1-planung-bau-betrieb.html",
        "archive_url": "https://web.archive.org/web/20260521145245/"
                       "https://de.dwa.de/de/regelwerk-news-volltext/arbeitsblatt-dwa-a-138-1-"
                       "anlagen-zur-versickerung-von-niederschlagswasser-teil-1-planung-bau-betrieb.html",
        "accessed": "2026-07-04",
    },
    "Baupreislexikon_Versickerung": {
        "ieee": "f:data GmbH (sirados Baudaten), „Mulden-Rigolenversickerung – aktuelle Preise "
                "für Bauelemente,“ Weimar, Deutschland. [Online]. Verfügbar: "
                "https://www.baupreislexikon.de/bauelement/mulden-rigolenversickerung. "
                "[Zugriff: 4. Juli 2026].",
        "url": "https://www.baupreislexikon.de/bauelement/mulden-rigolenversickerung",
        "archive_url": "https://web.archive.org/web/20231204035208/"
                       "https://www.baupreislexikon.de/bauelement/mulden-rigolenversickerung",
        "accessed": "2026-07-04",
    },
    "Agrarheute_Rueckhaltebecken": {
        "ieee": "agrarheute (Deutscher Landwirtschaftsverlag GmbH), „Regenrückhaltebecken "
                "gegen Überflutungen: Bauweise, Vorschriften und Kosten,“ München, Deutschland. "
                "[Online]. Verfügbar: https://www.agrarheute.com/management/betriebsfuehrung/"
                "rueckhaltebecken-gegen-ueberflutungen-bauweise-auflagen-kosten-621507. "
                "[Zugriff: 4. Juli 2026].",
        "url": "https://www.agrarheute.com/management/betriebsfuehrung/"
               "rueckhaltebecken-gegen-ueberflutungen-bauweise-auflagen-kosten-621507",
        "archive_url": "https://web.archive.org/web/20260303073601/"
                       "https://www.agrarheute.com/management/betriebsfuehrung/"
                       "rueckhaltebecken-gegen-ueberflutungen-bauweise-auflagen-kosten-621507",
        "accessed": "2026-07-04",
    },
    "DVGW_W392": {
        "ieee": "R. Prein, „Wasserverluste in Rohrnetzen – Bestimmung nach DVGW-Arbeitsblatt "
                "W 392,“ energie|wasser-praxis, Nr. 5/2019, DVGW Deutscher Verein des Gas- und "
                "Wasserfaches e.V., Bonn, Deutschland, 2019. [Online]. Verfügbar: "
                "https://www.dvgw.de/medien/dvgw/wasser/netze/wasserverluste-prein1905.pdf. "
                "[Zugriff: 4. Juli 2026].",
        "url": "https://www.dvgw.de/medien/dvgw/wasser/netze/wasserverluste-prein1905.pdf",
        "archive_url": "https://web.archive.org/web/20210917035135/"
                       "https://www.dvgw.de/medien/dvgw/wasser/netze/wasserverluste-prein1905.pdf",
        "accessed": "2026-07-04",
    },
    "Bremen_Entsiegelung": {
        "ieee": "Freie Hansestadt Bremen, Die Senatorin für Umwelt, Klima und Wissenschaft, "
                "„Förderung für die Entsiegelung von Flächen beantragen,“ Bremen, Deutschland. "
                "[Online]. Verfügbar: https://www.service.bremen.de/dienstleistungen/"
                "foerderung-fuer-die-entsiegelung-von-flaechen-beantragen-17485. "
                "[Zugriff: 4. Juli 2026].",
        "url": "https://www.service.bremen.de/dienstleistungen/"
               "foerderung-fuer-die-entsiegelung-von-flaechen-beantragen-17485",
        "archive_url": "https://web.archive.org/web/20240925212112/"
                       "https://www.service.bremen.de/dienstleistungen/"
                       "foerderung-fuer-die-entsiegelung-von-flaechen-beantragen-17485",
        "accessed": "2026-07-04",
    },
    # ── Gebäude / Hitze / Beläge ────────────────────────────────────────────
    "BBK_Hochwasserschutzfibel": {
        "ieee": "Bundesministerium für Wohnen, Stadtentwicklung und Bauwesen (BMWSB), "
                "„Hochwasserschutzfibel – Objektschutz und bauliche Vorsorge,“ Berlin, "
                "Deutschland, 2022. [Online]. Verfügbar: https://www.bmwsb.bund.de/"
                "SharedDocs/downloads/DE/publikationen/raumordnung/hochwasserschutzfibel.html. "
                "[Zugriff: 4. Juli 2026].",
        "url": "https://www.bmwsb.bund.de/SharedDocs/downloads/DE/publikationen/raumordnung/"
               "hochwasserschutzfibel.html",
        "archive_url": "https://web.archive.org/web/20251121213733/"
                       "https://www.bmwsb.bund.de/SharedDocs/downloads/DE/publikationen/"
                       "raumordnung/hochwasserschutzfibel.html",
        "accessed": "2026-07-04",
    },
    "Kostencheck_Rueckstauklappe": {
        "ieee": "kostencheck.de, „Rückstauklappe fürs Abwasser – Mit diesen Kosten ist zu "
                "rechnen,“ [Online]. Verfügbar: https://kostencheck.de/"
                "rueckstauklappe-abwasser-kosten. [Zugriff: 4. Juli 2026].",
        "url": "https://kostencheck.de/rueckstauklappe-abwasser-kosten",
        "archive_url": "https://web.archive.org/web/20260417193328/"
                       "https://kostencheck.de/rueckstauklappe-abwasser-kosten",
        "accessed": "2026-07-04",
    },
    "Asphaltshop_Dachbeschichtung": {
        "ieee": "Asphaltshop / KlimaBond, „KlimaBond ROOF SR – sonnenreflektierende "
                "Dachbeschichtung,“ [Online]. Verfügbar: https://www.asphalt-shop.de/"
                "klimabond-roof-sr-1.html. [Zugriff: 4. Juli 2026].",
        "url": "https://www.asphalt-shop.de/klimabond-roof-sr-1.html",
        "archive_url": "https://web.archive.org/web/20260616132244/"
                       "https://www.asphalt-shop.de/klimabond-roof-sr-1.html",
        "accessed": "2026-07-04",
    },
    "Kirschbaum_HellerAsphalt": {
        "ieee": "Kirschbaum Verlag, „Heller Asphalt zur Senkung der Temperaturen,“ Straße "
                "und Autobahn, Bonn, Deutschland. [Online]. Verfügbar: https://www.kirschbaum.de/"
                "fachzeitschriften/strasse-und-autobahn/aktuelles/artikel/"
                "heller-asphalt-zur-senkung-der-temperaturen.html. [Zugriff: 4. Juli 2026].",
        "url": "https://www.kirschbaum.de/fachzeitschriften/strasse-und-autobahn/aktuelles/"
               "artikel/heller-asphalt-zur-senkung-der-temperaturen.html",
        "archive_url": "https://web.archive.org/web/20230110091926/"
                       "https://www.kirschbaum.de/fachzeitschriften/strasse-und-autobahn/"
                       "aktuelles/artikel/heller-asphalt-zur-senkung-der-temperaturen.html",
        "accessed": "2026-07-04",
    },
    # ── Küste / Fluss / Fischerei ───────────────────────────────────────────
    "NLWKN_Generalplan_Kuestenschutz": {
        "ieee": "Niedersächsischer Landesbetrieb für Wasserwirtschaft, Küsten- und Naturschutz "
                "(NLWKN), „Generalplan Küstenschutz Niedersachsen/Bremen,“ Norden, Deutschland. "
                "[Online]. Verfügbar: https://www.nlwkn.niedersachsen.de/startseite/"
                "hochwasser_kustenschutz/kustenschutz/generalplane_fur_insel_und_kustenschutz/"
                "generalplan-kuestenschutz-45183.html. [Zugriff: 4. Juli 2026].",
        "url": "https://www.nlwkn.niedersachsen.de/startseite/hochwasser_kustenschutz/"
               "kustenschutz/generalplane_fur_insel_und_kustenschutz/generalplan-kuestenschutz-45183.html",
        "archive_url": "https://web.archive.org/web/20260217213953/"
                       "https://www.nlwkn.niedersachsen.de/startseite/hochwasser_kustenschutz/"
                       "kustenschutz/generalplane_fur_insel_und_kustenschutz/generalplan-kuestenschutz-45183.html",
        "accessed": "2026-07-04",
    },
    "UBA_Gewaesserrenaturierung": {
        "ieee": "Umweltbundesamt (UBA), „Finanzierung und Förderung von "
                "Gewässerrenaturierungen,“ Dessau-Roßlau, Deutschland. [Online]. Verfügbar: "
                "https://www.umweltbundesamt.de/finanzierung-foerderung-von. "
                "[Zugriff: 4. Juli 2026].",
        "url": "https://www.umweltbundesamt.de/finanzierung-foerderung-von",
        "archive_url": "https://web.archive.org/web/20260219102207/"
                       "https://www.umweltbundesamt.de/finanzierung-foerderung-von",
        "accessed": "2026-07-04",
    },
    "LfU_Bayern_Fischaufstieg": {
        "ieee": "Bayerisches Landesamt für Umwelt (LfU), „Beispiele von Maßnahmen zur "
                "Verbesserung der Durchgängigkeit an Querbauwerken (Fischaufstiegsanlagen),“ "
                "Augsburg, Deutschland. [Online]. Verfügbar: https://www.lfu.bayern.de/wasser/"
                "durchgaengigkeit/beispiele/index.htm. [Zugriff: 4. Juli 2026].",
        "url": "https://www.lfu.bayern.de/wasser/durchgaengigkeit/beispiele/index.htm",
        "archive_url": "https://web.archive.org/web/20210216150611/"
                       "https://www.lfu.bayern.de/wasser/durchgaengigkeit/beispiele/index.htm",
        "accessed": "2026-07-04",
    },
    # ── Land / Forst / Landwirtschaft ───────────────────────────────────────
    "AGDW_Wiederbewaldung": {
        "ieee": "AGDW – Die Waldeigentümer, „Wiederbewaldung und Waldumbau – Kulturkosten je "
                "Hektar (Infografiken),“ Berlin, Deutschland. [Online]. Verfügbar: "
                "https://www.waldeigentuemer.de/infografiken-wiederbewaldung-und-waldumbau/. "
                "[Zugriff: 4. Juli 2026].",
        "url": "https://www.waldeigentuemer.de/infografiken-wiederbewaldung-und-waldumbau/",
        "archive_url": "https://web.archive.org/web/20260511030627/"
                       "https://www.waldeigentuemer.de/infografiken-wiederbewaldung-und-waldumbau/",
        "accessed": "2026-07-04",
    },
    "KTBL_Feldbewaesserung": {
        "ieee": "Kuratorium für Technik und Bauwesen in der Landwirtschaft (KTBL) / "
                "Thünen-Institut, „Investitionen und Verfahrenskosten für die Feldbewässerung,“ "
                "Braunschweig/Darmstadt, Deutschland. [Online]. Verfügbar: "
                "https://literatur.thuenen.de/digbib_extern/dk041695.pdf. "
                "[Zugriff: 4. Juli 2026].",
        "url": "https://literatur.thuenen.de/digbib_extern/dk041695.pdf",
        "archive_url": "https://web.archive.org/web/20220702234502/"
                       "https://literatur.thuenen.de/digbib_extern/dk041695.pdf",
        "accessed": "2026-07-04",
    },
    "LfL_Pflanzenbau": {
        "ieee": "Bayerische Landesanstalt für Landwirtschaft (LfL), „Deckungsbeiträge und "
                "Kalkulationsdaten – Pflanzenbau,“ Freising, Deutschland. [Online]. Verfügbar: "
                "https://www.lfl.bayern.de/iba/pflanze/026149/index.php. "
                "[Zugriff: 4. Juli 2026].",
        "url": "https://www.lfl.bayern.de/iba/pflanze/026149/index.php",
        "archive_url": "https://web.archive.org/web/20220319222607/"
                       "https://www.lfl.bayern.de/iba/pflanze/026149/index.php",
        "accessed": "2026-07-04",
    },
    # ── Energie / Stadt / Bevölkerungsschutz ────────────────────────────────
    "RONT_Ortsnetzstation": {
        "ieee": "Forschungsstelle für Energienetze und Energiespeicher (FENES), OTH Regensburg, "
                "„Kosten – Informationsportal Regelbare Ortsnetztransformatoren (rONT),“ "
                "Regensburg, Deutschland. [Online]. Verfügbar: https://ront.info/tag/kosten/. "
                "[Zugriff: 4. Juli 2026].",
        "url": "https://ront.info/tag/kosten/",
        "archive_url": "https://web.archive.org/web/20260520184510/https://ront.info/tag/kosten/",
        "accessed": "2026-07-04",
    },
    "Kommunal_Fruehwarnsystem": {
        "ieee": "KOMMUNAL (Deutscher Gemeindeverlag), „Starkregen-Frühwarnsystem: Hier geht "
                "es schon bald an den Start,“ Berlin, Deutschland. [Online]. Verfügbar: "
                "https://www.kommunal.de/Starkregen-Fruehwarnsystem-NRW-Olpe. "
                "[Zugriff: 4. Juli 2026].",
        "url": "https://www.kommunal.de/Starkregen-Fruehwarnsystem-NRW-Olpe",
        "archive_url": "https://web.archive.org/web/20250211181808/"
                       "https://www.kommunal.de/Starkregen-Fruehwarnsystem-NRW-Olpe",
        "accessed": "2026-07-04",
    },
    "Semmler_Stadtgruen_2013": {
        "ieee": "R. Semmler, „Unterhaltungskosten und ihre Vorhersehbarkeit,“ Institut für "
                "Stadtgrün, Fachsymposium Stadtgrün, Julius Kühn-Institut, Quedlinburg, "
                "Deutschland, 2013. [Online]. Verfügbar: https://www.julius-kuehn.de/media/"
                "Institute/GF/_FS_Stadtgruen/1/"
                "FS-1-Stadtgruen_2.2_Semmler_Unterhaltungskosten_Vorhersehbarkeit.pdf. "
                "[Zugriff: 4. Juli 2026].",
        "url": "https://www.julius-kuehn.de/media/Institute/GF/_FS_Stadtgruen/1/"
               "FS-1-Stadtgruen_2.2_Semmler_Unterhaltungskosten_Vorhersehbarkeit.pdf",
        "archive_url": "https://web.archive.org/web/20190923200631/"
                       "https://www.julius-kuehn.de/media/Institute/GF/_FS_Stadtgruen/1/"
                       "FS-1-Stadtgruen_2.2_Semmler_Unterhaltungskosten_Vorhersehbarkeit.pdf",
        "accessed": "2026-07-04",
    },
    "Gartenbau_Hecke": {
        "ieee": "gartenbau.org, „Hecke pflanzen Kosten – Was kostet die Heckenpflanzung?,“ "
                "[Online]. Verfügbar: https://www.gartenbau.org/magazin/"
                "hecke-pflanzen-kosten-202222565. [Zugriff: 4. Juli 2026].",
        "url": "https://www.gartenbau.org/magazin/hecke-pflanzen-kosten-202222565",
        "archive_url": "https://web.archive.org/web/20221210033105/"
                       "https://www.gartenbau.org/magazin/hecke-pflanzen-kosten-202222565",
        "accessed": "2026-07-04",
    },
    # ══ Teil 2 — Nicht-Kosten-Parameter (Hazards, Risiken, Expositionen, Formeln) ══
    # ── Klimaprojektionen / Hazard-Kennwerte ────────────────────────────────
    "DWD_Klimareport": {
        "ieee": "Deutscher Wetterdienst (DWD), „Nationaler Klimareport – Klima: gestern, "
                "heute und in der Zukunft, 4. Auflage,“ Offenbach am Main, Deutschland. "
                "[Online]. Verfügbar: https://www.dwd.de/DE/leistungen/klimareports/"
                "download_report_auflage-4.pdf. [Zugriff: 4. Juli 2026].",
        "url": "https://www.dwd.de/DE/leistungen/klimareports/download_report_auflage-4.pdf",
        "archive_url": "https://web.archive.org/web/20231215011034/"
                       "https://www.dwd.de/DE/leistungen/klimareports/download_report_auflage-4.pdf",
        "accessed": "2026-07-04",
    },
    "IPCC_AR6_WG1": {
        "ieee": "Intergovernmental Panel on Climate Change (IPCC), „Climate Change 2021: The "
                "Physical Science Basis. Contribution of Working Group I to the Sixth Assessment "
                "Report,“ Cambridge University Press, Cambridge/New York, 2021. [Online]. "
                "Verfügbar: https://www.ipcc.ch/report/ar6/wg1/. [Zugriff: 4. Juli 2026].",
        "url": "https://www.ipcc.ch/report/ar6/wg1/",
        "archive_url": "https://web.archive.org/web/20210809075731/https://www.ipcc.ch/report/ar6/wg1/",
        "accessed": "2026-07-04",
    },
    "UBA_KWRA_2021": {
        "ieee": "Umweltbundesamt (UBA), „Klimawirkungs- und Risikoanalyse 2021 für "
                "Deutschland,“ Dessau-Roßlau, Deutschland, 2021. [Online]. Verfügbar: "
                "https://www.umweltbundesamt.de/klimawirkungs-risikoanalyse-2021-fuer-deutschland. "
                "[Zugriff: 4. Juli 2026].",
        "url": "https://www.umweltbundesamt.de/klimawirkungs-risikoanalyse-2021-fuer-deutschland",
        "archive_url": "https://web.archive.org/web/20210731125117/"
                       "https://www.umweltbundesamt.de/klimawirkungs-risikoanalyse-2021-fuer-deutschland",
        "accessed": "2026-07-04",
    },
    "UBA_KWRA_2021_TB1": {
        "ieee": "M. Kahlenborn u. a., „Klimawirkungs- und Risikoanalyse für Deutschland 2021 "
                "(Teilbericht 1): Grundlagen,“ Umweltbundesamt, Climate Change 20/2021, "
                "Dessau-Roßlau, Deutschland, 2021. [Online]. Verfügbar: "
                "https://www.umweltbundesamt.de/publikationen/KWRA-Teil-1-Grundlagen. "
                "[Zugriff: 5. Juli 2026].",
        "url": "https://www.umweltbundesamt.de/sites/default/files/medien/479/publikationen/"
               "kwra2021_teilbericht_1_grundlagen_bf_211027_0.pdf",
        "archive_url": "https://web.archive.org/web/20250829003720/"
                       "https://www.umweltbundesamt.de/sites/default/files/medien/479/publikationen/"
                       "kwra2021_teilbericht_1_grundlagen_bf_211027_0.pdf",
        "accessed": "2026-07-05",
    },
    "GIZ_Vulnerability_Sourcebook": {
        "ieee": "Deutsche Gesellschaft für Internationale Zusammenarbeit (GIZ) und EURAC, "
                "„The Vulnerability Sourcebook: Concept and guidelines for standardised "
                "vulnerability assessments,“ Bonn/Eschborn, Deutschland, 2. Aufl., 2017. "
                "[Online]. Verfügbar: https://www.adaptationcommunity.net/publications/"
                "vulnerability-sourcebook/. [Zugriff: 5. Juli 2026].",
        "url": "https://www.adaptationcommunity.net/download/va/vulnerability-guides-manuals-"
               "reports/vuln_source_2017_EN.pdf",
        "archive_url": "https://web.archive.org/web/20260601152904/"
                       "https://www.adaptationcommunity.net/download/va/vulnerability-guides-"
                       "manuals-reports/vuln_source_2017_EN.pdf",
        "accessed": "2026-07-05",
    },
    # ── Risiko-Kennwerte (Schäden / Gesundheit) ─────────────────────────────
    "Prognos_Klimaschaeden_2023": {
        "ieee": "Prognos AG, Gesellschaft für Wirtschaftliche Strukturforschung (GWS) und "
                "Institut für ökologische Wirtschaftsforschung (IÖW), „Kosten durch "
                "Klimawandelfolgen in Deutschland,“ im Auftrag des BMWK/BMUV, Osnabrück/Berlin, "
                "Deutschland, 2023. [Online]. Verfügbar: https://www.gws-os.com/de/energie-klima/"
                "projekte/detail/bmu-kliwafo. [Zugriff: 4. Juli 2026].",
        "url": "https://www.gws-os.com/de/energie-klima/projekte/detail/bmu-kliwafo",
        "archive_url": "https://web.archive.org/web/20220928001520/"
                       "https://www.gws-os.com/de/energie-klima/projekte/detail/bmu-kliwafo",
        "accessed": "2026-07-04",
    },
    "UBA_Methodenkonvention_MK3.1": {
        "ieee": "Umweltbundesamt (UBA), „Methodenkonvention 3.1 zur Ermittlung von "
                "Umweltkosten – Kostensätze,“ Dessau-Roßlau, Deutschland, 2020. [Online]. "
                "Verfügbar: https://www.umweltbundesamt.de/system/files/medien/1410/"
                "publikationen/2020-12-21_methodenkonvention_3_1_kostensaetze.pdf. "
                "[Zugriff: 4. Juli 2026].",
        "url": "https://www.umweltbundesamt.de/system/files/medien/1410/publikationen/"
               "2020-12-21_methodenkonvention_3_1_kostensaetze.pdf",
        "archive_url": "https://web.archive.org/web/20260312075140/"
                       "https://www.umweltbundesamt.de/system/files/medien/1410/publikationen/"
                       "2020-12-21_methodenkonvention_3_1_kostensaetze.pdf",
        "accessed": "2026-07-04",
    },
    "BBK_KRITIS": {
        "ieee": "Bundesamt für Bevölkerungsschutz und Katastrophenhilfe (BBK), „Kritische "
                "Infrastrukturen (KRITIS),“ Bonn, Deutschland. [Online]. Verfügbar: "
                "https://www.bbk.bund.de/DE/Themen/Kritische-Infrastrukturen/"
                "kritische-infrastrukturen_node.html. [Zugriff: 4. Juli 2026].",
        "url": "https://www.bbk.bund.de/DE/Themen/Kritische-Infrastrukturen/"
               "kritische-infrastrukturen_node.html",
        "archive_url": "https://web.archive.org/web/20210721012108/"
                       "https://www.bbk.bund.de/DE/Themen/Kritische-Infrastrukturen/"
                       "kritische-infrastrukturen_node.html",
        "accessed": "2026-07-04",
    },
    "RKI_Hitzemortalitaet": {
        "ieee": "M. an der Heiden, S. Muthers, H. Niemann u. a. / Robert Koch-Institut (RKI), "
                "„Hitzebedingte Mortalität – Sachstandsbericht Klimawandel und Gesundheit, "
                "Journal of Health Monitoring S4/2023,“ Berlin, Deutschland, 2023 (Methodik nach "
                "Winklmayr u. a., Dtsch. Arztebl. Int., 2022). [Online]. Verfügbar: "
                "https://edoc.rki.de/bitstream/handle/176904/11262/"
                "JHealthMonit_2023_S4_Hitze_Sachstandsbericht_Klimawandel_Gesundheit.pdf. "
                "[Zugriff: 4. Juli 2026].",
        "url": "https://edoc.rki.de/bitstream/handle/176904/11262/"
               "JHealthMonit_2023_S4_Hitze_Sachstandsbericht_Klimawandel_Gesundheit.pdf",
        "archive_url": "https://web.archive.org/web/20231024050849/"
                       "https://edoc.rki.de/bitstream/handle/176904/11262/"
                       "JHealthMonit_2023_S4_Hitze_Sachstandsbericht_Klimawandel_Gesundheit.pdf",
        "accessed": "2026-07-04",
    },
    "Winklmayr_2022": {
        "ieee": "C. Winklmayr, S. Muthers, H. Niemann, H.-G. Mücke und M. an der Heiden, "
                "„Heat-Related Mortality in Germany From 1992 to 2021,“ Dtsch. Arztebl. Int., "
                "Bd. 119, Nr. 26, S. 451–457, 2022, doi:10.3238/arztebl.m2022.0202. "
                "Generalisiertes additives Modell über Wochenmitteltemperatur und "
                "wöchentliche Gesamtsterblichkeit, geschichtet nach vier Altersgruppen "
                "(<65, 65–74, 75–84, ≥85) und drei Regionen (Nord/Mitte/Süd); liefert die "
                "Wirkschwellen 19,7/20,2/20,8 °C sowie die Jahresschätzungen 1992–2021. "
                "[Zugriff: 2. August 2026].",
        "url": "https://www.aerzteblatt.de/int/archive/article/225956",
        "archive_url": "https://web.archive.org/web/20240921163435/"
                       "https://www.aerzteblatt.de/int/archive/article/225956",
        "accessed": "2026-08-02",
    },
    "RKI_Wochenbericht_Hitzemortalitaet": {
        "ieee": "Robert Koch-Institut (RKI), „Wochenbericht zur hitzebedingten Mortalität,“ "
                "Berlin, Deutschland, fortlaufend (Sommermonate). Wöchentliche Schätzung der "
                "hitzebedingten Sterbefälle nach Altersgruppen; Datengrundlage Destatis-"
                "Sterbefallzahlen und DWD-Lufttemperatur. Ein Winter-/Kältependant wird "
                "nicht veröffentlicht. [Zugriff: 2. August 2026].",
        "url": "https://www.rki.de/DE/Themen/Gesundheit-und-Gesellschaft/"
               "Gesundheitliche-Einflussfaktoren-A-Z/H/Hitze/Bericht_Hitzemortalitaet.html",
        "archive_url": "https://web.archive.org/web/20260712131020/"
                       "https://www.rki.de/DE/Themen/Gesundheit-und-Gesellschaft/"
                       "Gesundheitliche-Einflussfaktoren-A-Z/H/Hitze/Bericht_Hitzemortalitaet.html",
        "accessed": "2026-08-02",
    },
    "Iungman_2023_UHI": {
        "ieee": "T. Iungman, M. Cirach, F. Marando u. a., „Cooling cities through urban green "
                "infrastructure: a health impact assessment of European cities,“ The Lancet, "
                "Bd. 401, Nr. 10376, S. 577–589, 2023, doi:10.1016/S0140-6736(22)02585-5. "
                "Schätzt 4,33 % [3,37; 5,27] der sommerlichen Sterbefälle in 93 europäischen "
                "Städten als der städtischen Wärmeinsel zurechenbar — hier als unabhängige "
                "Gegenprobe des ΔT-Modells genutzt. [Zugriff: 2. August 2026].",
        "url": "https://www.isglobal.org/en/-/"
               "4-of-summer-mortality-is-attributable-to-urban-heat-islands",
        "archive_url": "https://web.archive.org/web/20260801234533/"
                       "https://www.isglobal.org/en/-/"
                       "4-of-summer-mortality-is-attributable-to-urban-heat-islands",
        "accessed": "2026-08-02",
    },
    "DWD_CDC_Monatsraster_Temperatur": {
        "ieee": "Deutscher Wetterdienst (DWD), Climate Data Center (CDC), „Monatliche "
                "Rasterdaten der Lufttemperatur für Deutschland (1 km, air_temperature_mean / "
                "_min / _max),“ Offenbach, Deutschland. Gzip-komprimierte ESRI-ASCII-Raster "
                "in Gauß-Krüger Zone 3 (EPSG:31467); Werte in 1/10 °C. [Zugriff: 2. August 2026].",
        "url": "https://opendata.dwd.de/climate_environment/CDC/grids_germany/monthly/"
               "air_temperature_mean/",
        "archive_url": "https://web.archive.org/web/20260801234443/"
                       "https://opendata.dwd.de/climate_environment/CDC/grids_germany/monthly/"
                       "air_temperature_mean/",
        "accessed": "2026-08-02",
    },
    "Destatis_Sterbefaelle_Altersgruppen": {
        "ieee": "Statistisches Bundesamt (Destatis), „Todesursachenstatistik – Gestorbene nach "
                "Altersgruppen,“ Wiesbaden, Deutschland. Grundlage der altersspezifischen "
                "Basissterblichkeit je 100.000 Einwohner. [Zugriff: 2. August 2026].",
        "url": "https://www.destatis.de/DE/Themen/Gesellschaft-Umwelt/Gesundheit/"
               "Todesursachen/_inhalt.html",
        "archive_url": "https://web.archive.org/web/20260801234410/"
                       "https://www.destatis.de/DE/Themen/Gesellschaft-Umwelt/Gesundheit/"
                       "Todesursachen/_inhalt.html",
        "accessed": "2026-08-02",
    },
    "Destatis_Todesursachen_23211": {
        "ieee": "Statistisches Bundesamt (Destatis), „Todesursachenstatistik (GENESIS-Bereich "
                "23211), ICD-10-Positionen X30–X39 (Einwirkung von Naturgewalten),“ Wiesbaden, "
                "Deutschland. X37 (Sturm/Unwetter) und X38 (Überschwemmung) sind hier als "
                "Grundleiden kodiert und dienen als amtliche Gegenprobe zu den kuratierten "
                "Ereignislisten. [Zugriff: 2. August 2026].",
        "url": "https://www.destatis.de/DE/Themen/Gesellschaft-Umwelt/Gesundheit/"
               "Todesursachen/_inhalt.html",
        "archive_url": "https://web.archive.org/web/20260801234410/"
                       "https://www.destatis.de/DE/Themen/Gesellschaft-Umwelt/Gesundheit/"
                       "Todesursachen/_inhalt.html",
        "accessed": "2026-08-02",
    },
    "Destatis_Krankenhausdiagnosen_23131": {
        "ieee": "Statistisches Bundesamt (Destatis), „Krankenhausdiagnosestatistik "
                "(GENESIS-Bereich 23131) und fallpauschalenbezogene Krankenhausstatistik "
                "(DRG, 23141, Nebendiagnosen),“ Wiesbaden, Deutschland. Witterungsbedingte "
                "Verletzungen erscheinen als ICD-10-Außenursachen X30–X39; da diese in der "
                "deutschen Kodierpraxis **Neben**diagnosen sind, ist die DRG-Nebendiagnosen-"
                "Tabelle (23141BJ015, nach Altersgruppen) die belastbare Quelle, während die "
                "Hauptdiagnose-Tabelle deutlich untererfasst. [Zugriff: 2. August 2026].",
        "url": "https://www.destatis.de/DE/Themen/Gesellschaft-Umwelt/Gesundheit/"
               "Krankenhauser/_inhalt.html",
        "archive_url": "https://web.archive.org/web/20260801234830/"
                       "https://www.destatis.de/DE/Themen/Gesellschaft-Umwelt/Gesundheit/"
                       "Krankenhauser/_inhalt.html",
        "accessed": "2026-08-02",
    },
    "Jonkman_2008_LossOfLife": {
        "ieee": "S. N. Jonkman und E. Penning-Rowsell, „Loss of life due to floods,“ J. Flood "
                "Risk Manage., Bd. 1, Nr. 1, S. 43–56, 2008, doi:10.1111/j.1753-318X.2008.00006.x. "
                "Zoniert das Überflutungsgebiet nach Fließgeschwindigkeit, Anstiegsrate und "
                "Restzone; die Letalität je exponierter Person unterscheidet sich zwischen "
                "Sturzflut- und Langsam-Anstiegs-Regime um Größenordnungen. [Zugriff: 2. August 2026].",
        "url": "https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1753-318X.2008.00006.x",
        "archive_url": "https://web.archive.org/web/2026/"
                       "https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1753-318X.2008.00006.x",
        "accessed": "2026-08-02",
    },
    "CEDIM_Hochwasser_2021": {
        "ieee": "Center for Disaster Management and Risk Reduction Technology (CEDIM), "
                "Karlsruher Institut für Technologie, „Hochwasser Mitteleuropa, Juli 2021 – "
                "Bericht Nr. 1: Nordrhein-Westfalen und Rheinland-Pfalz,“ Karlsruhe, "
                "Deutschland, 2021. Ereignisdokumentation der Ahr-/Erft-Flut mit Todesopfern "
                "und Schadensbild. [Zugriff: 2. August 2026].",
        "url": "https://www.cedim.kit.edu/download/FDA_HochwasserJuli2021_Bericht1.pdf",
        "archive_url": "https://web.archive.org/web/2026/"
                       "https://www.cedim.kit.edu/download/FDA_HochwasserJuli2021_Bericht1.pdf",
        "accessed": "2026-08-02",
    },
    "DWD_Sturmereignisse": {
        "ieee": "Deutscher Wetterdienst (DWD), „Besondere Ereignisse – Stürme (u. a. Kyrill "
                "2007, Friederike 2018),“ Offenbach, Deutschland. Ereignisdokumentation mit "
                "Windfeld und Schadensbild; Grundlage der kuratierten Sturm-Ereignisliste. "
                "[Zugriff: 2. August 2026].",
        "url": "https://www.dwd.de/DE/leistungen/besondereereignisse/stuerme/"
               "20180123_friederike_europa.pdf",
        "archive_url": "https://web.archive.org/web/2026/"
                       "https://www.dwd.de/DE/leistungen/besondereereignisse/stuerme/"
                       "20180123_friederike_europa.pdf",
        "accessed": "2026-08-02",
    },
    "OECD_VSL_2012": {
        "ieee": "Organisation für wirtschaftliche Zusammenarbeit und Entwicklung (OECD), "
                "„Mortality Risk Valuation in Environment, Health and Transport Policies,“ "
                "OECD Publishing, Paris, 2012, doi:10.1787/9789264130807-en. Meta-Analyse "
                "internationaler Zahlungsbereitschafts-Studien zum Wert eines statistischen "
                "Lebens (VSL). [Online]. Verfügbar: https://www.oecd.org/en/publications/"
                "mortality-risk-valuation-in-environment-health-and-transport-policies_"
                "9789264130807-en.html. [Zugriff: 5. Juli 2026].",
        "url": "https://www.oecd.org/en/publications/"
               "mortality-risk-valuation-in-environment-health-and-transport-policies_"
               "9789264130807-en.html",
        "archive_url": "https://web.archive.org/web/20260223012309/"
                       "https://www.oecd.org/en/publications/"
                       "mortality-risk-valuation-in-environment-health-and-transport-policies_"
                       "9789264130807-en.html",
        "accessed": "2026-07-05",
    },
    "EWI_VoLL_2015": {
        "ieee": "C. Growitsch, R. Malischek, S. Nick und H. Wetzel, „The Costs of Power "
                "Interruptions in Germany – an Assessment in the Light of the Energiewende,“ "
                "EWI Working Paper Nr. 13/07, Energiewirtschaftliches Institut an der "
                "Universität zu Köln (EWI), Köln, Deutschland, 2013 (publ. German Economic "
                "Review, Bd. 16(3), S. 307–323, 2015). Value of Lost Load Haushalte "
                "~11,92 €/kWh; nationale Ausfallkosten ~430 Mio €/h. [Online]. Verfügbar: "
                "https://www.ewi.uni-koeln.de/cms/wp-content/uploads/2015/12/"
                "EWI_WP_13-07-Costs-of-Power-Interruptions-in-Germany.pdf. "
                "[Zugriff: 5. Juli 2026].",
        "url": "https://www.ewi.uni-koeln.de/cms/wp-content/uploads/2015/12/"
               "EWI_WP_13-07-Costs-of-Power-Interruptions-in-Germany.pdf",
        "archive_url": "https://web.archive.org/web/20250624093413/"
                       "https://www.ewi.uni-koeln.de/cms/wp-content/uploads/2015/12/"
                       "EWI_WP_13-07-Costs-of-Power-Interruptions-in-Germany.pdf",
        "accessed": "2026-07-05",
    },
    "TEEB_DE_Naturkapital": {
        "ieee": "Naturkapital Deutschland – TEEB DE (Hrsg. B. Hansjürgens u. a.), "
                "„Der Wert der Natur für Wirtschaft und Gesellschaft – Eine Einführung,“ "
                "Helmholtz-Zentrum für Umweltforschung (UFZ) im Auftrag von BMU/BfN, "
                "Leipzig/Berlin, Deutschland, 2012–2018. Ökonomische Bewertung von "
                "Ökosystemleistungen und Naturkapital in Deutschland. [Online]. Verfügbar: "
                "https://www.ufz.de/teebde/index.php?de=43777. [Zugriff: 5. Juli 2026].",
        "url": "https://www.ufz.de/teebde/index.php?de=43777",
        "archive_url": "https://web.archive.org/web/20260510142628/"
                       "https://www.ufz.de/teebde/index.php?de=43777",
        "accessed": "2026-07-05",
    },
    # ── Expositionen / Sensitivitäten (Normierungsskalen) ───────────────────
    "Zensus_2022": {
        "ieee": "Statistisches Bundesamt (Destatis), „Zensus 2022 – Bevölkerung im "
                "100-Meter-Gitter,“ Wiesbaden, Deutschland, 2022. [Online]. Verfügbar: "
                "https://www.destatis.de/DE/Themen/Gesellschaft-Umwelt/Bevoelkerung/Zensus2022/"
                "_inhalt.html. [Zugriff: 4. Juli 2026].",
        "url": "https://www.destatis.de/DE/Themen/Gesellschaft-Umwelt/Bevoelkerung/Zensus2022/"
               "_inhalt.html",
        "archive_url": "https://web.archive.org/web/20250709030127/"
                       "https://www.destatis.de/DE/Themen/Gesellschaft-Umwelt/Bevoelkerung/"
                       "Zensus2022/_inhalt.html",
        "accessed": "2026-07-04",
    },
    # ── Formel-Parameter (UHI-Koeffizienten) ────────────────────────────────
    "VDI3787_Stadtklima": {
        "ieee": "Verein Deutscher Ingenieure (VDI), „VDI 3787 Blatt 1: Umweltmeteorologie – "
                "Klima- und Lufthygienekarten für Städte und Regionen,“ Düsseldorf, Deutschland. "
                "[Online]. Verfügbar: https://www.vdi.de/richtlinien/details/"
                "vdi-3787-blatt-1-umweltmeteorologie-klima-und-planung. [Zugriff: 4. Juli 2026].",
        "url": "https://www.vdi.de/richtlinien/details/"
               "vdi-3787-blatt-1-umweltmeteorologie-klima-und-planung",
        "archive_url": "https://web.archive.org/web/20211027064307/"
                       "https://www.vdi.de/richtlinien/details/"
                       "vdi-3787-blatt-1-umweltmeteorologie-klima-und-planung",
        "accessed": "2026-07-04",
    },
    "StewartOke_LCZ_2012": {
        "ieee": "I. D. Stewart und T. R. Oke, „Local Climate Zones for Urban Temperature "
                "Studies,“ Bulletin of the American Meteorological Society, Bd. 93, Nr. 12, "
                "S. 1879–1900, 2012. [Online]. Verfügbar: https://journals.ametsoc.org/view/"
                "journals/bams/93/12/bams-d-11-00019.1.xml. [Zugriff: 4. Juli 2026].",
        "url": "https://journals.ametsoc.org/view/journals/bams/93/12/bams-d-11-00019.1.xml",
        "archive_url": "https://web.archive.org/web/20210411032356/"
                       "https://journals.ametsoc.org/view/journals/bams/93/12/bams-d-11-00019.1.xml",
        "accessed": "2026-07-04",
    },
    # ── Räumliche Datengrundlagen (Proxys für Hazards/Expositionen/Sensitivitäten) ──
    "OSM_Data": {
        "ieee": "OpenStreetMap-Mitwirkende, „OpenStreetMap – freie Geodaten (Gebäude, "
                "Landnutzung, Infrastruktur),“ OpenStreetMap Foundation. Daten lizenziert "
                "unter ODbL. [Online]. Verfügbar: https://www.openstreetmap.org/copyright. "
                "[Zugriff: 4. Juli 2026].",
        "url": "https://www.openstreetmap.org/copyright",
        "archive_url": "https://web.archive.org/web/20100610133123/"
                       "http://www.openstreetmap.org/copyright",
        "accessed": "2026-07-04",
    },
    "DWD_CDC": {
        "ieee": "Deutscher Wetterdienst (DWD), „Climate Data Center (CDC) – Raster- und "
                "Stationsdaten zu Klimakennwerten,“ Offenbach am Main, Deutschland. [Online]. "
                "Verfügbar: https://www.dwd.de/DE/leistungen/cdc/climate-data-center.html. "
                "[Zugriff: 4. Juli 2026].",
        "url": "https://www.dwd.de/DE/leistungen/cdc/climate-data-center.html",
        "archive_url": "https://web.archive.org/web/20210716013105/"
                       "https://www.dwd.de/DE/leistungen/cdc/climate-data-center.html",
        "accessed": "2026-07-04",
    },
    "DWD_CDC_Starkregen": {
        "ieee": "Deutscher Wetterdienst (DWD), „Climate Data Center (CDC) – Jährliche "
                "Rasterkarten der Anzahl Tage mit Niederschlag ≥ 20 mm bzw. ≥ 30 mm "
                "(grids_germany/annual, 1 km, EPSG:31467),“ Offenbach am Main, Deutschland. "
                "[Online]. Verfügbar: https://opendata.dwd.de/climate_environment/CDC/"
                "grids_germany/annual/precipGE20mm_days/. [Zugriff: 5. Juli 2026].",
        "url": "https://opendata.dwd.de/climate_environment/CDC/grids_germany/annual/"
               "precipGE20mm_days/",
        "archive_url": "https://web.archive.org/web/20260317084148/"
                       "https://opendata.dwd.de/climate_environment/CDC/grids_germany/annual/"
                       "precipGE20mm_days/",
        "accessed": "2026-07-05",
    },
    "Copernicus_C3S": {
        "ieee": "Copernicus Climate Change Service (C3S), ECMWF, „Copernicus Climate Change "
                "Service – Klimadaten und -indikatoren,“ Reading, Vereinigtes Königreich. "
                "[Online]. Verfügbar: https://climate.copernicus.eu/. [Zugriff: 4. Juli 2026].",
        "url": "https://climate.copernicus.eu/",
        "archive_url": "https://web.archive.org/web/20260701001320/https://climate.copernicus.eu/",
        "accessed": "2026-07-04",
    },
    "ERA5_C3S": {
        "ieee": "H. Hersbach u. a. / Copernicus Climate Change Service (C3S), „ERA5 hourly data "
                "on single levels from 1940 to present (ECMWF-Reanalyse v5),“ Copernicus Climate "
                "Data Store (CDS), 2023. Lizenz: CC-BY 4.0 (seit 02.07.2025). [Online]. Verfügbar: "
                "https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels. "
                "[Zugriff: 5. Juli 2026].",
        "url": "https://www.ecmwf.int/en/forecasts/dataset/ecmwf-reanalysis-v5",
        "archive_url": "https://web.archive.org/web/20260415053055/"
                       "https://www.ecmwf.int/en/forecasts/dataset/ecmwf-reanalysis-v5",
        "accessed": "2026-07-05",
    },
    "BBSR_INKAR": {
        "ieee": "Bundesinstitut für Bau-, Stadt- und Raumforschung (BBSR), „INKAR – Indikatoren "
                "und Karten zur Raum- und Stadtentwicklung,“ Bonn, Deutschland. [Online]. "
                "Verfügbar: https://www.inkar.de/. [Zugriff: 4. Juli 2026].",
        "url": "https://www.inkar.de/",
        "archive_url": "https://web.archive.org/web/20260628060549/https://www.inkar.de/",
        "accessed": "2026-07-04",
    },
    "DWD_VieljaehrigeMittel_1991_2020": {
        "ieee": "Deutscher Wetterdienst (DWD), „Vieljährige Mittelwerte 1991–2020 für "
                "Deutschland (Temperatur, Niederschlag, klimatologische Kenntage),“ "
                "Offenbach, Deutschland. [Online]. Verfügbar: https://www.dwd.de/DE/"
                "leistungen/klimadatendeutschland/vielj_mittelwerte.html. "
                "[Zugriff: 5. Juli 2026].",
        "url": "https://www.dwd.de/DE/leistungen/klimadatendeutschland/"
               "vielj_mittelwerte.html",
        "archive_url": "https://web.archive.org/web/2026/https://www.dwd.de/DE/"
                       "leistungen/klimadatendeutschland/vielj_mittelwerte.html",
        "accessed": "2026-07-05",
    },
    "DWD_Klimastatusbericht": {
        "ieee": "Deutscher Wetterdienst (DWD), „Klimastatusbericht Deutschland,“ "
                "Offenbach, Deutschland (jährliche Reihe). [Online]. Verfügbar: "
                "https://www.dwd.de/DE/leistungen/klimastatusbericht/"
                "klimastatusbericht.html. [Zugriff: 5. Juli 2026].",
        "url": "https://www.dwd.de/DE/leistungen/klimastatusbericht/"
               "klimastatusbericht.html",
        "archive_url": "https://web.archive.org/web/2026/https://www.dwd.de/DE/"
                       "leistungen/klimastatusbericht/klimastatusbericht.html",
        "accessed": "2026-07-05",
    },
    "DWD_CDC_Rasterklimatologie": {
        "ieee": "Deutscher Wetterdienst (DWD), Climate Data Center (CDC), „Raster der "
                "jährlichen klimatologischen Kenntage für Deutschland (grids_germany/"
                "annual: Schneedeckentage, heiße Tage, Frosttage, Starkregentage),“ "
                "Offenbach, Deutschland. [Online]. Verfügbar: https://opendata.dwd.de/"
                "climate_environment/CDC/grids_germany/annual/. [Zugriff: 5. Juli 2026].",
        "url": "https://opendata.dwd.de/climate_environment/CDC/grids_germany/annual/",
        "archive_url": "https://web.archive.org/web/2026/https://opendata.dwd.de/"
                       "climate_environment/CDC/grids_germany/annual/",
        "accessed": "2026-07-05",
    },
    # ── Maßnahmenwirkung & Betriebskosten (Parameter-Vollerklärung, Juli 2026) ──
    "VDI_2067_Blatt1": {
        "ieee": "Verein Deutscher Ingenieure (VDI), „VDI 2067 Blatt 1: Wirtschaftlichkeit "
                "gebäudetechnischer Anlagen – Grundlagen und Kostenberechnung,“ Düsseldorf, "
                "Deutschland, 2012. [Online]. Verfügbar: https://www.vdi.de/mitgliedschaft/"
                "vdi-richtlinien/details/vdi-2067-blatt-1-wirtschaftlichkeit-"
                "gebaeudetechnischer-anlagen-grundlagen-und-kostenberechnung-1. "
                "[Zugriff: 6. Juli 2026].",
        "url": "https://www.vdi.de/mitgliedschaft/vdi-richtlinien/details/vdi-2067-blatt-1-"
               "wirtschaftlichkeit-gebaeudetechnischer-anlagen-grundlagen-und-"
               "kostenberechnung-1",
        "archive_url": "https://web.archive.org/web/20260706052623/https://www.vdi.de/"
                       "mitgliedschaft/vdi-richtlinien/details/vdi-2067-blatt-1-"
                       "wirtschaftlichkeit-gebaeudetechnischer-anlagen-grundlagen-und-"
                       "kostenberechnung-1",
        "accessed": "2026-07-06",
    },
    "Urban_HHAP_Wirksamkeit_2025": {
        "ieee": "A. Urban, V. Huber, S. Henry u. a., „The effectiveness of heat prevention "
                "plans in reducing heat-related mortality across Europe,“ Environmental "
                "Research Letters, Bd. 20, Nr. 12, 124071, 2025, doi: 10.1088/1748-9326/"
                "ae2775. [Online]. Verfügbar: https://pmc.ncbi.nlm.nih.gov/articles/"
                "PMC12724396/. [Zugriff: 6. Juli 2026].",
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC12724396/",
        "archive_url": "https://web.archive.org/web/20260706052754/"
                       "https://pmc.ncbi.nlm.nih.gov/articles/PMC12724396/",
        "accessed": "2026-07-06",
    },
    "WMO_EarlyWarnings": {
        "ieee": "World Meteorological Organization (WMO), „Early warning system / Early "
                "Warnings for All,“ Genf, Schweiz. [Online]. Verfügbar: "
                "https://wmo.int/topics/early-warning-system. [Zugriff: 6. Juli 2026].",
        "url": "https://wmo.int/topics/early-warning-system",
        "archive_url": "https://web.archive.org/web/20260505235936/"
                       "https://wmo.int/topics/early-warning-system",
        "accessed": "2026-07-06",
    },
    "BNetzA_SAIDI_2023": {
        "ieee": "Bundesnetzagentur, „Versorgungsunterbrechungen Strom 2023 (SAIDI: 12,8 "
                "Minuten),“ Pressemitteilung, Bonn, Deutschland, 2024. [Online]. Verfügbar: "
                "https://www.bundesnetzagentur.de/SharedDocs/Pressemitteilungen/DE/2024/"
                "20241111_SAIDI_Strom.html. [Zugriff: 6. Juli 2026].",
        "url": "https://www.bundesnetzagentur.de/SharedDocs/Pressemitteilungen/DE/2024/"
               "20241111_SAIDI_Strom.html",
        "archive_url": "https://web.archive.org/web/20260626202318/"
                       "https://www.bundesnetzagentur.de/SharedDocs/Pressemitteilungen/"
                       "DE/2024/20241111_SAIDI_Strom.html",
        "accessed": "2026-07-06",
    },
    "BWB_Niederschlagswasserentgelt": {
        "ieee": "Berliner Wasserbetriebe, „Bestandsaufnahme von versiegelten Flächen auf "
                "Privatgrundstücken (Niederschlagswasserentgelt 1,84 €/m² versiegelte "
                "Fläche und Jahr),“ Berlin, Deutschland. [Online]. Verfügbar: "
                "https://www.bwb.de/de/bestandsaufnahme-von-versiegelten-flaechen-auf-"
                "privatgrundstuecken.php. [Zugriff: 6. Juli 2026].",
        "url": "https://www.bwb.de/de/bestandsaufnahme-von-versiegelten-flaechen-auf-"
               "privatgrundstuecken.php",
        "archive_url": "https://web.archive.org/web/20260706052927/https://www.bwb.de/de/"
                       "bestandsaufnahme-von-versiegelten-flaechen-auf-privatgrundstuecken.php",
        "accessed": "2026-07-06",
    },
    # ── LoD2: amtliche 3D-Gebäudemodelle der Länder (Gebäudehöhen + SVF) ──────
    "LoD2_NW": {
        "ieee": "Geobasis NRW, Bezirksregierung Köln, „3D-Gebäudemodelle LoD2 "
                "(CityGML), OpenGeodata.NRW,“ Köln, Deutschland, dl-de/zero-2-0. "
                "[Online]. Verfügbar: https://www.opengeodata.nrw.de/produkte/"
                "geobasis/3dg/lod2_gml/. [Zugriff: 14. Juli 2026].",
        "url": "https://www.opengeodata.nrw.de/produkte/geobasis/3dg/lod2_gml/",
        "archive_url": "https://web.archive.org/web/2026/https://www.opengeodata"
                       ".nrw.de/produkte/geobasis/3dg/lod2_gml/",
        "accessed": "2026-07-14",
    },
    "LoD2_BY": {
        "ieee": "Landesamt für Digitalisierung, Breitband und Vermessung Bayern, "
                "„3D-Gebäudemodelle LoD2 (CityGML), OpenData Bayern,“ München, "
                "Deutschland, CC BY 4.0. [Online]. Verfügbar: https://geodaten."
                "bayern.de/opengeodata/OpenDataDetail.html?pn=lod2. "
                "[Zugriff: 14. Juli 2026].",
        "url": "https://geodaten.bayern.de/opengeodata/OpenDataDetail.html?pn=lod2",
        "archive_url": "https://web.archive.org/web/2026/https://geodaten.bayern"
                       ".de/opengeodata/OpenDataDetail.html?pn=lod2",
        "accessed": "2026-07-14",
    },
    "LoD2_BB": {
        "ieee": "Landesvermessung und Geobasisinformation Brandenburg (LGB), "
                "„3D-Gebäudemodelle LoD2 (CityGML), Geobasis-BB,“ Potsdam, "
                "Deutschland, dl-de/by-2-0. [Online]. Verfügbar: https://data."
                "geobasis-bb.de/geobasis/daten/3d_gebaeude/. [Zugriff: 14. Juli 2026].",
        "url": "https://data.geobasis-bb.de/geobasis/daten/3d_gebaeude/",
        "archive_url": "https://web.archive.org/web/2026/https://data.geobasis-bb"
                       ".de/geobasis/daten/3d_gebaeude/",
        "accessed": "2026-07-14",
    },
    "LoD2_HH": {
        "ieee": "Landesbetrieb Geoinformation und Vermessung Hamburg, "
                "„3D-Gebäudemodell LoD2-DE Hamburg (CityGML), Transparenzportal,“ "
                "Hamburg, Deutschland, dl-de/by-2-0. [Online]. Verfügbar: "
                "https://suche.transparenz.hamburg.de/dataset/"
                "3d-gebaeudemodell-lod2-de-hamburg. [Zugriff: 14. Juli 2026].",
        "url": "https://suche.transparenz.hamburg.de/dataset/"
               "3d-gebaeudemodell-lod2-de-hamburg",
        "archive_url": "https://web.archive.org/web/2026/https://suche.transparenz"
                       ".hamburg.de/dataset/3d-gebaeudemodell-lod2-de-hamburg",
        "accessed": "2026-07-14",
    },
    "LoD2_Laender_Sammel": {
        "ieee": "Arbeitsgemeinschaft der Vermessungsverwaltungen der Länder (AdV), "
                "„3D-Gebäudemodelle LoD2 der Länder (CityGML) — Open-Data-Portale "
                "der Landesvermessungen (BW, NI, SH, BE, MV, SN, ST, TH, HE, RP, "
                "SL, HB),“ Deutschland, DL-DE/BY-2.0 bzw. CC BY 4.0. [Online]. "
                "Verfügbar: https://www.adv-online.de/AdV-Produkte/Standards-und-"
                "Produktblaetter/. [Zugriff: 14. Juli 2026].",
        "url": "https://www.adv-online.de/AdV-Produkte/Standards-und-Produktblaetter/",
        "archive_url": "https://web.archive.org/web/2026/https://www.adv-online.de/"
                       "AdV-Produkte/Standards-und-Produktblaetter/",
        "accessed": "2026-07-14",
    },
    "Zaksek_2011_SVF": {
        "ieee": "K. Zakšek, K. Oštir und Ž. Kokalj, „Sky-View Factor as a Relief "
                "Visualization Technique,“ Remote Sensing, Bd. 3, Nr. 2, "
                "S. 398–415, 2011. doi: 10.3390/rs3020398.",
        "url": "https://www.mdpi.com/2072-4292/3/2/398",
        "archive_url": "https://web.archive.org/web/2026/https://www.mdpi.com/"
                       "2072-4292/3/2/398",
        "accessed": "2026-07-14",
    },
    "Oke_1981_Canyon": {
        "ieee": "T. R. Oke, „Canyon geometry and the nocturnal urban heat island: "
                "Comparison of scale model and field observations,“ Journal of "
                "Climatology, Bd. 1, Nr. 3, S. 237–254, 1981. "
                "doi: 10.1002/joc.3370010304.",
        "url": "https://onlinelibrary.wiley.com/doi/10.1002/joc.3370010304",
        "archive_url": "https://web.archive.org/web/2026/https://onlinelibrary"
                       ".wiley.com/doi/10.1002/joc.3370010304",
        "accessed": "2026-07-14",
    },

    # ── Methodik #95 Rev. 7 (Integration; Bericht docs/methodik/95_hitzebelastung.md) ──
    "RKI_EpidBull_19_2025": {
        "ieee": "C. Winklmayr und M. an der Heiden, „Hitzebedingte Mortalität in "
                "Deutschland 2023 und 2024,“ Epidemiologisches Bulletin, Nr. 19/2025, "
                "S. 3–9, 2025. doi: 10.25646/13135. Revidierte Jahresreihe 1992–2024 "
                "inkl. Bundesländer-Anhang — Kalibrieranker des #95-Modells.",
        "url": "https://edoc.rki.de/handle/176904/12682",
        "archive_url": "https://web.archive.org/web/20250816015512/"
                       "https://edoc.rki.de/handle/176904/12682",
        "accessed": "2026-08-30",
    },
    "Karlsson_Ziebarth_2018": {
        "ieee": "M. Karlsson und N. R. Ziebarth, „Population health effects and health-"
                "related costs of extreme temperatures: Comprehensive evidence from "
                "Germany,“ J. Environ. Econ. Manage., Bd. 91, S. 93–117, 2018. "
                "doi: 10.1016/j.jeem.2018.06.004. Quasi-experimentelles Panel "
                "(170 Mio. Krankenhausfälle, 1999–2008): +2,4 % Einweisungen je "
                "zusätzlichem Hitzetag (konditional), Ø 7,2 Hitzetage/Jahr.",
        "url": "https://doi.org/10.1016/j.jeem.2018.06.004",
        "archive_url": "https://web.archive.org/web/20260514012723/"
                       "https://doi.org/10.1016/j.jeem.2018.06.004",
        "accessed": "2026-08-30",
    },
    "Karlsson_Ziebarth_IZA_DP7875": {
        "ieee": "M. Karlsson und N. R. Ziebarth, „Population Health Effects and Health-"
                "Related Costs of Climate Extremes,“ IZA Discussion Paper Nr. 7875, "
                "2014, Tab. 1/3, Fig. 9, App. A (Detailtabellen zur JEEM-Publikation: "
                "Kreislauf-Anteil 11,9 % des Einweisungs-Exzesses).",
        "url": "https://docs.iza.org/dp7875.pdf",
        "archive_url": "https://web.archive.org/web/20251224183503/"
                       "https://docs.iza.org/dp7875.pdf",
        "accessed": "2026-08-30",
    },
    "Semenza_1996_Chicago": {
        "ieee": "J. C. Semenza u. a., „Heat-Related Deaths during the July 1995 Heat "
                "Wave in Chicago,“ N. Engl. J. Med., Bd. 335, S. 84–90, 1996. "
                "doi: 10.1056/NEJM199607113350203. Fall-Kontroll-Studie: OR ≈ 2,3 "
                "„allein lebend“ (Todesfälle, Ältere).",
        "url": "https://www.nejm.org/doi/10.1056/NEJM199607113350203",
        "archive_url": "https://web.archive.org/web/20240120022812/"
                       "https://www.nejm.org/doi/10.1056/NEJM199607113350203",
        "accessed": "2026-08-30",
    },
    "Fouillet_2006_Frankreich": {
        "ieee": "A. Fouillet u. a., „Excess mortality related to the August 2003 heat "
                "wave in France,“ Int. Arch. Occup. Environ. Health, Bd. 80, S. 16–24, "
                "2006. doi: 10.1007/s00420-006-0089-4. Tab. 2: O/E nach Sterbeort "
                "(Heime 1,9 [1,7–2,1] vs. Wohnung ≥ 75: 1,9).",
        "url": "https://link.springer.com/article/10.1007/s00420-006-0089-4",
        "archive_url": "https://web.archive.org/web/20260123185210/"
                       "https://link.springer.com/article/10.1007/s00420-006-0089-4",
        "accessed": "2026-08-30",
    },
    "Bouchama_2007_Meta": {
        "ieee": "A. Bouchama u. a., „Prognostic Factors in Heat Wave–Related Deaths: "
                "A Meta-analysis,“ Arch. Intern. Med., Bd. 167, Nr. 20, S. 2170–2176, "
                "2007. doi: 10.1001/archinte.167.20.ira70009 (Stütze der "
                "β_pfl-Niveaukette, OR „nicht selbstversorgungsfähig“ 2,97).",
        "url": "https://doi.org/10.1001/archinte.167.20.ira70009",
        "archive_url": "https://web.archive.org/web/20260820142737/"
                       "https://doi.org/10.1001/archinte.167.20.ira70009",
        "accessed": "2026-08-30",
    },
    "Klenk_2010_Heime": {
        "ieee": "J. Klenk, C. Becker und K. Rapp, „Heat-related mortality in residents "
                "of nursing homes,“ Age Ageing, Bd. 39, Nr. 2, S. 245–251, 2010. "
                "doi: 10.1093/ageing/afp248 (ERF-Gültigkeit im Heim-Setting: +26 %/+62 % "
                "bei 32–33,9/≥ 34 °C).",
        "url": "https://doi.org/10.1093/ageing/afp248",
        "archive_url": "https://web.archive.org/web/20250629101359/"
                       "https://doi.org/10.1093/ageing/afp248",
        "accessed": "2026-08-30",
    },
    "Destatis_Sterbetafeln_2022_2024": {
        "ieee": "Statistisches Bundesamt (Destatis), Statistischer Bericht „Sterbetafeln "
                "2022/2024“ (Juli 2025), Blätter 12613-b01/-b02 (Restlebenserwartung "
                "e(x) nach Geschlecht), Wiesbaden. Bevölkerungsgewichte: Fortschreibung "
                "31.12.2023 (regionalstatistik.de, Tab. 12411-09-01-4-B, Basis "
                "Zensus 2022).",
        "url": "https://www.destatis.de/DE/Themen/Gesellschaft-Umwelt/Bevoelkerung/"
               "Sterbefaelle-Lebenserwartung/_inhalt.html",
        "archive_url": "https://web.archive.org/web/20260804142846/"
                       "https://www.destatis.de/DE/Themen/Gesellschaft-Umwelt/"
                       "Bevoelkerung/Sterbefaelle-Lebenserwartung/_inhalt.html",
        "accessed": "2026-08-30",
    },
    "Destatis_Kostennachweis_2023": {
        "ieee": "Statistisches Bundesamt (Destatis), „Kostennachweis der Krankenhäuser "
                "2023,“ Statistischer Bericht 12-6-4 (bereinigte Kosten je "
                "Behandlungsfall ≈ 6.996 €₂₀₂₃), Wiesbaden.",
        "url": "https://www.destatis.de/DE/Themen/Gesellschaft-Umwelt/Gesundheit/"
               "Krankenhaeuser/_inhalt.html",
        "archive_url": "https://web.archive.org/web/20250812204141/"
                       "https://www.destatis.de/DE/Themen/Gesellschaft-Umwelt/"
                       "Gesundheit/Krankenhaeuser/_inhalt.html",
        "accessed": "2026-08-30",
    },
    "Destatis_T67_Hitzeeinweisungen": {
        "ieee": "Statistisches Bundesamt (Destatis), Pressemitteilung N035 vom "
                "15.07.2024: „Hitzebedingte Krankenhausbehandlungen (ICD T67)“ "
                "(Ø ≈ 1.400–1.500 Fälle/Jahr; 2003: 2.600), Wiesbaden.",
        "url": "https://www.destatis.de/DE/Presse/Pressemitteilungen/2024/07/"
               "PD24_N035_231.html",
        "archive_url": "https://web.archive.org/web/20250128201850/"
                       "https://www.destatis.de/DE/Presse/Pressemitteilungen/2024/07/"
                       "PD24_N035_231.html",
        "accessed": "2026-08-30",
    },
    "Destatis_Pflegestatistik_2023": {
        "ieee": "Statistisches Bundesamt (Destatis), Pflegestatistik 2023 (GENESIS-"
                "Online Tab. 22421-0001; PM 478/2024: 0,80 Mio. vollstationär; 85+: "
                "424.300), Wiesbaden. Ergänzend WIdO-Pflegereport (Sterberate "
                "Heimbewohner ≈ 0,6–0,7 %/Woche).",
        "url": "https://www.destatis.de/DE/Presse/Pressemitteilungen/2024/12/"
               "PD24_478_224.html",
        "archive_url": "https://web.archive.org/web/20260601145452/"
                       "https://www.destatis.de/DE/Presse/Pressemitteilungen/2024/12/"
                       "PD24_478_224.html",
        "accessed": "2026-08-30",
    },
    "Destatis_Mikrozensus_2023_Einpersonenhaushalte": {
        "ieee": "Statistisches Bundesamt (Destatis)/BMFSFJ-Open-Data, „Anteil von "
                "Frauen und Männern ab 65 Jahren in Einpersonenhaushalten,“ "
                "Mikrozensus 2023 (Erstergebnisse): 34,6 % (Indikator 132088).",
        "url": "https://www.destatis.de/DE/Themen/Gesellschaft-Umwelt/Bevoelkerung/"
               "Haushalte-Familien/_inhalt.html",
        "archive_url": "https://web.archive.org/web/20260826040405/"
                       "https://www.destatis.de/DE/Themen/Gesellschaft-Umwelt/"
                       "Bevoelkerung/Haushalte-Familien/_inhalt.html",
        "accessed": "2026-08-30",
    },
    "UBA_MK40_Amann_2020_VOLY": {
        "ieee": "Umweltbundesamt, „Methodenkonvention 4.0 zur Ermittlung von "
                "Umweltkosten,“ Abschn. 3.4; M. Amann u. a. (IIASA), 2020a, Tab. 3.15: "
                "VOLY 79.500 €₂₀₀₅ — Kette auf €₂₀₂₄: × VPI 1,4638 × Raumtransfer "
                "1,1792 × Einkommensentwicklung 1,1719 = 160.800 € (Bericht #95 §3.5).",
        "url": "https://www.umweltbundesamt.de/publikationen/methodenkonvention-"
               "umweltkosten",
        "archive_url": "https://web.archive.org/web/20260415021252/"
                       "https://www.umweltbundesamt.de/publikationen/"
                       "methodenkonvention-umweltkosten",
        "accessed": "2026-08-30",
    },
    # ── Methodik #96 Rev. 1 (Aeroallergene; docs/methodik/96_aeroallergene.md) ──
    "Langen_2013_DEGS1": {
        "ieee": "U. Langen, R. Schmitz und H. Steppuhn, „Häufigkeit allergischer "
                "Erkrankungen in Deutschland: Ergebnisse der Studie zur Gesundheit "
                "Erwachsener in Deutschland (DEGS1),“ Bundesgesundheitsbl., Bd. 56, "
                "Nr. 5–6, S. 698–706, 2013. doi: 10.1007/s00103-012-1652-7. Tab. 3: "
                "12-Monats-Prävalenz Heuschnupfen nach Altersdekaden (14,6/17,2/14,3/"
                "10,1/8,2/5,0 %) — Basis der Band-Prävalenzen p_AR (#96 §3.2).",
        "url": "https://doi.org/10.1007/s00103-012-1652-7",
        "archive_url": "https://web.archive.org/web/20251225055737/"
                       "https://doi.org/10.1007/s00103-012-1652-7",
        "accessed": "2026-08-30",
    },
    "Thamm_2018_KiGGS_W2": {
        "ieee": "R. Thamm u. a., „Allergische Erkrankungen bei Kindern und Jugendlichen "
                "in Deutschland — Querschnittergebnisse aus KiGGS Welle 2,“ J. Health "
                "Monit., Bd. 3, Nr. 3, S. 3–18, 2018. doi: 10.17886/RKI-GBE-2018-075 "
                "(12-Monats-Prävalenz Heuschnupfen 0–17 Jahre: 8,8 % — Band u20).",
        "url": "https://doi.org/10.17886/RKI-GBE-2018-075",
        "archive_url": "https://web.archive.org/web/20251223141607/"
                       "https://doi.org/10.17886/RKI-GBE-2018-075",
        "accessed": "2026-08-30",
    },
    "Haftenberger_2013_Sensibilisierung": {
        "ieee": "M. Haftenberger u. a., „Prävalenz von Sensibilisierungen gegen "
                "Inhalations- und Nahrungsmittelallergene (DEGS1),“ Bundesgesundheitsbl., "
                "Bd. 56, Nr. 5–6, S. 687–697, 2013. doi: 10.1007/s00103-012-1658-1. "
                "Tab. 2/Abb. 1: Sensibilisierung Gräserpollen 19,4 %, Birke 17,4 % — "
                "Stütze der Anteile p_B/p_G (#96 §3.4).",
        "url": "https://doi.org/10.1007/s00103-012-1658-1",
        "archive_url": "https://web.archive.org/web/20260831051759/"
                       "https://doi.org/10.1007/s00103-012-1658-1",
        "accessed": "2026-08-31",
    },
    "Bergmann_2023_RKI_Allergie_Klima": {
        "ieee": "K.-C. Bergmann u. a., „Auswirkungen des Klimawandels auf allergische "
                "Erkrankungen in Deutschland,“ J. Health Monit., Bd. 8, Nr. S4, "
                "S. 82–110, 2023 (RKI-Sachstandsbericht Klimawandel und Gesundheit). "
                "doi: 10.25646/11648 — beschreibt den Spreizungs-Mechanismus der "
                "Pollensaison (Konstruktionsprinzip #96 §3.1).",
        "url": "https://doi.org/10.25646/11648",
        "archive_url": "https://web.archive.org/web/20260831051824/"
                       "https://doi.org/10.25646/11648",
        "accessed": "2026-08-31",
    },
    "Anderegg_2021_Pollensaison": {
        "ieee": "W. R. L. Anderegg u. a., „Anthropogenic climate change is worsening "
                "North American pollen seasons,“ PNAS, Bd. 118, Nr. 7, e2013284118, "
                "2021. doi: 10.1073/pnas.2013284118 (Saisonlänge +8 Tage, Pollenintegral "
                "+20,9 %; klimaattribuierter Anteil ≈ 50 % [IQR 19–84 %] — a_attr).",
        "url": "https://doi.org/10.1073/pnas.2013284118",
        "archive_url": "https://web.archive.org/web/20260808163832/"
                       "https://doi.org/10.1073/pnas.2013284118",
        "accessed": "2026-08-30",
    },
    "Pfaar_2017_EAACI_Pollensaison": {
        "ieee": "O. Pfaar, K.-C. Bergmann u. a., „Defining pollen exposure times for "
                "clinical trials of allergen immunotherapy — an EAACI position paper,“ "
                "Allergy, Bd. 72, S. 713–722, 2017. doi: 10.1111/all.13092 (definiert "
                "die Saisonkriterien Birke/Gräser; publiziert keine festen Längenwerte "
                "— L_B/L_G sind gekennzeichnete Abschätzungen, #96 §3.5).",
        "url": "https://doi.org/10.1111/all.13092",
        "archive_url": "https://web.archive.org/web/20260206101725/"
                       "https://doi.org/10.1111/all.13092",
        "accessed": "2026-08-30",
    },
    "Pfaar_2020_Symptomlast": {
        "ieee": "O. Pfaar u. a., „Pollen season is reflected on symptom load for grass "
                "and birch pollen-induced allergic rhinitis,“ Allergy, Bd. 75, S. 1099, "
                "2020. doi: 10.1111/all.14111 — nur qualitative Stütze (Pollen treibt "
                "Symptomlast); liefert KEINEN Zahlenwert für f (#96 §3.4).",
        "url": "https://doi.org/10.1111/all.14111",
        "archive_url": "https://web.archive.org/web/20260414195017/"
                       "https://doi.org/10.1111/all.14111",
        "accessed": "2026-08-30",
    },
    "Werchan_2017_Pollen_Berlin": {
        "ieee": "B. Werchan u. a., „Spatial distribution of allergenic pollen through a "
                "large metropolitan area,“ Environ. Monit. Assess., Bd. 189, 169, 2017. "
                "doi: 10.1007/s10661-017-5876-8 (Berlin, 14 Pollenfallen: Unterschiede "
                "zwischen Extremstandorten 245 % Birke / 306 % Gräser — λ-Kette #96 §3.4).",
        "url": "https://doi.org/10.1007/s10661-017-5876-8",
        "archive_url": "https://web.archive.org/web/20250916060402/"
                       "https://doi.org/10.1007/s10661-017-5876-8",
        "accessed": "2026-08-30",
    },
    "Werchan_2018_Symptome_Berlin": {
        "ieee": "B. Werchan u. a., „Spatial distribution of pollen-induced symptoms "
                "within a large metropolitan area — Berlin,“ Aerobiologia, Bd. 34, "
                "S. 539, 2018. doi: 10.1007/s10453-018-9529-3 (räumliche Kopplung "
                "Vegetation → Symptomlast; Stütze des λ-Terms).",
        "url": "https://doi.org/10.1007/s10453-018-9529-3",
        "archive_url": "https://web.archive.org/web/20250803100833/"
                       "https://doi.org/10.1007/s10453-018-9529-3",
        "accessed": "2026-08-30",
    },
    "Bogawski_2019_Baumkronen_Pollen": {
        "ieee": "P. Bogawski u. a., „Lidar-Derived Tree Crown Parameters: Are They New "
                "Variables Explaining Local Birch Pollen Concentrations?,“ Forests, "
                "Bd. 10, 1154, 2019. doi: 10.3390/f10121154 (Baumkronen-Parameter "
                "erklären lokale Birkenpollen-Konzentration — Stütze a_veg der λ-Kette).",
        "url": "https://doi.org/10.3390/f10121154",
        "archive_url": "https://web.archive.org/web/20250815192249/"
                       "https://doi.org/10.3390/f10121154",
        "accessed": "2026-08-30",
    },
    "Cardell_2016_TOTALL": {
        "ieee": "L.-O. Cardell u. a., „TOTALL: high cost of allergic rhinitis — a "
                "national Swedish population-based questionnaire study,“ npj Prim. Care "
                "Respir. Med., Bd. 26, 15082, 2016. doi: 10.1038/npjpcrm.2015.82 "
                "(bevölkerungsbasierte Stichprobe, alle Schweregrade: direkte Kosten "
                "210,3 € je Betroffenem·Jahr, Preisstand Feb. 2014 — Basis c_Jahr,direkt).",
        "url": "https://doi.org/10.1038/npjpcrm.2015.82",
        "archive_url": "https://web.archive.org/web/20260607195246/"
                       "https://doi.org/10.1038/npjpcrm.2015.82",
        "accessed": "2026-08-30",
    },
    "BT_Drs_19_22797_Allergiekosten": {
        "ieee": "Deutscher Bundestag, Drucksache 19/22797 (Antwort der Bundesregierung, "
                "23.09.2020), Antwort zu Frage 5: Krankheitskostenrechnung 2015 — "
                "Atmungssystem 16,5 Mrd. €, Asthma 1,9 Mrd. €; „Genauere Angaben zu "
                "Krankheitskosten allergischer Erkrankungen liegen nicht vor“ — Beleg "
                "der fehlenden J30-Ankerreihe (#96 §4, c_kal ≡ 1).",
        "url": "https://dserver.bundestag.de/btd/19/227/1922797.pdf",
        "archive_url": "https://web.archive.org/web/20250624072520/"
                       "https://dserver.bundestag.de/btd/19/227/1922797.pdf",
        "accessed": "2026-08-30",
    },
    "DWD_CDC_Phaenologie": {
        "ieee": "DWD Climate Data Center (CDC), Phänologie-Jahresmelder (wildwachsende "
                "Pflanzen, historisch), opendata.dwd.de — Hasel/Schwarz-Erle/Hänge-Birke "
                "(Blüte Beginn bzw. Blattentfaltung), Wiesen-Fuchsschwanz/Wiesen-"
                "Knäuelgras (Vollblüte); Basis der gemessenen Saison-Spreizung ΔS "
                "(Skript dwd_pollensaison.py).",
        "url": "https://opendata.dwd.de/climate_environment/CDC/observations_germany/"
               "phenology/",
        "archive_url": "https://web.archive.org/web/20250617091132/"
                       "https://opendata.dwd.de/climate_environment/CDC/"
                       "observations_germany/phenology/",
        "accessed": "2026-08-30",
    },
    "Destatis_VPI_lange_Reihen": {
        "ieee": "Statistisches Bundesamt (Destatis), Verbraucherpreisindex für "
                "Deutschland — lange Reihen (2020 = 100): 2000 = 75,9 · 2014 = 94,0 · "
                "2023 = 116,7 · 2024 = 119,3; Wiesbaden. Indexierungsbasis aller "
                "Kostensätze auf den Preisstand 2024.",
        "url": "https://www.destatis.de/DE/Themen/Wirtschaft/Preise/"
               "Verbraucherpreisindex/_inhalt.html",
        "archive_url": "https://web.archive.org/web/20260826041310/"
                       "https://www.destatis.de/DE/Themen/Wirtschaft/Preise/"
                       "Verbraucherpreisindex/_inhalt.html",
        "accessed": "2026-08-30",
    },
    "Feldbusch_2025_HHWS": {
        "ieee": "H. Feldbusch u. a., „Assessing the effectiveness of the heat health "
                "warning system in preventing mortality in 15 German cities: A "
                "difference-in-differences approach,“ Environ. Int., Bd. 203, 109746, "
                "2025. doi: 10.1016/j.envint.2025.109746 (RR 1,00 [0,98–1,01], "
                "adjustiert 0,85).",
        "url": "https://doi.org/10.1016/j.envint.2025.109746",
        "archive_url": "https://web.archive.org/web/20251217031229/"
                       "https://doi.org/10.1016/j.envint.2025.109746",
        "accessed": "2026-08-30",
    },
}


def resolve(keys: list[str] | None) -> list[dict[str, str]]:
    """Bibliografie-Einträge (inkl. ``key``) für eine Referenz-Key-Liste.

    Unbekannte Keys werden still übersprungen, damit ein noch nicht recherchierter
    Verweis die Kostenberechnung nicht bricht (die Prosa in ``source_details`` bleibt
    ohnehin die Basiserklärung).
    """
    out: list[dict[str, str]] = []
    for k in keys or []:
        entry = SOURCE_REFERENCES.get(k)
        if entry:
            out.append({"key": k, **entry})
    return out
