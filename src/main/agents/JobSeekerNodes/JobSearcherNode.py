import json
from typing import List
from urllib.parse import quote, quote_plus
from dotenv import load_dotenv

from src.main.utils.PromptReader import PromptReader
from src.main.agents.LLMClient import LLMClient
from src.main.utils.textHelpers import extract_json
from src.main.schemas.CareerState import CareerState
from src.main.schemas.JobSearchState import JobSearchState, JobSearchTarget

from src.resources.mockData.careerState import career, queries

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

def build_linkedin_urls(queries: List[str]) -> List[str]:
    base = "https://www.linkedin.com/jobs/search/?keywords="
    return [base + quote_plus(q) for q in queries]


def build_indeed_urls(queries: List[str]) -> List[str]:
    base = "https://www.indeed.com/jobs?q="
    return [base + quote_plus(q) for q in queries]


def build_google_jobs_urls(queries: List[str]) -> List[str]:
    base = "https://www.google.com/search?q="
    return [base + quote_plus(f"{q} jobs") for q in queries]

def build_job_search_targets(queries: List[str]) -> list[JobSearchTarget]:
    targets = []

    for q in queries:
        targets.extend([
            JobSearchTarget(
                source="linkedin",
                query=q,
                search_url=f"https://www.linkedin.com/jobs/{'-'.join(q.split())}"
            ),
            # JobSearchTarget(
            #     source="indeed",
            #     query=q,
            #     search_url=f"https://www.indeed.com/jobs?q={quote_plus(q)}"
            # ),
            # JobSearchTarget(
            #     source="naukri",
            #     query=q,
            #     search_url=f"https://www.naukri.com/{quote_plus(q)}-jobs"
            # )
        ])

    return targets


def job_search_intent_node(state: JobSearchState) -> dict:
    career = state.career_state

    search_queries = build_job_queries(career)
    targets = build_job_search_targets(search_queries)

    return {
        "search_queries": search_queries,
        "search_targets": targets
    }


if __name__ == "__main__":
    load_dotenv()
    print(build_job_search_targets(queries))
    # state = JobSearchState(career_state=career)
    # print(build_job_queries(career))
    # print(build_job_search_targets(queries))