# core/database.py

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Pode vir do config.py ou direto do .env
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+psycopg2://webot:secret@postgres:5432/webot_db"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# É aqui que o Alembic vai buscar o metadata
Base = declarative_base()
