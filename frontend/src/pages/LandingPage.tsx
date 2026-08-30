import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import CtaPair from '../components/CtaPair'
import StepSection from './landing/StepSection'
import RadarWidget from './landing/RadarWidget'
import HotspotWidget from './landing/HotspotWidget'
import MeasureGameWidget from './landing/MeasureGameWidget'
import ParamSliderWidget from './landing/ParamSliderWidget'
import ChainWidget from './landing/ChainWidget'
import PagerDots from './landing/PagerDots'
import { FEATURES } from '../config/features'

interface StudyHighlights {
  headline_facts?: string[]
  stand?: string
}

export default function LandingPage() {
  // Studien-Headlines aus dem Deutschland-Batch (Phase 7); nur solange die
  // Studie öffentlich ist (M0-Verschlankung: abgeschaltet).
  const [study, setStudy] = useState<StudyHighlights | null>(null)
  useEffect(() => {
    if (!FEATURES.studie) return
    fetch('/api/public/lite/study-highlights')
      .then((r) => (r.ok ? r.json() : null))
      .then((d) => setStudy(d))
      .catch(() => setStudy(null))
  }, [])

  // Mobil-Vollbild-Pager aktivieren (CSS greift nur < 900px; Desktop unberührt,
  // da `.pager-page` dort `display: contents` ist — reine Struktur, keine Optik).
  useEffect(() => {
    document.documentElement.classList.add('landing-pager')
    return () => document.documentElement.classList.remove('landing-pager')
  }, [])

  return (
    <div className="landing">
      {/* ── Seite 1 · Hero ───────────────────────────────────────────── */}
      <div className="pager-page">
        <section className="landing-hero">
          <h1>Klimarisiken Ihrer Kommune. In Euro.</h1>
          <p className="hero-sub">
            KAP2 rechnet die vollständige Klimawirkungs- und Risikoanalyse (KWRA)
            für deutsche Kommunen — vom 100-Meter-Raster bis zur priorisierten
            Anpassungsplanung mit Kosten und Nutzen in Euro.
          </p>
          <p className="hero-claim">
            Aus „hohes Hitzerisiko" wird greifbar:
            <strong> „2,1 Mio. € erwarteter Schaden pro Jahr."</strong>
          </p>
          <CtaPair />
        </section>
      </div>

      {/* ── Seiten 2–4 · Widget-Strecke (Desktop: eine Sektion) ──────── */}
      <section className="landing-section">
        <div className="pager-page">
          <h2>Kennen Sie Ihre Klimarisiken, bevor sie Sie treffen</h2>
          <p className="landing-section-intro">
            Klimaanpassung ist Daseinsvorsorge — aber man kann nur schützen, was
            man kennt, verortet und wirksam angeht. Drei Schritte, die Sie hier
            direkt ausprobieren können. Die Datengrundlage ist dabei schon
            aufbereitet — Sie starten nicht bei null, sondern direkt bei Ihrer
            Kommune.
          </p>

          <StepSection
            step="Schritt 1 · Bewerten"
            question="„Wo trifft uns der Klimawandel am härtesten?"
            painpoint={
              <>Schützen kann man nur, was man kennt — aber die wenigsten Kommunen
              wissen belastbar, welche Klimarisiken sie am stärksten bedrohen und
              wie diese im Vergleich zueinander stehen.</>
            }
            bullets={[
              { title: 'Förderfähig von Haus aus:', text: 'Bewertung nach UBA-KWRA-Leitfaden und DIN EN ISO 14091 — direkt verwendbar für KAnG-Pflichten und DAS-/ANK-Förderanträge, ohne methodische Nacharbeit.' },
              { title: 'Der €-Schalter überzeugt Kämmerei und Rat:', text: 'aus „Hitzerisiko: hoch" wird „2,1 Mio € erwarteter Schaden pro Jahr" — Beschlussvorlagen argumentieren mit Beträgen statt Ampelfarben.' },
              { title: '52 Klimawirkungen nach Bundes-Priorität:', text: 'KAP2 folgt strikt der Dringlichkeitseinstufung der KWRA 2021 — Start mit den drei sehr dringenden Gesundheits-Klimawirkungen, Ausbau nach öffentlicher Roadmap. Die Verdichtung auf Handlungsfelder zeigt in Sekunden, wo der Handlungsdruck liegt.' },
              { title: 'Verteidigbar nach außen:', text: 'einheitliche, dokumentierte Methodik statt Gutachter-Ermessen — Ergebnisse halten Nachfragen von Kreis, Land und Fachöffentlichkeit stand; Büros bewerten alle Mandate vergleichbar.' },
              { title: 'In Stunden statt Monaten:', text: 'der Datenbezug (DWD, Zensus, OSM, INKAR) läuft automatisch — kein vorgelagertes Datensammel-Projekt, keine Zuarbeit aus fünf Ämtern.' },
            ]}
            widget={<RadarWidget />}
          />
        </div>

        <div className="pager-page">
          <StepSection
            reverse
            step="Schritt 2 · Verorten"
            question="„Wo müssen wir zuerst handeln — und wen schützen?"
            painpoint={
              <>Der Klimawandel trifft nicht die ganze Stadt gleich — die
              verwundbarsten Menschen und die kritischsten Orte müssen zuerst
              geschützt werden. Aber wo genau liegen sie?</>
            }
            bullets={[
              { title: 'Zielgenau statt Gießkanne:', text: 'Betroffenheit pro Baublock — begrenzte Mittel fließen dorthin, wo sie den größten Schaden verhindern, und Sie können es begründen.' },
              { title: 'Was Sie schützen, bestimmt den Ort:', text: 'Menschenleben, Gebäudewerte und Ernten haben verschiedene Hotspots — der Umschalter zeigt, warum eine Maßnahme fürs eine am Standort des anderen nichts bringt.' },
              { title: 'In jeder Zelle steckt der komplette Rechenweg — und Sie können ihn öffnen:', text: 'Hinter jeder 100-m-Zelle liegt die vollständige H×E×V-Rechnung mit Bevölkerung, Alter und sozialer Lage (Zensus/INKAR), Quellen und Euro-Betrag. Fahren Sie mit der Maus über eine Zelle — der Inspektor zeigt Formel, Faktoren und Ergebnis, Zelle für Zelle. Nichts ist Blackbox.' },
              { title: 'Karten, die jeder versteht:', text: 'ratssitzungs- und bürgerbeteiligungstauglich — wer seine eigene Straße wiedererkennt, trägt die Maßnahme davor mit.' },
              { title: 'Kein Insel-Tool:', text: 'alle Layer als GeoPackage-Export direkt ins kommunale GIS, in Bauleitplanung und Hitzeaktionsplan.' },
            ]}
            widget={<HotspotWidget />}
          />
        </div>

        <div className="pager-page">
          <StepSection
            step="Schritt 3 · Planen"
            question="„Was schützt am wirksamsten?"
            painpoint={
              <>Dieselbe Maßnahme wirkt am einen Ort stark und am anderen gar
              nicht — gut gemeint ist eben nicht gut geschützt.</>
            }
            bullets={[
              { title: 'Wirkung vor Investition:', text: 'jede Maßnahme wird am konkreten Standort durchgerechnet, BEVOR Geld fließt — die Fehlplanung fällt im Modell auf, nicht drei Jahre später im Haushalt.' },
              { title: 'CAPEX und OPEX getrennt, über Jahre:', text: 'Investition und Folgekosten sauber ausgewiesen — belastbare Haushaltsplanung statt böser Überraschungen beim Unterhalt.' },
              { title: 'Vermiedene Schäden in €/Jahr:', text: 'die Sprache von Wirtschaftlichkeitsnachweisen und Fördermittelgebern — das Nutzen-Kosten-Verhältnis für den Antrag liefert KAP2 gleich mit.' },
              { title: 'Standort-Ranking statt Bauchgefühl:', text: 'gleiche Maßnahme, drei Kandidaten-Orte — die Rangfolge nach Nutzen-Kosten ist die fertige Beschlussgrundlage für den Rat.' },
              { title: 'Maßnahmen mit belegten Kostensätzen:', text: 'quellenbelegte Kostensätze und Wirkfaktoren im Katalog — zum Start die Gesundheits-Maßnahmen von Hitzeaktionsplan bis UV-Schutz, wachsend mit jeder Roadmap-Stufe.' },
            ]}
            widget={<MeasureGameWidget />}
          />
          <CtaPair demoLabel="An einer echten Kommune: Demo" />
        </div>
      </section>

      {/* ── Seiten 5–6 · Transparenz + Wirkungsmechanismus ───────────── */}
      <section className="landing-section landing-section-alt">
        <div className="pager-page">
          <h2>Fundiert bis ins Detail — Transparenz zum Anfassen</h2>
          <div className="transparenz-param-row">
            <ParamSliderWidget />
            <div className="transparenz-param-text">
              <p className="landing-section-intro">
                Jedes Klimarisiko als H×E×V-Wirkungskette auf dem 100m-Raster — und
                für jede Kennzahl der komplette Rechenweg: vom Rohdatum über jede
                Formel und jeden Parameter bis zum Euro-Betrag. Keine Blackbox.
              </p>
              <p>
                Jeder Parameter im Modell trägt Wert, Einheit und belegte Quelle.
                Rechnet Ihre Kämmerei mit anderen Sätzen? Ändern Sie den Wert direkt
                (nebenan ein Beispiel) — mit eigener Quelle, die im Ergebnis
                dokumentiert bleibt.
              </p>
            </div>
          </div>
        </div>
        <div className="pager-page">
          <ChainWidget />
        </div>
      </section>

      {/* ── Seite 7 · Deutschland im Klimarisiko-Check (Studie) ────────
          M0-Verschlankung: Studie/Deutschland-Karte sind offline; die Sektion
          kehrt mit ihnen zurück. */}
      {(FEATURES.studie || FEATURES.deutschlandKarte) && (
        <div className="pager-page">
          <section className="landing-section">
            <h2>Deutschland im Klimarisiko-Check</h2>
            <div className="study-teaser">
              <div>
                <p className="landing-section-intro" style={{ marginBottom: '0.75rem' }}>
                  Wir haben alle rund 11.000 Gemeinden Deutschlands durchgerechnet —
                  als kostenlose Grobschätzung für die wichtigsten Klimarisiken.
                </p>
                {study?.headline_facts?.length ? (
                  <ul className="study-facts">
                    {study.headline_facts.slice(0, 3).map((f, i) => <li key={i}>{f}</li>)}
                  </ul>
                ) : (
                  <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>
                    Die KAP2-Deutschlandstudie mit Rankings und Bundesland-Vergleichen
                    erscheint hier in Kürze.
                  </p>
                )}
                <div className="study-links">
                  {FEATURES.studie && <Link to="/studie" className="btn-primary">Zur Studie →</Link>}
                  {FEATURES.deutschlandKarte && <Link to="/deutschland" className="cta-contact">Ihre Gemeinde nachschlagen →</Link>}
                </div>
              </div>
            </div>
          </section>
        </div>
      )}

      {/* ── Seite 8 · Für wen + Abschluss + Footer ───────────────────── */}
      <div className="pager-page">
        <section className="landing-section landing-section-alt">
          <h2>Für wen ist KAP2?</h2>
          <div className="audience-row">
            <div className="audience-card">
              <h3>Kommunen</h3>
              <p>
                Klimaanpassungsmanagement, Umwelt- und Stadtplanungsämter — mit
                Ergebnissen in der Sprache von Kämmerei und Rat. Vom ländlichen
                Gemeindegebiet bis zur Großstadt.
              </p>
            </div>
            <div className="audience-card">
              <h3>Beratungs- und Planungsbüros</h3>
              <p>
                Für KWRA-Mandate und Klimaanpassungskonzepte: einheitliche,
                belastbare Methodik über alle Mandate — und Exporte, die direkt
                in Bericht und GIS wandern.
              </p>
            </div>
          </div>
        </section>

        <section className="landing-closing">
          <h2>Sehen Sie KAP2 an Ihrer Kommune.</h2>
          <p>
            Der Start mit den Gesundheits-Klimarisiken ist offen und kostenlos —
            im Gespräch rechnen wir direkt über Ihre Kommune, und die Roadmap
            zeigt, was als Nächstes kommt.
          </p>
          <CtaPair />
        </section>

        <footer className="landing-footer">
          <Link to="/kontakt">Kontakt</Link>
          <span>·</span>
          <a href="#impressum" onClick={(e) => e.preventDefault()} title="Folgt">Impressum</a>
          <span>·</span>
          <a href="#datenschutz" onClick={(e) => e.preventDefault()} title="Folgt">Datenschutz</a>
          <span>·</span>
          <span className="footer-sources">
            Datenquellen: DWD · Zensus 2022 · OSM · BBSR INKAR (offene Lizenzen)
          </span>
        </footer>
      </div>

      <PagerDots />
    </div>
  )
}
