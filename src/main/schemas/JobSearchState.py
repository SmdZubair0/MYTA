from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List, Literal

from src.main.schemas.CareerState import CareerState

class SalaryRange(BaseModel):
    min: float
    max: float

class JobSearchTarget(BaseModel):
    source: str          # linkedin, indeed, google_jobs
    search_url: str
    query: str

class RawJobPosting(BaseModel):
    title: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    job_type: Optional[List[str]] = None
    employment_type: Optional[List[str]] = None
    career_stage: Optional[List[str]] = None
    url: str
    source: str

class JobPosting(BaseModel):
    job_id: Optional[str] = None
    title: str
    company: str
    location: str
    job_type: Optional[str] = None
    description: Optional[str] = None
    url: str
    source: str                # linkedin / company_site / other
    salary_range: Optional[SalaryRange] = None
    career_stage: Literal["junior", "mid", "senior", "unknown"]

class RejectedJob(BaseModel):
    job: JobPosting
    reasons: List[str]

class ScoredJobPosting(BaseModel):
    job: JobPosting
    fit_score: float               # 0.0 – 1.0
    fit_level: Literal["low", "medium", "high"]
    reasons: List[str]             # why it fits
    missing_requirements: List[str]


class JobSearchState(BaseModel):
    career_state: CareerState

    # generated
    search_queries: List[str] = []
    search_targets: List[JobSearchTarget] = []

    raw_jobs: List[RawJobPosting] = []
    normalized_jobs: List[JobPosting] = []

    filtered_jobs: List[JobPosting] = []
    rejected_jobs: Optional[List[RejectedJob]] =[]

    scored_jobs: List[ScoredJobPosting] = []
    recommended_jobs: List[ScoredJobPosting] = []

    search_timestamp: Optional[datetime] = None