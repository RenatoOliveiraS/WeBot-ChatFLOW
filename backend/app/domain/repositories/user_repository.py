from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.user import User


class IUserRepository(ABC):
    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]:
        """Busca um usuário pelo email."""
        pass

    @abstractmethod
    def find_by_id(self, user_id: str) -> Optional[User]:
        """Busca um usuário pelo ID."""
        pass

    @abstractmethod
    def create(self, user: User) -> User:
        """Cria um novo usuário."""
        pass

    @abstractmethod
    def update(self, user: User) -> User:
        """Atualiza um usuário existente."""
        pass

    @abstractmethod
    def delete(self, user_id: str) -> bool:
        """Deleta um usuário pelo ID."""
        pass

    @abstractmethod
    def list_all(self) -> List[User]:
        """Lista todos os usuários."""
        pass
