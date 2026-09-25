"""KWRA-Bereichsvergleich der Anpassungsfähigkeit — übernommen aus Kap. 7.

Quelle: UBA/BMU „Klimawirkungs- und Risikoanalyse 2021 für Deutschland" (KWRA 2021),
Teilbericht 6 (Integrierte Auswertung), Kapitel 7 „Querbetrachtung der Systembereiche",
S. 146–154, dazu Abbildung 24 „Klimarisiken von betroffenen Systemen, Wirkbeziehungen und
Dringlichkeit von Anpassung" (S. 152).

Das Modul **übernimmt** den Vergleich der Bundesanalyse, es rechnet nichts. Je Systembereich
(Reihenfolge wie ``catalog.KWRA_SYSTEMBEREICHE``) stehen vier Blöcke:

- ``wirksamkeit`` — Wirksamkeit der beschlossenen und der weiterreichenden Anpassung,
  Unterschied zwischen optimistischem und pessimistischem Fall (Konformitätsliste Zeile 10, A3);
- ``klimarisiko_mit_anpassung`` — Klimarisiko nach Anpassung (A3, A5);
- ``anpassungsdauer`` — Anpassungsdauer im Vergleich der Bereiche (A4);
- ``grenzen`` — Grenzen der Anpassung (A5).

Jeder Block hat ``valide_aussage`` (sagt der Text für diesen Bereich etwas aus?), ``aussage``
(Wiedergabe mit Zitaten aus dem Text), ``seiten`` (Druckseiten des Berichts, auf denen die
Aussage steht) und, wo der Text sie nennt, ``klimawirkungen``. Sagt die Quelle ausdrücklich,
dass es für einen Bereich keine valide Aussage gibt (S. 150 für naturferne
Wirtschaftssysteme, S. 151 für Menschen und soziale Systeme), steht genau das da und kein Wert.
Schweigt der Text zu einem Block, steht ``valide_aussage: False`` mit den gelesenen Seiten des
Bereichsabschnitts und dem Vermerk, dass der Text dazu nichts sagt — nie ein geratener Wert.

Abbildung 24 zeigt die Balken „Klimarisiko mit und ohne Anpassung“ mit „Wirksamkeit der
Anpassung“ nur grafisch und ohne Zahlen; sie sind hier nicht abgelesen, sondern nur als
Hinweis „nur grafisch, Abb. 24, S. 152“ geführt.
"""

from __future__ import annotations

QUELLE = (
    "UBA/BMU, ›Klimawirkungs- und Risikoanalyse 2021 für Deutschland‹, Teilbericht 6 "
    "(Integrierte Auswertung), Kapitel 7 ›Querbetrachtung der Systembereiche‹, S. 146–154; "
    "Abbildung 24, S. 152. Dessau-Roßlau, 2021. "
    "Datei docs/KWAR/kwra2021_teilbericht_6_integrierte_auswertung_bf_211027_0.pdf."
)

BLOECKE: tuple[str, ...] = (
    "wirksamkeit",
    "klimarisiko_mit_anpassung",
    "anpassungsdauer",
    "grenzen",
)

ABBILDUNG_24 = (
    "Nur grafisch, Abb. 24, S. 152: Balken „Klimarisiko mit und ohne Anpassung“ mit "
    "„Wirksamkeit der Anpassung“ für die Auswahl der Klimawirkungen mit sehr dringendem "
    "Anpassungsbedarf — natürliche Systeme und Ressourcen „Auswahl (11)“, naturnutzende "
    "Wirtschaftssysteme „Auswahl (10)“, Infrastrukturen und Gebäude „Auswahl (7)“. Für "
    "naturferne Wirtschaftssysteme und Menschen und soziale Systeme zeigt die Abbildung nur "
    "„Klimarisiko ohne Anpassung“. Keine Zahlenwerte in der Abbildung."
)

SCHLUSS_ANPASSUNG = {
    "aussage": (
        "Für den Bereich „Natürliche Systeme und Ressourcen“ ist „die Anpassungsdauer "
        "tendenziell deutlich höher“, und „die Wirksamkeit von Anpassungsmaßnahmen [ist] "
        "vergleichsweise gering“ (S. 153). „Wie erwähnt sind jedoch die Möglichkeiten "
        "erfolgreicher Klimaanpassung gerade in dem Systembereich ‚Natürliche Systeme und "
        "Ressourcen‘ besonders eingeschränkt“ (S. 154)."
    ),
    "seiten": [153, 154],
}

_KEINE_AUSSAGE_IM_TEXT = "Der Text von Kap. 7 sagt dazu für diesen Bereich nichts aus."

