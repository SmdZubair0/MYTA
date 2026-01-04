from src.main.schemas.JobSearchState import JobSearchState, JobsFound

def return_found_jobs(state : JobSearchState) -> JobsFound:
    return JobsFound(
        recommended_jobs=state.recommended_jobs,
        search_timestamp=state.search_timestamp
    )