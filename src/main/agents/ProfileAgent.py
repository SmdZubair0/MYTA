from langgraph.graph import StateGraph, END, START

from src.main.agents.ProfileAgentNodes import *
from src.main.schemas.CareerState import CareerState
from src.main.schemas.ProfileProcessingState import ProfileProcessingState

# ======================================================
# BUILD COMPLETE PROFILE → CAREER STATE GRAPH
# ======================================================

def build_profile_processing_graph():
    """
        Full LangGraph for converting UserCareerProfile
        into CareerState using agentic processing.
    """

    graph = StateGraph(
        input=ProfileProcessingState,
        output=CareerState
    )

    # ----------------------------
    # Nodes
    # ----------------------------
    graph.add_node("education_summary", educationSummarizationNode)
    graph.add_node("experience_summary", experienceSummarizationNode)
    graph.add_node("project_summary", projectsSummarizationNode)

    graph.add_node("skills_summary", skillsSummarizationNode)

    graph.add_node("target_roles", targetRolesCreationNode)
    graph.add_node("strengths", strengthCreationNode)

    graph.add_node("skill_gaps", skillGapCreationNode)

    graph.add_node("career_state_assembler", career_state_assembler_node)

    # ----------------------------
    # ENTRY POINT
    # ----------------------------
    graph.set_entry_point(START)

    # ----------------------------
    # EDUCATION, EXPERIENCE AND PROJECTS
    # ----------------------------
    graph.add_edge(START, "education_summary")
    graph.add_edge(START, "experience_summary")
    graph.add_edge(START, "project_summary")

    # ----------------------------
    # SKILLS
    # ----------------------------
    graph.add_edge("experience_summary", "skills_summary")
    graph.add_edge("project_summary", "skills_summary")

    # ----------------------------
    # TARGET ROLES
    # ----------------------------
    graph.add_edge("skills_summary", "target_roles")
    
    # ----------------------------
    # TARGET ROLES
    # ----------------------------
    graph.add_edge("skills_summary", "strengths") # SINCE SKILLS ALREADY DEPENDS ON EXPERIENCE AND PROJECT, NOT INCLUDING HERE AGAIN

    # ----------------------------
    # SKILL GAPS
    # ----------------------------
    graph.add_edge("target_roles", "skill_gaps")
    graph.add_edge("strengths", "skill_gaps")

    # ----------------------------
    # FINAL ASSEMBLY
    # ----------------------------
    graph.add_edge("skill_gaps", "career_state_assembler")
    graph.add_edge("career_state_assembler", END)

    return graph.compile()
