from sqlalchemy.orm import Session
from app.db import models
from app.schemas.user import UserSignup
from app.db.models import UserRole, Profile
from typing import Optional

def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: UserSignup, hashed_pw: str) -> models.User:
    db_user = models.User(email=user.email, password_hash=hashed_pw, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    # Create profile
    profile = Profile(user_id=db_user.id, name=user.name)
    db.add(profile)
    db.commit()
    db.refresh(db_user)
    return db_user
