import logging
import os
import sys

import bcrypt

# Import the SQLAlchemy models and configuration
from app.config.database import get_database_url
from app.models.user import User
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Adicionar o diretório raiz ao PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))


def create_admin_user():
    # Carregar variáveis de ambiente
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
    load_dotenv(env_path)

    # Obter credenciais do admin do .env
    admin_email = os.getenv("ADMIN_EMAIL", "admin@webot.com")
    admin_password = os.getenv("ADMIN_PASSWORD")

    if not admin_password:
        raise ValueError("ADMIN_PASSWORD não está definida nas variáveis de ambiente")

    logger.info(f"Criando usuário admin com email: {admin_email}")

    # Criar hash da senha
    password_hash = bcrypt.hashpw(admin_password.encode("utf-8"), bcrypt.gensalt())

    # Verificar se o hash está correto
    is_valid = bcrypt.checkpw(admin_password.encode("utf-8"), password_hash)
    if not is_valid:
        raise ValueError("Erro ao gerar hash da senha")

    # Criar conexão com o banco de dados
    database_url = get_database_url()
    engine = create_engine(database_url)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Criar usuário admin
        admin_user = User(
            email=admin_email,
            password_hash=password_hash.decode("utf-8"),
            roles=["admin"],
            is_active=True,
        )

        # Verificar se o usuário já existe
        existing_user = session.query(User).filter(User.email == admin_email).first()
        if existing_user:
            logger.info(f"Usuário admin já existe com email: {admin_email}")
            return

        # Adicionar usuário ao banco de dados
        session.add(admin_user)
        session.commit()

        logger.info("Admin user created successfully")

    except Exception as e:
        logger.error(f"Erro ao criar usuário admin: {str(e)}")
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    create_admin_user()
