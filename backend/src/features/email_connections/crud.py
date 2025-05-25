# src/features/email_connections/crud.py

from datetime import datetime
from typing import List

from fastapi import HTTPException, status
from sqlmodel import Session, select

from .model import EmailConnection, EmailConnectionBase


def get_email_connections(db: Session) -> List[EmailConnection]:
    return db.exec(select(EmailConnection)).all()


def get_email_connection(db: Session, connection_id: int) -> EmailConnection:
    connection = db.get(EmailConnection, connection_id)
    if not connection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Conexão de e-mail com id={connection_id} não encontrada"
        )
    return connection


def create_email_connection(
    db: Session,
    connection_data: EmailConnectionBase
) -> EmailConnection:
    # AQUI: assume-se que `connection_data.password_encrypted` já vem criptografado
    connection = EmailConnection.from_orm(connection_data)
    db.add(connection)
    db.commit()
    db.refresh(connection)
    return connection


def update_email_connection(
    db: Session,
    connection_id: int,
    connection_data: EmailConnectionBase
) -> EmailConnection:
    connection = get_email_connection(db, connection_id)
    # Atualiza somente campos enviados (exclude_unset)
    for key, value in connection_data.dict(exclude_unset=True).items():
        setattr(connection, key, value)
    connection.updated_at = datetime.utcnow()
    db.add(connection)
    db.commit()
    db.refresh(connection)
    return connection


def delete_email_connection(db: Session, connection_id: int) -> None:
    connection = get_email_connection(db, connection_id)
    db.delete(connection)
    db.commit()
