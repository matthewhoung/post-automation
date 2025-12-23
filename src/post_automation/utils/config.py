"""Configuration management using pydantic-settings."""

from functools import lru_cache
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # HuggingFace Configuration
    hf_token: str = Field(..., description="HuggingFace API token")
    hf_model_name: str = Field(
        default="roberta-base-openai-detector", description="HuggingFace model for AI detection"
    )

    # API Configuration
    api_host: str = Field(default="0.0.0.0", description="FastAPI host")
    api_port: int = Field(default=8000, description="FastAPI port")
    api_workers: int = Field(default=4, description="Number of API workers")
    api_reload: bool = Field(default=False, description="Enable auto-reload")

    # Streamlit Configuration
    streamlit_port: int = Field(default=8501, description="Streamlit port")
    streamlit_server_address: str = Field(default="0.0.0.0", description="Streamlit server address")

    # File Upload Configuration
    max_upload_size_mb: int = Field(default=10, description="Maximum file upload size in MB")
    allowed_ppt_extensions: str = Field(default=".pptx,.ppt", description="Allowed PowerPoint extensions")

    # Logging Configuration
    log_level: str = Field(default="INFO", description="Logging level")
    log_format: str = Field(default="json", description="Logging format")

    # CORS Configuration
    cors_origins: str = Field(default="*", description="CORS allowed origins")

    # Temp File Storage
    temp_dir: str = Field(default="/tmp/post-automation", description="Temporary file directory")

    @property
    def max_upload_size_bytes(self) -> int:
        """Get maximum upload size in bytes."""
        return self.max_upload_size_mb * 1024 * 1024

    @property
    def cors_origins_list(self) -> List[str]:
        """Get CORS origins as a list."""
        return [origin.strip() for origin in self.cors_origins.split(",")]

    @property
    def allowed_extensions_list(self) -> List[str]:
        """Get allowed PowerPoint extensions as a list."""
        return [ext.strip() for ext in self.allowed_ppt_extensions.split(",")]


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
