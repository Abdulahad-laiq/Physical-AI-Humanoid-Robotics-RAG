/**
 * ChatInput component.
 *
 * Input field for user queries with validation and character counting.
 */

import React, { useState, useRef, useEffect } from 'react';
import type { ChatInputProps } from '../types/api';
import { QUERY_LIMITS } from '../types/api';

// ============================================================================
// ChatInput Component
// ============================================================================

export const ChatInput: React.FC<ChatInputProps> = ({
  onSend,
  disabled = false,
  placeholder = 'Ask a question about the textbook...',
  maxLength = QUERY_LIMITS.MAX_LENGTH,
}) => {
  const [query, setQuery] = useState('');
  const [isFocused, setIsFocused] = useState(false);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  /**
   * Auto-resize textarea based on content
   */
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
    }
  }, [query]);

  /**
   * Handle input change
   */
  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const value = e.target.value;
    if (value.length <= maxLength) {
      setQuery(value);
    }
  };

  /**
   * Handle send button click
   */
  const handleSend = () => {
    const trimmedQuery = query.trim();

    if (trimmedQuery.length === 0) {
      return;
    }

    if (trimmedQuery.length < QUERY_LIMITS.MIN_LENGTH) {
      return;
    }

    onSend(trimmedQuery);
    setQuery('');

    // Reset textarea height
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
    }
  };

  /**
   * Handle Enter key press
   */
  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    // Send on Enter (without Shift)
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  /**
   * Check if send button should be enabled
   */
  const canSend = () => {
    const trimmedQuery = query.trim();
    return (
      !disabled &&
      trimmedQuery.length >= QUERY_LIMITS.MIN_LENGTH &&
      trimmedQuery.length <= maxLength
    );
  };

  /**
   * Get character count class
   */
  const getCharCountClass = () => {
    const length = query.length;
    const remaining = maxLength - length;

    if (remaining < 50) {
      return 'chat-input__char-count--warning';
    }
    if (remaining < 100) {
      return 'chat-input__char-count--caution';
    }
    return '';
  };

  return (
    <div className={`chat-input ${isFocused ? 'chat-input--focused' : ''}`}>
      <div className="chat-input__wrapper">
        <textarea
          ref={textareaRef}
          className="chat-input__textarea"
          value={query}
          onChange={handleChange}
          onKeyDown={handleKeyDown}
          onFocus={() => setIsFocused(true)}
          onBlur={() => setIsFocused(false)}
          placeholder={placeholder}
          disabled={disabled}
          rows={1}
          maxLength={maxLength}
        />

        <button
          className={`chat-input__send ${canSend() ? 'chat-input__send--enabled' : ''}`}
          onClick={handleSend}
          disabled={!canSend()}
          title={canSend() ? 'Send message' : 'Enter a question to send'}
        >
          <svg
            className="chat-input__send-icon"
            width="20"
            height="20"
            viewBox="0 0 20 20"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M2 10L18 2L10 18L8 11L2 10Z"
              fill="currentColor"
            />
          </svg>
        </button>
      </div>

      <div className="chat-input__footer">
        <div className="chat-input__hint">
          Press <kbd>Enter</kbd> to send, <kbd>Shift+Enter</kbd> for new line
        </div>

        <div className={`chat-input__char-count ${getCharCountClass()}`}>
          {query.length} / {maxLength}
        </div>
      </div>
    </div>
  );
};

export default ChatInput;
