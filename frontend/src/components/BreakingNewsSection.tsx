import React from 'react';
import styled, { keyframes } from 'styled-components';
import { motion } from 'framer-motion';
import { FiAlertTriangle, FiExternalLink, FiClock, FiTrendingUp } from 'react-icons/fi';

interface BreakingNewsCard {
  id: number;
  title: string;
  content: string;
  source: string;
  is_critical?: boolean;
  importance_score?: number;
  sentiment?: string;
  impact_level?: string;
}

interface BreakingNewsSectionProps {
  card: BreakingNewsCard;
}

const pulse = keyframes`
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.7;
  }
`;

const Card = styled(motion.div)<{ $isCritical: boolean }>`
  background: ${props => props.$isCritical 
    ? 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)' 
    : 'rgba(255, 255, 255, 0.95)'};
  border-radius: 20px;
  padding: 2rem;
  max-width: 800px;
  width: 90%;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  border: ${props => props.$isCritical ? '3px solid #dc2626' : '1px solid rgba(255, 255, 255, 0.2)'};
  animation: ${props => props.$isCritical ? `${pulse} 2s infinite` : 'none'};
`;

const CriticalBadge = styled.div`
  background: #dc2626;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 700;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
  animation: ${pulse} 1.5s infinite;
`;

const Header = styled.div`
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  margin-bottom: 1.5rem;
`;

const IconContainer = styled.div<{ $isCritical: boolean }>`
  width: 60px;
  height: 60px;
  background: ${props => props.$isCritical 
    ? 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)' 
    : 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)'};
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
`;

const HeaderText = styled.div`
  flex: 1;
`;

const Title = styled.h2<{ $isCritical: boolean }>`
  font-size: 1.8rem;
  font-weight: 700;
  color: ${props => props.$isCritical ? 'white' : '#333'};
  margin-bottom: 0.5rem;
  line-height: 1.2;
`;

const Subtitle = styled.div<{ $isCritical: boolean }>`
  color: ${props => props.$isCritical ? 'rgba(255, 255, 255, 0.8)' : '#666'};
  font-size: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
`;

const Content = styled.p<{ $isCritical: boolean }>`
  font-size: 1.1rem;
  color: ${props => props.$isCritical ? 'rgba(255, 255, 255, 0.9)' : '#555'};
  line-height: 1.7;
  margin-bottom: 1.5rem;
`;

const MetaInfo = styled.div<{ $isCritical: boolean }>`
  display: flex;
  align-items: center;
  justify-content: space-between;
  color: ${props => props.$isCritical ? 'rgba(255, 255, 255, 0.7)' : '#888'};
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

const ImpactIndicator = styled.div<{ $impact: string }>`
  background: ${props => {
    switch (props.$impact) {
      case 'high': return '#ef4444';
      case 'medium': return '#f59e0b';
      case 'low': return '#10b981';
      default: return '#6b7280';
    }
  }};
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 600;
`;

const SentimentBadge = styled.div<{ $sentiment: string }>`
  background: ${props => {
    switch (props.$sentiment) {
      case 'positive': return '#10b981';
      case 'negative': return '#ef4444';
      case 'neutral': return '#6b7280';
      default: return '#6b7280';
    }
  }};
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 600;
`;

const ReadMoreButton = styled(motion.button)<{ $isCritical: boolean }>`
  background: ${props => props.$isCritical 
    ? 'rgba(255, 255, 255, 0.2)' 
    : 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)'};
  color: ${props => props.$isCritical ? 'white' : 'white'};
  border: ${props => props.$isCritical ? '1px solid rgba(255, 255, 255, 0.3)' : 'none'};
  padding: 0.75rem 1.5rem;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 1rem;
`;

const BreakingNewsSection: React.FC<BreakingNewsSectionProps> = ({ card }) => {
  const isCritical = card.is_critical || false;
  const impactLevel = card.impact_level || 'medium';
  const sentiment = card.sentiment || 'neutral';
  const importanceScore = card.importance_score || 0.5;

  return (
    <Card
      $isCritical={isCritical}
      initial={{ scale: 0.9, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      {isCritical && (
        <CriticalBadge>
          <FiAlertTriangle size={16} />
          CRITICAL BREAKING NEWS
        </CriticalBadge>
      )}
      
      <Header>
        <IconContainer $isCritical={isCritical}>
          <FiAlertTriangle size={24} />
        </IconContainer>
        <HeaderText>
          <Title $isCritical={isCritical}>{card.title}</Title>
          <Subtitle $isCritical={isCritical}>
            <FiClock size={16} />
            Breaking News • {card.source}
          </Subtitle>
        </HeaderText>
      </Header>
      
      <Content $isCritical={isCritical}>{card.content}</Content>
      
      <MetaInfo $isCritical={isCritical}>
        <MetaLeft>
          <MetaItem>
            <FiTrendingUp size={14} />
            Impact: {Math.round(importanceScore * 100)}%
          </MetaItem>
          <ImpactIndicator $impact={impactLevel}>
            {impactLevel.toUpperCase()} IMPACT
          </ImpactIndicator>
          <SentimentBadge $sentiment={sentiment}>
            {sentiment.toUpperCase()}
          </SentimentBadge>
        </MetaLeft>
      </MetaInfo>
      
      <ReadMoreButton
        $isCritical={isCritical}
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
      >
        <FiExternalLink size={16} />
        Read Full Story
      </ReadMoreButton>
    </Card>
  );
};

export default BreakingNewsSection; 