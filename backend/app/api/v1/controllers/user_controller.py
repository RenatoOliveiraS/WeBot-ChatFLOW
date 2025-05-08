from typing import List

from app.core.dependencies import UserRepositoryDep, get_current_user
from app.domain.dtos.user import CreateUserDTO, UpdateUserDTO, UserResponseDTO
from app.domain.entities.user import User
from app.use_cases.user.create_user import CreateUser
from app.use_cases.user.delete_user import DeleteUser
from app.use_cases.user.list_users import ListUsers
from app.use_cases.user.update_user import UpdateUser
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserResponseDTO, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: CreateUserDTO,
    user_repository: UserRepositoryDep,
    current_user: User = Depends(get_current_user),
) -> User:
    """Cria um novo usuário"""
    if "admin" not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas administradores podem criar usuários",
        )

    create_user = CreateUser(user_repository)
    return await create_user.execute(user_data)


@router.get("", response_model=List[UserResponseDTO])
async def list_users(
    user_repository: UserRepositoryDep, current_user: User = Depends(get_current_user)
) -> List[User]:
    """Lista todos os usuários"""
    if "admin" not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas administradores podem listar usuários",
        )

    list_users = ListUsers(user_repository)
    return await list_users.execute()


@router.get("/{user_id}", response_model=UserResponseDTO)
async def get_user(
    user_id: str,
    user_repository: UserRepositoryDep,
    current_user: User = Depends(get_current_user),
) -> User:
    """Obtém um usuário pelo ID"""
    if "admin" not in current_user.roles and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado"
        )

    user = await user_repository.find_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado"
        )
    return user


@router.get("/email/{email}", response_model=UserResponseDTO)
async def get_user_by_email(
    email: str,
    user_repository: UserRepositoryDep,
    current_user: User = Depends(get_current_user),
) -> User:
    """Obtém um usuário pelo email"""
    if "admin" not in current_user.roles and current_user.email != email:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado"
        )

    user = await user_repository.find_by_email(email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado"
        )
    return user


@router.put("/{user_id}", response_model=UserResponseDTO)
async def update_user(
    user_id: str,
    user_data: UpdateUserDTO,
    user_repository: UserRepositoryDep,
    current_user: User = Depends(get_current_user),
) -> User:
    """Atualiza um usuário"""
    if "admin" not in current_user.roles and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado"
        )

    update_user = UpdateUser(user_repository)
    return await update_user.execute(user_id, user_data)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: str,
    user_repository: UserRepositoryDep,
    current_user: User = Depends(get_current_user),
) -> None:
    """Deleta um usuário"""
    if "admin" not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas administradores podem deletar usuários",
        )

    delete_user = DeleteUser(user_repository)
    await delete_user.execute(user_id)
