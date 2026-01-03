import json
from urllib.parse import quote_plus

from main.utils import PromptReader
from src.main.agents.LLMClient import LLMClient
from src.main.utils.textHelpers import extract_json
from src.main.schemas.CareerState import CareerState
from src.resources.mockData.jobPostings import MOCK_JOBS
from src.main.schemas.JobSearchState import JobSearchState, JobPosting

promptReader = PromptReader()
JOB_SEARCH_INTENT_PROMPT = promptReader.read("job intent")

def build_job_queries(career: CareerState) -> list[str]:
    llm_response = LLMClient.generate(
        prompt=JOB_SEARCH_INTENT_PROMPT
            .replace("{{target_roles}}", ", ".join(career.target_roles))
            .replace("{{career_stage}}", career.career_stage)
            .replace("{{skills_summary}}", ", ".join(career.skills_summary))
            .replace("{{preferred_locations}}", ", ".join(career.preferred_locations or []))
            .replace("{{job_type_preference}}", ", ".join(career.job_type_preference))
    )

    try:
        search_queries = extract_json(llm_response).get("search_queries", [])
    except json.JSONDecodeError:
        return []
    
    return search_queries

def build_linkedin_search_urls(search_queries: list[str]) -> list[str]:
    base_url = "https://www.linkedin.com/jobs/search/?keywords="

    urls = []
    for query in search_queries:
        encoded_query = quote_plus(query)
        urls.append(f"{base_url}{encoded_query}")

    return urls

def discover_jobs_from_mock(search_queries: list[str]) -> list[JobPosting]:
    ### this is for mock data only
    discovered = []

    for job in MOCK_JOBS:
        for query in search_queries:
            if query.lower() in job["title"].lower():
                discovered.append(JobPosting(**job))
                break

    return discovered


def job_search_intent_node(state: JobSearchState) -> dict:
    career = state.career_state

    search_queries = build_job_queries(career)
    urls = build_linkedin_search_urls(search_queries)
    discovered_jobs = discover_jobs_from_mock(search_queries)
    normalized_jobs = list(discovered_jobs)  # ToDo: write a function to do this.

    return {
        "search_queries": search_queries,
        "search_urls": urls,
        "discovered_jobs": discovered_jobs,
        "normalized_jobs": normalized_jobs
    }
