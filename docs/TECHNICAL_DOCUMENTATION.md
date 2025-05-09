# WeBot ChatFLOW - Documentação Técnica

## Índice
1. [Estrutura do Projeto](#estrutura-do-projeto)
2. [Módulo de Usuários](#módulo-de-usuários)
3. [Módulo de Autenticação](#módulo-de-autenticação)
4. [Guia de Implementação de Novos Módulos](#guia-de-implementação-de-novos-módulos)
5. [Guia de Docker e Migrations](#guia-de-docker-e-migrations)

## Estrutura do Projeto
```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── controllers/
│   │       ├── routes/
│   │       └── dtos/
│   ├── domain/
│   │   └── entities/
│   ├── infrastructure/
│   │   ├── database/
│   │   └── repositories/
│   ├── repositories/
│   ├── use_cases/
│   └── core/
│       ├── auth/
│       └── config/
```

## Módulo de Usuários

### Estrutura de Arquivos
```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── controllers/
│   │       │   └── user_controller.py
│   │       ├── routes/
│   │       │   ├── __init__.py
│   │       │   └── user_routes.py
│   │       └── dtos/
│   │           └── user_dto.py
│   ├── domain/
│   │   └── entities/
│   │       └── user.py
│   ├── infrastructure/
│   │   ├── database/
│   │   │   └── models/
│   │   │       └── user.py
│   │   └── repositories/
│   │       └── postgres_user_repository.py
│   ├── repositories/
│   │   └── user_repository.py
│   └── use_cases/
│       └── user/
│           ├── create_user.py
│           ├── get_user.py
│           ├── list_users.py
│           ├── update_user.py
│           └── delete_user.py
```

### Endpoints Disponíveis
- POST `/api/v1/users` - Criar usuário
- GET `/api/v1/users` - Listar usuários
- GET `/api/v1/users/{user_id}` - Obter usuário por ID
- GET `/api/v1/users/email/{email}` - Obter usuário por email
- PUT `/api/v1/users/{user_id}` - Atualizar usuário
- DELETE `/api/v1/users/{user_id}` - Deletar usuário

### Exemplo de Prompt para Alterações
```
Módulo de Usuários
O que você deseja realizar: Incluir no modelo de usuário o campo <campo> 

Pastas/arquivos que precisam de ajustes:
- backend/app/api/v1/dtos/user_dto.py
- backend/app/infrastructure/database/models/user.py
- backend/app/migrations/      ← criar revisão Alembic
- backend/app/repositories/user_repository.py
- backend/app/use_cases/user/create_user.py
- backend/app/use_cases/user/update_user.py
- backend/app/api/v1/controllers/user_controller.py
- backend/app/api/v1/routes/user_routes.py
- app/tests/user/

Passos para aplicar as alterações:
1. Desenvolvimento Local:
   - Criar migration: `alembic revision --autogenerate -m "add <campo> column"`
   - Verificar migration gerada
   - Aplicar migration: `alembic upgrade head`
   - Testar alterações

2. Docker:
   ```bash
   docker compose down
   docker compose build backend
   docker compose up
   ```

3. Novo Ambiente:
   - Migration aplicada automaticamente ao iniciar container
   - Banco criado com estrutura atualizada
```

## Módulo de Autenticação

### Estrutura de Arquivos
```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── controllers/
│   │       │   └── auth_controller.py
│   │       ├── routes/
│   │       │   ├── __init__.py
│   │       │   └── auth_routes.py
│   │       └── dtos/
│   │           └── auth_dto.py
│   ├── core/
│   │   ├── auth/
│   │   │   ├── jwt_handler.py
│   │   │   └── password_handler.py
│   │   └── config/
│   │       └── settings.py
│   └── use_cases/
│       └── auth/
│           └── authenticate_user.py
```

### Endpoints de Autenticação
- POST `/api/v1/auth/login` - Login de usuário
- POST `/api/v1/auth/refresh` - Renovar token (se implementado)
- POST `/api/v1/auth/logout` - Logout (se implementado)

### Fluxo de Autenticação
1. **Login**
   ```python
   POST /api/v1/auth/login
   {
       "email": "usuario@exemplo.com",
       "password": "senha123"
   }
   ```

2. **Resposta**
   ```python
   {
       "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
       "token_type": "bearer"
   }
   ```

3. **Uso do Token**
   - Header: `Authorization: Bearer {token}`

### Exemplo de Prompt para Autenticação
```
Módulo de Autenticação
O que você deseja realizar: Implementar suporte a refresh tokens JWT

Pastas/arquivos que precisam de ajustes:
- backend/app/api/v1/dtos/auth_dto.py
- backend/app/infrastructure/database/models/refresh_token.py
- backend/app/migrations/      ← criar revisão Alembic para tabela `refresh_tokens`
- backend/app/repositories/auth_repository.py
- backend/app/use_cases/auth/login_user.py
- backend/app/use_cases/auth/refresh_token.py
- backend/app/api/v1/controllers/auth_controller.py
- backend/app/api/v1/routes/auth_routes.py
- app/tests/auth/      ← testes de fluxo de login e refresh token
- docker-compose.yml   ← configurar contêiner de DB e rodar migrações na inicialização
- backend/Dockerfile   ← adicionar Alembic e scripts de bootstrap

Passos para aplicar as alterações:
1. Desenvolvimento Local:
   - Criar migration: `alembic revision --autogenerate -m "add refresh tokens table"`
   - Verificar migration gerada
   - Aplicar migration: `alembic upgrade head`
   - Testar alterações

2. Docker:
   ```bash
   docker compose down
   docker compose build backend
   docker compose up
   ```

3. Novo Ambiente:
   - Migration aplicada automaticamente ao iniciar container
   - Banco criado com estrutura atualizada
```

## Guia de Docker e Migrations

### Comandos Essenciais
```bash
# Criar migration
docker compose exec backend bash
alembic revision --autogenerate -m "descrição"

# Aplicar migration
alembic upgrade head

# Reverter última migration
alembic downgrade -1

# Reconstruir e reiniciar
docker compose down
docker compose build backend
docker compose up
```

### Checklist de Deploy
- [ ] Migration criada e testada
- [ ] Código atualizado e testado
- [ ] Imagem Docker reconstruída
- [ ] Migration aplicada
- [ ] Endpoints testados
- [ ] Logs verificados
- [ ] Backup realizado (se necessário)

### Troubleshooting
- Migration falha: `alembic downgrade -1`
- Conflito no banco: 
  ```bash
  docker compose down
  docker volume rm webot-chatflow_postgres_data
  docker compose up
  ```
- Verificar logs: `docker compose logs -f backend`

## Exemplos de Prompts

### 1. Alteração em Módulo Existente
```
Módulo de Usuários
O que você deseja realizar: Incluir no modelo de usuário o campo <campo> 

Pastas/arquivos que precisam de ajustes:
- backend/app/api/v1/dtos/user_dto.py
- backend/app/infrastructure/database/models/user.py
- backend/app/migrations/      ← criar revisão Alembic
- backend/app/repositories/user_repository.py
- backend/app/use_cases/user/create_user.py
- backend/app/use_cases/user/update_user.py
- backend/app/api/v1/controllers/user_controller.py
- backend/app/api/v1/routes/user_routes.py
- app/tests/user/

Passos para aplicar as alterações:
1. Desenvolvimento Local:
   - Criar migration: `alembic revision --autogenerate -m "add <campo> column"`
   - Verificar migration gerada
   - Aplicar migration: `alembic upgrade head`
   - Testar alterações

2. Docker:
   ```bash
   docker compose down
   docker compose build backend
   docker compose up
   ```

3. Novo Ambiente:
   - Migration aplicada automaticamente ao iniciar container
   - Banco criado com estrutura atualizada
```

### 2. Implementação de Autenticação
```
Módulo de Autenticação
O que você deseja realizar: Implementar suporte a refresh tokens JWT

Pastas/arquivos que precisam de ajustes:
- backend/app/api/v1/dtos/auth_dto.py
- backend/app/infrastructure/database/models/refresh_token.py
- backend/app/migrations/      ← criar revisão Alembic para tabela `refresh_tokens`
- backend/app/repositories/auth_repository.py
- backend/app/use_cases/auth/login_user.py
- backend/app/use_cases/auth/refresh_token.py
- backend/app/api/v1/controllers/auth_controller.py
- backend/app/api/v1/routes/auth_routes.py
- app/tests/auth/      ← testes de fluxo de login e refresh token

Passos para aplicar as alterações:
1. Desenvolvimento Local:
   - Criar migration: `alembic revision --autogenerate -m "add refresh tokens table"`
   - Verificar migration gerada
   - Aplicar migration: `alembic upgrade head`
   - Testar alterações

2. Docker:
   ```bash
   docker compose down
   docker compose build backend
   docker compose up
   ```

3. Novo Ambiente:
   - Migration aplicada automaticamente ao iniciar container
   - Banco criado com estrutura atualizada
```

### 3. Implementação de Novo Módulo
```
### Exemplo de Prompt Implementação de Novos Módulos
Implementação de Novos Módulos
O que você deseja realizar: Criar e integrar um novo módulo `<nome_do_módulo>` completo (DTO, Model, Migration, Repositório, Use Cases, Controller, Rotas e Testes)

Pastas/arquivos que precisam de ajustes:
- backend/app/api/v1/dtos/<nome_do_módulo>_dto.py
- backend/app/infrastructure/database/models/<nome_do_módulo>.py
- backend/app/migrations/      ← criar revisão Alembic para tabela `<nome_do_módulo>`
- backend/app/repositories/<nome_do_módulo>_repository.py
- backend/app/use_cases/<nome_do_módulo>/create_<nome_do_módulo>.py
- backend/app/use_cases/<nome_do_módulo>/get_<nome_do_módulo>.py
- backend/app/use_cases/<nome_do_módulo>/update_<nome_do_módulo>.py
- backend/app/api/v1/controllers/<nome_do_módulo>_controller.py
- backend/app/api/v1/routes/<nome_do_módulo>_routes.py
- app/tests/<nome_do_módulo>/      ← testes de CRUD e validações do novo módulo

Passos para aplicar as alterações:
1. Desenvolvimento Local:
   - Criar migration: `alembic revision --autogenerate -m "create <nome_do_módulo> table"`
   - Verificar migration gerada
   - Aplicar migration: `alembic upgrade head`
   - Testar alterações

2. Docker:
   ```bash
   docker compose down
   docker compose build backend
   docker compose up
   ```

3. Novo Ambiente:
   - Migration aplicada automaticamente ao iniciar container
   - Banco criado com estrutura atualizada
```