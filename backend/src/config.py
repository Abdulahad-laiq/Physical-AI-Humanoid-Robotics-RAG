"""
Application configuration management.

Loads and validates environment variables and application settings.
Uses pydantic-settings for type-safe configuration.
"""

from pydantic_settings import BaseSettings
from pydantic import Field, field_validator
from typing import Optional
import os
from pathlib import Path


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    All settings can be configured via .env file or environment variables.
    """

    # ========================================================================
    # Gemini API Configuration
    # ========================================================================

    gemini_api_key: str = Field(
        ...,
        alias="GEMINI_API_KEY",
        description="Gemini API key for LLM access"
    )

    gemini_model: str = Field(
        default="gemini-2.0-flash",
        alias="GEMINI_MODEL",
        description="Gemini model name"
    )

    gemini_base_url: str = Field(
        default="https://generativelanguage.googleapis.com/v1beta/openai/",
        alias="GEMINI_BASE_URL",
        description="Gemini API base URL (OpenAI-compatible endpoint)"
    )

    gemini_max_tokens: int = Field(
        default=2048,
        alias="GEMINI_MAX_TOKENS",
        description="Maximum tokens for Gemini responses"
    )

    gemini_temperature: float = Field(
        default=0.3,
        alias="GEMINI_TEMPERATURE",
        description="Temperature for response generation (0.0-1.0)"
    )

    @field_validator("gemini_temperature")
    @classmethod
    def validate_temperature(cls, v: float) -> float:
        """Validate temperature is in valid range."""
        if not 0.0 <= v <= 2.0:
            raise ValueError("Temperature must be between 0.0 and 2.0")
        return v

    # ========================================================================
    # Qdrant Configuration
    # ========================================================================

    qdrant_url: str = Field(
        ...,
        alias="QDRANT_URL",
        description="Qdrant server URL"
    )

    qdrant_api_key: str = Field(
        ...,
        alias="QDRANT_API_KEY",
        description="Qdrant API key"
    )

    qdrant_collection_name: str = Field(
        default="textbook_chunks_v1",
        alias="QDRANT_COLLECTION_NAME",
        description="Qdrant collection name for textbook chunks"
    )

    qdrant_timeout: int = Field(
        default=30,
        alias="QDRANT_TIMEOUT",
        description="Qdrant client timeout in seconds"
    )

    # ========================================================================
    # Neon PostgreSQL Configuration
    # ========================================================================

    neon_database_url: str = Field(
        ...,
        alias="NEON_DATABASE_URL",
        description="Neon PostgreSQL connection URL"
    )

    @field_validator("neon_database_url")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        """Validate database URL format."""
        if not v.startswith("postgresql://"):
            raise ValueError("Database URL must start with 'postgresql://'")
        return v

    # ========================================================================
    # Embedding Configuration
    # ========================================================================

    embedding_model: str = Field(
        default="sentence-transformers/all-MiniLM-L6-v2",
        alias="EMBEDDING_MODEL",
        description="Sentence-Transformers model name"
    )

    embedding_dimension: int = Field(
        default=384,
        alias="EMBEDDING_DIMENSION",
        description="Embedding vector dimension"
    )

    embedding_device: str = Field(
        default="cpu",
        alias="EMBEDDING_DEVICE",
        description="Device for embedding model (cpu, cuda, mps)"
    )

    # ========================================================================
    # Retrieval Configuration
    # ========================================================================

    retrieval_top_k: int = Field(
        default=5,
        alias="RETRIEVAL_TOP_K",
        description="Number of chunks to retrieve for each query"
    )

    retrieval_score_threshold: float = Field(
        default=0.3,
        alias="RETRIEVAL_SCORE_THRESHOLD",
        description="Minimum similarity score for retrieved chunks"
    )

    @field_validator("retrieval_score_threshold")
    @classmethod
    def validate_score_threshold(cls, v: float) -> float:
        """Validate score threshold is in valid range."""
        if not 0.0 <= v <= 1.0:
            raise ValueError("Score threshold must be between 0.0 and 1.0")
        return v

    # ========================================================================
    # Chunking Configuration
    # ========================================================================

    chunk_max_tokens: int = Field(
        default=512,
        alias="CHUNK_MAX_TOKENS",
        description="Maximum tokens per chunk"
    )

    chunk_min_tokens: int = Field(
        default=50,
        alias="CHUNK_MIN_TOKENS",
        description="Minimum tokens per chunk"
    )

    chunk_overlap_tokens: int = Field(
        default=50,
        alias="CHUNK_OVERLAP_TOKENS",
        description="Token overlap between chunks"
    )

    # ========================================================================
    # Rate Limiting Configuration
    # ========================================================================

    rate_limit_per_minute: int = Field(
        default=100,
        alias="RATE_LIMIT_PER_MINUTE",
        description="Maximum requests per minute per IP"
    )

    rate_limit_enabled: bool = Field(
        default=True,
        alias="RATE_LIMIT_ENABLED",
        description="Enable rate limiting"
    )

    # ========================================================================
    # Application Configuration
    # ========================================================================

    environment: str = Field(
        default="development",
        alias="ENVIRONMENT",
        description="Environment name (development, staging, production)"
    )

    log_level: str = Field(
        default="INFO",
        alias="LOG_LEVEL",
        description="Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)"
    )

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level is valid."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        v_upper = v.upper()
        if v_upper not in valid_levels:
            raise ValueError(f"Log level must be one of: {valid_levels}")
        return v_upper

    debug: bool = Field(
        default=False,
        alias="DEBUG",
        description="Enable debug mode"
    )

    # ========================================================================
    # CORS Configuration
    # ========================================================================

    cors_origins: str = Field(
        default="*",
        alias="CORS_ORIGINS",
        description="Allowed CORS origins (comma-separated)"
    )

    @property
    def cors_origins_list(self) -> list[str]:
        """Parse CORS origins into list."""
        if self.cors_origins == "*":
            return ["*"]
        return [origin.strip() for origin in self.cors_origins.split(",")]

    # ========================================================================
    # Agent Configuration
    # ========================================================================

    agent_name: str = Field(
        default="TextbookAssistant",
        alias="AGENT_NAME",
        description="Agent name for identification"
    )

    agent_system_prompt: str = Field(
        default=(
            "You are a helpful AI assistant for a robotics textbook. "
            "Answer questions based ONLY on the provided context from the textbook. "
            "If the information is not in the context, say 'Information not found in the book.' "
            "Always cite sources using [Chapter X, Section Y.Z] format."
        ),
        alias="AGENT_SYSTEM_PROMPT",
        description="System prompt for the agent"
    )

    agent_timeout: int = Field(
        default=30,
        alias="AGENT_TIMEOUT",
        description="Agent response timeout in seconds"
    )

    # ========================================================================
    # Pydantic Settings Configuration
    # ========================================================================

    class Config:
        """Pydantic settings configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"  # Ignore extra fields in .env


