import { BrowserRouter, Routes, Route } from 'react-router-dom'
import PublicLayout from './layouts/PublicLayout'
import ProductLayout from './layouts/ProductLayout'
import RequireAuth from './components/RequireAuth'
import LandingPage from './pages/LandingPage'
import LoginPage from './pages/LoginPage'
import KontaktPage from './pages/KontaktPage'
import DemoPage from './pages/DemoPage'
import LiteMapPage from './pages/lite/LiteMapPage'
import AdminLayout from './pages/admin/AdminLayout'
import StudyPage from './pages/StudyPage'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Öffentlich: Landing, Login, Kontakt, Deutschland-Karte, Studie */}
        <Route element={<PublicLayout />}>
          <Route path="/" element={<LandingPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/kontakt" element={<KontaktPage />} />
          <Route path="/deutschland" element={<LiteMapPage />} />
          <Route path="/studie" element={<StudyPage />} />
        </Route>

        {/* Demo: Produkt-Shell im Demo-Modus (öffentlich, ohne Login) */}
        <Route path="/demo/*" element={<DemoPage />} />

        {/* Produkt (Login erforderlich) */}
        <Route
          path="/app/*"
          element={
            <RequireAuth>
              <ProductLayout />
            </RequireAuth>
          }
        />

        {/* Admin */}
        <Route
          path="/admin/*"
          element={
            <RequireAuth requireAdmin>
              <AdminLayout />
            </RequireAuth>
          }
        />

        {/* Fallback: Landing */}
        <Route path="*" element={<PublicLayout />}>
          <Route path="*" element={<LandingPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}
