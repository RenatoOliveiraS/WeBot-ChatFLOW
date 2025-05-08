import logging
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import QueuePool

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Carregar variáveis de ambiente
env_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), ".env"
)
load_dotenv(dotenv_path=env_path)


def get_database_url():
    # Obter a URL do banco de dados do arquivo .env
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL não está definida no arquivo .env")

    # Ajustar a URL para usar o nome do serviço postgres quando executado no Docker
    if "@localhost:" in database_url:
        database_url = database_url.replace("@localhost:", "@postgres:")

    logger.info(f"Database URL: {database_url}")
    return database_url


# Obter a URL do banco de dados
DATABASE_URL = get_database_url()

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,
    echo=True,  # Adiciona logs SQL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
