/**
 * API client for RAG Chatbot backend.
 *
 * Handles all HTTP communication with the FastAPI backend,
 * including error handling, retries, and type safety.
 */

import type {
  QueryRequest,
  SelectedTextQueryRequest,
  ChatResponse,
  HealthResponse,
  ErrorResponse,
  ApiConfig,
} from '../types/api';

// ============================================================================
// Configuration
// ============================================================================

const DEFAULT_CONFIG: Required<ApiConfig> = {
  baseUrl: process.env.REACT_APP_API_URL || 'http://localhost:8000',
  timeout: 30000, // 30 seconds
  retries: 3,
  sessionId: '',
  debug: process.env.NODE_ENV === 'development',
};

// ============================================================================
// Error Classes
// ============================================================================

export class ApiError extends Error {
  constructor(
    message: string,
    public statusCode?: number,
    public details?: any
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

export class RateLimitError extends ApiError {
  constructor(message: string = 'Rate limit exceeded') {
    super(message, 429);
    this.name = 'RateLimitError';
  }
}

export class ValidationError extends ApiError {
  constructor(message: string, details?: any) {
    super(message, 400, details);
    this.name = 'ValidationError';
  }
}

export class ServiceUnavailableError extends ApiError {
  constructor(message: string = 'Service temporarily unavailable') {
    super(message, 503);
    this.name = 'ServiceUnavailableError';
  }
}

// ============================================================================
// API Client Class
// ============================================================================

export class ChatApiClient {
  private config: Required<ApiConfig>;
  private abortController: AbortController | null = null;

  constructor(config: Partial<ApiConfig> = {}) {
    this.config = { ...DEFAULT_CONFIG, ...config };
  }

  /**
   * Send a query to the global chat endpoint.
   */
  async sendQuery(
    query: string,
    options: { debug?: boolean } = {}
  ): Promise<ChatResponse> {
    const request: QueryRequest = {
      query,
      session_id: this.config.sessionId || undefined,
      debug: options.debug ?? this.config.debug,
    };

    return this.post<ChatResponse>('/api/v1/chat', request);
  }

  /**
   * Send a query about selected text.
   */
  async sendSelectedTextQuery(
    query: string,
    selectedText: string,
    options: { debug?: boolean } = {}
  ): Promise<ChatResponse> {
    const request: SelectedTextQueryRequest = {
      query,
      selected_text: selectedText,
      session_id: this.config.sessionId || undefined,
      debug: options.debug ?? this.config.debug,
    };

    return this.post<ChatResponse>('/api/v1/chat/selected', request);
  }

  /**
   * Check backend health status.
   */
  async checkHealth(): Promise<HealthResponse> {
    return this.get<HealthResponse>('/health');
  }

  /**
   * Cancel any ongoing request.
   */
  cancelRequest(): void {
    if (this.abortController) {
      this.abortController.abort();
      this.abortController = null;
    }
  }

  /**
   * Update configuration.
   */
  updateConfig(config: Partial<ApiConfig>): void {
    this.config = { ...this.config, ...config };
  }

  // ============================================================================
  // Private HTTP Methods
  // ============================================================================

  private async get<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'GET',
    });
  }

  private async post<T>(endpoint: string, body: any): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    });
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit
  ): Promise<T> {
    const url = `${this.config.baseUrl}${endpoint}`;

    // Create new abort controller for this request
    this.abortController = new AbortController();

    const requestOptions: RequestInit = {
      ...options,
      signal: this.abortController.signal,
    };

    let lastError: Error | null = null;

    // Retry logic
    for (let attempt = 0; attempt < this.config.retries; attempt++) {
      try {
        const response = await this.fetchWithTimeout(url, requestOptions);

        // Handle different status codes
        if (response.ok) {
          const data = await response.json();
          return data as T;
        }

        // Handle error responses
        const errorData: ErrorResponse = await response.json().catch(() => ({
          detail: 'Unknown error occurred',
        }));

        throw this.createErrorFromResponse(response.status, errorData);
      } catch (error) {
        lastError = error as Error;

        // Don't retry on validation errors or rate limits
        if (
          error instanceof ValidationError ||
          error instanceof RateLimitError
        ) {
          throw error;
        }

        // Don't retry on abort
        if (error instanceof Error && error.name === 'AbortError') {
          throw new ApiError('Request cancelled');
        }

        // Exponential backoff before retry
        if (attempt < this.config.retries - 1) {
          await this.delay(Math.pow(2, attempt) * 1000);
        }
      }
    }

    // All retries failed
    throw lastError || new ApiError('Request failed after retries');
  }

  private async fetchWithTimeout(
    url: string,
    options: RequestInit
  ): Promise<Response> {
    const timeoutId = setTimeout(() => {
      if (this.abortController) {
        this.abortController.abort();
      }
    }, this.config.timeout);

    try {
      const response = await fetch(url, options);
      clearTimeout(timeoutId);
      return response;
    } catch (error) {
      clearTimeout(timeoutId);
      throw error;
    }
  }

  private createErrorFromResponse(
    status: number,
    errorData: ErrorResponse
  ): ApiError {
    const message =
      typeof errorData.detail === 'string'
        ? errorData.detail
        : errorData.detail.error || 'An error occurred';

    switch (status) {
      case 400:
        return new ValidationError(message, errorData.detail);
      case 429:
        return new RateLimitError(message);
      case 503:
        return new ServiceUnavailableError(message);
      default:
        return new ApiError(message, status, errorData.detail);
    }
  }

  private delay(ms: number): Promise<void> {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }
}

// ============================================================================
// Singleton Instance
// ============================================================================

let apiClientInstance: ChatApiClient | null = null;

export function getApiClient(config?: Partial<ApiConfig>): ChatApiClient {
  if (!apiClientInstance) {
    apiClientInstance = new ChatApiClient(config);
  } else if (config) {
    apiClientInstance.updateConfig(config);
  }
  return apiClientInstance;
}

// ============================================================================
// Convenience Functions
// ============================================================================

export async function sendChatQuery(
  query: string,
  debug: boolean = false
): Promise<ChatResponse> {
  const client = getApiClient();
  return client.sendQuery(query, { debug });
}

export async function sendSelectedTextQuery(
  query: string,
  selectedText: string,
  debug: boolean = false
): Promise<ChatResponse> {
  const client = getApiClient();
  return client.sendSelectedTextQuery(query, selectedText, { debug });
}

export async function checkBackendHealth(): Promise<HealthResponse> {
  const client = getApiClient();
  return client.checkHealth();
}

// ============================================================================
// Export
// ============================================================================

export default ChatApiClient;
