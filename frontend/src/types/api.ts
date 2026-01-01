/**
 * TypeScript type definitions for RAG Chatbot API.
 *
 * Matches backend Pydantic schemas for type safety.
 */

// ============================================================================
// Request Types
// ============================================================================

export interface QueryRequest {
  query: string;
  session_id?: string;
  debug?: boolean;
}

export interface SelectedTextQueryRequest {
  query: string;
  selected_text: string;
  session_id?: string;
  debug?: boolean;
}

// ============================================================================
// Response Types
// ============================================================================

export interface Citation {
  chunk_id: string;
  chapter: number;
  section: string;
  url_anchor: string;
  relevance_score: number;
  text_preview: string;
  source: string;
}

export interface ChatResponse {
  answer: string;
  citations: Citation[];
  query_id: string;
  generation_time_ms: number;
  debug_metadata?: {
    retrieval?: {
      chunks_retrieved: number;
      top_scores: number[];
      search_time_ms: number;
    };
    chunks?: Array<{
      chunk_id: string;
      score: number;
      chapter: number;
      section: string;
      text_preview: string;
    }>;
    mode?: string;
    selected_text_length?: number;
    chunks_created?: number;
    isolation?: string;
    global_db_accessed?: boolean;
  };
}

export interface HealthResponse {
  status: string;
  qdrant_connected: boolean;
  neon_connected: boolean;
  timestamp: string;
}

export interface ErrorResponse {
  detail: string | {
    error: string;
    query_id?: string;
    message?: string;
  };
}

// ============================================================================
// UI State Types
// ============================================================================

export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  citations?: Citation[];
  timestamp: Date;
  mode?: 'global' | 'selected-text';
  selectedText?: string;
  loading?: boolean;
  error?: string;
}

export interface ChatSession {
  session_id: string;
  messages: Message[];
  created_at: Date;
}

// ============================================================================
// Component Props Types
// ============================================================================

export interface ChatWidgetProps {
  apiBaseUrl?: string;
  initialOpen?: boolean;
  theme?: 'light' | 'dark';
  position?: 'bottom-right' | 'bottom-left';
  maxHeight?: string;
  sessionId?: string;
}

export interface ChatMessageProps {
  message: Message;
  onCitationClick?: (citation: Citation) => void;
}

export interface ChatInputProps {
  onSend: (query: string) => void;
  disabled?: boolean;
  placeholder?: string;
  maxLength?: number;
}

export interface SelectedTextButtonProps {
  selectedText: string;
  onAskAboutText: () => void;
  visible: boolean;
}

// ============================================================================
// API Configuration
// ============================================================================

export interface ApiConfig {
  baseUrl: string;
  timeout?: number;
  retries?: number;
  sessionId?: string;
  debug?: boolean;
}

// ============================================================================
// Text Selection Types
// ============================================================================

export interface TextSelection {
  text: string;
  range: Range | null;
  isValid: boolean;
}

// ============================================================================
// Constants
// ============================================================================

export const API_ENDPOINTS = {
  CHAT: '/api/v1/chat',
  CHAT_SELECTED: '/api/v1/chat/selected',
  HEALTH: '/health',
} as const;

export const QUERY_LIMITS = {
  MIN_LENGTH: 1,
  MAX_LENGTH: 1000,
} as const;

export const SELECTED_TEXT_LIMITS = {
  MIN_LENGTH: 10,
  MAX_LENGTH: 5000,
} as const;

export const RATE_LIMITS = {
  REQUESTS_PER_MINUTE: 100,
} as const;
