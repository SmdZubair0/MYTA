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

def format_experience_for_prompt(experiences):
    lines = []
    for exp in experiences:
        line = (
            f"Company: {exp.company_name or 'N/A'}, "
            f"Role: {exp.designation}, "
            f"Duration: {exp.start_date} to {exp.end_date or 'Present'}, "
            f"Summary: {exp.responsibilities_summary or 'N/A'}"
        )
        lines.append(line)
    return "\n".join(lines)