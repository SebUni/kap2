/**
 * M0-Verschlankung (docs/ROADMAP.md §5): Nicht-Kern-Bereiche sind abgeschaltet
 * und kehren mit späteren Stufen zurück (Demo: Stage 2, Studie: M3½,
 * Deutschland-Karte: mit der Re-Expansion). Nur hier schalten — Routen,
 * Navigation und CTAs hängen alle an diesem Modul. Serverseitiges Pendant:
 * DEMO_ENABLED / STUDY_ENABLED / LITE_PAGES_ENABLED in backend/app/config.py.
 */
export const FEATURES = {
  demo: false,
  studie: false,
  deutschlandKarte: false,
  roadmap: true,
} as const
