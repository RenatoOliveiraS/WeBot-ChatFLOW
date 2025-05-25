# src/features/cargos/router.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from fastapi import Body
from pydantic import BaseModel

from src.db import get_session
from src.features.cargos.crud import get_cargo, get_cargos, create_cargo
from src.security import get_current_user
from src.features.cargos.model import Cargo
from src.features.users.model import User



router = APIRouter(prefix="/cargos", tags=["cargos"])

class CargoCreate(BaseModel):
    name: str

@router.get("/", response_model=List[Cargo])
def read_cargos(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session),
    _: Cargo = Depends(get_current_user),
):
    return get_cargos(session, skip, limit)

@router.post("/", response_model=Cargo)
def create_new_cargo(
    cargo_in: CargoCreate = Body(...),
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),
):
    return create_cargo(session, cargo_in.name)

@router.get("/{cargo_id}", response_model=Cargo)
def read_cargo(
    cargo_id: int,
    session: Session = Depends(get_session),
    _: Cargo = Depends(get_current_user),
):
    cargo = get_cargo(session, cargo_id)
    if not cargo:
        raise HTTPException(status_code=404, detail="Cargo não encontrado")
    return cargo
