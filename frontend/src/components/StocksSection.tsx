import React from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { FiTrendingUp, FiTrendingDown } from 'react-icons/fi';

interface StockCard {
  id: number;
  symbol: string;
  price: number;
  change: string;
}

interface StocksSectionProps {
  card: StockCard;
}

const Card = styled(motion.div)`
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  padding: 2.5rem;
  width: 100%;
  max-width: 900px;
  height: auto;
  min-height: 400px;
  max-height: calc(100vh - 200px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
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

const ChartPlaceholder = styled.div`
  height: 200px;
  background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #6b7280;
  font-size: 1.1rem;
  margin: 1.5rem 0;
`;

const StatsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  margin-top: 1.5rem;
`;

const StatItem = styled.div`
  background: #f9fafb;
  padding: 1rem;
  border-radius: 12px;
  text-align: center;
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
  const isPositive = card.change.startsWith('+');
  const changeValue = parseFloat(card.change.replace(/[+\-%]/g, ''));

  return (
    <Card
      initial={{ scale: 0.9, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      <Header>
        <Symbol>{card.symbol}</Symbol>
        <PriceContainer>
          <Price>
            {card.price.toFixed(2)}
          </Price>
          <Change $isPositive={isPositive}>
            {isPositive ? <FiTrendingUp size={20} /> : <FiTrendingDown size={20} />}
            {card.change}
          </Change>
        </PriceContainer>
      </Header>

      <ChartPlaceholder>
        Live Chart Data
      </ChartPlaceholder>

      <StatsGrid>
        <StatItem>
          <StatLabel>Volume</StatLabel>
          <StatValue>2.5M</StatValue>
        </StatItem>
        <StatItem>
          <StatLabel>Market Cap</StatLabel>
          <StatValue>$2.5T</StatValue>
        </StatItem>
        <StatItem>
          <StatLabel>52W High</StatLabel>
          <StatValue>$182.94</StatValue>
        </StatItem>
        <StatItem>
          <StatLabel>52W Low</StatLabel>
          <StatValue>$124.17</StatValue>
        </StatItem>
      </StatsGrid>
    </Card>
  );
};

export default StocksSection; 