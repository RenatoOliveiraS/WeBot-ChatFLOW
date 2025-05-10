import pytest

from app.models.user import User


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