BEREICHSVERGLEICH_ANPASSUNG: dict[str, dict] = {
    "Natürliche Systeme und Ressourcen": {
        "wirksamkeit": {
            "valide_aussage": True,
            "vergleich": "niedriger als in den anderen Bereichen",
            "aussage": (
                "„Die Anpassungsmöglichkeiten sind tendenziell eher geringer als bei den anderen "
                "[…] Systemen. So wird die durchschnittliche Wirksamkeit von weiterreichender "
                "Anpassung als deutlich niedriger eingeschätzt als bei anderen "
                "Systembereichen.“ „Die beschlossenen Anpassungsmaßnahmen sind bei diesen "
                "Systemen weniger wirksam als bei den Klimawirkungen anderer Systeme.“ (S. 146) "
                "Die Gewissheit bei der Bewertung der Anpassungskapazität ist „tendenziell "
                "geringer als in den anderen Bereichen“ (S. 147). Schluss: Wirksamkeit "
                "„vergleichsweise gering“ (S. 153)."
            ),
            "seiten": [146, 147, 153],
        },
        "klimarisiko_mit_anpassung": {
            "valide_aussage": True,
            "aussage": (
                "Bei fünf Klimawirkungen wird „trotz weiterreichender Anpassung bereits zur Mitte "
                "des Jahrhunderts mit mittel-hohen oder hohen Klimarisiken im pessimistischen "
                "Fall gerechnet“ (S. 147)."
            ),
            "klimawirkungen": [
                "Bodenerosion durch Wasser",
                "Ausbreitung invasiver Arten",
                "Schäden an Wäldern",
                "Sturzfluten (Versagen von Entwässerungseinrichtungen und Überflutungsschutzsystemen)",
                "Grundwasserstand und Grundwasserqualität",
            ],
            "seiten": [147],
        },
        "anpassungsdauer": {
            "valide_aussage": True,
            "vergleich": "länger als in den anderen Bereichen",
            "aussage": (
                "„Die Anpassungsdauer ist bei diesen Systemen zumeist relativ lange, das heißt "
                "meist über zehn und teils über 50 Jahre, und im Durchschnitt deutlich länger "
                "als bei den anderen Systembereichen.“ Bei drei Klimawirkungen besteht „schon "
                "jetzt kaum noch die Zeit […], um bei einem starken Klimawandel die "
                "Klimarisiken noch rechtzeitig umfassend einzudämmen“ (S. 147). Schluss: "
                "Anpassungsdauer „tendenziell deutlich höher“ (S. 153)."
            ),
            "klimawirkungen": [
                "Schäden an Wäldern",
                "Wasserqualität und Grundwasserversalzung",
                "Naturräumliche Veränderungen an Küsten",
            ],
            "seiten": [147, 153],
        },
        "grenzen": {
            "valide_aussage": True,
            "aussage": (
                "„Bei vier untersuchten Klimawirkungen aus diesem Bereich werden auch die Grenzen "
                "der Anpassung absehbar überschritten, weil Anpassungsmaßnahmen grundsätzlich "
                "nicht zur Verfügung stehen“ (S. 147). Zusammen mit den neun vorgelagerten "
                "Klimawirkungen bestehen bei 13 Klimawirkungen keine Anpassungsmöglichkeiten "
                "(S. 147). Die Möglichkeiten erfolgreicher Klimaanpassung sind in diesem Bereich "
                "„besonders eingeschränkt“ (S. 154)."
            ),
            "klimawirkungen": [
                "Veränderung der Länge der Vegetationsperiode und Phänologie",
                "Schäden an Gebirgsökosystemen",
                "Bodenbiologie",
                "Bodenfunktionen: Filter- und Pufferfunktionen",
            ],
            "anzahl_ohne_anpassungsmoeglichkeit": 4,
            "seiten": [147, 154],
        },
    },
    "Naturnutzende Wirtschaftssysteme": {
        "wirksamkeit": {
            "valide_aussage": True,
            "vergleich": "höher als bei den natürlichen Systemen, insgesamt nicht überdurchschnittlich",
            "aussage": (
                "„Die beschlossenen Anpassungsmaßnahmen werden voraussichtlich deutlich wirksamer "
                "sein als bei den ‚Natürlichen Systemen und Ressourcen‘. Auch die Potentiale bei "
                "den weiterreichenden Anpassungsmaßnahmen sind grundsätzlich höher, aber in der "
                "Gesamtbetrachtung aller Systembereiche nicht überdurchschnittlich.“ Relativ hohe "
                "Potentiale in der Landwirtschaft, geringe in der Wald- und Forstwirtschaft und "
                "in der Fischerei. „Auffallend ist die erhebliche Diskrepanz zwischen der "
                "Wirksamkeit von Maßnahmen im optimistischen und im pessimistischen Fall“; bei "
                "starkem Klimawandel sinkt die Wirksamkeit erheblich (S. 148)."
            ),
            "seiten": [148],
        },
        "klimarisiko_mit_anpassung": {
            "valide_aussage": True,
            "aussage": (
                "Die Lage mit Anpassung sieht „spürbar besser aus als im Fall der ‚Natürlichen "
                "Systeme und Ressourcen‘“. Trotzdem wurde „für sechs von 11 insgesamt bewerteten "
                "Klimawirkungen das Klimarisiko mit Anpassung Mitte des Jahrhunderts im "
                "pessimistischen Fall auf mittel-hoch eingeschätzt“ (S. 148)."
            ),
            "klimawirkungen": [
                "Produktionsfunktionen",
                "Hitze und Trockenstress",
                "Nutzfunktion: Holzertrag",
                "Stress durch Schädlinge/Krankheiten",
                "Entkopplung von Nahrungsbeziehungen in der Ostsee",
                "Verbreitung von Fischarten",
            ],
            "anzahl_mittel_hoch": 6,
            "anzahl_bewertet": 11,
            "seiten": [148],
        },
        "anpassungsdauer": {
            "valide_aussage": True,
            "vergleich": "im Durchschnitt, stark streuend",
            "aussage": (
                "„Die mittlere Anpassungsdauer in diesem Systembereich liegt zwar im Durchschnitt "
                "aller Klimawirkungen, sie streut aber recht stark.“ Bei zwei Klimawirkungen "
                "reicht die Zeit zur Anpassung „jetzt schon kaum noch […] bis zur Mitte des "
                "Jahrhunderts (Anpassungsdauer über 50 Jahre), sofern es zu einem starken "
                "Klimawandel kommt“ (S. 148)."
            ),
            "klimawirkungen": [
                "Hitze und Trockenstress",
                "Stress durch Schädlinge/Krankheiten",
            ],
            "seiten": [148],
        },
        "grenzen": {
            "valide_aussage": True,
            "aussage": (
                "„Im Unterschied zu den ‚Natürlichen Systemen und Ressourcen‘ wurde in dem "
                "Systembereich auch keine Klimawirkung identifiziert, für die es keine "
                "Reaktionsmöglichkeiten gibt“ (S. 148)."
            ),
            "klimawirkungen": [],
            "anzahl_ohne_anpassungsmoeglichkeit": 0,
            "seiten": [148],
        },
    },
    "Infrastrukturen und Gebäude": {
        "wirksamkeit": {
            "valide_aussage": True,
            "vergleich": "höher als in den anderen Bereichen",
            "aussage": (
                "„Den tendenziell geringeren Klimarisiken steht eine besonders hohe Wirksamkeit "
                "der Anpassung gegenüber, die auch wenig davon beeinflusst wird, ob der "
                "Klimawandel stärker oder schwächer ausfällt.“ Für beschlossene wie "
                "weiterreichende Maßnahmen, im optimistischen wie im pessimistischen Fall sind "
                "die Möglichkeiten „im Vergleich zu den anderen Systembereichen relativ hoch“. "
                "Die Gewissheit bei den Anpassungsmaßnahmen liegt „deutlich über den anderen "
                "Systembereichen“ (S. 149)."
            ),
            "seiten": [149],
        },
        "klimarisiko_mit_anpassung": {
            "valide_aussage": True,
            "aussage": (
                "Die Kombination aus geringeren Risiken ohne Anpassung und hoher Wirksamkeit "
                "kann „zu einer deutlich besseren Risikosituation zur Mitte des Jahrhunderts (im "
                "Vergleich zu anderen Systembereichen) führen“ (S. 149–150). „Mit einer "
                "weiterreichenden Anpassung können die resultierenden Klimarisiken auch im "
                "pessimistischen Fall auf ‚mittel‘ oder ‚gering-mittel‘ eingegrenzt werden“ "
                "(S. 150)."
            ),
            "seiten": [149, 150],
        },
        "anpassungsdauer": {
            "valide_aussage": True,
            "vergleich": "meist mittel, laut Text länger als in anderen Bereichen",
            "aussage": (
                "„Vor diesem Hintergrund ist auch die meist mittlere Anpassungsdauer (länger als "
                "in anderen Systembereichen) weniger kritisch“ (S. 150)."
            ),
            "seiten": [150],
        },
        "grenzen": {
            "valide_aussage": False,
            "aussage": (
                _KEINE_AUSSAGE_IM_TEXT + " Der Abschnitt (S. 149–150) nennt keine Klimawirkung, "
                "bei der Grenzen der Anpassung erreicht werden; er sagt nur, dass die Risiken "
                "mit weiterreichender Anpassung auf „mittel“ oder „gering-mittel“ eingegrenzt "
                "werden können (S. 150)."
            ),
            "klimawirkungen": [],
            "seiten": [149, 150],
        },
    },
    "Naturferne Wirtschaftssysteme": {
        "wirksamkeit": {
            "valide_aussage": False,
            "aussage": (
                "Keine valide Aussage laut Quelle: „Zum Anpassungspotential lässt sich bei "
                "diesem Systembereich keine Aussage treffen, da nur eine Klimawirkung "
                "(‚Beeinträchtigung der Versorgung mit Rohstoffen und Zwischenprodukten "
                "(international)‘) mit Blick auf die Wirksamkeit von Anpassungsmaßnahmen "
                "untersucht wurde“ (S. 150)."
            ),
            "anzahl_untersucht": 1,
            "seiten": [150],
        },
        "klimarisiko_mit_anpassung": {
            "valide_aussage": False,
            "aussage": (
                "Keine valide Aussage laut Quelle: Zum Anpassungspotential lässt sich keine "
                "Aussage treffen, weil nur eine Klimawirkung untersucht wurde (S. 150). "
                "Abb. 24 (S. 152) zeigt für diesen Bereich nur „Klimarisiko ohne Anpassung“."
            ),
            "seiten": [150, 152],
        },
        "anpassungsdauer": {
            "valide_aussage": True,
            "vergleich": "kürzer als in allen anderen Bereichen",
            "aussage": (
                "„Mit Blick auf die Anpassungsdauer zeichnet sich aber ein klares Bild: Kein "
                "Systembereich weist eine so kurze Anpassungsdauer auf. Bei allen "
                "Klimawirkungen werden (den Experteneinschätzungen zufolge) "
                "Anpassungsmaßnahmen in weniger als zehn Jahren wirksam“ (S. 150)."
            ),
            "seiten": [150],
        },
        "grenzen": {
            "valide_aussage": False,
            "aussage": (
                "Keine valide Aussage laut Quelle: Zum Anpassungspotential lässt sich bei "
                "diesem Systembereich keine Aussage treffen (S. 150). Der Abschnitt "
                "(S. 150) nennt keine Klimawirkung, bei der Grenzen der Anpassung erreicht "
                "werden."
            ),
            "klimawirkungen": [],
            "seiten": [150],
        },
    },
    "Menschen und soziale Systeme": {
        "wirksamkeit": {
            "valide_aussage": False,
            "aussage": (
                "Keine valide Aussage laut Quelle: „Da nur bei drei Klimawirkungen die "
                "Anpassungskapazität genauer betrachtet wurde, lassen sich keine validen "
                "Aussagen zu den Anpassungsmöglichkeiten in dem gesamten Systembereich machen.“ "
                "„Offenkundig ist, dass schon viele Maßnahmen auf den Weg gebracht worden "
                "sind“ (S. 151)."
            ),
            "anzahl_untersucht": 3,
            "seiten": [151],
        },
        "klimarisiko_mit_anpassung": {
            "valide_aussage": False,
            "aussage": (
                "Keine valide Aussage für den ganzen Bereich laut Quelle (S. 151). Nur für die "
                "drei untersuchten Klimawirkungen: „Bei den drei untersuchten Klimawirkungen "
                "können auch im pessimistischem Fall Mitte des Jahrhunderts die Klimarisiken "
                "durch weiterreichende Anpassung auf mittel reduziert werden“ (S. 151)."
            ),
            "anzahl_untersucht": 3,
            "seiten": [151],
        },
        "anpassungsdauer": {
            "valide_aussage": True,
            "vergleich": "eher kurz",
            "aussage": (
                "„Auch wird die Anpassungsdauer auf eher kurz eingeschätzt (in zwei Drittel der "
                "Fälle auf unter zehn Jahre), was für die künftige Anpassung vorteilhaft ist“ "
                "(S. 151)."
            ),
            "seiten": [151],
        },
        "grenzen": {
            "valide_aussage": False,
            "aussage": (
                "Keine valide Aussage laut Quelle: Zu den Anpassungsmöglichkeiten im ganzen "
                "Bereich lassen sich keine validen Aussagen machen (S. 151). Der Abschnitt "
                "(S. 151) nennt keine Klimawirkung, bei der Grenzen der Anpassung erreicht "
                "werden."
            ),
            "klimawirkungen": [],
            "seiten": [151],
        },
    },
}


def bereiche_ohne_valide_aussage(block: str = "wirksamkeit") -> list[str]:
    """Bereiche, für die die Quelle zu ``block`` keine valide Aussage trifft."""
    return [b for b, eintrag in BEREICHSVERGLEICH_ANPASSUNG.items() if not eintrag[block]["valide_aussage"]]
