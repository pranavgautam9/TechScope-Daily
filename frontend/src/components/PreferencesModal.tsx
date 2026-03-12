import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { motion, AnimatePresence } from 'framer-motion';

type PreferencesMode = 'both' | 'news' | 'stocks';

interface PreferencesModalProps {
  isOpen: boolean;
  initialNewsSources: string[];
  initialStockSymbols: string[];
  onSave: (newsSources: string[], stockSymbols: string[]) => void;
  mode?: PreferencesMode;
}

// Internal representation values MUST match backend `source` and stock `symbol` fields
const AVAILABLE_NEWS_SOURCES: { id: string; label: string }[] = [
  { id: 'google_news', label: 'Google News (Tech)' },
  { id: 'wired.com', label: 'Wired' },
  { id: 'techcrunch.com', label: 'TechCrunch' },
  { id: 'theverge.com', label: 'The Verge' },
  { id: 'arstechnica.com', label: 'Ars Technica' },
  { id: 'engadget.com', label: 'Engadget' },
  { id: 'technologyreview.com', label: 'MIT Technology Review' },
  { id: 'cnet.com', label: 'CNET' },
  { id: 'venturebeat.com', label: 'VentureBeat' },
  { id: 'techrepublic.com', label: 'TechRepublic' },
];

const AVAILABLE_STOCK_SYMBOLS: { id: string; label: string }[] = [
  { id: 'AAPL', label: 'Apple (AAPL)' },
  { id: 'MSFT', label: 'Microsoft (MSFT)' },
  { id: 'GOOGL', label: 'Alphabet (GOOGL)' },
  { id: 'AMZN', label: 'Amazon (AMZN)' },
  { id: 'TSLA', label: 'Tesla (TSLA)' },
  { id: 'META', label: 'Meta (META)' },
  { id: 'NVDA', label: 'NVIDIA (NVDA)' },
  { id: 'NFLX', label: 'Netflix (NFLX)' },
  { id: 'ADBE', label: 'Adobe (ADBE)' },
  { id: 'CRM', label: 'Salesforce (CRM)' },
];

const Backdrop = styled(motion.div)`
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.65);
  backdrop-filter: blur(16px);
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding-top: 90px; /* leave room for top nav */
  padding-bottom: 32px;
  box-sizing: border-box;
  overflow-y: auto;
  z-index: 40;
`;

const ModalCard = styled(motion.div)`
  background: rgba(255, 255, 255, 0.97);
  border-radius: 24px;
  box-shadow: 0 30px 80px rgba(15, 23, 42, 0.4);
  padding: 32px 32px 24px;
  width: 100%;
  max-width: 720px;
  display: flex;
  flex-direction: column;
  gap: 20px;
`;

const Title = styled.h2`
  font-size: 1.7rem;
  font-weight: 700;
  color: #111827;
  margin: 0 0 4px;
`;

const Subtitle = styled.p`
  font-size: 0.95rem;
  color: #6b7280;
  margin: 0;
`;

const SectionsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 18px;
  margin-top: 12px;
`;

const Section = styled.div`
  background: rgba(249, 250, 251, 0.9);
  border-radius: 18px;
  padding: 16px 16px 10px;
  border: 1px solid rgba(209, 213, 219, 0.8);
`;

const SectionTitle = styled.h3`
  font-size: 0.95rem;
  font-weight: 600;
  color: #111827;
  margin: 0 0 6px;
`;

const SectionHint = styled.p`
  font-size: 0.8rem;
  color: #9ca3af;
  margin: 0 0 10px;
`;

const OptionsList = styled.div`
  max-height: 210px;
  overflow-y: auto;
  padding-right: 6px;
  display: flex;
  flex-direction: column;
  gap: 6px;
`;

const OptionRow = styled.label`
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 8px;
  border-radius: 10px;
  cursor: pointer;
  transition: background 0.15s ease;

  &:hover {
    background: rgba(255, 255, 255, 0.9);
  }
`;

const Checkbox = styled.input`
  width: 18px;
  height: 18px;
  accent-color: #4f46e5;
  cursor: pointer;
`;

const OptionLabel = styled.span`
  font-size: 0.9rem;
  color: #111827;
`;

const Footer = styled.div`
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 4px;
`;

const GhostButton = styled.button`
  margin-top: 10px;
  padding: 7px 13px;
  border-radius: 999px;
  border: 1px dashed rgba(148, 163, 184, 0.9);
  background: rgba(255, 255, 255, 0.9);
  color: #4f46e5;
  font-size: 0.8rem;
  font-weight: 500;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  letter-spacing: 0.02em;
  text-transform: uppercase;
  opacity: 0.85;
  transition:
    background 0.15s ease,
    color 0.15s ease,
    box-shadow 0.15s ease,
    transform 0.1s ease,
    opacity 0.15s ease;

  &:hover {
    background: #eef2ff;
    color: #4338ca;
    box-shadow: 0 4px 14px rgba(99, 102, 241, 0.35);
    transform: translateY(-0.5px);
    opacity: 1;
  }

  &:active {
    transform: translateY(0);
    box-shadow: 0 2px 8px rgba(99, 102, 241, 0.25);
  }
