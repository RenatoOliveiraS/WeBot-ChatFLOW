import uuid
from datetime import datetime

import pytest
from app.domain.entities.user import User
from app.infrastructure.models.user import Base
from app.infrastructure.repositories.postgres_user_repository import (
    PostgresUserRepository,
)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


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
def sample_user():
    """Fixture que cria um usuário de exemplo."""
    return User(
        id=str(uuid.uuid4()),
        email="test@example.com",
        password_hash="hashed_password",
        name="Usuário Teste",
        photo=None,
        roles=["user"],
        is_active=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )


def test_create_user(user_repository, sample_user):
    """Testa a criação de um usuário."""
    created_user = user_repository.create(sample_user)
    assert created_user.email == sample_user.email
    assert created_user.password_hash == sample_user.password_hash
    assert created_user.roles == sample_user.roles
    assert created_user.is_active == sample_user.is_active


def test_find_by_email(user_repository, sample_user):
    """Testa a busca de usuário por email."""
    created_user = user_repository.create(sample_user)
    found_user = user_repository.find_by_email(sample_user.email)
    assert found_user is not None
    assert found_user.email == sample_user.email
    assert found_user.id == created_user.id


def test_find_by_id(user_repository, sample_user):
    """Testa a busca de usuário por ID."""
    created_user = user_repository.create(sample_user)
    found_user = user_repository.find_by_id(created_user.id)
    assert found_user is not None
    assert found_user.id == created_user.id
    assert found_user.email == sample_user.email


def test_update_user(user_repository, sample_user):
    """Testa a atualização de um usuário."""
    created_user = user_repository.create(sample_user)
    created_user.password_hash = "new_hashed_password"
    created_user.roles = ["admin"]
    updated_user = user_repository.update(created_user)
    assert updated_user.password_hash == "new_hashed_password"
    assert updated_user.roles == ["admin"]


def test_delete_user(user_repository, sample_user):
    """Testa a deleção de um usuário."""
    created_user = user_repository.create(sample_user)
    assert user_repository.delete(created_user.id) is True
    assert user_repository.find_by_email(sample_user.email) is None


