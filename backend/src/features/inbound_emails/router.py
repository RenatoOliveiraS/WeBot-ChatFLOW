from fastapi import APIRouter, Depends, Body, status, Request
from typing import List, Optional
from sqlmodel import Session, SQLModel, Field

from src.db import get_session
from src.security import get_current_user
from .model import InboundEmail
from .crud import get_inbound_emails, get_inbound_email
from .service import ingest_raw_email

# --- Schemas ---
class RawEmailPayload(SQLModel):
    raw: str = Field(..., description="Conteúdo bruto RFC-822/MIME do e-mail")

# --- Router ---
router = APIRouter(
    prefix="/inbound-emails",
    tags=["Inbound Emails"]
)



@router.get(
    "/",
    response_model=List[InboundEmail],
    summary="Lista e-mails recebidos",
    dependencies=[Depends(get_current_user)]
)
def list_emails(
    request: Request,
    db: Session = Depends(get_session),
):
    emails = get_inbound_emails(db)
    for email_obj in emails:
        safe_id = email_obj.message_id.strip("<>")
        novos = []
        for a in email_obj.attachments:
            novos.append({
                "filename": a["filename"],
                "content_type": a.get("content_type"),
                "size": a.get("size"),
                "inline": a.get("inline"),
                "content_id": a.get("content_id"),
                "url": f"{request.base_url}attachments/{safe_id}/{a['filename']}"
            })
        email_obj.attachments = novos
    return emails


@router.get(
    "/{email_id}",
    response_model=InboundEmail,
    summary="Detalha um e-mail recebido",
    dependencies=[Depends(get_current_user)]
)
def retrieve_email(
    request: Request,
    email_id: int,
    db: Session = Depends(get_session),
):
    email_obj = get_inbound_email(db, email_id)
    safe_id = email_obj.message_id.strip("<>")
    novos = []
    for a in email_obj.attachments:
        novos.append({
            "filename": a["filename"],
            "content_type": a.get("content_type"),
            "size": a.get("size"),
            "inline": a.get("inline"),
            "content_id": a.get("content_id"),
            "url": f"{request.base_url}attachments/{safe_id}/{a['filename']}"
        })
    email_obj.attachments = novos
    return email_obj
