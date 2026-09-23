"""Zuständigkeit für Klimaanpassungskonzepte nach § 12 Abs. 1 KAnG je Bundesland.

Quelle ist ``docs/KANG_ZUSTAENDIGKEIT_LAENDER.md`` (Ticket T-0751, Vorhaben T-0664); dieses
Modul bildet die Tabelle dort ab. ``tests/test_kang_zustaendigkeit.py`` hält beide
deckungsgleich: bei einer Gesetzesänderung Dokument und Modul gemeinsam ändern.
Abbildung der Rechtslage, keine Rechtsauskunft.
"""

from __future__ import annotations

ZUSTAENDIGKEIT: dict[str, dict[str, str]] = {
    'Baden-Württemberg': {
        'rechtsgrundlage': '§ 29b Abs. 1 Satz 1 Nr. 1 bis 3 KlimaG BW (Klimaschutz- und Klimawandelanpassungsgesetz Baden-Württemberg, i. d. F. des Änderungsgesetzes vom 29.07.2025; Umsetzung von § 12 KAnG in §§ 29a ff.)',
        'fundstelle': 'https://www.landesrecht-bw.de/bsbw/document/jlr-KlimaSchGBW2023rahmen',
        'zustaendige_stelle': 'Stadtkreise und Große Kreisstädte für ihr Gemeindegebiet (Nr. 1); Landkreise für das Kreisgebiet (Nr. 2) und für die übrigen kreisangehörigen Gemeinden (Nr. 3); Beschluss möglichst bis 30.06.2031 (§ 29c Abs. 2 Nr. 1)',
        'pflicht': 'ja',
        'stand': '2026-09-23',
    },
    'Bayern': {
        'rechtsgrundlage': 'keine Bestimmung getroffen, Stand 2026-09-23',
        'fundstelle': 'https://www.gesetze-bayern.de/',
        'zustaendige_stelle': 'keine',
        'pflicht': 'keine Bestimmung getroffen',
        'stand': '2026-09-23',
    },
    'Berlin': {
        'rechtsgrundlage': 'keine Bestimmung getroffen, Stand 2026-09-23',
        'fundstelle': 'https://gesetze.berlin.de/',
        'zustaendige_stelle': 'keine',
        'pflicht': 'keine Bestimmung getroffen',
        'stand': '2026-09-23',
    },
    'Brandenburg': {
        'rechtsgrundlage': 'keine Bestimmung getroffen, Stand 2026-09-23',
        'fundstelle': 'https://bravors.brandenburg.de/',
        'zustaendige_stelle': 'keine',
        'pflicht': 'keine Bestimmung getroffen',
        'stand': '2026-09-23',
    },
    'Bremen': {
        'rechtsgrundlage': 'keine Bestimmung getroffen, Stand 2026-09-23',
        'fundstelle': 'https://www.transparenz.bremen.de/',
        'zustaendige_stelle': 'keine',
        'pflicht': 'keine Bestimmung getroffen',
        'stand': '2026-09-23',
    },
    'Hamburg': {
        'rechtsgrundlage': 'keine Bestimmung getroffen, Stand 2026-09-23',
        'fundstelle': 'https://www.landesrecht-hamburg.de/',
        'zustaendige_stelle': 'keine',
        'pflicht': 'keine Bestimmung getroffen',
        'stand': '2026-09-23',
    },
    'Hessen': {
        'rechtsgrundlage': 'keine Bestimmung getroffen, Stand 2026-09-23',
        'fundstelle': 'https://www.rv.hessenrecht.hessen.de/',
        'zustaendige_stelle': 'keine',
        'pflicht': 'keine Bestimmung getroffen',
        'stand': '2026-09-23',
    },
    'Mecklenburg-Vorpommern': {
        'rechtsgrundlage': 'keine Bestimmung getroffen, Stand 2026-09-23',
        'fundstelle': 'https://www.landesrecht-mv.de/',
        'zustaendige_stelle': 'keine',
        'pflicht': 'keine Bestimmung getroffen',
        'stand': '2026-09-23',
    },
    'Niedersachsen': {
        'rechtsgrundlage': '§ 26 Abs. 1 NKlimaG (Niedersächsisches Klimagesetz, Fassung gültig ab 01.01.2026)',
        'fundstelle': 'https://voris.wolterskluwer-online.de/browse/document/025ca7c9-36f3-3682-86f4-54cbfbdbca79',
        'zustaendige_stelle': 'Landkreise, kreisfreie Städte, Landeshauptstadt Hannover, Stadt Göttingen und Region Hannover (Frist 31.12.2028; Landkreise und Region je ein Konzept für ihr ganzes Gebiet)',
        'pflicht': 'ja',
        'stand': '2026-09-23',
    },
    'Nordrhein-Westfalen': {
        'rechtsgrundlage': 'keine Bestimmung getroffen, Stand 2026-09-23',
        'fundstelle': 'https://recht.nrw.de/',
        'zustaendige_stelle': 'keine',
        'pflicht': 'keine Bestimmung getroffen',
        'stand': '2026-09-23',
    },
    'Rheinland-Pfalz': {
        'rechtsgrundlage': 'keine Bestimmung getroffen, Stand 2026-09-23',
        'fundstelle': 'https://landesrecht.rlp.de/',
        'zustaendige_stelle': 'keine',
        'pflicht': 'keine Bestimmung getroffen',
        'stand': '2026-09-23',
    },
    'Saarland': {
        'rechtsgrundlage': 'keine Bestimmung getroffen, Stand 2026-09-23',
        'fundstelle': 'https://recht.saarland.de/',
        'zustaendige_stelle': 'keine',
        'pflicht': 'keine Bestimmung getroffen',
        'stand': '2026-09-23',
    },
    'Sachsen': {
        'rechtsgrundlage': 'keine Bestimmung getroffen, Stand 2026-09-23',
        'fundstelle': 'https://www.revosax.sachsen.de/',
        'zustaendige_stelle': 'keine',
        'pflicht': 'keine Bestimmung getroffen',
        'stand': '2026-09-23',
    },
    'Sachsen-Anhalt': {
        'rechtsgrundlage': '§ 1 Abs. 1 KAnG-AG LSA (Ausführungsgesetz des Landes Sachsen-Anhalt zum Bundes-Klimaanpassungsgesetz vom 15.07.2026, GVBl. LSA 2026 Nr. 15 vom 27.07.2026, S. 347; Wortlaut nach der vom Landtag angenommenen Beschlussempfehlung Drs. 8/7116, S. 3, verkündete Ausgabe selbst nicht gelesen)',
        'fundstelle': 'https://padoka.landtag.sachsen-anhalt.de/files/drs/wp8/drs/d7116vbe.pdf',
        'zustaendige_stelle': 'Landkreise und kreisfreie Städte (Vorlage des Konzepts bis 30.06.2031, § 3 Abs. 3)',
        'pflicht': 'ja',
        'stand': '2026-09-23',
    },
    'Schleswig-Holstein': {
        'rechtsgrundlage': '§ 33 Abs. 1 EWKG (Energiewende- und Klimaschutzgesetz Schleswig-Holstein, eingefügt durch Art. 1 Nr. 39 des Gesetzes vom 25.03.2025, GVOBl. Schl.-H. 2025/26 vom 28.03.2025, S. 39)',
        'fundstelle': 'https://verkuendungsportal.schleswig-holstein.de/home/gvobl/veroeffentlichungen/2025/2025_maerz/2025-26_maerz28',
        'zustaendige_stelle': 'Kreise und kreisfreie Städte (erstmals bis 30.06.2029); Gemeinden unter 100.000 Einwohnern ohne eigene Pflicht, wenn ein Kreiskonzept erstellt wird',
        'pflicht': 'ja',
        'stand': '2026-09-23',
    },
    'Thüringen': {
        'rechtsgrundlage': 'keine Bestimmung getroffen, Stand 2026-09-23',
        'fundstelle': 'https://landesrecht.thueringen.de/',
        'zustaendige_stelle': 'keine',
        'pflicht': 'keine Bestimmung getroffen',
        'stand': '2026-09-23',
    },
}

UNBEKANNT = "unbekannt"


def zustaendigkeit_fuer(bundesland: str | None) -> dict[str, str]:
    """Zuständigkeit für ein Land; ohne bekanntes Land ist ``pflicht`` ``unbekannt``."""
    eintrag = ZUSTAENDIGKEIT.get(bundesland) if bundesland else None
    if eintrag is None:
        return {
            "bundesland": bundesland or "",
            "rechtsgrundlage": "",
            "fundstelle": "",
            "zustaendige_stelle": "",
            "pflicht": UNBEKANNT,
            "stand": "",
        }
    return {"bundesland": bundesland, **eintrag}
