import { useEffect, useState } from 'react'
import { api, type AdminUser } from '../../api/client'
import InlineSpinner from '../../components/InlineSpinner'

interface KommuneHit { id: number; name: string; bundesland?: string }

function UserEditor({ user, onClose, onSaved }: {
  user: AdminUser | null
  onClose: () => void
  onSaved: (initialPw?: string) => void
}) {
  const [email, setEmail] = useState(user?.email ?? '')
  const [name, setName] = useState(user?.display_name ?? '')
  const [role, setRole] = useState(user?.role ?? 'user')
  const [active, setActive] = useState(user?.is_active ?? true)
  const [kommunen, setKommunen] = useState<{ id: number; name: string }[]>(user?.kommunen ?? [])
  const [search, setSearch] = useState('')
  const [hits, setHits] = useState<KommuneHit[]>([])
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (search.length < 2) { setHits([]); return }
    const t = setTimeout(async () => {
      try {
        // Bereits berechnete Kommunen aus der Liste (Admin sieht alle)
        const all = await api.listKommunen() as unknown as KommuneHit[]
        setHits(all.filter((k) => k.name.toLowerCase().includes(search.toLowerCase())).slice(0, 8))
      } catch { setHits([]) }
    }, 250)
    return () => clearTimeout(t)
  }, [search])

  const save = async () => {
    setBusy(true); setError(null)
    try {
      const kommune_ids = kommunen.map((k) => k.id)
      if (user) {
        await api.admin.updateUser(user.id, { display_name: name, role, is_active: active, kommune_ids })
        onSaved()
      } else {
        const res = await api.admin.createUser({ email, display_name: name, role, kommune_ids })
        onSaved(res.initial_password)
      }
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e))
    } finally { setBusy(false) }
  }

  return (
    <div className="admin-modal-overlay" onClick={onClose}>
      <div className="admin-modal" onClick={(e) => e.stopPropagation()}>
        <h3>{user ? 'Nutzer bearbeiten' : 'Nutzer anlegen'}</h3>
        <label className="admin-field">E-Mail
          <input value={email} disabled={!!user} onChange={(e) => setEmail(e.target.value)} />
        </label>
        <label className="admin-field">Anzeigename
          <input value={name} onChange={(e) => setName(e.target.value)} />
        </label>
        <div className="admin-field-row">
          <label className="admin-field">Rolle
            <select value={role} onChange={(e) => setRole(e.target.value as 'admin' | 'user')}>
              <option value="user">Nutzer</option>
              <option value="admin">Administrator</option>
            </select>
          </label>
          {user && (
            <label className="admin-field admin-check">
              <input type="checkbox" checked={active} onChange={(e) => setActive(e.target.checked)} /> aktiv
            </label>
          )}
        </div>
        <div className="admin-field">Zugeordnete Kommunen
          <div className="admin-chips">
            {kommunen.map((k) => (
              <span key={k.id} className="admin-chip">
                {k.name}
                <button onClick={() => setKommunen((cur) => cur.filter((x) => x.id !== k.id))}>×</button>
              </span>
            ))}
          </div>
          <input placeholder="Kommune suchen…" value={search} onChange={(e) => setSearch(e.target.value)} />
          {hits.length > 0 && (
            <div className="admin-hits">
              {hits.map((h) => (
                <button key={h.id} onClick={() => {
                  if (!kommunen.some((k) => k.id === h.id)) setKommunen((cur) => [...cur, { id: h.id, name: h.name }])
                  setSearch(''); setHits([])
                }}>{h.name}</button>
              ))}
            </div>
          )}
        </div>
        {error && <div className="login-error">{error}</div>}
        <div className="admin-modal-actions">
          <button className="btn-secondary" onClick={onClose}>Abbrechen</button>
          <button className="btn-primary" onClick={save} disabled={busy}>
            {busy ? <InlineSpinner /> : 'Speichern'}
          </button>
        </div>
      </div>
    </div>
  )
}

export default function UsersTab() {
  const [users, setUsers] = useState<AdminUser[]>([])
  const [loading, setLoading] = useState(true)
  const [editing, setEditing] = useState<AdminUser | null>(null)
  const [creating, setCreating] = useState(false)
  const [notice, setNotice] = useState<string | null>(null)

  const load = async () => {
    setLoading(true)
    try { setUsers(await api.admin.listUsers()) } finally { setLoading(false) }
  }
  useEffect(() => { load() }, [])

  return (
    <div className="admin-tab">
      <div className="admin-tab-head">
        <h2>Nutzer</h2>
        <button className="btn-primary" onClick={() => setCreating(true)}>+ Nutzer anlegen</button>
      </div>
      {notice && <div className="admin-notice">{notice}</div>}
      {loading ? <InlineSpinner /> : (
        <table className="admin-table">
          <thead><tr><th>E-Mail</th><th>Rolle</th><th>Kommunen</th><th>Status</th><th></th></tr></thead>
          <tbody>
            {users.map((u) => (
              <tr key={u.id}>
                <td>{u.email}</td>
                <td>{u.role === 'admin' ? 'Admin' : 'Nutzer'}</td>
                <td>{u.role === 'admin' ? '(alle)' : u.kommunen.map((k) => k.name).join(', ') || '—'}</td>
                <td><span className={`status-badge ${u.is_active ? 'done' : 'error'}`}>{u.is_active ? 'aktiv' : 'inaktiv'}</span></td>
                <td><button className="btn-secondary" onClick={() => setEditing(u)}>Bearbeiten</button></td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
      {(editing || creating) && (
        <UserEditor
          user={editing}
          onClose={() => { setEditing(null); setCreating(false) }}
          onSaved={(pw) => {
            setEditing(null); setCreating(false)
            if (pw) setNotice(`Initialpasswort (bitte weitergeben): ${pw}`)
            load()
          }}
        />
      )}
    </div>
  )
}
