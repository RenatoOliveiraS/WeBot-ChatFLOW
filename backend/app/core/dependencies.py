from typing import Annotated

from app.infrastructure.repositories.user_repository import UserRepositoryImpl
from app.use_cases.auth.authenticate_user import UserRepository
from fastapi import Depends


async def get_user_repository() -> UserRepository:
    """
    Provedor de dependência para o UserRepository
    """
    return UserRepositoryImpl()


# Tipo anotado para injeção de dependência
UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]
