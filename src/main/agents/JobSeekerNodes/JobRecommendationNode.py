from src.main.core.config import settings
from src.main.schemas.JobSearchState import JobSearchState, ScoredJobPosting

MIN_FIT_SCORE = settings.MIN_FIT_SCORE
MAX_RECOMMENDATIONS = settings.MAX_RECOMMENDATIONS

def job_recommendation_node(state: JobSearchState) -> dict:
    scored_jobs = state.scored_jobs or []

    # 1. Threshold
    eligible = [
        job for job in scored_jobs
        if job.fit_score >= MIN_FIT_SCORE
    ]

    # 2. Sort by fit score (desc), then reason count
    eligible.sort(
        key=lambda x: (x.fit_score, len(x.reasons)),
        reverse=True
    )

    # 3. Deduplicate by company (keep best)
    company_seen = set()
    recommendations = []

    for scored in eligible:
        company = scored.job.company.lower()
        if company in company_seen:
            continue

        company_seen.add(company)
        recommendations.append(scored)

        if len(recommendations) >= MAX_RECOMMENDATIONS:
            break

    return {
        "recommended_jobs": recommendations
    }
