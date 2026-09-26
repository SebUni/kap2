"""Katalog der Bestandsaufnahme-Größen (ISO 14091, Checklistenzeile 16, Teil 1).

Ticket T-0754, Vorhaben T-0447. Reines Datenmodul: kein Netz, keine Rechnung.
Jede Größe trägt entweder Quellschlüssel aus ``sources.SOURCE_REFERENCES`` oder
einen Lückensatz (Vorgabe P1) — nie beides, nie keines.
"""

from __future__ import annotations

LUECKENSATZ_VORLAGE = (
    "Für die Größe {label} liegt dem Produkt keine Datenquelle je Kommune vor; "
    "sie ist im Rahmen der Konzepterstellung vor Ort zu erheben."
)

# Laufzeitsatz, wenn eine sonst vorhandene Quelle für die Kommune nicht abrufbar war.
LAUFZEITSATZ_VORLAGE = (
    "Für die Größe {label} war die Datenquelle für diese Kommune nicht abrufbar; "
    "der Wert fehlt in dieser Bestandsaufnahme."
)

# Lückensatz, wenn eine flächenbezogene Größe (Starkregenereignisse) nicht zählbar ist,
# weil dem Produkt weder die Gemeindegrenze noch gespeicherte Rasterzellen der Kommune
# vorliegen. Die Quelle selbst ist vorhanden; es fehlt die Fläche (T-1297).
FLAECHE_FEHLT_SATZ_VORLAGE = (
    "Für die Größe {label} fehlt dem Produkt die Fläche der Kommune: Weder die "
    "Gemeindegrenze noch Rasterzellen der Kommune sind gespeichert. Der Wert fehlt in "
    "dieser Bestandsaufnahme."
)


HINWEIS_NICHT_IM_KATALOG = "nicht im Katalog"


def _g(code, gruppe, label, einheit, quellen=None, hinweis=None):
    eintrag = {
        "code": code,
        "gruppe": gruppe,
        "label": label,
        "einheit": einheit,
        "quellen": list(quellen or []),
        "luecke": "" if quellen else LUECKENSATZ_VORLAGE.format(label=label),
    }
    if hinweis:
        eintrag["hinweis"] = hinweis
    return eintrag


_VP = "vulnerable_personen"
_NS = "natuerliche_systeme"
_KS = "klimasensible_strukturen"
_VE = "vergangene_ereignisse"
_TR = "trends"

BESTANDSAUFNAHME_GROESSEN: list[dict] = [
    _g("aeltere_ab_65", _VP, "Ältere Menschen ab 65 Jahren", "%", ["Zensus_2022"]),
    _g("kinder_unter_18", _VP, "Kinder und Jugendliche unter 18 Jahren", "%", ["Zensus_2022"]),
    _g("arbeitslosenquote", _VP, "Arbeitslose (Arbeitslosenquote)", "%", ["Regionalstatistik_GENESIS"]),
    _g("pflegebeduerftige", _VP, "Pflegebedürftige Menschen", ""),
    _g("alleinlebende_aeltere", _VP, "Alleinlebende ältere Menschen", ""),
    _g("vorerkrankte", _VP, "Menschen mit Vorerkrankungen", ""),
    _g("wohnungslose", _VP, "Wohnungslose Menschen", ""),
    _g("gewaesser", _NS, "Gewässer", "", hinweis=HINWEIS_NICHT_IM_KATALOG),
    _g("wald", _NS, "Wald", "", hinweis=HINWEIS_NICHT_IM_KATALOG),
    _g("boeden", _NS, "Böden", "", hinweis=HINWEIS_NICHT_IM_KATALOG),
    _g("schutzgebiete", _NS, "Schutzgebiete", "", hinweis=HINWEIS_NICHT_IM_KATALOG),
    _g("energie", _KS, "Energieinfrastruktur", "Vorkommen", ["OSM_Data", "BBK_KRITIS"]),
    _g("wasser_abwasser", _KS, "Wasser- und Abwasserinfrastruktur", "Vorkommen", ["OSM_Data", "BBK_KRITIS"]),
    _g("verkehrsknoten", _KS, "Verkehrsknoten", "Vorkommen", ["OSM_Data", "BBK_KRITIS"]),
    _g("kommunikation", _KS, "Kommunikationsinfrastruktur", "Vorkommen", ["OSM_Data", "BBK_KRITIS"]),
    _g("krankenhaeuser", _KS, "Krankenhäuser", "Anzahl", ["OSM_Data"]),
    _g("pflegeeinrichtungen", _KS, "Pflegeeinrichtungen", "Anzahl", ["OSM_Data"]),
    _g("kitas_schulen", _KS, "Kindertagesstätten und Schulen", ""),
    _g("lieferketten", _KS, "Lieferketten", "", hinweis=HINWEIS_NICHT_IM_KATALOG),
    _g("starkregenereignisse", _VE, "Vergangene Starkregenereignisse seit 2001 (CatRaRE)", "Anzahl", ["DWD_CatRaRE"]),
    _g("schadensereignisse", _VE, "Vergangene Schadensereignisse durch Wetterextreme", ""),
    _g("bevoelkerungsentwicklung", _TR, "Bevölkerungsentwicklung", "%", ["Destatis_GVISys_Bevoelkerung"]),
]
