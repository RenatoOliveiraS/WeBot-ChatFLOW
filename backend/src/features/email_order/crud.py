# src/features/email_order/crud.py

from fastapi import HTTPException, status
from sqlmodel import Session, select, func

from .model import EmailOrder, EmailDirection


def get_last_sequence(db: Session, thread_id: int) -> int:
    stmt = (
        select(func.max(EmailOrder.sequence))
        .where(EmailOrder.thread_id == thread_id)
    )
    result = db.exec(stmt)
    # ScalarResult.one_or_none() retorna o valor (int) ou None
    last = result.one_or_none()
    # Se quiser garantir escalar:
    # last = result.scalars().one_or_none()
    return last or 0


def create_email_order(
    db: Session,
    thread_id: int,
    message_id: str,
    direction: EmailDirection
) -> EmailOrder:
    """
    Cria um novo registro em email_order, atribuindo
    sequence = last_sequence + 1 para o thread.
    """
    last_seq = get_last_sequence(db, thread_id)
    seq = last_seq + 1
    order = EmailOrder(
        thread_id=thread_id,
        message_id=message_id,
        direction=direction,
        sequence=seq
    )
    try:
        db.add(order)
        db.commit()
        db.refresh(order)
        return order
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar ordenação de email: {e}"
        )


def list_email_order(db: Session, thread_id: int) -> list[EmailOrder]:
    """
    Retorna todos os registros de email_order para este thread_id,
    em ordem crescente de sequence.
    """
    return db.exec(
        select(EmailOrder)
        .where(EmailOrder.thread_id == thread_id)
        .order_by(EmailOrder.sequence)
    ).all()
