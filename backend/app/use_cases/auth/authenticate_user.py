import logging
from datetime import datetime, timedelta

import jwt
from app.domain.dtos.auth import LoginRequest
from app.domain.repositories.user_repository import IUserRepository
from passlib.context import CryptContext

logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthenticateUser:
    """Caso de uso para autenticar um usuário."""

    def __init__(self, user_repository: IUserRepository, secret_key: str):
        """Inicializa o caso de uso."""
        self.user_repository = user_repository
        self.secret_key = secret_key

    def execute(self, email: str, password: str) -> str:
        """Executa o caso de uso."""
        logger.info(f"Tentando autenticar usuário: {email}")

        # Valida os dados de entrada
        login_request = LoginRequest(email=email, password=password)

        # Busca o usuário
        user = self.user_repository.find_by_email(login_request.email)
        if not user:
            logger.warning(f"Usuário não encontrado: {email}")
            raise ValueError("Usuário não encontrado")

        # Verifica se o usuário está ativo
        if not user.is_active:
            logger.warning(f"Usuário inativo: {email}")
            raise ValueError("Usuário inativo")

        # Log para depuração
        logger.info(f"Hash da senha armazenado: {user.password_hash}")
        logger.info(f"Senha fornecida: {password}")

        # Verifica a senha
        is_valid = pwd_context.verify(login_request.password, user.password_hash)
        logger.info(f"Resultado da verificação da senha: {is_valid}")

        if not is_valid:
            logger.warning(f"Senha incorreta para o usuário: {email}")
            raise ValueError("Senha incorreta")

        # Gera o token
        token = self._create_token(user)
        logger.info(f"Usuário autenticado com sucesso: {email}")
        return token

    def _create_token(self, user) -> str:
        """Cria um token JWT."""
        expires_delta = timedelta(minutes=30)
        expire = datetime.utcnow() + expires_delta

        data = {
            "sub": user.id,
            "email": user.email,
            "roles": user.roles,
            "exp": expire.timestamp(),
        }

        encoded_jwt = jwt.encode(data, self.secret_key, algorithm="HS256")
        return encoded_jwt
