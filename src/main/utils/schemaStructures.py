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

def format_education_for_prompt(education_list):
    lines = []
    for edu in education_list:
        line = f"{edu.degree} in {edu.field_of_study} from {edu.institution_name} ({edu.graduation_year})"
        lines.append(line)
    return "\n".join(lines)