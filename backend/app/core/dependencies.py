import os
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db
from app.domain.entities.user import User
from app.domain.repositories.user_repository import IUserRepository
from app.infrastructure.repositories.postgres_user_repository import (
    PostgresUserRepository,
)

# Carregar variáveis de ambiente
load_dotenv()

# Obter a chave secreta do JWT
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not JWT_SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY não está definida no arquivo .env")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")


async def get_user_repository(db: AsyncSession = Depends(get_db)) -> IUserRepository:
    return PostgresUserRepository(db)


UserRepositoryDep = Annotated[IUserRepository, Depends(get_user_repository)]


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], user_repository: UserRepositoryDep
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decodificar o token
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
        email: str = payload.get("email")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Buscar o usuário
    user = await user_repository.find_by_email(email)
    if user is None:
        raise credentials_exception

    # Verificar se o usuário está ativo
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Usuário inativo"
        )

    return user
