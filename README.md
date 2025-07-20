# TechScope Daily - AI-Powered Tech News Platform

A modern, AI-powered tech news platform that delivers personalized daily tech insights, breaking news, market updates, and fascinating tech facts.

## 🚀 Features

- **Real-time News**: Latest tech news from multiple sources
- **AI-Generated Content**: Personalized insights and summaries
- **Unified News Feed**: Latest tech news with breaking news integration
- **Stock Market Integration**: Real-time stock data and analysis
- **Daily Tech Facts**: Interesting tech facts displayed on the loading screen
- **Deep Dive Content**: In-depth analysis and trending topics

## 🏗️ Architecture

```
TechScope Daily/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── api/         # API routes
│   │   ├── core/        # Configuration
│   │   ├── models/      # Database models
│   │   ├── services/    # Business logic
│   │   └── ai/          # AI content generation
│   └── main.py          # FastAPI app entry point
├── frontend/            # React TypeScript frontend
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── styles/      # CSS and styling
│   │   └── App.tsx      # Main app component
│   └── package.json
└── README.md
```

## 🛠️ Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: Database ORM
- **OpenAI API**: AI content generation
- **News API**: Real-time news data
- **Alpha Vantage**: Stock market data

### Frontend
- **React 18**: UI framework
- **TypeScript**: Type safety
- **Styled Components**: CSS-in-JS styling
- **Framer Motion**: Animations
- **React Icons**: Icon library

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd techscope-daily
   ```

2. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On CMD: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   ```

4. **Environment Configuration**
   Create `.env` files in both backend and frontend directories with your API keys.

## 🚀 Running the Application

1. **Start Backend**
   ```bash
   cd backend
   uvicorn main:app --reload
   ```

2. **Start Frontend**
   ```bash
   cd frontend
   npm start
   ```

3. **Access the Application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## 📝 API Endpoints

- `GET /api/news` - Get latest tech news
- `GET /api/breaking-news` - Get breaking news alerts
- `GET /api/stocks` - Get stock market data
- `GET /api/facts/daily` - Get daily tech fact

## 🎯 Key Features

### Navigation
- **News**: Latest tech news with breaking news integration
- **Live Stocks**: Real-time stock market data and analysis

### Daily Facts
- **Loading Screen**: Displays a unique tech fact each day during app startup
- **5-Second Display**: Extended loading time to allow users to read the fact
- **Daily Rotation**: New fact generated automatically each day at midnight
- **AI-Generated**: Facts are generated using AI for variety and relevance

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License. 