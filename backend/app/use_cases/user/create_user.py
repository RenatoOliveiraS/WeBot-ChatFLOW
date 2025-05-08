from app.core.exceptions import BusinessError
from app.domain.dtos.user import CreateUserDTO
from app.domain.entities.user import User
from app.domain.repositories.user_repository import IUserRepository
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class CreateUser:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    async def execute(self, user_data: CreateUserDTO) -> User:
        # Verificar se o email já existe
        existing_user = await self.user_repository.find_by_email(user_data.email)
        if existing_user:
            raise BusinessError("Email já está em uso")

        # Hash da senha
        password_hash = pwd_context.hash(user_data.password)

        # Criar usuário
        user = User.create(
            email=user_data.email,
            password_hash=password_hash,
            name=user_data.name,
            photo=user_data.photo,
            roles=user_data.roles,
        )

        # Salvar no banco
        return await self.user_repository.create(user)
