---

## 1. Visão Geral

Este backend continua implementado em **FastAPI** + **SQLModel**, agora com:

* **Organização por features** (*auth*, *users*, *departamentos*, *cargos*) carregadas dinamicamente em `main.py`
* **Autenticação JWT** via *OAuth2PasswordBearer* e *PyJWT*
* **Hash de senha** com **bcrypt** (PassLib)
* **Relacionamentos many-to-many** entre usuários e departamentos/cargos, mapeados com *link tables*
* **Seed automático**: na inicialização, cria um usuário *admin*, o departamento **“Administrador”** e o cargo **“Administrador”**, e associa tudo automaticamente



---

## 2. Pré-requisitos

* **Python 3.10+**
* Dependências (adicione em `requirements.txt` ou `pyproject.toml`):

  * fastapi
  * uvicorn
  * sqlmodel
  * passlib\[bcrypt]
  * python-jwt (PyJWT)
  * python-dotenv
  * psycopg2-binary (opcional, para PostgreSQL)
  * **python-multipart** (necessário para `OAuth2PasswordRequestForm`)

---

## 3. Estrutura de Pastas

```
backend/
└── src/
    ├── __init__.py
    ├── main.py             # FastAPI app, inclui routers, depois create_all e seed_admin_user
    ├── config.py           # carrega .env, valida SECRET_KEY e ADMIN_*
    ├── db.py               # engine, get_session()
    ├── security.py         # authenticate_user, create_access_token, get_current_user
    ├── utils.py            # get_password_hash, verify_password
    └── features/
        ├── __init__.py
        ├── auth/
        │   └── router.py   # POST /auth/login (form-urlencoded)
        ├── users/
        │   ├── model.py    # User, UserDepartamentoLink, UserCargoLink, relacionamentos
        │   ├── crud.py     # CRUD de User + associações por UUID
        │   ├── schemas.py  # UserRead, DepartamentoRead, CargoRead (sem senha)
        │   └── router.py   # /users (CRUD e vinculações com UUID)
        ├── departamentos/
        │   ├── model.py
        │   ├── crud.py     # get/create by name + CRUD básico
        │   └── router.py   # /departamentos (JSON body, protegido)
        └── cargos/
            ├── model.py
            ├── crud.py
            └── router.py   # /cargos (JSON body, protegido)
```

---

## 4. Configuração

1. Crie o arquivo `.env` **na raiz** do projeto (`backend/.env`), incluindo **também** as vars para seed do admin:

   ```dotenv
   DATABASE_URL=sqlite:///./dev.db
   SECRET_KEY=<sua_chave_forte_gerada>
   ACCESS_TOKEN_EXPIRE_MINUTES=60
   ADMIN_NAME=Administrador
   ADMIN_EMAIL=admin@webot.com
   ADMIN_PASSWORD=WeBot@1234
   ```
2. Em `config.py`, as variáveis são carregadas com `load_dotenv()`, validadas (levanta erro se `SECRET_KEY` faltar ou for padrão) e expostas via um objeto `settings`.

---

## 5. Principais Arquivos

### **main.py**

* **Registro dinâmico** de todos os routers de `features/*/router.py`.
* Depois, chama `SQLModel.metadata.create_all(engine)` (agora só após importar modelos) e `seed_admin_user()` que:

  1. Garante criação do *admin* (se não existir).
  2. Garante existência do departamento **“Administrador”** e do cargo **“Administrador”** e os associa ao admin.

### **db.py**

* Define `engine = create_engine(settings.DATABASE_URL)`
* `get_session()` retorna `Session` por dependência.

### **security.py**

* `authenticate_user()`, `create_access_token()`, `get_current_user()` usando JWT com `SECRET_KEY`.
* `OAuth2PasswordBearer(tokenUrl="auth/login")` exige **python-multipart** instalado.

### **utils.py**

* `get_password_hash()` e `verify_password()` com passlib.bcrypt.

---

## 6. Endpoints

### 6.1 Auth

| Método | Rota          | Corpo                  | Protegido | Descrição                  |
| ------ | ------------- | ---------------------- | --------- | -------------------------- |
| POST   | `/auth/login` | x-www-form-urlencoded: | não       | Retorna `{ access_token }` |
|        |               | • `username`           |           |                            |
|        |               | • `password`           |           |                            |

> **Atenção:** requer `python-multipart` instalado.

### 6.2 Users

