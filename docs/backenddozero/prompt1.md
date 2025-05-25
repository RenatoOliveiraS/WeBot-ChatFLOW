Segue um exemplo “do zero” de um backend mínimo, funcional e seguro em FastAPI + SQLModel, com:

* Tabelas: `User`, `Departamento`, `Cargo` e tabelas de associação many-to-many (`user_departamentos`, `user_cargos`).
* CRUD completo para `users`, `departamentos`, `cargos`.
* Endpoint de autenticação (`/auth/login`) que gera JWT.

Você só precisa criar cada arquivo e, na pasta de “features”, adicionar novas pastas com `model.py`, `crud.py` e `router.py`; o `main.py` carrega tudo automaticamente.

---

## Estrutura de pastas

```
src/
├ config.py
├ db.py
├ security.py
├ main.py
└ features/
   ├ users/
   │  ├ model.py
   │  ├ crud.py
   │  └ router.py
   ├ departamentos/
   │  ├ model.py
   │  ├ crud.py
   │  └ router.py
   ├ cargos/
   │  ├ model.py
   │  ├ crud.py
   │  └ router.py
   └ auth/
      └ router.py
```

---

## 1. Configuração e banco

### src/config.py

```python
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./dev.db")
SECRET_KEY: str = os.getenv("SECRET_KEY", "troque_essa_chave_pra_producao")
ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
```

### src/db.py

```python
from sqlmodel import SQLModel, create_engine, Session
from config import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
```

---

## 2. Segurança e JWT

### src/security.py

```python
from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID
import jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session

from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from db import get_session
from features.users.crud import get_user_by_email
from features.users.model import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def authenticate_user(session: Session, email: str, password: str) -> Optional[User]:
    user = get_user_by_email(session, email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não autenticado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    user = session.get(User, int(user_id))
    if not user:
        raise credentials_exception
    return user
```

---

## 3. `main.py` com carregamento automático de routers

### src/main.py

```python
import pkgutil
import importlib
from fastapi import FastAPI

from db import create_db_and_tables

def get_app() -> FastAPI:
    app = FastAPI(title="Backend Simples")

    # Cria tabelas no startup (útil em dev)
    create_db_and_tables()

    # Importa dinamicamente todos os routers em features/*/router.py
    import features
    for _, module_name, _ in pkgutil.iter_modules(features.__path__):
        module = importlib.import_module(f"features.{module_name}.router")
        app.include_router(module.router)

    return app

app = get_app()
```

---

## 4. Features

### 4.1 Users

#### src/features/users/model.py

```python
from uuid import UUID, uuid4
from typing import Optional
from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    uuid: UUID = Field(default_factory=uuid4, unique=True, index=True)
    name: str
    email: str = Field(unique=True, index=True)
    hashed_password: str

class UserDepartamentoLink(SQLModel, table=True):
    user_id: Optional[int] = Field(
        default=None, foreign_key="user.id", primary_key=True
    )
    departamento_id: Optional[int] = Field(
        default=None, foreign_key="departamento.id", primary_key=True
    )

class UserCargoLink(SQLModel, table=True):
    user_id: Optional[int] = Field(
        default=None, foreign_key="user.id", primary_key=True
    )
    cargo_id: Optional[int] = Field(
        default=None, foreign_key="cargo.id", primary_key=True
    )
```

#### src/features/users/crud.py

```python
from typing import List
from sqlmodel import Session, select

from .model import User, UserDepartamentoLink, UserCargoLink
from features.departamentos.model import Departamento
from features.cargos.model import Cargo
from security import get_password_hash

# user
def get_user(session: Session, user_id: int) -> User | None:
    return session.get(User, user_id)

def get_user_by_email(session: Session, email: str) -> User | None:
    stmt = select(User).where(User.email == email)
    return session.exec(stmt).first()

def get_users(session: Session, skip: int = 0, limit: int = 100) -> List[User]:
    stmt = select(User).offset(skip).limit(limit)
    return session.exec(stmt).all()

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

# departamentos associados
def list_departamentos(session: Session, user_id: int) -> List[Departamento]:
    stmt = (
        select(Departamento)
        .join(UserDepartamentoLink)
        .where(UserDepartamentoLink.user_id == user_id)
    )
    return session.exec(stmt).all()

def assign_departamento(session: Session, user_id: int, dept_id: int):
    link = UserDepartamentoLink(user_id=user_id, departamento_id=dept_id)
    session.add(link)
    session.commit()

def remove_departamento(session: Session, user_id: int, dept_id: int):
    stmt = select(UserDepartamentoLink).where(
        UserDepartamentoLink.user_id == user_id,
        UserDepartamentoLink.departamento_id == dept_id
    )
    link = session.exec(stmt).first()
    if link:
        session.delete(link)
        session.commit()

# cargos associados
def list_cargos(session: Session, user_id: int) -> List[Cargo]:
    stmt = (
        select(Cargo)
        .join(UserCargoLink)
        .where(UserCargoLink.user_id == user_id)
    )
    return session.exec(stmt).all()

def assign_cargo(session: Session, user_id: int, cargo_id: int):
    link = UserCargoLink(user_id=user_id, cargo_id=cargo_id)
    session.add(link)
    session.commit()

def remove_cargo(session: Session, user_id: int, cargo_id: int):
    stmt = select(UserCargoLink).where(
        UserCargoLink.user_id == user_id,
        UserCargoLink.cargo_id == cargo_id
    )
    link = session.exec(stmt).first()
    if link:
        session.delete(link)
        session.commit()
```

