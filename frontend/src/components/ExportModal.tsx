import { useCallback, useEffect, useRef, useState } from 'react'
import { api } from '../api/client'
import type { GeoExportJob } from '../types'

interface Props {
  kommuneId: number
  onClose: () => void
}

const EXPORT_OPTIONS = [
  { key: 'alle', label: 'Alle Daten', enabled: false },
  { key: 'dashboard', label: 'Dashboard Daten', enabled: false },
  { key: 'geodaten', label: 'Geodaten', enabled: true },
  { key: 'massnahmen', label: 'Maßnahmendaten', enabled: false },
] as const

function formatJobDate(iso: string): string {
  const d = new Date(iso)
  const date = d.toLocaleDateString('de-DE', { day: '2-digit', month: '2-digit', year: 'numeric' })
  const time = d.toLocaleTimeString('de-DE', { hour: '2-digit', minute: '2-digit' })
  return `${date} – ${time}`
}

export default function ExportModal({ kommuneId, onClose }: Props) {
  const [jobs, setJobs] = useState<GeoExportJob[]>([])
  const [loading, setLoading] = useState(false)
  const [starting, setStarting] = useState(false)
  const pollRef = useRef<ReturnType<typeof setInterval> | null>(null)

  const loadJobs = useCallback(async () => {
    const data = await api.listExports(kommuneId)
    setJobs(data as unknown as GeoExportJob[])
  }, [kommuneId])

  useEffect(() => {
    setLoading(true)
    loadJobs().catch(() => {}).finally(() => setLoading(false))
  }, [loadJobs])

  const hasRunning = jobs.some(j => j.status === 'running' || j.status === 'pending')

  useEffect(() => {
    if (!hasRunning) {
      if (pollRef.current) clearInterval(pollRef.current)
      return
    }
    pollRef.current = setInterval(() => {
      loadJobs().catch(() => {})
    }, 2000)
    return () => { if (pollRef.current) clearInterval(pollRef.current) }
  }, [hasRunning, loadJobs])

  const handleStartGeodata = async () => {
    setStarting(true)
    try {
      await api.startGeodataExport(kommuneId)
      await loadJobs()
    } catch {
      alert('Export konnte nicht gestartet werden')
    } finally {
      setStarting(false)
    }
  }

  const geodataJobs = jobs.filter(j => j.export_type === 'geodaten')

  return (
    <div className="help-overlay" onClick={onClose}>
      <div className="export-overlay-content" onClick={e => e.stopPropagation()}>
        <div className="help-overlay-header">
          <h2>Daten exportieren</h2>
          <button onClick={onClose} className="help-overlay-close">✕</button>
        </div>
        <div className="help-overlay-body">
          <div className="export-options">
            {EXPORT_OPTIONS.map(opt => (
              <button
                key={opt.key}
                className={`export-option ${opt.enabled ? 'export-option-active' : 'export-option-disabled'}`}
                disabled={!opt.enabled || starting}
                onClick={opt.enabled ? handleStartGeodata : undefined}
                title={opt.enabled ? 'Geodatenpaket erstellen' : 'Noch nicht verfügbar'}
              >
                {opt.label}
              </button>
            ))}
          </div>

          <div className="export-geodaten-section">
            <h3>Geodaten</h3>
            {loading && geodataJobs.length === 0 ? (
              <p className="export-job-empty">Laden …</p>
            ) : geodataJobs.length === 0 ? (
              <p className="export-job-empty">Noch keine Geodatenpakete erstellt.</p>
            ) : (
              <ul className="export-job-list">
                {geodataJobs.map(job => (
                  <li key={job.id} className="export-job-item">
                    <span className="export-job-label">
                      Geodatenpaket – {formatJobDate(job.created_at)}
                    </span>
                    {job.status === 'running' || job.status === 'pending' ? (
                      <span className="export-job-status">In Bearbeitung</span>
                    ) : job.status === 'done' ? (
                      <a
                        href={api.exportDownloadUrl(kommuneId, job.id)}
                        download
                        className="export-job-download"
                      >
                        Herunterladen
                      </a>
                    ) : (
                      <span className="export-job-error" title={job.error_message || undefined}>
                        Fehler{job.error_message ? `: ${job.error_message}` : ''}
                      </span>
                    )}
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
