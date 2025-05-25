# src/features/inbound_emails/service.py
import imaplib
import email
from email.message import Message
from pathlib import Path
from uuid import uuid4
import hashlib
from sqlmodel import Session, select
from datetime import datetime

from src.config import settings
from .crud import create_inbound_email
from .model import InboundEmail

from src.features.email_order.crud import create_email_order
from src.features.email_order.model import EmailDirection

# Diretório de anexos
ATTACHMENTS_DIR = Path(
    getattr(settings, "INBOUND_EMAIL_ATTACHMENTS_DIR", "./attachments/inbound_emails")
)
ATTACHMENTS_DIR.mkdir(parents=True, exist_ok=True)


def create_inbound_email(db: Session, email_data: dict) -> InboundEmail:
    # Converte pydantic ou dict em dict puro
    if isinstance(email_data, InboundEmail):
        email_dict = email_data.dict(exclude_unset=True)
    else:
        email_dict = email_data

    inbound = InboundEmail(**email_dict, created_at=datetime.utcnow())

    # 1) Agrupa por Gmail thread ID
    if inbound.gm_thread_id:
        existing = db.exec(
            select(InboundEmail).where(InboundEmail.gm_thread_id == inbound.gm_thread_id)
        ).first()
        if existing:
            inbound.thread_id = existing.thread_id or existing.id

    # 2) Agrupa por In-Reply-To
    if inbound.thread_id is None and inbound.in_reply_to:
        existing = db.exec(
            select(InboundEmail).where(InboundEmail.message_id == inbound.in_reply_to)
        ).first()
        if existing:
            inbound.thread_id = existing.thread_id or existing.id

    # 3) Agrupa por References (primeiro Message-ID da lista)
    if inbound.thread_id is None and inbound.references:
        first_ref = inbound.references.split()[0]
        existing = db.exec(
            select(InboundEmail).where(InboundEmail.message_id == first_ref)
        ).first()
        if existing:
            inbound.thread_id = existing.thread_id or existing.id

    # 4) Agrupa por Thread-Index do Outlook
    if inbound.thread_id is None and inbound.thread_index:
        existing = db.exec(
            select(InboundEmail).where(InboundEmail.thread_index == inbound.thread_index)
        ).first()
        if existing:
            inbound.thread_id = existing.thread_id or existing.id

    # 5) Persiste o inbound para gerar inbound.id (e opcionalmente thread_id, se veio de agrupamento)
    db.add(inbound)
    db.commit()
    db.refresh(inbound)

    # 6) Se não havia thread_id (nova thread), atualiza para id gerado
    if inbound.thread_id is None:
        inbound.thread_id = inbound.id
        db.add(inbound)
        db.commit()
        db.refresh(inbound)

    # 7) Registra a ordem de chegada no thread
    create_email_order(
        db=db,
        thread_id=inbound.thread_id,
        message_id=inbound.message_id,
        direction=EmailDirection.IN
    )

    return inbound


def ingest_raw_email(db: Session, raw: str) -> InboundEmail:
    msg: Message = email.message_from_string(raw)
    message_id = msg.get("Message-ID") or f"<{uuid4().hex}>"
    raw_mid = message_id.strip("<>")
    safe_id = hashlib.sha256(raw_mid.encode("utf-8")).hexdigest()[:16]
    mail_dir = ATTACHMENTS_DIR / safe_id
    mail_dir.mkdir(parents=True, exist_ok=True)

    attachments, body_text, body_html = [], None, None

    for part in msg.walk():
        if part.is_multipart():
            continue
        content_type = part.get_content_type()
        disposition = part.get_content_disposition()

        if disposition in ("attachment", "inline") or content_type.startswith("image/"):
            filename = part.get_filename() or f"image_{len(attachments)+1}.{content_type.split('/')[-1]}"
            payload = part.get_payload(decode=True) or b""
            path = mail_dir / filename
            with open(path, "wb") as f:
                f.write(payload)
            attachments.append({
                "filename": filename,
                "content_type": content_type,
                "size": len(payload),
                "inline": (disposition == "inline") or content_type.startswith("image/"),
                "content_id": part.get("Content-ID"),
            })
        elif content_type == "text/plain" and body_text is None:
            charset = part.get_content_charset() or "utf-8"
            body_text = part.get_payload(decode=True).decode(charset, errors="replace")
        elif content_type == "text/html" and body_html is None:
            charset = part.get_content_charset() or "utf-8"
            body_html = part.get_payload(decode=True).decode(charset, errors="replace")

    # Extrai cabeçalhos de threading
    in_reply_to = msg.get("In-Reply-To")
    references = msg.get("References")
    thread_index = msg.get("Thread-Index")
    gm_thread_id = msg.get("X-GM-THRID") or msg.get("X-Gm-Thrid")

    inbound_email = InboundEmail(
        message_id=message_id,
        from_address=msg.get("From", ""),
        to_addresses=msg.get_all("To", []),
        subject=msg.get("Subject"),
        date=email.utils.parsedate_to_datetime(msg.get("Date")) if msg.get("Date") else None,
        body_text=body_text,
        body_html=body_html,
        raw_headers=dict(msg.items()),
        attachments=attachments,
        in_reply_to=in_reply_to,
        references=references,
        thread_index=thread_index,
        gm_thread_id=gm_thread_id,
    )
    return create_inbound_email(db, inbound_email)
