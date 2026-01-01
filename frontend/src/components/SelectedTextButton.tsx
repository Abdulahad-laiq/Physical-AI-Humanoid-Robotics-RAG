/**
 * SelectedTextButton component.
 *
 * Floating button that appears when text is selected,
 * allowing users to ask questions about the selected text.
 */

import React, { useState, useEffect } from 'react';
import type { SelectedTextButtonProps } from '../types/api';
import { getSelectionPosition } from '../hooks/useTextSelection';

// ============================================================================
// SelectedTextButton Component
// ============================================================================

export const SelectedTextButton: React.FC<SelectedTextButtonProps> = ({
  selectedText,
  onAskAboutText,
  visible,
}) => {
  const [position, setPosition] = useState<{ x: number; y: number } | null>(null);

  /**
   * Update button position when selection changes
   */
  useEffect(() => {
    if (visible && selectedText) {
      const pos = getSelectionPosition();
      setPosition(pos);
    } else {
      setPosition(null);
    }
  }, [visible, selectedText]);

  /**
   * Handle button click
   */
  const handleClick = () => {
    onAskAboutText();
  };

  if (!visible || !position) {
    return null;
  }

  return (
    <div
      className="selected-text-button"
      style={{
        position: 'fixed',
        left: `${position.x}px`,
        top: `${position.y}px`,
        transform: 'translateX(-50%) translateY(-100%)',
        zIndex: 9999,
      }}
    >
      <button
        className="selected-text-button__btn"
        onClick={handleClick}
        title={`Ask about selected text (${selectedText.length} characters)`}
      >
        <span className="selected-text-button__icon">💬</span>
        <span className="selected-text-button__text">Ask about this text</span>
      </button>

      <div className="selected-text-button__tooltip">
        {selectedText.length} characters selected
      </div>
    </div>
  );
};

export default SelectedTextButton;
