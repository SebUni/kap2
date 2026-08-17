import { NavLink, Navigate, Route, Routes, useNavigate } from 'react-router-dom'
import { useAuthStore } from '../../store/authStore'
import UsersTab from './UsersTab'
import AssessmentsTab from './AssessmentsTab'
import LiteBatchTab from './LiteBatchTab'
import DemoConfigTab from './DemoConfigTab'
import AiConfigTab from './AiConfigTab'

const TABS = [
  { to: '/admin/users', label: 'Nutzer' },
  { to: '/admin/berechnungen', label: 'Berechnungen' },
  { to: '/admin/deutschland', label: 'Deutschland-Batch' },
  { to: '/admin/demo', label: 'Demo' },
  { to: '/admin/ki', label: 'KI-Assistent' },
]

export default function AdminLayout() {
  const { user, logout } = useAuthStore()
  const navigate = useNavigate()

  return (
    <div className="admin-shell">
      <header className="admin-topbar">
        <h1>KAP2 Admin</h1>
        <nav className="admin-nav">
          {TABS.map((t) => (
            <NavLink key={t.to} to={t.to}
              className={({ isActive }) => `admin-nav-link${isActive ? ' active' : ''}`}>
              {t.label}
            </NavLink>
          ))}
        </nav>
        <div className="admin-topbar-right">
          <button className="btn-secondary" onClick={() => navigate('/app')}>Zum Produkt</button>
          <span className="admin-user">{user?.email}</span>
          <button className="btn-secondary" onClick={async () => { await logout(); navigate('/') }}>
            Abmelden
          </button>
        </div>
      </header>
      <main className="admin-content">
        <Routes>
          <Route index element={<Navigate to="/admin/users" replace />} />
          <Route path="users" element={<UsersTab />} />
          <Route path="berechnungen" element={<AssessmentsTab />} />
          <Route path="deutschland" element={<LiteBatchTab />} />
          <Route path="demo" element={<DemoConfigTab />} />
          <Route path="ki" element={<AiConfigTab />} />
        </Routes>
      </main>
    </div>
  )
}
