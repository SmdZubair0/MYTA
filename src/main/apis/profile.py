from fastapi import APIRouter
from dotenv import load_dotenv

from src.main.schemas.CareerState import CareerState
from src.main.schemas.UserCareerProfile import UserCareerProfile
from src.main.agents.ProfileAgent import build_profile_processing_graph
from src.main.schemas.ProfileProcessingState import ProfileProcessingState

load_dotenv()

app = APIRouter()

@app.post("/profile/process", response_model=CareerState)
async def process_profile(profile: UserCareerProfile):
    graph = build_profile_processing_graph()
    state = ProfileProcessingState(user_profile=profile)
    career_state = graph.invoke(state)

    return career_state