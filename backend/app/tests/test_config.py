from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Criar Base para testes
Base = declarative_base()

# Criar engine para testes
test_engine = create_async_engine(
    "sqlite+aiosqlite:///:memory:", echo=False, future=True
)

# Criar session maker para testes
TestSessionLocal = sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_test_db():
    """Função para obter uma sessão de teste."""
    async with TestSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
