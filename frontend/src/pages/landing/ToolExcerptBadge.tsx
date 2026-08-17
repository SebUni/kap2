/**
 * Kleiner Eck-Chip „interaktiv", der ein Landing-Widget als echten,
 * ausprobierbaren Ausschnitt aus dem KAP2-Tool kennzeichnet. Als erstes Kind in
 * jede `.landing-widget`-Wurzel gehängt; Position (Tab auf der oberen Kante),
 * Hover-Verhalten und Farben kommen aus index.css (`.tool-excerpt-badge`,
 * `.landing-widget:hover`). Rein dekorativ (`aria-hidden`, `pointer-events:none`).
 */
export default function ToolExcerptBadge() {
  return (
    <span className="tool-excerpt-badge" aria-hidden="true">
      <span className="tool-excerpt-dot" />
      interaktiv
    </span>
  )
}
