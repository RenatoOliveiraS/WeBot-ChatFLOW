import uuid
from datetime import datetime

import pytest
from app.domain.entities.user import User
from app.infrastructure.models.user import Base
from app.infrastructure.repositories.postgres_user_repository import (
    PostgresUserRepository,
)
from app.use_cases.auth.authenticate_user import AuthenticateUser
from passlib.context import CryptContext
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@pytest.fixture(scope="session")
def engine():
    """Cria um engine do SQLAlchemy para os testes."""
    return create_engine("sqlite:///:memory:")


@pytest.fixture(scope="session")
def tables(engine):
    """Cria as tabelas no banco de dados."""
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture
def db_session(engine, tables):
    """Cria uma sessão do SQLAlchemy."""
    connection = engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def user_repository(db_session):
    """Cria um repositório de usuários."""
    return PostgresUserRepository(db_session)


@pytest.fixture
def authenticate_user(user_repository):
    """Cria o caso de uso de autenticação."""
    return AuthenticateUser(user_repository, "test_secret_key")


@pytest.fixture
def sample_user():
    """Cria um usuário de exemplo."""
    return User(
        id=str(uuid.uuid4()),
        email="test@example.com",
        password_hash=pwd_context.hash("test_password"),
        roles=["user"],
        is_active=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
