from app.domain.entities.user import User
from app.tests.test_models import UserModel
from sqlalchemy.ext.asyncio import AsyncSession


class TestUserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user: User) -> User:
        user_model = UserModel(
            id=user.id,
            email=user.email.lower(),
            password_hash=user.password_hash,
            name=user.name,
            photo=user.photo,
            roles=user.roles,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
        self.session.add(user_model)
        await self.session.commit()
        return user
