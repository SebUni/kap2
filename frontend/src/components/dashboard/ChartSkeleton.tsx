import InlineSpinner from '../InlineSpinner'

/** Lade-Platzhalter in exakt der Endhöhe der Ziel-Box (kein Layout-Sprung). */
export default function ChartSkeleton({ height, label }: { height: number | string; label?: string }) {
  return (
    <div className="chart-skeleton" style={{ height }} role="status" aria-live="polite">
      <InlineSpinner size={14} />
      {label ?? 'Wird geladen …'}
    </div>
  )
}
