from typing import List, Optional
from fastapi import HTTPException, status
from sqlmodel import Session, select
from .model import OutboundEmail

def create_outbound_email(db: Session, outbound: OutboundEmail) -> OutboundEmail:
    db.add(outbound)
    db.commit()
    db.refresh(outbound)
    return outbound

def get_outbound_by_message_id(db: Session, message_id: str) -> Optional[OutboundEmail]:
    statement = select(OutboundEmail).where(OutboundEmail.message_id == message_id)
    return db.exec(statement).first()

def get_outbound_emails(db: Session) -> List[OutboundEmail]:
    """
    Retorna todos os e-mails enviados, do mais recente para o mais antigo.
    """
    stmt = select(OutboundEmail).order_by(OutboundEmail.created_at.desc())
    return db.exec(stmt).all()

def get_outbound_email(db: Session, email_id: int) -> OutboundEmail:
    """
    Busca um e-mail enviado pelo seu ID; dispara 404 se não existir.
    """
    email = db.get(OutboundEmail, email_id)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"E-mail enviado com id={email_id} não encontrado"
        )
    return email
