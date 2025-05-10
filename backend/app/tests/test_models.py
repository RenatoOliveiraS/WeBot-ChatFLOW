import pytest
from app.models.user import User
from app.tests.test_config import Base
from sqlalchemy import ARRAY, Boolean, Column, DateTime, String


class UserModel(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    name = Column(String, nullable=False)
    photo = Column(String, nullable=True)
    roles = Column(ARRAY(String), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


@pytest.mark.asyncio
async def test_user_model():
    # Test that the User model is properly defined
    assert User.__tablename__ == "users"
    assert hasattr(User, "id")
    assert hasattr(User, "email")
    assert hasattr(User, "password_hash")
    assert hasattr(User, "roles")
    assert hasattr(User, "is_active")
    assert hasattr(User, "created_at")
    assert hasattr(User, "updated_at")