#### src/features/users/router.py

```python
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from db import get_session
from .crud import (
    get_user, get_users, create_user,
    list_departamentos, assign_departamento, remove_departamento,
    list_cargos, assign_cargo, remove_cargo
)
from security import get_current_user
from .model import User

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=List[User])
def read_users(
    skip: int = 0, limit: int = 100,
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),
):
    return get_users(session, skip, limit)

@router.post("/", response_model=User)
def create_new_user(
    name: str, email: str, password: str,
    session: Session = Depends(get_session),
):
    return create_user(session, name, email, password)

@router.get("/{user_id}", response_model=User)
def read_user(
    user_id: int,
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),
):
    user = get_user(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user

# Associação departamentos
@router.get("/{user_id}/departamentos")
def get_user_departamentos(
    user_id: int,
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),
):
    return list_departamentos(session, user_id)

@router.post("/{user_id}/departamentos/{dept_id}")
def add_departamento_to_user(
    user_id: int, dept_id: int,
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),
):
    assign_departamento(session, user_id, dept_id)
    return {"msg": "Departamento associado"}

@router.delete("/{user_id}/departamentos/{dept_id}")
def del_departamento_from_user(
    user_id: int, dept_id: int,
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),
):
    remove_departamento(session, user_id, dept_id)
    return {"msg": "Associação removida"}

# Associação cargos
@router.get("/{user_id}/cargos")
def get_user_cargos(
    user_id: int,
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),
):
    return list_cargos(session, user_id)

@router.post("/{user_id}/cargos/{cargo_id}")
def add_cargo_to_user(
    user_id: int, cargo_id: int,
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),
):
    assign_cargo(session, user_id, cargo_id)
    return {"msg": "Cargo associado"}

@router.delete("/{user_id}/cargos/{cargo_id}")
def del_cargo_from_user(
    user_id: int, cargo_id: int,
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),
):
    remove_cargo(session, user_id, cargo_id)
    return {"msg": "Associação removida"}
```

---

### 4.2 Departamentos

#### src/features/departamentos/model.py

```python
from typing import Optional
from sqlmodel import SQLModel, Field

class Departamento(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
```

#### src/features/departamentos/crud.py

```python
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
```

#### src/features/departamentos/router.py

```python
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from db import get_session
from .crud import get_departamento, get_departamentos, create_departamento
from security import get_current_user
from .model import Departamento

router = APIRouter(prefix="/departamentos", tags=["departamentos"])

@router.get("/", response_model=List[Departamento])
def read_departamentos(
    skip: int = 0, limit: int = 100,
    session: Session = Depends(get_session),
    _: Departamento = Depends(get_current_user),
):
    return get_departamentos(session, skip, limit)

@router.post("/", response_model=Departamento)
def create_new_departamento(
    name: str,
    session: Session = Depends(get_session),
    _: Departamento = Depends(get_current_user),
):
    return create_departamento(session, name)

@router.get("/{dept_id}", response_model=Departamento)
def read_departamento(
    dept_id: int,
    session: Session = Depends(get_session),
    _: Departamento = Depends(get_current_user),
):
    dept = get_departamento(session, dept_id)
    if not dept:
        raise HTTPException(status_code=404, detail="Departamento não encontrado")
    return dept
```

---

### 4.3 Cargos

#### src/features/cargos/model.py

```python
from typing import Optional
from sqlmodel import SQLModel, Field

class Cargo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
```

#### src/features/cargos/crud.py

```python
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
```

#### src/features/cargos/router.py

```python
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from db import get_session
from .crud import get_cargo, get_cargos, create_cargo
from security import get_current_user
from .model import Cargo

router = APIRouter(prefix="/cargos", tags=["cargos"])

@router.get("/", response_model=List[Cargo])
def read_cargos(
    skip: int = 0, limit: int = 100,
    session: Session = Depends(get_session),
    _: Cargo = Depends(get_current_user),
):
    return get_cargos(session, skip, limit)

@router.post("/", response_model=Cargo)
def create_new_cargo(
    name: str,
    session: Session = Depends(get_session),
    _: Cargo = Depends(get_current_user),
):
    return create_cargo(session, name)

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
```

---

### 4.4 Autenticação

#### src/features/auth/router.py

```python
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from datetime import timedelta
from pydantic import BaseModel

from db import get_session
from security import authenticate_user, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

class Token(BaseModel):
    access_token: str
    token_type: str

@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        {"sub": str(user.id)}, expires_delta=timedelta(minutes=60)
    )
    return {"access_token": access_token, "token_type": "bearer"}
```

---

### Como adicionar novas tabelas/endpoints

1. Crie em `src/features/<nova_feature>/` os arquivos `model.py`, `crud.py` e `router.py`.
2. Defina o modelo com `SQLModel(table=True)`, funções CRUD em `crud.py` e rotas com `APIRouter` em `router.py`.
3. No próximo `uvicorn src.main:app --reload`, ele vai “auto-scan” e já expor suas rotas em `/nova_feature`.

Pronto: algo VERY simple, mas já seguro (hash de senha, JWT, dependência de autenticação) e fácil de estender.
