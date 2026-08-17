import { useEffect } from 'react'
import { Navigate, useLocation } from 'react-router-dom'
import { useAuthStore } from '../store/authStore'
import InlineSpinner from './InlineSpinner'

interface Props {
  children: React.ReactNode
  requireAdmin?: boolean
}

export default function RequireAuth({ children, requireAdmin = false }: Props) {
  const { user, checked, fetchMe } = useAuthStore()
  const location = useLocation()

  useEffect(() => {
    if (!checked) fetchMe()
  }, [checked, fetchMe])

  if (!checked) {
    return (
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', minHeight: '60vh', gap: 8, color: 'var(--text-muted)' }}>
        <InlineSpinner /> Anmeldung wird geprüft …
      </div>
    )
  }

  if (!user) {
    return <Navigate to="/login" replace state={{ from: location.pathname }} />
  }

  if (requireAdmin && user.role !== 'admin') {
    return (
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', minHeight: '60vh', color: 'var(--text-muted)' }}>
        Dieser Bereich ist Administratoren vorbehalten.
      </div>
    )
  }

  return <>{children}</>
}
