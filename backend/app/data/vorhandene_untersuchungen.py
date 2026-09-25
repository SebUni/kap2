"""Verzeichnis vorhandener Untersuchungen mit Fundorten je Land (Datenmodul, T-1166, A3/A10/A11/A13).

Quelle ist die Infobox „Datenquellen“ der UBA-Broschüre (S. 12–13): Vorhandene Untersuchungen
(Hochwassergefahren- und Hochwasserrisikokarten, Starkregengefahrenkarten, Analysen zu
städtischen Hitzeinseln und Feinstaub, wetterbedingte Einsätze der Feuerwehr, Klimafunktions-
und Klimaanalysekarten), Naturgefahrenreport, Nationaler Klimareport, CatRaRe, Klimarisikoanalysen
der Länder und KWRA. Die Kommune führt den Schritt „vorhandene Informationen sichten“ selbst;
das Produkt liefert das Material. Das Modul liest zur Laufzeit nichts aus dem Netz.

Die URLs der Landesportale wurden am 25.09.2026 abgerufen (jeweils HTTP 200). Hat ein Land
keine eigene Klimarisikoanalyse veröffentlicht, steht in ``kra_land`` ein Satz mit Datum statt
eines leeren Feldes (Vorgabe P2). Die Schlüssel von ``LANDESPORTALE`` entsprechen der Schreibweise
in ``Kommune.bundesland`` (siehe ``app.services.osm_service.BUNDESLAENDER``).
"""

from __future__ import annotations

_KOMMUNAL = "bei der Fachabteilung der Kommune zu erfragen (Umwelt-, Tiefbau- oder Stadtplanungsamt, Feuerwehr)"

UNTERSUCHUNGEN: list[dict[str, str]] = [
    {
        "code": "hochwassergefahrenkarten",
        "bezeichnung": "Hochwassergefahren- und Hochwasserrisikokarten nach EU-Hochwasserrisikomanagement-Richtlinie",
        "ebene": "land",
        "wo_erhaeltlich": "Landesportal des Bundeslands, URL je Land unter LANDESPORTALE[Land]['hochwasser']; "
                          "länderübergreifend im Kartenviewer der Bundesanstalt für Gewässerkunde: "
                          "https://geoportal.bafg.de/karten/HWRM/",
    },
    {
        "code": "starkregengefahrenkarten",
        "bezeichnung": "Starkregengefahrenkarten",
        "ebene": "kommunal",
        "wo_erhaeltlich": _KOMMUNAL + "; einige Länder stellen Karten für ihr Gebiet bereit",
    },
    {
        "code": "klimaanalysekarten",
        "bezeichnung": "Klimafunktions- und Klimaanalysekarten",
        "ebene": "kommunal",
        "wo_erhaeltlich": _KOMMUNAL,
    },
    {
        "code": "hitzeinseln",
        "bezeichnung": "Analysen zu städtischen Hitzeinseln",
        "ebene": "kommunal",
        "wo_erhaeltlich": _KOMMUNAL,
    },
    {
        "code": "feinstaub",
        "bezeichnung": "Analysen zu Feinstaub",
        "ebene": "kommunal",
        "wo_erhaeltlich": _KOMMUNAL,
    },
    {
        "code": "feuerwehreinsaetze",
        "bezeichnung": "Wetterbedingte Einsätze der Feuerwehr",
        "ebene": "kommunal",
        "wo_erhaeltlich": "bei der örtlichen Feuerwehr bzw. der Leitstelle zu erfragen (Einsatzstatistik)",
    },
    {
        "code": "catrare",
        "bezeichnung": "CatRaRE – Katalog radarbasierter Starkregenereignisse des Deutschen Wetterdienstes (DWD)",
        "ebene": "bund",
        "wo_erhaeltlich": "https://www.dwd.de/DE/leistungen/catrare/catrare.html; Daten: "
                          "https://opendata.dwd.de/climate_environment/CDC/event_catalogues/germany/precipitation/CatRaRE_v2026.01/data/",
    },
    {
        "code": "naturgefahrenreport",
        "bezeichnung": "Naturgefahrenreport des Gesamtverbands der Deutschen Versicherungswirtschaft (GDV)",
        "ebene": "bund",
        "wo_erhaeltlich": "https://www.gdv.de/gdv/statistik/datenservice-zum-naturgefahrenreport",
    },
    {
        "code": "klimareport",
        "bezeichnung": "Nationaler Klimareport des Deutschen Wetterdienstes (DWD)",
        "ebene": "bund",
        "wo_erhaeltlich": "https://www.dwd.de/DE/leistungen/nationalerklimareport/report.html",
    },
    {
        "code": "kra_land",
        "bezeichnung": "Klimarisikoanalyse (KRA) des Landes",
        "ebene": "land",
        "wo_erhaeltlich": "Landesregierung des Bundeslands, URL je Land unter LANDESPORTALE[Land]['kra_land']; "
                          "Überblick der Länder: "
                          "https://www.umweltbundesamt.de/themen/klima-energie/klimafolgen-anpassung/anpassung-an-den-klimawandel/anpassung-auf-laenderebene",
    },
    {
        "code": "kwra",
        "bezeichnung": "Klimawirkungs- und Risikoanalyse für Deutschland (KWRA)",
        "ebene": "bund",
        "wo_erhaeltlich": "https://www.bundesumweltministerium.de/themen/klimaanpassung/gesundheit-im-klimawandel/klimawirkungs-und-risikoanalyse-kwra-fuer-deutschland",
    },
]

