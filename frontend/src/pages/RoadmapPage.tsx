import { Link } from 'react-router-dom'
import { CLUSTER_CHIPS, ROADMAP_STAGES } from './roadmap/roadmapData'

const BRAND = 'KAP2'

/**
 * Öffentliche Roadmap-Seite — Web-Fassung von docs/ROADMAP_PUBLIC.html.
 * Statischer Inhalt aus roadmapData.ts; Timeline-Optik über roadmap-*-Klassen
 * in index.css.
 */
export default function RoadmapPage() {
  return (
    <div className="roadmap">
      <section className="roadmap-hero">
        <h1>{BRAND} — Roadmap 2026/27</h1>
        <p className="roadmap-claim">
          Klimarisiken verstehen. In Euro. In der Reihenfolge, die der Bund vorgibt.
        </p>
        <p>
          {BRAND} verbindet die KWRA-konforme Klimarisikoanalyse des Bundes mit dem, was bisher
          fehlte: erwartete Schäden in Euro und Anpassungsmaßnahmen mit Kosten-Nutzen-Rechnung.
          Der Ausbau folgt strikt der Dringlichkeitseinstufung der Klimawirkungs- und
          Risikoanalyse des Bundes (KWRA 2021) — <b>zuerst alle 31 als „sehr dringend"
          eingestuften Klimawirkungen, dann die dringenden</b>, jede einzeln als eigenes Risiko
          ausgewiesen.
        </p>
        <div className="roadmap-chips">
          {CLUSTER_CHIPS.map((c) => (
            <span key={c.label} className="roadmap-chip" style={{ background: c.color }}>
              {c.label}
            </span>
          ))}
        </div>
      </section>

      <h2 className="roadmap-h2">Die Etappen — mit allen Klimarisiken</h2>

      {ROADMAP_STAGES.map((s) => (
        <div key={s.when} className="roadmap-stage">
          <div className="roadmap-rail">
            <div className="roadmap-dot" style={{ background: s.color }} />
            <div className="roadmap-bar" />
          </div>
          <div className="roadmap-body">
            <div className="roadmap-when">{s.when}</div>
            <h3>{s.title}</h3>
            <p>{s.text}</p>
            {s.risks && (
              <p className="roadmap-risks">
                <b>{s.risksLabel}:</b> {s.risks.join(' · ')}
              </p>
            )}
          </div>
        </div>
      ))}

      <h2 className="roadmap-h2">Warum diese Reihenfolge?</h2>
      <div className="roadmap-why">
        <p>
          Die Klimawirkungs- und Risikoanalyse des Bundes (KWRA 2021) hat 102 Klimawirkungen
          bewertet und 31 davon als „sehr dringend", 23 als „dringend" priorisiert — genau die
          Feststellung, die das Bundes-Klimaanpassungsgesetz (§&nbsp;12 KAnG) kommunalen
          Klimaanpassungskonzepten zugrunde legt. 52 dieser 54 Klimawirkungen sind kommunal
          relevant; zwei liegen außerhalb kommunaler Steuerbarkeit (marine Nahrungsnetze,
          internationaler Warentransport). {BRAND} übernimmt die Priorisierung eins zu eins:
          erst die sehr dringenden, dann die dringenden Klimawirkungen, jede einzeln
          nachvollziehbar.
        </p>
        <p>
          Die Nachrichtenlage bestätigt den Einstieg: Der Sommer 2026 hat mit einer historischen
          Hitzewelle und rund 14.000 hitzebedingten Sterbefällen (vorläufige RKI-Schätzung, Stand
          Anfang August) gezeigt, wie dringlich Hitzevorsorge ist — und die Nachfrage der Kommunen
          nach Förderung für Klimaanpassung übersteigt die verfügbaren Bundesmittel um mehr als
          das Zehnfache.
        </p>
      </div>

      <div className="roadmap-cta">
        <b>Gestalten Sie den Ausbau mit.</b> Ab Sommer 2026 steht die Gesundheits-Analyse jeder
        Kommune kostenlos offen — Ihr Feedback fließt direkt in die nächsten Ausbaustufen ein.
        Kommunen und Fachbüros, die früh dabei sein wollen, nehmen wir gern in das
        Early-Access-Programm auf. <Link to="/kontakt">Kontakt aufnehmen →</Link>
      </div>

      <p className="roadmap-foot">
        Roadmap-Stand: August 2026 · Zeitangaben sind Planungsstände und können sich ändern. ·
        Methodische Grundlage: DIN EN ISO 14091, KWRA 2021 (UBA) inkl. Dringlichkeitseinstufung
        aus Teilbericht 6, §&nbsp;12 KAnG, UBA-Empfehlungen für kommunale Klimarisikoanalysen. ·
        Zwei Klimawirkungen der Dringlichkeitslisten sind kommunal nicht steuerbar (marine
        Nahrungsnetze, internationaler Warentransport) und daher nicht enthalten.
      </p>
    </div>
  )
}
