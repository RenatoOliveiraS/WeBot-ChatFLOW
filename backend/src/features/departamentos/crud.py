from typing import List
from sqlmodel import Session, select
from .model import Departamento

def get_departamento(session: Session, dept_id: int) -> Departamento | None:
    return session.get(Departamento, dept_id)

def get_departamentos(session: Session, skip: int = 0, limit: int = 100) -> List[Departamento]:
    stmt = select(Departamento).offset(skip).limit(limit)
    return session.exec(stmt).all()

def create_departamento(session: Session, name: str) -> Departamento:
    dept = Departamento(name=name)
    session.add(dept)
    session.commit()
    session.refresh(dept)
    return dept

def get_departamento_by_name(session: Session, name: str) -> Departamento | None:
    stmt = select(Departamento).where(Departamento.name == name)
    return session.exec(stmt).first()