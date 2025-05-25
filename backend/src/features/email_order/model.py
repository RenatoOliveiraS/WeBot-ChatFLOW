from datetime import datetime
from enum import Enum
from typing import Optional

import sqlalchemy as sa
from sqlmodel import SQLModel, Field
from sqlalchemy import Column  # certifique-se de importar Column aqui

class EmailDirection(str, Enum):
    IN = "IN"
    OUT = "OUT"

class EmailOrder(SQLModel, table=True):
    __tablename__ = "email_order"

    id: Optional[int] = Field(default=None, primary_key=True)
    thread_id: int = Field(
        foreign_key="inboundemail.id",
        index=True,
        nullable=False,
    )
    message_id: str = Field(index=True, nullable=False)
    # ↓ aqui ajustamos para passar tudo dentro do Column
    direction: EmailDirection = Field(
        sa_column=Column(
            sa.Enum(EmailDirection, name="emaildirection"),
            nullable=False,
        )
    )
    sequence: int = Field(nullable=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
