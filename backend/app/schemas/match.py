from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional

class MatchStatus(str, Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"
    cancelled = "cancelled"

class MatchRequestCreate(BaseModel):
    mentorId: int
    message: str

class MatchRequestUpdate(BaseModel):
    status: MatchStatus

class MatchRequestResponse(BaseModel):
    id: int
    mentorId: int = Field(..., alias="mentor_id")
    menteeId: int = Field(..., alias="mentee_id")
    message: Optional[str]
    status: MatchStatus

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
