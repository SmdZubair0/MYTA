from .client import db
from datetime import datetime


def save_career_state(user_id: str, career_state: dict):
    db.career_states.insert_one({
        "user_id": user_id,
        "career_state": career_state,
        "created_at": datetime.utcnow()
    })


def get_latest_career_state(user_id: str):
    return db.career_states.find_one(
        {"user_id": user_id},
        sort=[("created_at", -1)]
    )


def save_user_profile(user_id: str, profile: dict):
    db.user_profiles.insert_one({
        "user_id": user_id,
        "profile": profile,
        "created_at": datetime.utcnow()
    })


def save_job_posting(job_id: str, job: dict):
    db.job_postings.update_one(
        {"job_id": job_id},
        {"$set": job},
        upsert=True
    )