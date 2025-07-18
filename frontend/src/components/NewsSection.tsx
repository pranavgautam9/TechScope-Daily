import React from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { FiExternalLink, FiClock } from 'react-icons/fi';

interface NewsCard {
  id: number;
  title: string;
  content: string;
}

interface NewsSectionProps {
  card: NewsCard;
}

const Card = styled(motion.div)`
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  padding: 2rem;
  max-width: 800px;
  width: 90%;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
`;

const Title = styled.h2`
  font-size: 2rem;
  font-weight: 700;
  color: #333;
  margin-bottom: 1rem;
  line-height: 1.2;
`;

const Content = styled.p`
  font-size: 1.1rem;
  color: #666;
  line-height: 1.6;
  margin-bottom: 1.5rem;
`;

const MetaInfo = styled.div`
  display: flex;
  align-items: center;
  gap: 1rem;
  color: #888;
  font-size: 0.9rem;
`;

const MetaItem = styled.div`
  display: flex;
  align-items: center;
  gap: 0.5rem;
`;

const ReadMoreButton = styled(motion.button)`
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 1rem;
`;

const NewsSection: React.FC<NewsSectionProps> = ({ card }) => {
  return (
    <Card
      initial={{ scale: 0.9, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      <Title>{card.title}</Title>
      <Content>{card.content}</Content>
      
      <MetaInfo>
        <MetaItem>
          <FiClock size={16} />
          Just now
        </MetaItem>
        <MetaItem>
          <FiExternalLink size={16} />
          Tech News
        </MetaItem>
      </MetaInfo>
      
      <ReadMoreButton
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
      >
        <FiExternalLink size={16} />
        Read Full Article
      </ReadMoreButton>
    </Card>
  );
};

export default NewsSection; 