import React, { useState, useEffect, useCallback } from 'react';
import styled from 'styled-components';
import { motion, AnimatePresence } from 'framer-motion';
import { FiChevronLeft, FiChevronRight, FiPause, FiPlay } from 'react-icons/fi';

import NewsSection from './NewsSection';
import StocksSection from './StocksSection';

interface SlidingCardsProps {
  activeSection: 'news' | 'stocks';
}

const CardsContainer = styled.div`
  position: relative;
  width: 100%;
  height: 600px;
  overflow: hidden;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2);
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

  // Mock data for demonstration
  const getCardsForSection = (section: string) => {
    switch (section) {
      case 'news':
        return [
          { 
            id: 1, 
            title: 'CRITICAL: Major Cybersecurity Breach Detected', 
            content: 'A massive cybersecurity breach has been detected affecting millions of users worldwide. Security experts are working around the clock to contain the threat...',
            is_breaking: true,
            is_critical: true,
            importance_score: 0.95,
            impact_level: 'high',
            sentiment: 'negative',
            source: 'Security Alert'
          },
          { 
            id: 2, 
            title: 'BREAKING: Apple Announces Revolutionary AI Integration', 
            content: 'Apple has just announced a groundbreaking AI integration that will transform how users interact with their devices. The new system promises unprecedented personalization...',
            is_breaking: true,
            is_critical: false,
            importance_score: 0.85,
            impact_level: 'high',
            sentiment: 'positive',
            source: 'Tech News'
          },
          { 
            id: 3, 
            title: 'Latest AI Breakthrough', 
            content: 'OpenAI releases GPT-5 with unprecedented capabilities that could revolutionize the AI industry...',
            is_breaking: false,
            is_critical: false,
            importance_score: 0.75,
            source: 'AI News'
          },
          { 
            id: 4, 
            title: 'Tech Giant Merger', 
            content: 'Major tech companies announce strategic partnership that could reshape the industry landscape...',
            is_breaking: false,
            is_critical: false,
            importance_score: 0.65,
            source: 'Business News'
          },
          { 
            id: 5, 
            title: 'Quantum Computing Milestone', 
            content: 'IBM achieves quantum advantage in real-world applications, marking a significant breakthrough...',
            is_breaking: false,
            is_critical: false,
            importance_score: 0.70,
            source: 'Research News'
          },
        ];
      case 'stocks':
        return [
          { id: 1, symbol: 'AAPL', price: 150.25, change: '+2.5%' },
          { id: 2, symbol: 'MSFT', price: 320.10, change: '+1.8%' },
          { id: 3, symbol: 'GOOGL', price: 2750.50, change: '-0.5%' },
        ];

      default:
        return [];
    }
  };

  const cards = getCardsForSection(activeSection);
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
  }, [activeSection]);

  const renderCard = () => {
    const card = cards[currentCardIndex];
    if (!card) return null;

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