# ============================================================================
# Global Settings Instance
# ============================================================================

_settings: Optional[Settings] = None


def get_settings(force_reload: bool = False) -> Settings:
    """
    Get or create the global settings instance.

    Args:
        force_reload: Force reload settings from environment

    Returns:
        Settings: Global settings singleton
    """
    global _settings

    if _settings is None or force_reload:
        _settings = Settings()

    return _settings


# ============================================================================
# Environment Detection
# ============================================================================

def is_production() -> bool:
    """Check if running in production environment."""
    settings = get_settings()
    return settings.environment.lower() == "production"


def is_development() -> bool:
    """Check if running in development environment."""
    settings = get_settings()
    return settings.environment.lower() == "development"


def is_debug_enabled() -> bool:
    """Check if debug mode is enabled."""
    settings = get_settings()
    return settings.debug or settings.environment.lower() == "development"


# ============================================================================
# Configuration Validation
# ============================================================================

def validate_configuration():
    """
    Validate all configuration settings.

    Raises:
        ValueError: If configuration is invalid
    """
    settings = get_settings()

    # Validate critical settings
    required_settings = [
        ("GEMINI_API_KEY", settings.gemini_api_key),
        ("QDRANT_URL", settings.qdrant_url),
        ("QDRANT_API_KEY", settings.qdrant_api_key),
        ("NEON_DATABASE_URL", settings.neon_database_url),
    ]

    missing = []
    for name, value in required_settings:
        if not value or value.strip() == "":
            missing.append(name)

    if missing:
        raise ValueError(
            f"Missing required configuration: {', '.join(missing)}. "
            f"Check your .env file or environment variables."
        )

    print("[OK] Configuration validation passed")


# ============================================================================
# Configuration Display
# ============================================================================

def display_configuration():
    """
    Display current configuration (with sensitive data masked).

    Useful for debugging and startup logging.
    """
    settings = get_settings()

    def mask_secret(value: str, show_chars: int = 4) -> str:
        """Mask sensitive value, showing only last N characters."""
        if len(value) <= show_chars:
            return "***"
        return "***" + value[-show_chars:]

    print("\n" + "=" * 60)
    print("Application Configuration")
    print("=" * 60)
    print(f"Environment:           {settings.environment}")
    print(f"Debug Mode:            {settings.debug}")
    print(f"Log Level:             {settings.log_level}")
    print()
    print("Gemini API:")
    print(f"  Model:               {settings.gemini_model}")
    print(f"  API Key:             {mask_secret(settings.gemini_api_key)}")
    print(f"  Max Tokens:          {settings.gemini_max_tokens}")
    print(f"  Temperature:         {settings.gemini_temperature}")
    print()
    print("Qdrant:")
    print(f"  URL:                 {settings.qdrant_url}")
    print(f"  API Key:             {mask_secret(settings.qdrant_api_key)}")
    print(f"  Collection:          {settings.qdrant_collection_name}")
    print()
    print("Neon PostgreSQL:")
    print(f"  Database URL:        {mask_secret(settings.neon_database_url, show_chars=10)}")
    print()
    print("Embedding:")
    print(f"  Model:               {settings.embedding_model}")
    print(f"  Dimension:           {settings.embedding_dimension}")
    print(f"  Device:              {settings.embedding_device}")
    print()
    print("Retrieval:")
    print(f"  Top-K:               {settings.retrieval_top_k}")
    print(f"  Score Threshold:     {settings.retrieval_score_threshold}")
    print()
    print("Rate Limiting:")
    print(f"  Enabled:             {settings.rate_limit_enabled}")
    print(f"  Per Minute:          {settings.rate_limit_per_minute}")
    print()
    print("CORS:")
    print(f"  Allowed Origins:     {settings.cors_origins_list}")
    print("=" * 60 + "\n")


# ============================================================================
# Example Usage
# ============================================================================

if __name__ == "__main__":
    """
    Example usage and testing of configuration management.
    """
    # Load settings
    settings = get_settings()

    # Display configuration
    display_configuration()

    # Validate configuration
    try:
        validate_configuration()
    except ValueError as e:
        print(f"Configuration error: {e}")

    # Access individual settings
    print(f"Using Gemini model: {settings.gemini_model}")
    print(f"Retrieval top-K: {settings.retrieval_top_k}")
    print(f"Running in {'production' if is_production() else 'development'} mode")
