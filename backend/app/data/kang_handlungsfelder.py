"""Brücke KWRA-Handlungsfeld (Risiken) → KAnG-Handlungsfeld (Maßnahmen).

Nachweis nach § 8 Abs. 1 KAnG, Teil 1 (Ticket T-0461, Vorhaben T-0445): Risiken tragen
im Katalog das KWRA-Handlungsfeld als Freitext (``kwra_field``, siehe ``catalog.RISKS``
und ``catalog.PLANNED_RISKS``), Maßnahmen dagegen die KAnG-Einteilung
(``kang_cluster``/``kang_field``, ``catalog.KANG_CLUSTERS``). Für den Nachweis müssen
beide Seiten in derselben Einteilung stehen. Dieses Modul bildet ausschließlich die
Risiko-Seite (KWRA-Feld → KAnG-Cluster/-Feld) ab; ``catalog.py`` bleibt unverändert,
parallele Tickets schreiben dort.

Zehn der zwölf im Katalog vorkommenden KWRA-Handlungsfelder haben eine wortgleiche
oder unmittelbar erkennbare Entsprechung im KAnG-Katalog. Zwei nicht — 'Bauwesen' und
'Tourismuswirtschaft' — dort entscheidet der Bearbeiter und begründet die Wahl im
Feld ``begruendung`` (Vorgabe P1: Quelle oder ausgewiesene Abschätzung).
"""

from __future__ import annotations

from app.data import catalog

# KWRA-Handlungsfeld (Freitext aus catalog.RISKS / catalog.PLANNED_RISKS, Feld
# "kwra_field") → KAnG-Cluster/-Feld (Codes aus catalog.KANG_CLUSTERS) + Begründung.
KWRA_FELD_ZU_KANG: dict[str, dict[str, str]] = {
    "Bauwesen": {
        "cluster": "infrastructure",
        "feld": "buildings",
        "begruendung": (
            "Keine wortgleiche KAnG-Entsprechung. 'Bauwesen' (Bauwirtschaft, Gebäude- "
            "und Immobilienbestand, siehe die zugeordneten geplanten KWRA-Klimawirkungen "
            "wie Stadtklima/Wärmeinseln, Innenraumklima, Hochwasserschäden an Gebäuden) "
            "deckt sich inhaltlich mit dem KAnG-Feld 'Gebäude' im Cluster Infrastruktur — "
            "beide adressieren den baulichen Bestand und seine Errichtung/Sanierung. "
            "Abschätzung von KAP3 (P1)."
        ),
    },
    "Biologische Vielfalt": {
        "cluster": "land",
        "feld": "biodiversity",
        "begruendung": (
            "Wortgleiche fachliche Entsprechung zum KAnG-Feld 'Biologische Vielfalt' "
            "im Cluster Land und Landnutzung."
        ),
    },
    "Boden": {
        "cluster": "land",
        "feld": "soil",
        "begruendung": (
            "Wortgleiche fachliche Entsprechung zum KAnG-Feld 'Boden' im Cluster "
            "Land und Landnutzung."
        ),
    },
    "Fischerei": {
        "cluster": "water",
        "feld": "fisheries",
        "begruendung": (
            "Wortgleiche fachliche Entsprechung zum KAnG-Feld 'Fischerei' im "
            "Cluster Wasser."
        ),
    },
    "Industrie und Gewerbe": {
        "cluster": "economy",
        "feld": "industry",
        "begruendung": (
            "Wortgleiche fachliche Entsprechung zum KAnG-Feld 'Industrie und Gewerbe' "
            "im Cluster Wirtschaft."
        ),
    },
    "Küsten- und Meeresschutz": {
        "cluster": "water",
        "feld": "coastal",
        "begruendung": (
            "Wortgleiche fachliche Entsprechung zum KAnG-Feld 'Küsten- und "
            "Meeresschutz' im Cluster Wasser."
        ),
    },
    "Landwirtschaft": {
        "cluster": "land",
        "feld": "agriculture",
        "begruendung": (
            "Wortgleiche fachliche Entsprechung zum KAnG-Feld 'Landwirtschaft' im "
            "Cluster Land und Landnutzung."
        ),
    },
    "Menschliche Gesundheit": {
        "cluster": "health",
        "feld": "health",
        "begruendung": (
            "Das KAnG-Feld 'Gesundheit und Pflege' ist das einzige Feld im Cluster "
            "Menschliche Gesundheit und Pflege und deckt 'Menschliche Gesundheit' "
            "inhaltlich vollständig ab."
        ),
    },
    "Tourismuswirtschaft": {
        "cluster": "economy",
        "feld": "industry",
        "begruendung": (
            "Keine wortgleiche KAnG-Entsprechung; der KAnG-Katalog kennt kein eigenes "
            "Tourismus-Feld. Tourismuswirtschaft ist ein Dienstleistungs- und "
            "Gewerbesektor und wird deshalb dem KAnG-Feld 'Industrie und Gewerbe' "
            "(Cluster Wirtschaft) zugeordnet — dem einzigen gewerblich-unternehmerischen "
            "Feld neben der Finanzwirtschaft. Abschätzung von KAP3 (P1)."
        ),
    },
    "Verkehr, Verkehrsinfrastruktur": {
        "cluster": "infrastructure",
        "feld": "transport",
        "begruendung": (
            "Wortgleiche fachliche Entsprechung zum KAnG-Feld 'Verkehr und "
            "Verkehrsinfrastruktur' im Cluster Infrastruktur."
        ),
    },
    "Wald- und Forstwirtschaft": {
        "cluster": "land",
        "feld": "forestry",
        "begruendung": (
            "Wortgleiche fachliche Entsprechung zum KAnG-Feld 'Wald und "
            "Forstwirtschaft' im Cluster Land und Landnutzung."
        ),
    },
    "Wasserhaushalt, Wasserwirtschaft": {
        "cluster": "water",
        "feld": "water_management",
        "begruendung": (
            "Wortgleiche fachliche Entsprechung zum KAnG-Feld 'Wasserhaushalt und "
            "Wasserwirtschaft' im Cluster Wasser."
        ),
    },
}


def handlungsfeld_fuer_risiko(code: str | int) -> tuple[str, str]:
    """Liefert (kang_cluster, kang_feld) für einen Risiko-Code.

    ``code`` ist entweder ein Schlüssel aus ``catalog.RISKS_BY_CODE`` (aktive Risiken)
    oder eine ``kwra_id`` aus ``catalog.PLANNED_BY_KWRA_ID`` (geplante/gesperrte
    Risiken — sie tragen im Katalog keinen eigenen ``code``, ihre ``kwra_id`` ist der
    Identifikator). Unbekannte Codes werfen ``KeyError``.
    """
    if code in catalog.RISKS_BY_CODE:
        kwra_field = catalog.RISKS_BY_CODE[code]["kwra_field"]
    elif code in catalog.PLANNED_BY_KWRA_ID:
        kwra_field = catalog.PLANNED_BY_KWRA_ID[code]["kwra_field"]
    else:
        raise KeyError(code)

    eintrag = KWRA_FELD_ZU_KANG[kwra_field]
    return (eintrag["cluster"], eintrag["feld"])
