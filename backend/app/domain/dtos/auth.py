from datetime import datetime
from typing import List

from pydantic import BaseModel, EmailStr, Field, validator


class LoginRequest(BaseModel):
    email: EmailStr = Field(..., description="Email do usuário")
    password: str = Field(
        ..., min_length=6, max_length=100, description="Senha do usuário"
    )

    @validator("email")
    def email_must_be_lowercase(cls, v):
        return v.lower().strip()

    @validator("password")
    def password_must_contain_special_chars(cls, v):
        if not any(char in "!@#$%^&*()_+-=[]{}|;:,.<>?" for char in v):
            raise ValueError("A senha deve conter pelo menos um caractere especial")
        return v


class LoginResponse(BaseModel):
    access_token: str = Field(..., description="Token de acesso JWT")
    refresh_token: str = Field(..., description="Token de atualização JWT")
    token_type: str = Field(default="bearer", description="Tipo do token")
    expires_in: int = Field(..., description="Tempo de expiração do token em segundos")
    user_id: str = Field(..., description="ID do usuário")
    email: EmailStr = Field(..., description="Email do usuário")
    roles: List[str] = Field(default_factory=list, description="Roles do usuário")
    is_active: bool = Field(..., description="Status de ativação do usuário")
    created_at: datetime = Field(..., description="Data de criação do usuário")
    updated_at: datetime = Field(
        ..., description="Data da última atualização do usuário"
    )

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}
