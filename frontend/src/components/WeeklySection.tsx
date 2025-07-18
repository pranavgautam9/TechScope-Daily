import React from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';

interface WeeklyCard {
  id: number;
  title: string;
  content: string;
}

interface WeeklySectionProps {
  card: WeeklyCard;
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

const Header = styled.div`
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #f3f4f6;
`;

const IconContainer = styled.div`
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
`;

const HeaderText = styled.div`
  flex: 1;
`;

const Title = styled.h2`
  font-size: 1.8rem;
  font-weight: 700;
  color: #333;
  margin-bottom: 0.5rem;
`;

const Subtitle = styled.div`
  color: #666;
  font-size: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
`;

const Content = styled.p`
  font-size: 1.1rem;
  color: #555;
  line-height: 1.7;
  margin-bottom: 1.5rem;
`;

const Actions = styled.div`
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
`;

const ActionButton = styled(motion.button)`
  background: rgba(102, 126, 234, 0.1);
  color: #667eea;
  border: 1px solid rgba(102, 126, 234, 0.2);
  padding: 0.75rem 1.5rem;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
  
  &:hover {
    background: rgba(102, 126, 234, 0.2);
    transform: translateY(-2px);
  }
`;

const WeeklySection: React.FC<WeeklySectionProps> = ({ card }) => {
  return (
    <Card
      initial={{ scale: 0.9, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      <Header>
        <IconContainer>
          {/* FiCalendar removed */}
        </IconContainer>
        <HeaderText>
          <Title>{card.title}</Title>
          <Subtitle>
            {/* FiCalendar removed */}
            Weekly Curated Content
          </Subtitle>
        </HeaderText>
      </Header>
      
      <Content>{card.content}</Content>
      
      <Actions>
        <ActionButton
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          {/* FiBookmark removed */}
          Save
        </ActionButton>
        
        <ActionButton
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          {/* FiShare2 removed */}
          Share
        </ActionButton>
      </Actions>
    </Card>
  );
};

export default WeeklySection; 