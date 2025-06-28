from datetime import datetime, timedelta, timezone
from jose import jwt
from uuid import uuid4
from app.core.config import settings
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.user import UserInDB

def create_jwt_token(user_id: int, name: str, email: str, role: str) -> str:
    now = datetime.now(timezone.utc)
    exp = now + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    payload = {
        "iss": "MentorConnect",
        "sub": str(user_id),
        "aud": "MentorConnectUser",
        "exp": exp,
        "nbf": now,
        "iat": now,
        "jti": str(uuid4()),
        "name": name,
        "email": email,
        "role": role,
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

def decode_jwt_token(token: str):
    return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM], audience="MentorConnectUser")

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    db: Session = Depends(get_db),
) -> UserInDB:
    try:
        payload = decode_jwt_token(credentials.credentials)
        user = db.execute(
            "SELECT id, email, role, name FROM users WHERE id = :id",
            {"id": int(payload["sub"])}
        ).fetchone()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return UserInDB(
            id=user.id,
            email=user.email,
            role=user.role,
            profile={"name": user.name}
        )
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
