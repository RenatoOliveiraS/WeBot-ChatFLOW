import logging
import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

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

    # Converter a URL para async
    if "postgresql" in database_url:
        database_url = database_url.replace(
            "postgresql+psycopg2://", "postgresql+asyncpg://"
        )
        database_url = database_url.replace("postgresql://", "postgresql+asyncpg://")

    logger.info(f"Database URL: {database_url}")
    return database_url


# Obter a URL do banco de dados
DATABASE_URL = get_database_url()

# Create engine without specifying poolclass
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Adiciona logs SQL
)

AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)
Base = declarative_base()


async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
