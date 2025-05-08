from datetime import datetime
from typing import List

from pydantic import BaseModel, EmailStr, Field, validator


class LoginRequest(BaseModel):
    email: EmailStr = Field(..., description="Email do usuário")
    password: str = Field(
        ...,
        min_length=8,
        max_length=100,
        description="Senha do usuário (mínimo 8 caracteres, incluindo maiúscula, minúscula, número e caractere especial)",
    )

    @validator("email")
    def email_must_be_lowercase(cls, v):
        return v.lower().strip()

    @validator("password")
    def password_must_be_strong(cls, v):
        if len(v) < 8:
            raise ValueError("A senha deve ter pelo menos 8 caracteres")
        if not any(c.isupper() for c in v):
            raise ValueError("A senha deve conter pelo menos uma letra maiúscula")
        if not any(c.islower() for c in v):
            raise ValueError("A senha deve conter pelo menos uma letra minúscula")
        if not any(c.isdigit() for c in v):
            raise ValueError("A senha deve conter pelo menos um número")
        if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in v):
            raise ValueError("A senha deve conter pelo menos um caractere especial")
        return v


class LoginResponse(BaseModel):
    access_token: str = Field(..., description="Token de acesso JWT")
    refresh_token: str = Field(..., description="Token de atualização JWT")
    token_type: str = Field(default="bearer", description="Tipo do token")
    expires_in: int = Field(..., description="Tempo de expiração do token em segundos")
    email: EmailStr = Field(..., description="Email do usuário")
    roles: List[str] = Field(default_factory=list, description="Roles do usuário")
    is_active: bool = Field(..., description="Status de ativação do usuário")
    created_at: str = Field(
        ..., description="Data de criação do usuário em formato ISO"
    )
    updated_at: str = Field(
        ..., description="Data da última atualização do usuário em formato ISO"
    )

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}
