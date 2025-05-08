import re
from dataclasses import dataclass
from datetime import datetime
from typing import List
from uuid import UUID


@dataclass
class User:
    id: UUID
    email: str
    password_hash: str
    roles: List[str]
    created_at: datetime
    updated_at: datetime
    is_active: bool = True

    def __init__(
        self,
        id: str,
        email: str,
        password: str,
        roles: List[str],
        is_active: bool = True,
        created_at: datetime = None,
        updated_at: datetime = None,
    ):
        self.id = id
        self.email = email
        self.password = password
        self.roles = roles
        self.is_active = is_active
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    @classmethod
    def create(cls, email: str, password_hash: str, roles: List[str] = None) -> "User":
        """
        Factory method para criar um novo usuário
        """
        from uuid import uuid4

        now = datetime.utcnow()
        return cls(
            id=uuid4(),
            email=email.lower().strip(),
            password_hash=password_hash,
            roles=roles or ["user"],
            created_at=now,
            updated_at=now,
            is_active=True,
        )

    def validate_email(self) -> bool:
        """
        Valida o formato do email
        """
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(email_pattern, self.email))

    def has_role(self, role: str) -> bool:
        """
        Verifica se o usuário possui uma determinada role
        """
        return role in self.roles

    def add_role(self, role: str) -> None:
        """
        Adiciona uma nova role ao usuário
        """
        if role not in self.roles:
            self.roles.append(role)
            self.updated_at = datetime.utcnow()

    def remove_role(self, role: str) -> None:
        """
        Remove uma role do usuário
        """
        if role in self.roles:
            self.roles.remove(role)
            self.updated_at = datetime.utcnow()

    def deactivate(self) -> None:
        """
        Desativa o usuário
        """
        self.is_active = False
        self.updated_at = datetime.utcnow()

    def activate(self) -> None:
        """
        Reativa o usuário
        """
        self.is_active = True
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        return {
            "email": self.email,
            "roles": self.roles,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
