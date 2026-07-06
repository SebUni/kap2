export default function InlineSpinner({ size = 14 }: { size?: number }) {
  return (
    <span
      aria-hidden
      style={{
        display: 'inline-block',
        width: size,
        height: size,
        border: '2px solid var(--border)',
        borderTopColor: 'var(--primary)',
        borderRadius: '50%',
        animation: 'map-spin 0.8s linear infinite',
        verticalAlign: 'middle',
      }}
    />
  )
}
