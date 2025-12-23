from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List, Literal

from src.main.schemas.CareerState import CareerState

class SalaryRange(BaseModel):
    min: float
    max: float

class JobPosting(BaseModel):
    job_id: Optional[str] = None
    title: str
    company: str
    location: str
    job_type: Optional[str] = None
    description: Optional[str] = None
    url: str
    source: str                # linkedin / company_site / other
    salary_range: SalaryRange = None
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
    discovered_jobs: List[JobPosting] = []
    normalized_jobs: List[JobPosting] = []
    search_urls: List[str] = []

    filtered_jobs: List[JobPosting] = []
    rejected_jobs: Optional[List[RejectedJob]] =[]

    scored_jobs: List[ScoredJobPosting] = []
    recommended_jobs: List[ScoredJobPosting] = []

    # metadata
    search_timestamp: Optional[datetime] = None

