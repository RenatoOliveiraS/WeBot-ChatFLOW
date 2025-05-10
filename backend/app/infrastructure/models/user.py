import json
import uuid

from sqlalchemy import Boolean, Column, DateTime, String, func
from sqlalchemy.types import TEXT, TypeDecorator

from app.config.database import Base


class JSONList(TypeDecorator):
    """Representa uma lista como uma coluna JSON."""

    impl = TEXT

    def process_bind_param(self, value, dialect):
        if value is not None:
            return json.dumps(value)
        return "[]"

    def process_result_value(self, value, dialect):
        if value is not None:
            return json.loads(value)
        return []


class UserModel(Base):
    """Modelo de usuário para o SQLAlchemy."""

    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    name = Column(String, nullable=False)
    photo = Column(String, nullable=True)
    roles = Column(JSONList, nullable=False, default=["user"])
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(
        DateTime, nullable=False, default=func.now(), onupdate=func.now()
    )

    def __repr__(self):
        return f"<User {self.email}>"
