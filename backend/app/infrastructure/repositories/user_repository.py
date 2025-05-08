from app.domain.entities.user import User
from app.use_cases.auth.authenticate_user import UserRepository


class UserRepositoryImpl(UserRepository):
    """
    Implementação do repositório de usuários
    """

    async def find_by_email(self, email: str) -> User | None:
        """
        Busca um usuário pelo email
        TODO: Implementar busca no banco de dados
        """
        # Implementação temporária para testes
        if email == "admin@webot.com":
            return User(
                id="1",
                email="admin@webot.com",
                password="admin123",  # TODO: Implementar hash de senha
                roles=["admin"],
                is_active=True,
            )
        return None
