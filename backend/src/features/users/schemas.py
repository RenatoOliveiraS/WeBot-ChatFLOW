# src/features/users/schemas.py

from uuid import UUID
from typing import List
from pydantic import BaseModel

class DepartamentoRead(BaseModel):
    id: int
    name: str

class CargoRead(BaseModel):
    id: int
    name: str

class UserRead(BaseModel):
    
    uuid: UUID
    name: str
    email: str
    departamentos: List[DepartamentoRead] = []
    cargos: List[CargoRead] = []
