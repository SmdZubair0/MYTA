import re
import uuid
from typing import List, Optional, Tuple, Literal

# ============================================================
# SCHEMAS (import these from your project in real usage)
# ============================================================

from src.main.schemas.JobSearchState import JobSearchState
from src.main.utils.textHelpers import normalize_text
from src.main.schemas.JobSearchState import JobPosting, RawJobPosting, SalaryRange

CareerStage = Literal["junior", "mid", "senior", "unknown"]
JobType = Literal["remote", "hybrid", "onsite", "unknown"]

# ============================================================
# CAREER STAGE INFERENCE
# ============================================================

def resolve_career_stage(
    title: Optional[str],
    description: Optional[str],
    career_stage_list: Optional[List[str]]
) -> CareerStage:

    def score(text: str) -> CareerStage:
        t = text.lower()
        if any(k in t for k in ["intern", "fresher", "entry", "junior", "trainee"]):
            return "junior"
        if any(k in t for k in ["senior", "lead", "principal", "staff", "manager"]):
            return "senior"
        if any(k in t for k in ["engineer", "associate", "developer", "consultant"]):
            return "mid"
        return "unknown"

    # 1. Explicit career_stage field
    if career_stage_list:
        for value in career_stage_list:
            s = score(value)
            if s != "unknown":
                return s

    # 2. Title
    if title:
        s = score(title)
        if s != "unknown":
            return s

    # 3. Description
    if description:
        s = score(description)
        if s != "unknown":
            return s

    return "unknown"



# ============================================================
# JOB TYPE INFERENCE
# ============================================================

def resolve_job_type(
    title: Optional[str],
    location: Optional[str],
    description: Optional[str],
    employment_type: Optional[List[str]],
    job_type_list: Optional[List[str]],
    url:str
) -> JobType:

    def infer(text: str) -> JobType:
        t = text.lower()
        if any(k in t for k in ["remote", "wfh", "work from home"]):
            return "remote"
        if "hybrid" in t:
            return "hybrid"
        if any(k in t for k in ["onsite", "on-site", "wfo", "from office"]):
            return "onsite"
        return "unknown"

    # 1. Employment type (strongest signal)
    if employment_type:
        for value in employment_type:
            jt = infer(value)
            if jt != "unknown":
                return jt

    # 2. Explicit job_type list
    if job_type_list:
        for value in job_type_list:
            jt = infer(value)
            if jt != "unknown":
                return jt

    # 3. Location sometimes contains job type
    if location:
        jt = infer(location)
        if jt != "unknown":
            return jt

    # 4. Title + description
    for text in [title, description]:
        if text:
            jt = infer(text)
            if jt != "unknown":
                return jt
            
    # 5. sometimes url contains job type
    if url:
        jt = infer(url)
        if jt != "unknown":
            return jt
    return "unknown"


def normalize_employment_type(text: str | None) -> str | None:
    if not text:
        return None

    t = text.lower()
    if "full" in t:
        return "full-time"
    if "part" in t:
        return "part-time"
    if "intern" in t:
        return "internship"
    if "contract" in t:
        return "contract"

    return "unknown"


# ============================================================
# SALARY EXTRACTION (BEST EFFORT)
# ============================================================

def extract_salary(text: Optional[str]) -> Optional[Tuple[float, float]]:
    if not text:
        return None

    t = text.lower()

    # Examples handled:
    # 5-10 lpa
    # 8 lpa
    # 20k - 40k
    pattern = r"(\d+(?:\.\d+)?)\s*(lpa|lakhs?|k)"
    matches = re.findall(pattern, t)

    if not matches:
        return None

    values = []
    for num, unit in matches:
        value = float(num)
        if unit.startswith("k"):
            value *= 1_000
        else:  # lpa / lakhs
            value *= 100_000
        values.append(value)

    if not values:
        return None

    return min(values), max(values)


def extract_city(location: Optional[str]) -> Optional[str]:
    if not location:
        return None

    loc = location.lower()

    if "remote" in loc:
        return "remote"

    # remove brackets
    loc = re.sub(r"\(.*?\)", "", loc)

    # split by common separators
    for sep in [",", "-", "|", "/"]:
        if sep in loc:
            loc = loc.split(sep)[0]

    return loc.strip().title() if loc.strip() else None


# ============================================================
# SINGLE JOB NORMALIZATION
# ============================================================

def normalize_job(raw: RawJobPosting) -> JobPosting:
    career_stage = resolve_career_stage(
        title=raw.title,
        description=raw.description,
        career_stage_list=raw.career_stage
    )

    job_type = resolve_job_type(
        title=raw.title,
        location=raw.location,
        description=raw.description,
        employment_type=raw.employment_type,
        job_type_list=raw.job_type,
        url=raw.url
    )

    salary_tuple = extract_salary(
        " ".join(filter(None, [
            raw.title,
            raw.description
        ]))
    )

    salary_range = None
    if salary_tuple:
        salary_range = SalaryRange(
            min=salary_tuple[0],
            max=salary_tuple[1],
            currency="INR"
        )

    return JobPosting(
        job_id=str(uuid.uuid4()),
        title=normalize_text(raw.title) or "Unknown Role",
        company=normalize_text(raw.company) or "Unknown Company",
        location=extract_city(raw.location) or "Unknown Location",
        job_type=job_type,
        career_stage=career_stage,
        description=normalize_text(raw.description),
        url=raw.url,
        source=raw.source,
        salary_range=salary_range
    )


# # ============================================================
# # LANGGRAPH NODE
# # ============================================================

def job_normalization_node(state: JobSearchState) -> dict:
    """
        Input  : state.raw_jobs -> List[RawJobPosting]
        Output : normalized_jobs        -> List[JobPosting]
    """

    normalized_jobs: List[JobPosting] = []

    for raw_job in state.raw_jobs:
        try:
            normalized_jobs.append(normalize_job(raw_job))
        except Exception as e:
            print(e)
            # Never fail the pipeline due to one bad job
            continue

    return {
        "normalized_jobs": normalized_jobs
    }


# ============================================================
# LOCAL TESTING (OPTIONAL)
# ============================================================

if __name__ == "__main__":
    from src.resources.mockData.newData import raw_jobs

    class DummyState:
        raw_jobs = raw_jobs

    print(f"JobPostings : {job_normalization_node(DummyState())}")