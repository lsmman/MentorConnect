from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.core.jwt_utils import get_current_user
from app.db import models
from app.schemas.user import UserInDB
from PIL import Image
import io

router = APIRouter(prefix="/api/images", tags=["images"])

ALLOWED_TYPES = ["image/jpeg", "image/png"]
MIN_SIZE = 500
MAX_SIZE = 1000
MAX_BYTES = 1024 * 1024  # 1MB

@router.post("/{role}/{id}")
def upload_profile_image(
    role: str,
    id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: UserInDB = Depends(get_current_user)
):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail={"code":400, "message":"Bad request", "detail":"지원하지 않는 이미지 형식"})
    content = file.file.read()
    if len(content) > MAX_BYTES:
        raise HTTPException(status_code=400, detail={"code":400, "message":"Bad request", "detail":"이미지 용량 초과"})
    try:
        img = Image.open(io.BytesIO(content))
        w, h = img.size
        if w != h or w < MIN_SIZE or w > MAX_SIZE:
            raise HTTPException(status_code=400, detail={"code":400, "message":"Bad request", "detail":"정사각형 500~1000px만 허용"})
        # DB에 저장
        profile = db.query(models.Profile).filter(models.Profile.user_id == id).first()
        if not profile:
            raise HTTPException(status_code=404, detail={"code":404, "message":"Not found", "detail":"프로필 없음"})
        profile.image = content
        db.commit()
        return {"result": "ok"}
    except Exception:
        raise HTTPException(status_code=400, detail={"code":400, "message":"Bad request", "detail":"이미지 처리 실패"})

@router.get("/{role}/{id}")
def get_profile_image(
    role: str,
    id: int,
    db: Session = Depends(get_db),
    user: UserInDB = Depends(get_current_user)
):
    profile = db.query(models.Profile).filter(models.Profile.user_id == id).first()
    if not profile or not profile.image:
        # 플레이스홀더
        url = "https://placehold.co/500x500.jpg?text=MENTOR" if role == "mentor" else "https://placehold.co/500x500.jpg?text=MENTEE"
        import requests
        r = requests.get(url)
        return StreamingResponse(io.BytesIO(r.content), media_type="image/jpeg")
    img = profile.image
    return StreamingResponse(io.BytesIO(img), media_type="image/jpeg")
