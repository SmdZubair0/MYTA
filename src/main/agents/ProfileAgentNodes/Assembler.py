from datetime import datetime
from langgraph.graph import StateGraph, END

from src.main.schemas.CareerState import CareerState
from src.main.schemas.UserCareerProfile import UserCareerProfile
from src.main.schemas.ProfileProcessingState import ProfileProcessingState


def career_state_assembler_node(state: ProfileProcessingState) -> CareerState:
    """
    Final assembler node.
    Converts ProfileProcessingState into a persisted CareerState.
    No AI calls. Deterministic only.
    """

    user: UserCareerProfile = state.user_profile

    return CareerState(
        # ---- Direct fields from user profile ----
        name=user.basic_profile.name,
        current_location=user.basic_profile.current_location,
        job_type_preference=user.career_preferences.job_type_preference,
        preferred_locations=user.career_preferences.preferred_locations,
        current_ctc=user.career_preferences.current_ctc,
        expected_ctc=user.career_preferences.expected_ctc,
        online_presence_urls=[
            user.online_presence.linkedin_url,
            user.online_presence.github_url,
            user.online_presence.portfolio_url,
            user.online_presence.blog_url,
        ] if user.online_presence else [],

        # ---- Derived intelligence fields ----
        target_roles=state.target_roles,
        education_summary=state.education_summary,
        experience_summaries=state.experience_summaries,
        project_summaries=state.project_summaries,
        skills_summary=state.skills_summary,
        strengths=state.strengths,
        skill_gaps=state.skill_gaps,
        career_stage=state.career_stage,

        # ---- Metadata ----
        last_updated=datetime.now()
    )


def build_career_state_assembler_graph():
    """
    LangGraph that only contains the final assembler.
    Input: ProfileProcessingState
    Output: CareerState
    """

    graph = StateGraph(
        input=ProfileProcessingState,
        output=CareerState
    )

    graph.add_node("career_state_assembler", career_state_assembler_node)
    graph.set_entry_point("career_state_assembler")
    graph.add_edge("career_state_assembler", END)

    return graph.compile()
