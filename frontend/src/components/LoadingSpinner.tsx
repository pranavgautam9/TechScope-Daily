import React, { useState, useEffect } from 'react';
import styled, { keyframes } from 'styled-components';
import { motion } from 'framer-motion';
import { FiFileText, FiZap } from 'react-icons/fi';

const spin = keyframes`
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
`;

const LoadingContainer = styled.div`
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: white;
`;

const Logo = styled(motion.div)`
  font-size: 3rem;
  font-weight: 700;
  margin-bottom: 2rem;
  display: flex;
  align-items: center;
  gap: 1rem;
`;

const Spinner = styled.div`
  width: 60px;
  height: 60px;
  border: 4px solid rgba(255, 255, 255, 0.3);
  border-top: 4px solid white;
  border-radius: 50%;
  animation: ${spin} 1s linear infinite;
  margin-bottom: 2rem;
`;

const FactContainer = styled(motion.div)`
  max-width: 600px;
  text-align: center;
  margin-bottom: 2rem;
`;

const FactTitle = styled.div`
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
`;

const FactText = styled.div`
  font-size: 1.1rem;
  line-height: 1.6;
  opacity: 0.9;
  font-style: italic;
  margin-bottom: 1rem;
`;

const LoadingText = styled(motion.div)`
  font-size: 1rem;
  font-weight: 500;
  opacity: 0.8;
`;

interface DailyFact {
  fact_text: string;
  category: string;
}

const LoadingSpinner: React.FC = () => {
  const [dailyFact, setDailyFact] = useState<DailyFact | null>(null);
  const [isLoadingFact, setIsLoadingFact] = useState(true);

  useEffect(() => {
    // Fetch daily fact from backend
    const fetchDailyFact = async () => {
      try {
        setIsLoadingFact(true);
        const response = await fetch('http://localhost:8000/api/facts/daily');
        if (response.ok) {
          const data = await response.json();
          setDailyFact(data.data);
        } else {
          throw new Error('Failed to fetch fact');
        }
      } catch (error) {
        console.error('Failed to fetch daily fact:', error);
        // Fallback fact if API fails
        setDailyFact({
          fact_text: "The first computer bug was an actual bug - a moth found in the Harvard Mark II computer in 1947.",
          category: "Computer Science"
        });
      } finally {
        setIsLoadingFact(false);
      }
    };

    fetchDailyFact();
  }, []);

  return (
    <LoadingContainer>
      <Logo
        initial={{ scale: 0, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ duration: 0.8, ease: "easeOut" }}
      >
        <FiFileText size={48} />
        TechScope Daily
      </Logo>
      
      <Spinner />
      
      {!isLoadingFact && dailyFact && (
        <FactContainer
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.8, duration: 0.5 }}
        >
          <FactTitle>
            <FiZap size={20} />
            Tech Fact of the Day
          </FactTitle>
          <FactText>"{dailyFact.fact_text}"</FactText>
        </FactContainer>
      )}
      
      <LoadingText
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 1.2, duration: 0.5 }}
      >
        Loading your daily tech digest...
      </LoadingText>
    </LoadingContainer>
  );
};

export default LoadingSpinner; 