import { useState } from 'react'
import { Link } from 'react-router-dom'
import { useLiteStore, adjustedIndex, LITE_MEASURES } from '../../store/liteStore'
import InlineSpinner from '../../components/InlineSpinner'

function fmtNum(v: number, unit: string): string {
  const abs = Math.abs(v)
  const n = abs >= 1_000_000
    ? `${(v / 1_000_000).toLocaleString('de-DE', { maximumFractionDigits: 1 })} Mio`
    : abs >= 1000
      ? `${(v / 1000).toLocaleString('de-DE', { maximumFractionDigits: 1 })} Tsd`
      : v.toLocaleString('de-DE', { maximumFractionDigits: 1 })
  return unit.includes('€') ? `${n} €/Jahr` : `${n} ${unit}`
}

export default function LitePanel() {
  const {
    meta, selectedRisk, setRisk, gemeindeDetail, detailLoading,
    measureLevels, setMeasureLevel, resetMeasures, error,
  } = useLiteStore()
  const [openMech, setOpenMech] = useState(false)

  if (error) {
    return (
      <div className="lite-panel">
        <div className="lite-panel-empty">
          <p>Die Deutschland-Karte ist noch nicht berechnet.</p>
          <Link to="/kontakt" className="cta-contact">Beratungsgespräch vereinbaren →</Link>
        </div>
      </div>
    )
  }
  if (!meta) {
    return <div className="lite-panel"><div className="lite-panel-empty"><InlineSpinner /> Lädt …</div></div>
  }

  // Risiken nach Gruppe ordnen
  const groups: Record<string, typeof meta.risks> = {}
  for (const r of meta.risks) (groups[r.group ?? 'sonstige'] ??= []).push(r)
  const groupLabel: Record<string, string> = {
    heat: 'Hitze', flood: 'Hochwasser & Starkregen', drought: 'Trockenheit',
    compound: 'Verbund', gradual: 'Gradueller Wandel', sonstige: 'Weitere',
  }

  const detailRisk = gemeindeDetail?.risks.find((r) => r.code === selectedRisk)
  const baseIndex = detailRisk?.index ?? 0
  const adjIndex = detailRisk ? adjustedIndex(baseIndex, selectedRisk!, measureLevels) : 0
  const anyMeasure = Object.values(measureLevels).some((v) => v > 0)

  return (
    <div className="lite-panel">
      <div className="lite-panel-head">
        <h2>Deutschland-Karte</h2>
        <p>Kostenlose Grobschätzung je Gemeinde ({meta.gemeinde_count.toLocaleString('de-DE')} Gemeinden).</p>
      </div>

      <div className="lite-section">
        <h3>Risiko wählen</h3>
        {Object.entries(groups).map(([g, risks]) => (
          <div key={g} className="lite-risk-group">
            <div className="lite-risk-grouplabel">{groupLabel[g] ?? g}</div>
            {risks.map((r) => (
              <label key={r.code} className={`lite-risk-item${selectedRisk === r.code ? ' active' : ''}`}>
                <input type="radio" name="lite-risk" checked={selectedRisk === r.code}
                  onChange={() => setRisk(r.code)} />
                <span>{r.name}</span>
              </label>
            ))}
          </div>
        ))}
      </div>

      <div className="lite-legend">
        <span>gering</span>
        {meta.choropleth_colors.map((c) => <i key={c} style={{ background: c }} />)}
        <span>hoch</span>
      </div>

      {gemeindeDetail && (
        <div className="lite-section lite-detail">
          <h3>{gemeindeDetail.name}</h3>
          <p className="lite-detail-sub">
            {gemeindeDetail.population?.toLocaleString('de-DE')} EW ·
            {' '}{gemeindeDetail.area_km2?.toFixed(0)} km² · {gemeindeDetail.bundesland}
          </p>
          {detailLoading ? <InlineSpinner /> : detailRisk && (
            <div className="lite-risk-card">
              <div className="lite-risk-name">{detailRisk.name}</div>
              <div className="lite-index-bar">
                <div className="lite-index-fill" style={{ width: `${adjIndex}%` }} />
                <span className="lite-index-num">{Math.round(adjIndex)}</span>
              </div>
              <div className="lite-outcome">
                ≈ {fmtNum(detailRisk.outcome * (adjIndex / (baseIndex || 1)), detailRisk.unit)}
                {detailRisk.cost_eur > 0 && !detailRisk.unit.includes('€') &&
                  <> · ≈ {fmtNum(detailRisk.cost_eur * (adjIndex / (baseIndex || 1)), '€')}</>}
              </div>
              {anyMeasure && (
                <div className="lite-adjusted-note">
                  Basis {Math.round(baseIndex)} → mit Maßnahmen {Math.round(adjIndex)}
                </div>
              )}
              <button className="lite-mech-toggle" onClick={() => setOpenMech((o) => !o)}>
                {openMech ? '▾' : '▸'} Wirkungsmechanismus & Quellen
              </button>
              {openMech && (
                <div className="lite-mech">
                  <div className="lite-drivers">
                    {Object.entries(detailRisk.drivers).map(([k, v]) => (
                      <span key={k}><b>{k}:</b> {String(v)}</span>
                    ))}
                  </div>
                  <div className="lite-sources">
                    {detailRisk.sources.map((s) => (
                      <a key={s.key} href={s.url} target="_blank" rel="noreferrer" title={s.ieee}>
                        {s.key} ↗
                      </a>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      )}

      <div className="lite-section">
        <h3>Maßnahmen ausprobieren</h3>
        <p className="lite-measures-hint">Vereinfachte Abschätzung — reagiert live auf die Karte.</p>
        {LITE_MEASURES.map((m) => (
          <div key={m.code} className="lite-measure">
            <div className="lite-measure-row">
              <span>{m.name}</span>
              <span className="lite-measure-val">{Math.round((measureLevels[m.code] ?? 0) * 100)} %</span>
            </div>
            <input type="range" min={0} max={1} step={0.05}
              value={measureLevels[m.code] ?? 0}
              onChange={(e) => setMeasureLevel(m.code, Number(e.target.value))} />
          </div>
        ))}
        {anyMeasure && <button className="game-reset" onClick={resetMeasures}>↺ Zurücksetzen</button>}
      </div>

      <div className="lite-cta">
        <p>⚠ Grobschätzung auf Gemeindeebene. Detailanalyse auf dem 100m-Raster in der Demo bzw. Vollversion.</p>
        <div className="cta-pair cta-pair-left">
          <Link to="/demo" className="btn-primary">Demo ansehen</Link>
          <Link to="/kontakt" className="cta-contact">Beratungsgespräch →</Link>
        </div>
      </div>
    </div>
  )
}
