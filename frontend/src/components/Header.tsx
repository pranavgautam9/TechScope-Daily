import React from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { FiFileText, FiTrendingUp } from 'react-icons/fi';

interface HeaderProps {
  activeSection: 'news' | 'stocks';
  setActiveSection: (section: 'news' | 'stocks') => void;
}

const HeaderContainer = styled.header`
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  padding: 1rem 0;
`;

const HeaderContent = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
`;

const Logo = styled.div`
  font-size: 1.5rem;
  font-weight: 700;
  color: white;
  display: flex;
  align-items: center;
  gap: 0.5rem;
`;

const Navigation = styled.nav`
  display: flex;
  gap: 1rem;
`;

const NavTab = styled(motion.button)<{ $active: boolean }>`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 12px;
  background: ${props => props.$active ? 'rgba(255, 255, 255, 0.2)' : 'transparent'};
  color: white;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
  
  &:hover {
    background: rgba(255, 255, 255, 0.15);
    transform: translateY(-2px);
  }
`;

const Header: React.FC<HeaderProps> = ({ activeSection, setActiveSection }) => {
  const tabs = [
    { id: 'news', label: 'News', icon: FiFileText },
    { id: 'stocks', label: 'Live Stocks', icon: FiTrendingUp },
  ] as const;

  return (
    <HeaderContainer>
      <HeaderContent>
        <Logo>
          <FiFileText size={24} />
          TechScope Daily
        </Logo>
        
        <Navigation>
          {tabs.map((tab) => {
            const Icon = tab.icon;
            const isActive = activeSection === tab.id;
            
            return (
              <NavTab
                key={tab.id}
                $active={isActive}
                onClick={() => setActiveSection(tab.id)}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                <Icon size={18} />
                {tab.label}
              </NavTab>
            );
          })}
        </Navigation>
      </HeaderContent>
    </HeaderContainer>
  );
};

export default Header; 