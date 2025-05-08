from app.core.exceptions import BusinessError
from app.domain.dtos.user import UpdateUserDTO
from app.domain.entities.user import User
from app.domain.repositories.user_repository import IUserRepository


class UpdateUser:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    async def execute(self, user_id: str, user_data: UpdateUserDTO) -> User:
        # Verificar se o usuário existe
        existing_user = await self.user_repository.find_by_id(user_id)
        if not existing_user:
            raise BusinessError("Usuário não encontrado")

        # Se estiver atualizando o email, verificar se já existe
        if user_data.email and user_data.email != existing_user.email:
            user_with_email = await self.user_repository.find_by_email(user_data.email)
            if user_with_email:
                raise BusinessError("Email já está em uso")

        # Atualizar campos
        if user_data.email:
            existing_user.email = user_data.email
        if user_data.name:
            existing_user.name = user_data.name
        if user_data.photo is not None:
            existing_user.photo = user_data.photo
        if user_data.roles:
            existing_user.roles = user_data.roles
        if user_data.is_active is not None:
            existing_user.is_active = user_data.is_active

        # Salvar no banco
        return await self.user_repository.update(existing_user)
