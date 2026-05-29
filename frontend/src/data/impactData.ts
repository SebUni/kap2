/**
 * Impact reference data per climate type for Germany.
 * Sources: UBA Monitoringbericht 2023, GDV Naturgefahrenreport 2023,
 * RKI Hitzebericht 2023, DKRZ, Thünen-Institut, BfN
 *
 * Werte beziehen sich auf Deutschland gesamt (jährlich), werden in der
 * Anwendung auf kommunale Fläche/Bevölkerung heruntergerechnet.
 */

export interface ImpactCategory {
  label: string
  unit: string
  icon: string
  current: number       // IST – aktueller jährlicher Wert (national)
  projected45: number   // Ohne Maßnahmen 2050 (RCP 4.5)
  projected85: number   // Ohne Maßnahmen 2050 (RCP 8.5)
  mitigated: number     // Mit Maßnahmen (nach Umsetzung) – national
  source: string
  perCapita?: boolean   // true = pro 100.000 Einwohner, false = national total
}

export interface ClimateImpactData {
  label: string
  summary: string
  categories: ImpactCategory[]
}

/** Germany total reference data – area: 357,588 km², population: 84.4M */
export const GERMANY_AREA_KM2 = 357_588
export const GERMANY_POPULATION = 84_400_000

export const IMPACT_DATA: Record<string, ClimateImpactData> = {
  heat: {
    label: 'Hitze',
    summary: 'Hitzebedingte Gesundheits- und Produktivitätsverluste stellen die größte direkte Belastung dar.',
    categories: [
      {
        label: 'Hitzetote',
        unit: 'pro 100k EW/Jahr',
        icon: '💀',
        current: 9.5,       // ~8.000 Hitzetote/84.4M × 100k ≈ 9.5
        projected45: 14.2,
        projected85: 21.3,
        mitigated: 7.1,
        source: 'RKI Hitzebericht 2023',
        perCapita: true,
      },
      {
        label: 'Krankenhauseinweisungen',
        unit: 'pro 100k EW/Jahr',
        icon: '🏥',
        current: 45,
        projected45: 67,
        projected85: 95,
        mitigated: 30,
        source: 'RKI 2023',
        perCapita: true,
      },
      {
        label: 'Arbeitsproduktivitätsverlust',
        unit: 'Mrd. €/Jahr',
        icon: '📉',
        current: 6.5,
        projected45: 10.2,
        projected85: 16.8,
        mitigated: 4.2,
        source: 'UBA Monitoringbericht 2023',
      },
      {
        label: 'Kühlenergiebedarf',
        unit: 'Mrd. €/Jahr',
        icon: '❄️',
        current: 2.8,
        projected45: 4.5,
        projected85: 7.2,
        mitigated: 2.1,
        source: 'Fraunhofer ISE 2022',
      },
    ],
  },
  heavy_rain: {
    label: 'Starkregen',
    summary: 'Zunehmende Starkregenereignisse verursachen wachsende Gebäude- und Infrastrukturschäden.',
    categories: [
      {
        label: 'Gebäudeschäden',
        unit: 'Mrd. €/Jahr',
        icon: '🏚️',
        current: 2.9,
        projected45: 4.3,
        projected85: 6.8,
        mitigated: 1.8,
        source: 'GDV Naturgefahrenreport 2023',
      },
      {
        label: 'Infrastrukturkosten',
        unit: 'Mrd. €/Jahr',
        icon: '🛣️',
        current: 1.2,
        projected45: 1.9,
        projected85: 3.1,
        mitigated: 0.8,
        source: 'UBA 2023',
      },
      {
        label: 'Versicherungsschäden',
        unit: 'Mrd. €/Jahr',
        icon: '📋',
        current: 1.8,
        projected45: 2.7,
        projected85: 4.2,
        mitigated: 1.2,
        source: 'GDV 2023',
      },
    ],
  },
  river_flood: {
    label: 'Hochwasser',
    summary: 'Flusshochwasser verursacht die höchsten Einzelschadensereignisse in Deutschland.',
    categories: [
      {
        label: 'Überflutungsschäden',
        unit: 'Mrd. €/Jahr',
        icon: '🌊',
        current: 3.5,
        projected45: 5.2,
        projected85: 8.4,
        mitigated: 2.1,
        source: 'GDV 2023, Ahrtal-Analyse',
      },
      {
        label: 'Evakuierungskosten',
        unit: 'Mio. €/Jahr',
        icon: '🚨',
        current: 180,
        projected45: 270,
        projected85: 430,
        mitigated: 120,
        source: 'BBK 2023',
      },
      {
        label: 'Landwirtschaftsverluste',
        unit: 'Mio. €/Jahr',
        icon: '🌾',
        current: 340,
        projected45: 510,
        projected85: 820,
        mitigated: 220,
        source: 'Thünen-Institut 2022',
      },
    ],
  },
  drought: {
    label: 'Dürre',
    summary: 'Anhaltende Dürreperioden gefährden Wasserversorgung, Forst- und Landwirtschaft.',
    categories: [
      {
        label: 'Ernteausfälle',
        unit: 'Mrd. €/Jahr',
        icon: '🌾',
        current: 1.4,
        projected45: 2.5,
        projected85: 4.8,
        mitigated: 0.9,
        source: 'Thünen-Institut 2023',
      },
      {
        label: 'Wasserversorgungskosten',
        unit: 'Mrd. €/Jahr',
        icon: '💧',
        current: 0.8,
        projected45: 1.4,
        projected85: 2.5,
        mitigated: 0.5,
        source: 'BDEW 2023',
      },
      {
        label: 'Waldschäden',
        unit: 'Mrd. €/Jahr',
        icon: '🌲',
        current: 2.1,
        projected45: 3.6,
        projected85: 6.2,
        mitigated: 1.4,
        source: 'BMEL Waldzustandsbericht 2023',
      },
    ],
  },
  forest_fire: {
    label: 'Waldbrand',
    summary: 'Steigende Waldbrandgefahr durch längere Trockenperioden und höhere Temperaturen.',
    categories: [
      {
        label: 'Löschkosten',
        unit: 'Mio. €/Jahr',
        icon: '🚒',
        current: 85,
        projected45: 145,
        projected85: 260,
        mitigated: 55,
        source: 'BLE 2023',
      },
      {
        label: 'Holzwirtschaftsverluste',
        unit: 'Mio. €/Jahr',
        icon: '🪵',
        current: 120,
        projected45: 210,
        projected85: 380,
        mitigated: 75,
        source: 'Thünen-Institut 2022',
      },
      {
        label: 'Ökosystemschäden',
        unit: 'Mio. €/Jahr',
        icon: '🦎',
        current: 200,
        projected45: 350,
        projected85: 620,
        mitigated: 130,
        source: 'BfN 2023',
      },
    ],
  },
  agriculture: {
    label: 'Landwirtschaft',
    summary: 'Landwirtschaftliche Klimaauswirkungen durch Hitze, Frost, Dürre und Extremwetter.',
    categories: [
      {
        label: 'Ertragseinbußen',
        unit: 'Mrd. €/Jahr',
        icon: '🌾',
        current: 2.3,
        projected45: 3.8,
        projected85: 6.5,
        mitigated: 1.5,
        source: 'Thünen-Institut 2023',
      },
      {
        label: 'Bewässerungskosten',
        unit: 'Mrd. €/Jahr',
        icon: '💧',
        current: 0.6,
        projected45: 1.1,
        projected85: 2.0,
        mitigated: 0.4,
        source: 'BMEL 2023',
      },
      {
        label: 'Tierhaltungsschäden',
        unit: 'Mio. €/Jahr',
        icon: '🐄',
        current: 450,
        projected45: 720,
        projected85: 1200,
        mitigated: 300,
        source: 'KTBL 2022',
      },
    ],
  },
  storms: {
    label: 'Stürme',
    summary: 'Starkwinde und Orkane verursachen erhebliche Sachschäden und Netzausfälle.',
    categories: [
      {
        label: 'Gebäudeschäden',
        unit: 'Mrd. €/Jahr',
        icon: '🏚️',
        current: 3.2,
        projected45: 4.1,
        projected85: 5.6,
        mitigated: 2.4,
        source: 'GDV 2023',
      },
      {
        label: 'Stromausfallkosten',
        unit: 'Mrd. €/Jahr',
        icon: '⚡',
        current: 0.9,
        projected45: 1.2,
        projected85: 1.7,
        mitigated: 0.6,
        source: 'BNetzA 2023',
      },
      {
        label: 'Baumschäden/Forstwirtschaft',
        unit: 'Mrd. €/Jahr',
        icon: '🌲',
        current: 1.5,
        projected45: 1.9,
        projected85: 2.6,
        mitigated: 1.0,
        source: 'BMEL 2023',
      },
    ],
  },
  sea_level: {
    label: 'Meeresspiegel',
    summary: 'Steigende Meeresspiegel bedrohen Küstengebiete, Häfen und Infrastruktur.',
    categories: [
      {
        label: 'Küstenschutzkosten',
        unit: 'Mrd. €/Jahr',
        icon: '🏗️',
        current: 0.6,
        projected45: 1.2,
        projected85: 2.8,
        mitigated: 0.4,
        source: 'BMWK 2023',
      },
      {
        label: 'Landverlust (Wert)',
        unit: 'Mrd. €/Jahr',
        icon: '🗺️',
        current: 0.1,
        projected45: 0.4,
        projected85: 1.2,
        mitigated: 0.05,
        source: 'UBA 2023',
      },
      {
        label: 'Infrastrukturschäden',
        unit: 'Mrd. €/Jahr',
        icon: '🛣️',
        current: 0.3,
        projected45: 0.7,
        projected85: 1.8,
        mitigated: 0.2,
        source: 'DKRZ 2022',
      },
    ],
  },
}
