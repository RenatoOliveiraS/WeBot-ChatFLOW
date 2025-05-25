# src/features/inbound_emails/crud.py

from typing import List
from fastapi import HTTPException, status
from sqlmodel import Session, select

from .model import InboundEmail


def create_inbound_email(db: Session, email: InboundEmail) -> InboundEmail:
    try:
        db.add(email)
        db.commit()
        db.refresh(email)
        return email
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao salvar e-mail: {e}"
        )


def get_inbound_emails(db: Session) -> List[InboundEmail]:
    return db.exec(select(InboundEmail).order_by(InboundEmail.date.desc())).all()


def get_inbound_email(db: Session, email_id: int) -> InboundEmail:
    email = db.get(InboundEmail, email_id)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"E-mail com id={email_id} não encontrado"
        )
    return email


from typing import Optional
from sqlmodel import Session, select
from .model import InboundEmail


def get_inbound_by_message_id(db: Session, message_id: str) -> Optional[InboundEmail]:
    statement = select(InboundEmail).where(InboundEmail.message_id == message_id)
    return db.exec(statement).first()