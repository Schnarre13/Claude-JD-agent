from typing import Optional, Dict, Any, List
from pydantic import BaseModel

class FitScoreState(BaseModel):
    job_title: str
    company: str
    source_site: str
    job_url: str
    job_id: str

    jd_text: str
    jd_requirements: Dict[str, Any]
    resume_json: Dict[str, Any]

    fit_score: Optional[float] = None
    compensation_estimate: Optional[str] = None
    compensation_fit: Optional[str] = None
    role_type: Optional[str] = None
    contract_penalty_applied: Optional[bool] = None
    missing_skills: Optional[List[str]] = None
    strengths: Optional[List[str]] = None
    seniority_match: Optional[str] = None
    role_alignment: Optional[str] = None
    keyword_density: Optional[float] = None
    recommendation: Optional[str] = None

    explanation: Optional[str] = None
