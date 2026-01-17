/**
 * ChatbotWidget wrapper for Docusaurus integration.
 *
 * Integrates the RAG chatbot with Docusaurus theme system
 * and provides environment-based configuration.
 */

import React from 'react';
import { ChatWidget } from './chat/ChatWidget';
import '../css/chat.css';

export default function ChatbotWidget() {
  // Detect theme from document attribute (set by Docusaurus)
  const [theme, setTheme] = React.useState<'light' | 'dark'>('light');

  React.useEffect(() => {
    // Get initial theme
    const updateTheme = () => {
      const htmlElement = document.documentElement;
      const currentTheme = htmlElement.getAttribute('data-theme') as 'light' | 'dark';
      setTheme(currentTheme || 'light');
    };

    updateTheme();

    // Watch for theme changes
    const observer = new MutationObserver(updateTheme);
    observer.observe(document.documentElement, {
      attributes: true,
      attributeFilter: ['data-theme'],
    });

    return () => observer.disconnect();
  }, []);

  // Get API URL - use localhost in development
  const apiBaseUrl =
    typeof window !== 'undefined' && window.location.hostname === 'localhost'
      ? 'http://localhost:7860'
      : 'https://abdulahadlaiq-rag-chatbot.hf.space';

  return (
    <ChatWidget
      apiBaseUrl={apiBaseUrl}
      initialOpen={false}
      theme={theme}
      position="bottom-right"
      maxHeight="600px"
      sessionId={`session-${Date.now()}`}
    />
  );
}
