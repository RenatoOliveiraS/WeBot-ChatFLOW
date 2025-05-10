import uuid
from datetime import datetime

import pytest
from app.domain.entities.user import User
from app.tests.test_config import Base, TestSessionLocal, test_engine
from app.tests.test_repository import TestUserRepository
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@pytest.fixture(scope="session")
async def engine():
    """Creates an SQLAlchemy engine with in-memory database."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield test_engine
    await test_engine.dispose()


@pytest.fixture
async def db_session(engine):
    """Creates a new database session for a test."""
    async with TestSessionLocal() as session:
        yield session


@pytest.fixture
def user_repository(db_session):
    """Creates a user repository instance."""
    return TestUserRepository(db_session)


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


@pytest.mark.asyncio
async def test_database_connection(db_session):
    """Teste básico de conexão com o banco de dados."""
    from sqlalchemy import text

    result = await db_session.execute(text("SELECT 1"))
    assert result.scalar() == 1
