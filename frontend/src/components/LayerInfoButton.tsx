interface Props {
  label: string
  onClick: () => void
}

export default function LayerInfoButton({ label, onClick }: Props) {
  return (
    <button
      type="button"
      className="layer-info-btn"
      aria-label={`Info: ${label}`}
      title="Wirkungsmechanismus anzeigen"
      onClick={e => { e.stopPropagation(); onClick() }}
    >
      i
    </button>
  )
}
