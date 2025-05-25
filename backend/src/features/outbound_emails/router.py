# src/features/outbound_emails/router.py
from fastapi import APIRouter, Depends, Body, status, HTTPException
from sqlmodel import Session
from src.db import get_session
from typing import List

from .model import (
    OutboundEmailRead,
    OutboundEmailCreate,
    ReplyEmailPayload
)
from .service import send_email as send_email_service
from src.features.inbound_emails.crud import get_inbound_email

from .crud import get_outbound_emails, get_outbound_email

router = APIRouter(prefix="/outbound-emails", tags=["Outbound Emails"])

@router.post(
    "/send",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=OutboundEmailRead
)
def send_generic(
    payload: OutboundEmailCreate = Body(...),
    db: Session = Depends(get_session),
):
    try:
        outbound = send_email_service(
            db=db,
            to=payload.to,
            subject=payload.subject,
            body_text=payload.body_text,
            body_html=payload.body_html,
            in_reply_to=payload.in_reply_to
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return outbound

@router.post(
    "/{inbound_email_id}/reply",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=OutboundEmailRead
)
def reply_to_inbound(
    inbound_email_id: int,
    payload: ReplyEmailPayload = Body(...),
    db: Session = Depends(get_session),
):
    inbound = get_inbound_email(db, inbound_email_id)
    try:
        outbound = send_email_service(
            db=db,
            to=inbound.from_address,
            subject=f"Re: {inbound.subject or ''}",
            body_text=payload.body_text,
            body_html=payload.body_html,
            in_reply_to=inbound.message_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return outbound


@router.get(
    "/",
    response_model=List[OutboundEmailRead],
    summary="Lista todos os e-mails enviados",
)
def list_outbound_emails(db: Session = Depends(get_session)):
    return get_outbound_emails(db)

@router.get(
    "/{email_id}",
    response_model=OutboundEmailRead,
    summary="Detalha um e-mail enviado",
)
def retrieve_outbound_email(
    email_id: int,
    db: Session = Depends(get_session),
):
    return get_outbound_email(db, email_id)