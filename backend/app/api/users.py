from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.core.jwt_utils import decode_jwt_token
from app.services import user_service
from app.schemas.user import UserOut
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter()
security = HTTPBearer()

def get_current_user(token: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    try:
        payload = decode_jwt_token(token.credentials)
        user = user_service.get_user_by_email(db, payload["email"])
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.get("/me", response_model=UserOut)
def get_me(current_user=Depends(get_current_user)):
    profile = current_user.profile
    profile_dict = None
    if profile:
        profile_dict = {
            "name": profile.name,
            "bio": profile.bio,
            "imageUrl": f"/api/images/{current_user.role.value}/{current_user.id}"
        }
        if current_user.role.value == "mentor":
            profile_dict["skills"] = profile.skills.split(",") if profile.skills else []
    return {
        "id": current_user.id,
        "email": current_user.email,
        "role": current_user.role,
        "profile": profile_dict
    }
