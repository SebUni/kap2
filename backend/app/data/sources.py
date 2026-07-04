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
