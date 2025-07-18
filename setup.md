# 🚀 TechScope Daily Setup Guide

Welcome to your AI-powered TechScope Daily! This guide will help you get everything up and running.

## 📋 Prerequisites

Before you begin, make sure you have the following installed:

- **Python 3.8+** - [Download here](https://www.python.org/downloads/)
- **Node.js 16+** - [Download here](https://nodejs.org/)
- **Git** - [Download here](https://git-scm.com/)

## 🔑 Required API Keys

You'll need the following API keys to run the application:

1. **OpenAI API Key** - [Get here](https://platform.openai.com/api-keys)
   - Used for AI-generated content and summaries
   
2. **News API Key** - [Get here](https://newsapi.org/)
   - Used for fetching real-time news
   
3. **Alpha Vantage API Key** - [Get here](https://www.alphavantage.co/support/#api-key)
   - Used for stock market data

## 🚀 Quick Start

### 1. Clone and Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd techscope-daily

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 2. Backend Setup

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Create .env file
echo "OPENAI_API_KEY=your_openai_key_here" > .env
echo "NEWS_API_KEY=your_news_api_key_here" >> .env
echo "ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key_here" >> .env

# Initialize database
python -c "from app.models.database import Base, engine; Base.metadata.create_all(bind=engine)"

# Start the backend server
uvicorn main:app --reload
```

### 3. Frontend Setup

```bash
# Open a new terminal
cd frontend

# Install dependencies
npm install

# Start the frontend development server
npm start
```

## 🌐 Access Your Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📁 Project Structure

```
techscope-daily/
├── backend/
│   ├── app/
│   │   ├── ai/              # AI content generation
│   │   ├── api/             # API routes
│   │   ├── core/            # Configuration
│   │   ├── models/          # Database models
│   │   └── services/        # Business logic
│   ├── main.py              # FastAPI entry point
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── App.tsx          # Main app component
│   │   └── index.tsx        # Entry point
│   └── package.json         # Node.js dependencies
└── README.md
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the `backend` directory:

```env
OPENAI_API_KEY=your_openai_api_key
NEWS_API_KEY=your_news_api_key
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key
```

### Customization

- **News Sources**: Edit `backend/app/services/news_service.py` to modify news sources
- **Stock Symbols**: Update `backend/app/services/stock_service.py` to change tracked stocks
- **AI Prompts**: Modify `backend/app/ai/content_generator.py` to customize AI-generated content
- **Styling**: Edit `frontend/src/index.css` for global styles

## 🚀 Features Overview

Your AI-powered TechScope Daily is now running! The interface features:

- **Breaking News**: Real-time tech news updates
- **Stock Dashboard**: Live stock data for major tech companies
- **AI Facts**: Daily computer science and tech facts
- **Weekly Digest**: Curated weekly content
- **Responsive Design**: Works on desktop, tablet, and mobile

## 🐛 Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Kill process on port 8000
   lsof -ti:8000 | xargs kill -9
   ```

2. **Module not found errors**
   ```bash
   # Reinstall dependencies
   pip install -r requirements.txt
   ```

3. **API key errors**
   - Verify your API keys are correct
   - Check that the `.env` file is in the backend directory
   - Ensure no extra spaces in the `.env` file

### Getting Help

If you encounter issues:

1. Check the console for error messages
2. Verify all API keys are valid
3. Ensure all dependencies are installed
4. Check that both backend and frontend are running

## 🎉 Next Steps

- Customize the news sources and stock symbols
- Modify the AI prompts for different content styles
- Add your own branding and styling
- Deploy to production (Heroku, Vercel, etc.)

---

**Happy coding! 🚀** 