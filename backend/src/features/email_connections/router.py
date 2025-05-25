# src/features/email_connections/router.py

import smtplib
import socket
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, Field, SQLModel
import imaplib

from src.db import get_session
from src.security import get_current_user

from .model import EmailConnection
from .crud import (
    get_email_connections,
    get_email_connection,
    create_email_connection,
    update_email_connection,
    delete_email_connection
)
from .service import (
    test_email_connection,
    encrypt_password,
    fetch_inbound_emails
)


class EmailConnectionCreate(SQLModel):
    name: str = Field(..., max_length=100)
    smtp_server: str
    smtp_port: int
    username: str
    password: str
    use_tls: bool = True
    use_ssl: bool = False
    default: bool = False
    from_email: Optional[str] = None
    # novos campos IMAP
    imap_server: Optional[str] = None
    imap_port: Optional[int] = 993
    imap_use_ssl: bool = True
    imap_folder: str = "INBOX"


class EmailConnectionUpdate(SQLModel):
    name: Optional[str] = None
    smtp_server: Optional[str] = None
    smtp_port: Optional[int] = None
    username: Optional[str] = None
    password: Optional[str] = None
    use_tls: Optional[bool] = None
    use_ssl: Optional[bool] = None
    default: Optional[bool] = None
    from_email: Optional[str] = None
    # IMAP
    imap_server: Optional[str] = None
    imap_port: Optional[int] = None
    imap_use_ssl: Optional[bool] = None
    imap_folder: Optional[str] = None


router = APIRouter(
    prefix="/email-connections",
    tags=["Email Connections"],
    dependencies=[Depends(get_current_user)]
)


@router.get("/", response_model=List[EmailConnection])
def list_email_connections(db: Session = Depends(get_session)):
    return get_email_connections(db)


@router.get("/{connection_id}", response_model=EmailConnection)
def retrieve_email_connection(
    connection_id: int,
    db: Session = Depends(get_session)
):
    return get_email_connection(db, connection_id)


@router.post(
    "/",
    response_model=EmailConnection,
    status_code=status.HTTP_201_CREATED
)
def create_connection(
    data: EmailConnectionCreate,
    db: Session = Depends(get_session)
):
    encrypted = encrypt_password(data.password)
    obj = EmailConnection(
        name=data.name,
        smtp_server=data.smtp_server,
        smtp_port=data.smtp_port,
        username=data.username,
        password_encrypted=encrypted,
        use_tls=data.use_tls,
        use_ssl=data.use_ssl,
        default=data.default,
        from_email=data.from_email,
        imap_server=data.imap_server,
        imap_port=data.imap_port,
        imap_use_ssl=data.imap_use_ssl,
        imap_folder=data.imap_folder,
    )
    return create_email_connection(db, obj)


@router.put("/{connection_id}", response_model=EmailConnection)
def update_connection(
    connection_id: int,
    data: EmailConnectionUpdate,
    db: Session = Depends(get_session)
):
    update_data = data.dict(exclude_unset=True)
    if "password" in update_data:
        update_data["password_encrypted"] = encrypt_password(update_data.pop("password"))
    return update_email_connection(db, connection_id, EmailConnection(**update_data))


@router.delete("/{connection_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_connection(
    connection_id: int,
    db: Session = Depends(get_session)
):
    delete_email_connection(db, connection_id)


@router.post(
    "/{connection_id}/test",
    status_code=status.HTTP_200_OK
)
def test_connection(
    connection_id: int,
    db: Session = Depends(get_session)
):
    conn = get_email_connection(db, connection_id)
    try:
        test_email_connection(conn)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except (smtplib.SMTPException, socket.timeout) as e:
        raise HTTPException(status_code=400, detail=f"Falha ao conectar: {e}")
    return {"detail": "Conexão SMTP bem-sucedida"}


@router.post(
    "/{connection_id}/fetch",
    status_code=status.HTTP_200_OK,
    summary="Busca e armazena e-mails via IMAP (manual)"
)
def fetch_emails(
    connection_id: int,
    db: Session = Depends(get_session)
):
    conn = get_email_connection(db, connection_id)
    try:
        total = fetch_inbound_emails(conn, db)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except imaplib.IMAP4.error as e:
        raise HTTPException(status_code=400, detail=f"Erro IMAP: {e}")
    return {"detail": f"{total} e-mails processados"}
