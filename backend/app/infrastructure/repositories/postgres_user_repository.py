import logging
from datetime import datetime
from typing import List, Optional

from app.domain.entities.user import User
from app.domain.repositories.user_repository import IUserRepository
from app.infrastructure.models.user import UserModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


class PostgresUserRepository(IUserRepository):
    def __init__(self, session: Session):
        self.session = session

    def find_by_email(self, email: str) -> Optional[User]:
        try:
            logger.info(f"Buscando usuário com email: {email}")
            user_model = (
                self.session.query(UserModel)
                .filter(UserModel.email == email.lower())
                .first()
            )
            if user_model:
                return self._to_entity(user_model)
            return None
        except Exception as e:
            logger.error(f"Erro ao buscar usuário por email: {e}")
            raise

    def find_by_id(self, user_id: str) -> Optional[User]:
        try:
            logger.info(f"Buscando usuário com ID: {user_id}")
            user_model = (
                self.session.query(UserModel).filter(UserModel.id == user_id).first()
            )
            if user_model:
                return self._to_entity(user_model)
            return None
        except Exception as e:
            logger.error(f"Erro ao buscar usuário por ID: {e}")
            raise

    def create(self, user: User) -> User:
        try:
            if not user.email:
                raise ValueError("Email não pode ser nulo")

            if not user.validate_email(user.email):
                raise ValueError("Email inválido")

            if not user.roles:
                raise ValueError("Usuário deve ter pelo menos uma role")

            logger.info(f"Criando usuário com email: {user.email}")
            user_model = UserModel(
                email=user.email.lower(),
                password_hash=user.password_hash,
                roles=user.roles,
                is_active=user.is_active,
                created_at=user.created_at,
                updated_at=user.updated_at,
            )
            self.session.add(user_model)
            self.session.commit()
            self.session.refresh(user_model)
            return self._to_entity(user_model)
        except IntegrityError as e:
            logger.error(f"Erro de integridade ao criar usuário: {e}")
            self.session.rollback()
            raise ValueError("Email já cadastrado")
        except Exception as e:
            logger.error(f"Erro ao criar usuário: {e}")
            self.session.rollback()
            raise

    def update(self, user: User) -> User:
        try:
            logger.info(f"Atualizando usuário: {user.id}")
            user_model = (
                self.session.query(UserModel).filter(UserModel.id == user.id).first()
            )
            if not user_model:
                raise ValueError(f"Usuário não encontrado: {user.id}")

            user_model.email = user.email.lower()
            user_model.password_hash = user.password_hash
            user_model.roles = user.roles
            user_model.is_active = user.is_active
            user_model.updated_at = datetime.utcnow()

            self.session.commit()
            self.session.refresh(user_model)
            return self._to_entity(user_model)
        except IntegrityError as e:
            logger.error(f"Erro de integridade ao atualizar usuário: {e}")
            self.session.rollback()
            raise ValueError("Email já cadastrado")
        except Exception as e:
            logger.error(f"Erro ao atualizar usuário: {e}")
            self.session.rollback()
            raise

    def delete(self, user_id: str) -> bool:
        try:
            logger.info(f"Deletando usuário: {user_id}")
            user_model = (
                self.session.query(UserModel).filter(UserModel.id == user_id).first()
            )
            if not user_model:
                return False

            self.session.delete(user_model)
            self.session.commit()
            return True
        except Exception as e:
            logger.error(f"Erro ao deletar usuário: {e}")
            self.session.rollback()
            raise

    def list_all(self) -> List[User]:
        try:
            logger.info("Listando todos os usuários")
            user_models = self.session.query(UserModel).all()
            return [self._to_entity(model) for model in user_models]
        except Exception as e:
            logger.error(f"Erro ao listar usuários: {e}")
            raise

    def _to_entity(self, model: UserModel) -> User:
        """Converte o modelo do SQLAlchemy para a entidade de domínio."""
        return User(
            id=model.id,
            email=model.email,
            password_hash=model.password_hash,
            name=model.name,
            photo=model.photo,
            roles=model.roles,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
