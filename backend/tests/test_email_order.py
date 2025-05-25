
# tests/test_email_order.py

import pytest
from sqlmodel import SQLModel, create_engine, Session

# registra também a tabela de inbound para satisfazer a FK
from src.features.inbound_emails.model import InboundEmail
from src.features.email_order.model import EmailOrder, EmailDirection
from src.features.email_order.crud import create_email_order, list_email_order

@pytest.fixture(name="session")
def session_fixture(tmp_path):
    # Cria um SQLite em arquivo temporário e gera as tabelas
    db_file = tmp_path / "test.db"
    engine = create_engine(f"sqlite:///{db_file}", echo=False)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

def test_sequence_increments_within_thread(session):
    # No thread 1: IN -> 1, OUT -> 2, IN -> 3
    order1 = create_email_order(session, thread_id=1, message_id="msg-in-1", direction=EmailDirection.IN)
    assert order1.sequence == 1

    order2 = create_email_order(session, thread_id=1, message_id="msg-out-1", direction=EmailDirection.OUT)
    assert order2.sequence == 2

    order3 = create_email_order(session, thread_id=1, message_id="msg-in-2", direction=EmailDirection.IN)
    assert order3.sequence == 3

def test_sequences_are_independent_between_threads(session):
    # Thread 2 deve começar em 1 novamente
    o1 = create_email_order(session, thread_id=2, message_id="t2-1", direction=EmailDirection.IN)
    o2 = create_email_order(session, thread_id=2, message_id="t2-2", direction=EmailDirection.OUT)
    assert [o1.sequence, o2.sequence] == [1, 2]

    # Thread 1 não teve registros antes, deve começar em 1
    o4 = create_email_order(session, thread_id=1, message_id="msg-in-3", direction=EmailDirection.IN)
    assert o4.sequence == 1

def test_list_email_order(session):
    # Popula thread 3
    create_email_order(session, thread_id=3, message_id="a", direction=EmailDirection.IN)
    create_email_order(session, thread_id=3, message_id="b", direction=EmailDirection.OUT)
    create_email_order(session, thread_id=3, message_id="c", direction=EmailDirection.IN)

    orders = list_email_order(session, thread_id=3)
    sequences = [o.sequence for o in orders]
    message_ids = [o.message_id for o in orders]

    assert sequences == [1, 2, 3]
    assert message_ids == ["a", "b", "c"]
