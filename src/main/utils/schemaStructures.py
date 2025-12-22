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

def format_projects_for_prompt(projects):
    lines = []
    for p in projects:
        line = (
            f"Title: {p.title}, "
            f"Description: {p.description}, "
            f"Tech: {', '.join(p.tech_stack)}, "
            f"Live URL: {'yes' if p.live_url else 'no'}, "
            f"GitHub URL: {'yes' if p.github_url else 'no'}"
        )
        lines.append(line)
    return "\n".join(lines)


def format_skills_for_prompt(skills):
    collected = []

    # From explicit skills section
    for category, values in skills.model_dump().items():
        collected.extend(values)
    
    return ", ".join(set(collected))


def format_skills_from_experience_for_prompt(experience):
    collected = []
    # From experience tech stack
    for exp in experience:
        collected.extend(exp.tech_stack_used or [])
    
    return ", ".join(set(collected))


def format_skills_from_projects_for_prompt(projects):
    collected = []
    # From project tech stack
    for proj in projects:
        collected.extend(proj.tech_stack)

    return ", ".join(set(collected))
