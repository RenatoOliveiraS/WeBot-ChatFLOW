# src/features/threads/router.py

from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlmodel import Session, select
from src.db import get_session
from src.security import get_current_user
from src.features.inbound_emails.model import InboundEmail
from src.features.outbound_emails.model import OutboundEmail

router = APIRouter(
    prefix="/threads",
    tags=["Threads"],
    dependencies=[Depends(get_current_user)]
)

@router.get(
    "/{thread_id}",
    summary="Detalha os e-mails de uma thread",
)
def get_thread(thread_id: int, db: Session = Depends(get_session)):
    """
    Retorna inbound e outbound messages de uma mesma thread, ordenados cronologicamente.
    """
    inbounds = db.exec(
        select(InboundEmail)
        .where(InboundEmail.thread_id == thread_id)
    ).all()
    
    outbounds = db.exec(
        select(OutboundEmail)
        .where(OutboundEmail.thread_id == thread_id)
    ).all()

    if not inbounds and not outbounds:
        raise HTTPException(status_code=404, detail="Thread não encontrada")
    
    # Combina os inbounds e outbounds em uma lista
    all_emails = inbounds + outbounds
    
    # Ordena todos os e-mails pela data, usando `date` para inbound e `created_at` para outbound
    all_emails_sorted = sorted(
        all_emails,
        key=lambda email: email.date if isinstance(email, InboundEmail) else email.created_at
    )
    
    return {
        "thread_id": thread_id,
        "emails": all_emails_sorted  # Retorna os e-mails ordenados pela data
    }
