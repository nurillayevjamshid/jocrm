import { useTelegram } from './hooks/useTelegram'
import './App.css'

function App() {
  const { user, isReady, webApp, close, crmUser, isAuthLoading, authError, refreshAuth } = useTelegram()

  if (!isReady) {
    return (
      <div className="loading">
        <div className="spinner"></div>
        <p>Yuklanmoqda...</p>
      </div>
    )
  }

  return (
    <div className="app">
      <header className="header">
        <h1>For.Ever Cosmetics</h1>
        <p className="subtitle">CRM Tizimi</p>
      </header>

      <main className="main">
        {user ? (
          <section className="welcome-section">
            <div className="user-card">
              <div className="avatar">
                {user.first_name[0]}
                {user.last_name?.[0]}
              </div>
              <div className="user-info">
                <h2>
                  {user.first_name} {user.last_name}
                </h2>
                {user.username && <p>@{user.username}</p>}
                {user.is_premium && <span className="premium">⭐ Premium</span>}
              </div>
            </div>

            {/* CRM Auth Status */}
            <div className="auth-status" style={{ marginTop: '1rem', padding: '1rem', background: '#f0f0f0', borderRadius: '8px' }}>
              <h4>🔐 CRM Auth Status</h4>
              {isAuthLoading && <p style={{ color: '#666' }}>⏳ Backend bilan ulanmoqda...</p>}
              {authError && <p style={{ color: 'red' }}>❌ Xatolik: {authError}</p>}
              {crmUser && (
                <div style={{ color: 'green' }}>
                  <p>✅ CRM User: {crmUser.first_name} {crmUser.last_name}</p>
                  <p style={{ fontSize: '0.8rem', color: '#666' }}>
                    Telegram ID: {crmUser.telegram_id} | CRM ID: {crmUser.id}
                  </p>
                  {crmUser.created_at && (
                    <p style={{ fontSize: '0.8rem', color: '#666' }}>
                      Created: {new Date(crmUser.created_at).toLocaleString()}
                    </p>
                  )}
                </div>
              )}
              {crmUser && (
                <button 
                  onClick={refreshAuth} 
                  style={{ marginTop: '0.5rem', padding: '0.5rem 1rem', fontSize: '0.9rem' }}
                >
                  🔄 Auth ni yangilash
                </button>
              )}
            </div>

            <div className="features">
              <h3>Tez orada:</h3>
              <ul>
                <li>📊 Mijozlar boshqaruvi</li>
                <li>🛒 Buyurtmalarni kuzatish</li>
                <li>📈 Hisobotlar va statistika</li>
                <li>🔔 Real-time xabarnomalar</li>
              </ul>
            </div>
          </section>
        ) : (
          <section className="no-user">
            <div className="info-card">
              <h3>👋 Xush kelibsiz!</h3>
              <p>
                Bu Mini App Telegram ichida ishlaydi.
                <br />
                Bot orqali oching: @jocrmbot
              </p>
              <p className="dev-mode">Development mode</p>
            </div>
          </section>
        )}
      </main>

      <footer className="footer">
        {webApp && (
          <button className="close-btn" onClick={close}>
            ✅ Yopish
          </button>
        )}
        <p className="version">v0.1.0</p>
      </footer>
    </div>
  )
}

export default App
