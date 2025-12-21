from datetime import date
from src.main.schemas.ResumeExtraction import *
from src.main.schemas.UserCareerProfile import *

resume_extraction_input = ResumeExtractionInput(
    userProfile=UserCareerProfile(
        basic_profile=BasicInfo(
            name="Zubair Shaik",
            current_locator="Bangalore, India"
        ),
        career_preferences=CareerPreferences(
            target_role="AI Engineer",
            career_goal_summary="Transitioning from automation engineering to AI/ML with focus on GenAI.",
            job_type_preference=["Full-time", "Hybrid"],
            preferred_locations=["Bangalore", "Hyderabad", "Remote"],
            current_ctc=8.5,
            expected_ctc=18.0
        ),
        education=[
            Education(
                institution_name="XYZ Institute of Technology",
                degree="B.Tech",
                field_of_study="Computer Science",
                graduation_year=2023,
                score_or_percentage=8.2
            )
        ],
        experience=[
            Experience(
                company_name="ABC Tech Solutions",
                designation="Associate Software Engineer",
                role_type="Automation Engineer",
                start_date=date(2023, 7, 1),
                end_date=None,
                responsibilities_summary="Built and maintained automation frameworks and integrated AI workflows.",
                tech_stack_used=["Python", "Selenium", "PyTest", "LangChain"]
            )
        ],
        skills=Skills(
            technical=["Python", "Machine Learning", "Deep Learning"],
            tools=["Git", "Docker", "Groq"],
            frameworks=["LangChain", "LangGraph", "FastAPI"],
            domains=["Automation", "GenAI"],
            soft_skills=["Problem Solving", "Communication"]
        ),
        online_presence=OnlinePresence(
            linkedin_url="https://www.linkedin.com/in/zubair",
            github_url="https://github.com/zubair",
            portfolio_url=None,
            blog_url=None
        ),
        projects=[
            Project(
                title="AI Resume Analyzer",
                description="LLM-based system to analyze resumes and recommend career paths.",
                role="AI Engineer",
                tech_stack=["Python", "LangChain", "Pydantic"],
                github_url="https://github.com/zubair/ai-resume-analyzer",
                live_url=None,
                duration="3 months"
            )
        ],
        resume=ResumeMetadata(
            file_name="Zubair_resume.pdf",
            uploaded_at="2025-03-01"
        ),
        constraints=Constraints(
            notice_period="30 days",
            open_to_realocation="Yes",
            preferred_company_type="Product-based"
        )
    )
)
