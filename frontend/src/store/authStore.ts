import { create } from 'zustand'

interface AuthUser {
  id?: number
  username?: string
  email?: string
}

interface LoginResponse {
  token: string
  user: AuthUser
}

interface AuthStore {
  token: string | null
  user: AuthUser | null
  login: (email: string, password: string) => Promise<void>
  logout: () => void
  setToken: (token: string) => void
  setUser: (user: AuthUser) => void
}

export const useAuthStore = create<AuthStore>((set) => {
  // Load from localStorage on init
  const storedToken = localStorage.getItem('token')

  return {
    token: storedToken || null,
    user: null,

    login: async (email: string, password: string) => {
      try {
        const response = await fetch('/api/auth/login/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ username: email, password }),
        })

        if (!response.ok) throw new Error('Login failed')

        const data: LoginResponse = await response.json()
        localStorage.setItem('token', data.token)
        set({ token: data.token, user: data.user })
      } catch (error) {
        console.error('Login error:', error)
        throw error
      }
    },

    logout: () => {
      localStorage.removeItem('token')
      set({ token: null, user: null })
    },

    setToken: (token) => {
      localStorage.setItem('token', token)
      set({ token })
    },

    setUser: (user) => {
      set({ user })
    },
  }
})
