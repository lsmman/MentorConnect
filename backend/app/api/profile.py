from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.core.jwt_utils import decode_jwt_token
from app.services import user_service
from app.schemas.user import UserOut, ProfileBase, MentorProfile
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.api.users import get_current_user
from app.services import image_service

router = APIRouter()

@router.put("/profile", response_model=UserOut)
def update_profile(
    profile: ProfileBase,
    current_user=Depends(get_current_user),
    db: Session = Depends(SessionLocal),
):
    try:
        updated = user_service.update_profile(db, current_user, profile)
        return updated
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
