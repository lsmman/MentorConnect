from app.db import models
from sqlalchemy.orm import Session
from app.schemas.user import UserOut

def get_mentors(db: Session, skill: str = None, order_by: str = None):
    q = db.query(models.User).filter(models.User.role == models.UserRole.mentor)
    if skill:
        q = q.join(models.Profile).filter(models.Profile.skills.like(f"%{skill}%"))
    if order_by == "name":
        q = q.join(models.Profile).order_by(models.Profile.name.asc())
    elif order_by == "skill":
        q = q.join(models.Profile).order_by(models.Profile.skills.asc())
    else:
        q = q.order_by(models.User.id.asc())
    return q.all()
