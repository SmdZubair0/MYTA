from fastapi import APIRouter, HTTPException

from src.main.schemas.JobSearchState import ScoredJobPosting

app = APIRouter()

# TEMP in-memory cache (v1 only)
JOB_CACHE: dict[str, ScoredJobPosting] = {}


@app.get("/jobs/{job_id}", response_model=ScoredJobPosting)
def get_job_details(job_id: str):
    job = JOB_CACHE.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return job
