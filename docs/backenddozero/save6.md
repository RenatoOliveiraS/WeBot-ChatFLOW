Abaixo segue o **save6.md** completo, gerado do zero a partir da estrutura atual em `backend/src` e `backend/src/features`. Ele resume visão geral, pré-requisitos, estrutura de pastas, configuração, principais arquivos e todas as features já implementadas.

````markdown
## 1. Visão Geral

Este backend é construído com **FastAPI** e **SQLModel**, organizado por features carregadas dinamicamente em `main.py`.  
Principais características:
- **Auth JWT** com *OAuth2PasswordBearer* e *PyJWT*  
- **Hash de senha** via PassLib/Bcrypt  
- **Relacionamentos many-to-many** (usuários ↔ departamentos/cargos)  
- **Seed automático** de usuário _admin_, departamento _“Administrador”_ e cargo _“Administrador”_  
:contentReference[oaicite:1]{index=1}

---

## 2. Pré-requisitos

- **Python 3.10+**  
- Dependências (em `requirements.txt` ou `pyproject.toml`):  
  - fastapi  
  - uvicorn  
  - sqlmodel  
  - passlib\[bcrypt]  
  - python-jwt (PyJWT)  
  - python-dotenv  
  - psycopg2-binary (opcional para PostgreSQL)  
  - python-multipart (para formulários de login)  
:contentReference[oaicite:3]{index=3}

---

## 3. Estrutura de Pastas

```plain
backend/
└── src/
    ├── __init__.py
    ├── main.py           # cria app, registra routers de features, cria tables e seed_admin_user()
    ├── config.py         # carrega .env, valida SECRET_KEY e vars ADMIN_*
    ├── db.py             # engine e get_session()
    ├── security.py       # authenticate_user, create_access_token, get_current_user
    ├── utils.py          # get_password_hash, verify_password
    └── features/
        ├── __init__.py
        ├── auth/
        │   └── router.py
        ├── users/
        │   ├── model.py
        │   ├── schemas.py
        │   ├── crud.py
        │   └── router.py
        ├── departamentos/
        │   ├── model.py
        │   ├── crud.py
        │   └── router.py
        ├── cargos/
        │   ├── model.py
        │   ├── crud.py
        │   └── router.py
        ├── email_connections/
        │   ├── model.py
        │   ├── crud.py
        │   ├── service.py
        │   └── router.py
        ├── inbound_emails/
        │   ├── model.py
        │   ├── crud.py
        │   ├── service.py
        │   └── router.py
        └── outbound_emails/
            ├── model.py
            ├── service.py
            └── router.py
````

---

## 4. Configuração

1. Na raiz `backend/`, crie o arquivo `.env` com:

   ```dotenv
   DATABASE_URL=sqlite:///./dev.db
   SECRET_KEY=<sua_chave_forte>
   ACCESS_TOKEN_EXPIRE_MINUTES=60
   ADMIN_NAME=Administrador
   ADMIN_EMAIL=admin@webot.com
   ADMIN_PASSWORD=WeBot@1234
   FERNET_KEY=<chave_base64_32_bytes>  # para criptografia de senhas em email_connections
   ```
2. Em `config.py`, use `load_dotenv()` e exponha tudo via `settings` (levanta erro se faltar SECRET\_KEY, ADMIN\_\* ou FERNET\_KEY).


---

## 5. Principais Arquivos

### main.py

* Registra automaticamente todos os `APIRouter(prefix="/<feature>")` em `features/*/router.py`.
* Executa `SQLModel.metadata.create_all(engine)` e `seed_admin_user()` (garante admin, departamento e cargo).

### config.py

* Carrega e valida variáveis de ambiente.

### db.py

* `engine = create_engine(settings.DATABASE_URL)`
* `get_session()` retorna `Session` por dependência.

### security.py

* `authenticate_user()`, `create_access_token()`, `get_current_user()` usando JWT.
* `OAuth2PasswordBearer(tokenUrl="auth/login")` (exige python-multipart).

### utils.py

* `get_password_hash()`, `verify_password()` com PassLib/Bcrypt.


---

## 6. Features

### 6.1 Auth

* **POST** `/auth/login` (form-url-encoded) recebe `username` e `password`, retorna `{ access_token }`.


### 6.2 Users

* **model.py**: `User`, `UserDepartamentoLink`, `UserCargoLink`
* **schemas.py**: `UserRead`, `DepartamentoRead`, `CargoRead`
* **crud.py**: CRUD de usuários e associações (UUID)
* **router.py**:

  * **POST** `/users/` cria usuário (Bearer admin)
  * **GET** `/users/?skip=&limit=` lista
  * **GET** `/users/{user_uuid}` detalhes
  * **GET/POST/DELETE** associações de departamentos e cargos


### 6.3 Departamentos & Cargos

Para cada:

* **model.py**, **crud.py** e **router.py**
* **GET** lista, **POST** cria e **GET** detalhe


### 6.4 Email Connections

* **model.py**: `EmailConnection` com campos básicos + timestamps.
* **crud.py**: operações CRUD.
* **service.py**: `encrypt_password()`, `decrypt_password()`, `test_email_connection()`.
* **router.py**:

  * **GET** `/email-connections/`
  * **GET/POST/PUT/DELETE** `/email-connections/{id}`
  * **POST** `/email-connections/{id}/test`
* Usa `FERNET_KEY` para criptografia em servidor.


### 6.5 Inbound Emails

* **model.py**: `InboundEmail` (headers, corpo, anexos, JSON em colunas).
* **crud.py**: `create_inbound_email()`, `get_inbound_emails()`, `get_inbound_email()`.
* **service.py**:

  * `ingest_raw_email()` (parse RFC-822/MIME)
  * `fetch_inbound_emails()` (IMAP UNSEEN)
* **router.py**:

  * **POST** `/inbound-emails/webhook`
  * **POST** `/email-connections/{id}/fetch`
  * **GET** `/inbound-emails` e `/inbound-emails/{email_id}`


### 6.6 Outbound Emails

* **model.py**: `SendEmailPayload`, `ReplyEmailPayload`.
* **service.py**: `send_email()`: busca conexão SMTP, descriptografa senha, monta mensagem (headers/IDs), envia via `smtplib`.
* **router.py**:

  * **POST** `/outbound-emails/send`
  * **POST** `/outbound-emails/{inbound_email_id}/reply`
* Cuidados: timeouts, exceções, testes com `smtpd.DebuggingServer`.


---

## 7. Como adicionar nova **feature**

1. Crie pasta `src/features/<nome>/` com `__init__.py`.
2. Dentro, crie:

   * `model.py` com `class X(SQLModel, table=True)` (+ relações)
   * `crud.py` com lógica de DB
   * `router.py` com `APIRouter(prefix="/<nome>")`
3. Reinicie Uvicorn: a rota será registrada automaticamente.


---

## 8. Execução

```bash
cd backend
uvicorn src.main:app --reload
```

* **Swagger UI**: `http://127.0.0.1:8000/docs`
* **OpenAPI JSON**: `http://127.0.0.1:8000/openapi.json`

```

Qualquer ajuste ou feature nova, basta seguir o padrão acima e atualizar este save6.
```
