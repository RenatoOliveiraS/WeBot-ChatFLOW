from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship

from src.features.users.model import User
from src.features.users.model import UserCargoLink

class Cargo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    users: List[User] = Relationship(
        back_populates="cargos",
        link_model=UserCargoLink
    )
