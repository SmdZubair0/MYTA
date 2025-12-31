from langgraph.graph import StateGraph, START, END

from src.main.schemas.JobSearchState import JobSearchState

# Nodes
from src.main.agents.JobSeekerNodes.JobFilterNode import job_filter_node
from src.main.agents.JobSeekerNodes.JobFitScoreNode import job_fit_scoring_node
from main.agents.JobSeekerNodes.JobSearcherNode import job_search_intent_node
from src.main.agents.JobSeekerNodes.JobRecommendationNode import job_recommendation_node


def build_job_search_graph():
    """
    LangGraph for Job Seeker Agent
    Input  : JobSearchState (with CareerState injected)
    Output : JobSearchState (with recommended_jobs populated)
    """

    graph = StateGraph(
        input=JobSearchState,
        output=JobSearchState
    )

    # ----------------------------
    # Add nodes
    # ----------------------------
    graph.add_node("job_search", job_search_intent_node)
    graph.add_node("job_filter", job_filter_node)
    graph.add_node("job_fit_scoring", job_fit_scoring_node)
    graph.add_node("job_recommendation", job_recommendation_node)

    # ----------------------------
    # Entry point
    # ----------------------------
    graph.set_entry_point(START)

    # ----------------------------
    # Edges
    # ----------------------------
    graph.add_edge(START, "job_search")
    graph.add_edge("job_search", "job_filter")
    graph.add_edge("job_filter", "job_fit_scoring")
    graph.add_edge("job_fit_scoring", "job_recommendation")
    graph.add_edge("job_recommendation", END)

    return graph.compile()
