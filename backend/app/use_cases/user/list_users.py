from typing import List

from app.domain.entities.user import User
from app.domain.repositories.user_repository import IUserRepository


class ListUsers:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    async def execute(self) -> List[User]:
        return await self.user_repository.list_all()
