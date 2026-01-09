import React from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { FiTrendingUp, FiTrendingDown } from 'react-icons/fi';

interface StockCard {
  id: number | string;
  symbol: string;
  price: number;
  change: number;
  change_percent: number;
  company_name?: string;
  volume?: number;
  market_cap?: number;
}

interface StocksSectionProps {
  card: StockCard;
}

const Card = styled(motion.div)`
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(240, 235, 255, 0.95) 100%);
  border-radius: 20px;
  padding: 2.5rem;
  width: 100%;
  max-width: 900px;
  height: auto;
  min-height: 400px;
  max-height: calc(100vh - 200px);
  box-shadow: 0 20px 40px rgba(102, 126, 234, 0.2);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(102, 126, 234, 0.2);
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  position: relative;
`;

const Header = styled.div`
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.5rem;
`;

const Symbol = styled.h2`
  font-size: 2.5rem;
  font-weight: 700;
  color: #333;
`;

const PriceContainer = styled.div`
  text-align: right;
`;

const Price = styled.div`
  font-size: 2rem;
  font-weight: 700;
  color: #333;
  display: flex;
  align-items: center;
  gap: 0.5rem;
`;

const Change = styled.div<{ $isPositive: boolean }>`
  font-size: 1.2rem;
  font-weight: 600;
  color: ${props => props.$isPositive ? '#10b981' : '#ef4444'};
  display: flex;
  align-items: center;
  gap: 0.5rem;
`;

const StatsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  margin-top: 1.5rem;
`;

const StatItem = styled.div`
  background: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(10px);
  padding: 1rem;
  border-radius: 12px;
  text-align: center;
  border: 1px solid rgba(102, 126, 234, 0.1);
`;

const StatLabel = styled.div`
  font-size: 0.9rem;
  color: #6b7280;
  margin-bottom: 0.5rem;
`;

const StatValue = styled.div`
  font-size: 1.2rem;
  font-weight: 600;
  color: #333;
`;

const StocksSection: React.FC<StocksSectionProps> = ({ card }) => {
  const isPositive = card.change_percent >= 0;
  const changePercent = card.change_percent || 0;
  const price = card.price || 0;
  const volume = card.volume || 0;
  const marketCap = card.market_cap || 0;
  
  // Format large numbers
  const formatNumber = (num: number): string => {
    if (num >= 1e12) return `$${(num / 1e12).toFixed(2)}T`;
    if (num >= 1e9) return `$${(num / 1e9).toFixed(2)}B`;
    if (num >= 1e6) return `$${(num / 1e6).toFixed(2)}M`;
    if (num >= 1e3) return `$${(num / 1e3).toFixed(2)}K`;
    return `$${num.toFixed(2)}`;
  };
  
  const formatVolume = (vol: number): string => {
    if (vol >= 1e9) return `${(vol / 1e9).toFixed(2)}B`;
    if (vol >= 1e6) return `${(vol / 1e6).toFixed(2)}M`;
    if (vol >= 1e3) return `${(vol / 1e3).toFixed(2)}K`;
    return vol.toString();
  };

  return (
    <Card
      initial={{ scale: 0.9, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      <Header>
        <div>
          <Symbol>{card.symbol}</Symbol>
          {card.company_name && (
            <div style={{ fontSize: '1rem', color: '#666', marginTop: '0.5rem' }}>
              {card.company_name}
            </div>
          )}
        </div>
        <PriceContainer>
          <Price>
            ${price.toFixed(2)}
          </Price>
          <Change $isPositive={isPositive}>
            {isPositive ? <FiTrendingUp size={20} /> : <FiTrendingDown size={20} />}
            {isPositive ? '+' : ''}{changePercent.toFixed(2)}%
          </Change>
        </PriceContainer>
      </Header>

      <StatsGrid>
        <StatItem>
          <StatLabel>Change</StatLabel>
          <StatValue style={{ color: isPositive ? '#10b981' : '#ef4444' }}>
            {isPositive ? '+' : ''}${card.change?.toFixed(2) || '0.00'}
          </StatValue>
        </StatItem>
        <StatItem>
          <StatLabel>Volume</StatLabel>
          <StatValue>{formatVolume(volume)}</StatValue>
        </StatItem>
        <StatItem>
          <StatLabel>Market Cap</StatLabel>
          <StatValue>{marketCap > 0 ? formatNumber(marketCap) : 'N/A'}</StatValue>
        </StatItem>
        <StatItem>
          <StatLabel>Change %</StatLabel>
          <StatValue style={{ color: isPositive ? '#10b981' : '#ef4444' }}>
            {isPositive ? '+' : ''}{changePercent.toFixed(2)}%
          </StatValue>
        </StatItem>
      </StatsGrid>
    </Card>
  );
};

export default StocksSection; 