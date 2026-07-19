"""Runtime configuration: one place to swap providers, models, and paths.

Provider credentials use their native environment names (OPENAI_API_KEY,
GROQ_API_KEY) so SDK conventions and shell habits keep working; app-level
knobs take the SB_ prefix (e.g. SB_CHAT_MODEL, SB_DATA_DIR).
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="SB_", extra="ignore")

    # Credentials — native env names via explicit aliases.
    openai_api_key: SecretStr | None = Field(default=None, validation_alias="OPENAI_API_KEY")
    groq_api_key: SecretStr | None = Field(default=None, validation_alias="GROQ_API_KEY")

    # Cognitive task models, we might use a stronger model for segmentation.
    chat_model: str = "gpt-5-mini"
    segmenter_model: str = "gpt-5-mini"
    embed_model: str = "text-embedding-3-large"
    embed_dim: int = 1536  # Matryoshka truncation; SB_EMBED_DIM overrides

    # Retrieval funnel (thresholds provisional until Phase 3 calibration)
    rerank_model: str = "BAAI/bge-reranker-v2-m3"
    rerank_top: int = 20
    answer_top: int = 5
    tau_high: float = 0.6
    tau_low: float = 0.2

    @property
    def index_path(self) -> Path:
        return self.data_dir / "index.db"

    # Storage layout. `data_dir` is the root; everything below derives from it.
    data_dir: Path = Path("data")

    @property
    def notes_dir(self) -> Path:
        return self.data_dir / "notes"

    @property
    def transcripts_dir(self) -> Path:
        return self.data_dir / "transcripts"

    @property
    def traces_dir(self) -> Path:
        return self.data_dir / "traces"


@lru_cache
def get_settings() -> Settings:
    """Cached accessor — import this, never a module-level instance."""
    return Settings()