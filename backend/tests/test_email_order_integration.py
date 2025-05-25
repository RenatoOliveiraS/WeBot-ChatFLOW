# tests/test_email_order_integration.py

import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session
from src.main import get_app, create_db_and_tables
from src.db import engine, get_session
from src.features.email_connections.model import EmailConnection
from src.features.email_connections.crud import create_email_connection
from src.features.inbound_emails.service import ingest_raw_email
from datetime import datetime

@pytest.fixture(name="app")
def fixture_app():
    # Cria a instância do app e recria o banco em memória
    app = get_app()
    # Garante que todas as tabelas sejam criadas (inclui EmailConnection)
    create_db_and_tables()
    yield app

@pytest.fixture(name="client")
def fixture_client(app):
    return TestClient(app)

@pytest.fixture(name="session")
def fixture_session():
    # usa engine configurado para tests (sqlite:///:memory:)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
        session.rollback()

@pytest.fixture(autouse=True)
def override_get_session(session):
    # Override da dependência get_session para usar a sessão de teste
    def _get_session():
        with Session(engine) as s:
            yield s
    app = get_app()
    app.dependency_overrides[get_session] = _get_session

def test_full_flow(client, session):
    """
    Fluxo de integração:
      1) Provisiona EmailConnection dummy (ID=1)
      2) Ingesta um raw email via ingest_raw_email -> cria EmailOrder IN seq=1
      3) Responde com outbound -> cria EmailOrder OUT seq=2
      4) GET /threads/{thread_id}/order -> retorna [{"direction":"IN","sequence":1},{"direction":"OUT","sequence":2}]
    """
    # 1) Provisiona conexão dummy
    conn = EmailConnection(
        name="dummy",
        smtp_server="smtp.test",
        smtp_port=587,
        username="user",
        password_encrypted="ZmFrZV9wYXNzd29yZA==",  # base64 fake
        use_tls=True,
        use_ssl=False,
        default=True,
        from_email="no-reply@test",
        imap_server="imap.test",
        imap_port=993,
        imap_use_ssl=True,
        imap_folder="INBOX"
    )
    # cria no DB
    create_email_connection(session, conn)

    # 2) Ingesta raw email (thread_id vira `id` do primeiro inbound)
    raw = "\r\n".join([
        "Message-ID: <1@test>",
        "From: alice@test",
        "To: bob@test",
        "Subject: Teste",
        "",
        "Corpo do email."
    ])
    inbound = ingest_raw_email(session, raw)
    thread_id = inbound.thread_id or inbound.id

    # 3) Envia um outbound genérico (reply)
    payload = {
        "to": ["alice@test"],
        "subject": "Re: Teste",
        "body_text": "Resposta",
        "body_html": None,
        "in_reply_to": inbound.message_id
    }
    resp_out = client.post("/outbound-emails/send", json=payload)
    assert resp_out.status_code == 202, resp_out.text

    # 4) Recupera ordenação da thread
    resp_order = client.get(f"/threads/{thread_id}/order")
    assert resp_order.status_code == 200, resp_order.text

    data = resp_order.json()
    assert data == [
        {"direction": "IN", "sequence": 1},
        {"direction": "OUT", "sequence": 2},
    ]
