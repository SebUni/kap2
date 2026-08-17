import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'

interface RankRow { ags: string; name: string; bundesland: string | null; index: number; outcome: number; unit: string; cost_eur: number }
interface Study {
  stand: string | null
  gemeinde_count: number
  risks: { code: string; name: string; unit: string }[]
  rankings: Record<string, RankRow[]>
  bundesland_means: Record<string, Record<string, number>>
  headline_facts: string[]
}

export default function StudyPage() {
  const [study, setStudy] = useState<Study | null>(null)
  const [risk, setRisk] = useState<string | null>(null)
  const [error, setError] = useState(false)

  useEffect(() => {
    fetch('/api/public/lite/studie')
      .then((r) => (r.ok ? r.json() : Promise.reject()))
      .then((d: Study) => { setStudy(d); setRisk(d.risks[0]?.code ?? null) })
      .catch(() => setError(true))
  }, [])

  if (error) {
    return (
      <div className="landing-section" style={{ textAlign: 'center' }}>
        <h2>KAP2-Deutschlandstudie</h2>
        <p style={{ color: 'var(--text-muted)' }}>Die Studie wird gerade erstellt und erscheint in Kürze.</p>
        <Link to="/deutschland" className="btn-primary" style={{ display: 'inline-block', marginTop: '1rem' }}>Zur Deutschland-Karte →</Link>
      </div>
    )
  }
  if (!study || !risk) {
    return <div className="landing-section">Lädt …</div>
  }

  const ranking = study.rankings[risk] ?? []
  const blMeans = study.bundesland_means[risk] ?? {}
  const sortedBl = Object.entries(blMeans).sort((a, b) => b[1] - a[1])

  return (
    <div className="landing">
      <section className="landing-section">
        <h1>KAP2-Deutschlandstudie {study.stand ? new Date(study.stand).getFullYear() || '' : ''}</h1>
        <p className="landing-section-intro">
          {study.gemeinde_count.toLocaleString('de-DE')} Gemeinden · 8 Risiken · Datengrundlage DWD,
          Zensus 2022, INKAR. Grobschätzung je Gemeinde.
        </p>
        <div className="study-links">
          <a className="btn-primary" href="/api/public/lite/studie.csv">CSV herunterladen</a>
          <Link to="/deutschland" className="cta-contact">Interaktive Karte →</Link>
          <Link to="/kontakt" className="cta-contact">Presseanfragen</Link>
        </div>

        {study.headline_facts.length > 0 && (
          <>
            <h2 style={{ marginTop: '2rem' }}>Kernergebnisse</h2>
            <ul className="study-facts">
              {study.headline_facts.map((f, i) => <li key={i}>{f}</li>)}
            </ul>
          </>
        )}
      </section>

      <section className="landing-section landing-section-alt">
        <h2>Rankings & Bundesland-Vergleich</h2>
        <div className="widget-toggle widget-toggle-wrap" role="tablist" style={{ marginBottom: '1rem' }}>
          {study.risks.map((r) => (
            <button key={r.code} className={risk === r.code ? 'active' : ''} onClick={() => setRisk(r.code)}>
              {r.name}
            </button>
          ))}
        </div>

        <div className="study-tables">
          <div>
            <h3>Top 20 Gemeinden</h3>
            <div style={{ overflowX: 'auto' }}>
              <table className="admin-table">
                <thead><tr><th>#</th><th>Gemeinde</th><th>Land</th><th>Index</th></tr></thead>
                <tbody>
                  {ranking.map((r, i) => (
                    <tr key={r.ags}>
                      <td>{i + 1}</td>
                      <td><Link to={`/deutschland?ags=${r.ags}`}>{r.name}</Link></td>
                      <td>{r.bundesland}</td>
                      <td><b>{r.index.toFixed(0)}</b></td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
          <div>
            <h3>Bundesland-Mittel</h3>
            {sortedBl.map(([bl, v]) => (
              <div key={bl} className="study-bar-row">
                <span className="study-bar-label">{bl}</span>
                <div className="study-bar"><div style={{ width: `${v}%` }} /></div>
                <span className="study-bar-val">{v.toFixed(0)}</span>
              </div>
            ))}
          </div>
        </div>
        <p className="muted" style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: '1.5rem' }}>
          Methodik & Grenzen: Grobschätzung auf Gemeindeebene (p5–p95-Normierung je Risiko),
          keine centgenaue Prognose. Räumlich genaue Analyse auf dem 100m-Raster im KAP2-Hauptprodukt.
        </p>
      </section>
    </div>
  )
}
