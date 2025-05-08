from typing import Annotated

from app.domain.repositories.user_repository import IUserRepository
from app.infrastructure.repositories.user_repository import UserRepositoryImpl
from fastapi import Depends


async def get_user_repository() -> IUserRepository:
    """
    Provedor de dependência para o UserRepository
    """
    return UserRepositoryImpl()


# Tipo anotado para injeção de dependência
UserRepositoryDep = Annotated[IUserRepository, Depends(get_user_repository)]
