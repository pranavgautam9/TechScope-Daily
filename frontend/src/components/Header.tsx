import React, { useState } from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { FiFileText, FiTrendingUp, FiLogOut, FiUser, FiChevronDown, FiSettings, FiLock } from 'react-icons/fi';
import { useAuth } from '../contexts/AuthContext';
import toast from 'react-hot-toast';

interface HeaderProps {
  activeSection: 'news' | 'stocks';
  setActiveSection: (section: 'news' | 'stocks') => void;
  onOpenNewsPreferences: () => void;
  onOpenStockPreferences: () => void;
  onOpenPasswordModal: () => void;
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
  max-width: 1400px;
  width: 100%;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  
  @media (max-width: 768px) {
    padding: 0 10px;
  }
`;

const Logo = styled.div`
  font-size: 1.5rem;
  font-weight: 700;
  color: white;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-shrink: 0;
`;

const Navigation = styled.nav`
  display: flex;
  gap: 1rem;
  flex-shrink: 0;
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

const LogoutButton = styled(motion.button)`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 12px;
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
  margin-left: 0.5rem;
  
  &:hover {
    background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
    transform: translateY(-2px);
  }
`;

const AccountContainer = styled.div`
  position: relative;
  display: flex;
  align-items: center;
`;

const AccountButton = styled(motion.button)`
  display: flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.6rem 1rem;
  border: none;
  border-radius: 999px;
  background: rgba(15, 23, 42, 0.55);
  color: white;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.25s ease;
  backdrop-filter: blur(14px);
  max-width: 220px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;

  &:hover {
    background: rgba(15, 23, 42, 0.8);
    transform: translateY(-1px);
  }
`;

const AccountEmail = styled.span`
  max-width: 140px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  text-align: left;
`;

const AccountDropdown = styled(motion.div)`
  position: absolute;
  top: 110%;
  right: 0;
  min-width: 260px;
  background: rgba(15, 23, 42, 0.96);
  border-radius: 18px;
  box-shadow: 0 22px 60px rgba(15, 23, 42, 0.7);
  padding: 14px 14px 10px;
  color: white;
  backdrop-filter: blur(20px);
  border: 1px solid rgba(148, 163, 184, 0.4);
  z-index: 50;
`;

const AccountHeader = styled.div`
  display: flex;
  align-items: center;
  gap: 0.6rem;
  margin-bottom: 10px;
`;

const AccountDetails = styled.div`
  display: flex;
  flex-direction: column;
`;

const AccountLabel = styled.span`
  font-size: 0.75rem;
  color: rgba(209, 213, 219, 0.9);
`;

const AccountEmailFull = styled.span`
  font-size: 0.85rem;
  font-weight: 500;
`;

const AccountActions = styled.div`
  display: flex;
  flex-direction: column;
  margin-top: 6px;
`;

const AccountActionButton = styled.button`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 7px 8px;
  border: none;
  border-radius: 10px;
  background: transparent;
  color: rgba(229, 231, 235, 0.96);
  font-size: 0.8rem;
  cursor: pointer;
  transition: background 0.18s ease, color 0.18s ease, transform 0.1s ease;

  &:hover {
    background: rgba(31, 41, 55, 0.95);
    color: #e5e7eb;
    transform: translateY(-0.5px);
  }
`;

const Header: React.FC<HeaderProps> = ({
  activeSection,
  setActiveSection,
  onOpenNewsPreferences,
  onOpenStockPreferences,
  onOpenPasswordModal,
}) => {
  const { logout, user } = useAuth();
  const [isAccountOpen, setIsAccountOpen] = useState(false);
  const tabs = [
    { id: 'news', label: 'News', icon: FiFileText },
    { id: 'stocks', label: 'Live Stocks', icon: FiTrendingUp },
  ] as const;

  const handleLogout = () => {
    logout();
    toast.success('Logged out successfully');
  };

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
          <AccountContainer>
            <AccountButton
              type="button"
              onClick={() => setIsAccountOpen((open) => !open)}
              whileHover={{ scale: 1.03 }}
              whileTap={{ scale: 0.97 }}
            >
              <FiUser size={16} />
              <AccountEmail>{user?.email ?? 'Account'}</AccountEmail>
              <FiChevronDown size={14} />
            </AccountButton>
            {isAccountOpen && (
              <AccountDropdown
                initial={{ opacity: 0, y: -6, scale: 0.98 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                exit={{ opacity: 0, y: -4, scale: 0.98 }}
              >
                <AccountHeader>
                  <FiSettings size={16} />
                  <AccountDetails>
                    <AccountLabel>Signed in as</AccountLabel>
                    <AccountEmailFull>{user?.email}</AccountEmailFull>
                  </AccountDetails>
                </AccountHeader>
                <AccountActions>
                  <AccountActionButton
                    type="button"
                    onClick={() => {
                      onOpenNewsPreferences();
                      setIsAccountOpen(false);
                    }}
                  >
                    <FiFileText size={14} />
                    Change news sources
                  </AccountActionButton>
                  <AccountActionButton
                    type="button"
                    onClick={() => {
                      onOpenStockPreferences();
                      setIsAccountOpen(false);
                    }}
                  >
                    <FiTrendingUp size={14} />
                    Change companies
                  </AccountActionButton>
                  <AccountActionButton
                    type="button"
                    onClick={() => {
                      onOpenPasswordModal();
                      setIsAccountOpen(false);
                    }}
                  >
                    <FiLock size={14} />
                    Change password
                  </AccountActionButton>
                </AccountActions>
              </AccountDropdown>
            )}
          </AccountContainer>
          <LogoutButton
            onClick={handleLogout}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <FiLogOut size={18} />
            Logout
          </LogoutButton>
        </Navigation>
      </HeaderContent>
    </HeaderContainer>
  );
};

export default Header; 