from typing import List, Optional
from pydantic import BaseModel
from src.main.schemas.UserCareerProfile import UserCareerProfile


class ProfileProcessingState(BaseModel):
    user_profile: UserCareerProfile

    # Generated fields (start empty)
    target_roles: List[str] = []
    education_summary: str = ""
    experience_summaries: List[str] = []
    career_stage: str = ""
    project_summaries: List[str] = []
    skills_summary: List[str] = []
    strengths: List[str] = []
