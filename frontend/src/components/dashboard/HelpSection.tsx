import { useState, type ReactNode } from 'react'

interface SectionData {
  title: string
  content: ReactNode
}

export default function HelpSection() {
  const [expandedIdx, setExpandedIdx] = useState<number | null>(null)

  const toggle = (i: number) => setExpandedIdx(expandedIdx === i ? null : i)

  const sections: SectionData[] = [
    {
      title: '1. Berechnungsübersicht – Methodik',
      content: (
        <div className="help-content">
          <p>
            KAP2 bewertet Klimarisiken auf Basis eines <strong>100m × 100m Rasters</strong>, das über das
            gesamte Gemeindegebiet gelegt wird. Jede Rasterzelle wird anhand von OpenStreetMap-Daten,
            DWD-Klimadaten und regionalen Statistiken bewertet.
          </p>
          <h4>Bewertungsebenen (Level)</h4>
          <table className="help-table">
            <thead>
              <tr><th>Level</th><th>Bezeichnung</th><th>Beschreibung</th></tr>
            </thead>
            <tbody>
              <tr><td>1</td><td>Grundbewertung</td><td>Lokale Indikatoren aus OSM-Flächennutzung (Versiegelung, Grünflächen, Gewässer, Gebäude)</td></tr>
              <tr><td>2</td><td>Regionale Skalierung</td><td>Level 1 × regionaler Klimafaktor (DWD-Station)</td></tr>
              <tr><td>3</td><td>Sozioökonomisch</td><td>Integration von Bevölkerungsdichte und Infrastrukturindikatoren</td></tr>
              <tr><td>4</td><td>Vulnerabilitätsbewertung</td><td>Altersstruktur, soziale Einrichtungen, Vulnerabilitätsindex</td></tr>
            </tbody>
          </table>
          <h4>Pipeline-Schritte</h4>
          <ol>
            <li><strong>Grid-Generierung</strong>: 100m-Raster über Gemeindegeometrie (PostGIS)</li>
            <li><strong>OSM-Feature-Extraktion</strong>: Für jede Zelle werden Flächenanteile berechnet (imperviousness, green_fraction, water_fraction, building_fraction)</li>
            <li><strong>Indikator-Berechnung</strong>: Gewichtete Kombination der Features zu einem Risk Score (0–10)</li>
            <li><strong>Risikozonen</strong>: BFS Connected-Component-Algorithmus (8-Nachbarschaft, Schwellenwert ≥ 0.3)</li>
            <li><strong>Projektion</strong>: Skalierung mit IPCC AR6 / DWD KlimaFolgenOnline-Faktoren</li>
          </ol>
        </div>
      ),
    },
    {
      title: '2. Hitze (Heat)',
      content: (
        <div className="help-content">
          <p>Bewertet die städtische Wärmeinsel (UHI – Urban Heat Island) und Hitzestress.</p>
          <h4>Indikatoren</h4>
          <ul>
            <li><strong>imperviousness</strong>: Versiegelungsgrad (0–1)</li>
            <li><strong>green_fraction</strong>: Grünflächenanteil (0–1)</li>
            <li><strong>water_fraction</strong>: Gewässeranteil (0–1)</li>
            <li><strong>building_fraction</strong>: Gebäudeanteil (0–1)</li>
            <li><strong>albedo</strong>: Albedo-Schätzung (0.1–0.4)</li>
          </ul>
          <h4>Formel (Level 1)</h4>
          <div className="formula-block">
            <code>UHI_delta = α × (1 - albedo) × imperv + β × building - γ × green - δ × water</code>
          </div>
          <p>mit α = 5.0, β = 2.0, γ = 3.0, δ = 2.5</p>
          <div className="formula-block">
            <code>heat_stress = min(10, UHI_delta × 1.5)</code>
          </div>
          <div className="formula-block">
            <code>risk_score = heat_stress / 10</code>
          </div>
          <h4>Level 2 – Regionale Skalierung</h4>
          <div className="formula-block">
            <code>risk_score_L2 = risk_score_L1 × (hot_days_per_year / 12.5)</code>
          </div>
          <p>Referenzwert: 12.5 Heiße Tage/Jahr (DWD Mittel 1991–2020).</p>
          <h4>Level 4 – Vulnerabilität</h4>
          <div className="formula-block">
            <code>vulnerability_index = 0.3 × elderly_frac + 0.3 × pop_density_norm + 0.2 × healthcare_prox + 0.2 × social_infra</code>
          </div>
          <div className="formula-block">
            <code>risk_score_L4 = risk_score_L2 × (1 + 0.5 × vulnerability_index)</code>
          </div>
          <h4>Projektionsfaktoren</h4>
          <table className="help-table">
            <thead><tr><th>Szenario</th><th>Änderung bis 2050</th></tr></thead>
            <tbody>
              <tr><td>RCP 4.5</td><td>+30%</td></tr>
              <tr><td>RCP 8.5</td><td>+85%</td></tr>
            </tbody>
          </table>
          <p className="help-source">Quellen: DWD CDC, IPCC AR6 WG2 Ch. 12, UBA KlimaFolgenOnline</p>
        </div>
      ),
    },
    {
      title: '3. Starkregen (Heavy Rain)',
      content: (
        <div className="help-content">
          <p>Bewertet die Anfälligkeit gegenüber Starkregen anhand von Versiegelung, Entwässerung und Topographie.</p>
          <h4>Formel (Level 1)</h4>
          <div className="formula-block">
            <code>risk_score = 0.5 × imperviousness + 0.3 × drainage_deficit + 0.2 × topographic_exposure</code>
          </div>
          <ul>
            <li><strong>drainage_deficit</strong>: 1 − green_fraction − water_fraction (Entwässerungskapazität)</li>
            <li><strong>topographic_exposure</strong>: Geschätzter Höhenstatus (Senken stärker betroffen)</li>
          </ul>
          <h4>Level 2 – Regionale Skalierung</h4>
          <div className="formula-block">
            <code>risk_score_L2 = risk_score_L1 × (heavy_rain_days / 6.5)</code>
          </div>
          <h4>Projektionsfaktoren</h4>
          <table className="help-table">
            <thead><tr><th>Szenario</th><th>Änderung bis 2050</th></tr></thead>
            <tbody>
              <tr><td>RCP 4.5</td><td>+25%</td></tr>
              <tr><td>RCP 8.5</td><td>+70%</td></tr>
            </tbody>
          </table>
          <p className="help-source">Quellen: DWD RADKLIM, KOSTRA-DWD-2020, UBA 2023</p>
        </div>
      ),
    },
    {
      title: '4. Hochwasser (River Flood)',
      content: (
        <div className="help-content">
          <p>Bewertet Hochwassergefährdung durch Flussnähe, Geländehöhe und Bebauung.</p>
          <h4>Formel (Level 1)</h4>
          <div className="formula-block">
            <code>risk_score = 0.5 × proximity_to_river + 0.3 × elevation_exposure + 0.2 × building_density</code>
          </div>
          <h4>Level 2</h4>
          <div className="formula-block">
            <code>risk_score_L2 = risk_score_L1 × flood_frequency_factor</code>
          </div>
          <h4>Projektionsfaktoren</h4>
          <table className="help-table">
            <thead><tr><th>Szenario</th><th>Änderung bis 2050</th></tr></thead>
            <tbody>
              <tr><td>RCP 4.5</td><td>+20%</td></tr>
              <tr><td>RCP 8.5</td><td>+60%</td></tr>
            </tbody>
          </table>
          <p className="help-source">Quellen: BfG, LAWA, HQ-Statistik</p>
        </div>
      ),
    },
    {
      title: '5. Dürre (Drought)',
      content: (
        <div className="help-content">
          <p>Bewertet Trockenheitsanfälligkeit durch Versiegelung, Grünflächendefizite und Gewässerentfernung.</p>
          <h4>Formel (Level 1)</h4>
          <div className="formula-block">
            <code>risk_score = 0.3 × sealed_fraction + 0.4 × green_deficit + 0.3 × water_distance</code>
          </div>
          <h4>Level 2</h4>
          <div className="formula-block">
            <code>risk_score_L2 = risk_score_L1 × drought_factor</code>
          </div>
          <h4>Projektionsfaktoren</h4>
          <table className="help-table">
            <thead><tr><th>Szenario</th><th>Änderung bis 2050</th></tr></thead>
            <tbody>
              <tr><td>RCP 4.5</td><td>+35%</td></tr>
              <tr><td>RCP 8.5</td><td>+90%</td></tr>
            </tbody>
          </table>
          <p className="help-source">Quellen: UFZ Dürremonitor, DWD Bodenfeuchte, UBA 2023</p>
        </div>
      ),
    },
    {
      title: '6. Waldbrand (Forest Fire)',
      content: (
        <div className="help-content">
          <p>Bewertet Waldbrandgefahr durch Waldanteil, Trockenheitsindex und Siedlungs-Wald-Grenzlinien.</p>
          <h4>Formel (Level 1)</h4>
          <div className="formula-block">
            <code>risk_score = 0.4 × forest_fraction + 0.3 × dryness_index + 0.3 × wildland_urban_interface</code>
          </div>
          <h4>Projektionsfaktoren</h4>
          <table className="help-table">
            <thead><tr><th>Szenario</th><th>Änderung bis 2050</th></tr></thead>
            <tbody>
              <tr><td>RCP 4.5</td><td>+40%</td></tr>
              <tr><td>RCP 8.5</td><td>+100%</td></tr>
            </tbody>
          </table>
          <p className="help-source">Quellen: BLE Waldbrandstatistik, Copernicus EFFIS, DWD WBI</p>
        </div>
      ),
    },
    {
      title: '7. Landwirtschaft (Agriculture)',
      content: (
        <div className="help-content">
          <p>Bewertet klimatische Gefährdung landwirtschaftlicher Flächen.</p>
          <h4>Formel (Level 1)</h4>
          <div className="formula-block">
            <code>risk_score = 0.3 × ag_fraction + 0.3 × irrigation_deficit + 0.2 × heat_exposure + 0.2 × storm_exposure</code>
          </div>
          <h4>Level 2</h4>
          <div className="formula-block">
            <code>risk_score_L2 = risk_score_L1 × frost_factor</code>
          </div>
          <h4>Projektionsfaktoren</h4>
          <table className="help-table">
            <thead><tr><th>Szenario</th><th>Änderung bis 2050</th></tr></thead>
            <tbody>
              <tr><td>RCP 4.5</td><td>+25%</td></tr>
              <tr><td>RCP 8.5</td><td>+65%</td></tr>
            </tbody>
          </table>
          <p className="help-source">Quellen: Thünen-Institut, BMEL, DWD Agrarmeteo</p>
        </div>
      ),
    },
    {
      title: '8. Stürme (Storms)',
      content: (
        <div className="help-content">
          <p>Bewertet Sturmgefährdung durch Exponiertheit, Gebäudevulnerabilität und Baumbestand.</p>
          <h4>Formel (Level 1)</h4>
          <div className="formula-block">
            <code>risk_score = 0.4 × exposure + 0.3 × building_vulnerability + 0.3 × tree_canopy</code>
          </div>
          <h4>Level 2</h4>
          <div className="formula-block">
            <code>risk_score_L2 = risk_score_L1 × storm_frequency_factor</code>
          </div>
          <h4>Projektionsfaktoren</h4>
          <table className="help-table">
            <thead><tr><th>Szenario</th><th>Änderung bis 2050</th></tr></thead>
            <tbody>
              <tr><td>RCP 4.5</td><td>+15%</td></tr>
              <tr><td>RCP 8.5</td><td>+40%</td></tr>
            </tbody>
          </table>
          <p className="help-source">Quellen: DWD, MunichRe NatCat, GDV 2023</p>
        </div>
      ),
    },
    {
      title: '9. Meeresspiegel (Sea Level)',
      content: (
        <div className="help-content">
          <p>Bewertet Überflutungsgefahr durch Meeresspiegelanstieg (nur für Küstenkommunen relevant).</p>
          <h4>Formel (Level 1)</h4>
          <div className="formula-block">
            <code>risk_score = 0.5 × coastal_proximity + 0.3 × elevation_below_threshold + 0.2 × infrastructure_density</code>
          </div>
          <p>Für Binnenland-Kommunen: risk_score = 0 (automatisch).</p>
          <h4>Level 2</h4>
          <div className="formula-block">
            <code>risk_score_L2 = risk_score_L1 × 1.15</code>
          </div>
          <h4>Projektionsfaktoren</h4>
          <table className="help-table">
            <thead><tr><th>Szenario</th><th>Änderung bis 2050</th></tr></thead>
            <tbody>
              <tr><td>RCP 4.5</td><td>+30%</td></tr>
              <tr><td>RCP 8.5</td><td>+80%</td></tr>
            </tbody>
          </table>
          <p className="help-source">Quellen: BSH, IPCC AR6 WG1 Ch. 9, DIN 19712</p>
        </div>
      ),
    },
    {
      title: '10. Risikozonen – Algorithmus',
      content: (
        <div className="help-content">
          <p>
            Zusammenhängende Gebiete hohen Risikos werden mit dem <strong>BFS (Breadth-First Search)
            Connected-Component-Algorithmus</strong> identifiziert.
          </p>
          <h4>Parameter</h4>
          <ul>
            <li><strong>Schwellenwert</strong>: risk_score ≥ 0.3 (Zellen mit niedrigerem Wert werden ignoriert)</li>
            <li><strong>Nachbarschaft</strong>: 8-connected (Moore-Nachbarschaft: vertikal, horizontal, diagonal)</li>
            <li><strong>Mindestgröße</strong>: 3 Zellen (sonst nicht als Zone klassifiziert)</li>
          </ul>
          <h4>Zonenkennwerte</h4>
          <ul>
            <li><strong>mean_risk</strong>: Durchschnittlicher Risk Score aller Zellen in der Zone</li>
            <li><strong>max_risk</strong>: Höchster Risk Score in der Zone</li>
            <li><strong>area_m2</strong>: Zonenfläche (Zellanzahl × 10.000 m²)</li>
            <li><strong>centroid</strong>: Flächenschwerpunkt der Zone</li>
          </ul>
          <h4>Aggregiertes Risiko (ARI)</h4>
          <div className="formula-block">
            <code>ARI = mean_risk × ln(1 + zone_count) × (1 + total_area_m2 / Gemeindefläche)</code>
          </div>
        </div>
      ),
    },
    {
      title: '11. Klimaprojektionen',
      content: (
        <div className="help-content">
          <p>
            Projektionen basieren auf den Representative Concentration Pathways (RCP) des IPCC AR6:
          </p>
          <ul>
            <li><strong>RCP 4.5</strong>: Moderater Emissionspfad – globale Erwärmung ~2.0°C bis 2100</li>
            <li><strong>RCP 8.5</strong>: Hochemissionspfad – globale Erwärmung ~4.5°C bis 2100</li>
          </ul>
          <h4>Methode</h4>
          <p>Jeder Assessor definiert eigene Projektionsfaktoren (% Änderung bzgl. Basisjahr).
          Die Risikozonen werden für jedes Projektionsjahr (2025–2065) neu berechnet:</p>
          <div className="formula-block">
            <code>projected_risk(year) = base_risk × (1 + factor × (year − 2025) / (2050 − 2025))</code>
          </div>
          <p>Die Schwellenwerte für Risikozonen bleiben konstant; nur die Schwere und Flächenausdehnung ändern sich.</p>
          <p className="help-source">Quellen: IPCC AR6 (2021), DWD KlimaFolgenOnline, DKRZ CMIP6</p>
        </div>
      ),
    },
    {
      title: '12. Wirkungsanalyse & Datenquellen',
      content: (
        <div className="help-content">
          <p>Die gesellschaftlichen und wirtschaftlichen Auswirkungen basieren auf publizierten Statistiken:</p>
          <table className="help-table">
            <thead><tr><th>Quelle</th><th>Daten</th></tr></thead>
            <tbody>
              <tr><td>UBA Monitoringbericht (2023)</td><td>Klimafolgenkosten, Anpassungsmaßnahmen</td></tr>
              <tr><td>GDV Naturgefahrenreport (2023)</td><td>Versicherungsschäden durch Naturgefahren</td></tr>
              <tr><td>RKI Hitzebericht (2023)</td><td>Hitzetote, Hospitalisierungen</td></tr>
              <tr><td>Thünen-Institut</td><td>Landwirtschaftliche Schäden, Ernteausfälle</td></tr>
              <tr><td>DKRZ / CMIP6</td><td>Regionalisierte Klimaprojektionen</td></tr>
              <tr><td>DWD CDC</td><td>Historische Klimadaten, Stationsdaten</td></tr>
              <tr><td>BfN</td><td>Ökosystemschäden, Biodiversitätsindizes</td></tr>
              <tr><td>IPCC AR6</td><td>Globale und regionale Projektionsfaktoren</td></tr>
            </tbody>
          </table>
          <h4>Skalierung auf Kommunalebene</h4>
          <p>Nationale Werte werden proportional auf die Gemeindefläche und -bevölkerung umgerechnet
          und mit dem berechneten Risikoindex skaliert:</p>
          <div className="formula-block">
            <code>local_impact = national_impact × (area_kommun / area_germany) × risk_scale_factor</code>
          </div>
        </div>
      ),
    },
  ]

  return (
    <div className="dashboard-section">
      <h3 className="section-title">📚 Methodik & Hilfe</h3>
      <p style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginBottom: 12, marginTop: -4 }}>
        Detaillierte Dokumentation der Berechnungsverfahren, Formeln und Datenquellen.
      </p>
      <div className="help-accordion">
        {sections.map((sec, i) => (
          <div key={i} className={`help-item ${expandedIdx === i ? 'expanded' : ''}`}>
            <button className="help-item-header" onClick={() => toggle(i)}>
              <span>{sec.title}</span>
              <span className="help-chevron">{expandedIdx === i ? '▼' : '▶'}</span>
            </button>
            {expandedIdx === i && (
              <div className="help-item-body">{sec.content}</div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}
