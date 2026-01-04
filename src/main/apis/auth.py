from fastapi import APIRouter, HTTPException
from uuid import uuid4

from src.main.db.sql import SessionLocal, User
from src.main.utils.auth import hash_password, verify_password, create_token

router = APIRouter(prefix="/auth")

@router.post("/signup")
def signup(email: str, password: str, name: str):
    db = SessionLocal()

    if db.query(User).filter_by(email=email).first():
        raise HTTPException(400, "User already exists")

    user = User(
        id=str(uuid4()),
        email=email,
        password_hash=hash_password(password),
        status="ACCOUNT_CREATED"
    )
    db.add(user)
    db.commit()

    return {"success": True}

@router.post("/login")
def login(email: str, password: str):
    db = SessionLocal()
    user = db.query(User).filter_by(email=email).first()

    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(401, "Invalid credentials")

    return {
        "access_token": create_token(user.id),
        "user_id": user.id,
        "status": user.status
    }
