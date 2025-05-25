# src/config.py

from pathlib import Path
from dotenv import load_dotenv
import os
import warnings

# carrega .env da raiz do projeto
env_path = Path(__file__).resolve().parents[2] / ".env"
if not env_path.exists():
    raise FileNotFoundError(f".env não encontrado em {env_path}")
load_dotenv(dotenv_path=env_path)

# database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./dev.db")

# segurança
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("🔒 SECRET_KEY não definida no .env")
if SECRET_KEY == "troque_essa_chave_pra_producao":
    raise RuntimeError("🔒 SECRET_KEY padrão não é seguro para produção!")

ALGORITHM = os.getenv("ALGORITHM", "HS256")

# expiração de token
try:
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
except ValueError:
    raise ValueError("⏱️ ACCESS_TOKEN_EXPIRE_MINUTES deve ser um inteiro")

# variáveis de seed do usuário admin
ADMIN_NAME = os.getenv("ADMIN_NAME")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
if not (ADMIN_NAME and ADMIN_EMAIL and ADMIN_PASSWORD):
    warnings.warn(
        "⚠️ Variáveis de seed do admin não definidas: "
        "ADMIN_NAME, ADMIN_EMAIL e ADMIN_PASSWORD são necessárias para o seed automático."
    )


class Settings:
    DATABASE_URL = DATABASE_URL
    SECRET_KEY = SECRET_KEY
    ALGORITHM = ALGORITHM
    ACCESS_TOKEN_EXPIRE_MINUTES = ACCESS_TOKEN_EXPIRE_MINUTES

    # variáveis de seed do admin
    ADMIN_NAME = ADMIN_NAME
    ADMIN_EMAIL = ADMIN_EMAIL
    ADMIN_PASSWORD = ADMIN_PASSWORD
    
    INBOUND_EMAIL_ATTACHMENTS_DIR: str = "./attachments/inbound_emails"
# objeto que o main.py espera importar
settings = Settings()
