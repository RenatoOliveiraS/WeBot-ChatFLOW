# src/features/outbound_emails/service.py

import smtplib
from email.message import EmailMessage
from email.utils import make_msgid
from datetime import datetime
from sqlmodel import Session

from src.features.email_connections.service import decrypt_password
from src.features.email_connections.crud import get_email_connections
from src.features.outbound_emails.model import OutboundEmail
from src.features.outbound_emails.crud import create_outbound_email, get_outbound_by_message_id
from src.features.inbound_emails.crud import get_inbound_by_message_id

from src.features.email_order.crud import create_email_order
from src.features.email_order.model import EmailDirection

def get_default_connection(db: Session):
    conns = get_email_connections(db)
    default = next((c for c in conns if c.default), None)
    if not default:
        raise RuntimeError("Nenhuma conexão SMTP padrão")
    return default


def send_email(
    db: Session,
    to: str,
    subject: str,
    body_text: str | None = None,
    body_html: str | None = None,
    in_reply_to: str | None = None
) -> OutboundEmail:
    # 1) conexão SMTP
    conn = get_default_connection(db)
    pwd = decrypt_password(conn.password_encrypted)

    # 2) montagem do EmailMessage
    msg = EmailMessage()
    msg["From"] = conn.from_email
    msg["To"] = to
    msg["Subject"] = subject

    # Garante Message-ID
    if not msg.get("Message-ID"):
        domain = conn.from_email.split("@")[-1]
        msg_id = make_msgid(domain=domain)
        msg["Message-ID"] = msg_id
    else:
        msg_id = msg["Message-ID"]

    # Cabeçalhos de reply
    if in_reply_to:
        msg["In-Reply-To"] = in_reply_to
        # Monta References encadeando o anterior
        parent = get_inbound_by_message_id(db, in_reply_to) or get_outbound_by_message_id(db, in_reply_to)
        parent_refs = None
        if hasattr(parent, "raw_headers"):
            parent_refs = parent.raw_headers.get("References")
        if parent_refs:
            msg["References"] = f"{parent_refs} {in_reply_to}"
        else:
            msg["References"] = in_reply_to

    # Conteúdo
    if body_html:
        msg.set_content(body_text or "")
        msg.add_alternative(body_html, subtype="html")
    else:
        msg.set_content(body_text or "")

    # 3) envio via SMTP
    if conn.use_ssl:
        smtp = smtplib.SMTP_SSL(conn.smtp_server, conn.smtp_port)
    else:
        smtp = smtplib.SMTP(conn.smtp_server, conn.smtp_port)
        if conn.use_tls:
            smtp.starttls()
    smtp.login(conn.username, pwd)
    smtp.send_message(msg)
    smtp.quit()

    # 4) determina thread_id
    thread_id = None
    if in_reply_to:
        parent_inbound = get_inbound_by_message_id(db, in_reply_to)
        if parent_inbound:
            thread_id = parent_inbound.thread_id or parent_inbound.id
        else:
            outbound_parent = get_outbound_by_message_id(db, in_reply_to)
            if outbound_parent:
                thread_id = outbound_parent.thread_id

    # 5) persiste registro
    outbound = OutboundEmail(
        thread_id=thread_id,
        in_reply_to=in_reply_to,
        message_id=msg_id,
        from_email=conn.from_email,
        to=to,
        subject=subject,
        body_text=body_text,
        body_html=body_html,
        created_at=datetime.utcnow()
    )
    # 6) salva no banco e captura objeto com ID
    saved = create_outbound_email(db, outbound)

    # 7) registra ordem de envio no thread
    create_email_order(
        db=db,
        thread_id=saved.thread_id,
        message_id=saved.message_id,
        direction=EmailDirection.OUT
    )

    return saved