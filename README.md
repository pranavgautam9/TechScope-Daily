# 📰 TechScope Daily

<div align="center">

**AI-Powered Tech News Platform | Your Daily Tech Digest**

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-20232A?style=flat&logo=react&logoColor=61DAFB)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=flat&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[Live App](https://pranavgautam.com/TechScope-Daily) · [API Docs](http://localhost:8000/docs) · [Repository](https://github.com/pranavgautam9/TechScope-Daily)

*Stay informed with the latest tech news, stock updates, and AI-generated insights*

</div>

---

## 🎯 Overview

**TechScope Daily** is a modern, AI-powered tech news platform that delivers personalized daily tech insights, breaking news, market updates, and fascinating tech facts. The frontend is a React + TypeScript app; the backend is FastAPI with JWT auth, RSS news ingestion, yfinance stock data, and Hugging Face-backed fact generation.

The production frontend is deployed to GitHub Pages at [pranavgautam.com/TechScope-Daily](https://pranavgautam.com/TechScope-Daily). Locally you can run both servers and use SQLite; production can use PostgreSQL via `DATABASE_URL`.

### Key Highlights

- ✨ **Daily Updates**: Fresh news, stocks, and facts on a background scheduler
- 🤖 **AI-Powered**: Hugging Face for daily facts plus sentiment/impact analysis on news
- 📊 **Stock Tracking**: Live Yahoo Finance data for 10 major tech companies
- 🗞️ **10 News Sources**: Google News Tech, Wired, TechCrunch, The Verge, Ars Technica, Engadget, MIT Technology Review, CNET, VentureBeat, and TechRepublic
- 🎨 **Modern UI**: Glassmorphism design with auto-rotating cards
- 🔐 **Accounts**: Signup/login with JWT, bcrypt password hashing, and a built-in test account
- 🎛️ **Personalization**: Per-user news sources and companies, saved in the browser

---

## ✨ Features

### 🔐 Authentication & Login Flow

- **Login & Signup Screen**

<div align="center">
  <img src="images/login-screen.png" alt="Login and Signup Screen" width="800"/>
  <p><em>Authentication screen with login and sign-up tabs</em></p>
</div>

- **Loading Screen First**: On startup, users see a dynamic loading screen with a daily AI-generated tech fact.
- **Login / Signup Screen**: After loading, users land on a dedicated authentication page with:
  - Separate **Login** and **Create Account** tabs
  - Email, first name, last name, and password fields for signup
  - Password visibility toggle (eye icon)
  - Case-insensitive email matching so login is not blocked by capitalization
- **Secure Authentication**: FastAPI + JWT (`python-jose`); passwords hashed with bcrypt.
- **Persistent Sessions**: Auth state and token are stored in the browser so users stay logged in across refreshes.
- **Logout & Account Controls**: A **Logout** button and an **Account** menu in the navbar (top-right, next to *News* and *Live Stocks*).
- **First-Time Preferences**: On the first login for a user, a one-time preferences dialog appears so they can choose:
  - Which **tech news sources** to follow
  - Which **tech companies** to track in the stocks view
  These preferences are saved per-user in the browser and are **not shown again** automatically on subsequent logins.
- **In-App Account Settings**: From the account menu, users can:
  - **Change news sources**
  - **Change companies**
  - **Change password**
- **Built-in Test User** (created automatically on backend startup):
  - Email: `testuser@gmail.com`
  - Password: `Password123!`

### 🧠 Daily Facts

<div align="center">
  <img src="images/loading-screen.png" alt="Loading Screen with Daily Fact" width="800"/>
  <p><em>Loading screen displaying daily tech fact</em></p>
</div>

- **AI-Generated Facts**: Unique tech facts generated daily (Hugging Face, with a local fallback catalog)
- **Loading Screen Display**: Facts shown during app startup
- **Daily Rotation**: New fact every day at midnight (scheduler) or on first request if none exists yet
- **No API Key Required**: Uses the public Hugging Face Inference API by default

### 📰 News Section

<div align="center">
  <img src="images/news-section.png" alt="News Section" width="800"/>
  <p><em>News feed with article cards and impact scoring</em></p>
</div>

- **Curated Tech News**: RSS feeds from 10 quality tech sources
- **Breaking News Alerts**: Trending/breaking items with importance scoring
- **AI Analysis**: Sentiment (`positive` / `negative` / `neutral`) and impact (`high` / `medium` / `low`)
- **Content Extraction**: Article previews with a link to the full story
- **Personalized Sources**: The feed is filtered to the sources each user selected

**Sources**

| Source | Feed |
|--------|------|
| Google News (Tech) | Google News RSS |
| Wired | wired.com |
| TechCrunch | techcrunch.com |
| The Verge | theverge.com |
| Ars Technica | arstechnica.com |
| Engadget | engadget.com |
| MIT Technology Review | technologyreview.com |
| CNET | cnet.com |
| VentureBeat | venturebeat.com |
| TechRepublic | techrepublic.com |

News is fetched on backend startup, at 6:00 AM, at noon, and every 2 hours.

### 📈 Stocks Section

<div align="center">
  <img src="images/stocks-section.png" alt="Stocks Section" width="800"/>
  <p><em>Stock tracking with real-time data and metrics</em></p>
</div>

- **Major Tech Stocks**: AAPL, MSFT, GOOGL, AMZN, TSLA, META, NVDA, NFLX, ADBE, CRM
- **Yahoo Finance**: Prices via `yfinance` (no Alpha Vantage key required)
- **Daily Refresh**: Scheduler updates stocks at 9:00 AM (market open) and on backend startup
- **Metrics**: Price, change, volume, and market cap with color-coded gains/losses
- **Personalized Watchlist**: Cards are filtered to the companies each user selected

### 👤 User Accounts & Preferences

- **Account Menu & Settings**

<div align="center">
  <img src="images/account-menu.png" alt="Account menu with preferences and password options" width="800"/>
  <p><em>Account dropdown to change news sources, companies, and password</em></p>
</div>

- **Per-User Content Preferences**: Each user chooses preferred news sources and companies.
- **First-Time Onboarding**: On first login, a guided dialog walks users through selecting news sources and stocks.
- **In-App Account Settings**: From the account menu, users can adjust news sources, companies, and change their password.

**First-Time Preferences Dialog**

<div align="center">
  <img src="images/first-login-preferences.png" alt="First-time preferences dialog" width="800"/>
  <p><em>Onboarding dialog to pick preferred news sources and companies</em></p>
</div>

**Adjusting Preferences In-App**

<div align="center">
  <img src="images/change-news-sources.png" alt="Change news sources preferences" width="800"/>
  <p><em>News-only preferences dialog opened from the account menu</em></p>
</div>

<div align="center">
  <img src="images/change-companies.png" alt="Change companies preferences" width="800"/>
  <p><em>Companies-only preferences dialog opened from the account menu</em></p>
</div>

**Change Password**

<div align="center">
  <img src="images/change-password.png" alt="Change password dialog" width="800"/>
  <p><em>In-app change password modal for secure updates</em></p>
</div>

### 🗺️ Roadmap

- Topic-based feeds (AI/ML, cybersecurity, startups, cloud, and more)
- Filtering by date range and importance
- Saved articles and reading history
- Custom watchlists beyond the default 10 companies
- Price alerts and richer stock analytics

---

## 🛠️ Tech Stack

### Backend
| Technology | Purpose |
|------------|---------|
| **FastAPI** | Python API |
| **SQLAlchemy** | ORM |
| **SQLite / PostgreSQL** | Local SQLite; PostgreSQL in production via `DATABASE_URL` |
| **yfinance** | Stock market data |
| **BeautifulSoup4 + lxml** | RSS parsing and article extraction |
| **Hugging Face API** | Daily fact generation |
| **bcrypt + python-jose** | Password hashing and JWT |
| **Schedule** | Background jobs (facts, news, stocks) |

### Frontend
| Technology | Purpose |
|------------|---------|
| **React 18** | UI |
| **TypeScript** | Type safety |
| **Styled Components** | CSS-in-JS |
| **Framer Motion** | Animations |
| **React Icons** | Icons |
| **Axios** | HTTP client |
| **react-hot-toast** | Toasts |

### Deploy
| Technology | Purpose |
|------------|---------|
| **GitHub Pages** | Hosted frontend (`https://pranavgautam.com/TechScope-Daily`) |
| **GitHub Actions** | Build and deploy on push to `main` |

---

## 📁 Project Structure

```
TechScope Daily/
├── backend/
│   ├── app/
│   │   ├── ai/
│   │   │   └── content_generator.py      # AI facts & news analysis
│   │   ├── api/
│   │   │   └── routes/
│   │   │       ├── auth.py              # Signup, login, current user, change password
│   │   │       ├── news.py              # News endpoints
│   │   │       ├── breaking_news.py     # Breaking news endpoints
│   │   │       ├── stocks.py            # Stock endpoints
│   │   │       └── facts.py             # Daily facts endpoints
│   │   ├── core/
│   │   │   ├── config.py                # Settings, CORS, DATABASE_URL
│   │   │   └── security.py              # bcrypt hashing & JWT helpers
│   │   ├── models/
│   │   │   └── database.py              # Models (User, News, BreakingNews, Stock, Fact)
│   │   └── services/
│   │       ├── news_service.py          # News queries
│   │       ├── breaking_news_service.py # RSS fetch from 10 sources
│   │       ├── stock_service.py         # yfinance updates
│   │       └── scheduler.py             # Daily/hourly background jobs
│   ├── main.py                          # FastAPI app (test user + scheduler on startup)
│   ├── create_test_user.py              # Optional one-off test user script
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header.tsx               # Nav, account menu, logout
│   │   │   ├── LoginPage.tsx            # Login & signup
│   │   │   ├── SlidingCards.tsx         # Card carousel
│   │   │   ├── NewsSection.tsx          # News cards
│   │   │   ├── StocksSection.tsx        # Stock cards
│   │   │   ├── FactsSection.tsx         # Fact card UI
│   │   │   ├── LoadingSpinner.tsx       # Loading screen with daily fact
│   │   │   ├── PreferencesModal.tsx     # News sources & companies
│   │   │   └── ChangePasswordModal.tsx  # Password change
│   │   ├── contexts/
│   │   │   └── AuthContext.tsx          # Auth state; talks to REACT_APP_API_URL
│   │   ├── App.tsx
│   │   ├── index.tsx
│   │   └── index.css
│   └── package.json
│
├── .github/workflows/deploy.yml          # GitHub Pages deploy
├── images/                               # README screenshots
├── LICENSE
├── README.md
└── setup.md
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.8+** - [Download](https://www.python.org/downloads/)
- **Node.js 16+** - [Download](https://nodejs.org/)
- **Git** - [Download](https://git-scm.com/)

### Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/pranavgautam9/TechScope-Daily.git
cd TechScope-Daily
```

#### 2. Backend Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

cd backend
pip install -r requirements.txt
```

Tables are created automatically on first run.

#### 3. Frontend Setup

```bash
cd frontend
npm install
```

#### 4. Environment Configuration

Create a `.env` file in the `backend` directory if you need production or custom settings. The app runs locally without API keys.

```env
# Local default (omit to use SQLite)
# DATABASE_URL=sqlite:///./techscope_daily.db

# Production (Render/Heroku-style postgres:// URLs are normalized automatically)
# DATABASE_URL=postgresql://user:password@host:5432/techscope

# JWT signing key — change this in production
SECRET_KEY=your-secret-key-here

# Extra browser origins (comma-separated). Localhost and pranavgautam.com are already allowed.
# BACKEND_CORS_ORIGINS=https://your-frontend.example

# Optional: not required (Hugging Face is used by default)
# OPENAI_API_KEY=your_openai_key_here

# Optional: not required (RSS feeds are used by default)
# NEWS_API_KEY=your_news_api_key_here

# Optional: not required (yfinance is used by default)
# ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key_here
```

For a production frontend build, set the backend URL:

```env
REACT_APP_API_URL=https://your-backend-host
```

In local development the frontend proxies API calls to `http://127.0.0.1:8000`.

---

## 🎮 Running the Application

### Start Backend Server

```bash
cd backend
uvicorn main:app --reload
```

The backend will be available at: **http://localhost:8000**

On startup it creates/repairs the test user, starts the scheduler, and runs an initial news/stocks/facts fetch.

### Start Frontend Development Server

```bash
cd frontend
npm start
```

The frontend will be available at: **http://localhost:3000**

### Access Points

- **Live App**: https://pranavgautam.com/TechScope-Daily
- **Local Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Health Check**: http://localhost:8000/health
- **Swagger**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Default Login / Test Account

- After both servers are running, open the frontend and wait for the loading screen.
- You will be redirected to the **Login / Signup** page.
- Create a new account or use:
  - Email: `testuser@gmail.com`
  - Password: `Password123!`
- Once logged in, switch between **News** and **Live Stocks**, update preferences from the account menu, and log out from the navbar.

---

## 🚢 Deployment

### Frontend (GitHub Pages)

Pushing to `main` runs [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml): it builds `frontend/` with Node 18 and deploys the `build` folder to GitHub Pages.

Set the GitHub Actions secret **`REACT_APP_API_URL`** to your hosted API so the production UI talks to the real backend instead of `localhost`.

You can also deploy from the frontend folder:

```bash
cd frontend
npm run deploy
```

`package.json` `homepage` is set to `https://pranavgautam.com/TechScope-Daily`.

### Backend

Host the FastAPI app (for example Render, Fly.io, or a VPS) with:

| Variable | Notes |
|----------|--------|
| `DATABASE_URL` | PostgreSQL connection string. `postgres://` is rewritten to `postgresql://`. |
| `SECRET_KEY` | Used to sign JWTs — do not leave the default in production. |
| `BACKEND_CORS_ORIGINS` | Extra allowed origins. `http://localhost:3000`, `https://pranavgautam.com`, and `https://www.pranavgautam.com` are included by default. |

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
4. **Commit your changes**
   ```bash
   git commit -m 'Add some amazing feature'
   ```
5. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
6. **Open a Pull Request**

### Development Guidelines

- Follow existing code style
- Add comments for complex logic
- Update documentation for new features
- Test your changes before submitting

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.
