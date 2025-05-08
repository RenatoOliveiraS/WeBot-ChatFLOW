import json
import logging
from datetime import datetime

from app.domain.entities.user import User
from app.use_cases.auth.authenticate_user import UserRepository

logger = logging.getLogger(__name__)


class UserRepositoryImpl(UserRepository):
    """
    Implementação do repositório de usuários
    """

    async def find_by_email(self, email: str) -> User | None:
        """
        Busca um usuário pelo email
        TODO: Implementar busca no banco de dados
        """
        logger.info(f"Buscando usuário com email: {email}")

        # Implementação temporária para testes
        if email == "admin@webot.com":
            logger.info("Usuário admin encontrado")
            now = datetime.utcnow()
            user = User(
                id="1",
                email="admin@webot.com",
                password="Admin@123",  # Senha forte: maiúscula, minúscula, número e caractere especial
                roles=["admin"],
                is_active=True,
                created_at=now,
                updated_at=now,
            )
            logger.info(f"Dados do usuário: {json.dumps(user.to_dict(), indent=2)}")
            return user

        logger.info(f"Usuário não encontrado: {email}")
        return None
