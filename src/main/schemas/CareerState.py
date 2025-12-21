from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional

class CareerState(BaseModel):
    name: str
    current_location: str

    target_roles: List[str]
    job_type_preference: List[str]
    preferred_locations: Optional[List[str]] = None

    current_ctc: Optional[float] = None
    expected_ctc: Optional[float] = None

    education_summary: str
    experience_summaries: List[str]

    skills_summary: List[str]

    project_summaries: Optional[List[str]] = None

    online_presence_urls: List[str]

    career_stage: str  # junior / mid / senior
    strengths: List[str]
    skill_gaps: List[str]

    last_updated: datetime