from sqlalchemy.orm import Session
from .models import User, JobRecommendation


def create_user(db: Session, user_data: dict):
    user = User(**user_data)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def save_job_recommendation(db: Session, rec_data: dict):
    rec = JobRecommendation(**rec_data)
    db.add(rec)
    db.commit()
    return rec