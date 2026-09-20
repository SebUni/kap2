"""Nachweisrechnung je KAnG-Handlungsfeld (Ticket T-0462, Teil 2 des Nachweises
nach § 8 Abs. 1 KAnG, Vorhaben T-0445).

§ 8 Abs. 1 KAnG verlangt von den Trägern öffentlicher Aufgaben, die Belange der
Klimaanpassung *fachübergreifend und integriert* zu berücksichtigen. Dieses Modul
liefert die dafür nötige Gegenüberstellung: für jedes KAnG-Handlungsfeld
(``catalog.KANG_CLUSTERS``) steht nebeneinander, welche Risiken einer Planung dort
Schaden verursachen und welche Maßnahmen dieser Planung dort ansetzen. Daraus
folgt je Feld einer von drei Zuständen — 'berücksichtigt', 'offen',
'nicht betroffen' — und in der Zusammenfassung die Liste der offenen Felder.

Es wird **nichts neu gerechnet**: Eingang sind die andernorts berechneten
jährlichen Schadenssummen je Risikocode und die Maßnahmenliste der Planung; das
Modul ordnet diese vorhandenen Zahlen nur den Handlungsfeldern zu. Die Zuordnung
Risiko → Handlungsfeld kommt aus Teil 1 (``app.data.kang_handlungsfelder``), die
Zuordnung Maßnahme → Handlungsfeld aus den Katalogfeldern ``kang_cluster`` /
``kang_field`` der Maßnahmen.

Der 'integriert'-Teil der Vorschrift wird über ``integrierende_massnahmen``
abgebildet: Maßnahmen, deren ``linked_risk_codes`` auf mehr als ein
Handlungsfeld führen, wirken über Fachgrenzen hinweg.

Grenze der Aussage: Die Rechnung ist eine Vollständigkeitsprüfung gegen den
Katalog, keine Rechtsauskunft — siehe ``ABGRENZUNG``.
"""

from __future__ import annotations

from app.data import catalog
from app.data.kang_handlungsfelder import handlungsfeld_fuer_risiko

STATUS_BERUECKSICHTIGT = "berücksichtigt"
STATUS_OFFEN = "offen"
STATUS_NICHT_BETROFFEN = "nicht betroffen"

#: Was diese Rechnung leistet und was nicht. Wörtlich in die Ausgabe übernommen,
#: damit die Einschränkung jede Weiterverwendung (Export, Bericht) begleitet.
ABGRENZUNG: str = (
    "Diese Nachweisrechnung stellt den nach § 8 Abs. 1 KAnG geforderten "
    "fachübergreifenden und integrierten Blick als Gegenüberstellung dar: je "
    "KAnG-Handlungsfeld die zugeordneten Risiken mit ihrer jährlichen "
    "Schadenssumme und die dort ansetzenden Maßnahmen der Planung. Sie richtet "
    "sich an Träger öffentlicher Aufgaben als Arbeitshilfe für die eigene "
    "Abwägung und bescheinigt keine Rechtskonformität: Ob die Belange der "
    "Klimaanpassung im Sinne des § 8 Abs. 1 KAnG berücksichtigt worden sind, "
    "entscheidet der Träger in eigener Verantwortung. Geprüft wird allein die "
    "Vollständigkeit gegenüber dem hinterlegten Risiko- und Maßnahmenkatalog; "
    "Risiken, Maßnahmen oder Belange außerhalb dieses Katalogs bleiben "
    "unberücksichtigt, und ein Feld ohne Schaden im Modell ('nicht betroffen') "
    "kann in der Sache dennoch betroffen sein."
)


def _handlungsfeld_reihenfolge() -> list[tuple[str, str]]:
    """Alle Paare (Cluster-Code, Feld-Code) in Katalogreihenfolge."""
    return [
        (cluster["code"], feld["code"])
        for cluster in catalog.KANG_CLUSTERS
        for feld in cluster["fields"]
    ]


def _felder_einer_massnahme(code: str) -> set[tuple[str, str]]:
    """Handlungsfelder, auf die die verknüpften Risiken einer Maßnahme führen."""
    massnahme = catalog.MEASURES_BY_CODE[code]
    return {
        handlungsfeld_fuer_risiko(risiko_code)
        for risiko_code in (massnahme.get("linked_risk_codes") or [])
    }


