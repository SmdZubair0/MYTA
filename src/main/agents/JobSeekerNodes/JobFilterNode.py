from src.main.utils.textHelpers import normalize_text
from src.main.schemas.JobSearchState import JobSearchState, RejectedJob, SalaryRange

def job_type_allowed(job_type: str, preferences: list[str]) -> bool:
    job = normalize_text(job_type)
    prefs = {normalize_text(p) for p in preferences}

    # If user selected hybrid → allow everything
    if "hybrid" in prefs:
        return True

    # Otherwise, strict match
    return job in prefs


def career_stage_mismatch(user_stage: str, job_stage: str) -> bool:
    user_stage = normalize_text(user_stage)
    job_stage = normalize_text(job_stage)

    if job_stage == "unknown":
        return False

    if user_stage == "junior":
        return job_stage in ["mid", "senior"]

    if user_stage == "mid":
        return job_stage == "senior"

    if user_stage == "senior":
        return job_stage == "junior"

    return False


def salary_mismatch(job_salary: SalaryRange | None, expected_ctc: float | None) -> bool:
    if not job_salary or not expected_ctc:
        return False

    min_sal, max_sal = job_salary.min, job_salary.max

    if max_sal < 0.7 * expected_ctc:
        return True
    if min_sal > 1.3 * expected_ctc:
        return True

    return False


def role_mismatch(job_title: str, target_roles: list[str], skills: list[str]) -> bool:
    title = normalize_text(job_title)

    if any(normalize_text(role) in title for role in target_roles):
        return False

    if any(normalize_text(skill) in title for skill in skills[:10]):
        return False

    return True



def job_filter_node(state: JobSearchState) -> dict:
    career = state.career_state
    filtered, rejected = [], []

    for job in state.normalized_jobs:
        reasons = []

        # Job type
        if not job_type_allowed(job.job_type, career.job_type_preference):
            reasons.append("Job type mismatch")

        # Location
        if career.preferred_locations and normalize_text(job.job_type) in ['onsite', 'hybrid']:
            if not any(loc.lower() in job.location.lower() for loc in career.preferred_locations):
                reasons.append("Location mismatch")

        # Career stage
        if career_stage_mismatch(career.career_stage, job.career_stage):
            reasons.append("Career stage mismatch")

        # Target role relevance
        if role_mismatch(job.title, career.target_roles, career.skills_summary):
            reasons.append("Role mismatch")

        # Salary (optional)
        if salary_mismatch(getattr(job, "salary_range", None), career.expected_ctc):
            reasons.append("Salary mismatch")

        if reasons:
            rejected.append(RejectedJob(job=job, reasons=reasons))
        else:
            filtered.append(job)

    return {
        "filtered_jobs": filtered,
        "rejected_jobs": rejected
    }
