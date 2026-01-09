import React from 'react';
import styled, { keyframes, css } from 'styled-components';
import { motion } from 'framer-motion';
import { FiExternalLink, FiTrendingUp } from 'react-icons/fi';

interface NewsCard {
  id: number;
  title: string;
  content: string;
  source?: string;
  url?: string;
  is_breaking?: boolean;
  is_critical?: boolean;
  importance_score?: number;
  sentiment?: string;
  impact_level?: string;
}

interface NewsSectionProps {
  card: NewsCard;
}

const pulse = keyframes`
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.7;
  }
`;

const Card = styled(motion.div)<{ $isBreaking: boolean; $isCritical: boolean }>`
  background: ${props => {
    if (props.$isCritical) return 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)';
    if (props.$isBreaking) return 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)';
    return 'rgba(255, 255, 255, 0.95)';
  }};
  border-radius: 20px;
  padding: 2.5rem;
  width: 100%;
  max-width: 900px;
  height: auto;
  min-height: 400px;
  max-height: calc(100vh - 200px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  border: ${props => {
    if (props.$isCritical) return '3px solid #dc2626';
    if (props.$isBreaking) return '2px solid #d97706';
    return '1px solid rgba(255, 255, 255, 0.2)';
  }};
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  position: relative;
  ${props => props.$isCritical && css`
    animation: ${pulse} 2s infinite;
  `}
`;

const Header = styled.div`
  display: flex;
  align-items: flex-start;
  margin-bottom: 1.5rem;
`;

const HeaderText = styled.div`
  flex: 1;
  width: 100%;
`;

const Title = styled.h2<{ $isBreaking: boolean; $isCritical: boolean }>`
  font-size: 1.8rem;
  font-weight: 700;
  color: ${props => {
    if (props.$isCritical || props.$isBreaking) return 'white';
    return '#333';
  }};
  margin-bottom: 0.5rem;
  line-height: 1.2;
`;


const Content = styled.p<{ $isBreaking: boolean; $isCritical: boolean }>`
  font-size: 1.1rem;
  color: ${props => {
    if (props.$isCritical || props.$isBreaking) return 'rgba(255, 255, 255, 0.9)';
    return '#555';
  }};
  line-height: 1.8;
  margin-bottom: 1.5rem;
  flex: 1;
  overflow-y: auto;
  word-wrap: break-word;
  text-align: justify;
`;

const MetaInfo = styled.div<{ $isBreaking: boolean; $isCritical: boolean }>`
  display: flex;
  align-items: center;
  justify-content: space-between;
  color: ${props => {
    if (props.$isCritical || props.$isBreaking) return 'rgba(255, 255, 255, 0.7)';
    return '#888';
  }};
  font-size: 0.9rem;
  margin-bottom: 1rem;
`;

const MetaLeft = styled.div`
  display: flex;
  align-items: center;
  gap: 1rem;
`;

const MetaItem = styled.div`
  display: flex;
  align-items: center;
  gap: 0.5rem;
`;

const ReadMoreButton = styled(motion.button)<{ $isBreaking: boolean; $isCritical: boolean }>`
  background: ${props => {
    if (props.$isCritical) return 'rgba(255, 255, 255, 0.2)';
    if (props.$isBreaking) return 'rgba(255, 255, 255, 0.2)';
    return 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
  }};
  color: white;
  border: ${props => {
    if (props.$isCritical || props.$isBreaking) return '1px solid rgba(255, 255, 255, 0.3)';
    return 'none';
  }};
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
  const isBreaking = card.is_breaking || false;
  const isCritical = card.is_critical || false;
  const importanceScore = card.importance_score || 0.5;
  
  // Get content and ensure it's different from title, truncate if needed
  let displayContent = card.content || '';
  const title = card.title || '';
  
  // Clean up content - remove title if it appears at the start
  if (displayContent.toLowerCase().startsWith(title.toLowerCase())) {
    displayContent = displayContent.substring(title.length).trim();
    // Remove common separators
    displayContent = displayContent.replace(/^[-•|:]\s*/, '').trim();
  }
  
  // If content is same as title or very similar, use placeholder
  if (displayContent.toLowerCase().trim() === title.toLowerCase().trim() || 
      displayContent.length < 100) {
    displayContent = 'This article provides detailed information about the topic. Click "Read Full Story" to view the complete article and get all the details.';
  }
  
  // Truncate content to reasonable length (max 800 chars for better readability)
  const maxLength = 800;
  if (displayContent.length > maxLength) {
    // Try to truncate at a sentence boundary
    const truncated = displayContent.substring(0, maxLength);
    const lastPeriod = truncated.lastIndexOf('.');
    const lastExclamation = truncated.lastIndexOf('!');
    const lastQuestion = truncated.lastIndexOf('?');
    const lastSentence = Math.max(lastPeriod, lastExclamation, lastQuestion);
    
    if (lastSentence > maxLength * 0.7) {
      displayContent = truncated.substring(0, lastSentence + 1);
    } else {
      displayContent = truncated.trim() + '...';
    }
  }

  return (
    <Card
      $isBreaking={isBreaking}
      $isCritical={isCritical}
      initial={{ scale: 0.9, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      <Header>
        <HeaderText>
          <Title $isBreaking={isBreaking} $isCritical={isCritical}>{title}</Title>
        </HeaderText>
      </Header>
      
      <Content $isBreaking={isBreaking} $isCritical={isCritical}>{displayContent}</Content>
      
      <MetaInfo $isBreaking={isBreaking} $isCritical={isCritical}>
        <MetaLeft>
          <MetaItem>
            <FiTrendingUp size={14} />
            Impact: {Math.round(importanceScore * 100)}%
          </MetaItem>
        </MetaLeft>
      </MetaInfo>
      
      {card.url ? (
        <ReadMoreButton
          $isBreaking={isBreaking}
          $isCritical={isCritical}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={() => window.open(card.url, '_blank')}
        >
          <FiExternalLink size={16} />
          Read Full {isBreaking || isCritical ? 'Story' : 'Article'}
        </ReadMoreButton>
      ) : (
        <ReadMoreButton
          $isBreaking={isBreaking}
          $isCritical={isCritical}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          disabled
          style={{ opacity: 0.5, cursor: 'not-allowed' }}
        >
          <FiExternalLink size={16} />
          Read Full {isBreaking || isCritical ? 'Story' : 'Article'}
        </ReadMoreButton>
      )}
    </Card>
  );
};

export default NewsSection; 