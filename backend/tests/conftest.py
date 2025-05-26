# tests/conftest.py
import pytest
from sqlmodel import SQLModel, create_engine, Session

@pytest.fixture(name="db")
def db_session():
    # banco em memória: cria do zero a cada invocação da fixture
    engine = create_engine("sqlite:///:memory:", echo=True)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