`;

const PrimaryButton = styled.button`
  padding: 9px 20px;
  border-radius: 999px;
  border: none;
  background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
  color: white;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 10px 30px rgba(79, 70, 229, 0.6);
  display: inline-flex;
  align-items: center;
  gap: 6px;
  transition: transform 0.12s ease, box-shadow 0.12s ease, filter 0.12s ease;

  &:hover {
    transform: translateY(-1px);
    filter: brightness(1.03);
    box-shadow: 0 14px 40px rgba(79, 70, 229, 0.75);
  }

  &:active {
    transform: translateY(0);
    box-shadow: 0 8px 20px rgba(79, 70, 229, 0.6);
  }

  &:disabled {
    opacity: 0.7;
    cursor: not-allowed;
    box-shadow: none;
  }
`;

const ErrorText = styled.p`
  font-size: 0.8rem;
  color: #b91c1c;
  margin: 6px 0 0;
`;

const PreferencesModal: React.FC<PreferencesModalProps> = ({
  isOpen,
  initialNewsSources,
  initialStockSymbols,
  onSave,
  mode = 'both',
}) => {
  const [selectedNewsSources, setSelectedNewsSources] = useState<string[]>(initialNewsSources);
  const [selectedStockSymbols, setSelectedStockSymbols] = useState<string[]>(initialStockSymbols);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setSelectedNewsSources(initialNewsSources);
  }, [initialNewsSources]);

  useEffect(() => {
    setSelectedStockSymbols(initialStockSymbols);
  }, [initialStockSymbols]);

  const toggleNewsSource = (id: string) => {
    setSelectedNewsSources((prev) =>
      prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id]
    );
  };

  const toggleStockSymbol = (id: string) => {
    setSelectedStockSymbols((prev) =>
      prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id]
    );
  };

  const handleSelectAllNews = () => {
    setSelectedNewsSources(AVAILABLE_NEWS_SOURCES.map((s) => s.id));
  };

  const handleSelectAllStocks = () => {
    setSelectedStockSymbols(AVAILABLE_STOCK_SYMBOLS.map((s) => s.id));
  };

  const handleSave = () => {
    if (mode === 'both') {
      if (selectedNewsSources.length === 0 || selectedStockSymbols.length === 0) {
        setError('Please choose at least one news source and one company.');
        return;
      }
    } else if (mode === 'news') {
      if (selectedNewsSources.length === 0) {
        setError('Please choose at least one news source.');
        return;
      }
    } else if (mode === 'stocks') {
      if (selectedStockSymbols.length === 0) {
        setError('Please choose at least one company.');
        return;
      }
    }
    setError(null);
    onSave(selectedNewsSources, selectedStockSymbols);
  };

  if (!isOpen) {
    return null;
  }

  return (
    <AnimatePresence>
      <Backdrop
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
      >
        <ModalCard
          initial={{ opacity: 0, y: 40, scale: 0.96 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          exit={{ opacity: 0, y: 20, scale: 0.98 }}
          transition={{ duration: 0.28, ease: 'easeOut' }}
        >
          <div>
            <Title>Personalize your TechScope experience</Title>
            <Subtitle>
              Choose which news sources and tech companies you care about. Your feed will only
              show stories and stocks from your selections.
            </Subtitle>
          </div>

          <SectionsGrid>
            {(mode === 'both' || mode === 'news') && (
              <Section>
                <SectionTitle>News sources</SectionTitle>
                <SectionHint>Select one or more tech news outlets.</SectionHint>
                <OptionsList>
                  {AVAILABLE_NEWS_SOURCES.map((source) => (
                    <OptionRow key={source.id}>
                      <Checkbox
                        type="checkbox"
                        checked={selectedNewsSources.includes(source.id)}
                        onChange={() => toggleNewsSource(source.id)}
                      />
                      <OptionLabel>{source.label}</OptionLabel>
                    </OptionRow>
                  ))}
                </OptionsList>
                <GhostButton type="button" onClick={handleSelectAllNews}>
                  Select all sources
                </GhostButton>
              </Section>
            )}

            {(mode === 'both' || mode === 'stocks') && (
              <Section>
                <SectionTitle>Companies to track</SectionTitle>
                <SectionHint>Pick from the 10 major tech stocks.</SectionHint>
                <OptionsList>
                  {AVAILABLE_STOCK_SYMBOLS.map((stock) => (
                    <OptionRow key={stock.id}>
                      <Checkbox
                        type="checkbox"
                        checked={selectedStockSymbols.includes(stock.id)}
                        onChange={() => toggleStockSymbol(stock.id)}
                      />
                      <OptionLabel>{stock.label}</OptionLabel>
                    </OptionRow>
                  ))}
                </OptionsList>
                <GhostButton type="button" onClick={handleSelectAllStocks}>
                  Select all companies
                </GhostButton>
              </Section>
            )}
          </SectionsGrid>

          <Footer>
            {error && <ErrorText>{error}</ErrorText>}
            <PrimaryButton type="button" onClick={handleSave}>
              Save preferences
            </PrimaryButton>
          </Footer>
        </ModalCard>
      </Backdrop>
    </AnimatePresence>
  );
};

export default PreferencesModal;

