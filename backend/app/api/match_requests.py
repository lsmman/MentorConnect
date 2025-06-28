from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.match import (
    MatchRequestCreate, MatchRequestResponse, MatchStatus, MatchRequestUpdate
)
from app.services.match_service import (
    create_match_request, get_incoming_requests, get_outgoing_requests,
    accept_match_request, reject_match_request, cancel_match_request
)
from app.core.jwt_utils import get_current_user
from app.schemas.user import UserInDB

router = APIRouter(prefix="/api/match-requests", tags=["match-requests"])

@router.post("/", response_model=MatchRequestResponse)
def post_match_request(
    req: MatchRequestCreate,
    db: Session = Depends(get_db),
    user: UserInDB = Depends(get_current_user)
):
    if user.role != "mentee":
        raise HTTPException(status_code=403, detail={"code":403, "message":"Forbidden", "detail":"멘티만 요청 가능"})
    return create_match_request(db, req, user)

@router.get("/incoming", response_model=list[MatchRequestResponse])
def get_incoming(
    db: Session = Depends(get_db),
    user: UserInDB = Depends(get_current_user)
):
    if user.role != "mentor":
        raise HTTPException(status_code=403, detail={"code":403, "message":"Forbidden", "detail":"멘토만 조회 가능"})
    return get_incoming_requests(db, user)

@router.get("/outgoing", response_model=list[MatchRequestResponse])
def get_outgoing(
    db: Session = Depends(get_db),
    user: UserInDB = Depends(get_current_user)
):
    if user.role != "mentee":
        raise HTTPException(status_code=403, detail={"code":403, "message":"Forbidden", "detail":"멘티만 조회 가능"})
    return get_outgoing_requests(db, user)

@router.put("/{id}/accept", response_model=MatchRequestResponse)
def accept(
    id: int,
    db: Session = Depends(get_db),
    user: UserInDB = Depends(get_current_user)
):
    if user.role != "mentor":
        raise HTTPException(status_code=403, detail={"code":403, "message":"Forbidden", "detail":"멘토만 수락 가능"})
    return accept_match_request(db, id, user)

@router.put("/{id}/reject", response_model=MatchRequestResponse)
def reject(
    id: int,
    db: Session = Depends(get_db),
    user: UserInDB = Depends(get_current_user)
):
    if user.role != "mentor":
        raise HTTPException(status_code=403, detail={"code":403, "message":"Forbidden", "detail":"멘토만 거절 가능"})
    return reject_match_request(db, id, user)

@router.delete("/{id}", response_model=MatchRequestResponse)
def cancel(
    id: int,
    db: Session = Depends(get_db),
    user: UserInDB = Depends(get_current_user)
):
    if user.role != "mentee":
        raise HTTPException(status_code=403, detail={"code":403, "message":"Forbidden", "detail":"멘티만 취소 가능"})
    return cancel_match_request(db, id, user)
