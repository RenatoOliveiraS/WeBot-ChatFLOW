# src/features/users/router.py

from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from src.db import get_session
from src.security import get_current_user
from .crud import (
    get_user,
    get_users,
    create_user,
    list_departamentos,
    assign_departamento,
    remove_departamento,
    list_cargos,
    assign_cargo,
    remove_cargo,
)
from .model import User
from .schemas import UserRead, DepartamentoRead, CargoRead  # :contentReference[oaicite:0]{index=0}:contentReference[oaicite:1]{index=1}

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=List[UserRead])
def read_users(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),
):
    return get_users(session, skip, limit)

@router.get("/{user_uuid}", response_model=UserRead)
def read_user(
    user_uuid: UUID,
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),
):
    user = get_user(session, user_uuid)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user

@router.post("/", response_model=UserRead)
def create_new_user(
    name: str,
    email: str,
    password: str,
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),
):
    return create_user(session, name, email, password)

@router.get("/{user_uuid}/departamentos", response_model=List[DepartamentoRead])
def get_user_departamentos(
    user_uuid: UUID,
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),
):
    return list_departamentos(session, user_uuid)

@router.post("/{user_uuid}/departamentos/{dept_id}")
def add_departamento_to_user(
    user_uuid: UUID,
    dept_id: int,
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),
):
    assign_departamento(session, user_uuid, dept_id)
    return {"msg": "Departamento associado"}

@router.delete("/{user_uuid}/departamentos/{dept_id}")
def del_departamento_from_user(
    user_uuid: UUID,
    dept_id: int,
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),
):
    remove_departamento(session, user_uuid, dept_id)
    return {"msg": "Associação removida"}

@router.get("/{user_uuid}/cargos", response_model=List[CargoRead])
def get_user_cargos(
    user_uuid: UUID,
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),
):
    return list_cargos(session, user_uuid)

@router.post("/{user_uuid}/cargos/{cargo_id}")
def add_cargo_to_user(
    user_uuid: UUID,
    cargo_id: int,
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),
):
    assign_cargo(session, user_uuid, cargo_id)
    return {"msg": "Cargo associado"}

@router.delete("/{user_uuid}/cargos/{cargo_id}")
def del_cargo_from_user(
    user_uuid: UUID,
    cargo_id: int,
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),
):
    remove_cargo(session, user_uuid, cargo_id)
    return {"msg": "Associação removida"}
