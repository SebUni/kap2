import { useState } from 'react'

interface Props {
  step: string
  question: string
  painpoint: React.ReactNode
  bullets: { title: string; text: string }[]
  widget: React.ReactNode
  /** Desktop: Widget links (false) oder rechts (true) — alternierend. */
  reverse?: boolean
}

/**
 * Ein Arbeitsschritt der Widget-Strecke, als Grid aus drei Blöcken:
 * `.step-head` (Kicker + Frage + Painpoint), `.step-widget-col` (Widget) und
 * `.step-benefits` (Nutzen-Bullets). Desktop zweispaltig (alternierend); mobil
 * einspaltig in der Reihenfolge Überschrift → Widget → Vorteile (so kommt die
 * Überschrift immer vor dem Widget). Bullets ab dem vierten hinter „alle
 * anzeigen" (mobil eingeklappt).
 */
export default function StepSection({ step, question, painpoint, bullets, widget, reverse = false }: Props) {
  const [expanded, setExpanded] = useState(false)

  return (
    <section className={`step-section${reverse ? ' step-reverse' : ''}`}>
      <div className="step-head">
        <div className="step-kicker">{step}</div>
        <h3 className="step-question">{question}</h3>
        <p className="step-painpoint">{painpoint}</p>
      </div>
      <div className="step-widget-col">{widget}</div>
      <div className="step-benefits">
        <ul className={`step-bullets${expanded ? ' expanded' : ''}`}>
          {bullets.map((b, i) => (
            <li key={i} className={i >= 3 && !expanded ? 'bullet-collapsed' : ''}>
              <strong>{b.title}</strong> {b.text}
            </li>
          ))}
        </ul>
        {bullets.length > 3 && (
          <button className="bullets-toggle" onClick={() => setExpanded((e) => !e)}>
            {expanded ? 'Weniger anzeigen' : `Alle ${bullets.length} Vorteile anzeigen`}
          </button>
        )}
      </div>
    </section>
  )
}
