import json
import logging
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from app.config.database import SessionLocal
from app.domain.entities.user import User
from app.domain.repositories.user_repository import IUserRepository
from app.models.user import User as UserModel

logger = logging.getLogger(__name__)


class UserRepositoryImpl(IUserRepository):
    """
    Implementação do repositório de usuários
    """

    def __init__(self):
        self.db = SessionLocal()

    def find_by_email(self, email: str) -> Optional[User]:
        """
        Busca um usuário pelo email
        """
        logger.info(f"Buscando usuário com email: {email}")

        user_model = self.db.query(UserModel).filter(UserModel.email == email).first()
        if not user_model:
            logger.info(f"Usuário não encontrado: {email}")
            return None

        user = User(
            id=str(user_model.id),
            email=user_model.email,
            password_hash=user_model.password_hash,
            roles=user_model.roles or ["user"],
            is_active=user_model.is_active,
            created_at=user_model.created_at,
            updated_at=user_model.updated_at,
        )
        logger.info(f"Dados do usuário: {json.dumps(user.to_dict(), indent=2)}")
        return user

    def find_by_id(self, user_id: str) -> Optional[User]:
        """Busca um usuário pelo ID."""
        logger.info(f"Buscando usuário com ID: {user_id}")
        user_model = (
            self.db.query(UserModel).filter(UserModel.id == UUID(user_id)).first()
        )
        if not user_model:
            return None

        return User(
            id=str(user_model.id),
            email=user_model.email,
            password_hash=user_model.password_hash,
            roles=user_model.roles or ["user"],
            is_active=user_model.is_active,
            created_at=user_model.created_at,
            updated_at=user_model.updated_at,
        )

    def create(self, user: User) -> User:
        """Cria um novo usuário."""
        logger.info(f"Criando usuário: {user.email}")
        user_model = UserModel(
            email=user.email,
            password_hash=user.password_hash,
            roles=user.roles,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
        self.db.add(user_model)
        self.db.commit()
        self.db.refresh(user_model)
        return User(
            id=str(user_model.id),
            email=user_model.email,
            password_hash=user_model.password_hash,
            roles=user_model.roles or ["user"],
            is_active=user_model.is_active,
            created_at=user_model.created_at,
            updated_at=user_model.updated_at,
        )

    def update(self, user: User) -> User:
        """Atualiza um usuário existente."""
        logger.info(f"Atualizando usuário: {user.id}")
        user_model = (
            self.db.query(UserModel).filter(UserModel.id == UUID(user.id)).first()
        )
        if not user_model:
            return None

        user_model.email = user.email
        user_model.password_hash = user.password_hash
        user_model.roles = user.roles
        user_model.is_active = user.is_active
        user_model.updated_at = datetime.utcnow()

        self.db.commit()
        self.db.refresh(user_model)
        return User(
            id=str(user_model.id),
            email=user_model.email,
            password_hash=user_model.password_hash,
            roles=user_model.roles or ["user"],
            is_active=user_model.is_active,
            created_at=user_model.created_at,
            updated_at=user_model.updated_at,
        )

    def delete(self, user_id: str) -> bool:
        """Deleta um usuário pelo ID."""
        logger.info(f"Deletando usuário: {user_id}")
        user_model = (
            self.db.query(UserModel).filter(UserModel.id == UUID(user_id)).first()
        )
        if not user_model:
            return False

        self.db.delete(user_model)
        self.db.commit()
        return True

    def list_all(self) -> List[User]:
        """Lista todos os usuários."""
        logger.info("Listando todos os usuários")
        user_models = self.db.query(UserModel).all()
        return [
            User(
                id=str(user_model.id),
                email=user_model.email,
                password_hash=user_model.password_hash,
                roles=user_model.roles or ["user"],
                is_active=user_model.is_active,
                created_at=user_model.created_at,
                updated_at=user_model.updated_at,
            )
            for user_model in user_models
        ]
