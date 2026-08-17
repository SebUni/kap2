import { useEffect, useState } from 'react'

/**
 * Seitenpunkte für den Mobil-Vollbild-Pager: ein Punkt je `.pager-page`. Der
 * aktive Punkt folgt der im Viewport-Zentrum liegenden Seite (IntersectionObserver
 * mit schmalem Mittelband, robust für hohe wie niedrige Seiten). Klick scrollt zur
 * Seite. Nur mobil sichtbar (`html.landing-pager` + Media-Query in index.css);
 * auf Desktop `display: none`.
 */
export default function PagerDots() {
  const [count, setCount] = useState(0)
  const [active, setActive] = useState(0)

  useEffect(() => {
    const pages = Array.from(document.querySelectorAll<HTMLElement>('.pager-page'))
    setCount(pages.length)
    if (pages.length < 2) return

    const io = new IntersectionObserver(
      (entries) => {
        for (const e of entries) {
          if (!e.isIntersecting) continue
          const i = pages.indexOf(e.target as HTMLElement)
          if (i >= 0) setActive(i)
        }
      },
      // Schmales Band um die vertikale Mitte: die dort liegende Seite ist aktiv.
      { rootMargin: '-45% 0px -45% 0px', threshold: 0 },
    )
    pages.forEach((p) => io.observe(p))
    return () => io.disconnect()
  }, [])

  if (count < 2) return null

  const scrollTo = (i: number) => {
    document.querySelectorAll<HTMLElement>('.pager-page')[i]
      ?.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }

  return (
    <nav className="pager-dots" aria-label="Abschnitte">
      {Array.from({ length: count }, (_, i) => (
        <button
          key={i}
          type="button"
          className={`pager-dot${i === active ? ' active' : ''}`}
          aria-label={`Zu Abschnitt ${i + 1} von ${count}`}
          aria-current={i === active ? 'true' : undefined}
          onClick={() => scrollTo(i)}
        />
      ))}
    </nav>
  )
}
