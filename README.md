# WeBot-ChatFLOW

Repositório de infraestrutura e código do projeto WeBot-ChatFLOW.



## Scripts Docker

### Via npm
- `npm run docker:up`       – sobe todos os containers em background  
- `npm run docker:logs`     – exibe logs em tempo real  
- `npm run docker:down`     – derruba containers, redes e volumes  
- `npm run docker:restart`  – faz teardown + provision  


# Variáveis de Ambiente

Para rodar localmente, siga estes passos:

1. Copie o exemplo para gerar o seu `.env`:

cp .env.example .env

2. Abra o arquivo `.env` criado e substitua os valores de placeholder:

POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_postgres_password
POSTGRES_DB=webot_chatflow
DATABASE_URL=postgresql+psycopg2://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres:5432/${POSTGRES_DB}
REDIS_PASSWORD=your_redis_password
REDIS_URL=redis://redis:6379/0
SECRET_KEY=your_secret_key

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
