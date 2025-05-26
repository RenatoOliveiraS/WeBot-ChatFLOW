# tests/test_email_order_interleaved.py

from datetime import datetime
import pytest
from src.features.inbound_emails.model import InboundEmail
from src.features.email_order.crud import create_email_order, list_email_order
from src.features.email_order.model import EmailDirection

def test_interleaved_orders_multiple_threads(db):
    # 1) Cria dois InboundEmail “reais” para simular duas conversas distintas
    in_a = InboundEmail(
        message_id="a_in_1",
        from_address="user1@dominio.com",
        to_addresses=["suporte@empresa.com"],
        subject="Ajuda A",
        date=datetime.utcnow(),
        raw_headers={},
        attachments=[],
    )
    in_b = InboundEmail(
        message_id="b_in_1",
        from_address="user2@dominio.com",
        to_addresses=["suporte@empresa.com"],
        subject="Ajuda B",
        date=datetime.utcnow(),
        raw_headers={},
        attachments=[],
    )
    db.add_all([in_a, in_b])
    db.commit()
    db.refresh(in_a)
    db.refresh(in_b)

    # 2) Intercala chegadas e respostas nas duas threads
    # Thread A recebe e responde
    order_a1 = create_email_order(db, in_a.id, in_a.message_id, EmailDirection.IN)
    order_b1 = create_email_order(db, in_b.id, in_b.message_id, EmailDirection.IN)
    order_a2 = create_email_order(db, in_a.id, "a_out_1", EmailDirection.OUT)
    order_b2 = create_email_order(db, in_b.id, "b_out_1", EmailDirection.OUT)
    order_a3 = create_email_order(db, in_a.id, "a_in_2", EmailDirection.IN)
    order_b3 = create_email_order(db, in_b.id, "b_in_2", EmailDirection.IN)

    # 3) Verifica que cada thread manteve sua própria sequência
    assert order_a1.sequence == 1
    assert order_a2.sequence == 2
    assert order_a3.sequence == 3

    assert order_b1.sequence == 1
    assert order_b2.sequence == 2
    assert order_b3.sequence == 3

    # 4) Valida o list_email_order retorna na ordem correta por thread
    msgs_a = [o.message_id for o in list_email_order(db, in_a.id)]
    msgs_b = [o.message_id for o in list_email_order(db, in_b.id)]

    assert msgs_a == ["a_in_1", "a_out_1", "a_in_2"]
    assert msgs_b == ["b_in_1", "b_out_1", "b_in_2"]
