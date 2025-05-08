from typing import Protocol

from app.core.exceptions import AuthenticationError
from app.domain.dtos.auth import LoginRequest, LoginResponse
from app.domain.entities.user import User


class UserRepository(Protocol):
    async def find_by_email(self, email: str) -> User | None: ...


class AuthenticateUser:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, login_request: LoginRequest) -> LoginResponse:
        """
        Executa o caso de uso de autenticação
        """
        user = await self.user_repository.find_by_email(login_request.email)

        if not user:
            raise AuthenticationError("Usuário não encontrado")

        if not user.is_active:
            raise AuthenticationError("Usuário inativo")

        # TODO: Implementar verificação de senha
        # TODO: Implementar geração de token JWT

        return LoginResponse(
            access_token="dummy_token",  # TODO: Implementar geração real
            refresh_token="dummy_refresh_token",  # TODO: Implementar geração real
            token_type="bearer",
            expires_in=3600,  # 1 hora
            user_id=str(user.id),
            email=user.email,
            roles=user.roles,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
