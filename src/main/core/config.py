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
    company_registry:Path = Path("src/resources/companies.json")

    # jobs sites cofig
    MAX_JOBS_FROM_LINKEDIN:int = 10

    # career pages config
    MAX_COMPANIES:int = 3
    MAX_JOBS_PER_COMPANY:int = 10

    # recommendation configs
    MIN_FIT_SCORE: float = 0.45
    MAX_RECOMMENDATIONS: int = 5

    class Config:
        env_file = Path(__file__).resolve().parents[3] / ".env"

settings = Settings()