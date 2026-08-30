/**
 * Öffentliche Roadmap — statischer Inhalt, bewusst dupliziert zur internen
 * Quelle docs/ROADMAP.md (§Stufen) bzw. docs/ROADMAP_PUBLIC.html. Änderungen
 * an Stufen/Zieldaten IMMER zuerst dort pflegen, dann hier nachziehen.
 * Die Stage-Nummern entsprechen catalog.STAGE_LABELS im Backend.
 */

export interface RoadmapStage {
  when: string
  title: string
  text: string
  /** Cluster-Farbe des Timeline-Punkts. */
  color: string
  /** Überschrift der Risikoliste, z. B. „3 Klimarisiken". */
  risksLabel?: string
  risks?: string[]
}

export const CLUSTER_CHIPS = [
  { label: 'Land', color: '#22c55e' },
  { label: 'Wasser', color: '#3b82f6' },
  { label: 'Infrastruktur', color: '#8b5cf6' },
  { label: 'Wirtschaft', color: '#f59e0b' },
  { label: 'Menschliche Gesundheit', color: '#ef4444' },
]

/** Aktuelle RKI-Schätzung hitzebedingter Sterbefälle 2026 (vorläufig, Stand KW 32). */
export const HITZETOTE_2026 = 'rund 14.000'

