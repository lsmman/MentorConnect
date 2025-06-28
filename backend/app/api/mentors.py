from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.services import mentor_service
from app.api.users import get_current_user
from app.schemas.user import UserOut

router = APIRouter()

@router.get("/mentors", response_model=list[UserOut])
def list_mentors(
    skill: str = Query(None),
    order_by: str = Query(None, regex="^(name|skill)?$"),
    current_user=Depends(get_current_user),
    db: Session = Depends(SessionLocal),
):
    if current_user.role.value != "mentee":
        raise HTTPException(status_code=403, detail="Only mentee can view mentors")
    mentors = mentor_service.get_mentors(db, skill, order_by)
    return mentors
