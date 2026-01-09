# 📰 TechScope Daily

<div align="center">

**AI-Powered Tech News Platform | Your Daily Tech Digest**

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-20232A?style=flat&logo=react&logoColor=61DAFB)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=flat&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)

*Stay informed with the latest tech news, stock updates, and AI-generated insights*

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Configuration](#-configuration)
- [API Documentation](#-api-documentation)
- [Daily Updates](#-daily-updates)
- [Development](#-development)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

**TechScope Daily** is a modern, AI-powered tech news platform that delivers personalized daily tech insights, breaking news, market updates, and fascinating tech facts. Built with FastAPI and React, it provides a beautiful, responsive interface for staying up-to-date with the tech world.

### Key Highlights

- ✨ **Daily Updates**: Fresh content every day - news, stocks, and facts
- 🤖 **AI-Powered**: Free AI integration for fact generation and content analysis
- 📊 **Stock Tracking**: Real-time data for major tech companies
- 🎨 **Modern UI**: Beautiful glassmorphism design with smooth animations
- 🔄 **Auto-Rotating Cards**: Sliding card interface for easy browsing

---

## ✨ Features

### 📰 News Section
- **Daily Tech News**: Curated news from Google News and Wired.com
- **Breaking News Alerts**: Real-time breaking news with importance scoring
- **AI Analysis**: Automatic sentiment and impact analysis
- **Content Extraction**: Full article content previews
- **Source Filtering**: Focused on quality tech sources

### 📈 Stocks Section
- **Major Tech Stocks**: Track 10 major tech companies (AAPL, MSFT, GOOGL, AMZN, TSLA, META, NVDA, NFLX, ADBE, CRM)
- **Daily Updates**: Stock data refreshed daily at market open
- **Real-time Metrics**: Price, change, volume, and market cap
- **Visual Indicators**: Color-coded gains/losses
- **Formatted Data**: Easy-to-read number formatting (B, M, K)

### 🧠 Daily Facts
- **AI-Generated Facts**: Unique tech facts generated daily
- **Loading Screen Display**: Facts shown during app startup
- **Daily Rotation**: New fact every day at midnight
- **Free AI Integration**: Uses Hugging Face API (no API key required)
- **Fallback Database**: 30+ facts per category for reliability

### 🎨 User Interface
- **Glassmorphism Design**: Modern frosted glass aesthetic
- **Purple Gradient Theme**: Beautiful purple-to-pink gradient background
- **Smooth Animations**: Framer Motion powered transitions
- **Responsive Layout**: Works on desktop, tablet, and mobile
- **Auto-Play Cards**: Automatic card rotation with manual controls

---

## 🛠️ Tech Stack

### Backend
| Technology | Purpose |
|------------|---------|
| **FastAPI** | Modern Python web framework |
| **SQLAlchemy** | Database ORM |
| **SQLite** | Lightweight database |
| **yfinance** | Stock market data |
| **BeautifulSoup4** | Web scraping for news |
| **Hugging Face API** | Free AI for fact generation |
| **Schedule** | Background task scheduling |

### Frontend
| Technology | Purpose |
|------------|---------|
| **React 18** | UI framework |
| **TypeScript** | Type safety |
| **Styled Components** | CSS-in-JS styling |
| **Framer Motion** | Animations |
| **React Icons** | Icon library |
| **Axios** | HTTP client |

---

## 📁 Project Structure

```
TechScope Daily/
├── backend/
│   ├── app/
│   │   ├── ai/
│   │   │   └── content_generator.py    # AI fact generation & news analysis
│   │   ├── api/
│   │   │   └── routes/
│   │   │       ├── news.py            # News endpoints
│   │   │       ├── breaking_news.py   # Breaking news endpoints
│   │   │       ├── stocks.py          # Stock endpoints
│   │   │       └── facts.py            # Daily facts endpoints
│   │   ├── core/
│   │   │   └── config.py              # Configuration & settings
│   │   ├── models/
│   │   │   └── database.py             # Database models
│   │   └── services/
│   │       ├── news_service.py         # News business logic
│   │       ├── breaking_news_service.py # Breaking news fetching
│   │       ├── stock_service.py        # Stock data management
│   │       └── scheduler.py            # Daily task scheduler
│   ├── main.py                         # FastAPI app entry point
│   ├── requirements.txt                 # Python dependencies
│   └── techscope_daily.db              # SQLite database
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header.tsx              # Navigation header
│   │   │   ├── SlidingCards.tsx        # Card carousel container
│   │   │   ├── NewsSection.tsx         # News card component
│   │   │   ├── StocksSection.tsx       # Stock card component
│   │   │   └── LoadingSpinner.tsx      # Loading screen with facts
│   │   ├── App.tsx                     # Main app component
│   │   ├── index.tsx                   # React entry point
│   │   └── index.css                   # Global styles
│   ├── package.json                    # Node.js dependencies
│   └── build/                          # Production build
│
├── README.md                            # This file
└── setup.md                             # Detailed setup guide
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
git clone <repository-url>
cd "TechScope Daily"
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

# Navigate to backend
cd backend

# Install dependencies
pip install -r requirements.txt

# Initialize database (creates tables automatically on first run)
# Database will be created automatically when you start the server
```

#### 3. Frontend Setup

```bash
# Navigate to frontend (from project root)
cd frontend

# Install dependencies
npm install
```

#### 4. Environment Configuration

Create a `.env` file in the `backend` directory (optional - works without API keys):

```env
# Optional: For enhanced AI features (uses free Hugging Face by default)
OPENAI_API_KEY=your_openai_key_here

# Optional: Not currently required (using Google News RSS & Wired.com)
NEWS_API_KEY=your_news_api_key_here

# Optional: Not currently required (using yfinance)
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key_here
```

> **Note**: The app works without API keys! It uses free services (Hugging Face AI, Google News RSS, Wired.com RSS, yfinance) by default.

---

## 🎮 Running the Application

### Start Backend Server

```bash
cd backend
uvicorn main:app --reload
```

The backend will be available at: **http://localhost:8000**

### Start Frontend Development Server

```bash
cd frontend
npm start
```

The frontend will be available at: **http://localhost:3000**

### Access Points

- **Frontend Application**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation (Swagger)**: http://localhost:8000/docs
- **Alternative API Docs (ReDoc)**: http://localhost:8000/redoc

---

## ⚙️ Configuration

### Daily Scheduler

The application automatically runs background tasks:

- **00:00** - Generate new daily fact
- **06:00** - Fetch news from Google News & Wired.com
- **09:00** - Update stock data (market open)
- **12:00** - Fetch news updates
- **Every 2 hours** - Fetch breaking news during the day

### News Sources

Currently configured to fetch from:
- **Google News RSS** (tech news, filtered for Wired.com)
- **Wired.com RSS** (direct feed)

### Tracked Stocks

The following tech companies are tracked:
- Apple (AAPL)
- Microsoft (MSFT)
- Alphabet/Google (GOOGL)
- Amazon (AMZN)
- Tesla (TSLA)
- Meta (META)
- NVIDIA (NVDA)
- Netflix (NFLX)
- Adobe (ADBE)
- Salesforce (CRM)

---

## 📡 API Documentation

### News Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/news` | GET | Get daily tech news |
| `/api/news/latest` | GET | Get most recent news items |
| `/api/news/important` | GET | Get important news for weekly section |
| `/api/breaking-news` | GET | Get breaking news items |
| `/api/breaking-news/trending` | GET | Get trending breaking news |
| `/api/breaking-news/critical` | GET | Get critical breaking news |
| `/api/breaking-news/fetch-google-news` | POST | Manually fetch Google News |
| `/api/breaking-news/fetch-wired-news` | POST | Manually fetch Wired.com news |

### Stocks Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/stocks` | GET | Get all tracked stocks |
| `/api/stocks/daily` | GET | Get daily stocks for feed |
| `/api/stocks/live` | GET | Fetch live stock data and update DB |
| `/api/stocks/{symbol}` | GET | Get specific stock by symbol |
| `/api/stocks/top-gainers` | GET | Get top gaining stocks |
| `/api/stocks/top-losers` | GET | Get top losing stocks |
| `/api/stocks/market-summary` | GET | Get market summary statistics |

### Facts Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/facts/daily` | GET | Get today's daily fact |
| `/api/facts` | GET | Get multiple facts |
| `/api/facts/generate` | POST | Generate a new fact |
| `/api/facts/random` | GET | Get a random fact |

---

## 🔄 Daily Updates

### How It Works

1. **Daily Facts**: Generated at midnight using free Hugging Face AI or fallback database
2. **News Updates**: Fetched from Google News and Wired.com at 6 AM and throughout the day
3. **Stock Updates**: Refreshed daily at 9 AM (market open) using Yahoo Finance
4. **Automatic Analysis**: News is analyzed for importance, sentiment, and impact

### Data Storage

- All data is stored in SQLite database (`techscope_daily.db`)
- News articles are deduplicated by URL
- Stocks are updated in-place
- Facts are stored with daily rotation

---

## 🛠️ Development

### Backend Development

```bash
cd backend

# Run with auto-reload
uvicorn main:app --reload

# Run on custom port
uvicorn main:app --reload --port 8001
```

### Frontend Development

```bash
cd frontend

# Start development server
npm start

# Build for production
npm run build

# Run tests
npm test
```

### Database Management

The database is automatically created and managed by SQLAlchemy. Tables are created on first run.

To reset the database:
```bash
# Delete the database file
rm backend/techscope_daily.db

# Restart the server (tables will be recreated)
```

---

## 🎨 Customization

### Change News Sources

Edit `backend/app/services/breaking_news_service.py`:
- Modify `fetch_google_news()` for Google News queries
- Modify `fetch_wired_news()` for Wired.com feed

### Add/Remove Stocks

Edit `backend/app/services/stock_service.py`:
- Update the `tech_companies` list in `__init__()`

### Customize AI Prompts

Edit `backend/app/ai/content_generator.py`:
- Modify `generate_tech_fact()` for fact generation
- Modify analysis functions for news scoring

### Styling

Edit `frontend/src/index.css` for global styles or individual component files for specific styling.

---

## 🐛 Troubleshooting

### Common Issues

**Port Already in Use**
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:8000 | xargs kill -9
```

**Module Not Found**
```bash
# Reinstall backend dependencies
cd backend
pip install -r requirements.txt

# Reinstall frontend dependencies
cd frontend
npm install
```

**Database Errors**
- Ensure SQLite is installed
- Check file permissions for `techscope_daily.db`
- Delete database file to reset (data will be regenerated)

**API Connection Issues**
- Verify backend is running on port 8000
- Check CORS settings in `backend/main.py`
- Ensure frontend proxy is set correctly in `package.json`

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

---

## 🙏 Acknowledgments

- **Google News** - For RSS feed access
- **Wired.com** - For quality tech journalism
- **Hugging Face** - For free AI inference API
- **Yahoo Finance** - For stock market data via yfinance
- **FastAPI** - For the amazing Python framework
- **React** - For the powerful UI library

---

<div align="center">

**Made with ❤️ for tech enthusiasts**

[Report Bug](https://github.com/yourusername/techscope-daily/issues) · [Request Feature](https://github.com/yourusername/techscope-daily/issues) · [Documentation](setup.md)

</div>
