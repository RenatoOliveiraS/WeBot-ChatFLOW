from typing import List
from uuid import UUID
from sqlalchemy.orm import selectinload
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError

from .model import User, UserDepartamentoLink, UserCargoLink
from src.features.departamentos.model import Departamento
from src.features.cargos.model import Cargo
from src.utils import get_password_hash

def get_users(session: Session, skip: int = 0, limit: int = 100) -> List[User]:
    stmt = (
        select(User)
        .options(
            selectinload(User.departamentos),
            selectinload(User.cargos),
        )
        .offset(skip)
        .limit(limit)
    )
    return session.exec(stmt).all()

def get_user(session: Session, user_uuid: UUID) -> User | None:
    stmt = (
        select(User)
        .where(User.uuid == user_uuid)
        .options(
            selectinload(User.departamentos),
            selectinload(User.cargos),
        )
    )
    return session.exec(stmt).first()

def get_user_by_email(session: Session, email: str) -> User | None:
    stmt = select(User).where(User.email == email)
    return session.exec(stmt).first()

def create_user(session: Session, name: str, email: str, password: str) -> User:
    user = User(
        name=name,
        email=email,
        hashed_password=get_password_hash(password)
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def list_departamentos(session: Session, user_uuid: UUID) -> List[Departamento]:
    stmt = (
        select(Departamento)
        .join(UserDepartamentoLink)
        .where(UserDepartamentoLink.user_uuid == user_uuid)
    )
    return session.exec(stmt).all()

def assign_departamento(session: Session, user_uuid: UUID, departamento_id: int) -> None:
    # evita inserir duplicata
    existing = session.exec(
        select(UserDepartamentoLink)
        .where(UserDepartamentoLink.user_uuid == user_uuid)
        .where(UserDepartamentoLink.departamento_id == departamento_id)
    ).first()
    if not existing:
        link = UserDepartamentoLink(user_uuid=user_uuid, departamento_id=departamento_id)
        session.add(link)
        try:
            session.commit()
        except IntegrityError:
            session.rollback()

def remove_departamento(session: Session, user_uuid: UUID, dept_id: int) -> None:
    stmt = (
        select(UserDepartamentoLink)
        .where(
            UserDepartamentoLink.user_uuid == user_uuid,
            UserDepartamentoLink.departamento_id == dept_id
        )
    )
    link = session.exec(stmt).first()
    if link:
        session.delete(link)
        session.commit()

def list_cargos(session: Session, user_uuid: UUID) -> List[Cargo]:
    stmt = (
        select(Cargo)
        .join(UserCargoLink)
        .where(UserCargoLink.user_uuid == user_uuid)
    )
    return session.exec(stmt).all()

def assign_cargo(session: Session, user_uuid: UUID, cargo_id: int) -> None:
    # evita duplicar vínculo user–cargo
    existing = session.exec(
        select(UserCargoLink)
        .where(UserCargoLink.user_uuid == user_uuid)
        .where(UserCargoLink.cargo_id == cargo_id)
    ).first()
    if not existing:
        link = UserCargoLink(user_uuid=user_uuid, cargo_id=cargo_id)
        session.add(link)
        try:
            session.commit()
        except IntegrityError:
            session.rollback()

def remove_cargo(session: Session, user_uuid: UUID, cargo_id: int) -> None:
    stmt = (
        select(UserCargoLink)
        .where(
            UserCargoLink.user_uuid == user_uuid,
            UserCargoLink.cargo_id == cargo_id
        )
    )
    link = session.exec(stmt).first()
    if link:
        session.delete(link)
        session.commit()
