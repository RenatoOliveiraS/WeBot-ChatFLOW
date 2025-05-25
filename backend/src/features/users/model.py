from uuid import UUID, uuid4
from typing import List, Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

# quebra de import circular em tempo de TYPE_CHECKING
if TYPE_CHECKING:
    from src.features.departamentos.model import Departamento
    from src.features.cargos.model import Cargo

class UserDepartamentoLink(SQLModel, table=True):
    user_uuid: UUID = Field(foreign_key="user.uuid", primary_key=True)
    departamento_id: int = Field(foreign_key="departamento.id", primary_key=True)

class UserCargoLink(SQLModel, table=True):
    user_uuid: UUID = Field(foreign_key="user.uuid", primary_key=True)
    cargo_id: int = Field(foreign_key="cargo.id", primary_key=True)

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    uuid: UUID = Field(default_factory=uuid4, unique=True, index=True)
    name: str
    email: str = Field(unique=True, index=True)
    hashed_password: str  # mantém internamente, nunca retorna na API

    departamentos: List["Departamento"] = Relationship(
        back_populates="users",
        link_model=UserDepartamentoLink
    )
    cargos: List["Cargo"] = Relationship(
        back_populates="users",
        link_model=UserCargoLink
    )
