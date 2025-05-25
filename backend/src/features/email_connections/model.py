# src/features/email_connections/model.py

from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field


class EmailConnectionBase(SQLModel):
    name: str = Field(
        ...,
        max_length=100,
        description="Identificador amigável da conexão (ex: 'Gmail corporativo')"
    )
    smtp_server: str = Field(
        ...,
        description="Endereço do servidor SMTP"
    )
    smtp_port: int = Field(
        ...,
        description="Porta do servidor SMTP (ex: 587 para TLS, 465 para SSL)"
    )
    username: str = Field(
        ...,
        description="Usuário para autenticação SMTP"
    )
    password_encrypted: str = Field(
        ...,
        description="Senha SMTP **criptografada**"
    )
    use_tls: bool = Field(
        default=True,
        description="Usar STARTTLS"
    )
    use_ssl: bool = Field(
        default=False,
        description="Conexão SSL/TLS implícita"
    )
    default: bool = Field(
        default=False,
        description="Marca esta conexão como padrão para envios"
    )
    from_email: Optional[str] = Field(
        None,
        description="Endereço de remetente padrão (ex: 'no-reply@empresa.com')"
    )
        # NOVOS campos para IMAP
    imap_server: Optional[str] = Field(
        default=None, description="Endereço do servidor IMAP"
    )
    imap_port: Optional[int] = Field(
        default=993, description="Porta do servidor IMAP (ex: 993)"
    )
    imap_use_ssl: bool = Field(
        default=True, description="Usa SSL para IMAP"
    )
    imap_folder: str = Field(
        default="INBOX", description="Pasta IMAP a ser verificada"
    )


class EmailConnection(EmailConnectionBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)