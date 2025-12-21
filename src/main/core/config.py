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
    careerStatePromptsPath:Path = Path("src/resources/prompts/CareerStatePrompts")
    resumesPath:Path = Path("src/resources/resumes")

    class Config:
        env_file = Path(__file__).resolve().parents[3] / ".env"

settings = Settings()