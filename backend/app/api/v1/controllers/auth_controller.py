from app.core.dependencies import UserRepositoryDep
from app.core.exceptions import AuthenticationError
from app.domain.dtos.auth import LoginRequest, LoginResponse
from app.use_cases.auth import AuthenticateUser
from fastapi import APIRouter, HTTPException, status

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
async def login(
    login_request: LoginRequest, user_repository: UserRepositoryDep
) -> LoginResponse:
    """
    Rota para autenticação de usuários
    """
    try:
        authenticate_user = AuthenticateUser(user_repository)
        return await authenticate_user.execute(login_request)
    except AuthenticationError as auth_error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(auth_error)
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor",
        )
