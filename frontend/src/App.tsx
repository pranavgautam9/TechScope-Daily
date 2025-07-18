import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import styled from 'styled-components';
import { motion, AnimatePresence } from 'framer-motion';
import { Toaster } from 'react-hot-toast';

import Header from './components/Header';
import SlidingCards from './components/SlidingCards';
import NewsSection from './components/NewsSection';
import FactsSection from './components/FactsSection';
import StocksSection from './components/StocksSection';
import WeeklySection from './components/WeeklySection';
import LoadingSpinner from './components/LoadingSpinner';

const AppContainer = styled.div`
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
`;

const MainContent = styled.main`
  max-width: 1200px;
  margin: 0 auto;
  padding-top: 80px;
`;

const App: React.FC = () => {
  const [isLoading, setIsLoading] = useState(true);
  const [activeSection, setActiveSection] = useState<'news' | 'facts' | 'stocks' | 'weekly' | 'breaking'>('news');

  useEffect(() => {
    // Simulate loading time
    const timer = setTimeout(() => {
      setIsLoading(false);
    }, 2000);

    return () => clearTimeout(timer);
  }, []);

  if (isLoading) {
    return <LoadingSpinner />;
  }

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
        
        <Header activeSection={activeSection} setActiveSection={setActiveSection} />
        
        <MainContent>
          <AnimatePresence mode="wait">
            <motion.div
              key={activeSection}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.5 }}
            >
              <SlidingCards activeSection={activeSection} />
            </motion.div>
          </AnimatePresence>
        </MainContent>
      </AppContainer>
    </Router>
  );
};

export default App; 