import React from 'react';
import BrowserOnly from '@docusaurus/BrowserOnly';

// Lazy load the chatbot widget only in browser
const ChatbotWidget = React.lazy(() => import('../components/ChatbotWidget'));

export default function Root({children}) {
  return (
    <>
      {children}
      <BrowserOnly fallback={<div />}>
        {() => (
          <React.Suspense fallback={<div />}>
            <ChatbotWidget />
          </React.Suspense>
        )}
      </BrowserOnly>
    </>
  );
}
