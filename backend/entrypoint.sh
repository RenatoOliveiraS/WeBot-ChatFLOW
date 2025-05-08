#!/bin/bash

# Função para verificar se o PostgreSQL está pronto
wait_for_postgres() {
    echo "Aguardando PostgreSQL..."
    while ! nc -z postgres 5432; do
        sleep 1
    done
    echo "PostgreSQL está pronto!"
}

# Instala netcat para verificar a conexão com o PostgreSQL
apt-get update && apt-get install -y netcat-openbsd

# Aguarda o PostgreSQL ficar pronto
wait_for_postgres

# Executa as migrações
echo "Executando migrações..."
alembic upgrade head

# Executa o seed do admin
echo "Criando usuário admin..."
cd /app && python -m scripts.seed_admin

# Inicia a aplicação
echo "Iniciando a aplicação..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 