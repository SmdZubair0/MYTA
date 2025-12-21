from datetime import date
from typing import List, Optional
from pydantic import BaseModel, HttpUrl

class BasicInfo(BaseModel):
    name:str
    current_locator:str

class CareerPreferences(BaseModel):
    target_role: str
    career_goal_summary: Optional[str] = None
    job_type_preference: List[str]
    preferred_locations: Optional[List[str]] = None
    current_ctc: Optional[float] = None
    expected_ctc: Optional[float] = None

class Education(BaseModel):
    institution_name: str
    degree: str
    field_of_study: str
    graduation_year: int
    score_or_percentage: Optional[float] = None

class Experience(BaseModel):
    company_name: str
    designation: str
    role_type: Optional[str] = None
    start_date: str
    end_date: Optional[str] = None
    responsibilities_summary: Optional[str] = None
    tech_stack_used: Optional[List[str]] = None

class Skills(BaseModel):
    technical: List[str] = []
    tools: List[str] = []
    frameworks: List[str] = []
    domains: List[str] = []
    soft_skills: List[str] = []

class OnlinePresence(BaseModel):
    linkedin_url: str = None
    github_url: str = None
    portfolio_url: Optional[str] = None
    blog_url: Optional[str] = None

class ResumeMetadata(BaseModel):
    file_name: Optional[str] = None
    uploaded_at: Optional[str] = None

class Constraints(BaseModel):
    notice_period: str
    open_to_realocation: str
    preferred_company_type: str

class Project(BaseModel):
    title: str
    description: str
    role: Optional[str] = None
    tech_stack: List[str]
    github_url: Optional[HttpUrl] = None
    live_url: Optional[HttpUrl] = None
    duration: Optional[str] = None

class UserCareerProfile(BaseModel):
    basic_profile: BasicInfo
    career_preferences: CareerPreferences
    education: List[Education]
    experience: List[Experience]
    skills: Skills
    online_presence: Optional[OnlinePresence] = None
    projects: Optional[List[Project]] = []
    resume: Optional[ResumeMetadata] = None
    constraints: Optional[Constraints] = None