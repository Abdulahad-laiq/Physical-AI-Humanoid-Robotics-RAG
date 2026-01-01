/**
 * React hook for detecting text selection.
 *
 * Monitors user text selection and provides the selected text
 * along with utilities for selected-text queries.
 */

import { useState, useEffect, useCallback, useRef } from 'react';
import type { TextSelection } from '../types/api';
import { SELECTED_TEXT_LIMITS } from '../types/api';

// ============================================================================
// Hook
// ============================================================================

export interface UseTextSelectionOptions {
  /**
   * Minimum length of selected text to be considered valid
   */
  minLength?: number;

  /**
   * Maximum length of selected text to be considered valid
   */
  maxLength?: number;

  /**
   * Debounce delay in milliseconds before updating selection
   */
  debounceMs?: number;

  /**
   * Callback when selection changes
   */
  onSelectionChange?: (selection: TextSelection) => void;
}

export interface UseTextSelectionReturn extends TextSelection {
  /**
   * Clear the current selection
   */
  clearSelection: () => void;

  /**
   * Manually set selection text (for testing or programmatic use)
   */
  setSelection: (text: string) => void;

  /**
   * Check if text meets validation criteria
   */
  isValidLength: (text: string) => boolean;
}

export function useTextSelection(
  options: UseTextSelectionOptions = {}
): UseTextSelectionReturn {
  const {
    minLength = SELECTED_TEXT_LIMITS.MIN_LENGTH,
    maxLength = SELECTED_TEXT_LIMITS.MAX_LENGTH,
    debounceMs = 300,
    onSelectionChange,
  } = options;

  const [selection, setSelection] = useState<TextSelection>({
    text: '',
    range: null,
    isValid: false,
  });

  const debounceTimer = useRef<NodeJS.Timeout | null>(null);

  /**
   * Check if text length is valid
   */
  const isValidLength = useCallback(
    (text: string): boolean => {
      const trimmedLength = text.trim().length;
      return trimmedLength >= minLength && trimmedLength <= maxLength;
    },
    [minLength, maxLength]
  );

  /**
   * Handle selection change event
   */
  const handleSelectionChange = useCallback(() => {
    // Clear existing timer
    if (debounceTimer.current) {
      clearTimeout(debounceTimer.current);
    }

    // Debounce the selection change
    debounceTimer.current = setTimeout(() => {
      const selection = window.getSelection();

      if (!selection || selection.rangeCount === 0) {
        setSelection({
          text: '',
          range: null,
          isValid: false,
        });
        return;
      }

      const selectedText = selection.toString().trim();
      const range = selection.getRangeAt(0);

      const newSelection: TextSelection = {
        text: selectedText,
        range,
        isValid: isValidLength(selectedText),
      };

      setSelection(newSelection);

      if (onSelectionChange) {
        onSelectionChange(newSelection);
      }
    }, debounceMs);
  }, [debounceMs, isValidLength, onSelectionChange]);

  /**
   * Clear selection
   */
  const clearSelection = useCallback(() => {
    const selection = window.getSelection();
    if (selection) {
      selection.removeAllRanges();
    }

    setSelection({
      text: '',
      range: null,
      isValid: false,
    });
  }, []);

  /**
   * Manually set selection text
   */
  const setSelectionText = useCallback(
    (text: string) => {
      const newSelection: TextSelection = {
        text: text.trim(),
        range: null,
        isValid: isValidLength(text),
      };

      setSelection(newSelection);

      if (onSelectionChange) {
        onSelectionChange(newSelection);
      }
    },
    [isValidLength, onSelectionChange]
  );

  /**
   * Set up event listeners
   */
  useEffect(() => {
    // Listen for mouse up (end of selection)
    document.addEventListener('mouseup', handleSelectionChange);

    // Listen for keyboard selection (Shift + Arrow keys)
    document.addEventListener('keyup', handleSelectionChange);

    // Listen for selection change event (more reliable in some browsers)
    document.addEventListener('selectionchange', handleSelectionChange);

    // Cleanup
    return () => {
      document.removeEventListener('mouseup', handleSelectionChange);
      document.removeEventListener('keyup', handleSelectionChange);
      document.removeEventListener('selectionchange', handleSelectionChange);

      if (debounceTimer.current) {
        clearTimeout(debounceTimer.current);
      }
    };
  }, [handleSelectionChange]);

  return {
    ...selection,
    clearSelection,
    setSelection: setSelectionText,
    isValidLength,
  };
}

// ============================================================================
// Utility Functions
// ============================================================================

/**
 * Get currently selected text without using the hook
 */
export function getSelectedText(): string {
  const selection = window.getSelection();
  return selection ? selection.toString().trim() : '';
}

/**
 * Check if there is any text currently selected
 */
export function hasTextSelected(): boolean {
  const selection = window.getSelection();
  return selection !== null && selection.toString().trim().length > 0;
}

/**
 * Get selection position for positioning a popup button
 */
export function getSelectionPosition(): { x: number; y: number } | null {
  const selection = window.getSelection();

  if (!selection || selection.rangeCount === 0) {
    return null;
  }

  const range = selection.getRangeAt(0);
  const rect = range.getBoundingClientRect();

  return {
    x: rect.left + rect.width / 2,
    y: rect.top - 10, // Position above the selection
  };
}
