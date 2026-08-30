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
import RoadmapPage from './pages/RoadmapPage'
import { FEATURES } from './config/features'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Öffentlich: Landing, Login, Kontakt, Roadmap; abgeschaltete
            Bereiche (M0-Verschlankung) fallen in den Landing-Fallback. */}
        <Route element={<PublicLayout />}>
          <Route path="/" element={<LandingPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/kontakt" element={<KontaktPage />} />
          {FEATURES.roadmap && <Route path="/roadmap" element={<RoadmapPage />} />}
          {FEATURES.deutschlandKarte && <Route path="/deutschland" element={<LiteMapPage />} />}
          {FEATURES.studie && <Route path="/studie" element={<StudyPage />} />}
        </Route>

        {/* Demo: Produkt-Shell im Demo-Modus (öffentlich, ohne Login) */}
        {FEATURES.demo && <Route path="/demo/*" element={<DemoPage />} />}

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
