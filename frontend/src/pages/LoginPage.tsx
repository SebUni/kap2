import { useState } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { useAuthStore } from '../store/authStore'
import InlineSpinner from '../components/InlineSpinner'

export default function LoginPage() {
  const login = useAuthStore((s) => s.login)
  const navigate = useNavigate()
  const location = useLocation()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [busy, setBusy] = useState(false)

  const from = (location.state as { from?: string } | null)?.from

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)
    setBusy(true)
    try {
      const user = await login(email.trim(), password)
      navigate(from || (user.role === 'admin' ? '/admin' : '/app'), { replace: true })
    } catch (err) {
      const msg = err instanceof Error ? err.message : String(err)
      setError(msg.includes('401') ? 'E-Mail oder Passwort falsch.' : msg)
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="login-page">
      <form className="login-card" onSubmit={handleSubmit}>
        <h2>Anmelden</h2>
        <label className="login-label">
          E-Mail
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            autoComplete="username"
            required
            autoFocus
          />
        </label>
        <label className="login-label">
          Passwort
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            autoComplete="current-password"
            required
          />
        </label>
        {error && <div className="login-error">{error}</div>}
        <button type="submit" className="btn-primary login-submit" disabled={busy}>
          {busy ? <><InlineSpinner /> Anmelden …</> : 'Anmelden'}
        </button>
        <p className="login-hint">
          Noch kein Zugang? <Link to="/kontakt">Kontakt aufnehmen →</Link>
        </p>
      </form>
    </div>
  )
}
