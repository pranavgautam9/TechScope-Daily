import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import styled from 'styled-components';
import { motion, AnimatePresence } from 'framer-motion';
import { Toaster } from 'react-hot-toast';

import Header from './components/Header';
import SlidingCards from './components/SlidingCards';
import LoadingSpinner from './components/LoadingSpinner';
import LoginPage from './components/LoginPage';
import { useAuth } from './contexts/AuthContext';
import PreferencesModal from './components/PreferencesModal';
import ChangePasswordModal from './components/ChangePasswordModal';

const AppContainer = styled.div`
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 10px;
`;

const MainContent = styled.main`
  max-width: 1400px;
  width: 100%;
  margin: 0 auto;
  padding-top: 80px;
  padding-bottom: 20px;
`;

const App: React.FC = () => {
  const [isLoading, setIsLoading] = useState(true);
  const [activeSection, setActiveSection] = useState<'news' | 'stocks'>('news');
  const { isAuthenticated, isLoading: authLoading, user } = useAuth();
  const [selectedNewsSources, setSelectedNewsSources] = useState<string[]>([]);
  const [selectedStockSymbols, setSelectedStockSymbols] = useState<string[]>([]);
  const [showPreferences, setShowPreferences] = useState(false);
  const [preferencesMode, setPreferencesMode] = useState<'both' | 'news' | 'stocks'>('both');
  const [showPasswordModal, setShowPasswordModal] = useState(false);

  useEffect(() => {
    // Simulate loading time - increased to 5 seconds for fact reading
    const timer = setTimeout(() => {
      setIsLoading(false);
    }, 5000);

    return () => clearTimeout(timer);
  }, []);

  // Load saved preferences when user becomes authenticated
  useEffect(() => {
    if (!isAuthenticated || !user) {
      return;
    }
    const storageKey = `techscope_prefs_${user.id}`;
    const stored = localStorage.getItem(storageKey);
    if (stored) {
      try {
        const parsed = JSON.parse(stored) as {
          newsSources?: string[];
          stockSymbols?: string[];
        };
        setSelectedNewsSources(parsed.newsSources || []);
        setSelectedStockSymbols(parsed.stockSymbols || []);
      } catch {
        setSelectedNewsSources([]);
        setSelectedStockSymbols([]);
      }
      // Preferences already exist – do not auto-open modal on login
      setShowPreferences(false);
      return;
    }

    // No saved prefs yet – start with empty arrays and prompt user once
    setSelectedNewsSources([]);
    setSelectedStockSymbols([]);
    setPreferencesMode('both');
    setShowPreferences(true);
  }, [isAuthenticated, user]);

  // Show loading spinner while app is loading or auth is being checked
  if (isLoading || authLoading) {
    return <LoadingSpinner />;
  }

  // Show login page if not authenticated
  if (!isAuthenticated) {
    return (
      <>
        <Toaster 
          position="top-right"
          toastOptions={{
            duration: 4000,
            style: {
              background: 'rgba(255, 255, 255, 0.9)',
              backdropFilter: 'blur(10px)',
              border: '1px solid rgba(255, 255, 255, 0.2)',
              borderRadius: '12px',
            },
          }}
        />
        <LoginPage />
      </>
    );
  }

  const handleSavePreferences = (newsSources: string[], stockSymbols: string[]) => {
    if (!user) return;
    setSelectedNewsSources(newsSources);
    setSelectedStockSymbols(stockSymbols);
    const storageKey = `techscope_prefs_${user.id}`;
    localStorage.setItem(
      storageKey,
      JSON.stringify({ newsSources, stockSymbols })
    );
    setShowPreferences(false);
  };

  // Show main app if authenticated
  return (
    <Router>
      <AppContainer>
        <Toaster 
          position="top-right"
          toastOptions={{
            duration: 4000,
            style: {
              background: 'rgba(255, 255, 255, 0.9)',
              backdropFilter: 'blur(10px)',
              border: '1px solid rgba(255, 255, 255, 0.2)',
              borderRadius: '12px',
            },
          }}
        />
        
        <Header
          activeSection={activeSection}
          setActiveSection={setActiveSection}
          onOpenNewsPreferences={() => {
            setPreferencesMode('news');
            setShowPreferences(true);
          }}
          onOpenStockPreferences={() => {
            setPreferencesMode('stocks');
            setShowPreferences(true);
          }}
          onOpenPasswordModal={() => setShowPasswordModal(true)}
        />
        
        <MainContent>
          <PreferencesModal
            isOpen={showPreferences}
            initialNewsSources={selectedNewsSources}
            initialStockSymbols={selectedStockSymbols}
            onSave={handleSavePreferences}
            mode={preferencesMode}
          />
          <ChangePasswordModal
            isOpen={showPasswordModal}
            onClose={() => setShowPasswordModal(false)}
          />
          <AnimatePresence mode="wait">
            <motion.div
              key={activeSection}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.5 }}
            >
              <SlidingCards
                activeSection={activeSection}
                selectedNewsSources={selectedNewsSources}
                selectedStockSymbols={selectedStockSymbols}
              />
            </motion.div>
          </AnimatePresence>
        </MainContent>
      </AppContainer>
    </Router>
  );
};

export default App; 