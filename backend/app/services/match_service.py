from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.db import models
from app.schemas.match import (
    MatchRequestCreate, MatchRequestResponse, MatchStatus
)
from app.schemas.user import UserInDB
from app.services.xss import sanitize_text

def create_match_request(db: Session, req: MatchRequestCreate, user: UserInDB):
    # Check mentor exists
    mentor = db.query(models.User).filter(models.User.id == req.mentorId, models.User.role == "mentor").first()
    if not mentor:
        raise HTTPException(status_code=400, detail={"code":400, "message":"Bad request", "detail":"멘토 없음"})
    # Only one pending request per mentee
    exists = db.query(models.MatchRequest).filter(
        models.MatchRequest.mentee_id == user.id,
        models.MatchRequest.status == MatchStatus.pending
    ).first()
    if exists:
        raise HTTPException(status_code=400, detail={"code":400, "message":"Bad request", "detail":"이미 요청 있음"})
    # Sanitize message
    message = sanitize_text(req.message)
    match = models.MatchRequest(
        mentor_id=req.mentorId,
        mentee_id=user.id,
        message=message,
        status=MatchStatus.pending
    )
    db.add(match)
    db.commit()
    db.refresh(match)
    return MatchRequestResponse.from_orm(match)

def get_incoming_requests(db: Session, user: UserInDB):
    reqs = db.query(models.MatchRequest).filter(models.MatchRequest.mentor_id == user.id).all()
    return [MatchRequestResponse.from_orm(r) for r in reqs]

def get_outgoing_requests(db: Session, user: UserInDB):
    reqs = db.query(models.MatchRequest).filter(models.MatchRequest.mentee_id == user.id).all()
    return [MatchRequestResponse.from_orm(r) for r in reqs]

def accept_match_request(db: Session, id: int, user: UserInDB):
    req = db.query(models.MatchRequest).filter(models.MatchRequest.id == id, models.MatchRequest.mentor_id == user.id).first()
    if not req:
        raise HTTPException(status_code=404, detail={"code":404, "message":"Not found", "detail":"요청 없음"})
    req.status = MatchStatus.accepted
    db.commit()
    db.refresh(req)
    return MatchRequestResponse.from_orm(req)

def reject_match_request(db: Session, id: int, user: UserInDB):
    req = db.query(models.MatchRequest).filter(models.MatchRequest.id == id, models.MatchRequest.mentor_id == user.id).first()
    if not req:
        raise HTTPException(status_code=404, detail={"code":404, "message":"Not found", "detail":"요청 없음"})
    req.status = MatchStatus.rejected
    db.commit()
    db.refresh(req)
    return MatchRequestResponse.from_orm(req)

def cancel_match_request(db: Session, id: int, user: UserInDB):
    req = db.query(models.MatchRequest).filter(models.MatchRequest.id == id, models.MatchRequest.mentee_id == user.id).first()
    if not req:
        raise HTTPException(status_code=404, detail={"code":404, "message":"Not found", "detail":"요청 없음"})
    req.status = MatchStatus.cancelled
    db.commit()
    db.refresh(req)
    return MatchRequestResponse.from_orm(req)
