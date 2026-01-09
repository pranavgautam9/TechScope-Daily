import React, { useState, useEffect, useCallback } from 'react';
import styled from 'styled-components';
import { motion, AnimatePresence } from 'framer-motion';
import { FiChevronLeft, FiChevronRight, FiPause, FiPlay } from 'react-icons/fi';
import axios from 'axios';

import NewsSection from './NewsSection';
import StocksSection from './StocksSection';

interface SlidingCardsProps {
  activeSection: 'news' | 'stocks';
}

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Helper function to strip HTML tags from content
const stripHtml = (html: string): string => {
  if (!html) return '';
  // Create a temporary div element
  const tmp = document.createElement('div');
  tmp.innerHTML = html;
  // Get text content and clean it up
  let text = tmp.textContent || tmp.innerText || '';
  // Remove extra whitespace and newlines
  text = text.replace(/\s+/g, ' ').trim();
  // Remove HTML entities
  text = text.replace(/&nbsp;/g, ' ');
  text = text.replace(/&amp;/g, '&');
  text = text.replace(/&lt;/g, '<');
  text = text.replace(/&gt;/g, '>');
  text = text.replace(/&quot;/g, '"');
  text = text.replace(/&#39;/g, "'");
  return text;
};

const CardsContainer = styled.div`
  position: relative;
  width: 100%;
  height: calc(100vh - 140px);
  min-height: 600px;
  overflow: hidden;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
`;

const CardWrapper = styled(motion.div)`
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  box-sizing: border-box;
`;

const NavigationControls = styled.div`
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 1rem;
  z-index: 10;
`;

const ControlButton = styled(motion.button)`
  width: 50px;
  height: 50px;
  border: none;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
  
  &:hover {
    background: rgba(255, 255, 255, 0.3);
    transform: scale(1.1);
  }
`;

const ProgressBar = styled.div`
  position: absolute;
  bottom: 0;
  left: 0;
  height: 4px;
  background: rgba(255, 255, 255, 0.3);
  width: 100%;
`;

const Progress = styled(motion.div)`
  height: 100%;
  background: linear-gradient(90deg, #667eea, #764ba2);
  border-radius: 2px;
`;

const Card = styled(motion.div)`
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  padding: 2.5rem;
  width: 95%;
  max-width: 95%;
  height: calc(100% - 80px);
  max-height: calc(100vh - 220px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  display: flex;
  flex-direction: column;
  overflow-y: auto;
`;

interface NewsCard {
  id: number;
  title: string;
  content: string;
}

interface StockCard {
  id: number;
  symbol: string;
  price: number;
  change: string;
}

function isNewsCard(card: any): card is NewsCard {
  return 'title' in card && 'content' in card;
}

function isStockCard(card: any): card is StockCard {
  return 'symbol' in card && 'price' in card && 'change' in card;
}

const SlidingCards: React.FC<SlidingCardsProps> = ({ activeSection }) => {
  const [currentCardIndex, setCurrentCardIndex] = useState(0);
  const [isAutoPlaying, setIsAutoPlaying] = useState(true);
  const [progress, setProgress] = useState(0);
  const [newsCards, setNewsCards] = useState<any[]>([]);
  const [stockCards, setStockCards] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  // Fetch news from backend
  useEffect(() => {
    const fetchNews = async () => {
      try {
        setIsLoading(true);
        // Fetch breaking news first (most important)
        const breakingResponse = await axios.get(`${API_BASE_URL}/api/breaking-news/trending`);
        const breakingNews = breakingResponse.data.data || [];
        
        // Fetch regular news
        const newsResponse = await axios.get(`${API_BASE_URL}/api/news/latest`);
        const regularNews = newsResponse.data.data || [];
        
        // Combine and format news
        const formattedNews = [
          ...breakingNews.map((item: any) => ({
            id: item.id,
            title: stripHtml(item.title || ''),
            content: stripHtml(item.content || item.title || ''),
            source: item.source || 'Tech News',
            is_breaking: true,
            is_critical: item.is_critical || false,
            importance_score: item.importance_score || 0.7,
            impact_level: item.impact_level || 'medium',
            sentiment: item.sentiment || 'neutral',
            url: item.url
          })),
          ...regularNews.map((item: any) => ({
            id: item.id,
            title: stripHtml(item.title || ''),
            content: stripHtml(item.content || item.title || ''),
            source: item.source || 'Tech News',
            is_breaking: false,
            is_critical: false,
            importance_score: item.importance_score || 0.5,
            impact_level: 'medium',
            sentiment: 'neutral',
            url: item.url
          }))
        ];
        
        // If no news from API, use fallback
        if (formattedNews.length === 0) {
          formattedNews.push({
            id: 1,
            title: 'Welcome to TechScope Daily',
            content: 'Fetching the latest tech news for you...',
            source: 'TechScope Daily',
            is_breaking: false,
            is_critical: false,
            importance_score: 0.5
          });
        }
        
        setNewsCards(formattedNews);
      } catch (error) {
        console.error('Error fetching news:', error);
        // Fallback news
        setNewsCards([{
          id: 1,
          title: 'Welcome to TechScope Daily',
          content: 'Unable to fetch news. Please check your connection.',
          source: 'TechScope Daily',
          is_breaking: false,
          is_critical: false,
          importance_score: 0.5
        }]);
      } finally {
        setIsLoading(false);
      }
    };

    if (activeSection === 'news') {
      fetchNews();
    }
  }, [activeSection]);

  // Fetch stocks from backend
  useEffect(() => {
    const fetchStocks = async () => {
      try {
        const response = await axios.get(`${API_BASE_URL}/api/stocks/live`);
        const stocks = response.data.data || [];
        
        const formattedStocks = stocks.map((stock: any) => ({
          id: stock.symbol,
          symbol: stock.symbol,
          price: stock.current_price || 0,
          change: `${stock.change_percent >= 0 ? '+' : ''}${stock.change_percent?.toFixed(2) || 0}%`,
          company_name: stock.company_name
        }));
        
        if (formattedStocks.length === 0) {
          formattedStocks.push({
            id: 'AAPL',
            symbol: 'AAPL',
            price: 0,
            change: '+0%',
            company_name: 'Loading...'
          });
        }
        
        setStockCards(formattedStocks);
      } catch (error) {
        console.error('Error fetching stocks:', error);
        setStockCards([{
          id: 'AAPL',
          symbol: 'AAPL',
          price: 0,
          change: '+0%',
          company_name: 'Unable to load'
        }]);
      }
    };

    if (activeSection === 'stocks') {
      fetchStocks();
    }
  }, [activeSection]);

  const cards = activeSection === 'news' ? newsCards : stockCards;
  const totalCards = cards.length;

  const nextCard = useCallback(() => {
    setCurrentCardIndex((prev) => (prev + 1) % totalCards);
    setProgress(0);
  }, [totalCards]);

  const prevCard = useCallback(() => {
    setCurrentCardIndex((prev) => (prev - 1 + totalCards) % totalCards);
    setProgress(0);
  }, [totalCards]);

  const toggleAutoPlay = () => {
    setIsAutoPlaying(!isAutoPlaying);
    setProgress(0);
  };

  // Auto-advance cards
  useEffect(() => {
    if (!isAutoPlaying) return;

    const interval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 100) {
          nextCard();
          return 0;
        }
        return prev + 2; // Progress every 50ms for 5 second total
      });
    }, 100);

    return () => clearInterval(interval);
  }, [isAutoPlaying, nextCard]);

  // Reset when section changes
  useEffect(() => {
    setCurrentCardIndex(0);
    setProgress(0);
  }, [activeSection, cards]);

  const renderCard = () => {
    if (isLoading) {
      return (
        <div style={{ 
          textAlign: 'center', 
          padding: '2rem',
          color: 'white',
          fontSize: '1.2rem'
        }}>
          <p>Loading {activeSection}...</p>
        </div>
      );
    }

    if (cards.length === 0) {
      return (
        <div style={{ 
          textAlign: 'center', 
          padding: '2rem',
          color: 'white',
          fontSize: '1.2rem'
        }}>
          <p>No {activeSection} available at the moment.</p>
        </div>
      );
    }

    const card = cards[currentCardIndex];
    if (!card) {
      return (
        <div style={{ 
          textAlign: 'center', 
          padding: '2rem',
          color: 'white',
          fontSize: '1.2rem'
        }}>
          <p>No card data available.</p>
        </div>
      );
    }

    switch (activeSection) {
      case 'news':
        if (isNewsCard(card)) return <NewsSection card={card} />;
        break;
      case 'stocks':
        if (isStockCard(card)) return <StocksSection card={card} />;
        break;

      default:
        return null;
    }
    
    return null;
  };

  return (
    <CardsContainer>
      <AnimatePresence mode="wait">
        <CardWrapper
          key={`${activeSection}-${currentCardIndex}`}
          initial={{ opacity: 0, x: 300 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: -300 }}
          transition={{ duration: 0.5, ease: "easeInOut" }}
        >
          {renderCard()}
        </CardWrapper>
      </AnimatePresence>

      <NavigationControls>
        <ControlButton
          onClick={prevCard}
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
        >
          <FiChevronLeft size={20} />
        </ControlButton>

        <ControlButton
          onClick={toggleAutoPlay}
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
        >
          {isAutoPlaying ? <FiPause size={20} /> : <FiPlay size={20} />}
        </ControlButton>

        <ControlButton
          onClick={nextCard}
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
        >
          <FiChevronRight size={20} />
        </ControlButton>
      </NavigationControls>

      <ProgressBar>
        <Progress
          initial={{ width: 0 }}
          animate={{ width: `${progress}%` }}
          transition={{ duration: 0.1 }}
        />
      </ProgressBar>
    </CardsContainer>
  );
};

export default SlidingCards; 