import json

from src.main.agents.LLMClient import LLMClient
from src.main.utils.textHelpers import extract_json
from src.main.utils.PromptReader import PromptReader
from src.main.schemas.JobSearchState import JobSearchState, ScoredJobPosting

promptReader = PromptReader()
JOB_FIT_SCORE_PROMPT = promptReader.read("job fit score")

def job_fit_scoring_node(state: JobSearchState) -> dict:
    career = state.career_state
    scored = []

    for job in state.filtered_jobs:
        llm_response = LLMClient.generate(
            prompt=JOB_FIT_SCORE_PROMPT
                .replace("{{target_roles}}", ", ".join(career.target_roles))
                .replace("{{career_stage}}", career.career_stage)
                .replace("{{skills_summary}}", ", ".join(career.skills_summary))
                .replace("{{strengths}}", ", ".join(career.strengths))
                .replace("{{job_title}}", job.title)
                .replace("{{job_stage}}", job.career_stage)
                .replace("{{job_description}}", job.description or "")
        )

        try:
            structured_data = extract_json(llm_response)
        except json.JSONDecodeError:
            continue

        scored.append(
            ScoredJobPosting(
                job=job,
                fit_score=structured_data.get("fit_score", 0.0),
                fit_level=structured_data.get("fit_level", "medium"),
                reasons=structured_data.get("reasons", []),
                missing_requirements=structured_data.get("missing_requirements", [])
            )
        )

    return {
        "scored_jobs": scored
    }
