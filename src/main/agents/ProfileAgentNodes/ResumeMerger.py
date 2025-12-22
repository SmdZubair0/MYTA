from copy import deepcopy

from src.main.schemas.UserCareerProfile import *

from src.main.utils.textHelpers import normalize_text
from src.main.schemas.UserCareerProfile import Project
from src.main.utils.timeHelpers import dates_overlap, parse_year_month
from src.main.schemas.ResumeExtraction import ResumeMergeInput, ResumeMergeOutput

def is_same_company(a, b) -> bool:
    return bool(
        normalize_text(a.company_name)
        and normalize_text(a.company_name) == normalize_text(b.company_name)
    )

def is_same_designation(a, b) -> bool:
    return bool(
        normalize_text(a.designation)
        and normalize_text(a.designation) == normalize_text(b.designation)
    )


def is_duplicate_experience(new, existing) -> bool:
    overlap = dates_overlap(
        parse_year_month(new.start_date),
        parse_year_month(existing.start_date),
        parse_year_month(new.end_date),
        parse_year_month(existing.end_date)
    )

    # Case 1: Same company + same designation + overlap
    if is_same_company(new, existing) and is_same_designation(new, existing) and overlap:
        return True

    # Case 2: Same company + overlap (promotion or role change handled later)
    if is_same_company(new, existing) and overlap:
        return True

    # Case 3: Company missing → designation + overlap
    if not normalize_text(new.company_name) and is_same_designation(new, existing) and overlap:
        return True

    return False

def project_matches(p1: Project, p2: Project) -> bool:
        return any([
            normalize_text(p1.title) == normalize_text(p2.title),
            p1.github_url and p2.github_url and p1.github_url == p2.github_url,
            p1.live_url and p2.live_url and p1.live_url == p2.live_url
        ])

def resumeMergeNode(state: ResumeMergeInput) -> ResumeMergeOutput:

    profile = deepcopy(state.existing_profile)
    resume = state.extracted_resume_data

    added_summary = {
        "education": 0,
        "experience": 0,
        "skills": 0,
        "projects": 0
    }

    # --------------------
    # EDUCATION MERGE
    # Rule: don't merge if college name exists
    # --------------------
    existing_colleges = {
        normalize_text(e.institution_name)
        for e in profile.education
    }

    for edu in resume.education:
        if normalize_text(edu.institution_name) not in existing_colleges:
            profile.education.append(edu)
            added_summary["education"] += 1

    # --------------------
    # EXPERIENCE MERGE
    # Rule: ignore if company OR designation OR duration overlaps
    # --------------------
    for exp in resume.experience:
        if not any(is_duplicate_experience(exp, existing) for existing in profile.experience):
            profile.experience.append(exp)
            added_summary["experience"] += 1


    # --------------------
    # SKILLS MERGE
    # Rule: add only missing skills
    # --------------------

    for category in profile.skills.model_fields.keys():
        profile_list = getattr(profile.skills, category, [])
        resume_list = getattr(resume.skills, category, [])

        existing_norm = {normalize_text(skill) for skill in profile_list}

        for skill in resume_list:
            if normalize_text(skill) not in existing_norm:
                profile_list.append(skill)
                added_summary["skills"] += 1


    # --------------------
    # PROJECTS MERGE
    # Rule: ignore if title OR github OR live url matches
    # --------------------

    for proj in resume.projects:
        if not any(project_matches(proj, existing) for existing in profile.projects):
            profile.projects.append(proj)
            added_summary["projects"] += 1

    return ResumeMergeOutput(
        updated_profile=profile,
        added_items_summary=added_summary
    )


