# src/features/inbound_emails/model.py

from typing import Optional, List, Dict
from datetime import datetime
from sqlmodel import SQLModel, Field, Column
from sqlalchemy import JSON

class InboundEmail(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    message_id: str                                # unique, index
    from_address: str
    to_addresses: List[str] = Field(sa_column=Column(JSON))
    subject: Optional[str] = None
    date: datetime
    body_text: Optional[str] = None
    body_html: Optional[str] = None
    raw_headers: Dict[str, str] = Field(sa_column=Column(JSON))
    attachments: List[dict]  = Field(sa_column=Column(JSON))

    # ——— RFC-5322 / Proprietary threading headers ———
    in_reply_to: Optional[str] = Field(default=None)
    references: Optional[str] = Field(default=None)
    thread_index: Optional[str] = Field(default=None)  # Outlook
    gm_thread_id: Optional[str] = Field(default=None)  # Gmail (X-GM-THRID)

    # thread grouping id
    thread_id: Optional[int] = Field(default=None, foreign_key="inboundemail.id")
    created_at: datetime     = Field(default_factory=datetime.utcnow)