| Método | Rota                                    | Corpo JSON ou Path-param                   | Protegido? | Descrição                                                   |
| ------ | --------------------------------------- | ------------------------------------------ | ---------- | ----------------------------------------------------------- |
| POST   | `/users/`                               | JSON ou query: `{ name, email, password }` | sim\*      | Cria usuário + associa departamento/cargo **Administrador** |
| GET    | `/users/?skip=&limit=`                  | —                                          | sim        | Lista usuários com departamentos e cargos                   |
| GET    | `/users/{user_uuid}`                    | Path-param `UUID`                          | sim        | Detalha usuário com relacionamentos                         |
| GET    | `/users/{user_uuid}/departamentos`      | Path-param `UUID`                          | sim        | Lista departamentos do usuário                              |
| POST   | `/users/{user_uuid}/departamentos/{id}` | Path-param `UUID`, `int`                   | sim        | Associa departamento                                        |
| DELETE | `/users/{user_uuid}/departamentos/{id}` | Path-param `UUID`, `int`                   | sim        | Remove associação                                           |
| GET    | `/users/{user_uuid}/cargos`             | Path-param `UUID`                          | sim        | Lista cargos do usuário                                     |
| POST   | `/users/{user_uuid}/cargos/{id}`        | Path-param `UUID`, `int`                   | sim        | Associa cargo                                               |
| DELETE | `/users/{user_uuid}/cargos/{id}`        | Path-param `UUID`, `int`                   | sim        | Remove associação                                           |

> \* Para criar usuário é preciso passar o *Bearer token* de um admin já existente.

### 6.3 Departamentos e Cargos

| Método | Rota                  | Corpo JSON          | Protegido? | Descrição               |
| ------ | --------------------- | ------------------- | ---------- | ----------------------- |
| GET    | `/departamentos/`     | —                   | sim        | Lista todos             |
| POST   | `/departamentos/`     | `{ "name": "..." }` | sim        | Cria novo               |
| GET    | `/departamentos/{id}` | —                   | sim        | Detalha um departamento |
| GET    | `/cargos/`            | —                   | sim        | Lista todos             |
| POST   | `/cargos/`            | `{ "name": "..." }` | sim        | Cria novo               |
| GET    | `/cargos/{id}`        | —                   | sim        | Detalha um cargo        |

---

## 7. Como adicionar nova **feature**

1. Crie pasta `src/features/<nome>/` com `__init__.py`.
2. Dentro:

   * `model.py` com `class X(SQLModel, table=True)` e, se precisar, `Relationships`.
   * `crud.py` com lógica de DB.
   * `router.py` com `APIRouter(prefix="/<nome>")`.
3. Reinicie Uvicorn; a rota será auto-registrada.

---

## 8. Execução

```bash
cd backend
uvicorn src.main:app --reload
```

* **Swagger UI**: `http://127.0.0.1:8000/docs`
* **OpenAPI JSON**: `http://127.0.0.1:8000/openapi.json`

---


````markdown
## 9. Email Connections

Esta seção descreve o modelo, CRUD, serviço de teste e rotas para gerenciar conexões SMTP, com criptografia de senha 100% no servidor.

| Método | Rota                           | Corpo JSON                                                                                                 | Protegido | Descrição                                                       |
| ------ | ------------------------------ | ----------------------------------------------------------------------------------------------------------- | --------- | --------------------------------------------------------------- |
| GET    | `/email‐connections/`          | —                                                                                                           | sim       | Lista todas as conexões SMTP                                   |
| GET    | `/email‐connections/{id}`      | —                                                                                                           | sim       | Detalha uma conexão SMTP específica                             |
| POST   | `/email‐connections/`          | `{ name, smtp_server, smtp_port, username, password, use_tls, use_ssl, default, from_email }`                | sim       | Cria nova conexão (senha em texto puro; servidor encripta)      |
| PUT    | `/email‐connections/{id}`      | `{ name?, smtp_server?, smtp_port?, username?, password?, use_tls?, use_ssl?, default?, from_email? }`      | sim       | Atualiza conexão (criptografa senha se fornecida)              |
| DELETE | `/email‐connections/{id}`      | —                                                                                                           | sim       | Remove conexão SMTP                                            |
| POST   | `/email‐connections/{id}/test` | —                                                                                                           | sim       | Testa na prática a conexão SMTP configurada                     |

---

