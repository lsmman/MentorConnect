from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db import models
from app.schemas.user import UserSignup, UserLogin, UserOut
from app.core import jwt_utils
from passlib.hash import bcrypt
from app.services import user_service

router = APIRouter()

@router.post("/signup", response_model=UserOut, status_code=201)
def signup(user: UserSignup, db: Session = Depends(get_db)):
    if user_service.get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email already exists")
    hashed = bcrypt.hash(user.password)
    db_user = user_service.create_user(db, user, hashed)
    return db_user

@router.post("/login")
def login(data: UserLogin, db: Session = Depends(get_db)):
    db_user = user_service.get_user_by_email(db, data.email)
    if not db_user or not bcrypt.verify(data.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = jwt_utils.create_jwt_token(db_user.id, db_user.profile.name, db_user.email, db_user.role.value)
    return {"token": token}
