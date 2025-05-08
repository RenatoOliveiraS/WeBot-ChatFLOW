import re
import uuid
from datetime import datetime
from typing import List, Optional


class User:
    """Entidade de usuário."""

    def __init__(
        self,
        id: str,
        email: str,
        password_hash: str,
        name: str,
        photo: str,
        roles: List[str],
        is_active: bool,
        created_at: datetime,
        updated_at: datetime,
    ):
        """Inicializa um usuário."""
        self.id = id
        self.email = email
        self.password_hash = password_hash
        self.name = name
        self.photo = photo
        self.roles = roles
        self.is_active = is_active
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def create(
        cls,
        email: str,
        password_hash: str,
        name: str,
        photo: str = None,
        roles: Optional[List[str]] = None,
    ) -> "User":
        """Cria um novo usuário."""
        if not email:
            raise ValueError("Email não pode ser nulo")

        if not cls.validate_email(email):
            raise ValueError("Email inválido")

        if not name:
            raise ValueError("Nome não pode ser nulo")

        if not roles:
            roles = ["user"]
        elif not roles:
            raise ValueError("Usuário deve ter pelo menos uma role")

        return cls(
            id=str(uuid.uuid4()),
            email=email,
            password_hash=password_hash,
            name=name,
            photo=photo,
            roles=roles,
            is_active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

    @staticmethod
    def validate_email(email: str) -> bool:
        """Valida o formato do email."""
        if not email:
            return False

        # Regex mais rigoroso para validação de email
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, email):
            return False

        # Validações adicionais
        if email.count("@") != 1:
            return False

        local_part, domain = email.split("@")
        if not local_part or not domain:
            return False

        if len(local_part) > 64 or len(domain) > 255:
            return False

        if ".." in local_part or ".." in domain:
            return False

        if domain.startswith(".") or domain.endswith("."):
            return False

        return True

    def has_role(self, role: str) -> bool:
        """Verifica se o usuário tem um determinado papel."""
        return role in self.roles

    def add_role(self, role: str) -> None:
        """Adiciona um papel ao usuário."""
        if role not in self.roles:
            self.roles.append(role)
            self.updated_at = datetime.utcnow()

    def remove_role(self, role: str) -> None:
        """Remove um papel do usuário."""
        if role in self.roles and len(self.roles) > 1:
            self.roles.remove(role)
            self.updated_at = datetime.utcnow()

    def deactivate(self) -> None:
        """Desativa o usuário."""
        self.is_active = False
        self.updated_at = datetime.utcnow()

    def activate(self) -> None:
        """Ativa o usuário."""
        self.is_active = True
        self.updated_at = datetime.utcnow()

    def to_dict(self) -> dict:
        """Converte o usuário para um dicionário."""
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "photo": self.photo,
            "roles": self.roles,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
