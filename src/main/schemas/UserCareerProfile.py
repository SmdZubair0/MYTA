from typing import List, Optional
from pydantic import BaseModel, HttpUrl, Field

class BasicInfo(BaseModel):
    name: str = ""
    current_location: str = ""

class CareerPreferences(BaseModel):
    target_role: str = ""
    career_goal_summary: str = ""
    job_type_preference: List[str] = Field(default_factory=list)
    preferred_locations: List[str] = Field(default_factory=list)
    current_ctc: Optional[float] = None
    expected_ctc: Optional[float] = None

class Education(BaseModel):
    institution_name: str = ""
    degree: str = ""
    field_of_study: str = ""
    graduation_year: int
    score_or_percentage: Optional[float] = None

class Experience(BaseModel):
    company_name: str = ""
    designation: str = ""
    role_type: str = ""
    start_date: str
    end_date: str = ""
    responsibilities_summary: str = ""
    tech_stack_used: List[str] = Field(default_factory=list)

class Skills(BaseModel):
    technical: List[str] = Field(default_factory=list)
    tools: List[str] = Field(default_factory=list)
    frameworks: List[str] = Field(default_factory=list)
    domains: List[str] = Field(default_factory=list)
    soft_skills: List[str] = Field(default_factory=list)

class OnlinePresence(BaseModel):
    linkedin_url: str = ""
    github_url: str = ""
    portfolio_url: str = ""
    blog_url: str = ""

class ResumeMetadata(BaseModel):
    file_name: Optional[str] = None
    uploaded_at: Optional[str] = None

class Constraints(BaseModel):
    notice_period: str = ""
    open_to_relocation: str = ""
    preferred_company_type: str = ""

class Project(BaseModel):
    title: str = ""
    description: str = ""
    role: str = ""
    tech_stack: List[str] = Field(default_factory=list)
    github_url: Optional[HttpUrl] = None
    live_url: Optional[HttpUrl] = None
    duration: str = ""

class UserCareerProfile(BaseModel):
    basic_profile: BasicInfo
    career_preferences: CareerPreferences
    education: List[Education] = Field(default_factory=list)
    experience: List[Experience] = Field(default_factory=list)
    skills: Skills
    online_presence: Optional[OnlinePresence] = None
    projects: List[Project] = Field(default_factory=list)
    resume: Optional[ResumeMetadata] = None
    constraints: Optional[Constraints] = None