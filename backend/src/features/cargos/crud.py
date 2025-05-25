from typing import List
from sqlmodel import Session, select
from .model import Cargo

def get_cargo(session: Session, cargo_id: int) -> Cargo | None:
    return session.get(Cargo, cargo_id)

def get_cargos(session: Session, skip: int = 0, limit: int = 100) -> List[Cargo]:
    stmt = select(Cargo).offset(skip).limit(limit)
    return session.exec(stmt).all()

def create_cargo(session: Session, name: str) -> Cargo:
    cargo = Cargo(name=name)
    session.add(cargo)
    session.commit()
    session.refresh(cargo)
    return cargo

def get_cargo_by_name(session: Session, name: str) -> Cargo | None:
    stmt = select(Cargo).where(Cargo.name == name)
    return session.exec(stmt).first()