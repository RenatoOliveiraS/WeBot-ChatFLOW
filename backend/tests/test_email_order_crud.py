# tests/test_email_order_crud.py
import pytest
from sqlmodel import select
from src.features.email_order.crud import (
    get_last_sequence,
    create_email_order,
    list_email_order,
)
from src.features.email_order.model import EmailDirection

def test_get_last_sequence_empty(db):
    # sem nenhum registro, deve retornar 0
    assert get_last_sequence(db, thread_id=42) == 0

def test_create_email_order_increments_sequence(db):
    # primeira mensagem num thread novo → seq == 1
    order1 = create_email_order(
        db=db,
        thread_id=1,
        message_id="msg-1",
        direction=EmailDirection.IN,
    )
    assert order1.sequence == 1

    # segunda mensagem no mesmo thread → seq == 2
    order2 = create_email_order(
        db=db,
        thread_id=1,
        message_id="msg-2",
        direction=EmailDirection.OUT,
    )
    assert order2.sequence == 2

    # verify get_last_sequence reflete o último
    assert get_last_sequence(db, thread_id=1) == 2

def test_sequences_independent_between_threads(db):
    # thread 1
    o1 = create_email_order(db, thread_id=1, message_id="t1-msg1", direction=EmailDirection.IN)
    assert o1.sequence == 1
    # thread 2
    o2 = create_email_order(db, thread_id=2, message_id="t2-msg1", direction=EmailDirection.IN)
    assert o2.sequence == 1

def test_list_email_order_returns_ordered(db):
    # insere fora de ordem propositalmente
    create_email_order(db, thread_id=5, message_id="a", direction=EmailDirection.IN)
    create_email_order(db, thread_id=5, message_id="b", direction=EmailDirection.OUT)
    create_email_order(db, thread_id=5, message_id="c", direction=EmailDirection.IN)

    orders = list_email_order(db, thread_id=5)
    ids = [o.message_id for o in orders]
    assert ids == ["a", "b", "c"]

def test_create_email_order_raises_on_db_error(monkeypatch, db):
    # força falha no commit para testar rollback/HTTPException
    def fake_commit():
        raise Exception("fail commit")
    monkeypatch.setattr(db, "commit", fake_commit)

    with pytest.raises(Exception) as excinfo:
        create_email_order(
            db=db,
            thread_id=9,
            message_id="err-msg",
            direction=EmailDirection.OUT,
        )
    assert "Erro ao criar ordenação de email" in str(excinfo.value)
