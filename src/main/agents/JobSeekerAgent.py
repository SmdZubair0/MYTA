from langgraph.graph import StateGraph, START, END

from src.main.schemas.JobSearchState import JobSearchState

from src.main.agents.JobSeekerNodes.JobsFoundNode import return_found_jobs
from src.main.agents.JobSeekerNodes.JobSearcherNode import job_search_intent_node
from src.main.agents.JobSeekerNodes.JobDiscoverySitesNode import job_discovery_node
from src.main.agents.JobSeekerNodes.JobDiscoveryCareerPagesNode import company_job_discovery_node
from src.main.agents.JobSeekerNodes.JobNormalizingNode import job_normalization_node
from src.main.agents.JobSeekerNodes.JobFilterNode import job_filter_node
from src.main.agents.JobSeekerNodes.JobFitScoreNode import job_fit_scoring_node
from src.main.agents.JobSeekerNodes.JobRecommendationNode import job_recommendation_node


def build_job_search_graph():
    """
    LangGraph for Job Seeker Agent
    Input  : JobSearchState (career_state injected)
    Output : JobSearchState (recommended_jobs populated)
    """

    graph = StateGraph(
        input=JobSearchState,
        output=JobSearchState
    )

    # ----------------------------
    # Nodes
    # ----------------------------
    graph.add_node("job_search", job_search_intent_node)

    graph.add_node("discover_from_sites", job_discovery_node)
    graph.add_node("discover_from_companies", company_job_discovery_node)

    graph.add_node("normalize_jobs", job_normalization_node)
    graph.add_node("filter_jobs", job_filter_node)
    graph.add_node("score_jobs", job_fit_scoring_node)
    graph.add_node("recommend_jobs", job_recommendation_node)
    graph.add_node("found_jobs", return_found_jobs)

    # ----------------------------
    # Entry
    # ----------------------------
    graph.set_entry_point(START)

    # ----------------------------
    # Flow
    # ----------------------------

    # 1. Build search intent
    graph.add_edge(START, "job_search")
    graph.add_edge(START, "discover_from_companies")

    # 2. Parallel discovery (both append to raw_job_postings)
    graph.add_edge("job_search", "discover_from_sites")

    # 3. Normalize AFTER both discoveries
    graph.add_edge("discover_from_sites", "normalize_jobs")
    graph.add_edge("discover_from_companies", "normalize_jobs")

    # 4. Filter → score → recommend
    graph.add_edge("normalize_jobs", "filter_jobs")
    graph.add_edge("filter_jobs", "score_jobs")
    graph.add_edge("score_jobs", "recommend_jobs")
    graph.add_edge("recommend_jobs", "found_jobs")
    graph.add_edge("found_jobs", END)

    return graph.compile()
