import { useTelegram } from './hooks/useTelegram'
import './App.css'

function App() {
  const { user, isReady, webApp, close } = useTelegram()

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
