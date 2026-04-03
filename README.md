# For.Ever Cosmetics - Telegram Mini App CRM

Professional CRM system built as a Telegram Mini App with Python backend.

## 🏗️ Architecture

```
jocrm/
├── bot/                    # Telegram Bot (Entry Point)
│   ├── app/
│   │   ├── config.py      # Bot configuration
│   │   └── handlers/
│   │       └── commands.py  # /start, /help handlers
│   ├── main.py            # Bot entry point
│   ├── requirements.txt   # Bot dependencies
│   └── .env.example       # Bot env template
│
├── backend/               # FastAPI Backend
│   ├── app/
│   │   ├── config.py      # Backend configuration
│   │   ├── main.py        # FastAPI app
│   │   ├── api/
│   │   │   └── v1/
│   │   │       └── endpoints/
│   │   │           └── health.py
│   │   └── core/
│   ├── run.py             # Backend runner
│   ├── requirements.txt   # Backend dependencies
│   └── .env.example       # Backend env template
│
├── miniapp/               # React + Vite Mini App
│   ├── src/
│   │   ├── main.tsx       # React entry
│   │   ├── App.tsx        # Main component
│   │   ├── App.css        # Styles
│   │   └── hooks/
│   │       └── useTelegram.ts  # Telegram WebApp hook
│   ├── index.html         # HTML template
│   ├── package.json       # NPM dependencies
│   ├── tsconfig.json      # TypeScript config
│   └── vite.config.ts     # Vite config
│
├── .gitignore             # Root gitignore
└── README.md              # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Telegram Bot Token (from @BotFather)

### 1. Bot Setup

```bash
# Navigate to bot directory
cd bot

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env
# Edit .env and add your BOT_TOKEN
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env
```

### 3. Mini App Setup

```bash
# Navigate to miniapp directory
cd miniapp

# Install dependencies
npm install

# Start development server
npm run dev
```

## 🏃 Running the Project

You need to run 3 services simultaneously:

### Terminal 1: Backend
```bash
cd backend
venv\Scripts\activate
venv\Scripts\python run.py
# Or: uvicorn backend.app.main:app --reload --port 8000
```

### Terminal 2: Mini App
```bash
cd miniapp
npm run dev
```

### Terminal 3: Bot
```bash
cd bot
venv\Scripts\activate
venv\Scripts\python main.py
```

## � Service URLs

| Service | URL | Description |
|---------|-----|-------------|
| Mini App | http://localhost:5173 | React development server |
| Backend API | http://localhost:8000 | FastAPI server |
| API Docs | http://localhost:8000/docs | Swagger documentation |
| Bot | @jocrmbot | Telegram bot |

## 📱 How It Works

1. **User starts bot**: Sends `/start` to @jocrmbot
2. **Bot sends welcome**: Shows welcome message with Web App button
3. **User clicks button**: Opens Mini App inside Telegram
4. **Mini App loads**: React app fetches user data from Telegram WebApp
5. **CRM works**: User interacts with CRM features in Mini App
6. **Backend serves**: FastAPI handles data and database operations

## 🔧 Configuration

### Bot .env
```env
BOT_TOKEN=your_bot_token_here
BOT_MODE=polling
MINIAPP_URL=http://localhost:5173
API_URL=http://localhost:8000
```

### Backend .env
```env
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=http://localhost:5173
DATABASE_URL=postgresql+asyncpg://...
```

## 📦 Deployment

### Backend (e.g., Railway/Render)
1. Push to GitHub
2. Connect to Railway/Render
3. Set environment variables
4. Deploy

### Mini App (Static Hosting)
1. Build: `npm run build`
2. Upload `dist/` to static hosting
3. Set Mini App URL in @BotFather

### Bot
1. Set webhook URL (for production)
2. Or use polling (for development)

## �️ Tech Stack

- **Bot**: Python, aiogram 3.x
- **Backend**: FastAPI, SQLAlchemy, PostgreSQL, Pydantic
- **Frontend**: React 18, TypeScript, Vite
- **Integration**: Telegram WebApp API

## � Next Steps

1. [ ] Add database models (SQLAlchemy)
2. [ ] Create API endpoints
3. [ ] Build Mini App pages
4. [ ] Add authentication
5. [ ] Deploy to production

## 📞 Support

- Telegram: @support
- Email: info@forevercosmetics.uz
