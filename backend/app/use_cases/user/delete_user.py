from app.core.exceptions import BusinessError
from app.domain.repositories.user_repository import IUserRepository


class DeleteUser:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    async def execute(self, user_id: str) -> None:
        # Verificar se o usuário existe
        existing_user = await self.user_repository.find_by_id(user_id)
        if not existing_user:
            raise BusinessError("Usuário não encontrado")

        # Deletar usuário
        await self.user_repository.delete(user_id)
