import React from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { FiZap, FiBook } from 'react-icons/fi';

interface FactCard {
  id: number;
  fact: string;
}

interface FactsSectionProps {
  card: FactCard;
}

const Card = styled(motion.div)`
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  padding: 2rem;
  max-width: 800px;
  width: 90%;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  text-align: center;
`;

const IconContainer = styled.div`
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1.5rem;
  color: white;
`;

const Title = styled.h2`
  font-size: 1.5rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
`;

const FactText = styled.p`
  font-size: 1.3rem;
  color: #555;
  line-height: 1.6;
  margin-bottom: 1.5rem;
  font-style: italic;
`;

const Source = styled.div`
  color: #888;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
`;

const Category = styled.span`
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
  margin-top: 1rem;
  display: inline-block;
`;

const FactsSection: React.FC<FactsSectionProps> = ({ card }) => {
  return (
    <Card
      initial={{ scale: 0.9, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      <IconContainer>
        <FiZap size={32} />
      </IconContainer>
      
      <Title>
        <FiBook size={20} />
        Tech Fact of the Day
      </Title>
      
      <FactText>"{card.fact}"</FactText>
      
      <Source>
        <FiBook size={14} />
        AI Generated
      </Source>
      
      <Category>Computer Science</Category>
    </Card>
  );
};

export default FactsSection; 