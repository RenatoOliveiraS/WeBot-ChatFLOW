import uuid
from datetime import datetime

import jwt
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


@pytest.fixture
def db_session():
    """Fixture que cria uma sessão do SQLAlchemy com banco em memória."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


@pytest.fixture
def user_repository(db_session):
    """Fixture que cria um repositório de usuários."""
    return PostgresUserRepository(db_session)


@pytest.fixture
def authenticate_user(user_repository):
    """Fixture que cria o caso de uso de autenticação."""
    return AuthenticateUser(user_repository, "test_secret_key")


@pytest.fixture
def sample_user():
    """Fixture que cria um usuário de exemplo."""
    return User(
        id=str(uuid.uuid4()),
        email="test@example.com",
        password_hash=pwd_context.hash("TestPassword@123"),
        roles=["user"],
        is_active=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )


def test_authenticate_user_success(authenticate_user, user_repository, sample_user):
    """Testa a autenticação bem-sucedida de um usuário."""
    user_repository.create(sample_user)
    token = authenticate_user.execute(sample_user.email, "TestPassword@123")
    assert token is not None
    assert isinstance(token, str)
    assert len(token) > 0


def test_authenticate_user_wrong_password(
    authenticate_user, user_repository, sample_user
):
    """Testa a autenticação com senha incorreta."""
    user_repository.create(sample_user)
    with pytest.raises(ValueError, match="Senha incorreta"):
        authenticate_user.execute(sample_user.email, "WrongPassword@123")


def test_authenticate_user_not_found(authenticate_user):
    """Testa a autenticação de um usuário inexistente."""
    with pytest.raises(ValueError, match="Usuário não encontrado"):
        authenticate_user.execute("nonexistent@example.com", "TestPassword@123")


def test_authenticate_inactive_user(authenticate_user, user_repository, sample_user):
    """Testa a autenticação de um usuário inativo."""
    sample_user.is_active = False
    user_repository.create(sample_user)
    with pytest.raises(ValueError, match="Usuário inativo"):
        authenticate_user.execute(sample_user.email, "TestPassword@123")


def test_token_contains_user_info(authenticate_user, user_repository, sample_user):
    """Testa se o token contém as informações corretas do usuário."""
    user_repository.create(sample_user)
    token = authenticate_user.execute(sample_user.email, "TestPassword@123")
    assert token is not None
    assert isinstance(token, str)
    assert len(token) > 0


def test_token_expiration(authenticate_user, user_repository, sample_user):
    """Testa a expiração do token JWT."""
    user_repository.create(sample_user)
    token = authenticate_user.execute(sample_user.email, "TestPassword@123")

    # Decodifica o token para verificar a expiração
    decoded = jwt.decode(token, "test_secret_key", algorithms=["HS256"])
    assert "exp" in decoded
    assert decoded["exp"] > datetime.utcnow().timestamp()


def test_token_payload(authenticate_user, user_repository, sample_user):
    """Testa o conteúdo do payload do token JWT."""
    created_user = user_repository.create(sample_user)
    token = authenticate_user.execute(created_user.email, "TestPassword@123")

    # Decodifica o token para verificar o payload
    decoded = jwt.decode(token, "test_secret_key", algorithms=["HS256"])
    assert decoded["sub"] == created_user.id
    assert decoded["email"] == created_user.email
    assert decoded["roles"] == created_user.roles


def test_authentication_with_invalid_secret_key(
    authenticate_user, user_repository, sample_user
):
    """Testa a autenticação com chave secreta inválida."""
    # Primeiro cria o usuário
    user_repository.create(sample_user)

    # Tenta autenticar com chave inválida
    auth = AuthenticateUser(user_repository, "invalid_key")
    token = auth.execute(sample_user.email, "TestPassword@123")

    # Deve falhar ao decodificar o token
    with pytest.raises(jwt.InvalidTokenError):
        jwt.decode(token, "wrong_key", algorithms=["HS256"])


def test_authentication_with_empty_password(
    authenticate_user, user_repository, sample_user
):
    """Testa a autenticação com senha vazia."""
    user_repository.create(sample_user)
    with pytest.raises(ValueError):
        authenticate_user.execute(sample_user.email, "")


def test_authentication_with_empty_email(authenticate_user):
    """Testa a autenticação com email vazio."""
    with pytest.raises(ValueError):
        authenticate_user.execute("", "TestPassword@123")


def test_authentication_with_special_characters(authenticate_user, user_repository):
    """Testa a autenticação com caracteres especiais no email."""
    special_user = User(
        id=str(uuid.uuid4()),
        email="user+test@example.com",
        password_hash=pwd_context.hash("TestPassword@123"),
        roles=["user"],
        is_active=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    user_repository.create(special_user)

    token = authenticate_user.execute(special_user.email, "TestPassword@123")
    assert token is not None
    assert isinstance(token, str)