def test_list_all_users(user_repository, sample_user):
    """Testa a listagem de todos os usuários."""
    user1 = user_repository.create(sample_user)
    user2 = user_repository.create(
        User(
            id=str(uuid.uuid4()),
            email="test2@example.com",
            password_hash="hashed_password2",
            name="Usuário Teste 2",
            photo=None,
            roles=["user"],
            is_active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
    )
    users = user_repository.list_all()
    assert len(users) == 2
    assert any(u.email == user1.email for u in users)
    assert any(u.email == user2.email for u in users)


def test_create_duplicate_email(user_repository, sample_user):
    """Testa a criação de usuário com email duplicado."""
    user_repository.create(sample_user)
    with pytest.raises(ValueError, match="Email já cadastrado"):
        user_repository.create(sample_user)


def test_update_nonexistent_user(user_repository, sample_user):
    """Testa a atualização de um usuário inexistente."""
    with pytest.raises(ValueError, match="Usuário não encontrado"):
        user_repository.update(sample_user)


def test_delete_nonexistent_user(user_repository):
    """Testa a deleção de um usuário inexistente."""
    assert user_repository.delete(str(uuid.uuid4())) is False


def test_user_role_management(user_repository, sample_user):
    """Testa o gerenciamento de roles do usuário."""
    created_user = user_repository.create(sample_user)

    # Testa adicionar role
    created_user.add_role("admin")
    updated_user = user_repository.update(created_user)
    assert "admin" in updated_user.roles

    # Testa remover role
    updated_user.remove_role("user")
    final_user = user_repository.update(updated_user)
    assert "user" not in final_user.roles
    assert "admin" in final_user.roles


def test_user_activation_status(user_repository, sample_user):
    """Testa a ativação e desativação do usuário."""
    created_user = user_repository.create(sample_user)

    # Testa desativação
    created_user.deactivate()
    deactivated_user = user_repository.update(created_user)
    assert not deactivated_user.is_active

    # Testa reativação
    deactivated_user.activate()
    reactivated_user = user_repository.update(deactivated_user)
    assert reactivated_user.is_active


def test_user_email_validation():
    """Testa a validação de email."""
    # Emails válidos
    assert User.validate_email("test@example.com")
    assert User.validate_email("user.name@domain.co.uk")
    assert User.validate_email("user+tag@example.com")

    # Emails inválidos
    assert not User.validate_email("invalid.email")
    assert not User.validate_email("@domain.com")
    assert not User.validate_email("user@")
    assert not User.validate_email("user@.com")


def test_user_to_dict(user_repository, sample_user):
    """Testa a conversão do usuário para dicionário."""
    created_user = user_repository.create(sample_user)
    user_dict = created_user.to_dict()

    assert user_dict["id"] == created_user.id
    assert user_dict["email"] == created_user.email
    assert user_dict["roles"] == created_user.roles
    assert user_dict["is_active"] == created_user.is_active
    assert "created_at" in user_dict
    assert "updated_at" in user_dict


def test_user_create_with_custom_roles():
    """Testa a criação de usuário com roles personalizadas."""
    user = User.create(
        email="admin@example.com",
        password_hash="hashed_password",
        roles=["admin", "manager"],
    )

    assert user.email == "admin@example.com"
    assert user.roles == ["admin", "manager"]
    assert user.is_active
    assert user.id is not None


def test_user_create_with_default_role():
    """Testa a criação de usuário com role padrão."""
    user = User.create(email="user@example.com", password_hash="hashed_password")

    assert user.email == "user@example.com"
    assert user.roles == ["user"]
    assert user.is_active
    assert user.id is not None


def test_repository_error_handling(user_repository, sample_user):
    """Testa o tratamento de erros no repositório."""
    # Testa erro ao criar usuário com email inválido
    invalid_user = User(
        id=str(uuid.uuid4()),
        email="invalid-email",
        password_hash="hashed_password",
        name="Usuário Inválido",
        photo=None,
        roles=["user"],
        is_active=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    with pytest.raises(ValueError):
        user_repository.create(invalid_user)


def test_repository_transaction_rollback(user_repository, sample_user):
    """Testa o rollback de transações no repositório."""
    # Cria um usuário
    created_user = user_repository.create(sample_user)

    # Tenta criar outro usuário com o mesmo email (deve falhar)
    duplicate_user = User(
        id=str(uuid.uuid4()),
        email=sample_user.email,
        password_hash="another_hash",
        name="Usuário Duplicado",
        photo=None,
        roles=["user"],
        is_active=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

    with pytest.raises(ValueError, match="Email já cadastrado"):
        user_repository.create(duplicate_user)

    # Verifica se o usuário original ainda existe
    found_user = user_repository.find_by_email(sample_user.email)
    assert found_user is not None
    assert found_user.id == created_user.id


def test_repository_case_insensitive_email(user_repository, sample_user):
    """Testa a busca case-insensitive por email."""
    # Cria usuário com email em maiúsculas
    upper_email = sample_user.email.upper()
    user = User(
        id=str(uuid.uuid4()),
        email=upper_email,
        password_hash=sample_user.password_hash,
        name="Usuário Upper",
        photo=None,
        roles=sample_user.roles,
        is_active=sample_user.is_active,
        created_at=sample_user.created_at,
        updated_at=sample_user.updated_at,
    )
    created_user = user_repository.create(user)

    # Busca com email em minúsculas
    found_user = user_repository.find_by_email(sample_user.email.lower())
    assert found_user is not None
    assert found_user.id == created_user.id


def test_repository_empty_roles(user_repository):
    """Testa o comportamento com roles vazias."""
    user = User(
        id=str(uuid.uuid4()),
        email="empty_roles@example.com",
        password_hash="hashed_password",
        name="Usuário Empty Roles",
        photo=None,
        roles=[],
        is_active=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

    with pytest.raises(ValueError):
        user_repository.create(user)


def test_repository_null_fields(user_repository):
    """Testa o comportamento com campos nulos."""
    user = User(
        id=str(uuid.uuid4()),
        email=None,
        password_hash="hashed_password",
        name="Usuário Null Email",
        photo=None,
        roles=["user"],
        is_active=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

    with pytest.raises(ValueError):
        user_repository.create(user)
