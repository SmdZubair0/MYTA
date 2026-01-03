import json

from src.main.agents.LLMClient import LLMClient
from src.main.utils.textHelpers import extract_json
from src.main.utils.PromptReader import PromptReader
from src.main.schemas.JobSearchState import JobSearchState, ScoredJobPosting

promptReader = PromptReader()
JOB_FIT_SCORE_PROMPT = promptReader.read("job fit score")

MAX_JOBS_TO_SCORE = 15
DEFAULT_SCORE = 0.5

def normalize_score(value) -> float:
    try:
        score = float(value)
    except Exception:
        return DEFAULT_SCORE

    # Normalize common ranges
    if score > 1:
        score = score / 100 if score <= 100 else DEFAULT_SCORE

    return max(0.0, min(score, 1.0))


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
            data = extract_json(llm_response)
            fit_score = normalize_score(data.get("fit_score"))
            fit_level = data.get("fit_level", "medium")
            reasons = data.get("reasons", [])
            missing = data.get("missing_requirements", [])

        except Exception:
            # Fallback scoring
            fit_score = DEFAULT_SCORE
            fit_level = "medium"
            reasons = ["Automatic fallback score"]
            missing = []

        scored.append(
            ScoredJobPosting(
                job=job,
                fit_score=fit_score,
                fit_level=fit_level,
                reasons=reasons,
                missing_requirements=missing
            )
        )

    return {
        "scored_jobs": scored
    }
