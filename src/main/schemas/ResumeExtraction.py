from typing import List, Dict
from pydantic import BaseModel

from src.main.schemas.UserCareerProfile import *

class ResumeExtractionInput(BaseModel):
    file_name: str
    text: Optional[str] = None

class ResumeExtractedData(BaseModel):
    education: List[Education] = []
    experience: List[Experience] = []
    skills: Skills = Skills()
    projects: List[Project] = []

class ResumeMergeInput(BaseModel):
    existing_profile: UserCareerProfile
    extracted_resume_data: ResumeExtractedData

class ResumeMergeOutput(BaseModel):
    updated_profile: UserCareerProfile
    added_items_summary: Dict[str, int]  # transparency