export const ROADMAP_STAGES: RoadmapStage[] = [
  {
    when: 'Sommer 2026 · kostenlos & offen',
    title: 'Start: Menschliche Gesundheit — die drei sehr dringenden Klimawirkungen',
    color: '#ef4444',
    text:
      '„Hitzebelastung" ist die einzige Klimawirkung, die der Bund schon für die Gegenwart mit hohem Risiko ' +
      'bewertet — ausgewiesen mit erwarteter Mortalität, Erkrankungslast und Schäden in Euro. Gemeinsam mit den ' +
      'beiden weiteren sehr dringenden Gesundheits-Klimawirkungen stellen wir sie für jede deutsche Kommune offen ' +
      'und kostenlos bereit — mit Hitzeaktionsplänen, Schutzprogrammen für vulnerable Gruppen, allergenarmer ' +
      'Stadtbaumwahl und UV-Schutz im öffentlichen Raum als direkt umsetzbaren Maßnahmen.',
    risksLabel: '3 Klimarisiken',
    risks: [
      'Hitzebelastung',
      'Allergische Reaktionen durch Aeroallergene pflanzlicher Herkunft',
      'UV-bedingte Gesundheitsschädigungen (insbesondere Hautkrebs)',
    ],
  },
  {
    when: 'Herbst 2026 · kostenlos & offen',
    title: 'Die sehr dringenden Klimawirkungen — Stadt, Wasser, Land',
    color: '#22c55e',
    text:
      'In schnellen Ausbaustufen folgen 15 weitere „sehr dringende" Klimawirkungen aus Stadt & Gebäuden, ' +
      'Wasser & Entwässerung sowie Landwirtschaft & Boden — jeweils mit passenden Maßnahmen von ' +
      'Deichverstärkung über Schwammstadt bis Erosionsschutz.',
    risksLabel: '+15 Klimarisiken',
    risks: [
      'Stadtklima / Wärmeinseln', 'Innenraumklima', 'Vegetation in Siedlungen',
      'Schäden an Gebäuden aufgrund von Flusshochwasser', 'Belastung oder Versagen von Hochwasserschutzsystemen',
      'Sturzfluten', 'Überlastung der Entwässerungseinrichtungen in überflutungsgefährdeten Gebieten',
      'Grundwasserstand und Grundwasserqualität', 'Gewässertemperatur und biologische Wasserqualität',
      'Wassermangel im Boden', 'Produktionsfunktionen', 'Abiotischer Stress (Pflanzen)', 'Ertragsausfälle',
      'Bodenerosion durch Wasser', 'Bodenerosion durch Wind',
    ],
  },
  {
    when: 'Spätherbst 2026 · Early Access',
    title: 'Alle 31 sehr dringenden Klimawirkungen komplett — Early-Access-Programm',
    color: '#3b82f6',
    text:
      'Mit Wald, Natur, Küste und Wasserstraßen ist der komplette „sehr dringend"-Block des Bundes abgedeckt. ' +
      'KAP2 wird zum Early-Access-Programm: persönliche Freischaltung, direkter Draht zum Entwicklungsteam, enge ' +
      'Feedback-Partnerschaft. Eine interaktive Demo steht allen offen. Küstenrisiken werden nur für ' +
      'Küstenkommunen aktiviert.',
    risksLabel: '+13 Klimarisiken',
    risks: [
      'Schäden an Wäldern', 'Hitze- und Trockenstress', 'Waldbrandrisiko',
      'Stress durch Schädlinge / Krankheiten (Wald)', 'Nutzfunktion: Holzertrag',
      'Schäden an wassergebundenen Habitaten und Feuchtgebieten', 'Verbreitung von Fischarten in Fließgewässern',
      'Ausbreitung invasiver Arten', 'Wasserqualität und Grundwasserversalzung',
      'Naturräumliche Veränderungen an Küsten',
      'Beschädigung oder Zerstörung von Siedlung und Infrastruktur an der Küste',
      'Schiffbarkeit der Binnenschifffahrtsstraßen (Niedrigwasser)',
      'Beeinträchtigung des Warenverkehrs über Wasserstraßen (Inland)',
    ],
  },
  {
    when: 'Jahreswechsel 2026/27 · Marktstart',
    title: 'Volle Produktreife — die dringenden Klimawirkungen, Teil 1',
    color: '#8b5cf6',
    text:
      'KAP2 startet kommerziell: Benutzerverwaltung und Mandantenfähigkeit, formatierter Ergebnisbericht für Rat ' +
      'und Förderantrag, faires Preismodell nach Einwohnerzahl. Für akademische Zwecke bleibt KAP2 kostenfrei; ' +
      'Early-Access-Partner werden bevorzugt übernommen. Inhaltlich folgen die als „dringend" eingestuften ' +
      'Klimawirkungen rund um Infrastruktur, Wirtschaft und Gesundheitssystem.',
    risksLabel: '+11 Klimarisiken',
    risks: [
      'Schäden/Hindernisse bei Straßen und Schienenwegen (Hochwasser)',
      'Schäden/Hindernisse bei Straßen und Schienenwegen (gravitative Massenbewegungen)',
      'Schäden an Verkehrsleitsystemen, Oberleitungen und Stromversorgungsanlagen',
      'Schäden an Gebäuden aufgrund von Starkregen',
      'Einschränkungen der Funktionsfähigkeit von Kanalnetzen und Vorflutern und Kläranlagen',
      'Chemische Wasserqualität', 'Wasserbedarf',
      'Beeinträchtigung der Versorgung mit Rohstoffen und Zwischenprodukten (international)',
      'Leistungseinbußen von Beschäftigten', 'Atembeschwerden (aufgrund von Luftverunreinigungen)',
      'Auswirkungen auf das Gesundheitssystem',
    ],
  },
  {
    when: 'Frühjahr 2027 · Vollausbau',
    title: 'Das vollständige Bild: 52 Klimarisiken',
    color: '#f59e0b',
    text:
      'Mit den verbleibenden dringenden Klimawirkungen aus Natur, Küste, Wald und Tourismus bewertet KAP2 alle ' +
      '52 kommunal relevanten Klimawirkungen, die der Bund als sehr dringend oder dringend einstuft — jede ' +
      'einzeln unter ihrem KWRA-Namen ausgewiesen, quellenbelegt, mit Maßnahmen und in Euro.',
    risksLabel: '+10 Klimarisiken',
    risks: [
      'Verlust an genetischer Vielfalt', 'Verschiebung von Arealen und Rückgang der Bestände',
      'Schäden an Küstenökosystemen', 'Ökosystemleistungen', 'Rutschungen und Muren',
      'Schäden durch Windwurf', 'Nutzfunktion: Erholung',
      'Höhere Belastung oder Versagen von Küstenschutzsystemen', 'Mangel an Bewässerungswasser',
      'Wirtschaftliche Chancen und Risiken für die Tourismuswirtschaft',
    ],
  },
  {
    when: 'Perspektive · Termin offen',
    title: 'Darüber hinaus',
    color: '#9aa4b1',
    text:
      'Klimawirkungen ohne bundesseitige Dringlichkeitseinstufung folgen bedarfsgetrieben — darunter ' +
      'Personenschäden durch Extremereignisse, Energieversorgung, Trinkwasser, Nutztiere und Aquakultur sowie ' +
      'ergänzende Themen wie psychische Gesundheit, soziale Ungleichheit und indirekte wirtschaftliche Folgen.',
  },
]
