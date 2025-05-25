# \src\features\departamentos\router.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from fastapi import Body
from pydantic import BaseModel

from src.db import get_session
from .crud import get_departamento, get_departamentos, create_departamento
from src.security import get_current_user
from .model import Departamento
from src.features.users.model import User

router = APIRouter(prefix="/departamentos", tags=["departamentos"])

class DepartamentoCreate(BaseModel):
    name: str

@router.get("/", response_model=List[Departamento])
def read_departamentos(
    skip: int = 0, limit: int = 100,
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),
):
    return get_departamentos(session, skip, limit)

@router.post("/", response_model=Departamento)
def create_new_departamento(
    departamento_in: DepartamentoCreate = Body(...),
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),
):
    return create_departamento(session, departamento_in.name)

@router.get("/{dept_id}", response_model=Departamento)
def read_departamento(
    dept_id: int,
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),
):
    dept = get_departamento(session, dept_id)
    if not dept:
        raise HTTPException(status_code=404, detail="Departamento não encontrado")
    return dept
