import json
from dotenv import load_dotenv

from src.main.agents import LLMClient
from src.main.utils.textHelpers import extract_json
from src.main.utils.PromptReader import PromptReader
from src.main.schemas.ProfileProcessingState import ProfileProcessingState

promptReader = PromptReader()
TARGET_ROLE_PROMPT = promptReader.read("target roles")

def targetRolesCreationNode(ProfileState : ProfileProcessingState) -> ProfileProcessingState:
    state = ProfileState.user_profile
    
    llm_response = LLMClient.generate(
        prompt=TARGET_ROLE_PROMPT
        .replace("{{target_role}}", state.career_preferences.target_role)
        .replace("{{career_goal_summary}}", state.career_preferences.career_goal_summary)
        .replace("{{career_stage}}", ProfileState.career_stage)
        .replace("{{skills_summary}}", ", ".join(ProfileState.skills_summary))
        .replace("{{expected_ctc}}", str(state.career_preferences.expected_ctc))
    )

    try:
        structured_data = extract_json(llm_response)
    except json.JSONDecodeError:
        return {"target_roles" : []}

    return {
        "target_roles" : structured_data.get("target_roles",[])
    }


if __name__ == "__main__":
    load_dotenv()
    # userProfile = ProfileProcessingState(
    #     user_profile=UserCareerProfile(
    #         basic_profile=BasicInfo(
    #             name="Zubair Shaik",
    #             current_locator="Bangalore, India"
    #         ),

    #         career_preferences=CareerPreferences(
    #             target_role="AI Engineer",
    #             career_goal_summary=(
    #                 "Transitioning from automation engineering to AI/ML "
    #                 "with focus on GenAI."
    #             ),
    #             job_type_preference=["Full-time", "Hybrid"],
    #             preferred_locations=["Bangalore", "Hyderabad", "Remote"],
    #             current_ctc=8.5,
    #             expected_ctc=18.0
    #         ),

    #         education=[
    #             Education(
    #                 institution_name="XYZ Institute of Technology",
    #                 degree="B.Tech",
    #                 field_of_study="Computer Science",
    #                 graduation_year=2023,
    #                 score_or_percentage=8.2
    #             ),
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
    #                 company_name="ABC Tech Solutions",
    #                 designation="Associate Software Engineer",
    #                 role_type="Automation Engineer",
    #                 start_date="2023-07",
    #                 end_date="",
    #                 responsibilities_summary=(
    #                     "Built and maintained automation frameworks "
    #                     "and integrated AI workflows."
    #                 ),
    #                 tech_stack_used=[
    #                     "Python",
    #                     "Selenium",
    #                     "PyTest",
    #                     "LangChain"
    #                 ]
    #             ),
    #             Experience(
    #                 company_name="",
    #                 designation="Intern - Full Stack Development (MERN)",
    #                 role_type="",
    #                 start_date="2025-05",
    #                 end_date="2025-07",
    #                 responsibilities_summary=(
    #                     "Designed and developed responsive UI components "
    #                     "using ReactJS, HTML, CSS, and JavaScript. "
    #                     "Gained hands-on experience on a real-time project."
    #                 ),
    #                 tech_stack_used=[
    #                     "ReactJS",
    #                     "HTML",
    #                     "CSS",
    #                     "JavaScript"
    #                 ]
    #             )
    #         ],

    #         skills=Skills(
    #             technical=[
    #                 "Python",
    #                 "Machine Learning",
    #                 "Deep Learning",
    #                 "Java",
    #                 "HTML",
    #                 "CSS",
    #                 "JavaScript"
    #             ],
    #             tools=[
    #                 "Git",
    #                 "Docker",
    #                 "Groq",
    #                 "Excel",
    #                 "MySQL",
    #                 "AutoCAD"
    #             ],
    #             frameworks=[
    #                 "LangChain",
    #                 "LangGraph",
    #                 "FastAPI",
    #                 "React JS"
    #             ],
    #             domains=[
    #                 "Automation",
    #                 "GenAI"
    #             ],
    #             soft_skills=[
    #                 "Problem Solving",
    #                 "Communication",
    #                 "Team & Time Management",
    #                 "Leadership",
    #                 "Excellent communication"
    #             ]
    #         ),

    #         online_presence=OnlinePresence(
    #             linkedin_url="https://www.linkedin.com/in/zubair",
    #             github_url="https://github.com/zubair",
    #             portfolio_url="",
    #             blog_url=""
    #         ),

    #         projects=[
    #             Project(
    #                 title="AI Resume Analyzer",
    #                 description=(
    #                     "LLM-based system to analyze resumes "
    #                     "and recommend career paths."
    #                 ),
    #                 role="AI Engineer",
    #                 tech_stack=[
    #                     "Python",
    #                     "LangChain",
    #                     "Pydantic"
    #                 ],
    #                 github_url="https://github.com/zubair/ai-resume-analyzer",
    #                 live_url=None,
    #                 duration="3 months"
    #             ),
    #             Project(
    #                 title="Netflix clone",
    #                 description=(
    #                     "A fully responsive and user-friendly Netflix clone "
    #                     "using HTML, CSS, optimized for performance "
    #                     "across various devices."
    #                 ),
    #                 role="",
    #                 tech_stack=["HTML", "CSS"],
    #                 github_url=None,
    #                 live_url=None,
    #                 duration=""
    #             ),
    #             Project(
    #                 title="Web based Rock, Paper and Scissor game",
    #                 description=(
    #                     "An interactive command-line game using HTML, CSS, "
    #                     "& JavaScript, with game logic, score tracking, "
    #                     "and replay functionality."
    #                 ),
    #                 role="",
    #                 tech_stack=["HTML", "CSS", "JavaScript"],
    #                 github_url=None,
    #                 live_url=None,
    #                 duration=""
    #             )
    #         ],

    #         resume=ResumeMetadata(
    #             file_name="Zubair_resume.pdf",
    #             uploaded_at="2025-03-01"
    #         ),

    #         constraints=Constraints(
    #             notice_period="30 days",
    #             open_to_realocation="Yes",
    #             preferred_company_type="Product-based"
    #         )
    #     ),
    #     education_summary=(
    #         "B.Tech in Computer Science from XYZ Institute of Technology (2023) "
    #         "and B.Tech in Mechanical from G.Pullaiah College of Engineering and Technology (2025), "
    #         "with prior education including Intermediate (M.P.C) from Narayana Junior College, "
    #         "Kurnool (2021) and 10th (SSC) from KVR English Medium High School, Kurnool (2019)."
    #     ),
    #     experience_summaries=[
    #         "Associate Software Engineer at ABC Tech Solutions, building and maintaining automation frameworks and AI workflows.",
    #         "Interned in Full Stack Development, designing and developing responsive UI components using MERN stack."
    #     ],
    #     career_stage="junior",
    #     project_summaries=[
    #         "Developed an LLM-based system to analyze resumes and recommend career paths with code available on GitHub",
    #         "Built a fully responsive and user-friendly Netflix clone using HTML and CSS",
    #         "Created an interactive Rock, Paper and Scissor game using HTML, CSS, and JavaScript"
    #     ],
    #     skills_summary=[
    #         'JavaScript', 'HTML', 'CSS', 'Python', 'Java', 'Git', 'Docker', 'MySQL', 'React JS', 'Machine Learning', 'Deep Learning', 'Automation', 'FastAPI']
    # )
    # print(targetRolesCreationNode(userProfile))