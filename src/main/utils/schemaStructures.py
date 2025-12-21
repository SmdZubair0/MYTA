from typing import List

from src.main.schemas.UserCareerProfile import Skills

def flatten_skills(skills: Skills) -> List[str]:
    return [
        *skills.technical,
        *skills.tools,
        *skills.frameworks,
        *skills.domains,
        *skills.soft_skills,
    ]