import React from 'react';
import styled, { keyframes, css } from 'styled-components';
import { motion } from 'framer-motion';
import { FiExternalLink, FiClock, FiAlertTriangle, FiTrendingUp } from 'react-icons/fi';

interface NewsCard {
  id: number;
  title: string;
  content: string;
  source?: string;
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
  padding: 2rem;
  max-width: 800px;
  width: 90%;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  border: ${props => {
    if (props.$isCritical) return '3px solid #dc2626';
    if (props.$isBreaking) return '2px solid #d97706';
    return '1px solid rgba(255, 255, 255, 0.2)';
  }};
  ${props => props.$isCritical && css`
    animation: ${pulse} 2s infinite;
  `}
`;

const BreakingBadge = styled.div<{ $isCritical: boolean }>`
  background: ${props => props.$isCritical ? '#dc2626' : '#d97706'};
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 700;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
  ${props => props.$isCritical && css`
    animation: ${pulse} 1.5s infinite;
  `}
`;

const Header = styled.div`
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  margin-bottom: 1.5rem;
`;

const IconContainer = styled.div<{ $isBreaking: boolean; $isCritical: boolean }>`
  width: 60px;
  height: 60px;
  background: ${props => {
    if (props.$isCritical) return 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)';
    if (props.$isBreaking) return 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)';
    return 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
  }};
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

const Subtitle = styled.div<{ $isBreaking: boolean; $isCritical: boolean }>`
  color: ${props => {
    if (props.$isCritical) return 'rgba(255, 255, 255, 0.8)';
    if (props.$isBreaking) return 'rgba(255, 255, 255, 0.8)';
    return '#666';
  }};
  font-size: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
`;

const Content = styled.p<{ $isBreaking: boolean; $isCritical: boolean }>`
  font-size: 1.1rem;
  color: ${props => {
    if (props.$isCritical || props.$isBreaking) return 'rgba(255, 255, 255, 0.9)';
    return '#555';
  }};
  line-height: 1.7;
  margin-bottom: 1.5rem;
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
  const impactLevel = card.impact_level || 'medium';
  const sentiment = card.sentiment || 'neutral';
  const importanceScore = card.importance_score || 0.5;
  const source = card.source || 'Tech News';

  return (
    <Card
      $isBreaking={isBreaking}
      $isCritical={isCritical}
      initial={{ scale: 0.9, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      {(isBreaking || isCritical) && (
        <BreakingBadge $isCritical={isCritical}>
          <FiAlertTriangle size={16} />
          {isCritical ? 'CRITICAL BREAKING NEWS' : 'BREAKING NEWS'}
        </BreakingBadge>
      )}
      
      <Header>
        <IconContainer $isBreaking={isBreaking} $isCritical={isCritical}>
          {isBreaking || isCritical ? (
            <FiAlertTriangle size={24} />
          ) : (
            <FiExternalLink size={24} />
          )}
        </IconContainer>
        <HeaderText>
          <Title $isBreaking={isBreaking} $isCritical={isCritical}>{card.title}</Title>
          <Subtitle $isBreaking={isBreaking} $isCritical={isCritical}>
            <FiClock size={16} />
            {isBreaking || isCritical ? 'Breaking News' : 'Just now'} • {source}
          </Subtitle>
        </HeaderText>
      </Header>
      
      <Content $isBreaking={isBreaking} $isCritical={isCritical}>{card.content}</Content>
      
      <MetaInfo $isBreaking={isBreaking} $isCritical={isCritical}>
        <MetaLeft>
          <MetaItem>
            <FiTrendingUp size={14} />
            Impact: {Math.round(importanceScore * 100)}%
          </MetaItem>
          {(isBreaking || isCritical) && (
            <>
              <ImpactIndicator $impact={impactLevel}>
                {impactLevel.toUpperCase()} IMPACT
              </ImpactIndicator>
              <SentimentBadge $sentiment={sentiment}>
                {sentiment.toUpperCase()}
              </SentimentBadge>
            </>
          )}
        </MetaLeft>
      </MetaInfo>
      
      <ReadMoreButton
        $isBreaking={isBreaking}
        $isCritical={isCritical}
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
      >
        <FiExternalLink size={16} />
        Read Full {isBreaking || isCritical ? 'Story' : 'Article'}
      </ReadMoreButton>
    </Card>
  );
};

export default NewsSection; 