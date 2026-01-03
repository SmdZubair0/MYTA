from typing import List
from fastapi import APIRouter
from dotenv import load_dotenv

from src.main.schemas.CareerState import CareerState
from src.main.agents.JobSeekerAgent import build_job_search_graph
from src.main.schemas.JobSearchState import JobSearchState, ScoredJobPosting

load_dotenv()

app = APIRouter()

@app.post("/jobs/search", response_model=List[ScoredJobPosting])
async def search_jobs(career_state: CareerState):
    graph = build_job_search_graph()
    state = JobSearchState(career_state=career_state)
    result = graph.invoke(state)

    return result.recommended_jobs
