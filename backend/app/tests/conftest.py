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
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@pytest.fixture(scope="session")
async def engine():
    """Creates an SQLAlchemy engine with in-memory database."""
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:", echo=False, future=True
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest.fixture
def async_session_maker(engine):
    """Creates a session factory."""
    return sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )


@pytest.fixture
async def db_session(async_session_maker):
    """Creates a new database session for a test."""
    async with async_session_maker() as session:
        yield session


@pytest.fixture
async def user_repository(db_session):
    """Creates a user repository instance."""
    return PostgresUserRepository(db_session)


@pytest.fixture
async def authenticate_user(user_repository):
    """Creates an authentication use case instance."""
    return AuthenticateUser(user_repository, "test_secret_key")


@pytest.fixture
def sample_user():
    """Creates a sample user for testing."""
    return User(
        id=str(uuid.uuid4()),
        email="test@example.com",
        password_hash=pwd_context.hash("test_password"),
        name="Usuário Teste",
        photo=None,
        roles=["user"],
        is_active=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
