from pydantic import BaseModel, EmailStr, constr
from typing import Optional, List
from enum import Enum

class UserRole(str, Enum):
    mentor = "mentor"
    mentee = "mentee"

class UserSignup(BaseModel):
    email: EmailStr
    password: constr(min_length=6)
    name: str
    role: UserRole

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class ProfileBase(BaseModel):
    name: str
    bio: Optional[str] = None
    image: Optional[str] = None  # base64 encoded

class MentorProfile(ProfileBase):
    skills: List[str]

class MenteeProfile(ProfileBase):
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: UserRole
    profile: Optional[dict]

    class Config:
        orm_mode = True

class UserInDB(BaseModel):
    id: int
    email: EmailStr
    role: UserRole
    profile: Optional[dict]

    class Config:
        orm_mode = True