### 9.1 Model (`model.py`)
```python
class EmailConnection(EmailConnectionBase, table=True):
    id: Optional[int] = Field(None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
````

Define campos como `password_encrypted: str` — a criptografia fica a cargo do servidor.

### 9.2 CRUD (`crud.py`)

* `get_email_connections(db)`
* `get_email_connection(db, id)`
* `create_email_connection(db, data: EmailConnection)`
* `update_email_connection(db, id, data: EmailConnection)`
* `delete_email_connection(db, id)`

### 9.3 Service (`service.py`)

```python
def encrypt_password(plain: str) -> str
def decrypt_password(encrypted: str) -> str
def test_email_connection(connection: EmailConnection) -> None
```

* Usa `FERNET_KEY` do `.env` para encriptar/descriptar.
* `test_email_connection` abre SMTP/SSL, faz `starttls` se necessário e `login`.

### 9.4 Router (`router.py`)

* **Schemas**:

  * `EmailConnectionCreate`: recebe `password` em texto puro.
  * `EmailConnectionUpdate`: permite atualizar senha (`password`) opcionalmente.
* **Endpoints**:

  * `/` (GET, POST)
  * `/{id}` (GET, PUT, DELETE)
  * `/{id}/test` (POST)

Em todos, adiciona `Depends(get_current_user)` para exigir JWT.

### 9.5 Configuração

1. Adicione no **`backend/.env`**:

   ```dotenv
   FERNET_KEY=<chave_base64_32_bytes>
   ```
2. Certifique-se de usar `load_dotenv()` em `config.py`.

---

> Este **save3** reflete todas as mudanças da feature **email\_connections**: desde o **modelo** até o **endpoint de teste** SMTP, garantindo que a **criptografia de senha** seja totalmente feita no servidor .

---

````markdown
## 10. Inbound Emails

Essa feature permite receber e armazenar e-mails tanto via webhook (raw MIME) quanto via polling IMAP das mesmas conexões já cadastradas em `email_connections`.

| Método | Rota                                            | Corpo JSON                            | Protegido | Descrição                                                                                       |
| ------ | ----------------------------------------------- | ------------------------------------- | --------- | ------------------------------------------------------------------------------------------------ |
| POST   | `/inbound-emails/webhook`                       | `{ "raw": "<RFC-822/MIME completo>" }`| não       | Recebe e-mail bruto de provedor externo (webhook) e persiste como `InboundEmail`                 |
| POST   | `/email-connections/{id}/fetch`                 | —                                     | sim       | Conecta via IMAP usando a conexão `{id}`, busca UNSEEN, persiste no banco e marca como SEEN      |
| GET    | `/inbound-emails`                               | —                                     | sim       | Lista todos os e-mails recebidos                                                                 |
| GET    | `/inbound-emails/{email_id}`                    | —                                     | sim       | Detalha um e-mail específico                                                                     |

---

### 10.1 Model (`model.py`)

```python
class InboundEmail(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    message_id: str                                # unique, index
    from_address: str
    to_addresses: List[str] = Field(sa_column=Column(JSON))
    subject: Optional[str] = None
    date: datetime
    body_text: Optional[str] = None
    body_html: Optional[str] = None
    raw_headers: dict      = Field(sa_column=Column(JSON))
    attachments: List[dict]= Field(sa_column=Column(JSON))
    created_at: datetime   = Field(default_factory=datetime.utcnow)
````

### 10.2 CRUD (`crud.py`)

```python
def create_inbound_email(db: Session, email: InboundEmail) -> InboundEmail
def get_inbound_emails(db: Session) -> List[InboundEmail]
def get_inbound_email(db: Session, email_id: int) -> InboundEmail
```

### 10.3 Service (`service.py`)

* **`ingest_raw_email(db, raw: str)`**
  — parseia a string RFC-822/MIME, extrai cabeçalhos, corpo, anexos e chama `create_inbound_email`.

* **`fetch_inbound_emails(connection, db)`**
  — conecta via IMAP (UNSEEN), itera sobre mensagens, converte cada raw com `ingest_raw_email` e marca como lida.

### 10.4 Router (`router.py`)

```python
@router.post("/webhook", status_code=201)
def receive_email(payload: RawEmailPayload, db: Session)

@router.post("/email-connections/{id}/fetch", status_code=200)
def fetch_emails(connection_id: int, db: Session)

@router.get("/inbound-emails", response_model=List[InboundEmail])
def list_emails(db: Session)

@router.get("/inbound-emails/{email_id}", response_model=InboundEmail)
def retrieve_email(email_id: int, db: Session)
```

* **`RawEmailPayload`**: `{ raw: str }` — payload do webhook.

### 10.5 Uso

1. **Webhook**

   * Configure seu provedor (Mailgun/SendGrid) para enviar o raw completo em JSON `{ "raw": "..." }` para `POST /inbound-emails/webhook`.

2. **Polling manual**

   * Use `POST /email-connections/{id}/fetch` para forçar a leitura de novos e-mails via IMAP.

3. **Consulta**

   * `GET /inbound-emails` — lista (paginar com `skip`/`limit`).
   * `GET /inbound-emails/{id}` — detalhes de um e-mail.

---

Esse **save4** consolida toda a solução de recebimento e armazenamento de e-mails inbound, usando SQLModel para persistência e aproveitando suas conexões SMTP/IMAP já configuradas. \`\`\`
