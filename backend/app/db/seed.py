import os
from sqlalchemy.orm import Session
from app.db.database import SessionLocal, engine
from app.db import models
from app.schemas.match import MatchStatus
from passlib.hash import bcrypt

models.Base.metadata.create_all(engine)

def seed():
    db: Session = SessionLocal()
    # Users
    if not db.query(models.User).first():
        mentor = models.User(email="mentor@example.com", password_hash=bcrypt.hash("mentorpass"), role=models.UserRole.mentor)
        mentee = models.User(email="mentee@example.com", password_hash=bcrypt.hash("menteepass"), role=models.UserRole.mentee)
        db.add_all([mentor, mentee])
        db.commit()
        db.refresh(mentor)
        db.refresh(mentee)
        # Profiles
        mentor_profile = models.Profile(user_id=mentor.id, name="멘토", bio="프론트 멘토", skills="React,Vue")
        mentee_profile = models.Profile(user_id=mentee.id, name="멘티", bio="백엔드 멘티")
        db.add_all([mentor_profile, mentee_profile])
        db.commit()
        # MatchRequest
        match = models.MatchRequest(mentor_id=mentor.id, mentee_id=mentee.id, message="멘토링 요청", status=models.MatchStatus.pending)
        db.add(match)
        db.commit()
    db.close()

if __name__ == "__main__":
    seed()
