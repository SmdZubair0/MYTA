from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # keys
    groq_api_key : str

    # LLM Client
    LLM_Model: str = "llama-3.3-70b-versatile"
    temerature: float = 0.2
    timeout : int = 30

    # Paths
    promptsPath:Path = Path("src/resources/prompts/")
    resumesPath:Path = Path("src/resources/resumes")

    # recommendation configs
    MIN_FIT_SCORE: float = 0.45
    MAX_RECOMMENDATIONS: int = 5

    class Config:
        env_file = Path(__file__).resolve().parents[3] / ".env"

settings = Settings()