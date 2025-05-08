import json
import logging
import traceback

from app.core.dependencies import UserRepositoryDep
from app.core.exceptions import AuthenticationError
from app.domain.dtos.auth import LoginRequest, LoginResponse
from app.use_cases.auth import AuthenticateUser
from fastapi import APIRouter, HTTPException, status

# Configuração do logger
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

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

        authenticate_user = AuthenticateUser(user_repository)
        response = await authenticate_user.execute(login_request)

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