_KEINE_KRA = "Keine eigene, veröffentlichte Klimarisikoanalyse des Landes gefunden (Stand 25.09.2026)"

LANDESPORTALE: dict[str, dict[str, str]] = {
    "Baden-Württemberg": {
        "hochwasser": "https://www.hochwasser.baden-wuerttemberg.de/",
        "kra_land": _KEINE_KRA + "; die Anpassungsstrategie 2023 enthält Vulnerabilitätsbewertungen für elf Handlungsfelder: "
                    "https://um.baden-wuerttemberg.de/de/klima-energie/klimawandel-und-anpassung/anpassung-an-den-klimawandel/anpassungsstrategie-baden-wuerttemberg",
    },
    "Bayern": {
        "hochwasser": "https://www.lfu.bayern.de/wasser/hw_risikomanagement_umsetzung/hwgk_hwrk/index.htm",
        "kra_land": _KEINE_KRA,
    },
    "Berlin": {
        "hochwasser": "https://www.berlin.de/umweltatlas/wasser/hochwasser/fortlaufend-aktualisiert/kartenbeschreibung/",
        "kra_land": "https://www.berlin.de/sen/uvk/klimaschutz/anpassung-an-den-klimawandel/klimarisikoanalyse/",
    },
    "Brandenburg": {
        "hochwasser": "https://lfu.brandenburg.de/lfu/de/aufgaben/wasser/hochwasserschutz/hochwasserrisikomanagement/",
        "kra_land": _KEINE_KRA,
    },
    "Bremen": {
        "hochwasser": "https://umwelt.bremen.de/umwelt/hochwasser-und-kuestenschutz-quantitative-wasserwirtschaft/hochwasserrisikomanagement-23599",
        "kra_land": "https://www.klimaanpassung.bremen.de/klimaanpassung/die-klimaanpassungsstrategie/klimarisikoanalyse-23667",
    },
    "Hamburg": {
        "hochwasser": "https://www.hamburg.de/politik-und-verwaltung/behoerden/bukea/themen/wasser/hochwasser/hochwasserrisikomanagement/gefahren-risiko-karten-176540",
        "kra_land": _KEINE_KRA,
    },
    "Hessen": {
        "hochwasser": "https://www.hlnug.de/themen/wasser/hochwasser/hochwasserrisikomanagement",
        "kra_land": "Klimarisikoanalyse des Landes in Erarbeitung, Teil der Klimaanpassungsstrategie bis Anfang 2027 (Stand 25.09.2026)",
    },
    "Mecklenburg-Vorpommern": {
        "hochwasser": "https://www.lung.mv-regierung.de/",
        "kra_land": "Klimarisikoanalyse des Landes in Erarbeitung, Grundlage der Klimaanpassungsstrategie (Stand 25.09.2026)",
    },
    "Niedersachsen": {
        "hochwasser": "https://www.umweltkarten-niedersachsen.de/",
        "kra_land": "https://zkfn.de/klimarisikoanalyse-fuer-niedersachsen-2025/",
    },
    "Nordrhein-Westfalen": {
        "hochwasser": "https://www.flussgebiete.nrw.de/",
        "kra_land": _KEINE_KRA,
    },
    "Rheinland-Pfalz": {
        "hochwasser": "https://hochwassermanagement.rlp-umwelt.de/",
        "kra_land": _KEINE_KRA,
    },
    "Saarland": {
        "hochwasser": "https://www.saarland.de/mukmav/DE/portale/wasser/informationen/hochwasserschutzimsaarland/hochwasservorsorgeeigenvorsorge/hochwasserrisikoerkennen/hochwasserrisikoerkennen_node.html",
        "kra_land": _KEINE_KRA,
    },
    "Sachsen": {
        "hochwasser": "https://www.umwelt.sachsen.de/hochwasser-4101.html",
        "kra_land": _KEINE_KRA,
    },
    "Sachsen-Anhalt": {
        "hochwasser": "https://lhw.sachsen-anhalt.de/",
        "kra_land": _KEINE_KRA,
    },
    "Schleswig-Holstein": {
        "hochwasser": "https://www.schleswig-holstein.de/DE/fachinhalte/H/hochwasserschutz",
        "kra_land": "https://www.schleswig-holstein.de/DE/fachinhalte/K/klimaschutz/Downloads/klimarisikoanalyse.pdf?__blob=publicationFile&v=1",
    },
    "Thüringen": {
        "hochwasser": "https://tlubn.thueringen.de/wasser/hochwasserschutz",
        "kra_land": _KEINE_KRA,
    },
}

NACHBAR_SATZ = (
    "Liegen der Kommune keine eigenen Informationen vor, können Informationen benachbarter oder "
    "vergleichbarer Kommunen, des Kreises oder des Landes herangezogen werden."
)
