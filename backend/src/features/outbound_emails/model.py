from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field
from pydantic import BaseModel

# ——— Schemas de requisição ———

class SendEmailPayload(BaseModel):
    to: str
    subject: str
    body_text: Optional[str] = None
    body_html: Optional[str] = None

class ReplyEmailPayload(BaseModel):
    body_text: str
    body_html: Optional[str] = None

# ——— Modelos de persistência ———

class OutboundEmailBase(SQLModel):
    thread_id: Optional[int] = Field(default=None, foreign_key="inboundemail.id")
    in_reply_to: Optional[str] = None
    to: str
    subject: str
    body_text: Optional[str] = None
    body_html: Optional[str] = None

class OutboundEmail(OutboundEmailBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    message_id: str = Field(index=True, nullable=False)
    from_email: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class OutboundEmailCreate(OutboundEmailBase):
    pass

class OutboundEmailRead(OutboundEmail):
    pass
