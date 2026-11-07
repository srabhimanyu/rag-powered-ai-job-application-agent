from pydantic import BaseModel, Field
from typing import List, Optional

class Job(BaseModel):
    id: str
    company: str = "Unknown company"
    title: str
    location: str = "Not specified"
    experience_min: Optional[int] = None
    experience_max: Optional[int] = None
    skills: List[str] = Field(default_factory=list)
    description: str = ""
    source: str = "Manual"
    url: str = ""
    posted: str = ""
