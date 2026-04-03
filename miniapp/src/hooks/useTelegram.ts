import { useEffect, useState } from 'react'
import { useAuth } from './useAuth'

// Telegram WebApp types
declare global {
  interface Window {
    Telegram?: {
      WebApp: {
        initData: string
        initDataUnsafe: {
          query_id?: string
          user?: {
            id: number
            first_name: string
            last_name?: string
            username?: string
            language_code?: string
            is_premium?: boolean
          }
          auth_date?: number
          hash?: string
        }
        ready: () => void
        close: () => void
        expand: () => void
        MainButton: {
          setText: (text: string) => void
          show: () => void
          hide: () => void
          onClick: (callback: () => void) => void
          offClick: (callback: () => void) => void
        }
        BackButton: {
          show: () => void
          hide: () => void
          onClick: (callback: () => void) => void
        }
        themeParams: {
          bg_color: string
          text_color: string
          hint_color: string
          link_color: string
          button_color: string
          button_text_color: string
        }
        colorScheme: 'light' | 'dark'
      }
    }
  }
}

interface TelegramUser {
  id: number
  first_name: string
  last_name?: string
  username?: string
  language_code?: string
  is_premium?: boolean
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

interface UseTelegramReturn {
  webApp: any | null
  user: TelegramUser | null
  isReady: boolean
  ready: () => void
  close: () => void
  expand: () => void
  // Auth related
  crmUser: CRMUser | null
  isAuthLoading: boolean
  authError: string | null
  refreshAuth: () => void
}

export function useTelegram(): UseTelegramReturn {
  const [webApp, setWebApp] = useState<any | null>(null)
  const [user, setUser] = useState<TelegramUser | null>(null)
  const [isReady, setIsReady] = useState(false)
  const { authWithBackend, user: crmUser, isLoading: isAuthLoading, error: authError } = useAuth()

  useEffect(() => {
    // Check if running in Telegram WebApp
    if (window.Telegram?.WebApp) {
      const tg = window.Telegram.WebApp
      setWebApp(tg)
      const telegramUser = tg.initDataUnsafe?.user || null
      setUser(telegramUser)
      setIsReady(true)
      
      // Notify Telegram that app is ready
      tg.ready()
      console.log('[useTelegram] Telegram WebApp ready:', telegramUser)
    } else {
      console.warn('[useTelegram] Not running in Telegram WebApp')
      setIsReady(true)
    }
  }, [])

  // Auto auth with backend when Telegram user is available
  useEffect(() => {
    if (user && !crmUser && !isAuthLoading) {
      const userData = {
        telegram_id: user.id,
        first_name: user.first_name,
        last_name: user.last_name,
        username: user.username,
      }
      console.log('[useTelegram] Auto-authing with backend:', userData)
      authWithBackend(userData)
    }
  }, [user, crmUser, isAuthLoading, authWithBackend])

  const ready = () => {
    webApp?.ready()
  }

  const close = () => {
    webApp?.close()
  }

  const expand = () => {
    webApp?.expand()
  }

  const refreshAuth = () => {
    if (user) {
      authWithBackend({
        telegram_id: user.id,
        first_name: user.first_name,
        last_name: user.last_name,
        username: user.username,
      })
    }
  }

  return {
    webApp,
    user,
    isReady,
    ready,
    close,
    expand,
    crmUser,
    isAuthLoading,
    authError,
    refreshAuth,
  }
}
