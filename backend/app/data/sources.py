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