if __name__ == "__main__":
    pass
    # userProfile = UserCareerProfile(
    #     basic_profile=BasicInfo(
    #         name="Zubair Shaik",
    #         current_locator="Bangalore, India"
    #     ),
    #     career_preferences=CareerPreferences(
    #         target_role="AI Engineer",
    #         career_goal_summary="Transitioning from automation engineering to AI/ML with focus on GenAI.",
    #         job_type_preference=["Full-time", "Hybrid"],
    #         preferred_locations=["Bangalore", "Hyderabad", "Remote"],
    #         current_ctc=8.5,
    #         expected_ctc=18.0
    #     ),
    #     education=[
    #         Education(
    #             institution_name="XYZ Institute of Technology",
    #             degree="B.Tech",
    #             field_of_study="Computer Science",
    #             graduation_year=2023,
    #             score_or_percentage=8.2
    #         )
    #     ],
    #     experience=[
    #         Experience(
    #             company_name="ABC Tech Solutions",
    #             designation="Associate Software Engineer",
    #             role_type="Automation Engineer",
    #             start_date="2023-07",
    #             end_date=None,
    #             responsibilities_summary="Built and maintained automation frameworks and integrated AI workflows.",
    #             tech_stack_used=["Python", "Selenium", "PyTest", "LangChain"]
    #         )
    #     ],
    #     skills=Skills(
    #         technical=["Python", "Machine Learning", "Deep Learning"],
    #         tools=["Git", "Docker", "Groq"],
    #         frameworks=["LangChain", "LangGraph", "FastAPI"],
    #         domains=["Automation", "GenAI"],
    #         soft_skills=["Problem Solving", "Communication"]
    #     ),
    #     online_presence=OnlinePresence(
    #         linkedin_url="https://www.linkedin.com/in/zubair",
    #         github_url="https://github.com/zubair",
    #         portfolio_url=None,
    #         blog_url=None
    #     ),
    #     projects=[
    #         Project(
    #             title="AI Resume Analyzer",
    #             description="LLM-based system to analyze resumes and recommend career paths.",
    #             role="AI Engineer",
    #             tech_stack=["Python", "LangChain", "Pydantic"],
    #             github_url="https://github.com/zubair/ai-resume-analyzer",
    #             live_url=None,
    #             duration="3 months"
    #         )
    #     ],
    #     resume=ResumeMetadata(
    #         file_name="Zubair_resume.pdf",
    #         uploaded_at="2025-03-01"
    #     ),
    #     constraints=Constraints(
    #         notice_period="30 days",
    #         open_to_realocation="Yes",
    #         preferred_company_type="Product-based"
    #     )
    # )

    # resumeData = ResumeMergeInput(
    #     existing_profile=userProfile,
    #     extracted_resume_data=ResumeExtractedData(
    #         education=[
    #             Education(
    #                 institution_name="G.Pullaiah College of Engineering and Technology",
    #                 degree="B.tech in Mechanical",
    #                 field_of_study="Mechanical",
    #                 graduation_year=2025,
    #                 score_or_percentage=72.7
    #             ),
    #             Education(
    #                 institution_name="Narayana Junior College, Kurnool",
    #                 degree="Intermediate (M.P.C)",
    #                 field_of_study="",
    #                 graduation_year=2021,
    #                 score_or_percentage=65.6
    #             ),
    #             Education(
    #                 institution_name="KVR English Medium High School, Kurnool",
    #                 degree="10th (SSC)",
    #                 field_of_study="",
    #                 graduation_year=2019,
    #                 score_or_percentage=83.0
    #             )
    #         ],
    #         experience=[
    #             Experience(
    #                 company_name="",
    #                 designation="Intern - Full Stack Development (MERN)",
    #                 role_type="",
    #                 start_date="2025-05",
    #                 end_date="2025-07",
    #                 responsibilities_summary=(
    #                     "Designed and developed responsive UI components using ReactJS, "
    #                     "HTML, CSS, and JavaScript. Gained hands-on experience on a real-time project."
    #                 ),
    #                 tech_stack_used=["ReactJS", "HTML", "CSS", "JavaScript"]
    #             )
    #         ],
    #         skills=Skills(
    #             technical=["Java", "HTML", "CSS", "JavaScript"],
    #             tools=["Excel", "MySQL", "AutoCAD"],
    #             frameworks=["React JS"],
    #             domains=[],
    #             soft_skills=[
    #                 "Team & Time Management",
    #                 "Leadership",
    #                 "Problem Solving",
    #                 "Excellent communication"
    #             ]
    #         ),
    #         projects=[
    #             Project(
    #                 title="Netflix clone",
    #                 description=(
    #                     "A fully responsive and user-friendly Netflix clone using HTML, CSS, "
    #                     "optimized for performance across various devices."
    #                 ),
    #                 role=None,
    #                 tech_stack=["HTML", "CSS"],
    #                 github_url=None,
    #                 live_url=None,
    #                 duration=None
    #             ),
    #             Project(
    #                 title="Web based Rock, Paper and Scissor game",
    #                 description=(
    #                     "An interactive command-line game using HTML, CSS, & JavaScript, "
    #                     "with game logic, score tracking, and replay functionality."
    #                 ),
    #                 role=None,
    #                 tech_stack=["HTML", "CSS", "JavaScript"],
    #                 github_url=None,
    #                 live_url=None,
    #                 duration=None
    #             )
    #         ]
    #     )
    # )

    # print(ResumeMergeNode(resumeData))