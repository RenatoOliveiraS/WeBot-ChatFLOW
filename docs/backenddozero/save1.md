**Documentação Simples do Backend**

---

## 1. Visão Geral

Este backend é implementado em **FastAPI** + **SQLModel**, seguindo uma organização por **features**. Tem autenticação via JWT, hash de senha com **bcrypt** e rotas de CRUD para usuários, departamentos e cargos, incluindo associações many-to-many.

---

## 2. Pré-requisitos

* Python 3.10+
* Dependências em `pyproject.toml` ou `requirements.txt`:

  * fastapi
  * uvicorn
  * sqlmodel
  * passlib\[bcrypt]
  * python-jwt (PyJWT)
  * python-dotenv
  * psycopg2-binary (se usar PostgreSQL)

---

## 3. Estrutura de Pastas

```
backend/
└── src/
    ├── __init__.py
    ├── main.py             # entrypoint FastAPI
    ├── config.py           # lê .env (DATABASE_URL, SECRET_KEY…)
    ├── db.py               # engine, sessão e criação de tabelas
    ├── security.py         # JWT, autenticação
    ├── utils.py            # hash e verificação de senha
    └── features/
        ├── __init__.py
        ├── auth/
        │   └ router.py     # POST /auth/login
        ├── users/
        │   ├ model.py      # User, UserDepartamentoLink, UserCargoLink
        │   ├ crud.py       # funções de CRUD e associação
        │   └ router.py     # /users
        ├── departamentos/
        │   ├ model.py      # Departamento
        │   ├ crud.py
        │   └ router.py     # /departamentos
        └── cargos/
            ├ model.py      # Cargo
            ├ crud.py
            └ router.py     # /cargos
```

---

## 4. Configuração

1. Crie arquivo `.env` na raiz de `backend/` com ao menos:

   ```dotenv
   DATABASE_URL=sqlite:///./dev.db
   SECRET_KEY=uma_chave_forte_aqui
   ACCESS_TOKEN_EXPIRE_MINUTES=60
   ```
2. Os valores padrão em `config.py` cuidam de SQLite em dev; para PostgreSQL, basta ajustar `DATABASE_URL`.

---

## 5. Principais Arquivos

* **main.py**

  * Função `get_app()`: cria tabelas (`create_db_and_tables()`) e faz **scan** dinâmico de `features/*/router.py`.

* **db.py**

  * `engine = create_engine(...)`
  * `get_session()` devolve `Session` p/ dependências.

* **security.py**

  * `authenticate_user()`, `create_access_token()`, `get_current_user()`
  * Usa `oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")`

* **utils.py**

  * `get_password_hash()`, `verify_password()` com **passlib.bcrypt**

---

## 6. Endpoints

### 6.1 Auth

| Método | Rota          | Corpo/Form                              | Protegido | Descrição                  |
| ------ | ------------- | --------------------------------------- | --------- | -------------------------- |
| POST   | `/auth/login` | form-urlencoded: `username`, `password` | não       | Retorna `{ access_token }` |

### 6.2 Users

| Método | Rota                            | Corpo JSON                  | Protegido? | Descrição                |
| ------ | ------------------------------- | --------------------------- | ---------- | ------------------------ |
| POST   | `/users/`                       | `{ name, email, password }` | não        | Cria usuário             |
| GET    | `/users/?skip=&limit=`          | —                           | sim        | Lista usuários           |
| GET    | `/users/{user_id}/`             | —                           | sim        | Detalha um usuário       |
| GET    | `/users/{id}/departamentos/`    | —                           | sim        | Departamentos associados |
| POST   | `/users/{id}/departamentos/{d}` | —                           | sim        | Associa departamento     |
| DELETE | `/users/{id}/departamentos/{d}` | —                           | sim        | Remove associação        |
| GET    | `/users/{id}/cargos/`           | —                           | sim        | Cargos associados        |
| POST   | `/users/{id}/cargos/{c}`        | —                           | sim        | Associa cargo            |
| DELETE | `/users/{id}/cargos/{c}`        | —                           | sim        | Remove associação        |

### 6.3 Departamentos e Cargos

| Método | Rota                  | Corpo JSON | Protegido? | Descrição               |
| ------ | --------------------- | ---------- | ---------- | ----------------------- |
| GET    | `/departamentos/`     | —          | sim        | Lista todos             |
| POST   | `/departamentos/`     | `{ name }` | sim        | Cria novo               |
| GET    | `/departamentos/{id}` | —          | sim        | Detalha um departamento |
| GET    | `/cargos/`            | —          | sim        | Lista todos             |
| POST   | `/cargos/`            | `{ name }` | sim        | Cria novo               |
| GET    | `/cargos/{id}`        | —          | sim        | Detalha um cargo        |

---

## 7. Como adicionar nova **feature**

1. Criar pasta `src/features/<nome>/`
2. Dentro dela:

   * `model.py` com `class X(SQLModel, table=True)`
   * `crud.py` com as funções de DB
   * `router.py` com `APIRouter(prefix="/<nome>")`
3. Reiniciar Uvicorn; a rota é auto-registrada.

---

## 8. Execução

```bash
cd backend
uvicorn src.main:app --reload
```

* **Docs interativos**: `http://127.0.0.1:8000/docs`
* **Esquema OpenAPI**: `http://127.0.0.1:8000/openapi.json`

---

Pronto! Com este guia você consegue retomar o projeto em qualquer chat sem perder o contexto.