def nachweis_fachuebergreifend(
    schaeden: dict[str, float],
    massnahmen: list[str],
) -> dict:
    """Stellt Risiken und Maßnahmen einer Planung je KAnG-Handlungsfeld gegenüber.

    ``schaeden`` bildet Risikocodes (Schlüssel aus ``catalog.RISKS_BY_CODE`` oder
    ``kwra_id`` aus ``catalog.PLANNED_BY_KWRA_ID``) auf die jährliche
    Schadenssumme in Euro ab; ``massnahmen`` ist die Liste der Maßnahmencodes der
    Planung (Schlüssel aus ``catalog.MEASURES_BY_CODE``). Unbekannte Codes auf
    einer der beiden Seiten werfen ``KeyError`` — ein Nachweis, der eine Position
    still unterschlägt, wäre wertlos.

    Regel je Handlungsfeld: betroffen ist es, wenn ihm mindestens ein Risiko mit
    Schaden größer null zugeordnet ist. Betroffen mit mindestens einer
    zugeordneten Maßnahme heißt 'berücksichtigt', betroffen ohne Maßnahme heißt
    'offen', sonst 'nicht betroffen'.

    Rückgabe: dict mit ``handlungsfelder`` (ein Eintrag je Cluster-/Feld-Paar in
    Katalogreihenfolge), ``zusammenfassung`` und ``abgrenzung``.
    """
    felder = _handlungsfeld_reihenfolge()

    risiken_je_feld: dict[tuple[str, str], list[str]] = {f: [] for f in felder}
    schaden_je_feld: dict[tuple[str, str], float] = {f: 0.0 for f in felder}
    for risiko_code, betrag in schaeden.items():
        feld = handlungsfeld_fuer_risiko(risiko_code)
        wert = float(betrag or 0.0)
        if wert <= 0.0:
            continue
        risiken_je_feld[feld].append(risiko_code)
        schaden_je_feld[feld] += wert

    massnahmen_je_feld: dict[tuple[str, str], list[str]] = {f: [] for f in felder}
    integrierende: list[str] = []
    gesehen: set[str] = set()
    for massnahme_code in massnahmen:
        eintrag = catalog.MEASURES_BY_CODE[massnahme_code]
        if massnahme_code in gesehen:
            continue
        gesehen.add(massnahme_code)
        feld = (eintrag["kang_cluster"], eintrag["kang_field"])
        if feld in massnahmen_je_feld:
            massnahmen_je_feld[feld].append(massnahme_code)
        if len(_felder_einer_massnahme(massnahme_code)) > 1:
            integrierende.append(massnahme_code)

    handlungsfelder: list[dict] = []
    for feld in felder:
        cluster_code, feld_code = feld
        risiken = risiken_je_feld[feld]
        feld_massnahmen = massnahmen_je_feld[feld]
        if not risiken:
            status = STATUS_NICHT_BETROFFEN
        elif feld_massnahmen:
            status = STATUS_BERUECKSICHTIGT
        else:
            status = STATUS_OFFEN
        handlungsfelder.append({
            "cluster": cluster_code,
            "feld": feld_code,
            "status": status,
            "risiken": risiken,
            "schaden_eur": schaden_je_feld[feld],
            "massnahmen": feld_massnahmen,
        })

    betroffen = [e for e in handlungsfelder if e["status"] != STATUS_NICHT_BETROFFEN]
    offen = [e for e in betroffen if e["status"] == STATUS_OFFEN]

    return {
        "handlungsfelder": handlungsfelder,
        "zusammenfassung": {
            "betroffen_n": len(betroffen),
            "beruecksichtigt_n": len(betroffen) - len(offen),
            "offen_n": len(offen),
            "offene_handlungsfelder": [
                {"cluster": e["cluster"], "feld": e["feld"]} for e in offen
            ],
            "integrierende_massnahmen": integrierende,
        },
        "abgrenzung": ABGRENZUNG,
    }
