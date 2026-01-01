/**
 * ChatWidget component.
 *
 * Main chat interface that integrates all components:
 * - Message display
 * - Input field
 * - Selected text detection
 * - API communication
 */

import React, { useState, useEffect, useRef, useCallback } from 'react';
import { ChatMessage } from './ChatMessage';
import { ChatInput } from './ChatInput';
import { SelectedTextButton } from './SelectedTextButton';
import { useTextSelection } from '../hooks/useTextSelection';
import { getApiClient, ApiError, RateLimitError, ValidationError } from '../services/api';
import type { ChatWidgetProps, Message, Citation } from '../types/api';

// ============================================================================
// ChatWidget Component
// ============================================================================

export const ChatWidget: React.FC<ChatWidgetProps> = ({
  apiBaseUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000',
  initialOpen = false,
  theme = 'light',
  position = 'bottom-right',
  maxHeight = '600px',
  sessionId,
}) => {
  const [isOpen, setIsOpen] = useState(initialOpen);
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const apiClient = useRef(
    getApiClient({
      baseUrl: apiBaseUrl,
      sessionId: sessionId || `session-${Date.now()}`,
    })
  );

  // Text selection hook
  const selection = useTextSelection({
    minLength: 10,
    maxLength: 5000,
  });

  /**
   * Scroll to bottom of messages
   */
  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, []);

  /**
   * Scroll when messages change
   */
  useEffect(() => {
    scrollToBottom();
  }, [messages, scrollToBottom]);

  /**
   * Add a message to the chat
   */
  const addMessage = useCallback((message: Omit<Message, 'id' | 'timestamp'>) => {
    const newMessage: Message = {
      ...message,
      id: `msg-${Date.now()}-${Math.random()}`,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, newMessage]);
    return newMessage.id;
  }, []);

  /**
   * Update a message
   */
  const updateMessage = useCallback((id: string, updates: Partial<Message>) => {
    setMessages((prev) =>
      prev.map((msg) => (msg.id === id ? { ...msg, ...updates } : msg))
    );
  }, []);

  /**
   * Handle sending a global query
   */
  const handleSendQuery = useCallback(
    async (query: string) => {
      setIsLoading(true);
      setError(null);

      // Add user message
      const userMessageId = addMessage({
        role: 'user',
        content: query,
        mode: 'global',
      });

      // Add loading assistant message
      const assistantMessageId = addMessage({
        role: 'assistant',
        content: '',
        loading: true,
      });

      try {
        const response = await apiClient.current.sendQuery(query);

        // Update assistant message with response
        updateMessage(assistantMessageId, {
          content: response.answer,
          citations: response.citations,
          loading: false,
        });
      } catch (err) {
        const errorMessage = getErrorMessage(err);

        updateMessage(assistantMessageId, {
          content: '',
          loading: false,
          error: errorMessage,
        });

        setError(errorMessage);
      } finally {
        setIsLoading(false);
      }
    },
    [addMessage, updateMessage]
  );

  /**
   * Handle sending a selected-text query
   */
  const handleSendSelectedTextQuery = useCallback(
    async (query: string, selectedText: string) => {
      setIsLoading(true);
      setError(null);

      // Add user message
      const userMessageId = addMessage({
        role: 'user',
        content: query,
        mode: 'selected-text',
        selectedText,
      });

      // Add loading assistant message
      const assistantMessageId = addMessage({
        role: 'assistant',
        content: '',
        loading: true,
      });

      try {
        const response = await apiClient.current.sendSelectedTextQuery(
          query,
          selectedText
        );

        // Update assistant message with response
        updateMessage(assistantMessageId, {
          content: response.answer,
          citations: response.citations,
          loading: false,
          mode: 'selected-text',
        });
      } catch (err) {
        const errorMessage = getErrorMessage(err);

        updateMessage(assistantMessageId, {
          content: '',
          loading: false,
          error: errorMessage,
        });

        setError(errorMessage);
      } finally {
        setIsLoading(false);
        selection.clearSelection();
      }
    },
    [addMessage, updateMessage, selection]
  );

  /**
   * Handle "Ask about text" button click
   */
  const handleAskAboutSelectedText = useCallback(() => {
    if (!selection.text || !selection.isValid) {
      return;
    }

    // Open chat if closed
    if (!isOpen) {
      setIsOpen(true);
    }

    // Auto-populate input with default question
    // For now, just open the chat - user can type their question
    // TODO: Add input auto-population feature
  }, [selection, isOpen]);

  /**
   * Handle citation click
   */
  const handleCitationClick = useCallback((citation: Citation) => {
    // Scroll to citation in the document
    if (citation.url_anchor) {
      const element = document.querySelector(citation.url_anchor);
      if (element) {
        element.scrollIntoView({ behavior: 'smooth', block: 'center' });

        // Highlight the element temporarily
        element.classList.add('citation-highlight');
        setTimeout(() => {
          element.classList.remove('citation-highlight');
        }, 2000);
      }
    }
  }, []);

  /**
   * Toggle chat open/closed
   */
  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  /**
   * Clear chat history
   */
  const clearChat = () => {
    setMessages([]);
    setError(null);
  };

  return (
    <>
      {/* Selected text button */}
      <SelectedTextButton
        selectedText={selection.text}
        onAskAboutText={handleAskAboutSelectedText}
        visible={selection.isValid && !isOpen}
      />

      {/* Chat toggle button */}
      {!isOpen && (
        <button
          className={`chat-widget__toggle chat-widget__toggle--${position}`}
          onClick={toggleChat}
          title="Open chat"
        >
          <span className="chat-widget__toggle-icon">💬</span>
          {messages.length > 0 && (
            <span className="chat-widget__toggle-badge">{messages.length}</span>
          )}
        </button>
      )}

      {/* Chat window */}
      {isOpen && (
        <div
          className={`chat-widget chat-widget--${theme} chat-widget--${position}`}
          style={{ maxHeight }}
        >
          {/* Header */}
          <div className="chat-widget__header">
            <div className="chat-widget__title">
              <span className="chat-widget__title-icon">🤖</span>
              <span className="chat-widget__title-text">Textbook Assistant</span>
            </div>

            <div className="chat-widget__actions">
              {messages.length > 0 && (
                <button
                  className="chat-widget__action"
                  onClick={clearChat}
                  title="Clear chat"
                >
                  🗑️
                </button>
              )}

              <button
                className="chat-widget__action"
                onClick={toggleChat}
                title="Close chat"
              >
                ✕
              </button>
            </div>
          </div>

          {/* Messages */}
          <div className="chat-widget__messages">
            {messages.length === 0 && (
              <div className="chat-widget__welcome">
                <h3>Welcome! 👋</h3>
                <p>Ask me anything about the textbook.</p>
                <p className="chat-widget__welcome-hint">
                  💡 Tip: Select text and click "Ask about this text" for
                  context-specific questions.
                </p>
              </div>
            )}

            {messages.map((message) => (
              <ChatMessage
                key={message.id}
                message={message}
                onCitationClick={handleCitationClick}
              />
            ))}

            <div ref={messagesEndRef} />
          </div>

          {/* Error display */}
          {error && (
            <div className="chat-widget__error">
              <span className="chat-widget__error-icon">⚠️</span>
              <span className="chat-widget__error-text">{error}</span>
              <button
                className="chat-widget__error-dismiss"
                onClick={() => setError(null)}
              >
                ✕
              </button>
            </div>
          )}

          {/* Input */}
          <div className="chat-widget__input-wrapper">
            {selection.isValid && (
              <div className="chat-widget__selected-text-indicator">
                <span className="chat-widget__selected-text-icon">📄</span>
                <span className="chat-widget__selected-text-label">
                  {selection.text.length} characters selected
                </span>
                <button
                  className="chat-widget__selected-text-clear"
                  onClick={selection.clearSelection}
                  title="Clear selection"
                >
                  ✕
                </button>
              </div>
            )}

            <ChatInput
              onSend={(query) => {
                if (selection.isValid) {
                  handleSendSelectedTextQuery(query, selection.text);
                } else {
                  handleSendQuery(query);
                }
              }}
              disabled={isLoading}
              placeholder={
                selection.isValid
                  ? 'Ask about the selected text...'
                  : 'Ask a question about the textbook...'
              }
            />
          </div>
        </div>
      )}
    </>
  );
};

// ============================================================================
// Helper Functions
// ============================================================================

function getErrorMessage(error: unknown): string {
  if (error instanceof RateLimitError) {
    return 'Too many requests. Please wait a moment and try again.';
  }

  if (error instanceof ValidationError) {
    return 'Invalid input. Please check your question and try again.';
  }

  if (error instanceof ApiError) {
    return error.message || 'An error occurred. Please try again.';
  }

  if (error instanceof Error) {
    return error.message;
  }

  return 'An unexpected error occurred. Please try again.';
}

export default ChatWidget;
