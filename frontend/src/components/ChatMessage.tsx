/**
 * ChatMessage component.
 *
 * Displays a single message in the chat, including user queries
 * and assistant responses with citations.
 */

import React from 'react';
import type { ChatMessageProps, Citation } from '../types/api';

// ============================================================================
// ChatMessage Component
// ============================================================================

export const ChatMessage: React.FC<ChatMessageProps> = ({
  message,
  onCitationClick,
}) => {
  const isUser = message.role === 'user';

  /**
   * Handle citation click
   */
  const handleCitationClick = (citation: Citation) => {
    if (onCitationClick) {
      onCitationClick(citation);
    } else {
      // Default behavior: scroll to anchor if URL is provided
      if (citation.url_anchor) {
        const element = document.querySelector(citation.url_anchor);
        if (element) {
          element.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
      }
    }
  };

  /**
   * Format timestamp
   */
  const formatTime = (date: Date): string => {
    return date.toLocaleTimeString([], {
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  /**
   * Render citations
   */
  const renderCitations = () => {
    if (!message.citations || message.citations.length === 0) {
      return null;
    }

    return (
      <div className="chat-message__citations">
        <div className="chat-message__citations-label">Sources:</div>
        {message.citations.map((citation, index) => (
          <button
            key={citation.chunk_id}
            className="chat-message__citation"
            onClick={() => handleCitationClick(citation)}
            title={`Relevance: ${(citation.relevance_score * 100).toFixed(0)}%\n${citation.text_preview}`}
          >
            <span className="chat-message__citation-number">{index + 1}</span>
            <span className="chat-message__citation-source">
              {citation.source}
            </span>
            <span className="chat-message__citation-score">
              {(citation.relevance_score * 100).toFixed(0)}%
            </span>
          </button>
        ))}
      </div>
    );
  };

  /**
   * Render selected text badge
   */
  const renderSelectedTextBadge = () => {
    if (message.mode !== 'selected-text') {
      return null;
    }

    return (
      <div className="chat-message__badge">
        <span className="chat-message__badge-icon">📄</span>
        <span className="chat-message__badge-text">Selected Text</span>
      </div>
    );
  };

  /**
   * Render loading indicator
   */
  const renderLoading = () => {
    if (!message.loading) {
      return null;
    }

    return (
      <div className="chat-message__loading">
        <span className="chat-message__loading-dot"></span>
        <span className="chat-message__loading-dot"></span>
        <span className="chat-message__loading-dot"></span>
      </div>
    );
  };

  /**
   * Render error
   */
  const renderError = () => {
    if (!message.error) {
      return null;
    }

    return (
      <div className="chat-message__error">
        <span className="chat-message__error-icon">⚠️</span>
        <span className="chat-message__error-text">{message.error}</span>
      </div>
    );
  };

  return (
    <div
      className={`chat-message ${
        isUser ? 'chat-message--user' : 'chat-message--assistant'
      }`}
    >
      <div className="chat-message__avatar">
        {isUser ? (
          <span className="chat-message__avatar-icon">👤</span>
        ) : (
          <span className="chat-message__avatar-icon">🤖</span>
        )}
      </div>

      <div className="chat-message__content">
        {renderSelectedTextBadge()}

        <div className="chat-message__text">
          {message.loading ? renderLoading() : message.content}
        </div>

        {renderError()}
        {renderCitations()}

        <div className="chat-message__timestamp">{formatTime(message.timestamp)}</div>
      </div>
    </div>
  );
};

export default ChatMessage;
