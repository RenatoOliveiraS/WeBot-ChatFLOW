import logging
import sys
from pathlib import Path

from sqlalchemy import text

# Import the SQLAlchemy models and configuration
from app.config.database import SessionLocal
from app.models.user import User

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))


def check_users():
    db = SessionLocal()
    try:
        logger.info("Consultando usuários...")

        # Consulta SQL explícita para debug
        result = db.execute(text("SELECT * FROM users"))
        rows = result.fetchall()
        logger.info(f"Encontrados {len(rows)} usuários via SQL")

        for row in rows:
            print("\nInformações do usuário (via SQL):")
            print(f"ID: {row.id}")
            print(f"Email: {row.email}")
            print(f"Created at: {row.created_at}")
            print("-" * 50)

        # Consulta via ORM para comparação
        users = db.query(User).all()
        logger.info(f"Encontrados {len(users)} usuários via ORM")

        for user in users:
            print("\nInformações do usuário (via ORM):")
            print(f"ID: {user.id}")
            print(f"Email: {user.email}")
            print(f"Created at: {user.created_at}")
            print("-" * 50)

    except Exception as e:
        logger.error(f"Erro ao consultar usuários: {e}")
        import traceback

        logger.error(traceback.format_exc())
    finally:
        db.close()


if __name__ == "__main__":
    check_users()
