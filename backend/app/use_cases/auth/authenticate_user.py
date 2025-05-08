import json
import logging
from datetime import datetime
from typing import Protocol

from app.core.exceptions import AuthenticationError
from app.domain.dtos.auth import LoginRequest, LoginResponse
from app.domain.entities.user import User

logger = logging.getLogger(__name__)


class UserRepository(Protocol):
    async def find_by_email(self, email: str) -> User | None: ...


class AuthenticateUser:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, login_request: LoginRequest) -> LoginResponse:
        """
        Executa o caso de uso de autenticação
        """
        logger.info(f"Iniciando autenticação para: {login_request.email}")

        user = await self.user_repository.find_by_email(login_request.email)
        logger.info(
            f"Usuário encontrado: {json.dumps(user.to_dict() if user else None, indent=2)}"
        )

        if not user:
            logger.error(f"Usuário não encontrado: {login_request.email}")
            raise AuthenticationError("Usuário não encontrado")

        if not user.is_active:
            logger.error(f"Usuário inativo: {login_request.email}")
            raise AuthenticationError("Usuário inativo")

        # TODO: Implementar verificação de senha
        if login_request.password != user.password:
            logger.error(f"Senha inválida para: {login_request.email}")
            raise AuthenticationError("Senha inválida")

        # TODO: Implementar geração de token JWT
        logger.info(f"Autenticação bem sucedida para: {login_request.email}")

        return LoginResponse(
            access_token="dummy_token",  # TODO: Implementar geração real
            refresh_token="dummy_refresh_token",  # TODO: Implementar geração real
            token_type="bearer",
            expires_in=3600,  # 1 hora
            email=user.email,
            roles=user.roles,
            is_active=user.is_active,
            created_at=user.created_at.isoformat(),
            updated_at=user.updated_at.isoformat(),
        )
