# WeBot-ChatFLOW

[![CI Status](https://github.com/RenatoOliveiraS/WeBot-ChatFLOW/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/RenatoOliveiraS/WeBot-ChatFLOW/actions)  
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Repositório de infraestrutura e código do **WeBot-ChatFLOW**, com frontend em React+Vite e backend em Python (FastAPI), orquestrado com Docker Compose e CI/CD via GitHub Actions.

---

## Índice

1. [Pré-requisitos](#pré-requisitos)  
2. [Clone e Setup](#clone-e-setup)  
3. [Scripts Docker](#scripts-docker)  
4. [Variáveis de Ambiente](#variáveis-de-ambiente)  
5. [Executando a Aplicação](#executando-a-aplicação)  
6. [Contribuição](#contribuição)  
7. [Licença](#licença)  
8. [Testes](#testes)

---

## Pré-requisitos

- Git  
- Docker & Docker Compose  
- Node.js ≥ 18  
- Python ≥ 3.10  

---

## ✅ Checklist de Setup

Antes de abrir o seu editor ou começar a escrever código, garanta que **TODOS** os itens abaixo estão concluídos:

- [ ] Clone o repositório  
- [ ] Crie e ative o ambiente virtual Python  
- [ ] `python scripts/setup.py`

**O que esse comando faz** (em ordem):  
1. Cria/atualiza o virtualenv Python e instala dependências  
2. Instala dependências do frontend (`npm install`)  
3. Gera o `.env` a partir de `.env.example` (senhas e `SECRET_KEY` auto-gerados)  
4. Valida todas as variáveis de ambiente (fail-fast se faltar algo)  
5. Puxa imagens públicas e builda as imagens locais Docker  


# Clone e Setup


## 1) Clone o repositório
```bash
git clone https://github.com/RenatoOliveiraS/WeBot-ChatFLOW.git
cd WeBot-ChatFLOW
```
## 2) Crie e ative um ambiente virtual na raiz
```bash
python -m venv .venv
```
### macOS/Linux
```bash
source .venv/bin/activate
```
### Windows PowerShell
```bash
.venv\Scripts\Activate.ps1
```
## 3) Instale as dependências

Você pode instalar todas as dependências, gerar o arquivo `.env`, validar suas variáveis e preparar o Docker com um único comando:

### 💻 Windows (PowerShell)

```powershell
python scripts/setup.py
```


Esse script executa:
- Instalação de dependências Python (`pip install`)
- Instalação de dependências frontend (`npm install`)
- Download das imagens Docker (`docker-compose pull`)


---

## Scripts Docker

_Usando npm scripts (project root):_

```bash

npm run docker:up       # sobe todos os containers em background
npm run docker:logs     # exibe logs em tempo real
npm run docker:down     # derruba containers, redes e volumes
npm run docker:restart  # teardown + provision
npm run docker:migrate   # docker-compose exec backend alembic upgrade head

```

---

## Variáveis de Ambiente

```bash
cp .env.example .env
```

Abra o `.env` e preencha os valores:

| Variável           | Descrição                                   | Exemplo                                       |
|--------------------|---------------------------------------------|-----------------------------------------------|
| POSTGRES_USER      | Usuário do PostgreSQL                       | `postgres`                                    |
| POSTGRES_PASSWORD  | Senha do PostgreSQL                         | `s3nh@S3gur@`                                 |
| POSTGRES_DB        | Nome da base de dados                       | `webot_chatflow`                              |
| DATABASE_URL       | URL de conexão (SQLAlchemy/Alembic)         | `postgresql+psycopg2://postgres:senha@postgres:5432/webot_chatflow` |
| REDIS_PASSWORD     | Senha do Redis                              | `s3nh@R3dis`                                  |
| REDIS_URL          | URL de conexão do Redis                     | `redis://redis:6379/0`                        |
| SECRET_KEY         | Chave secreta para JWT e sessões            | `string_complexa_aleatoria`                   |

---

## Executando a Aplicação

**Frontend (React+Vite)**  
```bash
cd frontend
npm install
npm run dev
```  
Acesse em `http://localhost:3000`.

**Backend (FastAPI)**  
```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```  
Acesse em `http://localhost:8000/docs`.

---

## Contribuição

1. Crie uma branch:  
   ```bash
   git checkout -b feature/minha-nova-funcionalidade
   ```
2. Faça commits claros no estilo **`type(scope): descrição`**.  
3. Abra um Pull Request contra `main` (ou `develop`).  
4. Aguarde revisão com CI verde e, quando aprovado, faça o merge.

---

## Licença

Este projeto está licenciado sob a **MIT License** – veja o arquivo [LICENSE](LICENSE) para mais detalhes.  

## Testes

### Executando os testes localmente

#### Windows (PowerShell)
```powershell
cd backend
.\scripts\run_tests_local.ps1
```

#### Windows (CMD)
```cmd
cd backend
scripts\run_tests_local.bat
```

#### Linux/Mac
```bash
cd backend
./scripts/run_tests_local.sh
```

### Executando os testes com Docker

#### Windows (PowerShell)
```powershell
cd backend
.\scripts\run_tests_docker.ps1
```

#### Windows (CMD)
```cmd
cd backend
scripts\run_tests_docker.bat
```

#### Linux/Mac
```bash
cd backend
./scripts/run_tests_docker.sh
```

### Relatório de cobertura
Após a execução dos testes, um relatório de cobertura em HTML será gerado em `backend/htmlcov/index.html`. Abra este arquivo em seu navegador para visualizar a cobertura de código detalhada.  

## 🐳 Docker Compose

O projeto usa Docker Compose para orquestrar os serviços. Para iniciar todos os serviços, execute:

```bash
docker-compose up --build
```

### Serviços

- **Backend**: API Python em FastAPI
  - Porta: 8000
  - URL: http://localhost:8000

- **Frontend**: Aplicação React
  - Porta: 3000
  - URL: http://localhost:3000

- **PostgreSQL**: Banco de dados
  - Porta: 5432
  - Usuário padrão: webot
  - Senha padrão: secret
  - Banco: webot_db

- **Redis**: Cache e filas
  - Porta: 6379
  - Senha padrão: secret

### Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
# PostgreSQL
POSTGRES_USER=webot
POSTGRES_PASSWORD=secret
POSTGRES_DB=webot_db

# Redis
REDIS_PASSWORD=secret

# Backend
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=admin123

# Frontend
VITE_API_URL=http://localhost:8000
```

### Inicialização Automática

O sistema é configurado para:
1. Aguardar o PostgreSQL estar pronto
2. Executar as migrações do banco de dados
3. Criar o usuário admin
4. Iniciar a aplicação

Tudo isso acontece automaticamente ao executar `docker-compose up --build`.  
o chatgpt esteve aqui 2025-06-04 12:21:22 UTC
