import json
import logging
import os
import traceback

from app.core.dependencies import UserRepositoryDep
from app.core.exceptions import AuthenticationError
from app.domain.dtos.auth import LoginRequest, LoginResponse
from app.use_cases.auth.authenticate_user import AuthenticateUser
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, status

# Configuração do logger
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Carregar variáveis de ambiente
env_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), ".env"
)
load_dotenv(dotenv_path=env_path)

# Obter a chave secreta do JWT
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not JWT_SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY não está definida no arquivo .env")

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
async def login(
    login_request: LoginRequest, user_repository: UserRepositoryDep
) -> LoginResponse:
    """
    Rota para autenticação de usuários
    """
    try:
        logger.info(f"Tentativa de login para o email: {login_request.email}")
        logger.info(
            f"Dados da requisição: {json.dumps(login_request.dict(), indent=2)}"
        )

        authenticate_user = AuthenticateUser(user_repository, JWT_SECRET_KEY)
        token = authenticate_user.execute(login_request.email, login_request.password)

        # Buscar o usuário para obter os dados necessários
        user = user_repository.find_by_email(login_request.email)

        response = LoginResponse(
            access_token=token,
            refresh_token=token,  # Por enquanto, usando o mesmo token
            token_type="bearer",
            expires_in=3600,  # 1 hora
            email=user.email,
            roles=user.roles,
            is_active=user.is_active,
            created_at=user.created_at.isoformat(),
            updated_at=user.updated_at.isoformat(),
            name=user.name,
            photo=user.photo,
        )

        logger.info(f"Login bem sucedido para o email: {login_request.email}")
        logger.info(f"Resposta: {json.dumps(response.dict(), indent=2)}")

        return response
    except AuthenticationError as auth_error:
        logger.error(f"Erro de autenticação: {str(auth_error)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(auth_error)
        )
    except Exception as e:
        logger.error(f"Erro interno: {str(e)}")
        logger.error(f"Stack trace: {traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno do servidor: {str(e)}",
        )
