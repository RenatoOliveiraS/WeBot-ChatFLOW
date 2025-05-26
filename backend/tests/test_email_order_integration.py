# tests/test_email_order_integration.py

import pytest
from datetime import datetime
from sqlmodel import select

from src.features.email_order.crud import (
    create_email_order,
    get_last_sequence,
    list_email_order,
)
from src.features.email_order.model import EmailDirection

from src.features.inbound_emails.model import InboundEmail
from src.features.outbound_emails.crud import (
    create_outbound_email,
    get_outbound_by_message_id,
)
from src.features.outbound_emails.model import OutboundEmail


def test_email_order_with_real_inbound(db):
    # 1) Cria um inbound “de verdade”
    inbound = InboundEmail(
        message_id="in-123",
        from_address="a@b.com",
        to_addresses=["c@d.com"],
        subject="Assunto X",
        date=datetime.utcnow(),
        raw_headers={},
        attachments=[],
    )
    db.add(inbound)
    db.commit()
    db.refresh(inbound)

    # 2) Usa inbound.id como thread_id
    order = create_email_order(
        db=db,
        thread_id=inbound.id,
        message_id=inbound.message_id,
        direction=EmailDirection.IN,
    )
    assert order.thread_id == inbound.id
    assert order.sequence == 1


def test_outbound_crud_and_thread(db):
    # 1) Cria um OutboundEmail “de verdade” com os campos obrigatórios
    outbound = OutboundEmail(
        thread_id=999,
        message_id="out-456",
        to="x@y.com",                  # campo correto (NOT NULL)
        from_email="me@mydomain.com",  # também NOT NULL
        subject="Res: X",
        body_text="Oi",
        created_at=datetime.utcnow(),
        in_reply_to=None,
        body_html=None,
    )
    created = create_outbound_email(db, outbound)
    assert created.id is not None

    # 2) Recupera pelo message_id
    fetched = get_outbound_by_message_id(db, "out-456")
    assert fetched.id == created.id

    # 3) Registra ordenação de thread
    order = create_email_order(
        db=db,
        thread_id=created.thread_id,
        message_id=created.message_id,
        direction=EmailDirection.OUT,
    )
    assert order.direction == EmailDirection.OUT
    assert order.sequence == 1