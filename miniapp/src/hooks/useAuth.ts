/**
 * Telegram Auth Hook - Backend bilan autentifikatsiya
 */

import { useState, useCallback } from 'react'

interface TelegramUserData {
  telegram_id: number
  first_name: string
  last_name?: string
  username?: string
}

interface CRMUser {
  id: number
  telegram_id: string
  first_name: string
  last_name?: string
  username?: string
  created_at?: string
  updated_at?: string
}

interface AuthState {
  user: CRMUser | null
  isLoading: boolean
  error: string | null
}

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
console.log('[useAuth] Backend API URL:', API_URL)

export function useAuth() {
  const [authState, setAuthState] = useState<AuthState>({
    user: null,
    isLoading: false,
    error: null,
  })

  const authWithBackend = useCallback(async (telegramUser: TelegramUserData) => {
    console.log('[useAuth] Starting auth with backend:', telegramUser)
    setAuthState(prev => ({ ...prev, isLoading: true, error: null }))

    try {
      const response = await fetch(`${API_URL}/api/auth/telegram`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(telegramUser),
      })

      if (!response.ok) {
        const errorText = await response.text()
        throw new Error(`Auth failed: ${response.status} - ${errorText}`)
      }

      const user: CRMUser = await response.json()
      console.log('[useAuth] Backend auth successful:', user)
      
      setAuthState({
        user,
        isLoading: false,
        error: null,
      })

      return user
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Unknown error'
      console.error('[useAuth] Backend auth error:', errorMessage)
      
      setAuthState(prev => ({
        ...prev,
        isLoading: false,
        error: errorMessage,
      }))

      return null
    }
  }, [])

  const clearAuth = useCallback(() => {
    setAuthState({
      user: null,
      isLoading: false,
      error: null,
    })
  }, [])

  return {
    ...authState,
    authWithBackend,
    clearAuth,
  }
}
