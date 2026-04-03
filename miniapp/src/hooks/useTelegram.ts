import { useEffect, useState } from 'react'

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

interface UseTelegramReturn {
  webApp: any | null
  user: TelegramUser | null
  isReady: boolean
  ready: () => void
  close: () => void
  expand: () => void
}

export function useTelegram(): UseTelegramReturn {
  const [webApp, setWebApp] = useState<any | null>(null)
  const [user, setUser] = useState<TelegramUser | null>(null)
  const [isReady, setIsReady] = useState(false)

  useEffect(() => {
    // Check if running in Telegram WebApp
    if (window.Telegram?.WebApp) {
      const tg = window.Telegram.WebApp
      setWebApp(tg)
      setUser(tg.initDataUnsafe?.user || null)
      setIsReady(true)
      
      // Notify Telegram that app is ready
      tg.ready()
    } else {
      console.warn('Not running in Telegram WebApp')
      setIsReady(true)
    }
  }, [])

  const ready = () => {
    webApp?.ready()
  }

  const close = () => {
    webApp?.close()
  }

  const expand = () => {
    webApp?.expand()
  }

  return {
    webApp,
    user,
    isReady,
    ready,
    close,
    expand,
  }
}
