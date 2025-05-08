FROM python:3.11-slim

WORKDIR /app

# Instala dependências do sistema
RUN apt-get update --fix-missing \
    && apt-get install -y --no-install-recommends \
        gcc \
        libpq-dev \
        netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Copia e instala dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir alembic

# Copia o código fonte
COPY . .

# Torna o entrypoint executável
RUN chmod +x entrypoint.sh

# Define o entrypoint
ENTRYPOINT ["./entrypoint.sh"]