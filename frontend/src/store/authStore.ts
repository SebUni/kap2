import { create } from 'zustand'
import { api, setUnauthorizedHandler, type AuthUser } from '../api/client'

interface AuthState {
  user: AuthUser | null
  /** true, sobald /auth/me einmal beantwortet wurde (Spinner-Steuerung). */
  checked: boolean
  fetchMe: () => Promise<void>
  login: (email: string, password: string) => Promise<AuthUser>
  logout: () => Promise<void>
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  checked: false,

  fetchMe: async () => {
    try {
      const res = await api.auth.me()
      set({ user: res.authenticated && res.user ? res.user : null, checked: true })
    } catch {
      set({ user: null, checked: true })
    }
  },

  login: async (email, password) => {
    const user = await api.auth.login(email, password)
    set({ user, checked: true })
    return user
  },

  logout: async () => {
    try {
      await api.auth.logout()
    } finally {
      set({ user: null, checked: true })
    }
  },
}))

// 401 auf geschützten Pfaden: Session serverseitig tot → lokalen Zustand
// leeren; RequireAuth leitet dann zum Login um.
setUnauthorizedHandler(() => {
  const { user } = useAuthStore.getState()
  if (user) useAuthStore.setState({ user: null, checked: true })
})
