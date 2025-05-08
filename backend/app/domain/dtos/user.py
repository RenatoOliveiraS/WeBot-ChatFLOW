from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field


class CreateUserDTO(BaseModel):
    """DTO para criação de usuário."""

    email: EmailStr
    password: str = Field(..., min_length=6)
    name: str
    photo: Optional[str] = None
    roles: Optional[List[str]] = ["user"]


class UpdateUserDTO(BaseModel):
    """DTO para atualização de usuário."""

    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6)
    name: Optional[str] = None
    photo: Optional[str] = None
    roles: Optional[List[str]] = None
    is_active: Optional[bool] = None


class UserResponseDTO(BaseModel):
    """DTO para resposta de usuário."""

    id: str
    email: EmailStr
    name: str
    photo: Optional[str] = None
    roles: List[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Permite conversão de ORM models
